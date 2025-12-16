import matplotlib.pyplot as plt
import matplotlib.patches as patches

import os

# --- CONFIGURATION ---
# Output Format: PNG as requested
# Navigate to repo/figures relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "../figures/Fig_BZ_Schematic.png") 

def plot_bz():
    """
    Generates a schematic of the 2D Rectangular Brillouin Zone 
    for the 1T' monoclinic cell projection.
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # 1. Define BZ Dimensions (Normalized units)
    # kx goes from -0.5 to 0.5 (in units of 2pi/a)
    # ky goes from -0.5 to 0.5 (in units of 2pi/b)
    bz_width = 1.0
    bz_height = 1.0
    
    # 2. Draw the BZ Boundary
    rect = patches.Rectangle(
        (-0.5, -0.5), bz_width, bz_height, 
        linewidth=2, edgecolor='black', facecolor='#F5F5F5', zorder=1
    )
    ax.add_patch(rect)
    
    # 3. Define High Symmetry Points
    # Coordinates in normalized k-space
    points = {
        r'$\Gamma$': (0, 0),
        'X': (0.5, 0),
        'Y': (0, 0.5),
        'M': (0.5, 0.5)
    }
    
    # 4. Draw the K-Path (Trajectory for Band Structure)
    # Path: Gamma -> X -> M -> Gamma -> Y
    path_x = [0, 0.5, 0.5, 0, 0]
    path_y = [0, 0, 0.5, 0, 0.5]
    
    plt.plot(path_x, path_y, color='#D50032', linewidth=2.5, linestyle='--', zorder=2, label='Band Path')
    
    # 5. Plot Points and Labels
    for label, (px, py) in points.items():
        # Plot dot
        plt.scatter(px, py, color='#003366', s=150, zorder=3, edgecolor='white', linewidth=1.5)
        
        # Smart Label Offset
        off_x = 0.03 if px < 0.4 else -0.08
        off_y = 0.03 if py < 0.4 else -0.08
        
        # Adjust Gamma specifically
        if 'Gamma' in label: 
            off_x, off_y = 0.02, 0.02
            
        plt.text(px + off_x, py + off_y, label, fontsize=16, fontweight='bold', zorder=4)

    # 6. Formatting
    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-0.6, 0.6)
    ax.set_aspect('equal')
    ax.axis('off') # Hide axes for clean schematic look
    
    # Optional: Add axis arrows for kx/ky
    ax.arrow(-0.55, -0.55, 0.2, 0, head_width=0.03, head_length=0.03, fc='k', ec='k')
    ax.arrow(-0.55, -0.55, 0, 0.2, head_width=0.03, head_length=0.03, fc='k', ec='k')
    ax.text(-0.33, -0.57, r'$k_x$', fontsize=12)
    ax.text(-0.58, -0.33, r'$k_y$', fontsize=12)

    plt.title("First Brillouin Zone (2D)", fontsize=14, pad=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, format='png', dpi=300)
    print(f"Brillouin Zone schematic saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    plot_bz()
