from manim import *
import sympy as sp

class SGDMiniBatch(Scene):
    ####* Functions

    def explanation(self, text, next_to, next_to_direction, wait=0, fadeOut=True):
        explanation = Tex(text,color=WHITE).scale(0.5)
        explanation.next_to(next_to, next_to_direction)
        self.play(Write(explanation))
        if fadeOut:
            self.play(FadeOut(explanation))
        return explanation

    def graph(self, axes, formula, title=""):
        x = sp.symbols('x')
        formula = sp.sympify(formula)
        function = sp.lambdify(x, formula, 'numpy')
        graph = axes.plot(function, x_range=[0, 5],color=BLUE)

        title = Tex(title)
        title.next_to(axes, UP)
        return graph, title

    def equation(self, result, next_to, next_to_direction, align_to=None, align_to_direction=None, up=0, left=0):
        equation = MathTex(rf"{result}")
        equation.next_to(next_to, next_to_direction)
        if align_to != None:
            equation.align_to(align_to, align_to_direction)
        equation.shift(UP*up)
        equation.shift(LEFT*left)
        return equation

    def drawCoordinateSystem2(self, x_range, y_range, size):
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={"color": WHITE,},
            x_length = size,
            y_length = size,
            
        )
        # Add labels to the axes
        x_label = axes.get_x_axis_label("weight")
        y_label = axes.get_y_axis_label("height")
        return axes, x_label, y_label

    def dot2(self, axes, x, y):
        dot = Dot(axes.c2p(x, y), color=RED)
        return dot

    def miniBatch(self):
        ###* Draw coordinate system and dots
        axes, x_label, y_label = self.drawCoordinateSystem2(x_range=[0, 5], y_range=[0, 5], size=6)
        coordinates = [(1, 2),(1.1,2),(1.1,2.1),(1.2,2.1), (4, 4.5),(4.1,4.5),(4.1,4.6),(4.2,4.6), (3, 3),(3.1,3),(3.1,3.1),(3.2,3.1)]
        dots = VGroup(*[self.dot2(axes, x, y) for x, y in coordinates])

        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        group.scale(0.6)
        
        # Show coordinate system and dots
        self.play(Write(group))
        self.play(group.animate.shift(DOWN, LEFT*3))
        self.wait(2)
        

        ####* Explanation
        explanation = self.explanation(r"Note: The strict definition of Stochastic Gradient Descent \\ is to only use 1 sample per step...", axes, RIGHT, 2)
        explanation = self.explanation(r"...however, it's more common to use a small subset of data, \\ or \textbf{mini-batch}, for each step", axes, RIGHT, 2)
        explanation = self.explanation(r"For example we could use \textbf{3} samples per step instead \\ of just \textbf{1}", axes, RIGHT, fadeOut=False)

        targetDots = [dots[0].set_color(GREEN), dots[4].set_color("GREEN"), dots[8].set_color("GREEN")]
        arrows = [Arrow(start=DOWN+LEFT*0.6+UP*0.1, end=dot.get_center(), buff=0.1, color=BLUE) for dot in targetDots]
        self.play(*[GrowArrow(arrow) for arrow in arrows])
        self.wait(2)
        self.play(FadeOut(explanation))

        explanation = self.explanation(r"Using a \textbf{mini-batch} for each step takes the best of \\ both worlds between using just one sample and all of the \\ data at each step", axes, RIGHT, 2)
        self.play(FadeOut(VGroup(*arrows)))
        explanation = self.explanation(r"Similar to using all of the data, uisng a \textbf{mini-batch} \\ can result in more stable estimates of the parameters \\ in fewer steps", axes, RIGHT, 2)
        explanation = self.explanation(r"and like using just one sample per step, using a \textbf{mini-batch} \\ is much faster than using all of the data", axes, RIGHT, 2)
        
        graph = self.graph(axes, "0.68*x + 0.86", title="RSS")
        self.play(Write(graph[0]))
        explanation = self.explanation(r"In this example, using \textbf{3} samples per step we ended up with \\ the \textbf{intercept = 0.86} and the \textbf{slope = 0.68}", axes, RIGHT, 2)
        explanation = self.explanation(r"Which means that the estimate for the intercept was just little closer \\ to the gold standard, \textbf{0.87}, then when we \\ used one sample and got \textbf{0.85}", axes, RIGHT, 2)

        #* new data point
        newDot = self.dot2(axes, 2, 2.5)
        newDot.set_color(WHITE)
        self.play(Write(newDot))
        explanation = self.explanation(r"One cool thing about \textbf{Stochastic Gradient Descent} is \\ that when we get new data...", axes, RIGHT, 2)
        newDot.set_color(YELLOW)
        self.play(Write(newDot))
        explanation = self.explanation(r"...we can easily use it to take another step for the parameter \\ estimates without having to start from scratch", axes, RIGHT, 2)
        explanation = self.explanation(r"In other words, we don't have to go all the way back to the \\ initial guesses for the \textbf{slope} and \textbf{intercept} and redo everything", axes, RIGHT, 2)
        originStraight = self.graph(axes, "1*x", title="")
        self.play(FadeOut(graph[0]), Write(originStraight[0]))
        self.wait(2)
        self.play(FadeOut(originStraight[0]), FadeIn(graph[0]))
        explanation = self.explanation(r"Instead, we pick up right where we let off and take \\ one more step using the new sample", axes, RIGHT, 2)

    def construct(self):
        self.miniBatch()