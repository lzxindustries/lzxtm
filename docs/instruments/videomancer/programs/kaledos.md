---
draft: true
sidebar_position: 154
slug: /instruments/videomancer/kaledos
title: "Kaledos"
image: /img/instruments/videomancer/kaledos/kaledos_hero_s1.png
description: "In 1816, the Scottish physicist Sir David Brewster patented the kaleidoscope — a tube of mirrors that transforms a handful of colored fragments into an infinite tiling of perfect symmetry."
---

![Kaledos hero image](/img/instruments/videomancer/kaledos/kaledos_hero_s1.png)
*Kaledos transforming a live camera feed into an eight-fold kaleidoscopic reflection with per-sector hue rotation and circular vignette mask.*

---

## Overview

**Kaledos** is a kaleidoscope mirror that divides the screen into a tiled grid of identical sectors, reflecting alternate sectors to create the bilateral symmetry of a real kaleidoscope. A single strip of video is captured from the source, stored in a line buffer, and then replayed across every sector on screen. The result is the same kind of mesmerizing, endlessly unfolding pattern you see when you peer into a tube of angled mirrors (except Kaledos does it in real time with live video.)

At low fold counts, the effect is a simple split-screen mirror. At higher fold counts, the sectors become smaller and the symmetry pattern grows more intricate, producing crystalline tile grids that shimmer and shift as the source material moves. Enabling hue rotation tints each sector a different color, evoking the translucent glass fragments of a physical kaleidoscope. A circular mask and vignette complete the illusion, framing the pattern inside a round viewport just like looking through the eyepiece of Brewster's original instrument.

:::tip
***The diamond offset is the secret ingredient.*** Odd rows are shifted by half a strip width, creating a brick-like pattern that links adjacent sectors together. This produces the diagonal symmetry lines characteristic of a real kaleidoscope, not just a simple rectangular grid.
:::

### What's In a Name?

The name ***Kaledos*** comes from the Greek ***kalos*** (beautiful) and ***eidos*** (form): the same roots as ***kaleidoscope***, the optical instrument patented by Sir David Brewster in 1817. The shortened form nods to the program's concise, elegant approach: a single strip of video, reflected and rotated, produces an infinity of beautiful forms.

---

## Quick Start

1. Set **Fold Count** (Knob 1) to 4 or higher. The screen divides into a grid of mirrored tiles, each showing the same slice of the input reflected back and forth.
2. Turn **Rot Speed** (Knob 4) to about 25%. The pattern begins to scroll continuously, creating a slow kaleidoscopic rotation.
3. Enable **Hue Rotate** (Switch 7). Each sector takes on a different tint: golds, magentas, teals, and greens appear as the UV channels permute across sectors.
4. Enable **Circle Mask** (Switch 9) and **Vignette** (Switch 8). The rectangular screen melts into a soft-edged circular viewport, framing the pattern like a real kaleidoscope eyepiece.

---

## Parameters

![Videomancer front panel with Kaledos loaded](/img/instruments/videomancer/kaledos/kaledos_control_panel.png)
*Videomancer's front panel with Kaledos active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Fold Count

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 2 |

**Fold Count** selects the number of reflective symmetry divisions. The knob steps through eight discrete presets: 2, 3, 4, 6, 8, 12, 16, and 24 folds. Each fold count defines a corresponding sector width and height: at 2 folds, each sector spans half the screen; at 24 folds, sectors shrink to narrow slivers just 53 pixels wide.

Low fold counts produce bold, graphic mirrors. High fold counts produce dense, crystalline tile patterns where the original source material is barely recognizable.

:::note
Fold Count uses the top 3 bits of the knob, so the eight steps are evenly spaced across the full rotation.
:::

---

### Knob 2 — Sector Ofs

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Sector Ofs** (Sector Offset) shifts the starting phase of the tile pattern. Turning this knob slides the pattern horizontally, changing which slice of the source video appears in each sector. The offset is combined with the rotation DDS accumulator, so it acts as a manual position control layered on top of any automatic rotation from **Rot Speed**.

At 0°, the pattern starts at the default position. Sweeping through 360° cycles the entire pattern through one full repetition.

---

### Knob 3 — Zoom

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Zoom** magnifies the source video within each sector. At 0%, each sector shows a one-to-one mapping of the captured strip. As the value increases, the read address is progressively divided, zooming into the center of the strip. The zoom happens in power-of-two steps (the top two bits select 1×, 2×, 4×, or 8× magnification.)

:::tip
At 8× zoom, each sector shows only a tiny sliver of the source, stretched and reflected. Combined with high fold counts, this produces abstract, nearly geometric patterns disconnected from the source content.
:::

---

### Knob 4 — Rot Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Rot Speed** controls the rate of continuous pattern scrolling. A ***direct digital synthesis*** (DDS) accumulator advances the start offset by a small amount each frame, creating smooth, automatic rotation of the entire tile grid. At 0%, the pattern is static. As the value increases, the pattern scrolls faster.

The default value places the knob near the slow end of its range. Moderate settings produce a gentle, hypnotic drift. High settings create rapid scrolling that can produce strobing at the tile boundaries.

---

### Knob 5 — Center X

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Center X** positions the horizontal center of the source capture region. The captured strip of video is centered on this coordinate. At 50% (default), the capture region is centered on the screen. Turning the knob left or right slides the capture window, changing which part of the input feeds the kaleidoscope.

Center X also sets the horizontal origin for the vignette and circular mask, so the brightness falloff and mask edge track the capture region.

---

### Knob 6 — Center Y

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Center Y** positions the vertical center of the vignette and circular mask. At 50% (default), the vignette is centered vertically on the screen. Turning the knob repositions the soft brightness falloff and the circular mask boundary.

:::note
Center Y affects only the vignette and mask, not the source capture region. Vertical tiling is controlled by the strip counter and fold count.
:::

---

### Switch 7 — Hue Rotate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Hue Rotate** enables per-sector color shifting. When On, each sector's U and V color channels are permuted based on the sector index, cycling through four 90° hue rotations. Sector 0 passes color unchanged. Sector 1 swaps and inverts the chrominance axes, shifting hue by 90°. Sector 2 inverts both axes (180°). Sector 3 swaps in the opposite direction (270°).

The result is a stained-glass effect: adjacent sectors display the same brightness pattern in complementary colors. Because the sector index accumulates both horizontal and vertical strip counts, the color pattern forms a diagonal checker.

---

### Switch 8 — Vignette

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Vignette** enables a radial brightness falloff from the center of the screen. When On, pixels farther from the center are progressively darkened using a ***Manhattan distance*** calculation (|dx| + |dy|). The falloff is linear, reaching black at approximately 1000 pixels from center.

Vignette affects only luminance: colors at the edge fade to dark but retain their hue. Combined with **Circle Mask**, it creates a smooth transition from bright center to masked edge.

---

### Switch 9 — Circle Mask

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Circle Mask** enables a circular cutout that blacks out everything outside a fixed radius. Pixels beyond the mask boundary are replaced with black (Y = 0, U = V = neutral). The mask uses an ***octagonal distance approximation***: max(|dx|, |dy|) + min(|dx|, |dy|) / 2, which closely approximates a true circle without requiring a square root or multiplier.

The mask radius is fixed at 360 pixels: the vertical half-height of the 720p frame: inscribing the largest circle that fits within the screen height.

---

### Switch 10 — Mirror/Rot

| Property | Value |
|----------|-------|
| Off | Mirror |
| On | Rotate |
| Default | Mirror |

**Mirror/Rot** selects between two tiling modes. In **Mirror** mode (default), odd-numbered horizontal strips are reflected, producing bilateral symmetry across each virtual mirror line. In **Rotate** mode, all strips tile without reflection: the same strip repeats identically in every sector, producing a wallpaper-like pattern without mirror symmetry.

:::tip
Mirror mode creates the classic kaleidoscope look with symmetry lines. Rotate mode is useful for creating scrolling marquee or tiling texture effects, especially when combined with **Rot Speed**.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all kaleidoscope processing. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** blends between the dry (unprocessed) input and the wet (kaleidoscope) output using a per-channel ***interpolator***. At 0%, the original input passes through unchanged. At 100% (default), the full kaleidoscope effect is visible. Intermediate values create a ghostly double exposure where the source image is visible underneath the tiled pattern.

---

## Background

### Kaleidoscopes and Reflective Symmetry

The kaleidoscope was invented by Scottish physicist Sir David Brewster in 1816 and patented in 1817. Brewster's original design used two or three flat mirrors arranged in a triangular tube, with loose beads or glass fragments at one end. When light enters the tube, the mirrors reflect the fragments into a symmetrical pattern visible through the eyepiece. Brewster later described the "polycentral" variant: kaleidoscopes with more than three mirrors: which produced tessellating tile patterns that filled the entire field of view.

Kaledos implements a digital version of the polycentral kaleidoscope. The "mirrors" are horizontal strip boundaries where the read direction reverses, and the "fragments" are live video. The fold count selects how many virtual mirrors divide the image, from a simple two-fold bilateral mirror up to a 24-fold crystal lattice.

### The Diamond Offset

A rectangular grid of reflected tiles doesn't quite look like a kaleidoscope: it looks like wallpaper. Real kaleidoscopes produce angular symmetry lines that radiate from a center point, creating star-shaped or hexagonal patterns. Kaledos approximates this by applying a ***diamond offset***: on odd-numbered vertical strips, the horizontal start position shifts by half a strip width. This produces a brick-like stagger that links adjacent rows together along diagonal lines, creating the visual impression of angular symmetry even though the underlying geometry is rectangular.

### Direct Digital Synthesis

The continuous rotation is driven by a ***direct digital synthesis*** (DDS) accumulator: a counter that adds a fixed increment on every video frame (at vsync). The accumulated value wraps modulo the strip width, creating a smooth, repeating scroll. DDS is the same technique used in radio frequency synthesizers and audio oscillators to generate precise periodic waveforms from a fixed clock.

The sector offset knob adds a manual phase shift to the DDS output. Together, the two controls give you both a static position and a continuous rotation speed, just like the outer ring and inner tube of a physical kaleidoscope.


---

## Signal Flow

### Signal Flow Notes

The two main data paths: capture and reconstruction: operate simultaneously on the same scanline. While the current line's pixels are being written into the line buffer at the source capture position, the previous line's data is being read back at mirrored/zoomed addresses to reconstruct the tile pattern. This single-line buffer approach means the kaleidoscope effect is strictly horizontal: each output line is built from one input line's worth of data, and vertical tiling is achieved by repeating the same strip counter pattern across rows.

The hue rotation and vignette/mask stages sit between the BRAM read and the interpolator, operating on the reconstructed tile data. This means the vignette darkens the kaleidoscope pattern, not the source material, and hue rotation colors the reflected tiles rather than the captured strip.

:::note
Because the line buffer stores only one scanline, the vertical dimension relies on the natural frame-to-frame coherence of the source video. Each row independently samples the input at the same horizontal position, so vertically smooth source material produces vertically smooth tiles.
:::


---

## Exercises

These exercises progress from a simple mirror to a full stained-glass kaleidoscope. Each one engages more of the processing chain, building toward the complete effect.
### Exercise 1: Simple Mirror

![Simple Mirror result](/img/instruments/videomancer/kaledos/kaledos_ex1_s1.png)
*Simple Mirror — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean bilateral mirror: the classic "hall of mirrors" look: then expand it into a multi-fold tiling.

#### Key Concepts

- Fold count controls the number of symmetry divisions
- Mirror mode reflects alternate strips
- Center X positions the capture region

#### Video Source

A live camera feed or footage with recognizable subjects and some movement.

#### Steps

1. **Two-fold mirror**: Set **Fold Count** (Knob 1) fully counterclockwise (2 folds). The screen splits into two halves, mirrored along the center. Move your hand in front of the camera to confirm the bilateral symmetry.
2. **Shift the axis**: Turn **Center X** (Knob 5) left and right. The mirror axis slides across the frame, changing where the reflection originates.
3. **More folds**: Slowly turn Fold Count clockwise through 3, 4, 6, 8. At each step, the number of tiled sectors increases and the tiles shrink.
4. **Diamond pattern**: At 6 or 8 folds, look at the relationship between adjacent rows. The half-strip offset creates diagonal symmetry lines running through the tile grid.
5. **Rotate mode**: Flip **Mirror/Rot** (Switch 10) to **Rotate**. The bilateral symmetry disappears and tiles repeat identically, creating a wallpaper pattern.

#### Settings

| Control | Value |
|---------|-------|
| Fold Count | 4 |
| Sector Ofs | 0° |
| Zoom | 0% |
| Rot Speed | 0% |
| Center X | 50% |
| Center Y | 50% |
| Hue Rotate | Off |
| Vignette | Off |
| Circle Mask | Off |
| Mirror/Rot | Mirror |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Colored Glass

![Colored Glass result](/img/instruments/videomancer/kaledos/kaledos_ex2_s1.png)
*Colored Glass — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A stained-glass kaleidoscope with colored sectors, a soft vignette, and a circular viewport.

#### Key Concepts

- Hue rotation creates per-sector color shifts
- Vignette and circle mask frame the pattern
- Zoom magnifies the source within each tile

#### Video Source

Footage with rich color (flowers, fabrics, neon signs, or color bars.)

#### Steps

1. **Set the base**: Set **Fold Count** to 6 or 8 folds for a dense tile grid.
2. **Add color**: Enable **Hue Rotate** (Switch 7). Each sector shifts hue by 90°, creating a four-color mosaic across the tile grid. Adjacent tiles appear in complementary colors.
3. **Zoom in**: Increase **Zoom** (Knob 3) to about 33%. The source magnifies within each tile, reducing detail and emphasizing color and shape.
4. **Frame it**: Enable **Circle Mask** (Switch 9). The tiled pattern is cropped to a circle, like looking through a tube.
5. **Soften the edge**: Enable **Vignette** (Switch 8). The edges darken smoothly, completing the kaleidoscope eyepiece illusion.
6. **Reposition**: Adjust **Center X** and **Center Y** to move the vignette and mask center.

#### Settings

| Control | Value |
|---------|-------|
| Fold Count | 6 |
| Sector Ofs | 0° |
| Zoom | ~33% |
| Rot Speed | 0% |
| Center X | 50% |
| Center Y | 50% |
| Hue Rotate | On |
| Vignette | On |
| Circle Mask | On |
| Mirror/Rot | Mirror |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Spinning Mandala

![Spinning Mandala result](/img/instruments/videomancer/kaledos/kaledos_ex3_s1.png)
*Spinning Mandala — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A continuously rotating mandala pattern with automatic motion and wet/dry blending.

#### Key Concepts

- DDS rotation creates continuous pattern scrolling
- Sector offset adds manual phase control
- Mix creates double-exposure blending

#### Video Source

Footage with strong textures and contrast (water, foliage, or abstract patterns.)

#### Steps

1. **Build the pattern**: Set **Fold Count** to 8 or higher. Enable **Hue Rotate** and **Circle Mask** to create a dense, colorful mandala.
2. **Start rotating**: Slowly increase **Rot Speed** (Knob 4) from 0%. The entire tile pattern begins to scroll, creating the illusion of rotation. Find a gentle speed that feels hypnotic rather than frantic.
3. **Manual offset**: While the pattern scrolls, turn **Sector Ofs** (Knob 2). The offset adds to the rotation, letting you push the pattern ahead or pull it back without changing the speed.
4. **Zoom and frame**: Add some **Zoom** (~25%) and enable **Vignette** to create a framed, magnified mandala.
5. **Double exposure**: Pull the **Mix** fader (Fader 12) down to about 60%. The source video becomes visible underneath the kaleidoscope pattern, creating a translucent overlay.
6. **Explore**: Sweep Center X while the pattern rotates. The capture region shifts, feeding different source material into the spinning mandala.

#### Settings

| Control | Value |
|---------|-------|
| Fold Count | 7 |
| Sector Ofs | 0° |
| Zoom | ~25% |
| Rot Speed | ~40% |
| Center X | 50% |
| Center Y | 50% |
| Hue Rotate | On |
| Vignette | On |
| Circle Mask | On |
| Mirror/Rot | Mirror |
| Bypass | Off |
| Mix | ~60% |

---
## Glossary

- **Bilateral Symmetry**: A pattern that is identical on both sides of a mirror line, like a butterfly's wings.

- **BRAM**: Block RAM: dedicated memory blocks inside the FPGA, used here to store one scanline of captured video.

- **DDS**: Direct Digital Synthesis: a technique for generating periodic waveforms by accumulating a phase increment on each clock cycle.

- **Diamond Offset**: A half-strip horizontal shift applied to odd rows, creating a brick-like stagger that produces diagonal symmetry lines.

- **Fold Count**: The number of reflective symmetry divisions in a kaleidoscope pattern; higher counts produce denser, more intricate tiles.

- **Hue Rotation**: Shifting the hue of an image by permuting or inverting the U and V chrominance channels.

- **Interpolator**: A blending unit that crossfades between two signals based on a mix parameter.

- **Manhattan Distance**: The sum of the absolute horizontal and vertical distances between two points, named after the grid-like street layout of Manhattan.

- **Octagonal Approximation**: A computationally cheap estimate of circular distance: max(|dx|, |dy|) + min(|dx|, |dy|) / 2.

- **Sector**: One tile in the kaleidoscope pattern, containing a reflected or repeated copy of the source strip.

- **Strip Counter**: A modular counter that wraps at the sector width, tracking position within the current tile.

- **Vignette**: A gradual darkening of the image toward the edges, simulating the light falloff of a physical lens or tube.

---
