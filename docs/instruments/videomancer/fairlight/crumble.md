---
draft: true
sidebar_position: 70
slug: /instruments/videomancer/crumble
title: "Crumble"
image: /img/instruments/videomancer/crumble/crumble_hero_s1.png
description: "Most video dissolve effects require a frame buffer — dedicated memory to store a previous frame so that current pixels can blend with past ones."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import crumble_control_panel from '/img/instruments/videomancer/crumble/crumble_control_panel.png';
import crumble_source1_fruit from '/img/instruments/videomancer/crumble/crumble_source1_fruit.png';
import crumble_source2_skull from '/img/instruments/videomancer/crumble/crumble_source2_skull.png';
import crumble_source3_elephant from '/img/instruments/videomancer/crumble/crumble_source3_elephant.png';
import crumble_source4_pattern from '/img/instruments/videomancer/crumble/crumble_source4_pattern.png';
import crumble_source5_girl from '/img/instruments/videomancer/crumble/crumble_source5_girl.png';
import crumble_source6_paint from '/img/instruments/videomancer/crumble/crumble_source6_paint.png';
import crumble_hero_s1 from '/img/instruments/videomancer/crumble/crumble_hero_s1.png';
import crumble_hero_s2 from '/img/instruments/videomancer/crumble/crumble_hero_s2.png';
import crumble_hero_s3 from '/img/instruments/videomancer/crumble/crumble_hero_s3.png';
import crumble_hero_s4 from '/img/instruments/videomancer/crumble/crumble_hero_s4.png';
import crumble_hero_s5 from '/img/instruments/videomancer/crumble/crumble_hero_s5.png';
import crumble_hero_s6 from '/img/instruments/videomancer/crumble/crumble_hero_s6.png';
import crumble_ex1_s1 from '/img/instruments/videomancer/crumble/crumble_ex1_s1.png';
import crumble_ex1_s2 from '/img/instruments/videomancer/crumble/crumble_ex1_s2.png';
import crumble_ex1_s3 from '/img/instruments/videomancer/crumble/crumble_ex1_s3.png';
import crumble_ex1_s4 from '/img/instruments/videomancer/crumble/crumble_ex1_s4.png';
import crumble_ex1_s5 from '/img/instruments/videomancer/crumble/crumble_ex1_s5.png';
import crumble_ex1_s6 from '/img/instruments/videomancer/crumble/crumble_ex1_s6.png';
import crumble_ex2_s1 from '/img/instruments/videomancer/crumble/crumble_ex2_s1.png';
import crumble_ex2_s2 from '/img/instruments/videomancer/crumble/crumble_ex2_s2.png';
import crumble_ex2_s3 from '/img/instruments/videomancer/crumble/crumble_ex2_s3.png';
import crumble_ex2_s4 from '/img/instruments/videomancer/crumble/crumble_ex2_s4.png';
import crumble_ex2_s5 from '/img/instruments/videomancer/crumble/crumble_ex2_s5.png';
import crumble_ex2_s6 from '/img/instruments/videomancer/crumble/crumble_ex2_s6.png';
import crumble_ex3_s1 from '/img/instruments/videomancer/crumble/crumble_ex3_s1.png';
import crumble_ex3_s2 from '/img/instruments/videomancer/crumble/crumble_ex3_s2.png';
import crumble_ex3_s3 from '/img/instruments/videomancer/crumble/crumble_ex3_s3.png';
import crumble_ex3_s4 from '/img/instruments/videomancer/crumble/crumble_ex3_s4.png';
import crumble_ex3_s5 from '/img/instruments/videomancer/crumble/crumble_ex3_s5.png';
import crumble_ex3_s6 from '/img/instruments/videomancer/crumble/crumble_ex3_s6.png';

# Crumble

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: crumble_source1_fruit, after: crumble_hero_s1 },
    { label: "Skull", before: crumble_source2_skull, after: crumble_hero_s2 },
    { label: "Elephant", before: crumble_source3_elephant, after: crumble_hero_s3 },
    { label: "Pattern", before: crumble_source4_pattern, after: crumble_hero_s4 },
    { label: "Girl", before: crumble_source5_girl, after: crumble_hero_s5 },
    { label: "Paint", before: crumble_source6_paint, after: crumble_hero_s6 },
  ]}
/>
*Crumble applying stochastic spatial dissolve with solarization and monochrome tint to create stable, framebuffer-free decay textures.*

---

## Overview

Most video dissolve effects require a frame buffer — dedicated memory to store a previous frame so that current pixels can blend with past ones. On a small FPGA with limited block RAM, frame buffers are expensive. Crumble sidesteps the problem entirely. Instead of remembering previous frames, it uses a deterministic spatial hash to decide which pixels receive processing and which pass through unchanged. Because the hash depends only on the pixel's screen position and a user-controlled seed, the same pixels are always affected for a given configuration — the pattern is stable from frame to frame without storing a single pixel of history.

The name *Crumble* evokes surfaces breaking apart — plaster falling from a wall, paint flaking to reveal a different layer underneath. The processed regions are the exposed underlayer; the unprocessed regions are the intact surface. Four processing modes give the exposed layer its character: solarization folds the brightness curve back on itself, monochrome tint replaces color with a user-chosen hue, negative inverts everything, and pointillist posterizes brightness into hard bands with a tint overlay. The result ranges from subtle texture — a handful of scattered pixels catching a different color — to total disintegration where nearly every pixel is transformed.

Crumble draws inspiration from the dissolve and posterization effects found in the Fairlight CVI, a pioneering digital video effects processor from the 1980s. The Fairlight CVI could dissolve between two video signals by pseudo-randomly selecting pixels from each source. Crumble adapts that concept to a single-source context: one "source" is the original signal and the other is a processed version of the same signal, with the spatial hash acting as the selection mask.

---

## Background

### The Fairlight CVI and Stochastic Dissolves

The Fairlight Computer Video Instrument, released in 1984, was one of the first real-time digital video effects processors available to artists and broadcasters. Among its distinctive capabilities was a **stochastic dissolve** — a transition where individual pixels were randomly assigned to one of two video sources, creating a speckled, granular crossfade rather than the smooth optical dissolve familiar from film. The effect resembled static or snow gradually consuming one image to reveal another.

The CVI achieved this with dedicated frame-store hardware that could buffer entire video fields. Crumble reproduces the visual character of a stochastic dissolve without any frame buffer at all, by replacing true randomness with a deterministic position-seeded hash. The spatial pattern looks random to the eye but repeats identically each frame, eliminating flicker and temporal instability.

### Deterministic Hashing vs. True Randomness

A true random number generator produces different values each time it is queried. For a spatial dissolve effect, this would mean different pixels are selected every frame — the mask would flicker wildly, producing noisy, unstable output. Crumble uses a **deterministic hash** instead: a function that always produces the same output for the same input. The inputs are the pixel's block-quantized (x, y) coordinates and a user-controlled seed value. The hash function is built from XOR operations and multiple rounds of a Galois LFSR (Linear Feedback Shift Register) scramble. The result looks spatially random — neighboring pixels get wildly different hash values — but is perfectly repeatable.

### Spatial Dissolve and Pointillism

The stochastic dissolve has a visual kinship with **pointillism**, the painting technique developed by Georges Seurat and Paul Signac in the 1880s. Pointillist paintings are composed of individual dots of pure color that blend optically when viewed from a distance. Crumble's pixel-level dissolve creates a similar effect: at low density, scattered processed pixels sit among unprocessed ones, and from a distance the eye blends them together. The pointillist processing mode makes this connection explicit by posterizing brightness into discrete bands and applying a tint color, creating dots of flat color reminiscent of a Seurat canvas.

### Block Quantization and Mosaic Scale

Rather than operating on individual pixels, Crumble can quantize the spatial coordinates to blocks of 1×1, 2×2, 4×4, or 8×8 pixels before hashing. This means the dissolve mask operates on patches rather than single pixels. At larger block sizes, the crumbled regions become visible mosaic tiles — square patches of processed signal set into the unprocessed background. This transforms the effect from fine-grained pixel dissolution into a coarser mosaic fragmentation, extending the visual vocabulary from digital static to broken tilework.

### LFSR Scrambling

A Linear Feedback Shift Register is a shift register whose input bit is a function of its previous state — specifically, an XOR of selected bit positions called "taps." Galois LFSRs place the feedback taps along the register rather than at the input, making them efficient to implement in hardware. Crumble uses three rounds of Galois LFSR scrambling (with taps at bits 16, 14, 13, and 11) to thoroughly mix the position-and-seed input into a pseudo-random hash value. Three rounds is a balance: enough mixing to eliminate obvious spatial patterns, but few enough to complete within a single clock cycle.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Capture + Counters ──────────────────────────
│   ├─ Luma Invert (optional bitwise complement of Y)
│   ├─ Sync edge detection (hsync/vsync falling edges)
│   ├─ Pixel (h_count) and line (v_count) counters
│   ├─ Block coordinate quantization (1px / 2×2 / 4×4 / 8×8)
│   └─ Auto-sweep DDS (triangle wave density modulation)
│
├── Stage 2: Hash + Mask ──────────────────────────────────────
│   ├─ Concatenate block_h & block_v
│   ├─ XOR with seed register and constant (0xB5A7)
│   ├─ 3× Galois LFSR scramble (taps: 16, 14, 13, 11)
│   ├─ Compare hash[9:0] < effective_density → crumble_mask
│   └─ XOR mask with Invert toggle → final_mask
│
├── Stage 3: Processing Chain ─────────────────────────────────
│   ├─ Mode select (2-bit from Process pot):
│   │   ├─ 00: Solarize   — triangle fold Y at midpoint
│   │   ├─ 01: Mono Tint  — preserve Y, replace UV with tint
│   │   ├─ 10: Negative   — invert Y, U, V (1023 − value)
│   │   └─ 11: Pointillist — posterize Y to 4 levels + tint UV
│   ├─ Chroma Kill (optional: force U/V to 512)
│   └─ Depth gate (depth < 256: process only dark pixels)
│
├── Stage 4: Composite Mux ────────────────────────────────────
│   └─ final_mask ? processed : passthrough
│
├── Stages 5–8: Interpolator (4 clk) ─────────────────────────
│   └─ Wet/dry crossfade (delayed input ↔ composite, Mix fader)
│
├── Sync Delay Pipeline (8 clk) ───────────────────────────────
│   └─ hsync_n, vsync_n, field_n, Y, U, V delayed to match
│
└── Output Assignment ─────────────────────────────────────────
    └─ Bypass ? delayed_input : mixed_output
```

The critical insight is that the hash function replaces what would normally require memory. In a traditional stochastic dissolve, a random mask is generated once and stored in a frame buffer so it can be applied identically to each successive frame. Crumble computes the mask fresh every frame from the pixel coordinates, but because the computation is deterministic, the result is the same — stable spatial selection without storage.

The depth control introduces a content-dependent gate before the composite mux. At low depth values (below 256 in the 10-bit register), only pixels whose luminance falls below the depth threshold receive processing — dark areas crumble while bright areas remain intact. Above 256, the depth gate allows all pixels through to the processing chain regardless of brightness. This creates an intensity-sensitive dissolve where the effect eats into shadows first.

---

## Parameter Reference

<img src={crumble_control_panel} alt="Videomancer front panel with Crumble loaded"/>
*Videomancer's front panel with Crumble active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the threshold that determines what proportion of the image is affected by processing. The 10-bit hash output for each pixel (or block) is compared against this value — pixels whose hash falls below the density threshold receive the selected processing mode, while those above it pass through unchanged. At 0%, no pixels are processed and the output matches the input. At 100%, every pixel is processed. The transition between these extremes is the core of the dissolve effect: scattered individual pixels gradually coalesce into larger processed regions as density increases.

---

#### Knob 2 — Process
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

Selects one of four processing modes applied to crumbled pixels. Solarize folds the luminance curve at the midpoint, creating a characteristic brightness reversal where mid-tones become bright and highlights wrap back toward dark. Mono Tint preserves the original luminance but replaces the chrominance with a user-selected hue from the Tint Hue knob. Negative inverts all three channels — luma and both chroma components — producing a photographic negative of the original. Pointillist posterizes brightness into four flat bands (black, one-third, two-thirds, full white) and applies the tint color, creating a hard-edged, screen-print-like texture in the crumbled regions.

---

#### Knob 3 — Tint Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the chrominance color used by the Mono Tint and Pointillist processing modes. The knob directly controls the U component of the tint, while V is derived as the complement (1023 minus the U value). Sweeping the knob from 0° to 360° rotates through a range of hues. At 0° the tint is a deep blue-magenta; near 180° it shifts toward yellow-green. This knob has no effect in Solarize or Negative modes, which preserve or invert the original chrominance rather than replacing it.

---

#### Knob 4 — Block Sz
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

Selects the spatial scale of the dissolve mask. At 1 Pixel, each individual pixel gets its own hash value — the dissolve pattern is fine-grained, resembling static or grain. At 2×2, adjacent groups of four pixels share a hash, creating small square patches. At 4×4 and 8×8, the patches grow larger, transforming the effect from pixel-level dissolution into a visible mosaic of processed and unprocessed tiles. Larger blocks make the spatial pattern more obvious and give the effect a coarser, more architectural character.

---

#### Knob 5 — Seed
| Property | Value |
|----------|-------|
| Range | 0 – 255 |
| Default | 0 |

Sets the seed value XORed into the hash function before scrambling. Different seeds produce different spatial distributions of the crumble mask — the same density with different seeds will affect different pixels. Because the hash is fully deterministic, each seed value defines a unique but stable spatial pattern. Sweeping the seed while watching the output reveals how the dissolve pattern shuffles across the image without changing its overall density.

---

#### Knob 6 — Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls processing intensity through a luminance-dependent gate. At low depth values (below roughly the first quarter of the range), only pixels whose brightness falls below the depth threshold receive processing — dark regions crumble while bright regions remain intact. This creates a shadow-first dissolution effect. Above the first quarter, the depth gate opens fully and all masked pixels receive processing regardless of their brightness. At 100%, the depth gate has no effect and the processing applies uniformly to all crumbled regions.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — AutoSwep** | Off | On |
| **8 — Invert** | Off | On |
| **9 — Luma Inv** | Off | On |
| **10 — ChromaKill** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary modifiers that interact with the main processing chain. Auto Sweep adds temporal animation to the density parameter. Invert flips which pixels are crumbled versus preserved. Luma Invert transforms the brightness before all other processing. Chroma Kill strips color from the processed result. Bypass routes the input directly to the output, skipping all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the delayed original input and the composite crumbled output. At 0%, the output is entirely the unprocessed (delayed) input — no crumble effect is visible. At 100%, the output is entirely the composite signal with the full dissolve mask applied. Intermediate positions blend the crumbled result with the original proportionally, creating a softer version of the effect where processed pixels are partially transparent against the underlying original.

---

## Guided Exercises

These exercises progress from understanding the basic dissolve mask to combining processing modes, block sizing, and temporal animation for expressive results.

### Exercise 1: Basic Spatial Dissolve

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: crumble_source1_fruit, after: crumble_ex1_s1 },
    { label: "Skull", before: crumble_source2_skull, after: crumble_ex1_s2 },
    { label: "Elephant", before: crumble_source3_elephant, after: crumble_ex1_s3 },
    { label: "Pattern", before: crumble_source4_pattern, after: crumble_ex1_s4 },
    { label: "Girl", before: crumble_source5_girl, after: crumble_ex1_s5 },
    { label: "Paint", before: crumble_source6_paint, after: crumble_ex1_s6 },
  ]}
/>
*Basic Spatial Dissolve — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a mix of bright and dark regions.

**Objective**: Learn how the density control and hash seed create a stable stochastic dissolve mask.

1. **Sparse dissolve**: Set Density to about 25%. Observe scattered processed pixels appearing across the image.
2. **Increase density**: Slowly sweep Density from 25% toward 75%. Watch as the dissolved regions grow and merge.
3. **Change seed**: With Density at 50%, sweep the Seed knob. The pattern reshuffles — different pixels are selected — but the overall amount of processing stays the same.
4. **Invert mask**: Toggle Invert on. The processed and unprocessed regions swap. At 50% density the change is subtle; at 25% density it is dramatic.
5. **Block scale**: Switch Block Sz from 1 Pixel to 4×4/8×8. The fine-grained pixel dissolution becomes a coarser mosaic.

**Key concepts**: Deterministic hash produces stable spatial mask, density sets the proportion threshold, seed shuffles the pattern without changing density, block size scales the dissolve grain

---

### Exercise 2: Processing Mode Comparison

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: crumble_source1_fruit, after: crumble_ex2_s1 },
    { label: "Skull", before: crumble_source2_skull, after: crumble_ex2_s2 },
    { label: "Elephant", before: crumble_source3_elephant, after: crumble_ex2_s3 },
    { label: "Pattern", before: crumble_source4_pattern, after: crumble_ex2_s4 },
    { label: "Girl", before: crumble_source5_girl, after: crumble_ex2_s5 },
    { label: "Paint", before: crumble_source6_paint, after: crumble_ex2_s6 },
  ]}
/>
*Processing Mode Comparison — simulated result across source images.*
**Source**: Footage with moderate color saturation — skin tones, foliage, or painted surfaces.

**Objective**: Compare the four processing modes and learn how Tint Hue changes the color in tint-based modes.

1. **Solarize**: Set Process to Solarize, Density to 60%. Observe the characteristic brightness fold in the crumbled regions.
2. **Mono Tint**: Switch Process to MonoTint. The crumbled pixels retain their brightness but take on the hue set by Tint Hue. Sweep Tint Hue across 0–360° to explore the color range.
3. **Negative**: Switch Process to Negative. Crumbled regions become a photographic negative of the original.
4. **Pointillist**: Switch Process to Pointlst. The crumbled pixels snap to four brightness levels with tint color — a screen-printed, Seurat-like texture.
5. **Block + Pointillist**: Set Block Sz to 4×4 with Pointillist mode. The posterized patches become visible tiles of flat, tinted color.

**Key concepts**: Each processing mode transforms crumbled pixels differently, Tint Hue applies to MonoTint and Pointillist only, Pointillist posterizes to 4 levels, block sizing amplifies the mosaic quality of processed regions

---

### Exercise 3: Animated Dissolve with Auto-Sweep

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: crumble_source1_fruit, after: crumble_ex3_s1 },
    { label: "Skull", before: crumble_source2_skull, after: crumble_ex3_s2 },
    { label: "Elephant", before: crumble_source3_elephant, after: crumble_ex3_s3 },
    { label: "Pattern", before: crumble_source4_pattern, after: crumble_ex3_s4 },
    { label: "Girl", before: crumble_source5_girl, after: crumble_ex3_s5 },
    { label: "Paint", before: crumble_source6_paint, after: crumble_ex3_s6 },
  ]}
/>
*Animated Dissolve with Auto-Sweep — simulated result across source images.*
**Source**: Any video footage — motion enhances the breathing animation.

**Objective**: Combine auto-sweep, depth gating, and chroma kill for an animated, shadow-sensitive dissolve.

1. **Auto-sweep**: Enable AutoSwep with Density at about 40%. Watch the dissolve breathe — crumbled regions expand and contract rhythmically.
2. **Depth gate**: Lower Depth to about 25%. Now only dark regions of the image are processed; bright areas remain untouched. The dissolve eats into the shadows first.
3. **Chroma kill**: Enable ChromaKill. The crumbled regions lose all color, becoming monochrome fragments against the full-color original.
4. **Luma inversion**: Toggle Luma Inv. The tonal map flips — what was shadow becomes highlight — and the depth gate now targets the originally bright regions instead.
5. **Mix blend**: Lower Mix to about 60%. The crumbled pixels become partially transparent, blending with the original for a softer, layered effect.

**Key concepts**: Auto-sweep adds rhythmic temporal animation to a spatially stable mask, depth gate creates brightness-dependent dissolve, chroma kill strips color from processed regions, luma inversion recharacterizes which regions the depth gate targets

---


## Tips

- **Seed as composition tool**: Different seeds produce radically different spatial patterns at the same density. Audition several seeds to find a pattern that complements your source material.
- **Block size for texture vs. structure**: 1 Pixel creates a fine digital grain. 8×8 creates bold mosaic tiles. Choose based on whether you want subtle texture or architectural fragmentation.
- **Depth for selective dissolve**: Low depth values make the effect shadow-sensitive — only dark areas crumble. This is powerful for creating the illusion of decay starting in the recesses of an image.
- **Mix for layering**: Intermediate Mix values make the crumbled regions semi-transparent, creating a ghostly double-exposure effect where processed and original pixels blend together.
- **Auto-sweep + low density**: With density centered low and auto-sweep active, the dissolve breathes gently in and out — a handful of scattered pixels pulse with each sweep cycle.
- **Pointillist + large blocks**: Combining the Pointillist mode with 4×4 or 8×8 blocks creates a mosaic of flat colored tiles, strongly evoking Neo-Impressionist painting.
- **Feedback loops**: Routing Crumble's output back to its input creates recursive spatial dissolution — the hash pattern compounds on itself, producing evolving fractal-like fragmentation.
- **Luma Inv + Depth interaction**: Luma Invert flips the brightness map before the depth gate evaluates it, effectively swapping which tonal regions the depth control targets.

---

## Glossary

| Term | Definition |
|------|------------|
| **Block Quantization** | Grouping adjacent pixels into square blocks that share a single hash value, scaling the dissolve pattern from per-pixel to per-tile. |
| **BT.601** | The ITU-R standard for standard-definition video color encoding, defining the YUV matrix coefficients used in the Videomancer pipeline. |
| **Chroma** | The color information in a video signal, encoded as U and V offset components in YUV space. |
| **DDS** | Direct Digital Synthesis; a technique for generating a periodic waveform by incrementing a phase accumulator on each clock cycle. |
| **Deterministic Hash** | A function that always produces the same output for the same input, enabling stable spatial patterns without frame-buffer storage. |
| **Dissolve** | A transition effect where pixels from two sources are mixed together; in Crumble, the two "sources" are the processed and unprocessed versions of the same signal. |
| **Fairlight CVI** | The Fairlight Computer Video Instrument (1984), a pioneering digital video effects processor known for stochastic dissolves and posterization. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Galois LFSR** | A linear feedback shift register with feedback taps distributed along the register, providing efficient pseudo-random scrambling. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is an XOR of selected positions, producing a pseudo-random sequence. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Pointillism** | A painting technique using individual dots of color that blend optically at a distance, referenced by the Pointillist processing mode. |
| **Posterization** | Reducing continuous tonal values to a small number of discrete levels, creating flat bands of uniform brightness or color. |
| **Solarization** | A photographic effect where tones are partially reversed, originally caused by extreme overexposure; simulated by folding the brightness curve at the midpoint. |
| **Stochastic** | Involving randomness or probability; in Crumble, the pseudo-random spatial mask is stochastic in appearance but deterministic in computation. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
