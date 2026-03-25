---
draft: true
sidebar_position: 4
slug: /instruments/videomancer/amoeba
title: "Amoeba"
image: /img/instruments/videomancer/amoeba/amoeba_hero.png
description: "Amoeba is a metaball isosurface engine."
---

![Amoeba hero image](/img/instruments/videomancer/amoeba/amoeba_hero_s1.png)
*Amoeba generating four luminous metaball blobs that orbit, merge, and split in organic Lissajous patterns against a black field.*

---

## Overview

Amoeba is a real-time ***metaball*** synthesizer. It projects up to four glowing blobs onto the screen, each following its own ***Lissajous*** orbit: a smooth, looping path created by combining sine and cosine waves at different frequencies. Where blobs approach one another, their fields combine and their boundaries merge, producing the soft, organic fusion characteristic of metaball graphics. The effect resembles lava lamps, cell division, and living organisms.

At its simplest, Amoeba places a single bright circle on screen. Add more blobs and they begin to interact: two blobs flowing toward each other stretch and merge into one shape, then pinch and split apart again. The animation is continuous, self-evolving, and endlessly varied. Adjusting the threshold and skin width controls changes the apparent size of the shapes and the sharpness of their edges.

Amoeba can also key incoming video through its blob shapes using the **Source** toggle, letting you composite live footage inside the organic forms. Combined with the **Rainbow** color mode and **Hue Shift** control, the metaballs become vivid, chromatic organisms drifting across the frame.

:::tip
Amoeba is a ***synthesis*** program: it generates its own imagery without requiring a video input. Patch it at the beginning of your signal chain as a source, or layer it over existing footage using the **Mix** fader.
:::

### What's In a Name?

An ***amoeba*** is a single-celled organism that moves by extending and retracting pseudopods: temporary, bloblike projections of its body. The name captures both the organic visual quality of the metaball shapes and their tendency to merge, divide, and flow like living cells under a microscope.

---

## Quick Start

1. Set **Count** (Knob 6) fully clockwise to activate all four blobs. You should see four bright shapes orbiting the screen along overlapping curved paths.
2. Turn **Blob Size** (Knob 1) clockwise to about 60%. The shapes expand and begin merging where their orbits intersect (watch the boundaries stretch and fuse.)
3. Adjust **Threshold** (Knob 2) to control how much of each blob's field is visible. Lower values reveal larger, softer shapes; higher values shrink them to tight cores.
4. Enable **Rainbow** color by flipping the **Color** toggle (Switch 8) to **Rainbow**, then rotate **Hue Shift** (Knob 5) to explore the chromatic palette.

---

## Parameters

![Videomancer front panel with Amoeba loaded](/img/instruments/videomancer/amoeba/amoeba_control_panel.png)
*Videomancer's front panel with Amoeba active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Blob Size

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Blob Size** controls two things simultaneously: the amplitude of each blob's orbital path and the strength of its field contribution. At 0%, the blobs are tiny points clustered near the center of the screen with minimal orbits. As the value increases, the blobs travel wider paths and project stronger fields, growing larger and more likely to merge with one another. At 100%, the blobs sweep across most of the frame and their fields extend far from center, producing large, luminous shapes that overlap frequently.

:::note
Because **Blob Size** controls both the orbit radius and the field strength, increasing it doesn't just make the shapes bigger: it also changes the character of the animation. Larger blobs spend more time in overlap, so the metaball merging effect becomes more prominent.
:::

---

### Knob 2 — Threshold

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |

**Threshold** sets the ***isosurface*** level: the boundary between "inside" and "outside" the metaball field. Every pixel on screen has a field value computed from its distance to each blob center. Pixels whose combined field exceeds the threshold are classified as inside; those below it are outside. At 0%, the threshold is very low and nearly the entire screen is filled with metaball interior. As the value increases, the visible shapes shrink until only the pixel positions closest to a blob center remain lit. At 100%, only extremely strong field values survive, producing small, tight dots.

---

### Knob 3 — Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Speed** controls how quickly the blob phase accumulators advance, determining the rate of animation. At 0%, the blobs are nearly frozen in place. As the value increases, the orbits accelerate. At 100%, the blobs move rapidly, creating fast-flowing organic motion. Because each blob has a different frequency ratio for its X and Y axes, changing the speed doesn't simply make everything move faster: it also shifts the relative timing of the merge-and-split patterns.

:::tip
Very low **Speed** values are useful for slow, meditative compositions. At moderate values, the merging and splitting happens at a pace that is easy to follow visually. High values create rapid, pulsating animation.
:::

---

### Knob 4 — Skin Width

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |

**Skin Width** determines the thickness of the transition zone between the inside and outside of each metaball shape. This zone: the ***skin***: is the bright edge region where the field value is close to the threshold. At 0%, the skin is infinitely thin: the boundary between blob and background is a hard, sharp edge. As the value increases, the transition zone widens, producing a soft, glowing halo around each shape. At 100%, the skin zone is at its widest, creating broad gradients at the edges.

When **Outline** mode is enabled (Switch 10), only the skin zone is bright and the interior goes dark, making skin width directly control the thickness of the outline stroke.

---

### Knob 5 — Hue Shift

| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |

**Hue Shift** rotates the color of the metaballs when **Color** (Switch 8) is set to **Rainbow**. At 0 degrees, the rainbow coloring uses its default palette derived from the field strength. Rotating the knob shifts the hue through a full 360-degree cycle, sliding the color spectrum across the shapes. In **Mono** mode, this control has no visible effect.

---

### Knob 6 — Count

| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

**Count** selects how many blobs are active, from one to four. At the lowest setting, a single blob appears: useful for studying one shape in isolation. At two, the blobs begin to interact, merging and splitting as their orbits cross. Three and four blobs create increasingly complex patterns as multiple shapes overlap simultaneously.

:::note
Each blob follows a unique Lissajous path determined by fixed frequency ratios. Blob 1 orbits at a 1:2 ratio (X to Y), blob 2 at 3:1, blob 3 at 2:5, and blob 4 at 5:3. These ratios ensure that the blobs never simply chase each other in identical circles (their paths weave in and out of alignment over time.)
:::

---

### Switch 7 — Fill Mode

| Property | Value |
|----------|-------|
| Off | Solid |
| On | Hollow |
| Default | Solid |

**Fill Mode** determines what appears inside the metaball boundary. In **Solid** mode, the interior is filled with brightness proportional to the field strength (or with the incoming video signal if **Source** is set to **Video**). The brightest areas are at the blob centers, fading toward the edges. In **Hollow** mode, the interior is black: only the skin zone (the edge transition) is visible. Hollow mode is especially striking when combined with **Outline** (Switch 10), producing bright rings that merge and separate.

---

### Switch 8 — Color

| Property | Value |
|----------|-------|
| Off | Mono |
| On | Rainbow |
| Default | Mono |

**Color** switches between monochrome and rainbow rendering. In **Mono** mode, the metaballs are rendered as achromatic (grayscale) shapes: luminance only, with neutral chroma. In **Rainbow** mode, the U and V chroma channels are modulated by the field strength, producing colors that shift from cool to warm across the interior of each shape. The exact palette depends on the **Hue Shift** (Knob 5) setting.

---

### Switch 9 — Source

| Property | Value |
|----------|-------|
| Off | Synth |
| On | Video |
| Default | Synth |

**Source** selects whether the interior of each metaball is self-generated or sampled from the video input. In **Synth** mode, interior brightness comes from the computed field value: the blobs glow with their own internally generated luminance. In **Video** mode, the incoming video signal's luminance is used instead, effectively keying the video through the metaball shapes. The metaballs become windows into whatever is patched at the video input.

:::tip
Use **Video** mode to composite live footage inside the organic blobs. The metaball shapes act as a dynamic, animated ***matte***: the video is visible only where the field exceeds the threshold.
:::

---

### Switch 10 — Outline

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Outline** controls whether the skin zone is rendered as a bright boundary line. When **Off**, the skin zone displays a gradient proportional to the field strength. When **On**, the skin zone is rendered at maximum brightness (white in Mono mode, or colored in Rainbow mode), creating a crisp outline around each shape. Combined with **Hollow** fill mode (Switch 7), this produces glowing rings.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, disabling all Amoeba synthesis. The sync delay pipeline still aligns timing. Use Bypass for instant A/B comparison.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the original input video (fully counter-clockwise) and the Amoeba output (fully clockwise). At 0%, you see only the unprocessed input. At 100%, you see only the metaball synthesis. Intermediate values blend the two, allowing you to superimpose the metaball shapes over incoming footage at any desired opacity.

---

## Background

### Metaballs

***Metaballs*** are a computer graphics technique invented by Jim Blinn in 1982. Each metaball is a point in space that projects a field: a mathematical function that diminishes with distance. The classic field function is ***inverse-square***: the field strength is proportional to 1/d², where d is the distance from the center. At any point on screen, the total field is the sum of contributions from all nearby metaballs.

An ***isosurface*** is the set of all points where the total field equals a chosen threshold. In 2D, this produces smooth contour lines; in 3D, it produces blobby surfaces. When two metaballs are far apart, their isosurfaces are two separate circles. As they approach each other, their fields combine and the isosurfaces merge into a single, peanut-shaped form. This smooth blending is the defining visual characteristic of metaballs (there are no hard corners or seams, just organic flow.)

### Lissajous curves

Each blob's center position is computed from a ***Lissajous curve***: a parametric path where the X coordinate follows a sine function and the Y coordinate follows another sine function at a different frequency. The ratio of the two frequencies determines the shape of the path: a 1:1 ratio traces an ellipse, a 1:2 ratio traces a figure-eight, a 3:2 ratio traces a more complex pretzel-like loop, and so on. The four blobs in Amoeba use the ratios 1:2, 3:1, 2:5, and 5:3 for their X-to-Y frequency relationships, producing four distinct looping paths that overlap in complex, evolving patterns.

### Inverse-square fields

Amoeba computes each blob's field contribution using a 256-entry lookup table that maps distance-squared to a 10-bit field value. The formula is approximately 16384 / (d² + 1), clamped to the 10-bit range. This produces a steep falloff: the field is strongest at the center and drops off rapidly, reaching negligible levels within a few dozen pixels. When multiple blobs contribute to the same pixel, their field values are summed: this additive combination is what allows the isosurface to bulge outward and merge between adjacent blobs.


---

## Signal Flow

### Signal Flow Notes

The pipeline is divided into two phases. During ***vertical blanking***, the four blob center positions are updated. The phase accumulators advance by a speed-scaled increment multiplied by each blob's fixed frequency ratio, and the sin/cos LUT converts each phase into a screen coordinate centered around (640, 360). This computation is sequential: one blob at a time across four clock cycles: because it shares a single sin/cos LUT instance.

During ***active video***, the per-pixel pipeline runs in three stages. Stage 1 computes the squared distance from the current pixel to each of the four blob centers in parallel. Stage 2 scales each distance by the blob size parameter, looks up the inverse-square contribution from the BRAM LUT, sums all active blobs' contributions, and classifies the pixel. Stage 3 generates the output color based on the fill mode, color mode, source, and outline settings. The final interpolator crossfades between the delayed input video and the generated color.

:::note
The blob size parameter does double duty. It controls the orbit amplitude during vblank center computation (via bit-shifting the sin output) *and* the field falloff steepness during per-pixel evaluation (via the distance-to-LUT-index shift amount). This coupling is intentional (larger orbits naturally produce larger blobs.)
:::


---

## Exercises

These exercises progress from a single static blob to complex multi-blob synthesis with color and video keying.
### Exercise 1: Single Blob Exploration

![Single Blob Exploration result](/img/instruments/videomancer/amoeba/amoeba_ex1_s1.png)
*Single Blob Exploration — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A single glowing orb, experimenting with its shape, edges, and color.

#### Key Concepts

- Metaball field strength falls off with distance
- Threshold controls the visible boundary
- Skin width creates a soft edge transition

#### Steps

1. Set **Count** (Knob 6) to its lowest position (1 blob). A single bright circle appears on screen.
2. Increase **Blob Size** (Knob 1) to about 60%. The shape grows larger and begins to drift along its Lissajous orbit.
3. Lower **Speed** (Knob 3) to about 10% so the motion is slow enough to study.
4. Sweep **Threshold** (Knob 2) slowly from low to high. At low values, the shape is large and soft; at high values, it shrinks to a tight bright dot. Find a middle setting where the boundary is clearly defined.
5. Now increase **Skin Width** (Knob 4) from 0% upward. Watch the edge of the blob develop a soft halo that broadens as you turn.
6. Enable **Outline** (Switch 10). The interior darkens and only the skin zone glows, producing a bright ring.

#### Settings

| Control | Value |
|---------|-------|
| Blob Size | 60% |
| Threshold | 40% |
| Speed | 10% |
| Skin Width | 30% |
| Hue Shift | 0 d |
| Count | 1 |
| Fill Mode | Solid |
| Color | Mono |
| Source | Synth |
| Outline | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Merging Metaballs

![Merging Metaballs result](/img/instruments/videomancer/amoeba/amoeba_ex2_s1.png)
*Merging Metaballs — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Two to four blobs that merge and divide in flowing organic patterns.

#### Key Concepts

- Metaball fields are additive (overlapping blobs merge)
- Lissajous frequency ratios create varied orbit shapes
- Speed affects the timing of merge and split events

#### Steps

1. Set **Count** (Knob 6) to 2. Two blobs appear, each on its own orbital path.
2. Set **Blob Size** (Knob 1) to about 55% and **Threshold** (Knob 2) to about 40%. The two shapes should be large enough to overlap periodically.
3. Watch the blobs merge as they approach each other: notice the smooth, stretchy bridge that forms between them. As they separate, the bridge pinches and the shapes split apart.
4. Increase **Count** to 3, then 4. The interactions multiply: three-way and four-way merges produce complex, amorphous shapes.
5. Switch **Color** (Switch 8) to **Rainbow** and rotate **Hue Shift** (Knob 5) slowly through 360 degrees. The blobs take on vivid hues that shift across the spectrum.
6. Increase **Speed** (Knob 3) to about 50% for faster, more dynamic merging. Then try very high speeds for rapid pulsation.

#### Settings

| Control | Value |
|---------|-------|
| Blob Size | 55% |
| Threshold | 40% |
| Speed | 50% |
| Skin Width | 30% |
| Hue Shift | 170 d |
| Count | 4 |
| Fill Mode | Solid |
| Color | Rainbow |
| Source | Synth |
| Outline | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Video Keying Through Metaballs

![Video Keying Through Metaballs result](/img/instruments/videomancer/amoeba/amoeba_ex3_s1.png)
*Video Keying Through Metaballs — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Live video revealed through animated metaball windows, layered over incoming footage.

#### Key Concepts

- Metaball shapes can act as a dynamic matte for video
- Mix fader blends synthesis with live input
- Hollow and outline modes change the compositing character

#### Steps

1. Patch a video source into the Videomancer input. Set **Source** (Switch 9) to **Video**. The metaball interiors now show the video feed instead of self-generated luminance.
2. Set **Count** (Knob 6) to 3 or 4, **Blob Size** (Knob 1) to about 50%, and **Threshold** (Knob 2) to about 40%.
3. Watch the video appear only inside the metaball shapes. The organic, merging boundaries frame the footage dynamically.
4. Switch **Fill Mode** (Switch 7) to **Hollow**. Now only the skin edge is visible: the video disappears from the interior, leaving glowing outlines.
5. Set **Mix** (Fader 12) to about 50%. The metaball shapes blend with the unprocessed input, creating a translucent overlay effect.
6. Enable **Outline** (Switch 10) and set **Color** to **Rainbow**. The outlines become vivid colored rings drifting over the video.

#### Settings

| Control | Value |
|---------|-------|
| Blob Size | 50% |
| Threshold | 40% |
| Speed | 25% |
| Skin Width | 40% |
| Hue Shift | 200 d |
| Count | 3 |
| Fill Mode | Solid |
| Color | Rainbow |
| Source | Video |
| Outline | On |
| Bypass | Off |
| Mix | 50% |

---
## Glossary

- **Inverse-Square Falloff**: A mathematical relationship where a quantity diminishes proportionally to the square of the distance; used here to compute each blob's field contribution.

- **Isosurface**: The set of all points where a scalar field equals a given threshold value; in 2D, this produces a contour line (the metaball boundary.)

- **Lissajous Curve**: A parametric path created by combining sinusoidal motions on two axes at different frequencies; the characteristic figure-eight and pretzel-shaped orbits.

- **Matte**: A mask that determines which pixels are visible and which are transparent; Amoeba's metaball shapes can serve as a dynamic, animated matte for video keying.

- **Metaball**: A computer graphics technique where point sources project scalar fields that combine additively, producing smooth, bloblike shapes that merge organically.

- **Phase Accumulator**: A counter that advances by a fixed increment each frame, wrapping around to produce a repeating cycle; drives the Lissajous animation.

- **Scalar Field**: A function that assigns a single numeric value to every point in space; here, the field diminishes with distance from each blob center.

- **Skin Zone**: The transition region between the metaball interior and exterior where the field value is close to the threshold; rendered as a gradient or outline.

---
