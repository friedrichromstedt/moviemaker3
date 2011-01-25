"""
Defines time related stuff.

*   A *timescale* is a name for some time value.
*   A *time value* is some number.
*   A *timeline* is an object which can select a specific *timescale* from a
    :class:`Time` instance or extend an existing :class:`Time` instance.
*   A *time object* or simply a *time* is a :class:`Time` instance holding 
    multiple ``timescale: timevalue`` items.
"""

import copy
from moviemaker2.function import asfunction
from moviemaker2.math import MathFunction

# We don't need explicit access to Time, use Timeline.extend() without given
# *timeobject* instead:
__all__ = ['Timeline']

class Time:
    """Holds values of as many timescales as you wish."""

    def __init__(self, times=None):
        """Initialises the Time object to hold no times.  The arguments
        are for internal use."""
        
        if times is None:
            times = {}

        # A dictionary of ``timescale: timevalue`` items:
        self._times = times

    def extended(self, timescale, timevalue):
        """Returns a Time instance holding the ``timescale: timevalue``
        pairs of this instance and additionally a pair made from the 
        arguments."""

        # Copy the old ``times`` dictionary, so that adds do not alter
        # our own ._times object
        newtimes = copy.copy(self._times)

        # Add the new item
        newtimes[timescale] = timevalue

        # Instatiate a ``Time`` object
        return Time(times=newtimes)

    def retrieve(self, timescale):
        """Returns the value of the timescale requested, or raises 
        ``KeyError``."""
        
        return self._times[timescale]

class Timeline(MathFunction):
    """Can retrieve time scale values from :class:`Time` instances and can 
    extend existing :class:`Time` instances by an additional timescale 
    value."""

    def __init__(self, timescale, time=None):
        """*timescale* is the name of this ``Timeline``.
        
        *time* is the Function returning the time on call."""

        self._timescale = timescale
        self.time = asfunction(time)

    def extend(self, timevalue, timeobject=None):
        """Extends the time *timeobject* by the time value *timevalue* on the
        timeline given at initialisation time.  If *timeobject* is not given,
        create a new time object."""

        if timeobject is None:
            timeobject = Time()

        return timeobject.extended(timescale=self._timescale, 
            timevalue=timevalue)

    def retrieve(self, timeobject):
        """Retrieves the timescale value of this ``Timeline`` from the time
        *timeobject*."""

        return timeobject.retrieve(timescale=self._timescale)

    def __call__(self, *args, **kwargs):
        """Returns ``.retrieve()`` with ``.time()`` as argument."""

        time = self.time(*args, **kwargs)
        return self.retrieve(time)

class Warp(MathFunction):
    """Warps warp the time.  They have two leaf Function attributes, one for 
    retrieving the time, and one for extending the time.

    ``Warp`` might be used like this::
        
        warp = Warp(retrieve=(25 * Timeline('realtime')), 
            extend=Timeline('frametime'))
    """

    def __init__(self, retrieve=None, extend=None, time=None):
        """*time* is used to extract the time from the arguments.  *retrieve* 
        and *extend* are :class:`~moviemaker2.time.Timeline` objects used to
        modify the time."""

        self.retrieve = retrieve
        self.extend = extend
        self.time = asfunction(time)

    def __call__(self, *args, **kwargs):
        """Applies ``.extend.extend()`` onto the ``.time()`` with the 
        extension by ``.retrieve()`` applied onto the ``.time()``."""

        time = self.time(*args, **kwargs)
        retrieved = self.retrieve.retrieve(time)
        extended = self.extend.extend(timevalue=retrieved, timeobject=time)
        return extended
