from fframework import OpFunction, asfunction

class Extension(OpFunction):
    """Extends paramter objects by evaluating some Function with the parameter
    object as argument, and stores it using another ``p`` object.  Use like
    this::
        
        extended = target | extension"""
    
    def __init__(self, value, p):
        """*value* is called and stored in the parameter object via *p*."""

        self.value = asfunction(value)
        self.p = p

    def __call__(self, ps):
        """Extends *ps*, and calls *target* with the extended Ps."""

        value = self.value(ps)
        ps_ext = self.p.store(ps, value=value)
        return ps_ext
