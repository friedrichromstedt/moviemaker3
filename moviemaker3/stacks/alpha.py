from fframework import asfunction
from moviemaker3.stacks.stack import Stack

__all__ = ['AlphaStack']

class AlphaStack(Stack):
    r"""The formula used for combination of layer `i` using layer `i + 1` is:

    .. math::
        
        X = X_i (1 - \alpha_{i + 1}) + X_{i + 1} \alpha_{i + 1}

    where `X` is a Layer.
    
    Elements in the AlphaStack should return (*alpha*, *layer*); *layer* and 
    *alpha* are extracted by indexing (tuple assignment).  You might use 
    ``fframework.compound()`` to generate tuple Functions."""
    
    def __init__(self, background):
        """The *background* yields the background layer, no alpha."""
        
        Stack.__init__(self)
        self.background = asfunction(background)

    def __call__(self, ps):
        """Blends the layers one after the other.  Returns the result 
        layer, no alpha."""
        
        resultlayer = self.background(ps)
        for layer in self.elements:
            (alpha, layer) = layer(ps)
            resultlayer = resultlayer * (1 - alpha) + layer * alpha
        return resultlayer
