"""
Generate edge mode waveforms illustration for the Lumarian program guide.
Shows all 8 edge modes produced by the 3-bit switch selector (Switches 9, 10, 11).
Output: static/img/instruments/videomancer/lumarian/lumarian_edge_modes.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

out_dir = Path(__file__).resolve().parent.parent / "static" / "img" / "instruments" / "videomancer" / "lumarian"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "lumarian_edge_modes.png"

# Simulate a bipolar edge signal (derivative of a step edge, like bright→dark)
t = np.linspace(-2, 2, 512)
# Raw bipolar edge: positive lobe followed by negative lobe
raw_edge = np.exp(-((t - 0.3)**2) / 0.08) - np.exp(-((t + 0.3)**2) / 0.08)

def apply_mode(signal, invert, rectify, select):
    """
    3-bit mode selector:
    - invert (bit 0, sw9):  half-wave rectification (clip negative to zero)
    - rectify (bit 1, sw10): negate signal
    - select (bit 2, sw11):  full-wave rectification (absolute value)
    """
    s = signal.copy()
    if rectify:
        s = -s
    if invert:
        s = np.maximum(s, 0)  # half-wave rectify
    if select:
        s = np.abs(s)  # full-wave rectify
    return s

modes = []
for i in range(8):
    inv = bool(i & 1)   # bit 0 = switch 9 (Edge Invert)
    rec = bool(i & 2)   # bit 1 = switch 10 (Edge Rectify)
    sel = bool(i & 4)   # bit 2 = switch 11 (Edge Select)
    label_parts = []
    label_parts.append(f"Sw9={'On' if inv else 'Off'}")
    label_parts.append(f"Sw10={'On' if rec else 'Off'}")
    label_parts.append(f"Sw11={'On' if sel else 'Off'}")
    label = f"Mode {i}: {', '.join(label_parts)}"
    result = apply_mode(raw_edge, inv, rec, sel)
    modes.append((label, result))

# Color palette
colors = ['#66ccff', '#33aadd', '#ff9944', '#ffcc44',
          '#88dd66', '#44bb88', '#dd66aa', '#cc44ff']

fig, axes = plt.subplots(4, 2, figsize=(10, 10), facecolor='#1a1a2e')

for idx, (ax, (label, waveform)) in enumerate(zip(axes.flat, modes)):
    ax.set_facecolor('#1a1a2e')
    # Zero reference line
    ax.axhline(0, color='#555555', linewidth=0.8, linestyle='--')
    # Waveform
    ax.fill_between(t, 0, waveform, alpha=0.25, color=colors[idx])
    ax.plot(t, waveform, color=colors[idx], linewidth=2)
    ax.set_title(label, fontsize=9, color='#cccccc', pad=5)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#333333')

fig.suptitle("8 Edge Modes from Switches 9, 10, 11",
             fontsize=14, color='#ffffff', fontweight='bold', y=0.98)

# Add a small legend explaining the switches
fig.text(0.5, 0.01,
         "Sw 9 = Edge Invert (half-wave rectify)  ·  Sw 10 = Edge Rectify (negate)  ·  Sw 11 = Edge Select (full-wave rectify / abs)",
         ha='center', fontsize=9, color='#999999', style='italic')

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig(out_path, dpi=180, facecolor='#1a1a2e', bbox_inches='tight')
print(f"Saved: {out_path}")
