---
draft: true
sidebar_position: 159
slug: /instruments/videomancer/keystone
title: "Keystone"
image: /img/instruments/videomancer/keystone/keystone_hero_s1.png
description: "Most video is captured as a rectangle, and most displays reproduce it as a rectangle."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import keystone_control_panel from '/img/instruments/videomancer/keystone/keystone_control_panel.png';
import keystone_source1_field from '/img/instruments/videomancer/keystone/keystone_source1_field.png';
import keystone_source2_car from '/img/instruments/videomancer/keystone/keystone_source2_car.png';
import keystone_source3_elephant from '/img/instruments/videomancer/keystone/keystone_source3_elephant.png';
import keystone_source4_pattern from '/img/instruments/videomancer/keystone/keystone_source4_pattern.png';
import keystone_source5_woman from '/img/instruments/videomancer/keystone/keystone_source5_woman.png';
import keystone_source6_knit from '/img/instruments/videomancer/keystone/keystone_source6_knit.png';
import keystone_hero_s1 from '/img/instruments/videomancer/keystone/keystone_hero_s1.png';
import keystone_hero_s2 from '/img/instruments/videomancer/keystone/keystone_hero_s2.png';
import keystone_hero_s3 from '/img/instruments/videomancer/keystone/keystone_hero_s3.png';
import keystone_hero_s4 from '/img/instruments/videomancer/keystone/keystone_hero_s4.png';
import keystone_hero_s5 from '/img/instruments/videomancer/keystone/keystone_hero_s5.png';
import keystone_hero_s6 from '/img/instruments/videomancer/keystone/keystone_hero_s6.png';
import keystone_ex1_s1 from '/img/instruments/videomancer/keystone/keystone_ex1_s1.png';
import keystone_ex1_s2 from '/img/instruments/videomancer/keystone/keystone_ex1_s2.png';
import keystone_ex1_s3 from '/img/instruments/videomancer/keystone/keystone_ex1_s3.png';
import keystone_ex1_s4 from '/img/instruments/videomancer/keystone/keystone_ex1_s4.png';
import keystone_ex1_s5 from '/img/instruments/videomancer/keystone/keystone_ex1_s5.png';
import keystone_ex1_s6 from '/img/instruments/videomancer/keystone/keystone_ex1_s6.png';
import keystone_ex2_s1 from '/img/instruments/videomancer/keystone/keystone_ex2_s1.png';
import keystone_ex2_s2 from '/img/instruments/videomancer/keystone/keystone_ex2_s2.png';
import keystone_ex2_s3 from '/img/instruments/videomancer/keystone/keystone_ex2_s3.png';
import keystone_ex2_s4 from '/img/instruments/videomancer/keystone/keystone_ex2_s4.png';
import keystone_ex2_s5 from '/img/instruments/videomancer/keystone/keystone_ex2_s5.png';
import keystone_ex2_s6 from '/img/instruments/videomancer/keystone/keystone_ex2_s6.png';
import keystone_ex3_s1 from '/img/instruments/videomancer/keystone/keystone_ex3_s1.png';
import keystone_ex3_s2 from '/img/instruments/videomancer/keystone/keystone_ex3_s2.png';
import keystone_ex3_s3 from '/img/instruments/videomancer/keystone/keystone_ex3_s3.png';
import keystone_ex3_s4 from '/img/instruments/videomancer/keystone/keystone_ex3_s4.png';
import keystone_ex3_s5 from '/img/instruments/videomancer/keystone/keystone_ex3_s5.png';
import keystone_ex3_s6 from '/img/instruments/videomancer/keystone/keystone_ex3_s6.png';

# Keystone

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: keystone_source1_field, after: keystone_hero_s1 },
    { label: "Car", before: keystone_source2_car, after: keystone_hero_s2 },
    { label: "Elephant", before: keystone_source3_elephant, after: keystone_hero_s3 },
    { label: "Pattern", before: keystone_source4_pattern, after: keystone_hero_s4 },
    { label: "Woman", before: keystone_source5_woman, after: keystone_hero_s5 },
    { label: "Knit", before: keystone_source6_knit, after: keystone_hero_s6 },
  ]}
/>
*Keystone applying horizontal perspective foreshortening and skew to transform rectangular video into converging trapezoids.*

---

## Overview

Most video is captured as a rectangle, and most displays reproduce it as a rectangle. But the world is full of non-rectangular projections — oblique buildings, roads receding to a vanishing point, signs viewed at an angle. Keystone takes a rectangular input and reshapes it into a parallelogram (skew) or trapezoid (perspective), simulating the kind of geometric distortion that comes from viewing a surface at an angle.

The program works per-scanline: each horizontal line of the output is read from a different starting position and at a different sampling rate than its neighbors. Skew shifts every line by an amount proportional to its vertical position, converting the rectangle to a slanted parallelogram. Perspective scales each line's width proportionally to its distance from a configurable vanishing point, producing a trapezoid that converges toward that point. Both transforms can be combined for arbitrary quadrilateral mapping.

An internal oscillator can animate either the skew or perspective parameter automatically using sine or triangle wave modulation. This creates a rhythmic rocking or breathing effect — the image tilts and converges in time without any external modulation source. The name "Keystone" comes from the trapezoidal distortion seen in projectors when the projector axis is not perpendicular to the screen — the same geometry this program deliberately introduces.

---

## Quick Start

1. **Start at center**: Both Skew and Perspctv have their neutral position at center. The image is undistorted only when both are at 50%.
2. **VP Y is powerful**: Moving the vanishing point while perspective is active dramatically reshapes the distortion. Try VP Y at 0% for "looking down at the floor" and 100% for "looking up at a ceiling."
3. **Smear vs Black**: Black border creates clean mattes suitable for compositing. Smear border creates abstract edge-stretch effects useful for visual texture.

---

## Background

### Perspective Projection in Two Dimensions

In three-dimensional graphics, perspective projection maps a 3D scene onto a 2D plane such that objects farther from the camera appear smaller. Keystone implements a simplified version of this for a 2D video signal: each horizontal line is scaled by a factor that varies linearly with its vertical position. Lines near the vanishing point are compressed (read at a wider sampling step), and lines far from the vanishing point are stretched (read at a narrower step). The result is a trapezoid — wider at one end, narrower at the other — that mimics the appearance of a flat surface tilted away from the viewer.

### Skew and Shear Transforms

A shear transform displaces every point in an image by an amount proportional to its perpendicular distance from a reference axis. In Keystone, horizontal shear displaces each scanline left or right based on its vertical position. Lines at the top shift one direction, lines at the bottom shift the other, and the center remains stationary. The rectangle becomes a parallelogram. This is the geometric equivalent of tilting a deck of cards — each card slides relative to its neighbors.

### DDA Resampling

The Digital Differential Analyzer (DDA) is a classic algorithm for rasterizing lines and sampling at non-integer coordinates. Keystone uses a DDA accumulator to step through the source pixel addresses at a variable rate for each output scanline. When the step size equals 1.0, the output is a 1:1 copy. When it is greater than 1.0, the source is compressed (more source pixels are traversed per output pixel). When less than 1.0, the source is stretched. The DDA provides sub-pixel precision through its fractional accumulator, and the boundary check logic ensures clean handling of out-of-range addresses.

### Line Buffers and Ping-Pong Access

Keystone uses three dual-port line buffers (one each for Y, U, V) to decouple the input write order from the output read order. While one buffer bank stores the current incoming scanline, the other bank serves the previous scanline for non-sequential readout. This ping-pong scheme allows arbitrary horizontal address remapping without requiring a full frame buffer, keeping BRAM usage to just three line-sized memories.

### Animation Oscillators in Video Synthesis

Automatic parameter animation is a staple of analog and digital video synthesizers. Keystone's built-in oscillator generates sine or triangle waves at a rate controlled by the Anim Spd knob. The oscillation is applied as an additive modulation to the base skew or perspective value, scaled by the corresponding depth control. This creates rhythmic geometric motion — the image rocks, breathes, or pulses — without needing an external LFO or control voltage source.


---

## Signal Flow

Y / U / V Channels → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y / U / V Channels ────────────────────────────────────────
│   │
│   ├─ 1. Input Register        (latch incoming pixel + write to line buffer)
│   ├─ 2. Counter Update        (horizontal + vertical pixel counters)
│   ├─ 3. Animation Oscillator  (sine/triangle wave from phase accumulator)
│   ├─ 4. Per-Line Transform    (compute skew offset + perspective scale)
│   ├─ 5. DDA Address Gen       (step accumulator → read address + bounds check)
│   ├─ 6. Line Buffer Read      (2 clk: ping-pong dual-port BRAM)
│   ├─ 7. Border Fill           (black or smeared edge for out-of-bounds)
│   └─ 8. Interpolator Mix      (4 clk: dry/wet crossfade)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline (matched to processing latency)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical computation happens once per scanline, not once per pixel. At each horizontal sync, the per-line process calculates the skew offset and perspective scale factor for the upcoming line based on its vertical position. These two values configure the DDA for the entire line: the skew offset sets the starting position, and the perspective scale sets the step size. The DDA then runs at pixel rate, stepping through source addresses. When the DDA address falls outside the valid range (0 to 1279), the boundary check flags the pixel as out-of-bounds, and the compositor substitutes either black or the last valid edge pixel depending on the Border toggle.

The animation oscillator runs independently, advancing its phase accumulator at each vertical sync. The resulting wave value modulates the skew and perspective parameters additively, scaled by the depth controls. When Animate is set to Manual, the oscillator still runs but its output is not applied — the base pot values alone determine the transform.

---

## Parameter Reference

<img src={keystone_control_panel} alt="Videomancer front panel with Keystone loaded"/>
*Videomancer's front panel with Keystone active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Skew
| Property | Value |
|----------|-------|
| Range | -100% – 100% |
| Default | 0% |
| Suffix | % |

At center position the image is undistorted. Turning clockwise tilts the top of the image to the right and the bottom to the left, creating a right-leaning parallelogram. Turning counter-clockwise reverses the lean. The skew displacement is proportional to vertical distance from the image center, so extreme settings push the top and bottom edges well outside the frame while the center line remains stationary. Internally, sets the base horizontal skew angle.

---

#### Knob 2 — Perspctv
| Property | Value |
|----------|-------|
| Range | -100% – 100% |
| Default | 0% |
| Suffix | % |

At center position there is no foreshortening. Turning clockwise compresses the top of the image and stretches the bottom, creating a trapezoid that narrows toward the top. Counter-clockwise reverses the convergence direction. The vanishing point — where the trapezoid would converge to zero width — is set by the VP Y knob. Internally, sets the base perspective convergence amount.

---

#### Knob 3 — Anim Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

At minimum the oscillator is effectively frozen. As you increase the value, the animation cycles faster — the skew or perspective parameter rocks back and forth at an increasing tempo. The oscillator advances its phase accumulator once per vertical sync, so the animation rate is tied to the frame rate. Maximum speed produces rapid oscillation. Internally, controls the rate of automatic animation oscillation.

---

#### Knob 4 — VP Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Positions the vanishing point along the vertical axis. At 0% the vanishing point sits at the top of the frame; at 100% it sits at the bottom. At 50% it is centered. Lines closer to the vanishing point are compressed more than lines far from it by the perspective transform. Moving the vanishing point while perspective is active shifts the convergence center, dramatically changing the geometric distortion pattern.

---

#### Knob 5 — Skew Dep
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets the modulation depth for skew animation. When Auto Animate is enabled and Anim Mode targets Skew, this control determines how far the skew value swings from its base position. At 0% no modulation is applied regardless of oscillator state. At maximum the skew rocks through its full range. Combined with a slow Anim Spd, this creates a gentle rocking motion; at high speed it produces rapid lateral shearing.

---

#### Knob 6 — Prsp Dep
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets the modulation depth for perspective animation. Works identically to Skew Dep but targets the perspective parameter instead. When both depth controls are high and Auto Animate is enabled, both skew and perspective are modulated simultaneously, producing complex compound geometric motion where the image both tilts and converges rhythmically.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Border** | Black | Smear |
| **8 — AnimMode** | Skew | Persp |
| **9 — Wave** | Sine | Triangle |
| **10 — Animate** | Manual | Auto |
| **11 — Bypass** | Off | On |

The five toggle switches configure the animation system behavior and the border fill mode. Border selects how out-of-frame pixels appear. AnimMode chooses whether the oscillator targets skew or perspective. Wave selects the oscillation waveform shape. Animate enables or disables automatic oscillation. Bypass routes the unprocessed input directly to the output. The animation switches only matter when the corresponding depth control is above zero.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the dry/wet crossfade between the original input and the geometrically transformed output. At 0% the output is entirely dry (original). At 100% the output is entirely wet (transformed). Intermediate values blend the two, which creates a ghostly double-exposure effect where the original and skewed images are overlaid. This is more useful as a transition or compositing tool than as a permanent setting.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Keystone processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from simple skew to animated compound transforms, building familiarity with each control before combining them.

### Exercise 1: Parallelogram Tilt

<BeforeAfterSlider
  sources={[
    { label: "Field", before: keystone_source1_field, after: keystone_ex1_s1 },
    { label: "Car", before: keystone_source2_car, after: keystone_ex1_s2 },
    { label: "Elephant", before: keystone_source3_elephant, after: keystone_ex1_s3 },
    { label: "Pattern", before: keystone_source4_pattern, after: keystone_ex1_s4 },
    { label: "Woman", before: keystone_source5_woman, after: keystone_ex1_s5 },
    { label: "Knit", before: keystone_source6_knit, after: keystone_ex1_s6 },
  ]}
/>
*Parallelogram Tilt — simulated result across source images.*
**Source**: A camera feed aimed at a rectangular subject — bookshelf, window, or grid pattern.

**What You'll Create**: Learn how skew creates horizontal shear and how the border mode affects the result.

1. **Center skew**: Confirm the image is undistorted at center (default).
2. **Right lean**: Turn Skew clockwise to about 75%. The image tilts into a right-leaning parallelogram. Note the black triangular regions at the corners.
3. **Left lean**: Turn Skew counter-clockwise past center to about 25%. The lean reverses.
4. **Smear border**: Toggle Border to Smear. The black triangles are replaced by stretched edge pixels, creating abstract horizontal streaks.
5. **Extreme**: Push Skew to maximum. The parallelogram slant becomes extreme and most of the frame is border fill.

**Key concepts**: Skew is horizontal shear proportional to vertical position, border mode determines treatment of out-of-frame pixels, center value means no distortion

---

### Exercise 2: Vanishing Point Perspective

<BeforeAfterSlider
  sources={[
    { label: "Field", before: keystone_source1_field, after: keystone_ex2_s1 },
    { label: "Car", before: keystone_source2_car, after: keystone_ex2_s2 },
    { label: "Elephant", before: keystone_source3_elephant, after: keystone_ex2_s3 },
    { label: "Pattern", before: keystone_source4_pattern, after: keystone_ex2_s4 },
    { label: "Woman", before: keystone_source5_woman, after: keystone_ex2_s5 },
    { label: "Knit", before: keystone_source6_knit, after: keystone_ex2_s6 },
  ]}
/>
*Vanishing Point Perspective — simulated result across source images.*
**Source**: Footage with strong horizontal lines — architecture, hallways, roads.

**What You'll Create**: Explore perspective convergence and vanishing point positioning.

1. **Reset skew**: Return Skew to center (0%).
2. **Converge top**: Turn Perspctv clockwise to about 70%. The image narrows at the top and widens at the bottom — the floor recedes.
3. **Move VP**: Sweep VP Y from 0% to 100%. Watch the convergence center shift from top to bottom, dramatically altering the geometry.
4. **Center VP**: Set VP Y to 50%. Now perspective compresses lines near the center and stretches lines at both edges symmetrically.
5. **Combine**: Add moderate Skew (~60%) to the perspective. The trapezoid tilts into a non-symmetric quadrilateral.

**Key concepts**: Perspective scales each line's width based on distance from the vanishing point, VP Y positions the convergence center, skew and perspective combine for quadrilateral mapping

---

### Exercise 3: Animated Rocking

<BeforeAfterSlider
  sources={[
    { label: "Field", before: keystone_source1_field, after: keystone_ex3_s1 },
    { label: "Car", before: keystone_source2_car, after: keystone_ex3_s2 },
    { label: "Elephant", before: keystone_source3_elephant, after: keystone_ex3_s3 },
    { label: "Pattern", before: keystone_source4_pattern, after: keystone_ex3_s4 },
    { label: "Woman", before: keystone_source5_woman, after: keystone_ex3_s5 },
    { label: "Knit", before: keystone_source6_knit, after: keystone_ex3_s6 },
  ]}
/>
*Animated Rocking — simulated result across source images.*
**Source**: Any video feed — the animation works with any content.

**What You'll Create**: Configure automatic perspective animation with different wave shapes.

1. **Set perspective**: Perspctv to center (0%), Skew to center (0%).
2. **Enable animation**: Toggle Animate to Auto.
3. **Set depth**: Turn Prsp Dep to about 60%.
4. **Set speed**: Turn Anim Spd to about 30%. The image begins gently rocking — the perspective pulses in and out.
5. **Sine vs Triangle**: Toggle Wave between Sine and Triangle. Sine produces smooth organic motion; Triangle produces linear mechanical rocking with sharp reversals.
6. **Add skew animation**: Set Skew Dep to about 40%. Now both skew and perspective animate simultaneously, creating compound geometric motion.
7. **Speed up**: Increase Anim Spd to high values. The animation becomes rapid and stroboscopic.

**Key concepts**: Animation oscillator cycles at frame rate, depth controls scale the oscillation amplitude for each parameter, sine and triangle produce different motion characters

---


## Tips

- **Animate one at a time**: When learning, set only one depth control above zero to isolate skew animation from perspective animation before combining them.
- **Mix for compositing**: Setting Mix to about 50% creates double-exposure overlays of the distorted and undistorted images, useful for disorientation or dream-sequence effects.
- **Feedback loops**: Routing the output back to the input creates recursive geometric distortion — the parallelogram or trapezoid is applied to itself each frame, producing increasingly extreme warping.
- **Slow sine for organic motion**: A slow sine-wave animation on perspective with moderate depth creates a gentle breathing or pulsing effect that feels organic and alive.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDA** | Digital Differential Analyzer; an incremental algorithm for stepping through coordinates at a variable sampling rate. |
| **Foreshortening** | The apparent compression of an object's dimension when viewed at an angle; perspective convergence. |
| **Line Buffer** | A single-scanline memory that stores one row of pixel data for non-sequential readout. |
| **LUT** | Look-Up Table; a pre-computed array of values indexed by an input to avoid runtime calculation (used here for sine wave). |
| **Parallelogram** | A quadrilateral with two pairs of parallel sides; the result of a purely-shear (skew) transform applied to a rectangle. |
| **Ping-Pong** | A dual-buffer scheme where one buffer is written while the other is read, alternating each scanline. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **Shear** | A geometric transformation that displaces each point by an amount proportional to its distance from a reference axis. |
| **Trapezoid** | A quadrilateral with one pair of parallel sides; the result of a perspective distortion applied to a rectangle. |
| **Vanishing Point** | The point in a perspective projection where parallel lines appear to converge; configured by the VP Y control. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
