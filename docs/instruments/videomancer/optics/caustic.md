---
draft: true
sidebar_position: 38
slug: /instruments/videomancer/caustic
title: "Caustic"
image: /img/instruments/videomancer/caustic/caustic_hero.png
description: "Program guide for Caustic, a Videomancer optics program for the LZX video synthesizer."
---

import caustic_hero from '/img/instruments/videomancer/caustic/caustic_hero.png';
import caustic_before_after from '/img/instruments/videomancer/caustic/caustic_before_after.png';
import caustic_control_panel from '/img/instruments/videomancer/caustic/caustic_control_panel.png';
import caustic_exercise1_result from '/img/instruments/videomancer/caustic/caustic_exercise1_result.png';
import caustic_exercise2_result from '/img/instruments/videomancer/caustic/caustic_exercise2_result.png';
import caustic_exercise3_result from '/img/instruments/videomancer/caustic/caustic_exercise3_result.png';

# Caustic

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={caustic_hero} alt="Caustic hero image"/>
*Caustic refracting input video through simulated water surface ripples, creating luminous interference patterns.*
<img src={caustic_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Caustic applied.*

---

## Overview

Light passing through a disturbed water surface doesn't spread evenly — it focuses into bright caustic lines where refracted rays converge, leaving darker regions where they diverge. The result is the shimmering network of bright curves you see on the bottom of a swimming pool. Caustic recreates this phenomenon digitally, using dual-axis sinusoidal ripple functions to modulate the brightness of input video.

The program generates two orthogonal ripple patterns — one along the horizontal axis, one along the vertical — and combines them through interference. The resulting pattern multiplies the input luminance, creating bright nodes where ripple peaks coincide and dark valleys where they cancel. Animation advances the ripple phase per frame, producing the characteristic slow drift of underwater caustics.

At subtle settings, Caustic adds a gentle luminous shimmer to any video source. At extreme amplitude and frequency, the input is transformed into a pulsating grid of bright nodal points connected by thin caustic lines.

---

## Background

### What Are Caustics?

In optics, a caustic is the envelope of light rays reflected or refracted by a curved surface. The term comes from the Greek *kaustikos* ("burning") because caustic curves can concentrate enough light energy to ignite materials. The most familiar examples are the bright dancing curves on the bottom of a swimming pool and the bright line focused by a drinking glass on a table. Mathematically, caustics occur where the Jacobian of the ray-mapping function has zero determinant — points where the mapping from surface to projected plane folds over itself.

### Dual-Axis Ripple Interference

Caustic's ripple engine uses the simplest model of a disturbed water surface: two perpendicular sinusoidal waves. Each wave contributes a position-dependent phase offset that, when combined and folded through a triangle wave, creates the characteristic bright-line network. The interference pattern of two orthogonal sine waves produces a grid-like caustic pattern whose density and brightness distribution depend on the frequency and amplitude ratios.

### Triangle Wave Folding

Rather than using a true sine lookup table, which would require BRAM, the VHDL implementation folds the combined position-plus-phase value through a triangle wave function. The triangle wave approximation creates sharper caustic lines than a pure sinusoid, which actually better matches real-world caustic patterns where light focuses into thin bright curves rather than broad smooth undulations.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Ripple Generator ───────────────────────────────────────────
│   ├─ 1. H-Ripple Phase       (x_pos × frequency + frame_offset)
│   ├─ 2. V-Ripple Phase       (y_pos × frequency + frame_offset)
│   ├─ 3. XOR Fold             (combine axes via bitwise XOR)
│   └─ 4. Triangle Wave        (fold combined phase to triangle)
│
├── Y Channel ──────────────────────────────────────────────────
│   ├─ 5. Amplitude Scale      (triangle × amplitude register)
│   ├─ 6. Brightness Multiply  (scaled_ripple × input_Y)
│   └─ 7. Depth Blend          (mix between modulated and original)
│
├── U/V Channels ───────────────────────────────────────────────
│   └─ 8. Optional Chroma Mod  (ripple applied to U/V when Color on)
│
├── Output Stage ───────────────────────────────────────────────
│   └─ 9. Interpolator Mix     (3× interpolator_u wet/dry)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select processed or original signal
```

The XOR fold at stage 3 is the key to the caustic pattern. By XOR-ing the horizontal and vertical ripple phases, the resulting interference creates the characteristic diamond-grid caustic network. The triangle wave conversion at stage 4 sharpens the peaks, concentrating brightness into thin lines. The Depth control blends between the fully modulated signal and the original, allowing subtle caustic overlay without completely reshaping the input luminance.

---

## Parameter Reference

<img src={caustic_control_panel} alt="Videomancer front panel with Caustic loaded"/>
*Videomancer's front panel with Caustic active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Frequency
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the spatial frequency of the ripple pattern. Low values produce widely-spaced caustic lines with large bright zones between them. High values create a dense mesh of fine caustic lines. The frequency applies equally to both horizontal and vertical ripple axes, so the caustic grid maintains square symmetry.

---

#### Knob 2 — Amplitude
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scales the amplitude of the ripple modulation. At zero, no caustic pattern is visible — the input passes through unchanged. At maximum, the brightness modulation is extreme: caustic peaks become very bright while valleys become very dark. This controls the contrast of the caustic pattern overlaid on the source video.

---

#### Knob 3 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the animation speed when the Animate toggle is enabled. Higher values advance the ripple phase faster per frame, creating rapidly shifting caustic patterns. Lower values produce a slow, meditative drift. At zero with animation enabled, the pattern updates very slowly.

---

#### Knob 4 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

Master brightness offset applied after the ripple modulation. This lifts or lowers the overall output level. At mid-range, the caustic pattern modulates symmetrically around the input brightness. Higher values bias the output brighter; lower values create a darker overall image with only the caustic peaks reaching full brightness.

---

#### Knob 5 — Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the depth of the caustic effect by blending between the fully modulated signal and the unmodified input. At zero, the caustic pattern has minimal effect. At maximum, the full ripple modulation is applied. This is distinct from Amplitude — Depth controls how much of the modulated signal mixes with the original, while Amplitude controls the strength of the modulation itself.

---

#### Knob 6 — Sharpness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Sharpens or softens the caustic line pattern. Higher values create thinner, more defined caustic lines with sharper transitions between bright and dark. Lower values produce broader, softer undulations. This control adjusts the power curve applied to the triangle wave output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Color** | Off | On |
| **9 — Overlay** | Off | On |
| **10 — Reflect** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control animation, color processing, overlay mode, reflection symmetry, and bypass. Animate and Color are the most frequently used — together they control whether the pattern moves and whether it affects chroma channels.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry mix between the caustic-processed signal and the original input. At 100%, the full caustic effect is applied. At 0%, the original signal passes through unchanged. Intermediate values blend the two proportionally.

---

## Guided Exercises

These exercises progress from subtle luminous textures to intense caustic transformations, exploring the interplay between frequency, amplitude, and animation.

### Exercise 1: Gentle Pool Shimmer

<img src={caustic_exercise1_result} alt="Gentle Pool Shimmer result"/>
*Gentle Pool Shimmer — simulated result across source images.*
**Source**: Footage of a face or still life with smooth tonal gradients.

**Objective**: Add subtle underwater caustic shimmer to a video source.

1. Set Frequency to about 30% for widely-spaced caustic lines.
2. Set Amplitude to about 25% for gentle modulation.
3. Enable Animate (Switch 7) and set Speed to about 20%.
4. Set Depth to about 40% to blend subtly with the source.
5. Keep Color off for luminance-only modulation.
6. Observe the slow drift of bright caustic curves across the image.

**Key concepts**: Low frequency produces broad caustic patterns, moderate depth preserves source detail, animation speed controls the meditative quality of the shimmer

---

### Exercise 2: Dense Caustic Grid

<img src={caustic_exercise2_result} alt="Dense Caustic Grid result"/>
*Dense Caustic Grid — simulated result across source images.*
**Source**: High-contrast footage or geometric patterns.

**Objective**: Create a dense interference grid that strongly reshapes the input.

1. Increase Frequency to about 70% for a fine caustic mesh.
2. Set Amplitude to about 80% for strong modulation.
3. Set Depth to about 90%.
4. Enable Color (Switch 8) to add chroma modulation.
5. Set Speed to about 50% for moderate animation.
6. Enable Reflect (Switch 10) for symmetric patterns.

**Key concepts**: High frequency creates fine-mesh caustic networks, color modulation adds chromatic dispersion, reflection symmetry creates kaleidoscopic structure

---

### Exercise 3: Static Texture Overlay

<img src={caustic_exercise3_result} alt="Static Texture Overlay result"/>
*Static Texture Overlay — simulated result across source images.*
**Source**: Any video source — the caustic becomes a fixed texture layer.

**Objective**: Use static caustic patterns as a repeatable texture overlay.

1. Disable Animate (Switch 7) — pattern freezes.
2. Set Frequency to about 50%.
3. Set Amplitude to about 40%.
4. Switch to Overlay mode (Switch 9).
5. Adjust Sharpness to control line definition.
6. Sweep Frequency slowly to find a pleasing static pattern.
7. Use Mix fader to dial in the texture intensity.

**Key concepts**: Static mode freezes the caustic as a fixed overlay, overlay blend preserves source detail, frequency selects the texture scale

---


## Tips

- **Frequency sets the mood**: Low frequency = dreamy underwater; high frequency = crystalline lattice.
- **Depth before amplitude**: Use Depth to set how much caustic you want, then use Amplitude for the modulation intensity within that blend.
- **Overlay mode preserves shadows**: In overlay mode, dark areas of the source remain dark while mid-tones and highlights get the caustic pattern.
- **Static patterns as textures**: Turn off Animate to use caustics as fixed overlay textures on any source.
- **Color adds chromatic dispersion**: Enable Color to simulate the slight spectral splitting that real water caustics exhibit.
- **Sharpness for line quality**: Higher sharpness creates the thin bright lines of shallow-water caustics; lower sharpness gives deep-water softness.

---

## Glossary

| Term | Definition |
|------|------------|
| **Amplitude** | The peak-to-peak strength of a wave; controls the contrast between bright caustic lines and dark valleys. |
| **Caustic** | An envelope of light rays focused by refraction or reflection through a curved surface, creating bright concentrated lines. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interference** | The combination of two or more wave patterns, producing reinforcement at some points and cancellation at others. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Triangle Wave** | A periodic waveform that rises and falls linearly, approximating a sine wave with sharper transitions. |
| **XOR** | Exclusive OR; a bitwise operation that combines two patterns, producing a 1 where inputs differ and 0 where they match. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
