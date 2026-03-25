---
draft: true
sidebar_position: 281
slug: /instruments/videomancer/spore
title: "Spore"
image: /img/instruments/videomancer/spore/spore_hero.png
description: "In nature, a spore is a reproductive cell released by fungi, mosses, and ferns — a microscopic package of potential life that drifts outward from its source, carried by wind, water, or animal contact."
---

![Spore hero image](/img/instruments/videomancer/spore/spore_hero_s1.png)
*Spore generating concentric particle rings that expand outward from clustered emission points, dissolving into luminous clouds of noise-gated debris.*

---

## Overview

Spore is a particle-based synthesis program that generates expanding rings of bright spore particles from two or four source points on screen. Each source point emits concentric diamond-shaped rings that grow outward frame by frame, creating the illusion of spore clouds dispersing from their origin. A pseudorandom noise gate filters individual particles within each ring, breaking the geometric perfection into an organic, dissolving texture.

The effect is additive: spore particles brighten the underlying video signal rather than replacing it. With a dark or absent input, the spores appear as constellations of bright dots radiating outward from their emission points. With a live video input, the expanding rings overlay a shimmering, luminous texture that tracks across the image like biological growth or wind-scattered debris.

:::tip
**Spore is a synthesis program.** It generates its own pattern and overlays it onto whatever video signal arrives at the input. No input signal is required: the spore pattern will appear on a black background if nothing is connected.
:::

### What's In a Name?

The name ***Spore*** draws from mycology: the study of fungi. In nature, a spore is a tiny reproductive cell released by fungi, mosses, and ferns. Mushrooms release billions of spores from a single fruiting body, forming expanding clouds that drift outward on air currents. Spore's concentric rings mimic this dispersal pattern: bright particles radiate from fixed emission points, thinning as they travel, their density governed by a noise gate that simulates the randomness of wind and gravity.

---

## Quick Start

1. Set **Sources** (Knob 1) to about 50%. Two bright clusters of expanding rings appear, positioned symmetrically around the center of the screen. The rings grow outward continuously.
2. Turn **Spore Sz** (Knob 4) fully clockwise. The rings fill in with dense particles. Now sweep it counterclockwise: particles thin out, revealing the ring skeleton beneath the noise.
3. Increase **Fade Dst** (Knob 5) to brighten the spore overlay. The rings become vivid luminous bands against the background.
4. Flip **Pattern** (Switch 7) to **Plume**. Two additional source points appear in the lower quadrants, doubling the ring activity. The four emission points create an overlapping interference pattern as their rings cross.

---

## Parameters

![Videomancer front panel with Spore loaded](/img/instruments/videomancer/spore/spore_control_panel.png)
*Videomancer's front panel with Spore active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Sources

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Sources** controls the spatial separation between the emission points. At 0%, fully counterclockwise, all source points collapse to the center of the screen, stacking their rings on top of one another into a single expanding pattern. As the value increases, the sources spread apart: two points pulling toward opposite corners in **Burst** mode, or four points filling each quadrant in **Plume** mode. At 100%, the sources are at their maximum separation, placing emission points far from center.

:::note
The source positions are always symmetrical around the screen center. **Sources** controls the offset distance, not the absolute position.
:::

---

### Knob 2 — Emit Rat

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Emit Rat** (Emission Rate) controls how quickly the concentric rings expand outward from each source point. At low values, the rings grow slowly: each frame advances the ring radius by a fraction of a pixel, producing a glacial drift. At high values, rings rush outward rapidly, sweeping across the screen in just a few seconds. The expansion rate is divided from the frame clock through a series of power-of-two prescalers, so the speed increases in discrete steps rather than a smooth continuum.

:::tip
At very low **Emit Rat** settings, individual rings become visible as they creep outward. At maximum speed, the animation becomes a continuous ripple.
:::

---

### Knob 3 — Spread

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Spread** controls the thickness and spacing of the concentric rings. This parameter simultaneously sets both the ***ring period*** (distance between successive rings) and the ***ring width*** (how thick each band is). At low values, the rings are tightly packed with narrow bands: fine concentric lines radiating from each source. As **Spread** increases, the rings become wider and more widely spaced, producing broad luminous bands separated by dark gaps. At high values, the rings are so wide they nearly merge into solid circles of light.

The period is quantized to power-of-two masks (128, 256, 512, or 1024 pixels), so the pattern snaps between distinct scales as you sweep the knob.

---

### Knob 4 — Spore Sz

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Spore Sz** (Spore Size) controls the density of visible particles within each ring band. A ***linear feedback shift register*** generates pseudorandom noise on every pixel clock. This noise value is compared against the **Spore Sz** threshold: pixels whose noise falls below the threshold pass through; the rest are filtered out. At 0%, virtually no particles survive the gate: the rings are invisible. As the value increases, more and more pixels within each ring band light up, filling the rings from sparse scattered dots to solid bands. At 100%, every pixel within a ring is visible, producing clean geometric arcs.

:::tip
The sweet spot for organic-looking dispersal is around 30–60%. Below that, you get scattered star fields. Above 80%, the rings look more mechanical and geometric.
:::

---

### Knob 5 — Fade Dst

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Fade Dst** (Fade Distance) controls the brightness intensity of the spore overlay. Each spore pixel adds this brightness value to the underlying luminance: it's a purely additive operation, saturating at peak white. At 0%, spore pixels add no brightness and are invisible. At 100%, each spore pixel adds maximum brightness, driving the overlay to clipped white.

When **Spore** (Switch 8) is set to **Fiber**, this parameter also governs the strength of the chroma tint applied to spore pixels. Higher values produce stronger color shifts.

---

### Knob 6 — Tint

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Tint** is reserved for future use. In the current firmware, adjusting this knob has no visible effect on the output. A later update may connect this parameter to control the hue or color temperature of the spore overlay.

---

### Switch 7 — Pattern

| Property | Value |
|----------|-------|
| Off | Burst |
| On | Plume |
| Default | Burst |

**Pattern** selects the number of active source emission points. In **Burst** mode, two sources are active: positioned symmetrically above and below (or left and right of) the screen center, depending on the **Sources** separation setting. In **Plume** mode, four sources are active, one in each quadrant. Plume mode fills the screen more completely with overlapping ring patterns, creating denser interference where the rings from different sources cross.

---

### Switch 8 — Spore

| Property | Value |
|----------|-------|
| Off | Round |
| On | Fiber |
| Default | Round |

**Spore** selects the color mode of the particle overlay. In **Round** mode, spore pixels receive a pure white brightness boost: the underlying chroma channels pass through unchanged. In **Fiber** mode, spore pixels receive a chroma tint in addition to the brightness boost: the U channel is compressed toward neutral while the V channel is pushed away from neutral, producing a subtle warm-to-cool color shift on the spore particles. The strength of the tint is proportional to the **Fade Dst** (Knob 5) setting.

:::note
The names **Round** and **Fiber** are evocative labels. Round spores are bright and clean, like glowing spheres. Fiber spores carry a color signature, like iridescent filaments.
:::

---

### Switch 9 — React

| Property | Value |
|----------|-------|
| Off | Off |
| On | Luma |
| Default | Off |

**React** controls whether the source emission points drift over time. In **Off** mode, the sources remain at fixed positions determined solely by the **Sources** separation knob. In **Luma** mode, the source positions shift slowly each frame: the drift offset is derived from the internal frame counter, producing a gentle, looping wander. The sources trace a slow diagonal path across the screen, causing the ring patterns to slide and overlap in evolving configurations.

:::tip
Combine **React** set to **Luma** with a moderate **Sources** separation for slowly orbiting emission points that create constantly shifting interference patterns.
:::

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** is intended to enable or disable the ring expansion animation. In the current firmware, ring expansion runs continuously regardless of this toggle's position. Both **Off** and **On** produce the same behavior: rings expand outward at the rate set by **Emit Rat** (Knob 2).

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the input signal directly to the output, skipping all Spore processing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the spore-overlaid result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original input signal and the spore-processed output. At 0%, the output is pure unprocessed input: no spores visible. At 100%, the output is the fully processed signal with spore overlay at maximum strength. Intermediate values blend between the two, allowing you to dial in a subtle spore texture or a dominant particle field.

---

## Background

### Voronoi geometry and Manhattan distance

Spore's ring patterns are fundamentally geometric. Each source point emits concentric rings whose shape is defined by ***Manhattan distance***: a distance metric that measures the sum of horizontal and vertical displacements between two points, rather than the straight-line (Euclidean) distance. Manhattan distance produces diamond-shaped contours instead of circles. If you imagine walking on a grid of city blocks, Manhattan distance is the number of blocks you must walk, always along streets, never cutting diagonally.

The result is that Spore's "rings" are actually concentric diamonds. Each pixel on screen is assigned to the nearest source point by Manhattan distance, and its ring membership is determined by how far it is from that source. This nearest-source assignment implicitly creates a ***Voronoi tessellation***: the screen is divided into regions, one per source, where every pixel belongs to the source it is closest to. The ring pattern within each Voronoi cell radiates outward from its source independently.

### Ring expansion and the frame accumulator

The concentric rings don't just sit still: they expand outward over time. A ***frame accumulator*** increments a ring radius offset once per frame (or once every N frames, depending on the **Emit Rat** speed setting). This offset is added to each pixel's Manhattan distance before the ring band test, which has the effect of shifting the ring pattern outward.

Because the accumulator is a 10-bit counter that wraps around, the expansion is cyclical. Rings grow until they reach the counter's maximum, then the pattern resets and begins again. At high speeds, this produces a rapid pulsing effect. At low speeds, the expansion appears smooth and continuous over many seconds.

### Noise-gated particles

The spore particles are not solid. A ***linear feedback shift register*** (LFSR) generates a pseudorandom number for every pixel on every clock cycle. This noise value is compared against the **Spore Sz** density threshold. Only pixels whose noise falls below the threshold are allowed to light up. This creates a stochastic filter: each ring is not a solid band but a scattered field of bright dots, with the density controlled by the knob.

The LFSR is a 16-bit Galois-type register seeded with a fixed value. It produces a deterministic but visually random sequence that repeats every 65,535 clocks (long enough to appear non-repeating within a single frame.)


---

## Signal Flow

### Signal Flow Notes

The key architectural feature is the separation between the geometric engine and the visual compositing. The position counters, source calculator, and distance computation form a purely spatial subsystem that never touches pixel color data. This subsystem outputs a single boolean per pixel: `spore_on`: which the compositing stage uses to decide whether to brighten that pixel. The two subsystems run in parallel, meeting only at Stage 4.

The ring test itself is a modular arithmetic trick. Adding the continuously incrementing `ring_radius` to the pixel's distance before masking with the period creates the illusion of outward motion: as the radius grows, the point at which each pixel satisfies the ring condition shifts outward. The AND mask with a power-of-two period ensures the pattern repeats concentrically.

:::tip
**The mix fader blends between delayed input and the composed output.** At full **Mix**, you see the original video with bright spore particles overlaid. At zero **Mix**, you see the original video completely clean.
:::


---

## Exercises

These exercises explore Spore's geometric ring patterns, density control, and color overlay modes. Each exercise builds on the previous, gradually engaging more parameters.
### Exercise 1: Diamond Constellations

![Diamond Constellations result](/img/instruments/videomancer/spore/spore_ex1_s1.png)
*Diamond Constellations — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A slowly expanding field of bright diamond-shaped rings emanating from two source points, thinned to scattered particles.

#### Key Concepts

- Manhattan distance produces diamond-shaped contours
- Source separation controls the geometry of the Voronoi tessellation
- Particle density transforms solid rings into scattered star fields

#### Steps

1. Set **Sources** (Knob 1) to about 40%. Two clusters of concentric diamond rings appear on screen, symmetrically placed around center.
2. Set **Emit Rat** (Knob 2) to about 30%. The rings expand outward at a leisurely pace.
3. Set **Spread** (Knob 3) to about 25%. Rings are tightly spaced, creating fine concentric bands.
4. Reduce **Spore Sz** (Knob 4) to about 35%. The solid rings dissolve into scattered bright dots (a constellation of particles tracing diamond paths.)
5. Set **Fade Dst** (Knob 5) to about 70%. The particles are bright and clearly visible.
6. Watch the rings expand. Notice the diamond shape of the contours: this is Manhattan distance in action. Where rings from the two sources overlap, particles appear denser.

#### Settings

| Control | Value |
|---------|-------|
| Sources | ~40% |
| Emit Rat | ~30% |
| Spread | ~25% |
| Spore Sz | ~35% |
| Fade Dst | ~70% |
| Tint | 50% |
| Pattern | Burst |
| Spore | Round |
| React | Off |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Drifting Plume Field

![Drifting Plume Field result](/img/instruments/videomancer/spore/spore_ex2_s1.png)
*Drifting Plume Field — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A four-source pattern with drifting emission points and colored spore particles that create an evolving, organic interference field.

#### Key Concepts

- Four sources create overlapping Voronoi regions
- Drift causes source positions to wander over time
- Fiber color mode adds chroma tinting to spore particles

#### Steps

1. Flip **Pattern** (Switch 7) to **Plume**. Four emission points appear, one per quadrant.
2. Set **Sources** (Knob 1) to about 60%. The sources spread well into their quadrants.
3. Set **Spread** (Knob 3) to about 50%. Rings are moderately thick with visible gaps between them.
4. Set **Spore Sz** (Knob 4) to about 55%. The rings are partially filled (organic but still clearly ring-shaped.)
5. Flip **React** (Switch 9) to **Luma**. The four source points begin to drift slowly across the screen, and the ring patterns follow them. The Voronoi boundaries shift as sources move.
6. Flip **Spore** (Switch 8) to **Fiber**. The spore particles pick up a subtle color tint: warmer or cooler depending on the underlying chroma. Increase **Fade Dst** (Knob 5) to intensify the tint.

#### Settings

| Control | Value |
|---------|-------|
| Sources | ~60% |
| Emit Rat | ~50% |
| Spread | ~50% |
| Spore Sz | ~55% |
| Fade Dst | ~80% |
| Tint | 50% |
| Pattern | Plume |
| Spore | Fiber |
| React | Luma |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Pulsing Supernova

![Pulsing Supernova result](/img/instruments/videomancer/spore/spore_ex3_s1.png)
*Pulsing Supernova — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A rapid-fire burst of solid expanding wavefronts, blended at partial strength over a live input for a pulsating energy aura.

#### Key Concepts

- High emission rate creates rapid ring pulsation
- Dense particles at wide spread produce solid expanding wavefronts
- Mix fader blends the synthesis with the input signal

#### Steps

1. Set **Emit Rat** (Knob 2) to about 90%. Rings rush outward rapidly, creating a pulsing strobe of expanding wavefronts.
2. Set **Spread** (Knob 3) fully clockwise to 100%. Rings become very wide bands (nearly solid circles of light.)
3. Set **Spore Sz** (Knob 4) fully clockwise to 100%. Every pixel in each ring is active (clean geometric bands with no noise filtering.)
4. Set **Sources** (Knob 1) to about 20%. The two sources are close together, and their rings overlap almost completely, reinforcing each other.
5. Set **Fade Dst** (Knob 5) to about 60%. Bright but not fully clipped.
6. Pull the **Mix** fader (Fader 12) to about 40%. The solid expanding wavefronts blend gently over the input video, producing a pulsing energy halo.
7. Try flipping **Pattern** (Switch 7) to **Plume** for four overlapping supernova bursts.

#### Settings

| Control | Value |
|---------|-------|
| Sources | ~20% |
| Emit Rat | ~90% |
| Spread | 100% |
| Spore Sz | 100% |
| Fade Dst | ~60% |
| Tint | 50% |
| Pattern | Burst |
| Spore | Round |
| React | Off |
| Animate | On |
| Bypass | Off |
| Mix | ~40% |

---
## Glossary

- **Frame Accumulator**: A counter that increments once per video frame, used here to advance the ring expansion radius over time.

- **LFSR**: Linear Feedback Shift Register; a hardware circuit that generates a repeating but seemingly random sequence of bits, used for noise and probability gating.

- **Manhattan Distance**: A distance metric that measures displacement as the sum of absolute horizontal and vertical differences, producing diamond-shaped contours instead of circles.

- **Noise Gate**: A threshold filter that compares a random value against a cutoff, allowing only some events to pass through (used here to thin ring particles.)

- **Prescaler**: A divider that slows down a clock or counter by skipping beats, used to control the speed of ring expansion.

- **Ring Period**: The distance, in pixels, between successive concentric rings. Longer periods produce more widely spaced rings.

- **Voronoi Tessellation**: A partitioning of space into regions where each region contains all points nearest to a particular source, creating cell boundaries where two sources are equidistant.

- **Wet/Dry Mix**: A crossfade between the unprocessed input signal (dry) and the processed output (wet).

---
