---
draft: true
sidebar_position: 24
slug: /instruments/videomancer/blueprint
title: "Blueprint"
image: /img/instruments/videomancer/blueprint/blueprint_hero_s1.png
description: "Blueprint transforms a video signal into a cyanotype-style technical drawing."
---

![Blueprint hero image](/img/instruments/videomancer/blueprint/blueprint_hero_s1.png)
*Blueprint rendering white edge contours on a deep Prussian blue ground with dotted engineering grid overlay and dimension tick marks.*

---

## Overview

Blueprint transforms live video into the aesthetic of a ***cyanotype*** technical drawing. It extracts horizontal and vertical edges from the luminance channel and renders them as white contour lines on a deep Prussian blue background: the unmistakable look of an architectural blueprint. An optional engineering grid overlay adds dotted reference lines at regular intervals, and small dimension tick marks highlight grid intersections, completing the illusion of a hand-drafted plan.

At gentle settings, Blueprint produces clean, minimal contour drawings that trace the shapes in your source material with delicate white lines. Pushing the edge threshold lower and the brightness higher reveals a dense, intricate web of outlines that exposes every tonal boundary in the image. The engineering grid gives the output the structured, measured feeling of a technical document, turning any video signal into something that looks like it belongs on a drafting table.

:::tip
Blueprint is a ***processing*** program. It transforms whatever video you feed it, so the character of the source material directly shapes the output. High-contrast footage with strong geometric shapes produces the crispest, most architectural results.
:::

### What's In a Name?

The word ***blueprint*** originally referred to a specific photographic reproduction process. In the mid-1800s, the astronomer and chemist Sir John Herschel discovered that paper coated with iron-based chemicals turned deep ***Prussian blue*** when exposed to light: and areas shielded from light remained white. Architects and engineers adopted the process to copy technical drawings: the original was placed on sensitized paper, exposed to sunlight, and then washed, producing white lines on a rich blue ground. The term entered everyday language as a synonym for "a detailed plan," but the visual: white contours on blue: remains iconic. Blueprint recreates that distinctive palette digitally, using edge detection to generate the contour lines that cyanotype chemistry once traced from ink on vellum.

---

## Quick Start

1. Feed any video source into Videomancer with **Blueprint** loaded. The image immediately transforms into white edge contours on a deep blue ground. You are looking at the edges of your source material, drawn in light on Prussian blue paper.
2. Turn **Edge Thr** (Knob 1) counterclockwise to reveal finer edges, or clockwise to filter out everything but the strongest contours. Find the threshold that best captures the shapes in your source.
3. Increase **Brightness** (Knob 6) past the halfway mark. The contour lines become bolder and more prominent as the edge gain increases.
4. Flip the **Style** switch (Switch 7) to the "Green" position. A dotted engineering grid appears across the frame, adding the measured, schematic feel of a technical drawing.

---

## Parameters

![Videomancer front panel with Blueprint loaded](/img/instruments/videomancer/blueprint/blueprint_control_panel.png)
*Videomancer's front panel with Blueprint active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Edge Thr

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Edge Thr** sets the minimum edge strength required for a contour line to appear. At low values, the detector is highly sensitive: subtle gradients and fine textures all produce visible lines, and the output becomes dense with detail. As you increase the threshold, weaker edges are filtered out and only the boldest tonal boundaries survive. At maximum, only the very strongest edges in the image: hard silhouettes, sharp contrasts: generate contour lines. Everything else falls to the blue background.

:::note
The threshold interacts with **Brightness** (Knob 6). A high threshold with high brightness produces sparse but brilliant white contours. A low threshold with low brightness reveals dense but ghostly faint lines.
:::

---

### Knob 2 — Line W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Line W** is reserved for a future firmware update. In the current version, this control does not affect the visual output. Edge contour width can be broadened using the **Ticks** toggle (Switch 9) instead.

---

### Knob 3 — Grid Space

| Property | Value |
|----------|-------|
| Range | 8 – 64 |
| Default | 36 |

**Grid Space** selects the spacing between engineering grid lines. The control steps through five discrete power-of-two pixel spacings as you turn the knob: the tightest setting produces a dense mesh of closely spaced lines, and the widest setting creates an open lattice with generous spacing between lines. The grid is only visible when the **Style** switch (Switch 7) is set to "Green," or when the **Invert** switch (Switch 10) enables dimension tick marks independently.

:::tip
Wider grid spacing works well with high-resolution or complex source material, keeping the overlay from competing with the edge contours. A tight grid pairs nicely with simple, high-contrast subjects.
:::

---

### Knob 4 — Grid Opac

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Grid Opac** controls how bright the dotted grid lines appear. At low values, the grid is barely visible: a faint lattice lurking behind the edge contours. As you increase the value, the grid becomes more prominent against the blue background. Dimension tick marks (when enabled via the **Invert** switch) are always slightly brighter than the grid lines at any given setting, so they remain distinguishable.

:::note
In the inverted color mode (when the **Grid** switch is set to On), grid brightness is fixed and the **Grid Opac** knob has no effect.
:::

---

### Knob 5 — Blue Depth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Blue Depth** controls the luminance of the Prussian blue background. At the minimum setting, the background is nearly black, with only the faintest blue tint from the chrominance. As you increase the value, the blue ground brightens to a rich, medium Prussian blue. This is the "paper" of the drawing: darker values produce dramatic, high-contrast blueprints, while brighter values create a lighter, more washed-out look.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** controls the gain applied to the edge contour lines, determining how bright or dim they appear. The effect steps through five discrete intensity zones as you turn the knob clockwise. At the lowest setting, edges appear at one-quarter strength: very faint trace lines. Through the midrange, edges brighten to half strength and then full strength. Past the midpoint, edge brightness is boosted to double and then quadruple the detected value, making even subtle edges burn bright white.

:::tip
Set **Brightness** past the 60% mark and reduce **Edge Thr** for a look where every surface texture in the source material explodes into a blazing web of contour lines.
:::

---

### Switch 7 — Style

| Property | Value |
|----------|-------|
| Off | Blueprint |
| On | Green |
| Default | Blueprint |

**Style** selects between two visual modes. In the **Blueprint** position, the output shows clean edge contours on a blue ground without any grid overlay: a pure cyanotype aesthetic. In the **Green** position, a dotted engineering grid appears across the entire frame, adding horizontal and vertical reference lines at the spacing set by **Grid Space** (Knob 3). The grid lines are drawn as dotted lines (alternating pixels), matching the convention used in technical drafting.

---

### Switch 8 — Grid

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Grid** controls the color domain of the drawing. With Grid set to **Off**, white contour lines appear on a deep Prussian blue ground: the classic blueprint look. With Grid set to **On**, the scheme inverts: dark contour lines appear on a near-white ground, and grid lines and dimension marks become bright neutral tones. This "negative" mode resembles a photographic positive print or a whiteprint.

:::note
When the **Grid** switch is set to On (inverted mode), the **Blue Depth** and **Grid Opac** knobs have no effect (the background and grid brightness values are fixed.)
:::

---

### Switch 9 — Ticks

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Ticks** broadens the edge contour lines by lowering the detection threshold. When Ticks is set to **Off**, only edges exceeding the full **Edge Thr** threshold are drawn. When Ticks is set to **On**, the effective threshold is halved, allowing weaker edges to pass through. The result is thicker, more prominent contour lines and a denser overall drawing. Use Ticks as a quick way to make contours bolder without adjusting the threshold knob.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** adds small dimension markers at the intersections of the engineering grid. These markers appear as tiny bright dots where horizontal and vertical grid lines cross, resembling the ***tick marks*** found on architectural and engineering plans. The markers are visible even when the grid itself is hidden (Style set to "Blueprint"), which lets you scatter measurement reference points across the frame without the full grid overlay.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all edge detection, grid overlay, and color processing. The sync delay pipeline still aligns timing, so there is no glitch when switching. Use Bypass for instant A/B comparison between the raw source and the blueprint rendering.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (blueprint-processed) output. At 0%, the output is the original unprocessed video. At 100%, the output is the full blueprint effect. Intermediate values blend the two, letting you superimpose the blueprint contours over the original image at any desired strength. The default is 100% (fully wet).

:::tip
A mix around 30–50% overlays ghost-like blueprint contours onto the original footage, creating a layered, annotated look: as if technical drawings have been projected over live video.
:::

---

## Background

### The cyanotype process

The blueprint reproduction technique, properly called the ***cyanotype process***, was invented in 1842 by Sir John Herschel. It relies on the light-sensitivity of iron(III) compounds: a sheet of paper is coated with a solution of potassium ferricyanide and ferric ammonium citrate, dried in the dark, and then exposed to ultraviolet light through a translucent original. Where light passes through, the iron compounds react to form Prussian blue (ferric ferrocyanide). Where the original's ink blocks the light, the coating washes away, leaving white paper. The result is a white-on-blue negative image (the iconic blueprint.)

For over a century, this was the standard method for copying architectural and engineering drawings. The distinctive blue color was a side effect of the chemistry, not a design choice, but it became so strongly associated with technical plans that "blueprint" entered the language as a metaphor for any detailed scheme.

### Edge detection

Blueprint uses a ***first-order finite difference*** method to detect edges. For each pixel, it computes two differences: the horizontal difference between the current pixel and the previous pixel in the same row, and the vertical difference between the current pixel and the same pixel position on the previous line (stored in a ***block RAM*** line buffer). The absolute values of these two differences are summed to produce an ***edge strength*** value.

This approach is a close relative of the ***Sobel operator*** used in image processing, simplified for real-time FPGA implementation. It responds well to both hard silhouettes and gradual transitions, producing contour lines that thicken naturally around areas of high contrast.

### Engineering grid overlay

The engineering grid uses ***power-of-two bitmask*** comparison to generate evenly spaced reference lines without expensive division or modulo operations. The pixel's horizontal and vertical position counters are bitwise-ANDed with a mask derived from the **Grid Space** parameter. When the result is zero, the pixel falls on a grid boundary. The lines are drawn as dotted patterns: every other pixel is skipped: to match the visual convention of engineering graph paper. Small dimension markers appear as solid dots at grid intersections.


---

## Signal Flow

### Signal Flow Notes

The key architectural choice in Blueprint is the ***line buffer***. A single block RAM tile stores the previous line's luminance values, enabling the vertical edge difference computation. Without it, only horizontal edges (pixel-to-pixel changes within a row) would be detectable. The line buffer adds the vertical axis, producing contour lines that trace shapes in both dimensions.

The composite stage applies a strict priority: edges always draw on top of everything, dimension markers sit above grid lines, and grid lines sit above the background. This means edge contours are never obscured by the grid overlay, even when both are active and overlapping. The Prussian blue chrominance (U=650, V=350 in the 10-bit domain) is hardcoded and always present in the background and in inverted-mode edge lines (it is the signature color of the cyanotype aesthetic.)


---

## Exercises

These exercises build from a simple contour drawing to a full technical drawing with grid, markers, and inverted modes. Each one introduces new controls while reinforcing the ones already explored.
### Exercise 1: Clean Cyanotype Contours

![Clean Cyanotype Contours result](/img/instruments/videomancer/blueprint/blueprint_ex1_s1.png)
*Clean Cyanotype Contours — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean, minimal blueprint: white edge contours on deep blue, without any grid or markers. The goal is to find the threshold and brightness sweet spot for your source material.

#### Key Concepts

- Edge detection extracts contour lines from luminance differences
- Edge Thr controls sensitivity; Brightness controls edge gain
- Blue Depth sets the richness of the Prussian blue background

#### Video Source

A live camera feed or recorded footage with clear geometric shapes: architecture, furniture, or objects with defined edges work best.

#### Steps

1. **Load Blueprint** and feed your source. The image immediately becomes white contour lines on a blue ground.
2. **Sweep Edge Thr** (Knob 1) from minimum to maximum. At the low end, every subtle gradient generates a contour line and the image is dense with detail. At the high end, only the boldest silhouettes survive. Find a middle ground that captures the subject's main shapes without clutter.
3. **Adjust Brightness** (Knob 6) to the 60–70% range. The contour lines brighten noticeably as the gain shifts from normal to double.
4. **Adjust Blue Depth** (Knob 5). At low values, the background is nearly black. Increase it until you see a rich, saturated Prussian blue that contrasts well with the white lines.
5. **Try Ticks** (Switch 9) in the On position. The contour lines thicken as the detection threshold drops by half. Toggle it back and forth to compare thin precision lines versus bold outlines.

#### Settings

| Control | Value |
|---------|-------|
| Edge Thr | ~40% |
| Line W | 50% |
| Grid Space | 32 |
| Grid Opac | 50% |
| Blue Depth | 75% |
| Brightness | 65% |
| Style | Blueprint |
| Grid | Off |
| Ticks | Off |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Engineering Grid Overlay

![Engineering Grid Overlay result](/img/instruments/videomancer/blueprint/blueprint_ex2_s1.png)
*Engineering Grid Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A full engineering drawing: edge contours with a dotted reference grid and dimension tick marks, resembling a page from an architect's plan set.

#### Key Concepts

- The grid overlay uses power-of-two spacing for hardware-efficient dotted lines
- Grid Opac controls grid visibility against the blue ground
- Dimension markers highlight grid intersections

#### Video Source

Footage with a mix of geometric and organic shapes: a tabletop scene, a room interior, or a garden view provides good variety for the grid to interact with.

#### Steps

1. **Start from Exercise 1** settings: moderate Edge Thr, Brightness at 65%, Blue Depth at 75%.
2. **Flip Style** (Switch 7) to "Green." A dotted grid appears across the frame. The grid lines are faint at the default Grid Opac setting.
3. **Increase Grid Opac** (Knob 4) until the grid is clearly visible but doesn't overpower the edge contours. Around 60–70% is a good starting point.
4. **Step through Grid Space** (Knob 3). Turn the knob slowly and notice the grid snapping between five discrete spacings: from very tight to very wide. Choose a spacing that frames your subject well.
5. **Enable dimension markers**: flip the **Invert** switch (Switch 10) to On. Small bright dots appear at the intersections of the grid lines, completing the technical drawing look.
6. **Experiment**: try disabling the grid overlay (Style back to "Blueprint") while keeping Invert On. The dimension markers remain visible as scattered reference dots without connecting grid lines.

#### Settings

| Control | Value |
|---------|-------|
| Edge Thr | ~40% |
| Line W | 50% |
| Grid Space | 32 |
| Grid Opac | 65% |
| Blue Depth | 70% |
| Brightness | 65% |
| Style | Green |
| Grid | Off |
| Ticks | Off |
| Invert | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Negative Whiteprint

![Negative Whiteprint result](/img/instruments/videomancer/blueprint/blueprint_ex3_s1.png)
*Negative Whiteprint — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A "whiteprint": the photographic positive of a blueprint, with dark contour lines on a bright ground, blended back over the original video.

#### Key Concepts

- The Grid switch inverts the color domain: dark contours on a white ground
- Inverted mode fixes background and grid brightness, overriding Blue Depth and Grid Opac
- Mix blends the blueprint effect with the original source

#### Video Source

High-contrast footage such as a performer against a bright background, text on a screen, or backlit architecture (anything with strong silhouettes.)

#### Steps

1. **Start with default settings** and feed your source.
2. **Flip Grid** (Switch 8) to On. The color scheme inverts: the background becomes near-white and the edge contours turn dark blue. This is the "whiteprint" or positive-print mode.
3. **Enable the grid overlay** by flipping **Style** (Switch 7) to "Green." The dotted grid now appears as bright neutral lines against the white ground (subtle but visible.)
4. **Lower Edge Thr** (Knob 1) to capture fine detail. In inverted mode, dense contour lines create a delicate pen-and-ink quality.
5. **Reduce Mix** (Fader 12) to about 40%. The whiteprint contours blend over the original footage, creating a layered look (like technical annotations projected onto live video.)
6. **Compare**: flip **Bypass** (Switch 11) On and Off to see the source alone versus the blended result.

#### Settings

| Control | Value |
|---------|-------|
| Edge Thr | ~30% |
| Line W | 50% |
| Grid Space | 48 |
| Grid Opac | 50% |
| Blue Depth | 70% |
| Brightness | 60% |
| Style | Green |
| Grid | On |
| Ticks | Off |
| Invert | Off |
| Bypass | Off |
| Mix | 40% |

---
## Glossary

- **Block RAM**: A dedicated memory tile on an FPGA, used here to store one full line of luminance values for vertical edge computation.

- **Cyanotype**: A photographic printing process that produces white images on a Prussian blue background, originally used to copy architectural drawings.

- **Edge Detection**: The process of identifying boundaries in an image where pixel brightness changes abruptly, producing contour lines.

- **Finite Difference**: A mathematical operation that approximates a derivative by subtracting adjacent sample values; used here to detect edges.

- **Interpolator**: A hardware module that crossfades between two values based on a parameter, used for the wet/dry mix.

- **Line Buffer**: A memory buffer that stores the pixel values of the previous scan line, enabling comparisons between vertically adjacent pixels.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness.

- **Power-of-Two Bitmask**: A technique for detecting evenly spaced positions using bitwise AND instead of expensive division or modulo operations.

- **Prussian Blue**: A deep blue pigment (ferric ferrocyanide) produced by the cyanotype process; the signature color of architectural blueprints.

---
