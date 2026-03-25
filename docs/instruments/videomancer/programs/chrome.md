---
draft: true
sidebar_position: 51
slug: /instruments/videomancer/chrome
title: "Chrome"
image: /img/instruments/videomancer/chrome/chrome_hero_s1.png
description: "There is a particular quality to chrome — the way it swallows the world around it and hands it back distorted, compressed, impossibly bright."
---

![Chrome hero image](/img/instruments/videomancer/chrome/chrome_hero_s1.png)
*Chrome applying liquid-metal S-curve contrast, desaturation, and specular bloom to transform video into a polished reflective surface.*

---

## Overview

Chrome turns video into liquid metal. It applies a high-contrast ***S-curve*** to the luminance channel, pushing highlights brighter and shadows darker to create the dramatic tonal separation seen on a polished metallic surface. Chroma is attenuated toward monochrome, stripping away the color palette the way a real chrome mirror strips away the color of whatever it reflects. A ***specular bloom*** stage adds a hot, glowing boost to the brightest highlights: the digital equivalent of the white-hot glints that slide across a curved chrome bumper. An optional vertical blur averages each pixel with the line above it, softening the image into the smooth, undulating quality of molten mercury.

Together these stages produce a convincing metallic reflection aesthetic. At subtle settings, Chrome adds a steely, fashion-editorial grade to footage. At extreme settings, the image collapses into stark graphic shapes: high-contrast silhouettes swimming in a sea of burning silver. A warm-or-cool tint control lets you shift the chrome toward gold or blue, and a wet/dry mix fader lets you blend the processed signal with the original at any ratio.

:::tip
Chrome is a ***processing*** program. It transforms an incoming video signal, so you need to feed it a source (a camera, a pattern generator, or another program's output.)
:::

### What's In a Name?

***Chrome*** is short for ***chromium***, the element used to electroplate objects with a mirror-bright, corrosion-resistant finish. Chrome plating transforms ordinary steel into a silvery, reflective surface: car bumpers, bathroom fixtures, sci-fi props. This program does the same thing to video: it electroplates your signal with a high-contrast, desaturated metallic sheen. There is also a playful etymological echo: "chrome" shares its Greek root (χρῶμα, *chrōma*, meaning "color") with ***chroma***, the color information in a video signal. The irony is that Chrome's signature move is to *drain* chroma, reducing the image to luminance-driven metal.

---

## Quick Start

1. Feed a camera or recorded footage into Videomancer. With all controls at their defaults, Chrome applies a moderate S-curve, partial desaturation, and full wet mix. You should see the image take on a cooler, higher-contrast character immediately.
2. Increase **Contrast** (Knob 1) past the halfway mark. Shadows plunge toward black and highlights push toward white: the image snaps into a hard, reflective look with sharp tonal edges.
3. Turn **Desat** (Knob 2) clockwise while setting the **Tint** toggle (Switch 9) to **On**. Watch the color drain from the image in stages, leaving a near-monochrome metallic surface. Flip **Metal** (Switch 7) to **Steel** and increase **Tint Hue** (Knob 6) to push the chrome toward a warm, golden finish.
4. Raise **Bloom** (Knob 4) to add a hot glow on the brightest highlights. Adjust **Blur Amt** (Knob 3) to control how much of the image receives the bloom: lower values bloom more of the picture; higher values confine the glow to only the most intense highlights.

---

## Parameters

![Videomancer front panel with Chrome loaded](/img/instruments/videomancer/chrome/chrome_control_panel.png)
*Videomancer's front panel with Chrome active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contrast** controls the strength of the S-curve contrast enhancement applied to the luminance channel. The S-curve pushes pixel values away from the midpoint: highlights become brighter, shadows become darker, and the mid-gray region is stretched into a steep transition. At the bottom of its range, the curve applies a gentle polish: tonal separation is subtle, and the image retains its original dynamic range. As the control increases, the curve steepens through three discrete strength levels, progressively crushing shadows and clipping highlights into the hard, flat planes of a mirror surface. At full strength, the contrast push is dramatic: the luminance channel divides into stark light and dark regions with a razor-thin midtone band.

:::note
The S-curve uses three discrete strength levels internally, so you may notice the contrast "step" at roughly one-third and two-thirds of the knob's travel rather than changing continuously.
:::

---

### Knob 2 — Desat

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Desat** controls the amount of chroma reduction: how aggressively Chrome strips color from the signal. This control only takes effect when the **Tint** toggle (Switch 9) is set to **On**. With Tint On, the desaturation moves through four discrete levels: at the bottom of the range, source color passes through unaltered. As the value increases, chroma is progressively halved, quartered, and then reduced to an eighth of its original intensity, pulling the image toward monochrome in visible steps. At the top of the range, only a faint ghost of the original color remains: enough to hint at the source material without disrupting the metallic illusion.

:::tip
When the **Tint** toggle is **Off**, Chrome forces full monochrome regardless of this knob's position. Use Tint On + Desat to find the sweet spot between pure chrome and color-tinted metal.
:::

---

### Knob 3 — Blur Amt

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Blur Amt** sets the luminance threshold that activates the specular bloom effect. Pixels whose brightness exceeds this threshold receive an additive boost from the **Bloom** control (Knob 4). At the bottom of its range, nearly every pixel exceeds the threshold and the entire image receives the bloom boost, producing a bright, washed-out glow. Increasing the control raises the activation threshold, confining the bloom to progressively brighter highlights. At the top of the range, only the very brightest pixels in the image trigger the bloom, creating tight, jewel-like specular glints on reflective surfaces.

---

### Knob 4 — Bloom

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bloom** controls how much brightness is added to pixels that exceed the specular threshold set by **Blur Amt** (Knob 3). At the bottom of its range, no brightness is added even to qualifying pixels: the bloom effect is silent. As the value increases, qualifying highlights receive a progressively stronger brightness boost, pushing them toward peak white. At full strength, the specular glints burn hot and bright, simulating the searing highlights on a polished chrome surface catching direct light.

:::warning
High Bloom combined with a low Blur Amt can wash out the entire image to near-white. Use these two controls together: Blur Amt sets *where* the bloom appears, and Bloom sets *how intense* it is.
:::

---

### Knob 5 — Reflect

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Reflect** controls the vertical smoothing stage. Below the midpoint of its range, no smoothing takes place: the Y channel passes through with its original vertical detail intact. Once the control crosses the midpoint, Chrome begins averaging each pixel's luminance with the pixel directly above it on the previous scan line. This vertical blur softens hard horizontal edges into smooth gradients, giving the image the undulating, liquid quality of molten metal or a funhouse mirror. The effect is binary: either the averaging is on or off: so this control acts as a threshold switch rather than a gradual blend.

---

### Knob 6 — Tint Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Tint Hue** controls the intensity of the warm or cool color tint applied to the chrome surface. At the bottom of its range, no tint is applied: the chrome is a neutral silver. As the control increases, the tint strengthens, pushing the chroma channels further in the direction selected by the **Metal** toggle (Switch 7). At full intensity, the tint is pronounced: a rich gold or a deep steel-blue, depending on the toggle position. The tint is applied after desaturation, so it colors the chrome surface itself rather than modulating the source material's original palette.

---

### Switch 7 — Metal

| Property | Value |
|----------|-------|
| Off | Chrome |
| On | Steel |
| Default | Chrome |

**Metal** selects the color temperature of the tint applied by **Tint Hue** (Knob 6). In the **Chrome** position, the tint shifts toward cool blue-cyan tones: the classic cold, mirror-bright finish of decorative chromium plating. In the **Steel** position, the tint shifts toward warm golden-amber tones: the look of brushed brass, aged copper, or a gold-plated surface. This toggle has no visible effect when Tint Hue is at its minimum (no tint applied).

---

### Switch 8 — Curve

| Property | Value |
|----------|-------|
| Off | S-Curve |
| On | Clip |
| Default | S-Curve |

**Curve** selects the direction of the S-curve contrast enhancement. In the **S-Curve** position, the curve operates normally: highlights are pushed brighter and shadows are pushed darker, increasing contrast and creating the signature chrome look. In the **Clip** position, the curve is inverted: highlights are pulled *down* and shadows are pushed *up*, compressing the tonal range toward the midpoint. The Clip mode produces a flatter, more muted metallic surface (less mirror, more brushed aluminum.)

---

### Switch 9 — Tint

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Tint** controls whether Chrome retains any of the source video's original color. In the **Off** position, the chroma channels are forced to neutral gray, producing a fully monochrome output: pure chrome with no trace of the original color palette. In the **On** position, Chrome applies partial desaturation controlled by the **Desat** knob (Knob 2), allowing some of the source color to bleed through the metallic surface. In both modes, the warm/cool tint from **Tint Hue** (Knob 6) is still applied on top.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** activates a subtle shimmer animation on the specular bloom highlights. In the **Off** position, the specular threshold is static: the bloom boundary is fixed and stable. In the **On** position, the threshold oscillates slowly with the frame counter, causing the bloom highlights to pulse and shift in a gentle, rhythmic pattern. The effect is subtle: a quiet breathing of the specular glints, as though the chrome surface is alive and catching light from a slowly moving source.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Chrome processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw source and the chromed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (original) and wet (processed) signal. At the bottom of its range, the output is the unprocessed input: Chrome has no effect. As the fader moves up, the processed signal is blended in progressively. At the top of its range, the output is fully processed. The Mix fader operates independently on all three channels (Y, U, V), so the crossfade is smooth and artifact-free. Use intermediate Mix positions to apply a subtle chrome wash over the source without fully committing to the metallic look.

---

## Background

### The S-Curve: Sculpting Contrast

The heart of Chrome's metallic illusion is a ***sigmoidal contrast curve***: the S-curve. This technique has roots in photographic film processing, where "pushing" development creates a steeper characteristic curve with deeper blacks and brighter whites. In the analog video world, the same effect is achieved with a ***processing amplifier*** (proc amp) that applies gain and offset around a midpoint.

Chrome implements the S-curve entirely with shift operations: no multipliers. The algorithm measures how far each pixel's luminance sits from the midpoint (512 in a 10-bit system), then adds a fraction of that distance back, pushing the pixel further from center. The fraction is selected by the **Contrast** knob in three steps: one-eighth, one-quarter, or one-half of the distance. This creates a piecewise-linear approximation of a smooth sigmoid, with the midpoint acting as a fixed pivot. The result is the same as the tonal curve in photographic darkroom printing: shadows deepen, highlights bloom, and the midtones compress into a narrow, contrasty band.

### Desaturation and the Monochrome Spectrum

Real chrome surfaces reflect their surroundings with nearly perfect fidelity in luminance but dramatically reduced color saturation. A chrome bumper shows you the shape of the world it reflects, but not its colors: everything is rendered in grayscale or near-grayscale. Chrome simulates this property by attenuating the U and V chroma channels toward their neutral midpoint (512). The attenuation uses ***shift-based division***, stepping through four discrete levels of desaturation. At the strongest setting, chroma is reduced to one-eighth of its original magnitude: barely a whisper of color.

The **Tint** toggle provides an additional dimension: when set to Off, Chrome bypasses the graduated desaturation entirely and forces chroma to dead neutral, producing a pure monochrome output. The warm/cool tint from **Tint Hue** and **Metal** is then applied on top, coloring the neutral chrome surface with a uniform temperature shift.

### Specular Bloom

In the physical world, specular highlights are the blindingly bright reflections of light sources on shiny surfaces: the white-hot spots that slide across a chrome sphere as you move around it. Chrome simulates this with a conditional brightness boost: any pixel whose luminance exceeds a configurable threshold gets an additive kick from the **Bloom** control. The threshold is set by **Blur Amt** (Knob 3), and the strength by **Bloom** (Knob 4).

When the **Invert** toggle (Switch 10) is engaged, the threshold itself gently oscillates with the video frame counter, creating a subtle shimmer effect where the bloom highlights pulse and ripple. This emulates the way real specular reflections dance when the viewing angle or light source shifts slightly.


---

## Signal Flow

### Signal Flow Notes

The Y channel carries most of Chrome's character. Vertical blur softens the luminance first, then the S-curve carves it into high-contrast metal, and finally specular bloom adds the bright glints. The U and V channels are passengers through the first five stages: they pass through pipeline registers, waiting for Stage 6 to apply desaturation and tint. This means the contrast and bloom adjustments affect luminance *before* the chroma channels are processed, so the specular highlights bloom only in brightness, not in color.

The warm/cool tint is applied *after* desaturation, which is a deliberate design choice. Whether the image is fully monochrome (Tint Off) or partially desaturated (Tint On), the tint colors the final result uniformly. This means you can create pure-monochrome gold chrome (Tint Off + Metal Steel + Tint Hue high) or partially colored warm chrome (Tint On + moderate Desat + Metal Steel + Tint Hue).

:::tip
The **Mix** fader blends each channel independently using three parallel interpolators. This means you can dial in a half-strength chrome wash that retains some of the source's original character: useful for a metallic overlay that doesn't fully obliterate the underlying image.
:::


---

## Exercises

These exercises progress from basic contrast sculpting to full liquid-metal scene design. Each builds on the previous, gradually engaging more of Chrome's processing chain.
### Exercise 1: Mirror Finish

![Mirror Finish result](/img/instruments/videomancer/chrome/chrome_ex1_s1.png)
*Mirror Finish — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A high-contrast, monochrome chrome mirror from a camera feed. The goal is to make the image look like a reflection in a polished metal surface.

#### Key Concepts

- S-curve contrast creates the metallic tonal separation
- Desaturation strips color to reveal the chrome surface
- The Curve toggle reverses the contrast direction

#### Video Source

A live camera feed aimed at a scene with varied lighting: a face, a hand, or an object with both bright highlights and deep shadows.

#### Steps

1. Set **Contrast** (Knob 1) to about two-thirds clockwise. The image snaps into a stark, contrasty look (shadows plunge, highlights push toward white.)
2. Set **Tint** (Switch 9) to **Off**. The image becomes fully monochrome (a silver mirror.)
3. Turn **Desat** (Knob 2) to its midpoint. (This won't have a visible effect yet, since Tint is Off, but it prepares for the next exercise.)
4. Toggle **Curve** (Switch 8) to **Clip**. Notice how the image flattens: highlights darken, shadows lighten. This is the inverse S-curve, compressing the tonal range.
5. Toggle **Curve** back to **S-Curve**. The hard, reflective contrast returns.

#### Settings

| Control | Value |
|---------|-------|
| Contrast | ~66% |
| Desat | 50% |
| Blur Amt | 50% |
| Bloom | 0% |
| Reflect | 0% |
| Tint Hue | 0° |
| Metal | Chrome |
| Curve | S-Curve |
| Tint | Off |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Gold Chrome with Specular Bloom

![Gold Chrome with Specular Bloom result](/img/instruments/videomancer/chrome/chrome_ex2_s1.png)
*Gold Chrome with Specular Bloom — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A warm, golden chrome surface with bright specular highlights: the look of a gold-plated trophy or a vintage car's hood ornament.

#### Key Concepts

- Specular bloom adds hot glints to highlights
- Blur Amt and Bloom work together to control the bloom effect
- Metal and Tint Hue shift the chrome toward warm gold

#### Video Source

Footage with distinct bright highlights: a shiny surface, a window reflection, or direct light sources in frame.

#### Steps

1. Start from the Mirror Finish settings (Exercise 1). Set **Contrast** to about two-thirds.
2. Flip **Metal** (Switch 7) to **Steel**. Nothing visible changes yet (Tint Hue is at 0°).
3. Increase **Tint Hue** (Knob 6) to about halfway. The monochrome chrome takes on a warm, golden tone (we are gold-plating the signal.)
4. Lower **Blur Amt** (Knob 3) to about one-third. This sets a low specular threshold (more of the image qualifies for the bloom effect.)
5. Increase **Bloom** (Knob 4) to about halfway. Bright areas now glow with an additive boost, simulating hot specular reflections on the gold surface.
6. Toggle **Invert** (Switch 10) to **On**. The specular highlights begin to pulse gently: the bloom threshold oscillates with the frame counter, adding a living shimmer.

#### Settings

| Control | Value |
|---------|-------|
| Contrast | ~66% |
| Desat | 50% |
| Blur Amt | ~33% |
| Bloom | 50% |
| Reflect | 0% |
| Tint Hue | ~180° |
| Metal | Steel |
| Curve | S-Curve |
| Tint | Off |
| Invert | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Liquid Mercury

![Liquid Mercury result](/img/instruments/videomancer/chrome/chrome_ex3_s1.png)
*Liquid Mercury — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A molten, liquid-mercury surface where the video appears to ripple and flow, with faint traces of the original source color visible through the metallic sheen.

#### Key Concepts

- Vertical blur smooths the luminance into a liquid surface
- Partial desaturation (Tint On) retains ghost color through the metal
- The Mix fader blends chrome with the original for layered looks

#### Video Source

Slow-moving footage with organic shapes: water, clouds, smoke, or a slowly panning camera across textured surfaces.

#### Steps

1. Set **Contrast** (Knob 1) to about halfway for a moderate S-curve.
2. Set **Tint** (Switch 9) to **On**. This enables the graduated desaturation.
3. Turn **Desat** (Knob 2) clockwise to about 75%. Most of the color drains away, but faint hues remain (a ghost of the original palette.)
4. Increase **Reflect** (Knob 5) past the midpoint. The image softens vertically as each line averages with the one above it. Hard edges dissolve into smooth, mercury-like gradients.
5. Set **Bloom** (Knob 4) to about one-third and **Blur Amt** (Knob 3) to about halfway. Moderate specular bloom adds gentle highlights without overwhelming the liquid surface.
6. Pull **Mix** (Fader 12) down to about 60%. The chrome effect blends with the original source, creating a translucent metallic overlay (the source is visible through the liquid metal.)
7. Flip **Metal** (Switch 7) to **Chrome** and increase **Tint Hue** (Knob 6) slightly. A cool blue wash settles over the liquid surface, completing the mercury illusion.

#### Settings

| Control | Value |
|---------|-------|
| Contrast | 50% |
| Desat | ~75% |
| Blur Amt | 50% |
| Bloom | ~33% |
| Reflect | ~66% |
| Tint Hue | ~60° |
| Metal | Chrome |
| Curve | S-Curve |
| Tint | On |
| Invert | Off |
| Bypass | Off |
| Mix | ~60% |

---
## Glossary

- **Bloom**: An additive brightness boost applied selectively to pixels exceeding a luminance threshold, simulating the glare of specular highlights on reflective surfaces.

- **Chroma**: The color information in a video signal, encoded as U and V components in YUV color space; Chrome attenuates chroma toward neutral to simulate metallic reflection.

- **Desaturation**: Reducing the intensity of color channels toward their neutral midpoint, progressively stripping color from the image.

- **Interpolator**: A hardware module that performs linear interpolation between two values; Chrome uses three interpolators for the wet/dry mix crossfade.

- **Line Buffer**: A block RAM that stores one horizontal line of pixel data, enabling comparison or averaging between the current line and the previous line.

- **Luma**: The brightness component (Y) of a YUV video signal; Chrome's S-curve and bloom stages operate exclusively on luma.

- **S-Curve**: A contrast enhancement curve shaped like the letter S, which darkens shadows and brightens highlights while compressing the midtone transition. Named for its resemblance to a sigmoid function.

- **Specular Highlight**: A bright reflection of a light source on a shiny surface; in Chrome, pixels exceeding the specular threshold receive an additive bloom boost.

- **Wet/Dry Mix**: A crossfade between the processed (wet) signal and the original (dry) signal, allowing partial application of an effect.

---
