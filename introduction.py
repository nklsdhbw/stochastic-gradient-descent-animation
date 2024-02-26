from manim import *

class Introduction(Scene):
    def construct(self):
        # Texts
        title = Tex("Unveiling (Stochstic) Gradient Descent").scale(0.7)
        intro_text = Tex(r"""In the realm of machine learning, Gradient Descent and \\Stochastic Gradient Descent
                         are frequently employed to optimize models. You've probably heard \\these terms before, 
                         but what exactly do they entail? Today, we delve into the \\ depths of these concepts 
                         to uncover their mysteries.""").scale(0.5)
        
        title.move_to(UP*2)

        intro_text.move_to(DOWN)

        self.play(Write(title))

        self.wait(1)
        self.play(Write(intro_text))
        self.wait(2)
