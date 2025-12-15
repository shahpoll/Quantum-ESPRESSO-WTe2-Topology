import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Conversion factor
BOHR_TO_ANG = 0.529177

def parse_qe_input(filename):
    atoms = []
    cell = []
    
    # Defaults
    pos_unit = 'alat'
    cell_unit = 'alat' # Not strictly used if we just read the lines
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    # 1. Parse Cell
    for i, line in enumerate(lines):
        if "CELL_PARAMETERS" in line:
            if "bohr" in line.lower():
                cell_scale = BOHR_TO_ANG
            elif "angstrom" in line.lower():
                cell_scale = 1.0
            else:
                cell_scale = 1.0 # Default/ALAT warning
                
            # Read next 3 lines
            v1 = [float(x) for x in lines[i+1].split()]
            v2 = [float(x) for x in lines[i+2].split()]
            v3 = [float(x) for x in lines[i+3].split()]
            cell = np.array([v1, v2, v3]) * cell_scale
            break
            
    # 2. Parse Atoms
    in_atoms = False
    atom_scale = 1.0
    
    for line in lines:
        if "ATOMIC_POSITIONS" in line:
            in_atoms = True
            if "bohr" in line.lower():
                atom_scale = BOHR_TO_ANG
            elif "angstrom" in line.lower():
                atom_scale = 1.0
            elif "crystal" in line.lower():
                atom_scale = 'crystal'
            continue
            
        if in_atoms:
            if line.strip() == "" or "K_POINTS" in line:
                break
            parts = line.split()
            if len(parts) >= 4:
                species = parts[0]
                coords = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
                
                if atom_scale == 'crystal':
                    # Convert fractional to cartesian using cell vectors
                    # Cart = v1*f1 + v2*f2 + v3*f3
                    # Our cell matrix rows are vectors? Usually.
                    # r = f1*a1 + f2*a2 + f3*a3
                    # cell[0] = a1 vector
                    cart_coords = coords[0]*cell[0] + coords[1]*cell[1] + coords[2]*cell[2]
                    atoms.append({'s': species, 'pos': cart_coords})
                else:
                    atoms.append({'s': species, 'pos': coords * atom_scale})

    return cell, atoms

# --- EXECUTION ---
try:
    cell, atoms = parse_qe_input('wte2.scf.in')
    print(f"Parsed Cell (Angstroms):\n{cell}")
    print(f"Dimensions: a={np.linalg.norm(cell[0]):.2f}, b={np.linalg.norm(cell[1]):.2f}, c={np.linalg.norm(cell[2]):.2f}")
except Exception as e:
    print(f"Parsing Error: {e}")
    exit()

fig = plt.figure(figsize=(10, 5))

# --- SUBPLOT 1: TOP VIEW (a-b projected) ---
ax1 = fig.add_subplot(1, 2, 1)
# Project onto XY (assuming a along x, b along y roughly)
# Orthorhombic check:
# If cell is 6.6 0 0 bohr -> a is x.
# 0 11.96 0 -> b is y.
# 0 0 37.79 -> c is z.
# So just plotting x vs y is fine.

for atom in atoms:
    color = 'royalblue' if atom['s'] == 'W' else 'gold'
    size = 150 if atom['s'] == 'W' else 80
    zorder = 10 if atom['s'] == 'W' else 5
    
    # Original
    x, y, z = atom['pos']
    ax1.scatter(x, y, c=color, s=size, edgecolors='black', zorder=zorder)
    
    # 2x2 Supercell phantom atoms for connectivity
    # Add +/- a and +/- b
    shifts = [[1,0,0], [0,1,0], [1,1,0]]
    for s in shifts:
        s_vec = s[0]*cell[0] + s[1]*cell[1] + s[2]*cell[2]
        new_pos = atom['pos'] + s_vec
        ax1.scatter(new_pos[0], new_pos[1], c=color, s=size, edgecolors='black', alpha=0.3, zorder=zorder-1)

# Highlight Zigzag?
# W chains run along a (x-axis). 
# Distances alternate.
ax1.set_aspect('equal')
ax1.set_title("Top View (a-b plane)")
ax1.set_xlabel("x [Å]")
ax1.set_ylabel("y [Å]")
# Set limits to fit 1.5 unit cells
ax1.set_xlim(-1, np.linalg.norm(cell[0])*2)
ax1.set_ylim(-1, np.linalg.norm(cell[1])*2)

# --- SUBPLOT 2: SIDE VIEW (y-z projected) ---
# To see layers and vacuum
ax2 = fig.add_subplot(1, 2, 2)
for atom in atoms:
    color = 'royalblue' if atom['s'] == 'W' else 'gold'
    size = 150 if atom['s'] == 'W' else 80
    x, y, z = atom['pos']
    
    # We plot y vs z (Side view looking down a-axis)
    # Or x vs z.
    # User said "Side View: b-c plane", so y vs z.
    ax2.scatter(y, z, c=color, s=size, edgecolors='black')
    
    # Periodic image in z? No, we want to see vacuum.
    # Periodic image in y (b-axis) to show layer extent
    ax2.scatter(y + np.linalg.norm(cell[1]), z, c=color, s=size, edgecolors='black', alpha=0.3)

# Draw cell box in Z
c_len = np.linalg.norm(cell[2])
ax2.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax2.axhline(c_len, color='gray', linestyle='--', alpha=0.5)
ax2.text(1, c_len/2, "Vacuum Gap", ha='center', va='center', rotation=90)

ax2.set_aspect('equal')
ax2.set_title(f"Side View (c = {c_len:.1f} Å)")
ax2.set_xlabel("y [Å]")
ax2.set_ylabel("z [Å]")
ax2.set_ylim(-1, c_len + 1)

plt.tight_layout()
plt.savefig("Fig_Structure_Views_V2.png", dpi=150)
print("Saved Fig_Structure_Views_V2.png")
