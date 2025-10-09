import serial
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import zoom

# Configuración del puerto
puerto = 'COM4'
baudrate = 9600
arduino = serial.Serial(puerto, baudrate, timeout=5)

cols = 180  # número de pasos del servo (0.5° por paso)
rows = 150  # resolución vertical deseada
temperaturas = np.zeros(cols)

plt.ion()
fig, ax = plt.subplots()
mapa = ax.imshow(np.zeros((rows, cols)), cmap='plasma', interpolation='bicubic')
cbar = plt.colorbar(mapa)
cbar.set_label("Temperatura (°C)")
ax.set_title("Mapa térmico cuadrado un solo servo")

try:
    while True:
        # Leer todas las temperaturas del barrido horizontal
        for i in range(cols):
            linea = arduino.readline().decode('utf-8').strip()
            if linea and linea != "---Escaneo---":
                temperaturas[i] = float(linea)

        # Crear matriz cuadrada repitiendo verticalmente
        matriz = np.tile(temperaturas, (rows,1))
        matriz_suave = zoom(matriz, (1,1), order=3)

        t_min = np.nanmin(matriz_suave)
        t_max = np.nanmax(matriz_suave)
        rango = t_max - t_min
        vmin = t_min - 0.2*rango
        vmax = t_max + 0.2*rango

        mapa.set_data(matriz_suave)
        mapa.set_clim(vmin, vmax)
        plt.draw()
        plt.pause(0.01)

        arduino.readline()

except KeyboardInterrupt:
    print("Visualización detenida.")
    arduino.close()
