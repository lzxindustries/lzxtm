---
draft: true
sidebar_position: 185
slug: /instruments/videomancer/mirage
title: "Mirage"
image: /img/instruments/videomancer/mirage/mirage_hero.png
description: "The Quantel Mirage DVM8000, introduced in 1982, was the first real-time digital video effects system capable of mapping live television onto arbitrary 3D surfaces."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import mirage_hero from '/img/instruments/videomancer/mirage/mirage_hero.png';
import mirage_control_panel from '/img/instruments/videomancer/mirage/mirage_control_panel.png';
import mirage_exercise1_result from '/img/instruments/videomancer/mirage/mirage_exercise1_result.png';
import mirage_exercise2_result from '/img/instruments/videomancer/mirage/mirage_exercise2_result.png';
import mirage_exercise3_result from '/img/instruments/videomancer/mirage/mirage_exercise3_result.png';
import mirage_source1_kodim15 from '/img/instruments/videomancer/mirage/mirage_source1_kodim15.png';
import mirage_source2_kodim15_bw from '/img/instruments/videomancer/mirage/mirage_source2_kodim15_bw.png';
import mirage_source3_male_1024 from '/img/instruments/videomancer/mirage/mirage_source3_male_1024.png';

# Mirage

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: mirage_source1_kodim15, after: mirage_hero },
    { label: "Kodim15 B&W", before: mirage_source2_kodim15_bw, after: mirage_hero },
    { label: "Male", before: mirage_source3_male_1024, after: mirage_hero },
  ]}
/>
*Mirage wrapping a live video stream onto a rotating cylindrical surface with perspective shading and configurable background fill.*

---

## Overview

The Quantel Mirage DVM8000, introduced in 1982, was the first real-time digital video effects system capable of mapping live television onto arbitrary 3D surfaces. It could wrap a video image around a sphere, peel it off as a page curl, or ripple it like a flag — effects that were astonishing to broadcast audiences at the time and became iconic visual signatures of 1980s television. The Mirage program recreates this family of effects using per-pixel 2D coordinate remapping driven by a 64-entry sine/cosine lookup table.

Six surface types are available: cylinder, sphere, page peel, flag wave, cone, and shatter. Each surface type implements a different mathematical equation that displaces the horizontal read address on a per-pixel basis, reading from a dual-bank scanline buffer. A DDS (Direct Digital Synthesis) phase accumulator provides continuous rotation or animation, and perspective shading darkens regions that curve away from the viewer. Pixels that fall outside the surface boundary are replaced with a configurable background fill (black, white, blue, or gray).

The three toggle switches labeled "Surface A," "Surface B," and "Surface C" in the TOML are not independent on/off controls — the VHDL packs them as a 3-bit binary selector (bits 2:0 of register 6) that indexes all six surface types. The mapping is: 0=Cylinder, 1=Sphere, 2=Page Peel, 3=Flag, 4=Cone, 5=Shatter, with values 6–7 also producing Shatter (the default/others branch).

---

## Background

### The Quantel Mirage DVM8000

The Quantel Mirage was a broadcast video effects processor manufactured by Quantel Ltd. of Newbury, England. Debuting in 1982, it could texture-map live or pre-recorded video onto mathematically defined 3D surfaces in real time — a capability that previously required offline rendering. The machine was used extensively in broadcast television for station identification bumpers, music videos, and sports graphics. Its signature effects — the page turn, the spinning globe, the shattering pane — became visual clichés of the decade. The Mirage achieved its effects using custom hardware that computed per-pixel coordinate transformations at video rate, reading displaced samples from frame-buffer memory.

### Coordinate Remapping for 3D Effects

The core technique is 2D coordinate remapping: for each output pixel at position (x, y), the surface equation computes a displaced source address (x', y') from which the pixel value is read. On a cylinder, x' wraps horizontally according to a sinusoidal function, creating the illusion that the flat image is wrapped around a curved surface. On a sphere, both x and y displacements contribute. On a flag, a sinusoidal ripple modulates the horizontal position as a function of the vertical coordinate. The VHDL implements horizontal displacement only (using a previous-line buffer for the source), which is sufficient to create convincing surface illusions within the constraints of the iCE40 FPGA's limited block RAM.

### Direct Digital Synthesis (DDS) Animation

The Mirage's continuous rotation and wave animation are driven by a DDS phase accumulator — a simple counter that adds a programmable increment on every vertical sync pulse. The accumulated phase value indexes into the 64-entry sine/cosine lookup table, creating smooth cyclic animation. The Rotation knob controls the increment size: at zero there is no animation; at higher values the surface rotates or ripples faster. The Animation Direction toggle reverses the accumulator increment, reversing the direction of rotation or wave propagation.

### Perspective Shading

On curved surfaces (cylinder, sphere), regions that face away from the viewer should appear darker. The VHDL approximates this by using the cosine of the surface angle as a shading multiplier: pixels at the center of the visible surface (where cos ≈ 1.0) are fully bright, while pixels near the edge (where cos approaches 0) are progressively darkened. The Shading knob scales this effect. On flat surface types (flag, cone, shatter), shading is held at maximum brightness.

### Edge Masking and Background Fill

When the surface equation computes a source address that falls outside the valid pixel range (0–1023), the pixel is "out of bounds" and is replaced by a background fill color. The Background knob selects between four fills: black (mode 0), white (mode 1), broadcast blue (mode 2), and mid gray (mode 3). On the cylinder and sphere, out-of-bounds regions correspond to the back hemisphere — the part of the surface facing away from the viewer.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Scanline Buffer Write ─────────────────────────────────────
│   └─ Dual-bank BRAM (2048×10 per channel, Y/U/V)
│       Write current pixel to bank[line_sel], swap at hsync
│
├── Position Counters ─────────────────────────────────────────
│   ├─ h_count, v_count (absolute pixel position)
│   └─ x_norm, y_norm (signed, relative to frame center)
│
├── DDS Phase Accumulator ─────────────────────────────────────
│   └─ phase += rotation (or −=) at each vsync
│
├── Stage 1: Surface Parameter Decode ─────────────────────────
│   ├─ Scale coordinates by Scale pot
│   ├─ Compute theta index from surface equation + DDS phase
│   └─ Look up sin/cos from 64-entry LUT
│
├── Stage 2: Address Computation ──────────────────────────────
│   ├─ Per-surface displacement equation
│   ├─ x' = x_norm + 512 + displacement
│   ├─ Clamp and bounds check → out_of_bounds flag
│   └─ Compute shade_factor from cos (cylinder/sphere)
│
├── Stage 3: Sample Fetch ─────────────────────────────────────
│   └─ Read Y/U/V from opposite line buffer bank at x'
│
├── Stage 4: Shading + Edge Mask ──────────────────────────────
│   ├─ If out_of_bounds: output = background fill
│   └─ Else: Y = (sampled_Y × shade_factor) >> 10
│
├── Background Fill Generator ─────────────────────────────────
│   └─ 4 modes: Black / White / Blue / Gray
│
├── Wet/Dry Mix (3× interpolator_u, Fader) ────────────────────
│   └─ lerp(dry, wet, mix_amount) per channel
│
└── Bypass (Toggle 11) ────────────────────────────────────────
    └─ Select original or processed signal
```

The key constraint is that the VHDL uses a dual-bank single-scanline buffer — it reads from the *previous* line while writing the current line. This means vertical displacement is not directly implemented; the surface equations operate primarily through horizontal address remapping. The DDS phase accumulator increments once per frame (at vsync), so animation is frame-rate-locked. For cylinder and sphere surfaces, pixels on the back hemisphere (where cos < 0) are masked and replaced with background fill, creating a solid-looking 3D object floating over the background color.

---

## Parameter Reference

<img src={mirage_control_panel} alt="Videomancer front panel with Mirage loaded"/>
*Videomancer's front panel with Mirage active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Curvature
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the curvature or bend intensity of the selected surface type. On cylindrical and spherical surfaces, higher curvature increases the horizontal displacement driven by the sine component, making the surface appear more tightly curved. On the flag surface, curvature controls the wave amplitude. On the cone, it controls the perspective narrowing. On shatter, it controls the strip displacement distance. At zero curvature, most surfaces produce a flat (undistorted) image; at maximum, the distortion is extreme and pixels wrap far from their original positions.

---

#### Knob 2 — Rotation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the speed of the DDS phase accumulator, which drives continuous animation. At zero, the surface is static — no rotation, no wave motion. As the value increases, the animation speed increases: cylinders and spheres rotate faster, the flag ripples more rapidly, and the page peel advances its fold position. The relationship is linear: doubling the register value doubles the animation speed. Very high values create rapid spinning or flickering that can produce stroboscopic effects.

---

#### Knob 3 — Perspective
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls perspective foreshortening. In the current implementation, this value participates in the scale computation for surface coordinate normalization. Higher values increase the apparent depth perspective, making surfaces appear to recede more dramatically. The effect is most visible on the cylinder and sphere surfaces where it modulates how aggressively the surface narrows toward the edges. The effect is subtle compared to Curvature and Scale.

---

#### Knob 4 — Background
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 1 |

Selects the background fill color from four discrete modes, determined by the register value divided into four equal ranges. Mode 0 (0–255): black background — the surface floats over darkness. Mode 1 (256–511): white background — high contrast against dark surfaces. Mode 2 (512–767): broadcast blue — a saturated blue reminiscent of chroma-key backgrounds. Mode 3 (768–1023): mid gray — a neutral backdrop. The background is visible wherever the surface equation produces an out-of-bounds pixel address.

---

#### Knob 5 — Shading
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the intensity of perspective shading on curved surfaces. On cylinder and sphere, this scales the cosine-derived shade factor: at zero shading, the entire visible surface is uniformly bright; at maximum shading, edges darken dramatically while the center remains fully lit, creating a strong 3D appearance. On flag, cone, and shatter surfaces, the shade factor is held at maximum (no shading applied regardless of this knob's position).

---

#### Knob 6 — Scale
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the overall scale of the surface relative to the video frame. The normalized pixel coordinates are multiplied by this value before the surface equation is applied. Lower values create a larger virtual surface (less of it is visible, but what's visible is less distorted). Higher values shrink the surface, making the entire shape visible within the frame but increasing the displacement intensity. Values below a minimum clamp of 64 are forced to 64 to avoid division-related artifacts.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Surface A** | Off | On |
| **8 — Surface B** | Off | On |
| **9 — Surface C** | Off | On |
| **10 — Anim Dir** | Fwd | Rev |
| **11 — Bypass** | Off | On |

Toggles 7, 8, and 9 are not independent on/off switches — the VHDL combines them as a 3-bit binary surface selector (bits 2:0 of register 6). The combined value selects one of six surface types: 0 (all off) = Cylinder, 1 (A on) = Sphere, 2 (B on) = Page Peel, 3 (A+B on) = Flag, 4 (C on) = Cone, 5 (A+C on) = Shatter. Values 6–7 also produce Shatter (the VHDL default branch). Toggle 10 is an independent animation direction switch, and Toggle 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original video signal and the surface-mapped result. At 0%, the output is the unprocessed input. At 100%, the output is the fully distorted and shaded surface. Intermediate values create a blend where the original image ghosts through the 3D effect — this can create interesting double-exposure looks where the flat and curved versions of the image are superimposed.

---

## Guided Exercises

These exercises progress from simple cylinder wrapping to complex multi-surface animation. Each exercise demonstrates a different surface type and the interaction between curvature, animation, shading, and background.

### Exercise 1: Spinning Cylinder

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: mirage_source1_kodim15, after: mirage_exercise1_result },
    { label: "Kodim15 B&W", before: mirage_source2_kodim15_bw, after: mirage_exercise1_result },
    { label: "Male", before: mirage_source3_male_1024, after: mirage_exercise1_result },
  ]}
/>
*Spinning Cylinder — simulated result across source images.*
**Source**: A video with recognizable text or graphics — a title card, a news crawl, or a logo.

**Objective**: Learn how the cylinder wrap, rotation animation, and perspective shading interact.

1. Set Surface to Cylinder (all three surface toggles Off).
2. Set Curvature to about 50%. The image wraps into a visible curve.
3. Increase Rotation from 0. The cylinder begins spinning.
4. Increase Shading to 60%. The edges darken as they curve away.
5. Try different Background modes to see how the back-hemisphere fill changes.
6. Adjust Scale to shrink or grow the cylinder relative to the frame.

**Key concepts**: Cylinder uses sin/cos for horizontal displacement, cosine drives perspective shading, back hemisphere is masked to background

---

### Exercise 2: Flag Wave

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: mirage_source1_kodim15, after: mirage_exercise2_result },
    { label: "Kodim15 B&W", before: mirage_source2_kodim15_bw, after: mirage_exercise2_result },
    { label: "Male", before: mirage_source3_male_1024, after: mirage_exercise2_result },
  ]}
/>
*Flag Wave — simulated result across source images.*
**Source**: A full-frame image or graphic — a flag, a poster, or a painting.

**Objective**: Explore the sinusoidal ripple effect and how curvature controls wave amplitude.

1. Set Surface to Flag (Toggle 7 On, Toggle 8 On, Toggle 9 Off — value 3).
2. Set Curvature low (~20%) for gentle ripples.
3. Increase Rotation for faster wave animation.
4. Increase Curvature to intensify the wave amplitude — the image begins to buckle and distort.
5. Reverse direction with Anim Dir (Toggle 10) — the wave reverses.
6. Set Mix to ~60% to see the flat and rippled images superimposed.

**Key concepts**: Flag uses sinusoidal displacement as a function of vertical position, amplitude from Curvature pot, DDS drives wave propagation speed, no shading on flat surfaces

---

### Exercise 3: Shatter and Explode

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: mirage_source1_kodim15, after: mirage_exercise3_result },
    { label: "Kodim15 B&W", before: mirage_source2_kodim15_bw, after: mirage_exercise3_result },
    { label: "Male", before: mirage_source3_male_1024, after: mirage_exercise3_result },
  ]}
/>
*Shatter and Explode — simulated result across source images.*
**Source**: Any video with strong visual structure — faces, architecture, or color bars.

**Objective**: Use the shatter surface to break the image into displaced horizontal strips.

1. Set Surface to Shatter (Toggle 7 On, Toggle 9 On, Toggle 8 Off — value 5).
2. Set Curvature to 0% — the strips are aligned and the image looks normal.
3. Slowly increase Curvature. Horizontal strips begin displacing alternately left and right.
4. At high Curvature, the image explodes into offset bands that no longer form a coherent picture.
5. Set Background to White (mode 1) so the gaps between strips are visible.
6. Compare Shatter with Cone (Toggle 9 On, others Off — value 4) to see perspective narrowing instead.

**Key concepts**: Shatter displaces horizontal strips alternately based on vertical position, strip size is 16 pixels (v_count bits 8:4), Curvature controls displacement magnitude, no shading on shatter

---


## Tips

- **Surface selector is binary**: The three Surface toggles form a 3-bit number (0–7), not three independent controls. Learn the binary mapping to quickly select any of the six surface types.
- **Curvature at zero is flat**: Setting Curvature to 0 on any surface type produces a nearly undistorted image — useful as a starting point before dialing in the effect.
- **Shading only works on curves**: The perspective shading effect only engages on Cylinder and Sphere. On Flag, Cone, and Shatter, the Shading knob does nothing.
- **Background color sets the mood**: Black background creates a floating-object look; white creates a bright studio feel; blue approximates broadcast chroma key.
- **Rotation speed is frame-locked**: The DDS increments once per frame, so animation smoothness depends on the video frame rate. At very high Rotation values, the surface appears to jump rather than rotate smoothly.
- **Mix for compositing**: At mid-Mix values, the flat and distorted images overlap, creating a ghostly double-exposure of the original and warped video.
- **Flag for organic motion**: The Flag surface with moderate Curvature and slow Rotation produces a convincing cloth-like ripple that works beautifully with natural imagery.
- **Scale zooms the surface**: Low Scale values zoom into the surface (less distortion visible), high values zoom out (entire surface visible with more distortion).

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for scanline buffer storage. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Coordinate Remapping** | Computing a displaced source address for each output pixel, creating the illusion of geometric transformation. |
| **DDS** | Direct Digital Synthesis; a phase accumulator technique used here to drive continuous animation of the surface transformation. |
| **Edge Masking** | Replacing pixels that fall outside valid source bounds with a background fill color. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **LUT** | Look-Up Table; a pre-computed array of values (here, sine and cosine) indexed by angle for fast trigonometric evaluation. |
| **Perspective Shading** | Darkening surface regions that face away from the viewer, based on the cosine of the surface normal angle. |
| **Phase Accumulator** | A counter that adds a fixed increment each cycle, producing a linearly increasing phase angle that wraps modulo 2π. |
| **Quantel** | A British company that pioneered real-time digital video effects hardware in the 1980s. |
| **Scanline Buffer** | BRAM storage holding one or more complete video lines, enabling random-access reads for coordinate remapping. |
| **Surface Equation** | The mathematical function that maps output pixel coordinates to displaced source coordinates for a given 3D surface type. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
