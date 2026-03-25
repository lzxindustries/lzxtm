---
draft: true
sidebar_position: 239
slug: /instruments/videomancer/radiant
title: "Radiant"
image: /img/instruments/videomancer/radiant/radiant_hero_s1.png
description: "Radiant generates concentric colored rings that radiate outward from an adjustable center point, creating a tunnel-like wash of color that composites with the incoming video signal."
---

![Radiant hero image](/img/instruments/videomancer/radiant/radiant_hero_s1.png)
*Radiant projecting concentric rainbow rings outward from a drifting center point, tinting and illuminating a live video feed with animated spectral color.*

---

## Overview

Radiant is a concentric color ring generator inspired by the legendary Fairlight CVI's Colour Tunnel effect. It paints expanding rings of rainbow color onto the screen, radiating outward from a movable center point. The rings scroll continuously, creating the illusion of an endless tunnel of light rushing toward or away from you. Each ring carries its own hue from a smoothly cycling color palette, and the whole pattern composites over your input video: adding luminous color, or gating brightness through the ring structure.

The center of the ring pattern is adjustable with two knobs, and an optional orbit mode sends the center drifting through a quasi-Lissajous path, weaving the rings across the frame in a hypnotic dance. A separate auto-hue mode slowly rotates the color palette over time, so the rings shift through the entire spectrum without touching a single control.

At subtle settings, Radiant adds a soft color vignette or gentle tinting. At full strength, it transforms any input into a psychedelic tunnel of pulsing, scrolling rainbow light.

### What's In a Name?

***Radiant*** describes both the visual effect and the geometry. The rings ***radiate*** outward from a central point, like light emanating from a source. The word also evokes warmth and brilliance: fitting for a program that bathes video in luminous, saturated color. In optics, a ***radiant point*** is the apparent origin from which light appears to spread, which is exactly what the adjustable center parameter defines.

---

## Quick Start

1. Turn **Speed** (Knob 1) to about 25%. Concentric rings begin scrolling outward from the center of the frame, painting rainbow bands over your input.
2. Increase **Saturation** (Knob 3) clockwise. The rings become more vivid and colorful, shifting from pale tints to full spectral saturation.
3. Sweep **Hue** (Knob 2) slowly. The entire color palette rotates: greens become blues, reds become yellows: cycling through the full spectrum as you turn.
4. Enable **Orbit** (Switch 7). The center of the ring pattern begins drifting in a looping path, sweeping the rings across the frame automatically.

---

## Parameters

![Videomancer front panel with Radiant loaded](/img/instruments/videomancer/radiant/radiant_control_panel.png)
*Videomancer's front panel with Radiant active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Speed** controls how fast the rings scroll outward from the center. At 0%, the rings are frozen in place: a static pattern of concentric color bands. As you increase Speed, the rings begin to expand, creating the illusion of a tunnel rushing toward you. Higher values produce faster scrolling. Speed also controls the rate of the center orbit animation when **Orbit** is enabled: faster expansion means faster orbital drift.

:::tip
Even at very low Speed values, the ring pattern is always present. Set Speed to 0% and use **Hue** and **Center X/Y** manually to position a static color target or vignette over your video.
:::

---

### Knob 2 — Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Hue** rotates the base color of the ring palette. At 0°, the palette begins at its default starting color. Sweeping Hue through 360° cycles through the entire spectrum. Because the rings already cycle through hue as a function of distance, this control shifts *where* in the spectrum the cycle begins: think of it as rotating a color wheel that the rings are painted from.

---

### Knob 3 — Saturaton

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Saturation** controls the color intensity of the rings. At low values, the rings carry very little chrominance: they appear as near-neutral brightness variations. As Saturation increases, the U and V color components depart further from the neutral axis, and the rings become vividly colored. At maximum, the rings carry the strongest chroma the 10-bit signal allows.

The saturation control works by scaling the distance of the U and V values from the midpoint (512) using a power-of-two shift. This produces four discrete saturation levels internally, but the visual transition between them is smooth because the ring index itself varies continuously across the screen.

---

### Knob 4 — Value

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Value** sets the brightness of the ring pattern. In additive mode, this determines how much luminance the rings add to the input video: low Value produces dim, subtle rings; high Value produces bright, overdriven rings that can wash out the input. In multiply mode, Value controls the depth of the brightness gating: low Value allows the ring pattern to suppress the input almost to black, while high Value lets more of the input through.

---

### Knob 5 — Center X

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Center X** positions the horizontal origin of the ring pattern. At 50%, the center is in the middle of the frame. Turning counterclockwise shifts the center leftward; turning clockwise shifts it rightward. When **Orbit** is enabled, Center X sets the resting position around which the orbital animation oscillates.

---

### Knob 6 — Center Y

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Center Y** positions the vertical origin of the ring pattern. At 50%, the center is in the middle of the frame. Turning counterclockwise shifts the center upward; turning clockwise shifts it downward. Like **Center X**, this sets the resting position for the orbit animation.

:::note
The orbit animation adds a triangular-wave offset to both Center X and Center Y. The X and Y oscillators run at slightly different speeds, creating a quasi-***Lissajous*** figure that never quite repeats the same path.
:::

---

### Switch 7 — Orbit

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Orbit** enables the automatic center animation. When set to **Off**, the ring center stays wherever **Center X** and **Center Y** place it. When set to **On**, the center drifts in a looping triangular-wave path. The orbit speed is tied to the **Speed** parameter: faster ring expansion means faster orbital motion. Even at very low Speed values, a small constant offset keeps the orbit creeping slowly.

---

### Switch 8 — Auto Hue

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Auto Hue** enables automatic palette rotation. When set to **Off**, the ring colors depend only on the **Hue** knob and the distance from center. When set to **On**, the base hue increments by a small amount each frame, causing the entire ring palette to slowly drift through the spectrum. The rotation is slow and steady: it takes many seconds to complete a full cycle. Auto Hue combines additively with the manual **Hue** knob, so you can set a starting point and let the palette wander from there.

---

### Switch 9 — Multiply

| Property | Value |
|----------|-------|
| Off | Add |
| On | Mult |
| Default | Add |

**Multiply** selects the compositing method. When set to **Add**, the ring color is added to the input video: ring brightness is summed with input brightness, and ring chroma is summed with input chroma, with clamping at the signal limits. When set to **Mult**, the ring pattern gates the input video: ring brightness controls how much of the input signal passes through (darker ring regions suppress the input toward black), and ring chroma tints the input via averaging.

:::tip
***Multiply mode is the vignette tool.*** Position the center over your subject, lower the Value, and the ring pattern creates a natural spotlight-to-shadow falloff. The octagonal distance metric gives the vignette a subtly faceted, gem-like shape rather than a perfect circle.
:::

---

### Switch 10 — Wide Ring

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Wide Ring** doubles the width of each color ring. When set to **Off**, the ring index is derived directly from the full-precision radial distance, producing narrow, tightly packed rings. When set to **On**, the distance value is halved before the ring index is computed, effectively stretching each ring to twice its normal width. Wide rings are easier to see at a distance and produce a bolder, more graphic look.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input directly to the output, skipping all ring generation and compositing. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry input and the wet (ring-composited) output. At 0%, the output is entirely dry: no ring effect is visible. At 100%, the output is fully wet: the complete ring composite is active. Intermediate values blend the two proportionally, allowing you to dial in a subtle ring tint or overlay without committing to the full effect.

---

## Background

### Color Tunnels and the Fairlight CVI

The Fairlight CVI (Computer Video Instrument), released in 1984, was one of the earliest real-time digital video effects processors. Among its many effects was the ***Colour Tunnel***: a concentric ring pattern that could be overlaid on live video to create the illusion of flying through a tube of colored light. The effect became iconic in 1980s music videos and broadcast television, lending a distinctly futuristic, electronic aesthetic to everything it touched.

Radiant is a direct homage to this effect. It uses the same fundamental technique: computing a radial distance from a center point and mapping it through a scrolling color palette: but takes advantage of modern FPGA resources to add adjustable parameters, automatic animation, and flexible compositing options that the original hardware couldn't offer.

### Octagonal Distance

True circular distance requires a square root, which is expensive in hardware. Radiant uses an ***octagonal approximation***: a well-known technique in digital signal processing where the distance is estimated as:

$$d \approx \max(|dx|, |dy|) + \frac{3}{8} \cdot \min(|dx|, |dy|)$$

This produces iso-distance contours that are octagonal rather than circular, which is how the rings get their characteristic subtly faceted shape. The approximation is accurate to within a few percent of the true Euclidean distance and costs only a handful of additions and shifts (no multiplier or square root required.)

### Hue-to-UV Mapping

The ring color is generated by treating the ***ring index*** (a combination of distance, scroll position, and hue offset) as a hue value and converting it to YUV color space. The U and V components are derived by offsetting the ring index by 90 degrees (a quarter of the 10-bit range, or 256 counts), creating a quadrature pair. Saturation is applied by shifting U and V toward or away from the neutral midpoint (512). This is a simplified, hardware-efficient form of ***HSV-to-YUV*** conversion that produces a smooth, continuous color cycle without requiring lookup tables or trigonometric functions.


---

## Signal Flow

### Signal Flow Notes

The pipeline is eight clocks deep: four processing stages followed by a four-clock interpolator for wet/dry crossfading. The input video passes through a matching eight-stage delay line so that the dry signal arrives at the interpolator at the same time as the wet signal.

Three independent ***direct digital synthesis*** (DDS) accumulators drive the animation. The frame scroll DDS controls ring expansion speed, accumulating once per vertical sync. The orbit DDS controls center position, also accumulating per vsync with slightly different X and Y rates to produce the Lissajous-like drift. The hue auto-rotation DDS increments by a small fixed value per frame when Auto Hue is enabled, providing the slow palette rotation. Because all three accumulators update only on vsync, the ring pattern is rock-stable within each frame.

:::note
The orbit DDS uses triangular waves (formed by conditionally complementing the upper bits of the accumulator) rather than sinusoidal waves. This gives the orbit an angular, bouncing character instead of smooth curves. The X and Y oscillators have slightly different base frequencies (offsets of 32 and 48, respectively), so the path forms an open Lissajous-like figure that never perfectly repeats.
:::


---

## Exercises

These exercises progress from a static color target to a fully animated, orbiting rainbow tunnel. Each one layers additional controls to explore more of Radiant's capabilities.
### Exercise 1: Color Vignette

![Color Vignette result](/img/instruments/videomancer/radiant/radiant_ex1_s1.png)
*Color Vignette — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A colored spotlight vignette that highlights the center of the frame and dims the edges: a classic broadcast framing technique, reimagined with Radiant's faceted geometry.

#### Key Concepts

- Radial distance creates concentric rings from a center point
- Multiply mode gates input brightness with ring pattern
- Center X and Center Y position the ring origin

#### Video Source

A live camera feed or recorded footage with a subject centered in the frame.

#### Steps

1. Set **Speed** (Knob 1) to a low value, around 10%. Slow-moving rings should be visible.
2. Switch **Multiply** (Switch 9) to **Mult**. The ring pattern now gates the input rather than adding to it (edges of the frame darken.)
3. Enable **Wide Ring** (Switch 10). The rings spread out, creating a broader, smoother vignette rather than tightly packed bands.
4. Lower **Value** (Knob 4) to about 75%. The gating becomes gentler, letting more of the input show through.
5. Set **Hue** (Knob 2) to about 60°. A warm tint colors the ring structure. Adjust **Saturation** (Knob 3) to control how strongly the color tints the image.
6. Use **Center X** (Knob 5) and **Center Y** (Knob 6) to reposition the bright center over your subject.
7. Pull back **Mix** (Fader 12) to about 85% to blend the vignette gently with the original.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 10% |
| Hue | 60° |
| Saturation | 50% |
| Value | 75% |
| Center X | 50% |
| Center Y | 50% |
| Orbit | Off |
| Auto Hue | Off |
| Multiply | Mult |
| Wide Ring | On |
| Bypass | Off |
| Mix | 85% |

---

### Exercise 2: Rainbow Tunnel

![Rainbow Tunnel result](/img/instruments/videomancer/radiant/radiant_ex2_s1.png)
*Rainbow Tunnel — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic color tunnel effect: concentric rainbow rings expanding outward from a central vanishing point, composited additively over the input.

#### Key Concepts

- Ring index maps distance to hue, creating a rainbow cycle
- Speed controls expansion rate
- Auto Hue rotates the palette over time

#### Video Source

Dark or low-contrast footage works best: the additive rings will be most visible against darker backgrounds.

#### Steps

1. Set **Speed** (Knob 1) to about 25%. Rings expand steadily outward.
2. Increase **Saturation** (Knob 3) to about 75%. The rings become vividly colored.
3. Set **Value** (Knob 4) to about 75%. The rings are bright but not overwhelming.
4. Make sure **Multiply** (Switch 9) is set to **Add**. The rings add color and brightness to the input.
5. Sweep **Hue** (Knob 2) slowly through 360° to see the palette rotate. Park it wherever the color combination looks best.
6. Enable **Auto Hue** (Switch 8). The palette begins rotating on its own (watch the colors slowly shift through the spectrum.)
7. Toggle **Wide Ring** (Switch 10) on and off to compare narrow and wide ring spacing.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 25% |
| Hue | 0° |
| Saturation | 75% |
| Value | 75% |
| Center X | 50% |
| Center Y | 50% |
| Orbit | Off |
| Auto Hue | On |
| Multiply | Add |
| Wide Ring | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Orbiting Spectrum

![Orbiting Spectrum result](/img/instruments/videomancer/radiant/radiant_ex3_s1.png)
*Orbiting Spectrum — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A fully animated, self-running color tunnel with the center drifting across the frame, painting sweeping arcs of rainbow light over the input.

#### Key Concepts

- Orbit mode animates the center in a quasi-Lissajous triangular path
- Speed controls both ring expansion and orbit rate simultaneously
- Combining orbit with auto-hue produces a fully self-animating effect

#### Video Source

Any video feed: abstract material, camera footage, or even a static image. The orbit animation provides all the motion.

#### Steps

1. Start from the Exercise 2 settings: Speed 25%, Saturation 75%, Value 75%, Add mode.
2. Enable **Orbit** (Switch 7). The ring center begins tracing a looping path across the frame.
3. Increase **Speed** (Knob 1) to about 40%. Both the ring expansion and the orbital motion accelerate.
4. Enable **Auto Hue** (Switch 8) if not already on. The palette rotates continuously.
5. Offset the center: set **Center X** (Knob 5) to about 30% and **Center Y** (Knob 6) to about 60%. The orbit now sweeps around an off-center origin, creating asymmetric patterns.
6. Enable **Wide Ring** (Switch 10) for a bolder, more graphic look.
7. Lower **Mix** (Fader 12) to about 85%. The ring pattern blends with the input rather than dominating it (the orbiting rings become a dynamic color overlay.)

#### Settings

| Control | Value |
|---------|-------|
| Speed | 40% |
| Hue | 180° |
| Saturation | 100% |
| Value | 60% |
| Center X | 30% |
| Center Y | 60% |
| Orbit | On |
| Auto Hue | On |
| Multiply | Add |
| Wide Ring | On |
| Bypass | Off |
| Mix | 85% |

---
## Glossary

- **Additive Composite**: A blending method where the ring signal's brightness and color values are summed with the input, producing brighter results.

- **DDS (Direct Digital Synthesis)**: A technique for generating waveforms by incrementing an accumulator once per update cycle; used here to animate ring expansion, orbit, and hue rotation.

- **Hue**: The attribute of color that distinguishes red from blue from green (the position on the color wheel.)

- **Lissajous Figure**: A geometric curve formed by combining two oscillations at different frequencies; Radiant's orbit mode approximates this with triangular waves.

- **Multiply Composite**: A blending method where the ring signal gates the input brightness, darkening areas where the ring value is low.

- **Octagonal Distance**: A hardware-efficient approximation of Euclidean distance that produces octagonal iso-distance contours instead of perfect circles.

- **Radial Distance**: The distance from a pixel to the center point, used to determine which ring a pixel belongs to.

- **Ring Index**: A computed value combining radial distance, frame scroll, and hue offset that maps each pixel to a position in the color palette.

- **Saturation**: The intensity or purity of a color; low saturation approaches neutral gray, high saturation approaches vivid, pure color.

- **Triangular Wave**: A waveform that rises and falls linearly, forming a zigzag shape; used for the orbit animation to create angular, bouncing motion.

- **YUV**: A color model separating brightness (Y) from color difference signals (U, V); the native format of the Videomancer video pipeline.

---
