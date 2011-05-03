from fframework import OpFunction, asfunction

__all__ = ['Stack']

class Stack(OpFunction):
    """Base class for stacks with layers.  Stacks can be used as layers."""
    
    def __init__(self):
        """Initialises the ``.elements`` attribute to the empty list."""

        self.elements = []
    
    def __xor__(self, other):
        """Stack *other* onto *self*.  Acts in-place!  This is done so that
        derived classes do not have to overlaod just to get the return class
        right.  Anyway, returns *self*."""
        
        self.elements.append(asfunction(other))
        return self

    def add_top(self, other):
        """Stacks *other* onto *self*.  Acts in-place.  Returns the added
        element."""

        other_fn = asfunction(other)
        self.elements.append(other_fn)
        return other_fn

    def add_bottom(self, other):
        """Stacks *other* at the bottom of *self*.  Acts in-place.  Returns
        the added element."""

        other_fn = asfunction(other)
        self.elements = [other_fn] + self.elements
        return other_fn

    def insert(self, index, other):
        """Stacks *other* by insert()'ing it into the layer list.  Acts
        in-place.  Returns the inserted element."""

        other_fn = asfunction(other)
        self.elements.insert(index, other_fn)
        return other_fn

    def remove(self, other):
        """Removes the first occurence of *other* from *self*.  Returns 
        *self*."""

        self.elements.remove(other)
        return self

    def __delitem__(self, key):
        """Removes the object indexed by *key* from the layer list.  Returns
        nothing."""

        del self.elements[key]
