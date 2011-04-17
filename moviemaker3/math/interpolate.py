import numpy
from fframework import Function, asfunction, Constant, OpFunction

class Interp(OpFunction):
    """The pendant to ``numpy.interp()``."""

    def __init__(self, xp, fp, x, left=None, right=None):
        """Arguments are like for ``numpy.interp()``.  If *left* or *right* 
        is None, *None* will be handed over to ``numpy.interp()``."""

        self.xp = asfunction(xp)
        self.fp = asfunction(fp)
        self.x = asfunction(x)
        self.left = asfunction(left)
        self.right = asfunction(right)

    def __call__(self, ps):
        """Calls ``numpy.interp()`` with ``.xp(ps)``, ``.fp(ps)``, 
        ``.left(ps)``, ``.right(ps)``."""

        xp = self.xp(ps)
        fp = self.fp(ps)
        x = self.x(ps)
        left = self.left(ps)
        right = self.right(ps)

        return numpy.interp(xp=xp, fp=fp, x=x, left=left, right=right)

class Bezier(OpFunction):
    """Carries out Bezier interpolation."""

    def __init__(self, points, progress):
        """*points* is a sequence of points of the Bezier curve.  *progress* 
        is the real-valued [0, 1] progress value of the Bezier curve.
        
        The constituents of *points* must be Functions (callable).  So you
        might use ``fframework.compound()`` to generate a list or a tuple
        consisting of OpFunctions."""

        self.points = asfunction(points)
        self.progress = asfunction(progress)

    def __call__(self, ps):
        """Bezier-interpolates the result of ``.points(ps)`` at the position
        ``.progress(ps)``."""

        points = self.points(ps)
        progress = self.progress(ps)

        while(len(points) > 1):
            interpolated_points = []
            for (Afunc, Bfunc) in zip(points[:-1], points[1:]):
                A = Afunc(ps)
                B = Bfunc(ps)
                interpolated_points.append(A * (1 - progress) + B * progress)
            points = interpolated_points

        return points[0]
