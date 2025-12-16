import os
# import matplotlib.pyplot as plt (moved to main)
import subprocess
import re

# --- CONFIGURATION ---
PSEUDO_DIR = "./"  # Where your UPF files are
OUT_DIR = "convergence_results"
INPUT_TEMPLATE = "wte2.scf.in" # Ensure this exists in current folder

# Range of Cutoffs to test (Ry)
CUTOFFS = [30, 40, 50, 60, 70, 80]

def update_input(cutoff):
    with open(INPUT_TEMPLATE, 'r') as f:
        content = f.read()
    
    # Regex replace ecutwfc
    content = re.sub(r'ecutwfc\s*=\s*[\d\.]+', f'ecutwfc = {cutoff}', content)
    # Scale ecutrho usually 8x or 10x
    content = re.sub(r'ecutrho\s*=\s*[\d\.]+', f'ecutrho = {cutoff*8}', content)
    
    filename = f"wte2_cut_{cutoff}.in"
    with open(filename, 'w') as f:
        f.write(content)
    return filename

def get_energy(outfile):
    try:
        # Grep the energy
        result = subprocess.check_output(f"grep ! {outfile}", shell=True).decode()
        # Parse line: "!    total energy              =     -234.1234 Ry"
        return float(result.split('=')[1].split()[0])
    except:
        return None

def main():
    if not os.path.exists(OUT_DIR): os.makedirs(OUT_DIR)
    
    energies = []
    print("Starting Convergence Study...")
    
    for cut in CUTOFFS:
        inp = update_input(cut)
        out = inp.replace(".in", ".out")
        
        print(f"Running Cutoff {cut} Ry...")
        # Run PW.x (Adjust command if needed, e.g., mpirun)
        os.system(f"pw.x < {inp} > {OUT_DIR}/{out}")
        
        E = get_energy(f"{OUT_DIR}/{out}")
        if E:
            energies.append(E)
            print(f"  -> Energy: {E} Ry")
        else:
            print("  -> Failed")
            energies.append(None)

    # Plot
    valid_cuts = [c for c, e in zip(CUTOFFS, energies) if e is not None]
    valid_enes = [e for c, e in zip(CUTOFFS, energies) if e is not None]
    
    # Delta E relative to most converged
    if not valid_enes:
        print("No valid energies found.")
        return

    delta_E = [(e - valid_enes[-1])*13.605 for e in valid_enes] # eV
    
    # Save data to text file
    with open(f"{OUT_DIR}/convergence_data.txt", "w") as f:
        f.write("Cutoff(Ry) Energy(Ry) DeltaE(eV)\n")
        for c, e, de in zip(valid_cuts, valid_enes, delta_E):
            f.write(f"{c} {e} {de}\n")
    print(f"Data saved to {OUT_DIR}/convergence_data.txt")

    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(6,4))
        plt.plot(valid_cuts, delta_E, 'o-', color='#D50032')
        plt.xlabel("Plane Wave Cutoff (Ry)")
        plt.ylabel("Energy Difference (eV)")
        plt.title("Wavefunction Convergence Test")
        plt.grid(True, alpha=0.3)
        plt.axhline(0, color='black', lw=1)
        plt.tight_layout()
        plt.savefig("Fig_Convergence_Cutoff.png", dpi=300)
        print("Plot saved to Fig_Convergence_Cutoff.png")
    except ImportError:
        print("Matplotlib not found. Skipping plot generation.")


if __name__ == "__main__":
    main()
