"""
Generate gamma transfer curve illustration for the Lumarian program guide.
Shows logarithmic, linear, and exponential curves on a clean dark-themed plot.
Output: static/img/instruments/videomancer/lumarian/lumarian_gamma_curves.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Output path
out_dir = Path(__file__).resolve().parent.parent / "static" / "img" / "instruments" / "videomancer" / "lumarian"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "lumarian_gamma_curves.png"

x = np.linspace(0, 1, 512)

# Gamma curves — using power function like real gamma correction
# gamma < 1 = logarithmic (lift shadows)
# gamma = 1 = linear
# gamma > 1 = exponential (crush shadows)
curves = [
    (0.35, "Logarithmic (Gamma CCW)", "#66ccff"),
    (0.55, "Mild Log", "#3399cc"),
    (1.0,  "Linear (center)", "#cccccc"),
    (1.8,  "Mild Exp", "#cc9933"),
    (3.0,  "Exponential (Gamma CW)", "#ff9944"),
]

fig, ax = plt.subplots(figsize=(7, 6), facecolor='#1a1a2e')
ax.set_facecolor('#1a1a2e')

# Draw the linear reference first as a subtle dashed line
ax.plot(x, x, '--', color='#555555', linewidth=1, zorder=1)

for gamma_val, label, color in curves:
    y = np.clip(np.power(x, gamma_val), 0, 1)
    lw = 2.5 if gamma_val == 1.0 else 2.0
    ax.plot(x, y, color=color, linewidth=lw, label=label, zorder=2)

# Annotations
ax.annotate("Shadow lift\n(logarithmic)", xy=(0.2, 0.55), fontsize=9,
            color='#66ccff', ha='center', style='italic')
ax.annotate("Shadow crush\n(exponential)", xy=(0.55, 0.18), fontsize=9,
            color='#ff9944', ha='center', style='italic')

ax.set_xlabel("Input Brightness", fontsize=12, color='#cccccc', labelpad=10)
ax.set_ylabel("Output Brightness", fontsize=12, color='#cccccc', labelpad=10)
ax.set_title("Gamma Transfer Curves", fontsize=14, color='#ffffff', pad=15, fontweight='bold')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.tick_params(colors='#888888', labelsize=9)
for spine in ax.spines.values():
    spine.set_color('#444444')

ax.legend(fontsize=9, loc='lower right', framealpha=0.3,
          facecolor='#1a1a2e', edgecolor='#444444', labelcolor='#cccccc')

ax.grid(True, alpha=0.15, color='#888888')

plt.tight_layout()
plt.savefig(out_path, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
print(f"Saved: {out_path}")
