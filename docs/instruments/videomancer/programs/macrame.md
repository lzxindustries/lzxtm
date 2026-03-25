---
draft: true
sidebar_position: 183
slug: /instruments/videomancer/macrame
title: "Macrame"
image: /img/instruments/videomancer/macrame/macrame_hero_s1.png
description: "Fiber arts begin with repetition — a single knot tied again and again until a flat cord becomes a surface."
---

![Macrame hero image](/img/instruments/videomancer/macrame/macrame_hero_s1.png)
*Macrame weaving a luminous diamond lattice of knotted cords over a source image, with LFSR texture noise lending each strand an organic, handmade irregularity.*

---

## Overview

**Macrame** is a pattern overlay program that generates a repeating diamond lattice of diagonal cord lines with thickened knot points at every intersection. The lattice is drawn in real time on top of the incoming video, creating the appearance of a woven textile draped across the image. Cords can glow with their own brightness, tinted in warm cream tones, or borrow color from the source video beneath them. A pseudorandom noise generator adds subtle irregularity to every strand, so the result never looks perfectly mechanical.

At gentle settings, Macrame applies a faint grid of luminous threads over the picture: more ornamental frame than processing effect. At aggressive settings, the lattice dominates the image: thick ropes laced with bright knots obscure most of the source material, transforming it into a woven surface. The balance between cord and source is always under your control.

:::tip
Macrame is a ***processing*** program. It expects a live video input and overlays its lattice pattern on top of that signal. Without an input, you'll see the lattice pattern against black.
:::

### What's In a Name?

The name ***Macrame*** refers to the textile craft of knotting cords into decorative patterns. Traditional macramé produces diamond lattice structures through a series of half-hitch and square knots tied at regular intervals along hanging threads. The program generates exactly this geometry: two sets of diagonal lines crossing to form diamond cells, with round knot points swelling at each crossing. The word itself traces back through French and Arabic to a root meaning "striped cloth."

---

## Quick Start

1. Turn **Cord Sp** (Knob 1) fully clockwise to set wide spacing, then turn **Bright** (Knob 5) to about 75%. A widely-spaced grid of luminous diagonal lines appears over your source video.
2. Increase **Cord Thk** (Knob 3) clockwise. The thin diagonal lines thicken into visible strands.
3. Turn **Knot Size** (Knob 2) clockwise. Bright circular knots swell at every intersection where two diagonals cross. You're now looking at the characteristic macramé diamond lattice.
4. Sweep **Angle** (Knob 4) to skew the lattice diagonally. The whole pattern tilts as if you've pulled one corner of the textile.

---

## Parameters

![Videomancer front panel with Macrame loaded](/img/instruments/videomancer/macrame/macrame_control_panel.png)
*Videomancer's front panel with Macrame active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Cord Sp

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Cord Sp** sets the spacing between diagonal cord lines by selecting one of six power-of-two repeat intervals: 8, 16, 32, 64, 128, or 256 pixels. At 0%, fully counterclockwise, the lattice repeats every 8 pixels: a dense weave of fine threads. As you turn clockwise through each threshold, the repeat interval doubles and the diamond cells grow larger. At 100%, the lattice repeats every 256 pixels, producing a sparse grid of widely-separated cords.

:::note
Because spacing is quantized to powers of two, the control clicks through six discrete steps rather than sweeping smoothly. This is a design choice: power-of-two masks allow the FPGA to test cord positions with simple bitwise logic, keeping resource usage low.
:::

---

### Knob 2 — Knot Size

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Knot Size** controls the radius of the bright circles rendered at every lattice intersection: the points where two diagonal cords cross. Small values produce tight, jewel-like dots. Large values expand the knots into luminous discs that can overlap and merge into a continuous bright field. The knot radius is derived from the upper bits of the control value, mapping the full range to approximately 0–255 pixels of ***Manhattan distance***.

:::tip
At high values, knots overlap so much that the entire lattice becomes a continuous field of brightness. Pair this with the **Multiply** overlay mode (Switch 9) to create an unusual contrast mask.
:::

---

### Knob 3 — Cord Thk

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Cord Thk** sets the thickness of each diagonal cord line. The control maps to a threshold value between 1 and 16 pixels. Any pixel whose distance from the nearest cord centre is less than this threshold renders as a cord. At minimum, cords are single-pixel hairlines. At maximum, they swell into wide ribbons that nearly fill the diamond cells.

---

### Knob 4 — Angle

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Angle** offsets the vertical coordinate used in the diagonal computation, effectively skewing the entire lattice. At the midpoint, the lattice is symmetric: cords run at 45° diagonals. Turning the knob shifts the vertical reference, tilting the diamond pattern as if you've pulled one corner of the weave. Combined with **Animate** (Switch 10), the angle offset scrolls the lattice diagonally across the frame.

---

### Knob 5 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bright** controls the luminance level of the cord and knot pattern. At 0%, cords are invisible. As you turn clockwise, the lattice brightens. In **Add** overlay mode, this brightness is added to the source signal, so high values make cords glow hot against the image. In **Multiply** mode, cords replace the source, so Bright determines the absolute luminance of the pattern.

Knots render at 75% of the Bright value, with an additional pseudorandom noise texture layered on top. Cords render slightly dimmer: at roughly 75% of the knot brightness: with a subtler noise component.

---

### Knob 6 — Depth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Depth** is mapped in the VHDL but does not currently modulate the pipeline stages. It is reserved for future use as a depth-shading control that would darken cords based on their distance from the nearest knot, creating a three-dimensional woven appearance.

:::note
In the current firmware version, adjusting Depth has no visible effect on the output. The parameter is present so presets remain forward-compatible when depth shading is implemented.
:::

---

### Switch 7 — Pattern

| Property | Value |
|----------|-------|
| Off | Diamond |
| On | Chevron |
| Default | Diamond |

**Pattern** selects the lattice geometry. In the **Diamond** position, the program draws two independent sets of diagonal lines: one along the sum of horizontal and vertical coordinates, the other along the difference: forming a classic diamond grid. In the **Chevron** position, the pattern changes to an alternate coordinate mapping.

---

### Switch 8 — Color

| Property | Value |
|----------|-------|
| Off | Cream |
| On | Source |
| Default | Cream |

**Color** selects the tint of the cord and knot pattern. In the **Cream** position, cords are rendered with a warm, yellowish-brown chroma shift: U pulled below and V pushed above the neutral midpoint: evoking the color of natural hemp or cotton rope. In the **Source** position, cords and knots are rendered with neutral chroma (U and V at midpoint 512), producing a monochrome grayscale lattice.

:::tip
The Cream tint only appears when the lattice is visible. Background pixels (where no cord or knot is drawn) always pass the source video's color information, regardless of this switch.
:::

---

### Switch 9 — Overlay

| Property | Value |
|----------|-------|
| Off | Add |
| On | Multiply |
| Default | Add |

**Overlay** selects how the generated cord pattern composites onto the source video. In the **Add** position, the cord's brightness is added to the source (clamped to the maximum of 1023). The chroma is blended equally between the source and the cord tint. In the **Multiply** position, the cord pattern replaces the source entirely wherever a cord or knot is drawn (source video shows only through the gaps between cords.)

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** enables a slow diagonal scroll of the entire lattice pattern. When set to **On**, a frame counter increments on every vertical sync pulse and offsets the horizontal coordinate. The lattice drifts diagonally across the frame at approximately one pixel per frame. When set to **Off**, the lattice is stationary and locked to the video raster.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the delayed input signal directly to the output, skipping all pattern generation and compositing. The sync delay pipeline still runs, so toggling Bypass produces a clean, glitch-free transition. Use it for instant A/B comparison between the raw input and the overlaid result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the unprocessed source (dry) and the fully composited output (wet) using three parallel ***interpolator*** instances: one per YUV channel. At 0%, only the dry signal passes through. At 100%, only the processed composite is visible. Intermediate positions blend the two proportionally, allowing you to dial in exactly how much lattice overlay you want.

---

## Background

### Macramé craft and diamond lattice geometry

Macramé is one of the oldest textile techniques, predating the loom. It builds structure entirely from knots: no warp, no weft, no weaving shuttle. A series of cords hang from a mounting bar, and the artisan ties them together at regular intervals, creating a grid of diamond-shaped openings. The visual signature of macramé is that diamond lattice: two families of diagonal lines crossing in a regular pattern, with thickened points at every crossing where the knot sits.

The program reproduces this geometry using modular arithmetic. Two diagonal coordinates are computed: the sum and difference of horizontal and vertical pixel positions. A bitmask selects the repeat interval (the "cell size"), and a thickness threshold determines how far from the cell boundary a pixel must sit to qualify as "on a cord." Where both diagonal sets register as "on cord," the pixel is at an intersection: a knot.

### LFSR texture noise

A perfectly uniform digital lattice looks mechanical and synthetic. Real macramé cord has irregularities: slight variations in thickness, color, and twist from one segment to the next. The program injects ***pseudorandom noise*** from a 16-bit ***linear feedback shift register*** (LFSR) to break up the regularity.

The LFSR runs free at the pixel clock rate, producing a new 16-bit value every clock cycle. Six bits of this value are added to the cord brightness, creating pixel-by-pixel luminance variation along each strand. The noise is subtle: roughly 6% of the full brightness range: but enough to give the cords a textured, organic quality rather than a flat digital appearance.

### Overlay compositing

The program offers two compositing strategies. ***Additive*** overlay takes the source video and adds the cord pattern's brightness on top, clamping at the maximum value of 1023. This makes cords appear to glow: they brighten whatever lies beneath them. In areas where no cord is drawn, the source is dimmed by 1/16th to create subtle contrast between the lattice foreground and the source background.

***Replace*** overlay substitutes the cord pattern directly for the source signal wherever a cord or knot is drawn. The source video only shows through the gaps in the lattice. This mode is more aggressive, turning the lattice into a hard mask over the image.


---

## Signal Flow

### Signal Flow Notes

The pipeline runs in four register stages plus a four-clock interpolator, totaling eight clocks of latency. Diagonal coordinates are computed in Stage 1 using the sum and absolute difference of the pixel position: these two values partition the screen into diamond-shaped cells. Stage 2 measures each pixel's distance from the nearest cell edge (for cord detection) and from the nearest cell corner (for knot detection). Both distance tests use simple comparisons against thresholds derived from the Knob 2 and Knob 3 parameter values.

The compositing path in Stage 4 is asymmetric: in Additive mode, the pattern's brightness is halved before being added to the source, which preserves headroom and prevents constant clipping. Background pixels (those not on any cord or knot) are dimmed by 1/16th: a subtle shading that creates depth contrast between the lattice foreground and the video behind it.

:::note
The sync delay pipeline runs in parallel with the processing pipeline, ensuring that the delayed dry signal presented to the interpolator mix stage is perfectly time-aligned with the wet composite. This is what allows the Mix fader and Bypass switch to produce clean, glitch-free transitions.
:::


---

## Exercises

These exercises progress from a sparse luminous overlay to a dense, animated textile surface. Each one builds on the previous, engaging more of the parameter set.
### Exercise 1: Luminous Diamond Grid

![Luminous Diamond Grid result](/img/instruments/videomancer/macrame/macrame_ex1_s1.png)
*Luminous Diamond Grid — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic diamond lattice overlay that floats like a luminous net over the source video.

#### Key Concepts

- Cord spacing sets the repeat interval of the lattice
- Cord thickness and knot size control line weight and intersection emphasis
- Brightness determines how strongly the lattice glows over the source

#### Video Source

A live camera feed or recorded footage with moderate contrast and visible detail.

#### Steps

1. **Wide spacing**: Turn **Cord Sp** (Knob 1) fully clockwise for 256-pixel repeat. A sparse grid of faint diagonal lines appears.
2. **Visible cords**: Increase **Bright** (Knob 5) to about 80%. The diagonals glow distinctly.
3. **Thicken the strands**: Turn **Cord Thk** (Knob 3) to about 40%. Thin hairlines become visible ribbons.
4. **Reveal the knots**: Increase **Knot Size** (Knob 2) to about 40%. Bright knot circles swell at every intersection.
5. **Tighten the weave**: Slowly turn Cord Sp counterclockwise, stepping through the six spacing levels. Watch the lattice compress from a sparse net to a dense textile.

#### Settings

| Control | Value |
|---------|-------|
| Cord Sp | 100% |
| Knot Size | 40% |
| Cord Thk | 40% |
| Angle | 50% |
| Bright | 80% |
| Depth | 50% |
| Pattern | Diamond |
| Color | Cream |
| Overlay | Add |
| Animate | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Animated Textile Drift

![Animated Textile Drift result](/img/instruments/videomancer/macrame/macrame_ex2_s1.png)
*Animated Textile Drift — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A slowly drifting woven curtain that slides diagonally across the source video.

#### Key Concepts

- Animation offsets the lattice by one pixel per frame
- Angle skews the lattice diagonally
- Mix crossfades between the raw source and the overlaid result

#### Video Source

Slow-moving footage (clouds, water, or ambient visuals with gentle motion.)

#### Steps

1. **Start from Exercise 1**: Keep the diamond grid visible with moderate spacing (Cord Sp ~60%) and thickness.
2. **Enable animation**: Flip **Animate** (Switch 10) to **On**. The lattice begins drifting diagonally.
3. **Skew the angle**: Sweep **Angle** (Knob 4) from one extreme to the other. The drift direction and lattice tilt change.
4. **Blend it in**: Pull the **Mix** (Fader 12) down to about 50%. The lattice becomes semi-transparent, ghosting over the source.
5. **Switch to Multiply**: Flip **Overlay** (Switch 9) to **Multiply**. The lattice now replaces the source rather than adding to it (the source shows only through the diamond gaps.)
6. **Add color**: Flip **Color** (Switch 8) to **Cream**. The monochrome lattice takes on a warm, natural rope tone.

#### Settings

| Control | Value |
|---------|-------|
| Cord Sp | 60% |
| Knot Size | 35% |
| Cord Thk | 35% |
| Angle | 30% |
| Bright | 70% |
| Depth | 50% |
| Pattern | Diamond |
| Color | Cream |
| Overlay | Multiply |
| Animate | On |
| Bypass | Off |
| Mix | 50% |

---

### Exercise 3: Dense Woven Surface

![Dense Woven Surface result](/img/instruments/videomancer/macrame/macrame_ex3_s1.png)
*Dense Woven Surface — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dense, opaque textile that almost completely obscures the source, revealing it only through tiny diamond-shaped windows.

#### Key Concepts

- Tight spacing and thick cords create a near-opaque woven texture
- Knot size at maximum merges intersections into a continuous field
- Overlay mode fundamentally changes the composite character

#### Video Source

High-contrast footage with strong shapes: silhouettes, architectural lines, or high-contrast graphics.

#### Steps

1. **Dense weave**: Set **Cord Sp** (Knob 1) to about 15% (16-pixel spacing). Set **Cord Thk** (Knob 3) to about 70%. The lattice becomes a dense mesh.
2. **Big knots**: Turn **Knot Size** (Knob 2) to about 75%. Knots expand and merge, filling most of the diamond cells.
3. **Full brightness**: Set **Bright** (Knob 5) to 100%. The textile blazes.
4. **Replace mode**: Set **Overlay** (Switch 9) to **Multiply**. The source now peeks through only the tiny gaps not covered by cords or knots.
5. **Source color**: Flip **Color** (Switch 8) to **Source** to see monochrome cords against the colored source in the gaps.
6. **Animate and skew**: Enable **Animate** and sweep **Angle** while watching the dense weave crawl across the image.
7. **Pull back**: Use the **Mix** fader to dial the opaque textile back to a subtle overlay.

#### Settings

| Control | Value |
|---------|-------|
| Cord Sp | 15% |
| Knot Size | 75% |
| Cord Thk | 70% |
| Angle | 50% |
| Bright | 100% |
| Depth | 50% |
| Pattern | Diamond |
| Color | Source |
| Overlay | Multiply |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Additive Compositing**: A blending method that adds the brightness of an overlay pattern to the source signal, brightening wherever the overlay is present.

- **Diamond Lattice**: A repeating geometric pattern formed by two sets of diagonal lines crossing at regular intervals, creating diamond-shaped cells.

- **Interpolator**: A linear interpolation (lerp) circuit that crossfades between two input signals based on a blend factor.

- **LFSR**: Linear Feedback Shift Register; a simple digital circuit that produces a repeating sequence of pseudorandom values from a shift register with XOR feedback taps.

- **Manhattan Distance**: The sum of absolute horizontal and vertical distances between two points, measured along grid axes rather than in a straight line.

- **Modular Arithmetic**: Arithmetic performed with a fixed modulus (here, the cell size), causing values to wrap around and repeat at regular intervals.

- **Pseudorandom Noise**: A deterministic but statistically irregular sequence used to simulate randomness; produced here by an LFSR running at the pixel clock.

- **Replace Compositing**: A blending method that substitutes the overlay pattern directly for the source signal, showing the source only through gaps in the pattern.

- **YUV 4:4:4**: A video encoding format with one luma (Y) and two chroma (U, V) samples per pixel, each sampled at full resolution.

---
