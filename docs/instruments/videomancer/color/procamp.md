---
draft: true
sidebar_position: 237
slug: /instruments/videomancer/procamp
title: "Procamp"
image: /img/instruments/videomancer/procamp/procamp_hero_s1.png
description: "Every broadcast facility has a processing amplifier — a \"proc amp\" — sitting between source and destination, adjusting signal levels so that everything arriving downstream is correctly calibrated."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import procamp_control_panel from '/img/instruments/videomancer/procamp/procamp_control_panel.png';
import procamp_source1_castle from '/img/instruments/videomancer/procamp/procamp_source1_castle.png';
import procamp_source2_ballerina from '/img/instruments/videomancer/procamp/procamp_source2_ballerina.png';
import procamp_source3_collage from '/img/instruments/videomancer/procamp/procamp_source3_collage.png';
import procamp_source4_pattern from '/img/instruments/videomancer/procamp/procamp_source4_pattern.png';
import procamp_source5_boy from '/img/instruments/videomancer/procamp/procamp_source5_boy.png';
import procamp_source6_paint from '/img/instruments/videomancer/procamp/procamp_source6_paint.png';
import procamp_hero_s1 from '/img/instruments/videomancer/procamp/procamp_hero_s1.png';
import procamp_hero_s2 from '/img/instruments/videomancer/procamp/procamp_hero_s2.png';
import procamp_hero_s3 from '/img/instruments/videomancer/procamp/procamp_hero_s3.png';
import procamp_hero_s4 from '/img/instruments/videomancer/procamp/procamp_hero_s4.png';
import procamp_hero_s5 from '/img/instruments/videomancer/procamp/procamp_hero_s5.png';
import procamp_hero_s6 from '/img/instruments/videomancer/procamp/procamp_hero_s6.png';
import procamp_ex1_s1 from '/img/instruments/videomancer/procamp/procamp_ex1_s1.png';
import procamp_ex1_s2 from '/img/instruments/videomancer/procamp/procamp_ex1_s2.png';
import procamp_ex1_s3 from '/img/instruments/videomancer/procamp/procamp_ex1_s3.png';
import procamp_ex1_s4 from '/img/instruments/videomancer/procamp/procamp_ex1_s4.png';
import procamp_ex1_s5 from '/img/instruments/videomancer/procamp/procamp_ex1_s5.png';
import procamp_ex1_s6 from '/img/instruments/videomancer/procamp/procamp_ex1_s6.png';
import procamp_ex2_s1 from '/img/instruments/videomancer/procamp/procamp_ex2_s1.png';
import procamp_ex2_s2 from '/img/instruments/videomancer/procamp/procamp_ex2_s2.png';
import procamp_ex2_s3 from '/img/instruments/videomancer/procamp/procamp_ex2_s3.png';
import procamp_ex2_s4 from '/img/instruments/videomancer/procamp/procamp_ex2_s4.png';
import procamp_ex2_s5 from '/img/instruments/videomancer/procamp/procamp_ex2_s5.png';
import procamp_ex2_s6 from '/img/instruments/videomancer/procamp/procamp_ex2_s6.png';
import procamp_ex3_s1 from '/img/instruments/videomancer/procamp/procamp_ex3_s1.png';
import procamp_ex3_s2 from '/img/instruments/videomancer/procamp/procamp_ex3_s2.png';
import procamp_ex3_s3 from '/img/instruments/videomancer/procamp/procamp_ex3_s3.png';
import procamp_ex3_s4 from '/img/instruments/videomancer/procamp/procamp_ex3_s4.png';
import procamp_ex3_s5 from '/img/instruments/videomancer/procamp/procamp_ex3_s5.png';
import procamp_ex3_s6 from '/img/instruments/videomancer/procamp/procamp_ex3_s6.png';

# Procamp

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: procamp_source1_castle, after: procamp_hero_s1 },
    { label: "Ballerina", before: procamp_source2_ballerina, after: procamp_hero_s2 },
    { label: "Collage", before: procamp_source3_collage, after: procamp_hero_s3 },
    { label: "Pattern", before: procamp_source4_pattern, after: procamp_hero_s4 },
    { label: "Boy", before: procamp_source5_boy, after: procamp_hero_s5 },
    { label: "Paint", before: procamp_source6_paint, after: procamp_hero_s6 },
  ]}
/>
*Procamp applying independent per-channel gain, offset, and inversion across Y/U/V with fade-to-color interpolation.*

---

## Overview

Every broadcast facility has a processing amplifier — a "proc amp" — sitting between source and destination, adjusting signal levels so that everything arriving downstream is correctly calibrated. Procamp brings that same utility to Videomancer, providing independent gain and offset controls for each of the three YUV channels plus per-channel inversion and a fade-to-color output stage.

The architecture is deliberately straightforward: three parallel `proc_amp_u` instances (one per channel) apply contrast-style gain and brightness-style offset, followed by three `interpolator_u` instances that fade the processed result toward a selectable target color. The name follows broadcast convention — "proc amp" is standard video engineering shorthand for processing amplifier.

At default settings (all knobs at noon, fader fully up), the signal passes through unchanged. Small adjustments produce the level corrections and color shifts familiar to anyone who has used a hardware TBC or color corrector. Extreme settings push the signal into clipping, inversion, and full-field color washes that go well beyond calibration into creative territory.

---

## Background

### The Processing Amplifier in Broadcast Video

The processing amplifier is one of the oldest and most fundamental tools in video engineering. In analog television, signals degrade as they pass through cables, switchers, and distribution amplifiers — brightness drifts, contrast compresses, color shifts. The proc amp sits at the receiving end and applies corrective gain and offset to bring the signal back into specification. Procamp implements this concept digitally, operating on the Y, U, and V channels independently with 10-bit precision.

### Gain and Offset in the YUV Domain

Each channel's `proc_amp_u` computes: result = (input − 512) × gain + offset, where gain ranges from 0× to approximately 2× and offset ranges from −512 to +512 counts. The midpoint subtraction centers the multiplication around mid-scale so that gain changes expand or compress the signal symmetrically around 50% rather than scaling from zero. This is identical to the contrast/brightness model used in broadcast color correctors, where "contrast" is gain around the pedestal and "brightness" is a DC offset.

### Per-Channel Color Control

Operating on Y, U, and V independently rather than using combined "saturation" and "hue" controls gives full access to the signal structure. Increasing U gain while reducing V gain shifts the color balance toward blue-cyan. Offsetting U and V in opposite directions creates color tints that wouldn't be possible with a single saturation knob. This per-channel approach is more granular than traditional proc amps but also more powerful for creative color manipulation.

### Fade-to-Color

The output stage uses three `interpolator_u` instances to crossfade between the processed signal and a fixed target color. For the Y channel, the target is either black (0) or white (1023), selected by the Fade Color toggle. For U and V, the target is always 512 (neutral chroma), regardless of the Fade Color setting. This means the fade always desaturates toward monochrome, converging on either pure black or pure white. This is distinct from a wet/dry mix — a wet/dry mix would crossfade between the processed and the *original* signal, whereas fade-to-color crossfades between processed and a *fixed* color value.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   ├─ 1. Invert Y          (optional bitwise NOT)       [1 clk]
│   ├─ 2. Proc Amp Y        (gain + offset via proc_amp_u) [9 clk]
│   └─ 3. Fade-to-Color Y   (interpolator_u → black/white) [4 clk]
│
├── U Channel ──────────────────────────────────────────────────
│   ├─ 1. Invert U          (optional bitwise NOT)       [1 clk]
│   ├─ 2. Proc Amp U        (gain + offset via proc_amp_u) [9 clk]
│   └─ 3. Fade-to-Color U   (interpolator_u → 512)       [4 clk]
│
├── V Channel ──────────────────────────────────────────────────
│   ├─ 1. Invert V          (optional bitwise NOT)       [1 clk]
│   ├─ 2. Proc Amp V        (gain + offset via proc_amp_u) [9 clk]
│   └─ 3. Fade-to-Color V   (interpolator_u → 512)       [4 clk]
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 14-stage delay (hsync, vsync, field, Y/U/V bypass copy)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original (delayed) or processed signal
```

All three channels are processed in parallel through identical pipelines, but each with independent gain, offset, and inversion settings. The key architectural detail is the fade-to-color stage at the end: the Y interpolator crossfades between the processed Y and a fixed target (0 or 1023), while the U and V interpolators always crossfade toward 512 (neutral chroma). This means lowering the Fade Amount fader simultaneously dims (or brightens) and desaturates the image, converging on a flat monochrome field. The bypass path uses a 14-clock delay line to keep the dry signal time-aligned with the processed result.

---

## Parameter Reference

<img src={procamp_control_panel} alt="Videomancer front panel with Procamp loaded"/>
*Videomancer's front panel with Procamp active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the Y channel gain (contrast). The `proc_amp_u` centers the input around mid-scale (512) before applying gain, so this control expands or compresses the luminance range symmetrically. At noon (512), gain is unity — no change. Fully counter-clockwise crushes all luminance to a flat field at the offset level. Fully clockwise doubles the contrast, pushing highlights and shadows toward the extremes with hard clipping at 0 and 1023.

---

#### Knob 2 — U Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the U channel gain. Because U carries blue-yellow color difference information, increasing U gain intensifies blue and yellow components while reducing it desaturates toward the red-cyan axis. At unity (noon), color reproduction is unaltered. At zero, U is crushed to the offset value, effectively killing blue-yellow information.

---

#### Knob 3 — V Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the V channel gain. V carries the red-cyan color difference, so boosting V gain intensifies reds and cyans. Combined with U gain, these two knobs provide full control over chroma intensity and color axis balance — a more granular alternative to a single saturation control.

---

#### Knob 4 — Y Offset
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Y channel offset (brightness). Adds a DC shift to the luminance after gain scaling. At noon (512), offset is zero. Counter-clockwise darkens the image by subtracting from all luminance values; clockwise brightens it. When gain is set to zero, this knob alone determines the flat luminance level of the output.

---

#### Knob 5 — U Offset
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

U channel offset. Shifts the U component by a constant amount, producing a global color tint along the blue-yellow axis. Positive offset (clockwise) tints toward blue; negative (counter-clockwise) tints toward yellow. This is useful for deliberate color casts or correcting source material with a blue/yellow imbalance.

---

#### Knob 6 — V Offset
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

V channel offset. Shifts the V component along the red-cyan axis. Combined with U Offset, the two offset knobs can produce any arbitrary color tint — a capability not available in traditional single-axis hue controls.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Y Invert** | Off | On |
| **8 — U Invert** | Off | On |
| **9 — V Invert** | Off | On |
| **10 — Fade Color** | Black | White |
| **11 — Bypass** | Off | On |

The five toggles control three per-channel inversions plus the fade color selection and bypass. The inversions are applied *before* the proc amp stage, so they interact with gain and offset — inverting Y before applying 2× gain produces a very different result than inverting after. The Fade Color toggle only affects the Y channel's fade target; U and V always fade toward 512 regardless of this setting.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Fade Amount
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the fade-to-color amount. This is **not** a wet/dry mix — it crossfades between the processed signal and a *fixed color* (black or white for Y, neutral 512 for U/V). At 100% (fully up, default), the output is the fully processed signal. As you lower the fader, the image progressively converges on the target color. At 0%, the output is a flat monochrome field. The fade simultaneously affects brightness and saturation because all three channels converge on their respective targets.

---

## Guided Exercises

These exercises progress from basic level correction to creative color manipulation, exploring how per-channel control and fade-to-color interact.

### Exercise 1: Luminance Calibration

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: procamp_source1_castle, after: procamp_ex1_s1 },
    { label: "Ballerina", before: procamp_source2_ballerina, after: procamp_ex1_s2 },
    { label: "Collage", before: procamp_source3_collage, after: procamp_ex1_s3 },
    { label: "Pattern", before: procamp_source4_pattern, after: procamp_ex1_s4 },
    { label: "Boy", before: procamp_source5_boy, after: procamp_ex1_s5 },
    { label: "Paint", before: procamp_source6_paint, after: procamp_ex1_s6 },
  ]}
/>
*Luminance Calibration — simulated result across source images.*
**Source**: A grayscale ramp or test pattern with known black and white reference levels.

**Objective**: Learn how Y gain and Y offset interact to set correct brightness and contrast.

1. **Verify defaults**: Confirm all knobs at noon, fader fully up. Output should match input exactly.
2. **Offset adjustment**: Slowly turn Y Offset counter-clockwise. Watch the entire image darken uniformly — this is a DC shift.
3. **Gain adjustment**: Return Y Offset to noon. Now turn Y Gain clockwise past noon. Bright areas get brighter, dark areas get darker — contrast increases symmetrically around mid-gray.
4. **Combined**: Set Y Gain to ~75% for increased contrast, then use Y Offset to recenter the brightness. This is the classic broadcast calibration workflow.
5. **Zero gain**: Turn Y Gain fully counter-clockwise. The image collapses to a flat field whose brightness is set by Y Offset alone.

**Key concepts**: Gain is multiplication around the midpoint (contrast), offset is addition (brightness), gain at zero collapses the signal to a constant, proc amp centers around 512 before gain

---

### Exercise 2: Creative Color Tinting

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: procamp_source1_castle, after: procamp_ex2_s1 },
    { label: "Ballerina", before: procamp_source2_ballerina, after: procamp_ex2_s2 },
    { label: "Collage", before: procamp_source3_collage, after: procamp_ex2_s3 },
    { label: "Pattern", before: procamp_source4_pattern, after: procamp_ex2_s4 },
    { label: "Boy", before: procamp_source5_boy, after: procamp_ex2_s5 },
    { label: "Paint", before: procamp_source6_paint, after: procamp_ex2_s6 },
  ]}
/>
*Creative Color Tinting — simulated result across source images.*
**Source**: A well-exposed video source with a range of natural colors — outdoor scenes or skin tones work well.

**Objective**: Explore per-channel offset and gain for deliberate color grading.

1. **Warm tint**: Increase V Offset slightly (clockwise) to add red warmth. Decrease U Offset slightly (counter-clockwise) to reduce blue. The image takes on a warm, golden tone.
2. **Cool tint**: Reverse — increase U Offset, decrease V Offset. The image shifts toward blue-cyan.
3. **Desaturate one axis**: Set U Gain to zero while leaving V Gain at unity. Only the red-cyan color axis remains. The image appears partially desaturated with an unusual color palette.
4. **Boost and shift**: Set both U and V Gain to ~75% for high saturation, then offset both channels slightly to shift the entire color gamut.
5. **Compare**: Toggle Bypass to see the original. Toggle back to see your color grade.

**Key concepts**: U/V offsets create color tints along orthogonal axes, per-channel gain controls saturation per axis rather than uniformly, combining gain and offset gives full color grading control in YUV space

---

### Exercise 3: Fade-to-Color Drama

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: procamp_source1_castle, after: procamp_ex3_s1 },
    { label: "Ballerina", before: procamp_source2_ballerina, after: procamp_ex3_s2 },
    { label: "Collage", before: procamp_source3_collage, after: procamp_ex3_s3 },
    { label: "Pattern", before: procamp_source4_pattern, after: procamp_ex3_s4 },
    { label: "Boy", before: procamp_source5_boy, after: procamp_ex3_s5 },
    { label: "Paint", before: procamp_source6_paint, after: procamp_ex3_s6 },
  ]}
/>
*Fade-to-Color Drama — simulated result across source images.*
**Source**: Any dynamic footage — live camera, animations, or abstract video synthesis.

**Objective**: Use the fade-to-color stage for dramatic transitions and monochrome washes.

1. **Fade to black**: Set Fade Color to Black. Slowly lower the Fade Amount fader. Watch the image darken and desaturate simultaneously, converging on black.
2. **Fade to white**: Toggle Fade Color to White. Repeat the fade. Now the image brightens and desaturates, converging on a white field. Note that the *rate* of desaturation matches the brightness change because U and V always fade toward neutral.
3. **Partial fade + processing**: Set Fade Amount to ~50% for a half-faded look, then apply extreme Y Gain and color offsets. The fade stage softens the extremes by pulling everything back toward the target color.
4. **Inversion + fade**: Enable Y Invert, then slowly fade to white. The inverted luminance converges on white from below, creating a solarization-like effect at intermediate fade levels.
5. **Animated fade**: Patch a control voltage or slowly sweep the Fade Amount fader for a live fade-to-black or fade-to-white transition.

**Key concepts**: Fade-to-color is not a wet/dry mix — it targets a fixed color rather than the original signal, Y fades to black or white while U/V always fade to neutral, partial fade softens processing extremes

---


## Tips

- **Defaults are transparent**: At noon on all knobs and fader fully up, the signal passes through bit-identical. Procamp is safe to leave in the chain as a calibration point.
- **Gain before offset**: The proc amp applies gain *then* offset internally. To achieve a specific target level, set gain first for the desired contrast, then fine-tune offset.
- **Fade is not mix**: The fader does not crossfade between processed and original — it fades toward a *fixed color*. For a true dry/wet blend, use a downstream mixer program.
- **Per-channel desaturation**: Setting U Gain and V Gain to zero while leaving Y at unity produces a clean monochrome conversion without needing the Mono toggle found in other programs.
- **Color tinting shortcut**: For a quick warm or cool tint, offset U and V in opposite directions while leaving gains at unity.
- **Inversion as creative tool**: Y Invert before high gain creates extreme solarization effects that are different from simple post-gain inversion.
- **Fade for transitions**: The Fade Amount fader is ideal for live performance fade-to-black/white transitions because it simultaneously handles brightness and desaturation.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bypass** | Routes the time-aligned dry input directly to the output, skipping all processing stages. |
| **DC Offset** | A constant value added to every sample in a channel, shifting the entire signal up or down. |
| **Fade-to-Color** | Interpolation between the processed signal and a fixed target color (black, white, or neutral chroma); distinct from a wet/dry mix. |
| **Gain** | Multiplicative scaling of a signal centered around a reference point (512 in 10-bit YUV); equivalent to "contrast" in broadcast terminology. |
| **Interpolator** | A pipelined hardware unit that computes a + (b − a) × t for crossfading between two values. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies contrast and brightness correction to a video signal channel. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U = blue-yellow, V = red-cyan), used throughout the Videomancer video pipeline. |

---
