from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets as qtw
import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(qtw.QWidget):
    tanks = ['CIP1', 'CIP2', 'CIP3', 'CIP4', 'CIP5', 'CIP6', 'CIP7']

    def __init__(self):
        super().__init__()
        self.tanks = [1, 2, 3, 4, 5, 6, 7]
        self.cc = [32, 26, 18, 12, 16, 22, 30]
        self.plt = MplCanvas(self, width=5, height=4, dpi=100)
        self.build_ui()

    def build_ui(self):
        self.setWindowTitle("CIP Carbon Controller")
        self.setLayout(qtw.QHBoxLayout())
        self.left_side_panel()
        self.right_side_panel()
        self.show()

    def left_side_panel(self):
        # main container and layout for this widget
        container = qtw.QWidget()
        container.setLayout(qtw.QVBoxLayout())

        # Button for schedulling next batch
        nxt_batch_btn = qtw.QPushButton("Schedule The Next Batch")
        container.layout().addWidget(nxt_batch_btn)
        self.layout().addWidget(container)

    def right_side_panel(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        # Total Carbon Label
        lbl_tot_carbon = qtw.QLabel("Total CIP Carbon: ")
        container.layout().addWidget(lbl_tot_carbon, 0, 0)

        self.plt.axes.plot(self.tanks, self.cc)
        container.layout().addWidget(self.plt, 1, 0, 1, 2)
        self.layout().addWidget(container)

        rdo_manual = qtw.QRadioButton(self)
        rdo_manual.setText("Manual")
        rdo_auto = qtw.QRadioButton(self)
        rdo_auto.setText("Auto")

        container.layout().addWidget(rdo_manual, 2, 0)
        container.layout().addWidget(rdo_auto, 2, 1)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.cc = self.cc[1:] + [random.randint(10, 35)]
        self.plt.axes.cla()
        self.plt.axes.plot(self.tanks, self.cc, 'ro-')
        self.plt.draw()


if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    app.setStyle(qtw.QStyleFactory.create('Fusion'))
    sys.exit(app.exec_())
