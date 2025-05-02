import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
grid_size = 100
timesteps = 300
alpha = 0.05
beta = 0.02
gamma = 0.04
delta = 0.015
kappa = 0.03
lambd = 0.08
h = 1.0
S = 10
n = 2

# Initialize fields
D = np.zeros((grid_size, grid_size))
K = np.ones((grid_size, grid_size)) * 0.5
P = np.ones((grid_size, grid_size)) * 0.1
Phi = np.zeros((grid_size, grid_size), dtype=int)

# Initialize two particle analogs
center_1 = (30, 50)
center_2 = (70, 50)
D[center_1] = h * 0.9
D[center_2] = -h * 0.9
K[center_1] = 1.2
K[center_2] = 1.2
Phi[center_1] = 1
Phi[center_2] = -1

frames = []

def compute_delta_P(D, K, S, n):
    with np.errstate(divide='ignore', invalid='ignore'):
        delta_P = np.where((D != 0) & (K != 0), np.log(S) / (D**n * K), 0)
    delta_P[np.isnan(delta_P)] = 0
    return delta_P

for t in range(timesteps):
    D_target = np.where(Phi == 1, h,
                 np.where(Phi == -1, -h, D))

    dD_dt = alpha * (D_target - D) - beta * np.abs(D) * np.sign(D)
    D += dD_dt

    dK_dt = -gamma * (K - (1 - np.abs(D)/h)) + delta * np.abs(dD_dt)
    K += dK_dt

    delta_P = compute_delta_P(D, K, S, n)
    dP_dt = -kappa * P + lambd * delta_P
    P += dP_dt

    # Update Phi
    Phi[(D > 0.8 * h)] = 1
    Phi[(D < -0.8 * h)] = -1
    Phi[np.abs(D) <= 0.8 * h] = 0

    if t % 10 == 0:
        frames.append(K.copy())  # Save tension field

# Plot final tension map (ΔK interaction)
plt.figure(figsize=(6, 5))
plt.title("Figure 11: Recursive Tension Field Between ΔP Particle Analogs")
plt.imshow(K, cmap='viridis')
plt.colorbar(label='Dimensional Tension (K)')
plt.xlabel("X")
plt.ylabel("Y")
plt.tight_layout()
plt.show()

# Optional animation export (uncomment to save)
# fig, ax = plt.subplots()
# im = ax.imshow(frames[0], cmap='viridis', vmin=np.min(K), vmax=np.max(K))
# def update(frame):
#     im.set_array(frame)
#     return [im]
# ani = FuncAnimation(fig, update, frames=frames, interval=60)
# ani.save("force_field_interaction.gif", writer="pillow")
