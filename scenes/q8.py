"""
Orange Nelumbo · Kinematics · Q8 — "Projectile Explosion" (TEACHER-LED lesson)
JEE Adv projectile (multi-correct). Answer: A and C.
Style: a teacher explaining — show the question, say what it's about, WHICH methods and
WHY, pause-and-think prompts, on-screen written explanation beside the animation.
Follows kinematics_guidelines.md. Voice: Kokoro af_bella. Overlap-checked (layout_check).
"""
from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

BG       = "#0E0D10"
IGNITION = "#FF5A1F"     # concept in focus
EMBER    = "#FF7A2E"
CYAN     = "#3DE0D0"     # motion / vectors / data
TXT      = "#E8E6EC"
MUTED    = "#8A8A93"
REDX     = "#E0483C"
GOOD     = "#3DE0D0"
SG   = "Space Grotesk"
MONO = "JetBrains Mono"

TOTAL = 12


class Scene_q8(VoiceoverScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_speech_service(KokoroService(voice="af_bella"))

        # ---------- persistent chrome ----------
        tag  = Text("// KINEMATICS", font=MONO, color=IGNITION).scale(0.30)
        mark = Text("ORANGE NELUMBO", font=MONO, color=MUTED).scale(0.24)
        tag.to_corner(UL, buff=0.4)
        mark.next_to(tag, DOWN, aligned_edge=LEFT, buff=0.12)
        lesson = Text("LESSON · Projectile explosion", font=MONO, color=MUTED).scale(0.22)
        lesson.to_corner(DL, buff=0.35)
        prog = Text(f"01 / {TOTAL}", font=MONO, color=MUTED).scale(0.24).to_corner(UR, buff=0.4)
        self.add(tag, mark, lesson, prog)

        def set_prog(n):
            new = Text(f"{n:02d} / {TOTAL}", font=MONO, color=MUTED).scale(0.24).move_to(prog)
            self.play(Transform(prog, new), run_time=0.4)

        # small helper: a "written explanation" caption line, lives in a safe band, one at a time
        def caption(txt, color=MUTED):
            return Text(txt, font=MONO, color=color).scale(0.34).to_edge(DOWN, buff=1.15)

        # ================= 01 · TITLE =================
        title = Text("PROJECTILE EXPLOSION", font=SG, color=TXT, weight=BOLD).scale(0.85)
        sub   = Text("let's reason it out, together", font=MONO, color=MUTED).scale(0.4)
        sub.next_to(title, DOWN, buff=0.3)
        with self.voiceover(text="Hello. Today we're going to reason through a beautiful projectile problem — "
                                 "not just get the answer, but understand exactly why.") as t:
            self.play(Write(title), run_time=min(2.0, t.duration))
            self.play(FadeIn(sub, shift=UP*0.2), run_time=0.7)
            self.wait(max(0.1, t.duration - 2.7))
        self.play(FadeOut(title), FadeOut(sub))

        # ================= 02 · READ THE QUESTION =================
        set_prog(2)
        qlbl = Text("THE QUESTION", font=MONO, color=IGNITION).scale(0.4).to_edge(UP, buff=1.1)
        scenario = VGroup(
            Text("A particle is projected at speed u, angle θ.", font=MONO, color=TXT).scale(0.46),
            Text("At the highest point it explodes into two equal halves.", font=MONO, color=TXT).scale(0.46),
            Text("One half stops instantly and drops straight down.", font=MONO, color=CYAN).scale(0.46),
            Text("The other half flies on under gravity.", font=MONO, color=IGNITION).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(qlbl, DOWN, buff=0.6)
        with self.voiceover(text="First, let's read it slowly. A particle is projected with speed u at an angle theta. "
                                 "At the highest point of its flight, it explodes into two equal halves. "
                                 "One half stops instantly and drops straight down... "
                                 "while the other half keeps flying under gravity.") as t:
            self.play(FadeIn(qlbl), run_time=0.5)
            for line in scenario:
                self.play(FadeIn(line, shift=RIGHT*0.15), run_time=0.7)
            self.wait(max(0.1, t.duration - 3.3))
        self.play(FadeOut(qlbl), FadeOut(scenario))

        # options
        opts = VGroup(
            Text("A   2nd fragment lands at 3R/2 from launch", font=MONO, color=TXT).scale(0.44),
            Text("B   it lands with speed u√(cos²θ + 4sin²θ)", font=MONO, color=TXT).scale(0.44),
            Text("C   the centre of mass keeps the original path", font=MONO, color=TXT).scale(0.44),
            Text("D   time to fall after explosion = 2u sinθ / g", font=MONO, color=TXT).scale(0.44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(ORIGIN)
        olbl = Text("Which of these are correct?", font=MONO, color=MUTED).scale(0.4).next_to(opts, UP, buff=0.5)
        with self.voiceover(text="And we're asked — which of these four statements are correct? "
                                 "Don't try to solve yet. Just take them in.") as t:
            self.play(FadeIn(olbl), run_time=0.6)
            for o in opts:
                self.play(FadeIn(o, shift=RIGHT*0.12), run_time=0.5)
            self.wait(max(0.1, t.duration - 2.6))
        self.play(FadeOut(olbl), FadeOut(opts))

        # ================= 03 · WHAT IS THIS ABOUT? =================
        set_prog(3)
        head = Text("What is this really about?", font=SG, color=TXT).scale(0.6).to_edge(UP, buff=1.2)
        ideas = VGroup(
            Text("①  Projectile motion — a particle in flight", font=MONO, color=CYAN).scale(0.46),
            Text("②  An explosion — that means momentum", font=MONO, color=IGNITION).scale(0.46),
            Text("③  Centre of mass — of the broken pieces", font=MONO, color=EMBER).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.7)
        with self.voiceover(text="Now, step back. What is this question really testing? Three ideas are hiding here. "
                                 "One — projectile motion. Two — an explosion, which should make you think of momentum. "
                                 "And three — the centre of mass of the pieces.") as t:
            self.play(Write(head), run_time=1.2)
            for i in ideas:
                self.play(FadeIn(i, shift=RIGHT*0.15), run_time=0.8)
            self.wait(max(0.1, t.duration - 3.6))
        self.play(FadeOut(head), FadeOut(ideas))

        # ================= 04 · WHICH METHODS, AND WHY =================
        set_prog(4)
        head2 = Text("Which tools — and why?", font=SG, color=TXT).scale(0.6).to_edge(UP, buff=1.2)
        why = VGroup(
            Text("Explosion is INTERNAL  →  momentum is conserved", font=MONO, color=IGNITION).scale(0.44),
            Text("After the split  →  plain free-fall kinematics", font=MONO, color=CYAN).scale(0.44),
            Text("Only gravity acts outside  →  COM path unchanged", font=MONO, color=EMBER).scale(0.44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head2, DOWN, buff=0.7)
        with self.voiceover(text="Why those tools? Because the explosion is internal — no outside push — "
                                 "so momentum is conserved through the bang. "
                                 "Once the pieces separate, each just obeys ordinary free-fall kinematics. "
                                 "And since gravity is the only external force, the centre of mass can't feel the explosion at all.") as t:
            self.play(Write(head2), run_time=1.1)
            for w in why:
                self.play(FadeIn(w, shift=RIGHT*0.15), run_time=0.9)
            self.wait(max(0.1, t.duration - 3.8))
        self.play(FadeOut(head2), FadeOut(why))

        # ================= 05 · PAUSE & THINK #1 =================
        set_prog(5)
        think = Text("⏸  PAUSE & THINK", font=MONO, color=IGNITION, weight=BOLD).scale(0.55).to_edge(UP, buff=1.5)
        q1 = Text("At the highest point of a projectile,", font=MONO, color=TXT).scale(0.5)
        q1b = Text("what is its vertical velocity?", font=MONO, color=TXT).scale(0.5)
        qgrp = VGroup(q1, q1b).arrange(DOWN, buff=0.3).next_to(think, DOWN, buff=0.8)
        with self.voiceover(text="Let's pause. Here's your first think. At the highest point of any projectile, "
                                 "what is the vertical velocity? Pause the video... and picture it.") as t:
            self.play(FadeIn(think, shift=DOWN*0.2), run_time=0.8)
            self.play(FadeIn(qgrp), run_time=1.0)
            self.wait(max(0.4, t.duration - 1.8))
        reveal = MathTex(r"v_y = 0,\qquad v_x = u\cos\theta", color=IGNITION).scale(0.9).next_to(qgrp, DOWN, buff=0.7)
        with self.voiceover(text="Right — at the top, the vertical velocity is exactly zero. "
                                 "Only the horizontal part, u cosine theta, is left.") as t:
            self.play(Write(reveal), run_time=1.4)
            self.wait(max(0.1, t.duration - 1.4))
        self.play(FadeOut(think), FadeOut(qgrp), FadeOut(reveal))

        # ================= 06 · THE PICTURE (hero visual) =================
        set_prog(6)
        ground = Line(LEFT*6.2, RIGHT*6.2, color=MUTED, stroke_width=3).shift(DOWN*2.6)
        O   = np.array([-4.5, -2.6, 0]); AP = np.array([-1.5, 0.4, 0])
        RR  = np.array([1.5, -2.6, 0]);  L2 = np.array([4.5, -2.6, 0])
        arc0 = VMobject(color=CYAN, stroke_width=4); arc0.set_points_smoothly([O, AP, RR])
        dotO = Dot(O, color=CYAN).scale(0.8); apex = Dot(AP, color=IGNITION).scale(0.9)
        Hline = DashedLine(AP, [AP[0], -2.6, 0], color=MUTED, stroke_width=2)
        aplab = MathTex(r"\left(\tfrac{R}{2},\,H\right)", color=IGNITION).scale(0.5).next_to(AP, UP, buff=0.15)
        cap6 = caption("the apex: highest point, v_y = 0", CYAN)
        with self.voiceover(text="Let's draw it. The particle climbs along this cyan arc to its apex — "
                                 "that's the highest point, at R over two across and height H up.") as t:
            self.play(Create(ground), FadeIn(dotO), run_time=0.9)
            self.play(Create(arc0), run_time=min(1.8, max(0.8, t.duration-2.2)))
            self.play(FadeIn(apex, scale=1.4), Create(Hline), FadeIn(aplab), FadeIn(cap6), run_time=1.1)
            self.wait(max(0.1, t.duration - 3.8))

        # ================= 07 · PAUSE & THINK #2 =================
        set_prog(7)
        self.play(FadeOut(cap6))
        think2 = Text("⏸  THINK", font=MONO, color=IGNITION, weight=BOLD).scale(0.5).to_edge(UP, buff=1.4)
        q2 = VGroup(
            Text("One half stops dead.", font=MONO, color=TXT).scale(0.48),
            Text("Which law finds the other half's speed?", font=MONO, color=TXT).scale(0.48),
        ).arrange(DOWN, buff=0.3).next_to(think2, DOWN, buff=0.6)
        with self.voiceover(text="Second think. The explosion splits it in two, and one half simply stops. "
                                 "Which single law lets you find the speed of the other half? Pause and decide.") as t:
            self.play(FadeIn(think2, shift=DOWN*0.2), FadeIn(q2), run_time=1.0)
            self.wait(max(0.4, t.duration - 1.0))
        ans2 = Text("→  Conservation of momentum", font=MONO, color=IGNITION).scale(0.5).next_to(q2, DOWN, buff=0.6)
        with self.voiceover(text="Yes — conservation of momentum. The explosion is internal, "
                                 "so the total momentum just before equals the total just after.") as t:
            self.play(FadeIn(ans2, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration - 1.0))
        self.play(FadeOut(think2), FadeOut(q2), FadeOut(ans2))

        # ================= 08 · EXPLOSION → V = 2u cosθ =================
        set_prog(8)
        boom = Star(n=8, outer_radius=0.35, color=IGNITION, fill_opacity=1).move_to(AP)
        drop = DashedLine(AP, [AP[0], -2.6, 0], color=REDX, stroke_width=4)
        arc2 = VMobject(color=IGNITION, stroke_width=4); arc2.set_points_smoothly([AP, np.array([1.5,-1.0,0]), L2])
        landdot = Dot(L2, color=IGNITION).scale(0.8)
        mom = MathTex(r"\tfrac{M}{2}\,V = M u\cos\theta \ \Rightarrow\ V = 2u\cos\theta",
                      color=IGNITION).scale(0.6).to_edge(UP, buff=1.3).shift(RIGHT*2.0)
        cap8 = caption("half the mass carries all the momentum → twice the speed", IGNITION)
        with self.voiceover(text="Watch. Before the bang, mass M carries M u cosine theta of horizontal momentum. "
                                 "One half stops, so the OTHER half must carry all of it. "
                                 "Half the mass, same momentum — so it moves at twice the speed: two u cosine theta.") as t:
            self.play(FadeIn(boom, scale=1.6), Flash(apex, color=IGNITION, flash_radius=0.9), run_time=0.9)
            self.play(Write(mom), FadeIn(cap8), run_time=min(2.2, max(1.0, t.duration-2.6)))
            self.play(Create(drop), Create(arc2), FadeIn(landdot), run_time=1.6)
            self.wait(max(0.1, t.duration - 4.7))
        diagram = VGroup(ground, dotO, arc0, apex, Hline, aplab, boom, drop, arc2, landdot)
        self.play(FadeOut(mom), FadeOut(cap8), FadeOut(diagram))

        # ================= 09 · LANDING → A true, D false =================
        set_prog(9)
        t_eq = MathTex(r"H=\tfrac{1}{2}gt^2 \ \Rightarrow\ t=\frac{u\sin\theta}{g}", color=TXT).scale(0.85)
        x_eq = MathTex(r"x = 2u\cos\theta\cdot\frac{u\sin\theta}{g} = R", color=TXT).scale(0.8)
        tot  = MathTex(r"\tfrac{R}{2} + R = \tfrac{3R}{2}\quad\Rightarrow\quad \text{(A) true}", color=IGNITION).scale(0.85)
        dno  = MathTex(r"t=\tfrac{u\sin\theta}{g}\ \neq\ \tfrac{2u\sin\theta}{g}\quad\Rightarrow\quad \text{(D) false}", color=REDX).scale(0.6)
        col  = VGroup(t_eq, x_eq, tot, dno).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(text="Now the free-fall. From height H with zero vertical speed, it falls in time u sine theta over g. "
                                 "Notice that already kills option D, which has an extra factor of two.") as t:
            self.play(Write(t_eq), run_time=min(1.9, t.duration))
            self.wait(max(0.1, t.duration - 1.9))
        with self.voiceover(text="In that time it covers a horizontal distance of exactly R.") as t:
            self.play(Write(x_eq), run_time=min(1.7, t.duration))
            self.wait(max(0.1, t.duration - 1.7))
        with self.voiceover(text="Add the R over two it already had — it lands at three R over two. Option A is correct.") as t:
            self.play(Write(tot), run_time=1.2)
            self.play(FadeIn(dno), run_time=0.7)
            self.wait(max(0.1, t.duration - 1.9))
        self.play(FadeOut(col))

        # ================= 10 · SPEED → B false =================
        set_prog(10)
        vx = MathTex(r"v_x = 2u\cos\theta,\qquad v_y = gt = u\sin\theta", color=CYAN).scale(0.75)
        vv = MathTex(r"v = u\sqrt{4\cos^2\theta + \sin^2\theta}", color=IGNITION).scale(0.9)
        no = MathTex(r"\neq\ u\sqrt{\cos^2\theta + 4\sin^2\theta}\quad\Rightarrow\quad \text{(B) false}", color=REDX).scale(0.6)
        col2 = VGroup(vx, vv, no).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(text="Its landing speed? Horizontal stays two u cosine theta; vertical builds to u sine theta.") as t:
            self.play(Write(vx), run_time=min(1.7, t.duration))
            self.wait(max(0.1, t.duration - 1.7))
        with self.voiceover(text="Combine them and you get u root four cos-squared plus sin-squared. "
                                 "Option B put the four on the wrong term — so B is false.") as t:
            self.play(Write(vv), run_time=1.3)
            self.play(FadeIn(no), run_time=0.8)
            self.wait(max(0.1, t.duration - 2.1))
        self.play(FadeOut(col2))

        # ================= 11 · CENTRE OF MASS → C true =================
        set_prog(11)
        com = VGroup(
            Text("The explosion is internal.", font=MONO, color=TXT).scale(0.5),
            Text("Only gravity acts from outside.", font=MONO, color=TXT).scale(0.5),
            MathTex(r"\Rightarrow\ \text{COM keeps the original parabola}\ \ \text{(C) true}", color=IGNITION).scale(0.6),
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(text="Finally, the centre of mass. The explosion is internal, and the only outside force is gravity. "
                                 "So the centre of mass sails along the very same parabola, as if nothing exploded. "
                                 "Option C is correct.") as t:
            self.play(FadeIn(com[0], shift=UP*0.15), run_time=1.0)
            self.play(FadeIn(com[1], shift=UP*0.15), run_time=1.0)
            self.play(Write(com[2]), run_time=1.3)
            self.wait(max(0.1, t.duration - 3.3))
        self.play(FadeOut(com))

        # ================= 12 · RECAP + ANSWER =================
        set_prog(12)
        rows = VGroup(
            Text("A   lands at 3R/2            ✓", font=MONO, color=GOOD).scale(0.5),
            Text("B   speed form wrong         ✗", font=MONO, color=REDX).scale(0.5),
            Text("C   COM on original path     ✓", font=MONO, color=GOOD).scale(0.5),
            Text("D   time has extra factor 2  ✗", font=MONO, color=REDX).scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP*0.6)
        ans = VGroup(
            Text("ANSWER", font=MONO, color=MUTED).scale(0.4),
            Text("A   and   C", font=SG, color=IGNITION, weight=BOLD).scale(0.85),
        ).arrange(DOWN, buff=0.25).next_to(rows, DOWN, buff=0.7)
        box = SurroundingRectangle(ans[1], color=IGNITION, buff=0.28, corner_radius=0.1)
        with self.voiceover(text="Let's lock it in. A and C hold. B and D don't.") as t:
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT*0.15), run_time=0.4)
            self.wait(max(0.1, t.duration - 1.6))
        with self.voiceover(text="So the correct answer is A and C. And now you know exactly why. See you next time.") as t:
            self.play(FadeIn(ans, shift=DOWN*0.2), run_time=1.0)
            self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.8))
        self.wait(0.6)
