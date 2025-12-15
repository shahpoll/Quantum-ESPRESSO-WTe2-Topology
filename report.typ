// --- DOCUMENT SETUP ---
#set document(title: "1T'-WTe2 Topological Characterization", author: "Shahriar Pollob")
#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2cm),
  numbering: "1",
)
#set text(font: "Linux Libertine", size: 11pt)
#set heading(numbering: "1.1")

// --- TITLE ---
#align(center)[
  #text(17pt, weight: "bold")[Topological Characterization of Monolayer 1T'-WTe#sub[2]]
  #v(0.5em)
  #text(12pt)[Shahriar Pollob (Supervised by M. Shahnoor Rahman)] \
  #text(10pt, style: "italic")[Generated via Quantum ESPRESSO & Wannier90 Workflow]
  #v(1cm)
]

// --- ABSTRACT ---
= Abstract
We present a complete computational characterization of the Quantum Spin Hall (QSH) phase in monolayer 1T'-WTe#sub[2]. Utilizing a fully relativistic PBE+SOC framework, we demonstrate the robustness of the $Z_2=1$ topological invariant through two complementary observables: the quantized Spin Hall Conductivity (SHC) and the existence of helical edge states in a ribbon geometry.

// --- 1. METHODS ---
= Computational Methods
The electronic structure was calculated using Quantum ESPRESSO (v7.4.1) with fully relativistic Projector Augmented Wave (PAW) pseudopotentials. 

#figure(
  table(
    columns: (auto, auto),
    inset: 10pt,
    align: horizon,
    [*Parameter*], [*Value*],
    "Lattice Constants", "a=3.49 Å, b=6.33 Å",
    "Vacuum Spacing", "~17.6 Å",
    "Plane Wave Cutoff", "60 Ry (Wfc) / 720 Ry (Rho)",
    "K-Mesh (NSCF)", "12 x 6 x 1",
    "Wannier Window", "Frozen: [-10, 2.0] eV",
    "Smearing", "Marzari-Vanderbilt (14 meV)"
  ),
  caption: [Simulation Parameters]
)

// --- 2. ELECTRONIC STRUCTURE ---
= Electronic Structure & Topology
The 1T' phase exhibits a Peierls distortion that breaks the high symmetry of the 1T phase. 

#grid(
  columns: (1fr, 1fr),
  gutter: 10pt,
  figure(image("figures/Fig_Structure_Views_V2.png", width: 100%), caption: [Crystal Structure (Distorted 1T')]),
  figure(image("figures/Fig_PDOS_Inversion.png", width: 100%), caption: [Orbital Inversion (p-d mixing)])
)

The inclusion of Spin-Orbit Coupling (SOC) opens a fundamental gap at the inversion point, although the PBE functional yields a semimetallic overlap globally.

#figure(
  image("figures/Fig1_BandStructure_Final.png", width: 80%),
  caption: [Relativistic Band Structure showing the inverted gap.]
)

// --- 3. TOPOLOGICAL PROOF ---
= Topological Invariant ($Z_2 = 1$)
We verify the non-trivial topology via two methods:

== 3.1 Spin Hall Conductivity
The Spin Hall Conductivity $sigma_("xy")^("spin")$ exhibits a quantized plateau within the bulk gap, a hallmark of the QSH state.

#figure(
  image("figures/Fig2_SHC_Final.png", width: 80%),
  caption: [Spin Hall Conductivity Plateau.]
)

== 3.2 Bulk-Boundary Correspondence (Ribbon)
A tight-binding calculation on a 30-unit-cell ribbon reveals gapless edge states connecting the valence and conduction bands.

#figure(
  image("figures/Fig_Ribbon_EdgeStates.png", width: 70%),
  caption: [Helical Edge States traversing the bulk gap.]
)

// --- 4. VALIDATION ---
= Validation & Reproducibility
The Wannier tight-binding model was validated against DFT ground truth. The spread convergence confirms maximally localized functions.

#grid(
  columns: (1fr, 1fr),
  gutter: 10pt,
  figure(image("figures/Fig_Credibility_Spreads.png", width: 100%), caption: [Wannier Spread Convergence]),
  figure(image("figures/Fig_Workflow.png", width: 100%), caption: [Reproducible Workflow])
)
