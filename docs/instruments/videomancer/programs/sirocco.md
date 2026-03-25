---
draft: true
sidebar_position: 272
slug: /instruments/videomancer/sirocco
title: "Sirocco"
image: /img/instruments/videomancer/sirocco/sirocco_hero_s1.png
description: "A sirocco is a hot, sand-laden wind that blows across the Mediterranean from the Sahara."
---

![Sirocco hero image](/img/instruments/videomancer/sirocco/sirocco_hero_s1.png)
*A scorching wind sweeps across the frame, warping brightness into shimmering ripples and scattering bright sand particles through a warm, haze-tinted atmosphere.*

---

## Overview

Sirocco transforms video into a desert mirage. It layers four atmospheric effects on top of the source image: a per-scanline brightness ripple that simulates heat shimmer, a sparse sand particle overlay that scatters bright specks across the frame, a warm color temperature shift that pushes the palette toward sepia and amber, and a contrast boost that intensifies the tonal range. Each effect is independently switchable, and the six knobs provide continuous control over amplitude, speed, density, brightness, warmth, and crossfade balance.

The heart of Sirocco is the brightness ripple: a sine wave that rolls vertically through the image, raising and lowering pixel brightness line by line. At low amplitudes it produces a gentle atmospheric wobble; at high values it creates dramatic stripes of light and shadow that scroll down the screen. The animation is driven by a phase accumulator that advances once per frame, so the ripple slides through the picture at a tempo set by the **Turbulen** knob.

:::tip
Sirocco is a ***processing*** program. It modifies an existing video signal rather than generating its own imagery. Feed it a camera, a pattern generator, or another program's output to see the desert weather come to life.
:::

### What's In a Name?

A ***sirocco*** is a hot, dry wind that blows northward from the Sahara Desert across the Mediterranean. It carries fine sand and dust thousands of miles, turning skies hazy and raising temperatures sharply. In southern Europe, a sirocco can coat entire cities in a layer of orange dust. The program evokes that phenomenon: heat shimmer distorts the image, sand particles scatter across it, and a warm color shift tints everything in amber.

---

## Quick Start

1. Enable the shimmer effect by flipping the **Shimmer** toggle (Switch 8) to **On**. Turn **Intensity** (Knob 1) to about 50%. You'll see horizontal bands of brighter and darker pixels rippling down the screen (the heat shimmer.)
2. Turn **Turbulen** (Knob 2) slowly clockwise. The ripple bands begin scrolling faster, as though the air above hot asphalt is pulsing with convection currents.
3. Flip the **Storm** toggle (Switch 7) to **Fog** to enable the sand particle overlay. Turn **Haze Amt** (Knob 3) clockwise. Bright specks appear across the image, sparse at first, then increasingly dense as you increase the value (like sand blowing sideways through the frame.)
4. Flip the **Direction** toggle (Switch 9) to **Vert** and turn **Wind Dir** (Knob 5) clockwise. The image shifts toward warm amber and orange tones, as though the camera is filming through a dust-laden atmosphere at golden hour.

---

## Parameters

![Videomancer front panel with Sirocco loaded](/img/instruments/videomancer/sirocco/sirocco_control_panel.png)
*Videomancer's front panel with Sirocco active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Intensity

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Intensity** controls the amplitude of the per-scanline brightness ripple. At 0%, the ripple is silent: no brightness variation occurs. As you turn the knob clockwise, the sine wave grows taller: horizontal bands of brighter and darker pixels emerge, rolling vertically through the frame. The scaling follows four shift-based tiers, so the amplitude jumps in steps as you cross the quarter, half, and three-quarter marks. At 100%, the ripple can swing brightness by more than 120 levels in each direction, creating dramatic stripes of light and shadow.

:::note
**Intensity** has no visible effect unless the **Shimmer** toggle (Switch 8) is set to **On**.
:::

---

### Knob 2 — Turbulen

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Turbulen** sets the speed of the ripple animation. The upper bits of this value are added to a phase accumulator at every vertical sync pulse, so higher values produce faster scrolling of the brightness wave. At 0%, the ripple pattern is frozen in place. At moderate values, the bands drift slowly downward like heat currents. At 100%, the ripple races through the image at full speed, producing a flickering, turbulent shimmer.

---

### Knob 3 — Haze Amt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Haze Amt** controls the density of sand particles scattered across the image. Sand particles are sparse bright dots generated by comparing a per-pixel hash against a density threshold. At 0%, no particles appear. As you increase the value, more pixels pass the threshold and light up as bright specks. At 100%, particles become dense enough to form a visible grain across the entire frame.

:::note
Sand particles only appear when the **Storm** toggle (Switch 7) is set to **Fog**.
:::

---

### Knob 4 — Shimmer

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Shimmer** controls the brightness of individual sand particles. When a pixel is selected as a sand particle, half of this value is added to its luminance. At 0%, particles add no brightness and are invisible. At 100%, particles flare to maximum brightness, appearing as hot white specks against the image. Each sand particle also receives a small warm tint on the red-yellow axis, giving it a slightly amber appearance.

---

### Knob 5 — Wind Dir

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 90° |

**Wind Dir** controls the intensity of the atmospheric color temperature shift. Despite its compass-themed display, this parameter functions as a warmth control. When the color shift is active, higher values push the image further toward amber and orange tones by adding red-yellow bias and reducing blue. At 0°, no color shift occurs even if the **Direction** toggle is enabled. At 360°, the warm tint is at maximum strength, creating a deep sepia atmosphere.

:::tip
Combine a moderate **Wind Dir** value with high **Haze Amt** to simulate the golden-hour quality of a Saharan dust cloud: the image takes on a unified warm tone while bright particles drift through the frame.
:::

---

### Knob 6 — Warmth

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Warmth** is a reserved control in the current firmware. Adjusting this knob produces no visible change to the output. It is mapped internally but not connected to the processing pipeline.

---

### Switch 7 — Storm

| Property | Value |
|----------|-------|
| Off | Sand |
| On | Fog |
| Default | Sand |

**Storm** selects between two atmospheric modes. In the **Sand** position (default), the sand particle overlay is disabled: the atmosphere is clear, and only the ripple, color shift, and contrast effects are active. In the **Fog** position, Sirocco scatters bright particles across the image. The density and brightness of these particles are controlled by **Haze Amt** (Knob 3) and **Shimmer** (Knob 4).

---

### Switch 8 — Shimmer

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Shimmer** enables or disables the per-scanline brightness ripple. In the **Off** position (default), the ripple generator is inactive and the **Intensity** and **Turbulen** knobs have no effect. In the **On** position, the sine-wave ripple is applied to the luminance channel, producing the signature heat-shimmer distortion.

---

### Switch 9 — Direction

| Property | Value |
|----------|-------|
| Off | Horiz |
| On | Vert |
| Default | Horiz |

**Direction** enables or disables the atmospheric color temperature shift. In the **Horiz** position (default), no color modification occurs. In the **Vert** position, the warm color shift is applied, tinting the image according to the **Wind Dir** knob setting. The shift increases the red-yellow (V) component and decreases the blue (U) component.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** enables or disables a contrast boost that expands the tonal range around mid-gray. In the **On** position (default), pixel values above mid-gray are pushed brighter and values below are pushed darker by 25%, creating a subtle but visible increase in contrast: as though the desert sun is sharpening every shadow. In the **Off** position, the luminance passes through without contrast modification.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Sirocco processing stages. The sync delay pipeline still aligns timing so there is no glitch on transition. Use **Bypass** for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) and wet (processed) signals. At 0%, only the original input is heard: all Sirocco effects are silent. At 100%, the fully processed desert atmosphere replaces the source. Intermediate values blend the two, allowing you to dial in a subtle atmospheric tint without fully committing to the effect.

---

## Background

### Heat Shimmer and Atmospheric Refraction

When air near the ground is much hotter than the air above it, light passing through the boundary bends unpredictably. This is ***atmospheric refraction***, and its most familiar form is the shimmering mirage you see above hot asphalt or desert sand. Objects appear to wobble and ripple because the refraction varies from moment to moment and from place to place. Sirocco simulates this by applying a sine wave to pixel brightness, varying the wave's phase along the vertical axis so each scanline receives a slightly different brightness offset. The result is a vertical undulation of light and dark bands that approximates the visual experience of looking through heated air.

### Quarter-Wave Sine Lookup

Rather than computing a full sine function: which would require a multiplier or a large lookup table: Sirocco stores only one quarter of a sine period in an 8-entry table. A full wave is reconstructed by mirroring and negating the quarter-wave values. The table index is derived from the vertical line position plus a continuously advancing phase counter, so the wave pattern shifts downward over time. This technique uses no block RAM and no DSP resources, which is important on the resource-constrained iCE40 FPGA.

### Pseudorandom Sand Particles

Sand particles are generated by a hash function applied to each pixel's coordinates. The horizontal pixel count, a 16-bit ***linear feedback shift register*** (LFSR) output, and a scrambled version of the vertical count are XOR'd together to form a 12-bit hash. When the upper 8 bits of this hash fall below a threshold set by the **Haze Amt** knob, the pixel is tagged as a sand hit. Tagged pixels receive a brightness boost and a small warm color nudge. Because the LFSR runs freely and the hash mixes horizontal and vertical positions, the particle pattern appears random and evenly distributed.


---

## Signal Flow

### Signal Flow Notes

Three key interactions define Sirocco's processing chain:

1. **Ripple before contrast**: The brightness ripple is applied at Stage 3, before the contrast expansion at Stage 4. This means the contrast boost amplifies the ripple: bright ripple peaks are pushed brighter and dark troughs are pushed darker. The shimmer effect looks more dramatic with contrast enabled.

2. **Sand particles add warmth individually**: Each sand particle receives a small nudge toward warm chroma (V+8) in addition to its brightness boost. This tint is independent of the global color temperature shift. Even with the **Direction** toggle set to **Horiz** (color shift disabled), sand particles still carry a faint amber hue.

3. **Color shift is additive**: The warm color temperature at Stage 4 adds to any per-particle warmth from Stage 3. With both active, sand particles appear warmer than the surrounding image, standing out against the already-tinted background.

:::tip
**Processing order matters.** Ripple → Sand → Contrast → Warmth. Each stage transforms the signal before the next one sees it. Try enabling one stage at a time and watching how subsequent stages respond to the modified signal.
:::


---

## Exercises

These exercises build from a single atmospheric effect to a full desert sandstorm. Each one activates a new processing layer on top of the previous one.
### Exercise 1: Heat Shimmer

![Heat Shimmer result](/img/instruments/videomancer/sirocco/sirocco_ex1_s1.png)
*Heat Shimmer — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A gentle heat-shimmer effect that makes the image wobble as though viewed through hot air rising from pavement.

#### Key Concepts

- The brightness ripple is a sine wave applied per scanline
- Amplitude and speed are independent controls
- The phase accumulator creates smooth animation

#### Video Source

A live camera feed or recorded footage with strong horizontal features: rooftops, fences, or text: that make the ripple distortion easy to see.

#### Steps

1. Start clean: set all toggles to their default positions. Flip **Shimmer** (Switch 8) to **On**.
2. Turn **Intensity** (Knob 1) slowly clockwise to about 40%. Horizontal bands of lighter and darker pixels appear, rolling down the screen.
3. Increase **Turbulen** (Knob 2) from 0% to about 30%. The bands begin scrolling (slow at first, then faster as you turn.)
4. Sweep **Intensity** from low to high and notice the four scaling tiers. The amplitude jumps at roughly 25%, 50%, and 75%.
5. Use the **Mix** fader (Fader 12) to blend the shimmer subtly with the original signal at about 60%.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~40% |
| Turbulen | ~30% |
| Haze Amt | 0% |
| Shimmer | 0% |
| Wind Dir | 0° |
| Warmth | 0% |
| Storm | Sand |
| Shimmer | On |
| Direction | Horiz |
| Animate | Off |
| Bypass | Off |
| Mix | ~60% |

---

### Exercise 2: Sandstorm Atmosphere

![Sandstorm Atmosphere result](/img/instruments/videomancer/sirocco/sirocco_ex2_s1.png)
*Sandstorm Atmosphere — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A full desert atmosphere with drifting particles and a warm sepia tint layered over the shimmer from Exercise 1.

#### Key Concepts

- Sand particles are pseudorandom bright dots
- Density and brightness are independent
- Color temperature shift tints the entire image

#### Video Source

Footage with a variety of tonal values (street scenes, landscapes, or abstract patterns work well.)

#### Steps

1. Keep the shimmer from Exercise 1. Now flip **Storm** (Switch 7) to **Fog** to enable sand particles.
2. Turn **Haze Amt** (Knob 3) to about 40%. Sparse bright specks appear scattered across the frame.
3. Turn **Shimmer** (Knob 4) to about 50%. The particles brighten (each one flares like a mote of dust catching sunlight.)
4. Now flip **Direction** (Switch 9) to **Vert** to enable the color temperature shift.
5. Slowly increase **Wind Dir** (Knob 5) from 0° to about 200°. The image shifts from its natural palette toward a warm amber-orange atmosphere, as if sunlight is filtering through a cloud of dust.
6. Observe how the sand particles look warmer than the surrounding image: they carry their own small color tint in addition to the global shift.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~40% |
| Turbulen | ~30% |
| Haze Amt | ~40% |
| Shimmer | ~50% |
| Wind Dir | ~200° |
| Warmth | 0% |
| Storm | Fog |
| Shimmer | On |
| Direction | Vert |
| Animate | Off |
| Bypass | Off |
| Mix | ~80% |

---

### Exercise 3: Full Desert Storm

![Full Desert Storm result](/img/instruments/videomancer/sirocco/sirocco_ex3_s1.png)
*Full Desert Storm — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dramatic, fully engaged desert storm with heat shimmer, dense sand, warm color, and amplified contrast.

#### Key Concepts

- Contrast boost amplifies the ripple effect
- All four processing layers interact (ripple, sand, contrast, warmth)
- The mix fader controls the final balance between raw and processed signals

#### Video Source

High-contrast footage: faces, architecture, or bold graphic patterns that show the contrast expansion clearly.

#### Steps

1. Begin with the settings from Exercise 2. Flip **Animate** (Switch 10) to **On** to enable the contrast boost.
2. Notice how the ripple bands become more pronounced: the contrast expansion pushes bright bands brighter and dark bands darker.
3. Increase **Intensity** (Knob 1) to about 70% for a more dramatic shimmer.
4. Increase **Haze Amt** (Knob 3) to about 70% for a thick sandstorm.
5. Push **Wind Dir** (Knob 5) to about 300° for deep amber saturation.
6. Sweep the **Mix** fader between 0% and 100% to hear the full range from clean to storm-blasted.
7. Press **Bypass** (Switch 11) to **On** momentarily for an A/B comparison, then return to **Off**.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~70% |
| Turbulen | ~40% |
| Haze Amt | ~70% |
| Shimmer | ~60% |
| Wind Dir | ~300° |
| Warmth | 0% |
| Storm | Fog |
| Shimmer | On |
| Direction | Vert |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Atmospheric Refraction**: The bending of light as it passes through air layers of different temperatures, responsible for the shimmering, wobbling appearance of objects viewed over hot surfaces.

- **Chroma**: The color information in a video signal, encoded as U and V components in YUV color space. The U axis runs from blue to yellow, and V runs from green to red-magenta.

- **Color Temperature**: A measure of the warmth or coolness of light. Higher values appear bluer (like daylight), and lower values appear more amber-orange (like candlelight or sunset).

- **LFSR**: Linear feedback shift register: a simple circuit that produces a repeating but seemingly random sequence of bits, used here to generate pseudorandom sand particle positions.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Phase Accumulator**: A counter that advances by a fixed amount each frame, producing a steadily increasing value used to animate the sine wave's position over time.

- **Quarter-Wave Symmetry**: A technique for storing only one quarter of a sine period and reconstructing the full wave by mirroring and negating. Reduces memory requirements by a factor of four.

- **Sample and Hold**: A technique where one value is captured and held constant for a period. Here, each scanline samples the sine wave once and holds that brightness offset for the entire line.

- **Saturating Arithmetic**: Addition or subtraction that clamps the result to a maximum or minimum value instead of wrapping around. Prevents bright pixels from wrapping to black or vice versa.

- **Sine Wave**: A smooth, periodic oscillation used here as a brightness modulation pattern. Its shape produces gradual, organic-looking transitions between brighter and darker scanlines.

---
