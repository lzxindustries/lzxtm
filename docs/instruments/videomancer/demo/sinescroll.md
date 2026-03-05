---
draft: true
sidebar_position: 274
slug: /instruments/videomancer/sinescroll
title: "Sinescroll"
image: /img/instruments/videomancer/sinescroll/sinescroll_hero.png
description: "The sine scroller is one of the most iconic effects in demoscene history."
---

import sinescroll_hero from '/img/instruments/videomancer/sinescroll/sinescroll_hero.png';
import sinescroll_animation from '/img/instruments/videomancer/sinescroll/sinescroll_animation.gif';
import sinescroll_control_panel from '/img/instruments/videomancer/sinescroll/sinescroll_control_panel.png';
import sinescroll_exercise1_result from '/img/instruments/videomancer/sinescroll/sinescroll_exercise1_result.gif';
import sinescroll_exercise2_result from '/img/instruments/videomancer/sinescroll/sinescroll_exercise2_result.gif';
import sinescroll_exercise3_result from '/img/instruments/videomancer/sinescroll/sinescroll_exercise3_result.gif';

# Sinescroll

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={sinescroll_hero} alt="Sinescroll hero image"/>
*Sine Scroll warping a camera feed through undulating per-scanline horizontal displacement with colour bar tinting.*
<img src={sinescroll_animation} alt="Sinescroll animated output"/>
*Sinescroll output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

The sine scroller is one of the most iconic effects in demoscene history. On the ZX Spectrum, Commodore 64, and especially the Amiga, coders discovered that displacing each scanline by a different horizontal offset — with those offsets following a sine wave — could make static text and graphics appear to ripple and flow. The trick exploits the raster nature of CRT displays: because each line is drawn independently, shifting it costs almost nothing.

Sine Scroll applies this technique to live video. Every scanline of the incoming frame is captured into a line buffer, then read back at a displaced position computed from a sinusoidal lookup table. The displacement amount, frequency, speed, and shape are all continuously controllable. The name combines the mathematical *sine* function with the demoscene term *scroller* — a horizontally scrolling text or image effect.

At gentle settings, Sine Scroll produces a subtle liquid ripple across the image. At extreme amplitude and frequency, the picture disintegrates into bands of colour that bear little spatial relationship to the original, creating abstract patterns from any video source.

---

## Quick Start

1. **Start with amplitude**: The displacement depth is the most dramatic control. Get the ripple depth you want before adjusting frequency.
2. **Speed creates life**: Even a tiny H Speed offset makes a static image feel alive. Use very small values for subtle ambient motion.
3. **Phase twist breaks patterns**: Adding twist prevents the displacement from looking like a simple perspective transform. It introduces the spatial complexity that makes the effect feel organic.

---

## Background

### What Is Raster Displacement?

A raster display draws the image one horizontal line at a time, from top to bottom. If you shift each line sideways by a different amount before it reaches the screen, the image appears to warp vertically. This is **raster displacement** — also known as a raster scroll or raster split. The Amiga's copper coprocessor made this trivially easy by allowing register writes to be scheduled for specific scanlines, making per-line displacement a fundamental building block of demoscene visual effects.

### What Is a Quarter-Wave Sine LUT?

Computing a full sine function in real time on limited hardware is expensive. The standard trick is to precompute one quarter of the sine wave (0° to 90°) in a lookup table and derive the other three quarters through symmetry. The first quarter gives the positive rising edge; mirroring it gives the second quarter (positive falling); negating gives the third and fourth quarters. This technique reduces storage by 4× while producing a mathematically exact full-period sine. Sine Scroll uses a 256-entry quarter-wave table, yielding 1024 distinct phase positions.

### What Is Phase Twist?

Phase twist adds a per-line increment to the wave phase. Without twist, every scanline indexes the same sine wave — lines near each other get similar offsets, producing smooth undulation. With twist, the phase advances rapidly from line to line, creating tight, high-frequency spatial ripples. At maximum twist, the displacement pattern changes so quickly between adjacent scanlines that the image appears to shatter into thin horizontal fragments.

### What Are Colour Bars?

In demoscene terminology, colour bars (or copper bars) are horizontal bands of smoothly cycling colour overlaid on the display. The technique originated on the Amiga, where the copper coprocessor could change the background colour register on each scanline, producing rainbow gradient effects with zero CPU cost. Sine Scroll's optional colour bar mode tints each displaced scanline with a cycling hue derived from its vertical position, adding an Amiga-style chromatic wash to the displacement effect.

### What Is Waveshaping?

The displacement waveform doesn't have to be a pure sine. By post-processing the sine LUT output, you can produce alternative shapes: triangle (linear ramp up and down), square (hard snap between extremes), and sawtooth (linear ramp in one direction). Each shape changes the visual character of the displacement — sine gives smooth ripples, triangle gives V-shaped folds, square gives abrupt shifts, and sawtooth gives a cascading staircase effect.


---

## Signal Flow

Line Buffer Write → Wave Phase Computation → Wave Shape + LUT Lookup → ... → Wet/Dry Mix → Bypass Mux

```
Input Video (YUV 4:4:4)
│
├── Line Buffer Write ─────────────────────────────────────────
│   └─ Capture Y, U, V into 2048-entry BRAM at write address
│
├── Wave Phase Computation (Stage 1) ──────────────────────────
│   ├─ coord = v_count (or h_count if Axis = Vertical)
│   ├─ phase = coord × frequency + v_phase + v_count × phase_twist
│   └─ Mirror: fold from screen center if enabled
│
├── Wave Shape + LUT Lookup (Stage 2) ─────────────────────────
│   ├─ Sine:     quarter-wave LUT with quadrant mirroring
│   ├─ Triangle: abs(ramp) rescaled to ±511
│   ├─ Square:   sign(phase) × 511
│   └─ Sawtooth: linear phase − 512
│
├── Displacement + BRAM Read (Stages 3–4) ─────────────────────
│   ├─ displacement = wave_shaped × amplitude
│   ├─ read_addr = h_count + displacement + h_scroll
│   ├─ Wrap to 0..2047 range
│   └─ Read Y, U, V from line buffer at displaced address
│
├── Colour Bar Tinting + Brightness (Stage 5) ─────────────────
│   ├─ Y: brightness scaling (Y × brightness)
│   ├─ If Color Bars: blend source chroma with per-line hue
│   └─ If no Color Bars: pass source chroma
│
├── Wet/Dry Mix (Interpolator, 4 clocks) ──────────────────────
│   └─ lerp(delayed_input, processed, mix_amount)
│
└── Bypass Mux ────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical path runs through the line buffer. Incoming video is written at the current pixel position, then read back at an offset address computed from the sine wave. Because the buffer is 2048 entries wide (wider than the 1920 active pixels of HD video), displacements wrap around cleanly without visible seams. The horizontal and vertical scroll phase accumulators advance once per frame during vsync, creating continuous animation even when the input video is static.

The colour bar tinting path is independent of the displacement — it adds chromatic content based on the scanline's vertical position, not its displaced horizontal position. This means the colour wash remains stable and smooth even when the displacement is extreme.

---

## Parameter Reference

<img src={sinescroll_control_panel} alt="Videomancer front panel with Sinescroll loaded"/>
*Videomancer's front panel with Sinescroll active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Amplitude
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At zero, the image passes through undistorted. As you increase amplitude, each scanline shifts further from its original position, creating progressively deeper ripples. At maximum, lines can shift by hundreds of pixels, causing the image to wrap around through the line buffer. Internally, scales the sine wave displacement depth.

---

#### Knob 2 — Frequency
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls how many complete wave cycles fit within the screen height. Low frequency means the entire image bends as one long, slow undulation. High frequency packs many tight ripples into the frame, creating a corrugated or pleated look. Combined with phase twist, high frequency can produce interference-like moire patterns.

---

#### Knob 3 — H Speed
| Property | Value |
|----------|-------|
| Range | -90deg – 90deg |
| Default | 16deg |
| Suffix | deg |

Bipolar horizontal scroll speed. At center (0°), the displacement pattern is static. Turning clockwise scrolls the displacement pattern to the right; counter-clockwise scrolls left. This animates the effect even when the input video is a still frame, making the ripples appear to flow across the screen.

---

#### Knob 4 — V Speed
| Property | Value |
|----------|-------|
| Range | -90deg – 90deg |
| Default | 0deg |
| Suffix | deg |

Bipolar vertical phase scroll speed. This shifts the sine wave's starting phase each frame, causing the ripple pattern to drift vertically. Combined with H Speed, you can create complex Lissajous-like animation paths where the ripples flow diagonally across the screen.

---

#### Knob 5 — Phase Twist
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Adds a per-line phase increment to the wave. Without twist, adjacent scanlines receive similar displacements, producing a smooth wave. With twist, the phase ratchets forward on every line, creating increasingly rapid spatial variation. At extreme settings, the displacement changes so quickly between lines that the image fragments into thin displaced strips.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Output brightness scaling. The displaced luminance channel is multiplied by this value before mixing. Use it to darken the effect for layering with additive compositing in a signal chain, or to compensate for brightness changes caused by the displacement.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Wave Shape** | Sine | Sawtooth |
| **8 — Axis** | Horizontal | Vertical |
| **9 — Mirror** | Off | On |
| **10 — Color Bars** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control waveform shape, displacement axis, spatial symmetry, colour enhancement, and bypass. The wave shape switch (7) selects from four waveshaping algorithms applied to the sine LUT output. The remaining switches are independent binary options.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfade between the unprocessed input (dry) and the displaced output (wet). At 0%, the output is identical to the input. At 100%, the fully processed signal appears. Intermediate positions blend the two, which can create a ghostly double-image effect as the displaced and original images overlap.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Sinescroll processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore raster displacement from subtle ripple to full waveform deconstruction. Each builds on the previous, progressively engaging more controls.

### Exercise 1: Classic Sine Ripple

<img src={sinescroll_exercise1_result} alt="Classic Sine Ripple result"/>
*Classic Sine Ripple — simulated result across source images.*
**What You'll Create**: Learn how amplitude and frequency shape the basic sine displacement effect.

1. **Gentle ripple**: Set Amplitude to ~25% and Frequency to ~20%. The image should show a subtle undulation.
2. **Deeper wave**: Increase Amplitude to ~60%. The displacement becomes clearly visible as a sinusoidal deformation.
3. **Tight pleats**: Increase Frequency to ~70% while keeping high amplitude. The image folds into many tight corrugations.
4. **Animate**: Turn H Speed slightly clockwise from center. The ripples begin to flow horizontally across the screen.
5. **Vertical drift**: Add a small V Speed offset. The ripple origin point now drifts both horizontally and vertically.

**Key concepts**: Raster displacement shifts each scanline independently, amplitude controls depth, frequency controls spatial period, speed controls animation

---

### Exercise 2: Waveshaping Comparison

<img src={sinescroll_exercise2_result} alt="Waveshaping Comparison result"/>
*Waveshaping Comparison — simulated result across source images.*
**What You'll Create**: Compare the visual character of each waveform shape at identical displacement settings.

1. **Setup**: Set Amplitude ~50%, Frequency ~40%, H Speed slightly clockwise.
2. **Sine**: Select Wave Shape = Sine. Observe the smooth, organic ripple.
3. **Triangle**: Switch to Triangle. Note the V-shaped folds — sharper transitions than sine.
4. **Square**: Switch to Square. The image now snaps between two horizontal positions — a chopping effect.
5. **Sawtooth**: Switch to Sawtooth. Scanlines cascade in one direction — a waterfall or shearing pattern.
6. **Mirror**: Enable Mirror mode and cycle through shapes again. Observe how symmetry changes each pattern.

**Key concepts**: Waveshaping post-processes the sine LUT, each shape has different transition characteristics, mirror mode reflects displacement from screen center

---

### Exercise 3: Copper Bar Tinting

<img src={sinescroll_exercise3_result} alt="Copper Bar Tinting result"/>
*Copper Bar Tinting — simulated result across source images.*
**What You'll Create**: Add Amiga-style colour bar tinting to the displacement effect for a full demoscene aesthetic.

1. **Displacement**: Set moderate Amplitude (~40%), Frequency (~30%), and H Speed.
2. **Colour bars**: Enable Color Bars. A rainbow wash appears on each scanline.
3. **Phase twist**: Slowly increase Phase Twist. The colour gradient tilts and compresses, creating diagonal rainbow streaks.
4. **Brightness**: Reduce Brightness to ~60% for a moodier, more saturated result.
5. **Axis swap**: Switch Axis to Vertical. The displacement now runs top-to-bottom, and the colour wash follows.
6. **Mix**: Sweep the Mix fader to blend the colourful displaced version with the original monochrome source.

**Key concepts**: Colour bars are per-scanline hue cycling, phase twist creates spatial chroma variation, axis mode changes displacement direction

---


## Tips

- **Colour bars on monochrome**: The colour bar mode is most impactful on desaturated or monochrome sources, where it adds all the colour.
- **Square wave for glitch**: The Square waveshape creates a hard-switching effect that reads as a digital glitch rather than a smooth ripple.
- **Feedback**: Route the output back to the input for recursive displacement. The ripples compound into increasingly complex patterns.
- **Mix for layering**: Use 50% mix to create a ghostly double image where the displaced and original frames overlap.

---

## Glossary

| Term | Definition |
|------|------------|
| **Copper** | The coprocessor in the Amiga's custom chipset that could modify display registers on a per-scanline basis, enabling colour bars and raster effects. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms using a phase accumulator and a lookup table. |
| **Demoscene** | A computer art subculture focused on creating real-time audiovisual productions (demos) that push hardware to its limits. |
| **LUT** | Lookup Table; a precomputed table of values used to accelerate mathematical functions like sine. |
| **Phase** | The position within a periodic waveform cycle, measured in degrees or as a fraction of the full period. |
| **Quarter-Wave** | A symmetry-exploiting technique that stores only one quarter of a sine wave and derives the rest through mirroring and negation. |
| **Raster** | The horizontal scanning pattern used by CRT and video displays to draw an image line by line. |
| **Sample-and-Hold** | Reading a signal value and holding it constant until the next sample, used here to capture scanline pixels into the buffer. |
| **Waveshaping** | Post-processing a base waveform (sine) to produce alternative shapes (triangle, square, sawtooth). |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
