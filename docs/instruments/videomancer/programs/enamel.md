---
draft: true
sidebar_position: 101
slug: /instruments/videomancer/enamel
title: "Enamel"
image: /img/instruments/videomancer/enamel/enamel_hero_s1.png
description: "Enamel transforms live video into a digital simulation of cloisonné enamelwork — the ancient decorative art in which thin metal wires are soldered onto a surface to form cells, each filled with vitreous glass paste and fired to a glossy finish."
---

![Enamel hero image](/img/instruments/videomancer/enamel/enamel_hero_s1.png)
*Enamel transforming a live video feed into a cloisonné artwork with gold wire boundaries separating vivid, flat-colored cells.*

---

## Overview

Enamel recreates the look of ***cloisonné*** enamelwork: an ancient decorative art in which thin metal wires are soldered onto a surface to form compartments, then filled with vitreous glass paste and fired to a glossy finish. The program detects edges in the input video and renders them as metallic "wire" outlines, while the regions between wires are flattened into uniform, saturated fields of color. The result looks as if someone fused your video signal onto a piece of ornamental metalwork.

At gentle settings, Enamel adds a subtle stained-glass quality: outlines sharpen, colors become bolder, and smooth gradients snap into opaque bands. At extreme settings, the image dissolves into a mosaic of vivid cells separated by heavy wire borders: a fully abstracted material surface that you can animate with built-in shimmer and palette controls.

:::tip
Enamel is a ***processing*** program. It transforms an incoming video signal rather than generating imagery from scratch. Feed it a camera, a pattern generator, or the output of another program to see the cloisonné effect come alive.
:::

### What's In a Name?

***Enamel*** refers directly to ***vitreous enamel***, the glassy coating fused to metal in decorative arts such as cloisonné, champlevé, and plique-à-jour. In cloisonné, thin metal strips: called ***cloisons***: are bent into patterns and soldered to a base, forming cells that are filled with colored enamel powder and fired in a kiln. The finished surface is polished smooth, with gleaming wire boundaries separating pools of opaque color. Videomancer's Enamel program captures that process digitally: edge detection creates the wire, and luminance quantization fills each cell with flat, saturated color.

---

## Quick Start

1. Feed any video source into Videomancer and select **Enamel**. With default settings, you'll see the image with subtle edge-detected wire outlines and mild color flattening.
2. Turn **Edge Thr** (Knob 2) clockwise to widen the wire boundaries. More of the image becomes wire, thickening the dark or golden outlines between color cells.
3. Step through **Palette** (Knob 3) to reduce the number of luminance levels in the fill regions. At the lowest setting, cells snap to just a handful of flat tones (the classic enamel look.)
4. Flip **Style** (Switch 7) to **Basel** to switch from dark wires to bright gold wires, and toggle **Gloss** (Switch 9) to **On** to add a subtle reflective shimmer across the fill regions.

---

## Parameters

![Videomancer front panel with Enamel loaded](/img/instruments/videomancer/enamel/enamel_control_panel.png)
*Videomancer's front panel with Enamel active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Wire W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Wire W** sets the base sensitivity for edge detection. At low values, even faint gradients in the source image are classified as wire, producing dense, far-reaching outlines that cover much of the frame. As you increase **Wire W**, the edge detector becomes more selective: only strong, high-contrast boundaries register as wire, and the outlines shrink to trace only the most prominent features. At maximum, almost nothing qualifies as wire, and the effect reduces to color quantization alone.

:::note
**Wire W** and **Edge Thr** work together to define the wire network. Think of **Wire W** as the "sensitivity dial" and **Edge Thr** as the "width expansion." Balancing the two controls lets you sculpt wires that range from hairline traces to bold, heavy borders.
:::

---

### Knob 2 — Edge Thr

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Edge Thr** expands the effective wire coverage by lowering the internal detection threshold. At its minimum, only the edges that already exceed the **Wire W** sensitivity become wire. As you increase **Edge Thr**, the threshold drops, and progressively more pixels are reclassified as wire: making the outlines wider and the overall wire network denser. Pair **Edge Thr** with a moderate **Wire W** setting to create thick, dramatic wire borders reminiscent of heavy-gauge cloisonné metalwork.

---

### Knob 3 — Palette

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

**Palette** selects the number of luminance quantization levels applied to the fill regions between wires. This control steps through eight discrete settings, from heavily posterized (just a few flat brightness bands) to nearly unquantized (hundreds of tonal levels). Lower Palette values give the flat, opaque character of real enamel pigment: large areas of uniform tone with crisp boundaries between colors. Higher values preserve more of the source's tonal detail, producing a subtler, more photographic effect with only a hint of flattening.

:::tip
Set **Palette** to its lowest position for the most authentic cloisonné look. Real enamel cells contain a single color: no gradients. The fewer the levels, the closer you get to that handcrafted quality.
:::

---

### Knob 4 — Gloss

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Gloss** (Knob 4) is reserved for a future saturation enhancement feature. In the current firmware, adjusting this knob produces no visible change to the output. The enamel color saturation is boosted automatically by a fixed internal amount on all fill pixels.

---

### Knob 5 — Flat Amt

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Flat Amt** controls the brightness of wire pixels. In **Basel** mode (gold wires), the wire brightness tracks this control directly: turn it up for brilliant, gleaming wires, turn it down for muted, tarnished gold. In **Cloisnne** mode (dark wires), the effect is more subtle: the wire brightness is one-quarter of the control value, so even at maximum the wires remain dark, though not completely black. Use **Flat Amt** to fine-tune the contrast between wire outlines and the colored fill cells.

---

### Knob 6 — Wire Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Wire Hue** controls the intensity of the gloss effect on fill regions when **Gloss** (Switch 9) is enabled. Despite its name, this knob does not rotate the hue of the wire. Instead, it scales a position-based brightness modulation that simulates the curved, reflective surface of fired enamel glaze. At its minimum, the gloss pattern disappears entirely. As you increase the control, a subtle grid-like shimmer becomes visible across the fill cells, imitating the way light plays across a polished enamel surface.

:::note
The **Wire Hue** control only has a visible effect when **Gloss** (Switch 9) is set to **On**. With Gloss disabled, this knob does nothing.
:::

---

### Switch 7 — Style

| Property | Value |
|----------|-------|
| Off | Cloisnne |
| On | Basel |
| Default | Cloisnne |

**Style** selects between two enamel wire rendering modes. In the **Cloisnne** position, wires are rendered dark: low brightness with neutral chroma: evoking the look of oxidized or blackened metal partitions. In the **Basel** position, wires are rendered bright with a warm gold tint, simulating polished brass or gold-leaf wire. The wire brightness in both modes is further adjusted by the **Flat Amt** knob (Knob 5).

---

### Switch 8 — Wire Color

| Property | Value |
|----------|-------|
| Off | Gold |
| On | Black |
| Default | Gold |

**Wire Color** shifts the color palette of the fill regions. In the **Gold** position, chrominance passes through the saturation boost unaltered, producing a neutral-to-cool palette. In the **Black** position, a subtle warm shift is applied to the V (red-difference) channel, pushing fill colors toward warmer red and orange tones. This mimics the way certain enamel pigments shift toward warm amber when fired at high temperatures.

---

### Switch 9 — Gloss

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Gloss** enables or disables the surface gloss simulation on fill regions. When set to **On**, a position-dependent brightness pattern is added to fill pixels, creating a subtle, grid-like shimmer that suggests the curved, reflective surface of polished enamel. The strength of this shimmer is controlled by the **Wire Hue** knob (Knob 6). When set to **Off**, fill regions receive flat, uniform brightness from the quantizer with no reflective modulation.

---

### Switch 10 — Video Pal

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Video Pal** enables a shimmer animation on wire pixels. When set to **On**, wire brightness is modulated frame by frame using a pattern derived from the frame counter and horizontal pixel position. The result is a subtle sparkling effect along the wires, as if light is glinting off a metallic surface. When set to **Off**, wires are rendered with static, uniform brightness.

:::tip
Combine **Video Pal** with **Basel** style and a high **Flat Amt** for maximum sparkle (the bright gold wires catch the animated light beautifully.)
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Enamel processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the enamel-processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original (dry) input signal and the fully processed (wet) enamel output. At minimum, the output is entirely the original video. At maximum, the output is entirely the enamel effect. Intermediate positions blend the two, which can produce interesting semi-transparent overlay effects where the wire network and quantized fills are superimposed over the source at reduced opacity.

---

## Background

### Cloisonné enamelwork

***Cloisonné*** is one of the oldest decorative metalworking techniques, with origins tracing back to ancient Egypt and Byzantium. The word comes from the French *cloison*, meaning "partition." An artisan bends thin strips of metal: typically gold, silver, or copper: into intricate patterns and solders them to a metal base. The resulting network of tiny cells is filled with finely ground colored glass powder, then fired in a kiln at around 800°C. The glass melts, fuses to the metal, and hardens into smooth, opaque pools of vivid color separated by gleaming wire borders. The surface is then ground flat and polished to a high gloss.

Enamel captures this process in real time. Edge detection stands in for the metal wire, luminance quantization replaces the discrete pigment fills, and the gloss simulation mimics the polished surface.

### Edge detection as wire

The program detects edges by computing brightness gradients in two directions: horizontal (comparing each pixel to the one immediately before it) and vertical (comparing each pixel to the same position on the previous scan line). These two gradients are combined: the larger gradient dominates, with the smaller contributing at half strength: and the result is compared against a threshold. Pixels that exceed the threshold are classified as "wire" and receive the metallic rendering; pixels below are classified as "fill" and receive the quantized enamel treatment.

This two-axis edge detection ensures that both horizontal and vertical features in the source image produce wire outlines, creating a complete network of boundaries rather than detecting only one direction.

### Luminance quantization

Fill pixels undergo ***posterization***: their brightness values are quantized to a reduced number of discrete levels. The quantizer works by masking the lower bits of the 10-bit luminance value, effectively rounding each pixel's brightness down to the nearest step. With the **Palette** control at its lowest setting, only 8 brightness levels remain, producing the flat, opaque look of real enamel pigment. At higher settings, the quantization becomes finer, preserving more of the source's tonal subtlety.

In addition to luminance quantization, the program applies automatic ***saturation boost*** to fill pixels. Chroma values are pushed further from the neutral axis (midpoint 512), intensifying the color of each enamel cell. This compensates for the flattening effect of quantization and gives the fills the vivid, jewel-like quality characteristic of real vitreous enamel.


---

## Signal Flow

### Signal Flow Notes

The pipeline is 10 clocks deep: 6 clocks for the main processing stages, plus 4 clocks for the interpolator wet/dry mix. A parallel sync and data delay line keeps the original signal aligned with the processed output so the crossfader always blends matching pixels.

Two key interactions define the enamel character:

1. **Edge detection feeds wire/fill routing.** The wire/fill classification at Stage 5 is a binary gate: every pixel is either wire or fill, with no gradual blending. This hard boundary is what gives cloisonné its characteristic sharp partition between metal and glass. The **Wire W** and **Edge Thr** controls together set the sensitivity and width of this gate.

2. **Quantization and saturation boost work together.** Quantization flattens the luma of fill pixels into discrete bands, while the automatic saturation boost intensifies their chroma. The combination produces the vivid, opaque quality of real enamel (flat areas of bold color, like pools of molten glass.)

:::note
The vertical edge path requires a full ***video line buffer*** (1 BRAM). The line buffer stores the Y channel of the previous scan line so the gradient can be computed between vertically adjacent pixels. Without it, only horizontal edges would be detected, and the wire network would consist solely of vertical lines.
:::


---

## Exercises

These exercises progress from basic wire detection to full cloisonné composition. Each builds on the previous, gradually engaging more of Enamel's processing chain.
### Exercise 1: Wire Network

![Wire Network result](/img/instruments/videomancer/enamel/enamel_ex1_s1.png)
*Wire Network — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A bold wire-frame outline of your source image, with clearly visible metallic boundaries tracing every edge.

#### Key Concepts

- Edge detection creates the wire outlines
- Wire W and Edge Thr together control wire density and thickness
- Style toggle selects dark or gold wire rendering

#### Video Source

A live camera feed or recorded footage with strong shapes and moderate contrast (faces, architecture, or high-contrast objects work well.)

#### Steps

1. **Reveal the wires**: Turn **Wire W** (Knob 1) to about 40%. Thin outlines appear along edges in the source. The image looks like a lightly penciled sketch overlaid on the video.
2. **Thicken the wires**: Increase **Edge Thr** (Knob 2) to about 60%. The wire outlines expand, covering more of the image with the metallic rendering. Subtle edges that were invisible before now become visible partitions.
3. **Gold wires**: Flip **Style** (Switch 7) to **Basel**. The wires switch from dark outlines to bright, warm gold lines. Increase **Flat Amt** (Knob 5) to make the gold wires gleam brighter.
4. **Wire brightness**: Sweep **Flat Amt** from minimum to maximum. In Basel mode, the wires go from dim amber to blazing gold. Switch Style back to **Cloisnne** and sweep again (the dark wires shift subtly from near-black to dark gray.)
5. **Add shimmer**: Toggle **Video Pal** (Switch 10) to **On**. The wire pixels now sparkle with a frame-by-frame animation, as if catching light.

#### Settings

| Control | Value |
|---------|-------|
| Wire W | ~40% |
| Edge Thr | ~60% |
| Palette | 4 |
| Gloss | 50% |
| Flat Amt | ~70% |
| Wire Hue | 0° |
| Style | Basel |
| Wire Color | Gold |
| Gloss (Switch) | Off |
| Video Pal | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Enamel Palette

![Enamel Palette result](/img/instruments/videomancer/enamel/enamel_ex2_s1.png)
*Enamel Palette — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A richly colored cloisonné composition with distinct enamel cells, bold outlines, and a warm or cool palette shift.

#### Key Concepts

- Palette quantization creates flat, opaque fill regions
- Saturation boost intensifies fill colors automatically
- Wire Color toggle shifts the fill palette warm or cool

#### Video Source

Footage with varied colors and smooth gradients: landscapes, flowers, or abstract patterns with a range of hues and brightness levels.

#### Steps

1. **Set up wires**: Begin with **Wire W** at ~50% and **Edge Thr** at ~40% so a clear wire network is visible.
2. **Flatten the palette**: Step **Palette** (Knob 3) down to position 2 or 3. Smooth gradients in the source collapse into large regions of flat, uniform brightness: the enamel cells. Notice how the wire outlines naturally border these flat regions.
3. **Warm the palette**: Flip **Wire Color** (Switch 8) to **Black**. The fill regions shift toward warmer red and orange tones, as if the enamel was fired at a higher temperature.
4. **Compare palettes**: Toggle **Wire Color** back and forth between **Gold** and **Black**, observing how the chroma shifts. **Gold** preserves the source palette; **Black** pushes it warm.
5. **Full enamel**: Set **Style** to **Basel** for gold wires, **Wire Color** to **Black** for warm fills, and **Palette** to 1. The image becomes a mosaic of warm-toned flat cells with bright gold outlines (classic cloisonné.)

#### Settings

| Control | Value |
|---------|-------|
| Wire W | ~50% |
| Edge Thr | ~40% |
| Palette | 2 |
| Gloss | 50% |
| Flat Amt | ~60% |
| Wire Hue | 0° |
| Style | Basel |
| Wire Color | Black |
| Gloss (Switch) | Off |
| Video Pal | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Glossy Ornament

![Glossy Ornament result](/img/instruments/videomancer/enamel/enamel_ex3_s1.png)
*Glossy Ornament — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A fully realized cloisonné ornament with gloss sheen, animated wire sparkle, and a dry/wet blend for subtle overlay effects.

#### Key Concepts

- Gloss simulates a polished, reflective enamel surface
- Wire Hue controls gloss intensity
- Mix crossfades between raw and processed output

#### Video Source

Any footage with recognizable content: the effect is dramatic enough to transform any input into ornamental art.

#### Steps

1. **Full enamel setup**: Set **Wire W** ~40%, **Edge Thr** ~50%, **Palette** to 3, **Style** to **Basel**, and **Flat Amt** to ~70%.
2. **Enable gloss**: Flip **Gloss** (Switch 9) to **On**. A faint grid-like shimmer appears across the fill regions.
3. **Increase gloss intensity**: Turn **Wire Hue** (Knob 6) clockwise. The shimmer becomes more pronounced, creating a visible reflective pattern that suggests the curved surface of polished glass.
4. **Add wire animation**: Toggle **Video Pal** (Switch 10) to **On**. The gold wires now sparkle with frame-by-frame shimmer while the fill cells gleam with gloss.
5. **Blend with source**: Pull the **Mix** fader (Fader 12) down to about 50%. The enamel effect becomes semi-transparent, overlaying the wire network and quantized fills on top of the original footage at reduced opacity. This creates a "ghostly enamel" effect.
6. **Warm everything**: Set **Wire Color** to **Black** for warmth, and sweep **Wire Hue** slowly. Notice how the gloss interacts with the warm palette shift.

#### Settings

| Control | Value |
|---------|-------|
| Wire W | ~40% |
| Edge Thr | ~50% |
| Palette | 3 |
| Gloss | 50% |
| Flat Amt | ~70% |
| Wire Hue | ~200° |
| Style | Basel |
| Wire Color | Black |
| Gloss (Switch) | On |
| Video Pal | On |
| Bypass | Off |
| Mix | ~50% |

---
## Glossary

- **Cloisonné**: A decorative art technique in which thin metal wires are soldered to a surface to form compartments (cloisons) that are filled with colored enamel and fired.

- **Edge Detection**: Identifying boundaries in an image by computing brightness gradients between adjacent pixels; used here to locate wire positions.

- **Gradient**: The magnitude of change in pixel brightness between two neighboring samples; larger gradients indicate stronger edges.

- **Line Buffer**: A block of FPGA memory (BRAM) that stores one full scan line of pixel data, enabling comparison between vertically adjacent lines.

- **Posterization**: Reducing the number of distinct brightness or color levels in an image, creating flat regions separated by hard boundaries.

- **Quantization**: Mapping a continuous range of values to a smaller set of discrete levels; the mechanism behind posterization.

- **Saturation Boost**: Increasing the intensity of color by pushing chroma values further from their neutral midpoint.

- **Threshold**: A cutoff value that separates edge pixels (wire) from non-edge pixels (fill) based on computed gradient magnitude.

- **Vitreous Enamel**: A glassy decorative coating made by fusing powdered glass to a metal surface at high temperature.

- **Wire**: In Enamel's context, the rendered edge pixels that simulate the thin metal partitions in cloisonné artwork.

---
