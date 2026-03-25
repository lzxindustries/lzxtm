---
draft: true
sidebar_position: 204
slug: /instruments/videomancer/neon
title: "Neon"
image: /img/instruments/videomancer/neon/neon_hero_s1.png
description: "Every city at dusk has them — glass tubes bent into letters and shapes, filled with ionized gas, glowing with saturated color against dark storefronts."
---

![Neon hero image](/img/instruments/videomancer/neon/neon_hero_s1.png)
*Neon rendering luminous colored edge halos over a dark background, transforming ordinary video into glowing signage.*

---

## Overview

**Neon** is an edge-detection effect that isolates the contours in your video and redraws them as glowing colored tubes on a dark field: like a neon sign traced from a live camera feed. It works by sensing horizontal brightness changes, gating them through a threshold, and feeding the result into a horizontal bloom filter that spreads light outward from each edge. The core of each tube is driven to peak white, while the surrounding halo is tinted with a configurable color. The background can be solid black or a dimmed version of the original video, simulating a sign mounted on a dark wall.

At subtle settings, Neon adds luminous edge accents to an otherwise recognizable image. At extreme settings, the original picture dissolves entirely into a constellation of colored light tubes floating in darkness. The effect responds in real time to motion and brightness changes in your source, so the glowing contours dance and shimmer as the video content moves.

:::tip
Neon works best with source material that has strong, well-defined shapes: faces, hands, text, architecture. Soft gradients produce delicate wisps; hard edges produce bold tubes.
:::

### What's In a Name?

The name ***Neon*** refers directly to neon signage: those luminous glass tubes filled with gas that glow when electrified. Real neon signs are handmade: a craftsperson bends glass tubing to trace the outline of a shape, and the gas inside produces a characteristic colored glow with a bright core and a soft halo that fades into darkness. This program recreates that look electronically, tracing the edges of live video and rendering them with the same core-plus-halo structure.

---

## Quick Start

1. Feed a source with clear shapes: a face, a hand, or some text. At default settings you should see colored edges glowing against a dark background.
2. Turn **Threshold** (Knob 1) counterclockwise to reveal more edges, or clockwise to isolate only the strongest contours. This controls how much brightness contrast is required before an edge "lights up."
3. Sweep **Glow Size** (Knob 2) clockwise. The halos widen, bleeding light further from each edge. The tubes grow fat and smoky.
4. Rotate **Hue** (Knob 4) through the full 360° range and watch the tube color cycle through the spectrum (red, yellow, green, cyan, blue, magenta, and back to red.)

---

## Parameters

![Videomancer front panel with Neon loaded](/img/instruments/videomancer/neon/neon_control_panel.png)
*Videomancer's front panel with Neon active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Threshold

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Threshold** sets the minimum brightness difference required for a pixel to register as an edge. At 0%, fully counterclockwise, even the faintest luminance gradients produce glow, filling the screen with soft light. As you increase the value, weaker edges are suppressed and only strong contours remain. At 100%, only the sharpest transitions survive (bold outlines on an otherwise dark canvas.)

:::note
Threshold interacts with the **Edge** toggle (Switch 9). In **Soft** mode, edges above the threshold retain their relative magnitude: a strong edge glows brighter than a weak one. In **Hard** mode, any edge above the threshold is slammed to maximum intensity, producing uniform tube brightness.
:::

---

### Knob 2 — Glow Size

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Glow Size** controls the width of the luminous halo surrounding each edge. Internally, this parameter adjusts the decay rate of a horizontal ***infinite impulse response*** (IIR) filter. At low values the filter decays quickly, producing tight, crisp tubes. As you increase Glow Size, the filter decays more slowly and light bleeds further from each edge, creating wide, diffuse halos. At maximum, the glow spreads broadly across the screen, and individual edges begin to merge into overlapping pools of light.

:::tip
Because the IIR filter is purely horizontal, the glow spreads left and right but not vertically. Vertical edges produce the widest visible halos, while horizontal edges produce only a thin bright line. Feed a test pattern with lines at different angles to see this directional behavior.
:::

---

### Knob 3 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Bright** scales the peak intensity of the glow. At 0%, the glow is invisible: edges are detected but produce no light. As you turn the knob clockwise, the tubes grow brighter. At high values, the core of each tube overdrives to peak white, creating the characteristic "overexposed center" look of real neon. The halo surrounding the core is tinted by the **Hue** and **Saturate** controls.

---

### Knob 4 — Hue

| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 120deg |

**Hue** selects the color of the neon glow by rotating through a six-sector color wheel. The full 360° sweep cycles through red, yellow, green, cyan, blue, and magenta. The color is applied to the halo surrounding each edge: the core of the tube tends toward white regardless of hue, just as the hottest part of a real neon tube washes out to white.

This control has no effect when the **Color** toggle (Switch 7) is set to **Source**, because in that mode the glow takes its color from the original video rather than from the fixed hue wheel.

---

### Knob 5 — Saturate

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Saturate** controls how vivid the glow color is. At 0%, the glow is monochrome white: no color tinting is applied. As you increase the value, the halo takes on the hue selected by Knob 4. At maximum, the color is fully saturated. Moderate values produce pastel tints; high values produce intense, candy-colored tubes.

Like **Hue**, this control has no effect when the **Color** toggle is set to **Source**.

---

### Knob 6 — Bg Level

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 6% |

**Bg Level** controls the brightness of the background behind the neon tubes. At 0%, the background is completely black. As you increase the value, the background lightens. The behavior depends on the **Bg Style** toggle (Switch 8):

- In **Black** mode, the background is a uniform dark field. **Bg Level** adds a small amount of flat gray (like adjusting the ambient light in a dark room.)
- In **Dim Vid** mode, the background is a dimmed version of the original video. **Bg Level** controls the dimming intensity, from fully black (0%) to a recognizable but subdued version of the source (higher values).

---

### Switch 7 — Color

| Property | Value |
|----------|-------|
| Off | Fixed |
| On | Source |
| Default | Fixed |

**Color** selects the source of the glow tint. In the **Fixed** position, the glow color is determined by the **Hue** and **Saturate** knobs, producing a uniform tube color across the entire image. In the **Source** position, each pixel's glow takes its color from the original video's chrominance channels: edges glow in the colors of whatever they're outlining. A red object produces red tubes; a blue object produces blue tubes.

:::tip
**Source** mode creates a stained-glass look where the neon outlines inherit the palette of the original scene. Try it with colorful footage: the result resembles a luminous line drawing colored with the source material.
:::

---

### Switch 8 — Bg Style

| Property | Value |
|----------|-------|
| Off | Black |
| On | Dim Vid |
| Default | Black |

**Bg Style** selects what fills the space behind the neon tubes. In the **Black** position, the background is a uniform dark field: the classic neon-sign-on-black look. In the **Dim Vid** position, the background is a dimmed and desaturated version of the original video, letting you see the source content behind the glowing edges. Use **Bg Level** (Knob 6) to control how much of the background is visible.

---

### Switch 9 — Edge

| Property | Value |
|----------|-------|
| Off | Soft |
| On | Hard |
| Default | Soft |

**Edge** selects between two threshold behaviors. In the **Soft** position, edges above the threshold retain their original magnitude: strong edges glow brighter than weak ones, producing a natural, graded look. In the **Hard** position, any edge above the threshold is driven to full intensity, producing uniform tube brightness regardless of the original edge strength. Hard mode creates bold, uniform outlines reminiscent of cartoon cel shading.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** reverses the final luminance after compositing. With Invert **Off**, glowing tubes are bright on a dark background: the standard neon look. With Invert **On**, the image is complemented: tubes become dark outlines on a bright field. The effect resembles an X-ray or photographic negative of the neon sign.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Neon processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (neon-processed) output. At 0%, you hear: er, see: only the original video. At 100%, you see only the neon effect. Intermediate values blend the two, letting you dial in a subtle glow overlay on top of the source image. This is useful for adding luminous accents without completely replacing the original picture.

---

## Background

### Edge detection

***Edge detection*** is a fundamental image analysis technique that identifies locations in a picture where brightness changes sharply. Edges correspond to the boundaries between objects, shadows, textures, and other visual features. Neon uses the simplest form: a ***first-order horizontal difference***. For each pixel, it subtracts the previous pixel's brightness from the current pixel's brightness and takes the absolute value. A large difference means a strong edge; a small difference means a smooth gradient.

This horizontal-only approach means Neon is sensitive to vertical edges (where brightness changes from left to right) and insensitive to purely horizontal edges (where brightness changes from top to bottom). In practice, most natural imagery contains edges at many angles, so the effect is convincing: but you'll notice that perfectly horizontal stripes produce no glow at all.

### IIR glow filter

The glow surrounding each edge is produced by a horizontal ***infinite impulse response*** (IIR) filter: also called a ***leaky integrator*** or ***exponential moving average***. The filter maintains a running value that rises when it encounters an edge and decays exponentially between edges. The decay rate is controlled by the **Glow Size** knob: a slow decay produces wide halos, and a fast decay produces tight tubes.

Mathematically, each pixel's glow value is: `glow = prev - (prev >> shift) + (edge >> shift)`, where `shift` ranges from 1 (widest) to 4 (narrowest). This is a classic single-pole low-pass filter implemented entirely in integer arithmetic with bit shifts: no multipliers required for this stage. The result is a bloom that trails to the right of each edge and, because the next scanline feeds its own IIR instance, each line glows independently.

### Hue mapping

Neon maps the **Hue** knob to a six-sector piecewise approximation of a color wheel. The 10-bit hue value is divided into six equal sectors, and each sector defines a pair of UV offsets from neutral gray (512, 512). The **Saturate** knob scales the magnitude of those offsets: at zero saturation, UV stays at neutral and the glow is white; at full saturation, UV swings to the edge of the color gamut.

The six sectors roughly correspond to: red → yellow-green → cyan → blue → magenta → orange. The transitions between sectors are stepped rather than smoothly interpolated, so you may notice slight color jumps as you sweep the Hue knob. This is a deliberate design choice that keeps the FPGA resource usage low while providing a usable palette of neon colors.


---

## Signal Flow

### Signal Flow Notes

The Y channel carries the edge detection and glow logic. The first-order difference operates on adjacent pixels within a single scan line: it's a purely horizontal gradient detector. The IIR glow filter is also horizontal, maintaining one running accumulator per line (reset implicitly at blanking). This means the glow has a directional bias: it trails to the right of each edge because the filter processes pixels left to right.

The UV channels follow a separate path. Instead of detecting edges in color, Neon applies a fixed color (from the hue wheel) or the source video's own chrominance to the glow. A threshold of 64 on the glow magnitude determines which UV source appears at each pixel: where glow is visible, the tube's color dominates; where glow is faint, the background's color shows through. This creates a clean separation between the luminous tube regions and the dark background.

:::note
The glow-to-UV threshold is fixed at 64 (out of 1023) in the VHDL. This is not user-adjustable: it's tuned internally to prevent color fringing in the transition zone between glow and background.
:::


---

## Exercises

These exercises progress from basic edge extraction to full neon sign composition, each building on the techniques of the previous one.
### Exercise 1: Basic Neon Edges

![Basic Neon Edges result](/img/instruments/videomancer/neon/neon_ex1_s1.png)
*Basic Neon Edges — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Isolate the strongest edges from a video source and render them as glowing tubes on a black background.

#### Key Concepts

- Horizontal edge detection via first-order difference
- Threshold controls edge sensitivity
- Glow Size controls halo width

#### Video Source

A live camera feed or recorded footage with clear shapes: faces, hands, text, or architectural features with strong contrast.

#### Steps

1. **Reveal edges**: Start with **Threshold** (Knob 1) at its default. You should see colored glow lines tracing the strongest contours.
2. **Lower threshold**: Turn Threshold counterclockwise to 20%. More edges appear (finer details and weaker gradients begin to glow.)
3. **Widen glow**: Increase **Glow Size** (Knob 2) to about 75%. The halos widen dramatically, bleeding light across the screen.
4. **Max brightness**: Turn **Bright** (Knob 3) fully clockwise. The tube cores overdrive to white while the halos remain tinted.
5. **Hard edges**: Flip the **Edge** toggle (Switch 9) to **Hard**. All visible edges now glow at uniform intensity (the image looks like a neon line drawing.)

#### Settings

| Control | Value |
|---------|-------|
| Threshold | ~20% |
| Glow Size | ~75% |
| Bright | 100% |
| Hue | 120° |
| Saturate | ~75% |
| Bg Level | 0% |
| Color | Fixed |
| Bg Style | Black |
| Edge | Hard |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Neon Sign on a Dark Wall

![Neon Sign on a Dark Wall result](/img/instruments/videomancer/neon/neon_ex2_s1.png)
*Neon Sign on a Dark Wall — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Compose a neon sign effect where glowing edges float over a dimmed version of the original video (like a sign mounted on a dark storefront.)

#### Key Concepts

- Background modes: black vs. dimmed source video
- Color source: fixed hue vs. source chrominance
- Background level interaction with background style

#### Video Source

Footage with recognizable subjects and moderate color (a street scene, a portrait, or a still life.)

#### Steps

1. **Set the sign**: Start with the settings from Exercise 1. You should have bright neon edges on black.
2. **Reveal the wall**: Flip **Bg Style** (Switch 8) to **Dim Vid**. The original video appears behind the glow, heavily dimmed.
3. **Brighten the wall**: Increase **Bg Level** (Knob 6) until the background is faintly visible (around 50–60%. The neon tubes should still dominate.)
4. **Source colors**: Flip **Color** (Switch 7) to **Source**. Each tube now glows in the color of the object it's outlining. Faces glow warm; sky glows blue.
5. **Soften**: Flip **Edge** (Switch 9) back to **Soft**. Stronger edges glow brighter than weak ones, creating a more naturalistic depth illusion.
6. **Blend**: Pull the **Mix** fader (Fader 12) down to about 70%. The neon effect blends with the dry signal, adding glow accents on top of the original image.

#### Settings

| Control | Value |
|---------|-------|
| Threshold | ~20% |
| Glow Size | ~50% |
| Bright | ~75% |
| Hue | 0° |
| Saturate | ~75% |
| Bg Level | ~55% |
| Color | Source |
| Bg Style | Dim Vid |
| Edge | Soft |
| Invert | Off |
| Bypass | Off |
| Mix | ~70% |

---

### Exercise 3: Inverted X-Ray Glow

![Inverted X-Ray Glow result](/img/instruments/videomancer/neon/neon_ex3_s1.png)
*Inverted X-Ray Glow — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Create an inverted neon effect where dark contour lines carve into a bright field (like an X-ray or photographic negative of a neon sign.)

#### Key Concepts

- Invert transforms bright-on-dark to dark-on-bright
- Combining invert with dim video background creates ethereal negatives
- Mix blending creates layered compositions

#### Video Source

High-contrast footage works best: black-and-white graphics, strong silhouettes, or text on a plain background.

#### Steps

1. **Start from defaults**: Set all controls to their default positions.
2. **Strong glow**: Set **Glow Size** (Knob 2) to about 70% and **Bright** (Knob 3) to maximum. Bold, fat tubes.
3. **Invert**: Flip the **Invert** toggle (Switch 10) to **On**. The image flips (dark tubes on a bright, washed-out field.)
4. **Add background**: Set **Bg Style** (Switch 8) to **Dim Vid** and raise **Bg Level** (Knob 6) to about 40%. The inverted tubes now carve dark channels through a ghostly image of the source.
5. **Color**: Choose a cool hue: try around 200° (cyan-blue). With inversion, the tint appears in the bright field rather than in the tubes.
6. **Hard edges**: Flip **Edge** (Switch 9) to **Hard** for uniform contour width. The result looks like an etched plate or X-ray negative.

#### Settings

| Control | Value |
|---------|-------|
| Threshold | ~38% |
| Glow Size | ~70% |
| Bright | 100% |
| Hue | ~200° |
| Saturate | ~75% |
| Bg Level | ~40% |
| Color | Fixed |
| Bg Style | Dim Vid |
| Edge | Hard |
| Invert | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Edge Detection**: Identifying locations in an image where brightness changes sharply, corresponding to boundaries between objects or textures.

- **First-Order Difference**: The simplest gradient measure: the absolute value of the difference between two adjacent pixel values.

- **Halo**: The soft luminous glow surrounding the bright core of a neon tube, produced by the IIR bloom filter.

- **Hue**: The angular position on a color wheel, measured in degrees. 0° is red, 120° is green, 240° is blue.

- **IIR Filter**: Infinite Impulse Response filter: a feedback-based filter whose output depends on both the current input and previous outputs, producing exponentially decaying tails.

- **Leaky Integrator**: A type of IIR filter that accumulates input over time while losing a fraction of its stored value each clock cycle, creating a bloom or decay effect.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Neon**: A noble gas that glows orange-red when electrified in a glass tube; by extension, any gas-discharge signage using colored tubes.

- **Saturation**: The intensity or purity of a color. Zero saturation is gray; full saturation is the most vivid version of a hue.

- **Threshold**: A cutoff value below which a signal is suppressed. In Neon, it determines the minimum edge strength required to produce glow.

---
