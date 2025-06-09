"""
scope.py: A module providing classes for real-time plotting and visualization.

This module contains a collection of classes designed to simplify the process
of visualizing real-time data such as signals, images, and video streams.
"""
import sys
import numpy as np
from array import array
from collections import deque
from time import time
import pyqtgraph as pg

from pyqtgraph.Qt import QtWidgets

if 'PyQt6' in sys.modules:
    from PyQt6.QtCore import Qt
elif 'PyQt5' in sys.modules:
    from PyQt5.QtCore import Qt
else:
    raise ImportError("Scope requires either PyQt5 or PyQt6")


#region : Descriptor Classes
class _ScopeInfo():
    def __init__(self, **kwargs):
        self.title = kwargs.pop('title', None)
        self.rows = kwargs.pop('rows', 1)
        self.cols = kwargs.pop('cols', 1)

        self.maxSampleRate = kwargs.pop('maxSampleRate', 1024) # samples/second
        self.fps = kwargs.pop('fps', 30)

        self.axes = []

class _AxisInfo():
    def __init__(self, **kwargs):
        self._title = kwargs.pop('title', None)
        if self._title is None:
            self._title = kwargs.pop('_title', None)

        self._xLabel = kwargs.pop('xLabel', None)
        if self._xLabel is None:
            self._xLabel = kwargs.pop('_xLabel', None)

        self._yLabel = kwargs.pop('yLabel', None)
        if self._yLabel is None:
            self._yLabel = kwargs.pop('_yLabel', None)

        self._yLim = kwargs.pop('yLim', None)
        if self._yLim is None:
            self._yLim = kwargs.pop('_yLim', None)

        self.row = kwargs.pop('row', 0)
        self.col = kwargs.pop('col', 0)
        self.rowSpan = kwargs.pop('rowSpan', 1)
        self.colSpan = kwargs.pop('colSpan', 1)

        self.signals = []

class _XYAxisInfo(_AxisInfo):
    def __init__(self, **kwargs):
        self._xLim = kwargs.pop('xLim', None)
        if self._xLim is None:
            self._xLim = kwargs.pop('_xLim', None)

        super().__init__(**kwargs)

        self.images = []

class _TYAxisInfo(_AxisInfo):
    def __init__(self, **kwargs):
        self.timeWindow = kwargs.pop('timeWindow', 10)
        self.displayMode = kwargs.pop('displayMode', 0)
        super().__init__(**kwargs)

class _SignalInfo():
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.color = kwargs.pop('color', None)
        self.lineStyle = kwargs.pop('lineStyle', None)
        self.width = kwargs.pop('width', None)
        self.scale = kwargs.pop('scale', 1)
        self.offset = kwargs.pop('offset', 0)

class _ImageInfo(): #XXX
    def __init__(self, **kwargs):
        self._scale = kwargs.pop('scale', (1,1))
        if self._scale is None:
            self._scale = kwargs.pop('_scale', None)

        self._offset = kwargs.pop('offset', (0,0))
        if self._offset is None:
            self._offset = kwargs.pop('_offset', None)

        self._rotation = kwargs.pop('rotation', 0)
        if self._rotation is None:
            self._rotation = kwargs.pop('_rotation', None)

        self._levels = kwargs.pop('levels', (0, 1))
        if self._levels is None:
            self._levels = kwargs.pop('_levels', None)
#endregion

#region : Primary Scope Classes
class MultiScope(_ScopeInfo):
    """MultiScope: A class for creating and a scope with multiple axes.

    This class inherits from _ScopeInfo and allows for the creation and
    management of a scope with multiple axes in a grid layout, supporting both
    time-y and x-y axes.

    Attributes:
        activeScopes (list): A list of active MultiScope instances.
        spf (float): Time to wait between frames.
        tpf (float): Time of the last frame.
    """

    activeScopes = []
    spf = None # time to wait between frames
    tpf = 0 # time of last frame

    def __init__(self, *args, **kwargs):
        """Initialize a MultiScope instance.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        graphicsLayoutWidget = kwargs.pop('graphicsLayoutWidget', None)

        if args and isinstance(args[0], _ScopeInfo):
            super().__init__(**vars(args[0]))
            axes = args[0].axes
        else:
            super().__init__(**kwargs)
            axes = []

        MultiScope.activeScopes.append(self)
        if MultiScope.spf is None:
            MultiScope.spf = 1 / self.fps
        else:
            MultiScope.spf = np.minimum(
                MultiScope.spf,
                1 / self.fps
            )

        # = Create buffers for short term storage of samples prior to plotting
        self._bufferSize = int(np.ceil(2*self.maxSampleRate/self.fps))

        # = Create window object
        if graphicsLayoutWidget is None:
            self.graphicsLayoutWidget = pg.GraphicsLayoutWidget(
                show=True,
                title=self.title
            )
        else:
            self.graphicsLayoutWidget = graphicsLayoutWidget

        # = Create empty grid of cells to be filled with axes later
        self.cells = []
        for i in range(self.rows):
            self.cells.append([None]*self.cols)

        for axis in axes:
            self._addAxis(axis)

    def _cells_available(self,row, col, rowSpan, colSpan):
        # = Check if requested cells outside of grid
        if (row < 0
            or col < 0
            or row+rowSpan > self.rows
            or col+colSpan > self.cols
            ):
            return False

        # = Check if any cells inside the grid are already occupied
        for i in range(rowSpan):
            for j in range(colSpan):
                if self.cells[row+i][col+j] is not None:
                    return False

        return True

    def _populate_cells(self, axis):
        # = Assumes cells_available has already been checked
        for i in range(axis.rowSpan):
            for j in range(axis.colSpan):
                self.cells[axis.row+i][axis.col+j] = axis

    def _addAxis(self, axisInfo):
        if isinstance(axisInfo, _TYAxisInfo):
            AxisType = TYAxis
        elif isinstance(axisInfo, _XYAxisInfo):
            AxisType = XYAxis
        else:
            raise TypeError('Invalid Axis type provided')

        if not self._cells_available(
                axisInfo.row,
                axisInfo.col,
                axisInfo.rowSpan,
                axisInfo.colSpan
            ):
            raise Exception("Scope cell range invalid or already occupied ")

        # = Create a new axis object and add it to the list of axes
        axis = AxisType(
            graphicsLayoutWidget=self.graphicsLayoutWidget,
            bufferSize=self._bufferSize,
            **vars(axisInfo)
        )

        for sig in axisInfo.signals:
            axis.attachSignal(sig)

        if isinstance(axisInfo, _XYAxisInfo):
            for img in axisInfo.images:
                axis.attachImage(img)

        self.axes.append(axis)


    # Really addYtAxis, but addAxis reads nicer...
    def addAxis(self, *args, **kwargs):
        """Add a time-y axis to the MultiScope instance.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        if args:
            if isinstance(args[0], _TYAxisInfo):
                self._addAxis(args[0])
            else:
                raise TypeError(
                    'Must use keyword arguments, unless '
                    + 'providing a _TYAxisInfo object.'
                )
        else:
            self._addAxis(_TYAxisInfo(**kwargs))

    def addXYAxis(self, *args, **kwargs):
        """Add an x-y axis to the MultiScope instance.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        if args:
            if isinstance(args[0], _XYAxisInfo):
                self._addAxis(args[0])
            else:
                raise TypeError(
                    'Must use keyword arguments, unless '
                    + 'providing a _XYAxisInfo object.'
                )
        else:
            self._addAxis(_XYAxisInfo(**kwargs))


    def refresh(self):
        """Refresh the MultiScope instance, updating contained axes.
        """
        MultiScope.refreshAll()

    def refreshAll():
        """Refresh all active MultiScope instances, updating all scope plots.
        """
        if time()-MultiScope.tpf >= MultiScope.spf:
            MultiScope.tpf = time()
            flush = True
        else:
            flush = False

        for scope in MultiScope.activeScopes:
            for axis in scope.axes:
                axis.refresh(flush)

        if flush:
            QtWidgets.QApplication.processEvents()


class Axis(_AxisInfo):
    """Axis: A base class for creating and managing scope plot axes

    This class inherits from _AxisInfo and is used to create and manage
    scope plot axes. It is not meant to be used directly but serves as
    the base class for specialized axis classes (e.g., TYAxis, XYAxis).

    Attributes:
        xLabel (str): The label for the x-axis.
        yLabel (str): The label for the y-axis.
        xLim (tuple): The limits of the x-axis in the form (min, max).
        yLim (tuple): The limits of the y-axis in the form (min, max).
    """

    def __init__(self, graphicsLayoutWidget, bufferSize, **kwargs):
        """Initialize an Axis instance.

        Args:
            graphicsLayoutWidget (GraphicsLayoutWidget): The parent widget.
            bufferSize (int): Buffer size for short term storage of samples.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

        # = Create and Configure Plot
        self.plot = graphicsLayoutWidget.addPlot(
            self.row,
            self.col,
            self.rowSpan,
            self.colSpan,
            labels={
                'bottom': (self._xLabel,),
                'left': (self._yLabel,)
            }
        )
        self.plot.showGrid(x=True, y=True)
        self.plot.addLegend()
        self.yLim = self._yLim

        # = Create buffers for short term storage of samples prior to plotting
        self._bufferSize = bufferSize
        self._tBuffer = array('f', range(bufferSize))
        self._dataBuffer = []
        self._iBuffer = -1
        self._sampleQueue = deque()

        self.refresh = self._initial_refresh

    def attachSignal(self, *args, **kwargs):
        """Attach a signal to the Axis instance.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        di = len(self.signals)
        s = Signal(self.plot, di=di, *args, **kwargs)
        self.signals.append(s)

    def sample(self, t, data):
        """Sample data for the Axis instance.

        Args:
            t (float): The time value.
            data (list): The data samples for each attached signal.
        """
        data = [data] if np.isscalar(data) else data
        self._sampleQueue.appendleft([t, data])

    def clean(self):
        self._sampleQueue.clear

    def clear(self):
        """Clear the signals in the Axis instance."""
        for s in self.signals:
            s.clear()

    def _initial_refresh(self, flush):
        if len(self._sampleQueue) < 2:
            return
        self.refresh = self._post_initial_refresh
        self.refresh(flush)

    def _post_initial_refresh(self, flush):
        pass

    @property
    def xLabel(self):
        """str: The label for the x-axis of the Axis instance."""
        return self._xLabel
    @xLabel.setter
    def xLabel(self, newXLabel):
        self._xLabel = newXLabel
        self.plot.setLabel('bottom', newXLabel)

    @property
    def yLabel(self):
        """str: The label for the y-axis of the Axis instance."""
        return self._yLabel
    @yLabel.setter
    def yLabel(self, newYLabel):
        self._yLabel = newYLabel
        self.plot.setLabel('left', newYLabel)

    @property
    def xLim(self):
        """tuple: The limits of the x-axis in the form (min, max).
            Set to None to enable auto-ranging.
        """
        return self._xLim
    @xLim.setter
    def xLim(self, newXLimits):
        if newXLimits is None:
            self.plot.enableAutoRange(axis='x')
            return
        self._xLim = newXLimits
        self.plot.setXRange(newXLimits[0],newXLimits[1])

    @property
    def yLim(self):
        """tuple: The limits of the y-axis in the form (min, max).
            Set to None to enable auto-ranging.
        """
        return self._yLim
    @yLim.setter
    def yLim(self, newYLimits):
        if newYLimits is None:
            self.plot.enableAutoRange(axis='y')
            return
        self._yLim = newYLimits
        self.plot.setYRange(newYLimits[0],newYLimits[1])


class XYAxis(Axis, _XYAxisInfo):
    """XYAxis: A class for creating and managing an x-y axis in a MultiScope.

    This class inherits from Axis and _XYAxisInfo and is used to create
    and manage an x-y plot axis in a MultiScope.
    """

    def __init__(self, **kwargs):
        """Initialize an XYAxis instance.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.xLim = self._xLim

    def attachSignal(self, *args, **kwargs):
        """Attach a 2D signal to the axis.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        # - x data from 0:self._bufferSize+1
        # - y data from self._bufferSize:self._bufferSize*2+1
        self._dataBuffer.append(array('f', range(2*self._bufferSize)))
        super().attachSignal(*args, **kwargs)

    def attachImage(self, *args, **kwargs):
        """Attach an image to the axis.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.plot.showGrid(x=False, y=False)
        img = Image(self.plot, *args, **kwargs)
        self.images.append(img)

    def _post_initial_refresh(self, flush):
        # = empty out sample queue
        while True: # XXX break if max iterations passed
            try:
                if self._iBuffer >= self._bufferSize-1:
                    flush = True
                    break
                sample = self._sampleQueue.pop()
                self._iBuffer += 1
                self._tBuffer[self._iBuffer] = sample[0]
                for i in range(len(self.signals)):
                    self._dataBuffer[i][self._iBuffer] = sample[1][i][0]
                    self._dataBuffer[i][self._iBuffer+self._bufferSize] = \
                        sample[1][i][1]
            except IndexError:
                break

        if flush and self._iBuffer > 0:
            # = Plot chunk for using new data points
            for i, signal in enumerate(self.signals):
                signal.add_chunk(
                    self._dataBuffer[i][0:self._iBuffer+1],
                    self._dataBuffer[i]\
                        [self._bufferSize:self._bufferSize+self._iBuffer+1]
                )
                self._dataBuffer[i][0] = \
                    self._dataBuffer[i][self._iBuffer]
                self._dataBuffer[i][self._bufferSize] = \
                    self._dataBuffer[i][self._bufferSize+self._iBuffer]

            self._tBuffer[0] = self._tBuffer[self._iBuffer]
            self._iBuffer = 0


class TYAxis(Axis, _TYAxisInfo):
    """TYAxis: A class for creating and managing a time-y axis in a MultiScope.

    This class inherits from Axis and _TYAxisInfo and is used to create
    and manage a time-y plot axis in a MultiScope.
    """

    def __init__(self, **kwargs):
        """Initialize a TYAxis instance.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

    def attachSignal(self, *args, **kwargs):
        """Attach a signal to the TYAxis instance.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        self._dataBuffer.append(array('f', range(self._bufferSize)))
        super().attachSignal(*args, **kwargs)

    def _post_initial_refresh(self, flush):
        # = empty out sample queue
        while True: # XXX break if max iterations passed
            try:
                if self._iBuffer >= self._bufferSize-1:
                    flush = True
                    break
                sample = self._sampleQueue.pop()
                self._iBuffer += 1
                self._tBuffer[self._iBuffer] = sample[0]
                for i in range(len(self.signals)):
                    self._dataBuffer[i][self._iBuffer] = sample[1][i]
            except IndexError:
                break

        if flush and self._iBuffer > 0:
            # = Plot chunk for using new data points
            self.plot.setXRange(
                np.max([0, self._tBuffer[self._iBuffer]-self.timeWindow]),
                np.max([self._tBuffer[self._iBuffer], self.timeWindow]),
                padding=0
            )
            for i, signal in enumerate(self.signals):
                signal.add_chunk(
                    self._tBuffer[0:self._iBuffer+1],
                    self._dataBuffer[i][0:self._iBuffer+1]
                )
                self._dataBuffer[i][0] = \
                    self._dataBuffer[i][self._iBuffer]

            self._tBuffer[0] = self._tBuffer[self._iBuffer]
            self._iBuffer = 0


class Signal(_SignalInfo):
    maxChunks = 1024

    defaultStyles = [
        _SignalInfo(color=[196,78,82], width=1.5, lineStyle='-'),
        _SignalInfo(color=[85,85,85], width=1.5, lineStyle='-.'),
        _SignalInfo(color=[85,168,104], width=1.5, lineStyle=':'),
        _SignalInfo(color=[76,114,176], width=1.5, lineStyle='--'),
        _SignalInfo(color=[248,217,86], width=1.5, lineStyle='-.'),
        _SignalInfo(color=[129,114,179], width=1.5, lineStyle='-..'),
        _SignalInfo(color=[221,132,82], width=1.5, lineStyle='-'),
    ]

    def __init__(self, plot, *args, **kwargs):
        di = kwargs.pop('di', 0)

        if args and isinstance(args[0], _SignalInfo):
            super().__init__(**vars(args[0]))
        else:
            super().__init__(**kwargs)
        self.plot = plot
        self._pDIs = deque()

        # = Configure Cosmetic Properties
        if self.color is None:
            self.color = Signal.defaultStyles[di].color
        if self.width is None:
            self.width = Signal.defaultStyles[di].width
        if self.lineStyle is None:
            self.lineStyle = Signal.defaultStyles[di].lineStyle

        if 'PyQt6' in sys.modules:
            if self.lineStyle == ':':
                lineStyle = Qt.PenStyle.DotLine
            elif self.lineStyle == '--':
                lineStyle = Qt.PenStyle.DashLine
            elif self.lineStyle == '-.':
                lineStyle = Qt.PenStyle.DashDotLine
            elif self.lineStyle == '-..':
                lineStyle = Qt.PenStyle.DashDotDotLine
            else:
                lineStyle = Qt.PenStyle.SolidLine
        else:
            if self.lineStyle == ':':
                lineStyle = Qt.DotLine
            elif self.lineStyle == '--':
                lineStyle = Qt.DashLine
            elif self.lineStyle == '-.':
                lineStyle = Qt.DashDotLine
            elif self.lineStyle == '-..':
                lineStyle = Qt.DashDotDotLine
            else:
                lineStyle = Qt.SolidLine

        self.pen = pg.mkPen(
            color=pg.mkColor(self.color),
            width=self.width,
            style=lineStyle
        )

        self._pDI4Legend = pg.PlotDataItem(name=self.name, pen=self.pen)
        self.plot.addItem(self._pDI4Legend)

    def add_chunk(self, x, y):
        pdi = pg.PlotDataItem(
            x,
            y,
            skipFiniteCheck=True,
            connect='all',
            pen=self.pen
        )
        self.plot.addItem(pdi)
        self._pDIs.append(pdi)

        while len(self._pDIs) > Signal.maxChunks:
            pdi = self._pDIs.popleft()
            self.plot.removeItem(pdi)

    def clear(self):
        # print(len(self._pDIs))
        while len(self._pDIs) > 0:
            pdi = self._pDIs.popleft()
            self.plot.removeItem(pdi)


class Image(_ImageInfo):
    """Image: A class for containing and managing images to be plotted

    This class inherits from _ImageInfo and provides additional functionality
    for displaying images within a scope, including scaling, offset, and
    rotation.
    """

    def __init__(self, plot, *args, **kwargs):
        """
        Initialize an Image instance.

        Args:
            plot (pg.PlotItem): The plot to which the image will be added.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        if args and isinstance(args[0], _ImageInfo):
            super().__init__(**vars(args[0]))
        else:
            super().__init__(**kwargs)

        self.imageItem = pg.ImageItem(
            levels=self._levels,
            axisOrder='row-major'
        )
        plot.addItem(self.imageItem)

        self._tr = pg.QtGui.QTransform()
        self.scale = self._scale
        self.offset = self._offset
        self.rotation = self._rotation

    def setImage(self, image):
        """Set the image data for the Image instance.

        Args:
            image (np.ndarray): The image data to be displayed.
        """
        self.imageItem.setImage(
            image=image,
            levels=self._levels,
        )

    @property
    def scale(self):
        """Get the scale of the image.

        Returns:
            tuple: The scale factor of the image (x_scale, y_scale).
        """
        return self._scale
    @scale.setter
    def scale(self, newScale):
        """Set the scale of the image.

        Args:
            newScale (tuple): The new scale factor for the image
                (x_scale, y_scale).
        """
        self._scale = newScale
        self._tr.scale(*self._scale)
        self.imageItem.setTransform(self._tr)

    @property
    def offset(self):
        """Get the offset of the image.

        Returns:
            tuple: The offset of the image (x_offset, y_offset).
        """
        return self._offset
    @offset.setter
    def offset(self, newOffset):
        """Set the offset of the image.

        Args:
            newOffset (tuple): The new offset for the image
                (x_offset, y_offset).
        """
        self._offset = newOffset
        self._tr.translate(*self._offset)
        self.imageItem.setTransform(self._tr)

    @property
    def rotation(self):
        """Get the rotation of the image.

        Returns:
            float: The rotation angle of the image in degrees.
        """
        return self._rotation
    @rotation.setter
    def rotation(self, newRotation):
        """Set the rotation of the image.

        Args:
            newRotation (float): The new rotation angle for the image in
                degrees.
        """
        self._rotation = newRotation
        self._tr.rotate(self._rotation)
        self.imageItem.setTransform(self._tr)

    @property
    def levels(self):
        """Get the color levels of the image.

        Returns:
            tuple: The color levels of the image (min_level, max_level).
        """
        return self._levels
    @levels.setter
    def levels(self, newLevels):
        """Set the color levels of the image.

        Args:
            newLevels (tuple): The new color levels for the image
                (min_level, max_level).
        """
        self._levels = newLevels
        self.imageItem.setLevels(self._levels)

#endregion


class Scope():
    """
    Scope: A class for real-time plotting of 1D signals.

    This class provides an interface for real-time visualization of 1D signals,
    such as sensor readings, control signals, or any time-varying data.
    """

    def __init__(self, title=None, **kwargs):
        """Initialize a Scope instance.

        Args:
            title (str, optional): The title of the scope window.
            **kwargs: Additional keyword arguments for creating the axis.
        """
        self._ms = MultiScope(
            title=title,
            graphicsLayoutWidget=kwargs.pop('graphicsLayoutWidget', None),
        )
        self._ms.addAxis(**kwargs)

    def attachSignal(self, **kwargs):
        """Attach a signal to the Scope instance for plotting.

        Args:
            **kwargs: Additional keyword arguments for attaching the signal.
        """
        self._ms.axes[0].attachSignal(**kwargs)

    def sample(self, t, data):
        """Provide a new data sample for the attached signals.

        Args:
            t (float): The timestamp of the data sample.
            data (float or np.ndarray): The new data sample to be plotted.
        """
        self._ms.axes[0].sample(t, data)

    def clean(self):
        self._ms.axes[0].clean()

    def clear(self):
        self._ms.axes[0].clear()

    def refresh(self):
        """Refresh the Scope instance to update the plot with the latest data.
        """
        self._ms.refresh()

    def refreshAll():
        """Refresh all the active Scope instances.
        """
        MultiScope.refreshAll()

class XYScope():
    """XYScope: A class for real-time display of 2D signals and images.

    This class provides an interface for real-time visualization of 2D signals
    and images, updating them in real-time.

    Attributes:
        images (list): A list of attached images for the XYScope instance.
    """

    def __init__(self, title=None, **kwargs):
        """Initialize an XYScope instance.

        Args:
            title (str, optional): The title of the scope window.
            **kwargs: Additional keyword arguments for creating the axis.
        """
        self._ms = MultiScope(
            title=title,
            graphicsLayoutWidget=kwargs.pop('graphicsLayoutWidget', None),
        )
        self._ms.addXYAxis(**kwargs)

        self.images = []

    def attachSignal(self, **kwargs):
        """Attach a signal to the XYScope instance for plotting.

        Args:
            **kwargs: Additional keyword arguments for attaching the signal.
        """
        self._ms.axes[0].attachSignal(**kwargs)

    def attachImage(self, *args, **kwargs):
        """Attach an image to the XYScope instance for display.

        Args:
            *args: Additional arguments for attaching the image.
            **kwargs: Additional keyword arguments for attaching the image.
        """
        self._ms.axes[0].attachImage(*args, **kwargs)
        self.images.append(self._ms.axes[0].images[-1])

    def sample(self, t, data):
        """Provide a new data sample for the attached signals.

        Args:
            t (float): The timestamp of the data sample.
            data (list): The new data sample to be plotted.
        """
        self._ms.axes[0].sample(t, data)

    def clear(self):
        self._ms.axes[0].clear()

    def refresh(self):
        """Refresh the display of the XYScope to update the signals and images.
        """
        self._ms.refresh()

    def refreshAll():
        """Refresh all the active Scope instances.
        """
        MultiScope.refreshAll()