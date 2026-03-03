---
draft: true
sidebar_position: 337
slug: /instruments/videomancer/wobbulator
title: "Wobbulator"
image: /img/instruments/videomancer/wobbulator/wobbulator_hero_s1.png
description: "Wobbulator simulates the electromagnetic raster distortion made famous by Nam June Paik's 1965 \"Magnet TV,\" where a large magnet placed against a CRT bent the electron beam and warped the displayed image in organic, fluid curves."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import wobbulator_control_panel from '/img/instruments/videomancer/wobbulator/wobbulator_control_panel.png';
import wobbulator_source1_skull from '/img/instruments/videomancer/wobbulator/wobbulator_source1_skull.png';
import wobbulator_source2_fruit from '/img/instruments/videomancer/wobbulator/wobbulator_source2_fruit.png';
import wobbulator_source3_elephant from '/img/instruments/videomancer/wobbulator/wobbulator_source3_elephant.png';
import wobbulator_source4_pattern from '/img/instruments/videomancer/wobbulator/wobbulator_source4_pattern.png';
import wobbulator_source5_man from '/img/instruments/videomancer/wobbulator/wobbulator_source5_man.png';
import wobbulator_source6_berries from '/img/instruments/videomancer/wobbulator/wobbulator_source6_berries.png';
import wobbulator_hero_s1 from '/img/instruments/videomancer/wobbulator/wobbulator_hero_s1.png';
import wobbulator_hero_s2 from '/img/instruments/videomancer/wobbulator/wobbulator_hero_s2.png';
import wobbulator_hero_s3 from '/img/instruments/videomancer/wobbulator/wobbulator_hero_s3.png';
import wobbulator_hero_s4 from '/img/instruments/videomancer/wobbulator/wobbulator_hero_s4.png';
import wobbulator_hero_s5 from '/img/instruments/videomancer/wobbulator/wobbulator_hero_s5.png';
import wobbulator_hero_s6 from '/img/instruments/videomancer/wobbulator/wobbulator_hero_s6.png';
import wobbulator_ex1_s1 from '/img/instruments/videomancer/wobbulator/wobbulator_ex1_s1.png';
import wobbulator_ex1_s2 from '/img/instruments/videomancer/wobbulator/wobbulator_ex1_s2.png';
import wobbulator_ex1_s3 from '/img/instruments/videomancer/wobbulator/wobbulator_ex1_s3.png';
import wobbulator_ex1_s4 from '/img/instruments/videomancer/wobbulator/wobbulator_ex1_s4.png';
import wobbulator_ex1_s5 from '/img/instruments/videomancer/wobbulator/wobbulator_ex1_s5.png';
import wobbulator_ex1_s6 from '/img/instruments/videomancer/wobbulator/wobbulator_ex1_s6.png';
import wobbulator_ex2_s1 from '/img/instruments/videomancer/wobbulator/wobbulator_ex2_s1.png';
import wobbulator_ex2_s2 from '/img/instruments/videomancer/wobbulator/wobbulator_ex2_s2.png';
import wobbulator_ex2_s3 from '/img/instruments/videomancer/wobbulator/wobbulator_ex2_s3.png';
import wobbulator_ex2_s4 from '/img/instruments/videomancer/wobbulator/wobbulator_ex2_s4.png';
import wobbulator_ex2_s5 from '/img/instruments/videomancer/wobbulator/wobbulator_ex2_s5.png';
import wobbulator_ex2_s6 from '/img/instruments/videomancer/wobbulator/wobbulator_ex2_s6.png';
import wobbulator_ex3_s1 from '/img/instruments/videomancer/wobbulator/wobbulator_ex3_s1.png';
import wobbulator_ex3_s2 from '/img/instruments/videomancer/wobbulator/wobbulator_ex3_s2.png';
import wobbulator_ex3_s3 from '/img/instruments/videomancer/wobbulator/wobbulator_ex3_s3.png';
import wobbulator_ex3_s4 from '/img/instruments/videomancer/wobbulator/wobbulator_ex3_s4.png';
import wobbulator_ex3_s5 from '/img/instruments/videomancer/wobbulator/wobbulator_ex3_s5.png';
import wobbulator_ex3_s6 from '/img/instruments/videomancer/wobbulator/wobbulator_ex3_s6.png';

# Wobbulator

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: wobbulator_source1_skull, after: wobbulator_hero_s1 },
    { label: "Fruit", before: wobbulator_source2_fruit, after: wobbulator_hero_s2 },
    { label: "Elephant", before: wobbulator_source3_elephant, after: wobbulator_hero_s3 },
    { label: "Pattern", before: wobbulator_source4_pattern, after: wobbulator_hero_s4 },
    { label: "Man", before: wobbulator_source5_man, after: wobbulator_hero_s5 },
    { label: "Berries", before: wobbulator_source6_berries, after: wobbulator_hero_s6 },
  ]}
/>
*A radial magnetic warp pulls the centre of a test image inward, compressing scanlines near the focus point while stretching the surrounding field in concentric rings.*

---

## Overview

Wobbulator simulates the electromagnetic raster distortion made famous by Nam June Paik's 1965 "Magnet TV," where a large magnet placed against a CRT bent the electron beam and warped the displayed image in organic, fluid curves.  The program computes a per-pixel horizontal warp offset based on the Manhattan distance from a movable focus point.  Pixels near the focus are displaced strongly; those far away are displaced weakly, producing an inverse-distance falloff that compresses one region while stretching another.

The effect is implemented through a double-buffered scanline buffer.  As each line is written into one half of the buffer, the previous line is read from the other half using a displaced address pointer.  The displacement magnitude depends on the pixel's distance from the warp centre, scaled by Field Strength and shaped by Radius and Falloff.  In Attract mode pixels slide toward the focus, creating a visual whirlpool; in Repel mode they flee outward, producing a lens-like bulge.

Because the warp is computed per pixel in real time, the distortion responds instantaneously to parameter changes.  Moving Center X and Center Y sweeps the warp focal point across the screen while the source material continues playing — an experience that feels like pressing a magnet against a live television set.

---

## Background

### Nam June Paik and Magnet TV

In 1965, Korean-American artist Nam June Paik placed a large horseshoe magnet on top of an operating television set and exhibited the distorted result as "Magnet TV."  The external magnetic field deflected the CRT's electron beam, warping the raster in ways that shifted with the magnet's position and the TV's internal scan geometry.  Paik's gesture transformed the television from a broadcast receiver into a sculptural medium, founding the genre of video art.

### The Wobbulator

The term "Wobbulator" historically refers to a sweep oscillator used in radio and television alignment.  In the video art context, Paik and his collaborator Shuya Abe built custom wobbulators that injected modulated signals into the TV yoke coils, producing controllable geometric distortions.  These electronic interventions could create smooth, oscillating warp patterns that evolved in time — a bridge between the static magnet, the CRT, and abstract animation.

### Inverse-Distance Warping

The warp model in this program uses a simplified inverse-distance function.  For each pixel, the Manhattan distance to the focus point is computed.  The displacement is proportional to the field strength divided by the distance (clamped to prevent division by zero).  This produces concentric diamond-shaped contours — a natural consequence of the Manhattan metric — where pixels near the centre experience maximal displacement and those at the periphery remain nearly undisturbed.

### Scanline Buffering

Because the iCE40 FPGA has limited block RAM, only a single scanline of three YUV channels can be stored at once.  The double-buffer approach writes the incoming line into one bank while reading the warped output from the other, swapping banks every horizontal sync.  This means vertical warp is achieved indirectly — by adjusting how much of each line is compressed or stretched horizontally, the visual impression of vertical bending emerges.

### Dual Source Mode

When Sources is set to Dual, a second warp focus point is mirrored symmetrically about the screen centre.  The two fields combine additively, crossing where they overlap and producing interference-like patterns along the midline.  This recalls multimagnet sculptures where several magnets were arranged around a CRT, each bending the beam in a different direction.


---

## Signal Flow

```
          Input Video (Y/U/V per pixel)
                   │
         ┌─────────▼──────────┐
         │   Write Line Buffer │
         │  (bank A or B)      │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  Distance Compute   │
         │  |Δx| + |Δy| from  │
         │  focus point        │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  Warp Offset Calc   │
         │  strength / dist    │
         │  (attract / repel)  │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │ Read Line Buffer    │
         │  (bank B or A at    │
         │   displaced addr)   │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  Interpolator Mix   │
         │  (dry / wet fader)  │
         └─────────┬──────────┘
                   │
                Output Y/U/V
```

The key constraint is that warp is strictly horizontal: the line buffer holds one row, and the read address is offset along that row.  The perceived vertical warp is a visual artefact of horizontal compression — when pixels near the focus are pulled left or right, the brain interprets the resulting density change as vertical bending.  This is exactly how CRT magnetic deflection works: the magnet displaces the beam's horizontal scan, not the vertical, yet the image appears to bend in two dimensions.

The Falloff knob modifies the distance denominator, effectively widening or narrowing the warp field.  Low Falloff values concentrate the warp into a tight spot; high values spread it gently across the full screen.  Radius sets the maximum distance at which warp is applied, acting as a hard boundary beyond which displacement is zero.

---

## Parameter Reference

<img src={wobbulator_control_panel} alt="Videomancer front panel with Wobbulator loaded"/>
*Videomancer's front panel with Wobbulator active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Field Str
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Field Str sets the overall magnitude of the warp displacement.  At zero the image passes through unaltered; increasing Field Str pushes pixels progressively further from their original positions.  At maximum the warp is severe enough to fold the image, creating duplicated or mirrored strips where the read address wraps.  The visual effect is directly analogous to moving a magnet closer to or further from the CRT face.

---

#### Knob 2 — Center X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Center X positions the warp focus point along the horizontal axis.  At 50 % the focus is dead centre; at 0 % it sits on the left edge, and at 100 % on the right.  Moving Center X while the program is running drags the warp field across the image, creating a sweeping distortion that is the digital equivalent of sliding a magnet across the television screen.

---

#### Knob 3 — Center Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Center Y positions the warp focus point along the vertical axis.  Combined with Center X, this allows the focal point to be placed anywhere on the display.  Moving both knobs simultaneously traces a two-dimensional path for the warp centre, enabling freehand "magnetic drawing" on the video surface.

---

#### Knob 4 — Radius
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Radius defines the outer boundary of the warp field.  Pixels beyond this distance from the focus are left undisturbed regardless of Field Strength.  Small Radius values create a tight, localised dimple; large values allow the field to extend across the entire screen.  Setting Radius to its maximum makes the warp global, affecting every pixel proportionally.

---

#### Knob 5 — Drift Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Drift Spd controls the speed of the internal DDS phase accumulator that animates the focus point when the Animate toggle is active.  At zero the focus is static.  Increasing Drift Spd makes the focus circle slowly around its resting position, producing a rhythmic, breath-like undulation.  At high values the circular motion becomes fast enough to create visual blurring.

---

#### Knob 6 — Falloff
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Falloff adjusts how sharply the displacement diminishes with distance.  Low Falloff makes the warp field steep — high displacement at the focus dropping quickly to zero.  High Falloff produces a gentle, spread-out field where even distant pixels experience moderate warping.  This parameter is the inverse of the damping coefficient in the magnetic analogy: more Falloff ≈ weaker spring ≈ wider influence.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Polarity** | Attract | Repel |
| **8 — Sources** | Single | Dual |
| **9 — Animate** | Off | On |
| **10 — Chroma Warp** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into character controls and utility.  Polarity is the single most dramatic switch — flipping from Attract to Repel inverts all displacement directions, turning a vortex into a bulge.  Sources doubles the warp field symmetrically, and Animate sets the focus in orbital motion.  Chroma Warp adds channel-dependent offsets for prismatic fringing.  Bypass passes the signal through unchanged.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the warped wet output.  At zero the output is the unmodified source; at maximum it is the fully warped signal.  Intermediate values blend the two, creating a ghost effect where the original image appears faintly beneath the distorted version.

---

## Guided Exercises

These exercises explore the core behaviours of magnetic warping, from simple single-point attraction to animated dual-source interference.

### Exercise 1: Magnet On Glass

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: wobbulator_source1_skull, after: wobbulator_ex1_s1 },
    { label: "Fruit", before: wobbulator_source2_fruit, after: wobbulator_ex1_s2 },
    { label: "Elephant", before: wobbulator_source3_elephant, after: wobbulator_ex1_s3 },
    { label: "Pattern", before: wobbulator_source4_pattern, after: wobbulator_ex1_s4 },
    { label: "Man", before: wobbulator_source5_man, after: wobbulator_ex1_s5 },
    { label: "Berries", before: wobbulator_source6_berries, after: wobbulator_ex1_s6 },
  ]}
/>
*Magnet On Glass — simulated result across source images.*
**Source**: A high-contrast graphic — text, a test pattern, or a grid — works best to reveal warping geometry.

**Objective**: Create a classic magnet-on-CRT effect with a single attraction point at the screen centre.

1. Set Center X and Center Y both to 50 % to place the focus at the centre.
2. Set Field Str to 50 % and Radius to 70 %.
3. Confirm Polarity is Attract and Sources is Single.
4. Observe the image pulling inward toward the centre, compressing in the middle and stretching at the edges.
5. Slowly increase Field Str and watch the distortion deepen.
6. Drag Center X from 0 % to 100 % — the warp slides across the screen like moving a magnet.

**Key concepts**: - Inverse-distance falloff produces concentrated central warping
- Manhattan distance creates diamond-shaped warp contours
- Horizontal line buffer means warp is strictly horizontal but appears two-dimensional

---

### Exercise 2: Dual Field Interference

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: wobbulator_source1_skull, after: wobbulator_ex2_s1 },
    { label: "Fruit", before: wobbulator_source2_fruit, after: wobbulator_ex2_s2 },
    { label: "Elephant", before: wobbulator_source3_elephant, after: wobbulator_ex2_s3 },
    { label: "Pattern", before: wobbulator_source4_pattern, after: wobbulator_ex2_s4 },
    { label: "Man", before: wobbulator_source5_man, after: wobbulator_ex2_s5 },
    { label: "Berries", before: wobbulator_source6_berries, after: wobbulator_ex2_s6 },
  ]}
/>
*Dual Field Interference — simulated result across source images.*
**Source**: A camera or any spatially detailed source with large regions of mid-brightness.

**Objective**: Create symmetrical warp fields with two focal points and observe the interference between them.

1. Set Field Str to 40 % and Sources to Dual.
2. Set Center X and Center Y to 50 % — the two fields are symmetric about centre.
3. Increase Falloff to 80 % for broad fields.
4. Note the central axis where the two fields oppose, creating a pinch or fold.
5. Toggle Polarity between Attract and Repel and observe the inverted geometry.
6. Move Center X away from 50 % to separate the focal points further.

**Key concepts**: - Dual sources produce mirrored symmetric warp
- Additive displacement creates constructive and destructive interference
- Polarity inversion reverses the entire field geometry

---

### Exercise 3: Animated Chromatic Wobble

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: wobbulator_source1_skull, after: wobbulator_ex3_s1 },
    { label: "Fruit", before: wobbulator_source2_fruit, after: wobbulator_ex3_s2 },
    { label: "Elephant", before: wobbulator_source3_elephant, after: wobbulator_ex3_s3 },
    { label: "Pattern", before: wobbulator_source4_pattern, after: wobbulator_ex3_s4 },
    { label: "Man", before: wobbulator_source5_man, after: wobbulator_ex3_s5 },
    { label: "Berries", before: wobbulator_source6_berries, after: wobbulator_ex3_s6 },
  ]}
/>
*Animated Chromatic Wobble — simulated result across source images.*
**Source**: A medium-contrast camera feed or colour bars.

**Objective**: Produce a slow, rhythmic wobble with prismatic colour fringing.

1. Set Field Str to 30 %, Radius to 60 %, Drift Spd to 40 %.
2. Enable Animate and Chroma Warp.
3. Observe the focus point orbiting around the centre, producing a rhythmic wobble.
4. Watch for rainbow fringing especially visible along high-contrast edges.
5. Increase Drift Spd to 80 % for faster motion, then back down and increase Falloff for wider influence.

**Key concepts**: - Animate uses a DDS phase accumulator for smooth orbital motion
- Chroma Warp separates Y/U/V displacements for prismatic fringing
- Drift Spd and Falloff together control the spatial and temporal scale of the wobble

---


## Tips

- **Start subtle:** Begin with Field Str around 20–30 % to get a gentle CRT-era wobble before dialling up to extreme values.
- **Use a grid source:** A grid or test pattern reveals the warp geometry most clearly — you can see exactly which pixels are displaced and by how much.
- **Move the focus live:** The most expressive use of Wobbulator is manual focus point sweeping — slowly dragging Center X and Center Y during a performance creates the feeling of holding a magnet against the screen.
- **Dual for symmetry:** Switch to Dual Sources whenever you want bilateral symmetry — useful for Rorschach-like effects or for centring an abstract composition.
- **Chroma Warp sparingly:** A little chromatic fringing adds realism to the CRT simulation; too much starts to look like a calibration error rather than an artistic choice.
- **Chain with feedback:** Routing Wobbulator's output back through a feedback delay creates ever-deepening recursive distortion, mimicking the cascading deflection of real multi-magnet setups.
- **Low Falloff for precision:** When you want a surgical, localised dimple in the image, reduce Falloff to concentrate the field tightly around the focus point.

---
