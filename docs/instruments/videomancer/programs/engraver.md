---
draft: true
sidebar_position: 103
slug: /instruments/videomancer/engraver
title: "Engraver"
image: /img/instruments/videomancer/engraver/engraver_hero_s1.png
description: "In traditional engraving, a craftsman cuts lines into a metal plate."
---

![Engraver hero image](/img/instruments/videomancer/engraver/engraver_hero_s1.png)
*Engraver carving crisp contour lines from a posterized video source, reducing the image to flat tonal bands separated by sharp drawn edges like an etched copper plate.*

---

## Overview

**Engraver** combines two foundational image processing techniques: ***posterization*** and ***edge detection***: to produce effects that range from cartoon cel-shading to the dense linework of an etched copper plate. The posterization stage reduces all three video channels to a programmable number of discrete levels, collapsing smooth gradients into flat bands of color. The edge detection stage then compares each pixel to its immediate horizontal neighbor, drawing a contour line wherever pixel values cross a quantization boundary.

The interplay between these two stages is the heart of Engraver. Coarse quantization creates large flat regions with a few bold contour lines: the clean outlines of an animated cartoon. Fine quantization preserves more tonal steps and scatters edge lines across the frame, imitating the dense hatching of an engraved plate. Independent controls for edge brightness, edge color, fill style, and chroma removal let you shape the final image into anything from a monochrome pen-and-ink illustration to a vivid neon wireframe.

:::tip
Start with a low number of quantization levels and the contour lines will leap out immediately. Fewer levels produce fewer: but bolder: edge lines.
:::

### What's In a Name?

An ***engraver*** is a craftsperson who carves lines into a surface: traditionally a polished copper plate: to create an image defined entirely by incised marks. When the plate is inked and pressed to paper, the carved grooves hold pigment while the flat surface wipes clean, so the printed image is built from lines alone. Engraver applies the same principle to video: it finds the natural contour boundaries of the quantized image and draws them over a simplified fill, producing results that evoke copperplate engravings, woodcut illustrations, and cel-shaded animation.

---

## Quick Start

1. Feed a video source with clear shapes: a face, a hand, or geometric objects work well. Turn **Y Levels** (Knob 1) counter-clockwise to reduce the number of quantization levels. Watch as smooth gradients collapse into flat brightness bands. Fine contour lines appear at the boundaries between bands: these are the detected edges.
2. Increase **U Levels** (Knob 2) to brighten the contour lines. At low values the edges are dim or invisible; at high values they burn bright across the image.
3. Set **Desaturate** (Switch 9) to **On**. The fill regions vanish, leaving only the extracted contour lines on a black background (a pure line drawing carved from the video.)
4. Pull **Mix** (Fader 12) down from 100% to blend the line drawing back over the unprocessed source, creating an overlay effect where edges are inscribed onto the original footage.

---

## Parameters

![Videomancer front panel with Engraver loaded](/img/instruments/videomancer/engraver/engraver_control_panel.png)
*Videomancer's front panel with Engraver active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Y Levels

| Property | Value |
|----------|-------|
| Range | 2 – 32 |
| Default | 10 |

**Y Levels** controls the quantization depth applied to all three video channels simultaneously. Turning it counter-clockwise reduces the number of distinct tonal levels, collapsing smooth gradients into hard-edged bands of flat color. At the minimum setting, the image is crushed to just two stark levels. Turning it clockwise restores tonal steps; at the maximum, hundreds of discrete levels are available and the image closely tracks the original.

Because quantization depth directly determines where contour boundaries fall, this control also governs the density and placement of edge lines. Fewer levels mean fewer, bolder lines. More levels scatter finer lines across the frame.

---

### Knob 2 — U Levels

| Property | Value |
|----------|-------|
| Range | 2 – 32 |
| Default | 10 |

**U Levels** controls the luminance of detected edge pixels. At the minimum, edge lines are black and invisible against a dark fill. As the value increases, edge pixels grow progressively brighter, making the contour lines more visible and dominant. At the maximum, edge lines render at peak brightness.

This control has no effect on fill regions between edges (it adjusts only the brightness of edge pixels themselves.)

:::tip
Think of **U Levels** as the "ink darkness" on the engraved plate. Turn it up to make the carved lines stand out; turn it down for subtle, barely visible contours.
:::

---

### Knob 3 — V Levels

| Property | Value |
|----------|-------|
| Range | 2 – 32 |
| Default | 10 |

**V Levels** sets the luminance of the fill region when flat fill mode is active (see **Edge Invert**, Switch 8). At the minimum, the fill is black regardless of the input. At the maximum, the fill is a bright, uniform tone. When flat fill mode is disabled: the default: this control has no visible effect because the fill uses the quantized input values instead.

---

### Knob 4 — Edge Y

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Edge Y** sets the U (blue-difference) chrominance of the fill in flat fill mode. At the minimum, the fill's blue-difference component is at its lowest. Turning clockwise shifts the fill color along the blue-orange axis. This control only affects the output when flat fill mode is engaged via **Edge Invert** (Switch 8).

---

### Knob 5 — Edge U

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Edge U** sets the V (red-difference) chrominance of the fill in flat fill mode. At the default midpoint, the fill's red-difference component is neutral. Turning counter-clockwise shifts toward green; turning clockwise shifts toward magenta. Combined with **Edge Y** (Knob 4), these two knobs let you dial in any fill color when flat fill mode is active.

---

### Knob 6 — Edge V

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Edge V** tints the edge lines with color. At its midpoint, edge lines are neutral: pure grayscale with no chrominance. Turning the knob away from center adds a complementary-color tint: one direction pushes the hue toward warm tones, the other toward cool tones. The farther from center, the more saturated the edge color becomes.

:::tip
To create a colored wireframe on a black background, engage **Desaturate** (Switch 9) for edge-only mode, set **U Levels** (Knob 2) for edge brightness, and adjust **Edge V** (Knob 6) to tint the lines.
:::

---

### Switch 7 — Edge Mode

| Property | Value |
|----------|-------|
| Off | Fill+Edge |
| On | Edge Only |
| Default | Fill+Edge |

**Edge Mode** controls whether the input luminance is inverted before processing. In its default position (**Fill+Edge**), the luminance channel passes through normally. When set to **Edge Only**, the luminance is bitwise-inverted: bright becomes dark and dark becomes bright: before quantization and edge detection occur. Because edge positions depend on where quantized values change, inverting the luma shifts the contour lines to different locations in the image, producing an alternate version of the line drawing.

---

### Switch 8 — Edge Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Edge Invert** selects the fill style for non-edge regions. When **Off**, the fill uses the quantized version of the input video: you see flat posterized bands in the colors of the original source. When **On**, the fill switches to a uniform flat color determined by **V Levels** (Knob 3), **Edge Y** (Knob 4), and **Edge U** (Knob 5). This flat fill mode is useful for creating clean graphic looks where contour lines stand out against a solid-color background.

---

### Switch 9 — Desaturate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Desaturate** enables edge-only mode. When **Off**, both the fill regions and the edge lines are visible. When **On**, the fill regions are replaced with black and neutral chroma, and only the edge lines remain: a pure line drawing on a dark canvas. This mode isolates the contour lines entirely.

:::note
**Desaturate** overrides the fill mode selected by **Edge Invert** (Switch 8). When Desaturate is On, the fill is always black regardless of the fill mode setting.
:::

---

### Switch 10 — Link Levels

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Link Levels** removes all chrominance from the quantized fill, producing a grayscale posterized image. When **Off**, the quantized fill preserves the original color information. When **On**, the U and V channels are replaced with neutral gray, leaving only the brightness structure of the quantized image.

This control affects only the quantized fill mode (the default). In flat fill mode (**Edge Invert** On) or edge-only mode (**Desaturate** On), this control has no visible effect because those modes override the quantized fill.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input directly to the output, skipping all processing stages. The sync timing pipeline still runs, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original (dry) input and the processed (wet) output. At the minimum, the output is 100% dry: the original video passes through untouched. At the maximum, the output is 100% wet: the fully processed signal. Intermediate positions blend the two, which is useful for subtly overlaying contour lines onto the unprocessed source or softening the effect's intensity.

---

## Background

### Posterization and Quantization

When the continuous range of pixel values is forced into a smaller set of discrete steps, the result is called ***posterization***. Named after the flat, limited-color aesthetic of block-printed posters, this technique collapses smooth gradients into bands of uniform tone. Engraver's quantization stage works by masking the lower bits of each pixel value, rounding it down to the nearest power-of-two step. The number of surviving levels is always a power of two: 2, 4, 8, 16, 32, 64, 128, 256, or 512: depending on how many bits are discarded.

Posterization is applied identically to all three YUV channels. Luminance and both chrominance components are quantized by the same depth, creating a unified flat-shaded look where color transitions simplify alongside brightness transitions.

### Edge Detection by Adjacency

Engraver uses a simple, efficient form of ***edge detection***. Each quantized pixel is compared to the pixel that arrived one clock cycle earlier: its immediate horizontal neighbor. If any of the three quantized channels (Y, U, or V) differ between the two pixels, the current pixel is flagged as an edge. This method finds horizontal transitions only: wherever the image crosses a quantization boundary from left to right, a contour line is drawn.

Because edges are detected on the quantized signal rather than the original, the density of contour lines is directly tied to the quantization depth. Fewer quantization levels mean fewer boundaries to cross, producing bold, sparse outlines. Many quantization levels scatter thin lines across the image, creating a dense, hatched texture reminiscent of engraved illustrations.

### Composition Priority

Engraver composes its output pixel by pixel using a priority chain:

1. **Edge pixels** always take visual precedence. If a pixel is flagged as an edge, it receives a brightness set by the edge gain control and a chrominance tint set by the edge color control.
2. **Edge-only mode** is checked next. If active, non-edge pixels are replaced with black.
3. **Flat fill mode** is checked next. If active, non-edge pixels receive a uniform fill color.
4. **Quantized fill** is the default. Non-edge pixels retain their quantized channel values, with optional chrominance removal.

This priority chain means edge pixels always dominate, and edge-only mode always overrides the fill style.


---

## Signal Flow

### Signal Flow Notes

Two key facts about Engraver's processing order:

1. **Quantization feeds edge detection.** The edge detector operates on the quantized output, not the original input. Edge lines always fall exactly on quantization boundaries. Changing the quantization depth with **Y Levels** (Knob 1) moves and redraws the contour lines (they are not independent of the posterization.)

2. **Luma inversion is the first step.** When **Edge Mode** is set to **Edge Only**, the luminance channel is inverted before the quantizer sees it. This changes the values entering the quantizer, which shifts where quantization boundaries fall, which changes the positions of every contour line. All downstream stages: quantization, edge detection, and composition: see a different image.

:::tip
**Edge density = quantization depth.** The single most powerful control in Engraver is **Y Levels** (Knob 1). Sweeping it from low to high takes the output from bold cartoon outlines to fine engraved hatching.
:::


---

## Exercises

These exercises progress from a simple cartoon look to a detailed etching and finally to a colorized contour map. Each one builds on the previous, engaging more of Engraver's control surface.
### Exercise 1: Cartoon Cel-Shading

![Cartoon Cel-Shading result](/img/instruments/videomancer/engraver/engraver_ex1_s1.png)
*Cartoon Cel-Shading — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A cartoon cel-shaded version of live video with flat gray bands outlined by visible contour lines, resembling the bold outlines of a traditionally animated TV show.

#### Key Concepts

- Quantization creates flat tonal bands
- Edge detection draws contour lines at band boundaries
- Chroma kill creates a clean monochrome look

#### Video Source

A live camera feed or footage with recognizable subjects (faces, hands, or objects with clear silhouettes work best.)

#### Steps

1. Feed video into Videomancer and select the **Engraver** program.
2. Turn **Y Levels** (Knob 1) to about three-quarters clockwise. The image posterizes into several distinct brightness bands. Fine contour lines appear at the boundaries.
3. Raise **U Levels** (Knob 2) to roughly one-third. Edge lines become visible as dim contours overlaid on the posterized fill.
4. Turn on **Link Levels** (Switch 10). The image desaturates to grayscale, giving a clean inkwash look with contour lines separating each brightness band.
5. Experiment with **Y Levels** to taste: turning it lower reduces the band count and makes the contour lines bolder and fewer.

#### Settings

| Control | Value |
|---------|-------|
| Y Levels | ~25 |
| U Levels | ~10 |
| V Levels | ~8 |
| Edge Y | 0.0% |
| Edge U | 50.0% |
| Edge V | 50.0% |
| Edge Mode | Fill+Edge |
| Edge Invert | Off |
| Desaturate | Off |
| Link Levels | On |
| Bypass | Off |
| Mix | 100.0% |

---

### Exercise 2: Copper Plate Etching

![Copper Plate Etching result](/img/instruments/videomancer/engraver/engraver_ex2_s1.png)
*Copper Plate Etching — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dense network of contour lines on a dark background imitating the line-dense aesthetic of a traditional copperplate etching or engraving print.

#### Key Concepts

- Edge-only mode isolates contour lines on a black background
- Finer quantization creates denser linework
- Mixing dry signal with edge extraction creates overlay effects

#### Video Source

Footage with rich textures and tonal variation (fabric, foliage, architectural details, or skin.)

#### Steps

1. Turn **Y Levels** (Knob 1) fully clockwise for maximum quantization depth. Many fine contour lines emerge across the frame.
2. Set **U Levels** (Knob 2) to about three-quarters. The lines are bright and crisp.
3. Turn on **Desaturate** (Switch 9). The fill regions disappear, leaving only the edge lines on black (a pure line drawing.)
4. Adjust **Edge V** (Knob 6) slightly below center to tint the lines with a cool copper-like hue. Return to center for neutral white lines.
5. Pull **Mix** (Fader 12) down to about 70%. The original image bleeds through behind the line drawing, creating a ghostly overlay where the engraved lines are inscribed onto a faint version of the source.
6. Slowly reduce **Y Levels** and watch the linework go from dense hatching to bold contours.

#### Settings

| Control | Value |
|---------|-------|
| Y Levels | 32 |
| U Levels | ~23 |
| V Levels | ~13 |
| Edge Y | 50.0% |
| Edge U | 65.0% |
| Edge V | 30.0% |
| Edge Mode | Fill+Edge |
| Edge Invert | Off |
| Desaturate | On |
| Link Levels | On |
| Bypass | Off |
| Mix | 70.0% |

---

### Exercise 3: Neon Contour Map

![Neon Contour Map result](/img/instruments/videomancer/engraver/engraver_ex3_s1.png)
*Neon Contour Map — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A vivid, color-tinted contour map: bright colored edge lines drawn over a solid-color flat fill, with inverted luma for unexpected contour placement.

#### Key Concepts

- Flat fill mode creates a uniform background for contour lines
- Edge color tints the extracted lines with chrominance
- Luma inversion shifts the contour positions for an alternate line drawing

#### Video Source

Any footage with interesting shapes: dancers or athletes work well because their movement continuously redraws the contour map in real time.

#### Steps

1. Set **Y Levels** (Knob 1) to about half for moderate quantization (a balance between bold and fine linework.)
2. Set **U Levels** (Knob 2) to about three-quarters for bright, prominent edge lines.
3. Turn on **Edge Invert** (Switch 8) to activate flat fill mode. The regions between edges snap to a uniform color.
4. Set **V Levels** (Knob 3) to a low value for a dim background. Adjust **Edge Y** (Knob 4) and **Edge U** (Knob 5) to choose the fill color (try a deep blue or dark green.)
5. Rotate **Edge V** (Knob 6) well away from center to tint the contour lines. The farther from center, the more vivid the edge color.
6. Toggle **Edge Mode** (Switch 7) to **Edge Only**. The luma inverts and the contour lines jump to new positions in the image, revealing an alternate map.
7. Observe how movement redraws the neon contour map in real time.

#### Settings

| Control | Value |
|---------|-------|
| Y Levels | ~17 |
| U Levels | ~25 |
| V Levels | ~10 |
| Edge Y | 30.0% |
| Edge U | 70.0% |
| Edge V | 20.0% |
| Edge Mode | Edge Only |
| Edge Invert | On |
| Desaturate | Off |
| Link Levels | Off |
| Bypass | Off |
| Mix | 100.0% |

---
## Glossary

- **Chroma**: The color information in a video signal, encoded as U (blue-difference) and V (red-difference) components in YUV color space.

- **Contour Line**: A visible line drawn at the boundary where quantized pixel values change between two adjacent horizontal pixels.

- **Edge Detection**: The process of identifying boundaries where pixel values change sharply; Engraver uses horizontal pixel-pair comparison on the quantized signal.

- **Engraving**: A printmaking technique where lines are carved into a polished metal plate to hold ink, producing images built entirely from incised marks.

- **Flat Fill**: A uniform color substituted for the quantized input in non-edge regions, controlled by brightness and chroma fill parameters.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Posterization**: Reducing continuous tonal values to a limited set of discrete levels, creating flat areas of uniform color or brightness separated by hard transitions.

- **Quantization**: Mapping a continuous range of values to a smaller set of fixed steps by discarding lower-order bits; the resolution of the staircase determines edge density.

- **Wet/Dry Mix**: A crossfade between the processed output (wet) and the unprocessed input (dry), allowing partial blending of the effect.

---
