from manim import Create, Write, FadeIn, Axes, UP, Tex, WHITE, GREEN, Scene, Dot, DashedLine, YELLOW, RED, BLUE, DOWN, LEFT, VGroup, RIGHT, FadeOut, MathTex, Transform, FadeTransform, ReplacementTransform
import sympy as sp

class Visualize(Scene):
    ####* Functions
    def drawLoss(self, dots, coordinates, axes, slope, intercept):
        perpendicular_slope = -1 / slope
        newDots = {}
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

        # Draw loss function lines
        connections = {}
        for dot_obj, new_dot in newDots.items():
            connections[dot_obj] = DashedLine(dot_obj.get_center(), new_dot.get_center(), color=RED)

        for connection in connections.values():
            self.play(Write(connection))
        return newDots, connections

    def equation(self, result, next_to, next_to_direction, align_to=None, align_to_direction=None, up=0, left=0):
        equation = MathTex(rf"{result}")
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
        axes = Axes(
            x_range=[0, 5],
            y_range=[0, 5],
            axis_config={"color": WHITE,},
            x_length = 6,
            y_length = 6,
            
        )
        # Add labels to the axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        # Create a dots
        dots = []
        coordinates = [(1, 2), (2, 4), (2.5, 3)]
        for x, y in coordinates:
            dots.append(self.dot(axes, x, y))
        


        # Show coordinate system and dots
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(2)
        for dot in dots:
            self.play(Write(dot))
        self.wait(2)


        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        self.play(group.animate.shift(LEFT*3))
        self.wait(3)


        # Create regression line
        slope = 1.5
        intercept = 0
        line, linetitle = self.graph(axes, f"{slope}*x + {intercept}")

        function = MathTex("y")
        function2 = MathTex("= slope \cdot x + intercept")
        function3 = MathTex(f"= {slope} \cdot x + {intercept}")
        function.next_to(axes, RIGHT)
        function.shift(UP*2)
        function.shift(LEFT*0.7)
        function2.next_to(function, RIGHT)
        function3.next_to(function2, DOWN)
        function3.align_to(function2, LEFT)
        self.play(Write(function), Write(function2))
        self.play(Write(function3))
        # Show regression line
        self.wait(3)
        self.play(Write(line), Write(linetitle))




        # Create orthogonal lines
        newDots, connections = self.drawLoss(dots, coordinates, axes, slope, intercept)

        
        self.play(FadeOut(function), FadeOut(function2), FadeOut(function3))

        # Residuals sum of squares
        RSS = Tex("$RSS = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$")
        RSS.next_to(axes, RIGHT)
        RSS.shift(UP*2)
        RSS.shift(LEFT*0.7)
        self.play(Write(RSS))
        self.wait(2)
        self.play(FadeOut(RSS))

        # Derivatives of RSS
        derivativeSlope = r"&"
        derivativeIntercept = r"&"
        simplifiedDerivativeSlope = r"&"
        simplifiedDerivativeIntercept = r"&"
        totalResultSlope = 0
        totalResultIntercept = 0
        totalResultSlopeString = r"="
        totalResultInterceptString = r"="
        for cords in coordinates:
            if cords == coordinates[0]:
                derivativeIntercept += r"="
                derivativeSlope += r"="
                simplifiedDerivativeSlope += r"="
                simplifiedDerivativeIntercept += r"="
            x, y = cords
            derivativeSlope += rf"(-2) \cdot {x} \cdot ({intercept} + {slope} \cdot {x}) \\ & +"
            derivativeIntercept += rf"(-2) \cdot ({intercept} + {slope} \cdot {x}) \\ & +"
            calculationSlope = (-2) * x * (intercept + slope * x)
            calculationIntercept = (-2) * (intercept + slope * x)
            totalResultSlope += calculationSlope
            totalResultIntercept += calculationIntercept
            simplifiedDerivativeIntercept += rf"{calculationIntercept} +"
            simplifiedDerivativeSlope += rf"{calculationSlope} +"
        derivativeSlope = derivativeSlope[:-1]
        derivativeIntercept = derivativeIntercept[:-1]
        simplifiedDerivativeIntercept = simplifiedDerivativeIntercept[:-1]
        simplifiedDerivativeIntercept = simplifiedDerivativeIntercept.replace("+-", "-")
        simplifiedDerivativeSlope = simplifiedDerivativeSlope[:-1]
        simplifiedDerivativeSlope = simplifiedDerivativeSlope.replace("+-", "-")
        totalResultSlopeString += rf"{totalResultSlope}"
        totalResultInterceptString += rf"{totalResultIntercept}"
        partialSlopeText1 = self.equation(result=r"\dfrac{\partial RSS}{\partial slope}", next_to=axes, next_to_direction=RIGHT, up=2, left=0.7)
        partialSlopeText2 = self.equation(result=r"& = -2 \sum_{i=1}^{n} x_i(y_i - \hat{y}_i) \\ &", next_to=partialSlopeText1, next_to_direction=RIGHT)
        partialSlopeText3 = self.equation(result=derivativeSlope, next_to=partialSlopeText2, next_to_direction=DOWN, align_to=partialSlopeText2, align_to_direction=LEFT)
        partialSlopeText4 = self.equation(result=simplifiedDerivativeSlope, next_to=partialSlopeText2, next_to_direction=DOWN, align_to=partialSlopeText3, align_to_direction=LEFT)
        partialSlopeText5 = self.equation(result=totalResultSlopeString, next_to=partialSlopeText2, next_to_direction=DOWN, align_to=partialSlopeText4, align_to_direction=LEFT)
        # Remove last plus sign
        self.play(Write(partialSlopeText1))
        
        self.play(Write(partialSlopeText2))
        self.play(Write(partialSlopeText3))
        self.wait(3)
        
        self.play(FadeTransform(partialSlopeText3, partialSlopeText4))
        self.wait(2)
        self.play(FadeOut(partialSlopeText2), partialSlopeText5.animate.next_to(partialSlopeText1, RIGHT))
        self.wait(2)

        partialInterceptText1 = self.equation(result=r"\dfrac{\partial RSS}{\partial intercept}", next_to=partialSlopeText1, next_to_direction=DOWN)
        partialInterceptText2 = self.equation(result=r"= -2 \sum_{i=1}^{n} (y_i - \hat{y}_i) \\ &", next_to=partialInterceptText1, next_to_direction=RIGHT)
        partialInterceptText3 = self.equation(result=derivativeIntercept, next_to=partialInterceptText2, next_to_direction=DOWN, align_to=partialInterceptText2, align_to_direction=LEFT)
        partialInterceptText4 = self.equation(result=simplifiedDerivativeIntercept, next_to=partialInterceptText2, next_to_direction=DOWN, align_to=partialInterceptText3, align_to_direction=LEFT)
        partialInterceptText5 = self.equation(result=totalResultInterceptString, next_to=partialInterceptText2, next_to_direction=DOWN, align_to=partialInterceptText4, align_to_direction=LEFT)

        self.play(Write(partialInterceptText1))
        
        self.play(Write(partialInterceptText2))
        self.play(Write(partialInterceptText3))
        self.wait(3)
        
        self.play(FadeTransform(partialInterceptText3, partialInterceptText4))
        self.wait(3)
        #partialSlopeText5, DERIVATIVE_SLOPE = self.partialDerivative5("slope", coordinates, 0, slope, partialSlopeText2, DOWN, 2)
        self.play(FadeTransform(partialInterceptText4, partialInterceptText5))
        self.wait(2)
        self.play(FadeOut(partialInterceptText2), partialInterceptText5.animate.next_to(partialInterceptText1, RIGHT))
        self.wait(2)
        
        # clear up all objects
        objects = [axes, x_label, y_label, *dots, *newDots.values(), *connections.values(), line, linetitle]
        group = VGroup(*objects)
        self.play(FadeOut(group))
        self.wait(0.5)
        slopeGroup = [partialSlopeText1, partialSlopeText5]
        interceptGroup = [partialInterceptText1, partialInterceptText5]
        slopeGroup = VGroup(*slopeGroup)
        interceptGroup = VGroup(*interceptGroup)
        #group = VGroup(*derivatives)
        self.play(slopeGroup.animate.shift(LEFT*6))
        vertical_shift = slopeGroup[0].get_center()[1] - interceptGroup[0].get_center()[1]
        self.play(interceptGroup.animate.shift(UP*vertical_shift))
        # Animate move group to left
        
        
        # Gradient descent
        stepSizeSlope = self.equation(result=r"stepSize_{Slope}", next_to=partialSlopeText1, next_to_direction=DOWN, left=-1)
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




        # Visualize
        stepSizeIntercept = r"stepSize_{intercept}"
        stepSizeIntercept = self.equation(result=r"{stepSizeIntercept}", next_to=stepSizeSlope, next_to_direction=DOWN, left=0.3, up=-0.5)
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
        self.play(stepsize.animate.shift(UP*2))

        newSlope1 = self.equation(result=r"slope_{new}",next_to=stepSizeIntercept, next_to_direction=DOWN, left=-2)
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

        
        
        newintercept1 = self.equation(result=r"intercept_{new}", next_to=newSlope1, next_to_direction=DOWN)
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
        linearFunction1 = MathTex("y")
        linearFunction2 = MathTex("= slope \cdot x + intercept")
        linearFunction3 = MathTex(f"= {newSlopeValue} \cdot x + {newinterceptValue}")
        linearFunction1.next_to(newintercept1, DOWN)
        linearFunction1.align_to(newintercept1, LEFT)
        linearFunction2.next_to(linearFunction1, RIGHT)
        linearFunction3.next_to(linearFunction2, DOWN)
        linearFunction3.align_to(linearFunction2, LEFT)
        self.play(Write(linearFunction1))
        self.play(Write(linearFunction2))
        self.play(Write(linearFunction3))
        self.play(FadeOut(linearFunction2), linearFunction3.animate.align_to(linearFunction1, UP))
        
        # Clear new slopes and intercepts
        remove = [newSlope1, newSlope4, newintercept1, newintercept4]
        remove = VGroup(*remove)
        self.play(FadeOut(remove))

        # Move linear function to the right
        linearFunction = [linearFunction1, linearFunction3]
        linearFunction = VGroup(*linearFunction)
        self.play(linearFunction.animate.shift(RIGHT*5))
        self.wait(2)

        # Show coordinate system again

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(2)
        for dot in dots:
            self.play(Write(dot))
        self.wait(2)

        # Add new regression line
        line, linetitle = self.graph(axes, f"{newSlopeValue}*x + {newinterceptValue}")
        self.play(Write(line), Write(linetitle))


        # Create orthogonal lines
        newDots, connections = self.drawLoss(dots, coordinates, axes, newSlopeValue, newinterceptValue)
        
        
        
