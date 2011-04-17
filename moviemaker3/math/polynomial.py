from fframework import OpFunction, asfunction, Constant

class Polynomial(OpFunction):
    """Implements polynomials with Functions a coefficients and argument."""

    def __init__(self, coefficients, x=None, null=None):
        """*coefficients* gives the coefficients of the polynomial.  *x* gives
        the argument of the polynomial.  *null* is the null with respect to
        +, and ``None`` means ordinary 0.0."""

        self.coefficients = asfunction(coefficients)
        self.x = asfunction(x)

        if null is None:
            self.null = Constant(0.0)
        else:
            self.null = asfunction(null)

    def __call__(self, ps):
        """Returns the polynomial specified by ``.coefficients()`` at the
        position ``.x()``."""

        coefficients = self.coefficients(ps)
        x = self.x(ps)
        null = self.null(ps)

        result = null
        for (order, coefficient) in enumerate(coefficients):
            result += coefficient * x ** order

        return result
