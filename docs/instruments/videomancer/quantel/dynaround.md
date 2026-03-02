---
draft: true
sidebar_position: 90
slug: /instruments/videomancer/dynaround
title: "Dynaround"
image: /img/instruments/videomancer/dynaround/dynaround_hero.png
description: "Every digital video system must decide how many bits to use for each pixel."
---

import dynaround_hero from '/img/instruments/videomancer/dynaround/dynaround_hero.png';
import dynaround_before_after from '/img/instruments/videomancer/dynaround/dynaround_before_after.png';
import dynaround_control_panel from '/img/instruments/videomancer/dynaround/dynaround_control_panel.png';
import dynaround_exercise1_result from '/img/instruments/videomancer/dynaround/dynaround_exercise1_result.png';
import dynaround_exercise2_result from '/img/instruments/videomancer/dynaround/dynaround_exercise2_result.png';
import dynaround_exercise3_result from '/img/instruments/videomancer/dynaround/dynaround_exercise3_result.png';

# Dynaround

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={dynaround_hero} alt="Dynaround hero image"/>
*Dynaround applying probabilistic dynamic rounding and blue-noise dithering to reduce bit depth while preserving tonal smoothness across luminance and chrominance channels.*
<img src={dynaround_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Dynaround applied.*

---

## Overview

Every digital video system must decide how many bits to use for each pixel. More bits mean smoother gradients and subtler color transitions; fewer bits mean visible steps between adjacent levels — the flat bands and hard contours known as posterization. In professional broadcast engineering, the question was never merely *how many* bits to keep but *how* to discard the rest. The answer shaped the visual quality of an entire generation of television equipment.

Dynaround brings six different bit-discard strategies into a single FPGA program, turning a problem of engineering necessity into a creative tool. The name references the Quantel Dynamic Rounding technique — a patented method from the 1980s that used the discarded bits themselves as a randomness source for probabilistic rounding, achieving statistically perfect reconstruction without the cumulative errors of truncation or the visible patterns of ordered dithering. Alongside this signature mode, Dynaround offers simple truncation, ordered Bayer dithering, LFSR-driven blue noise, temporal field-alternating dither, and 1D error diffusion. Each mode sculpts the quantization boundary differently, yielding distinct visual textures from the same bit-depth reduction.

The Y and UV channels can be reduced independently from 10 bits down to 1 bit, with an optional lock that forces chrominance to follow the luminance depth. A pre-dither contrast expansion stage stretches the signal before quantization, emphasizing or compressing the tonal range that gets carved into steps. An LFSR grain overlay adds analog-style noise on top of the quantized result, and a wet/dry mix fader allows continuous blending between the processed and original signals.

---

## Background

### Dynamic Rounding: The Quantel Innovation

In 1982, Quantel Ltd. patented a technique called Dynamic Rounding for their digital video effects systems. The problem they faced was fundamental: every time a video signal passes through a digital processor that operates at a lower internal precision than the input word length, the discarded least-significant bits introduce quantization error. If you simply truncate (round toward zero), the error accumulates across cascaded processing stages and manifests as visible banding. Quantel's insight was elegant — use the *discarded bits themselves* as a comparison value against a pseudo-random number. If the discarded bits exceed the random threshold, round up; otherwise, round down. Because the discarded bits already encode the sub-quantum residual, this comparison produces a statistically unbiased rounding decision with zero net DC error. The technique was so effective that Quantel hardware could cascade dozens of processing stages without visible degradation — a feat that simple truncation or conventional rounding could not match.

### Ordered Dithering and the Bayer Matrix

Ordered dithering dates to the earliest days of digital image processing. The idea is to add a spatially varying threshold *before* quantization, so that pixels near a level boundary get pushed alternately above and below it in a repeating pattern. The Bayer matrix — a recursively constructed threshold map — is the most common ordered dither kernel because it distributes threshold values as uniformly as possible across the tile. The result is a characteristic stipple pattern: regular, structured, and visually reminiscent of newspaper halftone printing. Dynaround uses a 4×4 Bayer matrix, producing a 16-level threshold pattern that tiles across the frame.

### Error Diffusion and Floyd-Steinberg

Error diffusion takes a different approach. Instead of adding noise *before* quantization, it computes the quantization error *after* rounding and propagates that error to neighboring pixels. The Floyd-Steinberg algorithm (1976) distributes the error to four neighbors using fixed fractional weights. Dynaround implements a simplified 1D variant: the full quantization error of each pixel is carried forward to the next pixel on the same scanline. This produces smoother gradients than ordered dithering at the cost of directional bias — error propagates left to right, creating subtle horizontal texture. The error carry resets at each scanline boundary to prevent runaway accumulation.

### Blue Noise and Pseudo-Random Dithering

Blue noise refers to a randomness spectrum with minimal low-frequency energy — no clumps, no patterns, just evenly distributed randomness. True blue noise requires pre-computed void-and-cluster textures, but LFSR-based pseudo-random noise is a practical approximation that avoids the structured patterns of ordered dithering while adding less visible texture than white noise. Dynaround's blue noise mode uses three independent 16-bit Galois LFSRs (one per channel) scaled by the dither intensity control. The LFSR Seed parameter shifts the generator's starting state, allowing different noise textures from frame to frame.

### Temporal Dithering

Television's interlaced scanning provides a natural two-phase dithering opportunity. Temporal dithering alternates the rounding direction on even and odd fields: on even fields, pixels above the quantization midpoint round up; on odd fields, they round down. At the display's field rate (50 or 60 Hz), the viewer's eye integrates both fields, perceiving an intermediate level that neither field contains. This is the same principle behind CRT phosphor persistence and LCD frame-rate-conversion dithering (FRC) used in modern displays to simulate 10-bit color depth from 8-bit panels.


---

## Signal Flow

```
Input Video (YUV 4:4:4, 10-bit)
│
├─ Stage 1: Contrast Expansion ─────────────────────────────────
│   (val - 512) × contrast / 512 + 512
│   Applied to Y, U, V independently
│
├─ Stage 2: Dither Engine (6 modes) ────────────────────────────
│   ┌─ Mode 0: Dynamic Round ──── discarded bits vs. LFSR
│   ├─ Mode 1: Truncate ────────── bit discard + expand
│   ├─ Mode 2: Ordered Bayer ──── 4×4 threshold + truncate
│   ├─ Mode 3: Blue Noise ──────── LFSR random + truncate
│   ├─ Mode 4: Temporal ────────── field-alternating round
│   └─ Mode 5: Error Diffusion ── 1D scanline carry
│   │
│   Bit depth: Y = Pot 1 (1-10), UV = Pot 2 or locked to Y
│   Truncate-expand: MSB replication for full-range mapping
│
├─ Stage 3: Grain Overlay ──────────────────────────────────────
│   LFSR noise × grain amount, added to dithered result
│   Y uses full grain range, UV uses half
│
├─ Stage 4: Reassemble ────────────────────────────────────────
│   Combine Y, U, V into output stream
│
├─ Stage 5: Wet/Dry Mix ───────────────────────────────────────
│   3× interpolator_u (delayed dry ↔ processed wet)
│   Mix = Fader 12
│
├─ Sync Delay Pipeline ────────────────────────────────────────
│   8-clock delay shift register for hsync, vsync, field, data
│
└─ Bypass Mux ─────────────────────────────────────────────────
    Toggle 11: select delayed original or mixed output
```

The critical interaction is between the contrast expansion stage and the dither engine. Contrast expansion stretches or compresses the signal range *before* bit depth reduction, which directly controls how many quantization steps fall within the visible range. At low contrast values, the signal is compressed toward mid-gray, so even aggressive bit reduction produces few visible steps. At high contrast, the full 10-bit range is stretched beyond clipping, maximizing the number of harsh posterization bands for a given bit depth.

The three LFSRs operate independently with different initial seeds (0xACE1, 0xBEEF, 0xCAFE), seeded additionally by the LFSR Seed parameter. This ensures Y, U, and V channels receive uncorrelated noise patterns in Dynamic Round and Blue Noise modes. The grain overlay stage uses the *same* LFSRs for its noise, but with independent scaling — Y receives the full grain amplitude while U and V receive half, preventing chrominance noise from overwhelming the subtler color signal.

---

## Parameter Reference

<img src={dynaround_control_panel} alt="Videomancer front panel with Dynaround loaded"/>
*Videomancer's front panel with Dynaround active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Depth
| Property | Value |
|----------|-------|
| Range | 1 bit – 10 bit |
| Default | 6 bit |
| Suffix |  bit |

Controls the luminance channel bit depth, ranging from 1-bit (two levels: black and white) through 10-bit (full resolution, 1024 levels). At low bit depths, the Y channel collapses into stark bands with hard contour edges — the severity of these contours depends on which dither mode is active. Dynamic Round smooths them probabilistically; Truncate leaves them razor-sharp; Ordered Bayer replaces them with stipple patterns. This control has the most dramatic visual impact because luminance carries the majority of perceived image detail.

---

#### Knob 2 — UV Depth
| Property | Value |
|----------|-------|
| Range | 1 bit – 10 bit |
| Default | 6 bit |
| Suffix |  bit |

Controls the chrominance bit depth for both U and V channels simultaneously. Reducing chroma depth independently of luma creates a distinctive painterly look — smooth brightness gradients paired with coarsely quantized color that snaps between hues. When UV Lock is engaged, this control is overridden and both channels follow the Y Depth setting. The independent mode is most useful for artistic effects where you want to selectively degrade color fidelity while preserving luminance structure.

---

#### Knob 3 — Dith Intns
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scales the dither amplitude for Ordered Bayer and Blue Noise modes. At 0%, these modes add no threshold offset, behaving identically to Truncate. As intensity increases, the threshold signal grows stronger, pushing more pixels across quantization boundaries. At extreme intensity, the dither pattern becomes visible as texture even at high bit depths. This control has no effect on Dynamic Round (which derives its threshold internally), Truncate (which uses no threshold), Temporal (which uses field parity), or Error Diffusion (which uses error carry).

---

#### Knob 4 — Grain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Adds LFSR pseudo-random noise *after* the dither and quantization stages. Unlike the dither modes, which operate *before* or *during* quantization to influence rounding decisions, grain is purely additive post-processing. At low values, it creates a subtle analog film texture. At high values, it overwhelms the quantized structure with dense, flickering noise. The grain is applied with half amplitude to the U and V channels compared to Y, keeping chrominance noise subdued relative to luminance.

---

#### Knob 5 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies a contrast expansion centered on mid-scale (512) before the signal enters the dither engine. At 50% (register 512), the signal passes unchanged. Below 50%, the signal is compressed toward mid-gray, reducing the effective dynamic range seen by the quantizer. Above 50%, the signal is expanded — bright and dark extremes are pushed further apart, potentially clipping, which increases the visible severity of quantization steps. This pre-processing stage provides artistic control over how the dither modes interact with the image's tonal distribution.

---

#### Knob 6 — LFSR Seed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the operational characteristics of the three internal LFSR pseudo-random generators. The LFSRs are 16-bit Galois type with taps at bits 15, 13, 12, and 10. This control does not directly seed the generators but influences their trajectory, producing visually different noise textures in Dynamic Round, Blue Noise, and Grain modes. Sweeping this control while processing video creates evolving noise patterns — useful for animation or for finding a noise character that complements a particular source.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Dither A** | Off | On |
| **8 — Dither B** | Off | On |
| **9 — Dither C** | Off | On |
| **10 — UV Lock** | Indep | Lock Y |
| **11 — Bypass** | Off | On |

Toggles 7, 8, and 9 form a 3-bit binary selector that chooses one of six dithering strategies. The combination is read as a 3-bit unsigned integer: Dither A is bit 0, Dither B is bit 1, Dither C is bit 2. Values 000 through 101 (0–5) select the six modes; values 110 and 111 (6–7) are undefined and fall through to the Error Diffusion handler. Toggle 10 locks the UV bit depth to match the Y depth. Toggle 11 is a global bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Wet/dry crossfade between the delayed original signal and the fully processed signal. At 0% (fader down), the output is entirely dry — the original signal passes through unchanged. At 100% (fader up), the output is entirely wet — the full dithered and quantized result. Intermediate positions blend between the two using three `interpolator_u` instances (one per channel). This is particularly effective for dialing in subtle dither textures: process aggressively with low bit depth, then blend back toward the original to taste.

---

## Guided Exercises

These exercises explore each dithering strategy and its interaction with bit depth, contrast, and grain. Start with the most historically significant mode — Dynamic Round — and progress through increasingly textural alternatives.

### Exercise 1: Dynamic Round — The Quantel Technique

<img src={dynaround_exercise1_result} alt="Dynamic Round — The Quantel Technique result"/>
*Dynamic Round — The Quantel Technique — simulated result across source images.*
**Source**: A color gradient test pattern or footage with smooth sky/skin tones that reveal quantization artifacts.

**Objective**: Understand how Dynamic Rounding uses discarded bits for probabilistic rounding, and compare its visual quality against simple truncation at several bit depths.

1. **Baseline truncation**: Set all toggles off (mode 000 = Dynamic Round). Set Y Depth to 4 bits. Note the smooth contouring.
2. **Switch to truncate**: Turn on Dither A only (mode 001 = Truncate). At 4 bits, hard posterization bands become visible.
3. **Compare at 3 bits**: Reduce Y Depth to 3 bits on both modes. The quality difference becomes dramatic — Dynamic Round maintains perceptual smoothness while Truncate produces stark staircase banding.
4. **UV independence**: Set UV Lock to Indep, reduce UV Depth to 2 bits while keeping Y at 6 bits. Watch chrominance collapse into coarse color blocks while luminance remains detailed.
5. **Contrast interaction**: On Dynamic Round, sweep Contrast from 0% to 100%. At high contrast, even Dynamic Round shows contours because the signal range exceeds the quantizer's ability to distribute rounding decisions.

**Key concepts**: Dynamic Rounding is statistically unbiased because it uses the discarded bits as the comparison threshold, truncation produces hard bands because it always rounds toward zero, independent Y/UV depth allows selective channel degradation

---

### Exercise 2: Ordered vs. Blue Noise Dither

<img src={dynaround_exercise2_result} alt="Ordered vs. Blue Noise Dither result"/>
*Ordered vs. Blue Noise Dither — simulated result across source images.*
**Source**: A photographic image with gradual tonal transitions — portraits, landscapes, or test gradients.

**Objective**: Compare the visual texture of Bayer ordered dithering against LFSR blue noise dithering, and explore how Dith Intns modulates each.

1. **Ordered Bayer**: Set Dither B on, all others off (mode 010). Set Y Depth to 3 bits, UV Lock on. A regular stipple grid appears in the gradient regions.
2. **Sweep intensity**: Turn Dith Intns from 0% to 100%. At zero, the mode behaves like truncation. As intensity rises, the Bayer pattern breaks up the quantization contours with increasing visibility.
3. **Blue Noise**: Switch to mode 011 (Dither A on, Dither B on, Dither C off). The regular grid dissolves into a random, grain-like texture.
4. **Seed variation**: Sweep LFSR Seed. The noise texture shifts character — different random sequences produce subtly different spatial distributions.
5. **Add grain**: Increase Grain to 30%. The post-dither noise overlays on top of the dither pattern, creating a denser, more analog-feeling texture.

**Key concepts**: Ordered dithering produces spatially structured patterns visible as a grid, blue noise dithering produces unstructured randomness resembling film grain, dither intensity scales the threshold amplitude before truncation

---

### Exercise 3: Error Diffusion and Temporal Dither

<img src={dynaround_exercise3_result} alt="Error Diffusion and Temporal Dither result"/>
*Error Diffusion and Temporal Dither — simulated result across source images.*
**Source**: High-contrast black-and-white footage or text patterns that expose error propagation and temporal flicker.

**Objective**: Explore the two modes that use context beyond the current pixel: error diffusion (spatial context) and temporal dither (temporal context).

1. **Temporal dither**: Set Dither C on, all others off (mode 100). Set Y Depth to 2 bits, UV Lock on. On interlaced or progressive-scan displays, the alternating round directions create an inter-field shimmer that perceptually increases the apparent bit depth.
2. **Error diffusion**: Switch to mode 101 (Dither A on, Dither C on). The banding dissolves into a directional texture — horizontal streaking as error propagates left to right along each scanline.
3. **Low bit depths**: Reduce to 1 bit. Error diffusion produces a one-bit halftone effect reminiscent of early Macintosh graphics. Temporal dither at 1 bit creates a flickering checkerboard.
4. **Grain overlay**: Add moderate Grain (40%) to both modes. The post-quantization noise masks the directional bias of error diffusion and smooths the temporal flicker.
5. **Mix for subtlety**: Set Mix to 50%, blending the aggressive 1-bit result with the original to create a ghostly, partially quantized overlay.

**Key concepts**: Error diffusion propagates rounding error to the next pixel on the scanline, temporal dither alternates rounding direction per field for inter-field integration, scanline error resets prevent runaway accumulation

---


## Tips

- **Dynamic Round is the default for a reason**: Mode 000 produces the most perceptually transparent bit-depth reduction. Start here and switch to other modes only when you want visible dither texture.
- **Ordered Bayer for retro aesthetics**: The 4×4 stipple pattern at 3–4 bits closely resembles early computer graphics and newspaper halftone printing.
- **Error Diffusion for organic halftones**: At 1-bit depth, error diffusion produces halftone-like textures reminiscent of early Macintosh screen graphics or laser-printed dithering.
- **Contrast is your gain stage**: Pre-dither contrast expansion is the most powerful way to control how aggressive the quantization appears — more effective than bit depth alone.
- **UV Lock simplifies exploration**: Lock UV to Y when learning the modes, then unlock for independent channel experiments.
- **Grain adds analog character**: A small amount of post-dither grain (10–20%) softens digital quantization edges without undoing the dither mode's texture.
- **Mix for parallel processing**: Run aggressive dithering at low bit depth, then blend back with the original at 30–50% for subtle detail-preserving texture.
- **LFSR Seed for animation**: Slowly automating the LFSR Seed parameter creates evolving noise textures — useful for generative visual compositions.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bayer Matrix** | A recursively constructed threshold pattern used in ordered dithering; distributes quantization decisions evenly across a tile grid. |
| **Bit Depth** | The number of binary digits used to represent each sample; 10-bit provides 1024 levels, 1-bit provides 2 levels. |
| **Blue Noise** | A randomness spectrum with minimal low-frequency energy, producing evenly distributed spatial noise without visible clumping. |
| **BT.601** | ITU-R Recommendation 601; the color space standard used for standard-definition video encoding (Y, Cb, Cr). |
| **Dynamic Rounding** | Quantel's patented technique using discarded bits as a pseudo-random threshold for probabilistic rounding. |
| **Error Diffusion** | A dithering technique where quantization error is propagated to neighboring pixels to preserve local average intensity. |
| **Floyd-Steinberg** | A 1976 error diffusion algorithm distributing quantization error to four neighboring pixels with fixed fractional weights. |
| **Galois LFSR** | A Linear Feedback Shift Register using XOR taps on the output bit; produces a maximal-length pseudo-random sequence. |
| **Grain** | Additive pseudo-random noise overlaid on the signal to simulate analog film texture. |
| **Interpolator** | A hardware module performing linear interpolation (crossfade) between two input signals based on a mix parameter. |
| **Posterization** | Visible banding artifacts caused by reducing the number of quantization levels in an image. |
| **Quantization** | The process of mapping a continuous or fine-grained signal to a smaller set of discrete levels. |
| **Truncation** | Discarding least-significant bits without rounding, always biasing toward zero. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V); used throughout the Videomancer video pipeline. |

---
