import pyqtgraph as pg
import numpy as np

from PyQt5.QtCore import pyqtSignal


class TimeSeriesWidget(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        pg.GraphicsLayoutWidget.__init__(self, parent)

        self.graph_sensor_1 = self.centralWidget.addPlot()
        self.graph_sensor_1.setDownsampling(mode='peak')
        self.graph_sensor_1.setClipToView(True)

    # public methods
    def update_plot(self, time_stamp, frequency):
        self.graph_sensor_1.plot(time_stamp, frequency)
