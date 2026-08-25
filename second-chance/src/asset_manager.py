from __future__ import annotations

from pathlib import Path

from .models import Shot
from .utils import read_json, write_json


def update_manifest(root: Path, **status: bool) -> None:
    path = root / "data" / "production_manifest.json"
    data = read_json(path) if path.exists() else {}
    data.setdefault("status", {})
    data["status"].update(status)
    write_json(path, data)


def validate_assets(root: Path, shots: list[Shot]) -> dict[str, bool]:
    return {shot.shot_id: (root / "assets" / "images" / f"{shot.shot_id}.png").exists() for shot in shots}
