from PyQt5 import QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from matplotlib.figure import Figure
import matplotlib.dates as m_dates
import matplotlib as plt


class MplCanvas(Canvas):  # Matplotlib canvas class to create figure
    axes = ...  # type: Figure.axes

    def __init__(self, width=3.0, height=2.0, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, constrained_layout=True)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        # Canvas.__init__(self, self.fig)
        # Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # Canvas.updateGeometry(self)


class MplWidget(QtWidgets.QWidget):  # Matplotlib widget

    canvas = ...  # type: MplCanvas

    def __init__(self, parent=None, width=3.0, height=2.0, dpi=100):
        QtWidgets.QWidget.__init__(self, parent)  # Inherit from QWidget
        self.canvas = MplCanvas(width, height, dpi)  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout(parent)  # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.rect = None
        self.date_fmt = m_dates.DateFormatter("%a %d %b")
        self.week_loc = m_dates.WeekdayLocator()
        self.toolbar = NavigationToolbar(self.canvas, self)

    def plot_bar(self, legend, data):
        self.rect = self.canvas.axes.bar(legend, data)
        c_map = self.get_c_map(len(self.rect) + 1)
        i = 0
        for rect in self.rect:
            rect.set_color(c_map(i))
            i += 1

    def plot_line(self, legend, data):
        self.canvas.axes.plot(legend, data)

    def set_x_tick(self, **kwargs):
        self.canvas.fig.axes.tick_prams(kwargs)

    def auto_label(self):
        """Attach a text label above each bar in *rect*, displaying its height."""
        for rect in self.rect:
            height = rect.get_height()
            self.canvas.axes.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
                                      xytext=(0, 3),  # 3 points vertical offset
                                      textcoords="offset points",
                                      ha='center', va='bottom')

    def grid(self, state):
        self.canvas.axes.grid(state)

    @staticmethod
    def get_c_map(n, name='hsv'):
        # Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
        # RGB color; the keyword argument name must be a standard mpl colormap name.
        return plt.cm.get_cmap(name, n)
