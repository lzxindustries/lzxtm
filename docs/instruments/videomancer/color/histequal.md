---
draft: true
sidebar_position: 137
slug: /instruments/videomancer/histequal
title: "Histogram EQ"
image: /img/instruments/videomancer/histequal/histequal_hero_s1.png
description: "Not all video signals use their full dynamic range."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import histequal_control_panel from '/img/instruments/videomancer/histequal/histequal_control_panel.png';
import histequal_source1_field from '/img/instruments/videomancer/histequal/histequal_source1_field.png';
import histequal_source2_ballerina from '/img/instruments/videomancer/histequal/histequal_source2_ballerina.png';
import histequal_source3_collage from '/img/instruments/videomancer/histequal/histequal_source3_collage.png';
import histequal_source4_pattern from '/img/instruments/videomancer/histequal/histequal_source4_pattern.png';
import histequal_source5_girl from '/img/instruments/videomancer/histequal/histequal_source5_girl.png';
import histequal_source6_paint from '/img/instruments/videomancer/histequal/histequal_source6_paint.png';
import histequal_hero_s1 from '/img/instruments/videomancer/histequal/histequal_hero_s1.png';
import histequal_hero_s2 from '/img/instruments/videomancer/histequal/histequal_hero_s2.png';
import histequal_hero_s3 from '/img/instruments/videomancer/histequal/histequal_hero_s3.png';
import histequal_hero_s4 from '/img/instruments/videomancer/histequal/histequal_hero_s4.png';
import histequal_hero_s5 from '/img/instruments/videomancer/histequal/histequal_hero_s5.png';
import histequal_hero_s6 from '/img/instruments/videomancer/histequal/histequal_hero_s6.png';
import histequal_ex1_s1 from '/img/instruments/videomancer/histequal/histequal_ex1_s1.png';
import histequal_ex1_s2 from '/img/instruments/videomancer/histequal/histequal_ex1_s2.png';
import histequal_ex1_s3 from '/img/instruments/videomancer/histequal/histequal_ex1_s3.png';
import histequal_ex1_s4 from '/img/instruments/videomancer/histequal/histequal_ex1_s4.png';
import histequal_ex1_s5 from '/img/instruments/videomancer/histequal/histequal_ex1_s5.png';
import histequal_ex1_s6 from '/img/instruments/videomancer/histequal/histequal_ex1_s6.png';
import histequal_ex2_s1 from '/img/instruments/videomancer/histequal/histequal_ex2_s1.png';
import histequal_ex2_s2 from '/img/instruments/videomancer/histequal/histequal_ex2_s2.png';
import histequal_ex2_s3 from '/img/instruments/videomancer/histequal/histequal_ex2_s3.png';
import histequal_ex2_s4 from '/img/instruments/videomancer/histequal/histequal_ex2_s4.png';
import histequal_ex2_s5 from '/img/instruments/videomancer/histequal/histequal_ex2_s5.png';
import histequal_ex2_s6 from '/img/instruments/videomancer/histequal/histequal_ex2_s6.png';
import histequal_ex3_s1 from '/img/instruments/videomancer/histequal/histequal_ex3_s1.png';
import histequal_ex3_s2 from '/img/instruments/videomancer/histequal/histequal_ex3_s2.png';
import histequal_ex3_s3 from '/img/instruments/videomancer/histequal/histequal_ex3_s3.png';
import histequal_ex3_s4 from '/img/instruments/videomancer/histequal/histequal_ex3_s4.png';
import histequal_ex3_s5 from '/img/instruments/videomancer/histequal/histequal_ex3_s5.png';
import histequal_ex3_s6 from '/img/instruments/videomancer/histequal/histequal_ex3_s6.png';

# Histogram EQ

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: histequal_source1_field, after: histequal_hero_s1 },
    { label: "Ballerina", before: histequal_source2_ballerina, after: histequal_hero_s2 },
    { label: "Collage", before: histequal_source3_collage, after: histequal_hero_s3 },
    { label: "Pattern", before: histequal_source4_pattern, after: histequal_hero_s4 },
    { label: "Girl", before: histequal_source5_girl, after: histequal_hero_s5 },
    { label: "Paint", before: histequal_source6_paint, after: histequal_hero_s6 },
  ]}
/>
*Histequal applying per-scanline auto-contrast with adaptive clipping to expand the dynamic range of crushed and low-contrast video signals.*

---

## Overview

Not all video signals use their full dynamic range. Footage shot in flat lighting profiles, old VHS tapes, or signals passing through multiple analog stages often arrive with compressed tonality — the darkest pixels never reach true black, and the brightest pixels never reach true white. The histogram of such a signal is bunched in the middle, leaving the extremes unused. **Histogram equalization** is the standard technique for fixing this: it remaps pixel values so that the output histogram is as uniform as possible, spreading the available tones evenly across the full range.

Histequal implements a simplified form of this technique operating on a per-scanline basis. Rather than computing a full histogram and cumulative distribution function (which would require far more memory than an iCE40 FPGA provides), it tracks the minimum and maximum luminance on each scanline and stretches the range between them to fill the full 0–1023 output space. The effect is **auto-contrast**: each scanline independently expands its tonal range to use the maximum available dynamic range.

The Clip Limit control allows clipping the tracked min/max inward, ignoring extreme outlier pixels. The Strength control blends between the equalized and original signal. A Black Level control lifts the floor of the equalized output. The result ranges from subtle shadow-and-highlight extension to aggressive per-line auto-contrast that dramatically reshapes the image's tonal character, with visible line-by-line variation creating a distinctive scanning-beam aesthetic.

---

## Background

### What Is Histogram Equalization?

**Histogram equalization** is an image processing technique that redistributes pixel values to approximate a uniform histogram — one where every brightness level is equally represented. The standard algorithm computes the cumulative distribution function (CDF) of the input histogram and uses it as a transfer function. Pixels bunch at a given brightness level get spread apart; brightness levels with few pixels get compressed together. The result is an image with maximized contrast. Histequal approximates this using per-scanline min/max tracking rather than a full histogram, which is computationally much cheaper but achieves a similar contrast-expansion effect.

### What Is Auto-Contrast?

**Auto-contrast** (or auto-levels) is a simpler variant of histogram equalization. Instead of computing a full CDF, it identifies the minimum and maximum values in the data and linearly stretches that range to fill the full output range. If the darkest pixel on a scanline is 200 and the brightest is 800, auto-contrast maps 200→0 and 800→1023, with everything in between linearly interpolated. Histequal implements this per-scanline, so each horizontal line gets its own independent stretch — resulting in line-by-line tonal variation that is visible as a scanning-beam effect on signals with varying dynamic range.

### What Is Clip Limiting?

Without clipping, a single very bright or very dark pixel on a scanline can anchor the min or max, preventing the rest of the line from being stretched effectively. **Clip limiting** narrows the tracked range by clipping a portion of the extremes — ignoring the bottom and top few percent of values. This prevents outliers from dominating the stretch and produces a more aggressive, higher-contrast expansion of the main body of pixel values. Histequal implements this as an inward offset applied to the tracked min and max before the stretch computation.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel (Ping-Pong Tracking) ─────────────────────────────
│   │
│   ├─ Line N: Track min & max luminance (rolling min/max)
│   │
│   └─ Line N+1: Apply stretch using Line N's min/max
│       │
│       ├─ 1. Clip Boundaries     (inward offset by clip_limit)
│       ├─ 2. Clamp to Range      (clip input to [min+clip, max-clip])
│       ├─ 3. Center              (subtract clipped min)
│       ├─ 4. Scale ×1023         (expand to full range)
│       ├─ 5. Divide by Range     (shift-based approximation)
│       ├─ 6. Black Level Offset  (lift floor)
│       └─ 7. Strength Blend      (original ↔ equalized)
│
├── UV Channels ────────────────────────────────────────────────
│   │
│   └─ Saturation Adjustment    (scale UV around neutral)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

Two key design choices shape the effect: (1) The ping-pong buffer — min/max are tracked on line N and applied to line N+1. This creates a one-line latency but allows the min/max computation and the stretch application to operate simultaneously on different scanlines. (2) The division is approximated using cascading threshold checks (512, 256, 128, 64, 32) rather than a true divider, which would be too expensive for the iCE40. This approximation introduces slight quantization in the stretch mapping, but the error is imperceptible at video rates.

---

## Parameter Reference

<img src={histequal_control_panel} alt="Videomancer front panel with Histogram EQ loaded"/>
*Videomancer's front panel with Histogram EQ active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Strength
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the blend between the equalized and original luminance. At 100%, the output is fully equalized — each scanline's dynamic range is maximally stretched. At 0%, the output is the original signal with no equalization. Intermediate values mix the two, providing a subtle contrast enhancement rather than a full equalization. This is the primary control for the intensity of the auto-contrast effect.

---

#### Knob 2 — Clip Limit
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Sets the clip boundary as a fraction of the tracked min/max range. At 0%, no clipping — the full min-to-max range is used for the stretch. At higher values, the tracked range is narrowed by clipping inward from both extremes, ignoring outlier pixels and producing a more aggressive stretch of the midtone values. High clip limit combined with high strength creates extreme per-line auto-contrast that can dramatically reshape the image.

---

#### Knob 3 — Sat Adj
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adjusts the saturation of the UV channels relative to their equalized luminance. At center, chrominance passes unchanged. Above center, saturation is boosted to compensate for the contrast increase in the Y channel. Below center, saturation is reduced. This control prevents the equalized image from looking under- or over-saturated relative to the enhanced luminance contrast.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies gain around the midpoint (512) to the luminance channel after equalization. Values above center increase contrast further, pushing bright pixels brighter and dark pixels darker on top of the auto-contrast stretch. Values below center reduce contrast, softening the equalized result. This stacks with the equalization itself, allowing fine control over the final tonal separation.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC offset to the equalized luminance. At center, no offset. Above center, the entire image brightens. Below center, it darkens. Applied after the equalization and contrast stages, this control sets the overall exposure level of the output.

---

#### Knob 6 — Black Level
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Lifts the floor of the equalized range. At 0%, the darkest equalized pixels map to true black (0). As Black Level increases, the floor rises, preventing any pixel from going fully dark. This is useful for creating a "lifted blacks" look where even the shadows retain some luminance, mimicking the tonal characteristics of certain film stocks or CRT monitors.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Bins** | 64 | 128 |
| **8 — Show Hist** | Off | On |
| **9 — Y Invert** | Off | On |
| **10 — Sat Comp** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control the equalization resolution, display modes, and processing options. Bins selects the tracking precision. Show Hist replaces output with a diagnostic visualization. Y Invert provides luminance polarity reversal. Sat Comp enables automatic saturation compensation. Bypass enables instant comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the equalized output and the original input signal. At 100%, the full equalized signal passes. Lowering the fader blends the original back in. At 0%, the output is the unprocessed input.

---

## Guided Exercises

These exercises progress from gentle contrast enhancement to aggressive per-line auto-contrast that reveals the scanning-beam character of the equalization algorithm.

### Exercise 1: Gentle Auto-Contrast

<BeforeAfterSlider
  sources={[
    { label: "Field", before: histequal_source1_field, after: histequal_ex1_s1 },
    { label: "Ballerina", before: histequal_source2_ballerina, after: histequal_ex1_s2 },
    { label: "Collage", before: histequal_source3_collage, after: histequal_ex1_s3 },
    { label: "Pattern", before: histequal_source4_pattern, after: histequal_ex1_s4 },
    { label: "Girl", before: histequal_source5_girl, after: histequal_ex1_s5 },
    { label: "Paint", before: histequal_source6_paint, after: histequal_ex1_s6 },
  ]}
/>
*Gentle Auto-Contrast — simulated result across source images.*
**Source**: Low-contrast footage — indoor scenes, overcast day, or a flat color profile recording.

**Objective**: Apply subtle auto-contrast to expand the available dynamic range without obvious artifacts.

1. **Assess the input**: Enable Bypass and observe the low-contrast source. Note the washed-out shadows and dull highlights.
2. **Full equalization**: Disable Bypass. Set Strength to ~80%, Clip Limit to ~20%. The image immediately snaps to higher contrast as the per-scanline stretch expands shadows and highlights.
3. **Reduce strength**: Lower Strength to ~50% for a more natural-looking enhancement that doesn't over-process the image.
4. **Saturation match**: Adjust Sat Adj until the color intensity matches the original. Enable Sat Comp if the automatic compensation helps.
5. **Black level**: If the shadows are too crushed, increase Black Level to ~15% to lift the darkest values.

**Key concepts**: Auto-contrast stretches the per-scanline dynamic range, clip limiting ignores outliers, strength controls enhancement intensity

---

### Exercise 2: Aggressive Line-by-Line Equalization

<BeforeAfterSlider
  sources={[
    { label: "Field", before: histequal_source1_field, after: histequal_ex2_s1 },
    { label: "Ballerina", before: histequal_source2_ballerina, after: histequal_ex2_s2 },
    { label: "Collage", before: histequal_source3_collage, after: histequal_ex2_s3 },
    { label: "Pattern", before: histequal_source4_pattern, after: histequal_ex2_s4 },
    { label: "Girl", before: histequal_source5_girl, after: histequal_ex2_s5 },
    { label: "Paint", before: histequal_source6_paint, after: histequal_ex2_s6 },
  ]}
/>
*Aggressive Line-by-Line Equalization — simulated result across source images.*
**Source**: Footage with varying dynamic range across different parts of the frame — a scene with bright sky and dark foreground, or a mixed-lighting environment.

**Objective**: Push the per-scanline equalization to create visible line-by-line tonal variation.

1. **Maximum equalization**: Set Strength to 100%, Clip Limit to ~60%. Each scanline independently maxes out its contrast, creating visible line-to-line brightness variation.
2. **Observe the scanning effect**: Look at areas where the dynamic range changes vertically — the auto-contrast creates a visible banding effect as each scanline operates independently.
3. **Diagnostic view**: Enable Show Hist (Switch 8). Observe how the tracked min/max varies per scanline.
4. **Enhance the effect**: Increase Contrast to ~70% to amplify the per-line variation.
5. **Black level sculpting**: Raise Black Level to ~30%. The lifted floor interacts with the aggressive stretch, creating a distinctive high-key look.

**Key concepts**: Per-scanline processing creates visible line variation, high clip limit aggressively stretches midtones, black level lifts the output floor

---

### Exercise 3: Creative Tonal Manipulation

<BeforeAfterSlider
  sources={[
    { label: "Field", before: histequal_source1_field, after: histequal_ex3_s1 },
    { label: "Ballerina", before: histequal_source2_ballerina, after: histequal_ex3_s2 },
    { label: "Collage", before: histequal_source3_collage, after: histequal_ex3_s3 },
    { label: "Pattern", before: histequal_source4_pattern, after: histequal_ex3_s4 },
    { label: "Girl", before: histequal_source5_girl, after: histequal_ex3_s5 },
    { label: "Paint", before: histequal_source6_paint, after: histequal_ex3_s6 },
  ]}
/>
*Creative Tonal Manipulation — simulated result across source images.*
**Source**: Any footage — the effect is independent of content.

**Objective**: Combine equalization with inversion and saturation manipulation for creative tonal effects.

1. **Strong equalization**: Strength ~80%, Clip Limit ~40%.
2. **Invert**: Enable Y Invert (Switch 9). The equalized image inverts — the auto-contrast now stretches the inverted tonal range.
3. **Desaturate**: Lower Sat Adj to ~20%. The high-contrast inverted image becomes nearly monochrome.
4. **Contrast push**: Set Contrast to ~80% for an extreme tonal separation.
5. **Mix blend**: Lower Mix to ~50%. The inverted equalized signal blends with the original, creating a solarization-like effect where tones split and merge.
6. **A/B comparison**: Toggle Bypass repeatedly to compare the creative processing with the original.

**Key concepts**: Inversion reverses the tonal mapping before equalization, low saturation creates graphic monochrome, mix blending creates solarization effects

---


## Tips

- **Strength for subtlety**: Keep Strength at 40–60% for natural-looking contrast enhancement. Full strength creates visible per-line variation.
- **Clip Limit prevents anchor pixels**: A single hot pixel can dominate the auto-contrast. Clip Limit at 20–30% ignores these outliers.
- **Show Hist for diagnostics**: Use Show Hist mode to understand how your source material's dynamic range varies across scanlines before committing to settings.
- **Black Level for mood**: Lifted blacks create a filmic, low-contrast-shadow look even with aggressive equalization on the highlights.
- **Sat Comp is your friend**: Enable Sat Comp whenever using high Strength — it prevents the equalized image from looking unnaturally saturated or desaturated.
- **Per-line variation as aesthetic**: The visible line-by-line tonal bandwidth of aggressive equalization is itself a distinctive visual texture — embrace it as a design element.

---

## Glossary

| Term | Definition |
|------|------------|
| **Auto-Contrast** | A technique that stretches a signal's dynamic range to fill the available output range, based on the observed minimum and maximum values. |
| **CDF** | Cumulative Distribution Function; in histogram equalization, used as a transfer function to remap pixel values for uniform distribution. |
| **Clip Limit** | A threshold that narrows the tracked dynamic range by ignoring extreme outlier values at both ends. |
| **Dynamic Range** | The ratio between the brightest and darkest values in a signal; wider range means more tonal levels are utilized. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Histogram** | A graph showing the distribution of pixel values in an image; bunched histograms indicate low contrast. |
| **Ping-Pong** | A double-buffering technique where tracking occurs on one scanline while processing uses the previous scanline's results. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
