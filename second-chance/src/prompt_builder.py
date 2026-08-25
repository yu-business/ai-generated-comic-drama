from __future__ import annotations

from pathlib import Path

from .models import Shot
from .utils import load_yaml


class PromptBuilder:
    """Builds consistent image and character reference prompts."""

    def __init__(self, root: Path):
        self.root = root
        self.characters = load_yaml(root / "config" / "characters.yaml")["characters"]
        self.style = load_yaml(root / "config" / "style.yaml")

    def shot_prompt(self, shot: Shot) -> str:
        identities = [self.characters[name]["identity_prompt"] for name in shot.characters if name in self.characters]
        lighting = self.style["death_lighting"] if "road" in shot.scene.lower() or shot.shot_id in {"S01", "S02", "S03", "S04", "S05"} else self.style["wedding_lighting"]
        clothing = self._clothing(shot)
        parts = identities + [
            shot.description,
            clothing,
            shot.scene,
            lighting,
            self.style["base_style_prompt"],
            shot.camera,
            "vertical 9:16",
        ]
        return ",\n".join([p for p in parts if p])

    def _clothing(self, shot: Shot) -> str:
        chunks: list[str] = []
        for name in shot.characters:
            data = self.characters.get(name, {})
            if shot.shot_id in {"S01", "S02", "S03", "S04", "S05", "S11"} and name == "Elena":
                chunks.extend(data.get("death_outfit", []))
            else:
                chunks.extend(data.get("wedding_outfit", []))
        return ", ".join(chunks)

    def write_character_prompts(self) -> list[Path]:
        paths: list[Path] = []
        for name, data in self.characters.items():
            slug = name.lower()
            folder = self.root / "assets" / "characters" / slug
            folder.mkdir(parents=True, exist_ok=True)
            ref = folder / "reference_prompt.txt"
            ref.write_text(data["identity_prompt"] + "\n", encoding="utf-8")
            sheet = folder / "character_sheet_prompt.txt"
            outfits = data.get("wedding_outfit", [])
            outfit_text = ", ".join(outfits)
            sheet.write_text(
                f"Character reference sheet of {data['identity_prompt']}.\n\n"
                "Front portrait, three-quarter portrait, side profile, full body.\n\n"
                f"She/he wears {outfit_text}.\n\n"
                "Cinematic modern webtoon illustration, semi-realistic graphic novel style, "
                "dark romance aesthetic, detailed expressive eyes, soft cinematic lighting, "
                "consistent facial identity, clean neutral background, professional character design sheet.\n",
                encoding="utf-8",
            )
            paths.extend([ref, sheet])
        return paths
