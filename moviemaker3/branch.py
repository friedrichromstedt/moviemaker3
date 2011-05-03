from fframework import OpFunction, asfunction

class Branch(OpFunction):
    """On being called, the ``Branch`` evaluates a selector, and chooses
    one Function based on the value."""

    def __init__(self, key, choices=None):
        """*key* gives an index into *choices*.  *choices* is supposed to be a 
        dictionary, mapping return values onto Functions, and defaults to the 
        empty dict."""

        if choices is None:
            choices = {}

        self.key = asfunction(key)
        self.choices = choices

    def add_branch(self, key, choice):
        """Registers Function *choice* under choice key *key*."""

        self.choices[key] = choice

    def __call__(self, ps):
        """Evaluates ``.key(ps)`` and calls the appropriate function.  The
        item from the dict will be passed through ``asfunction``."""

        key = self.key(ps)
        return asfunction(self.choices[key])(ps)
