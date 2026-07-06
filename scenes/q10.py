"""
Orange Nelumbo · DEBRIEF · Thermodynamics · Q10 — "Compress, cool, expand"
JEE Advanced 2026 · Paper 2 · Multiple correct.  Answer: A, B, C  (D wrong).
Concept-first teaching + a working piston-cylinder synced to the P-V diagram + step rail.
No progress counter. Logo top-left, chapter bottom-left. Voice af_bella. 4K. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

WORKC = LEFT * 1.2


class Scene_q10(VoiceoverScene):
    def construct(self):
        background(self)
        self.set_speech_service(KokoroService(voice="af_bella"))

        # ---- chrome (no progress counter) ----
        logo = on_logo(0.5).to_corner(UL, buff=0.45)
        chapter = Body("Thermodynamics", color=TITANIUM).scale(0.4).to_corner(DL, buff=0.45)
        self.add(logo, chapter)

        self._ri = 0
        RAIL_X, RAIL_Y = 5.05, [2.3, 1.55, 0.8]
        def add_result(latex, color=SIGNAL):
            c = mchip(latex, color=color, tscale=0.4).move_to(RIGHT * RAIL_X + UP * RAIL_Y[self._ri])
            self._ri += 1
            self.play(FadeIn(c, shift=LEFT * 0.15), run_time=0.5, rate_func=smooth)
            return c

        # ============ 01 · QUESTION ============
        badge_t = Mono("1", color=OBSIDIAN).scale(0.5)
        badge = VGroup(SurroundingRectangle(badge_t, color=SIGNAL, fill_color=SIGNAL,
                       fill_opacity=1, buff=0.13, corner_radius=0.06), badge_t)
        meta = Mono("JEE ADVANCED 2026 · PAPER 2", color=EMBER).scale(0.32)
        fmt = Mono("MULTIPLE CORRECT · +4 / −1", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=1.0)
        q = VGroup(
            Body("10 mol of a monoatomic gas (state a: 300 K, volume V0).", color=WHITE).scale(0.46),
            Body("Suddenly compressed to V0/3  →  state b.", color=WHITE).scale(0.46),
            Body("Piston locked, cooled in an 11°C bath  →  state c.", color=WHITE).scale(0.46),
            Body("Piston slowly returned to V0 in the bath  →  state f.", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).next_to(head, DOWN, buff=0.6)
        opts = VGroup(
            Mono("A  the P–V diagram shown", color=TITANIUM).scale(0.42),
            Mono("B  ΔU(a→b) = 4860 R", color=TITANIUM).scale(0.42),
            Mono("C  net ΔU = −240 R", color=TITANIUM).scale(0.42),
            Mono("D  Pb = 2.08 atm,  Tb = 624 K", color=TITANIUM).scale(0.42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(q, DOWN, buff=0.5)
        with self.voiceover(text="Here's a rich JEE Advanced thermodynamics problem. A monoatomic gas is taken "
                                 "through three steps: a sudden compression, then cooling at fixed volume, then a "
                                 "slow expansion back — and we're asked which of four statements are correct.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            for ln in q:
                self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.5, rate_func=smooth)
            for o in opts:
                self.play(FadeIn(o, shift=RIGHT * 0.1), run_time=0.35)
            self.wait(max(0.2, t.duration - 4.8))
        self.play(FadeOut(head), FadeOut(q), FadeOut(opts))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause here, and sketch the three processes yourself first.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)),
                          run_time=max(0.4, (t.duration - 1.2) / 4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST (teach the 3 processes before solving) ============
        head3 = Label("First — the three moves, explained", color=WHITE).scale(0.6).to_edge(UP, buff=1.0)

        def mini_piston(compressed=False, color=IGNITION):
            w, fh, by = 0.55, 0.9, -0.45
            wall = VMobject(stroke_color=TITANIUM, stroke_width=3)
            wall.set_points_as_corners([[-w/2, fh+0.15, 0], [-w/2, by, 0], [w/2, by, 0], [w/2, fh+0.15, 0]])
            h = (fh * 0.4) if compressed else fh
            gas = Rectangle(width=w-0.05, height=h, fill_color=color, fill_opacity=0.30, stroke_width=0).move_to([0, by+h/2, 0])
            pist = Rectangle(width=w+0.1, height=0.1, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([0, by+h+0.05, 0])
            return VGroup(wall, gas, pist)

        def concept_card(title, sub, rel, relcol, icon):
            t_ = Label(title, color=IGNITION).scale(0.5)
            s_ = Body(sub, color=TITANIUM).scale(0.36)
            r_ = MathTex(rel, color=relcol).scale(0.6)
            txt = VGroup(t_, s_, r_).arrange(DOWN, buff=0.22)
            return VGroup(icon.scale(0.9), txt).arrange(DOWN, buff=0.35)

        c1 = concept_card("ADIABATIC", "sudden → no heat escapes", r"PV^{\gamma}=\text{const}", IGNITION, mini_piston(True, IGNITION))
        c2 = concept_card("ISOCHORIC", "piston locked → volume fixed", r"V=\text{const}", SIGNAL, mini_piston(False, SIGNAL))
        c3 = concept_card("ISOTHERMAL", "slow in a bath → temp fixed", r"T=\text{const}", EMBER, mini_piston(False, EMBER))
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.1).next_to(head3, DOWN, buff=0.7)
        with self.voiceover(text="Before we touch the numbers, let's understand the three moves. First — adiabatic. "
                                 "A sudden squeeze gives no time for heat to leave, so P V to the gamma stays constant, "
                                 "and the gas heats up.") as t:
            self.play(Write(head3), run_time=0.8)
            self.play(FadeIn(c1, shift=UP * 0.15), run_time=1.0)
            self.wait(max(0.1, t.duration - 1.8))
        with self.voiceover(text="Second — isochoric. Lock the piston and the volume can't change, so no work is done; "
                                 "cooling just drops the pressure.") as t:
            self.play(FadeIn(c2, shift=UP * 0.15), run_time=1.0)
            self.wait(max(0.1, t.duration - 1.0))
        with self.voiceover(text="Third — isothermal. Move the piston slowly in a water bath and the temperature stays "
                                 "pinned, so the internal energy doesn't change at all.") as t:
            self.play(FadeIn(c3, shift=UP * 0.15), run_time=1.0)
            self.wait(max(0.1, t.duration - 1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · WORKING VISUALISATION (piston + P-V in lockstep) ============
        CX = -3.9; base_y = -1.7; full_h = 3.0; cw = 1.5
        wl, wr, wt = CX - cw/2, CX + cw/2, base_y + full_h
        walls = VMobject(stroke_color=TITANIUM, stroke_width=4)
        walls.set_points_as_corners([[wl, wt+0.5, 0], [wl, base_y, 0], [wr, base_y, 0], [wr, wt+0.5, 0]])

        def gas_rect(vol, col=IGNITION):
            h = vol * full_h
            return Rectangle(width=cw-0.06, height=h, fill_color=col, fill_opacity=0.28, stroke_width=0).move_to([CX, base_y+h/2, 0])

        def piston_g(vol):
            h = vol * full_h
            bar = Rectangle(width=cw+0.14, height=0.14, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([CX, base_y+h+0.07, 0])
            rod = Rectangle(width=0.13, height=0.45, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([CX, base_y+h+0.07+0.3, 0])
            return VGroup(bar, rod)

        gas = gas_rect(1.0); pist = piston_g(1.0)
        cyl_lbl = Mono("piston & cylinder", color=TITANIUM).scale(0.34).next_to(walls, DOWN, buff=0.2)

        # P-V axes on the right
        Ox, Oy = 2.5, -1.7
        def PV(vx, py): return np.array([Ox + vx, Oy + py, 0])
        vax = Arrow(PV(0, 0), PV(3.3, 0), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.18)
        pax = Arrow(PV(0, 0), PV(0, 3.9), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.18)
        vlab = Mono("V", color=TITANIUM).scale(0.4).next_to(vax, RIGHT, buff=0.1)
        plab = Mono("P", color=TITANIUM).scale(0.4).next_to(pax, UP, buff=0.1)
        A, B, C, F = PV(2.8, 1.0), PV(0.95, 3.3), PV(0.95, 1.55), PV(2.8, 0.28)
        dA = Dot(A, color=SIGNAL).scale(0.7); lA = Mono("a", color=SIGNAL).scale(0.42).next_to(dA, UR, buff=0.05)
        moving = Dot(A, color=IGNITION).scale(0.9)

        with self.voiceover(text="Now watch it happen. On the left, the real piston and cylinder; on the right, the "
                                 "P–V diagram, moving in lockstep. We start at state a, at full volume.") as t:
            self.play(Create(walls), FadeIn(gas), FadeIn(pist), FadeIn(cyl_lbl), run_time=1.3)
            self.play(Create(vax), Create(pax), FadeIn(vlab), FadeIn(plab), run_time=1.0)
            self.play(FadeIn(dA), FadeIn(lA), FadeIn(moving, scale=1.3), run_time=0.7)
            self.wait(max(0.1, t.duration - 3.0))

        adia = VMobject(color=IGNITION, stroke_width=4); adia.set_points_smoothly([A, PV(1.7, 1.6), B])
        dB = Dot(B, color=IGNITION).scale(0.7); lB = Mono("b", color=IGNITION).scale(0.42).next_to(dB, UP, buff=0.1)
        with self.voiceover(text="Sudden compression — the piston slams down to a third of the volume. That's the steep "
                                 "adiabatic curve up to b, and the gas gets hot.") as t:
            self.play(Transform(gas, gas_rect(1/3)), Transform(pist, piston_g(1/3)),
                      MoveAlongPath(moving, adia), Create(adia), run_time=min(2.4, max(1.2, t.duration-1.4)))
            self.play(FadeIn(dB), FadeIn(lB), run_time=0.5)
            self.wait(max(0.1, t.duration - 2.9))

        iso_bc = Line(B, C, color=EMBER, stroke_width=4)
        dC = Dot(C, color=EMBER).scale(0.7); lC = Mono("c", color=EMBER).scale(0.42).next_to(dC, LEFT, buff=0.1)
        with self.voiceover(text="Now the piston is locked and the cylinder is cooled in the bath. Volume can't move, "
                                 "so the point drops straight down to c as the pressure falls.") as t:
            self.play(Transform(gas, gas_rect(1/3, EMBER)),
                      MoveAlongPath(moving, iso_bc), Create(iso_bc), run_time=min(2.0, max(1.0, t.duration-1.2)))
            self.play(FadeIn(dC), FadeIn(lC), run_time=0.5)
            self.wait(max(0.1, t.duration - 2.5))

        isot = VMobject(color=SIGNAL, stroke_width=4); isot.set_points_smoothly([C, PV(1.7, 0.95), F])
        dF = Dot(F, color=SIGNAL).scale(0.7); lF = Mono("f", color=SIGNAL).scale(0.42).next_to(dF, DR, buff=0.05)
        with self.voiceover(text="Finally the piston is drawn slowly back to full volume, staying in the bath — an "
                                 "isothermal expansion along the gentle curve to f.") as t:
            self.play(Transform(gas, gas_rect(1.0, SIGNAL)), Transform(pist, piston_g(1.0)),
                      MoveAlongPath(moving, isot), Create(isot), run_time=min(2.4, max(1.2, t.duration-1.2)))
            self.play(FadeIn(dF), FadeIn(lF), run_time=0.5)
            self.wait(max(0.1, t.duration - 2.9))

        pv_group = VGroup(vax, pax, vlab, plab, adia, iso_bc, isot, dA, dB, dC, dF, lA, lB, lC, lF, moving)
        self.play(FadeOut(walls), FadeOut(gas), FadeOut(pist), FadeOut(cyl_lbl),
                  pv_group.animate.scale(0.42).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 05 · STEP RAIL + SOLVE ============
        rail = StepRail(3)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        # STEP 1 — Tb
        s1t = Label("STEP 1 — heat of the adiabatic squeeze", color=WHITE).scale(0.44).move_to(WORKC + UP * 1.9)
        s1a = MathTex(r"T_b = T_a\left(\tfrac{V_a}{V_b}\right)^{\gamma-1} = 300\cdot 3^{2/3}", color=WHITE).scale(0.62).move_to(WORKC + UP * 0.7)
        s1b = MathTex(r"= 300\cdot 2.08 = 624\ \mathrm{K}", color=IGNITION).scale(0.7).move_to(WORKC + DOWN * 0.6)
        with self.voiceover(text="Step one. The adiabatic law gives T-b equals T-a times three to the two-thirds — "
                                 "that's three hundred times two point zero eight, which is six hundred twenty-four kelvin.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(2.0, t.duration))
            self.play(Write(s1b), run_time=1.0)
            add_result(r"T_b = 624\ \mathrm{K}", IGNITION)
            self.wait(max(0.1, t.duration - 3.0))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), rail.done(0), rail.active(1))

        # STEP 2 — dU a->b (option B)
        s2t = Label("STEP 2 — ΔU from a to b", color=WHITE).scale(0.46).move_to(WORKC + UP * 1.9)
        s2a = MathTex(r"\Delta U_{a\to b} = nC_V\,\Delta T = 10\cdot\tfrac{3}{2}R\,(624-300)", color=WHITE).scale(0.56).move_to(WORKC + UP * 0.6)
        s2b = MathTex(r"= 15R\cdot 324 = 4860\,R \quad\Rightarrow\ \text{(B)}\,\checkmark", color=CORRECT).scale(0.58).move_to(WORKC + DOWN * 0.7)
        with self.voiceover(text="Step two. Internal energy change is n C-v delta T. Ten times three-halves R times the "
                                 "three-twenty-four kelvin rise gives four thousand eight hundred sixty R. Option B is correct.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(2.2, t.duration))
            self.play(Write(s2b), run_time=1.0)
            add_result(r"\Delta U_{a\to b}=4860R", CORRECT)
            self.wait(max(0.1, t.duration - 3.2))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), rail.done(1), rail.active(2))

        # STEP 3 — net dU (option C)
        s3t = Label("STEP 3 — net ΔU (state function)", color=WHITE).scale(0.46).move_to(WORKC + UP * 1.9)
        s3a = MathTex(r"\Delta U_{\text{net}} = nC_V(T_f - T_a) = 15R(284-300)", color=WHITE).scale(0.58).move_to(WORKC + UP * 0.6)
        s3b = MathTex(r"= 15R(-16) = -240\,R \quad\Rightarrow\ \text{(C)}\,\checkmark", color=CORRECT).scale(0.58).move_to(WORKC + DOWN * 0.7)
        with self.voiceover(text="Step three. Internal energy is a state function — it only cares about the start and end "
                                 "temperatures, three hundred and two eighty-four. So the net change is fifteen R times "
                                 "minus sixteen: minus two hundred forty R. Option C is correct.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.2, t.duration))
            self.play(Write(s3b), run_time=1.0)
            add_result(r"\Delta U_{\text{net}}=-240R", CORRECT)
            self.wait(max(0.1, t.duration - 3.2))
        self.play(FadeOut(s3t), FadeOut(s3a), FadeOut(s3b), rail.done(2))

        # ============ 06 · OPTION D (the trap) ============
        dlbl = kicker("D", "OPTION D — THE TRAP", color=ERROR).move_to(WORKC + UP * 1.9)
        d1 = MathTex(r"P_b = P_a\,3^{5/3} = 3\cdot 2.08\,P_a \approx 6.24\,P_a", color=WHITE).scale(0.6).move_to(WORKC + UP * 0.5)
        d2 = MathTex(r"6.24 \neq 2.08 \quad\Rightarrow\ \text{(D)}\,\times", color=ERROR).scale(0.62).move_to(WORKC + DOWN * 0.7)
        with self.voiceover(text="Now the trap. T-b of six twenty-four is right, but the pressure isn't two point zero "
                                 "eight — it's P-a times three to the five-thirds, about six point two four. So option D "
                                 "mixes up the numbers and is wrong.") as t:
            self.play(FadeIn(dlbl), Write(d1), run_time=min(2.2, t.duration))
            self.play(Write(d2), run_time=1.0)
            self.wait(max(0.1, t.duration - 3.2))
        self.play(FadeOut(dlbl), FadeOut(d1), FadeOut(d2))

        # ============ 07 · LOCK-IN ============
        a_ok = MathTex(r"\text{(A) the P-V picture matches}\ \checkmark", color=CORRECT).scale(0.55).move_to(WORKC + UP * 0.6)
        ans = Label("ANSWER:   A ,  B ,  C", color=IGNITION).scale(0.8).move_to(WORKC + DOWN * 0.7)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        with self.voiceover(text="And option A? The diagram we drew — steep adiabatic, vertical isochoric, gentle "
                                 "isothermal — is exactly right, so A is correct too.") as t:
            self.play(Write(a_ok), run_time=min(1.8, t.duration))
            self.wait(max(0.1, t.duration - 1.8))
        with self.voiceover(text="So the answer is A, B, and C. One trap dodged, three marks earned. That's it — "
                                 "solved, completely.") as t:
            self.play(FadeIn(ans, shift=UP * 0.1), run_time=0.9)
            self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.7))
        self.wait(0.6)
