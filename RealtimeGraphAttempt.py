import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton
from PyQt5.QtCore import QTimer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Canvas(FigureCanvas):
    def __init__(self, parent):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        super().__init__(self.fig)
        self.setParent(parent)

        self.x = np.linspace(0, 10, 100)
        self.amp = 1
        self.off = 0
        self.phase = 0
        self.step_size = (self.x[-1] - self.x[0]) / len(self.x)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.anim_running = False

    def start_stop_animation(self):
        if self.anim_running:
            self.timer.stop()
        else:
            self.timer.start(100)
        self.anim_running = not self.anim_running

    def update_amp(self, amp):
        self.amp = amp

    def update_off(self, off):
        self.off = off

    def update_phase(self, phase):
        self.phase = phase

    def update_amp(self, amp):
        self.amp = amp
        self.update_plot()

    def update_plot(self):
        self.x += self.step_size
        y = self.amp * np.sin(self.x + self.phase) + self.off

        self.ax.clear()
        self.ax.plot(self.x, y)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_title('Sine Wave')

        self.ax.set_xlim(self.x[0], self.x[-1])

        # Set y-axis limits dynamically based on the amplitude
        min_y = -1.1 * self.amp + self.off  # Adjust the multiplier as needed
        max_y = 1.1 * self.amp + self.off  # Adjust the multiplier as needed
        self.ax.set_ylim(min_y, max_y)

        # Set aspect ratio based on amplitude
        self.ax.set_aspect('auto')

        self.ax.relim()
        self.ax.autoscale_view()

        self.draw()


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sine Wave Generator")
        self.resize(800, 600)

        self.layout = QVBoxLayout()

        self.chart = Canvas(self)
        self.layout.addWidget(self.chart)

        self.label_amp = QLabel("Amplitude")
        self.spin_box_amp = QSpinBox(self)
        self.spin_box_amp.setRange(0, 100)
        self.spin_box_amp.valueChanged.connect(lambda value: self.chart.update_amp(value))
        self.layout.addWidget(self.label_amp)
        self.layout.addWidget(self.spin_box_amp)

        self.label_off = QLabel("Offset")
        self.spin_box_off = QSpinBox(self)
        self.spin_box_off.setRange(0, 100)
        self.spin_box_off.valueChanged.connect(lambda value: self.chart.update_off(value))
        self.layout.addWidget(self.label_off)
        self.layout.addWidget(self.spin_box_off)

        self.label_phase = QLabel("Phase")
        self.spin_box_phase = QSpinBox(self)
        self.spin_box_phase.setRange(0, 100)
        self.spin_box_phase.valueChanged.connect(lambda value: self.chart.update_phase(value))
        self.layout.addWidget(self.label_phase)
        self.layout.addWidget(self.spin_box_phase)

        self.button_start_stop = QPushButton("Start/Stop Animation", self)
        self.button_start_stop.clicked.connect(self.chart.start_stop_animation)

        self.layout.addWidget(self.button_start_stop)

        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())
