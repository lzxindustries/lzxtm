---
draft: true
sidebar_position: 2
slug: /instruments/videomancer/bitcullis
title: "Bitcullis"
---

import bitcullis_hero from '/img/instruments/videomancer/bitcullis/bitcullis_hero.png';
import bitcullis_control_panel from '/img/instruments/videomancer/bitcullis/bitcullis_control_panel.png';
import bitcullis_posterization_levels from '/img/instruments/videomancer/bitcullis/bitcullis_posterization_levels.png';
import bitcullis_exercise2_result from '/img/instruments/videomancer/bitcullis/bitcullis_exercise2_result.png';
import bitcullis_exercise3_result from '/img/instruments/videomancer/bitcullis/bitcullis_exercise3_result.png';

# Bitcullis

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={bitcullis_hero} alt="Bitcullis processed video output showing pixelation, posterization, and dithering effects on a natural source"/>

*Bitcullis reduces, quantizes, and rearranges the digital structure of any video source in real time — turning high-resolution imagery into mosaic, posterized, and dithered graphics.*

---

## Overview

Digital video is made of discrete numbers — brightness and color values laid out on a grid of pixels. Most video processing tries to hide that fact, making the grid and the numbers as smooth and invisible as possible. Bitcullis does the opposite. It takes the digital structure of the signal and makes it the subject.

The program chains seven processing stages together — spatial decimation (horizontal and vertical pixelation), luminance-driven modulation of those effects, ordered and random dithering, posterization (bit-depth reduction), bit-order reversal, and luminance threshold keying. Every stage operates simultaneously on every pixel of every frame. The name is a portmanteau of *bit* (the fundamental digital unit) and *portcullis* (the iron gate of a castle) — a gate made of bits, controlling what passes through.

At conservative settings, Bitcullis can create subtle mosaic textures or gentle posterization. At extreme settings, it reduces video to hard-edged block graphics, glitch patterns, and abstract digital structures that bear little resemblance to the source.

---

## Background

### What Is Spatial Decimation?

Bitcullis's horizontal and vertical decimation controls implement **sample-and-hold** downsampling. The effect is identical to what happens when you reduce a high-resolution image to a very low resolution and then scale it back up without interpolation — pixels become visible as uniform blocks. Television engineers call this "decimation" because it discards samples. Bitcullis uses a frequency accumulator to control the decimation rate, which means the block size is continuously variable rather than limited to integer ratios.

The horizontal and vertical axes are controlled independently. You can create wide horizontal bars (high vertical decimation, low horizontal), tall vertical columns (high horizontal, low vertical), or uniform square blocks (both equal). Because the decimation frequency is controlled by an accumulator, the block boundaries can shift and alias in interesting ways as you sweep the controls.

### What Is Posterization?

When you reduce the number of brightness or color levels that a pixel can take, the smooth gradients in an image collapse into flat regions separated by hard edges. This effect is called **posterization** — named after the appearance of screen-printed posters, which use a small number of ink colors to represent a continuous image. Bitcullis applies posterization independently to the luminance and chrominance channels, so you can crush the brightness resolution while leaving color smooth, or vice versa.

### What Is Dithering?

Dithering is a technique for making a low-bit-depth image appear to have more tonal levels than it actually contains. It works by adding a small, structured noise pattern to the signal *before* quantization. The noise pushes pixel values across quantization boundaries in a pattern that, from a distance, creates the illusion of intermediate tones. Bitcullis offers two dithering algorithms: **ordered dithering** (a fixed 2×2 or 4×4 Bayer matrix) and **random dithering** (an LFSR pseudo-random pattern). Ordered dithering produces a regular stipple texture; random dithering produces a film-grain-like noise.

### What Is Bit-Order Reversal?

Every pixel value is stored as a 10-bit binary number. The **bit-order reversal** toggle flips the significance of those bits — the most significant bit becomes the least significant and vice versa. This is not a simple inversion (which flips 1s to 0s); it is a *permutation* of the binary representation. The result is a nonlinear, often chaotic remapping of brightness and color values that produces glitch-like visual artifacts.

---

## Signal Flow

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

Two key interactions to notice:

1. **Luminance-driven modulation**: The Y channel (after inversion) drives *two* modulation controls. Luma→Hori varies the horizontal decimation frequency pixel-by-pixel based on brightness — bright areas can have larger or smaller blocks than dark areas, creating luminance-adaptive mosaic patterns. Luma→Chroma varies the chroma saturation based on brightness, linking color intensity to tonal value.

2. **Processing order**: Decimation happens *before* posterization, so the posterizer quantizes the already-pixelated signal. Dithering sits between decimation and posterization, adding noise to the blocky signal before it gets quantized. This order matters — dithering before quantization is what makes the technique work.

---

## Parameter Reference

<img src={bitcullis_control_panel} alt="Videomancer front panel with Bitcullis loaded, controls annotated"/>

*Videomancer's front panel with Bitcullis active. Knobs 1–6, Switches 7–11, and Fader 12 are labeled with their Bitcullis functions.*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Hori Decimate
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.0% (center) |
| Suffix | % |

Controls the **horizontal decimation frequency** — how often the signal is re-sampled along each scan line. At 0%, the signal is re-sampled so rarely that each row becomes virtually a single color (maximum pixelation). At 200%, the signal is sampled at or near full resolution (minimal pixelation). The default center position produces a moderate mosaic effect. This control sets the *base* frequency — the Luma to Hori control (Knob 3) can further modulate it on a per-pixel basis.

---

#### Knob 2 — Vert Decimate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **vertical decimation frequency** — how often the signal is re-sampled across scan lines. At 0%, each column of the image is stretched into wide horizontal bands. At 100%, each line is sampled independently (minimal vertical pixelation). Combined with Hori Decimate, this creates the block size and shape of the mosaic pattern: equal settings produce square blocks; unequal settings produce rectangles.

---

#### Knob 3 — Luma to Hori
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls how strongly the **input luminance modulates the horizontal decimation frequency**. At center (50%), there is a moderate modulation — bright areas get a different block size than dark areas. At 0%, there is less modulation (more uniform blocks). At 100%, the modulation is strongest, creating dramatic luminance-adaptive mosaic patterns where bright and dark regions of the image have visibly different pixel sizes.

This is one of Bitcullis's most distinctive controls. Because the decimation frequency varies with brightness, the mosaic pattern follows the tonal structure of the source image — edges between bright and dark regions create boundaries between different block sizes.

---

#### Knob 4 — Luma Poster
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% (fully CCW) |
| Suffix | % |

Controls the **luminance posterization depth** — how many brightness levels survive quantization. At 0%, the full 10-bit resolution is preserved (1024 levels). As you increase the value, the number of distinct brightness levels decreases: the smooth tonal ramp collapses into a staircase of flat regions separated by hard edges. At 100%, only a handful of levels remain — the image becomes a stark, high-contrast graphic.

<img src={bitcullis_posterization_levels} alt="Posterization levels illustration showing how bit-depth reduction collapses smooth gradients into discrete steps"/>

*Posterization quantizes the luminance ramp into discrete steps. More posterization (right) means fewer brightness levels and harder tonal boundaries.*

---

#### Knob 5 — Chroma Poster
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **chrominance posterization depth** — the same bit-depth reduction applied to the U and V color channels independently of the Y channel. At 0%, full color resolution is preserved. At 100%, the color channels are reduced to a handful of levels, producing abrupt color transitions and banding. Setting Chroma Poster high while keeping Luma Poster low creates an image with smooth brightness but posterized color — a painterly, silk-screen-like effect.

---

#### Knob 6 — Luma to Chroma
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls how strongly the **input luminance modulates chroma saturation**. This is a proc amp stage that uses the Y channel value as a gain multiplier for the U and V channels. At center (50%), there is a moderate correlation. Below center, less modulation. Above center, bright areas become more saturated and dark areas become less saturated (or vice versa, depending on Luma Invert). The result is a tonal-dependent color intensity that links brightness to vividness.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Luma Invert** | Normal luminance | Luminance inverted (negative) |
| **8 — Bit Order** | Normal bit ordering | Bits reversed (MSB↔LSB) |
| **9 — Dithering** | Dithering disabled | Dithering enabled |
| **10 — Dither Algo** | 2×2 ordered (Bayer) | 4×4 random (LFSR) |
| **11 — Bypass** | Processing active | Bypass (signal passes unmodified) |

**Luma Invert** applies a bitwise complement to the luminance channel as the *first* processing step — before decimation and all subsequent stages. Because the luma-to-hori and luma-to-chroma modulation paths also use the inverted signal, flipping this switch reverses which brightness regions get larger blocks and more saturation.

**Bit Order** reverses the significance of all 10 bits in each YUV channel after posterization. The value `0b1000000000` (512, neutral gray) becomes `0b0000000001` (1, near-black). `0b1111111111` (1023, peak white) stays `0b1111111111` (1023). The mapping is highly nonlinear and produces glitch-like visual patterns that are deterministic but unpredictable to the eye.

**Dithering** enables noise injection before the posterization stage. The noise pattern is chosen by the Dither Algo toggle. Dithering is most visible when posterization is active — without posterization, the dither noise is too small to see at full bit depth.

**Dither Algo** selects between two dithering methods:
- **2×2**: A fixed ordered dither pattern (Bayer matrix). Produces a regular, visible stipple grid — the classic "newspaper dot" look.
- **4×4**: A pseudo-random dither pattern generated by a 16-bit linear feedback shift register. Produces an irregular, film-grain-like noise.

**Bypass** routes the input signal directly to the output, skipping all processing. Useful for instant before/after comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% (fully up) |
| Suffix | % |

The Threshold fader sets a luminance key at the end of the processing chain. Any pixel whose processed Y value falls below the threshold is replaced with black (Y = 0) and neutral chroma (U = V = 512). At 100% (default), the threshold is at maximum — everything passes through. As you lower the fader, progressively darker portions of the processed image snap to black.

Because the threshold operates on the *processed* signal (after decimation, posterization, and bit reversal), it interacts with every upstream stage. Posterization creates hard tonal boundaries, and the threshold key can slice cleanly between those boundaries, creating graphic cutout effects. Bit-order reversal scrambles the brightness mapping, so the threshold cuts through the glitch pattern in unexpected ways.

---

## Guided Exercises

### Exercise 1: Mosaic Pixelation

**Source**: A live camera feed or recorded footage with recognizable subjects — faces, landscapes, or objects with clear silhouettes.

**Objective**: Learn how the horizontal and vertical decimation controls create mosaic patterns and how luminance modulation adds adaptive structure.

1. **Initialize**: Load Bitcullis with all defaults. The image should pass through with moderate pixelation already visible (Hori Decimate at center).

2. **Horizontal pixelation**: Turn **Hori Decimate** fully CCW. The image collapses into wide horizontal color bands — each scan line is reduced to a few held values. Now slowly turn clockwise. Watch the blocks shrink as the sampling frequency increases. Past center, the blocks become very small and the image approaches the original.

3. **Vertical pixelation**: Return Hori Decimate to center. Turn **Vert Decimate** fully CCW. Horizontal bands appear — each cluster of scan lines displays the same value. Combine both axes: set Hori Decimate to about 30% and Vert Decimate to about 30%. Uniform square blocks appear, creating a classic mosaic.

4. **Luminance-adaptive mosaic**: With both decimation controls at moderate settings (~40%), slowly sweep **Luma to Hori** from 0% to 100%. Watch how bright and dark regions of the image develop different block sizes. At high modulation, the mosaic pattern follows the tonal contours of the source — bright areas might resolve into small, detailed blocks while dark areas dissolve into large, flat regions.

5. **Invert the modulation**: With Luma to Hori at a high value, flip **Luma Invert** on. The relationship reverses — dark areas now get the small blocks and bright areas get large ones. This creates a completely different mosaic character from the same source.

:::tip
Hori and Vert Decimate set the base block size. Luma to Hori modulates horizontal blocks by brightness. Luma Invert reverses the modulation mapping.
:::

---

### Exercise 2: Posterized Graphics

<img src={bitcullis_exercise2_result} alt="Posterized video — a natural scene reduced to flat color regions with hard tonal boundaries"/>

*Luma Poster at 60%, Chroma Poster at 70%, Dithering enabled with ordered Bayer pattern — natural footage transformed into a screen-print graphic.*

**Source**: Footage with gradual tonal transitions — skin tones, skies, shadows, or color gradients.

**Objective**: Explore posterization and dithering to create graphic, print-inspired textures.

1. **Prepare**: Set both decimation controls to produce moderate pixelation (Hori ~60%, Vert ~50%). Set Luma to Hori and Luma to Chroma to center.

2. **Luma posterization**: Slowly turn **Luma Poster** from 0% toward 100%. Watch smooth gradients collapse into flat regions. At low values, the effect is subtle — just a few tonal steps disappear. At high values, the image becomes stark, with only a handful of brightness levels remaining.

3. **Chroma posterization**: Now sweep **Chroma Poster** from 0% to 100%. The color transitions break into bands while the brightness structure (set by Luma Poster) stays unchanged. Try high Chroma Poster with low Luma Poster — smooth brightness, banded color. Then reverse: high Luma Poster, low Chroma Poster — flat brightness blocks with smooth color gradients through them.

4. **Add dithering**: Flip **Dithering** (Switch 9) to Enabled. With Luma Poster at about 60%, the dither pattern becomes visible as a stipple texture within the posterized regions. The flat color blocks now contain a fine pattern that suggests intermediate tones. Toggle between **Dither Algo** 2×2 (ordered) and 4×4 (random) to compare the stipple character: ordered is regular and grid-like; random is noisy and organic.

5. **Bit reversal**: Turn Luma Poster back to about 40% and flip **Bit Order** to Swapped. The tonal mapping becomes chaotic — brightness values are scrambled by the bit permutation. Dark areas may become bright and vice versa, but the mapping is not a simple inversion. The result is a glitch-art texture that is completely deterministic (the same input always produces the same output) but appears random.

6. **Key the result**: Lower the **Threshold** fader to slice through the posterized/glitched image. Because posterization creates hard tonal steps, the threshold can isolate specific quantization levels, producing clean graphic cutouts.

:::tip
Luma and Chroma Poster are independent quantizers. Dithering adds noise before quantization to simulate intermediate levels. Bit Order Reversal scrambles the bit representation. Threshold key slices through the result.
:::

---

### Exercise 3: Digital Texture Synthesis

<img src={bitcullis_exercise3_result} alt="Extreme bit-manipulation — glitch patterns, dithered blocks, and threshold-keyed digital textures"/>

*Bit Order Swapped, Luma Poster at 80%, Dithering enabled (random), Threshold at 40% — the source image is deconstructed into abstract digital texture.*

**Source**: Any footage, but especially effective with high-contrast material, text, or geometric patterns.

**Objective**: Combine all of Bitcullis's processing stages to create abstract digital textures that transcend the source material.

1. **Start with strong modulation**: Set **Hori Decimate** to about 30%, **Vert Decimate** to about 25%. Set **Luma to Hori** to about 80% and **Luma to Chroma** to about 75%. The image is now a luminance-adaptive mosaic with brightness-driven color modulation.

2. **Add posterization**: Set **Luma Poster** to about 70% and **Chroma Poster** to about 60%. The mosaic blocks are now quantized into flat tonal and color steps.

3. **Enable dithering**: Turn on **Dithering** and select **4×4** (random). The dither adds a grainy texture to the quantized blocks.

4. **Reverse the bits**: Flip **Bit Order** to Swapped. The image transforms dramatically — the bit permutation remaps every brightness and color value. The mosaic structure remains but the tonal content is completely scrambled.

5. **Sculpt with the threshold**: Lower the **Threshold** fader from 100% to about 40%. Dark regions of the bit-reversed image snap to black, carving away portions of the texture and revealing the abstract structure.

6. **Explore inversions**: Toggle **Luma Invert** to change which brightness regions drive the modulation. Because inversion happens before decimation, the entire mosaic and modulation character shifts.

7. **Animate**: Move controls slowly while watching the output. Bitcullis responds to every change in real time — sweeping Luma to Hori while the source moves creates an evolving, living digital texture.

:::tip
Bitcullis is a layered signal deconstruction tool. Each stage reduces or rearranges information in a different way, and the stages compound: decimation → dithering → posterization → bit-reversal → threshold. The order matters, and the interactions create results that are far more complex than any single stage could produce alone.
:::

---

## Tips

- **Order matters**: The signal flows through Inversion → Modulation → Decimation → Dithering → Posterization → Bit Reversal → Threshold. Each stage transforms the signal before the next. Dithering only matters if posterization is active. Bit reversal scrambles the posterized result. Threshold cuts through whatever the upstream stages produced.

- **Dithering needs posterization**: Dithering adds ±8 counts at 10-bit resolution (a tiny perturbation). Without posterization to quantize those perturbations into visible tonal steps, the dither pattern is imperceptible. Enable both together.

- **Luma modulation is the signature effect**: Most pixelation tools create uniform block sizes. Bitcullis's luminance-to-horizontal modulation creates *adaptive* mosaics where block size follows the tonal structure of the image. This is what makes it different from a simple resize.

- **Bit reversal is not inversion**: Luma Invert flips all bits (0↔1), which is a linear brightness reversal. Bit Order Reversal *permutes* the bit positions (MSB↔LSB), which is a wild nonlinear transformation. Both are available; they do very different things.

- **Feedback loops**: If Videomancer's output is routed back to its input, Bitcullis's decimation and posterization create self-referencing block structures that evolve over time. Each feedback pass re-decimates and re-quantizes the already-processed signal, creating cascading pixel patterns.

- **Bypass for A/B comparison**: Switch 11 (Bypass) instantly shows the unprocessed signal. Use it to evaluate how much the processing has departed from the source. Toggle rapidly for a "before/after" effect.
