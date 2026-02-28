---
draft: true
sidebar_position: 76
slug: /instruments/videomancer/domino
title: "Domino"
image: /img/instruments/videomancer/domino/domino_hero.png
description: "In the world of broadcast television, the most dramatic transitions are the ones that reveal the next image piece by piece — not in a smooth fade but in..."
---

import domino_hero from '/img/instruments/videomancer/domino/domino_hero.png';
import domino_before_after from '/img/instruments/videomancer/domino/domino_before_after.png';
import domino_control_panel from '/img/instruments/videomancer/domino/domino_control_panel.png';
import domino_exercise1_result from '/img/instruments/videomancer/domino/domino_exercise1_result.png';
import domino_exercise2_result from '/img/instruments/videomancer/domino/domino_exercise2_result.png';
import domino_exercise3_result from '/img/instruments/videomancer/domino/domino_exercise3_result.png';

# Domino

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={domino_hero} alt="Domino hero image"/>
*Domino sweeping a cascade dissolve across a cell grid, progressively flipping tiles in a diagonal wave to reveal inverted and color-filled regions.*
<img src={domino_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Domino applied.*

---

## Overview

In the world of broadcast television, the most dramatic transitions are the ones that reveal the next image piece by piece — not in a smooth fade but in a cascade of discrete cells, each flicking from one state to another like the tiles on a departures board. Domino recreates this effect as a continuously evolving video process rather than a one-shot transition.

The program divides the video frame into a rectangular grid of tiles and sweeps a threshold across the cell coordinates. Tiles whose index falls on one side of the threshold pass the input video unchanged; tiles on the other side are flipped — either inverted (bitwise complement of YUV) or replaced with a solid color fill. The sweep advances automatically each frame, creating a cascading wave of reveals that rolls across the screen. The name references the chain-reaction toppling of dominoes — once a tile flips, the next one follows.

At gentle settings with large tiles and slow speed, Domino produces stately broadcast-style wipes. At small tile sizes with diagonal mode engaged, the cascade becomes a rapid crystalline dissolution that shatters the image into a mosaic of inverted and original fragments.

---

## Background

### Quantel and Digital Video Effects

Quantel Corporation pioneered digital video effects (DVE) hardware in the late 1970s and 1980s. Their products — the Quantel DPE 5000, Mirage, and later the Henry and Hal — introduced broadcasters to real-time spatial transformations that were impossible with analog equipment: page turns, cube rotations, mosaic dissolves, and cascade reveals. The "cascade dissolve" — where an image disintegrates or assembles tile by tile in a sweeping pattern — became a signature broadcast transition. Domino distills that cascade mechanism into a continuous processing loop rather than a one-shot transition.

### Cascade Dissolve Transitions

A cascade dissolve works by partitioning the frame into a grid and then sequentially toggling each cell from one source to another. The order of toggling defines the visual character of the transition: left-to-right produces a curtain wipe, diagonal produces a waterfall, random produces a sparkle dissolve. In broadcast DVE units, the grid was typically fixed at power-of-two sizes (8×8, 16×16, 32×32). Domino uses a continuously variable tile size controlled by an analog potentiometer, producing grids that range from a few massive blocks to hundreds of small cells.

### Cell-Based Video Processing

Dividing a video frame into spatial cells is a fundamental technique in image processing. Block-based transforms (like the DCT blocks in JPEG and MPEG) operate on 8×8 pixel cells. Motion estimation in video codecs partitions each frame into macroblocks. Domino's cell grid is simpler — it uses the cell coordinates purely as an index for the cascade threshold, not for any transform within the cell. Each cell passes its pixels unchanged or applies a uniform inversion, making the tile boundary itself the visual element.

### The Domino Cascade

The physical phenomenon of a domino cascade — where toppling one tile triggers the next in sequence — is a classic example of a threshold-driven chain reaction. Each tile has two states (standing or fallen) and a threshold (the force required to topple it). Once the threshold is exceeded, the transition is binary and irreversible. Domino's sweep works the same way: each cell is either flipped or not, based on whether its coordinate index has been reached by the advancing sweep counter. The result is a sharp boundary between flipped and unflipped regions that marches across the frame.

### Inversion as Reveal

Bitwise inversion of a video signal — replacing each sample with its ones-complement — produces a negative image where bright becomes dark and colors shift to their complements. In analog video synthesis, inversion is a fundamental building block for keying, matting, and contrast manipulation. Domino uses inversion as its primary "flip" operation because it preserves the spatial structure of the source while making the flipped tiles visually distinct. The alternative color-fill mode replaces flipped tiles with a uniform luminance, creating a more graphic, screen-print-like result.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Cell Grid Subdivision ─────────────────────────────
│   ├─ Tile Size → cell_width = tile_size(9:5) + 4 (4–35 px)
│   ├─ Pixel counters: x_counter, y_counter
│   ├─ Local position: local_x, local_y (within cell)
│   └─ Cell coordinates: cell_x, cell_y (cell index)
│
├── Stage 2: Sweep Threshold ───────────────────────────────────
│   ├─ Diagonal off: cell_idx = cell_x
│   ├─ Diagonal on:  cell_idx = cell_x + cell_y
│   ├─ Sweep value from frame_counter(11:0)
│   ├─ Normal:  flipped = (cell_idx < sweep)
│   └─ Reverse: flipped = (cell_idx > sweep)
│
├── Stage 3: Tile Processing ───────────────────────────────────
│   ├─ Unflipped: Y, U, V = input (pass-through)
│   ├─ Flipped + Invert:     Y = NOT(Y), U = NOT(U), V = NOT(V)
│   └─ Flipped + Color Fill: Y = Color pot, U = 512, V = 512
│
├── Stage 4: Wet/Dry Mix (3× interpolator_u, 4 clocks) ────────
│   └─ lerp(delayed_input, processed, mix_amount)
│
├── Sync Delay Pipeline (8 clocks) ─────────────────────────────
│   └─ hsync_n, vsync_n, field_n, Y, U, V delayed to match
│
└── Output ─────────────────────────────────────────────────────
    └─ Bypass off: mixed output | Bypass on: delayed input
```

The cascade effect emerges from a single comparison: cell index versus sweep counter. Every pixel's fate is determined by which cell it occupies and whether that cell's index has crossed the sweep threshold. The frame counter advances on each vertical sync by a speed-dependent step, so the wave rolls forward in time. Diagonal mode sums the X and Y cell coordinates, producing a diagonal wavefront instead of a vertical one — the cascade sweeps from the top-left corner toward the bottom-right.

---

## Parameter Reference

<img src={domino_control_panel} alt="Videomancer front panel with Domino loaded"/>
*Videomancer's front panel with Domino active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Tile Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Tile Size controls the width and height of each cell in the grid. At 0% the cell width is 4 pixels, producing a dense grid of tiny tiles that can number in the thousands across a single frame. At 100% the cell width reaches 35 pixels, producing a coarse grid of large rectangular blocks. Smaller tiles create a fine-grained cascade that resembles a crystalline dissolution; larger tiles create a bold, graphic reveal with clearly visible block boundaries.

---

#### Knob 2 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Speed controls how fast the sweep counter advances. On each vertical sync pulse the frame counter increments by a value derived from the upper bits of this parameter (1 to 8 steps per frame). At minimum speed the cascade crawls across the grid over many seconds; at maximum speed the entire frame can flip in under a second. When Animate is disengaged the frame counter freezes and Speed has no effect.

---

#### Knob 3 — Direction
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Direction biases the sweep starting position. At center (50%) the sweep begins at the natural zero index. Rotating below center shifts the sweep origin so that tiles on the right side of the frame flip first; rotating above center shifts it so tiles on the left flip first. Combined with Diagonal mode this rotates the wavefront angle, allowing the cascade to sweep in from corners or edges.

---

#### Knob 4 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Threshold offsets the comparison point between cell index and sweep counter. At center (50%) the comparison is neutral. Rotating below center makes fewer tiles flip at any given moment — the cascade contracts. Rotating above center makes more tiles flip — the cascade expands. This control sets the "bias" of the transition, determining how much of the frame is in the flipped state at any instant.

---

#### Knob 5 — Color
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Color sets the luminance value used for solid color fill when Color Fill mode is active. At 0% flipped tiles become black; at 100% they become peak white. Chrominance is fixed at neutral (U=V=512), producing achromatic fills. When Color Fill is disengaged this control has no visible effect — flipped tiles show the inverted video signal instead.

---

#### Knob 6 — Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Depth modulates the visual intensity of the flipped tiles. At minimum the flip effect is subtle — flipped tiles are barely distinguishable from unflipped ones. At maximum the full inversion or color fill is applied. This parameter allows you to dial in a partial inversion that creates a softer, more blended cascade rather than a hard binary flip.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Diagonal** | Off | On |
| **8 — Reverse** | Off | On |
| **9 — Color Fill** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure independent aspects of the cascade behavior. Diagonal and Reverse modify the sweep geometry. Color Fill selects between two flip modes (inversion versus solid fill). Animate enables or freezes the sweep counter. Bypass disables all processing for A/B comparison. No two toggles interact in a combinatorial way — each controls a single binary decision in the pipeline.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the delayed dry input and the processed wet output. At 100% (default) the full cascade effect is visible. At 0% the output is the unprocessed input. Intermediate positions blend the processed and unprocessed signals, producing a ghostly overlay where flipped tiles appear semi-transparent against the original image.

---

## Guided Exercises

These exercises progress from a simple vertical wipe to a fully animated diagonal cascade. Each builds on the previous, engaging more controls to explore the program's range.

### Exercise 1: Vertical Curtain Wipe

<img src={domino_exercise1_result} alt="Vertical Curtain Wipe result"/>
*Vertical Curtain Wipe — simulated result across source images.*
**Source**: A live camera feed or recorded footage with clear subject matter and moderate contrast.

**Objective**: Understand the basic cell grid and sweep mechanism by creating a left-to-right curtain wipe.

1. **Large tiles**: Set Tile Size to about 70%. The grid should show clearly defined blocks.
2. **Slow sweep**: Set Speed to about 25%. The animation should advance slowly enough to observe individual tiles flipping.
3. **Watch the curtain**: The sweep rolls left to right, flipping tiles to their inverted complement.
4. **Reverse**: Engage Reverse (Toggle 8). The curtain now moves right to left.
5. **Color fill**: Engage Color Fill (Toggle 9) and set Color to about 25%. Flipped tiles become dark gray rectangles instead of inverted video.
6. **Tile size sweep**: Slowly decrease Tile Size from 70% down to 10%. The curtain transitions from coarse blocks to a fine grain.

**Key concepts**: Cell grid divides the frame into uniform tiles, sweep counter determines which tiles are flipped, tile size controls grid density

---

### Exercise 2: Diagonal Waterfall

<img src={domino_exercise2_result} alt="Diagonal Waterfall result"/>
*Diagonal Waterfall — simulated result across source images.*
**Source**: Footage with strong geometric elements — architecture, grids, or patterned surfaces.

**Objective**: Explore diagonal sweep mode and the interaction between tile geometry and image content.

1. **Enable diagonal**: Engage Diagonal (Toggle 7). The sweep direction changes to a diagonal wavefront.
2. **Medium tiles**: Set Tile Size to about 40% for a visible grid that isn't too coarse.
3. **Moderate speed**: Set Speed to about 50%. The diagonal cascade should be clearly visible.
4. **Adjust threshold**: Sweep Threshold from 0% to 100%. Watch how the flip region expands and contracts across the grid.
5. **Try both modes**: Toggle Color Fill on and off. With architectural source material, the flat-fill rectangles create a Mondrian-like composition against the inverted video tiles.
6. **Freeze and compose**: Disengage Animate (Toggle 10). Adjust Tile Size and Threshold to compose a specific mosaic pattern that works with the geometric source content.

**Key concepts**: Diagonal mode sums cell X and Y coordinates, threshold shifts the boundary between flipped and unflipped regions, static mode enables compositional control

---

### Exercise 3: Animated Mosaic Composite

<img src={domino_exercise3_result} alt="Animated Mosaic Composite result"/>
*Animated Mosaic Composite — simulated result across source images.*
**Source**: High-contrast footage — silhouettes, stage lighting, or graphic overlays.

**Objective**: Combine all controls for a continuously evolving tile mosaic with semi-transparent blending.

1. **Small tiles**: Set Tile Size to about 15%. The grid becomes a dense mosaic.
2. **Fast cascade**: Set Speed to about 75%. The sweep races across the grid.
3. **Diagonal + reverse**: Engage both Diagonal and Reverse. The cascade sweeps from bottom-right toward top-left.
4. **Color fill**: Engage Color Fill and set Color to about 80% for bright white tiles.
5. **Partial mix**: Lower Mix to about 60%. The cascade becomes semi-transparent — flipped tiles ghost against the original image.
6. **Sweep depth**: Adjust Depth to moderate the inversion intensity. Compare full-strength inversion with a subtle tonal shift.
7. **Speed variation**: Slowly sweep Speed from minimum to maximum. The cascade accelerates from a slow reveal to a rapid flicker.

**Key concepts**: Small tiles create dense mosaic textures, mix control enables transparency compositing, color fill with high luminance creates a strobe-like flash pattern across the grid

---


## Tips

- **Freeze to compose**: Disengage Animate to freeze the cascade at a specific pattern, then adjust Tile Size and Threshold to design a static mosaic composition.
- **Diagonal creates depth**: Diagonal mode sweeps from corner to corner, giving the cascade a three-dimensional quality that works well with perspective shots.
- **Color Fill for graphic overlays**: Engage Color Fill with a high Color value to create bright tile patterns that function as a graphic overlay on the original video.
- **Mix for ghosting**: Reduce Mix to 50–70% to make flipped tiles semi-transparent — the inversion becomes a subtle tonal shift rather than a hard flip.
- **Speed for tempo**: Match Speed to the tempo of music or performance. At 1 step per vsync (~2 seconds per full sweep at 30 fps), the cascade syncs naturally with slow musical passages.
- **Feedback loops**: Routing the output back to the input creates recursive cascade patterns — tiles that have been inverted once get inverted again on subsequent sweeps, producing evolving interference patterns.
- **Small tiles for texture**: At minimum Tile Size (4 pixels), the cascade becomes a fine-grained texture generator rather than a recognizable wipe transition.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bitwise Complement** | Inverting every bit in a binary value; maps 0→1023 and 1023→0 in the 10-bit domain. Also called ones-complement or NOT. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **Cascade Dissolve** | A transition effect where tiles in a grid sequentially change state, creating a sweeping reveal pattern. |
| **Cell Index** | The grid coordinate of a tile, used as the comparison value against the sweep threshold. In diagonal mode, the sum of X and Y cell coordinates. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **DVE** | Digital Video Effects; hardware or software that performs real-time spatial transformations on video signals. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived luminance. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **Sweep** | The advancing threshold that determines which tiles are in the flipped state; driven by the frame counter. |
| **Vsync** | Vertical sync pulse marking the start of each video frame; triggers the frame counter increment. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
