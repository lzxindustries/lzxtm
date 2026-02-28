---
draft: true
sidebar_position: 172
slug: /instruments/videomancer/moiré
title: "Moiré"
image: /img/instruments/videomancer/moir%C3%A9/moir%C3%A9_hero.png
description: "Program guide for Moiré, a Videomancer illusion program for the LZX video synthesizer."
---

import moir__before_after from '/img/instruments/videomancer/moiré/moiré_before_after.png';
import moir__control_panel from '/img/instruments/videomancer/moiré/moiré_control_panel.png';
import moir__exercise1_result from '/img/instruments/videomancer/moiré/moiré_exercise1_result.png';
import moir__exercise2_result from '/img/instruments/videomancer/moiré/moiré_exercise2_result.png';
import moir__exercise3_result from '/img/instruments/videomancer/moiré/moiré_exercise3_result.png';
import moir__hero from '/img/instruments/videomancer/moiré/moiré_hero.png';
import moir__source1_kodim01 from '/img/instruments/videomancer/moiré/moiré_source1_kodim01.png';
import moir__source2_kodim02 from '/img/instruments/videomancer/moiré/moiré_source2_kodim02.png';
import moir__source3_kodim01_bw from '/img/instruments/videomancer/moiré/moiré_source3_kodim01_bw.png';

# Moiré

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={moir__hero} alt="Moiré hero image"/>
*Moiré generating dense interference fringes from two rotated grid layers with video-reactive phase modulation.*
<img src={moir__before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Moiré applied.*

---

## Overview

When two periodic patterns are overlaid at slightly different pitches or angles, the result is a third pattern that doesn't exist in either original — a phantom structure that emerges purely from interference. This phenomenon is called a moiré pattern, from the French word for a watered silk textile whose chatoyant shimmer arises from the interference of warp and weft threads. Moiré is simultaneously a precision alignment tool, a visual artifact that print technicians spend careers avoiding, and — in the hands of Op Art pioneers like Bridget Riley and Victor Vasarely — a medium for kinetic visual illusion.

The Moiré program generates two independent grid layers on the FPGA, rotates each to an arbitrary angle, and superimposes them using one of four interference modes. The result is a monochrome pattern field that shifts and shimmers as the grid parameters change. Input video can modulate the phase of Grid B, embedding the source image into the interference structure. A DDS (Direct Digital Synthesis) accumulator animates Grid A's phase offset from frame to frame, creating slow spatial drift even with static input. The output is composited with the input via a wet/dry crossfade.

At zero video modulation, Moiré is a pure pattern generator — the output depends only on the grid pitches, angles, and combination mode. As Video Mod increases, the input video warps the interference fringes, bending straight grid lines around luminance contours. The result sits in an unusual space between synthesis and processing: a generated pattern that responds to incoming imagery.

---

## Background

### The Physics of Moiré Interference

Moiré patterns arise whenever two periodic structures sample each other at slightly mismatched frequencies. The visible fringes represent the **beat frequency** — the difference between the two spatial frequencies. Just as two tuning forks at 440 Hz and 442 Hz produce a 2 Hz audible beat, two grids at 32-pixel and 34-pixel pitch produce wide fringes whose spacing corresponds to the difference frequency. The closer the pitches, the wider the fringes; identical pitches produce a uniform field.

Rotating one grid relative to the other introduces angular interference. Even at identical pitches, a slight angle offset creates diagonal fringes. The fringe direction is perpendicular to the bisector of the two grid angles, and the fringe spacing is inversely proportional to the angle difference. This rotational sensitivity is why moiré patterns are used in precision alignment: a fraction-of-a-degree angular misalignment produces clearly visible fringes.

### Coordinate Rotation and Grid Evaluation

Each grid layer is constructed by rotating screen coordinates through a 2D rotation matrix: $x' = x \cos\theta + y \sin\theta$, $y' = y \cos\theta - x \sin\theta$. The FPGA uses a 32-entry signed lookup table for cosine and sine (8-bit values scaled by 127), so the rotation angle is quantized to 32 steps across 360° — effectively 11.25° per step, though only 180° of unique orientations are exposed via the control range.

After rotation, the coordinates are reduced modulo the grid pitch to produce a cell-local position. A simple threshold at half the pitch generates a square wave — bright where the position falls in the first half of the cell, dark in the second half. This creates the fundamental stripe pattern. For dots (Grid A) or circles (Grid B), both axes or a distance metric are evaluated instead of just one axis.

### Grid Shape Variants

Grid A offers lines or dots. In line mode, only the rotated X coordinate is evaluated, producing parallel stripes. In dot mode, both X and Y are evaluated and ANDed, producing a checkerboard-like dot matrix whose orientation follows the rotation angle.

Grid B offers lines or concentric circles. Circle mode replaces the directional coordinate evaluation with a Chebyshev-approximated distance function: $d \approx \max(|x|, |y|) + \frac{1}{2}\min(|x|, |y|)$. This generates concentric rings whose spacing is set by the pitch control. Combined with rotation, the ring pattern tilts in space, creating interference fringes between the circular B grid and the linear A grid.

### DDS Animation and Video Phase Modulation

A 16-bit Direct Digital Synthesis accumulator increments once per video frame by the Anim Speed register value. The upper 10 bits of the accumulator are added to Grid A's rotated X coordinate, producing a smooth spatial drift — the grid slides horizontally through the interference field. At low speeds, the fringes shift imperceptibly; at high speeds, the pattern scrolls rapidly, creating a shimmering, liquid quality.

Video Mod adds the input luminance (scaled by the modulation depth) to Grid B's rotated X coordinate before pattern evaluation. Bright areas of the input shift Grid B's phase forward; dark areas leave it unperturbed. The net effect is that the interference fringes bend around luminance contours in the source image — straight grid lines develop curves that follow edges and gradients.

### Interference Combination Modes

Two toggles (Combine A and Combine B) select one of four ways to superimpose the two grid patterns:

- **Multiply** (A=0, B=0): $\text{out} = \frac{A \times B}{1024}$. Produces the intersection of both patterns — bright only where both grids are bright. The classic moiré fringe.
- **XOR** (A=1, B=0): Bitwise exclusive-or of the two 10-bit pattern values. Creates a high-frequency alternating pattern at grid intersections.
- **Absolute Difference** (A=0, B=1): $\text{out} = |A - B|$. Highlights regions where the two grids disagree — bright where one grid is on and the other is off.
- **Minimum** (A=1, B=1): $\text{out} = \min(A, B)$. Takes the darker of the two grids at each pixel, producing a union-like effect where dark regions from either grid dominate.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel (used for video modulation only) ──────────────
│   │
│   └── Pipeline delay → s_y_in_s2 for Grid B phase offset
│
├── Position Counters ──────────────────────────────────────
│   ├── H counter (reset on hsync, incr on avid)
│   └── V counter (reset on vsync, incr on avid_start)
│
├── Animation DDS ──────────────────────────────────────────
│   └── 16-bit accumulator += anim_speed per frame
│       └── s_anim_phase = accum(15:6)
│
├── Stage 1: Coordinate Rotation (1 clk) ────────────────
│   ├── Grid A: rx = hc·cos_a + vc·sin_a + anim_phase
│   │           ry = vc·cos_a − hc·sin_a
│   └── Grid B: rx = hc·cos_b + vc·sin_b
│               ry = vc·cos_b − hc·sin_b
│
├── Stage 2: Pattern Evaluation (1 clk) ─────────────────
│   ├── Grid A: lines (X mod pitch) or dots (X&Y mod pitch)
│   └── Grid B: video mod → rx_b offset
│               lines (X mod pitch) or circles (distance mod pitch)
│
├── Stage 3: Interference Combination (1 clk) ───────────
│   └── 4 modes: Multiply / XOR / Abs Diff / Minimum
│       → s_moire (10-bit monochrome)
│
├── Stage 4: Output Composite (1 clk) ──────────────────
│   └── Y = moire, U = 512, V = 512 (monochrome)
│
├── Interpolator: Wet/Dry Mix (4 clks) ─────────────────
│   └── lerp(dry, wet, mix_amount) per Y, U, V
│
└── Bypass ─────────────────────────────────────────────
    └── Select original or processed signal
```

The moiré pattern itself is purely generated — it does not process the input video's pixel values through the pattern pipeline. Input video participates only through the Video Mod path, where luma offsets Grid B's phase coordinate, and through the wet/dry mix, where the pattern is crossfaded with the original. This makes Moiré a hybrid between a synthesis program (the grid patterns are internally generated) and a processing program (the output is composited with input, and luma modulates the pattern). The output is inherently monochrome — U and V are fixed at the neutral midpoint (512) — so the wet/dry mix is the only path for color to appear in the output.

---

## Parameter Reference

<img src={moir__control_panel} alt="Videomancer front panel with Moiré loaded"/>
*Videomancer's front panel with Moiré active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Pitch A
| Property | Value |
|----------|-------|
| Range | 4px – 64px |
| Default | 27px |
| Suffix | px |

Controls the pitch (spatial period) of Grid A. The knob selects one of eight discrete steps from a lookup table: 4, 8, 12, 16, 24, 32, 48, and 64 pixels. Smaller pitches create fine, closely-spaced stripes or dots; larger pitches create broad bands. The pitch interacts multiplicatively with Grid B's pitch to determine the interference fringe spacing — the moiré beat frequency is determined by the ratio and difference of the two pitches. Setting both grids to the same pitch and slightly different angles produces classic angular moiré fringes.

---

#### Knob 2 — Pitch B
| Property | Value |
|----------|-------|
| Range | 4px – 64px |
| Default | 30px |
| Suffix | px |

Controls the pitch of Grid B using the same eight-step lookup table as Grid A. The most dramatic interference fringes appear when the two pitches are close but not identical — for example, Pitch A at 32 and Pitch B at 24 produces wide, slowly varying fringes. When the pitches are identical, only the angular difference between the grids creates interference. When the pitches are very different (e.g., 4 and 64), the interference is less visually coherent and the patterns interact at a fine scale.

---

#### Knob 3 — Angle A
| Property | Value |
|----------|-------|
| Range | 0° – 180° |
| Default | 0° |
| Suffix | ° |

Sets the rotation angle of Grid A. The 10-bit pot value is quantized to one of 32 entries in a cosine/sine lookup table, covering 0° to approximately 180° in steps of about 5.6°. At 0°, Grid A produces vertical stripes (or a vertical dot grid). Rotating Grid A while leaving Grid B fixed sweeps the interference fringe orientation across the image. Even small angular differences between the two grids produce large-scale fringes, making this a sensitive control for fine-tuning the interference pattern.

---

#### Knob 4 — Angle B
| Property | Value |
|----------|-------|
| Range | 0° – 180° |
| Default | 23° |
| Suffix | ° |

Sets the rotation angle of Grid B, using the same 32-entry lookup table as Angle A. The relative angle between the two grids is the primary control for fringe orientation and spacing — the fringes run perpendicular to the angle bisector. Setting both angles equal eliminates angular interference, leaving only pitch-ratio effects. Sweeping Angle B while holding Angle A fixed rotates the entire interference pattern.

---

#### Knob 5 — Anim Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the DDS animation speed. At zero, the grid pattern is static. Increasing the value adds a per-frame phase increment to Grid A's rotated X coordinate via a 16-bit accumulator. The visible effect is a steady horizontal drift of Grid A through the interference field, causing the fringes to slide, pulse, and shimmer. At low settings, the motion is a slow, tidal drift; at high settings, the pattern scrolls rapidly and the interference fringes flicker. The animation is built into the FPGA's frame timing, so it requires no input signal — it runs even with static or black input.

---

#### Knob 6 — Video Mod
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls how strongly input luminance modulates Grid B's phase. At zero, Grid B's pattern is purely geometric — unaffected by the input video. As Video Mod increases, the rotated X coordinate of Grid B is offset by a value proportional to the input luma. Bright pixels push Grid B's stripes or circles forward; dark pixels leave them in place. The resulting interference fringes bend around luminance edges in the source, embedding a ghostly impression of the input imagery into the moiré structure. At maximum modulation, the grid structure is heavily warped by the input, and the interference fringes become contour lines of the source luminance.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Grid A** | Lines | Dots |
| **8 — Grid B** | Lines | Circles |
| **9 — Combine A** | Multiply | XOR |
| **10 — Combine B** | Diff | Min |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 select the geometric shape of each grid layer independently. Toggles 9 and 10 form a 2-bit combiner mode selector that determines how the two grid patterns are superimposed. Toggle 11 is the standard bypass. The most dramatic changes come from the combiner mode pair — the four modes produce fundamentally different interference textures from the same grid geometry.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry crossfade between the original input video and the moiré output. At 0%, the output is the unmodified input. At 100%, the output is the full moiré pattern (monochrome, as U and V are fixed at 512). Intermediate positions blend the monochrome moiré with the original color video, producing a ghostly overlay effect where the interference fringes modulate the source image. Because the moiré output is monochrome, increasing the mix also desaturates the output.

---

## Guided Exercises

These exercises move from basic grid visualization through interference tuning to video-reactive pattern modulation. Each introduces a new dimension of the program's behavior.

### Exercise 1: Pitch-Ratio Interference

<img src={moir__exercise1_result} alt="Pitch-Ratio Interference result"/>
*Pitch-Ratio Interference — simulated result across source images.*
**Source**: A static test pattern or color bars — any stable image for observing interference fringes without motion.

**Objective**: Learn how the ratio and difference of the two grid pitches control the moiré fringe spacing.

1. **Baseline**: Set both pitches to 16 px with both angles at 0°. The two grids are identical — the output is a uniform stripe pattern with no interference.
2. **Pitch offset**: Change Pitch B to 12 px. Wide moiré fringes appear as the two frequencies beat against each other.
3. **Closer pitches**: Change Pitch B to 24 px. The fringe spacing changes — the beat frequency depends on the pitch ratio.
4. **Fine fringes**: Set Pitch A to 48 and Pitch B to 64. The close ratio produces broadly spaced fringes.
5. **Angular interference**: Return both pitches to 16 px. Slowly rotate Angle B. Diagonal fringes appear from the angular difference alone.

**Key concepts**: Moiré fringes arise from the beat frequency between two spatial frequencies, pitch ratio determines fringe spacing, angular difference creates diagonal fringes

---

### Exercise 2: Shape and Mode Exploration

<img src={moir__exercise2_result} alt="Shape and Mode Exploration result"/>
*Shape and Mode Exploration — simulated result across source images.*
**Source**: A simple geometric pattern or gradient test card.

**Objective**: Explore how grid shapes and combination modes produce different interference textures.

1. **Dots vs lines**: Set Pitch A to 8, Pitch B to 12, Angle A to 0°, Angle B to ~45°. Switch Grid A between Lines and Dots — observe how the dot grid creates denser, two-dimensional interference.
2. **Circles**: Switch Grid B to Circles. Radial spoke-like fringes appear from the line/circle interaction.
3. **XOR mode**: Switch Combine A to XOR. The smooth fringes become high-contrast digital patterns.
4. **Minimum mode**: Set Combine A to XOR, Combine B to Min. The output takes the darker of the two patterns — dark stripes from both grids appear simultaneously.
5. **Abs Difference**: Set Combine A to Multiply, Combine B to Min. Boundary regions between the grids light up.

**Key concepts**: Grid shapes create different interference geometries, combination modes generate fundamentally different textures from identical grids, circles produce radial fringes

---

### Exercise 3: Video-Modulated Animation

<img src={moir__exercise3_result} alt="Video-Modulated Animation result"/>
*Video-Modulated Animation — simulated result across source images.*
**Source**: A live camera feed or footage with high-contrast subjects and clear luminance edges.

**Objective**: Combine video modulation and DDS animation to create a reactive, evolving moiré field.

1. **Video embedding**: Set Video Mod to ~60%. The moiré fringes bend around luminance contours in the source, revealing a ghostly imprint of the input.
2. **Animation**: Increase Anim Speed to ~20%. Grid A drifts through the interference, causing fringes to pulse and shift while maintaining their visual lock to the source luminance.
3. **Mix blending**: Set Mix to ~50%. The monochrome moiré blends with the original color video, creating a semi-transparent pattern overlay.
4. **Circle interference**: Switch Grid B to Circles. The video-modulated circles create concentric ripples centered on luminance features.
5. **Speed sweep**: Slowly increase Anim Speed to maximum. The pattern becomes a rapid shimmer over the source.

**Key concepts**: Video Mod embeds input luminance into the interference structure, animation creates temporal evolution independent of input motion, partial Mix preserves source color beneath the pattern

---


## Tips

- **Start with identical grids**: Set both pitches and angles equal, then slowly offset one parameter at a time. This builds intuition for how each variable contributes to the interference.
- **Pitch ratio matters more than absolute pitch**: Two grids at 8 and 12 px produce the same fringe pattern shape as two grids at 32 and 48 px (both are 2:3 ratios), just at different spatial scales.
- **Small angles, big fringes**: The angular sensitivity is high — a single LUT step (~5.6°) produces dramatic fringes. Use small angular offsets for large-scale, slowly varying patterns.
- **Circles add radial structure**: Switching Grid B to Circles introduces spoke-like and spiral interference that is impossible with two line grids alone.
- **Video Mod for reactive patterns**: Even a small amount of Video Mod (10–20%) bends the grid fringes enough to create a visible impression of the input content within the moiré field.
- **Animation for temporal texture**: Low Anim Speed values (5–15%) create a hypnotic, slowly evolving shimmer. High values produce rapid flicker that can serve as a modulation source for downstream programs.
- **Mix for overlay compositing**: At 30–50% Mix, the monochrome moiré serves as a semi-transparent texture layer over the original color video.

---

## Glossary

| Term | Definition |
|------|------------|
| **Beat Frequency** | The difference frequency produced when two periodic signals of slightly different frequencies interact; in moiré patterns, this determines the spacing of the visible fringes. |
| **Chebyshev Distance** | An approximation of Euclidean distance using $\max(|x|, |y|)$; used here with a correction term for circle pattern generation. |
| **DDS** | Direct Digital Synthesis; a technique for generating arbitrary waveforms using a phase accumulator and lookup table. |
| **Fringe** | A visible band or contour in a moiré pattern, caused by constructive or destructive interference between two periodic structures. |
| **Interference** | The phenomenon where overlapping periodic patterns create new visible structures (fringes) at the beat frequency. |
| **LUT** | Lookup Table; a pre-computed array of values indexed by an input parameter, used here for trigonometric functions and pitch decoding. |
| **Moiré** | A pattern arising from the superposition of two periodic structures, named after watered silk fabric. |
| **Phase Accumulator** | A counter that wraps around at a fixed modulus, used in DDS to generate a linearly advancing phase that can be converted to a spatial offset. |
| **Square Wave** | A periodic signal alternating between two levels (here, 0 and 1023) at a duty cycle of 50%, used to generate grid stripe patterns. |
| **XOR** | Exclusive OR; a bitwise operation that outputs 1 where the two inputs differ, creating high-contrast digital interference patterns. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
