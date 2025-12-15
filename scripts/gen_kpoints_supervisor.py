nx, ny, nz = 12, 6, 1
kpoints = []
# X-fastest ordering (Standard for W90)
# Loop order: Z (slow), Y (med), X (fast) ?
# W90 usually expects: 
#   do k3=...
#     do k2=...
#       do k1=...
# So X is fastest.
for kx in range(nx): # Wait, if loop order is kx, ky, kz, then KZ is fastest?
    # No, python list append order:
    # 0,0,0 -> 0,0,1 ... (if kz inner)
    # The user snippet was:
    # for kx in range(nx):
    #    for ky in range(ny):
    #        for kz in range(nz):
    # This makes kx slowest, kz fastest.
    # Standard Mesh: k = (i-1)/n1 * b1 + ...
    # Standard W90 ordering: 
    # "The k-points are stored in the order ... with the first index running fastest." (W90 User Guide)
    # i.e. x is fastest.
    # So `for kz... for ky... for kx...`
    pass

# Re-reading Supervisor Instruction:
# script:
# for kx in range(nx):
#    for ky in range(ny):
#        for kz in range(nz):
# This generates:
# 0 0 0
# 0 0 1 (if nz>1)
# ...
# 0 1 0
# ...
# 1 0 0
# So KX is SLOWEST. KZ is FASTEST.
#
# BUT, usually W90 wants X fastest. 
# Let's check wte2.wout error "Non-symmetric k-point neighbours".
# If I use `mp_grid 12 6 1`, W90 expects 12 points along b1, 6 along b2.
# 
# Let's stick strictly to the Supervisor's python snippet.
# If it's wrong, I'll fix the ordering later. But "Supervisor" implies authority.
# Wait, let's verify ordering.
# If I paste a list, W90 usually reads it sequentially.
# If `mp_grid` is specified, W90 assumes the list is ordered.
# 
# Let's write the code provided in the prompt exactly:
kpoints = []
for kx in range(nx):
    for ky in range(ny):
        for kz in range(nz):
             kpoints.append(f"{kx/nx:.8f}  {ky/ny:.8f}  {kz/nz:.8f}  {1.0/(nx*ny*nz):.6f}")

with open('kpoints_frac.txt', 'w') as f:
    f.write('\n'.join(kpoints))
