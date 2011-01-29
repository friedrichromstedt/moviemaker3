from moviemaker2.math import MathFunction
from moviemaker2.function import asfunction

class Extension(MathFunction):
    
    def __init__(self, target, value, p):
        self.target = asfunction(target)
        self.value = asfunction(value)
        self.p = p

    def __call__(self, ps):
        value = self.value(ps)
        ps_ext = self.p.store(ps, value=value)
        return self.target(ps_ext)
