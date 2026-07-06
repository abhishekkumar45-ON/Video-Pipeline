# CLAUDE.md — read this fully before writing any scene

This repo turns a JEE question into a brand-perfect 4K **DEBRIEF** video (Orange Nelumbo).
Your job when asked to make a video is to write `scenes/<id>.py` — a Manim scene — that follows
**every** rule below. Then the user runs one command and the pipeline renders it, adds the intro
and outro bumpers, mixes music, and uploads it. If you skip any rule, the video ships wrong.

## Before you write a scene, READ these three (in order)
1. **`brand_system.md`** — the full rulebook (colour law, 9 beats, animation grammar, collision law).
2. **`scenes/q10.py`** — the GOLD EXAMPLE. Copy its structure, chrome, and helpers exactly.
3. **`guidelines/03_debrief_format.txt`** (and the others in `guidelines/`) — the source specs.

## The workflow (codegen is done here, in chat — the pipeline can't call an LLM)
1. Add the question to `questions.json` (`id, chapter, question, options, answer, status:"pending"`).
2. Write `scenes/<id>.py` (class `Scene_<id>`) following the checklist below.
3. Run the gate until it prints CLEAN:
   `.venv/bin/python layout_check.py scenes/<id>.py Scene_<id>`
4. Build (renders 4K, wraps intro/outro, adds ducked music, uploads):
   `.venv/bin/python orchestrator.py build <id> --quality=-qk --music --drive=gdrive:JEE-Videos/<Chapter>`
5. **VERIFY visually**: extract a few frames with ffmpeg and LOOK at them before reporting. The user
   rejects claimed-but-wrong results. Report with the Drive link.

## SCENE CHECKLIST — every item is mandatory (this is what other chats keep missing)
- [ ] `from manim import *`, `from nelumbo import *`, `VoiceoverScene`, `KokoroService`.
- [ ] First lines: `background(self)`  then  `self.set_speech_service(KokoroService(voice="af_bella"))`.
- [ ] **Chrome:** `on_logo(0.5).to_corner(UL, buff=0.45)` (real logo, top-left) + a `Body("<Chapter>")`
      bottom-left. **NO progress counter. NO "//" before any text.**
- [ ] **Solve uses `StepRail(n)`** on the left — `rail.active(i)` / `rail.done(i)` as steps complete.
- [ ] **Results rail** on the right — `mchip(r"...latex...", color=...)` for each key result (LaTeX).
- [ ] **Diagram/visual:** draw it centre, then dock bottom-right (`.animate.scale(0.4).to_corner(DR)`).
- [ ] **Concept-first:** teach the governing concept(s) with a small animation BEFORE solving.
- [ ] **Detailed steps:** each step shows LAW → SUBSTITUTION → RESULT (not just the formula). More
      steps / longer video is fine.
- [ ] **Live readouts** where a quantity varies: `DecimalNumber` + `ValueTracker` (NEVER always_redraw
      a MathTex). Show the piston/point MOVE and the numbers change (see q10's V/P/T).
- [ ] **All maths in LaTeX:** `v_0`, `T_1` — never "v0"/"T1" in Mono text. On-screen sentences start
      with a Capital letter.
- [ ] **Colour law:** IGNITION=active/target, EMBER=secondary/tricks, SIGNAL(cyan)=givens/data only,
      TITANIUM=scaffold, AMBER=READ-beat triggers only, CORRECT(green)=answer once, ERROR(red)=trap.
- [ ] **Banned animations:** no Flash / Wiggle / ApplyWave / camera spins / zooms. Use
      Write / Create / FadeIn / Indicate, `rate_func=smooth`, fade out each beat before the next.
- [ ] **NO intro, NO outro, NO end card, NO music in the scene** — the pipeline adds all of those.
      The scene is ONLY the solution: question card → pause → concept → solve → answer/takeaway.
- [ ] **MathTex basictex-safe:** `\text{}` and `\checkmark`/`\times` work; unicode ✓/✗ do NOT; no
      `\boxed`. `Label()` already bolds — do NOT pass `weight=BOLD` again (it crashes).
- [ ] **Collision-clean:** position with arrange/next_to/to_edge/to_corner; fade before you fill;
      keep the work area LEFT of centre so it never touches the right rail. The gate is binding.

## Voice / assets
Default voice Kokoro `af_bella`. Real logo `assets/on_logo.png`, ground `assets/bg.png`,
bumpers `assets/intro.mp4` / `assets/outro.mp4`, music `assets/bgm.mp3` — all wired via
`nelumbo.py` and the pipeline. Secrets (Drive/API keys) are never in the repo.

## The one constraint
Headless `claude -p` is disabled for this org and the paid API is not used, so YOU (in chat) write
the scene. Everything else is the one `orchestrator.py build` command.
