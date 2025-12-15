import matplotlib.pyplot as plt
import re

iterations = []
spreads = []

in_table = False

with open('wte2.wout', 'r') as f:
    for line in f:
        # Detect header: | Iter  Delta Spread     RMS Gradient      Spread (Ang^2)      Time  |<-- CONV
        if "RMS Gradient" in line and "Spread (Ang^2)" in line:
            in_table = True
            continue
            
        if in_table:
            # End of table check
            if "Total Execution Time" in line or "All done" in line or "trace" in line:
                in_table = False
                break
            
            # Line format:       1   -0.292E+03       0.499E-05      0.341E+02       0.46
            parts = line.split()
            if len(parts) >= 4:
                try:
                    # Column 0: Iter
                    it = int(parts[0])
                    # Column 3: Spread (Ang^2) - check header order
                    # Header: Iter, Delta, RMS, Spread, Time
                    # Index:  0     1      2    3       4
                    sp = float(parts[3])
                    
                    iterations.append(it)
                    spreads.append(sp)
                except ValueError:
                    continue

print(f"Parsed {len(iterations)} iterations.")
if len(iterations) > 0:
    plt.figure(figsize=(8, 5))
    plt.plot(iterations, spreads, 'o-', color='purple', markersize=3, linewidth=1)
    
    # Annotate Final Spread
    final_spread = spreads[-1]
    plt.annotate(f"{final_spread:.2f}", xy=(iterations[-1], spreads[-1]), 
                 xytext=(iterations[-1]-10, spreads[-1]+(max(spreads)-min(spreads))*0.1),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    plt.xlabel("Iteration")
    plt.ylabel(r"Total Spread ($\AA^2$)")
    plt.title("Maximally Localized Wannier Function Convergence")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("Fig_Credibility_Spreads.png", dpi=300)
    print("Spread plot saved.")
else:
    print("Could not parse iterations. Check wte2.wout format.")
