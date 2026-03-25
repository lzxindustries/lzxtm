---
draft: true
sidebar_position: 297
slug: /instruments/videomancer/tarmac
title: "Tarmac"
image: /img/instruments/videomancer/tarmac/tarmac_hero.png
description: "The Super Nintendo's Mode 7 background layer was a hardware trick that changed everything."
---

![Tarmac hero image](/img/instruments/videomancer/tarmac/tarmac_hero_s1.png)
*A floor of pixelated video tiles spirals away into infinity, rotating and pulsing with a retro console ground-plane perspective*

---

## Overview

**Tarmac** recreates the SNES PPU ***Mode 7*** affine transform inside the FPGA, capturing your input video into a sixty-four-by-sixty-four tile buffer and playing it back through a rotating, zooming, tiling matrix. The captured image repeats infinitely in every direction like a seamless wallpaper: rotate it and the tiled pattern spirals hypnotically; zoom in and individual pixels bloom into blocky mosaics; zoom out and the repeating grid shrinks toward a vanishing point. Two DDS oscillators animate the rotation angle and scale independently, creating endlessly evolving motion from a still input.

The effect is deliberately lo-fi: downsampling the input to sixty-four pixels on a side produces the characteristically chunky look of 16-bit console pseudo-3D. Combined with the Mix fader, Tarmac can overlay its transformed texture on the dry input, creating double-exposure composites where the original image floats beneath its own spinning, zoomed reflection.

### What's In a Name?

***Tarmac*** is the paved surface of a road or runway: the ground beneath your wheels. The name evokes the racing-game ground planes of *F-Zero* and *Super Mario Kart*, where SNES Mode 7 transformed flat textures into convincing pseudo-3D surfaces that rushed toward the horizon. In Videomancer, the highway is whatever video signal you feed in.

---

## Quick Start

1. Patch a video source: camera, pattern generator, or media player: into the Videomancer input. Without input the tile buffer captures only black.
2. Set **Bypass** to Off and push **Mix** fully clockwise. You'll see a coarse, pixelated version of your input tiled across the screen.
3. Turn **Rot Speed** a few clicks clockwise. The tiled image begins spinning smoothly, repeating in every direction.
4. Increase **Base Scale** to zoom in on the tile pattern, or decrease it to shrink the tiles and reveal more repetitions.

---

## Parameters

![Videomancer front panel with Tarmac loaded](/img/instruments/videomancer/tarmac/tarmac_control_panel.png)
*Videomancer's front panel with Tarmac active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Rot Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Rot Speed** controls how quickly the affine-transformed image rotates, measured in phase-accumulator increments per frame. At zero the image is stationary. Turning clockwise increases the rotational velocity: the tiled video spins faster and faster until tiny adjustments create rapid whirling. The rotation advances smoothly via a sixteen-bit DDS accumulator, so even at low values the motion is continuous and jitter-free.

:::tip
Very small values of **Rot Speed** (just a few clicks off zero) produce a slow, meditative spin that's ideal for ambient performance backdrops.
:::

---

### Knob 2 — Zoom Depth

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Zoom Depth** sets the amplitude of the scale oscillation. At zero the zoom level stays fixed at whatever **Base Scale** is set to. Turning clockwise makes the image pulse in and out: the tiles grow and shrink rhythmically as a sine wave modulates the scale coefficient. Higher values produce more dramatic zoom pulsing, while moderate settings add subtle breathing to the rotation.

---

### Knob 3 — Perspective

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Perspective** is mapped in the parameter configuration but has no visible effect in the current FPGA implementation. The control is reserved for a future update that would add per-scanline scale modulation for pseudo-3D ground-plane effects.

---

### Knob 4 — Base Scale

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Base Scale** sets the overall zoom level of the affine transform. At the lowest values the captured image is zoomed in tightly, revealing individual pixels as large squares. At the midpoint the tile roughly fills the screen at one-to-one mapping. Turning further increases the zoom-out level, shrinking each tile repetition and revealing more of the infinite tiled grid. The minimum scale is clamped so the image never collapses to a single pixel.

---

### Knob 5 — Zoom Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Zoom Speed** controls the oscillation rate of the scale animation. At zero the zoom depth (if any) is frozen at its initial phase. Turning clockwise speeds up the sine-wave modulation that drives the zoom pulsing, creating faster in-and-out breathing. Combined with rotation, this produces a spiraling, pulsating tunnel effect.

---

### Knob 6 — Center Y

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Center Y** positions the vertical center of rotation. At the midpoint the rotation axis is centered vertically on screen. Turning the knob moves the center up or down, causing the image to orbit around an off-center point. This shifts the visual balance of the spinning tiles: low center values pull the vortex toward the top of the frame, and high values push it toward the bottom.

---

### Switch 7 — Rot Dir

| Property | Value |
|----------|-------|
| Off | CW |
| On | CCW |
| Default | CW |

**Rot Dir** selects the rotation direction. At CW the image rotates clockwise; at CCW it rotates counterclockwise. Flipping this toggle mid-performance reverses the spinning instantly, creating a satisfying visual snap as the tile pattern switches direction.

---

### Switch 8 — Shear

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Shear** is mapped in the parameter configuration but has no visible effect in the current FPGA implementation. The control is reserved for a future update that would add a horizontal shearing component to the affine matrix.

---

### Switch 9 — Wrap Mode

| Property | Value |
|----------|-------|
| Off | Wrap |
| On | Clamp |
| Default | Wrap |

**Wrap Mode** is mapped in the parameter configuration but has no visible effect in the current FPGA implementation. The tile buffer always wraps via natural 6-bit address truncation: coordinates modulo sixty-four: so the tiled pattern repeats infinitely in every direction.

---

### Switch 10 — Persp Hold

| Property | Value |
|----------|-------|
| Off | Center |
| On | Bottom |
| Default | Center |

**Persp Hold** is mapped in the parameter configuration but has no visible effect in the current FPGA implementation. The control is reserved for a future update that would shift the perspective reference point between center and bottom screen positions.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** switches the output between the processed effect and the unmodified input. When On, the input signal passes through unchanged regardless of the Mix position.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 100 |

**Mix** crossfades between the dry input and the affine-transformed output. At minimum you see only the input; at maximum you see only the rotated, zoomed tile pattern. Intermediate positions create a double-exposure composite where the original video shows through the spinning tiles.

---

## Background

### SNES Mode 7

The Super Nintendo Entertainment System's PPU (Picture Processing Unit) included a hardware mode called ***Mode 7*** that applied a 2×2 affine transformation matrix to a background layer. By rotating and scaling a flat texture plane and varying the scale per scanline, games like *F-Zero*, *Super Mario Kart*, and *Pilotwings* created the illusion of three-dimensional ground planes rushing toward the player. Tarmac recreates this transformation in Videomancer's iCE40 FPGA, applying the same mathematics to live video captured into a tile buffer.

### The Affine Transform

The core of the effect is a standard 2D affine matrix:

```
tx = M7A × (sx − cx) + M7B × (sy − cy) + cx
ty = M7C × (sx − cx) + M7D × (sy − cy) + cy
```

Where `M7A = cos(θ) × scale`, `M7B = sin(θ) × scale`, `M7C = −sin(θ) × scale`, `M7D = cos(θ) × scale`, and `(cx, cy)` is the rotation center. For efficiency, the per-pixel computation reduces to two additions: after computing the start coordinates for each scanline, the transform walks across pixels by simply adding M7A to tx and M7C to ty (avoiding per-pixel multiplication entirely.)

### Quarter-Wave Sine LUT

A sixty-four-entry quarter-wave sine lookup table provides the cosine and sine values for the rotation matrix. The full 360-degree range is reconstructed using quadrant folding: the table stores only the first quadrant (0°–90°), and the lookup function flips and negates the index and result for the remaining three quadrants. Cosine is computed as sine of the phase plus 256 (a quarter-cycle offset). This compact approach requires just sixty-four ten-bit entries: small enough to infer into FPGA logic without a dedicated BRAM block.

### Tile Buffer Capture

The input video is downsampled into a sixty-four-by-sixty-four tile buffer by skipping pixels horizontally (every ~30th pixel) and lines vertically (every ~16th line). The buffer stores thirty bits per entry (ten bits each for Y, U, and V), requiring approximately four BRAM tiles. Because the capture rate is much lower than the pixel clock, the buffer represents a coarse snapshot of the input: fine detail is lost, replaced by the chunky pixel-art aesthetic characteristic of Mode 7 rendering.


---

## Signal Flow

### Signal Flow Notes

The system operates on two timescales. Per-frame processing (at vsync) advances the DDS accumulators for rotation and zoom, looks up sine and cosine values, and computes the four matrix coefficients. Per-pixel processing (at the full pixel clock) initializes the affine walk at the start of each scanline and then increments the texture coordinates by the column deltas M7A and M7C for every active pixel: reducing the transform to just two additions per pixel after the row setup.

The tile buffer is written during active video by downsampling the input and read during the next frame's display by using the affine-transformed coordinates as the buffer address. Because the buffer address is naturally truncated to six bits (modulo 64), the tile pattern repeats infinitely in every direction without explicit wrap logic.


---

## Exercises

Below are three exercises exploring Tarmac's affine transform capabilities. Patch a video source into the input before beginning (without input the tile buffer captures only black.)
### Exercise 1: Spinning Gallery

![Spinning Gallery result](/img/instruments/videomancer/tarmac/tarmac_ex1_s1.png)
*Spinning Gallery — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A slowly spinning mosaic of your input video, tiled across the screen in an endless rotating lattice.

#### Key Concepts

Basic rotation, tile repetition, DDS-based animation

#### Steps

1. Patch a camera or media player into the input. Dial in the settings below.
2. You should see a coarse, pixelated version of your input tiled across the screen and slowly rotating.
3. Increase **Rot Speed** slightly: watch the rotation pick up speed. Each tile of your input image spins in unison, creating a kaleidoscopic pattern.
4. Adjust **Base Scale** to zoom in (see fewer, larger tiles) or zoom out (see many tiny repetitions of the captured texture).
5. Try **Rot Dir** at CCW, then flip back to CW (the image snaps to the opposite spin direction.)

#### Settings

| Control | Value |
|---------|-------|
| Rot Speed | 15% |
| Zoom Depth | 0% |
| Perspective | 0% |
| Base Scale | 50% |
| Zoom Speed | 0% |
| Center Y | 50% |
| Rot Dir | CW |
| Shear | Off |
| Wrap Mode | Wrap |
| Persp Hold | Center |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Breathing Zoom

![Breathing Zoom result](/img/instruments/videomancer/tarmac/tarmac_ex2_s1.png)
*Breathing Zoom — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A pulsing, breathing rotation where the tile pattern expands and contracts rhythmically while spinning.

#### Key Concepts

Scale oscillation, zoom pulsing, combined rotation and zoom

#### Steps

1. Start from the settings below (moderate rotation with zoom pulsing enabled.)
2. Watch the tile pattern: it should be spinning slowly while simultaneously expanding and contracting in a smooth sine wave.
3. Increase **Zoom Depth** to exaggerate the pulsing. At high values the tiles grow very large at the peak, then shrink to reveal many repetitions at the trough.
4. Adjust **Zoom Speed** to change the breathing rate. Faster speeds create a frantic pumping; slower speeds produce a gentle, hypnotic swell.
5. Set **Mix** to about 70% to see the dry input showing through the pulsing tiles (a layered double-exposure effect.)

#### Settings

| Control | Value |
|---------|-------|
| Rot Speed | 10% |
| Zoom Depth | 40% |
| Perspective | 0% |
| Base Scale | 50% |
| Zoom Speed | 20% |
| Center Y | 50% |
| Rot Dir | CW |
| Shear | Off |
| Wrap Mode | Wrap |
| Persp Hold | Center |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Vortex Tunnel

![Vortex Tunnel result](/img/instruments/videomancer/tarmac/tarmac_ex3_s1.png)
*Vortex Tunnel — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A spiraling tunnel effect where the rotation center is offset and fast zoom pulsing creates the illusion of zooming into an infinite fractal of your own video.

#### Key Concepts

Off-center rotation, rapid zoom, psychedelic compositing

#### Steps

1. Dial in the settings below. The rotation center is pulled toward the top of the frame.
2. Notice how the spinning pattern orbits around the off-center point, creating an asymmetric spiral.
3. Push **Rot Speed** higher: the vortex accelerates. The tiled input becomes a blur of repeating textures.
4. Set **Mix** to 50%. The dry input shows through the middle of the spiral, creating a portal-like composite.
5. Try feeding a high-contrast source (bold graphics or stark lighting) to maximize the visual impact of the tiled repetition.

#### Settings

| Control | Value |
|---------|-------|
| Rot Speed | 40% |
| Zoom Depth | 50% |
| Perspective | 0% |
| Base Scale | 40% |
| Zoom Speed | 30% |
| Center Y | 25% |
| Rot Dir | CCW |
| Shear | Off |
| Wrap Mode | Wrap |
| Persp Hold | Center |
| Bypass | Off |
| Mix | 80% |

---
## Glossary

- **Affine transform**: A geometric transformation that preserves parallel lines: rotation, scaling, shearing, and translation applied via a 2×2 matrix plus a translation vector.

- **DDS**: Direct digital synthesis: a phase-accumulator technique that produces smooth periodic motion from a counter that wraps at a configurable rate.

- **Downsampling**: Reducing the resolution of a signal by taking every Nth sample, here capturing every ~30th pixel and every ~16th line to fill the 64×64 tile buffer.

- **Fixed-point arithmetic**: Numbers stored as integers with an implicit fractional part: here the affine accumulators use 12.10 format (twelve integer bits, ten fractional bits).

- **Mode 7**: A video mode on the Super Nintendo that applied a per-scanline affine transform to a background layer, enabling pseudo-3D effects in games like *F-Zero* and *Super Mario Kart*.

- **Phase accumulator**: A counter that wraps at its maximum value, producing a sawtooth ramp whose frequency is set by the increment per step (the core of DDS.)

- **Quarter-wave LUT**: A lookup table storing only the first 90° of a sine wave; the remaining 270° are reconstructed by folding and negating, reducing storage by 75%.

- **Tile buffer**: The 64×64 pixel memory that stores a downsampled snapshot of the input video; readings beyond the buffer size wrap modulo 64, creating seamless infinite tiling.

---
