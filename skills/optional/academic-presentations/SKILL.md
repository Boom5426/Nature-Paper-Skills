---
name: academic-presentations
description: >-
  Create academic presentation slide decks and optionally demo videos from
  research papers. Use when the user asks to "make slides", "create a deck",
  "make a presentation", "demo video", "paper slides", "conference talk slides",
  or wants to turn a paper into a visual presentation. Covers slide generation,
  narration scripts, TTS audio, and video assembly.
---

# Academic Presentations

Produce slide decks (and optionally narrated demo videos) from research papers. The human drives all outline and visual decisions — the agent executes.

## Pipeline

```
[1] Script Draft ──→ [2] Slide Generation ──→ [3] TTS Audio (optional) ──→ [4] Video Assembly (optional)
     Claude Code          nanobanana /edit     edge-tts / Kokoro / ElevenLabs       ffmpeg
```

Skip stages 3–4 for slide-only output. User can enter at any stage.

## Stage 1: Script / Outline

**Input**: paper + user-provided outline or slide plan
**Output**: `video-scripts.md` or `slide-outline.md` — per-slide content with talking points

The agent drafts scripts based on the user's outline. The user owns the structure — agent does not decide slide count, order, or what to emphasize.

## Stage 2: Slide Generation

> Full reference: [references/slide-generation.md](references/slide-generation.md)

**Tool**: nanobanana (Gemini CLI extension)

**Priority order** (edit-first):
1. **Has paper figure** → nanobanana `/edit` to wrap into slide frame
2. **Has existing slide** → `/edit` to adapt
3. **User-provided reference** (e.g., from NotebookLM or PPTX the user made) → `/edit` to refine
4. **Title slide from scratch** → generate with academic style prompt
5. **Content slide from scratch** → generate with deck-style preamble

**Key principle**: prefer `/edit` on existing HQ paper figures over generating from scratch.

**Deck style**: create `deck-style.md` once per deck, prepend to all generate-from-scratch prompts. For `/edit`, style is inherited from the base image.

Example `deck-style.md`:
```markdown
- Canvas: 1920x1080, white background
- Accent: #2563EB blue, text: #1e293b dark slate
- Clean sans-serif, flat design, no gradients/shadows
- Bottom bar: blue accent with white affiliation text
```

## Stage 3: TTS Audio (optional)

> Full reference: [references/tts-engines.md](references/tts-engines.md)
> Batch scripts: [scripts/batch_tts_edge.py](scripts/batch_tts_edge.py), [scripts/batch_tts_kokoro.py](scripts/batch_tts_kokoro.py)

**Output**: one audio file per narrated slide

### Engine Selection

| Engine | Quality | Cost | Latency | Best For |
|--------|---------|------|---------|----------|
| **edge-tts** (default) | Very good | Free, unlimited | ~6s/slide (cloud) | Quick generation, good male voices |
| **Kokoro** | Very good | Free, unlimited | ~1.5s/slide (local) | Offline use, fast batch, good female voices |
| **ElevenLabs** | Premium | 10k chars free/mo | ~3s/slide (cloud) | Highest quality, voice cloning |

**Default**: Use edge-tts unless user requests offline or premium quality.

### Quick Start (edge-tts)

```python
import edge_tts, asyncio

async def tts_slide(text, output, voice="en-US-AndrewNeural"):
    await edge_tts.Communicate(text, voice).save(output)

asyncio.run(tts_slide("Your slide text here", "slide_01.mp3"))
```

**Voices**: AndrewNeural (male, presenter), AriaNeural (female), GuyNeural (male, warm), JennyNeural (female, pro)

## Stage 4: Video Assembly (optional)

**Tool**: ffmpeg
**Input**: slide PNGs + audio files + optional demo recording

```bash
# Use symlink to avoid iCloud path spaces: ln -sfn "long path" /tmp/workdir

# Slide with audio:
ffmpeg -y -loop 1 -i slide.png -i audio.mp3 \
  -c:v libx264 -tune stillimage -pix_fmt yuv420p \
  -c:a aac -ar 44100 -ac 2 -shortest seg.mp4

# Silent slide (N seconds):
ffmpeg -y -loop 1 -i slide.png -f lavfi -i anullsrc=r=44100:cl=stereo \
  -c:v libx264 -tune stillimage -pix_fmt yuv420p \
  -c:a aac -ar 44100 -ac 2 -t N seg.mp4

# Concat (always re-encode, never -c copy):
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\n..." > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -ar 44100 -ac 2 final.mp4
```

All segments MUST share: 44100Hz sample rate, stereo, AAC codec.

## PPTX Conversion (if needed)

> Full reference: [references/pptx-conversion.md](references/pptx-conversion.md)

If starting from an existing PPTX, convert slides to PNG images first:
```bash
soffice --headless --convert-to pdf --outdir output/ presentation.pptx
pdftoppm -png -r 300 output/presentation.pdf output/slide
```

## NotebookLM — Human Reference Only

**The agent must NOT auto-invoke NotebookLM or use its outputs to drive slide/script decisions.** The human owns the outline, visual arrangement, and deck direction.

**When to recommend**: only when the user says they're unsure what to put on slides or need inspiration.

## Gotchas

- **iCloud paths with spaces break ffmpeg** — symlink to `/tmp/`
- **Audio format mismatch breaks concat** — always re-encode with `-ar 44100 -ac 2`
- **ElevenLabs free tier** — `mp3_22050_32` only, 10k chars/month
- **edge-tts needs internet** — falls back to Kokoro if offline
- **Kokoro WAV files are ~7x larger** — convert to MP3 with ffmpeg before video assembly
- **Kokoro first run downloads ~350MB model** — ensure pip is in the venv
- **`/edit` distorts figure** — be more explicit: "Keep the original figure exactly as-is, only add framing"
- **Style drift across slides** — use `/edit` from base slide or prepend shared `deck-style.md`

## Dependencies

| Tool | Stage | Install |
|------|-------|---------|
| Gemini CLI + nanobanana | 2 | `gemini extensions install https://github.com/gemini-cli-extensions/nanobanana` |
| LibreOffice + poppler | 2 (PPTX) | `brew install --cask libreoffice && brew install poppler` |
| edge-tts | 3 | `pip install edge-tts` |
| Kokoro | 3 (offline) | `pip install kokoro soundfile` |
| ElevenLabs | 3 (premium) | `pip install elevenlabs` + `ELEVENLABS_API_KEY` |
| ffmpeg | 4 | `brew install ffmpeg` |
