from manim import *
import sympy as sp

class SGD(Scene):
    ####* Functions
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
    
    def partialDerivative(self, coordinates, intercept, slope, axes, wrt, next_to=None):
        derivative = r"&"
        simplifiedDerivative = r"&"
        totalResult = 0
        totalResultString = r"="
        for cords in coordinates:
            if cords == coordinates[0]:
                derivative += r"="
                simplifiedDerivative += r"="
            x, y = cords
            if wrt == "slope":
                derivative += rf"(-2) \cdot {x} \cdot ({y} - ({intercept} + {slope} \cdot {x}) \\ & +"
                calculation = round((-2) * x * (y - (intercept + slope * x)),2)
            else:
                derivative += rf"(-2) \cdot ({y} - ({intercept} + {slope} \cdot {x})) \\ & +"
                calculation = round((-2) * (y - (intercept + slope * x)), 2)
            totalResult += calculation
            simplifiedDerivative += rf"{calculation} +"
        derivative = derivative[:-1]
        simplifiedDerivative = simplifiedDerivative[:-1]
        simplifiedDerivative = simplifiedDerivative.replace("+-", "-")
        totalResultString += rf"{totalResult}"
        if wrt == "slope":
            partial1 = self.equation(result=r"\dfrac{\partial RSS}{\partial slope}", next_to=axes, next_to_direction=RIGHT, up=2, left=0.7)
            partial2 = self.equation(result=r"& = -2 \sum_{i=1}^{n} x_i(y_i - \hat{y}_i) \\ &", next_to=partial1, next_to_direction=RIGHT)
        else:
            partial1 = self.equation(result=r"\dfrac{\partial RSS}{\partial intercept}", next_to=next_to, next_to_direction=DOWN)
            partial2 = self.equation(result=r"= -2 \sum_{i=1}^{n} (y_i - \hat{y}_i) \\ &", next_to=partial1, next_to_direction=RIGHT)
        partial3 = self.equation(result=derivative, next_to=partial2, next_to_direction=DOWN, align_to=partial2, align_to_direction=LEFT)
        partial4 = self.equation(result=simplifiedDerivative, next_to=partial2, next_to_direction=DOWN, align_to=partial3, align_to_direction=LEFT)
        partial5 = self.equation(result=totalResultString, next_to=partial2, next_to_direction=DOWN, align_to=partial4, align_to_direction=LEFT)
        # Remove last plus sign
        self.play(Write(partial1))
        
        self.play(Write(partial2))
        self.play(Write(partial3))
        self.wait(3)
        
        self.play(FadeTransform(partial3, partial4))
        self.wait(2)
        self.play(FadeTransform(partial4, partial5))
        self.wait()
        self.play(FadeOut(partial2), partial5.animate.next_to(partial1, RIGHT))
        self.wait(2)
        return partial1, partial5, totalResult


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

    def example2(self):
        axes, x_label, y_label = self.drawCoordinateSystem2(x_range=[0, 5], y_range=[0, 5], size=6)

        # Create dots
        dots = VGroup()
        coordinates = [(1, 2),(1.1,2),(1.1,2.1),(1.2,2.1), (4, 4.5),(4.1,4.5),(4.1,4.6),(4.2,4.6), (3, 3),(3.1,3),(3.1,3.1),(3.2,3.1)]
        for x, y in coordinates:
            dots.add(self.dot2(axes, x, y))
        
        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        group.scale(0.6)
        
        # Show coordinate system and dots
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Write(dots))
        

        self.play(group.animate.shift(DOWN, LEFT*3))
        self.wait(2)

        self.wait(2)
        self.wait(2)
        explanation = Tex(r"Note: The strict definition of Stochastic Gradient Descent is to only use 1 sample per step...", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(explanation))
        explanation = Tex(r"...however, it's more common to use a small subset of data, or \textbf{mini-batch}, for each step", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(explanation))
        explanation = Tex(r"For example we could use \textbf{3} samples per step instead of just \textbf{1}", color=WHITE).scale(0.5)
        targetDots = [dots[0], dots[4], dots[8]]
        arrows = []
        for dot in targetDots:
            dot.set_color(GREEN)
            arrow = Arrow(start=2*UP+2*LEFT, end=dot.get_center(), buff=0.1, color=BLUE)
            arrows.append(arrow)
            self.play(GrowArrow(arrow))


        self.wait(2)
        self.play(FadeOut(explanation))
        explanation = Tex(r"Using a \textbf{mini-batch} for each step takes the best of both worlds between using just one sample and all of the data at each step", color=WHITE).scale(0.5)
        # Fade out all arrows
        self.play(FadeOut(arrows[0]), FadeOut(arrows[1]), FadeOut(arrows[2]))
        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(explanation))
        explanation = Tex(r"Similar to using all of the data, uisng a \textbf{mini-batch} can result in more stable estimates of the parameters in fewer steps", color=WHITE).scale(0.5)
        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(explanation))
        explanation = Tex(r"and like using just one sample per step, using a \textbf{mini-batch} is much faster than using all of the data", color=WHITE).scale(0.5)
        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(explanation))
        
        graph = self.graph(axes, "0.68*x + 0.86", title="RSS")
        explanation = Tex(r"In this example, using \textbf{3} samples per step we ended up with the \textbf{intercept = 0.86} and the \textbf{slope = 0.68}", color=WHITE).scale(0.5)
        self.play(Write(graph[0]), Write(explanation))
        self.wait(2)
        self.play(FadeOut(explanation))
        explanation = Tex(r"Which means that the estimate for the intercept was just little closer to the gold standard, \textbf{0.87}, then when we used one sample and got \textbf{0.85}", color=WHITE).scale(0.5)
        self.play(Write(explanation))
        self.wait(2)

    def construct(self):
        self.example2()