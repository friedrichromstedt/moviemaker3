from moviemaker2.math import MathFunction
from moviemaker2.function import asfunction

class Branch(MathFunction):
    """On being called, the ``Branch`` evaluates a selector, and chooses
    one Function based on the value."""

    def __init__(self, fns, choice):
        """*choice* gives an index into *fns*.  Especially, *fns* might
        be a dictionary, mapping return values onto Functions."""

        self.choice = asfunction(choice)
        self.fns = fns

    def __call__(self, ps):
        """Evaluates ``.choice(ps)`` and calls the appropriate function."""

        choice = self.choice(ps)
        return asfunction(self.fns[choice])(ps)
