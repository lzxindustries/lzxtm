---
draft: true
sidebar_position: 100
slug: /instruments/videomancer/emboss
title: "Emboss"
image: /img/instruments/videomancer/emboss/emboss_hero_s1.png
description: "Every surface tells a story through the way it catches light."
---

![Emboss hero image](/img/instruments/videomancer/emboss/emboss_hero_s1.png)
*Emboss transforming a face into a carved stone bas-relief: highlights and shadows revealing surface geometry as if the image were pressed into metal.*

---

## Overview

**Emboss** creates a three-dimensional ***bas-relief*** effect by computing spatial gradients: the rate at which brightness changes from pixel to pixel: and combining them with a configurable virtual light source direction. Where a surface slopes toward the light, it brightens; where it slopes away, it darkens. The result looks like the original image has been pressed into a metal or stone surface and lit from a single direction.

The program computes both horizontal gradients (comparing each pixel to its left neighbor) and vertical gradients (comparing each pixel to the previous scanline via a BRAM line buffer), then combines them according to one of eight cardinal or diagonal light directions. A depth control amplifies the gradient, a bias sets the neutral mid-point, and a contrast stage stretches the final output. An optional metallic tint adds a warm color cast to the relief surface.

### What's In a Name?

***Emboss*** comes from the Old French ***embocer*** ("to swell out"), referring to the technique of creating raised designs on metal, leather, or paper. In traditional metalwork, embossing pushes the material up from behind to create a three-dimensional surface. Emboss simulates this in video by computing how brightness "rises" and "falls" across the image surface, then lighting the result as if it were a physical relief.

---

## Quick Start

1. Feed any video source into Videomancer with **Emboss** loaded. The image immediately takes on a gray, three-dimensional appearance with edges revealed as highlights and shadows.
2. Increase **Depth** (Knob 1) to about 60%. The edge relief becomes more pronounced (highlights brighter, shadows deeper.)
3. Slowly turn **Light Ang** (Knob 2). The light source moves around the image in eight directions, dramatically changing which edges catch the light and which fall into shadow.
4. Adjust **Bias** (Knob 3) to control the overall brightness of the relief. At 50%, the surface is mid-gray. Below 50%, it darkens; above 50%, it brightens.

---

## Parameters

![Videomancer front panel with Emboss loaded](/img/instruments/videomancer/emboss/emboss_control_panel.png)
*Videomancer's front panel with Emboss active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Depth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Depth** controls the amplitude of the emboss effect: how much the gradients are amplified before becoming visible. At 0%, the surface is perfectly flat (no gradient contribution). As Depth increases, subtle pixel-to-pixel brightness changes are magnified into visible highlights and shadows. Very high Depth values create an aggressive, high-contrast relief where even minor details cast dramatic shadows.

---

### Knob 2 — Light Ang

| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 90deg |

**Light Ang** selects the direction of the virtual light source from eight positions: East, Southeast, South, Southwest, West, Northwest, North, and Northeast. The light direction determines the sign combinations of the horizontal and vertical gradients: an East light creates highlights on right-facing edges and shadows on left-facing edges. Rotating the light around all eight positions creates a dramatic shift in the perceived three-dimensionality of the image.

:::tip
Try slowly sweeping Light Ang while the source video is static. The image appears to rotate in three dimensions as the light moves around it: a convincing illusion that a 2D video signal has become a physical surface.
:::

---

### Knob 3 — Bias

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bias** adds a DC offset to the entire embossed output. At 50%, the surface appears mid-gray in flat areas (no gradient). Below 50%, flat areas darken toward black; above 50%, they brighten toward white. Bias controls the overall "exposure" of the relief: the base brightness upon which the highlights and shadows are painted.

---

### Knob 4 — Sharpen

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Sharpen** boosts the edge gradients by adding a proportion of the raw gradient back into the depth-scaled result. At 0%, no additional sharpening. As Sharpen increases, edges become harder and more defined: useful for bringing out fine detail in low-contrast sources. At high values, the effect can become visually aggressive.

---

### Knob 5 — Metal Tnt

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Metal Tnt** applies a metallic color tint to the embossed surface when Color is set to Source. The tint shifts the U channel positive and the V channel negative proportionally to the Y value (brightness), creating a warm metallic cast that's stronger in bright areas and weaker in shadows: mimicking the color behavior of a polished metal surface catching warm light.

---

### Knob 6 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contrast** stretches the embossed output around mid-gray (512). At 50%, contrast is unity. Above 50%, the highlights are pushed brighter and shadows deeper, increasing the perceived depth of the relief. Below 50%, contrast is reduced (the relief becomes flatter and more subtle.)

---

### Switch 7 — Style

| Property | Value |
|----------|-------|
| Off | Raised |
| On | Carved |
| Default | Raised |

**Style** selects between **Raised** and **Carved** relief. Raised creates the appearance of a surface pushed outward (the default embossing direction). Carved inverts the gradient, making the surface appear pressed inward: like an intaglio engraving where the image is cut into the material rather than raised above it.

---

### Switch 8 — Color

| Property | Value |
|----------|-------|
| Off | Gray |
| On | Source |
| Default | Gray |

**Color** selects between **Gray** (monochrome) and **Source** (color-preserved) output. In Gray mode, the embossed output is achromatic: pure luminance relief with neutral chroma. In Source mode, the original U and V channels are passed through (optionally modified by Metal Tnt), so the relief surface retains the color of the original image.

---

### Switch 9 — Channel

| Property | Value |
|----------|-------|
| Off | Y Only |
| On | YUV |
| Default | Y Only |

**Channel** selects between **Y Only** and **YUV** processing scope. Currently, the emboss gradient computation is performed exclusively on the Y (luminance) channel regardless of this setting.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** flips the output luminance. With Invert **On**, highlights become shadows and shadows become highlights: equivalent to viewing the relief from behind the surface or reversing the light source direction.

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

**Mix** crossfades between the dry (unprocessed) signal and the wet (Emboss-processed) signal. At partial values, the emboss effect blends with the original video, which can create a detail-enhanced look: the edges from the emboss add subtle dimensional cues to the original image.

---

## Background

### Bas-relief and embossing

***Bas-relief*** (from the Italian ***basso-rilievo***, "low relief") is a sculptural technique where figures project slightly from a flat background. Unlike full three-dimensional sculpture, the depth is compressed: everything exists within a shallow layer. This compression makes bas-relief ideal for representing complex scenes on flat surfaces: coins, architectural friezes, and decorative metalwork. Digital embossing mimics this by extracting the edge information from an image and presenting it as a shallow surface lit from a single direction.

### Spatial gradients and edge detection

The mathematical foundation of embossing is the ***spatial gradient***: the rate of change of brightness across space. The horizontal gradient measures how brightness changes from left to right (computed by subtracting the previous pixel). The vertical gradient measures top-to-bottom change (computed by subtracting the previous scanline stored in a BRAM line buffer). These two gradients define a surface normal at each pixel: the direction the surface "faces." Combining them with a light direction vector determines whether each point is lit (highlight) or shadowed.

### The eight light directions

Traditional 2D emboss filters combine horizontal and vertical gradients in fixed proportions. Emboss extends this by offering eight selectable light positions: the four cardinal directions (North, South, East, West) and four diagonals (NE, SE, SW, NW). Each direction uses a specific sign combination of the H and V gradients:

- **East** (+H): highlights on right-facing edges
- **West** (−H): highlights on left-facing edges
- **South** (+V): highlights on downward-facing edges
- **North** (−V): highlights on upward-facing edges
- **Diagonals**: Average of two adjacent cardinal gradients


---

## Signal Flow

### Signal Flow Notes

The gradient computation uses a single pixel delay for horizontal comparison and a single BRAM line buffer for vertical comparison. This makes the gradients first-order (Sobel-like with a 1-pixel kernel), which gives clean, one-pixel-wide edge transitions. The directional combine selects from eight pre-defined gradient combinations using the three MSBs of the Light Ang pot, providing 45° angular resolution. The depth scaling is a signed multiply, and the bias offset is added afterward, so the bias does not affect the gradient amplitude (it only shifts the DC level.)


---

## Exercises

These exercises progress from a basic stone-carved relief to a metallic color emboss.
### Exercise 1: Stone Relief

![Stone Relief result](/img/instruments/videomancer/emboss/emboss_ex1_s1.png)
*Stone Relief — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic gray stone relief with Southeast lighting: the most familiar emboss look, like a carved architectural panel.

#### Key Concepts

- Bias sets the surface's neutral brightness
- Depth amplifies edge gradients
- Southeast lighting is the most natural for Western eyes (light from upper-left)

#### Video Source

A portrait, text, or any image with clear edges. High-contrast subjects with distinct outlines produce the most readable relief.

#### Steps

1. Set **Color** (Switch 8) to Gray for monochrome output.
2. Set **Light Ang** (Knob 2) to about 25% (approximately Southeast).
3. Set **Depth** (Knob 1) to about 50%.
4. Set **Bias** (Knob 3) to 50% (mid-gray neutral surface).
5. Set **Contrast** (Knob 6) to about 60% for slightly enhanced depth.
6. Observe edges appearing as light/shadow pairs (the image looks carved into stone.)

#### Settings

| Control | Value |
|---------|-------|
| Depth | ~50% |
| Light Ang | ~25% |
| Bias | ~50% |
| Sharpen | ~0% |
| Metal Tnt | ~0% |
| Contrast | ~60% |
| Style | Raised |
| Color | Gray |
| Channel | Y Only |
| Invert | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 2: Metallic Color Surface

![Metallic Color Surface result](/img/instruments/videomancer/emboss/emboss_ex2_s1.png)
*Metallic Color Surface — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A polished metal surface with warm color tinting: like a bronze relief panel where the original colors shimmer through the metallic surface.

#### Key Concepts

- Source color preserves the original chromatic information
- Metal Tnt adds a warm, brightness-dependent cast
- High contrast with partial mix creates a detail-enhanced look

#### Video Source

Video with visible color: landscapes, paint, fabric. The metallic tint interacts most dramatically with saturated sources.

#### Steps

1. Set **Color** to Source to preserve the original chroma.
2. Set **Depth** to about 40% and **Light Ang** to about 35% (approximately South-Southwest).
3. Set **Metal Tnt** (Knob 5) to about 60%. A warm metallic cast appears, stronger in highlights.
4. Set **Sharpen** (Knob 4) to about 30% for enhanced edge detail.
5. Reduce **Mix** to about 40%. The emboss blends with the original video, adding dimensional detail without losing the original image.

#### Settings

| Control | Value |
|---------|-------|
| Depth | ~40% |
| Light Ang | ~35% |
| Bias | ~50% |
| Sharpen | ~30% |
| Metal Tnt | ~60% |
| Contrast | ~50% |
| Style | Raised |
| Color | Source |
| Channel | Y Only |
| Invert | Off |
| Bypass | Off |
| Mix | ~40% |

---

### Exercise 3: Inverted Intaglio

![Inverted Intaglio result](/img/instruments/videomancer/emboss/emboss_ex3_s1.png)
*Inverted Intaglio — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An intaglio engraving where the image appears cut into the surface rather than raised above it (like a printing plate or carved seal.)

#### Key Concepts

- Carved style reverses the relief direction
- Invert swaps highlights and shadows
- Combining Carved + Invert creates a double-reversed look

#### Video Source

High-contrast subject with bold shapes: text, logos, or strong geometric patterns work well for an intaglio look.

#### Steps

1. Set **Style** (Switch 7) to Carved. The gradient is negated (previously raised areas become cut-in.)
2. Set **Depth** to about 70% for a deep carving.
3. Set **Bias** to about 55% (slightly brighter surface).
4. Set **Contrast** (Knob 6) to about 75% for dramatic depth.
5. Enable **Invert** (Switch 10). The highlight/shadow relationship inverts again: the combination of Carved + Invert creates a unique double-reversal that can look like a photographic print from an engraving plate.

#### Settings

| Control | Value |
|---------|-------|
| Depth | ~70% |
| Light Ang | ~25% |
| Bias | ~55% |
| Sharpen | ~0% |
| Metal Tnt | ~0% |
| Contrast | ~75% |
| Style | Carved |
| Color | Gray |
| Channel | Y Only |
| Invert | On |
| Bypass | Off |
| Mix | ~100% |

---
## Glossary

- **Bas-Relief**: A sculptural technique where figures project slightly from a flat background (the visual effect Emboss simulates.)

- **Gradient**: The rate of change of a value across space. Horizontal gradient compares left-to-right; vertical gradient compares top-to-bottom.

- **Intaglio**: The opposite of relief: an image cut into a surface rather than raised above it, used in printmaking and seal carving.

- **Light Direction**: The virtual angle from which the embossed surface is illuminated, determining which edges appear as highlights and which as shadows.

- **Line Buffer**: A BRAM memory storing the previous scanline's Y values for vertical gradient computation.

- **Spatial Frequency**: How rapidly brightness changes across the image: high spatial frequencies (fine detail) produce the strongest gradients.

---
