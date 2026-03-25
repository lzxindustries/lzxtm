---
draft: true
sidebar_position: 216
slug: /instruments/videomancer/parallax
title: "Parallax"
image: /img/instruments/videomancer/parallax/parallax_hero.png
description: "In the 1980s and early 1990s, the Amiga computer's custom Copper coprocessor could change hardware color registers on a per-scanline basis, enabling programmers to produce smooth horizontal color gradients and scrolling raster bar effects that seemed impossible for the era's hardware."
---

![Parallax hero image](/img/instruments/videomancer/parallax/parallax_hero_s1.png)
*Parallax generating scrolling color-cycling raster bars with the Neon palette, blending neon pinks and cyans over a live video feed in additive mode.*

---

## Overview

Parallax is a color-cycling raster bar generator inspired by the Amiga ***Copper*** coprocessor and the demoscene tradition. It paints horizontal bands of color that scroll vertically across the screen, each scanline picking its color from one of eight curated palettes. An optional horizontal oscillator adds a second dimension of color variation, producing swirling ***plasma*** patterns that fill the frame with shifting, iridescent hues.

What makes Parallax distinctive is the way it responds to video input. The incoming picture's brightness can modulate the bar colors, so the generated pattern wraps around live footage like colored cellophane or neon light. Two blend modes control the interaction: multiply mode darkens bars according to the video, and additive mode layers bars on top of the image as a luminous overlay.

:::tip
Parallax is classified as a ***synthesis*** program: it generates imagery from scratch. The video input is optional: with **Video Depth** at zero, the bars stand on their own. Increase Video Depth to blend the input video into the raster effect.
:::

### What's In a Name?

The name ***Parallax*** evokes the optical phenomenon where objects at different depths appear to move at different speeds: a staple of side-scrolling video games. In those games, background layers scroll at different rates to create an illusion of depth. Here, the horizontal and vertical color oscillators work similarly: each axis cycles at its own frequency, and as they combine, the colored bands seem to slide past one another at different speeds, creating an illusion of layered, shifting depth.

---

## Quick Start

1. Turn **V Freq** (Knob 1) clockwise to about 40%. Horizontal bands of color appear, evenly spaced across the screen. The default palette is Rainbow (a full-spectrum hue cycle.)
2. Slowly adjust **Scroll** (Knob 2) away from center. The bars begin to drift upward or downward. Turning clockwise scrolls one direction; counterclockwise scrolls the other.
3. Rotate **Palette** (Knob 5) to step through the eight color palettes. Each click of the stepped selector reveals a different mood: warm copper gradients, deep ocean blues, neon synthwave, phosphor greens.
4. Feed a video signal into the input and increase **Video Depth** (Knob 4). The bars begin to respond to the brightness of the source, wrapping around shapes in the picture like colored light through stained glass.

---

## Parameters

![Videomancer front panel with Parallax loaded](/img/instruments/videomancer/parallax/parallax_control_panel.png)
*Videomancer's front panel with Parallax active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — V Freq

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**V Freq** controls the vertical frequency of the raster bars: how many color bands appear from top to bottom of the screen. At 0%, fully counterclockwise, a single sweep of the palette spans the entire frame height, producing very wide bands. As the value increases, the bars get thinner and more numerous. At 100%, fully clockwise, the bars are tightly packed and the palette repeats many times across the screen.

V Freq drives a ***direct digital synthesis*** (DDS) accumulator that increments once per scanline. The accumulator's phase determines which palette color is selected for that line. Higher frequency values mean larger per-line increments and faster cycling through the palette.

---

### Knob 2 — Scroll

| Property | Value |
|----------|-------|
| Range | -180° – 180° |
| Default | 0° |

**Scroll** sets the speed and direction of vertical bar scrolling. At the center position (0°), the bars are stationary. Turning the knob clockwise scrolls the bars in one direction; turning it counterclockwise scrolls them in the opposite direction. The further the knob is from center, the faster the scroll.

Internally, the pot value is converted to a signed rate centered at 512. Each frame, this rate is added to a running scroll offset, which shifts the entire vertical phase pattern up or down. The result is smooth, continuous motion.

:::note
When **Sync Field** (Switch 10) is set to On, the scroll offset is reset to zero every frame, freezing the bars in place regardless of the Scroll setting.
:::

---

### Knob 3 — H Freq

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**H Freq** controls the horizontal frequency of an optional second oscillator that adds pixel-by-pixel color variation along each scanline. At 0%, this oscillator is silent (even if enabled). As the value increases, horizontal color ripples appear, and the raster bars take on a two-dimensional, undulating character reminiscent of classic ***plasma*** effects.

H Freq only takes effect when **H Enable** (Switch 8) is turned on. With H Enable off, this knob has no visible effect.

---

### Knob 4 — Video Depth

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Video Depth** controls how strongly the input video's brightness modulates the raster bar output. At 0%, fully counterclockwise, the video input has no effect: the bars display at full palette brightness. As the value increases, the input luma exerts more control. At 100%, the bars are fully modulated by the incoming picture.

In ***Multiply*** mode (Switch 9 set to Multiply), Video Depth controls how much the video darkens the bars: brighter video areas let more bar color through, while darker areas suppress it, like colored glass filtering light. In ***Additive*** mode, Video Depth controls how much bar luma is added on top of the video input, creating a neon glow overlay.

:::tip
With Video Depth at zero, Parallax behaves as a pure color field generator: no video input is needed. This is ideal for standalone pattern synthesis.
:::

---

### Knob 5 — Palette

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

**Palette** selects one of eight curated color palettes. Each palette contains eight colors arranged in a gradient, and the waveform sweeps through them in order. The eight palettes are:

- **0: Rainbow**: Full-spectrum hue cycle from red through violet.
- **1: Copper**: Warm Amiga-inspired gradient from black through amber to bright gold.
- **2: Ocean**: Deep blues and teals fading to white and back.
- **3: Neon**: Synthwave purples, magentas, oranges, and cyan.
- **4: Phosphor**: Terminal greens from black to bright lime.
- **5: Plasma**: Demoscene classic cycling through blue, purple, red, orange, yellow, green, and cyan.
- **6: Sunset**: Warm gradient from dark violets through reds and oranges to white.
- **7: Binary**: Stark two-tone black-and-white alternation.

The palette selector uses 8 stepped detent positions. Each palette's colors are stored as pre-computed YUV constants derived from 9-bit RGB values at synthesis time.

---

### Knob 6 — Waveshape

| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 1 |

**Waveshape** selects the waveform used to sweep through the palette. Four shapes are available, each producing a different character of color transition:

- **0: Ramp** (sawtooth): Colors cycle smoothly in one direction, then abruptly jump back. This creates a sharp boundary at the wrap point.
- **1: Triangle**: Colors sweep up to the palette peak and then reverse, creating a symmetrical, mirror-image pattern.
- **2: Sine Approximation**: Similar to Triangle, but with softened corners that produce rounder, less angular color transitions.
- **3: Square**: Hard two-level switching between the bottom and top halves of the palette. This produces stark, alternating bands with no gradient between them.

The waveshape is applied after the DDS phase accumulator, so it reshapes the same underlying frequency set by **V Freq**.

---

### Switch 7 — Mirror

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mirror** reflects the raster bar pattern from the center of the screen. With Mirror off, bars repeat uniformly from top to bottom. With Mirror on, the pattern folds at the vertical midpoint: bars in the upper half mirror those in the lower half, creating a symmetrical butterfly pattern centered on the screen.

Mirror works by comparing the current scanline to the total line count for the frame. Lines before the midpoint use the normal phase; lines after the midpoint use the inverted phase.

---

### Switch 8 — H Enable

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**H Enable** activates the horizontal oscillator controlled by **H Freq** (Knob 3). With H Enable off, only the vertical DDS drives the palette lookup: each scanline is a single uniform color. With H Enable on, the horizontal DDS adds pixel-by-pixel phase variation to the vertical phase, creating two-dimensional plasma-like color fields that scroll and ripple across both axes.

:::tip
For the classic demoscene plasma look, turn on **H Enable**, set both **V Freq** and **H Freq** to moderate values, choose the **Plasma** palette, and let the pattern scroll. The two orthogonal sine-like oscillators create the characteristic swirling interference pattern.
:::

---

### Switch 9 — Blend Mode

| Property | Value |
|----------|-------|
| Off | Multiply |
| On | Additive |
| Default | Multiply |

**Blend Mode** selects how the raster bar colors interact with the input video signal. With the switch set to **Multiply**, bar brightness is scaled by the video luma: the bars appear to tint the image like a colored filter, and dark areas of the video suppress the bar color. With the switch set to **Additive**, bar luma is added to the video luma (with saturation clamping), and bar chroma is averaged with the video chroma: the bars appear as a luminous neon overlay on top of the picture.

The distinction is most visible when **Video Depth** (Knob 4) is above zero. With Video Depth at zero, multiply mode simply shows bars at full brightness and additive mode shows bars without video contribution.

---

### Switch 10 — Sync Field

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Sync Field** locks the scroll offset to zero on every frame. With Sync Field off, the bars scroll freely at the rate set by **Scroll** (Knob 2): the scroll offset accumulates over time. With Sync Field on, the offset is reset each frame, freezing the bars in place. This is useful when you want a stable, stationary bar pattern that does not drift.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Parallax processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the raster bar composite.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry input signal and the wet processed signal. At 0%, fully down, only the original input is heard. At 100%, fully up, only the raster bar composite is visible. Intermediate values blend the two proportionally using a linear interpolator.

Mix operates independently of **Video Depth**. Video Depth controls how much the input video modulates the bar generation, while Mix controls how much of the final composite appears versus the unprocessed passthrough.

---

## Background

### The Copper and the Demoscene

The Amiga personal computer (1985) contained a coprocessor called the ***Copper***: a simple programmable engine that could change hardware color registers on a per-scanline basis. By cycling through a series of colors as the display raster swept from top to bottom, programmers could fill the screen with smooth rainbow gradients using almost no CPU time. These gradient effects, known as ***copper bars*** or ***raster bars***, became an iconic visual signature of the Amiga demoscene.

Parallax recreates this technique in FPGA hardware, using a DDS phase accumulator instead of a programmable register list. The effect is the same: each scanline selects a color from a palette, and the colors cycle smoothly as the raster position changes.

### Plasma Effects

In the early 1990s, demoscene programmers discovered that combining two or more sine-wave oscillators: one cycling vertically and one cycling horizontally: produced swirling, undulating color fields that seemed to ripple like the surface of a liquid. These were called ***plasma effects***, and they became one of the most recognizable visual signatures of the era.

Parallax's horizontal oscillator recreates this technique. When **H Enable** is on, a second DDS accumulator increments per pixel along each scanline. Its phase is added to the vertical phase before the palette lookup, creating two-dimensional interference patterns. The result is a color field that shifts in both axes simultaneously.

### Direct Digital Synthesis

Both the vertical and horizontal oscillators in Parallax use ***direct digital synthesis*** (DDS), a technique for generating waveforms by incrementing a phase accumulator at a fixed rate. The accumulator wraps around naturally at its bit width, producing a sawtooth wave. Waveshaping (triangle, sine approximation, square) is applied after the accumulator, transforming the raw sawtooth into other waveform shapes.

The key property of DDS is that the output frequency is determined entirely by the increment value. Larger increments mean faster cycling through the palette and thinner bars; smaller increments mean slower cycling and wider bars. Because the accumulator is integer-only, the frequency resolution is inherently quantized: but at 16 bits of accumulator width, the steps are fine enough to be imperceptible.


---

## Signal Flow

### Signal Flow Notes

Two interactions are central to understanding the pipeline:

1. **Phase accumulation is per-axis.** The vertical accumulator increments once per scanline and determines which palette color fills that line. The horizontal accumulator increments once per pixel and, when enabled, adds per-pixel color variation. The two phases are summed before waveshaping, and the combined shaped value's top 3 bits index into the selected palette. This means the palette is always the single source of color: the oscillators only control *where* the palette is sampled.

2. **Video modulation is post-palette, pre-output.** The input video luma is multiplied by Video Depth using a shift-and-add approximation (3-bit precision). In multiply mode, this modulation factor darkens the bar colors proportionally to the input brightness. In additive mode, the modulated luma is added to the bar luma. Both blend modes preserve the bar's chrominance; additive mode additionally averages bar chroma with input chroma.

:::note
The shift-and-add multiply uses only the top 3 bits of the Video Depth and input luma values. This is a hardware-efficient approximation, not a full-precision multiply. At extreme settings, the quantization may produce subtle stepping in the modulation response.
:::


---

## Exercises

These exercises progress from basic raster bars to complex plasma compositions. Each builds on the previous one, engaging more of the synthesis engine.
### Exercise 1: Classic Copper Bars

![Classic Copper Bars result](/img/instruments/videomancer/parallax/parallax_ex1_s1.png)
*Classic Copper Bars — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Recreate the classic Amiga copper bar effect: smoothly scrolling horizontal color bands.

#### Key Concepts

- DDS frequency controls bar density
- Scroll creates vertical motion
- Palette selection defines the color character

#### Steps

1. Set **V Freq** (Knob 1) to about 25%. Wide, clearly visible bands of the default Rainbow palette fill the screen.
2. Turn **Scroll** (Knob 2) gently clockwise from center. The bars begin to drift upward. Turn counterclockwise for downward drift.
3. Switch **Palette** (Knob 5) to step 1: the **Copper** palette. The bars shift to warm amber tones, evoking the original Amiga look.
4. Experiment with **Waveshape** (Knob 6): Triangle produces symmetrical bands; Square produces hard-edged stripes; the Sine approximation softens the triangle's corners.
5. Turn on **Mirror** (Switch 7). The bars reflect from the center, creating a symmetrical butterfly pattern.

#### Settings

| Control | Value |
|---------|-------|
| V Freq | ~25% |
| Scroll | ~55° |
| H Freq | 0% |
| Video Depth | 0% |
| Palette | 1 (Copper) |
| Waveshape | 1 (Triangle) |
| Mirror | Off |
| H Enable | Off |
| Blend Mode | Multiply |
| Sync Field | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Demoscene Plasma

![Demoscene Plasma result](/img/instruments/videomancer/parallax/parallax_ex2_s1.png)
*Demoscene Plasma — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Build a classic demoscene plasma effect: swirling, undulating two-dimensional color fields.

#### Key Concepts

- Horizontal oscillator creates two-dimensional color fields
- The two DDS axes produce interference patterns
- Sine-approximation waveshaping maximizes the "liquid" quality

#### Steps

1. Set **V Freq** (Knob 1) to about 40% and **H Freq** (Knob 3) to about 35%.
2. Turn on **H Enable** (Switch 8) to activate the horizontal oscillator. The uniform horizontal bands instantly transform into a rippling, two-dimensional color field.
3. Switch **Palette** (Knob 5) to step 5: the **Plasma** palette. The classic demoscene color cycle appears.
4. Set **Waveshape** (Knob 6) to step 2: the Sine approximation. The waveform corners soften, and the color transitions become smooth and rounded.
5. Increase **Scroll** (Knob 2) to set the field in motion. The plasma pattern drifts and evolves continuously.
6. Turn on **Mirror** (Switch 7). The rippling pattern reflects symmetrically, creating a kaleidoscopic interference effect.

#### Settings

| Control | Value |
|---------|-------|
| V Freq | ~40% |
| Scroll | ~65° |
| H Freq | ~35% |
| Video Depth | 0% |
| Palette | 5 (Plasma) |
| Waveshape | 2 (Sine Approx) |
| Mirror | On |
| H Enable | On |
| Blend Mode | Multiply |
| Sync Field | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Neon Video Overlay

![Neon Video Overlay result](/img/instruments/videomancer/parallax/parallax_ex3_s1.png)
*Neon Video Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Layer neon-colored raster bars over a live video feed, creating a colorful overlay that responds to the image content.

#### Key Concepts

- Additive blend mode creates luminous overlays
- Video Depth modulates bar brightness with the input picture
- Mix controls the balance between dry input and wet composite

#### Steps

1. Feed a video signal into the input. Set **Bypass** (Switch 11) to On momentarily to confirm the signal is present, then set it back to Off.
2. Set **V Freq** (Knob 1) to about 30% and **Scroll** (Knob 2) slightly off center for gentle drift.
3. Switch **Palette** (Knob 5) to step 3: the **Neon** palette. Bright purples, pinks, oranges, and cyans appear.
4. Set **Blend Mode** (Switch 9) to **Additive**. The bars now layer on top of the video input as colored light rather than replacing it.
5. Increase **Video Depth** (Knob 4) to about 70%. The bar brightness begins to respond to the video content: bright areas of the image intensify the neon bars, creating a luminous halo effect.
6. Pull **Mix** (Fader 12) down to about 70%. Some of the original image bleeds through, softening the effect and creating a richer composite.

#### Settings

| Control | Value |
|---------|-------|
| V Freq | ~30% |
| Scroll | ~10° |
| H Freq | 0% |
| Video Depth | ~70% |
| Palette | 3 (Neon) |
| Waveshape | 0 (Ramp) |
| Mirror | Off |
| H Enable | Off |
| Blend Mode | Additive |
| Sync Field | Off |
| Bypass | Off |
| Mix | ~70% |

---
## Glossary

- **Additive Blending**: A compositing method that sums the brightness values of two layers, producing a luminous overlay where both layers contribute to the output.

- **Copper**: A coprocessor in the Amiga personal computer that could reprogram hardware color registers on a per-scanline basis, enabling smooth color gradient effects with minimal CPU usage.

- **DDS (Direct Digital Synthesis)**: A technique for generating periodic waveforms by incrementing a phase accumulator at a fixed rate; the accumulator value maps to the output waveform amplitude.

- **Multiply Blending**: A compositing method that scales one layer's brightness by another's, producing a colored filter effect where dark areas suppress the overlay.

- **Palette**: A fixed set of colors arranged in a specific order; the oscillator waveform sweeps through the palette to produce the raster bar pattern.

- **Phase Accumulator**: A counter that wraps around at its maximum value, producing a repeating sawtooth wave whose frequency depends on the increment size.

- **Plasma Effect**: A two-dimensional color pattern created by combining orthogonal sine-wave oscillators, producing swirling, interference-like color fields.

- **Raster Bar**: A horizontal band of color that changes per scanline, typically produced by reprogramming color registers during the vertical scan of a CRT display.

- **Waveshaping**: The process of transforming a basic waveform shape (such as a sawtooth) into another shape (triangle, sine, square) through mathematical operations.

- **YUV**: A color encoding system that separates brightness (Y) from color information (U, V); used in video systems to match human visual perception.

---
