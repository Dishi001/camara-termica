import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import zoom

ser = serial.Serial('COM7', 500000, timeout=0.01)
rows, cols = 24, 32
amplificar = 8  # Ampliación visual

def leer_frame():
    datos = np.zeros((rows, cols), dtype=float)
    fila = 0
    while fila < rows:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line == "" or line.startswith("==="): continue
            valores = [float(x) for x in line.split()]
            if len(valores) == cols:
                datos[fila, :] = valores
                fila += 1
        except:
            continue
    return datos


frame_actual = leer_frame()
frame_siguiente = leer_frame()
velocidad = frame_siguiente - frame_actual

alpha = 0.0
delta_alpha = 16 / 40

fig, ax = plt.subplots()
frame_ampliado = zoom(frame_actual, (amplificar, amplificar))
im = ax.imshow(frame_ampliado, cmap='inferno', vmin=20, vmax=40, interpolation='bicubic')
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Temperatura (°C)')

title_text = ax.set_title('Cámara Térmica MLX90640')
temp_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white', fontsize=10,
                    bbox=dict(facecolor='black', alpha=0.5))


def actualizar(frame_num):
    global frame_actual, frame_siguiente, velocidad, alpha, frame_ampliado

    frame_predicho = frame_actual + alpha * velocidad

    frame_ampliado = zoom(frame_predicho, (amplificar, amplificar))
    im.set_data(frame_ampliado)

    temp_text.set_text(f'Max: {np.max(frame_predicho):.1f}°C  Min: {np.min(frame_predicho):.1f}°C  Avg: {np.mean(frame_predicho):.1f}°C')

    alpha += delta_alpha
    if alpha >= 1.0:
        frame_actual = frame_siguiente.copy()
        frame_siguiente = leer_frame()
        velocidad = frame_siguiente - frame_actual
        alpha = 0.0

    return im, temp_text

ani = FuncAnimation(fig, actualizar, interval=25, blit=False)
plt.show()

try:
    while True:
        pass
except KeyboardInterrupt:
    ser.close()
    print("Programa terminado.")
