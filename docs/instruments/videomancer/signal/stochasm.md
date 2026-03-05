---
draft: true
sidebar_position: 291
slug: /instruments/videomancer/stochasm
title: "Stochasm"
image: /img/instruments/videomancer/stochasm/stochasm_hero_s1.png
description: "In most signal processing contexts, noise is the enemy — an unwanted corruption that obscures the signal you are trying to preserve."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import stochasm_control_panel from '/img/instruments/videomancer/stochasm/stochasm_control_panel.png';
import stochasm_source1_field from '/img/instruments/videomancer/stochasm/stochasm_source1_field.png';
import stochasm_source2_car from '/img/instruments/videomancer/stochasm/stochasm_source2_car.png';
import stochasm_source3_clouds from '/img/instruments/videomancer/stochasm/stochasm_source3_clouds.png';
import stochasm_source4_pattern from '/img/instruments/videomancer/stochasm/stochasm_source4_pattern.png';
import stochasm_source5_boy from '/img/instruments/videomancer/stochasm/stochasm_source5_boy.png';
import stochasm_source6_paint from '/img/instruments/videomancer/stochasm/stochasm_source6_paint.png';
import stochasm_hero_s1 from '/img/instruments/videomancer/stochasm/stochasm_hero_s1.png';
import stochasm_hero_s2 from '/img/instruments/videomancer/stochasm/stochasm_hero_s2.png';
import stochasm_hero_s3 from '/img/instruments/videomancer/stochasm/stochasm_hero_s3.png';
import stochasm_hero_s4 from '/img/instruments/videomancer/stochasm/stochasm_hero_s4.png';
import stochasm_hero_s5 from '/img/instruments/videomancer/stochasm/stochasm_hero_s5.png';
import stochasm_hero_s6 from '/img/instruments/videomancer/stochasm/stochasm_hero_s6.png';
import stochasm_ex1_s1 from '/img/instruments/videomancer/stochasm/stochasm_ex1_s1.png';
import stochasm_ex1_s2 from '/img/instruments/videomancer/stochasm/stochasm_ex1_s2.png';
import stochasm_ex1_s3 from '/img/instruments/videomancer/stochasm/stochasm_ex1_s3.png';
import stochasm_ex1_s4 from '/img/instruments/videomancer/stochasm/stochasm_ex1_s4.png';
import stochasm_ex1_s5 from '/img/instruments/videomancer/stochasm/stochasm_ex1_s5.png';
import stochasm_ex1_s6 from '/img/instruments/videomancer/stochasm/stochasm_ex1_s6.png';
import stochasm_ex2_s1 from '/img/instruments/videomancer/stochasm/stochasm_ex2_s1.png';
import stochasm_ex2_s2 from '/img/instruments/videomancer/stochasm/stochasm_ex2_s2.png';
import stochasm_ex2_s3 from '/img/instruments/videomancer/stochasm/stochasm_ex2_s3.png';
import stochasm_ex2_s4 from '/img/instruments/videomancer/stochasm/stochasm_ex2_s4.png';
import stochasm_ex2_s5 from '/img/instruments/videomancer/stochasm/stochasm_ex2_s5.png';
import stochasm_ex2_s6 from '/img/instruments/videomancer/stochasm/stochasm_ex2_s6.png';
import stochasm_ex3_s1 from '/img/instruments/videomancer/stochasm/stochasm_ex3_s1.png';
import stochasm_ex3_s2 from '/img/instruments/videomancer/stochasm/stochasm_ex3_s2.png';
import stochasm_ex3_s3 from '/img/instruments/videomancer/stochasm/stochasm_ex3_s3.png';
import stochasm_ex3_s4 from '/img/instruments/videomancer/stochasm/stochasm_ex3_s4.png';
import stochasm_ex3_s5 from '/img/instruments/videomancer/stochasm/stochasm_ex3_s5.png';
import stochasm_ex3_s6 from '/img/instruments/videomancer/stochasm/stochasm_ex3_s6.png';

# Stochasm

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: stochasm_source1_field, after: stochasm_hero_s1 },
    { label: "Car", before: stochasm_source2_car, after: stochasm_hero_s2 },
    { label: "Clouds", before: stochasm_source3_clouds, after: stochasm_hero_s3 },
    { label: "Pattern", before: stochasm_source4_pattern, after: stochasm_hero_s4 },
    { label: "Boy", before: stochasm_source5_boy, after: stochasm_hero_s5 },
    { label: "Paint", before: stochasm_source6_paint, after: stochasm_hero_s6 },
  ]}
/>
*Stochasm applying multi-stage stochastic resonance to extract sub-threshold signal features through controlled noise injection.*

---

## Overview

In most signal processing contexts, noise is the enemy — an unwanted corruption that obscures the signal you are trying to preserve. Stochastic resonance turns this on its head. Under carefully tuned conditions, adding noise to a weak signal actually *improves* the ability to detect it. Stochasm implements this counter-intuitive phenomenon as a real-time video processing pipeline with up to eight cascaded threshold comparators, each fed by independent LFSR noise generators.

The program decomposes each pixel's brightness (and optionally chroma) into a series of binary decisions: is the signal-plus-noise above or below a given threshold? The outputs of these comparators are weighted and summed to reconstruct a quantised version of the input. The name *Stochasm* fuses *stochastic* (governed by probability) with *chasm* — the gap between signal and threshold that noise bridges.

At low noise amplitudes with few stages, Stochasm applies gentle threshold-based quantisation. As you increase the noise amplitude and stage count, the visual texture shifts from clean posterisation to granular, film-grain-like surfaces. With temporal correlation enabled, the noise becomes frame-to-frame persistent, producing a stippled, etched quality that follows the tonal structure of the source.

---

## Quick Start

1. **Match noise to spacing**: The stochastic resonance sweet spot occurs when the noise amplitude is roughly equal to the spacing between adjacent thresholds. Start with both at ~30% and fine-tune from there.
2. **Signed noise for symmetry**: Signed mode produces zero-mean dither that preserves the average brightness of the source. Unsigned mode adds a positive bias — useful for intentionally shifting the threshold response upward.
3. **Temporal correlation for texture**: Without correlation, the noise flickers every pixel — energetic but visually busy. Enabling correlation creates a stable stipple pattern that reads as a textured surface rather than random grain.

---

## Background

### Stochastic Resonance

Stochastic resonance was first described in the context of paleoclimatology — researchers observed that periodic ice-age cycles could be explained by weak orbital forcing amplified by climatic noise. The principle has since been found in neurobiology (neurons detect sub-threshold stimuli with noise), electronics (dithering in ADCs), and signal processing. The core requirement is a nonlinear threshold: without the threshold, noise simply degrades the signal. With it, noise pushes sub-threshold signals across the detection boundary, creating a measurable response where none existed before.

### Threshold Comparators and Cascading

A single threshold comparator produces a 1-bit output: above or below. This captures the gross structure of a signal but discards all amplitude detail within each region. By arranging multiple comparators at evenly spaced thresholds, you create an *N*-level flash ADC-like structure — each comparator captures a different brightness band. Stochasm's cascade of up to eight comparators reconstructs an 8-level quantised representation of the input, with the spacing between threshold levels controlled by the Spacing parameter.

### Linear Feedback Shift Registers

The noise source in Stochasm is a Galois LFSR — a shift register with XOR feedback taps chosen for maximal sequence length. A 10-bit LFSR with polynomial x¹⁰ + x⁷ + 1 produces a pseudo-random sequence of 1023 values before repeating. Three independent LFSRs with different seeds provide decorrelated noise for Y, U, and V channels when Per-Channel Noise mode is active. In Shared mode, a single LFSR drives all three channels, producing spatially correlated noise textures.

### Noise Scaling and Signed Representation

The raw LFSR output is a 10-bit unsigned integer. Stochasm scales it using a shift-and-add multiplier approximation — the top three bits of the Noise Amp register select combinations of half, quarter, and eighth of the raw noise value. In Signed mode, the scaled noise is centered around zero by subtracting half the amplitude, producing symmetric ±N dither. In Unsigned mode, the noise is a positive bias that shifts the entire signal upward, creating asymmetric thresholding.

### Temporal Correlation

When Correlation is above midpoint, Stochasm blends each noise sample 50/50 with the previous sample. This creates autocorrelated noise — consecutive samples are related rather than independent. Visually, the noise pattern becomes temporally smooth, producing a stippled texture that persists across frames rather than the flickering grain of uncorrelated noise. This is analogous to colored noise in audio processing.


---

## Signal Flow

Input Register → Noise Scaling → Threshold Computation → ... → Final Weighted Sum → Invert + Output

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + LFSR Noise Capture ─────────────
│   ├─ Register Y, U, V input samples
│   └─ Capture raw LFSR outputs (shared or per-channel)
│
├── Stage 2: Noise Scaling + Temporal Correlation ────────────
│   ├─ Shift-add multiply: noise × amplitude (top 3 bits)
│   ├─ Signed conversion (optional: center around zero)
│   └─ Temporal blend: 50/50 with previous noise if active
│
├── Stage 3: Threshold Computation ───────────────────────────
│   └─ 8 parallel thresholds: base + i × (spacing / 8)
│       with saturation at 1023
│
├── Stage 4: Cascade Comparison + Step Pre-computation ───────
│   ├─ For each stage i: (signal + noise) >= threshold(i)?
│   ├─ Inactive stages (i >= active_stages) get step = 0
│   └─ Weight mode: equal steps (1023/N) or decaying (1023>>i)
│
├── Stage 5: Partial Weighted Sum (stages 0–3) ───────────────
│   └─ Accumulate step values for active comparators
│
├── Stage 6: Final Weighted Sum (stages 4–7) + Clamp ────────
│   ├─ Add remaining stage contributions
│   ├─ Clamp to 10-bit range [0, 1023]
│   └─ Luma-only: pass original U/V unchanged
│
├── Stage 7: Invert + Output ─────────────────────────────────
│   └─ Optional bitwise complement of Y (and U/V if not luma-only)
│
├── Mix (4 clk interpolator) ─────────────────────────────────
│   └─ Wet/dry crossfade: dry × (1 − mix) + wet × mix
│
└── Bypass Mux ───────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical interaction is between noise amplitude, threshold spacing, and stage count. When noise amplitude roughly matches the spacing between adjacent thresholds, each comparator has a probability of firing that is proportional to the signal's proximity to its threshold — this is the resonance sweet spot. Too little noise and the quantisation is harsh; too much noise and the output dissolves into randomness. The Weight control shifts between equal-step reconstruction (uniform quantisation) and exponentially decaying steps that emphasise the lower comparators, producing a compressive transfer curve.

---

## Parameter Reference

<img src={stochasm_control_panel} alt="Videomancer front panel with Stochasm loaded"/>
*Videomancer's front panel with Stochasm active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the base comparator threshold for the first stage of the cascade. All subsequent thresholds are derived from this base plus multiples of the spacing step. At 0%, the first threshold sits at black level — virtually all signal passes. At 100%, the base threshold is at full white — only the brightest pixels with sufficient noise can exceed the first comparator. The base threshold determines the overall brightness offset of the quantised output.

---

#### Knob 2 — Spacing
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the spacing between adjacent threshold levels in the cascade. When spacing is zero, all eight comparators sit at the same threshold and produce identical outputs — the cascade collapses to a single threshold. As spacing increases, the thresholds fan out across the dynamic range, creating wider quantisation bands. The spacing interacts directly with the noise amplitude: when the spacing matches the noise standard deviation, stochastic resonance is strongest.

---

#### Knob 3 — Noise Amp
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the amplitude of LFSR noise injected into the signal before each comparator. This is the primary stochastic resonance control. At zero, the cascade operates as a clean multi-level quantiser. At moderate levels, sub-threshold features are probabilistically promoted past their nearest comparator, revealing detail that clean thresholding suppresses. At extreme levels, the noise overwhelms the signal and the output becomes dominated by random texture.

---

#### Knob 4 — Stages
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

Selects how many cascade stages are active, from 1 to 8. With one stage, the output is a simple 1-bit threshold (above or below). Each additional stage adds a quantisation level, progressively refining the tonal resolution. More stages also mean more interaction with the noise — with eight stages and moderate noise, the output develops a complex granular texture as pixels randomly cross multiple threshold boundaries.

---

#### Knob 5 — Weight
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the weighting curve for the cascade output reconstruction. Below midpoint, all active stages contribute equal step values — the quantisation levels are uniformly spaced (1023/N per stage). Above midpoint, each successive stage contributes half the previous stage's step value, creating an exponentially decaying weighting curve. The decaying mode compresses the tonal range, emphasising the lowest threshold levels.

---

#### Knob 6 — Correlation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the temporal correlation of the noise. Below midpoint, each noise sample is fully independent — the texture flickers rapidly between frames. Above midpoint, each sample is a 50/50 blend of the current LFSR output and the previous sample, producing a temporally smoothed noise pattern. The correlated mode creates a stable, etched texture that persists across frames.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Per-Ch Noise** | Shared | Indep. |
| **8 — Noise Sign** | Unsigned | Signed |
| **9 — Luma Only** | All Ch. | Y Only |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control independent binary options that shape the character of the noise, its distribution across channels, and the output signal path. None of the toggles interact combinatorially with each other — each enables or disables a distinct processing option.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original input signal and the processed output. At 0%, only the original signal is present. At 100%, only the processed signal is output. Intermediate values blend the two, allowing subtle noise texturing over the original image.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Stochasm processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from basic threshold quantisation to full stochastic resonance texturing, building familiarity with how noise amplitude, threshold spacing, and stage count interact.

### Exercise 1: Single-Stage Threshold

<BeforeAfterSlider
  sources={[
    { label: "Field", before: stochasm_source1_field, after: stochasm_ex1_s1 },
    { label: "Car", before: stochasm_source2_car, after: stochasm_ex1_s2 },
    { label: "Clouds", before: stochasm_source3_clouds, after: stochasm_ex1_s3 },
    { label: "Pattern", before: stochasm_source4_pattern, after: stochasm_ex1_s4 },
    { label: "Boy", before: stochasm_source5_boy, after: stochasm_ex1_s5 },
    { label: "Paint", before: stochasm_source6_paint, after: stochasm_ex1_s6 },
  ]}
/>
*Single-Stage Threshold — simulated result across source images.*
**Source**: A live camera feed or recorded footage with smooth tonal gradients — sky, skin tones, or gradient test patterns.

**What You'll Create**: Understand the basic threshold comparator mechanism and how noise modifies its behaviour.

1. **Clean threshold**: Set Stages to 1, Noise Amp to 0%. The output is a hard 1-bit black/white threshold controlled by the Threshold knob. Sweep Threshold across the range and watch sections of the image snap between black and white.
2. **Add noise**: Slowly increase Noise Amp. Watch the hard threshold edge become probabilistic — pixels near the boundary begin flickering between black and white. This is stochastic resonance at its simplest.
3. **Signed vs. unsigned**: Toggle Noise Sign (Switch 8). Observe how unsigned noise shifts the effective threshold downward, while signed noise creates symmetric dithering around the threshold.
4. **Temporal smoothing**: Enable Correlation (Knob 6 above 50%). The flickering noise pattern becomes stable across frames — a frozen stipple texture.

**Key concepts**: A single threshold creates 1-bit quantisation, noise widens the transition zone probabilistically, signed noise is symmetric while unsigned is biased

---

### Exercise 2: Multi-Stage Quantisation

<BeforeAfterSlider
  sources={[
    { label: "Field", before: stochasm_source1_field, after: stochasm_ex2_s1 },
    { label: "Car", before: stochasm_source2_car, after: stochasm_ex2_s2 },
    { label: "Clouds", before: stochasm_source3_clouds, after: stochasm_ex2_s3 },
    { label: "Pattern", before: stochasm_source4_pattern, after: stochasm_ex2_s4 },
    { label: "Boy", before: stochasm_source5_boy, after: stochasm_ex2_s5 },
    { label: "Paint", before: stochasm_source6_paint, after: stochasm_ex2_s6 },
  ]}
/>
*Multi-Stage Quantisation — simulated result across source images.*
**Source**: Footage with a wide dynamic range — outdoor scenes with highlights and shadows, or a greyscale ramp test pattern.

**What You'll Create**: Explore how cascaded thresholds reconstruct a quantised signal and how noise affects multi-level quantisation.

1. **Four stages**: Set Stages to 4, Spacing to ~50%. The output now has four brightness levels. Adjust Threshold to centre the quantisation range on the image content.
2. **Resonance tuning**: Increase Noise Amp slowly from 0%. Watch the hard quantisation boundaries soften — intermediate values appear as noise pushes pixels across adjacent thresholds.
3. **Eight stages**: Increase Stages to 8. The tonal resolution improves. Note how the noise texture becomes finer as each comparator responds to a narrower signal band.
4. **Weight curve**: Toggle the Weight knob above midpoint. The weighting shifts from uniform to exponentially decaying — the lower stages dominate, compressing the output range.
5. **Per-channel noise**: Enable Per-Ch Noise (Switch 7). The noise texture gains chromatic variation as each channel receives decorrelated dither.

**Key concepts**: Threshold spacing determines quantisation band width, noise amplitude should roughly match spacing for optimal resonance, weight curve controls tonal compression

---

### Exercise 3: Stochastic Texture Synthesis

<BeforeAfterSlider
  sources={[
    { label: "Field", before: stochasm_source1_field, after: stochasm_ex3_s1 },
    { label: "Car", before: stochasm_source2_car, after: stochasm_ex3_s2 },
    { label: "Clouds", before: stochasm_source3_clouds, after: stochasm_ex3_s3 },
    { label: "Pattern", before: stochasm_source4_pattern, after: stochasm_ex3_s4 },
    { label: "Boy", before: stochasm_source5_boy, after: stochasm_ex3_s5 },
    { label: "Paint", before: stochasm_source6_paint, after: stochasm_ex3_s6 },
  ]}
/>
*Stochastic Texture Synthesis — simulated result across source images.*
**Source**: Any footage, especially material with subtle tonal variations — underwater footage, cloud formations, or fabric textures.

**What You'll Create**: Combine all parameters to create controlled stochastic textures that reveal sub-threshold structures in the source material.

1. **Full cascade**: Set Stages to 8, Spacing ~40%, Threshold ~20%.
2. **Resonance sweep**: Increase Noise Amp to ~40%. The output should show a granular reconstruction of the source with visible stochastic texture.
3. **Temporal persistence**: Increase Correlation above 50%. The flickering noise freezes into a stable stipple pattern.
4. **Luma-only processing**: Enable Luma Only (Switch 9). The stochastic texture is confined to brightness variations while chrominance stays smooth.
5. **Inversion**: Toggle Invert (Switch 10) for a solarised, high-contrast result. The quantisation levels reverse — dark areas become bright band graphics.
6. **Blend**: Lower the Mix fader to ~60% to layer the stochastic texture over the original image as a subtle overlay.

**Key concepts**: Stochastic resonance reveals structure hidden below the noise floor, temporal correlation converts flicker to texture, luma-only processing preserves colour fidelity

---


## Tips

- **Luma-only for subtlety**: Applying stochastic resonance only to the Y channel preserves the original colour information while adding monochromatic texture — a useful mode for overlaying grain on clean footage.
- **Weight curve for tone**: The exponentially decaying weight mode creates a nonlinear brightness response — useful for producing dark, moody images where only the brightest features survive.
- **Feedback loops**: Route Stochasm's output back to its input for recursive stochastic resonance. The cascade progressively re-quantises its own output, creating evolving textures that settle into periodic attractors.
- **Stage count shapes granularity**: One stage = hard threshold. Eight stages = fine-grain quantisation with noise. Use intermediate values to control the coarseness of the stochastic texture.
- **Bypass for A/B**: Switch 11 instantly shows the unprocessed signal for direct comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **Cascade** | A series of identical processing stages connected in sequence, where each stage's decision contributes to the final output. |
| **Comparator** | A circuit that produces a binary (1-bit) output: high if the input exceeds a threshold, low otherwise. |
| **Dither** | Small noise added to a signal before quantisation to break up banding and create the appearance of additional tonal levels. |
| **Galois LFSR** | A type of linear feedback shift register where XOR gates are placed in the data path between register stages, producing pseudo-random sequences. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function (XOR) of its previous state, generating a pseudo-random binary sequence. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage for brightness and contrast adjustment. |
| **Quantisation** | Mapping a continuous range of values to a smaller set of discrete levels. |
| **Stochastic Resonance** | A phenomenon where adding noise to a sub-threshold signal improves its detection by a nonlinear system (threshold comparator). |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
