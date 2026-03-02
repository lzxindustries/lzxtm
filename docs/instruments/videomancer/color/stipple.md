---
draft: true
sidebar_position: 272
slug: /instruments/videomancer/stipple
title: "Stipple"
image: /img/instruments/videomancer/stipple/stipple_hero.png
description: "Every classic computer had a fixed palette — a small set of colors chosen by the hardware designers, often constrained by cost, memory, and the television standards of the era."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import stipple_hero from '/img/instruments/videomancer/stipple/stipple_hero.png';
import stipple_control_panel from '/img/instruments/videomancer/stipple/stipple_control_panel.png';
import stipple_exercise1_result from '/img/instruments/videomancer/stipple/stipple_exercise1_result.png';
import stipple_exercise2_result from '/img/instruments/videomancer/stipple/stipple_exercise2_result.png';
import stipple_exercise3_result from '/img/instruments/videomancer/stipple/stipple_exercise3_result.png';
import stipple_source1_kodim03 from '/img/instruments/videomancer/stipple/stipple_source1_kodim03.png';
import stipple_source2_kodim15 from '/img/instruments/videomancer/stipple/stipple_source2_kodim15.png';
import stipple_source3_peppers_512 from '/img/instruments/videomancer/stipple/stipple_source3_peppers_512.png';

# Stipple

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: stipple_source1_kodim03, after: stipple_hero },
    { label: "Kodim15", before: stipple_source2_kodim15, after: stipple_hero },
    { label: "Peppers", before: stipple_source3_peppers_512, after: stipple_hero },
  ]}
/>
*Stipple mapping live video through eight classic computing palettes with ordered Bayer dithering to recreate the look of Game Boy, CGA, Macintosh, NES, EGA, C64, Amiga, and Amstrad CPC screens.*

---

## Overview

Every classic computer had a fixed palette — a small set of colors chosen by the hardware designers, often constrained by cost, memory, and the television standards of the era. Artists working within those constraints developed techniques to coax more apparent colors from fewer actual ones, using spatial patterns of alternating pixels to trick the eye into seeing intermediate shades. This optical mixing is called *dithering*, and it became the defining visual signature of an entire generation of digital imagery.

Stipple brings that process to live video. It takes a full-color input signal and reduces it to one of eight historically accurate palettes — from the Game Boy's four shades of green to the Amstrad CPC's saturated 27-color gamut. Before quantization, an ordered Bayer dither matrix adds a spatially structured offset to each pixel, pushing values across palette boundaries in a regular pattern that simulates additional tonal levels. The name comes from the printmaking technique of *stippling* — creating tone through dots rather than continuous ink.

The program pairs palette quantization with brightness, contrast, and saturation controls, scanline darkening for CRT authenticity, pixel doubling for blocky low-resolution aesthetics, and a selectable dither matrix size ranging from no dithering through 2×2, 4×4, and full 8×8 Bayer patterns. At subtle settings, Stipple adds a gentle retro patina. At full strength, it transforms any video source into a faithful recreation of a bygone computing era.

---

## Background

### Ordered Dithering and the Bayer Matrix

Ordered dithering uses a fixed threshold matrix tiled across the image. For each pixel, the corresponding matrix value is added to or subtracted from the signal before quantization. The most common matrix is the **Bayer matrix**, named after Bryce Bayer of Kodak. An 8×8 Bayer matrix contains 64 unique threshold values arranged so that, when tiled, they produce an even stipple pattern with no visible clustering. Smaller 4×4 and 2×2 subsets produce coarser patterns with fewer intermediate tones. Stipple's Dither Size control selects among these: no dithering, 2×2, 4×4, or the full 8×8 matrix. The Dither Amt control scales how aggressively the threshold offsets push pixel values across palette boundaries.

### Platform Color Palettes

Each of Stipple's eight palettes reproduces the exact color set of a real computing platform. The Game Boy (1989) had four shades of olive green displayed on a dot-matrix LCD. CGA Mode 4 (1981) offered black, magenta, cyan, and white — the default high-intensity palette on IBM PCs. The original Macintosh (1984) was strictly monochrome: black and white. The NES (1983) used a master palette of 54 colors, of which games typically selected 16. EGA (1984) offered 16 colors from a 64-color space. The Commodore 64 (1982) had a fixed 16-color palette. The Amiga OCS (1985) could display up to 4096 colors but typically used 16 or 32 per screen. The Amstrad CPC (1984) selected 16 from its 27-color hardware palette. Each palette in Stipple contains 16 entries sorted by BT.601 luminance; smaller palettes repeat entries to fill the 16 slots.

### Quantization and Palette Matching

Stipple quantizes by dividing the 10-bit luminance range into 16 equal bands of 64 levels each. The brightness-adjusted, dithered Y value is divided by 64 to produce a palette index (0–15), which looks up the corresponding entry in the selected platform's color table. Because the palettes are pre-converted from RGB to YUV at synthesis time, the lookup is a direct constant fetch — no distance calculation or search is needed. The dither pattern creates transitions between adjacent palette entries, simulating more tonal levels than the palette actually contains.

### Scanlines and Pixel Doubling

CRT monitors displayed interlaced fields with visible gaps between scan lines. Many classic computers also operated at resolutions far below the CRT's native capability, producing visibly blocky pixels. Stipple's Scanlines toggle darkens every other line to 50% brightness, recreating the horizontal stripe pattern of a CRT. Pixel Dbl holds each palette-quantized pixel for two horizontal samples, halving the effective horizontal resolution and producing the chunky, square-pixel look of low-resolution display modes.

### Shift-Add Multiplication in Hardware

The FPGA has no hardware multiplier for arbitrary values. Stipple implements contrast scaling using **shift-add multiplication** — the contrast register's top three bits select which power-of-two shifts of the input are summed. This approximation is fast and resource-efficient, producing 8 discrete contrast levels from fully dark to nearly double gain. The same technique scales the dither offset by the Dither Amt parameter.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1a. Contrast          (shift-add multiply, 3-bit approx)
│   ├─ 1b. Brightness + Clamp + Invert
│   ├─ 2a. Bayer/Noise Lookup (none / 2×2 / 4×4 / 8×8)
│   ├─ 2b. Dither Offset + Quantize (y / 64 → palette index)
│   ├─ 3.  Palette Lookup    (8 × 16 entries → YUV)
│   │      + Saturation      (UV scaling: 0% / 50% / 100% / 150%)
│   ├─ 4.  Pixel Double      (hold every 2 px)
│   │      + Scanlines       (Y × 50% on odd lines)
│   └─ *.  Interpolator Mix  (dry/wet crossfade, 4 clk)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 3.  Palette Lookup    (palette entry UV)
│   │      + Saturation      (UV scaled by top 2 bits of pot)
│   ├─ 4.  Pixel Double + Scanlines passthrough
│   └─ *.  Interpolator Mix  (4 clk each)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delayed by 10 clocks (pass-through)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical path runs through luminance: contrast → brightness → dither → quantize → palette lookup. Chrominance bypasses all stages before palette lookup — the palette entries provide both the Y and UV output. Saturation acts on the palette's own UV values, not the input chroma, so it controls how colorful the chosen platform's palette appears. The dither offset is computed as a shift-add product of the centered Bayer value (−32 to +31) and the Dither Amt register's top three bits, giving coarse but efficient analog-style control over dither intensity.

---

## Parameter Reference

<img src={stipple_control_panel} alt="Videomancer front panel with Stipple loaded"/>
*Videomancer's front panel with Stipple active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Palette
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Selects one of eight retro computing palettes. Each palette contains 16 color entries sorted by BT.601 luminance. Palette 0 (Game Boy) maps the entire image to four shades of olive green. Palette 1 (CGA) uses black, magenta, cyan, and white. Palette 2 (Macintosh) is pure black and white — maximum contrast, no gray. Palettes 3–7 (NES, EGA, C64, Amiga, CPC) each provide 16 distinct colors spanning the full luminance range.

---

#### Knob 2 — Dither Size
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 1 |

Controls the spatial resolution of the dither pattern. At position 0, dithering is disabled — quantization produces hard, unbanded palette transitions. Position 1 uses a 2×2 sub-matrix (4 threshold levels). Position 2 uses 4×4 (16 levels). Position 3 uses the full 8×8 Bayer matrix (64 levels), producing the finest stipple pattern with the most simulated intermediate tones. Larger matrices create more convincing tonal gradients but with a finer, more visible dot pattern.

---

#### Knob 3 — Dither Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scales the dither threshold offset amplitude. At zero, even with a dither matrix selected, the offset is suppressed and quantization is hard. As the amount increases, the Bayer thresholds push more aggressively, creating wider transition zones between palette colors. Very high values can cause the dither pattern to dominate, producing a noisy, stippled texture across the entire image.

---

#### Knob 4 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

DC brightness offset applied after contrast scaling. The register value is centered at 512 (no change); values below darken, values above brighten. Because brightness is applied *before* dithering and quantization, it shifts which palette entries the image maps to — increasing brightness pushes more of the image into lighter palette slots.

---

#### Knob 5 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Gain applied to the input luminance via shift-add multiplication. The top three bits of the register select which power-of-two components are summed, producing 8 discrete contrast levels. At zero, the image is flat black. At midpoint, roughly unity gain. At maximum, high contrast that compresses the tonal range into fewer palette entries, creating bolder, more graphic results.

---

#### Knob 6 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the saturation of the palette's own chroma values. The top two bits select four discrete levels: fully desaturated (grayscale palette), 50% saturation, 100% (native palette colors), and 150% (oversaturated). This does not affect the input chroma — it scales the UV components stored in the palette ROM. Desaturating converts any palette to a grayscale version of itself.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pixel Dbl** | Off | On |
| **8 — Scanlines** | Off | On |
| **9 — Dither Mode** | Bayer | Noise |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent binary options. Pixel Dbl and Scanlines together recreate the look of low-resolution CRT displays. Dither Mode selects between structured Bayer patterns and random LFSR noise. Invert reverses the luminance before all subsequent processing. Bypass routes the input directly to output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (unprocessed) and wet (palette-quantized) signal via the interpolator. At 0%, the output is the original input. At 100%, the output is fully processed. Intermediate values blend the two, which can produce interesting translucent overlay effects where the retro palette sits ghosted over the original image.

---

## Guided Exercises

These exercises progress from basic palette selection through dither exploration to full retro display emulation. Each builds on the previous, gradually engaging more of the processing chain.

### Exercise 1: Platform Showcase

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: stipple_source1_kodim03, after: stipple_exercise1_result },
    { label: "Kodim15", before: stipple_source2_kodim15, after: stipple_exercise1_result },
    { label: "Peppers", before: stipple_source3_peppers_512, after: stipple_exercise1_result },
  ]}
/>
*Platform Showcase — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a range of colors and brightness — faces, landscapes, or colorful objects work well.

**Objective**: Explore the eight palettes and understand how each platform's color limitations shape the image.

1. **Game Boy**: Set Palette to position 0. The image collapses to four shades of olive green. Note how all color information is lost.
2. **CGA**: Turn to position 1. Four colors — black, magenta, cyan, white. Stark and graphic.
3. **Macintosh**: Position 2. Pure black and white with no gray — the harshest quantization.
4. **NES through CPC**: Sweep slowly through positions 3–7. Watch how the number and distribution of available colors changes the rendering.
5. **Add dithering**: Set Dither Size to position 3 (8×8) and Dither Amt to ~50%. Observe how the stipple pattern creates the illusion of intermediate colors within each palette.

**Key concepts**: Each palette reproduces a real computing platform's color set, fewer colors produce more drastic image simplification, dithering simulates intermediate tones

---

### Exercise 2: Dither Textures

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: stipple_source1_kodim03, after: stipple_exercise2_result },
    { label: "Kodim15", before: stipple_source2_kodim15, after: stipple_exercise2_result },
    { label: "Peppers", before: stipple_source3_peppers_512, after: stipple_exercise2_result },
  ]}
/>
*Dither Textures — simulated result across source images.*
**Source**: Footage with gradual tonal transitions — skies, skin tones, or gradient test patterns.

**Objective**: Explore how dither matrix size and amount control the stipple pattern.

1. **No dithering**: Set Dither Size to 0 and observe the hard palette boundaries — flat bands of uniform color with harsh edges.
2. **2×2 dither**: Set Dither Size to 1. A coarse checkerboard pattern appears in transition zones.
3. **4×4 dither**: Position 2. The stipple becomes finer and more evenly distributed.
4. **8×8 dither**: Position 3. The finest pattern with the most tonal gradations.
5. **Dither amount**: With 8×8 selected, sweep Dither Amt from 0% to 100%. Watch the transition zones widen from sharp edges to broad stippled gradients.
6. **Noise mode**: Toggle Dither Mode to Noise. The geometric Bayer pattern is replaced by random grain. Compare the two textures.

**Key concepts**: Larger matrices produce finer stipple with more intermediate tones, dither amount controls the transition zone width, Bayer produces structured patterns while LFSR noise produces organic grain

---

### Exercise 3: CRT Emulation

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: stipple_source1_kodim03, after: stipple_exercise3_result },
    { label: "Kodim15", before: stipple_source2_kodim15, after: stipple_exercise3_result },
    { label: "Peppers", before: stipple_source3_peppers_512, after: stipple_exercise3_result },
  ]}
/>
*CRT Emulation — simulated result across source images.*
**Source**: Any footage, especially retro game footage or graphics.

**Objective**: Combine pixel doubling, scanlines, and dithering for authentic retro display emulation.

1. **Select C64 palette**: Set Palette to 5.
2. **Enable pixel doubling**: Toggle Pixel Dbl on. The image becomes blocky with doubled horizontal pixels.
3. **Enable scanlines**: Toggle Scanlines on. Every other line darkens, revealing the scan line structure.
4. **Add dithering**: Set Dither Size to 2 (4×4) and Dither Amt to ~40%. The dither pattern interacts with pixel doubling to create authentic-looking blocks.
5. **Adjust contrast**: Sweep Contrast to find the sweet spot where the C64 palette compresses into bold, graphic blocks.
6. **Desaturate**: Turn Saturation to the lowest position. The C64 palette becomes grayscale — like watching a color broadcast on a black-and-white monitor.
7. **Mix blend**: Slowly lower the Mix fader to superimpose the original over the retro version.

**Key concepts**: Pixel doubling halves horizontal resolution, scanlines simulate CRT phosphor gaps, combining all effects recreates the look of classic hardware

---


## Tips

- **Start with the palette**: Choose your target aesthetic first — the palette defines the color universe. Everything else is refinement.
- **Dither Size 3 for realism**: The full 8×8 Bayer matrix produces the most convincing tonal gradations. Use smaller sizes for deliberately crude, lo-fi effects.
- **Macintosh mode for graphic design**: Palette 2 (pure B&W) with high-contrast settings produces bold, posterized black-and-white imagery ideal for graphic overlays.
- **Scanlines need Pixel Dbl**: Scanline darkening alone can look like horizontal banding. Combined with pixel doubling, it becomes an authentic CRT emulation.
- **Invert changes the story**: Inverting before palette mapping flips the tonal assignment — light subjects become dark palette entries. This can dramatically change the character of the palette.
- **Mix for overlay effects**: At 30–60% Mix, the palette-quantized image sits as a translucent color wash over the original — useful for subtle retro tinting without full commitment.
- **Saturation at 0% for B&W vintage**: Desaturating any palette produces a grayscale version, even palettes like C64 that are famous for their color. This creates unique monochrome textures.
- **Feedback loops**: Routing Stipple's output back to its input creates recursive palette quantization — each pass simplifies the image further toward the palette's most dominant entries.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bayer Matrix** | A fixed threshold pattern (typically 4×4 or 8×8) used in ordered dithering to create evenly distributed dot patterns that simulate intermediate tones. |
| **BT.601** | ITU-R Recommendation BT.601; the color matrix standard used for standard-definition video YUV encoding throughout the Videomancer pipeline. |
| **CGA** | Color Graphics Adapter (1981); IBM's first color display standard for PCs, offering 4-color modes. |
| **CRT** | Cathode Ray Tube; the display technology used by classic computers and televisions, characterized by visible scan lines and phosphor glow. |
| **Dithering** | Adding a small noise or threshold pattern before quantization to break up banding and simulate additional tonal levels with a limited palette. |
| **EGA** | Enhanced Graphics Adapter (1984); IBM's second-generation color display standard, offering 16 colors from a 64-color space. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **LFSR** | Linear Feedback Shift Register; a circuit that generates a pseudo-random bit sequence, used here for noise-mode dithering. |
| **Luminance** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Palette** | A fixed set of colors from which all pixel values must be drawn; the defining constraint of classic computing displays. |
| **Quantization** | Mapping a continuous range of values to a smaller set of discrete levels, producing visible steps in gradients. |
| **RGB9** | A compact color representation using 3 bits per channel (red, green, blue), encoding 512 possible colors. Used internally to store palette definitions. |
| **Shift-Add Multiplication** | Approximating multiplication using bit shifts and additions, avoiding the need for a hardware multiplier. |
| **Stippling** | A drawing technique that creates tonal gradation using patterns of small dots rather than continuous shading. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
