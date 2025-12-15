import matplotlib.pyplot as plt
import numpy as np
import os

# --- CONFIGURATION ---
filename = 'wte2_wilson.dat'  # Trying standard name
if not os.path.exists(filename):
    filename = 'wte2_wcc.dat' # Fallback

if not os.path.exists(filename):
    print(f"Error: Could not find {filename} or wte2_wcc.dat. Check 'ls' output.")
    exit()

print(f"Reading {filename}...")
data = np.loadtxt(filename)

# Wilson Loop data is typically: k_point (x), WCC (y)
k = data[:, 0]
wcc_cols = data.shape[1] - 1

plt.figure(figsize=(8, 6))
# Plot points
for i in range(1, wcc_cols + 1):
    plt.scatter(k, data[:, i], s=1, c='blue', alpha=0.5)

plt.title("Wilson Loop (Wannier Charge Centers) - 1T'-WTe2")
plt.xlabel("Momentum k (along loop)")
plt.ylabel("Wannier Charge Center (Phase / 2pi)")
plt.ylim(0, 1)
plt.grid(True, linestyle='--', alpha=0.3)

plt.savefig("z2_wilson_loop.png", dpi=300)
print("Plot saved as z2_wilson_loop.png")
