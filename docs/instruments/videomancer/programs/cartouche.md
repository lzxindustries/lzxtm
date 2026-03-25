---
draft: true
sidebar_position: 38
slug: /instruments/videomancer/cartouche
title: "Cartouche"
image: /img/instruments/videomancer/cartouche/cartouche_hero_s1.png
description: "Ancient Egyptian artists did not paint pictures the way we understand them."
---

![Cartouche hero image](/img/instruments/videomancer/cartouche/cartouche_hero_s1.png)
*Cartouche dividing a video frame into horizontal registers and painting each band with an ancient Egyptian mineral pigment palette.*

---

## Overview

Cartouche is a video effect inspired by the wall paintings of ancient Egyptian tombs: specifically the horizontal ***register system*** that organized nearly all two-dimensional Egyptian art for over three thousand years. The program divides the video frame into two to five horizontal bands (registers), each separated by dark ground lines, and maps the colors in each band to a six-pigment palette modeled after the actual mineral pigments used by ancient Egyptian painters. The result is a striking, layered composition that transforms any video feed into something resembling a painted tomb wall or papyrus scroll.

At default settings, Cartouche applies moderate palette quantization across three registers, producing a subtle posterized look with warm earth tones. Pushing the **Palette Dep** control higher forces colors into hard six-pigment quantization, while the **Color Mode** knob selects different palette subsets: from the full spectrum of mineral pigments to stark black-and-white silhouettes. The **Ground Line** and **Accent Hue** controls add decorative separators and shift the overall hue to taste.

:::tip
Cartouche pairs exceptionally well with programs that generate strong horizontal structure: try placing it after a horizontal mirror or stripe generator to reinforce the register composition.
:::

### What's In a Name?

A ***cartouche*** is the oval frame found on Egyptian temple walls and tomb ceilings that encloses the hieroglyphic spelling of a pharaoh's name. The word entered English via French, where *cartouche* means "cartridge": early European travelers to Egypt thought the oval shape resembled a musket cartridge case. In Egyptology, the cartouche is one of the most recognizable motifs: a protective border that frames a royal identity. The program borrows this idea of framing, dividing the video into bordered horizontal bands just as a cartouche frames its inscription within a defined boundary.

---

## Quick Start

1. Turn **Registers** (Knob 1) fully clockwise to divide the frame into five horizontal bands. You'll see your video split into stacked strips.
2. Increase **Palette Dep** (Knob 3) past the halfway point. Watch the colors in each band snap to flat, mineral-pigment tones (earthy reds, blues, and ochres replace the original colors.)
3. Turn **Separator** (Switch 9) to **Zigzag**. Dark ground lines appear between the registers, completing the tomb-painting look.
4. Sweep **Accent Hue** (Knob 6) slowly. The overall color temperature of the palette shifts (warm ochre tones give way to cooler blues and greens.)

---

## Parameters

![Videomancer front panel with Cartouche loaded](/img/instruments/videomancer/cartouche/cartouche_control_panel.png)
*Videomancer's front panel with Cartouche active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Registers

| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 2 |

**Registers** selects how many horizontal bands the frame is divided into. This is a stepped control with four positions. At position 0 (fully counterclockwise), the frame is split into two registers: a simple top-and-bottom division. Turning clockwise steps through three, four, and five registers. At position 3 (fully clockwise), five equal-height bands tile the frame from top to bottom.

Each register receives its own independent slice of the input video. The number of registers determines how much vertical space each band occupies: five registers on an HD frame gives each band roughly 216 lines, while two registers divide the frame into two halves of about 540 lines each.

---

### Knob 2 — Scroll Spd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Scroll Spd** controls the rate of per-register ***direct digital synthesis*** phase accumulators that run independently for each band. Each register maintains its own DDS accumulator that advances once per frame at a rate set by this knob. At 0%, the accumulators are frozen. As the value increases, they accumulate faster.

:::note
The scroll accumulators are active per-register but the visible effect depends on the output stage. In the current version, this control drives the internal timing infrastructure and may have minimal visible effect on the output image.
:::

---

### Knob 3 — Palette Dep

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Palette Dep** controls the crossfade between the original pixel color and the nearest match in the six-pigment Egyptian palette. At 0%, fully counterclockwise, the original colors pass through unmodified: the palette has no influence. At 100%, fully clockwise, pixel colors are fully replaced by their nearest palette match. Intermediate values produce a smooth blend between the original and the quantized result, letting you dial in just a hint of mineral pigment warmth or push all the way to hard flat color.

The six pigments that make up the palette are carbon black, ***Egyptian blue*** (the world's oldest synthetic pigment, made from cuprorivaite), red ochre, yellow ochre, malachite green, and calcium carbonate white. The nearest match is determined by luminance distance: each pixel is compared against all six palette entries and assigned to the closest one by brightness.

:::tip
Setting Palette Dep around 40–60% creates a watercolor wash effect where the original image shows through the pigment quantization. This can look more natural than the full 100% setting.
:::

---

### Knob 4 — Color Mode

| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

**Color Mode** selects which subset of the six-pigment palette is active. This is a stepped control with four positions:

- **Mode 0** (Full Palette): All six mineral pigments are available. This gives the widest tonal range: from carbon black through the mid-tone reds, greens, and blues to calcium white.
- **Mode 1** (Black & White): Mid-tone pigments are collapsed to either black or white based on a brightness threshold at mid-gray. This produces stark silhouette compositions reminiscent of shadow puppetry.
- **Mode 2** (Warm Palette): Blue and green pigments are replaced by yellow ochre, creating a warm desert palette of blacks, reds, yellows, and whites.
- **Mode 3** (Cool Palette): Red ochre is replaced by Egyptian blue and yellow ochre by malachite green, shifting the palette toward cool mineral tones.

---

### Knob 5 — Ground Line

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Ground Line** controls the thickness of the dark separator lines drawn between registers. At 0%, no ground lines are visible, even when the **Separator** toggle is enabled: the width is zero. As the value increases, the lines become thicker, occupying more scanlines at the top edge of each register band. At 100%, ground lines extend several scanlines into each band, creating pronounced dark bars between registers.

The ground line color is a dark brown-black (slightly warm), inspired by the painted baselines found in Egyptian tomb paintings that separate one narrative register from the next.

---

### Knob 6 — Accent Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Accent Hue** rotates the color of the palette output along the hue axis. At the noon position (default), no rotation is applied. Turning counterclockwise shifts the palette toward warmer tones by increasing the U (blue-difference) component and decreasing the V (red-difference) component. Turning clockwise shifts toward cooler tones by the reverse adjustment. The rotation is applied as a signed offset (±¼ of the full range) to the U and V channels in opposite directions, producing a gentle hue walk without affecting luminance.

:::note
Accent Hue only affects the palette-processed pixels. Ground lines and bypassed pixels are not shifted.
:::

---

### Switch 7 — Scroll Dir

| Property | Value |
|----------|-------|
| Off | Alternate |
| On | Same |
| Default | Alternate |

**Scroll Dir** controls the direction relationship between adjacent register scroll accumulators. In **Alternate** mode (default), odd-numbered registers scroll in the opposite direction from even-numbered ones: a pattern inspired by ***boustrophedon*** writing, where ancient inscriptions alternate reading direction line by line. In **Same** mode, all registers scroll in the same direction.

---

### Switch 8 — Mode Vary

| Property | Value |
|----------|-------|
| Off | Uniform |
| On | Alternate |
| Default | Uniform |

**Mode Vary** selects whether the color mode is applied uniformly across all registers or alternated between adjacent bands. In **Uniform** mode (default), every register uses the same color mode setting from Knob 4. In **Alternate** mode, adjacent registers alternate between the selected mode and the full palette, creating visual variety between bands.

:::note
This control is reserved for a future update and may not produce a visible difference in the current version.
:::

---

### Switch 9 — Separator

| Property | Value |
|----------|-------|
| Off | Plain |
| On | Zigzag |
| Default | Plain |

**Separator** enables or disables the ground line rendering between registers. In **Plain** mode (default), ground lines are not drawn: the register bands sit flush against one another. In **Zigzag** mode, dark separator lines are drawn at the top edge of each register band. The thickness of these lines is set by the **Ground Line** knob (Knob 5).

---

### Switch 10 — Scale Rank

| Property | Value |
|----------|-------|
| Off | Equal |
| On | Graduated |
| Default | Equal |

**Scale Rank** selects whether registers are equal in height or graduated. In **Equal** mode (default), all registers share the same height. In **Graduated** mode, registers are intended to vary in size, with larger bands at the bottom: echoing the ancient Egyptian convention where the lowest register (the foreground) was the most important and received the most space.

:::note
This control is reserved for a future update and may not produce a visible difference in the current version.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Cartouche processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw source and the Egyptian register composition.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the wet/dry crossfade between the original input video and the fully processed Cartouche output. At 0%, fully down, only the original (dry) signal passes through. At 100%, fully up, only the processed (wet) signal is output. Intermediate values blend the two. The crossfade is implemented per-channel (Y, U, and V independently) using three hardware interpolators.

:::tip
A Mix setting around 60–70% lays the mineral pigment palette over the original image with visible transparency, creating the look of a painted overlay on photographic footage (like ancient pigment applied to a modern photograph.)
:::

---

## Background

### Ancient Egyptian Register Painting

For thirty centuries, nearly all Egyptian two-dimensional art: from tomb walls to papyrus scrolls to coffin decorations: was organized according to the ***register system***. The picture surface was divided into horizontal bands separated by straight ground lines, with each band (register) containing an independent scene or narrative episode. Registers were read from bottom to top: the lowest band depicted the foreground (near events, earthly activities), while upper bands depicted the background (distant events, divine encounters). Within each register, figures and objects were arranged along the ground line without atmospheric perspective or cast shadows. Scale indicated importance, not distance: a pharaoh towered over servants regardless of their relative positions.

This compositional system is one of the most visually distinctive features of Egyptian art, immediately recognizable across thousands of years and hundreds of sites. Cartouche translates its key structural elements: horizontal division, ground lines, mineral pigment palette: into real-time video processing.

### The Six Mineral Pigments

The ancient Egyptian artist's palette was remarkably consistent across millennia, built from minerals and compounds that were locally available or easily traded. Cartouche models six of these pigments:

- **Carbon black**: made from soot or charcoal; used for outlines, text, and hair
- **Egyptian blue** (cuprorivaite): the world's first synthetic pigment, manufactured by heating silica, lime, copper, and natron; reserved for skies, water, and divine figures
- **Red ochre**: iron oxide earth pigment; used for skin tones of male figures and decorative borders
- **Yellow ochre**: hydrated iron oxide; used for skin tones of female figures, sand, and grain
- **Malachite green**: copper carbonate mineral; used for vegetation, papyrus reeds, and fertility symbols
- **Calcium carbonate white**: ground limestone or gypsum; used as the background ground and for garments


---

## Signal Flow

### Signal Flow Notes

The core processing chain is five pipeline stages followed by a four-clock interpolator, totaling nine clocks of latency. The frame is divided into registers by comparing the vertical line counter against the computed register height (`v_active / N`), using a chain of comparisons rather than runtime division.

Palette matching is done by ***luminance distance***: the pipeline compares the input pixel's Y value against all six palette entries and selects the closest one. This means the match is entirely brightness-based: a bright pixel will snap to yellow ochre or white regardless of its original hue. The U and V channels are then replaced by the selected palette entry's fixed chrominance values, producing flat mineral-pigment color. The blend amount (Palette Dep) controls how much of this replacement actually reaches the output.

:::tip
Because palette matching is luminance-only, high-contrast source material with a wide dynamic range produces the most varied and visually interesting palette mappings. Flat or low-contrast input tends to collapse onto one or two pigments.
:::


---

## Exercises

These exercises progress from basic register division to full Egyptian tomb wall composition. Each builds on the previous one, gradually layering more of Cartouche's processing stages.
### Exercise 1: Register Division and Palette

![Register Division and Palette result](/img/instruments/videomancer/cartouche/cartouche_ex1_s1.png)
*Register Division and Palette — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A multi-band composition with flat Egyptian pigment colors (the foundation of the tomb-painting look.)

#### Key Concepts

- Register division splits the frame into horizontal bands
- Palette quantization maps video colors to mineral pigments
- Color modes select palette subsets for different tonal character

#### Video Source

A live camera feed or recorded footage with a range of brightness levels (faces, landscapes, or still life work well.)

#### Steps

1. **Two registers**: Set **Registers** (Knob 1) fully counterclockwise. The frame splits into a top half and bottom half (two simple bands.)
2. **Apply palette**: Increase **Palette Dep** (Knob 3) to about 80%. Colors snap to the six-pigment mineral palette. Notice how skin tones shift toward red or yellow ochre, skies toward Egyptian blue, and shadows toward carbon black.
3. **Full registers**: Turn Registers clockwise through all four steps (2, 3, 4, 5 bands). At five registers, the bands are narrow strips, each showing its own slice of the image.
4. **Color mode sweep**: Turn **Color Mode** (Knob 4) through its four positions. Mode 0 gives the full palette. Mode 1 collapses to stark black and white silhouettes. Mode 2 is warm desert tones. Mode 3 is cool mineral blues and greens.
5. **Partial blend**: Reduce Palette Dep to about 40%. The original colors show through the pigment overlay, creating a watercolor wash.

#### Settings

| Control | Value |
|---------|-------|
| Registers | 3 (fully clockwise) |
| Scroll Spd | 0% |
| Palette Dep | 80% |
| Color Mode | 0 (Full Palette) |
| Ground Line | 0% |
| Accent Hue | 0° |
| Scroll Dir | Alternate |
| Mode Vary | Uniform |
| Separator | Plain |
| Scale Rank | Equal |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Ground Lines and Accent Color

![Ground Lines and Accent Color result](/img/instruments/videomancer/cartouche/cartouche_ex2_s1.png)
*Ground Lines and Accent Color — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A register composition with dark separator lines and a shifted color palette (closer to the look of actual painted tomb walls.)

#### Key Concepts

- Ground lines separate registers, completing the tomb-wall structure
- Accent Hue rotates the palette color along the hue axis
- Mix blends the processed image with the original for transparency effects

#### Video Source

Footage with moderate contrast and a variety of colors (outdoor scenes or colorful still life subjects.)

#### Steps

1. **Base setup**: Set **Registers** to 3 (three bands), **Palette Dep** to 70%, **Color Mode** to 0 (Full Palette).
2. **Enable ground lines**: Flip **Separator** (Switch 9) to **Zigzag**. Dark lines appear between the register bands.
3. **Thicken the lines**: Increase **Ground Line** (Knob 5) from 0% toward 50%. The dark separator bars grow wider, filling more of each band boundary.
4. **Shift the hue**: Sweep **Accent Hue** (Knob 6) slowly across its full range. The palette warms and cools as the U and V channels rotate. Find a position where the palette feels especially "Egyptian" (usually somewhere in the warm ochre range.)
5. **Translucent overlay**: Lower **Mix** (Fader 12) to about 65%. The original source shows through the processed registers, creating a look of painted pigment over photographic texture.

#### Settings

| Control | Value |
|---------|-------|
| Registers | 1 (midpoint, three bands) |
| Scroll Spd | 0% |
| Palette Dep | 70% |
| Color Mode | 0 (Full Palette) |
| Ground Line | 50% |
| Accent Hue | ~90° |
| Scroll Dir | Alternate |
| Mode Vary | Uniform |
| Separator | Zigzag |
| Scale Rank | Equal |
| Bypass | Off |
| Mix | 65% |

---

### Exercise 3: Full Tomb Wall Composition

![Full Tomb Wall Composition result](/img/instruments/videomancer/cartouche/cartouche_ex3_s1.png)
*Full Tomb Wall Composition — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A five-register Egyptian tomb wall composition with full palette saturation, thick separator lines, accent color, and partial transparency (the most complete Cartouche effect.)

#### Key Concepts

- Combining all processing stages reproduces the layered structure of Egyptian wall paintings
- Black-and-white silhouette mode creates dramatic contrast between registers
- Thick ground lines and strong palette saturation complete the ancient look

#### Video Source

Footage featuring human figures or objects with clear outlines: dancers, performers, or people moving against a plain background produce the most striking Egyptian silhouette quality.

#### Steps

1. **Five registers**: Set **Registers** (Knob 1) to fully clockwise. Five narrow bands stack from top to bottom.
2. **Full palette**: Push **Palette Dep** (Knob 3) to 100%. Complete mineral pigment quantization.
3. **Enable separators**: Flip **Separator** (Switch 9) to **Zigzag** and set **Ground Line** (Knob 5) to about 40%. Dark bars divide each band.
4. **Warm accent**: Set **Accent Hue** (Knob 6) to about 60°. The palette takes on a warm golden quality reminiscent of sandstone and firelight.
5. **Silhouette mode**: Switch **Color Mode** (Knob 4) to Mode 1 (Black & White). The five bands collapse to stark silhouettes: dark figures against bright backgrounds. Now switch back to Mode 0 (Full Palette) to compare.
6. **Blend**: Set **Mix** (Fader 12) to about 80%. A trace of the original video shows through the painted register composition.
7. **Compare**: Use **Bypass** (Switch 11) to toggle between the raw input and the tomb wall. The transformation is dramatic.

#### Settings

| Control | Value |
|---------|-------|
| Registers | 3 (fully clockwise, five bands) |
| Scroll Spd | 0% |
| Palette Dep | 100% |
| Color Mode | 0 (Full Palette) |
| Ground Line | 40% |
| Accent Hue | ~60° |
| Scroll Dir | Alternate |
| Mode Vary | Uniform |
| Separator | Zigzag |
| Scale Rank | Equal |
| Bypass | Off |
| Mix | 80% |

---
## Glossary

- **Boustrophedon**: An ancient writing system in which alternate lines read in opposite directions: left-to-right, then right-to-left: like the path of an ox plowing a field.

- **Cartouche**: An oval frame used in ancient Egyptian art to enclose the hieroglyphic spelling of a royal name; from the French word for "cartridge."

- **DDS (Direct Digital Synthesis)**: A technique for generating waveforms or offsets using a phase accumulator incremented at a fixed rate each frame or sample.

- **Egyptian Blue**: The world's oldest known synthetic pigment, a calcium copper silicate (cuprorivaite) manufactured in Egypt from at least 2500 BC.

- **Ground Line**: A horizontal baseline in Egyptian register painting that separates one narrative band from the next and provides a surface on which figures stand.

- **Interpolator**: A hardware component that computes a weighted blend between two input values, used here for wet/dry crossfading.

- **Luminance Distance**: A simple metric comparing two colors by the absolute difference of their brightness (Y) values, ignoring hue and saturation.

- **Palette Quantization**: The process of mapping each pixel's color to the nearest entry in a fixed set of colors, reducing the image to a limited palette.

- **Register (Art History)**: A horizontal band in a two-dimensional composition, used in Egyptian art to organize multiple scenes on a single surface.

---
