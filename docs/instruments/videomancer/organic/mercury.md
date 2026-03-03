---
draft: true
sidebar_position: 190
slug: /instruments/videomancer/mercury
title: "Mercury"
image: /img/instruments/videomancer/mercury/mercury_hero.png
description: "Mercury simulates the behaviour of liquid metal — droplets of chrome that orbit, merge, and split in a continuous dance driven by digital oscillators."
---

import mercury_hero from '/img/instruments/videomancer/mercury/mercury_hero.png';
import mercury_animation from '/img/instruments/videomancer/mercury/mercury_animation.gif';
import mercury_control_panel from '/img/instruments/videomancer/mercury/mercury_control_panel.png';
import mercury_exercise1_result from '/img/instruments/videomancer/mercury/mercury_exercise1_result.gif';
import mercury_exercise2_result from '/img/instruments/videomancer/mercury/mercury_exercise2_result.gif';
import mercury_exercise3_result from '/img/instruments/videomancer/mercury/mercury_exercise3_result.gif';

# Mercury

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={mercury_hero} alt="Mercury hero image"/>
*Liquid chrome blobs orbit and merge on a black field, their specular edges flaring as surface tension draws bright rings around each metallic puddle.*
<img src={mercury_animation} alt="Mercury animated output"/>
*Mercury output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Mercury simulates the behaviour of liquid metal — droplets of chrome that orbit, merge, and split in a continuous dance driven by digital oscillators. Each blob is defined by a DDS (Direct Digital Synthesis) phase accumulator that traces an elliptical path across the screen. For every pixel, the program computes the Manhattan distance to the nearest blob centre. Pixels inside the blob radius are rendered as bright chrome (high luma, neutral chroma), and a surface-tension edge ring at the boundary draws a specular highlight — the bright glint that real mercury exhibits where surface curvature is highest.

Two or four blobs can be active simultaneously. Because each blob's DDS uses coprime frequency multipliers, the blobs orbit at different rates, periodically approaching one another and "merging" when their radii overlap in the distance field. The minimum-distance selector automatically creates the illusion of pooling: where two blobs are close, the near-equal distances produce a saddle point in the field, and the edge-detection threshold draws a bright bridge between them. When the blobs separate, the bridge snaps apart and the droplets resume their independent orbits.

The name references the element mercury (quicksilver) — the only metal that is liquid at room temperature. Its high surface tension causes it to bead into nearly perfect spheres, and its mirror-bright surface reflects its surroundings with a convex distortion. Mercury's rainbow mode swaps the neutral chrome for per-blob colour assignment, turning the metallic simulation into a coloured Voronoi diagram where each blob's territory is painted a different hue.

---

## Background

### Liquid Metal Surface Tension

Surface tension is the cohesive force that causes the surface of a liquid to contract to the smallest possible area. In mercury, this force is exceptionally strong — about six times that of water — which is why mercury beads into tight, nearly spherical droplets rather than spreading out. At the boundary of each droplet, the surface curves sharply, and this curvature creates a bright specular highlight when light reflects off it. Mercury's edge-detection stage models this phenomenon: pixels near the blob boundary (within the surface-tension width) are rendered at full reflectivity, while interior pixels receive a slightly distance-attenuated brightness. The result is the characteristic bright ring around each blob that makes it look three-dimensional and metallic.

### Manhattan Distance Fields

A distance field assigns to each pixel the distance to the nearest feature point — in this case, the nearest blob centre. Euclidean distance (the straight-line metric) requires a square root, which is expensive in hardware. The Manhattan distance (also called the L1 norm or taxicab distance) uses the sum of absolute coordinate differences: $d = |x_1 - x_2| + |y_1 - y_2|$. This metric produces diamond-shaped contours rather than circular ones, giving Mercury's blobs their characteristic angular, crystalline appearance. The computation requires only subtraction and absolute value — no multiplier, no BRAM — making it ideal for the resource-constrained iCE40 FPGA.

### Direct Digital Synthesis for Animation

Each blob's position is driven by a pair of DDS phase accumulators — one for X, one for Y. A phase accumulator is simply a register that increments by a fixed amount on each clock (here, once per video frame at vsync). The top bits of the accumulator represent the current position, and because the accumulator wraps around at overflow, the position traces a periodic orbit. By using coprime frequency multipliers for different blobs (137, 251, 199, 311 for X; 173, 293, 223, 157 for Y), Mercury ensures that no two blobs follow exactly the same path, producing complex Lissajous-like trajectories that bring blobs into proximity at irregular intervals — creating the unpredictable merge-and-split behaviour that gives the simulation its organic quality.

### Voronoi Diagrams and Nearest-Neighbour Partitioning

When Mercury renders in rainbow mode, the screen is effectively partitioned into Voronoi cells — regions where each pixel is coloured according to the nearest blob. A Voronoi diagram is a fundamental structure in computational geometry, appearing in crystal growth, cell biology, and territorial mapping. Mercury's 2-level parallel minimum-distance selector performs the nearest-neighbour lookup in hardware: distances to all four blobs are computed simultaneously, then reduced via two levels of pairwise comparison to find the closest blob and its index. The blob index drives the colour assignment, painting each cell a different hue derived from the reflectivity parameter.

### LFSR Jitter and Organic Motion

A 16-bit maximal-length Linear Feedback Shift Register (LFSR) generates pseudo-random noise that is added to the blob positions at each frame. The jitter amplitude is controlled by the Jitter pot (labelled "Pool Spd" on the panel). This noise breaks the perfect periodicity of the DDS orbits, adding the kind of wobble and irregularity that real liquid droplets exhibit as they respond to vibrations, thermal fluctuations, and surface imperfections. Alternating the jitter sign between blob pairs creates asymmetric perturbations, so the blobs don't all wobble in the same direction at the same time.


---

## Signal Flow

```
                              ┌──────────────────────────────────────┐
                              │ Register Decode                      │
                              │  blob_size = reg(0) [radius]         │
                              │  speed     = reg(1) [DDS increment]  │
                              │  tension   = reg(2) [edge width]     │
                              │  reflect   = reg(3) [chrome bright]  │
                              │  jitter    = reg(4) [LFSR amplitude] │
                              │  mix_pot   = reg(5) [UNUSED]         │
                              │  toggles:  reg(6) bits 0-4           │
                              │  mix_amt   = reg(7)                  │
                              └──────────────────┬───────────────────┘
                                                 │
          ┌──────────────────────────────────────┐│
          │ Blob DDS Update (once per vsync)     ││
          │  dds_x(i) += speed<<3 + X_MULT(i)   ││
          │  dds_y(i) += speed<<3 + Y_MULT(i)   ││
          │  blob_pos = dds[15:4] + lfsr_jitter  ││
          └──────────────────────────────────────┘│
                                                  │
┌─────────────────────────────────────────────────┤
│ Stage 1: Input Register + Manhattan Distance    │
│  For each blob i:                               │
│    dist(i) = |h_count - blob_x(i)|             │
│            + |v_count - blob_y(i)|             │
│  Register input Y, U, V                        │
└──────────────────────────┬──────────────────────┘
                           │
┌──────────────────────────┴──────────────────────┐
│ Stage 2: Min Distance Select + Edge Detect      │
│  2-level parallel min: d01 vs d23 → min_dist   │
│  radius = blob_size << 2                        │
│  edge_lo = radius - (tension >> 1)              │
│  is_inside = (min_dist < radius)                │
│  is_edge   = (min_dist >= edge_lo) AND inside   │
└──────────────────────────┬──────────────────────┘
                           │
┌──────────────────────────┴──────────────────────┐
│ Stage 3: Chrome Render + Color Select           │
│  Edge:    Y = reflectivity, U=V=512             │
│  Inside:  Y = reflect - (min_dist>>3), clamped  │
│           Rainbow? U,V by blob_idx              │
│           Chrome?  U=V=512                      │
│  Outside: pass source Y, U, V                  │
└──────────────────────────┬──────────────────────┘
                           │
┌──────────────────────────┴──────────────────────┐
│ Stage 4: Composite with Source                  │
│  Replace: chrome replaces source                │
│  Additive: Y = clamp(src_Y + chrome_Y)          │
│            U,V = avg(src, chrome)               │
│  Outside: pass source                           │
└──────────────────────────┬──────────────────────┘
                           │
┌──────────────────────────┴──────────────────────┐
│ Interpolator (4 clocks)                         │
│  lerp(dry, wet, mix_amount) × 3 channels       │
└──────────────────────────┬──────────────────────┘
                           │
       data_in ──► [8-clk sync delay] ──► dry     │
                                                   ▼
                                               data_out
                                       (bypass mux if s_bypass)
```

The pipeline's most distinctive feature is the parallel Manhattan distance computation in Stage 1, which evaluates all four blob distances simultaneously in a single clock. The 2-level minimum selector in Stage 2 uses two pairwise comparisons followed by a final comparison — a classic parallel reduction tree that finds both the minimum distance and the winning blob index in one clock. Edge detection is a simple threshold band: pixels whose distance falls between `radius - tension_width` and `radius` are classified as edge pixels and receive the full specular highlight. The DDS position update runs asynchronously from the pixel pipeline, executing once per frame at vsync, which ensures smooth animation without per-pixel overhead.

Note that register 5 (`s_mix_pot`, labelled "Ripple" on the panel) is declared but never referenced in the processing pipeline. The actual wet/dry mix is controlled exclusively by register 7 (`s_mix_amount`, the fader).

---

## Parameter Reference

<img src={mercury_control_panel} alt="Videomancer front panel with Mercury loaded"/>
*Videomancer's front panel with Mercury active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Blob Cnt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the radius of each blob despite being labelled "Blob Cnt" on the panel. In the VHDL, the register value is shifted left by 2 bits, giving an effective range of 0 to about 4092 pixels in Manhattan distance. At low values the blobs are tiny pinpoints — barely visible specular dots orbiting the screen. At high values the blobs expand to fill large regions of the frame, and the merge zones between adjacent blobs become correspondingly wider. Because the edge highlight width (Tension) is subtracted from this radius, increasing Blob Cnt also increases the proportion of each blob that is rendered as solid interior chrome versus bright specular rim. At maximum, the blobs may overlap continuously, producing a single merged metallic field.

---

#### Knob 2 — Blob Sz
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the DDS orbit speed despite being labelled "Blob Sz" on the panel. The register value is shifted left by 3 bits and added to each blob's fixed coprime frequency multiplier before being used as the DDS phase increment. At zero, only the coprime offsets drive the orbits — the blobs move very slowly. At maximum, the blobs orbit rapidly, tracing their Lissajous paths multiple times per second. Because the four blobs have different coprime multipliers, increasing speed doesn't make them move in lockstep — it accelerates each blob proportionally, maintaining the complex phase relationships that produce unpredictable merge encounters. Speed interacts with Jitter: at high speed with high jitter, blob paths become chaotic and the merging pattern is highly irregular.

---

#### Knob 3 — Tension
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the width of the surface-tension edge highlight ring. The register value is shifted right by 1 bit, giving a maximum edge width of about 512 pixels. This value is subtracted from the blob radius to create a threshold band: pixels with Manhattan distance between `radius - tension_width` and `radius` are classified as edge pixels and rendered at full reflectivity brightness. At low Tension values, only a thin bright ring appears at the blob boundary — a sharp, crisp specular highlight. At high values, a wide bright band surrounds each blob, creating a soft, luminous halo effect. When two blobs approach each other and their edge bands overlap in the distance field, the surface tension ring bridges between them, visually simulating the meniscus that forms when two mercury droplets begin to merge.

---

#### Knob 4 — Reflect
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness of the chrome rendering — both the specular edge highlight and the blob interior. At the edge, luma is set directly to the Reflect value. In the interior, luma is calculated as `reflectivity - (min_distance >> 3)`, producing a gradual falloff from the edge inward. At zero, blobs are invisible (black chrome). At maximum (1023), the specular ring is pure white and the blob interior is bright silver with gentle distance shading. In rainbow mode, Reflect also scales the chroma offset — higher values produce more saturated per-blob colours, while lower values produce muted, pastel tints.

---

#### Knob 5 — Pool Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the amplitude of LFSR jitter noise added to blob positions, despite being labelled "Pool Spd" on the panel. The register value is shifted right by 2 bits, then ANDed with the LFSR output bytes to produce position offsets. At zero, no jitter is applied and the blobs trace perfectly smooth DDS orbits. At moderate values, the blobs wobble slightly as they orbit — an organic tremor that breaks the mathematical precision of the Lissajous paths. At maximum, the jitter dominates the motion, causing the blobs to jump erratically around their DDS-defined positions. Jitter is applied asymmetrically: one blob pair gets positive jitter while the other pair may get negative jitter (controlled by LFSR bit 0), preventing all blobs from wobbling in the same direction simultaneously.

---

#### Knob 6 — Ripple
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Labelled "Ripple" on the panel, this register is mapped to `s_mix_pot` in the VHDL but is never referenced in the processing pipeline. Adjusting this knob has no visible effect on the output. The actual wet/dry mix is handled exclusively by the fader (register 7). This is a vestigial parameter — likely intended for a ripple distortion effect that was removed during development.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Shape** | Organic | Geomtrc |
| **8 — Metal** | Silver | Gold |
| **9 — Merge** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 each present four labels on the panel but are wired to single bits in the VHDL, meaning only two states are actually available per toggle. Toggle 9 selects between chrome and rainbow colouring. Toggle 10 controls animation freeze but is inverted relative to its label — "On" in the TOML means the freeze bit is set, which stops animation. Toggle 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix at the end of the processing chain. At 100%, the output is the fully composited blob rendering. At 0%, the output is the unprocessed source video. Intermediate values blend between the two via three 4-clock interpolators operating on Y, U, and V simultaneously. This control is the primary tool for dialing in subtle metallic overlay effects — at 30–50%, the chrome blobs become translucent ghosts hovering over the video.

---

## Guided Exercises

These exercises progress from basic blob visualization through merge behaviour exploration to animated rainbow Voronoi fields. Each reveals a different aspect of the distance-field rendering and DDS animation system.

### Exercise 1: Static Chrome Droplets

<img src={mercury_exercise1_result} alt="Static Chrome Droplets result"/>
*Static Chrome Droplets — simulated result across source images.*
**Objective**: Visualize the basic blob geometry and understand how radius and surface tension shape the metallic rendering.

1. **Freeze animation**: Set Animate to On (which freezes the DDS accumulators, halting blob motion).
2. **Two blobs**: Set Shape to Organic (2-blob mode). Two metallic discs appear on the screen.
3. **Adjust radius**: Sweep Blob Cnt from 0% to ~60%. The blobs grow from pinpoints to large metallic pools.
4. **Observe edge ring**: Set Tension to ~40%. A bright specular ring appears around each blob boundary.
5. **Increase Tension**: Push to ~70%. The bright ring widens, consuming more of the blob interior.
6. **Adjust Reflectivity**: Sweep Reflect from 0% (invisible) to 100% (brilliant white chrome).

**Key concepts**: Blob Cnt controls radius via left-shift by 2, Tension controls edge highlight width, Reflect sets chrome brightness, Manhattan distance produces diamond-shaped contours

---

### Exercise 2: Merge Behaviour and Compositing

<img src={mercury_exercise2_result} alt="Merge Behaviour and Compositing result"/>
*Merge Behaviour and Compositing — simulated result across source images.*
**Objective**: Explore how blobs merge when their distance fields overlap, and compare additive versus replace compositing.

1. **Enable animation**: Set Animate to Off (animation runs — inverted label). Set Blob Sz to ~30% for slow orbits.
2. **Four blobs**: Set Shape to Geomtrc (4-blob mode). Four metallic discs orbit the screen.
3. **Large radius**: Set Blob Cnt to ~60% so the blobs often overlap.
4. **Watch merges**: As blobs approach, their surface-tension rings bridge together. The minimum-distance field creates a saddle point between them.
5. **Additive mode**: Set Metal to Silver (additive). Where blobs overlap the source video, brightness accumulates — merged regions are brighter.
6. **Replace mode**: Set Metal to Gold (replace). Blobs are now opaque — merged regions show only the chrome, no source video beneath.

**Key concepts**: Merge occurs naturally via minimum-distance selection, additive compositing accumulates brightness, replace compositing makes blobs opaque, 4-blob mode creates more frequent merge events

---

### Exercise 3: Rainbow Voronoi with Jitter

<img src={mercury_exercise3_result} alt="Rainbow Voronoi with Jitter result"/>
*Rainbow Voronoi with Jitter — simulated result across source images.*
**Objective**: Activate rainbow mode and jitter to create an animated, colour-partitioned Voronoi field with organic wobble.

1. **Enable rainbow**: Toggle Merge On. Each blob's territory is now painted a different colour.
2. **Four blobs**: Set Shape to Geomtrc (4 blobs) for a full four-colour partition.
3. **Animation running**: Set Animate to Off (animation runs). Set Blob Sz to ~40% for moderate orbit speed.
4. **Add jitter**: Increase Pool Spd to ~50%. The blob orbits gain organic wobble.
5. **Large radius**: Set Blob Cnt to ~80%. The blobs fill the screen, creating a continuous Voronoi tessellation with no gaps.
6. **Observe colour boundaries**: The per-blob colour assignment makes the Voronoi cell boundaries visible. Where two cells meet, the colour changes abruptly across the equal-distance line.

**Key concepts**: Rainbow mode assigns hue by blob index, Voronoi partition emerges from nearest-neighbour distance selection, jitter breaks DDS periodicity for organic motion, large radius eliminates black gaps

---


## Tips

- **Blob Cnt is radius, not count**: Despite the panel label, this knob controls the size of each blob via a left-shift by 2. For blob count, use the Shape toggle (2 or 4 blobs).
- **Blob Sz is speed, not size**: This knob controls DDS orbit speed via a left-shift by 3. For blob size, use the Blob Cnt knob.
- **Ripple does nothing**: Register 5 is declared but unreferenced in the VHDL. Adjusting this knob has zero effect on the output.
- **Animate is inverted**: Toggle On = freeze, Toggle Off = run. The VHDL signal `s_freeze` is active-high, opposite to what the label suggests.
- **Shape and Metal are binary**: Despite having four labels each, these toggles are single-bit — only two states exist. Shape: 2 blobs / 4 blobs. Metal: additive / replace.
- **Large radius + high tension = full merge**: Pushing Blob Cnt and Tension to high values causes the blobs to fill the screen as a continuous chrome field — useful as a metallic overlay texture.
- **Jitter for organic motion**: Pool Spd adds LFSR noise to blob positions. Even small amounts (~20%) break the mathematical precision of the DDS orbits, making the motion feel alive.
- **Rainbow + 4 blobs = Voronoi art**: Enable Merge (rainbow) and Geomtrc (4 blobs). Set Blob Cnt high enough that the blobs tile the screen. The result is an animated four-colour Voronoi partition — a real-time computational geometry visualization.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory blocks within an FPGA. Mercury uses zero BRAMs — all computation is combinatorial and register-based. |
| **Coprime** | Two integers whose greatest common divisor is 1. Mercury uses coprime frequency multipliers for each blob's DDS to ensure their orbits never synchronize exactly. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator that wraps at overflow, producing a sawtooth phase ramp whose top bits represent position. |
| **Distance field** | A scalar field that assigns to each pixel the distance to the nearest feature point. Mercury uses Manhattan distance to the nearest blob centre. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip that implements Mercury's pixel pipeline in parallel hardware. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function (XOR) of its previous state. Produces a pseudo-random sequence that repeats after $2^n - 1$ cycles. |
| **Lissajous figure** | The path traced by a point whose X and Y coordinates are independent sinusoidal (or periodic) functions of time. Mercury's blob orbits are Lissajous-like curves driven by DDS accumulators. |
| **Manhattan distance** | The L1 or taxicab distance metric: $d = |x_1 - x_2| + |y_1 - y_2|$. Produces diamond-shaped equidistant contours instead of circles. |
| **Specular highlight** | A bright reflection on a curved surface where the viewing angle equals the reflection angle. Mercury simulates this as a bright edge ring at the blob boundary. |
| **Surface tension** | The cohesive force at a liquid's surface that minimizes its area. In Mercury, this parameter controls the width of the edge highlight ring that simulates specular reflection. |
| **Voronoi diagram** | A partition of a plane into regions based on proximity to a set of seed points, where each region contains all points closer to its seed than to any other. Mercury's rainbow mode visualizes this partition. |
| **YUV** | A colour space separating luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |

---
