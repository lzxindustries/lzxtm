---
draft: true
sidebar_position: 105
slug: /instruments/videomancer/facet
title: "Facet"
image: /img/instruments/videomancer/facet/facet_hero_s1.png
description: "Most video effects blur, bend, or color-grade a continuous image."
---

![Facet hero image](/img/instruments/videomancer/facet/facet_hero_s1.png)
*Facet dividing a live video frame into flat-shaded crystal cells with dark leadwork outlines, producing a mosaic resembling hand-cut stained glass.*

---

## Overview

Facet is a spatial tessellation effect that cuts the video frame into a grid of rectangular cells, each painted with a single sampled color. The result looks like looking through a faceted crystal or a stained glass window: the original image is still recognizable by its broad shapes and colors, but all fine detail within each cell has been replaced by a single flat tone. Black outlines at the cell boundaries complete the illusion, adding dark leadwork between the colored panes. Toggle the outlines off, and the cells butt together seamlessly like bathroom tiles; toggle flat shading off, and the original image shows through a black grid overlay.

At conservative settings: small cells, thin outlines: Facet produces a gentle mosaic that softens the image without destroying it. At extreme settings: large cells, heavy leadwork: the video collapses into an abstract quilt of bold color blocks separated by thick dark borders. Enable **Mono** to strip the chroma entirely, reducing the mosaic to a grayscale crystal lattice. The wet/dry **Mix** fader lets you dissolve smoothly between the faceted effect and the unprocessed source, opening up a range of semi-transparent overlay textures.

:::tip
Facet's signature look is the combination of flat shading and outlines. Together, they turn any video source into a stained glass window in real time.
:::

### What's In a Name?

A ***facet*** is one of the flat, polished surfaces of a cut gemstone. When light enters a diamond or a prism, each facet reflects a single color at a single angle: a tiny, flat mirror. Facet does the same thing to video: it cuts the image into flat faces, each capturing one color from the source. The whole frame becomes a jewel, its surface divided into clean geometric planes.

---

## Quick Start

1. With **Flat Shade** (Switch 9) and **Outlines** (Switch 8) both set to **On** (their defaults), slowly turn **Cell Size** (Knob 1) clockwise. The image breaks into progressively larger blocks of uniform color, like zooming into a mosaic.
2. Increase **Edge Width** (Knob 2). Black borders appear at the boundaries of each cell, dividing the mosaic into a stained glass grid. Wider edges create heavier leadwork.
3. Toggle **Flat Shade** (Switch 9) to **Off**. The original image shows through the grid: only the dark outlines remain, overlaid like a wire mesh on the source video.
4. Sweep the **Mix** fader (Fader 12) from right to left. The faceted effect fades into the original, creating a ghostly overlay at intermediate positions.

---

## Parameters

![Videomancer front panel with Facet loaded](/img/instruments/videomancer/facet/facet_control_panel.png)
*Videomancer's front panel with Facet active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Cell Size

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Cell Size** controls the width and height of each rectangular cell in the mosaic grid. At 0%, cells are only a few pixels across: a fine tessellation barely distinguishable from the original image. As you turn the knob clockwise, cells grow wider and taller, and the mosaic becomes coarser. At 100%, cells are large blocks spanning dozens of pixels, reducing the image to a bold grid of flat color panels. Because cell width and height are equal, all cells are square.

---

### Knob 2 — Edge Width

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Edge Width** controls the thickness of the black outlines drawn at cell boundaries when **Outlines** (Switch 8) is enabled. At 0%, the outlines are invisible: zero pixels wide: even if the Outlines toggle is on. As Edge Width increases, a dark border grows along the left and top edges of each cell, creating heavier and heavier leadwork. At maximum, the outlines consume up to seven pixels of each cell edge, leaving thick black bars between the colored panes.

:::note
Edge Width has no visible effect unless **Outlines** (Switch 8) is set to **On**. With Outlines off, the Edge Width knob does nothing.
:::

---

### Knob 3 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contrast** is reserved for a future firmware update. It is intended to apply a ***proc amp*** contrast adjustment to the faceted image, scaling pixel values around their midpoint to make the mosaic punchier or flatter. This control currently has no visible effect on the output.

---

### Knob 4 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** is reserved for a future firmware update. It is intended to apply a brightness offset to the faceted image, shifting all pixel values up or down to lighten or darken the mosaic. This control currently has no visible effect on the output.

---

### Knob 5 — Color Reduce

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Color Reduce** is reserved for a future firmware update. It is intended to ***quantize*** color values within each cell, snapping them to a smaller palette of distinct levels. Lower values would produce fewer colors, creating a bolder, more poster-like mosaic. This control currently has no visible effect on the output.

---

### Knob 6 — Randomize

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |

**Randomize** is reserved for a future firmware update. It is intended to add spatial jitter to cell boundaries, breaking the rigid grid into an irregular, organic tessellation: something closer to a ***Voronoi diagram*** than a regular checkerboard. This control currently has no visible effect on the output.

---

### Switch 7 — Hex Grid

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Hex Grid** is reserved for a future firmware update. It is intended to switch the cell tessellation from a rectangular grid to a hexagonal layout, where cells interlock like honeycomb. This toggle currently has no visible effect on the output.

---

### Switch 8 — Outlines

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Outlines** enables or disables the black borders drawn at cell boundaries. Default: **On**. When enabled, pixels at the left edge and top edge of each cell are rendered as solid black (luminance zero, neutral chroma), creating dark leadwork lines between cells. The width of these outlines is controlled by **Edge Width** (Knob 2). When disabled, cells sit edge to edge with no visible border, and the mosaic becomes a seamless patchwork of flat color.

---

### Switch 9 — Flat Shade

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Flat Shade** enables or disables flat shading of cell interiors. Default: **On**. When enabled, each cell is filled with a single color sampled from the first pixel at the cell boundary: effectively the top-left corner of the cell. All original image detail within the cell is replaced by this uniform tone. When disabled, the original video image passes through unmodified, and only the outlines (if enabled) are drawn over it. Turning Flat Shade off transforms Facet from a mosaic effect into a grid overlay effect.

:::tip
With **Flat Shade** off and **Outlines** on, Facet becomes a simple grid generator. The dark lines divide the image into cells without altering the video content inside them: useful for compositional framing or a retro CRT-monitor aesthetic.
:::

---

### Switch 10 — Mono

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mono** converts the flat-shaded cells to monochrome. Default: **Off**. When enabled, the chroma channels (U and V) are replaced with neutral midpoint values, removing all color and leaving only grayscale facets. The luminance values are preserved, so the brightness structure of the mosaic remains intact. Mono only has a visible effect when **Flat Shade** (Switch 9) is also enabled; with Flat Shade off, the chroma passes through from the original signal unmodified.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Facet processing stages. Default: **Off**. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the faceted result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the wet/dry blend between the faceted (processed) signal and the original (delayed) video. At 0%, fully left, the output is entirely dry: the original image with no facet effect. At 100% (default), fully right, the output is entirely wet: the full mosaic. Intermediate values create a semi-transparent overlay where the mosaic sits ghosted on top of the source, producing a soft, dreamlike double exposure.

---

## Background

### Spatial Tessellation

***Tessellation*** is the art of dividing a flat surface into smaller shapes that fit together without gaps or overlaps. Floor tiles, honeycomb, and stained glass windows are all tessellations. In mathematics, the study of tessellations goes back to ancient Greece, but the term entered popular culture through the impossible geometries of M. C. Escher. Facet implements the simplest possible tessellation: a regular grid of identical squares. Each square cell captures one color from the underlying image, discarding all the fine detail within its borders.

### Flat Shading

In computer graphics, ***flat shading*** is the earliest and most basic technique for coloring a polygon. Each face receives a single, uniform color: there is no smooth gradient across the surface. This was the standard rendering method for early 3D games and CAD software because it required the fewest calculations per polygon. Facet applies the same idea to 2D video: each cell in the grid is a "polygon" filled with a single sampled color. The result is a mosaic of flat planes that looks hand-cut, like a stained glass window or a low-polygon 3D model viewed head-on.

### Stained Glass and Leadwork

The visual metaphor at the heart of Facet is the stained glass window. In traditional glasswork, colored glass pieces are cut to shape and joined by strips of lead called ***came***. The dark came lines serve a structural purpose: holding the glass together: but they also define the visual rhythm of the window, separating the color fields and giving the design its characteristic boldness. In Facet, the black outlines play the same role. They are not structurally necessary, but they define the visual boundaries between cells and give the mosaic its weight and presence.


---

## Signal Flow

### Signal Flow Notes

The pipeline has two key interactions to understand. First, ***edge detection takes priority over flat shading***. If a pixel lies at the left or top edge of a cell and outlines are enabled, it is always rendered black regardless of the Flat Shade or Mono settings. Second, ***Mono only affects the flat shading path***. When Flat Shade is off, the original chroma passes through untouched, and the Mono toggle has no visible effect.

The 8-clock sync and data delay pipeline preserves a time-aligned copy of the original input. This delayed copy serves two roles: it feeds the "dry" side of the wet/dry mix, and it provides the sync signals (hsync, vsync, field) for the output. Because all three interpolator instances share the same enable signal, the Y, U, and V mix outputs are always phase-aligned.

:::note
Five TOML-declared parameters: **Contrast**, **Brightness**, **Color Reduce**, **Randomize**, and **Hex Grid**: are mapped to hardware registers but are not yet connected to the processing pipeline. They are reserved for a future firmware update and currently have no visible effect.
:::


---

## Exercises

These exercises progress from a basic stained glass look to monochrome abstraction, gradually exploring the interactions among cell size, outlines, flat shading, and monochrome mode.
### Exercise 1: Stained Glass Window

![Stained Glass Window result](/img/instruments/videomancer/facet/facet_ex1_s1.png)
*Stained Glass Window — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A stained glass window effect with bold colored cells and prominent dark borders.

#### Key Concepts

- Flat shading replaces all detail within a cell with a single sampled color
- Outlines create dark leadwork at cell boundaries
- Edge Width controls the heaviness of the leadwork

#### Video Source

Colorful footage with large areas of distinct hue: flowers, neon signs, painted murals, or color bar test patterns.

#### Steps

1. **Set the cell size**: Turn **Cell Size** (Knob 1) to roughly 60%. The image breaks into a medium-coarse mosaic of flat-colored squares.
2. **Add leadwork**: With **Outlines** (Switch 8) already on, increase **Edge Width** (Knob 2) to about 50%. Thick black borders appear between cells, completing the stained glass illusion.
3. **Refine the grid**: Sweep Cell Size slowly. Smaller cells preserve more of the source's shape; larger cells create bolder, more abstract panels. Find the sweet spot where the subject is still recognizable but clearly "glassed."
4. **Compare**: Toggle **Bypass** (Switch 11) on and off to see the raw source next to the faceted version.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | ~60% |
| Edge Width | ~50% |
| Contrast | ~50% |
| Brightness | ~50% |
| Color Reduce | ~25% |
| Randomize | ~12% |
| Hex Grid | Off |
| Outlines | On |
| Flat Shade | On |
| Mono | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Ghost Grid Overlay

![Ghost Grid Overlay result](/img/instruments/videomancer/facet/facet_ex2_s1.png)
*Ghost Grid Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A semi-transparent dark grid overlaid on live video, like looking through a wire mesh or a window screen.

#### Key Concepts

- Flat Shade off turns Facet into a grid overlay on the original image
- Mix creates semi-transparent blending between processed and dry signals
- Edge Width and Cell Size define the grid geometry independently

#### Video Source

A live camera feed or recorded footage with recognizable subjects and moderate contrast.

#### Steps

1. **Disable flat shading**: Set **Flat Shade** (Switch 9) to **Off**. The mosaic disappears, and the original video shows through.
2. **Enable outlines**: Confirm **Outlines** (Switch 8) is **On**. A grid of dark lines now overlays the source image.
3. **Adjust the grid**: Set **Cell Size** (Knob 1) to about 40% and **Edge Width** (Knob 2) to about 30%. You see a fine dark grid dividing the frame into small squares.
4. **Soften with Mix**: Slide the **Mix** fader (Fader 12) to roughly 60%. The grid becomes semi-transparent (a ghostly lattice floating over the source.)
5. **Explore extremes**: Push Edge Width to maximum while keeping Cell Size small. The outlines grow so thick that the grid becomes a dominant visual element, nearly occluding the image.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | ~40% |
| Edge Width | ~30% |
| Contrast | ~50% |
| Brightness | ~50% |
| Color Reduce | ~25% |
| Randomize | ~12% |
| Hex Grid | Off |
| Outlines | On |
| Flat Shade | Off |
| Mono | Off |
| Bypass | Off |
| Mix | ~60% |

---

### Exercise 3: Monochrome Crystal

![Monochrome Crystal result](/img/instruments/videomancer/facet/facet_ex3_s1.png)
*Monochrome Crystal — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An abstract monochrome pattern of large grayscale blocks separated by heavy black borders (a crystal lattice reduced to pure light and shadow.)

#### Key Concepts

- Mono strips color from the flat-shaded cells, leaving only grayscale facets
- Large cells with heavy outlines create bold abstract compositions
- The interaction between Mono and Flat Shade: Mono only works when Flat Shade is on

#### Video Source

High-contrast footage: stark shadows, bright highlights, strong silhouettes. Black-and-white film clips or backlit subjects work especially well.

#### Steps

1. **Large cells**: Turn **Cell Size** (Knob 1) to about 80%. The image becomes a very coarse mosaic of large flat blocks.
2. **Heavy borders**: Increase **Edge Width** (Knob 2) to roughly 70%. Thick black outlines dominate the grid.
3. **Enable monochrome**: Set **Mono** (Switch 10) to **On** while keeping **Flat Shade** (Switch 9) on. All color vanishes, leaving a grayscale crystal lattice.
4. **Full wet**: Confirm **Mix** (Fader 12) is at 100% so the effect is fully applied.
5. **Observe luminance structure**: Move your camera or change the source. Notice how the grayscale values in each cell track the average brightness of the underlying image region, even though all detail is gone.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | ~80% |
| Edge Width | ~70% |
| Contrast | ~50% |
| Brightness | ~50% |
| Color Reduce | ~25% |
| Randomize | ~12% |
| Hex Grid | Off |
| Outlines | On |
| Flat Shade | On |
| Mono | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Came**: The lead strips joining pieces of glass in a stained glass window; Facet's outlines serve the same visual role

- **Chroma**: The color information in a video signal, encoded as U and V components in YUV color space

- **Flat Shading**: A rendering technique where each polygon or cell receives a single uniform color with no smooth gradation

- **Interpolation**: Computing intermediate values between two known points; used by the Mix fader to blend processed and original signals

- **Leadwork**: The network of lead came strips in a stained glass window; in Facet, the black cell outlines

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness

- **Mosaic**: An image composed of small, uniformly colored tiles arranged in a grid

- **Proc Amp**: Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal

- **Tessellation**: Dividing a surface into shapes that fit together without gaps or overlaps

- **Voronoi Diagram**: A partition of a plane into regions based on distance to a set of seed points, producing an irregular, organic-looking tessellation

---
