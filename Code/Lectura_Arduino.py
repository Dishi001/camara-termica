import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configuración del puerto serial
ser = serial.Serial('COM7', 115200, timeout=1)  # Cambia 'COM4' según tu PC
rows, cols = 24, 32

# Crear figura y eje
fig, ax = plt.subplots()
frame = np.zeros((rows, cols))
im = ax.imshow(frame, cmap='inferno', vmin=20, vmax=40)
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Temperatura (°C)')
title_text = ax.set_title('Cámara Térmica MLX90640')
temp_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white', fontsize=10,
                    bbox=dict(facecolor='black', alpha=0.5))

def leer_frame():
    """Lee un frame completo desde la ESP"""
    frame = []
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
        except:
            continue
        if line == "":
            continue
        if line.startswith("==="):  # fin del frame
            break
        valores = [float(x) for x in line.split()]
        if len(valores) == cols:
            frame.append(valores)
    return np.array(frame)

def actualizar(frame_num):
    """Función de animación para actualizar la imagen"""
    global frame
    try:
        frame = leer_frame()
        if frame.shape == (rows, cols):
            im.set_data(frame)
            # Actualizar el texto con temperaturas
            temp_max = np.max(frame)
            temp_min = np.min(frame)
            temp_avg = np.mean(frame)
            temp_text.set_text(f'Max: {temp_max:.1f}°C  Min: {temp_min:.1f}°C  Avg: {temp_avg:.1f}°C')
    except Exception as e:
        print("Error:", e)

# Animación con actualización cada 100 ms y cache deshabilitado (sin warnings)
ani = FuncAnimation(fig, actualizar, interval=100, cache_frame_data=False)
plt.show()

# Mantener el puerto abierto hasta Ctrl+C
try:
    while True:
        pass
except KeyboardInterrupt:
    ser.close()
    print("Programa terminado.")
