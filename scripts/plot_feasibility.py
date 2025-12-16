import matplotlib.pyplot as plt
import numpy as np

import os

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "../figures/Fig_Feasibility_Memory.png")

def plot_memory_feasibility():
    """
    Visualizes the memory bottleneck during the Wannierization step.
    Compares Standard Desktop vs High-Performance Cluster Node.
    """
    
    # Data: Peak Memory Usage (Estimated from logs)
    # Wannier90 (High K-mesh) typically spikes memory during disentanglement
    peak_memory_req = 38.0  # GB (Estimated requirement for 12x12x1 full matrix)
    
    # System Capabilities
    systems = ['Standard Workstation', 'High-Performance Node']
    ram_limits = [16.0, 64.0] # GB
    
    # Colors (Scientific Palette)
    # Red for insufficient, Green/Blue for sufficient
    colors = ['#E0E0E0', '#4A90E2'] 
    edge_colors = ['#888888', '#003366']

    fig, ax = plt.subplots(figsize=(7, 5))
    
    # 1. Plot the RAM Limits (The Container)
    bars = ax.bar(systems, ram_limits, color=colors, edgecolor=edge_colors, 
                  width=0.5, linewidth=2, label='Available RAM')
    
    # 2. Plot the Requirement Line
    # Draw a dashed line across the plot showing the memory needed
    ax.axhline(y=peak_memory_req, color='#D50032', linestyle='--', linewidth=2, zorder=3)
    ax.text(0.5, peak_memory_req + 2, f'Min. Requirement (~{int(peak_memory_req)} GB)', 
            color='#D50032', ha='center', fontweight='bold', fontsize=11)
    
    # 3. Annotations (Status)
    
    # Bar 1: Standard
    ax.text(0, ram_limits[0]/2, "16 GB Capacity", ha='center', va='center', color='black')
    ax.text(0, ram_limits[0] + 2, "FAILURE\n(Out of Memory)", 
            ha='center', va='bottom', color='#D50032', fontweight='bold')
    
    # Bar 2: High Performance
    ax.text(1, ram_limits[1]/2, "64 GB Capacity", ha='center', va='center', color='white')
    ax.text(1, peak_memory_req - 10, "Calculation\nConverged", 
            ha='center', va='center', color='white', fontweight='bold')

    # 4. Styling
    ax.set_ylabel("System Memory (GB)", fontsize=12)
    ax.set_ylim(0, 75)
    ax.set_title("Computational Resource Feasibility", fontsize=14)
    ax.grid(axis='y', linestyle=':', alpha=0.5)
    
    # Add a "Hatched" region to show the "Crash Zone" for system 1
    # We visually shade the area above the 16GB bar up to the red line to imply "Missing Resource"
    # (Optional, keeping it clean for now)

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, format='png', dpi=300)
    print(f"Feasibility chart saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    plot_memory_feasibility()
