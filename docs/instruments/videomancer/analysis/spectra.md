---
draft: true
sidebar_position: 263
slug: /instruments/videomancer/spectra
title: "Spectra"
image: /img/instruments/videomancer/spectra/spectra_hero.png
description: "Scientific instruments often visualize invisible phenomena by mapping measured values to color — thermal cameras paint heat as a spectrum from cool blue to hot white, weather radar maps rainfall intensity to a green-yellow-red gradient, and medical imaging uses false color to highlight tissue density."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import spectra_hero from '/img/instruments/videomancer/spectra/spectra_hero.png';
import spectra_control_panel from '/img/instruments/videomancer/spectra/spectra_control_panel.png';
import spectra_exercise1_result from '/img/instruments/videomancer/spectra/spectra_exercise1_result.png';
import spectra_exercise2_result from '/img/instruments/videomancer/spectra/spectra_exercise2_result.png';
import spectra_exercise3_result from '/img/instruments/videomancer/spectra/spectra_exercise3_result.png';
import spectra_source1_grayscale_ramp_h_1920x1080 from '/img/instruments/videomancer/spectra/spectra_source1_grayscale_ramp_h_1920x1080.png';
import spectra_source2_grayscale_ramp_v_1920x1080 from '/img/instruments/videomancer/spectra/spectra_source2_grayscale_ramp_v_1920x1080.png';
import spectra_source3_step_wedge_21level_512 from '/img/instruments/videomancer/spectra/spectra_source3_step_wedge_21level_512.png';

# Spectra

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Grayscale Ramp H", before: spectra_source1_grayscale_ramp_h_1920x1080, after: spectra_hero },
    { label: "Grayscale Ramp V", before: spectra_source2_grayscale_ramp_v_1920x1080, after: spectra_hero },
    { label: "Step Wedge 21level", before: spectra_source3_step_wedge_21level_512, after: spectra_hero },
  ]}
/>
*Spectra decomposing video luminance into discrete spectral bands and false-coloring each zone with configurable rainbow, heat, cool, or earth palettes.*

---

## Overview

Scientific instruments often visualize invisible phenomena by mapping measured values to color — thermal cameras paint heat as a spectrum from cool blue to hot white, weather radar maps rainfall intensity to a green-yellow-red gradient, and medical imaging uses false color to highlight tissue density. Spectra brings this visualization technique to live video, decomposing the brightness of each pixel into discrete bands and assigning each band a color from a selectable palette.

The program quantizes the luminance (or chrominance) signal into 2, 4, 8, or 16 discrete zones, then maps each zone to a color from one of four built-in palettes: Rainbow, Heat, Cool, or Earth. A hue offset rotates the palette assignment, a spread control expands contrast before banding, and optional contour lines mark the transitions between zones. The name comes from the Latin *spectrum* — the band of colors produced when white light is dispersed by a prism.

At low band counts, Spectra reduces an image to bold, poster-like color zones — two bands creates a stark binary split, four bands a topographic map. At sixteen bands with a heat palette, the output closely resembles a thermal imaging camera. The contour mode turns the band boundaries into black outlines, transforming the video into a topographic elevation map.

---

## Background

### False Color Imaging

False color is any visualization technique where colors are assigned to data values that have no inherent color of their own. Thermal cameras are the most familiar example: they measure infrared radiation (invisible to the human eye) and display it using a color gradient — typically blue for cold, red for hot, white for hottest. Spectra applies the same principle to video luminance: dark areas of the image get one color, bright areas get another, and the gradient between them is divided into discrete bands. The result turns brightness information into a color map that makes tonal structure immediately visible.

### Band Quantization

The core operation in Spectra is **quantization** — reducing a continuous range of values to a small number of discrete levels. The input luminance (10 bits, 1024 possible values) is quantized to 2, 4, 8, or 16 bands by discarding lower-order bits. With 2 bands, only the MSB matters: the image splits into "dark" and "light." With 16 bands, the top 4 bits are preserved, creating fine tonal gradations. This is the same mathematical operation as posterization, but instead of reducing bit depth for visual effect, Spectra uses the quantized level as an index into a color palette.

### Palette Design

Each of Spectra's four palettes is an 8-entry lookup table of YUV color triplets. The band index (plus a configurable hue offset) addresses this table, wrapping around for band counts greater than 8. Rainbow cycles through spectral hues — red, orange, yellow, green, cyan, blue, magenta. Heat maps the intensity gradient of a blackbody — black, dark red, red, orange, yellow, white. Cool runs from deep blue through cyan to white, emulating cryogenic or underwater visualization. Earth uses natural tones — browns, greens, tans, and creams — for a topographic map aesthetic.

### Contour Lines

In cartography, contour lines connect points of equal elevation, making the shape of terrain visible on a flat map. Spectra's contour mode applies the same principle to video: whenever a pixel's band index differs from its neighbor's, the output is forced to black. The result is a network of dark lines tracing the boundaries between brightness zones — a real-time topographic map of the video signal's luminance surface.

### Spread and Contrast Enhancement

Before quantization, the spread control pushes luminance values away from the midpoint, expanding the deviation from center. This is effectively a contrast enhancement that makes the full range of bands visible even in low-contrast source material. Without spread, a low-contrast input might fall entirely within one or two bands; with spread at maximum, the input is stretched to use all available bands.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Source Selection ────────────────────────────────────────────
│   └─ Select Y, U, or V channel as analysis input
│
├── Processing Chain ────────────────────────────────────────────
│   │
│   ├─ 1. Optional Invert     (1023 − value)
│   ├─ 2. Spread Enhancement   (push values from mid, contrast boost)
│   ├─ 3. Band Quantization    (top 1/2/3/4 bits → 2/4/8/16 bands)
│   ├─ 4. Hue Offset           (rotate palette index)
│   ├─ 5. Palette Lookup       (band index → YUV color from LUT)
│   ├─ 6. Contour Detection    (band ≠ prev pixel → black)
│   ├─ 7. Saturation Scaling   (4 levels from saturate control)
│   └─ 8. Brightness Offset    (Y ± offset centered at 512)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
├── Bypass ─────────────────────────────────────────────────────
│   └─ Select original or processed signal
│
└── Mix ────────────────────────────────────────────────────────
    └─ Interpolate original ↔ processed (linear_potentiometer_12)
```

The source selection at the top of the chain determines which component of the input signal drives the analysis. In Luma mode, the Y channel is used — the most common choice. In Chroma mode, the chrominance magnitude is used instead, analyzing color saturation rather than brightness. The spread enhancement occurs *before* quantization, so it determines how much of the input range maps to the available bands. The contour detector compares each pixel's band index to its left neighbor, inserting black lines at every transition — this is a horizontal-only edge detector driven by the quantized signal, not the raw input.

---

## Parameter Reference

<img src={spectra_control_panel} alt="Videomancer front panel with Spectra loaded"/>
*Videomancer's front panel with Spectra active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Bands
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 9 |

Selects the number of spectral bands: 2, 4, 8, or 16. With 2 bands, the image splits into a simple binary — every pixel falls into either the "low" or "high" zone. With 4 bands, the image resembles a simple topographic map. With 8 bands, fine tonal gradations become visible. With 16 bands, the output approaches a continuous gradient — especially useful with the Heat palette for thermal camera emulation. The band count is selected by register thresholds, creating four discrete steps.

---

#### Knob 2 — Saturate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls the chroma saturation of the false-color output at four discrete levels. At full saturation, the palette colors are vivid and fully chromatic. Reducing saturation progressively desaturates the output, ultimately producing a grayscale banded image that resembles a simple posterization. The four levels are derived from the top two bits of the register, creating coarse but predictable saturation steps.

---

#### Knob 3 — Hue Offs
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |
| Suffix | deg |

Rotates the palette color assignment by adding an offset to the band index before the lookup table. At 0°, band 0 maps to the first palette entry. Rotating the offset shifts which color corresponds to which brightness zone — dark areas might start as blue (Rainbow) and rotate through green, yellow, red as the offset increases. The offset wraps around the 8-entry palette, so a full rotation cycles through all available colors. This allows fine-tuning the color-to-brightness mapping without changing the palette itself.

---

#### Knob 4 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the spread (contrast) enhancement applied before band quantization. At 0%, no enhancement — the input maps directly to bands based on its raw luminance. At 100%, values are pushed away from the midpoint, stretching the input to fill the full 0–1023 range. This is essential for low-contrast sources that might otherwise fall within only one or two bands. High spread values ensure all bands are populated, producing a full-spectrum false-color output.

---

#### Knob 5 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies a brightness offset to the false-colored output. The offset is centered at the register midpoint — 50% means no change. Below center, the entire output darkens; above center, it brightens. This is a global Y adjustment applied *after* palette lookup, so it shifts the overall brightness of the false-color image without affecting which band each pixel falls into.

---

#### Knob 6 — Gamma
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for gamma correction in the register mapping, but not actively used in the current VHDL pipeline. Adjusting this control has no visible effect on the output. Future firmware revisions may implement gamma curve reshaping before quantization.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Rainbow | Heat |
| **8 — Contour** | Off | On |
| **9 — Source** | Luma | Chroma |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control palette selection (4 palettes via 2 bits), contour overlay, analysis source selection, luminance inversion, and bypass. The Palette and Source toggles use non-standard multi-bit encoding — Palette uses two bit positions to select among four options, and Source uses two bits for four channel options (though the TOML exposes only Luma and Chroma as labels).

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the false-color processed output and the original input signal via three parallel interpolator units. At 100%, the output is fully false-colored. At 0%, the original input passes through unaltered. Intermediate positions blend the false-color overlay with the source video, creating a semi-transparent analysis overlay — useful for seeing the false-color bands superimposed on the original image content.

---

## Guided Exercises

These exercises progress from simple two-band analysis to complex multi-palette visualization, building familiarity with Spectra's band decomposition and false-color mapping.

### Exercise 1: Thermal Camera

<BeforeAfterSlider
  sources={[
    { label: "Grayscale Ramp H", before: spectra_source1_grayscale_ramp_h_1920x1080, after: spectra_exercise1_result },
    { label: "Grayscale Ramp V", before: spectra_source2_grayscale_ramp_v_1920x1080, after: spectra_exercise1_result },
    { label: "Step Wedge 21level", before: spectra_source3_step_wedge_21level_512, after: spectra_exercise1_result },
  ]}
/>
*Thermal Camera — simulated result across source images.*
**Source**: A scene with a wide range of brightness — a person against a bright window, or outdoor footage with sky, foliage, and shadows.

**Objective**: Create a convincing thermal camera visualization that maps brightness to the Heat palette.

1. **Heat palette**: Set Palette to Heat. The default band count may already show color zones.
2. **Band count**: Set Bands to 16 for the finest thermal-like gradation.
3. **Full saturation**: Ensure Saturate is at maximum for vivid thermal colors.
4. **Spread**: Adjust Spread until all bands are populated — you should see the full gradient from black through red to yellow to white.
5. **Brightness**: Adjust Bright to center the thermal range on the most interesting part of the scene.
6. **Contour lines**: Enable Contour to add isothermal lines at band boundaries, resembling a real thermal measurement overlay.

**Key concepts**: Band count determines resolution of the thermal map, spread ensures full palette utilization, Heat palette mimics blackbody radiation gradient

---

### Exercise 2: Topographic Map

<BeforeAfterSlider
  sources={[
    { label: "Grayscale Ramp H", before: spectra_source1_grayscale_ramp_h_1920x1080, after: spectra_exercise2_result },
    { label: "Grayscale Ramp V", before: spectra_source2_grayscale_ramp_v_1920x1080, after: spectra_exercise2_result },
    { label: "Step Wedge 21level", before: spectra_source3_step_wedge_21level_512, after: spectra_exercise2_result },
  ]}
/>
*Topographic Map — simulated result across source images.*
**Source**: A slowly moving camera across a textured surface — landscape, architecture, or a face.

**Objective**: Create a contour-line topographic map visualization of the brightness surface.

1. **Earth palette**: Set Palette to Earth for a natural cartographic look.
2. **Few bands**: Set Bands to 4 for widely-spaced contour zones.
3. **Contour on**: Enable Contour. Black lines appear at every band boundary, dividing the image into topographic zones.
4. **Spread**: Set Spread to about 60% so the bands correspond to visible brightness differences.
5. **Saturate**: Try reducing Saturate. At low saturation, the zones become pastel — more like a real topographic map.
6. **Increase bands**: Switch Bands to 8. The contour lines become denser, creating a finer elevation map.
7. **Hue rotation**: Sweep Hue Offs slowly. Watch the color assignments rotate through the palette — dark zones change from brown to green to tan.

**Key concepts**: Contour mode detects band transitions and renders them as black lines, fewer bands create bolder zones, hue offset rotates which color maps to which brightness level

---

### Exercise 3: Chroma Analysis with Overlay

<BeforeAfterSlider
  sources={[
    { label: "Grayscale Ramp H", before: spectra_source1_grayscale_ramp_h_1920x1080, after: spectra_exercise3_result },
    { label: "Grayscale Ramp V", before: spectra_source2_grayscale_ramp_v_1920x1080, after: spectra_exercise3_result },
    { label: "Step Wedge 21level", before: spectra_source3_step_wedge_21level_512, after: spectra_exercise3_result },
  ]}
/>
*Chroma Analysis with Overlay — simulated result across source images.*
**Source**: Footage with strong, varied colors — a color chart, fruit market, or painted mural.

**Objective**: Analyze the chrominance structure of the source using false color, blended as a semi-transparent overlay on the original video.

1. **Rainbow palette**: Set Palette to Rainbow for maximum color differentiation.
2. **Source to Chroma**: Switch Source to Chroma. The analysis now responds to color saturation rather than brightness.
3. **8 bands**: Set Bands to 8 for a useful number of chrominance zones.
4. **Full spread**: Set Spread to 100% to stretch the chroma range across all bands.
5. **Overlay blend**: Reduce Mix to about 50%. The false-color analysis appears superimposed on the original video.
6. **Invert**: Toggle Invert On. The mapping reverses — saturated areas now receive the colors that previously mapped to desaturated areas.
7. **Hue offset sweep**: Slowly rotate Hue Offs while watching the overlay. Different palette rotations emphasize different parts of the chrominance spectrum.

**Key concepts**: Source toggle selects chroma analysis instead of luma, Mix fader creates analysis overlay, invert reverses the color mapping direction

---


## Tips

- **Start with Heat + 16 bands**: This combination most closely resembles a thermal camera and is the most immediately recognizable false-color visualization.
- **Spread is essential for low-contrast sources**: Without spread enhancement, a flat or low-contrast input may fall entirely within one or two bands, producing a nearly uniform color output.
- **Contour lines need space**: Contour mode is most legible with 2–4 bands, where the lines are widely spaced. At 16 bands, contour lines become a dense texture.
- **Hue offset is palette rotation**: It does not add new colors — it shifts which existing palette entry maps to which band. Use it to align the most visually important palette colors with the brightness zones you want to highlight.
- **Chroma mode reveals color structure**: Switching Source to Chroma analyzes saturation rather than brightness, making color patterns visible that are invisible in luminance-only analysis.
- **Mix for overlay analysis**: Reducing the Mix fader below 100% superimposes the false-color analysis on the original video, creating a transparent overlay useful for alignment and study.
- **Gamma is reserved**: The Gamma knob is defined in the register map but does not affect the current pipeline. Adjusting it has no visible effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **Band** | A discrete brightness zone produced by quantizing the luminance signal; each band maps to one palette color. |
| **BT.601** | ITU-R Recommendation 601; the color matrix standard used for YUV conversions in standard-definition video. |
| **Contour** | A line marking the boundary between two adjacent bands, rendered as black pixels at band transitions. |
| **False Color** | A visualization technique that maps non-visual data values to arbitrary colors for analysis and display. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware executing the video processing pipeline. |
| **Luminance** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **LUT** | Lookup Table; a fixed array of pre-computed values (here, palette YUV triplets) addressed by an index. |
| **Palette** | An ordered set of colors used to visualize quantized data; Spectra offers Rainbow, Heat, Cool, and Earth. |
| **Pipeline** | Sequential processing stages where each stage operates on every pixel every clock cycle. |
| **Quantization** | Reducing a continuous range to discrete levels; here, mapping 1024 brightness values to 2–16 bands. |
| **Spread** | Contrast enhancement applied before quantization, pushing values away from the midpoint to populate more bands. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
