import numpy
import PIL.Image
from fframework import Function

class PIL(Function):
    """Generates PIL images from numpy ndarrays."""

    def __init__(self, rgbindices=None, aindex=None):
        """*rgbindices* should give the indices for ``R, G, B, A`` to take 
        from the array fed to *self.__call__*.  Default is *rgbindices = 
        [0, 1, 2]*.  If *rgbindices* is ``None``, then the array will be 
        intereted as grayscale, and *aindex* is ignored.  *aindex* is either 
        ``None`` (alpha channel opaque) or the index where to take the alpha 
        channel from."""
        
        if rgbindices is None:
            rgbindices = [0, 1, 2]

        Function.__init__(self)

        self.rgbindices = rgbindices
        self.aindex = aindex

    def __call__(self, layer):
        """*layer* is supposed to be argb data with the colour index in the
        first dimension, y in the second and x in the third.

        Return value is a PIL image.  The input value range is [0, 1]."""

        if self.rgbindices is None:
            ones = numpy.ones_like(layer)
            image = numpy.asarray([layer, layer, layer, ones])
        else:
            if self.aindex is None:
                alpha = numpy.ones(layer.shape[1:])
            else:
                alpha = layer[self.aindex]
            image = numpy.asarray([layer[index] \
                for index in self.rgbindices] + [alpha])

        # [band, y, x] -> [y, x, band]:
        image = numpy.rollaxis(image, 0, 3)
        # value in [0, 1]:
        image = image.clip(0, 1)

        return PIL.Image.fromarray((image * 255).astype(numpy.uint8))
