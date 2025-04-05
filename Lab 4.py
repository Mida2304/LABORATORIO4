import sys
import csv
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox, QFileDialog
from PyQt6.QtCore import QTimer
import numpy as np
import pyqtgraph as pg
from scipy.signal import butter, filtfilt, iirnotch
from scipy.signal.windows import hamming, hann
from scipy.fft import fft
from scipy.stats import ttest_rel
import pyqtgraph.exporters

class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LABORATORIO 4 - EMG")
        self.setGeometry(200, 200, 1000, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QHBoxLayout(self.main_widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffbd8f;
            }
            QPushButton {
                background-color: #ff7514;
                color: black;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d15600;
            }
        """)

        self.FS = 1000
        self.N_SAMPLES = 100
        self.WINDOW_SIZE = 256
        self.data = np.zeros(self.FS)
        self.filtered_data = np.zeros(self.FS)
        self.recording = False
        self.file = None
        self.writer = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.task = None

        self.initUI()

    def initUI(self):
        graph_layout = QVBoxLayout()
        button_layout = QVBoxLayout()

        self.graph = pg.PlotWidget()
        self.graph.setBackground('k')
        self.curve = self.graph.plot(self.data, pen='w')
        graph_layout.addWidget(self.graph)

        self.fft_graph = pg.PlotWidget()
        self.fft_graph.setBackground('k')
        self.fft_curve = self.fft_graph.plot([], pen='y')
        graph_layout.addWidget(self.fft_graph)

        self.window_graph = pg.PlotWidget()
        self.window_graph.setBackground('k')
        self.hamming_curve = self.window_graph.plot([], pen='r', name="Hamming")
        self.hanning_curve = self.window_graph.plot([], pen='b', name="Hanning")
        self.hamming_applied_curve = self.window_graph.plot([], pen='m', name="Hamming Aplicado")
        self.hanning_applied_curve = self.window_graph.plot([], pen='c', name="Hanning Aplicado")
        graph_layout.addWidget(self.window_graph)

        self.compare_graph = pg.PlotWidget()
        self.compare_graph.setBackground('k')
        self.original_curve = self.compare_graph.plot([], pen='w', name="Original")
        self.filtered_curve = self.compare_graph.plot([], pen='g', name="Filtrada")
        graph_layout.addWidget(self.compare_graph)

        for label, func in [
            ("Guardar Gráfica", self.save_graph),
            ("Test de Hipótesis", self.hypothesis_test),
            ("Iniciar Captura", self.start_acquisition),
            ("Detener Captura", self.stop_acquisition),
            ("Análisis Espectral", self.compute_fft),
            ("Aplicar Filtro", lambda: self.apply_filter(self.data)),
            ("Mostrar Ventanas", self.show_windows),
            ("Cargar CSV", self.load_csv),
            ("Comparar Señales", self.plot_comparison)
        ]:
            button = QPushButton(label)
            button.clicked.connect(func)
            button_layout.addWidget(button)

        button_layout.addStretch()
        self.layout.addLayout(graph_layout, stretch=3)
        self.layout.addLayout(button_layout, stretch=1)

    def start_acquisition(self):
        try:
            import nidaqmx
            from nidaqmx.constants import AcquisitionType

            self.task = nidaqmx.Task()
            self.task.ai_channels.add_ai_voltage_chan("Dev3/ai2")
            self.task.timing.cfg_samp_clk_timing(self.FS, sample_mode=AcquisitionType.CONTINUOUS)
            self.timer.start(1000)

            self.file = open("emg_data.csv", "w", newline="")
            self.writer = csv.writer(self.file)
            self.writer.writerow(["Tiempo (s)", "Voltaje (V)"])
            self.recording = True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo iniciar la captura: {str(e)}")

    def stop_acquisition(self):
        if self.task:
            self.task.close()
            self.task = None
        self.timer.stop()
        self.save_graph_image(self.graph, "grafica_emg.png")
        if self.file:
            self.file.close()
            self.file = None
            self.recording = False

    def update_plot(self):
        try:
            if self.task:
                values = self.task.read(number_of_samples_per_channel=self.N_SAMPLES)
                self.data = np.roll(self.data, -self.N_SAMPLES)
                self.data[-self.N_SAMPLES:] = values
                self.filtered_data = self.apply_filter(self.data)
                self.curve.setData(self.filtered_data)

                if self.recording and self.writer:
                    time_values = np.linspace(0, len(values)/self.FS, len(values))
                    for t, v in zip(time_values, values):
                        self.writer.writerow([t, v])
        except Exception as e:
            print(f"Error al leer datos: {e}")
            self.stop_acquisition()

    def apply_filter(self, data):
        b_high, a_high = butter(4, 20/(self.FS/2), btype='high')
        b_low, a_low = butter(4, 450/(self.FS/2), btype='low')
        notch_b, notch_a = iirnotch(50/(self.FS/2), 30)
        filtered_data = filtfilt(b_high, a_high, data)
        filtered_data = filtfilt(b_low, a_low, filtered_data)
        filtered_data = filtfilt(notch_b, notch_a, filtered_data)
        return filtered_data

    def compute_fft(self):
        windowed_data = self.filtered_data * hann(len(self.filtered_data))
        fft_result = np.abs(fft(windowed_data))[:len(self.filtered_data)//2]
        freqs = np.fft.fftfreq(len(self.filtered_data), d=1/self.FS)[:len(self.filtered_data)//2]
        self.fft_curve.setData(freqs, fft_result)

    def show_windows(self):
        x = np.linspace(0, 1, self.WINDOW_SIZE)
        hamming_win = hamming(self.WINDOW_SIZE, sym=False)
        hanning_win = hann(self.WINDOW_SIZE, sym=False)
        self.hamming_curve.setData(x, hamming_win)
        self.hanning_curve.setData(x, hanning_win)

        segment = self.filtered_data[-self.WINDOW_SIZE:]
        hamming_applied = segment * hamming_win
        hanning_applied = segment * hanning_win
        self.hamming_applied_curve.setData(x, hamming_applied)
        self.hanning_applied_curve.setData(x, hanning_applied)

    def hypothesis_test(self):
        if len(self.data) != len(self.filtered_data):
            QMessageBox.warning(self, "Advertencia", "Las señales no tienen la misma longitud.")
            return

        try:
            if np.all(self.data == 0) or np.all(self.filtered_data == 0):
                QMessageBox.warning(self, "Advertencia", "Una de las señales es completamente cero. No se puede realizar el test.")
                return

            t_stat, p_val = ttest_rel(self.data, self.filtered_data, nan_policy='omit')
            resultado = f"t = {t_stat:.4f}, p = {p_val:.4f}"

            if p_val < 0.05:
                resultado += "\n→ Diferencia significativa entre señales original y filtrada."
            else:
                resultado += "\n→ No hay diferencia significativa."

            QMessageBox.information(self, "Test de Hipótesis", resultado)
            print("Test de hipótesis realizado:", resultado)

            with open("resultado_ttest.txt", "w") as f:
                f.write(resultado)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo realizar el test: {str(e)}")

    def plot_comparison(self):
        self.original_curve.setData(self.data, pen='w')
        self.filtered_curve.setData(self.filtered_data, pen='g')
        self.save_graph_image(self.compare_graph, "comparacion_senales.png")

    def save_graph_image(self, plot_widget, filename):
        try:
            exporter = pg.exporters.ImageExporter(plot_widget.plotItem)
            exporter.export(filename)
        except Exception as e:
            print(f"Error al guardar imagen: {e}")

    def save_graph(self):
        self.save_graph_image(self.graph, "grafica_emg.png")
        QMessageBox.information(self, "Guardado", "Gráfica guardada como 'grafica_emg.png'.")

    def load_csv(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, "Cargar archivo CSV", "", "CSV Files (*.csv)")
            if not path:
                return
            times, voltages = [], []
            with open(path, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    times.append(float(row[0]))
                    voltages.append(float(row[1]))
            self.data = np.array(voltages)
            self.filtered_data = self.apply_filter(self.data)
            self.curve.setData(self.filtered_data)
            QMessageBox.information(self, "Carga completa", f"Datos cargados desde {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = Principal()
    viewer.show()
    sys.exit(app.exec())

