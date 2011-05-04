import matplotlayers.backends.PIL
from fframework import OpFunction

class Mpl2PIL(OpFunction):
    """Generates PIL images from a matplotlib Figure."""

    def __init__(self, figure, shape):
        """*figure* is the :class:`matplotlib.figure.Figure` to process.

        *shape* is the shape ``(shapey, shapex)`` of the resulting image
        in pixels.  It is a :class:`moviemaker3.p`."""

        self.figure = figure
        self.backend = matplotlayers.backends.PIL.FigureCanvasPIL(figure)
        self.shape = shape

    def __call__(self, ps):
        """Renders the figure."""

        shape = self.shape(ps)

        image = self.backend.output_PIL(shape)
        return image
