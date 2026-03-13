---
draft: true
sidebar_position: 114
slug: /instruments/videomancer/fisheye
title: "Fisheye"
image: /img/instruments/videomancer/fisheye/fisheye_hero_s1.png
description: "Every lens bends light."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import fisheye_control_panel from '/img/instruments/videomancer/fisheye/fisheye_control_panel.png';
import fisheye_source1_fruit from '/img/instruments/videomancer/fisheye/fisheye_source1_fruit.png';
import fisheye_source2_parrot from '/img/instruments/videomancer/fisheye/fisheye_source2_parrot.png';
import fisheye_source3_elephant from '/img/instruments/videomancer/fisheye/fisheye_source3_elephant.png';
import fisheye_source4_pattern from '/img/instruments/videomancer/fisheye/fisheye_source4_pattern.png';
import fisheye_source5_man from '/img/instruments/videomancer/fisheye/fisheye_source5_man.png';
import fisheye_source6_knit from '/img/instruments/videomancer/fisheye/fisheye_source6_knit.png';
import fisheye_hero_s1 from '/img/instruments/videomancer/fisheye/fisheye_hero_s1.png';
import fisheye_hero_s2 from '/img/instruments/videomancer/fisheye/fisheye_hero_s2.png';
import fisheye_hero_s3 from '/img/instruments/videomancer/fisheye/fisheye_hero_s3.png';
import fisheye_hero_s4 from '/img/instruments/videomancer/fisheye/fisheye_hero_s4.png';
import fisheye_hero_s5 from '/img/instruments/videomancer/fisheye/fisheye_hero_s5.png';
import fisheye_hero_s6 from '/img/instruments/videomancer/fisheye/fisheye_hero_s6.png';
import fisheye_ex1_s1 from '/img/instruments/videomancer/fisheye/fisheye_ex1_s1.png';
import fisheye_ex1_s2 from '/img/instruments/videomancer/fisheye/fisheye_ex1_s2.png';
import fisheye_ex1_s3 from '/img/instruments/videomancer/fisheye/fisheye_ex1_s3.png';
import fisheye_ex1_s4 from '/img/instruments/videomancer/fisheye/fisheye_ex1_s4.png';
import fisheye_ex1_s5 from '/img/instruments/videomancer/fisheye/fisheye_ex1_s5.png';
import fisheye_ex1_s6 from '/img/instruments/videomancer/fisheye/fisheye_ex1_s6.png';
import fisheye_ex2_s1 from '/img/instruments/videomancer/fisheye/fisheye_ex2_s1.png';
import fisheye_ex2_s2 from '/img/instruments/videomancer/fisheye/fisheye_ex2_s2.png';
import fisheye_ex2_s3 from '/img/instruments/videomancer/fisheye/fisheye_ex2_s3.png';
import fisheye_ex2_s4 from '/img/instruments/videomancer/fisheye/fisheye_ex2_s4.png';
import fisheye_ex2_s5 from '/img/instruments/videomancer/fisheye/fisheye_ex2_s5.png';
import fisheye_ex2_s6 from '/img/instruments/videomancer/fisheye/fisheye_ex2_s6.png';
import fisheye_ex3_s1 from '/img/instruments/videomancer/fisheye/fisheye_ex3_s1.png';
import fisheye_ex3_s2 from '/img/instruments/videomancer/fisheye/fisheye_ex3_s2.png';
import fisheye_ex3_s3 from '/img/instruments/videomancer/fisheye/fisheye_ex3_s3.png';
import fisheye_ex3_s4 from '/img/instruments/videomancer/fisheye/fisheye_ex3_s4.png';
import fisheye_ex3_s5 from '/img/instruments/videomancer/fisheye/fisheye_ex3_s5.png';
import fisheye_ex3_s6 from '/img/instruments/videomancer/fisheye/fisheye_ex3_s6.png';

# Fisheye

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: fisheye_source1_fruit, after: fisheye_hero_s1 },
    { label: "Parrot", before: fisheye_source2_parrot, after: fisheye_hero_s2 },
    { label: "Elephant", before: fisheye_source3_elephant, after: fisheye_hero_s3 },
    { label: "Pattern", before: fisheye_source4_pattern, after: fisheye_hero_s4 },
    { label: "Man", before: fisheye_source5_man, after: fisheye_hero_s5 },
    { label: "Knit", before: fisheye_source6_knit, after: fisheye_hero_s6 },
  ]}
/>
*Fisheye applying radial brightness falloff and chromatic aberration to simulate barrel lens distortion across a multi-source video composite.*

---

## Overview

Every lens bends light. Wide-angle lenses bend it a lot — straight lines bow outward from the center of the frame, corners stretch, and the image takes on the swollen, curved geometry that photographers call barrel distortion. Fisheye takes its name from the ultra-wide lenses that push this distortion to its extreme, compressing an entire hemisphere of the visual field into a single circular image.

True spatial lens distortion requires a frame buffer to remap pixel coordinates — reading from one location and writing to another. The iCE40 FPGA has no memory budget for that. Instead, Fisheye simulates the *appearance* of barrel distortion through a radial brightness falloff: pixels farther from the center of the frame are darkened proportionally to the square of their distance. The result is a vignetting effect that mimics the way wide-angle lenses attenuate light at the edges, combined with optional chromatic aberration that shifts color channels outward from center — reproducing the prismatic fringing that cheap or extreme lenses produce.

At moderate settings, Fisheye adds a subtle focus-pulling vignette that draws the eye to the center of the frame. At extreme settings, it produces dramatic tunnel-vision effects, hard-edged circular borders, and rainbow chromatic halos. The Convex toggle inverts the falloff direction, brightening the periphery instead of darkening it — a pincushion-like counterpart to the default barrel mode.

---

## Quick Start

1. **Start with the vignette**: Set Distortion to ~50% with all toggles off and Mix at 100%. This gives a clean radial darkening baseline before adding complexity.
2. **Border creates compositing mattes**: With Border on, Fisheye becomes a circular key generator. Route the output to a downstream mixer's key input for shaped compositing.
3. **Chromatic aberration is subtle at center**: Because the offset is distance-based, the center always stays clean. Move Center X/Y off-frame to push strong chromatic fringing across the entire visible area.

---

## Background

### Barrel and Pincushion Distortion

Optical lens distortion comes in two primary forms. **Barrel distortion** causes straight lines to bow outward from the center — the image appears to bulge, as though painted on the surface of a sphere. **Pincushion distortion** does the opposite: lines curve inward, and the image appears to pinch toward the center. Both are radial distortions — the displacement increases with distance from the optical axis. Every real lens exhibits some combination of both, and correcting for it is one of the fundamental tasks of optical engineering. Fisheye's Convex toggle switches between simulating the darkening pattern associated with barrel distortion (edges darker) and pincushion distortion (center darker).

### Radial Vignetting in Optics

Vignetting is the gradual darkening of an image toward its edges and corners. In physical optics, it occurs because light rays entering the lens at steep angles are partially blocked by the lens barrel, aperture blades, or front filter rings. The falloff follows a $\cos^4\theta$ law for ideal thin lenses, where $\theta$ is the angle from the optical axis. Fisheye approximates this with a distance-squared falloff — computationally simpler but visually similar. The result is the characteristic bright-center, dark-edges look that photographers sometimes add deliberately for mood or to draw the viewer's attention inward.

### Chromatic Aberration in Lens Systems

When white light passes through a lens, different wavelengths refract at slightly different angles. Blue light bends more than red, causing color channels to separate at the edges of the frame. This effect — called **lateral chromatic aberration** — produces colored fringes along high-contrast edges, especially near the corners of the image. In Fisheye, the chromatic aberration stage offsets the U and V chroma channels in opposite directions based on the radial distance from center, creating a similar prismatic color separation. The effect is most visible on high-contrast edges far from the center point.

### Lens Correction in Photography

Modern digital cameras and post-processing software routinely apply automatic lens correction profiles that undo barrel distortion, vignetting, and chromatic aberration. Fisheye takes the opposite approach — it *adds* these optical artifacts to a clean digital signal. This reversal is useful in video synthesis because optical imperfections are part of the visual vocabulary of analog media. Adding controlled vignetting and chromatic fringing to a synthetic signal makes it feel more organic and less computer-generated.

### Distance-Based Falloff Functions

The core computation in Fisheye is the squared Euclidean distance from each pixel to an adjustable center point: $d^2 = (x - c_x)^2 + (y - c_y)^2$. This distance-squared value drives both the darkening factor and the chromatic offset. Squaring the distance rather than using linear distance produces a steeper, more natural-looking falloff curve — brightness drops slowly near center and rapidly near the edges. The distortion control sets a threshold on $d^2$ beyond which pixels receive a fixed attenuation, creating a visible boundary between the treated and untreated zones.


---

## Signal Flow

Timing Detection → Distance Computation → Y Channel → ... → Sync Delay Pipeline → Output / Bypass

```
Input Video (YUV 4:4:4)
│
├── Timing Detection ──────────────────────────────────────────
│   ├─ hsync/vsync edge detect → x_counter, y_counter
│   └─ Pixel position tracking (12-bit counters)
│
├── Distance Computation ──────────────────────────────────────
│   ├─ v_cx = x_counter − (center_x + 128)
│   ├─ v_cy = y_counter − center_y
│   └─ v_dist_sq = v_cx² + v_cy²
│
├── Y Channel ─────────────────────────────────────────────────
│   ├─ 1. Darken factor from dist_sq vs distortion threshold
│   │     ├─ Convex Off: 1023 − dist_sq  (edges darken)
│   │     └─ Convex On:  512 + dist_sq/2 (edges brighten)
│   ├─ 2. Outside threshold:
│   │     ├─ Convex Off: darken = 256  (dim)
│   │     └─ Convex On:  darken = 1023 (full)
│   └─ 3. Y_out = (Y_in × darken) >> 10
│
├── U/V Channels ──────────────────────────────────────────────
│   ├─ Chromatic Off: pass through
│   └─ Chromatic On:  U += dist_sq[19:10], V −= dist_sq[19:10]
│
├── Border Fill ───────────────────────────────────────────────
│   └─ If Border On AND dist_sq > distortion:
│         Y = 0, U = 512, V = 512  (black)
│
├── Mix Stage (3× interpolator_u, 4 clocks each) ─────────────
│   └─ lerp(dry, wet, mix_amount) per Y, U, V
│
├── Sync Delay Pipeline (8 clocks) ────────────────────────────
│   └─ Shift registers for hsync_n, vsync_n, field_n, Y, U, V
│
└── Output / Bypass ───────────────────────────────────────────
    └─ Bypass Off → mixed result; Bypass On → delayed dry signal
```

The critical path is the distance-squared computation: each pixel's horizontal and vertical offsets from the adjustable center are squared and summed in a single clock cycle. The upper bits of this 24-bit distance value drive two independent effects — Y-channel darkening and UV chromatic offset — using different bit slices. The darken factor multiplies the input Y value in 20-bit arithmetic (10×10), and the result is truncated back to 10 bits. Because the distance computation uses 12-bit pixel counters, the center position controls have reasonable range across HD video frames when the 10-bit register value is extended with padding.

The border fill stage overwrites the darkening result when active, replacing outside-threshold pixels with pure black (Y=0, U=V=512). This creates a hard circular mask whose radius is controlled by the Distortion knob — effectively a distance-keyed matte generator.

---

## Parameter Reference

<img src={fisheye_control_panel} alt="Videomancer front panel with Fisheye loaded"/>
*Videomancer's front panel with Fisheye active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Distortion
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At low values, only a small region near the center receives gradual falloff — most of the frame hits the floor. At high values, the gradual zone extends nearly to the edges. This control defines the effective "lens radius" of the simulated distortion. Combined with Border, it sets the edge of a circular mask. Internally, sets the distance-squared threshold that defines the boundary between the smoothly attenuated center zone and the hard-limited outer zone.

---

#### Knob 2 — Center X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the center of the radial falloff pattern horizontally. At midpoint, the center aligns with the middle of the active video area. Sweeping left or right moves the bright spot, causing asymmetric darkening. The VHDL adds a 128-pixel offset to the raw register value to better center the effect within the typical active line width of an HD video signal.

---

#### Knob 3 — Center Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the center of the radial falloff pattern vertically. At midpoint, the center aligns roughly with the middle scan line. Moving the center off-axis creates dramatic directional vignetting — useful for simulating off-center lens effects or directing the viewer's gaze to a specific region of the frame.

---

#### Knob 4 — Zoom
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for a zoom or field-of-view adjustment, but not connected in the current VHDL implementation. The register is read but the value is not used in any computation. Adjusting this control has no visible effect on the output.

---

#### Knob 5 — Chromatic
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the intensity of the chromatic aberration effect when the Chromatic toggle is enabled. Higher values increase the distance-dependent offset applied to the U and V channels, spreading the color fringing further from center. At zero, no chromatic offset is applied even when the toggle is on. The offset is derived from a different bit slice of the distance-squared value than the darkening factor, so the two effects have different spatial profiles.

---

#### Knob 6 — Curvature
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for a curvature adjustment, but not connected in the current VHDL implementation. The register is read but the value is not used. Adjusting this control has no visible effect on the output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Convex** | Off | On |
| **8 — Circular** | Off | On |
| **9 — Chromatic** | Off | On |
| **10 — Border** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent binary processing options. Convex reverses the direction of the radial falloff. Circular is reserved but unused. Chromatic enables the UV color-fringing stage. Border enables the hard circular mask fill. Bypass routes the delayed dry signal directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry mix between the processed and original signal. At maximum (100%), the output is fully processed. At minimum (0%), the output is the original delayed signal. Intermediate values blend linearly between the two via three parallel interpolator instances (one each for Y, U, and V). This allows subtle vignetting to be dialed in without committing to the full effect intensity.





---

## Guided Exercises

These exercises progress from simple vignetting to complex chromatic effects. Each builds on the previous, demonstrating how center position, falloff threshold, and chromatic aberration interact.

### Exercise 1: Classic Vignette

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: fisheye_source1_fruit, after: fisheye_ex1_s1 },
    { label: "Parrot", before: fisheye_source2_parrot, after: fisheye_ex1_s2 },
    { label: "Elephant", before: fisheye_source3_elephant, after: fisheye_ex1_s3 },
    { label: "Pattern", before: fisheye_source4_pattern, after: fisheye_ex1_s4 },
    { label: "Man", before: fisheye_source5_man, after: fisheye_ex1_s5 },
    { label: "Knit", before: fisheye_source6_knit, after: fisheye_ex1_s6 },
  ]}
/>
*Classic Vignette — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a centered subject and visible detail in the corners.

**What You'll Create**: Learn how the Distortion threshold and center position controls create a traditional photographic vignette.

1. **Default vignette**: With Distortion at midpoint, observe the radial darkening from center to edges.
2. **Tighten the circle**: Reduce Distortion. Watch the bright center zone shrink and the edges darken further.
3. **Open it up**: Increase Distortion toward maximum. The darkening becomes very subtle — nearly the full frame is in the bright zone.
4. **Move the center**: Sweep Center X left and right. The bright spot follows. Then sweep Center Y up and down. The vignette tracks the center point.
5. **Off-center drama**: Set Center X and Center Y to create an off-center spotlight effect.

**Key concepts**: Distance-squared falloff creates a natural vignette, the Distortion threshold sets the effective lens radius, center position controls shift the focal point

---

### Exercise 2: Barrel vs. Pincushion

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: fisheye_source1_fruit, after: fisheye_ex2_s1 },
    { label: "Parrot", before: fisheye_source2_parrot, after: fisheye_ex2_s2 },
    { label: "Elephant", before: fisheye_source3_elephant, after: fisheye_ex2_s3 },
    { label: "Pattern", before: fisheye_source4_pattern, after: fisheye_ex2_s4 },
    { label: "Man", before: fisheye_source5_man, after: fisheye_ex2_s5 },
    { label: "Knit", before: fisheye_source6_knit, after: fisheye_ex2_s6 },
  ]}
/>
*Barrel vs. Pincushion — simulated result across source images.*
**Source**: Footage with visible detail across the full frame — a wide shot or geometric test pattern.

**What You'll Create**: Compare the barrel (concave) and pincushion (convex) falloff modes and explore the border fill function.

1. **Barrel mode**: With Convex off, set Distortion to ~40%. Observe the dark edges and bright center.
2. **Pincushion mode**: Enable Convex (Toggle 7). The brightness distribution inverts — edges brighten, center dims.
3. **Toggle back and forth**: Flip Convex repeatedly to see the two modes as complementary transformations.
4. **Enable border**: Turn on Border (Toggle 10). Outside the Distortion threshold, pixels snap to black — a hard circular mask.
5. **Resize the mask**: Sweep Distortion with Border on. The circular window grows and shrinks.
6. **Off-center mask**: Shift Center X and Center Y while Border is on to create a moving circular spotlight.

**Key concepts**: Convex inverts the radial brightness curve, border fill creates a hard circular matte, the distortion threshold controls both vignette softness and mask radius

---

### Exercise 3: Chromatic Fringing

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: fisheye_source1_fruit, after: fisheye_ex3_s1 },
    { label: "Parrot", before: fisheye_source2_parrot, after: fisheye_ex3_s2 },
    { label: "Elephant", before: fisheye_source3_elephant, after: fisheye_ex3_s3 },
    { label: "Pattern", before: fisheye_source4_pattern, after: fisheye_ex3_s4 },
    { label: "Man", before: fisheye_source5_man, after: fisheye_ex3_s5 },
    { label: "Knit", before: fisheye_source6_knit, after: fisheye_ex3_s6 },
  ]}
/>
*Chromatic Fringing — simulated result across source images.*
**Source**: High-contrast footage — sharp edges, bright highlights against dark backgrounds.

**What You'll Create**: Explore chromatic aberration and its interaction with vignetting and border fill.

1. **Enable chromatic**: Turn on Chromatic toggle (Toggle 9).
2. **Increase intensity**: Slowly raise the Chromatic knob (Pot 5) from 0%. Watch color fringes appear at the edges of the frame.
3. **Center vs. edge**: Note that the center of the frame remains clean — chromatic offset is proportional to distance from center.
4. **Move the center**: Shift Center X/Y off-center. The clean zone moves with the center point — fringes realign around the new center.
5. **Add border**: Enable Border. The chromatic fringes are visible inside the circular window, and outside pixels are pure black.
6. **Convex + chromatic**: Toggle Convex on. The brightness inverts but chromatic fringing remains distance-based — the color halos still intensify toward the edges.
7. **Mix for subtlety**: Use the Mix fader to blend 30–50% of the chromatic effect with the dry signal for a subtle lens imperfection look.

**Key concepts**: Chromatic aberration offsets U and V in opposite directions based on distance, the effect radiates from the adjustable center point, mixing allows subtle integration of chromatic fringing

---


## Tips

- **Convex for spotlight effects**: Pincushion mode (Convex on) brightens the edges — useful for creating an inverted spotlight or halo effect when combined with border fill.
- **Unused controls are future-ready**: Zoom, Curvature, and Circular are reserved for potential spatial remapping if a future hardware revision adds frame buffer memory.
- **Mix for film-quality vignetting**: Real camera vignettes are subtle — 20–40% mix with a wide Distortion setting produces a filmic edge darkening that integrates naturally with live footage.
- **Feedback loops amplify the falloff**: Routing the output back to the input through an external mixer creates recursive darkening — the vignette compounds on each pass, producing dramatic tunnel effects.
- **Pair with color programs**: Fisheye's vignetting and chromatic fringing complement color-processing programs like Duotone or Chrome — apply Fisheye downstream for a convincing analog lens look.

---

## Glossary

| Term | Definition |
|------|------------|
| **Barrel Distortion** | A lens aberration where straight lines bow outward from the center, giving the image a convex, bulging appearance. |
| **Chromatic Aberration** | Colored fringing caused by a lens focusing different wavelengths at slightly different points, most visible at image edges. |
| **Distance-Squared** | The sum of squared horizontal and vertical offsets from a reference point; used as a computationally efficient proxy for radial distance. |
| **Pincushion Distortion** | A lens aberration where straight lines bow inward toward the center, giving the image a concave, pinched appearance. |
| **Radial Falloff** | A brightness attenuation that increases with distance from a central point, simulating optical vignetting. |
| **Vignetting** | The gradual darkening of an image toward its edges and corners, caused by optical or mechanical properties of a lens system. |

---
