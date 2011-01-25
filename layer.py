"""Layers can accumulate another Layer.  When accumulating another Layer,
the bands are combined using the logic of the accumulating Layer.

The accumulation is done by the topmost (last) layer.  Thus the layer type of 
the result layer from the accumulation does not matter.  Each layer defines
how he accumulates the accumulation result of all previous layers."""

import numpy
from moviemaker2.function import Function, asfunction

# Only export end-user objects:
__all__ = ['Band', 'AdditionLayer', 'AlphaBlendLayer']

class Band(Function):
    """A band is one channel of a layer.  It has a name and data, and supports
    basic arithemtic by forwarding it to the data."""

    def __init__(self, name, data):
        """*data* is an array_like, *name* is some string identifying the 
        band.  *data* will be fed through ``numpy.asarray``."""

        self.data = asfunction(data)
        self.name = name

    def __add__(self, other):
        """If *other* is a Band, adds the ``.data`` up, and keeps self's name.
        Else, add *other* to ``self.data``, and keep self's name."""

        if isinstance(other, Band):
            return Band(data=(self.data + other.data), name=self.name)
        else:
            return Band(data=(self.data + other), name=self.name)

    __radd__ = __add__

    def __sub__(self, other):
        """If *other* is a Band, subtracts the ``.data`` attributes, else
        subtracts *other*, and keeps self's name."""

        if isinstance(other, Band):
            return Band(data=(self.data - other.data), name=self.name)
        else:
            return Badn(data=(self.data - other), name=self.name)

    def __rsub__(self, other):
        """If *other* is a Band, ``other.__sub__`` will be called instead of
        ``self.__rsub__``.  So we care only about cases where *other* isn't
        a Band, and subtract self's data attribute from other directly, 
        keeping self's name."""

        return Band(data=(other - self.data), name=self.name)

    def __mul__(self, other):
        """If *other* is a Band, multiplies the ``.data`` attributes, else
        multiplies with *other* directly.  Keeps self's name."""

        if isinstance(other, Band):
            return Band(data=(self.data * other.data), name=self.name)
        else:
            return Band(data=(self.data * other), name=self.name)

    __rmul__ = __mul__
    
    def __pow__(self, other):
        """If *other* is a Band, raises self's data to the power of the 
        other's data, else raises self's data to the power of *other*.
        Keeps self's name."""

        if isinstance(other, Band):
            return Band(data=(self.data ** other.data), name=self.name)
        else:
            return Band(data=(self.data ** other), name=self.name)

    def __call__(self, *args, **kwargs):
        """Returns a Band with the same name, but data attribute 
        calculated by ``.data()``."""

        return Band(name=self.name, data=self.data(*args, **kwargs))

class Layer(Function):
    """This is the base class for all Layers.  A layer holds several colour 
    result bands and an alpha band.  The colour result bands can be accessed 
    via their name with attribute access.  They are named like the original
    colour bands.
    
    Layers can be combined to stacks by OR'ing them.  The addition is left
    associative in Python, so::
    
        A | B | C == (A | B) | C
    
    Thus the bottom-most Layer is the first operand.
    
    Layers can set themselves to "ignored" on call time.  The 
    :class:`Accumulation` instance carrying out the accumulation on call time 
    will ignore Layers which have to be ignored."""

    def __init__(self, alpha, colours=None, results=None, ignore=None):
        r"""*alpha* is the alpha band.  Additionally, one of *colours* and 
        *results* must be given, else ``ValueError`` is raised.  Only result 
        bands are stored.  *colours* has higher precedence.

        If *colours* is given, the result bands are calculated by:

        .. math::

            R = C \cdot \alpha

        If *results* is given, they are stored directly.
        
        *ignore* is a boolean Function.  *ignore* is used when accumulating
        Layers (accumulation is done by OR'ing the layers).  If *ignore* is
        true, the Layer will not take part in accumulation."""

        self.alpha = alpha
        self.results = []
        self.ignore = asfunction(ignore)

        if colours is not None:
            for band in colours:
                self.results.append(band * alpha)
        elif results is not None:
            self.results = results
        else:
            raise ValueError('Either *colours* or *results* must be '
                'specified')

    def is_ignored(self, *args, **kwargs):
        """Returns true, if this Layer is to be ignored."""

        return self.ignor(*args, **kwargs)

    def get_band(self, name):
        """Returns the result band *name* or raises ``ValueError``."""

        for band in self.results:
            if band.name == name:
                return band

        raise ValueError("No such band: '%s'" % name)

    def has_band(self, name):
        """Returns ``True`` if there is a Band named *name*, else 
        ``False``."""

        for band in self.results:
            if band.name == name:
                return True
        return False

    def __getattr__(self, name):
        """Returns the band with the given *name* or raises ``ValueError``."""

        return self.get_band(name)

    def accumulate(self, other):
        """Derived must overload.  Accumulate the other Layer under the
        terms and conditions of *self*."""

        raise NotImplementedError('Derived must overload')

    def __or__(self, other):
        """Returns an :class:`Accumulation` of *self* by *other*."""

        return Accumulation(accumulated=self, accumulator=other)

    def __call__(self, *args, **kwargs):
        """Returns a Layer with all Bands called once."""

        alpha = self.alpha(*args, **kwargs)
        results = []
        for result in self.results:
            results.append(result(*args, **kwargs))
        return Layer(alpha=alpha, results=results)

class Accumulation(Layer):
    """On being called, the ``Accumulation`` accumulates one layer by 
    another.
    
    Furthermore, the Accumulation acts as a Layer.  This means, it can be
    called, yielding a called Layer with called Bands, and it can be asked
    by ``.ignore()`` if it is to be ignored."""

    def __init__(self, accumulated, accumulator):
        """*accumulated* is the Layer accumulated by *accumulator*."""

        self.accumulated = accumulated
        self.accumulator = accumulator

    def is_ignored(self, *args, **kwargs):
        """This Layer is to be ignored if all constituents are to be 
        ignored."""

        return self.accumulated.ignore() and self.accumulator.ignore()

    def __call__(self, *args, **kwargs):
        """Generates the combined Layer.
        
        *   If both components are not to be ignored, accumulates 
            ``.accumulated()`` by ``.accumulator()``.
        *   If one component is to be ignored, returns the other called.
        *   If both components are to be ignored, this means that there are
            no Layers at all.  An exception is raised."""

        if self.accumulated.is_ignored(*args, **kwargs):
            if self.accumulator.is_ignored(*args, **kwargs):
                raise RuntimeError('No Layer present')
            else:
                return self.accumulator(*args, **kwargs)
        else:
            if self.accumulator.is_ignored(*args, **kwargs):
                return self.accumulated(*args, **kwargs)
            else:
                accumulated = self.accumulated(*args, **kwargs)
                accumulator = self.accumulator(*args, **kwargs)
                return accumulator.accumulate(accumulated)

class AdditionLayer(Layer):
    """This Layer type accumulates another Layer by adding up all matching
    bands."""

    def accumulate(self, other):
        """Adds all bands of *other* to the bands present.  Bands present in 
        *other* but not present in *self* are set to zero for *self*.  Returns 
        another ``AdditionLayer``."""

        alpha = self.alpha + other.alpha

        results = []
        for band in other.results:
            if self.has_band(band.name):
                results.append(band + other.get_band(band.name))
            else:
                results.append(band)

        return AdditionLayer(alpha=alpha, results=results)

class AlphaBlendLayer(Layer):
    """This Layer type performs alpha blending."""

    def accumulate(self, other):
        r"""Performs for all bands present in *other* alpha blending using the 
        alpha band:

        .. math::

            X = X_i \cdot (1 - \alpha_{i + 1}) + X_{i + 1}

        where *X* is the resulting band, :math:`X_i` is the accumulated band,
        and :math:`X_{i + 1}` is the band from this Layer.  If the band is not
        present in *self*, it is set zero.
        
        Bands present in *self* but not in *other* are ignored.  Returns 
        another ``AlphaBlendLayer``."""

        alpha_calc = self.alpha

        alpha_result = other.alpha * (1 - alpha_calc) + self.alpha

        results = []
        for band in other.results:
            if self.has_band(band.name):
                results.append(band * (1 - alpha_calc) + 
                    self.get_band(band.name))
            else:
                results.append(band * (1 - alpha_calc))

        return AlphaBlendLayer(alpha=alpha_result, results=results)
