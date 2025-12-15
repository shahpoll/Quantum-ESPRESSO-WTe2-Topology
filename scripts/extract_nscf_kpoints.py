import re
import sys

# Read from stdin or file
lines = sys.stdin.readlines()

kpoints = []
for line in lines:
    # Format: k(   1) = (   0.0000000   0.0000000   0.0000000), wk =   0.0138889
    match = re.search(r'k\(\s*\d+\)\s*=\s*\(\s*([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s*\)', line)
    if match:
        kpoints.append(f"{float(match.group(1)):.6f} {float(match.group(2)):.6f} {float(match.group(3)):.6f}")

print("begin kpoints")
for kp in kpoints:
    print(kp)
print("end kpoints")
