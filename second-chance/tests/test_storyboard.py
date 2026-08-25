import shutil
from pathlib import Path

from src.storyboard import build_storyboard


ROOT = Path(__file__).resolve().parents[1]


def _isolated_root(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    shutil.copytree(ROOT / "config", root / "config")
    (root / "data").mkdir(parents=True)
    (root / "assets" / "characters").mkdir(parents=True)
    return root


def test_storyboard_has_14_ordered_shots(tmp_path):
    shots = build_storyboard(_isolated_root(tmp_path))
    assert len(shots) == 14
    assert [shot.shot_id for shot in shots] == [f"S{i:02d}" for i in range(1, 15)]
    assert all(a.end <= b.start for a, b in zip(shots, shots[1:]))


def test_duration_and_characters_are_valid(tmp_path):
    shots = build_storyboard(_isolated_root(tmp_path))
    valid = {"Elena", "Adrian", "Claire"}
    assert all(shot.duration > 0 for shot in shots)
    assert 50 <= sum(shot.duration for shot in shots) <= 65
    assert all(set(shot.characters).issubset(valid) for shot in shots)


def test_image_prompts_exist_except_black_screen(tmp_path):
    shots = build_storyboard(_isolated_root(tmp_path))
    assert all(shot.image_prompt for shot in shots if shot.needs_image)
    assert all(not shot.image_prompt for shot in shots if not shot.needs_image)
