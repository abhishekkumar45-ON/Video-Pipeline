# Orange Nelumbo — DEBRIEF Video Pipeline

Turns a JEE question into a **brand-perfect 4K narrated Manim video** — intro bumper →
step-by-step solution → outro bumper, with the Orange Nelumbo logo, the grid+glow ground,
background music, and every rule from the DEBRIEF/brand guidelines baked in.

One command renders a scene to a finished, Drive-uploaded video. This README is the Ubuntu
setup + operating guide.

---

## 0. What is and isn't automatic (read this first)

| Stage | Who does it |
|---|---|
| Selecting a question, tracking status | pipeline (`questions.json`) |
| **Writing the Manim scene from a question** | **an LLM (Claude in chat), or a paid Anthropic API key** — see below |
| Overlap/off-frame gate, 4K render, music, intro+outro, loudness, Drive upload | pipeline (fully automatic) |

The one non-automatic step is **codegen** — turning a question into `scenes/<id>.py`. Headless
`claude -p` is disabled on this org and the paid API isn't used, so today the scene is written by
Claude *in chat* (paste the question, save the reply). Everything around it is one command.
So the loop is: **get the scene (chat) → save it → `orchestrator.py build`**.

---

## 1. Ubuntu quick start

```bash
git clone https://github.com/abhishekkumar45-ON/Video-Pipeline.git
cd Video-Pipeline
bash setup_ubuntu.sh          # system deps + .venv (manim) + .venv-kokoro (voice)
```

Then build any question whose scene already exists:

```bash
./.venv/bin/python orchestrator.py build q10 --quality=-qk --music --drive=gdrive:JEE-Videos/Thermodynamics
```

This runs: **py_compile → overlap gate → 4K render → wrap intro+outro → background music
(ducked) → upload to Drive → mark done**. The finished file is `outputs/<id>_wrapped_final.mp4`.

- `--quality=-ql` for a fast draft, `-qk` for the 4K master.
- Drop `--drive=...` to skip upload. Drop `--music` to skip music.
- Google Drive upload needs rclone once: `rclone config` → new remote named **`gdrive`**.

---

## 2. The one command

```
python orchestrator.py build <id> [--quality=-qk] [--music] [--music-vol 0.08] [--drive=REMOTE:FOLDER]
python orchestrator.py status          # table of every question + state
python orchestrator.py next            # print the paste-ready codegen prompt for the next pending question
```

`build` is self-contained — it puts the venv, apt/Homebrew tools and LaTeX on PATH itself, so it
runs from any directory with absolute paths and needs no `source`/`export`.

---

## 3. Making a NEW video (the full loop)

1. Add the question to `questions.json` (`id`, `chapter`, `question`, `options`, `answer`, `status:"pending"`).
2. `python orchestrator.py next` → copies a prompt (brand rules + a gold example + the question).
   Paste it to Claude in chat.
3. Save Claude's `scenes/<id>.py` reply into `scenes/`.
4. `python orchestrator.py build <id> --quality=-qk --music --drive=gdrive:JEE-Videos/<Chapter>`.

The gate rejects any overlap/off-frame; if the render fails it writes a repair prompt with the
traceback to paste back.

---

## 4. Project layout

```
orchestrator.py        the pipeline (build / status / next); wrap intro+outro; call add_bgm; upload
nelumbo.py             THE shared brand module — palette, fonts, on_logo(), background(),
                       StepRail, mchip(), kicker(). Every scene does `from nelumbo import *`.
layout_check.py        deterministic overlap / off-frame gate (renders with a mock silent voice)
add_bgm.py             mixes assets/bgm.mp3 under the narration (sidechain-ducked), limiter
kokoro_service.py      voice (Kokoro af_bella) — shells out to .venv-kokoro (isolated torch)
kokoro_tts.py          the Kokoro CLI run inside .venv-kokoro
guidelines/masterclass/  the operative rulebook (per-frame PYQ Masterclass spec + script/frame agents)
guidelines/            supporting brand/colour/diagram/YouTube specs
questions.json         source of truth: id / chapter / question / options / answer / status / video_url
scenes/<id>.py         one Manim scene per question (q1, q3, q5-q10, samples)
assets/                on_logo.png (real logo, transparent) . bg.png (grid+glow ground) .
                       intro.mp4 . outro.mp4 . bgm.mp3
outputs/               rendered mp4s (gitignored)          build/  media cache (gitignored)
setup_ubuntu.sh        one-shot Ubuntu installer
gcloud_tts_service.py / polly_service.py / elevenlabs_service.py / mac_say_service.py   alt voices
```

---

## 5. What every video gets (baked in - don't re-explain)

- **Intro -> solution -> outro** (assets/intro.mp4, assets/outro.mp4).
- **Chrome:** real Orange Nelumbo logo top-left, chapter bottom-left, **no** progress counter.
- **Ground:** obsidian + faint grid + dim radial glow (`assets/bg.png`), matching the intro.
- **DEBRIEF beats:** question card -> pause -> concept-first teaching -> working visual ->
  step-by-step solve with the **1.2.3 step rail** (green=done, orange=active) -> right-side
  **results rail** (LaTeX chips) -> lock-in. Diagrams dock bottom-right for reference.
- **Live readouts** where a process varies (e.g. V/P/T counting as a piston moves).
- **Voice:** Kokoro `af_bella`, teaching-style narration. **Music:** ducked under the voice
  (louder over the silent bumpers, quiet under teaching), gentle limiter.
- **Collision-clean** (the gate blocks any overlap), MathTex basictex-safe, banned animations
  (Flash/Wiggle/spins) not used.

Full rules: `guidelines/masterclass/` (and the supporting `guidelines/` specs).

---

## 6. Voices

Default is **Kokoro `af_bella`** (US, natural, offline - set up by `setup_ubuntu.sh`).
Swap per scene by changing the two voice lines:

| Service | Accent | Notes |
|---|---|---|
| `KokoroService()` | US | default; offline; `.venv-kokoro` |
| `GCloudTTSService()` | **Indian** (en-IN Chirp3-HD) | `pip install google-cloud-texttospeech`; key at `~/.gcp_tts_key.json` |
| `PollyService()` | Indian (Kajal) | AWS creds in `~/.aws/credentials` |
| `ElevenLabsService()` | Indian (Anika) | key in `~/.elevenlabs_key`; paid plan for library voices |

Secrets (AWS/GCP/ElevenLabs keys) are **never** committed - copy them to the box yourself.

---

## 7. Notes

- **Fonts:** `fonts-jetbrains-mono` is installed (maths). Headlines/body (Space Grotesk / Manrope)
  fall back gracefully; install them from Google Fonts for pixel-exact brand type.
- **4K is slow on a fanless laptop** (thermal throttling); Ubuntu with a fan / more cores is ideal.
  Render several ids in parallel terminals if needed.
- **Regenerate the background** (`assets/bg.png`) or **swap the logo** (`assets/on_logo.png`) any time;
  every scene picks them up via `nelumbo.py`.
- Older reference docs: `RENDER_UBUNTU.md`, `BATCH_GUIDE.md`. The original API-based scaffolding
  (`pipeline.py`, `scriptwriter.py`, `scene.py`, `config.py`) is kept but superseded by `orchestrator.py`.
