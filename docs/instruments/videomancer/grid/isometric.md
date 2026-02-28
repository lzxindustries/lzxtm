---
draft: true
sidebar_position: 130
slug: /instruments/videomancer/isometric
title: "Isometric"
image: /img/instruments/videomancer/isometric/isometric_hero.png
description: "Program guide for Isometric, a Videomancer grid program for the LZX video synthesizer."
---

import isometric_animation from '/img/instruments/videomancer/isometric/isometric_animation.gif';
import isometric_control_panel from '/img/instruments/videomancer/isometric/isometric_control_panel.png';
import isometric_exercise1_result from '/img/instruments/videomancer/isometric/isometric_exercise1_result.gif';
import isometric_exercise2_result from '/img/instruments/videomancer/isometric/isometric_exercise2_result.gif';
import isometric_exercise3_result from '/img/instruments/videomancer/isometric/isometric_exercise3_result.gif';
import isometric_hero from '/img/instruments/videomancer/isometric/isometric_hero.png';

# Isometric

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={isometric_hero} alt="Isometric hero image"/>
*Isometric projecting a three-axis engineering grid over a video source, the 60-degree diagonal lines transforming the frame into a drafting table.*
<img src={isometric_animation} alt="Isometric animated output"/>
*Isometric output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Engineering drawings have used isometric grids since the early nineteenth century — a projection system where three axes are equally spaced at 120 degrees, creating a visual framework that represents three-dimensional space on a flat surface without the convergence of true perspective. The result is a network of lines at 0°, +60°, and −60° that tile the plane into equilateral parallelograms.

Isometric generates this grid pattern in real time using modular arithmetic on the horizontal and vertical pixel counters. Horizontal lines are detected where the vertical counter falls on a grid boundary. Diagonal lines at ±60° are detected where the sum or difference of the horizontal counter and twice the vertical counter falls on a grid boundary. The approximation of tan(60°) ≈ 2 is a deliberate integer simplification that avoids trigonometric computation entirely while producing a visually convincing isometric lattice. Where any line hits, the program composites a bright overlay onto the source video using additive blending.

Grid spacing is continuously variable across three power-of-two steps, with a density toggle that shifts the entire range between fine (8/16/32 pixels) and coarse (32/64/128 pixels). Horizontal and diagonal line directions can be independently enabled or disabled via threshold controls. Dashed line mode masks out alternating segments using a higher bit of the position counter. A scroll mechanism animates the grid vertically, making the entire lattice slide across the frame.

---

## Background

### Isometric Projection in Technical Drawing

Isometric projection is one of the axonometric projections defined by the geometry of parallel lines. In a true isometric view, the three coordinate axes appear equally foreshortened and are separated by exactly 120°. This makes all three dimensions equally prominent, which is why architects, engineers, and game designers have used isometric grids for over two centuries. The earliest formal description is attributed to Professor William Farish at Cambridge in 1822. Unlike perspective projection, isometric projection preserves parallel lines — two edges that are parallel in three-dimensional space remain parallel in the drawing. This property makes it ideal for technical illustration, where accurate measurement is more important than photographic realism.

### Grid Patterns and Modular Arithmetic

The simplest way to generate a repeating grid in hardware is with a bitmask. If the grid spacing is a power of two — 8, 16, 32, 64, or 128 pixels — then a line occurs wherever the pixel counter ANDed with (spacing − 1) equals zero. This replaces an expensive modulo operation with a single AND gate. The Isometric program uses this technique for all three line directions: horizontal lines test the vertical counter, while diagonal lines test linear combinations of the horizontal and vertical counters. The grid spacing control selects among three power-of-two values, and the density toggle shifts the entire set between a fine and coarse range.

### Line Dashing and Segment Masking

Dashed lines are a fundamental element of technical drawing, used to indicate hidden edges, construction lines, or boundaries. In hardware, dashing is implemented by masking the line hit signal with a higher bit of the position counter. When bit 3 of the counter is high, the line is suppressed; when low, it is drawn. The result is a regular on-off pattern along the line's length. Because the mask bit period is fixed at 16 pixels (2⁴), the dash length is constant regardless of grid spacing — fine grids produce several dashes per cell, while coarse grids may contain only one or two dash segments per cell.

### Additive Compositing

When a grid line is detected, the Isometric program adds the Line Brightness value to the existing source luminance, clamping at maximum (1023). This additive overlay means the grid is always visible regardless of the source content — bright lines appear on top of dark regions, and they push bright regions toward white. The chroma channels pass through unmodified, so the grid lines inherit the color of the underlying video, tinted toward white by the luma addition.

### Scrolling and Animation

The vertical scroll mechanism adds a per-frame offset to the vertical counter before the grid line tests. This shifts all three line directions simultaneously — horizontal lines slide vertically, and diagonal lines shift along their perpendicular axes. The scroll offset accumulates over time, creating continuous motion. The speed is controlled by a register value that is right-shifted by 4 bits per frame, giving a range from 0 to 63 pixels of scroll per frame.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Clock 1: Input Register + Position Counters ────────────────
│   ├─ Y_in, U_in, V_in registered
│   ├─ h_count: horizontal pixel counter
│   ├─ v_count: vertical line counter
│   └─ v_scrolled = v_count + scroll_offset
│
├── Clock 2: Line Test Arithmetic ──────────────────────────────
│   ├─ hit_horiz    = (v_scrolled AND grid_mask) == 0
│   ├─ hit_diag_pos = ((h_count + v_scrolled<<1) AND grid_mask) == 0
│   └─ hit_diag_neg = ((h_count - v_scrolled<<1) AND grid_mask) == 0
│
├── Clock 3: Combine Hits + Dash Mask + Brightness ─────────────
│   ├─ Enable gates: horiz hit gated by h_thresh > 64
│   │                diag hits gated by d_thresh > 64
│   ├─ Dashed mode: mask out hit when position bit 3 = 1
│   └─ overlay_y = line_bright (pre-registered)
│
├── Clock 4: Composite Output ──────────────────────────────────
│   ├─ Line hit: Y = clamp(Y_in + overlay_y, 0, 1023)
│   ├─ No hit:   Y = Y_in
│   └─ U, V = pass-through (unmodified)
│
├── Clocks 5–8: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(delayed_input, composed, mix_amount)
│
└── Output: Y, U, V, sync
```

The critical design choice is the use of bitmask AND operations for grid line detection, which constrains spacing to powers of two but allows the entire line test to be completed in a single clock cycle with minimal logic. The diagonal line approximation (slope ≈ 2 instead of tan(60°) ≈ 1.732) introduces a slight angular error — the diagonals are at approximately 63.4° rather than exactly 60° — but this deviation is visually negligible on a raster display. The horizontal and diagonal enable thresholds act as independent visibility gates: setting a threshold below 64 disables that line direction entirely, allowing selective display of horizontals-only, diagonals-only, or all three directions.

---

## Parameter Reference

<img src={isometric_control_panel} alt="Videomancer front panel with Isometric loaded"/>
*Videomancer's front panel with Isometric active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Grid Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the grid cell size by selecting among three power-of-two spacings. In coarse mode (density toggle off), the range is 32, 64, or 128 pixels. In fine mode (density toggle on), the range shifts to 8, 16, or 32 pixels. The transition between spacing values is abrupt — each third of the pot's range snaps to one of the three spacings. Smaller spacing produces a denser grid with more lines on screen; larger spacing produces a sparser, more architectural grid.

---

#### Knob 2 — Line Br
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the luminance of the grid lines. At 0%, the grid lines are invisible (zero brightness added). At 100%, each grid line adds maximum luma to the source, pushing affected pixels toward peak white. Because the compositing is additive, the effective visual contrast of the grid depends on the source brightness — dark source material shows the grid most clearly, while bright source material may clip to white.

---

#### Knob 3 — Axis Vis
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the horizontal line enable threshold. When the value exceeds 64, horizontal grid lines are drawn. Below 64, horizontal lines are suppressed entirely. This allows you to display only the diagonal lines for a different visual emphasis. The threshold itself does not modulate the line brightness — it acts as a binary gate.

---

#### Knob 4 — Scroll Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the diagonal line enable threshold. Functions identically to the horizontal threshold but gates the two diagonal line directions (both +60° and −60°) simultaneously. Setting this below 64 while keeping the horizontal threshold high produces horizontal-only grid lines. Setting both above 64 produces the full three-axis isometric grid.

---

#### Knob 5 — Rotation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the vertical scroll speed. The register value is right-shifted by 4 bits per frame, giving an effective scroll increment of 0 to 63 pixels per frame. At zero, the grid is stationary. At moderate values, the lattice slides smoothly across the frame. At maximum, the scroll is so fast that the grid appears to shimmer or strobe, creating moiré-like visual effects as the power-of-two spacing interacts with the scroll rate.

---

#### Knob 6 — Opacity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

This control is reserved and currently has no effect on the output. The corresponding VHDL register is not connected to any processing logic. Future firmware revisions may assign functionality to this parameter.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Grid** | Iso | Axono |
| **8 — Axes** | All | XY |
| **9 — Style** | Thin | Heavy |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The three active toggles control grid density range, scroll animation enable, and line dash style. Toggle 10 (Animate) is labeled in the TOML metadata but is not connected in the VHDL — scroll animation is controlled solely by the scroll enable toggle and scroll speed knob. Bypass disables all processing and passes the input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the grid-composited signal and the delayed original input. At 0%, only the original signal passes through. At 100%, the full grid overlay is visible. Intermediate positions blend the two proportionally, allowing subtle grid underlays.

---

## Guided Exercises

These exercises explore the grid engine's range from architectural overlays to animated pattern textures, progressively engaging the scroll, dash, and density controls.

### Exercise 1: Architectural Grid Overlay

<img src={isometric_exercise1_result} alt="Architectural Grid Overlay result"/>
*Architectural Grid Overlay — simulated result across source images.*
**Objective**: Create a clean isometric drafting grid over a video source and explore how spacing and brightness interact.

1. Set Grid Sp to ~50% (64-pixel spacing in coarse mode). Set Line Br to ~60%.
2. Observe the three-axis isometric grid overlaying the source video.
3. Sweep Grid Sp across its range — watch the grid snap between 32, 64, and 128 pixel spacings.
4. Toggle Grid to fine mode — the grid becomes much denser (8/16/32 pixels).
5. Reduce Line Br to ~20% for a subtle underlay, then increase to ~90% for a bold overlay.
6. Set Axis Vis below ~6% to disable horizontal lines. Observe diagonals-only.
7. Set Scroll Sp below ~6% to disable diagonal lines. Re-enable Axis Vis. Observe horizontals-only.

**Key concepts**: Grid spacing snaps to power-of-two values, density toggle shifts the entire range, line directions can be independently gated by threshold controls

---

### Exercise 2: Animated Scrolling Lattice

<img src={isometric_exercise2_result} alt="Animated Scrolling Lattice result"/>
*Animated Scrolling Lattice — simulated result across source images.*
**Objective**: Explore the scroll mechanism and dashed line rendering for dynamic pattern generation.

1. Enable scrolling by toggling Axes to its alternate position (scroll enable).
2. Set Rotation (scroll speed) to ~30%. The grid begins to slide vertically.
3. Increase scroll speed to ~70%. The lattice streams rapidly across the frame.
4. Toggle Style to Heavy (dashed). The continuous lines break into segmented dashes.
5. Experiment with fine grid density + fast scroll + dashed lines — the combination creates a complex, animated texture.
6. Reduce Mix to ~50% to blend the animated grid softly over the source.

**Key concepts**: Scroll offset accumulates per frame, dashing masks alternating 8-pixel segments, the scroll affects all three line directions simultaneously

---

### Exercise 3: Selective Axis Patterns

<img src={isometric_exercise3_result} alt="Selective Axis Patterns result"/>
*Selective Axis Patterns — simulated result across source images.*
**Objective**: Use the threshold controls to isolate individual line directions, creating varied geometric textures.

1. Set both Axis Vis and Scroll Sp to ~50% — full three-axis grid visible.
2. Lower Axis Vis below ~6% — horizontal lines disappear, leaving only diagonals. The pattern becomes a diamond lattice.
3. Restore Axis Vis to ~50%. Lower Scroll Sp below ~6% — diagonals disappear, leaving only horizontals. The pattern becomes pure scan lines.
4. Enable dashed mode with horizontals-only for a halftone screen effect.
5. Switch to fine density mode and compare the visual weight of dense vs. sparse grids.
6. Enable scroll and toggle between diagonals-only and full grid while animated.

**Key concepts**: Threshold controls gate line directions below a minimum value, horizontal-only and diagonal-only modes create fundamentally different visual textures, combining density and dashing produces varied screen patterns

---


## Tips

- **Power-of-two spacing**: Grid spacing snaps to 8, 16, 32, 64, or 128 pixels — there are no intermediate sizes. The knob selects among three values within the coarse or fine range.
- **Threshold as gate**: The Axis Vis and Scroll Sp knobs act as on/off gates for their respective line directions. Values below ~6% disable the direction entirely.
- **Diagonals-only for diamond lattice**: Disable horizontal lines to get a pure diamond/rhombus pattern that reads as a different geometric texture.
- **Dashing for drafting look**: Enable dashed mode for a technical-drawing aesthetic. The 8-pixel dash period is fixed, so it interacts visually with grid spacing.
- **Scroll for animation**: Even low scroll speeds create a sense of depth and motion. Fast scroll with fine grid spacing produces moiré-like optical textures.
- **Additive blend**: The grid is always additive — it never subtracts from the source. Consider this when choosing Line Brightness for bright vs. dark source material.
- **Opacity knob is reserved**: Knob 6 has no current function. Do not expect it to control visual opacity.
- **Feedback routing**: Sending the grid output back to the input creates recursive grid-on-grid interference patterns that shift with each feedback iteration.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Compositing** | A blending mode where the overlay value is added to the source, clamping at maximum; always brightens. |
| **Axonometric** | A family of parallel projections that preserve parallelism, of which isometric is a special case with equal foreshortening on all axes. |
| **Bitmask** | A binary AND operation used to test whether a counter falls on a power-of-two grid boundary; replaces the modulo operator. |
| **BRAM** | Block RAM; dedicated FPGA memory. Isometric uses zero BRAM — all computation is combinational and registered logic. |
| **Dashing** | Breaking a continuous line into alternating drawn and undrawn segments using a higher bit of the position counter. |
| **DDS** | Direct Digital Synthesis; a phase-accumulator technique used here for the scroll offset accumulation. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Grid Mask** | The (spacing − 1) bitmask applied to position counters to detect grid line intersections. |
| **Interpolator** | A linear interpolation module that blends two values using a mix parameter; used for wet/dry crossfade. |
| **Isometric** | A projection where the three coordinate axes are equally spaced at 120°, preserving parallel lines and equal foreshortening. |
| **Moiré** | An interference pattern created when two regular patterns of similar frequency overlap; can occur with fast scroll and fine grid spacing. |
| **Raster** | The horizontal scan-line pattern used to render video; the grid is computed per-pixel as the raster sweeps the frame. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
