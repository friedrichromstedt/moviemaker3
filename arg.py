import copy
from moviemaker2.function import asfunction
from moviemaker2.math import MathFunction

__all__ = ['PositionalArg', 'KwArg']

class Arg(MathFunction):
    """Retrieves and extends argument objects (*args* and *kwargs*)."""
    
    def __init__(self):
        """Derived should overload."""
        pass
    
    def retrieve(self, args, kwargs):
        """Retrieves the arg from the *args* or the *kwargs*.  Notice that in
        this function, *args* and *kwargs* are not used as call parameters,
        but in the sense of ordinary arguments."""

        raise NotImplementedError("Derived must overload")

    def store(self, args, kwargs, arg):
        """Stores the *arg* by extending *args* or *kwargs*.  Notice that in
        this function, *args* and *kwargs* are not used as call parameters, 
        but in the sense of ordinary arguments."""

        raise NotImplementedError("Derived must overload")

class PositionalArg(Arg):
    """Handles a positional argument."""

    def __init__(self, position):
        """*position* is the position index of the argument to be returned
        on call."""
        
        Arg.__init__(self)
        self.position = position

    def retrieve(self, args, kwargs):
        """Returns the indexing result of *args*."""

        return args[self.position]

    def store(self, args, kwargs, arg):
        """Overwrites the index of *args*.  Note that it doesn't extend the
        *args*."""

        args = copy.copy(args)
        args[self.position] = arg
        return (args, kwargs)

    def __call__(self, *args, **kwargs):
        """Returns the positional argument called."""

        return asfunction(self.retrieve(args, kwargs))(*args, **kwargs)

class KwArg(MathFunction):
    """Handles a keyword argument."""

    def __init__(self, keyword):
        """*keyword* is the keyword the argument shall have."""

        self.keyword = keyword

    def retrieve(self, args, kwargs):
        """Returns the value from *kwargs*."""

        return kwargs[self.keyword]

    def store(self, args, kwargs, arg):
        """Overrides or extends *kwargs*."""

        kwargs = copy.copy(kwargs)
        kwargs[self.keyword] = arg
        return (args, kwargs)

    def __call__(self, *args, **kwargs):
        """Returns the keyword argument called."""

        return asfunction(self.retrieve(args, kwargs))(*args, **kwargs)
