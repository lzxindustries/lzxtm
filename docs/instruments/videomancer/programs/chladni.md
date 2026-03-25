---
draft: true
sidebar_position: 48
slug: /instruments/videomancer/chladni
title: "Chladni"
image: /img/instruments/videomancer/chladni/chladni_hero.png
description: "In 1787, the German physicist Ernst Chladni drew a violin bow across the edge of a metal plate dusted with fine sand."
---

![Chladni hero image](/img/instruments/videomancer/chladni/chladni_hero_s1.png)
*Chladni generating luminous standing wave nodal patterns with high-harmonic mode numbers and superposition morphing.*

---

## Overview

**Chladni** conjures the ethereal geometry of vibrating plates, drawing the invisible lines where sound becomes shape. Its engine evaluates a pair of ***standing wave*** functions across the screen, superimposes them, and highlights the ***nodal lines***: the places where the vibration amplitude crosses zero. The result is a family of intricate, symmetrical patterns that shift and bloom as you dial through harmonic mode numbers. It's like sprinkling sand on a singing plate, except the sand is light and the plate is your display.

At low mode numbers, Chladni produces bold, simple divisions of the screen: broad arcs, crosses, and diamond grids. As you raise the harmonics, the figures multiply into dense lattices of fine lines reminiscent of lace, circuit boards, or the veins of a leaf. The **Superpose** control blends two mathematically degenerate modes together, morphing between fundamentally different symmetries in a single sweep. Enable **Animate** and the pattern drifts through mode space on its own, cycling through an endless gallery of figures.

:::tip
Chladni is a ***synthesis*** program: it generates its own imagery from scratch. You can also overlay its patterns onto a live video signal using the **Render** switch, turning any input into a stained-glass window of nodal geometry.
:::

### What's In a Name?

The program is named after ***Ernst Chladni***, an eighteenth-century German physicist who pioneered the study of acoustics. Chladni discovered that sprinkling fine sand on a vibrating metal plate reveals striking geometric patterns: the sand collects along the ***nodal lines*** where the plate doesn't move, tracing the standing wave structure of each resonant mode. These ***Chladni figures*** are among the oldest visualizations of wave physics, and they remain a staple of physics demonstrations to this day.

---

## Quick Start

1. Turn **Mode M** (Knob 1) and **Mode N** (Knob 2) to different positions. A lattice of bright lines and dark regions fills the screen (you've summoned a Chladni figure.)
2. Sweep **Superpose** (Knob 3) from one end to the other. Watch the figure morph between two different symmetries, as if the plate were vibrating in two ways at once.
3. Flip the **Animate** switch (Switch 8) to **Morph** and adjust **Speed** (Knob 5). The pattern drifts continuously through harmonic modes like a slow-motion kaleidoscope.
4. Experiment with **Threshold** (Knob 4) to widen or narrow the nodal lines. Thin lines create delicate filigree; thick lines produce bold stencil shapes.

---

## Parameters

![Videomancer front panel with Chladni loaded](/img/instruments/videomancer/chladni/chladni_control_panel.png)
*Videomancer's front panel with Chladni active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Mode M

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

**Mode M** selects the horizontal harmonic number, stepping through eight discrete modes. At mode 1, the pattern has a single broad division across the width of the screen. Each higher mode adds another harmonic fold, doubling and redoubling the figure's horizontal complexity. By mode 8, the screen is filled with a dense grid of fine vertical subdivisions. Mode M determines one axis of the standing wave pair: changing it reshapes the figure along the horizontal direction while leaving the vertical structure untouched.

---

### Knob 2 — Mode N

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 4 |

**Mode N** selects the vertical harmonic number, stepping through eight discrete modes. It works identically to Mode M but along the vertical axis. At mode 1, the pattern has a single broad vertical division; at mode 8, it fills the screen with many horizontal subdivisions. The interplay between Mode M and Mode N defines the overall geometry of the Chladni figure: equal values produce symmetric, diagonally balanced patterns, while unequal values create elongated or lopsided structures.

:::tip
Try setting **Mode M** and **Mode N** to the same value. The resulting figure is perfectly square-symmetric: like the classic textbook Chladni pattern for a square plate.
:::

---

### Knob 3 — Superpose

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Superpose** controls the blending coefficient between two ***degenerate modes***: two standing wave patterns that share the same resonant frequency but have different spatial orientations. At 0%, only the first mode orientation contributes. At 50%, both orientations are equally mixed, producing the most symmetric figure. At 100%, the second orientation dominates. Sweeping Superpose smoothly morphs the figure between these two extremes, rotating and reshaping the nodal lines. This is the most expressive control on the panel: a single sweep can transform a grid of diamonds into a mesh of circles.

---

### Knob 4 — Threshold

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Threshold** adjusts the width of the detected nodal lines. At low values the program highlights only the thinnest sliver where the wave function crosses zero, producing fine, delicate tracery. As you increase the value, the detection band widens, painting broader strokes around each nodal line. At high values, wide swaths of the screen are classified as "on the node," and the figure becomes bold and blocky. Threshold is essentially a sensitivity dial: it controls how close to zero the wave amplitude must be to count as a nodal line.

---

### Knob 5 — Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Speed** controls the rate of animation when **Animate** (Switch 8) is set to **Morph**. At 0%, the pattern is frozen even with Animate enabled. As you increase Speed, the horizontal mode number drifts faster, cycling the figure through a continuous sequence of harmonic shapes. At high values the pattern flows rapidly, producing a mesmerizing, ever-changing display. When Animate is set to **Static**, Speed has no visible effect.

:::note
Animation morphs only the horizontal mode (M). The vertical mode (N) remains fixed. This creates a characteristic horizontal "breathing" as the pattern evolves.
:::

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Brightness** scales the luminance of the generated pattern. At 0%, the pattern areas between nodal lines are dark, and only the nodal lines themselves are visible. Increasing Brightness reveals the contour shading of the wave function: brighter areas represent higher wave amplitude. At maximum, the full amplitude range maps to peak white, producing a high-contrast, glowing figure. Brightness does not affect the nodal line detection itself, only the luminance of the surrounding pattern.

---

### Switch 7 — Shape

| Property | Value |
|----------|-------|
| Off | Square |
| On | Cross |
| Default | Square |

**Shape** selects between two different plate geometries. In the **Square** position, the program evaluates the classical Chladni superposition formula for a square plate, adding two standing wave products with a blending coefficient. In the **Cross** position, the two products are multiplied instead of added, producing a denser, more intricate interference pattern with narrower, more numerous nodal lines. The Cross mode tends to produce lace-like textures that fill the screen more uniformly.

---

### Switch 8 — Animate

| Property | Value |
|----------|-------|
| Off | Static |
| On | Morph |
| Default | Static |

**Animate** enables or disables automatic mode morphing. In the **Static** position, the figure is frozen at whatever Mode M and Mode N values you've selected. In the **Morph** position, an internal oscillator continuously offsets the horizontal mode number, causing the pattern to drift through a sequence of harmonic figures. The rate of change is controlled by **Speed** (Knob 5).

---

### Switch 9 — Render

| Property | Value |
|----------|-------|
| Off | Overlay |
| On | Replace |
| Default | Overlay |

**Render** selects how the Chladni pattern is composited with the input video. In the **Overlay** position, the pattern modulates the incoming video: nodal lines appear as bright white lines over the image, and the wave amplitude darkens or brightens the video between the lines. Colors from the input video are preserved between lines but desaturated at the nodes. In the **Replace** position, the input video is ignored entirely: the output is a monochrome rendering of the Chladni figure with neutral gray chrominance.

:::tip
In **Overlay** mode, feed Chladni a colorful video source. The nodal lines act like a luminous web laid over the image, creating a stained-glass effect where colors are framed by glowing white geometry.
:::

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** reverses the pattern. When set to **On**, nodal lines become dark gaps instead of bright highlights, and the wave amplitude rendering is complemented: the bright and dark regions swap. Invert also flips the nodal line detection, so areas that were previously considered "on the node" become "off the node" and vice versa. Combined with Overlay mode, this turns the luminous web into a dark lattice that carves shadows into the video.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Chladni processing. The sync delay pipeline still aligns timing, so switching between processed and bypassed output is glitch-free. Use Bypass for instant A/B comparison.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original input video and the Chladni-processed output. At 0%, the output is the unmodified input. At 100%, the output is the fully processed Chladni pattern. Intermediate values blend the two, allowing you to dial in subtle pattern overlays or ghostly texture layers. Mix operates independently of the **Render** switch: in Replace mode, it fades between the source video and the monochrome pattern; in Overlay mode, it fades between the source and the composited overlay.

---

## Background

### Chladni Figures and Vibrating Plates

In 1787, Ernst Chladni published a method for visualizing the vibration modes of rigid surfaces. He drew a violin bow across the edge of a thin metal plate dusted with sand. The plate vibrated at one of its resonant frequencies, and the sand migrated to the ***nodal lines***: the curves where the plate remained stationary. The result was a beautiful, symmetric pattern unique to each resonant mode.

These patterns arise from ***standing waves***: two traveling waves moving in opposite directions combine to create a fixed pattern of alternating peaks and nodes. On a two-dimensional plate, the standing wave is described by a pair of mode numbers (m, n) that count the number of half-wavelengths in each direction. Low mode numbers produce simple figures with a few broad divisions; high mode numbers produce intricate lattices of fine lines.

### Standing Wave Mathematics

The Chladni program approximates the vibration of a rectangular plate using the formula:

*f(x, y) = tri(m · x) · tri(n · y) + k · tri(n · x) · tri(m · y)*

Here, *tri()* is a ***triangle wave***: a piecewise-linear function that rises and falls like a zigzag. It approximates the cosine function used in the true wave equation, but can be computed on an FPGA with simple shift-and-fold logic instead of expensive trigonometric hardware. The variables *m* and *n* are the mode numbers (selected by Knobs 1 and 2), and *k* is the ***superposition coefficient*** (Knob 3).

The two terms in the formula represent two ***degenerate modes***: standing wave patterns that share the same resonant frequency but are rotated 90° relative to each other. The coefficient *k* blends between them. When *k* = 0, only the first orientation appears. When *k* = ±1, the second orientation contributes fully. Sweeping *k* morphs the nodal pattern continuously between the two orientations.

### Triangle Waves and Efficient Hardware

Computing a true cosine function in hardware requires either a lookup table stored in ***block RAM*** or a complex polynomial approximation. Chladni avoids both by using a ***triangle wave***: a piecewise-linear approximation of cosine that can be computed entirely with combinational logic. The algorithm folds a linear phase counter using a bitwise XOR and a shift, producing a zigzag waveform that closely tracks the zero crossings of a cosine at a fraction of the hardware cost. The result is zero BRAM usage and a compact pipeline of roughly 800 logic cells.

### Nodal Line Detection

The visual heart of a Chladni figure is the nodal line: the curve where the wave function crosses zero. In the physical experiment, sand accumulates here because the plate isn't moving. In the digital version, the program computes the absolute value of the wave function at each pixel and compares it to a ***threshold***. If the magnitude is below the threshold, the pixel is classified as "on the node" and rendered as a bright highlight. The **Threshold** knob adjusts how wide this detection band is, controlling whether the lines appear as hairline traces or broad ribbons.


---

## Signal Flow

### Signal Flow Notes

The pattern generation pipeline runs in four clock stages followed by a four-clock interpolator, totaling eight clocks of latency. The sync delay shift register compensates by delaying the input sync signals and video data by the same eight clocks, keeping everything aligned at the output.

The most important interaction is between **Superpose** and **Shape**. In Square mode, Superpose controls the linear blend coefficient *k* between two degenerate standing wave orientations: this is the classical Chladni formula. In Cross mode, the two wave products are multiplied instead of added, and Superpose is bypassed. This produces a fundamentally different class of figures with denser, more intricate nodal networks.

:::note
In **Overlay** mode, the Y channel of the input video is modulated by the wave amplitude while the U and V channels are desaturated at nodal lines. This means nodal lines always appear as desaturated white regardless of the input color. Between the lines, the original colors of the input video are preserved but their brightness is scaled by the wave function.
:::


---

## Exercises

These exercises progress from basic pattern exploration to animated compositions. Each exercise builds on the previous, introducing more of the Chladni engine's capabilities.
### Exercise 1: Exploring Harmonic Modes

![Exploring Harmonic Modes result](/img/instruments/videomancer/chladni/chladni_ex1_s1.png)
*Exploring Harmonic Modes — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Explore the family of Chladni figures by sweeping through harmonic modes and superposition.

#### Key Concepts

- Mode numbers control the spatial frequency of the standing wave pattern
- Equal mode numbers produce square-symmetric figures
- Superpose morphs between degenerate mode orientations

#### Steps

1. **Simple figure**: Set **Mode M** (Knob 1) and **Mode N** (Knob 2) to the same value: around the middle of their range. A symmetric lattice of nodal lines fills the screen.
2. **Asymmetric figure**: Turn Mode M to a low value and Mode N to a high value. The figure stretches: few divisions horizontally, many divisions vertically.
3. **Superposition sweep**: With Mode M and Mode N at different values, slowly sweep **Superpose** (Knob 3) from one end to the other. The nodal lines rotate and reshape, morphing between two distinct symmetries.
4. **Line width**: Adjust **Threshold** (Knob 4). Low values produce hairline traces; high values produce broad, bold nodal bands.
5. **Brightness**: Increase **Brightness** (Knob 6) to reveal the wave amplitude contours between the lines (brighter areas represent higher wave magnitude.)

#### Settings

| Control | Value |
|---------|-------|
| Mode M | 3 |
| Mode N | 5 |
| Superpose | ~50% |
| Threshold | ~25% |
| Speed | 0% |
| Brightness | ~75% |
| Shape | Square |
| Animate | Static |
| Render | Replace |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Animated Morphing

![Animated Morphing result](/img/instruments/videomancer/chladni/chladni_ex2_s1.png)
*Animated Morphing — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Set the Chladni pattern in motion and compare square and cross plate geometries.

#### Key Concepts

- The animation oscillator continuously offsets the horizontal mode number
- Speed controls the morphing rate
- Cross mode produces denser, lace-like interference patterns

#### Steps

1. **Enable animation**: Flip **Animate** (Switch 8) to **Morph**. The pattern begins drifting through harmonic modes (the figure breathes and evolves.)
2. **Speed control**: Adjust **Speed** (Knob 5). At low values the morphing is glacial and meditative. At high values the figure flows rapidly, producing strobing transitions.
3. **Cross mode**: Flip **Shape** (Switch 7) to **Cross**. The pattern transforms from broad arcs into a dense, lace-like mesh. The animation takes on a more chaotic, shimmering character.
4. **Thick lines**: Increase **Threshold** (Knob 4) to about 75%. The nodal lines become wide ribbons, and the animated morphing looks like ink spreading across paper.
5. **Invert**: Toggle **Invert** (Switch 10) to **On**. The bright lines become dark voids, and the formerly dark regions glow (a photographic negative of the vibration pattern.)

#### Settings

| Control | Value |
|---------|-------|
| Mode M | 2 |
| Mode N | 4 |
| Superpose | ~50% |
| Threshold | ~75% |
| Speed | ~50% |
| Brightness | ~75% |
| Shape | Cross |
| Animate | Morph |
| Render | Replace |
| Invert | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Video Overlay Composition

![Video Overlay Composition result](/img/instruments/videomancer/chladni/chladni_ex3_s1.png)
*Video Overlay Composition — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Combine Chladni's generated pattern with a video signal to create a luminous geometric overlay.

#### Key Concepts

- Overlay mode composites the Chladni pattern onto a live video input
- Nodal lines appear as bright geometry over the video
- Mix allows subtle blending of pattern and source

#### Steps

1. **Connect a source**: Route a video signal into Videomancer. Any colorful footage works well (nature scenes, abstract video feedback, or camera input.)
2. **Switch to Overlay**: Set **Render** (Switch 9) to **Overlay**. The Chladni pattern appears as a web of bright white lines over the video. Between the lines, the video is visible but its brightness is modulated by the wave amplitude.
3. **Dial the mix**: Lower **Mix** (Fader 12) to about 60%. The pattern becomes a ghostly overlay, blending with the source.
4. **High harmonics**: Increase both **Mode M** (Knob 1) and **Mode N** (Knob 2) to high values. The overlay becomes a fine mesh of intersecting lines (like looking at the video through a luminous screen.)
5. **Animate the web**: Enable **Animate** (Switch 8) and set **Speed** (Knob 5) to a low value. The geometric overlay slowly shifts and evolves, adding organic motion to the composition.
6. **Brightness balance**: Adjust **Brightness** (Knob 6) to balance the intensity of the wave-amplitude modulation against the source video.

#### Settings

| Control | Value |
|---------|-------|
| Mode M | 6 |
| Mode N | 7 |
| Superpose | ~50% |
| Threshold | ~25% |
| Speed | ~25% |
| Brightness | ~50% |
| Shape | Square |
| Animate | Morph |
| Render | Overlay |
| Invert | Off |
| Bypass | Off |
| Mix | ~60% |

---
## Glossary

- **Chladni Figure**: A geometric pattern formed by the nodal lines of a vibrating surface, named after physicist Ernst Chladni.

- **DDS**: Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator at a controlled rate.

- **Degenerate Modes**: Two or more vibration patterns that share the same resonant frequency but differ in spatial orientation.

- **Harmonic**: A whole-number multiple of a fundamental frequency; higher harmonics produce finer spatial subdivisions.

- **Mode Number**: An integer (m or n) that specifies how many half-wavelengths fit across one dimension of the vibrating plate.

- **Nodal Line**: A curve on a vibrating surface where the displacement is always zero; sand collects here in the classic Chladni experiment.

- **Standing Wave**: A wave pattern that remains stationary in space, formed by the superposition of two traveling waves moving in opposite directions.

- **Superposition**: The principle that two or more waves can be combined by adding their amplitudes at each point in space.

- **Triangle Wave**: A piecewise-linear waveform that rises and falls in a zigzag; used here as a computationally efficient approximation of the cosine function.

---
