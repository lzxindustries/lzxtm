---
draft: true
sidebar_position: 128
slug: /instruments/videomancer/intermod
title: "Intermod"
image: /img/instruments/videomancer/intermod/intermod_hero.png
description: "Program guide for Intermod, a Videomancer signal program for the LZX video synthesizer."
---

import intermod_before_after from '/img/instruments/videomancer/intermod/intermod_before_after.png';
import intermod_control_panel from '/img/instruments/videomancer/intermod/intermod_control_panel.png';
import intermod_exercise1_result from '/img/instruments/videomancer/intermod/intermod_exercise1_result.png';
import intermod_exercise2_result from '/img/instruments/videomancer/intermod/intermod_exercise2_result.png';
import intermod_exercise3_result from '/img/instruments/videomancer/intermod/intermod_exercise3_result.png';
import intermod_hero from '/img/instruments/videomancer/intermod/intermod_hero.png';
import intermod_source1_kodim15 from '/img/instruments/videomancer/intermod/intermod_source1_kodim15.png';
import intermod_source2_kodim01 from '/img/instruments/videomancer/intermod/intermod_source2_kodim01.png';
import intermod_source3_stream_bridge_512 from '/img/instruments/videomancer/intermod/intermod_source3_stream_bridge_512.png';

# Intermod

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={intermod_hero} alt="Intermod hero image"/>
*Intermod applying polynomial non-linear distortion with cross-channel coupling to produce overdriven harmonic textures and saturated color artifacts.*
<img src={intermod_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Intermod applied.*

---

## Overview

Analog amplifiers do not clip gracefully. Push a signal beyond the linear range of a transistor stage and the output bends — gently at first, then hard. The bending creates new frequency components that were never in the original signal. These unwanted harmonics and sum/difference tones are called intermodulation distortion, and they are the reason overdriven guitar amps sound fat and broken speakers sound terrible. Intermod brings this effect to video.

The program models a polynomial non-linear transfer function with separately adjustable second-order (square-law) and third-order (cube-law) distortion stages. Second-order distortion produces even harmonics and a DC shift; third-order distortion produces odd harmonics and the characteristic gain compression of a saturating amplifier. A cross-coupling control mixes the luminance channel into the chrominance channels before the non-linearity, creating intermodulation products between Y, U, and V that generate metallic color shifts and iridescent artifacts impossible to achieve with single-channel processing.

An asymmetry offset shifts the DC operating point before the non-linearity, affecting the balance between positive and negative distortion products. Hard clip truncates the signal at the rails; soft clip uses a shift-based approximation of hyperbolic tangent saturation for a smoother roll-off. Feedback re-injects the output into the next sample's input, creating cumulative distortion that can range from gentle thickening to chaotic self-oscillation. Rectify folds the negative excursion of the centered signal upward, and invert flips the entire output. A luma-only toggle restricts processing to the Y channel, leaving chrominance untouched.

---

## Background

### Intermodulation Distortion in Electronics

When two or more signals pass through a non-linear device — a vacuum tube, a transistor amplifier, a diode mixer — they interact to produce sum and difference frequencies called intermodulation products. In audio, these products are what give a distorted guitar its "thickness" and a clipping preamp its "grunge." For video, the three YUV channels act as the multiple signals, and the polynomial non-linearity creates cross-products between brightness and color that would never occur in a linear system. The 2nd and 3rd order controls in Intermod are named after the standard characterization of amplifier non-linearity in RF engineering.

### Square-Law and Cube-Law Transfer Functions

A square-law device produces an output proportional to the square of the input: $y = x^2$. This generates even harmonics (2nd, 4th, 6th...) and creates a DC offset because $x^2$ is always positive. A cube-law device produces $y = x^3$, generating odd harmonics (3rd, 5th, 7th...) and preserving the sign of the input. Real amplifiers exhibit a combination of both. Intermod applies each independently with adjustable weighting: the 2nd Order knob scales the square product and the 3rd Order knob scales the cube product, letting you dial in even harmonics, odd harmonics, or both.

### Cross-Channel Coupling

In a linear video system, Y, U, and V are independent. Cross-coupling deliberately breaks this independence by multiplying the luminance signal with each chrominance channel before applying the non-linearity. The result is a set of intermodulation products ($Y \times U$, $Y \times V$) that shift colors in ways dependent on brightness — dark areas shift differently from bright areas. This produces metallic, holographic, or solarized color effects that cannot be achieved by processing Y, U, and V separately.

### Hard Clip vs. Soft Saturation

When a signal exceeds the representable range [0, 1023], the system must decide what to do with the excess. Hard clipping simply truncates: anything above 1023 becomes 1023, anything below 0 becomes 0. This creates sharp discontinuities and aggressive visual artifacts. Soft saturation compresses the excess instead of removing it — the VHDL implements this as $1023 - (excess \gg 2)$ for overflow and $excess \gg 2$ for underflow, which folds the out-of-range signal back toward the rails with decreasing slope. The result resembles the smooth saturation curve of a vacuum tube.

### Temporal Feedback in Video

Feedback in audio creates echo, reverb, and oscillation. In single-sample video feedback (as opposed to frame-buffer feedback), the output of one pixel calculation is mixed into the input of the next pixel calculation along the scan line. Because video is scanned left-to-right, top-to-bottom, this creates a directional smearing effect where distortion accumulates across the line. At high feedback levels, the system can self-oscillate, producing chaotic patterns that run across the screen.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y/U/V Channels ─────────────────────────────────────────────
│   │
│   ├─ 1. Center + Drive Gain        (subtract 512, apply gain curve;
│   │      └─ + Feedback injection     add scaled feedback from stage 5)
│   │
│   ├─ 2. Square-Law (2nd Order)      (x² shift-multiply per channel)
│   │
│   ├─ 3. Cube-Law (3rd Order)        (x³ shift-multiply per channel
│   │      └─ + Cross-Coupling         Y×U and Y×V intermod products)
│   │
│   ├─ 4. Weighted Accumulate         (linear + 2nd_ord×sq + 3rd_ord×cb
│   │      └─ + Asymmetry Offset       + cross_couple×xp + DC bias)
│   │
│   ├─ 5. Clip + Re-center            (hard clip or soft saturation
│   │      └─ → Feedback state update   → back to unsigned [0, 1023])
│   │
│   ├─ 6. Rectify / Invert + Output   (abs fold or bitwise complement;
│   │      └─ Luma-only passthrough     optional UV bypass)
│   │
│   └─ 7. Interpolator Mix            (4-clock wet/dry crossfade)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline (10 clocks)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline operates in a signed domain: input values are centered around zero by subtracting 512, which converts the unsigned 10-bit range [0, 1023] into a signed range [−512, +511]. All non-linear operations (square, cube, cross-products) operate on these centered values using a shift-multiply function that computes $(a \times b) \gg 10$ in 12-bit signed arithmetic. After the weighted accumulation in stage 4, the signal is re-centered by adding 512 back and then clipped or soft-saturated to fit [0, 1023]. Feedback operates at the drive stage, injecting the previous output sample (from stage 5) scaled by the feedback parameter — this means feedback accumulates horizontally along each scan line.

---

## Parameter Reference

<img src={intermod_control_panel} alt="Videomancer front panel with Intermod loaded"/>
*Videomancer's front panel with Intermod active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Drive
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the input gain applied before any non-linear processing. The drive curve has four regions: below 25% the signal is attenuated by half (shift right 1), 25–50% is unity gain, 50–75% applies 1.5× gain (input plus half), and above 75% applies 2× gain (shift left 1). Higher drive pushes more of the signal into the non-linear region of the square-law and cube-law stages, dramatically increasing visible distortion. At low drive settings, even aggressive 2nd and 3rd Order controls produce only subtle wavering.

---

#### Knob 2 — 2nd Order
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the weighting of the second-order (square-law) distortion product. The squared signal is multiplied by this parameter (scaled by a 10-bit right shift) and added to the linear signal in stage 4. Even harmonics from the square law produce a characteristic brightness shift and asymmetric waveform clipping. At zero the square-law path is silent; at maximum it dominates the output, pushing the signal toward a half-wave-rectified shape with strong DC offset. Combined with high drive, this creates aggressive posterized edges.

---

#### Knob 3 — 3rd Order
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the weighting of the third-order (cube-law) distortion product. The cubed signal preserves the sign of the input — peaks become sharper while the zero crossing is preserved — producing odd harmonics and the gain compression characteristic of tube amplifiers. At moderate levels this adds a warm, thickened quality. At high levels the cube-law generates sharp cusps and foldover artifacts. Third-order distortion interacts multiplicatively with drive: doubling the drive roughly octuples the cube product.

---

#### Knob 4 — X-Couple
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the cross-channel coupling strength. At zero, Y, U, and V are processed independently. As the knob increases, the luma channel is multiplied into U and V before the weighted accumulation, creating intermodulation products that shift color based on brightness. Low settings produce subtle iridescent color shifts on edges; high settings create dramatic hue rotations and metallic chromatic artifacts. Cross-coupling is applied only in stage 3 and only affects the chrominance channels — luma receives only its own distortion products.

---

#### Knob 5 — Asymmetry
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Applies a signed DC offset to the signal before clipping. At 50% (512) the offset is zero. Below 50% the signal is shifted negative; above 50% it is shifted positive. This asymmetry control biases the operating point of the non-linearity, affecting which polarity of the signal clips first. A positive asymmetry produces more clipping on bright peaks; a negative asymmetry clips dark troughs first. Combined with rectify, asymmetry determines whether the rectified output is bright-biased or dark-biased.

---

#### Knob 6 — Feedback
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the amount of temporal feedback injected into the drive stage. The previous output (from stage 5's clipped accumulator) is scaled by this parameter and added to the current input at stage 1. Below a threshold of approximately 6% (register value 64) feedback is disabled entirely. Low feedback values produce a subtle scan-line smear; moderate values create visible horizontal trailing; high values drive the system toward self-oscillation with chaotic patterns that propagate across the scan line. Feedback interacts strongly with drive and distortion order — even small amounts of feedback at high drive levels can produce dramatic results.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Luma Only** | All Ch. | Y Only |
| **8 — Clip Mode** | Hard | Soft |
| **9 — Rectify** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles provide signal routing and post-processing options. Luma Only restricts all distortion processing to the Y channel, passing U and V through unmodified — useful for adding harmonic texture to brightness without disturbing color. Clip Mode selects between hard clipping (sharp digital truncation) and soft saturation (smooth compression of excess signal). Rectify folds the bottom half of the signal upward, creating a full-wave rectification effect. Invert flips the entire output. Bypass disables all processing. Rectify and invert are mutually exclusive on the Y channel — if rectify is active, invert is suppressed for luma (but applies normally to chroma when not in luma-only mode).

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the original video signal and the distorted output. At 0% the output is entirely the dry (original) signal; at 100% the output is entirely the wet (distorted) signal. Intermediate positions blend the distorted signal over the original, which is useful for adding subtle harmonic texture without fully replacing the source. The mix is implemented via three parallel `interpolator_u` instances — one per Y/U/V channel.

---

## Guided Exercises

These exercises demonstrate the range of Intermod's distortion character, from subtle analog warmth to aggressive harmonic destruction and cross-channel color mutation.

### Exercise 1: Warm Tube Overdrive

<img src={intermod_exercise1_result} alt="Warm Tube Overdrive result"/>
*Warm Tube Overdrive — simulated result across source images.*
**Source**: A portrait or talking-head shot with smooth skin tones and moderate contrast.

**Objective**: Add subtle second-order harmonic warmth to the luminance channel without disturbing color, simulating a gently overdriven tube amplifier stage.

1. Enable luma-only mode (Toggle 7 = Y Only) to protect color.
2. Set Drive (Pot 1) to 55% for slight gain above unity.
3. Raise 2nd Order (Pot 2) to 40% for moderate even-harmonic content.
4. Keep 3rd Order (Pot 3) at 0% — no odd harmonics for this warm tone.
5. Set X-Couple (Pot 4) to 0% — not needed in luma-only mode.
6. Set Asymmetry (Pot 5) to 50% (center, no DC offset).
7. Select soft clip (Toggle 8 = Soft) for smooth saturation.
8. Set Mix (Fader) to 70% to blend the harmonic texture with the original.

**Key concepts**: Even-harmonic distortion, soft saturation, luma-only processing, wet/dry blending.

---

### Exercise 2: Metallic Color Shred

<img src={intermod_exercise2_result} alt="Metallic Color Shred result"/>
*Metallic Color Shred — simulated result across source images.*
**Source**: A high-contrast scene with saturated colors — neon signs, painted surfaces, or colorful textiles.

**Objective**: Create aggressive intermodulation artifacts with metallic, iridescent color shifts using cross-channel coupling and cube-law distortion.

1. Process all channels (Toggle 7 = All Ch.).
2. Set Drive (Pot 1) to 80% for aggressive 2× gain.
3. Set 2nd Order (Pot 2) to 50%.
4. Set 3rd Order (Pot 3) to 70% for dominant odd harmonics and gain compression.
5. Raise X-Couple (Pot 4) to 60% for strong Y→UV intermodulation.
6. Set Asymmetry (Pot 5) to 65% for positive bias — clips brights first.
7. Select hard clip (Toggle 8 = Hard) for sharp digital edges.
8. Set Mix (Fader) to 100%.

**Key concepts**: Cross-channel intermodulation, cube-law odd harmonics, hard clipping, asymmetric bias.

---

### Exercise 3: Self-Oscillating Chaos

<img src={intermod_exercise3_result} alt="Self-Oscillating Chaos result"/>
*Self-Oscillating Chaos — simulated result across source images.*
**Source**: Any source — at high feedback the input material is largely destroyed by self-oscillation. A static graphic or test pattern helps visualize the feedback propagation direction.

**Objective**: Push the processor into chaotic self-oscillation using maximum feedback, creating horizontal interference patterns that evolve across the scan line.

1. Process all channels (Toggle 7 = All Ch.).
2. Set Drive (Pot 1) to 70%.
3. Set 2nd Order (Pot 2) to 30% and 3rd Order (Pot 3) to 30% for moderate non-linearity.
4. Set X-Couple (Pot 4) to 40% for moderate cross-feed.
5. Set Asymmetry (Pot 5) to 50% (centered).
6. Raise Feedback (Pot 6) to 85% — high enough for sustained oscillation.
7. Enable rectify (Toggle 9 = On) to fold negative excursions, adding visual complexity.
8. Set Mix (Fader) to 100%.
9. Slowly sweep Drive from 50% to 100% and observe the oscillation evolve from trailing streaks to fully chaotic patterns.

**Key concepts**: Temporal feedback, self-oscillation, scan-line propagation, rectification adding harmonic density.

---


## Tips

- **Start with Drive:** Distortion intensity is primarily controlled by drive. Set 2nd and 3rd Order first, then adjust drive to taste — small drive changes have large effects on distortion visibility.
- **Use luma-only for texture:** When you want harmonic grit without color mutation, enable Y Only mode. This preserves the original color palette while adding edge emphasis and tonal compression.
- **Soft clip for analog feel:** Soft saturation is more forgiving and less prone to banding artifacts. Use hard clip when you specifically want sharp digital edges.
- **Cross-coupling needs saturated source:** The Y×U and Y×V products are most visible with colorful source material. Monochrome sources have near-zero U/V so cross-coupling has little effect.
- **Feedback accumulates horizontally:** Remember that single-sample feedback creates a left-to-right propagation effect because of the scan-line order. Vertical structures in the image create horizontal smearing.
- **Asymmetry biases clipping:** Shifting asymmetry off-center determines which polarity clips first. Use this to create intentionally bright-biased or dark-biased distortion.
- **Rectify doubles frequency:** Full-wave rectification folds negative excursions upward, effectively doubling the spatial frequency of brightness variations. Combine with moderate 3rd-order for complex waveform shapes.
- **Mix for parallel distortion:** Blending the distorted signal with the clean original at 30–50% creates a parallel distortion effect — harmonic content is added without fully replacing the clean signal.
