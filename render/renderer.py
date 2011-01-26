import Queue
import threading
import traceback
import os.path
import numpy
import numpypic
import moviemaker2.time

"""Provides a multithreaded rendering engine."""

__all__ = ['Renderer']

class ResultCapsule:
    """Holds an image and its frameindex."""

    def __init__(self, image, relative_frameindex, error=None):
        """*image* is a PIL image representing a frame resulting from 
        rendering.  *relative_frameidx* is the index of the frame, always 
        starting with 0.  *error* (boolean) tells if there was an error."""
        
        if error is None:
            error = False

        self.error = error
        self.image = image
        self.relative_frameindex = relative_frameindex

class Renderer:
    """Holds the parameters of a video and the event, and runs the 
    rendering.  Initially supported timelines are ``'realtime'`` and
    ``'frametime'``."""

    def __init__(self, layer, framerate, mesh,
            directory, extension=None, prefix=None,
            nthreads=None,
            startrealtime=None, stoprealtime=None,
            startframetime=None, stopframetime=None):
        """
        *   *layer* is the Layer to be rendered (might be a stack, of course).
        *   *directory* is the output directory, *extension* the filename
            extension.  *prefix* will be prepended to the filename.
        *   Rendering will use *nthreads* threads.
        *   Times can be given either by frametime or by realtime.  The 
            frametimes given have precedence over the realtimes given.
        *   *mesh* is the mesh to use to render, determining the resoltion
            of the output.
        """ 

        if extension is None:
            extension = 'png'
        if prefix is None:
            prefix = ''
        if nthreads is None:
            nthreads = 1
        
        self.layer = layer
        self.framerate = framerate
        self.nthreads = nthreads

        self.file_template = os.path.join(directory, 
            '%s%%06d.%s' % (prefix, extension))

        # Get the duration to render ...

        if startrealtime is not None:
            self.startframetime = int(startrealtime * framerate)
        if stoprealtime is not None:
            self.stopframetime = int(stoprealtime * framerate)

        if startframetime is not None:
            self.startframetime = int(startframetime)
        if stopframetime is not None:
            self.stopframetime = int(stopframetime)

        self.nframes = self.stopframetime - self.startframetime + 1

        # It is intentional that the stored times may deviate from the 
        # times handed over, because they represent the times of frames.
        self.startrealtime = self.startframetime / float(self.framerate)
        self.stoprealtime = self.stopframetime / float(self.framerate)

        self.mesh = mesh

        # Initialise the queue ...

        self.queue = Queue.Queue()

        for frametime in xrange(self.startframetime, self.stopframetime + 1):
            self.queue.put(frametime)

    def start_rendering(self, capsule_queue=None):
        """Renders to HDD and puts ImageCapsules into *capsule_queue* if
        given."""

        for threadindex in xrange(0, self.nthreads):
            thread = threading.Thread(target=self._render,
                kwargs=dict(capsule_queue=capsule_queue))
            thread.setDaemon(True)
            thread.start()

    def _render(self, capsule_queue=None):
        """*capsule_queue* is optional."""
        
        frametimeline = moviemaker2.time.Timeline('frametime')
        realtimeline = moviemaker2.time.Timeline('realtime')

        while not self.queue.empty():
            try:
                # Another thread may have raced, we have to not-block.
                frametime = self.queue.get(block=False)
                realtime = float(frametime) / self.framerate
                try:
                    time = realtimeline.extend(realtime,
                        frametimeline.extend(frametime))

                    layer = self.layer(time=time, mesh=self.mesh)
                    R = layer.R.data()
                    G = layer.G.data()
                    B = layer.B.data()
                    image = numpy.rollaxis(numpy.asarray([R, G, B]), 0, 3)
                    numpypic.writepicrgb(self.file_template % frametime,
                        (image * 255).astype(numpy.int))

                    if capsule_queue is not None:
                        capsule_queue.put(ResultCapsule(
                            image=image, 
                            relative_frameindex=(frametime - 
                                self.startframetime)))
                except:
                    print "(Renderer) Exception in frame", frametime, 
                    print "at time", realtime, ":"
                    traceback.print_exc()
                    if capsule_queue is not None:
                        capsule_queue.put(ResultCapsule(
                            image=None,
                            relative_frameindex=(frametime - 
                                self.startframetime),
                            error=True))

                self.queue.task_done()
            except Queue.Empty:
                # Well, another thread was faster.
                pass
