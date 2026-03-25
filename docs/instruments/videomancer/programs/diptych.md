---
draft: true
sidebar_position: 85
slug: /instruments/videomancer/diptych
title: "Diptych"
image: /img/instruments/videomancer/diptych/diptych_hero_s1.png
description: "A diptych is a two-panel artwork — two images joined along a central hinge."
---

![Diptych hero image](/img/instruments/videomancer/diptych/diptych_hero_s1.png)
*Diptych splitting a camera feed into two contrasting panels: natural color on the left, complementary chroma on the right: divided by a black gap.*

---

## Overview

**Diptych** splits your video into two side-by-side panels separated by an adjustable dividing line. The left panel passes through untouched while the right panel displays the same image in ***complementary colors***: every hue is replaced by its opposite. The effect is immediate and striking: warm tones become cool, greens become magentas, and the two halves of the screen become a paired study in chromatic contrast. An optional black gap at the split point frames the two panels like a gallery mounting.

At default settings, **Diptych** divides the screen near the center with no gap, producing a clean bilateral color separation. By adjusting the **Split Point** and **Gap Width** knobs, you can position the dividing line anywhere across the frame and open up a black border between the panels. Engaging the **Vertical** toggle adds luminance inversion on the reflected side, turning the complementary panel into a full negative image. The **Mix** fader lets you dial between the split effect and the unprocessed original for subtle color-shift composites.

:::tip
**Diptych** is especially effective with colorful source material. Feed it footage rich in saturated hues and watch the right panel transform into a vivid chromatic mirror.
:::

### What's In a Name?

A ***diptych*** is a work of art composed of two hinged panels displayed side by side: a format used since antiquity for devotional paintings, writing tablets, and paired portraits. The word comes from the Greek ***diptykhos***, meaning "folded in two." This program folds your video into two panels, each presenting a different chromatic interpretation of the same scene, like a painter rendering the same subject in two contrasting palettes.

---

## Quick Start

1. With a colorful video source connected, observe the default split: the left half of the screen shows your original image, and the right half shows the same image in complementary colors. The dividing line sits near the center.
2. Sweep **Split Point** (Knob 1) left and right. The boundary between the two panels slides across the screen, giving more or less room to each side.
3. Turn **Gap Width** (Knob 2) clockwise to open a black border between the panels. The gap frames the two halves like a gallery diptych mounting.
4. Flip **Vertical** (Switch 7) to **On**. The right panel now shows a full negative image: both brightness and color are inverted. Toggle it back to compare the chromatic complement against the full negative.

---

## Parameters

![Videomancer front panel with Diptych loaded](/img/instruments/videomancer/diptych/diptych_control_panel.png)
*Videomancer's front panel with Diptych active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Split Point

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Split Point** sets the horizontal position of the dividing line between the two panels. At 0%, the split sits near the left edge of the active picture, giving almost the entire screen to the complementary-color panel. At 100%, the split moves to the right edge, and nearly the entire screen passes through unchanged. At the default of 50%, the image is divided roughly in half.

The split position is mapped to the active line width, so it tracks correctly across video standards.

---

### Knob 2 — Gap Width

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Gap Width** controls the size of the black border at the split point. At 0%, fully counterclockwise, there is no gap and the two panels sit flush against each other. As you turn the knob clockwise, a bar of solid black opens up at the dividing line, widening symmetrically around the split position. At high values, the gap can consume a significant portion of the image, isolating the two panels like paintings on a wall.

:::tip
A narrow gap of around 30% creates a crisp dividing line that emphasizes the contrast between the two panels. A wider gap is useful for framing compositions or creating a letterbox-style border effect.
:::

---

### Knob 3 — Offset

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Offset** is reserved for a future update and does not currently affect the output. The control is mapped to an internal register for planned spatial offset functionality.

---

### Knob 4 — Zoom

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Zoom** is reserved for a future update and does not currently affect the output. The control is mapped to an internal register for planned zoom functionality.

---

### Knob 5 — Tilt

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Tilt** is reserved for a future update and does not currently affect the output. The control is mapped to an internal register for planned tilt functionality.

---

### Knob 6 — Tint

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Tint** is reserved for a future update and does not currently affect the output. The control is mapped to an internal register for planned color tinting functionality.

:::note
Knobs 3 through 6 (**Offset**, **Zoom**, **Tilt**, and **Tint**) are reserved for planned features. Turning these knobs has no visible effect on the output in the current version.
:::

---

### Switch 7 — Vertical

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Vertical** controls whether luminance is also inverted on the processed panel. When set to **Off**, only the chrominance channels are inverted, producing complementary colors while preserving the original brightness structure: dark areas stay dark, bright areas stay bright. When set to **On**, luminance is inverted as well, creating a full ***negative image*** on the processed side: dark becomes light, light becomes dark, and all colors shift to their complements simultaneously.

The difference between complementary chroma (Off) and full negative (On) is dramatic. Complementary chroma retains the recognizable form of the image while recoloring it. Full negative transforms brightness and color together, producing a more abstract, eerie result.

---

### Switch 8 — Double

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Double** is reserved for a future update and does not currently affect the output. The control is mapped to an internal register for planned bilateral doubling functionality.

---

### Switch 9 — Reverse

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Reverse** is reserved for a future update and does not currently affect the output. The control is mapped to an internal register for planned mirror-direction reversal.

---

### Switch 10 — Color Tint

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color Tint** is reserved for a future update and does not currently affect the output. The control is mapped to an internal register for planned color tinting functionality.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Diptych processing stages. The sync delay pipeline still aligns timing, so there is no visual glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the split result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the wet/dry crossfade between the processed split effect and the unprocessed original. At 0%, the output is entirely the delayed original: no split is visible. At 100%, the full split effect is shown. At intermediate values, the processed and original signals are blended, which softens the color difference between the two panels into a gradual transition rather than a hard split.

:::tip
At around 50%, the two halves of the split begin to merge, creating a gentle color gradient across the image rather than a sharp divide. This is useful for subtle tonal shifts.
:::

---

## Background

### The diptych in art

A ***diptych*** is one of the oldest formats in visual art: two panels joined by a hinge. From Byzantine ivory carvings to Renaissance altarpieces, the paired panel format invites comparison and contrast. Each panel can present a complementary viewpoint: sacred and profane, before and after, light and shadow. The Videomancer **Diptych** program applies this principle to moving images, dividing the video frame into two halves with contrasting chromatic treatments.

### Complementary colors

Every color has a ***complement***: the hue directly opposite it on the color wheel. Red complements cyan, blue complements yellow, and green complements magenta. In video signal processing, complementary colors are produced by inverting the ***chrominance*** channels. The YUV color space separates brightness (Y) from color (U and V). Inverting U and V: flipping each value to its opposite around the neutral midpoint: replaces every hue with its complement while leaving brightness intact. This is exactly what **Diptych** does to the right panel: a bitwise complement of the U and V channels, transforming warm tones to cool and vice versa.

### Negative images

A ***negative*** image inverts all channels: both brightness and color. In photographic film, the negative is the intermediate stage where dark areas appear light and light areas appear dark. Colors also reverse: blue skies become orange, green leaves become magenta. The **Vertical** toggle in **Diptych** engages luminance inversion on top of the chroma complement, producing a full negative on the processed panel. The visual effect goes beyond simple color swapping: the entire tonal structure flips, creating an uncanny, ghostly version of the original scene.

### Interpolation and mixing

The wet/dry ***mix*** stage uses ***linear interpolation*** to crossfade between two signals. Given two values: the original (dry) and the processed (wet): the interpolator calculates a weighted average based on the **Mix** fader position. At one extreme you hear only the dry signal; at the other, only the wet. In between, both contribute proportionally. **Diptych** uses three parallel interpolator instances to independently mix the Y, U, and V channels, preserving correct color balance throughout the crossfade.


---

## Signal Flow

### Signal Flow Notes

The processing pipeline runs in a single `process(clk)` block. Pixel position is tracked by 12-bit counters: `s_x_counter` increments every clock and resets at each horizontal sync edge, while `s_y_counter` increments per line and resets at vertical sync. The split point is computed as `s_split_point + 128`, mapping the 10-bit register value to an offset within the active picture area.

The gap width register is divided by 8 (a 3-bit right shift) to produce the half-width of the black border region. When a pixel falls within this region, the output is forced to black (Y=0) with neutral chroma (U=V=512). Outside the gap, pixels left of the split pass through unchanged while pixels right of the split receive chroma inversion. If the **Vertical** toggle is engaged, luma is also inverted on the right side. The sync signals (hsync_n, vsync_n, field_n) and original video data pass through an 8-stage shift register to align with the processing latency, providing the delayed "dry" input to the three interpolator mix instances.

:::note
**Diptych** does not perform spatial mirroring: it does not flip or rearrange pixels across the split line. The effect is purely chromatic: one panel shows original colors, the other shows their complements. True spatial reflection would require a line buffer (BRAM), which this program does not use.
:::


---

## Exercises

These exercises explore the bilateral color-split effect from simple panel division to full negative compositing. Each builds on the previous, engaging the active controls.
### Exercise 1: Clean Panel Split

![Clean Panel Split result](/img/instruments/videomancer/diptych/diptych_ex1_s1.png)
*Clean Panel Split — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A cleanly divided two-panel composition with original colors on the left and complementary colors on the right, framed by a black border.

#### Key Concepts

- The split point divides the frame into two chromatic panels
- The gap creates a visible border between panels
- Complementary chroma inverts hue while preserving brightness

#### Video Source

A live camera feed or recorded footage with varied, saturated colors: faces, flowers, painted surfaces, or colorful clothing work well.

#### Steps

1. **Default split**: Observe the screen at default settings. The left half shows your original image; the right half shows the same image in complementary colors. Notice how warm tones on the left become cool on the right.
2. **Reposition the divide**: Sweep **Split Point** (Knob 1) slowly from left to right. The boundary between panels slides across the frame, revealing more or less of each color treatment.
3. **Open a gap**: Turn **Gap Width** (Knob 2) to about 30%. A black bar emerges at the split, framing the two panels like a gallery display.
4. **Compare**: Use **Bypass** (Switch 11) to toggle between the split and the unprocessed original. Notice how the left panel is always identical to the original (only the right panel is transformed.)

#### Settings

| Control | Value |
|---------|-------|
| Split Point | ~50% |
| Gap Width | ~30% |
| Offset | 50% |
| Zoom | 50% |
| Tilt | 50% |
| Tint | 50% |
| Vertical | Off |
| Double | Off |
| Reverse | Off |
| Color Tint | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Negative Panel

![Negative Panel result](/img/instruments/videomancer/diptych/diptych_ex2_s1.png)
*Negative Panel — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A diptych with a full negative panel on the right, then blend the two panels together for a soft color gradient.

#### Key Concepts

- Luma inversion plus chroma inversion produces a full negative image
- The difference between complementary color and full negative is dramatic
- Mix blending softens the split into a gradient

#### Video Source

High-contrast footage with strong light and shadow: architectural interiors, backlit silhouettes, or stage lighting produce vivid negatives.

#### Steps

1. **Start with the default split**: Confirm the complementary color split is visible with **Split Point** near center and **Mix** at 100%.
2. **Engage full negative**: Toggle **Vertical** (Switch 7) to **On**. The right panel transforms from a color complement into a full negative: dark areas become light, and all colors reverse. The transformation is more dramatic than chroma complement alone.
3. **Compare the two modes**: Toggle **Vertical** back and forth. With it off, the right panel retains the original brightness structure. With it on, brightness also inverts.
4. **Blend the panels**: Lower **Mix** (Fader 12) to about 50%. The hard split dissolves into a soft gradient, merging the original and processed panels. Colors shift subtly across the frame rather than switching abruptly at the boundary.
5. **Adjust the border**: Set **Gap Width** (Knob 2) to about 50% with **Mix** back at 100%. The wider gap isolates the two panels further, emphasizing the contrast between original and negative.

#### Settings

| Control | Value |
|---------|-------|
| Split Point | ~50% |
| Gap Width | ~50% |
| Offset | 50% |
| Zoom | 50% |
| Tilt | 50% |
| Tint | 50% |
| Vertical | On |
| Double | Off |
| Reverse | Off |
| Color Tint | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Off-Center Composition

![Off-Center Composition result](/img/instruments/videomancer/diptych/diptych_ex3_s1.png)
*Off-Center Composition — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An asymmetric diptych with a narrow complementary-color strip on one side, blended back toward the original for a subtle selective color-shift effect.

#### Key Concepts

- Asymmetric split positions create unequal panel proportions
- Combining narrow gap, off-center split, and mix produces layered effects
- The split point can isolate small regions for selective color treatment

#### Video Source

Footage with a strong subject on one side of the frame: a portrait, a single object against a background, or any composition with an off-center focal point.

#### Steps

1. **Move the split off-center**: Turn **Split Point** (Knob 1) to about 70%, pushing the dividing line toward the right edge. The left panel now dominates the frame, with only a narrow strip of complementary color on the right.
2. **Add a thin gap**: Set **Gap Width** (Knob 2) to about 15%. A narrow black line marks the boundary, giving the composition a graphic, designed quality.
3. **Pull back the mix**: Lower **Mix** (Fader 12) to about 75%. The complementary panel softens, blending partially with the original. We get a tinted strip along the right edge rather than a hard chromatic split.
4. **Try the other extreme**: Turn **Split Point** to about 20%. Now the complementary panel dominates, with a narrow strip of the original on the left. Observe how the composition changes when the relationship between the two panels is reversed.
5. **Engage full negative**: Toggle **Vertical** (Switch 7) to **On** while the split is off-center. The narrow original strip next to the wide negative panel creates a dramatic framing effect.
6. **Sweep the mix**: Slowly move **Mix** from 0% to 100%. Watch the strip gradually emerge from the background as the effect fades in.

#### Settings

| Control | Value |
|---------|-------|
| Split Point | ~70% |
| Gap Width | ~15% |
| Offset | 50% |
| Zoom | 50% |
| Tilt | 50% |
| Tint | 50% |
| Vertical | On |
| Double | Off |
| Reverse | Off |
| Color Tint | Off |
| Bypass | Off |
| Mix | ~75% |

---
## Glossary

- **Chrominance**: The color information in a video signal, encoded as U and V components in YUV color space, representing hue and saturation independently of brightness

- **Complementary Colors**: Colors that sit opposite each other on the color wheel; in video processing, produced by inverting the chrominance channels

- **Diptych**: A work of art composed of two panels displayed side by side, traditionally hinged together

- **Interpolation**: A mathematical technique for calculating values between two known points; used here to crossfade between the original and processed video signals

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color

- **Negative Image**: An image in which both brightness and color are inverted (dark becomes light, and all hues shift to their complements)

- **Split Point**: The horizontal pixel position where the image divides into two panels, each receiving a different color treatment

- **YUV**: A color space that separates brightness (Y) from color (U and V), allowing independent processing of luminance and chrominance

---
