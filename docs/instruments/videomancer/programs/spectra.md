---
draft: true
sidebar_position: 277
slug: /instruments/videomancer/spectra
title: "Spectra"
image: /img/instruments/videomancer/spectra/spectra_hero_s1.png
description: "Scientific instruments often visualize invisible phenomena by mapping measured values to color — thermal cameras paint heat as a spectrum from cool blue to hot white, weather radar maps rainfall intensity to a green-yellow-red gradient, and medical imaging uses false color to highlight tissue density."
---

![Spectra hero image](/img/instruments/videomancer/spectra/spectra_hero_s1.png)
*Spectra decomposing a video signal into spectral bands, mapping each luminance zone to a vivid false color.*

---

## Overview

**Spectra** is a false-color analysis program that slices the luminance range of a video signal into discrete bands, then paints each band with a color from a configurable palette. The result resembles the displays of scientific instruments: thermal cameras, topographic maps, weather radar: where color encodes magnitude rather than appearance. Feed any video source into Spectra, and it reveals the hidden structure of brightness as a vivid rainbow zone map.

The number of bands, the choice of palette, and the spread of tones are all adjustable in real time. At low band counts, the image collapses into bold, poster-like zones. At high band counts, the zones become narrow slivers that trace subtle gradations in the source. Enabling contour mode draws black outlines at every band transition, transforming the image into something resembling a stained-glass window or a topographic chart.

:::tip
Spectra is classified as an ***Analysis*** program because it reveals information about the video signal that is invisible in the original image. The colors you see are not the colors of the source (they are a map of its brightness structure.)
:::

### What's In a Name?

The name ***Spectra*** refers to the electromagnetic spectrum: the full range of wavelengths that includes visible light. Just as a prism splits white light into a rainbow of colors, Spectra splits a monochrome brightness range into a rainbow of false-color zones. The plural form (spectra, not spectrum) suggests the multiple bands, the multiple colors, and the multiple palettes available.

---

## Quick Start

1. Feed a video signal into Videomancer and load **Spectra**. The image immediately appears false-colored: each brightness zone mapped to a different hue from the Rainbow palette.
2. Turn **Bands** (Knob 1) to see the band count change. Counterclockwise gives you 2 wide zones; clockwise gives you up to 16 narrow zones. Watch how the color boundaries shift with the tonal structure of your source.
3. Rotate **Hue Offs** (Knob 3) to spin the palette, cycling which colors correspond to which brightness levels. The entire rainbow rotates through the zones.
4. Flip **Contour** (Switch 8) to **On**. Black outlines appear at every band boundary, giving the image a stained-glass or topographic look.

---

## Parameters

![Videomancer front panel with Spectra loaded](/img/instruments/videomancer/spectra/spectra_control_panel.png)
*Videomancer's front panel with Spectra active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Bands

| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 9 |

**Bands** sets the number of spectral zones that the luminance range is divided into. The control selects among four discrete band counts: 2, 4, 8, and 16. At the lowest setting, the range is split into two broad zones: a simple bright/dark division. At the highest setting, the range is carved into 16 narrow slivers, each painted with its own palette color.

With a low band count, the color boundaries are bold and dramatic. Increasing the count reveals progressively finer tonal structure in the source. The number of distinct colors visible at any moment depends on both this setting and the tonal range of the input signal: a flat, low-contrast source may not contain enough variation to fill all 16 zones.

---

### Knob 2 — Saturate

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Saturate** controls the chroma intensity of the false colors applied to each band. At low values, the palette colors are muted and pastel: the chroma differences from neutral gray are halved. At moderate values, colors reach roughly three-quarters intensity. At high values, the full palette chroma is applied, producing vivid, saturated bands.

:::tip
Reducing **Saturate** while keeping a high band count creates a subtle, pastel zone map that encodes brightness without overwhelming the image. This is useful when stacking Spectra in a signal chain where downstream programs add their own color.
:::

---

### Knob 3 — Hue Offs

| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |

**Hue Offs** rotates the palette assignment around the band index. At zero, band 0 maps to the first palette color, band 1 to the second, and so on. As **Hue Offs** increases, the mapping shifts: colors cycle to different bands. The offset wraps around, so rotating fully through the range returns to the starting assignment.

This is Spectra's most expressive control. Because the palette is a fixed sequence of colors, rotating the offset changes which brightness levels receive which colors. A sunset scene might shift from cool blues in the shadows to warm reds at the highlights, or the reverse (all without changing the structure of the bands themselves.)

---

### Knob 4 — Spread

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Spread** enhances the contrast of the source signal before it is quantized into bands. Below the midpoint, no spread adjustment is applied. Above the midpoint, values above mid-gray are pushed brighter and values below mid-gray are pushed darker, increasing the separation between tonal zones. This expands the effective range of the banding, causing more of the palette colors to appear even in low-contrast source material.

At minimum, the source passes through unmodified. At maximum, the contrast enhancement is strongest: shadows deepen and highlights brighten before banding occurs. This processing happens *before* band quantization, so it changes which band each pixel falls into without changing the palette itself.

---

### Knob 5 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bright** offsets the luminance of the false-color output. At the midpoint (50%), no offset is applied: the palette's native luminance values are used. Turning counterclockwise darkens the entire output; turning clockwise brightens it. The offset is added to the palette luminance after the band lookup, so it shifts the overall brightness of the false-color image without changing which band each pixel belongs to.

:::note
**Bright** affects only the luminance of the false-color output, not the source signal. Band assignments are determined before brightness is applied. Pushing **Bright** to extremes can clip the output to full black or full white.
:::

---

### Knob 6 — Gamma

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Gamma** is reserved for a future update. In the current version, adjusting this control has no visible effect on the output.

---

### Switch 7 — Palette

| Property | Value |
|----------|-------|
| Off | Rainbow |
| On | Earth |
| Default | Rainbow |

**Palette** selects the color scheme used to paint the spectral bands. Set to **Rainbow**, the palette cycles through the visible spectrum: reds, oranges, yellows, greens, cyans, blues, and magentas: distributing maximum color contrast between adjacent bands. Set to **Earth**, the palette progresses through warm tones: near-black through dark reds, oranges, and yellows toward white, resembling a thermal imaging or heat-map display.

The Rainbow palette is suited for general-purpose visualization, where you want every band to be immediately distinguishable from its neighbors. The Earth palette is better suited for thermal-style imagery, where the color scale is perceived as a continuous temperature gradient from cold to hot.

---

### Switch 8 — Contour

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Contour** enables band-boundary edge detection. When set to **On**, any pixel whose band index differs from its horizontal neighbor is rendered as black (Y = 0, U = 512, V = 512). This draws a one-pixel-wide black line at every transition between spectral zones, outlining each colored region.

The contour lines trace ***isocontours*** of the source luminance: lines of equal brightness, like elevation lines on a topographic map. With a low band count, the contour lines are sparse and sweeping. With a high band count, they cluster tightly around gradients, revealing fine tonal structure.

:::tip
Turn **Saturate** to zero and enable **Contour** to produce a pure contour-line drawing: black outlines on a gray field, with no false color. This is useful for analyzing tonal structure without the distraction of color.
:::

---

### Switch 9 — Source

| Property | Value |
|----------|-------|
| Off | Luma |
| On | Chroma |
| Default | Luma |

**Source** selects which component of the input signal drives the band decomposition. Set to **Luma**, the luminance (Y) channel is analyzed: brightness determines zone assignment. Set to **Chroma**, the U chrominance channel drives the banding instead.

In Luma mode, the zone map reveals brightness structure. In Chroma mode, the zone map reveals color information: regions of similar U-channel chrominance fall into the same band, regardless of brightness.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** reverses the luminance of the false-color output. When enabled, bright palette colors become dark and dark palette colors become bright. The inversion is applied after all other processing: palette lookup, saturation scaling, and brightness offset: so it flips the final result. Chroma values are not affected by inversion.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the original input signal directly to the output, disabling all Spectra processing. The sync delay pipeline ensures clean switching with no timing glitch. Use Bypass for instant A/B comparison between the raw input and the false-color result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original input signal and the processed false-color output. At 0% (fully left), the output is the unprocessed source. At 100% (fully right), the output is the full false-color result. Intermediate positions blend the two using per-channel linear interpolation.

A moderate Mix setting can create a tinted overlay effect: the original image visible beneath a translucent wash of false color. This is especially effective in Chroma source mode, where the overlay reveals color structure within the original scene.

---

## Background

### False-Color Imaging

***False-color imaging*** is a visualization technique that replaces the natural colors of an image with an artificial palette designed to reveal information that would otherwise be invisible or difficult to perceive. The technique originated in remote sensing and scientific imaging: weather satellites color-code cloud temperatures, medical scanners map tissue density to color, and thermal cameras render heat as a rainbow.

The core principle is simple: take a single-channel measurement: brightness, temperature, altitude, intensity: and map its range onto a color palette. The human eye can distinguish far more colors than shades of gray, so false-coloring dramatically increases the perceptual resolution of the data. Spectra applies this same principle to video in real time.

### Band Quantization

Spectra divides the source range into ***bands***: discrete zones of equal width. This is a form of ***uniform quantization***: the full 10-bit range (0 to 1023) is divided into N equal segments, and every pixel within a segment receives the same palette color. The number of segments (2, 4, 8, or 16) determines the coarseness of the zone map.

Band quantization is implemented by right-shifting the source value. A 10-bit value shifted right by 1 bit yields 2 zones. Shifted right by 2 bits yields 4 zones, by 3 bits yields 8, and by 4 bits yields 16. This is computationally efficient: no multiplication or division is required, just a bit shift. The result is a 4-bit band index that drives the palette lookup.

### Contour Detection

Spectra's contour mode detects boundaries between adjacent bands by comparing each pixel's band index to its horizontal predecessor. When a transition is detected: the current pixel falls in a different band than the pixel before it: the output is forced to black. This draws a thin edge line at every ***isocontour*** of the source signal.

This technique is closely related to ***edge detection*** in image processing, but operates on the quantized band index rather than the raw signal. The result is a set of contour lines that trace the boundaries of equal-brightness zones, much like the elevation contour lines on a topographic map. Because the comparison is horizontal only, contour lines emphasize vertical structures in the source.

### Palette Design

Each palette in Spectra is a lookup table of eight YUV color entries, indexed by the low 3 bits of the hue-offset-adjusted band index. The Rainbow palette distributes entries across the full hue circle for maximum contrast between adjacent bands. The Earth palette arranges entries along a single warm gradient: dark neutrals through reds and oranges toward bright whites: producing a perceptual temperature scale.

The hue offset control adds a constant to the band index before lookup, rotating the color assignment. Because the index wraps modulo 8, the palette repeats cyclically across all 16 bands. Two adjacent bands always receive different colors (within the same 8-entry cycle), ensuring visual separation.


---

## Signal Flow

### Signal Flow Notes

The pipeline has two key structural properties. First, band quantization operates on the *modified* source: after Spread has enhanced the contrast. This means Spread changes which band each pixel falls into, altering the zone boundaries without touching the palette. Second, contour detection compares adjacent band indices in the horizontal (pixel) direction only. The contour line is drawn at the current pixel when its band differs from the previous pixel, producing a one-pixel-wide edge.

:::note
Because contour detection is a horizontal-neighbor comparison, contour lines appear at vertical edges in the source image (where brightness steps between adjacent pixels). Horizontal edges: where brightness changes from one scan line to the next: do not produce contour lines.
:::

The wet/dry mix uses three `interpolator_u` instances to independently crossfade each channel (Y, U, V). The mix blends the delayed original signal with the processed output, so at Mix = 0% the original passes through unchanged. The delay pipeline ensures the original and processed signals are time-aligned before mixing.


---

## Exercises

These exercises progress from basic false-color visualization through contour mapping to creative palette design. Each exercise explores a different aspect of Spectra's spectral decomposition.
### Exercise 1: Thermal Camera

![Thermal Camera result](/img/instruments/videomancer/spectra/spectra_ex1_s1.png)
*Thermal Camera — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A thermal-camera-style visualization where brightness maps to a heat scale, revealing the tonal structure of a live video signal.

#### Key Concepts

- False-color mapping reveals brightness structure invisible in the original
- Band count controls the granularity of the zone map
- Palette selection changes the visual language of the analysis

#### Video Source

A live camera feed or recorded footage with a range of brightness levels (faces, landscapes, or indoor scenes work well.)

#### Steps

1. Load **Spectra** and set **Palette** (Switch 7) to **Earth**. The image shifts from rainbow bands to a warm dark-to-red-to-yellow-to-white progression.
2. Turn **Bands** (Knob 1) fully clockwise to set 16 bands. The image is sliced into many narrow thermal zones.
3. Increase **Saturate** (Knob 2) fully clockwise for vivid thermal colors.
4. Adjust **Spread** (Knob 4) to approximately 80%. This pushes the tonal range apart, ensuring that even low-contrast sources fill all available thermal zones.
5. Try rotating **Hue Offs** (Knob 3) slowly. The thermal palette slides through the bands (previously hot regions become cold-colored and vice versa.)

#### Settings

| Control | Value |
|---------|-------|
| Bands | 100% (16 bands) |
| Saturate | 100% |
| Hue Offs | 0 deg |
| Spread | 80% |
| Bright | 50% |
| Gamma | 50% |
| Palette | Earth |
| Contour | Off |
| Source | Luma |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Topographic Map

![Topographic Map result](/img/instruments/videomancer/spectra/spectra_ex2_s1.png)
*Topographic Map — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A topographic-map-style image with contour lines outlining regions of equal brightness, like elevation lines on a terrain map.

#### Key Concepts

- Contour lines trace isocontours of equal brightness
- Low band counts produce bold, map-like regions
- Contour with reduced saturation creates analytical line drawings

#### Video Source

Footage with smooth tonal gradients: sky at sunset, slowly moving water, or a gradient test pattern.

#### Steps

1. Set **Bands** (Knob 1) to a moderate value (about 25%, yielding 4 bands). The image breaks into four broad color zones.
2. Enable **Contour** (Switch 8). Black outlines appear at every boundary between zones, drawing the topography of the brightness field.
3. Reduce **Saturate** (Knob 2) to approximately 40%. The colors soften to pastels, letting the contour lines dominate.
4. Slowly increase **Bands** toward 8 or 16 bands. More contour lines appear as the zone boundaries become finer, revealing progressively subtler tonal gradients.
5. Try setting **Palette** (Switch 7) to **Earth** for a terrain-chart aesthetic, then back to **Rainbow** for a weather-map look.

#### Settings

| Control | Value |
|---------|-------|
| Bands | ~25% (4 bands) |
| Saturate | 40% |
| Hue Offs | 0 deg |
| Spread | 60% |
| Bright | 50% |
| Gamma | 50% |
| Palette | Rainbow |
| Contour | On |
| Source | Luma |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Chroma Spectroscopy

![Chroma Spectroscopy result](/img/instruments/videomancer/spectra/spectra_ex3_s1.png)
*Chroma Spectroscopy — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An overlay that reveals the chrominance structure of a color image, blending false-color chroma analysis with the original footage.

#### Key Concepts

- Source selection switches from luminance to chrominance analysis
- Hue offset rotates the palette assignment around the bands
- Mix crossfade blends false color with the original image

#### Video Source

Colorful footage: flowers, painted walls, neon signs, or any scene with strong saturated colors. Avoid monochrome sources, which have no chroma structure to analyze.

#### Steps

1. Set **Source** (Switch 9) to **Chroma**. The spectral bands now map to the U chrominance channel rather than luminance. Regions with similar chroma values fall into the same band, regardless of brightness.
2. Set **Bands** (Knob 1) to approximately 50% (8 bands) and **Saturate** (Knob 2) to 100%.
3. Rotate **Hue Offs** (Knob 3) slowly through its full range. Because the palette is rotating over the chroma values, the colors cycle through the chrominance structure of the image.
4. Pull **Mix** (Fader 12) down to approximately 50%. The original image becomes visible beneath the false-color overlay, creating a tinted X-ray effect that shows both the original content and its chroma structure.
5. Enable **Contour** (Switch 8) to draw chroma isocontours: outlines around regions of equal chrominance, independent of brightness.

#### Settings

| Control | Value |
|---------|-------|
| Bands | ~50% (8 bands) |
| Saturate | 100% |
| Hue Offs | 0 deg |
| Spread | 100% |
| Bright | 50% |
| Gamma | 50% |
| Palette | Rainbow |
| Contour | On |
| Source | Chroma |
| Invert | Off |
| Bypass | Off |
| Mix | 50% |

---
## Glossary

- **Band**: A discrete zone within the luminance or chrominance range, defined by uniform quantization of the source signal.

- **Chrominance**: The color information in a video signal, encoded as U and V components in YUV color space, independent of brightness.

- **Contour**: A line drawn at the boundary between adjacent bands, analogous to elevation lines on a topographic map.

- **False Color**: A visualization technique that replaces natural image colors with an artificial palette to reveal information encoded in a single channel.

- **Interpolation**: Blending between two values using a fractional mixing coefficient; used here for the wet/dry crossfade.

- **Isocontour**: A line connecting points of equal value: in Spectra, points at the boundary between two spectral bands.

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Palette**: A fixed table of colors assigned to spectral bands; Spectra offers Rainbow and Earth palettes.

- **Quantization**: Mapping a continuous range of values to a smaller set of discrete levels, producing visible steps or zones in gradients.

- **Saturation**: The intensity or purity of a color; high saturation produces vivid hues, low saturation approaches neutral gray.

- **Spread**: Contrast enhancement applied to the source signal before band quantization, pushing values away from the midpoint to fill more zones.

---
