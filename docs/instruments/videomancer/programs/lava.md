---
draft: true
sidebar_position: 167
slug: /instruments/videomancer/lava
title: "Lava"
image: /img/instruments/videomancer/lava/lava_hero.png
description: "Lava simulates the hypnotic motion of a lava lamp — viscous blobs of heated wax rising and falling through a translucent medium, merging when they touch and splitting apart as they drift."
---

import lava_hero from '/img/instruments/videomancer/lava/lava_hero.png';
import lava_animation from '/img/instruments/videomancer/lava/lava_animation.gif';
import lava_control_panel from '/img/instruments/videomancer/lava/lava_control_panel.png';
import lava_exercise1_result from '/img/instruments/videomancer/lava/lava_exercise1_result.gif';
import lava_exercise2_result from '/img/instruments/videomancer/lava/lava_exercise2_result.gif';
import lava_exercise3_result from '/img/instruments/videomancer/lava/lava_exercise3_result.gif';

# Lava

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lava_hero} alt="Lava hero image"/>
*Lava conjuring four molten blobs in the Classic Red palette — organic metaball surfaces merge and divide in slow vertical convection against a dark field.*
<img src={lava_animation} alt="Lava animated output"/>
*Lava output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Lava simulates the hypnotic motion of a lava lamp — viscous blobs of heated wax rising and falling through a translucent medium, merging when they touch and splitting apart as they drift. The effect is achieved through a metaball field computation: for every pixel on screen, the program sums the inverse-square distance contributions from four animated blob primitives. Where the accumulated field exceeds a threshold, the pixel is rendered as blob interior; where it falls below, it becomes background. The smooth falloff of the 1/d² function produces the characteristic organic merging behavior: as two blobs approach each other, their fields overlap and the isosurface smoothly joins them together.

The name *Lava* is a direct reference to the lava lamp, invented in 1963 by Edward Craven Walker under the brand name Astro Lamp. The device uses heat to melt colored wax suspended in a liquid of similar density, creating the slow, meditative blob motion that became an icon of 1960s counterculture and later 1990s retro aesthetics. Lava recreates this thermal convection digitally, with DDS oscillators providing the sinusoidal vertical motion and prime-number frequency ratios ensuring that the four blobs never quite repeat the same configuration.

Eight curated palettes provide distinct visual identities, from the warm reds and oranges of a classic lava lamp through alien greens, cosmic blues, and a psychedelic rainbow mode where chrominance cycles continuously through the YUV color wheel. An edge glow effect highlights the isosurface boundary — the transition zone where field values cross the threshold — reproducing the translucent rim-lighting visible in real wax lamps.

---

## Quick Start

1. **Threshold and Blob Size are complementary**: Increasing Blob Size makes the field stronger (blobs appear larger). Increasing Threshold makes the cutoff higher (blobs appear smaller). Find the balance where blobs are large enough to merge but small enough to separate.
2. **Edge Glow creates depth**: Even a small amount of edge glow dramatically improves the three-dimensional appearance of the blobs. The bright rim mimics the translucent wax edge in real lava lamps.
3. **Teardrop mode for realism**: Real lava lamp wax elongates as it rises due to drag and thermal gradients. Teardrop mode recreates this by halving the vertical distance in the field calculation.

---

## Background

### What Are Metaballs?

**Metaballs** (also called blobby objects or soft objects) were introduced by Jim Blinn in 1982 as a technique for modeling organic surfaces. Each metaball primitive defines a scalar field that falls off with distance from its center. The field contributions from multiple primitives are summed at every point in space, and an isosurface (constant-value surface) is extracted at a chosen threshold. The key visual property is smooth merging: as two metaballs approach, their combined field creates a continuous bridge between them, producing the characteristic liquid-like coalescence without any sharp boolean union edges.

In two dimensions — as in Lava — the field is evaluated per-pixel and the threshold produces filled regions rather than surfaces. The visual result resembles a microscope view of oil droplets merging on water, or the cross-section of a lava lamp's wax formations.

### Inverse-Square Distance Fields

The field function used in Lava is $f(\mathbf{p}) = \sum_{i} \frac{r_i^2}{|\mathbf{p} - \mathbf{c}_i|^2}$ where $\mathbf{c}_i$ is each blob center, $r_i$ is the blob radius, and $\mathbf{p}$ is the pixel coordinate. The inverse-square falloff produces soft, rounded field contours. Near a blob center the field is very high (approaching infinity at zero distance, clamped in hardware). Far from all blobs the field approaches zero. The threshold level determines how large the rendered blobs appear: a low threshold includes more pixels (larger blobs), while a high threshold restricts rendering to only the highest-field pixels near blob centers.

### Thermal Convection Motion

Real lava lamps operate on thermal convection: wax at the bottom is heated until its density drops below the surrounding liquid, causing it to rise. At the top, it cools, densifies, and sinks. This creates a continuous vertical circulation. Lava approximates this with sinusoidal DDS oscillators — each blob's vertical position follows a sine wave, oscillating between the top and bottom of the screen. The oscillation frequencies use prime-number-based ratios (7919, 11933, 5501, 9311) to ensure that the four blobs never synchronize, producing the endlessly varying configurations characteristic of real lava lamps.

### Isosurface Rendering and Edge Glow

The **isosurface** is the contour line where the field value equals the threshold. In real lava lamps, light shining through the glass creates a characteristic bright rim around each wax blob where the material transitions from opaque to translucent. Lava recreates this by detecting pixels whose field values fall within a narrow band around the threshold — the edge zone — and rendering them with a brighter or differently colored palette entry. This two-tone rendering (interior + edge) gives the blobs three-dimensional depth cues despite being rendered as flat 2D fields.

### Color Palettes and Hue Cycling

Lava provides eight palette presets stored as constant arrays, each defining three color sets: blob interior, edge glow, and tinted background. The eighth palette (Psychedelic) is special — instead of using fixed colors, it computes chrominance from a sine lookup of the field value plus a continuously cycling hue phase, producing rainbow-washed blobs that shift color in real time. This approach references the 1960s light-show aesthetic where projected colored oils produced slowly morphing chromatic fields.


---

## Signal Flow

```
┌──────────────────────────────────────────────────────────────────┐
│  Video Timing Generator                                          │
│     └─ Extracts sync, generates pixel/line counters              │
│        s_hcount (12-bit), s_vcount (12-bit)                      │
│                                                                  │
│  Blob Animation (update at vsync, gated by Freeze)               │
│     ├─ For each blob i (0–3):                                    │
│     │   vert_phase += C_VERT_FREQ(i) × rise_speed >> 6          │
│     │   horz_phase += C_HORZ_FREQ(i) × rise_speed >> 8          │
│     │   y_pos = 360 + sine_lookup(vert_phase) × 300 >> 9        │
│     │   x_pos = C_H_CENTERS(i) + sine_lookup(horz_phase)×80>>9  │
│     └─ Hue phase increments for psychedelic palette              │
│           ◄── Rise Speed (reg 2), Freeze (reg 6 bit 3)          │
│                                                                  │
│  Per-Pixel Metaball Evaluation (1 clk per blob, sequential)      │
│     ├─ For each active blob (0 to blob_count):                   │
│     │   dx = hcount − blob_x, dy = vcount − blob_y              │
│     │   if teardrop: dy = dy >> 1 (vertical elongation)          │
│     │   dist_sq = dx² + dy² (clamp ≥ 4)                         │
│     │   leading zeros → reciprocal approx: radius_sq >> shift    │
│     │   accum += contribution                                    │
│     └─ v_accum = sum of all blob 1/dist² contributions           │
│           ◄── Blob Count (reg 0), Blob Size (reg 1),            │
│               Blob Shape (reg 6 bit 1)                           │
│                                                                  │
│  Threshold + Edge Detection (same clock)                         │
│     ├─ inside_blob = (accum ≥ threshold)                         │
│     ├─ edge_lo = threshold − edge_glow(9:2)                     │
│     ├─ edge_hi = threshold + edge_glow(9:2)                     │
│     └─ near_edge = (accum ≥ edge_lo AND accum ≤ edge_hi)        │
│           ◄── Threshold (reg 3), Edge Glow (reg 5)              │
│                                                                  │
│  Colour Mapping (same clock)                                     │
│     ├─ Inside + Video Fill: pass through input video             │
│     ├─ Inside + near_edge: palette edge colour                   │
│     ├─ Inside + palette 7: psychedelic hue cycling               │
│     ├─ Inside (else): palette blob colour                        │
│     ├─ Outside + tinted_bg: palette background colour            │
│     └─ Outside (else): black + neutral chroma                    │
│           ◄── Palette (reg 4), Background (reg 6 bit 0),        │
│               Video Fill (reg 6 bit 2)                           │
│                                                                  │
│  Interpolator (4 clk, per Y/U/V)                                │
│     └─ mix = lerp(input_delayed, rendered, mix_amount)           │
│           ◄── Mix (reg 7)                                        │
└──────────────────────────────────────────────────────────────────┘

 Output = bypass ? input_delayed : mix_result
           ◄── Bypass (reg 6 bit 4)
```

The metaball field evaluation is the computationally heaviest part of the pipeline. For each pixel, the VHDL evaluates all four blobs sequentially in a single process, accumulating field contributions. The reciprocal approximation avoids a hardware divider by using a leading-zero-count technique: the number of leading zeros in the distance-squared value determines the shift amount applied to the radius-squared term, producing a coarse but visually effective 1/d² approximation. Blob animation runs in a separate process triggered at vsync, decoupled from the per-pixel evaluation. The prime-number DDS frequencies ensure quasi-random phase relationships between blobs. Edge detection uses a symmetric band around the threshold — the edge glow control widens or narrows this band, affecting how much of the isosurface transition zone is highlighted.

---

## Parameter Reference

<img src={lava_control_panel} alt="Videomancer front panel with Lava loaded"/>
*Videomancer's front panel with Lava active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Blob Count
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

Controls the number of active blobs contributing to the metaball field. The 10-bit register is quantized via its upper 3 bits (`blob_count(9:7) + 1`), but clamped to the hardware maximum of 4 blobs. At 1 blob, a single smooth disc floats and oscillates. At 2 blobs, merging and splitting interactions begin. At 3–4 blobs, the field becomes complex with multiple simultaneous merging events. Because the blob positions use prime-ratio frequencies, adding more blobs dramatically increases the variety of configurations the system visits over time.

---

#### Knob 2 — Blob Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the influence radius of each blob in the metaball field. The register value is squared (`blob_size × blob_size`) to produce a 20-bit radius-squared term used in the reciprocal distance computation. At low values, blobs have small spheres of influence and appear as isolated discs. At high values, the field extends far from each center, causing blobs to merge at greater distances and producing larger, more amorphous forms. Very high blob sizes can cause the entire screen to exceed the threshold, filling it with solid color.

---

#### Knob 3 — Rise Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the vertical oscillation speed of the blob animation. The register value is used as a multiplier against each blob's DDS frequency constant. At zero, blobs are frozen in place. At low values, they drift slowly in hypnotic convection cycles. At high values, blobs race up and down the screen. The same speed multiplier also affects the horizontal perturbation oscillators (but with a larger right-shift divisor), so high speeds produce both fast vertical motion and increased horizontal wobble. The Freeze toggle (reg 6 bit 3) overrides this control when active.

---

#### Knob 4 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the isosurface threshold for the metaball field. The 10-bit register is extended to 16 bits for comparison against the accumulated field value. At low thresholds, more pixels pass the test and the blobs appear large and widely merged. At high thresholds, only pixels very close to blob centers are rendered, producing small isolated dots. The threshold interacts strongly with Blob Size: increasing size while maintaining threshold creates larger blobs; increasing threshold while maintaining size creates smaller ones. The artistic sweet spot is where blobs are large enough to merge occasionally but small enough to separate between interactions.

---

#### Knob 5 — Palette
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Selects one of eight color palette presets. The upper 3 bits of the register (`palette_sel(9:7)`) index a constant array of palette entries. Each palette defines three color sets:

| Index | Name | Blob Interior | Edge Highlight | Tinted Background |
|-------|------|---------------|----------------|-------------------|
| 0 | Classic Red | Deep red | Orange | Dark warm |
| 1 | Cosmic Blue | Royal blue | Cyan | Dark blue |
| 2 | Alien Green | Lime green | Yellow | Dark green |
| 3 | Ultraviolet | Purple | Magenta | Dark violet |
| 4 | Solar | Orange | Yellow | Deep blue |
| 5 | Coral | Pink | White | Dark neutral |
| 6 | Arctic | White | Ice blue | Dark blue |
| 7 | Psychedelic | Rainbow cycling | Bright white | Dark neutral |

Palette 7 is unique: instead of fixed blob colors, it computes chrominance from a sine lookup of the field value plus a continuously cycling hue phase, producing rainbow-washed blobs that shift over time.

---

#### Knob 6 — Edge Glow
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the width of the edge glow band around the isosurface boundary. The upper 8 bits of the register (`edge_glow(9:2)`) define a symmetric zone above and below the threshold. Pixels within this zone are rendered with the palette's edge color instead of the interior color, creating a bright rim effect. At zero, there is no edge highlight — the blob transitions directly from interior to background. At high values, the edge zone widens, and more of the blob surface shows the edge color, creating a translucent halo effect around each blob.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Background** | Black | Tinted |
| **8 — Blob Shape** | Round | Tear |
| **9 — Video Fill** | Off | On |
| **10 — Freeze** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles provide independent binary controls. Background selects between pure black and a palette-tinted background color. Blob Shape elongates blobs vertically for a teardrop effect. Video Fill replaces blob interior color with the input video signal. Freeze halts all blob animation. Bypass routes input directly to output. These controls are orthogonal — any combination is valid.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the delayed input video and the rendered metaball output. At 0% (fully down), the output is pure input video. At 100% (fully up), the output is pure Lava synthesis. Intermediate positions blend the metaball animation over the input at variable opacity, useful for superimposing organic blob shapes over live footage as a visual overlay.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Lava processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises progress from basic blob observation through palette exploration to advanced video fill compositions. Because Lava is a synthesis program with animated state, allow 10–20 seconds after each parameter change for the blobs to cycle through representative configurations.

### Exercise 1: Classic Lava Lamp

<img src={lava_exercise1_result} alt="Classic Lava Lamp result"/>
*Classic Lava Lamp — simulated result across source images.*
**What You'll Create**: Recreate the classic lava lamp aesthetic with warm colors, slow motion, and organic merging.

1. **Classic Red palette**: Set Palette to position 0 (Classic Red). Deep red blobs with orange edges.
2. **Moderate blob size**: Set Blob Size to ~55%. Large enough to merge occasionally.
3. **Slow rise**: Set Rise Speed to ~30%. Leisurely convection motion.
4. **Find the threshold**: Set Threshold to ~45%. Adjust until blobs are clearly defined but merge when approaching each other.
5. **Add edge glow**: Set Edge Glow to ~60%. A warm orange rim appears around each blob.
6. **Tinted background**: Switch Background to Tinted. The dark warm background creates ambient atmosphere.
7. **Full mix**: Set Mix to 100%.
8. **Watch and wait**: Observe for 30 seconds. The four blobs rise, fall, merge, split — a digital lava lamp.

**Key concepts**: Metaball field produces smooth organic merging, threshold controls blob size and merge distance, edge glow highlights the isosurface boundary, prime-ratio DDS frequencies create non-repeating motion

---

### Exercise 2: Psychedelic Rainbow Blobs

<img src={lava_exercise2_result} alt="Psychedelic Rainbow Blobs result"/>
*Psychedelic Rainbow Blobs — simulated result across source images.*
**What You'll Create**: Explore the psychedelic palette with rainbow cycling and teardrop shapes.

1. **Psychedelic palette**: Set Palette to position 7 (maximum). Chrominance cycles through the hue wheel.
2. **Teardrop shape**: Switch Blob Shape to Tear. Blobs elongate vertically.
3. **Large blobs**: Set Blob Size to ~70%. Blobs nearly fill the screen and merge frequently.
4. **Low threshold**: Set Threshold to ~35%. Wide metaball surfaces with lots of merging.
5. **Maximum edge glow**: Set Edge Glow to ~90%. Bright halo edges.
6. **Medium speed**: Set Rise Speed to ~50%. Moderate convection.
7. **Black background**: Switch Background to Black. Maximum contrast.
8. **Observe the hue cycling**: The rainbow shifts over time as the hue phase accumulates — watch the color wheel rotate through each blob.

**Key concepts**: Psychedelic palette computes chrominance from sine(field + hue_phase), teardrop mode halves vertical distance for elongation, high blob size with low threshold creates amorphous merged forms

---

### Exercise 3: Video Fill Windows

<img src={lava_exercise3_result} alt="Video Fill Windows result"/>
*Video Fill Windows — simulated result across source images.*
**What You'll Create**: Use metaball shapes as animated windows into the input video signal.

1. **Enable video fill**: Switch Video Fill to On. Blob interiors now show input video.
2. **Cosmic Blue palette**: Set Palette to position 1. Blue edge glow frames the video windows.
3. **Moderate blob size**: Set Blob Size to ~50%. Manageable window sizes.
4. **Clear threshold**: Set Threshold to ~50%. Well-defined blob boundaries.
5. **Edge glow**: Set Edge Glow to ~70%. Cyan edges frame each video window.
6. **Tinted background**: Switch Background to Tinted to create a dark blue sea around the windows.
7. **Slow motion**: Set Rise Speed to ~25%. Windows drift gently.
8. **Partial mix**: Set Mix to ~80%. Slight input video bleed-through in background areas.

**Key concepts**: Video Fill replaces blob interior with input video while preserving edge glow, creating animated window shapes, palette edge colors frame the video content, tinted background creates atmospheric context

---


## Tips

- **Psychedelic palette evolves over time**: Palette 7 continuously cycles its hue phase — the rainbow pattern will never repeat at exactly the same point. Allow at least 60 seconds to observe the full chromatic evolution.
- **Freeze for composition**: Use Freeze to lock an interesting blob arrangement, then adjust Threshold, Edge Glow, or Palette to refine the static composition.
- **Video Fill creates organic mattes**: With Video Fill active, the metaball shapes become animated transparency windows into the input signal — useful for compositing applications.
- **Low Rise Speed for meditation**: Very slow rise speeds (5–15%) produce the most hypnotic, contemplative motion — closest to a real lava lamp.
- **Mix fader for overlay**: At partial mix, the lava blobs appear as semi-transparent overlays on the input video, creating ethereal atmospheric effects.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator that increments by a fixed step, used here to drive blob oscillation. |
| **Isosurface** | The contour line (or surface in 3D) where a scalar field equals a constant threshold value; in Lava, the boundary between blob interior and background. |
| **Leading-zero count** | A technique for approximating floating-point operations in integer hardware by counting the number of zero bits before the first set bit, used here for reciprocal distance estimation. |
| **Metaball** | A rendering primitive defined by a scalar field that falls off with distance from its center; multiple metaballs produce smooth organic merging at their isosurface boundaries. |
| **Phase accumulator** | A digital counter that increments by a configurable step and wraps at overflow, producing periodic oscillation for blob vertical/horizontal motion. |
| **Reciprocal approximation** | A method for computing 1/x without a hardware divider, using bit-shift operations guided by leading-zero count to produce a coarse but visually acceptable estimate. |
| **Scalar field** | A function that assigns a single numerical value to every point in space; in Lava, the sum of 1/distance² contributions from all active blobs. |
| **Sine LUT** | A lookup table storing quarter-wave sine values; the full sine function is reconstructed via quadrant logic, providing smooth oscillation for blob motion. |
| **Thermal convection** | The physical process where heated fluid rises and cooled fluid sinks, creating circulation patterns; the motion model that Lava's blob animation simulates. |

---
