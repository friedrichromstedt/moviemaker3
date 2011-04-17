import numpy
from fframework import asfunction, OpFunction

__all__ = ['Angle']

class Angle(OpFunction):
    """Transforms a mesh into the angle of the mesh to the x axis."""

    def __init__(self, mesh):
        """*mesh* is the mesh Function."""

        self.mesh = asfunction(mesh)

    def __call__(self, ps):
        """Returns the arctan2.  The (y, x) coordinate is in the last 
        dimension."""

        meshT = self.mesh(ps).T
        return numpy.arctan2(meshT[0], meshT[1]).T
