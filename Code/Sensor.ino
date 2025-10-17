import serial
import numpy as np
import matplotlib.pyplot as plt
import time

# Configuración del puerto serial
ser = serial.Serial('COM4', 115200, timeout=1)  # Cambia 'COM4' por tu puerto

# Tamaño de la matriz del MLX90640
rows = 24
cols = 32

def leer_frame():
    """Lee un frame completo desde la ESP"""
    frame = []
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("Frame recibido") or line == "":
            continue
        if line.startswith("==="):  # Fin del frame
            break
        # Convierte la fila en floats
        valores = [float(x) for x in line.split()]
        if len(valores) == cols:
            frame.append(valores)
    return np.array(frame)

def mostrar_imagen(frame):
    """Muestra la matriz como imagen térmica"""
    plt.imshow(frame, cmap='inferno')  # 'inferno' es un buen colormap térmico
    plt.colorbar(label='Temperatura (°C)')
    plt.title('Imagen Térmica MLX90640')
    plt.show()

# Loop principal
try:
    while True:
        frame = leer_frame()
        if frame.shape == (rows, co
