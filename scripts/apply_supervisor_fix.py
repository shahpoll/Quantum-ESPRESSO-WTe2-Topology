
# Read the fractional kpoints
with open('kpoints_frac.txt', 'r') as f:
    lines = f.readlines()

kpoints_nscf = "".join(lines)
kpoints_win = "".join(["  ".join(line.split()[:3]) + "\n" for line in lines])

# 1. Update NSCF
with open('wte2.nscf.in', 'r') as f:
    nscf_content = f.read()

# Replace K_POINTS block
# We look for "K_POINTS" and replace everything after it with "crystal\n72\n" + list
if "K_POINTS" in nscf_content:
    base = nscf_content.split("K_POINTS")[0]
    new_nscf = base + "K_POINTS crystal\n72\n" + kpoints_nscf
    with open('wte2.nscf.in', 'w') as f:
        f.write(new_nscf)
    print("Updated wte2.nscf.in")

# 2. Update WIN
with open('wte2.win', 'r') as f:
    win_content = f.read()

# Replace kpoints block
# We need to find "begin kpoints" and "end kpoints"
import re
new_win = re.sub(r'begin kpoints.*?end kpoints', f'begin kpoints\n{kpoints_win}end kpoints', win_content, flags=re.DOTALL)

with open('wte2.win', 'w') as f:
    f.write(new_win)
print("Updated wte2.win")
