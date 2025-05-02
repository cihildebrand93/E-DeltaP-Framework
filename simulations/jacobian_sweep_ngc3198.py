import numpy as np
from numpy.linalg import eigvals
import matplotlib.pyplot as plt

# ===============================
# 1. Dummy Galaxy Simulation Data
# ===============================

# Simulate radius from 0 to 50 kpc
r = np.linspace(0, 50, 100)

# Simulated field values across radius
D_vals = 0.8 - 0.01 * r          # Dimensionality slowly decays
K_vals = 0.1 + 0.005 * r         # Tension increases (halo tension)
P_vals = 1.0 + 0.02 * r          # Pressure rises outward
S_vals = 10 + r                  # Log-scale factor S(r)

# ===============================
# 2. ΔP Jacobian Matrix Function
# ===============================

def get_jacobian(D, K, P, alpha, gamma, kappa, lambd, n, S, h):
    if D == 0 or K == 0:
        return np.zeros((3, 3))

    dΔP_dD = -n * np.log(S) / (D**(n+1) * K)
    dΔP_dK = -np.log(S) / (D**n * K**2)

    dD_dD = -alpha
    dK_dD = gamma * np.sign(D) / h
    dK_dK = -gamma
    dP_dD = lambd * dΔP_dD
    dP_dK = lambd * dΔP_dK

    return np.array([
        [dD_dD, 0, 0],
        [dK_dD, dK_dK, 0],
        [dP_dD, dP_dK, -kappa]
    ])

# ===============================
# 3. Simulation Constants
# ===============================

alpha = 0.1
gamma = 0.1
kappa = 0.1
lambd = 0.1
n = 2
h = 1.0

# ===============================
# 4. Choose Radius Samples
# ===============================

sample_indices = [5, 15, 25, 35, 45]
eigenvalues = []

# ===============================
# 5. Run Jacobian Sweep
# ===============================

for i in sample_indices:
    D = D_vals[i]
    K = K_vals[i]
    P = P_vals[i]
    S = S_vals[i]

    J = get_jacobian(D, K, P, alpha, gamma, kappa, lambd, n, S, h)
    λ = eigvals(J)
    eigenvalues.append(λ)
    print(f"Radius {r[i]:.2f} kpc → Eigenvalues: {λ}")

# ===============================
# 6. Plot Real and Imaginary Parts
# ===============================

r_plot = [r[i] for i in sample_indices]
real_parts = [[eig.real for eig in lam] for lam in eigenvalues]
imag_parts = [[eig.imag for eig in lam] for lam in eigenvalues]

# Real parts plot
plt.figure(figsize=(10, 5))
for j in range(3):
    plt.plot(r_plot, [real_parts[i][j] for i in range(len(real_parts))], label=f"Re(λ{j+1})")
plt.xlabel("Radius (kpc)")
plt.ylabel("Real(λ)")
plt.title("Jacobian Real Parts Across Radius")
plt.grid()
plt.legend()
plt.show()

# Imaginary parts plot
plt.figure(figsize=(10, 5))
for j in range(3):
    plt.plot(r_plot, [imag_parts[i][j] for i in range(len(imag_parts))], label=f"Im(λ{j+1})")
plt.xlabel("Radius (kpc)")
plt.ylabel("Imag(λ)")
plt.title("Jacobian Imaginary Parts Across Radius")
plt.grid()
plt.legend()
plt.show()
