# PRE_IMPACTO.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Configuración inicial
fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_title("Sistema Didymos-Dimorphos (Pre-Impacto)")
ax.set_aspect('equal')
ax.grid(True)

# Parámetros orbitales
radio_orbita = 2.0
velocidad_angular = 0.02  # Radianes por frame

# Cuerpos celestes
didymos = plt.Circle((0, 0), 0.3, color='#8B4513')
dimorphos = plt.Circle((radio_orbita, 0), 0.15, color='#808080')

ax.add_patch(didymos)
ax.add_patch(dimorphos)

# Trayectoria orbital
trayectoria, = ax.plot([], [], 'b--', alpha=0.5)
historia_pos = []

# Configurar frames para completar un ciclo completo
frames_total = int(2 * np.pi / velocidad_angular)  # 314 frames para 2π radianes

def init():
    dimorphos.center = (radio_orbita, 0)
    trayectoria.set_data([], [])
    return dimorphos, trayectoria

def animate(i):
    angulo = velocidad_angular * i
    x = radio_orbita * np.cos(angulo)
    y = radio_orbita * np.sin(angulo)
    
    dimorphos.center = (x, y)
    historia_pos.append((x, y))
    
    # Mantener solo un ciclo completo de puntos
    if len(historia_pos) > frames_total:
        historia_pos.pop(0)
    
    trayectoria.set_data(*zip(*historia_pos))
    return dimorphos, trayectoria

ani = animation.FuncAnimation(
    fig, animate,
    init_func=init,
    frames=frames_total,  # Exactamente un ciclo orbital
    interval=20,
    blit=True,
    repeat=True  # Bucle infinito
)

plt.show()