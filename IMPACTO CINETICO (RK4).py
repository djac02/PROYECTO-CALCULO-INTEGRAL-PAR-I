import numpy as np
import matplotlib.pyplot as plt

# Constantes
G = 6.67430e-11  # m³ kg⁻¹ s⁻²
M_earth = 5.972e24  # kg
R_earth = 6.371e6  # metros
altura_asteroide = 400e3  # 400 km
r_asteroide = R_earth + altura_asteroide
v_asteroide = np.sqrt(G * M_earth / r_asteroide)  # Velocidad orbital

# Parámetros de simulación
t_total = 60  # segundos
dt = 0.1  # paso de tiempo (mayor precisión)
pasos = int(t_total / dt)

# Condiciones iniciales del asteroide
estado_asteroide = np.array([r_asteroide, 0.0, 0.0, v_asteroide])  # x, y, vx, vy

# Condiciones iniciales del proyectil (ajustadas para impacto)
v0_x = 7500  # Componente radial
v0_y = v_asteroide + 50  # Componente tangencial
estado_proyectil = np.array([R_earth, 0.0, v0_x, v0_y])  # x, y, vx, vy

def aceleracion_gravitacional(x, y):
    r = np.sqrt(x**2 + y**2)
    ax = -G * M_earth * x / r**3
    ay = -G * M_earth * y / r**3
    return ax, ay

def paso_rk4(estado, dt):
    x, y, vx, vy = estado
    ax1, ay1 = aceleracion_gravitacional(x, y)
    k1x = vx
    k1y = vy
    
    ax2, ay2 = aceleracion_gravitacional(x + k1x*dt/2, y + k1y*dt/2)
    k2x = vx + ax1*dt/2
    k2y = vy + ay1*dt/2
    
    ax3, ay3 = aceleracion_gravitacional(x + k2x*dt/2, y + k2y*dt/2)
    k3x = vx + ax2*dt/2
    k3y = vy + ay2*dt/2
    
    ax4, ay4 = aceleracion_gravitacional(x + k3x*dt, y + k3y*dt)
    k4x = vx + ax3*dt
    k4y = vy + ay3*dt
    
    x_nuevo = x + (k1x + 2*k2x + 2*k3x + k4x) * dt / 6
    y_nuevo = y + (k1y + 2*k2y + 2*k3y + k4y) * dt / 6
    vx_nuevo = vx + (ax1 + 2*ax2 + 2*ax3 + ax4) * dt / 6
    vy_nuevo = vy + (ay1 + 2*ay2 + 2*ay3 + ay4) * dt / 6
    
    return np.array([x_nuevo, y_nuevo, vx_nuevo, vy_nuevo])

# Almacenamiento de trayectorias
trayectoria_asteroide = np.zeros((pasos+1, 2))
trayectoria_proyectil = np.zeros((pasos+1, 2))
trayectoria_asteroide[0] = estado_asteroide[:2]
trayectoria_proyectil[0] = estado_proyectil[:2]

# Simulación
impacto = False
for i in range(pasos):
    estado_asteroide = paso_rk4(estado_asteroide, dt)
    trayectoria_asteroide[i+1] = estado_asteroide[:2]
    
    estado_proyectil = paso_rk4(estado_proyectil, dt)
    trayectoria_proyectil[i+1] = estado_proyectil[:2]
    
    distancia = np.linalg.norm(trayectoria_asteroide[i+1] - trayectoria_proyectil[i+1])
    if not impacto and distancia < 100:
        print(f"¡IMPACTO en t = {(i+1)*dt:.1f} s!")
        impacto = True

# Graficar
plt.figure(figsize=(10, 10))
plt.plot(trayectoria_asteroide[:,0], trayectoria_asteroide[:,1], 'g-', label='Asteroide')
plt.plot(trayectoria_proyectil[:,0], trayectoria_proyectil[:,1], 'r--', label='Proyectil')
plt.scatter(R_earth, 0, c='blue', s=100, label='Tierra')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Simulación de Impacto Cinético (RK4)')
plt.legend()
plt.axis('equal')
plt.grid()
plt.show()

# Resultados
print("Posición final asteroide:", trayectoria_asteroide[-1])
print("Posición final proyectil:", trayectoria_proyectil[-1])
print("Distancia final:", np.linalg.norm(trayectoria_asteroide[-1] - trayectoria_proyectil[-1]), "m")