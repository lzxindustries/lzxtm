---
draft: true
sidebar_position: 114
slug: /instruments/videomancer/fisheye
title: "Fisheye"
image: /img/instruments/videomancer/fisheye/fisheye_hero_s1.png
description: "Every lens bends light."
---

![Fisheye hero image](/img/instruments/videomancer/fisheye/fisheye_hero_s1.png)
*Fisheye applying radial brightness falloff and chromatic color fringing to create lens-distortion vignettes from a live video source.*

---

## Overview

**Fisheye** is a radial vignette and chromatic aberration program that simulates the look of curved optical elements. Rather than remapping pixels spatially: which would demand a full frame buffer: Fisheye achieves its effect by modulating brightness as a function of radial distance from a movable center point. The result is a convincing impression of barrel or pincushion lens distortion, complete with adjustable color fringing and hard-edged border masking.

At moderate settings, Fisheye adds a gentle spotlight-like falloff that draws the eye toward the center of the frame. At extreme settings, the image collapses into a tight bright disc surrounded by darkness or: in convex mode: a glowing halo that gets brighter toward the edges. Enabling chromatic aberration separates the color channels along the radial axis, producing rainbow-edged fringing that intensifies with distance from center.

:::note
Fisheye simulates lens distortion through brightness modulation rather than true spatial warping. The geometry of the image remains unchanged: what changes is how bright or dark each pixel becomes based on its distance from the center point.
:::

### What's In a Name?

A ***fisheye lens*** is an ultra-wide-angle lens that produces strong visual distortion intended to create a wide panoramic or hemispherical image. The distinctive barrel distortion of a fisheye lens causes straight lines to curve outward from the center, and objects at the periphery appear stretched and dimmed. Fisheye captures the spirit of that optical artifact: not by bending geometry, but by sculpting light and color radially, the way a real curved glass element redistributes intensity across the image plane.

---

## Quick Start

1. Turn **Distortion** (Knob 1) counter-clockwise to shrink the bright central region. A dark vignette appears around the edges of the image, like looking through a tunnel.
2. Adjust **Center X** (Knob 2) and **Center Y** (Knob 3) to relocate the bright center. The spotlight follows your adjustments.
3. Toggle **Convex** (Switch 7) to On. The effect reverses: the edges brighten while the center dims, as if light is wrapping around a convex surface.

---

## Parameters

![Videomancer front panel with Fisheye loaded](/img/instruments/videomancer/fisheye/fisheye_control_panel.png)
*Videomancer's front panel with Fisheye active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Distortion

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Distortion** controls the radius of the bright zone. It sets the threshold distance from center beyond which brightness drops sharply. At 0%, the vignette is at its most aggressive: only pixels very close to the center retain full brightness. As you increase Distortion, the bright zone expands outward, letting more of the image through at full intensity. At 100%, nearly the entire image falls within the bright zone and the vignette effect becomes subtle.

:::tip
Think of Distortion as setting the size of a spotlight. Low values create a tight beam; high values flood the frame with light.
:::

---

### Knob 2 — Center X

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Center X** shifts the horizontal position of the effect's focal point. At 50%, the center sits roughly in the middle of the frame. Turning the knob counter-clockwise moves the center leftward; clockwise moves it rightward. The radial falloff, chromatic fringing, and border mask all follow this center point.

---

### Knob 3 — Center Y

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Center Y** shifts the vertical position of the effect's focal point. At 50%, the center sits roughly in the middle of the frame vertically. Counter-clockwise moves the center upward; clockwise moves it downward. Combined with Center X, you can place the focal point anywhere in the frame.

---

### Knob 4 — Zoom

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Zoom** is reserved for a future update and does not currently affect the output. The knob is present on the panel and reads out a value, but turning it produces no visible change.

---

### Knob 5 — Chromatic

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Chromatic** (intensity knob) is reserved for a future update. The chromatic aberration effect is currently controlled solely by the **Chromatic** toggle (Switch 9), which enables or disables the effect at full strength. This knob is intended to control the intensity of the color fringing in a future revision.

---

### Knob 6 — Curvature

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Curvature** is reserved for a future update and does not currently affect the output. It is intended to shape the radial falloff curve in a future revision.

---

### Switch 7 — Convex

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Convex** reverses the direction of the radial brightness modulation. With the switch Off (concave mode), pixels near the center are bright and pixels at the edges are dim: the classic barrel-distortion vignette. With the switch On (convex mode), the relationship inverts: the center dims and the edges brighten, simulating the look of light bending around a convex surface. In concave mode, pixels beyond the Distortion radius drop to about 25% brightness. In convex mode, pixels beyond the radius jump to full brightness.

---

### Switch 8 — Circular

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Circular** is reserved for a future update and does not currently affect the output. It is intended to select between circular and elliptical distortion shapes.

---

### Switch 9 — Chromatic

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Chromatic** (toggle) enables chromatic aberration. When On, the U and V color channels are offset in opposite directions based on radial distance from center. U shifts positively and V shifts negatively as distance increases, producing complementary color fringing: warm tones on one side, cool tones on the other: that intensifies toward the edges and converges to neutral at the center point.

:::tip
Chromatic aberration mimics the ***lateral chromatic dispersion*** of real lenses, where different wavelengths of light refract at slightly different angles through curved glass, producing colored halos.
:::

---

### Switch 10 — Border

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Border** replaces all pixels beyond the Distortion radius with solid black (Y = 0, neutral chroma). Instead of a gradual falloff, the image is hard-clipped to a disc shape. This creates a clean circular mask around the focal point. The size of the disc is controlled by the **Distortion** knob, and its position by **Center X** and **Center Y**.

:::note
When Border is On, the brightness modulation inside the disc still applies. The border only affects pixels that fall beyond the Distortion threshold (everything inside is processed normally.)
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Fisheye processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** blends between the dry (unprocessed) and wet (processed) signals using a crossfade. At 0%, the output is entirely dry: the input passes through unchanged. At 100%, the output is entirely the processed Fisheye effect. Intermediate positions create a transparent overlay where the vignette is subtly layered over the original image.

---

## Background

### Lens distortion in optics

Real camera lenses are not perfect. Every lens introduces some amount of ***geometric distortion***: a warping of straight lines caused by the curvature of the glass elements. ***Barrel distortion*** causes straight lines to bow outward from the center, making the image look like it's been inflated. ***Pincushion distortion*** does the opposite, pulling lines inward as if the image were being stretched at the corners. These terms come from the shapes they produce: a barrel bulges outward; a pincushion pinches inward.

Fisheye lenses take barrel distortion to the extreme, cramming an ultra-wide field of view: sometimes exceeding 180 degrees: into a flat image. The result is a globe-like projection where the center of the frame appears normal but the periphery is dramatically stretched and curved.

### Radial brightness falloff

In photography, ***vignetting*** is a reduction of brightness at the edges of an image compared to the center. It occurs naturally in most lenses because the aperture blocks some peripheral light rays, and because light striking the sensor at steep angles covers more area. Fisheye exploits this principle as a creative tool, using distance from a movable center point to modulate pixel brightness. The squared distance calculation means the falloff accelerates: close to the center, brightness changes slowly; farther out, it drops (or rises) rapidly.

### Chromatic aberration

When white light passes through a curved glass element, different wavelengths refract at slightly different angles. Blue light bends more than red, green falls in between. This separation creates colored fringes at high-contrast edges: a phenomenon called ***chromatic aberration***. In Fisheye, the effect is simulated by offsetting the U and V color channels in opposite directions based on radial distance. Near the center the offset is negligible, but toward the edges the color channels spread apart, producing the characteristic rainbow halos of an imperfect lens.


---

## Signal Flow

### Signal Flow Notes

The processing pipeline computes a ***squared radial distance*** from each pixel's position to the adjustable center point. This distance value drives three independent effects: brightness modulation on the Y channel, chromatic offset on the U/V channels, and the border fill mask. All three share the same distance calculation, so they always align spatially.

The brightness modulation multiplies each Y sample by a scaling factor derived from the distance. In concave mode, this factor decreases with distance (darkening the edges); in convex mode, it increases (brightening the edges). The multiplication is a full 10 × 10 → 20-bit product, with the upper 10 bits taken as the output.

:::tip
Because the distance is ***squared***, the falloff is nonlinear: brightness drops slowly near the center and accelerates toward the edges. This matches the natural behavior of real optical vignetting.
:::


---

## Exercises

These exercises progress from basic vignetting to creative compositing techniques. Each one builds on the previous, introducing additional controls.
### Exercise 1: Classic Vignette

![Classic Vignette result](/img/instruments/videomancer/fisheye/fisheye_ex1_s1.png)
*Classic Vignette — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A cinematic vignette that draws the eye toward a subject in the frame.

#### Key Concepts

- Radial brightness falloff simulates optical vignetting
- The Distortion knob sets the radius of the bright zone
- Center X and Center Y position the focal point

#### Video Source

A live camera feed or recorded footage with a recognizable subject positioned near the center of the frame.

#### Steps

1. **Set center**: Position **Center X** (Knob 2) and **Center Y** (Knob 3) at 50% to place the focal point in the middle.
2. **Open the vignette**: Set **Distortion** (Knob 1) to about 60%. The edges darken gently while the center stays bright.
3. **Tighten the spotlight**: Reduce Distortion toward 30%. The dark ring closes in, creating a more dramatic tunnel effect.
4. **Reposition**: Shift Center X and Center Y to track your subject. The vignette follows.
5. **Compare**: Toggle **Bypass** (Switch 11) to see the raw input alongside the vignetted result.

#### Settings

| Control | Value |
|---------|-------|
| Distortion | ~60% |
| Center X | 50% |
| Center Y | 50% |
| Zoom | 50% |
| Chromatic | 0% |
| Curvature | 50% |
| Convex | Off |
| Circular | On |
| Chromatic | Off |
| Border | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Chromatic Iris

![Chromatic Iris result](/img/instruments/videomancer/fisheye/fisheye_ex2_s1.png)
*Chromatic Iris — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A bordered disc with rainbow color fringing at the edges (like looking through a glass marble.)

#### Key Concepts

- Chromatic aberration separates U and V channels radially
- The Border switch creates a hard circular mask
- Convex mode reverses the brightness direction

#### Video Source

High-contrast footage with strong edges: text, geometric patterns, or high-contrast portraits work well.

#### Steps

1. **Enable border**: Turn on **Border** (Switch 10). Pixels beyond the Distortion radius turn black, framing the image in a clean disc.
2. **Shrink the disc**: Lower **Distortion** (Knob 1) to about 40%. The circular window tightens.
3. **Add fringing**: Enable **Chromatic** (Switch 9). Color fringing appears at the edges of the disc, with warm and cool halos on opposite sides.
4. **Flip the brightness**: Toggle **Convex** (Switch 7) to On. The center dims while the ring near the border brightens (the disc becomes a glowing ring.)
5. **Blend**: Pull **Mix** (Fader 12) to about 60% to layer the effect transparently over the original image.

#### Settings

| Control | Value |
|---------|-------|
| Distortion | ~40% |
| Center X | 50% |
| Center Y | 50% |
| Zoom | 50% |
| Chromatic | 0% |
| Curvature | 50% |
| Convex | On |
| Circular | On |
| Chromatic | On |
| Border | On |
| Bypass | Off |
| Mix | ~60% |

---

### Exercise 3: Roaming Spotlight

![Roaming Spotlight result](/img/instruments/videomancer/fisheye/fisheye_ex3_s1.png)
*Roaming Spotlight — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A moving spotlight effect that scans across the image, revealing areas as it passes.

#### Key Concepts

- The center point can be animated by sweeping knobs in real time
- Concave mode creates a traveling spotlight
- Low Distortion values create tight, dramatic beams

#### Video Source

A busy scene: crowd footage, abstract patterns, or a complex still image with detail across the entire frame.

#### Steps

1. **Tight beam**: Set **Distortion** (Knob 1) to about 20%. Only a small circle of the image is visible.
2. **Enable border**: Turn on **Border** (Switch 10) for a clean edge.
3. **Enable chromatic**: Turn on **Chromatic** (Switch 9) for colored fringing at the disc edge.
4. **Scan horizontally**: Slowly sweep **Center X** (Knob 2) from left to right. The spotlight travels across the frame, revealing and concealing the image.
5. **Scan vertically**: Now sweep **Center Y** (Knob 3) while Center X remains in the middle. The beam moves up and down.
6. **Combine**: Sweep both Center X and Center Y simultaneously to trace irregular paths across the image. Enable **Convex** (Switch 7) briefly to invert the spotlight into a shadow that roams in the opposite brightness direction.

#### Settings

| Control | Value |
|---------|-------|
| Distortion | ~20% |
| Center X | (swept) |
| Center Y | (swept) |
| Zoom | 50% |
| Chromatic | 0% |
| Curvature | 50% |
| Convex | Off |
| Circular | On |
| Chromatic | On |
| Border | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Barrel Distortion**: A type of optical aberration where straight lines bow outward from the center of the image, as if inflated.

- **Chromatic Aberration**: Color fringing caused by different wavelengths of light refracting at different angles through a lens element.

- **Concave**: Curving inward, like the inside of a bowl; in Fisheye, the mode where the center is bright and edges are dark.

- **Convex**: Curving outward, like the surface of a ball; in Fisheye, the mode where the center is dark and edges are bright.

- **Interpolator**: A hardware block that blends between two values using a fractional mix amount; used for wet/dry crossfading.

- **Pincushion Distortion**: The opposite of barrel distortion (straight lines bow inward toward the center.)

- **Radial Distance**: The straight-line distance from a given pixel to the center point, measured along the radius of an imaginary circle.

- **Vignette**: A gradual darkening of the image toward its edges, originally an optical artifact, now widely used as a creative effect.

---
