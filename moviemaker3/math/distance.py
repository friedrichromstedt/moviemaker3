import numpy
from fframework import asfunction, OpFunction

__all__ = ['Distance']

class Distance(OpFunction):
    """Calculates the distance in a mesh from the origin."""

    def __init__(self, mesh=None):
        """*mesh* is the mesh generator."""

        self.mesh = asfunction(mesh)

    def __call__(self, ps):
        """Returns the distance of the points of the mesh from the origin.
        
        The spacial coordinates are in the last dimension."""

        meshT = self.mesh(ps).T

        return numpy.sqrt((meshT ** 2).sum(axis=0)).T
