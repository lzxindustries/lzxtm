---
draft: true
sidebar_position: 136
slug: /instruments/videomancer/hilbert
title: "Hilbert"
image: /img/instruments/videomancer/hilbert/hilbert_hero.png
description: "The screen is divided into a grid of square blocks."
---

import hilbert_hero from '/img/instruments/videomancer/hilbert/hilbert_hero.png';
import hilbert_animation from '/img/instruments/videomancer/hilbert/hilbert_animation.gif';
import hilbert_control_panel from '/img/instruments/videomancer/hilbert/hilbert_control_panel.png';
import hilbert_exercise1_result from '/img/instruments/videomancer/hilbert/hilbert_exercise1_result.gif';
import hilbert_exercise2_result from '/img/instruments/videomancer/hilbert/hilbert_exercise2_result.gif';
import hilbert_exercise3_result from '/img/instruments/videomancer/hilbert/hilbert_exercise3_result.gif';

# Hilbert

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={hilbert_hero} alt="Hilbert hero image"/>
*Hilbert generating a fractal reveal sequence with color-shifted blocks tracing the space-filling curve across a grid.*
<img src={hilbert_animation} alt="Hilbert animated output"/>
*Hilbert output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

The screen is divided into a grid of square blocks. Each block is assigned a position along a **Hilbert curve** — a continuous, self-similar path that visits every cell of a 2D grid exactly once without crossing itself. An animation counter traces this path, progressively revealing blocks in curve order against a solid background. The result is a fractal unfolding: the image does not appear left-to-right or top-to-bottom, but in the recursive, folding pattern of the Hilbert curve itself.

The name *Hilbert* refers to the mathematician David Hilbert, who described the curve in 1891 as a limit of a sequence of piecewise-linear paths. Each successive **order** of the curve subdivides the grid further, visiting 4ⁿ cells at order *n*. The program computes the mapping combinationally for orders 1 through 4, covering grids from 2×2 to 16×16 blocks. Combined with configurable block sizes from 8 to 64 pixels, this produces spatial permutation grids from very coarse (a handful of large tiles) to quite fine (256 small blocks across the frame).

At conservative settings — large blocks, full reveal position, no color shift — Hilbert simply passes video through with an optional grid overlay. As you lower the reveal position or enable animation, the fractal traversal pattern becomes the dominant visual element. With color shift engaged, each block's chrominance is offset proportional to its Hilbert distance, painting a rainbow gradient that follows the curve's recursive topology rather than simple spatial coordinates.

---

## Background

### What Is a Space-Filling Curve?

A **space-filling curve** is a continuous path that passes through every point in a two-dimensional region. The concept seems paradoxical — a one-dimensional line filling a two-dimensional area — but it works because the path folds back on itself at every scale, becoming infinitely detailed in the limit. In practice, discrete approximations at finite orders are used: an order-*n* Hilbert curve visits all 4ⁿ cells of a 2ⁿ × 2ⁿ grid. The key property is **locality preservation** — points that are close together along the curve tend to be close together in 2D space. This makes Hilbert curves useful in image processing, database indexing, and dithering, because they traverse space without the long jumps that a simple raster scan produces.

### How Does the Hilbert Mapping Work?

The program uses a well-known iterative algorithm to convert between 2D coordinates (x, y) and the one-dimensional Hilbert distance *d*. At each level of recursion, the algorithm identifies which of four quadrants the point falls in, accumulates the corresponding distance, and rotates/reflects the coordinate system for the next level. The VHDL implements this as an unrolled combinational function — four iterations, one per possible order, evaluated in a single clock cycle. The maximum grid is 16×16 = 256 cells, fitting the Hilbert distance comfortably in 8 bits.

### Block-Level Processing

Unlike programs that operate on individual pixels, Hilbert works at the **block** level. The frame is partitioned into square blocks of 8, 16, 32, or 64 pixels. All pixels within a block share the same Hilbert distance value and therefore the same reveal state and color shift. This avoids the need for a frame buffer — the block's grid position is computed from the pixel counter on the fly, and the Hilbert distance is derived combinationally from that position. Edge detection (first pixel of each block) provides optional grid outlines.

### Reveal Animation

The reveal mechanism uses a 16-bit counter that increments once per video frame. Blocks whose Hilbert distance falls at or below the counter's upper 8 bits are "revealed" (showing video); blocks above the threshold show the background color. As the counter advances, blocks appear in Hilbert-curve order — spiraling inward through the recursive quadrant structure rather than sweeping linearly. The direction toggle reverses the counter, creating a progressive erasure effect.

### Color Shift Along the Curve

When the color shift control is active, revealed blocks receive a chrominance offset proportional to their Hilbert distance. The offset is added to the U channel and subtracted from the V channel, creating a hue rotation that follows the curve's topology. Blocks that are adjacent in Hilbert distance get similar hues; blocks that are far apart along the curve — even if spatially adjacent — get different hues. This visualizes the curve's structure as a rainbow gradient painted across the grid.


---

## Signal Flow

```
Generated Output (YUV 4:4:4)
│
├── YUV Channels (combined) ────────────────────────────────────
│   │
│   ├─ 1. Input Register         (latch data_in Y/U/V + block coord from counters)
│   ├─ 2. Hilbert Mapping        (xy-to-d: block coords → 8-bit curve distance)
│   ├─ 3. Reveal Test            (compare distance to reveal counter threshold)
│   ├─ 4. Compose Output         (revealed: video ± color shift; unrevealed: background)
│   │      ├─ Outline overlay    (bright/dim line at block edges if enabled)
│   │      └─ Color shift        (distance-proportional U+/V− offset)
│   └─ 5–8. Interpolator         (wet/dry mix, 4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay pipeline (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical path is the combinational Hilbert xy-to-d function in stage 2, which must complete within one clock cycle. Because it is unrolled for four iterations (orders 1–4 only), this is achievable at 74.25 MHz without pipelining the function itself. All three color channels share the same processing path — the reveal test and compose logic apply identically to Y, U, and V, with the color shift adding a distance-proportional offset only to U and V. The bypass mux sits at the final output assignment, selecting between the interpolator output and the 8-clock-delayed original data.

---

## Parameter Reference

<img src={hilbert_control_panel} alt="Videomancer front panel with Hilbert loaded"/>
*Videomancer's front panel with Hilbert active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Order
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

Controls the Hilbert curve order — the number of recursive subdivisions of the grid. The VHDL maps the potentiometer's 10-bit value into four thresholds, producing orders 1 through 4. Order 1 creates a 2×2 grid (4 blocks), order 2 a 4×4 grid (16 blocks), order 3 an 8×8 grid (64 blocks), and order 4 a 16×16 grid (256 blocks). Note that while the TOML labels suggest orders up to 8, the VHDL hard-limits the mapping to a maximum of 4. Higher orders would exceed the 4-bit coordinate width of the combinational converter. The visual impact of this control depends strongly on block size — order 4 with 8-pixel blocks produces a very fine grid, while order 1 with 64-pixel blocks shows just four enormous tiles.

---

#### Knob 2 — BlkSize
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 2 |

Sets the pixel block size. The potentiometer value is mapped to four discrete sizes: 8×8, 16×16, 32×32, and 64×64 pixels. Smaller blocks create a finer spatial permutation grid with more cells to reveal; larger blocks create a coarser mosaic. Combined with the Order control, this determines the total number of cells and the visual density of the Hilbert pattern. At block size 8 with order 4, the grid covers 128×128 pixels of screen space per Hilbert tile — repeated across the frame. At block size 64 with order 1, the entire visible area is divided into just four massive quadrants.

---

#### Knob 3 — RevlSpd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the speed of the automatic reveal animation. The 10-bit register value is right-shifted by 4 bits and added to (or subtracted from) the 16-bit reveal counter once per video frame. At minimum, the counter barely moves and the reveal crawls; at maximum, blocks appear rapidly. The animation only advances when the Animate toggle is enabled — otherwise this control has no effect, and the reveal position is set entirely by Knob 4.

---

#### Knob 4 — RevlPos
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Sets the manual reveal position. When the Animate toggle is off, this control directly positions the reveal threshold by mapping the 10-bit register into the upper bits of the 16-bit counter. Fully clockwise reveals all blocks; fully counter-clockwise hides all blocks. At intermediate positions, the Hilbert curve's characteristic recursive spiral is frozen mid-trace, showing which blocks have been "visited" by the curve up to that distance value.

---

#### Knob 5 — BgLuma
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the luminance of unrevealed (background) blocks. At minimum, hidden blocks are black. As you increase the control, the background brightens to a uniform gray. The chrominance of background blocks is always neutral (U=512, V=512). When outlines are enabled, background block edges are drawn at a dim level (approximately 300/1023), providing a faint grid structure even before blocks are revealed.

---

#### Knob 6 — ClrShft
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the magnitude of the color shift applied to revealed blocks. At zero, all revealed blocks show the source video with its original chrominance. As you increase the control, each block's U channel is increased and its V channel decreased by an amount proportional to the product of the block's Hilbert distance and this register value. The result is a rainbow gradient that follows the curve's topology — blocks close together in Hilbert order share similar hues, while blocks far apart along the curve diverge in color even if they are spatially adjacent.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Dir** | Forward | Reverse |
| **9 — Map** | Shuffle | Inverse |
| **10 — Outline** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control mostly independent options, though Animate and Direction form a natural pair governing the reveal counter behavior. Toggle 9 (Map) is registered in the VHDL but has no effect on the processing pipeline — the signal `s_inverse_map` is assigned from the register but never read by any downstream logic. This is a vestigial control from a planned shuffle/inverse mapping mode that was not implemented.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix crossfade between the original (delayed) input and the processed output. The three interpolator instances (one per Y, U, V channel) blend linearly between input `a` (delayed original) and input `b` (processed) using this register as the interpolation parameter `t`. At minimum, the output is entirely the original signal; at maximum, the output is entirely the Hilbert-processed result. Intermediate values produce a transparent overlay of the fractal grid pattern on the source video.

---

## Guided Exercises

These exercises progress from exploring the grid structure to animating the Hilbert curve reveal and finally combining color shift with animation for a full fractal composition.

### Exercise 1: Grid Structure and Reveal

<img src={hilbert_exercise1_result} alt="Grid Structure and Reveal result"/>
*Grid Structure and Reveal — simulated result across source images.*
**Objective**: Understand how order, block size, and reveal position interact to create the Hilbert grid pattern.

1. **Start with a visible grid**: Set Order to position 3 (order 3 = 8×8 grid) and Block Size to position 2 (16×16 pixels). Enable Outline.
2. **Manual reveal**: With Animate off, slowly sweep the Reveal Pos knob from minimum to maximum. Watch blocks appear one by one in the recursive spiral pattern of the Hilbert curve — not in a linear sweep.
3. **Freeze mid-reveal**: Stop the Reveal Pos knob at about 50%. Observe the characteristic U-shaped and S-shaped clusters of revealed blocks that reflect the curve's quadrant structure.
4. **Change order**: Switch Order from position 3 to position 1. The grid collapses to 2×2 — only four blocks, revealed in a simple L-shaped sequence. Then try order 4 for the densest 16×16 grid.
5. **Change block size**: With order 3 active, sweep Block Size from position 1 (8px) to position 4 (64px). The grid pattern is the same, but the blocks range from tiny tiles to large panels.

**Key concepts**: Hilbert curve order determines grid subdivision depth, block size determines pixel granularity, reveal position traces the curve from start to end

---

### Exercise 2: Animated Reveal

<img src={hilbert_exercise2_result} alt="Animated Reveal result"/>
*Animated Reveal — simulated result across source images.*
**Objective**: Explore the reveal animation and direction controls to create dynamic Hilbert curve tracing.

1. **Set up the grid**: Order at position 3, Block Size at position 2 (16px), Outline on, BgLuma at about 10% so the background is dark gray rather than black.
2. **Start animation**: Enable the Animate toggle. The reveal counter begins advancing, and blocks appear in Hilbert order.
3. **Adjust speed**: Sweep the RevlSpd knob. At low values the curve traces slowly — you can follow its recursive path. At high values the entire grid fills and wraps around quickly.
4. **Reverse direction**: Toggle Dir to Reverse. The curve now retracts, erasing blocks in descending distance order. The visual pattern is the mirror image of the forward trace.
5. **Background brightness**: Increase BgLuma to about 30%. The unrevealed blocks become visible as a gray field, and the faint grid outline on background blocks (Y=300) becomes more apparent.

**Key concepts**: Reveal animation traces the Hilbert curve in real time, speed controls counter increment per frame, direction reverses the traversal, background brightness provides context for unrevealed regions

---

### Exercise 3: Color Curve Composition

<img src={hilbert_exercise3_result} alt="Color Curve Composition result"/>
*Color Curve Composition — simulated result across source images.*
**Objective**: Combine color shift, reveal animation, and the mix fader for a full fractal color composition.

1. **Enable color shift**: With the grid from Exercise 2 active, slowly increase the ClrShft knob. Watch each revealed block take on a hue proportional to its Hilbert distance — creating a rainbow that follows the curve's recursive path rather than spatial position.
2. **Full reveal with color**: Set RevlPos to maximum (or let animation fill the grid). The entire frame becomes a color-mapped mosaic where the Hilbert topology is visible as a continuous gradient.
3. **Fine grid**: Increase Order to 4 and decrease Block Size to 8px. The color gradient becomes smoother because more blocks sample more points along the curve.
4. **Mix with source**: Lower the Mix fader to about 60%. The fractal color grid becomes semi-transparent, overlaying the source video beneath.
5. **Animate with color**: Enable Animate at moderate speed. The rainbow reveals and retracts, painting the curve's structure in real time.

**Key concepts**: Color shift encodes Hilbert distance as chrominance, curve topology creates non-spatial rainbow gradients, mix controls overlay transparency, fine grids produce smoother color fields

---


## Tips

- **Order × Block Size = visual density**: Order determines how many cells the Hilbert curve visits; block size determines how many pixels each cell covers. The combination controls the overall grid density. Order 4 with 8px blocks is the finest; order 1 with 64px blocks is the coarsest.
- **The reveal is the signature effect**: The Hilbert curve's recursive traversal order is what makes this program unique. Use manual reveal (Animate off, sweep Knob 4) to study the curve's structure before enabling animation.
- **Toggle 9 does nothing**: The Map switch is registered in hardware but has no effect on the output. This is a known vestigial control — do not expect Shuffle/Inverse behavior differences.
- **Color shift visualizes topology**: The rainbow gradient follows Hilbert distance, not screen position. Two blocks that are next to each other on screen may have very different hues if they are far apart along the curve. This is a direct visualization of the space-filling curve's locality properties.
- **Mix for overlay**: At intermediate Mix values, the Hilbert grid becomes semi-transparent over the source video. Combined with color shift, this creates a fractal color overlay — useful for visualizing the curve structure on recognizable content.
- **Background brightness for context**: Setting BgLuma above zero lets you see the full grid structure (with outlines) even before blocks are revealed. The dim outlines on unrevealed blocks provide spatial context for the reveal animation.
- **Feedback loops**: Routing the output back to the input creates recursive Hilbert permutation — each frame re-maps the already-mapped blocks, producing evolving fractal mosaic patterns.

---

## Glossary

| Term | Definition |
|------|------------|
| **Block** | A square group of pixels (8×8, 16×16, 32×32, or 64×64) that shares a single Hilbert distance value and is processed as a unit. |
| **Combinational** | Logic that produces an output immediately from its inputs without waiting for a clock edge, as opposed to registered (clocked) logic. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Hilbert Curve** | A continuous, self-similar space-filling curve that visits every cell of a 2D grid exactly once, preserving spatial locality. |
| **Hilbert Distance** | The one-dimensional index of a cell along the Hilbert curve; used for reveal ordering and color shift computation. |
| **Interpolator** | A linear crossfade module that blends between two input signals based on a mix parameter. |
| **LUT** | Look-Up Table; a basic logic element in FPGA fabric used to implement combinational functions. |
| **Order** | The number of recursive subdivisions of the Hilbert curve; order *n* produces a 2ⁿ × 2ⁿ grid of cells. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Reveal** | The progressive display of blocks in Hilbert curve order, controlled by a threshold counter compared against each block's curve distance. |
| **Space-Filling Curve** | A continuous path that passes through every point in a multi-dimensional region; the Hilbert curve is the most common example. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
