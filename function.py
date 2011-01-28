"""
*   Defining math overloads requires that the mathematical Functions are at
    hand.  But those are derivatives of ``Function``.  So we would have to
    define the Functions for mathematical overloads in the same scope as the
    Function base class.

*   Defining the ``Function`` class first, it is possible to define 
    mathematical Functions in ``moviemaker2.math``, when defining the 
    ``MathFunction`` class, which has mathematical overloads using those
    mathematical Functions.

*   Tests whether an object is a function or not require only testing if the
    object is an instance of ``Function``.
"""

import numpy

# Only export for ``from xx import *`` the really useful objects:
__all__ = ['Function', 'asfunction', 'asfunctionv']

class Function:
    """The base class of all Functions.  It is a bare class without any 
    attributes.  Used in ``isinstance(object, Function)``."""

    pass

class Constant(Function):
    """
    A Function yielding always the same value.
    """

    def __init__(self, value):
        """
        *value* is the value of the Constant.
        """

        self.value = value

    def __call__(self, *args, **kwargs):
        """Returns the constant value."""
        return self.value

class Identity(Function):
    """
    Returns always its argument(s).  If called with precisely one 
    argument, returns the argument as a scalar, else the argument vector
    is returned.
    """

    def __call__(self, *args):
        if len(args) == 1:
            return args[0]
        else:
            return args

def asfunction(function_like):
    """
    *   If *function_like* is a :class:`Function`, it is returned unchanged.
    *   If *function_like* is None, an :class:`Identity` is returned.
    *   Else, the *function_like* is interpreted as a :class:`Constant`.
    
    For ``asfunctionv()``, ``asfunction()`` is applied to any element of an 
    array_like argument.
    """

    if isinstance(function_like, Function):
        return function_like
    elif function_like is None:
        return Identity()
    else:
        return Constant(function_like)

asfunctionv = numpy.vectorize(asfunction)
