---
draft: true
sidebar_position: 7
slug: /instruments/videomancer/anodize
title: "Anodize"
image: /img/instruments/videomancer/anodize/anodize_hero_s1.png
description: "Anodize simulates the appearance of anodized aluminum — the electrochemical surface treatment that gives metal products their vivid, uniform colours while maintaining a distinctive metallic reflective quality."
---

![Anodize hero image](/img/instruments/videomancer/anodize/anodize_hero_s1.png)
*Anodize applying a saturated red-orange tint to source video, preserving specular highlights as metallic white reflections.*

---

## Overview

Anodize is a color-tinting effect that replaces the chroma of incoming video with a single, vivid hue while preserving the original brightness and detail. The result simulates the look of anodized aluminum: a flat, saturated color bonded to a metallic surface, where bright specular reflections punch through the tint and glint white. In practice, this means color video enters the program and exits wearing a new outfit: the shapes and textures of the source survive, but the palette is wholly rewritten.

At mild settings, Anodize can subtly warm or cool an image by shifting its color cast. At full strength, it floods the picture with intense, poster-flat color while bright highlights remain brilliant and clean. The **Sheen** control adds a distinctive metallic quality by coupling the brightness contour of the image back into the tint, so light and shadow modulate the color itself: just as light playing across a brushed-aluminum surface shifts the perceived hue.

:::tip
***The core trick is chroma replacement.*** Unlike a color filter that multiplies existing color, Anodize ***discards*** the original U/V chroma entirely and substitutes a computed tint. The source's brightness structure is all that survives. This is what gives the effect its distinctive, flat, industrial character.
:::

### What's In a Name?

***Anodize*** takes its name from ***anodizing***, the electrochemical process used to color aluminum. A thin oxide layer is grown on the metal's surface and infused with dye, producing vibrant colors: reds, blues, golds, greens: while the bare metal beneath still catches the light. The visual result is color that sits *on* a reflective surface rather than *in* it. That's exactly what this program does: it lays a uniform color tint over your video while letting bright highlights shine through untinted, as though the image itself were a sheet of colored metal.

---

## Quick Start

1. Turn **Saturate** (Knob 2) fully clockwise. The entire image floods with a vivid color (the tint has replaced all original chroma.)
2. Sweep **Hue** (Knob 1) slowly from left to right. Watch the tint shift through four distinct color zones: red-orange, blue-purple, green-teal, and gold.
3. Lower **Hi Thrsh** (Knob 3) so that bright areas in the image begin to lose the tint and appear neutral or white. These are the specular highlights (the anodized metal reflecting the light.)
4. Raise **Sheen** (Knob 4) past the halfway point. The brightness contour of the image now subtly shifts the tint: shadows and highlights wear slightly different hues, as though light is playing across a curved metal surface.

---

## Parameters

![Videomancer front panel with Anodize loaded](/img/instruments/videomancer/anodize/anodize_control_panel.png)
*Videomancer's front panel with Anodize active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Hue

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Hue** selects the tint color. When the **Color** toggle (Switch 7) is set to **Red**, the hue knob divides its range into four broad zones based on its upper two bits. The zones sweep through red-orange, blue-purple, green-teal, and gold as the knob turns from minimum to maximum. The transitions between zones are abrupt (the color snaps from one family to the next.)

When the **Color** toggle is set to **Gold**, the hue knob switches to a smooth mode where individual bits in the middle of its range independently flip the polarity of each chroma axis, creating a more continuous sweep through the color wheel. The full range of the knob produces varied color steps rather than four flat zones.

:::note
In both modes, the actual color you see depends equally on **Saturate** (Knob 2). Hue selects the direction of the tint in UV color space; Saturate controls how far the tint reaches from neutral.
:::

---

### Knob 2 — Saturate

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Saturate** controls the intensity of the tint: how far the computed color pushes away from neutral gray in the U/V chroma plane. At 0%, fully counterclockwise, the tint offset is zero and the output chroma stays at the midpoint (neutral), producing a monochrome image. As Saturate increases, the tint becomes more vivid and the chosen hue grows stronger. At 100%, the chroma offset is at half the total range, producing an intensely saturated color.

Because Anodize replaces the input chroma entirely, **Saturate** is effectively the master saturation of the output. There is no way to preserve the original colors: only to control how strongly the new tint asserts itself before the wet/dry **Mix** fader blends the result back with the untouched input.

---

### Knob 3 — Hi Thrsh

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Hi Thrsh** sets the luminance threshold above which the tint begins to fade toward neutral, simulating specular highlights on anodized metal. At 0%, the threshold is at the bottom of the brightness range and nearly every pixel experiences some desaturation. At 100%, the threshold is near the top and only the very brightest pixels lose their tint.

When luma exceeds the threshold, the tint UV values are pushed halfway toward the chroma midpoint (neutral), softening the color in bright areas. If **Finish** (Switch 8) is set to **Mirror**, pixels whose luma exceeds the threshold by a significant margin snap all the way to full neutral (a hard, clean specular highlight with no color cast at all.)

:::tip
For a realistic anodized-metal look, set Hi Thrsh to about 75–80% so that only the brightest reflections punch through. For a duotone poster effect, lower the threshold so that most midtones already appear washed out.
:::

---

### Knob 4 — Sheen

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Sheen** adds a metallic quality by coupling the source brightness back into the chroma output. With Sheen at 0%, the tint color is flat and uniform regardless of brightness. As Sheen increases, brightness variations begin to shift the tint: lighter areas pull the chroma in one direction, darker areas in another, mimicking the way light plays across brushed or curved metal.

The VHDL implements this as a stepped gain control with three thresholds. Below roughly 25%, no sheen is applied. Between 25% and 50%, a subtle shift of one-sixteenth of the luma deviation is added. Between 50% and 75%, the shift doubles to one-eighth. Above 75%, the shift doubles again to one-quarter. Each step produces a noticeably stronger luma-to-chroma coupling.

---

### Knob 5 — Grain

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Grain** introduces a subtle spatial texture by XOR-hashing the horizontal and vertical pixel coordinates and mixing the result into the luma channel. At 0%, no texture is added. As Grain increases, a fine, position-dependent pattern appears across the image, simulating the micro-texture of a brushed or bead-blasted metal surface.

The grain pattern is deterministic: it repeats identically on every frame because it is derived from pixel position, not from a random source. This gives the texture a stable, static quality rather than the flickering of film grain or video noise.

:::note
Grain only affects the luma (brightness) channel. It does not alter the tint color. The texture appears as subtle brightness variation overlaid on the colored surface.
:::

---

### Knob 6 — Uniformty

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Uniformty** is mapped in the parameter register but is reserved in the current firmware. Adjusting this knob has no visible effect on the output. Future firmware revisions may activate this control to adjust the evenness or coverage of the tint.

---

### Switch 7 — Color

| Property | Value |
|----------|-------|
| Off | Red |
| On | Gold |
| Default | Red |

**Color** selects the hue-selection algorithm. In the **Red** position, the **Hue** knob (Knob 1) operates in ***quadrant mode***: its upper two bits divide the range into four discrete color families (red-orange, blue-purple, green-teal, and gold). Transitions between families are abrupt.

In the **Gold** position, the knob operates in ***smooth mode***: individual bits in the middle of the hue range independently flip the U and V chroma axes, creating finer color steps across the full sweep. Smooth mode offers more granular color selection at the expense of the bold, distinct zones that quadrant mode provides.

---

### Switch 8 — Finish

| Property | Value |
|----------|-------|
| Off | Matte |
| On | Mirror |
| Default | Matte |

**Finish** changes how specular highlights behave above the **Hi Thrsh** threshold. In the **Matte** position, pixels above the threshold are partially desaturated: the tint fades gently toward neutral but never disappears completely. This creates a soft, satin-like reflection.

In the **Mirror** position, pixels whose brightness significantly exceeds the threshold snap to full neutral (pure white chroma). This produces hard, clean specular peaks: the kind of crisp, mirror-bright glint you see on polished anodized aluminum under direct light.

---

### Switch 9 — Hi Light

| Property | Value |
|----------|-------|
| Off | Soft |
| On | Sharp |
| Default | Soft |

**Hi Light** controls whether surface grain texture is applied. In the **Soft** position, the luma channel passes through smoothly with no added texture. In the **Sharp** position, the grain engine is active: a position-derived bit pattern is mixed into the luma, creating subtle surface texture across the entire image.

The visual effect at **Sharp** depends heavily on the **Grain** knob (Knob 5). If Grain is at zero, switching to Sharp has no visible impact because the grain amplitude is zero. Increase Grain to see the texture appear.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** inverts the computed tint color, producing the complementary hue on the opposite side of the color wheel. When set to **Off**, the tint is applied as computed from the **Hue** and **Saturate** controls. When set to **On**, the U and V tint values are mirrored around the top of the range, flipping reds to cyans, blues to yellows, and greens to magentas.

:::tip
Toggle **Animate** on and off to quickly compare a tint and its complement. Combined with sweeping the **Hue** knob, this effectively doubles the number of accessible color positions.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Anodize processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the tinted result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (tinted) output. At 0%, only the original video is visible: the tint has no effect. At 100%, the full Anodize processing is applied. Intermediate values blend the two, producing a partial tint that lets some of the original color show through.

The mix is implemented as three parallel ***interpolators*** (one per YUV channel). Each interpolator linearly blends the delayed dry signal with the processed wet signal based on the Mix fader position.

---

## Background

### Anodizing as a visual process

***Anodizing*** is an electrochemical treatment used to color and protect aluminum. The metal is immersed in an acid bath and subjected to an electric current, which grows a porous oxide layer on its surface. This oxide layer is then infused with dye: red, blue, gold, green, black: before being sealed. The result is a surface that is vibrantly colored yet still distinctly metallic: the dye sits in a thin, transparent layer so that the underlying metal texture and reflective character remain visible.

This is the visual model Anodize recreates digitally. The input video's brightness structure represents the metal surface: its contours, textures, and reflections. The tint represents the dye. Bright specular highlights represent areas where the oxide layer is thin or the viewing angle causes the metal to reflect light directly, overwhelming the dye.

### Chroma replacement vs. color filtering

Most color effects in video processing are ***multiplicative***: they scale or shift existing color values. A color filter, for instance, multiplies each pixel's color by a filter coefficient, preserving the relative relationships between colors in the scene. The result looks like viewing the world through tinted glass.

Anodize takes a fundamentally different approach. It performs ***chroma replacement***: the input's U and V channels are discarded entirely and replaced with a single computed tint value. Every pixel receives the same base color (before highlight desaturation and metallic sheen modulation). This is why the effect looks flat and industrial: the color information of the scene is not tinted, it is overwritten.

### Specular highlight preservation

The visual key to the anodized-metal illusion is ***specular highlight preservation***. In the real world, when light reflects off a colored metal surface at a steep angle, the reflected light overwhelms the thin dye layer and appears white (or the color of the light source). Anodize simulates this by comparing each pixel's luma against a configurable threshold. Pixels above the threshold have their tint pushed toward neutral, reducing saturation in bright areas. The **Finish** toggle controls whether this desaturation is gradual (matte) or abrupt (mirror), corresponding to different surface finishes on real anodized metal.


---

## Signal Flow

### Signal Flow Notes

The central asymmetry is the key to understanding Anodize. The Y (luma) channel is largely preserved: it carries the contours, textures, and brightness detail of the source image through to the output. The U and V (chroma) channels are entirely replaced. The computed tint color is a function of the **Hue**, **Saturate**, and **Animate** controls alone: it does not depend on the input color in any way.

Brightness enters the chroma path in two places. First, the highlight detector (stage 4) uses input luma to decide where to desaturate the tint. Second, the metallic sheen stage (stage 6) feeds luma deviation back into the chroma, creating brightness-dependent color modulation. These two luma-to-chroma couplings: one subtractive (desaturation), one additive (sheen): work together to produce the illusion of light interacting with a colored metal surface.

:::note
The **Mix** fader is the only way to recover original color information. Because the wet signal has no trace of original chroma, intermediate Mix values produce a partial blend where the flat tint sits atop the original palette (a useful creative tool in its own right.)
:::


---

## Exercises

These exercises progress from basic tinting to polished metallic surfaces to creative combinations. Each builds familiarity with a different aspect of the Anodize pipeline.
### Exercise 1: Flat Color Poster

![Flat Color Poster result](/img/instruments/videomancer/anodize/anodize_ex1_s1.png)
*Flat Color Poster — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A bold, single-color poster effect where the source video is rendered in one vivid hue with clean white highlights.

#### Key Concepts

- Chroma replacement creates uniform, poster-flat color
- Hue quadrant selection and saturation control
- Highlight threshold determines where color breaks

#### Video Source

A live camera feed or recorded footage with visible specular highlights: metallic objects, wet surfaces, or direct light sources work well.

#### Steps

1. **Tint the image**: Turn **Saturate** (Knob 2) to about 75%. The image floods with color.
2. **Choose a hue**: Sweep **Hue** (Knob 1) to find a color you like. With **Color** (Switch 7) at **Red**, you'll feel four distinct zones click into place.
3. **Reveal highlights**: Lower **Hi Thrsh** (Knob 3) until bright areas begin to lose their tint and appear white. Set it around 75% for a natural look.
4. **Set finish**: Toggle **Finish** (Switch 8) to **Mirror**. The highlights snap to clean white. Toggle back to **Matte** to compare the softer, satin look.
5. **Compare**: Use **Bypass** (Switch 11) to flip between the original and the tinted version.

#### Settings

| Control | Value |
|---------|-------|
| Hue | ~25% |
| Saturate | 75% |
| Hi Thrsh | 75% |
| Sheen | 0% |
| Grain | 0% |
| Uniformty | 50% |
| Color | Red |
| Finish | Mirror |
| Hi Light | Soft |
| Animate | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Metallic Surface

![Metallic Surface result](/img/instruments/videomancer/anodize/anodize_ex2_s1.png)
*Metallic Surface — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A convincing anodized-metal look where brightness contours modulate the tint color and surface grain adds tactile texture.

#### Key Concepts

- Metallic sheen couples luma variations into chroma
- Grain adds surface micro-texture
- Matte vs. Mirror finish changes specular behavior

#### Video Source

Footage with strong tonal variation: faces, hands, landscapes with dramatic lighting, or slowly moving geometric shapes.

#### Steps

1. **Base tint**: Set **Hue** (Knob 1) to about 40% and **Saturate** (Knob 2) to 60%. You should see a blue-purple tint.
2. **Add sheen**: Increase **Sheen** (Knob 4) past 50%. Notice how the color begins to shift in bright and dark areas: shadows and highlights no longer wear the same hue. Push Sheen to about 80% for a strong metallic modulation.
3. **Reveal specular peaks**: Set **Hi Thrsh** (Knob 3) to about 65% with **Finish** at **Mirror**. Bright highlights snap to neutral white.
4. **Add grain**: Toggle **Hi Light** (Switch 9) to **Sharp**, then raise **Grain** (Knob 5) to about 30%. A fine, stable texture appears across the image, simulating the micro-surface of bead-blasted metal.
5. **Refine**: Try switching **Finish** (Switch 8) between **Matte** and **Mirror** to compare satin and polished surfaces.

#### Settings

| Control | Value |
|---------|-------|
| Hue | ~40% |
| Saturate | 60% |
| Hi Thrsh | 65% |
| Sheen | 80% |
| Grain | 30% |
| Uniformty | 50% |
| Color | Red |
| Finish | Mirror |
| Hi Light | Sharp |
| Animate | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Complementary Color Split

![Complementary Color Split result](/img/instruments/videomancer/anodize/anodize_ex3_s1.png)
*Complementary Color Split — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A split-color composition using the Animate toggle to flip between a tint and its complement, blended at partial mix for creative color grading.

#### Key Concepts

- Animate inverts the tint to produce complementary hues
- Mix fader partially blends tint with original color
- Smooth hue mode offers finer color selection

#### Video Source

Footage with a varied color palette (outdoor scenes, colorful objects, or abstract patterns.)

#### Steps

1. **Switch to smooth mode**: Set **Color** (Switch 7) to **Gold**. The **Hue** knob now sweeps through finer color steps.
2. **Select a tint**: Set **Hue** (Knob 1) to about 50% and **Saturate** (Knob 2) to 50%. Note the resulting color.
3. **Flip to complement**: Toggle **Animate** (Switch 10) to **On**. The color jumps to the complementary hue (the opposite side of the color wheel.)
4. **Partial blend**: Lower the **Mix** fader (Fader 12) to about 40%. The original colors bleed through the tint, creating a color-graded look rather than a flat replacement.
5. **Compare tint and complement**: Toggle **Animate** back and forth. At partial Mix, you get two distinct color grades from the same base settings (warm and cool versions of the same image.)
6. **Add metallic character**: Raise **Sheen** (Knob 4) to about 50% to add subtle luma-to-chroma modulation to both the tint and its complement.

#### Settings

| Control | Value |
|---------|-------|
| Hue | 50% |
| Saturate | 50% |
| Hi Thrsh | 80% |
| Sheen | 50% |
| Grain | 0% |
| Uniformty | 50% |
| Color | Gold |
| Finish | Matte |
| Hi Light | Soft |
| Animate | On |
| Bypass | Off |
| Mix | 40% |

---
## Glossary

- **Anodizing**: An electrochemical process that colors aluminum by growing a porous oxide layer and infusing it with dye, producing vibrant colors on a metallic surface.

- **Chroma**: The color information in a video signal, encoded as U (blue-difference) and V (red-difference) components in YUV color space.

- **Chroma Replacement**: Discarding the original color channels of a video signal and substituting computed values, as opposed to multiplicative filtering.

- **Complementary Color**: The hue directly opposite a given color on the color wheel; red and cyan, blue and yellow, green and magenta are complementary pairs.

- **Interpolator**: A hardware module that linearly blends two values based on a fractional mix parameter, used here for the wet/dry crossfade.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Quadrant Mode**: A hue-selection method that divides the control range into four discrete color zones corresponding to the four quadrants of the UV color plane.

- **Specular Highlight**: A bright reflection from a glossy or metallic surface where reflected light overwhelms surface coloring, appearing white or near-white.

---
