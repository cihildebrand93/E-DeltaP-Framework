import numpy as np

# ======================================
# 1. Define Galaxy Radius (kpc)
# ======================================

# Simulate 100 points from 0 to 50 kpc
r_vals = np.linspace(0, 50, 100)

# ======================================
# 2. Define Phase Zones Based on Radius
# ======================================

# Φ = +1 for emergence core (< 8 kpc)
# Φ =  0 for stable disk (< 25 kpc)
# Φ = –1 for collapse halo (>= 25 kpc)

Φ_vals = []
for r in r_vals:
    if r < 8:
        Φ_vals.append(1)
    elif r < 25:
        Φ_vals.append(0)
    else:
        Φ_vals.append(-1)

Φ_vals = np.array(Φ_vals)

# ======================================
# 3. Output Array
# ======================================

# Print first few values
print("Φ(r) phase states:")
print(Φ_vals[:10], "...")

# Save to file for visualization later
np.savetxt("phi_vals.txt", Φ_vals, fmt='%d')

print("Φ(r) array saved to: phi_vals.txt")
