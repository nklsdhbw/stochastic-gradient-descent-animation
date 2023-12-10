from manim import *

class Conclusion(Scene):
    def construct(self):
        summary = Text("Der Algorithmus konvergiert zum Minimum der Funktion")
        
        self.play(Write(summary))
        self.wait(2)
