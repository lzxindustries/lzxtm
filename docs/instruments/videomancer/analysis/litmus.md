---
draft: true
sidebar_position: 167
slug: /instruments/videomancer/litmus
title: "Litmus"
image: /img/instruments/videomancer/litmus/litmus_hero.png
description: "In every chemistry laboratory there is a drawer full of narrow paper strips impregnated with chemical indicators — compounds that change color in the presence of specific substances."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import litmus_hero from '/img/instruments/videomancer/litmus/litmus_hero.png';
import litmus_control_panel from '/img/instruments/videomancer/litmus/litmus_control_panel.png';
import litmus_exercise1_result from '/img/instruments/videomancer/litmus/litmus_exercise1_result.png';
import litmus_exercise2_result from '/img/instruments/videomancer/litmus/litmus_exercise2_result.png';
import litmus_exercise3_result from '/img/instruments/videomancer/litmus/litmus_exercise3_result.png';
import litmus_source1_grayscale_ramp_h_1920x1080 from '/img/instruments/videomancer/litmus/litmus_source1_grayscale_ramp_h_1920x1080.png';
import litmus_source2_grayscale_ramp_v_1920x1080 from '/img/instruments/videomancer/litmus/litmus_source2_grayscale_ramp_v_1920x1080.png';
import litmus_source3_step_wedge_21level_512 from '/img/instruments/videomancer/litmus/litmus_source3_step_wedge_21level_512.png';

# Litmus

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Grayscale Ramp H", before: litmus_source1_grayscale_ramp_h_1920x1080, after: litmus_hero },
    { label: "Grayscale Ramp V", before: litmus_source2_grayscale_ramp_v_1920x1080, after: litmus_hero },
    { label: "Step Wedge 21level", before: litmus_source3_step_wedge_21level_512, after: litmus_hero },
  ]}
/>
*Litmus applying pH reagent false-color mapping with paper texture to transform video into chemical indicator strip imagery.*

---

## Overview

In every chemistry laboratory there is a drawer full of narrow paper strips impregnated with chemical indicators — compounds that change color in the presence of specific substances. Litmus paper turns red in acid and blue in base. Universal indicator paper fans through a rainbow from deep red at pH 1 to violet at pH 14. Biuret reagent turns pale blue to deep purple in the presence of protein. Iodine solution turns brown-black when it encounters starch. These color shifts are the language of wet chemistry — a visual readout of invisible molecular conditions.

Litmus translates this visual language to video. The program quantizes the input luminance (or chrominance) into discrete color zones and maps each zone to a color from one of four reagent-inspired palettes. The result resembles a chemical test strip viewed under bright fluorescent light: flat fields of saturated color with sharp zone boundaries, printed on slightly noisy paper. The number of zones, the saturation, the paper texture, and the zone border bleed are all continuously variable, creating a range from subtle false-color overlays to full posterized indicator imagery.

At minimum settings, Litmus adds a gentle tint that follows the tonal structure of the source. At maximum, it reduces the image to a handful of flat, vivid color bands — a chemical heat map of the video signal's luminance topology.

---

## Background

### Chemical Indicator Color Science

Chemical indicators are weak acids or bases whose conjugate forms have different absorption spectra — they absorb different wavelengths of light depending on the pH of their environment. Litmus, the most familiar indicator, contains a mixture of dyes extracted from lichens. In acidic solution (pH < 4.5), litmus absorbs blue light and appears red. In basic solution (pH > 8.3), it absorbs red light and appears blue. Universal indicator is a blend of multiple indicators chosen so that each pH unit produces a distinct color step across the visible spectrum. Litmus's pH palette approximates this rainbow progression: red → orange → yellow → green → blue → indigo → violet.

### Zone Quantization

Litmus divides the input signal into discrete zones by extracting the most significant bits of the source value. With 2 zones, the signal is split at the midpoint into two flat color regions. With 4 zones, the top 2 bits define four bands. With 8 zones, three bits create eight regions, and with 16 zones, four bits produce sixteen narrow color bands. The zone boundaries are hard — each zone maps to one palette entry — creating the flat, stepped appearance characteristic of chemical test strips. The Offset control shifts the zone boundaries up or down the luminance range, letting you "rotate" the color map relative to the source content.

### False Color in Scientific Imaging

False-color mapping is a foundational technique in scientific visualization. Thermal cameras map infrared intensity to a rainbow scale. Medical imaging maps tissue density to color. Astronomical images map spectral bands to visible hues. In every case, the purpose is the same: to make invisible structure visible by mapping a scalar measurement to a color palette designed for human perception. Litmus applies this principle to video, treating luminance (or chrominance) as the scalar input and the reagent palettes as the perceptual color map.

### Paper Texture and Zone Bleed

Real chemical test strips are porous — the reagent-soaked paper has a fibrous texture, and the color boundary between adjacent zones bleeds slightly because the liquid wicks along the paper fibers. Litmus simulates both effects. Paper texture adds LFSR noise to the luminance channel at an amplitude determined by the Paper control (four discrete levels matching four paper weights). Zone bleed adds extra noise near zone boundaries — where the zone fraction is very small or very large — creating a soft, diffused edge between adjacent color bands.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Source Selection ───────────────────────────────────────────
│   └─ Luma (Y) or Chroma (U) via Source toggle
│
├── Zone Quantization ──────────────────────────────────────────
│   │
│   ├─ 1. Apply Offset              (shift + clamp)
│   ├─ 2. Count Zones               (2/4/8/16 from Zones register)
│   └─ 3. Extract Zone Index + Frac (bit-shift quantization)
│
├── Palette Lookup ─────────────────────────────────────────────
│   └─ 4 reagents × 8 colors       (pH / Redox / Biuret / Iodine)
│
├── Post-Processing ────────────────────────────────────────────
│   │
│   ├─ Paper Texture                (LFSR noise × paper weight)
│   ├─ Zone Border Bleed            (noise near zone boundaries)
│   ├─ Saturation Scale             (4 levels: ¼ / ½ / ¾ / full)
│   └─ Brightness Offset            (+/- 512)
│
├── Output ─────────────────────────────────────────────────────
│   │
│   ├─ Invert                       (1023 − Y)
│   └─ Interpolator                 (4 clk wet/dry mix)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline (8+4 clk matched)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline splits into two phases. The first phase (Stages 1–2) quantizes the source signal into zones and looks up palette colors — this is a pure mapping operation with no dependency on the original chrominance. The second phase (Stages 3–4) applies analog imperfections: paper texture, zone bleed, saturation scaling, and brightness offset. The Source toggle at the input determines whether luminance or chrominance drives the zone assignment: in Luma mode, the Y channel is quantized; in Chroma mode, the U channel is used directly, creating a color-space-aware mapping where input hue determines the output palette color.

---

## Parameter Reference

<img src={litmus_control_panel} alt="Videomancer front panel with Litmus loaded"/>
*Videomancer's front panel with Litmus active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Zones
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 9 |

Zones controls how many color bands the input signal is divided into. At the lowest setting, only two zones are produced — a simple binary split between two palette colors. At higher settings, 4, 8, or 16 zones create increasingly fine color steps. With 16 zones and a full-range input, the output closely tracks the input topology because each narrow luminance band gets its own palette color. With 2 zones, the image reduces to a stark two-color posterization.

---

#### Knob 2 — Saturate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Saturate controls the color saturation of the palette output. The VHDL implements four discrete levels based on the register value: at maximum, palette colors are at full saturation. At lower settings, chroma differences from the neutral midpoint (512) are progressively halved — ¾ saturation, ½ saturation, and ¼ saturation. At minimum, the palette colors are nearly desaturated, reducing the effect to a luminance-only zone map with faint color tints.

---

#### Knob 3 — Bleed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Bleed controls the amount of color noise at zone boundaries. Real chemical test strips show diffused edges where one color zone meets the next — the reagent liquid wicks along the paper fibers, blurring the boundary. Litmus simulates this by adding LFSR-based noise near zone boundaries (where the zone fraction is close to 0 or close to its maximum). Higher Bleed values increase the noise amplitude, creating a wider, noisier transition between adjacent color bands.

---

#### Knob 4 — Texture
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Texture controls the paper fiber noise applied uniformly across the image. Four discrete levels correspond to paper weight: Smooth (no noise), Light (subtle grain), Medium (moderate fiber texture), and Heavy (pronounced paper noise). The noise is added to the luminance channel only, modulating brightness without affecting the palette colors — just as real paper texture affects the perceived lightness of the printed color without changing the dye itself.

---

#### Knob 5 — Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Offset shifts the zone boundaries up or down the luminance range. At the center position (512), the mapping is neutral. Turning the control counter-clockwise shifts the color bands toward the dark end of the scale; clockwise shifts them toward the bright end. This lets you "rotate" the color palette relative to the source content — positioning specific palette colors on specific parts of the image without changing the source material.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Bright applies a global brightness offset to the palette output. At the center position (512), no offset is applied. Turning counter-clockwise darkens the output; clockwise brightens it. The offset is added after texture and bleed, so it shifts the entire processed image uniformly. This is useful for matching the processed output's overall brightness to the original source when mixing.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Reagent** | pH | Redox |
| **8 — Paper** | Smooth | Rough |
| **9 — Source** | Luma | Chroma |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The toggle switches control non-standard packed bit fields. Reagent (Switch 7) is a 2-bit selector occupying bits 0–1 of register 6, selecting one of four palettes. Paper (Switch 8) is a 2-bit selector on bits 2–3, selecting one of four texture levels. Source (Switch 9), Invert (Switch 10), and Bypass (Switch 11) are single-bit flags on bits 4, 5, and 6 respectively.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original input and the processed palette output. At 0%, the output is entirely the original signal. At 100%, the output is entirely the false-color palette mapping. Intermediate values create a semi-transparent overlay of palette colors on the source — useful for maintaining recognizable imagery while adding chemical color accents.

---

## Guided Exercises

These exercises introduce the four reagent palettes and progressively engage the texture and bleed controls to build complete chemical indicator imagery.

### Exercise 1: pH Strip Colorization

<BeforeAfterSlider
  sources={[
    { label: "Grayscale Ramp H", before: litmus_source1_grayscale_ramp_h_1920x1080, after: litmus_exercise1_result },
    { label: "Grayscale Ramp V", before: litmus_source2_grayscale_ramp_v_1920x1080, after: litmus_exercise1_result },
    { label: "Step Wedge 21level", before: litmus_source3_step_wedge_21level_512, after: litmus_exercise1_result },
  ]}
/>
*pH Strip Colorization — simulated result across source images.*
**Source**: A high-contrast scene with a full tonal range — architectural interiors, landscapes with sky and ground.

**Objective**: Learn zone quantization and the pH palette mapping.

1. **Start simple**: Set Zones to the middle position (~8 zones). The image should break into distinct color bands following the pH palette rainbow.
2. **Reduce zones**: Pull Zones to minimum (2 zones). The image becomes a two-color split — red and violet, the extremes of the pH scale.
3. **Increase zones**: Push Zones to maximum (16 zones). The color bands become narrow and detailed, closely tracking the source luminance.
4. **Shift with Offset**: Sweep Offset to rotate the palette relative to the source. Watch different colors land on different parts of the image.
5. **Desaturate**: Pull Saturate to minimum. The vivid pH colors fade to pale tints, creating a subtle analytical overlay.

**Key concepts**: Zone count determines color resolution, offset rotates the palette, saturation controls color intensity, pH palette follows the universal indicator rainbow

---

### Exercise 2: Paper Texture and Zone Bleed

<BeforeAfterSlider
  sources={[
    { label: "Grayscale Ramp H", before: litmus_source1_grayscale_ramp_h_1920x1080, after: litmus_exercise2_result },
    { label: "Grayscale Ramp V", before: litmus_source2_grayscale_ramp_v_1920x1080, after: litmus_exercise2_result },
    { label: "Step Wedge 21level", before: litmus_source3_step_wedge_21level_512, after: litmus_exercise2_result },
  ]}
/>
*Paper Texture and Zone Bleed — simulated result across source images.*
**Source**: Footage with smooth gradients — soft lighting, fog, or water surfaces.

**Objective**: Explore how paper texture and zone bleed add analog character to the digital palette mapping.

1. **Clean palette**: Set Zones ~50%, Saturate ~75%, Reagent pH, Bleed 0%, Texture 0%.
2. **Add texture**: Cycle the Paper toggle through its positions. Watch paper fiber noise appear in the luminance channel — subtle at Light, pronounced at Heavy.
3. **Add bleed**: Increase Bleed from 0%. The hard zone boundaries soften as noise diffuses the edges between adjacent color bands.
4. **Combined**: With both Texture and high Bleed, the image looks like a chemical strip test viewed under fluorescent light — flat color fields with noisy boundaries on textured paper.
5. **Try Iodine**: Switch Reagent to Iodine. The warm amber-brown palette with paper texture creates a convincing reagent paper appearance.

**Key concepts**: Paper texture adds uniform luminance noise, bleed adds noise specifically at zone boundaries, the combination creates analog paper character, different palettes interact differently with texture

---

### Exercise 3: Chroma Source and Reagent Comparison

<BeforeAfterSlider
  sources={[
    { label: "Grayscale Ramp H", before: litmus_source1_grayscale_ramp_h_1920x1080, after: litmus_exercise3_result },
    { label: "Grayscale Ramp V", before: litmus_source2_grayscale_ramp_v_1920x1080, after: litmus_exercise3_result },
    { label: "Step Wedge 21level", before: litmus_source3_step_wedge_21level_512, after: litmus_exercise3_result },
  ]}
/>
*Chroma Source and Reagent Comparison — simulated result across source images.*
**Source**: Colorful footage — flowers, neon signs, painted surfaces, or color test patterns.

**Objective**: Compare Luma and Chroma source modes across all four reagent palettes.

1. **Luma baseline**: Set Source to Luma, Reagent to pH, Zones ~50%. The color palette maps to brightness.
2. **Switch to Chroma**: Toggle Source to Chroma. Now the U channel drives the zone mapping — blue-shifted areas and yellow-shifted areas get different palette colors.
3. **Cycle reagents**: Step through pH, Redox, Biuret, and Iodine. Each palette tells a different visual story with the same source — warm browns (Iodine), cool purples (Biuret), rainbow (pH), or progressive oxidation (Redox).
4. **Invert**: Toggle Invert to rearrange the luminance distribution across the palette bands.
5. **Mix to overlay**: Pull Mix to ~50% to blend the palette with the original source. The chemical colors tint the original image.

**Key concepts**: Source mode selects the driving signal for zone quantization, Chroma mode produces color-space-aware mapping, each reagent palette has a different character and use case, Mix enables palette overlay

---


## Tips

- **Start with 8 zones**: Eight zones is the sweet spot for most source material — enough color bands to read the tonal structure, few enough for clear visual separation.
- **Offset is your palette rotator**: Offset doesn't change the colors — it shifts which luminance range each color lands on. Use it to position a specific palette color on the area of interest.
- **Chroma mode for colorful sources**: When the source has strong colors, switching to Chroma mode maps the palette along the blue-yellow axis, creating color-space-aware false coloring.
- **Paper + Bleed for analog feel**: Smooth paper with no bleed produces a clinical, digital look. Adding paper texture and zone bleed transforms the output into something that looks like it came out of a chemistry lab.
- **Iodine is the warmest palette**: The Iodine reagent produces warm amber-brown tones that work well as a sepia-like treatment, especially with texture enabled.
- **Mix for tinted overlay**: Pulling Mix to 50% blends palette colors with the original source — subtle false-color accents without losing the source image.
- **Brightness for level matching**: Use Bright to shift the processed output up or down in brightness to match the original when mixing.

---

## Glossary

| Term | Definition |
|------|------------|
| **Biuret Reagent** | A chemical test for proteins; the reagent turns from pale blue to deep purple in proportion to protein concentration. |
| **BT.601** | The ITU-R standard defining the YUV color space used by standard-definition video and throughout the Videomancer pipeline. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **False Color** | A visualization technique that maps a scalar measurement to an arbitrary color palette designed to reveal structure. |
| **Iodine Test** | A chemical test for starch; iodine solution turns brown-black in the presence of starch molecules. |
| **LFSR** | Linear Feedback Shift Register; a deterministic pseudo-random number generator used for texture noise. |
| **Litmus** | A pH indicator derived from lichens that turns red in acid and blue in base — the most familiar chemical indicator. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Redox** | Reduction-oxidation potential; a measure of a substance's tendency to gain or lose electrons, visualized by indicator color changes. |
| **Universal Indicator** | A blend of pH indicators chosen to produce a distinct color at each pH unit, creating a continuous rainbow spectrum. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
| **Zone Quantization** | Dividing a continuous signal range into a fixed number of discrete bands, each mapped to a single output value. |

---
