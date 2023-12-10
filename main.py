from manim import *

# Importieren Sie hier Ihre eigenen Klassendefinitionen
from introduction import Introduction
from function_plot import FunctionPlot
from initialization import Initialization
from gradient_calculation import GradientCalculation
from update_step import UpdateStep
from iteration import Iteration
from convergence import Convergence
from conclusion import Conclusion

# Fügen Sie die Szenen in der gewünschten Reihenfolge hinzu
class StochasticGradientDescent(Scene):
    def construct(self):
        # Fügen Sie jede Szene hinzu, die Sie rendern möchten
        self.add(Introduction())
        self.add(FunctionPlot())
        self.add(Initialization())
        self.add(GradientCalculation())
        self.add(UpdateStep())
        self.add(Iteration())
        self.add(Convergence())
        self.add(Conclusion())

# Führen Sie das Skript mit Manim aus
if __name__ == "__main__":
    # Führen Sie Manim mit der gewünschten Konfiguration aus
    # Beispiel: manim -pql main.py StochasticGradientDescent