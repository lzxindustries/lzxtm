---
draft: true
sidebar_position: 4
slug: /instruments/videomancer/amoeba
title: "Amoeba"
image: /img/instruments/videomancer/amoeba/amoeba_hero.png
description: "Amoeba is a metaball isosurface engine."
---

import amoeba_hero from '/img/instruments/videomancer/amoeba/amoeba_hero.png';
import amoeba_animation from '/img/instruments/videomancer/amoeba/amoeba_animation.gif';
import amoeba_control_panel from '/img/instruments/videomancer/amoeba/amoeba_control_panel.png';
import amoeba_exercise1_result from '/img/instruments/videomancer/amoeba/amoeba_exercise1_result.gif';
import amoeba_exercise2_result from '/img/instruments/videomancer/amoeba/amoeba_exercise2_result.gif';
import amoeba_exercise3_result from '/img/instruments/videomancer/amoeba/amoeba_exercise3_result.gif';

# Amoeba

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={amoeba_hero} alt="Amoeba hero image"/>
*Amoeba rendering two Lissajous-orbit metaballs in rainbow mode — the blobs merge and split organically as their orbits intersect, with bright skin outlines tracing the isosurface boundary.*
<img src={amoeba_animation} alt="Amoeba animated output"/>
*Amoeba output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Amoeba is a metaball isosurface engine. Up to two animated blobs orbit the screen center on independent Lissajous curves, and for every pixel the program computes the cumulative field potential — the sum of inverse-square distance contributions from each active blob center. The resulting scalar field is classified into three zones: inside (field above threshold), skin (field within a configurable band below threshold), and outside (field below the skin boundary). Each zone is colored differently, producing the characteristic metaball visual: discrete circles that smoothly merge into organic shapes as they approach one another.

The name *Amoeba* describes the visual result exactly. A single-celled amoeba has no fixed shape — its membrane deforms and extends pseudopods as internal forces push it outward. Metaballs behave the same way: when two blob fields overlap, the isosurface between them bulges outward and merges, creating a bridge that looks like a cell dividing in reverse. Reduce the threshold and the blobs separate into independent circles; increase it and they fuse into a single amorphous mass.

At conservative settings — a single blob, slow speed, wide skin — the screen shows a cleanly defined circle gliding across the frame. At extreme settings — two blobs, high speed, narrow skin, rainbow colour, outline enabled — the metaball boundaries trace rapidly evolving organic contours in vivid colour against a black background, creating complex abstract patterns reminiscent of lava-lamp fluid dynamics or microscope footage of living cells.

---

## Quick Start

1. **Blob Size and Threshold are the primary shape controls**: Blob Size determines the field radius, Threshold determines where the boundary is drawn. A large blob size with a low threshold produces well-separated circles. A large blob size with a high threshold produces merged amorphous shapes.
2. **Speed = 0 freezes the animation**: Set Speed to 0% to stop all blob motion and use the static metaball pattern as a fixed overlay.
3. **Outline + Hollow = vector graphics**: This combination strips the metaballs down to pure contour lines on black — clean line art that traces the isosurface boundary.

---

## Background

### What Are Metaballs?

**Metaballs** are a technique from computer graphics for modeling soft, organic shapes. Each metaball is defined by a center point and a field function — typically an inverse-square or inverse-power-of-distance function that produces a large value near the center and falls off rapidly with distance. At any point in space, the total field is the sum of contributions from all nearby metaballs. An isosurface is drawn at a chosen threshold value: points where the total field exceeds the threshold are "inside" the surface, and points where it falls below are "outside."

The defining characteristic of metaballs is their merging behaviour. When two metaballs are far apart, each produces an independent circular (or spherical, in 3D) isosurface. As they approach each other, the overlapping fields add together, causing the isosurface to bulge outward between them. At a critical proximity, the two surfaces bridge and merge into a single continuous shape. This produces the smooth, fluid merging and splitting that makes metaballs look organic rather than geometric.

In this program, the field function is implemented as a 32-entry lookup table mapping $d_{scaled}^2$ (the scaled squared distance from pixel to blob center) to a 10-bit field contribution. The LUT is initialized as $f(i) = \min(2048 / (i + 1), 1023)$, which approximates an inverse-square falloff with saturation near the center.

### What Are Lissajous Curves?

A **Lissajous curve** is the path traced by a point whose X and Y coordinates oscillate sinusoidally at different frequencies. If the X frequency is $f_x$ and the Y frequency is $f_y$, the resulting path depends on the frequency ratio $f_x : f_y$. A 1:1 ratio produces an ellipse (or circle, or line, depending on phase). A 1:2 ratio produces a figure-eight. Other ratios produce more complex curves — the higher the ratio integers, the more intricate the path.

In this program, each of the two blobs has a fixed frequency ratio that determines its orbital path:

| Blob | X freq | Y freq | Ratio | Path character |
|------|--------|--------|-------|---------------|
| 0 | 1 | 2 | 1:2 | Figure-eight |
| 1 | 3 | 1 | 3:1 | Three-lobed horizontal |

The speed parameter controls the phase increment per frame, applied to both blobs simultaneously. Because each blob's X and Y phase accumulators are multiplied by different frequency constants, the two blobs evolve along different paths at the same base rate, creating organic and unpredictable merge/split patterns when the orbits bring their centers close together.

### What Is Isosurface Classification?

In a scalar field, an **isosurface** is the set of all points where the field has a particular value. For 2D metaballs, this is more precisely an isoline — a contour line at the threshold level. Points are classified into three zones:

- **Inside**: field value ≥ threshold. These points are within the metaball body.
- **Skin**: field value between (threshold − skin_width) and threshold. These points form a band around the isosurface boundary.
- **Outside**: field value < (threshold − skin_width). These points are in empty space.

The skin zone is what gives metaballs their visible boundary. Without it, there is only a binary inside/outside distinction. By controlling the skin width, the user adjusts how wide the transition band is around the metaball surface — a wide skin produces soft, glowing edges; a narrow skin produces sharp contour lines.

### What Is the Inverse-Square Field Function?

The **inverse-square law** describes quantities that decrease with the square of the distance from a source — gravity, electric field strength, and light intensity all follow this relationship. For metaballs, the field function $f(r) = k / r^2$ produces a strong contribution near the blob center that falls off rapidly with distance. This gives each blob a well-defined "zone of influence" that extends only a few multiples of its effective radius.

The program implements this function as a precomputed lookup table indexed by the scaled squared distance. The squared distance is computed directly from the pixel-to-center offsets (avoiding the need for a square root), shifted right by a configurable amount based on the Blob Size parameter. Larger blob sizes shift less (producing a wider field), smaller sizes shift more (concentrating the field close to the center).


---

## Signal Flow

```
┌──────────────────────────────────────────────────────────────────┐
│  Vblank Computation (blob center update)                         │
│                                                                  │
│  1. Phase Accumulator Update                                     │
│     ├─ For each blob: phase_x += speed × freq_x                 │
│     ├─ For each blob: phase_y += speed × freq_y                 │
│     └─ 16-bit wrapping → smooth continuous orbits                │
│           ◄── Speed (pot 3)                                      │
│                                                                  │
│  2. Blob Center Computation (5 phases per blob, sequential)      │
│     ├─ Phase 0: Sine X lookup → register                        │
│     ├─ Phase 1: Multiply X → register; Sine Y lookup → register │
│     ├─ Phase 2: cx = mult_x >> 4 + 640; Multiply Y → register   │
│     ├─ Phase 3: cy = mult_y >> 4 + 360                            │
│     └─ Phase 4: Advance to next blob or finish                  │
│           ◄── Blob Size (pot 1), Count (pot 6)                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Active Video Pipeline (15 clocks total)                         │
│                                                                  │
│  Input Video (YUV 4:4:4 30-bit)                                  │
│  │                                                               │
│  ├─ Stage A (1 clk): Subtract + absolute value                   │
│  │   └─ dx[i] = |h_count - cx[i]|, dy[i] = |v_count - cy[i]|   │
│  │       (both blobs in parallel, truncated to 6 bits via >>5)   │
│  │                                                               │
│  ├─ Stage B (1 clk): Square multiply (6×6)                       │
│  │   └─ dx_sq[i] = dx[i]², dy_sq[i] = dy[i]²                   │
│  │       (both blobs in parallel)                                │
│  │                                                               │
│  ├─ Stage C1 (1 clk): Sum                                        │
│  │   └─ dist[i] = dx_sq[i] + dy_sq[i]                           │
│  │       (both blobs in parallel)                                │
│  │                                                               │
│  ├─ Stage C2 (1 clk): Dynamic shift + clamp                      │
│  │   ├─ index[i] = dist[i] >> blob_size[9:7]                    │
│  │   └─ clamp index to [0, 31]                                  │
│  │         ◄── Blob Size (pot 1)                                 │
│  │                                                               │
│  ├─ Stage D (1 clk): 1/d² LUT lookup                             │
│  │   └─ contrib[i] = C_INV_SQ[index[i]]  (32:1 mux)            │
│  │                                                               │
│  ├─ Stage E1 (1 clk): Accumulate + normalize                     │
│  │   ├─ field = Σ contrib[i] for active blobs                   │
│  │   └─ field_norm = clamp(field, 0, 1023)                      │
│  │                                                               │
│  ├─ Stage E1b (1 clk): Classification                            │
│  │   └─ Classify: inside/skin/outside vs threshold               │
│  │         ◄── Threshold (pot 2), Skin Width (pot 4)             │
│  │                                                               │
│  ├─ Stage E2 (1 clk): Color mapping                              │
│  │   └─ Map zone + parameters → Y/U/V                           │
│  │         ◄── Hue Shift (pot 5), Fill Mode (toggle 7),          │
│  │             Color (toggle 8), Source (toggle 9),              │
│  │             Outline (toggle 10)                               │
│  │                                                               │
│  ├── Interpolator (4 clocks per Y/U/V)                           │
│  │   └─ Mix = lerp(input_delayed, generated, mix_amount)         │
│  │         ◄── Mix (fader 12)                                    │
│  │                                                               │
│  └── Pipeline overhead (3 clocks)                                │
│                                                                  │
│  Bypass: select delayed input or mix result                      │
│           ◄── Bypass (toggle 11)                                 │
└──────────────────────────────────────────────────────────────────┘
```

The processing divides cleanly into two phases. During vertical blanking, a sequential state machine cycles through both blobs (5 clock phases each) to compute their center positions using the quarter-wave sine LUT — this requires 10 clocks total, well within the blanking interval. During active video, the per-pixel field evaluation pipeline runs at full pixel rate, computing both blob contributions in parallel across eight pipeline stages (A, B, C1, C2, D, E1, E1b, E2).

The field evaluation achieves full parallelism by maintaining two independent signal paths through Stages A–D. Each path computes the absolute offset, squares it, shifts it based on Blob Size, and performs the LUT lookup independently. Only in Stage E1 do the two contributions converge into a single accumulated field value for classification.

The 1/d² LUT provides a critical optimization: instead of performing a division per blob per pixel (which would be prohibitively expensive in the iCE40), the squared distance is used directly as an index into a precomputed 32-entry table. The Blob Size parameter's upper 3 bits control how many bits of right-shift are applied before the LUT lookup, effectively scaling the field radius without changing the LUT contents.

---

## Parameter Reference

<img src={amoeba_control_panel} alt="Videomancer front panel with Amoeba loaded"/>
*Videomancer's front panel with Amoeba active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Blob Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At low values, the field evaluation right-shift is large, concentrating each blob's field contribution into a small area around its center — the blobs appear as small circles and must approach very closely before their fields overlap enough to merge. At high values, the field extends much farther from each center, producing larger circles that merge at greater separation distances. The orbit amplitude also scales with this parameter — larger blobs swing across a wider area of the frame, smaller blobs orbit near the center. The upper 3 bits of the register select the distance shift (0–7), providing 8 discrete size steps within the continuous pot range. Internally, controls the spatial extent of each blob's field and the amplitude of its orbital path simultaneously.

---

#### Knob 2 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

At low threshold values, only pixels very close to a blob center reach the threshold — the visible shapes are small, tightly defined circles. At high threshold values, the field needs less contribution to qualify as "inside," so the shapes appear larger and merge at greater distances. The threshold interacts directly with Blob Size: a large blob size with a low threshold produces defined circles, while a large blob size with a high threshold produces a single amorphous merged mass. The threshold value is compared against the 12-bit accumulated field total from all active blobs. Internally, sets the isosurface threshold that defines the inside/skin/outside classification boundary.

---

#### Knob 3 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

At 0%, the blobs are frozen in position — their phase accumulators do not increment, and the metaball pattern is static. As speed increases, the Lissajous orbits evolve more rapidly. At maximum, the blobs trace their orbital paths quickly, creating rapid merge/split activity. Because each blob has a different Lissajous frequency ratio, the same speed value produces different apparent velocities — blob 0 (1:2 ratio) traces a figure-eight in the time blob 1 (3:1 ratio) traces a three-lobed horizontal path. Internally, controls the rate at which both blob phase accumulators advance per frame.

---

#### Knob 4 — Skin Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

At 0%, the skin band has zero width — there is only inside and outside, with no visible edge transition. As skin width increases, a wider band of pixels is classified as "skin" rather than "outside," producing a broader visible edge around each metaball. With outline enabled, the skin zone renders as a bright contour line; without outline, it renders at the raw field-normalized brightness, creating a soft glow around the shape boundary. The skin width value is right-shifted by 2 bits before being subtracted from the threshold. Internally, controls the width of the skin classification band below the isosurface threshold.

---

#### Knob 5 — Hue Shift
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

Rotates the chroma components of the generated output. At 0°, the hue-shifted U and V values are at their neutral position. Rotating through 360° cycles through the colour spectrum. This parameter only has visible effect when Color is set to Rainbow — in Mono mode, all generated chroma is at midpoint regardless of hue shift. In Rainbow mode, the hue shift offsets the base U/V mapping derived from the field value, and when Outline is enabled, the skin zone uses the hue shift directly as its U value with the inverse as V, producing a coloured contour line.

---

#### Knob 6 — Count
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Selects how many blobs are active in the field computation: 1 or 2. The control operates in boolean mode — below the midpoint selects one blob, above selects two. With one blob, the output is a single circle (or circle with skin) orbiting the center on a figure-eight path. With two, merge/split events occur when the two orbital paths bring the blobs close together, creating the characteristic metaball merging behaviour.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Fill Mode** | Solid | Hollow |
| **8 — Color** | Mono | Rainbow |
| **9 — Source** | Synth | Video |
| **10 — Outline** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control **independent binary options** with no combined selector logic. Fill Mode, Color, Source, and Outline interact to create a wide range of visual styles — solid monochrome fills, hollow outlines, rainbow-tinted interiors, video-keyed shapes, and coloured contour lines. Bypass routes the delayed input directly to output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original input video (delayed to match the 15-clock processing pipeline) and the metaball-generated output. At 0%, the output is pure unprocessed input — no metaballs are visible. At 100%, the output is the fully generated metaball scene. Intermediate positions blend the two, allowing the metaball shapes to be superimposed over the source footage at any opacity. In Video source mode, this creates a partial keying effect where the metaball boundaries are visible but semi-transparent.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from a single stationary blob through multi-blob merging dynamics to full-featured video-keyed metaball compositions.

### Exercise 1: Single Blob Anatomy

<img src={amoeba_exercise1_result} alt="Single Blob Anatomy result"/>
*Single Blob Anatomy — simulated result across source images.*
**What You'll Create**: Understand the three-zone classification system (inside/skin/outside) and how threshold and skin width define the metaball boundary.

1. **Single blob**: Set Count (Knob 6) to 1. Set Speed (Knob 3) to ~10% (slow drift). Set Mix at 100%, Bypass off.
2. **Large blob**: Set Blob Size (Knob 1) to ~60%. A single circle drifts slowly on a figure-eight path.
3. **Observe threshold effect**: Start with Threshold (Knob 2) at ~20%. The visible circle is small. Slowly increase threshold — the circle grows as more pixels exceed the threshold level. At maximum, nearly the entire screen is "inside."
4. **Observe skin width**: Set Threshold to ~40%. Set Skin Width (Knob 4) to ~10%. A thin band of intermediate brightness surrounds the solid interior. Increase Skin Width to ~80% — the band widens into a broad gradient halo.
5. **Enable outline**: Toggle Outline (Toggle 10) on. The skin band becomes a bright white contour line. A narrow skin width produces a sharp outline; a wide skin width produces a thick glowing border.
6. **Hollow mode**: Toggle Fill Mode (Toggle 7) to Hollow. The interior becomes black. Only the skin zone (the outline contour) is visible — a clean bright ring tracing the isosurface.
7. **Freeze and examine**: Set Speed to 0%. The blob stops. Examine the zones at leisure.

**Key concepts**: Isosurface threshold defines shape size, skin width defines edge band, outline converts gradient to bright contour, hollow removes interior fill, zones are inside/skin/outside

---

### Exercise 2: Splitting and Merging

<img src={amoeba_exercise2_result} alt="Splitting and Merging result"/>
*Splitting and Merging — simulated result across source images.*
**What You'll Create**: Observe metaball merging and splitting behaviour with two blobs, and understand how the isosurface boundary deforms as the blobs approach and separate.

1. **Two blobs**: Set Count (Knob 6) to 2. Set Speed to ~35%, Blob Size to ~55%, Threshold to ~35%. Enable Outline (Toggle 10) so the isosurface boundary is clearly visible.
2. **Watch for merge events**: The two blobs orbit on different Lissajous paths (blob 0 traces a figure-eight, blob 1 a three-lobed curve). When their paths bring them close together, the outlines bulge outward toward each other and eventually bridge into a single continuous contour.
3. **Observe the split**: As the blobs separate, the bridge between them narrows into a thin neck. The neck pinches and snaps apart, restoring two independent circles. This merge-split cycle repeats every time the orbits cross.
4. **Increase threshold**: Raise Threshold to ~55%. The blobs merge at greater distances — the combined field exceeds the threshold even when the centers are far apart. The shapes stay merged for longer portions of the orbit.
5. **Decrease threshold**: Lower Threshold to ~20%. The blobs must be nearly overlapping before their fields combine enough to merge. They appear as independent circles most of the time.
6. **Rainbow colour**: Switch Color (Toggle 8) to Rainbow and set Hue Shift (Knob 5) to ~60°. The field gradient becomes visible as a warm colour ramp inside each blob — during merges, the colour gradients blend where the fields overlap, revealing how the two contributions combine.

**Key concepts**: Metaball merging from overlapping inverse-square fields, isosurface boundary deformation during approach, threshold controls merge distance, outline makes boundary shape changes clearly visible

---

### Exercise 3: Hollow Rainbow Contours

<img src={amoeba_exercise3_result} alt="Hollow Rainbow Contours result"/>
*Hollow Rainbow Contours — simulated result across source images.*
**What You'll Create**: Create pure vector-style contour line graphics using hollow fill mode with rainbow colour, producing bright organic outlines on a black background.

1. **Hollow outline setup**: Set Fill Mode (Toggle 7) to Hollow and enable Outline (Toggle 10). The blob interiors are black — only the skin-zone contour lines are visible.
2. **Configure shapes**: Count to 2, Blob Size to ~55%, Threshold to ~35%, Speed to ~20%, Skin Width to ~30%.
3. **Rainbow contours**: Switch Color (Toggle 8) to Rainbow. Set Hue Shift (Knob 5) to ~270°. The contour lines are now rendered in cool purple-blue tones that shift with the field gradient.
4. **Observe contour merging**: Watch as the two hollow outlines drift on their Lissajous paths. When they approach, their contours bulge and connect — but the interior remains black, so only the merged boundary line is visible. This produces clean topological transitions.
5. **Rotate hue**: Slowly rotate Hue Shift through 360°. The contour colour cycles through the full spectrum while the geometry stays constant — the line art changes palette without changing shape.
6. **Widen skin**: Increase Skin Width to ~60%. The contour lines thicken into broad glowing bands, creating a neon-tube aesthetic. Decrease to ~10% for razor-thin lines.
7. **Compare with solid**: Switch Fill Mode back to Solid to see the filled version of the same shapes. The hollow contour mode strips away the interior, leaving only the boundary — useful for overlaying on other video content via mix.

**Key concepts**: Hollow mode for pure contour graphics, rainbow colour maps field gradient to hue, skin width controls line thickness, outline converts gradient band to bright contour, hue shift rotates colour palette

---


## Tips

- **Video source turns metaballs into dynamic masks**: In Video mode, the blob shapes become windows into the input signal. Two blobs reveal different parts of the frame simultaneously.
- **Skin Width controls edge character**: Narrow skin = sharp boundaries. Wide skin = soft glowing edges. At zero skin width, there is no visible transition zone.
- **Rainbow mode reveals field topology**: In Rainbow mode, the chroma is driven by the field value, so you can see the field strength gradient even within the "inside" zone — useful for understanding how the fields of different blobs combine.
- **Count toggles between solo and duo**: With one blob, the output is a clean orbiting circle. With two, merge/split events add organic complexity as the Lissajous paths cross.
- **Feedback loops create fractal-like patterns**: Routing the output back to the input seed causes the metaball shapes to feed into themselves, creating recursive patterns especially visible in Video source mode.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chroma** | The colour components (U and V) of a YUV video signal, encoding hue and saturation independently of brightness. |
| **Inverse-Square Law** | A mathematical relationship where a quantity decreases proportionally to the square of the distance from a source; used here for the metaball field function. |
| **Isosurface** | The set of all points in a scalar field where the field equals a chosen threshold value; in 2D this is an isoline (contour) dividing inside from outside. |
| **Lissajous Curve** | A parametric path traced when X and Y coordinates oscillate sinusoidally at different frequencies; the frequency ratio determines the curve's shape (figure-eight, three-lobed, etc.). |
| **LUT (Lookup Table)** | A precomputed array that maps an input index to an output value, replacing expensive runtime computation with a single memory read. |
| **Metaball** | A computer-graphics technique for rendering soft organic shapes by summing inverse-distance field contributions from point sources and drawing an isosurface at a chosen threshold. |
| **Phase Accumulator** | A register that increments by a fixed step each frame, wrapping at overflow to produce a continuously advancing angle for sine-wave orbit generation. |
| **Scalar Field** | A function that assigns a single numeric value to every point in a 2D space; in Amoeba, the field value at each pixel is the sum of all active blob contributions. |
| **Skin Zone** | The classification band between the isosurface threshold and the outer boundary, rendered as a visible edge or contour around each metaball. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
