"""
Provides conversion between polar and cartesian coordinates.
"""

import numpy
from fframework import asfunction, OpFunction

__all__ = ['Polar2DtoCartesian2D', 'Cartesian2DtoPolar2D']

class Polar2DtoCartesian2D(OpFunction):
    """Computes cartesian 2D coordinates ``[y, x]`` from 2D polar 
    coordinates ``[r, phi]``."""

    def __init__(self, mesh=None):
        """*mesh* is in polar coordinates ``[r, phi]``."""

        self.mesh = asfunction(mesh)

    def __call__(self, *args, **kwargs):
        """Calculates the cartesian coordinates ``[y, x]`` from the polar 
        coordinates."""

        mesh = self.mesh(*args, **kwargs)

        r = mesh[0]
        phi = mesh[1]

        return numpy.asarray([numpy.sin(phi), numpy.cos(phi)]) * r

class Cartesian2DtoPolar2D(OpFunction):
    """Calculates 2D polar coordinates ``[r, phi]`` from 2D cartesian 
    coordinates ``[y, x]``."""

    def __init__(self, mesh=None):
        """*mesh* is in cartesian coordinates ``[y, x]``."""

        self.mesh = asfunction(mesh)

    def __call__(self, *args, **kwargs):
        """Calculates the polar coordinates ``[r, phi]`` from the cartesian 
        coordinates ``[y, x]``.

        The angle is calculated mathematically positive starting in the 
        direction os :math:`+x` with phi=0."""
        
        mesh = self.mesh(*args, **kwargs)

        y = mesh[0]
        x = mesh[1]

        r = numpy.sqrt(y ** 2 + x ** 2)
        phi = numpy.arctan2(y, x)
        
        return numpy.asarray([r, phi])
