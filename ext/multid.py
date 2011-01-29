from moviemaker2.math import MathFunction
from moviemaker2.function import asfunction
from moviemaker2.extension import Extension

class Multid(MathFunction):

    def __init__(self, target, stack, values, p):
        """*values* is an iterable.  There will be as many layers superimposed 
        as there are items in *values*.  *p* is used to store the values from
        *values*.  For each value, an Extension is generated, with that value,
        which is appended to the *stack* on call time.  *target* is the 
        supplier of layers called for each *value* by one of the 
        Extensions."""

        self.stack = stack
        
        for value in values:
            value = asfunction(value)
            extension = Extension(target=target, value=value, p=p)
            self.stack = self.stack ^ extension

    def __call__(self, ps):
        
        return self.stack(ps)
