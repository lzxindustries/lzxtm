---
draft: true
sidebar_position: 34
slug: /instruments/videomancer/calico
title: "Calico"
image: /img/instruments/videomancer/calico/calico_hero_s1.png
description: "The Commodore Amiga's HAM (Hold-And-Modify) display mode was one of the most ingenious compromises in the history of computer graphics."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import calico_control_panel from '/img/instruments/videomancer/calico/calico_control_panel.png';
import calico_source1_fruit from '/img/instruments/videomancer/calico/calico_source1_fruit.png';
import calico_source2_dog from '/img/instruments/videomancer/calico/calico_source2_dog.png';
import calico_source3_turtle from '/img/instruments/videomancer/calico/calico_source3_turtle.png';
import calico_source4_pattern from '/img/instruments/videomancer/calico/calico_source4_pattern.png';
import calico_source5_girl from '/img/instruments/videomancer/calico/calico_source5_girl.png';
import calico_source6_wood from '/img/instruments/videomancer/calico/calico_source6_wood.png';
import calico_hero_s1 from '/img/instruments/videomancer/calico/calico_hero_s1.png';
import calico_hero_s2 from '/img/instruments/videomancer/calico/calico_hero_s2.png';
import calico_hero_s3 from '/img/instruments/videomancer/calico/calico_hero_s3.png';
import calico_hero_s4 from '/img/instruments/videomancer/calico/calico_hero_s4.png';
import calico_hero_s5 from '/img/instruments/videomancer/calico/calico_hero_s5.png';
import calico_hero_s6 from '/img/instruments/videomancer/calico/calico_hero_s6.png';
import calico_ex1_s1 from '/img/instruments/videomancer/calico/calico_ex1_s1.png';
import calico_ex1_s2 from '/img/instruments/videomancer/calico/calico_ex1_s2.png';
import calico_ex1_s3 from '/img/instruments/videomancer/calico/calico_ex1_s3.png';
import calico_ex1_s4 from '/img/instruments/videomancer/calico/calico_ex1_s4.png';
import calico_ex1_s5 from '/img/instruments/videomancer/calico/calico_ex1_s5.png';
import calico_ex1_s6 from '/img/instruments/videomancer/calico/calico_ex1_s6.png';
import calico_ex2_s1 from '/img/instruments/videomancer/calico/calico_ex2_s1.png';
import calico_ex2_s2 from '/img/instruments/videomancer/calico/calico_ex2_s2.png';
import calico_ex2_s3 from '/img/instruments/videomancer/calico/calico_ex2_s3.png';
import calico_ex2_s4 from '/img/instruments/videomancer/calico/calico_ex2_s4.png';
import calico_ex2_s5 from '/img/instruments/videomancer/calico/calico_ex2_s5.png';
import calico_ex2_s6 from '/img/instruments/videomancer/calico/calico_ex2_s6.png';
import calico_ex3_s1 from '/img/instruments/videomancer/calico/calico_ex3_s1.png';
import calico_ex3_s2 from '/img/instruments/videomancer/calico/calico_ex3_s2.png';
import calico_ex3_s3 from '/img/instruments/videomancer/calico/calico_ex3_s3.png';
import calico_ex3_s4 from '/img/instruments/videomancer/calico/calico_ex3_s4.png';
import calico_ex3_s5 from '/img/instruments/videomancer/calico/calico_ex3_s5.png';
import calico_ex3_s6 from '/img/instruments/videomancer/calico/calico_ex3_s6.png';

# Calico

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: calico_source1_fruit, after: calico_hero_s1 },
    { label: "Dog", before: calico_source2_dog, after: calico_hero_s2 },
    { label: "Turtle", before: calico_source3_turtle, after: calico_hero_s3 },
    { label: "Pattern", before: calico_source4_pattern, after: calico_hero_s4 },
    { label: "Girl", before: calico_source5_girl, after: calico_hero_s5 },
    { label: "Wood", before: calico_source6_wood, after: calico_hero_s6 },
  ]}
/>
*Calico rendering a portrait through Amiga HAM6 encoding with the Workbench palette, producing characteristic horizontal color fringing at every sharp edge.*

---

## Overview

The Commodore Amiga's HAM (Hold-And-Modify) display mode was one of the most ingenious compromises in the history of computer graphics. On hardware that normally supported 32 or 64 simultaneous colors, HAM could display all 4,096 colors in the 12-bit RGB space — but at a cost. Each pixel was encoded not as an independent color, but as an *operation* on the previous pixel: either set to one of 16 base palette colors, or modify a single RGB channel of the preceding pixel's output. The result was beautiful photographic images marred by a telltale horizontal color fringe at every sharp edge, as the encoder changed one channel at a time to reach the target color.

Calico faithfully reproduces this encoding constraint on live video. The input is converted to RGB, quantized to HAM6 (4-bit) or HAM8 (6-bit) precision, and then processed through the same left-to-right (or right-to-left) per-scanline state machine that the original Amiga hardware used. Four era-accurate 16-color base palettes deliver different visual flavors — the stark primaries of Workbench 1.x, the perceptually-spaced grays of DigiView Gold, broadcast-safe NTSC tones, and the soft pastels of Deluxe Paint. The name references the calico cat's distinctive patches of color — irregular, adjacent, never quite blending — much like the way HAM mode patches together color one channel at a time.

At full fringe strength with HAM6 and the lowest resolution setting, the output is immediately recognizable as an authentic 1987 digitized Amiga photo. Dialing down fringe strength or switching to HAM8 cleans the image progressively, revealing a spectrum from nostalgic artifact to subtle palette-limited aesthetic.

---

## Quick Start

1. **Palette choice shapes fringe pattern**: Choose a palette whose colors are well-distributed relative to your source material. A palette with colors close to the source produces more SET operations and fewer fringes; a distant palette forces more MODIFY operations and wider fringes.
2. **Resolution amplifies fringe width**: Lower resolution means fewer pixels per scanline for the HAM encoder to work with, so color transitions take proportionally more of the visible image. 80px mode turns fringes into broad color bands.
3. **HAM6 for drama, HAM8 for subtlety**: HAM6's 4-bit precision produces the characteristic 1987 Amiga look with bold, visible fringes. HAM8's 6-bit precision is cleaner — visually interesting but less immediately recognizable as HAM.

---

## Background

### The Amiga's Color Problem

When Commodore released the Amiga 1000 in 1985, its custom chipset (OCS) could address 4,096 colors from a 12-bit RGB palette — but in standard display modes, only 32 (lo-res) or 16 (hi-res) of those colors could appear on screen simultaneously. This was a painful limitation for displaying photographic images, which need thousands of tonal variations. HAM mode was the engineers' solution: a display mode that could show all 4,096 colors at once, by encoding each pixel as a *relationship* to the one before it rather than as an independent color value. The Amiga was the first personal computer to treat video as a first-class creative medium, and HAM mode was the technique that made digitized photographs possible on affordable hardware.

### How Hold-And-Modify Works

HAM mode encodes each pixel using a 2-bit operation code and a 4-bit data field (6 bits total per pixel). The four operations are: **SET** (use one of 16 base palette colors, all three RGB channels change instantly), **MODIFY RED** (replace only the red channel with the 4-bit data, hold green and blue from the previous pixel), **MODIFY GREEN** (replace green, hold red and blue), and **MODIFY BLUE** (replace blue, hold red and green). The encoder processes each scanline left-to-right, maintaining a running "current color" register that starts at palette color 0 (the background).

When the next target pixel is close in color to the current state, a single MODIFY operation is often sufficient — change the channel with the largest error. When the target is far from the current state — a sharp edge between, say, blue sky and an orange face — the encoder may need two or three consecutive MODIFY operations to reach the target, producing a visible trail of intermediate colors. This is the **HAM fringe**: a horizontal smear of color that is as recognizable to anyone who owned an Amiga as the sound of a floppy drive.

### Color Fringing as Visual Fingerprint

The HAM fringe was not random noise or a rendering bug — it was a *deterministic artifact* of the encoding algorithm. The fringe always ran horizontally (because the encoder processed left-to-right), always appeared at color boundaries, and its width depended on how many channels needed to change. A transition from pure red to pure blue required changing two channels (reduce red, increase blue), taking two pixels of intermediate color. A transition from white to black required all three channels, taking three pixels. This gave HAM images their characteristic look: smooth gradients rendered beautifully, but every sharp edge trailed a rainbow of transitional colors.

### Genlock Compositing

The Amiga's video output was designed to be genlocked (synchronized) to external video sources. With a genlock adapter like the SuperGen by Digital Creations or Commodore's own A2300, HAM-rendered graphics could be overlaid on live video — the first affordable video titling and graphics overlay system. Palette color 0 acted as a transparency key: any pixel set to the background color became transparent, revealing the live video beneath. This capability made the Amiga the workhorse of 1990s public access television, wedding videography, corporate presentations, and low-budget cable programming worldwide. Calico's Genlock toggle recreates this transparency behavior.

### Bayer Dithering for Smoother Quantization

Before the HAM encoder quantizes each pixel to 4-bit or 6-bit precision, an optional **ordered dithering** step adds a small structured offset from a 4×4 Bayer matrix. This pushes pixel values across quantization boundaries in a regular pattern, creating the illusion of additional tonal levels when viewed at normal distance. Bayer dithering was a standard technique in early computer graphics and printing — the same matrix pattern used by newspaper halftone screens and the Apple Macintosh's original 1-bit display. Combined with HAM's already-limited palette, dithering trades sharp quantization boundaries for a fine cross-hatch texture.


---

## Signal Flow

YUV → RGB Conversion → Resolution → HAM Encode → RGB → YUV Back-Conversion → Genlock Key → Output Register

```
Input Video (YUV 4:4:4 30-bit)
│
├── Stage 1: YUV → RGB Conversion ─────────────────────────────
│   │
│   ├─ Shift-add approximation (CORDIC-free)
│   ├─ R = Y + V' + (V'>>1) - (V'>>3)
│   ├─ G = Y - (U'>>2) - (U'>>5) - (V'>>1) - (V'>>3)
│   └─ B = Y + U' + (U'>>1) + (U'>>2)
│       where U' = U - 512, V' = V - 512
│       Output: 4-bit RGB (HAM6) and 6-bit RGB (HAM8)
│
├── Stage 2: Resolution Sample-and-Hold + Dither ───────────────
│   │
│   ├─ Sample-and-hold at selected period (2/4/5/8 clocks)
│   │   320px / 160px / 128px / 80px effective resolution
│   ├─ Optional 4×4 Bayer ordered dither (±8 counts)
│   └─ Clamped quantized RGB held until next sample
│
├── Stage 3: HAM Encode (per-scanline state machine) ───────────
│   │
│   ├─ Current color register: reset to palette[0] at scanline start
│   ├─ For each pixel:
│   │   ├─ Find nearest palette color (Manhattan RGB distance × 16 entries)
│   │   ├─ Calculate per-channel error vs current state
│   │   ├─ If palette_distance < modify_distance → SET (use palette entry)
│   │   └─ If modify closer → MODIFY channel with largest error
│   │       (hold other two channels from previous pixel)
│   └─ Fringe Dir toggle reverses scan direction (L-to-R / R-to-L)
│
├── Stage 4: RGB → YUV Back-Conversion ─────────────────────────
│   │
│   ├─ Expand 4-bit/6-bit → 10-bit (bit replication)
│   ├─ Y = (R>>2) + (R>>5) + (G>>1) + (G>>4) + (B>>3) + (B>>6)
│   ├─ U = (B - Y)>>1 + 512
│   └─ V = (R - Y) - ((R - Y)>>3) + 512
│
├── Stage 5: Genlock Key + Scanline Overlay ────────────────────
│   │
│   ├─ If Genlock on and HAM output matches palette[0]:
│   │   pass through original input (transparent)
│   └─ If Scanlines on: odd lines darkened by 50%
│
├── Stage 6: Output Register ───────────────────────────────────
│
└── Mix (3× interpolator_u) ────────────────────────────────────
    └─ Wet/dry crossfade: original input ↔ processed output
```

The heart of Calico is the Stage 3 HAM encoder — a per-scanline state machine that decides, for each pixel, whether to SET the running color to a palette entry or MODIFY a single RGB channel. This decision cascade creates the characteristic horizontal fringe: when the encoder encounters a sharp color boundary, it can only change one channel per pixel, producing a trail of intermediate colors as it converges on the target. The Fringe Dir toggle reverses this scan direction, shifting fringes from leading to trailing edges. Everything else in the pipeline — the color conversion, resolution downsampling, dithering, and genlock — serves to prepare input for and post-process the output of this central HAM encoding step.

---

## Parameter Reference

<img src={calico_control_panel} alt="Videomancer front panel with Calico loaded"/>
*Videomancer's front panel with Calico active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Palette
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Selects one of four 16-color base palettes used for SET operations in the HAM encoder. **Workbench** delivers the stark blue-white-black-orange primaries of Amiga Workbench 1.x — the palette most users associate with the Amiga's identity. **DigiView** uses perceptually-spaced grays plus saturated primaries, matching how DigiView Gold optimized its capture palette for photographic content. **NTSC** provides broadcast-legal colors suitable for video output. **DPaint** offers the soft pastel tones associated with the Deluxe Paint era. The palette choice fundamentally changes where SET operations occur versus where the encoder must MODIFY, reshaping the fringe pattern across the entire image.

---

#### Knob 2 — Fringe Str
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

At 0%, the encoder bypasses the hold-and-modify logic and performs direct palette quantization only, producing a clean but limited-palette image. As fringe strength increases, the HAM constraint becomes more active, and the encoder increasingly relies on MODIFY operations that change only one channel at a time. At 100%, the full HAM encoding algorithm runs with maximum fidelity to the original Amiga behavior, including maximum-width color fringes at every sharp color transition. Internally, controls the intensity of the HAM encoding constraint — how strongly the characteristic color fringing is applied.

---

#### Knob 3 — Resolution
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Sets the effective horizontal resolution via sample-and-hold downsampling. **320px** matches the standard Amiga lo-res display — pixels are sampled every 2 clocks. **160px** halves that again, producing wider pixels and more pronounced HAM fringing per visible color block — the look of early DigiView Gold captures that traded resolution for smoother color transitions. **128px** creates a painterly, chunky appearance. **80px** reduces the image to extremely coarse color bands, turning the HAM fringe into broad stripes of transitional color.

---

#### Knob 4 — BG Hue
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |
| Suffix | deg |

Adjusts the hue of the genlock background key color. When Genlock mode is active, pixels matching palette entry 0 become transparent, revealing the original input video beneath. This control rotates the hue of that key color, allowing you to choose which base color acts as the transparency key — useful for keying on specific background colors in the source material rather than defaulting to black.

---

#### Knob 5 — Pal Sat
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the saturation of all 16 colors in the active base palette. At 50%, the palette colors are at their nominal saturation as designed. At 0%, all palette entries collapse toward their luminance-equivalent grays, producing a monochrome HAM image where fringing appears only as brightness stepping. At 100%, palette colors are pushed to maximum saturation, creating vivid primary blocks wherever the encoder chooses SET over MODIFY.

---

#### Knob 6 — Luma Quant
| Property | Value |
|----------|-------|
| Range | 2bit – 6bit |
| Default | 2bit |
| Suffix | bit |

At minimum, luminance is quantized to 2-bit precision (4 levels), creating dramatic posterization of brightness values. At maximum, luminance is quantized to 6-bit precision (64 levels), which produces smooth tonal gradation nearly indistinguishable from the full 10-bit range. This parameter compounds with the HAM encoder's inherent color quantization to create a layered retro aesthetic — coarse luma quantization plus HAM fringing replicates the look of heavily dithered Amiga screenshots. Internally, controls the luminance quantization depth applied to the Y channel of the output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — HAM Mode** | HAM6 | HAM8 |
| **8 — Genlock** | Off | On |
| **9 — Fringe Dir** | L-to-R | R-to-L |
| **10 — Scanlines** | Off | On |
| **11 — Dither** | Off | On |

Switches 7–11 control five independent display options. HAM Mode sets the color precision (HAM6 vs HAM8). Genlock enables transparency keying. Fringe Dir reverses the encoding direction. Scanlines adds CRT-style line darkening. Dither enables ordered dithering before quantization. Unlike many programs, there is no dedicated Bypass toggle — the Mix fader at 0% serves as the bypass mechanism, crossfading between the processed and original signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original input video and the HAM-processed output. At 0%, the output is the unmodified input signal — functionally equivalent to bypass. At 100%, the output is fully HAM-encoded. Intermediate values blend the HAM fringing and palette quantization with the clean original, creating a partial retro overlay effect. Because Calico has no dedicated Bypass toggle, this fader is the primary mechanism for A/B comparison.





---

## Guided Exercises

These exercises introduce the HAM encoding constraint progressively, starting with palette selection and building to full genlock compositing. Each exercise engages more of the processing chain and reveals different aspects of the Hold-And-Modify algorithm.

### Exercise 1: Palette Character

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: calico_source1_fruit, after: calico_ex1_s1 },
    { label: "Dog", before: calico_source2_dog, after: calico_ex1_s2 },
    { label: "Turtle", before: calico_source3_turtle, after: calico_ex1_s3 },
    { label: "Pattern", before: calico_source4_pattern, after: calico_ex1_s4 },
    { label: "Girl", before: calico_source5_girl, after: calico_ex1_s5 },
    { label: "Wood", before: calico_source6_wood, after: calico_ex1_s6 },
  ]}
/>
*Palette Character — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and varied colors — faces, clothing, backgrounds.

**What You'll Create**: Explore how the four base palettes change the balance between SET and MODIFY operations, reshaping the fringe pattern.

1. **Workbench primaries**: Set Palette to Workbench. Note the stark blue, orange, and white blocks where the encoder uses SET — these correspond to the iconic Amiga desktop colors.
2. **DigiView photo mode**: Switch to DigiView. The gray ramp in this palette produces smoother tonal transitions — this was the palette optimized for digitized photographs.
3. **Broadcast-safe**: Switch to NTSC. The muted, legal-range colors produce a more subdued image suitable for broadcast work.
4. **Soft pastels**: Switch to DPaint. The pastel palette creates a painterly, illustrative quality — reminiscent of DPaint artwork.
5. **Resolution**: Try each palette at 320px, then at 160px. Notice how lower resolution exaggerates the fringe width and makes palette choice more dramatically visible.

**Key concepts**: Different palettes create different SET/MODIFY patterns, palette colors that are close to the source content produce fewer fringes, resolution affects fringe visibility

---

### Exercise 2: Fringing and Direction

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: calico_source1_fruit, after: calico_ex2_s1 },
    { label: "Dog", before: calico_source2_dog, after: calico_ex2_s2 },
    { label: "Turtle", before: calico_source3_turtle, after: calico_ex2_s3 },
    { label: "Pattern", before: calico_source4_pattern, after: calico_ex2_s4 },
    { label: "Girl", before: calico_source5_girl, after: calico_ex2_s5 },
    { label: "Wood", before: calico_source6_wood, after: calico_ex2_s6 },
  ]}
/>
*Fringing and Direction — simulated result across source images.*
**Source**: High-contrast footage with strong vertical edges — text overlays, architectural details, or graphic patterns.

**What You'll Create**: Demonstrate the HAM fringe artifact and explore how direction and strength controls shape it.

1. **Maximum fringe**: Set Fringe Str to 100% with HAM6 and 160px resolution. Notice the horizontal color smear trailing to the right of every vertical edge.
2. **Reverse direction**: Toggle Fringe Dir to R-to-L. The fringes now trail to the left — the visual weight of edges shifts.
3. **Reduce fringe**: Slowly lower Fringe Str from 100% to 0%. Watch the fringes compress and eventually disappear as the encoder shifts from MODIFY operations to direct palette matching.
4. **HAM8 comparison**: Toggle HAM Mode to HAM8. The fringes become much subtler — the 6-bit per channel precision allows the encoder to approximate colors more closely with each MODIFY step.
5. **Dither smoothing**: Enable Dither. The Bayer pattern softens the quantization steps visible within the fringe transitions.

**Key concepts**: HAM fringe is deterministic and horizontal, fringe width depends on color distance, HAM8 reduces fringe visibility vs. HAM6, dithering smooths quantization boundaries

---

### Exercise 3: Genlock Compositing

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: calico_source1_fruit, after: calico_ex3_s1 },
    { label: "Dog", before: calico_source2_dog, after: calico_ex3_s2 },
    { label: "Turtle", before: calico_source3_turtle, after: calico_ex3_s3 },
    { label: "Pattern", before: calico_source4_pattern, after: calico_ex3_s4 },
    { label: "Girl", before: calico_source5_girl, after: calico_ex3_s5 },
    { label: "Wood", before: calico_source6_wood, after: calico_ex3_s6 },
  ]}
/>
*Genlock Compositing — simulated result across source images.*
**Source**: Footage with a solid-colored background region — a person against a dark backdrop, or any scene with a prominent area of near-black or near-solid color.

**What You'll Create**: Recreate the classic Amiga genlock overlay effect — HAM graphics floating over live video.

1. **Prepare the HAM image**: Set Palette to Workbench, Resolution to 320px, Fringe Str to ~75%, HAM6 mode. Observe the fully processed HAM output.
2. **Enable genlock**: Toggle Genlock to On. Areas of the image that match palette[0] (black in the Workbench palette) become transparent — the original unprocessed video shows through.
3. **Add scanlines**: Enable Scanlines. The alternating bright/dark lines complete the CRT look — you now have a HAM genlock overlay indistinguishable from a 1990 Amiga video titling setup.
4. **Adjust palette saturation**: Sweep Pal Sat. At low saturation, the HAM overlay becomes monochrome, revealing only structural edges. At high saturation, the overlay is vivid and graphic.
5. **Luma quantization**: Lower Luma Quant to 2-bit. The HAM overlay becomes a high-contrast graphic with bold tonal steps — the look of a heavily posterized Amiga screenshot.
6. **Mix blend**: Lower Mix to ~60%. The HAM overlay semi-transparently blends with the clean source — a modern compositing effect using a retro rendering engine.

**Key concepts**: Genlock transparency uses palette[0] as the key color, scanlines simulate CRT display, saturation and quantization controls shape the overlay character

---


## Tips

- **Dithering before encoding**: The Bayer dither adds texture that survives the HAM encoding, softening what would otherwise be hard quantization steps. Most effective at 160px and lower resolutions.
- **Genlock for compositing**: Enable Genlock to create transparent overlays — the HAM-processed image floats over the original video where the background color appears. This was the Amiga's killer app for video production.
- **Fringe direction for creative control**: Reversing the scan direction shifts the visual weight of every edge in the image. On text or graphic sources, this can dramatically change readability and perceived motion.
- **Scanlines complete the look**: Add scanline darkening for the full CRT-photographed-Amiga-monitor experience. The combination of HAM fringing, palette quantization, and scanline structure is the complete retro aesthetic.
- **Mix for comparison**: Without a dedicated Bypass toggle, use the Mix fader at 0% for instant A/B comparison against the original input.

---

## Glossary

| Term | Definition |
|------|------------|
| **AGA** | Advanced Graphics Architecture; the Amiga chipset (1992) that introduced HAM8 mode with 6-bit-per-channel color precision. |
| **Bayer dithering** | An ordered dithering technique using a fixed matrix of threshold offsets to simulate additional tonal levels in quantized images. |
| **CRT** | Cathode Ray Tube; a display technology using electron beams scanned across a phosphor screen, standard for televisions and monitors before LCD adoption. |
| **Genlock** | A technique for synchronizing video signals so that computer-generated graphics can be overlaid on external video, using a key color for transparency. |
| **HAM** | Hold-And-Modify; an Amiga display mode that encodes each pixel as either a palette SET or a single-channel MODIFY of the previous pixel's color. |
| **Luminance** | The brightness component (Y channel) of a YUV video signal, independent of color information. |
| **Manhattan distance** | A distance metric summing the absolute differences of each component (here, R, G, B channels) rather than using Euclidean distance. |
| **NTSC** | National Television System Committee; the analog broadcast standard used in North America and Japan, operating at 525 lines and 59.94 Hz. |
| **OCS** | Original Chip Set; the first Amiga custom chipset (1985) supporting HAM6 mode with 4-bit-per-channel color. |
| **Quantization** | The process of reducing a continuous or high-precision value to a discrete set of levels, introducing rounding error. |
| **RGB** | Red, Green, Blue; a color model representing colors as combinations of three additive primary components. |
| **Sample-and-hold** | A technique that captures a signal value at a specific instant and holds it constant for a defined period, used here for resolution downsampling. |

---
