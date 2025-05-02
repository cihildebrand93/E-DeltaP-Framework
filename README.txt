# E = ΔP: A Dynamical Framework for Emergent Structure and Time Reversal  
**Author:** Christopher Hildebrand  
**Email:** cihildebrand93@gmail.com  
**Location:** Seattle, Washington, USA

---

##  Overview

This repository accompanies the paper:  
**E = ΔP: A Dynamical Framework for Emergent Structure and Time Reversal**  
located in [`/docs/`](./docs/).

> This framework redefines structure, time, light, quantum behavior, forces, and thermodynamics as emergent from a recursive field interaction—without requiring mass, spacetime curvature, or fundamental particles.  
>  
> All simulation results are generated using ΔP dynamics and match known physical phenomena, including galaxy rotation curves, gravitational lensing, Shapiro delay, entanglement, particle-like formation, and entropy gradients.

---

##  Paper

- **PDF Location:** [`/docs/E = ΔP A Dynamical Framework for Emergent Structure and Time Reversal.pdf`](./docs/)
- **arXiv Link:** _(to be added after submission)_

---

##  Simulation Tools

Scripts used to generate all figures and run experiments are in [`/simulations/`](./simulations/).

| Script                                  | Description                                                      |
|-----------------------------------------|------------------------------------------------------------------|
| `E_DeltaP_GalaxySim.py`                 | Velocity field solver for NGC 3198, Milky Way, and DF2           |
| `galaxy_evolution_animation.py`         | Emergent structure evolution across radial shells                |
| `jacobian_sweep_ngc3198.py`             | Extracts local eigenvalues for field stability                   |
| `generate_phi_array.py`                 | Generates Φ(r) phase-state map                                   |
| `simulate_lensing_deltap.py`            | Light deflection from pressure-tension gradients                 |
| `simulate_entanglement_response.py`     | Recursive phase correlation simulating entanglement              |
| `simulate_particle_emergence.py`        | Soliton-like field stabilization: particle formation             |
| `simulate_force_interface.py`           | Field tension interaction between two particle analogs           |
| `simulate_entropy_diffusion.py`         | Recursive entropy smoothing via pressure decay                   |

---

##  Figures

All output plots and visualizations are located in [`/figures/`](./figures/), numbered to match the main paper.

---

##  Requirements

- Python 3.9+
- Required libraries:
  - `numpy`
  - `matplotlib`
  - `scipy`

Install dependencies:

```bash
pip install numpy matplotlib scipy


 Contact
For collaboration, questions, or peer discussion:
 cihildebrand93@gmail.com
 Seattle, Washington

 License
MIT License — freely usable, forkable, and open for public testing and research.
See LICENSE for full terms.