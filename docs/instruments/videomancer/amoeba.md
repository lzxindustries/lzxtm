---
draft: false
sidebar_position: 6
slug: /instruments/videomancer/amoeba
title: "Amoeba"
---

import amoeba_hero from '/img/instruments/videomancer/amoeba/amoeba_hero.png';
import amoeba_animation from '/img/instruments/videomancer/amoeba/amoeba_animation.gif';
import amoeba_exercise1_result from '/img/instruments/videomancer/amoeba/amoeba_exercise1_result.gif';
import amoeba_exercise2_result from '/img/instruments/videomancer/amoeba/amoeba_exercise2_result.gif';
import amoeba_exercise3_result from '/img/instruments/videomancer/amoeba/amoeba_exercise3_result.gif';

# Amoeba

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={amoeba_hero} alt="Amoeba rendering four Lissajous-orbit metaballs in rainbow mode — the blobs merge and split organically as their orbits intersect, with bright skin outlines tracing the isosurface boundary"/>

<img src={amoeba_animation} alt="Amoeba output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source"/>

*Amoeba output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

<details>
<summary>Hero image settings</summary>

| Control | Value |
|---------|-------|
| Blob Size | ~55% |
| Threshold | ~40% |
| Speed | ~20% |
| Skin Width | ~25% |
| Hue Shift | ~120° |
| Count | 4 |
| Fill Mode | Solid |
| Color | Rainbow |
| Source | Synth |
| Outline | On |
| Bypass | Off |
| Mix | ~100% |

</details>

---

## Overview

Amoeba is a metaball isosurface engine. Four animated blobs orbit the screen center on independent Lissajous curves, and for every pixel the program computes the cumulative field potential — the sum of inverse-square distance contributions from each active blob center. The resulting scalar field is classified into three zones: inside (field above threshold), skin (field within a configurable band below threshold), and outside (field below the skin boundary). Each zone is colored differently, producing the characteristic metaball visual: discrete circles that smoothly merge into organic shapes as they approach one another.

The name *Amoeba* describes the visual result exactly. A single-celled amoeba has no fixed shape — its membrane deforms and extends pseudopods as internal forces push it outward. Metaballs behave the same way: when two blob fields overlap, the isosurface between them bulges outward and merges, creating a bridge that looks like a cell dividing in reverse. Reduce the threshold and the blobs separate into independent circles; increase it and they fuse into a single amorphous mass.

At conservative settings — one or two blobs, slow speed, wide skin — the screen shows cleanly defined circles gliding across the frame. At extreme settings — four blobs, high speed, narrow skin, rainbow colour, outline enabled — the metaball boundaries trace rapidly evolving organic contours in vivid colour against a black background, creating complex abstract patterns reminiscent of lava-lamp fluid dynamics or microscope footage of living cells.

---

## Background

### What Are Metaballs?

**Metaballs** are a technique from computer graphics for modeling soft, organic shapes. Each metaball is defined by a center point and a field function — typically an inverse-square or inverse-power-of-distance function that produces a large value near the center and falls off rapidly with distance. At any point in space, the total field is the sum of contributions from all nearby metaballs. An isosurface is drawn at a chosen threshold value: points where the total field exceeds the threshold are "inside" the surface, and points where it falls below are "outside."

The defining characteristic of metaballs is their merging behaviour. When two metaballs are far apart, each produces an independent circular (or spherical, in 3D) isosurface. As they approach each other, the overlapping fields add together, causing the isosurface to bulge outward between them. At a critical proximity, the two surfaces bridge and merge into a single continuous shape. This produces the smooth, fluid merging and splitting that makes metaballs look organic rather than geometric.

In this program, the field function is implemented as a 256-entry lookup table mapping $d_{scaled}^2$ (the scaled squared distance from pixel to blob center) to a 10-bit field contribution. The LUT is initialized as $f(i) = \min(16384 / (i + 1), 1023)$, which approximates an inverse-square falloff with saturation near the center.

### What Are Lissajous Curves?

A **Lissajous curve** is the path traced by a point whose X and Y coordinates oscillate sinusoidally at different frequencies. If the X frequency is $f_x$ and the Y frequency is $f_y$, the resulting path depends on the frequency ratio $f_x : f_y$. A 1:1 ratio produces an ellipse (or circle, or line, depending on phase). A 1:2 ratio produces a figure-eight. Other ratios produce more complex curves — the higher the ratio integers, the more intricate the path.

In this program, each of the four blobs has a fixed frequency ratio that determines its orbital path:

| Blob | X freq | Y freq | Ratio | Path character |
|------|--------|--------|-------|---------------|
| 0 | 1 | 2 | 1:2 | Figure-eight |
| 1 | 3 | 1 | 3:1 | Three-lobed horizontal |
| 2 | 2 | 5 | 2:5 | Complex five-crossing |
| 3 | 5 | 3 | 5:3 | Dense winding |

The speed parameter controls the phase increment per frame, applied to all four blobs simultaneously. Because each blob's X and Y phase accumulators are multiplied by different frequency constants, the four blobs evolve along different paths at the same base rate, creating organic and unpredictable merge/split patterns when two or more orbits bring their centers close together.

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
│  2. Blob Center Computation (4 phases per blob, sequential)      │
│     ├─ Phase 0: present phase_x to sin_cos LUT                  │
│     ├─ Phase 1: read sin → cx = sin × (blob_size/4) / 16 + 640  │
│     ├─ Phase 2: present phase_y to sin_cos LUT                  │
│     ├─ Phase 3: read sin → cy = sin × (blob_size/4) / 16 + 360  │
│     └─ Repeat for all 4 blobs                                   │
│           ◄── Blob Size (pot 1), Count (pot 6)                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Active Video Pipeline (12 clocks total)                         │
│                                                                  │
│  Input Video (YUV 4:4:4 30-bit)                                  │
│  │                                                               │
│  ├─ Stage A (1 clk): Subtract + absolute value                   │
│  │   └─ dx[i] = |h_count - cx[i]|, dy[i] = |v_count - cy[i]|   │
│  │       (all 4 blobs in parallel, truncated to 8 bits)          │
│  │                                                               │
│  ├─ Stage B (1 clk): Square multiply (8×8)                       │
│  │   └─ dx_sq[i] = dx[i]², dy_sq[i] = dy[i]²                   │
│  │       (all 4 blobs in parallel)                               │
│  │                                                               │
│  ├─ Stage C (1 clk): Sum + shift + clamp                         │
│  │   ├─ dist[i] = dx_sq[i] + dy_sq[i]                           │
│  │   ├─ index[i] = dist[i] >> blob_size[9:7]                    │
│  │   └─ clamp index to [0, 255]                                 │
│  │         ◄── Blob Size (pot 1)                                 │
│  │                                                               │
│  ├─ Stage D (1 clk): 1/d² LUT lookup                             │
│  │   └─ contrib[i] = C_INV_SQ[index[i]]  (256:1 mux)           │
│  │                                                               │
│  ├─ Stage E (1 clk): Accumulate + classify + color               │
│  │   ├─ field = Σ contrib[i] for active blobs                   │
│  │   ├─ Classify: inside/skin/outside vs threshold               │
│  │   └─ Map zone + parameters → Y/U/V                           │
│  │         ◄── Threshold (pot 2), Skin Width (pot 4),            │
│  │             Hue Shift (pot 5), Fill Mode (toggle 7),          │
│  │             Color (toggle 8), Source (toggle 9),              │
│  │             Outline (toggle 10)                               │
│  │                                                               │
│  ├── Interpolator (4 clocks per Y/U/V)                           │
│  │   └─ Mix = lerp(input_delayed, generated, mix_amount)         │
│  │         ◄── Mix (fader 12)                                    │
│  │                                                               │
│  └── Output register + pipeline overhead (2 clocks)              │
│                                                                  │
│  Bypass: select delayed input or mix result                      │
│           ◄── Bypass (toggle 11)                                 │
└──────────────────────────────────────────────────────────────────┘
```

The processing divides cleanly into two phases. During vertical blanking, a sequential state machine cycles through all four blobs (4 clock phases each) to compute their center positions using the shared sin/cos LUT — this requires 16 clocks total, well within the blanking interval. During active video, the per-pixel field evaluation pipeline runs at full pixel rate, computing all four blob contributions in parallel across five pipeline stages (A through E).

The field evaluation achieves full parallelism by maintaining four independent signal paths through Stages A–D. Each path computes the absolute offset, squares it, shifts it based on Blob Size, and performs the LUT lookup independently. Only in Stage E do the four contributions converge into a single accumulated field value for classification.

The 1/d² LUT provides a critical optimization: instead of performing a division per blob per pixel (which would be prohibitively expensive in the iCE40), the squared distance is used directly as an index into a precomputed table. The Blob Size parameter's upper 3 bits control how many bits of right-shift are applied before the LUT lookup, effectively scaling the field radius without changing the LUT contents.

---

## Parameter Reference

*Videomancer's front panel with Amoeba active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Blob Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial extent of each blob's field and the amplitude of its orbital path simultaneously. At low values, the field evaluation right-shift is large, concentrating each blob's field contribution into a small area around its center — the blobs appear as small circles and must approach very closely before their fields overlap enough to merge. At high values, the field extends much farther from each center, producing larger circles that merge at greater separation distances. The orbit amplitude also scales with this parameter — larger blobs swing across a wider area of the frame, smaller blobs orbit near the center. The upper 3 bits of the register select the distance shift (0–7), providing 8 discrete size steps within the continuous pot range.

---

#### Knob 2 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Sets the isosurface threshold that defines the inside/skin/outside classification boundary. At low threshold values, only pixels very close to a blob center reach the threshold — the visible shapes are small, tightly defined circles. At high threshold values, the field needs less contribution to qualify as "inside," so the shapes appear larger and merge at greater distances. The threshold interacts directly with Blob Size: a large blob size with a low threshold produces defined circles, while a large blob size with a high threshold produces a single amorphous merged mass. The threshold value is compared against the 12-bit accumulated field total from all active blobs.

---

#### Knob 3 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the rate at which all blob phase accumulators advance per frame. At 0%, the blobs are frozen in position — their phase accumulators do not increment, and the metaball pattern is static. As speed increases, the Lissajous orbits evolve more rapidly. At maximum, the blobs trace their orbital paths quickly, creating rapid merge/split activity. Because each blob has a different Lissajous frequency ratio, the same speed value produces different apparent velocities for different blobs — blob 0 (1:2 ratio) traces its figure-eight slowly while blob 3 (5:3 ratio) traces a denser path at the same base rate.

---

#### Knob 4 — Skin Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

Controls the width of the skin classification band below the isosurface threshold. At 0%, the skin band has zero width — there is only inside and outside, with no visible edge transition. As skin width increases, a wider band of pixels is classified as "skin" rather than "outside," producing a broader visible edge around each metaball. With outline enabled, the skin zone renders as a bright contour line; without outline, it renders at the raw field-normalized brightness, creating a soft glow around the shape boundary. The skin width value is right-shifted by 2 bits before being subtracted from the threshold.

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

Selects how many blobs are active in the field computation, from 1 to 4. Inactive blobs are excluded from the Stage E accumulation — their field contributions are not added to the total. With one blob, the output is a single circle (or circle with skin) orbiting the center. With two, merge/split events occur when the two orbital paths bring the blobs close together. With three or four, the interaction pattern becomes increasingly complex as multiple merging events can occur simultaneously, creating networks of connected shapes.

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

Wet/dry crossfade between the original input video (delayed to match the 12-clock processing pipeline) and the metaball-generated output. At 0%, the output is pure unprocessed input — no metaballs are visible. At 100%, the output is the fully generated metaball scene. Intermediate positions blend the two, allowing the metaball shapes to be superimposed over the source footage at any opacity. In Video source mode, this creates a partial keying effect where the metaball boundaries are visible but semi-transparent.

---

## Guided Exercises

These exercises progress from a single stationary blob through multi-blob merging dynamics to full-featured video-keyed metaball compositions.

### Exercise 1: Single Blob Anatomy

<img src={amoeba_exercise1_result} alt="Single Blob Anatomy — simulated result"/>

*Single Blob Anatomy — simulated result.*

**Objective**: Understand the three-zone classification system (inside/skin/outside) and how threshold and skin width define the metaball boundary.

1. **Single blob**: Set Count (Knob 6) to 1. Set Speed (Knob 3) to ~10% (slow drift). Set Mix at 100%, Bypass off.
2. **Large blob**: Set Blob Size (Knob 1) to ~60%. A single circle drifts slowly on a figure-eight path.
3. **Observe threshold effect**: Start with Threshold (Knob 2) at ~20%. The visible circle is small. Slowly increase threshold — the circle grows as more pixels exceed the threshold level. At maximum, nearly the entire screen is "inside."
4. **Observe skin width**: Set Threshold to ~40%. Set Skin Width (Knob 4) to ~10%. A thin band of intermediate brightness surrounds the solid interior. Increase Skin Width to ~80% — the band widens into a broad gradient halo.
5. **Enable outline**: Toggle Outline (Toggle 10) on. The skin band becomes a bright white contour line. A narrow skin width produces a sharp outline; a wide skin width produces a thick glowing border.
6. **Hollow mode**: Toggle Fill Mode (Toggle 7) to Hollow. The interior becomes black. Only the skin zone (the outline contour) is visible — a clean bright ring tracing the isosurface.
7. **Freeze and examine**: Set Speed to 0%. The blob stops. Examine the zones at leisure.

:::tip
Isosurface threshold defines shape size, skin width defines edge band, outline converts gradient to bright contour, hollow removes interior fill, zones are inside/skin/outside.
:::

---

### Exercise 2: Merge Dynamics

<img src={amoeba_exercise2_result} alt="Merge Dynamics — simulated result"/>

*Merge Dynamics — simulated result.*

**Objective**: Observe metaball merging and splitting behaviour with two and four blobs, and understand how blob size, threshold, and count interact to control merge distance.

1. **Two blobs**: Set Count (Knob 6) to 2. Set Speed to ~25%, Blob Size to ~55%, Threshold to ~35%.
2. **Watch for merge events**: Two blobs orbit on different Lissajous paths. When their paths bring them close together, the isosurface between them bulges outward and eventually bridges into a single shape. When they separate, the bridge narrows and snaps apart.
3. **Increase threshold**: Raise Threshold to ~60%. The blobs merge at greater distances — the combined field exceeds the threshold even when the centers are far apart. The shapes stay merged longer.
4. **Decrease threshold**: Lower Threshold to ~15%. The blobs must be nearly overlapping before their fields combine enough to merge. Most of the time they appear as independent circles.
5. **Four blobs**: Set Count to 4. The four Lissajous orbits create frequent multi-way merge events. Adjust Blob Size to ~50% to see three-way and four-way merges where multiple blobs fuse into a single amorphous mass.
6. **Enable rainbow**: Switch Color (Toggle 8) to Rainbow. Interior field values modulate chroma — regions near blob centers have different colour from regions near the isosurface boundary. During merges, the colour gradients blend organically.
7. **Add hue shift**: Rotate Hue Shift (Knob 5) through 360°. The colour palette cycles, revealing how the U/V mapping rotates with the shift parameter.

:::tip
Metaball merging from overlapping inverse-square fields, threshold controls merge distance, count increases interaction complexity, rainbow chroma reveals field topology.
:::

---

### Exercise 3: Video-Keyed Organic Shapes

<img src={amoeba_exercise3_result} alt="Video-Keyed Organic Shapes — simulated result"/>

*Video-Keyed Organic Shapes — simulated result.*

**Objective**: Use the metaball isosurface as a dynamic video key — video is visible only inside the organic blob shapes, with optional coloured outlines framing the revealed content.

1. **Video source**: Set Source (Toggle 9) to Video. Set Fill Mode to Solid. The metaball interiors now show the input video — the synthetic field-normalized luminance is replaced by the actual Y channel of the source.
2. **Configure shapes**: Count to 3, Blob Size to ~55%, Threshold to ~35%, Speed to ~20%.
3. **Observe keying**: The video content is visible only inside the blob shapes. Outside regions are black. As blobs drift and merge, different parts of the frame are revealed and concealed.
4. **Add outline**: Enable Outline (Toggle 10). Bright white contour lines frame each blob shape, clearly delineating the video-filled regions.
5. **Rainbow outlines**: Switch Color (Toggle 8) to Rainbow and rotate Hue Shift (Knob 5). The outlines become coloured borders. The interior chroma is also tinted by the rainbow mapping, blending the video content with the synthetic colour.
6. **Hollow key**: Switch to Hollow mode. The interior goes black — only the contour outlines and the video are suppressed. This creates pure line graphics — bright coloured outlines tracing the metaball boundaries against black.
7. **Blend with Mix**: Pull Mix (Fader 12) to ~50%. The metaball output blends with the original full-frame video, creating a ghostly superimposition where the blob outlines overlay the complete source image.

:::tip
Video source mode for luminance keying, metaball boundaries as dynamic mask, outline provides visible framing, mix fader for superimposition, hollow mode for pure contour graphics.
:::

---

## Tips

- **Blob Size and Threshold are the primary shape controls**: Blob Size determines the field radius, Threshold determines where the boundary is drawn. A large blob size with a low threshold produces well-separated circles. A large blob size with a high threshold produces merged amorphous shapes.
- **Speed = 0 freezes the animation**: Set Speed to 0% to stop all blob motion and use the static metaball pattern as a fixed overlay.
- **Outline + Hollow = vector graphics**: This combination strips the metaballs down to pure contour lines on black — clean line art that traces the isosurface boundary.
- **Video source turns metaballs into dynamic masks**: In Video mode, the blob shapes become windows into the input signal. Multiple blobs reveal different parts of the frame simultaneously.
- **Skin Width controls edge character**: Narrow skin = sharp boundaries. Wide skin = soft glowing edges. At zero skin width, there is no visible transition zone.
- **Rainbow mode reveals field topology**: In Rainbow mode, the chroma is driven by the field value, so you can see the field strength gradient even within the "inside" zone — useful for understanding how the fields of different blobs combine.
- **Count enables progressive complexity**: Start with one blob to understand the basic shape, then add blobs incrementally to see how interactions emerge.
- **Feedback loops create fractal-like patterns**: Routing the output back to the input seed causes the metaball shapes to feed into themselves, creating recursive patterns especially visible in Video source mode.
