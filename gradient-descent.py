from manim import Create, Write, FadeIn, Axes, UP, Tex, WHITE, GREEN, Scene, Dot, DashedLine, YELLOW, RED, BLUE, DOWN, LEFT, VGroup, RIGHT, FadeOut, MathTex, Transform, FadeTransform, ReplacementTransform, Arrow
import sympy as sp

class Visualize(Scene):
    ####* Functions
    def linearFunctionText(self, slope, intercept, next_to):
        linearFunction1 = MathTex("y").scale(0.5)
        linearFunction2 = MathTex("= slope \cdot x + intercept").scale(0.5)
        linearFunction3 = MathTex(f"= {slope} \cdot x + {intercept}").scale(0.5)
        linearFunction1.next_to(next_to, RIGHT)
        #linearFunction1.align_to(next_to, LEFT)
        linearFunction2.next_to(linearFunction1, RIGHT)
        linearFunction3.next_to(linearFunction2, DOWN)
        linearFunction3.align_to(linearFunction2, LEFT)
        self.play(Write(linearFunction1))
        self.play(Write(linearFunction2))
        self.play(Write(linearFunction3))
        self.play(FadeOut(linearFunction2), linearFunction3.animate.align_to(linearFunction1, UP))
        return linearFunction1, linearFunction3

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
            partial1 = self.equation(result=r"\dfrac{\partial RSS}{\partial slope}", next_to=axes, next_to_direction=RIGHT, up=2, left=0.7)
            partial1.shift(RIGHT)
            partial2 = self.equation(result=r"& = -2 \sum_{i=1}^{n} x_i(y_i - \hat{y}_i) \\ &", next_to=partial1, next_to_direction=RIGHT)
        else:
            partial1 = self.equation(result=r"\dfrac{\partial RSS}{\partial intercept}", next_to=next_to, next_to_direction=DOWN)
            partial1.align_to(next_to, LEFT)
            partial1.shift(LEFT*0.5)
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

    def RSS(self, coordinates, newCoordinates, next_to, next_to_direction, up=0, left=0):
        RSS1 = self.equation(result="RSS", next_to=next_to, next_to_direction=next_to_direction, up=up, left=left)
        RSS1.shift(DOWN)
        RSS1.shift(RIGHT)
        RSS2 = self.equation(r"= \sum_{i=1}^{n} (y_i - \hat{y}_i)^2", next_to=RSS1, next_to_direction=RIGHT)
        self.play(Write(RSS1))
        self.play(Write(RSS2))
        self.wait(2)
        RSS3 = "="
        RSS4 = "="
        totalResult = 0
        for cords, newCords in zip(coordinates, newCoordinates):
            x, y = cords
            x2, y_hat = newCords
            y_hat = round(y_hat, 2)
            RSS3 += rf"({y} - {y_hat})^2  \\ +"
            result = round((y - y_hat)**2, 2)
            RSS4 += rf"{result} +"
            totalResult += result
        # Remove last plus sign
        RSS3 = RSS3[:-1]
        RSS4 = RSS4[:-1]
        RSS3 = self.equation(result=rf"{RSS3}", next_to=RSS2, next_to_direction=DOWN, align_to=RSS2, align_to_direction=LEFT)
        RSS4 = self.equation(result=rf"{RSS4}", next_to=RSS2, next_to_direction=DOWN, align_to=RSS2, align_to_direction=LEFT)
        self.play(Write(RSS3))
        self.play(FadeTransform(RSS3, RSS4))
        RSS5 = self.equation(result=rf"= {totalResult}", next_to=RSS2, next_to_direction=DOWN, align_to=RSS2, align_to_direction=LEFT)
        self.play(FadeTransform(RSS4, RSS5))
        self.wait(2)
        self.play(FadeOut(RSS2), RSS5.animate.next_to(RSS1, RIGHT))
        #self.play(FadeOut(RSS1), FadeOut(RSS5))
        return RSS1, RSS5

    def explanation(self, text, next_to, next_to_direction, wait=0, fadeOut=True):
        explanation = Tex(text,color=WHITE).scale(0.5)
        explanation.next_to(next_to, UP)
        explanation.shift(UP)
        self.play(Write(explanation))
        self.wait(wait)
        if fadeOut:
            self.play(FadeOut(explanation))
        return explanation

    def drawCoordinateSystem(self, x_range, y_range, size):
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={"color": WHITE,},
            x_length = size,
            y_length = size,
            
        ).scale(0.5)
        # Add labels to the axes
        x_label = axes.get_x_axis_label("Weight").scale(0.5)
        y_label = axes.get_y_axis_label("Height").scale(0.5)
        return axes, x_label, y_label
    
    def drawLoss(self, dots, coordinates, axes, slope, intercept):
        perpendicular_slope = -1 / slope
        newDots = {}
        newDotsCoordinates = []
        for dot_obj, cords in zip(dots, coordinates):
            # y = mx + b
            x, y = cords
            b = y - x*(perpendicular_slope)
            
            m1, b1 = (slope, intercept)
            m2, b2 = (perpendicular_slope, b)
            x_value = (b2 - b1) / (m1 - m2)
            y_value = m2 * x_value + b2
            new_dot = self.dot(axes, x_value, y_value)
            newDots[dot_obj] = new_dot
            newDotsCoordinates.append((x_value, y_value))

        # Draw loss function lines
        connections = {}
        for dot_obj, new_dot in newDots.items():
            connections[dot_obj] = DashedLine(dot_obj.get_center(), new_dot.get_center(), color=RED)

        for connection in connections.values():
            self.play(Write(connection))
        return newDots, connections, newDotsCoordinates

    def equation(self, result, next_to, next_to_direction, align_to=None, align_to_direction=None, up=0, left=0):
        equation = MathTex(rf"{result}").scale(0.5)
        equation.next_to(next_to, next_to_direction)
        if align_to != None:
            equation.align_to(align_to, align_to_direction)
        equation.shift(UP*up)
        equation.shift(LEFT*left)
        return equation

    def graph(self, axes, formula, title=""):
        x = sp.symbols('x')
        formula = sp.sympify(formula)
        function = sp.lambdify(x, formula, 'numpy')
        graph = axes.plot(function, x_range=[0, 3.1],color=BLUE)

        title = Tex(title)
        title.next_to(axes, UP)
        return graph, title
    
    def dot(self, axes, x, y):
        dot = Dot(axes.c2p(x, y), color=RED)
        return dot

    ####* Construct
    def construct(self):
        title = Tex("Gradient Descent")
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        self.wait(2)

        # Create axes
        axes, x_label, y_label = self.drawCoordinateSystem(x_range=[0, 5], y_range=[0, 5], size=6)

        # Create a dots
        dots = []
        coordinates = [(1, 2), (2, 4), (2.5, 3)]
        for x, y in coordinates:
            dots.append(self.dot(axes, x, y))

        # Show coordinate system and dots
        group = VGroup(axes, x_label, y_label)
        self.play(Write(group))
        self.wait(2)
        for dot in dots:
            self.play(Write(dot))
        self.wait(2)

        group = VGroup(axes, x_label, y_label, *dots)
        # Move coordinate system to the left all at the same time
        self.play(group.animate.shift(LEFT*3))
        self.wait(3)

        explanation = self.explanation(r"So let's start with a simple dataset", next_to=group, next_to_direction=UP, wait=3)
        explanation = self.explanation(r"We have \textbf{Height} and \textbf{Weight} measurements \\ from three different people", next_to=axes, next_to_direction=UP, wait=3)
        explanation = self.explanation(r"And we want to find the best fitting line", next_to=axes, next_to_direction=UP, wait=3)
        explanation = self.explanation(r"We start with this generic equation for a line", next_to=axes, next_to_direction=UP, wait=3)
        eq1 = MathTex(r"\textbf{Predicted Height} = slope \times \textbf{Weight}}").scale(0.5).next_to(axes, RIGHT)
        self.play(Write(eq1))
        explanation = self.explanation(r"And the goal is to find the optimal values \\ for the \textbf{intercept} and \textbf{slope}", next_to=axes, next_to_direction=UP, wait=3)
        self.play(FadeOut(eq1))
        explanation = self.explanation(r"For example, if we started with the \\ \textbf{intercept = 0} and the \textbf{slope = 1}...", next_to=axes, next_to_direction=UP, wait=3)
        # Create regression line
        slope = 1.5
        intercept = 0
        line, linetitle = self.graph(axes, f"{slope}*x + {intercept}")

        # Show linear function equation
        function, function3 = self.linearFunctionText(slope, intercept, next_to=line)
        # Show regression line
        self.wait(3)
        self.play(Write(line), Write(linetitle))
        self.play(FadeOut(function), FadeOut(function3))

        explanation = self.explanation(r"...then we could use \textbf{Weight}...", next_to=axes, next_to_direction=UP, wait=3)
        explanation = self.explanation(r"...to predict \textbf{Height}", next_to=axes, next_to_direction=UP, wait=3)
        
        # Create orthogonal lines
        newDots, connections, newDotsCoordinates = self.drawLoss(dots, coordinates, axes, slope, intercept)

        
        #self.play(FadeOut(function), FadeOut(function2), FadeOut(function3))
        explanation1 = self.explanation(r"We can use the sum of the squared residuals as the \\ \textbf{Loss Function} to measure how well the initial line fits the data", next_to=axes, next_to_direction=UP, wait=3, fadeOut=False)
        # Residuals sum of squares
        RSS1, RSS5 = self.RSS(coordinates, newDotsCoordinates, next_to=axes, next_to_direction=RIGHT, up=2, left=0.7)

        self.play(FadeOut(explanation1))
        explanation = self.explanation(r"\textbf{Note:} The sum of the squared residuals is \\ just one of many different \textbf{Loss Functions} that \\ can be used to evaluate how well something fits the data", next_to=axes, next_to_direction=UP, wait=3, fadeOut=True)
        explanation = self.explanation(r"In this case that something is a line", next_to=axes, next_to_direction=UP, wait=3)
        self.play(FadeOut(RSS1), FadeOut(RSS5))
        explanation = self.explanation(r"To find the optimal values for \textbf{slope} \\ and \textbf{intercept}, we first calculate the partial derivatives \\ with respect to \textbf{slope} and \textbf{intercept} and plug in the data", next_to=axes, next_to_direction=UP, wait=3, fadeOut=False)
        
        # Derivatives of RSS
        partialSlope1, partialSlope5, totalResultSlope = self.partialDerivative(coordinates, intercept, slope, axes, "slope")
        slopeGroup = [partialSlope1, partialSlope5]
        slopeGroup = VGroup(*slopeGroup)
        partialIntercept1, partialIntercept5, totalResultIntercept = self.partialDerivative(coordinates, intercept, slope, axes, "intercept", next_to=partialSlope1)
        interceptGroup = [partialIntercept1, partialIntercept5]
        interceptGroup = VGroup(*interceptGroup)

        self.play(FadeOut(explanation))
        # clear up all objects
        objects = [axes, x_label, y_label, *dots, *newDots.values(), *connections.values(), line, linetitle]
        group = VGroup(*objects)
        self.play(FadeOut(group))
        self.wait(0.5)
        
        
        #group = VGroup(*derivatives)
        self.play(slopeGroup.animate.shift(LEFT*4))
        vertical_shift = slopeGroup[0].get_center()[1] - interceptGroup[0].get_center()[1]
        self.play(slopeGroup.animate.shift(DOWN*vertical_shift))
        # Animate move group to left
        
        explanation = Tex(r"Afterwards we can calculate the \textbf{stepsizes} \\ of the \textbf{intercept} and the \textbf{slope} by multiplying \\ our partial derivatives by the learning rate which is set to 0.01").next_to(slopeGroup, UP).scale(0.5)
        #explanation.shift(DOWN)
        explanation.shift(RIGHT*1.5)
        self.play(Write(explanation))
        
        # Gradient descent
        stepSizeSlope = self.equation(result=r"stepSize_{Slope}", next_to=partialSlope1, next_to_direction=DOWN, left=0, up=-1)
        stepSizeSlope2 = self.equation(result = r"= \dfrac{\partial RSS}{\partial slope} \cdot learningRate", next_to=stepSizeSlope, next_to_direction=RIGHT, left=0)
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




        # Visualize
        stepSizeIntercept = r"stepSize_{intercept}"
        stepSizeIntercept = self.equation(result=r"stepSize_{Intercept}", next_to=stepSizeSlope, next_to_direction=DOWN, left=0.3, up=-0.5)
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


        # New slopes and intercepts
        self.play(FadeOut(slopeGroup), FadeOut(interceptGroup))
        #self.play(stepsize.animate.shift(UP*2))
        self.play(FadeOut(explanation))

        explanation = Tex(r"Finally, we update the \textbf{slope} and the \textbf{intercept} \\ by subtracting the stepsizes from the old values").next_to(slopeGroup, UP).scale(0.5)
        #explanation.shift(DOWN)
        explanation.shift(RIGHT*1.5)
        self.play(Write(explanation))
        
        newSlope1 = self.equation(result=r"slope_{new}",next_to=stepSizeSlope, next_to_direction=RIGHT, left=-2)
        newSlope2 = self.equation(result=r"= slope_{old} - stepSize_{slope}", next_to=newSlope1, next_to_direction=RIGHT)
        self.play(Write(newSlope1))
        self.play(Write(newSlope2))
        newSlope3 = self.equation(result=rf"= {slope} - ({stepSizeSlopeValue})", next_to=newSlope2, next_to_direction=DOWN, align_to=newSlope2, align_to_direction=LEFT)
        self.play(Write(newSlope3))
        newSlopeValue = slope - stepSizeSlopeValue
        newSlope4 = self.equation(result=rf"= {newSlopeValue}", next_to=newSlope2, next_to_direction=DOWN, align_to=newSlope2, align_to_direction=LEFT)
        self.play(FadeTransform(newSlope3, newSlope4))
        self.play(FadeOut(newSlope2))
        self.play(newSlope4.animate.next_to(newSlope1, RIGHT))

        
        
        newintercept1 = self.equation(result=r"intercept_{new}", next_to=stepSizeIntercept4, next_to_direction=RIGHT, left=-1)
        newintercept2 = self.equation(result=r"= intercept_{old} - stepSize_{intercept}", next_to=newintercept1, next_to_direction=RIGHT)
        self.play(Write(newintercept1))
        self.play(Write(newintercept2))

        newintercept3 = self.equation(result=rf"= {intercept} - ({stepSizeInterceptValue})", next_to=newintercept2, next_to_direction=DOWN, align_to=newintercept2, align_to_direction=LEFT)
        self.play(Write(newintercept3))
        newinterceptValue = intercept - stepSizeInterceptValue
        newintercept4 = self.equation(result=rf"= {newinterceptValue}", next_to=newintercept2, next_to_direction=DOWN, align_to=newintercept2, align_to_direction=LEFT)
        self.play(FadeTransform(newintercept3, newintercept4))
        self.play(FadeOut(newintercept2))
        self.play(newintercept4.animate.next_to(newintercept1, RIGHT))

        # Clear stepsizes
        stepsizes = [stepSizeSlope, stepSizeSlope4, stepSizeIntercept, stepSizeIntercept4]
        stepsizes = VGroup(*stepsizes)
        self.play(FadeOut(stepsizes))

        # Clear new slopes and intercepts
        remove = [newSlope1, newSlope4, newintercept1, newintercept4]
        remove = VGroup(*remove)
        self.play(FadeOut(remove))

        self.play(FadeOut(explanation))

        explanation = Tex(r"Now we can use the new values for the slope and the intercept \\ to create a new regression line").scale(0.5).next_to(axes, UP)
        explanation.shift(RIGHT*1.5)
        explanation.shift(UP)
        self.play(Write(explanation))
        # Add linear function equation as text
        linearFunction1, linearFunction3 = self.linearFunctionText(newSlopeValue, newinterceptValue, next_to=line)
    
        # Show coordinate system again

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(2)
        for dot in dots:
            self.play(Write(dot))
        self.wait(2)

        # Add new regression line
        line, linetitle = self.graph(axes, f"{newSlopeValue}*x + {newinterceptValue}")
        self.play(Write(line), Write(linetitle))

        self.play(FadeOut(explanation))

        explanation = self.explanation(r"Finally, we can calculate the sum of the squared residuals again \\ to see how well the new line fits the data", next_to=axes, next_to_direction=UP, wait=3, fadeOut=False)
        # Create orthogonal lines
        newDots, connections, newDotsCoordinates = self.drawLoss(dots, coordinates, axes, newSlopeValue, newinterceptValue)
        self.wait(2)
        self.play(FadeOut(linearFunction1), FadeOut(linearFunction3))
        self.wait(2)
        self.RSS(coordinates, newDotsCoordinates, next_to=axes, next_to_direction=RIGHT, up=2, left=0.7)
        self.play(FadeOut(explanation))
        explanation = self.explanation(r"And we see that the new line fits the \\ data better because the RSS is \\ now 0.16 instead of 0.17", next_to=axes, next_to_direction=UP, wait=3, fadeOut=True)
        explanation = self.explanation(r"This process is repeated until the RSS can't be reduced any further", next_to=axes, next_to_direction=UP, wait=3, fadeOut=True)
        
        
        
