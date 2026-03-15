---
draft: true
sidebar_position: 242
slug: /instruments/videomancer/reagent
title: "Reagent"
image: /img/instruments/videomancer/reagent/reagent_hero.png
description: "Chemistry has a beautiful color language."
---

import reagent_hero from '/img/instruments/videomancer/reagent/reagent_hero.png';
import reagent_animation from '/img/instruments/videomancer/reagent/reagent_animation.gif';
import reagent_control_panel from '/img/instruments/videomancer/reagent/reagent_control_panel.png';
import reagent_exercise1_result from '/img/instruments/videomancer/reagent/reagent_exercise1_result.gif';
import reagent_exercise2_result from '/img/instruments/videomancer/reagent/reagent_exercise2_result.gif';
import reagent_exercise3_result from '/img/instruments/videomancer/reagent/reagent_exercise3_result.gif';

# Reagent

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={reagent_hero} alt="Reagent hero image"/>
*Reagent mapping input luminance to a pH-scale color gradient, tinting shadows in acid hues and highlights in base hues with smooth indicator transitions.*
<img src={reagent_animation} alt="Reagent animated output"/>
*Reagent output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Chemistry has a beautiful color language. Litmus paper turns red in acid, blue in base, and stays a muted purple-gray in neutral solutions. Universal indicator goes further — it paints the entire pH scale in a smooth rainbow from red through orange, yellow, green, and blue. Reagent applies this metaphor to video: the brightness of each pixel becomes its pH value, and the program assigns colors along a configurable acid-to-base gradient.

The name references the chemical substances — reagents — that reveal the nature of a solution through color change. In Reagent's signal chain, the input video's luminance is the unknown solution, and the program's hue mapping is the indicator paper. Dark pixels map to the acid end of the scale, bright pixels map to the base end, and a configurable neutral zone in the middle can preserve the original color or show a distinct buffer-zone highlight.

A minor implementation note: the Bypass toggle's condition is never met in the VHDL logic, so it does not function as a true bypass. Use the Mix fader at 0% to achieve a fully dry signal instead.

---

## Quick Start

1. **Bypass is broken — use Mix**: The Bypass toggle has no effect due to a dead code path. Use the Mix fader at 0% to see unprocessed input.
2. **Complementary hues for maximum range**: Setting Acid Hue and Base Hue to opposite sides of the color wheel (e.g., red/cyan, blue/yellow) creates the widest visual gradient.
3. **Buffer reveals contours**: The Buffer toggle turns Reagent into a tonal contour detector. Narrow the gap between pH Low and pH High, then enable Buffer to trace brightness boundaries.

---

## Background

### pH and Indicator Chemistry

The pH scale measures the acidity or alkalinity of a solution on a logarithmic scale from 0 (strong acid) to 14 (strong base), with 7 being neutral. **Indicators** are chemical substances that change color at specific pH values. Simple indicators like litmus produce a binary response — red or blue. Universal indicator uses a mixture of dyes to produce a continuous color gradient across the entire pH range: red, orange, yellow, green, blue, indigo, violet.

Reagent abstracts this concept. The "pH" is the pixel's luminance (mapped to a continuous range), and the "indicator dyes" are user-selected hue values. The program doesn't simulate real chemistry — it borrows the visual language of color-as-measurement to create expressive tonal-to-chromatic mappings.

### Luma-to-Color Mapping

The core technique behind Reagent is **pseudocolor mapping** — assigning false colors to a grayscale signal based on intensity. This technique is widely used in scientific imaging: thermal cameras map temperature to color (blue=cold, red=hot), medical imaging uses color lookup tables to highlight tissue density, and weather radar encodes precipitation intensity as a color gradient. Reagent applies the same principle to video, with the added artistic control of choosing the endpoint colors and transition style.

### Hue Wheels and Color Selection

Reagent uses a 6-segment hue wheel to convert the Acid Hue and Base Hue register values into actual colors. The 10-bit register range (0–1023) is divided into six equal zones: red, yellow, green, cyan, blue, and magenta. Each zone transitions linearly to the next, creating a smooth color ring. The two hue controls independently select the color for the acid (low-luma) and base (high-luma) endpoints of the gradient.

### Buffer Zones and Transition Regions

In chemistry, a **buffer** is a solution that resists changes in pH — it stays near neutral even when acid or base is added. Reagent's buffer zone serves a similar visual function: it defines a transition region around the neutral midpoint where the color mapping changes behavior. When the Buffer toggle is active, pixels in the boundary region between acid and base zones receive a distinct visual treatment — highlighting the transition rather than smoothly interpolating through it.

### Gradient vs Sharp Transitions

The Gradient toggle controls whether color assignment changes smoothly or abruptly at pH boundaries. With gradient enabled, the color interpolates linearly between acid and base hues across the transition zone, like a universal indicator. With gradient disabled, the transition is a hard threshold — pixels snap to either the acid color or the base color with no intermediate values, like a litmus test that shows only red or blue.


---

## Signal Flow

Luma Extraction → Zone Classification → Hue Assignment → ... → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Luma Extraction ────────────────────────────────────────────
│   └─ 1. Extract Y channel as "pH value"
│
├── Zone Classification ────────────────────────────────────────
│   ├─ 2. Compare Y against pH Low threshold → acid zone
│   ├─ 3. Compare Y against pH High threshold → base zone
│   └─ 4. Between thresholds → neutral zone
│
├── Hue Assignment ─────────────────────────────────────────────
│   ├─ 5. Acid zone: assign Acid Hue color (6-segment wheel)
│   ├─ 6. Base zone: assign Base Hue color (6-segment wheel)
│   ├─ 7. Neutral zone: gradient interpolation or passthrough
│   └─ 8. Indicator mode: multi-color gradient vs 2-color snap
│
├── Modifiers ──────────────────────────────────────────────────
│   ├─ 9. Buffer zone highlight (boundary region emphasis)
│   ├─ 10. Invert: swap acid and base mapping
│   └─ 11. Saturation scaling on output chroma
│
├── Compositing ────────────────────────────────────────────────
│   └─ 12. Mix interpolator: wet/dry crossfade (3x interpolator_u)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Dead — condition never met. Use Mix for dry signal.
```

The entire color mapping is computed per-pixel from the input luminance — no BRAMs or frame buffers are required. The 6-segment hue wheel converts the Acid Hue and Base Hue register values into YUV color components at full saturation. The Saturation control then scales the chroma amplitude. The neutral zone can either interpolate between the two endpoint colors (gradient mode) or pass through the original video color (non-gradient mode). The buffer zone is a secondary detection layer that highlights pixels near the acid-base boundary, making the transition region visually distinct.

---

## Parameter Reference

<img src={reagent_control_panel} alt="Videomancer front panel with Reagent loaded"/>
*Videomancer's front panel with Reagent active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sub Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the low pH threshold — the luminance level below which pixels are classified as "acid." Dark pixels with brightness below this threshold receive the Acid Hue color. Raising this control expands the acid zone, pushing the acid-base boundary higher into the midtones. At maximum, nearly the entire image is classified as acid. At minimum, only the very darkest pixels qualify.

---

#### Knob 2 — Delay
| Property | Value |
|----------|-------|
| Range | 0frm – 3frm |
| Default | 1frm |
| Suffix | frm |

Sets the high pH threshold — the luminance level above which pixels are classified as "base." Bright pixels above this threshold receive the Base Hue color. Lowering this control expands the base zone downward. The gap between pH Low and pH High defines the neutral zone width. When pH Low exceeds pH High, the zones invert — there is no neutral zone, and the acid and base regions overlap, creating a hard binary split.

---

#### Knob 3 — Main Brt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Selects the color assigned to the acid zone (low-brightness pixels). The 10-bit register maps around a 6-segment hue wheel: red → yellow → green → cyan → blue → magenta. Sweeping this control rotates through the full color spectrum. The classic litmus association is red for acid, but any hue can be chosen.

---

#### Knob 4 — Sub Brt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Selects the color assigned to the base zone (high-brightness pixels). Same 6-segment hue wheel as Acid Hue. The classic association is blue for base. When Acid Hue and Base Hue are set to complementary colors (e.g., red and cyan), the gradient between them passes through neutral desaturation. When set to adjacent colors (e.g., red and yellow), the gradient stays vibrant throughout.

---

#### Knob 5 — Win Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

At minimum, the transition between acid and base colors is abrupt — pixels snap directly from one zone to the other. At maximum, a wide band of neutral-zone pixels sits between the two colored regions, either interpolating smoothly (gradient mode) or preserving original colors. The Neutral control interacts with the Buffer toggle to determine how the boundary region is visualized. Internally, controls the width of the neutral zone between the acid and base boundaries.

---

#### Knob 6 — Win Pos
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At maximum, the acid and base hues are rendered at full saturation — vivid, pure colors. At minimum, the output is desaturated — the color mapping is still present but muted toward gray. Intermediate values produce pastel-like tints. This control affects only the U and V components; luminance is preserved. Internally, scales the chroma saturation of the output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Math A** | Add | Sub |
| **8 — Math B** | Full | Half |
| **9 — Sub Inv** | Off | On |
| **10 — Window** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control four processing modes and a non-functional bypass. Gradient selects smooth versus sharp color transitions. Indicator chooses between multi-color gradient mapping and strict two-color litmus-style snapping. Buffer highlights the acid-base boundary region. Invert swaps which end of the luminance range receives which color. Bypass is non-functional due to a dead code path in the VHDL — use the Mix fader for dry signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input video (0%) and the fully processed pH-color-mapped result (100%). Because the bypass toggle is non-functional, the Mix fader is the only way to preview the unprocessed input. At intermediate values, the color mapping appears as a tinted overlay on the source video. This also serves as a saturation-like control in practice — low mix values produce subtle tinting, high values produce full false-color.





---

## Guided Exercises

These exercises progress from simple two-tone litmus coloring to complex multi-indicator gradients with buffer highlighting and zone manipulation.

### Exercise 1: Litmus Paper

<img src={reagent_exercise1_result} alt="Litmus Paper result"/>
*Litmus Paper — simulated result across source images.*
**What You'll Create**: Learn the basic acid-base mapping: assign two colors to dark and bright regions of the image.

1. **Set acid red**: Turn Acid Hue to about 0% (red zone on the hue wheel).
2. **Set base blue**: Turn Base Hue to about 67% (blue zone on the hue wheel).
3. **Sharp threshold**: Turn Gradient off (Toggle 7 off). Turn Indicator off (Toggle 8 off).
4. **Set boundaries**: Set pH Low to about 40% and pH High to about 60%. The image splits into red (dark) and blue (bright) zones with a narrow neutral band.
5. **Sweep pH Low**: Watch the acid zone expand as you lower the threshold. Dark areas turn red, bright areas stay blue.
6. **Full saturation**: Set Saturation to 100%. Turn Mix to 100%.

**Key concepts**: Luma-to-zone classification, 6-segment hue wheel, sharp vs gradient transitions, pH Low and pH High define the zone boundaries

---

### Exercise 2: Universal Indicator

<img src={reagent_exercise2_result} alt="Universal Indicator result"/>
*Universal Indicator — simulated result across source images.*
**What You'll Create**: Create a smooth multi-color gradient that maps the full brightness range to a rainbow of indicator colors.

1. **Enable gradient**: Toggle Gradient on (Toggle 7).
2. **Enable indicator**: Toggle Indicator on (Toggle 8). The transition between acid and base now passes through intermediate hues.
3. **Widen neutral zone**: Increase Neutral to about 60%. The gradient becomes broader and smoother.
4. **Choose complementary endpoints**: Set Acid Hue to about 0% (red) and Base Hue to about 50% (cyan). The gradient passes through orange, yellow, and green.
5. **Reduce saturation**: Lower Saturation to about 60% for a more subtle, pastel-like indicator strip.
6. **Mix blend**: Set Mix to about 80% to let some source detail show through.

**Key concepts**: Gradient interpolation, indicator mode multi-hue mapping, neutral zone width controls gradient smoothness, complementary hues create the widest color range

---

### Exercise 3: Contour Map

<img src={reagent_exercise3_result} alt="Contour Map result"/>
*Contour Map — simulated result across source images.*
**What You'll Create**: Use buffer zone highlighting to reveal tonal contour lines, like elevation contours on a topographic map.

1. **Set narrow boundaries**: pH Low ~35%, pH High ~65%. Keep Neutral at about 30%.
2. **Enable gradient**: Toggle Gradient on.
3. **Enable buffer**: Toggle Buffer on (Toggle 9). Bright lines appear at the boundaries between acid and base zones.
4. **Sweep thresholds**: Move pH Low and pH High closer together. The contour lines tighten, tracing tonal boundaries in the source image.
5. **Invert**: Toggle Invert on (Toggle 10). The acid-base colors swap, but the contour lines remain at the same brightness boundaries.
6. **Subtle overlay**: Set Mix to about 60% to overlay the contour-highlighted result on the source.

**Key concepts**: Buffer zone as contour highlighting, boundary detection through zone classification, invert swaps colors but not boundary positions

---


## Tips

- **Indicator mode adds hue variety**: With Indicator on, the gradient passes through multiple intermediate hues instead of blending directly between two colors. This creates richer, more analytic-looking color maps.
- **Saturation as a subtlety control**: Lower Saturation to create pastel tints instead of vivid false colors. This makes the pH mapping more tasteful as a creative overlay.
- **Invert for creative reversal**: Toggle Invert to swap which tonal range gets which color without re-dialing the Acid and Base Hue knobs.
- **Feedback loops**: Routing the output back to the input creates recursive color mapping — each pass recolors the already-tinted signal, building up layered hue gradients.

---

## Glossary

| Term | Definition |
|------|------------|
| **Acid** | In Reagent's metaphor, the low-brightness end of the luminance range. Pixels darker than the pH Low threshold are classified as acid and receive the Acid Hue color. |
| **Base** | The high-brightness end of the luminance range. Pixels brighter than the pH High threshold receive the Base Hue color. |
| **Buffer Zone** | A transition region near the acid-base boundary where pixels receive distinct emphasis or highlighting, similar to a chemical buffer that resists pH change. |
| **Hue Wheel** | A circular arrangement of colors divided into six segments (red, yellow, green, cyan, blue, magenta). The Acid Hue and Base Hue controls each select a position on this wheel. |
| **Indicator** | A substance (or in Reagent's case, a color-mapping mode) that produces a multi-color response across a range of pH values, as opposed to a binary litmus-style response. |
| **Litmus** | A simple binary indicator that turns red in acid and blue in base. Reagent's non-gradient mode approximates this behavior. |
| **Neutral Zone** | The luminance range between pH Low and pH High where pixels are classified as neither acid nor base. |
| **Pseudocolor** | False-color mapping that assigns colors to a grayscale signal based on intensity, used in thermal imaging, medical scans, and scientific visualization. |

---
