"""Layers can accumulate another Layer.  When accumulating another Layer,
the channels are combined using the logic of the accumulating Layer.

The accumulation is done by the topmost (last) layer.  Thus the layer type of 
the result layer from the accumulation does not matter.  Each layer defines
how he accumulates the accumulation result of all previous layers."""

import copy
import numpy
from moviemaker2.function import Function, asfunction
from moviemaker2.math.primitive import asmathfunction

# Only export end-user objects:
__all__ = ['Channel', 'Branch', 'AdditionLayer', 'AlphaBlendLayer']

class Layer(Function):
    
    def __init__(self):
        pass
    
    def is_ignored(self, *args, **kwargs):
        return False

    def accumulate(self, other):
        return other

    def __or__(self, other):
        """Returns an :class:`Stack` of *self* below *other*.  *other* will
        have the accumulating role."""

        return Stack([self, other])

    def __xor__(self, other):
        """If *other* is a :class:`Stack`, add *self* at the bottom of 
        *other*.  Else, return a new Stack consisting of *self* and 
        *other*."""

        if isinstance(other, Stack):
            return other.copy().add_bottom(self)
        else:
            return Stack([self, other])

class Channel(Function):
    """A channel is one channel of a layer.  It has a name and data, and 
    supports basic arithemtic by forwarding it to the data."""

    def __init__(self, name, data):
        """*data* is an array_like, *name* is some string identifying the 
        channel.  *data* will be fed through ``numpy.asarray``."""

        self.data = asmathfunction(data)
        self.name = name

    def __add__(self, other):
        """If *other* is a Channel, adds the ``.data`` up, and keeps self's 
        name.  Else, add *other* to ``self.data``, and keep self's name."""

        if isinstance(other, Channel):
            return Channel(data=(self.data + other.data), name=self.name)
        else:
            return Channel(data=(self.data + other), name=self.name)

    __radd__ = __add__

    def __sub__(self, other):
        """If *other* is a Channel, subtracts the ``.data`` attributes, else
        subtracts *other*, and keeps self's name."""

        if isinstance(other, Channel):
            return Channel(data=(self.data - other.data), name=self.name)
        else:
            return Badn(data=(self.data - other), name=self.name)

    def __rsub__(self, other):
        """If *other* is a Channel, ``other.__sub__`` will be called instead 
        of ``self.__rsub__``.  So we care only about cases where *other* isn't
        a Channel, and subtract self's data attribute from other directly, 
        keeping self's name."""

        return Channel(data=(other - self.data), name=self.name)

    def __mul__(self, other):
        """If *other* is a Channel, multiplies the ``.data`` attributes, else
        multiplies with *other* directly.  Keeps self's name."""

        if isinstance(other, Channel):
            return Channel(data=(self.data * other.data), name=self.name)
        else:
            return Channel(data=(self.data * other), name=self.name)

    __rmul__ = __mul__
    
    def __pow__(self, other):
        """If *other* is a Channel, raises self's data to the power of the 
        other's data, else raises self's data to the power of *other*.
        Keeps self's name."""

        if isinstance(other, Channel):
            return Channel(data=(self.data ** other.data), name=self.name)
        else:
            return Channel(data=(self.data ** other), name=self.name)

    def __call__(self, *args, **kwargs):
        """Returns a Channel with the same name, but data attribute calculated 
        by ``.data()``."""

        return Channel(name=self.name, data=self.data(*args, **kwargs))

class AlphaLayer(Layer):
    """This is the base class for all Layers with alpha channel.  A layer 
    holds several result channels and an alpha channel.  The result channels 
    can be accessed via their name with attribute access.  They are named like 
    the original channels without alpha.  
    AlphaLayers can set themselves to "ignored" on call time.  The 
    :class:`Stack` instance carrying out the accumulation on call time will 
    ignore Layers which have to be ignored."""

    def __init__(self, alpha, without_alpha=None, results=None, ignore=None):
        r"""*alpha* is the alpha channel.  Additionally, one of 
        *without_alpha* and *results* must be given, else ``ValueError`` is 
        raised.  Only result channels are stored.  *without_alpha* has the 
        higher precedence of *without_alpha* and *results*.

        If *without_alpha* is given, the result channels are calculated by:

        .. math::

            R = W \cdot \alpha

        If *results* is given, they are stored directly.
        
        *ignore* is a boolean Function.  *ignore* is used when accumulating
        Layers.  If *ignore* is true, the Layer will not take part in 
        accumulation."""

        self.alpha = alpha
        self.results = []
        self.ignore = asfunction(ignore)

        if without_alpha is not None:
            for channel in without_alpha:
                self.results.append(channel * alpha)
        elif results is not None:
            self.results = results
        else:
            raise ValueError('Either *without_alpha* or *results* must be '
                'specified')

    def is_ignored(self, *args, **kwargs):
        """Returns true, if this Layer is to be ignored."""

        return self.ignore(*args, **kwargs)

    def get_channel(self, name):
        """Returns the result channel *name* or raises ``ValueError``."""

        for channel in self.results:
            if channel.name == name:
                return channel

        raise ValueError("No such channel: '%s'" % name)

    def get_channel_names(self):
        """Returns a set of all channel names present."""

        return set([channel.name for channel in self.results])

    def has_channel(self, name):
        """Returns ``True`` if there is a Channel named *name*, else 
        ``False``."""

        for channel in self.results:
            if channel.name == name:
                return True
        return False

#    def __getattr__(self, name):
#        """Returns the channel with the given *name* or raises 
#        ``ValueError``."""
#
#        return self.get_channel(name)

    def accumulate(self, other):
        """Derived must overload.  Accumulate the other Layer under the
        terms and conditions of *self*."""

        raise NotImplementedError('Derived must overload')

    def __call__(self, *args, **kwargs):
        """Returns a Layer with all Channels called once."""

        alpha = self.alpha(*args, **kwargs)
        results = []
        for result in self.results:
            results.append(result(*args, **kwargs))
        return AlphaLayer(alpha=alpha, results=results)

class Stack(Layer):
    """On being called, the ``Stack`` accumulates layers each by another.
    
    Furthermore, the Stack acts as a Layer.  This means, it can be called, 
    yielding a called Layer with called Channels, it can be asked by 
    ``.ignore()`` if it is to be ignored, and it can be stacked."""

    def __init__(self, elements):
        """*elements* are the elements of the Stack."""

        self.elements = elements

    def is_ignored(self, *args, **kwargs):
        """This Stack is to be ignored if all constituents are to be 
        ignored.  If the stack is empty, is it to be ignored."""

        for element in self.elements:
            if not element.is_ignored(*args, **kwargs):
                return False
        return True

    def copy(self):
        return Stack(copy.copy(self.elements))

    # __or__ is okay how it comes from Layer.
    
    def __xor__(self, other):
        """If *other* is a Stack, merge the stacks by returning a new
        stacks with the element lists concatenated.  Else, add *other* to
        the stack."""

        if isinstance(other, Stack):
            return Stack(self.elements + other.elements)
        else:
            return Stack(self.elements + [other])

    def add_top(self, other):
        """Adds *other* as another element at the top of the stack."""

        self.elements.append(other)

    def add_bottom(self, other):
        """Adds *other* as another element at the bottom of the stack."""

        self.elements.insert(0, other)

    def merge_top(self, other):
        """Merges with the elements of another Stack *other*, adding the
        elements on top."""

        self.elements.extend(other.elements)

    def merge_bottom(self, other):
        """Merges with the elements of another Stack *other*, adding the
        elements at the bottom."""

        self.elements = other.elements + self.elements

    def remove(self, element):
        """Remove the first occurence of *element* in this stack."""

        self.elements.remove(element)

    def __call__(self, *args, **kwargs):
        """Generates the combined Layer.
        
        Starting with the first non-ignored element, accumulating the
        elements one after another.  The first element in ``.elements`` is
        accumulated by the next, and so on.

        Returns the result of the call of the merge layer.
        
        If there are no elements to combine, raises RuntimeError."""

        # Generate a list of non-ignored Layers.
        elements = []
        for element in self.elements:
            if not element.is_ignored(*args, **kwargs):
                #elements.append(element(*args, **kwargs))
                elements.append(element)

        layer = elements[0]
        for element in elements[1:]:
            layer = element.accumulate(layer)
        return layer(*args, **kwargs)

class Branch(Layer):
    """On being called, the ``Branch`` evaluates a selector, and chooses
    one Layer based on the value."""

    def __init__(self, layers, choice):
        """*choice* gives an index into *layers*.  Especially, *layers* might
        be a dictionary, mapping return values onto Layers."""

        self.choice = asfunction(choice)
        self.layers = layers

    def __call__(self, *args, **kwargs):
        """Evaluates ``.choice(...)``, and calls the appropriate layer."""

        choice = self.choice(*args, **kwargs)
        return self.layers[choice](*args, **kwargs)

class AdditionLayer(AlphaLayer):
    """This Layer type accumulates another Layer by adding up all matching
    channels."""

    def accumulate(self, other):
        """Adds Channels with the same name up.  Groups present in *other* but 
        not present in *self* are set to the Channel of *other*, and Groups 
        present in *self* but not in *other* are set to the Channel of *self*.  
        Returns another ``AdditionLayer``."""

        alpha = self.alpha + other.alpha

        results = []
        channel_names_self = self.get_channel_names()
        channel_names_other = other.get_channel_names()
        for channel_name in channel_names_self | channel_names_other:
            if channel_name in channel_names_self:
                if channel_name in channel_names_other:
                    results.append(self.get_channel(channel_name) + 
                        other.get_channel(channel_name))
                else:
                    results.append(self.get_channel(channel_name))
            else:
                # channel is in other
                results.append(other.get_channel(channel_name))

        return AdditionLayer(alpha=alpha, results=results)

    def __call__(self, *args, **kwargs):
        """Returns a Layer with all Channels called once."""

        alpha = self.alpha(*args, **kwargs)
        results = []
        for result in self.results:
            results.append(result(*args, **kwargs))
        return AdditionLayer(alpha=alpha, results=results)

class AlphaBlendLayer(AlphaLayer):
    """This Layer type performs alpha blending."""

    def accumulate(self, other):
        r"""Performs for all channels present alpha blending using the alpha 
        channel:

        .. math::

            X = X_i \cdot (1 - \alpha_{i + 1}) + X_{i + 1}

        where *X* is the resulting channel, :math:`X_i` is the accumulated 
        channel, and :math:`X_{i + 1}` is the channel from this Layer.  If the 
        channel is not present in one of the Layers, the remaining Channel is
        used.
        
        Returns another ``AlphaBlendLayer``."""

        alpha_calc = self.alpha

        alpha_result = other.alpha * (1 - alpha_calc) + self.alpha

        results = []
        channel_names_self = self.get_channel_names()
        channel_names_other = other.get_channel_names()
        for channel_name in channel_names_self | channel_names_other:
            if channel_name in channel_names_self:
                if channel_name in channel_names_other:
                    results.append(
                        other.get_channel(channel_name) * (1 - alpha_calc) + 
                        self.get_channel(channel_name))
                else:
                    results.append(self.get_channel(channel_name))
            else:
                # channel is in other
                results.append(
                    other.get_channel(channel_name) * (1 - alpha_calc))

        return AlphaBlendLayer(alpha=alpha_result, results=results)

    def __call__(self, *args, **kwargs):
        """Returns a Layer with all Channels called once."""

        alpha = self.alpha(*args, **kwargs)
        results = []
        for result in self.results:
            results.append(result(*args, **kwargs))
        return AlphaBlendLayer(alpha=alpha, results=results)
