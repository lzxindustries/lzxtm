---
draft: false
sidebar_position: 20
slug: /instruments/videomancer/bitcullis
title: "Bitcullis"
image: /img/instruments/videomancer/bitcullis/bitcullis_hero_s1.png
description: "Digital video is made of discrete numbers — brightness and color values laid out on a grid of pixels."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import bitcullis_control_panel from '/img/instruments/videomancer/bitcullis/bitcullis_control_panel.png';
import bitcullis_source1_fruit from '/img/instruments/videomancer/bitcullis/bitcullis_source1_fruit.png';
import bitcullis_source2_field from '/img/instruments/videomancer/bitcullis/bitcullis_source2_field.png';
import bitcullis_source3_elephant from '/img/instruments/videomancer/bitcullis/bitcullis_source3_elephant.png';
import bitcullis_source4_pattern from '/img/instruments/videomancer/bitcullis/bitcullis_source4_pattern.png';
import bitcullis_source5_man from '/img/instruments/videomancer/bitcullis/bitcullis_source5_man.png';
import bitcullis_source6_berries from '/img/instruments/videomancer/bitcullis/bitcullis_source6_berries.png';
import bitcullis_hero_s1 from '/img/instruments/videomancer/bitcullis/bitcullis_hero_s1.png';
import bitcullis_hero_s2 from '/img/instruments/videomancer/bitcullis/bitcullis_hero_s2.png';
import bitcullis_hero_s3 from '/img/instruments/videomancer/bitcullis/bitcullis_hero_s3.png';
import bitcullis_hero_s4 from '/img/instruments/videomancer/bitcullis/bitcullis_hero_s4.png';
import bitcullis_hero_s5 from '/img/instruments/videomancer/bitcullis/bitcullis_hero_s5.png';
import bitcullis_hero_s6 from '/img/instruments/videomancer/bitcullis/bitcullis_hero_s6.png';
import bitcullis_ex1_s1 from '/img/instruments/videomancer/bitcullis/bitcullis_ex1_s1.png';
import bitcullis_ex1_s2 from '/img/instruments/videomancer/bitcullis/bitcullis_ex1_s2.png';
import bitcullis_ex1_s3 from '/img/instruments/videomancer/bitcullis/bitcullis_ex1_s3.png';
import bitcullis_ex1_s4 from '/img/instruments/videomancer/bitcullis/bitcullis_ex1_s4.png';
import bitcullis_ex1_s5 from '/img/instruments/videomancer/bitcullis/bitcullis_ex1_s5.png';
import bitcullis_ex1_s6 from '/img/instruments/videomancer/bitcullis/bitcullis_ex1_s6.png';
import bitcullis_ex2_s1 from '/img/instruments/videomancer/bitcullis/bitcullis_ex2_s1.png';
import bitcullis_ex2_s2 from '/img/instruments/videomancer/bitcullis/bitcullis_ex2_s2.png';
import bitcullis_ex2_s3 from '/img/instruments/videomancer/bitcullis/bitcullis_ex2_s3.png';
import bitcullis_ex2_s4 from '/img/instruments/videomancer/bitcullis/bitcullis_ex2_s4.png';
import bitcullis_ex2_s5 from '/img/instruments/videomancer/bitcullis/bitcullis_ex2_s5.png';
import bitcullis_ex2_s6 from '/img/instruments/videomancer/bitcullis/bitcullis_ex2_s6.png';
import bitcullis_ex3_s1 from '/img/instruments/videomancer/bitcullis/bitcullis_ex3_s1.png';
import bitcullis_ex3_s2 from '/img/instruments/videomancer/bitcullis/bitcullis_ex3_s2.png';
import bitcullis_ex3_s3 from '/img/instruments/videomancer/bitcullis/bitcullis_ex3_s3.png';
import bitcullis_ex3_s4 from '/img/instruments/videomancer/bitcullis/bitcullis_ex3_s4.png';
import bitcullis_ex3_s5 from '/img/instruments/videomancer/bitcullis/bitcullis_ex3_s5.png';
import bitcullis_ex3_s6 from '/img/instruments/videomancer/bitcullis/bitcullis_ex3_s6.png';

# Bitcullis

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: bitcullis_source1_fruit, after: bitcullis_hero_s1 },
    { label: "Field", before: bitcullis_source2_field, after: bitcullis_hero_s2 },
    { label: "Elephant", before: bitcullis_source3_elephant, after: bitcullis_hero_s3 },
    { label: "Pattern", before: bitcullis_source4_pattern, after: bitcullis_hero_s4 },
    { label: "Man", before: bitcullis_source5_man, after: bitcullis_hero_s5 },
    { label: "Berries", before: bitcullis_source6_berries, after: bitcullis_hero_s6 },
  ]}
/>
*Bitcullis applying luminance-modulated decimation and ordered dithering to create adaptive mosaic textures.*

---

## Overview

Digital video is made of discrete numbers — brightness and color values laid out on a grid of pixels. Most video processing tries to hide that fact, making the grid and the numbers as smooth and invisible as possible. Bitcullis does the opposite. It takes the digital structure of the signal and makes it the subject.

The program chains seven processing stages together — spatial decimation (horizontal and vertical pixelation), luminance-driven modulation of those effects, ordered and random dithering, posterization (bit-depth reduction), bit-order reversal, and luminance threshold keying. Every stage operates simultaneously on every pixel of every frame. The name is a portmanteau of *bit* (the fundamental digital unit) and *portcullis* (the iron gate of a castle) — a gate made of bits, controlling what passes through.

At conservative settings, Bitcullis can create subtle mosaic textures or gentle posterization. At extreme settings, it reduces video to hard-edged block graphics, glitch patterns, and abstract digital structures that bear little resemblance to the source.

---

## Quick Start

1. **Order matters**: Inversion → Modulation → Decimation → Dithering → Posterization → Bit Reversal → Threshold. Each stage transforms the signal before the next one sees it.
2. **Dithering needs posterization**: Dithering adds −16 to +14 counts at 10-bit resolution, which is imperceptible without posterization to amplify the effect.
3. **Luma modulation is the signature effect**: Luminance-to-horizontal modulation creates *adaptive* mosaics where the block pattern follows the image content. This is what makes Bitcullis unique.

---

## Background

### What Is Spatial Decimation?

Bitcullis's horizontal and vertical decimation controls implement **sample-and-hold** downsampling. The effect is identical to what happens when you reduce a high-resolution image to a very low resolution and then scale it back up without interpolation — pixels become visible as uniform blocks. Television engineers call this "decimation" because it discards samples. Bitcullis uses a frequency accumulator to control the decimation rate, which means the block size is continuously variable rather than limited to integer ratios.

The horizontal and vertical axes are controlled independently. You can create wide horizontal bars (high vertical decimation, low horizontal), tall vertical columns (high horizontal, low vertical), or uniform square blocks (both equal). Because the decimation frequency is controlled by an accumulator, the block boundaries can shift and alias in interesting ways as you sweep the controls.

### What Is Posterization?

When you reduce the number of brightness or color levels that a pixel can take, the smooth gradients in an image collapse into flat regions separated by hard edges. This effect is called **posterization** — named after the appearance of screen-printed posters, which use a small number of ink colors to represent a continuous image. Bitcullis applies posterization independently to the luminance and chrominance channels, so you can crush the brightness resolution while leaving color smooth, or vice versa.

### What Is Dithering?

Dithering is a technique for making a low-bit-depth image appear to have more tonal levels than it actually contains. It works by adding a small, structured noise pattern to the signal *before* quantization. The noise pushes pixel values across quantization boundaries in a pattern that, from a distance, creates the illusion of intermediate tones. Bitcullis offers two dithering algorithms: **ordered dithering** (a fixed 4×4 Bayer matrix) and **random dithering** (an LFSR pseudo-random pattern). Ordered dithering produces a regular stipple texture; random dithering produces a film-grain-like noise.

### What Is Bit-Order Reversal?

Every pixel value is stored as a 10-bit binary number. The **bit-order reversal** toggle flips the significance of those bits — the most significant bit becomes the least significant and vice versa. This is not a simple inversion (which flips 1s to 0s); it is a *permutation* of the binary representation. The result is a nonlinear, often chaotic remapping of brightness and color values that produces glitch-like visual artifacts.


---

## Signal Flow

Y Channel → U/V Channels → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Luma Invert            (optional bitwise complement)
│   ├─ 2. Luma→Hori Modulation   (luminance controls H-decimation frequency)
│   ├─ 3. Vertical Decimation    (sample-and-hold per scan line)
│   ├─ 4. Horizontal Decimation  (sample-and-hold per pixel, modulated by Y)
│   ├─ 5. Dithering              (ordered Bayer or random LFSR, optional)
│   ├─ 6. Luma Posterization     (quantizer — bit-depth reduction)
│   ├─ 7. Bit Order Reversal     (optional bit permutation)
│   └─ 8. Threshold Key          (luminance threshold → black below cutoff)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Luma→Chroma Modulation (luminance controls UV saturation)
│   ├─ 2. Vertical Decimation    (same frequency as Y)
│   ├─ 3. Horizontal Decimation  (same frequency as Y, modulated by Y)
│   ├─ 4. Dithering              (same pattern as Y)
│   ├─ 5. Chroma Posterization   (quantizer — independent of Y)
│   ├─ 6. Bit Order Reversal     (optional, same as Y)
│   └─ 7. Threshold Key          (keyed to neutral when Y below threshold)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

Two key interactions: (1) **Luminance-driven modulation**: The Y channel drives *two* modulation controls. Luma→Hori varies the horizontal decimation frequency pixel-by-pixel based on brightness. Luma→Chroma varies the chroma saturation based on brightness. (2) **Processing order**: Decimation happens *before* posterization, so the posterizer quantizes the already-pixelated signal. Dithering sits between decimation and posterization, adding noise to the blocky signal before it gets quantized.

---

## Parameter Reference

<img src={bitcullis_control_panel} alt="Videomancer front panel with Bitcullis loaded"/>
*Videomancer's front panel with Bitcullis active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Hori Decimate
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

At 0%, maximum pixelation — the image is reduced to wide bands of uniform color. At 200%, the decimation rate is so high that each pixel retains its original value (near full resolution). The Luma to Hori control (Knob 3) can further modulate this frequency on a per-pixel basis, making the block size dependent on the image content. Internally, controls the horizontal decimation frequency.

---

#### Knob 2 — Vert Decimate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the vertical decimation frequency. Lower values create taller horizontal bands; higher values create thinner bands. Combined with Hori Decimate, this defines the block geometry: equal values create roughly square blocks, unequal values create rectangles — wide horizontal bars or tall vertical columns.

---

#### Knob 3 — Luma to Hori
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls how strongly the input luminance modulates the horizontal decimation frequency. At 0%, decimation is uniform across the image. As you increase this control, bright areas of the source get different block sizes than dark areas. This is one of Bitcullis's most distinctive controls — the mosaic pattern follows the tonal structure of the source image, creating *adaptive* pixelation that reveals the underlying content.

---

#### Knob 4 — Luma Poster
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Luminance posterization depth. At 0%, the posterizer reduces the Y channel to just 2 levels (only the most significant bit is preserved), producing extreme banding. As you increase the control, more brightness levels are preserved and gradients become smoother. At 100%, the full 10-bit resolution (1024 levels) passes unchanged.

---

#### Knob 5 — Chroma Poster
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Chrominance posterization depth — independent of the Y channel quantizer. Setting this high while keeping Luma Poster low creates a painterly, silk-screen-like effect where brightness remains smooth but colors snap to a reduced palette. The reverse combination (high Luma Poster, low Chroma Poster) produces banded tonal steps with smooth color transitions.

---

#### Knob 6 — Luma to Chroma
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Luminance modulates chroma saturation. Bright areas of the input can be made more or less saturated than dark areas. This creates a content-dependent colorization effect — the color structure of the output follows the original brightness structure, even after heavy decimation and posterization.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Luma Invert** | Off | On |
| **8 — Bit Order** | Normal | Swapped |
| **9 — Dithering** | Disabled | Enabled |
| **10 — Dither Algo** | Ordered | Random |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent binary processing options. Unlike Lumarian's edge mode switches, these do not form a combined selector — each switch enables or disables a specific stage in the processing chain.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Luminance key at the end of the processing chain. At 0%, everything passes through (no keying). As you raise the fader, progressively brighter portions of the post-processed image are replaced with black, because more pixels fall below the rising threshold. At 100%, only the very brightest pixels survive. This interacts powerfully with posterization: because posterized signals have hard boundaries between tonal bands, the threshold cuts cleanly between levels. With bit-order reversal active, the threshold cuts through the chaotic value mapping in unexpected ways.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Bitcullis processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from simple decimation to full signal deconstruction. Each builds on the previous, gradually engaging more of the processing chain.

### Exercise 1: Mosaic Pixelation

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: bitcullis_source1_fruit, after: bitcullis_ex1_s1 },
    { label: "Field", before: bitcullis_source2_field, after: bitcullis_ex1_s2 },
    { label: "Elephant", before: bitcullis_source3_elephant, after: bitcullis_ex1_s3 },
    { label: "Pattern", before: bitcullis_source4_pattern, after: bitcullis_ex1_s4 },
    { label: "Man", before: bitcullis_source5_man, after: bitcullis_ex1_s5 },
    { label: "Berries", before: bitcullis_source6_berries, after: bitcullis_ex1_s6 },
  ]}
/>
*Mosaic Pixelation — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects.

**What You'll Create**: Learn how decimation and luminance modulation interact to create adaptive mosaic textures.

1. **Horizontal bands**: Turn Hori Decimate slowly counter-clockwise. Watch as the image breaks into wide vertical bands of uniform color.
2. **Vertical bands**: Now sweep Vert Decimate. The image breaks into horizontal bands.
3. **Square blocks**: Set both controls to about 30%. The image becomes a uniform mosaic of roughly square blocks.
4. **Adaptive mosaic**: Slowly increase Luma to Hori from 0 to 100%. Watch the block grid respond to the image content — bright and dark regions get different block sizes. This is Bitcullis's signature effect.
5. **Inversion**: Toggle Luma Invert (Switch 7). The modulation reverses — block sizes swap between bright and dark regions.

**Key concepts**: Decimation is sample-and-hold downsampling, horizontal and vertical axes are independent, luminance modulation creates content-adaptive mosaics

---

### Exercise 2: Posterized Graphics

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: bitcullis_source1_fruit, after: bitcullis_ex2_s1 },
    { label: "Field", before: bitcullis_source2_field, after: bitcullis_ex2_s2 },
    { label: "Elephant", before: bitcullis_source3_elephant, after: bitcullis_ex2_s3 },
    { label: "Pattern", before: bitcullis_source4_pattern, after: bitcullis_ex2_s4 },
    { label: "Man", before: bitcullis_source5_man, after: bitcullis_ex2_s5 },
    { label: "Berries", before: bitcullis_source6_berries, after: bitcullis_ex2_s6 },
  ]}
/>
*Posterized Graphics — simulated result across source images.*
**Source**: Footage with gradual tonal transitions — skies, skin tones, or gradient test patterns.

**What You'll Create**: Explore posterization and dithering interactions.

1. **Prepare**: Set moderate decimation (Hori and Vert ~50%) to create a visible mosaic.
2. **Luma posterization**: Slowly increase Luma Poster. Watch smooth gradients collapse into staircase bands.
3. **Chroma posterization**: Now increase Chroma Poster while leaving Luma Poster at a moderate value. Colors snap to a reduced palette while brightness remains smooth.
4. **Dithering**: Enable Dithering (Switch 9). The harsh posterization boundaries soften as noise pushes values across level boundaries. Compare ordered (Switch 10 Off) vs. random (Switch 10 On).
5. **Bit reversal**: Enable Bit Order (Switch 8). The orderly posterized levels explode into chaotic digital textures.
6. **Threshold**: Apply the Threshold fader to carve into the posterized result. Note how the threshold cuts cleanly along posterization boundaries.

**Key concepts**: Posterization is quantization of pixel values, dithering masks quantization artifacts by adding structured noise, bit reversal is a nonlinear permutation distinct from inversion

---

### Exercise 3: Digital Texture Synthesis

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: bitcullis_source1_fruit, after: bitcullis_ex3_s1 },
    { label: "Field", before: bitcullis_source2_field, after: bitcullis_ex3_s2 },
    { label: "Elephant", before: bitcullis_source3_elephant, after: bitcullis_ex3_s3 },
    { label: "Pattern", before: bitcullis_source4_pattern, after: bitcullis_ex3_s4 },
    { label: "Man", before: bitcullis_source5_man, after: bitcullis_ex3_s5 },
    { label: "Berries", before: bitcullis_source6_berries, after: bitcullis_ex3_s6 },
  ]}
/>
*Digital Texture Synthesis — simulated result across source images.*
**Source**: Any footage, especially high-contrast material.

**What You'll Create**: Combine all stages for abstract digital textures.

1. **Strong modulation**: Set Hori Decimate ~30%, Vert Decimate ~25%, Luma to Hori ~80%.
2. **Heavy processing**: Increase both Luma and Chroma Poster to high values.
3. **Random dithering**: Enable Dithering with random mode (Switch 10 On).
4. **Bit reversal**: Enable Bit Order (Switch 8) for chaotic value remapping.
5. **Threshold sculpt**: Lower the Threshold to ~40% to carve the texture.
6. **Inversion layers**: Toggle Luma Invert to see how it reverses the entire modulation chain.
7. **Animate**: Slowly sweep controls to watch the digital texture evolve in real time.

**Key concepts**: Bitcullis is a layered signal deconstruction tool, each stage reduces or rearranges information, the stages compound (decimation → dithering → posterization → bit-reversal → threshold)

---


## Tips

- **Bit reversal is not inversion**: Luma Invert flips all bits (linear complement). Bit Order Reversal *permutes* bit positions (nonlinear mapping). They produce completely different results.
- **Feedback loops**: Routing the output back to the input creates recursive decimation and posterization — self-referencing block structures that evolve over time.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed signal for before/after comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bit Depth** | The number of discrete levels available to represent a signal; higher bit depth means finer gradations. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Decimation** | Reducing spatial resolution by discarding samples at regular intervals, creating a blocky mosaic effect. |
| **Dithering** | Adding a small noise pattern before quantization to break up banding artifacts and simulate additional tonal levels. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Posterization** | Reducing the number of distinct tonal levels in an image, creating flat areas of uniform color or brightness. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **Quantization** | Mapping a continuous range of values to a smaller set of discrete levels, producing visible steps in gradients. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
