---
draft: true
sidebar_position: 44
slug: /instruments/videomancer/chatoyant
title: "Chatoyant"
image: /img/instruments/videomancer/chatoyant/chatoyant_hero_s1.png
description: "Certain gemstones — tiger's eye, chrysoberyl, moonstone — contain parallel fibrous inclusions that act as a natural diffraction grating."
---

![Chatoyant hero image](/img/instruments/videomancer/chatoyant/chatoyant_hero_s1.png)
*Chatoyant casting luminance-reactive specular streaks across the frame, simulating the shimmering band of light seen in cat's-eye gemstones.*

---

## Overview

Chatoyant recreates the optical phenomenon of ***chatoyancy***: the narrow, bright band of reflected light that glides across the surface of certain fibrous gemstones. Feed it a video signal, and Chatoyant draws a directional streak of light across the frame. Where the streak intersects bright areas of the source, it produces a specular highlight: a concentrated brightening that follows the contours of the image content. Dark areas resist the streak, receiving little or no boost. The result is an effect that looks, and behaves, like the reflective band on a polished tiger's eye cabochon.

The streak's direction, width, position, and intensity are all independently controllable. A combined mode selector lets you lock the streak to horizontal, vertical, or diagonal orientations, or leave it free to follow a custom angle. An optional color tint shifts the highlight toward warm amber-gold or cool blue-white, adding chromatic dimension to the specular band. A mirrored double-streak mode creates a symmetrical pair, and an animation mode sweeps the streak continuously across the frame.

:::tip
The key to Chatoyant is the interaction between the streak and the source brightness. The highlight responds to image content: brighter pixels receive a stronger boost. This makes the effect ***reactive*** rather than a simple overlay.
:::

### What's In a Name?

The word ***chatoyant*** comes from the French *chatoyer*, meaning "to shimmer like a cat's eye." In gemology, chatoyancy describes the optical phenomenon where a single bright band of light appears to glide across the surface of a polished stone as it rotates. The effect is caused by parallel fibrous inclusions reflecting light along a single axis, and it gives gems like ***tiger's eye***, ***chrysoberyl cat's eye***, and ***moonstone*** their distinctive silky luster. Chatoyant names this program after the shimmer itself.

---

## Quick Start

1. Set **Streak L** (Knob 5) to about 50%. A horizontal highlight band should appear partway down the frame. You may need to increase **Threshold** (Knob 3) clockwise past the midpoint to make it visible.
2. Adjust **Axis Ang** (Knob 2) to widen the highlight band. Turning clockwise increases the band's thickness, making the streak broader and more prominent.
3. Turn up **Threshold** (Knob 3) further. The highlight becomes stronger: bright areas of the source image light up where they meet the streak.
4. Sweep **Streak L** (Knob 5) slowly. The streak glides vertically up and down the frame, interacting with different parts of the source as it moves. This is the cat's-eye effect: a band of specular light that reveals the image content it passes over.

---

## Parameters

![Videomancer front panel with Chatoyant loaded](/img/instruments/videomancer/chatoyant/chatoyant_control_panel.png)
*Videomancer's front panel with Chatoyant active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Streak W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Streak W** controls the angular orientation of the streak when the direction mode is set to free (see Toggle Group Notes below). In free mode, this knob determines how steeply the streak tilts from horizontal. At 0%, fully counterclockwise, the streak is nearly level. As the value increases, the streak tilts more, adding an increasing horizontal contribution to the streak's slope. At 100%, the streak is tilted at a steep diagonal.

In vertical direction mode, this control instead sets the horizontal position of the vertical streak line. In horizontal and diagonal modes, this control has no effect on the streak position.

:::note
The behavior of **Streak W** changes depending on the direction mode set by **Gem Type** and **Streaks**. In free mode it's an angle control; in vertical mode it's a position control.
:::

---

### Knob 2 — Axis Ang

| Property | Value |
|----------|-------|
| Range | 0° – 180° |
| Default | 90° |

**Axis Ang** controls the width of the highlight band: how many pixels on either side of the streak center are affected by the specular boost. At 0%, fully counterclockwise, the band is very narrow (about 4 pixels wide), producing a thin, crisp line of light. As the value increases, the band broadens. At 100%, the band is roughly 260 pixels wide, creating a soft, diffuse wash of highlight across a large swath of the frame.

The band width also affects the falloff behavior: pixels in the center half of the band receive full highlight, while pixels in the outer half are attenuated according to **Intensity** (Knob 4).

---

### Knob 3 — Threshold

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Threshold** controls the brightness boost applied to pixels within the highlight band. It determines how strongly the streak emphasizes bright areas of the source. At low values (0 to 25%), the boost is very subtle: a gentle glow that barely alters the image. At moderate values (25 to 50%), the highlight becomes clearly visible as a band of increased brightness. At higher values (50 to 75%), the boost is strong and conspicuous. At maximum (75 to 100%), the highlight is at full intensity, capable of pushing bright source pixels to peak white.

The boost is always proportional to source brightness: dark pixels receive little to no boost regardless of this setting.

---

### Knob 4 — Intensity

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Intensity** controls the edge softness of the highlight band: how quickly the specular boost fades from the center of the streak toward its edges. At 0%, the falloff is sharp: pixels outside the center half of the band drop off quickly, creating a hard-edged streak. As the value increases, the falloff becomes more gradual, and the edges of the band blend smoothly into the unaffected image. At 100%, the falloff is very gentle, producing a soft, Gaussian-like highlight profile.

:::tip
Combine a wide **Axis Ang** with a gradual **Intensity** falloff for a dreamy, atmospheric glow. Use a narrow **Axis Ang** with a sharp falloff for a crisp, laser-like line of light.
:::

---

### Knob 5 — Streak L

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Streak L** controls the vertical position of the streak across the frame. At 0%, the streak sits at the top of the frame. As the value increases, the streak moves downward. At 100%, the streak is near the bottom edge. This control provides the primary means of positioning the chatoyant band (sweeping it slowly produces the classic cat's-eye glide.)

In horizontal, diagonal, and free direction modes, **Streak L** is the base position for the streak. In vertical mode, the streak position is determined by **Streak W** (Knob 1) instead, and **Streak L** has no effect.

---

### Knob 6 — Hue Tint

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Hue Tint** controls the contribution of the ***vertical gradient***: the difference in brightness between each pixel and the pixel directly above it: to the highlight calculation. Below the midpoint, this control is inactive: the highlight depends only on source brightness and distance from the streak center. Above the midpoint, the vertical gradient adds to the highlight intensity, causing the streak to emphasize horizontal edges in the source image: places where brightness changes sharply from one scan line to the next.

This makes the highlight ***edge-sensitive***: the streak brightens not only where the source is bright but also where brightness is changing rapidly in the vertical direction. The effect is subtle but adds texture and definition to the specular band.

:::note
Despite the display showing a 0 to 360° range, this control behaves as a threshold: below the midpoint it is off, above the midpoint it is on. The numerical display does not correspond to a hue rotation.
:::

---

### Switch 7 — Gem Type

| Property | Value |
|----------|-------|
| Off | Tigers |
| On | Opal |
| Default | Tigers |

**Gem Type** works together with **Streaks** (Switch 8) to select the direction mode of the streak. See the Toggle Group Notes section below for the full mode table.

With **Gem Type** set to **Tigers** and **Streaks** set to **1**, the direction mode is free: **Streak W** (Knob 1) controls the angle of the streak. With **Gem Type** set to **Opal**, the streak locks to a fixed horizontal orientation.

---

### Switch 8 — Streaks

| Property | Value |
|----------|-------|
| Off | 1 |
| On | 6 |
| Default | 1 |

**Streaks** works together with **Gem Type** (Switch 7) to select the direction mode. See the Toggle Group Notes section below for the full mode table.

With **Streaks** set to **6** and **Gem Type** set to **Tigers**, the streak locks to a vertical orientation. With both set to their alternate positions (**Opal** and **6**), the streak follows a 45-degree diagonal.

---

### Switch 9 — Color Hlt

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color Hlt** selects the color temperature of the specular highlight. With the switch set to **Off**, the highlight is tinted warm: shifting toward ***amber and gold*** by pulling the U channel below neutral and pushing the V channel above neutral. With the switch set to **On**, the highlight is tinted cool: shifting toward ***blue and white*** by pushing U above neutral and pulling V below neutral.

The color tint is proportional to the brightness boost: stronger highlights produce more visible tinting. When the boost is very small (below a threshold of about 16 levels), no tint is applied and the source chroma passes through unchanged.

---

### Switch 10 — Anim

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Anim** creates a mirrored companion streak at a symmetrical position on the opposite side of the frame. With the switch set to **Off**, a single streak appears. With the switch set to **On**, a second streak appears at the vertically mirrored position (active height minus the primary streak position). Each pixel is highlighted by whichever streak is closer, creating a symmetrical pair of specular bands.

:::tip
The mirrored pair works well with diagonal or free modes, creating an X-shaped or V-shaped pattern of intersecting highlights.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** enables continuous animated motion of the streak. With the switch set to **Off**, the streak sits at its stationary position determined by **Streak L** or **Streak W**. With the switch set to **On**, the streak sweeps continuously up and down (or across, depending on mode), creating a scanning motion. The sweep bounces between the top and bottom edges of the active frame at a rate determined by the pixel clock.

Because the sweep accumulator runs at the full clock rate, the animation creates a rapid within-frame modulation: the streak's position shifts during the raster scan itself, producing a dynamic, continuously evolving pattern rather than a slow, steady glide.

---

:::note Toggle Group Notes

**Gem Type** (Switch 7) and **Streaks** (Switch 8) form a combined two-bit direction mode selector. Together they determine the orientation and positional behavior of the chatoyant streak:

| Gem Type | Streaks | Direction Mode | Behavior |
|----------|---------|----------------|----------|
| Tigers | 1 | Free | Streak W (Knob 1) controls tilt angle. Streak L (Knob 5) sets vertical position. |
| Opal | 1 | Horizontal | Streak is a horizontal band. Streak L (Knob 5) sets vertical position. |
| Tigers | 6 | Vertical | Streak is a vertical band. Streak W (Knob 1) sets horizontal position. |
| Opal | 6 | Diagonal | Streak follows a 45° diagonal path. Streak L (Knob 5) sets base position. |

In free mode, the streak's slope is controlled by the top three bits of **Streak W**, producing eight discrete tilt levels ranging from flat (0%) to steeply angled (100%). In locked modes (horizontal, vertical, diagonal), the streak geometry is fixed and the relevant position control adjusts placement only.

:::tip
**Tigers + 1** (free mode) is the most versatile starting point. Lock to a direction only when you need a perfectly straight horizontal, vertical, or diagonal band.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (highlight-composited) output. At 0%, the output is pure dry signal: identical to the source. At 100%, the output is the fully processed result with all highlight and tint effects applied. Intermediate values blend the two proportionally using linear interpolation across all three YUV channels.

:::tip
Use a moderate Mix value (40–60%) to retain source fidelity while adding a gentle specular sheen. Full wet (100%) is most dramatic but can overwhelm subtle source detail.
:::

---

## Background

### Chatoyancy and Asterism

***Chatoyancy*** is an optical phenomenon caused by the reflection of light from parallel needle-like inclusions within a gemstone. When a stone like ***tiger's eye*** or ***chrysoberyl*** is cut into a cabochon (a smooth, domed shape), the aligned fibers act as a cylindrical mirror, reflecting light into a single bright band that appears to glide across the surface as the viewing angle changes. This band is the "cat's eye."

A related phenomenon, ***asterism***, occurs when a gemstone contains multiple sets of parallel inclusions oriented at different angles. ***Star sapphires*** and ***star rubies*** display six-rayed stars where three sets of inclusions at 60° angles produce intersecting bands. Chatoyant's direction mode selector provides a simplified version of this: single-axis chatoyancy in free or locked orientations, with the mirrored double-streak option creating a two-axis pattern.

### Specular Highlights in Video

In optical systems, a ***specular highlight*** is the bright spot or streak created when light reflects off a smooth surface at the angle of maximum reflection. Unlike ***diffuse reflection***, which scatters light evenly in all directions, specular reflection concentrates light into a narrow range of angles. Chatoyant simulates this by boosting the brightness of source pixels only where they fall within the streak band, and scaling the boost by the source's own luminance: so brighter pixels receive more specular energy, just as a glossy surface produces stronger highlights than a matte one.

### Gradient-Based Edge Detection

Chatoyant includes a simple vertical ***gradient detector***: it stores the previous scan line's luminance in a line buffer and computes the absolute difference between each pixel and the pixel directly above it. Large differences indicate horizontal edges: boundaries where brightness changes sharply. When the **Hue Tint** control is above its midpoint, this gradient is added to the highlight calculation, making the streak ***edge-sensitive***. The streak then emphasizes not just brightness but also contrast boundaries, adding definition and texture to the specular band.


---

## Signal Flow

### Signal Flow Notes

Three key interactions define Chatoyant's behavior:

1. **Brightness-reactive highlighting**: The highlight boost is proportional to the source luma. The VHDL computes `v_luma_scale := Y >> 2`, then applies the **Threshold** shift to scale the final boost. This means the streak is invisible on black areas and strongest on white areas (the effect is inherently content-adaptive.)

2. **Two-zone falloff**: The streak band is divided into a center zone (inner half) and an edge zone (outer half). Pixels in the center receive the full luma-scaled highlight. Pixels in the edge zone are attenuated by the **Intensity** falloff shift. This creates a highlight profile that is brightest at the center and tapers toward the edges, approximating a Gaussian cross-section.

3. **Color tint blending**: When the highlight boost exceeds a threshold of 16 levels, the highlight pixels receive a chromatic tint. The tint is blended 50/50 with the source chroma using a shift-based mix: `U_out = (source_U >> 1) + (tint_U >> 1)`. This ensures the tint is visible but doesn't completely overwrite the source color information.

:::note
The line buffer stores only one previous scan line of luma. The gradient is purely vertical (line-to-line brightness difference). There is no horizontal gradient computation.
:::


---

## Exercises

These exercises progress from a simple static streak to animated multi-streak configurations. Each builds on the previous, engaging more of the processing chain.
### Exercise 1: Cat's-Eye Glide

![Cat's-Eye Glide result](/img/instruments/videomancer/chatoyant/chatoyant_ex1_s1.png)
*Cat's-Eye Glide — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A single bright streak that glides up and down the frame, illuminating bright areas of the source as it passes over them.

#### Key Concepts

- The chatoyant streak interacts with source brightness
- Sweeping the position control produces the classic cat's-eye glide
- Highlight intensity scales with source luma

#### Video Source

A live camera feed or recorded footage with a mix of bright and dark regions (faces, lamps, windows, or high-contrast graphics.)

#### Steps

1. **Position the streak**: Set **Streak L** (Knob 5) to about 50%. A horizontal highlight band should appear near the center of the frame.
2. **Widen the band**: Turn **Axis Ang** (Knob 2) to about 40%. The highlight band broadens into a visible swath.
3. **Increase the boost**: Turn **Threshold** (Knob 3) past the 75% mark. Bright areas within the band should now glow distinctly.
4. **Glide the streak**: Slowly sweep **Streak L** from 0% to 100%. Watch how the streak illuminates different parts of the image as it moves (bright areas light up, dark areas remain unchanged.)
5. **Soften the edges**: Increase **Intensity** (Knob 4) to about 70%. The band's edges become more gradual and natural-looking.

#### Settings

| Control | Value |
|---------|-------|
| Streak W | 0% |
| Axis Ang | 40% |
| Threshold | 80% |
| Intensity | 70% |
| Streak L | 50% |
| Hue Tint | 0° |
| Gem Type | Tigers |
| Streaks | 1 |
| Color Hlt | Off |
| Anim | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Warm and Cool Tinting

![Warm and Cool Tinting result](/img/instruments/videomancer/chatoyant/chatoyant_ex2_s1.png)
*Warm and Cool Tinting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Explore the color tint options and direction modes to create warm golden highlights and cool icy streaks.

#### Key Concepts

- The Color Hlt toggle shifts the highlight toward warm or cool tones
- The tint is proportional to the brightness boost
- Direction modes change the streak's geometry

#### Video Source

Footage with skin tones, metallic surfaces, or warm-lit scenes (these show tint shifts most clearly.)

#### Steps

1. **Start with a visible streak**: Use the settings from Exercise 1 as a starting point.
2. **Enable warm tint**: Ensure **Color Hlt** (Switch 9) is set to **Off** (warm mode). The highlight should take on a subtle amber-gold character, especially visible in brighter areas.
3. **Switch to cool tint**: Flip **Color Hlt** to **On**. The highlight shifts toward blue-white, giving a cooler, more clinical look.
4. **Lock horizontal**: Set **Gem Type** (Switch 7) to **Opal** and **Streaks** (Switch 8) to **1**. The streak snaps to a perfectly horizontal band.
5. **Lock vertical**: Set **Gem Type** to **Tigers** and **Streaks** to **6**. The streak becomes vertical. Adjust **Streak W** (Knob 1) to position it horizontally.
6. **Diagonal**: Set both to their alternate positions (**Opal** + **6**). The streak follows a 45-degree diagonal.

#### Settings

| Control | Value |
|---------|-------|
| Streak W | 50% |
| Axis Ang | 50% |
| Threshold | 80% |
| Intensity | 50% |
| Streak L | 50% |
| Hue Tint | 0° |
| Gem Type | Opal |
| Streaks | 1 |
| Color Hlt | On |
| Anim | Off |
| Bypass | Off |
| Mix | 80% |

---

### Exercise 3: Animated Double Streak

![Animated Double Streak result](/img/instruments/videomancer/chatoyant/chatoyant_ex3_s1.png)
*Animated Double Streak — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Combine the double-streak mirror and animation modes to create a dynamic, symmetrical pattern of scanning highlights.

#### Key Concepts

- The Anim switch creates a mirrored pair of streaks
- The Bypass switch enables continuous animated sweep
- The Hue Tint control adds edge sensitivity via gradient detection

#### Video Source

High-contrast footage works best: geometric patterns, architectural scenes, or video feedback loops.

#### Steps

1. **Enable double streak**: Flip **Anim** (Switch 10) to **On**. A second streak appears at a mirrored vertical position, creating a symmetrical pair.
2. **Enable animation**: Flip **Bypass** (Switch 11) to **On**. Both streaks begin sweeping dynamically, creating a continuously evolving pattern of highlights.
3. **Add edge sensitivity**: Turn **Hue Tint** (Knob 6) past the midpoint (above 180°). The highlights now emphasize horizontal edges in the source, adding texture and definition.
4. **Widen and soften**: Increase **Axis Ang** (Knob 2) to about 60% and **Intensity** (Knob 4) to about 80%. The sweeping streaks become broad, soft washes of specular light.
5. **Tint the highlights**: Flip **Color Hlt** (Switch 9) to **On** for cool blue-white highlights, or leave it **Off** for warm amber.
6. **Mix for subtlety**: Pull the **Mix** (Fader 12) down to about 50%. The animated highlights blend gently with the source, producing a shimmering overlay.

#### Settings

| Control | Value |
|---------|-------|
| Streak W | 50% |
| Axis Ang | 60% |
| Threshold | 80% |
| Intensity | 80% |
| Streak L | 30% |
| Hue Tint | 270° |
| Gem Type | Tigers |
| Streaks | 1 |
| Color Hlt | On |
| Anim | On |
| Bypass | On |
| Mix | 50% |

---
## Glossary

- **Asterism**: An optical phenomenon in gemstones where multiple sets of parallel inclusions create a multi-rayed star pattern of reflected light.

- **Cabochon**: A gemstone that has been polished into a smooth, rounded dome rather than faceted, which is the shape that best displays chatoyancy.

- **Chatoyancy**: The cat's-eye optical effect in certain fibrous gemstones, where a single bright band of light appears to glide across the surface as the viewing angle changes.

- **Falloff**: The rate at which a signal's intensity decreases with distance from its center point; sharp falloff produces hard edges, gradual falloff produces soft transitions.

- **Gradient**: The rate of change of a value over distance; in Chatoyant, the vertical gradient is the brightness difference between adjacent scan lines.

- **Interpolator**: A hardware component that computes a weighted blend between two input values; used here for the dry/wet mix crossfade.

- **Line Buffer**: A block RAM that stores one complete scan line of pixel data for vertical comparisons between adjacent lines.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Specular Highlight**: A concentrated bright reflection from a smooth surface where the angle of reflection aligns with the viewer; contrasts with diffuse reflection, which scatters light evenly.

---
