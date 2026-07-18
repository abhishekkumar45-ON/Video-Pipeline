"""
Orange Nelumbo · DEBRIEF · Thermodynamics · t6 — "Adiabatic vs isothermal to the same state"
JEE Advanced 2023 · Paper 1 · Single correct.  Answer: (A) T_A/T_B = 5^(gamma-1).
Concept-first (isothermal keeps T fixed; adiabatic obeys T V^(gamma-1)=const) + one P-V plane
with both branches V0 -> 5V0 and a live V readout + full step-by-step derivation + step rail.
No progress counter. Voice af_bella. 4K. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t6(VoiceoverScene):
    def construct(self):
        background(self)
        self.set_speech_service(KokoroService(voice="af_bella"))

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
        meta = Mono("JEE ADVANCED 2023 · PAPER 1", color=EMBER).scale(0.32)
        fmt = Mono("SINGLE CORRECT", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)
        q = VGroup(
            Body("One mole expands ADIABATICALLY from (T_A, V0) to (T_f, 5V0).", color=WHITE).scale(0.46),
            Body("Another mole of the same gas expands ISOTHERMALLY from", color=WHITE).scale(0.46),
            Body("(T_B, V0) to the same final state (T_f, 5V0).", color=WHITE).scale(0.46),
            Body("With γ = C_P / C_V, find the ratio T_A / T_B.", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).next_to(head, DOWN, buff=0.55)
        opts = VGroup(
            Mono("A   5^(γ−1)", color=TITANIUM).scale(0.44),
            Mono("B   5^(1−γ)", color=TITANIUM).scale(0.44),
            Mono("C   5^(γ)", color=TITANIUM).scale(0.44),
            Mono("D   5^(1+γ)", color=TITANIUM).scale(0.44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(q, DOWN, buff=0.45)
        with self.voiceover(text="Here's a clean thermodynamics problem. One mole of gas expands adiabatically from "
                                 "volume V-nought to five V-nought. A second mole of the same gas expands isothermally "
                                 "to the very same final state. Given gamma, we must find the ratio of their starting "
                                 "temperatures, T-A over T-B.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            for ln in q:
                self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.45, rate_func=smooth)
            for o in opts:
                self.play(FadeIn(o, shift=RIGHT * 0.1), run_time=0.3)
            self.wait(max(0.2, t.duration - 5.0))
        self.play(FadeOut(head), FadeOut(q), FadeOut(opts))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause, and think about what each process fixes before you compute.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — the two processes, explained", color=WHITE).scale(0.58).to_edge(UP, buff=LOGO_CLEAR)
        def ccard(title, sub, rel, relcol, icol):
            chip = Rectangle(width=0.9, height=0.9, fill_color=icol, fill_opacity=0.28, stroke_color=icol, stroke_width=3)
            return VGroup(chip,
                          VGroup(Label(title, color=IGNITION).scale(0.5), Body(sub, color=TITANIUM).scale(0.33),
                                 MathTex(rel, color=relcol).scale(0.55)).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.32)
        c1 = ccard("ISOTHERMAL", "temperature held fixed", r"T = \text{const}", EMBER, EMBER)
        c2 = ccard("ADIABATIC", "no heat, Q = 0", r"T\,V^{\gamma-1} = \text{const}", IGNITION, IGNITION)
        cards = VGroup(c1, c2).arrange(RIGHT, buff=1.6).next_to(head3, DOWN, buff=0.8)
        with self.voiceover(text="Before any algebra, two ideas. Isothermal means the temperature is held fixed the whole "
                                 "way — so the start and end temperatures are equal.") as t:
            self.play(Write(head3), run_time=0.8); self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="Adiabatic means no heat crosses, Q is zero — and there the combination T times V to the "
                                 "gamma minus one stays constant. That single relation carries all the work.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"\text{both end at the same state } (T_f,\ 5V_0)", color=SIGNAL).scale(0.6),
            MathTex(r"\text{isothermal} \ \Rightarrow\ T = \text{const along the path}", color=EMBER).scale(0.6),
            MathTex(r"\text{adiabatic} \ \Rightarrow\ T\,V^{\gamma-1} = \text{const}", color=IGNITION).scale(0.6),
            MathTex(r"V_0 \ \longrightarrow\ 5V_0,\qquad \gamma = \tfrac{C_P}{C_V}", color=WHITE).scale(0.6),
        ).arrange(DOWN, buff=0.42).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. Both gases finish at the identical state — final temperature T-f at "
                                 "five V-nought. The isothermal path keeps temperature constant. The adiabatic path obeys "
                                 "T times V to the gamma minus one equals a constant. Both start at V-nought and expand to "
                                 "five times that.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · LIVE VISUAL — one P-V plane, both branches ============
        head5 = Label("Both expansions on one P–V plane", color=WHITE).scale(0.52).to_edge(UP, buff=LOGO_CLEAR)
        Ox, Oy = -3.4, -2.2
        def PV(vx, py): return np.array([Ox + vx, Oy + py, 0])
        vax = Arrow(PV(0, 0), PV(5.6, 0), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        pax = Arrow(PV(0, 0), PV(0, 4.2), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        vlab = Mono("V", color=TITANIUM).scale(0.4).next_to(vax, RIGHT, buff=0.1)
        plab = Mono("P", color=TITANIUM).scale(0.4).next_to(pax, UP, buff=0.1)
        # start volume V0 and final 5V0 tick positions on the V axis
        vx0, vx5 = 0.9, 4.9
        START = PV(vx0, 3.5)        # common start volume V0 (top-left, high P)
        ENDI = PV(vx5, 0.95)       # isothermal end (gentler, higher P at 5V0)
        ENDA = PV(vx5, 0.45)       # adiabatic end (steeper, lower P at 5V0)
        tick0 = Line(PV(vx0, -0.12), PV(vx0, 0.12), color=TITANIUM, stroke_width=3)
        tick5 = Line(PV(vx5, -0.12), PV(vx5, 0.12), color=TITANIUM, stroke_width=3)
        v0lab = MathTex(r"V_0", color=TITANIUM).scale(0.5).next_to(tick0, DOWN, buff=0.12)
        v5lab = MathTex(r"5V_0", color=TITANIUM).scale(0.5).next_to(tick5, DOWN, buff=0.12)

        dS = Dot(START, color=SIGNAL).scale(0.8)
        lS = Mono("start", color=SIGNAL).scale(0.36).next_to(dS, UP, buff=0.1)

        # live V readout
        vt = ValueTracker(1.0)
        vlbl = Mono("V =", color=TITANIUM).scale(0.44)
        vnum = DecimalNumber(1.0, num_decimal_places=1, color=IGNITION, font_size=38)
        vnum.add_updater(lambda m: m.set_value(vt.get_value()))
        vunit = Mono("V₀", color=IGNITION).scale(0.4)
        readout = VGroup(vlbl, vnum, vunit).arrange(RIGHT, buff=0.13).to_edge(UP, buff=LOGO_CLEAR)

        with self.voiceover(text="Here is one P–V plane. Both gases begin at the same start point — volume V-nought, up at "
                                 "high pressure — and both expand out to five V-nought. Watch the volume up top climb from "
                                 "one to five as they go.") as t:
            self.play(Write(head5), run_time=0.7)
            self.play(Create(vax), Create(pax), FadeIn(vlab), FadeIn(plab), run_time=1.0)
            self.play(FadeIn(tick0), FadeIn(tick5), Write(v0lab), Write(v5lab), run_time=0.8)
            self.play(FadeOut(head5), FadeIn(dS), FadeIn(lS), FadeIn(readout, shift=DOWN*0.15), run_time=0.7)
            self.wait(max(0.1, t.duration - 3.2))

        iso = VMobject(color=EMBER, stroke_width=4)
        iso.set_points_smoothly([START, PV(2.6, 1.9), PV(3.8, 1.25), ENDI])
        moving = Dot(START, color=EMBER).scale(0.95)
        dI = Dot(ENDI, color=EMBER).scale(0.8)
        lI = Mono("isothermal", color=EMBER).scale(0.36).next_to(dI, RIGHT, buff=0.12)
        with self.voiceover(text="The isothermal branch, in amber, is the gentler curve. Temperature never changes along "
                                 "it, so its endpoints share one temperature.") as t:
            self.play(vt.animate.set_value(5.0), MoveAlongPath(moving, iso), Create(iso),
                      run_time=min(3.0, max(1.6, t.duration - 1.2)))
            self.play(FadeIn(dI), FadeIn(lI), run_time=0.5)
            self.wait(max(0.1, t.duration - 3.0))

        adia = VMobject(color=IGNITION, stroke_width=4)
        adia.set_points_smoothly([START, PV(2.3, 1.25), PV(3.6, 0.7), ENDA])
        moving2 = Dot(START, color=IGNITION).scale(0.95)
        dA = Dot(ENDA, color=IGNITION).scale(0.8)
        lA = Mono("adiabatic", color=IGNITION).scale(0.36).next_to(dA, DR, buff=0.08)
        with self.voiceover(text="The adiabatic branch, in orange, drops off steeper because no heat comes in to prop up "
                                 "the pressure — so the gas cools as it expands. Same start, same final volume, but it "
                                 "lands lower.") as t:
            vt.set_value(1.0)
            self.play(vt.animate.set_value(5.0), MoveAlongPath(moving2, adia), Create(adia),
                      run_time=min(3.0, max(1.6, t.duration - 1.2)))
            self.play(FadeIn(dA), FadeIn(lA), run_time=0.5)
            self.wait(max(0.1, t.duration - 3.0))

        vnum.clear_updaters()
        pv_group = VGroup(vax, pax, vlab, plab, tick0, tick5, v0lab, v5lab,
                          dS, lS, iso, adia, moving, moving2, dI, dA, lI, lA)
        self.play(FadeOut(readout),
                  pv_group.animate.scale(0.4).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 06 · STEP RAIL + DETAILED SOLVE ============
        rail = StepRail(3, top=1.5, gap=1.05, size=0.62)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        s1t = Label("STEP 1 — the isothermal branch", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s1a = MathTex(r"\text{isothermal}: \ T = \text{const along the path}", color=WHITE).scale(0.55).move_to(WORKC + UP*0.85)
        s1b = MathTex(r"\text{start } T_B \ \longrightarrow\ \text{end } T_f,\quad T_B = T_f", color=WHITE).scale(0.55).move_to(WORKC + DOWN*0.35)
        s1c = MathTex(r"\Rightarrow\ T_B = T_f", color=EMBER).scale(0.66).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step one, the isothermal branch. Law: temperature is constant the whole way. "
                                 "Substitution: the start temperature T-B and the end temperature T-f are the same point "
                                 "on that constant. Result: T-B simply equals T-f.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(2.0, t.duration))
            self.play(Write(s1b), run_time=1.3)
            self.play(Write(s1c), run_time=0.9)
            add_result(r"T_B = T_f", EMBER)
            self.wait(max(0.1, t.duration - 4.2))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), FadeOut(s1c), rail.done(0), rail.active(1))

        s2t = Label("STEP 2 — the adiabatic branch", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s2a = MathTex(r"\text{adiabatic}: \ T\,V^{\gamma-1} = \text{const}", color=WHITE).scale(0.55).move_to(WORKC + UP*0.85)
        s2b = MathTex(r"T_A\,V_0^{\gamma-1} = T_f\,(5V_0)^{\gamma-1}", color=WHITE).scale(0.55).move_to(WORKC + DOWN*0.35)
        s2c = MathTex(r"\Rightarrow\ T_A = T_f\,\cdot 5^{\gamma-1}", color=IGNITION).scale(0.64).move_to(WORKC + DOWN*1.45)
        with self.voiceover(text="Step two, the adiabatic branch. Law: T times V to the gamma minus one is constant. "
                                 "Substitution: T-A times V-nought to the gamma minus one equals T-f times five V-nought "
                                 "to the same power. The V-nought pieces cancel, leaving five to the gamma minus one. "
                                 "Result: T-A equals T-f times five to the gamma minus one.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(2.0, t.duration))
            self.play(Write(s2b), run_time=1.3)
            self.play(Write(s2c), run_time=0.9)
            add_result(r"T_A = T_f\,5^{\gamma-1}", IGNITION)
            self.wait(max(0.1, t.duration - 4.2))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), FadeOut(s2c), rail.done(1), rail.active(2))

        s3t = Label("STEP 3 — the ratio", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s3a = MathTex(r"\frac{T_A}{T_B} = \frac{T_f\,\cdot 5^{\gamma-1}}{T_f}", color=WHITE).scale(0.6).move_to(WORKC + UP*0.7)
        s3b = MathTex(r"\Rightarrow\ \frac{T_A}{T_B} = 5^{\gamma-1}", color=CORRECT).scale(0.66).move_to(WORKC + DOWN*0.55)
        s3c = MathTex(r"\Rightarrow\ \text{option (A)}", color=CORRECT).scale(0.55).move_to(WORKC + DOWN*1.6)
        with self.voiceover(text="Step three, the ratio. Divide T-A by T-B. The T-f in the numerator cancels the T-f in "
                                 "the denominator, and what remains is five to the gamma minus one. That is option A.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.0, t.duration))
            self.play(Write(s3b), run_time=1.1)
            self.play(Write(s3c), run_time=0.8)
            add_result(r"\frac{T_A}{T_B} = 5^{\gamma-1}", CORRECT)
            self.wait(max(0.1, t.duration - 4.0))
        self.play(FadeOut(s3t), FadeOut(s3a), FadeOut(s3b), FadeOut(s3c), rail.done(2))

        # ============ 07 · OPTIONS + ANSWER LOCK-IN ============
        oA = MathTex(r"\text{(A)}\ \ 5^{\gamma-1}\ \ \checkmark", color=CORRECT).scale(0.6)
        oB = MathTex(r"\text{(B)}\ \ 5^{1-\gamma}\ \ \times", color=ERROR).scale(0.6)
        oC = MathTex(r"\text{(C)}\ \ 5^{\gamma}\ \ \times", color=ERROR).scale(0.6)
        oD = MathTex(r"\text{(D)}\ \ 5^{1+\gamma}\ \ \times", color=ERROR).scale(0.6)
        optcol = VGroup(oA, oB, oC, oD).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(WORKC + UP*0.55)
        with self.voiceover(text="Check the four options. A, five to the gamma minus one, is correct. B flips the sign of "
                                 "the exponent, C drops the minus one, and D adds one instead — all wrong.") as t:
            self.play(Write(oA), run_time=0.7)
            self.play(Write(oB), Write(oC), Write(oD), run_time=1.4)
            self.wait(max(0.1, t.duration - 2.1))

        ans = Label("ANSWER:   (A)   5^(γ−1)", color=IGNITION).scale(0.8).move_to(WORKC + DOWN*1.7)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        with self.voiceover(text="So the ratio T-A over T-B is five to the gamma minus one — option A. The isothermal branch "
                                 "pins T-B to T-f, and one adiabatic relation does the rest. Solved, completely.") as t:
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9); self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.7))
        self.wait(0.6)
