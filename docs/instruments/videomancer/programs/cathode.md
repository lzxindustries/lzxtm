---
draft: true
sidebar_position: 40
slug: /instruments/videomancer/cathode
title: "Cathode"
image: /img/instruments/videomancer/cathode/cathode_hero_s1.png
description: "Lightning is nature's most dramatic display of electrical energy — a branching, jagged path of ionized air that exists for less than a millisecond but burns into visual memory."
---

![Cathode hero image](/img/instruments/videomancer/cathode/cathode_hero_s1.png)
*Cathode generating forked lightning bolts with Gaussian glow over live video, additively composited in Electric Blue palette.*

---

## Overview

Cathode is a procedural lightning bolt and electrical discharge generator. It draws jagged bolt paths across the screen using a random walk algorithm, surrounds them with a soft Gaussian glow, and composites the result additively over your input video. The effect ranges from subtle static sparks to dramatic, screen-spanning electrical arcs that flash, hold, and fade on their own schedule.

The bolt path is generated fresh during each vertical blanking interval, written into a dedicated block of FPGA memory. During active video, every pixel on every scanline measures its distance from the bolt center and looks up a glow intensity from a precomputed curve. The result is a smooth, organic-looking discharge that follows a truly random path: no two bolts are ever the same. Four color palettes tint the glow from electric blue to purple, warm white, or green.

Cathode draws its creative inspiration from the NewTek Video Toaster's Forked Lightning and Jagged Lightning effects, reimagined for modern hardware with per-pixel glow, palette-tinted chroma, and real-time parameter control.

### What's In a Name?

The name ***Cathode*** refers to the ***cathode ray***: the beam of electrons fired from the back of a CRT television tube toward the phosphor screen. Lightning is nature's cathode ray: a massive electrical discharge arcing through the atmosphere. The name also evokes the warm, glowing aesthetic of ***cathode ray tubes*** themselves, connecting the digital lightning effect to video's analog past.

---

## Quick Start

1. Set **Brightness** (Knob 6) to about 75%. A jagged bolt of light should appear superimposed over your input video, glowing in electric blue.
2. Turn **Roughness** (Knob 1) clockwise. The bolt becomes more jagged and erratic, zig-zagging wildly across the screen.
3. Increase **Fork** (Knob 2). Occasional sharp kinks appear along the bolt path (sudden directional changes that visually suggest branching.)
4. Flip **Animate** (Switch 9) to **On** and adjust **Flash Rate** (Knob 4). The bolt now regenerates periodically, flashing bright and then fading away before a new bolt strikes.

---

## Parameters

![Videomancer front panel with Cathode loaded](/img/instruments/videomancer/cathode/cathode_control_panel.png)
*Videomancer's front panel with Cathode active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Roughness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Roughness** controls how jagged the bolt path is. At 0%, fully counterclockwise, the bolt is nearly a straight vertical line. As Roughness increases, each step of the random walk displaces further from the previous position, creating increasingly wild zig-zag patterns. At 100%, the bolt careens across the full width of the screen with dramatic, angular deviations.

The roughness value scales the magnitude of a random displacement applied at each of the 128 path segments. Internally, an 8-bit signed random number from the ***LFSR*** is multiplied by the roughness scale factor, so low roughness keeps the bolt close to the target position while high roughness lets it wander freely.

---

### Knob 2 — Fork

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Fork** controls the probability of sudden, extra-large kinks in the bolt path. At 0%, the bolt follows a smooth random walk with uniform displacement. As Fork increases, the chance of a displacement being doubled at any given segment rises, creating sharp angular breaks that visually suggest branching or forking. At 100%, nearly every segment has an exaggerated kink, making the bolt extremely chaotic.

:::tip
**Fork** and **Roughness** are complementary. Roughness sets the baseline jaggedness, while Fork adds punctuated bursts of extra displacement on top. For realistic lightning, try moderate Roughness (~40%) with low Fork (~20%).
:::

---

### Knob 3 — Glow Width

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |

**Glow Width** controls the radius of the Gaussian glow surrounding the bolt center. At 0%, the glow is very tight and narrow: the bolt appears as a thin, sharp line. As Glow Width increases, the glow spreads further from the bolt center, creating a soft, diffuse halo. At 100%, the glow is wide enough to illuminate a large portion of the screen around the bolt.

The glow profile is stored as a 64-entry lookup table containing a precomputed Gaussian curve. Glow Width controls how many pixels of horizontal distance map across those 64 entries: narrow settings compress the entire curve into a few pixels, while wide settings stretch it across many.

---

### Knob 4 — Flash Rate

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |

**Flash Rate** controls how quickly new bolts are generated when **Animate** (Switch 9) is enabled. At 0%, bolts regenerate very slowly: the discharge lingers and fades for a long time before a new strike appears. At 100%, bolts regenerate rapidly, creating a near-continuous flickering barrage.

After each new bolt is generated, it holds at full brightness for three frames, then fades exponentially: each frame, the intensity is halved. The Flash Rate timer determines how many frames pass before the next bolt replaces the fading one.

:::note
When **Animate** is set to **Off**, Flash Rate has no visible effect. The bolt regenerates every frame with no fade, so it updates continuously in response to parameter changes.
:::

---

### Knob 5 — Target X

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Target X** controls the horizontal starting position of the bolt. At 0%, the bolt originates at the left edge of the screen. At 50%, the bolt starts at the center. At 100%, the bolt originates at the right edge. The first segment of the bolt path is always placed exactly at the Target X position; subsequent segments wander away from it according to Roughness and Fork.

:::tip
Sweep **Target X** slowly during a performance to animate the bolt's strike point across the screen. Combine with low **Roughness** for a controlled beam, or high **Roughness** for a bolt that wanders far from the starting position.
:::

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Brightness** controls the overall intensity of the bolt and its glow. At 0%, the bolt is invisible: its glow is scaled to zero. At 100%, the bolt is at maximum intensity, easily saturating the luma channel where it overlaps the glow center. The brightness value is multiplied against the glow profile after the Gaussian lookup, before compositing.

Because the bolt is composited ***additively***: its brightness is added to the existing video: the result is always lighter than the input. Dark input areas show the bolt clearly, while bright input areas may clip to white where the bolt overlaps.

---

### Switch 7 — Palette A

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Palette A** is the low bit of the two-bit color palette selector. Together with **Palette B** (Switch 8), it selects one of four color tints applied to the bolt's glow. See the Toggle Group Notes below for the full palette table.

---

### Switch 8 — Palette B

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Palette B** is the high bit of the two-bit color palette selector. Together with **Palette A** (Switch 7), it selects one of four color tints. See the Toggle Group Notes below for the full palette table.

---

### Switch 9 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** enables automatic bolt regeneration and fade behavior. When set to **On**, bolts are generated periodically according to **Flash Rate** (Knob 4), hold at full brightness for three frames, and then fade exponentially. When set to **Off**, the bolt is regenerated every single frame with no fade, creating a continuously-updating bolt that responds instantly to parameter changes. Static mode is useful for dialing in Roughness, Fork, and Glow Width without the bolt disappearing between flashes.

---

### Switch 10 — Direction

| Property | Value |
|----------|-------|
| Off | Down |
| On | Up |
| Default | Down |

**Direction** controls the orientation of the bolt. When set to **Down**, the bolt begins at the top of the screen and extends downward: the first BRAM entry corresponds to the top scanline. When set to **Up**, the address mapping is reversed: the bolt begins at the bottom and extends upward. The bolt path data itself does not change; only the read order is flipped.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the input video directly to the output, bypassing all Cathode processing. The sync delay pipeline still aligns timing so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the composited result.

---

:::note Toggle Group Notes

**Palette A** (Switch 7) and **Palette B** (Switch 8) combine to form a two-bit palette selector. The four palettes tint the bolt's glow by shifting the U and V chroma channels proportionally to the glow intensity:

| Palette A | Palette B | Color | Chroma Behavior |
|-----------|-----------|-------|-----------------|
| Off | Off | Electric Blue | U shifts positive, V shifts negative |
| On | Off | Purple | U shifts slightly positive, V shifts positive |
| Off | On | Warm White | U shifts slightly negative, V shifts slightly positive |
| On | On | Green | U shifts negative, V shifts slightly negative |

The chroma shift is proportional to the glow value: brighter regions of the bolt receive more tint, while areas far from the bolt center remain unchanged. This creates a natural falloff where the color tint fades with the glow.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Mix** controls the wet/dry balance between the original input video and the bolt-composited result. At 0%, fully down, the output is the unprocessed input: no bolt is visible. At 100%, fully up, the output is the fully composited result with the bolt and glow at the intensity set by **Brightness**. Intermediate values crossfade smoothly between the two.

:::tip
Use **Mix** at moderate values (40–60%) to create a subtle, ghostly lightning overlay that doesn't overpower the source material. At 100%, the bolt dominates the image, which is ideal for standalone synthesis effects.
:::

---

## Background

### Midpoint displacement and random walks

Cathode generates bolt paths using a ***random walk***: a mathematical process where each step moves in a random direction from the previous position. The bolt starts at the **Target X** coordinate and walks downward (or upward) through 128 path segments, accumulating random displacements at each step. The result is a jagged, naturalistic path that mimics the fractal structure of real electrical discharges.

This technique is closely related to ***midpoint displacement***, the algorithm used in early computer graphics to generate lightning, mountains, and coastlines. The principle is the same: start with two endpoints, displace the midpoint by a random amount, then recursively subdivide. Cathode's random walk is a one-pass version: it walks from top to bottom in a single sweep, displacing each segment once.

Real lightning follows a similar process. The electrical leader propagates step by step from cloud to ground, each segment finding the path of least resistance through the atmosphere. The resulting path has a ***fractal*** quality: it looks similar at every scale, with smaller branches mirroring the shape of the main channel.

### Gaussian glow profiles

The glow surrounding the bolt uses a ***Gaussian function***: the familiar bell curve from statistics. The Gaussian's smooth, symmetric falloff creates a natural-looking radiance that peaks at the bolt center and tapers to zero. This is stored as a 64-entry lookup table precomputed from the formula $\text{glow}(i) = 1023 \cdot e^{-(i/16)^2}$.

The Gaussian profile produces a softer, more realistic glow than a simple linear ramp. The center of the bolt appears bright and well-defined, while the edges dissolve gradually into the surrounding image. The **Glow Width** control stretches or compresses the distance-to-index mapping, effectively widening or narrowing the bell curve without changing its shape.

### Additive compositing

Cathode layers the bolt over the input video using ***additive compositing***: the bolt's brightness is added to the existing pixel values. This is the same blending mode used for lens flares, light beams, and particle effects in film and game engines. Additive compositing never darkens: it can only make pixels brighter or leave them unchanged.

For the luma channel, the addition is saturating: values that would exceed the maximum (1023) are clamped to white. For the chroma channels, the palette tint is added with clamping to the valid range, ensuring no wraparound artifacts.

:::note
Because of additive compositing, the bolt is most visible over dark areas of the input. Over bright input, the bolt may be invisible because luma is already near maximum. Feed Cathode dark or moderately-lit footage for the most dramatic results.
:::

### Flash-hold-fade timing

When **Animate** is enabled, each bolt follows a three-phase lifecycle: ***flash***, ***hold***, and ***fade***. The flash phase generates a new bolt path and displays it at full brightness. The hold phase maintains full brightness for three frames, giving the eye time to register the bolt. The fade phase applies ***exponential decay***: each frame, the intensity is halved by shifting the fade register right by one bit. This produces a rapid initial dimming that gradually slows, mimicking the afterglow of a real electrical discharge.

The **Flash Rate** control sets the interval between flash events. At high rates, bolts overlap their fade tails, creating a continuous flickering storm. At low rates, each bolt fades nearly to black before the next one arrives, producing isolated, dramatic strikes.


---

## Signal Flow

### Signal Flow Notes

The bolt path and the video pipeline operate in two distinct phases. During ***vertical blanking***, the bolt generator runs its random walk state machine, writing 128 X-position entries into BRAM. During ***active video***, the pipeline reads from that same BRAM: one entry per band of eight scanlines: and computes per-pixel distance from the bolt center.

The key signal path for the glow is: distance → Gaussian LUT → brightness multiply → fade multiply → palette color shift → additive composite → Mix interpolator. Each multiply is a 10×10-bit product truncated to 10 bits, preserving the full dynamic range of the glow curve. The **Direction** toggle simply reverses the BRAM read address, flipping the bolt vertically without regenerating it.

:::tip
Because the bolt path is stored in BRAM and only regenerated during vblank, parameter changes to **Roughness**, **Fork**, and **Target X** take effect on the *next* bolt generation: not instantly. In static mode (Animate Off), this happens every frame. In animated mode, it happens at the next flash event.
:::


---

## Exercises

These exercises progress from a basic static bolt to animated lightning storms composited over live video. Each exercise explores a different facet of Cathode's controls.
### Exercise 1: Your First Lightning Bolt

![Your First Lightning Bolt result](/img/instruments/videomancer/cathode/cathode_ex1_s1.png)
*Your First Lightning Bolt — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A single, well-defined static bolt positioned over your source video. You'll learn how Roughness and Glow Width shape the bolt's character.

#### Key Concepts

- Random walk bolt generation
- Roughness and glow width interaction
- Target X positioning

#### Video Source

A dark or moderately-lit source: live camera in a dimly lit room, or footage of a night sky or dark landscape. Dark scenes show the additive bolt most clearly.

#### Steps

1. Turn **Animate** (Switch 9) to **Off** so the bolt regenerates every frame and responds instantly to changes.
2. Set **Brightness** (Knob 6) to about 75%. A bolt of light should appear over your input.
3. Turn **Roughness** (Knob 1) slowly from 0% to 100%. Watch the bolt evolve from a nearly straight line to a wild zig-zag.
4. Set Roughness to about 50%. Now sweep **Glow Width** (Knob 3) from low to high. The bolt transforms from a razor-thin line to a broad, diffuse wash of light.
5. Sweep **Target X** (Knob 5) left and right. The bolt's origin slides across the screen.

#### Settings

| Control | Value |
|---------|-------|
| Roughness | ~50% |
| Fork | 0% |
| Glow Width | ~40% |
| Flash Rate | ~30% |
| Target X | ~50% |
| Brightness | ~75% |
| Palette A | Off |
| Palette B | Off |
| Animate | Off |
| Direction | Down |
| Bypass | Off |
| Mix | ~75% |

---

### Exercise 2: Animated Lightning Storm

![Animated Lightning Storm result](/img/instruments/videomancer/cathode/cathode_ex2_s1.png)
*Animated Lightning Storm — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A repeating lightning storm with forked bolts that flash, hold, and fade over time.

#### Key Concepts

- Flash-hold-fade lifecycle
- Fork creates visual branching
- Direction reversal

#### Video Source

Footage of clouds, a dark cityscape, or any dramatic scene. Cloud footage works especially well (the bolts appear to strike from the clouds.)

#### Steps

1. Flip **Animate** (Switch 9) to **On**. The bolt now flashes periodically instead of regenerating every frame.
2. Set **Flash Rate** (Knob 4) to about 40%. Bolts should appear every second or so, flash bright, then fade away.
3. Increase **Fork** (Knob 2) to about 30%. Occasional sharp kinks appear along the bolt path, suggesting branching.
4. Set **Roughness** (Knob 1) to about 40% for a naturalistic bolt shape.
5. Toggle **Direction** (Switch 10) to **Up**. The bolt now originates at the bottom and extends upward (ground-to-cloud lightning.)
6. Set **Mix** (Fader 12) to 100% for full intensity.

#### Settings

| Control | Value |
|---------|-------|
| Roughness | ~40% |
| Fork | ~30% |
| Glow Width | ~40% |
| Flash Rate | ~40% |
| Target X | ~50% |
| Brightness | ~75% |
| Palette A | Off |
| Palette B | Off |
| Animate | On |
| Direction | Up |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Color Palette Exploration

![Color Palette Exploration result](/img/instruments/videomancer/cathode/cathode_ex3_s1.png)
*Color Palette Exploration — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Explore all four color palettes and see how each interacts with your source video's existing colors.

#### Key Concepts

- Four color palettes tint the bolt via chroma shifts
- Additive compositing interacts with source color
- Mix blending creates layered effects

#### Video Source

Colorful footage with a mix of warm and cool tones: a garden, a city at sunset, or abstract color patterns from another Videomancer program.

#### Steps

1. Set **Roughness** to about 40%, **Fork** to about 25%, **Glow Width** to about 50%, and **Brightness** to about 75%.
2. Start with both **Palette A** (Switch 7) and **Palette B** (Switch 8) set to **Off**. This is Electric Blue (the default. Observe the cool blue tint in the bolt's glow.)
3. Flip **Palette A** to **On** (leaving Palette B Off). The bolt shifts to Purple (warmer and more saturated.)
4. Flip **Palette A** back to **Off** and set **Palette B** to **On**. The bolt becomes Warm White (a nearly neutral glow with a subtle warm cast.)
5. Set both **Palette A** and **Palette B** to **On**. The bolt turns Green (an eerie, unnatural discharge.)
6. With each palette, sweep **Mix** (Fader 12) from 0% to 100% to see how the tint blends with the source colors at different intensities.

#### Settings

| Control | Value |
|---------|-------|
| Roughness | ~40% |
| Fork | ~25% |
| Glow Width | ~50% |
| Flash Rate | ~30% |
| Target X | ~50% |
| Brightness | ~75% |
| Palette A | On |
| Palette B | On |
| Animate | On |
| Direction | Down |
| Bypass | Off |
| Mix | ~75% |

---
## Glossary

- **Additive Compositing**: A blending method where the effect's brightness is added to the underlying image, always making pixels brighter or leaving them unchanged.

- **BRAM**: Block RAM; a dedicated memory resource on the FPGA used here to store the 128-entry bolt path between vertical blanking and active video.

- **Exponential Decay**: A fade pattern where intensity is halved each frame, producing rapid initial dimming that slows over time.

- **Fractal**: A geometric pattern that exhibits self-similarity at different scales; lightning bolts have fractal structure.

- **Gaussian Function**: A bell-curve function used to compute the glow profile; it produces a smooth, symmetric falloff from bright center to dark edges.

- **Glow Profile**: The brightness curve surrounding the bolt center, described by a Gaussian lookup table.

- **LFSR**: Linear Feedback Shift Register; a hardware-efficient pseudorandom number generator that produces the random displacements for the bolt path.

- **Midpoint Displacement**: A fractal algorithm that generates naturalistic forms by randomly displacing midpoints between endpoints; the conceptual basis for the bolt's random walk.

- **Random Walk**: A mathematical process where each step moves in a random direction from the previous position, used here to generate the bolt path.

- **Saturating Addition**: An addition operation that clamps the result to the maximum representable value instead of wrapping around.

- **Vertical Blanking**: The interval between video frames when no active picture data is transmitted; the bolt generator runs during this period.

---
