import numpy
import matplotlib.figure
import matplotlayers
import matplotlayers.backends.PIL
from moviemaker2.math import MathFunction

class MatplotlibRGB(MathFunction):
    
    def __init__(self):
        """Initialises the figure."""
        
        self.figure = matplotlib.figure.Figure()
        self.stack = matplotlayers.Stack(self.figure, left=-1, bottom=-1, 
            width=3, height=3)
        #self.stack = matplotlayers.Stack(self.figure)
        self.stack.set_xlim((-1, 2))
        self.stack.set_ylim((-1, 2))

        self.mpl_layer = matplotlayers.LayerImshow()
        self.stack.add_layer(self.mpl_layer)

        self.backend = matplotlayers.backends.PIL.FigureCanvasPIL(
            self.figure)

    def __call__(self, layer):
        """*layer* is supposed to be argb data with the colour index in the
        first dimension, y in the second and x in the third.
        
        Return value is a PIL image."""

        image = numpy.rollaxis(layer[1:], 0, 3).clip(0, 1)

        self.mpl_layer.configure(X=image, 
            aspect=(float(image.shape[0]) / float(image.shape[1])))
        # mpl leaves the first pixel blank (prolly for image stacking)
        self.mpl_layer.configure(extent=(-1.0/image.shape[1], 1,
            -1.0/image.shape[0], 1))
        self.stack.render()
        
        return self.backend.output_PIL(shape=image.shape[:2][::-1])
