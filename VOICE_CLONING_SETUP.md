# Voice Cloning Setup (Render Machine)

This pipeline can narrate videos in **your own cloned voice** instead of the
Kokoro preset voice. Cloning is **zero-shot**: it reads one short reference clip
of your voice on every generation — **no training, no dataset, ~10-30s of audio
is enough** (not 60k-90k words).

## How it's wired

Every scene now calls one factory instead of hardcoding a voice:

```python
from voice import narration_service
self.set_speech_service(narration_service(kokoro_voice="af_bella"))
```

`voice.narration_service()` reads **`config.VOICE_ENGINE`** and returns either:

| VOICE_ENGINE | Engine | Voice |
|--------------|--------|-------|
| `"kokoro"` (default) | Kokoro preset | `af_bella` etc. — generic |
| `"clone"` | Chatterbox | **your voice**, from `assets/my_voice.wav` |

Nothing changes until you switch it, so current renders keep working.

## One-time setup on the render machine

1. **Create the isolated cloning venv** (keeps torch away from the manim venv,
   exactly like `.venv-kokoro`):
   ```bash
   python3 -m venv .venv-chatterbox
   .venv-chatterbox/bin/pip install --upgrade pip
   .venv-chatterbox/bin/pip install chatterbox-tts torchaudio
   ```
   > NVIDIA render box: install the CUDA build of torch first if you want GPU
   > speed — `chatterbox_tts.py` auto-detects `cuda` / `mps` / `cpu`.

2. **Add the reference clip:** place a 10-30s WAV of the target voice at
   `assets/my_voice.wav` (quiet room, mic 6-12in away, mono, 44.1/48 kHz).
   Path is configurable via `config.CLONE_REFERENCE`.

3. **Smoke-test the engine directly** (before rendering a whole video):
   ```bash
   echo "Hello, this is my cloned voice." | \
     .venv-chatterbox/bin/python chatterbox_tts.py \
       --reference assets/my_voice.wav --out /tmp/clone_test.wav
   # listen to /tmp/clone_test.wav
   ```

## Switching the pipeline to your voice

Either edit `config.py`:
```python
VOICE_ENGINE = "clone"
```
…or override per render without editing anything:
```bash
VOICE_ENGINE=clone python batch_render.py ...    # or your usual render command
```

To go back to Kokoro: set it to `"kokoro"` (or just don't set the env var).

## Files involved

| File | Role |
|------|------|
| `config.py` | `VOICE_ENGINE` switch + `CLONE_REFERENCE` path |
| `voice.py` | factory that picks the engine (all scenes call this) |
| `chatterbox_service.py` | manim-voiceover SpeechService (caching, subprocess) |
| `chatterbox_tts.py` | CLI inside `.venv-chatterbox` that does the actual cloning |
| `assets/my_voice.wav` | your reference clip (you provide this) |

## Notes / gotchas

- **First render is slow.** Chatterbox loads a ~1GB model per narration block.
  Generated audio is cached (sha256 by text + reference), so re-renders are fast.
  Re-recording the clip auto-invalidates the cache.
- Chatterbox is **English**. For other languages, swap to Qwen3-TTS or
  Chatterbox-Multilingual inside `chatterbox_tts.py` (same `generate()` shape).
- Cloning quality tracks clip quality: clean, consistent, no background noise.
  Add a 2nd/3rd clip and pick the best if the first sounds off.
- Only clone a voice you have the right to use.
