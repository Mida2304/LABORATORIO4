<h1 align="center"> LABORATORIO 4. FATIGA </h1>

Autores: Midalys Vanessa Aux y Manuela Martinez

# Introducción
La fatiga muscular se refiere a la perdida de la capacidad de los musculos de relajarse llegando al fallo siendo un mecanismo de defensa del cuerpo al realizar un ejercicio intenso o deportes de alta intensidad, esto se genera dado que al realizar algun tipo de movimiento que signifique contraccion y fuerza, se acumulan de manera anaerobica hiones de hidrogeno y acido lactico en el musculo interfiriendo conel funcionamiento o union de actina y miosina afectando la contraccion muscular, al momento de llegar al fallo, el musculo pierde fuerza y comienza a sentirse dolor.

En el presente, se plantea el estudio de la fatiga muscular del brazo de una persona con tendonitis que en teoria llegaria mas rapido al fallo.

### Procedimiento:

En primer lugar se crea la interfaz grafica con cada uno de los items a tener en cuenta, como el tomar la captura a tiempo real, guardar todos los datos tomados, plantear el analisis espectral y prueba de hipotesis.

<img src="https://github.com/Mida2304/LABORATORIO4/blob/main/interfaz.png?raw=true" width="20%" />


Posteriormente, gracias a la teoria se planteo en el laboratorio, se procede instalar el programa NI MAX el cual permitira identificar la conexion de DAQ National Instruments, para ser conectado al AD8232 que permitira adquirir la señal EMG.

<img src="https://github.com/Mida2304/LABORATORIO4/blob/main/IMG-20250404-WA0036.jpg?raw=true" width="20%" />

A continuacion se muestra la conexion con el DAQ

<img src="https://github.com/Mida2304/LABORATORIO4/blob/main/IMG-20250404-WA0042.jpg?raw=true" width="40%" />

Posteriormente se realiza la prueba de aquisiscion de datos:

<img src="https://github.com/Mida2304/LABORATORIO4/blob/main/IMG-20250404-WA0040.jpg?raw=true" width="40%" />

### Conceptos para tener en cuenta:
En este siguiente ítem se encuentran los conceptos que se deben tener en cuenta para poder entender de forma más adecuada el presente laboratorio.
##### • [^1^] Señal EMG: En primera instancia hay que tener en cuenta que es EMG, que, gracias a sus siglas, se le conoce como electromiografía. Así mismo, una señal EMG, o, en otras palabras, una señal electromiografía es la corriente eléctrica que se genera cuando un músculo se contrae. La señal EMG permite construir electromiograma, como se puede divisar en el presente laboratorio, el cual corresponde a la suma temporal y espacial de los potenciales de acción de las unidades motoras durante el proceso de contracción muscular, y gracias a ello, se pueden detectar distintas enfermedades o patología como lo es la tendinitis. 
[^1^]: Guzmán-Muñoz, E., & Méndez-Rebolledo, G. (n.d.). Electromiografía en las ciencias de la rehabilitación. Revista Salud Uninorte. http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S0120-55522018000300753#:~:text=La%20se%C3%B1al%20electromiogr%C3%A1fica%20permite%20construir,comportamiento%20bioel%C3%A9ctrico%20muscular%201%2C3. 
##### • [^2^] Tendinitis: La tendinitis es una inflamación de los tendones, los cuales son los tejidos que conectan los músculos a los huesos. Este puede afectar a cualquier tendón del cuerpo, sin embargo, de los más comunes es el de la muñeca, el cual fue el escogido para esta práctica. Al padecer de tendinitis, el músculo afectado posee de menos fuerza puesto que los tendones se encuentran inflamados, por tanto, no van a producir una contracción considerable frente a un músculo totalmente sano, por lo cual se llegará a la fatiga mucho más rápido.
[^2^]: Mayo Foundation for Medical Education and Research. (2023, February 8). Tendinitis. Mayo Clinic. https://www.mayoclinic.org/es/diseases-conditions/tendinitis/symptoms-causes/syc-20378243 
##### • [^3^] Transformada de Fourier: La transformada de Fourier descompone una señal en sus componentes de frecuencia. En otras palabras, convierte una señal en el dominio del tiempo en una representación que permite divisar la distribución de sus frecuencias. 
[^3^]: FFT. MathWorks. (n.d.). https://la.mathworks.com/help/matlab/math/fourier-transforms.html 

Esto es de gran utilidad puesto que muchas señales complejas pueden analizarse de manera más fácil cuando se descomponen en componentes de frecuencia simples (funciones de senos y de cosenos). Esta herramienta es fundamental en el análisis espectral puesto que muestra las frecuencias que están presentes en una señal y cómo estas se distribuyen. 
##### • [^4^] Ventana Hanning: La ventana Hanning es una función matemática que se utiliza principalmente en el procesamiento de señales con el objetivo de suavizar los bordes de una señal; es un de varios intentos de diseñar una ventana en el dominio de Fourier.
[^4^]: Entender la Ventana de Hanning: Una Guía Práctica para principiantes. Wray Castle. (n.d.). https://wraycastle.com/es/blogs/knowledge-base/hanning-window?srsltid=AfmBOor-KA62xrXNMDT5-2604qge4108-baEEFHgdDilFbYUhSqvJYri 
##### • [^5^] Ventana Hamming: Por otra parte, la ventana Hamming es una función usada para concentrar la energía de un cuadro en el espectro, esto con el propósito de reducir la disparidad del borde de una señal al multiplicar cada cuadro con esta función.
[^5^]: Hamming window - an overview | sciencedirect topics. (n.d.-b). https://www.sciencedirect.com/topics/computer-science/hamming-window 
Ambos tipos de ventanas son funciones utilizadas para reducir el efecto de fugas espectrales al momento de aplicar la Transformada de Fourier a señales finitas. Son bastante parecidas, sin embargo, la ventana Hanning puede ser usada si se necesita reducir mucho más el ruido espectral. Por otro lado, si se tiene interés en la resolución espectral, en otras palabras, si se tienen picos más definidos, la ventana Hamming puede ser una mejor opción. En esta práctica se usó una ventana Hanning.
##### • [^6^] Test de hipótesis: Es un procedimiento estadístico que se utiliza para poder decidir si los datos de una muestra proporcionan suficiente evidencia con el propósito de rechazar una afirmación con respecto a una población.
[^6^]: ¿Qué es una prueba de hipótesis?. Minitab. (n.d.). https://support.minitab.com/es-mx/minitab/help-and-how-to/statistics/basic-statistics/supporting-topics/basics/what-is-a-hypothesis-test/ 



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

<img src="https://github.com/Mida2304/LABORATORIO4/blob/main/librerias.png?raw=true" width="20%" />

posteriormente, se crea la adquisicion de datos a tiempo real con DAQ y utilizando el boton iniciar captura se procede a visualizar los datos de la señal EMG a tiempo real.

<img src="https://github.com/Mida2304/LABORATORIO4/blob/main/grafica_emg.png?raw=true" width="20%" />

Despues se realiza el analisis espectral de la señal.

<img src="https://github.com/Mida2304/LABORATORIO4/blob/main/ESPECTRO.png?raw=true" width="20%" />

A continación se realizara una prueba de hipotesis de los datos calculados a partir de medianas calculadar al realizar cada contraccion y el resultado es el siguiente:

<img src="https://github.com/Mida2304/LABORATORIO4/blob/main/t.png?raw=true" width="20%" />




# Requisitos
- Contar con Python 3.9.0 instalado.
- Contar con señal internet.
- Instalar las librerías necesarias instaladas para ejecutar el código correctamente.
- Contar con conocimiento sobre programacion en Python.
- Contar con un AD8232
- Instalar IN MAX
- Tener conocimientos sobre el funcionamiento de DAQ
  
  
# Usar
Por favor, cite este articulo de la siguiente manera:

Aux, M.; Martinez, M.;  LABORATORIO 4. FATIGA. 4 de Abril de 2025.

# Información de contacto

est.manuela.martin@unimilitar.edu.co y est.midalys.aux@unimilitar.edu.co
