---
draft: true
sidebar_position: 58
slug: /instruments/videomancer/colorizer
title: "Colorizer"
image: /img/instruments/videomancer/colorizer/colorizer_hero_s1.png
description: "Colorizer is a hard-band luminance colorizer inspired by the Paik-Abe Video Synthesizer of 1969."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import colorizer_control_panel from '/img/instruments/videomancer/colorizer/colorizer_control_panel.png';
import colorizer_source1_parrot from '/img/instruments/videomancer/colorizer/colorizer_source1_parrot.png';
import colorizer_source2_runner from '/img/instruments/videomancer/colorizer/colorizer_source2_runner.png';
import colorizer_source3_elephant from '/img/instruments/videomancer/colorizer/colorizer_source3_elephant.png';
import colorizer_source4_pattern from '/img/instruments/videomancer/colorizer/colorizer_source4_pattern.png';
import colorizer_source5_woman from '/img/instruments/videomancer/colorizer/colorizer_source5_woman.png';
import colorizer_source6_berries from '/img/instruments/videomancer/colorizer/colorizer_source6_berries.png';
import colorizer_hero_s1 from '/img/instruments/videomancer/colorizer/colorizer_hero_s1.png';
import colorizer_hero_s2 from '/img/instruments/videomancer/colorizer/colorizer_hero_s2.png';
import colorizer_hero_s3 from '/img/instruments/videomancer/colorizer/colorizer_hero_s3.png';
import colorizer_hero_s4 from '/img/instruments/videomancer/colorizer/colorizer_hero_s4.png';
import colorizer_hero_s5 from '/img/instruments/videomancer/colorizer/colorizer_hero_s5.png';
import colorizer_hero_s6 from '/img/instruments/videomancer/colorizer/colorizer_hero_s6.png';
import colorizer_ex1_s1 from '/img/instruments/videomancer/colorizer/colorizer_ex1_s1.png';
import colorizer_ex1_s2 from '/img/instruments/videomancer/colorizer/colorizer_ex1_s2.png';
import colorizer_ex1_s3 from '/img/instruments/videomancer/colorizer/colorizer_ex1_s3.png';
import colorizer_ex1_s4 from '/img/instruments/videomancer/colorizer/colorizer_ex1_s4.png';
import colorizer_ex1_s5 from '/img/instruments/videomancer/colorizer/colorizer_ex1_s5.png';
import colorizer_ex1_s6 from '/img/instruments/videomancer/colorizer/colorizer_ex1_s6.png';
import colorizer_ex2_s1 from '/img/instruments/videomancer/colorizer/colorizer_ex2_s1.png';
import colorizer_ex2_s2 from '/img/instruments/videomancer/colorizer/colorizer_ex2_s2.png';
import colorizer_ex2_s3 from '/img/instruments/videomancer/colorizer/colorizer_ex2_s3.png';
import colorizer_ex2_s4 from '/img/instruments/videomancer/colorizer/colorizer_ex2_s4.png';
import colorizer_ex2_s5 from '/img/instruments/videomancer/colorizer/colorizer_ex2_s5.png';
import colorizer_ex2_s6 from '/img/instruments/videomancer/colorizer/colorizer_ex2_s6.png';
import colorizer_ex3_s1 from '/img/instruments/videomancer/colorizer/colorizer_ex3_s1.png';
import colorizer_ex3_s2 from '/img/instruments/videomancer/colorizer/colorizer_ex3_s2.png';
import colorizer_ex3_s3 from '/img/instruments/videomancer/colorizer/colorizer_ex3_s3.png';
import colorizer_ex3_s4 from '/img/instruments/videomancer/colorizer/colorizer_ex3_s4.png';
import colorizer_ex3_s5 from '/img/instruments/videomancer/colorizer/colorizer_ex3_s5.png';
import colorizer_ex3_s6 from '/img/instruments/videomancer/colorizer/colorizer_ex3_s6.png';

# Colorizer

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: colorizer_source1_parrot, after: colorizer_hero_s1 },
    { label: "Runner", before: colorizer_source2_runner, after: colorizer_hero_s2 },
    { label: "Elephant", before: colorizer_source3_elephant, after: colorizer_hero_s3 },
    { label: "Pattern", before: colorizer_source4_pattern, after: colorizer_hero_s4 },
    { label: "Woman", before: colorizer_source5_woman, after: colorizer_hero_s5 },
    { label: "Berries", before: colorizer_source6_berries, after: colorizer_hero_s6 },
  ]}
/>
*Input luminance is sliced into coloured bands by stacked comparators, painting the image in flat saturated hues.*

---

## Overview

Colorizer is a hard-band luminance colorizer inspired by the Paik-Abe Video Synthesizer of 1969. Shuya Abe and Nam June Paik's instrument included a "colorizer" section that divided the greyscale range of a monochrome camera into discrete brightness zones and assigned each zone a saturated colour. The transitions between zones are abrupt — hard-keyed — producing the characteristic flat, posterized look that would become synonymous with early video art.

This implementation slices 10-bit input luminance into 2–8 zones using integer division against the zone count. Each zone is mapped to a pre-computed colour from either a Rainbow palette cycling through red → yellow → green → cyan → blue → violet → magenta → pink, or a Complementary palette alternating warm and cool hues. A Hue Base rotation shifts the palette starting point, and an optional per-frame animation phase cycles the colour assignment.

Two luminance output modes are provided: Hard mode quantises the output brightness into flat bands matching the zone boundaries; Stepped mode preserves the original pixel luminance while applying the colour overlay, producing a false-colour effect with full tonal detail.

---

## Quick Start

1. **Two-band split**: Zone Count = 2 plus maximum saturation creates the iconic Paik-Abe pop-art look with a single hard boundary.
2. **Bias as key level**: Treat the Bias knob like a key threshold — it determines where the first colour transition falls on the brightness scale.
3. **Cycling speed**: The animation rate is fixed at 4 phase units per frame; the visible speed depends on Zone Count (fewer bands make cycling more apparent).

---

## Background

### The Paik-Abe Colorizer

In 1969, Nam June Paik and engineer Shuya Abe built what is widely considered the first video synthesizer, incorporating a section that mapped monochrome TV signals to colour. Rather than applying a smooth colour gradient, the Paik-Abe instrument used comparator thresholds to create hard transitions — a pixel was either "red" or "blue" with nothing in between. This aesthetic became a visual signature of the Fluxus movement.

### Comparator Threshold Chains

A hardware comparator outputs high when an input exceeds a reference voltage. Stacking several comparators at evenly spaced thresholds creates a "thermometer code" that identifies which brightness band a pixel belongs to. Colorizer replicates this digitally: the 0–1023 luminance range is divided into equal-width bands, and each pixel's band index selects a palette entry.

### Rainbow vs Complementary Palettes

The Rainbow palette distributes hue evenly around the colour wheel, producing a spectrum effect reminiscent of thermal imaging. The Complementary palette alternates between two opposing hue poles (warm and cool), creating a simpler, more graphic two-tone posterisation that emphasises contrast.

### Band Animation

When the Animate toggle is active, a phase counter increments by 4 per frame, slowly rotating which palette entry is assigned to each band. This causes the colours to "crawl" across the luminance range, making the coloured zones appear to flow through the image without any change to the underlying brightness.


---

## Signal Flow

```
                    ┌────────────────────┐
 data_in.y ────────▸│  Threshold offset  │
                    │  (bias)            │
                    └────────┬───────────┘
                             │ shifted luma
                             ▼
                    ┌────────────────────┐
                    │  Band index        │
                    │  = luma / band_size│
                    └────────┬───────────┘
                             │ 0..7
                             ▼
      ┌──────────────────────┴──────────────────────┐
      │  + hue_offset + anim_phase                  │
      │  mod 8 → palette LUT select                 │
      └────────────────────┬────────────────────────┘
                           │ U, V from palette
                           ▼
      ┌────────────────────────────────────┐
      │  Saturation scaling on (U,V)       │
      │  (centered at 512, signed multiply)│
      └────────────────────┬───────────────┘
                           │
    Hard mode ─────────────┤──── Stepped mode
    Y = band_size × idx    │     Y = luma × brightness
                           ▼
              ┌─────────────────────────┐
    dry ─────▸│  interpolator mix       │──▸ data_out
              └─────────────────────────┘
```

The band index calculation uses integer division of the shifted luminance by the computed band width, then clamps to the maximum band count. The hue offset, animation phase, and band index are all summed modulo 8 to select the palette entry, so rotating the Hue Base knob shifts all zone colours simultaneously. Saturation is applied as a signed multiply centred at 512 — at zero saturation the chroma outputs remain at achromatic mid-code.

---

## Parameter Reference

<img src={colorizer_control_panel} alt="Videomancer front panel with Colorizer loaded"/>
*Videomancer's front panel with Colorizer active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Zone Count
| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 5 |

**Zone Count** selects the number of luminance bands from 2 to 8 using a stepped control. Two bands produce a stark binary split; eight bands create a fine posterisation with many colour zones. Because the 1024-value luminance range is divided evenly, more bands mean narrower brightness slices and more colour transitions across the image.

---

#### Knob 2 — Hue Base
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

**Hue Base** rotates the palette starting point through 360° of hue angle. This determines which colour is assigned to the lowest luminance band, and all subsequent bands shift accordingly. A base of 0° starts at red; 120° starts at green; 240° starts at blue.

---

#### Knob 3 — Hue Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

**Hue Spread** adjusts how far apart the palette entries are distributed around the colour wheel. High spread means the 8 band colours span the full spectrum; low spread clusters them around the base hue for a more monochromatic posterisation.

---

#### Knob 4 — Bias
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**Bias** offsets all luminance thresholds, effectively shifting where the band boundaries fall on the greyscale. Increasing bias pushes the bands toward brighter pixels; decreasing it pulls them toward darker regions. This is equivalent to adjusting the reference voltage on a hardware comparator chain.

---

#### Knob 5 — Saturation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

**Saturation** scales the chroma intensity of the palette colours. At zero the output is monochrome with only the luminance quantisation visible. At maximum the full palette vividness is applied. The scaling is performed as a signed multiply centred at the chroma midpoint.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**Brightness** controls the output luminance gain in Stepped mode, scaling the original pixel brightness before it reaches the mixer. In Hard mode this register is less visible because the output luminance is already quantised to band levels.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Spacing** | Equal | Weighted |
| **8 — Hue Mode** | Fixed | Cycling |
| **9 — Edge Glow** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles shape the artistic character: Spacing selects equal band widths or a weighted distribution favouring shadows. Hue Mode either fixes the palette or cycles it over time. Edge Glow adds a subtle brightness boost at zone transitions. Invert reverses the palette order, and Bypass disables the colorizer entirely.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

**Mix** crossfades between the dry input and the colourised output. At zero the output is unaltered; at maximum it is fully colourised.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore Colorizer's range from subtle two-tone tinting to full psychedelic rainbow posterisation.

### Exercise 1: Classic Two-Tone Posterisation

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: colorizer_source1_parrot, after: colorizer_ex1_s1 },
    { label: "Runner", before: colorizer_source2_runner, after: colorizer_ex1_s2 },
    { label: "Elephant", before: colorizer_source3_elephant, after: colorizer_ex1_s3 },
    { label: "Pattern", before: colorizer_source4_pattern, after: colorizer_ex1_s4 },
    { label: "Woman", before: colorizer_source5_woman, after: colorizer_ex1_s5 },
    { label: "Berries", before: colorizer_source6_berries, after: colorizer_ex1_s6 },
  ]}
/>
*Classic Two-Tone Posterisation — simulated result across source images.*
**Source**: A talking-head interview or portrait with a smooth background gradient.

**What You'll Create**: Divide the image into two stark colour zones for a pop-art look.

1. Set Zone Count to 2.
2. Set Hue Base to 0° (red/blue split).
3. Set Hue Spread to 50 %, Saturation to 75 %.
4. Set Bias to 50 %, Brightness to 50 %.
5. Select Equal Spacing, Fixed Hue Mode.
6. Observe the image split into two flat fields of saturated colour.

**Key concepts**: Comparator threshold, binary posterisation, hard keying.

---

### Exercise 2: Crawling Rainbow

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: colorizer_source1_parrot, after: colorizer_ex2_s1 },
    { label: "Runner", before: colorizer_source2_runner, after: colorizer_ex2_s2 },
    { label: "Elephant", before: colorizer_source3_elephant, after: colorizer_ex2_s3 },
    { label: "Pattern", before: colorizer_source4_pattern, after: colorizer_ex2_s4 },
    { label: "Woman", before: colorizer_source5_woman, after: colorizer_ex2_s5 },
    { label: "Berries", before: colorizer_source6_berries, after: colorizer_ex2_s6 },
  ]}
/>
*Crawling Rainbow — simulated result across source images.*
**Source**: A slowly moving subject with a wide tonal range (landscape, dancer).

**What You'll Create**: Create a full-spectrum rainbow posterisation that slowly cycles through the image.

1. Set Zone Count to 8 for maximum bands.
2. Set Hue Base to 0°, Hue Spread to 100 %.
3. Set Saturation to 90 %, Brightness to 50 %.
4. Set Bias to 50 %.
5. Enable Cycling Hue Mode — watch the colours rotate through the zones.
6. Adjust Bias to shift where the colour boundaries fall relative to the subject's brightness.

**Key concepts**: Full-range posterisation, palette cycling, animation phase.

---

### Exercise 3: Neon Contour with Edge Glow

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: colorizer_source1_parrot, after: colorizer_ex3_s1 },
    { label: "Runner", before: colorizer_source2_runner, after: colorizer_ex3_s2 },
    { label: "Elephant", before: colorizer_source3_elephant, after: colorizer_ex3_s3 },
    { label: "Pattern", before: colorizer_source4_pattern, after: colorizer_ex3_s4 },
    { label: "Woman", before: colorizer_source5_woman, after: colorizer_ex3_s5 },
    { label: "Berries", before: colorizer_source6_berries, after: colorizer_ex3_s6 },
  ]}
/>
*Neon Contour with Edge Glow — simulated result across source images.*
**Source**: An architectural scene with strong geometric lines and moderate contrast.

**What You'll Create**: Combine posterised colour bands with glowing edges to emphasise structural contours.

1. Set Zone Count to 5, Hue Base to 180° (blue-green starting point).
2. Set Hue Spread to 60 %, Saturation to 80 %.
3. Set Bias to 45 %, Brightness to 55 %.
4. Enable Edge Glow — bright lines appear at the transitions between colour zones.
5. Toggle between Equal and Weighted spacing to see how the glow lines redistribute.

**Key concepts**: Zone boundary detection, edge emphasis, band distribution.

---


## Tips

- **Mix for blending**: At 30–50 % mix the colour overlay tints the image without completely flattening it.
- **Invert for negative palette**: Reversing the palette order can dramatically change the mood — bright regions get dark-associated hues and vice versa.
- **Hard vs Stepped luma**: Hard mode gives the classic flat-colour look; Stepped mode preserves tonal detail while adding false colour.

---
