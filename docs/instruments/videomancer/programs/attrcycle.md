---
draft: true
sidebar_position: 11
slug: /instruments/videomancer/attrcycle
title: "Attrcycle"
image: /img/instruments/videomancer/attrcycle/attrcycle_hero.png
description: "Attr Cycle recreates the ZX Spectrum's distinctive attribute colour system, where the screen is divided into character-sized cells and each cell holds a foreground (ink) and background (paper) colour from a limited 8-colour palette."
---

![Attrcycle hero image](/img/instruments/videomancer/attrcycle/attrcycle_hero_s1.png)
*Attrcycle painting the screen in cycling ZX Spectrum attribute colours, with coarse block grids and ink-paper luminance keying.*

---

## Overview

Attrcycle recreates the legendary colour system of the Sinclair ZX Spectrum home computer. The Spectrum divided its display into a coarse grid of 8×8 pixel cells, each assigned a single foreground (***ink***) colour and a single background (***paper***) colour from a palette of eight. Because every pixel in one cell had to share those two colours, graphic artists worked within extreme constraints (and the resulting aesthetic became iconic.)

Attrcycle generates that aesthetic from scratch. The screen is divided into configurable blocks, and each block is assigned ink and paper colours from the Spectrum's eight-colour palette. A ***phase accumulator*** cycles the palette assignments over time, sweeping every block through a continuous colour rotation. The input video signal is not discarded: its luminance determines which pixels within each block receive the ink colour and which receive the paper colour. Bright areas take the ink; dark areas take the paper. The result is a living, breathing mosaic of shifting colour blocks whose internal patterns are shaped by whatever video signal you feed in.

:::tip
Although Attrcycle is classified as a ***synthesis*** program, it uses the input video's brightness as a key. Feed it a camera, a pattern generator, or another Videomancer program's output to control how the colours are distributed within each block.
:::

### What's In a Name?

The name ***Attrcycle*** is a portmanteau of ***attribute*** and ***cycle***. On the ZX Spectrum, the colour data for each 8×8 cell was stored in a section of memory called the ***attribute area***. Each attribute byte held an ink colour, a paper colour, a brightness bit, and a flash bit. "Cycle" refers to the continuous rotation of palette colours across the grid (the defining animation of this program.)

---

## Quick Start

1. With all controls at their defaults, you should see a grid of coloured blocks filling the screen. The **Grid Lines** toggle (Switch 10) is on, drawing dark borders between blocks. Each block displays a colour from the ZX Spectrum palette.
2. Turn **Speed** (Knob 1) clockwise. The colours begin to cycle: each block's ink and paper rotate through the palette. At high speed, the entire grid shimmers with rainbow waves.
3. Feed a video signal into Videomancer and adjust **Density** (Knob 5). This controls the luminance threshold that separates ink from paper. Bright areas of your source take the ink colour; dark areas take the paper colour. The source image's structure becomes visible within the mosaic.
4. Turn **Block Size** (Knob 2) to explore four discrete cell sizes: 8×8, 16×16, 32×32, and 64×64 pixels. Smaller blocks reveal more of the source image's detail; larger blocks create bolder colour fields.

---

## Parameters

![Videomancer front panel with Attrcycle loaded](/img/instruments/videomancer/attrcycle/attrcycle_control_panel.png)
*Videomancer's front panel with Attrcycle active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Speed** controls the rate of colour cycling. A ***phase accumulator*** increments once per video frame; the speed value determines how much it advances each frame. At 0%, fully counterclockwise, the palette is frozen: no cycling occurs, and the colour pattern is static. As speed increases, the colours rotate faster. At 100%, fully clockwise, the palette sweeps rapidly and the entire grid becomes a shimmering cascade of shifting hues.

:::note
The cycling speed depends on the video frame rate. At 60 fps, a given speed setting produces faster visual motion than at 50 fps.
:::

---

### Knob 2 — Block Size

| Property | Value |
|----------|-------|
| Range | 1x – 8x |
| Default | 4x |

**Block Size** selects the dimensions of each attribute cell. The control operates in eight discrete steps mapped to four block sizes: steps 1–2 produce 8×8 pixel blocks, steps 3–4 produce 16×16, steps 5–6 produce 32×32, and steps 7–8 produce 64×64. Smaller blocks create a finer mosaic with more spatial detail. Larger blocks produce bold, poster-like fields of colour. The block grid always aligns to the top-left corner of the active video area.

---

### Knob 3 — Palette Offset

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Palette Offset** shifts the starting point of the colour cycle. At 0%, fully counterclockwise, the palette begins at its default phase. Turning the knob clockwise advances the starting position, changing which colour each block displays at any given moment. This is a spatial offset, not a speed control: it shifts the entire colour map without altering the rate of cycling. Combined with **Speed**, Palette Offset lets you freeze the cycle at a specific colour arrangement.

---

### Knob 4 — Saturation

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Saturation** controls the intensity of the palette colours. At 0%, fully counterclockwise, all chroma is removed and the output becomes monochrome: only the luminance values of the Spectrum palette remain. As saturation increases, the colours grow richer and more vivid. At the default position (~75%), the colours closely match the original ZX Spectrum's CRT output. At 100%, chroma is at full scale.

:::tip
Setting **Saturation** to zero creates a monochrome mode that preserves the luminance structure of the eight Spectrum colours. Black stays black, white stays white, and the six intermediate colours map to distinct gray levels.
:::

---

### Knob 5 — Density

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 62.6% |

**Density** sets the luminance threshold that separates foreground from background within each block. Pixels from the input video whose brightness exceeds the threshold take the block's ***ink*** colour; pixels below the threshold take the ***paper*** colour. At 0%, nearly the entire image is above the threshold: almost everything displays ink. At 100%, nearly everything falls below the threshold: almost everything displays paper. At moderate values, the brightness contours of the input video create visible patterns of ink and paper within each block.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Brightness** scales the luminance of the generated output. At 0%, fully counterclockwise, the generated colours are crushed to black. As brightness increases, the palette colours become more visible. At 100%, the colours appear at their full luminance values. This control affects only the generated Spectrum colours, not the input video signal that passes through the mix.

---

### Switch 7 — Palette

| Property | Value |
|----------|-------|
| Off | Spectrum |
| On | Mono |
| Default | Spectrum |

**Palette** selects between **Spectrum** and **Mono** colour palettes. In the **Spectrum** position, the program uses the classic ZX Spectrum eight-colour palette: black, blue, red, magenta, green, cyan, yellow, and white. In the **Mono** position, the palette is intended to reduce to monochrome tones. In the current version, the Spectrum palette is active in both positions.

---

### Switch 8 — Pattern

| Property | Value |
|----------|-------|
| Off | Checker |
| On | Stripe |
| Default | Checker |

**Pattern** selects the spatial arrangement used to assign colours to blocks. In the **Checker** position, block colours are determined by XORing the column and row indices: adjacent blocks that differ in both axes receive different palette offsets, creating a checkerboard-like distribution of colours. In the **Stripe** position, only the row index is used: all blocks in the same row share the same base colour, producing horizontal bands that cycle through the palette from top to bottom.

:::tip
**Checker** mode creates a more chaotic, pointillistic field of colour. **Stripe** mode creates orderly horizontal ribbons. Both animate when **Speed** is active: checker mode creates a shimmering mosaic while stripe mode produces scrolling colour bars.
:::

---

### Switch 9 — Flash

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Flash** enables the ZX Spectrum's ***FLASH*** attribute. On the original hardware, setting the FLASH bit in an attribute byte caused the ink and paper colours to swap at a fixed rate, creating a blinking effect. Attrcycle recreates this: when Flash is **On**, the ink and paper assignments swap approximately once per second (every 64 frames). The swap is instantaneous: all affected blocks change simultaneously. When Flash is **Off**, colours remain stable.

---

### Switch 10 — Grid Lines

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Grid Lines** enables dark borders at the boundary of each attribute block. When set to **On**, the first pixel at the left edge and top edge of every block is drawn as a near-black line, making the block grid visible. This recreates the visual structure of the Spectrum's character cell grid. When set to **Off**, the grid lines are hidden and adjacent blocks blend edge-to-edge. The grid line colour is fixed at near-black regardless of palette or brightness settings.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Attrcycle processing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the generated colour pattern.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input video and the wet (generated Spectrum colour) output. At 0%, the fader fully left, only the original input video is visible: no Spectrum colours appear. At 100%, the fader fully right, only the generated colour pattern is visible. At intermediate positions, the input video and the generated pattern blend together, creating ghostly overlays where the source image shows through the colour blocks.

---

## Background

### The ZX Spectrum attribute system

The Sinclair ZX Spectrum, released in 1982, was one of the most popular home computers in the United Kingdom and Europe. Its display was organized into a 256×192 pixel bitmap, but colour was applied at the level of 8×8 pixel ***character cells*** rather than individual pixels. Each cell had a single ***attribute byte*** that defined two colours: ***ink*** (foreground) and ***paper*** (background): plus a brightness bit and a flash bit. This meant that within any 8×8 block, only two colours were possible.

This constraint led to a visual artifact known as ***attribute clash***: when objects of different colours overlapped within a single cell, one colour would overwrite the other, producing visible fringing along cell boundaries. Programmers and pixel artists developed elaborate techniques to work within these limits, and the resulting aesthetic: bold colour blocks, stark two-tone patterns, and visible grid structure: became one of the most recognizable visual signatures in computing history.

### The FLASH bit

The ZX Spectrum's attribute byte included a single-bit flag called FLASH. When set, the hardware automatically swapped the ink and paper colours at a fixed rate of approximately once per second. Game designers used this for blinking cursors, warning indicators, and attention-grabbing UI elements. Attrcycle's **Flash** toggle recreates this behavior by swapping the ink and paper palette indices every 64 frames.

### Colour cycling

***Colour cycling***, also called ***palette animation***, is a technique where the entries in a colour lookup table are rotated over time rather than redrawing actual pixels. On hardware with indexed colour: including the ZX Spectrum, Commodore Amiga, and early VGA PCs: cycling the palette was computationally cheap: you changed a handful of colour registers and the entire display updated instantly. Artists exploited this for waterfalls, fire effects, scrolling backgrounds, and psychedelic light shows.

Attrcycle's phase accumulator implements a continuous version of this technique. Rather than rotating a lookup table in discrete steps, the accumulator adds a fractional amount each frame, producing smooth, controllable animation speed.


---

## Signal Flow

### Signal Flow Notes

The key interaction in Attrcycle is between the ***generated colour grid*** and the ***input video luminance***. The pipeline generates a full-screen pattern of cycling Spectrum colours, but the decision of whether each pixel shows ink or paper is driven by the brightness of the input video at that pixel position. This creates a hybrid: the colours are synthetic, but their spatial arrangement is shaped by the live input.

The palette index computation is the creative core of the program. Each block's colour is a function of its grid position (column, row), the animation phase, and the user-selected offset. The ink and paper indices are separated by exactly four palette positions: half the eight-colour palette: so contrasting colours naturally face each other. When Flash is enabled, these two indices swap approximately once per second, causing the entire display to alternate between two complementary colour arrangements.

:::note
The saturation stage scales chroma ***around the neutral axis*** (value 512). This means reducing saturation moves colours toward gray without shifting their hue. At zero saturation, only the luminance values of the eight palette colours remain.
:::


---

## Exercises

These exercises explore Attrcycle's colour cycling, block structure, and input-dependent keying. Each builds on the previous, progressing from static patterns to animated effects.
### Exercise 1: The Spectrum Grid

![The Spectrum Grid result](/img/instruments/videomancer/attrcycle/attrcycle_ex1_s1.png)
*The Spectrum Grid — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A static mosaic of ZX Spectrum colours with visible cell boundaries, exploring how block size and palette offset shape the pattern.

#### Key Concepts

- Block size controls the spatial granularity of the attribute grid
- Palette offset shifts the colour distribution across the grid
- Grid lines reveal the underlying cell structure

#### Steps

1. Set **Speed** (Knob 1) to 0% so the palette does not cycle. The colour grid is frozen.
2. Turn **Block Size** (Knob 2) to step 1 (8×8 blocks). The screen fills with a fine mosaic of small coloured tiles.
3. Slowly turn **Block Size** through its four positions: 8×8, 16×16, 32×32, 64×64. Watch the grid coarsen from a detailed mosaic to large, bold colour panels.
4. Set Block Size to 16×16 and slowly sweep **Palette Offset** (Knob 3). The colour assignments shift across the grid (you're rotating which colour appears in which block.)
5. Toggle **Pattern** (Switch 8) between **Checker** and **Stripe**. In Checker mode, adjacent blocks have different colours. In Stripe mode, all blocks in a row share the same base colour.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 0% |
| Block Size | 2x (16×16) |
| Palette Offset | ~50% |
| Saturation | 75% |
| Density | ~63% |
| Brightness | 75% |
| Palette | Spectrum |
| Pattern | Checker |
| Flash | Off |
| Grid Lines | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Colour Cycling Animation

![Colour Cycling Animation result](/img/instruments/videomancer/attrcycle/attrcycle_ex2_s1.png)
*Colour Cycling Animation — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated colour cycle with flashing ink/paper swap, exploring the interplay of speed, flash rate, and colour intensity.

#### Key Concepts

- The phase accumulator drives palette rotation per frame
- Flash recreates the ZX Spectrum's blinking attribute
- Saturation desaturation reveals luminance structure

#### Steps

1. Starting from the Exercise 1 settings, slowly increase **Speed** (Knob 1). The colour grid begins to animate (each block cycles through the Spectrum palette in sequence.)
2. At moderate speed (~40%), toggle **Flash** (Switch 9) to **On**. Every second or so, ink and paper swap across the entire display. The grid pulses with alternating colour arrangements.
3. Lower **Saturation** (Knob 4) to 0%. The grid becomes monochrome: you can see the luminance structure of the eight palette colours: black, dark grays, mid grays, and white. The cycling and flashing continue, but now in grayscale.
4. Bring **Saturation** back up to full (100%) and switch **Pattern** (Switch 8) to **Stripe**. The cycling colours now scroll as horizontal bands from top to bottom (a colour waterfall.)
5. Increase **Speed** to maximum. The palette rotates so quickly that adjacent frames blur together, creating a shimmering rainbow effect.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 40% |
| Block Size | 3x (16×16) |
| Palette Offset | 0% |
| Saturation | 100% |
| Density | ~63% |
| Brightness | 75% |
| Palette | Spectrum |
| Pattern | Stripe |
| Flash | On |
| Grid Lines | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Input-Shaped Colour Keying

![Input-Shaped Colour Keying result](/img/instruments/videomancer/attrcycle/attrcycle_ex3_s1.png)
*Input-Shaped Colour Keying — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A composite image where the cycling Spectrum colours are shaped by a live video source, with the mix crossfader creating translucent overlays.

#### Key Concepts

- Input video luminance drives the ink/paper threshold
- Density controls the balance between ink and paper regions
- Mix blends the generated pattern with the source

#### Steps

1. Feed a video signal with strong tonal contrast into Videomancer (a face, text, or geometric shapes work well).
2. From the default settings, set **Speed** to a slow value (~10%) so the cycling is visible but gentle.
3. Sweep **Density** (Knob 5) from 0% to 100%. At 0%, nearly everything is ink: one colour dominates. At 100%, nearly everything is paper: the complementary colour dominates. At moderate values, the bright and dark areas of your source split into two contrasting Spectrum colours. The shape of your input becomes visible.
4. Set **Block Size** (Knob 2) to the smallest setting (8×8). The fine grid resolves more detail from the input image. Now try 64×64 (the input image is abstracted into broad colour fields.)
5. Pull **Mix** (Fader 12) down to ~50%. The original input video ghosts through the colour pattern, creating a double-exposure effect. Bright input areas blend with their ink colour; dark areas blend with paper.
6. Turn **Grid Lines** (Switch 10) **Off** and set **Block Size** to 8×8. The colours fill the screen edge-to-edge with no visible cell borders. The input image's structure appears as a colour-mapped silhouette.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 10% |
| Block Size | 1x (8×8) |
| Palette Offset | 0% |
| Saturation | 75% |
| Density | 50% |
| Brightness | 75% |
| Palette | Spectrum |
| Pattern | Checker |
| Flash | Off |
| Grid Lines | Off |
| Bypass | Off |
| Mix | 50% |

---
## Glossary

- **Attribute**: On the ZX Spectrum, a byte of data assigned to each 8×8 character cell defining its ink colour, paper colour, brightness, and flash state.

- **Attribute Clash**: A visual artifact on the ZX Spectrum where only two colours could appear within a single 8×8 cell, causing colour fringing when objects overlapped cell boundaries.

- **Colour Cycling**: An animation technique that rotates entries in a colour lookup table over time, producing the appearance of motion without redrawing pixel data.

- **Density**: In Attrcycle, the luminance threshold that separates ink (foreground) from paper (background) regions within each block.

- **Flash**: A ZX Spectrum attribute bit that caused ink and paper colours to swap at a fixed rate, producing a blinking effect.

- **Ink**: The foreground colour assigned to a character cell in the ZX Spectrum attribute system; applied to pixels above the luminance threshold.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness.

- **Paper**: The background colour assigned to a character cell in the ZX Spectrum attribute system; applied to pixels below the luminance threshold.

- **Phase Accumulator**: A counter that increments by a configurable amount each frame, producing a continuously advancing animation phase used for colour cycling.

---
