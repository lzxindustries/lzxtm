---
draft: true
sidebar_position: 150
slug: /instruments/videomancer/isotherm
title: "Isotherm"
image: /img/instruments/videomancer/isotherm/isotherm_hero_s1.png
description: "Every surface radiates energy."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import isotherm_control_panel from '/img/instruments/videomancer/isotherm/isotherm_control_panel.png';
import isotherm_source1_sunset from '/img/instruments/videomancer/isotherm/isotherm_source1_sunset.png';
import isotherm_source2_fruit from '/img/instruments/videomancer/isotherm/isotherm_source2_fruit.png';
import isotherm_source3_clouds from '/img/instruments/videomancer/isotherm/isotherm_source3_clouds.png';
import isotherm_source4_pattern from '/img/instruments/videomancer/isotherm/isotherm_source4_pattern.png';
import isotherm_source5_woman from '/img/instruments/videomancer/isotherm/isotherm_source5_woman.png';
import isotherm_source6_wood from '/img/instruments/videomancer/isotherm/isotherm_source6_wood.png';
import isotherm_hero_s1 from '/img/instruments/videomancer/isotherm/isotherm_hero_s1.png';
import isotherm_hero_s2 from '/img/instruments/videomancer/isotherm/isotherm_hero_s2.png';
import isotherm_hero_s3 from '/img/instruments/videomancer/isotherm/isotherm_hero_s3.png';
import isotherm_hero_s4 from '/img/instruments/videomancer/isotherm/isotherm_hero_s4.png';
import isotherm_hero_s5 from '/img/instruments/videomancer/isotherm/isotherm_hero_s5.png';
import isotherm_hero_s6 from '/img/instruments/videomancer/isotherm/isotherm_hero_s6.png';
import isotherm_ex1_s1 from '/img/instruments/videomancer/isotherm/isotherm_ex1_s1.png';
import isotherm_ex1_s2 from '/img/instruments/videomancer/isotherm/isotherm_ex1_s2.png';
import isotherm_ex1_s3 from '/img/instruments/videomancer/isotherm/isotherm_ex1_s3.png';
import isotherm_ex1_s4 from '/img/instruments/videomancer/isotherm/isotherm_ex1_s4.png';
import isotherm_ex1_s5 from '/img/instruments/videomancer/isotherm/isotherm_ex1_s5.png';
import isotherm_ex1_s6 from '/img/instruments/videomancer/isotherm/isotherm_ex1_s6.png';
import isotherm_ex2_s1 from '/img/instruments/videomancer/isotherm/isotherm_ex2_s1.png';
import isotherm_ex2_s2 from '/img/instruments/videomancer/isotherm/isotherm_ex2_s2.png';
import isotherm_ex2_s3 from '/img/instruments/videomancer/isotherm/isotherm_ex2_s3.png';
import isotherm_ex2_s4 from '/img/instruments/videomancer/isotherm/isotherm_ex2_s4.png';
import isotherm_ex2_s5 from '/img/instruments/videomancer/isotherm/isotherm_ex2_s5.png';
import isotherm_ex2_s6 from '/img/instruments/videomancer/isotherm/isotherm_ex2_s6.png';
import isotherm_ex3_s1 from '/img/instruments/videomancer/isotherm/isotherm_ex3_s1.png';
import isotherm_ex3_s2 from '/img/instruments/videomancer/isotherm/isotherm_ex3_s2.png';
import isotherm_ex3_s3 from '/img/instruments/videomancer/isotherm/isotherm_ex3_s3.png';
import isotherm_ex3_s4 from '/img/instruments/videomancer/isotherm/isotherm_ex3_s4.png';
import isotherm_ex3_s5 from '/img/instruments/videomancer/isotherm/isotherm_ex3_s5.png';
import isotherm_ex3_s6 from '/img/instruments/videomancer/isotherm/isotherm_ex3_s6.png';

# Isotherm

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: isotherm_source1_sunset, after: isotherm_hero_s1 },
    { label: "Fruit", before: isotherm_source2_fruit, after: isotherm_hero_s2 },
    { label: "Clouds", before: isotherm_source3_clouds, after: isotherm_hero_s3 },
    { label: "Pattern", before: isotherm_source4_pattern, after: isotherm_hero_s4 },
    { label: "Woman", before: isotherm_source5_woman, after: isotherm_hero_s5 },
    { label: "Wood", before: isotherm_source6_wood, after: isotherm_hero_s6 },
  ]}
/>
*Isotherm mapping video luminance into false-color thermal palettes with contour lines and HUD overlay.*

---

## Overview

Every surface radiates energy. Thermal cameras translate that invisible radiation into visible colour maps — turning temperature differences into vivid gradients that the eye can instantly parse. Isotherm brings this scientific imaging language into the creative video domain. It treats the luminance channel of the input signal as a proxy for temperature and maps it through one of four selectable colour palettes to produce a false-colour rendering of the original scene.

The name comes from the meteorological term *isotherm* — a contour line connecting points of equal temperature on a weather map. In this program, isotherm contour lines are drawn at configurable intervals across the palette-mapped image, adding topographic-like banding that delineates regions of equal brightness. An optional auto-ranging envelope tracker dynamically stretches the input luma to fill the full palette range, maximising contrast regardless of the source signal's native dynamic range.

A heads-up display overlay adds crosshair and corner bracket reticles, completing the scientific instrumentation aesthetic. At full mix with the Ironbow palette and auto-range enabled, Isotherm transforms any video feed into a convincing thermal camera simulation. At partial mix or with the monochromatic WhiteHot and BlackHot palettes, it becomes a sophisticated contrast enhancement and visualisation tool.

---

## Quick Start

1. **Ironbow for realism**: The Ironbow palette closely matches FLIR thermal camera colour schemes. Combined with auto-range and HUD, it produces the most convincing thermal simulation.
2. **Auto-range is your friend**: Leave it on unless you need precise manual control. It ensures the full palette range is always used, regardless of input levels.
3. **Contours reveal structure**: Even at minimum width, a few contour lines add significant perceptual depth to the false-colour rendering. Try step 5 or 6 for subtle topographic detail.

---

## Background

### False Colour in Scientific Imaging

False colour is a visualisation technique in which data values are mapped to colours that bear no relation to the subject's actual appearance. Thermal cameras are the most familiar example — they assign blues and purples to cool regions and reds, oranges, and whites to warm regions. But the technique extends far beyond thermography: astronomers use false colour to visualise wavelengths outside the visible spectrum, geologists use it to distinguish rock types in satellite imagery, and medical imaging uses it to highlight blood flow and tissue density. The common thread is replacing a single variable (temperature, wavelength, density) with a colour gradient that makes spatial patterns immediately visible.

### Piecewise-Linear Palette Interpolation

A naive lookup table with 1024 entries for a 10-bit luma value would consume significant FPGA resources. Isotherm instead stores each palette as 16 key-point colours evenly spaced across the luma range. Between key-points, the output colour is linearly interpolated using the fractional position within each segment. This piecewise-linear approach produces smooth colour gradients with only 64 colour constants (16 key-points × 4 palettes × 3 channels), entirely in registers — no BRAM required.

### Auto-Range Envelope Tracking

Many video signals use only a fraction of the available dynamic range. A dimly lit scene might occupy only the bottom quarter of the luma scale, meaning most of the palette's colour range goes unused. Isotherm's auto-range mode tracks the minimum and maximum luma values across each frame using an IIR (infinite impulse response) envelope follower with fast attack and slow release. The tracked range is then used to normalise incoming luma before palette lookup, effectively stretching any input signal to span the full palette.

### Contour Lines and Topographic Mapping

Contour lines on a topographic map connect points of equal elevation. In Isotherm, they connect pixels of equal normalised brightness. The contour detection works by computing the modular remainder of the normalised luma value with respect to a configurable interval. When the remainder falls within a threshold distance of zero, the pixel is classified as on-contour and rendered in bright white, cutting across the palette colours like elevation lines carved into a painted relief map.

### Heads-Up Display Overlays

HUD overlays originated in military aviation, where critical flight data was projected onto the pilot's forward view so they never had to look away from their target. Isotherm borrows this visual language with a centre crosshair and corner reticle brackets. Beyond aesthetics, these elements provide fixed spatial reference points that help the viewer gauge feature positions within the false-colour field — particularly useful when auto-range is stretching and shifting the colour mapping frame to frame.


---

## Signal Flow

Y Channel → U/V Channels → 4-Clock Interpolator → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register + Spatial Smoothing (2-tap average, 4 modes)
│   ├─ 2. Auto-Range IIR Envelope Tracking (fast attack / slow release)
│   │      └─ OR Manual Gain + Offset (when Auto Range = Off)
│   ├─ 3. Normalised Luma → Palette Lookup
│   │      └─ 16-keypoint piecewise-linear interpolation
│   │      └─ 4 palettes: Ironbow / Rainbow / WhiteHot / BlackHot
│   ├─ 4. Contour Detection (modular remainder vs interval threshold)
│   ├─ 5. HUD Overlay (crosshair + corner brackets)
│   └─ 6. Output Composite (palette + contour + HUD)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   └─ Replaced entirely by palette-generated Cb / Cr
│
├── 4-Clock Interpolator (wet/dry mix per channel) ─────────────
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay pipeline (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical architectural decision is that Isotherm discards the input chrominance entirely. The U and V channels of the output come exclusively from the palette lookup — the original colour information is not blended or preserved (except through the wet/dry mix fader which interpolates against the delayed dry signal). This means the program is fundamentally a luma-to-colour mapper: all output colour is derived from input brightness.

The auto-range normalisation stage sits between input smoothing and palette lookup, which means the palette always receives a signal stretched to the full 0–1023 range (when auto-range is active). The contour detector operates on the normalised luma, so contour line positions shift dynamically as the auto-range envelope adapts — contour lines track the scene content rather than fixed absolute brightness levels.

---

## Parameter Reference

<img src={isotherm_control_panel} alt="Videomancer front panel with Isotherm loaded"/>
*Videomancer's front panel with Isotherm active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sensitivity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At low values, the envelope adapts slowly — it takes many frames for the tracked minimum and maximum to settle after a scene change. At high values, the envelope responds almost instantly to new extremes. Faster sensitivity produces more responsive contrast stretching but can cause visible pumping on rapidly changing material. Slower sensitivity produces stable mapping but may clip highlights or crush shadows during transitions. This control has no effect when Auto Range is switched off. Internally, controls the speed of the auto-range IIR envelope follower.

---

#### Knob 2 — Contour Int
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 4 |

Sets the spacing between isotherm contour lines. The control is quantised to eight steps, producing intervals from tight (16 luma levels apart) to wide (192 levels apart). Tight intervals create dense topographic banding that reveals fine tonal gradations. Wide intervals produce sparse, bold contour strokes that highlight only major brightness boundaries. At the widest setting with a narrow contour width, only one or two contour lines may be visible across the entire image.

---

#### Knob 3 — Smoothing
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 2 |

Selects the spatial smoothing kernel applied to the input luma before any further processing. Four modes are available: no smoothing (raw pixel values), light 2-tap average, weighted 2-tap (3:1 ratio favouring the current pixel), and heavy 2-tap average. Smoothing reduces noise and pixel-level jitter in the palette mapping, producing cleaner colour transitions at the cost of spatial resolution. On noisy analogue sources, moderate smoothing prevents the contour lines from chattering.

---

#### Knob 4 — Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Manual brightness gain applied to the smoothed luma. The gain is a multiplicative scaling factor: at centre position (512), the signal passes at unity. Below centre the signal is attenuated; above centre it is amplified. Gain interacts with Offset to provide manual contrast control when Auto Range is turned off. With Auto Range on, this control is bypassed — the auto-range normalisation overrides manual gain and offset.

---

#### Knob 5 — Offset
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Manual brightness offset added after gain. At centre position (512), no offset is applied. Below centre, the signal is shifted darker; above centre, it is shifted brighter. Combined with Gain, this provides conventional brightness and contrast adjustment of the palette input signal. Like Gain, this control is bypassed when Auto Range is active.

---

#### Knob 6 — Contour Wid
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the thickness of contour lines. Internally, this controls the threshold distance from the modular remainder zero-crossing — wider thresholds produce thicker white contour strokes. At minimum, contour lines are a single pixel thin. At maximum, the contour regions expand to fill a significant portion of each interval, producing wide bands of white that begin to dominate the palette colours.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette A** | Lo | Hi |
| **8 — Palette B** | Lo | Hi |
| **9 — Auto Range** | On | Off |
| **10 — HUD** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches divide into three functional groups. Palette A and Palette B form a 2-bit binary selector for the four colour palettes (00 = Ironbow, 01 = Rainbow, 10 = WhiteHot, 11 = BlackHot). Auto Range independently enables or disables the IIR envelope tracker. HUD enables or disables the crosshair and bracket overlay. Bypass routes the input directly to the output. The palette toggles interact — changing either one immediately changes the output colour scheme across the entire image.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Isotherm-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from basic palette exploration to advanced contour mapping and diagnostic workflows. Each demonstrates a different facet of Isotherm's scientific visualisation toolkit.

### Exercise 1: Thermal Camera Simulation

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: isotherm_source1_sunset, after: isotherm_ex1_s1 },
    { label: "Fruit", before: isotherm_source2_fruit, after: isotherm_ex1_s2 },
    { label: "Clouds", before: isotherm_source3_clouds, after: isotherm_ex1_s3 },
    { label: "Pattern", before: isotherm_source4_pattern, after: isotherm_ex1_s4 },
    { label: "Woman", before: isotherm_source5_woman, after: isotherm_ex1_s5 },
    { label: "Wood", before: isotherm_source6_wood, after: isotherm_ex1_s6 },
  ]}
/>
*Thermal Camera Simulation — simulated result across source images.*
**Source**: A live camera feed of a person or scene with varied brightness — skin, clothing, background surfaces.

**What You'll Create**: Create a convincing thermal camera simulation using auto-range and the Ironbow palette.

1. **Start with defaults**: Ensure Auto Range is On, HUD is Off, Bypass is Off, and Mix is at 100%.
2. **Ironbow palette**: Set Palette A and B both to Lo (Ironbow). The image immediately maps to the classic thermal gradient — dark blues for cool (dark) areas, reds and oranges for warm (bright) areas, and white for the hottest (brightest) regions.
3. **Adjust sensitivity**: Sweep the Sensitivity knob. Notice how faster settings make the colour mapping react more quickly to scene changes, while slower settings produce a more stable but less responsive render.
4. **Add contours**: Set Contour Int to step 4 (~64 levels). White isotherm lines appear, banding the image like a topographic map. Increase Contour Width to make the lines bolder.
5. **Enable HUD**: Switch HUD On. The crosshair and corner brackets appear in bright white, completing the thermal camera aesthetic.

**Key concepts**: Auto-range stretches any input to fill the full palette, Ironbow is the classic thermal camera colour scheme, contour lines add topographic banding

---

### Exercise 2: Contour Mapping

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: isotherm_source1_sunset, after: isotherm_ex2_s1 },
    { label: "Fruit", before: isotherm_source2_fruit, after: isotherm_ex2_s2 },
    { label: "Clouds", before: isotherm_source3_clouds, after: isotherm_ex2_s3 },
    { label: "Pattern", before: isotherm_source4_pattern, after: isotherm_ex2_s4 },
    { label: "Woman", before: isotherm_source5_woman, after: isotherm_ex2_s5 },
    { label: "Wood", before: isotherm_source6_wood, after: isotherm_ex2_s6 },
  ]}
/>
*Contour Mapping — simulated result across source images.*
**Source**: Footage with smooth gradients — skies, light falloff on walls, or a gradient test pattern.

**What You'll Create**: Explore contour line behaviour across different intervals and palettes.

1. **Dense contours**: Set Contour Int to step 1 (interval = 16 levels). Dense white lines carve the palette into narrow bands.
2. **Sparse contours**: Increase Contour Int to step 8 (interval = 192). Only a few bold contour strokes remain.
3. **Thick vs thin**: Sweep Contour Width from minimum to maximum. At minimum, contour lines are hair-thin. At maximum, they expand into wide bands.
4. **Rainbow palette**: Switch to Rainbow (Palette A = Hi, B = Lo). The contour lines now cut across a full spectral gradient.
5. **WhiteHot**: Switch to WhiteHot (A = Lo, B = Hi). Contour lines are now visible as bright strokes on a greyscale gradient — a pure luminance contour map.

**Key concepts**: Contour interval controls line spacing, contour width controls line thickness, contour lines are modular remainder detectors

---

### Exercise 3: False-Colour Overlay

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: isotherm_source1_sunset, after: isotherm_ex3_s1 },
    { label: "Fruit", before: isotherm_source2_fruit, after: isotherm_ex3_s2 },
    { label: "Clouds", before: isotherm_source3_clouds, after: isotherm_ex3_s3 },
    { label: "Pattern", before: isotherm_source4_pattern, after: isotherm_ex3_s4 },
    { label: "Woman", before: isotherm_source5_woman, after: isotherm_ex3_s5 },
    { label: "Wood", before: isotherm_source6_wood, after: isotherm_ex3_s6 },
  ]}
/>
*False-Colour Overlay — simulated result across source images.*
**Source**: Any recognisable footage — faces, landscapes, architecture.

**What You'll Create**: Blend the false-colour palette with the original image for a colour-wash overlay effect.

1. **Half mix**: Set Mix to ~50%. The original image structure shows through the false colour.
2. **Ironbow tint**: With the Ironbow palette, the image gains a warm-to-cool tint that follows brightness — shadow areas turn blue, highlights turn amber.
3. **Rainbow wash**: Switch to Rainbow. The spectrum overlays the scene, creating a psychedelic brightness map.
4. **Fine-tune gain**: Turn Auto Range Off and manually adjust Gain and Offset to control where the palette gradient sits relative to the source tones.
5. **Add subtle contours**: Set Contour Int to step 5 and Contour Width to minimum. Barely-visible contour lines add topographic texture to the blended result.

**Key concepts**: Partial mix blends false colour with the original, manual gain and offset provide precise control of palette placement, subtle contours add texture without overwhelming the source

---


## Tips

- **Partial mix for colour wash**: At 40–60% mix, the false colour overlays the original image like a luminance-dependent colour filter — useful for artistic grading.
- **WhiteHot for analysis**: The WhiteHot palette is a simple greyscale ramp — use it to verify auto-range behaviour or check input signal levels without the distraction of colour.
- **Smoothing tames noise**: If contour lines are jittery on noisy sources, increase Smoothing to step 3 or 4 before reaching for sensitivity.
- **Gain and Offset are manual-mode only**: These controls are bypassed when Auto Range is On. Switch Auto Range Off to access precise manual palette positioning.
- **Feedback loops**: Feeding the output back into the input with a Rainbow palette creates recursive false-colour layering — each brightness band gets re-mapped through the spectrum.

---

## Glossary

| Term | Definition |
|------|------------|
| **Auto-Range** | Dynamic normalisation that stretches the input signal's native range to span the full palette, maximising contrast automatically. |
| **BT.601** | ITU-R Recommendation BT.601; the standard colour space for standard-definition video, used here for YUV↔RGB conversion. |
| **Contour Line** | A line drawn at pixels where the normalised luma falls at a regular modular interval, analogous to elevation lines on a topographic map. |
| **False Colour** | A visualisation technique that maps a single-variable data range (here, luminance) to an arbitrary colour gradient. |
| **HUD** | Heads-Up Display; an overlay of graphical reference elements (crosshair, brackets) superimposed on the processed image. |
| **IIR** | Infinite Impulse Response; a filter whose output depends on both current input and previous output, used here for envelope tracking. |
| **Ironbow** | A false-colour palette progressing from black through deep blue, red, orange, yellow, to white, mimicking standard thermal camera rendering. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Normalisation** | Scaling a signal so that its minimum maps to 0 and its maximum maps to full scale. |
| **Piecewise-Linear** | An interpolation method that connects key-points with straight line segments, producing smooth gradients with minimal data. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
