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
__all__ = ['Function', 'asfunction', 'asfunctionv', 'fasarray', 'fdict']

class Function:
    """The base class of all Functions.  It is a bare class without any 
    attributes.  Used in ``isinstance(object, Function)``."""

    def __init__(self):
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

def call_recursive(obj, args, kwargs):
    """Calls function nested somewhere inside a primitive *obj*.

    *   lists and tuples: Calls on all items.
    *   dicts: Calls on keys and values.

    Constant atomic items are returned as-is.  Atomic items are items that are
    neither lists, tuples, nor dicts."""

    if isinstance(obj, list):
        return [call_recursive(item, args, kwargs) for item in obj]
    elif isinstance(obj, tuple):
        return tuple([call_recursive(item, args, kwargs) for item in obj])
    elif isinstance(obj, dict):
        return dict([(call_recursive(key, args, kwargs), 
            call_recursive(value, args, kwargs)) for (key, value) in \
                obj.items()])
    else:
        return asfunction(obj)(*args, **kwargs)

class fasarray(Function):
    """Converts to ndarrays, with arbitrary arguments."""

    def __init__(self, array_like, *args, **kwargs):
        """Converts the array_like-valued Function *array_like* via
        ``numpy.ndarray()`` with all *args* and *kwargs* given.  
        *array_like* will be passed through :func:`call_recusive` on call
        time."""

        self.array_like = array_like 
            # converted by asfunction in call_recursive

        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """Applies the args and kwargs from initialisation time onto
        ``.array_like()`` via ``numpy.asarray()``."""

        array_like = call_recursive(self.array_like, args, kwargs)
        return numpy.asarray(array_like, *self.args, **self.kwargs)

class fdict(Function):
    """Converts to dicts."""

    def __init__(self, dict_like):
        """Converts the dict_like-valued Function *dict_like* via dict() after
        passing through :func:`call_recursive`."""

        self.dict_like = dict_like

    def __call__(self, *args, **kwargs):
        """Applies the args and kwargs from initialisation time onto
        ``.array_like()`` via ``numpy.asarray()``."""

        return dict(call_recursive(self.dict_like, args, kwargs))
