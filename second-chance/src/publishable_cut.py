from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .models import ROOT
from .utils import ensure_bin_wrappers, run, srt_time
from .video_renderer import ensure_fallback_audio_assets


TIMELINE = [
    ("key_death.png", 0.0, 4.0, "我死的那一晚，\n我的丈夫，就站在那里看着。", "rain"),
    ("key_betrayal.png", 4.0, 8.0, "而他身边的人，\n是我最信任的闺蜜。", "rain"),
    ("key_headlights.png", 8.0, 11.0, "我以为一切都结束了。", "crash"),
    ("key_rebirth.png", 11.0, 16.0, "可当我再次睁开眼，\n我竟然站在自己的婚礼上。", "heartbeat"),
    ("key_wedding.png", 16.0, 23.0, "回到了他们杀死我的三年前。", "tension"),
    ("key_wedding.png", 23.0, 28.0, "神父问我：\n你愿意嫁给他吗？", "silence"),
    ("key_revenge.png", 28.0, 35.0, "我看着他的笑脸，\n然后说：不愿意。\n这一世，我要先毁掉他们。", "impact"),
]


def render_publishable(root: Path = ROOT) -> Path:
    ensure_bin_wrappers(root)
    ensure_fallback_audio_assets(root)
    create_rain_overlay(root)
    create_title_card(root)
    create_publish_srt(root)
    shot_dir = root / "output" / "publish_shots"
    shot_dir.mkdir(parents=True, exist_ok=True)
    clips: list[Path] = []
    for idx, (image, start, end, _subtitle, _mood) in enumerate(TIMELINE, start=1):
        src = root / "assets" / "images" / image
        out = shot_dir / f"P{idx:02d}.mp4"
        duration = end - start
        _render_motion_shot(root, src, out, duration, idx, _mood)
        clips.append(out)
    title = shot_dir / "P08.mp4"
    run([
        "ffmpeg", "-y", "-loop", "1", "-t", "2.2", "-i", str(root / "assets" / "images" / "publish_title.png"),
        "-f", "lavfi", "-t", "2.2", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-vf", "scale=1080:1920,format=yuv420p", "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(title),
    ], root)
    clips.append(title)
    concat = shot_dir / "concat.txt"
    concat.write_text("".join(f"file '{clip.resolve()}'\n" for clip in clips), encoding="utf-8")
    no_subs = root / "output" / "episode_001_publish_no_subs.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(no_subs)], root)
    audio = create_publish_audio(root)
    final = root / "output" / "episode_001.mp4"
    srt = root / "output" / "episode_001.srt"
    escaped_srt = str(srt.resolve()).replace(":", "\\:")
    subtitle_filter = (
        f"subtitles={escaped_srt}:"
        "force_style='FontName=Noto Sans CJK SC,FontSize=17,PrimaryColour=&HFFFFFF&,"
        "OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=250'"
    )
    run([
        "ffmpeg", "-y", "-i", str(no_subs), "-i", str(audio),
        "-vf", subtitle_filter, "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(final),
    ], root)
    report = {
        "type": "publishable_cut",
        "duration_target": 37.2,
        "visual_assets": [item[0] for item in TIMELINE],
        "audio": {
            "bgm": "assets/music/background.mp3",
            "sfx": ["rain.wav", "thunder.wav", "heartbeat.wav", "crash.wav", "impact.wav"],
            "voice": "not included: external TTS requires explicit approval",
        },
        "video": str(final),
    }
    (root / "output" / "production_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return final


def create_publish_srt(root: Path) -> Path:
    blocks = []
    for idx, (_image, start, end, subtitle, _mood) in enumerate(TIMELINE, start=1):
        blocks.append(f"{idx}\n{srt_time(start)} --> {srt_time(end)}\n{subtitle}\n")
    blocks.append(f"{len(TIMELINE)+1}\n{srt_time(35.0)} --> {srt_time(37.2)}\nSECOND CHANCE\nEPISODE 1\n")
    out = root / "output" / "episode_001.srt"
    out.write_text("\n".join(blocks), encoding="utf-8")
    return out


def create_publish_audio(root: Path) -> Path:
    out = root / "output" / "episode_001_mix.wav"
    inputs = [
        root / "assets" / "music" / "background.mp3",
        root / "assets" / "audio" / "publish_voice.wav",
        root / "assets" / "sfx" / "rain.wav",
        root / "assets" / "sfx" / "thunder.wav",
        root / "assets" / "sfx" / "heartbeat.wav",
        root / "assets" / "sfx" / "crash.wav",
        root / "assets" / "sfx" / "impact.wav",
    ]
    cmd = ["ffmpeg", "-y"]
    for item in inputs:
        cmd.extend(["-i", str(item)])
    filt = (
        "[0:a]volume=0.07[a0];"
        "[1:a]adelay=250|250,volume=2.8,acompressor=threshold=-16dB:ratio=3:attack=8:release=180,loudnorm=I=-15:TP=-1.5:LRA=8[a1];"
        "[2:a]atrim=0:11,volume=0.18[a2];"
        "[3:a]adelay=1200|1200,volume=0.34[a3];"
        "[3:a]adelay=6200|6200,volume=0.25[a4];"
        "[4:a]adelay=11000|11000,volume=0.35[a5];"
        "[4:a]adelay=12400|12400,volume=0.26[a6];"
        "[5:a]adelay=10200|10200,volume=0.55[a7];"
        "[6:a]adelay=29200|29200,volume=0.60[a8];"
        "[a0][a1][a2][a3][a4][a5][a6][a7][a8]amix=inputs=9:duration=longest:normalize=0,alimiter=limit=0.92,atrim=0:37.2[aout]"
    )
    cmd.extend(["-filter_complex", filt, "-map", "[aout]", "-c:a", "pcm_s16le", str(out)])
    run(cmd, root)
    return out


def _render_motion_shot(root: Path, src: Path, out: Path, duration: float, idx: int, mood: str) -> None:
    frames = int(duration * 30)
    if mood in {"rain", "crash"}:
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-t", f"{duration:.3f}", "-i", str(src),
            "-stream_loop", "-1", "-t", f"{duration:.3f}", "-i", str(root / "assets" / "overlays" / "rain_overlay.mp4"),
            "-f", "lavfi", "-t", f"{duration:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-filter_complex", _motion_filter(frames, idx, mood, rain=True),
            "-map", "[v]", "-map", "2:a:0",
            "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out),
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-t", f"{duration:.3f}", "-i", str(src),
            "-f", "lavfi", "-t", f"{duration:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-filter_complex", _motion_filter(frames, idx, mood, rain=False),
            "-map", "[v]", "-map", "1:a:0",
            "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out),
        ]
    run(cmd, root)


def _motion_filter(frames: int, idx: int, mood: str, rain: bool) -> str:
    zoom = "1.0+0.10*on/{frames}" if idx not in {3, 7} else "1.11-0.08*on/{frames}"
    x_expr = "iw/2-(iw/zoom/2)"
    y_expr = "ih/2-(ih/zoom/2)"
    if idx in {2, 5}:
        x_expr = "iw/2-(iw/zoom/2)+sin(on/9)*24"
    if idx == 3:
        x_expr = "iw/2-(iw/zoom/2)+sin(on/2)*18"
        y_expr = "ih/2-(ih/zoom/2)+cos(on/3)*18"
    base = (
        f"[0:v]scale=1320:2347,zoompan=z='{zoom.format(frames=frames)}':"
        f"x='{x_expr}':y='{y_expr}':d={frames}:s=1080x1920:fps=30,"
        "eq=contrast=1.08:saturation=1.07"
    )
    if idx == 3:
        base += ",fade=t=in:st=0:d=0.18:color=white,fade=t=out:st=2.55:d=0.35:color=white"
    if idx == 7:
        base += ",fade=t=out:st=6.35:d=0.65:color=black"
    if rain:
        return base + "[base];[1:v]format=rgba,colorchannelmixer=aa=0.55[r];[base][r]overlay=0:0[v]"
    return base + "[v]"


def create_rain_overlay(root: Path) -> None:
    overlay = root / "assets" / "overlays" / "rain_overlay.mp4"
    if overlay.exists():
        return
    frame_dir = root / "assets" / "overlays" / "rain_frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    for frame in range(60):
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        shift = frame * 26
        for x in range(-200, 1280, 52):
            for y in range(-260, 2180, 230):
                y0 = (y + shift + (x % 170)) % 2180 - 260
                draw.line((x, y0, x + 34, y0 + 116), fill=(205, 228, 255, 115), width=3)
        img.save(frame_dir / f"rain_{frame:03d}.png")
    run([
        "ffmpeg", "-y", "-framerate", "30", "-i", str(frame_dir / "rain_%03d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuva420p", "-t", "2", str(overlay),
    ], root)


def create_title_card(root: Path) -> None:
    path = root / "assets" / "images" / "publish_title.png"
    img = Image.new("RGB", (1080, 1920), (4, 4, 7))
    draw = ImageDraw.Draw(img)
    title = _font(92, True)
    sub = _font(42)
    draw.text((138, 780), "SECOND CHANCE", fill=(238, 230, 211), font=title)
    draw.text((386, 910), "EPISODE 1", fill=(185, 36, 56), font=sub)
    draw.text((250, 1010), "I WOKE UP AT MY OWN WEDDING", fill=(220, 220, 220), font=_font(30))
    img.save(path)


def _font(size: int, bold: bool = False):
    for path in [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()
