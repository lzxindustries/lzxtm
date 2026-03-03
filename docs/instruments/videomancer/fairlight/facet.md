---
draft: true
sidebar_position: 104
slug: /instruments/videomancer/facet
title: "Facet"
image: /img/instruments/videomancer/facet/facet_hero_s1.png
description: "Most video effects blur, bend, or color-grade a continuous image."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import facet_control_panel from '/img/instruments/videomancer/facet/facet_control_panel.png';
import facet_source1_skull from '/img/instruments/videomancer/facet/facet_source1_skull.png';
import facet_source2_cat from '/img/instruments/videomancer/facet/facet_source2_cat.png';
import facet_source3_clouds from '/img/instruments/videomancer/facet/facet_source3_clouds.png';
import facet_source4_pattern from '/img/instruments/videomancer/facet/facet_source4_pattern.png';
import facet_source5_boy from '/img/instruments/videomancer/facet/facet_source5_boy.png';
import facet_source6_wood from '/img/instruments/videomancer/facet/facet_source6_wood.png';
import facet_hero_s1 from '/img/instruments/videomancer/facet/facet_hero_s1.png';
import facet_hero_s2 from '/img/instruments/videomancer/facet/facet_hero_s2.png';
import facet_hero_s3 from '/img/instruments/videomancer/facet/facet_hero_s3.png';
import facet_hero_s4 from '/img/instruments/videomancer/facet/facet_hero_s4.png';
import facet_hero_s5 from '/img/instruments/videomancer/facet/facet_hero_s5.png';
import facet_hero_s6 from '/img/instruments/videomancer/facet/facet_hero_s6.png';
import facet_ex1_s1 from '/img/instruments/videomancer/facet/facet_ex1_s1.png';
import facet_ex1_s2 from '/img/instruments/videomancer/facet/facet_ex1_s2.png';
import facet_ex1_s3 from '/img/instruments/videomancer/facet/facet_ex1_s3.png';
import facet_ex1_s4 from '/img/instruments/videomancer/facet/facet_ex1_s4.png';
import facet_ex1_s5 from '/img/instruments/videomancer/facet/facet_ex1_s5.png';
import facet_ex1_s6 from '/img/instruments/videomancer/facet/facet_ex1_s6.png';
import facet_ex2_s1 from '/img/instruments/videomancer/facet/facet_ex2_s1.png';
import facet_ex2_s2 from '/img/instruments/videomancer/facet/facet_ex2_s2.png';
import facet_ex2_s3 from '/img/instruments/videomancer/facet/facet_ex2_s3.png';
import facet_ex2_s4 from '/img/instruments/videomancer/facet/facet_ex2_s4.png';
import facet_ex2_s5 from '/img/instruments/videomancer/facet/facet_ex2_s5.png';
import facet_ex2_s6 from '/img/instruments/videomancer/facet/facet_ex2_s6.png';
import facet_ex3_s1 from '/img/instruments/videomancer/facet/facet_ex3_s1.png';
import facet_ex3_s2 from '/img/instruments/videomancer/facet/facet_ex3_s2.png';
import facet_ex3_s3 from '/img/instruments/videomancer/facet/facet_ex3_s3.png';
import facet_ex3_s4 from '/img/instruments/videomancer/facet/facet_ex3_s4.png';
import facet_ex3_s5 from '/img/instruments/videomancer/facet/facet_ex3_s5.png';
import facet_ex3_s6 from '/img/instruments/videomancer/facet/facet_ex3_s6.png';

# Facet

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: facet_source1_skull, after: facet_hero_s1 },
    { label: "Cat", before: facet_source2_cat, after: facet_hero_s2 },
    { label: "Clouds", before: facet_source3_clouds, after: facet_hero_s3 },
    { label: "Pattern", before: facet_source4_pattern, after: facet_hero_s4 },
    { label: "Boy", before: facet_source5_boy, after: facet_hero_s5 },
    { label: "Wood", before: facet_source6_wood, after: facet_hero_s6 },
  ]}
/>
*Facet dividing a video frame into flat-shaded crystal cells with black edge outlines, creating a stained-glass mosaic effect.*

---

## Overview

Most video effects blur, bend, or color-grade a continuous image. Facet does something more structural — it divides the entire frame into a regular grid of rectangular cells and replaces the contents of each cell with a single, uniform color sampled from the source at the cell's origin. The result looks like a view through a faceted crystal or a leaded stained-glass window: flat panes of color separated by sharp geometric boundaries.

The name comes from the flat, polished surfaces of a cut gemstone. Each cell in Facet's grid acts like one facet of a crystal — reflecting a single point of the scene behind it as a uniform plane of color. At small cell sizes, the effect is a subtle loss of detail, like frosted glass. At large cell sizes, the image dissolves into an abstract color-field painting where only the broadest tonal structure of the source remains.

Two toggles give Facet its character. **Outlines** draws black borders at cell boundaries, turning the mosaic into an explicit grid — a stained-glass window or comic-book panel layout. **Flat Shade** switches between the sample-and-hold mosaic (flat color per cell) and the original live pixels, allowing the grid outlines to overlay a fully detailed image. Combined with the Mono desaturation toggle and the wet/dry Mix fader, these controls span a range from subtle texture to bold graphic abstraction.

---

## Background

### The Fairlight CVI and Early Video Mosaics

Facet belongs to the Fairlight category — effects inspired by the Fairlight Computer Video Instrument, one of the first real-time digital video effects processors. The original Fairlight CVI (1984) could pixelate live video by reducing spatial resolution in real time, creating the blocky mosaic look that became iconic in 1980s music videos and television. Facet extends this legacy with configurable cell sizes, optional outlines, and flat-shading control.

### Sample-and-Hold in Video

The core technique behind Facet's flat shading is **sample-and-hold**: at the start of each cell, the current pixel value is captured and held constant until the next cell boundary. This is the spatial equivalent of a zero-order hold in signal processing — no interpolation, no averaging, just the raw value at one sample point extended across a region. The result is a staircase approximation of the original image, with each step being one cell wide.

In analog video processing, sample-and-hold circuits were used for time-base correction and signal clamping. Digital implementations like Facet's use a simple register that latches the incoming pixel value whenever a counter resets. The visual effect is identical to nearest-neighbor downsampling followed by nearest-neighbor upsampling — pixels become visible as uniform rectangles.

### Cell Grids and Tesselation

Facet divides the frame using a regular rectangular grid. The cell width is derived from the Cell Size register: bits [9:5] plus a constant offset of 4, giving a range of 4 to 35 pixels. Both axes use the same cell width, producing square cells. Local X and Y counters track position within each cell, resetting at cell boundaries to drive both the sample-and-hold latch and the edge detector.

This fixed-frequency grid contrasts with irregular tessellation methods like Voronoi diagrams or Delaunay triangulations. Facet's regularity is deliberate — it creates a mechanical, crystalline quality rather than an organic one. The grid is synchronized to the video raster, so cell boundaries align consistently across frames.

### Flat Shading and Cel Animation

The Flat Shade toggle switches between two rendering modes. When enabled, each cell displays the held sample — a single uniform color. When disabled, the original live pixels pass through, and only the edge outlines (if enabled) affect the image. The "flat shade" terminology comes from 3D computer graphics, where it refers to rendering each polygon face with a single color rather than interpolating across vertices.

Combined with black outlines, flat shading creates a look reminiscent of **cel animation** — the traditional animation technique where characters and backgrounds are painted with flat colors and outlined in black ink. The visual connection is immediate: Facet turns live video into something that looks hand-drawn.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Sync Detection ─────────────────────────────────────────────
│   ├─ Detect hsync/vsync falling edges
│   ├─ Maintain global X/Y raster counters
│   └─ Maintain local_x / local_y within current cell
│
├── Cell Grid ──────────────────────────────────────────────────
│   ├─ Cell width = reg(0)[9:5] + 4    (range 4–35 pixels)
│   ├─ local_x resets at cell boundary  → sample-and-hold Y/U/V
│   └─ local_y resets at row cell boundary
│
├── Processing ─────────────────────────────────────────────────
│   ├─ 1. Edge detect: local_x < edge_w OR local_y < edge_w
│   │      → black (Y=0, U=512, V=512)
│   ├─ 2. Flat shade: held Y/U/V from cell origin sample
│   │      OR live input Y/U/V (when Flat Shade off)
│   └─ 3. Mono: force U/V to 512 (neutral chroma)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ 3× interpolator_u: lerp(dry, wet, mix_amount)
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock pipeline delay for hsync/vsync/field/data
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed or delayed-dry signal
```

The processing pipeline is structurally simple — a single process handles sync detection, cell grid tracking, sample-and-hold, edge detection, and output selection in sequence. The critical interaction is between the cell grid counters and the sample-and-hold latch: when `local_x` resets to zero (cell boundary), the current input pixel is captured into `held_y/u/v` registers. All subsequent pixels within that cell use the held values when Flat Shade is active. Edge detection runs in parallel, checking whether the current local position falls within the edge-width threshold — if so, the pixel is forced to black regardless of the shading mode.

The edge width is derived from bits [9:7] of the Edge Width register, giving a 3-bit range of 0–7 pixels. This is compared against both `local_x` and `local_y`, so edges appear as an L-shaped border at the top and left of each cell. At maximum, the edge can consume nearly the entire cell, leaving only a small window of the shaded content visible.

---

## Parameter Reference

<img src={facet_control_panel} alt="Videomancer front panel with Facet loaded"/>
*Videomancer's front panel with Facet active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the cell size — the width and height of each rectangular facet in the grid. The VHDL extracts bits [9:5] and adds 4 to the result, producing cell dimensions from 4 pixels (fully counter-clockwise) to 35 pixels (fully clockwise). At small values, the mosaic is fine enough that the source image remains recognizable. At large values, the image dissolves into a coarse grid of color blocks where only the broadest tonal regions are distinguishable.

---

#### Knob 2 — Edge Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the width of the black edge borders drawn at cell boundaries. The VHDL extracts bits [9:7], giving a 3-bit integer range of 0–7 pixels. At 0, no edges are drawn regardless of the Outlines toggle. As the value increases, the black border at the top and left of each cell widens, progressively obscuring more of the cell's interior. At maximum edge width relative to a small cell size, the entire grid can appear nearly black — the edges consume the cells.

---

#### Knob 3 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Mapped to a register but not used in the current VHDL implementation. The Contrast control is reserved for a future processing stage. Adjusting this knob has no effect on the output.

---

#### Knob 4 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Mapped to a register but not used in the current VHDL implementation. The Brightness control is reserved for a future processing stage. Adjusting this knob has no effect on the output.

---

#### Knob 5 — Color Reduce
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Mapped to a register but not used in the current VHDL implementation. The Color Reduce control is reserved for a future processing stage that would quantize the color palette. Adjusting this knob has no effect on the output.

---

#### Knob 6 — Randomize
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Mapped to a register but not used in the current VHDL implementation. The Randomize control is reserved for a future stage that would jitter cell boundaries or introduce noise into the grid. Adjusting this knob has no effect on the output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Hex Grid** | Off | On |
| **8 — Outlines** | Off | On |
| **9 — Flat Shade** | Off | On |
| **10 — Mono** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 8 through 10 control the three active rendering modes — outlines, flat shading, and monochrome desaturation. Toggle 7 (Hex Grid) is mapped but not implemented in the current VHDL. Toggle 11 is the standard bypass switch. The active toggles are independent: Outlines and Flat Shade can each be enabled or disabled separately, giving four distinct visual combinations — outlines only (grid overlay on live video), flat shade only (mosaic without borders), both (stained-glass look), or neither (pass-through with only the cell-boundary sample-and-hold latch active but no visible effect).

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the processed signal and the delayed original. At 100%, the output is fully processed (faceted). At 0%, the output is the original signal. The mix is implemented as three parallel interpolators (one per Y/U/V channel) running for 4 clock cycles each. Intermediate values blend between the mosaic and the source, creating a semi-transparent overlay effect where cell boundaries and flat shading are partially visible over the original image.

---

## Guided Exercises

These exercises progress from simple mosaic effects to graphic stained-glass compositions, building familiarity with cell size, edge outlines, and flat shading interactions.

### Exercise 1: Crystal Mosaic

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: facet_source1_skull, after: facet_ex1_s1 },
    { label: "Cat", before: facet_source2_cat, after: facet_ex1_s2 },
    { label: "Clouds", before: facet_source3_clouds, after: facet_ex1_s3 },
    { label: "Pattern", before: facet_source4_pattern, after: facet_ex1_s4 },
    { label: "Boy", before: facet_source5_boy, after: facet_ex1_s5 },
    { label: "Wood", before: facet_source6_wood, after: facet_ex1_s6 },
  ]}
/>
*Crystal Mosaic — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects — faces, text, or geometric objects work well.

**Objective**: Learn how Cell Size and Flat Shade interact to create mosaic effects at different resolutions.

1. **Enable flat shading**: Confirm Flat Shade (Toggle 9) is On and Outlines (Toggle 8) is Off.
2. **Minimum cells**: Turn Cell Size fully counter-clockwise. At 4-pixel cells, the image is slightly softened but recognizable.
3. **Increase cell size**: Slowly sweep Cell Size clockwise. Watch the image progressively dissolve into larger and larger color blocks.
4. **Find the sweet spot**: Around 40–50%, faces and objects are still recognizable as colored shapes but fine detail is gone.
5. **Maximum cells**: At 100%, the image is a very coarse grid — only broad color regions remain.

**Key concepts**: Cell size controls the trade-off between detail and abstraction, flat shading samples one pixel per cell and holds it across the entire cell area

---

### Exercise 2: Stained Glass

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: facet_source1_skull, after: facet_ex2_s1 },
    { label: "Cat", before: facet_source2_cat, after: facet_ex2_s2 },
    { label: "Clouds", before: facet_source3_clouds, after: facet_ex2_s3 },
    { label: "Pattern", before: facet_source4_pattern, after: facet_ex2_s4 },
    { label: "Boy", before: facet_source5_boy, after: facet_ex2_s5 },
    { label: "Wood", before: facet_source6_wood, after: facet_ex2_s6 },
  ]}
/>
*Stained Glass — simulated result across source images.*
**Source**: Brightly colored footage — flowers, neon signs, colorful fabrics, or abstract video feedback.

**Objective**: Combine flat shading with edge outlines to create a stained-glass window effect.

1. **Set moderate cell size**: Cell Size around 50–60% to create visible color panes.
2. **Enable outlines**: Turn on Outlines (Toggle 8). Black borders appear at cell boundaries.
3. **Adjust edge width**: Sweep Edge Width from minimum to maximum. Watch the grid lines thicken.
4. **Find the balance**: Around 30–40% Edge Width, the black borders create distinct cell separation without overwhelming the color content.
5. **Try without flat shade**: Turn off Flat Shade (Toggle 9). The outlines now overlay the full-resolution source — a comic-book panel effect.
6. **Re-enable flat shade**: The combination of flat color panes and black borders creates the classic stained-glass look.

**Key concepts**: Outlines draw black borders at cell boundaries, edge width controls the visual weight of the grid, flat shade and outlines are independent and combinable

---

### Exercise 3: Monochrome Grid Overlay

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: facet_source1_skull, after: facet_ex3_s1 },
    { label: "Cat", before: facet_source2_cat, after: facet_ex3_s2 },
    { label: "Clouds", before: facet_source3_clouds, after: facet_ex3_s3 },
    { label: "Pattern", before: facet_source4_pattern, after: facet_ex3_s4 },
    { label: "Boy", before: facet_source5_boy, after: facet_ex3_s5 },
    { label: "Wood", before: facet_source6_wood, after: facet_ex3_s6 },
  ]}
/>
*Monochrome Grid Overlay — simulated result across source images.*
**Source**: High-contrast footage — silhouettes, architectural details, or stark black-and-white material.

**Objective**: Use Mono and Outlines together to create a graphic pencil-sketch or architectural wireframe effect.

1. **Enable mono**: Turn on Mono (Toggle 10). The image becomes grayscale.
2. **Enable outlines and flat shade**: Both toggles On.
3. **Set cell size**: Around 40% for medium-resolution cells.
4. **Increase edge width**: Around 50% to make the grid structure prominent.
5. **Adjust mix**: Lower Mix to ~60%. The grid starts to dissolve into the monochrome source underneath — a technical drawing or blueprint effect.
6. **Try large cells**: Increase Cell Size to 80–100%. With mono and outlines, this creates bold, abstract compositions of gray blocks separated by thick black lines.
7. **Compare**: Toggle Bypass to see the unprocessed signal for A/B comparison.

**Key concepts**: Mono strips chrominance, leaving only luminance structure visible through the faceted grid; mix fader blends the effect intensity

---


## Tips

- **Cell Size sweet spot**: Around 30–50% produces cells large enough to read as flat color panes while preserving enough of the source composition to remain recognizable — the ideal range for stained-glass effects.
- **Edge width scales with cell size**: A 3-pixel edge is barely visible in a 35-pixel cell but consumes 75% of a 4-pixel cell. Increase cell size before increasing edge width to maintain visible cell interiors.
- **Outlines without flat shade**: Disabling Flat Shade while keeping Outlines on creates a grid overlay on full-resolution video — useful as a compositional guide or graphic design element.
- **Mono for emphasis**: The Mono toggle removes color distraction, making the geometric structure of the grid more prominent. Try it with high-contrast source material for bold graphic results.
- **Mix for subtlety**: At 100%, Facet fully replaces the source. Pulling Mix back to 60–80% lets the original detail show through the mosaic — a frosted-glass look.
- **Feedback loops**: Routing Facet's output back to its input creates recursive mosaics — each pass samples the already-flat-shaded cells, progressively reducing the image to fewer and fewer unique color values.
- **Reserved controls**: Knobs 3–6 and Toggle 7 are mapped but unused in the current VHDL. Future firmware updates may activate Contrast, Brightness, Color Reduce, Randomize, and Hex Grid features.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R BT.601; the color encoding standard used by Videomancer's YUV pipeline for standard-definition video. |
| **Cell** | A rectangular region of the frame defined by the cell grid; each cell displays either a flat-shaded sample or the live input depending on mode. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interpolator** | A linear blending unit (lerp) used for the wet/dry mix stage; three instances blend Y, U, and V independently. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Mosaic** | A spatial effect that replaces groups of pixels with uniform blocks, reducing spatial resolution. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Sample-and-Hold** | A technique that captures a signal value at a specific moment and holds it constant until the next capture event. |
| **Tessellation** | The division of a surface into tiles (cells) that cover it without gaps or overlaps. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
| **Zero-Order Hold** | A signal reconstruction method that holds each sample constant until the next sample arrives, producing a staircase waveform. |

---
