#POST_IMPACTO.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# inicial
fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_title("Sistema Didymos-Dimorphos (Post-Impacto)")
ax.set_aspect('equal')
ax.grid(True)

# Parámetros orbitales alterados
radio_orbita = 1.5
velocidad_angular = 0.035  # Órbita más rápida

# Cuerpos celestes
didymos = plt.Circle((0, 0), 0.3, color='#8B4513', label='Didymos')
dimorphos = plt.Circle((radio_orbita, 0), 0.15, color='#FF4500', label='Dimorphos')  # Color naranja por impacto

ax.add_patch(didymos)
ax.add_patch(dimorphos)
ax.legend()

# Trayectoria orbital y escombros
trayectoria, = ax.plot([], [], 'r--', alpha=0.5)
escombros, = ax.plot([], [], 'y.', markersize=2, alpha=0.7)
historia_pos = []
escombros_data = []

def init():
    trayectoria.set_data([], [])
    escombros.set_data([], [])
    return dimorphos, trayectoria, escombros

def animate(i):
    global historia_pos, escombros_data
    angulo = velocidad_angular * i
    x = radio_orbita * np.cos(angulo)
    y = radio_orbita * np.sin(angulo)
    
    # Actualizar posición de Dimorphos
    dimorphos.center = (x, y)
    
    # Actualizar trayectoria
    historia_pos.append((x, y))
    if len(historia_pos) > 100:
        historia_pos.pop(0)
    
    # Generar escombros (puntos aleatorios)
    new_escombros = np.random.normal(scale=0.1, size=(10,2)) + [x, y]
    if len(escombros_data) < 200:
        escombros_data.extend(new_escombros)
    else:
        escombros_data = escombros_data[10:] + new_escombros.tolist()
    
    trayectoria.set_data(*zip(*historia_pos))
    escombros.set_data(*zip(*escombros_data))
    
    return dimorphos, trayectoria, escombros

ani = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=1000, interval=20, blit=True)

plt.show()