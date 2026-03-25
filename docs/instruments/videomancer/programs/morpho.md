---
draft: true
sidebar_position: 197
slug: /instruments/videomancer/morpho
title: "Morpho"
image: /img/instruments/videomancer/morpho/morpho_hero_s1.png
description: "Mathematical morphology is a branch of image processing based on set theory — it treats images as collections of shapes and applies operations that expand, shrink, or extract boundaries."
---

![Morpho hero image](/img/instruments/videomancer/morpho/morpho_hero_s1.png)
*Morpho applying morphological gradient extraction to a textured source, revealing luminous edge contours against a dark field.*

---

## Overview

**Morpho** is an edge sculptor. It applies ***morphological image processing***: a family of techniques that probe the shape and structure of an image by sliding a small sampling window across the video signal. The window finds the darkest or brightest pixel in the neighborhood and uses that value to erode, dilate, or outline the features in the frame. The result is a set of tools for thinning bright regions, expanding them, or extracting their edges as glowing outlines.

At gentle settings, Morpho can soften noise, clean up rough edges, or subtly sharpen contours. At extreme settings, it reduces the image to stark silhouettes, thick neon outlines, or high-contrast graphic shapes. The gradient mode is particularly striking: it computes the difference between the thickest and thinnest versions of the image, producing edge maps that look like hand-drawn ink outlines or luminous wireframes.

Because Morpho operates on a horizontal neighborhood of three pixels, it's fast and resource-light: no frame buffers, no memory, just a sliding window and some comparisons. This makes it responsive and artifact-free, perfect for real-time performance where clean edges and bold silhouettes are the goal.

### What's In a Name?

The name ***Morpho*** carries a dual meaning. The first is ***morphology***, the study of form and structure: the mathematical discipline from which these operations originate. The second is the ***Morpho butterfly***, a genus of iridescent blue butterflies whose wings reveal intricate structural patterns when viewed up close. Like the butterfly, Morpho reveals the hidden structure in a video signal: the edges, contours, and boundaries that define its shape.

---

## Quick Start

1. Set **Operation** (Switch 7) to **Erode** and **Channel** (Switch 8) to **All**. This activates gradient mode. You should see a mostly dark screen with bright outlines tracing the edges of your video source.
2. Turn **Edge Gain** (Knob 6) clockwise. The edge outlines grow brighter and more prominent, as if someone is tracing them with a neon marker.
3. Raise **Threshold** (Knob 3) slightly. The faintest, noisiest edges vanish, leaving only the strongest contours behind (a clean, bold edge map.)
4. Sweep **Mix** (Fader 12) from right to left. The processed edges blend back toward the original image, creating a sharpening effect where edges are enhanced but the source is still recognizable.

---

## Parameters

![Videomancer front panel with Morpho loaded](/img/instruments/videomancer/morpho/morpho_control_panel.png)
*Videomancer's front panel with Morpho active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Erode Amt

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Erode Amt** controls the intensity of the erosion effect. ***Erosion*** shrinks bright regions by replacing each pixel with the darkest value found in its immediate neighborhood. At low values, the erosion is subtle: fine details soften and thin bright lines begin to disappear. At high values, bright features are aggressively consumed by their darker surroundings, leaving only the largest, most dominant shapes.

---

### Knob 2 — Dilate Amt

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Dilate Amt** controls the intensity of the dilation effect. ***Dilation*** is the opposite of erosion: it expands bright regions by replacing each pixel with the brightest value in its neighborhood. At low values, the effect is gentle: small bright features grow slightly. At high values, bright areas spread outward, swallowing dark gaps and thin dark lines, producing bold, thickened shapes.

---

### Knob 3 — Threshold

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Threshold** clips dim pixels to black. At 0%, fully counterclockwise, every pixel passes through unchanged. As you increase the threshold, progressively brighter pixels are forced to black, carving away the dimmest parts of the image. This is especially powerful in gradient mode: raising the threshold eliminates faint, noisy edges while preserving strong contours, producing a clean edge map.

:::tip
In gradient mode, **Threshold** acts as an edge-strength filter. Low threshold values let every faint ripple through; high values isolate only the boldest structural boundaries.
:::

---

### Knob 4 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contrast** adjusts the tonal range of the processed signal. At the default midpoint, contrast is neutral. Turning counterclockwise compresses the tonal range, flattening the image toward mid-gray. Turning clockwise expands it, pushing darks darker and brights brighter for a punchier, more dramatic result.

---

### Knob 5 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** shifts the overall luminance of the processed signal. At the default midpoint, brightness is neutral. Turning counterclockwise darkens the image; turning clockwise brightens it. Combined with **Contrast**, this pair provides standard proc amp adjustment over the morphological output.

---

### Knob 6 — Edge Gain

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Edge Gain** amplifies the output of gradient mode. In gradient mode, the program computes the difference between the local maximum and local minimum: the ***morphological gradient***. Edge Gain multiplies that difference, boosting faint edges into visibility or driving strong edges into hard saturation. At the default midpoint, the gradient passes through at roughly unity gain. Turning clockwise pushes edges brighter; turning fully counterclockwise reduces the gradient toward silence.

:::note
Edge Gain only affects the output when gradient mode is active (Operation = **Erode**, Channel = **All**). In other modes, this knob has no visible effect.
:::

---

### Switch 7 — Operation

| Property | Value |
|----------|-------|
| Off | Erode |
| On | Open |
| Default | Erode |

**Operation** selects between two primary morphological behaviors. When set to **Erode**, the program applies erosion (or gradient, depending on the **Channel** switch). When set to **Open**, the program applies dilation (or an opening approximation). The effect of this switch changes depending on the Channel setting (see the Toggle Group Notes below.)

---

### Switch 8 — Channel

| Property | Value |
|----------|-------|
| Off | Luma |
| On | All |
| Default | Luma |

**Channel** selects whether morphological processing applies to the luma channel only or to all three channels (Y, U, and V). When set to **Luma**, the brightness channel is processed while color information passes through unaltered. When set to **All**, color channels are also processed: and the Operation switch changes its behavior, unlocking gradient and open modes.

:::tip
Start with **Luma** mode. Processing only brightness preserves the original color palette while sculpting edges and silhouettes. Switch to **All** when you want the full morphological treatment: gradient edge maps with neutral color, or all-channel erosion and dilation.
:::

---

### Switch 9 — Struct Elm

| Property | Value |
|----------|-------|
| Off | Cross |
| On | Square |
| Default | Cross |

**Struct Elm** (Structuring Element) selects the shape of the sampling neighborhood used for morphological operations. When set to **Cross**, the window samples in a cross-shaped pattern. When set to **Square**, the window uses a full square neighborhood. The cross pattern emphasizes horizontal and vertical edges; the square pattern treats all directions equally.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** flips the brightness of the input signal before any morphological processing takes place. Because inversion happens at the very first stage, it reverses the behavior of erosion and dilation: what was erode becomes a dilation-like effect (since dark regions become bright and vice versa), and gradient edges shift to different contours. This is a powerful creative tool for exploring the complementary structure of an image.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all morphological processing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw source and the processed result.

---

:::note Toggle Group Notes

**Operation** (Switch 7) and **Channel** (Switch 8) combine to select one of four processing modes. The two toggles form a binary selector that fundamentally changes how Morpho processes the video signal:

| Operation | Channel | Mode | Description |
|-----------|---------|------|-------------|
| Erode | Luma | Erode | Local minimum on Y only; color preserved |
| Open | Luma | Dilate | Local maximum on Y only; color preserved |
| Erode | All | Gradient | Edge map (max − min) on Y; color set to neutral |
| Open | All | Open | Erosion on all channels (opening approximation) |

In **Luma** modes, only the brightness channel is affected; U and V pass through untouched. In **All** modes, all three channels are processed. Gradient mode is special: it computes the morphological gradient on the luma channel and forces color to neutral gray, producing a monochrome edge map amplified by **Edge Gain**.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (original) signal and the wet (processed) signal. At 100%, fully right, the output is entirely morphological. At 0%, fully left, the output is the original video. Intermediate positions blend the two, which is particularly useful for subtle edge enhancement: a small amount of gradient mixed into the original signal acts as an unsharp mask, gently sharpening contours without replacing the image.

:::tip
***Mix is your sharpening dial.*** In gradient mode, blending a small amount of the edge map back into the original signal produces a sharpening effect similar to an ***unsharp mask*** (a classic technique from darkroom photography.)
:::

---

## Background

### Mathematical Morphology

The word ***morphology*** means "the study of form." In image processing, ***mathematical morphology*** is a set of operations that probe an image with a small shape called a ***structuring element***: a tiny template slid across every pixel. At each position, the structuring element examines the pixel's neighbors and produces a single output value based on the neighborhood. The two fundamental operations are ***erosion*** (take the minimum) and ***dilation*** (take the maximum).

Erosion shrinks bright regions and widens dark ones. If you imagine white shapes on a black background, erosion eats away at their edges. Dilation does the opposite: bright regions grow, swallowing narrow dark gaps. These two operations are the building blocks of more complex morphological filters.

### Compound Operations

By combining erosion and dilation in sequence, we get two compound operations:

- ***Opening*** (erode, then dilate) removes small bright noise while preserving the overall shape of larger features. It smooths the contours of bright objects without changing their size.
- ***Closing*** (dilate, then erode) removes small dark gaps and holes while preserving bright shapes.

The ***morphological gradient*** is the difference between dilation and erosion: `dilate(image) − erode(image)`. This produces thick outlines at every boundary: wherever pixel values change rapidly across the structuring element. It's a nonlinear edge detector that responds to the *magnitude* of transitions regardless of direction.

### Structuring Elements

The structuring element defines the shape and reach of the neighborhood. A ***cross*** element samples only the pixels directly above, below, left, and right of the center. A ***square*** element samples all eight surrounding pixels plus the center. The cross is sensitive to horizontal and vertical edges; the square is more isotropic, responding equally to diagonal boundaries.

Morpho uses a 3-pixel horizontal window: a one-dimensional structuring element. This means it detects horizontal transitions in the signal. Vertical structure is preserved but not directly probed. The advantage is speed and simplicity: no line buffers or frame memory are required, keeping the design compact and the latency low.


---

## Signal Flow

### Signal Flow Notes

Morpho's pipeline is short and direct: two clocks for the morphological computation, then four clocks through the interpolator for wet/dry mixing (six clocks total.)

The critical interaction is between the **Operation** and **Channel** toggles. These two switches form a 2-bit selector that chooses among four distinct algorithms. Gradient mode is the most complex: it computes both the local minimum and maximum, subtracts them, multiplies the result by **Edge Gain**, and forces the color channels to neutral gray. This produces a monochrome edge map where brightness represents edge strength.

:::note
Morpho's structuring element is a 3-pixel horizontal line: a 1D neighborhood. This means edges are detected along the horizontal axis. Vertical edges perpendicular to the scan direction are detected strongly; purely horizontal edges (parallel to the scan) may be less pronounced. For full 2D morphology, consider chaining Morpho with a program that operates in the vertical dimension.
:::


---

## Exercises

These exercises progress from basic erosion to gradient edge extraction and creative blending. Each one builds on the previous, gradually engaging more of the processing modes.
### Exercise 1: Erosion and Dilation

![Erosion and Dilation result](/img/instruments/videomancer/morpho/morpho_ex1_s1.png)
*Erosion and Dilation — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Explore how erosion and dilation reshape the bright and dark features of a video signal.

#### Key Concepts

- Erosion shrinks bright regions by selecting the local minimum
- Dilation expands bright regions by selecting the local maximum
- The two operations are complementary inverses

#### Video Source

A live camera feed or recorded footage with clear bright-on-dark subjects: white text on a black background, a face lit against darkness, or high-contrast graphic shapes.

#### Steps

1. **Erode**: With **Operation** set to **Erode** and **Channel** set to **Luma**, the video signal is already being eroded. Bright features appear slightly thinner, and fine white details begin to vanish.
2. **Dilate**: Flip **Operation** to **Open** (with Channel still on Luma). Bright features expand outward. Thin dark gaps between bright objects fill in. White text becomes bolder.
3. **Invert and compare**: Toggle **Invert** (Switch 10). The brightness inverts before morphological processing, so erosion now shrinks what *was* dark (now bright), producing a different silhouette.
4. **All-channel processing**: Set **Channel** to **All** and **Operation** to **Open**. Now erosion applies to color as well as brightness. Saturated regions shrink; neutral zones encroach.

#### Settings

| Control | Value |
|---------|-------|
| Erode Amt | 50% |
| Dilate Amt | 50% |
| Threshold | 0% |
| Contrast | 50% |
| Brightness | 50% |
| Edge Gain | 50% |
| Operation | Erode |
| Channel | Luma |
| Struct Elm | Cross |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Gradient Edge Map

![Gradient Edge Map result](/img/instruments/videomancer/morpho/morpho_ex2_s1.png)
*Gradient Edge Map — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Extract a clean, luminous edge map from a video source (bright outlines on a dark field, like a neon wireframe.)

#### Key Concepts

- The morphological gradient is the difference between dilation and erosion
- Edge Gain amplifies faint edges into visibility
- Threshold filters out noise, isolating strong contours

#### Video Source

Footage with strong structural features: architecture, mechanical objects, or a face with clear contours. Moderate contrast works best: extremely flat or extremely busy sources produce less interesting gradients.

#### Steps

1. **Activate gradient mode**: Set **Operation** to **Erode** and **Channel** to **All**. The screen goes mostly dark with faint bright lines at every edge.
2. **Boost edges**: Turn **Edge Gain** (Knob 6) clockwise past the midpoint. The edge outlines brighten dramatically, like luminous tracings of the source geometry.
3. **Clean up noise**: Raise **Threshold** (Knob 3) slowly. The faintest edges: noise, texture, subtle gradients: disappear, leaving only the strongest structural boundaries.
4. **Blend with source**: Pull **Mix** (Fader 12) to about 70%. The edge map blends with the original image, creating an edge-sharpened version of the source where contours glow while the image remains recognizable.

#### Settings

| Control | Value |
|---------|-------|
| Erode Amt | 50% |
| Dilate Amt | 50% |
| Threshold | 30% |
| Contrast | 50% |
| Brightness | 50% |
| Edge Gain | 80% |
| Operation | Erode |
| Channel | All |
| Struct Elm | Cross |
| Invert | Off |
| Bypass | Off |
| Mix | 70% |

---

### Exercise 3: Silhouette Sculpting

![Silhouette Sculpting result](/img/instruments/videomancer/morpho/morpho_ex3_s1.png)
*Silhouette Sculpting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Combine erosion, inversion, and thresholding to sculpt silhouettes and high-contrast graphic shapes from a video source.

#### Key Concepts

- Inversion before morphology reverses which features are eroded or dilated
- Threshold carves the processed output into stark shapes
- Mix allows subtle blending for composite effects

#### Video Source

High-contrast footage: a performer against a bright background, projected graphics, or any source with clear foreground/background separation.

#### Steps

1. **Strong erosion**: Set **Operation** to **Erode**, **Channel** to **Luma**, and push **Erode Amt** (Knob 1) high. Bright features thin dramatically, leaving skeletal remnants.
2. **Invert**: Enable **Invert** (Switch 10). The brightness flips before erosion, so now *dark* features are being eroded. The silhouette restructures: what was foreground becomes background, and new shapes emerge.
3. **Threshold sculpt**: Raise **Threshold** (Knob 3) to carve the eroded image into stark black-and-white shapes. The threshold cuts cleanly through the eroded tonal range.
4. **Blend back**: Pull **Mix** (Fader 12) to about 40%. The silhouette blends into the original image, creating a ghostly overlay where hard-edged shapes float over recognizable content.
5. **Explore openings**: Flip **Operation** to **Open** and **Channel** to **All**. The combined erosion-on-all-channels produces a different silhouette character (softer, more rounded.)

#### Settings

| Control | Value |
|---------|-------|
| Erode Amt | 80% |
| Dilate Amt | 50% |
| Threshold | 40% |
| Contrast | 50% |
| Brightness | 50% |
| Edge Gain | 50% |
| Operation | Erode |
| Channel | Luma |
| Struct Elm | Cross |
| Invert | On |
| Bypass | Off |
| Mix | 40% |

---
## Glossary

- **Dilation**: A morphological operation that replaces each pixel with the maximum value in its neighborhood, expanding bright regions and filling dark gaps

- **Erosion**: A morphological operation that replaces each pixel with the minimum value in its neighborhood, shrinking bright regions and widening dark areas

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color

- **Morphological Gradient**: The difference between dilation and erosion at each pixel, producing an edge map where brightness indicates edge strength

- **Morphology**: In image processing, a family of operations that probe the shape and structure of an image using a small neighborhood template

- **Opening**: A compound morphological operation consisting of erosion followed by dilation, used to remove small bright noise while preserving larger shapes

- **Proc Amp**: Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal

- **Structuring Element**: The shape defining which neighboring pixels are examined during a morphological operation (cross, square, line, etc.)

- **Threshold**: A brightness cutoff below which pixel values are forced to black, used to clean up or isolate features

- **Unsharp Mask**: A sharpening technique that enhances edges by subtracting a blurred version of the image from the original, or by blending an edge map back into the source

---
