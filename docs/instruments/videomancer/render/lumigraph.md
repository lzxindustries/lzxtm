---
draft: true
sidebar_position: 172
slug: /instruments/videomancer/lumigraph
title: "Lumigraph"
image: /img/instruments/videomancer/lumigraph/lumigraph_hero.png
description: "Lumigraph generates slowly evolving fields of diffuse colour inspired by Thomas Wilfred's Lumia compositions — the earliest abstract light art, first exhibited at the Museum of Modern Art in the 1920s."
---

import lumigraph_hero from '/img/instruments/videomancer/lumigraph/lumigraph_hero.png';
import lumigraph_animation from '/img/instruments/videomancer/lumigraph/lumigraph_animation.gif';
import lumigraph_control_panel from '/img/instruments/videomancer/lumigraph/lumigraph_control_panel.png';
import lumigraph_exercise1_result from '/img/instruments/videomancer/lumigraph/lumigraph_exercise1_result.gif';
import lumigraph_exercise2_result from '/img/instruments/videomancer/lumigraph/lumigraph_exercise2_result.gif';
import lumigraph_exercise3_result from '/img/instruments/videomancer/lumigraph/lumigraph_exercise3_result.gif';

# Lumigraph

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lumigraph_hero} alt="Lumigraph hero image"/>
*Vast pools of luminous colour drift glacially across the screen, overlapping in soft additive clouds of light.*
<img src={lumigraph_animation} alt="Lumigraph animated output"/>
*Lumigraph output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Lumigraph generates slowly evolving fields of diffuse colour inspired by Thomas Wilfred's Lumia compositions — the earliest abstract light art, first exhibited at the Museum of Modern Art in the 1920s. Wilfred built the Clavilux, a keyboard-controlled instrument that projected immense soft-edged forms of tinted light through rotating glass discs and shaped apertures. His "Lumia" works featured glacial drift, additive colour mixing where pools overlapped, and hypnotic temporal evolution measured in hours rather than seconds.

This implementation generates 3 or 5 large elliptical colour regions, each following an independent DDS-driven Lissajous drift path. Per-pool colour comes from a palette table (Warm or Full spectrum) scaled by saturation. Where pools overlap, their luminance and chrominance contributions are summed additively, producing luminous secondary hues. The result is a framebuffer-free synthesis — zero BRAM, pure combinatorial rendering — that captures the serene, meditative quality of Wilfred's light compositions.

The entire rendering pipeline runs per-pixel with no memory dependency, making Lumigraph one of the most resource-efficient programs in the collection while producing some of its most visually refined output.

---

## Background

### Thomas Wilfred and the Clavilux

Thomas Wilfred (1889–1968) is considered the pioneer of abstract light art. Beginning in 1919, he developed the Clavilux — a succession of increasingly sophisticated instruments that projected coloured light through shaped apertures, rotating prisms, and translucent discs. His performances, which he called "Lumia," created slowly evolving compositions of pure light and colour without any representational imagery. The Museum of Modern Art acquired several of his autonomous "Lumia" compositions, which run continuously without performer intervention.

### Additive Colour Mixing

When multiple light sources overlap on a surface, their contributions add. Red plus green yields yellow; all primaries together approach white. Lumigraph implements this principle digitally: each pool contributes luminance and signed chrominance, and the contributions are summed. Where two warm-toned pools overlap, the luminance doubles and the chrominance shifts — producing the naturally luminous secondary colours that characterise projected light art.

### Lissajous Drift Paths

Each pool centre follows a 2D Lissajous trajectory driven by two independent DDS phase accumulators (X and Y). The phase increments include prime-number offsets per pool index (23i+7 for X, 31i+13 for Y), ensuring that pools drift at slightly different rates and never synchronise exactly. This produces the endlessly evolving, non-repeating spatial relationships that make Wilfred-style compositions meditative rather than mechanical.

### Distance-Squared Falloff

The intensity of each pool follows an inverse relationship with the squared distance from its centre. Pixels inside the pool radius receive an intensity proportional to $(r^2 - d^2) / r^2$, providing a smooth gradient from full brightness at the centre to zero at the edge. The Softness control adjusts the transition: high softness produces a gradual gaussian-like gradient; low softness creates a harder disc with a narrow fringe.

### Zero-BRAM Synthesis

Unlike most synthesis programs in the collection, Lumigraph uses no block RAM. Each pixel's colour is computed entirely from the current pool positions (stored in DDS phase registers) and the pixel's screen coordinates. This combinatorial approach limits the complexity of per-pixel processing but is ideal for the simple distance-based falloff that defines diffuse colour fields.


---

## Signal Flow

```
  ┌──────────────────────────────────────────────┐
  │  Pool DDS Drift (per frame)                   │
  │  5 × (X phase, Y phase) + speed + motion     │
  │  → sine_lookup → pool centres (cx, cy)       │
  └───────────────────┬──────────────────────────┘
                      │
  ┌───────────────────▼──────────────────────────┐
  │  Per-Pixel Pool Loop (i = 0..num_pools-1)    │
  │  dx = h_count - cx(i)                         │
  │  dy = v_count - cy(i)                         │
  │  dist² = dx² + dy²                            │
  │  radius² = (pool_size + 64)²                  │
  │  if dist² < radius²:                          │
  │    falloff = (radius² - dist²) >> 14          │
  │    intensity = (falloff > softness)            │
  │                ? 1023                          │
  │                : falloff × 1023 >> 10          │
  │    intensity × brightness → Y accum           │
  │    palette(i).u × saturation × intensity → U  │
  │    palette(i).v × saturation × intensity → V  │
  └───────────────────┬──────────────────────────┘
                      │
  ┌───────────────────▼──────────────────────────┐
  │  Video Seed: Y accum × input luma / 1023     │
  │  Clamp Y/U/V to [0, 1023]                    │
  └───────────────────┬──────────────────────────┘
                      │
  ┌───────────────────▼──────┐    ┌──────────┐
  │ wet Y/U/V                ├───►│ Interp   ├──► data_out
  └──────────────────────────┘    │ (dry/wet) │
                                  └──────────┘
```

The pool loop iterates over up to 5 pools per pixel clock cycle (unrolled in hardware). Only pools within their radius contribute to the accumulator. The distance-squared computation uses absolute values rather than true squaring — `|dx|²` and `|dy|²` are summed, providing a Manhattan-weighted Euclidean approximation that conserves LUTs.

The Hue Range parameter is declared as `polar_degs_360` in the TOML but internally just varies the diversity of colour across the pool ensemble. In the VHDL, each pool's chrominance is scaled by its palette entry and the saturation knob; hue_range is available for future per-pool phase rotation.

---

## Parameter Reference

<img src={lumigraph_control_panel} alt="Videomancer front panel with Lumigraph loaded"/>
*Videomancer's front panel with Lumigraph active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Drift Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Drift Speed controls how fast the colour pools move across the screen. At minimum the pools are nearly stationary, changing position so slowly that the eye barely perceives motion. At higher settings the pools glide visibly across the frame, their overlapping regions continuously shifting. The DDS phase increment is directly proportional to this value, with an additional per-pool prime offset ensuring each pool drifts at a unique rate.

---

#### Knob 2 — Pool Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |
| Suffix | % |

Pool Size sets the radius of each colour region. Small values produce compact disc-shaped pools that occupy a fraction of the screen. Large values create enormous elliptical fields that extend well beyond the visible area, filling the frame with their gradient. The radius is computed as (Pool Size + 64) in pixel units.

---

#### Knob 3 — Softness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Softness controls the edge gradient of each pool. At low Softness, pools have a narrow transition from full intensity to zero — appearing as relatively hard-edged discs. At high Softness, the falloff region extends further, creating a wide gaussian-like gradient that feathers each pool into the background. The implementation compares each pixel's falloff value against the Softness threshold: pixels with falloff exceeding the threshold are rendered at full brightness.

---

#### Knob 4 — Hue Range
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 180d |
| Suffix | d |

Hue Range sets the angular span of colours distributed across the ensemble. At minimum all pools share similar hues. At maximum the pools span the full colour wheel, producing complementary overlaps. This parameter affects the perceived diversity of the colour palette without changing the fundamental palette table.

---

#### Knob 5 — Saturation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Saturation scales the chrominance of each pool's colour contribution. At zero the output is greyscale — pure luminance pools with no colour. At maximum the pools carry their full palette chrominance, producing vivid tinted fields. The scaling is applied as a signed multiply of each palette entry's U and V offsets.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Brightness scales the luminance contribution of each pool. At minimum the pools contribute no visible light; at maximum each pool's intensity reaches full scale. This parameter directly multiplies the distance-falloff intensity before accumulation, affecting both the brightness of individual pools and the intensity of their overlapping regions.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pools** | 3 | 5 |
| **8 — Motion** | Slow | Medium |
| **9 — Palette** | Warm | Full |
| **10 — Video Seed** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the pool count, animation speed multiplier, colour palette, input interaction, and bypass. Pools determines the spatial complexity (3 pools for calm compositions, 5 for richer overlapping). Motion doubles the drift speed for faster evolution. Palette selects between warm amber/rose tones and full rainbow. Video Seed modulates the synthesis by the incoming video luminance. Bypass passes the input unchanged.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the input video (dry) and the Lumigraph synthesis (wet). At minimum the original video passes through; at maximum only the colour pools are visible. Intermediate positions overlay the pools on top of the video, creating a tinted wash effect.

---

## Guided Exercises

These exercises explore the meditative range of Lumigraph, from minimal ambient washes to vibrant additive colour fields.

### Exercise 1: Wilfred Meditation

<img src={lumigraph_exercise1_result} alt="Wilfred Meditation result"/>
*Wilfred Meditation — simulated result across source images.*
**Objective**: Create a slow, warm-toned Lumia composition with minimal pools and maximal softness.

1. Set Pools to 3, Motion to Slow.
2. Set Pool Size to 70% for large, room-filling fields.
3. Set Softness to 90% for extreme gradient.
4. Set Drift Speed to 10% for glacial motion.
5. Set Palette to Warm, Saturation to 60%, Brightness to 70%.
6. Sit back and observe the composition evolve over 30+ seconds.

**Key concepts**: Wilfred's compositions were designed for extended contemplation. The combination of large pool size, high softness, and slow drift creates a meditative experience where colour transitions happen gradually enough to be perceived subconsciously.

---

### Exercise 2: Full Spectrum Dense

<img src={lumigraph_exercise2_result} alt="Full Spectrum Dense result"/>
*Full Spectrum Dense — simulated result across source images.*
**Objective**: Create a richly coloured field with 5 pools using the Full palette for maximum additive mixing.

1. Set Pools to 5, Palette to Full.
2. Set Pool Size to 50%, Softness to 60%.
3. Set Drift Speed to 30%, Motion to Medium.
4. Set Saturation to 80%, Brightness to 60%.
5. Observe the primary-colour pools overlapping to produce secondaries.
6. Note how two overlapping pools produce a brighter region than either individually.

**Key concepts**: With the Full palette, overlapping red and green pools produce yellow; red and blue produce magenta; all three produce near-white. This demonstrates additive colour mixing — the fundamental principle of projected light art.

---

### Exercise 3: Stained Glass Overlay

<img src={lumigraph_exercise3_result} alt="Stained Glass Overlay result"/>
*Stained Glass Overlay — simulated result across source images.*
**Objective**: Use Video Seed to mask the Lumigraph synthesis with incoming video content.

1. Feed a contrasty image or video into Videomancer.
2. Set Pools to 5, Palette to Full, Saturation to 100%.
3. Enable Video Seed.
4. Set Brightness to 80%, Pool Size to 60%.
5. Observe how the colour pools appear only in the bright areas of the input.
6. Reduce Mix to 50% to blend the coloured pools over the original image.

**Key concepts**: Video Seed multiplies the synthesised luminance by the input Y channel. This creates a masking effect where the abstract colour fields are sculpted by the shape and texture of the incoming video — combining synthesis with processing.

---


## Tips

- **Slow is good**: Wilfred's compositions evolved over minutes. Set Drift Speed below 15% for the most meditative experience.
- **Softness over Size**: Increasing Softness has a more dramatic effect on the diffuse quality than increasing Pool Size. Try high Softness with moderate Size.
- **Warm for ambience**: The Warm palette is specifically tuned for ambient background compositions — all hues produce pleasant overlaps.
- **Full for education**: The Full palette demonstrates additive colour mixing clearly — use it to show how primaries combine.
- **Video Seed at half mix**: Video Seed is most effective at 40–60% Mix, where the colour pools tint the original image rather than replacing it.
- **3 pools for projection**: When using Lumigraph for projected installations, 3 pools with Warm palette and low drift create the most Wilfred-authentic experience.
- **Zero Saturation for light study**: Setting Saturation to 0% produces pure greyscale luminance pools — useful for studying falloff and overlap without colour distraction.

---
