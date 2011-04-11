import numpy
import PIL.Image
from fframework import Function

class PILfromARGB(Function):
    """Generates PIL images from numpy ndarrays."""

    def __init__(self):
        Function.__init__(self)

    def __call__(self, layer):
        """*layer* is supposed to be argb data with the colour index in the
        first dimension, y in the second and x in the third.

        Return value is a PIL image.  The value range is [0, 1]."""

        # RGBA data: [band, y, x]
        image = numpy.asarray([layer[1], layer[2], layer[3], layer[0]])
        # [y, x, band]:
        image = numpy.rollaxis(image, 0, 3)
        # value in [0, 1]:
        image = image.clip(0, 1)

        return PIL.Image.fromarray((image * 255).astype(numpy.uint8))
