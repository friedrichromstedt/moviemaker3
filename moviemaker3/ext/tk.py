import Tkinter
import PIL.ImageTk
import threading
import Queue
import traceback
import numpy
import moviemaker2.ext.render_capsules

"""Provides a Tkinter.Frame descendant capable of rendering with
graphical feedback."""

__all__ = ['RenderFrame']

class StatusBar(Tkinter.Frame):
    """Creates a widget with lots of Labels to display progress in a 
    multithreaded rendering program."""

    def __init__(self, master, nbins=None, 
            *frame_args, **frame_kwargs):
        """*nbins* is the number of bins to use.  For each bin, a Label will 
        be created (at least 1px wide).  All other args and kwargs go to 
        Frame."""
        
        if nbins is None:
            nbins = 1
    
        Tkinter.Frame.__init__(self, master, *frame_args, **frame_kwargs)

        self.labels = []  # .setup() needs .labels initialised.
        self.nbins = nbins

    def setup(self, nslots):
        """Setup the StatusBar.  If *nbins* > *nslots*, *nbins* is set to 
        *nslots*."""
        
        if self.nbins > nslots:
            # This were not useful, because some labels never get set.
            nbins = nslots
        else:
            nbins = self.nbins
        
        self.nslots = nslots

        # Clear.
        for label in self.labels:
            label.destroy()

        # Create.
        self.labels = []
        self.states_bins = numpy.zeros(nbins)
        self.states_slots = numpy.zeros(self.nslots)
        self.state_unset = 0
        self.state_ok = 1
        self.state_error = 2
        for index in xrange(0, nbins):
            label = Tkinter.Label(self, background='lightgray',
                borderwidth=0)
            label.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=True)
            self.labels.append(label)

        # To calculate the bin, use SLOT * .SLOPE
        self.slope = float(nbins) / float(self.nslots)

    def enable(self, slot):
        """Turns on the label with index *slot*."""

        bin = int(slot * self.slope)
        if self.states_bins[bin] != self.state_error:
            self.labels[bin].configure(background='gray')
            self.states_bins[bin] = self.state_ok
        self.states_slots[slot] = self.state_ok

        self.check_set_green()

    def check_set_green(self):
        """Checks if the process is finished."""

        # If all done, set to all-green except those with errors.
        if self.state_unset not in self.states_slots:
            for (state, label) in zip(self.states_slots, self.labels):
                if state == self.state_ok:
                    label.configure(background = 'green')

    def error(self, slot):
        """Signals an error in slot SLOT."""

        bin = int(slot * self.slope)
        self.labels[bin].configure(background='red')
        self.states_bins[bin] = self.state_error
        self.states_slots[slot] = self.state_error

        self.check_set_green()

class RenderFrame(Tkinter.Frame):
    """A Tkinter.Frame which can render events with graphical feedback.  The
    .start() method must be called once to start the polling mechanism. 
    
    Use the .render_queue as argument to a Renderer's .render() method."""

    def __init__(self, master, nbins=None,
            *frame_args, **frame_kwargs):
        """*nbins* is the number of sections used for the status bar.
        *frame_args* and *frame_kwargs* go to the ``Frame`` class."""

        Tkinter.Frame.__init__(self, *frame_args, **frame_kwargs)

        # Initialise attributes ...

        # The message queue for ImageCapsules:
        self.render_queue = Queue.Queue()

        # Initialise status bar ...

        self.status_bar = StatusBar(self, nbins=nbins)
        self.status_bar.pack(side=Tkinter.TOP, fill=Tkinter.X)

        # Initialise display ...
        
        self.canvas = Tkinter.Canvas(self, highlightthickness=0)
        self.canvas.pack(side=Tkinter.TOP)
        self.photo_id = None

        self.spacer = Tkinter.Label(self, text='Moviemaker2 Output')
        self.spacer.pack(side=Tkinter.TOP)
    
        self.start()

    def setup(self, nslots):
        """Sets the slots and bin number.  *nslots* is the number of frames
        to be rendered.  *nbins* should be some reasonably smaller number."""
        self.status_bar.setup(nslots=nslots)

    def start(self):
        """Starts the polling mechanism essential for visual feedback."""

        self.after(100, self.poll)

    def poll(self):
        """Grabs all items from the .render_queue, displays the latest
        frame, and enables all frames' status slot.
        
        Will poll again after 100 ms."""

        try:
            # Poll all capsules ...

            capsules = []
            try:
                while True:
                    capsules.append(self.render_queue.get(block=False))
            except Queue.Empty:
                pass

            if len(capsules) == 0:
                self.after(100, self.poll)
                return

            # Find the latest capsule ...

            # Set all slots involved ...

            image_capsules = []
            for capsule in capsules:
                if isinstance(capsule,
                        moviemaker2.ext.render_capsules.AnnounceCapsule):
                    self.status_bar.setup(nslots=capsule.nframes)
                elif isinstance(capsule, 
                        moviemaker2.ext.render_capsules.ResultCapsule):
                    if not capsule.error:
                        self.status_bar.enable(capsule.frameindex)
                    else:
                        self.status_bar.error(capsule.frameindex)
                    image_capsules.append(capsule)

            # Display the latest frame without errors ...

            image_capsules.sort(key=lambda c: c.frameindex)

            for index in xrange(-1, -len(image_capsules) - 1, -1):
                capsule = image_capsules[index]
                if not capsule.error:
                    photo_image = PIL.ImageTk.PhotoImage(capsule.image)
                    old_id = self.photo_id
                    self.canvas.configure(width=capsule.image.size[0],
                        height=capsule.image.size[1])
                    self.photo_id = self.canvas.create_image((0, 0),
                        image=photo_image, anchor=Tkinter.NW)
                    if old_id is not None:
                        self.canvas.delete(old_id)
                    # need to store a ref to the image, else it gets
                    # deleted, as well as its display on the canvas.
                    self.photo_image = photo_image
                    break

        except Exception, exc:
            print "(RenderFrame) Exception while polling:"
            traceback.print_exc()

        self.after(100, self.poll)

