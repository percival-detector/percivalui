"""Matplotlib-based 2D image canvas widget for ODIN data viewer.

This class implements a Matplotlib 2D image plotting canvas for displaying
generic frames. It is different from the original in that it is
generic and has the capability of showing several types of frame data.

We could delete mplplot.py at some moment as this covers its functionality.

Tim Nichols STFC / WNichols DLS
"""
import numpy as np
import time

import matplotlib
from matplotlib.backends.qt_compat import QtCore, QtWidgets

if QtCore.qVersion()[0]=='5':
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.colorbar import make_axes, Colorbar

# this is a QT widget that has a matplotlib.figure.Figure member.
class MplPlotCanvas(FigureCanvas):
    """
    Matplot plot canvas.

    This class implements the updating 2D image canvas.
    """
    matplotlib.rcParams.update({'font.size': 8})
    cbar_numticks = 9

    def __init__(self, parent=None, dpi=100, labels=('Gain', 'Coarse', 'Fine'),):
        """
        Initialise the plot canvas object.

        This method initialises the plot canvas object, creating an empty subplot
        within it.
        """
        # Create a list what parameters we are plotting.
        self._labels = labels;

        # Create the figure canvas
        self.figure = Figure(dpi=dpi)
        # talking to the superclass here
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.axes = [];
        self.img_shape = dict.fromkeys(self._labels, None);
        self.img_obj = dict.fromkeys(self._labels, None);
        self.colorbar = dict.fromkeys(self._labels, None);

        for i in range(len(self._labels)):
          self.axes.append(self.figure.add_subplot(1, 3, i+1));
          self.axes[i].set_title(self._labels[i]);

        # Set up storage variables
        self.img_range = ()
        self.bar_orient = 'horizontal'
 
        # Render an initial empty image frame
        self.multi_render_frame([None,None,None])
        self.figure.tight_layout()


    def blank_image(self):
        if hasattr(self, "_blank_image")==False:
          img = np.arange(100, dtype=np.uint16);
          img = img.reshape(10,10);
          for r in range(10):
            for c in range(10):
              if r==9-c or r==c:
                img[r,c] = 0;
          self._blank_image = img;
        return self._blank_image;
      

    def multi_render_frame(self, imgs_data, min_val=None, max_val=None):
        """
        convenience function to render the images;
        @param imgs_data a list of np.arrays of length like _labels.
        """
        for i in range( min(len(imgs_data), len(self._labels)) ):
            self.render_frame(imgs_data[i], self.axes[i], self._labels[i], min_val, max_val);


    def render_frame(self, img_data, axe, label, min_val=None, max_val=None):
        """
        Render an image frame in the plot canvas. The pixel data is in img_data
        which may be None.

        This method renders a scaled image and colorbar in the plot canvas. For speed,
        the image data is just updated if there is no change to the image shape, otherwise
        the axes and colorbar are redrawn. None is an acceptable value for an img.
        """

        if (img_data is None):
            img_data = self.blank_image();
        # If the minimum and/or maximum values are not defined, determine from the 
        # incoming image data; This seems to take ~3ms for int16 / float types.
        if min_val is None:
            min_val = np.amin(img_data)
        if max_val is None:
            max_val = np.amax(img_data)

        # If the shape of the incoming data has changed, delete the image object to force
        # a redraw
        if self.img_shape[label] != img_data.shape:
            self.img_shape[label] = img_data.shape
            self.img_obj.update({label: None})

            # Set the colorbar orientation dependent on the aspect ratio of the image
            if self.img_shape[label][0] < self.img_shape[label][1]:
                self.bar_orient = 'horizontal'
            else:
                self.bar_orient = 'vertical'

            # Remove any existing colorbar prior to subsequent re-draw
            if self.colorbar[label] is not None:
                self.colorbar[label].remove()
                self.colorbar.update({label: None})

        # If no image object exists, draw one and add a colorbar
        if self.img_obj[label] is None:
            self.img_obj[label] = axe.imshow(
                img_data, interpolation='nearest', vmin=min_val, vmax=max_val, cmap='jet')
            axe.invert_xaxis()
            if self.colorbar[label] is None:
                cbar_ticks = np.linspace(
                    min_val, max_val, self.cbar_numticks, dtype=np.int32).tolist()
                self.colorbar[label] = self.figure.colorbar(
                    self.img_obj[label], ax=axe, orientation=self.bar_orient, ticks=cbar_ticks)

        # Otherwise just update the image data for speed
        else:
            self.img_obj[label].set_data(img_data)
            axe.draw_artist(self.img_obj[label])

        # If the range of the data changed, update the colorbar accordingly
        if self.img_range != (min_val, max_val):
            self.img_range = (min_val, max_val)
            cbar_ticks = np.linspace(min_val, max_val, self.cbar_numticks, dtype=np.int32).tolist()
            self.colorbar[label].mappable.set_clim(min_val, max_val)
            self.colorbar[label].set_ticks(cbar_ticks)
            self.colorbar[label].draw_all()

        # Draw the frame
        self.draw()

class MplNavigationToolbar(NavigationToolbar):
    """
    Navigation toolbar for the plot canvas.

    This class is a simple wrapper around the imported navigation toolbar.
    """
    def __init__(self, canvas, parent, coordinates=True):
        """Initialise the toolbar."""
        super(MplNavigationToolbar, self).__init__(canvas, parent, coordinates)
