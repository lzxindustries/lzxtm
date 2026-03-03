---
draft: true
sidebar_position: 243
slug: /instruments/videomancer/refract
title: "Refract"
image: /img/instruments/videomancer/refract/refract_hero_s1.png
description: "Light bends when it passes through glass, water, or any boundary between materials of different density."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import refract_source1_sunset from '/img/instruments/videomancer/refract/refract_source1_sunset.png';
import refract_source2_fruit from '/img/instruments/videomancer/refract/refract_source2_fruit.png';
import refract_source3_collage from '/img/instruments/videomancer/refract/refract_source3_collage.png';
import refract_source4_pattern from '/img/instruments/videomancer/refract/refract_source4_pattern.png';
import refract_source5_woman from '/img/instruments/videomancer/refract/refract_source5_woman.png';
import refract_source6_paint from '/img/instruments/videomancer/refract/refract_source6_paint.png';
import refract_hero_s1 from '/img/instruments/videomancer/refract/refract_hero_s1.png';
import refract_hero_s2 from '/img/instruments/videomancer/refract/refract_hero_s2.png';
import refract_hero_s3 from '/img/instruments/videomancer/refract/refract_hero_s3.png';
import refract_hero_s4 from '/img/instruments/videomancer/refract/refract_hero_s4.png';
import refract_hero_s5 from '/img/instruments/videomancer/refract/refract_hero_s5.png';
import refract_hero_s6 from '/img/instruments/videomancer/refract/refract_hero_s6.png';
import refract_ex1_s1 from '/img/instruments/videomancer/refract/refract_ex1_s1.png';
import refract_ex1_s2 from '/img/instruments/videomancer/refract/refract_ex1_s2.png';
import refract_ex1_s3 from '/img/instruments/videomancer/refract/refract_ex1_s3.png';
import refract_ex1_s4 from '/img/instruments/videomancer/refract/refract_ex1_s4.png';
import refract_ex1_s5 from '/img/instruments/videomancer/refract/refract_ex1_s5.png';
import refract_ex1_s6 from '/img/instruments/videomancer/refract/refract_ex1_s6.png';
import refract_ex2_s1 from '/img/instruments/videomancer/refract/refract_ex2_s1.png';
import refract_ex2_s2 from '/img/instruments/videomancer/refract/refract_ex2_s2.png';
import refract_ex2_s3 from '/img/instruments/videomancer/refract/refract_ex2_s3.png';
import refract_ex2_s4 from '/img/instruments/videomancer/refract/refract_ex2_s4.png';
import refract_ex2_s5 from '/img/instruments/videomancer/refract/refract_ex2_s5.png';
import refract_ex2_s6 from '/img/instruments/videomancer/refract/refract_ex2_s6.png';
import refract_ex3_s1 from '/img/instruments/videomancer/refract/refract_ex3_s1.png';
import refract_ex3_s2 from '/img/instruments/videomancer/refract/refract_ex3_s2.png';
import refract_ex3_s3 from '/img/instruments/videomancer/refract/refract_ex3_s3.png';
import refract_ex3_s4 from '/img/instruments/videomancer/refract/refract_ex3_s4.png';
import refract_ex3_s5 from '/img/instruments/videomancer/refract/refract_ex3_s5.png';
import refract_ex3_s6 from '/img/instruments/videomancer/refract/refract_ex3_s6.png';

# Refract

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: refract_source1_sunset, after: refract_hero_s1 },
    { label: "Fruit", before: refract_source2_fruit, after: refract_hero_s2 },
    { label: "Collage", before: refract_source3_collage, after: refract_hero_s3 },
    { label: "Pattern", before: refract_source4_pattern, after: refract_hero_s4 },
    { label: "Woman", before: refract_source5_woman, after: refract_hero_s5 },
    { label: "Paint", before: refract_source6_paint, after: refract_hero_s6 },
  ]}
/>
*Refract applying luma-driven displacement mapping with chromatic aberration and fresnel edge bending to split and distort a live video signal.*

---

## Overview

Light bends when it passes through glass, water, or any boundary between materials of different density. The angle of bending depends on the material, the wavelength of the light, and the angle of incidence. Refract simulates this phenomenon digitally, treating the input video's luminance as a height map that drives spatial displacement of the image.

The program chains displacement mapping, luma-to-offset conversion, fresnel-style radial bending, and per-channel chromatic offset into a ten-stage pipeline backed by two BRAMs configured as line buffers. Three interpolator instances smooth the displaced readback for sub-pixel accuracy. The name comes directly from the optical phenomenon — *refraction* — the bending of light at a material boundary.

At subtle settings, Refract produces gentle lens-like warping that follows the tonal contours of the source. At extreme settings, the image tears apart along luminance gradients, with each color channel pulling in a different direction to create prismatic color fringing reminiscent of looking through cut crystal.

---

## Background

### Displacement Mapping

Displacement mapping is a spatial transformation where pixel positions are shifted according to a control signal. In Refract, the source image's own luminance serves as the displacement map — bright pixels cause large offsets, dark pixels cause small offsets (or vice versa when inverted). The displaced pixel is read back from a BRAM line buffer at the offset address, creating a warped version of the image where the warping pattern follows the brightness structure of the source itself. This creates a feedback-like visual relationship: the content determines its own distortion.

### Fresnel Edge Bending

In optics, the Fresnel effect describes how light bends more strongly at glancing angles than at perpendicular incidence. Refract approximates this by computing each pixel's radial distance from the screen center and scaling the displacement proportionally. Pixels near the edges of the frame receive stronger displacement than those at the center. This creates a lens-like barrel or pincushion distortion that compounds with the luma-driven displacement, producing a naturalistic optical warping effect.

### Chromatic Aberration

Real lenses refract different wavelengths of light by different amounts — blue bends more than red. Refract models this by applying slightly different displacement offsets to each YUV channel. The chromatic control separates the Y, U, and V readback positions, creating color fringing along displacement gradients. This is the same artifact visible in photographs taken with low-quality or wide-angle lenses, repurposed here as a creative tool.

### Directional Displacement via Sin/Cos LUT

The displacement direction is determined by a 32-entry sine/cosine lookup table indexed by the angle control. This converts the angle parameter into horizontal and vertical displacement components, allowing the displacement vector to sweep through 360 degrees. Combined with the luma-driven magnitude, this creates directional flow fields where the image material slides in a chosen direction proportional to its brightness.

### Anamorphic Mode

Anamorphic lenses compress one axis relative to the other — traditionally used in cinema to capture widescreen images on standard-width film. Refract's anamorphic mode restricts displacement to the horizontal axis only, collapsing the vertical component to zero. This creates the characteristic horizontal stretching and squeezing associated with anamorphic optics, particularly visible as elongated bokeh and directional smearing.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Luma Extraction        (Y value → displacement magnitude)
│   ├─ 2. Luma Drive Scaling     (scale Y by luma_drive register)
│   ├─ 3. Angle Decomposition    (32-entry sin/cos LUT → dx, dy)
│   ├─ 4. Fresnel Scaling        (radial distance → edge magnification)
│   ├─ 5. Displacement Calc      (strength × luma × fresnel → offset)
│   ├─ 6. BRAM Line Buffer Read  (read Y at displaced address)
│   ├─ 7. Interpolation          (interpolator_u smoothing)
│   └─ 8. Invert Mux             (optional negate displacement)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Chromatic Offset       (per-channel displacement shift)
│   ├─ 2. BRAM Line Buffer Read  (read U/V at offset address)
│   ├─ 3. Interpolation          (interpolator_u per channel)
│   └─ 4. Shape Mask             (circular or rectangular boundary)
│
├── Sync / Control ─────────────────────────────────────────────
│   ├─ DDS Animator              (auto-sweep angle when enabled)
│   ├─ Anamorphic Gate           (zero vertical component if set)
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Output ─────────────────────────────────────────────────────
    └─ Wet/Dry Mix → Bypass Mux
```

The core interaction is between luma drive and displacement strength. Luma drive converts the input brightness into a per-pixel displacement magnitude, which is then scaled by the global strength control and decomposed into horizontal and vertical components via the angle LUT. The fresnel control adds a radial magnification that increases displacement toward the frame edges, creating the lens-like curvature. Chromatic aberration applies a secondary offset to the U and V channel readback addresses, so each color channel reads from a slightly different displaced position.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Phase
| Property | Value |
|----------|-------|
| Range | 0.0 – 1023.0 |
| Default | 0.0 |

Controls the global displacement magnitude. At zero, no displacement occurs regardless of other settings. As the value increases, the spatial offset applied to each pixel grows, creating more dramatic warping. At extreme values, the image can tear apart along luminance boundaries where adjacent pixels receive very different offset amounts. This control acts as a master intensity for the entire refraction effect.

---

#### Knob 2 — U Phase
| Property | Value |
|----------|-------|
| Range | 0.0 – 1023.0 |
| Default | 0.0 |

Sets the displacement direction via a 32-entry sine/cosine lookup table. The register value indexes the LUT to produce horizontal and vertical displacement components. Sweeping this control rotates the direction of the displacement field — at 0 the displacement is purely horizontal, at quarter-range it becomes diagonal, at half-range it is vertical, and so on through the full circle. When the animate toggle is active, a DDS accumulator sweeps this parameter automatically.

---

#### Knob 3 — V Phase
| Property | Value |
|----------|-------|
| Range | 0.0 – 1023.0 |
| Default | 0.0 |

Scales how strongly the input luminance drives displacement magnitude. At zero, displacement is uniform across the image regardless of brightness. As this value increases, bright pixels receive larger displacement than dark pixels (or vice versa when inverted), creating content-adaptive warping where the distortion pattern follows the tonal structure of the source image. This is the key control that makes Refract responsive to image content rather than applying a fixed geometric distortion.

---

#### Knob 4 — Y Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 0.0% |
| Suffix | % |

Controls fresnel-style edge bending intensity. The pipeline computes each pixel's radial distance from the frame center and scales displacement proportionally. At zero, displacement is spatially uniform. As this value increases, pixels near the frame edges receive progressively stronger displacement while the center remains relatively stable. This creates a barrel-distortion or pincushion effect layered on top of the luma-driven displacement.

---

#### Knob 5 — U Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 0.0% |
| Suffix | % |

Applies per-channel displacement offsets to create chromatic aberration. At zero, all three YUV channels read from the same displaced address. As this value increases, U and V channels receive progressively larger offsets relative to Y, causing color fringing along displacement gradients. The effect is most visible at luminance boundaries where displacement changes rapidly — prismatic rainbow edges appear, splitting the image into separated color planes.

---

#### Knob 6 — V Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 0.0% |
| Suffix | % |

Controls the interpolation smoothness applied to the displaced readback. Lower values produce hard, aliased edges at displacement boundaries. Higher values engage the interpolator more aggressively, producing smoother transitions between displaced and undisplaced regions. This is particularly important when displacement magnitudes are small — without smoothing, sub-pixel offsets produce stepping artifacts.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Y Flip** | Off | On |
| **8 — U Flip** | Off | On |
| **9 — V Flip** | Off | On |
| **10 — Fade Color** | Black | White |
| **11 — Bypass** | Off | On |

The five toggles control geometric mode, motion animation, and signal routing. Shape and Anamorphic define the displacement geometry. Animate adds temporal variation. Invert reverses the luma-to-displacement polarity. Bypass provides instant A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Fade Amount
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the displaced and original signal. At 100%, the fully refracted signal passes through. At 0%, the original signal is output unmodified. Intermediate values create a semi-transparent overlay effect where the displaced and undisplaced images blend, producing ghost-like double exposures along displacement contours.

---

## Guided Exercises

These exercises progress from basic displacement through chromatic aberration to animated optical effects. Each builds familiarity with a different aspect of the refraction engine.

### Exercise 1: Basic Lens Warp

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: refract_source1_sunset, after: refract_ex1_s1 },
    { label: "Fruit", before: refract_source2_fruit, after: refract_ex1_s2 },
    { label: "Collage", before: refract_source3_collage, after: refract_ex1_s3 },
    { label: "Pattern", before: refract_source4_pattern, after: refract_ex1_s4 },
    { label: "Woman", before: refract_source5_woman, after: refract_ex1_s5 },
    { label: "Paint", before: refract_source6_paint, after: refract_ex1_s6 },
  ]}
/>
*Basic Lens Warp — simulated result across source images.*
**Source**: A high-contrast image with sharp edges — text, geometric patterns, or architectural subjects.

**Objective**: Understand the relationship between displacement strength, angle, and luma drive.

1. **Global displacement**: Slowly increase Y Phase from zero. Watch the image begin to shift spatially. The displacement is uniform across the frame because Luma Drive is at zero.
2. **Set direction**: Adjust U Phase to rotate the displacement direction. Notice the image sliding in different directions as you sweep through the angle LUT.
3. **Content-adaptive**: Increase V Phase (Luma Drive) to about 50%. Now displacement tracks brightness — bright regions warp more than dark regions.
4. **Invert polarity**: Toggle Fade Color (Invert) to reverse which brightness regions warp. Dark areas now receive the strongest displacement.
5. **Smooth it out**: Increase V Displace (Smooth) to soften the displacement transitions. Compare harsh aliased edges versus smooth interpolated warping.

**Key concepts**: Displacement magnitude is controlled globally by strength, direction is set by angle LUT, luma drive makes displacement content-adaptive, interpolation smooths sub-pixel artifacts

---

### Exercise 2: Chromatic Prism

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: refract_source1_sunset, after: refract_ex2_s1 },
    { label: "Fruit", before: refract_source2_fruit, after: refract_ex2_s2 },
    { label: "Collage", before: refract_source3_collage, after: refract_ex2_s3 },
    { label: "Pattern", before: refract_source4_pattern, after: refract_ex2_s4 },
    { label: "Woman", before: refract_source5_woman, after: refract_ex2_s5 },
    { label: "Paint", before: refract_source6_paint, after: refract_ex2_s6 },
  ]}
/>
*Chromatic Prism — simulated result across source images.*
**Source**: Footage with smooth tonal gradients — sunsets, skin tones, or color bars.

**Objective**: Explore chromatic aberration and fresnel edge bending.

1. **Set base displacement**: Y Phase ~30%, V Phase (Luma Drive) ~40%.
2. **Add chromatic split**: Increase U Displace (Chromatic) slowly. Watch color fringing appear at luminance boundaries. U and V channels separate from Y, creating rainbow edges.
3. **Enable fresnel**: Increase Y Displace (Fresnel) from zero. The edges of the frame begin to warp more than the center, creating a lens curvature effect.
4. **Circular vs rectangular**: Toggle Y Flip (Shape) to switch between circular and rectangular boundary masking. Notice how the fresnel bending changes geometry.
5. **Combine**: With moderate chromatic and fresnel active, sweep U Phase (Angle). The prismatic edges rotate around the frame, creating a rotating crystal effect.

**Key concepts**: Chromatic aberration separates color channels spatially, fresnel adds radial magnification toward edges, circular and rectangular modes change the geometry of the effect

---

### Exercise 3: Animated Optical Flow

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: refract_source1_sunset, after: refract_ex3_s1 },
    { label: "Fruit", before: refract_source2_fruit, after: refract_ex3_s2 },
    { label: "Collage", before: refract_source3_collage, after: refract_ex3_s3 },
    { label: "Pattern", before: refract_source4_pattern, after: refract_ex3_s4 },
    { label: "Woman", before: refract_source5_woman, after: refract_ex3_s5 },
    { label: "Paint", before: refract_source6_paint, after: refract_ex3_s6 },
  ]}
/>
*Animated Optical Flow — simulated result across source images.*
**Source**: Any video with moderate tonal variation.

**Objective**: Combine animation with full refraction for dynamic optical effects.

1. **Enable animation**: Toggle V Flip (Animate) to activate the DDS angle sweep. The displacement direction begins rotating automatically.
2. **Set moderate strength**: Y Phase ~35%, V Phase ~50%.
3. **Add fresnel lens**: Y Displace ~40% creates a rotating barrel distortion centered on the frame.
4. **Chromatic rainbow**: U Displace ~50% separates the color channels, creating a rotating prismatic halo.
5. **Anamorphic variant**: Toggle U Flip (Anamorphic). The rotation collapses to horizontal-only oscillation — the image slides left and right rather than swirling.
6. **Mix blend**: Lower Fade Amount to ~50% to blend the animated refraction with the original, creating a shimmering heat-haze effect.

**Key concepts**: DDS animation sweeps the angle automatically, anamorphic restricts to horizontal displacement, wet/dry mix creates ghost-like overlays, full pipeline demonstrates the interaction of all controls

---


## Tips

- **Luma Drive is the signature control**: Without it, Refract applies uniform geometric displacement. With it, the displacement follows the image content — this is what makes Refract feel like a real optical effect rather than a simple image shift.
- **Chromatic aberration adds realism**: Even small amounts of chromatic split make the displacement feel like genuine lens distortion. Start with low values and increase gradually.
- **Fresnel creates lens curvature**: Combined with luma drive, fresnel produces a convincing simulation of looking through a curved glass surface. Circular mode enhances the lens illusion.
- **Anamorphic for cinematic effects**: Horizontal-only displacement creates the widescreen stretching associated with anamorphic cinematography. Combine with animation for oscillating horizontal flow.
- **Mix for heat shimmer**: Setting the wet/dry mix to ~30–50% blends displaced and original images, creating a translucent heat-haze effect that's less aggressive than full refraction.
- **Animation + chromatic = rotating prism**: With both animate and chromatic active, the color separation rotates around the frame, creating a kaleidoscopic prismatic effect.
- **Smooth high for subtle effects**: When using gentle displacement strengths, increase the smoothing control to eliminate aliasing artifacts. The interpolators need headroom to work effectively.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated on-chip memory in the FPGA used as line buffers for displaced pixel readback. |
| **BT.601** | ITU-R BT.601 color standard defining the YUV encoding used in the Videomancer pipeline. |
| **Chromatic Aberration** | Wavelength-dependent refraction causing different colors to focus at different points, creating color fringing at edges. |
| **DDS** | Direct Digital Synthesis; a numerically-controlled oscillator that generates a continuous sweep of the angle parameter for animation. |
| **Displacement Mapping** | A spatial transformation where pixel positions are shifted by an amount determined by a control signal, here the input luminance. |
| **Fresnel** | In optics, the increase in reflectance and refraction at glancing incidence angles; here approximated as radial distance-based displacement scaling. |
| **Interpolator** | A sub-pixel smoothing module (`interpolator_u`) that blends between adjacent displaced samples for artifact-free warping. |
| **LUT** | Lookup Table; the 32-entry sin/cos table that converts the angle register into horizontal and vertical displacement components. |
| **Pipeline** | Sequential processing stages, each operating on the previous stage's output every clock cycle; Refract uses 10 pipeline stages. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
