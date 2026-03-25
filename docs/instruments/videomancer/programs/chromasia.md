---
draft: true
sidebar_position: 50
slug: /instruments/videomancer/chromasia
title: "Chromasia"
image: /img/instruments/videomancer/chromasia/chromasia_hero_s1.png
description: "Every video effects box from the 1980s and 1990s shipped with a bank of colour transformations — negative, solarise, posterise, sepia — accessible by punching a number on a keypad or scrolling through a menu."
---

![Chromasia hero image](/img/instruments/videomancer/chromasia/chromasia_hero_s1.png)
*Chromasia applying its eight-mode color processing chain to transform video through negative, solarize, posterize, colorize, sepia, threshold, color swap, and sketch effects.*

---

## Overview

Chromasia is a multi-mode color processor inspired by the legendary NewTek Video Toaster's ChromaFX bank. It packs eight switchable color effects into a single program, selected by a three-bit toggle combination. Each mode transforms video in a fundamentally different way: from simple color inversion to edge-detected sketch lines: and every mode responds to the same set of knobs, letting you reshape the effect with familiar, consistent controls.

At its gentlest, Chromasia adds a warm sepia wash or a subtle single-hue tint. At its most aggressive, it crushes video into hard black-and-white thresholds, swaps color channels into alien palettes, or reduces the image to sketch-like edge outlines. The **Mix** fader lets you crossfade between the dry input and the processed result, so you can dial in exactly as much transformation as you want.

:::tip
Think of Chromasia as a ***spell book*** with eight pages. Each toggle combination opens a different page, and the six knobs shape the spell on that page.
:::

### What's In a Name?

The name ***Chromasia*** blends ***chroma***, the Greek word for color, with ***-asia***, evoking a dreamlike, fantastical quality: a land where color behaves differently. It's also a nod to ***chromatic aberration*** and ***synesthesia***, the blending of senses. In Chromasia's world, brightness can become hue, edges can become drawings, and channels can trade places.

---

## Quick Start

1. Set all three **Mode** toggles (Switches 7, 8, 9) to Off. This selects **Negative** mode. Your video inverts (darks become lights, lights become darks.)
2. Flip **Mode A** (Switch 7) to On, leaving the others Off. This selects **Solarize** mode. Turn **Intensity** (Knob 1) slowly. Watch as the solarization threshold sweeps across the tonal range, creating a folded, metallic look.
3. Now set **Mode A** to On and **Mode B** to On (Switches 7 and 8 both On, Switch 9 Off). This selects **Colorize** mode. Turn the **Hue** knob (Knob 3) to paint the entire image in a single rotating color.
4. Adjust the **Mix** fader (Fader 12) to blend the colorized result with the original. At 50%, you get a tinted overlay; at 100%, full effect.

---

## Parameters

![Videomancer front panel with Chromasia loaded](/img/instruments/videomancer/chromasia/chromasia_control_panel.png)
*Videomancer's front panel with Chromasia active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Intensity

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Intensity** is the primary parameter for most modes, though its exact behavior depends on which mode is active. In **Solarize** mode, Intensity sets the fold threshold: values below this point pass through unchanged, while values above it are reflected back downward, creating a V-shaped transfer curve. In **Posterize** mode, Intensity controls how many quantization levels remain: fully counterclockwise yields extreme 1-bit banding, while fully clockwise preserves nearly all detail. In **Sepia** mode, Intensity controls the warmth of the brown tint: higher values push the image further from neutral. In **Threshold** mode, Intensity sets the cutoff level for the binary black-and-white conversion.

:::note
In **Negative**, **Colorize**, **Color Swap**, and **Sketch** modes, Intensity has no visible effect. Those modes use other dedicated controls.
:::

---

### Knob 2 — Secondary

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Secondary** is a mode-dependent auxiliary parameter. Its primary role is in **Color Swap** mode, where it selects one of eight channel-routing sub-modes. The top three bits of the Secondary value determine which routing applies, so turning the knob steps through discrete swap configurations rather than producing a smooth sweep. In other modes, Secondary has no visible effect.

:::tip
In **Color Swap** mode, you can think of the **Secondary** knob as a ***rotary switch*** with eight positions. Each position defines a different wiring diagram for how Y, U, and V channels are shuffled.
:::

---

### Knob 3 — Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Hue** controls the tint angle in **Colorize** mode. Turning the knob sweeps through the full 360° color wheel. At 0°, the tint is dominated by blue-cyan tones. Rotating clockwise moves through greens, yellows, reds, magentas, and back around. The hue value addresses a 64-entry sine/cosine lookup table that generates U and V chroma offsets, producing a smooth circular sweep through color space. In modes other than Colorize, the Hue knob has no effect.

---

### Knob 4 — Saturation

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Saturation** controls the chroma intensity of the applied tint in **Colorize** mode. At 0%, fully counterclockwise, the chroma offsets are zero regardless of the Hue setting: the image remains desaturated. As Saturation increases, the single-hue tint grows stronger, pushing U and V channels further from neutral. At 100%, the tint is at full strength. In modes other than Colorize, this control has no visible effect.

---

### Knob 5 — Edge Gain

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Edge Gain** controls the sensitivity of horizontal edge detection in **Sketch** mode. The sketch algorithm computes the absolute difference between each pixel and its left neighbor, then multiplies by the Edge Gain value. Low gain produces faint, subtle outlines of only the strongest edges. High gain amplifies even small brightness transitions into bold dark lines. The result is rendered as dark strokes on a white background. In modes other than Sketch, Edge Gain has no effect.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |

**Brightness** is mapped to the register but is not directly applied in the current VHDL implementation: it is reserved for future use as an output brightness offset. In the current version, this knob has no visible effect.

:::note
The **Brightness** parameter is defined in the program metadata and mapped to `registers_in(5)`, but the processing pipeline does not currently read it. It may be activated in a future firmware update.
:::

---

### Switch 7 — Mode A

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mode A** is bit 0 of the three-bit mode selector. Together with **Mode B** (Switch 8) and **Mode C** (Switch 9), it selects which of the eight processing modes is active. See the Toggle Group Notes below for the complete mode table.

---

### Switch 8 — Mode B

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mode B** is bit 1 of the three-bit mode selector. Combined with **Mode A** and **Mode C**, it selects the active processing mode. See the Toggle Group Notes below for the full table.

---

### Switch 9 — Mode C

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mode C** is bit 2 of the three-bit mode selector. It is the highest-order bit of the mode selection, so flipping this single switch jumps between the lower four modes (Negative, Solarize, Posterize, Colorize) and the upper four modes (Sepia, Threshold, Color Swap, Sketch). See the Toggle Group Notes below for the full table.

---

### Switch 10 — All Channels

| Property | Value |
|----------|-------|
| Off | Y Only |
| On | YUV |
| Default | Y Only |

**All Channels** determines whether the active mode processes only the luminance channel or all three YUV channels. When set to **Y Only**, modes like Negative, Solarize, and Posterize affect only the brightness (Y) while leaving chrominance (U, V) untouched. When set to **YUV**, the same operation is applied to all three channels simultaneously, producing dramatically different color results. This toggle is most impactful in Negative, Solarize, and Posterize modes.

:::tip
Try **Negative** mode with **All Channels** set to **Y Only**: you get a luminance inversion that looks like a film negative, but the colors stay recognizable. Switch to **YUV** and the colors also invert, producing true complementary color reversal.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Chromasia processing. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

:::note Toggle Group Notes

Toggles 7, 8, and 9 (**Mode A**, **Mode B**, **Mode C**) form a 3-bit binary mode selector. Together they choose one of eight processing modes:

| Mode C (Sw 9) | Mode B (Sw 8) | Mode A (Sw 7) | Binary | Mode |
|:-:|:-:|:-:|:-:|:--|
| Off | Off | Off | 000 | **Negative** — inverts pixel values (complement) |
| Off | Off | On | 001 | **Solarize** — V-curve fold around Intensity threshold |
| Off | On | Off | 010 | **Posterize** — bit-mask quantization controlled by Intensity |
| Off | On | On | 011 | **Colorize** — desaturate and apply single Hue tint |
| On | Off | Off | 100 | **Sepia** — desaturate and apply warm brown tint |
| On | Off | On | 101 | **Threshold** — binary black/white at Intensity cutoff |
| On | On | Off | 110 | **Color Swap** — channel routing selected by Secondary |
| On | On | On | 111 | **Sketch** — horizontal edge detection with Edge Gain |

Only one mode is active at a time. The mode selection is purely combinational: switching toggles produces an instant transition with no glitch or fade.

#### Color Swap Sub-Modes

Within **Color Swap** mode (binary 110), the **Secondary** knob selects one of eight channel-routing patterns via its top three bits:

| Secondary Range | Sub-Mode | Routing |
|:-:|:-:|:--|
| 0–12% | Identity | Y → Y, U → U, V → V (no change) |
| 13–24% | U↔V | U and V swap places |
| 25–37% | Y→U | Luma replaces U; V unchanged |
| 38–49% | Y→V | Luma replaces V; U unchanged |
| 50–62% | Rotate CW | V → Y, Y → U, U → V |
| 63–74% | Rotate CCW | U → Y, V → U, Y → V |
| 75–87% | Average | (U+V)/2 → Y, Y → U, Y → V |
| 88–100% | Monochrome | Y → all three channels |

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (processed) output. At 0%, the output is entirely the original signal. At 100%, the output is entirely the processed result. Intermediate values blend the two. The crossfade is implemented using three parallel interpolators (one per YUV channel) with 4-clock latency each.

:::tip
**Mix** is powerful for subtle effects. A **Threshold** at full effect is stark black-and-white, but mixed at 30% it becomes a gentle contrast boost. A **Solarize** at full strength is dramatic, but at 20% it adds a soft metallic sheen.
:::

---

## Background

### The NewTek Video Toaster ChromaFX Legacy

Chromasia is a spiritual successor to the ***ChromaFX*** effects bank from the NewTek Video Toaster, the groundbreaking Amiga-based video production system of the early 1990s. ChromaFX offered a panel of color transformations: negative, solarize, posterize, colorize, sepia: that could be applied to live video in real time. These were among the first affordable real-time digital color effects available to independent video producers, and they became iconic visual signatures of the era. Chromasia reimagines that toolkit in modern FPGA hardware, adding channel-swap and sketch modes while providing fine parametric control over each effect.

### Solarization and the Sabattier Effect

The solarization mode implements a ***V-curve transfer function***, a digital simulation of the ***Sabattier effect*** from darkroom photography. In the analog darkroom, briefly re-exposing a partially developed print causes tones near the exposure threshold to reverse, creating haunting, metallic-looking images with mixed positive and negative regions. Chromasia's digital version uses the **Intensity** knob as the threshold: pixel values below the threshold pass through unchanged, while values above it are reflected downward. The result is a symmetric fold in the tonal curve that produces the same eerie partial-reversal look.

### Colorization and Hue Mapping

The colorize mode strips all existing color from the image and replaces it with a single hue. Internally, this works by setting the U and V chroma channels to offsets computed from a 64-entry sine/cosine ***lookup table*** addressed by the **Hue** parameter. The sine and cosine values trace a circle in the UV color plane, and the **Saturation** parameter scales the radius of that circle. The result is a monochromatic wash: the image retains its brightness contours but all color information comes from the chosen hue angle.

### Edge Detection and Sketch

The sketch mode performs ***horizontal edge detection*** by computing the absolute brightness difference between each pixel and its immediate left neighbor. This one-pixel delay creates a simple ***finite difference*** gradient detector. Strong brightness transitions produce large differences, which the **Edge Gain** parameter amplifies. The output is rendered as dark lines on a white background: white minus the scaled edge magnitude: so that edges appear as dark pencil strokes against a clean field. Because only horizontal differences are computed (no vertical component), the sketch emphasizes vertical edges and contour lines more than horizontal ones.


---

## Signal Flow

### Signal Flow Notes

The critical architectural insight is that all eight modes are computed ***in parallel*** every clock cycle, and a single multiplexer selects which mode's output reaches the composite register. This means switching modes via the toggles produces an instantaneous, glitch-free transition: there's no reconfiguration delay, no pipeline flush. Every mode is always "running" in the background.

The **All Channels** toggle (Switch 10) controls whether Negative, Solarize, and Posterize apply their transformation to all three YUV channels or only to Y. For Colorize, Sepia, Threshold, and Sketch, the chroma handling is hardcoded: Colorize and Sepia replace U/V with computed values, Threshold and Sketch force U/V to neutral midpoint.

:::tip
Because all modes run in parallel, the FPGA resource cost is the ***sum*** of all eight modes, not just the active one. This is why Chromasia uses zero BRAM: all processing is purely combinational and register-based, keeping the resource footprint low enough to fit all eight modes simultaneously.
:::


---

## Exercises

These exercises explore three progressively complex uses of Chromasia's mode-switching architecture, from single-mode color manipulation to rapid mode-switching performance.
### Exercise 1: Solarize Sweep

![Solarize Sweep result](/img/instruments/videomancer/chromasia/chromasia_ex1_s1.png)
*Solarize Sweep — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A slowly sweeping solarization effect that reveals the Sabattier-like metallic tonal inversion across the full brightness range.

#### Key Concepts

- Solarization creates a V-curve fold in the tonal range
- The Intensity threshold determines where the fold occurs
- All Channels extends the fold to chrominance

#### Video Source

A live camera feed or recorded footage with a wide tonal range (faces, landscapes, or anything with smooth gradients.)

#### Steps

1. Select **Solarize** mode: set **Mode A** (Switch 7) to On, **Mode B** (Switch 8) and **Mode C** (Switch 9) to Off.
2. Set **Mix** (Fader 12) to 100% so the full effect is visible.
3. Turn **Intensity** (Knob 1) slowly from minimum to maximum. Watch the solarization threshold sweep across the image: tones above the threshold fold downward, creating metallic, molten-looking regions.
4. Set **All Channels** (Switch 10) to **YUV**. The fold now applies to the color channels as well, producing surreal rainbow inversions in the solarized regions.
5. Back **Mix** down to about 50%. The solarized version blends with the original, creating a subtle iridescent overlay.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~75% |
| Secondary | 0% |
| Hue | 0° |
| Saturation | 50% |
| Edge Gain | 0% |
| Brightness | 0% |
| Mode A | On |
| Mode B | Off |
| Mode C | Off |
| All Channels | YUV |
| Bypass | Off |
| Mix | 50% |

---

### Exercise 2: Colorize and Sepia Tinting

![Colorize and Sepia Tinting result](/img/instruments/videomancer/chromasia/chromasia_ex2_s1.png)
*Colorize and Sepia Tinting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A tinted monochrome look, transitioning from cool single-hue colorization to warm sepia.

#### Key Concepts

- Colorize replaces all chroma with a single hue angle
- Saturation controls the strength of the applied tint
- Sepia applies a fixed warm brown tint scaled by Intensity

#### Video Source

Black-and-white or muted footage works well, but any source benefits from tinting.

#### Steps

1. Select **Colorize** mode: set **Mode A** (Switch 7) to On, **Mode B** (Switch 8) to On, **Mode C** (Switch 9) to Off.
2. Set **Saturation** (Knob 4) to about 30%. Turn **Hue** (Knob 3) slowly. The entire image tints with a single pure color that sweeps through the rainbow.
3. Increase **Saturation** to 80%. The color becomes vivid and dominant (the image becomes a monochrome study in your chosen hue.)
4. Now switch to **Sepia** mode: set **Mode C** (Switch 9) to On, **Mode A** (Switch 7) to Off, **Mode B** (Switch 8) to Off.
5. Turn **Intensity** (Knob 1) to about 75%. The image takes on the warm, nostalgic brown tone of an old photograph. Higher Intensity pushes the tone further from neutral.
6. Lower **Mix** (Fader 12) to about 40% for a subtle vintage warmth layered over the original colors.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | 75% |
| Secondary | 0% |
| Hue | 180° |
| Saturation | 30% |
| Edge Gain | 0% |
| Brightness | 0% |
| Mode A | Off |
| Mode B | Off |
| Mode C | On |
| All Channels | Y Only |
| Bypass | Off |
| Mix | 40% |

---

### Exercise 3: Sketch Threshold Mask

![Sketch Threshold Mask result](/img/instruments/videomancer/chromasia/chromasia_ex3_s1.png)
*Sketch Threshold Mask — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A high-contrast sketch effect where bold edge outlines emerge from a thresholded image, resembling a pen-and-ink drawing.

#### Key Concepts

- Sketch mode detects horizontal edges via pixel-to-pixel luminance difference
- Edge Gain amplifies subtle transitions into bold lines
- Threshold mode can be layered via Mix for contrast enhancement

#### Video Source

Footage with strong structural content: architecture, text, mechanical objects, or faces with clear contour lines.

#### Steps

1. Select **Sketch** mode: set all three mode toggles to On (**Mode A**, **Mode B**, **Mode C** all On).
2. Set **Edge Gain** (Knob 5) to about 70%. Bold dark lines appear at brightness transitions, drawn on a white background.
3. Set **Mix** (Fader 12) to 100% to see the full sketch effect.
4. Lower **Edge Gain** to about 30%. Only the strongest edges survive: finer detail fades into the white field. Increase back to 90% for aggressive, detailed line work.
5. Now switch to **Threshold** mode: set **Mode A** (Switch 7) to On, **Mode B** (Switch 8) to Off, **Mode C** (Switch 9) to On.
6. Set **Intensity** (Knob 1) to about 50%. The image snaps to stark black and white.
7. Lower **Mix** to about 70% and compare the feel of Threshold's hard binary key versus Sketch's edge-detected line drawing.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | 50% |
| Secondary | 0% |
| Hue | 0° |
| Saturation | 50% |
| Edge Gain | 70% |
| Brightness | 0% |
| Mode A | On |
| Mode B | On |
| Mode C | On |
| All Channels | Y Only |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Chroma**: The color information in a video signal, encoded as U and V components in YUV color space, where U and V values of 512 represent neutral (no color).

- **Complement**: The arithmetical inverse of a pixel value; for a 10-bit signal, the complement of a value *x* is 1023 − *x*.

- **Edge Detection**: A technique for finding boundaries in an image by measuring the rate of change (gradient) of brightness between neighboring pixels.

- **Finite Difference**: A discrete approximation of a derivative, computed by subtracting adjacent sample values. Chromasia uses a first-order horizontal finite difference for sketch mode.

- **Interpolator**: A circuit that smoothly blends between two values using a fractional mix parameter; used here for the dry/wet crossfade.

- **Lookup Table (LUT)**: A precomputed array of values that replaces real-time calculation; Chromasia's colorize mode uses a 64-entry sine/cosine LUT for hue mapping.

- **Posterization**: Reducing the number of distinct tonal levels by discarding low-order bits, producing flat bands of uniform color.

- **Sabattier Effect**: A darkroom technique in which partial re-exposure during development produces a mix of positive and negative tones; digital solarization simulates this with a V-curve transfer function.

- **Solarization**: A tonal transformation that folds brightness values around a threshold, creating regions of reversed contrast within the image.

- **Transfer Function**: The mathematical relationship between input and output values for each pixel; Chromasia's modes implement different transfer functions (linear complement, V-curve fold, step function, etc.).

---
