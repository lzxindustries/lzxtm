---
draft: true
sidebar_position: 307
slug: /instruments/videomancer/totem
title: "Totem"
image: /img/instruments/videomancer/totem/totem_hero.png
description: "In the Amiga demoscene of the early 1990s, one visual effect became a calling card of technical prowess: the copper bar."
---

import totem_hero from '/img/instruments/videomancer/totem/totem_hero.png';
import totem_animation from '/img/instruments/videomancer/totem/totem_animation.gif';
import totem_control_panel from '/img/instruments/videomancer/totem/totem_control_panel.png';
import totem_exercise1_result from '/img/instruments/videomancer/totem/totem_exercise1_result.gif';
import totem_exercise2_result from '/img/instruments/videomancer/totem/totem_exercise2_result.gif';
import totem_exercise3_result from '/img/instruments/videomancer/totem/totem_exercise3_result.gif';

# Totem

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={totem_hero} alt="Totem hero image"/>
*Totem rendering eight interleaved Kefrens bars in the Braid preset, their sinusoidal paths weaving a luminous twisted column against black.*
<img src={totem_animation} alt="Totem animated output"/>
*Totem output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In the Amiga demoscene of the early 1990s, one visual effect became a calling card of technical prowess: the copper bar. By reprogramming the display hardware's color registers on every scanline, demo coders could create the illusion of smooth, colored horizontal bars floating and weaving across the screen. The most advanced variant — Kefrens bars — gave each bar a different horizontal position per scanline, so the bars traced sinusoidal paths that appeared to twist and braid around each other like a three-dimensional column.

Totem recreates this technique in real-time video hardware. Multiple horizontal bars are rasterized in parallel, each following a sine-wave path with configurable frequency, amplitude, and phase offset. The bars are composited additively — where they overlap, their colors blend toward white, creating bright highlight seams along the twisting intersections. Eight preset motion configurations (Column, Braid, DNA, Cascade, Maypole, Crown, Chaos, Minimal) define different frequency and phase relationships between the bars, producing visual patterns ranging from a single oscillating column to chaotic multi-frequency interference.

The name *Totem* refers to a carved totem pole — a vertical structure made of stacked, interleaved figures. The visual output of the program, especially in the Braid and DNA presets, resembles a luminous carved column rotating in space.

---

## Background

### The Amiga Copper and Raster Effects

The Amiga's custom Agnus chip included a coprocessor called the Copper that could execute simple instructions synchronized to the video beam position. By writing new color values to palette registers at specific scanline positions, demo programmers could change the background color on every line — creating smooth horizontal gradient bars with no CPU overhead. This technique, called "raster bars" or "copper bars," became one of the foundational effects of the Amiga demoscene and spawned increasingly complex variants.

### Kefrens Bars: Per-Scanline Displacement

The group Kefrens (from Denmark) popularized a variant where each bar's horizontal position varied per scanline, typically following a sine wave. Instead of simple horizontal stripes, the bars traced curved paths across the screen — sine waves, figure-eights, and helices. The key insight was that by changing only the *position* of each bar on each scanline (not its shape), the effect remained computationally cheap while looking dramatically three-dimensional.

### Additive Compositing and Light Illusions

When multiple translucent light sources overlap, their intensities add together. This is how real light behaves — two flashlight beams crossing become brighter at the intersection. Totem uses additive compositing for its bar layers: each bar contributes color weighted by a smooth gradient profile (bright center, fading edges), and overlapping bars sum their contributions. The result is a convincing illusion of glowing, semi-transparent ribbons passing through each other, with bright white seams where they intersect.

### Phase Relationships and Visual Complexity

The visual complexity of the bar pattern depends entirely on the phase and frequency relationships between bars. When all bars share the same frequency and phase, they move in lockstep — a single column. When bars have different frequencies (harmonics), they drift in and out of alignment, creating ever-changing interference patterns. When bars have the same frequency but offset phases, they trace parallel paths that braid around each other. Totem's eight presets explore this parameter space, from the simplest (Single column) to the most complex (Chaos, with incommensurate frequency ratios).

### DDS Phase Accumulators for Smooth Animation

Totem uses a Direct Digital Synthesis (DDS) approach for animation: each bar maintains a 16-bit phase accumulator that increments by a speed-dependent value once per video frame. The accumulated phase is combined with the scanline number and the bar's frequency multiplier and phase offset to produce the sine argument. This produces smooth, continuous animation without jitter, and the speed control directly adjusts the rate of phase accumulation.


---

## Signal Flow

```
Per Frame:
│
├── Phase Update ─────────────────────────────────────────────
│   │
│   └─ For each bar i (0..7):
│        bar_phase[i] += speed * preset.freq[i]
│
Per Scanline:
│
├── Bar Position ─────────────────────────────────────────────
│   │
│   └─ For each bar i:
│        arg = vcount * frequency + bar_phase[i] + preset.phase[i]
│        sine_val = sin_lut(arg)
│        bar_x[i] = center + (sine_val * amplitude) >> 9
│
Per Pixel:
│
├── Distance + Gradient ──────────────────────────────────────
│   │
│   └─ For each bar i (0..num_bars):
│        dx = |pixel_x - bar_x[i]|
│        if dx < half_width:
│            brightness[i] = (half_width - dx) << 3
│        else:
│            brightness[i] = 0
│
├── Additive Composite ───────────────────────────────────────
│   │
│   └─ For each active bar i:
│        color_idx = (i + hue_shift) mod 8
│        acc_y += bar_color[color_idx].y * brightness[i] >> 10
│        acc_u += bar_color[color_idx].u * brightness[i] >> 10
│        acc_v += bar_color[color_idx].v * brightness[i] >> 10
│
├── Clamp + Brightness ───────────────────────────────────────
│   │
│   ├─ Clamp Y/U/V to 0..1023
│   ├─ Y *= brightness_knob / 1024
│   └─ Over Video: Y += input_Y >> 1 (additive)
│
├── Mix ──────────────────────────────────────────────────────
│   └─ interpolator_u × 3 (wet/dry crossfade)
│
└── Bypass ───────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical architecture is that bar positions are computed per-scanline (they depend only on the vertical counter), but distance and gradient brightness are computed per-pixel (they depend on the horizontal counter). This two-level computation is what makes Kefrens bars efficient — the expensive sine evaluation happens once per line, while the per-pixel work is a simple distance comparison and linear gradient calculation.

Additive compositing with per-layer palette coloring means that overlapping bars create mixed colors. Two complementary bars (e.g., red and cyan) overlapping produce white at the intersection. The brightness knob scales the composite result *after* additive summation, so it controls overall luminosity without affecting the blend ratios between layers.

---

## Parameter Reference

<img src={totem_control_panel} alt="Videomancer front panel with Totem loaded"/>
*Videomancer's front panel with Totem active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the animation speed of the bar pattern. The value sets the DDS phase increment applied to each bar's phase accumulator once per frame. At zero, the bars are frozen in place. At low values, the pattern evolves slowly — bars drift gently. At higher values, the bars oscillate rapidly, with complex presets producing fast-moving interference patterns. The speed is multiplied by each bar's preset frequency factor, so higher multipliers in presets like Cascade and Chaos amplify the speed effect differently per bar.

---

#### Knob 2 — Amplitude
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the horizontal sweep amplitude — how far the bars travel from center. At zero, all bars sit at the center of the screen regardless of their sine position. As amplitude increases, the bars sweep wider, eventually reaching the edges of the frame. At maximum, the bars can travel well beyond the visible area, appearing only briefly as they cross the screen. The amplitude is applied as a multiplier on the sine lookup result.

---

#### Knob 3 — Frequency
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the sine oscillation frequency — how many complete sine cycles fit within the vertical extent of the screen. At low values, each bar traces a gentle, wide curve across the full screen height. At high values, each bar oscillates rapidly, creating many tight undulations within the frame. Combined with the preset's per-bar frequency multipliers, this control determines the spatial density of the bar pattern.

---

#### Knob 4 — Bar Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the width of each bar's gradient profile. At zero, bars are vanishingly thin and barely visible. As width increases, bars become broader with wider gradient falloff zones. At maximum, bars are very wide and their gradients overlap significantly even when their centers are far apart. The width is computed as `register >> 2`, giving a half-width in pixels. The gradient is linear: maximum brightness at center, falling to zero at the edges.

---

#### Knob 5 — Hue Shift
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |
| Suffix | deg |

Rotates the palette color assignment across bar layers. Each bar is assigned a color from the 8-entry palette based on its layer index plus the hue shift offset. At zero offset, bar 0 gets color 0 (red), bar 1 gets color 1 (cyan), etc. Rotating the hue shift reassigns which color appears on which bar without changing the spatial pattern. At 360°, the assignment wraps back to the original mapping.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the overall brightness of the bar composite. Applied as a multiplier `(Y * brightness) >> 10` after additive compositing. At zero, the output is black regardless of bar activity. At the default position (~75%), bars appear at natural intensity. Higher values push toward clipping, especially where multiple bars overlap. This control does not affect the U/V channels — only luminance.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Preset** | Column | Braid |
| **8 — Bar Count** | 4 Bars | 8 Bars |
| **9 — Gradient** | Smooth | Hard |
| **10 — Over Video** | Black | Add |
| **11 — Bypass** | Off | On |

Toggle 7 selects from 8 motion presets that define frequency and phase relationships between bar layers. Toggle 8 switches between 4 and 8 active bar layers. Toggle 9 selects smooth (linear gradient) or hard-edge bar profiles. Toggle 10 controls whether bars render against black or are additively composited over the input video. Toggle 11 bypasses all processing. The preset selection is the primary creative control — each preset produces a fundamentally different visual geometry.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix crossfade between the processed bar output and the delayed input signal. At 0%, the output is the unprocessed input. At 100%, the output is the full bar composite. Intermediate positions blend the bar pattern with the input at proportional intensity, allowing subtle overlays or faint bar textures without full replacement of the source signal.

---

## Guided Exercises

These exercises explore Totem's Kefrens bar geometry, from a single oscillating column through complex multi-bar braiding to full additive video overlay.

### Exercise 1: Single Oscillating Column

<img src={totem_exercise1_result} alt="Single Oscillating Column result"/>
*Single Oscillating Column — simulated result across source images.*
**Objective**: Understand the basic per-scanline bar displacement mechanism and how speed, amplitude, and frequency shape the bar's path.

1. **Minimal preset**: Set Preset to Minimal (single bar only). Observe a single bright bar tracing a sine wave path.
2. **Adjust amplitude**: Sweep Amplitude from 0% to maximum. Watch the bar path widen from a straight vertical line to a wide sinusoidal sweep.
3. **Adjust frequency**: Increase Frequency. The bar path gains more oscillations — tighter sine curves within the same screen height.
4. **Adjust speed**: Increase Speed. The bar begins to oscillate horizontally in real time, its position shifting smoothly each frame.
5. **Bar width**: Sweep Bar Width from minimum to maximum. The bar grows from a thin line to a wide gradient stripe.
6. **Switch to Column**: Change Preset to Column. All 4 (or 8) bars now move in lockstep — the column appears as one thick multi-colored bar.

**Key concepts**: Bar position follows a sine wave per scanline, frequency controls spatial oscillation density, amplitude controls horizontal displacement range, speed controls temporal animation rate

---

### Exercise 2: Braided DNA Helix

<img src={totem_exercise2_result} alt="Braided DNA Helix result"/>
*Braided DNA Helix — simulated result across source images.*
**Objective**: Explore phase relationships between bars and how they create the illusion of intertwining three-dimensional structure.

1. **DNA preset**: Set Preset to DNA. Two groups of bars trace offset sine paths, creating a double-helix pattern.
2. **Observe intersections**: Watch where the two groups cross — additive compositing creates bright white seams at the intersection points.
3. **Try Braid preset**: Switch to Braid. The pattern changes to a woven, braided structure with different frequency ratios between groups.
4. **Hue shift**: Rotate Hue Shift to reassign colors between bars. Note how the color pattern changes without affecting the geometry.
5. **8 Bars**: Switch Bar Count to 8 Bars. The same DNA/Braid pattern becomes denser and more complex.
6. **Hard gradient**: Switch Gradient to Hard. The soft cylinder illusion is replaced by hard-edged rectangular bars — a more retro, 8-bit aesthetic.

**Key concepts**: Phase offset creates the illusion of depth and intertwining, additive compositing produces bright highlights at intersections, more bars increase visual density without changing the underlying geometry

---

### Exercise 3: Chaos Over Video

<img src={totem_exercise3_result} alt="Chaos Over Video result"/>
*Chaos Over Video — simulated result across source images.*
**Objective**: Use the Chaos preset with Over Video mode to overlay complex non-repeating bar patterns on a live signal.

1. **Chaos preset**: Set Preset to Chaos. Incommensurate frequencies produce a non-repeating, constantly evolving pattern.
2. **Over Video mode**: Switch Over Video to Add. The bars now overlay the incoming video (or a flat gray if no input).
3. **Reduce brightness**: Lower Brightness to ~40% so the bars blend subtly with the video rather than dominating.
4. **Increase speed**: Push Speed to ~70%. The chaotic pattern evolves rapidly, creating a shimmering, organic overlay.
5. **Wide bars**: Increase Bar Width to ~60% for a softer, more diffuse glow effect.
6. **Hue rotation**: Slowly sweep Hue Shift while the pattern animates. The color mapping rotates through the bar layers continuously.

**Key concepts**: Incommensurate frequencies produce non-repeating visual patterns, Over Video mode additively mixes bars with the source, brightness scaling after additive composite controls blend intensity

---


## Tips

- **Start with Minimal**: Begin with the Minimal preset (single bar) to understand the basic per-scanline displacement before adding complexity with multi-bar presets.
- **Presets are the core creative tool**: Each preset's frequency and phase array produces a fundamentally different visual geometry. Explore all eight before tweaking other parameters.
- **Amplitude and frequency are complementary**: Low frequency + high amplitude = wide, gentle sine curves. High frequency + low amplitude = tight, dense oscillations. Both moderate = balanced complexity.
- **Bar width controls depth illusion**: Narrow bars with smooth gradients look like thin glowing wires. Wide bars look like translucent ribbons. The gradient profile is critical for the 3D cylinder illusion.
- **Hue shift rotates without restructuring**: Hue Shift changes *which* colors appear on *which* bars, but never changes the spatial pattern. Use it to find color combinations that highlight the preset geometry.
- **Over Video for augmented reality**: Add mode composites bars over live video, halving the input to prevent clipping. Reduce Brightness for subtle overlays.
- **Feedback loops create recursive geometry**: Route the output back to the input with Over Video enabled to create self-referencing bar structures that evolve continuously.
- **Speed zero for static patterns**: With Speed at 0%, the bar pattern freezes, revealing the spatial structure of the preset as a static graphic.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Compositing** | Layer blending where pixel values are summed; overlapping regions become brighter, mimicking real light addition. |
| **Copper** | The Amiga custom coprocessor that could modify display registers synchronized to the video beam, enabling raster bar effects. |
| **DDS** | Direct Digital Synthesis; a phase accumulator technique for generating smooth periodic waveforms at arbitrary frequencies. |
| **Demoscene** | Computer art subculture focused on creating audio-visual presentations (demos) that push hardware to its limits. |
| **Gradient** | A smooth transition in brightness from center to edge within each bar, creating a cylinder-like 3D illusion. |
| **Half-Width** | Half the total bar width; the distance from bar center to the point where brightness falls to zero. |
| **Kefrens Bars** | A demoscene effect where horizontal bars' positions vary per scanline, tracing curved paths across the screen. |
| **Phase Accumulator** | A counter incremented each frame whose value drives the sine lookup, producing continuous animation. |
| **Phase Offset** | A constant added to a bar's phase accumulator, shifting its sine wave relative to other bars. |
| **Preset** | A predefined set of frequency multipliers and phase offsets for all 8 bar layers, defining the visual geometry. |
| **Raster Bars** | Horizontal color bars created by modifying palette registers per scanline; the predecessor to Kefrens bars. |
| **Sine LUT** | A lookup table storing precomputed sine values, used to evaluate trigonometric functions efficiently in FPGA logic. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
