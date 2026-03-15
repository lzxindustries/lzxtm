---
draft: true
sidebar_position: 333
slug: /instruments/videomancer/whitebal
title: "White Balance"
image: /img/instruments/videomancer/whitebal/whitebal_hero_s1.png
description: "White Balance (Whitebal) provides parametric color temperature and tint correction — the same fundamental operation performed by every camera, display, and color grading system to ensure that neutral objects appear neutral under different illuminants."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import whitebal_control_panel from '/img/instruments/videomancer/whitebal/whitebal_control_panel.png';
import whitebal_source1_ballerina from '/img/instruments/videomancer/whitebal/whitebal_source1_ballerina.png';
import whitebal_source2_sunset from '/img/instruments/videomancer/whitebal/whitebal_source2_sunset.png';
import whitebal_source3_clouds from '/img/instruments/videomancer/whitebal/whitebal_source3_clouds.png';
import whitebal_source4_pattern from '/img/instruments/videomancer/whitebal/whitebal_source4_pattern.png';
import whitebal_source5_man from '/img/instruments/videomancer/whitebal/whitebal_source5_man.png';
import whitebal_source6_paint from '/img/instruments/videomancer/whitebal/whitebal_source6_paint.png';
import whitebal_hero_s1 from '/img/instruments/videomancer/whitebal/whitebal_hero_s1.png';
import whitebal_hero_s2 from '/img/instruments/videomancer/whitebal/whitebal_hero_s2.png';
import whitebal_hero_s3 from '/img/instruments/videomancer/whitebal/whitebal_hero_s3.png';
import whitebal_hero_s4 from '/img/instruments/videomancer/whitebal/whitebal_hero_s4.png';
import whitebal_hero_s5 from '/img/instruments/videomancer/whitebal/whitebal_hero_s5.png';
import whitebal_hero_s6 from '/img/instruments/videomancer/whitebal/whitebal_hero_s6.png';
import whitebal_ex1_s1 from '/img/instruments/videomancer/whitebal/whitebal_ex1_s1.png';
import whitebal_ex1_s2 from '/img/instruments/videomancer/whitebal/whitebal_ex1_s2.png';
import whitebal_ex1_s3 from '/img/instruments/videomancer/whitebal/whitebal_ex1_s3.png';
import whitebal_ex1_s4 from '/img/instruments/videomancer/whitebal/whitebal_ex1_s4.png';
import whitebal_ex1_s5 from '/img/instruments/videomancer/whitebal/whitebal_ex1_s5.png';
import whitebal_ex1_s6 from '/img/instruments/videomancer/whitebal/whitebal_ex1_s6.png';
import whitebal_ex2_s1 from '/img/instruments/videomancer/whitebal/whitebal_ex2_s1.png';
import whitebal_ex2_s2 from '/img/instruments/videomancer/whitebal/whitebal_ex2_s2.png';
import whitebal_ex2_s3 from '/img/instruments/videomancer/whitebal/whitebal_ex2_s3.png';
import whitebal_ex2_s4 from '/img/instruments/videomancer/whitebal/whitebal_ex2_s4.png';
import whitebal_ex2_s5 from '/img/instruments/videomancer/whitebal/whitebal_ex2_s5.png';
import whitebal_ex2_s6 from '/img/instruments/videomancer/whitebal/whitebal_ex2_s6.png';
import whitebal_ex3_s1 from '/img/instruments/videomancer/whitebal/whitebal_ex3_s1.png';
import whitebal_ex3_s2 from '/img/instruments/videomancer/whitebal/whitebal_ex3_s2.png';
import whitebal_ex3_s3 from '/img/instruments/videomancer/whitebal/whitebal_ex3_s3.png';
import whitebal_ex3_s4 from '/img/instruments/videomancer/whitebal/whitebal_ex3_s4.png';
import whitebal_ex3_s5 from '/img/instruments/videomancer/whitebal/whitebal_ex3_s5.png';
import whitebal_ex3_s6 from '/img/instruments/videomancer/whitebal/whitebal_ex3_s6.png';

# White Balance

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: whitebal_source1_ballerina, after: whitebal_hero_s1 },
    { label: "Sunset", before: whitebal_source2_sunset, after: whitebal_hero_s2 },
    { label: "Clouds", before: whitebal_source3_clouds, after: whitebal_hero_s3 },
    { label: "Pattern", before: whitebal_source4_pattern, after: whitebal_hero_s4 },
    { label: "Man", before: whitebal_source5_man, after: whitebal_hero_s5 },
    { label: "Paint", before: whitebal_source6_paint, after: whitebal_hero_s6 },
  ]}
/>
*White Balance applying color temperature correction along the Planckian locus, shifting the chrominance of the input video from cool blue-white through neutral to warm amber-orange.*

---

## Overview

**White Balance** (Whitebal) provides parametric color temperature and tint correction — the same fundamental operation performed by every camera, display, and color grading system to ensure that neutral objects appear neutral under different illuminants. The Color Temp knob shifts the chrominance of the entire signal along the blue-amber axis, simulating the Planckian locus (the curve of color temperatures from candle light to overcast sky). The Tint knob provides orthogonal green-magenta correction. Together, they form a complete two-axis white balance system.

Beyond color balance, Whitebal includes a full luminance processing chain: Y Gain scales overall brightness, Contrast expands or compresses the tonal range around 512, Brightness adds a DC offset, and Saturation controls chromatic intensity. Y Invert and UV Invert provide complement operations on their respective channels. A Wide Range toggle doubles the chrominance offset for extreme color grading.

Whitebal is in the **Color** category — a fundamental color correction tool designed for both technical correction and creative color grading.

---

## Quick Start

1. **Color Temp + Vectorscope**: Use Vectorscope to monitor the UV shift as you adjust Color Temp — the dot cloud moves along the blue-amber axis.
2. **Normal Range for correction**: Normal Range halves the offset for precise correction — use it when matching to a reference white point.
3. **Wide Range for creative**: Wide Range enables extreme shifts — deep blue moonlight or scorching amber sunset.

---

## Background

### What Is Color Temperature?

**Color temperature** describes the hue of a light source by comparing it to the color of a theoretical blackbody radiator heated to a given temperature (in Kelvin). Low temperatures (~2700K) produce warm amber light (incandescent bulbs); mid temperatures (~5600K) produce neutral daylight; high temperatures (~10000K) produce cool blue light (overcast sky). Camera white balance corrects for the color of the illuminant so that white objects appear white regardless of the lighting.

### What Is the Planckian Locus?

The **Planckian locus** is the path traced by blackbody radiation on a chrominance diagram as temperature varies. It curves through the amber-orange region at low temperatures, passes through neutral white, and continues into the blue region at high temperatures. Whitebal approximates this curve by applying a signed UV offset: positive offset adds warm (amber) tint, negative offset adds cool (blue) tint. The offset is applied asymmetrically to U and V to follow the approximate locus direction.

### What Is Tint Correction?

The **tint** axis is perpendicular to the color temperature axis on the chrominance plane. While color temperature moves between blue and amber, tint moves between green and magenta. This orthogonal correction compensates for light sources that don't fall exactly on the Planckian locus — particularly fluorescent and LED lighting, which often have a green or magenta cast. Whitebal applies tint as an equal offset to both U and V channels.

### What Is Saturation?

**Saturation** is the colorfulness of a signal — how far its chrominance extends from neutral gray. A fully desaturated signal is monochrome; a fully saturated signal has maximum chromatic intensity. Whitebal implements saturation as a simple multiplicative gain on U and V: values below 1.0 desaturate, values above 1.0 boost color intensity. This is applied after the color temperature/tint shift.


---

## Signal Flow

Color Temperature Shift → Tint Shift → Saturation → ... → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Color Temperature Shift ────────────────────────────────────
│   ├─ 1. Compute signed offset  (pot centered at 512)
│   ├─ 2. Wide Range: use full offset; Normal: offset/2
│   ├─ 3. U' = U − offset        (warm subtracts from U)
│   └─ 4. V' = V + offset        (warm adds to V)
│
├── Tint Shift ─────────────────────────────────────────────────
│   ├─ 1. Compute tint offset    (pot centered at 512)
│   ├─ 2. U' = U' + tint/2       (green-magenta axis)
│   └─ 3. V' = V' + tint/2
│
├── Saturation ─────────────────────────────────────────────────
│   ├─ U' = (U' − 512) × sat / 512 + 512
│   └─ V' = (V' − 512) × sat / 512 + 512
│
├── UV Invert (optional) ──────────────────────────────────────
│   └─ U' = 1023 − U'; V' = 1023 − V'
│
├── Contrast ───────────────────────────────────────────────────
│   └─ Y' = (Y − 512) × contrast / 512 + brightness
│
├── Y Gain ─────────────────────────────────────────────────────
│   └─ Y' = Y' × y_gain / 512   (clamp to 0–1023)
│
├── Y Invert (optional) ───────────────────────────────────────
│   └─ Y' = 1023 − Y'
│
├── Output ─────────────────────────────────────────────────────
│   ├─ Clamp all channels to 0–1023
│   └─ Bypass mux
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through with 6-clock delay
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The processing chain is entirely feedforward — no memory, no line buffers, no BRAMs. Each pixel is independently transformed in a 6-stage pipeline. Color temperature is applied first (shifting U down and V up for warmth, or vice versa for cool), then tint adds a perpendicular correction. Saturation scales the shifted UV around 512. The Y channel is processed separately: contrast expands/compresses the range around 512, brightness adds a DC offset, and Y Gain provides a final multiplicative scale. All operations use 10-bit signed arithmetic with clamping to the 0–1023 output range.

---

## Parameter Reference

<img src={whitebal_control_panel} alt="Videomancer front panel with White Balance loaded"/>
*Videomancer's front panel with White Balance active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Color Temp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the color temperature offset. The knob is centered at 50% (512) for neutral — no chrominance shift. Turning above center warms the image (adds amber: subtracts from U, adds to V). Turning below center cools the image (adds blue: adds to U, subtracts from V). The offset magnitude is halved in Normal Range mode (Switch 7) for fine adjustment, or used at full value in Wide Range mode for extreme color grading.

---

#### Knob 2 — Tint
| Property | Value |
|----------|-------|
| Range | -100% – 100% |
| Default | 0% |
| Suffix | % |

Controls the tint offset — the green-magenta axis perpendicular to color temperature. Centered at 50% for no tint shift. Above center pushes toward magenta (adds to both U and V). Below center pushes toward green (subtracts from both U and V). The tint offset is always halved (divided by 2) for fine control, regardless of the Range toggle.

---

#### Knob 3 — Y Gain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the Y Gain — a final luminance multiplier applied after contrast and brightness. At 50% (512), gain is unity. Above 50%, the signal is amplified (brighter). Below 50%, it is attenuated (darker). The gain is a simple multiply-and-shift operation with clamping to 0–1023. This provides an overall brightness scaling independent of the contrast/brightness curve.

---

#### Knob 4 — Saturation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls chrominance saturation. At center (50%), saturation is unity. Above center, UV values are expanded away from neutral (boosted saturation — more vivid colors). Below center, UV values are compressed toward 512 (reduced saturation — muted or monochrome). At minimum, the signal is completely desaturated.

---

#### Knob 5 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the contrast — the expansion or compression of the luminance range around midpoint (512). At 50%, contrast is unity. Above 50%, the range is expanded (brighter brights and darker darks). Below 50%, the range is compressed toward mid-gray. The formula is `Y' = (Y - 512) × contrast / 512 + brightness`.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC brightness offset to the luminance after contrast scaling. At 50%, no offset. Above center brightens the entire image; below center darkens it. This is the "lift" control in color grading terminology — it shifts the entire tonal curve up or down.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Range** | Normal | Wide |
| **8 — Auto Sat** | Off | On |
| **9 — Y Invert** | Off | On |
| **10 — UV Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control the color temperature range, automatic saturation compensation, Y inversion, UV inversion, and bypass. The Range switch (7) is the most technically significant — it determines whether the color temperature offset is applied at full or half strength.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the corrected output and the original input via the hardware interpolator. At 100%, the full correction is applied. Lowering the fader blends back toward the uncorrected original — useful for dialing in partial corrections.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all White Balance processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises demonstrate corrective white balance, creative color grading, and the separate luminance processing controls.

### Exercise 1: Corrective White Balance

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: whitebal_source1_ballerina, after: whitebal_ex1_s1 },
    { label: "Sunset", before: whitebal_source2_sunset, after: whitebal_ex1_s2 },
    { label: "Clouds", before: whitebal_source3_clouds, after: whitebal_ex1_s3 },
    { label: "Pattern", before: whitebal_source4_pattern, after: whitebal_ex1_s4 },
    { label: "Man", before: whitebal_source5_man, after: whitebal_ex1_s5 },
    { label: "Paint", before: whitebal_source6_paint, after: whitebal_ex1_s6 },
  ]}
/>
*Corrective White Balance — simulated result across source images.*
**Source**: Camera feed under tungsten (warm) or fluorescent (cool/green) lighting, showing skin tones or a white reference surface.

**What You'll Create**: Correct the color temperature to achieve neutral white balance.

1. **Identify cast**: Under tungsten lighting, the image has a warm amber cast (excess V, deficit U). Under fluorescent, it has a cool greenish cast.
2. **Color Temp**: For tungsten, turn Color Temp below center (cool shift) to compensate. For fluorescent, turn above center slightly.
3. **Normal Range**: Keep Range at Normal (Switch 7) for fine adjustment.
4. **Tint**: If a green or magenta cast remains after temperature correction, adjust Tint. Fluorescent often needs a slight magenta push (above center).
5. **Saturation**: If colors appear washed out after correction, boost Saturation slightly above 50%.
6. **Bypass compare**: Toggle Bypass to compare corrected vs uncorrected. White and neutral gray surfaces should appear truly neutral.

**Key concepts**: Color temperature corrects along the blue-amber axis, Tint corrects along the green-magenta axis, Normal Range provides fine adjustment, two-axis correction handles most illuminant mismatches

---

### Exercise 2: Creative Color Grading (Warm/Cool Look)

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: whitebal_source1_ballerina, after: whitebal_ex2_s1 },
    { label: "Sunset", before: whitebal_source2_sunset, after: whitebal_ex2_s2 },
    { label: "Clouds", before: whitebal_source3_clouds, after: whitebal_ex2_s3 },
    { label: "Pattern", before: whitebal_source4_pattern, after: whitebal_ex2_s4 },
    { label: "Man", before: whitebal_source5_man, after: whitebal_ex2_s5 },
    { label: "Paint", before: whitebal_source6_paint, after: whitebal_ex2_s6 },
  ]}
/>
*Creative Color Grading (Warm/Cool Look) — simulated result across source images.*
**Source**: Landscape, portrait, or narrative video — content where mood-setting color shifts enhance the visual story.

**What You'll Create**: Apply intentional creative color shifts for cinematic color grading.

1. **Wide Range**: Enable Wide Range (Switch 7). The full offset range becomes available.
2. **Warm look**: Turn Color Temp to ~65%. The image takes on a warm, golden-hour amber cast.
3. **Saturation boost**: Set Saturation to ~65%. Colors become more vivid.
4. **Contrast push**: Set Contrast to ~60%. Slight expansion enhances the cinematic look.
5. **Cool look**: Now turn Color Temp to ~35%. The same scene takes on a cold, blue-toned look.
6. **Tint for cinema**: Add a slight magenta tint (~55%) for the classic warm/magenta teal-and-orange split.
7. **Mix/fade**: Use Mix to blend the graded look with the original at ~70% for a subtler effect.

**Key concepts**: Wide Range enables extreme shifts for creative use, combined temperature + tint creates cinematic color palettes, saturation and contrast enhance the effect

---

### Exercise 3: Luminance Processing Chain

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: whitebal_source1_ballerina, after: whitebal_ex3_s1 },
    { label: "Sunset", before: whitebal_source2_sunset, after: whitebal_ex3_s2 },
    { label: "Clouds", before: whitebal_source3_clouds, after: whitebal_ex3_s3 },
    { label: "Pattern", before: whitebal_source4_pattern, after: whitebal_ex3_s4 },
    { label: "Man", before: whitebal_source5_man, after: whitebal_ex3_s5 },
    { label: "Paint", before: whitebal_source6_paint, after: whitebal_ex3_s6 },
  ]}
/>
*Luminance Processing Chain — simulated result across source images.*
**Source**: Any input — high-contrast content makes the effects most visible.

**What You'll Create**: Explore the Y Gain, Contrast, and Brightness controls independently, then combine with inversion.

1. **Neutral color**: Set Color Temp and Tint to center (50%). Only luminance processing is active.
2. **Contrast**: Sweep Contrast from 0% to 100%. At minimum, the image compresses to flat gray. At maximum, stark black-and-white contrast with hard clipping.
3. **Brightness**: At high contrast, sweep Brightness. The clipping point shifts up and down.
4. **Y Gain**: Return Contrast to 50%, then sweep Y Gain. The overall luminance scales uniformly.
5. **Y Invert**: Enable Y Invert (Switch 9). The image becomes a luminance negative — dark becomes light.
6. **UV Invert**: Enable UV Invert (Switch 10). Colors flip to complements while luminance stays inverted. The image is now a full negative.
7. **Combined**: Disable Y Invert but keep UV Invert. Luminance is normal but colors are complementary — a chrominance-only negative.

**Key concepts**: Contrast expands/compresses around midpoint, brightness shifts the DC level, Y Gain scales overall amplitude, Y Invert and UV Invert produce selective negatives

---


## Tips

- **Tint for fluorescent**: Fluorescent lighting typically needs a magenta tint push (~55–60%) after temperature correction.
- **Saturation below 50% is beautiful**: Subtle desaturation (40–45%) creates a pleasing, film-like muted palette.
- **Chain order matters**: Place Whitebal early in the processing chain (before effects) for corrective use, or late (after effects) for creative grading.
- **UV Invert for split toning**: Combine UV Invert with partial Mix to blend complementary colors with the original for a split-tone look.

---

## Glossary

| Term | Definition |
|------|------------|
| **Blackbody Radiator** | A theoretical object that emits light whose color depends only on its temperature, defining the color temperature scale. |
| **Color Temperature** | A measurement (in Kelvin) of the hue of a light source, ranging from warm amber (~2700K) through neutral daylight (~5600K) to cool blue (~10000K). |
| **Complement** | The opposite color on the color wheel; computed by subtracting U and V from their maximum value (1023). |
| **Contrast** | The tonal range of an image; high contrast means wide separation between brightest and darkest regions. |
| **Planckian Locus** | The curve traced by blackbody radiation on a chrominance diagram as temperature varies, passing through amber, white, and blue. |
| **Saturation** | The colorfulness or chromatic intensity of a signal; desaturated signals are gray, fully saturated signals have vivid color. |
| **Tint** | The green-magenta axis of color correction, perpendicular to the blue-amber color temperature axis. |
| **White Balance** | The process of adjusting color temperature and tint so that neutral objects appear truly neutral (gray/white) under a given illuminant. |
| **Y Gain** | A multiplicative luminance scaling factor applied after contrast and brightness, controlling overall signal amplitude. |

---
