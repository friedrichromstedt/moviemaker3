import numpy
from moviemaker2.function import asfunction
from moviemaker2.math import MathFunction

class Distance(MathFunction):
    """Calculates the distance in a mesh from the origin."""

    def __init__(self, mesh=None):
        """*mesh* is the mesh generator."""

        self.mesh = asfunction(mesh)

    def __call__(self, *args, **kwargs):
        """Returns the distance of the points of the mesh from the origin."""

        mesh = self.mesh(*args, **kwargs)

        return numpy.sqrt((mesh ** 2).T.sum(axis=0).T)
