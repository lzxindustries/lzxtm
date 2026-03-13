---
draft: true
sidebar_position: 57
slug: /instruments/videomancer/colorbars
title: "Colorbars"
image: /img/instruments/videomancer/colorbars/colorbars_hero.png
description: "Every video engineer's first instinct when commissioning a new system is to call up color bars."
---

import colorbars_hero from '/img/instruments/videomancer/colorbars/colorbars_hero.png';
import colorbars_control_panel from '/img/instruments/videomancer/colorbars/colorbars_control_panel.png';

# Colorbars

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<img src={colorbars_hero} alt="Colorbars hero image"/>
*Colorbars generating a full-amplitude SMPTE 7-bar test pattern — seven clean vertical stripes spanning the full YUV gamut from white through blue.*
---

## Overview

Every video engineer's first instinct when commissioning a new system is to call up color bars. Colorbars generates the classic seven-bar SMPTE test pattern directly in FPGA hardware, producing pixel-accurate vertical stripes at either 75% or 100% amplitude. Because the pattern is generated from constant YUV lookup tables with no frame memory or feedback, the output is perfectly static and repeatable — ideal for calibrating monitors, verifying signal chains, and confirming that downstream equipment decodes color correctly.

The program auto-measures the active line width from incoming sync signals, then uses a DDA (Digital Differential Analyzer) algorithm to divide each line into seven equal bars without requiring a hardware divider. This makes the pattern resolution-independent: it produces correct bars at any video standard the Videomancer core supports. The Y Level and C Level knobs allow independent attenuation of luminance and chrominance, which is useful for testing decoder response to partial-amplitude signals or for creative desaturation effects.

The name *Colorbars* needs no etymology — it is exactly what it says. The seven-bar pattern (White, Yellow, Cyan, Green, Magenta, Red, Blue) descends from the SMPTE Engineering Guideline EG 1, first standardized in 1978 and still the universal language of video test signals.

---

## Quick Start

1. **Load and go**: Colorbars produces a valid test pattern at default settings — seven 75% bars, full brightness, full saturation, normal order.
2. **Switch to 100%**: Toggle Level (Switch 7) to 100% for full-amplitude bars that exercise the complete YUV gamut.
3. **Verify with a waveform monitor**: Route the output to a vectorscope or waveform monitor to confirm chrominance levels and phase.

---

## Background

### The SMPTE Color Bar Standard

The seven-bar color bar pattern was formalized by SMPTE (Society of Motion Picture and Television Engineers) as Engineering Guideline EG 1. The bar order — White, Yellow, Cyan, Green, Magenta, Red, Blue — is not arbitrary: it follows a descending luminance sequence. White has the highest Y value, blue the lowest. This ordering makes the pattern immediately diagnostic on a waveform monitor: the luminance staircase should descend smoothly from left to right, and any deviation indicates a color-space or gain error.

### 75% vs 100% Amplitude

The 75% bar pattern is the most commonly used test signal in broadcast environments. At 75% amplitude, the peak chrominance levels remain within the "legal" range of analog video, avoiding clipping in legacy equipment. The 100% pattern pushes chrominance to full excursion — useful for testing headroom and confirming that the signal chain handles full-gamut YUV without distortion. Many consumer monitors and capture cards have never seen a proper 100% bar signal; switching between levels is a quick diagnostic for downstream clipping.

### DDA: Division Without a Divider

The iCE40 HX4K has no hardware divider, and implementing division in LUTs is expensive. Colorbars uses a Digital Differential Analyzer — essentially the Bresenham line algorithm applied in one dimension — to distribute seven bars evenly across any measured line width. An accumulator adds 7 per pixel and wraps at the measured width, advancing the bar index at each wrap. This produces bars of exactly equal width (±1 pixel rounding) regardless of resolution.


---

## Signal Flow

```
 registers_in(0) ──► Y Level gain
 registers_in(1) ──► C Level gain
 registers_in(6)(0) ► Level 75/100%
 registers_in(6)(1) ► Reverse order

 ┌────────────────────────────────────────────────────────────┐
 │  Timing Generator (1 clk)                                  │
 │     data_in sync ──► video_timing_generator_fielded        │
 │     outputs: avid, avid_start, hsync_start                 │
 │                                                            │
 │  Pixel Counter (1 clk)                                     │
 │     timing ──► h_count, v_count                            │
 │                                                            │
 │  Resolution Measure (continuous)                           │
 │     counts active pixels per line ──► s_measured_h         │
 │                                                            │
 │  DDA Bar Index (1 clk)                                     │
 │     accum += 7 per pixel, wrap at s_measured_h             │
 │     ──► s_bar_index (0..6)                                 │
 │                                                            │
 │  YUV Lookup (1 clk)                                        │
 │     bar_index × level_select ──► LUT ──► bar_y, bar_u,    │
 │     bar_v                                                  │
 │     (reverse: index = 6 − bar_index)                       │
 │                                                            │
 │  Gain Scaling (1 clk)                                      │
 │     out_y = bar_y × Y_Level / 1024                         │
 │     out_u = 512 ± |bar_u − 512| × C_Level / 1024          │
 │     out_v = 512 ± |bar_v − 512| × C_Level / 1024          │
 │                                                            │
 │  Output Register (1 clk)                                   │
 │     ──► s_out_y, s_out_u, s_out_v                          │
 └────────────────────────────────────────────────────────────┘

 Sync pipeline: 6 × shift register (avid, hsync_n, vsync_n, field_n)

 ┌────────────────────────────────────────────────────────────┐
 │  Interpolator (4 clk per channel)                          │
 │     lerp(input_delayed, colorbars_output, Mix)             │
 │     ──► data_out Y/U/V                                     │
 └────────────────────────────────────────────────────────────┘

 Bypass mux: toggle_switch_11 selects raw input
```

The pipeline is purely combinational through constant LUTs — no BRAM, no feedback, no frame memory. The DDA bar index tracks horizontal position with one clock of latency, and the YUV lookup and gain scaling each add one clock. The 6-element sync pipeline matches the total processing delay so that video timing signals arrive at the output simultaneously with the processed pixel data. The chroma gain stage works in unsigned arithmetic: it computes the absolute deviation of each chroma channel from the midpoint (512), scales it by the C Level pot, then adds or subtracts the result from 512 depending on the original sign. This preserves the chroma phase while allowing smooth desaturation to neutral gray.

---

## Parameter Reference

<img src={colorbars_control_panel} alt="Videomancer front panel with Colorbars loaded"/>
*Videomancer's front panel with Colorbars active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Level
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the overall luminance level of the color bars. At 100%, bar Y values are output at their nominal amplitude (75% or 100% depending on the Level toggle). At 0%, all bars collapse to black. Intermediate positions scale linearly. This is useful for testing waveform monitor calibration — dialing the gain to exactly 50% should produce a half-amplitude staircase.

---

#### Knob 2 — C Level
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the chrominance saturation of the color bars. At 100%, chroma channels carry their full deviation from neutral (512). At 0%, all chroma collapses to 512 and the output becomes a pure luminance grayscale staircase — white through black with no color. This is the classic "luma-only bars" test signal, useful for isolating luminance path issues from chrominance path issues.

---

#### Knob 3 — —
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 50 |

Unused. This control has no effect on the output.

---

#### Knob 4 — —
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 50 |

Unused. This control has no effect on the output.

---

#### Knob 5 — —
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 50 |

Unused. This control has no effect on the output.

---

#### Knob 6 — —
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 50 |

Unused. This control has no effect on the output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Level** | 75% | 100% |
| **8 — Order** | Normal | Reverse |
| **9 — —** | Off | On |
| **10 — —** | Off | On |
| **11 — Bypass** | Off | On |

Only two of the five toggles are active. Level (Switch 7) selects between the 75% and 100% bar amplitude standards. Order (Switch 8) reverses the bar sequence from the standard White→Blue to Blue→White. Bypass (Switch 11) routes the input signal directly to the output, bypassing all processing. Switches 9 and 10 are unused.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the delayed input video and the generated color bars. At 0%, the output is pure input video. At 100%, the output is pure color bars. Intermediate positions blend the two, which can be useful for superimposing bars over a live image to check alignment, or for creative overlay effects.





---

## Guided Exercises

These exercises demonstrate the primary use cases for Colorbars: signal verification, chrominance testing, and gain calibration.

### Exercise 1: Standard 75% Test Pattern

1. Load Colorbars with default settings. The output should show seven vertical bars at 75% amplitude.
2. Observe the bar order from left to right: White, Yellow, Cyan, Green, Magenta, Red, Blue.
3. If a waveform monitor is available, confirm the luminance staircase descends smoothly from left to right.
4. Toggle Level (Switch 7) to 100%. The bars become visibly brighter and more saturated — the luminance staircase extends to full scale.
5. Return to 75%.

**Key concepts**: SMPTE bar order follows descending luminance, 75% bars stay within broadcast-legal chrominance limits, 100% bars exercise full YUV gamut

---

### Exercise 2: Grayscale Staircase

1. Set C Level (Knob 2) to 0%. All chroma collapses to neutral — the output becomes seven shades of gray.
2. On a waveform monitor, only the Y channel shows activity; U and V are flat at 512.
3. Gradually increase C Level. Watch the chroma return — at 50%, the color is half-saturated; at 100%, it is fully saturated.
4. Set Y Level (Knob 1) to 50%. The entire staircase drops to half amplitude while maintaining the same relative bar-to-bar ratios.

**Key concepts**: C Level at zero produces a luminance-only test signal, Y Level scales the entire staircase uniformly, separating Y from C isolates signal path issues

---

### Exercise 3: Reversed Full-Amplitude Bars

1. Toggle Level (Switch 7) to 100% for full-amplitude bars.
2. Toggle Order (Switch 8) to Reverse. The bars now read Blue→Red→Magenta→Green→Cyan→Yellow→White from left to right.
3. On a waveform monitor, the luminance staircase now ascends from left to right — Blue (lowest Y) to White (highest Y).
4. Set Mix to ~50% to overlay the bars on a live video input. The color bar pattern is visible superimposed on the source image.

**Key concepts**: Reversed order produces ascending luminance staircase, 100% amplitude tests full-gamut headroom, Mix fader enables overlay composition

---


## Tips

- **Use for signal chain verification**: Route Colorbars through your entire video chain (mixer, effects, capture) and verify that all seven bars arrive at the destination with correct hue and amplitude.
- **Grayscale mode for luminance testing**: Set C Level to 0% for a pure grayscale staircase — this isolates luminance-path issues from chrominance-path issues.
- **100% bars reveal clipping**: If your downstream equipment clips or distorts the 100% pattern but handles 75% cleanly, the chroma path lacks headroom for full-gamut signals.
- **Reversed bars for ascending ramp**: Toggle Reverse for an ascending luminance staircase, which some waveform monitors display more intuitively.
- **Mix for overlay alignment**: Set Mix to ~30% to ghost the bar pattern over a live image — useful for checking that the generated pattern aligns with the active picture area.
- **Zero-resource pattern**: Colorbars uses no BRAM and minimal LUTs, making it one of the lightest programs available. It can serve as a baseline for FPGA resource comparisons.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation BT.601, the color encoding standard used for standard-definition digital video, defining the YCbCr (YUV) color matrix. |
| **Chrominance** | The color-difference components (U and V) of a YUV signal, representing hue and saturation independently of brightness. |
| **DDA** | Digital Differential Analyzer; an incremental algorithm that distributes N equal divisions across a measured length without hardware division. |
| **Luminance** | The brightness component (Y) of a YUV signal, representing the grayscale intensity of each pixel. |
| **SMPTE** | Society of Motion Picture and Television Engineers; the standards body that defined the original color bar test pattern in Engineering Guideline EG 1. |
| **Vectorscope** | A test instrument that displays the chrominance components of a video signal on a circular plot, used to verify hue and saturation accuracy. |
| **Waveform monitor** | A test instrument that displays the voltage levels of a video signal over time, used to verify luminance amplitude and timing. |
| **YUV** | Color encoding separating luminance (Y) from two chrominance channels (U, V), centered at 512 in 10-bit representation. |

---
