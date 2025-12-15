# Limitations & Future Outlook

## Electronic Correlation (GGA vs GGA+U)
- **Limitation:** Standard PBE (GGA) was used. In WTe$_2$, this overestimates the $p$-$d$ band overlap (semimetallic behavior).
- **Impact:** The topological gap is qualitatively correct ($Z_2=1$) but the magnitude is likely underestimated compared to hybrid functional (HSE06) results.

## Dimensionality & Coulomb Cutoff
- **Limitation:** A standard 3D periodic solver was used with high vacuum (~17.6 Å).
- **Refinement:** We did not employ a 2D Coulomb cutoff (e.g., `assume_isolated='2D'`). Long-range van der Waals interactions between periodic images are assumed negligible but not explicitly truncated.

## Finite-Temperature Stability
- **Limitation:** Calculations correspond to $T=0$ K.
- **Outlook:** The topological protection is robust, but phonon stability and electron-phonon scattering at room temperature were not simulated.
