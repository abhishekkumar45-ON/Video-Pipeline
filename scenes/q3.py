"""
Orange Nelumbo · Kinematics · Q3 — "The Drop"
A stone dropped from a 45 m building; time to reach the ground.
h = 1/2 g t^2 -> 45 = 5 t^2 -> t = 3 s.   Answer: (B) 3 s.

Narrated via offline Kokoro (af_nova, teaching pace). Renders via batch_render / orchestrator.
"""

from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

# ---------- brand tokens ----------
BG       = "#0E0D10"
IGNITION = "#FF5A1F"   # orange — the concept in focus
EMBER    = "#FF7A2E"
CYAN     = "#3DE0D0"   # velocity cyan — motion, vectors & data
CARBON   = "#1E1B20"
TXT      = "#E8E6EC"
MUTED    = "#8A8A93"

MONO = "JetBrains Mono"


class Scene_q3(VoiceoverScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_speech_service(KokoroService())   # af_nova — teaching voice

        # ---------------- persistent chrome ----------------
        tag  = Text("// KINEMATICS", font=MONO, color=IGNITION).scale(0.32)
        mark = Text("ORANGE NELUMBO", font=MONO, color=MUTED).scale(0.26)
        tag.to_corner(UL, buff=0.4)
        mark.next_to(tag, DOWN, aligned_edge=LEFT, buff=0.12)
        prog = Text("01 / 06", font=MONO, color=MUTED).scale(0.26).to_corner(UR, buff=0.4)
        self.add(tag, mark, prog)

        def set_prog(n):
            new = Text(f"0{n} / 06", font=MONO, color=MUTED).scale(0.26).move_to(prog)
            self.play(Transform(prog, new), run_time=0.4)

        # ================= 01 — HOOK =================
        title = Text("THE DROP", font=MONO, color=TXT, weight=BOLD).scale(1.1)
        sub   = Text("forty-five metres, straight down",
                     font=MONO, color=MUTED).scale(0.4).next_to(title, DOWN, buff=0.3)
        with self.voiceover(text="A stone is let go... from the top of a tall building. "
                                 "No push, no throw — just released. The question is simple: "
                                 "how long... before it hits the ground?") as t:
            self.play(Write(title), run_time=min(2.0, t.duration))
            self.play(FadeIn(sub, shift=UP*0.2), run_time=0.8)
            self.wait(max(0.1, t.duration - 2.8))
        self.play(FadeOut(title), FadeOut(sub))

        # ================= 02 — SETUP =================
        set_prog(2)
        ground = Line(LEFT*6, RIGHT*6, color=MUTED).shift(DOWN*3.2)
        building = Rectangle(width=1.4, height=5.6, color=MUTED, fill_color=CARBON,
                             fill_opacity=1.0).next_to(ground, UP, buff=0).shift(LEFT*3.8)
        stone = Dot(color=CYAN).scale(1.4).move_to(building.get_top())
        brace = BraceBetweenPoints(building.get_top()+LEFT*1.1,
                                   building.get_bottom()+LEFT*1.1, LEFT, color=MUTED)
        hlab  = MathTex(r"h = 45\,\mathrm{m}", color=CYAN).scale(0.7).next_to(brace, LEFT, buff=0.15)

        givens = VGroup(
            MathTex(r"u = 0", color=CYAN).scale(0.85),
            MathTex(r"g = 10\,\mathrm{m/s^2}", color=CYAN).scale(0.85),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=1.6).shift(UP*0.6)

        with self.voiceover(text="Here's the setup. A building, forty-five metres tall. "
                                 "The stone starts at the very top... at rest. "
                                 "So its initial speed — is zero.") as t:
            self.play(Create(ground), FadeIn(building, shift=UP*0.2), run_time=1.2)
            self.play(GrowFromCenter(stone), FadeIn(brace), Write(hlab), run_time=1.0)
            self.play(Write(givens[0]), run_time=0.8)
            self.wait(max(0.1, t.duration - 3.0))
        with self.voiceover(text="And gravity pulls it down... at ten metres per second, squared.") as t:
            self.play(Write(givens[1]), run_time=1.0)
            self.wait(max(0.1, t.duration - 1.0))

        # ================= 03 — FORMULA =================
        set_prog(3)
        gen = MathTex(r"h = ut + \tfrac{1}{2} g t^2", color=MUTED).scale(0.9)
        red = MathTex(r"h = \tfrac{1}{2} g t^2", color=TXT).scale(1.0)
        VGroup(gen, red).arrange(DOWN, buff=0.5).to_edge(UP, buff=1.4).shift(RIGHT*2.2)

        with self.voiceover(text="Now, the distance fallen under gravity — "
                                 "u t plus one half g t squared.") as t:
            self.play(Write(gen), run_time=min(1.8, t.duration))
            self.wait(max(0.1, t.duration - 1.8))
        with self.voiceover(text="But watch — u is zero. So that first term... simply vanishes. "
                                 "We're left with h equals one half g t squared.") as t:
            self.play(TransformFromCopy(gen, red), run_time=min(1.8, t.duration))
            self.wait(max(0.1, t.duration - 1.8))

        # ================= 04 — SUBSTITUTE =================
        set_prog(4)
        # clear the setup labels now that their numbers live inside the equations,
        # so nothing lingers to overlap later beats (the answer, the roots).
        self.play(FadeOut(givens), FadeOut(brace), FadeOut(hlab))
        s1 = MathTex(r"45 = \tfrac{1}{2}(10)\,t^2", color=IGNITION).scale(1.0)
        s2 = MathTex(r"45 = 5\,t^2", color=IGNITION).scale(1.0)
        s3 = MathTex(r"t^2 = 9", color=IGNITION).scale(1.1)
        VGroup(s1, s2, s3).arrange(DOWN, buff=0.5).shift(DOWN*0.3+RIGHT*2.2)

        with self.voiceover(text="Put the numbers in. Forty-five equals one half, times ten, times t squared.") as t:
            self.play(Write(s1), run_time=min(1.8, t.duration))
            self.wait(max(0.1, t.duration - 1.8))
        with self.voiceover(text="One half of ten is five. So — forty-five equals five t squared.") as t:
            self.play(TransformFromCopy(s1, s2), run_time=min(1.6, t.duration))
            self.wait(max(0.1, t.duration - 1.6))
        with self.voiceover(text="Divide both sides by five... and t squared is nine.") as t:
            self.play(TransformFromCopy(s2, s3), run_time=min(1.6, t.duration))
            self.wait(max(0.1, t.duration - 1.6))
        self.play(FadeOut(gen), FadeOut(red), FadeOut(s1), FadeOut(s2),
                  s3.animate.to_edge(UP, buff=1.3).shift(LEFT*2.2))

        # ================= 05 — SOLVE =================
        set_prog(5)
        root = MathTex(r"t = \sqrt{9} = 3\,\mathrm{s}", color=TXT).scale(1.1).next_to(s3, DOWN, buff=0.7).shift(RIGHT*2.2)
        rej  = Text("(t = -3 s rejected — time can't be negative)",
                    font=MONO, color=MUTED).scale(0.35).next_to(root, DOWN, buff=0.35)
        with self.voiceover(text="Take the square root — t is three. "
                                 "The negative root? We throw it away... time doesn't run backwards.") as t:
            self.play(Write(root), run_time=min(1.6, t.duration))
            self.play(FadeIn(rej), run_time=0.6)
            self.wait(max(0.1, t.duration - 2.2))
        self.play(FadeOut(s3), FadeOut(root), FadeOut(rej))

        # ================= 06 — PAYOFF: the fall + answer =================
        set_prog(6)
        with self.voiceover(text="Let's watch it happen. Three seconds... top to ground.") as t:
            self.play(stone.animate.move_to(building.get_bottom()),
                      run_time=min(2.4, max(1.0, t.duration - 0.4)),
                      rate_func=rate_functions.ease_in_quad)
            self.play(Flash(stone, color=CYAN, flash_radius=0.7), run_time=0.6)
            self.wait(max(0.1, t.duration - 3.0))

        ans = VGroup(
            Text("ANSWER", font=MONO, color=MUTED).scale(0.4),
            Text("(B)  3 seconds", font=MONO, color=IGNITION, weight=BOLD).scale(0.62),
        ).arrange(DOWN, buff=0.2).to_edge(RIGHT, buff=1.4).shift(UP*0.4)
        box = SurroundingRectangle(ans[1], color=IGNITION, buff=0.25, corner_radius=0.1)
        with self.voiceover(text="So there it is. The stone hits the ground in exactly three seconds. "
                                 "The answer... is B.") as t:
            self.play(FadeIn(ans, shift=DOWN*0.2), run_time=1.0)
            self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.8))
        self.wait(0.6)
