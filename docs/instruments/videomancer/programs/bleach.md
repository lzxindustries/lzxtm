---
draft: true
sidebar_position: 21
slug: /instruments/videomancer/bleach
title: "Bleach"
image: /img/instruments/videomancer/bleach/bleach_hero_s1.png
description: "Bleach simulates the photochemical bleach bypass (also known as skip bleach or ENR) process — a film lab technique where the bleach step in colour negative development is partially or fully omitted, leaving metallic silver in the emulsion alongside the colour dyes."
---

![Bleach hero image](/img/instruments/videomancer/bleach/bleach_hero_s1.png)
*Bleach transforming a portrait into a high-contrast, desaturated silver retention look (the hallmark of war films and neo-noir cinema.)*

---

## Overview

Bleach simulates the photochemical ***bleach bypass*** process (also known as ENR or silver retention), a film developing technique where the bleaching step is partially or fully omitted.  In traditional film processing, the bleach step removes the metallic silver from the emulsion after the color dyes have been formed. By skipping this step, the silver remains in the film alongside the color dyes, acting as a neutral density overlay that simultaneously desaturates and boosts contrast.

The effect is immediately recognizable from films like *Saving Private Ryan*, *Se7en*, and *Minority Report*: a gritty, desaturated, high-contrast look with deep blacks, muted colors, and an almost metallic quality. Bleach recreates this entirely within the video signal path, offering fine control over the silver density, contrast stretch, film grain, highlight protection, and tonal warmth or coolness.

### What's In a Name?

In a photographic darkroom, the ***bleach*** bath is a chemical step that dissolves the metallic silver from developed film, leaving only the transparent color dyes. To ***bypass*** this step: or use a milder variant called ***ENR*** (named after Ernesto Novelli Rimo, the Technicolor Rome technician who refined the process): means the silver stays, adding density and desaturation. The program name captures the essence of what is removed: the bleach itself.

---

## Quick Start

1. Feed any video source into Videomancer with Bleach loaded. The image immediately appears desaturated and slightly higher in contrast.
2. Increase **Bypass Amt** (Knob 1) to about 75%. Colors drain further and contrast sharpens (the hallmark bleach bypass look.)
3. Turn **Silver** (Knob 2) up to about 60%. The highlights brighten and take on a metallic, silvery quality.
4. Add a touch of **Grain** (Knob 4) at about 30% for the organic film texture that completes the look.

---

## Parameters

![Videomancer front panel with Bleach loaded](/img/instruments/videomancer/bleach/bleach_control_panel.png)
*Videomancer's front panel with Bleach active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Bypass Amt

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Bypass Amt** controls how much of the bleach step is skipped: in other words, how much desaturation is applied to the image. At 0%, chroma passes through unmodified. As the value increases, the U and V channels are pulled progressively toward neutral (512): at low-mid values, 87.5% of the chroma is retained; at mid values, 75%; at high values, only 50%. The result is a controlled drain of color saturation that leaves the image feeling steely and cool.

---

### Knob 2 — Silver

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Silver** controls the density of the retained silver layer. This adds a luminance boost proportional to the existing brightness: bright areas get brighter, amplifying the metallic quality of the image. At low values, the silver deposit is minimal and the image stays dark. As Silver increases, highlights gain a brilliant, almost reflective quality. The ENR vs. Skip process mode changes how aggressively the silver scales with brightness.

:::note
The silver boost is ***proportional*** to brightness: it amplifies what's already bright. Dark areas receive very little boost. This is different from a simple brightness offset: it specifically enhances the luminous, metallic quality of highlights.
:::

---

### Knob 3 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |

**Contrast** stretches the luminance range outward from the midpoint (512). At 0%, contrast passes through at unity. As the value increases, the image stretches: at low-mid values, contrast scales to 1.125×; at mid, 1.25×; at high, 1.5×. The expansion is symmetrical around the midpoint, so blacks get darker and whites get brighter simultaneously. Combined with the desaturation from Bypass Amt, this creates the punchy, gritty tonal character of bleach bypass cinema.

---

### Knob 4 — Grain

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Grain** adds LFSR-based film grain noise to the luminance channel. At 0%, no grain is applied. As the value increases, progressively larger random values are added to or subtracted from each pixel's brightness. The grain size (Fine or Coarse) controls the bit depth of the noise, with Coarse mode producing larger, more visible grain clumps.

---

### Knob 5 — Hi Prot

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Hi Prot** (Highlight Protection) prevents the contrast stretch and silver boost from clipping highlight detail. When enabled (values above ~25%), pixels with original brightness above 768 are blended 50/50 with their contrast-stretched counterparts. This preserves detail in very bright areas: skin highlights, reflections, and specular sources: that would otherwise be crushed to pure white by the aggressive contrast processing.

:::tip
Highlight Protection is essential when processing faces. Skin tones in bright areas tend to blow out with high contrast and silver settings. Setting Hi Prot to ~50% keeps facial detail intact while the rest of the frame gets the full treatment.
:::

---

### Knob 6 — Black Pt

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |

**Black Pt** (Black Point) sets a minimum brightness floor. At 0%, blacks can reach absolute zero. As the value increases, the darkest possible output is lifted, creating a lifted-blacks look that softens the shadow regions and gives the image a slightly faded, archival quality. The floor is derived by shifting the pot value right by 3, so at full the floor reaches about 128.

---

### Switch 7 — Process

| Property | Value |
|----------|-------|
| Off | ENR |
| On | Skip |
| Default | ENR |

**Process** selects between two bleach bypass development modes. **ENR** (the default) simulates the Technicolor ENR process, where the silver retention is more controlled and the luminance boost scales gradually with brightness. **Skip** simulates the more aggressive skip-bleach technique, where the silver boost is stronger and more abrupt, producing a harder, more contrasty result.

---

### Switch 8 — Grain Sz

| Property | Value |
|----------|-------|
| Off | Fine |
| On | Coarse |
| Default | Fine |

**Grain Sz** (Grain Size) controls the visual scale of the film grain. **Fine** uses the lower 6 bits of the LFSR for small, dense grain particles. **Coarse** shifts up to bits 7–2, producing larger, more visible grain clumps that resemble high-speed film stock pushed in development.

---

### Switch 9 — Tone

| Property | Value |
|----------|-------|
| Off | Cold |
| On | Warm |
| Default | Cold |

**Tone** shifts the overall color temperature of the processed image. **Cold** adds a slight blue push to U (+12) and pulls V back (−8), creating the steely, blue-tinged look of most bleach bypass cinematography. **Warm** reverses this with an amber shift (U −8, V +12), evoking the look of warm-toned print stock or a gold-tinted silver retention process.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** flips the processed luminance channel. With Invert **On**, highlights become shadows and vice versa. This is applied after all other processing (grain, contrast, silver boost), creating a negative image with the bleach bypass treatment applied in the inverted domain.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Bleach processing stages. Use for instant A/B comparison.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) signal and the wet (Bleach-processed) signal. At 0%, only the original video is output. At 100%, only the fully processed signal passes through. Intermediate values allow a subtle bleach bypass effect that retains more of the original color while adding a hint of the metallic, desaturated character.

---

## Background

### Bleach bypass history

The bleach bypass technique was developed in the 1960s but became widely known through its use in feature films from the 1990s onward. Cinematographer Janusz Kamiński and film lab technician Deluxe developed the look for *Schindler's List* (1993) and refined it further for *Saving Private Ryan* (1998), where it became synonymous with the desaturated, gritty war reality aesthetic. Darius Khondji used the ENR process extensively in *Se7en* (1995), creating the oppressive, rain-soaked darkness that defined the film's visual identity.

### Silver retention photochemistry

In conventional color negative processing (***C-41***), the bleach bath converts the metallic silver image back into silver halide salts, which are then dissolved in the fixer bath. Only the transparent color dyes remain. When the bleach is skipped or weakened, the metallic silver particles stay in the emulsion, sitting on top of the color dyes like a permanent neutral density filter. This has three simultaneous effects: desaturation (the silver blocks some light that would otherwise show color), contrast increase (the silver adds density primarily in the highlights and midtones where it was formed during development), and grain emphasis (the retained silver particles add visible texture).

### Shift-based signal processing

Bleach implements all arithmetic using ***bit shifts*** and additions: no hardware multiplications. On the iCE40 HX4K FPGA, multipliers consume significant resources, so shift-based approximations are both faster and more area-efficient. For example, the desaturation stage computes "keep 75% of chroma" by computing `chroma - (chroma >> 2)`, which equals `chroma × 0.75` without a multiplier. Similarly, the contrast stretch computes `1.25×` as `value + (value >> 2)`. These approximations sacrifice some precision but maintain the visual character of the effect.


---

## Signal Flow

### Signal Flow Notes

The pipeline order matters: desaturation happens first, then silver boost, then contrast. This matches the photochemistry: the silver retention changes the density (brightness), and then printing the film on high-contrast stock (the contrast stage) amplifies the density differences. Reversing the order would produce a different look, because the contrast stretch would be applied to the un-silvered brightness values.

The highlight protection stage operates as a safety valve, blending the extreme high values back toward the original to prevent detail loss. It's applied after contrast but before grain, so the grain texture is added on top of the protected highlights rather than being amplified by the contrast stretch.

:::warning
With both Silver and Contrast at high values, the image can easily clip to pure white in highlights. Use Highlight Protection to preserve detail in bright areas, or reduce Mix to blend the effect with the original. The Black Point floor also helps prevent hard black clipping at the bottom of the range.
:::


---

## Exercises

These exercises progress from a basic bleach bypass look through to a stylized cinematic grade with grain and split toning.
### Exercise 1: The Saving Private Ryan Look

![The Saving Private Ryan Look result](/img/instruments/videomancer/bleach/bleach_ex1_s1.png)
*The Saving Private Ryan Look — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A desaturated, high-contrast image with muted but still present color (the signature look of modern war cinema.)

#### Key Concepts

- Desaturation via silver retention drains color without eliminating it
- Contrast stretch amplifies the density differences from the silver layer
- ENR mode provides the controlled, gradual look used in war cinematography

#### Video Source

Any video with a range of tones (a scene with faces, sky, and dark shadows works best.)

#### Steps

1. Set **Process** (Switch 7) to ENR.
2. Set **Bypass Amt** (Knob 1) to ~75% for strong desaturation.
3. Set **Contrast** (Knob 3) to ~60% for punchy mid-range contrast.
4. Set **Silver** (Knob 2) to ~50% for a moderate metallic boost.
5. Enable **Hi Prot** (Knob 5) at ~50% to prevent skin tones from clipping.
6. Switch **Tone** (Switch 9) to Cold for the steely blue-silver feel.

#### Settings

| Control | Value |
|---------|-------|
| Bypass Amt | ~75% |
| Silver | ~50% |
| Contrast | ~60% |
| Grain | ~0% |
| Hi Prot | ~50% |
| Black Pt | ~0% |
| Process | ENR |
| Grain Sz | Fine |
| Tone | Cold |
| Invert | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 2: Se7en Darkness

![Se7en Darkness result](/img/instruments/videomancer/bleach/bleach_ex2_s1.png)
*Se7en Darkness — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dark, gritty image with heavy grain and lifted blacks: the claustrophobic feel of neo-noir thriller cinematography.

#### Key Concepts

- Skip bleach produces a harder, more extreme version of the look
- Coarse grain adds visible film texture
- Black point lift creates a faded, oppressive atmosphere

#### Video Source

A dimly lit scene or one with strong shadows. Interior scenes work particularly well.

#### Steps

1. Switch **Process** (Switch 7) to Skip for the harder bleach bypass variant.
2. Set **Bypass Amt** to ~85% for near-total desaturation.
3. Push **Contrast** to ~80%. Shadows deepen dramatically.
4. Add **Grain** at ~60% with **Grain Sz** set to Coarse. Visible film texture appears.
5. Lift **Black Pt** to ~30%. The deepest blacks soften slightly, preventing total blackness.
6. Set **Silver** to ~70%. Highlights gain a harsh metallic intensity.

#### Settings

| Control | Value |
|---------|-------|
| Bypass Amt | ~85% |
| Silver | ~70% |
| Contrast | ~80% |
| Grain | ~60% |
| Hi Prot | ~30% |
| Black Pt | ~30% |
| Process | Skip |
| Grain Sz | Coarse |
| Tone | Cold |
| Invert | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 3: Warm Silver Print

![Warm Silver Print result](/img/instruments/videomancer/bleach/bleach_ex3_s1.png)
*Warm Silver Print — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A warm-toned, moderately desaturated image reminiscent of silver gelatin prints displayed under tungsten lighting.

#### Key Concepts

- Warm tone creates an amber-tinted bleach bypass look
- Moderate settings produce a more subtle, refined effect
- Mix allows blending the effect with original color

#### Video Source

Portraits or vintage-feeling subject matter (book spines, textured fabrics, architectural details.)

#### Steps

1. Set **Process** to ENR and **Tone** (Switch 9) to Warm.
2. Set **Bypass Amt** to ~55% for moderate desaturation that retains some color.
3. Set **Silver** to ~40% for subtle metallic highlights.
4. Set **Contrast** to ~45% for gentle contrast enhancement.
5. Add fine **Grain** at ~25% for a delicate film texture.
6. Reduce **Mix** to ~70% to let some original color bleed through.

#### Settings

| Control | Value |
|---------|-------|
| Bypass Amt | ~55% |
| Silver | ~40% |
| Contrast | ~45% |
| Grain | ~25% |
| Hi Prot | ~50% |
| Black Pt | ~10% |
| Process | ENR |
| Grain Sz | Fine |
| Tone | Warm |
| Invert | Off |
| Bypass | Off |
| Mix | ~70% |

---
## Glossary

- **Bleach Bypass**: A film processing technique where the bleach step is skipped, leaving metallic silver in the emulsion alongside color dyes.

- **C-41**: The standard chemical process for developing color negative film, consisting of developer, bleach, fixer, stabilizer, and wash steps.

- **Desaturation**: The reduction of color intensity toward neutral gray, caused in bleach bypass by the silver layer blocking light.

- **ENR**: A refinement of the bleach bypass process developed at Technicolor Rome, named after technician Ernesto Novelli Rimo. Produces a more controlled, subtle silver retention effect.

- **Film Grain**: Random variations in density across the film surface caused by silver halide crystals of varying sizes. Simulated here with an LFSR-based noise generator.

- **LFSR**: Linear Feedback Shift Register; a deterministic pseudo-random number generator used for film grain noise.

- **Shift-Based Arithmetic**: Using bit shifts (multiply/divide by powers of 2) instead of hardware multipliers to perform approximate calculations, conserving FPGA resources.

- **Silver Retention**: Another term for bleach bypass; the metallic silver particles that remain in the emulsion contribute both density and grain to the image.

---
