---
draft: true
sidebar_position: 81
slug: /instruments/videomancer/dendrite
title: "Dendrite"
image: /img/instruments/videomancer/dendrite/dendrite_hero.png
description: "Water freezing on a windowpane does not spread uniformly."
---

import dendrite_hero from '/img/instruments/videomancer/dendrite/dendrite_hero.png';
import dendrite_animation from '/img/instruments/videomancer/dendrite/dendrite_animation.gif';
import dendrite_control_panel from '/img/instruments/videomancer/dendrite/dendrite_control_panel.png';
import dendrite_exercise1_result from '/img/instruments/videomancer/dendrite/dendrite_exercise1_result.gif';
import dendrite_exercise2_result from '/img/instruments/videomancer/dendrite/dendrite_exercise2_result.gif';
import dendrite_exercise3_result from '/img/instruments/videomancer/dendrite/dendrite_exercise3_result.gif';

# Dendrite

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={dendrite_hero} alt="Dendrite hero image"/>
*Dendrite overlaying branching crystal structures onto a live video source, tracing frost-like growth patterns across the frame.*
<img src={dendrite_animation} alt="Dendrite animated output"/>
*Dendrite output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Water freezing on a windowpane does not spread uniformly. It starts from a seed — a speck of dust, a scratch in the glass — and grows outward in branching fingers, each one splitting and turning as it encounters variations in temperature and surface texture. The result is a dendritic structure: a tree-like pattern where no two branches are identical, yet the overall form is instantly recognizable as frost.

Dendrite simulates this process in real time. Eight branch arms grow outward from the center of the frame, each following a compass direction that jitters randomly from frame to frame. As the branches extend, every pixel in the image checks its Manhattan distance to the nearest branch tip. Pixels close to a branch receive a luminance boost and a color tint — white or blue — simulating the crystalline glow of frost. Pixels far from any branch are dimmed, pushing the background into shadow. The result is an evolving, organic overlay that traces branching paths across whatever video source is connected.

The name comes from the Greek *dendron* (tree), the same root that gives us the branching structures of nerve cells, mineral crystal formations, and the mathematical models that generate them. In Dendrite, the tree grows continuously — controlled by speed, spread, and glow parameters — until the operator resets it and the growth begins again from the center.

---

## Quick Start

1. **Reset is your rhythm tool**: Toggling Reset on and off in time with music creates pulsing crystal bursts that grow outward, vanish, and regrow. Each cycle produces a unique pattern because the LFSR is in a different state.
2. **Branch spread is the organic control**: At zero, Dendrite produces geometric starbursts. Even a small amount of spread (10–20%) introduces enough randomness to create natural-looking frost. Above 60%, branches become chaotic.
3. **Background dim creates depth**: Use moderate background dimming (40–60%) to push the source video into shadow, making the crystal overlay feel like it's on a separate layer in front of the image.

---

## Background

### Diffusion-Limited Aggregation

Dendrite's branching patterns are inspired by **diffusion-limited aggregation** (DLA), a model first described by Witten and Sander in 1981. In DLA, particles undergo random walks until they contact a growing cluster, at which point they stick permanently. The resulting structures are fractal — self-similar at multiple scales — with characteristic branching that resembles frost, lightning, mineral deposits, and river deltas. The FPGA implementation simplifies DLA to eight deterministic arms with LFSR-driven direction jitter, but the visual result captures the essential character of aggregation growth: branching paths that spread outward with controlled randomness.

### Crystal Growth and Frost Patterns

Natural frost forms when water vapor deposits directly onto a cold surface as ice crystals. The growth follows the surface's thermal gradients — advancing faster where the surface is coldest and the vapor supply is greatest. Each crystal face grows at a rate determined by its crystallographic orientation, which is why frost patterns exhibit six-fold symmetry at the microscopic scale but appear random at the macroscopic scale. Dendrite's eight compass directions approximate this directional growth, with the branch spread parameter controlling how much each arm deviates from its initial heading — low spread produces straight radial lines, high spread produces wandering, organic branches.

### Lichtenberg Figures

When a high voltage is discharged through an insulating material — resin, acrylic, glass — the electrical breakdown traces branching paths called **Lichtenberg figures**. These figures follow the same mathematical principles as DLA and frost: the discharge propagates along the path of least resistance, branching wherever the field strength is sufficient to ionize new material. Dendrite's inward growth mode (direction toggle) reverses the branch propagation, creating patterns that converge rather than diverge — visually similar to the root-like structures of captured lightning.

### Manhattan Distance and Digital Proximity

The program determines each pixel's proximity to the nearest branch tip using **Manhattan distance** — the sum of absolute horizontal and vertical offsets, named for the grid-like street layout of Manhattan. Unlike Euclidean distance (straight-line), Manhattan distance produces diamond-shaped glow patterns around each branch tip. This is a deliberate design choice: Manhattan distance requires only addition and comparison (no multiplication or square root), making it efficient in FPGA fabric. The diamond-shaped glow gives the crystal overlay a faceted, mineral-like quality rather than the smooth circles of Euclidean proximity.

### Generative Art and Procedural Overlay

Dendrite belongs to a tradition of generative overlay effects where algorithmically created graphics are composited onto live video. Unlike programs that purely transform the input signal, Dendrite *generates* structure — the branch positions, glow fields, and crystal tints — and layers it on top of the source. The source video provides the canvas; the algorithm provides the frost. This overlay approach means the effect is additive: the original image remains visible beneath the crystal layer, with the mix fader controlling the balance between generated and source content.


---

## Signal Flow

Branch Growth Engine → Per-Pixel Pipeline → Wet/Dry Mix → Sync Delay Pipeline → Bypass Mux

```
Input Video (YUV 4:4:4)
│
├── Branch Growth Engine (updated on vsync) ────────────────────
│   │
│   ├─ 8 branch arms, each with (x, y, direction)
│   ├─ LFSR jitters direction per frame
│   ├─ Growth speed controls update rate
│   ├─ Branch spread controls direction jitter range
│   ├─ Direction toggle: outward / inward
│   └─ Reset returns all branches to center (960, 540)
│
├── Per-Pixel Pipeline ─────────────────────────────────────────
│   │
│   ├─ Stage 1: Manhattan distance to all 8 branch tips → min
│   ├─ Stage 2: Glow determination (distance < threshold?)
│   │           Glow level = inverse distance (closer = brighter)
│   ├─ Stage 3: Composite
│   │   ├─ Crystal pixel: Y += glow >> bright_shift
│   │   │                 UV = white (512,512) or blue (700,400)
│   │   └─ Background pixel: Y dimmed, UV pass-through
│   └─ Stage 4: Output registration
│
├── Wet/Dry Mix (3× interpolator_u) ────────────────────────────
│   └─ Blend processed ↔ delayed original per Mix fader
│
├── Sync Delay Pipeline (8 clocks) ─────────────────────────────
│   └─ hsync, vsync, field, Y, U, V delayed to match processing
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed or original signal
```

The branch growth engine operates asynchronously from the pixel pipeline — branches update their positions once per frame on the vsync rising edge, while the pixel pipeline runs at full pixel clock. This means the crystal overlay is spatially static within each frame and only moves between frames, producing smooth animation rather than per-scanline jitter. The growth speed counter gates how frequently branches actually advance, so low speed values cause the pattern to evolve over many seconds while high values produce rapid growth.

The glow threshold derived from the Glow Size parameter determines the diamond-shaped region around each branch tip where pixels are affected. Within this region, the glow level is the *difference* between the threshold and the actual distance — so pixels directly on a branch tip receive maximum brightness boost, and pixels at the threshold boundary receive none. This inverse-distance falloff creates a natural luminance gradient radiating outward from each branch.

---

## Parameter Reference

<img src={dendrite_control_panel} alt="Videomancer front panel with Dendrite loaded"/>
*Videomancer's front panel with Dendrite active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Growth Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how quickly the branches extend outward from their seed point. The growth speed register gates a frame counter — higher values allow the branches to advance on more frames, producing faster growth. At minimum, the branches are essentially frozen in place; at maximum, they race outward and can traverse the full frame in a few seconds. Because the LFSR jitters the direction each time a branch advances, faster growth also means more frequent direction changes, which produces denser, more convoluted branching paths.

---

#### Knob 2 — Density
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the glow radius around each branch tip. In the VHDL, this parameter maps to the glow threshold calculation: larger values expand the diamond-shaped region where pixels receive crystal brightening. At low values, only pixels very close to a branch tip are affected, producing thin, wire-like crystal traces. At high values, each branch tip radiates a broad glow that overlaps with neighboring branches, filling larger areas of the frame with frost-like luminance.

---

#### Knob 3 — Branch
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness boost applied to crystal pixels — those within the glow threshold of any branch tip. The parameter maps to a shift value that scales the glow level before it is added to the input luminance. At low settings, the crystal overlay is subtle and translucent. At high settings, crystal pixels are driven toward peak white, creating hard, bright frost lines against the dimmed background. The boost is additive and clamped to 1023, so bright source regions near branch tips will clip to white.

---

#### Knob 4 — Seed Pos
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how much the background — pixels outside the glow threshold of any branch — is dimmed. The VHDL implements this as a shift-based attenuation of the input luminance. At minimum, the background actually receives a slight brightness boost (factor ~1.5×). As the control increases through its midrange, the background passes through unity and then progressively darkens, reaching approximately 56% of original brightness at maximum. This dimming increases the visual contrast between the glowing crystal overlay and the underlying video.

---

#### Knob 5 — Crystal Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the size of the glow field around each branch tip. This parameter feeds directly into the glow threshold calculation: `threshold = (register >> 2) + 2`. At minimum, the threshold is just 2 pixels — essentially point-like crystal markers. At maximum, the threshold reaches 257 pixels of Manhattan distance, creating broad diamond-shaped glow regions that can span a significant portion of the frame. This interacts with the density parameter (Pot 2) to determine the overall coverage and intensity of the crystal overlay.

---

#### Knob 6 — Opacity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the range of direction jitter applied to each branch on every growth step. The branch spread register is masked against the LFSR output to determine how much each branch's compass direction deviates when it advances. At zero spread, branches grow in perfectly straight lines along their initial compass headings — producing a symmetric starburst. As spread increases, each step can veer further from the previous direction, creating increasingly organic, wandering paths that resemble natural frost crystallization.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Seed Mode** | Center | Multi |
| **8 — Growth** | Tree | Light |
| **9 — Video Mod** | Off | On |
| **10 — Reset** | Off | On |
| **11 — Bypass** | Off | On |

The TOML labels for toggles 7 and 8 suggest four-position selectors (Center/Edge/Corner/Multi and Tree/Frost/Coral/Light), but the VHDL reads only a single bit from each toggle register. In practice, only two states are active: the first label (bit=0) and the second label (bit=1). Toggles 9–11 are straightforward binary on/off switches. Together, the five toggles control color mode, growth direction, animation enable, growth reset, and bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Dendrite-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises explore Dendrite's crystal growth from simple radial patterns through organic frost textures to dynamic video-reactive compositions.

### Exercise 1: Radial Starburst

<img src={dendrite_exercise1_result} alt="Radial Starburst result"/>
*Radial Starburst — simulated result across source images.*
**What You'll Create**: Observe the basic branch growth pattern and understand how speed and spread interact.

1. **Reset**: Toggle Reset (Switch 10) on and off to seed the branches at center.
2. **Enable animation**: Ensure Video Mod (Switch 9) is on.
3. **Slow growth**: Set Growth Sp to about 25%. Watch the eight branches slowly extend outward along their compass directions.
4. **Zero spread**: Set Opacity (Branch Spread) to 0%. The branches grow in perfectly straight lines — a symmetric eight-pointed star.
5. **Add spread**: Gradually increase Opacity to 50%. The branches begin to wander, deviating from their compass headings with each step.
6. **Full spread**: Push Opacity to 100%. The branches take highly irregular paths, doubling back and crossing each other.
7. **Reset and repeat**: Toggle Reset to restart the growth. Each run produces a different pattern because the LFSR phase differs.

**Key concepts**: Branch growth is frame-synchronized, direction jitter is LFSR-driven, zero spread produces straight compass lines, higher spread produces organic wandering

---

### Exercise 2: Frost on Glass

<img src={dendrite_exercise2_result} alt="Frost on Glass result"/>
*Frost on Glass — simulated result across source images.*
**What You'll Create**: Create a convincing frost-on-glass effect using glow size, crystal brightness, and background dimming.

1. **Reset and grow**: Start fresh with a Reset toggle. Set Growth Sp to ~40% and let branches grow for several seconds.
2. **Expand glow**: Increase Crystal Hue (Glow Size) to ~60%. The diamond-shaped glow regions around each branch tip expand, creating broad frost patches.
3. **Brighten crystals**: Set Branch (Crystal Brightness) to ~70%. The frost lines become prominently bright against the source.
4. **Dim background**: Increase Seed Pos (Background Dim) to ~60%. The areas between frost branches darken, simulating the view through frosted glass where unfrosted regions are clearer.
5. **Blue tint**: Switch Seed Mode (Toggle 7) to Edge position for blue frost. The crystal overlay shifts from white to cool blue.
6. **Blend**: Pull Mix down to ~70%. The frost becomes translucent, revealing more of the source image beneath.

**Key concepts**: Glow size sets the frost patch radius, crystal brightness controls frost opacity, background dim controls contrast between frosted and clear areas, blue tint simulates natural ice color

---

### Exercise 3: Lightning Convergence

<img src={dendrite_exercise3_result} alt="Lightning Convergence result"/>
*Lightning Convergence — simulated result across source images.*
**What You'll Create**: Use inward growth mode with fast speed to create converging lightning-like patterns.

1. **Inward mode**: Set Growth (Toggle 8) to Frost position for inward growth.
2. **Fast growth**: Set Growth Sp to ~80%.
3. **High spread**: Set Opacity (Branch Spread) to ~60% for irregular, lightning-like branching.
4. **Narrow glow**: Set Crystal Hue (Glow Size) to ~20% for thin, sharp crystal lines.
5. **Maximum brightness**: Set Branch (Crystal Brightness) to ~90% for intense white lines.
6. **White frost**: Set Seed Mode (Toggle 7) to Center for achromatic white.
7. **Watch convergence**: Let branches grow inward. They converge toward center from their starting positions.
8. **Reset and loop**: Toggle Reset to restart. The branches re-emerge from center and reverse inward. Rapid reset cycling creates a pulsing, breathing pattern of converging light.

**Key concepts**: Inward growth reverses branch direction vectors, high speed with high spread creates jagged paths, narrow glow produces sharp lines, rapid reset cycling creates rhythmic patterns

---


## Tips

- **Blue frost on warm sources**: The blue tint (Toggle 7, Edge position) is most effective over warm-toned source material — skin tones, fire, sunset colors — where the cool blue creates strong color contrast.
- **Freeze for compositing**: Disable animation (Toggle 9 off) once the crystal pattern reaches a shape you like. The frozen overlay can then be used as a static graphic element, blended with live video via the Mix fader.
- **Inward mode for implosion**: Inward growth (Toggle 8, Frost position) creates patterns that feel like energy converging rather than radiating. Combined with fast growth and rapid reset cycling, this produces a rhythmic breathing effect.
- **Mix for transparency**: The fader does not affect the crystal shape — it only controls the blend opacity. At 30–50% mix, the frost overlay becomes a delicate translucent texture rather than a dominant graphic element.

---

## Glossary

| Term | Definition |
|------|------------|
| **Compass Direction LUT** | A lookup table mapping 8 integer indices (0–7) to unit vectors in the cardinal and ordinal directions (E, NE, N, NW, W, SW, S, SE). |
| **Dendritic** | Tree-like; branching structures that subdivide recursively, named from the Greek *dendron* (tree). |
| **DLA** | Diffusion-Limited Aggregation; a model of particle growth where random-walking particles stick to a growing cluster on contact, producing fractal branching. |
| **Glow Threshold** | The maximum Manhattan distance from a branch tip at which a pixel receives crystal brightening; pixels beyond this distance are treated as background. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a function of its previous state, generating a deterministic pseudo-random sequence. |
| **Lichtenberg Figure** | A branching electrical discharge pattern captured in an insulating material; visually similar to DLA structures. |
| **Manhattan Distance** | The sum of absolute horizontal and vertical offsets between two points; produces diamond-shaped equidistant contours rather than the circles of Euclidean distance. |
| **Vsync** | Vertical synchronization pulse marking the boundary between video frames; Dendrite updates branch positions on the vsync rising edge. |

---
