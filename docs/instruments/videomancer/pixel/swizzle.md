---
draft: true
sidebar_position: 278
slug: /instruments/videomancer/swizzle
title: "Swizzle"
image: /img/instruments/videomancer/swizzle/swizzle_hero.png
description: "Every pixel in the Videomancer video pipeline is a triplet of numbers — luminance (Y), and two chrominance components (U and V)."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import swizzle_hero from '/img/instruments/videomancer/swizzle/swizzle_hero.png';
import swizzle_control_panel from '/img/instruments/videomancer/swizzle/swizzle_control_panel.png';
import swizzle_exercise1_result from '/img/instruments/videomancer/swizzle/swizzle_exercise1_result.png';
import swizzle_exercise2_result from '/img/instruments/videomancer/swizzle/swizzle_exercise2_result.png';
import swizzle_exercise3_result from '/img/instruments/videomancer/swizzle/swizzle_exercise3_result.png';
import swizzle_source1_kodim02 from '/img/instruments/videomancer/swizzle/swizzle_source1_kodim02.png';
import swizzle_source2_kodim07 from '/img/instruments/videomancer/swizzle/swizzle_source2_kodim07.png';
import swizzle_source3_kodim01_bw from '/img/instruments/videomancer/swizzle/swizzle_source3_kodim01_bw.png';

# Swizzle

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: swizzle_source1_kodim02, after: swizzle_hero },
    { label: "Kodim07", before: swizzle_source2_kodim07, after: swizzle_hero },
    { label: "Kodim01 B&W", before: swizzle_source3_kodim01_bw, after: swizzle_hero },
  ]}
/>
*Swizzle reordering and offsetting YUV channels to shift hues and reveal the hidden color structure of video signals.*

---

## Overview

Every pixel in the Videomancer video pipeline is a triplet of numbers — luminance (Y), and two chrominance components (U and V). Under normal circumstances these three channels stay locked together, faithfully reproducing the colors of the source material. Swizzle breaks that lock. It lets you rearrange which data goes to which channel, add DC offsets to shift the color balance, and invert the brightness — revealing the hidden internal structure of the YUV color space.

The name comes from computer graphics, where a "swizzle" is a reordering of the components of a vector. In GPU programming, swizzling a color vector means selecting and rearranging its R, G, B, and A components in arbitrary order. Swizzle applies this same concept to the YUV domain: you can swap the two chroma axes, rotate all three channels in a cycle, or leave them in place and simply shift their DC levels. Even a small offset on the U or V channel produces dramatic hue rotations across the entire image.

At default settings Swizzle passes the signal unmodified. As you engage the swaps, rotation, inversion, and offsets, the image transforms from a faithful reproduction into an abstract color-field study. Because the operations are simple arithmetic — addition, subtraction, and channel reordering — the results are always clean and alias-free, with no noise or spatial artifacts.

> **Note:** The Rotation (Knob 4), Scale (Knob 5), Spread (Knob 6), and Border (Switch 10) controls are reserved for a future firmware update. In the current version they are declared in the FPGA source but not wired into the processing pipeline. Adjusting them will have no visible effect.

---

## Background

### What Is Channel Swizzling?

In GPU shader programming, a *swizzle* is a compile-time reordering of vector components. Writing `color.bgr` instead of `color.rgb` swaps the red and blue channels. Swizzle applies this concept in the YUV domain. Swapping U and V mirrors the color wheel — warm tones become cool and vice versa. Rotating all three channels (Y→U→V→Y) feeds brightness data into the chrominance channels and chroma data into the luminance channel, producing psychedelic false-color imagery where the image structure is recognizable but the colors are completely alien.

### YUV Color Space and DC Offsets

In YUV encoding, Y carries brightness (0 = black, 1023 = white) while U and V carry color difference signals centered at 512. A pixel with U = V = 512 has no chroma — it is a shade of gray. Adding a positive offset to U shifts all colors toward blue; subtracting shifts toward yellow. Adding to V shifts toward red; subtracting toward cyan. Offsetting Y shifts the overall brightness. Because these are linear additions, the relative structure of the image is preserved — gradients stay smooth, edges stay sharp — only the overall color balance changes.

### Luminance Inversion

Inverting Y replaces each brightness value with its complement: Y′ = 1023 − Y. Black becomes white, white becomes black, and mid-grays stay roughly the same. This is a simple linear negative. Combined with channel swizzling, inversion can produce striking results because the brightness data that gets swizzled into the chroma channels is now reversed, creating a complementary palette.

### Channel Rotation vs. Channel Swap

Swizzle offers two distinct channel reordering modes. *Swap UV* exchanges the two chroma channels while leaving luminance untouched — this is a mirror of the color wheel. *Rotate Ch* performs a three-way cyclic permutation: the original V channel becomes the new Y, the original Y becomes the new U, and the original U becomes the new V. This is a much more radical transformation because luminance and chrominance data cross domains. Rotate Ch takes priority over Swap UV — if both are enabled, only the rotation applies.

### Feedback and Signal Chains

Because Swizzle's output is a valid video signal with the same format as its input, it can be fed back into itself or chained with other programs. Feeding Swizzle's output back to its input with a small chroma offset creates a slowly drifting color palette that evolves over time. Chaining two Swizzle instances allows independent rotation plus offset, building complex color transformations from simple primitives.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ─────────────────────────────────────────────────
├── U Channel ─────────────────────────────────────────────────
├── V Channel ─────────────────────────────────────────────────
│
├─ 1. Channel Reorder ────────────────────────────────────────
│      Rotate Ch ON:  Y←V, U←Y, V←U  (3-way cyclic)
│      Swap UV ON:    Y←Y, U←V, V←U  (chroma mirror)
│      Both OFF:      pass-through
│
├─ 2. Invert Y ───────────────────────────────────────────────
│      Y ← 1023 − Y  (optional brightness complement)
│
├─ 3. DC Offsets ─────────────────────────────────────────────
│      Y ← Y + (Y Offset − 512)
│      U ← U + (U Offset − 512)
│      V ← V + (V Offset − 512)
│
├─ 4. Clamp ──────────────────────────────────────────────────
│      Clamp all channels to [0, 1023]
│
├─ 5. Mix (interpolator_u × 3) ──────────────────────────────
│      result = lerp(dry, wet, Mix)
│
├── Sync Signals ──────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, delayed to match)
│
└── Bypass ────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The channel reorder stage sits before offsets and inversion, so the DC shifts apply to whatever data is in each channel *after* the swap or rotation. If you rotate channels and then add a U offset, you are offsetting the data that was originally in the Y channel. This interaction is the key to Swizzle's expressive range — the combination of reordering and offsetting creates color transformations that would be difficult to achieve with either operation alone.

The Invert Y stage applies to the Y channel after reordering. If Rotate Ch is active, the data in the Y channel at that point is actually the original V data — so inversion complements the V signal, not the original luminance.

---

## Parameter Reference

<img src={swizzle_control_panel} alt="Videomancer front panel with Swizzle loaded"/>
*Videomancer's front panel with Swizzle active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

DC offset applied to the Y channel after any channel reorder. The control is centered at 50% (register value 512), where it has zero effect. Turning clockwise brightens the image; turning counter-clockwise darkens it. At the extremes the image is pushed to full white or full black. Combined with Invert Y, this acts as a brightness-with-polarity control.

---

#### Knob 2 — U Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

DC offset applied to the U channel. Centered at 50% for zero effect. Positive offsets shift colors toward blue; negative offsets shift toward yellow. Even small adjustments produce visible hue shifts across the entire image. With Swap UV or Rotate Ch active, this offset applies to whatever data occupies the U channel after reordering.

---

#### Knob 3 — V Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

DC offset applied to the V channel. Centered at 50% for zero effect. Positive offsets shift colors toward red/magenta; negative offsets shift toward green/cyan. Combined with the U Offset, these two controls let you navigate the full chrominance plane — any target hue can be reached by setting appropriate U and V offsets.

---

#### Knob 4 — Rotation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for a future firmware update. This control is declared in the FPGA source but not connected to the processing pipeline. Adjusting it has no visible effect on the output signal.

---

#### Knob 5 — Scale
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for a future firmware update. This control is declared in the FPGA source but not connected to the processing pipeline. Adjusting it has no visible effect on the output signal.

---

#### Knob 6 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Reserved for a future firmware update. This control is declared in the FPGA source but not connected to the processing pipeline. Adjusting it has no visible effect on the output signal.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Swap UV** | Off | On |
| **8 — Invert Y** | Off | On |
| **9 — Rotate Ch** | Off | On |
| **10 — Border** | Off | On |
| **11 — Bypass** | Off | On |

Three of the five toggles control the processing pipeline: Swap UV mirrors the chrominance axes, Invert Y complements the brightness channel, and Rotate Ch performs a three-way channel cycle. Rotate Ch takes priority over Swap UV — enabling both results in rotation only. The Border toggle (Switch 10) is reserved and has no effect. Bypass routes the input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original signal and the processed result. At 100%, the output is fully processed. At 0%, the output is the unmodified input. Intermediate positions blend the two, allowing subtle color shifts without fully committing to the swizzled result.

---

## Guided Exercises

These exercises progress from simple DC color shifts to full channel reordering, building an intuition for how YUV channel manipulation creates color transformations.

### Exercise 1: Chroma Offset Color Wash

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: swizzle_source1_kodim02, after: swizzle_exercise1_result },
    { label: "Kodim07", before: swizzle_source2_kodim07, after: swizzle_exercise1_result },
    { label: "Kodim01 B&W", before: swizzle_source3_kodim01_bw, after: swizzle_exercise1_result },
  ]}
/>
*Chroma Offset Color Wash — simulated result across source images.*
**Source**: A live camera feed or recorded footage with natural colors (skin tones, foliage, sky).

**Objective**: Learn how U and V offsets shift the overall color palette without affecting image structure.

1. **Baseline**: Confirm all controls at default (offsets centered, toggles off, mix 100%).
2. **Blue shift**: Slowly turn U Offset clockwise past center. Watch the entire image shift toward blue.
3. **Red shift**: Return U Offset to center. Now turn V Offset clockwise. The image shifts toward red/magenta.
4. **Diagonal hue**: Set both U and V Offset slightly above center. The combined shift creates a purple or teal wash depending on the direction.
5. **Brightness offset**: Turn Y Offset above center to brighten the color-washed image. Note how the color tint remains constant while brightness changes.

**Key concepts**: U and V offsets navigate the chrominance plane, Y offset shifts brightness independently, offsets are additive and preserve image structure

---

### Exercise 2: Channel Swap and Inversion

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: swizzle_source1_kodim02, after: swizzle_exercise2_result },
    { label: "Kodim07", before: swizzle_source2_kodim07, after: swizzle_exercise2_result },
    { label: "Kodim01 B&W", before: swizzle_source3_kodim01_bw, after: swizzle_exercise2_result },
  ]}
/>
*Channel Swap and Inversion — simulated result across source images.*
**Source**: Footage with strong color contrast — flowers, neon signs, or color bars.

**Objective**: Explore channel reordering and luminance inversion as compositional tools.

1. **Swap UV**: Enable Swap UV (Switch 7). Observe how warm and cool colors trade places.
2. **Add inversion**: Enable Invert Y (Switch 8) while keeping Swap UV on. The brightness inverts while the color swap remains, creating a complementary negative.
3. **Rotate channels**: Disable Swap UV and Invert Y. Enable Rotate Ch (Switch 9). The image transforms into psychedelic false color.
4. **Rotate + invert**: Enable Invert Y with Rotate Ch still active. The false-color palette shifts to its complement.
5. **Offset the rotation**: With Rotate Ch on, slowly increase U Offset. Because Y data is now in the U channel, this offset shifts the luminance-derived color component.

**Key concepts**: Swap UV mirrors the color wheel, Rotate Ch creates false-color by crossing luminance and chrominance domains, inversion complements whatever data occupies the Y channel, offsets apply after reordering

---

### Exercise 3: Subtle Color Grading with Mix

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: swizzle_source1_kodim02, after: swizzle_exercise3_result },
    { label: "Kodim07", before: swizzle_source2_kodim07, after: swizzle_exercise3_result },
    { label: "Kodim01 B&W", before: swizzle_source3_kodim01_bw, after: swizzle_exercise3_result },
  ]}
/>
*Subtle Color Grading with Mix — simulated result across source images.*
**Source**: Cinematic footage or any material where subtle color grading is appropriate.

**Objective**: Use Swizzle as a color grading tool by blending processed and original signals.

1. **Set a hue shift**: Enable Swap UV. Set U Offset to ~55%, V Offset to ~45%.
2. **Reduce mix**: Lower the Mix fader to ~30%. The output blends 30% of the swizzled signal with 70% of the original.
3. **Fine-tune offsets**: Adjust U and V Offset in small increments while watching the blended result. The low mix amount means even large offset changes produce subtle shifts.
4. **Try rotation at low mix**: Enable Rotate Ch instead of Swap UV. At 20% mix, the psychedelic rotation becomes a subtle color cast.
5. **Compare**: Toggle Bypass to compare the graded result against the original.

**Key concepts**: Mix fader enables subtle color grading from extreme processing, blending swizzled and original signals creates usable tint effects, bypass provides instant A/B comparison

---


## Tips

- **Offsets are centered at 50%**: The Y, U, and V Offset knobs have zero effect at their midpoint. Turn clockwise for positive shift, counter-clockwise for negative. This bipolar behavior is key to navigating the color space.
- **Swap UV for quick complementary colors**: A single toggle flip mirrors the entire color wheel — an instant way to see what the complementary palette of your source looks like.
- **Rotate Ch for false color**: Channel rotation is the most dramatic transformation. It maps brightness into color and color into brightness, creating imagery that is structurally related to the source but chromatically unrecognizable.
- **Low mix for color grading**: Even extreme swizzle settings become usable color grades when the Mix fader is set to 10–30%. This is a powerful, fast color correction tool.
- **Feedback creates drift**: Route the output back to the input with a tiny chroma offset. The color palette will slowly drift through the hue wheel as the offset accumulates frame over frame.
- **Reserved knobs**: Rotation (Knob 4), Scale (Knob 5), Spread (Knob 6), and Border (Switch 10) are reserved for a future update. Leave them at their defaults — they currently have no effect.
- **Invert + Rotate = complementary false color**: Combining luminance inversion with channel rotation creates the complement of the false-color palette, doubling the number of available looks without touching the offset knobs.
- **Clean signal path**: Swizzle uses only addition and channel selection — no multiplication, no spatial filtering, no memory. The output is always clean and alias-free.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | The ITU television standard defining the YUV color encoding used throughout the Videomancer video pipeline. |
| **Channel Rotation** | A cyclic permutation of three components (Y→U→V→Y), moving each channel's data to the next position in the cycle. |
| **Chrominance** | The color information in a video signal, encoded as U and V components centered at 512 in 10-bit representation. |
| **DC Offset** | A constant value added to a signal, shifting its entire range up or down without changing its shape. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interpolator** | A hardware module that linearly blends two input values based on a mix parameter (lerp). |
| **Luminance** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Swizzle** | In GPU programming, a reordering of vector components; in this program, a reordering of YUV channels. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
