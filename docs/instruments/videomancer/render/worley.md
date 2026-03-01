---
draft: true
sidebar_position: 287
slug: /instruments/videomancer/worley
title: "Worley"
image: /img/instruments/videomancer/worley/worley_hero.png
description: "In 1996 Steven Worley published a paper describing a procedural texture function based on distances to randomly distributed feature points."
---

import worley_animation from '/img/instruments/videomancer/worley/worley_animation.gif';
import worley_control_panel from '/img/instruments/videomancer/worley/worley_control_panel.png';
import worley_exercise1_result from '/img/instruments/videomancer/worley/worley_exercise1_result.gif';
import worley_exercise2_result from '/img/instruments/videomancer/worley/worley_exercise2_result.gif';
import worley_exercise3_result from '/img/instruments/videomancer/worley/worley_exercise3_result.gif';
import worley_hero from '/img/instruments/videomancer/worley/worley_hero.png';

# Worley

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={worley_hero} alt="Worley hero image"/>
*Worley generating animated Voronoi cellular textures with Manhattan distance and the Thermal palette, producing volcanic heat-map terrain.*
<img src={worley_animation} alt="Worley animated output"/>
*Worley output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1996 Steven Worley published a paper describing a procedural texture function based on distances to randomly distributed feature points. The technique — now widely known as cellular noise or Voronoi noise — produces organic, cell-like patterns that resemble biological tissue, cracked earth, stone surfaces, and stained glass. Worley synthesizes these patterns in real time on the FPGA by distributing pseudo-random feature points on a regular grid, computing distances from every pixel to its nine nearest grid neighbours, and sorting the two shortest distances to produce F1 (nearest) and F2 (second nearest) outputs.

The visual character of Voronoi noise depends on which distances are displayed and how they are measured. F1 produces bright cell edges around dark centres — the classic cellular look. F2 produces a softer, more complex pattern. F2−F1 highlights only the ridges between cells, producing vein-like or web-like structures. The Colored mode assigns a unique hue to each cell based on its grid coordinates, creating stained-glass mosaics. Switching the distance metric between Manhattan and Chebyshev changes the cell geometry from diamond-shaped to square.

Animation is driven by a time counter that modulates the hash function's seed, causing feature points to drift smoothly within their cells. A separate scroll offset DDS slides the entire cellular field across the screen. Combined with four color palettes (Organic, Stone, Neon, Thermal), Worley produces a wide range of living, evolving textures entirely from arithmetic — no frame buffers, no stored images.

---

## Background

### Voronoi Diagrams and Feature Points

A Voronoi diagram partitions a plane into regions, each containing all points closer to one particular seed than to any other. In Worley's formulation, seed points are placed on a regular grid and then displaced by a pseudo-random jitter. The grid ensures that each pixel needs to check only the 3×3 neighbourhood of cells (9 candidates) to find the nearest feature point — a bounded, constant-time operation suitable for hardware.

### The Cell Hash Function

Worley's FPGA implementation uses a compact integer hash to generate deterministic pseudo-random positions. The hash takes cell coordinates (cx, cy) and a time value, combines them via prime multiplications and XOR, then applies three avalanche passes (shift-right-7 XOR, shift-left-3 XOR, shift-right-5 XOR). The result is a 16-bit value split into X and Y jitter offsets. This is not cryptographic randomness — it is a fast, deterministic scramble that produces visually convincing spatial disorder.

### Distance Metrics

The distance between a pixel and a feature point can be measured in several ways. Manhattan distance (|dx| + |dy|) produces diamond-shaped iso-distance contours, giving cells an angular, crystalline appearance. Chebyshev distance (max(|dx|, |dy|)) produces square contours, creating a tiled, boxy look. Euclidean distance (√(dx² + dy²)) would produce circles, but is expensive in hardware. The Manhattan and Chebyshev options provide distinct visual characters without requiring multipliers.

### Palettes and Coloring

The four palette modes map the computed luma value to chroma offsets. Organic mixes green-brown tones reminiscent of moss and earth. Stone produces desaturated warm grays like sandstone. Neon creates vivid cyan-magenta gradients. Thermal maps dark-to-bright values through blue-to-red, imitating infrared camera displays. In Colored Voronoi mode, each cell gets a unique color derived from hashing its cell ID, bypassing the palettes entirely.

### Video Modulation

When Video Mod is enabled, the cellular noise pattern modulates the input video's luminance instead of generating a standalone texture. Bright cellular regions lighten the source image, creating a living texture overlay that follows the Voronoi structure while preserving the original video content.


---

## Signal Flow

```
┌─────────────────────────────────────────────────────┐
│  Timing Generator                                   │
│  ├─ h_count, v_count (pixel counters)               │
│  ├─ DDS scroll offsets (x_offset, y_offset)         │
│  └─ time_phase (animation counter)                  │
└───────────────┬─────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────┐
│  Stage 1: Grid Cell + Hash                          │
│  ├─ px = h + scroll_x, py = v + scroll_y            │
│  ├─ cell_x = px >> cell_shift                       │
│  ├─ 9 neighbours: cell_hash(ncx, ncy, time)        │
│  └─ jitter → feature point positions                │
└───────────────┬─────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────┐
│  Stage 2: Distance + F1/F2 Sort                     │
│  ├─ 9× distance (Manhattan or Chebyshev)            │
│  ├─ F1 = nearest, F2 = second nearest               │
│  └─ F1_id = cell index of nearest                   │
└───────────────┬─────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────┐
│  Stage 3: Output Mode + Contrast                    │
│  ├─ F1 / F2 / F2−F1 / Colored                      │
│  ├─ noise × contrast >> 9                           │
│  └─ + brightness offset                             │
└───────────────┬─────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────┐
│  Stage 4: Palette + Video Mod                       │
│  ├─ Palette color mapping (Organic/Stone/Neon/Thermal) │
│  ├─ Colored Voronoi: cell_hash → U,V               │
│  ├─ Video Mod: Y += noise/2, keep source U,V       │
│  └─ Final Y, U, V                                  │
└───────────────┬─────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────┐
│  Mix (3× interpolator_u) + Bypass                   │
│  └─ lerp(dry, wet, mix) → Output                   │
└─────────────────────────────────────────────────────┘
```

The pipeline is organized so that the computationally intensive neighbourhood search and distance sorting happen in the first two clock stages, while palette coloring and compositing occupy the later stages. The cell_hash function is purely combinational — it runs 9 times per pixel (once per neighbour) in a single clock cycle. The F1/F2 tracking maintains running minimums as each of the 9 distances is computed, so the sort is complete at the end of the loop.

---

## Parameter Reference

<img src={worley_control_panel} alt="Videomancer front panel with Worley loaded"/>
*Videomancer's front panel with Worley active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Animation Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the speed of animation. The time counter increments by this value each frame, modulating the hash function seed and causing feature points to drift within their cells. At 0% the pattern is static. Higher values increase drift speed, creating a flowing, organic evolution of the cellular texture.

---

#### Knob 2 — Cell Scale
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 2 |

Selects the grid cell size via a 4-step selector. The steps map to cell shift values of 5 (32px), 6 (64px), 6 (64px), and 7 (128px), controlling the spatial scale of the Voronoi cells. Small cells produce fine, densely packed cellular textures; large cells create broad, sweeping regions with fewer, larger features.

---

#### Knob 3 — Jitter Amount
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the amount of pseudo-random displacement applied to each feature point within its grid cell. At 0% feature points sit exactly on grid intersections, producing a perfectly regular tiled pattern. At 100% feature points are maximally displaced, creating irregular, organic cell boundaries. Mid-range values produce a visually appealing balance between order and randomness.

---

#### Knob 4 — Scroll Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the scroll speed of the entire cellular field. A DDS accumulator adds this value to the X and Y pixel offsets each frame, sliding the pattern across the screen. The Y scroll runs at half the rate of X for a diagonal drift. At 0% the field is stationary (animation still operates via feature point drift).

---

#### Knob 5 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scales the contrast of the distance-to-luminance mapping. The noise value is multiplied by contrast and right-shifted by 9, giving a gain range from 0× to approximately 2×. Low contrast produces a washed-out, low-dynamic-range texture; high contrast pushes cell boundaries toward full black-and-white, emphasizing the cellular structure.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Adds a brightness offset to the computed luminance. The value is halved and added to the contrast-scaled noise. Higher brightness lifts the overall level, preventing dark cells from clipping to black. Lower brightness allows the cellular pattern to occupy only the shadow range.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Output Mode** | F1 | F2 |
| **8 — Distance** | Manhattan | Chebyshev |
| **9 — Palette** | Organic | Stone |
| **10 — Video Mod** | Off | On |
| **11 — Bypass** | Off | On |

Toggle 7 selects among four output modes using two bits (F1, F2, F2−F1, Colored). Toggle 8 selects the distance metric (Manhattan or Chebyshev). Toggle 9 selects among four color palettes using two bits. Toggle 10 enables Video Modulation mode, which overlays the cellular pattern on the input video. Toggle 11 bypasses all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input signal and the synthesized cellular texture. At 0% the output is the unprocessed input. At 100% the output is the full Worley synthesis. Intermediate positions blend the cellular texture with the source at varying opacity.

---

## Guided Exercises

These exercises progress from static cellular patterns to animated, content-reactive textures, exploring how distance metrics, output modes, and palettes combine to produce diverse visual effects.

### Exercise 1: Classic Voronoi Cells

<img src={worley_exercise1_result} alt="Classic Voronoi Cells result"/>
*Classic Voronoi Cells — simulated result across source images.*
**Objective**: Create a static cellular texture and understand how F1/F2 outputs differ.

1. **Static F1**: Set Animation Speed to 0%. Observe the F1 pattern — dark cell centres surrounded by bright edges.
2. **Switch to F2**: Change Output Mode to F2. Notice the more complex, overlapping distance field.
3. **F2−F1 ridges**: Switch to F2−F1. Only the cell boundaries remain as bright lines on a dark background.
4. **Colored Voronoi**: Switch to Colored mode. Each cell gets a unique hash-derived color.
5. **Metric comparison**: Toggle Distance between Manhattan and Chebyshev. Diamond cells versus square cells.

**Key concepts**: F1 and F2 are the first and second nearest distances, F2−F1 isolates cell boundaries, distance metric changes cell geometry

---

### Exercise 2: Animated Lava Flow

<img src={worley_exercise2_result} alt="Animated Lava Flow result"/>
*Animated Lava Flow — simulated result across source images.*
**Objective**: Create a slowly evolving thermal texture using animation, scroll, and the Thermal palette.

1. **Set Thermal palette**: Select Palette = Thermal for blue-to-red heat-map coloring.
2. **Enable animation**: Set Animation Speed to ~25%. Feature points begin drifting, creating flowing cell boundaries.
3. **Add scroll**: Set Scroll Speed to ~15%. The entire field drifts diagonally across the screen.
4. **Increase contrast**: Raise Contrast to ~75%. Cell boundary ridges become more pronounced.
5. **Try F2−F1**: Switch Output Mode to F2−F1 for glowing vein-like channels between cells.
6. **Scale up**: Switch Cell Scale to X-Large. Fewer, larger volcanic regions slowly flow and merge.

**Key concepts**: Animation modulates hash seed causing point drift, scroll uses DDS accumulators, Thermal palette creates heat-map aesthetics

---

### Exercise 3: Video Overlay Texture

<img src={worley_exercise3_result} alt="Video Overlay Texture result"/>
*Video Overlay Texture — simulated result across source images.*
**Objective**: Use Video Mod to overlay cellular noise onto live source footage.

1. **Enable Video Mod**: Toggle Video Mod On. The cellular noise now brightens the source video's luminance.
2. **Set small cells**: Choose Cell Scale = Small for a fine, detailed overlay.
3. **Animate gently**: Set Animation Speed to ~10% for subtle motion.
4. **Adjust brightness**: Lower Brightness so the overlay doesn't blow out highlights.
5. **Try Neon palette**: Even though Video Mod preserves source chroma, the underlying noise structure is visible as luminance texture.
6. **Blend with Mix**: Reduce Mix to ~60% for a subtler overlay effect.

**Key concepts**: Video Mod adds half the noise value to source luma, cellular noise creates living texture on real video

---


## Tips

- **F2−F1 for veins**: The F2−F1 output mode isolates cell boundaries as bright ridges on black — perfect for blood vessel, lightning, or crack textures.
- **Manhattan for crystals, Chebyshev for tiles**: The distance metric fundamentally changes the visual character. Manhattan creates diamond-faceted cells; Chebyshev creates boxy, tile-like cells.
- **Jitter is the key to organic**: Zero jitter produces a perfectly regular grid. Maximum jitter creates fully organic, irregular cells. The sweet spot around 70–80% looks most natural.
- **Large cells + slow animation**: Big cells with gentle animation produce a meditative, slowly evolving landscape. Small cells with fast animation produce frantic, buzzing textures.
- **Scroll for continuous backgrounds**: Use Scroll Speed without Animation Speed for a continuously scrolling tile pattern — useful as a moving background or texture source.
- **Video Mod for texture overlay**: Enabling Video Mod turns Worley from a standalone synthesizer into a texture overlay processor that adds cellular structure to live footage.
- **Contrast and brightness work together**: High contrast without enough brightness can clip cell interiors to black. Balance both for the desired dynamic range.

---

## Glossary

| Term | Definition |
|------|------------|
| **Cell Hash** | A deterministic pseudo-random function that converts grid coordinates into jitter offsets, using prime multiplication and XOR avalanche mixing. |
| **Cellular Noise** | A procedural texture function based on distances to randomly placed feature points, producing organic cell-like patterns. |
| **Chebyshev Distance** | A distance metric computed as max(|dx|, |dy|), producing square-shaped iso-distance contours. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator and using the result to index a lookup table. |
| **F1** | The distance from a pixel to the nearest feature point in the Voronoi diagram. |
| **F2** | The distance from a pixel to the second-nearest feature point. |
| **Feature Point** | A seed location in the Voronoi diagram; pixels are colored based on their distance to these points. |
| **Jitter** | Random displacement of feature points from their grid positions, breaking regularity and creating organic cell shapes. |
| **Manhattan Distance** | A distance metric computed as |dx| + |dy|, producing diamond-shaped iso-distance contours. |
| **Voronoi Diagram** | A partition of a plane into regions, each containing all points closer to a particular seed than to any other seed. |
| **Worley Noise** | Another name for cellular noise, after Steven Worley who published the technique in 1996. |
