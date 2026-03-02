---
draft: true
sidebar_position: 127
slug: /instruments/videomancer/harlequin
title: "Harlequin"
image: /img/instruments/videomancer/harlequin/harlequin_hero.png
description: "The Atari Video Music (model C240) was released in 1977 — a consumer device that plugged into a television and translated stereo audio into geometric color patterns."
---

import harlequin_hero from '/img/instruments/videomancer/harlequin/harlequin_hero.png';
import harlequin_before_after from '/img/instruments/videomancer/harlequin/harlequin_before_after.png';
import harlequin_control_panel from '/img/instruments/videomancer/harlequin/harlequin_control_panel.png';
import harlequin_exercise1_result from '/img/instruments/videomancer/harlequin/harlequin_exercise1_result.png';
import harlequin_exercise2_result from '/img/instruments/videomancer/harlequin/harlequin_exercise2_result.png';
import harlequin_exercise3_result from '/img/instruments/videomancer/harlequin/harlequin_exercise3_result.png';

# Harlequin

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={harlequin_hero} alt="Harlequin hero image"/>
*Harlequin rendering tiled Manhattan distance diamonds over a video source, colored by DDS hue cycling and modulated by IIR-averaged luminance.*
<img src={harlequin_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Harlequin applied.*

---

## Overview

The Atari Video Music (model C240) was released in 1977 — a consumer device that plugged into a television and translated stereo audio into geometric color patterns. Its signature visual was the diamond: sharp-edged shapes that pulsed and grew in response to the music's stereo channels, tiled across the screen in selectable repeating grids. Harlequin recreates this aesthetic using video luminance as the driving signal instead of audio, generating Manhattan distance diamond fields whose sizes respond to the brightness of the upper and lower halves of the incoming image.

The name *Harlequin* references the diamond-patterned costume of the commedia dell'arte character — a motley of repeating diamond shapes in contrasting colors. It is also apt because the program's output is inherently theatrical: bold geometric forms, cycling rainbow hues, and a repertoire of shape modes that the hardware can shuffle automatically.

At conservative settings with a single tile and solid fill, Harlequin produces a single centered diamond that gently breathes with the source video's luminance. At extreme settings with maximum tiling, ring mode, fast hue cycling, and auto cycle enabled, the screen fills with a kaleidoscopic grid of pulsing diamond outlines in rapidly shifting colors — a faithful recreation of the Atari Video Music experience, driven by light instead of sound.

---

## Background

### What Is Manhattan Distance?

In everyday geometry, the distance between two points is measured in a straight line — the Euclidean distance. **Manhattan distance** (also called taxicab distance or L1 norm) measures distance differently: it sums the absolute horizontal and vertical displacements, as if you were navigating a grid of city blocks. Where Euclidean distance produces circles, Manhattan distance produces *diamonds* — rotated squares whose corners point up, down, left, and right. Harlequin computes the Manhattan distance from each pixel to the center of its tile, then compares that distance against a threshold to determine whether the pixel is inside or outside the diamond shape.

### What Is IIR Averaging?

Harlequin's diamonds don't just sit at a fixed size — they respond to the video content. The program divides the screen into upper and lower halves and computes a running average of the luminance for each half. This is done with an **IIR (Infinite Impulse Response) filter**, a simple feedback loop: the new average equals the old average plus a small fraction of the difference between the incoming pixel's brightness and the current average. The Contour control adjusts the smoothing constant — higher values make the average change more slowly, so the diamonds breathe gently rather than jittering with every pixel. The upper-half average drives the outer diamond size; the lower-half average drives the inner diamond size.

### What Is DDS Hue Cycling?

The color of Harlequin's diamonds comes from a **Direct Digital Synthesis (DDS)** oscillator that sweeps through the hue spectrum. A phase accumulator increments by a fixed amount every frame. The accumulated phase indexes into a quarter-wave sine lookup table (256 entries) to produce sine and cosine values, which are used to generate U and V chrominance components. The result is a smooth, continuous rotation through the color wheel. The Color Speed control sets the accumulator increment — at zero the hue is static, at maximum it cycles rapidly through the entire spectrum.

### What Is Tiling?

Harlequin can replicate its diamond pattern across the screen in a grid. The tiling system divides the 1280×720 active area into equal rectangular cells using preset tile counts: horizontally {1, 2, 3, 5} and vertically {1, 2, 4, 8}. Each tile contains its own centered diamond computed from the same Manhattan distance function. At 5×8 tiling, the screen fills with 40 independent diamond shapes — all responding to the same luminance averages, but each computed from its own local tile coordinates.

### Shape Modes: Solid, Hole, and Ring

The original Atari Video Music had push buttons to select different display modes. Harlequin faithfully recreates three of these. **Solid** mode fills the diamond entirely — any pixel whose Manhattan distance is less than the threshold is lit. **Hole** mode renders the outer diamond but cuts out any pixel that falls inside the inner diamond, creating a diamond-shaped annular region. **Ring** mode draws only the outline of each diamond — pixels within a narrow band around the threshold boundary are lit, and everything else is dark. The Fader control has a dual purpose: it sets the wet/dry mix *and* the ring thickness, since the VHDL implementation uses the same register for both.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Luminance Analysis ─────────────────────────────────────────
│   │
│   ├─ 1. IIR Average — Upper Half   (running average → outer diamond size)
│   └─ 2. IIR Average — Lower Half   (running average → inner diamond size)
│
├── Diamond Rendering ──────────────────────────────────────────
│   │
│   ├─ 3. Tile Coordinate              (modular pixel position within tile)
│   ├─ 4. Manhattan Distance           (|dx| + |dy| from tile center)
│   ├─ 5. Shape Mode Threshold         (solid / hole / ring select)
│   ├─ 6. DDS Hue Color Generation     (quarter-wave sine LUT → YUV)
│   └─ 7. Background Composite         (diamond color or video/black)
│
├── Auto Cycle ─────────────────────────────────────────────────
│   └─ LFSR (seed 0xB1A5)             (randomizes shape/ring every ~4s)
│
├── Mix Stage ──────────────────────────────────────────────────
│   └─ 8. Interpolator × 3             (wet/dry crossfade, 4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay-aligned pass-through (9 clocks)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

Two signal paths feed into the diamond rendering. First, the **IIR luminance analysis** divides the frame vertically at scanline 360 — pixels in the upper half update the outer diamond average, and pixels in the lower half update the inner diamond average. The Contour knob controls the IIR smoothing constant, determining how quickly or slowly the diamond sizes track changes in the source video. Second, the **tile coordinate system** wraps pixel positions modulo the tile dimensions to produce repeating tile-local coordinates. The Manhattan distance is computed from these local coordinates, so every tile gets its own centered diamond. The diamond color comes from the DDS hue oscillator, which is independent of both the source video and the diamond geometry — it cycles continuously regardless of other settings. The Fader register serves double duty: it controls both the interpolator's wet/dry mix *and* the ring thickness in ring mode, meaning that pulling the fader down simultaneously narrows the ring outline and fades toward the dry signal.

---

## Parameter Reference

<img src={harlequin_control_panel} alt="Videomancer front panel with Harlequin loaded"/>
*Videomancer's front panel with Harlequin active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Outer Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 62.6% |
| Suffix | % |

Controls the gain applied to the upper-half IIR average before it becomes the outer diamond's radius. At low values the outer diamond stays small even when the upper portion of the source video is bright. At high values the outer diamond responds aggressively to luminance changes, filling a large portion of each tile when the upper half of the image is bright. This control and Inner Gain (Knob 2) together determine the balance between the two nested diamond fields.

---

#### Knob 2 — Inner Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the gain applied to the lower-half IIR average, which drives the inner diamond's radius. In Hole mode the inner diamond carves a cutout from the outer diamond, so this control determines how much of the center is removed. In Solid mode the inner diamond is not separately visible, but its average is still tracked internally and becomes relevant if you switch to Hole or Ring mode.

---

#### Knob 3 — Color Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the increment of the DDS phase accumulator that drives hue cycling. At zero the hue is frozen at whatever phase the accumulator has reached. As the value increases the diamond color cycles through the full spectrum faster, producing a rainbow sweep effect. The hue generation is computed from a quarter-wave sine lookup table — 256 entries covering one quadrant, mirrored and negated to cover the full 360 degrees — which is indexed by the upper bits of the 32-bit phase accumulator.

---

#### Knob 4 — Contour
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the IIR smoothing constant for the luminance averaging filters. Higher values produce heavier smoothing, so the diamond sizes change slowly and gently even when the source video has rapid brightness fluctuations. Lower values let the diamonds track luminance changes more tightly, creating jittery or percussive responses. This also affects the contour blend at shape boundaries — smoother averaging produces cleaner diamond edges because the threshold value changes less from frame to frame.

---

#### Knob 5 — H Tiles
| Property | Value |
|----------|-------|
| Range | 1 – 5 |
| Default | 1 |

Selects the horizontal tile count from the preset table {1, 2, 3, 5}. The control operates in four discrete steps — the upper two bits of the 10-bit register select the preset index. At 1 tile the diamond spans the full screen width. At 5 tiles the screen is divided into five equal columns, each containing its own diamond. The non-power-of-two values (3, 5) produce even divisions of the 1280-pixel active width.

---

#### Knob 6 — V Tiles
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 1 |

Selects the vertical tile count from the preset table {1, 2, 4, 8}. Combined with H Tiles, this creates a grid of diamonds. At 1×1 there is a single centered diamond. At 5×8 there are 40 diamonds on screen simultaneously. Large tile counts produce smaller diamonds because each tile occupies a smaller portion of the screen. Vertical tiling interacts with the IIR averaging — the upper/lower half split at scanline 360 is independent of the tile boundaries, so all tiles respond to the same two luminance averages.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Shape** | Solid | Hole |
| **8 — Ring** | Fill | Ring |
| **9 — Auto Cycle** | Off | On |
| **10 — Video BG** | Black | Video |
| **11 — Bypass** | Off | On |

Switches 7–10 control four independent aspects of the diamond rendering. Switches 7 and 8 together select the shape mode: Solid (both off), Hole (7 on, 8 off), Ring (8 on, regardless of 7 in ring mode — see VHDL). Switch 9 enables an autonomous LFSR-driven randomizer that overrides switches 7 and 8. Switch 10 selects the background behind the diamonds. Switch 11 is the standard bypass. Unlike some programs where toggles form a combined binary selector, here switches 7 and 8 define a shape taxonomy while 9 and 10 are independent modifiers.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

This control serves a dual purpose in the VHDL implementation. As the wet/dry mix parameter, it crossfades between the original input video and the diamond-rendered output via three interpolator instances (Y, U, V). Simultaneously, the same register value is used to compute the ring thickness in Ring mode — the upper bits of the fader value set the pixel-width of the diamond outline. Pulling the fader down therefore narrows the ring *and* fades toward the dry signal. At maximum the diamond output is at full strength and rings are at their widest; at minimum the output approaches the original video and rings are at their thinnest (clamped to a minimum of 2 pixels).

---

## Guided Exercises

These exercises progress from a single static diamond to a full tiled, color-cycling, auto-randomizing display. Each builds on the previous by engaging more of Harlequin's shape and color controls.

### Exercise 1: Single Breathing Diamond

<img src={harlequin_exercise1_result} alt="Single Breathing Diamond result"/>
*Single Breathing Diamond — simulated result across source images.*
**Source**: A camera feed or recorded footage with distinct bright and dark regions — faces against dark backgrounds or sky/ground compositions work well.

**Objective**: Learn how the IIR luminance analysis drives diamond size and how Outer Gain and Contour interact.

1. **Single diamond**: Confirm H Tiles and V Tiles are at their minimum position (1 tile each). A single large diamond should appear centered on screen.
2. **Outer Gain sweep**: Slowly increase Outer Gain from zero. Watch the diamond grow as the video's upper-half brightness is amplified. With a bright source the diamond can fill most of the screen.
3. **Inner Gain sweep**: Now increase Inner Gain. In Solid mode the inner diamond is not separately visible — note that nothing changes visually yet.
4. **Contour smoothing**: Sweep the Contour knob while the source is changing. At low values the diamond jitters rapidly with brightness changes. At high values it breathes slowly and smoothly.
5. **Video background**: Toggle Video BG (Switch 10) to On. The black background is replaced by the source video, and the diamond becomes a colored overlay.

**Key concepts**: Manhattan distance creates diamond shapes, IIR averaging smooths luminance-to-size mapping, Contour controls temporal responsiveness

---

### Exercise 2: Hole and Ring Modes

<img src={harlequin_exercise2_result} alt="Hole and Ring Modes result"/>
*Hole and Ring Modes — simulated result across source images.*
**Source**: Footage with a strong brightness gradient between the upper and lower halves of the frame — a horizon line, or a subject lit from above.

**Objective**: Explore the three shape modes and see how Inner Gain creates the hole cutout.

1. **Prepare**: Set H Tiles to 1, V Tiles to 1, Outer Gain ~60%, Inner Gain ~40%, Color Speed ~20%.
2. **Solid mode**: With Shape set to Solid and Ring set to Fill, observe the single filled diamond.
3. **Hole mode**: Flip Shape to Hole. The inner diamond is now cut out, leaving a diamond-shaped frame. Adjust Inner Gain to control how much of the center is removed.
4. **Ring mode**: Flip Ring to Ring (Switch 8). Only the outline of the diamond is drawn. Pull the Fader down to narrow the ring — note that the mix also fades toward dry as you do this.
5. **Dual ring**: With both Shape=Hole and Ring=Ring, observe that both the outer and inner diamond boundaries are drawn as outlines.
6. **Tiling**: Increase H Tiles and V Tiles. The hole/ring pattern repeats in every tile.

**Key concepts**: Hole mode subtracts the inner diamond from the outer, Ring mode draws boundary outlines only, Fader controls both mix and ring thickness simultaneously

---

### Exercise 3: Full Atari Video Music Recreation

<img src={harlequin_exercise3_result} alt="Full Atari Video Music Recreation result"/>
*Full Atari Video Music Recreation — simulated result across source images.*
**Source**: Any active video footage — music videos, live camera feeds, or high-contrast abstract footage.

**Objective**: Combine maximum tiling, fast hue cycling, and auto cycle to recreate the Atari Video Music experience.

1. **Maximum tiling**: Set H Tiles to the highest step (5) and V Tiles to the highest step (8). The screen fills with a 5×8 grid of 40 small diamonds.
2. **Fast color cycling**: Turn Color Speed to ~80%. The diamonds cycle rapidly through the hue spectrum.
3. **Enable Auto Cycle**: Flip Auto Cycle (Switch 9) to On. The shape mode now changes autonomously every ~4 seconds, shuffling between solid, hole, and ring states.
4. **Video background**: Toggle Video BG to On. The source video fills the spaces between the diamonds.
5. **Gain balance**: Adjust Outer Gain and Inner Gain so the diamonds pulse visibly with the source brightness. The upper half of the video drives the outer diamonds; the lower half drives the inner.
6. **Smooth or percussive**: Sweep Contour from minimum to maximum. Low values make the diamonds jitter like an audio visualizer; high values make them breathe gently.

**Key concepts**: Tiling creates repeating diamond grids, DDS hue cycling reproduces the Atari Video Music color knob, LFSR auto cycle randomizes shape parameters, upper/lower screen halves drive independent diamond fields

---


## Tips

- **Dual-purpose fader**: The Mix fader simultaneously controls wet/dry balance and ring thickness. If you want wide rings at partial mix, there is no way to decouple these — plan compositions with this constraint in mind.
- **Upper/lower split**: The luminance analysis divides the frame at scanline 360 (mid-screen). If your source has uniform brightness across both halves, the outer and inner diamonds will be the same size. Use sources with contrast between top and bottom for the most dynamic response.
- **Contour is temporal smoothing**: The Contour knob does not sharpen diamond edges spatially — it controls how quickly the IIR filter tracks brightness changes over time. Low = percussive, high = slow breathing.
- **Auto Cycle is deterministic**: The LFSR sequence repeats exactly from the same seed every power cycle. If you need a specific shape mode at a specific time, Auto Cycle is predictable — but the cycle is long enough that it appears random in practice.
- **Tile counts are not powers of two**: The horizontal presets include 3 and 5, which evenly divide the 1280-pixel width. This is faithful to the original Atari Video Music, which offered non-power-of-two tile options.
- **Feedback loops**: Routing Harlequin's output back to its input creates a recursive feedback loop where the diamond shapes respond to their own brightness — producing self-reinforcing or oscillating diamond fields.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed source for before/after evaluation.
- **Pair with a mixer**: Because Harlequin generates bold geometric overlays, it works well as a layer in a multi-program composite — feed its output into another program's video background input.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric. Harlequin uses 0 BRAMs — all state fits in LUT-based registers. |
| **DDS** | Direct Digital Synthesis; a technique for generating a periodic waveform by incrementing a phase accumulator and using it to index a lookup table. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip that executes the video processing pipeline. |
| **IIR** | Infinite Impulse Response; a filter whose output depends on both the current input and the filter's own previous output, creating exponential smoothing. |
| **LFSR** | Linear-Feedback Shift Register; a pseudo-random number generator using a shift register with XOR-combined feedback taps. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **LUT** | Lookup Table; (1) in DSP context, a precomputed table of function values indexed by input; (2) in FPGA context, the basic logic element. |
| **Manhattan distance** | The sum of absolute horizontal and vertical displacements between two points; produces diamond-shaped equidistant contours. |
| **Pipeline** | A series of sequential processing stages where each stage completes in one clock cycle, passing results to the next stage. |
| **Quarter-wave sine** | A lookup table storing only 0°–90° of a sine wave; the remaining quadrants are reconstructed by mirroring and negation. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
