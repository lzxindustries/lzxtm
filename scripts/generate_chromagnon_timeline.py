"""
Generate a Chromagnon production timeline graphic matching the docs.lzxindustries.net visual style.
Dark background, orange accent (#d6770a), clean sans-serif typography.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from pathlib import Path

# Output path
OUTPUT = Path(__file__).parent.parent / "blog" / "2026-03-05-chromagnon-building-it-right" / "chromagnon-timeline-graphic.png"

# === Color scheme matching docs.lzxindustries.net dark theme ===
BG_COLOR = '#1b1b1d'         # Docusaurus dark bg (--ifm-color-gray-900 approx)
TEXT_COLOR = '#e3e3e3'        # Light gray text
ACCENT = '#d6770a'            # LZX orange primary
ACCENT_LIGHT = '#f5982e'      # Lighter orange for highlights
MUTED = '#666666'             # Muted gray for secondary elements
LINE_COLOR = '#444444'        # Subtle grid/connector lines
DONE_COLOR = '#3a8a3a'        # Green for completed items
PROGRESS_COLOR = '#d6770a'    # Orange for in-progress
FUTURE_COLOR = '#555555'      # Gray for future items
MILESTONE_BG = '#2a2a2d'      # Slightly lighter bg for milestone boxes

# === Milestones ===
milestones = [
    ("MAR 12", "Videomancer\nFirmware Update", "done"),
    ("MID-MAR", "Full Chromagnon\nFocus", "done"),
    ("EARLY APR", "RevI Board\nDesign Complete", "progress"),
    ("APR", "Firmware\nIntegration", "future"),
    ("LATE APR–\nEARLY MAY", "RevI Prototype\nFabricated", "future"),
    ("MAY–JUN", "Hardware\nValidation", "future"),
    ("JUN", "Production-\nReady", "milestone"),
    ("JUN–JUL", "Production\nOrdering", "future"),
    ("AUG", "Ship\nUnit #1", "milestone"),
    ("SEP+", "Fulfillment\nAt Scale", "future"),
]

# === Figure setup ===
fig_width = 10
fig_height = 4.5
fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(-0.5, len(milestones) - 0.5)
ax.set_ylim(-1.8, 2.2)
ax.axis('off')

# === Title ===
ax.text(len(milestones) / 2 - 0.5, 2.0, 'CHROMAGNON PRODUCTION TIMELINE',
        ha='center', va='center', fontsize=16, fontweight='bold',
        color=TEXT_COLOR, fontfamily='sans-serif')

# === Timeline backbone ===
backbone_y = 0.3
ax.plot([-0.3, len(milestones) - 0.7], [backbone_y, backbone_y],
        color=LINE_COLOR, linewidth=2.5, solid_capstyle='round', zorder=1)

# === Draw colored progress line over backbone ===
# Progress covers first 2.5 items (done through early progress)
progress_end = 2.3
ax.plot([-0.3, progress_end], [backbone_y, backbone_y],
        color=ACCENT, linewidth=3, solid_capstyle='round', zorder=2)

# === Draw milestones ===
for i, (date, label, status) in enumerate(milestones):
    x = i

    # Node color based on status
    if status == 'done':
        node_color = DONE_COLOR
        node_edge = DONE_COLOR
        node_size = 12
    elif status == 'progress':
        node_color = ACCENT
        node_edge = ACCENT_LIGHT
        node_size = 14
    elif status == 'milestone':
        node_color = ACCENT
        node_edge = ACCENT_LIGHT
        node_size = 16
    else:
        node_color = FUTURE_COLOR
        node_edge = MUTED
        node_size = 10

    # Node circle
    ax.plot(x, backbone_y, 'o', markersize=node_size, color=node_color,
            markeredgecolor=node_edge, markeredgewidth=1.5, zorder=3)

    # Inner dot for milestones
    if status == 'milestone':
        ax.plot(x, backbone_y, 'o', markersize=6, color=BG_COLOR, zorder=4)

    # Date label (below line)
    date_color = ACCENT_LIGHT if status == 'milestone' else (TEXT_COLOR if status in ('done', 'progress') else MUTED)
    ax.text(x, backbone_y - 0.35, date, ha='center', va='top',
            fontsize=7.5, fontweight='bold', color=date_color,
            fontfamily='sans-serif')

    # Description label (above line)
    label_color = TEXT_COLOR if status in ('done', 'progress', 'milestone') else '#999999'
    label_weight = 'bold' if status == 'milestone' else 'normal'
    ax.text(x, backbone_y + 0.45, label, ha='center', va='bottom',
            fontsize=8, fontweight=label_weight, color=label_color,
            fontfamily='sans-serif', linespacing=1.3)

# === Legend ===
legend_y = -1.5
legend_items = [
    (DONE_COLOR, "Complete"),
    (ACCENT, "In Progress"),
    (FUTURE_COLOR, "Upcoming"),
    (ACCENT, "Key Milestone (◉)"),
]
legend_start = len(milestones) / 2 - 2.5
for j, (color, text) in enumerate(legend_items):
    lx = legend_start + j * 1.8
    if text.startswith("Key"):
        ax.plot(lx - 0.15, legend_y, 'o', markersize=8, color=color,
                markeredgecolor=ACCENT_LIGHT, markeredgewidth=1, zorder=3)
        ax.plot(lx - 0.15, legend_y, 'o', markersize=3, color=BG_COLOR, zorder=4)
    else:
        ax.plot(lx - 0.15, legend_y, 'o', markersize=8, color=color, zorder=3)
    ax.text(lx + 0.05, legend_y, text, va='center', fontsize=7.5,
            color=TEXT_COLOR, fontfamily='sans-serif')

# === Year label ===
ax.text(len(milestones) - 0.7, -1.5, '2026', ha='right', va='center',
        fontsize=9, color=MUTED, fontfamily='sans-serif', fontstyle='italic')

# === Save ===
plt.tight_layout(pad=0.5)
fig.savefig(OUTPUT, dpi=200, facecolor=BG_COLOR, bbox_inches='tight',
            pad_inches=0.3)
plt.close()
print(f"Saved timeline graphic to {OUTPUT}")
print(f"Size: {OUTPUT.stat().st_size:,} bytes")
