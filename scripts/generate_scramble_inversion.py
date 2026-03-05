"""
Generate inversion zones illustration for the Scramble program guide.
Shows alternating bands of normal and inverted video at different period settings.
Output: static/img/instruments/videomancer/scramble/scramble_inversion_zones.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

out_dir = Path(__file__).resolve().parent.parent / "static" / "img" / "instruments" / "videomancer" / "scramble"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "scramble_inversion_zones.png"

# Create a synthetic gradient image (simulate a video frame)
width = 256
height = 256

# Make a gradient with some structure
x_coords = np.linspace(0, 1, width)
y_coords = np.linspace(0, 1, height)
xx, yy = np.meshgrid(x_coords, y_coords)

# A radial gradient with some wave pattern
r = np.sqrt((xx - 0.5)**2 + (yy - 0.5)**2)
base_image = 0.5 + 0.4 * np.cos(r * 12) * np.cos(xx * 8 + yy * 6)
base_image = np.clip(base_image, 0, 1)

# Inversion periods: steps 0-7 select line group sizes (0=off, 1=2, 2=4, 3=8, 4=16, 5=32, 6=64, 7=128)
periods = [
    (0, "Period 0: Off"),
    (1, "Period 1: 2-line groups"),
    (2, "Period 2: 4-line groups"),
    (3, "Period 3: 8-line groups"),
    (4, "Period 4: 16-line groups"),
    (5, "Period 5: 32-line groups"),
    (6, "Period 6: 64-line groups"),
    (7, "Period 7: 128-line groups"),
]

fig, axes = plt.subplots(2, 4, figsize=(12, 7), facecolor='#1a1a2e')

for ax, (step, label) in zip(axes.flat, periods):
    ax.set_facecolor('#1a1a2e')
    
    if step == 0:
        # No inversion
        display = base_image
    else:
        group_size = 2 ** step  # 2, 4, 8, 16, 32, 64, 128
        display = base_image.copy()
        for row in range(height):
            # Which group does this line belong to?
            group_index = row // group_size
            if group_index % 2 == 1:
                # Invert this line
                display[row, :] = 1.0 - display[row, :]
    
    ax.imshow(display, cmap='gray', aspect='equal', vmin=0, vmax=1)
    ax.set_title(label, fontsize=8.5, color='#cccccc', pad=5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#333333')
    
    # Add colored bar on right edge showing inversion zones
    if step > 0:
        group_size = 2 ** step
        for row in range(0, height, group_size):
            group_index = row // group_size
            color = '#ff4444' if group_index % 2 == 1 else '#44ff44'
            rect = mpatches.Rectangle((width - 8, row), 8, min(group_size, height - row),
                                       linewidth=0, facecolor=color, alpha=0.6)
            ax.add_patch(rect)

fig.suptitle("Video Inversion Zones — Alternating Normal / Inverted Line Groups",
             fontsize=13, color='#ffffff', fontweight='bold', y=0.98)

# Legend
fig.text(0.5, 0.01,
         "Green bars = normal video  ·  Red bars = inverted video  ·  Each step doubles the group size",
         ha='center', fontsize=9, color='#999999', style='italic')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(out_path, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
print(f"Saved: {out_path}")
