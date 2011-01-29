from moviemaker2.math import MathFunction

__all__ = ['p']

class Ps:
    
    def __init__(self, parameters=None):
        if parameters is None:
            parameters = {}
        self.parameters = parameters

    def extended(self, name, value):
        parameters = self.parameters.copy()
        parameters[name] = value
        return Ps(parameters)

    def retrieve(self, name):
        return self.parameters[name]

class p(MathFunction):
    
    def __init__(self, name):
        self.name = name

    def __call__(self, ps):
        return ps.retrieve(self.name)

    def store(self, ps, value):
        return ps.extended(self.name, value)
