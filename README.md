<h1 align="center"> LABORATORIO 4. FATIGA </h1>

Autores: Midalys Vanessa Aux y Manuela Martinez

# Introducción
La fatiga muscular se refiere a la perdida de la capacidad de los musculos de relajarse llegando al fallo siendo un mecanismo de defensa del cuerpo al realizar un ejercicio intenso o deportes de alta intensidad, esto se genera dado que al realizar algun tipo de movimiento que signifique contraccion y fuerza, se acumulan de manera anaerobica hiones de hidrogeno y acido lactico en el musculo interfiriendo conel funcionamiento o union de actina y miosina afectando la contraccion muscular, al momento de llegar al fallo, el musculo pierde fuerza y comienza a sentirse dolor.

En el presente, se plantea el estudio de la fatiga muscular del brazo de una persona con tendonitis que en teoria llegaria mas rapido al fallo.

### Procedimiento:

En primer lugar se crea la interfaz grafica con cada uno de los items a tener en cuenta, como el tomar la captura a tiempo real, guardar todos los datos tomados, plantear el analisis espectral y prueba de hipotesis.

<img src="https://github.com/Mida2304/LABORATORIO4/blob/main/interfaz.png?raw=true" width="40%" />

### Conceptos para tener en cuenta:


# Análisis
Para el procedimiento anterior se tienen que tomar en cuenta las siguientes librerias:
##### - sys: Interactuar con sistema operativo de la interfaz.
##### - csv: Sirve para leer y escribir archivos en formatos CSV.
##### - PyQt6: Libreria empelada para la creación de la interfaz grafica, botones, ventanas y muestra de la adquisicion de los datos.
##### - numpy: Para la realización de calculos numericos, estadistica, algebra y arreglos. 
##### - pyqtgraph: Para graficar datos dentro de la interfaz en tiempo real.
##### - nidaqmx: libreria empleada para controlar dispositivos de adquisición de National Instruments NI DAQ, leyendo directamente la señal EMG de la targeta de adquisicion (en el caso del presente, se empleo un AD8232).
##### - AcquisitionType: Para especificar el tipo de adquisicion de datos (lectura continua o captura puntual).
##### - butter, filtfilt, iirnotch: Crea un filtro Butterworth sin cambiar la fase y un filtro rechaza banda para eliminar el ruido de 50 a 60 Hz, filtrando y suavizando la señal.
##### - hamming, hann: La creacion de estas ventanas, atenuan los extremos de las señales para evitar errores por los bordes abruptos.
##### - fft: Es para realizar los calculos de la transformada de Fourier para analizar el contenido en frecuencia de una señal.
##### - ttest_rel: Esta libreria se utiliza para realizar la prueba de hipotesis de t muestras relacionadas.



# Requisitos
- Contar con Python 3.9.0 instalado.
- Contar con señal internet.
- Instalar las librerías necesarias instaladas para ejecutar el código correctamente.
- Contar con conocimiento sobre programacion en Python.
- 
# Usar
Por favor, cite este articulo de la siguiente manera:

Aux, M.; Martinez, M.;  LABORATORIO 4. FATIGA. 4 de Abril de 2025.

# Información de contacto

est.manuela.martin@unimilitar.edu.co y est.midalys.aux@unimilitar.edu.co
