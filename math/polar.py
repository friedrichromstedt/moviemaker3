"""
Provides conversion between polar and cartesian coordinates.
"""

import numpy
from moviemaker2.function import asfunction
from moviemaker2.math.primitive import MathFunction

__all__ = ['Polar2DtoCartesian2D', 'Cartesian2DtoPolar2D']

class Polar2DtoCartesian2D(MathFunction):
    """Computes cartesian 2D coordinates from 2D polar coordinates."""

    def __init__(self, r, phi):
        """*r* and *phi* are the polar coordinates."""

        self.r = asfunction(r)
        self.phi = asfunction(phi)

    def __call__(self, *args, **kwargs):
        """Calculates the cartesian coordinates from the polar coordinates.
        The result of *r* and *phi* must be of compatible shape.
        
        Return a ndarray ``[y, x]``."""

        r = self.r(*args, **kwargs)
        phi = self.phi(*args, **kwargs)

        return numpy.asarray([numpy.sin(phi), numpy.cos(phi)]) * r

class Cartesian2DtoPolar2D(MathFunction):
    """Calculates 2D polar coordinates from 2D cartesian coordinates."""

    def __init__(self, y, x):
        """*x* and *y* are the cartesian coordinates."""

        self.y = asfunction(y)
        self.x = asfunction(x)

    def __call__(self, *args, **kwargs):
        """Calculates the polar coordaintes from the cartesian coordinates.

        The value of *x* and *y* must at least be of compatible shape.
    
        The angle is calculates mathematically positive starting in the 
        direction os +x with phi=0.
        
        Returns a ndarray ``[r, phi]``"""

        y = self.y(*args, **kwargs)
        x = self.x(*args, **kwargs)

        r = numpy.sqrt(y ** 2 + x ** 2)
        phi = numpy.arctan2(y, x)
        
        return numpy.asarray([r, phi])
