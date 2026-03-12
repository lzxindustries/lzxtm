---
draft: true
sidebar_position: 301
slug: /instruments/videomancer/tempest
title: "Tempest"
image: /img/instruments/videomancer/tempest/tempest_hero.png
description: "A storm is not random — it is a system of interacting oscillations, each warping the others."
---

import tempest_hero from '/img/instruments/videomancer/tempest/tempest_hero.png';
import tempest_animation from '/img/instruments/videomancer/tempest/tempest_animation.gif';
import tempest_control_panel from '/img/instruments/videomancer/tempest/tempest_control_panel.png';
import tempest_exercise1_result from '/img/instruments/videomancer/tempest/tempest_exercise1_result.gif';
import tempest_exercise2_result from '/img/instruments/videomancer/tempest/tempest_exercise2_result.gif';
import tempest_exercise3_result from '/img/instruments/videomancer/tempest/tempest_exercise3_result.gif';

# Tempest

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={tempest_hero} alt="Tempest hero image"/>
*Tempest generating storm-like spatial turbulence from three noise-modulated DDS oscillators folded through triangle waveshaping.*
<img src={tempest_animation} alt="Tempest animated output"/>
*Tempest output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

A storm is not random — it is a system of interacting oscillations, each warping the others. Tempest translates this principle into the video domain. Three direct digital synthesis oscillators sweep across horizontal, vertical, and temporal axes, their frequencies noise-modulated via FM synthesis to create churning, turbulent spatial patterns. The result is a generative texture field that ranges from gentle, rippling interference to violent visual chaos.

The name comes from the atmospheric phenomenon and its connotation of barely-controlled energy. At low noise modulation, Tempest produces orderly interference patterns — standing waves and Moire-like lattice structures. As noise-to-phase modulation increases, the oscillators' frequencies jitter unpredictably, and the pattern disintegrates into turbulence. A second noise injection path adds grain texture directly to the output luminance, independent of the spatial pattern.

The program processes input video through a proc_amp stage where the combined oscillator pattern becomes the brightness offset, and the Luma Gain control sets the contrast (how strongly the input modulates the output). This means Tempest can function as a pure spatial synthesizer (low gain, high cutoffs) or as a turbulence overlay on live video (high gain). Fade Amount crossfades between the processed output and a solid target colour, while desaturation and luma inversion provide final tonal shaping.

---

## Quick Start

1. **Start with zero noise**: Set Noise to Phase and Noise to Luma both to 0% to understand the clean oscillator lattice before adding turbulence.
2. **H and V Cutoff set the geometry**: Equal values create diagonal diamond patterns; unequal values create elongated horizontal or vertical structures.
3. **LFSR vs. Pattern are fundamentally different**: LFSR turbulence is organic and grain-like. Pattern turbulence is self-referencing and geometric. Choose based on the visual texture you want.

---

## Background

### Direct Digital Synthesis and Spatial Oscillators

Tempest's three oscillators are DDS phase accumulators — the same architecture used in radio transmitters and audio synthesizers to generate precise waveforms. Each accumulator adds a frequency word to a 16-bit phase register on every clock cycle within its range. The horizontal accumulator advances every pixel, the vertical every line, and the animation accumulator every frame. The upper 10 bits of each accumulator's phase form a ramp wave, which is then folded into a triangle by the frequency doubler stage. Because the accumulators wrap at 16 bits, the spatial period of each oscillator is determined entirely by the frequency word — higher values produce tighter spatial frequencies with more cycles across the screen.

### Frequency Modulation

In classic FM synthesis, one oscillator modulates the frequency of another, producing complex sidebands. Tempest applies this principle spatially: a noise source (LFSR pseudo-random or structured XOR pattern) modulates all three oscillator frequencies simultaneously. The noise is centred around zero — values above 512 push the frequency up, values below push it down. The Noise to Phase control scales this modulation depth. At maximum depth, the frequency can swing from near-zero to twice the base rate on a per-pixel basis, creating the characteristic turbulent, storm-like textures.

### LFSR Pseudo-Random Noise

The LFSR (Linear Feedback Shift Register) is a hardware-efficient random number generator. Tempest uses a 10-bit maximal-length LFSR with polynomial x¹⁰ + x⁷ + 1, producing a period of 1023 before repeating. Because the LFSR runs at video pixel rate, each pixel gets a different noise value, creating grain-like spatial texture. This noise source drives the turbulent mode — unstructured, aperiodic frequency modulation.

### Structured XOR Interference

The alternative noise mode replaces the LFSR with a structured pattern: the XOR of the horizontal and vertical ramp waves. Because the ramps are derived from the same accumulators being modulated, this creates a feedback loop — the pattern modulates its own generator frequencies. The result is self-similar interference patterns that can form complex geometric structures, qualitatively different from the grain-like LFSR turbulence.

### Triangle Waveshaping

The frequency doubler module folds a sawtooth ramp into a triangle wave by mirroring the upper half of the ramp about its midpoint. This doubles the fundamental frequency while removing abrupt discontinuities at the wrap point. Triangle waves produce smoother spatial gradients than raw sawtooths, which is why Tempest uses them as the base waveform for its oscillator sum. The three folded triangles are averaged together (sum >> 2) to produce the final spatial pattern.


---

## Signal Flow

```
[Video Timing Generator]
│
├─ H/V/F position ────────────────────────────────────────────
│
│  ┌──────────────────────────────────────┐
│  │  LFSR Noise ─or─ Ramp H XOR Ramp V  │◄── Noise Algo
│  │            (Noise Source)            │
│  └──────────┬───────────────────┬───────┘
│             │                   │
│     ┌───────▼────────┐  ┌──────▼──────────┐
│     │  FM Modulation │  │ Noise to Luma   │
│     │  × Noise to    │  │   Offset        │
│     │    Phase       │  └──────┬──────────┘
│     └───────┬────────┘         │
│             │                  │
│    ┌────────▼─────────────┐    │
│    │  3× DDS Accumulator  │    │
│    │  H (pixel), V (line),│    │
│    │  F (frame)           │    │
│    └────────┬─────────────┘    │
│             │                  │
│    ┌────────▼─────────────┐    │
│    │  3× Triangle Fold    │    │
│    │  (frequency doubler) │    │
│    └────────┬─────────────┘    │
│             │                  │
│    ┌────────▼─────────────┐    │
│    │  Sum / 4 + Noise     │◄───┘
│    │  (Pattern Brightness)│
│    └────────┬─────────────┘
│             │
├─ Input Y ──►│
│    ┌────────▼─────────────┐
│    │  proc_amp_u          │◄── Luma Gain (contrast)
│    │  contrast × input    │
│    │  + pattern brightness│
│    └────────┬─────────────┘
│             │
│    ┌────────▼─────────────┐
│    │  Luma Invert (opt.)  │
│    └────────┬─────────────┘
│             │
├─ U/V ──────►│
│    ┌────────▼─────────────┐
│    │  Desaturate (opt.)   │
│    │  U,V → 512 midpoint  │
│    └────────┬─────────────┘
│             │
│    ┌────────▼─────────────┐
│    │  Fade-to-Colour      │◄── Fade Amount, Fade Color
│    │  (interpolator_u ×3) │
│    └────────┬─────────────┘
│             │
│    ┌────────▼─────────────┐
│    │  Bypass Mux          │◄── Bypass
│    └────────┬─────────────┘
│             ▼
│        Output YUV
```

The critical interaction is the noise-to-oscillator feedback path. Noise modulates all three oscillator frequencies simultaneously, but the oscillators sweep at different spatial rates (pixel, line, frame), so the same noise field produces different turbulence textures in each dimension. The noise source selection (LFSR vs. XOR pattern) fundamentally changes the character of this modulation — LFSR produces grain-like randomness while XOR produces structured, self-referencing interference because the ramp values used in the XOR are derived from the same accumulators being modulated.

The dual noise injection paths — Noise to Phase and Noise to Luma — are independent. Noise to Phase creates spatial frequency jitter (turbulence), while Noise to Luma adds texture directly to the output brightness. Both can be active simultaneously, or either can be zeroed to isolate the other effect. The proc_amp stage then combines the spatial pattern with the input video signal: the pattern becomes the brightness offset and Luma Gain sets how strongly the input video contributes.

---

## Parameter Reference

<img src={tempest_control_panel} alt="Videomancer front panel with Tempest loaded"/>
*Videomancer's front panel with Tempest active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — H Cutoff
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the horizontal oscillator's base frequency. Higher values produce tighter horizontal spatial frequencies — more cycles of the triangle wave across the width of the screen. At zero, the horizontal oscillator is effectively frozen. Because this oscillator accumulates per pixel, even small frequency values produce visible spatial structure. The FM offset from Noise to Phase modulates this base frequency, so higher H Cutoff values make the horizontal turbulence pattern finer-grained.

---

#### Knob 2 — V Cutoff
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the vertical oscillator's base frequency. This oscillator accumulates per scan line rather than per pixel, creating horizontal stripe patterns. Combined with H Cutoff, it defines a 2D spatial lattice — equal values produce diagonal interference, and unequal values create elongated patterns. Noise modulation affects this oscillator the same way as the horizontal one, but the visual result is different because the accumulation rate is per-line.

---

#### Knob 3 — F Cutoff
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the animation (frame-rate) oscillator frequency. This oscillator accumulates once per frame, creating slow temporal evolution of the spatial pattern. At zero, the pattern is static from frame to frame. At high values, the pattern cycles rapidly, producing flickering animation. This is the primary control for making Tempest's output evolve over time rather than remaining frozen.

---

#### Knob 4 — Noise to Phase
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Noise to Phase depth — controls how strongly the noise source modulates the oscillator frequencies. At zero, the three oscillators produce clean, orderly interference patterns (standing waves, Moire lattices). As this control increases, noise pushes each pixel's local oscillator frequency away from the base value, creating spatial turbulence. At maximum, frequency modulation dominates and the geometric structure of the oscillators dissolves into chaotic storm-like textures. The FM offset is computed as (noise − 512) × depth >> 8, symmetric around zero, so bright noise pixels speed up the oscillators and dark pixels slow them down.

---

#### Knob 5 — Noise to Luma
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Noise to Luma — adds noise texture directly to the output brightness independent of the oscillator pattern. The noise is centred (subtracted by 512) and scaled by this control, then added to the combined triangle-wave pattern before clamping. At zero, the output brightness comes purely from the oscillator pattern. At maximum, the noise grit dominates. This control is independent of Noise to Phase, so you can have turbulent spatial frequencies with clean brightness, or stable frequencies with grainy brightness.

---

#### Knob 6 — Luma Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Luma Gain is the contrast input to the proc_amp stage. It controls how strongly the input video signal (from the video input connector) modulates the oscillator pattern. At zero contrast, only the spatial pattern and noise drive the output. At unity (512), the input video comes through at standard gain. At maximum, the input is amplified, combining with the pattern for high-contrast results. For pure synthesis use (no input video), this control adjusts the overall brightness scaling of the pattern.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Luma Invert** | Off | On |
| **8 — Desaturate** | Off | On |
| **9 — Noise Algo** | LFSR | Pattern |
| **10 — Fade Color** | Black | White |
| **11 — Bypass** | Off | On |

The five toggles control binary processing options at different points in the signal chain. Luma Invert and Desaturate shape the processed signal. Noise Algo selects between two fundamentally different noise character. Fade Color sets the target of the crossfade stage. Bypass routes around all processing. Note the unusual register mapping: each toggle uses its own full 10-bit register address (registers 6–10) rather than sharing bits within a single register.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Fade Amount
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Fade Amount controls the crossfade between the processed output and the solid target colour (black or white, set by Fade Color). At maximum (1023), the full processed signal passes through — oscillator pattern, noise, gain, inversion, and all. At zero, the output is solid black or white. At intermediate values, the processed pattern is partially transparent over the target, creating washed-out or silhouette effects. The interpolation is linear via the interpolator_u entity.





---

## Guided Exercises

These exercises build from static spatial patterns through animated turbulence to full noise-modulated chaos. Because Tempest is a generative synthesis program, it produces visual output from its internal oscillators — allow the animation to run for a few seconds before evaluating the pattern.

### Exercise 1: Standing Wave Interference

<img src={tempest_exercise1_result} alt="Standing Wave Interference result"/>
*Standing Wave Interference — simulated result across source images.*
**What You'll Create**: Understand how the three DDS oscillators combine to produce 2D spatial patterns, and how the H, V, and F Cutoff controls shape the interference field.

1. **Freeze animation**: Set F Cutoff to 0%. The pattern should be static.
2. **Zero noise**: Set Noise to Phase and Noise to Luma both to 0%. The oscillators should produce clean geometric patterns.
3. **Horizontal stripes**: Set H Cutoff to ~50%, V Cutoff to 0%. Observe vertical stripe patterns from the horizontal oscillator alone.
4. **Add vertical**: Increase V Cutoff to ~50%. Horizontal stripes appear and combine with the vertical, forming a plaid-like lattice.
5. **Diagonal interference**: Set both H and V Cutoff to the same value. The triangle waves create diamond-shaped interference.
6. **Animate**: Slowly increase F Cutoff. The pattern begins to evolve over time as the frame-rate oscillator adds a third dimension.

**Key concepts**: Three DDS oscillators sweep at pixel, line, and frame rates. Triangle folding creates smooth spatial gradients. Equal H and V frequencies create diagonal interference. F Cutoff controls animation speed.

---

### Exercise 2: FM Turbulence

<img src={tempest_exercise2_result} alt="FM Turbulence result"/>
*FM Turbulence — simulated result across source images.*
**What You'll Create**: Explore how noise-to-phase modulation transforms orderly interference into turbulent storm-like textures.

1. **Start clean**: Use the standing wave pattern from Exercise 1 (H and V Cutoff ~50%, no noise).
2. **LFSR turbulence**: Slowly increase Noise to Phase from 0%. Watch the clean lattice begin to shimmer and distort as noise jitters the oscillator frequencies.
3. **Maximum chaos**: Push Noise to Phase to ~80%. The geometric pattern dissolves into turbulent spatial noise.
4. **Switch to Pattern mode**: Toggle Noise Algo to Pattern. The turbulence character changes from grain-like randomness to structured, self-referencing interference.
5. **Add luma noise**: Increase Noise to Luma to ~60% alongside the phase noise. The output gains visible textural grain on top of the spatial turbulence.
6. **Animate**: Set F Cutoff to ~25%. The turbulent pattern now evolves over time.

**Key concepts**: FM modulation creates sideband complexity from simple oscillators. LFSR produces organic grain; XOR pattern produces geometric feedback. Noise to Phase and Noise to Luma are independent injection paths. Animation adds temporal evolution.

---

### Exercise 3: Fade and Inversion Sculpting

<img src={tempest_exercise3_result} alt="Fade and Inversion Sculpting result"/>
*Fade and Inversion Sculpting — simulated result across source images.*
**What You'll Create**: Use the fade-to-colour crossfade and luma inversion to shape the turbulent output into contrasting visual treatments.

1. **Establish turbulence**: Set H Cutoff ~40%, V Cutoff ~30%, Noise to Phase ~60%, F Cutoff ~15%.
2. **Fade to black**: Lower Fade Amount to ~50%. The pattern becomes semi-transparent over black, creating a dark atmospheric effect.
3. **Switch to white**: Toggle Fade Color to White. The same fade now washes the pattern toward bright white — the visual character reverses entirely.
4. **Invert**: Toggle Luma Invert. The bright peaks become dark valleys against the fade target, creating a negative-image effect.
5. **Desaturate off**: If using with input video, disable Desaturate to allow colour through. With pure synthesis, the chroma channels remain neutral.
6. **Full fade sweep**: Slowly sweep Fade Amount from 0% to 100% to see the full range of the crossfade. At the extremes, the pattern vanishes into solid colour; in the middle, it creates translucent overlay textures.

**Key concepts**: Fade Amount crossfades linearly between processed and solid target. Fade Color selects the target (black or white). Luma Invert reverses the pattern after processing. These controls sculpt the final tonal range of the turbulence output.

---


## Tips

- **Fade Amount is a density control**: Rather than thinking of it as a volume knob, use Fade Amount to control how much of the turbulent pattern is visible against the solid background.
- **F Cutoff animates slowly**: Because the frame oscillator accumulates once per frame (not per pixel), even high F Cutoff values produce relatively slow temporal evolution. This is intentional — the animation should breathe, not strobe.
- **Luma Gain with live video**: When processing input video, Luma Gain controls how much the source modulates the turbulence. Low gain = pure synthesis; high gain = video shows through the pattern.
- **Feedback routing**: Send Tempest's output back to its input for recursive turbulence. The proc_amp re-processes the already-turbulent signal, creating fractal-like self-similar structures.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDS** | Direct Digital Synthesis; a method of generating waveforms by incrementing a phase accumulator at a rate determined by a frequency word. |
| **FM** | Frequency Modulation; modulating the frequency of one signal with another to create complex sidebands and timbral variation. |
| **Frequency Doubler** | A waveshaping module that folds a sawtooth ramp into a triangle wave by mirroring the upper half, doubling the apparent frequency. |
| **Frequency Word** | The value added to a DDS phase accumulator on each clock cycle; determines the output frequency. |
| **LFSR** | Linear Feedback Shift Register; a hardware-efficient pseudo-random number generator using XOR feedback of selected bit positions. |
| **Moire** | An interference pattern produced when two periodic patterns overlap at slightly different frequencies or angles. |
| **Phase Accumulator** | A register that wraps around at a fixed modulus, producing a periodic ramp waveform; the core of any DDS oscillator. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies contrast (multiplication) and brightness (addition) to a video signal. |
| **Triangle Wave** | A periodic waveform that rises and falls linearly, creating smooth spatial gradients without the abrupt discontinuity of a sawtooth. |
| **Turbulence** | In this context, spatial frequency distortion caused by noise-modulating the oscillator DDS — analogous to atmospheric turbulence distorting light. |
| **XOR** | Exclusive OR; a bitwise operation where corresponding bits differ produces 1, creating structured spatial interference patterns when applied to ramp waves. |

---
