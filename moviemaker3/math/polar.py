"""Provides conversion between polar and cartesian coordinates."""

import numpy
from fframework import asfunction, OpFunction

__all__ = ['Polar2Cartesian', 'Cartesian2Polar']

class Polar2Cartesian(OpFunction):
    """Computes cartesian 2D coordinates from 2D polar coordinates."""

    def __init__(self, mesh=None):
        """*mesh* is in polar coordinates (r, phi).  This spacial coordinates
        are in the last dimension of the mesh."""

        self.mesh = asfunction(mesh)

    def __call__(self, ps):
        """Calculates the cartesian coordinates (y, x) from the polar 
        coordinates.  The spacial (y, x) coordinaates will be in the last
        dimension of the returned array."""

        meshT = self.mesh(ps).T

        rT = meshT[0]
        phiT = meshT[1]

        return (numpy.asarray([numpy.sin(phiT), numpy.cos(phiT)]) * rT).T

class Cartesian2Polar(OpFunction):
    """Calculates 2D polar coordinates (r, phi) from 2D cartesian coordinates 
    (y, x)."""

    def __init__(self, mesh=None):
        """*mesh* is in cartesian coordinates (y, x).  The (y, x) coordinates
        are in the last dimension of the mesh."""

        self.mesh = asfunction(mesh)

    def __call__(self, ps):
        """Calculates the polar coordinates (r, phi) from the cartesian 
        coordinates.  The (r, phi) coordinates will be in the last dimension
        of the array returned."""
        
        meshT = self.mesh(ps).T

        yT = meshT[0]
        xT = meshT[1]

        rT = numpy.sqrt(yT ** 2 + xT ** 2)
        phiT = numpy.arctan2(yT, xT)
        
        return numpy.asarray([rT, phiT]).T
