from fframework import OpFunction, asfunction
from moviemaker3.extension import Extension

class Multid(OpFunction):

    def __init__(self, target, stack, values, p):
        """*values* is an iterable.  There will be as many layers superimposed 
        as there are items in *values*.  *p* is used to store the values from
        *values*.  
        
        Each value is stored by an Extension using *p*, and the result is fed
        to the *target*.  The stack will contain elements for each such
        combination."""

        self.stack = stack
        
        for value in values:
            # Feed the extension result to the target:
            extended = Extension(value=value, p=p) | target
            # Stack ``extended``:
            self.stack ^ extended

    def __call__(self, ps):
        
        return self.stack(ps)
