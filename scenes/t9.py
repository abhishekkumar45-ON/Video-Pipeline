"""
Orange Nelumbo · DEBRIEF · Thermodynamics · t9 — "Isothermal then adiabatic expansion of helium"
JEE Advanced 2020 · Paper 1 · Numerical.  Answer: f = 16/9 ≈ 1.78.
Concept-first + P–V plane with an isotherm segment (EMBER) then a steeper adiabatic segment
(IGNITION) in lockstep with a LIVE V readout as a dot travels + full step-by-step derivation +
step rail. No progress counter. Voice af_bella. 4K. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from voice import narration_service

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t9(VoiceoverScene):
    def construct(self):
        background(self)
        self.set_speech_service(narration_service(kokoro_voice="af_bella"))

        logo = on_logo(0.5).to_corner(UL, buff=0.45)
        chapter = Body("Thermodynamics", color=TITANIUM).scale(0.4).to_corner(DL, buff=0.45)
        self.add(logo, chapter)

        self._ri = 0
        RAIL_X, RAIL_Y = 5.05, [2.4, 1.75, 1.1, 0.45, -0.2]
        def add_result(latex, color=SIGNAL):
            c = mchip(latex, color=color, tscale=0.36).move_to(RIGHT * RAIL_X + UP * RAIL_Y[self._ri])
            self._ri += 1
            self.play(FadeIn(c, shift=LEFT * 0.15), run_time=0.5, rate_func=smooth)
            return c

        # ============ 01 · QUESTION ============
        bt = Mono("1", color=OBSIDIAN).scale(0.5)
        badge = VGroup(SurroundingRectangle(bt, color=SIGNAL, fill_color=SIGNAL, fill_opacity=1, buff=0.13, corner_radius=0.06), bt)
        meta = Mono("JEE ADVANCED 2020 · PAPER 1", color=EMBER).scale(0.32)
        fmt = Mono("NUMERICAL", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)
        q = VGroup(
            Body("One mole of helium at (P₁, V₁).", color=WHITE).scale(0.46),
            Body("Expands ISOTHERMALLY to 4V₁, then ADIABATICALLY to 32V₁.", color=WHITE).scale(0.46),
            Body("The two works satisfy  W_iso / W_adia = f · ln 2.", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.55)
        ask = Mono("Find f.", color=IGNITION).scale(0.5).next_to(q, DOWN, buff=0.5)
        with self.voiceover(text="Here's a two-step gas problem. One mole of helium first expands isothermally to four "
                                 "times its volume, then adiabatically all the way to thirty-two times. The ratio of the "
                                 "two works is f times the natural log of two, and we must find f.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            for ln in q:
                self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.45, rate_func=smooth)
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.4)
            self.wait(max(0.2, t.duration - 4.6))
        self.play(FadeOut(head), FadeOut(q), FadeOut(ask))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause, and set up the two works yourself first.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — the two kinds of work", color=WHITE).scale(0.58).to_edge(UP, buff=LOGO_CLEAR)
        def mini(compressed=False, color=IGNITION):
            w, fh, by = 0.55, 0.9, -0.45
            wall = VMobject(stroke_color=TITANIUM, stroke_width=3)
            wall.set_points_as_corners([[-w/2, fh+0.15, 0], [-w/2, by, 0], [w/2, by, 0], [w/2, fh+0.15, 0]])
            h = fh*0.4 if compressed else fh
            gas = Rectangle(width=w-0.05, height=h, fill_color=color, fill_opacity=0.30, stroke_width=0).move_to([0, by+h/2, 0])
            pst = Rectangle(width=w+0.1, height=0.1, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([0, by+h+0.05, 0])
            return VGroup(wall, gas, pst)
        def ccard(title, sub, rel, relcol, icon):
            return VGroup(icon.scale(0.9),
                          VGroup(Label(title, color=IGNITION).scale(0.5), Body(sub, color=TITANIUM).scale(0.35),
                                 MathTex(rel, color=relcol).scale(0.54)).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.32)
        c1 = ccard("ISOTHERMAL", "T fixed → use ln of ratio", r"W = nRT\ln\tfrac{V_f}{V_i}", EMBER, mini(False, EMBER))
        c2 = ccard("ADIABATIC", "no heat, Q = 0", r"TV^{\gamma-1}=\text{const}", IGNITION, mini(True, IGNITION))
        c3 = ccard("ADIABATIC W", "work equals −ΔU", r"W = \tfrac{nR(T_i-T_f)}{\gamma-1}", SIGNAL, mini(False, SIGNAL))
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.05).next_to(head3, DOWN, buff=0.7)
        with self.voiceover(text="Before any numbers, three ideas. First, isothermal work: the temperature is fixed, so "
                                 "the work is n R T times the natural log of the volume ratio.") as t:
            self.play(Write(head3), run_time=0.8); self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="Second, adiabatic — no heat flows, so T V to the gamma minus one is constant, which "
                                 "fixes the temperature after the expansion.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        with self.voiceover(text="Third, because Q is zero, the adiabatic work equals minus the change in internal energy: "
                                 "n R times the temperature drop, over gamma minus one.") as t:
            self.play(FadeIn(c3, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"n=1,\quad \text{helium is monatomic}\ \Rightarrow\ \gamma=\tfrac{5}{3}", color=WHITE).scale(0.6),
            MathTex(r"\gamma-1=\tfrac{5}{3}-1=\tfrac{2}{3}", color=SIGNAL).scale(0.6),
            MathTex(r"\text{isothermal: } V_1 \to 4V_1 \ \text{ at } T_1", color=EMBER).scale(0.6),
            MathTex(r"\text{adiabatic: } 4V_1 \to 32V_1 \quad(\text{ratio } 8)", color=IGNITION).scale(0.6),
        ).arrange(DOWN, buff=0.42).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. Helium is monatomic, so gamma is five-thirds and gamma minus one is "
                                 "two-thirds. The first leg is isothermal, from V-one to four V-one at temperature T-one. "
                                 "The second leg is adiabatic, from four V-one to thirty-two V-one — a volume ratio of "
                                 "eight.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · WORKING VISUALISATION with LIVE V readout on a P–V plane ============
        vt = ValueTracker(1.0)
        lbl = Mono("V =", color=TITANIUM).scale(0.44)
        nV = DecimalNumber(vt.get_value(), num_decimal_places=0, color=SIGNAL, font_size=40)
        nV.add_updater(lambda m: m.set_value(vt.get_value()))
        uV = Mono("V₁", color=SIGNAL).scale(0.4)
        readout = VGroup(lbl, nV, uV).arrange(RIGHT, buff=0.42).to_edge(UP, buff=LOGO_CLEAR)

        Ox, Oy = -5.4, -2.6
        SX = 0.30   # horizontal scale so 32 volume units span the plane
        def PV(vx, py): return np.array([Ox + vx * SX, Oy + py, 0])
        vax = Arrow(PV(0, 0), PV(35, 0), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        pax = Arrow(PV(0, 0), PV(0, 4.6), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        vlab = Mono("V", color=TITANIUM).scale(0.4).next_to(vax, RIGHT, buff=0.1)
        plab = Mono("P", color=TITANIUM).scale(0.4).next_to(pax, UP, buff=0.1)

        # P ∝ 1/V on the isotherm; keep the curve on-plane with a fixed constant.
        K = 4.0
        def iso_pt(v):  return PV(v, K / v)
        A = iso_pt(1.0)      # start: V=1
        B = iso_pt(4.0)      # after isothermal: V=4
        # adiabatic from B: P ∝ V^-gamma, gamma=5/3. P_B=K/4=1.0 at V=4.
        PB = K / 4.0
        def adia_pt(v): return PV(v, PB * (4.0 / v) ** (5.0/3.0))
        Fp = adia_pt(32.0)   # end: V=32

        dA = Dot(A, color=SIGNAL).scale(0.7); lA = Mono("V₁", color=SIGNAL).scale(0.36).next_to(dA, UP, buff=0.08)
        moving = Dot(A, color=IGNITION).scale(0.95)

        with self.voiceover(text="Now watch it live on the P–V plane. The volume readout is up top, in units of V-one. "
                                 "We start at V-one, high pressure, on the left.") as t:
            self.play(Create(vax), Create(pax), FadeIn(vlab), FadeIn(plab), run_time=1.0)
            self.play(FadeIn(dA), FadeIn(lA), FadeIn(moving), FadeIn(readout, shift=DOWN*0.15), run_time=0.9)
            self.wait(max(0.1, t.duration - 1.9))

        iso_curve = VMobject(color=EMBER, stroke_width=5)
        iso_curve.set_points_smoothly([iso_pt(v) for v in np.linspace(1.0, 4.0, 12)])
        dB = Dot(B, color=EMBER).scale(0.7); lB = Mono("4V₁", color=EMBER).scale(0.36).next_to(dB, UR, buff=0.06)
        with self.voiceover(text="First the isothermal expansion to four V-one. Temperature is fixed, so the gas glides "
                                 "down the gentle EMBER hyperbola while the volume climbs from one to four.") as t:
            self.play(vt.animate.set_value(4.0), MoveAlongPath(moving, iso_curve), Create(iso_curve),
                      run_time=min(3.0, max(1.8, t.duration-1.2)))
            self.play(FadeIn(dB), FadeIn(lB), run_time=0.5)
            self.wait(max(0.1, t.duration - 3.5))

        adia_curve = VMobject(color=IGNITION, stroke_width=5)
        adia_curve.set_points_smoothly([adia_pt(v) for v in np.linspace(4.0, 32.0, 16)])
        dF = Dot(Fp, color=IGNITION).scale(0.7); lF = Mono("32V₁", color=IGNITION).scale(0.36).next_to(dF, UR, buff=0.06)
        with self.voiceover(text="Then the adiabatic expansion to thirty-two V-one. With no heat, the pressure drops "
                                 "faster — the steeper IGNITION curve — and the volume runs all the way out to thirty-two.") as t:
            self.play(vt.animate.set_value(32.0), MoveAlongPath(moving, adia_curve), Create(adia_curve),
                      run_time=min(3.2, max(1.8, t.duration-1.2)))
            self.play(FadeIn(dF), FadeIn(lF), run_time=0.5)
            self.wait(max(0.1, t.duration - 3.7))

        nV.clear_updaters()
        pv_group = VGroup(vax, pax, vlab, plab, iso_curve, adia_curve, dA, dB, dF, lA, lB, lF, moving)
        self.play(FadeOut(readout), pv_group.animate.scale(0.4).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 06 · STEP RAIL + DETAILED SOLVE ============
        rail = StepRail(4, top=1.5, gap=1.0, size=0.56)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        s1t = Label("STEP 1 — the isothermal work", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s1a = MathTex(r"W_{\text{iso}} = nRT_1 \ln\!\frac{V_f}{V_i} = RT_1 \ln\!\frac{4V_1}{V_1}", color=WHITE).scale(0.55).move_to(WORKC + UP*0.9)
        s1b = MathTex(r"= RT_1 \ln 4 = 2\,R T_1 \ln 2", color=EMBER).scale(0.62).move_to(WORKC + DOWN*0.3)
        with self.voiceover(text="Step one. The isothermal work is n R T-one times the log of the volume ratio — R T-one "
                                 "times the log of four. And log of four is two times log of two, so the isothermal work "
                                 "is two R T-one log two.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(2.2, t.duration))
            self.play(Write(s1b), run_time=1.2)
            add_result(r"W_{\text{iso}} = 2RT_1\ln 2", EMBER)
            self.wait(max(0.1, t.duration - 3.6))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), rail.done(0), rail.active(1))

        s2t = Label("STEP 2 — temperature after the adiabatic", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s2a = MathTex(r"T V^{\gamma-1} = \text{const} \ \Rightarrow\ T_f = T_1\!\left(\tfrac{4V_1}{32V_1}\right)^{2/3}", color=WHITE).scale(0.54).move_to(WORKC + UP*0.9)
        s2b = MathTex(r"T_f = T_1\left(\tfrac{1}{8}\right)^{2/3} = T_1\cdot 8^{-2/3}", color=WHITE).scale(0.58).move_to(WORKC + DOWN*0.3)
        s2c = MathTex(r"= T_1\cdot 2^{-2} = \tfrac{T_1}{4}", color=IGNITION).scale(0.62).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step two, the temperature after the adiabatic leg. T V to the gamma minus one is "
                                 "constant, and it starts at T-one and four V-one, ending at thirty-two V-one — a ratio of "
                                 "one-eighth, raised to the two-thirds. Eight to the two-thirds is four, so T-f is T-one "
                                 "over four.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(2.2, t.duration))
            self.play(Write(s2b), run_time=1.2)
            self.play(Write(s2c), run_time=0.9)
            add_result(r"T_f = \tfrac{T_1}{4}", IGNITION)
            self.wait(max(0.1, t.duration - 4.3))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), FadeOut(s2c), rail.done(1), rail.active(2))

        s3t = Label("STEP 3 — the adiabatic work", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s3a = MathTex(r"W_{\text{adia}} = \frac{nR(T_i - T_f)}{\gamma-1} = \frac{R\left(T_1 - \tfrac{T_1}{4}\right)}{2/3}", color=WHITE).scale(0.54).move_to(WORKC + UP*0.9)
        s3b = MathTex(r"= \tfrac{3}{2}R\cdot \tfrac{3T_1}{4} = \tfrac{9}{8}\,R T_1", color=SIGNAL).scale(0.62).move_to(WORKC + DOWN*0.3)
        with self.voiceover(text="Step three, the adiabatic work. It's n R times the temperature drop, over gamma minus "
                                 "one — R times T-one minus T-one over four, all over two-thirds. That's three-halves R "
                                 "times three T-one over four, which is nine-eighths R T-one.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.2, t.duration))
            self.play(Write(s3b), run_time=1.2)
            add_result(r"W_{\text{adia}} = \tfrac{9}{8}RT_1", SIGNAL)
            self.wait(max(0.1, t.duration - 3.6))
        self.play(FadeOut(s3t), FadeOut(s3a), FadeOut(s3b), rail.done(2), rail.active(3))

        s4t = Label("STEP 4 — the ratio, and f", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s4a = MathTex(r"\frac{W_{\text{iso}}}{W_{\text{adia}}} = \frac{2RT_1\ln 2}{\tfrac{9}{8}RT_1} = \tfrac{16}{9}\ln 2", color=WHITE).scale(0.56).move_to(WORKC + UP*0.7)
        s4b = MathTex(r"= f\ln 2 \ \Rightarrow\ f = \tfrac{16}{9}", color=CORRECT).scale(0.6).move_to(WORKC + DOWN*0.4)
        s4c = MathTex(r"f = \tfrac{16}{9} \approx 1.78", color=CORRECT).scale(0.58).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step four, the ratio. The isothermal work over the adiabatic work is two R T-one log two "
                                 "over nine-eighths R T-one — the R T-ones cancel, leaving sixteen-ninths log two. Matching "
                                 "f log two, f is sixteen over nine, about one point seven eight.") as t:
            self.play(FadeIn(s4t), Write(s4a), run_time=min(2.4, t.duration))
            self.play(Write(s4b), run_time=1.2)
            self.play(Write(s4c), run_time=0.9)
            add_result(r"f = \tfrac{16}{9} \approx 1.78", CORRECT)
            self.wait(max(0.1, t.duration - 4.5))
        self.play(FadeOut(s4t), FadeOut(s4a), FadeOut(s4b), FadeOut(s4c), rail.done(3))

        # ============ 07 · LOCK-IN ============
        ans = Label("ANSWER:   f = 16/9 ≈ 1.78", color=IGNITION).scale(0.8).move_to(WORKC + UP*0.2)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        note = MathTex(r"W_{\text{iso}} = 2RT_1\ln 2,\quad W_{\text{adia}} = \tfrac{9}{8}RT_1", color=SIGNAL).scale(0.5).next_to(ans, DOWN, buff=0.7)
        with self.voiceover(text="So f is sixteen over nine, about one point seven eight — the isothermal work is two R "
                                 "T-one log two, the adiabatic work is nine-eighths R T-one. Solved, completely.") as t:
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9); self.play(Create(box), run_time=0.8)
            self.play(Write(note), run_time=0.9)
            self.wait(max(0.3, t.duration - 2.6))
        self.wait(0.6)
