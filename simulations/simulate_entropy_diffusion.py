import numpy as np
import matplotlib.pyplot as plt

# Parameters
grid_size = 100
timesteps = 300
alpha = 0.05      # D convergence rate
beta = 0.02       # D damping
gamma = 0.03      # K relaxation
delta = 0.015     # K driven by dD
kappa = 0.02      # P dissipation
lambd = 0.07      # ΔP amplification
h = 1.0           # Planck threshold
S = 10            # System scale
n = 2             # Emergence exponent

# Initialize fields
D = np.ones((grid_size, grid_size)) * 0.5
K = np.ones((grid_size, grid_size)) * 0.5
P = np.zeros((grid_size, grid_size))
Phi = np.zeros((grid_size, grid_size), dtype=int)

# Add central spike in pressure
center = (grid_size // 2, grid_size // 2)
P[center] = 10.0
D[center] = 0.1
K[center] = 1.0

def compute_delta_P(D, K, S, n):
    with np.errstate(divide='ignore', invalid='ignore'):
        delta_P = np.where((D != 0) & (K != 0), np.log(S) / (D**n * K), 0)
    delta_P[np.isnan(delta_P)] = 0
    return delta_P

# Simulation loop
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

    # Update Φ field
    Phi[(D > 0.8 * h)] = 1
    Phi[(D < -0.8 * h)] = -1
    Phi[np.abs(D) <= 0.8 * h] = 0

# Plot final pressure field (entropy proxy)
plt.figure(figsize=(6, 5))
plt.imshow(P, cmap='plasma')
plt.title("Figure 12: Recursive Entropy Diffusion in ΔP Field")
plt.colorbar(label='Primal Pressure (P)')
plt.xlabel("X")
plt.ylabel("Y")
plt.tight_layout()
plt.savefig("figure_12_entropy_diffusion.png", dpi=300)
plt.show()
