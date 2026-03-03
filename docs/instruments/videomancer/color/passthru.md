---
draft: true
sidebar_position: 215
slug: /instruments/videomancer/passthru
title: "Passthru"
image: /img/instruments/videomancer/passthru/passthru_hero_s1.png
description: "Every video processing chain begins with a signal that enters and exits unchanged — a pass-through."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import passthru_source1_cat from '/img/instruments/videomancer/passthru/passthru_source1_cat.png';
import passthru_source2_dog from '/img/instruments/videomancer/passthru/passthru_source2_dog.png';
import passthru_source3_collage from '/img/instruments/videomancer/passthru/passthru_source3_collage.png';
import passthru_source4_pattern from '/img/instruments/videomancer/passthru/passthru_source4_pattern.png';
import passthru_source5_boy from '/img/instruments/videomancer/passthru/passthru_source5_boy.png';
import passthru_source6_wood from '/img/instruments/videomancer/passthru/passthru_source6_wood.png';
import passthru_hero_s1 from '/img/instruments/videomancer/passthru/passthru_hero_s1.png';
import passthru_hero_s2 from '/img/instruments/videomancer/passthru/passthru_hero_s2.png';
import passthru_hero_s3 from '/img/instruments/videomancer/passthru/passthru_hero_s3.png';
import passthru_hero_s4 from '/img/instruments/videomancer/passthru/passthru_hero_s4.png';
import passthru_hero_s5 from '/img/instruments/videomancer/passthru/passthru_hero_s5.png';
import passthru_hero_s6 from '/img/instruments/videomancer/passthru/passthru_hero_s6.png';

# Passthru

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: passthru_source1_cat, after: passthru_hero_s1 },
    { label: "Dog", before: passthru_source2_dog, after: passthru_hero_s2 },
    { label: "Collage", before: passthru_source3_collage, after: passthru_hero_s3 },
    { label: "Pattern", before: passthru_source4_pattern, after: passthru_hero_s4 },
    { label: "Boy", before: passthru_source5_boy, after: passthru_hero_s5 },
    { label: "Wood", before: passthru_source6_wood, after: passthru_hero_s6 },
  ]}
/>
*Passthru applying brightness, contrast, and saturation adjustments with per-channel inversion to reveal the fundamental building blocks of video color correction.*

---

## Overview

Every video processing chain begins with a signal that enters and exits unchanged — a pass-through. Passthru starts there but adds the most essential color correction tool in video engineering: the processing amplifier, or proc amp. Brightness shifts the entire luminance range up or down. Contrast expands or compresses that range around mid-gray. Saturation does the same for color. These three parameters define the foundation of every color grading workflow.

Beyond the proc amp, Passthru provides per-channel inversion toggles that flip luma, U chroma, or V chroma independently, a monochrome switch that kills all color information, and a hue control that cross-blends the U and V chroma axes. The name is literal — it passes video through — but the processing it applies along the way teaches you how YUV color space works from the inside.

With all controls at center and all toggles off, the output is identical to the input. This makes Passthru the ideal starting point for learning the Videomancer control surface, understanding YUV signal structure, and calibrating your monitoring chain.

---

## Background

### What Is a Proc Amp?

A **processing amplifier** is the oldest and most fundamental video correction tool. In analog broadcast facilities, the proc amp was a rack-mount unit that adjusted the gain (contrast) and pedestal (brightness) of a composite video signal before transmission. Every broadcast chain had at least one. The digital proc amp in Passthru performs the identical mathematical operation on each pixel: subtract the midpoint, scale by a contrast factor, then add a brightness offset. The formula — `Y' = (Y − 512) × contrast / 512 + brightness + 512` — is the discrete equivalent of the analog gain-and-offset circuit.

### Why YUV?

Television engineers separated brightness from color for a practical reason: black-and-white receivers needed to display color broadcasts. The Y (luminance) channel carries brightness; U and V (chrominance) carry color difference signals. This separation has a profound creative consequence — you can manipulate brightness and color independently. Passthru exploits this by giving you separate contrast and saturation controls, plus per-channel inversion toggles that affect Y, U, and V independently. Inverting Y produces a photographic negative. Inverting U or V rotates the color wheel by 180° along one axis, producing complementary color shifts.

### What Does Channel Inversion Do?

Inversion computes `1023 − value` for a 10-bit signal. For luminance, this turns white to black and black to white — a photographic negative. For chrominance, inversion around the midpoint (512) maps each color to its complement: blues become yellows (U inversion), reds become cyans (V inversion). Combining U and V inversion together rotates the entire color palette by 180°, swapping every hue for its opposite.

### What Is Monochrome Mode?

Setting both chroma channels to the midpoint value (512) removes all color information. The result is a pure luminance signal — grayscale video. This is not desaturation (which would reduce chroma toward 512 gradually); it is an absolute clamp that forces U = V = 512 regardless of input. The brightness and contrast controls still operate on the Y channel, so you can grade the monochrome image after stripping color.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   ├─ 1. Proc Amp              Y' = (Y−512) × contrast/512 + brightness + 512
│   ├─ 2. Invert Y              (optional: 1023 − Y')
│   └─ 3. Mix                   crossfade dry/wet
│
├── U Channel ──────────────────────────────────────────────────
│   ├─ 1. Mono Clamp            (optional: force U = 512)
│   ├─ 2. Proc Amp              U' = (U−512) × saturation/512 + 512
│   ├─ 3. Hue Blend             (cross-mix U↔V)
│   ├─ 4. Invert U              (optional: 1023 − U')
│   └─ 5. Mix                   crossfade dry/wet
│
├── V Channel ──────────────────────────────────────────────────
│   ├─ 1. Mono Clamp            (optional: force V = 512)
│   ├─ 2. Proc Amp              V' = (V−512) × saturation/512 + 512
│   ├─ 3. Hue Blend             (cross-mix V↔U)
│   ├─ 4. Invert V              (optional: 1023 − V')
│   └─ 5. Mix                   crossfade dry/wet
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Toggle 5 selects original or processed signal
```

The proc amp stage runs on all three channels simultaneously through three parallel `interpolator_u` instances. The Y channel receives brightness and contrast; the U and V channels receive saturation only. The hue control does not perform a true trigonometric rotation — it cross-blends U into V and V into U, which approximates hue shifting at moderate settings but compresses chrominance at extremes. Per-channel inversion occurs after the proc amp, so the contrast-expanded signal is what gets inverted. The wet/dry mix fader crossfades between the fully processed result and the original unprocessed input.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Null 1
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Brightness. Shifts the entire luminance range up or down. At center (512), no offset is applied. Turning clockwise adds a positive DC offset — the image gets brighter, with black lifting toward gray. Turning counter-clockwise subtracts — the image darkens, with highlights pulling down. Brightness applies after contrast, so it shifts the contrast-expanded range uniformly.

---

#### Knob 2 — Null 2
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Contrast. Scales the luminance channel around the midpoint (512). At center, the gain is unity — no change. Clockwise expands the range: darks get darker, brights get brighter, and mid-tones spread apart. Counter-clockwise compresses: the image flattens toward a uniform gray. The formula is `(Y − 512) × contrast / 512`, so a register value of 1023 roughly doubles the contrast, while 0 collapses all luminance to the brightness offset.

---

#### Knob 3 — Null 3
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Saturation. Applies the same gain-around-midpoint operation to both U and V chrominance channels simultaneously. At center, color is unchanged. Clockwise increases saturation — colors become more vivid and eventually clip to the 10-bit limits. Counter-clockwise desaturates — colors fade toward gray. At minimum, the result is nearly monochrome (though not clamped to exactly 512 like the Mono toggle). Saturation interacts with the Mono toggle: if Mono is on, U and V are clamped to 512 before the saturation stage, so the control has no visible effect.

---

#### Knob 4 — Null 4
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Hue. Cross-blends the U and V chroma channels, simulating a hue rotation. At center (512), no blending occurs. Turning the control mixes a portion of U into the V channel and V into the U channel, shifting the apparent hue of all colors. This is not a true angular rotation in color space — it approximates one at small offsets but compresses chroma amplitude at extremes. For precise hue rotation, keep this control near center and make small adjustments.

---

#### Knob 5 — Null 5
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

R Offset. This register is declared in the hardware interface but is not connected to any processing logic in the current firmware. Adjusting this control has no visible effect on the output. It is reserved for future use.

---

#### Knob 6 — Null 6
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

G Offset. Like R Offset, this register is declared but unused in the current implementation. Adjusting this control produces no change in the output signal. Reserved for future firmware revisions.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Null 7** | Off | On |
| **8 — Null 8** | Off | On |
| **9 — Null 9** | Off | On |
| **10 — Null 10** | Off | On |
| **11 — Null 11** | Off | On |

The five toggles provide binary processing options. Toggles 7–9 invert individual YUV channels independently — any combination of the three can be active simultaneously. Toggle 10 enables monochrome mode by clamping chroma before the saturation stage. Toggle 11 is the standard bypass that routes the input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Null 12
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix. Wet/dry crossfade between the processed signal and the original input. At 100% (fully clockwise), the output is entirely the processed signal. At 0% (fully counter-clockwise), the output is the unprocessed input — functionally identical to Bypass but with a smooth transition. Intermediate positions blend the two, useful for dialing back aggressive contrast or saturation settings without reconfiguring individual knobs.

---

## Guided Exercises

These exercises explore Passthru's proc amp from basic brightness adjustment through full channel manipulation. Each builds a deeper understanding of YUV signal structure.

### Exercise 1: Brightness and Contrast

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: passthru_source1_kodim03, after: passthru_exercise1_result },
    { label: "Kodim15", before: passthru_source2_kodim15, after: passthru_exercise1_result },
    { label: "Peppers", before: passthru_source3_peppers_512, after: passthru_exercise1_result },
  ]}
/>
*Brightness and Contrast — simulated result across source images.*
**Source**: A camera feed or recorded footage with a mix of highlights, midtones, and shadows.

**Objective**: Learn how brightness and contrast interact in the proc amp formula and observe clipping behavior at extremes.

1. **Baseline**: Confirm all knobs are centered and all toggles are off. The output should match the input.
2. **Brightness sweep**: Slowly turn Brightness clockwise. Watch shadows lift toward gray. Now sweep counter-clockwise past center — highlights crush toward black.
3. **Contrast expansion**: Return Brightness to center. Sweep Contrast clockwise. Darks get darker, brights get brighter, and the image gains punch. Note how mid-gray (512) remains anchored.
4. **Contrast compression**: Sweep Contrast counter-clockwise. The image flattens toward uniform gray.
5. **Combined**: Set Contrast to ~75% and Brightness to ~60%. Observe the expanded-then-shifted result.

**Key concepts**: Brightness is a DC offset applied after gain, contrast is gain around the midpoint, clipping occurs when values exceed 0 or 1023

---

### Exercise 2: Color Manipulation

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: passthru_source1_kodim03, after: passthru_exercise2_result },
    { label: "Kodim15", before: passthru_source2_kodim15, after: passthru_exercise2_result },
    { label: "Peppers", before: passthru_source3_peppers_512, after: passthru_exercise2_result },
  ]}
/>
*Color Manipulation — simulated result across source images.*
**Source**: Footage with strong, varied colors — flowers, painted surfaces, or color bars.

**Objective**: Explore saturation, per-channel inversion, and monochrome mode to understand YUV color space.

1. **Saturate**: Sweep Saturation clockwise past center. Colors become more vivid. Note how luminance is unaffected — brightness doesn't change, only color intensity.
2. **Desaturate**: Sweep Saturation counter-clockwise. Colors fade. Compare with Mono toggle.
3. **Mono toggle**: Enable Mono (Switch 10). All color vanishes instantly. Sweep Saturation — nothing changes, confirming Mono clamps before the saturation stage.
4. **Channel inversion**: Disable Mono. Enable Invert U (Switch 8). Blues and yellows swap. Now also enable Invert V (Switch 9). All hues shift to their complements.
5. **Full negative**: Enable Invert Y (Switch 7) as well. The image is now a full photographic/video negative.
6. **Hue blend**: Disable all inversions. Slowly adjust Hue away from center. Watch colors shift as U and V cross-blend.

**Key concepts**: Saturation is chroma gain around midpoint, inversion maps each channel to its complement, Mono is an absolute clamp not a gradual fade, YUV separates brightness from color

---

### Exercise 3: Signal Chain Exploration

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: passthru_source1_kodim03, after: passthru_exercise3_result },
    { label: "Kodim15", before: passthru_source2_kodim15, after: passthru_exercise3_result },
    { label: "Peppers", before: passthru_source3_peppers_512, after: passthru_exercise3_result },
  ]}
/>
*Signal Chain Exploration — simulated result across source images.*
**Source**: Any live or recorded video with moderate contrast and color.

**Objective**: Use Mix, Bypass, and combined settings to understand the full signal chain and gain confidence with A/B comparison.

1. **Aggressive processing**: Set Brightness ~70%, Contrast ~80%, Saturation ~30%. Enable Invert Y.
2. **Mix blend**: Slowly lower Mix from 100% toward 0%. Watch the processed signal fade into the original input.
3. **Half mix**: Set Mix to ~50%. The output is a blend — inverted and non-inverted luminance average out, contrast partially applies.
4. **Bypass A/B**: Toggle Bypass on and off rapidly. Compare the blended output with the clean input.
5. **Mono + contrast**: Enable Mono. Increase Contrast to ~85%. The monochrome image gains dramatic separation. Use Mix to blend this against the color original.
6. **Reset and verify**: Return all controls to center, all toggles off, Mix to 100%. Confirm the output matches the input exactly.

**Key concepts**: Mix crossfades processed and original in the 10-bit domain, Bypass is a hard switch while Mix is a smooth blend, proc amp and channel inversion compound before the mix stage

---


## Tips

- **Start here**: Passthru is the simplest program in the Videomancer library. Use it to learn the control surface and understand YUV signal structure before exploring more complex programs.
- **Proc amp calibration**: Use Brightness and Contrast with a known test pattern to calibrate your output levels before recording or patching into downstream equipment.
- **Per-channel inversion is not hue rotation**: Inverting U or V mirrors one chroma axis. The Hue knob cross-blends both axes. These are geometrically different operations in color space.
- **Mono is absolute**: The Mono toggle hard-clamps chroma to 512. It is not the same as setting Saturation to zero (which approaches but may not reach exactly 512 due to rounding).
- **Mix for subtle correction**: Instead of dialing back Contrast or Saturation, make aggressive settings and use the Mix fader to blend the result against the original. This often produces more natural-looking corrections.
- **Bypass for live performance**: Switch 11 gives instant, glitch-free A/B comparison. Assign it to a convenient position on your control surface for rapid toggling during live sets.
- **Unused controls**: R Offset and G Offset (knobs 5 and 6) are reserved and have no effect. Don't be surprised when they do nothing — this is by design.
- **Feedback-safe**: Because Passthru is a pure proc amp with no spatial effects, it is stable in feedback loops. Route the output back to the input for iterative contrast/saturation expansion.

---

## Glossary

| Term | Definition |
|------|------------|
| **Brightness** | A DC offset added to the luminance signal, shifting all pixel values up or down uniformly. |
| **Chroma** | The color-difference components (U and V) of a YUV video signal, encoding hue and saturation information. |
| **Clipping** | When a signal value exceeds the representable range (0–1023), it is clamped to the boundary value, losing detail. |
| **Contrast** | A gain factor applied around the midpoint (512), expanding or compressing the luminance range. |
| **Interpolator** | A hardware module that performs linear crossfading between two input values, used here for wet/dry mix. |
| **Inversion** | Computing the complement of a signal value: `1023 − value`. Flips bright to dark (Y) or shifts colors to their complements (U, V). |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Mono** | Monochrome mode, achieved by clamping both chroma channels to the midpoint (512). |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness, contrast, and saturation adjustment to a video signal. |
| **Saturation** | The intensity of color in a video signal, controlled by applying gain to the U and V chroma channels around their midpoint. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
