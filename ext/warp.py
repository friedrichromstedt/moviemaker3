from moviemaker2.function import asfunction
from moviemaker2.layer import Layer

class Warp(Layer):
    """Warps warp the time.  They have leaf Function attributes for retrieving 
    and for extending the time object, for getting the new time value, and for 
    getting the time argument.

    ``Warp`` might be used like this::
        
        warp = Warp(value=(25 * Timeline('realtime', time=KwArg('time')),
            extender=Timeline('frametime'), arg=KwArg('time'))
    """

    def __init__(self, value, extender, arg):
        """*value* will become the new time value.  *arg* is used to specify 
        which argument upon call holds the time object.  *extender* is a
        :class:`~moviemaker2.time.Timeline` object used to modify the time 
        object."""

        self.value = asfunction(value)
        self.extender = extender
        self.arg = arg

    def accumulate(self, layer):
        """Binds this Warp to a Layer."""

        return BoundWarp(layer=layer, value=self.value, extender=   
            self.extender, arg=self.arg)

class BoundWarp(Warp):
    """A Warp bound to a Layer.  Binding happens through accumulation of
    the Layer by the Warp."""

    def __init__(self, layer, value, extender, arg):
        """Same meaning as :meth:`Warp.__init__`."""

        Warp.__init__(self, value=value, extender=extender, arg=arg)
        self.layer = layer

    def __call__(self, *args, **kwargs):
        """Retrieves the time object, gets the new timevalue, then stores
        it in the timeobject, and hands over the modified timeobject together
        with all other arguments to the layer."""

        timeobject = self.arg.retrieve(args, kwargs)
        timevalue = self.value(*args, **kwargs)
        extended = self.extender.extend(timevalue=timevalue, 
            timeobject=timeobject)
        (args_ext, kwargs_ext) = self.arg.store(args, kwargs, extended)
        return self.layer(*args_ext, **kwargs_ext)
