# Kinematics — Orange Nelumbo Design System (decoded from the official guideline files)

Source of truth for every Kinematics video. Two docs merged: the 2D Video Design Guideline
(used for most questions incl. 1D motion) and the 3D Manim Guideline (only for genuinely 3D
content). The Manim coder must follow this. Companion hard-rules live in `brand_system.md`.

═══════════════════════════════════════════════════════════════════════════
## PART A — 2D VIDEO DESIGN (default for almost every question)
═══════════════════════════════════════════════════════════════════════════

### Colour law (never swap the roles)
| Token | Hex | Meaning |
|---|---|---|
| Carbon canvas | `#0E0D10` / panels `#1E1B20`, `#161418` | background |
| IGNITION orange | `#FF5A1F` (grad `#FF8A3D`→`#FF5A1F`; EMBER `#FF7A2E`) | the concept IN FOCUS |
| VELOCITY CYAN | `#3DE0D0` | motion, vectors, trails, graph lines, measured data |
| Titanium / muted | `#8A8A93`, white @ 45% | scaffold, secondary text |
| Error red | `#E0483C` | wrong / negative states |
**Orange = concept in focus. Cyan = motion, vectors & data. Never swap.**

### Type
- **Space Grotesk** — headlines (falls back gracefully if not installed).
- **Manrope** — captions & body text.
- **JetBrains Mono** — ALL equations, values, units, and the mono chrome tags. Never set formulae in Manrope.

### Persistent chrome (identical on every frame)
- Top-left: `// KINEMATICS` (mono, orange).
- Below it / top-right: `ORANGE NELUMBO` wordmark + mark.
- Bottom-left: lesson label, e.g. `LESSON 03  ·  Equations of motion`.
- Top-right: progress count `NN / total` (e.g. `03 / 12`) + a progress bar.
- **Safe zone: keep titles & key diagrams inside the 90% title-safe box.**
  Bottom 12% may be covered by captions — NEVER put critical maths there.

### The video arc — 8 frame types (pick the ones the question needs, in order)
1. **TITLE** — chapter tag, lesson path (`PHYSICS · CH 01 · LESSON NN`), big two-line title.
2. **HOOK** — a question/paradox that pulls them in (e.g. "run 400 m, end where you started → displacement 0").
3. **CONCEPT** — split layout: idea on the LEFT, motion diagram on the RIGHT.
4. **FORMULA** — the governing equations; highlight the one `· IN FOCUS` (orange), others muted.
5. **EXAMPLE** — problem on the LEFT (GIVEN / FIND), stepped solution on the RIGHT (01,02,03 → ANSWER).
6. **GRAPH** — v–t or x–t; shade area = displacement; call out `slope = a`, `area = s`.
7. **RECAP** — ≤3 numbered takeaway bars (orange for a concept, cyan for a visual idea).
8. **END CARD** — next-lesson title + one Subscribe + one site CTA (orangenelumbo.com), orbital motif, hold 4–5 s.

### Motion motifs (the chapter's signature visuals)
motion trail + velocity vector · v–t / x–t graph · projectile arc · vector components (vₓ, v_y).
Give moving objects a fading cyan trail so frames "feel like they're moving."

### Frame recipes (how each teach-frame is laid out)
- **Concept**: heading + one-line definition left; a small labelled diagram (x₀, x, v arrow) right.
- **Formula**: the three equations of motion stacked, numbered 01/02/03, the in-focus one enlarged + orange.
- **Example**: left card = GIVEN (u,a,t) + FIND; right = numbered algebra steps ending in a boxed ANSWER.
- **Graph**: axes cyan, curve cyan, shaded area under curve = displacement (orange fill, low opacity).
- **Projectile (hero)**: one arc, decompose into vₓ (constant) and v_y (changes); mark Range R, Height H, v_y=0 at apex.
- **Recap**: numbered bars, ≤3.

═══════════════════════════════════════════════════════════════════════════
## PART B — 3D MANIM (ONLY for genuinely 3D content: motion in space, 3D vectors, surfaces)
═══════════════════════════════════════════════════════════════════════════
For 1D/2D motion use Part A — do NOT force 3D.

### Scene setup
- Subclass `ThreeDScene`. Standard establishing view: `set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)`.
  (phi = tilt from vertical, theta = spin, gamma = roll.) Three-quarter view reads as space without confusing.
- Chrome is 2D: add via `add_fixed_in_frame_mobjects(...)` so it never rotates with the camera.

### Depth cues — MANDATORY (never show 3D without a ground grid + shadow)
1. **Ground grid**: faint x–y `NumberPlane().set_opacity(0.15)` on the floor.
2. **Dropped shadow**: `always_redraw(lambda: Dot([*ball.get_center()[:2], 0], fill_opacity=0.3))`.
3. **Fade with distance**.
4. **Gentle orbit** (`begin_ambient_camera_rotation(rate=0.2)`) only if depth is still unclear after 2 s — don't add more labels.
Colour law carries over: cyan = motion, orange = acceleration/vertical, titanium = scaffold.

### 3D recipes
- **A · Projectile in space**: `traj(t)=[vx*t, vy*t, vz*t-0.5*g*t**2]`; `ParametricFunction` arc (IGNITION),
  `Sphere(0.12)` ball + shadow; `MoveAlongPath` then `move_camera(theta=30*DEGREES)`.
  Beat: open on a FRONT view (looks 2D/familiar) → orbit to reveal hidden sideways drift ("it was 3D all along").
- **B · Resolving a 3D vector**: `Arrow3D` + dashed `Line3D` projections onto each axis (cyan for x,y legs; orange for the vertical), ambient rotate to make vₓ,v_y,v_z unmistakable. Beat: |v|² = vₓ²+v_y²+v_z².
- **C · Orbit & frame change**: 3/4 view → `move_camera(phi=0, theta=-90)` top-down (flatten to familiar 2D) →
  ride object A's frame via an updater `world.add_updater(lambda m: m.shift(-A.get_center()))` to show relative motion.
- **D · Surfaces**: `Surface(...)` with `checkerboard_colors=[IGNITION, EMBER]`, `fill_opacity≤0.7` so the grid shows through,
  `resolution=(24,24)` draft. Reserve for "why 45°" moments — don't over-use.

### Camera choreography & performance
- `set_camera_orientation` = opening view · `move_camera` = deliberate ~3 s cut · `begin_ambient_camera_rotation` = idle orbit while explaining · settle back for the key reveal.
- AVOID: continuous spinning under narration (nausea); high surface res while drafting; more than ONE camera move per idea.
- Render: draft `-qm`, final `-qk` (4K).
- Always open on a familiar view before revealing depth.
