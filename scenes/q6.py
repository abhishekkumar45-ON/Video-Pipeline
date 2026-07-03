"""
Orange Nelumbo · EM Fields · Q6 — "Two Fields, One Charge"
JEE Adv 2026 P2 Q6 (multi-correct). Charge in E+gravity (phase 1), then B+gravity (phase 2).
Phase1: a=(i-10j); at 0.2s v=(1.2,0,0), y=0.2. Phase2: y=0.2-5t'^2, R=1.2/6=0.2m.  Answer: A, C.
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


class Scene_q6(VoiceoverScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_speech_service(KokoroService())

        tag  = Text("// EM FIELDS", font=MONO, color=IGNITION).scale(0.30)
        mark = Text("ORANGE NELUMBO", font=MONO, color=MUTED).scale(0.24)
        tag.to_corner(UL, buff=0.4)
        mark.next_to(tag, DOWN, aligned_edge=LEFT, buff=0.12)
        prog = Text("01 / 06", font=MONO, color=MUTED).scale(0.24).to_corner(UR, buff=0.4)
        self.add(tag, mark, prog)

        def set_prog(n):
            new = Text(f"0{n} / 06", font=MONO, color=MUTED).scale(0.24).move_to(prog)
            self.play(Transform(prog, new), run_time=0.4)

        # ---------- 01 HOOK ----------
        title = Text("TWO FIELDS, ONE CHARGE", font=MONO, color=TXT, weight=BOLD).scale(0.72)
        sub   = Text("first electric, then magnetic", font=MONO, color=MUTED).scale(0.4)
        sub.next_to(title, DOWN, buff=0.3)
        with self.voiceover(text="A tiny charged particle is launched. First it feels an electric field... "
                                 "then, part way through, the field switches to magnetic. "
                                 "Let's track it, carefully.") as t:
            self.play(Write(title), run_time=min(2.2, t.duration))
            self.play(FadeIn(sub, shift=UP*0.2), run_time=0.7)
            self.wait(max(0.1, t.duration - 2.9))
        self.play(FadeOut(title), FadeOut(sub))

        # ---------- 02 GIVEN ----------
        set_prog(2)
        given = VGroup(
            MathTex(r"q = 1\,\mu C,\quad m = 1\,\mathrm{mg}\ \Rightarrow\ q/m = 1", color=CYAN).scale(0.7),
            MathTex(r"\vec{v}_0 = (\hat{i} + 2\hat{j})\ \mathrm{m/s}", color=CYAN).scale(0.7),
            MathTex(r"0 \le t < 0.2:\ \ \vec{E}=1\hat{i},\ \ \vec{g}=-10\hat{j}", color=TXT).scale(0.7),
            MathTex(r"t \ge 0.2:\ \ \vec{E}\ \text{off},\ \ \vec{B}=6\hat{j}", color=EMBER).scale(0.7),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN)
        with self.voiceover(text="Here's what we're given. Charge over mass is one — that keeps the numbers clean. "
                                 "It starts moving with velocity i plus two j.") as t:
            self.play(Write(given[0]), run_time=1.1)
            self.play(Write(given[1]), run_time=1.0)
            self.wait(max(0.1, t.duration - 2.1))
        with self.voiceover(text="For the first fifth of a second, an electric field along x, plus gravity pulling down. "
                                 "After that — field off, and a magnetic field along y switches on.") as t:
            self.play(Write(given[2]), run_time=1.2)
            self.play(Write(given[3]), run_time=1.2)
            self.wait(max(0.1, t.duration - 2.4))
        self.play(FadeOut(given))

        # ---------- 03 PHASE 1 ----------
        set_prog(3)
        p1t = Text("PHASE 1  ·  electric + gravity", font=MONO, color=IGNITION).scale(0.4).to_edge(UP, buff=1.2)
        acc = MathTex(r"\vec{a} = \hat{i} - 10\hat{j}\ \mathrm{m/s^2}", color=TXT).scale(0.85)
        vel = MathTex(r"v_x = 1 + 1(0.2) = 1.2,\quad v_y = 2 - 10(0.2) = 0", color=TXT).scale(0.7)
        pos = MathTex(r"y = 2(0.2) - 5(0.2)^2 = 0.2\ \mathrm{m}", color=TXT).scale(0.75)
        end = MathTex(r"\text{at } t=0.2:\ \ \vec{v}=(1.2,0,0),\ \ y=0.2\,\mathrm{m}", color=IGNITION).scale(0.7)
        body = VGroup(acc, vel, pos, end).arrange(DOWN, buff=0.45).next_to(p1t, DOWN, buff=0.6)
        with self.voiceover(text="Phase one. The acceleration is i minus ten j — a push along x, gravity along minus y.") as t:
            self.play(FadeIn(p1t), Write(acc), run_time=min(1.8, t.duration))
            self.wait(max(0.1, t.duration - 1.8))
        with self.voiceover(text="After zero point two seconds: the x speed grows to one point two, "
                                 "and the y speed drops... exactly to zero.") as t:
            self.play(Write(vel), run_time=1.4)
            self.wait(max(0.1, t.duration - 1.4))
        with self.voiceover(text="And the height climbs to zero point two metres. "
                                 "So at the switch: velocity purely along x, and y equals nought point two.") as t:
            self.play(Write(pos), run_time=1.2)
            self.play(TransformFromCopy(pos, end), run_time=1.2)
            self.wait(max(0.1, t.duration - 2.4))
        self.play(FadeOut(p1t), FadeOut(acc), FadeOut(vel), FadeOut(pos),
                  end.animate.to_edge(UP, buff=1.2).set_color(MUTED).scale(0.9))

        # ---------- 04 PHASE 2 ----------
        set_prog(4)
        p2t = Text("PHASE 2  ·  magnetic + gravity", font=MONO, color=EMBER).scale(0.4).next_to(end, DOWN, buff=0.5)
        idea = Text("B along y  ->  y is free-fall,  x-z is a circle",
                    font=MONO, color=MUTED).scale(0.38).next_to(p2t, DOWN, buff=0.4)
        yf = MathTex(r"y = 0.2 - 5\,t'^2 \qquad (t' = t - 0.2)", color=CYAN).scale(0.78)
        rr = MathTex(r"\omega = \frac{qB}{m} = 6,\qquad R = \frac{v_\perp}{\omega} = \frac{1.2}{6} = 0.2\,\mathrm{m}",
                     color=IGNITION).scale(0.72)
        body2 = VGroup(yf, rr).arrange(DOWN, buff=0.55).next_to(idea, DOWN, buff=0.6)
        with self.voiceover(text="Phase two. The magnetic field points along y — so the magnetic force never touches "
                                 "the y direction. The y motion is just free fall, and the x-z motion becomes a circle.") as t:
            self.play(FadeIn(p2t), FadeIn(idea), run_time=1.3)
            self.wait(max(0.1, t.duration - 1.3))
        with self.voiceover(text="So y starts at nought point two and falls as five t-primed squared.") as t:
            self.play(Write(yf), run_time=min(1.6, t.duration))
            self.wait(max(0.1, t.duration - 1.6))
        with self.voiceover(text="The magnetic force does no work, so the in-plane speed stays one point two. "
                                 "Angular frequency is six, and the radius comes out to nought point two metres — "
                                 "twenty centimetres.") as t:
            self.play(Write(rr), run_time=min(2.0, t.duration))
            self.wait(max(0.1, t.duration - 2.0))
        self.play(FadeOut(end), FadeOut(p2t), FadeOut(idea), FadeOut(yf), FadeOut(rr))

        # ---------- 05 OPTIONS ----------
        set_prog(5)
        def row(letter, tex, ok):
            badge = Text(letter, font=MONO, color=(GOOD if ok else REDX), weight=BOLD).scale(0.5)
            body  = MathTex(tex, color=TXT).scale(0.55)
            mk    = Text("✓" if ok else "✗", color=(GOOD if ok else REDX)).scale(0.55)
            return VGroup(badge, body, mk).arrange(RIGHT, buff=0.35)
        rows = VGroup(
            row("A", r"t=0.3:\ y=0.2-5(0.1)^2=0.15\,\mathrm{m}=15\,\mathrm{cm}", True),
            row("B", r"t=0.4:\ y=0\ \Rightarrow\ \text{dist}=0,\ \text{not }10\,\mathrm{cm}", False),
            row("C", r"R=\tfrac{1.2}{6}=0.2\,\mathrm{m}=20\,\mathrm{cm}", True),
            row("D", r"y=0\ \text{at}\ t=0.4\,\mathrm{s},\ \text{not }0.35\,\mathrm{s}", False),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)
        with self.voiceover(text="Now the options. A — at t equals nought point three, y is fifteen centimetres. Correct. "
                                 "B — at nought point four, y is exactly zero, so the distance is zero, not ten. Wrong.") as t:
            self.play(FadeIn(rows[0], shift=RIGHT*0.2), run_time=0.8)
            self.play(FadeIn(rows[1], shift=RIGHT*0.2), run_time=0.8)
            self.wait(max(0.1, t.duration - 1.6))
        with self.voiceover(text="C — the radius is twenty centimetres. Correct. "
                                 "D — it returns to the plane at nought point four seconds, not nought point three five. Wrong.") as t:
            self.play(FadeIn(rows[2], shift=RIGHT*0.2), run_time=0.8)
            self.play(FadeIn(rows[3], shift=RIGHT*0.2), run_time=0.8)
            self.wait(max(0.1, t.duration - 1.6))
        self.play(FadeOut(rows))

        # ---------- 06 ANSWER ----------
        set_prog(6)
        ans = VGroup(
            Text("ANSWER", font=MONO, color=MUTED).scale(0.4),
            Text("A   and   C", font=MONO, color=IGNITION, weight=BOLD).scale(0.9),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        box = SurroundingRectangle(ans[1], color=IGNITION, buff=0.3, corner_radius=0.1)
        with self.voiceover(text="Two survive. The answer... is A and C.") as t:
            self.play(FadeIn(ans, shift=DOWN*0.2), run_time=1.0)
            self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.8))
        self.wait(0.6)
