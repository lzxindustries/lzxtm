---
draft: true
sidebar_position: 64
slug: /instruments/videomancer/contour
title: "Contour"
image: /img/instruments/videomancer/contour/contour_hero_s1.png
description: "A topographic map turns continuous terrain into a set of discrete elevation lines."
---

![Contour hero image](/img/instruments/videomancer/contour/contour_hero_s1.png)
*Contour tracing iso-luminance lines across a landscape: dark lines separating bands of brightness like a topographic elevation map drawn in light.*

---

## Overview

**Contour** draws lines wherever the brightness of your video crosses discrete threshold levels, creating an image that looks like a ***topographic map*** of light. Each contour line marks the boundary between one brightness band and the next. Where the image changes suddenly: sharp edges, contrasty transitions: the contour lines crowd together. Where the image is smooth and gradual, the lines spread apart. The result is an abstraction that reveals the terrain of luminance hidden in any video source.

The program quantizes the input luma into a configurable number of discrete levels (from 16 to 512), then detects where the quantized value of a pixel differs from its horizontal or vertical neighbor. Those boundary pixels become contour lines. An optional ***index contour*** system (borrowed from cartography) draws every Nth line brighter than the others, giving the map a sense of scale. The areas between contour lines can show the original video or a flat-fill background.

### What's In a Name?

***Contour*** comes from the Italian ***contorno***, meaning "outline" or "to draw around." In cartography, contour lines connect points of equal elevation: the wavy concentric lines on a topographic map. Contour applies the same principle to video: its lines connect pixels of equal brightness, turning a moving image into a living elevation map where brightness is the altitude.

---

## Quick Start

1. Feed any video source into Videomancer with **Contour** loaded. You'll see the image broken into horizontal bands of flat brightness, with dark lines at the boundaries.
2. Turn **Interval** (Knob 1) clockwise. The contour lines multiply: more brightness levels are distinguished, and the lines pack together more tightly in areas of gradual transition.
3. Increase **Line Thk** (Knob 2) to about 80%. The contour lines become brighter and more prominent against the background.
4. Set **Style** (Switch 7) to Terrain. The areas between contours become a flat gray instead of the original video, emphasizing the map-like quality.

---

## Parameters

![Videomancer front panel with Contour loaded](/img/instruments/videomancer/contour/contour_control_panel.png)
*Videomancer's front panel with Contour active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Interval

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Interval** controls how many discrete brightness levels the image is divided into. At low values, the image is quantized into just 16 levels: very coarse banding with widely spaced contour lines. As Interval increases, the number of levels rises through 32, 64, 128, 256, and up to 512, producing finer and finer contour spacing. With fine spacing, only areas with very steep brightness gradients show visible contour lines; with coarse spacing, contours appear everywhere.

:::tip
For a clean topographic look, start with Interval around 40% (about 64 brightness levels). This gives enough resolution to see the shape of the image while keeping the contour lines clearly distinct.
:::

---

### Knob 2 — Line Thk

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Line Thk** sets the brightness of the contour lines themselves. At low values, the lines are dim and subtle. At high values, they are bright white. Index contours (when enabled) are drawn at the full Line Thk brightness, while regular contours are drawn at half brightness: so increasing this parameter also increases the contrast between major and minor contours.

---

### Knob 3 — Major Frq

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Major Frq** controls the brightness of the flat fill shown between contour lines when Style is set to Terrain. At 0%, the fill is black; at 100%, the fill is white. When Style is set to Topo (source video visible between contours), this control has no visible effect on the fill areas.

---

### Knob 4 — Fill Xpar

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Fill Xpar** determines how frequently index (major) contours appear. At low values, every second contour is drawn as an index line. At mid values, every fourth or eighth contour is an index. At high values, only every sixteenth contour is promoted to index. Index contours are drawn at full brightness while regular contours are half brightness, creating the visual hierarchy familiar from cartographic maps.

---

### Knob 5 — Smooth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Smooth** adds a hue shift to the contour lines when Color is set to Source. This shifts the U (blue-yellow) component of the contour line color, creating colored rather than monochrome contour lines. At 50%, no offset is applied. Below 50%, the contours shift toward blue; above 50%, toward yellow.

---

### Knob 6 — Offset

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Offset** is reserved and currently has no visible effect.

---

### Switch 7 — Style

| Property | Value |
|----------|-------|
| Off | Topo |
| On | Terrain |
| Default | Topo |

**Style** selects what is shown between the contour lines. **Topo** preserves the original source video in the non-contour areas, overlaying contour lines on top. **Terrain** replaces the non-contour areas with a flat fill whose brightness is set by Major Frq, creating a clean map-like rendering with only lines and a uniform background.

---

### Switch 8 — Color

| Property | Value |
|----------|-------|
| Off | Brown |
| On | Source |
| Default | Brown |

**Color** enables or disables the index contour system. When set to **Brown**, all contour lines are drawn at the same brightness (no index hierarchy). When set to **Source**, index contours are enabled: every Nth contour (frequency set by Fill Xpar) is drawn brighter than the rest, creating a visual hierarchy of major and minor contour lines.

:::note
The label "Brown" vs "Source" refers to the intended map style: brown-ink topographic lines (uniform) versus source-derived colored contours (with index hierarchy). The actual line color is controlled by the Smooth parameter and the Color toggle interaction.
:::

---

### Switch 9 — Fill

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Fill** enables or disables color on the contour lines themselves. When **Off**, contour lines are rendered in monochrome (neutral gray at the brightness set by Line Thk). When **On**, the contour lines receive a hue shift controlled by Smooth, creating colored lines that can make the map more visually interesting.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** is reserved for future use and currently has no visible effect.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) signal and the wet (Contour-processed) signal.

---

## Background

### Topographic cartography

***Topographic maps*** represent three-dimensional terrain on a two-dimensional surface using contour lines: curves that connect all points at the same elevation. Where the terrain is steep, contour lines pack tightly together. Where the terrain is gentle, they spread apart. A skilled map reader can reconstruct the shape of hills, valleys, and ridges purely from the pattern of these lines. Contour applies an identical principle to brightness: the "elevation" is the luminance value of each pixel.

### Quantization and contouring

The technical process behind Contour is ***luminance quantization***: reducing the continuous range of brightness values to a small number of discrete steps. This is done by discarding the low-order bits of the 10-bit luminance value: shift right to remove detail, shift left to restore scale. The number of bits discarded determines the number of levels (and therefore the density of contour lines). Contour lines appear wherever a quantized pixel differs from its immediate horizontal neighbor (1-pixel delay register) or its vertical neighbor (previous scanline stored in a BRAM line buffer).

### Index contours and map hierarchy

Cartographers use a hierarchical system where every fifth contour line (in typical 1:24,000 scale maps) is drawn slightly thicker and labeled with the elevation value. These ***index contours*** help the map reader quickly estimate elevation without counting every individual line. Contour implements a similar system: a bitmask on the quantized level number determines which lines are promoted to "index" status and drawn at full brightness rather than half brightness.


---

## Signal Flow

### Signal Flow Notes

The contour detection compares quantized values rather than raw pixel values, which provides inherent noise immunity: small pixel-to-pixel variations that don't cross a quantization boundary are ignored. The detection is strictly binary (is the boundary crossed or not), with no gradual falloff, which gives the contour lines their characteristic crisp, one-pixel-wide appearance. The line buffer uses a single BRAM tile to store one complete line of quantized Y values for vertical comparison.


---

## Exercises

These exercises progress from a basic topographic rendering to a colorful animated terrain display.
### Exercise 1: Classic Topographic Map

![Classic Topographic Map result](/img/instruments/videomancer/contour/contour_ex1_s1.png)
*Classic Topographic Map — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A black-and-white topographic map of brightness, with clean contour lines on a uniform gray background.

#### Key Concepts

- Quantization creates discrete brightness bands
- Contour lines appear at band boundaries
- Terrain-style fill creates a clean map-like look

#### Video Source

A landscape, face, or any image with smooth tonal gradients. High-contrast geometric scenes work less well (too many edges = too many contour lines everywhere).

#### Steps

1. Set **Style** (Switch 7) to Terrain for a flat-fill background.
2. Set **Interval** (Knob 1) to about 40% for moderate contour density.
3. Set **Major Frq** (Knob 3) to about 30% for a dark gray background.
4. Set **Line Thk** (Knob 2) to about 80% for bright contour lines.
5. Set **Color** (Switch 8) to Source to enable index contours.
6. Set **Fill Xpar** (Knob 4) to about 50% so every 8th contour is thicker.

#### Settings

| Control | Value |
|---------|-------|
| Interval | ~40% |
| Line Thk | ~80% |
| Major Frq | ~30% |
| Fill Xpar | ~50% |
| Smooth | ~50% |
| Offset | ~50% |
| Style | Terrain |
| Color | Source |
| Fill | Off |
| Animate | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 2: Source-Through Contour Overlay

![Source-Through Contour Overlay result](/img/instruments/videomancer/contour/contour_ex2_s1.png)
*Source-Through Contour Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

The original video with contour lines overlaid, emphasizing edges and tonal transitions.

#### Key Concepts

- Topo style preserves the original video between contour lines
- The contour lines act as an edge overlay on the source image
- Fine interval spacing emphasizes areas of rapid brightness change

#### Video Source

Any dynamic video source: movement creates shifting contour patterns as the brightness landscape changes frame to frame.

#### Steps

1. Set **Style** to Topo. The original video now shows through between the contour lines.
2. Increase **Interval** to about 70% for dense contour lines.
3. Set **Line Thk** to about 60% (visible but not overpowering.)
4. Set **Fill** (Switch 9) to On and adjust **Smooth** (Knob 5) to give the lines a colored tint.
5. Reduce **Mix** (Fader 12) to about 60% to blend the contour overlay with the original.

#### Settings

| Control | Value |
|---------|-------|
| Interval | ~70% |
| Line Thk | ~60% |
| Major Frq | ~50% |
| Fill Xpar | ~50% |
| Smooth | ~60% |
| Offset | ~50% |
| Style | Topo |
| Color | Brown |
| Fill | On |
| Animate | Off |
| Bypass | Off |
| Mix | ~60% |

---

### Exercise 3: Dense High-Contrast Contour Field

![Dense High-Contrast Contour Field result](/img/instruments/videomancer/contour/contour_ex3_s1.png)
*Dense High-Contrast Contour Field — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dense field of contour lines on a near-black background (the image reduced to a lattice of brightness boundaries.)

#### Key Concepts

- Maximum contour density creates a dense line field
- Terrain fill with a dark background creates maximum contrast
- Index contours provide visual rhythm in a dense field

#### Video Source

A slowly moving image with a mix of gradients and detail (clouds, water, or abstract video textures.)

#### Steps

1. Set **Interval** to 100% for maximum contour density (512 levels).
2. Set **Line Thk** to 100% for maximum line brightness.
3. Set **Style** to Terrain and **Major Frq** to about 5% (near-black fill).
4. Enable index contours: **Color** to Source, **Fill Xpar** to about 25% (every 4th line is major).
5. The image becomes a dense lattice of fine lines with periodic bright index contours.

#### Settings

| Control | Value |
|---------|-------|
| Interval | ~100% |
| Line Thk | ~100% |
| Major Frq | ~5% |
| Fill Xpar | ~25% |
| Smooth | ~50% |
| Offset | ~50% |
| Style | Terrain |
| Color | Source |
| Fill | Off |
| Animate | Off |
| Bypass | Off |
| Mix | ~100% |

---
## Glossary

- **Contour Line**: A line connecting all points at the same value: in topography, the same elevation; in Contour, the same brightness level.

- **Index Contour**: A heavier contour line drawn at regular intervals (every 4th, 8th, or 16th) to provide visual hierarchy and help the viewer estimate values.

- **Line Buffer**: A single-scanline BRAM memory that stores the previous line's quantized brightness, enabling vertical contour detection.

- **Quantization**: The process of reducing a continuous range of values to a small number of discrete levels, discarding fine detail to reveal broad structure.

- **Topographic Map**: A map that represents three-dimensional terrain using contour lines (the direct inspiration for Contour's visual approach.)

---
