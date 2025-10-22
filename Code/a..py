import socket
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import zoom

# ==== CONFIGURACIÓN ====
IP_ESP = "192.168.134.149"  # ⚠️ Reemplazá con la IP que imprime la ESP8266
PUERTO = 1234
rows, cols = 24, 32
amplificar = 4

# ==== CONEXIÓN TCP ====
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Conectando a {IP_ESP}:{PUERTO} ...")
sock.connect((IP_ESP, PUERTO))
sock.settimeout(0.5)
print("Conectado!")

# ==== VARIABLES ====
frame_actual = np.zeros((rows, cols))
frame_siguiente = np.zeros((rows, cols))
alpha = 0.0
delta_alpha = 1 / 6

# ==== FIGURA ====
fig, ax = plt.subplots()
frame_ampliado = zoom(frame_actual, (amplificar, amplificar))
im = ax.imshow(frame_ampliado, cmap='inferno', vmin=20, vmax=40, interpolation='bicubic')
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Temperatura (°C)')

title_text = ax.set_title('Cámara Térmica MLX90640')
temp_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white', fontsize=10,
                    bbox=dict(facecolor='black', alpha=0.5))

# ==== FUNCIONES ====
def leer_frame():
    datos = np.zeros((rows, cols), dtype=float)
    fila = 0
    buffer = ""
    while fila < rows:
        try:
            chunk = sock.recv(4096).decode('utf-8', errors='ignore')
            if not chunk:
                continue
            buffer += chunk

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if line == "" or line.startswith("==="):
                    continue
                valores = [float(x) for x in line.replace(",", " ").split()]
                if len(valores) == cols:
                    datos[fila, :] = valores
                    fila += 1
                    if fila >= rows:
                        return datos
        except socket.timeout:
            continue
        except Exception as e:
            print("Error:", e)
            continue
    return datos


def actualizar(frame_num):
    global frame_actual, frame_siguiente, frame_ampliado, alpha, delta_alpha

    frame_interp = (1 - alpha) * frame_actual + alpha * frame_siguiente
    frame_ampliado = zoom(frame_interp, (amplificar, amplificar))
    im.set_data(frame_ampliado)

    temp_text.set_text(
        f'Max: {np.max(frame_interp):.1f}°C  Min: {np.min(frame_interp):.1f}°C  Avg: {np.mean(frame_interp):.1f}°C'
    )

    alpha += delta_alpha
    if alpha >= 1.0:
        frame_actual = frame_siguiente.copy()
        frame_siguiente = leer_frame()
        alpha = 0.0

    return im, temp_text


# ==== ANIMACIÓN ====
frame_siguiente = leer_frame()
ani = FuncAnimation(fig, actualizar, interval=11, blit=False)
plt.show()

# ==== SALIDA LIMPIA ====
try:
    while True:
        pass
except KeyboardInterrupt:
    sock.close()
    print("Conexión cerrada.")
