"""
Orange Nelumbo · DEBRIEF · Thermodynamics · t1 — "Adiabatic + isobaric cycle on a V–T diagram"
JEE Advanced 2025 · Paper 2 · Numerical.  Answer: Q_XY = 1.6 J.
Concept-first + live V–T diagram with a moving state point and LIVE T readout +
full step-by-step derivation + step rail. No progress counter. Voice af_bella. 4K. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t1(VoiceoverScene):
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
        meta = Mono("JEE ADVANCED 2025 · PAPER 2", color=EMBER).scale(0.32)
        fmt = Mono("NUMERICAL", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)
        q = VGroup(
            Body("n moles of an ideal monatomic gas run a cycle W→X→Y→Z→W", color=WHITE).scale(0.46),
            Body("of adiabatic and isobaric steps, on a V–T diagram.", color=WHITE).scale(0.46),
            Body("Volumes at W, X, Y are 64, 125, 250 cm³.  Given nRT_W = 1 J.", color=WHITE).scale(0.46),
            Body("Find the heat absorbed (in J) along the path X→Y.", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.55)
        with self.voiceover(text="Here's a clean thermodynamics problem. A monatomic gas runs a cycle of alternating "
                                 "adiabatic and isobaric steps on a volume–temperature diagram. The volumes at W, X and Y "
                                 "are sixty-four, one twenty-five and two hundred fifty cubic centimetres, and n R T-W "
                                 "equals one joule. We must find the heat absorbed along the path X to Y.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            for ln in q:
                self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.45, rate_func=smooth)
            self.wait(max(0.2, t.duration - 2.5))
        self.play(FadeOut(head), FadeOut(q))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause, and try the two steps — the adiabatic and the isobaric — yourself first.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — the two moves, explained", color=WHITE).scale(0.58).to_edge(UP, buff=LOGO_CLEAR)
        def mini(color=IGNITION, slope=False):
            ax = VGroup(
                Arrow([-0.55, -0.45, 0], [-0.55, 0.75, 0], color=TITANIUM, stroke_width=3, buff=0, tip_length=0.12),
                Arrow([-0.55, -0.45, 0], [0.7, -0.45, 0], color=TITANIUM, stroke_width=3, buff=0, tip_length=0.12),
            )
            if slope:
                curve = Line([-0.35, -0.3, 0], [0.55, 0.6, 0], color=color, stroke_width=4)
            else:
                curve = VMobject(color=color, stroke_width=4)
                curve.set_points_smoothly([[-0.35, 0.55, 0], [0.05, 0.0, 0], [0.55, -0.28, 0]])
            return VGroup(ax, curve)
        def ccard(title, sub, rel, relcol, icon):
            return VGroup(icon,
                          VGroup(Label(title, color=IGNITION).scale(0.5), Body(sub, color=TITANIUM).scale(0.35),
                                 MathTex(rel, color=relcol).scale(0.58)).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.32)
        c1 = ccard("ADIABATIC", "no heat, Q = 0", r"T\,V^{\gamma-1}=\text{const}", IGNITION, mini(IGNITION, slope=False))
        c2 = ccard("ISOBARIC", "constant P → V ∝ T", r"\tfrac{V}{T}=\text{const}", SIGNAL, mini(SIGNAL, slope=True))
        c3 = ccard("ISOBARIC HEAT", "monatomic gas", r"Q=nC_P\,\Delta T", EMBER, mini(EMBER, slope=True))
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.05).next_to(head3, DOWN, buff=0.7)
        with self.voiceover(text="Before any numbers, understand the two moves. Adiabatic — no heat crosses the wall, so "
                                 "Q is zero and T times V to the gamma minus one stays constant.") as t:
            self.play(Write(head3), run_time=0.8); self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="Isobaric — the pressure is fixed, so volume is proportional to temperature. On a V–T "
                                 "diagram that's a straight ray through the origin.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        with self.voiceover(text="And the heat at constant pressure is n C-p delta T, where C-p is five-halves R for a "
                                 "monatomic gas.") as t:
            self.play(FadeIn(c3, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"\text{monatomic}\ \Rightarrow\ \gamma=\tfrac{5}{3},\quad \gamma-1=\tfrac{2}{3}", color=WHITE).scale(0.6),
            MathTex(r"C_V=\tfrac{3}{2}R,\qquad C_P=\tfrac{5}{2}R", color=WHITE).scale(0.6),
            MathTex(r"V_W=64,\quad V_X=125,\quad V_Y=250\ (\mathrm{cm^3})", color=SIGNAL).scale(0.6),
            MathTex(r"nRT_W = 1\ \mathrm{J}", color=SIGNAL).scale(0.6),
        ).arrange(DOWN, buff=0.42).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. The gas is monatomic, so gamma is five-thirds and gamma minus one is "
                                 "two-thirds. C-v is three-halves R and C-p is five-halves R. The volumes are sixty-four, "
                                 "one twenty-five and two hundred fifty, and n R T-W is one joule.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · WORKING VISUALISATION with LIVE T ============
        # V–T diagram: T horizontal, V vertical. Isobaric X→Y is a ray through the origin (V ∝ T).
        Ox, Oy = -5.1, -2.2
        ST, SV = 2.9, 0.010   # T-axis scale (per T_W unit), V-axis scale (per cm^3)
        def VT(tw, vol): return np.array([Ox + tw * ST, Oy + vol * SV, 0])

        tax = Arrow(VT(0, 0), VT(1.75, 0), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        vax = Arrow(VT(0, 0), VT(0, 320), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        tlab = Mono("T", color=TITANIUM).scale(0.4).next_to(tax, RIGHT, buff=0.1)
        vlab = Mono("V", color=TITANIUM).scale(0.4).next_to(vax, UP, buff=0.1)

        TW, TX, TY = 1.0, 16/25, 32/25   # temperatures in units of T_W
        Wpt = VT(TW, 64); Xpt = VT(TX, 125); Ypt = VT(TY, 250)
        dW = Dot(Wpt, color=EMBER).scale(0.7); lW = Mono("W", color=EMBER).scale(0.4).next_to(dW, DR, buff=0.05)
        dX = Dot(Xpt, color=IGNITION).scale(0.7); lX = Mono("X", color=IGNITION).scale(0.4).next_to(dX, UL, buff=0.05)
        dY = Dot(Ypt, color=SIGNAL).scale(0.7); lY = Mono("Y", color=SIGNAL).scale(0.4).next_to(dY, UR, buff=0.05)
        moving = Dot(Wpt, color=IGNITION).scale(0.95)

        # live T readout (in units of T_W)
        tt = ValueTracker(TW)
        tlbl = Mono("T =", color=TITANIUM).scale(0.44)
        tnum = DecimalNumber(tt.get_value(), num_decimal_places=2, color=IGNITION, font_size=38)
        tnum.add_updater(lambda m: m.set_value(tt.get_value()))
        tunit = Mono("T_W", color=IGNITION).scale(0.4)
        readout = VGroup(tlbl, tnum, tunit).arrange(RIGHT, buff=0.13).to_edge(UP, buff=LOGO_CLEAR)

        with self.voiceover(text="Now watch it live. On this volume–temperature diagram T runs across and V runs up. We "
                                 "start at W — volume sixty-four — and the live readout shows the temperature in units of "
                                 "T-W as the state moves.") as t:
            self.play(Create(tax), Create(vax), FadeIn(tlab), FadeIn(vlab), run_time=1.0)
            self.play(FadeIn(dW), FadeIn(lW), FadeIn(moving), FadeIn(readout, shift=DOWN*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration - 2.0))

        adia = VMobject(color=IGNITION, stroke_width=4)
        adia.set_points_smoothly([Wpt, VT((TW+TX)/2 - 0.03, (64+125)/2 + 6), Xpt])
        with self.voiceover(text="First, the adiabatic step W to X. As it compresses to one twenty-five, the temperature "
                                 "drops to zero point six four T-W. That's the curved adiabatic arc to X.") as t:
            self.play(tt.animate.set_value(TX), MoveAlongPath(moving, adia), Create(adia),
                      run_time=min(3.0, max(1.6, t.duration - 1.2)))
            self.play(FadeIn(dX), FadeIn(lX), run_time=0.5)
            self.wait(max(0.1, t.duration - 3.5))

        iso = Line(Xpt, Ypt, color=SIGNAL, stroke_width=4)
        ray = DashedLine(VT(0, 0), Ypt, color=TITANIUM, stroke_width=2).set_opacity(0.35)
        with self.voiceover(text="Then the isobaric step X to Y. Pressure is fixed, so V over T is constant — a straight "
                                 "ray through the origin. The volume doubles to two hundred fifty, and the temperature "
                                 "climbs to one point two eight T-W.") as t:
            self.play(FadeIn(ray), run_time=0.4)
            self.play(tt.animate.set_value(TY), MoveAlongPath(moving, iso), Create(iso),
                      run_time=min(3.0, max(1.6, t.duration - 1.6)))
            self.play(FadeIn(dY), FadeIn(lY), run_time=0.5)
            self.wait(max(0.1, t.duration - 3.5))

        tnum.clear_updaters()
        vt_group = VGroup(tax, vax, tlab, vlab, adia, iso, ray, dW, dX, dY, lW, lX, lY, moving)
        self.play(FadeOut(readout), vt_group.animate.scale(0.4).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 06 · STEP RAIL + DETAILED SOLVE ============
        rail = StepRail(3, top=1.5, gap=0.86, size=0.56)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        s1t = Label("STEP 1 — adiabatic W→X gives T_X", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s1a = MathTex(r"T_W\,V_W^{2/3} = T_X\,V_X^{2/3}", color=WHITE).scale(0.62).move_to(WORKC + UP*0.95)
        s1b = MathTex(r"64^{2/3}=16,\quad 125^{2/3}=25 \ \Rightarrow\ 16\,T_W = 25\,T_X", color=WHITE).scale(0.52).move_to(WORKC + DOWN*0.15)
        s1c = MathTex(r"T_X = \tfrac{16}{25}\,T_W", color=IGNITION).scale(0.66).move_to(WORKC + DOWN*1.3)
        with self.voiceover(text="Step one. The adiabatic law says T V to the two-thirds is constant. Sixty-four to the "
                                 "two-thirds is sixteen, and one twenty-five to the two-thirds is twenty-five, so sixteen "
                                 "T-W equals twenty-five T-X. That gives T-X equal to sixteen twenty-fifths of T-W.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(1.8, t.duration))
            self.play(Write(s1b), run_time=1.3)
            self.play(Write(s1c), run_time=0.9)
            add_result(r"T_X = \tfrac{16}{25}\,T_W", IGNITION)
            self.wait(max(0.1, t.duration - 4.0))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), FadeOut(s1c), rail.done(0), rail.active(1))

        s2t = Label("STEP 2 — isobaric X→Y gives T_Y", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s2a = MathTex(r"\text{constant }P:\quad \frac{V_X}{T_X} = \frac{V_Y}{T_Y}", color=WHITE).scale(0.6).move_to(WORKC + UP*0.75)
        s2b = MathTex(r"\frac{125}{T_X} = \frac{250}{T_Y} \ \Rightarrow\ T_Y = 2\,T_X", color=WHITE).scale(0.56).move_to(WORKC + DOWN*0.45)
        s2c = MathTex(r"T_Y = \tfrac{32}{25}\,T_W", color=SIGNAL).scale(0.66).move_to(WORKC + DOWN*1.55)
        with self.voiceover(text="Step two. At constant pressure V over T is constant, so V-X over T-X equals V-Y over "
                                 "T-Y. With one twenty-five and two fifty, T-Y is twice T-X — that's thirty-two "
                                 "twenty-fifths of T-W.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(2.0, t.duration))
            self.play(Write(s2b), run_time=1.3)
            self.play(Write(s2c), run_time=0.9)
            add_result(r"T_Y = \tfrac{32}{25}\,T_W", SIGNAL)
            self.wait(max(0.1, t.duration - 4.2))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), FadeOut(s2c), rail.done(1), rail.active(2))

        s3t = Label("STEP 3 — heat absorbed X→Y", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s3a = MathTex(r"Q_{XY} = nC_P\,(T_Y - T_X) = \tfrac{5}{2}\,nR\left(\tfrac{32}{25}-\tfrac{16}{25}\right)T_W", color=WHITE).scale(0.5).move_to(WORKC + UP*0.75)
        s3b = MathTex(r"= \tfrac{5}{2}\cdot\tfrac{16}{25}\,(nRT_W) = \tfrac{8}{5}\,(1)", color=WHITE).scale(0.56).move_to(WORKC + DOWN*0.45)
        s3c = MathTex(r"Q_{XY} = 1.6\ \mathrm{J}", color=CORRECT).scale(0.68).move_to(WORKC + DOWN*1.55)
        with self.voiceover(text="Step three, the heat. At constant pressure Q is n C-p delta T — five-halves n R times "
                                 "T-Y minus T-X, which is sixteen twenty-fifths of T-W. That's five-halves times sixteen "
                                 "twenty-fifths times n R T-W, which is eight-fifths of one joule: one point six joules.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.2, t.duration))
            self.play(Write(s3b), run_time=1.3)
            self.play(Write(s3c), run_time=0.9)
            add_result(r"Q_{XY}=1.6\ \mathrm J", CORRECT)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(s3t), FadeOut(s3a), FadeOut(s3b), FadeOut(s3c), rail.done(2))

        # ============ 07 · ANSWER LOCK-IN ============
        ans = Label("ANSWER:   Q_XY = 1.6 J", color=IGNITION).scale(0.8).move_to(WORKC + UP*0.1)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        with self.voiceover(text="So the heat absorbed along X to Y is one point six joules. Solved, completely.") as t:
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9); self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.7))
        self.wait(0.6)
