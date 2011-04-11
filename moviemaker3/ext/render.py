import Queue
import threading
import traceback
import os.path
import numpy
import numpypic
from moviemaker2.parameter import p, Ps
import moviemaker2.layer
import moviemaker2.ext.render_capsules

"""Provides a multithreaded rendering engine."""

__all__ = ['Renderer']

class Render(moviemaker2.layer.Layer):
    """Runs the rendering.  Initially supported timelines are ``'realtime'`` 
    and ``'frametime'``."""

    def __init__(self, fn):
        """
        *   *fn* is the supplier of PIL images.
        """

        self.fn = fn

    def __call__(self, framerate,
            directory, extension=None, prefix=None, nthreads=None,
            startrealtime=None, stoprealtime=None,
            startframetime=None, stopframetime=None,
            render_queue=None, framestep=None):
        """
        *   *framerate* is fps.
        *   *directory* is the output directory, *extension* the filename
            extension.  *prefix* will be prepended to the filename.
        *   Rendering will use *nthreads* threads.
        *   Times can be given either by frametime or by realtime.  The 
            frametimes given have precedence over the realtimes given.
        *   *render_queue* is optional, giving a capsule where to post
            progress.
        *   *args* and *kwargs* are handed over to the Layer this
            ``BoundRenderLayer`` was bound to upon initialisation time.
        *   During rendering, the frametime is stepped with *framestep*.

        Renders to HDD and puts ImageCapsules into *render_queue* if
        given.
        """ 

        if extension is None:
            extension = 'png'
        if prefix is None:
            prefix = ''
        if nthreads is None:
            nthreads = 1
        if framestep is None:
            framestep = 1
        
        file_template = os.path.join(directory, 
            '%s%%06d.%s' % (prefix, extension))

        # Get the duration to render ...

        if startrealtime is not None:
            startframetime = int(startrealtime * framerate)
        if stoprealtime is not None:
            stopframetime = int(stoprealtime * framerate)

        if startframetime is not None:
            startframetime = int(startframetime)
        if stopframetime is not None:
            stopframetime = int(stopframetime)

        nframes = stopframetime - startframetime + 1

        # It is intentional that the stored times may deviate from the 
        # times handed over, because they represent the times of frames.
        startrealtime = startframetime / float(framerate)
        stoprealtime = stopframetime / float(framerate)

        # Initialise the queue ...

        queue = Queue.Queue()

        for frametime in xrange(startframetime, stopframetime + 1, 
                framestep):
            queue.put(frametime)

        # Announce the render ...

        if render_queue is not None:
            render_queue.put(moviemaker2.ext.render_capsules.AnnounceCapsule(
                nframes=nframes))

        # Start the render ...

        for threadindex in xrange(0, nthreads):
            thread = threading.Thread(target=self._render,
                kwargs=dict(queue=queue,
                            render_queue=render_queue,
                            framerate=framerate,
                            file_template=file_template,
                            startframetime=startframetime))
            thread.setDaemon(True)
            thread.start()

    def _render(self, queue, framerate, file_template, startframetime,
            render_queue=None):
        """*render_queue* is optional."""

        frametimeline = p('time/frame')
        realtimeline = p('time/real')

        while not queue.empty():
            try:
                # Another thread may have raced, we have to not-block.
                frametime = queue.get(block=False)
                realtime = float(frametime) / framerate
                try:
                    ps = Ps()
                    ps = frametimeline.store(ps, frametime)
                    ps = realtimeline.store(ps, realtime)

                    image = self.fn(ps)
                    image.save(file_template % frametime)

                    if render_queue is not None:
                        render_queue.put(
                            moviemaker2.ext.render_capsules.ResultCapsule(
                                image=image, 
                                frameindex=(frametime - startframetime)))
                except:
                    print "(Renderer) Exception in frame", frametime, 
                    print "at time", realtime, ":"
                    traceback.print_exc()
                    if render_queue is not None:
                        render_queue.put(
                            moviemaker2.ext.render_capsules.ResultCapsule(
                                image=None,
                                frameindex=(frametime - startframetime),
                                error=True))

                queue.task_done()
            except Queue.Empty:
                # Well, another thread was faster.
                pass
