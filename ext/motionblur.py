from moviemaker2.layer import Layer, Stack

class Motionblur(Layer):
    """Blurs the motion by adding several instantiations of the accumulated
    layer at modified times."""

    def __init__(self, timemodvalues, timemod, timeline, timearg, 
            timemodarg):
        """*timemodvalues* is an iterable.  There will be as many layers
        superimposed as there are items in *timemodargs*.  *timemod* returns
        with kwarg "timemodarg" a new time value.  *timeline* is used to 
        replace the timevalue.  *timearg* gives the argument to use as time 
        object.  *timemodarg* gives the argument to use when handing the
        timemodvalue over."""

        self.timemodvalues = timemodvalues
        self.timemod = timemod
        self.timeline = timeline
        self.timearg = timearg
        self.timemodarg = timemodarg

    def accumulate(self, layer):
        """Returns a Stack of BoundMotionBlurs which will modify the time
        on call time before passing it on to *layer*."""
        
        result = None

        for timemodvalue in self.timemodvalues:
            if result is None:
                result = BoundMotionblurLayer(target=layer, accumulate=None,
                    timemodvalue=timemodvalue, timemod=self.timemod, 
                    timeline=self.timeline, timearg=self.timearg,
                    timemodarg=self.timemodarg)
            else:   
                result = BoundMotionblurLayer(target=layer, accumulate=result,
                    timemodvalue=timemodvalue, timemod=self.timemod,
                    timeline=self.timeline, timearg=self.timearg,
                    timemodarg=self.timemodarg)

        return result

class BoundMotionblurLayer(Layer):
    """Alters time on call time."""
    
    def __init__(self, target, accumulate, 
            timemodvalue, timemod, timeline, timearg, timemodarg):
        """Meaning is the same as for Motionblur."""

        self.target = target
        self.timemodvalue = timemodvalue
        self.timemod = timemod
        self.timeline = timeline
        self.timearg = timearg
        self.timemodarg = timemodarg
        self.accumulate = accumulate

    def __call__(self, *args, **kwargs):
        """Alters the time."""

        (extended_args, extended_kwargs) = self.timemodarg.store(
            args, kwargs, self.timemodvalue)
        timevalue = self.timemod(*extended_args, **extended_kwargs)

        timeobject = self.timearg.retrieve(extended_args, extended_kwargs)
        modified_timeobject = self.timeline.extend(timeobject=timeobject,
            timevalue=timevalue)
        (modified_args, modified_kwargs) = self.timearg.store(
            extended_args, extended_kwargs, modified_timeobject)

        target = self.target(*modified_args, **modified_kwargs)
        if self.accumulate is None:
            return target
        else:
            accumulate = self.accumulate(*args, **kwargs)
            return target.accumulate(accumulate)
