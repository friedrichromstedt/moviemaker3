import numpy
from fframework import asfunction, OpFunction

class Distance(OpFunction):
    """Calculates the distance in a mesh from the origin."""

    def __init__(self, mesh=None):
        """*mesh* is the mesh generator."""

        self.mesh = asfunction(mesh)

    def __call__(self, ps):
        """Returns the distance of the points of the mesh from the origin."""

        mesh = self.mesh(ps)

        return numpy.sqrt((mesh ** 2).T.sum(axis=0).T)
