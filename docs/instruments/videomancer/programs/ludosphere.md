---
draft: true
sidebar_position: 179
slug: /instruments/videomancer/ludosphere
title: "Ludosphere"
image: /img/instruments/videomancer/ludosphere/ludosphere_hero_s1.png
description: "Take three spinning wheels — one sweeping left to right across the screen, one sweeping top to bottom, and one pulsing forward through time."
---

![Ludosphere hero image](/img/instruments/videomancer/ludosphere/ludosphere_hero_s1.png)
*Ludosphere projecting spherical color patterns across three spatial axes, blending oscillator geometry with input video luminance.*

---

## Overview

Ludosphere is a three-axis oscillator colorizer that sweeps ramp and triangle waveforms through the YUV color space to produce spherical color patterns. Three independent ***direct digital synthesis*** (DDS) phase accumulators operate along the horizontal, vertical, and frame axes, generating luminance and chrominance patterns that can be blended with the input video. The result is a rich palette of interference patterns, animated gradients, and procedural color fields layered onto or driven by whatever signal enters the input.

At its simplest, Ludosphere replaces the input picture with pure oscillator geometry: smooth washes and hard-edged bands that tile across the screen. Blend in the input video's brightness via the three Mod controls, and those geometric patterns begin to react to the source content, bending and warping along the contours of the image. Enable **Colorize** and the program paints new hues onto the picture, turning monochrome footage into kaleidoscopic color.

:::tip
Ludosphere excels at adding color to black-and-white or desaturated sources. Feed it a monochrome camera signal, enable **Colorize**, and explore the Shift fader to sweep through the entire chroma wheel.
:::

### What's In a Name?

The name ***Ludosphere*** fuses the Latin *ludus*: meaning play, game, or sport: with *sphere*. It refers to a playful sphere of color: three oscillator axes carving out a region of YUV color space the way latitude, longitude, and time sweep through a globe. The name also nods to the Dutch historian Johan Huizinga's concept of the ***magic circle***, the boundary within which the rules of play apply. Inside Ludosphere's magic circle, the ordinary rules of color are suspended.

---

## Quick Start

1. Turn all three **Clock** knobs (Knobs 1–3) to roughly 60%. Vertical bands, horizontal bands, and a slow animation appear on screen, superimposed on the input.
2. Enable **Colorize** (Switch 10). The grayscale pattern explodes into color: the V and F oscillators now drive the U and V chroma channels directly.
3. Slowly sweep **Shift** (Fader 12) from end to end. The entire color palette rotates through the chroma wheel, shifting hues smoothly.
4. Turn **H Mod** (Knob 4) fully clockwise. The horizontal oscillator pattern now bends with the brightness of the input video: bright areas push the pattern one way, dark areas pull it the other.

---

## Parameters

![Videomancer front panel with Ludosphere loaded](/img/instruments/videomancer/ludosphere/ludosphere_control_panel.png)
*Videomancer's front panel with Ludosphere active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — H Clock

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**H Clock** sets the frequency of the horizontal oscillator. This oscillator accumulates phase once per pixel, so it produces vertical bands on screen. At 0%, fully counterclockwise, the oscillator is nearly static: a single uniform wash spans the entire width of the picture. As the value increases, more cycles of the waveform fit within each scan line, and the vertical bands multiply and become narrower. At 100%, fully clockwise, the bands are at their highest spatial frequency.

Because the oscillator is a ***phase accumulator***, the number of bands on screen is not always a whole number. At certain knob positions the pattern tiles perfectly; at others, the last band on the right edge is truncated, producing a visible seam. This is normal DDS behavior.

---

### Knob 2 — V Clock

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**V Clock** sets the frequency of the vertical oscillator. This oscillator accumulates phase once per scan line, so it produces horizontal bands on screen. At 0%, a single wash stretches from the top to the bottom of the picture. As the value increases, horizontal bands multiply and grow thinner. At 100%, the bands are at their highest vertical frequency.

**V Clock** and **H Clock** interact to create a grid of color cells. When both are set to similar values, the cells are roughly square. Unequal values produce tall or wide rectangles.

---

### Knob 3 — F Clock

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**F Clock** sets the frequency of the frame oscillator. Unlike the horizontal and vertical oscillators, this one accumulates phase once per video frame, creating patterns that evolve over time rather than across the screen. At 0%, the oscillation is extremely slow: barely perceptible. As the value increases, the animation speeds up. At high values the pattern cycles rapidly, producing a flickering or pulsing effect.

:::note
The frame oscillator is free-running: it does not reset at the start of each frame. This means its phase drifts continuously, creating organic motion rather than a locked loop.
:::

---

### Knob 4 — H Mod

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**H Mod** controls how much the input video's luminance modulates the horizontal oscillator output. At 0%, the horizontal oscillator produces a pure, unmodulated pattern: a clean ramp or triangle independent of the input image. As the value increases, the input brightness is blended additively with the oscillator waveform: bright areas of the input push the oscillator value higher, dark areas pull it lower. At 100%, the modulation is at full strength and the oscillator pattern strongly tracks the contours of the source image.

Because H Mod drives the Y (luminance) output channel, turning it up makes the input picture visible through the oscillator pattern.

---

### Knob 5 — V Mod

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**V Mod** controls how much the input video's luminance modulates the vertical oscillator output. The behavior mirrors **H Mod**, but the vertical oscillator feeds the U (blue-difference) chroma channel when **Colorize** is enabled. At 0%, the vertical oscillator runs independently. At higher values, input brightness reshapes the vertical color pattern.

:::tip
With **Colorize** enabled, **V Mod** determines how strongly the source image's brightness drives the blue-yellow axis of the output color. High values create a color pattern that follows the contours of the input.
:::

---

### Knob 6 — F Mod

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**F Mod** controls how much the input video's luminance modulates the frame oscillator output. The frame oscillator feeds the V (red-difference) chroma channel when **Colorize** is enabled. At 0%, the frame oscillator produces a pure animation unrelated to the input. At higher values, the source brightness is blended in, causing the animated color to track the image content.

---

### Switch 7 — H Flip

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**H Flip** selects the waveform shape of the horizontal oscillator. With the switch set to **Off**, the oscillator outputs a ***sawtooth*** (ramp) waveform: a smooth rise from black to white followed by an abrupt reset. With the switch set to **On**, the waveform is converted to a ***triangle*** by folding the ramp at its midpoint: values below center are scaled upward, values above center are mirrored back down. The triangle waveform is symmetrical and produces softer, more rounded visual patterns than the hard-edged sawtooth.

---

### Switch 8 — V Flip

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**V Flip** selects the waveform shape of the vertical oscillator. **Off** produces a sawtooth; **On** produces a triangle. The effect is the same transformation described for **H Flip**, applied to the vertical axis. Sawtooth produces sharp horizontal edges at each cycle boundary; triangle produces smooth peaks and valleys.

---

### Switch 9 — F Flip

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**F Flip** selects the waveform shape of the frame oscillator. **Off** produces a sawtooth; **On** produces a triangle. With a sawtooth, the animated color ramps up and then snaps back. With a triangle, the color fades up and then fades back down symmetrically, creating a gentler pulsation.

---

### Switch 10 — Colorize

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Colorize** controls whether the oscillators replace the input's chroma channels. With the switch set to **Off**, the input U and V chroma channels pass through unchanged: only the Y (luminance) channel is affected by the horizontal oscillator. With the switch set to **On**, the vertical oscillator output (plus the **Shift** offset) replaces the U channel, and the frame oscillator output (plus the **Shift** offset) replaces the V channel. This injects entirely new color into the image.

:::tip
***Colorize is the gateway to Ludosphere's full color palette.*** Without it, only the luminance channel is processed. Enable it and the program becomes a complete YUV color synthesizer layered on top of the input signal.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Ludosphere processing. Sync timing is unaffected, so there is no glitch when toggling. Use **Bypass** for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Shift

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Shift** applies a global offset to the U and V chroma channels. The offset is added as a signed value centered at the midpoint: at 50% there is no shift. Moving the fader below 50% rotates chroma in one direction; moving above 50% rotates it in the other. Because the addition wraps around rather than clamping, **Shift** smoothly rotates the entire color palette through the chroma wheel.

**Shift** only affects the output when **Colorize** is enabled. Without Colorize, the chroma channels pass through from the input and the shift has no visible effect.

:::note
Because Shift uses wrapping arithmetic, sweeping the fader from one end to the other cycles through all possible hue offsets with no discontinuity (the colors loop seamlessly.)
:::

---

## Background

### Direct digital synthesis

The core of Ludosphere is three ***direct digital synthesis*** (DDS) phase accumulators. A DDS oscillator works by adding a fixed number: the ***frequency word***: to an accumulator register on every clock tick. When the accumulator overflows, it wraps around and the cycle begins again. The upper bits of the accumulator form a sawtooth ramp whose frequency is proportional to the frequency word.

In Ludosphere, the three accumulators tick at different rates. The horizontal accumulator advances once per pixel, so its pattern repeats within a single scan line. The vertical accumulator advances once per line, so its pattern repeats within a single field. The frame accumulator advances once per frame, producing motion that evolves over time.

### Waveshaping

Each oscillator passes through a ***frequency doubler*** module that can convert the sawtooth ramp into a triangle wave. The conversion works by folding the waveform at its midpoint: values in the lower half are scaled up by two, and values in the upper half are mirrored and scaled. The result is a symmetrical triangle that rises to a peak at the center value and then descends back to zero.

The Flip toggles bypass or engage this fold. In sawtooth mode, the oscillator produces hard edges at every cycle boundary where the ramp resets. In triangle mode, those edges disappear, replaced by smooth peaks and valleys. This distinction becomes very visible at lower frequencies where individual cycles span large regions of the screen.

### Luma modulation

After waveshaping, each oscillator is mixed with the input luminance through a ***proc amp*** (processing amplifier) stage. The proc amp computes:

$$\text{result} = (\text{input luma} - 0.5) \times \text{mod depth} + \text{oscillator}$$

When the mod depth is zero, the input luma term vanishes and the result is the pure oscillator waveform. As the mod depth increases, the input brightness is blended in: bright parts of the image push the oscillator output higher, dark parts pull it lower. At full mod depth the input picture is strongly visible through the oscillator geometry.


---

## Signal Flow

### Signal Flow Notes

The key architectural detail is how the three oscillator axes map to the three YUV channels. The horizontal oscillator exclusively drives the Y (luminance) output: this makes the most visually prominent oscillator the one that creates vertical banding. The vertical oscillator drives U (blue-difference chroma), and the frame oscillator drives V (red-difference chroma). This asymmetry means the spatial oscillators control color hue while the temporal oscillator controls color saturation along a different chroma axis. Together, the three axes trace a path through YUV color space that resembles motion across the surface of a sphere: hence the name.

The **Shift** fader applies a uniform offset to both U and V outputs simultaneously. Because it uses wrapping addition (no clamping), it acts as a hue rotation control that shifts the entire chroma palette in one smooth motion. This global shift interacts with the V and F oscillators multiplicatively: the oscillators create the color pattern, and Shift rotates the whole pattern through the color wheel.

:::tip
**Mapping summary**: H oscillator → Y (brightness pattern), V oscillator → U (blue-yellow color), F oscillator → V (red-cyan color). Keeping this mapping in mind helps predict what each knob will do.
:::


---

## Exercises

These exercises progress from pure oscillator geometry to full video colorization, gradually introducing modulation and chroma controls.
### Exercise 1: Oscillator Grid

![Oscillator Grid result](/img/instruments/videomancer/ludosphere/ludosphere_ex1_s1.png)
*Oscillator Grid — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A static grid of geometric bands, transitioning from hard-edged sawtooth stripes to soft triangular waves.

#### Key Concepts

- DDS phase accumulators create tiling ramp patterns
- Horizontal oscillator tiles per pixel; vertical oscillator tiles per line
- Flip converts sawtooth edges to smooth triangle peaks

#### Video Source

Any video source: a camera feed, color bars, or a test pattern. The input will be mostly hidden behind the oscillator pattern.

#### Steps

1. Turn **H Clock** (Knob 1) to about 60%. Vertical bands of varying brightness appear across the screen.
2. Turn **V Clock** (Knob 2) to about 60%. Horizontal bands appear, crossing the vertical ones to form a checkerboard-like grid.
3. Leave **F Clock** (Knob 3) at 0% and all three **Mod** knobs at 0%. The pattern should be purely geometric and static.
4. Toggle **H Flip** (Switch 7) on. The vertical bands change from hard-edged sawtooth ramps to smooth triangles. The visual texture softens noticeably.
5. Toggle **V Flip** (Switch 8) on. The horizontal bands also become triangular. The grid now has rounded diamond-shaped cells.

#### Settings

| Control | Value |
|---------|-------|
| H Clock | 60% |
| V Clock | 60% |
| F Clock | 0% |
| H Mod | 0% |
| V Mod | 0% |
| F Mod | 0% |
| H Flip | On |
| V Flip | On |
| F Flip | Off |
| Colorize | Off |
| Bypass | Off |
| Shift | 50% |

---

### Exercise 2: Animated Colorizer

![Animated Colorizer result](/img/instruments/videomancer/ludosphere/ludosphere_ex2_s1.png)
*Animated Colorizer — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A slowly pulsating color wash that paints the input video in cycling hues.

#### Key Concepts

- The frame oscillator creates temporal animation
- Colorize maps oscillators to the U and V chroma channels
- Shift rotates the entire chroma palette

#### Video Source

A live camera feed or black-and-white footage. Desaturated or monochrome material works especially well because the color is entirely generated by the oscillators.

#### Steps

1. Set **H Clock** (Knob 1) to about 40% and **V Clock** (Knob 2) to about 40%, creating a moderate grid in the luminance channel.
2. Set **F Clock** (Knob 3) to about 30%. A slow animation begins: because F Clock drives the V chroma channel (via the output mux), the color will cycle once Colorize is enabled.
3. Enable **Colorize** (Switch 10). The screen fills with color. The horizontal and vertical patterns define the luminance structure, while the frame oscillator creates a pulsing color shift.
4. Slowly sweep **Shift** (Fader 12) from one end to the other. The entire color palette rotates: reds become greens become blues and back again, smoothly and without discontinuity.
5. Toggle **F Flip** (Switch 9) on. The pulsation changes from a sharp sawtooth ramp-and-snap to a symmetrical fade-up-then-fade-down (a gentler, breathing rhythm.)

#### Settings

| Control | Value |
|---------|-------|
| H Clock | 40% |
| V Clock | 40% |
| F Clock | 30% |
| H Mod | 0% |
| V Mod | 0% |
| F Mod | 0% |
| H Flip | Off |
| V Flip | Off |
| F Flip | On |
| Colorize | On |
| Bypass | Off |
| Shift | 50% |

---

### Exercise 3: Video-Reactive Color Sculpting

![Video-Reactive Color Sculpting result](/img/instruments/videomancer/ludosphere/ludosphere_ex3_s1.png)
*Video-Reactive Color Sculpting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A fully modulated color field where the oscillator geometry bends and warps along the contours of the source image, painting the video in reactive, shifting hues.

#### Key Concepts

- Luma modulation blends input brightness into the oscillator pattern
- All three axes can respond to source content simultaneously
- Colorize + modulation = input-reactive color synthesis

#### Video Source

High-contrast footage: faces, architectural scenes, or anything with strong brightness gradients. The richer the tonal range, the more the modulation has to work with.

#### Steps

1. Start with the Exercise 2 settings (**H Clock** 40%, **V Clock** 40%, **F Clock** 30%, **Colorize** on, **F Flip** on).
2. Turn **H Mod** (Knob 4) to about 70%. The luminance pattern begins tracking the input: bright areas of the source push the oscillator higher, dark areas pull it lower. The geometric grid warps to follow the image content.
3. Turn **V Mod** (Knob 5) to about 70%. The chroma U channel now also follows the source brightness. Colors begin to cluster along the edges and contours of the input picture.
4. Turn **F Mod** (Knob 6) to about 50%. The animated color pulsation is now modulated by brightness: bright regions pulse at full amplitude while dark regions remain more subdued.
5. Sweep **Shift** (Fader 12) to find a hue that complements your source material. The entire color map rotates while preserving the modulated structure.
6. Flip all three **Flip** switches on. The waveforms change from sawtooth to triangle. The pattern softens: edges become gradients, and the color transitions become smoother.
7. Use **Bypass** (Switch 11) to compare the processed and unprocessed images.

#### Settings

| Control | Value |
|---------|-------|
| H Clock | 40% |
| V Clock | 40% |
| F Clock | 30% |
| H Mod | 70% |
| V Mod | 70% |
| F Mod | 50% |
| H Flip | On |
| V Flip | On |
| F Flip | On |
| Colorize | On |
| Bypass | Off |
| Shift | 50% |

---
## Glossary

- **Chroma**: The color information in a video signal, encoded as U (blue-difference) and V (red-difference) components in YUV color space.

- **DDS (Direct Digital Synthesis)**: A method of generating waveforms by incrementing a phase accumulator at a fixed rate; the accumulator's overflow creates a repeating ramp whose frequency is determined by the increment size.

- **Frequency Doubler**: A waveshaping module that folds a ramp waveform at its midpoint, converting a sawtooth into a symmetrical triangle and doubling its apparent frequency.

- **Frequency Word**: The fixed increment added to a DDS phase accumulator on each clock tick; larger values produce higher frequencies.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Phase Accumulator**: A register that wraps around on overflow, producing a periodic ramp signal whose period depends on the increment value.

- **Proc Amp**: Processing Amplifier; a gain-and-offset stage that applies contrast (multiplication) and brightness (offset) adjustments to a signal.

- **Sawtooth**: A waveform that rises linearly from minimum to maximum and then resets abruptly, producing a ramp with a hard edge at each cycle boundary.

- **Triangle**: A waveform that rises linearly to a peak and then falls linearly back to the minimum, producing smooth, symmetrical peaks and valleys.

- **Wrapping Addition**: Arithmetic that allows values to overflow and wrap around to zero rather than clamping at the maximum, producing seamless cyclic behavior.

- **YUV**: A color space that separates luminance (Y) from chrominance (U, V), allowing independent manipulation of brightness and color.

---
