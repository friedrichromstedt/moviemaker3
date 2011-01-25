from moviemaker2.math import MathFunction

__all__ = ['PositionalArg', 'KwArg']

class PositionalArg(MathFunction):
    """Returns a positional argument once called."""

    def __init__(self, position):
        """*position* is the position index of the argument to be returned
        on call."""

        self.position = position

    def __call__(self, *args, **kwargs):
        """Returns the positional argument specified at initialisation 
        time."""

        return args[self.position]

class KwArg(MathFunction):
    """Returns a keyword argument once called."""

    def __init__(self, keyword):
        """*keyword* is the keyword the argument shall have."""

        self.keyword = keyword

    def __call__(self, *args, **kwargs):
        """Returns the keyword argument specified at initialisation time."""

        return kwargs[self.keyword]
