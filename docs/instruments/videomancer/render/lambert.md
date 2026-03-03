---
draft: true
sidebar_position: 164
slug: /instruments/videomancer/lambert
title: "Lambert"
image: /img/instruments/videomancer/lambert/lambert_hero.png
description: "Lambert draws a single 3D sphere on the screen using the Lambertian reflection model — the same diffuse shading equation that underpins virtually all real-time 3D rendering."
---

import lambert_hero from '/img/instruments/videomancer/lambert/lambert_hero.png';
import lambert_animation from '/img/instruments/videomancer/lambert/lambert_animation.gif';
import lambert_control_panel from '/img/instruments/videomancer/lambert/lambert_control_panel.png';
import lambert_exercise1_result from '/img/instruments/videomancer/lambert/lambert_exercise1_result.gif';
import lambert_exercise2_result from '/img/instruments/videomancer/lambert/lambert_exercise2_result.gif';
import lambert_exercise3_result from '/img/instruments/videomancer/lambert/lambert_exercise3_result.gif';

# Lambert

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lambert_hero} alt="Lambert hero image"/>
*Lambert rendering a Lambertian-shaded sphere with toon quantization bands floating against a dark void.*
<img src={lambert_animation} alt="Lambert animated output"/>
*Lambert output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Lambert draws a single 3D sphere on the screen using the Lambertian reflection model — the same diffuse shading equation that underpins virtually all real-time 3D rendering. A hardcoded light source illuminates the sphere from the upper left, and the brightness of each pixel on the sphere's surface is determined by the dot product of the surface normal and the light direction. Pixels outside the sphere fall to near-black, creating a stark figure-ground separation.

The program is named after Johann Heinrich Lambert (1728–1777), the Swiss mathematician who first described the cosine law of diffuse reflection in his 1760 treatise *Photometria*. Lambert's law states that the apparent brightness of an ideal matte surface is proportional to the cosine of the angle between the surface normal and the incoming light direction — exactly the dot product computed by this FPGA program on every pixel of every frame.

At its defaults, Lambert produces a smooth monochrome sphere — a luminous orb emerging from darkness. The Size control scales the sphere radius across the frame. Ambient lifts the minimum brightness so that unlit portions of the sphere remain partially visible rather than falling to pure shadow. Toon mode quantizes the continuous shading gradient into discrete bands, producing a cel-shaded aesthetic reminiscent of hand-drawn animation or comic book art. In RGB color mode, the sphere acquires a chroma gradient controlled by the Color knob, shifting from warm to cool hues across the U/V axes.

---

## Background

### The Lambertian Reflection Model

In 1760, Johann Heinrich Lambert published *Photometria*, establishing the first quantitative theory of light measurement. His law of diffuse reflection states that an ideal matte surface reflects incoming light equally in all directions, and that the perceived brightness is proportional to the cosine of the incidence angle. Mathematically: $I = I_0 \cos\theta = I_0 (\hat{n} \cdot \hat{l})$, where $\hat{n}$ is the surface normal and $\hat{l}$ is the light direction. This single dot product is the foundation of all diffuse shading in computer graphics — from early Gouraud shading on the Evans & Sutherland systems of the 1970s to the base layer of every modern PBR shader. Lambert implements this equation directly in FPGA fabric, computing the dot product per pixel at video rate.

### Surface Normals on an Implicit Sphere

A sphere centered at the origin has a beautifully simple normal: at any surface point $(x, y, z)$, the outward normal is simply $\hat{n} = (x, y, z) / r$. Lambert exploits this by computing the pixel's offset from the screen center, using those offsets as approximations of the X and Y components of the surface normal. The Z component is implicit (the sphere faces the viewer), so the dot product reduces to a weighted sum of the X and Y offsets — specifically, the VHDL computes $\text{dot} = -v_{cx}/2 + (-v_{cy})/4$, which models a light direction pointing toward the upper left at roughly 60° azimuth and moderate elevation. This is a simplified but effective approximation that avoids square roots entirely.

### Toon Shading and Cel Animation

Toon shading — also called cel shading — replaces smooth gradients with a small number of flat brightness bands, mimicking the hand-painted cells of traditional animation. The technique was popularized in video games like *Jet Set Radio* (2000) and *The Legend of Zelda: The Wind Waker* (2003). Lambert's toon mode quantizes the 10-bit shading value to its top 3 bits, producing up to 8 distinct brightness bands. The visual effect is a sphere that looks drawn rather than rendered — hard-edged shadow boundaries replace the smooth cosine falloff. Combined with strong contour outlines from an upstream program, this creates a convincing cartoon aesthetic.

### Ambient Light in Shading Models

In real-world lighting, even surfaces facing away from a light source receive some illumination from indirect light bouncing off nearby surfaces. In computer graphics, this indirect contribution is often approximated by a constant *ambient* term added to the diffuse calculation: $I = I_{\text{ambient}} + I_0 \max(0, \hat{n} \cdot \hat{l})$. Lambert's Ambient control sets this floor — the minimum brightness of any pixel on the sphere. At zero, the unlit hemisphere is completely black. At high values, the entire sphere glows uniformly, washing out the directional shading. The sweet spot is usually 15–30%, providing enough fill to reveal surface curvature in the shadows without flattening the overall contrast.

### Synthesis Programs as Compositing Sources

Lambert generates imagery from nothing — no input video is required. This makes it a *synthesis* program, ideal for compositing workflows. The sphere can serve as a luminance mask for keying, a shape generator for downstream effects, or a standalone graphical element in multi-layer compositions. The Brightness fader (which functions as a wet/dry mix against the delayed input) allows blending the synthetic sphere with incoming video, creating overlay and superimposition effects.


---

## Signal Flow

```
Pixel Clock
│
├── Clock 1: Sync Detection + Counters ─────────────────────────
│   ├─ Detect hsync/vsync falling edges
│   ├─ Maintain x_counter (per pixel) and y_counter (per line)
│   └─ Increment frame_counter on vsync (if Animate On)
│
├── Clock 2: Center Coordinates ────────────────────────────────
│   ├─ v_cx = x_counter − 640   (signed offset from center)
│   └─ v_cy = y_counter − 360
│
├── Clock 3: Distance² and Sphere Test ─────────────────────────
│   ├─ v_dist_sq = cx² + cy²
│   ├─ v_radius_sq = Size × Size
│   └─ v_in_sphere = (dist_sq >> 4) < radius_sq
│
├── Clock 4: Dot Product (Lambert Diffuse) ─────────────────────
│   ├─ v_nx = −cx, v_ny = −cy   (surface normal approximation)
│   ├─ v_dot = nx/2 + ny/4      (hardcoded upper-left light)
│   └─ v_shade = max(0, dot)    (clamp negative to zero)
│
├── Clock 5: Ambient + Toon ────────────────────────────────────
│   ├─ v_shade = shade + Ambient  (add ambient floor)
│   ├─ Clamp to 1023
│   └─ If Toon: quantize to top 3 bits (8 bands)
│
├── Clock 6: Color Assignment ──────────────────────────────────
│   ├─ In sphere + Mono:  Y=shade, U=512, V=512
│   ├─ In sphere + RGB:   Y=shade, U=Color, V=1023−Color
│   └─ Outside sphere:    Y=64, U=512, V=512
│
├── Clocks 5–8: Interpolator (wet/dry Brightness) ──────────────
│   └─ lerp(dry, wet, Brightness)  ×3 channels  (4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-stage delay pipeline (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The entire shading computation happens in a single monolithic process — there are no sub-entity instantiations for the core math. The dot product uses a simplified hardcoded light direction (nx/2 + ny/4) rather than computing a true directional vector from the Light Angle register, which means the light always comes from the upper left regardless of the Light Angle knob position. The Brightness fader is wired to the interpolator's mix input, so it functions as a wet/dry crossfade between the synthetic sphere and the delayed input video — not as an additive brightness offset despite its label.

---

## Parameter Reference

<img src={lambert_control_panel} alt="Videomancer front panel with Lambert loaded"/>
*Videomancer's front panel with Lambert active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Light Angle
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 90° |
| Suffix | ° |

Labeled "Light Angle" and wired to the register, but the VHDL pipeline never references this value. The light direction is hardcoded to upper-left (nx/2 + ny/4). This control exists as a stub for future development. Turning it has no visible effect on the output.

---

#### Knob 2 — Elevation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

Labeled "Elevation" and read into the s_elevation signal, but the pipeline never uses this value in any computation. Like Light Angle, it is a placeholder for a future version that might implement full spherical light positioning. Currently has no effect.

---

#### Knob 3 — Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the sphere radius. At zero, the sphere vanishes entirely — every pixel fails the inside test and falls to the dark background. At maximum, the sphere fills much of the frame, its edges extending nearly to the screen boundaries. The radius enters the pipeline as a squared comparison (Size × Size vs. distance²), so the visual scaling is roughly linear in screen area rather than linear in radius. Mid-range values around 50% produce a sphere that fills approximately one quarter of the frame — a good starting point for seeing the full shading gradient from highlight to shadow.

---

#### Knob 4 — Ambient
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the ambient light floor — the minimum brightness of any pixel on the sphere's surface. The ambient value is added directly to the dot-product shade, so at zero ambient the unlit hemisphere is pure black, and at maximum ambient the entire sphere glows uniformly at full brightness with no visible directional shading. The perceptual sweet spot is 20–30%, which reveals enough shadow detail to show the sphere's curvature while preserving a strong sense of directionality in the lighting.

---

#### Knob 5 — Color
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the chroma intensity when Color mode (Toggle 8) is set to RGB. The register value is assigned directly to the U channel, and its complement (1023 − Color) to the V channel. At the midpoint (512), U and V are nearly complementary neutrals; sweeping toward zero or maximum pushes the sphere into saturated warm or cool hues. In Mono mode this control has no visible effect because U and V are locked to 512 (neutral gray).

---

#### Knob 6 — Specular
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Labeled "Specular" and read into the s_specular signal, but the pipeline never references this value. It was intended for a Phong-style specular highlight that was not implemented. Turning it has no visible effect.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Color** | Mono | RGB |
| **9 — Specular** | Off | On |
| **10 — Toon** | Off | On |
| **11 — Bypass** | Off | On |

Of the five toggles, only three produce visible changes: Color (Toggle 8) switches between monochrome and RGB coloring, Toon (Toggle 10) enables quantized shading bands, and Bypass (Toggle 11) routes the input directly to the output. The Animate toggle (Toggle 7) increments an internal frame counter on each vsync, but that counter is never used in the shading pipeline — it has no visible effect. The Specular toggle (Toggle 9) is similarly a stub with no downstream reference.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Labeled "Brightness" in the TOML but wired to the interpolator's mix input — it functions as a wet/dry crossfade, not an additive brightness control. At 0%, the output is 100% dry (passthrough of delayed input video). At 100%, the output is 100% wet (pure synthetic sphere). Intermediate values blend the sphere over the input, creating a superimposition effect. This is the standard Videomancer mix architecture shared across all programs.

---

## Guided Exercises

These exercises explore Lambert's shading model from basic sphere rendering through toon quantization to compositing workflows, using only the controls that produce visible effects.

### Exercise 1: The Lambertian Sphere

<img src={lambert_exercise1_result} alt="The Lambertian Sphere result"/>
*The Lambertian Sphere — simulated result across source images.*
**Objective**: Understand the relationship between sphere size, ambient light, and the Lambertian shading gradient.

1. **Default sphere**: Set Size to ~50%, Ambient to ~25%, Brightness (fader) to 100%. A monochrome sphere appears, illuminated from the upper left.
2. **Shadow depth**: Sweep Ambient from 0% to 100%. At 0%, the unlit hemisphere is pure black. At 100%, the entire sphere glows uniformly — the directional shading vanishes.
3. **Size scaling**: Sweep Size from 0% to 100%. At low values the sphere is a small bright dot. At maximum it nearly fills the frame, revealing the full gradient from highlight through terminator to shadow.
4. **Observe the gradient**: With Size at ~70% and Ambient at ~15%, note how the brightest point is upper-left (facing the light) and brightness falls off smoothly toward the lower-right limb. This is Lambert's cosine law made visible.
5. **Background level**: Notice the area outside the sphere sits at Y=64 (near-black). This is a fixed background, not affected by any control.

**Key concepts**: Lambertian diffuse shading is a dot product between surface normal and light direction, ambient sets the shadow floor, the light direction is fixed upper-left

---

### Exercise 2: Toon Shading Bands

<img src={lambert_exercise2_result} alt="Toon Shading Bands result"/>
*Toon Shading Bands — simulated result across source images.*
**Objective**: Explore how toon quantization transforms the smooth Lambertian gradient into discrete cel-shaded bands.

1. **Start smooth**: Size ~60%, Ambient ~20%, Toon Off. Observe the continuous shading gradient.
2. **Enable Toon**: Toggle Toon On. The smooth gradient snaps into flat bands — hard-edged concentric arcs separating brightness levels. Count the visible bands (typically 3–5 depending on Ambient).
3. **Ambient interaction**: Slowly increase Ambient. As the floor rises, the darkest bands disappear — the sphere appears to have fewer shading steps. At very high Ambient, only 1–2 bands remain.
4. **Size interaction**: With Toon On, increase Size to maximum. The bands become wide arcs spanning the frame, revealing their concentric geometry clearly.
5. **Compare**: Toggle Toon On and Off rapidly to see the smooth-to-quantized transition. The highlight position doesn't change — only the gradient resolution.

**Key concepts**: Toon shading truncates to 3 MSBs producing 8 possible levels, ambient compresses visible band count, band boundaries follow iso-brightness contours of the dot product

---

### Exercise 3: Color Sphere Compositing

<img src={lambert_exercise3_result} alt="Color Sphere Compositing result"/>
*Color Sphere Compositing — simulated result across source images.*
**Objective**: Use RGB color mode and the mix fader to composite a colored sphere over incoming video.

1. **Enable RGB**: Toggle Color to RGB. The sphere acquires a visible hue.
2. **Sweep Color**: Turn the Color knob through its full range. The sphere's hue shifts from one saturated extreme through neutral to the complementary extreme. At midpoint (~50%), the chroma is minimal.
3. **Choose a hue**: Set Color to a value that produces a pleasing tint — around 30% for warm tones or 70% for cool tones.
4. **Composite**: With video feeding the input, pull Brightness (fader) to ~60%. The colored sphere blends over the incoming video as a semi-transparent overlay.
5. **Toon + Color**: Enable Toon while in RGB mode. The color gradient is preserved within each toon band, creating a pop-art quality — flat-shaded colored arcs over the video.
6. **Full opacity**: Push Brightness to 100% for an opaque sphere floating over black, or 0% for pure passthrough.

**Key concepts**: RGB mode assigns Color register to U and its complement to V, the fader is a wet/dry mix not a brightness offset, toon quantization applies to luminance while chroma is unaffected

---


## Tips

- **Light Angle, Elevation, Specular pot, Animate, and Specular toggle are stubs**: These controls are wired to registers but not used in the current pipeline. Save yourself troubleshooting time by knowing they have no effect.
- **Brightness is actually Mix**: Despite the TOML label, the fader controls wet/dry blend, not additive brightness. Use it for compositing the sphere over incoming video.
- **Ambient controls shadow visibility**: Low ambient gives dramatic chiaroscuro lighting. High ambient produces a flatter, more uniformly lit sphere — useful when using the sphere as a mask or compositing element.
- **Toon mode works best with low Ambient**: Higher ambient compresses the toon bands toward the top of the brightness range, reducing visible contrast between bands. Low ambient (10–20%) maximizes the number of visible discrete bands.
- **RGB mode complementary chroma**: U is set to the Color value and V to its complement (1023 − Color). At Color = 512, both are near-neutral. Offset from center for saturated hues.
- **Use as a compositing element**: Route Lambert into a downstream keyer or mixer. The clean sphere-on-black output makes an excellent luminance mask or shape source.
- **Background is fixed at Y=64**: The area outside the sphere is always near-black. It cannot be adjusted. For a different background, composite Lambert over another program's output using the fader.

---

## Glossary

| Term | Definition |
|------|------------|
| **Ambient light** | A constant minimum brightness added to all surface points regardless of their orientation to the light source, approximating indirect illumination. |
| **Cel shading** | A rendering technique that quantizes smooth shading into flat tonal bands, mimicking hand-painted animation cells. Also called toon shading. |
| **Cosine law** | Lambert's law: the intensity of reflected light from a diffuse surface is proportional to the cosine of the angle between the surface normal and the light direction. |
| **Diffuse reflection** | Light scattered equally in all directions from a matte surface, as described by Lambert's law. Distinguished from specular (mirror-like) reflection. |
| **Dot product** | The scalar product of two vectors, equal to the product of their magnitudes times the cosine of the angle between them. Used here to compute shading intensity. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that implements the video processing pipeline in hardware. |
| **Lambertian surface** | An idealized perfectly matte surface that reflects light equally in all directions, obeying Lambert's cosine law. |
| **Proc amp** | Processing amplifier; a gain-and-offset stage applied to a video signal. The interpolator in Lambert functions as a wet/dry mix rather than a traditional proc amp. |
| **Surface normal** | A unit vector perpendicular to a surface at a given point, used to compute the angle of incoming light for shading calculations. |
| **Toon shading** | See cel shading. |
| **YUV** | A color space separating luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |

---
