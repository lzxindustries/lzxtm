---
draft: true
sidebar_position: 186
slug: /instruments/videomancer/marcher
title: "Marcher"
image: /img/instruments/videomancer/marcher/marcher_hero.png
description: "Signed distance fields (SDFs) define geometry not by drawing edges or filling polygons, but by computing a single number at every point in space: the shortest distance to the nearest surface."
---

import marcher_hero from '/img/instruments/videomancer/marcher/marcher_hero.png';
import marcher_animation from '/img/instruments/videomancer/marcher/marcher_animation.gif';
import marcher_control_panel from '/img/instruments/videomancer/marcher/marcher_control_panel.png';
import marcher_exercise1_result from '/img/instruments/videomancer/marcher/marcher_exercise1_result.gif';
import marcher_exercise2_result from '/img/instruments/videomancer/marcher/marcher_exercise2_result.gif';
import marcher_exercise3_result from '/img/instruments/videomancer/marcher/marcher_exercise3_result.gif';

# Marcher

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={marcher_hero} alt="Marcher hero image"/>
*Marcher rendering six smoothly merging SDF primitives with orbiting light, distance-based contour lines, and the Neon color palette.*
<img src={marcher_animation} alt="Marcher animated output"/>
*Marcher output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Signed distance fields (SDFs) define geometry not by drawing edges or filling polygons, but by computing a single number at every point in space: the shortest distance to the nearest surface. If the number is negative, the point is inside an object. If positive, it is outside. If zero, it is exactly on the boundary. Marcher evaluates this computation at every pixel, every frame, directly on the FPGA — no CPU, no frame buffer, no ray-marching iteration loop. The result is a real-time field of six moving geometric primitives that merge, separate, and flow like liquid blobs.

The six primitives — four circles and two boxes (when mixed mode is enabled) — orbit the center of the screen on DDS-driven Lissajous paths, each at a different coprime frequency so the trajectories never exactly repeat. Where two primitives come close together, the smooth-min operator blends their distance fields, creating the organic merging and separating behavior characteristic of metaball graphics. The program is named for the sphere-tracing ray marching algorithm introduced by John Hart in 1989, though the FPGA implementation evaluates the 2D distance field directly rather than iterating rays.

At conservative settings — moderate smoothness, low animation speed — Marcher produces gently drifting organic shapes with subtle boundary glow. At extreme settings, the primitives merge into a single churning mass surrounded by dense contour rings and lit by a rapidly orbiting light source.

---

## Quick Start

1. **Palette and toggles are linked**: Because palette bits overlap with Render Mode and Primitive Mix, some palette colors are only available in specific render/mix configurations. Explore all 8 positions to find the combinations you want.
2. **Smooth-min at moderate k is most interesting**: Very low smoothness gives hard unions; very high creates a featureless blob. The sweet spot is where shapes visibly stretch toward each other before merging.
3. **Light rotation adds depth**: Even slow light rotation (10–20%) dramatically changes the perception of dimensionality. Stationary light makes the output look flat.

---

## Background

### Signed Distance Fields

A **signed distance field** (SDF) assigns every point in space a signed scalar value: the minimum distance to the nearest surface, negative inside and positive outside. For a circle of radius $r$ centered at $(cx, cy)$, the SDF at point $(x, y)$ is $d = \|\mathbf{p} - \mathbf{c}\| - r$. For a box with half-widths $(sx, sy)$, the SDF is $d = \max(|x - cx| - sx, |y - cy| - sy)$. The zero-crossing of the field defines the surface boundary. SDFs are the foundation of modern procedural graphics — Shadertoy, demoscene intros, and game engines all use them extensively because they compose elegantly: the union of two SDFs is simply $\min(d_1, d_2)$.

### Smooth Union (Smooth-Min)

The standard union of two distance fields — $\min(d_1, d_2)$ — produces a sharp crease where the two surfaces meet. The **smooth-min** operator replaces this crease with a smooth blend:

$$d_{\text{smooth}} = \min(d_1, d_2) - \frac{h^2}{4k}, \quad h = \max(k - |d_1 - d_2|, 0)$$

The parameter $k$ controls the blend radius. Large $k$ creates wide, blobby merges; small $k$ approaches the hard union. In the FPGA, $k$ is derived from the Smoothness pot and the correction term $h^2/(4k)$ is approximated via bit shifts to avoid division. Marcher cascades five smooth-min operations to combine all six primitives into a single composite field.

### Distance-Based Shading

Once the composite SDF is computed, Marcher derives shading from the distance value itself. Pixels inside the surface (negative distance) are shaded proportionally to penetration depth — darker the deeper inside. Pixels on the boundary (near-zero distance) receive a bright edge glow that falls off with distance. Pixels in the exterior (positive distance) display iso-distance contour rings at intervals controlled by the Contour Density pot.

### Lambertian Diffuse Lighting

Marcher estimates the surface normal at each pixel using **central differences** — the gradient of the SDF approximated by comparing the current pixel's distance to its immediate horizontal and vertical neighbours. The dot product of this normal with a DDS-driven rotating light direction produces Lambertian diffuse shading: surfaces facing the light appear bright, surfaces facing away appear dark. The lighting adds dimensionality to what would otherwise be a flat 2D field.

### Toggle Bit Collision

The palette selector, render mode, and primitive mix share bits within `registers_in(6)`. The palette uses bits 2:0 (a 3-bit field giving 8 values), but render mode is also mapped to bit 1 and primitive mix to bit 2. This means changing the palette can simultaneously change the render mode and primitive mix, and vice versa. Only 8 total combinations of these three controls exist, not the 32 (8 × 2 × 2) that independent toggles would provide.


---

## Signal Flow

SDF Evaluation → Smooth Union Cascade → Normal Estimation → Palette + Output Compose

```
Timing Detection ───────────────────────────────────────────────
│   ├─ Pixel counters (hcount, vcount) from timing generator
│   └─ vsync_start triggers per-frame DDS update
│
├── DDS Animation (per-frame at vsync) ─────────────────────────
│   ├─ 6× phase accumulators (coprime freq multipliers)
│   ├─ Position = center + triangle_wave(phase) × scale
│   ├─ s_radius = scale_reg(9:3) + 20  (primitive size)
│   └─ Light angle DDS (triangle_wave → light_dx, light_dy)
│
├── Stage 1: SDF Evaluation (6 primitives) ─────────────────────
│   ├─ i < 4 or Circles mode: circle SDF (Manhattan length − r)
│   ├─ i ≥ 4 and Mixed mode: box SDF (Chebyshev max − r)
│   └─ 6 signed distance values
│
├── Stage 2: Smooth Union Cascade ──────────────────────────────
│   ├─ 5× smooth_min(accumulator, next_primitive)
│   ├─ k = smoothness_reg(9:3), minimum 4
│   ├─ h = max(k − |a−b|, 0)
│   └─ result = min(a,b) − h²>>7
│
├── Stage 3: Normal Estimation + Lighting ──────────────────────
│   ├─ nx = sdf(x) − sdf(x−1),  ny = sdf(y) − sdf(y−1)
│   ├─ N·L = nx×light_dx + ny×light_dy
│   └─ diffuse = clamp(N·L >> 10, 0, 1023)
│
├── Stage 4: Palette + Output Compose ──────────────────────────
│   ├─ Edge glow: bright near |dist| < 8, falloff to 32
│   ├─ Interior: 512 − depth + diffuse/2
│   ├─ Exterior: contour lines (modular distance bands)
│   ├─ 8 palette colour mappings (Neon..Mono)
│   ├─ Contour-only render mode (suppress interior fill)
│   └─ Video mask mode (boundary reveals input video)
│
├── Interpolator Mix (4 clocks) ────────────────────────────────
│   └─ 3× interpolator_u: crossfade delayed input ↔ SDF output
│
├── Sync / Data Delay (8 clocks) ───────────────────────────────
│   └─ Shift registers: hsync, vsync, field, Y, U, V
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ s_bypass selects processed or delayed input
```

All six SDF evaluations and the five-stage smooth-union cascade are evaluated combinationally within a single clock cycle in the VHDL. The normal estimation uses previous-pixel and previous-line SDF values as finite-difference approximations — a cheap shortcut that produces adequate normals for diffuse shading despite being only a single-sample gradient. The palette and render mode interact through the shared toggle register, meaning the 8 palette selections implicitly include render mode and primitive mix states. The video mask feature replaces the SDF output with the input video signal wherever the distance is near zero (within 32 pixels of the boundary), creating a "window" effect where the SDF boundary reveals the live input.

---

## Parameter Reference

<img src={marcher_control_panel} alt="Videomancer front panel with Marcher loaded"/>
*Videomancer's front panel with Marcher active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Animation Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the orbital velocity of all six SDF primitives. The register value is used as the base DDS increment. Each primitive multiplies this base by a different coprime factor (2, 5, 8, 11, 14, 17 for X; 3, 8, 13, 18, 23, 28 for Y), so increasing Animation Speed accelerates all orbits proportionally while preserving their relative phase relationships. At 0%, the primitives freeze in place. At maximum, they orbit rapidly, creating fast-evolving fluid shapes.

---

#### Knob 2 — Smoothness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At low values, primitives merge only when they overlap directly — the boundary between touching shapes is a sharp crease. As Smoothness increases, the blend zone widens: shapes begin to stretch toward each other before contact, creating blobby, organic connections. At maximum, the entire field becomes a single soft mass. The register's upper bits become $k$ (minimum 4), so very low settings still produce some blending. Internally, controls the blend radius ($k$) of the smooth-union operator that merges primitive distance fields.

---

#### Knob 3 — Primitive Scale
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls both the size of the SDF primitives and the amplitude of their orbital paths. The effective radius is `scale_reg(9:3) + 20`, giving a range of approximately 20 to 147 pixels. Larger primitives overlap more, creating more merging events. The orbital amplitude also scales with this value — larger primitives orbit in wider paths, covering more of the screen. At minimum, small shapes trace tight circles near the center; at maximum, large shapes sweep across the full frame.

---

#### Knob 4 — Contour Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the spacing of iso-distance contour lines rendered in the exterior region (where the SDF is positive). The register controls which bits of the distance value are used for the contour modulo operation. At low values, contour lines are widely spaced — only a few rings surround the shapes. At high values, dense contour rings pack tightly around the boundary, creating a topographic-map appearance. In contour-only render mode (Render Mode toggle), these rings are the primary visual output.

---

#### Knob 5 — Light Rotation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the angular velocity of the orbiting light source. The light direction is computed from a DDS triangle wave — effectively a point light circling the scene. At 0%, the light is stationary and shading is fixed. As the value increases, the light orbits faster, creating dynamic shadows that sweep across the SDF surfaces. The light direction is a 2D vector derived from two triangle waves in quadrature, producing circular motion.

---

#### Knob 6 — Edge Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the intensity of the boundary edge glow. When the SDF value is near zero (within 8 pixels of the surface), pixels receive full edge brightness. The glow falls off in steps: half brightness at distance 8–15, quarter at 16–31, and none beyond 32. At maximum, the edge glow creates bright halos around every shape boundary. At low values, the edges are subtle and the interior/exterior shading dominates.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Neon | Mono |
| **8 — Render Mode** | Surface | Contour |
| **9 — Primitive Mix** | Circles | Mixed |
| **10 — Video Mask** | Off | On |
| **11 — Bypass** | Off | On |

The first three toggles (Palette, Render Mode, Primitive Mix) share bits in `registers_in(6)`. Palette reads bits 2:0 as a 3-bit value giving 8 palette selections. Render Mode reads bit 1 and Primitive Mix reads bit 2 — these overlap with palette bits 1 and 2 respectively. This means changing the palette also changes the render mode and primitive mix. Only 8 unique combinations exist across all three controls, not the 32 that fully independent toggles would provide. Video Mask and Bypass are on separate bits (3 and 4) and function independently.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the delayed input and the SDF rendered output via three `interpolator_u` instances. At 0% (register 0), the output is the delayed input — no SDF visible. At 100% (register 1023), the output is fully the rendered distance field. Intermediate values superimpose the SDF rendering over the input video with controllable opacity, useful for subtle overlay effects or for layering the SDF pattern on a live camera feed.





---

## Guided Exercises

These exercises progress from observing the raw distance field to exploring smooth merging, lighting dynamics, and palette variations.

### Exercise 1: Basic SDF Shapes

<img src={marcher_exercise1_result} alt="Basic SDF Shapes result"/>
*Basic SDF Shapes — simulated result across source images.*
**What You'll Create**: Understand the fundamental SDF rendering — interior shading, edge glow, and exterior contour rings.

1. **Slow down**: Set Animation Speed to ~10%. The primitives nearly freeze, allowing careful observation.
2. **Observe three zones**: Note the three visually distinct regions: bright edge glow at surface boundaries, darker shading inside shapes, and contour rings in the exterior.
3. **Edge Brightness**: Sweep Edge Brightness from 0% to 100%. Watch the boundary halos grow from invisible to dominant.
4. **Contour Density**: Increase Contour Density. Watch exterior contour rings pack more densely around each shape.
5. **Primitive Scale**: Sweep from minimum to maximum. Small primitives are well-separated; large ones overlap and merge.
6. **Contour mode**: Select a palette that triggers Contour render mode (e.g., toggle to see outlines only). The interior disappears, leaving thin boundary traces.

**Key concepts**: SDF value is negative inside, zero at boundary, positive outside; edge glow falls off in discrete steps (8, 16, 32 pixels); contour lines are modular-distance bands in the exterior

---

### Exercise 2: Smooth Merging

<img src={marcher_exercise2_result} alt="Smooth Merging result"/>
*Smooth Merging — simulated result across source images.*
**What You'll Create**: Explore how the smooth-union operator creates organic shape blending.

1. **Hard union**: Set Smoothness to minimum. Shapes that overlap show creased boundaries — hard unions with no blending.
2. **Gradual blend**: Slowly increase Smoothness. Watch the creases soften. Shapes begin to stretch toward each other before making contact.
3. **Maximum blob**: At maximum Smoothness, all six primitives merge into a single undulating mass. The individual shapes are no longer distinguishable.
4. **Speed interaction**: Increase Animation Speed to ~40%. The merging and separating cycle becomes visible as primitives orbit past each other.
5. **Scale interaction**: Reduce Primitive Scale to ~25%. Smaller shapes must come closer together before the smooth blend zone takes effect, creating brief, transient connections.
6. **Palette sweep**: Cycle through palettes to see how different color mappings reveal or hide the blending zones.

**Key concepts**: Smooth-min blend radius k controls how far the blending effect extends, larger k creates blobby organic shapes, small k approaches hard min union, the correction term h²/4k is approximated via bit shifts

---

### Exercise 3: Dynamic Lighting and Video Mask

<img src={marcher_exercise3_result} alt="Dynamic Lighting and Video Mask result"/>
*Dynamic Lighting and Video Mask — simulated result across source images.*
**What You'll Create**: Explore the orbiting light source and the video mask feature that uses SDF boundaries as a dynamic stencil.

1. **Light in motion**: Set Light Rotation to ~50%. Watch the diffuse shading sweep across the SDF surfaces as the light orbits.
2. **Fast light**: Increase to ~80%. The rapid light rotation creates a strobing effect across the interior surfaces.
3. **Stationary light**: Set to 0%. Observe fixed shading — some primitives face the light (bright) while others face away (dark).
4. **Video mask**: Enable Video Mask. The SDF boundaries now reveal the input video signal. The organic shape edges become windows into the underlying live feed.
5. **Animate with mask**: Increase Animation Speed. The windows move with the SDF shapes, creating a dynamic stencil reveal effect across the input.
6. **Mix overlay**: Reduce Mix to ~60% while Video Mask is On. The SDF stencil blends with the input, creating a layered composite.

**Key concepts**: Central-difference normal estimation approximates the SDF gradient, Lambertian N·L shading adds dimensionality, video mask reveals input at near-zero distance regions, distance threshold is 32 pixels

---


## Tips

- **Video mask for compositing**: Video Mask turns the SDF into a dynamic matte or stencil. Feed interesting footage through the input while the SDF boundaries reveal it — useful for live performance.
- **Edge Brightness and Contour Density define the exterior**: The interior is depth-shaded automatically, but the exterior appearance depends almost entirely on these two controls.
- **Six coprime velocities**: The primitives never repeat the same arrangement because their DDS increments are pairwise coprime. The pattern is effectively infinite in variation.
- **Boxes add structure**: In Mixed mode, the two box primitives (Chebyshev SDF) introduce rectangular elements that create interesting visual tension against the four circular primitives when smooth blending is active.
- **Downstream chaining**: Route Marcher's output into a Warp or Color program. The sharp edge glow lines and organic shapes provide strong compositional anchors for further processing.

---

## Glossary

| Term | Definition |
|------|------------|
| **Central differences** | A finite-difference method for estimating gradients by comparing a function's value at adjacent sample points. |
| **Chebyshev distance** | The maximum of the absolute axis differences; produces square-shaped SDF contours for box primitives. |
| **DDS** | Direct Digital Synthesis; generates periodic waveforms from a phase accumulator and lookup/approximation function. |
| **Lambertian** | A shading model where surface brightness equals the dot product of the surface normal and light direction, clamped to non-negative values. |
| **Manhattan distance** | The sum of absolute differences along each axis; used in Marcher's circle SDF length approximation. |
| **Metaball** | A graphics technique where implicit surfaces merge smoothly, producing organic blob-like shapes. Marcher's smooth union achieves the same visual effect. |
| **SDF** | Signed Distance Field; a scalar field where each point holds the signed distance to the nearest surface (negative inside, positive outside). |
| **Smooth-min** | An operator that blends two distance values smoothly instead of taking a hard minimum, parameterised by blend radius $k$. |
| **Triangle wave** | A piecewise-linear approximation of a sine wave used for DDS position computation — cheaper than a LUT on iCE40. |

---
