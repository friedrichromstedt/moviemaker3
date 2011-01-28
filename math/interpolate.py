import numpy
from moviemaker2.function import Function, asfunction, Constant
from moviemaker2.math import MathFunction

class Interp(MathFunction):
    """The pendant to ``numpy.interp()``."""

    def __init__(self, xp, fp, x, left=None, right=None):
        """Arguments are like for ``numpy.interp()``.  If *left* or *right* 
        is None, *None* is handed over to ``numpy.interp()`` in ``__call__``
        (i.e., ``None`` is not interpreted as the identity Function)."""

        self.xp = asfunction(xp)
        self.fp = asfunction(fp)
        self.x = asfunction(x)
        if left is None:
            self.left = Constant(None)
        else:
            self.left = asfunction(left)
        if right is None:
            self.right = Constant(None)
        else:
            self.right = asfunction(right)

    def __call__(self, *args, **kwargs):
        """Calls ``numpy.interp()`` with ``.xp()``, ``.fp()``, ``.left()``,
        ``.right()``."""

        xp = self.xp(*args, **kwargs)
        fp = self.fp(*args, **kwargs)
        x = self.x(*args, **kwargs)
        left = self.left(*args, **kwargs)
        right = self.right(*args, **kwargs)

        print xp, fp, x
    
        return numpy.interp(xp=xp, fp=fp, x=x, left=left, right=right)

class Spline(MathFunction):
    """Carries out spline interpolation."""

    def __init__(self, points, progress):
        """*points* is a sequence of points of the spline.  *progress* is the
        real-valued [0, 1] progress value of the spline."""

        self.points = asfunction(points)
        self.progress = asfunction(progress)

    def __call__(self, *args, **kwargs):
        """Spline-interpolates the result of ``.points()`` at the position
        ``.progress()``."""

        points = self.points(*args, **kwargs)
        progress = self.progress(*args, **kwargs)

        while(len(points) > 1):
            interpolated_points = []
            for (A, B) in zip(points[:-1], points[1:]):
                # If *points* is a tuple, it will end up as a Constant.
                # But the constituents might be Functions too, so we must 
                # call them.
                A = asfunction(A)(*args, **kwargs)
                B = asfunction(B)(*args, **kwargs)
                interpolated_points.append(A * (1 - progress) + B * progress)
            points = interpolated_points

        return points[0]
