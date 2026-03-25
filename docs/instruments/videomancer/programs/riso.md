---
draft: true
sidebar_position: 249
slug: /instruments/videomancer/riso
title: "Riso"
image: /img/instruments/videomancer/riso/riso_hero_s1.png
description: "Risograph printing is a stencil-based duplicating process beloved by artists and zine-makers for its vivid spot inks, imperfect registration, and textured grain."
---

![Riso hero image](/img/instruments/videomancer/riso/riso_hero_s1.png)
*Riso simulating multi-pass risograph spot-color printing with fluorescent pink and blue inks, visible misregistration, and stencil grain texture.*

---

## Overview

Riso transforms live video into the look of a ***risograph*** print: the beloved, slightly imperfect duplicating process favored by zine makers, poster artists, and indie publishers the world over. It separates the image into tonal layers, assigns each layer a spot-color ink from a palette of four risograph-inspired colors, and composites them subtractively onto warm uncoated paper stock. The result is saturated, lo-fi, and full of character.

What makes Riso special is the deliberate imperfection. Real risograph machines print one color at a time, feeding the paper through for each pass. The registration between passes is never quite perfect, and the stencil master leaves a grainy texture in the ink. Riso models both of these artifacts: per-layer horizontal misregistration shifts each ink layer by a configurable number of pixels, and an LFSR-based stencil grain roughens the edges of each tonal zone. You can dial in a subtle duotone or push it toward a sloppy, overinked punk-zine aesthetic.

:::tip
Riso works best with bold, high-contrast source material. Portraits, hand-drawn graphics, and architectural subjects all produce striking results. Feed in something with strong tonal separation and let the ink layers do their work.
:::

### What's In a Name?

The name **Riso** is short for ***risograph***, a stencil duplicator manufactured by the Riso Kagaku Corporation of Japan. The risograph occupies a middle ground between a photocopier and a screen printer: it burns a master stencil for each color and forces ink through it onto paper, one pass per color. The process produces vibrant spot colors with a distinctive grain, and the multi-pass registration is famously imprecise. That imprecision: the slight horizontal drift between color layers: became an aesthetic signature embraced by artists and designers.

---

## Quick Start

1. Connect a video source with recognizable subjects. With the default settings, you'll see a duotone print in **Fluorescent Pink** and **Blue** on warm paper. The image is split at a luminance threshold: shadows print in pink, highlights in blue.
2. Turn **Threshold** (Knob 1) to shift the boundary between the two ink layers. Lower values push more of the image into the shadow layer (pink); higher values push more into the highlight layer (blue).
3. Increase **Grain** (Knob 2) to roughen the stencil texture. The edges of each tonal zone become noisy and organic, mimicking a well-used master stencil.
4. Turn **B H-Offset** (Knob 3) away from center to shift the blue ink layer horizontally. The two color layers misalign, revealing the paper color in the gaps (the hallmark of risograph printing.)

---

## Parameters

![Videomancer front panel with Riso loaded](/img/instruments/videomancer/riso/riso_control_panel.png)
*Videomancer's front panel with Riso active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Threshold

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Threshold** sets the luminance value that divides shadow from highlight. Pixels darker than the threshold receive ink A (the shadow layer); pixels brighter than the threshold receive ink B (the highlight layer). At the minimum, nearly everything falls below the threshold and prints in ink A. At the maximum, nearly everything falls above the threshold and prints in ink B. The midpoint produces a roughly equal split between the two inks, with the boundary tracking the tonal contours of the source image.

When **Layers** (Switch 11) is set to **3-Color**, a midtone band appears between the shadow and highlight zones, adding a third ink layer for the tonal middle ground.

---

### Knob 2 — Grain

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Grain** controls the intensity of the stencil grain texture applied to each ink layer. At minimum, the masks are smooth and the ink coverage is clean. As you increase Grain, an LFSR-based noise source roughens each layer's density mask, producing a stippled texture that mimics the uneven ink transfer of a real stencil master.

:::tip
A little grain goes a long way. Values around 20–30% produce a convincing analog texture. Push it past 50% for aggressive, lo-fi results where the stencil grain dominates the image.
:::

---

### Knob 3 — B H-Offset

| Property | Value |
|----------|-------|
| Range | -16px – 16px |
| Default | 1px |

**B H-Offset** controls the horizontal ***misregistration*** of ink layer B (the highlight layer). At center, layer B is aligned with layer A. Turning the knob away from center shifts layer B to the right by up to seven pixels, simulating the inter-pass alignment error of a real risograph. The offset is quantized to whole pixels internally.

The misregistration reveals the paper base color in the gaps between layers: a stripe of warm cream where the inks don't overlap. This is the visual signature of multi-pass printing.

---

### Knob 4 — B V-Offset

| Property | Value |
|----------|-------|
| Range | -8ln – 8ln |
| Default | 1ln |

**B V-Offset** is reserved for vertical misregistration of layer B. This parameter is mapped but not currently implemented due to FPGA memory constraints. Adjusting it has no visible effect.

:::note
Vertical misregistration would require line-buffer storage (block RAM) to delay an entire scan line. The iCE40 HX4K's 32 block RAMs are a limited resource. This parameter may be activated in a future revision if BRAM budget permits.
:::

---

### Knob 5 — C H-Offset

| Property | Value |
|----------|-------|
| Range | -16px – 16px |
| Default | -1px |

**C H-Offset** controls the horizontal misregistration of ink layer C (the midtone layer), used only when **Layers** (Switch 11) is set to **3-Color**. It works identically to **B H-Offset** but shifts the third ink layer independently. Setting B and C offsets to different values produces a staggered three-layer misregistration where each color pass drifts by a different amount.

In **2-Color** mode, layer C is disabled and this control has no visible effect.

---

### Knob 6 — C V-Offset

| Property | Value |
|----------|-------|
| Range | -8ln – 8ln |
| Default | 0ln |

**C V-Offset** is reserved for vertical misregistration of layer C. Like **B V-Offset**, this parameter is mapped but not currently implemented. Adjusting it has no visible effect.

---

### Switch 7 — Color A Hi

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color A Hi** is the high bit of the two-bit ink A color selector. Combined with **Color A Lo** (Switch 8), it selects one of four ink colors for the shadow layer. See the Toggle Group Notes below for the full color table.

---

### Switch 8 — Color A Lo

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color A Lo** is the low bit of the two-bit ink A color selector. Combined with **Color A Hi** (Switch 7), it selects the shadow layer ink color from the palette: Fluorescent Pink, Teal, Blue, or Black.

---

### Switch 9 — Color B Hi

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Color B Hi** is the high bit of the two-bit ink B color selector. Combined with **Color B Lo** (Switch 10), it selects one of four ink colors for the highlight layer. The palette is the same as ink A: both layers draw from the same four colors, but you can assign different colors to each.

---

### Switch 10 — Color B Lo

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color B Lo** is the low bit of the two-bit ink B color selector. Combined with **Color B Hi** (Switch 9), it selects the highlight layer ink color.

---

### Switch 11 — Layers

| Property | Value |
|----------|-------|
| Off | 2-Color |
| On | 3-Color |
| Default | 2-Color |

**Layers** selects between **2-Color** and **3-Color** printing modes. In 2-Color mode, the image is split into two tonal zones: shadows and highlights: each printed with its own ink. In 3-Color mode, a midtone band appears between the shadow and highlight zones. The midtone layer uses ink A's color at a fixed density and can be shifted horizontally with **C H-Offset** (Knob 5). Three-color mode produces richer, more complex prints but the midtone band has a flat density rather than a graduated one.

---

:::note Toggle Group Notes

Switches 7–8 and Switches 9–10 each form a two-bit color selector. The bit encoding is {Hi, Lo}, where Hi is the most significant bit:

| Hi | Lo | Ink Color |
|----|----|-----------|
| Off | Off | Fluorescent Pink |
| Off | On | Teal |
| On | Off | Blue |
| On | On | Black |

Both ink A (shadow layer) and ink B (highlight layer) draw from this same palette. The default configuration is Fluorescent Pink for ink A and Blue for ink B (a classic risograph duotone combination.)

:::tip
**Black ink** is useful as an anchor layer. Pair it with a vivid color for a stark, high-contrast duotone. In 3-Color mode, try Black shadows, a saturated color for midtones, and a different saturated color for highlights.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input signal and the wet (risograph-processed) output. At minimum, the original video passes through unchanged. At maximum: the default: the full risograph effect is applied. Intermediate values blend the two, letting you fade the printed look over the live image like a translucent overlay.

---

## Background

### Risograph printing

The ***risograph*** is a high-speed stencil duplicator that works like a cross between a screen printer and a photocopier. For each color, the machine cuts a master stencil from a thermal film, wraps it around a rotating drum filled with ink, and forces ink through the stencil onto paper as each sheet passes through. The process is fast and inexpensive, but each color requires a separate pass: the paper goes through the machine once for pink, again for blue, and so on.

This multi-pass approach gives risograph its visual identity. The registration between passes is never perfect: each color layer drifts by a pixel or two. The stencil itself is imperfect, too: the thermal cutting process and the ink transfer leave a grainy, slightly random texture. And because risograph inks are semi-transparent, overlapping colors mix ***subtractively*** on the paper, producing unexpected intermediate hues where layers overlap.

### Subtractive color mixing

When light passes through transparent ink on paper, some wavelengths are absorbed and others are reflected. This is ***subtractive*** color mixing: the more ink you add, the darker the result. It's the opposite of the ***additive*** mixing used by video displays, where adding light makes things brighter.

Riso models subtractive mixing by computing the absorption of each ink layer relative to the paper base color, then subtracting that absorption from the paper. Where two ink layers overlap, their absorptions add together, producing a darker, more saturated result. The paper base itself is a warm off-white (not pure white), so even the uninked areas have a slight cream tone (just like real uncoated stock.)

### Tonal separation

Commercial printing separates a continuous-tone image into discrete layers. Riso uses a simple luminance threshold to divide the image into two or three tonal zones:

- **Shadow zone** (below threshold): receives ink A
- **Highlight zone** (above threshold): receives ink B
- **Midtone zone** (3-color mode only): receives ink A at a fixed density

The shadow mask's density is proportional to how dark the pixel is: darker areas get heavier ink coverage. The highlight mask's density is proportional to how bright the pixel is. This produces a natural tonal rendering where ink density tracks the original image's tonality.


---

## Signal Flow

### Signal Flow Notes

The pipeline is driven entirely by luminance. The Y channel determines which tonal zone each pixel belongs to and how much ink density each layer receives. Chrominance (U and V) enters only at the compositing stage, where the ink colors' YUV values define the chroma contribution.

The horizontal misregistration is implemented with a flip-flop shift register (not block RAM). When layer B reads from a different position in the shift register than layer A, the two layers see pixels from different horizontal positions: producing the characteristic inter-pass drift. Because the shift register is only 8 pixels deep, the maximum misregistration is 7 pixels to the right.

:::note
The chroma compositing direction is determined by ink A's chrominance relative to the paper base. If ink A's U value is below the paper's U value, the total chroma absorption is subtracted; otherwise it's added. This means the chroma behavior can shift when you change ink A's color, even if ink B stays the same.
:::


---

## Exercises

These exercises progress from a simple duotone print to a complex three-color misregistered composition. Each one introduces more of Riso's capabilities.
### Exercise 1: Classic Duotone

![Classic Duotone result](/img/instruments/videomancer/riso/riso_ex1_s1.png)
*Classic Duotone — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean two-color risograph print with aligned registration (the starting point for all risograph work.)

#### Key Concepts

- Threshold separates shadow and highlight ink layers
- Subtractive mixing creates intermediate colors at overlap
- Paper base color affects the overall warmth

#### Video Source

A portrait or high-contrast still image with clear tonal separation.

#### Steps

1. Leave all controls at their defaults. The image appears as a duotone print in **Fluorescent Pink** (shadows) and **Blue** (highlights) on warm paper.
2. Sweep **Threshold** (Knob 1) slowly from minimum to maximum. Watch the boundary between pink and blue shift across the tonal range. Find a split that suits the subject.
3. Increase **Grain** (Knob 2) to about 25%. The clean ink boundaries roughen, adding stencil texture.
4. Flip **Color A Lo** (Switch 8) to **On**, changing ink A from Fluorescent Pink to **Teal**. The shadow layer shifts to a cool blue-green. Flip it back to confirm the color change.
5. Set **Color B Hi** and **Color B Lo** (Switches 9–10) both to **On** to select **Black** for the highlight layer. The print becomes a teal-and-black duotone with a more sober character.

#### Settings

| Control | Value |
|---------|-------|
| Threshold | 50.0% |
| Grain | 25.0% |
| B H-Offset | 0 px |
| B V-Offset | 0 ln |
| C H-Offset | 0 px |
| C V-Offset | 0 ln |
| Color A Hi | Off |
| Color A Lo | Off |
| Color B Hi | On |
| Color B Lo | Off |
| Layers | 2-Color |
| Mix | 100.0% |

---

### Exercise 2: Misregistered Duotone

![Misregistered Duotone result](/img/instruments/videomancer/riso/riso_ex2_s1.png)
*Misregistered Duotone — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A duotone print with deliberate horizontal misregistration, revealing the paper between color layers.

#### Key Concepts

- Horizontal misregistration shifts layer B relative to layer A
- Gaps between layers reveal the paper base color
- Subtractive overlap darkens where both inks print

#### Video Source

Footage with strong vertical structures: buildings, trees, fences, or text: that make misregistration clearly visible.

#### Steps

1. Start from the Exercise 1 settings (Fluorescent Pink + Blue, Threshold ~50%, Grain ~25%).
2. Turn **B H-Offset** (Knob 3) slowly to the right. The blue (highlight) layer slides rightward, creating a colored fringe on one side of each edge and a paper-colored gap on the other.
3. Push the offset to maximum. The two layers are now visibly displaced. Notice the warm cream stripe of paper visible between the inks.
4. Sweep **Threshold** (Knob 1) while misregistration is active. The boundary zone between the two layers shifts, changing the width and character of the overlap region.
5. Increase **Grain** (Knob 2) to about 60%. The stencil texture is now aggressive, breaking up the ink coverage into a stippled pattern.

#### Settings

| Control | Value |
|---------|-------|
| Threshold | 50.0% |
| Grain | 60.0% |
| B H-Offset | 16 px |
| B V-Offset | 0 ln |
| C H-Offset | 0 px |
| C V-Offset | 0 ln |
| Color A Hi | Off |
| Color A Lo | Off |
| Color B Hi | On |
| Color B Lo | Off |
| Layers | 2-Color |
| Mix | 100.0% |

---

### Exercise 3: Three-Color Punk Zine

![Three-Color Punk Zine result](/img/instruments/videomancer/riso/riso_ex3_s1.png)
*Three-Color Punk Zine — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A three-color risograph print with staggered misregistration and heavy grain (the overinked, slightly chaotic look of DIY zine art.)

#### Key Concepts

- 3-Color mode adds a midtone layer with independent misregistration
- Stacking misregistered layers produces complex color overlaps
- Aggressive grain pushes the aesthetic toward lo-fi print culture

#### Video Source

High-contrast material with bold shapes: hand-drawn artwork, protest graphics, or animated footage.

#### Steps

1. Set **Layers** (Switch 11) to **3-Color**. A midtone band appears between the shadow and highlight zones.
2. Set **Color A Hi** to **On** and **Color A Lo** to **On**, selecting **Black** for the shadow layer. Set **Color B** to **Fluorescent Pink** (Switches 9–10 both **Off**).
3. Turn **B H-Offset** (Knob 3) to about 10 px to shift the pink highlight layer rightward.
4. Turn **C H-Offset** (Knob 5) to about -10 px (the opposite direction) to shift the midtone layer the other way. The three color passes now stagger in opposite directions.
5. Increase **Grain** (Knob 2) to about 80%. The stencil texture becomes dominant, breaking up the ink into a rough, organic stipple.
6. Lower **Threshold** (Knob 1) to about 25%. More of the image falls into the shadow (black) zone, producing a dark, ink-heavy print.
7. Pull **Mix** (Fader 12) back to about 70% to let some of the original image show through beneath the printed layers.

#### Settings

| Control | Value |
|---------|-------|
| Threshold | 25.0% |
| Grain | 80.0% |
| B H-Offset | 10 px |
| B V-Offset | 0 ln |
| C H-Offset | -10 px |
| C V-Offset | 0 ln |
| Color A Hi | On |
| Color A Lo | On |
| Color B Hi | Off |
| Color B Lo | Off |
| Layers | 3-Color |
| Mix | 70.0% |

---
## Glossary

- **Duotone**: A print made with exactly two ink colors, each assigned to a different tonal range of the image.

- **LFSR**: ***Linear Feedback Shift Register***; a shift register whose input bit is a function of its previous state. Used here to generate pseudo-random noise for stencil grain.

- **Misregistration**: The horizontal offset between successive print passes caused by imprecise paper alignment. In risograph printing, this creates colored fringes and paper-colored gaps at edges.

- **Risograph**: A high-speed stencil duplicator that prints one ink color per pass. Known for vibrant spot colors, grainy texture, and imprecise registration.

- **Spot Color**: A pre-mixed ink used as a single color in printing, as opposed to process color (CMYK) which builds colors from overlapping halftone dots.

- **Stencil Grain**: The irregular texture in risograph prints caused by the thermal stencil cutting process and uneven ink transfer through the master.

- **Subtractive Mixing**: Color mixing where pigments absorb (subtract) wavelengths from reflected light. More ink produces darker results: the opposite of additive (light-based) mixing used by video displays.

- **Tonal Separation**: Dividing a continuous-tone image into discrete zones based on brightness, each zone assigned to a different printing layer.

---
