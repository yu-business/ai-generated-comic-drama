from __future__ import annotations

import json
import os
import shutil
import subprocess
import wave
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = f"{cwd / 'bin'}:{env.get('PATH', '')}"
    result = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            + " ".join(cmd)
            + "\nSTDOUT:\n"
            + result.stdout
            + "\nSTDERR:\n"
            + result.stderr
        )
    return result


def resolve_ffmpeg(root: Path) -> Path:
    system = shutil.which("ffmpeg")
    if system:
        return Path(system)
    try:
        import imageio_ffmpeg

        return Path(imageio_ffmpeg.get_ffmpeg_exe())
    except Exception as exc:
        raise RuntimeError("ffmpeg is not available; install imageio-ffmpeg or system ffmpeg") from exc


def ensure_bin_wrappers(root: Path) -> None:
    bin_dir = root / "bin"
    bin_dir.mkdir(exist_ok=True)
    ffmpeg_path = resolve_ffmpeg(root)
    ffmpeg_wrapper = bin_dir / "ffmpeg"
    ffmpeg_wrapper.write_text(f"#!/usr/bin/env sh\nexec {ffmpeg_path} \"$@\"\n", encoding="utf-8")
    ffmpeg_wrapper.chmod(0o755)
    ffprobe_wrapper = bin_dir / "ffprobe"
    ffprobe_wrapper.write_text(
        "#!/usr/bin/env python3\n"
        "import json, subprocess, sys\n"
        "args=sys.argv[1:]\n"
        "if '-version' in args or '--version' in args:\n"
        "    print('ffprobe wrapper 1.0 using bundled ffmpeg backend')\n"
        "    sys.exit(0)\n"
        "path=args[-1]\n"
        "ffmpeg='" + str(ffmpeg_path) + "'\n"
        "p=subprocess.run([ffmpeg,'-hide_banner','-i',path],text=True,capture_output=True)\n"
        "text=p.stderr\n"
        "info={'streams':[],'format':{'duration':'0'}}\n"
        "import re\n"
        "m=re.search(r'Duration: (\\d+):(\\d+):(\\d+\\.\\d+)', text)\n"
        "if m:\n"
        "    h,mi,s=m.groups(); info['format']['duration']=str(int(h)*3600+int(mi)*60+float(s))\n"
        "vm=re.search(r'Video: ([^,]+).*?, (\\d+)x(\\d+).*?(\\d+(?:\\.\\d+)?) fps', text)\n"
        "if vm:\n"
        "    codec,w,h,fps=vm.groups(); info['streams'].append({'codec_type':'video','codec_name':codec.strip().split()[0],'width':int(w),'height':int(h),'r_frame_rate':fps+'/1','avg_frame_rate':fps+'/1'})\n"
        "am=re.search(r'Audio: ([^,]+)', text)\n"
        "if am: info['streams'].append({'codec_type':'audio','codec_name':am.group(1).strip().split()[0]})\n"
        "if '-of' in args and 'json' in args: print(json.dumps(info))\n"
        "else: print(json.dumps(info, indent=2))\n",
        encoding="utf-8",
    )
    ffprobe_wrapper.chmod(0o755)


def make_silent_wav(path: Path, duration: float, sample_rate: int = 44100) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = int(duration * sample_rate)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(b"\x00\x00" * frames)


def srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, milli = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{milli:03d}"
