import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# Function to draw box with text
def draw_step(x, y, text, script_name, color='#E0E0E0', extra_label=None, extra_color='red'):
    # Box
    rect = patches.FancyBboxPatch((x, y), 2.5, 1.2, boxstyle="round,pad=0.1", 
                                  linewidth=1.5, edgecolor='black', facecolor=color)
    ax.add_patch(rect)
    
    if extra_label:
        # 3-line spacing
        ax.text(x+1.25, y+0.9, text, ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(x+1.25, y+0.6, f"({script_name})", ha='center', va='center', fontsize=10, 
                color='#333333', style='italic')
        ax.text(x+1.25, y+0.3, extra_label, ha='center', va='center', fontsize=8, 
                color=extra_color, fontweight='bold')
    else:
        # Standard 2-line spacing
        ax.text(x+1.25, y+0.8, text, ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(x+1.25, y+0.4, f"({script_name})", ha='center', va='center', fontsize=10, 
                color='#333333', style='italic')

# --- DRAW STEPS ---
# 1. SCF (Ground State)
draw_step(0.5, 4, "DFT Ground State", "pw.x < wte2.scf.in")

# 2. NSCF (Wavefunctions)
draw_step(3.8, 4, "Wavefunctions", "pw.x < wte2.nscf.in")

# 3. Projection
draw_step(7.1, 4, "Wannier Prep", "wannier90.x -pp")

# 4. Wannierization
draw_step(3.8, 2, "Minimization", "wannier90.x", extra_label="Memory Critical (>32GB)", extra_color='red')
# ax.text removed as it's now internal

# 5. Topology (The Pivot)
draw_step(3.8, 0, "Topological Proof\n(SHC + Ribbon)", "plot_shc.py\nplot_ribbon.py", color='#FFCDD2')

# --- ARROWS ---
style = "Simple, tail_width=0.5, head_width=4, head_length=8"
kw = dict(arrowstyle=style, color="k")

# SCF -> NSCF
ax.add_patch(patches.FancyArrowPatch((3.1, 4.6), (3.7, 4.6), connectionstyle="arc3,rad=0", **kw))
# NSCF -> Prep
ax.add_patch(patches.FancyArrowPatch((6.4, 4.6), (7.0, 4.6), connectionstyle="arc3,rad=0", **kw))
# Prep -> Min (Curved back)
ax.add_patch(patches.FancyArrowPatch((8.35, 3.9), (6.4, 2.6), connectionstyle="arc3,rad=-0.3", **kw))
# Min -> Topology
ax.add_patch(patches.FancyArrowPatch((5.05, 1.9), (5.05, 1.3), connectionstyle="arc3,rad=0", **kw))

ax.set_title("Reproducible Topological Workflow", fontsize=16)
plt.savefig("Fig_Workflow.png", dpi=300)
print("Workflow flowchart generated.")
