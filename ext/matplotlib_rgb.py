import numpy
import matplotlib.figure
import matplotlayers
import matplotlayers.backends.PIL
import moviemaker2.layer

class MatplotlibRGB(moviemaker2.layer.Layer):
    
    # Overload Layer.__init__:
    def __init__(self):
        moviemaker2.layer.Layer.__init__(self)
    
    def accumulate(self, layer):
        return BoundMatplotlibRGB(layer)

class BoundMatplotlibRGB(moviemaker2.layer.Layer):

    def __init__(self, layer):
        """Initialises the figure."""
        
        moviemaker2.layer.Layer.__init__(self)

        self.layer = layer

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

    def __call__(self, *args, **kwargs):
        """Calls the layer."""

        called = self.layer(*args, **kwargs)

        R = called.get_channel('R').data()
        G = called.get_channel('G').data()
        B = called.get_channel('B').data()

        image = numpy.rollaxis(numpy.asarray([R, G, B]), 0, 3).clip(0, 1)
        #image = numpy.rollaxis(image, 0, 2)
        #print image.shape

        self.mpl_layer.configure(X=image, 
            aspect=(float(image.shape[0]) / float(image.shape[1])))
        # mpl leaves the first pixel blank (prolly for image stacking)
        self.mpl_layer.configure(extent=(-1.0/image.shape[1], 1,
            -1.0/image.shape[0], 1))
        self.stack.render()
        
        return self.backend.output_PIL(shape=image.shape[:2][::-1])
