from __future__ import annotations

import json
from pathlib import Path

from .models import Shot
from .subtitle_generator import generate_subtitles
from .utils import ensure_bin_wrappers, read_json, run, write_json
from .voice_generator import audio_lines


def render(root: Path, shots: list[Shot]) -> Path:
    ensure_bin_wrappers(root)
    generate_subtitles(root, shots)
    ensure_fallback_audio_assets(root)
    shot_paths = []
    for shot in shots:
        out = root / "output" / "shots" / f"{shot.shot_id}.mp4"
        img = root / "assets" / "images" / f"{shot.shot_id}.png"
        vf = _filter_for(shot)
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-t", f"{shot.duration:.3f}", "-i", str(img),
            "-f", "lavfi", "-t", f"{shot.duration:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-vf", vf,
            "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out),
        ]
        run(cmd, root)
        shot_paths.append(out)
        print(f"  ✓ {shot.shot_id}.mp4")
    concat = root / "output" / "shots" / "concat.txt"
    concat.write_text("".join(f"file '{p.resolve()}'\n" for p in shot_paths), encoding="utf-8")
    temp = root / "output" / "episode_001_no_subs.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(temp)], root)
    mixed_audio = build_audio_mix(root, shots)
    srt = root / "output" / "episode_001.srt"
    final = root / "output" / "episode_001.mp4"
    subtitle_filter = (
        f"subtitles={_escape_filter_path(srt)}:"
        "force_style='FontName=DejaVu Sans,FontSize=16,PrimaryColour=&HFFFFFF&,"
        "OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=0,"
        "Alignment=2,MarginV=260'"
    )
    run([
        "ffmpeg", "-y",
        "-i", str(temp),
        "-i", str(mixed_audio),
        "-vf", subtitle_filter,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        "-movflags", "+faststart",
        str(final),
    ], root)
    report = build_report(root, shots, final)
    write_json(root / "output" / "production_report.json", report)
    return final


def ensure_fallback_audio_assets(root: Path) -> None:
    """Create simple local BGM and SFX when publishable audio files are absent."""
    music = root / "assets" / "music" / "background.mp3"
    if not music.exists():
        music.parent.mkdir(parents=True, exist_ok=True)
        run([
            "ffmpeg", "-y", "-f", "lavfi", "-t", "57.2",
            "-i", "sine=frequency=92:sample_rate=44100",
            "-f", "lavfi", "-t", "57.2",
            "-i", "sine=frequency=184:sample_rate=44100",
            "-filter_complex", "[0:a]volume=0.10[a0];[1:a]volume=0.035,tremolo=f=0.22:d=0.65[a1];[a0][a1]amix=inputs=2:duration=longest[a]",
            "-map", "[a]", "-c:a", "libmp3lame", str(music),
        ], root)
    specs = {
        "rain.wav": ("anoisesrc=color=pink:sample_rate=44100", "18", "volume=0.11,highpass=f=600"),
        "thunder.wav": ("sine=frequency=58:sample_rate=44100", "2.3", "volume=0.22,tremolo=f=5:d=0.9"),
        "heartbeat.wav": ("sine=frequency=72:sample_rate=44100", "1.2", "volume=0.25"),
        "crash.wav": ("anoisesrc=color=white:sample_rate=44100", "0.7", "volume=0.28,lowpass=f=1700"),
        "impact.wav": ("sine=frequency=46:sample_rate=44100", "0.8", "volume=0.32"),
    }
    sfx_dir = root / "assets" / "sfx"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    for name, (source, duration, filt) in specs.items():
        path = sfx_dir / name
        if path.exists():
            continue
        run([
            "ffmpeg", "-y", "-f", "lavfi", "-t", duration, "-i", source,
            "-af", filt, "-c:a", "pcm_s16le", str(path),
        ], root)


def build_audio_mix(root: Path, shots: list[Shot]) -> Path:
    out = root / "output" / "episode_001_mix.wav"
    inputs: list[Path] = [root / "assets" / "music" / "background.mp3"]
    filters: list[str] = ["[0:a]volume=0.18[a0]"]
    labels = ["[a0]"]
    index = 1

    for shot, speaker, _text, filename in audio_lines(shots):
        path = root / "assets" / "audio" / filename
        if not path.exists():
            continue
        delay = int((shot.start + _line_offset(shot, speaker, filename.name)) * 1000)
        inputs.append(path)
        volume = 1.0 if speaker in {"elena", "priest"} else 0.92
        filters.append(f"[{index}:a]adelay={delay}|{delay},volume={volume}[a{index}]")
        labels.append(f"[a{index}]")
        index += 1

    for name, starts, volume in [
        ("rain.wav", [0], 0.55),
        ("thunder.wav", [1.1, 5.4], 0.85),
        ("heartbeat.wav", [15.0, 16.2, 34.1], 0.95),
        ("crash.wav", [14.15], 0.95),
        ("impact.wav", [49.7], 0.95),
    ]:
        path = root / "assets" / "sfx" / name
        if not path.exists():
            continue
        for start in starts:
            delay = int(start * 1000)
            inputs.append(path)
            filters.append(f"[{index}:a]adelay={delay}|{delay},volume={volume}[a{index}]")
            labels.append(f"[a{index}]")
            index += 1

    cmd = ["ffmpeg", "-y"]
    for path in inputs:
        cmd.extend(["-i", str(path)])
    filter_complex = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0,atrim=0:57.04[aout]"
    cmd.extend(["-filter_complex", filter_complex, "-map", "[aout]", "-c:a", "pcm_s16le", str(out)])
    run(cmd, root)
    return out


def _line_offset(shot: Shot, speaker: str, filename: str) -> float:
    if shot.voice_over and filename.endswith("_elena.wav"):
        return 0.15
    if shot.dialogue and shot.voice_over:
        return min(shot.duration * 0.56, shot.duration - 1.0)
    if len(shot.dialogue) > 1 and speaker == "elena":
        return min(shot.duration * 0.72, shot.duration - 0.8)
    return 0.35


def _filter_for(shot: Shot) -> str:
    frames = max(int(shot.duration * 30), 1)
    if shot.motion_prompt == "black":
        return "scale=1080:1920,format=yuv420p"
    if shot.motion_prompt in {"slow_zoom_in", "rapid_zoom_out", "flash"}:
        zoom = "zoom='min(zoom+0.0018,1.12)'" if shot.motion_prompt != "rapid_zoom_out" else "zoom='max(1.12-on/900,1.0)'"
        return f"scale=1200:2134,zoompan={zoom}:d={frames}:s=1080x1920:fps=30,format=yuv420p"
    if shot.motion_prompt == "slow_zoom_out":
        return f"scale=1200:2134,zoompan=zoom='max(1.10-on/1500,1.0)':d={frames}:s=1080x1920:fps=30,format=yuv420p"
    if shot.motion_prompt == "pan_right":
        return f"scale=1200:1920,zoompan=z=1:x='min(on*2,120)':y=0:d={frames}:s=1080x1920:fps=30,format=yuv420p"
    return "scale=1080:1920,format=yuv420p"


def _escape_filter_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "\\\\").replace(":", "\\:")


def build_report(root: Path, shots: list[Shot], final: Path) -> dict:
    manifest_path = root / "data" / "production_manifest.json"
    manifest = read_json(manifest_path) if manifest_path.exists() else {}
    manifest.setdefault("status", {})["render"] = True
    manifest["files"] = {
        "video": str(final),
        "subtitles": str(root / "output" / "episode_001.srt"),
        "storyboard": str(root / "data" / "storyboard.json"),
    }
    write_json(manifest_path, manifest)
    return {
        "project": "SECOND CHANCE",
        "episode": 1,
        "video": str(final),
        "shots": [shot.model_dump() for shot in shots],
        "manifest": manifest,
    }


def probe(root: Path, video: Path) -> dict:
    ensure_bin_wrappers(root)
    result = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)], root)
    return json.loads(result.stdout)
