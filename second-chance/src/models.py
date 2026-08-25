from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Shot:
    shot_id: str
    start: float
    end: float
    duration: float
    scene: str
    characters: list[str]
    description: str
    motion_prompt: str
    camera: str
    dialogue: list[str] = field(default_factory=list)
    voice_over: str = ""
    image_prompt: str = ""
    transition: str = ""
    sfx: list[str] = field(default_factory=list)
    music_mood: str = ""
    asset_type: str = "image"

    @property
    def needs_image(self) -> bool:
        return self.asset_type != "black"

    @property
    def subtitle_text(self) -> str:
        lines = []
        if self.voice_over:
            lines.append(self.voice_over)
        lines.extend(self.dialogue)
        return "\n".join(lines).strip()

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Manifest:
    project: str = "SECOND CHANCE"
    episode: int = 1
    resolution: str = "1080x1920"
    fps: int = 30
    shots: int = 14
    characters: list[str] = field(default_factory=lambda: ["Elena", "Adrian", "Claire"])
    status: dict[str, bool] = field(default_factory=lambda: {
        "storyboard": False,
        "images": False,
        "voices": False,
        "render": False,
    })
    files: dict[str, Any] = field(default_factory=dict)

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


ROOT = Path(__file__).resolve().parents[1]
