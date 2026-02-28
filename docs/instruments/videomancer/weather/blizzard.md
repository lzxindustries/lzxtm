---
draft: true
sidebar_position: 22
slug: /instruments/videomancer/blizzard
title: "Blizzard"
image: /img/instruments/videomancer/blizzard/blizzard_hero.png
description: "Program guide for Blizzard, a Videomancer weather program for the LZX video synthesizer."
---

import blizzard_hero from '/img/instruments/videomancer/blizzard/blizzard_hero.png';
import blizzard_before_after from '/img/instruments/videomancer/blizzard/blizzard_before_after.png';
import blizzard_control_panel from '/img/instruments/videomancer/blizzard/blizzard_control_panel.png';
import blizzard_exercise1_result from '/img/instruments/videomancer/blizzard/blizzard_exercise1_result.png';
import blizzard_exercise2_result from '/img/instruments/videomancer/blizzard/blizzard_exercise2_result.png';
import blizzard_exercise3_result from '/img/instruments/videomancer/blizzard/blizzard_exercise3_result.png';

# Blizzard

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={blizzard_hero} alt="Blizzard hero image"/>
*Blizzard compositing multi-layer parallax snowfall with frost accumulation over a winter landscape source.*
<img src={blizzard_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Blizzard applied.*

---

## Overview

Snow in real life has depth. Flakes close to the viewer are large, bright, and fast; flakes in the distance are small, dim, and slow. The brain assembles these cues into a three-dimensional volume of falling particles — an effect that flat video overlays rarely capture. Blizzard recreates this depth illusion using two independent particle layers with parallax separation: a near layer with bright, fast-falling flakes and a far layer with dimmer, slower flakes on a finer grid.

Each layer uses an LFSR-driven pseudo-random hash to determine flake positions on a per-pixel basis. Per-frame accumulators shift the particle field vertically (gravity) and horizontally (wind drift) without any multiply operations in the pixel data path. Flake density, size, fall speed, wind direction, and brightness are all independently controllable. An optional frost overlay progressively darkens the top of the frame with a blue tint, simulating ice accumulation on a camera lens or window.

The entire program operates without BRAM — all particle positions are computed algorithmically from pixel coordinates XORed with LFSR noise and frame-accumulated offsets. The result is a convincing seasonal weather effect that transforms any video source into a snowy scene, from gentle flurries to heavy blizzard whiteout conditions.

---

## Background

### Parallax Particle Systems

Real snowfall exhibits depth parallax: near particles move fast and appear large, far particles move slowly and appear small. Blizzard simulates this with two independent layers, each with its own position accumulators and fall rates. The near layer's vertical offset accumulates at the full fall speed parameter, while the far layer advances at half rate. The same ratio applies to horizontal wind drift. This 2:1 speed ratio, combined with the far layer's dimmer brightness, creates a convincing stereoscopic depth cue even on a flat display.

### LFSR-Based Flake Placement

Rather than storing particle positions in memory, Blizzard uses two 16-bit linear-feedback shift registers (LFSRs) running at pixel clock rate. The LFSR output is XORed with position coordinates to create a spatially varying pseudo-random field. Flake "hits" occur where the coordinate-XORed LFSR value falls below a density threshold on a coarse grid — this produces spatially distributed particles without any memory storage or particle tracking.

### Grid-Based Hit Testing

Flake placement uses bitwise grid masking: the lower bits of the hashed coordinate are compared against a small threshold (1-2 pixels) to determine whether the current pixel is at a grid intersection point. The grid spacing is controlled by how many bits are masked. Combined with the density threshold on the upper bits, this creates a sparse-but-regular distribution of flake positions. The grid mask is derived from the Flake Size parameter — larger flake sizes use wider grids with more spacing between potential flake positions.

### Frost Accumulation

The frost overlay simulates ice forming on a camera lens or window. A descending frost line advances from the top of the frame at a rate controlled by the Frost Rate parameter. Above the frost line, pixel brightness is halved and a slight blue chromatic shift is applied. The frost line only advances when Frost is enabled and never exceeds the frame height, so it gradually fills the frame from top to bottom over time.

### Additive Compositing

Snow flakes are composited additively — their brightness is added to the input video rather than replacing it. This physically correct model reflects how real snow particles scatter light in front of a camera: they add brightness to whatever is behind them. The additive model allows flakes to be visible against both dark and bright backgrounds, though they are most prominent against dark source regions.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   │
│   ├─ 1. H/V Counters           (pixel position from sync edges)
│   └─ 2. Per-Frame Accumulators  (fall offset, wind offset, frost line)
│
├── Stage 1: Hash + Grid ──────────────────────────────────────
│   │
│   ├─ 3. Near Layer Hash         (coord + near_offset XOR LFSR1)
│   ├─ 4. Far Layer Hash          (coord + far_offset XOR LFSR2)
│   └─ 5. Grid Mask Decode        (flake_size → bit mask width)
│
├── Stage 2: Hit Test ─────────────────────────────────────────
│   │
│   ├─ 6. Near Hit                (grid intersection + density threshold)
│   └─ 7. Far Hit                 (finer grid, lower density)
│
├── Stage 3: Brightness ───────────────────────────────────────
│   │
│   ├─ 8. Near Brightness         (hit × brightness parameter)
│   ├─ 9. Far Brightness          (hit × brightness/2, optional depth blur)
│   └─ 10. Accumulate             (saturating add near + far)
│
├── Stage 4-5: Frost + Composite ──────────────────────────────
│   │
│   ├─ 11. Frost Overlay          (halve Y, blue-shift UV above frost line)
│   └─ 12. Additive Snow          (Y += accumulated brightness)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ 13. Interpolator × 3       (dry/wet crossfade Y, U, V)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The key architectural choice is additive compositing: snow brightness is *added* to the input luma rather than replacing it. This means flakes appear as bright spots over the source video — physically correct for light-scattering particles. The frost overlay is subtractive: it halves brightness and shifts chroma toward blue. When both frost and snow are active, the bottom portion of the frame shows snow over the original source while the top portion shows snow over a darkened, blue-tinted version — exactly how a frosting window with snowfall outside would appear.

---

## Parameter Reference

<img src={blizzard_control_panel} alt="Videomancer front panel with Blizzard loaded"/>
*Videomancer's front panel with Blizzard active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the density of flakes in both layers. At low values, snow is sparse — individual flake positions are widely spaced and the source video dominates. At high values, flakes fill the frame densely. The density threshold is applied independently to each layer, with the far layer using half the threshold of the near layer, so low density settings produce mostly near-layer flakes while high density settings activate both layers fully.

---

#### Knob 2 — Wind
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the lateral wind speed. This determines how quickly flakes drift horizontally as they fall. At 0%, there is no horizontal drift — flakes fall straight down. At 100%, the horizontal drift rate matches the vertical fall speed, producing diagonal snowfall trajectories. The Wind Direction toggle determines whether drift moves right or left. Wind affects both layers, with the far layer drifting at half the near layer's rate to maintain depth parallax.

---

#### Knob 3 — Flake Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the flake size by adjusting the hit-test grid spacing. Small values produce a fine grid with many small-flake positions. Larger values produce a coarse grid with fewer but visually larger flake positions. The grid uses power-of-two masking, so size changes are stepped rather than continuous. Combined with Density, this parameter determines the visual weight of the snowfall — large sparse flakes versus small dense flakes create very different moods.

---

#### Knob 4 — Frost Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the rate at which the frost line descends from the top of the frame. At 0%, frost does not advance (remains at the top edge). At higher values, the frost line descends faster, more quickly engulfing the frame in the blue-tinted, darkened frost overlay. The frost line only advances when the Frost toggle is enabled. Once the frost line reaches the bottom of the frame, additional frost rate has no further effect.

---

#### Knob 5 — Fall Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the vertical fall speed of the snowflakes. This determines how quickly the per-frame vertical offset accumulator advances, making flakes appear to fall faster or slower. Higher values produce rapid snowfall; lower values produce gentle drifting. The near layer falls at the full rate while the far layer falls at half rate, maintaining the parallax depth illusion at all speeds.

---

#### Knob 6 — Opacity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the overall brightness (opacity) of snow flakes when they appear. Since compositing is additive, this parameter determines how much brightness each flake adds to the underlying source video. At low values, flakes are faint and translucent. At high values, flakes are bright white spots that can clip to maximum brightness over the source. The far layer uses half the brightness of the near layer (quarter if Depth Blur is enabled).

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Layers** | 1 | 2 |
| **8 — Drift Mode** | Sine | Random |
| **9 — Frost** | Off | On |
| **10 — Whiteout** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control wind direction, snowfall intensity, frost accumulation, depth rendering, and signal bypass. Wind Direction reverses the horizontal drift. Heavy/Light toggles between a base-density and double-density mode by forcing the density MSB high. Frost enables the progressive frost overlay. Depth Blur further attenuates the far layer's brightness for increased depth separation. Bypass passes the signal through unchanged.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet mix between the original input video and the snow-processed output. At 0% (fully dry), the output is the unprocessed input. At 100% (fully wet), the output is the full snowfall composite. Intermediate values blend between the two — at 50%, the snow effect is at half intensity, useful for subtle seasonal overlays.

---

## Guided Exercises

These exercises progress from gentle flurries to a full blizzard whiteout, exploring the interplay between snowflake density, wind drift, parallax depth, and frost accumulation.

### Exercise 1: Gentle Flurries

<img src={blizzard_exercise1_result} alt="Gentle Flurries result"/>
*Gentle Flurries — simulated result across source images.*
**Source**: Feed a landscape or outdoor scene (Kodak #24 — the mountain chalet provides natural winter context).

**Objective**: Create a gentle, sparse snowfall with visible depth parallax between near and far layers.

1. Set Density to 30% for sparse flake distribution.
2. Set Wind to 25% for gentle rightward drift.
3. Set Flake Size to 40% for medium-sized flakes.
4. Set Frost Amt to 0% (no frost).
5. Set Fall Speed to 35% for a slow, gentle drift.
6. Set Opacity to 70% for visible but not overwhelming flakes.
7. Set Wind Direction to first position (right drift).
8. Set Heavy/Light to first position (normal density).
9. Set Frost to Off.
10. Set Depth Blur to On — observe how far-layer flakes appear dimmer and more distant.
11. Set Mix to 100%.
12. Watch the two layers: near flakes fall fast and bright, far flakes drift slowly and dim.

**Key concepts**: The parallax depth illusion comes from two sources: the 2:1 speed ratio between near and far layers, and the brightness difference. Depth Blur increases this difference by further attenuating the far layer. Even with sparse density, the two-layer system creates a convincing volumetric quality.

---

### Exercise 2: Heavy Snowfall with Wind

<img src={blizzard_exercise2_result} alt="Heavy Snowfall with Wind result"/>
*Heavy Snowfall with Wind — simulated result across source images.*
**Source**: Feed a scene with mixed bright and dark regions (Kodak #13 — the mountain/water scene shows flakes clearly against both the bright sky and dark water).

**Objective**: Create a heavy blizzard with strong diagonal wind and maximum flake intensity.

1. Set Density to 80% for dense flake coverage.
2. Set Wind to 75% for strong lateral drift.
3. Set Flake Size to 60% for large, prominent flakes.
4. Set Frost Amt to 0% (isolate the snow effect).
5. Set Fall Speed to 75% for rapid downfall.
6. Set Opacity to 90% for bright, prominent flakes.
7. Set Wind Direction to first position (rightward drift).
8. Set Heavy/Light to second position (heavy mode — doubles density).
9. Set Frost to Off.
10. Set Depth Blur to Off (let far layer remain relatively bright).
11. Set Mix to 100%.
12. Observe the dense diagonal snowfall — the combination of high density, heavy mode, and fast fall creates blizzard intensity.

**Key concepts**: Heavy mode forces the density MSB high, roughly doubling the flake population. Combined with high Wind and Fall Speed, this creates diagonal trajectories where flakes appear to be driven by strong wind. The additive compositing means very bright flakes can wash out dark source regions, creating the whiteout effect of a real blizzard.

---

### Exercise 3: Frost and Snow Combined

<img src={blizzard_exercise3_result} alt="Frost and Snow Combined result"/>
*Frost and Snow Combined — simulated result across source images.*
**Source**: Feed a rural or architectural scene (Kodak #22 — the barn scene with its horizontal roof lines makes the frost line descent visually clear).

**Objective**: Combine progressive frost accumulation with moderate snowfall to create a full winter weather scene.

1. Set Density to 50% for moderate flake density.
2. Set Wind to 15% for light drift.
3. Set Flake Size to 35% for small-to-medium flakes.
4. Set Frost Amt to 60% for moderate frost advance rate.
5. Set Fall Speed to 45% for natural fall speed.
6. Set Opacity to 65% for naturally visible flakes.
7. Set Wind Direction to first position.
8. Set Heavy/Light to first position (normal).
9. Enable Frost — observe the frost line beginning to descend from the top.
10. Set Depth Blur to On for atmospheric depth.
11. Set Mix to 100%.
12. Watch as frost progressively darkens and blue-tints the upper portion of the frame while snow falls over the entire image. The frost line creates a visible horizon between the iced-over and clear regions.

**Key concepts**: Frost and snow interact compositionally: the frost overlay darkens and blue-shifts pixels above the frost line, then snow flakes are added on top. This means snow above the frost line appears brighter relative to the darkened background. The blue tint plus bright white flakes creates a cold, wintry color palette — exactly the look of viewing snowfall through a frosting window.

---


## Tips

- **Start gentle**: Begin with low density (20-30%) and moderate opacity to establish the parallax depth before increasing to blizzard intensity. The depth effect is most apparent when individual flakes are distinguishable.
- **Wind creates mood**: No wind produces peaceful, straight-down snowfall. Light wind (10-25%) creates gentle drifting. Heavy wind (60%+) produces driven, dramatic blizzard trajectories.
- **Frost is cumulative**: The frost line only advances while enabled — use it as a slow reveal effect that gradually transforms the top of the frame. Timing the frost advance to musical cues creates dramatic building tension.
- **Depth Blur for atmosphere**: Enabling Depth Blur makes the far layer significantly dimmer, increasing the sense of atmospheric depth but reducing overall snow density visually. Disable it for uniform blizzard intensity.
- **Dark sources look best**: Snow flakes are additive (white), so they read most clearly against dark or mid-tone source material. Very bright sources can make flakes hard to see at lower opacity settings.
- **Mix for subtlety**: At 30-50% mix, the snow effect becomes a subtle seasonal overlay — enough to suggest winter atmosphere without obscuring the source content.
- **Combine with color correction**: Feeding a blue-tinted or desaturated source enhances the winter mood. The frost overlay adds its own blue tint, so a warm source creates an interesting warm/cool contrast.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive compositing** | A blending method where pixel brightness values are summed rather than averaged, causing overlapping elements to appear brighter; physically models light-scattering particles. |
| **Chromatic shift** | A fixed offset applied to the U and V colour channels of a video signal, producing an overall colour cast such as the blue tint of the frost overlay. |
| **Depth blur** | Additional brightness attenuation applied to the far snow layer to increase the perceived distance between near and far particles. |
| **Grid masking** | A technique using a bitwise AND operation to test whether a pixel coordinate falls on a regularly spaced grid, used here to determine potential flake positions. |
| **Interpolator** | A hardware mixing block that crossfades between two input signals using a weighted average, used here for dry/wet blending. |
| **LFSR** | Linear Feedback Shift Register; a shift register that produces a deterministic pseudo-random bit sequence, used here to generate spatially varying flake positions without memory storage. |
| **Luma** | The brightness component (Y) of a YUV video signal, independent of colour information. |
| **MSB** | Most Significant Bit; the highest-value bit in a binary number, forced high in Heavy mode to approximately double flake density. |
| **Parallax** | The apparent difference in speed or position of objects at different depths; Blizzard uses a 2:1 speed ratio between near and far layers to simulate volumetric depth. |
| **Saturating add** | An addition operation that clamps the result at the maximum representable value (1023) rather than wrapping around on overflow. |
| **XOR** | Exclusive-OR; a bitwise operation that outputs 1 when its two input bits differ, used here to combine pixel coordinates with LFSR output for pseudo-random spatial distribution. |
| **YUV** | A colour encoding system that separates brightness (Y) from two colour-difference components (U and V), used as the native signal format in Videomancer. |

---
