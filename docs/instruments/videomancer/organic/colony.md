---
draft: true
sidebar_position: 56
slug: /instruments/videomancer/colony
title: "Colony"
image: /img/instruments/videomancer/colony/colony_hero.png
description: "Colony simulates the territorial expansion of bacterial cultures on a nutrient agar plate."
---

import colony_hero from '/img/instruments/videomancer/colony/colony_hero.png';
import colony_animation from '/img/instruments/videomancer/colony/colony_animation.gif';
import colony_control_panel from '/img/instruments/videomancer/colony/colony_control_panel.png';
import colony_exercise1_result from '/img/instruments/videomancer/colony/colony_exercise1_result.gif';
import colony_exercise2_result from '/img/instruments/videomancer/colony/colony_exercise2_result.gif';
import colony_exercise3_result from '/img/instruments/videomancer/colony/colony_exercise3_result.gif';

# Colony

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={colony_hero} alt="Colony hero image"/>
*Four bacterial colonies expanding from quadrant centers, their LFSR-noised growth fronts colliding at bright mutual exclusion boundaries that trace a living Voronoi tessellation.*
<img src={colony_animation} alt="Colony animated output"/>
*Colony output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Colony simulates the territorial expansion of bacterial cultures on a nutrient agar plate. Four seed points — fixed at the quadrant centers of the frame — grow outward via DDS-based radius accumulators. Each pixel is assigned to its nearest colony by Manhattan distance, and the regions where two colonies nearly meet are detected and highlighted as bright boundary lines. The result is a dynamic Voronoi-like tessellation whose cell walls push outward in real time, subdividing the screen into colored territories that compete for space.

The name *Colony* is borrowed directly from microbiology, where a colony is a visible cluster of microorganisms that has grown from a single progenitor on a solid medium. In the program's domain, each colony is a geometric expansion zone whose radius increases frame by frame according to the Growth Speed parameter. The LFSR adds irregularity to the growth frontier — the edge of each colony wobbles and fractures rather than expanding as a perfect circle, mimicking the stochastic nutrient diffusion and cell division timing that produce the irregular perimeters of real bacterial colonies.

The number of active colonies, the width of the boundary exclusion zone, the color saturation, and the growth pattern (monotonic versus pulsing) are all continuously adjustable. At low growth speeds the tessellation emerges slowly and deliberately; at high speeds the colonies race across the frame, their boundaries snapping into position within seconds. The Reset toggle clears all accumulated growth, allowing the expansion to begin fresh — useful for synchronized performances or for studying the early stages of territorial partitioning.

---

## Background

### Cellular Automata and Growth Simulation

The study of self-organizing spatial patterns has a long history in mathematics and biology. John von Neumann's cellular automata (1940s) demonstrated that simple local rules could produce complex global behavior — cells updating their state based on their neighbors could generate growth, replication, and even universal computation. Colony's growth model is simpler than a full cellular automaton: each colony expands uniformly from a fixed center point, with the only interaction being mutual exclusion at the boundaries. But the visual result — an evolving tessellation of competing territories — echoes the emergent structure of cellular automata like Conway's Game of Life, where local interactions produce large-scale spatial organization without any global coordinator.

### Voronoi Diagrams

A Voronoi diagram partitions a plane into cells, one per seed point, such that every point in a cell is closer to its seed than to any other. Colony's nearest-colony assignment is exactly a Voronoi decomposition under the Manhattan (L1) metric rather than the usual Euclidean (L2) metric. Under L1, Voronoi cells have polygonal boundaries with edges aligned to the 45° diagonals rather than the arbitrary angles of Euclidean Voronoi cells. The boundary detection stage identifies pixels where two cells nearly tie — the second-nearest colony distance minus the nearest colony distance falls below a threshold — and highlights them, making the Voronoi edges visible as bright lines. Adjusting the Border Width parameter controls how thick these edges appear, from hairline Voronoi walls to broad exclusion corridors.

### Bacterial Colony Morphology

When bacteria are streaked onto agar and incubated, each viable cell multiplies into a visible colony whose shape depends on species, nutrient availability, agar stiffness, and temperature. Some species produce smooth circular colonies (regular expansion on homogeneous media), others produce fractal, dendritic, or lobate patterns (nutrient-limited diffusion, chemotaxis, or surface motility). Colony's LFSR-modulated edges approximate the stochastic irregularity seen in real growth fronts — the edge noise parameter controls how much the frontier deviates from a perfect circle, ranging from clean geometric expansion (low noise) to rough, lichen-like perimeters (high noise).

### DDS Accumulators for Animation

Direct Digital Synthesis drives the colony radii. Each colony maintains a 16-bit phase accumulator that increments by the Growth Speed value on every vertical sync pulse. The upper 12 bits of the accumulator represent the effective radius. In monotonic mode, the radius grows until it saturates at maximum. In pulse mode, the accumulator wraps freely and the MSB is used to fold the radius into a triangle wave — colonies expand and contract rhythmically, producing concentric ring-like patterns as the growth frontier advances and retreats. The DDS approach guarantees glitch-free, phase-continuous evolution at any growth rate, from glacial creep to rapid oscillation.

### Manhattan Distance in Hardware

Euclidean distance requires squaring and square roots — expensive operations in FPGA logic. Manhattan distance (|Δx| + |Δy|) replaces these with absolute differences and addition, costing only a few LUTs per colony. The trade-off is geometric: Manhattan iso-distance contours are diamonds (rotated squares) rather than circles. This gives Colony's territorial boundaries a characteristic angular quality — cell walls tend to align with the 0° and 90° axes rather than forming smooth curves. The visual effect is distinctive and deliberately retained as part of Colony's aesthetic identity.


---

## Signal Flow

```
Video Input (YUV 4:4:4)
│
├── Register Decode ────────────────────────────────────────────
│   ├─ growth_rate  = registers_in(0)
│   ├─ colony_count = registers_in(1)  →  s_active_cols 1–4
│   ├─ boundary_w   = registers_in(2)  →  s_bnd_thresh
│   ├─ color_int    = registers_in(3)
│   ├─ source_blend = registers_in(4)
│   ├─ edge_noise   = registers_in(5)  →  s_noise_shift
│   └─ toggles: mode_pulse, color_mode, animate, reset, bypass
│       mix_amount  = registers_in(7)
│
├── Timing Generator ───────────────────────────────────────────
│   └─ video_timing_generator → s_h_count, s_v_count
│
├── LFSR Noise ─────────────────────────────────────────────────
│   └─ lfsr16 (seed 0xACE1) → s_lfsr_noise (8-bit)
│
├── Colony Animation (per vsync) ───────────────────────────────
│   ├─ s_colony_radii[0..3] += growth_rate  (DDS accumulator)
│   ├─ Monotonic: clamp at 0xFF00
│   └─ Pulse: free-running, MSB folds into triangle
│
├── Clock 1: Manhattan Distance ────────────────────────────────
│   └─ s_dist[i] = |h_count − cx[i]| + |v_count − cy[i]|  ×4
│
├── Clock 2: Min-Find ─────────────────────────────────────────
│   ├─ s_nearest_idx, s_nearest_dist  (closest colony)
│   └─ s_second_dist                  (runner-up distance)
│
├── Clock 3: Boundary + Color ──────────────────────────────────
│   ├─ Inside test: nearest_dist < colony_radius + noise
│   ├─ Boundary test: (second_dist − nearest_dist) < threshold
│   ├─ Colony color: UV offsets from C_COLONY_COLORS table
│   └─ Mono/Color mode select
│
├── Clock 4: Final Composite ───────────────────────────────────
│   ├─ Boundary → bright white (Y + 256, clamped)
│   ├─ Inside   → colony color (tinted Y, colored UV)
│   └─ Outside  → pass source YUV
│
├── Clocks 5–8: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(dry, wet, Mix)  ×3 channels  (4 clocks)
│
├── Sync Delay Pipeline (8 clocks) ─────────────────────────────
│   └─ hsync, vsync, field, Y, U, V delayed to match
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select delayed source or processed signal
```

The computational core of Colony is the four-way Manhattan distance computation in Clock 1 and the min-find tree in Clock 2. Because Manhattan distance uses only absolute difference and addition, all four distances are computed in a single clock cycle with minimal LUT cost. The min-find stage performs a linear scan of the four distances, tracking both the nearest and second-nearest colonies — the gap between these two distances is the key metric for boundary detection. In Clock 3, a pixel is classified as a boundary pixel when it lies inside a colony *and* the gap between the two nearest colony distances falls below the Border Width threshold. This dual condition ensures that boundaries only appear where colonies actually overlap — not in the open space beyond all growth fronts. The LFSR noise is added to the colony radius during the inside test, so the growth frontier itself is noisy while the boundary detection remains clean. The 8-clock total pipeline uses zero BRAMs, keeping resource utilization low at roughly 900 LUTs plus the three interpolator instances.

---

## Parameter Reference

<img src={colony_control_panel} alt="Videomancer front panel with Colony loaded"/>
*Videomancer's front panel with Colony active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Growth Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the rate at which all colony radii increase, setting the DDS accumulator step size applied on each vertical sync edge. At 0% the colonies are frozen at their current size and the territorial map is static. At moderate values the growth fronts creep outward over several seconds, giving you time to observe the Voronoi boundaries forming as colonies approach each other. At 100% the colonies race across the frame almost instantly, snapping the boundary structure into its final equilibrium configuration within a few frames. When the Animate toggle is engaged, this parameter governs the overall tempo of the expansion animation — the fundamental clock speed of the biological simulation.

---

#### Knob 2 — Colonies
| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 5 |

Selects how many colonies are active, mapped through a step function that quantizes the 10-bit register into 1 through 4 active seed points. The VHDL uses threshold tiers at 256, 512, and 768 — below 256 only colony 0 (top-left quadrant) is active, producing a single expanding disc with no boundaries. At 2 colonies the screen splits into two competing territories with a single boundary line. At 3 or 4 colonies the tessellation becomes progressively more complex, with triple junctions and enclosed cells. The visual character shifts dramatically with colony count — one colony is a radial gradient, four colonies is a full Voronoi partition of the frame.

---

#### Knob 3 — Ring Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the spacing of concentric rings within each colony's territory. In the VHDL this corresponds to the Ring Spacing parameter. The ring pattern modulates the colony interior visually — at low values the rings are tightly packed, creating a dense banding reminiscent of bacterial growth rings visible in cross-section. At high values the rings spread out into broad annular zones. At 0% rings are absent and the colony interior is a uniform tint. The ring pattern interacts with the growth animation: as the colony radius increases, the rings expand outward from the center like ripples in a pond.

---

#### Knob 4 — Border W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adjusts the width of the mutual exclusion boundary between adjacent colonies. The VHDL computes a threshold from this value: `(boundary_w >> 1) + 2`, giving a minimum width of 2 pixels and a maximum that scales with the register value. At low settings the boundary is a thin line — a mathematical Voronoi edge made visible. At high settings the boundary expands into a broad corridor of highlighted pixels, creating a stained-glass effect where the colored territorial cells are separated by thick luminous walls. The boundary width has no effect when only one colony is active, since there is no competing neighbor to trigger the boundary condition.

---

#### Knob 5 — Color Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the color saturation and spread of the colony UV offsets. The four colonies each have a distinct hue encoded as fixed UV offsets in the `C_COLONY_COLORS` constant table — red-ish, green-ish, blue-ish, and magenta-ish. This parameter scales the intensity of those offsets: at 0% the colonies are monochrome (UV at neutral 512), at 50% the tints are pastel, and at 100% the colonies saturate to their full chromatic identity. The color spread also affects the visual contrast between adjacent territories — high values make the Voronoi cells easy to distinguish by color alone, while low values require the boundary lines for differentiation.

---

#### Knob 6 — Opacity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the overall opacity of the synthesized colony pattern relative to the source video, controlling how much of the generated imagery is blended into the video stream. At 0% the colony visualization is fully transparent — only the source video passes through. At 100% the colony pattern completely replaces the video content. Intermediate values create a composite where the Voronoi tessellation overlays the video as a translucent stained-glass window, allowing the video content to be visible through the colored territorial cells. This is distinct from the Mix fader, which interpolates between processed and unprocessed outputs at the final stage.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Colony | Lichen |
| **8 — Border** | Dark | Bright |
| **9 — Video Mod** | Off | On |
| **10 — Reset** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure orthogonal aspects of the simulation. Pattern (7) selects the growth morphology — Colony for standard circular expansion, Lichen for irregular fractal fronts, Crystal for angular geometric growth, and Moss for soft organic edges. Border (8) controls the boundary line appearance — dark outlines, bright highlights, color-coded edges, or no borders at all. Video Mod (9) enables modulation of colony colors by the incoming video signal. Reset (10) clears all colony radii to zero, restarting the growth animation from seed points. Bypass (11) is the standard signal bypass. These toggles are independent — every combination of Pattern, Border, and Video Mod produces a distinct visual character, from clean geometric Voronoi diagrams to organic, video-modulated territorial maps.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix at the final stage of the pipeline. At 100% (default), the output is the fully processed colony visualization. At 0%, the output is the unprocessed input video (delayed by the 8-clock pipeline). Intermediate values crossfade smoothly via the three-channel interpolator, blending the territorial map with the original video. Use moderate mix levels to overlay the Voronoi structure as a subtle texture on the video, or pull to zero for a clean pass-through that preserves the colony state for later recall.

---

## Guided Exercises

These exercises explore Colony's synthesis capabilities from basic territorial visualization through animated growth to complex multi-layer compositions. Each builds on the previous, revealing how the interaction between colony count, growth speed, and boundary width shapes the emergent Voronoi tessellation.

### Exercise 1: Static Voronoi Map

<img src={colony_exercise1_result} alt="Static Voronoi Map result"/>
*Static Voronoi Map — simulated result across source images.*
**Objective**: Create a static four-colony territorial partition and explore how colony count and boundary width determine the tessellation geometry.

1. Set Growth Speed to about 60% and wait for colonies to expand and fill the frame.
2. Set Colonies to maximum (4 active). Four colored regions should be visible with boundaries between them.
3. Adjust Border Width from 0% to 100%. Watch the boundary lines thicken from hairlines into broad luminous corridors.
4. Try reducing Colonies to 2 — the frame splits into two halves with a single boundary line. Then 3 — a Y-shaped junction appears.
5. Sweep Color Spread to see the colonies shift from monochrome to fully saturated tints.
6. Set Growth Speed to 0% to freeze the map and examine the geometry.

**Key concepts**: Colony count determines Voronoi complexity, boundary width controls cell wall thickness, Color Spread modulates chromatic identity, freezing growth allows static analysis of the territorial partition.

---

### Exercise 2: Animated Growth from Seeds

<img src={colony_exercise2_result} alt="Animated Growth from Seeds result"/>
*Animated Growth from Seeds — simulated result across source images.*
**Objective**: Watch colonies expand from seed points in real time and observe the moment when growth fronts collide and boundaries crystallize.

1. Toggle Reset to On and then Off to clear all growth.
2. Set Growth Speed to about 25% for slow, visible expansion.
3. Set Colonies to maximum. Observe the four dots at quadrant centers.
4. As colonies expand, note how boundaries first appear as faint lines where two growth fronts meet.
5. Increase Border Width to emphasize the collision moment.
6. Try Pulse mode (Pattern → Lichen or Crystal variants) to see rhythmic expansion and contraction.

**Key concepts**: DDS-driven growth is continuous and deterministic, boundaries emerge only when colonies interact, low growth speed reveals the dynamics of territorial formation, Reset provides precise animation control.

---

### Exercise 3: Pulsing Organism

<img src={colony_exercise3_result} alt="Pulsing Organism result"/>
*Pulsing Organism — simulated result across source images.*
**Objective**: Create a rhythmic, breathing organism effect using pulse mode with high edge noise and maximum colony interaction.

1. Set Pattern to Lichen for maximum edge irregularity.
2. Set Growth Speed to about 70% for rapid pulsation.
3. Set Colonies to maximum and Border Width to about 60%.
4. Switch Border to Color for rainbow-edged cell walls.
5. Set Color Spread to maximum for vivid territorial contrast.
6. Toggle Reset to synchronize the pulse across all colonies, then observe the breathing pattern as colonies expand and contract in unison.

**Key concepts**: Pulse mode creates rhythmic expansion/contraction via DDS triangle folding, edge noise adds organic irregularity to the growth frontier, Color border mode produces chromatic cell walls, Reset synchronizes the phase of all colony oscillators.

---


## Tips

- **Reset for synchronized starts**: Toggle Reset before a performance segment to guarantee all colonies begin expanding from their seed points simultaneously. This makes the growth animation predictable and repeatable.
- **Low Colony count for simplicity**: With only 2 colonies active, the boundary reduces to a single dividing line — a clean, graphic bisection of the frame that works well as a compositional element.
- **Border Width controls visual weight**: Thin borders (10–20%) produce delicate Voronoi filigree; thick borders (60–80%) create bold stained-glass partitions where the boundaries dominate the image.
- **Color Spread at zero for monochrome maps**: Turn Color Spread to 0% for a purely luminance-based visualization where colonies differ only in brightness, not hue. This is useful for downstream keying or compositing.
- **Pulse mode for rhythmic textures**: Switch Pattern to Crystal or Lichen in combination with moderate Growth Speed for oscillating colony sizes that produce hypnotic breathing patterns. The DDS triangle fold guarantees smooth, glitch-free oscillation.
- **Mix for overlay compositing**: Pull Mix to 40–60% to overlay the colony tessellation transparently onto live video, creating a living Voronoi grid that colors and partitions the video content.
- **Edge noise adds organic character**: Increase the noise parameter to roughen the growth fronts — at high values the colonies look like biological cultures rather than geometric constructions.
- **Video Mod for reactive territories**: Enable Video Mod to let the incoming video signal modulate colony colors. Bright video regions intensify the colony tint while dark regions suppress it, creating a video-responsive territorial map.

---

## Glossary

| Term | Definition |
|------|------------|
| **Agar** | A gelatinous growth medium used in microbiology to culture bacterial colonies; Colony simulates expansion on a flat agar surface. |
| **BRAM** | Block RAM; dedicated FPGA memory used for line buffers and look-up tables. Colony uses zero BRAMs. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator, used here to drive colony radius expansion. |
| **Growth front** | The expanding edge of a colony's territory; modulated by LFSR noise for organic irregularity. |
| **L1 metric** | Manhattan distance: |Δx| + |Δy|; the distance metric used for nearest-colony assignment, producing diamond-shaped iso-distance contours. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used to add stochastic noise to colony growth edges. |
| **Manhattan distance** | The sum of absolute differences in horizontal and vertical coordinates; used instead of Euclidean distance for hardware efficiency. |
| **Mutual exclusion boundary** | The zone between two adjacent colonies where neither territory has clear dominance; detected when the gap between nearest and second-nearest distances falls below a threshold. |
| **Seed point** | The fixed center position from which a colony expands; placed at quadrant centers in Colony's configuration. |
| **Voronoi diagram** | A partition of a plane into cells, each containing all points closer to a given seed than to any other seed. Colony's territorial map is a Manhattan-metric Voronoi diagram. |
| **YUV** | A color space separating luminance (Y) from chrominance (U, V); the native pixel format of the Videomancer processing pipeline. |

---
