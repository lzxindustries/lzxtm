---
draft: true
sidebar_position: 195
slug: /instruments/videomancer/perlin
title: "Perlin"
image: /img/instruments/videomancer/perlin/perlin_hero.png
---

import perlin_animation from '/img/instruments/videomancer/perlin/perlin_animation.gif';
import perlin_control_panel from '/img/instruments/videomancer/perlin/perlin_control_panel.png';
import perlin_exercise1_result from '/img/instruments/videomancer/perlin/perlin_exercise1_result.gif';
import perlin_exercise2_result from '/img/instruments/videomancer/perlin/perlin_exercise2_result.gif';
import perlin_exercise3_result from '/img/instruments/videomancer/perlin/perlin_exercise3_result.gif';
import perlin_hero from '/img/instruments/videomancer/perlin/perlin_hero.png';

# Perlin

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={perlin_hero} alt="Perlin hero image"/>
*Perlin generating animated gradient noise fields with fire palette and turbulent absolute-value folding, a fractal texture born from integer arithmetic alone.*
<img src={perlin_animation} alt="Perlin animated output"/>
*Perlin output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1983, Ken Perlin invented a noise function to add naturalistic texture to computer-generated imagery for the film *Tron*. The key insight was that smooth, continuous randomness — unlike the white-noise static of a detuned television — could simulate clouds, marble, terrain, fire, and water. Perlin noise has since become one of the most widely used algorithms in computer graphics. This program implements a real-time FPGA-native approximation of Perlin's gradient noise, generating animated 2D noise textures at video rate.

The screen is divided into a grid of cells whose size is selectable from 8 to 128 pixels. At each grid vertex, a pseudo-random gradient direction is selected from 8 compass points using an LFSR-style hash function — no BRAM is needed for the permutation table. For each pixel, four gradient dot products are computed (one per cell corner) and smoothly interpolated using a piecewise-linear approximation of the quintic smoothstep curve. The result is a single octave of smooth gradient noise. The noise value is then mapped through one of four color palettes — Marble (grayscale), Cloud (blue-white), Terrain (green-brown), and Fire (red-yellow-black) — with optional contrast scaling and palette cycling.

A DDS (direct digital synthesis) scroll engine animates the noise field by adding per-frame offsets to the pixel coordinates, with direction selectable in four quadrants. Video modulation mode multiplies the noise luma with the input video luminance, creating content-dependent textures. Absolute-value mode folds the signed noise into ridge-like patterns, and domain warping feeds the previous frame's noise back into the coordinate lookup for turbulent distortion.

---

## Background

### Gradient Noise

Unlike value noise (which assigns random values to grid points and interpolates between them), gradient noise assigns random *gradient vectors* to grid points and computes the dot product between each gradient and the displacement vector from the grid point to the current pixel. The result is a function that is exactly zero at every grid vertex and varies smoothly between them. This produces smoother, more isotropic textures than value noise. Perlin's program quantises the gradient directions to 8 compass points — N, NE, E, SE, S, SW, W, NW — and approximates the dot product using shift-and-add arithmetic, avoiding hardware multipliers.

### The Hash Function

Classical Perlin noise uses a pre-computed 256-entry permutation table to assign pseudo-random gradient indices to grid vertices. Storing 256 bytes would require BRAM on the iCE40, so this implementation replaces the table with a combinational LFSR-style hash: XOR the x and y cell coordinates with rotated and shifted copies of themselves, then take the lowest 3 bits as the gradient index. The resulting noise is not identical to Perlin's original, but it is visually smooth and sufficiently random for real-time video synthesis.

### Smoothstep Interpolation

Raw bilinear interpolation between the four dot products would produce visible grid artifacts — straight-line transitions along cell boundaries. Perlin's original algorithm uses a cubic Hermite interpolant; the improved version uses a quintic polynomial $6t^5 - 15t^4 + 10t^3$. This program approximates the quintic with a piecewise-linear S-curve: for the lower half of the fractional range, the curve is steepened via `t - (t >> 2)`; the upper half is obtained by mirroring. The result eliminates first-derivative discontinuities at cell boundaries, producing seamlessly flowing textures.

### Scroll Animation via DDS

The noise field is animated by adding a 16-bit phase accumulator offset to the pixel coordinates each frame. The scroll speed pot sets the accumulator increment, and the direction pot selects one of four quadrants (right, down, left, up). Because the noise function is continuous and tileable (grid vertices wrap via modular arithmetic), scrolling produces an endlessly flowing texture with no visible seams.

### Color Palettes

Four palettes map the noise value through different YUV color schemes. **Marble** is grayscale — neutral U/V at 512 with luma tracking the noise index. **Cloud** adds a subtle blue bias (U=560, V=490). **Terrain** splits at the midpoint — values below 128 get green tones (U=470, V=440) and above 128 get brown (U=490, V=560). **Fire** has a black floor for low noise values, then ramps luma with warm chroma (U=440, V=600). The palette offset is cycled each frame by adding a portion of the Palette Cycle pot, creating animated color flow independent of the noise field geometry.


---

## Signal Flow

```
Parameter Registers
│
├── Scroll Speed → DDS increment (16-bit phase accumulator)
├── Direction → quadrant select (R/D/L/U)
├── Scale → cell_shift (3..7, cell sizes 8..128 px)
├── Turbulence → 2nd-octave amplitude (declared, used for future fBm)
├── Contrast → output luma gain
├── Palette Cycle → palette offset increment per frame
│
├── Processing Pipeline (per pixel, 4 stages) ──────────────────
│   │
│   ├─ Stage 1: Coordinate + Grid Cell (1 clk)
│   │   ├─ px = hcount + x_offset[15:4]
│   │   ├─ py = vcount + y_offset[15:4]
│   │   ├─ Domain warp: add previous noise to coords
│   │   ├─ cell_x/y = px >> cell_shift (integer cell)
│   │   └─ frac_x/y = px[low bits] (8-bit fractional)
│   │
│   ├─ Stage 2: Hash + Gradient Select (1 clk)
│   │   ├─ perlin_hash(cell_x, cell_y) → hash_00
│   │   ├─ perlin_hash(cell_x+1, cell_y) → hash_10
│   │   ├─ perlin_hash(cell_x, cell_y+1) → hash_01
│   │   └─ perlin_hash(cell_x+1, cell_y+1) → hash_11
│   │
│   ├─ Stage 3: Dot Products + Interpolation (1 clk)
│   │   ├─ 4× grad_dot(hash, frac) → dot00..dot11
│   │   ├─ smoothstep(frac_x) → sx, smoothstep(frac_y) → sy
│   │   ├─ slerp(dot00, dot10, sx) → lerp_top
│   │   ├─ slerp(dot01, dot11, sx) → lerp_bot
│   │   └─ slerp(lerp_top, lerp_bot, sy) → noise
│   │
│   └─ Stage 4: Palette + Output (1 clk)
│       ├─ Absolute mode: |noise| for ridge textures
│       ├─ palette_idx = noise[7:0] + pal_offset
│       ├─ Palette select → Y/U/V from 4 LUT schemes
│       ├─ Contrast: luma × contrast_reg / 512
│       └─ Video mod: luma × input_Y / 1024
│
├── Mix: Interpolator (4 clk) ──────────────────────────────────
│   └─ Y/U/V wet/dry crossfade via Mix fader
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock shift register for hsync/vsync/field/data
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select generated or pass-through signal
```

The pipeline is a classic noise-generation architecture: coordinate computation → hash → dot product → interpolation → palette mapping. The hash function is fully combinational (no BRAM), hashing cell coordinates through XOR-rotate-add operations to produce 3-bit gradient indices. The four dot products use 8-direction gradient vectors quantised to ±1 and ±0.5 components, computed entirely with shifts and adds. The smoothstep interpolation approximates the quintic ease curve with a mirrored piecewise-linear function, then feeds two successive slerp (signed linear interpolation) passes — first horizontally, then vertically — to produce the final noise value.

The palette stage maps the 8-bit noise index (plus per-frame cycling offset) through one of four color schemes. Contrast scaling multiplies the result by `contrast_reg / 512`, and video modulation mode multiplies with the input video's Y channel, replacing chroma with the input's U/V. Note that toggle bit 1 is shared between Palette selection and Video Mod — changing the palette may also toggle video modulation, and vice versa.

---

## Parameter Reference

<img src={perlin_control_panel} alt="Videomancer front panel with Perlin loaded"/>
*Videomancer's front panel with Perlin active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Scroll Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the scroll animation speed via a DDS phase accumulator. At zero, the noise field is static. As the value increases, the noise scrolls faster in the direction selected by the Direction knob. The raw pot value is used directly as the 16-bit increment, so the scroll rate is linearly proportional to the knob position. At maximum, the noise rushes past rapidly, creating a streaming fluid-like texture.

---

#### Knob 2 — Scale
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 4 |

Selects the grid cell size using 3 top bits mapped to cell shift values 3 through 7, corresponding to cell sizes of 8, 16, 32, 64, and 128 pixels. Smaller cells produce fine-grained, detailed noise. Larger cells produce broad, smooth gradients. This control has the most dramatic effect on the visual character of the noise — small cells look like television static or film grain, while large cells look like cloud formations or lava flows.

---

#### Knob 3 — Direction
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |
| Suffix | deg |

Selects the scroll direction by dividing the pot range into four quadrants. 0–25%: scroll right (+X). 25–50%: scroll down (+Y). 50–75%: scroll left (−X). 75–100%: scroll up (−Y). The direction is axis-aligned — the VHDL implements a simplified decomposition that selects one axis at a time rather than computing true angular components.

---

#### Knob 4 — Turbulence
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Turbulence control. In the current implementation, this value is registered at vsync and stored in `s_turb_reg` for future use in multi-octave fractal summation (fBm). The second octave is described in the VHDL header but not yet implemented in the pipeline. Adjusting this control has no visible effect in the current build.

---

#### Knob 5 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the output contrast by scaling the palette luma. The palette Y value is multiplied by `contrast_reg` and right-shifted by 9 bits, equivalent to dividing by 512. At the default midpoint (512), the contrast is unity. Below midpoint, the output is darker and less contrasty. Above midpoint, the output is brighter and more contrasty, with values clipping at 1023.

---

#### Knob 6 — Palette Cycle
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the speed of palette color cycling. Each frame, the palette offset is incremented by `pot[9:2]` — the top 8 bits of the pot value. At zero, colors are static. At maximum, the palette index advances by 255 per frame, creating rapid color rotation. The cycling wraps around the 256-entry palette index space, producing continuous flowing color without discontinuities.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Marble | Cloud |
| **8 — Video Mod** | Off | On |
| **9 — Absolute** | Signed | Abs |
| **10 — Domain Warp** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control palette selection (2-bit), video modulation, absolute/signed mode, domain warping, and bypass. Note that toggle bit 1 is shared between Palette selection (`s_palette_sel <= registers_in(6)(1 downto 0)`) and Video Mod (`s_video_mod <= registers_in(6)(1)`). This means the second palette bit and the video modulation flag track the same hardware bit — changing one changes the other. This is a known hardware quirk documented in the VHDL.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the delayed input video (dry) and the noise-generated output (wet). At 0%, only the input passes through. At 100%, the full noise texture is output. Intermediate values superimpose the noise over the video with adjustable opacity, useful for creating textured overlays.

---

## Guided Exercises

These exercises explore the noise generator's controls from basic static textures through animated scrolling to advanced domain warping and video modulation.

### Exercise 1: Classic Marble Texture

<img src={perlin_exercise1_result} alt="Classic Marble Texture result"/>
*Classic Marble Texture — simulated result across source images.*
**Objective**: Generate a static grayscale Perlin noise texture resembling polished marble, exploring scale and contrast.

1. **Default state**: Confirm Palette is Marble, Scroll Speed at 0%, and Absolute mode is Signed. A smooth grayscale noise pattern fills the screen.
2. **Scale sweep**: Rotate Scale through all positions. Watch the noise transition from fine grain (8px cells) through medium texture (32px) to broad smooth gradients (128px).
3. **Contrast**: Sweep Contrast from minimum to maximum. At low values, the texture is flat and washed out. At high values, the marble veins become sharp and dramatic.
4. **Absolute ridges**: Toggle Absolute to Abs. The smooth gradients fold into ridge patterns with sharp creases — a veined marble effect.
5. **Palette cycling**: Increase Palette Cycle slightly. The grayscale noise pulses gently as brightness levels shift.

**Key concepts**: Grid cell size controls spatial frequency, contrast scales the output dynamic range, absolute mode folds signed noise into ridge patterns

---

### Exercise 2: Flowing Fire

<img src={perlin_exercise2_result} alt="Flowing Fire result"/>
*Flowing Fire — simulated result across source images.*
**Objective**: Create an animated fire texture using the Fire palette, upward scrolling, and absolute mode for flickering flame shapes.

1. **Fire palette**: Select the Fire palette (position 4 on the Palette toggle).
2. **Upward scroll**: Set Direction to about 90% (upward). Increase Scroll Speed to about 40%. The fire palette scrolls upward.
3. **Absolute folding**: Toggle Absolute to Abs. The smooth gradients become jagged flame tongues.
4. **Scale for flames**: Set Scale to about 3 (16px cells) for medium-sized flame structures.
5. **Contrast for intensity**: Increase Contrast to about 70% for vivid reds and yellows.
6. **Palette cycling**: Add gentle Palette Cycle (~20%) for animated color variation within the flames.
7. **Domain warp**: Enable Domain Warp to add turbulent swirling to the flame motion.

**Key concepts**: Fire palette has a black floor creating dark negative space, absolute mode creates jagged ridge patterns resembling flames, domain warp adds turbulent flow

---

### Exercise 3: Video-Modulated Cloud Overlay

<img src={perlin_exercise3_result} alt="Video-Modulated Cloud Overlay result"/>
*Video-Modulated Cloud Overlay — simulated result across source images.*
**Objective**: Superimpose cloud-palette noise over a live video source using video modulation and partial mix.

1. **Cloud palette**: Select the Cloud palette (position 2).
2. **Large scale**: Set Scale to 7 (64px cells) for broad, cloud-like formations.
3. **Slow scroll**: Set Scroll Speed to about 15% and Direction to 0° for gentle rightward drift.
4. **Video modulation**: Enable Video Mod. The noise pattern is now multiplied with the input video's brightness — the noise is visible only where the video is bright.
5. **Partial mix**: Reduce Mix to about 50%. The cloud texture overlays the video at half opacity.
6. **Contrast**: Adjust Contrast to about 55% for gentle cloud density.
7. **Signed mode**: Keep Absolute in Signed mode for smooth, soft cloud edges.

**Key concepts**: Video modulation multiplies noise with input Y channel for content-dependent textures, partial Mix creates translucent overlay, large cell size produces smooth cloud shapes

---


## Tips

- **Scale is the most important control**: Cell size sets the fundamental character of the noise — 8px cells look like static grain, 128px cells look like clouds or lava. Start here when designing a texture.
- **Absolute mode for organic textures**: Folding the noise at zero creates ridge patterns that resemble marble veins, lightning, or cracked earth. Combine with the Terrain palette for topographic effects.
- **Fire palette needs upward scroll**: The Fire palette looks most flame-like when scrolling upward (Direction ~90%) at moderate speed. Add domain warp for turbulent flickering.
- **Domain warp accumulates**: The warp feedback doesn't decay between frames, so the distortion grows over time. Toggle Domain Warp off and back on to reset the accumulated distortion.
- **Video Mod creates content-dependent noise**: The noise intensity follows the input video's brightness, making luminous textures that respond to live camera feeds.
- **Palette bit overlap is documented**: Selecting Cloud or Fire palette also enables Video Mod due to shared bit 1. If you want pure noise without video modulation, use Marble or Terrain.
- **Palette Cycle adds free animation**: Even with Scroll Speed at zero, palette cycling creates animated color flow. Combine with static noise for shimmering crystal or aurora effects.
- **Mix for textured overlays**: At 20–40% Mix, the noise becomes a subtle texture layer over the input video — useful for adding grain, atmosphere, or organic movement to clean sources.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation BT.601; the standard for analog-to-digital conversion of SD video, defining the YUV color matrix used throughout Videomancer. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator at a fixed rate each clock cycle. |
| **Domain Warp** | Feeding the output of a noise function back into its coordinate inputs, creating self-referential distortion that produces turbulent, swirling patterns. |
| **fBm** | Fractional Brownian motion; summing multiple octaves of noise at increasing frequency and decreasing amplitude to create fractal textures with detail at multiple scales. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Gradient Noise** | A noise algorithm that assigns random gradient vectors to grid vertices and computes dot products with displacement vectors, producing smoother results than value noise. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function of its previous state, producing pseudo-random sequences. |
| **Octave** | In noise synthesis, one layer of noise at a specific frequency. Multiple octaves are summed to create fractal detail. |
| **Palette** | A lookup table mapping noise index values to YUV color triplets. |
| **Perlin Noise** | The gradient noise algorithm invented by Ken Perlin in 1983 for procedural texturing in computer graphics. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Smoothstep** | An S-shaped interpolation function that has zero first derivative at both endpoints, eliminating visible grid artifacts. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
