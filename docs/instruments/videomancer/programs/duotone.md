---
draft: true
sidebar_position: 95
slug: /instruments/videomancer/duotone
title: "Duotone"
image: /img/instruments/videomancer/duotone/duotone_hero_s1.png
description: "Most color video processors adjust the colors that already exist in the source signal."
---

![Duotone hero image](/img/instruments/videomancer/duotone/duotone_hero_s1.png)
*Duotone splitting a live camera feed into warm shadow tones and cool highlight tones, painting the world in two carefully chosen inks.*

---

## Overview

Duotone is a two-color tinting effect that remaps the brightness of your video into a blend of two selectable hues. Dark areas take on one color, bright areas take on another, and everything in between is a smooth gradient between the two. The result looks like a photograph printed with two ink colors: a technique that has been a staple of graphic design and fine-art printmaking for over a century.

At default settings, Duotone applies a subtle warm-and-cool split that gives ordinary footage a cinematic, stylized look. Pushing the controls further yields bold, poster-like color schemes, hard-edged stencil graphics, or eerie inverted tintypes. Because Duotone preserves the luminance structure of the original image while replacing its color information, faces, textures, and shapes remain recognizable even under extreme color transformations.

:::tip
Duotone is a ***processing*** program: it transforms an incoming video signal. Feed it a camera, a pattern generator, or the output of another Videomancer program for the most interesting results.
:::

### What's In a Name?

The name ***Duotone*** comes directly from the printmaking world. A ***duotone*** print uses exactly two ink colors: typically black plus one spot color: to reproduce a photographic image. The shadows are rendered in one ink and the highlights in the other, with midtones emerging from the overlap. Videomancer's Duotone program generalizes this idea: you choose both colors freely, and the luma of your video decides how much of each ink to lay down.

---

## Quick Start

1. Feed a video source into Videomancer and select the **Duotone** program. You'll see your image tinted with two colors: darker areas lean toward one hue, brighter areas toward the other.
2. Turn **Shadow Hue** (Knob 1) and **Highlight Hue** (Knob 2) slowly. Watch the two tint colors shift independently: shadows and highlights each sweep through different regions of the color wheel.
3. Toggle **Hard Edge** (Switch 9) to **On**. The smooth gradient between the two tones snaps into a sharp binary split: every pixel is now painted in one color or the other, with nothing in between. Adjust **Threshold** (Knob 3) to slide the dividing line up and down the tonal range.
4. Toggle **Invert** (Switch 10) to swap which areas receive the shadow hue and which receive the highlight hue. The entire tonal mapping flips.

---

## Parameters

![Videomancer front panel with Duotone loaded](/img/instruments/videomancer/duotone/duotone_control_panel.png)
*Videomancer's front panel with Duotone active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Shadow Hue

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |

**Shadow Hue** selects the color applied to dark regions of the image. At minimum, the shadow tone is neutral: dark areas remain achromatic. As you turn the knob clockwise, the shadow color sweeps along an arc in the color wheel, introducing progressively stronger tinting. The hue traces a path that moves in one direction through the UV color plane, so different knob positions produce distinctly different colors rather than simply increasing saturation.

At its default position, a gentle warm tint is applied to the shadows. Turning fully clockwise produces a bold, saturated shadow tone.

---

### Knob 2 — Highlight Hue

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Highlight Hue** selects the color applied to bright regions of the image, independently of the shadow hue. The highlight hue traces the opposite arc in the color plane compared to Shadow Hue: when one control produces warm tones, the other naturally produces cool tones at the same knob position. This complementary relationship makes it easy to create classic split-tone color schemes.

At its default position, highlights receive a cool-toned tint that contrasts with the warm shadow default. Fully counterclockwise, highlights are neutral; fully clockwise, they carry a strong saturated color.

---

### Knob 3 — Threshold

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Threshold** controls the crossover point between shadow and highlight tones, but only when **Hard Edge** (Switch 9) is enabled. In hard-edge mode, every pixel whose brightness falls below the threshold receives the shadow hue, and every pixel at or above the threshold receives the highlight hue. Turning the knob clockwise raises the bar, pushing more of the image into shadow territory. Turning it counterclockwise lowers the bar, allowing more of the image to be painted with the highlight color.

:::note
In soft-blend mode (Hard Edge off), the blend between shadow and highlight is driven directly by the input luminance, and the Threshold knob has no visible effect. Switch Hard Edge on to hear this control speak.
:::

---

### Knob 4 — Spread

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Spread** is reserved for a future update. In the current version of Duotone, adjusting this knob has no visible effect on the output image. It is intended to control the width of the transition zone between shadow and highlight tones.

---

### Knob 5 — Intensity

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Intensity** is reserved for a future update. In the current version of Duotone, adjusting this knob has no visible effect on the output image. It is intended to control the saturation strength of the applied color tinting.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** scales the luminance of the processed output. At midpoint (the default), the original brightness is preserved at roughly half scale. Turning the knob clockwise brightens the image; turning it fully clockwise pushes luminance toward maximum. Turning it counterclockwise dims the image; fully counterclockwise produces black regardless of the input.

Because Brightness operates on the processed luma before the wet/dry mix, it affects only the tinted version of the image. The dry signal retains its original brightness. Use this control to balance the tinted image against the original when blending with the **Mix** fader.

---

### Switch 7 — Swap

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Swap** is reserved for a future update. In the current version of Duotone, toggling this switch has no visible effect. It is intended to exchange the shadow and highlight hue assignments.

---

### Switch 8 — Mono Input

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mono Input** is reserved for a future update. In the current version of Duotone, toggling this switch has no visible effect. It is intended to strip incoming chroma before processing, forcing a monochrome input into the duotone mapping.

---

### Switch 9 — Hard Edge

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Hard Edge** switches the blend between shadow and highlight hues from a smooth gradient to a sharp binary cut. With Hard Edge **Off** (the default), the input luminance itself serves as the blend factor: dark pixels receive more shadow hue, bright pixels receive more highlight hue, and midtones get a proportional mix of both. The transition is gentle and continuous.

With Hard Edge **On**, the blend snaps to a binary decision controlled by the **Threshold** knob: pixels below the threshold receive the pure shadow hue, and pixels at or above the threshold receive the pure highlight hue. There is no gradient: the image becomes a two-color stencil. This mode is where Duotone produces its most graphic, poster-like results.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** flips the input luminance before all other processing. Dark becomes bright and bright becomes dark, which reverses the entire tonal mapping: areas that were painted with the shadow hue now receive the highlight hue, and vice versa. In hard-edge mode, Invert effectively swaps which side of the threshold is which. In soft-blend mode, it reverses the gradient direction.

:::tip
Combining **Invert** with different **Shadow Hue** and **Highlight Hue** settings creates a second set of completely different color splits from the same two hue positions. Think of it as getting two duotone looks for the price of one.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all duotone processing. Sync timing is still aligned through the delay pipeline, so switching Bypass on and off does not cause glitches. Use Bypass for instant A/B comparison between the raw video and the tinted result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the original (dry) video and the duotone-processed (wet) video. At maximum (fully right), you see only the processed result. At minimum (fully left), you see only the original input. Intermediate positions blend the two, allowing you to dial in a subtle tint or a half-strength color wash.

Because the mix operates after all other processing stages, it's the final creative control in the signal chain. Pulling the fader back is the quickest way to soften the effect without changing any other settings.

---

## Background

### Duotone printing

The ***duotone*** technique dates back to the early twentieth century, when printers discovered that a single black ink couldn't capture the full tonal range of a photograph. By printing the same image twice: once in black and once in a second color: they could extend the dynamic range and add a color mood to the print. Modern graphic designers use digital duotone effects for the same reason: to impose a deliberate, limited palette on photographic imagery.

Videomancer's Duotone program applies this concept in real time. Instead of inks, it uses two positions in the YUV color plane. Instead of a printing press, it uses a blend function driven by the input video's luma channel. The result is the same: a two-tone image where color follows brightness.

### YUV color space

Video signals are encoded in ***YUV*** format, where Y carries luminance (brightness) and U and V carry chrominance (color). The neutral point in the UV plane is (512, 512): this represents achromatic gray, with no color. Moving away from the center in any direction adds color. Duotone generates two points in the UV plane: one for shadows, one for highlights: and blends between them based on luminance.

The **Shadow Hue** and **Highlight Hue** knobs each trace an arc through the UV plane, but in opposite directions. The shadow path increases U while decreasing V; the highlight path decreases U while increasing V. This complementary layout means that when both knobs are at similar positions, the resulting shadow and highlight colors sit on opposite sides of the color wheel (a natural split-tone palette.)

### Blend modes

Duotone offers two blend modes, selected by the **Hard Edge** toggle:

- **Soft blend**: The raw input luma *is* the blend factor. Every pixel gets a proportional mixture of shadow and highlight color based on its brightness. The result is a smooth tonal gradient from one hue to the other.
- **Hard blend**: A binary threshold divides pixels into two groups. Every pixel is painted with one color or the other (no mixing. The **Threshold** knob sets the dividing line.)

Soft blend produces cinematic, tonal looks. Hard blend produces flat, graphic, poster-like results. Toggling between them with the same hue settings reveals two completely different aesthetics from the same parameters.


---

## Signal Flow

### Signal Flow Notes

The core of the pipeline is the blend computation in stage 3. In soft mode, the input luma itself controls the crossfade between shadow and highlight UV coordinates: no threshold is involved. This creates a continuous tonal mapping where every brightness level corresponds to a unique color. In hard mode, the threshold creates a binary partition, and the entire image is painted with exactly two flat colors.

The brightness control (stage 4) scales the output luma independently of the color mapping. This means you can dim or brighten the duotone image without affecting which hue each pixel receives: color assignment depends solely on the *input* luma, not the output.

:::note
The delay pipeline aligns sync signals with processed data across the full 8-clock latency, ensuring the wet/dry mix and bypass switch operate on correctly aligned data.
:::


---

## Exercises

These exercises progress from basic split-toning to graphic stencil effects and creative inversions. Each exercise highlights a different aspect of the duotone color mapping.
### Exercise 1: Classic Split Tone

![Classic Split Tone result](/img/instruments/videomancer/duotone/duotone_ex1_s1.png)
*Classic Split Tone — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A warm-shadow, cool-highlight split-tone look reminiscent of cyanotype prints or toned silver gelatin photographs.

#### Key Concepts

- Luma drives the blend between two hues
- Shadow and highlight hues trace complementary arcs in the color plane
- Soft blend creates a smooth tonal gradient

#### Video Source

A live camera feed or recorded footage with a mix of light and dark regions (faces, architecture, or landscapes work well.)

#### Steps

1. Set **Shadow Hue** (Knob 1) to roughly 25%. Dark areas take on a warm, amber tint.
2. Set **Highlight Hue** (Knob 2) to roughly 75%. Bright areas shift toward a cool complementary tone.
3. Make sure **Hard Edge** (Switch 9) is **Off**. The transition between the two colors should be smooth and continuous.
4. Adjust **Brightness** (Knob 6) until the overall exposure looks balanced. Try positions just above and below the midpoint.
5. Pull the **Mix** fader (Fader 12) to about 75% to let a hint of the original color show through.

#### Settings

| Control | Value |
|---------|-------|
| Shadow Hue | ~25% |
| Highlight Hue | ~75% |
| Threshold | 50% |
| Spread | 25% |
| Intensity | 75% |
| Brightness | ~50% |
| Swap | Off |
| Mono Input | Off |
| Hard Edge | Off |
| Invert | Off |
| Bypass | Off |
| Mix | ~75% |

---

### Exercise 2: Two-Color Stencil

![Two-Color Stencil result](/img/instruments/videomancer/duotone/duotone_ex2_s1.png)
*Two-Color Stencil — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A bold, flat, two-color graphic that looks like a screen-printed poster or a stencil cutout.

#### Key Concepts

- Hard-edge mode creates a binary threshold
- The Threshold knob controls the dividing line
- Invert flips the entire mapping

#### Video Source

High-contrast footage: strong backlighting, silhouettes, or a black-and-white pattern generator output.

#### Steps

1. Enable **Hard Edge** (Switch 9). The smooth gradient snaps into two flat colors.
2. Set **Shadow Hue** (Knob 1) to about 10% and **Highlight Hue** (Knob 2) to about 60%. You should see a two-color split.
3. Sweep **Threshold** (Knob 3) slowly from left to right. Watch the dividing line between the two colors slide across the brightness range (like adjusting the exposure of a lithographic print.)
4. Toggle **Invert** (Switch 10). The two color regions swap. What was shadow is now highlight.
5. Turn **Brightness** (Knob 6) fully clockwise. The luminance channel opens up, and the stencil edges become crisper against the brighter field.
6. Set **Mix** (Fader 12) to 100% for the full graphic effect.

#### Settings

| Control | Value |
|---------|-------|
| Shadow Hue | ~10% |
| Highlight Hue | ~60% |
| Threshold | ~50% |
| Spread | 25% |
| Intensity | 75% |
| Brightness | 100% |
| Swap | Off |
| Mono Input | Off |
| Hard Edge | On |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Inverted Duotone with Wet/Dry Blend

![Inverted Duotone with Wet/Dry Blend result](/img/instruments/videomancer/duotone/duotone_ex3_s1.png)
*Inverted Duotone with Wet/Dry Blend — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An eerie, otherworldly image where inverted tonal relationships peek through the original color palette.

#### Key Concepts

- Invert reverses the tonal mapping before all processing
- Mix blends processed and original signals
- Combining invert with a partial mix creates complex tonal layering

#### Video Source

Any footage with rich midtone detail (foliage, textiles, or a face with even lighting.)

#### Steps

1. Set **Shadow Hue** (Knob 1) to about 40% and **Highlight Hue** (Knob 2) to about 50% for a subtle, close-hued palette.
2. Enable **Invert** (Switch 10). The tonal mapping flips: formerly bright areas now receive the shadow hue and vice versa.
3. Make sure **Hard Edge** (Switch 9) is **Off** for a smooth gradient.
4. Turn **Brightness** (Knob 6) to about 40%. The dimmer setting enhances the inverted, negative-image quality.
5. Pull **Mix** (Fader 12) to about 50%. The inverted duotone blends with the unprocessed original, creating a ghostly double-exposed quality.
6. Slowly sweep **Shadow Hue** and **Highlight Hue** to explore how the inverted color map interacts with the original hues visible through the mix.

#### Settings

| Control | Value |
|---------|-------|
| Shadow Hue | ~40% |
| Highlight Hue | ~50% |
| Threshold | 50% |
| Spread | 25% |
| Intensity | 75% |
| Brightness | ~40% |
| Swap | Off |
| Mono Input | Off |
| Hard Edge | Off |
| Invert | On |
| Bypass | Off |
| Mix | ~50% |

---
## Glossary

- **Blend Factor**: A value that determines the proportion of two signals mixed together; in Duotone, luminance serves as the blend factor between shadow and highlight colors.

- **Chrominance**: The color component of a video signal, encoded as U and V channels in YUV color space; moving away from the neutral midpoint (512, 512) adds color.

- **Duotone**: A technique originating in printmaking that uses exactly two colors to reproduce a photographic image, with brightness controlling the proportion of each color.

- **Hard Edge**: A binary threshold that divides pixels into two groups with no blend or transition between them, producing flat, graphic color regions.

- **Interpolator**: A hardware module that computes a weighted blend (linear interpolation) between two input values, used here for the wet/dry mix.

- **Luminance**: The brightness component (Y) of a YUV video signal, independent of color information.

- **Split Tone**: A photographic technique where shadows and highlights are tinted with different colors, a specific application of duotone processing.

- **Threshold**: A fixed brightness level that divides pixels into two groups; pixels above and below the threshold receive different treatments.

- **Wet/Dry Mix**: A crossfade between the processed (wet) signal and the original unprocessed (dry) signal, allowing partial-strength effects.

---
