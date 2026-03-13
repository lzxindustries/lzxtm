---
draft: true
sidebar_position: 19
slug: /instruments/videomancer/birefring
title: "Birefring"
image: /img/instruments/videomancer/birefring/birefring_hero_s1.png
description: "When light passes through a crystalline material like calcite or quartz, something unusual happens — the crystal splits the light into two rays that travel at different speeds."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import birefring_control_panel from '/img/instruments/videomancer/birefring/birefring_control_panel.png';
import birefring_source1_ballerina from '/img/instruments/videomancer/birefring/birefring_source1_ballerina.png';
import birefring_source2_house from '/img/instruments/videomancer/birefring/birefring_source2_house.png';
import birefring_source3_elephant from '/img/instruments/videomancer/birefring/birefring_source3_elephant.png';
import birefring_source4_pattern from '/img/instruments/videomancer/birefring/birefring_source4_pattern.png';
import birefring_source5_woman from '/img/instruments/videomancer/birefring/birefring_source5_woman.png';
import birefring_source6_paint from '/img/instruments/videomancer/birefring/birefring_source6_paint.png';
import birefring_hero_s1 from '/img/instruments/videomancer/birefring/birefring_hero_s1.png';
import birefring_hero_s2 from '/img/instruments/videomancer/birefring/birefring_hero_s2.png';
import birefring_hero_s3 from '/img/instruments/videomancer/birefring/birefring_hero_s3.png';
import birefring_hero_s4 from '/img/instruments/videomancer/birefring/birefring_hero_s4.png';
import birefring_hero_s5 from '/img/instruments/videomancer/birefring/birefring_hero_s5.png';
import birefring_hero_s6 from '/img/instruments/videomancer/birefring/birefring_hero_s6.png';
import birefring_ex1_s1 from '/img/instruments/videomancer/birefring/birefring_ex1_s1.png';
import birefring_ex1_s2 from '/img/instruments/videomancer/birefring/birefring_ex1_s2.png';
import birefring_ex1_s3 from '/img/instruments/videomancer/birefring/birefring_ex1_s3.png';
import birefring_ex1_s4 from '/img/instruments/videomancer/birefring/birefring_ex1_s4.png';
import birefring_ex1_s5 from '/img/instruments/videomancer/birefring/birefring_ex1_s5.png';
import birefring_ex1_s6 from '/img/instruments/videomancer/birefring/birefring_ex1_s6.png';
import birefring_ex2_s1 from '/img/instruments/videomancer/birefring/birefring_ex2_s1.png';
import birefring_ex2_s2 from '/img/instruments/videomancer/birefring/birefring_ex2_s2.png';
import birefring_ex2_s3 from '/img/instruments/videomancer/birefring/birefring_ex2_s3.png';
import birefring_ex2_s4 from '/img/instruments/videomancer/birefring/birefring_ex2_s4.png';
import birefring_ex2_s5 from '/img/instruments/videomancer/birefring/birefring_ex2_s5.png';
import birefring_ex2_s6 from '/img/instruments/videomancer/birefring/birefring_ex2_s6.png';
import birefring_ex3_s1 from '/img/instruments/videomancer/birefring/birefring_ex3_s1.png';
import birefring_ex3_s2 from '/img/instruments/videomancer/birefring/birefring_ex3_s2.png';
import birefring_ex3_s3 from '/img/instruments/videomancer/birefring/birefring_ex3_s3.png';
import birefring_ex3_s4 from '/img/instruments/videomancer/birefring/birefring_ex3_s4.png';
import birefring_ex3_s5 from '/img/instruments/videomancer/birefring/birefring_ex3_s5.png';
import birefring_ex3_s6 from '/img/instruments/videomancer/birefring/birefring_ex3_s6.png';

# Birefring

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: birefring_source1_ballerina, after: birefring_hero_s1 },
    { label: "House", before: birefring_source2_house, after: birefring_hero_s2 },
    { label: "Elephant", before: birefring_source3_elephant, after: birefring_hero_s3 },
    { label: "Pattern", before: birefring_source4_pattern, after: birefring_hero_s4 },
    { label: "Woman", before: birefring_source5_woman, after: birefring_hero_s5 },
    { label: "Paint", before: birefring_source6_paint, after: birefring_hero_s6 },
  ]}
/>
*Birefring applying Michel-Lévy interference coloring and polarizer extinction to transform luminance into iridescent mineralogical spectra.*

---

## Overview

When light passes through a crystalline material like calcite or quartz, something unusual happens — the crystal splits the light into two rays that travel at different speeds. The delay between these rays depends on the crystal's thickness and its internal stress. When the two rays recombine, they interfere, and the resulting color depends entirely on the amount of delay. This phenomenon is called **birefringence**, and it is the basis for the vivid interference colors seen in polarized-light microscopy of thin rock sections.

Birefring simulates this optical process electronically. It treats the input luminance as a proxy for crystal thickness — bright pixels represent thick material, dark pixels represent thin. Each pixel's brightness is mapped through a spectral lookup table that reproduces either the **Michel-Lévy** interference chart (the standard geological color sequence) or the **Newton's rings** spectrum (an alternative interference pattern). The result is a false-color rendering where grayscale video is transformed into crystallographic color.

A virtual polarizer adds the final optical element. Real petrographic microscopes use crossed polarizers to create extinction bands — dark regions where the crystal orientation cancels all transmitted light. The polarizer control sweeps a cos² extinction function across the image, creating angular-dependent darkening that interacts with the spectral coloring. Combined with stress modulation and dispersion, Birefring can produce effects ranging from subtle mineral tinting to full psychedelic spectral animation.

---

## Quick Start

1. **Thickness sets the starting color**: Think of Thickness as choosing which mineral you're simulating — different starting positions in the chart produce completely different color palettes.
2. **Stress is the key creative control**: Low stress creates subtle tinting; high stress creates vivid spectral banding that reveals the image's tonal structure.
3. **Polarizer adds drama**: Even a slight polarizer offset creates contrast between spectral colors at different extinction angles. Sweep slowly for the best effect.

---

## Background

### What Is Birefringence?

Birefringence is the optical property of a material having a refractive index that depends on the polarization and propagation direction of light. In a birefringent crystal, an incoming light ray splits into an **ordinary ray** and an **extraordinary ray**, each traveling at a different speed through the material. The phase difference between these two rays, when they recombine at the exit face, determines the interference color observed. The amount of retardation depends on the crystal thickness and the magnitude of birefringence — a relationship captured in the Michel-Lévy color chart used by geologists to identify minerals under a polarizing microscope.

### What Is the Michel-Lévy Chart?

The **Michel-Lévy interference color chart** is a standard reference in optical mineralogy. It maps the relationship between retardation (path difference in nanometers), crystal thickness, and birefringence to a sequence of interference colors. The first-order colors progress from black through gray, white, yellow, orange, red, and violet. Higher orders cycle through blues, greens, yellows, and pinks with decreasing saturation. Birefring encodes a 64-entry approximation of this spectral sequence in a YUV lookup table, mapping input luminance directly to the chart colors.

### What Is Polarizer Extinction?

In a polarizing microscope, rotating the analyzer produces periodic extinction — angles where the crystal appears dark because the polarized light is completely blocked. The transmitted intensity follows a **cos²** function of the angle between the polarizer and the crystal's optical axis (Malus's Law). Birefring simulates this with a 16-entry cos² lookup table indexed by the Polarizer knob, creating smooth angular darkening across the full 360° rotation.

### What Is Chromatic Dispersion?

In real birefringent materials, the amount of retardation varies slightly with wavelength — blue light is retarded more than red. This **dispersion** causes the U and V color channels to index slightly different positions in the spectral lookup table, producing subtle color fringing at transitions. The Dispersion control in Birefring offsets the UV lookup indices relative to the Y index, simulating this wavelength-dependent behavior.


---

## Signal Flow

Y Channel → U/V Channels → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Base Index            (thickness + stress × input_Y)
│   ├─ 2. Animation Offset      (frame-count-based cycling, optional)
│   ├─ 3. Invert Map            (optional index reversal)
│   ├─ 4. Spectrum LUT Lookup   (64-entry Michel-Lévy or Newton table → Y')
│   ├─ 5. Polarizer Extinction  (16-entry cos² LUT → darken Y')
│   └─ 6. Y Couple              (blend with input luma × couple factor)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Base Index + Dispersion Offset  (shift UV LUT index relative to Y)
│   ├─ 2. Spectrum LUT Lookup   (same table → U', V')
│   ├─ 3. Saturation Scaling    (× saturation pot)
│   └─ 4. Brightness Offset     (DC shift)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical interaction is between the spectral LUT and the polarizer. The LUT maps input luminance to interference colors, creating a false-color image. The polarizer then modulates the brightness of that false-color image according to a cos² angular function. Because the polarizer operates *after* the color mapping, it creates extinction bands that cut through the spectral colors — mimicking the appearance of a thin section viewed through crossed polarizers. The Dispersion control adds a secondary interaction by offsetting the UV color lookup relative to the Y lookup, so the color fringing tracks the spectral position rather than being independent.

---

## Parameter Reference

<img src={birefring_control_panel} alt="Videomancer front panel with Birefring loaded"/>
*Videomancer's front panel with Birefring active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Thickness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, the LUT starts at the beginning of the interference sequence (first-order black/gray). Higher values move deeper into the chart, cycling through the characteristic color orders. Because the Stress control adds input luminance to this base, Thickness sets the "zero brightness" color while Stress determines how far across the chart the brightest pixels reach. Internally, sets the base position in the spectral lookup table — the equivalent of crystal thickness in a real petrographic setup.

---

#### Knob 2 — Stress
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how strongly the input luminance modulates the LUT index — the equivalent of birefringence magnitude. At 0%, every pixel maps to the same spectral color regardless of brightness (flat false color). As Stress increases, bright and dark pixels map to increasingly different positions in the interference chart, producing vivid color separation that follows the tonal structure of the source image. High Stress values cause the mapping to wrap around the 64-entry table multiple times, creating banded color fringes.

---

#### Knob 3 — Polarizer
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |
| Suffix | deg |

Sweeps the virtual polarizer angle through 360°. The cos² extinction function creates smooth darkening that reaches zero at specific angles, simulating the effect of rotating a polarizer on a petrographic microscope stage. The extinction pattern modulates the brightness of the already-colored signal, so colors near the extinction angle fade to black while colors at the transmission maximum remain vivid. A full sweep produces two complete extinction/transmission cycles (cos² has period 180°).

---

#### Knob 4 — Dispersion
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Offsets the UV channel LUT indices relative to the Y channel index. At 0%, Y, U, and V all look up the same spectral position. As Dispersion increases, U and V indices shift in opposite directions, producing color fringing at tonal transitions. This simulates the wavelength-dependent retardation of real birefringent crystals, where different colors of light accumulate different phase delays. The effect is most visible at strong tonal edges in the source image.

---

#### Knob 5 — Saturation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

At 0%, the output is monochrome (interference grays only). At mid-position, the spectral colors appear at their natural saturation. Higher values exaggerate the chrominance, producing hyper-saturated interference colors. This control determines whether the output looks like a subtle geological thin-section photograph or a vivid psychedelic color field. Internally, scales the U and V values read from the spectral lookup table.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC offset to the final output luminance after all spectral processing and polarizer extinction. Use this to lift the overall brightness of the interference image, particularly useful when the polarizer is creating deep extinction bands that darken the image significantly. Also serves as a final tonal adjustment for matching the output level to downstream equipment.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Spectrum** | Michel-Levy | Newton |
| **8 — Animate** | Off | On |
| **9 — Invert Map** | Off | On |
| **10 — Y Couple** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent aspects of the simulation. The Spectrum switch selects the fundamental color mapping. Animate adds temporal variation. Invert Map reverses the luminance-to-index relationship. Y Couple blends source luminance back into the result. Bypass provides instant A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Birefring processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Birefring-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from basic spectral false-coloring to full petrographic simulation with polarizer dynamics and dispersion effects.

### Exercise 1: Mineral Color Mapping

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: birefring_source1_ballerina, after: birefring_ex1_s1 },
    { label: "House", before: birefring_source2_house, after: birefring_ex1_s2 },
    { label: "Elephant", before: birefring_source3_elephant, after: birefring_ex1_s3 },
    { label: "Pattern", before: birefring_source4_pattern, after: birefring_ex1_s4 },
    { label: "Woman", before: birefring_source5_woman, after: birefring_ex1_s5 },
    { label: "Paint", before: birefring_source6_paint, after: birefring_ex1_s6 },
  ]}
/>
*Mineral Color Mapping — simulated result across source images.*
**Source**: A live camera feed or recorded footage with smooth tonal gradients — skin tones, landscapes, or gradient test patterns work well.

**What You'll Create**: Learn how Thickness and Stress map input luminance to the Michel-Lévy interference color chart.

1. **Flat color**: Set Stress to 0%. The entire image receives a single interference color determined by Thickness. Sweep Thickness slowly and watch the color cycle through the Michel-Lévy chart — black, gray, white, yellow, orange, red, violet, blue, green, yellow, pink.
2. **Luminance mapping**: Increase Stress to ~50%. Now bright and dark areas receive different interference colors. The spectral distribution follows the image's tonal structure.
3. **Full range**: Push Stress to 100%. The full 64-color chart maps across the image's brightness range. Look for color banding where the LUT wraps around.
4. **Newton comparison**: Toggle Switch 7 to Newton mode. Compare the color sequence with Michel-Lévy.
5. **Saturation**: Sweep the Saturation knob from 0% (monochrome interference grays) to maximum (hyper-saturated spectral colors).

**Key concepts**: Birefringence maps crystal thickness to interference color, Michel-Lévy chart is a standard geological reference, stress modulation creates content-dependent false color

---

### Exercise 2: Polarizer Extinction

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: birefring_source1_ballerina, after: birefring_ex2_s1 },
    { label: "House", before: birefring_source2_house, after: birefring_ex2_s2 },
    { label: "Elephant", before: birefring_source3_elephant, after: birefring_ex2_s3 },
    { label: "Pattern", before: birefring_source4_pattern, after: birefring_ex2_s4 },
    { label: "Woman", before: birefring_source5_woman, after: birefring_ex2_s5 },
    { label: "Paint", before: birefring_source6_paint, after: birefring_ex2_s6 },
  ]}
/>
*Polarizer Extinction — simulated result across source images.*
**Source**: High-contrast footage with distinct bright and dark regions — text on white background, silhouettes, or architectural subjects.

**What You'll Create**: Explore how the polarizer creates angular extinction patterns through the spectral colors.

1. **Setup**: Set Thickness ~30%, Stress ~60%, Saturation ~80%. Establish a clear spectral color mapping.
2. **Sweep polarizer**: Slowly rotate the Polarizer knob through its full 360° range. Watch the image darken at two extinction angles (0° and 180°) and brighten at two transmission maxima (90° and 270°).
3. **Extinction depth**: At an extinction angle, notice which spectral colors survive — some colors resist extinction more than others due to their position in the cos² curve.
4. **Combined with animation**: Enable Animate (Switch 8). The cycling spectral colors now pass through the polarizer extinction, creating temporal pulses of color that fade in and out.
5. **Y Couple**: Enable Y Couple (Switch 10). Note how the original luminance structure re-emerges through the polarized spectral field.

**Key concepts**: Malus's Law governs polarizer transmission as cos² of angle, extinction creates angular-dependent darkening, animation simulates stage rotation

---

### Exercise 3: Chromatic Dispersion and Full Simulation

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: birefring_source1_ballerina, after: birefring_ex3_s1 },
    { label: "House", before: birefring_source2_house, after: birefring_ex3_s2 },
    { label: "Elephant", before: birefring_source3_elephant, after: birefring_ex3_s3 },
    { label: "Pattern", before: birefring_source4_pattern, after: birefring_ex3_s4 },
    { label: "Woman", before: birefring_source5_woman, after: birefring_ex3_s5 },
    { label: "Paint", before: birefring_source6_paint, after: birefring_ex3_s6 },
  ]}
/>
*Chromatic Dispersion and Full Simulation — simulated result across source images.*
**Source**: Footage with fine detail and strong tonal edges — foliage, fabric textures, or patterned surfaces.

**What You'll Create**: Combine all optical elements for a complete petrographic simulation with dispersion fringing.

1. **Base setup**: Thickness ~20%, Stress ~70%, Saturation ~90%, Polarizer ~45° (partial extinction).
2. **Add dispersion**: Slowly increase Dispersion from 0%. Watch color fringing appear at tonal edges — U and V shift in opposite directions, producing complementary color halos.
3. **High dispersion**: Push Dispersion to ~80%. The UV channels index significantly different spectral positions, creating dramatic rainbow fringing.
4. **Animate + dispersion**: Enable Animate. The cycling spectral colors now include dispersion-shifted U and V, creating complex temporal color patterns.
5. **Invert map**: Toggle Invert Map (Switch 9). The entire color assignment reverses — compare the two mappings.
6. **Full simulation**: Set all controls to moderate values and observe the combination: spectral false color + polarizer extinction + dispersion fringing + Y coupling + animation.

**Key concepts**: Dispersion separates color channels in the spectral lookup, inversion reverses the luminance-to-color mapping, all optical elements interact multiplicatively

---


## Tips

- **Dispersion is subtle at low values**: Start with Dispersion at 0 and increase gradually. The effect is most visible at strong tonal transitions.
- **Y Couple for recognizability**: When the spectral colors flatten the image too much, enable Y Couple to bring back the source's spatial structure.
- **Michel-Lévy vs. Newton**: Try both spectrum modes with the same settings. The choice of LUT fundamentally changes the color palette.
- **Animation for live performance**: Animate mode creates continuously evolving color fields that work well for live video synthesis without any input manipulation.
- **Feedback routing**: Route the output back to the input for recursive spectral mapping — each pass through the LUT shifts colors further into higher-order interference patterns.

---

## Glossary

| Term | Definition |
|------|------------|
| **Birefringence** | The optical property of a material having different refractive indices for different polarization directions, causing double refraction. |
| **Cos²** | The squared cosine function; in optics, describes the transmitted intensity through a polarizer as a function of angle (Malus's Law). |
| **Dispersion** | The variation of refractive index with wavelength, causing different colors to travel at different speeds through a material. |
| **Extinction** | In polarized-light microscopy, the condition where a crystal appears dark because its optical axis is aligned with the polarizer. |
| **Interference Color** | The color produced by constructive and destructive interference of light waves that have traveled different paths through a birefringent material. |
| **LUT** | Look-Up Table; a pre-computed array that maps input values to output values for fast, deterministic signal transformation. |
| **Malus's Law** | The relationship I = I₀ cos²θ describing how polarized light intensity depends on the angle between polarizer and analyzer. |
| **Michel-Lévy Chart** | A standard reference chart in optical mineralogy mapping retardation, thickness, and birefringence to interference colors. |
| **Newton's Rings** | Circular interference fringes produced by thin air gaps between two glass surfaces, displaying a sequence of spectral colors. |

---
