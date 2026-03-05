---
draft: true
sidebar_position: 268
slug: /instruments/videomancer/shatter
title: "Shatter"
image: /img/instruments/videomancer/shatter/shatter_hero_s1.png
description: "Analog video synthesizers from the 1980s had a distinctive trick: split the screen into two complementary regions using a spatial pattern, apply a different processing effect to each region, then alternate them at a controllable rate."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import shatter_control_panel from '/img/instruments/videomancer/shatter/shatter_control_panel.png';
import shatter_source1_boat from '/img/instruments/videomancer/shatter/shatter_source1_boat.png';
import shatter_source2_dog from '/img/instruments/videomancer/shatter/shatter_source2_dog.png';
import shatter_source3_clouds from '/img/instruments/videomancer/shatter/shatter_source3_clouds.png';
import shatter_source4_pattern from '/img/instruments/videomancer/shatter/shatter_source4_pattern.png';
import shatter_source5_woman from '/img/instruments/videomancer/shatter/shatter_source5_woman.png';
import shatter_source6_berries from '/img/instruments/videomancer/shatter/shatter_source6_berries.png';
import shatter_hero_s1 from '/img/instruments/videomancer/shatter/shatter_hero_s1.png';
import shatter_hero_s2 from '/img/instruments/videomancer/shatter/shatter_hero_s2.png';
import shatter_hero_s3 from '/img/instruments/videomancer/shatter/shatter_hero_s3.png';
import shatter_hero_s4 from '/img/instruments/videomancer/shatter/shatter_hero_s4.png';
import shatter_hero_s5 from '/img/instruments/videomancer/shatter/shatter_hero_s5.png';
import shatter_hero_s6 from '/img/instruments/videomancer/shatter/shatter_hero_s6.png';
import shatter_ex1_s1 from '/img/instruments/videomancer/shatter/shatter_ex1_s1.png';
import shatter_ex1_s2 from '/img/instruments/videomancer/shatter/shatter_ex1_s2.png';
import shatter_ex1_s3 from '/img/instruments/videomancer/shatter/shatter_ex1_s3.png';
import shatter_ex1_s4 from '/img/instruments/videomancer/shatter/shatter_ex1_s4.png';
import shatter_ex1_s5 from '/img/instruments/videomancer/shatter/shatter_ex1_s5.png';
import shatter_ex1_s6 from '/img/instruments/videomancer/shatter/shatter_ex1_s6.png';
import shatter_ex2_s1 from '/img/instruments/videomancer/shatter/shatter_ex2_s1.png';
import shatter_ex2_s2 from '/img/instruments/videomancer/shatter/shatter_ex2_s2.png';
import shatter_ex2_s3 from '/img/instruments/videomancer/shatter/shatter_ex2_s3.png';
import shatter_ex2_s4 from '/img/instruments/videomancer/shatter/shatter_ex2_s4.png';
import shatter_ex2_s5 from '/img/instruments/videomancer/shatter/shatter_ex2_s5.png';
import shatter_ex2_s6 from '/img/instruments/videomancer/shatter/shatter_ex2_s6.png';
import shatter_ex3_s1 from '/img/instruments/videomancer/shatter/shatter_ex3_s1.png';
import shatter_ex3_s2 from '/img/instruments/videomancer/shatter/shatter_ex3_s2.png';
import shatter_ex3_s3 from '/img/instruments/videomancer/shatter/shatter_ex3_s3.png';
import shatter_ex3_s4 from '/img/instruments/videomancer/shatter/shatter_ex3_s4.png';
import shatter_ex3_s5 from '/img/instruments/videomancer/shatter/shatter_ex3_s5.png';
import shatter_ex3_s6 from '/img/instruments/videomancer/shatter/shatter_ex3_s6.png';

# Shatter

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: shatter_source1_boat, after: shatter_hero_s1 },
    { label: "Dog", before: shatter_source2_dog, after: shatter_hero_s2 },
    { label: "Clouds", before: shatter_source3_clouds, after: shatter_hero_s3 },
    { label: "Pattern", before: shatter_source4_pattern, after: shatter_hero_s4 },
    { label: "Woman", before: shatter_source5_woman, after: shatter_hero_s5 },
    { label: "Berries", before: shatter_source6_berries, after: shatter_hero_s6 },
  ]}
/>
*Shatter splitting a video signal into strobing binary pattern regions with solarized processing and checkerboard compositing.*

---

## Overview

Analog video synthesizers from the 1980s had a distinctive trick: split the screen into two complementary regions using a spatial pattern, apply a different processing effect to each region, then alternate them at a controllable rate. The result was a strobing, pulsating visual texture that transformed any input into a rhythmic graphic. Shatter recreates this technique digitally, with eight selectable spatial patterns, four processing modes, and a phase-locked DDS toggle oscillator.

The program divides every frame into two complementary zones — Region A and Region B — using a binary spatial mask. Region A receives a selectable processing effect (solarize, monochrome tint, negative, or posterize), while Region B shows the original input with optional inversion. A direct digital synthesis (DDS) accumulator toggles the mask between normal and inverted states, creating a strobe effect whose speed is continuously variable from sub-frame flicker to multi-second alternation. The name *Shatter* evokes the shattering of a unified image into tessellated fragments, each carrying different treatments of the same source.

At conservative settings — slow rate, coarse checkerboard, subtle processing — Shatter creates a gentle overlay texture. At extreme settings — fast rate, fine density, negative or solarize processing — it produces aggressive stroboscopic fragmentation that obliterates the original image structure.

---

## Quick Start

1. **Freeze the toggle to study patterns**: Set Rate to 0% to see the static spatial pattern without temporal alternation. This makes it much easier to understand what each pattern mode does.
2. **Use Posterize for graphic overlays**: The 4-level quantization creates hard-edged graphics that read clearly even at fine pattern densities. Combine with ChromaKill for bold black-and-white pattern effects.
3. **Solarize creates edge contours**: The V-shaped fold generates dark lines wherever the input crosses the midpoint brightness. These contours outline tonal transitions in the source material.

---

## Background

### The Fairlight CVI Legacy

The Fairlight CVI (Computer Video Instrument), released in 1984, was one of the earliest real-time digital video effects processors. Among its many capabilities was a "posterize and strobe" mode that alternated between processed and unprocessed regions of the frame. Shatter draws direct inspiration from this approach — the binary spatial mask, the controllable toggle rate, and the selectable processing effects all echo the CVI's architecture. The category name "Fairlight" acknowledges this lineage.

### Binary Spatial Patterns

Every pixel in Shatter's output is assigned to one of two regions based on a binary spatial mask. The mask is constructed from the pixel's position within a grid of cells. The cell coordinates are computed by shifting the pixel's horizontal and vertical counters right by a variable number of bits (the Density control), creating a coarser or finer grid. The eight available patterns — checkerboard, horizontal bars, vertical bars, diagonal, halves, sparse, wide checkerboard, and wide diagonal — are all single-bit functions of these cell coordinates, typically XOR or AND operations on the least significant bits.

### Direct Digital Synthesis Toggle

The toggle oscillator uses a DDS (direct digital synthesis) accumulator — a 16-bit counter that increments by a scaled version of the Rate parameter on every vertical sync pulse (once per frame at ~60 Hz). The most significant bit of the accumulator becomes the toggle state, which is XOR'd with the spatial pattern to form the composite mask. Because the accumulator wraps naturally, the toggle frequency is continuously variable and phase-coherent, just like a DDS frequency synthesizer in an RF transmitter.

### Solarization

Solarization — named after the Sabattier effect in darkroom photography — is a tonal curve that folds the brightness range at the midpoint. Values below mid-gray are remapped upward, values above mid-gray are remapped downward, creating a V-shaped transfer function. In Shatter, the VHDL implements this by doubling the input value and conditionally inverting: dark pixels become bright, bright pixels stay bright, and mid-tones collapse to black.

### Composite Region Architecture

The two-region architecture is fundamental to Shatter's visual identity. Region A always receives the selected processing effect. Region B shows either the unmodified input or its inverse (controlled by the Region B toggle). The composite mask selects between these two outputs on a pixel-by-pixel basis, creating hard-edged boundaries between processed and unprocessed zones. This creates a visual paradox: the viewer sees two different treatments of the same source material interleaved in a regular geometric pattern.


---

## Signal Flow

Input Capture → Pattern + Toggle → Processing → Composite Mux

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Capture ─────────────────────────────────────
│   ├─ Optional luma inversion (toggle 10)
│   ├─ Sync edge detection (hsync/vsync falling)
│   └─ Pixel/line counter update
│
├── Stage 2: Pattern + Toggle ──────────────────────────────────
│   ├─ Cell coords = pos >> density_shift (top 3 bits of pot 2)
│   ├─ 8 spatial patterns from cell coordinates
│   ├─ Toggle DDS: accumulate rate×64 per frame
│   ├─ Auto-phase sweep (slow accumulator)
│   └─ Composite mask = pattern_bit XOR toggle_state
│
├── Stage 3: Processing ────────────────────────────────────────
│   ├─ Mode "00" Solarize: Y×2 triangle fold
│   ├─ Mode "01" MonoTint: keep Y, UV = tint hue
│   ├─ Mode "10" Negative: 1023 − Y/U/V
│   ├─ Mode "11" Posterize: Y → 4 levels (0/341/682/1023)
│   └─ Chroma Kill: force U/V → 512 (toggle 8)
│
├── Stage 4: Composite Mux ────────────────────────────────────
│   ├─ Mask=1 → Region A (processed)
│   └─ Mask=0 → Region B (passthrough or inverted)
│
├── Stages 5–8: Interpolator ──────────────────────────────────
│   └─ Wet/dry crossfade (4 clocks)
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock sync/data pipeline delay
│
└── Output ─────────────────────────────────────────────────────
    └─ Bypass selects interpolator output or delayed dry signal
```

The key architectural feature is the separation of spatial pattern generation (Stage 2) from the processing chain (Stage 3). The pattern mask and the processing effect are computed in parallel pipelines that converge at the composite mux (Stage 4). This means the pattern boundaries are pixel-accurate — there is no interaction between the pattern geometry and the processing effect. The DDS toggle adds a temporal dimension to the spatial mask, but it operates at frame rate (once per vsync), so within a single frame the pattern is static. The auto-phase sweep adds a slow spatial drift to the pattern, creating subtle sliding motion even without manual Phase adjustment.

---

## Parameter Reference

<img src={shatter_control_panel} alt="Videomancer front panel with Shatter loaded"/>
*Videomancer's front panel with Shatter active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

At 0%, the toggle is frozen and the pattern remains static. As you increase the rate, the pattern begins to strobe at progressively higher frequencies. At higher values the toggling becomes fast enough to produce visual beating and flicker fusion. The DDS accumulator adds rate×64 per frame, so small rate values produce slow gentle alternation while moderate values create aggressive stroboscopic flicker. Internally, controls the toggle DDS frequency — how fast the spatial mask alternates between normal and inverted states.

---

#### Knob 2 — Density
| Property | Value |
|----------|-------|
| Range | 1px – 256px |
| Default | 65px |
| Suffix | px |

Sets the spatial density of the pattern cells. The top 3 bits of this register select a shift amount from 0 to 7, dividing pixel coordinates into cells of size 1 to 128 pixels. Low density values (high shift) create very large regions — screen-spanning blocks of processed vs. unprocessed video. High density values create fine-grained textures where individual cell boundaries become visible. The density control affects all eight pattern types simultaneously.

---

#### Knob 3 — Pattern
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Selects one of eight binary spatial patterns. The patterns are all computed from cell coordinates using simple bit operations: Checkerboard (XOR of cell X and Y LSBs), Horizontal Bars (cell Y LSB), Vertical Bars (cell X LSB), Diagonal (XOR of combined X+Y coordinate LSB), Halves (screen left/right split from pixel counter MSB), Sparse (AND of X and Y — only regions where both coordinates are odd), Wide Checkerboard (wider cell X bit XOR cell Y LSB), and Wide Diagonal (wider combined coordinate bit).

---

#### Knob 4 — Process
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Selects the processing effect applied to Region A. Solarize folds the luminance at the midpoint by doubling the value and conditionally inverting, creating a V-shaped transfer curve. MonoTint preserves Y but replaces U/V with the Tint Hue color, creating a duotone effect. Negative inverts all three channels (1023−Y, 1023−U, 1023−V). Posterize quantizes Y to exactly four levels (0, 341, 682, 1023) using the top 2 bits, creating a hard graphic poster effect. All four modes preserve sync and timing.

---

#### Knob 5 — Tint Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the color for MonoTint mode. The register value directly becomes U, while V is set to 1023 minus the register value, creating complementary color sweeps as you rotate the knob. At 0° the tint is deep blue, at 180° it passes through neutral, and at 360° it reaches deep orange-red. This control has no visible effect when a processing mode other than MonoTint is selected, unless Chroma Kill is off and the mode preserves chroma.

---

#### Knob 6 — Phase
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Adds a spatial phase offset to the pattern coordinates. Increasing the phase shifts the pattern horizontally by adding an offset to the pixel counter before cell coordinate computation. This creates a sliding motion in the pattern — checkerboard tiles shift sideways, bar patterns translate, and diagonal patterns drift at an angle. Combined with Auto Phase, this allows continuous hands-free pattern animation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Region B** | Normal | Invert |
| **8 — ChromaKill** | Off | On |
| **9 — AutoPhase** | Off | On |
| **10 — Luma Inv** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options that modify different stages of the pipeline. Region B (toggle 7) affects the composite mux output for unmasked regions. ChromaKill (toggle 8) strips color from the processed output. AutoPhase (toggle 9) enables a slow automatic phase sweep. Luma Inv (toggle 10) inverts the input luminance before all processing. Bypass (toggle 11) routes the delayed dry signal directly to the output. These switches can be freely combined — for example, Luma Inv + ChromaKill creates a monochrome inverted strobe pattern.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Shatter-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from static pattern exploration through processing mode comparison to dynamic strobing performance. Each builds familiarity with a different section of the pipeline.

### Exercise 1: Pattern Gallery

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: shatter_source1_boat, after: shatter_ex1_s1 },
    { label: "Dog", before: shatter_source2_dog, after: shatter_ex1_s2 },
    { label: "Clouds", before: shatter_source3_clouds, after: shatter_ex1_s3 },
    { label: "Pattern", before: shatter_source4_pattern, after: shatter_ex1_s4 },
    { label: "Woman", before: shatter_source5_woman, after: shatter_ex1_s5 },
    { label: "Berries", before: shatter_source6_berries, after: shatter_ex1_s6 },
  ]}
/>
*Pattern Gallery — simulated result across source images.*
**Source**: A camera feed with clear subject separation — a face against a contrasting background, or geometric objects on a flat surface.

**What You'll Create**: Explore the eight spatial patterns at various densities to understand how cell geometry maps to screen space.

1. Set Rate to 0% to freeze the toggle and see a static pattern.
2. Start with Checkerboard (Pattern = "Check") and sweep Density from minimum to maximum. Watch cell sizes change from screen-spanning blocks to fine pixel grids.
3. Step through all eight patterns one by one, observing how each divides the frame differently.
4. Set Density to a mid-range value (~50 px) and compare Diagonal vs. Wide Diagonal — note the doubled cell width in the wide variant.
5. Try Sparse (AND pattern) — notice that only one quarter of cells show the processed region, creating a dotted texture.
6. Set Phase to ~50% and observe horizontal pattern displacement.

**Key concepts**: Cell coordinates are computed by bit-shifting pixel position, all patterns derive from simple bit operations on cell coordinates, density controls the shift amount

---

### Exercise 2: Processing Mode Comparison

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: shatter_source1_boat, after: shatter_ex2_s1 },
    { label: "Dog", before: shatter_source2_dog, after: shatter_ex2_s2 },
    { label: "Clouds", before: shatter_source3_clouds, after: shatter_ex2_s3 },
    { label: "Pattern", before: shatter_source4_pattern, after: shatter_ex2_s4 },
    { label: "Woman", before: shatter_source5_woman, after: shatter_ex2_s5 },
    { label: "Berries", before: shatter_source6_berries, after: shatter_ex2_s6 },
  ]}
/>
*Processing Mode Comparison — simulated result across source images.*
**Source**: Footage with a wide tonal range — scenes with both bright and dark areas, gradients, and saturated color.

**What You'll Create**: Compare the four processing effects applied to Region A to build intuition for each mode's tonal transformation.

1. Set a medium Checkerboard pattern (Density ~64 px, Rate 0%) so both regions are clearly visible.
2. Start with Solarize: observe the V-shaped fold — dark areas brighten, bright areas stay bright, mid-tones collapse. Look for the characteristic dark contour at the fold point.
3. Switch to MonoTint: the processed region becomes a duotone of the tint color. Sweep Tint Hue through 360° and watch the color shift.
4. Switch to Negative: full inversion of all channels. Note how complementary colors appear.
5. Switch to Posterize: the smooth tonal range snaps to exactly four brightness levels. Edges become hard and graphic.
6. Enable ChromaKill and compare each mode in monochrome.
7. Toggle Region B → Invert: both regions now show different processing, creating maximum visual contrast.

**Key concepts**: Solarize folds luminance at midpoint, MonoTint replaces chroma with fixed color, Negative inverts all channels, Posterize quantizes to 4 levels

---

### Exercise 3: Stroboscopic Performance

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: shatter_source1_boat, after: shatter_ex3_s1 },
    { label: "Dog", before: shatter_source2_dog, after: shatter_ex3_s2 },
    { label: "Clouds", before: shatter_source3_clouds, after: shatter_ex3_s3 },
    { label: "Pattern", before: shatter_source4_pattern, after: shatter_ex3_s4 },
    { label: "Woman", before: shatter_source5_woman, after: shatter_ex3_s5 },
    { label: "Berries", before: shatter_source6_berries, after: shatter_ex3_s6 },
  ]}
/>
*Stroboscopic Performance — simulated result across source images.*
**Source**: Music video, rhythmic footage, or any source with visual motion to complement the temporal strobing.

**What You'll Create**: Use the toggle DDS and auto-phase to create dynamic, animated pattern effects suitable for live performance.

1. Set a Checkerboard pattern at moderate density (~32 px).
2. Slowly increase Rate from 0%. Watch the pattern begin to alternate between normal and inverted states. At low rates the alternation is a slow pulse; at higher rates it becomes a rapid strobe.
3. Find a rate that feels rhythmic with the source material.
4. Enable AutoPhase: the pattern begins to drift slowly across the screen, adding lateral motion to the temporal strobe.
5. Adjust Phase manually to shift the starting position of the auto-sweep.
6. Switch patterns during the strobe — try H-Bars for a rolling shutter effect, or Diagonal for a sweeping wipe.
7. Lower Mix to ~60% to soften the effect into a semi-transparent overlay.

**Key concepts**: DDS toggle adds rate×64 to a 16-bit accumulator per frame, auto-phase sweeps position, Mix blends composite with dry signal

---


## Tips

- **MonoTint is a duotone machine**: Keep the processed region in MonoTint mode and sweep Tint Hue slowly for a color-cycling overlay effect that follows the pattern geometry.
- **Stack feedback for recursion**: Route the output back to the input. The pattern compositing becomes recursive — each frame applies the pattern to the previous frame's pattern, creating nested fractal-like structures.
- **AutoPhase adds life**: Even a frozen toggle (Rate 0%) becomes dynamic when AutoPhase is enabled. The slow drift creates a hypnotic sliding motion through the pattern.
- **Region B Invert for maximum contrast**: Setting Region B to Invert while using Solarize or Posterize in Region A maximizes the visual difference between the two regions, creating the most aggressive edge boundaries.
- **Mix for subtlety**: At 50% Mix, the pattern structure is visible as a transparent overlay rather than a hard binary split. This can be more suitable for layered compositions.

---

## Glossary

| Term | Definition |
|------|------------|
| **Cell Coordinates** | The position of a pixel within the spatial grid, computed by bit-shifting the pixel counter right by the density shift amount. |
| **Composite Mask** | A single-bit signal that determines whether each pixel belongs to Region A (processed) or Region B (passthrough/inverted). |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic signals using a phase accumulator, used here for the toggle oscillator and auto-phase sweep. |
| **Fairlight CVI** | Computer Video Instrument by Fairlight (1984); an early digital video effects processor that inspired Shatter's binary pattern strobe architecture. |
| **LUT** | Look-Up Table; the fundamental logic element in an FPGA, used here for pattern generation and processing logic. |
| **Posterization** | Reducing continuous tonal values to a small number of discrete levels, creating flat graphic areas. |
| **Solarization** | A tonal curve that folds brightness at the midpoint, named after the Sabattier effect in analog photography. |
| **Toggle State** | The current binary state of the DDS oscillator, XOR'd with the spatial pattern to create the composite mask. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
