import sys
from datetime import datetime

import numpy as np
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import pyqtgraph as pg


class SineWavePlotter(QThread):
    data_signal = pyqtSignal(float)

    def __init__(self):
        QThread.__init__(self)
        self.running = False
        self.amplitude = 1.0
        self.offset = 0.0
        self.frequency = 1.0
        self.data = []

    def run(self):
        x = 0
        while self.running:
            y = self.amplitude * np.sin(2 * np.pi * self.frequency * x) + self.offset
            self.data_signal.emit(y)
            self.data.append((time.time(), y))
            x += 0.01
            time.sleep(0.01)

            if len(self.data) >= 6000:  # Save every 1 minute
                self.save_data()

    def update_parameters(self, amplitude, offset, frequency):
        self.amplitude = amplitude
        self.offset = offset
        self.frequency = frequency

    def start_plotting(self):
        self.running = True
        self.start()

    def stop_plotting(self):
        self.running = False
        self.save_data()
        self.wait()

    def save_data(self):
        timestamp = datetime.now()

        # Convert the timestamp to a string
        timestamp_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

        print("Timestamp as string:", timestamp_str)

        np.save(timestamp_str +'.npy', self.data)
        self.data = []


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()

        self.button = QPushButton("Start/Stop Plotting", self)
        left_layout.addWidget(self.button)

        self.amplitude_input = QLineEdit(self)
        self.amplitude_input.setPlaceholderText("Amplitude")
        self.amplitude_input.textChanged.connect(self.update_parameters)
        left_layout.addWidget(self.amplitude_input)

        self.offset_input = QLineEdit(self)
        self.offset_input.setPlaceholderText("Offset")
        self.offset_input.textChanged.connect(self.update_parameters)
        left_layout.addWidget(self.offset_input)

        self.frequency_input = QLineEdit(self)
        self.frequency_input.setPlaceholderText("Frequency")
        self.frequency_input.textChanged.connect(self.update_parameters)
        left_layout.addWidget(self.frequency_input)

        main_layout.addLayout(left_layout)

        self.plot_widget = pg.PlotWidget(self)
        main_layout.addWidget(self.plot_widget)

        self.setLayout(main_layout)

        self.button.clicked.connect(self.toggle_plotting)

        self.plotter = SineWavePlotter()
        self.plotter.data_signal.connect(self.update_plot)
        self.plot_data = []

    def toggle_plotting(self):
        if self.plotter.running:
            self.plotter.stop_plotting()
        else:
            amplitude = float(self.amplitude_input.text())
            offset = float(self.offset_input.text())
            frequency = float(self.frequency_input.text())
            self.plotter.update_parameters(amplitude, offset, frequency)
            self.plotter.start_plotting()

    def update_parameters(self):
        if self.plotter.running:
            try:
                amplitude = float(self.amplitude_input.text())
                offset = float(self.offset_input.text())
                frequency = float(self.frequency_input.text())
                self.plotter.update_parameters(amplitude, offset, frequency)
            except ValueError:
                pass  # Ignore if the input is not a valid float

    def update_plot(self, data):
        self.plot_data.append(data)
        self.plot_widget.plot(self.plot_data, clear=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
