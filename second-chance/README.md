# SECOND CHANCE

Local CLI production pipeline for **SECOND CHANCE - Episode 1: I Woke Up at My Own Wedding**, a 50-60 second vertical dark-romance motion-comic demo.

The project works without paid AI keys. By default it uses placeholder storyboard frames, local/fallback voice assets, generated subtitles, and FFmpeg rendering.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Check FFmpeg:

```bash
ffmpeg -version
ffprobe -version
```

If system FFmpeg is not installed, the pipeline can use `imageio-ffmpeg` and creates local wrappers in `bin/`.

## Run

```bash
python main.py
python main.py --mode storyboard
python main.py --mode assets
python main.py --mode audio
python main.py --mode render
python main.py --mode all
```

`python main.py` defaults to `--mode all`.

## Placeholder Mode

`IMAGE_PROVIDER=placeholder` generates clean 1080x1920 storyboard cards with shot ID, description, characters, dialogue, voice-over, and duration. This keeps the full pipeline testable without OpenAI, Replicate, Fal, Kling, or other image services.

## AI Image Mode

The code uses provider abstractions so adapters can be added later. Missing API keys never stop the pipeline. Configure credentials in `.env` if you extend providers:

```text
OPENAI_API_KEY=
ELEVENLABS_API_KEY=
REPLICATE_API_TOKEN=
FAL_KEY=
```

## Voice Mode

The fallback voice provider tries local `espeak`. If no local TTS is available, it creates silent WAV files with expected timing so rendering still succeeds.

## Rendering

Each shot renders first to:

```text
output/shots/S01.mp4
...
output/shots/S14.mp4
```

The shots are concatenated, subtitles are burned in, and the final video is written to:

```text
output/episode_001.mp4
```

Target format: 1080x1920, 9:16, 30 FPS, H.264 video, AAC audio.

## Manual Image Replacement

You can externally generate better images and replace:

```text
assets/images/S01.png
assets/images/S02.png
...
assets/images/S14.png
```

Then run:

```bash
python main.py --mode render
```

Existing images are not overwritten unless you explicitly run:

```bash
python main.py --mode assets --force
```

## Folder Structure

```text
config/      project, character, and style definitions
data/        episode data, storyboard, production manifest
src/         reusable production pipeline modules
assets/      character prompts, images, audio, music, sfx, subtitles
output/      rendered shots, final MP4, SRT, production report
tests/       storyboard validation tests
```

## Tests

```bash
pytest
```
