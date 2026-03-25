---
draft: true
sidebar_position: 14
slug: /instruments/videomancer/barcode
title: "Barcode"
image: /img/instruments/videomancer/barcode/barcode_hero_s1.png
description: "Barcodes are a visual language designed for machines — parallel lines of varying width that encode numeric data."
---

![Barcode hero image](/img/instruments/videomancer/barcode/barcode_hero_s1.png)
*Barcode encoding a live camera feed as variable-width vertical stripes, transforming luminance into a scannable pattern of dark and light bars.*

---

## Overview

Barcode turns your video signal into a field of vertical (or horizontal) stripes that look like the barcodes printed on product packaging. The program samples the brightness of the incoming image and renders it as thick or thin bars: bright areas become thin bars separated by wide white spaces, while dark areas produce thick, heavy bars. The result is a graphic, high-contrast transformation that makes any video look as if it were being read by a laser scanner at the checkout counter.

Beyond simple vertical stripes, Barcode offers grid and matrix modes that extend the pattern into two dimensions, creating lattice-like overlays. A set of color tint options lets you shift the bars away from stark black-and-white into tinted palettes. Guard bars, contrast shaping, and brightness offset give you fine control over the density and tone of the barcode field. When blended with the dry signal using the fader, the bars overlay the source image like a scan-line cage.

:::tip
***The Mix fader is key to compositing.*** At full mix, the barcode replaces the image entirely. Pull the fader back to overlay the bar pattern on top of the source video, creating a hybrid of data and image.
:::

### What's In a Name?

The name ***Barcode*** refers directly to the machine-readable stripe patterns printed on packaging and labels. These ***Universal Product Codes*** encode numeric data as sequences of bars and spaces of varying widths. Barcode borrows the visual vocabulary of that encoding system: quantized luminance, fixed-width stripe cells, guard bars at the margins, and quiet zones of blank space. The program doesn't encode real data, but it transforms video into imagery that looks convincingly like it could be scanned.

---

## Quick Start

1. Turn **Bar W** (Knob 1) to the midpoint. The image breaks into a pattern of vertical stripes: alternating bars and white spaces that tile across the screen.
2. Sweep **Levels** (Knob 2) slowly. The number of brightness steps in the bars changes: fewer levels create stark, high-contrast bars, while more levels let the bars carry more tonal nuance from the source.
3. Toggle **Type** (Switch 7) to **Matrix**. The stripe pattern rotates, adding a second dimension to the barcode field.
4. Pull the **Mix** fader (Fader 12) to the midpoint. The barcode pattern blends with the original video, overlaying stripes on top of the source image.

---

## Parameters

![Videomancer front panel with Barcode loaded](/img/instruments/videomancer/barcode/barcode_control_panel.png)
*Videomancer's front panel with Barcode active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Bar W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bar W** controls the width of each individual bar in the stripe pattern. At low values, bars are narrow: just one or two pixels wide: producing a dense, fine-grained field of hairline stripes. As you increase Bar W, the bars grow wider and the pattern becomes chunkier, with broad blocks of color separated by equally broad spaces. At maximum, each bar occupies up to 64 pixels, creating a very coarse, blocky grid.

The bar width also determines the spatial period of the stripe pattern: wider bars mean fewer stripes visible across the screen. Narrow bars produce dense, textile-like textures; wide bars produce bold, graphic partitions.

---

### Knob 2 — Levels

| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 9 |

**Levels** controls the number of ***quantization*** levels applied to the luminance of each bar. At low values, the brightness of the bars is crushed into very few steps: the bars snap to just a handful of distinct tones, producing stark, poster-like contrast. As Levels increases, more brightness steps are preserved, and the bars carry a richer gradient of tones inherited from the source image.

:::note
Levels uses a stepped control mode with eight detent positions. Each position selects a different quantization depth internally.
:::

---

### Knob 3 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contrast** adjusts the tonal separation between bright and dark bars. At the midpoint, contrast is neutral. Turning Contrast above the midpoint pushes bright bars brighter and dark bars darker, increasing the visual punch of the barcode pattern. Below the midpoint, bright and dark bars converge toward a flat gray, reducing the legibility of the stripe pattern.

---

### Knob 4 — Spacing

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Spacing** controls the gap between adjacent bars. At low values, bars are packed tightly together with little or no visible space between them, creating a dense, saturated stripe field. Increasing Spacing widens the white gaps between bars, letting the background breathe and making individual bars more distinct (closer to the look of a printed barcode label.)

---

### Knob 5 — Quiet Zn

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Quiet Zn** sets the width of the ***quiet zone***, the blank margin of white space at the left and right edges of the barcode field. Real barcodes require quiet zones so that scanners can distinguish the code from surrounding graphics. At zero, the stripe pattern extends all the way to the edges of the frame. Increasing Quiet Zn pushes the stripes inward, framing the barcode within a border of empty space.

---

### Knob 6 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bright** applies a global brightness offset to the entire barcode image. At the midpoint, brightness is neutral: no offset is applied. Turning Bright above the midpoint lifts the entire image, washing out the darkest bars. Below the midpoint, the image darkens, and even the white spaces between bars begin to gray out. Use Bright to shift the overall exposure of the barcode pattern without changing the contrast relationship between bars.

---

### Switch 7 — Type

| Property | Value |
|----------|-------|
| Off | 1D Vert |
| On | Matrix |
| Default | 1D Vert |

**Type** selects the orientation of the bar pattern. In the **1D Vert** position, bars run vertically: the classic barcode look, with stripes marching from left to right. In the **Matrix** position, the bar orientation changes, creating a different spatial arrangement of the stripe field.

:::tip
Combine **Type** with **Color** (Switch 8) for additional pattern modes. The two switches together select from a family of bar geometries: vertical stripes, horizontal stripes, and two-dimensional grid patterns.
:::

---

### Switch 8 — Color

| Property | Value |
|----------|-------|
| Off | B/W |
| On | Green |
| Default | B/W |

**Color** selects the color tint of the barcode pattern. In the **B/W** position, bars are rendered in neutral black and white with no color bias. In the **Green** position, the bars take on a green tint: the same sickly green glow of a barcode scanner's laser line.

---

### Switch 9 — Guard

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Guard** enables the ***guard bars***, the tall, dark lines at the very beginning and end of a barcode that mark where the code starts and stops. When Guard is set to **On**, thin black bars appear at the left and right edges of the active video area. When set to **Off**, the stripe pattern extends uninterrupted to the frame edges.

:::tip
Guard bars add a finishing touch that makes the barcode pattern look authentic. Enable them when you want the output to resemble an actual product label.
:::

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** reverses the luminance of the barcode pattern. When **Off**, bars are dark on a light background: the standard barcode appearance. When **On**, the polarity flips: bars become bright on a dark background, like a photographic negative of a barcode.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all barcode processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the barcode-processed result.

---

:::note Toggle Group Notes

**Type** (Switch 7) and **Color** (Switch 8) together form a combined two-bit mode selector that controls both bar orientation and color tint. The four combinations produce distinct visual modes:

| Type | Color | Result |
|------|-------|--------|
| 1D Vert | B/W | Vertical black-and-white stripes (classic barcode) |
| Matrix | B/W | Horizontal black-and-white stripes |
| 1D Vert | Green | Two-dimensional grid pattern (vertical + horizontal bars) |
| Matrix | Green | Vertical stripes with green tint |

Similarly, **Guard** (Switch 9) and **Invert** (Switch 10) together form a combined two-bit color tint selector:

| Guard | Invert | Result |
|-------|--------|--------|
| Off | Off | Neutral black and white |
| On | Off | Warm reddish tint |
| Off | On | Cool bluish tint |
| On | On | Green tint |

:::note
Because these toggles interact in groups, the label on each individual switch describes only part of the combined behavior. Experiment with all four combinations to explore the full palette of modes.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** controls the wet/dry blend between the barcode-processed signal and the original input. At 100%, fully right, the output is entirely barcode: the source video is completely replaced by the stripe pattern. At 0%, fully left, the output is the unprocessed source. Intermediate positions overlay the barcode on top of the source with variable opacity, creating a composited look where the stripe pattern is visible but the underlying image shows through.

:::tip
A Mix value around 50% creates a striking overlay effect: the barcode stripes act as a semi-transparent grid laid over the source footage. This is especially effective with moving video, where the bars remain static while the image flows beneath them.
:::

---

## Background

### Barcodes and machine vision

The first patent for a barcode system was filed in 1952 by Norman Woodland and Bernard Silver. Woodland's original design used concentric circles: a bull's-eye pattern: but the idea of encoding data as parallel lines of varying width eventually won out. The ***Universal Product Code*** (UPC), introduced in 1974, became the ubiquitous standard: a sequence of black bars and white spaces that encodes a 12-digit number. A laser scanner reads the pattern by measuring the reflectance of each stripe.

In a real UPC barcode, data is encoded in the ***widths*** of bars and spaces. A wider bar represents a different bit pattern than a narrow bar. The start and end of the code are marked by fixed ***guard bars***, and a blank ***quiet zone*** on either side ensures the scanner can distinguish the code from its surroundings. Barcode borrows all of these visual conventions: variable width, guard bars, quiet zones: and applies them to video.

### Quantization and level reduction

***Quantization*** is the process of mapping a continuous range of values to a smaller set of discrete steps. When you photograph a scene, the camera's sensor captures billions of possible brightness levels, but the digital file stores only a fixed number: 256 levels for 8-bit video, or 1024 for 10-bit. Reducing the number of levels further produces visible banding: smooth gradients collapse into flat plateaus separated by hard edges. This is the same principle behind ***posterization*** in image editing.

Barcode uses quantization to decide how dark each bar should be. The incoming luminance of each stripe region is rounded down to the nearest quantization step, then rendered as a bar of that brightness. Fewer levels mean more aggressive rounding, and the bars snap to a small set of distinct tones. More levels let the bars carry a wider range of brightness, producing a more detailed barcode.

### Color encoding in barcodes

Traditional barcodes are strictly monochrome: the contrast between black ink and white paper is what makes them reliable. Two-dimensional codes like ***QR codes*** are also black and white, though some modern implementations add color for branding. Barcode takes the liberty of tinting the stripe pattern with selectable color palettes: warm reds, cool blues, and green tones inspired by the laser scanners used to read real barcodes. The tint is applied uniformly to the UV chrominance channels, shifting the entire pattern away from neutral.


---

## Signal Flow

### Signal Flow Notes

Two key architectural features define the barcode pipeline:

1. **Position-based stripe generation**: The program maintains horizontal and vertical pixel counters synchronized to the video timing. Each pixel's position is tested against the bar width using modular arithmetic on the lower 6 bits of the counter. This creates a repeating stripe pattern with a fixed spatial period. The bar orientation mode selects whether the horizontal counter, vertical counter, or both are used, controlling whether stripes run vertically, horizontally, or in a grid.

2. **Luminance-driven bar darkness**: The quantized luminance of the source image determines how dark each bar is drawn. In bar regions, the output Y value is the quantized luma: bright source areas produce light bars, dark areas produce dark bars. In space regions (between bars), the output is forced to white (1023). This creates the characteristic barcode appearance where bar width is fixed but bar darkness varies with the source content.

:::tip
**Processing order matters.** Quantization happens in Stage 2 before contrast and brightness adjustments in Stages 3–4. This means contrast and brightness shape the quantized result, not the raw input. Adjusting Contrast after quantization exaggerates the steps between quantized levels.
:::


---

## Exercises

These exercises progress from basic stripe generation to full barcode compositing. Each exercise builds on the previous one, introducing more controls and creative possibilities.
### Exercise 1: Classic Vertical Barcode

![Classic Vertical Barcode result](/img/instruments/videomancer/barcode/barcode_ex1_s1.png)
*Classic Vertical Barcode — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean vertical barcode where the stripe darkness follows the luminance of the source image.

#### Key Concepts

- Bar width controls stripe density
- Quantization levels determine tonal richness of bars
- Contrast shapes the visual weight of the pattern

#### Video Source

A live camera feed or recorded footage with a mix of bright and dark regions (a face, a landscape, or a high-contrast graphic.)

#### Steps

1. **Set bar width**: Turn **Bar W** (Knob 1) to about 30%. The image breaks into a field of medium-width vertical stripes.
2. **Reduce levels**: Turn **Levels** (Knob 2) fully clockwise for maximum quantization depth. The bars carry a range of tones from the source.
3. **Boost contrast**: Increase **Contrast** (Knob 3) to about 70%. The difference between dark and light bars becomes more pronounced.
4. **Add guard bars**: Set **Guard** (Switch 9) to **On**. Thin black bars appear at the left and right edges, framing the barcode.
5. **Compare**: Toggle **Bypass** (Switch 11) to compare the barcode pattern with the raw source.

#### Settings

| Control | Value |
|---------|-------|
| Bar W | ~30% |
| Levels | 16 |
| Contrast | ~70% |
| Spacing | ~50% |
| Quiet Zn | 0% |
| Bright | ~50% |
| Type | 1D Vert |
| Color | B/W |
| Guard | On |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Tinted Grid Overlay

![Tinted Grid Overlay result](/img/instruments/videomancer/barcode/barcode_ex2_s1.png)
*Tinted Grid Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A colored two-dimensional grid overlaid on the source video at partial opacity.

#### Key Concepts

- Toggle combinations create grid patterns and color tints
- The Mix fader composites the barcode over the source
- Brightness offset shifts the overall exposure of the pattern

#### Video Source

Footage with smooth gradients and gentle motion (clouds, water, or abstract color fields work well.)

#### Steps

1. **Enable grid mode**: Set **Type** (Switch 7) to **1D Vert** and **Color** (Switch 8) to **Green**. A two-dimensional grid of intersecting bars appears.
2. **Set bar width**: Turn **Bar W** (Knob 1) to about 50%. The grid lines are medium thickness with visible gaps between them.
3. **Add color tint**: Set **Guard** (Switch 9) to **On**. The grid shifts to a warm reddish tint.
4. **Reduce mix**: Pull the **Mix** fader (Fader 12) to about 50%. The grid blends with the source, becoming a semi-transparent overlay.
5. **Adjust brightness**: Sweep **Bright** (Knob 6) to shift the overall lightness of the grid. Find a balance where the grid is visible but doesn't overwhelm the source.

#### Settings

| Control | Value |
|---------|-------|
| Bar W | ~50% |
| Levels | 12 |
| Contrast | ~50% |
| Spacing | ~30% |
| Quiet Zn | ~30% |
| Bright | ~40% |
| Type | 1D Vert |
| Color | Green |
| Guard | On |
| Invert | Off |
| Bypass | Off |
| Mix | ~50% |

---

### Exercise 3: Inverted Barcode Negative

![Inverted Barcode Negative result](/img/instruments/videomancer/barcode/barcode_ex3_s1.png)
*Inverted Barcode Negative — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A high-contrast inverted barcode with guard bars and quiet zones, resembling a photographic negative of a product label.

#### Key Concepts

- Inversion reverses the polarity of the barcode
- Combining all stages produces the most dramatic transformations
- Quiet zone framing completes the barcode aesthetic

#### Video Source

High-contrast footage with strong shapes: silhouettes, geometric patterns, or text on a plain background.

#### Steps

1. **Narrow bars**: Set **Bar W** (Knob 1) to about 45%. The stripe pattern is moderately dense.
2. **High contrast**: Turn **Contrast** (Knob 3) to about 70%. Bars are punchy and well-separated.
3. **Reduce levels**: Set **Levels** (Knob 2) low. The bars snap to just a few distinct brightness levels, producing a stark, graphic quality.
4. **Invert**: Set **Invert** (Switch 10) to **On**. The barcode flips to bright bars on a dark background.
5. **Add quiet zone**: Increase **Quiet Zn** (Knob 5) to about 30%. White margins appear at the edges, framing the barcode.
6. **Guard bars**: Set **Guard** (Switch 9) to **On** for the finishing touch.
7. **Full mix**: Ensure the **Mix** fader (Fader 12) is at 100% for the full barcode effect.

#### Settings

| Control | Value |
|---------|-------|
| Bar W | ~45% |
| Levels | 4 |
| Contrast | ~70% |
| Spacing | ~20% |
| Quiet Zn | ~30% |
| Bright | ~50% |
| Type | 1D Vert |
| Color | B/W |
| Guard | On |
| Invert | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Guard Bar**: A fixed dark bar at the beginning or end of a barcode that marks the start or stop of the encoded data region

- **Interpolator**: A hardware module that smoothly blends between two input values based on a mix coefficient, used here for the wet/dry crossfade

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color

- **Quantization**: Mapping a continuous range of values to a smaller set of discrete steps, producing visible banding in gradients

- **Quiet Zone**: The blank margin of white space surrounding a barcode, required so that scanners can distinguish the code from adjacent graphics

- **UPC**: Universal Product Code; the standard one-dimensional barcode format used on retail products since 1974

- **YUV**: A color encoding system that separates brightness (Y) from color information (U and V), used in broadcast video


---
