import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
grid_size = 100
timesteps = 200
alpha = 0.05
beta = 0.02
gamma = 0.05
delta = 0.02
kappa = 0.05
lambd = 0.1
h = 1.0
S = 10
n = 2

# Initialize fields
D = np.random.uniform(-0.1, 0.1, (grid_size, grid_size))
K = np.ones((grid_size, grid_size)) * 0.5
P = np.ones((grid_size, grid_size)) * 0.1
Phi = np.zeros((grid_size, grid_size), dtype=int)

# Storage for plotting
frames = []

# Time evolution
for t in range(timesteps):
    D_target = np.where(Phi == 1, h,
                 np.where(Phi == -1, -h, D))

    dD_dt = alpha * (D_target - D) - beta * np.abs(D) * np.sign(D)
    D += dD_dt

    dK_dt = -gamma * (K - (1 - np.abs(D)/h)) + delta * np.abs(dD_dt)
    K += dK_dt

    delta_P = np.where(D != 0, np.log(S) / (D**n * K), 0)
    dP_dt = -kappa * P + lambd * delta_P
    P += dP_dt

    # Optional noise injection every 50 steps
    if t % 50 == 0:
        D += np.random.normal(0, 0.01, D.shape)

    # Update Phi phase
    Phi[(D > 0.8 * h)] = 1
    Phi[(D < -0.8 * h)] = -1
    Phi[(np.abs(D) <= 0.8 * h)] = 0

    if t % 10 == 0:
        frames.append(P.copy())

# Plot last frame as heatmap
plt.figure(figsize=(6, 5))
plt.title("Figure 10: Heatmap of Stable Collapse Regions (ΔP Particle Analogs)")
plt.imshow(P, cmap='inferno')
plt.colorbar(label='Primal Pressure (P)')
plt.xlabel("X")
plt.ylabel("Y")
plt.tight_layout()
plt.show()

# Optional: Save animation (uncomment to export)
# fig, ax = plt.subplots()
# im = ax.imshow(frames[0], cmap='inferno', vmin=np.min(P), vmax=np.max(P))
# def update(frame):
#     im.set_array(frame)
#     return [im]
# ani = FuncAnimation(fig, update, frames=frames, interval=50)
# ani.save("particle_emergence.gif", writer="pillow")
