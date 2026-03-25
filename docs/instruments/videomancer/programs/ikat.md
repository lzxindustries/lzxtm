---
draft: true
sidebar_position: 141
slug: /instruments/videomancer/ikat
title: "Ikat"
image: /img/instruments/videomancer/ikat/ikat_hero_s1.png
description: "Ikat simulates the ancient resist-dyeing technique of the same name by dividing the video frame into vertical (or horizontal) stripe columns and processing each column as if it were a bundle of warp threads dipped into a dye bath."
---

![Ikat hero image](/img/instruments/videomancer/ikat/ikat_hero_s1.png)
*Ikat transforming a live video feed into resist-dyed textile stripes with quantized color columns, feathered dye-bleed edges, and LFSR grain.*

---

## Overview

**Ikat** simulates the ancient textile dyeing technique of the same name, transforming video into a woven fabric of quantized color stripes. The screen becomes a loom: the image is divided into vertical (or horizontal) columns, each column's luminance is reduced to a limited palette of tones, and the boundaries between columns blur with pseudo-random jitter: just as real dye bleeds past the edges of tightly tied threads.

At subtle settings, Ikat adds a gentle woven texture to any source, softening hard edges into organic, fabric-like transitions. At extreme settings, the image collapses into bold bands of flat color separated by ragged, jittering seams. The effect evokes hand-dyed silk, traditional batik cloth, and the imperfect beauty of artisan craft.

:::note
Ikat is a ***processing*** program: it transforms an incoming video signal. Feed it camera footage, pattern generators, or the output of other Videomancer programs for the richest results.
:::

### What's In a Name?

***Ikat*** is a Malay-Indonesian word meaning "to tie" or "to bind." It names a family of dyeing techniques practiced across Southeast Asia, Central Asia, Japan, and Latin America for centuries. In traditional ikat, artisans tightly bind sections of yarn with resist material before submerging the yarn in dye. The bound sections resist the dye, creating patterns where color and bare thread alternate. Because the bindings are never perfectly tight, dye bleeds slightly past the edges, producing the characteristic feathered boundaries that distinguish ikat from printed fabric. This Videomancer program recreates that imperfect resist process digitally: columns of pixels are "tied" into quantized bands, and pseudo-random jitter blurs their edges just as dye seeps past thread bindings.

---

## Quick Start

1. Feed a video source with visible detail and color variation. Turn **Col Width** (Knob 1) clockwise to create narrow vertical stripes across the image. The source breaks into columns of quantized color.
2. Increase **Bleed Amt** (Knob 2). The hard edges between columns soften as color bleeds between adjacent stripes (dye seeping past resist boundaries.)
3. Lower **Palette** (Knob 3) to reduce the number of tonal levels within each column. The image simplifies into bold, flat bands of color, like cloth dipped in a limited number of dye baths.
4. Raise **Dye Depth** (Knob 5) to inject LFSR jitter into the luminance channel. The column edges become ragged and organic rather than perfectly straight, completing the hand-dyed illusion.

---

## Parameters

![Videomancer front panel with Ikat loaded](/img/instruments/videomancer/ikat/ikat_control_panel.png)
*Videomancer's front panel with Ikat active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Col Width

| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 7 |

**Col Width** sets the width of each color column. The image is divided into stripes whose widths are always powers of two: 4, 8, 16, 32, or 64 pixels: so the boundaries snap between discrete sizes as you turn the knob. At the narrowest setting, the image is sliced into many thin stripes that preserve fine detail. At the widest, broad columns of uniform color dominate the frame, each one a wide swatch of dyed fabric.

:::tip
Because column widths are powers of two, there are only five distinct stripe sizes rather than a continuous sweep. Listen for the visual "clicks" as the pattern snaps between widths.
:::

---

### Knob 2 — Bleed Amt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Bleed Amt** controls how much color bleeds across column boundaries. At zero, each column is a crisp, hard-edged stripe. As bleed increases, the chroma channels fade toward neutral gray at the edges of each column, simulating dye that has seeped past an imperfect resist. The bleed is symmetrical: both edges of every column soften identically. At maximum, the bleeding extends deep into each column, and narrow columns may lose nearly all their color saturation.

---

### Knob 3 — Palette

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 1 |

**Palette** determines how many brightness levels survive within each column. At the minimum setting, the luminance channel is aggressively quantized into very few tonal steps, producing bold, flat bands reminiscent of cloth dipped in just two or three dye baths. As the value increases clockwise, more tonal levels are preserved and the banding becomes subtler. At the maximum, quantization is minimal and the original luminance detail remains largely intact.

---

### Knob 4 — Saturate

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Saturate** amplifies or attenuates the color richness of the processed signal. At the midpoint, chroma passes through unchanged. Turning the knob clockwise pushes the U and V channels further from neutral, intensifying colors the way a concentrated dye bath produces more vivid hues. Below the midpoint, the chroma channels compress toward neutral, producing a muted, sun-faded textile appearance.

:::note
Saturation boost is applied ***before*** edge bleed, so highly saturated columns show more dramatic color fading at their boundaries. Pushing saturation high while increasing bleed creates vivid stripe centers that wash out to neutral at the seams.
:::

---

### Knob 5 — Dye Depth

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Dye Depth** scales the amplitude of pseudo-random jitter applied to the luminance channel. At zero, the quantized luminance is clean and uniform within each column. As the value increases, the 16-bit LFSR displaces brightness values by increasing amounts, producing the irregular, organic texture of hand-applied dye. At maximum, the jitter is strong enough to create visible speckle and grain across the columns.

---

### Knob 6 — Warmth

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Warmth** is reserved for a future firmware update. It is intended to shift the processed palette toward warmer or cooler tones. Currently has no visible effect on the output.

---

### Switch 7 — Axis

| Property | Value |
|----------|-------|
| Off | Vert |
| On | Horiz |
| Default | Vert |

**Axis** selects the orientation of the column grid. In the default **Vert** position, columns run vertically: the image is sliced into side-by-side stripes like warp threads on a loom. Switch to **Horiz** to rotate the grid ninety degrees, creating horizontal bands like weft threads. Column width, bleed, and all other parameters operate identically in both orientations.

---

### Switch 8 — Palette Src

| Property | Value |
|----------|-------|
| Off | Fixed |
| On | Video |
| Default | Fixed |

**Palette Src** is reserved for a future firmware update. It is intended to select whether the dye color palette is derived from fixed internal values (**Fixed**) or sampled from the incoming video signal (**Video**). Currently has no visible effect on the output.

---

### Switch 9 — Double Ikat

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Double Ikat** enables luminance quantization on both axes simultaneously. With the switch **Off**, only the primary axis (set by **Axis**) is quantized into columns. With it **On**, the perpendicular axis also receives the same quantization mask, converting continuous stripes into a grid of rectangular tiles. This mimics the traditional ***double ikat*** technique, where both warp and weft threads are resist-dyed before weaving (arguably the most difficult and prized form of the craft.)

:::tip
Double Ikat combined with moderate **Col Width** and low **Palette** produces a mosaic of flat-colored tiles that resembles traditional Balinese ***geringsing*** double-ikat cloth.
:::

---

### Switch 10 — Noise

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Noise** is intended to control animation of the jitter pattern. The LFSR jitter source free-runs on every active pixel, so the displacement pattern naturally varies from frame to frame regardless of this toggle's position. The visual effect is subtle and frame-rate-dependent.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input directly to the output, disabling all Ikat processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) and wet (processed) signal. At 0%, the output is the original input: identical to Bypass. At 100%, the output is fully processed. Intermediate values blend the two, allowing you to dial in subtle textile textures overlaid on the source image.

---

## Background

### Resist dyeing

***Resist dyeing*** is one of humanity's oldest decorative techniques. The principle is simple: protect part of a material from absorbing dye, and only the unprotected areas take on color. Wax resist (batik), paste resist (katazome), and tie resist (shibori) are all variations on this theme. Ikat is a specific form where individual threads are tied before dyeing and then woven into fabric. Because the ties are never perfectly tight and the threads shift slightly during weaving, the resulting patterns have characteristically soft, feathered edges: in stark contrast to the hard edges of printed fabric. This feathering is the visual signature of ikat, and it's what we're recreating digitally.

### Column quantization

Ikat's column quantization implements a spatial version of ***sample and hold***. The pixel position along the chosen axis is divided by the column width using a ***barrel shift***: a single-cycle bit-shift that replaces a hardware divider, but constrains widths to powers of two. The remainder (fractional position within the column) is extracted with a bitwise mask. Within each column, the luminance channel is quantized by masking its low-order bits, collapsing smooth gradients into flat dye-lot bands. The number of bits masked is controlled by the **Palette** parameter.

### LFSR jitter

A ***linear feedback shift register*** (LFSR) generates a deterministic but pseudo-random sequence of 16-bit values. Ikat uses the lower 8 bits of this sequence, scaled by the **Dye Depth** parameter, to displace the Y channel after quantization. Because the LFSR advances on every active pixel, the displacement pattern is spatially varying: each pixel receives a different jitter offset. The result resembles the uneven dye absorption of natural fiber, where some threads absorb more dye than others despite receiving the same treatment.

### Edge bleed mechanics

The edge bleed algorithm computes each pixel's distance from the nearest column boundary. Pixels within the bleed zone: the region near the edge controlled by **Bleed Amt**: have their chroma scaled toward the neutral midpoint (value 512). Pixels near the center of a column retain full color, while those at the boundary fade to gray. This creates the ikat signature: vivid color in the stripe centers washing out to soft, undefined boundaries at the edges.


---

## Signal Flow

### Signal Flow Notes

The critical interaction is between column quantization and edge bleed. Stage 1 determines which "thread" each pixel belongs to and computes the fractional position within the column. Stage 2 uses that fractional position to compute the edge blend factor. In Stage 3, the edge blend factor scales chroma toward neutral: pixels near the center of a column retain full saturation while pixels near the boundary fade to gray.

**Saturate** amplifies chroma ***before*** edge bleed is applied (Stage 2 feeds into Stage 3). This means boosting saturation intensifies not only the column centers but also increases the contrast of the edge fade: vivid centers wash out more dramatically. Conversely, **Dye Depth** jitter is applied to the luminance channel ***after*** palette quantization (Stage 3), so the jitter displaces quantized levels rather than raw pixel values. The result is displacement within the "dye lot" rather than generic noise.

:::tip
**Chroma is spatial, luma is textural.** Edge bleed affects U and V (color fading at column edges) while LFSR jitter affects only Y (brightness grain within columns). The two effects operate on different channels, creating a layered visual texture that separates color structure from luminance detail.
:::


---

## Exercises

These exercises progress from basic stripe creation to complex double-ikat textile simulation. Each exercise introduces new controls and builds on the previous visual discoveries.
### Exercise 1: Warp Threads

![Warp Threads result](/img/instruments/videomancer/ikat/ikat_ex1_s1.png)
*Warp Threads — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Transform a video source into a simple vertical-stripe warp pattern with soft, dye-bleed edges.

#### Key Concepts

- Column quantization divides the image into vertical stripes
- Power-of-two column widths create discrete stripe sizes
- Edge bleed softens column boundaries with a dye-like fade

#### Video Source

A live camera feed or recorded footage with recognizable subjects and color variation (faces, landscapes, or colorful objects work well.)

#### Steps

1. Turn **Col Width** (Knob 1) to its midpoint. The image breaks into vertical stripes, each column showing a simplified version of the source.
2. Lower **Palette** (Knob 3) to about 25%. Luminance within each column collapses into broad tonal bands (like cloth dipped in very few dye baths.)
3. Slowly raise **Bleed Amt** (Knob 2) from zero. Watch the hard edges between stripes soften as color fades toward gray at each boundary.
4. Increase **Saturate** (Knob 4) past the midpoint to enrich the colors within each stripe. Notice how the bleed edges become more dramatic with higher saturation (vivid centers, neutral seams.)
5. Toggle **Bypass** (Switch 11) on and off to compare the woven result with the original source.

#### Settings

| Control | Value |
|---------|-------|
| Col Width | ~50% |
| Bleed Amt | ~40% |
| Palette | ~25% |
| Saturate | ~65% |
| Dye Depth | 0% |
| Warmth | 50% |
| Axis | Vert |
| Palette Src | Fixed |
| Double Ikat | Off |
| Noise | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Dye Bleed and Grain

![Dye Bleed and Grain result](/img/instruments/videomancer/ikat/ikat_ex2_s1.png)
*Dye Bleed and Grain — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Add dye imperfections and grain to the stripe pattern, creating a more realistic hand-dyed textile appearance.

#### Key Concepts

- LFSR jitter adds organic texture to quantized luminance
- Edge bleed and jitter operate on different channels (U/V vs. Y)
- Dye Depth controls the amplitude of luminance displacement

#### Video Source

Footage with moderate tonal range: interior scenes, still lifes, or nature footage with both highlights and shadows.

#### Steps

1. Begin with the settings from Exercise 1 (moderate column width, bleed, low palette).
2. Raise **Dye Depth** (Knob 5) slowly from zero. A grainy, speckled texture appears within each column as the LFSR displaces luminance values.
3. At about 50%, the grain is clearly visible. Each column now has an organic, fibrous texture rather than flat posterized bands.
4. Sweep **Col Width** (Knob 1) between its five width settings. Notice how the grain interacts differently at each column width: narrow columns compress the jitter into tight speckle, while wide columns spread it into gentle undulation.
5. Experiment with **Axis** (Switch 7), flipping between **Vert** and **Horiz**. The stripes rotate ninety degrees, reorienting the "warp" direction while all other parameters stay the same.

#### Settings

| Control | Value |
|---------|-------|
| Col Width | ~50% |
| Bleed Amt | ~40% |
| Palette | ~25% |
| Saturate | ~65% |
| Dye Depth | ~50% |
| Warmth | 50% |
| Axis | Vert |
| Palette Src | Fixed |
| Double Ikat | Off |
| Noise | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Double Ikat Mosaic

![Double Ikat Mosaic result](/img/instruments/videomancer/ikat/ikat_ex3_s1.png)
*Double Ikat Mosaic — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Build a full double-ikat mosaic: a grid of quantized tiles with blurred edges and animated grain, resembling traditional Balinese geringsing cloth.

#### Key Concepts

- Double ikat quantizes both axes simultaneously
- Combined parameters create complex textile textures
- Mix blends the textile effect with the source image

#### Video Source

High-contrast footage with bold shapes: architectural details, dancer silhouettes, or colorful abstract patterns from other Videomancer programs.

#### Steps

1. Set **Col Width** (Knob 1) to a moderate value. Enable **Double Ikat** (Switch 9). The vertical stripes become a grid of rectangular tiles as both axes are quantized simultaneously.
2. Lower **Palette** (Knob 3) to a low value. Each tile snaps to a single flat tone (the image becomes a mosaic of dyed squares.)
3. Increase **Bleed Amt** (Knob 2) to about 60%. The tile edges bleed, and narrow tiles may lose color entirely, leaving only the wider tiles with vivid centers.
4. Raise **Dye Depth** (Knob 5) to about 50%. The tiles shimmer with luminance grain.
5. Pull **Mix** (Fader 12) back to about 70% to blend the mosaic with the original source. The textile pattern overlays the recognizable image beneath like a woven screen.
6. Increase **Saturate** (Knob 4) to push the dye colors to vivid intensity. The contrast between saturated tile centers and neutral edges creates a jewel-toned fabric effect.

#### Settings

| Control | Value |
|---------|-------|
| Col Width | ~60% |
| Bleed Amt | ~60% |
| Palette | ~20% |
| Saturate | ~80% |
| Dye Depth | ~50% |
| Warmth | 50% |
| Axis | Vert |
| Palette Src | Fixed |
| Double Ikat | On |
| Noise | Off |
| Bypass | Off |
| Mix | ~70% |

---
## Glossary

- **Barrel Shift**: A digital circuit that shifts a binary number by a variable number of positions in a single clock cycle, used here to divide pixel position by power-of-two column widths without a hardware divider.

- **Double Ikat**: A textile technique where both warp and weft threads are resist-dyed before weaving, creating patterns that align on two axes; in this program, luminance quantization applied on both horizontal and vertical axes simultaneously.

- **Edge Bleed**: The softening of color at stripe boundaries, simulating dye that has seeped past an imperfect resist binding; implemented by fading chroma toward neutral gray near column edges.

- **Ikat**: A dyeing technique in which threads are tied and dyed before weaving, producing patterns with characteristically soft, feathered edges.

- **LFSR**: Linear Feedback Shift Register: a shift register whose input bit is a function of its previous state, producing a deterministic pseudo-random sequence used here for luminance jitter.

- **Palette Quantization**: Reducing the number of distinct brightness levels by masking the low-order bits of each pixel value, collapsing smooth gradients into flat dye-lot bands.

- **Power of Two**: A number that is an exact power of 2 (4, 8, 16, 32, 64), enabling efficient division via bit shifts instead of hardware dividers.

- **Resist**: A material or technique that prevents dye from penetrating certain areas of fabric, creating patterns through selective dye absorption.

- **Sample and Hold**: A signal processing operation that captures a value at one point and maintains it unchanged across a range, used here to hold a single quantized color across each column width.

- **Warp**: The set of vertical threads stretched on a loom, through which the horizontal weft threads are woven; in this program, the primary axis of column quantization.

---
