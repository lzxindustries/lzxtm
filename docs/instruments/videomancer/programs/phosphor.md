---
draft: true
sidebar_position: 226
slug: /instruments/videomancer/phosphor
title: "Phosphor"
image: /img/instruments/videomancer/phosphor/phosphor_hero_s1.png
description: "Phosphor recreates the look of analogue CRT monitors — the faint glow bleeding rightward from bright edges, the dark scanline gaps between rows, and the characteristic colour of a phosphor screen."
---

![Phosphor hero image](/img/instruments/videomancer/phosphor/phosphor_hero_s1.png)
*Phosphor simulating a glowing green CRT monitor with visible scanlines, bloom glow, and edge-darkened vignette across a live camera feed.*

---

## Overview

Phosphor transforms any video signal into a convincing cathode ray tube display. The classic CRT look is built from four layers: a brightness and contrast gain stage, visible scanline structure, a rightward bloom glow that smears bright pixels horizontally, and a monochrome phosphor tint that recolors the entire image. Combined, these stages recreate the warm, luminous character of vintage monitors ranging from green-screen terminals to amber oscilloscopes to arcade vector displays.

At conservative settings, Phosphor adds a subtle retro warmth: gentle scanlines and a hint of bloom on highlights. Crank the controls and the image dissolves into a glowing wireframe world, especially with **Hi Contrast** enabled to force the luminance into pure black-and-white before the glow stage. The **Mix** fader lets you blend between the raw input and the full CRT treatment, making Phosphor useful as both a dramatic effect and a tasteful finishing touch.

### What's In a Name?

A ***phosphor*** is the chemical coating on the inside face of a cathode ray tube. When struck by the electron beam, it glows: and different phosphor compounds produce different colors. The CRT industry assigned standard designations: P1 (green), P4 (white), P7 (amber), P31 (blue-white), and many more. Phosphor recreates eight of these classic tints in silicon, letting you choose the glow color of your virtual tube.

---

## Quick Start

1. Turn **Scanlines** (Knob 4) to about 60%. Watch as alternating dark lines appear across the image, instantly suggesting a low-resolution CRT.
2. Increase **Bloom** (Knob 3) past 50%. Bright areas develop a rightward glow trail, as if the electron beam is leaving a luminous wake across the screen.
3. Rotate **Phosphor** (Knob 5) through the eight presets. The entire image shifts through green, white, amber, blue-white, and more (each one a different species of vintage monitor.)
4. Enable **Vignette** (Switch 9). The edges of the frame darken, completing the illusion of a convex glass screen.

---

## Parameters

![Videomancer front panel with Phosphor loaded](/img/instruments/videomancer/phosphor/phosphor_control_panel.png)
*Videomancer's front panel with Phosphor active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Brightness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Brightness** adds or removes a DC offset from the luminance channel after contrast scaling. At 50%, the offset is zero and brightness passes through unchanged. Turning below 50% darkens the entire image toward black. Turning above 50% lifts the image toward white. Brightness interacts with **Contrast**: increasing contrast with low brightness produces deep, inky shadows, while high brightness with moderate contrast gives the washed-out look of an overdriven CRT.

---

### Knob 2 — Contrast

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Contrast** scales the luminance signal before all other processing. At 0%, the image is crushed to black. At 50%, the signal passes through at unity gain. At 100%, luminance is doubled, pushing highlights into clipping. Contrast is the first stage in the pipeline, so it controls the overall dynamic range that all subsequent stages: scanlines, bloom, phosphor tint: operate on.

:::tip
Setting Contrast above 75% with **Hi Contrast** off produces a hot, overdriven look where highlights clip and bloom trails become more intense. This mimics a CRT running at elevated beam current.
:::

---

### Knob 3 — Bloom

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Bloom** controls the strength of a horizontal ***IIR*** glow that spreads bright pixels to the right. At 0%, bloom is disabled and the image is sharp. At low values, a subtle glow softens bright edges. At 25%, each bright pixel blends equally with its neighbor. At higher values, the glow trail extends further and further to the right, creating long luminous streaks from highlights. The bloom filter operates as a one-pole IIR that retains up to 94% of the previous pixel's brightness at maximum.

:::note
Bloom spreads only to the ***right***. This is deliberate: on a real CRT, the electron beam scans left-to-right, and phosphor persistence causes the glow trail to follow the beam direction.
:::

---

### Knob 4 — Scanlines

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Scanlines** controls the depth of the scanline darkening effect. At 0%, all lines pass through at full brightness: scanlines are invisible. As the value increases, alternating lines are progressively darkened, producing the characteristic horizontal stripe pattern of a low-resolution CRT. At 100%, the dark lines are almost black, creating a bold, high-contrast raster look. The pattern of dark lines depends on the **Scan Mode** setting.

---

### Knob 5 — Phosphor

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

**Phosphor** selects one of eight color presets that tint the monochrome output. Positions 0 through 6 correspond to historical CRT phosphor types, each with a fixed hue. Position 7 activates the **Custom Hue** control, letting you dial in any tint you like. Stepping through the presets changes the overall color of the image: green terminal, white television, amber instrument, blue-tinged lab monitor, and more.

---

### Knob 6 — Custom Hue

| Property | Value |
|----------|-------|
| Range | -180° – 180° |
| Default | -120° |

**Custom Hue** sets the phosphor tint color when **Phosphor** (Knob 5) is set to position 7 (Custom). The control sweeps through four quadrants of the color wheel: red-yellow, yellow-green, green-cyan, and cyan-red. At any other Phosphor preset position, this control has no visible effect.

---

### Switch 7 — Scan Mode

| Property | Value |
|----------|-------|
| Off | Alternate |
| On | Triple |
| Default | Alternate |

**Scan Mode** selects the scanline pattern. In the **Alternate** position, every other line is darkened, producing a classic 2-line repeating pattern. In the **Triple** position, every third line is darkened, creating a wider gap between dark lines. The Triple mode is subtler and preserves more vertical resolution, while Alternate mode produces a more dramatic, retro-looking stripe.

---

### Switch 8 — Bloom Axis

| Property | Value |
|----------|-------|
| Off | H Only |
| On | H+V |
| Default | H Only |

**Bloom Axis** controls whether the bloom glow operates in one dimension or two. In the **H Only** position, bloom spreads only horizontally, creating rightward glow trails. In the **H+V** position, the bloom from the previous scanline carries over to seed the current line's glow, producing a soft vertical smear in addition to the horizontal spread. The result is a warmer, more diffuse glow that wraps around bright areas.

---

### Switch 9 — Vignette

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Vignette** enables an edge-darkening effect that simulates the falloff at the edges of a curved CRT screen. With the switch **On**, the left and right edges of the image darken progressively: hard darkening at the extreme edges, graduating to a subtle reduction further in. The center of the image is unaffected. This completes the CRT illusion by mimicking the way a real curved glass screen loses brightness toward the corners.

---

### Switch 10 — Hi Contrast

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Hi Contrast** forces the luminance channel into a 1-bit black-and-white image before scanlines and bloom are applied. Any pixel brighter than mid-gray becomes full white; anything darker becomes black. This transforms the image into a stark vector-display look, perfect for recreating the appearance of early arcade games like Asteroids or Battlezone. The bloom glow then softens the hard edges, producing luminous beam traces on a black background.

:::tip
**Hi Contrast** is the key to the vector display aesthetic. Enable it, set **Phosphor** to Green, increase **Bloom** to 70%, and the result looks like a genuine monochrome vector monitor.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Phosphor processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the CRT-processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) signal and the wet (Phosphor-processed) signal. At 0%, only the dry signal passes through. At 100%, only the processed signal is heard. Intermediate values blend the two, which can be useful for adding a hint of CRT warmth without committing to the full effect.

---

## Background

### The cathode ray tube

The ***cathode ray tube*** dominated visual display technology for over a century, from early oscilloscopes in the 1890s to the last CRT televisions manufactured in the 2010s. Inside the glass envelope, an electron gun fires a focused beam at a phosphor-coated screen. The beam scans left to right, top to bottom, painting one line at a time. Where it strikes, the phosphor glows: and different chemical compounds produce different colors of light. The CRT's characteristic visual qualities: visible scan lines, soft glow on bright areas, color tinting, and edge falloff: are not flaws but byproducts of the physics of electron beams and phosphor chemistry.

### Phosphor types and color

CRT manufacturers developed dozens of phosphor formulations, each assigned a ***P-number*** designation. P1 (zinc silicate) glowed green and was used in early radar displays and oscilloscopes. P4 (a mix of blue and yellow phosphors) produced white light for broadcast television. P7 (zinc sulfide) gave a distinctive amber-orange used in long-persistence radar screens. P31 emitted a blue-white flash for high-speed oscillographic recording. Phosphor recreates seven of these historical formulations as fixed presets, plus one custom slot that lets you dial any hue.

### Beam bloom and persistence

When the electron beam hits a bright area, the phosphor glows more intensely: and that glow spills outward. On a real CRT, this ***bloom*** effect causes bright objects to appear slightly larger and softer than dark ones. Phosphor simulates this with a horizontal ***infinite impulse response*** filter that accumulates brightness from left to right, mimicking the beam's scanning direction. The filter retains a configurable fraction of each pixel's brightness into the next pixel, creating a rightward glow trail whose length depends on the Bloom setting.


---

## Signal Flow

### Signal Flow Notes

The pipeline is luminance-dominant. All five Y-channel stages run in sequence: contrast, brightness, scanline, bloom, and vignette. The U and V channels are replaced entirely by the selected phosphor preset values: the input chrominance is discarded and replaced with fixed tint coordinates. This means the output is always monochrome (within the selected phosphor hue), regardless of the input's color content.

:::note
Because the phosphor tint replaces chroma entirely, colorful inputs will appear monochromatic. To retain some input color, use the **Mix** fader to blend between the dry and wet paths.
:::

The **Hi Contrast** clamp occurs after contrast scaling but before scanline darkening. This means scanning and bloom operate on the binary-quantized signal, which produces distinctly different glow behavior compared to continuous-tone input.


---

## Exercises

These exercises progress from basic CRT styling to full vector display recreation. Each builds on the previous, engaging more of the processing pipeline.
### Exercise 1: Retro Monitor

![Retro Monitor result](/img/instruments/videomancer/phosphor/phosphor_ex1_s1.png)
*Retro Monitor — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A green-screen terminal look with visible scanlines and darkened edges.

#### Key Concepts

- Scanline darkening recreates low-resolution raster structure
- Phosphor tint recolors the image to match a historical CRT type
- Vignette adds edge falloff for screen curvature

#### Video Source

A camera feed with clearly visible subjects (faces, objects, or text work well.)

#### Steps

1. **Set the tint**: Rotate **Phosphor** (Knob 5) to position 0 (P1 Green). The image takes on a green monochrome hue.
2. **Add scanlines**: Increase **Scanlines** (Knob 4) to about 60%. Alternating dark lines appear.
3. **Darken edges**: Enable **Vignette** (Switch 9). The left and right edges of the frame darken.
4. **Adjust brightness**: Turn **Brightness** (Knob 1) up slightly above center. The overall image lifts, mimicking a CRT with the brightness knob turned up.

#### Settings

| Control | Value |
|---------|-------|
| Brightness | ~55% |
| Contrast | ~50% |
| Bloom | ~0% |
| Scanlines | ~60% |
| Phosphor | 0 (P1 Green) |
| Custom Hue | ~50% |
| Scan Mode | Alternate |
| Bloom Axis | H Only |
| Vignette | On |
| Hi Contrast | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 2: Bloom Trails

![Bloom Trails result](/img/instruments/videomancer/phosphor/phosphor_ex2_s1.png)
*Bloom Trails — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A warm amber monitor with prominent glow trails streaming from bright areas.

#### Key Concepts

- Horizontal IIR bloom creates directional glow from bright pixels
- Bloom Axis adds vertical smearing when set to H+V
- Contrast and Bloom interact to control glow intensity

#### Video Source

High-contrast footage: bright lights against dark backgrounds, candle flames, or stage lighting.

#### Steps

1. **Select amber**: Rotate **Phosphor** (Knob 5) to position 2 (P7 Amber). The image turns warm orange.
2. **Increase contrast**: Turn **Contrast** (Knob 2) to about 65%. Highlights push toward clipping, creating strong bloom sources.
3. **Add bloom**: Increase **Bloom** (Knob 3) to about 70%. Bright areas develop long rightward glow trails that smear across the screen.
4. **Enable vertical bloom**: Set **Bloom Axis** (Switch 8) to **H+V**. The glow broadens vertically, wrapping around bright spots.
5. **Add scanlines**: Set **Scanlines** (Knob 4) to about 40% for subtle line structure over the glow.

#### Settings

| Control | Value |
|---------|-------|
| Brightness | ~50% |
| Contrast | ~65% |
| Bloom | ~70% |
| Scanlines | ~40% |
| Phosphor | 2 (P7 Amber) |
| Custom Hue | ~50% |
| Scan Mode | Alternate |
| Bloom Axis | H+V |
| Vignette | Off |
| Hi Contrast | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 3: Vector Arcade Display

![Vector Arcade Display result](/img/instruments/videomancer/phosphor/phosphor_ex3_s1.png)
*Vector Arcade Display — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A glowing vector display reminiscent of 1979-era arcade cabinets like Asteroids or Battlezone.

#### Key Concepts

- Hi Contrast reduces the image to 1-bit before the glow stage
- Strong bloom on binary edges produces a vector CRT aesthetic
- Phosphor preset and Custom Hue colorize the beam traces

#### Video Source

Footage with strong edges and geometric shapes (architecture, text, or graphic patterns.)

#### Steps

1. **Enable vector mode**: Turn on **Hi Contrast** (Switch 10). The image snaps to pure black and white.
2. **Set green phosphor**: Rotate **Phosphor** (Knob 5) to position 0 (P1 Green).
3. **Increase bloom**: Set **Bloom** (Knob 3) to about 80%. The white edges now glow with a soft green halo.
4. **Add vertical bloom**: Set **Bloom Axis** (Switch 8) to **H+V** for thicker, more atmospheric beam traces.
5. **Adjust contrast**: Fine-tune **Contrast** (Knob 2) to control which edges trigger the white threshold.
6. **Add scanlines**: Set **Scanlines** (Knob 4) to about 30% for a subtle grid across the glow.
7. **Darken edges**: Enable **Vignette** (Switch 9) for the full arcade cabinet illusion.

#### Settings

| Control | Value |
|---------|-------|
| Brightness | ~50% |
| Contrast | ~60% |
| Bloom | ~80% |
| Scanlines | ~30% |
| Phosphor | 0 (P1 Green) |
| Custom Hue | ~50% |
| Scan Mode | Alternate |
| Bloom Axis | H+V |
| Vignette | On |
| Hi Contrast | On |
| Bypass | Off |
| Mix | ~100% |

---
## Glossary

- **Bloom**: A glow effect where bright pixels spread light into neighboring pixels, simulating phosphor overload on a CRT.

- **CRT**: Cathode Ray Tube; a vacuum tube display technology using an electron beam to excite phosphor coatings on a glass screen.

- **IIR**: Infinite Impulse Response; a filter type where the output feeds back into the input, creating exponentially decaying trails.

- **Phosphor**: A chemical compound that emits light when struck by the electron beam in a CRT; different compounds produce different colors.

- **Scanline**: A single horizontal line traced by the electron beam across the screen; visible scanlines are the dark gaps between active lines.

- **Vector Display**: A CRT display mode where the beam draws lines directly between points rather than scanning a raster grid, used in early arcade games.

- **Vignette**: Darkening at the edges of an image, simulating the brightness falloff at the periphery of a curved CRT screen.

---
