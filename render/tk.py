import Tkinter
import matplotlib.figure
import matplotlib.ticker
import matplotlayers
import matplotlayers.backends.tk
import threading
import Queue
import traceback
import numpy

"""Provides a Tkinter.Frame descendant capable of rendering with
graphical feedback."""

__all__ = ['RenderFrame']

class StatusBar(Tkinter.Frame):
    """Creates a widget with lots of Labels to display progress in a 
    multithreaded rendering program."""

    def __init__(self, master, nslots=None, nbins=None, 
            *frame_args, **frame_kwargs):
        """*nslots* is the number of tasks to be done.  *nbins* is the number 
        of bins to use.  For each bin, a Label will be created (at least 1px 
        wide).  All other args and kwargs go to Frame."""
        
        if nslots is None:
            nslots = 1
        if nbins is None:
            nbins = 1
    
        Tkinter.Frame.__init__(self, master, *frame_args, **frame_kwargs)

        self.labels = []  # .setup() needs .labels initialised.
        self.setup(nslots=nslots, nbins=nbins)

    def setup(self, nslots, nbins):
        """Setup the StatusBar.  If *nbins* > *nslots*, *nbins* is set to 
        *nslots*."""
        
        if nbins > nslots:
            # This were not useful, because some labels never get set.
            nbins = nslots
        
        self.nslots = nslots
        self.nbins = nbins

        # Clear.
        for label in self.labels:
            label.destroy()

        # Create.
        self.labels = []
        self.states_bins = numpy.zeros(nbins)
        self.states_slots = numpy.zeros(nslots)
        self.state_unset = 0
        self.state_ok = 1
        self.state_error = 2
        for index in xrange(0, nbins):
            label = Tkinter.Label(self, background='lightgray',
                borderwidth=0)
            label.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=True)
            self.labels.append(label)

        # To calculate the bin, use SLOT * .SLOPE
        self.slope = float(nbins) / float(nslots)

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
            for (state, label) in zip(self.states, self.labels):
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
    
    Use the .capsule_queue as argument to a Renderer's .render() method."""

    def __init__(self, master, nslots=None, nbins=None, shape=None,
            *frame_args, **frame_kwargs):
        """*nslots* should be the number of frames.  *nbins* is the number of
        sections used for the status bar.  *shape* is the extent of the figure
        in pixels, defaulting to (400, 300).  *frame_args* and *frame_kwargs* 
        go to the ``Frame`` class."""

        if shape is None:   
            shape = (400, 300)

        Tkinter.Frame.__init__(self, *frame_args, **frame_kwargs)

        # Initialise attributes ...

        # The message queue for ImageCapsules:
        self.capsule_queue = Queue.Queue()

        # Initialise status bar ...

        self.status_bar = StatusBar(self, nslots=nslots, nbins=nbins)
        self.status_bar.pack(side=Tkinter.TOP, fill=Tkinter.X)

        # Initialise figure ...

        self.figure = matplotlib.figure.Figure(frameon=False)
        self.stack = matplotlayers.Stack(self.figure,
            left=0, bottom=0, width=1, height=1)
        self.stack.set_locators(
            matplotlib.ticker.NullLocator(), matplotlib.ticker.NullLocator())
        
        self.layer_imshow = matplotlayers.LayerImshow()
        self.layer_imshow.configure(origin='lower')
        self.stack.add_layer(self.layer_imshow)

        self.backend_figure = matplotlayers.backends.tk.FigureCanvasTk(
            self, self.figure, shape=shape)
    
        self.start()

    def setup(self, nslots, nbins):
        """Sets the slots and bin number.  *nslots* is the number of frames
        to be rendered.  *nbins* should be some reasonably smaller number."""
        self.status_bar.setup(nslots=nslots, nbins=nbins)

    def start(self):
        """Starts the polling mechanism essential for visual feedback."""

        self.after(100, self.poll)

    def poll(self):
        """Grabs all items from the .capsule_queue, displays the latest
        frame, and enables all frames' status slot.
        
        Will poll again after 100 ms."""

        try:
            # Poll all capsules ...

            capsules = []
            try:
                while True:
                    capsules.append(self.capsule_queue.get(block=False))
            except Queue.Empty:
                pass

            if len(capsules) == 0:
                self.after(100, self.poll)
                return

            # Find the latest capsule ...

            capsules.sort(key=lambda c: c.relative_frameindex)

            # Set all slots involved ...

            for capsule in capsules:
                if not capsule.error:
                    self.status_bar.enable(capsule.relative_frameindex)
                else:
                    self.status_bar.error(capsule.relative_frameindex)

            # Display the latest frame without errors ...

            for index in xrange(-1, -len(capsules) - 1, -1):
                if not capsules[index].error:
                    self.layer_imshow.configure(X=capsules[index].image)
                    self.stack.render()
                    self.backend_figure.update()
                    break

        except Exception, exc:
            print "(RenderFrame) Exception while polling:"
            traceback.print_exc()

        self.after(100, self.poll)
