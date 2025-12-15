import matplotlib.pyplot as plt
import numpy as np
import sys

# --- PLOT 1: BAND STRUCTURE ---
def plot_bands():
    try:
        # Wannier90 band format: Col 2 is Energy
        # The file contains blocks separated by blank lines for each band
        data = np.loadtxt('wte2_band.dat')
        k = data[:, 0]
        e = data[:, 1]
        
        plt.figure(figsize=(6, 8))
        
        # Filter for relevant energy window (-1 to +1 eV) to show Inversion
        plt.scatter(k, e, s=0.5, c='black', alpha=0.6)
        
        plt.ylim(-1.5, 1.5)
        plt.xlim(min(k), max(k))
        plt.axhline(0, color='red', linestyle='--', linewidth=0.8, label='Fermi Level')
        plt.ylabel("Energy (eV)")
        plt.title("Electronic Band Structure\n(Wannier Interpolated)")
        
        # Add labels for High Symmetry Points (Approximate based on 100 pts/segment)
        # G(0) -> X(1.57) -> M(...) 
        # We just label start/end for simplicity in this auto-script
        plt.xticks([])
        plt.xlabel("Wavevector k (G - X - M - G - Y)")
        
        plt.grid(True, alpha=0.2)
        plt.savefig("Figure_1_BandStructure.png", dpi=300)
        print("Generated Figure_1_BandStructure.png")
    except Exception as e:
        print(f"Skipping Bands: {e}")

# --- PLOT 2: SPIN HALL CONDUCTIVITY (The Result) ---
def plot_shc():
    try:
        data = np.loadtxt('wte2-kubo_S_xy.dat')
        energy = data[:, 0]
        shc = data[:, 1] # Col 2 is usually the conductivity
        
        plt.figure(figsize=(8, 6))
        plt.plot(energy, shc, color='#004488', linewidth=2.5)
        
        # Formatting
        plt.axvline(0, color='black', linestyle='-', linewidth=1)
        plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
        plt.fill_between(energy, shc, 0, where=(shc<0), color='#004488', alpha=0.1)
        
        plt.xlim(-1.0, 1.0) # Zoom in on the topological window
        plt.xlabel("Energy (eV)", fontsize=12)
        plt.ylabel(r"Spin Hall Conductivity ($\sigma_{xy}^{spin}$)", fontsize=12)
        plt.title("Spin Hall Conductivity: 1T'-WTe2", fontsize=14)
        plt.grid(True, linestyle=':', alpha=0.5)
        
        plt.savefig("Figure_2_SHC.png", dpi=300)
        print("Generated Figure_2_SHC.png")
    except Exception as e:
        print(f"Skipping SHC: {e}")

# --- PLOT 3: ANOMALOUS HALL (The Validation) ---
def plot_ahc():
    try:
        data = np.loadtxt('wte2-kubo_A_xy.dat')
        energy = data[:, 0]
        ahc = data[:, 1]
        
        plt.figure(figsize=(8, 4))
        plt.plot(energy, ahc, color='green', linewidth=2)
        plt.ylim(-10, 10) # Set a scale to show how small it is
        plt.title("Anomalous Hall Conductivity (Check)", fontsize=14)
        plt.xlabel("Energy (eV)")
        plt.ylabel(r"$\sigma_{xy}^{AHC}$")
        plt.grid(True, alpha=0.3)
        plt.text(0, 5, "Expectation: ~0 (Time Reversal Symmetry)", ha='center')
        
        plt.savefig("Figure_3_AHC_Validation.png", dpi=300)
        print("Generated Figure_3_AHC_Validation.png")
    except Exception as e:
        print(f"Skipping AHC: {e}")

if __name__ == "__main__":
    plot_bands()
    plot_shc()
    plot_ahc()
