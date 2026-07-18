# AGENT BRIEF — author ONE Orange Nelumbo DEBRIEF scene

You are writing a single Manim scene file for a JEE Thermodynamics "DEBRIEF" video.
Your output is a gate-clean `scenes/<id>.py`. You do NOT render 4K, add music, or upload —
that pipeline runs later. Work only in the repo at the current working directory.

## STEP 0 — read these first (in order), they are binding
1. `CLAUDE.md` — the project rulebook (chrome, colour law, banned animations).
2. `scenes/q10.py` — the GOLD EXAMPLE. **Copy its structure wholesale** and swap in your question.
3. `brand_system.md` — the full colour/animation grammar.
4. `nelumbo.py` — the helpers you must use: `background`, `on_logo`, `Body`, `Label`, `Mono`,
   `kicker`, `mchip`, `StepRail`, and the colour constants
   (`IGNITION, EMBER, SIGNAL, TITANIUM, CORRECT, ERROR, OBSIDIAN, GRAPHITE, WHITE`).

## THE MANDATORY SKELETON (copy from q10.py, keep verbatim)
```python
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo

class Scene_<id>(VoiceoverScene):
    def construct(self):
        background(self)
        self.set_speech_service(KokoroService(voice="af_bella"))

        logo = on_logo(0.5).to_corner(UL, buff=0.45)
        chapter = Body("Thermodynamics", color=TITANIUM).scale(0.4).to_corner(DL, buff=0.45)
        self.add(logo, chapter)
        # ... copy q10's add_result results-rail helper verbatim ...
```
Use the SAME `add_result(...)` results-rail helper q10 defines (right side, `mchip` LaTeX chips).
Use `.to_edge(UP, buff=LOGO_CLEAR)` on EVERY centered top header/readout (this is the 1.5 cm logo gap).

## BEAT STRUCTURE (same as q10) — the scene is ONLY the solution
1. **QUESTION card** — badge + exam tag ("JEE ADVANCED <year> · PAPER <n>") + format line
   (NUMERICAL, or "SINGLE CORRECT" / "MULTIPLE CORRECT · +4/−1"). Show the statement + options
   (if MCQ). Fade out.
2. **PAUSE & ATTEMPT IT** — the countdown ring (copy q10's beat 02).
3. **CONCEPT-FIRST** — teach the governing law(s) with a SMALL animation BEFORE solving
   (q10 uses three mini piston cards). Adapt to your physics.
4. **GROUNDWORK** — list the constants/laws you'll use (kicker header + MathTex lines).
5. **LIVE VISUAL** (include this whenever a quantity varies — volume, pressure, temperature,
   radius, plate temps): draw the real thing centre-left with `ValueTracker` + `DecimalNumber`
   live readouts that CHANGE as the process runs (copy q10's V/P/T machinery). Then dock the
   diagram bottom-right with `.animate.scale(0.4).to_corner(DR)`. If nothing numerically varies
   (pure matching/inequality question), animate the concept clearly instead.
6. **STEP RAIL SOLVE** — `StepRail(n)` on the left. Each step shows **LAW → SUBSTITUTION → RESULT**
   (three lines, not just a formula). `rail.active(i)` when a step starts, `rail.done(i)` when done.
   Push a `mchip` to the results rail for each key result.
7. **ANSWER LOCK-IN** — reveal the final answer once, boxed with `SurroundingRectangle` in CORRECT
   (green). Anchor everything to the KNOWN ANSWER in your spec; never contradict it.

## HARD RULES (the gate + a human reviewer both check)
- Voice: `KokoroService(voice="af_bella")`. Real logo top-left, `Body("Thermodynamics")` bottom-left.
- **NO** progress counter. **NO** `//` before any text. **NO** intro/outro/end-card/music in the scene.
- Colour law: IGNITION = active/target, EMBER = secondary, SIGNAL(cyan) = givens/data, TITANIUM =
  scaffold, AMBER = READ triggers only, CORRECT(green) = the answer once, ERROR(red) = a trap/wrong option.
- Banned: Flash, Wiggle, ApplyWave, camera spins/zooms. Use Write/Create/FadeIn/Indicate,
  `rate_func=smooth`, and FADE OUT each beat before the next fills the space.
- All maths in LaTeX (`v_0`, `T_1` — never "v0"). On-screen sentences start with a Capital letter.
- MathTex must be basictex-safe: `\text{}`, `\checkmark`, `\times` OK; **no** unicode ✓/✗; **no** `\boxed`
  (use colour + a SurroundingRectangle instead). `Label()` already bolds — do NOT pass `weight=BOLD`.
- Live readouts: `DecimalNumber` + `ValueTracker` (NEVER `always_redraw` a MathTex).
- Collision-clean: position with arrange/next_to/to_edge/to_corner; keep the work area LEFT of centre
  so it never touches the right results rail. Fade before you fill.

## GATE — you MUST leave it CLEAN before returning
Run repeatedly, fixing overlaps/off-frame by repositioning, until it prints `CLEAN`:
```
.venv/bin/python layout_check.py scenes/<id>.py Scene_<id>
```
(Ignore the SoX / "Font Space Grotesk not found" warnings — cosmetic. Grep the output for
`CLEAN` or `violation` / `OVERLAP` / `OFF-FRAME`.) Do NOT run `manim` at 4K and do NOT run
`orchestrator.py`. When the gate is CLEAN, return a one-line confirmation: `<id> CLEAN`.
```
```
