---
draft: true
sidebar_position: 144
slug: /instruments/videomancer/jacquard
title: "Jacquard"
image: /img/instruments/videomancer/jacquard/jacquard_hero.png
description: "The Jacquard loom, invented in 1804 by Joseph Marie Jacquard, was the first machine to use punched cards for controlling the pattern of a weave."
---

import jacquard_hero from '/img/instruments/videomancer/jacquard/jacquard_hero.png';
import jacquard_before_after from '/img/instruments/videomancer/jacquard/jacquard_before_after.png';
import jacquard_control_panel from '/img/instruments/videomancer/jacquard/jacquard_control_panel.png';
import jacquard_exercise1_result from '/img/instruments/videomancer/jacquard/jacquard_exercise1_result.png';
import jacquard_exercise2_result from '/img/instruments/videomancer/jacquard/jacquard_exercise2_result.png';
import jacquard_exercise3_result from '/img/instruments/videomancer/jacquard/jacquard_exercise3_result.png';

# Jacquard

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={jacquard_hero} alt="Jacquard hero image"/>
*Jacquard weaving video pixels into interlaced textile patterns with warp and weft hue tinting.*
<img src={jacquard_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Jacquard applied.*

---

## Overview

The Jacquard loom, invented in 1804 by Joseph Marie Jacquard, was the first machine to use punched cards for controlling the pattern of a weave. It is often cited as a conceptual ancestor of digital computing — each card row encoded a binary instruction (raise thread / lower thread) that determined whether a warp or weft thread appeared on the fabric surface at each intersection. Jacquard applies this idea to video: it divides the image into a grid of cells, and at each cell, a binary pattern lookup determines whether the pixel belongs to a warp thread (running vertically) or a weft thread (running horizontally).

The four available weave patterns — Plain, Twill, Satin, and Herringbone — are stored as 8×8 bit arrays and tiled across the frame. Warp threads can be tinted toward one hue while weft threads are tinted toward another, with an adjustable tint strength. Under-threads (the ones that pass behind at each crossing) are darkened by a configurable shadow amount, simulating the depth of a real woven fabric. An LFSR noise generator adds subtle per-pixel irregularity that mimics the imperfections of physical thread.

At full tint with contrasting warp and weft hues, Jacquard transforms video into a vivid tartan or plaid-like textile. At low tint with high shadow, it creates a subtle canvas or linen texture overlaid on the source. The Grid Show toggle reveals the underlying cell boundaries, exposing the digital loom structure.

---

## Background

### Weave Patterns and Binary Matrices

In real weaving, the pattern of a fabric is defined by which thread goes over and which goes under at every crossing point. This can be described as a binary matrix: a 1 means the warp thread is on top, a 0 means the weft thread is on top. A plain weave alternates 1-0-1-0 in both directions like a checkerboard. A twill weave offsets the pattern diagonally, producing characteristic diagonal ridges (think denim). A satin weave scatters the crossover points to minimise visible texture, creating a smooth surface. Herringbone is a twill variant where the diagonal direction reverses at regular intervals, producing a V-shaped zigzag.

### The Jacquard Loom and Computing History

Joseph Marie Jacquard's 1804 loom used punched cards to automate the selection of warp threads. Each hole in the card corresponded to a hook that lifted a specific thread, creating complex patterns without manual intervention. Charles Babbage recognised the significance of this mechanism and adapted the concept for his Analytical Engine. Ada Lovelace described the connection explicitly: "The Analytical Engine weaves algebraical patterns, just as the Jacquard loom weaves flowers and leaves." Jacquard brings this full circle — using digital binary logic to simulate the loom that inspired digital computing.

### Hue Tinting via UV Offset

In YUV colour space, hue is determined by the angle of the (U, V) vector around the neutral point (512, 512). Jacquard uses an 8-entry lookup table that maps hue angles (0°, 45°, 90°, …, 315°) to (U, V) offset pairs. The Tint Amount control scales these offsets before they are added to each pixel's native chrominance. At zero tint, the original video colours are preserved. At full tint, the colours shift strongly toward the selected hue. Since warp and weft threads use independent hue lookups, two-tone colourisation follows the weave pattern automatically.

### Shadow and Depth Perception

The illusion of three-dimensional weave structure comes from darkening the thread that passes underneath at each crossing. In a real fabric, the under-thread is partially occluded by the over-thread and receives less light. Jacquard simulates this by multiplying the Y (luma) channel of under-thread pixels by a shadow factor: at zero shadow, both threads have equal brightness; at maximum shadow, under-threads are rendered dramatically darker, creating strong depth contrast at every crossing point.

### LFSR Noise as Textile Irregularity

Real textiles are never perfectly uniform. Thread thickness varies, dye absorption is uneven, and mechanical tension fluctuates during weaving. Jacquard adds a 16-bit Linear Feedback Shift Register (LFSR) pseudo-random noise source that injects small brightness perturbations on a per-pixel basis. The noise amplitude is fixed at ±8 luma levels — subtle enough to add organic texture without disrupting the weave pattern. The LFSR is seeded with a fixed value (0xCAFE) so the noise pattern is deterministic and repeatable.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Grid Coordinate Extraction ────────────────────────
│   ├─ Divide pixel position by Thread Width → cell coordinates
│   ├─ Cell (x mod 8, y mod 8) → pattern lookup
│   ├─ Pattern LUT: Plain / Twill / Satin / Herringbone
│   └─ Output: is_warp_over flag + boundary detection
│
├── Stage 2: Tint + Shadow ────────────────────────────────────
│   ├─ Warp-over: apply Warp Hue tint to U/V, full brightness
│   ├─ Weft-over: apply Weft Hue tint to U/V, darkened by Shadow
│   ├─ Tint Amount scales hue offset strength
│   └─ Color Src toggle: Tint mode or Video passthrough
│
├── Stage 3: Composite ────────────────────────────────────────
│   ├─ Grid Show: draw dark lines at cell boundaries
│   ├─ Noise: add LFSR jitter to Y channel
│   └─ Clamp outputs to 0–1023
│
├── Stage 4: Output Registration ──────────────────────────────
│
├── 4-Clock Interpolator (wet/dry mix per channel) ────────────
│
├── Sync Signals ──────────────────────────────────────────────
│   └─ 8-clock delay pipeline (hsync, vsync, field)
│
└── Bypass ────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The weave pattern is stateless and purely combinational — there is no frame buffer or memory of previous pixels. The cell coordinates are derived from running horizontal and vertical position counters, and the pattern lookup is an instantaneous ROM read from one of four 8×8 bit arrays. This means the pattern tiles seamlessly across the frame regardless of resolution, and Thread Width changes take effect immediately on the next pixel.

The colour tinting path has an important toggle: Color Src selects whether the U/V channels are modified by the hue LUT (Tint mode) or passed through from the input (Video mode). In Video mode, the original video colours are preserved — only the luma channel is affected by the weave shadow pattern, producing a contrast-texture overlay rather than a colour remapping.

---

## Parameter Reference

<img src={jacquard_control_panel} alt="Videomancer front panel with Jacquard loaded"/>
*Videomancer's front panel with Jacquard active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Thread W
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 7 |

Selects the thread width — the number of pixels per weave cell — from an 8-step lookup table. The available widths are 2, 3, 4, 5, 6, 8, 10, and 16 pixels. Small widths create a fine, dense textile texture; large widths create coarse, blocky weave patterns. At width 2, the weave is just barely visible as a fine grid. At width 16, individual threads are clearly distinguishable as wide bars. The weave pattern tiles across the frame based on this width, so the total number of visible cells depends on both the thread width and the frame resolution.

---

#### Knob 2 — Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the density of thread coverage. Higher density values produce tighter, more solid-looking fabric; lower values create a looser, more open weave appearance. Density interacts with the shadow system — denser weaves show more continuous colour from the over-thread, while sparser weaves reveal more of the darkened under-thread, increasing the visual depth of the texture.

---

#### Knob 3 — Warp Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 60° |
| Suffix | ° |

Selects the hue for warp (vertical) threads. The control maps through an 8-entry lookup table covering eight hues spaced at 45° intervals around the colour wheel: red, orange, yellow-green, green, cyan, blue, purple, and magenta. The selected hue is applied as a UV offset scaled by the Tint Amount control. When Color Src is set to Video, this control has no visible effect — the original chrominance is preserved.

---

#### Knob 4 — Weft Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 240° |
| Suffix | ° |

Selects the hue for weft (horizontal) threads, using the same 8-entry hue lookup table as Warp Hue. Choosing contrasting warp and weft hues (e.g., red warp + cyan weft) produces vivid tartan-like patterns. Similar hues (e.g., blue warp + purple weft) produce subtler tonal variation within the weave. Setting both to the same hue produces a monochromatic tint with only shadow depth distinguishing the threads.

---

#### Knob 5 — Tint Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the strength of the hue tint applied to both warp and weft threads. At zero, no colour shifting occurs — the original video chrominance is preserved (equivalent to Color Src = Video). At maximum, the UV channels are shifted fully toward the selected hue values. Intermediate values produce a partial blend between the original colours and the thread hues.

---

#### Knob 6 — Shadow
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the depth of shadow applied to under-threads. At zero, all threads (over and under) have equal brightness — the weave pattern is visible only through colour differences. As shadow increases, under-threads become progressively darker, creating the illusion of three-dimensional interlacing. At maximum, under-threads are rendered as deep shadows, producing high-contrast weave structures that look almost embossed.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Plain | Twill |
| **8 — Noise** | Off | On |
| **9 — Color Src** | Tint | Video |
| **10 — Grid Show** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control qualitatively different aspects of the program. Pattern is a 2-bit selector (using bits 0 and 1 of the toggle register) that chooses among four weave structures. Noise enables LFSR-based texture irregularity. Color Src selects between hue-tinted and video-passthrough colour modes. Grid Show overlays cell boundary lines for diagnostic visibility. Bypass is at bit 5 (shifted from the standard bit 4 position), routing the input directly to the output. Note the non-standard bypass bit position — this is specific to Jacquard.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed (woven) signal and the delayed dry input signal. At 100%, the output shows the full textile effect. At 0%, the output is the original input. Intermediate values blend the weave texture with the source, creating a semi-transparent overlay that lets the original image show through the fabric pattern. This is particularly useful at 30–50% mix, where the weave adds subtle canvas texture to an otherwise normal image.

---

## Guided Exercises

These exercises explore Jacquard's textile simulation from basic weave patterns to complex colourised fabrics. Each builds on the previous, introducing more of the program's parameter interactions.

### Exercise 1: Basic Weave Patterns

<img src={jacquard_exercise1_result} alt="Basic Weave Patterns result"/>
*Basic Weave Patterns — simulated result across source images.*
**Source**: A static image or live camera feed with varied colour and contrast — a face, landscape, or still life.

**Objective**: Compare the four weave patterns and understand thread width scaling.

1. **Plain weave**: Set Pattern to Plain. Set Thread Width to step 4 (width = 5 pixels). The image breaks into a checkerboard of lighter and darker squares.
2. **Increase shadow**: Sweep Shadow to ~60%. The under-thread squares darken, making the weave structure clearly visible.
3. **Twill diagonal**: Switch Pattern to Twill. The checkerboard is replaced by diagonal stripes running lower-left to upper-right.
4. **Satin smooth**: Switch to Satin. The crossover points scatter — the texture appears smoother and less structured.
5. **Herringbone V**: Switch to Herringbone. The diagonal reverses at the midpoint, creating a V-shaped zigzag.
6. **Scale up**: Increase Thread Width to step 8 (width = 16). Each pattern becomes very coarse — individual threads are thick bars.
7. **Scale down**: Decrease Thread Width to step 1 (width = 2). The weave becomes an almost imperceptibly fine texture.

**Key concepts**: Four binary weave patterns tiled as 8×8 matrices, thread width controls cell size, shadow reveals the over/under structure

---

### Exercise 2: Tartan Colourisation

<img src={jacquard_exercise2_result} alt="Tartan Colourisation result"/>
*Tartan Colourisation — simulated result across source images.*
**Source**: A well-lit face or portrait — skin tones provide a good neutral base for colour tinting.

**Objective**: Use contrasting warp and weft hues to create tartan-like two-tone fabric.

1. **Contrasting hues**: Set Warp Hue to ~60° (red) and Weft Hue to ~240° (cyan-blue). Set Tint Amount to ~70%.
2. **Increase shadow**: Shadow to ~50%. The under-thread darkening creates clear depth between the two coloured thread sets.
3. **Twill pattern**: Switch to Twill. The diagonal ridges now show alternating colour bands — a tartan effect.
4. **Reduce scale**: Set Thread Width to step 3 (width = 4). The tartan becomes finer, resembling a dress fabric scale.
5. **Add noise**: Enable Noise. Subtle irregularity appears in the thread brightness, adding organic texture.
6. **Show grid**: Enable Grid Show. Dark boundary lines appear at every cell edge, revealing the digital loom structure beneath the colour.

**Key concepts**: 8-entry hue LUT maps register position to colour wheel angle, warp and weft hues are independent, tint amount scales UV offset

---

### Exercise 3: Canvas Texture Overlay

<img src={jacquard_exercise3_result} alt="Canvas Texture Overlay result"/>
*Canvas Texture Overlay — simulated result across source images.*
**Source**: Any footage where you want to add a subtle fabric texture — landscapes, abstract video, or recorded material.

**Objective**: Create a subtle canvas or linen overlay that preserves the original video colours.

1. **Video colour mode**: Set Color Src to Video. The original colours are now preserved — only luma is affected.
2. **Fine weave**: Set Thread Width to step 2 (width = 3). The texture is fine and dense.
3. **Subtle shadow**: Set Shadow to ~25%. A gentle darkening at under-thread crossings creates the impression of canvas grain.
4. **Plain weave**: Use Plain pattern for the most uniform canvas texture.
5. **Partial mix**: Set Mix to ~40%. The canvas texture blends with the source, adding a painted-on-fabric quality.
6. **Add noise**: Enable Noise for additional organic irregularity. The result resembles video projected onto a linen surface.

**Key concepts**: Video colour mode preserves original chrominance, partial mix blends texture with source, fine thread width creates canvas grain

---


## Tips

- **Start with shadow**: Shadow is the control that most clearly reveals the weave pattern. Set it to 40–60% before adjusting other parameters.
- **Plain for texture, Twill for stripes**: Plain creates uniform background texture; Twill creates more directional, fabric-like diagonal ridges.
- **Herringbone is the showstopper**: The V-zigzag pattern is the most visually distinctive and immediately reads as "woven fabric."
- **Video mode for subtlety**: Set Color Src to Video and use shadow only for a subtle canvas-grain overlay that preserves the original colour.
- **Small widths disappear at low res**: At SD resolution (720 pixels wide), thread width 2 is essentially invisible. Use width 4+ for visible texture at SD.
- **Noise adds realism**: The LFSR noise is very subtle (±8 levels on a 1024 scale) but adds perceptible organic quality, especially at larger thread widths.
- **Bypass is at bit 5**: If writing automation, note that Jacquard's bypass bit is shifted to position 5 rather than the standard position 4.
- **Feedback creates plaid layers**: Routing the output back into the input with a different pattern selection creates layered weave-on-weave structures.

---

## Glossary

| Term | Definition |
|------|------------|
| **Herringbone** | A weave pattern where the twill diagonal reverses direction at regular intervals, producing a V-shaped zigzag. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function of its previous state, generating pseudo-random sequences. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Plain Weave** | The simplest weave structure, alternating over-under like a checkerboard. |
| **Satin Weave** | A weave where crossover points are scattered to minimise visible texture, creating a smooth fabric surface. |
| **Shadow** | Darkening applied to threads that pass underneath at each crossing, simulating depth in the weave. |
| **Tint** | A colour shift applied to the U and V channels, steering a pixel's hue toward a target colour. |
| **Twill Weave** | A weave where diagonal ridges are formed by offsetting the over/under pattern one position per row. |
| **UV Offset** | A signed displacement applied to the chrominance channels (U, V) to shift the pixel's hue. |
| **Warp** | Threads running vertically in a weave; in Jacquard, associated with the Warp Hue control. |
| **Weft** | Threads running horizontally in a weave; in Jacquard, associated with the Weft Hue control. |
| **YUV** | A colour encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
