"""
Orange Nelumbo · DEBRIEF · Thermodynamics · t5 — "Degrees of freedom: U up, sound down"
JEE Advanced 2023 · Paper 2 · Single correct.  Answer: (C)  v5 > v7 and U5 < U6.
Concept-first (equipartition + speed of sound) → two opposite monotonic trends → step-rail solve
that eliminates A, B, D in ERROR red and locks (C) in CORRECT green.  Voice af_bella. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from voice import narration_service

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t5(VoiceoverScene):
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
        meta = Mono("JEE ADVANCED 2023 · PAPER 2", color=EMBER).scale(0.32)
        fmt = Mono("SINGLE CORRECT", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)
        q = VGroup(
            Body("An ideal gas in equilibrium; each molecule has n degrees of freedom.", color=WHITE).scale(0.44),
            Body("Internal energy of one mole is Uₙ ; the speed of sound is vₙ.", color=WHITE).scale(0.44),
            Body("At fixed temperature and pressure, which one is correct?", color=WHITE).scale(0.44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).next_to(head, DOWN, buff=0.5)
        opts = VGroup(
            MathTex(r"\text{(A)}\quad v_3 < v_6 \ \ \text{and}\ \ U_3 > U_6", color=TITANIUM).scale(0.5),
            MathTex(r"\text{(B)}\quad v_5 > v_3 \ \ \text{and}\ \ U_3 > U_5", color=TITANIUM).scale(0.5),
            MathTex(r"\text{(C)}\quad v_5 > v_7 \ \ \text{and}\ \ U_5 < U_6", color=TITANIUM).scale(0.5),
            MathTex(r"\text{(D)}\quad v_6 < v_7 \ \ \text{and}\ \ U_6 < U_7", color=TITANIUM).scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(q, DOWN, buff=0.42)
        with self.voiceover(text="An ideal gas is in equilibrium, and each molecule has n degrees of freedom. "
                                 "The internal energy of one mole is U-n, and the speed of sound is v-n. At fixed "
                                 "temperature and pressure, which one of these four statements is correct?") as t:
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
        with self.voiceover(text="Pause, and work out how U and the speed of sound depend on n yourself first.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — two laws that pull opposite ways", color=WHITE).scale(0.56).to_edge(UP, buff=LOGO_CLEAR)

        def dof_icon(color=IGNITION):
            core = Dot(ORIGIN, color=color, radius=0.16)
            arrows = VGroup(
                Arrow(ORIGIN, RIGHT * 0.7, color=color, buff=0.16, stroke_width=4, tip_length=0.14),
                Arrow(ORIGIN, UP * 0.7, color=color, buff=0.16, stroke_width=4, tip_length=0.14),
                Arrow(ORIGIN, (LEFT + DOWN) * 0.5, color=color, buff=0.16, stroke_width=4, tip_length=0.14),
            )
            return VGroup(arrows, core)

        def wave_icon(color=SIGNAL):
            ax = Line(LEFT * 0.75, RIGHT * 0.75, color=color, stroke_width=2).set_opacity(0.4)
            w = FunctionGraph(lambda x: 0.32 * np.sin(2.6 * x), x_range=[-0.75, 0.75], color=color).set_stroke(width=4)
            return VGroup(ax, w)

        def ccard(title, sub, rel, relcol, icon):
            return VGroup(icon.scale(0.95),
                          VGroup(Label(title, color=IGNITION).scale(0.5), Body(sub, color=TITANIUM).scale(0.34),
                                 MathTex(rel, color=relcol).scale(0.56)).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.34)
        c1 = ccard("EQUIPARTITION", "more freedoms → more energy", r"U_n=\tfrac{n}{2}RT", IGNITION, dof_icon(IGNITION))
        c2 = ccard("SOUND SPEED", "stiffer gas → faster sound", r"v_n=\sqrt{\tfrac{\gamma RT}{M}}", SIGNAL, wave_icon(SIGNAL))
        c3 = ccard("ADIABATIC INDEX", "more freedoms → softer gas", r"\gamma=1+\tfrac{2}{n}", EMBER, wave_icon(EMBER))
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.0).next_to(head3, DOWN, buff=0.7)
        with self.voiceover(text="Before any options, two laws. Equipartition says the internal energy of a mole is "
                                 "n over two, times R T — so more degrees of freedom means more energy.") as t:
            self.play(Write(head3), run_time=0.8); self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="The speed of sound is the square root of gamma R T over M — so it rises and falls "
                                 "with gamma, the adiabatic index.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        with self.voiceover(text="And gamma equals one plus two over n. So as n grows, gamma shrinks toward one — the gas "
                                 "gets softer, and the sound gets slower. The two trends pull opposite ways.") as t:
            self.play(FadeIn(c3, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"U_n=\tfrac{n}{2}RT \ \Rightarrow\ U_n \ \text{increases with } n", color=IGNITION).scale(0.6),
            MathTex(r"\gamma=\tfrac{C_P}{C_V}=1+\tfrac{2}{n} \ \Rightarrow\ \gamma \ \text{decreases with } n", color=EMBER).scale(0.6),
            MathTex(r"v_n=\sqrt{\tfrac{\gamma RT}{M}} \ \Rightarrow\ v_n \ \text{decreases with } n", color=SIGNAL).scale(0.6),
            MathTex(r"T,\ P \ \text{fixed for all } n \ \Rightarrow\ \text{only } n \ \text{varies}", color=WHITE).scale(0.6),
        ).arrange(DOWN, buff=0.42).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. U-n is n over two R T, so it increases with n. Gamma is one plus "
                                 "two over n, so it decreases with n. And since the speed of sound grows with gamma, "
                                 "v-n decreases with n. Temperature and pressure are fixed, so only n changes.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · VISUAL — two opposite monotonic trends ============
        head5 = Label("Two opposite trends across n = 3, 5, 6, 7", color=WHITE).scale(0.5).to_edge(UP, buff=LOGO_CLEAR)
        ns = [3, 5, 6, 7]

        def trend_panel(title, title_col, heights, bar_col, ascending):
            base = Line(LEFT * 1.35, RIGHT * 1.35, color=TITANIUM, stroke_width=2).set_opacity(0.5)
            bars = VGroup()
            for i, (nn, h) in enumerate(zip(ns, heights)):
                x = -1.05 + i * 0.7
                bar = Rectangle(width=0.34, height=h, fill_color=bar_col, fill_opacity=0.55, stroke_color=bar_col, stroke_width=1.5)
                bar.move_to([x, 0, 0], aligned_edge=DOWN).align_to(base, DOWN)
                nlab = Mono(str(nn), color=TITANIUM).scale(0.34).next_to(base, DOWN, buff=0.12).set_x(x)
                bars.add(VGroup(bar, nlab))
            arrow_dir = UP if ascending else DOWN
            trend = Arrow(base.get_left() + arrow_dir * 0.2, base.get_right() + arrow_dir * 1.5,
                          color=title_col, stroke_width=4, buff=0.1, tip_length=0.2)
            ttl = title.copy().set_color(title_col)
            panel = VGroup(base, bars, trend)
            grp = VGroup(ttl, panel).arrange(DOWN, buff=0.45)
            return grp

        u_heights = [0.55, 0.9, 1.05, 1.2]          # U rises with n
        v_heights = [1.2, 0.95, 0.85, 0.72]         # v falls with n
        t_u = VGroup(MathTex(r"U_n", color=IGNITION).scale(0.6), Body("rises", color=IGNITION).scale(0.34)).arrange(RIGHT, buff=0.18)
        t_v = VGroup(MathTex(r"v_n", color=SIGNAL).scale(0.6), Body("falls", color=SIGNAL).scale(0.34)).arrange(RIGHT, buff=0.18)
        p_u = trend_panel(t_u, IGNITION, u_heights, IGNITION, True)
        p_v = trend_panel(t_v, SIGNAL, v_heights, SIGNAL, False)
        panels = VGroup(p_u, p_v).arrange(RIGHT, buff=2.0).next_to(head5, DOWN, buff=0.7).shift(LEFT * 0.4)

        with self.voiceover(text="Picture it. On the left, U-n climbs as n goes three, five, six, seven — the taller each "
                                 "bar, the more internal energy.") as t:
            self.play(Write(head5), run_time=0.7)
            self.play(FadeIn(p_u[0]), Create(p_u[1][0]), run_time=0.7)
            self.play(*[GrowFromEdge(b[0], DOWN) for b in p_u[1][1]], *[FadeIn(b[1]) for b in p_u[1][1]], run_time=1.0)
            self.play(GrowArrow(p_u[1][2]), run_time=0.8)
            self.wait(max(0.1, t.duration - 3.2))
        with self.voiceover(text="On the right, the speed of sound does the opposite — it falls as n grows. The two "
                                 "trends are mirror images.") as t:
            self.play(FadeIn(p_v[0]), Create(p_v[1][0]), run_time=0.7)
            self.play(*[GrowFromEdge(b[0], DOWN) for b in p_v[1][1]], *[FadeIn(b[1]) for b in p_v[1][1]], run_time=1.0)
            self.play(GrowArrow(p_v[1][2]), run_time=0.8)
            self.wait(max(0.1, t.duration - 2.5))
        self.play(FadeOut(head5), panels.animate.scale(0.4).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 06 · STEP RAIL + SOLVE ============
        rail = StepRail(3, top=1.5, gap=1.0, size=0.6)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        s1t = Label("STEP 1 — order the energies", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s1a = MathTex(r"U_n=\tfrac{n}{2}RT \ \ (\text{equipartition})", color=WHITE).scale(0.6).move_to(WORKC + UP*0.9)
        s1b = MathTex(r"n:\ 3<5<6<7 \ \Rightarrow\ U_3<U_5<U_6<U_7", color=WHITE).scale(0.54).move_to(WORKC + DOWN*0.2)
        s1c = MathTex(r"\Rightarrow\ U_5<U_6 \ \checkmark", color=IGNITION).scale(0.6).move_to(WORKC + DOWN*1.3)
        with self.voiceover(text="Step one, order the energies. Since U-n is n over two R T, it grows with n. So U-three "
                                 "is less than U-five, less than U-six, less than U-seven. In particular, U-five is less "
                                 "than U-six.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(1.8, t.duration))
            self.play(Write(s1b), run_time=1.3)
            self.play(Write(s1c), run_time=0.9)
            add_result(r"U_5<U_6", IGNITION)
            self.wait(max(0.1, t.duration - 4.0))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), FadeOut(s1c), rail.done(0), rail.active(1))

        s2t = Label("STEP 2 — order the sound speeds", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s2a = MathTex(r"v_n=\sqrt{\tfrac{\gamma RT}{M}},\quad \gamma=1+\tfrac{2}{n}", color=WHITE).scale(0.58).move_to(WORKC + UP*0.9)
        s2b = MathTex(r"n\uparrow \Rightarrow \gamma\downarrow \Rightarrow v_n\downarrow:\ v_3>v_5>v_6>v_7", color=WHITE).scale(0.5).move_to(WORKC + DOWN*0.2)
        s2c = MathTex(r"\Rightarrow\ v_5>v_7 \ \checkmark", color=SIGNAL).scale(0.6).move_to(WORKC + DOWN*1.3)
        with self.voiceover(text="Step two, order the sound speeds. The speed is the square root of gamma R T over M, and "
                                 "gamma is one plus two over n. As n rises, gamma falls, so v-n falls: v-three beats "
                                 "v-five beats v-six beats v-seven. In particular, v-five is greater than v-seven.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(2.0, t.duration))
            self.play(Write(s2b), run_time=1.3)
            self.play(Write(s2c), run_time=0.9)
            add_result(r"v_5>v_7", SIGNAL)
            self.wait(max(0.1, t.duration - 4.2))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), FadeOut(s2c), rail.done(1), rail.active(2))

        s3t = Label("STEP 3 — test the four options", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        oA = MathTex(r"\text{(A)}\ v_3<v_6\ \times\ (v_3>v_6)", color=ERROR).scale(0.52).move_to(WORKC + UP*1.0)
        oB = MathTex(r"\text{(B)}\ U_3>U_5\ \times\ (U_3<U_5)", color=ERROR).scale(0.52).move_to(WORKC + UP*0.25)
        oD = MathTex(r"\text{(D)}\ v_6<v_7\ \times\ (v_6>v_7)", color=ERROR).scale(0.52).move_to(WORKC + DOWN*0.5)
        oC = MathTex(r"\text{(C)}\ v_5>v_7\ \checkmark\ \ \text{and}\ \ U_5<U_6\ \checkmark", color=CORRECT).scale(0.52).move_to(WORKC + DOWN*1.35)
        with self.voiceover(text="Step three, test the options. In A, v-three is not less than v-six — it's greater. Wrong. "
                                 "In B, U-three is not greater than U-five — it's less. Wrong. In D, v-six is not less than "
                                 "v-seven — it's greater. Wrong.") as t:
            self.play(FadeIn(s3t), run_time=0.5)
            self.play(Write(oA), run_time=0.9)
            self.play(Write(oB), run_time=0.9)
            self.play(Write(oD), run_time=0.9)
            self.wait(max(0.1, t.duration - 3.2))
        with self.voiceover(text="Only C survives: v-five is greater than v-seven, and U-five is less than U-six. Both true.") as t:
            self.play(Write(oC), run_time=1.2)
            self.wait(max(0.1, t.duration - 1.2))
        self.play(FadeOut(s3t), FadeOut(oA), FadeOut(oB), FadeOut(oD), FadeOut(oC), rail.done(2))

        # ============ 07 · ANSWER LOCK-IN ============
        ans = Label("ANSWER:   (C)", color=IGNITION).scale(0.85).move_to(WORKC + UP*0.5)
        sub = MathTex(r"v_5>v_7 \ \ \text{and}\ \ U_5<U_6", color=CORRECT).scale(0.62).move_to(WORKC + DOWN*0.75)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        with self.voiceover(text="So the answer is C. The speed of sound falls with n, and the internal energy rises with "
                                 "n — two opposite trends, one clean choice.") as t:
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9)
            self.play(Create(box), run_time=0.8)
            self.play(Write(sub), run_time=1.0)
            self.wait(max(0.3, t.duration - 2.7))
        self.wait(0.6)
