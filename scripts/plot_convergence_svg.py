import re
import math

# File paths
input_file = 'Final_Results/01_Geometry/wte2.vc-relax.out'
output_file = 'Final_Results/01_Geometry/convergence_plot.svg'

# 1. Parse Data
energies = []
try:
    with open(input_file, 'r') as f:
        for line in f:
            if "total energy" in line and "=" in line:
                # Format:      total energy              =   -2982.40465548 Ry
                parts = line.split('=')
                if len(parts) > 1:
                    try:
                        e_ry = float(parts[1].split()[0])
                        energies.append(e_ry)
                    except ValueError:
                        continue
except FileNotFoundError:
    print(f"Error: Could not find {input_file}")
    exit()

if not energies:
    print("No energy data found.")
    exit()

# 2. SVG Configuration
width = 800
height = 600
margin = 80
plot_width = width - 2 * margin
plot_height = height - 2 * margin

# 3. Scaling
min_e = min(energies)
max_e = max(energies)
range_e = max_e - min_e if max_e != min_e else 1.0
min_x = 0
max_x = len(energies) - 1
range_x = max_x if max_x > 0 else 1

def map_x(i):
    return margin + (i / range_x) * plot_width

def map_y(e):
    # Higher energy = lower pixel Y (SVG Y goes down)
    normalized = (e - min_e) / range_e
    return (height - margin) - (normalized * plot_height)

# 4. Generate SVG
svg = []
svg.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background-color:white; font-family:Arial">')
svg.append(f'<rect width="100%" height="100%" fill="white"/>')

# Title & Axes
svg.append(f'<text x="{width/2}" y="40" font-size="20" text-anchor="middle">Geometry Optimization History: 1T\'-WTe2</text>')
svg.append(f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="black" stroke-width="2"/>') # X Axis
svg.append(f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="black" stroke-width="2"/>') # Y Axis
svg.append(f'<text x="{width/2}" y="{height-20}" font-size="14" text-anchor="middle">BFGS Iteration Step</text>')
svg.append(f'<text x="20" y="{height/2}" font-size="14" text-anchor="middle" transform="rotate(-90, 20, {height/2})">Total Energy (Ry)</text>')

# Gridlines & Y Labels (5 steps)
steps = 5
for i in range(steps + 1):
    val = min_e + (range_e * i / steps)
    y_pos = map_y(val)
    svg.append(f'<line x1="{margin}" y1="{y_pos}" x2="{width-margin}" y2="{y_pos}" stroke="#ddd" stroke-dasharray="4"/>')
    svg.append(f'<text x="{margin-10}" y="{y_pos+5}" font-size="12" text-anchor="end">{val:.4f}</text>')

# Plot Line
points = []
for i, e in enumerate(energies):
    points.append(f'{map_x(i):.1f},{map_y(e):.1f}')

svg.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="blue" stroke-width="2"/>')

# Plot Points
for i, e in enumerate(energies):
    cx = map_x(i)
    cy = map_y(e)
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="blue"/>')

# Highlight Final Point
last_x = map_x(len(energies)-1)
last_y = map_y(energies[-1])
svg.append(f'<circle cx="{last_x}" cy="{last_y}" r="5" fill="red"/>')
svg.append(f'<text x="{last_x-10}" y="{last_y-10}" font-size="14" fill="red" text-anchor="end">Converged: {energies[-1]:.4f} Ry</text>')

svg.append('</svg>')

# 5. Write File
with open(output_file, 'w') as f:
    f.write("\n".join(svg))

print(f"Generated {output_file} ({len(energies)} iterations)")
