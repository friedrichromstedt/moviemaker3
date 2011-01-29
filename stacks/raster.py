from moviemaker2.math import MathFunction, asmathfunction

#
#   Layers are simply Functions yielding ``nchannel x channelshape``
#   ndarrays.
#

#
#   Stacks can be used as layers.
#

class AdditiveRasterStack(MathFunction):
    
    def __init__(self, background):

        self.background = asmathfunction(background)
        self.layers = []

    # Stacking ...

    def __xor__(self, other):
        """Stack *other* onto *self*.  Acts in-place!  This is done so that
        derived classes do not have to overlaod just to get the return class
        right.  Anyway, returns *self*."""
        
        self.layers.append(asmathfunction(other))
        return self

    def __call__(self, ps):
        """Adds up the layers."""

        result = self.background(ps)
        for layer in self.layers:
            result = result + layer(ps)
        return result

class AlphaBlendRasterStack(MathFunction):
    
    def __init__(self, background):
        
        self.background = asmathfunction(background)
        self.layers = []

    # Stacking ...

    def __xor__(self, other):
        """Stack *other* onto *self*.  Returns *self*."""

        self.layers.append(asmathfunction(other))
        return self

    def __call__(self, ps):
        """Blends the layers one after the other.  The alpha channel is the
        first channel."""
        
        result = self.background(ps)
        for layer in self.layers:
            layerdata = layer(ps)
            alpha = layerdata[0]
            result = result * (1 - alpha) + layerdata
        return result
