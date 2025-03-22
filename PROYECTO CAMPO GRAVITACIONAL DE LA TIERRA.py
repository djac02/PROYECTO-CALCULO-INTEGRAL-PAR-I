import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x, y = 2, 0
vx, vy = 0, 1.2  # Velocidad inicial
GM = 10           # Constante gravitacional * masa del sol
dt = 0.01

fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-')
sol, = ax.plot([0], [0], 'yo', markersize=10)

def init():
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    return line,

def update(frame):
    global x, y, vx, vy
    r = np.sqrt(x**2 + y**2)
    ax = -GM * x / r**3  # Aceleración gravitacional en x
    ay = -GM * y / r**3  # Aceleración gravitacional en y
    vx += ax * dt  # ∫a_x dt
    vy += ay * dt  # ∫a_y dt
    x += vx * dt   # ∫v_x dt
    y += vy * dt   # ∫v_y dt
    line.set_data(np.append(line.get_xdata(), x), np.append(line.get_ydata(), y))
    return line,

ani = FuncAnimation(fig, update, frames=1000, init_func=init, blit=True, interval=10)
plt.show()
