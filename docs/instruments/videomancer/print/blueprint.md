---
draft: true
sidebar_position: 23
slug: /instruments/videomancer/blueprint
title: "Blueprint"
image: /img/instruments/videomancer/blueprint/blueprint_hero.png
description: "Program guide for Blueprint, a Videomancer print program for the LZX video synthesizer."
---

import blueprint_hero from '/img/instruments/videomancer/blueprint/blueprint_hero.png';
import blueprint_before_after from '/img/instruments/videomancer/blueprint/blueprint_before_after.png';
import blueprint_control_panel from '/img/instruments/videomancer/blueprint/blueprint_control_panel.png';
import blueprint_exercise1_result from '/img/instruments/videomancer/blueprint/blueprint_exercise1_result.png';
import blueprint_exercise2_result from '/img/instruments/videomancer/blueprint/blueprint_exercise2_result.png';
import blueprint_exercise3_result from '/img/instruments/videomancer/blueprint/blueprint_exercise3_result.png';

# Blueprint

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={blueprint_hero} alt="Blueprint hero image"/>
*White contour lines trace every edge in the source against a deep Prussian blue ground, turning living video into an engineering drawing.*
<img src={blueprint_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Blueprint applied.*

---

## Overview

Blueprint transforms a video signal into a cyanotype-style technical drawing. Every edge in the source image is extracted as a white (or blue) contour line on a deep Prussian blue (or white) background. An optional dotted engineering grid overlays the result with horizontal and vertical reference lines at power-of-two spacings, and dimension tick marks appear at grid intersections when enabled.

The edge detection operates on luminance only, computing horizontal differences between adjacent pixels and vertical differences between adjacent lines via a single BRAM line buffer. The two gradient components — horizontal and vertical — are summed, thresholded, and scaled to produce contour luminance. The result is composited with a constant Prussian blue background colour (Y≈180, U=650, V=350), producing the characteristic deep blue of iron-based photographic prints.

The name references the cyanotype contact-printing process invented by Sir John Herschel in 1842. Originally used for reproducing architectural and engineering drawings, the "blueprint" became synonymous with technical documentation. Blueprint brings this analogue reproduction process into real-time video, turning any live source into a continuously-updating technical drawing.

---

## Background

### What Is a Cyanotype?

The cyanotype is one of the oldest photographic printing processes. A solution of ferric ammonium citrate and potassium ferricyanide is coated onto paper, exposed to ultraviolet light through a negative or transparent drawing, then washed in water. Exposed areas turn Prussian blue (iron hexacyanoferrate), while unexposed areas remain white. The result is a negative image — lines drawn on the original appear white on blue. Blueprints were the standard method for copying technical drawings from the 1870s through the 1940s and remain an iconic visual style.

### Edge Detection by Finite Differences

Blueprint uses the simplest edge detection method: first-order finite differences. The horizontal gradient is |Y(x) − Y(x−1)| — the absolute brightness change between adjacent pixels. The vertical gradient is |Y(line) − Y(line−1)| — the brightness change between adjacent lines, obtained via a one-line BRAM delay. Summing these two components produces an edge strength proportional to the local gradient magnitude. This is computationally equivalent to a simplified Sobel operator without the smoothing kernels.

### Power-of-Two Grid Spacing

Engineering drawings use reference grids at regular intervals. Blueprint implements this using a bitmask AND trick: a pixel is on a grid line when `(position AND mask) == 0`. The mask is a power-of-two minus one (7, 15, 31, 63, 127), creating grid periods of 8, 16, 32, 64, or 128 pixels. This replaces expensive modulo division with a single bitwise AND. The grid lines are "dotted" — only drawn on even-numbered pixels/lines — for a traditional engineering drawing aesthetic.

### Shift-Based Contrast Scaling

Rather than using hardware multipliers for edge brightness scaling, Blueprint uses five discrete shift levels: ×0.25 (`>>2`), ×0.5 (`>>1`), ×1.0 (none), ×2.0 (`<<1`, clamped), and ×4.0 (`<<2`, clamped). This creates a stepped contrast curve that can boost faint edges into visibility or pull strong edges back to subtle outlines, all without consuming DSP resources.


---

## Signal Flow

```
                              ┌────────────────────┐
data_in ─────────────────────►│ Input Register      │
         Y ─────────────────► │   + line buffer     │
                              │   write/read (BRAM) │
                              └──────┬─────────────┘
                                     │ Stage 1
                                     ▼
                              ┌────────────────────┐
                              │ Horizontal Diff     │
                              │  |Y(x) - Y(x-1)|   │
                              │ Vertical Diff       │
                              │  |Y(line)-Y(prev)|  │
                              └──────┬─────────────┘
                                     │ Stage 2
                                     ▼
                              ┌────────────────────┐
                              │ Abs + Sum + Clamp   │
                              │  edge_strength      │
                              └──────┬─────────────┘
                                     │ Stage 3
                                     ▼
                              ┌────────────────────┐
                              │ Threshold + Grid    │
                              │  + edge luma scale  │
                              │  + dim markers      │
                              └──────┬─────────────┘
                                     │ Stage 4
                                     ▼
                              ┌────────────────────┐
                              │ Composite Output    │
                              │  edge → white/blue  │
                              │  bg   → blue/white  │
                              │  grid → dim lines   │
                              └──────┬─────────────┘
                                     │ Stage 5
                                     ▼
data_in ──► [sync delay] ──► dry ──► Interpolator ◄── wet
                                       (4 clk)
                                          │
                                          ▼
                                      data_out
```

The pipeline has two data paths running in parallel: the processing chain computes edge strength and composites the drawing, while the sync delay chain preserves the original signal for the wet/dry interpolator. The line buffer stores one full line of Y data in BRAM, creating a one-line delay for vertical edge detection. Position counters track horizontal and vertical pixel coordinates for the grid overlay. The grid mask is pre-computed from the Grid Space pot and operates as a combinational bitwise AND — no clocked resources required.

The composite stage has a clear priority order: edges take highest priority (white or inverted blue), then dimension marks (slightly brighter grid dots), then grid lines (dim dots), then background fill (Prussian blue or white). The Negative toggle swaps the polarity of the entire composition — edges become blue on a white ground, inverting the traditional cyanotype relationship.

---

## Parameter Reference

<img src={blueprint_control_panel} alt="Videomancer front panel with Blueprint loaded"/>
*Videomancer's front panel with Blueprint active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Edge Thr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the edge detection threshold — the minimum gradient strength required for a pixel to be classified as an edge. The pot value is shifted right by 2 (divided by 4) to produce a threshold from 0 to 255. At low values (0–25%), nearly every pixel with any brightness change appears as a contour line, creating a dense, detailed drawing. At high values (75–100%), only the strongest edges survive, producing a sparse, bold outline. When Thick Lines mode is active, edges at half the threshold strength are also included, broadening the contour lines.

---

#### Knob 2 — Line W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls line width indirectly through the thick lines feature. In the current pipeline implementation, this parameter's value is available to the thick lines logic. The VHDL uses the Thick Lines toggle (Toggle 9) as the primary line broadening control — when active, the edge threshold is halved, allowing weaker gradient pixels adjacent to strong edges to also appear as contour lines, effectively doubling the visual line weight.

---

#### Knob 3 — Grid Space
| Property | Value |
|----------|-------|
| Range | 8 – 64 |
| Default | 36 |

Selects the grid spacing from five power-of-two periods. The pot is quantised into 8 steps, but the VHDL decodes five threshold zones: below 205 → 8-pixel grid, 205–409 → 16-pixel, 410–613 → 32-pixel, 614–818 → 64-pixel, 819–1023 → 128-pixel. Smaller grids produce a fine mesh suitable for detailed technical drawings; larger grids create a sparse reference frame.

---

#### Knob 4 — Grid Opac
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness of grid lines and dimension marks. The pot value is halved to produce the grid line luminance (`grid_y_pre`), and the dimension mark luminance is set to 1.5× the grid line level. At low values, grid lines are barely visible — subtle reference marks. At high values, the grid becomes a prominent overlay on the Prussian blue background. In Negative mode, grid lines appear as slightly dimmer white.

---

#### Knob 5 — Blue Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the depth of the Prussian blue background. The pot value scales the background luminance: `bg_y = 180 × blue_depth / 1024`. At 0%, the background is black. At 50%, it's a dark navy. At 100%, it's the full Prussian blue colour at Y≈180 with U=650, V=350. This allows the artist to make the background darker for a deeper, more saturated blue or lighter for a more washed-out cyanotype print.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the edge contrast scaling — how bright the detected contour lines appear. Five shift-based levels are decoded: below 205 → ×0.25 (`>>2`, very faint lines), 205–409 → ×0.5 (`>>1`, dim lines), 410–613 → ×1.0 (edge strength as-is), 614–818 → ×2.0 (`<<1`, boosted), 819–1023 → ×4.0 (`<<2`, maximum boost). Higher values make even weak edges appear as bright white lines; lower values produce subtle, faint outlines.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Blueprint | Whitepr |
| **8 — Grid** | Off | On |
| **9 — Ticks** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control the grid overlay, the cyanotype polarity, line thickness, dimension marks, and bypass. Toggle 7 is the VHDL parameter labelled "Style" — in the VHDL it controls whether the engineering grid overlay is visible. Toggle 8 controls the polarity (normal white-on-blue or negative blue-on-white). Toggle 9 enables thick line mode (halved edge threshold). Toggle 10 enables dimension tick marks at grid intersections. Toggle 11 bypasses all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) and wet (blueprint) signal using three parallel interpolators. At 0% the output is the unmodified input; at 100% the output is the full cyanotype drawing. Intermediate values superimpose the contour lines over the original video, creating a translucent overlay effect.

---

## Guided Exercises

These exercises progress from basic edge extraction through grid overlay to the complete engineering drawing aesthetic.

### Exercise 1: Simple Edge Drawing

<img src={blueprint_exercise1_result} alt="Simple Edge Drawing result"/>
*Simple Edge Drawing — simulated result across source images.*
**Source**: Architectural footage or any scene with clear geometric shapes.

**Objective**: Understand the edge detection pipeline and threshold control.

1. **Reveal all edges**: Set Edge Thr to 0%. Every pixel transition appears as a contour line.
2. **Raise threshold**: Increase Edge Thr to about 50%. Weak textures disappear, leaving only strong contours.
3. **Maximum threshold**: Push to 90%. Only the boldest edges survive — a very sparse drawing.
4. **Adjust contrast**: Set Contrast (Pot 6) to about 70%. Faint edges become brighter white.
5. **Blue depth**: Adjust Blue Depth (Pot 5) from 0% to 80%. Watch the background shift from black to Prussian blue.
6. **Toggle polarity**: Enable Invert (Toggle 10) to see the negative — blue lines on white.

**Key concepts**: Higher threshold = fewer edges, contrast scaling boosts faint edges, blue depth controls background colour, negative flips the cyanotype polarity

---

### Exercise 2: Engineering Grid Overlay

<img src={blueprint_exercise2_result} alt="Engineering Grid Overlay result"/>
*Engineering Grid Overlay — simulated result across source images.*
**Source**: Any footage — the grid is independent of video content.

**Objective**: Explore the grid overlay system, spacing, brightness, and dimension marks.

1. **Enable grid**: Set Grid (Toggle 8) to On. Dotted grid lines appear.
2. **Adjust spacing**: Turn Grid Space through its 8 steps. Watch the grid period change from 8px to 128px.
3. **Grid brightness**: Adjust Grid Opac from 0% to 80%. Grid lines become more prominent.
4. **Dimension marks**: Enable Ticks (Toggle 9). Small marks appear at every grid intersection.
5. **Combine with edges**: Set Edge Thr to about 40%. Contour lines and grid lines coexist; edges take priority at overlapping pixels.
6. **Negative mode**: Toggle Invert. Grid lines now appear as slightly dimmer white on the white background.

**Key concepts**: Grid uses power-of-two bitmask spacing, grid brightness is independent of background blue, dimension marks highlight intersections, edges have priority over grid in the compositor

---

### Exercise 3: Full Technical Drawing

<img src={blueprint_exercise3_result} alt="Full Technical Drawing result"/>
*Full Technical Drawing — simulated result across source images.*
**Source**: Mechanical parts, circuit boards, or architectural subjects.

**Objective**: Create a complete engineering drawing aesthetic with all features active.

1. **Moderate edge threshold**: Edge Thr at about 35% — enough detail without clutter.
2. **Strong contrast**: Brightness (Pot 6) at about 75%. Edges appear as bright, confident lines.
3. **Full blue**: Blue Depth at about 80%. Deep Prussian blue background.
4. **Fine grid**: Grid Space at about 25% (16-pixel period). Enable Grid.
5. **Grid subtle**: Grid Opac at about 30%. Grid is visible but doesn't overpower the contours.
6. **Dimension marks**: Enable Ticks. Intersection dots add engineering drawing authenticity.
7. **Thick lines**: Enable Ticks toggle (Toggle 9) for broader contour widths.
8. **Mix for overlay**: Reduce Mix to about 60%. The blueprint overlays the original source ghostly beneath.

**Key concepts**: All features combine: edges + grid + dimension marks + blue background produce authentic cyanotype aesthetic, thick lines broaden contours, mix allows ghost overlay

---


## Tips

- **Start with Contrast before Threshold**: Boost Contrast (Pot 6) first. This makes faint edges visible without lowering the threshold, reducing noise.
- **32-pixel grid for general use**: Grid Space at ~60% (32px period) provides a good balance between density and readability.
- **Negative mode for projections**: The blue-on-white "whiteprint" mode is easier to read when projected or overlaid on bright backgrounds.
- **Use Mix for ghost overlay**: Mix at 40–60% superimposes the blueprint contours over the original video, creating a technical drawing analysis view.
- **Blue Depth sets the mood**: Low Blue Depth (dark background) creates a more dramatic, high-contrast drawing; high Blue Depth is more faithful to real cyanotype prints.
- **Dimension marks for precision**: Enable Ticks when using the grid as a measurement reference — the intersection dots make counting grid squares easier.
- **Thick lines + low threshold = poster art**: This combination creates bold, graphic outlines suitable for screen printing or poster imagery.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bitmask** | A binary pattern used with a bitwise AND operation to test whether a pixel coordinate falls on a power-of-two grid line, replacing expensive modulo division. |
| **BRAM** | Block RAM; dedicated memory blocks within an FPGA, used here to store one full line of luminance data for vertical edge detection. |
| **Cyanotype** | A photographic contact-printing process using iron salts that produces white imagery on a deep Prussian blue background, invented by Sir John Herschel in 1842. |
| **Diazo** | A reprographic printing process that produces dark lines on a white or off-white background, the tonal inverse of a cyanotype; also called a whiteprint. |
| **DSP** | Digital Signal Processor; a dedicated hardware multiplication block within an FPGA, avoided by Blueprint's shift-based contrast scaling. |
| **Finite difference** | A numerical method that approximates a derivative by computing the difference between adjacent sample values, used here for edge detection. |
| **Gradient** | The rate of brightness change between adjacent pixels, used as a measure of edge strength in the horizontal or vertical direction. |
| **Interpolator** | A hardware mixing block that crossfades between two input signals using a weighted average, used here for dry/wet blending. |
| **Luma** | The brightness component (Y) of a YUV video signal, the only channel used for edge detection in Blueprint. |
| **LUT** | Look-Up Table; a small memory or combinational logic structure that maps an input index to a pre-computed output value. |
| **Prussian blue** | Iron hexacyanoferrate; the deep blue pigment produced by the cyanotype chemical reaction, used as the background colour (Y≈180, U=650, V=350). |
| **Sobel operator** | A standard image processing edge detection kernel that combines horizontal and vertical gradient estimates with smoothing; Blueprint uses a simplified variant without the smoothing kernels. |
| **YUV** | A colour encoding system that separates brightness (Y) from two colour-difference components (U and V), used as the native signal format in Videomancer. |

---
