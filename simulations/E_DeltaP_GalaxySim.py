import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# E = ΔP dynamics for a single shell
def galaxy_shell_dynamics(t, y, S, phi):
    D, K, P = y
    h = 1.0
    n = 2
    alpha = 0.1
    beta = 0.05
    gamma = 0.02
    delta = 0.01
    kappa = 0.05
    lam = 0.02

    # Determine phase target for dimensionality
    if phi == 1:
        D_target = h
    elif phi == -1:
        D_target = -h
    else:
        D_target = D

    dD_dt = alpha * (D_target - D) - beta * abs(D) * np.sign(D)
    dK_dt = -gamma * (K - (0.5 * (1 - abs(D) / h))) + delta * abs(dD_dt)
    
    # Avoid division by zero
    epsilon_div = 1e-6
    delta_P = np.log(S + epsilon_div) / (D ** n * K + epsilon_div)
    
    dP_dt = -kappa * P + lam * delta_P

    return [dD_dt, dK_dt, dP_dt]

# Initial condition generator per shell
def initial_conditions_for_radius(r):
    D0 = 0.8 * np.exp(-r / 20)  # D falls with distance
    K0 = 0.5                    # Constant tension start
    P0 = 1.0 / (r + 1)          # Pressure higher in core
    return [D0, K0, P0]

# Set up 50 galactic shells from 0.1 to 50 kpc
radii = np.linspace(0.1, 50, 50)
phi = 1  # All shells in emergence phase for now

all_results = []

# Run simulation for each shell
for r in radii:
    init_cond = initial_conditions_for_radius(r)
    S = r  # Use radius as scale
    sol = solve_ivp(
        lambda t, y: galaxy_shell_dynamics(t, y, S, phi),
        [0, 50],
        init_cond,
        t_eval=np.linspace(0, 50, 300)
    )
    all_results.append({
        'radius': r,
        'time': sol.t,
        'D': sol.y[0],
        'K': sol.y[1],
        'P': sol.y[2]
    })

# Plot D, K, P at final time step for all shells
D_final = [res['D'][-1] for res in all_results]
K_final = [res['K'][-1] for res in all_results]
P_final = [res['P'][-1] for res in all_results]

plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(radii, D_final, label='D (dimensionality)')
plt.ylabel('D at t=50')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(radii, K_final, label='K (tension)')
plt.ylabel('K at t=50')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(radii, P_final, label='P (pressure)')
plt.xlabel('Radius (kpc)')
plt.ylabel('P at t=50')
plt.legend()

plt.tight_layout()
plt.show()
