---
draft: true
sidebar_position: 117
slug: /instruments/videomancer/floorplan
title: "Floorplan"
image: /img/instruments/videomancer/floorplan/floorplan_hero.png
description: "Every video image is full of boundaries — places where brightness changes abruptly across adjacent pixels."
---

![Floorplan hero image](/img/instruments/videomancer/floorplan/floorplan_hero_s1.png)
*Floorplan rendering edge-detected wall lines from a video source as dark architectural outlines on bright paper with a blueprint grid overlay.*

---

## Overview

Floorplan transforms live video into an architectural drawing. It scans the incoming picture for edges: places where brightness changes sharply from one pixel to the next: and redraws them as dark wall lines on a bright, uniform background. The result looks like you unrolled a set of building blueprints across the screen: clean outlines trace the shapes in your source, while the spaces between fill with white paper or tinted blue. An optional dimension grid lays faint ruled lines across the entire frame, completing the technical-drawing illusion.

At gentle settings, Floorplan adds a subtle drafting-paper quality to your video, softening detail while preserving strong contours. Push the sensitivity higher and lower the wall threshold, and even the faintest texture becomes a maze of corridors. The program offers two visual styles: a classic black-on-white schematic and a blueprint mode that renders bright lines on deep blue paper. A wet/dry mix fader lets you blend the architectural overlay with the original footage for layered compositing.

:::tip
Floorplan works best with source material that has clear structural edges: architecture, faces, geometric objects, and high-contrast graphics. Soft, diffuse sources like clouds or gradients will produce fewer wall lines.
:::

### What's In a Name?

A ***floorplan*** is a scaled diagram of a room or building as seen from above, showing walls, doors, and dimensions. The name captures the program's core transformation: it reduces a video image to its structural outlines, as though an architect traced the edges of the scene onto drafting paper. Every frame becomes the blueprint for an imaginary building.

---

## Quick Start

1. Feed a video signal with strong edges into Videomancer. Turn **Sensitiv** (Knob 3) to about 75%: the background paper brightens and wall lines appear where edges exist in the source image.
2. Sweep **Wall Thk** (Knob 1) from right to left. As the value decreases, fainter edges begin registering as walls. At low settings, even subtle textures become dense networks of lines.
3. Flip **Dims** (Switch 9) to **On**. A faint 32-pixel grid appears across the entire frame, giving the image the look of graph paper or an engineering drawing.
4. Flip **Lines** (Switch 8) to **Source**. The color palette inverts to a blueprint style: bright lines on a deep blue background.

---

## Parameters

![Videomancer front panel with Floorplan loaded](/img/instruments/videomancer/floorplan/floorplan_control_panel.png)
*Videomancer's front panel with Floorplan active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Wall Thk

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Wall Thk** (Wall Thickness) sets the primary ***edge detection threshold***: the minimum brightness change between adjacent pixels that the program considers a wall. At 0%, the threshold is at its lowest: virtually every gradient in the source triggers a wall line, filling the screen with dense architectural detail. As you turn the knob clockwise, the threshold rises and the program becomes more selective, drawing only the strongest, most prominent edges. At 100%, only the sharpest transitions survive as wall lines, leaving large areas of clean background paper.

:::tip
Start with **Wall Thk** around 50% and adjust downward to reveal more detail, or upward to isolate only the boldest contours. Pair with **Door Gap** (Knob 5) to fine-tune which edges make the cut.
:::

---

### Knob 2 — Bg Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bg Bright** controls a secondary threshold for ***thick wall*** detection. This second test catches edges that fall below the primary **Wall Thk** threshold but still carry enough gradient strength to contribute to the drawing. At 0%, the secondary threshold is near zero, so almost any faint gradient adds extra wall-adjacent pixels: making lines appear thicker and bolder. Increasing the value raises this secondary bar, producing cleaner, thinner lines. At 100%, only pixels that already passed the primary threshold are drawn, and the thickening effect is minimal.

Together, **Wall Thk** and **Bg Bright** give you two levels of control over line weight: the first decides which edges appear at all, and the second decides how generously those edges are padded.

---

### Knob 3 — Sensitiv

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Sensitiv** (Sensitivity) sets the brightness of the background paper and the ceiling brightness of wall lines. At 0%, the paper is completely dark and wall outlines are invisible against it: the entire frame goes black. As you increase the value, the background brightens to a clean white (or tinted blue in blueprint mode). Wall pixels are calculated relative to this ceiling, so a brighter background produces higher-contrast wall lines. At 100%, the paper is at maximum brightness.

:::note
Because **Sensitiv** controls both the paper brightness and the wall brightness ceiling, it acts as a master contrast control for the entire floorplan rendering.
:::

---

### Knob 4 — Dim Sp

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Dim Sp** (Dimension Spacing) controls how dark the wall lines are rendered relative to the background: a ***contrast*** control for the architectural drawing. Internally, this parameter selects among three levels of edge darkening. At low values (below roughly 33%), wall lines are rendered at quarter-brightness, producing very dark, heavy strokes. In the middle range, walls render at half-brightness. At high values (above roughly 67%), walls render at full brightness relative to the background, producing the lightest, most subtle strokes.

---

### Knob 5 — Door Gap

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Door Gap** controls how aggressively the program amplifies edge gradients before threshold testing: a pre-gain or ***sensitivity*** stage. The parameter selects among four amplification levels: no amplification at 0–25%, double at 25–50%, quadruple at 50–75%, and eightfold at 75–100%. Higher amplification makes the detector responsive to weaker gradients, revealing fine textures and subtle edges. At low settings, only strong, obvious transitions trigger wall detection.

:::tip
**Door Gap** and **Wall Thk** interact directly. Increasing **Door Gap** amplifies gradients before they're compared to the threshold set by **Wall Thk**. You can achieve similar visual results by either lowering the threshold or raising the amplification: but the texture of the result differs. High amplification with a moderate threshold reveals fine detail; a low threshold with no amplification catches only broad transitions.
:::

---

### Knob 6 — Scale

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Scale** is reserved for future use. Adjusting this knob has no visible effect on the output in the current firmware version.

---

### Switch 7 — Style

| Property | Value |
|----------|-------|
| Off | Modern |
| On | Sketch |
| Default | Modern |

**Style** is reserved for future use. Toggling between **Modern** and **Sketch** has no visible effect on the output in the current firmware version.

---

### Switch 8 — Lines

| Property | Value |
|----------|-------|
| Off | Black |
| On | Source |
| Default | Black |

**Lines** selects the color scheme for the floorplan rendering. When set to **Black**, the program draws dark wall lines on a bright white background with neutral (achromatic) chroma: a classic technical drawing appearance. When set to **Source**, the program switches to ***blueprint mode***: wall pixels are rendered as bright lines on a deep blue background, and all areas: walls, grid, and paper: are tinted with a saturated blue chroma reminiscent of cyanotype architectural prints.

:::tip
Blueprint mode inverts the brightness relationship of walls: in **Black** mode, walls are darker than the paper. In **Source** (blueprint) mode, walls are ***brighter*** than the paper. This inversion creates a striking visual difference (the same edge map looks completely different in each mode.)
:::

---

### Switch 9 — Dims

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Dims** (Dimensions) enables or disables the ***dimension grid*** overlay. When set to **On**, faint ruled lines appear at fixed 32-pixel intervals across the entire frame, both horizontally and vertically. These grid lines are slightly dimmer than the background paper, creating a subtle graph-paper effect. When set to **Off**, no grid is drawn and only wall lines and background appear.

In blueprint mode, the grid lines take on the same blue tint as the rest of the frame, appearing as faint cyan rules on the dark blue paper.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** is reserved for future use. Toggling between **Off** and **On** has no visible effect on the output in the current firmware version.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Floorplan processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use **Bypass** for instant A/B comparison between the raw input and the architectural rendering.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (original) input video and the wet (processed) floorplan output. At 0%, you see only the unprocessed source. At 100%, you see the full architectural rendering. Intermediate values blend the two, allowing the original image to show through the wall lines and paper background: useful for creating a translucent overlay effect where the floorplan drawing sits on top of the source footage.

---

## Background

### Edge Detection

***Edge detection*** is one of the oldest techniques in image processing. An edge is any place in an image where pixel brightness changes abruptly: the boundary between a dark jacket and a bright wall, the outline of a face against a background, or the seam between two differently lit surfaces. The simplest way to find edges is to compare each pixel to its neighbors: if the difference in brightness exceeds some threshold, that pixel sits on an edge.

Floorplan uses this approach in two dimensions. It compares each pixel to the pixel immediately to its left (horizontal edge) and to the pixel directly above it on the previous scan line (vertical edge), stored in a single block of on-chip memory. The absolute values of both differences are added together to produce a combined ***edge strength***, which is then compared against configurable thresholds to decide whether the pixel belongs to a wall line.

### Architectural Drawing

Since antiquity, builders have communicated their designs through scaled drawings: stylized views that reduce a three-dimensional structure to flat outlines on paper. A ***floorplan*** shows a building sliced horizontally, revealing walls as thick dark lines, doorways as gaps, and rooms as the bright spaces between. The conventions of architectural drawing: black ink on white paper, or white lines on blue cyanotype stock: are so visually distinctive that we recognize them instantly.

Floorplan borrows this visual language and applies it to live video. Edges in the source material become wall lines; flat areas become paper. The ***blueprint*** color scheme references the iron-based photographic printing process (***cyanotype***) that engineers used to reproduce technical drawings for over a century. The dimension grid overlays a regular ruling across the frame, completing the illusion that you're looking at a measured plan rather than a video signal.


---

## Signal Flow

### Signal Flow Notes

Two key interactions define the processing pipeline:

1. **Edge detection is Y-only.** The program extracts horizontal and vertical gradients from the luminance channel exclusively. Chrominance is not analyzed: the U and V outputs are synthesized entirely from constants (neutral gray or blueprint blue), not derived from the input chroma. This means the floorplan rendering converts any input to a monochrome or two-tone drawing regardless of the source's color content.

2. **Two-level wall detection.** The wall composite stage evaluates two separate thresholds. The primary threshold (**Wall Thk**) determines which pixels are classified as walls. The secondary threshold (**Bg Bright**) catches weaker edges and adds them to the wall set, effectively thickening the lines. Both thresholds are compared against the same amplified edge strength, so the **Door Gap** sensitivity amplification affects both simultaneously.

:::note
The sync delay pipeline is exactly 8 clocks deep (4 processing + 4 interpolator), matching the total processing latency. Dry video data is delayed by the same 8 clocks before entering the interpolator, ensuring the mix fader blends temporally aligned samples.
:::


---

## Exercises

These exercises progress from basic wall extraction to full blueprint composition. Each builds on the previous, gradually engaging more of the processing chain.
### Exercise 1: Wall Extraction

![Wall Extraction result](/img/instruments/videomancer/floorplan/floorplan_ex1_s1.png)
*Wall Extraction — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean black-on-white architectural rendering that traces the outlines of your source video.

#### Key Concepts

- Edge detection converts brightness gradients into wall lines
- The Wall Thk threshold controls which edges are drawn
- Sensitivity amplification reveals fine detail

#### Steps

1. **Feed a source**: Connect a video input with clear structural edges (a room interior, a face, or printed graphics work well.)
2. **Brighten the paper**: Turn **Sensitiv** (Knob 3) clockwise to about 80%. The background should be a clean white.
3. **Set the threshold**: Turn **Wall Thk** (Knob 1) to about 50%. Strong edges in the source appear as dark wall lines on the white paper.
4. **Reveal more detail**: Slowly turn **Wall Thk** counter-clockwise toward 25%. Fainter edges appear, filling the frame with more architectural lines.
5. **Amplify**: Turn **Door Gap** (Knob 5) clockwise past 50%. Even subtle textures now register as walls (the drawing becomes dense and intricate.)
6. **Compare**: Toggle **Bypass** (Switch 11) to alternate between the raw input and the floorplan rendering.

#### Settings

| Control | Value |
|---------|-------|
| Wall Thk | ~25% |
| Bg Bright | ~50% |
| Sensitiv | ~80% |
| Dim Sp | ~50% |
| Door Gap | ~60% |
| Scale | ~50% |
| Style | Modern |
| Lines | Black |
| Dims | Off |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Blueprint Mode

![Blueprint Mode result](/img/instruments/videomancer/floorplan/floorplan_ex2_s1.png)
*Blueprint Mode — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A cyanotype-style blueprint with bright wall lines on deep blue paper and a ruled dimension grid.

#### Key Concepts

- Blueprint mode inverts the wall brightness relationship
- The dimension grid adds architectural ruling at fixed intervals
- Contrast controls wall line weight in both color schemes

#### Steps

1. **Switch to blueprint**: Flip **Lines** (Switch 8) to **Source**. The color scheme changes to bright lines on a saturated blue background.
2. **Enable the grid**: Flip **Dims** (Switch 9) to **On**. Faint horizontal and vertical rules appear at 32-pixel intervals, giving the image a graph-paper quality.
3. **Adjust paper darkness**: Turn **Sensitiv** (Knob 3) to about 40%. In blueprint mode, lower sensitivity produces a deeper blue background.
4. **Darken the lines**: Turn **Dim Sp** (Knob 4) fully counter-clockwise. The wall lines render at their darkest contrast: which, since blueprint mode inverts the brightness, means the brightest strokes against the dark paper.
5. **Thicken walls**: Lower **Wall Thk** (Knob 1) to about 30% and raise **Bg Bright** (Knob 2) to about 40%. The secondary threshold catches additional edge pixels, producing thicker wall lines.

#### Settings

| Control | Value |
|---------|-------|
| Wall Thk | ~30% |
| Bg Bright | ~40% |
| Sensitiv | ~40% |
| Dim Sp | ~10% |
| Door Gap | ~50% |
| Scale | ~50% |
| Style | Modern |
| Lines | Source |
| Dims | On |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Translucent Overlay

![Translucent Overlay result](/img/instruments/videomancer/floorplan/floorplan_ex3_s1.png)
*Translucent Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A composite image where the architectural line drawing is layered transparently over the original video footage.

#### Key Concepts

- The Mix fader blends the floorplan rendering with the original video
- Combining edge detection with the source creates an embossed, illustrated look
- All processing parameters affect the blend result

#### Steps

1. **Set up the drawing**: Start from the Exercise 1 settings: **Wall Thk** ~40%, **Sensitiv** ~80%, **Lines** set to **Black**, **Dims** set to **Off**.
2. **Pull back the mix**: Slide **Mix** (Fader 12) down to about 50%. The original video becomes visible beneath the wall lines and white paper.
3. **Increase sensitivity**: Turn **Door Gap** (Knob 5) to about 70%. Fine edge detail appears in the overlay, tracing the source content with dense architectural lines.
4. **Add the grid**: Flip **Dims** (Switch 9) to **On**. The dimension grid superimposes over the blended image, creating a technical overlay.
5. **Try blueprint**: Flip **Lines** (Switch 8) to **Source**. The overlay shifts to a blue-tinted transparent layer. Pull **Mix** to about 30% for a subtle blue-line tracing effect.
6. **Sweep the mix**: Slowly sweep **Mix** from 0% to 100% and back while watching the balance between the source footage and the floorplan rendering shift in real time.

#### Settings

| Control | Value |
|---------|-------|
| Wall Thk | ~40% |
| Bg Bright | ~50% |
| Sensitiv | ~80% |
| Dim Sp | ~50% |
| Door Gap | ~70% |
| Scale | ~50% |
| Style | Modern |
| Lines | Black |
| Dims | On |
| Animate | On |
| Bypass | Off |
| Mix | ~50% |

---
## Glossary

- **Blueprint**: A cyanotype reproduction of a technical drawing, characterized by white lines on a deep blue background

- **BRAM**: Block RAM; a dedicated memory tile on the FPGA used here to store one full scan line of luminance values for vertical edge comparison

- **Cyanotype**: An iron-based photographic printing process that produces blue-and-white prints, historically used to reproduce architectural and engineering drawings

- **Edge Detection**: An image processing technique that identifies pixels where brightness changes sharply between neighbors, marking boundaries between regions

- **Edge Strength**: The combined magnitude of horizontal and vertical brightness gradients at a single pixel, used to determine whether that pixel lies on an edge

- **Floorplan**: A scaled architectural diagram of a building viewed from above, showing walls, doorways, and room dimensions as outlines on paper

- **Interpolator**: A hardware module that performs linear crossfading between two input values based on a blend parameter, used here for the wet/dry mix

- **Threshold**: A minimum value that a measurement must exceed to trigger a detection; in Floorplan, the minimum edge strength required for a pixel to be classified as a wall line

---
