"""
The primitive arithmetic operations must be overloaded in the class definition
directly, and therefore the returned Functions are defined in this module too,
and not in :mod:`moviemaker.math` where they belong to.  Nevertheless they 
will be available through the :mod:`moviemaker.math` module, too.
"""

import numpy
from moviemaker2.function import Function, Constant, Identity, asfunction

# All other Function can be accessed more clearly by ordinary means or by
# using numpy functions (numpy.sin, numpy.cos):
__all__ = ['MathFunction', 'asmathfunction', 'asmathfunctionv', 'asarray',
    'Less', 'Greater', 'LessEqual', 'GreaterEqual', 'Equal', 'Not']

class MathFunction(Function):
    """
    Supports overloaded primitve arithmetics.  Can wrap an ordinary 
    Function, to extend it by math overloads.

    Examples:  (fXXX is a function for something "XXX")

    1)  ``fa + fb``, etc.
    2)  ``numpy.cos(fangle)``.  This works through the :meth:`cos` method.
        Same for ``numpy.sin(fangle)``.
    3)  ``numpy.sum(farray, axis=1)``.  This works through the :meth:`sum`
        method.
    """
    def __init__(self, wrap):
        """*wrap* is an ordinary Function, being used during __call__."""

        self.wrap = wrap

    def __call__(self, *args, **kwargs):
        """Calls just ``.wrap``."""

        return self.wrap(*args, **kwargs)

    def __add__(self, other):
        """Returns the :class:`Sum` with another Function."""

        other = asfunction(other)
        return Sum(self, other)

    def __radd__(self, other):
        """Returns the :class:`Sum` with another Function."""

        other = asfunction(other)
        return Sum(other, self)

    def __sub__(self, other):
        """Returns the :class:`Sum` with the negative of the other 
        Function."""

        other = asfunction(other)
        return Sum(self, -other)

    def __rsub__(self, other):
        """Returns the :class:`Sum` of the other Function with the negative of
        ``self``."""

        other = asfunction(other)
        return Sum(other, -self)

    def __mul__(self, other):
        """Returns the :class:`Product` with the other Function."""

        other = asfunction(other)
        return Product(self, other)

    def __rmul__(self, other):
        """Returns the :class:`Product` of the other Function with 
        ``self``."""

        other = asfunction(other)
        return Product(other, self)

    def __div__(self, other):
        """Returns the :class:`Quotient` with the other Function."""

        other = asfunction(other)
        return Quotient(self, other)

    def __rdiv__(self, other):
        """Returns the :class:`Quotient` of the other Function with 
        ``self``."""

        other = asfunction(other)
        return Quotient(other, self)

    def __pow__(self, exponent):
        """Raises ``self`` to the power of the other Function."""

        exponent = asfunction(exponent)
        return Power(base=self, exponent=exponent)

    def __rpow__(self, base):
        """Raises the other Function to the power of ``self``."""

        base = asfunction(base)
        return Power(base=base, exponent=self)

    def __pos__(self):
        """Returns ``self``."""

        return self

    def __neg__(self):
        """Returns the :class:`Nagative` of ``self``."""

        return Neg(invertible=self)

    def sin(self):
        """Takes the sine."""

        return Sin(self)

    def cos(self):
        """Takes the cosine."""

        return Cos(self)

    def exp(self):
        """Exponentiates."""

        return Exp(self)

    def sum(self, *args, **kwargs):
        """Returns a :class:`Sum` of self with the arguments for calling
        ``.sum()`` given by the arguments given here."""

        return SumCall(array=self, *args, **kwargs)

    def clip(self, low, high):
        """Returns a :class:`Clip` instance of ``self`` with *low* and *high* 
        set up."""

        return Clip(leaf=self, low=low, high=high)

    def astype(self, *args, **kwargs):
        """Returns a :class:`asarray` instance of ``self`` with *args* and
        *kwargs* handed over.  Can be used for converting to other dtypes::

            func.astype(dtype=numpy.int)
        """

        return asarray(array_like=self, *args, **kwargs)

    def __getitem__(self, index):
        """Returns a :class:`Indexing` instance of ``self`` with *index* set
        up."""

        return Indexing(items=self, index=index)

    def __or__(self, other):
        """Piping is composition of Functions.  The pipe operator is designed
        such that the wrapping function is written last: *other* will be 
        executed with the ouput of *self* as input."""

        return MathComposedFunction(a=self, b=other)

class MathComposedFunction(MathFunction):
    """Executes one function with the output of another."""

    def __init__(self, a, b):
        """*b* will be executed with the output of *a* as input."""

        self.a = asfunction(a)
        self.b = asfunction(b)
    
    def __call__(self, *args, **kwargs):
        return self.b(self.a(*args, **kwargs))

class MathConstant(Constant, MathFunction):
    """:class:`~moviemaker2.function.Constant`, extended by mathematical
    overloads."""

    pass

class MathIdentity(Identity, MathFunction):
    """:class:`~moviemaker2.function.Identity`, extended by mathatical
    overloads."""

    pass

def asmathfunction(mathfunction_like):
    """
    *   If *mathfunction_like* is a :class:`MathFunction`, it is returned 
        unchanged.
    *   If *mathfunction_like* is a :class:`~moviemaker2.function.Function`,
        ``MathFunction(mathfunction_like)`` is returned.
    *   If *function_like* is None, a :class:`MathIdentity` is returned.
    *   Else, the *function_like* is interpreted as a :class:`MathConstant`.

    For ``asmathfunctionv()``, ``asmathfunction()`` is applied on any element
    of an array_like argument.
    """

    if isinstance(mathfunction_like, Function):
        return mathfunction_like
    elif mathfunction_like is None:
        return MathIdentity()
    else:
        return MathConstant(mathfunction_like)

asmathfunctionv = numpy.vectorize(asmathfunction)

class Sum(MathFunction):
    """
    Abstract sum Function.
    """
    
    def __init__(self, one, two):
        
        self.one = asfunction(one)
        self.two = asfunction(two)

    def __call__(self, *args, **kwargs):
        
        return self.one(*args, **kwargs) + self.two(*args, **kwargs)

class Product(MathFunction):
    """
    Abstract product Function.
    """
    
    def __init__(self, one, two):
        
        self.one = asfunction(one)
        self.two = asfunction(two)

    def __call__(self, *args, **kwargs):
        
        return self.one(*args, **kwargs) * self.two(*args, **kwargs)

class Quotient(MathFunction):
    """
    Abstract quotient Function.
    """
    
    def __init__(self, one, two):
        
        self.one = asfunction(one)
        self.two = asfunction(two)

    def __call__(self, *args, **kwargs):
        
        return self.one(*args, **kwargs) / self.two(*args, **kwargs)

class Cmp(MathFunction):
    """
    Abstract comparison Function.
    """

    def __init__(self, A, B):
        
        self.A = asfunction(A)
        self.B = asfunction(B)

    def __call__(self, *args, **kwargs):
        
        return cmp(self.A(*args, **kwargs), self.B(*args, **kwargs))

class Less(MathFunction):
    """
    Abstract comparison Function.
    """

    def __init__(self, A, B):
        
        self.A = asfunction(A)
        self.B = asfunction(B)

    def __call__(self, *args, **kwargs):
        
        return self.A(*args, **kwargs) < self.B(*args, **kwargs)

class Greater(MathFunction):
    """
    Abstract comparison Function.
    """

    def __init__(self, A, B):
        
        self.A = asfunction(A)
        self.B = asfunction(B)

    def __call__(self, *args, **kwargs):
        
        return self.A(*args, **kwargs) > self.B(*args, **kwargs)

class LessEqual(MathFunction):
    """
    Abstract comparison Function.
    """

    def __init__(self, A, B):
        
        self.A = asfunction(A)
        self.B = asfunction(B)

    def __call__(self, *args, **kwargs):
        
        return self.A(*args, **kwargs) <= self.B(*args, **kwargs)

class GreaterEqual(MathFunction):
    """
    Abstract comparison Function.
    """

    def __init__(self, A, B):
        
        self.A = asfunction(A)
        self.B = asfunction(B)

    def __call__(self, *args, **kwargs):
        
        return self.A(*args, **kwargs) >= self.B(*args, **kwargs)

class Equal(MathFunction):
    """
    Abstract comparison Function.
    """

    def __init__(self, A, B):
        
        self.A = asfunction(A)
        self.B = asfunction(B)

    def __call__(self, *args, **kwargs):
        
        return self.A(*args, **kwargs) == self.B(*args, **kwargs)

class Not(MathFunction):
    """
    Abstract comparison Function.
    """

    def __init__(self, A):
        
        self.A = asfunction(A)

    def __call__(self, *args, **kwargs):
        
        return not self.A(*args, **kwargs)

class Power(MathFunction):
    """
    Abstract power Function.
    """
    
    def __init__(self, base, exponent):
        
        self.base = asfunction(base)
        self.exponent = asfunction(exponent)

    def __call__(self, *args, **kwargs):
        
        return self.base(*args, **kwargs) ** self.exponent(*args, **kwargs)

class Neg(MathFunction):
    """
    Abstract negative Function.
    """
    
    def __init__(self, invertible):
        
        self.invertible = asfunction(invertible)

    def __call__(self, *args, **kwargs):
        
        return -self.invertible(*args, **kwargs)

class Cos(MathFunction):
    """Takes the cosine."""

    def __init__(self, angle=None):
        """The value of *angle* is in radians."""

        self.angle = asfunction(angle)

    def __call__(self, *args, **kwargs):
        """Calculates the cosine of the value of *angle* using 
        ``numpy.cos``."""

        angle = self.angle(*args, **kwargs)
        return numpy.cos(angle)

class Sin(MathFunction):
    """Takes the sine."""

    def __init__(self, angle=None):
        """The value of *angle* is in radians."""

        self.angle = asfunction(angle)

    def __call__(self, *args, **kwargs):
        """Calculates the sine of the value of *angle* using 
        ``numpy.sin``."""

        angle = self.angle(*args, **kwargs)
        return numpy.sin(angle)

class Exp(MathFunction):
    """Exponentiates."""

    def __init__(self, exponent=None):
        """*exponent* is used as the argument to ``numpy.exp()``."""

        self.exponent = asfunction(exponent)

    def __call__(self, *args, **kwargs):
        """Calculates ``exp()`` of ``.exponent()``."""

        exponent = self.exponent(*args, **kwargs)
        return numpy.exp(exponent)

class SumCall(MathFunction):
    """Calles ``.sum()`` with predefined arguments.  This is intended for
    use with ndarray-values Functions."""
    
    def __init__(self, array, *sum_args, **sum_kwargs):
        """The value of *array* must have a ``.sum`` method.  The sum() method
        will be called on call time with the arguments and kwargs given."""

        self.array = asfunction(array)
        self.sum_args = sum_args
        self.sum_kwargs = sum_kwargs

    def __call__(self, *args, **kwargs):
        """Calls *array* with the arguments, and then calls ``.sum()`` on
        the value with the arguments defined at initialisation time."""

        array = self.array(*args, **kwargs)
        return array.sum(*self.sum_args, **self.sum_kwargs)

class Indexing(MathFunction):
    """
    Returns an item from the value of another Function.

    Examples:

    1)  Indexing of a tuple with an integer.
    2)  Indexing of a ndarray with any index accepted by the ndarray.
    3)  Indexing of a dictionary.

    The index is static, i.e., it isn't a Function.
    """

    def __init__(self, index, items=None):
        """*items* returns the items the Indexing chooses from.  The value
        of *items* must support indexing.
        
        *index* might be any index accepted by the value of *items*."""

        self.items = asfunction(items)
        self.index = asfunction(index)

    def __call__(self, *args, **kwargs):
        """Indexes the value of *items* with *index*."""

        items = self.items(*args, **kwargs)
        index = self.index(*args, **kwargs)
        return items[index]

class AttributeAccess(MathFunction):
    """
    Returns an attribute from the value of another Function.
    """

    def __init__(self, attribute, host=None):
        """*host* is the Function with values hosting the attribute named 
        *attribute*."""

        self.host = asfunction(host)
        self.attribute = asfunction(attribute)

    def __call__(self, *args, **kwargs):
        """Returns the attribute *attribute* from the value of *host*."""

        host = self.host(*args, **kwargs)
        attribute = self.attribute(*args, **kwargs)
        return getattr(host, attribute)

class Clip(MathFunction):
    """
    Clips the leaf Function's value.
    """

    def __init__(self, low, high, leaf=None):
        """*low* is the Function giving the lower boundary, *high* gives the
        upper boundary, and *leaf* is the Function to be clipped."""

        self.low = asfunction(low)
        self.high = asfunction(high)
        self.leaf = asfunction(leaf)

    def __call__(self, *args, **kwargs):
        """Calls ``.low()``, ``.high()``, ``.leaf()``, and clips using the
        values."""

        low = self.low(*args, **kwargs)
        high = self.high(*args, **kwargs)
        leaf = self.leaf(*args, **kwargs)
        return numpy.clip(leaf, low, high)

class asarray(MathFunction):
    """Converts ndarrays, with arbitrary arguments."""

    def __init__(self, array_like, *args, **kwargs):
        """Converts the array_like-values Function *array_like* via
        ``numpy.ndarray()`` with all *args* and *kwargs* given."""

        self.array_like = asfunction(array_like)

        self.args = args
        self.kwargs = kwargs

    def reduce(self, array_like, args, kwargs):
        """If *array_like* is scalar, returns the call of the item with *args* 
        and *kwargs*.  Else, iterates."""

        if isinstance(array_like, list) or isinstance(array_like, tuple):
            return numpy.asarray([self.reduce(item, args, kwargs) \
                for item in array_like])
        else:
            return asfunction(array_like)(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Applies the args and kwargs from initialisation time onto
        ``.array_like()`` via ``numpy.asarray()``."""

        array_like = self.reduce(self.array_like(*args, **kwargs), 
            args, kwargs)

        return numpy.asarray(array_like, *self.args, **self.kwargs)
