import matplotlib.pyplot as plt
import numpy as np
import os

# --- STYLE SETTINGS (MATCHING 1T' SCRIPT) ---
params = {
    'figure.figsize': (10, 8),
    'font.family': 'sans-serif',
    'font.weight': 'bold',
    'font.size': 16,
    'axes.labelsize': 18,
    'lines.linewidth': 2,
}
plt.rcParams.update(params)

def plot_1T_3d():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # --- 1T GEOMETRY (Ideal Octahedral) ---
    # a = b approx 3.5 A
    a_lat = 3.52 
    
    # Hexagonal Lattice Vectors
    # a1 = (a, 0, 0)
    # a2 = (-a/2, a*sqrt(3)/2, 0)
    a1 = np.array([a_lat, 0, 0])
    a2 = np.array([-a_lat/2, a_lat * np.sqrt(3)/2, 0])
    c_vec = np.array([0, 0, 15.0]) # Vacuum
    
    # Atomic Basis (Monolayer 1T)
    # W at (0,0,0)
    # Te at (1/3, 2/3, z) and (2/3, 1/3, -z)
    z_te = 1.6 # Approx height
    
    coords = []
    species = []
    
    # Create Strip of Lattice to match 1T' flow
    # 1T' has atoms flowing roughly along Y (and slightly X due to skew)
    # We want a "Ribbon" that contains the Red Box and extends up/right.
    # Red Box is at i=0, j=0 (relative to our chosen origin).
    # so we need i around 0, and j extending -1 to +3 or so.
    
    nx_range = range(-1, 2) # Narrow in X (just neighbors)
    ny_range = range(-1, 4) # Long in Y (Flow direction)
    
    for i in nx_range:
        for j in ny_range:
            # Origin of cell
            origin = i*a1 + j*a2
            
            w_pos = origin
            coords.append(w_pos)
            species.append('W')
            
            te1_pos = origin + (1.0/3.0)*a1 + (2.0/3.0)*a2 + np.array([0, 0, z_te])
            coords.append(te1_pos)
            species.append('Te')
            
            te2_pos = origin + (2.0/3.0)*a1 + (1.0/3.0)*a2 + np.array([0, 0, -z_te])
            coords.append(te2_pos)
            species.append('Te')
            
    coords = np.array(coords)
    
    # --- DEFINE RECTANGULAR CELL (Match 1T') ---
    u_rect = a1
    v_rect = a1 + 2*a2
    
    # We need to pick a "Reference Origin" for the lattice to define the box.
    # We want the box to be on the "central" atoms of our strip.
    # Let's pick i=0, j=0.
    ref_origin = np.array([0., 0., 0.])
    
    x_limit = np.linalg.norm(u_rect) 
    y_limit = np.linalg.norm(v_rect)
    
    primary_indices = []
    
    for idx, (x, y, z) in enumerate(coords):
        # Relative pos
        rx = x - ref_origin[0]
        ry = y - ref_origin[1]
        
        tol = 0.1
        # Check geometric inclusion in the Rectangular Box at (0,0)
        if (-tol <= rx <= x_limit + tol) and (-tol <= ry <= y_limit + tol):
            primary_indices.append(idx)
            
    # --- COORDINATE ALIGNMENT ---
    # Calculate Centroid of these Primary Atoms
    primary_atom_coords = coords[primary_indices]
    current_centroid = np.mean(primary_atom_coords, axis=0)
    
    # Target Centroid (from 1T' Debug)
    target_primary_centroid = np.array([1.745, 4.706, 10.16])
    
    shift = target_primary_centroid - current_centroid
    coords += shift
    
    # Apply shift to reference origin too (for drawing box)
    box_origin = ref_origin + shift
    # Project box origin Z to mean Z
    box_origin[2] = np.mean(coords[:, 2])

    
    # --- PLOTTING ---
    
    # Plot Atoms
    # Re-extract shifted columns for plotting
    xs = coords[:, 0]
    ys = coords[:, 1]
    zs = coords[:, 2]
    
    for idx, (x, y, z) in enumerate(coords):
        is_primary = (idx in primary_indices)

        atom = species[idx]
        if atom == 'W':
            base_color = '#2c3e50'
        else:
            base_color = '#f39c12'
            
        if is_primary:
            color = base_color
            alpha = 1.0
            edgecolor = 'black'
        else:
            if atom == 'W': color = '#bdc3c7'
            else: color = '#fcd088'
            alpha = 0.8
            edgecolor = 'gray'
            
        size = 400 if atom == 'W' else 300
        zorder = 10 if atom == 'W' else 9
            
        ax.scatter(x, y, z, s=size, c=color, edgecolors=edgecolor, alpha=1.0, zorder=zorder)
        
    # Plot Bonds
    # 1T Coordination: Each W connected to 6 Te (3 top, 3 bottom)
    # Cutoff distance
    bond_cutoff = 3.0
    
    # Iterate over W atoms and find Te neighbors
    w_indices = [k for k, s in enumerate(species) if s == 'W']
    te_indices = [k for k, s in enumerate(species) if s == 'Te']
    
    for i in w_indices:
        p1 = coords[i]
        for j in te_indices:
            p2 = coords[j]
            dist = np.linalg.norm(p1 - p2)
            if dist < bond_cutoff:
                # 1T Bonds are all identical (gray)
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                       color='gray', alpha=0.4, linewidth=2)

    # Unit Cell Box (Rectangular 1T' shape)
    uc_corners = [
        box_origin,
        box_origin + u_rect,
        box_origin + u_rect + v_rect,
        box_origin + v_rect,
        box_origin
    ]
    uc_x = [p[0] for p in uc_corners]
    uc_y = [p[1] for p in uc_corners]
    uc_z = [p[2] for p in uc_corners]
    ax.plot(uc_x, uc_y, uc_z, color='red', linestyle='--', linewidth=2, label='Unit Cell')

    # --- CAMERA & LIMITS (EXACT 1T' MATCH) ---
    ax.view_init(elev=30, azim=-60)
    
    # Hardcoded Dimensions from Debug
    ax.set_xlim(-0.1, 5.75)
    ax.set_ylim(0.82, 12.92)
    ax.set_zlim(6.96, 12.96)
    
    ax.set_box_aspect((0.80, 1.55, 0.77))
    
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(False)
    
    # Labels
    ax.set_xlabel(r"$x$ ($\AA$)", labelpad=10)
    ax.set_ylabel(r"$y$ ($\AA$)", labelpad=10)
    ax.set_zlabel(r"$z$ ($\AA$)", labelpad=12)
    
    # Title
    ax.set_title(r"1T-WTe$_2$ (Ideal)", pad=-20, fontsize=24, y=1.02)
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='W',
               markerfacecolor='#2c3e50', markersize=15, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Te',
               markerfacecolor='#f39c12', markersize=12, markeredgecolor='black')
    ]
    ax.legend(handles=legend_elements, loc='upper left', frameon=False, fontsize=14)
    
    out_dir = os.path.dirname(os.path.abspath(__file__)) + "/../figures"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    plt.savefig(f"{out_dir}/Fig_Structure_3D_1T.png", dpi=300, bbox_inches='tight', pad_inches=0.02)
    print(f"Saved {out_dir}/Fig_Structure_3D_1T.png")

if __name__ == "__main__":
    plot_1T_3d()
