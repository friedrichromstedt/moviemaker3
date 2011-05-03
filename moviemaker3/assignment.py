from fframework import OpFunction, asfunction

class Assignment(OpFunction):
    """Extends parameter objects by evaluating some Function with the parameter
    object as argument, and stores it using a ``p`` object.  Use like this::
        
        extended = assignment | target
        
    where ``assignment`` might be::
    
        Assignment(p('a'), 1)"""
    
    def __init__(self, p, value):
        """*value* is called and stored in the parameter object via *p*."""

        self.p = p
        self.value = asfunction(value)

    def __call__(self, ps):
        """Extends *ps*."""

        value = self.value(ps)
        ps_ext = self.p.store(ps, value=value)
        return ps_ext
