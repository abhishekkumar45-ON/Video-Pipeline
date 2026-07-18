"""
Orange Nelumbo · DEBRIEF · Thermodynamics · T10 — "Adiabatic expansion, cooling gas"
JEE Advanced 2018 · Paper 2 · Numerical.  Answer: decrease in internal energy = 900 J.
Concept-first + working piston expanding V→8V & steep adiabatic P–V in lockstep with LIVE
V, T readouts + full step-by-step derivation + step rail. No progress counter. Voice af_bella.
4K. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t10(VoiceoverScene):
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
        meta = Mono("JEE ADVANCED 2018 · PAPER 2", color=EMBER).scale(0.32)
        fmt = Mono("NUMERICAL", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)
        q = VGroup(
            Body("One mole of a monatomic ideal gas expands adiabatically", color=WHITE).scale(0.46),
            Body("so its volume becomes 8× the initial value.", color=WHITE).scale(0.46),
            Body("Initial temperature 100 K,  R = 8.0 J·mol⁻¹·K⁻¹.", color=WHITE).scale(0.46),
            Body("Find the DECREASE in internal energy (J).", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.55)
        with self.voiceover(text="A clean numerical. One mole of a monatomic ideal gas expands adiabatically until its "
                                 "volume is eight times larger. It starts at a hundred kelvin, with R equal to eight. "
                                 "Find the decrease in its internal energy.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            for ln in q:
                self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.45, rate_func=smooth)
            self.wait(max(0.2, t.duration - 4.5))
        self.play(FadeOut(head), FadeOut(q))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause, and work out the final temperature yourself first.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — the two ideas, explained", color=WHITE).scale(0.58).to_edge(UP, buff=LOGO_CLEAR)
        def mini(expanded=False, color=IGNITION):
            w, fh, by = 0.55, 0.9, -0.45
            wall = VMobject(stroke_color=TITANIUM, stroke_width=3)
            wall.set_points_as_corners([[-w/2, fh+0.15, 0], [-w/2, by, 0], [w/2, by, 0], [w/2, fh+0.15, 0]])
            h = fh if expanded else fh*0.45
            gas = Rectangle(width=w-0.05, height=h, fill_color=color, fill_opacity=0.30, stroke_width=0).move_to([0, by+h/2, 0])
            pst = Rectangle(width=w+0.1, height=0.1, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([0, by+h+0.05, 0])
            return VGroup(wall, gas, pst)
        def ccard(title, sub, rel, relcol, icon):
            return VGroup(icon.scale(0.9),
                          VGroup(Label(title, color=IGNITION).scale(0.5), Body(sub, color=TITANIUM).scale(0.35),
                                 MathTex(rel, color=relcol).scale(0.58)).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.32)
        c1 = ccard("ADIABATIC", "no heat in, Q = 0", r"T\,V^{\gamma-1}=\text{const}", IGNITION, mini(True, IGNITION))
        c2 = ccard("INTERNAL ENERGY", "monatomic gas", r"\Delta U = nC_V\,\Delta T", SIGNAL, mini(False, SIGNAL))
        cards = VGroup(c1, c2).arrange(RIGHT, buff=1.6).next_to(head3, DOWN, buff=0.7)
        with self.voiceover(text="Before any numbers, two ideas. Adiabatic — no heat enters or leaves, Q is zero, so T "
                                 "times V to the gamma minus one stays constant. As the gas expands, it does work with "
                                 "no heat coming in, so it must cool down.") as t:
            self.play(Write(head3), run_time=0.8); self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="Second — internal energy. For a monatomic gas, the change in U is n times C-v times "
                                 "the temperature change, and C-v is three-halves R. Cool the gas, and its internal "
                                 "energy drops.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"\text{adiabatic} \Rightarrow Q=0,\quad T\,V^{\gamma-1}=\text{const}", color=IGNITION).scale(0.6),
            MathTex(r"C_V=\tfrac{3}{2}R,\quad C_P=\tfrac{5}{2}R \ \Rightarrow\ \gamma=\tfrac{C_P}{C_V}=\tfrac{5}{3}", color=WHITE).scale(0.6),
            MathTex(r"\gamma-1=\tfrac{5}{3}-1=\tfrac{2}{3}", color=SIGNAL).scale(0.6),
            MathTex(r"n=1,\quad T_i=100\,\mathrm{K},\quad V_f=8V_i,\quad R=8.0", color=WHITE).scale(0.6),
        ).arrange(DOWN, buff=0.42).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. Adiabatic means Q is zero and T V to the gamma minus one is "
                                 "constant. For a monatomic gas C-v is three-halves R and C-p is five-halves R, so gamma "
                                 "is five-thirds, and gamma minus one is two-thirds. We have one mole, a hundred kelvin, "
                                 "volume growing eightfold, and R equal to eight.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · WORKING VISUALISATION with LIVE V, T ============
        CX, base_y, full_h, cw = -3.9, -1.8, 2.9, 1.45
        wl, wr, wt = CX-cw/2, CX+cw/2, base_y+full_h
        walls = VMobject(stroke_color=TITANIUM, stroke_width=4)
        walls.set_points_as_corners([[wl, wt+0.5, 0], [wl, base_y, 0], [wr, base_y, 0], [wr, wt+0.5, 0]])
        # volume fraction runs 1/8 (initial) → 1 (final, = 8×), so the piston physically rises.
        def gas_rect(frac, col):
            h=frac*full_h; return Rectangle(width=cw-0.06, height=h, fill_color=col, fill_opacity=0.30, stroke_width=0).move_to([CX, base_y+h/2, 0])
        def piston_g(frac):
            h=frac*full_h
            bar=Rectangle(width=cw+0.14, height=0.13, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([CX, base_y+h+0.06, 0])
            rod=Rectangle(width=0.12, height=0.4, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([CX, base_y+h+0.06+0.27, 0])
            return VGroup(bar, rod)
        gas = gas_rect(1/8, IGNITION); pist = piston_g(1/8)
        cyl_lbl = Mono("piston & cylinder", color=TITANIUM).scale(0.32).next_to(walls, DOWN, buff=0.18)

        vt = ValueTracker(1.0); tt = ValueTracker(100.0)
        def stat(name, tr, unit, col, dec):
            lbl = Mono(name, color=TITANIUM).scale(0.44)
            n = DecimalNumber(tr.get_value(), num_decimal_places=dec, color=col, font_size=38)
            n.add_updater(lambda m, tr=tr: m.set_value(tr.get_value()))
            u = Mono(unit, color=col).scale(0.4)
            return VGroup(lbl, n, u).arrange(RIGHT, buff=0.13), n
        sV, nV = stat("V =", vt, "V₀", SIGNAL, 0)
        sT, nT = stat("T =", tt, "K", IGNITION, 0)
        readout = VGroup(sV, sT).arrange(RIGHT, buff=1.1).to_edge(UP, buff=LOGO_CLEAR)

        Ox, Oy = 2.5, -2.4   # dropped so the P–V diagram clears the lowered live readout
        def PV(vx, py): return np.array([Ox+vx, Oy+py, 0])
        vax = Arrow(PV(0,0), PV(3.6,0), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        pax = Arrow(PV(0,0), PV(0,3.9), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        vlab = Mono("V", color=TITANIUM).scale(0.4).next_to(vax, RIGHT, buff=0.1)
        plab = Mono("P", color=TITANIUM).scale(0.4).next_to(pax, UP, buff=0.1)
        # steep adiabatic: high P at small V (state i), low P at large V (state f)
        I, F = PV(0.5, 3.4), PV(3.2, 0.35)
        dI = Dot(I, color=SIGNAL).scale(0.7); lI = Mono("i", color=SIGNAL).scale(0.42).next_to(dI, UR, buff=0.05)
        moving = Dot(I, color=IGNITION).scale(0.95)

        with self.voiceover(text="Now watch it live. On the left the real piston and cylinder; on the right the P–V "
                                 "diagram; and up top, the volume and temperature changing as we go. We start at i — "
                                 "small volume, high pressure, a hundred kelvin.") as t:
            self.play(Create(walls), FadeIn(gas), FadeIn(pist), FadeIn(cyl_lbl), run_time=1.2)
            self.play(Create(vax), Create(pax), FadeIn(vlab), FadeIn(plab), FadeIn(dI), FadeIn(lI), FadeIn(moving), run_time=1.2)
            self.play(FadeIn(readout, shift=DOWN*0.15), run_time=0.8)
            self.wait(max(0.1, t.duration - 3.2))

        adia = VMobject(color=IGNITION, stroke_width=4); adia.set_points_smoothly([I, PV(1.4, 1.15), F])
        dF = Dot(F, color=IGNITION).scale(0.7); lF = Mono("f", color=IGNITION).scale(0.42).next_to(dF, DR, buff=0.05)
        with self.voiceover(text="Adiabatic expansion — the piston rises until the volume is eight times bigger. Watch "
                                 "the numbers: volume climbs from one to eight, and with no heat coming in the "
                                 "temperature falls all the way from a hundred down to twenty-five kelvin. That's the "
                                 "steep adiabatic curve down to f.") as t:
            self.play(vt.animate.set_value(8.0), tt.animate.set_value(25.0),
                      Transform(gas, gas_rect(1.0, IGNITION)), Transform(pist, piston_g(1.0)),
                      MoveAlongPath(moving, adia), Create(adia), run_time=min(3.4, max(2.0, t.duration-1.6)))
            self.play(FadeIn(dF), FadeIn(lF), run_time=0.5)
            self.wait(max(0.1, t.duration - 4.2))

        for n in (nV, nT):
            n.clear_updaters()
        pv_group = VGroup(vax, pax, vlab, plab, adia, dI, dF, lI, lF, moving)
        self.play(FadeOut(walls), FadeOut(gas), FadeOut(pist), FadeOut(cyl_lbl), FadeOut(readout),
                  pv_group.animate.scale(0.4).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 06 · STEP RAIL + DETAILED SOLVE ============
        rail = StepRail(3, top=1.5, gap=0.86, size=0.56)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        s1t = Label("STEP 1 — the final temperature", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s1a = MathTex(r"T_i V_i^{\gamma-1} = T_f V_f^{\gamma-1}", color=WHITE).scale(0.62).move_to(WORKC + UP*0.95)
        s1b = MathTex(r"T_f = T_i\left(\tfrac{V_i}{8V_i}\right)^{2/3} = \tfrac{100}{8^{2/3}} = \tfrac{100}{4}", color=WHITE).scale(0.55).move_to(WORKC + DOWN*0.1)
        s1c = MathTex(r"= 25\ \mathrm{K}", color=IGNITION).scale(0.66).move_to(WORKC + DOWN*1.2)
        with self.voiceover(text="Step one, the final temperature. T V to the gamma minus one is constant, so T-f is T-i "
                                 "times the volume ratio to the two-thirds. Eight to the two-thirds is four, so T-f is a "
                                 "hundred over four — twenty-five kelvin.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(1.8, t.duration))
            self.play(Write(s1b), run_time=1.3)
            self.play(Write(s1c), run_time=0.9)
            add_result(r"T_f = 25\ \mathrm{K}", IGNITION)
            self.wait(max(0.1, t.duration - 4.0))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), FadeOut(s1c), rail.done(0), rail.active(1))

        s2t = Label("STEP 2 — the change in internal energy", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s2a = MathTex(r"\Delta U = nC_V\,\Delta T = 1\cdot\tfrac{3}{2}R\,(T_f-T_i)", color=WHITE).scale(0.55).move_to(WORKC + UP*0.75)
        s2b = MathTex(r"= \tfrac{3}{2}(8.0)(25-100) = 12\,(-75)", color=WHITE).scale(0.58).move_to(WORKC + DOWN*0.35)
        s2c = MathTex(r"\Delta U = -900\ \mathrm{J}", color=CORRECT).scale(0.66).move_to(WORKC + DOWN*1.45)
        with self.voiceover(text="Step two, the change in internal energy. Delta U is n C-v delta T — one times "
                                 "three-halves R times twenty-five minus a hundred. Three-halves times eight is twelve, "
                                 "times minus seventy-five gives minus nine hundred joules.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(2.0, t.duration))
            self.play(Write(s2b), run_time=1.3)
            self.play(Write(s2c), run_time=0.9)
            add_result(r"\Delta U = -900\ \mathrm{J}", CORRECT)
            self.wait(max(0.1, t.duration - 4.2))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), FadeOut(s2c), rail.done(1), rail.active(2))

        s3t = Label("STEP 3 — decrease in internal energy", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s3a = MathTex(r"\Delta U = -900\,\mathrm{J} < 0 \ \Rightarrow\ U\ \text{decreases}", color=WHITE).scale(0.52).move_to(WORKC + UP*0.5)
        s3b = MathTex(r"\text{The gas does } 900\,\mathrm{J}\ \text{of work adiabatically.}", color=SIGNAL).scale(0.5).move_to(WORKC + DOWN*0.6)
        with self.voiceover(text="Step three. The change is negative, so the internal energy decreases. With no heat in, "
                                 "that lost energy went entirely into work — the gas does nine hundred joules of work as "
                                 "it expands.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.0, t.duration))
            self.play(Write(s3b), run_time=1.3)
            self.wait(max(0.1, t.duration - 3.3))
        self.play(FadeOut(s3t), FadeOut(s3a), FadeOut(s3b), rail.done(2))

        # ============ 07 · LOCK-IN ============
        ans = Label("DECREASE IN U  =  900 J", color=IGNITION).scale(0.8).move_to(WORKC + UP*0.1)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        with self.voiceover(text="So the decrease in internal energy is nine hundred joules. Solved, completely.") as t:
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9); self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.7))
        self.wait(0.6)
