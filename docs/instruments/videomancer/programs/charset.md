---
draft: true
sidebar_position: 43
slug: /instruments/videomancer/charset
title: "Charset"
image: /img/instruments/videomancer/charset/charset_hero_s1.png
description: "Every screen you have ever read — every terminal, every text editor, every status display — renders characters on a fixed grid."
---

![Charset hero image](/img/instruments/videomancer/charset/charset_hero_s1.png)
*Input video rendered as density-mapped glyph patterns on an eight-by-eight cell grid, evoking vintage terminal displays and dot-matrix character art.*

---

## Overview

Charset transforms live video into a mosaic of geometric ***glyph*** patterns, as if the image were being rendered on a vintage character display. The screen is divided into a grid of 8×8 pixel cells. Within each cell, the input luminance is sampled and mapped to one of eight density levels, each rendered as a distinct geometric pattern: from a single lit corner pixel for the darkest tones to a fully filled block for the brightest. The result is a halftone-like rendering where image brightness is expressed through the density of lit pixels, not through continuous tonal gradation.

At its gentlest, Charset adds a subtle structured texture to the image, a pixelated film grain. At full strength, it reduces video to stark geometric abstractions that recall the era of character ROMs and phosphor terminals. Color can pass through from the source or be stripped to monochrome. Grid lines at cell boundaries can be drawn to emphasize the tiled structure. A wet/dry mix fader allows any blend between the raw input and the processed output.

:::tip
Charset is at its most expressive when the source material has strong ***tonal contrast***: bright highlights and deep shadows produce a wide range of density patterns across the grid, making the image content readable through the glyph layer.
:::

### What's In a Name?

A ***charset***: short for ***character set***: is the complete library of glyphs stored in a computer's character ROM. In vintage systems like the Commodore 64, Apple II, and VT100 terminal, every letter, number, and symbol was defined as an 8×8 pixel bitmap in a read-only memory chip. The program borrows that grid geometry and the idea of rendering arbitrary content through a fixed set of tile patterns. Instead of letters, Charset's patterns are abstract density fills: but the spirit is the same: the world expressed through an 8×8 window.

---

## Quick Start

1. Feed a video source with recognizable features: a face, a hand, or geometric shapes work well. You'll see the image immediately transformed into a grid of small geometric patterns. Brighter areas appear as dense fills; darker areas are sparse or empty.
2. Turn **Brightness** (Knob 3) clockwise and counterclockwise. This controls how bright the lit pixels in each glyph are. At low values, the patterns are dim; at high values, they glow.
3. Flip the **Invert** toggle (Switch 7) to **On**. The density mapping reverses: bright regions become sparse and dark regions become dense, like a photographic negative rendered in tile patterns.
4. Flip **Grid Lines** (Switch 9) to **On**. Thin bright lines appear at every cell boundary, emphasizing the tiled structure. The image now resembles a terminal or LED matrix display.

---

## Parameters

![Videomancer front panel with Charset loaded](/img/instruments/videomancer/charset/charset_control_panel.png)
*Videomancer's front panel with Charset active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Cell Size

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

**Cell Size** selects the pixel dimensions of each character cell. At the default value, cells are 8×8 pixels: the classic character ROM geometry. This parameter is reserved for future expansion to additional cell sizes.

:::note
In the current implementation, cells are fixed at 8×8 pixels regardless of this knob's position.
:::

---

### Knob 2 — Threshold

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Threshold** sets a luminance cutoff for the density mapping. This parameter is reserved for future implementation of a brightness gate that would force cells below the threshold to render as empty.

:::note
In the current implementation, this knob has no visible effect. Density mapping uses the full luminance range.
:::

---

### Knob 3 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |

**Brightness** controls the luminance of lit pixels within each glyph pattern. When a pattern pixel is "on," this parameter determines how bright it appears. At 0%, fully counterclockwise, the lit pixels are dim: nearly as dark as the unlit background. At 100%, fully clockwise, the lit pixels are at maximum brightness. The default is moderately bright, producing good contrast against the near-black background of unlit pixels.

The unlit pixels always render at a fixed near-black level (approximately 6% of full scale), so **Brightness** effectively controls the contrast ratio of the glyph pattern. Higher values create hard, punchy graphics reminiscent of a monochrome CRT. Lower values create a ghostly, barely-visible texture.

---

### Knob 4 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contrast** is intended to apply gain to the glyph output, adjusting the tonal range of the rendered patterns. This parameter is reserved for future implementation.

:::note
In the current implementation, this knob has no visible effect.
:::

---

### Knob 5 — Font Weight

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Font Weight** is intended to control the thickness or fill density of the glyph patterns, simulating the difference between light and bold typefaces. This parameter is reserved for future implementation.

:::note
In the current implementation, this knob has no visible effect. See the **Bold** toggle (Switch 10) for a related feature.
:::

---

### Knob 6 — Spacing

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Spacing** is intended to control the gap between adjacent character cells, inserting blank columns or rows between glyphs. This parameter is reserved for future implementation.

:::note
In the current implementation, this knob has no visible effect. Use the **Grid Lines** toggle (Switch 9) to visually separate cells.
:::

---

### Switch 7 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** reverses the density mapping. With Invert set to **Off**, bright input regions produce dense fill patterns and dark regions produce sparse patterns: the natural mapping. With Invert set to **On**, the relationship flips: dark regions fill densely and bright regions become sparse. This is not a simple luminance inversion: it is an inversion of the *pattern selection logic*, so the geometric character of each density level is preserved but assigned to the opposite end of the tonal scale.

:::tip
**Invert** interacts with **Grid Lines**: when both are enabled, the grid lines remain bright regardless of inversion, creating a lattice that frames the inverted density fills.
:::

---

### Switch 8 — Mono

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mono** strips all color information from the output. With Mono set to **Off**, the chroma (U and V) channels pass through from the source, so the glyph patterns are rendered in the original colors of the input video. With Mono set to **On**, chroma is forced to neutral (midpoint), producing a purely monochrome output. The glyph patterns appear as shades of gray: or, more precisely, as a single brightness level (set by **Brightness**) against a near-black background, with no color tinting.

---

### Switch 9 — Grid Lines

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Grid Lines** draws thin bright lines at every cell boundary, outlining the 8×8 grid across the entire frame. The grid lines appear at the first pixel of each row and column within a cell (`local_x = 0` or `local_y = 0`), creating a one-pixel-wide lattice. When enabled, the grid overlays on top of the density patterns: a cell that would otherwise be empty still shows its boundary lines. This emphasizes the tiled structure and gives the output a distinctly digital, terminal-like appearance.

---

### Switch 10 — Bold

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bold** is intended to thicken the glyph patterns within each cell, adding adjacent pixels to create heavier strokes. This parameter is reserved for future implementation.

:::note
In the current implementation, this toggle has no visible effect.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Charset processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the character-mapped result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the wet/dry blend between the original input video and the processed glyph output. At 0%, fully down, the output is the unprocessed input: identical to engaging **Bypass**. At 100%, fully up, the output is entirely the character-mapped result. Intermediate positions create a translucent overlay where the glyph patterns are superimposed on the source video. The mix is applied independently to all three channels (Y, U, V) via matched ***interpolator*** stages.

:::tip
At around 50% mix, the glyph grid becomes a visible texture layered over the original image: useful for adding a subtle digital patina without fully replacing the source.
:::

---

## Background

### Character ROMs and tile graphics

The earliest personal computers and video terminals rendered text and graphics using ***character ROMs***: read-only memory chips containing a library of small pixel bitmaps, typically 8×8 pixels each. Every character on the screen was a lookup into this ROM: the system stored only a grid of character codes, and the display hardware fetched the corresponding bitmap for each cell on every scan line. This architecture was astonishingly efficient: a full screen of 40×25 characters required only 1,000 bytes of RAM, while the pixel data was generated on the fly from a shared ROM.

The aesthetic of character-based graphics has a distinctive quality: hard pixel edges, a rigid grid, and a limited vocabulary of shapes. These constraints forced creative solutions. Artists working within character ROM systems developed techniques for composing complex images from simple tile building blocks: a practice that became known as ***PETSCII art*** on Commodore systems and ***ASCII art*** on terminals.

### Density mapping and halftoning

Charset uses a form of ***density mapping*** to represent continuous-tone images through the binary language of on/off pixels. The principle is the same one underlying newspaper halftones and laser printer dithering: the human visual system perceives a cluster of small dots as a shade of gray, with denser clusters reading as darker tones and sparser clusters reading as lighter tones.

In traditional halftoning, dot size varies continuously. Charset instead uses a fixed vocabulary of eight discrete patterns: from an empty cell to a fully filled one, with six intermediate densities based on checkerboards, grids, and logical combinations of pixel coordinates. The visual effect resembles an ordered ***dither matrix***, but generated procedurally from bit-level logic rather than from a lookup table.

### Pattern generation

Each of the eight density levels is generated by a different Boolean combination of the three least-significant bits of the local X and Y coordinates within a cell:

| Density | Logic | Visual |
|---------|-------|--------|
| 0 (darkest) | Always off | Empty cell |
| 1 | `x(2) AND y(2)` | Single corner pixel |
| 2 | `x(1) XOR y(1)` | Coarse 2×2 checkerboard |
| 3 | `x(1) AND y(1)` | Coarse 2×2 dots |
| 4 | `x(0) XOR y(0)` | Fine 1×1 checkerboard |
| 5 | `x(0) OR y(0)` | Fine grid (¾ fill) |
| 6 | `x(0) NAND y(0)` | Inverse dot (¾ fill) |
| 7 (brightest) | Always on | Solid fill |

The density level is selected by the three most significant bits of the held luminance sample (`s_held_y(9 downto 7)`), dividing the 10-bit luminance range into eight equal bands.


---

## Signal Flow

### Signal Flow Notes

The key architectural feature is the ***sample and hold*** at cell boundaries. Luminance is sampled only when `local_x` wraps from 7 to 0: the first pixel of each new cell column. This held value determines the density pattern for the entire 8×8 cell, so the glyph pattern is uniform within each tile regardless of how the source luminance varies across the cell's interior. This is what gives Charset its character ROM aesthetic: each cell displays a single glyph, not a continuous gradient.

The chroma path is simpler than the luminance path. When **Mono** is off, U and V pass through from the source unchanged: the glyph patterns are "painted" with whatever color the source provides. The density patterns affect only the Y channel decision (Brightness vs. near-black), so color appears wherever a pattern pixel is lit. When **Mono** is on, both U and V are clamped to midpoint (512), removing all color and producing a monochrome result.

:::note
The sync delay pipeline (8-clock shift register) keeps the original video data aligned with the processed output. The interpolator mix operates on the delayed data and the processed data, ensuring correct timing at the output.
:::


---

## Exercises

These exercises progress from basic density visualization to creative compositing, gradually engaging the grid, chroma, and mix controls.
### Exercise 1: Terminal Display

![Terminal Display result](/img/instruments/videomancer/charset/charset_ex1_s1.png)
*Terminal Display — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A monochrome terminal display effect: bright text-like patterns against a dark background with visible cell boundaries.

#### Key Concepts

- Luminance maps to glyph density: bright = dense, dark = sparse
- Brightness controls the intensity of lit pixels
- Grid Lines add a structural lattice

#### Video Source

A live camera feed or recorded footage with a face or hand, providing strong tonal contrast.

#### Steps

1. **Observe the default**: With default settings, the input is already rendered as density-mapped glyphs. Notice how bright areas of the source produce filled cells and dark areas produce sparse or empty cells.
2. **Go monochrome**: Flip **Mono** (Switch 8) to **On**. All color is stripped (the image is now pure brightness patterns.)
3. **Add the grid**: Flip **Grid Lines** (Switch 9) to **On**. Bright lines appear at every cell boundary. The image now looks like a vintage terminal or LED matrix.
4. **Adjust brightness**: Turn **Brightness** (Knob 3) up to about 75%. The lit pixels glow brighter, increasing contrast against the dark background.
5. **Invert**: Flip **Invert** (Switch 7) to **On**. The density mapping reverses: dark regions become dense, bright regions become sparse. The image reads as a photographic negative rendered through the glyph grid.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | default |
| Threshold | default |
| Brightness | ~75% |
| Contrast | default |
| Font Weight | default |
| Spacing | default |
| Invert | On |
| Mono | On |
| Grid Lines | On |
| Bold | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Color Character Mosaic

![Color Character Mosaic result](/img/instruments/videomancer/charset/charset_ex2_s1.png)
*Color Character Mosaic — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A colorful mosaic where the source video's hues shine through a density-mapped glyph overlay.

#### Key Concepts

- Chroma passes through from the source when Mono is off
- The wet/dry mix blends glyph patterns with the original image
- Invert creates a negative-density rendering

#### Video Source

Footage with vivid, saturated colors: flowers, neon signs, painted surfaces, or colorful clothing.

#### Steps

1. **Ensure Mono is Off**: The chroma channels should pass through from the source. You'll see the glyph patterns rendered *in color*: wherever a pattern pixel is lit, it carries the original hue of the source.
2. **Lower the mix**: Pull the **Mix** fader (Fader 12) down to about 50%. The glyph patterns become translucent, overlaid on the original image. The source video shows through the gaps.
3. **Turn up Brightness**: Set **Brightness** (Knob 3) to about 80%. The lit pattern pixels pop against the blended background.
4. **Toggle Grid Lines**: Flip **Grid Lines** (Switch 9) on and off to compare. With the grid, the mosaic structure is explicit. Without it, the patterns blend more naturally into the image.
5. **Sweep Mix**: Slowly move the **Mix** fader from 0% to 100%. Watch the glyph texture emerge from the raw video and gradually dominate the output.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | default |
| Threshold | default |
| Brightness | ~80% |
| Contrast | default |
| Font Weight | default |
| Spacing | default |
| Invert | Off |
| Mono | Off |
| Grid Lines | On |
| Bold | Off |
| Bypass | Off |
| Mix | ~50% |

---

### Exercise 3: Inverted Dot Matrix Print

![Inverted Dot Matrix Print result](/img/instruments/videomancer/charset/charset_ex3_s1.png)
*Inverted Dot Matrix Print — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dot-matrix printer simulation where dark ink dots map to the bright areas of the source, resembling a printed halftone on white paper.

#### Key Concepts

- Inverted density mapping reverses the tonal relationship
- Grid lines frame cells independently of inversion
- Combining inversion with high brightness creates a "light-on-dark" print aesthetic

#### Video Source

High-contrast black-and-white footage, portraits, or graphic shapes (woodcut prints or silhouettes work well.)

#### Steps

1. **Invert**: Flip **Invert** (Switch 7) to **On**. Dark source areas now produce dense patterns and bright areas produce sparse patterns (like ink on paper.)
2. **Monochrome**: Flip **Mono** (Switch 8) to **On** for a pure black-and-white print look.
3. **High brightness**: Set **Brightness** (Knob 3) to about 80%. The "ink" pixels are bright. Because they represent the dark areas of the source (due to inversion), the visual reads as bright dots filling in the shadows.
4. **Add grid**: Enable **Grid Lines** (Switch 9). The grid frames each dot cell, reinforcing the mechanical, printed quality.
5. **Full mix**: Set **Mix** (Fader 12) to 100% for the pure effect.
6. **Compare**: Toggle **Bypass** (Switch 11) to compare the raw input with the dot-matrix rendering. Toggle it back off.
7. **Experiment with inversion off**: Flip **Invert** back to **Off** while keeping all other settings. The tonal mapping reverses again: notice how the same source material reads completely differently when the density relationship changes.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | default |
| Threshold | default |
| Brightness | ~80% |
| Contrast | default |
| Font Weight | default |
| Spacing | default |
| Invert | On |
| Mono | On |
| Grid Lines | On |
| Bold | Off |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Cell**: A fixed-size block of pixels (8×8 in Charset) that acts as the fundamental display unit, analogous to a single character position on a text terminal.

- **Character ROM**: A read-only memory chip in vintage computers that stores pixel bitmap definitions for each displayable character; the hardware equivalent of a font file.

- **Density Mapping**: A technique for representing continuous brightness through the proportion of lit versus unlit pixels in a cell, where denser fills appear brighter to the eye.

- **Glyph**: A single visual symbol or pattern from a character set; in Charset, each density level produces a distinct glyph.

- **Halftone**: A reprographic technique for simulating continuous-tone images using discrete dots of varying size or spacing; Charset's density patterns are a digital analog of halftone screens.

- **Interpolator**: A mix stage that blends between two signals by a fractional amount, used here for the wet/dry crossfade between original and processed video.

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **PETSCII**: The character encoding and art form native to Commodore computers, in which artists compose images from the system's built-in character ROM glyphs.

- **Sample and Hold**: A technique that captures a signal value at one moment and holds it constant until the next sample, used here to lock the luminance reading per cell.

---
