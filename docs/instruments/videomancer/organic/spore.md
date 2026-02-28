---
draft: true
sidebar_position: 241
slug: /instruments/videomancer/spore
title: "Spore"
image: /img/instruments/videomancer/spore/spore_hero.png
description: "In nature, a spore is a reproductive cell released by fungi, mosses, and ferns — a microscopic package of potential life that drifts outward from its so..."
---

import spore_animation from '/img/instruments/videomancer/spore/spore_animation.gif';
import spore_control_panel from '/img/instruments/videomancer/spore/spore_control_panel.png';
import spore_exercise1_result from '/img/instruments/videomancer/spore/spore_exercise1_result.gif';
import spore_exercise2_result from '/img/instruments/videomancer/spore/spore_exercise2_result.gif';
import spore_exercise3_result from '/img/instruments/videomancer/spore/spore_exercise3_result.gif';
import spore_hero from '/img/instruments/videomancer/spore/spore_hero.png';

# Spore

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={spore_hero} alt="Spore hero image"/>
*Spore dispersing concentric particle rings from four source points, Manhattan-distance ripples dissolving into a noisy spore cloud overlay on the input video.*
<img src={spore_animation} alt="Spore animated output"/>
*Spore output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In nature, a spore is a reproductive cell released by fungi, mosses, and ferns — a microscopic package of potential life that drifts outward from its source, carried by wind, water, or animal contact. When a spore cloud is released, it expands in concentric waves, each wave representing a generation of particles at the same distance from the origin. Over time, the cloud thins as particles spread across a wider area, eventually dissolving into individual scattered specks.

Spore simulates this dispersal process using Manhattan distance — the taxicab metric where distance is measured as |Δx| + |Δy| rather than the Euclidean straight-line formula. Two or four source points act as emission sites, each projecting expanding concentric rings computed at pixel rate. A per-pixel LFSR noise gate determines whether each ring pixel survives or is filtered out, simulating the stochastic nature of particle dispersal. The ring radius expands frame by frame via a DDS accumulator, creating the illusion of outward-propagating wavefronts. Where a spore "hit" is detected, the program additively brightens the source video, overlaying the ring pattern as a luminous structure on top of the original image.

The Manhattan distance metric gives the rings a distinctive diamond-shaped geometry rather than the circular contours of Euclidean distance. At close range the diamonds are clearly visible; at greater distances the ring structure dissolves into a fine particle spray, modulated by the LFSR's pseudo-random bit sequence. Adjustable ring width, density, brightness, and speed controls provide precise sculpting of the visual result. Optional source point drift adds slow spatial modulation, making the emission sites wander across the frame.

---

## Background

### Manhattan Distance and Diamond Rings

The Manhattan distance (also called taxicab distance or city-block distance) between two points is the sum of the absolute differences of their coordinates: d = |x₁ − x₂| + |y₁ − y₂|. Named after the grid layout of Manhattan streets, where you cannot cut diagonally through buildings, this metric produces diamond-shaped isodistance contours rather than the circles of Euclidean geometry. In hardware, Manhattan distance is dramatically cheaper to compute than Euclidean distance — it requires only two absolute differences and an addition, with no multiplication or square root. Spore exploits this economy to compute distances from every pixel to every source point at full pixel rate.

### Expanding Ring Wavefronts

Spore's rings work by maintaining a single frame-counter-driven radius value that increments at a rate controlled by the Speed parameter. Each pixel's minimum Manhattan distance to the nearest source is compared against this expanding radius using modular arithmetic: the distance is folded into a ring period, and a hit is detected when the folded distance falls within the ring width band. As the radius counter advances, the ring pattern appears to expand outward from each source point, creating concentric wavefronts. Because the ring period is finite, the pattern repeats — multiple concentric rings are visible simultaneously, each separated by one period.

### LFSR Density Gating

A Linear Feedback Shift Register (LFSR) generates a repeating pseudo-random bit sequence at pixel rate. For each pixel that passes the ring geometry test, the LFSR output is compared against the Density threshold: if the random value exceeds the threshold, the pixel is filtered out and no spore is drawn. This creates a stochastic particle texture within the ring bands — at high density, the rings appear solid; at low density, they dissolve into scattered specks. The LFSR's deterministic but pseudo-random sequence ensures that the noise pattern is stable from frame to frame (given the same starting seed), preventing the distracting flicker that would result from true random noise.

### Multi-Source Emission and Spatial Interference

When multiple source points are active, each pixel is assigned to the nearest source (minimum Manhattan distance). The ring pattern radiates independently from each emission site, but the boundaries where two sources meet form Voronoi-like edges — the Manhattan-metric Voronoi diagram, which consists of straight-line segments rather than the curved boundaries of the Euclidean Voronoi. These boundaries create additional visual structure where the ring patterns from adjacent sources interlock and interfere.

### Additive Brightness Overlay

Rather than replacing the source video, Spore adds brightness to it — each spore pixel increases the luma of the underlying video. This additive compositing preserves the original image as a backdrop while the ring structure appears as a luminous overlay. The brightness control sets the intensity of the overlay, and the optional color tint mode shifts the chroma channels to give the spore particles a subtle green-magenta coloration. The wet/dry mix fader provides final control over how much of the processed signal blends with the original.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Clock 0: Register Decode + Position Counters ──────────────
│   ├─ spread, speed, width, density, brightness, mix_ctrl
│   ├─ toggles: four_src, color_mode, drift_en, bypass
│   ├─ frame_count++, ring_radius += f(speed)
│   └─ source positions = center ± spread ± drift_offset
│
├── Clock 1: Input Register ────────────────────────────────────
│   └─ Latch Y, U, V from data_in
│
├── Clock 2: Manhattan Distance ────────────────────────────────
│   ├─ dist_n = |px − src_n_x| + |py − src_n_y|  for n ∈ {0..3}
│   ├─ min01 = min(dist0, dist1)
│   ├─ min23 = min(dist2, dist3)  [if 4 sources]
│   └─ min_all = min(min01, min23) or min01 [if 2 sources]
│
├── Clock 3: Ring Test + LFSR Density Gate ─────────────────────
│   ├─ ring_period = f(width)     [127, 255, 511, or 1023]
│   ├─ dist_mod = (min_dist + ring_radius) AND period_mask
│   ├─ hit = (dist_mod ≤ ring_w) OR (dist_mod ≥ period − ring_w)
│   └─ hit &= (lfsr < density)   [particle survives noise gate]
│
├── Clock 4: Brightness Compose + Color Overlay ────────────────
│   ├─ hit=1: Y = clamp(Y_in + brightness)
│   │         color=0: U,V = passthrough (white overlay)
│   │         color=1: U,V = tinted (chroma shift)
│   └─ hit=0: Y,U,V = passthrough (source unchanged)
│
├── Clocks 5–8: Interpolator (wet/dry Mix, 4 clocks) ──────────
│   └─ lerp(input_delayed, composited, mix_amount)
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ bypass=1 → pass input; bypass=0 → interpolated output
```

The key architectural feature is the parallel minimum-distance computation across all source points in a single clock cycle. By computing Manhattan distances to all four sources simultaneously and reducing to the minimum in the same pipeline stage, the design avoids the multi-cycle sequential search that would be required for more sources. The ring test uses modular arithmetic with power-of-two period masks, which means the period snaps between 128, 256, 512, and 1024 rather than varying continuously — the Width knob selects among these quantized periods and simultaneously controls the ring band thickness within the selected period.

---

## Parameter Reference

<img src={spore_control_panel} alt="Videomancer front panel with Spore loaded"/>
*Videomancer's front panel with Spore active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sources
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial separation between source emission points. At 0% the sources collapse onto the screen center, producing a single expanding ring set. As Spread increases, the sources migrate toward the corners: source 0 moves upper-left, source 1 upper-right, source 2 lower-left, source 3 lower-right (sources 2 and 3 are only active when 4 Sources mode is enabled). At maximum spread, the sources are widely separated and the Manhattan-distance diamonds from each source fill distinct quadrants of the screen with minimal overlap.

---

#### Knob 2 — Emit Rat
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the ring expansion speed — how quickly the ring radius counter increments frame by frame. The VHDL implementation uses a speed divider that maps the 10-bit register to frame-skip intervals: high values update the radius every frame (fast expansion), low values update every 32 frames (very slow expansion). At maximum speed, rings propagate outward rapidly and the wavefront reaches the screen edge in a few seconds. At minimum speed, the rings creep outward almost imperceptibly, creating a slow-building meditative pattern.

---

#### Knob 3 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the ring band width and period. The Width parameter controls two linked quantities simultaneously: the ring period (how far apart successive ring bands are, selected from 128, 256, 512, or 1024 pixels) and the ring width within that period (how thick each band is). Higher values produce wider, more widely spaced rings; lower values produce tighter, narrower rings with more concentric bands visible at once. The minimum ring width is clamped at 2 pixels to prevent the rings from becoming invisible.

---

#### Knob 4 — Spore Sz
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the LFSR density gate threshold. At maximum (100%), all ring pixels pass the noise gate and the rings appear as solid bands. As density decreases, more pixels are filtered out by the pseudo-random noise, and the rings dissolve into a scattered particle texture. At very low density, only occasional specks survive within the ring zones, simulating the sparse outer edge of a dispersing spore cloud. The LFSR pattern is deterministic, so the speckle texture is stable from frame to frame.

---

#### Knob 5 — Fade Dst
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the spore overlay brightness — the amount of luminance added to the source video where spore hits are detected. At 0% no visible overlay appears. At maximum, spore hits saturate to white (Y=1023). Moderate values create a translucent, glowing ring overlay that reveals the source video beneath. The brightness is applied additively, so dark source regions show the rings more prominently than bright regions.

---

#### Knob 6 — Tint
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the wet/dry crossfade via the effect intensity blend. This register feeds the interpolator that mixes between the source video and the composited spore overlay. At 100% the full spore effect is applied; at 0% the source passes through unmodified. This provides a final master intensity control independent of the Brightness knob.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Burst | Stream |
| **8 — Spore** | Round | Oval |
| **9 — React** | Off | Luma |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The three active toggles control independent binary options: source count (2 vs 4 emission points), color mode (white vs tinted overlay), and source drift (static vs wandering positions). Each toggle modifies a different pipeline stage. The Bypass toggle routes the input directly to the output, bypassing all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the final wet/dry mix via the interpolator. At 100%, the full spore composite replaces the delayed input. At 0%, the original input passes through unmodified. Intermediate values blend the spore overlay with the source at proportional intensity. This fader provides the primary mixing control and interacts multiplicatively with the Brightness knob's additive overlay.

---

## Guided Exercises

These exercises progress from understanding the basic ring geometry through density and color sculpting to dynamic multi-source compositions with drift. Each builds on the spatial interference patterns created by Manhattan-distance ring propagation.

### Exercise 1: Two-Source Diamond Rings

<img src={spore_exercise1_result} alt="Two-Source Diamond Rings result"/>
*Two-Source Diamond Rings — simulated result across source images.*
**Objective**: Understand the Manhattan-distance ring geometry and how Speed and Width interact to control the expanding wavefront pattern.

1. **Set 2 sources**: Ensure the Count toggle is set to 2 sources (default).
2. **Maximum spread**: Set Spread to ~80% so the two sources are well separated.
3. **Medium speed**: Set Speed to ~50% for a moderate expansion rate. Diamond-shaped rings should expand visibly from two points on either side of center.
4. **Tighten rings**: Reduce Width to ~20% to see many narrow concentric rings. Note the ring period snaps between quantised values.
5. **Full density**: Set Density to 100% so rings appear as solid bands. Observe the clean diamond geometry characteristic of Manhattan distance.
6. **Reduce density**: Slowly lower Density to ~40%. Watch the solid rings dissolve into stochastic speckle within the ring zones.
7. **Adjust brightness**: Set Brightness to ~60% for a translucent overlay. The source video should be clearly visible beneath the ring pattern.

**Key concepts**: Manhattan distance produces diamond-shaped contours, ring period is quantised to powers of two, LFSR density gating controls particle visibility, additive overlay preserves source video

---

### Exercise 2: Four-Source Interference

<img src={spore_exercise2_result} alt="Four-Source Interference result"/>
*Four-Source Interference — simulated result across source images.*
**Objective**: Activate all four source points and explore the spatial interference patterns created by overlapping Manhattan-distance ring fields.

1. **Enable 4 sources**: Toggle Count to 4 sources. Two additional emission points appear in the lower half of the frame.
2. **Moderate spread**: Set Spread to ~50%. The four sources form a rectangle around the screen center.
3. **Wide rings**: Set Width to ~70% for broad ring bands. The four ring fields overlap, creating complex interference at the boundaries where two sources have equal distance.
4. **Observe boundaries**: The lines where two source distances are equal form the Manhattan Voronoi diagram — straight edges that divide the screen into diamond-shaped regions, each dominated by its nearest source.
5. **Enable color tint**: Toggle Color to tint mode. The spore particles gain a subtle color cast, making the overlay pattern more visually distinct from the source.
6. **Enable drift**: Toggle Drift On. The four sources begin wandering, causing the Voronoi boundaries and interference patterns to evolve slowly.

**Key concepts**: Four sources create Manhattan Voronoi tessellation, ring interference at source boundaries produces complex moiré, drift adds temporal evolution to the spatial pattern

---

### Exercise 3: Dissolving Spore Cloud

<img src={spore_exercise3_result} alt="Dissolving Spore Cloud result"/>
*Dissolving Spore Cloud — simulated result across source images.*
**Objective**: Create a sparse, dissolving particle atmosphere by combining low density with high brightness, simulating a drifting spore cloud.

1. **Minimal density**: Set Density to ~15%. Only scattered particles survive the LFSR gate, producing a sparse, dust-like overlay.
2. **Slow speed**: Set Speed to ~20%. The rings expand very slowly, creating a gradual, hypnotic propagation.
3. **Maximum brightness**: Set Brightness to ~90%. The surviving particles glow brightly against the dark source, creating pinpoint highlights.
4. **Wide spread**: Set Spread to ~70% with 2 sources. The two distant emission points send sparse particle waves across the frame.
5. **Narrow rings**: Set Width to ~10%. The combination of narrow rings and low density creates a fine, almost invisible particle spray that occasionally catches the eye as a bright speck drifts past.
6. **Enable drift**: Toggle Drift On for subtle source movement that prevents the pattern from locking into a static grid.
7. **Reduce mix**: Set Mix to ~50% to let the dark source footage dominate, with the spore particles appearing as ethereal floating specks.

**Key concepts**: Low density + high brightness creates individual particle highlights, slow speed produces meditative expansion, narrow width reduces ring visibility to sparse specks, Mix sets overall overlay intensity

---


## Tips

- **Manhattan geometry is the signature**: The diamond-shaped ring contours are the distinctive visual hallmark of Spore. Embrace the angular aesthetic rather than expecting circular rings.
- **Density for atmosphere**: Low density (10–25%) creates a dusty, atmospheric particle texture that works beautifully over dark footage. High density (80–100%) produces solid geometric bands suited to graphic compositions.
- **Speed and drift work together**: Slow speed with drift enabled creates a meditation — rings creep outward while the sources wander, producing constantly shifting geometry over minutes rather than seconds.
- **Brightness is additive**: Unlike multiplicative overlays, Spore adds brightness to the source. This means it works best over mid-to-dark images. On already-bright footage, the overlay saturates at white and loses definition.
- **Ring width controls visual density**: Narrow rings with high LFSR density create fine lattice textures. Wide rings with low density create broad cloudy bands of scattered particles.
- **4 sources for complexity**: The Voronoi boundaries between four sources add geometric structure that isn't present with just two sources. The boundaries create additional straight-line features that divide the diamond rings.
- **Tint for color**: The default white overlay is clean but can get lost on bright source material. Switching to tint mode gives the spore particles a subtle color identity that stands out against the source chroma.
- **Feedback loops**: Routing the output back to the input causes the additive overlay to build up over frames, creating self-reinforcing ring structures that bloom outward from the sources.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Compositing** | A blending technique where the overlay brightness is added to the source, producing luminous highlights that cannot darken the original image. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator and using the result to index a lookup table. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **Manhattan Distance** | The sum of absolute differences |Δx| + |Δy|, producing diamond-shaped isodistance contours. |
| **Modular Arithmetic** | Distance folded into a fixed period using a bitmask AND operation, creating repeating ring bands. |
| **Ring Period** | The distance between successive ring band centers, quantised to powers of two (128, 256, 512, 1024). |
| **Voronoi Diagram** | A partitioning of space into regions, each containing all points nearest to a given source; in Manhattan metric these boundaries are straight-line segments. |
| **Wet/Dry Mix** | The interpolation factor between the processed (wet) and unprocessed (dry) signal. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
