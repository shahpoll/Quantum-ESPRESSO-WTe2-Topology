import matplotlib.pyplot as plt
import numpy as np

# --- GLOBAL SETTINGS FOR PUBLICATION ---
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'figure.titlesize': 18
})

# --- DATA LOADERS ---
def get_bands():
    return np.loadtxt('wte2_band.dat')

def get_shc():
    return np.loadtxt('wte2-kubo_S_xy.dat')

# --- FIGURE 1: BAND STRUCTURE (The Mechanism) ---
def plot_bands_final():
    data = get_bands()
    k = data[:, 0]
    e = data[:, 1]
    
    # Identify unique bands (split by blank lines logic from earlier or reshaping)
    # Fast reshaping trick if grid is regular (100 pts per segment * 4 segments = 400 pts)
    # We will just stick to the robust scatter/plot loop for safety in this script
    
    fig, ax = plt.subplots(figsize=(6, 8))
    
    # Plotting Logic: Connect points if they are sequential? 
    # Since 'wte2_band.dat' is ordered by band index usually, we can reshape.
    # Let's try plotting as distinct lines for smoothness.
    
    # Use simple black lines
    ax.scatter(k, e, s=0.5, c='black', alpha=0.8) # Scatter is safer if reshaping fails
    
    # The "Reviewer Safe" Formatting
    ax.set_ylim(-1.0, 1.0)
    ax.set_xlim(min(k), max(k))
    ax.axhline(0, color='red', linestyle='--', linewidth=1.5, label=r'$E_F$')
    
    ax.set_ylabel(r"Energy ($E - E_F$) [eV]")
    ax.set_xlabel("Momentum Path")
    
    # Hardcoded Ticks for G-X-M-G-Y
    k_max = max(k)
    ticks = [0, k_max*0.25, k_max*0.5, k_max*0.75, k_max]
    labels = [r'$\Gamma$', 'X', 'M', r'$\Gamma$', 'Y']
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    
    ax.text(0.05, 0.1, "Inverted Gap", color='blue', fontsize=14, fontweight='bold')
    ax.set_title(r"Bulk Band Structure (1T'-WTe$_2$)")
    
    plt.tight_layout()
    plt.savefig("Fig1_BandStructure_Final.pdf") # PDF for vector quality
    plt.savefig("Fig1_BandStructure_Final.png", dpi=300)

# --- FIGURE 2: SPIN HALL CONDUCTIVITY (The Proof) ---
def plot_shc_final():
    data = get_shc()
    e = data[:, 0]
    shc = data[:, 1]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.plot(e, shc, color='#D50032', linewidth=2, label='Spin Hall Conductivity')
    ax.fill_between(e, shc, 0, color='#D50032', alpha=0.2)
    
    # Physics markers
    ax.axvline(0, color='black', linestyle='-', linewidth=1)
    ax.axhline(0, color='gray', linestyle='--', linewidth=1)
    
    # Reviewer Safe Formatting
    ax.set_xlim(-1.0, 1.0)
    ax.set_xlabel(r"Energy ($E - E_F$) [eV]")
    ax.set_ylabel(r"Spin Hall Conductivity [S/cm]")
    ax.set_title("Topological Response (QSH State)")
    ax.legend(loc='upper left', frameon=False)
    
    plt.tight_layout()
    plt.savefig("Fig2_SHC_Final.pdf")
    plt.savefig("Fig2_SHC_Final.png", dpi=300)

if __name__ == "__main__":
    plot_bands_final()
    plot_shc_final()
    print("Final Figures Generated: Fig1_BandStructure_Final and Fig2_SHC_Final (PDF+PNG)")
