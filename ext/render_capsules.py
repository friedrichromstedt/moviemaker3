"""Capsules to be used with rendering."""

class AnnounceCapsule:
    """Holds the number of frames to be rendered."""

    def __init__(self, nframes):
        """*nframes* is the number of frames to be rendered.  *shape* is the
        shape of the images transferred later."""

        self.nframes = nframes

class ResultCapsule:
    """Holds an image and its frameindex."""

    def __init__(self, image, frameindex, error=None):
        """*image* is a PIL image representing a frame resulting from 
        rendering.  *frameidx* is the index of the frame, always 
        starting with 0.  *error* (boolean) tells if there was an error."""
        
        if error is None:
            error = False

        self.error = error
        self.image = image
        self.frameindex = frameindex
