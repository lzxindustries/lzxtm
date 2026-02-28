---
draft: true
sidebar_position: 236
slug: /instruments/videomancer/silhouette
title: "Silhouette"
image: /img/instruments/videomancer/silhouette/silhouette_hero.png
---

import silhouette_before_after from '/img/instruments/videomancer/silhouette/silhouette_before_after.png';
import silhouette_control_panel from '/img/instruments/videomancer/silhouette/silhouette_control_panel.png';
import silhouette_exercise1_result from '/img/instruments/videomancer/silhouette/silhouette_exercise1_result.png';
import silhouette_exercise2_result from '/img/instruments/videomancer/silhouette/silhouette_exercise2_result.png';
import silhouette_exercise3_result from '/img/instruments/videomancer/silhouette/silhouette_exercise3_result.png';
import silhouette_hero from '/img/instruments/videomancer/silhouette/silhouette_hero.png';
import silhouette_source1_kodim02 from '/img/instruments/videomancer/silhouette/silhouette_source1_kodim02.png';
import silhouette_source2_kodim07 from '/img/instruments/videomancer/silhouette/silhouette_source2_kodim07.png';
import silhouette_source3_kodim01_bw from '/img/instruments/videomancer/silhouette/silhouette_source3_kodim01_bw.png';

# Silhouette

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={silhouette_hero} alt="Silhouette hero image"/>
*Silhouette extracting a luminance key from a high-contrast portrait, replacing keyed regions with a warm amber matte colour.*
<img src={silhouette_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Silhouette applied.*

---

## Overview

Every image is a landscape of brightness and colour values. Silhouette draws a boundary through that landscape — pixels on one side of the threshold pass through unaltered, while pixels on the other side are replaced by a flat matte colour. The result is a composited image where parts of the original video appear to float on top of (or cut out from) a solid-colour background.

The program implements a complete keyer with two key modes — *luma* and *chroma* — plus adjustable span (softness), gain, and independent per-channel matte colour selection. In luma mode, the key is derived from the absolute distance between each pixel's brightness and a threshold point. In chroma mode, the key is derived from the maximum of the U and V colour distances from their respective thresholds. The name *Silhouette* evokes the art of cutting profiles from black paper — reducing complex scenes to their essential outlines.

At extreme settings the key becomes a hard binary mask, producing clean silhouette cut-outs. With moderate span and gain, the key transitions are soft and gradual, blending the matte colour into the source image for compositing and overlay effects. The per-channel matte controls allow any arbitrary replacement colour in the YUV domain.

---

## Background

### What Is a Luma Key?

A **luma key** generates an alpha (transparency) signal from the brightness channel of the input video. Pixels whose luminance is close to a chosen threshold become transparent (keyed), while pixels far from the threshold remain opaque. Television engineers have used luma keying since the earliest days of electronic switching — it is the simplest form of video keying, requiring only a comparator and a threshold level.

Silhouette's luma key computes `|Y - threshold|` for every pixel, producing a distance signal that increases the further a pixel's brightness is from the threshold. This distance is then shaped by the span and gain controls before being used as an alpha channel for compositing.

### What Is a Chroma Key?

A **chroma key** extends the same principle to the colour channels. Instead of keying on brightness alone, the program computes `|U - threshold|` and `|V - threshold|` and takes the maximum of those two distances. This creates a key that responds to colour position in the UV plane — pixels near the threshold colour become transparent, while pixels of different hues remain opaque. Chroma keying is the basis of the classic "green screen" effect used in television and film production.

### What Is Span (Soft-Clip)?

The span control sets a *deadband* below which the key distance is forced to zero. Think of it as a clip level: only distances above `(1023 - span)` contribute to the key. When span is at maximum (1023), the clip level is 0 and all distance values pass through — producing a very soft, gradual key. When span is at minimum (0), the clip level is 1023 and virtually nothing passes — producing a hard cut-off. Span is the primary control for adjusting the "softness" or "feather" of the key edge.

### What Is Key Gain?

After span clipping, the surviving distance signal is multiplied by the key gain value. This multiplication scales the key alpha — higher gain makes a narrower (harder) key for a given span setting, while lower gain makes a wider (softer) key. The gain range toggle selects between 1× and 16× scaling, extending the usable range dramatically. At 16× gain, even small distance values produce opaque key regions, useful for tight keys around specific luminance or chrominance values.

### What Is Interpolator Compositing?

The final compositing stage uses three `interpolator_u` instances (one per YUV channel) to crossfade between the matte colour and the source video based on the key alpha. Where alpha is 0 (keyed region), the output shows the matte colour. Where alpha is 1023 (non-keyed region), the output shows the original source. Intermediate alpha values produce a smooth blend — the soft edge of the silhouette.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Conditioning ────────────────────────────────
│   ├─ Optional luma invert (bitwise NOT of Y)
│   └─ Pass U, V unchanged
│
├── Stage 2: Absolute Difference ───────────────────────────────
│   ├─ diff_y = |Y_cond - thresh_yu|
│   ├─ diff_u = |U - thresh_yu|
│   └─ diff_v = |V - thresh_v|
│
├── Stage 3: Key Type Selection + Span ─────────────────────────
│   ├─ Luma mode:   distance = diff_y
│   ├─ Chroma mode: distance = max(diff_u, diff_v)
│   ├─ clip_level = 1023 - span
│   └─ key_raw = max(0, distance - clip_level)
│
├── Stage 4: Gain Multiply ─────────────────────────────────────
│   └─ key_product = key_raw × key_gain  (20-bit)
│
├── Stage 5: Scale + Clamp + Invert ────────────────────────────
│   ├─ 1x range:  alpha = product >> 10
│   ├─ 16x range: alpha = product >> 6  (clamp 1023)
│   └─ Key invert: alpha = 1023 - alpha
│
├── Delay: 4-clock video pipeline ──────────────────────────────
│   └─ Align conditioned Y/U/V with key alpha
│
├── Stages 6–9: Interpolator Compositing ───────────────────────
│   ├─ Y out = lerp(matte_y, source_y, alpha)
│   ├─ U out = lerp(matte_u, source_u, alpha)
│   └─ V out = lerp(matte_v, source_v, alpha)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field) with matched delay
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The key alpha generation pipeline (stages 1–5) and the video delay pipeline run in parallel. The video delay carries the conditioned source Y/U/V forward by exactly 4 clocks so that it arrives at the interpolator inputs simultaneously with the key alpha from stage 5. The interpolator treats the matte colour as input `a` (shown when alpha = 0, keyed region) and the delayed source as input `b` (shown when alpha = 1023, non-keyed region). This means that *increasing* the key alpha reveals *more* of the original source — unintuitive at first, but consistent with the convention that alpha = full means fully opaque (source visible).

---

## Parameter Reference

<img src={silhouette_control_panel} alt="Videomancer front panel with Silhouette loaded"/>
*Videomancer's front panel with Silhouette active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Span
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the span (softness) of the key edge. At 0%, the clip level is at maximum and virtually no key signal passes through — the output is almost entirely the original source. As you increase Span toward 100%, the clip level drops and more of the distance signal contributes to the key alpha, widening the soft transition zone between keyed and non-keyed regions. This is the primary control for adjusting how gradually the matte colour blends into the source.

---

#### Knob 2 — Threshold Y/U
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the key threshold for the Y channel (in luma mode) and the U channel (in chroma mode). In luma mode, this determines the brightness value around which the key operates — pixels at this brightness are fully keyed, and pixels further from it become progressively more opaque. In chroma mode, this same register sets the U threshold for the chroma distance calculation. The threshold acts as the centre point of the key.

---

#### Knob 3 — Threshold V
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the V channel threshold for chroma keying. In luma mode, this control has no visible effect because only the Y distance is used. In chroma mode, the key distance is `max(|U - thresh_yu|, |V - thresh_v|)`, so this control determines the V-axis centre point of the chroma key. Together with Threshold Y/U, it defines the target colour in the UV plane.

---

#### Knob 4 — Y Matte
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the Y (luminance) component of the matte replacement colour. This controls the brightness of the flat colour that replaces keyed regions. At 0% the matte is black, at 50% it is mid-grey, and at 100% it is white. Combined with U Matte and V Matte, any colour in the YUV gamut can be specified as the replacement.

---

#### Knob 5 — U Matte
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the U (blue-difference chrominance) component of the matte colour. At 50% (register 512), the matte has neutral U chrominance. Values below 50% shift the matte toward yellow, values above 50% shift it toward blue. This operates independently from V Matte, so you can dial in arbitrary target colours by adjusting U and V together.

---

#### Knob 6 — V Matte
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the V (red-difference chrominance) component of the matte colour. At 50% (register 512), the matte has neutral V chrominance. Values below 50% shift the matte toward cyan-green, values above 50% shift it toward red-magenta. With Y Matte, U Matte, and V Matte together, any colour in the broadcast YUV space can be produced as the replacement fill.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Key Type** | Luma | Chroma |
| **8 — Key Invert** | Off | On |
| **9 — Gain Range** | 1x | 16x |
| **10 — Luma Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control the key generation mode and pipeline options. Key Type selects between two fundamentally different keying algorithms. Key Invert flips which side of the threshold is keyed. Gain Range extends the key gain multiplier by 16×. Luma Invert preprocesses the brightness channel before key computation. Bypass routes the input directly to the output for A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Key Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the key gain multiplier applied after span clipping. Higher values produce more opaque key regions for a given distance — effectively tightening the key boundary. At maximum (100%), the raw key signal is scaled at full strength. At 0%, no key signal passes through and the output is entirely the original source regardless of other settings. This is the primary "amount" control for the overall keying effect.

---

## Guided Exercises

These exercises progress from basic luma keying through chroma keying to advanced compositing. Each introduces new controls while building on previously learned concepts.

### Exercise 1: Basic Luma Silhouette

<img src={silhouette_exercise1_result} alt="Basic Luma Silhouette result"/>
*Basic Luma Silhouette — simulated result across source images.*
**Source**: High-contrast black-and-white footage or a test pattern with strong brightness differences (e.g., white text on black background).

**Objective**: Learn luma keying fundamentals — threshold placement, span softness, and gain control.

1. **Set the threshold**: Adjust Threshold Y/U to approximately 50% — the midpoint of the brightness range.
2. **Open the span**: Increase Span to about 70%. You should see mid-grey regions begin to show the matte colour (default mid-grey).
3. **Set a visible matte**: Turn Y Matte to 0% (black) or 100% (white) to clearly see which regions are keyed.
4. **Adjust gain**: Sweep Key Gain from 0% to 100%. Watch the key edge sharpen as gain increases.
5. **Try Key Invert**: Toggle Key Invert to swap which side of the threshold is keyed.
6. **16× gain**: Enable Gain Range to 16× and reduce Key Gain. Notice how much tighter the key becomes.

**Key concepts**: Luma threshold defines the brightness centre point of the key, span controls edge softness, gain controls overall key strength

---

### Exercise 2: Chroma Key Compositing

<img src={silhouette_exercise2_result} alt="Chroma Key Compositing result"/>
*Chroma Key Compositing — simulated result across source images.*
**Source**: Footage with a strong, saturated colour (e.g., a red object on a neutral background, or footage shot against a coloured backdrop).

**Objective**: Explore chroma keying — removing a specific colour from the image and replacing it with a custom matte colour.

1. **Switch to chroma mode**: Set Key Type to Chroma.
2. **Target the colour**: Adjust Threshold Y/U and Threshold V to match the U and V values of the colour you want to key. For a saturated red: Threshold Y/U ~50% (neutral U), Threshold V ~80% (high V).
3. **Open the span**: Set Span to ~60% to begin seeing the key effect.
4. **Choose matte colour**: Set Y Matte to ~50%, U Matte to ~30%, V Matte to ~30% for a blue-green matte replacement.
5. **Refine with gain**: Increase Key Gain to tighten the chroma key around the target colour.
6. **Invert**: Toggle Key Invert to see the complementary key — now only the target colour remains visible.

**Key concepts**: Chroma key uses max(|U-thresh|, |V-thresh|) for colour-based keying, U and V thresholds define target colour, matte controls set replacement colour

---

### Exercise 3: Soft Compositing with Luma Invert

<img src={silhouette_exercise3_result} alt="Soft Compositing with Luma Invert result"/>
*Soft Compositing with Luma Invert — simulated result across source images.*
**Source**: A video scene with a range of brightness values (landscape, portrait, or abstract footage).

**Objective**: Combine luma inversion with soft key compositing to create painterly overlay effects.

1. **Enable Luma Invert**: Toggle Luma Invert On. The key now sees an inverted brightness map — dark areas register as bright for keying purposes.
2. **Set moderate span**: Span ~50% for a soft blend.
3. **Choose a warm matte**: Y Matte ~60%, U Matte ~40%, V Matte ~70% for a warm amber tone.
4. **Moderate gain**: Key Gain ~50% with 1× range for a gentle composite.
5. **Compare**: Toggle Key Invert to swap the composite relationship. Notice how Luma Invert and Key Invert produce different results — one reverses input, the other reverses output.
6. **Sweep threshold**: Move Threshold Y/U slowly from 0% to 100%. Watch the composite "slide" across the image as different brightness regions enter and exit the key zone.

**Key concepts**: Luma Invert reverses brightness before keying (preprocessing), Key Invert reverses alpha after keying (post-processing), soft span creates gradual compositing blends

---


## Tips

- **Span is your softness control**: Think of Span as "feather radius." Higher span = softer edge. Use it before reaching for gain to shape the key transition.
- **Key Gain is your strength control**: Once you have the right softness via Span, use Key Gain to set how strongly the key replaces the source with matte.
- **Luma Invert ≠ Key Invert**: Luma Invert flips the Y channel *before* the distance computation (changes *what* gets keyed). Key Invert flips the alpha *after* gain (changes *how* the key composites). They produce different results and can be combined.
- **16× gain for tight keys**: When you need a narrow key band — keying on a specific brightness or colour without affecting nearby values — use 16× Gain Range with a low Key Gain setting.
- **Matte colour as creative tool**: The YUV matte controls can produce any colour, not just neutral tones. Use saturated matte colours for graphic design and compositing effects.
- **Feedback loops**: Route the output back to the input to create recursive keying — the key operates on its own output, producing evolving silhouette patterns.
- **Threshold sweep for animation**: Slowly modulating Threshold Y/U with an external control creates a "wipe" effect where the key region moves through the brightness range.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha** | A transparency value (0 = fully transparent / keyed, 1023 = fully opaque / source visible) used for compositing two signals together. |
| **Chroma** | The colour information in a video signal, encoded as U (blue-difference) and V (red-difference) components in YUV colour space. |
| **Chroma Key** | A keying method that derives the transparency signal from colour-channel distances rather than brightness. |
| **Compositing** | Combining two video signals into one by blending them according to an alpha (transparency) map. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interpolator** | A hardware module that linearly crossfades between two input values based on a third value (the alpha or mix control). |
| **Key** | A signal derived from the input video that determines which regions are transparent and which are opaque. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Luma Key** | A keying method that derives the transparency signal from the absolute luminance distance from a threshold. |
| **Matte** | A flat replacement colour that fills the keyed (transparent) regions of the output image. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Span** | The soft-clip deadband below which key distance is forced to zero, controlling key edge softness. |
| **YUV** | A colour encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
