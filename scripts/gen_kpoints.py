import sys

# Hardcoded for 12 x 6 x 1
nk1, nk2, nk3 = 12, 6, 1

print("begin kpoints")
for k in range(nk3):       # Z (Slowest)
    for j in range(nk2):   # Y (Middle)
        for i in range(nk1): # X (Fastest)
             kx = i / nk1
             ky = j / nk2
             kz = k / nk3 if nk3 > 1 else 0.0
             print(f"{kx:.6f} {ky:.6f} {kz:.6f}")
print("end kpoints")
