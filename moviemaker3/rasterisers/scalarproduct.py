import numpy
from fframework import asfunction, OpFunction

class ScalarProduct(OpFunction):
    """Calculates the scalar product of the mesh points with a given vector
    Function.  Useful for plane wave calculations."""

    def __init__(self, vector, mesh=None):
        """*mesh* is the mesh Function, *vector* the vector Function."""

        self.vector = asfunction(vector)
        self.mesh = asfunction(mesh)

    def __call__(self, ps):
        """Calculates the dot product of each mesh vector and the 
        ``.vector()``."""

        vector = self.vector(ps)
        mesh = self.mesh(ps)

        return numpy.tensorproduct(mesh, vector, (-1, 0))
