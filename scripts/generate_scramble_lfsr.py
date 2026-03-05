"""
Generate LFSR (Linear Feedback Shift Register) diagram for the Scramble program guide.
Shows a 16-bit shift register with XOR feedback taps and the output sequence concept.
Output: static/img/instruments/videomancer/scramble/scramble_lfsr_diagram.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

out_dir = Path(__file__).resolve().parent.parent / "static" / "img" / "instruments" / "videomancer" / "scramble"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "scramble_lfsr_diagram.png"

fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 6.5), facecolor='#1a1a2e',
                                      gridspec_kw={'height_ratios': [1.2, 1]})

# ============ TOP: LFSR Register Diagram ============
ax = ax_top
ax.set_facecolor('#1a1a2e')
ax.set_xlim(-1, 18)
ax.set_ylim(-1.5, 3)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Draw 16 register cells
cell_w = 0.85
cell_h = 0.85
y_reg = 1.0
tap_bits = {4, 13, 15, 16}  # Taps at positions 16, 15, 13, 4
example_state = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1]

for i in range(16):
    x = i + 0.5
    bit_num = 16 - i  # Bit 16 on the left, bit 1 on the right
    is_tap = bit_num in tap_bits
    
    # Cell rectangle
    ec = '#ff9944' if is_tap else '#555555'
    fc = '#2a2a4e' if not is_tap else '#332211'
    rect = mpatches.FancyBboxPatch((x - cell_w/2, y_reg - cell_h/2), cell_w, cell_h,
                                    boxstyle="round,pad=0.05",
                                    facecolor=fc, edgecolor=ec, linewidth=2 if is_tap else 1)
    ax.add_patch(rect)
    
    # Bit value
    ax.text(x, y_reg, str(example_state[i]), ha='center', va='center',
            fontsize=12, color='#ffffff', fontweight='bold', fontfamily='monospace')
    
    # Bit number label
    color = '#ff9944' if is_tap else '#888888'
    ax.text(x, y_reg + 0.65, f"b{bit_num}", ha='center', va='center',
            fontsize=7, color=color)

# Shift arrow across the bottom
ax.annotate('', xy=(16.3, y_reg - 0.65), xytext=(0.2, y_reg - 0.65),
            arrowprops=dict(arrowstyle='->', color='#66ccff', lw=1.5))
ax.text(8.5, y_reg - 0.9, "Shift direction →", ha='center', fontsize=8, color='#66ccff')

# XOR feedback paths (from taps back to input)
tap_positions = [16 - (t - 1) + 0.5 for t in [16, 15, 13, 4]]  # x positions of taps
# Draw lines down from taps to a feedback bus
feedback_y = y_reg + 1.2
for tp_x in tap_positions:
    ax.plot([tp_x, tp_x], [y_reg + 0.5, feedback_y], color='#ff9944', linewidth=1.5, linestyle='-')

# Horizontal feedback bus
ax.plot([min(tap_positions), max(tap_positions)], [feedback_y, feedback_y],
        color='#ff9944', linewidth=1.5)

# XOR symbol (⊕) at the junction
xor_x = max(tap_positions)
ax.text(xor_x + 0.5, feedback_y, "⊕", ha='center', va='center',
        fontsize=16, color='#ff9944', fontweight='bold')

# Arrow from XOR back to bit 16 (leftmost)
ax.annotate('', xy=(0.5, y_reg + 0.5), xytext=(0.5, feedback_y),
            arrowprops=dict(arrowstyle='->', color='#ff9944', lw=1.5))

# Labels
ax.text(8.5, 2.7, "16-Bit LFSR — Taps at bits 16, 15, 13, 4",
        ha='center', fontsize=12, color='#ffffff', fontweight='bold')
ax.text(17.2, y_reg, "→ Output\n(cut point)", ha='left', va='center',
        fontsize=9, color='#66ccff', fontweight='bold')

# Legend marker
ax.add_patch(mpatches.FancyBboxPatch((0.0, -1.2), 0.4, 0.4,
             boxstyle="round,pad=0.05", facecolor='#332211', edgecolor='#ff9944', linewidth=2))
ax.text(0.7, -1.0, "= Feedback tap", fontsize=8, color='#ff9944', va='center')

# ============ BOTTOM: LFSR Output Sequence ============
ax = ax_bot
ax.set_facecolor('#1a1a2e')

# Simulate a simple LFSR to show pseudo-random output
def lfsr_16(seed, n_steps):
    """16-bit LFSR with taps at 16, 15, 13, 4"""
    state = seed & 0xFFFF
    if state == 0:
        state = 1
    outputs = []
    for _ in range(n_steps):
        outputs.append(state)
        # XOR taps at bits 16, 15, 13, 4 (1-indexed)
        bit = ((state >> 0) ^ (state >> 1) ^ (state >> 3) ^ (state >> 12)) & 1
        state = (state >> 1) | (bit << 15)
    return outputs

n_lines = 64
seed_a = 0xACE1
seed_b = 0x1234

seq_a = lfsr_16(seed_a, n_lines)
seq_b = lfsr_16(seed_b, n_lines)

# Normalize to 0-1023 (10-bit cut point range)
seq_a_norm = [v & 0x3FF for v in seq_a]
seq_b_norm = [v & 0x3FF for v in seq_b]

lines = np.arange(n_lines)
ax.bar(lines - 0.2, seq_a_norm, width=0.35, color='#66ccff', alpha=0.7, label=f'Seed A (0x{seed_a:04X})')
ax.bar(lines + 0.2, seq_b_norm, width=0.35, color='#ff9944', alpha=0.7, label=f'Seed B (0x{seed_b:04X})')

ax.set_xlabel("Scanline Number", fontsize=10, color='#cccccc', labelpad=8)
ax.set_ylabel("Cut Point (px)", fontsize=10, color='#cccccc', labelpad=8)
ax.set_title("Per-Line Cut Points from Different Seeds", fontsize=11, color='#cccccc', pad=8)
ax.set_xlim(-1, n_lines)
ax.set_ylim(0, 1024)
ax.tick_params(colors='#888888', labelsize=8)
for spine in ax.spines.values():
    spine.set_color('#444444')
ax.legend(fontsize=9, loc='upper right', framealpha=0.3,
          facecolor='#1a1a2e', edgecolor='#444444', labelcolor='#cccccc')
ax.grid(True, alpha=0.1, color='#888888', axis='y')

fig.suptitle("LFSR Pseudo-Random Sequence Generator", fontsize=14,
             color='#ffffff', fontweight='bold', y=0.99)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(out_path, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
print(f"Saved: {out_path}")
