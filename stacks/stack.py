from moviemaker2.math import MathFunction, asmathfunction

class Stack(MathFunction):
    """Base class for stacks with layers."""
    
    def __init__(self):
        """Initialises the ``.layers`` attribute to the empty list."""

        self.layers = []
    
    def __xor__(self, other):
        """Stack *other* onto *self*.  Acts in-place!  This is done so that
        derived classes do not have to overlaod just to get the return class
        right.  Anyway, returns *self*."""
        
        self.layers.append(asmathfunction(other))
        return self

    def add_top(self, other):
        """Stacks *other* onto *self*.  Acts in-place.  Like 
        :meth:`__xor__`."""

        self.layers.append(asmathfunction(other))
        return self

    def add_bottom(self, other):
        """Stacks *other* at the bottom of *self*.  Acts in-place."""

        self.layers = [other] + self.layers
        return self

    def insert(self, index, other):
        """Stacks *other* by insert()'ing it into the layer list.  Acts
        in-place."""

        self.layers.insert(index, other)
        return self

    def remove(self, other):
        """Removes the first occurence of *other* from *self*."""

        self.layers.remove(other)
        return self

    def __delitem__(self, key):
        """Removes the object indexed by *key* from the layer list."""

        del self.layers[key]
        return self
