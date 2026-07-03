"""
Orange Nelumbo · Optics · Q5 — "Two Prisms, One Mirror"
JEE Adv 2026 P2 Q5 (multi-correct). Two prisms with vertical inner faces over a mirror.
Key link: the ray reflects off the mirror so i2 = e1.  Answer: A, D.
"""
from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

BG       = "#0E0D10"
IGNITION = "#FF5A1F"
EMBER    = "#FF7A2E"
CYAN     = "#3DE0D0"
TXT      = "#E8E6EC"
MUTED    = "#8A8A93"
REDX     = "#E0483C"
GOOD     = "#3DE0D0"
MONO = "JetBrains Mono"


class Scene_q5(VoiceoverScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_speech_service(KokoroService())

        tag  = Text("// OPTICS", font=MONO, color=IGNITION).scale(0.30)
        mark = Text("ORANGE NELUMBO", font=MONO, color=MUTED).scale(0.24)
        tag.to_corner(UL, buff=0.4)
        mark.next_to(tag, DOWN, aligned_edge=LEFT, buff=0.12)
        prog = Text("01 / 06", font=MONO, color=MUTED).scale(0.24).to_corner(UR, buff=0.4)
        self.add(tag, mark, prog)

        def set_prog(n):
            new = Text(f"0{n} / 06", font=MONO, color=MUTED).scale(0.24).move_to(prog)
            self.play(Transform(prog, new), run_time=0.4)

        # ---------- 01 HOOK ----------
        title = Text("TWO PRISMS, ONE MIRROR", font=MONO, color=TXT, weight=BOLD).scale(0.7)
        sub   = Text("one link solves everything", font=MONO, color=MUTED).scale(0.4)
        sub.next_to(title, DOWN, buff=0.3)
        with self.voiceover(text="Two prisms face each other over a flat mirror. "
                                 "It looks intimidating... but there is one single link "
                                 "that unlocks the whole problem.") as t:
            self.play(Write(title), run_time=min(2.2, t.duration))
            self.play(FadeIn(sub, shift=UP*0.2), run_time=0.7)
            self.wait(max(0.1, t.duration - 2.9))
        self.play(FadeOut(title), FadeOut(sub))

        # ---------- 02 SETUP DIAGRAM ----------
        set_prog(2)
        mirror = Line(LEFT*5.2, RIGHT*5.2, color=MUTED, stroke_width=3).shift(DOWN*2.6)
        hatch = VGroup(*[
            Line(mirror.point_from_proportion(p) + DOWN*0.0,
                 mirror.point_from_proportion(p) + DOWN*0.28 + LEFT*0.18, color=MUTED, stroke_width=2)
            for p in [i/22 for i in range(1, 22)]
        ])
        mlab = Text("M", font=MONO, color=MUTED).scale(0.4).next_to(mirror.get_end(), UP, buff=0.12)

        pr1 = Polygon([-0.8, 1.7, 0], [-0.8, -0.1, 0], [-2.8, 0.8, 0],
                      color=CYAN, stroke_width=3).set_fill(CYAN, opacity=0.06)
        pr2 = Polygon([0.8, 1.7, 0], [0.8, -0.1, 0], [2.8, 0.8, 0],
                      color=EMBER, stroke_width=3).set_fill(EMBER, opacity=0.06)
        l1 = Text("1", font=MONO, color=CYAN).scale(0.45).move_to([-1.35, 0.75, 0])
        l2 = Text("2", font=MONO, color=EMBER).scale(0.45).move_to([1.35, 0.75, 0])

        ray_pts = [np.array(p) for p in [
            [-4.6, 2.1, 0], [-2.0, 1.05, 0], [-0.8, 0.45, 0],
            [0.0, -2.6, 0], [0.8, 0.45, 0], [2.0, 1.05, 0], [4.6, 2.1, 0]]]
        ray = VMobject(color=IGNITION, stroke_width=4)
        ray.set_points_as_corners(ray_pts)
        hit = Dot([0.0, -2.6, 0], color=IGNITION).scale(0.7)

        with self.voiceover(text="Here it is. Two prisms — one and two — with their inner faces vertical, "
                                 "parallel, and both standing on the mirror.") as t:
            self.play(Create(mirror), FadeIn(hatch), Write(mlab), run_time=1.3)
            self.play(Create(pr1), Create(pr2), FadeIn(l1), FadeIn(l2), run_time=1.4)
            self.wait(max(0.1, t.duration - 2.7))
        with self.voiceover(text="A ray enters prism one, leaves its inner face heading down, "
                                 "bounces off the mirror, climbs into prism two, and finally emerges. "
                                 "Follow that single orange path.") as t:
            self.play(Create(ray), run_time=min(2.6, max(1.2, t.duration - 0.8)))
            self.play(FadeIn(hit, scale=1.5), run_time=0.5)
            self.wait(max(0.1, t.duration - 3.1))
        diagram = VGroup(mirror, hatch, mlab, pr1, pr2, l1, l2, ray, hit)
        self.play(diagram.animate.scale(0.34).to_corner(DR, buff=0.4))

        # ---------- 03 PRISM RELATIONS ----------
        set_prog(3)
        r1 = MathTex(r"\sin i = n \sin r_1", color=TXT).scale(0.8)
        r2 = MathTex(r"r_1 + r_2 = A", color=TXT).scale(0.8)
        r3 = MathTex(r"n \sin r_2 = \sin e", color=TXT).scale(0.8)
        md = MathTex(r"\text{min. deviation: } r_1=r_2=\tfrac{A}{2},\ i=e,\ \sin i = n\sin\tfrac{A}{2}",
                     color=IGNITION).scale(0.62)
        col = VGroup(r1, r2, r3, md).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        col.to_edge(LEFT, buff=1.0).shift(UP*0.5)
        with self.voiceover(text="First, the standard prism rules. Snell's law at entry — sine i equals n sine r one. "
                                 "The two internal angles add to the prism angle A. And at exit, n sine r two equals sine e.") as t:
            self.play(Write(r1), run_time=1.0)
            self.play(Write(r2), run_time=0.9)
            self.play(Write(r3), run_time=1.0)
            self.wait(max(0.1, t.duration - 2.9))
        with self.voiceover(text="At minimum deviation the ray is symmetric — r one equals r two equals A over two, "
                                 "i equals e, and sine i equals n sine of A over two. Remember that one.") as t:
            self.play(Write(md), run_time=min(2.2, t.duration))
            self.wait(max(0.1, t.duration - 2.2))
        self.play(FadeOut(col))

        # ---------- 04 THE KEY LINK ----------
        set_prog(4)
        klbl = Text("THE ONE LINK", font=MONO, color=IGNITION).scale(0.44).to_edge(UP, buff=1.2)
        link = MathTex(r"i_2 = e_1", color=IGNITION).scale(1.5)
        why  = Text("ray exits prism 1 at e1 -> reflects off M -> hits prism 2 at i2 = e1",
                    font=MONO, color=MUTED).scale(0.34)
        grp = VGroup(link, why).arrange(DOWN, buff=0.5).next_to(klbl, DOWN, buff=0.7)
        with self.voiceover(text="Here is the key. The ray leaves prism one at angle e one. "
                                 "It reflects off the mirror — the reflection just flips it upward, keeping the angle. "
                                 "So when it strikes prism two, the angle of incidence i two... equals e one.") as t:
            self.play(FadeIn(klbl), run_time=0.6)
            self.play(Write(link), run_time=1.2)
            self.play(Flash(link, color=IGNITION, flash_radius=1.4), run_time=0.8)
            self.wait(max(0.1, t.duration - 2.6))
        with self.voiceover(text="This holds for every ray, whatever the prisms are doing. It's pure geometry.") as t:
            self.play(FadeIn(why), run_time=1.0)
            self.wait(max(0.1, t.duration - 1.0))
        self.play(FadeOut(klbl), FadeOut(grp), FadeOut(diagram))

        # ---------- 05 OPTIONS ----------
        set_prog(5)
        def row(letter, tex, ok):
            badge = Text(letter, font=MONO, color=(GOOD if ok else REDX), weight=BOLD).scale(0.5)
            body  = MathTex(tex, color=TXT).scale(0.55)
            mk    = Text("✓" if ok else "✗", color=(GOOD if ok else REDX)).scale(0.55)
            return VGroup(badge, body, mk).arrange(RIGHT, buff=0.35)
        rows = VGroup(
            row("A", r"\text{both min. dev}\Rightarrow \tfrac{n_2}{n_1}=\tfrac{\sin(A_1/2)}{\sin(A_2/2)}", True),
            row("B", r"\sin i_1 = n_2\sin(A_2/2)\ \text{ not always true}", False),
            row("C", r"\theta=\tfrac{1}{2}\big[\ldots\big]\ \text{ off by a factor of 2}", False),
            row("D", r"\text{prism 1 min. dev}\Rightarrow \sin i_2 = n_1\sin(A_1/2)", True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)
        with self.voiceover(text="Now the options. A — both prisms at minimum deviation. Then i one equals i two, "
                                 "and the index ratio equals the ratio of those half-angle sines. Correct.") as t:
            self.play(FadeIn(rows[0], shift=RIGHT*0.2), run_time=0.9)
            self.wait(max(0.1, t.duration - 0.9))
        with self.voiceover(text="B ties sine i one to prism two — but that only works if prism one is also symmetric, "
                                 "which isn't given. Wrong. C has the apex angle right in form, "
                                 "but carries an extra one-half — off by a factor of two. Wrong.") as t:
            self.play(FadeIn(rows[1], shift=RIGHT*0.2), run_time=0.9)
            self.play(FadeIn(rows[2], shift=RIGHT*0.2), run_time=0.9)
            self.wait(max(0.1, t.duration - 1.8))
        with self.voiceover(text="D — prism one at minimum deviation gives sine i one equals n one sine A one over two. "
                                 "And since i two equals e one equals i one, sine i two equals that too. Correct.") as t:
            self.play(FadeIn(rows[3], shift=RIGHT*0.2), run_time=0.9)
            self.wait(max(0.1, t.duration - 0.9))
        self.play(FadeOut(rows))

        # ---------- 06 ANSWER ----------
        set_prog(6)
        ans = VGroup(
            Text("ANSWER", font=MONO, color=MUTED).scale(0.4),
            Text("A   and   D", font=MONO, color=IGNITION, weight=BOLD).scale(0.9),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        box = SurroundingRectangle(ans[1], color=IGNITION, buff=0.3, corner_radius=0.1)
        with self.voiceover(text="One link did all the work. The answer... is A and D.") as t:
            self.play(FadeIn(ans, shift=DOWN*0.2), run_time=1.0)
            self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.8))
        self.wait(0.6)
