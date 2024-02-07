from manim import *
import sympy as sp

class SGDMiniBatch(Scene):
    ####* Functions
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
                derivative += rf"(-2) \cdot {x} \cdot ({intercept} + {slope} \cdot {x}) \\ & +"
                calculation = (-2) * x * (intercept + slope * x)
            else:
                derivative += rf"(-2) \cdot ({intercept} + {slope} \cdot {x}) \\ & +"
                calculation = (-2) * (intercept + slope * x)
            totalResult += calculation
            simplifiedDerivative += rf"{calculation} +"
        derivative = derivative[:-1]
        simplifiedDerivative = simplifiedDerivative[:-1]
        simplifiedDerivative = simplifiedDerivative.replace("+-", "-")
        totalResultString += rf"{totalResult}"
        if wrt == "slope":
            partial1 = self.equation(result=r"\dfrac{\partial RSS}{\partial slope}", next_to=axes, next_to_direction=RIGHT, up=2, left=-0.7)
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
        self.wait(1)
        self.play(FadeTransform(partial4, partial5))
        self.wait(1)
        self.play(FadeOut(partial2), partial5.animate.next_to(partial1, RIGHT))
        self.wait(1)
        return partial1, partial5, totalResult

    def explanation(self, text, next_to, next_to_direction, wait=0, fadeOut=True):
        explanation = Tex(text,color=WHITE).scale(0.5)
        explanation.next_to(next_to, UP)
        explanation.shift(UP)
        self.play(Write(explanation))
        self.wait(wait)
        if fadeOut:
            self.play(FadeOut(explanation))
        return explanation

    def graph(self, axes, formula, title="", color=BLUE):
        x = sp.symbols('x')
        formula = sp.sympify(formula)
        function = sp.lambdify(x, formula, 'numpy')
        graph = axes.plot(function, x_range=[0, 5],color=color)

        title = Tex(title)
        title.next_to(axes, UP)
        return graph, title

    def equation(self, result, next_to, next_to_direction, align_to=None, align_to_direction=None, up=0, left=0):
        equation = MathTex(rf"{result}").scale(0.5)
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
            
        ).scale(0.5)
        # Add labels to the axes
        x_label = axes.get_x_axis_label("weight").scale(0.5)
        y_label = axes.get_y_axis_label("height").scale(0.5)
        return axes, x_label, y_label

    def dot2(self, axes, x, y):
        dot = Dot(axes.c2p(x, y), color=RED).scale(0.5)
        return dot

    def miniBatch(self):
        ###* Draw coordinate system and dots
        axes, x_label, y_label = self.drawCoordinateSystem2(x_range=[0, 5], y_range=[0, 5], size=6)
        coordinates = [(1, 2),(1.1,2),(1.1,2.1),(1.2,2.1), (4, 4.5),(4.1,4.5),(4.1,4.6),(4.2,4.6), (3, 3),(3.1,3),(3.1,3.1),(3.2,3.1)]
        dots = VGroup(*[self.dot2(axes, x, y) for x, y in coordinates])

        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        
        # Show coordinate system and dots
        self.play(Write(group))
        self.play(group.animate.shift(LEFT*3))
        #self.play(group.move_to, LEFT*3)
        self.wait(2)
        

        ####* Explanation
        explanation = self.explanation(r"Note: The strict definition of Stochastic Gradient Descent \\ is to only use 1 sample per step...", axes, UP, wait=7)
        explanation = self.explanation(r"...however, it's more common to use a small subset of data, \\ or \textbf{mini-batch}, for each step", axes, UP, wait=6)
        explanation = self.explanation(r"For example we could use \textbf{3} samples per step instead \\ of just \textbf{1}", axes, UP, fadeOut=False, wait=3)

        targetDots = [dots[0].set_color(GREEN), dots[4].set_color("GREEN"), dots[8].set_color("GREEN")]
        arrows = [Arrow(start=LEFT*2+UP*3, end=dot.get_center(), buff=0.1, color=BLUE) for dot in targetDots]
        self.play(*[GrowArrow(arrow) for arrow in arrows])
        self.wait(2)
        self.play(FadeOut(explanation))
        self.play(FadeOut(VGroup(*arrows)))
        explanation = self.explanation(r"Using a \textbf{mini-batch} for each step takes the best of \\ both worlds between using just one sample and all of the \\ data at each step", axes, UP, wait=8)
        
        explanation = self.explanation(r"Similar to using all of the data, using a \textbf{mini-batch} \\ can result in more stable estimates of the parameters \\ in fewer steps", axes, UP, wait=7)
        explanation = self.explanation(r"and like using just one sample per step, using a \textbf{mini-batch} \\ is much faster than using all of the data", axes, UP, wait=7)
        
        intercept = 0.414
        slope = 0.9082
        graph = self.graph(axes, f"{slope}*x + {intercept}", title="RSS")
        self.play(Write(graph[0]))
        explanation = self.explanation(r"In this example, using \textbf{3} samples per step we ended up with \\ the \textbf{intercept = 0.86} and the \textbf{slope = 0.68}", axes, UP, wait=9)
        explanation = self.explanation(r"Which means that the estimate for the intercept was just little closer \\ to the gold standard, \textbf{0.87}, then when we \\ used one sample and got \textbf{0.85}", axes, UP, wait=10)

        #* new data point
        newDot = self.dot2(axes, 2, 2.5)
        newDot.set_color(WHITE)
        self.play(Write(newDot))
        explanation = self.explanation(r"One cool thing about \textbf{Stochastic Gradient Descent} is \\ that when we get new data...", axes, UP, wait=5)
        newDot.set_color(YELLOW)
        self.play(Write(newDot))
        explanation = self.explanation(r"...we can easily use it to take another step for the parameter \\ estimates without having to start from scratch", axes, UP, wait=5)
        explanation = self.explanation(r"In other words, we don't have to go all the way back to the \\ initial guesses for the \textbf{slope} and \textbf{intercept} and redo everything", axes, UP, wait=8)
        originStraight = self.graph(axes, "1*x", title="")
        self.play(FadeOut(graph[0]), Write(originStraight[0]))
        self.wait(2)
        self.play(FadeOut(originStraight[0]), FadeIn(graph[0]))
        explanation = self.explanation(r"Instead, we pick up right where we let off and take \\ one more step using the new sample", axes, RIGHT, wait=5)

        explanation = self.explanation(r"So we calculate again the partial derivatives \\ but now we onply plug in the new point", axes, RIGHT, wait=0, fadeOut=False)
        # New data point
        partialSlope1, partialSlope2, totalResultSlope = self.partialDerivative([(2, 2.5)], 0.414, 0.9082, axes, "slope", next_to=axes)
        self.wait(2)
        partialIntercept1, partialIntercept2, totalResultIntercept = self.partialDerivative([(2, 2.5)], 0.414, 0.9082, axes, "intercept", next_to=partialSlope1)
        self.wait(2)
        self.play(FadeOut(explanation))

        explanation = self.explanation(r"Then we calculate the step size for the \textbf{slope} and \\ \textbf{intercept} using the new partial derivatives", axes, RIGHT, wait=0, fadeOut=False)

        stepSizeSlope = self.equation(result=r"stepSize_{Slope}", next_to=partialIntercept1, next_to_direction=DOWN, left=0)
        stepSizeSlope2 = self.equation(result = r"= \dfrac{\partial RSS}{\partial slope} \cdot learningRate", next_to=stepSizeSlope, next_to_direction=RIGHT)
        self.play(Write(stepSizeSlope))
        self.play(Write(stepSizeSlope2))

        learningRate = 0.01
        stepSizeSlope3 = self.equation(rf"= {totalResultSlope} \cdot {learningRate}", next_to=stepSizeSlope2, next_to_direction=DOWN, align_to=stepSizeSlope2, align_to_direction=LEFT)
        self.play(Write(stepSizeSlope3))

        stepSizeSlopeValue  = totalResultSlope * learningRate
        stepSizeSlope4 = self.equation(result=rf"= {stepSizeSlopeValue}", next_to=stepSizeSlope2, next_to_direction=DOWN, align_to=stepSizeSlope2, align_to_direction=LEFT)
        self.play(FadeTransform(stepSizeSlope3, stepSizeSlope4))
        self.play(FadeOut(stepSizeSlope2))
        self.play(stepSizeSlope4.animate.next_to(stepSizeSlope, RIGHT))


        stepSizeIntercept = r"stepSize_{intercept}"
        stepSizeIntercept = self.equation(result=r"{stepSizeIntercept}", next_to=stepSizeSlope, next_to_direction=DOWN, left=
                                          0.3, up=-0.5)
        stepSizeIntercept2 = self.equation(result=r"= \dfrac{\partial RSS}{\partial intercept} \cdot learningRate", next_to=stepSizeIntercept, next_to_direction=RIGHT)
        self.play(Write(stepSizeIntercept))
        self.play(Write(stepSizeIntercept2))
        
        learningRate = 0.01
        stepSizeIntercept3 = self.equation(result=rf"= {totalResultIntercept} \cdot {learningRate}", next_to=stepSizeIntercept2, next_to_direction=DOWN, align_to=stepSizeIntercept2, align_to_direction=LEFT)
        self.play(Write(stepSizeIntercept3))

        stepSizeInterceptValue = totalResultIntercept * learningRate
        stepSizeIntercept4 = self.equation(result=rf"= {stepSizeInterceptValue}", next_to=stepSizeIntercept2, next_to_direction=DOWN, align_to=stepSizeIntercept2, align_to_direction=LEFT)
        self.play(FadeTransform(stepSizeIntercept3, stepSizeIntercept4))
        self.play(FadeOut(stepSizeIntercept2))
        self.play(stepSizeIntercept4.animate.next_to(stepSizeIntercept, RIGHT))
        stepsize = [stepSizeSlope, stepSizeSlope4, stepSizeIntercept, stepSizeIntercept4]
        stepsize = VGroup(*stepsize)

        slopeGroup = VGroup(partialSlope1, partialSlope2)
        interceptGroup = VGroup(partialIntercept1, partialIntercept2)
        # New slopes and intercepts
        self.play(FadeOut(slopeGroup), FadeOut(interceptGroup))
        self.play(stepsize.animate.shift(UP*2))

        self.play(FadeOut(explanation))

        explanation = self.explanation(r"Finally, we update the \textbf{slope} and \textbf{intercept} using the \\ step sizes we just calculated", axes, RIGHT, wait=0, fadeOut=False)
        newSlope1 = self.equation(result=r"slope_{new}",next_to=stepSizeIntercept, next_to_direction=DOWN, left=-0.5)
        newSlope2 = self.equation(result=r"= slope_{old} - stepSize_{slope}", next_to=newSlope1, next_to_direction=RIGHT)
        self.play(Write(newSlope1))
        self.play(Write(newSlope2))
        newSlope3 = self.equation(result=rf"= {slope} - ({stepSizeSlopeValue})", next_to=newSlope2, next_to_direction=DOWN, align_to=newSlope2, align_to_direction=LEFT)
        self.play(Write(newSlope3))
        newSlopeValue = round(slope - stepSizeSlopeValue, 2)
        newSlope4 = self.equation(result=rf"= {newSlopeValue}", next_to=newSlope2, next_to_direction=DOWN, align_to=newSlope2, align_to_direction=LEFT)
        self.play(FadeTransform(newSlope3, newSlope4))
        self.play(FadeOut(newSlope2))
        self.play(newSlope4.animate.next_to(newSlope1, RIGHT))

        
        
        newintercept1 = self.equation(result=r"intercept_{new}", next_to=newSlope1, next_to_direction=DOWN)
        newintercept2 = self.equation(result=r"= intercept_{old} - stepSize_{intercept}", next_to=newintercept1, next_to_direction=RIGHT)
        self.play(Write(newintercept1))
        self.play(Write(newintercept2))

        newintercept3 = self.equation(result=rf"= {intercept} - ({stepSizeInterceptValue})", next_to=newintercept2, next_to_direction=DOWN, align_to=newintercept2, align_to_direction=LEFT)
        self.play(Write(newintercept3))
        newinterceptValue = round(intercept - stepSizeInterceptValue, 2)
        newintercept4 = self.equation(result=rf"= {newinterceptValue}", next_to=newintercept2, next_to_direction=DOWN, align_to=newintercept2, align_to_direction=LEFT)
        self.play(FadeTransform(newintercept3, newintercept4))
        self.play(FadeOut(newintercept2))
        self.play(newintercept4.animate.next_to(newintercept1, RIGHT))
        objects = [stepSizeIntercept, stepSizeIntercept4, stepSizeSlope, stepSizeSlope4, newSlope1, newSlope4, newintercept1, newintercept4]
        objects = VGroup(*objects)
        self.play(FadeOut(objects), FadeOut(explanation))

        explanation = self.explanation(r"And that's it! We've taken another step using the new data", axes, RIGHT, wait=0, fadeOut=False)
        self.play(FadeOut(graph[0]))
        newGraph = self.graph(axes, f"{newSlopeValue}*x + {newinterceptValue}", title="", color=RED)
        self.play(Write(newGraph[0]))
        self.play(FadeOut(explanation))
        objects = [axes, x_label, y_label, *dots, newDot, newGraph[0]]
        self.play(FadeOut(VGroup(*objects)))
        self.wait(2)
        
        summary = Tex("In Summary...")
        self.play(Write(summary))
        self.wait(2)
        self.play(FadeOut(summary))

        axes, x_label, y_label = self.drawCoordinateSystem2(x_range=[0, 5], y_range=[0, 5], size=6)
        coordinates = [(1, 2),(1.1,2),(1.1,2.1),(1.2,2.1), (4, 4.5),(4.1,4.5),(4.1,4.6),(4.2,4.6), (3, 3),(3.1,3),(3.1,3.1),(3.2,3.1)]
        dots = VGroup(*[self.dot2(axes, x, y) for x, y in coordinates])
        dots[0].set_color(GREEN)
        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        self.play(Write(group))
        explanation = self.explanation(r"\textbf{Stochastic Gradient Descent} is just like regular \textbf{Gradient Descent}, \\ except it only looks at one sample per step...", axes, UP, wait=7)
        dots[0].set_color(GREEN)
        dots[4].set_color("GREEN")
        dots[8].set_color("GREEN")
        explanation = self.explanation(r"...or a small subset, or \textbf{mini-batch}, for each step", axes, UP, wait=7)
        objects = [axes, x_label, y_label, *dots]
        self.play(FadeOut(VGroup(*objects)))

        explanation1 = self.explanation(r"\textbf{Stochastic Gradient Descent} is great when we have tons of data and a lot of parameters", axes, UP, wait=7, fadeOut=False)
        explanation2 = self.explanation(r"In these situations, regular \textbf{Gradient Descent} may not be computationally feasable", explanation1, DOWN, wait=7, fadeOut=False)
        explanations = [explanation1, explanation2]
        self.play(FadeOut(VGroup(*explanations)))
        explanation = self.explanation("And it's cool that we can easily update the parameters when new data shows up", axes, UP, wait=0, fadeOut=False)
        axes, x_label, y_label = self.drawCoordinateSystem2(x_range=[0, 5], y_range=[0, 5], size=6)
        coordinates = [(1, 2),(1.1,2),(1.1,2.1),(1.2,2.1), (4, 4.5),(4.1,4.5),(4.1,4.6),(4.2,4.6), (3, 3),(3.1,3),(3.1,3.1),(3.2,3.1), (2, 2.5)]
        dots = VGroup(*[self.dot2(axes, x, y) for x, y in coordinates])
        dots[-1].set_color("YELLOW")
        graph = self.graph(axes, f"{slope}*x + {intercept}", title="RSS")
        self.play(Write(VGroup(axes, x_label, y_label, *dots, graph[0])))
        self.wait(1)
        newGraph = self.graph(axes, f"{newSlopeValue}*x + {newinterceptValue}", title="", color=RED)
        self.play(Write(newGraph[0]))
        objects = [axes, x_label, y_label, *dots, newGraph[0], explanation, graph[0]]
        self.play(FadeOut(VGroup(*objects)))
        end = Tex("The End")
        self.play(Write(end))
        self.wait(2)
        self.play(FadeOut(end))
    def construct(self):
        self.miniBatch()