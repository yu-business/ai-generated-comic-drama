from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .models import Shot
from .utils import make_silent_wav


class VoiceProvider:
    def synthesize(self, text: str, character: str, output_path: Path, duration: float) -> str:
        raise NotImplementedError


class FallbackVoiceProvider(VoiceProvider):
    """Uses available local TTS, otherwise deterministic silent WAV."""

    def synthesize(self, text: str, character: str, output_path: Path, duration: float) -> str:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if shutil.which("espeak"):
            raw = output_path.with_suffix(".raw.wav")
            result = subprocess.run(["espeak", "-w", str(raw), text], text=True, capture_output=True)
            if result.returncode == 0 and raw.exists():
                raw.replace(output_path)
                return str(output_path)
        make_silent_wav(output_path, duration)
        return str(output_path)


def audio_lines(shots: list[Shot]) -> list[tuple[Shot, str, str, Path]]:
    lines: list[tuple[Shot, str, str, Path]] = []
    for shot in shots:
        speaker = "elena"
        if shot.voice_over:
            lines.append((shot, "elena", shot.voice_over, Path(f"{shot.shot_id.lower()}_elena.wav")))
        for item in shot.dialogue:
            if ":" in item:
                name, text = item.split(":", 1)
                speaker = name.strip().lower()
                spoken = text.strip()
            else:
                spoken = item
            lines.append((shot, speaker, spoken, Path(f"{shot.shot_id.lower()}_{speaker}.wav")))
    return lines


def generate_audio(root: Path, shots: list[Shot], force: bool = False) -> list[Path]:
    provider = FallbackVoiceProvider()
    paths = []
    for shot, speaker, text, filename in audio_lines(shots):
        path = root / "assets" / "audio" / filename
        if path.exists() and not force:
            paths.append(path)
            continue
        provider.synthesize(text, speaker, path, min(max(shot.duration - 0.2, 0.8), 4.5))
        paths.append(path)
        print(f"  ✓ {path.name}")
    return paths
