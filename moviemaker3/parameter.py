from fframework import MathFunction

__all__ = ['p']

class Ps(dict):
    """Holds a number of parameter values.
    
    The values are hierarchical, this means that the name specifies a
    slash-separated path.  Setting a name containing a slash will set the
    basename in some leaf ``Ps``.  E.g.::
        
        ps = Ps()
        ps['root/leaf'] = 'foobar'
    
    will set the ``'leaf'`` value in the ``'root'`` value of ``ps``, where the
    ``'root'`` value of ``ps`` is in turn a ``Ps`` instance.  This means, 
    you can do::
        
        ps['root/leaf2'] = 'hello world'
        subps = ps['root']
    
    and will have a ``Ps`` containing two values ``'leaf'`` and ``'leaf2'`` in
    the variable ``subps``."""
    
    def __init__(self, parameters=None, name=None, value=None):
        """*parameters* is the initial dictionary specification, defaulting to 
        the empty dictionary.  It will be passed to the dictionary 
        constructor.
        
        Additionally, if *name* is not None, the name *name* will be set to
        *value*."""

        if parameters is None:
            parameters = {}
        
        dict.__init__(self, parameters)

        if name is not None:
            self.extend(name, value)
    
    def split(self, name):
        """Splits the string *name* at the ``/`` positions and returns the 
        tuple ``(root, leaf)``, where *root* is the largest portion of the 
        string *name* starting at the beginning and not containing a slash,
        and *leaf* is either ``None`` if there is no slash or the rest after
        the first slash."""

        components = name.split('/')
        root = components[0]
        if len(components) == 1:
            return (root, None)
        else:
            return (root, '/'.join(components[1:]))

    def extend(self, name, value):
        """Returns *self* extended by ``name: value``."""

        (root, leaf) = self.split(name)
        if leaf is None:
            self.parameters[root] = value
        else:
            self.parameters.setdefault(root, Ps())
            self.parameters[root].extend(leaf, value)
        return self

    def extended(self, name, value):
        """Returns a copy of *self* extended by (*name*, *value*)."""

        copied = self.copy()
        return copied.extend(name, value)

    def __setitem__(self, key, value):
        """Alias for ``.extend()`` for syntax like e.g. 
        ``ps['hi'] = 'world'``."""

        return self.extend(name, value)

    def copy(self):
        """Returns a ``Ps`` with copied ``.parameters``.  All ``Ps`` objects
        will be copied, but not the data."""

        new_data = []
        for (key, value) in self.items():
            if isinstance(value, Ps):
                new_data.append((key, value.copy()))
            else:
                new_data.append((key, value))
        return Ps(parameters=dict(new_data))

    def retrieve(self, name):
        """Retrieves the value of *name*."""

        components = name.split('/')
        root = components[0]
        leaf = '/'.join(components[1:])
        if len(components) == 1:
            return self.parameters[root]
        else:
            return self.parameters[root][leaf]

    def __getitem__(self, key):
        """Alias for ``.retrieve()`` for syntax like e.g. ``ps['foobar']``."""

        return self.retrieve(key)

class p(MathFunction):
    """Accesses a parameter by name."""
    
    def __init__(self, name):
        """Access will be done for parameter named *name*."""

        self.name = name

    def __call__(self, ps):
        """Returns the parameter value in *ps*."""

        return ps.retrieve(self.name)

    def store(self, ps, value):
        """Extends *ps* by *value*."""

        return ps.extended(self.name, value)
