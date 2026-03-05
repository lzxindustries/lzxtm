---
draft: true
sidebar_position: 219
slug: /instruments/videomancer/patina
title: "Patina"
image: /img/instruments/videomancer/patina/patina_hero_s1.png
description: "Copper starts bright and warm."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import patina_control_panel from '/img/instruments/videomancer/patina/patina_control_panel.png';
import patina_source1_boat from '/img/instruments/videomancer/patina/patina_source1_boat.png';
import patina_source2_sunset from '/img/instruments/videomancer/patina/patina_source2_sunset.png';
import patina_source3_clouds from '/img/instruments/videomancer/patina/patina_source3_clouds.png';
import patina_source4_pattern from '/img/instruments/videomancer/patina/patina_source4_pattern.png';
import patina_source5_man from '/img/instruments/videomancer/patina/patina_source5_man.png';
import patina_source6_berries from '/img/instruments/videomancer/patina/patina_source6_berries.png';
import patina_hero_s1 from '/img/instruments/videomancer/patina/patina_hero_s1.png';
import patina_hero_s2 from '/img/instruments/videomancer/patina/patina_hero_s2.png';
import patina_hero_s3 from '/img/instruments/videomancer/patina/patina_hero_s3.png';
import patina_hero_s4 from '/img/instruments/videomancer/patina/patina_hero_s4.png';
import patina_hero_s5 from '/img/instruments/videomancer/patina/patina_hero_s5.png';
import patina_hero_s6 from '/img/instruments/videomancer/patina/patina_hero_s6.png';
import patina_ex1_s1 from '/img/instruments/videomancer/patina/patina_ex1_s1.png';
import patina_ex1_s2 from '/img/instruments/videomancer/patina/patina_ex1_s2.png';
import patina_ex1_s3 from '/img/instruments/videomancer/patina/patina_ex1_s3.png';
import patina_ex1_s4 from '/img/instruments/videomancer/patina/patina_ex1_s4.png';
import patina_ex1_s5 from '/img/instruments/videomancer/patina/patina_ex1_s5.png';
import patina_ex1_s6 from '/img/instruments/videomancer/patina/patina_ex1_s6.png';
import patina_ex2_s1 from '/img/instruments/videomancer/patina/patina_ex2_s1.png';
import patina_ex2_s2 from '/img/instruments/videomancer/patina/patina_ex2_s2.png';
import patina_ex2_s3 from '/img/instruments/videomancer/patina/patina_ex2_s3.png';
import patina_ex2_s4 from '/img/instruments/videomancer/patina/patina_ex2_s4.png';
import patina_ex2_s5 from '/img/instruments/videomancer/patina/patina_ex2_s5.png';
import patina_ex2_s6 from '/img/instruments/videomancer/patina/patina_ex2_s6.png';
import patina_ex3_s1 from '/img/instruments/videomancer/patina/patina_ex3_s1.png';
import patina_ex3_s2 from '/img/instruments/videomancer/patina/patina_ex3_s2.png';
import patina_ex3_s3 from '/img/instruments/videomancer/patina/patina_ex3_s3.png';
import patina_ex3_s4 from '/img/instruments/videomancer/patina/patina_ex3_s4.png';
import patina_ex3_s5 from '/img/instruments/videomancer/patina/patina_ex3_s5.png';
import patina_ex3_s6 from '/img/instruments/videomancer/patina/patina_ex3_s6.png';

# Patina

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: patina_source1_boat, after: patina_hero_s1 },
    { label: "Sunset", before: patina_source2_sunset, after: patina_hero_s2 },
    { label: "Clouds", before: patina_source3_clouds, after: patina_hero_s3 },
    { label: "Pattern", before: patina_source4_pattern, after: patina_hero_s4 },
    { label: "Man", before: patina_source5_man, after: patina_hero_s5 },
    { label: "Berries", before: patina_source6_berries, after: patina_hero_s6 },
  ]}
/>
*Patina applying LFSR-seeded oxidation, copper tinting, and verdigris overlay to simulate the progressive aging of metal surfaces.*

---

## Overview

Copper starts bright and warm. Over decades of exposure to air and moisture, a thin oxide layer forms — first darkening the surface to a ruddy brown, then blooming into the distinctive blue-green crust called verdigris. Patina simulates this electrochemical aging process as a real-time video effect. Every pixel is evaluated against a spatial noise field to determine whether it has "oxidized." Oxidized pixels darken, shift toward teal-green chrominance, and gain a rough surface texture. Non-oxidized pixels retain a warm copper or neutral bronze tone.

The program divides its processing into six stages: input registration with position tracking, a spatial hash that combines an LFSR noise source with coarsened pixel coordinates, an oxidation mask that compares the hash against a threshold, a darkening stage that reduces luminance based on oxidation depth, a chroma tinting stage that applies verdigris color to oxidized pixels and warm copper to clean metal, and a final composition with wet/dry mix. An optional animation mode advances the oxidation frontier frame by frame, simulating the slow spread of corrosion over time.

At conservative settings, Patina adds a subtle warm-metallic grade to the image. At extreme settings, it transforms the source into an abstract surface of dark corroded patches and bright green-blue oxide blooms, resembling aerial photographs of aged copper rooftops.

---

## Quick Start

1. **Low Age for color grading**: Age below 20% with Copper mode creates a warm photographic grade without any visible oxidation texture. Use this as a subtle color correction tool.
2. **Spot Size controls texture scale**: The four discrete coarseness levels produce very different looks. Spend time sweeping this control slowly to understand the transitions.
3. **Roughness is the realism control**: Real verdigris is never smooth. Even a small amount of roughness (10–20%) makes the effect look more natural and less like a tint overlay.

---

## Background

### What Is Verdigris?

Verdigris is the green patina that forms on copper, bronze, and brass when they are exposed to air or seawater over long periods. Chemically, it is a mixture of copper carbonates and copper chlorides. The Statue of Liberty, originally the color of a new penny, turned green over several decades as its copper skin oxidized. In the video domain, Patina approximates this by pushing the U chrominance channel upward (toward blue-green) and pulling V downward (away from red-orange). The Color Intensity parameter controls the strength of this chromatic shift.

### How Does Spatial Noise Create Oxidation Patterns?

Real oxidation doesn't happen uniformly — it starts at imperfections, cracks, and exposed edges, then spreads outward in irregular patterns. Patina models this by generating a pseudo-random noise field from a 16-bit LFSR (linear-feedback shift register). The LFSR output is XOR-hashed with coarsened pixel coordinates to produce a per-pixel noise value. When this value falls below the oxidation threshold (set by the Age control), the pixel is considered oxidized. The Spot Size parameter controls the coordinate coarsening, which determines the spatial scale of the oxidation patches — small spots create fine stipple, large spots create broad corroded regions.

### What Is an LFSR?

A **linear-feedback shift register** is a simple circuit that produces a long, deterministic sequence of pseudo-random bits. It shifts its internal state by one bit each clock cycle, feeding back a combination of tapped bits via XOR. The sequence repeats after $2^n - 1$ cycles (65,535 for a 16-bit LFSR). Patina uses the LFSR as a spatially-varying noise source — the bit pattern is different at every pixel position and every frame, but reproducible given the same seed. This gives the oxidation texture its characteristic granularity without requiring block RAM for a stored noise table.

### How Does Position-Dependent Aging Work?

When animation is enabled, Patina advances a frame counter that scales with the Front Speed parameter. This counter is combined with the Age threshold to create a time-varying oxidation frontier. The Reverse toggle inverts the animation direction, simulating de-oxidation (chemical cleaning of the surface). The spatial hash ensures that the frontier doesn't sweep uniformly — it creeps through the noise field, oxidizing some regions early and others late, producing a naturalistic temporal spread.

### Copper vs. Bronze Base Metal

Toggle 7 selects between copper and bronze as the base metal interpretation. In copper mode, non-oxidized pixels receive a slight warm V-channel boost (orange tint). Oxidized pixels in copper mode receive the standard verdigris shift. In bronze mode, non-oxidized pixels remain chromatically neutral, and oxidized pixels receive an additional U-channel boost (extra green), simulating the distinct patination of bronze alloys. The difference is subtle but visible on close inspection.


---

## Signal Flow

Input Register → Spatial Noise Hash → Oxidation Mask → Darken Y → Teal/Green Tinting → Compose Output

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Position Counters ────────────────
│   ├─ Latch Y, U, V
│   ├─ Track horizontal and vertical position
│   └─ Advance frame counter (if Animate enabled)
│
├── Stage 2: Spatial Noise Hash + Oxidation Threshold ──────────
│   ├─ Coarsen position by Spot Size (4 levels)
│   ├─ XOR hash coarsened (h,v) with LFSR output
│   └─ Compute threshold = clamp(Age + animation_phase, 0, 1023)
│
├── Stage 3: Oxidation Mask ────────────────────────────────────
│   ├─ Compare noise_val < threshold → oxidized flag
│   └─ Compute oxide_depth = threshold − noise_val (gradient)
│
├── Stage 4: Darken Y + Surface Roughness ──────────────────────
│   ├─ Oxidized: Y − dark_amt (Heavy/Light scales depth)
│   │            + roughness noise (LFSR-derived)
│   └─ Non-oxidized: Y + base_tone/4 (warm brightness boost)
│
├── Stage 5: Teal/Green Tinting ────────────────────────────────
│   ├─ Oxidized: U + color_intensity/2, V − color_intensity/2
│   │            Bronze: extra U + color_intensity/8
│   └─ Non-oxidized: Copper: V + base_tone/16 (warm tint)
│   │                Bronze: neutral pass-through
│
├── Stage 6: Compose Output ────────────────────────────────────
│   └─ Latch processed Y, U, V
│
├── Interpolator Stage: Wet/Dry Mix (3x interpolator_u) ────────
│   └─ Crossfade between delayed dry input and processed output
│
├── Sync Delay Pipeline (10 clocks) ────────────────────────────
│   └─ Delay hsync, vsync, field, Y, U, V for alignment
│
└── Output Assignment ──────────────────────────────────────────
    └─ Bypass selects delayed input or mixed output
```

The oxidation threshold combines the static Age control with a time-varying animation phase, producing a frontier that creeps through the spatial noise field. The LFSR runs freely every clock cycle (always enabled), so its output varies with pixel position within a frame. Crucially, the same LFSR serves double duty: it provides both the spatial hash input (via XOR with coordinates) and the roughness texture noise (via its lower 8 bits). Stage 4 and Stage 5 branch on the oxidation mask — oxidized and non-oxidized pixels follow completely different processing paths, with the mask acting as a hard switch rather than a crossfade.

---

## Parameter Reference

<img src={patina_control_panel} alt="Videomancer front panel with Patina loaded"/>
*Videomancer's front panel with Patina active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Age Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Age. Sets the baseline oxidation coverage — the proportion of pixels classified as oxidized. At zero, no pixels pass the threshold and the entire image retains its base metal appearance. As Age increases, more of the spatial noise field falls below the threshold and the verdigris patches grow. At maximum, virtually every pixel is oxidized and the image takes on a uniformly dark, teal-green cast. This is the primary creative control — it determines how much of the surface has corroded.

---

#### Knob 2 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Spot Size. Controls the spatial coarseness of the oxidation pattern by selecting which bits of the position counters feed the spatial hash. At low values, the hash uses fine-resolution coordinates and the oxidation texture is a dense pixel-level stipple. At high values, the hash uses coarsened coordinates (upper bits only), producing broad, blocky oxidation patches. There are four discrete coarseness levels corresponding to threshold boundaries at register values 256, 512, and 768.

---

#### Knob 3 — Frontier
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Color Intensity. Determines the strength of the verdigris chroma tint applied to oxidized pixels. The register value is halved to produce the tint amount: U increases and V decreases by this amount. At zero, oxidized pixels darken without any color shift — pure luminance aging. At maximum, the teal-green shift is dramatic. In Bronze mode, an additional quarter of this value is added to U for extra green emphasis.

---

#### Knob 4 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Roughness. Controls the amplitude of LFSR-derived luminance noise added to oxidized pixels during Stage 4. The register value is right-shifted by 2 and AND-masked with the lower 8 bits of the LFSR output. At zero, oxidized regions are smooth. As roughness increases, the oxide surface gains a gritty, irregular texture. This simulates the physical roughness of real verdigris, which is never perfectly smooth.

---

#### Knob 5 — Roughness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Front Speed. When animation is enabled (Toggle 9), this parameter scales the rate at which the oxidation frontier advances. The register value masks the frame counter bits — higher values allow more frame counter bits through, producing faster frontier movement. At minimum, the animation advances very slowly. At maximum, the oxidation front sweeps across the noise field rapidly. Has no visible effect when animation is disabled.

---

#### Knob 6 — Base Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Base Tone. Adjusts the brightness of non-oxidized (clean metal) pixels. The register value is right-shifted by 2 and added to the luminance of pixels that did not pass the oxidation threshold. This simulates the base reflectivity of the metal — low values leave the source luminance untouched, high values brighten clean metal areas. In copper mode, a scaled fraction of Base Tone also adds a warm V-channel tint to non-oxidized pixels (base_tone / 16).

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Metal** | Copper | Iron |
| **8 — Stage** | Fresh | Full |
| **9 — Animate** | Off | On |
| **10 — Reveal** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control the metal type, patina intensity, animation, reversal, and bypass. Toggle 7 and Toggle 8 interact with the tinting and darkening stages to define the character of the oxidation effect. Toggle 9 and Toggle 10 control the time-domain behavior. Toggle 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Patina processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Patina-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from basic copper toning through animated oxidation sequences. Each demonstrates a different aspect of the patina simulation pipeline.

### Exercise 1: Warm Copper Grade

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: patina_source1_boat, after: patina_ex1_s1 },
    { label: "Sunset", before: patina_source2_sunset, after: patina_ex1_s2 },
    { label: "Clouds", before: patina_source3_clouds, after: patina_ex1_s3 },
    { label: "Pattern", before: patina_source4_pattern, after: patina_ex1_s4 },
    { label: "Man", before: patina_source5_man, after: patina_ex1_s5 },
    { label: "Berries", before: patina_source6_berries, after: patina_ex1_s6 },
  ]}
/>
*Warm Copper Grade — simulated result across source images.*
**Source**: Portrait or still-life footage with skin tones and neutral backgrounds.

**What You'll Create**: Use minimal oxidation to apply a warm copper color grade, understanding the base metal tinting path.

1. **Copper warmth**: Set Age to ~15%. Only scattered pixels oxidize. With Copper/Bronze off (Copper mode), notice the subtle warm shift on non-oxidized pixels from the Base Tone V-channel tint.
2. **Base Tone brightness**: Increase Base Tone to ~70%. Non-oxidized areas brighten, enhancing the metallic sheen.
3. **Minimal color**: Set Color Intensity to ~20%. The few oxidized pixels gain a faint teal cast.
4. **Compare**: Toggle Bypass to compare with the unprocessed source. The change is subtle — a warm photographic grade.
5. **Bronze alternative**: Toggle Copper/Bronze on. Non-oxidized areas lose their warm tint, becoming chromatically neutral. The overall feel shifts cooler.

**Key concepts**: Base Tone adds brightness and warm tint to clean metal, Copper vs. Bronze affects both oxidized and non-oxidized color paths, low Age settings create photographic color grades

---

### Exercise 2: Verdigris Texture

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: patina_source1_boat, after: patina_ex2_s1 },
    { label: "Sunset", before: patina_source2_sunset, after: patina_ex2_s2 },
    { label: "Clouds", before: patina_source3_clouds, after: patina_ex2_s3 },
    { label: "Pattern", before: patina_source4_pattern, after: patina_ex2_s4 },
    { label: "Man", before: patina_source5_man, after: patina_ex2_s5 },
    { label: "Berries", before: patina_source6_berries, after: patina_ex2_s6 },
  ]}
/>
*Verdigris Texture — simulated result across source images.*
**Source**: Architectural footage — building facades, metalwork, or stone surfaces.

**What You'll Create**: Create a heavy verdigris patina with visible texture, exploring the interaction between oxidation depth, roughness, and color intensity.

1. **Coverage**: Set Age to ~60%. Roughly half the image should be oxidized.
2. **Large patches**: Increase Spot Size to ~80%. The oxidation forms broad, irregular regions.
3. **Dark oxide**: Enable Heavy/Light (Heavy, on). Oxidized areas darken dramatically.
4. **Green tint**: Increase Color Intensity to ~75%. Oxidized regions turn distinctly teal-green.
5. **Surface texture**: Increase Roughness to ~65%. The oxidized surface gains a gritty, irregular noise texture.
6. **Contrast**: Notice how non-oxidized areas remain bright (boosted by Base Tone) while oxidized areas are dark and green. This contrast creates the characteristic patina look.

**Key concepts**: Oxidation mask is a hard switch (not a blend), roughness adds LFSR noise to oxidized Y only, Heavy vs. Light controls darkening gain, Spot Size has four discrete coarsening levels

---

### Exercise 3: Animated Oxidation

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: patina_source1_boat, after: patina_ex3_s1 },
    { label: "Sunset", before: patina_source2_sunset, after: patina_ex3_s2 },
    { label: "Clouds", before: patina_source3_clouds, after: patina_ex3_s3 },
    { label: "Pattern", before: patina_source4_pattern, after: patina_ex3_s4 },
    { label: "Man", before: patina_source5_man, after: patina_ex3_s5 },
    { label: "Berries", before: patina_source6_berries, after: patina_ex3_s6 },
  ]}
/>
*Animated Oxidation — simulated result across source images.*
**Source**: Any video with slow or moderate motion — landscapes, time-lapse, or abstract patterns.

**What You'll Create**: Enable animation to watch the oxidation frontier advance across the image in real time, then reverse it.

1. **Prepare**: Set Age to ~30%, Spot Size ~50%, Color Intensity ~60%, Roughness ~40%.
2. **Start animation**: Toggle Animate on. The verdigris patches begin to grow frame by frame.
3. **Speed control**: Adjust Front Speed. Low values produce a slow, geological creep. High values produce rapid coverage.
4. **Watch the frontier**: The oxidation doesn't sweep uniformly — it fills in the spatial noise field, creating an irregular, organic spreading pattern.
5. **Reverse**: Toggle Reverse on. The direction inverts — verdigris retreats, revealing clean copper underneath.
6. **Mix blend**: Lower Mix to ~60% to overlay the animated oxidation subtly over the source, preserving more of the original image.

**Key concepts**: Animation advances the oxidation threshold over time, the spatial noise field determines spread order (not a simple wipe), Reverse inverts the phase, Front Speed masks frame counter bits

---


## Tips

- **Heavy patina for drama**: The Heavy/Light toggle doubles the darkening intensity. Use Heavy for dramatic, high-contrast oxidation. Use Light for a weathered, lived-in patina.
- **Animation is geological**: At low Front Speed, the oxidation frontier advances very slowly — let it run for 30+ seconds to see the full progression.
- **Bronze for cooler results**: Bronze mode removes the warm copper tint from clean metal and adds extra green to oxidized areas, producing a colder, more industrial look.
- **Mix for overlay**: Setting Mix to 40–60% overlays the patina effect over the source, preserving the original image structure while adding an aged quality.
- **Feedback loops**: Routing the output back to the input compounds the darkening and tinting, producing progressively deeper oxidation with each pass.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chrominance** | The color-difference components (U and V) of a YUV video signal, encoding hue and saturation information. |
| **LFSR** | Linear-Feedback Shift Register; a simple digital circuit that generates a long pseudo-random bit sequence. Used as a spatial noise source. |
| **Luminance** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Oxidation** | A chemical reaction where metal combines with oxygen, forming an oxide layer. In Patina, this refers to pixels that have been darkened and tinted. |
| **Patina** | The colored surface layer that forms on metals through long-term oxidation, especially the green-blue verdigris on copper. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage used in video processing. Patina's base tone adjustment is a simplified form. |
| **Spatial Hash** | An XOR combination of pixel coordinates and LFSR output that produces a pseudo-random value unique to each screen position. |
| **Verdigris** | The green-blue patina (copper carbonate/chloride) that forms on copper surfaces exposed to air and moisture over time. |
| **XOR** | Exclusive OR; a bitwise operation where the output is 1 when the inputs differ. Used to combine position and noise values. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
