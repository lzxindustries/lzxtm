---
draft: true
sidebar_position: 183
slug: /instruments/videomancer/macrame
title: "Macrame"
image: /img/instruments/videomancer/macrame/macrame_hero_s1.png
description: "Fiber arts begin with repetition — a single knot tied again and again until a flat cord becomes a surface."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import macrame_control_panel from '/img/instruments/videomancer/macrame/macrame_control_panel.png';
import macrame_source1_field from '/img/instruments/videomancer/macrame/macrame_source1_field.png';
import macrame_source2_ballerina from '/img/instruments/videomancer/macrame/macrame_source2_ballerina.png';
import macrame_source3_collage from '/img/instruments/videomancer/macrame/macrame_source3_collage.png';
import macrame_source4_pattern from '/img/instruments/videomancer/macrame/macrame_source4_pattern.png';
import macrame_source5_boy from '/img/instruments/videomancer/macrame/macrame_source5_boy.png';
import macrame_source6_wood from '/img/instruments/videomancer/macrame/macrame_source6_wood.png';
import macrame_hero_s1 from '/img/instruments/videomancer/macrame/macrame_hero_s1.png';
import macrame_hero_s2 from '/img/instruments/videomancer/macrame/macrame_hero_s2.png';
import macrame_hero_s3 from '/img/instruments/videomancer/macrame/macrame_hero_s3.png';
import macrame_hero_s4 from '/img/instruments/videomancer/macrame/macrame_hero_s4.png';
import macrame_hero_s5 from '/img/instruments/videomancer/macrame/macrame_hero_s5.png';
import macrame_hero_s6 from '/img/instruments/videomancer/macrame/macrame_hero_s6.png';
import macrame_ex1_s1 from '/img/instruments/videomancer/macrame/macrame_ex1_s1.png';
import macrame_ex1_s2 from '/img/instruments/videomancer/macrame/macrame_ex1_s2.png';
import macrame_ex1_s3 from '/img/instruments/videomancer/macrame/macrame_ex1_s3.png';
import macrame_ex1_s4 from '/img/instruments/videomancer/macrame/macrame_ex1_s4.png';
import macrame_ex1_s5 from '/img/instruments/videomancer/macrame/macrame_ex1_s5.png';
import macrame_ex1_s6 from '/img/instruments/videomancer/macrame/macrame_ex1_s6.png';
import macrame_ex2_s1 from '/img/instruments/videomancer/macrame/macrame_ex2_s1.png';
import macrame_ex2_s2 from '/img/instruments/videomancer/macrame/macrame_ex2_s2.png';
import macrame_ex2_s3 from '/img/instruments/videomancer/macrame/macrame_ex2_s3.png';
import macrame_ex2_s4 from '/img/instruments/videomancer/macrame/macrame_ex2_s4.png';
import macrame_ex2_s5 from '/img/instruments/videomancer/macrame/macrame_ex2_s5.png';
import macrame_ex2_s6 from '/img/instruments/videomancer/macrame/macrame_ex2_s6.png';
import macrame_ex3_s1 from '/img/instruments/videomancer/macrame/macrame_ex3_s1.png';
import macrame_ex3_s2 from '/img/instruments/videomancer/macrame/macrame_ex3_s2.png';
import macrame_ex3_s3 from '/img/instruments/videomancer/macrame/macrame_ex3_s3.png';
import macrame_ex3_s4 from '/img/instruments/videomancer/macrame/macrame_ex3_s4.png';
import macrame_ex3_s5 from '/img/instruments/videomancer/macrame/macrame_ex3_s5.png';
import macrame_ex3_s6 from '/img/instruments/videomancer/macrame/macrame_ex3_s6.png';

# Macrame

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: macrame_source1_field, after: macrame_hero_s1 },
    { label: "Ballerina", before: macrame_source2_ballerina, after: macrame_hero_s2 },
    { label: "Collage", before: macrame_source3_collage, after: macrame_hero_s3 },
    { label: "Pattern", before: macrame_source4_pattern, after: macrame_hero_s4 },
    { label: "Boy", before: macrame_source5_boy, after: macrame_hero_s5 },
    { label: "Wood", before: macrame_source6_wood, after: macrame_hero_s6 },
  ]}
/>
*Macrame overlaying a knotted diamond cord lattice with textured intersections across a video source.*

---

## Overview

Fiber arts begin with repetition — a single knot tied again and again until a flat cord becomes a surface. Macrame brings that principle to the pixel grid. The program generates a lattice of diagonal cord lines across the screen, placing thickened knot circles at every intersection, and composites the result over the input video. The pattern tiles seamlessly because its repeat distances are always powers of two, locking the lattice to the binary structure of the pixel coordinates.

The name comes from the textile craft of the same name — decorative knotwork made by tying cords into geometric patterns rather than weaving or knitting them. Traditional macramé produces diamond, chevron, and spiral motifs from nothing but cord and repetition. This program translates those geometric rules into modular-arithmetic tests on horizontal and vertical pixel addresses.

At low Cord Spacing values the lattice is dense, almost like a mesh screen overlaid on the video. At high values the diamonds open up into wide cells with prominent knot circles. The Brightness control sets the luminance level of the cord structure itself, while the Overlay toggle determines whether the cords add light to the source or replace it entirely.

---

## Quick Start

1. **Cell size jumps**: Cord Spacing steps through six discrete sizes. If you need a specific density, remember that the transitions happen at roughly 15%, 29%, 43%, 57%, 71% of the pot range.
2. **Knot visibility**: Knots are brightest at the center and draw at 75% of the Brightness setting. If knots are too subtle, increase both Knot Size and Brightness together.
3. **Dark backgrounds for additive**: Additive overlay is most visible against dark source material. Bright sources wash out the lattice. Use replace mode for consistent visibility.

---

## Background

### Diagonal Lattice Geometry

The core of Macrame is the diagonal coordinate transform. Two new axes are derived from the pixel position: the *sum* axis (h + v) and the *difference* axis (h − v). Lines of constant sum run at −45° and lines of constant difference run at +45°. Testing whether the sum or difference, modulo a cell size, falls below a thickness threshold draws two sets of evenly spaced diagonal lines crossing the screen. Where both sets of lines overlap, a knot point appears. This is identical to the mathematical construction of a diamond lattice from two families of parallel diagonals.

### Power-of-Two Tiling

Rather than dividing by an arbitrary repeat distance (which costs an FPGA divider), Macrame masks the diagonal coordinates with a bitmask to extract the fractional position within a repeating cell. The available cell sizes — 8, 16, 32, 64, 128, and 256 pixels — are all powers of two, so the modulus operation reduces to a bitwise AND. This makes the repeat perfectly seamless and costs zero DSP resources. The Cord Spacing pot selects which mask is active, stepping through the six sizes across its range.

### Manhattan Distance for Knot Detection

At each pixel, the program computes the distance to the nearest lattice intersection. True Euclidean distance would require a multiply and square-root, which are expensive on a small FPGA. Instead Macrame uses the Manhattan distance (|dx| + |dy|), which approximates a circle as a diamond shape. The Knot Size control sets the radius threshold: any pixel whose Manhattan distance from the nearest intersection falls below this value is drawn as part of the knot rather than the cord. The result is a slightly faceted circle that reads as round from normal viewing distance.

### LFSR Texture Noise

Real cord is not perfectly uniform — fibers catch light unevenly, knots have visible texture, and natural dyes create subtle variation. Macrame adds a pseudo-random noise offset from a 16-bit linear feedback shift register to the brightness of every cord and knot pixel. The noise is small (6 bits, or about 6% of full scale) but enough to break the mechanical perfection of the digital lattice and give the cords an organic, tactile quality.

### Overlay Compositing

The program offers two compositing modes for combining the cord pattern with the input video. In additive mode, the cord brightness is added to the source — the lattice glows over the image, and black regions of the source show the cord pattern most clearly. In replace mode, cord pixels completely overwrite the source — the lattice becomes opaque, punching through the video wherever a cord or knot falls. Background pixels (where no cord is drawn) pass the source through with a very slight dimming to increase depth contrast.


---

## Signal Flow

Input Register → Cord Test → Cord → Overlay Blend + Clamp

```
Input Video (YUV 4:4:4)
│
├── Parameter Pre-Registration
│   ├─ Cord Spacing → bitmask select (8/16/32/64/128/256 px)
│   ├─ Knot Size → knot radius (top 8 bits)
│   ├─ Cord Thickness → line threshold (top 4 bits → 1..16)
│   ├─ Angle → vertical offset for diagonal skew
│   └─ Brightness → cord luminance level
│
├── Stage 1: Input Register + Diagonal Sums
│   ├─ Latch Y/U/V input
│   ├─ h_pos = h_count [+ frame_count if Animate]
│   ├─ v_pos = v_count + angle_offset
│   ├─ diag_sum  = h_pos + v_pos
│   ├─ diag_diff = |h_pos − v_pos|
│   └─ frac_sum/frac_diff = diag & space_mask
│
├── Stage 2: Cord Test + Knot Detection + Noise
│   ├─ dist_a = min(frac_sum, cell_size − frac_sum)
│   ├─ dist_b = min(frac_diff, cell_size − frac_diff)
│   ├─ on_cord_a = dist_a < cord_thresh
│   ├─ on_cord_b = dist_b < cord_thresh
│   ├─ knot_dist = dist_a + dist_b
│   ├─ is_knot = knot_dist < knot_radius
│   └─ noise_val = LFSR[5:0]
│
├── Stage 3: Cord/Knot Color Compose + Depth Shading
│   ├─ Knot: Y = bright×0.75 + noise, UV = neutral or warm tint
│   ├─ Cord: Y = bright×0.75 + noise(÷4), UV = neutral or slight tint
│   └─ Background: pass source Y/U/V
│
├── Stage 4: Overlay Blend + Clamp
│   ├─ Additive: Y_out = Y_src + pattern_Y/2 (clamped)
│   │   UV_out = avg(UV_src, UV_pattern)
│   ├─ Replace: Y_out = pattern_Y, UV_out = pattern_UV
│   └─ Background: Y_out = Y_src − Y_src/16
│
├── Interpolator (4 clocks)
│   └─ Mix: lerp(dry, wet, mix_amount) per Y/U/V
│
└── Output Mux
    └─ Bypass=On: pass delayed input; Bypass=Off: output mix result
```

The diagonal coordinate transform is the architectural heart of the program. By computing h+v and |h−v| and masking to the cell size, two independent modular-distance tests generate intersecting diagonal line families without any division or trigonometry. The knot detection is a natural byproduct — it fires wherever both line tests report a small distance simultaneously, which geometrically corresponds to the lattice intersection points.

The overlay stage's additive mode adds half the pattern brightness to the source, which means the cord structure is most visible against dark backgrounds and washes out against bright areas. Replace mode makes the lattice opaque regardless of source content. The slight dimming applied to background pixels (source minus source/16, roughly 6% darker) provides depth contrast that makes the cord structure appear to sit in front of the video.

---

## Parameter Reference

<img src={macrame_control_panel} alt="Videomancer front panel with Macrame loaded"/>
*Videomancer's front panel with Macrame active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cord Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the repeat distance of the lattice by selecting one of six power-of-two cell sizes: 8, 16, 32, 64, 128, or 256 pixels. The pot range is divided into six equal bands. Small cell sizes create a fine, dense mesh; large cell sizes produce wide-open diamond shapes with prominent knot circles. Because the sizes are powers of two, transitions between bands are abrupt — you step from one grid density to the next rather than smoothly sweeping.

---

#### Knob 2 — Knot Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the radius of the knot circles at lattice intersections. The top 8 bits of the register are used directly as a pixel distance threshold, giving a range from very small dots (barely visible at 2 pixels) to large circles (up to 32 pixels radius, visually dominant). Larger knots overlap the cord lines and create a more solid, heavy appearance at the intersections. At zero, no knots are drawn and the output is pure cord lines.

---

#### Knob 3 — Cord Thk
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the thickness of the cord lines. The top 4 bits of the register map to a threshold of 1 to 16 pixels. At minimum, the cords are hairline single-pixel diagonals. At maximum, each cord becomes a broad band 16 pixels wide. Thick cords with large knots create a heavy, woven appearance; thin cords with small knots produce a delicate filigree overlay.

---

#### Knob 4 — Angle
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Tilts the lattice by adding a vertical offset derived from the bottom 8 bits of the register. At center position the lattice is symmetric, with diagonals at ±45°. Turning the knob skews the vertical component, making one family of diagonals steeper and the other shallower. The effect is subtle at small values and increasingly distorted as you approach the extremes, stretching the diamond shapes into parallelograms.

---

#### Knob 5 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At zero, the pattern is completely dark — invisible in additive mode, black lines in replace mode. At maximum, the cords are full brightness. Knots receive 75% of this brightness level plus noise; cord lines receive a slightly lower fraction. This control directly sets the visual weight of the textile overlay against the source video. Internally, sets the luminance level of the cord and knot pixels.

---

#### Knob 6 — Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Declared and mapped to the register but not referenced in the processing pipeline. Adjusting this control has no visible effect on the output. It is reserved for a future depth-shading feature that would darken cords based on their distance from the viewer or their position in the lattice cell.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Diamond | Chevron |
| **8 — Color** | Cream | Source |
| **9 — Overlay** | Add | Multiply |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 each use a single VHDL bit despite having four TOML labels. In practice they behave as binary switches — the first label maps to bit=0 and the remaining labels map to bit=1. Toggle 9 selects between additive and replace compositing. Toggle 10 enables frame-by-frame animation drift. Toggle 11 is a standard bypass.

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

Wet/dry crossfade between the original (dry) signal and the Macrame-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises build from basic lattice construction to full textile overlay compositing. Each one highlights a different aspect of the cord geometry and its interaction with the source video.

### Exercise 1: Diamond Lattice Construction

<BeforeAfterSlider
  sources={[
    { label: "Field", before: macrame_source1_field, after: macrame_ex1_s1 },
    { label: "Ballerina", before: macrame_source2_ballerina, after: macrame_ex1_s2 },
    { label: "Collage", before: macrame_source3_collage, after: macrame_ex1_s3 },
    { label: "Pattern", before: macrame_source4_pattern, after: macrame_ex1_s4 },
    { label: "Boy", before: macrame_source5_boy, after: macrame_ex1_s5 },
    { label: "Wood", before: macrame_source6_wood, after: macrame_ex1_s6 },
  ]}
/>
*Diamond Lattice Construction — simulated result across source images.*
**Source**: A medium-contrast camera feed or recorded footage with recognizable subjects and some dark regions.

**What You'll Create**: Understand how cord spacing, thickness, and knot size combine to form the basic lattice.

1. **Open grid**: Set Cord Spacing to about 70% to select the 128-pixel cell size. The lattice will have widely spaced diagonals.
2. **Thin cords**: Set Cord Thickness to about 20%. Hairline diagonal lines appear over the video.
3. **Add knots**: Increase Knot Size from zero to about 40%. Bright dots appear at every intersection.
4. **Thicken cords**: Increase Cord Thickness to about 60%. The cord lines widen and begin to merge with the knots.
5. **Dense grid**: Lower Cord Spacing to about 20% to switch to a smaller cell size. The lattice becomes a fine mesh.
6. **Full brightness**: Set Brightness to 80%. The lattice becomes a strong overlay.

**Key concepts**: Power-of-two cell sizes create abrupt grid transitions, Manhattan distance knots are diamond-shaped up close, cord thickness and knot size are independent parameters

---

### Exercise 2: Colored Textile Overlay

<BeforeAfterSlider
  sources={[
    { label: "Field", before: macrame_source1_field, after: macrame_ex2_s1 },
    { label: "Ballerina", before: macrame_source2_ballerina, after: macrame_ex2_s2 },
    { label: "Collage", before: macrame_source3_collage, after: macrame_ex2_s3 },
    { label: "Pattern", before: macrame_source4_pattern, after: macrame_ex2_s4 },
    { label: "Boy", before: macrame_source5_boy, after: macrame_ex2_s5 },
    { label: "Wood", before: macrame_source6_wood, after: macrame_ex2_s6 },
  ]}
/>
*Colored Textile Overlay — simulated result across source images.*
**Source**: High-contrast footage with dark backgrounds — stage performance, night scenes, or silhouettes.

**What You'll Create**: Explore color modes and overlay compositing against varied source brightness.

1. **Set medium lattice**: Cord Spacing ~50%, Knot Size ~50%, Cord Thickness ~40%, Brightness ~70%.
2. **Additive over dark**: With Overlay set to Add, observe how the lattice glows brightly against dark areas of the source and washes out against bright areas.
3. **Color tint**: Switch Color to the tinted mode (toggle high). The cords take on a warm cream-brown hue resembling natural hemp rope.
4. **Replace mode**: Switch Overlay to Multiply (replace). The lattice now punches through the video as an opaque layer.
5. **Angle tilt**: Sweep Angle from 0% to 100%. Watch the diamond shapes distort into parallelograms as the vertical skew increases.
6. **Mix blend**: Lower Mix to about 50% to blend the lattice subtly with the source.

**Key concepts**: Additive compositing is source-dependent (bright sources hide the lattice), replace compositing is absolute, color tint adds chroma offset to the neutral cord brightness

---

### Exercise 3: Animated Lattice Drift

<BeforeAfterSlider
  sources={[
    { label: "Field", before: macrame_source1_field, after: macrame_ex3_s1 },
    { label: "Ballerina", before: macrame_source2_ballerina, after: macrame_ex3_s2 },
    { label: "Collage", before: macrame_source3_collage, after: macrame_ex3_s3 },
    { label: "Pattern", before: macrame_source4_pattern, after: macrame_ex3_s4 },
    { label: "Boy", before: macrame_source5_boy, after: macrame_ex3_s5 },
    { label: "Wood", before: macrame_source6_wood, after: macrame_ex3_s6 },
  ]}
/>
*Animated Lattice Drift — simulated result across source images.*
**Source**: Slow-moving or static footage — landscapes, architecture, or a fixed camera feed.

**What You'll Create**: Combine animation, fine lattice density, and strong overlay for an evolving textile texture.

1. **Fine lattice**: Set Cord Spacing to about 15% for the densest cell size. Cord Thickness ~30%, Knot Size ~30%.
2. **Enable animation**: Switch Animate to On. The lattice begins drifting diagonally.
3. **Brightness modulation**: Set Brightness to about 60% — moderate overlay intensity.
4. **Replace mode**: Switch Overlay to Multiply. The lattice is opaque with the source visible in the gaps.
5. **Color**: Switch to tinted mode for warm cord color.
6. **Angle**: Set Angle to about 30% for a slight skew.
7. **Observe**: Watch the drifting lattice interact with the static or slow-moving source. The fine grid creates a moire-like shimmer.

**Key concepts**: Animation increments the horizontal offset once per frame, fine lattice creates moire interaction with video detail, replace mode makes the drift more visible than additive

---


## Tips

- **Angle for asymmetry**: A small Angle offset breaks the rotational symmetry of the diamond lattice, creating parallelogram cells that feel more hand-crafted.
- **Color tint is subtle**: The warm tint shifts chroma by only 20–40 counts on a 1024-count scale. It is most visible against neutral or cool-toned source material.
- **Animation speed is fixed**: The drift is one pixel per frame regardless of any control setting. For slower drift, use the Mix control to blend less of the animated signal.
- **Depth does nothing**: Pot 6 is reserved for future use. Do not expect any visual change from it.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chroma** | Color information in a video signal, encoded as U and V offsets from neutral gray in YUV color space. |
| **Diagonal Sum / Difference** | h+v and |h−v| coordinate transforms that create ±45° line families across the pixel grid. |
| **LFSR** | Linear Feedback Shift Register; a simple pseudo-random number generator used here for cord texture noise. |
| **Luma** | Brightness component (Y) of a YUV video signal. |
| **Manhattan Distance** | The sum of absolute coordinate differences (|dx|+|dy|), producing diamond-shaped distance contours instead of circles. |
| **Power-of-Two** | Values like 8, 16, 32, 64, 128, 256 that allow modular arithmetic via bitwise AND instead of division. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage for brightness and contrast. |

---
