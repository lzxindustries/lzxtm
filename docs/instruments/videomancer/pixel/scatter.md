---
draft: true
sidebar_position: 260
slug: /instruments/videomancer/scatter
title: "Scatter"
image: /img/instruments/videomancer/scatter/scatter_hero_s1.png
description: "Every pixel in a digital video frame is a number."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import scatter_control_panel from '/img/instruments/videomancer/scatter/scatter_control_panel.png';
import scatter_source1_castle from '/img/instruments/videomancer/scatter/scatter_source1_castle.png';
import scatter_source2_house from '/img/instruments/videomancer/scatter/scatter_source2_house.png';
import scatter_source3_turtle from '/img/instruments/videomancer/scatter/scatter_source3_turtle.png';
import scatter_source4_pattern from '/img/instruments/videomancer/scatter/scatter_source4_pattern.png';
import scatter_source5_boy from '/img/instruments/videomancer/scatter/scatter_source5_boy.png';
import scatter_source6_paint from '/img/instruments/videomancer/scatter/scatter_source6_paint.png';
import scatter_hero_s1 from '/img/instruments/videomancer/scatter/scatter_hero_s1.png';
import scatter_hero_s2 from '/img/instruments/videomancer/scatter/scatter_hero_s2.png';
import scatter_hero_s3 from '/img/instruments/videomancer/scatter/scatter_hero_s3.png';
import scatter_hero_s4 from '/img/instruments/videomancer/scatter/scatter_hero_s4.png';
import scatter_hero_s5 from '/img/instruments/videomancer/scatter/scatter_hero_s5.png';
import scatter_hero_s6 from '/img/instruments/videomancer/scatter/scatter_hero_s6.png';
import scatter_ex1_s1 from '/img/instruments/videomancer/scatter/scatter_ex1_s1.png';
import scatter_ex1_s2 from '/img/instruments/videomancer/scatter/scatter_ex1_s2.png';
import scatter_ex1_s3 from '/img/instruments/videomancer/scatter/scatter_ex1_s3.png';
import scatter_ex1_s4 from '/img/instruments/videomancer/scatter/scatter_ex1_s4.png';
import scatter_ex1_s5 from '/img/instruments/videomancer/scatter/scatter_ex1_s5.png';
import scatter_ex1_s6 from '/img/instruments/videomancer/scatter/scatter_ex1_s6.png';
import scatter_ex2_s1 from '/img/instruments/videomancer/scatter/scatter_ex2_s1.png';
import scatter_ex2_s2 from '/img/instruments/videomancer/scatter/scatter_ex2_s2.png';
import scatter_ex2_s3 from '/img/instruments/videomancer/scatter/scatter_ex2_s3.png';
import scatter_ex2_s4 from '/img/instruments/videomancer/scatter/scatter_ex2_s4.png';
import scatter_ex2_s5 from '/img/instruments/videomancer/scatter/scatter_ex2_s5.png';
import scatter_ex2_s6 from '/img/instruments/videomancer/scatter/scatter_ex2_s6.png';
import scatter_ex3_s1 from '/img/instruments/videomancer/scatter/scatter_ex3_s1.png';
import scatter_ex3_s2 from '/img/instruments/videomancer/scatter/scatter_ex3_s2.png';
import scatter_ex3_s3 from '/img/instruments/videomancer/scatter/scatter_ex3_s3.png';
import scatter_ex3_s4 from '/img/instruments/videomancer/scatter/scatter_ex3_s4.png';
import scatter_ex3_s5 from '/img/instruments/videomancer/scatter/scatter_ex3_s5.png';
import scatter_ex3_s6 from '/img/instruments/videomancer/scatter/scatter_ex3_s6.png';

# Scatter

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: scatter_source1_castle, after: scatter_hero_s1 },
    { label: "House", before: scatter_source2_house, after: scatter_hero_s2 },
    { label: "Turtle", before: scatter_source3_turtle, after: scatter_hero_s3 },
    { label: "Pattern", before: scatter_source4_pattern, after: scatter_hero_s4 },
    { label: "Boy", before: scatter_source5_boy, after: scatter_hero_s5 },
    { label: "Paint", before: scatter_source6_paint, after: scatter_hero_s6 },
  ]}
/>
*Scatter applying XOR-based pixel corruption with structured hash patterns and edge-faded intensity to fracture a video signal into digital noise textures.*

---

## Overview

Every pixel in a digital video frame is a number. Scatter treats those numbers as raw binary material — something to be broken, flipped, and recombined. Rather than moving pixels around in space, it corrupts them *in place* by XOR-ing their values with pseudo-random or structured hash masks. The result is a family of digital noise textures that range from subtle static to total signal disintegration.

The name *Scatter* suggests spatial displacement, but the actual processing is bitwise: the program generates a corruption mask from either an LFSR (pseudo-random) or a deterministic hash of pixel coordinates, scales that mask by an intensity parameter, and XOR-s it against each pixel's Y, U, and V components. The Amount control determines how aggressively the corruption eats into the signal. Color Mod provides an independent corruption intensity for the chroma channels, letting you destroy color information while preserving luminance structure, or vice versa. Edge Fade attenuates the corruption near frame boundaries, creating a vignette of clarity surrounded by noise.

At low Amount settings, Scatter introduces a faint digital grain — a crunch of toggled bits that textures the image without obscuring it. At high settings, the XOR corruption overwhelms the original signal, producing abstract fields of digital snow that retain only a structural echo of the source. The transition between these extremes is non-linear and unpredictable, because XOR operations interact with the bit-patterns of the source in content-dependent ways.

---

## Background

### XOR as a Corruption Tool

The exclusive-or (XOR) operation is the simplest possible way to corrupt a digital signal. Given two binary numbers, XOR produces a 1 wherever the inputs differ and a 0 wherever they agree. When you XOR a pixel value with a random mask, you flip an unpredictable subset of its bits — some flips change the value slightly (low-order bits), others change it drastically (high-order bits). This makes XOR corruption fundamentally different from additive noise: instead of shifting values up or down, it *scrambles* them across the entire numeric range. A mid-gray pixel XOR-ed with a large mask might become nearly black, nearly white, or anything in between.

### Linear Feedback Shift Registers

Scatter's random mode uses a 16-bit **LFSR** (Linear Feedback Shift Register) to generate pseudo-random corruption masks. An LFSR is a shift register whose input bit is computed by XOR-ing selected bits of the current state. The resulting sequence is deterministic (repeating after $2^{16}-1$ clocks) but statistically uniform enough to appear random on screen. LFSRs are the standard random number generator in FPGA designs because they require only a few logic gates and produce one new output bit per clock cycle.

### Structured Hash Patterns

When the Pattern toggle selects structured mode, the corruption mask is computed as a deterministic hash of the pixel's horizontal and vertical coordinates, optionally mixed with a frame counter. This produces a fixed spatial pattern of corruption — a crystalline grid of glitched pixels that remains stable from frame to frame (unless Animate is enabled). The hash function is a series of XOR, shift, and add operations that distribute the coordinate values across the 10-bit output range.

### Edge Fade and Vignette

The Edge Fade parameter creates a spatial mask that reduces corruption intensity near the edges of the active video frame. The mask ramps linearly from zero at the frame boundary to full intensity at a configurable distance inward. This produces a vignette effect: the center of the frame is fully corrupted while the periphery remains clean — or, depending on how you think about it, the corruption blooms outward from the center, fading before it reaches the edges.

### Chroma-Only Corruption

The ChromaOnly toggle routes corruption exclusively to the U and V channels, leaving Y untouched. Because the human visual system is far more sensitive to luminance than chrominance, chroma-only corruption can produce dramatic color disruption while the underlying image structure remains recognizable. This is the principle behind chroma subsampling in broadcast video — and Scatter exploits the same perceptual asymmetry for creative effect.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 0: Input Register
│   └─ Latch Y, U, V; advance LFSR
│
├── Stage 1: Hash Computation
│   ├─ Random mode: use LFSR output as mask
│   └─ Struct mode: XOR(h_count, v_count, frame_count) → mask
│
├── Stage 2: Corruption Mask Scaling
│   └─ Extract bits from hash; scale by Amount → corruption_mask
│
├── Stage 3: Y Corruption
│   ├─ ChromaOnly off: Y' = Y XOR (corruption_mask & amount_scale)
│   └─ ChromaOnly on:  Y' = Y (pass-through)
│
├── Stage 4: Chroma Corruption
│   └─ U' = U XOR (mask & color_mod_scale)
│   └─ V' = V XOR (mask & color_mod_scale)
│
├── Stage 5: Edge Fade
│   └─ Attenuate corruption near frame edges
│   └─ Blend corrupted ↔ original based on edge distance
│
├── Stage 6: Invert Toggle
│   └─ If Invert: Y' = 1023 - Y'
│
├── Stage 7: Mix + Output Register
│   └─ Interpolate processed ↔ original by Mix amount
│
├── Sync Signals ─── Pass-through
│
└── Bypass ─── Select original or processed signal
```

The critical distinction is that Scatter performs *bitwise* corruption, not spatial displacement. The LFSR or hash function generates a mask that is XOR-ed against pixel values, flipping bits rather than moving pixels. The Amount and Color Mod controls independently scale the corruption applied to luminance and chrominance, allowing selective destruction of one domain while preserving the other. Edge Fade operates as a post-corruption blend, mixing corrupted and original pixels based on their distance from the frame boundary.

---

## Parameter Reference

<img src={scatter_control_panel} alt="Videomancer front panel with Scatter loaded"/>
*Videomancer's front panel with Scatter active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Radius
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the intensity of XOR corruption applied to the luminance channel (and to all channels when ChromaOnly is off). At 0%, the corruption mask is zeroed — no bits are flipped. As the value increases, more bits of the mask are allowed through, producing progressively more severe corruption. The relationship between the control position and the visual result is highly non-linear because XOR operations interact unpredictably with the source material's bit patterns.

---

#### Knob 2 — Density
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Originally labeled Radius for a planned spatial displacement mode, this register is stored but has minimal effect in the current XOR-based implementation. The value is latched and may influence the LFSR seeding or mask computation in subtle ways, but the primary corruption intensity is governed by Amount. Future firmware revisions may activate true spatial displacement using this parameter.

---

#### Knob 3 — Seed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Originally labeled Direction for planned directional displacement. Like Radius, this register is latched but has minimal effect on the current XOR pipeline. The value is present in the hash computation for structured mode, where it contributes to the spatial pattern, but it does not produce directional bias in the current implementation.

---

#### Knob 4 — Direction
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Originally labeled Grain, this parameter is registered but minimally used in the current implementation. Its value may subtly influence the LFSR feedback taps or hash distribution, but the dominant corruption control remains Amount. The parameter is included for future spatial-displacement modes where grain would control sub-pixel noise density.

---

#### Knob 5 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the XOR corruption intensity applied independently to the U and V chroma channels. When ChromaOnly is active, this is the *only* corruption control — Amount is bypassed for Y. When ChromaOnly is off, both Amount and Color Mod contribute to the final result, with Color Mod governing chroma corruption and Amount governing luma corruption. Setting Color Mod high with Amount at zero produces vivid rainbow noise over an intact luminance image.

---

#### Knob 6 — Grain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the edge fade distance — how far from the frame boundary the corruption attenuates. At 0%, the entire frame is uniformly corrupted. As you increase the control, a progressively wider border of clean signal appears at the frame edges while the center remains fully corrupted. This creates a vignette effect where noise blooms from the center outward but fades before reaching the periphery.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Luma Only** | Off | On |
| **8 — Chroma Only** | Off | On |
| **9 — Diagonal** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure independent binary processing options. Pattern selects the corruption source (LFSR vs. hash). ChromaOnly routes corruption to UV only. Animate makes the LFSR seed time-varying. Invert applies a luminance complement. Bypass disables all processing. These switches are fully independent — any combination is valid.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the original input signal and the fully processed output. At 0%, the output is identical to the input regardless of other control settings. At 100%, the full corruption chain is applied. Intermediate values produce a weighted blend — useful for dialing in subtle textures without overwhelming the source material. The mix is applied via the standard interpolator after all corruption and edge-fade processing.

---

## Guided Exercises

These exercises progress from subtle digital grain to full signal deconstruction, exploring the interaction between XOR corruption, chroma separation, and spatial masking.

### Exercise 1: Digital Grain Texture

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: scatter_source1_castle, after: scatter_ex1_s1 },
    { label: "House", before: scatter_source2_house, after: scatter_ex1_s2 },
    { label: "Turtle", before: scatter_source3_turtle, after: scatter_ex1_s3 },
    { label: "Pattern", before: scatter_source4_pattern, after: scatter_ex1_s4 },
    { label: "Boy", before: scatter_source5_boy, after: scatter_ex1_s5 },
    { label: "Paint", before: scatter_source6_paint, after: scatter_ex1_s6 },
  ]}
/>
*Digital Grain Texture — simulated result across source images.*
**Source**: A live camera feed or recorded footage with smooth tonal gradients — skin tones, skies, or soft lighting.

**Objective**: Learn how the Amount control introduces XOR-based noise as a digital grain texture.

1. **Subtle grain**: Set Amount to approximately 15%. A faint static appears over the image — individual pixel values are being flipped by one or two low-order bits.
2. **Increasing corruption**: Slowly increase Amount to 40%. The grain becomes coarser and more aggressive as higher-order bits are included in the XOR mask.
3. **Random vs. Structured**: Toggle Pattern (Switch 7) between Random and Struct. Random produces uniform noise; Structured produces a fixed spatial pattern of corruption.
4. **Animate**: Enable Animate (Switch 9) in Random mode. The grain begins to churn — each frame uses a different LFSR seed.
5. **Edge vignette**: Increase Edge Fade to 50%. The corruption fades near the frame edges, creating a vignette of grain.

**Key concepts**: XOR corruption flips bits rather than adding noise, Amount controls how many bits are exposed to flipping, Random mode produces temporal noise while Structured produces spatial patterns

---

### Exercise 2: Chroma Destruction

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: scatter_source1_castle, after: scatter_ex2_s1 },
    { label: "House", before: scatter_source2_house, after: scatter_ex2_s2 },
    { label: "Turtle", before: scatter_source3_turtle, after: scatter_ex2_s3 },
    { label: "Pattern", before: scatter_source4_pattern, after: scatter_ex2_s4 },
    { label: "Boy", before: scatter_source5_boy, after: scatter_ex2_s5 },
    { label: "Paint", before: scatter_source6_paint, after: scatter_ex2_s6 },
  ]}
/>
*Chroma Destruction — simulated result across source images.*
**Source**: Footage with strong, saturated colors — flowers, neon signs, colored fabrics.

**Objective**: Use ChromaOnly mode and Color Mod to destroy color information while preserving luminance.

1. **Enable ChromaOnly**: Set Switch 8 to Chroma. The Y channel is now protected from corruption.
2. **Color Mod sweep**: Slowly increase Color Mod from 0% to 80%. Watch colors fragment into rainbow noise while the underlying image structure remains recognizable.
3. **Structured chroma**: Enable Structured mode (Switch 7). The chroma corruption forms a fixed grid pattern — colors tile in a crystalline arrangement.
4. **Amount comparison**: Now disable ChromaOnly and increase Amount. Compare the effect of corrupting all channels versus chroma only.
5. **Inversion layer**: Enable Invert (Switch 10). The luminance inverts, but the chroma corruption remains — producing a negative image with scrambled colors.

**Key concepts**: Chroma-only corruption exploits the eye's lower sensitivity to color detail, independent luma and chroma corruption intensities, structured patterns create tiling color grids

---

### Exercise 3: Full Signal Disintegration

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: scatter_source1_castle, after: scatter_ex3_s1 },
    { label: "House", before: scatter_source2_house, after: scatter_ex3_s2 },
    { label: "Turtle", before: scatter_source3_turtle, after: scatter_ex3_s3 },
    { label: "Pattern", before: scatter_source4_pattern, after: scatter_ex3_s4 },
    { label: "Boy", before: scatter_source5_boy, after: scatter_ex3_s5 },
    { label: "Paint", before: scatter_source6_paint, after: scatter_ex3_s6 },
  ]}
/>
*Full Signal Disintegration — simulated result across source images.*
**Source**: Any footage — high-contrast material works well.

**Objective**: Combine all corruption tools for maximum signal destruction.

1. **Heavy corruption**: Set Amount to 80% and Color Mod to 70%.
2. **Structured hash**: Enable Structured mode (Switch 7) for deterministic spatial patterns.
3. **Animation**: Enable Animate (Switch 9) to make the pattern time-varying.
4. **Edge containment**: Set Edge Fade to 40% to create a border of clean signal around the chaos.
5. **Inversion**: Toggle Invert (Switch 10) on and off — watch how the complement interacts with XOR-corrupted values.
6. **Mix control**: Use Mix to blend the destruction back toward the original — find the threshold where structure is just barely recognizable.

**Key concepts**: XOR corruption is non-linear and content-dependent, Edge Fade provides spatial control over destruction, Mix allows partial application of extreme effects

---


## Tips

- **Amount is the primary control**: Radius, Direction, and Grain are registered but minimally active in the current XOR implementation. Focus on Amount and Color Mod for intensity.
- **ChromaOnly for subtle textures**: Corrupting only chroma produces dramatic color disruption while keeping the image recognizable — a useful halfway point between clean and destroyed.
- **Structured mode for repeatable patterns**: When you find a corruption pattern you like, Structured mode ensures it stays consistent frame to frame (with Animate off).
- **Edge Fade as a compositing tool**: Use Edge Fade to contain corruption in the center of frame, creating a natural focal point surrounded by clean signal.
- **Mix for partial application**: Extreme corruption settings become usable at low Mix values — dial in just a touch of digital grain without overwhelming the source.
- **Invert changes everything**: Because Invert is downstream of XOR corruption, it interacts with the corrupted values in non-obvious ways. Always try toggling it.
- **Feedback loops**: Routing Scatter's output back to its input creates recursive XOR corruption — the signal disintegrates progressively over time into pure digital noise.
- **XOR is its own inverse**: XOR-ing a value twice with the same mask returns the original. This means certain parameter combinations can partially cancel, producing unexpected clean patches.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric. Scatter uses no BRAMs. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Edge Fade** | Spatial attenuation of an effect based on distance from the frame boundary, producing a vignette pattern. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Hash** | A deterministic function that maps input coordinates to a pseudo-random output value for structured patterns. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input is a linear function of its previous state, producing a deterministic pseudo-random sequence. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **XOR** | Exclusive-or; a bitwise operation that outputs 1 when inputs differ and 0 when inputs agree. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
