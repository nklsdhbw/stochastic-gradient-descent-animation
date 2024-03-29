from manim import *
# Scene, Text, Write, FadeOut, FadeIn, Axes, Dot, Transform, MathTex, GREEN, WHITE, RED, YELLOW, BLUE, PINK, 
# UP, RIGHT, LEFT, DOWN, VGroup, Arrow, Create, Indicate, SurroundingRectangle, GrowArrow, GrowFromCenter, 
# DrawBorderThenFill, BLACK, MoveToTarget, ReplacementTransform, Paragraph, config, LaggedStart, PURPLE, ORANGE, 
# ThreeDAxes, Surface, BLUE_E, DEGREES, ThreeDScene
import numpy as np

# use to render the scene: manim -pql adaptive-gradient-descent.py or manim -pqh adaptive-gradient-descent.py

##############################################################################################################
# This is the code for the video "Adaptive Gradient Descent" #################################################
##############################################################################################################

class AdaGrad(MovingCameraScene):
    def construct(self):
        title_text = Text("Adaptive Gradient Descent", font_size=48, color=WHITE)
        self.play(Write(title_text))
        self.wait(2)
        self.play(title_text.animate.scale(1.2).set_opacity(1.2))
        self.wait(2)
        self.play(FadeOut(title_text))

        self.basics()

##############################################################################################################
# The following scene is for the basics ######################################################################
##############################################################################################################

    def basics(self):
        what_is_adagrad = Text("Wait, but what is AdaGrad in particular?", font_size=40, color=WHITE)
        self.play(Write(what_is_adagrad))
        self.wait(2)
        self.play(what_is_adagrad.animate.to_edge(UP, buff=1))

        what_is_adagrad2 = Text("In short: AdaGrad is an adaptive learning rate method.", font_size=36, color=WHITE)
        what_is_adagrad2.next_to(what_is_adagrad, DOWN)
        self.play(Write(what_is_adagrad2))
        self.wait(2)
        self.play(FadeOut(what_is_adagrad2))

        what_is_adagrad3 = Text("The AdaGrad is effective for large and sparse datasets.", font_size=36, color=WHITE)
        what_is_adagrad3.next_to(what_is_adagrad, DOWN)
        self.play(Write(what_is_adagrad3))
        self.wait(2)
        self.play(FadeOut(what_is_adagrad3))
        self.play(FadeOut(what_is_adagrad))

        what_is_adagrad4 = Text("AdaGrad improves the convergence speed.", font_size=36, color=WHITE)
        what_is_adagrad4.next_to(what_is_adagrad, DOWN)
        self.play(Write(what_is_adagrad3))
        self.wait(2)
        self.play(FadeOut(what_is_adagrad4))
        self.play(FadeOut(what_is_adagrad))

        # mach erst mal die Basics
        concept_title = Text("In conclusion the main concepts of the AdaGrad are:", font_size=40, color=WHITE)
        self.play(FadeIn(concept_title))
        self.play(concept_title.animate.to_edge(UP, buff=1))
        self.wait(2)

        # basic concept of AdaGrad
        concept1 = Text("Adaptive learning rate adjustment", font_size=36).next_to(concept_title, DOWN)
        concept2 = Text("Effective for large, sparse datasets", font_size=36).next_to(concept1, DOWN)
        concept3 = Text("Improves convergence speed", font_size=36).next_to(concept2, DOWN)
        self.wait(2)

        self.play(Write(concept1))
        self.wait(2)
        self.play(Write(concept2))
        self.wait(2)
        self.play(Write(concept3))
        self.wait(2)
        self.play(FadeOut(concept3))
        self.wait(1)
        self.play(FadeOut(concept2))
        self.wait(1)
        self.play(FadeOut(concept1))
        self.wait(1)
        self.play(FadeOut(concept_title))
        self.wait(2)

        to_formula = Text("Now, we want to take a deeper look at AdaGrad", font_size=40, color=WHITE).next_to(concept_title, DOWN)
        to_formula2 = Text("Let's start with the formula", font_size=40, color=WHITE).next_to(to_formula, DOWN)
        self.play(Write(to_formula))
        self.wait(2)
        self.play(to_formula.animate.to_edge(UP, buff=1))
        self.wait(2)
        self.play(Write(to_formula2))
        self.wait(2)
        self.play(to_formula2.animate.to_edge(UP, buff=1))
        self.play(FadeOut(to_formula), FadeOut(to_formula2))
        self.wait(2)

        # formula of AdaGrad
        adagrad_formula = MathTex(
            r"\eta_{t,i} = \frac{\eta}{\sqrt{\sum_{\tau=1}^t g_{\tau,i}^2 + \epsilon}}",
            font_size=30)
        self.play(Write(adagrad_formula))
        self.wait(2)
        self.play(adagrad_formula.animate.scale(1.5).set_opacity(1.5))
        self.play(adagrad_formula.animate.to_edge(UP, buff=1))

        # define different components of the formula
        learning_rate_desc = MathTex(
            r"\text{Initial learning rate } \eta",
            font_size=24
        ).next_to(adagrad_formula, DOWN, aligned_edge=LEFT)

        sqrt_desc = MathTex(
            r"\text{Adjustment based on historical gradients}",
            font_size=24
        ).next_to(learning_rate_desc, DOWN, aligned_edge=LEFT)

        gradient_sum_desc = MathTex(
            r"\sum_{\tau=1}^t g_{\tau,i}^2 \text{: Sum of the squared gradients}",
            font_size=24
        ).next_to(sqrt_desc, DOWN, aligned_edge=LEFT)

        epsilon_desc = MathTex(
            r"\epsilon \text{: Small value to avoid division by zero}",
            font_size=24
        ).next_to(gradient_sum_desc, DOWN, aligned_edge=LEFT)

        # animation of the different components
        self.play(Transform(adagrad_formula[0][13:16], learning_rate_desc))
        self.wait(2)
        self.play(Transform(adagrad_formula[0][22:31], gradient_sum_desc))
        self.wait(2)
        self.play(Transform(adagrad_formula[0][34:35], epsilon_desc))
        self.wait(2)

        # create boxes around the different components
        # adagrad_formula_box = SurroundingRectangle(adagrad_formula, color=WHITE)
        # learning_rate_desc_box = SurroundingRectangle(learning_rate_desc, color=WHITE)
        # sqrt_desc_box = SurroundingRectangle(sqrt_desc, color=WHITE)
        # gradient_sum_desc_box = SurroundingRectangle(gradient_sum_desc, color=WHITE)
        # epsilon_desc_box = SurroundingRectangle(epsilon_desc, color=WHITE)

        # animation of the variables
        self.play(Write(adagrad_formula))
        self.wait(2)
        self.play(Write(learning_rate_desc))
        self.wait(2)
        self.play(Write(sqrt_desc))
        self.wait(2)
        self.play(Write(gradient_sum_desc))
        self.wait(2)
        self.play(Write(epsilon_desc))
        self.wait(2)

        # group all elements together to let them all fade out at once
        all_elements = VGroup(adagrad_formula, learning_rate_desc, sqrt_desc, gradient_sum_desc, epsilon_desc)
        self.play(FadeOut(all_elements))

        # transitional text to the advantages and disadvantages
        adv_title = Text("Now, let's take a look at the advantages and disadvantages of AdaGrad", font_size=36, color=WHITE)
        self.play(FadeIn(adv_title))
        self.play(concept_title.animate.to_edge(UP, buff=1))
        self.wait(2)
        self.play(FadeOut(adv_title))

        # advantages of AdaGrad
        advantages_title = Text("Advantages of AdaGrad", font_size=36, color=WHITE)
        self.play(FadeIn(advantages_title))
        self.play(advantages_title.animate.to_edge(UP, buff=1))
        self.wait(2)

        advantage1 = Text("1. Automatically adjusts the learning rate", font_size=24, color=GREEN).next_to(advantages_title, DOWN, aligned_edge=LEFT)
        advantage2 = Text("2. Suitable for non-stationary problems", font_size=24, color=GREEN).next_to(advantage1, DOWN, aligned_edge=LEFT)
        advantage3 = Text("3. Reduces the need for manual tuning", font_size=24, color=GREEN).next_to(advantage2, DOWN, aligned_edge=LEFT)

        self.play(Write(advantage1))
        self.wait(2)
        self.play(Write(advantage2))
        self.wait(2)
        self.play(Write(advantage3))
        self.wait(2)
        self.play(FadeOut(advantage3))
        self.wait(1)
        self.play(FadeOut(advantage2))
        self.wait(1)
        self.play(FadeOut(advantage1))
        self.wait(1)
        self.play(FadeOut(advantages_title))
        self.wait(3)

        # disadvantages of AdaGrad
        disadvantages_title = Text("Disadvantages of AdaGrad", font_size=36, color=WHITE)
        self.play(FadeIn(disadvantages_title))
        self.play(disadvantages_title.animate.to_edge(UP, buff=1))
        self.wait(2)

        disadvantage1 = Text("1. Risk of learning rate reducing too quickly", font_size=24, color=RED).next_to(disadvantages_title, DOWN, aligned_edge=LEFT)
        disadvantage2 = Text("2. Can be suboptimal in deep networks", font_size=24, color=RED).next_to(disadvantage1, DOWN, aligned_edge=LEFT)
        disadvantage3 = Text("3. Requires fine-tuning of ε", font_size=24, color=RED).next_to(disadvantage2, DOWN, aligned_edge=LEFT)

        self.play(Write(disadvantage1))
        self.wait(2)
        self.play(Write(disadvantage2))
        self.wait(2)
        self.play(Write(disadvantage3))
        self.wait(2)
        self.play(FadeOut(disadvantage3))
        self.wait(1)
        self.play(FadeOut(disadvantage2))
        self.wait(1)
        self.play(FadeOut(disadvantage1))
        self.wait(1)
        self.play(FadeOut(disadvantages_title))
        self.wait(3)


        self.convex_AdaGrad()

##############################################################################################################
# The following scene is for the animation of the AdaGrad algorithm ##########################################
##############################################################################################################

    def convex_AdaGrad(self):
        # Einführungstext
        transition_text = Text("Now, let's move on to the practical application of AdaGrad", font_size=36, color=WHITE)
        self.play(Write(transition_text))
        self.wait(2)
        self.play(FadeOut(transition_text))

        # Grafik der AdaGrad-Anwendung
        axes = Axes(x_range=[-3, 3], y_range=[-5, 5], axis_config={"color": WHITE})
        function_curve = axes.plot(lambda x: x**2, color=GREEN)
        function_label = MathTex("f(x) = x^2", color=GREEN).next_to(function_curve, UP)
        self.add(axes, function_curve, function_label)

        # Startpunkt
        start_x = 2
        dot = Dot(axes.c2p(start_x, start_x**2), color=RED)
        self.add(dot)

        # Initialwerte für AdaGrad
        learning_rate = 1.0
        historical_gradient = 0
        epsilon = 1e-8

        # Formel initialisieren
        formula_text = self.get_formula_text(learning_rate, epsilon, 0, 2*start_x, historical_gradient)
        formula = MathTex(formula_text, font_size=24).to_edge(RIGHT)
        self.add(formula)

        # AdaGrad Schritte durchführen
        for step in range(1, 11):
            gradient = 2 * start_x
            historical_gradient += gradient ** 2
            adjusted_learning_rate = learning_rate / (np.sqrt(historical_gradient) + epsilon)
            start_x -= adjusted_learning_rate * gradient
            new_dot_position = axes.c2p(start_x, start_x**2)
            
            # Aktualisiere Punkt und Formel
            new_dot = Dot(new_dot_position, color=RED)
            self.play(Transform(dot, new_dot))
            
            new_formula_text = self.get_formula_text(learning_rate, epsilon, step, gradient, historical_gradient)
            new_formula = MathTex(new_formula_text, font_size=24).to_edge(RIGHT)
            self.play(Transform(formula, new_formula))
            
            self.wait(0.5)  # Eine kurze Pause zwischen den Iterationen

        self.wait(2)  # Warte am Ende der Animation

    def get_formula_text(self, eta, epsilon, step, gradient, historical_gradient):
        # Erzeugt den Text für die Formel mit aktuellen Werten
        return f"\\eta_{{t+1}} = \\frac{{{eta:.2f}}}{{\\sqrt{{\\sum_{{\\tau=1}}^{step} ({gradient:.2f})^2 + {epsilon}}}}}"




        self.non_convex_AdaGrad()

##############################################################################################################
# The following scene is for the animation of the AdaGrad algorithm with a non-convex function ###############
##############################################################################################################

    def non_convex_AdaGrad(self):
        nonconvex1 = Text("Wait, what happens if we use a non-convex function?", font_size=36, color=WHITE)
        self.play(Write(nonconvex1))
        self.wait(2)
        self.play(FadeOut(nonconvex1))
        # same as before, but with a non-convex function
        nonconvex_title = Text("AdaGrad sample application (non-convex)", font_size=36)
        self.play(Write(nonconvex_title))
        self.wait(2)
        self.play(FadeOut(nonconvex_title))

        axes = Axes(x_range=[-3, 3], y_range=[-5, 5], axis_config={"color": WHITE})
        function_curve = axes.plot(lambda x: x**3 - 3*x, color=BLUE)
        function_label = MathTex("f(x) = x^3 - 3x", color=BLUE).next_to(function_curve, UP)

        self.play(Write(axes), Write(function_curve), Write(function_label))

        start_x = 2.5
        start_dot = Dot(axes.c2p(start_x, start_x**3 - 3*start_x), color=RED)
        self.play(FadeIn(start_dot))

        explanation_text = MathTex("", font_size=24).to_edge(UP)
        self.play(Write(explanation_text))

        # AdaGrad optimization steps
        x = start_x
        historical_gradient = 0
        learning_rate = 0.5

        for i in range(20):
            gradient = 3 * x**2 - 3
            historical_gradient += gradient ** 2
            adjusted_learning_rate = learning_rate / (np.sqrt(historical_gradient) + 1e-8)
            x = x - adjusted_learning_rate * gradient
            new_dot = Dot(axes.c2p(x, x**3 - 3*x), color=RED)

            # update the explanation text
            new_explanation_text = MathTex(
                f"Schritt {i+1}:",
                f"Gradient: {gradient:.2f}",
                f"\\quad Angepasste Lernrate: {adjusted_learning_rate:.2f}",
                f"\\quad Position: ({x:.2f}, {x**3 - 3*x:.2f})",
                font_size=24
            ).to_edge(UP)

            # dot and text animation at the same time
            self.play(Transform(start_dot, new_dot), Transform(explanation_text, new_explanation_text))

        self.wait(3)
        self.play(FadeOut(function_curve), FadeOut(axes), FadeOut(start_dot), FadeOut(function_label), FadeOut(explanation_text))

        self.explain_adagrad()

##############################################################################################################
# The following scene is for the explanation of the AdaGrad algorithm ########################################
##############################################################################################################

    def explain_adagrad(self):
        
        what_happend_text = Text("What happened in the animation?", font_size=36)
        self.play(Write(what_happend_text))
        self.wait(2)
        self.play(FadeOut(what_happend_text))

        title_explanation = Text("Explanation of the AdaGrad-animation", font_size=36)
        self.play(Write(title_explanation))
        self.wait(2)
        self.play(title_explanation.animate.to_edge(UP))

        learning_rate_text = Text("For your memory, here is the formula:", font_size=24).shift(UP * 2)
        self.play(Write(learning_rate_text))
        self.wait(2)

        # example of a learning rate formula
        learning_rate_formula = MathTex(r"\eta_{t} = \frac{\eta}{\sqrt{G_{t} + \epsilon}}", font_size=24).next_to(learning_rate_text, DOWN, buff=0.5)
        self.play(Write(learning_rate_formula))
        self.wait(2)

        # move the learning rate explanation
        lr_group = VGroup(learning_rate_text, learning_rate_formula)
        self.play(lr_group.animate.next_to(title_explanation, DOWN, buff=0.5))

        # explanation of the gradient
        gradient_text = Text("The gradient influences the direction of the optimisation", font_size=24).shift(UP)
        self.play(Write(gradient_text))
        self.wait(2)

        # visualisation of the gradient with an arrow
        arrow = Arrow(RIGHT, LEFT, buff=0).next_to(gradient_text, DOWN, buff=0.5)
        arrow_text = Text("Direction of the gradient", font_size=24).next_to(arrow, DOWN)
        self.play(GrowArrow(arrow), Write(arrow_text))
        self.wait(3)

        # move the explanation
        gradient_group = VGroup(gradient_text, arrow, arrow_text)
        self.play(gradient_group.animate.next_to(lr_group, DOWN, buff=0.5))

        # end of the scene
        end_text = Text("That's the Adaptive Gradient Descent!", font_size=36, color=GREEN).next_to(gradient_group, DOWN, buff=0.5)
        self.play(Write(end_text))
        self.wait(3)

        self.play(FadeOut(lr_group), FadeOut(gradient_group), FadeOut(end_text), FadeOut(title_explanation))

        self.comparison()

##############################################################################################################
# The following scene is for the comparison of AdaGrad, RMSprop and Adam #####################################
##############################################################################################################

    def comparison(self):
        # introduction for the following animation
        intro_title = Text("Comparison of AdaGrad, RMSprop and Adam", font_size=36, color=GREEN).to_edge(UP)
        intro_text = Paragraph(
            "In the following animation, we will compare the optimization algorithms AdaGrad, RMSprop, and Adam. ",
            "Each point represents an algorithm, and its movement on the function graph demonstrates ",
            "how each algorithm attempts to find the minimum of the function.",
            font_size=24,
            line_spacing=1.5
        ).next_to(intro_title, DOWN, buff=0.5)#.scale_to_fit_width(config.frame_width - 2)

        self.play(Write(intro_title))
        self.wait(2)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_title), FadeOut(intro_text))

        short_explanation = Text("Here is a short explanation of the different algorithms:", font_size=36, color=WHITE)
        self.play(Write(short_explanation))
        self.wait(2)
        self.play(FadeOut(short_explanation))

        # rmsprop explanation
        rmsprop_title = Text("RMSprop", font_size=36, color=WHITE).to_edge(UP)
        rmsprop_text = Paragraph(
            "RMSprop (Root Mean Square Propagation) is an adaptive learning rate method. ",
            "It was designed to resolve the diminishing learning rates of AdaGrad. ",
            "RMSprop adjusts the learning rate by dividing it with an exponentially ",
            "decaying average of squared gradients.",
            font_size=24,
            line_spacing=1.5
        ).next_to(rmsprop_title, DOWN, buff=0.5).scale_to_fit_width(config.frame_width - 2)

        self.play(Write(rmsprop_title))
        self.wait(2)
        self.play(Write(rmsprop_text))
        self.wait(3)
        self.play(FadeOut(rmsprop_title), FadeOut(rmsprop_text))

        # adam explanation
        adam_title = Text("Adam", font_size=36, color=WHITE).to_edge(UP)
        adam_text = Paragraph(
            "Adam (Adaptive Moment Estimation) combines the ideas of RMSprop and momentum. ",
            "It keeps an exponentially decaying average of past gradients (like RMSprop) ",
            "and also keeps an exponentially decaying average of past squared gradients. ",
            "This makes it effective for problems with noisy or sparse gradients.",
            font_size=24,
            line_spacing=1.5
        ).next_to(adam_title, DOWN, buff=0.5).scale_to_fit_width(config.frame_width - 2)

        self.play(Write(adam_title))
        self.wait(2)
        self.play(Write(adam_text))
        self.wait(3)
        self.play(FadeOut(adam_title), FadeOut(adam_text))

        animation_text3 = Text("Let's see how the different algorithms perform", font_size=36, color=WHITE)
        self.play(Write(animation_text3))
        self.wait(2)
        self.play(FadeOut(animation_text3))

        # definition of the functions and of the gradient
        def func(x):
            return x**2

        def grad_func(x):
            return 2 * x

        # initialisation of the variables
        start_x = 2
        lr = 0.1
        epsilon = 1e-8
        adagrad_cache = 0
        decay_rate = 0.99
        rmsprop_cache = 0 # rmsprop specific
        beta1 = 0.9 # adam specific
        beta2 = 0.999 # adam specific
        m = 0 # adam specific
        v = 0 # adam specific

        # create axes and function
        axes = Axes(x_range=[-3, 3], y_range=[-1, 9])
        graph = axes.plot(func, color=WHITE)
        self.add(axes, graph)

        # initialise the dots for adagrad, rmsprop and adam
        adagrad_dot = Dot(color=RED).move_to(axes.c2p(start_x, func(start_x)))
        rmsprop_dot = Dot(color=GREEN).move_to(axes.c2p(start_x, func(start_x)))
        adam_dot = Dot(color=BLUE).move_to(axes.c2p(start_x, func(start_x)))

        # create text labels for the dots
        adagrad_label = Text("AdaGrad", font_size=20, color=RED).next_to(adagrad_dot, UP+RIGHT)
        rmsprop_label = Text("RMSprop", font_size=20, color=GREEN).next_to(rmsprop_dot, UP+RIGHT)
        adam_label = Text("Adam", font_size=20, color=BLUE).next_to(adam_dot, UP+RIGHT)

        self.add(adagrad_dot, rmsprop_dot, adam_dot, adagrad_label, rmsprop_label, adam_label)

        # create a descriptive text for the animation
        description = Text("Initializing optimization algorithms", font_size=24).to_edge(UP)
        self.add(description)

        # loop for the animation
        for i in range(10):
            # update the descriptive text
            if i == 5:
                self.play(ReplacementTransform(description, Text("Optimizing...", font_size=24).to_edge(UP)))
                description = Text("Optimizing...", font_size=24).to_edge(UP)

            grad = grad_func(start_x)

        # loop for the animation
        for _ in range(10):
            grad = grad_func(start_x)
            # adagrad update
            adagrad_cache += grad**2
            start_x -= lr * grad / (np.sqrt(adagrad_cache) + epsilon)
            new_adagrad_dot = Dot(color=RED).move_to(axes.c2p(start_x, func(start_x)))
            new_adagrad_label = Text("AdaGrad", font_size=20, color=RED).next_to(new_adagrad_dot, UP+RIGHT)
            
            # rmsprop update
            rmsprop_cache = decay_rate * rmsprop_cache + (1 - decay_rate) * grad**2
            start_x -= lr * grad / (np.sqrt(rmsprop_cache) + epsilon)
            new_rmsprop_dot = Dot(color=GREEN).move_to(axes.c2p(start_x, func(start_x)))
            new_rmsprop_label = Text("RMSprop", font_size=20, color=GREEN).next_to(new_rmsprop_dot, UP+RIGHT)

            # adam update
            m = beta1 * m + (1 - beta1) * grad
            mt = m / (1 - beta1)
            v = beta2 * v + (1 - beta2) * (grad**2)
            vt = v / (1 - beta2)
            start_x -= lr * mt / (np.sqrt(vt) + epsilon)
            new_adam_dot = Dot(color=BLUE).move_to(axes.c2p(start_x, func(start_x)))
            new_adam_label = Text("Adam", font_size=20, color=BLUE).next_to(new_adam_dot, UP+RIGHT)

            self.play(
                ReplacementTransform(adagrad_dot, new_adagrad_dot),
                ReplacementTransform(rmsprop_dot, new_rmsprop_dot),
                ReplacementTransform(adam_dot, new_adam_dot),
                ReplacementTransform(adagrad_label, new_adagrad_label),
                ReplacementTransform(rmsprop_label, new_rmsprop_label),
                ReplacementTransform(adam_label, new_adam_label),
                run_time=0.5
            )

            # update to the new dots and labels
            adagrad_dot, rmsprop_dot, adam_dot = new_adagrad_dot, new_rmsprop_dot, new_adam_dot
            adagrad_label, rmsprop_label, adam_label = new_adagrad_label, new_rmsprop_label, new_adam_label

        self.wait(3)
        self.play(FadeOut(description))
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(adagrad_dot), FadeOut(rmsprop_dot), FadeOut(adam_dot), FadeOut(adagrad_label), FadeOut(rmsprop_label), FadeOut(adam_label))

        self.three_d_animation()

    # # maybe keep this, because it isn't working properly
    # def three_d_animation(self):
    #     self.renderer.camera_class = ThreeDCamera

    #     axes = ThreeDAxes()

    #     transition_text2 = Text("How does it look in 3D?", font_size=36, color=ORANGE)
    #     self.play(Write(transition_text2))
    #     self.wait(3)
    #     self.play(FadeOut(transition_text2))

    #     self.wait(2)

    #     transition_text3 = Text("Let's find out!", font_size=36, color=ORANGE)
    #     self.play(Write(transition_text3))
    #     self.wait(3)
    #     self.play(FadeOut(transition_text3))

    #     def func(x, y):
    #         return np.sin(np.sqrt(x**2 + y**2))
        
    #     def grad_func(x, y):
    #         # Berechnen der partiellen Ableitungen der Funktion
    #         r = np.sqrt(x**2 + y**2)
    #         df_dx = (x/r) * np.cos(r)
    #         df_dy = (y/r) * np.cos(r)
    #         return np.array([df_dx, df_dy])

    #     surface = Surface(
    #         lambda u, v: axes.c2p(u, v, func(u, v)),
    #         u_range=[-2, 2],
    #         v_range=[-2, 2],
    #         resolution=(30, 30)
    #     )

    #     surface.set_style(fill_opacity=0.5, fill_color=BLUE_E, stroke_color=BLUE_E)
    #     self.add(axes, surface)

    #     start_point = np.array([1.5, 1.5, func(1.5, 1.5)])
    #     adagrad_dot = Dot(axes.c2p(*start_point), color=RED)
    #     rmsprop_dot = Dot(axes.c2p(*start_point), color=GREEN)
    #     adam_dot = Dot(axes.c2p(*start_point), color=YELLOW)

    #     self.play(FadeIn(adagrad_dot), FadeIn(rmsprop_dot), FadeIn(adam_dot))
    #     self.wait(1)

    #     learning_rate = 0.1
    #     epsilon = 1e-8
    #     historical_gradient = np.zeros(2)

    #     for _ in range(10):
    #         x, y, _ = adagrad_dot.get_center()
    #         gradient = grad_func(x, y)
    #         historical_gradient += gradient**2
    #         adjusted_lr = learning_rate / (np.sqrt(historical_gradient) + epsilon)
    #         new_point = np.array([x, y]) - adjusted_lr * gradient
    #         new_adagrad_pos = axes.c2p(new_point[0], new_point[1], func(*new_point))

    #         self.play(
    #             adagrad_dot.animate.move_to(new_adagrad_pos),
    #             run_time=1
    #         )

    #     self.wait(2)
    #     self.play(FadeOut(adagrad_dot), FadeOut(rmsprop_dot), FadeOut(adam_dot), FadeOut(surface), FadeOut(axes)) 