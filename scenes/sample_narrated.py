from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService


class SampleNarrated(VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService())

        title = Text("Projectile: maximum height", font_size=42).to_edge(UP)
        with self.voiceover(text="A ball is thrown straight up at twenty meters per second.") as t:
            self.play(Write(title), run_time=t.duration)

        eq = MathTex(r"H = \frac{u^2}{2g}", font_size=54)
        with self.voiceover(text="The maximum height equals u squared over two g.") as t:
            self.play(Write(eq), run_time=t.duration)

        ans = MathTex(r"H = \frac{20^2}{2 \times 10} = 20\ \text{m}",
                      font_size=48).next_to(eq, DOWN, buff=0.8)
        with self.voiceover(text="Substituting the values, the height is twenty meters.") as t:
            self.play(Write(ans), run_time=t.duration)

        self.wait(0.5)
