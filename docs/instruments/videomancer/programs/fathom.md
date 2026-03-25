---
draft: true
sidebar_position: 106
slug: /instruments/videomancer/fathom
title: "Fathom"
image: /img/instruments/videomancer/fathom/fathom_hero_s1.png
description: "Every topographic map you have ever seen uses the same trick: draw lines where the ground crosses a constant altitude, then fill the zones between those lines with colours that suggest the terrain — green lowlands, brown mountains, white glacial peaks."
---

![Fathom hero image](/img/instruments/videomancer/fathom/fathom_hero_s1.png)
*Fathom rendering contour isolines and hypsometric zone tinting over a video source, transforming luminance into a living terrain map.*

---

## Overview

Fathom is a contour-line renderer that treats the brightness of your video signal as elevation on a topographic map. Wherever the luminance crosses a fixed threshold between two adjacent pixels, Fathom draws a contour line: just like the isolines on a hiking map that trace paths of equal altitude. Between those lines, each elevation band receives its own color from a ***hypsometric*** palette, filling the screen with the greens, browns, and whites of a terrain survey or the blues and whites of an ocean depth chart.

The effect runs in real time: as your video source moves, the contour lines shift and flow like a landscape in motion. Bright areas become mountain peaks crowned with tightly packed lines. Dark areas become valleys or ocean trenches with wide, sweeping contours. Mid-tones become rolling plains where the lines spread gently apart. With a few knob turns you can go from a subtle cartographic overlay to a vivid, poster-like terrain map that completely replaces your source imagery.

:::tip
Fathom is not an edge detector. Edge detection highlights *gradient magnitude*: where brightness changes fast. Fathom draws ***isolines*** at fixed brightness intervals, producing closed, concentric rings that respond to the *absolute level* of the signal. A smooth gradient becomes a series of parallel lines like a hillside, while a hard edge becomes tightly packed lines like a cliff face.
:::

### What's In a Name?

A ***fathom*** is a unit of depth measurement equal to six feet, used in nautical charting to mark the distance from the ocean surface to the seafloor. Bathymetric charts: maps of underwater terrain: are drawn in fathom increments, producing concentric contour lines that reveal ridges, trenches, and plateaus hidden beneath the waves. The name captures Fathom's core idea: plumbing the depths (and heights) of your video signal and drawing a map of what it finds.

---

## Quick Start

1. Feed a video source with a range of brightness values: a face, a landscape, or a gradient test pattern all work well. You should see contour lines and colored bands immediately.
2. Turn **Contour Int** (Knob 1) slowly through its eight steps. Notice how the spacing between contour lines changes: fewer steps means wider bands, more steps means tighter lines packed closer together.
3. Turn **Zone Opac** (Knob 4) counterclockwise to reduce the hypsometric fill. The colored bands fade and the original video shows through between the contour lines.
4. Flip **Palette A** (Switch 7) to **Bathy**. The terrain greens and browns are replaced with oceanic blues, turning your map from a mountain survey into a seafloor chart.

---

## Parameters

![Videomancer front panel with Fathom loaded](/img/instruments/videomancer/fathom/fathom_control_panel.png)
*Videomancer's front panel with Fathom active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Contour Int

| Property | Value |
|----------|-------|
| Range | 16 – 256 |
| Default | 106 |

**Contour Int** sets the spacing between contour lines, expressed as a step selector with eight discrete values. At the lowest setting (step 1), contour lines are drawn every 16 luminance levels: extremely tight, producing many closely packed isolines even across subtle brightness gradients. At the highest setting (step 8), lines are drawn every 256 luminance levels: very wide spacing that produces only a handful of broad elevation bands across the full brightness range.

Wider intervals create a bolder, more graphic look with large, flat-colored zones. Tighter intervals produce dense, detailed maps that reveal the fine structure of brightness variation in your source. Because the 10-bit luminance range spans 0 to 1023, the tightest setting of 16 can produce up to 15 visible contour levels, while the widest setting of 256 produces only 3 or 4.

:::note
The eight interval steps are: 16, 32, 48, 64, 96, 128, 192, and 256 luminance levels. These are not evenly spaced: the steps grow larger toward the high end, giving you finer control over tight contour spacings and coarser control over wide spacings.
:::

---

### Knob 2 — Line Weight

| Property | Value |
|----------|-------|
| Range | 1px – 4px |
| Default | 2px |

**Line Weight** controls the thickness of the contour lines in four discrete steps: 1, 2, 3, or 4 pixels wide. At the minimum setting, contour lines are drawn as single-pixel hairlines, producing a delicate, engraved appearance. At the maximum, lines are drawn four pixels wide, creating bold, prominent contours that dominate the image.

Heavier line weights are achieved by extending the horizontal crossing detection to include a second pixel neighbor. This means the thickening is most visible in the horizontal direction.

---

### Knob 3 — Contour Clr

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 45° |

**Contour Clr** selects the color of the contour lines from a palette of eight hues, swept across 360 degrees. The available colors cycle through brown, black, white, blue, red, green, yellow, and purple. The default position produces a cartographic brown: the traditional color for contour lines on topographic maps.

:::tip
Black contour lines on a monochrome palette (Switch 8 set to **Mono**) produce a clean, technical look reminiscent of architectural elevation drawings. Switch to white lines for a chalk-on-blackboard effect.
:::

---

### Knob 4 — Zone Opac

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Zone Opac** controls how strongly the hypsometric zone colors are applied. At 100%, the zone palette completely replaces the original video between contour lines: you see only the map colors. At 0%, the zone colors vanish entirely and the original video shows through between contour lines, with only the lines themselves drawn on top.

At intermediate values, the zone colors blend with the original video, creating a translucent overlay effect: as if a tinted map has been layered over a window into the real scene. This parameter has no effect on contour lines themselves; they are always drawn at full intensity.

:::note
When **Fill Mode** (Switch 10) is set to **VideoFill**, this parameter has no effect because the fill is already the original video.
:::

---

### Knob 5 — Elev Offset

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Elev Offset** shifts the entire elevation scale by adding a constant value to every pixel's luminance before contour detection. At 0%, no offset is applied and the darkest parts of your video correspond to the lowest elevation zones. As you increase the offset, the contour map slides upward through the brightness range: areas that were previously in the middle zones shift toward the peaks, and new low-elevation zones appear from below.

This is analogous to adjusting "sea level" on a terrain map. Increasing the offset is like flooding the valleys: contour lines that were far apart in the lowlands compress as rising "water" pushes them up the slopes.

---

### Knob 6 — Zone Sat

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Zone Sat** controls the color saturation of the hypsometric zone fill. At 100%, zone colors are vivid and poster-like: deep greens, warm browns, bright whites. At 0%, the chroma channels are zeroed out and the zone fill becomes a pure grayscale elevation map. Intermediate values produce a subtle, desaturated wash of color that tints the elevation bands without overwhelming the image.

This parameter applies to both the terrain and bathymetric palettes. It scales the Cb and Cr components around neutral (512), so the overall brightness of the zones is unaffected.

---

### Switch 7 — Palette A

| Property | Value |
|----------|-------|
| Off | Terrain |
| On | Bathy |
| Default | Terrain |

**Palette A** selects between two hypsometric color palettes. In the **Terrain** position, zones progress from dark green lowlands through yellow-green foothills, tan and brown mountains, gray alpine rock, to white snow-capped peaks: the classic topographic map color scheme. In the **Bathy** position, the palette inverts to an oceanic scheme: deep blue abyssal zones at the bottom, lighter blues for shallows, and white near the surface.

---

### Switch 8 — Palette B

| Property | Value |
|----------|-------|
| Off | Tinted |
| On | Mono |
| Default | Tinted |

**Palette B** switches the zone fill between **Tinted** and **Mono** modes. In Tinted mode, the full hypsometric palette is used with all its colors. In Mono mode, the Cb and Cr channels of the zone palette are forced to neutral (512), producing a grayscale elevation map where zones differ only in brightness. Contour line color (set by **Contour Clr**, Knob 3) is unaffected by this switch.

---

### Switch 9 — Major/Minor

| Property | Value |
|----------|-------|
| Off | Equal |
| On | Styled |
| Default | Equal |

**Major/Minor** controls whether contour lines are drawn with visual hierarchy. In the **Equal** position, every contour line has the same appearance regardless of its elevation level. In the **Styled** position, every fifth contour level is treated as a ***major contour*** (also called an ***index contour*** on topographic maps) and drawn at the full contour color intensity, while intermediate lines remain at the same weight. On real topographic maps, major contours are printed bolder so that a reader can quickly count elevation intervals; Fathom recreates this convention.

:::note
Major contours occur at levels 5, 10, and 15 (out of a maximum of 15 contour levels). With wide contour intervals, you may see only one or two major contours on screen.
:::

---

### Switch 10 — Fill Mode

| Property | Value |
|----------|-------|
| Off | HypsoFill |
| On | VideoFill |
| Default | HypsoFill |

**Fill Mode** selects what appears between contour lines. In the **HypsoFill** position, the spaces between contours are filled with hypsometric zone colors drawn from the currently selected palette. In the **VideoFill** position, the original input video passes through unaltered between the contour lines, and only the lines themselves are drawn on top. VideoFill mode turns Fathom into a contour-line overlay, useful for adding cartographic lines to footage without replacing its color.

:::tip
Combine **VideoFill** with a bold **Line Weight** (Knob 2) and a contrasting **Contour Clr** (Knob 3) for a wire-frame overlay effect that traces the brightness terrain of your video without hiding it.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the input signal directly to the output, skipping all Fathom processing. The sync delay pipeline still runs, so switching Bypass on and off produces no glitch or timing disruption. Use Bypass for instant A/B comparison between the raw input and the contour-mapped result.

---

:::note Toggle Group Notes

Toggles 7 and 8 form a combined palette selector with four possible combinations:

| Palette A | Palette B | Result |
|-----------|-----------|--------|
| Terrain | Tinted | Classic topographic map — green valleys to white peaks |
| Terrain | Mono | Grayscale elevation — brightness-only terrain shading |
| Bathy | Tinted | Oceanic depth chart — deep blue abyss to white shallows |
| Bathy | Mono | Grayscale depth chart — inverted brightness for ocean floor |

Toggles 9, 10, and 11 operate independently of the palette selector and of each other.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (unprocessed) input and the wet (contour-mapped) output. At 0%, the output is entirely dry: identical to the original video. At 100%, the output is entirely wet: the full Fathom effect. Intermediate values blend the two, which can produce a ghostly overlay of contour lines and zone colors on top of the original footage.

The crossfade is performed by three `interpolator_u` instances (one each for Y, Cb, and Cr), providing smooth, artifact-free blending across the full range of the fader.

---

## Background

### Topographic contour mapping

A ***contour line*** (also called an ***isoline***) connects all points on a surface that share the same elevation. On a topographic map, contour lines are drawn at fixed vertical intervals: every 20 meters, every 100 feet, or every fathom. Where the terrain is steep, the lines bunch together; where it is gentle, they spread apart. A trained reader can "see" the three-dimensional shape of a landscape just by studying the spacing and curvature of these lines.

Fathom applies the same principle to video. Instead of geographic elevation, the "height" is the brightness of each pixel. Instead of a static survey, the terrain evolves in real time as the video plays. The result is a continuously morphing map that reveals the tonal structure of your source in a way that is both analytically precise and visually striking.

### Hypsometric tinting

***Hypsometric tinting*** is the cartographic practice of coloring elevation zones with a graduated palette. The most common convention uses greens for low elevations, yellows and browns for mountains, and white for snow-capped peaks. Bathymetric charts use the inverse: white or light blue for shallow water, darkening to deep blue or black for ocean trenches. Swiss cartographer Eduard Imhof codified many of these conventions in the mid-twentieth century, and his palettes remain the gold standard for shaded relief maps.

Fathom's terrain palette follows this tradition: eight zones stepping from dark green through tan farmers' fields, brown rocky slopes, gray alpine scree, to brilliant white summits. The bathymetric palette reverses the brightness ramp, placing the lightest tones at the high end (sea surface) and the deepest blues at the low end (ocean floor).

### Contour detection algorithm

Unlike traditional edge detection (which measures the *rate of change* of brightness), contour detection tests whether a fixed brightness threshold falls *between* two adjacent pixels. If the current pixel's luminance is above the threshold and its neighbor's luminance is below it (or vice versa), the threshold "crosses" between them and a contour line is drawn at the current pixel.

Fathom tests up to 15 thresholds simultaneously, spaced at the interval set by **Contour Int**. For each threshold, both horizontal (left neighbor) and vertical (above neighbor, via a one-line BRAM delay) crossings are checked. This produces closed, concentric contour rings that faithfully trace the luminance terrain of the video source.


---

## Signal Flow

### Signal Flow Notes

The pipeline is eight clocks deep: four processing stages followed by the four-clock interpolator. A parallel delay pipeline shifts the original video data through the same eight clocks so that it arrives at the mix stage time-aligned with the processed result.

The key interaction is between **Elevation Offset** (Pot 5) and **Contour Int** (Pot 1). The offset shifts the input luma upward before contour detection, which changes *where* the threshold crossings land. Increasing the offset causes contour lines to migrate downward through the image: as if raising the water level floods the valleys and pushes contour lines up the slopes. The contour interval then controls how many thresholds are tested across whatever luminance range remains.

The line buffer stores one complete scanline of offset-adjusted luma in a single BRAM tile, enabling vertical contour detection alongside horizontal. Both horizontal and vertical crossings feed into a single `on_contour` flag, so a contour pixel detected in either direction is drawn identically.


---

## Exercises

Three exercises explore Fathom's contour mapping from simple cartographic overlays to vivid hypsometric landscapes and custom-styled depth charts.
### Exercise 1: Terrain Survey

![Terrain Survey result](/img/instruments/videomancer/fathom/fathom_ex1_s1.png)
*Terrain Survey — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic topographic map visualization with green valleys, brown mountains, and white peaks.

#### Key Concepts

- Contour lines appear wherever brightness crosses a threshold between adjacent pixels
- Hypsometric tinting colors each elevation band according to a terrain palette
- Contour interval controls the density of isolines

#### Video Source

A video source with a wide range of brightness values: a well-lit face, a landscape, or a luma ramp. Footage with both gradual gradients and sharp transitions works best.

#### Steps

1. **Default terrain**: With default settings, observe the contour lines and color bands on your source. The terrain palette should be visible with green lowlands and bright peaks.
2. **Tighten contours**: Turn **Contour Int** (Knob 1) counterclockwise to a low step. The contour lines become tightly packed, revealing fine structure in the brightness gradients like a detailed survey map.
3. **Bold lines**: Increase **Line Weight** (Knob 2) to 3 or 4 pixels. The contour lines become prominent, standing out clearly against the colored zones.
4. **Index contours**: Flip **Major/Minor** (Switch 9) to **Styled**. Every fifth contour level now has a bolder appearance, creating the visual hierarchy of a real topographic map.
5. **Elevation shift**: Slowly turn **Elev Offset** (Knob 5) clockwise. Watch the contour lines migrate across the image as "sea level" rises.
6. **Desaturate**: Lower **Zone Sat** (Knob 6) to produce a subtle, pastel-washed terrain map.

#### Settings

| Control | Value |
|---------|-------|
| Contour Int | Step 2 (32) |
| Line Weight | 3 px |
| Contour Clr | 45° (brown) |
| Zone Opac | 75% |
| Elev Offset | 0% |
| Zone Sat | 50% |
| Palette A | Terrain |
| Palette B | Tinted |
| Major/Minor | Styled |
| Fill Mode | HypsoFill |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Contour Overlay on Video

![Contour Overlay on Video result](/img/instruments/videomancer/fathom/fathom_ex2_s1.png)
*Contour Overlay on Video — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A wire-frame contour overlay drawn on top of live video, without replacing the video's color.

#### Key Concepts

- VideoFill mode preserves the original video between contour lines
- Contour color and weight can be tuned for maximum visibility against the source
- Mix can blend the contour overlay with the dry signal for subtle effects

#### Video Source

Any video footage: this exercise works especially well with moving content, revealing how contour lines flow in real time over the live image.

#### Steps

1. **Switch to VideoFill**: Flip **Fill Mode** (Switch 10) to **VideoFill**. The colored zones vanish and the original video appears between the contour lines.
2. **Contrast lines**: Set **Contour Clr** (Knob 3) to white (approximately 90°). Turn **Line Weight** (Knob 2) up to 2 or 3 pixels so the lines stand out against the video.
3. **Adjust interval**: Turn **Contour Int** (Knob 1) to a medium step (step 4 or 5). Too many lines clutter the image; too few make the overlay sparse.
4. **Subtle blend**: Lower **Mix** (Fader 12) to about 70%. The contour lines become semi-transparent, ghosting over the source.
5. **Elevation animation**: Sweep **Elev Offset** (Knob 5) slowly back and forth. The contour lines ripple across the image like elevation bands being raised and lowered.
6. **Enable major contours**: Flip **Major/Minor** (Switch 9) to **Styled** for periodic bold lines over the finer mesh.

#### Settings

| Control | Value |
|---------|-------|
| Contour Int | Step 4 (64) |
| Line Weight | 2 px |
| Contour Clr | 90° (white) |
| Zone Opac | 75% |
| Elev Offset | 0% |
| Zone Sat | 75% |
| Palette A | Terrain |
| Palette B | Tinted |
| Major/Minor | Styled |
| Fill Mode | VideoFill |
| Bypass | Off |
| Mix | 70% |

---

### Exercise 3: Deep Sea Chart

![Deep Sea Chart result](/img/instruments/videomancer/fathom/fathom_ex3_s1.png)
*Deep Sea Chart — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An oceanic depth chart with deep blue trenches, lighter blue shallows, and white surface zones.

#### Key Concepts

- The bathymetric palette reverses the brightness-to-color mapping for an oceanic aesthetic
- Monochrome mode strips color from the zone fill for a technical look
- Zone opacity and saturation together control the visual weight of the fill

#### Video Source

High-contrast footage, ideally with large dark regions that will become "deep water." Abstract camera footage, silhouettes, or dark theatrical lighting work well.

#### Steps

1. **Select bathymetric palette**: Flip **Palette A** (Switch 7) to **Bathy**. The zone colors shift to oceanic blues.
2. **Vivid saturation**: Turn **Zone Sat** (Knob 6) fully clockwise for maximum color intensity. The blues should be rich and deep.
3. **Full zone opacity**: Set **Zone Opac** (Knob 4) fully clockwise so the palette completely replaces the video.
4. **Black contour lines**: Turn **Contour Clr** (Knob 3) to approximately 45° (black). The contour lines become dark depth markings against the blue zones.
5. **Wide intervals**: Set **Contour Int** (Knob 1) to step 5 or 6 (96 or 128). Wide spacing produces the appearance of a large-scale bathymetric chart with broad depth bands.
6. **Explore monochrome**: Flip **Palette B** (Switch 8) to **Mono**. The blues vanish, leaving a grayscale depth chart where elevation bands differ only in brightness (a more technical, scientific look.)
7. **Hairline weight**: Set **Line Weight** (Knob 2) to 1 px for fine, precise depth contours.

#### Settings

| Control | Value |
|---------|-------|
| Contour Int | Step 5 (96) |
| Line Weight | 1 px |
| Contour Clr | 45° (black) |
| Zone Opac | 100% |
| Elev Offset | 0% |
| Zone Sat | 100% |
| Palette A | Bathy |
| Palette B | Tinted |
| Major/Minor | Equal |
| Fill Mode | HypsoFill |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Bathymetric**: Relating to the measurement and mapping of underwater depth; a bathymetric chart shows ocean floor terrain using color-coded depth bands.

- **Contour Line**: A line on a map connecting points of equal value (elevation, depth, temperature); also called an isoline or isopleth.

- **Hypsometric Tinting**: The cartographic technique of coloring elevation zones with a graduated palette, typically greens for lowlands, browns for mountains, and white for peaks.

- **Index Contour**: A heavier or bolder contour line drawn at regular intervals (typically every fifth line) to make elevation counting easier; also called a major contour.

- **Interpolator**: A hardware module that smoothly blends between two values using a fractional coefficient; used here for the wet/dry mix crossfade.

- **Isoline**: A contour line connecting points of equal value; from the Greek *iso-* meaning "equal."

- **Line Buffer**: A single-scanline memory (BRAM) that stores one row of pixel data, enabling comparison between the current pixel and the pixel directly above it.

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Threshold Crossing**: The condition where a fixed value falls between two adjacent pixel luminances, indicating that a contour line passes between them.

---
