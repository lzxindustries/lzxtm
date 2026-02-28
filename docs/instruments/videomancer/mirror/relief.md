---
draft: true
sidebar_position: 216
slug: /instruments/videomancer/relief
title: "Relief"
image: /img/instruments/videomancer/relief/relief_hero.png
description: "A bas-relief is a sculptural technique where figures are carved into a flat surface, projecting slightly outward to catch light at their edges."
---

import relief_before_after from '/img/instruments/videomancer/relief/relief_before_after.png';
import relief_control_panel from '/img/instruments/videomancer/relief/relief_control_panel.png';
import relief_exercise1_result from '/img/instruments/videomancer/relief/relief_exercise1_result.png';
import relief_exercise2_result from '/img/instruments/videomancer/relief/relief_exercise2_result.png';
import relief_exercise3_result from '/img/instruments/videomancer/relief/relief_exercise3_result.png';
import relief_hero from '/img/instruments/videomancer/relief/relief_hero.png';
import relief_source1_kodim15 from '/img/instruments/videomancer/relief/relief_source1_kodim15.png';
import relief_source2_kodim15_bw from '/img/instruments/videomancer/relief/relief_source2_kodim15_bw.png';
import relief_source3_male_1024 from '/img/instruments/videomancer/relief/relief_source3_male_1024.png';

# Relief

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={relief_hero} alt="Relief hero image"/>
*Relief applying directional emboss with specular highlights and Lambertian surface lighting to sculpt a flat video signal into a three-dimensional bas-relief.*
<img src={relief_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Relief applied.*

---

## Overview

A bas-relief is a sculptural technique where figures are carved into a flat surface, projecting slightly outward to catch light at their edges. The illusion of depth comes entirely from how light interacts with the carved surface — shadows on one side of each raised feature, highlights on the other. Relief recreates this effect digitally, treating the input video's luminance as a height field and computing directional lighting across its surface.

The program chains directional edge detection, height-field processing, Lambertian diffuse shading, specular highlight extraction, surface coloring, and ambient fill into an eight-clock pipeline using three interpolator instances. The name refers directly to *relief* sculpture — the art of creating the illusion of three dimensions on a fundamentally flat surface.

At subtle settings, Relief adds a gentle textural emboss that gives video a chiseled, engraved quality. At extreme settings, it transforms the image into a metallic surface map where only the edges and highlights of the original content remain, lit by a virtual light source that the performer can rotate in real time.

---

## Background

### Directional Edge Detection

Relief computes edges by taking the difference between each pixel and its neighbor at a specific angle offset. This is a *directional derivative* — it measures how rapidly brightness changes along a chosen direction. Where the image is smooth, the derivative is near zero. Where there's a sharp edge, the derivative is large and positive on one side, large and negative on the other. This asymmetry is what creates the illusion of a raised surface: one side of the edge appears lit (positive derivative), the other appears shadowed (negative derivative).

### Lambertian Shading

In the Lambertian lighting model, the brightness of a surface point depends on the cosine of the angle between the surface normal and the incoming light direction. Relief approximates this by using the directional derivative as a proxy for surface orientation — bright derivatives face toward the virtual light source, dark derivatives face away. The result is a convincing illusion of a lit three-dimensional surface, even though the computation is a simple directional difference operation.

### Specular Highlights

Real surfaces produce bright specular reflections where the viewing angle aligns with the reflected light direction. Relief approximates this by thresholding the derivative — pixels where the directional derivative exceeds a threshold are treated as specular highlights and given an additional brightness boost. The specular control sets this threshold, determining how bright an edge must be to produce a glinting highlight.

### Emboss versus Engrave

The classic emboss effect makes features appear to protrude from the surface — raised above the background plane. The opposite effect, *engrave*, makes features appear to be cut into the surface — recessed below the background plane. The difference is purely a sign change in the directional derivative. Relief's mode toggle switches between adding and subtracting the derivative, flipping the perceived depth direction.

### Surface Tinting and Metallic Mode

The surface color of a relief can be uniform (stone, plaster) or can inherit the chrominance of the source material. Relief's color mode toggle switches between monochrome relief (gray stone) and color-preserving relief (tinted metal). Metallic mode further modifies the shading by multiplying the specular highlights with the source chrominance, creating the appearance of colored metallic surfaces where highlights take on the hue of the underlying material.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Pre-Blur              (smoothing via interpolator_u)
│   ├─ 2. Direction Decompose   (32-entry sin/cos LUT → sample offsets)
│   ├─ 3. Directional Derivative (current - neighbor at angle offset)
│   ├─ 4. Depth Scaling         (derivative × depth register)
│   ├─ 5. Emboss/Engrave Mux    (negate derivative if engrave mode)
│   ├─ 6. Invert Mux            (optional height field inversion)
│   ├─ 7. Surface + Ambient     (center at ambient + derivative)
│   └─ 8. Specular Addition     (threshold → highlight boost)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Color/Mono Select     (pass through or zero to neutral)
│   ├─ 2. Metallic Shading      (multiply chroma by specular)
│   └─ 3. Surface Tint Bias     (add ambient tint offset)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Output ─────────────────────────────────────────────────────
    └─ Wet/Dry Mix → Bypass Mux
```

The core computation is the directional derivative: `output = 512 + (current_pixel - neighbor_pixel) * depth`. The result is centered at mid-gray (512 in 10-bit), with positive derivatives above and negative derivatives below. The direction register selects which neighbor to sample via the sin/cos LUT, while the depth register scales the derivative magnitude. Specular highlights are extracted by thresholding the absolute derivative value and adding a brightness boost to pixels that exceed the threshold.

---

## Parameter Reference

<img src={relief_control_panel} alt="Videomancer front panel with Relief loaded"/>
*Videomancer's front panel with Relief active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Light Angle
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 90° |
| Suffix | ° |

Sets the virtual light direction via a 32-entry sine/cosine lookup table. The register value indexes the LUT to select horizontal and vertical neighbor offsets for the directional derivative computation. Sweeping this control rotates the apparent light source around the relief surface — at 0° the light comes from the left, at 90° from above, at 180° from the right, and at 270° from below. Edges perpendicular to the light direction show maximum contrast.

---

#### Knob 2 — Elevation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the relief depth — the magnitude of the directional derivative scaling. At zero, the derivative has no effect and the output is a flat mid-gray surface. As the value increases, edge contrast grows, making the relief appear deeper and more strongly carved. High values produce dramatic chiaroscuro lighting with deep shadows and bright highlights on opposite sides of each edge.

---

#### Knob 3 — Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Applies pre-detection blur via an interpolator instance, smoothing the input luminance before the directional derivative is computed. At minimum, the derivative detects every fine-grained edge and noise artifact. As smoothing increases, only larger-scale features produce derivatives — fine detail is suppressed and the relief appears carved from a smoother surface material.

---

#### Knob 4 — Smoothing
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 2 |

Sets the surface color brightness — the base luminance level of the relief surface independent of the derivative. This is analogous to the ambient reflectance of the sculpted material. Low values create a dark stone-like surface where only highlights are visible. High values create a bright plaster-like surface where shadows carve dark lines into a light background.

---

#### Knob 5 — Specular
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the specular highlight intensity. The pipeline thresholds the directional derivative to detect bright peaks — pixels where the derivative exceeds the threshold receive an additional brightness boost. Low specular values produce matte surfaces with no highlights. High values create glossy, reflective surfaces with sharp glinting points along edges. Most effective when combined with moderate depth values.

---

#### Knob 6 — Surface Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the minimum ambient brightness — a floor value added to every pixel regardless of the derivative computation. This prevents shadows from going completely black, preserving detail in recessed areas. Combined with the surface control, this defines the overall luminance range of the relief: surface sets the midpoint, ambient sets the shadow floor.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Output Mode A** | Relief | Lit |
| **8 — Output Mode B** | Normal | Emboss |
| **9 — Invert** | Off | On |
| **10 — Edge Enhance** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control output mode, shading model, and signal path. Output Mode A and B select the visual treatment. Invert and Edge Enhance modify the height field and derivative. Bypass provides instant A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the relief-processed and original signal. At 100%, the full relief output is shown. At 0%, the original video passes through unmodified. Intermediate values blend the relief over the source, creating a subtle textural overlay that adds dimensionality without fully replacing the original image.

---

## Guided Exercises

These exercises progress from basic directional emboss through surface lighting to metallic shading. Each builds familiarity with a different aspect of the relief engine.

### Exercise 1: Stone Carving

<img src={relief_exercise1_result} alt="Stone Carving result"/>
*Stone Carving — simulated result across source images.*
**Source**: A portrait or face close-up with strong tonal variation.

**Objective**: Create a classic bas-relief sculpture effect with directional lighting.

1. **Set light direction**: Adjust Light Angle to about 135° (upper-left illumination). This is the classic emboss lighting angle.
2. **Add depth**: Increase Elevation (Depth) to about 50%. Edges become visible as lit/shadowed pairs.
3. **Smooth the surface**: Increase Depth (Smooth) to step 2 of 4. Fine skin texture disappears, leaving only major facial features.
4. **Set surface tone**: Adjust Smoothing (Surface) to about 60% for a warm stone-like base brightness.
5. **Add ambient**: Set Surface Tint (Ambient) to about 30% to prevent shadows from going fully black.
6. **Compare**: Toggle Bypass to see the original versus the carved relief.

**Key concepts**: Directional derivative creates the illusion of a lit surface, light angle controls which edges are highlighted versus shadowed, smoothing removes fine detail for a sculptural appearance

---

### Exercise 2: Metallic Surface

<img src={relief_exercise2_result} alt="Metallic Surface result"/>
*Metallic Surface — simulated result across source images.*
**Source**: Colorful footage — flowers, painted surfaces, or abstract color fields.

**Objective**: Create a metallic relief with color-tinted specular highlights.

1. **Base relief**: Light Angle ~90° (top-lit), Elevation ~40%.
2. **Add specular gloss**: Increase Specular to about 60%. Bright highlight points appear along the sharpest edges.
3. **Enable color**: Toggle Output Mode B to Normal, and ensure color source chrominance passes through.
4. **Enable metallic**: Toggle Invert (Metallic) on. Specular highlights now take the hue of the underlying image. Golden areas produce gold highlights, blue areas produce blue highlights.
5. **Rotate light**: Slowly sweep Light Angle through 360°. Watch the highlights and shadows orbit around the features, revealing the metallic surface from different angles.
6. **Adjust ambient**: Set Surface Tint (Ambient) to ~20% for deep shadows that make the metallic sheen more dramatic.

**Key concepts**: Specular highlights are thresholded derivative peaks, metallic mode tints highlights with source chrominance, rotating the light direction reveals surface detail from different angles

---

### Exercise 3: Emboss Edge Map

<img src={relief_exercise3_result} alt="Emboss Edge Map result"/>
*Emboss Edge Map — simulated result across source images.*
**Source**: High-contrast graphics, text, or geometric patterns.

**Objective**: Use Relief as an edge extractor by isolating the raw directional derivative.

1. **Emboss-only output**: Toggle Output Mode B to Emboss. The output becomes the raw centered derivative — mid-gray with bright/dark edge pairs.
2. **Set direction**: Light Angle ~0° (horizontal edges emphasized).
3. **Increase depth**: Elevation ~70%. Edge contrast becomes very strong.
4. **No smoothing**: Set Depth (Smooth) to step 1 (minimum). Every pixel-level edge is captured.
5. **Engrave comparison**: Toggle Output Mode A between Relief and Lit. Notice how the bright and dark sides of each edge swap — this is the sign change in the derivative.
6. **Height inversion**: Toggle Edge Enhance (Invert height) to invert the input brightness before derivative computation. The edge map changes because different features now form the height peaks.
7. **Mix overlay**: Lower Mix to ~40% to blend the edge map over the original, creating a sharpened appearance.

**Key concepts**: Emboss mode outputs the raw derivative centered at mid-gray, emboss versus engrave is a derivative sign change, height inversion changes which features are peaks versus valleys, mixing edge map with source creates edge enhancement

---


## Tips

- **Upper-left lighting is classic**: Setting Light Angle to ~135° produces the traditional emboss look used in graphic design. This angle feels natural because we expect illumination from above-left.
- **Smoothing controls the sculpting grain**: Low smoothing captures every pixel-level edge (fine sandstone). High smoothing captures only major features (smooth marble). Choose based on the source material.
- **Emboss mode for edge extraction**: Output Mode B in Emboss produces a clean centered-derivative signal useful as input to other programs in a processing chain.
- **Metallic needs color**: The Metallic toggle has no visible effect unless the Color toggle is also active, because monochrome relief has no chrominance to tint the highlights with.
- **Specular adds sparkle at edges**: Start with specular at zero to dial in the basic relief look, then add specular last to introduce shiny contact points along the sharpest edges.
- **Mix for subtle texture**: Setting mix to 30–50% blends the relief over the original video, adding a subtle carved texture without fully replacing the source image.
- **Invert vs engrave**: These produce different results. Engrave negates the derivative output (lit edges swap sides). Invert negates the input height field (different features become peaks/valleys). Try both.

---

## Glossary

| Term | Definition |
|------|------------|
| **Ambient** | The minimum brightness level applied uniformly to all pixels, preventing shadow regions from going completely black. |
| **Bas-Relief** | A sculptural technique where shapes are carved to project slightly from a flat background surface. |
| **BT.601** | The ITU-R standard defining the color matrix used to convert between RGB and YUV in video systems. |
| **Derivative** | The rate of change of a signal; the directional derivative measures brightness change along a specific angle. |
| **Emboss** | A visual effect that makes features appear to protrude from a surface, created by adding the directional derivative to a base brightness. |
| **Engrave** | The opposite of emboss; makes features appear recessed by subtracting the directional derivative. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Height Field** | A 2D map of elevation values; here, the input luminance treated as a surface height for lighting calculations. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **Lambertian** | A shading model where surface brightness depends on the cosine of the angle between the surface normal and light direction. |
| **LUT** | Lookup Table; the 32-entry sin/cos table that converts the direction register into neighbor-sampling offsets. |
| **Specular** | Bright highlight reflections that occur when viewing angle aligns with reflected light direction; approximated here by thresholding the derivative magnitude. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
