from moviemaker2.function import Function, asfunction

class Centre(Function):
    """Composed of a mesh Function and a vector Function.  Subtracts the
    vector function from the mesh Function.
    
    This can of course be achieved the same using ``Sum``, ``Identity``,
    ``Negative``, but it's easier to write using this class."""

    def __init__(self, mesh, vector):
        """*mesh* is a mesh Function, *vector* a vector function."""

        self.mesh = asfunction(mesh)
        self.vector = asfunction(vector)

    def __call__(self, *args, **kwargs):
        """Subtracts ``.vector()`` from ``.mesh()``."""

        mesh = self.mesh(*args, **kwargs)
        vector = self.vector(*args, **kwargs)

        return mesh - vector
