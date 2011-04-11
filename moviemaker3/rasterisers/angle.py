import numpy
from fframework import asfunction, OpFunction

class Angle(OpFunction):
    """Transforms a mesh into the angle of the mesh to the x axis."""

    def __init__(self, mesh=None):
        """*mesh* is the mesh Function."""

        self.mesh = asfunction(mesh)

    def __call__(self, ps):
        """Returns the arctan2."""

        mesh = self.mesh(ps)

        return numpy.arctan2(mesh[..., 0], mesh[..., 1])
