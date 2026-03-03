---
draft: true
sidebar_position: 197
slug: /instruments/videomancer/mosaic
title: "Mosaic"
image: /img/instruments/videomancer/mosaic/mosaic_hero_s1.png
description: "Every digital image is already a mosaic — a grid of discrete samples."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import mosaic_source1_boat from '/img/instruments/videomancer/mosaic/mosaic_source1_boat.png';
import mosaic_source2_parrot from '/img/instruments/videomancer/mosaic/mosaic_source2_parrot.png';
import mosaic_source3_clouds from '/img/instruments/videomancer/mosaic/mosaic_source3_clouds.png';
import mosaic_source4_pattern from '/img/instruments/videomancer/mosaic/mosaic_source4_pattern.png';
import mosaic_source5_man from '/img/instruments/videomancer/mosaic/mosaic_source5_man.png';
import mosaic_source6_knit from '/img/instruments/videomancer/mosaic/mosaic_source6_knit.png';
import mosaic_hero_s1 from '/img/instruments/videomancer/mosaic/mosaic_hero_s1.png';
import mosaic_hero_s2 from '/img/instruments/videomancer/mosaic/mosaic_hero_s2.png';
import mosaic_hero_s3 from '/img/instruments/videomancer/mosaic/mosaic_hero_s3.png';
import mosaic_hero_s4 from '/img/instruments/videomancer/mosaic/mosaic_hero_s4.png';
import mosaic_hero_s5 from '/img/instruments/videomancer/mosaic/mosaic_hero_s5.png';
import mosaic_hero_s6 from '/img/instruments/videomancer/mosaic/mosaic_hero_s6.png';
import mosaic_ex1_s1 from '/img/instruments/videomancer/mosaic/mosaic_ex1_s1.png';
import mosaic_ex1_s2 from '/img/instruments/videomancer/mosaic/mosaic_ex1_s2.png';
import mosaic_ex1_s3 from '/img/instruments/videomancer/mosaic/mosaic_ex1_s3.png';
import mosaic_ex1_s4 from '/img/instruments/videomancer/mosaic/mosaic_ex1_s4.png';
import mosaic_ex1_s5 from '/img/instruments/videomancer/mosaic/mosaic_ex1_s5.png';
import mosaic_ex1_s6 from '/img/instruments/videomancer/mosaic/mosaic_ex1_s6.png';
import mosaic_ex2_s1 from '/img/instruments/videomancer/mosaic/mosaic_ex2_s1.png';
import mosaic_ex2_s2 from '/img/instruments/videomancer/mosaic/mosaic_ex2_s2.png';
import mosaic_ex2_s3 from '/img/instruments/videomancer/mosaic/mosaic_ex2_s3.png';
import mosaic_ex2_s4 from '/img/instruments/videomancer/mosaic/mosaic_ex2_s4.png';
import mosaic_ex2_s5 from '/img/instruments/videomancer/mosaic/mosaic_ex2_s5.png';
import mosaic_ex2_s6 from '/img/instruments/videomancer/mosaic/mosaic_ex2_s6.png';
import mosaic_ex3_s1 from '/img/instruments/videomancer/mosaic/mosaic_ex3_s1.png';
import mosaic_ex3_s2 from '/img/instruments/videomancer/mosaic/mosaic_ex3_s2.png';
import mosaic_ex3_s3 from '/img/instruments/videomancer/mosaic/mosaic_ex3_s3.png';
import mosaic_ex3_s4 from '/img/instruments/videomancer/mosaic/mosaic_ex3_s4.png';
import mosaic_ex3_s5 from '/img/instruments/videomancer/mosaic/mosaic_ex3_s5.png';
import mosaic_ex3_s6 from '/img/instruments/videomancer/mosaic/mosaic_ex3_s6.png';

# Mosaic

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: mosaic_source1_boat, after: mosaic_hero_s1 },
    { label: "Parrot", before: mosaic_source2_parrot, after: mosaic_hero_s2 },
    { label: "Clouds", before: mosaic_source3_clouds, after: mosaic_hero_s3 },
    { label: "Pattern", before: mosaic_source4_pattern, after: mosaic_hero_s4 },
    { label: "Man", before: mosaic_source5_man, after: mosaic_hero_s5 },
    { label: "Knit", before: mosaic_source6_knit, after: mosaic_hero_s6 },
  ]}
/>
*Mosaic applying luma-modulated sample-and-hold pixelation with edge enhancement to create content-adaptive block structures.*

---

## Overview

Every digital image is already a mosaic — a grid of discrete samples. Mosaic takes that hidden structure and forces it into visibility by holding each sampled pixel value over a programmable number of horizontal clocks and scanlines. The result is the familiar pixelation effect: the image breaks into rectangular blocks of uniform color, each block representing a single sample stretched across a neighborhood of pixels.

What distinguishes Mosaic from simple downsampling is its luma-reactive block modulation. The horizontal hold period can be modulated by input luminance, so bright areas of the image get different block sizes than dark areas. The mosaic grid adapts to the content, creating organic, non-uniform pixelation where the block geometry reveals the tonal structure of the source. Additional processing stages — luma inversion, square locking, edge enhancement, and chroma kill — sculpt the final appearance.

Three potentiometer registers (4, 5, 6) are declared in the VHDL but not connected to any processing logic. They are reserved for future expansion and have no effect on the output.

---

## Background

### Sample-and-Hold Pixelation

The fundamental pixelation technique is **sample-and-hold**: at a programmable interval, the program latches the current input pixel value and continues outputting that value for a number of subsequent clocks. The counter resets at each horizontal sync pulse and at each block boundary. The result is that each block displays the color of whichever pixel happened to arrive at the sampling instant — a temporal snapshot stretched across space.

Horizontal and vertical hold operate independently. The horizontal counter increments once per pixel clock and resets after reaching the effective hold period. The vertical counter increments once per scanline and resets after reaching the vertical hold period. When the vertical counter is within a block, the output holds the values from the first scanline of that block. This two-axis hold creates rectangular blocks whose width and height are independently programmable.

### Luma-Modulated Block Size

The effective horizontal hold period is the sum of the H Block Size register and a luma-dependent offset. The offset is computed as $(Y_{in} \times \text{Luma Mod}) \gg 10$, where the input luma value and modulation depth are both 10-bit quantities. The shift-by-10 normalizes the product back to the register range. The result is that bright pixels extend the hold period (creating wider blocks) and dark pixels leave it near the base value (creating narrower blocks). This content-adaptive modulation is the program's signature capability.

### Square Mode and Period Locking

When Square Mode is engaged, the vertical hold period is forced to match the horizontal hold period, producing square blocks regardless of the V Block Size setting. Without square mode, the two axes are independent, allowing tall thin columns (large H, small V) or wide flat bars (small H, large V). Square mode simplifies the control surface when uniform block geometry is desired.

### Edge Enhancement

The edge enhance toggle adds a difference-based highlight at block boundaries. The program computes the absolute difference between the current block's luma and the previous block's luma, shifts it left by 2 (multiply by 4), and adds it to the output luma with saturation at 1023. The effect is a bright outline at every transition between blocks, making the grid structure more visible and giving the mosaic a faceted, stained-glass quality.

### Chroma Kill

When engaged, the chroma kill toggle forces U and V to the neutral midpoint (512), converting the mosaic output to monochrome. The luma channel is unaffected. This is useful for isolating the block geometry without the distraction of color, and for creating high-contrast grayscale pixelation.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Luma Invert (1 clk) ──────
│   └── Y optionally bitwise-inverted (NOT)
│
├── Luma Modulation Compute ─────────────────────────────
│   └── h_period = h_block_size + (y_in × luma_mod) >> 10
│
├── Stage 2: Horizontal Sample-and-Hold (1 clk) ────────
│   ├── Counter resets on hsync_fall
│   ├── Counter resets + sample when h_counter >= h_period >> 2
│   └── Holds Y, U, V between samples
│
├── Stage 3: Vertical Hold (1 clk) ─────────────────────
│   ├── Line counter resets on vsync_fall
│   ├── Line counter resets when v_counter >= v_period >> 2
│   ├── Square Mode: v_period = h_block_size
│   └── Holds first-line values across subsequent lines in block
│
├── Stage 4: Edge Enhance + Chroma Kill (1 clk) ────────
│   ├── Edge enhance: Y += |Y_curr − Y_prev| × 4, clamp 1023
│   └── Chroma kill: U = V = 512
│
├── Interpolator: Wet/Dry Mix (4 clks) ─────────────────
│   └── lerp(dry, wet, mix_amount) per Y, U, V
│
└── Bypass ─────────────────────────────────────────────
    └── Select original or processed signal
```

The luma inversion happens *before* the luma modulation computation, so it reverses which brightness regions get wider blocks. The horizontal and vertical hold stages are cascaded — horizontal hold determines the block width per pixel clock, then vertical hold repeats entire scanlines. The edge enhancement operates on the vertically-held output, highlighting transitions between blocks rather than transitions in the source image. The three unused potentiometer registers (Y Contrast, U Saturation, V Saturation at positions 4, 5, 6) are mapped to VHDL signals that are declared but never read by any processing logic — they have no effect on the output.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — H Block
| Property | Value |
|----------|-------|
| Range | 1 – 128 |
| Default | 1 |

Controls the base horizontal block width. This register sets the number of pixel clocks that each sampled value is held before a new sample is taken. The effective hold count is the upper 8 bits of the register value (register >> 2), giving a range of 0 to 255 pixel clocks. At 0, every pixel is sampled independently (no pixelation). At maximum, each sample is held for 255 clocks, reducing the effective horizontal resolution to a few blocks per line. The Luma Mod control can add to this base value on a per-pixel basis.

---

#### Knob 2 — V Block
| Property | Value |
|----------|-------|
| Range | 1 – 64 |
| Default | 1 |

Controls the vertical block height — the number of scanlines that each block row is held before new values are latched. Like the horizontal period, the effective count uses the upper 8 bits (register >> 2). At 0, every scanline is independent. At maximum, each block spans many scanlines. When Square Mode is enabled, this register is ignored and the vertical period matches the horizontal block size.

---

#### Knob 3 — Luma to H
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the luma modulation depth. The input luminance (after optional inversion) is multiplied by this value and the result is added to the base H Block Size. At 0, the block width is uniform across the image. As the value increases, bright areas get progressively wider blocks while dark areas retain the base width. At maximum, a fully bright pixel can nearly double the effective hold period. This creates content-adaptive pixelation where the mosaic grid follows the tonal structure of the source.

---

#### Knob 4 — Luma to V
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Reserved — Y Contrast. This register is mapped to the VHDL signal `s_y_contrast` but the signal is not connected to any processing logic. Adjusting this control has no effect on the output. It is retained for potential future use.

---

#### Knob 5 — Matte Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Reserved — U Saturation. This register is mapped to the VHDL signal `s_u_saturation` but is not connected to any processing logic. Adjusting this control has no effect on the output.

---

#### Knob 6 — Blend
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Reserved — V Saturation. This register is mapped to the VHDL signal `s_v_saturation` but is not connected to any processing logic. Adjusting this control has no effect on the output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — H Shape** | Linear | Exp |
| **8 — V Shape** | Linear | Exp |
| **9 — Chroma Hold** | Off | On |
| **10 — Luma Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary processing options. Luma Invert and Square Mode modify the sample-and-hold behavior. Edge Enhance and Chroma Kill are post-processing stages applied after the hold. Bypass routes the signal around all processing. Note that the TOML labels for toggles 7–10 do not match the VHDL implementation — the descriptions here reflect the actual hardware behavior.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original input and the mosaic output. At 0%, the output is the unmodified input. At 100%, the output is the full mosaic effect. Intermediate values blend the two, creating a semi-transparent pixelated overlay on the source.

---

## Guided Exercises

These exercises progress from basic pixelation through content-adaptive modulation to edge-enhanced monochrome textures. Each introduces additional processing stages.

### Exercise 1: Basic Pixelation

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: mosaic_source1_boat, after: mosaic_ex1_s1 },
    { label: "Parrot", before: mosaic_source2_parrot, after: mosaic_ex1_s2 },
    { label: "Clouds", before: mosaic_source3_clouds, after: mosaic_ex1_s3 },
    { label: "Pattern", before: mosaic_source4_pattern, after: mosaic_ex1_s4 },
    { label: "Man", before: mosaic_source5_man, after: mosaic_ex1_s5 },
    { label: "Knit", before: mosaic_source6_knit, after: mosaic_ex1_s6 },
  ]}
/>
*Basic Pixelation — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and varied color.

**Objective**: Learn how horizontal and vertical block size controls interact to create rectangular mosaic blocks.

1. **Horizontal blocks**: Set H Block Size to ~50%. The image breaks into wide vertical bands of held color. V Block Size remains at 0, so each scanline is independent.
2. **Vertical blocks**: Reset H Block Size to 0, set V Block Size to ~50%. Horizontal bands appear — each block row repeats the same scanline.
3. **Combined**: Set both H and V Block Size to ~30%. Rectangular blocks appear. Adjust the ratio to create squares, wide rectangles, or tall columns.
4. **Square lock**: Enable Square Mode. Now only H Block Size matters — the blocks are always square regardless of V Block Size.
5. **Size sweep**: With Square Mode on, slowly sweep H Block Size from minimum to maximum. Watch the mosaic resolution decrease from near-original to very coarse blocks.

**Key concepts**: Horizontal and vertical hold operate independently, square mode locks V to H, the upper 8 bits of the register set the effective hold count

---

### Exercise 2: Content-Adaptive Modulation

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: mosaic_source1_boat, after: mosaic_ex2_s1 },
    { label: "Parrot", before: mosaic_source2_parrot, after: mosaic_ex2_s2 },
    { label: "Clouds", before: mosaic_source3_clouds, after: mosaic_ex2_s3 },
    { label: "Pattern", before: mosaic_source4_pattern, after: mosaic_ex2_s4 },
    { label: "Man", before: mosaic_source5_man, after: mosaic_ex2_s5 },
    { label: "Knit", before: mosaic_source6_knit, after: mosaic_ex2_s6 },
  ]}
/>
*Content-Adaptive Modulation — simulated result across source images.*
**Source**: Footage with strong luminance contrast — a face against a dark background, or a brightly lit subject with shadows.

**Objective**: Explore how luma modulation creates non-uniform, content-aware pixelation.

1. **Base mosaic**: Set H Block Size to ~20%, V Block Size to ~20%, Square Mode off.
2. **Introduce modulation**: Slowly increase Luma Mod from 0. Bright areas of the image begin to develop wider blocks while dark areas retain finer resolution.
3. **Strong modulation**: At ~70% Luma Mod, the block size variation is dramatic — bright regions become very coarse while shadows remain detailed.
4. **Invert the response**: Toggle Luma Invert. Now dark areas get wider blocks and bright areas remain fine. The mosaic grid structure reverses its relationship to the source content.
5. **Balance with V Block Size**: Increase V Block Size independently to create vertically-stretched blocks in the dark regions while bright regions (modulated) stretch horizontally.

**Key concepts**: Luma modulation adds input brightness to the base hold period, inversion reverses the modulation direction, content-adaptive pixelation reveals tonal structure

---

### Exercise 3: Stained Glass Effect

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: mosaic_source1_boat, after: mosaic_ex3_s1 },
    { label: "Parrot", before: mosaic_source2_parrot, after: mosaic_ex3_s2 },
    { label: "Clouds", before: mosaic_source3_clouds, after: mosaic_ex3_s3 },
    { label: "Pattern", before: mosaic_source4_pattern, after: mosaic_ex3_s4 },
    { label: "Man", before: mosaic_source5_man, after: mosaic_ex3_s5 },
    { label: "Knit", before: mosaic_source6_knit, after: mosaic_ex3_s6 },
  ]}
/>
*Stained Glass Effect — simulated result across source images.*
**Source**: Footage with varied color and moderate contrast — nature scenes, architectural subjects, or abstract patterns.

**Objective**: Combine edge enhancement and chroma kill with modulated pixelation for a faceted, monochrome stained-glass texture.

1. **Moderate mosaic**: Set H Block Size to ~25%, V Block Size to ~25%.
2. **Enable edges**: Toggle Edge Enhance. Bright outlines appear at every block boundary, giving the mosaic a beveled, faceted quality.
3. **Chroma kill**: Toggle Chroma Kill. The output becomes monochrome — the block geometry and edge highlights are now the only visual structure.
4. **Add modulation**: Increase Luma Mod to ~50%. The block sizes vary with content, and the edge highlights trace the boundary between different-sized blocks.
5. **Mix overlay**: Set Mix to ~60%. The monochrome edge-enhanced mosaic blends with the original color video, creating a stained-glass overlay where color shows through the block grid.
6. **Invert for contrast**: Toggle Luma Invert and observe how the edge pattern changes as the modulation direction reverses.

**Key concepts**: Edge enhancement highlights block boundaries, chroma kill isolates geometry, partial Mix creates overlay compositing, edge pattern depends on modulation direction

---


## Tips

- **H and V are independent**: Mosaic's most expressive textures come from deliberately mismatched horizontal and vertical block sizes — try wide columns or flat bars before settling on squares.
- **Luma Mod is the signature control**: Content-adaptive pixelation distinguishes Mosaic from a simple downsampler. Even small amounts (10–20%) create visible tonal mapping in the grid geometry.
- **Invert before modulate**: Because Luma Invert precedes the modulation computation, it completely reverses which image regions get coarser blocks. Use it as a creative tool, not just a preprocessing step.
- **Edge Enhance for structure**: The 4× amplification of block-boundary differences creates strong visual outlines. Combine with Chroma Kill for a pure geometry display.
- **Square Mode for simplicity**: When exploring Luma Mod, enable Square Mode so both axes respond to a single control. Disable it later for asymmetric textures.
- **Partial Mix for overlay**: At 30–60% Mix, the mosaic acts as a semi-transparent texture layer over the original. Edge-enhanced monochrome mosaics make especially effective overlays.
- **Reserved controls are safe to touch**: The three unused potentiometers (positions 4, 5, 6) have no effect. They will not cause unexpected behavior.

---

## Glossary

| Term | Definition |
|------|------------|
| **Block** | A rectangular region of the output where all pixels share the same sampled color value, created by the sample-and-hold process. |
| **Chebyshev Distance** | An approximation of distance using $\max(|x|, |y|)$; not used in Mosaic but referenced in related programs. |
| **Chroma Kill** | Forcing the color components (U, V) to the neutral midpoint (512), producing monochrome output. |
| **Edge Enhancement** | Amplifying the luminance difference between adjacent blocks to create visible boundary highlights. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Hold Period** | The number of pixel clocks or scanlines that a sampled value is maintained before a new sample is taken. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Luma Modulation** | Varying a processing parameter (here, block size) based on the input luminance, creating content-adaptive effects. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Sample-and-Hold** | A circuit that captures an input value at a specific instant and maintains that value as its output until the next sampling event. |
| **Saturation Clamping** | Limiting a computed value to a maximum (here, 1023) to prevent overflow or wraparound artifacts. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
