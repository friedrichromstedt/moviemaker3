from fframework import asfunction
from moviemaker3.stacks.stack import Stack

class WeightedStack(Stack):
    """Elements in the WeightedStack should return (*weight*, *layer*); 
    *layer* and *weight* are extracted by indexing (tuple assignment).  You 
    might use ``fframework.compound()`` to generate tuple Functions."""
    
    def __init__(self, zero_layer=None, zero_weight=None):
        """*zero_layer* is the 0 to use in summing up the layers (the start 
        value), it defaults to 0.
        
        *zero_weight* is the 0 to use in summing up the weights, it default to
        0, too."""

        if zero_layer is None:
            zero_layer = 0
        if zero_weight is None:
            zero_weight = 0

        Stack.__init__(self)
        self.zero_layer = asfunction(zero_layer)
        self.zero_weight = asfunction(zero_weight)

    def __call__(self, ps):
        """Blends the layers together.  Note that if all weights are zero,
        the result is undefined.  The start value for summing up the layers
        is *self.zero_layer*.  The start value for summing up the weights is
        *self.zero_weight*.  Both are evaluated with *ps*."""
        
        sumlayer = self.zero_layer(ps)
        weightsum = self.zero_weight(ps)
        for layer in self.elements:
            (weight, layer) = layer(ps)
            # We don't use augmented arithmetics because we might want to
            # employ broadcasting.
            sumlayer = sumlayer + weight * layer
            weightsum = weight + weightsum
        return sumlayer / weightsum
