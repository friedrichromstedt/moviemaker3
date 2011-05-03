from fframework import asfunction
from moviemaker3.stacks.stack import Stack

__all__ = ['AdditiveStack']

class AdditiveStack(Stack):
    
    def __init__(self, background):

        Stack.__init__(self)
        self.background = asfunction(background)

    def __call__(self, ps):
        """Adds up the elements."""

        result = self.background(ps)
        for layer in self.elements:
            result = result + layer(ps)
        return result
