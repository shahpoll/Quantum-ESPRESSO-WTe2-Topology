import matplotlib.pyplot as plt
import numpy as np

# Load the Spin Hall Conductivity Data
# Col 1: Energy (eV), Col 2: SHC (S/cm)
filename = 'wte2-kubo_S_xy.dat'
try:
    data = np.loadtxt(filename)
except IOError:
    print(f"Error: {filename} not found.")
    exit()

energy = data[:, 0]
# Depending on Wannier90 version, the physical result is often in Col 2 or Col 3.
# Given the A_xy file showed "zero" in Col 3, we will plot BOTH to be safe, 
# but usually Col 2 is the Real part (Conductivity).
shc_col2 = data[:, 1]
shc_col3 = data[:, 2]

plt.figure(figsize=(10, 6))

# Plot Column 2 (Likely the signal)
plt.plot(energy, shc_col2, color='blue', linewidth=2, label='SHC (Col 2)')
# Plot Column 3 (Just in case)
plt.plot(energy, shc_col3, color='red', linestyle='--', alpha=0.5, label='SHC (Col 3)')

plt.axvline(0, color='black', linestyle='-', linewidth=1, label='Fermi Energy')
plt.title("Spin Hall Conductivity (1T'-WTe2)\nSignature of QSH State", fontsize=14)
plt.xlabel("Energy (eV)", fontsize=12)
plt.ylabel("Conductivity (S/cm)", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)
plt.xlim(-2, 2)  # Focus on the relevant window around Fermi level

plt.savefig("final_shc_result.png", dpi=150)
print("Plot saved to final_shc_result.png")
