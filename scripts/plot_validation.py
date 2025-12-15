import matplotlib.pyplot as plt
import numpy as np
import re

def parse_qe_bands(filename):
    """Parses bands from PWSCF output"""
    bands = []
    kpoints = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    in_bands = False
    current_k = None
    
    for i, line in enumerate(lines):
        if "End of band structure calculation" in line:
            break
        if "k =" in line and "bands (ev)" in line:
            # k = 0.0000 0.0000 0.0000     bands (ev):
            k_match = re.search(r'k =\s*([\d\.-]+)\s*([\d\.-]+)\s*([\d\.-]+)', line)
            if k_match:
                # Store k-point (not strictly used for x-axis here since we just strictly order them)
                pass
            in_bands = True
            continue
        
        if in_bands:
            if "k =" in line or not line.strip(): 
                in_bands = False
                continue
            # Read energy values
            try:
                vals = [float(x) for x in line.split()]
                # We need to flatten this list into a structure, but QE output spreads bands across lines
                # This parser is simple: we'll just collect all numbers found in the "bands" section
                # actually, better to collect per k-point.
                pass 
            except:
                pass

    # Re-implmenting robust parser
    # Strategy: Find "k =" lines, then read following lines until next "k ="
    # It's tricky to get exact path distance (x-axis) without re-calculating metric.
    # Hybrid approach: Assume linear spacing or index.
    
    # Better: Use the 'bands.x' tool? No, user wants direct output parsing.
    # Let's use a simpler heuristic:
    # 1. Extract all 'bands (ev):' blocks.
    # 2. Flatten.
    extracted_bands = []
    
    current_k_bands = []
    capturing = False
    
    for line in lines:
        if "bands (ev):" in line:
            if current_k_bands:
                extracted_bands.append(current_k_bands)
                current_k_bands = []
            capturing = True
            continue
        
        if capturing:
            # Stop capturing if we hit a new k-point header or end of job
            # Valid band lines contain floats. 
            # If line contains "k =" or "JOB DONE" or "writing output", stop.
            if "k =" in line or "JOB DONE" in line or "writing output" in line:
                capturing = False
                if current_k_bands:
                     extracted_bands.append(current_k_bands)
                     current_k_bands = []
            elif line.strip(): # If line has content
                # Try to parse numbers. 
                try:
                    # Clean the line of non-numeric noise if necessary, but usually just numbers
                    vals = [float(x) for x in line.split()]
                    if vals: # Only append if we actually found numbers
                        current_k_bands.extend(vals)
                except ValueError:
                    # If conversion fails, it's likely text, so stop capturing
                    pass
                    
    if current_k_bands:
        extracted_bands.append(current_k_bands)
        
    return np.array(extracted_bands)

def parse_wannier_bands(filename):
    """
    Reads a standard Wannier90 band.dat file.
    """
    bands = []
    current_band = []
    
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip():
                if current_band:
                    bands.append(np.array(current_band))
                    current_band = []
            else:
                try:
                    parts = line.split()
                    k = float(parts[0])
                    e = float(parts[1])
                    current_band.append([k, e])
                except ValueError:
                    continue
    if current_band:
        bands.append(np.array(current_band))
    return bands

# --- LOAD DATA ---
try:
    qe_data = parse_qe_bands('wte2.dft_bands.out')
    print(f"Loaded DFT bands: {qe_data.shape} (k-points, bands)")
except Exception as e:
    print(f"DFT Load Error: {e}")
    qe_data = None

try:
    wan_bands = parse_wannier_bands('wte2_band.dat')
    print(f"Loaded Wannier bands: {len(wan_bands)} bands")
except:
    wan_bands = None

# --- PLOTTING ---
fig, ax = plt.subplots(figsize=(8, 6))

# Plot DFT (Red Dots)
if qe_data is not None:
    # We need an x-axis. Using index is okay if we align path, 
    # but Wannier has X-axis in path length.
    # Let's scale DFT x-axis to match Wannier range [0, max_k]
    # Assuming same k-path (81 points vs 100 points?)
    # wte2.dft_bands.in has K_POINTS crystal_b with 5 points (20 intervals -> ~80 pts)
    # Wannier: 100 pts/segment * 4 segments = 400 pts?
    # Scaling is hard. We will plot separate or overlay roughly.
    
    # We will try to map the x-axis:
    # Best effort: Just plotting Energy vs Index for DFT is misleading.
    # Let's rely on just energy range visual check or matching k-path length.
    
    # Simplification: Plot DFT as scattered points on their index normalized to 1?
    # No, let's just plot DFT Bands.
    
    # Actually, let's assume Wannier path is the "master" axis.
    # We won't perfectly align X-axis in this quick script without computing path length.
    # We'll plot Energy vs "K-point Index" and scale Wannier to match.
    
    nk_dft = qe_data.shape[0]
    x_dft = np.linspace(0, 1, nk_dft)
    
    if wan_bands:
        nk_wan = len(wan_bands[0])
        x_wan = np.linspace(0, 1, nk_wan)
    
    # DFT
    for ib in range(qe_data.shape[1]):
        ax.scatter(x_dft, qe_data[:, ib], color='red', s=10, label='DFT' if ib==0 else "", zorder=2)

    # Wannier
    if wan_bands:
        for band in wan_bands:
            # Interpolate Wannier to 0..1 x-axis
            # band[:, 0] is path length.
            # We normalize it.
            k_raw = band[:, 0]
            k_norm = (k_raw - k_raw[0]) / (k_raw[-1] - k_raw[0])
            e = band[:, 1]
            ax.plot(k_norm, e, color='blue', linewidth=1, alpha=0.7, label='Wannier' if band is wan_bands[0] else "", zorder=1)

ax.set_ylim(-3, 3)
ax.axhline(0, color='gray', linestyle='--')
ax.set_title("Validation: DFT (Red) vs Wannier (Blue)")
ax.set_xlabel("Normalized K-Path")
ax.set_ylabel("Energy (eV)")
ax.legend()
ax.grid(True, alpha=0.3)

plt.savefig("validation_dft_vs_wannier.png", dpi=150)
print("Saved validation_dft_vs_wannier.png")
