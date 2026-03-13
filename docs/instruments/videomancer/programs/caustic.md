---
draft: true
sidebar_position: 41
slug: /instruments/videomancer/caustic
title: "Caustic"
image: /img/instruments/videomancer/caustic/caustic_hero_s1.png
description: "Light passing through a disturbed water surface doesn't spread evenly — it focuses into bright caustic lines where refracted rays converge, leaving darker regions where they diverge."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import caustic_control_panel from '/img/instruments/videomancer/caustic/caustic_control_panel.png';
import caustic_source1_house from '/img/instruments/videomancer/caustic/caustic_source1_house.png';
import caustic_source2_skull from '/img/instruments/videomancer/caustic/caustic_source2_skull.png';
import caustic_source3_clouds from '/img/instruments/videomancer/caustic/caustic_source3_clouds.png';
import caustic_source4_pattern from '/img/instruments/videomancer/caustic/caustic_source4_pattern.png';
import caustic_source5_man from '/img/instruments/videomancer/caustic/caustic_source5_man.png';
import caustic_source6_wood from '/img/instruments/videomancer/caustic/caustic_source6_wood.png';
import caustic_hero_s1 from '/img/instruments/videomancer/caustic/caustic_hero_s1.png';
import caustic_hero_s2 from '/img/instruments/videomancer/caustic/caustic_hero_s2.png';
import caustic_hero_s3 from '/img/instruments/videomancer/caustic/caustic_hero_s3.png';
import caustic_hero_s4 from '/img/instruments/videomancer/caustic/caustic_hero_s4.png';
import caustic_hero_s5 from '/img/instruments/videomancer/caustic/caustic_hero_s5.png';
import caustic_hero_s6 from '/img/instruments/videomancer/caustic/caustic_hero_s6.png';
import caustic_ex1_s1 from '/img/instruments/videomancer/caustic/caustic_ex1_s1.png';
import caustic_ex1_s2 from '/img/instruments/videomancer/caustic/caustic_ex1_s2.png';
import caustic_ex1_s3 from '/img/instruments/videomancer/caustic/caustic_ex1_s3.png';
import caustic_ex1_s4 from '/img/instruments/videomancer/caustic/caustic_ex1_s4.png';
import caustic_ex1_s5 from '/img/instruments/videomancer/caustic/caustic_ex1_s5.png';
import caustic_ex1_s6 from '/img/instruments/videomancer/caustic/caustic_ex1_s6.png';
import caustic_ex2_s1 from '/img/instruments/videomancer/caustic/caustic_ex2_s1.png';
import caustic_ex2_s2 from '/img/instruments/videomancer/caustic/caustic_ex2_s2.png';
import caustic_ex2_s3 from '/img/instruments/videomancer/caustic/caustic_ex2_s3.png';
import caustic_ex2_s4 from '/img/instruments/videomancer/caustic/caustic_ex2_s4.png';
import caustic_ex2_s5 from '/img/instruments/videomancer/caustic/caustic_ex2_s5.png';
import caustic_ex2_s6 from '/img/instruments/videomancer/caustic/caustic_ex2_s6.png';
import caustic_ex3_s1 from '/img/instruments/videomancer/caustic/caustic_ex3_s1.png';
import caustic_ex3_s2 from '/img/instruments/videomancer/caustic/caustic_ex3_s2.png';
import caustic_ex3_s3 from '/img/instruments/videomancer/caustic/caustic_ex3_s3.png';
import caustic_ex3_s4 from '/img/instruments/videomancer/caustic/caustic_ex3_s4.png';
import caustic_ex3_s5 from '/img/instruments/videomancer/caustic/caustic_ex3_s5.png';
import caustic_ex3_s6 from '/img/instruments/videomancer/caustic/caustic_ex3_s6.png';

# Caustic

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "House", before: caustic_source1_house, after: caustic_hero_s1 },
    { label: "Skull", before: caustic_source2_skull, after: caustic_hero_s2 },
    { label: "Clouds", before: caustic_source3_clouds, after: caustic_hero_s3 },
    { label: "Pattern", before: caustic_source4_pattern, after: caustic_hero_s4 },
    { label: "Man", before: caustic_source5_man, after: caustic_hero_s5 },
    { label: "Wood", before: caustic_source6_wood, after: caustic_hero_s6 },
  ]}
/>
*Caustic refracting input video through simulated water surface ripples, creating luminous interference patterns.*

---

## Overview

Light passing through a disturbed water surface doesn't spread evenly — it focuses into bright caustic lines where refracted rays converge, leaving darker regions where they diverge. The result is the shimmering network of bright curves you see on the bottom of a swimming pool. Caustic recreates this phenomenon digitally, using dual-axis sinusoidal ripple functions to modulate the brightness of input video.

The program generates two orthogonal ripple patterns — one along the horizontal axis, one along the vertical — and combines them through interference. The resulting pattern multiplies the input luminance, creating bright nodes where ripple peaks coincide and dark valleys where they cancel. Animation advances the ripple phase per frame, producing the characteristic slow drift of underwater caustics.

At subtle settings, Caustic adds a gentle luminous shimmer to any video source. At extreme amplitude and frequency, the input is transformed into a pulsating grid of bright nodal points connected by thin caustic lines.

---

## Quick Start

1. **Frequency sets the mood**: Low frequency = dreamy underwater; high frequency = crystalline lattice.
2. **Depth before amplitude**: Use Depth to set how much caustic you want, then use Amplitude for the modulation intensity within that blend.
3. **Overlay mode preserves shadows**: In overlay mode, dark areas of the source remain dark while mid-tones and highlights get the caustic pattern.

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

Ripple Generator → Y Channel → U/V Channels → Output Stage → Bypass

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

At zero, no caustic pattern is visible — the input passes through unchanged. At maximum, the brightness modulation is extreme: caustic peaks become very bright while valleys become very dark. This controls the contrast of the caustic pattern overlaid on the source video. Internally, scales the amplitude of the ripple modulation.

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

At zero, the caustic pattern has minimal effect. At maximum, the full ripple modulation is applied. This is distinct from Amplitude — Depth controls how much of the modulated signal mixes with the original, while Amplitude controls the strength of the modulation itself. Internally, controls the depth of the caustic effect by blending between the fully modulated signal and the unmodified input.

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


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Caustic processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises progress from subtle luminous textures to intense caustic transformations, exploring the interplay between frequency, amplitude, and animation.

### Exercise 1: Gentle Pool Shimmer

<BeforeAfterSlider
  sources={[
    { label: "House", before: caustic_source1_house, after: caustic_ex1_s1 },
    { label: "Skull", before: caustic_source2_skull, after: caustic_ex1_s2 },
    { label: "Clouds", before: caustic_source3_clouds, after: caustic_ex1_s3 },
    { label: "Pattern", before: caustic_source4_pattern, after: caustic_ex1_s4 },
    { label: "Man", before: caustic_source5_man, after: caustic_ex1_s5 },
    { label: "Wood", before: caustic_source6_wood, after: caustic_ex1_s6 },
  ]}
/>
*Gentle Pool Shimmer — simulated result across source images.*
**Source**: Footage of a face or still life with smooth tonal gradients.

**What You'll Create**: Add subtle underwater caustic shimmer to a video source.

1. Set Frequency to about 30% for widely-spaced caustic lines.
2. Set Amplitude to about 25% for gentle modulation.
3. Enable Animate (Switch 7) and set Speed to about 20%.
4. Set Depth to about 40% to blend subtly with the source.
5. Keep Color off for luminance-only modulation.
6. Observe the slow drift of bright caustic curves across the image.

**Key concepts**: Low frequency produces broad caustic patterns, moderate depth preserves source detail, animation speed controls the meditative quality of the shimmer

---

### Exercise 2: Dense Caustic Grid

<BeforeAfterSlider
  sources={[
    { label: "House", before: caustic_source1_house, after: caustic_ex2_s1 },
    { label: "Skull", before: caustic_source2_skull, after: caustic_ex2_s2 },
    { label: "Clouds", before: caustic_source3_clouds, after: caustic_ex2_s3 },
    { label: "Pattern", before: caustic_source4_pattern, after: caustic_ex2_s4 },
    { label: "Man", before: caustic_source5_man, after: caustic_ex2_s5 },
    { label: "Wood", before: caustic_source6_wood, after: caustic_ex2_s6 },
  ]}
/>
*Dense Caustic Grid — simulated result across source images.*
**Source**: High-contrast footage or geometric patterns.

**What You'll Create**: Create a dense interference grid that strongly reshapes the input.

1. Increase Frequency to about 70% for a fine caustic mesh.
2. Set Amplitude to about 80% for strong modulation.
3. Set Depth to about 90%.
4. Enable Color (Switch 8) to add chroma modulation.
5. Set Speed to about 50% for moderate animation.
6. Enable Reflect (Switch 10) for symmetric patterns.

**Key concepts**: High frequency creates fine-mesh caustic networks, color modulation adds chromatic dispersion, reflection symmetry creates kaleidoscopic structure

---

### Exercise 3: Static Texture Overlay

<BeforeAfterSlider
  sources={[
    { label: "House", before: caustic_source1_house, after: caustic_ex3_s1 },
    { label: "Skull", before: caustic_source2_skull, after: caustic_ex3_s2 },
    { label: "Clouds", before: caustic_source3_clouds, after: caustic_ex3_s3 },
    { label: "Pattern", before: caustic_source4_pattern, after: caustic_ex3_s4 },
    { label: "Man", before: caustic_source5_man, after: caustic_ex3_s5 },
    { label: "Wood", before: caustic_source6_wood, after: caustic_ex3_s6 },
  ]}
/>
*Static Texture Overlay — simulated result across source images.*
**Source**: Any video source — the caustic becomes a fixed texture layer.

**What You'll Create**: Use static caustic patterns as a repeatable texture overlay.

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
| **Interference** | The combination of two or more wave patterns, producing reinforcement at some points and cancellation at others. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Triangle Wave** | A periodic waveform that rises and falls linearly, approximating a sine wave with sharper transitions. |
| **XOR** | Exclusive OR; a bitwise operation that combines two patterns, producing a 1 where inputs differ and 0 where they match. |

---
