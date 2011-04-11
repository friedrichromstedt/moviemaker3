from fframework import OpFunction, asfunction
from moviemaker3.stacks.stack import Stack

#
#   Layers are simply Functions yielding ``nchannel x channelshape``
#   ndarrays.
#

#
#   Stacks can be used as layers.
#

class AdditiveRasterStack(Stack):
    
    def __init__(self, background):

        Stack.__init__(self)
        self.background = asfunction(background)

    def __call__(self, ps):
        """Adds up the layers."""

        result = self.background(ps)
        for layer in self.layers:
            result = result + layer(ps)
        return result

class AlphaBlendRasterStack(Stack):
    
    def __init__(self, background):
        
        Stack.__init__(self)
        self.background = asfunction(background)

    def __call__(self, ps):
        """Blends the layers one after the other.  The alpha channel is the
        first channel."""
        
        result = self.background(ps)
        for layer in self.layers:
            layerdata = layer(ps)
            alpha = layerdata[0]
            result = result * (1 - alpha) + layerdata
        return result
