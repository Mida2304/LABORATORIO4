import sys
from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import *
import numpy as np
import pyqtgraph as pg
import nidaqmx
from scipy.signal import butter, filtfilt, get_window, welch

class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LABORATORIO 4")
        self.setGeometry(200, 200, 800, 600)

        # Widget principal
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self)

        # Estilo general
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffbd8f;  /* naranja claro */
            }
                    QPushButton {
                background-color: #ff7514; /* naranja pastel */
                color: black;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d15600;  /* naranja más oscuro al pasar el cursor */
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #FFA500;  /* Azul oscuro */
            }
            QTextEdit {
                background-color: #993f00;
                color: #f38f49;
                border-radius: 5px;
                font-size: 14px;
            }
        """)

        self.FS = 1000  # Frecuencia de muestreo en Hz
        self.data = np.zeros(100)  # Datos iniciales simulados
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.task = None  # Inicializa la tarea de nidaqmx

        self.initUI()

    def initUI(self):
        self.graph = pg.PlotWidget()
        self.graph.setBackground('k')  # Fondo negro
        self.curve = self.graph.plot(self.data, pen='w')  # Línea blanca
        self.layout.addWidget(self.graph)

        self.start_button = QPushButton("Iniciar Captura")
        self.start_button.clicked.connect(self.start_acquisition)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Detener Captura")
        self.stop_button.clicked.connect(self.stop_acquisition)
        self.layout.addWidget(self.stop_button)

        self.main_widget.setLayout(self.layout)

    def start_acquisition(self):
        self.task = nidaqmx.Task()
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0")  # Configura el canal adecuado
        self.timer.start(100)  # Actualiza cada 100 ms

    def stop_acquisition(self):
        if self.task:
            self.task.close()
        self.timer.stop()

    def butter_filter(self, data, cutoff, fs, order=4, filter_type='high'):
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)
        return filtfilt(b, a, data)

    def update_plot(self):
        if self.task:
            value = self.task.read()  # Lee el valor del DAQ
            self.data = np.roll(self.data, -1)
            self.data[-1] = value  # Usa el valor real de la EMG
            
            # Filtrado de la señal
            emg_filtered = self.butter_filter(self.data, 20, self.FS, filter_type='high')
            emg_filtered = self.butter_filter(emg_filtered, 450, self.FS, filter_type='low')

            # Transformada de Fourier (FFT)
            ventana = get_window("hamming", len(emg_filtered))
            frequencies, power_spectrum = welch(emg_filtered, self.FS, window=ventana, nperseg=len(emg_filtered))

            # Cálculo de frecuencia mediana
            def frecuencia_mediana(power_spectrum, frequencies):
                total_power = np.sum(power_spectrum)
                cumulative_power = np.cumsum(power_spectrum)
                return frequencies[np.where(cumulative_power >= total_power / 2)[0][0]]
            freq_mediana = frecuencia_mediana(power_spectrum, frequencies)
            print(f"Frecuencia Mediana: {freq_mediana:.2f} Hz")

            # Actualizar gráfico
            self.curve.setData(self.data)

    def calcular_respuesta_impulsiva(self, I0, sigma, d, w, z, u, t):
        x = z - u * t
        es = (I0 / (4 * np.pi * sigma)) * ((1 / np.sqrt((x - w/2)**2 + d**2)) - (1 / np.sqrt((x + w/2)**2 + d**2)))
        return es

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = Principal()
    viewer.show()
    sys.exit(app.exec())
