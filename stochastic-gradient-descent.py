from manim import *
import sympy as sp

class Visualize(Scene):
    ####* Functions
    def why_sgd(self):
        #* Why SGD?
        why_sgd = Tex(r"Why Stochastic Gradient Descent?", color=WHITE)
        self.play(Create(why_sgd))
        self.wait(2)
        self.play(FadeOut(why_sgd))
    
    def explain_sgd(self):
        set1 = Tex(r"Imagine we had a more complicated model, like a Logistic Regression that used 23,000 genes to predict if someone will have a disease?").scale(0.8)
        set2 = Tex(r"Then we would have 23,000 derivatives to plug the data into.").scale(0.8)
        set3 = Tex(r"And what if we had data from 1,000,000 samples?").scale(0.8)

        VGroup(set1, set2, set3).arrange(DOWN)
        self.play(Write(set1))
        self.wait(8)
        self.play(FadeIn(set2, shift=DOWN))
        self.wait(4)
        self.play(FadeIn(set3, shift=DOWN))
        self.wait(3)
        self.play(FadeOut(set1), FadeOut(set2), FadeOut(set3))
        self.wait(1)
        set4 = Tex(r"Then we would have to calculate 1,000,000 terms for each of the 23,000 derivatives.").scale(0.8)
        set5 = Tex(r"In other words, we'd have to calculate 23,000,000,000 terms for each step.").scale(0.8)
        set6 = Tex(r"And since it is common to take at least 1,000 steps, we would calculate at least 2,300,000,000,000 terms.").scale(0.8) 
        VGroup(set4, set5, set6).arrange(DOWN)
        self.play(Write(set4))
        self.wait(5)
        self.play(FadeIn(set5, shift=DOWN))
        self.wait(5)
        self.play(FadeIn(set6, shift=DOWN))
        self.wait(6)
        self.play(FadeOut(set4), FadeOut(set5), FadeOut(set6))
        self.wait(1)
        set7 = Tex(r"So, for BIG DATA, Gradient Descent is slow.").scale(0.8)
        set8 = Tex(r"This is where Stochastic Gradient Descent comes in handy.").scale(0.8)
        VGroup(set7, set8).arrange(DOWN)
        self.play(Write(set7))
        self.wait(3)
        self.play(FadeIn(set8, shift=DOWN))
        self.wait(3)
        self.play(FadeOut(set7), FadeOut(set8))
        self.wait(1)



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

    def drawLoss2(self, dots, coordinates, axes, slope, intercept):
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

    def dot2(self, axes, x, y):
        dot = Dot(axes.c2p(x, y), color=RED)
        return dot

    def example1(self):
        # Create axes
        axes, x_label, y_label = self.drawCoordinateSystem2(x_range=[0, 5], y_range=[0, 5], size=6)

        # Create dots
        dots = VGroup()
        coordinates = [(1, 2), (2, 4), (3, 3)]
        for x, y in coordinates:
            dots.add(self.dot2(axes, x, y))

        # Create a title for the coordinate system
        title = Tex("Simple Example", color=BLUE).scale(0.8)
        title.next_to(axes, UP, buff=0.5)

        # Show coordinate system and dots
        self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
        for dot in dots:
            self.play(Write(dot))
        self.wait(2)

        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        group.scale(0.6)
        self.play(group.animate.shift(DOWN, LEFT*3))
        self.wait(3)

        # Example: Add an arrow pointing to the first dot with explanation
        target_dot = dots[0]

        # Grey out other dots
        for dot in dots:
            if dot != target_dot:
                dot.set_color(GREY)

        # Create an arrow
        arrow = Arrow(start=2*UP+2*LEFT, end=target_dot.get_center(), buff=0.1, color=BLUE)

        # Create explanatory text
        explanation = Tex(r"Stochastic Gradient Descent would randomly pick one sample for each step…", color=WHITE).scale(0.5)
        explanation.next_to(arrow.get_start(), UP, buff=0.1)
        self.wait(5)
        # Add the arrow and text to the scene
        self.play(GrowArrow(arrow), Write(explanation))
        self.wait(2)

        # Optional: Additional explanatory text
        explanation2 = Tex(r"...and just use that one sample to calculate the derivatives.", color=WHITE).scale(0.5)
        explanation2.next_to(arrow.get_start(), UP, buff=0.1)
        self.play(FadeOut(explanation))
        self.play(Write(explanation2))
        self.wait(3)
        self.play(FadeOut(explanation2), FadeOut(arrow))

        # Create the derivative equation parts
        equation_part1 = MathTex(
            r"\frac{d}{d \text{intercept}}",
            r"\text{ Sum of squared residuals}",
            r"=",
            font_size=24
        )
        equation_part2 = MathTex(
            r"-2(\text{Height} - (\text{intercept} + \text{slope} \times \text{Weight}))",
            font_size=24
        )

        # Position the equation parts
        equation_part1.next_to(group, RIGHT, buff=0.5)
        equation_part1.shift(UP*2)
        equation_part2.next_to(equation_part1, DOWN, aligned_edge=LEFT)

        # Display the equation parts
        self.play(Write(equation_part1))
        self.play(Write(equation_part2))
        self.wait(2)

        # Create arrows
        # Since we cannot target the exact submobject, we will approximate the position manually
        # Adjust the arrow's end positions as needed to accurately point to 'Height' and 'Weight'
        arrow_to_height_end = equation_part2.get_center() + LEFT * 1.8   # These values are examples; adjust as needed
        arrow_to_weight_end = equation_part2.get_center() + RIGHT * 2 + DOWN * 0.2   # These values are examples; adjust as needed

        arrow_to_height = Arrow(start=dots[0].get_center(), end=arrow_to_height_end, buff=0.1, color=BLUE)
        arrow_to_weight = Arrow(start=dots[0].get_center(), end=arrow_to_weight_end, buff=0.1, color=BLUE)

        # Display the arrows
        self.play(GrowArrow(arrow_to_height), GrowArrow(arrow_to_weight))
        self.wait(2)
        self.play(FadeOut(arrow_to_height), FadeOut(arrow_to_weight))
        equation_part1.set_color(GREY)
        equation_part2.set_color(GREY)

        # Create the derivative equation parts
        equation_part3 = MathTex(
            r"\frac{d}{d \text{intercept}}",
            r"\text{ Sum of squared residuals}",
            r"=",
            font_size=24
        )
        equation_part4 = MathTex(
            r"-2 x \text{Weight}(\text{Height} - (\text{intercept} + \text{slope} \times \text{Weight}))",
            font_size=24
        )

        # Position the equation parts
        equation_part3.next_to(group, DR, buff=0.5)
        equation_part3.shift(UP*2)
        equation_part4.next_to(equation_part3, DOWN, aligned_edge=LEFT)

        # Display the equation parts
        self.play(Write(equation_part3))
        self.play(Write(equation_part4))
        self.wait(2)

        # Create arrows
        # Since we cannot target the exact submobject, we will approximate the position manually
        # Adjust the arrow's end positions as needed to accurately point to 'Height' and 'Weight'
        arrow_to_height_end = equation_part3.get_center() + LEFT * 1.4 + DOWN * 0.6 # These values are examples; adjust as needed
        arrow_to_weight_end = equation_part3.get_center() + RIGHT * 2.4 + DOWN * 0.6   # These values are examples; adjust as needed

        arrow_to_height = Arrow(start=dots[0].get_center(), end=arrow_to_height_end, buff=0.1, color=BLUE)
        arrow_to_weight = Arrow(start=dots[0].get_center(), end=arrow_to_weight_end, buff=0.1, color=BLUE)

        # Display the arrows
        self.play(GrowArrow(arrow_to_height), GrowArrow(arrow_to_weight))
        self.wait(2)
        self.play(FadeOut(arrow_to_height), FadeOut(arrow_to_weight))
        equation_part1.set_color(WHITE)
        equation_part2.set_color(WHITE)


        # Create an arrow
        arrow = Arrow(start=2*UP+2*LEFT, end=target_dot.get_center(), buff=0.1, color=BLUE)
        arrow2 = Arrow(start=2*UP+2*LEFT, end=equation_part1.get_center(), buff=0.1, color=BLUE)
        arrow3 = Arrow(start=2*UP+2*LEFT, end=equation_part3.get_center(), buff=0.1, color=BLUE)
        # Create explanatory text
        explanation = Tex(r"Thus, in this super simple example, Stochastic Gradient Descent reduced the number of terms computed by a factor of 3", color=WHITE).scale(0.5)
        explanation.next_to(arrow.get_start(), UP, buff=0.1)

        # Add the arrow and text to the scene
        self.play(
            GrowArrow(arrow),  # Grow the first arrow
            GrowArrow(arrow2),  # Grow the second arrow
            GrowArrow(arrow3),  # Grow the third arrow
            Write(explanation),  # Write the explanation text
            )
        self.wait(8)
        self.play(FadeOut(explanation))
        equation_part1.set_color(GREY)
        equation_part2.set_color(GREY)
        equation_part3.set_color(GREY)
        equation_part4.set_color(GREY)
        axes.set_color(GREY)
        arrow.set_color(GREY)
        arrow2.set_color(GREY)
        arrow3.set_color(GREY)
        target_dot.set_color(GREY)

        explanation = Tex(r"If we had 1,000,000 samples, then Stochastic Gradient Descent would reduce the amount terms computed by a factor of 1,000,000.", color=WHITE).scale(0.5)
        explanation.next_to(arrow.get_start(), UP, buff=0.1)
        self.play(Write(explanation))
        self.wait(7)
        self.play(FadeOut(dots), FadeOut(title), FadeOut(x_label), FadeOut(y_label), FadeOut(axes), FadeOut(dot),FadeOut(arrow), FadeOut(explanation), FadeOut(arrow2), FadeOut(arrow3), FadeOut(equation_part1), FadeOut(equation_part2), FadeOut(equation_part3), FadeOut(equation_part4))

    def example2(self):
        axes, x_label, y_label = self.drawCoordinateSystem2(x_range=[0, 5], y_range=[0, 5], size=6)

        # Create dots
        dots = VGroup()
        coordinates = [(1, 2),(1.1,2),(1.1,2.1),(1.2,2.1), (4, 4.5),(4.1,4.5),(4.1,4.6),(4.2,4.6), (3, 3),(3.1,3),(3.1,3.1),(3.2,3.1)]
        for x, y in coordinates:
            dots.add(self.dot2(axes, x, y))
        
        # Create a title for the coordinate system
        title = Tex("Redundancy", color=BLUE).scale(0.8)
        title.next_to(axes, UP, buff=0.5)
        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        group.scale(0.6)
        
        # Show coordinate system and dots
        self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
 
        self.play(Write(dots))
        

        self.play(group.animate.shift(DOWN, LEFT*3))
        self.wait(2)
        explanation = Tex(r"Stochastic Gradient Descent is especially useful when there are redundancies in the data.", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(6)
        self.play(FadeOut(explanation))
        self.wait(1)
        explanation = Tex(r"For example, we have 12 data points, but there is a lot of redundancy that forms 3 clusters.", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(6)
        dot1 = dots[0]
        dot3 = dots[4]
        dot5 = dots[8]
        arrow = Arrow(start=2*UP+2*LEFT, end=dot1.get_center(), buff=0.1, color=BLUE)
        arrow2 = Arrow(start=2*UP+2*LEFT, end=dot3.get_center(), buff=0.1, color=BLUE)
        arrow3 = Arrow(start=2*UP+2*LEFT, end=dot5.get_center(), buff=0.1, color=BLUE)
        self.play(GrowArrow(arrow))
        self.play(GrowArrow(arrow2))
        self.play(GrowArrow(arrow3))
        self.wait(2)
        self.play(FadeOut(explanation))
        self.play(FadeOut(arrow), FadeOut(arrow2), FadeOut(arrow3))
        
        explanation = Tex(r"So we start with a line with the intercept = 0 and the slope = 1…", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(4)
        intercept = 0
        slope = 1
        # Linie mit intercept = 0 und slope = 1 zeichnen
        start_line = axes.c2p(0, intercept)  # Anfangspunkt der Linie bei (0, intercept)
        end_line = axes.c2p(5, 5*slope + intercept)  # Endpunkt der Linie
        prediction_line = Line(start=start_line, end=end_line, color=WHITE)
        self.play(Create(prediction_line)) 
        self.play(FadeOut(explanation))
        explanation = Tex(r"...then we randomly pick this point…", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        dots[7].set_color(GREEN)
        self.wait(2)
        self.play(FadeOut(explanation))
        explanation = Tex(r"...and use that point to calculate Hight=4,2, Weight=4,6, Intercept=0, Slope=1", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(7)
        

        # Create the derivative equation parts
        equation_part1 = MathTex(
            r"\frac{d}{d \text{intercept}}",
            r"\text{ Sum of squared residuals}",
            r"=",
            font_size=24
        )
        equation_part2 = MathTex(
            r"-2(4,2 - (0 + 1 \times 4,6))",
            rf"= {round(-2*(4.2-(0+1*4.6)), 2)}",
            font_size=24
        )

        # Position the equation parts
        equation_part1.next_to(group, RIGHT, buff=0.5)
        equation_part1.shift(UP*2)
        equation_part2.next_to(equation_part1, DOWN, aligned_edge=LEFT)

        # Display the equation parts
        self.play(Write(equation_part1))
        self.play(Write(equation_part2))
        self.wait(2)

        # Create the derivative equation parts
        equation_part3 = MathTex(
            r"\frac{d}{d \text{intercept}}",
            r"\text{ Sum of squared slopes}",
            r"=",
            font_size=24
        )
        equation_part4 = MathTex(
            r"-2 \times 4,6(4,2 - (0 + 1 \times 4,6))",
            rf"={round(-2*4.6*(4.2-(0+1*4.6)), 2)}",
            font_size=24
        )

        # Position the equation parts
        equation_part3.next_to(group, DR, buff=0.5)
        equation_part3.shift(UP*2)
        equation_part4.next_to(equation_part3, DOWN, aligned_edge=LEFT)

        # Display the equation parts
        self.play(Write(equation_part3))
        self.play(Write(equation_part4))
        
        self.wait(2)
        self.play(FadeOut(explanation))

        explanation = Tex(r"Plug in the Slopes and the Learning Rate", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(2)
        # Create the derivative equation parts
        equation_part5 = MathTex(
            r"\text{Step Size}_{\text{Intercept}} = \text{Slope} \times \text{Learning Rate}",
            rf"={0.8 * 0.01}",
            font_size=24
        )
        equation_part6 = MathTex(
           r"\text{Step Size}_{\text{Slope}} = \text{Slope} \times \text{Learning Rate}",
           rf"={round(3.68 * 0.1, 3)}",
            font_size=24
        )

        # Position the equation parts
        equation_part5.next_to(equation_part2, DOWN, buff=0.5)
        
        equation_part6.next_to(equation_part5, DOWN, aligned_edge=LEFT)

        # Display the equation parts
        
        self.play(Write(equation_part5))
        self.play(Write(equation_part6))
        self.play(FadeOut(explanation))
        explanation = Tex(r"Just like with regular Gradient Descent, Stochastic Gradient Descent is sensitive to the value you choose for the Learning Rate...", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(8)
        self.play(FadeOut(explanation))
        explanation = Tex(r"...and just like for regular Gradient Descent, the general strategy is to start with a relatively large Learning Rate and make it smaller with each step...", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(10)
        self.play(FadeOut(explanation))
        explanation = Tex(r"...and lastly, just like for regular Gradient Descent, many implementations of Stochastic Gradient Descent will take care of this for you by default.", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(8)
        self.play(FadeOut(explanation))
        explanation = Tex(r"In this simple example, however, we'll just setting the Learning Rate to 0.01.", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(5)
        self.play(FadeOut(explanation))
        self.play(FadeOut(equation_part1), FadeOut(equation_part2), FadeOut(equation_part3), FadeOut(equation_part4), FadeOut(equation_part5), FadeOut(equation_part6))
        explanation = Tex(r"…calculate the new intercept…", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(2)

        # New Intersect
        equation_part1 = MathTex(
            r"\text{New Intercept} &= \text{Old Intercept} - \text{Step Size} \\",
            r"&= 0 - \frac{1}{125} \\",
            r"&= " + str(0 - (1/125)),
            font_size=24
        )
        equation_part2 = MathTex(
            r"\text{New Slope} &= \text{Old Slope} - \text{Step Size} \\",
            r"&= 1 - 0.0368\\",
            r"&= " + str(round(1 - 0.0368, 4)),
            font_size=24
        )

        # Position the equation parts
        equation_part1.next_to(group, RIGHT, buff=0.5)
        equation_part1.shift(UP*2)
        equation_part2.next_to(equation_part1, DOWN, aligned_edge=LEFT)
        
        self.wait(2)
        # Display the equation parts
        self.play(Write(equation_part1))
        self.play(Write(equation_part2))

        intercept1 = -(1/125)
        slope1 = 0.9632
       
        start_line1 = axes.c2p(0, intercept1)  
        end_line1 = axes.c2p(5, 5*slope1 + intercept1)  # Endpunkt der Linie
        prediction_line1 = Line(start=start_line1, end=end_line1, color=BLUE)
        self.play(Create(prediction_line1)) 

        dots[7].set_color(RED)
        self.play(FadeOut(explanation))
        self.play(FadeOut(equation_part1), FadeOut(equation_part2))
        
        explanation = Tex(r"...then we randomly pick another point…", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        # 1.2,2.1
        self.wait(2)
        self.play(FadeOut(explanation))
        self.play(FadeOut(prediction_line))
        explanation = Tex(r"and we just repeat everything a bunch of times...", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(3)
        FadeOut(prediction_line1)
        self.play(FadeOut(prediction_line1))
        line = self.sgd_visualization(axes, dots)
        self.play(FadeOut(explanation))
        explanation = Tex(r"until we get the best fitting line", color=WHITE).scale(0.5)
        explanation.next_to(axes, UP * 8, buff=0.1)
        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(dots), FadeOut(title), FadeOut(x_label), FadeOut(y_label), FadeOut(axes), FadeOut(explanation))
        self.play(FadeOut(line))
    def sgd_visualization(self, axes, dots):
        learning_rate = 0.01
        intercept = 0
        slope = 1
        num_iterations = 12  # Adjust for visualization

        for i in range(num_iterations):
            for dot in dots:
                x, y = axes.p2c(dot.get_center())
                intercept, slope = self.update_parameters(x, y, intercept, slope, learning_rate)
            if i < num_iterations - 1:
                line = self.draw_line(axes, intercept, slope, color="BLUE")
                self.play(FadeOut(line))  # Add a fade-out animation


        # Draw the perfect line in red
        return self.draw_line(axes, intercept, slope, color="RED")


    def update_parameters(self, x, y, intercept, slope, learning_rate):
        gradient_intercept = -2 * (y - (slope * x + intercept))
        gradient_slope = -2 * x * (y - (slope * x + intercept))
        new_intercept = intercept - learning_rate * gradient_intercept
        new_slope = slope - learning_rate * gradient_slope
        return new_intercept, new_slope

    def draw_line(self, axes, intercept, slope, color=BLUE):
        start_line = axes.c2p(0, intercept)
        end_line = axes.c2p(5, 5 * slope + intercept)  # Anpassung der Länge auf 5 Einheiten
        line = Line(start=start_line, end=end_line, color=color)
        self.play(Create(line))
        return line
        

    def construct(self):
        self.why_sgd()  # Call the why_sgd function within the construct method
        self.explain_sgd()
        self.example1()
        self.example2()