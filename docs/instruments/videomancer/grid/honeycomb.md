---
draft: true
sidebar_position: 139
slug: /instruments/videomancer/honeycomb
title: "Honeycomb"
image: /img/instruments/videomancer/honeycomb/honeycomb_hero.png
description: "Honeycomb draws a hexagonal grid directly onto the video output — bright lines marking cell boundaries over either a dark background or the incoming video signal."
---

import honeycomb_hero from '/img/instruments/videomancer/honeycomb/honeycomb_hero.png';
import honeycomb_animation from '/img/instruments/videomancer/honeycomb/honeycomb_animation.gif';
import honeycomb_control_panel from '/img/instruments/videomancer/honeycomb/honeycomb_control_panel.png';
import honeycomb_exercise1_result from '/img/instruments/videomancer/honeycomb/honeycomb_exercise1_result.gif';
import honeycomb_exercise2_result from '/img/instruments/videomancer/honeycomb/honeycomb_exercise2_result.gif';
import honeycomb_exercise3_result from '/img/instruments/videomancer/honeycomb/honeycomb_exercise3_result.gif';

# Honeycomb

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={honeycomb_hero} alt="Honeycomb hero image"/>
*Honeycomb generating a luminous hexagonal lattice overlaid on a dark background with colored cell edges.*
<img src={honeycomb_animation} alt="Honeycomb animated output"/>
*Honeycomb output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Honeycomb draws a hexagonal grid directly onto the video output — bright lines marking cell boundaries over either a dark background or the incoming video signal. Every parameter of the grid is adjustable in real time: cell size, line thickness, edge brightness, and edge color. The result ranges from fine honeycomb meshes to bold stained-glass partitions, all generated entirely within the FPGA with zero frame buffer memory.

The name refers to the natural hexagonal structure of a bee's honeycomb — one of the most efficient tessellations found in nature. In geometry, a regular hexagonal tiling covers a plane with the least total perimeter for a given cell area. Honeycomb approximates this tiling using a rectangular grid with alternating row offsets, producing a pattern that reads as hexagonal even though the underlying math is simpler than true hex geometry.

At conservative settings — small cells, thin lines, moderate brightness — Honeycomb produces a subtle overlay grid useful for calibration, framing, or compositing reference. At extreme settings — large cells, thick lines, full color — it generates bold graphic structures that can serve as standalone visual content or as a keying layer in a larger video chain.

---

## Background

### Hexagonal Tessellations

A **tessellation** is a pattern of shapes that tiles a plane without gaps or overlaps. Squares and triangles tessellate trivially, but hexagons are unique among regular polygons: they achieve the maximum area-to-perimeter ratio while still tiling perfectly. This property is why bees build hexagonal cells — it minimizes the wax needed for a given volume of honey storage. In video synthesis, hexagonal grids create a more organic, less "digital" appearance than square grids because the eye is less accustomed to seeing hex patterns on screens.

Honeycomb approximates a hexagonal grid by offsetting every other row of a rectangular cell grid by half a cell width. This creates the characteristic zigzag edge pattern of a hex lattice without requiring trigonometric coordinate transforms. The approximation is visually convincing, especially at smaller cell sizes where the rectangular cell proportions are less noticeable.

### Edge Detection in Grid Patterns

In a tiled grid, **edge pixels** are those that fall near the boundary between adjacent cells. Honeycomb identifies edges by computing each pixel's local position within its cell and checking whether that position is within the line width of the cell boundary. If the pixel's local X coordinate or local Y coordinate is less than the line width, it is classified as an edge. This is a simple modular-arithmetic test — no convolution kernels or gradient operators are needed because the grid geometry is known exactly.

### Four-Quadrant Hue Mapping

When color mode is enabled, Honeycomb maps the Color knob to a hue by assigning the register value directly to the U channel and its complement (1023 minus the value) to the V channel. This creates a **four-quadrant hue sweep**: as the knob travels from 0% to 100%, the output moves through cyan, green, magenta, and yellow in the YUV color space. The mapping is computationally trivial — a single subtraction — but produces a full hue rotation because the U and V axes of YUV span the complete color plane.

### Synthesis vs. Processing Hybrid

Although Honeycomb is classified as a synthesis program (Grid category), it has a unique hybrid behavior. When the Fill toggle is enabled, non-edge pixels pass the incoming video signal through unchanged — the grid lines are overlaid on the live input. When Fill is off, non-edge pixels are replaced with a near-black background, making Honeycomb a pure pattern generator. This dual personality means the program can function as both a standalone graphic source and a compositing overlay tool.


---

## Signal Flow

```
Video Input (YUV 4:4:4)
│
├── Timing Detection ───────────────────────────────────────────
│   ├─ hsync/vsync falling-edge detect (manual, not video_timing_generator)
│   ├─ X counter (pixel position within scanline)
│   └─ Y counter (scanline number within frame)
│
├── Hex Grid Computation ───────────────────────────────────────
│   ├─ 1. Cell width         (cell_size upper bits + 4 → range ~4-35 pixels)
│   ├─ 2. Row offset         (odd rows shifted by half cell width)
│   ├─ 3. Local position     (pixel X/Y modulo cell size, 6-bit wraparound)
│   └─ 4. Edge test          (local_x < line_width OR local_y < line_width)
│
├── Pixel Assignment ───────────────────────────────────────────
│   ├─ Edge pixel:
│   │   ├─ Y = Brightness (pot 3)
│   │   ├─ U = Color (pot 4) if Color enabled, else 512
│   │   └─ V = 1023 - Color if Color enabled, else 512
│   │
│   └─ Non-edge pixel:
│       ├─ Fill On:  pass-through input Y/U/V
│       └─ Fill Off: Y=64, U=512, V=512 (near-black)
│
├── Interpolator Mix ───────────────────────────────────────────
│   └─ 3× interpolator_u: crossfade between delayed input and processed output
│
├── Sync / Data Delay (8 clocks) ───────────────────────────────
│   └─ Shift registers for hsync, vsync, field, Y, U, V
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed (mix output) or delayed input
```

Honeycomb uses manual sync detection — falling-edge detection on hsync_n and vsync_n — rather than the shared `video_timing_generator` entity. This means the X and Y counters free-run from sync edges without active-video gating. The hex grid approximation works by adding half the cell width to the X coordinate on odd-numbered rows, creating the characteristic offset that makes rectangular cells read as hexagonal. The edge test operates on 6-bit local coordinates (modulo 64), and the line width is extracted from the upper 3 bits of the Line Width register, giving only 8 discrete thickness levels (0–7 pixels). Several registered parameters — Fill amount (Knob 5), Speed (Knob 6), Animate (Toggle 9), and 3D Effect (Toggle 10) — are wired to signals but have no effect on the output in the current implementation.

---

## Parameter Reference

<img src={honeycomb_control_panel} alt="Videomancer front panel with Honeycomb loaded"/>
*Videomancer's front panel with Honeycomb active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the width of each hexagonal cell. The register value is right-shifted by 5 bits and offset by 4, producing an effective cell width range of approximately 4 to 35 pixels. At low values the grid is fine and dense — hundreds of tiny cells fill the screen. At high values the cells become large enough that only a handful are visible, creating bold graphic partitions. Because the hex offset is half the cell width, changing cell size also changes the apparent regularity of the hexagonal pattern.

---

#### Knob 2 — Line Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the thickness of the grid lines that define cell boundaries. Only the upper 3 bits of the register are used, giving 8 discrete line width steps from 0 (no visible lines) to 7 pixels wide. At zero, no edge pixels are generated and the output is entirely fill (video or dark). At maximum, the lines are thick enough to dominate the pattern, leaving only small non-edge regions inside each cell. The stepped nature of this control means fine adjustments produce no change until the next bit boundary is crossed.

---

#### Knob 3 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Sets the luminance of edge pixels — the brightness of the grid lines themselves. At 0% the lines are black and invisible against a dark background, useful only when Fill mode passes video through the cell interiors. At 100% the lines are maximum white. This control has no effect on non-edge pixels; cell interiors are always either video pass-through or near-black depending on the Fill toggle.

---

#### Knob 4 — Color
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the hue of the grid lines when Color mode is enabled (Toggle 8 = RGB). The register value is assigned directly to the U channel of edge pixels, and its complement (1023 minus the value) is assigned to V. This creates a four-quadrant hue sweep through the YUV color plane as the knob travels from minimum to maximum. When Color mode is off (Mono), this control has no effect — edge pixels use neutral chroma (U=512, V=512), producing a monochrome grid.

---

#### Knob 5 — Fill
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Labeled "Fill" and registered as `s_fill_amt`, but this parameter is not connected to any processing logic in the current VHDL implementation. The signal is latched from the register on every clock cycle but never read by any output assignment. Adjusting this knob produces no visible change. It may be reserved for a future feature such as variable fill opacity.

---

#### Knob 6 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Labeled "Speed" and registered as `s_speed`, this parameter is intended to control animation rate. A frame counter increments on each vsync when the Animate toggle is enabled, but the counter value is never used in any address or output computation. Adjusting this knob produces no visible change in the current implementation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Fill** | Off | On |
| **8 — Color** | Mono | RGB |
| **9 — Animate** | Off | On |
| **10 — 3D Effect** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options, but two of them (Animate and 3D Effect) are non-functional in the current VHDL. Fill (Toggle 7) and Color (Toggle 8) are the primary creative switches. Bypass (Toggle 11) is a standard signal routing switch. The toggles do not form a combined mode selector — each bit is decoded independently from `registers_in(6)`.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry crossfade between the delayed input signal and the processed grid output via three `interpolator_u` instances (one per Y/U/V channel). At 0% (register 0), the output is the delayed input — no grid visible. At 100% (register 1023), the output is fully the processed grid signal. Intermediate values create a transparent overlay effect where the grid lines are semi-visible over the input video, regardless of the Fill toggle setting.

---

## Guided Exercises

These exercises progress from a basic monochrome grid to colored overlays and hybrid compositing, exploring each functional parameter of the hexagonal pattern generator.

### Exercise 1: Basic Hex Grid

<img src={honeycomb_exercise1_result} alt="Basic Hex Grid result"/>
*Basic Hex Grid — simulated result across source images.*
**Objective**: Learn how cell size and line width define the hexagonal lattice structure.

1. **Default grid**: With all controls at default, observe the hexagonal grid pattern on a dark background. Note how odd-numbered scanline rows are offset to create the hex appearance.
2. **Cell size sweep**: Slowly turn Cell Size from minimum to maximum. Watch the grid transition from a fine mesh to large bold partitions. Count the approximate number of cells visible at each extreme.
3. **Line width steps**: Starting with Cell Size at ~40%, sweep Line Width from 0% to 100%. Notice the stepped behavior — the line thickness changes in discrete jumps because only 3 bits of the register are used.
4. **No lines**: Set Line Width to 0%. All pixels become non-edge, and with Fill Off, the screen goes dark. This confirms that the grid is purely edge-detection-driven.
5. **Maximum coverage**: Set Line Width to 100% and Cell Size to minimum. The thick lines and small cells fill most of the screen with edge pixels, leaving only tiny dark gaps.

**Key concepts**: Hexagonal approximation via row offset, 6-bit modular coordinate system, 3-bit quantized line width, edge detection as less-than comparison

---

### Exercise 2: Colored Overlay Grid

<img src={honeycomb_exercise2_result} alt="Colored Overlay Grid result"/>
*Colored Overlay Grid — simulated result across source images.*
**Objective**: Explore color assignment and video fill to create a colored hex overlay on live video.

1. **Enable color**: Set Color toggle to RGB. The grid lines change from white to a hue determined by the Color knob.
2. **Hue sweep**: Slowly turn the Color knob from 0% to 100%. Watch the grid lines cycle through cyan, green, magenta, and yellow — the four quadrants of the YUV color space.
3. **Fill mode**: Enable the Fill toggle. Cell interiors now show the incoming video signal, with colored hex lines overlaid on top.
4. **Brightness adjustment**: Reduce Brightness to ~30%. The colored lines become darker, allowing more of the fill video to dominate the composition.
5. **Mix blend**: Lower the Mix fader to ~50%. The grid becomes semi-transparent, blending with the input signal for a subtle overlay effect.

**Key concepts**: Four-quadrant YUV hue mapping, U/V complementary assignment, video pass-through fill, wet/dry mix as transparency control

---

### Exercise 3: Bold Graphic Lattice

<img src={honeycomb_exercise3_result} alt="Bold Graphic Lattice result"/>
*Bold Graphic Lattice — simulated result across source images.*
**Objective**: Push the grid to maximum visual impact with large cells, thick lines, full brightness, and saturated color.

1. **Large cells**: Set Cell Size to ~90%. Only a few cells span the screen, creating bold geometric partitions.
2. **Thick lines**: Set Line Width to 100%. The lines dominate, leaving small island-like cell interiors.
3. **Full brightness and color**: Set Brightness to 100%, enable RGB Color, and set the Color knob to ~25% for a vivid cyan-green hue.
4. **Dark background**: Ensure Fill is Off. The large bright colored lattice stands out against near-black cell interiors.
5. **Feed to another program**: Route Honeycomb's output into a downstream processing program (e.g., a feedback loop or color rotator). The strong geometric structure creates striking recursive patterns.
6. **Mix comparison**: Sweep the Mix fader while observing. At low Mix values, the grid fades into the background input, demonstrating the interpolator crossfade.

**Key concepts**: Grid as standalone graphic source, geometric structure as compositional element, interpolator wet/dry crossfade behavior, downstream chaining

---


## Tips

- **Row offset is the key**: The hexagonal appearance comes entirely from shifting every other row by half a cell width. Without this offset, Honeycomb would produce a rectangular grid.
- **Line Width is quantized**: Only 3 bits control line thickness (8 discrete steps). Fine adjustments to the knob may produce no visible change until the next step boundary.
- **Fill toggle changes the role**: With Fill Off, Honeycomb is a pattern generator. With Fill On, it becomes an overlay tool. This makes it useful in two fundamentally different positions within a video chain.
- **Color knob at 50% = neutral**: The midpoint of the Color knob produces U=512, V=512, which is achromatic. Move away from center in either direction to introduce color.
- **Four parameters are non-functional**: Fill amount (Knob 5), Speed (Knob 6), Animate (Toggle 9), and 3D Effect (Toggle 10) are registered but produce no output change. They appear to be reserved for future development.
- **Mix as transparency**: The Mix fader controls the interpolator crossfade. At intermediate values, the grid becomes a semi-transparent overlay regardless of Fill mode, which can be useful for subtle reference grids.
- **Downstream chaining**: Honeycomb's bold geometric output is particularly effective as input to feedback, rotation, or color processing programs. The high-contrast edge structure provides strong visual anchors for recursive effects.
- **Bypass for A/B**: Toggle 11 instantly compares the processed grid against the raw input. Useful for checking the impact of the overlay on the source material.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation BT.601; the standard color matrix used for converting between RGB and YUV in standard-definition video. Videomancer uses BT.601 coefficients throughout. |
| **Edge pixel** | A pixel whose local coordinates within a grid cell fall within the line width boundary, classified as part of the grid line structure. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable integrated circuit that executes the grid generation and video processing pipeline. |
| **Hue** | The attribute of color that distinguishes red from blue, green from yellow, etc. In YUV, hue is determined by the angle formed by the U and V components. |
| **Interpolator** | A linear crossfade module (`interpolator_u`) that blends two signals based on a mix parameter. Used here for the wet/dry output mix. |
| **Modular arithmetic** | Arithmetic where values wrap around upon reaching a fixed modulus. Used here for computing local pixel position within a cell (6-bit wraparound). |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. Honeycomb uses an 8-clock pipeline. |
| **Tessellation** | A pattern that tiles a plane without gaps or overlaps. Regular hexagons form one of three regular tessellations (along with squares and equilateral triangles). |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V). Honeycomb generates patterns directly in YUV and applies color by manipulating U and V values. |

---
