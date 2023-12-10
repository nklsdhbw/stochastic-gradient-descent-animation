from manim import *

class Introduction(Scene):
    def construct(self):
        title = Text("Stochastic Gradient Descent Visualization")
        description = Text(
            "Visualizing the process of Stochastic Gradient Descent", 
            font_size=24
        ).next_to(title, DOWN)

        self.play(Write(title))
        self.play(Write(description))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(description))