# Project Goal

Build a complete, runnable local project that produces a 50–60 second vertical AI motion-comic demo titled:

**SECOND CHANCE — Episode 1: I Woke Up at My Own Wedding**

Genre:

* Rebirth
* Revenge
* Romance
* Mystery
* Dark romance

The project must be designed as a reusable AI comic production pipeline, not as a one-off script.

The final result should be able to generate or assemble:

1. Character definitions
2. Storyboard data
3. Image-generation prompts
4. Voice-over text
5. Subtitles
6. Shot timing
7. Placeholder or generated visual assets
8. Final 9:16 MP4 video
9. Production metadata for every shot

The application must work locally.

If external AI API keys are unavailable, the project must still run end-to-end using placeholder images and locally generated title cards, so that a final demo MP4 can always be rendered.

---

# 1. Technical Stack

Use:

* Python 3.11+
* FFmpeg
* Pillow
* pydantic
* python-dotenv
* requests or httpx
* optionally MoviePy only if useful

Do not build a frontend.

This is a CLI-based production pipeline.

Main command:

```bash
python main.py
```

Also support:

```bash
python main.py --mode storyboard
python main.py --mode assets
python main.py --mode audio
python main.py --mode render
python main.py --mode all
```

Default:

```bash
python main.py --mode all
```

---

# 2. Expected Folder Structure

Create this structure:

```text
second-chance/
│
├── README.md
├── requirements.txt
├── .env.example
├── main.py
│
├── config/
│   ├── project.yaml
│   ├── characters.yaml
│   └── style.yaml
│
├── data/
│   ├── episode_001.json
│   ├── storyboard.json
│   └── production_manifest.json
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── storyboard.py
│   ├── prompt_builder.py
│   ├── image_generator.py
│   ├── voice_generator.py
│   ├── subtitle_generator.py
│   ├── asset_manager.py
│   ├── video_renderer.py
│   └── utils.py
│
├── assets/
│   ├── characters/
│   │   ├── elena/
│   │   ├── adrian/
│   │   └── claire/
│   │
│   ├── images/
│   ├── audio/
│   ├── music/
│   ├── sfx/
│   └── subtitles/
│
├── output/
│   ├── episode_001.mp4
│   ├── episode_001.srt
│   └── production_report.json
│
└── tests/
    └── test_storyboard.py
```

Create all necessary files.

---

# 3. Video Format

Final video:

```text
Resolution: 1080x1920
Aspect Ratio: 9:16
FPS: 30
Duration target: 50–60 seconds
Format: MP4
Video codec: H.264
Audio codec: AAC
```

Output:

```text
output/episode_001.mp4
```

---

# 4. Visual Style

Use one global visual style.

Style name:

```text
Cinematic Dark Romance Webtoon
```

Base style prompt:

```text
cinematic modern webtoon illustration,
semi-realistic graphic novel style,
dark romance thriller aesthetic,
expressive detailed eyes,
professional composition,
dramatic cinematic lighting,
high visual consistency,
polished digital illustration,
vertical 9:16
```

Wedding scenes:

```text
warm golden-white cinematic lighting,
luxurious romantic wedding atmosphere,
soft sunlight,
white flowers,
elegant modern European church
```

Death scenes:

```text
cold blue-gray night lighting,
heavy rain,
wet asphalt reflections,
high contrast,
dark thriller atmosphere
```

Characters must remain visually consistent across shots.

---

# 5. Characters

Store all character definitions in:

```text
config/characters.yaml
```

## Elena

```yaml
name: Elena
age: 27
role: protagonist

appearance:
  gender: female
  hair: long straight black hair
  eyes: dark brown
  face: oval
  skin: fair
  identifying_feature: small beauty mark under left eye
  body: slim elegant figure

personality:
  before_rebirth:
    - gentle
    - trusting
    - emotional

  after_rebirth:
    - calm
    - intelligent
    - controlled
    - dangerous
    - determined

wedding_outfit:
  - minimalist white satin wedding dress
  - pearl earrings
  - delicate silver necklace

death_outfit:
  - elegant black evening dress

voice:
  style: young adult female
  tone: intimate cinematic narration
  transformation: warm at first, colder after rebirth
```

Character identity prompt:

```text
Elena, a beautiful 27-year-old woman,
long straight black hair,
dark brown eyes,
oval face,
fair skin,
small beauty mark under her left eye,
slim elegant figure,
refined facial features
```

---

## Adrian

```yaml
name: Adrian
age: 31
role: husband

appearance:
  gender: male
  hair: short dark brown hair
  eyes: gray-blue
  face: sharp jawline
  body: tall athletic build
  facial_hair: clean shaven

personality:
  public:
    - charming
    - trustworthy
    - sophisticated
    - gentle

  hidden:
    - manipulative
    - emotionally cold

wedding_outfit:
  - luxury black tuxedo
  - white shirt
  - black bow tie
```

Identity prompt:

```text
Adrian, a handsome 31-year-old man,
short dark brown hair,
sharp jawline,
gray-blue eyes,
tall athletic build,
clean shaven,
charming and sophisticated appearance
```

---

## Claire

```yaml
name: Claire
age: 27
role: best_friend

appearance:
  gender: female
  hair: long wavy blonde hair
  eyes: green
  face: delicate feminine features
  skin: fair
  body: slender elegant figure

personality:
  public:
    - sweet
    - innocent
    - supportive

  hidden:
    - deceptive
    - calculating

wedding_outfit:
  - elegant champagne-colored bridesmaid dress
```

Identity prompt:

```text
Claire, a beautiful 27-year-old woman,
long wavy blonde hair,
green eyes,
delicate feminine facial features,
fair skin,
slender elegant figure,
sweet innocent appearance
```

---

# 6. Episode Story

Create:

```text
data/episode_001.json
```

Story title:

```text
SECOND CHANCE
```

Episode:

```text
EP01 — I Woke Up at My Own Wedding
```

Premise:

Elena dies after discovering that her husband Adrian and her best friend Claire betrayed her.

Immediately after her death, Elena wakes up three years earlier, standing at the altar during her own wedding.

The priest asks whether she accepts Adrian as her husband.

Knowing what will happen in the future, Elena says:

```text
No.
```

She decides to destroy Adrian and Claire before they destroy her.

---

# 7. Storyboard

Create exactly 14 shots.

Each shot must contain:

```json
{
  "shot_id": "S01",
  "start": 0.0,
  "end": 3.0,
  "duration": 3.0,
  "scene": "",
  "characters": [],
  "description": "",
  "dialogue": [],
  "voice_over": "",
  "image_prompt": "",
  "motion_prompt": "",
  "camera": "",
  "transition": "",
  "sfx": [],
  "music_mood": "",
  "asset_type": "image"
}
```

Use the following storyboard.

---

## S01 — 00:00–00:03

Elena lies injured on a deserted road during heavy rain.

Visual:

```text
Elena lying injured on wet asphalt at night,
black evening dress,
wet black hair stuck to her face,
terrified and betrayed expression,
heavy rain,
streetlights reflecting on the road
```

Adrian is visible only as a blurred silhouette in the distance.

Voice-over:

```text
The night I died...
```

Camera:

```text
slow push-in toward Elena
```

SFX:

```text
rain
distant thunder
```

---

## S02 — 00:03–00:06

Adrian stands under a black umbrella.

He looks down at Elena outside the frame.

Voice-over:

```text
my husband was watching.
```

Camera:

```text
slow cinematic zoom toward Adrian's face
```

---

## S03 — 00:06–00:09

Claire steps out from behind Adrian.

She gently links her arm with his.

Dialogue:

```text
CLAIRE:
I'm sorry, Elena.
```

Camera:

```text
slow side reveal
```

---

## S04 — 00:09–00:12

Extreme close-up of Elena.

Her eyes widen when she understands the betrayal.

No dialogue.

Use rain and breathing SFX.

---

## S05 — 00:12–00:15

Elena POV.

Two bright car headlights rapidly approach.

Do not show a physical vehicle hitting Elena.

Use:

```text
headlights approaching
white flash
```

Dialogue:

```text
ELENA:
Wait—
```

Then:

```text
CRASH
```

---

## S06 — 00:15–00:18

Pure black screen.

SFX:

```text
heartbeat
heartbeat
```

Priest voice:

```text
Elena?
```

---

## S07 — 00:18–00:22

Elena suddenly opens her eyes.

Lighting is now warm and bright.

She is wearing her wedding dress.

Camera:

```text
extreme close-up on eyes
quick pull-back
```

---

## S08 — 00:22–00:26

Wide shot.

Elena stands inside an elegant wedding church.

Adrian stands opposite her.

White flowers and guests surround them.

Priest dialogue:

```text
Do you take Adrian to be your husband?
```

---

## S09 — 00:26–00:30

Close-up.

Elena looks down at her hands.

There are no wounds.

Voice-over:

```text
This can't be real...
```

---

## S10 — 00:30–00:34

Elena looks toward the front row.

Claire is sitting there smiling innocently.

Camera:

```text
slow zoom toward Claire
```

---

## S11 — 00:34–00:39

Rapid memory montage.

Reuse visuals from:

```text
S03
S04
S05
```

Very short flashes.

Voice-over:

```text
I came back...
```

---

## S12 — 00:39–00:44

Back at the wedding.

Adrian smiles and extends his hand toward Elena.

Dialogue:

```text
ADRIAN:
Elena?
```

Voice-over:

```text
Three years before they killed me.
```

---

## S13 — 00:44–00:50

Priest:

```text
Elena, do you take this man to be your husband?
```

Pause.

Adrian smiles.

Elena looks at him calmly.

Music fades out.

Elena says:

```text
No.
```

After she says it:

```text
complete silence for approximately 0.5 seconds
```

Then subtle dramatic impact sound.

---

## S14 — 00:50–00:57

Wedding guests react.

Elena turns away from Adrian.

She looks directly toward Claire.

Claire's smile disappears.

Cut back to Elena.

Elena gives a very subtle cold smile.

Voice-over:

```text
This time...
I'll destroy them first.
```

Cut to black.

Title:

```text
SECOND CHANCE
```

Then:

```text
EPISODE 2
```

---

# 8. Image Prompt Generation

Implement a prompt builder.

Every generated prompt must combine:

```text
character identity
+
shot description
+
current clothing
+
scene
+
visual style
+
lighting
+
camera composition
+
9:16
```

Example:

```text
Elena, a beautiful 27-year-old woman,
long straight black hair,
dark brown eyes,
oval face,
fair skin,
small beauty mark under her left eye,

lying injured on a deserted road at night during heavy rain,
wearing an elegant black evening dress,
wet hair stuck to her face,
terrified and betrayed expression,

wet asphalt reflecting street lights,
cold blue-gray cinematic lighting,
dark romance thriller atmosphere,

cinematic modern webtoon illustration,
semi-realistic graphic novel style,
dramatic close-up,
professional composition,
vertical 9:16
```

Save prompts into:

```text
data/storyboard.json
```

and:

```text
output/production_report.json
```

---

# 9. AI Provider Architecture

Do not hard-code one AI provider.

Create abstraction interfaces.

For images:

```python
class ImageProvider:
    def generate(self, prompt: str, output_path: str) -> str:
        ...
```

Implement:

```text
PlaceholderImageProvider
```

Optional adapters may be created for:

```text
OpenAI
Replicate
Stability
Fal
```

only if credentials exist.

Do not make the program fail because API keys are absent.

Environment variables should use:

```text
IMAGE_PROVIDER=placeholder
VOICE_PROVIDER=local
```

Example:

```text
OPENAI_API_KEY=
ELEVENLABS_API_KEY=
REPLICATE_API_TOKEN=
FAL_KEY=
```

---

# 10. Placeholder Mode

Placeholder mode is mandatory.

If AI generation APIs are unavailable:

Generate visually clean temporary storyboard frames automatically using Pillow.

Each placeholder must show:

```text
SHOT ID
shot description
characters
dialogue
voice-over
duration
```

Use a vertical 1080x1920 canvas.

The final MP4 must still render correctly using these frames.

This guarantees the project is always testable.

---

# 11. Audio

Create voice lines as individual audio assets.

Expected structure:

```text
assets/audio/
    s01_elena.wav
    s02_elena.wav
    s03_claire.wav
    s05_elena.wav
    s06_priest.wav
    s08_priest.wav
    s09_elena.wav
    s11_elena.wav
    s12_adrian.wav
    s12_elena.wav
    s13_priest.wav
    s13_elena.wav
    s14_elena.wav
```

Create a voice abstraction:

```python
class VoiceProvider:
    def synthesize(
        self,
        text: str,
        character: str,
        output_path: str
    ) -> str:
        ...
```

At minimum implement a fallback provider.

Fallback can use:

```text
macOS say
pyttsx3
espeak
```

depending on platform.

If none are available, generate silent WAV files of the expected duration so the pipeline remains functional.

---

# 12. Subtitles

Automatically create:

```text
output/episode_001.srt
```

Subtitles should include spoken dialogue and important narration.

Do not subtitle:

```text
rain
heartbeat
crash
```

Example:

```text
1
00:00:00,000 --> 00:00:03,000
The night I died...

2
00:00:03,000 --> 00:00:06,000
my husband was watching.
```

Burn subtitles into the final video.

Subtitle style:

```text
large readable white text
black outline
centered horizontally
positioned in lower third
safe margin from TikTok/Shorts UI
```

Highlighting individual words is not necessary.

---

# 13. Motion Effects

Static images must not simply stay motionless.

Implement basic motion effects using FFmpeg or Python.

Supported effects:

```text
slow_zoom_in
slow_zoom_out
pan_left
pan_right
shake
flash
fade
crossfade
```

Recommended mapping:

```text
S01 slow_zoom_in
S02 slow_zoom_in
S03 pan_right
S04 slow_zoom_in
S05 rapid_zoom + white flash
S06 black
S07 rapid_zoom_out
S08 slow_zoom_out
S09 slow_zoom_in
S10 slow_zoom_in
S11 flash montage
S12 slow_zoom_in
S13 slow_zoom_in
S14 slow_zoom_in
```

---

# 14. Music and SFX

The application should support optional files:

```text
assets/music/background.mp3

assets/sfx/rain.wav
assets/sfx/thunder.wav
assets/sfx/heartbeat.wav
assets/sfx/crash.wav
assets/sfx/impact.wav
```

If files are missing, skip them gracefully.

Music behavior:

00:00–00:15

```text
dark suspense
```

00:18–00:44

```text
mysterious emotional tension
```

00:44–00:50

music volume gradually decreases.

Before:

```text
No.
```

music should nearly disappear.

After "No":

play subtle impact sound.

00:50–00:57:

revenge / dark determination mood.

---

# 15. Rendering

Render each shot individually first:

```text
output/shots/S01.mp4
...
output/shots/S14.mp4
```

Then concatenate into:

```text
output/episode_001.mp4
```

Add:

```text
voice audio
music
sound effects
subtitles
```

Final duration should be approximately:

```text
57 seconds
```

Allow small variation depending on voice synthesis.

---

# 16. Character Reference Assets

Generate prompt text files:

```text
assets/characters/elena/reference_prompt.txt
assets/characters/adrian/reference_prompt.txt
assets/characters/claire/reference_prompt.txt
```

Also generate character-sheet prompts.

Elena character sheet:

```text
Character reference sheet of Elena, a beautiful 27-year-old woman,
long straight black hair,
dark brown eyes,
oval face,
fair skin,
small beauty mark under her left eye,
slim elegant figure,
refined facial features.

Front portrait,
three-quarter portrait,
side profile,
full body.

She wears a minimalist white satin wedding dress,
pearl earrings,
delicate silver necklace.

Cinematic modern webtoon illustration,
semi-realistic graphic novel style,
dark romance aesthetic,
detailed expressive eyes,
soft cinematic lighting,
consistent facial identity,
clean neutral background,
professional character design sheet.
```

Create equivalent files for Adrian and Claire.

---

# 17. Production Manifest

Create:

```text
data/production_manifest.json
```

Example:

```json
{
  "project": "SECOND CHANCE",
  "episode": 1,
  "resolution": "1080x1920",
  "fps": 30,
  "shots": 14,
  "characters": [
    "Elena",
    "Adrian",
    "Claire"
  ],
  "status": {
    "storyboard": true,
    "images": false,
    "voices": false,
    "render": false
  }
}
```

Update this automatically as assets are generated.

---

# 18. Logging

Print clear CLI output.

Example:

```text
[SECOND CHANCE]

[1/5] Loading project
[2/5] Building storyboard
[3/5] Generating image assets
  ✓ S01
  ✓ S02
  ✓ S03
...
[4/5] Generating audio
[5/5] Rendering video

DONE

Video:
output/episode_001.mp4

Subtitles:
output/episode_001.srt

Production report:
output/production_report.json
```

Errors for individual shots must not terminate the complete process when a fallback asset can be produced.

---

# 19. README

Write a high-quality README.

Include:

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Check FFmpeg:

```bash
ffmpeg -version
```

Run:

```bash
python main.py
```

Explain:

```text
placeholder mode
AI image mode
voice mode
rendering
folder structure
how to replace generated images manually
```

---

# 20. Manual Asset Replacement

This is important.

The user should be able to manually generate better images externally and replace:

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

The program must rebuild the final video using the manually replaced images.

Do not overwrite existing manually provided images unless:

```bash
--force
```

is specified.

---

# 21. CLI Options

Support:

```bash
python main.py --mode all
python main.py --mode storyboard
python main.py --mode assets
python main.py --mode audio
python main.py --mode render

python main.py --force
python main.py --episode 1
```

Optional:

```bash
python main.py --provider placeholder
```

---

# 22. Code Quality

Requirements:

* clean Python architecture
* type hints
* docstrings for important public methods
* no giant single-file implementation
* reusable classes
* provider abstraction
* graceful error handling
* pathlib instead of manually concatenated paths
* structured JSON/YAML data
* no hardcoded secrets
* deterministic file naming
* comments only where useful

---

# 23. Tests

At minimum test:

```text
14 storyboard shots exist
shot IDs are S01 through S14
shots are chronologically ordered
duration values are positive
total duration is between 50 and 65 seconds
all character names are valid
all shots have image prompts except black-screen shots
```

---

# 24. Acceptance Criteria

The task is complete only when:

* [ ] project folder is fully created
* [ ] `pip install -r requirements.txt` succeeds
* [ ] `python main.py --mode storyboard` succeeds
* [ ] `python main.py --mode all` succeeds without requiring paid API keys
* [ ] exactly 14 shots are created
* [ ] placeholder assets are created automatically
* [ ] subtitles are generated
* [ ] final MP4 is generated
* [ ] final MP4 is vertical 1080x1920
* [ ] final video duration is approximately 50–60 seconds
* [ ] all prompts are stored in structured data
* [ ] manually replacing images and rerunning render works
* [ ] existing manual images are not overwritten without `--force`
* [ ] README contains complete usage instructions
* [ ] tests pass

---

# 25. Final Instruction

Do not merely explain how to build this.

Actually create the entire project.

Run the program.

Fix runtime errors.

Run tests.

Generate the placeholder final video.

At the end, report:

```text
1. Files created
2. Commands executed
3. Test results
4. Final video path
5. Storyboard path
6. Character prompt paths
7. Any optional API integrations that remain disabled because credentials are missing
```

The main required deliverable is a working:

```text
output/episode_001.mp4
```

Do not stop after generating code.

The task is only finished after the local placeholder demo video has been successfully rendered.
