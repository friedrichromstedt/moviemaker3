import numpy
from moviemaker2.function import asfunction
from moviemaker2.math import MathFunction

class ScalarProduct(MathFunction):
    """Calculates the scalar product of the mesh points with a given vector
    Function.  Useful for plane wave calculations."""

    def __init__(self, vector, mesh=None):
        """*mesh* is the mesh Function, *vector* the vector Function."""

        self.vector = asfunction(vector)
        self.mesh = asfunction(mesh)

    def __call__(self, *args, **kwargs):
        """Calculates the dot product of each mesh vector and the 
        ``.vector()``."""

        vector = self.vector(*args, **kwargs)
        mesh = self.mesh(*args, **kwargs)

        return numpy.tensorproduct(mesh, vector, (-1, 0))
