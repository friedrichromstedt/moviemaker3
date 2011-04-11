from moviemaker2.math import MathFunction

__all__ = ['p']

class Ps:
    """Holds a number of parameter values."""
    
    def __init__(self, parameters=None):
        """*parameters* is a dictionary ``{name: value}``."""

        if parameters is None:
            parameters = {}
        self.parameters = parameters

    def extended(self, name, value):
        """Returns *self* copied and extended by ``name: value``."""

        parameters = self.parameters.copy()
        parameters[name] = value
        return Ps(parameters)

    def retrieve(self, name):
        """Retrieves the value of *name*."""

        return self.parameters[name]

class p(MathFunction):
    """Accesses a parameter by name."""
    
    def __init__(self, name):
        """Access will be done for parameter named *name*."""

        self.name = name

    def __call__(self, ps):
        """Returns the parameter value in *ps*."""

        return ps.retrieve(self.name)

    def store(self, ps, value):
        """Extends *ps* by *value*."""

        return ps.extended(self.name, value)
