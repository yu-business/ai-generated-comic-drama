from __future__ import annotations

from pathlib import Path

from .models import Manifest, Shot
from .prompt_builder import PromptBuilder
from .utils import write_json


def base_shots() -> list[Shot]:
    rows = [
        ("S01", 0, 3, "Deserted road at night", ["Elena", "Adrian"], "Elena lying injured on wet asphalt at night, black evening dress, wet black hair stuck to her face, terrified and betrayed expression, heavy rain, streetlights reflecting on the road; Adrian is a blurred silhouette in the distance.", [], "The night I died...", "slow_zoom_in", "slow push-in toward Elena", "fade", ["rain", "distant thunder"], "dark suspense", "image"),
        ("S02", 3, 6, "Deserted road at night", ["Adrian"], "Adrian stands under a black umbrella, looking down at Elena outside the frame, emotionally unreadable.", [], "my husband was watching.", "slow_zoom_in", "slow cinematic zoom toward Adrian's face", "cut", ["rain"], "dark suspense", "image"),
        ("S03", 6, 9, "Deserted road at night", ["Adrian", "Claire"], "Claire steps out from behind Adrian and gently links her arm with his under the rain.", ["CLAIRE: I'm sorry, Elena."], "", "pan_right", "slow side reveal", "cut", ["rain"], "dark suspense", "image"),
        ("S04", 9, 12, "Deserted road at night", ["Elena"], "Extreme close-up of Elena as her eyes widen with the full understanding of betrayal.", [], "", "slow_zoom_in", "extreme close-up", "cut", ["rain", "breathing"], "dark suspense", "image"),
        ("S05", 12, 15, "Deserted road at night", ["Elena"], "Elena POV: two bright car headlights rapidly approach, then a white flash. Do not show impact.", ["ELENA: Wait—"], "", "flash", "rapid zoom into headlights", "white flash", ["crash"], "dark suspense", "image"),
        ("S06", 15, 18, "Black void", [], "Pure black screen between death and rebirth.", ["PRIEST: Elena?"], "", "black", "static black frame", "fade", ["heartbeat", "heartbeat"], "silence", "black"),
        ("S07", 18, 22, "Elegant wedding church", ["Elena"], "Elena suddenly opens her eyes in warm bright light, now wearing her wedding dress.", [], "", "rapid_zoom_out", "extreme close-up on eyes, quick pull-back", "flash", [], "mysterious emotional tension", "image"),
        ("S08", 22, 26, "Elegant wedding church", ["Elena", "Adrian"], "Wide shot inside an elegant European wedding church with white flowers and guests. Adrian stands opposite Elena.", ["PRIEST: Do you take Adrian to be your husband?"], "", "slow_zoom_out", "wide establishing shot", "cut", [], "mysterious emotional tension", "image"),
        ("S09", 26, 30, "Elegant wedding church", ["Elena"], "Close-up of Elena looking down at her unwounded hands in disbelief.", [], "This can't be real...", "slow_zoom_in", "close-up on hands and face", "cut", [], "mysterious emotional tension", "image"),
        ("S10", 30, 34, "Elegant wedding church", ["Claire"], "Claire sits in the front row smiling innocently in a champagne bridesmaid dress.", [], "", "slow_zoom_in", "slow zoom toward Claire", "cut", [], "mysterious emotional tension", "image"),
        ("S11", 34, 39, "Memory montage", ["Elena", "Adrian", "Claire"], "Rapid memory montage reusing betrayal, Elena's terrified eyes, and approaching headlights as short flashes.", [], "I came back...", "flash", "rapid flash montage", "flash", ["heartbeat"], "mysterious emotional tension", "image"),
        ("S12", 39, 44, "Elegant wedding church", ["Elena", "Adrian"], "Back at the wedding, Adrian smiles and extends his hand toward Elena.", ["ADRIAN: Elena?"], "Three years before they killed me.", "slow_zoom_in", "slow push toward Adrian's hand and Elena's face", "cut", [], "mysterious emotional tension", "image"),
        ("S13", 44, 50, "Elegant wedding church", ["Elena", "Adrian"], "The priest repeats the question. Adrian smiles. Elena looks at him calmly as the music fades out, then says No.", ["PRIEST: Elena, do you take this man to be your husband?", "ELENA: No."], "", "slow_zoom_in", "tight dramatic close-up", "impact cut", ["impact"], "music fades to silence", "image"),
        ("S14", 50, 57, "Elegant wedding church", ["Elena", "Claire"], "Wedding guests react. Elena turns away from Adrian and looks directly toward Claire. Claire's smile disappears. Elena gives a subtle cold smile. Cut to black title SECOND CHANCE, then EPISODE 2.", [], "This time...\nI'll destroy them first.", "slow_zoom_in", "reaction montage to cold close-up", "cut to black", [], "revenge dark determination", "image"),
    ]
    return [
        Shot(
            shot_id=sid,
            start=float(start),
            end=float(end),
            duration=float(end - start),
            scene=scene,
            characters=chars,
            description=desc,
            dialogue=dialogue,
            voice_over=vo,
            image_prompt="",
            motion_prompt=motion,
            camera=camera,
            transition=transition,
            sfx=sfx,
            music_mood=music,
            asset_type=asset_type,
        )
        for sid, start, end, scene, chars, desc, dialogue, vo, motion, camera, transition, sfx, music, asset_type in rows
    ]


def build_storyboard(root: Path) -> list[Shot]:
    builder = PromptBuilder(root)
    shots = []
    for shot in base_shots():
        if shot.needs_image:
            shot.image_prompt = builder.shot_prompt(shot)
        shots.append(shot)
    write_json(root / "data" / "storyboard.json", [shot.model_dump() for shot in shots])
    manifest = Manifest(status={"storyboard": True, "images": False, "voices": False, "render": False})
    write_json(root / "data" / "production_manifest.json", manifest.model_dump())
    builder.write_character_prompts()
    return shots
