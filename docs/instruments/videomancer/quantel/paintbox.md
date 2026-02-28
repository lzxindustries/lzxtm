---
draft: true
sidebar_position: 187
slug: /instruments/videomancer/paintbox
title: "Paintbox"
image: /img/instruments/videomancer/paintbox/paintbox_hero.png
description: "Paintbox reduces the continuous 10-bit YUV color space to a finite number of discrete levels, creating the characteristic flat, posterized look of scree..."
---

import paintbox_before_after from '/img/instruments/videomancer/paintbox/paintbox_before_after.png';
import paintbox_control_panel from '/img/instruments/videomancer/paintbox/paintbox_control_panel.png';
import paintbox_exercise1_result from '/img/instruments/videomancer/paintbox/paintbox_exercise1_result.png';
import paintbox_exercise2_result from '/img/instruments/videomancer/paintbox/paintbox_exercise2_result.png';
import paintbox_exercise3_result from '/img/instruments/videomancer/paintbox/paintbox_exercise3_result.png';
import paintbox_hero from '/img/instruments/videomancer/paintbox/paintbox_hero.png';
import paintbox_source1_kodim15 from '/img/instruments/videomancer/paintbox/paintbox_source1_kodim15.png';
import paintbox_source2_kodim01 from '/img/instruments/videomancer/paintbox/paintbox_source2_kodim01.png';
import paintbox_source3_kodim01_bw from '/img/instruments/videomancer/paintbox/paintbox_source3_kodim01_bw.png';

# Paintbox

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={paintbox_hero} alt="Paintbox hero image"/>
*A sunset photograph reduced to eight flat color bands — each pixel snapped to its nearest palette entry with ordered dither softening the transitions between quantized zones.*
<img src={paintbox_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Paintbox applied.*

---

## Overview

Paintbox reduces the continuous 10-bit YUV color space to a finite number of discrete levels, creating the characteristic flat, posterized look of screen-printed posters, early video games, and pop-art silk screening. The core operation is quantization: each channel is divided into N evenly-spaced levels (from 2 to 256), and every pixel value is snapped to the nearest level. Before quantization, an optional dither stage adds controlled noise — either a repeating 2×2 Bayer ordered pattern or an LFSR pseudo-random field — to break up the hard contour lines that quantization would otherwise produce.

Eight preset color palettes provide further creative control. When a palette is active, each quantized pixel is remapped to the nearest color in the palette's 8-entry lookup table using Euclidean distance in YUV space. This transforms the image from a merely posterized version of itself into a recolored interpretation using the palette's specific color vocabulary — warm earth tones, cool blues, neon, pastel, sepia, night-vision green, or high-contrast primaries.

The proc_amp chain (brightness, contrast, saturation) operates before quantization, allowing tonal shaping of the image before it is reduced to discrete levels. This ordering is significant: boosting contrast before posterizing increases the visual separation between quantized zones, while reducing saturation before posterizing with a colored palette lets the palette dominate the output's color identity.

---

## Background

### Posterization in Photography and Print

Posterization — the reduction of continuous tones to a small number of flat colors — was originally a darkroom technique involving successive high-contrast photographic copies. Each generation eliminated tonal gradations, producing large areas of uniform tone separated by hard edges. The term comes from poster printing, where limited ink colors required this tonal simplification. Andy Warhol's screen prints are perhaps the most famous artistic application, reducing photographic portraits to 3–4 flat color layers. Paintbox makes this reduction parametric: the Levels control selects from 2 to 256 quantization steps, spanning from brutal 1-bit binary to nearly imperceptible 8-bit reduction.

### Dithering: Ordered vs. Random

Quantization introduces contour artifacts — visible staircase edges where smooth gradients are snapped to discrete levels. Dithering mitigates this by adding controlled noise before quantization, dispersing the error across neighboring pixels. Ordered dithering uses a repeating Bayer matrix (here, 2×2 with threshold values 0, 2, 3, 1) that creates a deterministic, structured noise field with a recognizable cross-hatch pattern. Random dithering uses an LFSR pseudo-random source, producing a film-grain-like texture with no visible pattern but more noise energy overall. Ordered dither is computationally cheaper and produces cleaner results at low quantization levels; random dither is better at hiding contours in smooth gradients.

### Nearest-Match Palette Mapping

When a palette is active, each pixel's quantized YUV value is compared against all entries in the palette table, and the closest match by Euclidean distance is substituted. This is the same principle used in GIF compression, indexed-color display modes, and palette-based game consoles like the NES and Game Boy. The palette acts as a color dictionary — the image can only contain colors from the dictionary, so the visual result takes on the palette's character.

### The proc_amp Chain

proc_amp (processing amplifier) is the standard video signal conditioning stage: brightness offsets the entire signal, contrast scales the deviation from midpoint 512, and saturation scales the chrominance deviation. In Paintbox, the proc_amp operates before quantization and dithering, so its effect is to reshape the tonal distribution that the posterizer will then slice into discrete levels.

### LFSR Noise in Video Processing

The 16-bit Linear Feedback Shift Register provides a deterministic pseudo-random number sequence at pixel rate. In Paintbox, the LFSR output is scaled by the Dither amplitude control and added to each channel before quantization. The LFSR repeats with a period of $2^{16} - 1$ (65,535 values), but this repeat period is much larger than any visible structure in the output, making the effect perceptually random.


---

## Signal Flow

```
data_in ──────────────────────────────────────────────────────
│
├── Stage 1: proc_amp ─────────────────────────────────────
│   ├─ Y' = (Y − 512) × contrast/512 + 512 + (brightness − 512)×2
│   ├─ U' = (U − 512) × saturation/512 + 512
│   └─ V' = (V − 512) × saturation/512 + 512
│
├── Stage 2: Invert ───────────────────────────────────────
│   └─ If Invert on: Y' = 1023 − Y'
│
├── Stage 3: Dither ───────────────────────────────────────
│   ├─ Ordered on: Bayer 2×2 matrix × dither_amplitude
│   └─ Ordered off: LFSR16 × dither_amplitude
│
├── Stage 4: Posterize (shift-mask-shift) ─────────────────
│   ├─ levels = 2^(bits + 1), bits = reg(1)[9:7]
│   ├─ step = 1023 / (levels − 1)
│   ├─ Y = round(Y / step) × step
│   ├─ If not Y Only: U, V quantized identically
│   └─ Y Only on: chroma passes through unquantized
│
├── Stage 5: Palette Nearest-Match LUT ────────────────────
│   ├─ palette = reg(0)[9:7] → 0–7 (0 = off)
│   ├─ For each pixel: find nearest palette entry
│   └─ dist = (Y−Yp)² + (U−Up)² + (V−Vp)²
│
├── Stage 6: Mono ─────────────────────────────────────────
│   └─ If Mono on: U = V = 512
│
├── Interpolator (wet/dry mix, 4 clocks) ──────────────────
│   └─ lerp(delayed_input, processed, mix) per Y/U/V
│
└── Output Mux ────────────────────────────────────────────
    ├─ Bypass off → mixed output
    └─ Bypass on → delayed input
```

The proc_amp chain before quantization is the key to Paintbox's expressiveness. By adjusting the tonal distribution before it is sliced into levels, the artist controls where the quantization boundaries fall relative to the source material's content. High contrast pushes midtones toward the extremes, creating a more graphic, high-impact posterization. Low contrast compresses the tonal range, making all quantized levels similar in brightness for a flatter result.

The Y Only toggle is particularly useful with colored palettes — quantizing luma only preserves the source video's natural chrominance while applying the posterized tonal structure. This creates images with smooth color but stepped brightness, reminiscent of hand-painted animation cels where flat color fills are bounded by ink outlines.

---

## Parameter Reference

<img src={paintbox_control_panel} alt="Videomancer front panel with Paintbox loaded"/>
*Videomancer's front panel with Paintbox active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Palette selects one of eight color palette presets using the top 3 bits (9:7) of the register, giving 8 positions. Position 0 bypasses the palette LUT, outputting posterized values directly. Positions 1–7 activate presets: warm earth tones, cool blues, neon, pastel, sepia, night-vision green, and high-contrast primaries. When active, each pixel is remapped to the nearest palette entry by Euclidean distance in YUV space. The palette selection dramatically changes the image's color identity — the same posterized structure can look like a pop-art print, a vintage photograph, or a military night-vision display.

---

#### Knob 2 — Softness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Levels controls the number of posterization steps. The top 3 bits (9:7) select from 8 quantization depths: 2, 4, 8, 16, 32, 64, 128, or 256 levels. At 2 levels, the image is reduced to stark binary. At 4 levels, the classic screen-print look emerges with visible flat zones. At 16–32 levels, posterization is subtle, visible primarily in smooth gradients. At 256 levels, the effect is nearly invisible. The level count is always a power of two, ensuring even spacing across the 0–1023 range.

---

#### Knob 3 — Fill Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Dither controls the amplitude of noise added before quantization. At zero, no dither is applied and quantization produces hard contour edges. As Dither increases, noise amplitude grows, spreading quantization error across neighboring pixels. At moderate values (300–600), dither softens contour edges into a pleasant stippled texture. At high values (800–1023), the noise becomes visible as grain overlaying the posterized image. Dither interacts strongly with Levels — low levels with high dither produce dramatic stippled textures, while high levels with low dither produce smooth color reduction.

---

#### Knob 4 — Fill Bright
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Brightness offsets the luminance channel before quantization. At midpoint (512), no offset is applied. Below 512, the image is darkened — pushing more of the tonal range into lower quantization bins. Above 512, the image is brightened, shifting pixels into upper bins. At extremes, the entire image may collapse into a single quantization level. Brightness operates as a DC offset: `offset = (register − 512) × 2`.

---

#### Knob 5 — Border Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Contrast scales the luminance deviation from midpoint 512. At 512, gain is unity (1.0×). Below 512, contrast is reduced and the tonal range compresses toward mid-gray. Above 512, contrast is boosted — shadows darken and highlights brighten. The formula is `(Y − 512) × contrast/512 + 512`. High contrast before posterizing is the classic pop-art technique: it forces the image into a few strongly separated tonal zones.

---

#### Knob 6 — Border Color
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Saturation scales the chrominance deviation from neutral 512. At 512, color saturation is unity. Below 512, colors are desaturated toward monochrome — useful before palette mapping to let the palette's colors dominate. Above 512, saturation is boosted for vivid posterized colors. At zero, output is fully desaturated. Saturation operates independently on U and V: `U' = (U − 512) × saturation/512 + 512`.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Matte Mode A** | Off | On |
| **8 — Matte Mode B** | Off | On |
| **9 — Fill Mode** | Color | Invert |
| **10 — Matte Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles modify quantization behavior and output routing. Y Only limits quantization to luma, preserving natural chrominance. Ordered selects between structured Bayer dither and random LFSR dither. Mono forces desaturation after all processing. Invert flips luma polarity before quantization, changing which content falls into which bin. Bypass routes input directly to output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the dry (original) and wet (processed) signal using three parallel interpolators. At 0% the output is unmodified input. At 100% the output is fully posterized and palette-mapped. Intermediate values blend the processed look with the original — a 30–50% mix can suggest a poster-art quality without fully committing to flat color zones.

---

## Guided Exercises

These exercises progress from basic posterization through palette mapping to complex dithered compositions, exploring the interaction between tonal shaping and color quantization.

### Exercise 1: Pop-Art Posterization

<img src={paintbox_exercise1_result} alt="Pop-Art Posterization result"/>
*Pop-Art Posterization — simulated result across source images.*
**Source**: High-contrast portrait or face close-up with varied skin tones and a simple background.

**Objective**: Create a bold, screen-printed pop-art look using minimal quantization levels and high contrast.

1. **Set levels**: Levels to 4 levels (~30%). The image snaps to four tonal zones.
2. **Boost contrast**: Contrast to ~75%. Midtones are pushed toward extremes.
3. **No dither**: Dither at 0%. Hard contour edges emphasize the graphic look.
4. **Neutral brightness**: Brightness at ~50%.
5. **Neutral saturation**: Saturation at ~50%. Let native colors come through.
6. **Observe**: The portrait becomes a four-tone pop-art image with flat color zones and hard edges — reminiscent of Warhol's Marilyn prints.

**Key concepts**: Low quantization levels create bold flat zones, high contrast before posterizing forces separation between tonal areas, no dither preserves hard contour edges

---

### Exercise 2: Sepia Palette with Ordered Dither

<img src={paintbox_exercise2_result} alt="Sepia Palette with Ordered Dither result"/>
*Sepia Palette with Ordered Dither — simulated result across source images.*
**Source**: Landscape or architectural scene with smooth gradients — sky, water, distant hills.

**Objective**: Apply the sepia palette with ordered dither to create a vintage photographic look.

1. **Select sepia**: Palette to position 5 (~65%). The sepia palette activates.
2. **Moderate levels**: Levels to 8 levels (~40%). Enough steps for a smooth result.
3. **Add dither**: Dither to ~40%. Softens quantization contours.
4. **Ordered dither**: Toggle Ordered on. A structured halftone texture appears.
5. **Reduce saturation**: Saturation to ~25%. Source colors fade, letting sepia dominate.
6. **Observe**: The landscape takes on a warm, vintage character with cross-hatch dither texture in the gradients.

**Key concepts**: Palette selection recolors the entire image, reduced saturation before palette mapping lets the palette dominate, ordered dither creates structured halftone texture

---

### Exercise 3: Night Vision with Random Noise

<img src={paintbox_exercise3_result} alt="Night Vision with Random Noise result"/>
*Night Vision with Random Noise — simulated result across source images.*
**Source**: Any footage — indoor scene, outdoor, or abstract video.

**Objective**: Create a night-vision-style monochrome image with random dither grain and the green palette.

1. **Night vision palette**: Palette to position 6 (~80%). Green palette activates.
2. **High levels**: Levels to 32 levels (~65%). Smooth enough to look realistic.
3. **Random dither**: Toggle Ordered off. Set Dither to ~50%. LFSR noise adds grain.
4. **Boost contrast**: Contrast to ~65%. Night vision is high-contrast.
5. **Boost brightness**: Brightness to ~60%. Emulates light amplification.
6. **Observe**: The image is rendered in shades of green with noisy, surveillance-camera quality. Random dither simulates photon noise of real night vision systems.

**Key concepts**: Palette selection transforms the color identity, random dither simulates photon noise, brightness boost emulates light amplification

---


## Tips

- **Start with 4 levels**: Four tonal zones produce the most dramatic, recognizable posterization. Increase levels for subtlety.
- **Contrast is the secret weapon**: High contrast before posterizing creates bold, graphic separation between zones. Low contrast creates uniform, muted output.
- **Desaturate before palette mapping**: Reducing Saturation to 25–40% before activating a palette lets the palette's colors dominate rather than competing with the source video's native colors.
- **Ordered dither for print looks**: The 2×2 Bayer pattern produces a halftone-like texture similar to newspaper photo reproduction.
- **Random dither for film looks**: LFSR dither at moderate amplitude creates a photographic grain quality that softens contours organically.
- **Y Only for animation-cel style**: Posterized brightness with smooth color produces the flat-shaded look of traditional animation cels.
- **Invert remaps tonal zones**: Inverting before quantizing doesn't just negate the image — it changes which content falls into which quantized zone, often with surprising results.
- **Mix for subtlety**: At 40–60% mix, posterization affects texture and color without eliminating all tonal detail.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bayer matrix** | A repeating threshold matrix used in ordered dithering to distribute quantization error in a structured, deterministic pattern. Named after Bryce Bayer of Kodak. |
| **Dithering** | The deliberate addition of noise to a signal before quantization to reduce visible contouring artifacts by dispersing error across neighboring pixels. |
| **Euclidean distance** | The straight-line distance between two points in a multi-dimensional space, used here to find the nearest palette color in YUV space. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **Nearest-match** | A color reduction technique that maps each pixel to the closest available color in a predefined palette by minimizing distance in color space. |
| **Posterization** | The reduction of continuous tonal gradations to a limited number of discrete levels, producing flat color zones with hard boundary edges. |
| **Proc amp** | Processing amplifier; a gain-and-offset stage that applies contrast (multiplication) and brightness (addition) to a signal. |
| **Quantization** | The process of mapping a continuous or high-resolution signal to a smaller set of discrete values. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
