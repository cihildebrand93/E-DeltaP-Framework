import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Dynamics function (same as before)
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

    if phi == 1:
        D_target = h
    elif phi == -1:
        D_target = -h
    else:
        D_target = D

    dD_dt = alpha * (D_target - D) - beta * abs(D) * np.sign(D)
    dK_dt = -gamma * (K - (0.5 * (1 - abs(D) / h))) + delta * abs(dD_dt)
    epsilon_div = 1e-6
    delta_P = np.log(S + epsilon_div) / (D ** n * K + epsilon_div)
    dP_dt = -kappa * P + lam * delta_P

    return [dD_dt, dK_dt, dP_dt]

# Initial conditions
def initial_conditions_for_radius(r):
    D0 = 0.8 * np.exp(-r / 20)
    K0 = 0.5
    P0 = 1.0 / (r + 1)
    return [D0, K0, P0]

# Simulation parameters
radii = np.linspace(0.1, 50, 50)
phi = 1
t_span = (0, 50)
t_eval = np.linspace(0, 50, 300)

# Run simulation for all shells
all_D = []
all_K = []
all_P = []

for r in radii:
    init_cond = initial_conditions_for_radius(r)
    S = r
    sol = solve_ivp(
        lambda t, y: galaxy_shell_dynamics(t, y, S, phi),
        t_span,
        init_cond,
        t_eval=t_eval
    )
    all_D.append(sol.y[0])
    all_K.append(sol.y[1])
    all_P.append(sol.y[2])

# Convert to arrays: shape (num_shells, num_time_steps)
all_D = np.array(all_D)
all_K = np.array(all_K)
all_P = np.array(all_P)

# Set up the animated plot
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
lines = [axs[i].plot([], [], lw=2)[0] for i in range(3)]
titles = ['Dimensionality D(r)', 'Tension K(r)', 'Pressure P(r)']

for ax, title in zip(axs, titles):
    ax.set_xlim(radii[0], radii[-1])
    ax.set_ylim(0, 1.5)
    ax.set_title(title)
    ax.grid(True)

axs[2].set_xlabel('Radius (kpc)')

# Animation update function
def update(frame):
    lines[0].set_data(radii, all_D[:, frame])
    lines[1].set_data(radii, all_K[:, frame])
    lines[2].set_data(radii, all_P[:, frame])
    return lines

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(t_eval),
    interval=50,
    blit=True
)

plt.tight_layout()
plt.show()
