---
draft: true
sidebar_position: 180
slug: /instruments/videomancer/nimbus
title: "Nimbus"
image: /img/instruments/videomancer/nimbus/nimbus_hero.png
description: "Program guide for Nimbus, a Videomancer weather program for the LZX video synthesizer."
---

import nimbus_before_after from '/img/instruments/videomancer/nimbus/nimbus_before_after.png';
import nimbus_control_panel from '/img/instruments/videomancer/nimbus/nimbus_control_panel.png';
import nimbus_exercise1_result from '/img/instruments/videomancer/nimbus/nimbus_exercise1_result.png';
import nimbus_exercise2_result from '/img/instruments/videomancer/nimbus/nimbus_exercise2_result.png';
import nimbus_exercise3_result from '/img/instruments/videomancer/nimbus/nimbus_exercise3_result.png';
import nimbus_hero from '/img/instruments/videomancer/nimbus/nimbus_hero.png';
import nimbus_source1_kodim01 from '/img/instruments/videomancer/nimbus/nimbus_source1_kodim01.png';
import nimbus_source2_kodim02 from '/img/instruments/videomancer/nimbus/nimbus_source2_kodim02.png';
import nimbus_source3_stream_bridge_512 from '/img/instruments/videomancer/nimbus/nimbus_source3_stream_bridge_512.png';

# Nimbus

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={nimbus_hero} alt="Nimbus hero image"/>
*Nimbus dividing a video frame into cloud-like horizontal strata with warm tonal compression and altitude-dependent desaturation.*
<img src={nimbus_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Nimbus applied.*

---

## Overview

In the early 1820s, the English painter John Constable devoted two summers to painting nothing but clouds over Hampstead Heath — small oil sketches that recorded the layered, stratified structure of cumulus and cumulonimbus formations. Nimbus takes that observation and turns it into a real-time video operation. It divides the frame into three to seven horizontal strata (cloud layers), applies distinct tonal transforms within each band, perturbs the boundaries with LFSR-driven noise, and drifts the entire formation vertically over time.

The name is taken from *cumulonimbus*, the towering cloud genus that rises through multiple atmospheric layers. Each stratum receives its own luminance compression range and chrominance tint, drawn from either a warm palette (Constable's dark gray base rising to bright white summit) or a cool palette (Turner's blue-gray tones). The boundaries between strata billow and undulate via an IIR-smoothed noise source, and a DDS phase accumulator scrolls the entire stratum set up or down the frame at a speed controlled by the Drift Spd knob.

At conservative settings — few strata, low turbulence, warm palette — Nimbus creates gentle, horizontal tonal banding that evokes cloud layers at altitude. At extreme settings — seven strata, high turbulence, hard edges, cool palette with full summit glow — it produces sharp, billowing bands of desaturated blue-gray that slice across the video like weather fronts.

---

## Background

### Horizontal Stratification

Nimbus works by classifying every scanline into a stratum index. The frame is divided into evenly-spaced horizontal zones, and each pixel's vertical position determines which stratum it belongs to. This is a purely spatial classification — no line buffers or BRAM tiles are needed. The number of strata (3–7) is selected by the Strata knob, which maps the 10-bit pot value across five discrete steps. The comparator chain walks the boundary array and assigns the highest matching stratum index.

### LFSR Boundary Perturbation

The stratum boundaries are not straight lines. A 16-bit linear feedback shift register advances once per scanline, producing a pseudo-random sequence. This raw noise is fed through an IIR low-pass filter (first-order, α = 1/8) that smooths the per-line variations into gentle, slowly-varying undulations. The smoothed noise is then scaled by the Turbulence knob and added to each boundary position. When Hard Edge is enabled, the IIR filter is bypassed and boundaries reset to straight lines.

### DDS Vertical Drift

A direct digital synthesis phase accumulator increments (or decrements) once per frame by an amount proportional to the Drift Spd knob. The upper bits of the accumulator produce a signed vertical offset that shifts all boundary positions up or down the frame. Over time, the strata scroll past the camera like cloud layers drifting across the sky. The Drift Dir toggle selects rising or sinking motion.

### Per-Stratum Tonal Mapping

Each stratum has a pre-defined luminance range (y_min to y_max) and a chrominance tint (u_tint, v_tint). The VHDL stores two complete palettes — warm and cool — as constant arrays of seven stratum records. For each pixel, the input luminance is compressed into the selected stratum's range, scaled by the Contrast knob. The chrominance channels are blended toward the stratum's tint color, controlled by the Warmth knob. Lower strata are darker and more tinted; upper strata are brighter and closer to neutral.

### Altitude Desaturation and Summit Glow

At the final processing stage, the stratum index itself drives a desaturation fraction. Higher strata (larger index) are pulled more aggressively toward neutral chrominance, simulating the washed-out appearance of high-altitude cloud tops. Simultaneously, the Summit Glow knob boosts the luminance of upper strata, creating a bright rim on the topmost cloud layer. Both effects scale with stratum index × the Summit Glow pot value.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   └─ h_count, v_count (from hsync/vsync edges)
│
├── LFSR Noise ─────────────────────────────────────────────────
│   └─ 16-bit LFSR → IIR smooth (α=1/8) → s_smooth_noise
│      (Hard Edge → bypass IIR, noise = 0)
│
├── DDS Drift ──────────────────────────────────────────────────
│   └─ 16-bit accumulator ± drift_speed per frame → s_drift_offset
│
├── Boundary Computation (per scanline) ────────────────────────
│   └─ base = (i+1) × 720 / (num_strata+1)
│      boundary(i) = clamp(base + turbulence×noise + drift_offset)
│
├── Stage 1: Stratum Classification ────────────────────────────
│   └─ Compare v_count against boundary array → stratum_idx
│      (Invert toggle → reverse index order)
│
├── Stage 2: Tonal Mapping ─────────────────────────────────────
│   ├─ Y: compress [0,1023] → [y_min, y_max] × contrast
│   ├─ U: blend input → stratum u_tint by warmth
│   └─ V: blend input → stratum v_tint by warmth
│
├── Stage 3: Altitude Desaturation + Summit Glow ───────────────
│   ├─ UV: pull toward 512 by (stratum_idx × summit_glow)
│   └─ Y: boost by (stratum_idx × summit_glow)
│
├── Interpolator (4 clocks) ────────────────────────────────────
│   └─ lerp(dry, wet, mix_amount) per Y, U, V
│
└── Output Mux ─────────────────────────────────────────────────
    └─ Bypass=Off → interpolator result
       Bypass=On  → delayed dry signal
```

The key architectural feature is that boundary computation happens once per scanline — the LFSR advances and the boundary array is recalculated at every horizontal sync edge — while the tonal mapping pipeline runs per pixel. This means the stratum boundaries shift from line to line (creating the undulating cloud-edge effect), but within a single scanline every pixel sees the same boundary set and the classification is purely vertical. The turbulence perturbation and DDS drift offset are additive to the evenly-spaced base positions, so the strata maintain roughly equal width even as they billow.

The two palettes (warm and cool) are stored as constant arrays in the VHDL. Each palette has seven entries with distinct Y ranges and UV tints, grading from dark and subtly tinted at index 0 to bright and near-neutral at index 6. The Palette toggle selects which array is read. The warm palette (Constable-inspired) has faint pink-orange tints in lower strata; the cool palette (Turner-inspired) has blue-shifted tints throughout.

---

## Parameter Reference

<img src={nimbus_control_panel} alt="Videomancer front panel with Nimbus loaded"/>
*Videomancer's front panel with Nimbus active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Drift Spd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the vertical drift speed of the stratum set. The DDS accumulator adds this value once per frame. At 0%, the strata are stationary. As the value increases, the cloud layers scroll up or down the frame at increasing speed. The drift direction is set by the Drift Dir toggle. Because the accumulator is 16 bits and only the upper bits are used as offset, the motion is smooth and continuous even at low speeds.

---

#### Knob 2 — Strata
| Property | Value |
|----------|-------|
| Range | 3 – 7 |
| Default | 5 |

Selects the number of horizontal strata dividing the frame. The pot is decoded as a steps_8 control mapping to five discrete values: 3, 4, 5, 6, or 7 strata. Fewer strata produce wide, dramatic tonal bands with large boundary undulations. More strata create finer layering with narrower bands. The boundary positions are calculated as evenly-spaced divisions of the 720 active lines.

---

#### Knob 3 — Turbulence
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls the amplitude of LFSR noise added to the stratum boundaries. At 0%, boundaries are straight horizontal lines (or zero, if Hard Edge is enabled). As the value increases, the IIR-smoothed noise drives larger excursions in the boundary positions, creating billowing, cloud-like undulations. The noise is multiplied by this pot value before being added to each boundary, so the perturbation scales linearly with the control.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scales the luminance compression range within each stratum. Each stratum defines a y_min and y_max; the contrast pot controls what fraction of that range is used. At full value, the input luminance is mapped across the entire stratum range. At lower values, the mapped range narrows, producing flatter, more compressed tonal bands. This affects only luminance — chrominance tinting is independent.

---

#### Knob 5 — Warmth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the chrominance tint blending strength. Each stratum has a predefined UV tint (warm amber or cool blue-gray, depending on the palette). The warmth pot controls how strongly the input chrominance is pulled toward that tint. At 0%, the original color is preserved. At full value, the chrominance is fully replaced by the stratum's tint color. Intermediate values produce a proportional blend.

---

#### Knob 6 — Summit Glow
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls two coupled altitude effects simultaneously. First, it scales the desaturation applied to upper strata — higher stratum indices have their chrominance pulled more aggressively toward neutral (512). Second, it adds a luminance boost to upper strata, creating a bright glow on the topmost cloud layer. Both effects are proportional to (stratum_index × pot value), so lower strata are unaffected regardless of the setting.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Warm | Cool |
| **8 — Drift Dir** | Rise | Sink |
| **9 — Invert** | Off | On |
| **10 — Hard Edge** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options. Palette and Drift Dir select from two-valued parameters; Invert reverses the stratum ordering; Hard Edge disables the IIR noise smoother; Bypass routes the original signal directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input (delayed to match pipeline latency) and the processed output. At 0% (value 0), the output is fully dry — unprocessed video. At 100% (value 1023), the output is fully wet — stratified and tinted. The interpolator performs linear interpolation: `output = dry + (wet - dry) × mix / 1023`.

---

## Guided Exercises

These exercises progress from simple stratification to full atmospheric compositing. Each introduces additional controls while building on the spatial classification concept.

### Exercise 1: Basic Cloud Strata

<img src={nimbus_exercise1_result} alt="Basic Cloud Strata result"/>
*Basic Cloud Strata — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and varied tonal range.

**Objective**: Understand how horizontal strata divide the frame and apply distinct tonal treatments.

1. Set Mix to 100% to hear only the wet signal. Set Strata to the center position (5 strata).
2. Start with Turbulence at 0, Contrast at ~50%, Warmth at ~30%. Observe five distinct horizontal bands with different brightness ranges.
3. Slowly increase Turbulence. Watch the band boundaries begin to undulate as LFSR noise perturbs them.
4. Toggle Palette between Warm and Cool. Observe the chrominance shift in lower strata — warm pink-amber vs. cool blue-gray.
5. Increase Warmth to 100% to see the full tint effect in each band.

**Key concepts**: Vertical position determines stratum membership, each stratum has a unique luminance range and chrominance tint, turbulence perturbs boundary positions via smoothed LFSR noise

---

### Exercise 2: Drifting Atmosphere

<img src={nimbus_exercise2_result} alt="Drifting Atmosphere result"/>
*Drifting Atmosphere — simulated result across source images.*
**Source**: Static or slow-moving footage — landscapes, skylines, or abstract color fields.

**Objective**: Explore vertical drift animation and altitude desaturation effects.

1. Begin from Exercise 1 settings. Turn on Summit Glow to ~60%.
2. Observe the upper strata becoming brighter and more desaturated — the summit glow effect.
3. Now increase Drift Spd to ~25%. Watch the strata scroll upward across the frame.
4. Toggle Drift Dir to Sink. The strata reverse, scrolling downward.
5. Increase Drift Spd further. At high speeds, the strata sweep rapidly like weather fronts.
6. Toggle Invert. The bright summit stratum appears at the bottom instead of the top.

**Key concepts**: DDS phase accumulator provides smooth continuous drift, summit glow couples desaturation and brightness boost to stratum index, invert reverses the altitude gradient

---

### Exercise 3: Sharp Fronts and Full Atmosphere

<img src={nimbus_exercise3_result} alt="Sharp Fronts and Full Atmosphere result"/>
*Sharp Fronts and Full Atmosphere — simulated result across source images.*
**Source**: High-contrast footage — performers against a dark background, architectural details, or video feedback.

**Objective**: Combine all parameters to create a complex atmospheric effect with hard-edged strata and full tonal treatment.

1. Set Strata to maximum (7 strata) for fine layering. Set Hard Edge On for sharp boundaries.
2. Switch to Cool palette and set Warmth to ~80%. The frame divides into sharp blue-gray bands.
3. Increase Contrast to ~80% for strong tonal compression within each band.
4. Enable Summit Glow at ~70%. Upper strata wash out to bright near-white.
5. Add moderate Drift Spd (~30%) and set Drift Dir to Sink for descending weather fronts.
6. Toggle Hard Edge Off. The sharp boundaries soften into undulating cloud edges.
7. Lower Mix to ~60% to blend the atmospheric effect with the original video.

**Key concepts**: Hard Edge disables IIR smoothing for sharp vs. soft boundaries, 7 strata with high contrast create dramatic tonal segmentation, mix fader blends the atmospheric treatment with the source

---


## Tips

- **Fewer strata, wider bands**: Three strata produce dramatic, wide tonal divisions. Seven strata produce fine atmospheric layering. Start with 5 and adjust.
- **Turbulence needs Hard Edge Off**: The IIR smoothing is disabled when Hard Edge is On, so Turbulence has no visible effect in that mode — boundaries stay straight.
- **Summit Glow is altitude-dependent**: It only affects upper strata. With Invert On, the "summit" moves to the top of the frame, changing which part of the image glows.
- **Drift Spd at zero for static compositing**: Disable drift for a fixed stratification that you can tune precisely with turbulence and contrast.
- **Mix as final creative control**: Blend the atmospheric effect with the original at 40–60% for subtle cloud layering over recognizable video content.
- **Warm palette for portraiture**: The warm palette's lower strata have gentle amber tints well-suited to skin tones and warm-lit scenes.
- **Cool palette for landscapes**: The cool palette's blue-gray tints evoke overcast skies and maritime atmospheres.
- **Feedback loops**: Routing Nimbus output back to its input creates recursive stratification — each pass subdivides the existing bands into new layers.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory within the FPGA. Nimbus uses zero BRAM tiles. |
| **Chrominance** | The color information (U and V channels) in a YUV video signal. |
| **DDS** | Direct Digital Synthesis; a phase accumulator technique for generating smooth, frequency-controlled periodic signals. |
| **IIR** | Infinite Impulse Response; a recursive digital filter. Nimbus uses a first-order IIR to smooth LFSR noise. |
| **LFSR** | Linear Feedback Shift Register; a hardware-efficient pseudo-random number generator. |
| **Luminance** | The brightness component (Y) of a YUV video signal. |
| **Stratum** | A single horizontal band in the stratification. Each stratum has its own tonal range and chrominance tint. |
| **YUV** | A color encoding separating brightness (Y) from color (U, V), used throughout the Videomancer pipeline. |
