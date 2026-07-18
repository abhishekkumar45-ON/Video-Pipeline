"""
Orange Nelumbo · DEBRIEF · Thermodynamics · t8 — "Adiabatic compression of a gas mixture"
JEE Advanced 2022 · Paper 2 · Multiple correct.  Answer: A, C, D  (B is the trap).
Concept-first + working piston-cylinder & steep P-V curve in lockstep with LIVE V, P, T
readouts + full step-by-step derivation + step rail. No progress counter. Voice af_bella.
4K. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from voice import narration_service

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t8(VoiceoverScene):
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
        meta = Mono("JEE ADVANCED 2022 · PAPER 2", color=EMBER).scale(0.32)
        fmt = Mono("MULTIPLE CORRECT · +4 / −1", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)
        q = VGroup(
            Body("5 mol monatomic gas + 1 mol rigid diatomic gas.", color=WHITE).scale(0.46),
            Body("Start at P₀, V₀, T₀. Adiabatically compressed to V₀/4.", color=WHITE).scale(0.46),
            Body("Given  2^1.2 = 2.3,  2^3.2 = 9.2.  Which are correct?", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.55)
        opts = VGroup(
            Mono("A  |W| in the process is 13 R T₀", color=TITANIUM).scale(0.42),
            Mono("B  avg KE after is between 18 and 19 R T₀", color=TITANIUM).scale(0.42),
            Mono("C  the final pressure is between 9 and 10 P₀", color=TITANIUM).scale(0.42),
            Mono("D  the adiabatic constant of the mixture is 1.6", color=TITANIUM).scale(0.42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(q, DOWN, buff=0.45)
        with self.voiceover(text="Here's a mixture thermodynamics problem. Five moles of a monatomic gas and one mole of "
                                 "a rigid diatomic gas are compressed adiabatically to a quarter of their volume, and we "
                                 "must decide which of four statements are correct.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            for ln in q:
                self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.45, rate_func=smooth)
            for o in opts:
                self.play(FadeIn(o, shift=RIGHT * 0.1), run_time=0.3)
            self.wait(max(0.2, t.duration - 4.6))
        self.play(FadeOut(head), FadeOut(q), FadeOut(opts))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause, and find the mixture's gamma yourself first.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — the ideas we need", color=WHITE).scale(0.58).to_edge(UP, buff=LOGO_CLEAR)
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
        c1 = ccard("MIXTURE C_V", "moles-weighted average", r"C_V=\tfrac{\sum n_i C_{V,i}}{\sum n_i}", SIGNAL, mini(False, SIGNAL))
        c2 = ccard("ADIABATIC", "no heat, Q = 0", r"PV^{\gamma}=\text{const}", IGNITION, mini(True, IGNITION))
        c3 = ccard("WORK (Q=0)", "work equals |ΔU|", r"|W|=nC_V|\Delta T|", EMBER, mini(False, EMBER))
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.05).next_to(head3, DOWN, buff=0.7)
        with self.voiceover(text="Before any numbers, three ideas. First, for a mixture, the heat capacity is the "
                                 "moles-weighted average of each gas's heat capacity.") as t:
            self.play(Write(head3), run_time=0.8); self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="Second, adiabatic — a sudden squeeze, no time for heat to leave, so Q is zero and "
                                 "P V to the gamma is constant.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        with self.voiceover(text="Third, because Q is zero, all the work done goes into internal energy, so the "
                                 "magnitude of the work equals n C-v times the temperature change.") as t:
            self.play(FadeIn(c3, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"\text{monatomic: } C_V=\tfrac{3}{2}R,\qquad \text{rigid diatomic: } C_V=\tfrac{5}{2}R", color=WHITE).scale(0.58),
            MathTex(r"C_P = C_V + R,\qquad \gamma = \tfrac{C_P}{C_V}", color=WHITE).scale(0.58),
            MathTex(r"\text{adiabatic: } TV^{\gamma-1}=\text{const},\quad PV^{\gamma}=\text{const}", color=IGNITION).scale(0.58),
            MathTex(r"2^{1.2}=2.3,\qquad 2^{3.2}=9.2", color=SIGNAL).scale(0.58),
        ).arrange(DOWN, buff=0.42).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. A monatomic gas has C-v three-halves R; a rigid diatomic gas has "
                                 "C-v five-halves R. In general C-p is C-v plus R, and gamma is their ratio. The "
                                 "adiabatic laws relate temperature, pressure and volume, and we're handed two useful "
                                 "powers of two.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · WORKING VISUALISATION with LIVE V, P, T ============
        CX, base_y, full_h, cw = -3.9, -1.8, 2.9, 1.45
        wl, wr, wt = CX-cw/2, CX+cw/2, base_y+full_h
        walls = VMobject(stroke_color=TITANIUM, stroke_width=4)
        walls.set_points_as_corners([[wl, wt+0.5, 0], [wl, base_y, 0], [wr, base_y, 0], [wr, wt+0.5, 0]])
        def gas_rect(vol, col):
            h=vol*full_h; return Rectangle(width=cw-0.06, height=h, fill_color=col, fill_opacity=0.30, stroke_width=0).move_to([CX, base_y+h/2, 0])
        def piston_g(vol):
            h=vol*full_h
            bar=Rectangle(width=cw+0.14, height=0.13, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([CX, base_y+h+0.06, 0])
            rod=Rectangle(width=0.12, height=0.4, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([CX, base_y+h+0.06+0.27, 0])
            return VGroup(bar, rod)
        gas = gas_rect(1.0, IGNITION); pist = piston_g(1.0)
        cyl_lbl = Mono("piston & cylinder", color=TITANIUM).scale(0.32).next_to(walls, DOWN, buff=0.18)

        vt = ValueTracker(1.0); pt_ = ValueTracker(1.0); tt = ValueTracker(1.0)
        def stat(name, tr, unit, col, dec):
            lbl = Mono(name, color=TITANIUM).scale(0.44)
            n = DecimalNumber(tr.get_value(), num_decimal_places=dec, color=col, font_size=38)
            n.add_updater(lambda m, tr=tr: m.set_value(tr.get_value()))
            u = Mono(unit, color=col).scale(0.4)
            return VGroup(lbl, n, u).arrange(RIGHT, buff=0.13), n
        sV, nV = stat("V =", vt, "V₀", SIGNAL, 2)
        sP, nP = stat("P =", pt_, "P₀", EMBER, 1)
        sT, nT = stat("T =", tt, "T₀", IGNITION, 1)
        readout = VGroup(sV, sP, sT).arrange(RIGHT, buff=0.7).to_edge(UP, buff=LOGO_CLEAR)

        Ox, Oy = 2.5, -2.4   # dropped so the P–V diagram clears the lowered live readout
        def PV(vx, py): return np.array([Ox+vx, Oy+py, 0])
        vax = Arrow(PV(0,0), PV(3.3,0), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        pax = Arrow(PV(0,0), PV(0,3.9), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        vlab = Mono("V", color=TITANIUM).scale(0.4).next_to(vax, RIGHT, buff=0.1)
        plab = Mono("P", color=TITANIUM).scale(0.4).next_to(pax, UP, buff=0.1)
        # initial state (full V, low P) → final state (quarter V, high P): a steep adiabatic
        I, Fp = PV(2.9, 0.35), PV(0.75, 3.5)
        dI = Dot(I, color=SIGNAL).scale(0.7); lI = Mono("i", color=SIGNAL).scale(0.42).next_to(dI, UR, buff=0.05)
        moving = Dot(I, color=IGNITION).scale(0.95)

        with self.voiceover(text="Now watch it live. On the left the real piston and cylinder; on the right a P–V "
                                 "diagram; and up top, the volume, pressure and temperature in units of the starting "
                                 "values. We start at the initial state — full volume, pressure P-nought, temperature "
                                 "T-nought.") as t:
            self.play(Create(walls), FadeIn(gas), FadeIn(pist), FadeIn(cyl_lbl), run_time=1.2)
            self.play(Create(vax), Create(pax), FadeIn(vlab), FadeIn(plab), FadeIn(dI), FadeIn(lI), FadeIn(moving), run_time=1.2)
            self.play(FadeIn(readout, shift=DOWN*0.15), run_time=0.8)
            self.wait(max(0.1, t.duration - 3.2))

        adia = VMobject(color=IGNITION, stroke_width=4); adia.set_points_smoothly([I, PV(1.55, 1.35), Fp])
        dF = Dot(Fp, color=IGNITION).scale(0.7); lF = Mono("f", color=IGNITION).scale(0.42).next_to(dF, UP, buff=0.1)
        with self.voiceover(text="Adiabatic compression to a quarter of the volume. Watch the numbers: volume falls to "
                                 "zero point two five, temperature rises to two point three, and pressure jumps all the "
                                 "way to nine point two. That's the steep adiabatic climb to the final state.") as t:
            self.play(vt.animate.set_value(0.25), tt.animate.set_value(2.3), pt_.animate.set_value(9.2),
                      Transform(gas, gas_rect(0.25, IGNITION)), Transform(pist, piston_g(0.25)),
                      MoveAlongPath(moving, adia), Create(adia), run_time=min(3.4, max(2.0, t.duration-1.4)))
            self.play(FadeIn(dF), FadeIn(lF), run_time=0.5)
            self.wait(max(0.1, t.duration - 4.0))

        for n in (nV, nP, nT):
            n.clear_updaters()
        pv_group = VGroup(vax, pax, vlab, plab, adia, dI, dF, lI, lF, moving)
        self.play(FadeOut(walls), FadeOut(gas), FadeOut(pist), FadeOut(cyl_lbl), FadeOut(readout),
                  pv_group.animate.scale(0.4).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 06 · STEP RAIL + DETAILED SOLVE ============
        rail = StepRail(5, top=1.5, gap=0.86, size=0.56)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        s1t = Label("STEP 1 — mixture heat capacities", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s1a = MathTex(r"C_V = \frac{5\cdot\tfrac{3}{2}R + 1\cdot\tfrac{5}{2}R}{6} = \frac{\tfrac{15}{2}+\tfrac{5}{2}}{6}R", color=WHITE).scale(0.55).move_to(WORKC + UP*0.9)
        s1b = MathTex(r"C_V = \tfrac{5R}{3}, \qquad C_P = C_V + R = \tfrac{8R}{3}", color=WHITE).scale(0.6).move_to(WORKC + DOWN*0.4)
        with self.voiceover(text="Step one. The mixture's C-v is the moles-weighted average: five moles at three-halves "
                                 "R plus one mole at five-halves R, all over six moles. That gives five R over three. "
                                 "Adding R, C-p is eight R over three.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(2.2, t.duration))
            self.play(Write(s1b), run_time=1.2)
            add_result(r"C_V=\tfrac{5R}{3},\ C_P=\tfrac{8R}{3}", SIGNAL)
            self.wait(max(0.1, t.duration - 3.6))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), rail.done(0), rail.active(1))

        s2t = Label("STEP 2 — the adiabatic constant (D)", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s2a = MathTex(r"\gamma = \frac{C_P}{C_V} = \frac{8/3}{5/3} = \frac{8}{5} = 1.6", color=WHITE).scale(0.6).move_to(WORKC + UP*0.7)
        s2b = MathTex(r"\gamma - 1 = 0.6", color=SIGNAL).scale(0.6).move_to(WORKC + DOWN*0.4)
        s2c = MathTex(r"\Rightarrow\ \text{(D) is correct}", color=CORRECT).scale(0.6).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step two. Gamma is C-p over C-v — eight-thirds over five-thirds, which is eight-fifths, "
                                 "exactly one point six. So gamma minus one is zero point six, and option D is correct.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(2.2, t.duration))
            self.play(Write(s2b), run_time=1.0)
            self.play(Write(s2c), run_time=0.8)
            add_result(r"\gamma = 1.6", CORRECT)
            self.wait(max(0.1, t.duration - 4.0))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), FadeOut(s2c), rail.done(1), rail.active(2))

        s3t = Label("STEP 3 — final temperature", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s3a = MathTex(r"T_0 V_0^{\gamma-1} = T_f\left(\tfrac{V_0}{4}\right)^{\gamma-1}", color=WHITE).scale(0.58).move_to(WORKC + UP*0.9)
        s3b = MathTex(r"T_f = T_0\cdot 4^{0.6} = T_0\cdot 2^{1.2} = 2.3\,T_0", color=IGNITION).scale(0.6).move_to(WORKC + DOWN*0.4)
        with self.voiceover(text="Step three, the final temperature. T V to the gamma minus one is constant, so T-f is "
                                 "T-nought times four to the zero point six. Four to the zero point six is two to the one "
                                 "point two, which we're told is two point three. So T-f is two point three T-nought.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.2, t.duration))
            self.play(Write(s3b), run_time=1.2)
            add_result(r"T_f = 2.3\,T_0", IGNITION)
            self.wait(max(0.1, t.duration - 3.6))
        self.play(FadeOut(s3t), FadeOut(s3a), FadeOut(s3b), rail.done(2), rail.active(3))

        s4t = Label("STEP 4 — the final pressure (C)", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s4a = MathTex(r"P_0 V_0^{\gamma} = P_f\left(\tfrac{V_0}{4}\right)^{\gamma}", color=WHITE).scale(0.58).move_to(WORKC + UP*0.9)
        s4b = MathTex(r"P_f = P_0\cdot 4^{1.6} = P_0\cdot 2^{3.2} = 9.2\,P_0", color=WHITE).scale(0.58).move_to(WORKC + DOWN*0.4)
        s4c = MathTex(r"9 P_0 < 9.2\,P_0 < 10 P_0 \ \Rightarrow\ \text{(C) is correct}", color=CORRECT).scale(0.52).move_to(WORKC + DOWN*1.5)
        with self.voiceover(text="Step four, the pressure. P V to the gamma is constant, so P-f is P-nought times four to "
                                 "the one point six — that's two to the three point two, which is nine point two. Nine "
                                 "point two P-nought lies between nine and ten, so option C is correct.") as t:
            self.play(FadeIn(s4t), Write(s4a), run_time=min(2.2, t.duration))
            self.play(Write(s4b), run_time=1.2)
            self.play(Write(s4c), run_time=0.9)
            add_result(r"P_f = 9.2\,P_0", CORRECT)
            self.wait(max(0.1, t.duration - 4.3))
        self.play(FadeOut(s4t), FadeOut(s4a), FadeOut(s4b), FadeOut(s4c), rail.done(3), rail.active(4))

        s5t = Label("STEP 5 — the work, and the trap (A, B)", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s5a = MathTex(r"|W| = |\Delta U| = nC_V|\Delta T| = 6\cdot\tfrac{5R}{3}(2.3T_0 - T_0)", color=WHITE).scale(0.5).move_to(WORKC + UP*0.9)
        s5b = MathTex(r"= 10R\cdot 1.3\,T_0 = 13\,R T_0 \ \Rightarrow\ \text{(A) is correct}", color=CORRECT).scale(0.52).move_to(WORKC + DOWN*0.3)
        s5c = MathTex(r"\text{but } \Delta U = 13\,R T_0 \notin (18,19)R T_0 \ \Rightarrow\ \text{(B) is false}", color=ERROR).scale(0.5).move_to(WORKC + DOWN*1.5)
        with self.voiceover(text="Step five, the work. Since Q is zero, the magnitude of the work equals the internal "
                                 "energy change: n C-v times delta T — six moles times five R over three times the one "
                                 "point three T-nought rise. That's ten R times one point three, thirteen R T-nought, so "
                                 "option A is correct. But that same energy is thirteen R T-nought, which is not between "
                                 "eighteen and nineteen, so option B is the trap — false.") as t:
            self.play(FadeIn(s5t), Write(s5a), run_time=min(2.4, t.duration))
            self.play(Write(s5b), run_time=1.2)
            self.play(Write(s5c), run_time=1.0)
            add_result(r"|W| = 13\,R T_0", CORRECT)
            self.wait(max(0.1, t.duration - 4.6))
        self.play(FadeOut(s5t), FadeOut(s5a), FadeOut(s5b), FadeOut(s5c), rail.done(4))

        # ============ 07 · LOCK-IN ============
        ans = Label("ANSWER:   A ,  C ,  D", color=IGNITION).scale(0.8).move_to(WORKC + UP*0.2)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        trap = MathTex(r"\text{(B) is the trap} \ \times", color=ERROR).scale(0.55).next_to(ans, DOWN, buff=0.7)
        with self.voiceover(text="So the answer is A, C, and D — the work is thirteen R T-nought, the pressure is nine "
                                 "point two P-nought, and gamma is one point six. Option B is the trap. Solved, "
                                 "completely.") as t:
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9); self.play(Create(box), run_time=0.8)
            self.play(Write(trap), run_time=0.9)
            self.wait(max(0.3, t.duration - 2.6))
        self.wait(0.6)
