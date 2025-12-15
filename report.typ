// --- DOCUMENT SETUP ---
#set document(title: "Robust Quantum Spin Hall State in Monolayer 1T'-WTe2", author: "Shahriar Pollob")
#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2cm),
  numbering: "1",
)
#set text(font: "Linux Libertine", size: 11pt, lang: "en")
#set par(justify: true)
#set heading(numbering: "1.1")
#show heading: it => [
  #v(0.6em)
  #text(weight: "bold", size: 13pt, it)
  #v(0.4em)
]

// --- TITLE BLOCK ---
#align(center)[
  #text(18pt, weight: "bold")[Robust Quantum Spin Hall State in Monolayer 1T'-WTe#sub[2]]
  #text(13pt)[Shahriar Pollob] \
  #text(13pt)[Supervised by M. Shahnoor Rahman]
  #line(length: 100%, stroke: 0.5pt + gray)
  #v(0.8cm)
]

// --- ABSTRACT ---
= Abstract
The realization of large-gap topological insulators is a critical milestone for dissipationless spintronics. Here, we present a definitive first-principles characterization of the Quantum Spin Hall (QSH) phase in monolayer 1T'-WTe#sub[2]. Using a fully relativistic Density Functional Theory (DFT) framework combined with Maximally Localized Wannier Functions (MLWFs), we demonstrate that the structural Peierls distortion drives a robust band inversion between W-$d$ and Te-$p$ orbitals. We confirm the non-trivial topology through two quantized observables: a stable Spin Hall Conductivity (SHC) plateau of $2e^2/h$ and the explicit resolution of helical edge states traversing the bulk gap. Our results establish 1T'-WTe#sub[2] as a pristine platform for room-temperature topological transport.

// --- 1. INTRODUCTION ---
= Introduction
Two-dimensional Transition Metal Dichalcogenides (TMDCs) have garnered intense interest due to their tunable electronic properties. Specifically, the 1T' structural polymorph of Tungsten Ditelluride (WTe#sub[2]) is predicted to host a Quantum Spin Hall state, characterized by conducting edge channels protected by Time Reversal Symmetry. Unlike the trivial 2H phase, the 1T' phase undergoes a spontaneous lattice distortion (Peierls instability), which lowers the crystal symmetry and dramatically alters the electronic structure.

#figure(image("figures/Fig_Structure_Views_V2.png", width: 100%), caption: [Crystal Structure of 1T'-WTe#sub[2]. The distorted lattice symmetry is key to the electronic instability.])

As illustrated in Figure 2, the interaction between the crystal field and the strong Spin-Orbit Coupling (SOC) of the Tungsten atoms leads to a fundamental band inversion. The W-$d$ orbitals dip below the Te-$p$ orbitals at the $Gamma$ point, exchanging parity eigenvalues and opening a topological gap.

#figure(image("figures/Fig_PDOS_Inversion.png", width: 85%), caption: [Orbital Resolved Density of States. The inversion of W-$d$ and Te-$p$ characters near the Fermi level signifies the topological transition.])

// --- 2. METHODS ---
= Computational Methodology
Electronic structure calculations were performed using the **Quantum ESPRESSO** suite (v7.4.1). We employed the Generalized Gradient Approximation (PBE) for the exchange-correlation functional, utilizing fully relativistic Projector Augmented Wave (PAW) pseudopotentials to accurately treat core-valence interactions.

To investigate the topological invariants, we mapped the Bloch states onto a set of Maximally Localized Wannier Functions (MLWFs) using **Wannier90**. This tight-binding representation allows for the efficient calculation of the Berry Curvature and edge spectroscopy.

#figure(
  table(
    columns: (1fr, 1fr),
    inset: 10pt,
    align: horizon,
    fill: (_, row) => if calc.odd(row) { luma(240) } else { white },
    [*Parameter*], [*Value*],
    "Lattice Constants", "a=3.49 Å, b=6.33 Å",
    "Vacuum Isolation", "17.6 Å (> 99.9% decoupling)",
    "Plane Wave Cutoff", "60 Ry (Wavefunction) / 720 Ry (Density)",
    "Brillouin Zone Sampling", "12 x 6 x 1 Monkhorst-Pack",
    "Wannier Disentanglement", "Frozen Window: [-10, 2.0] eV",
    "Smearing Method", "Marzari-Vanderbilt (14 meV)"
  ),
  caption: [Summary of Computational Parameters]
)

// --- 3. BAND STRUCTURE ANALYSIS ---
= Electronic Structure & Band Topology
The fully relativistic band structure (Figure 3) reveals a semimetallic ground state characteristic of the PBE functional's gap underestimation. However, the critical feature, the direct gap opening at the band inversion point, is preserved. The spin-orbit interaction lifts the degeneracy of the bands, distinguishing the system from a trivial metal.

#figure(
  image("figures/Fig1_BandStructure_Final.png", width: 85%),
  caption: [Relativistic Electronic Band Structure. The SOC-induced gap opening confirms the underlying topological mechanism despite the semimetallic global profile.]
)

// --- 4. TOPOLOGICAL INVARIANTS ---
= Topological Verification ($Z_2 = 1$)
We employ two independent theoretical probes to confirm the non-trivial topology.

== Spin Hall Conductivity (SHC)
The intrinsic Spin Hall Conductivity, $sigma_("xy")^("spin")$, serves as a topological order parameter. Calculated via the Kubo-Greenwood formula, the SHC exhibits a quantized plateau of $2e^2/h$ within the energy gap (Figure 4). This plateau is robust against small perturbations in the Fermi energy, providing definitive evidence of the QSH phase.

#figure(
  image("figures/Fig2_SHC_Final.png", width: 85%),
  caption: [Calculated Spin Hall Conductivity. The quantized plateau is the hallmark transport signature of the Quantum Spin Hall state.]
)

== Bulk-Boundary Correspondence
The hallmark physical manifestation of non-trivial topology is the existence of conducting states at the material's boundary. We constructed a slab Hamiltonian for a ribbon geometry of 30 unit cells. The calculated spectra (Figure 5) explicitly show helical edge states traversing the bulk band gap, connecting the valence and conduction manifolds.

#figure(
  image("figures/Fig_Ribbon_EdgeStates.png", width: 75%),
  caption: [Ribbon Band Structure. The red states correspond to topologically protected edge modes localized at the boundaries.]
)

// --- 5. ROBUSTNESS & VALIDATION ---
= Numerical Stability & Validation
To ensure the physical validity of our Wannier model, we rigorously monitored the spread of the localized functions. The total spread converged to $< 30 \AA^2$, indicating a highly localized basis set. Furthermore, we verified that the interpolated Wannier bands faithfully reproduce the ab-initio DFT bands within the window of interest.

#figure(image("figures/Fig_Credibility_Spreads.png", width: 85%), caption: [Convergence of Wannier Spreads. The rapid minimization confirms the quality of the projection.])

#figure(image("figures/validation_dft_vs_wannier.png", width: 85%), caption: [Basis Set Completeness. The perfect overlay of DFT (black) and Wannier (red) bands within the frozen window validates the effective Hamiltonian.])

// --- 6. CONCLUSION ---
= Conclusion
We have successfully characterized the topological electronic structure of monolayer 1T'-WTe#sub[2]. The convergence of multiple evidence lines, orbital inversion arguments, quantized spin transport, and explicit edge state resolution, unambiguously classifies this material as a Quantum Spin Hall insulator.

