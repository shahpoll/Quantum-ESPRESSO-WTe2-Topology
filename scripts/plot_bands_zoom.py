import matplotlib.pyplot as plt
import numpy as np

try:
    # Load Wannier90 Band Data
    # wte2_band.dat usually has columns: k (length), energy (eV)
    # The file contains blocks separated by newlines
    data = np.loadtxt('wte2_band.dat')
    k = data[:, 0]
    e = data[:, 1]
    
    fig, ax = plt.subplots(figsize=(7, 9))
    
    # Plot the bands
    # Use small markers to resolve splitting
    ax.scatter(k, e, s=0.2, c='black', alpha=0.7)
    
    # --- VISUALIZATION TUNING ---
    # 1. Zoom in on the "Inversion Window" (-0.5 to +0.5 eV)
    ax.set_ylim(-0.8, 0.8)
    ax.set_xlim(min(k), max(k))
    
    # 2. Add Fermi Level
    ax.axhline(0, color='red', linestyle='--', linewidth=1, label='E_F (0 eV)')
    
    # 3. Annotate the Gap
    # We expect the gap near Gamma (k=0) or along G-X
    ax.text(0.1, 0.1, "Topological Gap", fontsize=10, color='blue', ha='left')
    
    ax.set_ylabel("Energy (eV) - relative to Fermi Level")
    ax.set_xlabel("Momentum Path (G - X - M - G - Y)")
    ax.set_title("1T'-WTe2 Band Structure\n(Showing Spin-Orbit Gap Opening)")
    ax.grid(True, alpha=0.2)
    
    plt.savefig("wte2_band_structure_zoom.png", dpi=300)
    print("Band plot saved as wte2_band_structure_zoom.png")

except Exception as e:
    print(f"Error plotting bands: {e}")
