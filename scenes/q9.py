"""
Orange Nelumbo · DEBRIEF · Kinematics · Q9 — "Two projectiles collide"
JEE Advanced 2024 · Paper 2 · Numerical.  Answer: (T1/T2)^2 = 2.
Chrome: logo top-left · chapter bottom-left · progress top-right · results rail right ·
diagram docks bottom-right · like+subscribe end card.  Voice af_bella. 4K. Collision-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

TOTAL = 12
WORKC = LEFT * 1.7          # centre of the left-hand work area during the solve
RAIL_X = 4.85               # right-side results rail x
RAIL_Y = [2.35, 1.72, 1.09, 0.46, -0.17]


class Scene_q9(VoiceoverScene):
    def construct(self):
        apply_bg(self)
        self.set_speech_service(KokoroService(voice="af_bella"))

        # ---------------- persistent chrome ----------------
        logo = on_logo(0.5).to_corner(UL, buff=0.45)
        chapter = Body("Kinematics", color=TITANIUM).scale(0.4).to_corner(DL, buff=0.45)
        prog = Mono(f"01 / {TOTAL}", color=TITANIUM).scale(0.28).to_corner(UR, buff=0.45)
        self.add(logo, chapter, prog)

        def set_prog(n):
            self.play(Transform(prog, Mono(f"{n:02d} / {TOTAL}", color=TITANIUM).scale(0.28)
                                 .to_corner(UR, buff=0.45)), run_time=0.4, rate_func=smooth)

        # results rail (fixed slots, LaTeX chips, no re-stacking)
        self._ri = 0
        def add_result(latex, color=SIGNAL):
            c = mchip(latex, color=color, tscale=0.38).move_to(RIGHT * RAIL_X + UP * RAIL_Y[self._ri])
            self._ri += 1
            self.play(FadeIn(c, shift=LEFT * 0.15), run_time=0.5, rate_func=smooth)
            return c

        # ============ 01 · QUESTION ============
        badge_t = Mono("N1", color=OBSIDIAN).scale(0.5)
        badge = VGroup(SurroundingRectangle(badge_t, color=IGNITION, fill_color=IGNITION,
                       fill_opacity=1, buff=0.13, corner_radius=0.06), badge_t)
        meta = Mono("JEE ADVANCED 2024 · PAPER 2", color=EMBER).scale(0.34)
        fmt = Mono("NUMERICAL", color=SIGNAL).scale(0.34)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.4), fmt).arrange(RIGHT, buff=1.0).to_edge(UP, buff=1.0)
        qline = VGroup(
            Body("A ball is thrown from A; a stone from B, at the same instant,", color=WHITE).scale(0.5),
            Body("with just the right speed to hit the ball in mid-air.", color=WHITE).scale(0.5),
            MathTex(r"(45^\circ,45^\circ)\to T_1 \qquad (60^\circ,30^\circ)\to T_2", color=SIGNAL).scale(0.6),
        ).arrange(DOWN, buff=0.38).next_to(head, DOWN, buff=0.7)
        target = MathTex(r"\text{Find}\ \ (T_1/T_2)^2", color=IGNITION).scale(0.9).next_to(qline, DOWN, buff=0.6)
        with self.voiceover(text="Here's a beautiful JEE Advanced problem. A ball is thrown from one point, and at "
                                 "the same instant a stone from another — with exactly the right speed to collide "
                                 "with it in mid-air. We want the ratio of the two collision times, squared.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.8)
            for ln in qline:
                self.play(FadeIn(ln, shift=UP * 0.12), run_time=0.6, rate_func=smooth)
            self.play(Write(target), run_time=0.9)
            self.wait(max(0.2, t.duration - 3.9))
        self.play(FadeOut(head), FadeOut(qline), FadeOut(target))

        # ============ 02 · PAUSE ============
        set_prog(2)
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Before we solve — pause, and try setting it up yourself. Five seconds.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)),
                          run_time=max(0.4, (t.duration - 1.4) / 4), rate_func=linear)
            self.wait(0.2)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · READ ============
        set_prog(3)
        rlbl = kicker("03", "READ THE SETUP").to_edge(UP, buff=1.0)
        g1 = MathTex(r"\text{Given: }\ v_0,\ \theta_0,\ \theta_1,\ L", color=SIGNAL).scale(0.55)
        g2 = Body("Trigger:  \"same instant\"  ·  \"suitable speed to hit\"", color=AMBER).scale(0.46)
        g3 = MathTex(r"\text{Target:}\ \ (T_1/T_2)^2", color=IGNITION).scale(0.62)
        col = VGroup(g1, g2, g3).arrange(DOWN, buff=0.5).next_to(rlbl, DOWN, buff=0.7)
        with self.voiceover(text="Read carefully. The givens, in cyan: the ball's speed and angle, the stone's "
                                 "angle, and the gap L.") as t:
            self.play(FadeIn(rlbl), run_time=0.4); self.play(FadeIn(g1, shift=RIGHT * 0.15), run_time=0.9)
            self.wait(max(0.1, t.duration - 1.3))
        with self.voiceover(text="The triggers, in amber: they launch at the same instant, and the stone's speed is "
                                 "not free — it's suitable, chosen to make them meet.") as t:
            self.play(FadeIn(g2, shift=RIGHT * 0.15), run_time=0.9); self.wait(max(0.1, t.duration - 0.9))
        with self.voiceover(text="And the target, in orange: a squared ratio — so it should be a pure number.") as t:
            self.play(FadeIn(g3, shift=RIGHT * 0.15), run_time=0.9); self.wait(max(0.1, t.duration - 0.9))
        self.play(FadeOut(rlbl), FadeOut(col))

        # ============ 04 · CONCEPT MAP ============
        set_prog(4)
        clbl = kicker("04", "CONCEPTS IN PLAY").to_edge(UP, buff=1.0)
        def cchip(txt, colr, crux=False):
            tt = Mono(txt, color=colr).scale(0.44)
            return VGroup(SurroundingRectangle(tt, color=(IGNITION if crux else colr), buff=0.17,
                          corner_radius=0.08, stroke_width=(3 if crux else 1.5)), tt)
        chips = VGroup(cchip("PROJECTILE MOTION", TITANIUM),
                       cchip("SHARED VERTICAL MOTION", IGNITION, crux=True),
                       cchip("HORIZONTAL CATCH-UP", SIGNAL)).arrange(DOWN, buff=0.38).next_to(clbl, DOWN, buff=0.65)
        misfire = Body("Misfire:  chasing full time-of-flight — you never need it", color=ERROR).scale(0.42)
        misfire.next_to(chips, DOWN, buff=0.55)
        with self.voiceover(text="Three ideas. Projectile motion, yes. But the crux — the ignition chip — is that both "
                                 "objects share the exact same vertical motion. See that, and the collision is a pure "
                                 "horizontal catch-up.") as t:
            self.play(FadeIn(clbl), run_time=0.4)
            for c in chips:
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.55, rate_func=smooth)
            self.wait(max(0.1, t.duration - 2.1))
        with self.voiceover(text="The classic misfire is chasing the full time of flight. You never need it.") as t:
            self.play(FadeIn(misfire, shift=UP * 0.1), run_time=0.8); self.wait(max(0.1, t.duration - 0.8))
        self.play(FadeOut(clbl), FadeOut(chips), FadeOut(misfire))

        # ============ 05 · THE PICTURE (draw centre, then dock bottom-right) ============
        set_prog(5)
        ground = Line(LEFT * 5.0, RIGHT * 5.0, color=TITANIUM, stroke_width=3).shift(DOWN * 2.2)
        A = np.array([-4.2, -2.2, 0]); B = np.array([4.2, -2.2, 0]); P = np.array([0.5, 1.0, 0])
        ball = VMobject(color=EMBER, stroke_width=4)
        ball.set_points_smoothly([A, np.array([-2.0, 1.6, 0]), P, np.array([2.2, -2.2, 0])])
        stone = VMobject(color=TITANIUM, stroke_width=4)
        stone.set_points_smoothly([B, np.array([2.5, 1.5, 0]), P])
        dotA = Dot(A, color=EMBER).scale(0.8); dotB = Dot(B, color=SIGNAL).scale(0.8); Pdot = Dot(P, color=IGNITION).scale(1.1)
        Alab = Mono("A", color=EMBER).scale(0.5).next_to(dotA, DOWN, buff=0.16)
        Blab = Mono("B", color=SIGNAL).scale(0.5).next_to(dotB, DOWN, buff=0.16)
        Plab = Mono("P", color=IGNITION).scale(0.5).next_to(Pdot, UP, buff=0.13)
        with self.voiceover(text="Here's the picture. The ball launches from A, the stone from B, and they meet at P.") as t:
            self.play(Create(ground), FadeIn(dotA), FadeIn(dotB), Write(Alab), Write(Blab), run_time=1.1)
            self.play(Create(ball), run_time=min(1.5, max(0.8, t.duration - 2.2)))
            self.play(Create(stone), run_time=1.1)
            self.play(FadeIn(Pdot, scale=1.4), Write(Plab), run_time=0.6)
            self.wait(max(0.1, t.duration - 3.4))
        diagram = VGroup(ground, ball, stone, dotA, dotB, Pdot, Alab, Blab, Plab)
        # dock bottom-right as the reference thumbnail
        self.play(diagram.animate.scale(0.34).to_corner(DR, buff=0.4), run_time=0.9, rate_func=smooth)

        # ============ 06 · STEP 1 — vertical match ============
        set_prog(6)
        s1t = Label("STEP 1 — match the vertical motion", color=WHITE).scale(0.46).move_to(WORKC + UP * 2.0)
        s1a = MathTex(r"v_0\sin\theta_0 = v_1\sin\theta_1", color=WHITE).scale(0.8).move_to(WORKC + UP * 0.8)
        s1b = MathTex(r"v_1 = \frac{v_0\sin\theta_0}{\sin\theta_1}", color=IGNITION).scale(0.85).move_to(WORKC + DOWN * 0.3)
        s1n = Body("Same vertical speed → equal height, always", color=SIGNAL).scale(0.42).move_to(WORKC + DOWN * 1.4)
        with self.voiceover(text="Step one — match the vertical motion. Same gravity, so to stay level they need the "
                                 "same upward speed: v-zero sine theta-zero equals v-one sine theta-one.") as t:
            self.play(FadeIn(s1t), run_time=0.4); self.play(Write(s1a), run_time=1.0)
            self.wait(max(0.1, t.duration - 1.4))
        with self.voiceover(text="That fixes the stone's suitable speed — and means they never differ in height.") as t:
            self.play(Write(s1b), run_time=1.0); self.play(FadeIn(s1n, shift=UP * 0.1), run_time=0.5)
            add_result(r"v_1 = v_0\sin\theta_0/\sin\theta_1", IGNITION)
            self.wait(max(0.1, t.duration - 2.0))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), FadeOut(s1n))

        # ============ 07 · STEP 2 — horizontal catch-up ============
        set_prog(7)
        s2t = Label("STEP 2 — horizontal catch-up", color=WHITE).scale(0.46).move_to(WORKC + UP * 2.0)
        s2a = MathTex(r"T = \frac{L}{v_0\cos\theta_0 + v_1\cos\theta_1}", color=WHITE).scale(0.72).move_to(WORKC + UP * 0.7)
        s2b = MathTex(r"= \frac{L\sin\theta_1}{v_0\,\sin(\theta_0+\theta_1)}", color=IGNITION).scale(0.78).move_to(WORKC + DOWN * 0.8)
        with self.voiceover(text="Step two. They close the gap L at their combined horizontal speed — so T is L over "
                                 "v-zero cos theta-zero plus v-one cos theta-one.") as t:
            self.play(FadeIn(s2t), run_time=0.4); self.play(Write(s2a), run_time=1.2)
            self.wait(max(0.1, t.duration - 1.6))
        with self.voiceover(text="Substitute and tidy up, and it folds into a clean form: L sine theta-one over "
                                 "v-zero sine of theta-zero plus theta-one.") as t:
            self.play(Write(s2b), run_time=1.2)
            add_result(r"T = \frac{L\sin\theta_1}{v_0\sin(\theta_0+\theta_1)}", SIGNAL)
            self.wait(max(0.1, t.duration - 1.2))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b))

        # ============ 08 · STEP 3 — plug in ============
        set_prog(8)
        s3t = Label("STEP 3 — the two cases", color=WHITE).scale(0.46).move_to(WORKC + UP * 2.0)
        t1 = MathTex(r"T_1 = \frac{L\sin 45^\circ}{v_0\sin 90^\circ} = \frac{L}{\sqrt{2}\,v_0}", color=WHITE).scale(0.72).move_to(WORKC + UP * 0.6)
        t2 = MathTex(r"T_2 = \frac{L\sin 30^\circ}{v_0\sin 90^\circ} = \frac{L}{2 v_0}", color=WHITE).scale(0.72).move_to(WORKC + DOWN * 0.9)
        with self.voiceover(text="Step three — plug in. First case, forty-five and forty-five: the angles sum to "
                                 "ninety, so T-one is L over root two v-zero.") as t:
            self.play(FadeIn(s3t), run_time=0.4); self.play(Write(t1), run_time=1.3)
            add_result(r"T_1 = L/\sqrt{2}\,v_0", SIGNAL)
            self.wait(max(0.1, t.duration - 1.7))
        with self.voiceover(text="Second case, sixty and thirty — again ninety — T-two is L over two v-zero.") as t:
            self.play(Write(t2), run_time=1.3)
            add_result(r"T_2 = L/2v_0", SIGNAL)
            self.wait(max(0.1, t.duration - 1.3))
        self.play(FadeOut(s3t), FadeOut(t1), FadeOut(t2))

        # ============ 09 · STEP 4 — the ratio ============
        set_prog(9)
        s4 = MathTex(r"\frac{T_1}{T_2} = \frac{2}{\sqrt{2}} = \sqrt{2}", color=WHITE).scale(0.85).move_to(WORKC + UP * 0.6)
        ans = MathTex(r"\left(\frac{T_1}{T_2}\right)^2 = 2", color=CORRECT).scale(1.0).move_to(WORKC + DOWN * 1.0)
        with self.voiceover(text="Step four. Divide: two over root two is root two.") as t:
            self.play(Write(s4), run_time=1.1); self.wait(max(0.1, t.duration - 1.1))
        with self.voiceover(text="Square it — the answer is exactly two.") as t:
            self.play(Write(ans), run_time=1.0)
            add_result(r"(T_1/T_2)^2 = 2", CORRECT)
            self.wait(max(0.1, t.duration - 1.0))
        self.play(FadeOut(s4), FadeOut(ans))

        # ============ 10 · THE SHORTCUT ============
        set_prog(10)
        hlbl = kicker("10", "THE SHORTCUT", color=SIGNAL).move_to(WORKC + UP * 2.0)
        h1 = MathTex(r"\theta_0+\theta_1 = 90^\circ \Rightarrow \sin(\theta_0+\theta_1)=1", color=SIGNAL).scale(0.66).move_to(WORKC + UP * 0.7)
        h2 = MathTex(r"T \propto \sin\theta_1 \Rightarrow \frac{T_1}{T_2}=\frac{\sin 45^\circ}{\sin 30^\circ}=\sqrt{2}", color=IGNITION).scale(0.62).move_to(WORKC + DOWN * 0.7)
        with self.voiceover(text="Here's the shortcut a sharp exam-taker spots at once. In both cases the angles add "
                                 "to ninety, so that whole denominator is just one.") as t:
            self.play(FadeIn(hlbl), run_time=0.4); self.play(Write(h1), run_time=1.2)
            self.wait(max(0.1, t.duration - 1.6))
        with self.voiceover(text="So the time is simply proportional to sine theta-one, and the ratio is root two — "
                                 "no algebra at all.") as t:
            self.play(Write(h2), run_time=1.3); self.wait(max(0.1, t.duration - 1.3))
        self.play(FadeOut(hlbl), FadeOut(h1), FadeOut(h2))

        # ============ 11 · THE TRAP ============
        set_prog(11)
        tlbl = kicker("11", "THE TRAP", color=ERROR).move_to(WORKC + UP * 2.0)
        trap = MathTex(r"v_1 = v_0", color=ERROR).scale(0.85).move_to(WORKC + UP * 0.6)
        trapc = Body("(Assuming equal speeds)", color=ERROR).scale(0.42).move_to(WORKC + DOWN * 0.1)
        strike = Line(trap.get_left(), trap.get_right(), color=ERROR, stroke_width=5).move_to(trap)
        why = Body("The stone's speed is set by the height-match", color=TITANIUM).scale(0.42).move_to(WORKC + DOWN * 1.1)
        with self.voiceover(text="And the trap. It's tempting to assume the stone has the same speed as the ball. "
                                 "It doesn't.") as t:
            self.play(FadeIn(tlbl), run_time=0.4); self.play(Write(trap), FadeIn(trapc), run_time=1.0)
            self.play(Create(strike), run_time=0.5); self.wait(max(0.1, t.duration - 1.9))
        with self.voiceover(text="Its speed is pinned by the height-match. The word suitable was doing real work.") as t:
            self.play(FadeIn(why, shift=UP * 0.1), run_time=0.8); self.wait(max(0.1, t.duration - 0.8))
        self.play(FadeOut(tlbl), FadeOut(trap), FadeOut(trapc), FadeOut(strike), FadeOut(why),
                  FadeOut(diagram), FadeOut(self._collect_rail()))

        # ============ 12 · LOCK-IN + END CARD ============
        set_prog(12)
        box_ans = MathTex(r"\left(\frac{T_1}{T_2}\right)^2 = 2", color=CORRECT).scale(1.3).move_to(UP * 1.4)
        box = SurroundingRectangle(box_ans, color=CORRECT, buff=0.3, corner_radius=0.1)
        take = Label("Shared vertical motion → collision is pure horizontal catch-up.", color=WHITE).scale(0.44).next_to(box, DOWN, buff=0.6)
        with self.voiceover(text="Lock it in — the answer is two. And the one thing to carry away: when two "
                                 "projectiles share their vertical motion, the collision is nothing but a horizontal "
                                 "catch-up.") as t:
            self.play(FadeIn(box_ans, shift=DOWN * 0.1), run_time=0.9); self.play(Create(box), run_time=0.8)
            self.play(FadeIn(take, shift=UP * 0.1), run_time=0.9)
            self.wait(max(0.2, t.duration - 2.6))
        self.play(FadeOut(box_ans), FadeOut(box), FadeOut(take))

        # end card — clean like / subscribe buttons
        big = on_logo(0.66).move_to(UP * 2.0)
        head_e = Label("Enjoyed the breakdown?", color=WHITE).scale(0.6).move_to(UP * 0.55)

        def button(label_txt, filled):
            lt = Label(label_txt, color=(OBSIDIAN if filled else IGNITION)).scale(0.5)
            bx = RoundedRectangle(width=lt.width + 0.85, height=lt.height + 0.55, corner_radius=0.22,
                                  fill_color=IGNITION, fill_opacity=(1 if filled else 0),
                                  stroke_color=IGNITION, stroke_width=(0 if filled else 3))
            return VGroup(bx, lt)
        btns = VGroup(button("LIKE", False), button("SUBSCRIBE", True)).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.75)
        mantra = Mono("In pursuit of mastery.", color=EMBER).scale(0.44).move_to(DOWN * 2.15)
        with self.voiceover(text="If this made it click, hit like and subscribe — we solve one JEE problem, "
                                 "completely, every single time. In pursuit of mastery.") as t:
            self.play(FadeIn(big, shift=DOWN * 0.15), run_time=0.9)
            self.play(Write(head_e), run_time=0.8)
            self.play(FadeIn(btns[0], shift=UP * 0.1), FadeIn(btns[1], shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(mantra), run_time=0.5)
            self.wait(max(0.4, t.duration - 2.9))
        self.wait(0.7)

    # collect all rail chips currently on screen for a clean fade
    def _collect_rail(self):
        return VGroup(*[m for m in self.mobjects
                        if isinstance(m, VGroup) and len(m) == 2
                        and isinstance(m[0], RoundedRectangle)])
