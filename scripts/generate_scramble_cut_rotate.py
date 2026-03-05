"""
Generate cut-and-rotate scrambling illustration for the Scramble program guide.
Shows a scanline being split at a cut point and the two halves swapped.
Output: static/img/instruments/videomancer/scramble/scramble_cut_and_rotate.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

out_dir = Path(__file__).resolve().parent.parent / "static" / "img" / "instruments" / "videomancer" / "scramble"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "scramble_cut_and_rotate.png"

fig, axes = plt.subplots(3, 1, figsize=(10, 6), facecolor='#1a1a2e',
                          gridspec_kw={'height_ratios': [1, 0.5, 1]})

for ax in axes:
    ax.set_facecolor('#1a1a2e')
    ax.set_xlim(0, 1024)
    ax.set_ylim(-0.3, 1.3)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

# Colors
color_a = '#66ccff'
color_b = '#ff9944'
cut_color = '#ff4444'
bg_alpha = 0.3

cut_point = 384  # pixels into the 1024-pixel line

# --- Top: Original scanline ---
ax = axes[0]
ax.set_title("Original Scanline", fontsize=11, color='#cccccc', pad=8, loc='left')

# Draw the full scanline as two halves
ax.barh(0.5, cut_point, height=0.6, left=0, color=color_a, alpha=0.7, edgecolor='#ffffff', linewidth=0.5)
ax.barh(0.5, 1024 - cut_point, height=0.6, left=cut_point, color=color_b, alpha=0.7, edgecolor='#ffffff', linewidth=0.5)

# Cut point marker
ax.axvline(cut_point, color=cut_color, linewidth=2, linestyle='--', ymin=0.1, ymax=0.9)
ax.annotate(f"Cut Point\n(pixel {cut_point})", xy=(cut_point, 1.05), fontsize=9,
            color=cut_color, ha='center', fontweight='bold')

# Labels
ax.text(cut_point / 2, 0.5, f"Part A\n({cut_point} px)", ha='center', va='center',
        fontsize=10, color='#ffffff', fontweight='bold')
ax.text(cut_point + (1024 - cut_point) / 2, 0.5, f"Part B\n({1024 - cut_point} px)",
        ha='center', va='center', fontsize=10, color='#ffffff', fontweight='bold')

# Pixel ruler
ax.text(0, -0.15, "0", fontsize=8, color='#888888', ha='center')
ax.text(1024, -0.15, "1023", fontsize=8, color='#888888', ha='center')

# --- Middle: Arrows showing the swap ---
ax = axes[1]
# Curved arrows to show the swap
ax.annotate('', xy=(750, 0.7), xytext=(200, 0.7),
            arrowprops=dict(arrowstyle='->', color=color_a, lw=2,
                          connectionstyle='arc3,rad=-0.3'))
ax.annotate('', xy=(200, 0.3), xytext=(750, 0.3),
            arrowprops=dict(arrowstyle='->', color=color_b, lw=2,
                          connectionstyle='arc3,rad=-0.3'))
ax.text(512, 0.5, "Swap", ha='center', va='center', fontsize=11,
        color='#ffffff', fontweight='bold', style='italic')

# --- Bottom: Scrambled scanline ---
ax = axes[2]
ax.set_title("Scrambled Scanline (cut-and-rotate)", fontsize=11, color='#cccccc', pad=8, loc='left')

# B comes first, then A
b_width = 1024 - cut_point
ax.barh(0.5, b_width, height=0.6, left=0, color=color_b, alpha=0.7, edgecolor='#ffffff', linewidth=0.5)
ax.barh(0.5, cut_point, height=0.6, left=b_width, color=color_a, alpha=0.7, edgecolor='#ffffff', linewidth=0.5)

# Labels
ax.text(b_width / 2, 0.5, f"Part B\n({b_width} px)", ha='center', va='center',
        fontsize=10, color='#ffffff', fontweight='bold')
ax.text(b_width + cut_point / 2, 0.5, f"Part A\n({cut_point} px)",
        ha='center', va='center', fontsize=10, color='#ffffff', fontweight='bold')

# Wrap boundary
ax.axvline(b_width, color='#aaaaaa', linewidth=1, linestyle=':', ymin=0.1, ymax=0.9)

ax.text(0, -0.15, "0", fontsize=8, color='#888888', ha='center')
ax.text(1024, -0.15, "1023", fontsize=8, color='#888888', ha='center')

fig.suptitle("Per-Line Cut-and-Rotate Scrambling", fontsize=14,
             color='#ffffff', fontweight='bold', y=0.98)
fig.text(0.5, 0.01,
         "Each scanline is split at a pseudo-random cut point and the two halves are swapped, wrapping around the 1024-pixel buffer.",
         ha='center', fontsize=9, color='#999999', style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 0.95])
plt.savefig(out_path, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
print(f"Saved: {out_path}")
