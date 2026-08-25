from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv

from src.asset_manager import update_manifest
from src.image_generator import generate_images
from src.models import ROOT, Shot
from src.storyboard import build_storyboard
from src.subtitle_generator import generate_subtitles
from src.utils import ensure_bin_wrappers, read_json
from src.video_renderer import render
from src.voice_generator import generate_audio


def load_storyboard(root: Path) -> list[Shot]:
    path = root / "data" / "storyboard.json"
    if not path.exists():
        return build_storyboard(root)
    return [Shot(**item) for item in read_json(path)]


def run_pipeline(mode: str, force: bool = False, episode: int = 1, provider: str = "placeholder") -> None:
    load_dotenv(ROOT / ".env")
    print("[SECOND CHANCE]\n")
    if episode != 1:
        raise ValueError("Only episode 1 is implemented in this demo pipeline.")
    if provider != "placeholder":
        print(f"Provider '{provider}' requested, but no credentials are configured; using placeholder.")
    ensure_bin_wrappers(ROOT)
    shots: list[Shot] = []
    if mode in {"storyboard", "all"}:
        print("[1/5] Building storyboard")
        shots = build_storyboard(ROOT)
        update_manifest(ROOT, storyboard=True)
        print("  ✓ storyboard.json")
    if mode in {"assets", "audio", "render"}:
        shots = load_storyboard(ROOT)
    if mode in {"assets", "all"}:
        print("[2/5] Generating image assets")
        if not shots:
            shots = load_storyboard(ROOT)
        generate_images(ROOT, shots, force=force)
        update_manifest(ROOT, images=True)
    if mode in {"audio", "all"}:
        print("[3/5] Generating audio")
        if not shots:
            shots = load_storyboard(ROOT)
        generate_audio(ROOT, shots, force=force)
        generate_subtitles(ROOT, shots)
        update_manifest(ROOT, voices=True)
    if mode in {"render", "all"}:
        print("[4/5] Rendering video")
        if not shots:
            shots = load_storyboard(ROOT)
        final = render(ROOT, shots)
        update_manifest(ROOT, render=True)
        print("\nDONE\n")
        print(f"Video:\n{final}")
        print(f"\nSubtitles:\n{ROOT / 'output' / 'episode_001.srt'}")
        print(f"\nProduction report:\n{ROOT / 'output' / 'production_report.json'}")
    elif mode == "storyboard":
        print("\nDONE\nStoryboard:\ndata/storyboard.json")


def main() -> None:
    parser = argparse.ArgumentParser(description="SECOND CHANCE local motion-comic pipeline")
    parser.add_argument("--mode", choices=["all", "storyboard", "assets", "audio", "render"], default="all")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated assets")
    parser.add_argument("--episode", type=int, default=1)
    parser.add_argument("--provider", default="placeholder")
    args = parser.parse_args()
    run_pipeline(args.mode, args.force, args.episode, args.provider)


if __name__ == "__main__":
    main()
