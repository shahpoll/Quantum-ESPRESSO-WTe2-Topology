import matplotlib.pyplot as plt
import re

# Parse the log for spread
iterations = []
spreads = []

# State flags
in_minimization = False

with open('wte2.wout', 'r') as f:
    for line in f:
        if "Initial State" in line:
            in_minimization = True
            continue
        
        if "Final State" in line:
            in_minimization = False
            break
            
        if in_minimization:
            # Line format: Integers (Iter) followed by Floats (Spread)
            # Example:      1    2.9237516095E+02     5.9529342404E+02 ...
            # Regex: Start with whitespace, number, whitespace, number...
            if re.search(r'^\s*\d+\s+\d+\.\d+', line):
                parts = line.split()
                # Ensure it's the right table (usually has >3 columns: Iter, O_D, O_OD, O_TOT, etc)
                if len(parts) >= 4:
                    try:
                        it = int(parts[0])
                        # In W90, Total Spread is typically the 2nd column or last?
                        # Header: Iter  Delta Spread  RMS Gradient  Spread
                        # Actually standard output:
                        # Iter   Delta Spread     RMS Gradient      Spread
                        #   1    -0.292E+03       0.499E-05      0.341E+02
                        # Let's check the line content from the grep I'll see in a moment.
                        # Assuming last column is Spread or 2nd is Delta.
                        # Wait, usually it prints: Iter, O_I, O_D, O_OD, Total
                        # Let's rely on the simple logic: if it parses, plot column 2 (or verify).
                        # Let's verify with the grep output first.
                        pass
                    except:
                        continue

# REFINED LOGIC AFTER SEEING GREP:
# IF the grep shows:
#      1     292.37516095     292.37370258       4.988E-06     34.11    <-- DIS
# This is Disentanglement? No, "Cycles" are disentanglement.
# Minimization usually strictly integers.
# I will wait for the grep result to write the correct parser.
