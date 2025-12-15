# Computational Methods

| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Lattice Constants** | $a=3.49$ Å, $b=6.33$ Å, $c=20.00$ Å | Optimized 1T' Monolayer |
| **Vacuum Spacing** | ~17.6 Å | $c_{cell} - (\max z - \min z)$ |
| **Plane Wave Cutoff** | 60 Ry (Wavefn) / 720 Ry (Density) | PBE Solider |
| **K-Point Grid** | $12 \times 6 \times 1$ | Monkhurst-Pack (NSCF) |
| **Smearing** | Marzari-Vanderbilt (0.001 Ry / 14 meV) | Cold Smearing |
| **Bands** | 70 Total (36 Occupied) | Spin-Orbit Coupling included |
| **Wannier Windows** | Outer: $[-15, 40]$ eV<br>Frozen: $[-10, 2]$ eV | Maximal Localization + Topological Fit |
| **Software** | Quantum ESPRESSO v7.4.1<br>Wannier90 v3.1.0 | Fully Relativistic Build |

**Notes:**
- A=3.49, B=6.33, C=20.00
- Vacuum calculated from max extent of W/Te atoms (~2.4A thick).
- Frozen window extended to 2.0 eV for better conduction band fit.
