---
draft: true
sidebar_position: 269
slug: /instruments/videomancer/silhouette
title: "Silhouette"
image: /img/instruments/videomancer/silhouette/silhouette_hero_s1.png
description: "Every image is a landscape of brightness and colour values."
---

![Silhouette hero image](/img/instruments/videomancer/silhouette/silhouette_hero_s1.png)
*Silhouette keying a dancer against a flat-color matte: the figure's outline cut cleanly from the background, replaced by a solid wash of color.*

---

## Overview

**Silhouette** is a ***video keyer***: a tool that separates a video image into two regions (the subject and the background) and replaces one region with a flat matte color. It can key on ***luminance*** (brightness) or ***chrominance*** (color), with adjustable threshold, softness, and gain controls that determine how precisely the boundary is drawn. The areas identified as "keyed" are replaced by a user-defined matte color, while the non-keyed areas retain the original video.

Unlike a simple hard cut, Silhouette generates a smooth ***key alpha*** signal that controls the blend between source video and matte color. The Span parameter softens the key edge, creating a gentle transition rather than a hard border. The Gain control amplifies the key signal to tighten or loosen the selection, and a 16× gain range mode allows extreme precision for subtle keying tasks. The result is a flexible compositing tool that can produce everything from hard graphic silhouettes to soft, feathered mattes.

### What's In a Name?

***Silhouette*** refers to the art of cutting a person's profile from black paper, named after Étienne de Silhouette, the eighteenth-century French finance minister whose hobby of paper-cutting gave the term its lasting meaning. The program transforms video into a similar binary visual statement: subject versus background, figure versus ground: where the original image is distilled into a matte cutout.

---

## Quick Start

1. Feed a video source into Videomancer with **Silhouette** loaded. At default settings, the image appears mostly unchanged.
2. Set **Key Type** (Switch 7) to Luma. The keyer will now evaluate brightness.
3. Adjust **Threshold Y/U** (Knob 2) to about 50%. Areas near this brightness level begin to be replaced by the matte color.
4. Increase **Span** (Knob 1) to about 70%. A wider range of brightness values around the threshold is now keyed, and the transition between keyed and unkeyed areas is softer.

---

## Parameters

![Videomancer front panel with Silhouette loaded](/img/instruments/videomancer/silhouette/silhouette_control_panel.png)
*Videomancer's front panel with Silhouette active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Span

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Span** controls the width and softness of the key transition. At 0%, the key has a very narrow, hard transition: only pixels very close to the threshold are keyed. As Span increases, the transition zone widens, creating a softer edge. At maximum, the key is very broad and permissive, with a long gradual fade between fully keyed and fully unkeyed regions. Mathematically, Span sets a clip level: the raw distance from the threshold must exceed (max − Span) before any key signal is generated.

:::note
Span and Key Gain (Fader 12) work together. Span determines the width of the transition zone; Key Gain determines how quickly the key signal ramps up within that zone. A wide Span with high Gain creates a broad but sharp key. A narrow Span with low Gain creates a subtle, localized effect.
:::

---

### Knob 2 — Threshold Y/U

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Threshold Y/U** sets the reference point for the key. In Luma mode, this is the brightness value that forms the center of the key region: pixels near this brightness are keyed. In Chroma mode, this same value is used as the threshold for both the Y and U channels: pixels whose U value is near the threshold are candidates for keying. Adjusting this knob "slides" the key region up or down the brightness or color scale.

---

### Knob 3 — Threshold V

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Threshold V** sets the reference point for the V (red-cyan) channel in Chroma key mode. Pixels whose V value is near this threshold contribute to the chroma key signal. In Luma mode, this control has no effect. Together with Threshold Y/U, the two threshold knobs define a rectangular region in U/V color space that is keyed.

---

### Knob 4 — Y Matte

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Y Matte** sets the luminance (brightness) of the matte replacement color. Keyed pixels are replaced by this brightness value. At 0%, the matte is black; at 100%, white. Combined with U Matte and V Matte, you can create any solid color for the keyed regions.

---

### Knob 5 — U Matte

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**U Matte** sets the U (blue-yellow) chroma component of the matte replacement color. At 50% (center), the matte has no blue-yellow tint. Below 50%, the matte shifts yellow; above 50%, toward blue.

---

### Knob 6 — V Matte

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**V Matte** sets the V (red-cyan) chroma component of the matte replacement color. At 50% (center), the matte has no red-cyan tint. Below 50%, the matte shifts cyan; above 50%, toward red.

:::tip
To create specific matte colors: black (Y=0%, U=50%, V=50%), white (Y=100%, U=50%, V=50%), red (Y~50%, U~30%, V~80%), blue (Y~30%, U~80%, V~30%), green (Y~60%, U~30%, V~30%). Experiment with combinations (precise placement depends on the YUV color space.)
:::

---

### Switch 7 — Key Type

| Property | Value |
|----------|-------|
| Off | Luma |
| On | Chroma |
| Default | Luma |

**Key Type** selects the keying mode. **Luma** keys on brightness: the absolute difference between pixel brightness and the Threshold Y/U value determines whether the pixel is keyed. **Chroma** keys on color: the maximum of the |U − threshold| and |V − threshold| distances determines the key. Luma keying is best for separating bright from dark areas; Chroma keying is best for isolating specific colors.

---

### Switch 8 — Key Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Key Invert** reverses which pixels are keyed and which pass through. With Key Invert **Off**, pixels near the threshold are replaced by the matte color. With Key Invert **On**, pixels near the threshold pass through and everything else becomes the matte color (the keyed and unkeyed regions swap.)

---

### Switch 9 — Gain Range

| Property | Value |
|----------|-------|
| Off | 1x |
| On | 16x |
| Default | 1x |

**Gain Range** selects between **1×** and **16×** gain scaling for the key signal. In 1× mode, the Key Gain fader provides a gain range of 0.0 to 1.0: suitable for most keying tasks. In 16× mode, the gain range extends to 0.0 to 16.0, allowing very narrow key transitions to be amplified into hard cuts. Use 16× mode when you need a very precise, tight key with minimal feathering.

---

### Switch 10 — Luma Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Luma Invert** inverts the input luminance before key distance computation. With Luma Invert **On**, the keyer treats dark areas as bright and vice versa. This effectively flips the keying relationship: useful when you want to key on shadows rather than highlights without changing the threshold position.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output.

---

### Fader 12 — Key Gain

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Key Gain** is the master gain for the key alpha signal. The raw key distance is multiplied by this value. At 0%, no keying occurs (alpha always zero, everything becomes matte). At 100%, the full key signal reaches the interpolator. Reducing Key Gain softens and narrows the key effect; increasing it tightens and hardens the key edge.

---

## Background

### Video keying fundamentals

***Keying*** is the compositing technique of replacing part of a video image with another image or solid color, based on a specific property of the original pixels. The two most common types are ***luminance keying*** (selecting pixels by brightness) and ***chroma keying*** (selecting pixels by color: the technology behind green screen and blue screen effects). Silhouette implements both, allowing the artist to isolate elements by brightness, color, or a combination.

### The key alpha signal

The heart of any keyer is the ***alpha*** signal: a per-pixel value between 0 and 1 (or in Silhouette's 10-bit system, 0 and 1023) that determines how much of the source video versus the replacement matte is shown. An alpha of 0 means full matte (the pixel is completely keyed). An alpha of 1023 means full source (the pixel is completely unkeyed). Values in between create a blend: a soft, feathered transition at the edges of the keyed region.

### Soft keying with span and gain

A simple threshold key creates hard, jaggy edges. Silhouette softens this with two controls. ***Span*** sets a clip level: the raw distance from the threshold must exceed this clip before any key signal is generated, creating a dead zone that prevents noise from triggering the key. Once outside the dead zone, the distance is multiplied by ***Key Gain*** and clamped to the 0–1023 range. Together, Span and Gain form a transfer curve: Span shifts the curve horizontally (when the key starts), and Gain controls the curve's slope (how quickly it transitions from fully keyed to fully unkeyed).


---

## Signal Flow

### Signal Flow Notes

The keyer generates the alpha signal in 5 pipeline stages (5 clocks), and the source video is delayed by 4 clocks internally to align with the alpha at the interpolator input. The interpolator then takes 4 additional clocks, bringing the total pipeline latency to 9 clocks. Note that the interpolator blends matte (shown when alpha = 0, keyed region) with source (shown when alpha = max, unkeyed region). In chroma mode, the key distance uses the maximum of the U and V differences (rather than the sum), which creates a square selection region in U/V space rather than a circular one (sufficient for most video keying applications.)


---

## Exercises

These exercises progress from a basic luma key to a chroma key with soft edges.
### Exercise 1: Hard Luma Silhouette

![Hard Luma Silhouette result](/img/instruments/videomancer/silhouette/silhouette_ex1_s1.png)
*Hard Luma Silhouette — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A stark black silhouette on a white matte background (a classic paper-cutout look.)

#### Key Concepts

- Luma keying separates bright from dark regions
- A tight key creates a hard-edged graphic silhouette
- The matte color fills the keyed area

#### Video Source

A subject lit against a contrasting background. A bright background with a darker subject, or vice versa.

#### Steps

1. Set **Key Type** (Switch 7) to Luma.
2. Set **Threshold Y/U** (Knob 2) to a value between the subject and background brightness.
3. Set **Span** (Knob 1) to about 70% for a wide key zone.
4. Set **Key Gain** (Fader 12) to about 80%.
5. Set the matte to white: **Y Matte** (Knob 4) = 100%, **U Matte** (Knob 5) = 50%, **V Matte** (Knob 6) = 50%.
6. The darker subject areas become the silhouette (source video passes through); the lighter background is replaced by white matte.

#### Settings

| Control | Value |
|---------|-------|
| Span | ~70% |
| Threshold Y/U | ~50% |
| Threshold V | ~50% |
| Y Matte | ~100% |
| U Matte | ~50% |
| V Matte | ~50% |
| Key Type | Luma |
| Key Invert | Off |
| Gain Range | 1x |
| Luma Invert | Off |
| Bypass | Off |
| Key Gain | ~80% |

---

### Exercise 2: Soft Chroma Matte

![Soft Chroma Matte result](/img/instruments/videomancer/silhouette/silhouette_ex2_s1.png)
*Soft Chroma Matte — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A soft-edged chroma key that replaces a specific color range with a colored matte (like a gentle chromakey compositing effect.)

#### Key Concepts

- Chroma keying isolates pixels by color rather than brightness
- Span controls the softness of the key transition
- Two threshold controls define the target color region in U/V space

#### Video Source

Video with a distinct color region: a colored wall, fabric, or any saturated area. Green or blue backgrounds work best for traditional chroma key.

#### Steps

1. Set **Key Type** to Chroma.
2. Set **Threshold Y/U** (Knob 2) and **Threshold V** (Knob 3) to match the target color's position in U/V space.
3. Set **Span** to about 60% for a moderately soft key edge.
4. Set **Key Gain** to about 70%.
5. Set the matte to a complementary color: adjust **Y Matte**, **U Matte**, **V Matte** to taste.
6. The matched color area is replaced by the matte color with a soft, feathered transition.

#### Settings

| Control | Value |
|---------|-------|
| Span | ~60% |
| Threshold Y/U | ~60% |
| Threshold V | ~80% |
| Y Matte | ~50% |
| U Matte | ~30% |
| V Matte | ~30% |
| Key Type | Chroma |
| Key Invert | Off |
| Gain Range | 1x |
| Luma Invert | Off |
| Bypass | Off |
| Key Gain | ~70% |

---

### Exercise 3: Inverted Key with 16× Precision

![Inverted Key with 16× Precision result](/img/instruments/videomancer/silhouette/silhouette_ex3_s1.png)
*Inverted Key with 16× Precision — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A precision-keyed image where a narrow brightness band is preserved while everything else becomes matte (an inverted key isolating a specific tonal range.)

#### Key Concepts

- Key Invert swaps keyed and unkeyed regions
- 16× gain range allows extremely precise key edges
- Luma Invert pre-processes the input for shadow keying

#### Video Source

An image with a wide tonal range: the narrow isolated band will appear as a "slice" of the original brightness.

#### Steps

1. Set **Key Type** to Luma and **Key Invert** (Switch 8) to On.
2. Set **Threshold Y/U** to about 50% (mid-brightness target).
3. Set **Span** to about 30% for a narrow selection.
4. Set **Gain Range** (Switch 9) to 16× and **Key Gain** to about 40%.
5. Set the matte to black: **Y Matte** = 0%, **U Matte** = 50%, **V Matte** = 50%.
6. A narrow band of mid-brightness pixels passes through; everything else is replaced by black matte.

#### Settings

| Control | Value |
|---------|-------|
| Span | ~30% |
| Threshold Y/U | ~50% |
| Threshold V | ~50% |
| Y Matte | ~0% |
| U Matte | ~50% |
| V Matte | ~50% |
| Key Type | Luma |
| Key Invert | On |
| Gain Range | 16x |
| Luma Invert | Off |
| Bypass | Off |
| Key Gain | ~40% |

---
## Glossary

- **Alpha**: A per-pixel value (0–1023) controlling the blend between source video and matte color. Zero = full matte; 1023 = full source.

- **Chroma Key**: A keying technique that selects pixels based on their color (U and V channels) rather than their brightness.

- **Feathering**: The gradual transition between keyed and unkeyed regions, controlled by Span and Key Gain.

- **Key Signal**: The computed per-pixel value that determines what is keyed and what passes through.

- **Luminance Key**: A keying technique that selects pixels based on their brightness (Y channel).

- **Matte**: The replacement color displayed in keyed regions. In film compositing, a matte is any mask used to combine image elements.

- **Threshold**: The reference value around which the key is evaluated. Pixels near the threshold are candidates for keying.

---
