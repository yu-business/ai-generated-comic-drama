from __future__ import annotations

from pathlib import Path

from .models import Shot
from .utils import srt_time


def generate_subtitles(root: Path, shots: list[Shot]) -> Path:
    blocks = []
    index = 1
    for shot in shots:
        text = shot.subtitle_text
        if not text:
            continue
        blocks.append(f"{index}\n{srt_time(shot.start)} --> {srt_time(shot.end)}\n{text}\n")
        index += 1
    out = root / "output" / "episode_001.srt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(blocks), encoding="utf-8")
    (root / "assets" / "subtitles" / "episode_001.srt").write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    return out
