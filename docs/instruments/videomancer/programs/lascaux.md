---
draft: true
sidebar_position: 164
slug: /instruments/videomancer/lascaux
title: "Lascaux"
image: /img/instruments/videomancer/lascaux/lascaux_hero_s1.png
description: "Thirty-two thousand years ago, artists crouched in the darkness of limestone caves and painted animals, handprints, and abstract symbols onto rough stone walls using nothing but mineral pigments and firelight."
---

![Lascaux hero image](/img/instruments/videomancer/lascaux/lascaux_hero_s1.png)
*Lascaux rendering a live camera feed as a torchlit Paleolithic cave painting with earth-tone pigments and charcoal contour lines scored into rough stone.*

---

## Overview

**Lascaux** transforms any video signal into a Paleolithic cave painting. Your input is recast through a four-pigment earth-tone palette derived from the mineral pigments found in actual prehistoric art, dark charcoal contour lines are etched over the image, and a rough stone surface texture is applied beneath the paint. An animated torch casts a circle of warm light across the cave wall, dimming the surrounding stone to near-darkness. The result is something that looks like it was painted by firelight onto limestone thirty thousand years ago (and then discovered yesterday.)

At gentle settings, Lascaux adds a warm, weathered quality to footage: like a candlelit oil painting on rough canvas. At extreme settings, it reduces the image to stark charcoal outlines scratched onto flickering stone, barely visible outside the torch's narrow cone. Every control pushes the image deeper into the cave.

:::tip
***The torch is the signature effect.*** It's not a simple vignette: the torch drifts across the frame, its flame flickers randomly, and the darkness actually desaturates the color channels. When you turn it on and crank the radius down, it feels like you're holding a real torch in a real cave.
:::

### What's In a Name?

The name ***Lascaux*** refers to the cave complex in southwestern France's Dordogne region discovered in 1940, famous for its Paleolithic paintings dating to approximately 17,000 BC. The Hall of the Bulls at Lascaux contains some of the finest examples of prehistoric art ever found: large-scale animal figures rendered in mineral pigments on limestone walls. This program recreates the material qualities of that art: the ochre and sienna palette, the charcoal contour drawing, the rough stone substrate, and the flickering torchlight that would have been the only way to see it.

---

## Quick Start

1. Feed any video signal into Videomancer and load **Lascaux**. Your image immediately shifts into warm earth tones: the mineral pigment palette replaces the original colors. You're painting on cave walls now.
2. Turn **Contour Wt** (Knob 3) clockwise. Dark charcoal outlines appear along edges in the image, as if someone traced the shapes with a burnt stick. The heavier the weight, the thicker and darker the outlines.
3. Turn **Torch Radius** (Knob 4) down to about 40%. A circle of light appears on the cave wall, dimming everything outside its reach. Watch the torch drift slowly across the frame (it's alive.)
4. Increase **Flicker** (Knob 6). The torch flame becomes unsteady, and the light intensity pulses randomly. The cave breathes.

---

## Parameters

![Videomancer front panel with Lascaux loaded](/img/instruments/videomancer/lascaux/lascaux_control_panel.png)
*Videomancer's front panel with Lascaux active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Torch Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Torch Speed** controls how quickly the torch drifts across the cave wall. The torch position is driven by a pair of ***direct digital synthesis*** oscillators: one for horizontal drift and one for vertical: tracing a slow, looping figure on the frame. At the minimum setting, the torch barely moves: it creeps across the wall almost imperceptibly. As you turn the knob clockwise, the drift speed increases, and the torch traces its path more quickly. At maximum, the torch sweeps briskly across the image.

:::note
If **Torch Lock** (Switch 10) is set to **Center**, Torch Speed has no visible effect: the torch is pinned to the center of the frame regardless of this setting.
:::

---

### Knob 2 — Pigments

| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 2 |

**Pigments** selects how many of the four mineral pigments are active in the ***palette quantization*** stage. Lascaux classifies every input pixel by calculating the ***Manhattan distance*** in YUV color space to each pigment and snapping to the nearest match. At the lowest setting, only two pigments are available: charcoal black and yellow ochre. Adding a third pigment introduces red ochre. At the maximum setting, all four pigments are active: charcoal, yellow ochre, red ochre, and raw sienna: providing the richest earth-tone palette. Fewer pigments produce starker, more graphic results; more pigments produce subtler tonal gradation.

---

### Knob 3 — Contour Wt

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contour Wt** controls the darkness of the charcoal contour lines overlaid on the palette-quantized image. The contour detector measures brightness differences between neighboring pixels: both horizontally (pixel to pixel) and vertically (line to line, using a ***BRAM line buffer***): and darkens the output proportionally. At the minimum setting, no contour darkening is applied. As you increase the weight, edges in the image are progressively outlined in dark charcoal. At maximum, even subtle edges produce heavy black lines, and the image takes on the look of a charcoal rubbing.

:::tip
Contour extraction traces the ***luminance*** channel of the original input, not the palette-quantized output. This means contours respond to fine detail in the source even when the palette has reduced the image to a few flat tones.
:::

---

### Knob 4 — Torch Radius

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Torch Radius** sets the size of the illuminated area around the torch. The torch applies a radial brightness falloff based on ***Manhattan distance*** from the torch center: pixels inside the radius are bright, and pixels outside the radius drop to a dim ambient level. At the minimum setting, the torch illuminates only a small spot. At maximum, the torch floods most of the frame with light. A large radius creates a gentle vignette; a small radius turns the program into a focused spotlight on the cave wall.

---

### Knob 5 — Stone Grain

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Stone Grain** controls the roughness of the simulated stone surface. A ***linear feedback shift register*** generates pseudo-random noise that is mixed into the luminance channel, producing a gritty, granular texture. At the minimum setting, the stone surface is smooth: no grain is visible. As you increase the knob, the surface becomes progressively rougher, with pixel-level noise that simulates the irregular texture of limestone or basalt. At maximum, the grain is heavy and dominant, obscuring fine image detail beneath a thick layer of rock texture.

---

### Knob 6 — Flicker

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Flicker** controls how much the torch flame intensity varies from frame to frame. The LFSR noise source modulates the torch brightness on every vertical sync pulse, creating a random intensity wobble that simulates the unsteady light of an open flame. At the minimum setting, the torch burns steadily with no variation. As you increase the knob, the light becomes more erratic: the flame gutters and surges. At maximum, the torch swings between near-darkness and bright flare, producing a dramatic, unsettling strobe.

:::warning
High flicker combined with a small torch radius can produce rapid brightness changes. Use caution for photosensitive viewers.
:::

---

### Switch 7 — Cave Type

| Property | Value |
|----------|-------|
| Off | Limestone |
| On | Basalt |
| Default | Limestone |

**Cave Type** selects the color of the stone surface. **Limestone** produces warm, yellowish cave walls with a subtle amber tint: the classic look of the Lascaux and Altamira caves. **Basalt** produces cool, neutral gray walls reminiscent of volcanic rock formations. The cave type affects both the grain texture tint and the stone color visible in **Edges Only** mode. Limestone is warmer; basalt is cooler and more austere.

---

### Switch 8 — Torch Color

| Property | Value |
|----------|-------|
| Off | Fat Lamp |
| On | Pine Resin |
| Default | Fat Lamp |

**Torch Color** selects the character of the torch illumination. **Fat Lamp** simulates a ***wick lamp*** burning animal fat: the type of lamp found in Lascaux, producing a warm, steady amber glow. **Pine Resin** simulates a resinous torch: brighter and more volatile, with a cooler, smokier quality.

---

### Switch 9 — Edges Only

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Edges Only** switches the program into a pure contour drawing mode. When enabled, the palette quantization and pigment coloring are bypassed: the output shows only the charcoal contour lines drawn on a plain stone background. Edges above a fixed threshold appear as dark charcoal; everything else is rendered as bare stone in the selected **Cave Type** color. This mode produces stark, graphic results that look like cave wall etchings or charcoal sketches.

---

### Switch 10 — Torch Lock

| Property | Value |
|----------|-------|
| Off | Drift |
| On | Center |
| Default | Drift |

**Torch Lock** controls whether the torch drifts or stays fixed. In **Drift** mode, the torch position is animated by the DDS oscillators, tracing a slow figure across the frame at a speed set by **Torch Speed** (Knob 1). In **Center** mode, the torch is locked to the center of the frame and does not move. Center mode is useful when you want a stable vignette or when the torch drift would be distracting.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Lascaux processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the cave painting effect.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the crossfade between the dry (unprocessed) input and the wet (fully processed) cave painting output. At the minimum setting, you hear only the dry signal: the original video passes through unchanged. At maximum, the output is entirely the processed cave painting. Intermediate values blend the two, allowing you to dial in a subtle warmth or weathering effect without committing to the full prehistoric treatment.

---

## Background

### Paleolithic cave painting

The cave paintings at Lascaux, Altamira, and Chauvet are among the oldest known works of art, dating from roughly 32,000 to 15,000 BC. Prehistoric artists worked with a limited palette of mineral pigments: charcoal and ***manganese dioxide*** for black, ***goethite*** for yellow ochre, ***haematite*** for red ochre, and various iron oxides for earth browns. These pigments were ground, mixed with animal fat or water, and applied to cave walls using fingers, fur pads, and reed brushes. Outlines were drawn with sticks of charcoal or manganese crayons.

Lascaux's four-pigment palette is modeled on ***spectroscopic analysis*** of actual paint samples recovered from the Lascaux cave complex. The program maps every input pixel to the perceptually nearest pigment using Manhattan distance in YUV color space: a computationally efficient approximation of color similarity.

### Edge detection and contour drawing

The charcoal contour lines in Lascaux are generated by a simple ***gradient magnitude*** edge detector. For each pixel, the detector computes two differences: the horizontal gradient (brightness difference between the current pixel and the previous pixel on the same line) and the vertical gradient (brightness difference between the current pixel and the same position on the previous line, stored in a BRAM line buffer). The sum of these two gradients approximates the edge strength at each point.

This result is scaled by the **Contour Wt** parameter and subtracted from the palette-quantized luminance, darkening edges proportionally. The technique is similar to a ***Sobel filter*** but simplified to use absolute differences rather than convolution kernels, saving FPGA resources while still producing visually convincing outlines.

### Torch illumination and radial falloff

The torch simulation combines three elements: position animation, radial brightness falloff, and random flicker. The torch position is driven by two DDS phase accumulators: one for horizontal motion (cosine) and one for vertical motion (sine): each looking up a 32-entry waveform table. This produces a smooth, looping trajectory across the frame.

Brightness at each pixel is determined by Manhattan distance from the torch center. Pixels inside the torch radius receive brightness proportional to their proximity; pixels outside the radius receive a low ambient value (approximately 3% of full scale), simulating distant cave darkness. Finally, the torch brightness is modulated per frame by an LFSR-generated random value, producing a natural flame flicker.

In the darkest regions, the program also desaturates the color channels by pulling U and V toward neutral. This simulates the way human vision loses color perception in low light (a phenomenon called ***scotopic vision***.)


---

## Signal Flow

### Signal Flow Notes

Three key interactions define Lascaux's visual character:

1. **Palette before contour**: The edge detector in stage 2 operates on the ***original*** input luminance (stored as `s_orig_y_s1`), not the palette-quantized output. This means contours track the source image detail even when the palette has flattened the tonal range to just two or three pigments. The contour darkness is then subtracted from the palette output, overlaying fine charcoal lines onto coarse pigment blocks.

2. **Stone tint on color channels**: Stage 3 doesn't just add grain to luminance: it also blends the U and V channels 75% toward the cave surface color constant (limestone warm amber or basalt cool gray). This pulls all colors toward a unified stone palette, reinforcing the material illusion.

3. **Torch desaturation**: In stage 4b, the torch brightness multiplies Y directly, but U and V are offset from neutral (512) before multiplication and then re-centered. In dark areas (low light value), this collapses U/V toward neutral, simulating the loss of color perception in dim light. The result is that only the torchlit region retains vivid pigment color; the surrounding darkness fades to warm gray.

:::tip
**Order matters.** Palette quantization sees the original input colors. Contour extraction sees original luminance. Stone grain and torch lighting see the palette output. This means changes to **Pigments** affect the colors you see, but not the contour lines (those always follow the source detail.)
:::


---

## Exercises

These exercises progress from basic palette restriction to full cave painting simulation, gradually engaging more of the processing chain. Each one builds on the previous, layering effects until the image looks like it was painted thirty millennia ago.
### Exercise 1: Earth-Tone Palette

![Earth-Tone Palette result](/img/instruments/videomancer/lascaux/lascaux_ex1_s1.png)
*Earth-Tone Palette — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A warm, posterized image rendered in mineral pigments with subtle charcoal outlines (like an illustrated plate from an archaeology book.)

#### Key Concepts

- Palette quantization snaps every pixel to its nearest pigment
- Fewer pigments produce bolder, more graphic results
- Contour lines overlay the palette with charcoal edge darkening

#### Video Source

A live camera feed or recorded footage with recognizable subjects and moderate contrast. Faces, plants, or animals work well because the pigment palette emphasizes warm skin tones and organic shapes.

#### Steps

1. Load **Lascaux** and set **Mix** (Fader 12) to maximum. The image shifts immediately into earth tones.
2. Turn **Pigments** (Knob 2) fully counter-clockwise. Only two pigments are active: charcoal black and yellow ochre. The image becomes a stark two-tone graphic.
3. Slowly turn Pigments clockwise to add red ochre, then raw sienna. Watch the image gain warmth and tonal nuance as more pigments join the palette.
4. Increase **Contour Wt** (Knob 3) to about 50%. Dark charcoal lines appear along edges, defining the shapes in the image.
5. Toggle **Cave Type** (Switch 7) between **Limestone** and **Basalt**. The underlying stone tint shifts between warm amber and cool gray.

#### Settings

| Control | Value |
|---------|-------|
| Torch Speed | 25% |
| Pigments | 3 (step 3 of 4) |
| Contour Wt | 50% |
| Torch Radius | 100% |
| Stone Grain | 0% |
| Flicker | 0% |
| Cave Type | Limestone |
| Torch Color | Fat Lamp |
| Edges Only | Off |
| Torch Lock | Center |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Torchlit Stone

![Torchlit Stone result](/img/instruments/videomancer/lascaux/lascaux_ex2_s1.png)
*Torchlit Stone — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A cave painting illuminated by a wandering torch: bright warm color in the spotlight, fading to dark gray stone in the periphery.

#### Key Concepts

- The torch applies radial brightness falloff from a drifting center point
- Flicker randomizes torch intensity per frame
- Darkness desaturates the color channels toward neutral

#### Video Source

High-contrast footage with strong shapes: dancers, architecture, or geometric patterns. The torch spotlight isolates and reveals portions of the image as it drifts.

#### Steps

1. Start from the Exercise 1 settings. Ensure **Pigments** is at step 3 or 4 and **Contour Wt** is at about 50%.
2. Set **Torch Lock** (Switch 10) to **Drift** and turn **Torch Radius** (Knob 4) down to about 40%. A cone of light appears, and the surrounding image dims to near-darkness.
3. Increase **Torch Speed** (Knob 1) to about 30%. The torch begins drifting across the frame, illuminating different parts of the painting as it moves.
4. Turn up **Flicker** (Knob 6) to about 40%. The torch flame becomes unsteady, pulsing and guttering randomly.
5. Increase **Stone Grain** (Knob 5) to about 30%. The stone surface becomes visibly rough, especially in the torchlit area where you can see the grain texture clearly.
6. Watch the periphery of the torch radius. Notice how the color drains from the image in the dim areas (only the spotlight region retains full pigment saturation.)

#### Settings

| Control | Value |
|---------|-------|
| Torch Speed | 30% |
| Pigments | 3 (step 3 of 4) |
| Contour Wt | 50% |
| Torch Radius | 40% |
| Stone Grain | 30% |
| Flicker | 40% |
| Cave Type | Limestone |
| Torch Color | Fat Lamp |
| Edges Only | Off |
| Torch Lock | Drift |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Charcoal Etching

![Charcoal Etching result](/img/instruments/videomancer/lascaux/lascaux_ex3_s1.png)
*Charcoal Etching — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A stark charcoal drawing etched into rough stone, illuminated by a flickering pine resin torch: the kind of image archaeologists might find deep in a cave chamber.

#### Key Concepts

- Edges Only mode bypasses palette quantization and shows pure contour lines
- Stone grain adds texture to the bare stone background
- Cave Type and torch work together to create atmosphere

#### Video Source

Footage with strong, distinct edges: silhouettes, architectural details, text, or high-contrast line art. Subjects with clear outlines produce the best charcoal etchings.

#### Steps

1. Enable **Edges Only** (Switch 9). The image strips down to pure contour lines on a stone background. Only the edge information remains.
2. Set **Contour Wt** (Knob 3) to about 60%. The charcoal lines become bold and dark.
3. Set **Cave Type** (Switch 7) to **Basalt** and increase **Stone Grain** (Knob 5) to about 50%. The background becomes rough, cool gray stone with visible granular texture.
4. Set **Torch Color** (Switch 8) to **Pine Resin** for a cooler, smokier light.
5. Set **Torch Radius** (Knob 4) to about 35% and **Torch Lock** to **Drift**. The torch wanders across the stone face, revealing sections of the charcoal drawing as it passes.
6. Increase **Flicker** (Knob 6) to about 60%. The torch gutters and surges, making the drawing appear and disappear in rhythmic pulses.
7. Slowly reduce **Torch Speed** (Knob 1) until the torch barely moves. The scene becomes meditative: a single guttering flame, a stone wall, and ancient marks slowly emerging from darkness.

#### Settings

| Control | Value |
|---------|-------|
| Torch Speed | 10% |
| Pigments | 3 (step 3 of 4) |
| Contour Wt | 60% |
| Torch Radius | 35% |
| Stone Grain | 50% |
| Flicker | 60% |
| Cave Type | Basalt |
| Torch Color | Pine Resin |
| Edges Only | On |
| Torch Lock | Drift |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **BRAM**: Block RAM; a dedicated memory tile on the FPGA used here to store one scanline of luminance for vertical edge detection

- **DDS**: Direct Digital Synthesis; a technique for generating waveforms by stepping through a lookup table at a controlled rate, used here to animate the torch position

- **Goethite**: An iron oxyhydroxide mineral (FeOOH) that produces yellow ochre pigment, one of the primary colors used in Paleolithic cave art

- **Haematite**: An iron oxide mineral (Fe₂O₃) that produces red ochre pigment, widely used in prehistoric painting and body decoration

- **LFSR**: Linear Feedback Shift Register; a digital circuit that generates a pseudo-random bit sequence, used here for stone grain noise and torch flicker

- **Manhattan distance**: A distance metric that sums the absolute differences along each axis, used here to classify pixels to their nearest palette pigment and to compute torch falloff

- **Palette quantization**: The process of mapping each pixel's color to the nearest entry in a restricted set of allowed colors, reducing the image to a fixed palette

- **Scotopic vision**: Human visual perception in low-light conditions, characterized by loss of color sensitivity; simulated here by the torch's desaturation of U/V channels in darkness

- **Sobel filter**: An edge detection algorithm that computes image gradients using convolution kernels; Lascaux uses a simplified variant based on absolute pixel differences

---
