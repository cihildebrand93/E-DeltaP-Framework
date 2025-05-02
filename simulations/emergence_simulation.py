import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the system of ODEs
def emergence_system(t, y, params):
    D, K, P = y
    alpha, beta, gamma, delta, kappa, lam, h, epsilon, tau, S, n_func, phase, sigma = params

    # Determine phase Φ based on D
    if D > h + epsilon:
        Phi = 1
        D_target = h
    elif D < -h - epsilon:
        Phi = -1
        D_target = -h
    else:
        Phi = 0
        D_target = D  # stay at current D if within boundary

    # Calculate n
    n = n_func(S, D, 0, Phi)  # For simplicity, ignoring dD/dt here

    # ΔP
    # To avoid division by zero, add small epsilon
    epsilon_div = 1e-8
    delta_P = np.log(S + epsilon_div) * (D ** n) * K

    # dD/dt
    # Approximate dD/dt for use in the absolute value term
    # For simplicity, assume previous dD/dt is approximated by finite difference or use last step
    # But since not available here, we approximate using current dD/dt in a small step
    # Alternatively, ignore the damping term or handle differently
    # For simulation, we can ignore the damping term or implement a two-pass approach
    # For now, ignore the damping in the function (or set beta=0)
    dD_dt = alpha * (D_target - D)  # Simplification
    # To include damping, you might need to store previous dD/dt

    # For now, include damping as zero to keep code simple
    # To incorporate damping properly, you'd need a more complex setup

    # dK/dt
    dK_dt = -gamma * (K - K0 * (1 - abs(D)/h)) + delta * abs(dD_dt)

    # dP/dt
    dP_dt = -kappa * P + lam * delta_P

    return [dD_dt, dK_dt, dP_dt]

# Example n function
def n_function(S, D, dD_dt, Phi):
    # Simple example: constant exponent, or a function of phase
    if Phi == 1:
        return 2
    elif Phi == -1:
        return 1
    else:
        return 1.5

# Parameters (tweak as needed)
alpha = 0.5
beta = 0.01
gamma = 0.2
delta = 0.05
kappa = 0.1
lam = 1.0
h = 1.0
epsilon = 0.01
tau = 1.0
S = 1.0
sigma = 0.0  # set >0 for noise

params = [alpha, beta, gamma, delta, kappa, lam, h, epsilon, tau, S, n_function, 0, sigma]

# Initial conditions
D0 = 0.0
K0 = 0.5
P0 = 0.1
y0 = [D0, K0, P0]

# Time span
t_span = [0, 50]
t_eval = np.linspace(t_span[0], t_span[1], 1000)

# Run simulation
sol = solve_ivp(lambda t, y: emergence_system(t, y, params), t_span, y0, t_eval=t_eval, method='RK45')

# Plot results
plt.figure(figsize=(12, 8))
plt.subplot(3,1,1)
plt.plot(sol.t, sol.y[0], label='D(t)')
plt.ylabel('D')
plt.legend()

plt.subplot(3,1,2)
plt.plot(sol.t, sol.y[1], label='K(t)')
plt.ylabel('K')
plt.legend()

plt.subplot(3,1,3)
plt.plot(sol.t, sol.y[2], label='P(t)')
plt.xlabel('Time')
plt.ylabel('P')
plt.legend()

plt.tight_layout()
plt.show()