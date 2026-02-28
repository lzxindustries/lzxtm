---
draft: true
sidebar_position: 184
slug: /instruments/videomancer/organica
title: "Organica"
image: /img/instruments/videomancer/organica/organica_hero.png
description: "Organica generates procedural color palettes by sweeping a six-segment hue wheel across the video frame."
---

import organica_before_after from '/img/instruments/videomancer/organica/organica_before_after.png';
import organica_control_panel from '/img/instruments/videomancer/organica/organica_control_panel.png';
import organica_exercise1_result from '/img/instruments/videomancer/organica/organica_exercise1_result.png';
import organica_exercise2_result from '/img/instruments/videomancer/organica/organica_exercise2_result.png';
import organica_exercise3_result from '/img/instruments/videomancer/organica/organica_exercise3_result.png';
import organica_hero from '/img/instruments/videomancer/organica/organica_hero.png';
import organica_source1_kodim15 from '/img/instruments/videomancer/organica/organica_source1_kodim15.png';
import organica_source2_kodim03 from '/img/instruments/videomancer/organica/organica_source2_kodim03.png';
import organica_source3_kodim13_bw from '/img/instruments/videomancer/organica/organica_source3_kodim13_bw.png';

# Organica

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={organica_hero} alt="Organica hero image"/>
*Organica painting a flowing procedural color palette across the video frame, with hue gradients driven by horizontal position and input luminance.*
<img src={organica_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Organica applied.*

---

## Overview

Organica generates procedural color palettes by sweeping a six-segment hue wheel across the video frame. Instead of processing the input signal's texture or shape, Organica uses the input primarily as a brightness and position reference — the incoming luma can modulate where the hue gradient falls, creating organic color fields that respond to the content of the source material. The name evokes the smooth, living quality of the resulting color fields — gradients that breathe and shift in response to video input.

At its core, Organica maps horizontal pixel position to a hue value on a continuous color wheel. Two controls set the starting hue and how far the gradient sweeps. Another pair controls the saturation and brightness of the generated palette. An optional DDS (direct digital synthesis) accumulator adds animation, slowly rotating the hue field over time. When Video Mod is engaged, the input signal's luminance pushes the gradient position, so bright areas of the source pull different hues than dark areas.

The Turbulence parameter (Knob 5, `registers_in(4)`) is declared in the VHDL register mapping but is **not connected** to any processing logic — the noise modulation stage it was intended for has not been implemented. Adjusting this control has no effect on the output.

---

## Background

### The Six-Segment Hue Wheel

Color wheels date back to Isaac Newton's 1704 *Opticks*, where he arranged spectral hues in a circle. In digital video, a six-segment hue wheel divides the circle into primary and secondary color sectors: red → yellow → green → cyan → blue → magenta → red. Organica traverses this wheel using a linear ramp mapped from pixel position, producing smooth rainbow gradients whose starting point and width are user-controlled.

### Direct Digital Synthesis for Animation

Direct digital synthesis (DDS) is a technique borrowed from RF signal generation. A phase accumulator increments by a fixed step each clock cycle; the accumulated value wraps around at the word boundary, producing a sawtooth that drives the hue offset. The Speed control sets the step size — larger steps mean faster rotation through the palette. Because the accumulator wraps cleanly, the animation loops seamlessly without discontinuities.

### Video-Driven Modulation

The Video Mod toggle lets input luminance shift the gradient position on a per-pixel basis. Bright regions of the source pull the hue toward one end of the gradient range; dark regions pull toward the other. This creates a content-responsive palette where the color map follows the structure of the input video — edges, textures, and tonal gradients in the source all become visible in the hue mapping.

### Gradient Modes: Position-Based vs. Flat

When the Gradient toggle is off, every pixel in the frame receives the same hue — the value set by Hue Start. When Gradient is on, horizontal position drives the hue sweep: the left edge begins at Hue Start and the right edge reaches Hue Start plus Hue Range. This produces a smooth horizontal rainbow whose width and offset are continuously adjustable.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel (luma reference) ─────────────────────────────────
│   │
│   └─ Luma extraction for video modulation path
│
├── Palette Generation ─────────────────────────────────────────
│   │
│   ├─ 1. Position Ramp       (horizontal pixel position → 0..1)
│   ├─ 2. DDS Phase Offset    (accumulator adds animation shift)
│   ├─ 3. Hue Mapping         (position × Hue Range + Hue Start)
│   ├─ 4. Video Modulation    (optional: input Y shifts hue position)
│   ├─ 5. Hue Wheel Lookup    (6-segment HSV → YUV conversion)
│   ├─ 6. Saturation Scaling  (chroma amplitude from Saturation knob)
│   ├─ 7. Brightness Scaling  (luma amplitude from Brightness knob)
│   └─ 8. Invert              (optional luma inversion)
│
├── Dry/Wet Mix ────────────────────────────────────────────────
│   └─ Crossfade between input and generated palette
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or palette signal
```

The central interaction is between position-based hue mapping and video-driven modulation. When both Gradient and Video Mod are active, the hue at each pixel is determined by the sum of its horizontal position ramp and its input luminance — bright objects in the source shift the rainbow, creating organic contours of color that follow the video content. The Saturation and Brightness knobs act as final scaling stages applied after the hue wheel lookup, controlling the intensity and visibility of the palette without changing its spectral shape.

---

## Parameter Reference

<img src={organica_control_panel} alt="Videomancer front panel with Organica loaded"/>
*Videomancer's front panel with Organica active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the starting position on the hue wheel. At 0%, the gradient begins at red. Sweeping the control rotates the starting hue through the full spectrum. This is a pure offset — it shifts the entire palette without changing its width or shape. In flat mode (Gradient off), this control alone determines the single color applied to the entire frame.

---

#### Knob 2 — Scale
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls how far the gradient sweeps across the hue wheel. At 0%, the gradient collapses to a single hue (set by Knob 1). At 100%, the gradient spans the full wheel, producing a complete rainbow across the frame width. Intermediate values create partial sweeps — green-to-blue, red-to-yellow, etc. — depending on where Hue Start places the origin.

---

#### Knob 3 — Turbulence
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Base saturation level of the generated palette. At 0%, the output is fully desaturated (grayscale). At 100%, colors are at maximum chroma. This scales the U and V components symmetrically around the neutral axis. Moderate settings produce pastel palettes; high settings produce vivid, saturated hues.

---

#### Knob 4 — Bias
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Output brightness scaling applied after hue wheel conversion. At 0%, the output is black regardless of hue. At 100%, full brightness. This scales the Y component of the generated palette. Combined with Saturation, it controls whether the palette is vivid and bright, dark and saturated, or pale and washed.

---

#### Knob 5 — Softness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Turbulence — **this parameter is declared in the register mapping but is not connected to any processing stage**. The intended noise modulation was not implemented in the current VHDL. Adjusting this knob has no effect on the output. It is documented here for completeness and may be connected in a future firmware revision.

---

#### Knob 6 — Fill Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the DDS accumulator step size for hue animation. At 0%, no animation — the palette is static. As Speed increases, the entire hue field rotates continuously, cycling through the color wheel. The animation is smooth and seamless because the phase accumulator wraps at word boundaries. Higher values produce faster rotation. This control has no effect when Animate is off.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode A** | Off | On |
| **8 — Mode B** | Off | On |
| **9 — Mode C** | Off | On |
| **10 — Seed** | A | B |
| **11 — Invert** | Off | On |

The five toggles configure the palette's spatial structure and modulation behavior. Gradient and Video Mod control how hue is assigned to each pixel. Animate enables temporal evolution via the DDS accumulator. Invert flips the luma channel for negative-image effects. Bypass routes the input directly to the output for A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input signal and the generated palette. At 0%, the output is the unmodified input. At 100%, the output is the pure palette. Intermediate values blend the palette over the source, allowing subtle color washes or transparent overlays.

---

## Guided Exercises

These exercises progress from a static single-color field to animated, video-responsive palettes. Each builds on the previous, gradually engaging more of the palette engine.

### Exercise 1: Static Color Wash

<img src={organica_exercise1_result} alt="Static Color Wash result"/>
*Static Color Wash — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and varied brightness.

**Objective**: Learn how Hue Start and Saturation/Brightness interact to produce flat color overlays.

1. **Single color**: With Gradient off, set Hue Start to mid-range. The entire frame fills with a single hue.
2. **Rotate hue**: Sweep Hue Start slowly. Watch the color cycle through the full wheel — red, yellow, green, cyan, blue, magenta.
3. **Desaturate**: Lower Saturation toward 0%. The color progressively fades to gray.
4. **Dim**: Lower Brightness. The color darkens toward black.
5. **Mix**: Reduce Mix to ~50%. The flat color overlays the source video as a transparent tint.
6. **Invert**: Toggle Invert. The brightness relationship between palette and source reverses.

**Key concepts**: Hue Start selects spectrum position, Saturation controls chroma amplitude, Brightness controls luma amplitude, Mix blends palette with source

---

### Exercise 2: Rainbow Gradient

<img src={organica_exercise2_result} alt="Rainbow Gradient result"/>
*Rainbow Gradient — simulated result across source images.*
**Source**: Simple footage with a clear horizon or strong horizontal structure — landscapes, skylines.

**Objective**: Explore position-based hue gradients and their interaction with Hue Range.

1. **Enable gradient**: Turn on Gradient (Switch 7). A horizontal rainbow appears across the frame.
2. **Narrow sweep**: Set Hue Range low (~20%). Only a small portion of the wheel is visible — a gentle two-color gradient.
3. **Widen sweep**: Increase Hue Range toward 100%. The full spectrum appears from left to right.
4. **Shift origin**: Sweep Hue Start while Hue Range is at ~50%. The gradient slides along the color wheel.
5. **Video modulation**: Enable Video Mod (Switch 9). The rainbow warps to follow the brightness contours of the source.
6. **Animate**: Enable Animate (Switch 8) and set Speed to ~30%. The rainbow slowly rotates through the hue wheel.

**Key concepts**: Gradient maps horizontal position to hue, Hue Range controls spectral width, Video Mod adds content-responsive distortion, DDS animation adds temporal evolution

---

### Exercise 3: Animated Video-Responsive Palette

<img src={organica_exercise3_result} alt="Animated Video-Responsive Palette result"/>
*Animated Video-Responsive Palette — simulated result across source images.*
**Source**: High-contrast footage with movement — dancers, traffic, flowing water, or abstract video feedback.

**Objective**: Combine all palette features for fully animated, video-driven color fields.

1. **Full gradient**: Enable Gradient, set Hue Range ~70%, Saturation ~80%, Brightness ~90%.
2. **Video modulation**: Enable Video Mod. Watch the rainbow contort around bright and dark regions of the source.
3. **Animate**: Enable Animate, set Speed ~40%. The palette drifts through the spectrum.
4. **Lower mix**: Set Mix to ~60%. The palette becomes a transparent color layer over the source.
5. **Invert experiment**: Toggle Invert. The tonal mapping reverses — previously dark areas now glow.
6. **Speed sweep**: Slowly increase Speed from 0 to 80%. The rotation accelerates from glacial to rapid.
7. **Source change**: Switch to different source material. Watch how the palette responds to new brightness structures.

**Key concepts**: All four modulation sources (position, DDS, video luma, invert) combine additively to determine final hue; mix controls transparency of palette over source

---


## Tips

- **Start with flat mode**: Turn Gradient off and explore Hue Start alone before engaging the gradient. This builds intuition for the hue wheel before adding spatial mapping.
- **Saturation and Brightness are independent**: Saturation scales chroma (UV), Brightness scales luma (Y). You can have vivid dark colors or pale bright pastels.
- **Video Mod is the key creative control**: It transforms the palette from a generic color overlay to a content-responsive effect. The source video becomes visible through color variation rather than brightness.
- **Turbulence does nothing**: Do not expect Knob 5 to affect the output. The noise modulation stage is unimplemented.
- **Mix for transparency**: Partial mix values overlay the palette as a transparent wash, preserving source detail while adding color — useful for tinting.
- **Feedback loops**: Route the output back to the input for recursive color mapping. The palette re-maps its own output, creating evolving fractal-like color fields.
- **Speed for meditation**: Very low Speed values create barely perceptible color drift — excellent for ambient installations.
- **Combine with downstream effects**: Organica's clean gradients are ideal input for threshold keyers, posterizers, and edge detectors downstream.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | The ITU-R standard defining the color matrix used to convert between RGB and YUV in video systems. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator and using the result to index a lookup table. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Hue Wheel** | A circular arrangement of spectral hues divided into six sectors (red, yellow, green, cyan, blue, magenta). |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived luminance. |
| **Phase Accumulator** | A register that increments by a fixed step each clock; its overflow creates a periodic ramp waveform. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **Proc amp** | Processing amplifier; a gain-and-offset stage that applies contrast (multiplication) and brightness (addition) to a signal. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
