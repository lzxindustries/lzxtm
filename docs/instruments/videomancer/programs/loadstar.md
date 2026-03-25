---
draft: true
sidebar_position: 177
slug: /instruments/videomancer/loadstar
title: "Loadstar"
image: /img/instruments/videomancer/loadstar/loadstar_hero_s1.png
description: "There was a ritual shared by an entire generation of home computer users."
---

![Loadstar hero image](/img/instruments/videomancer/loadstar/loadstar_hero_s1.png)
*Loadstar applying character cell quantization and animated border color cycling to live video, evoking the unmistakable aesthetic of a Commodore 64 loading screen.*

---

## Overview

Loadstar transforms live video into a real-time homage to the Commodore 64 loading experience. The program divides the screen into a visible border region and a central picture area, just like the C64's VIC-II chip. The border pulses with animated color cycling, while the inner image is broken into character cells with quantized luma values: a faithful recreation of the ***attribute clash*** that defined 8-bit home computing visuals. The result is a lo-fi, blocky aesthetic that sits somewhere between retro nostalgia and modern glitch art.

At subtle settings, Loadstar adds a gentle character cell texture and a discreet flashing border frame. Push the controls further and the image collapses into a grid of flat color blocks surrounded by a hyperactive neon border. The wet/dry **Mix** fader lets you blend the processed result with the original signal at any ratio, making Loadstar equally useful as a light texture overlay or a full-screen 8-bit time machine.

:::tip
Loadstar pairs beautifully with synthesis programs. Route a pattern generator through Loadstar to give procedural graphics the unmistakable look of a 1980s home computer display.
:::

### What's In a Name?

***Loadstar*** was the name of a beloved disk magazine published for the Commodore 64 and 128 from 1984 to 2007. The word itself combines "load," the keyword you typed to run a program on a C64 (`LOAD "*",8,1`), with "star," evoking both the wildcard asterisk in that command and the guiding North Star. For a generation of computer users, the flashing border bars and blocky character graphics of a loading screen were the ritual prelude to every adventure. This program recreates that ritual.

---

## Quick Start

1. Feed a video signal into Videomancer and select **Loadstar**. The border of the screen immediately begins flashing with animated color bars (the loading ritual has begun.)
2. Toggle **Attr Clash** (Switch 9) to **On**. The central image snaps into flat, cell-sized blocks of quantized brightness, as though the video has been stuffed into a character-mapped display.
3. Turn **Cell Size** (Knob 2) clockwise to increase the width of each character cell. The image becomes coarser and more abstract, like zooming into the PETSCII character grid.
4. Slide the **Mix** fader (Fader 12) toward the center to blend the 8-bit effect with the original video. You can dial in just a hint of retro texture or go full C64.

---

## Parameters

![Videomancer front panel with Loadstar loaded](/img/instruments/videomancer/loadstar/loadstar_control_panel.png)
*Videomancer's front panel with Loadstar active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Border Spd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Border Spd** controls how quickly the border color cycles from frame to frame. At 0%, fully counterclockwise, the border color advances slowly: a gentle, meditative pulse. As you turn the knob clockwise, the cycling accelerates and the border flashes through its palette more aggressively. At 100%, the color change is rapid and frenetic, recalling the frantic border stripes of a C64 turbo loader. The speed is determined by the top three bits of the control value, added to a base increment of one per frame.

:::note
Border Spd has no effect unless **Border Flash** (Switch 7) is set to **On**.
:::

---

### Knob 2 — Cell Size

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

**Cell Size** sets the width of each character cell in pixels. The cell width is computed from the top three bits of the control value plus a base of four, giving a range of four to eleven pixels. At minimum, cells are narrow and the image retains more horizontal detail. As you increase the value, cells widen and horizontal information is increasingly quantized: each cell holds a single sampled luma value that repeats across its full width. At maximum, cells span eleven pixels and the image dissolves into broad, flat stripes.

---

### Knob 3 — Color Depth

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

**Color Depth** is reserved for future development. In the current version of Loadstar, adjusting this knob does not change the output. It is mapped to a register but not yet consumed by the processing pipeline.

---

### Knob 4 — Charset

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

**Charset** is reserved for future development. In the current version of Loadstar, adjusting this knob does not change the output. A future revision may use this control to select among character pattern overlays.

---

### Knob 5 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |

**Brightness** is reserved for future development. In the current version of Loadstar, adjusting this knob does not change the output. A future revision may use this control to apply a brightness offset to the processed signal, emulating the variable phosphor brightness of vintage CRT monitors.

---

### Knob 6 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contrast** is reserved for future development. In the current version of Loadstar, adjusting this knob does not change the output. A future revision may use this control to apply a contrast gain to the processed signal.

---

### Switch 7 — Border Flash

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Border Flash** enables or disables the animated border color cycling. When set to **On**, the border region: the frame surrounding the central picture area: cycles through colors at a rate set by **Border Spd** (Knob 1). Each video frame, the border color index advances by a step derived from the speed setting. When set to **Off**, the border color freezes at its current value.

---

### Switch 8 — Color Cycle

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color Cycle** is reserved for future development. In the current version of Loadstar, toggling this switch does not change the output.

---

### Switch 9 — Attr Clash

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Attr Clash** enables ***attribute clash***, the defining visual limitation of 8-bit character-mapped displays. When set to **On**, the luma channel is quantized to three bits per character cell. Each cell can display only one of eight brightness levels, and the chroma channels are forced to neutral gray. The result is a flat, monochrome mosaic that recalls the C64's high-resolution bitmap mode, where each 8×8 cell was limited to two colors. When set to **Off**, the central picture area passes through without attribute-clash quantization: luma and chroma retain their full input values (still subject to cell-size sampling on the luma channel).

:::tip
***Attribute clash is the signature effect.*** It is what separates Loadstar from a generic pixelator. With Attr Clash enabled, the image looks like it has been drawn on a character-mapped display. Without it, you get cell-width horizontal quantization but the colors remain natural.
:::

---

### Switch 10 — Interlace

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Interlace** simulates the look of an interlaced display by darkening every other scan line. When set to **On**, odd-numbered lines have their luma value halved, creating visible horizontal stripe artifacts reminiscent of a CRT television displaying an interlaced signal. When set to **Off**, all lines are processed at full brightness.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed, delay-aligned input signal directly to the output, skipping all Loadstar processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the wet/dry blend between the processed Loadstar output and the original input signal. At 0%, fully down, only the original input is heard: the effect is silent. As you raise the fader, the character cells, border flash, and attribute clash fade in. At 100%, fully up, the output is entirely the Loadstar-processed signal. The crossfade is performed by three independent interpolators (one each for Y, U, and V), ensuring smooth transitions with no color artifacts.

---

## Background

### Character cells and attribute clash

The Commodore 64's VIC-II video chip divided the screen into a grid of ***character cells***, typically 8×8 pixels each. In high-resolution bitmap mode, each cell could display only two colors: a foreground and a background: chosen from a fixed 16-color palette. When an image contained more color variation than the cell could represent, neighboring cells snapped to different palette entries, creating hard, blocky boundaries. This artifact was known as ***attribute clash*** (or "color clash" on the ZX Spectrum), and it became one of the most recognizable visual signatures of 8-bit computing.

Loadstar recreates this effect by sampling the luma value at the start of each character cell and holding it for the cell's full width. When **Attr Clash** is enabled, the held value is further quantized to three bits, reducing the image to eight discrete brightness levels with neutral chroma.

### Border color cycling

On the Commodore 64, the screen border was a separate, programmable region surrounding the main display area. Clever programmers discovered that by rapidly changing the border color register during the vertical blanking interval, they could produce animated color bars in the border region. This technique became especially associated with ***turbo loaders***, fast-loading routines that displayed flashing border stripes as a progress indicator while data streamed from the disk drive. The faster the stripes, the faster the load.

Loadstar divides the output frame into a border region (pixels outside the central 1184×648 area) and a picture region. The border color is a 4-bit index that advances by a configurable step on each vertical sync event. The speed knob controls the magnitude of each step, and the resulting color is mapped into the YUV domain with offset chroma values.

### Interlaced scanning

***Interlaced*** video displays each frame in two passes: first the odd-numbered lines, then the even-numbered lines. On a CRT, the two fields blend together in the viewer's eye. On an LCD or in a digital processing chain, the two-field structure can produce visible horizontal line artifacts, especially when the image contains fast motion. Loadstar's interlace mode simulates this look by halving the brightness of every other scan line, producing the characteristic stripe texture of an interlaced CRT viewed at close range.


---

## Signal Flow

### Signal Flow Notes

The processing pipeline is implemented in a single clocked process with an 8-clock total delay. Timing detection and frame counting happen first: the x and y counters track the current pixel position, and the frame counter increments on each vertical sync falling edge. The cell boundary detector uses a local counter that resets when it reaches the configured cell width, at which point the current input luma value is captured into a hold register.

Two key branching paths follow. If the current pixel falls in the border region, the output is a synthetic color derived from the cycling border index. If the pixel is inside the picture area and attribute clash is enabled, the held luma value is quantized to three bits and chroma is forced to the neutral midpoint. Without attribute clash, the input YUV passes through unmodified (though the Y channel still shows cell-width sample-and-hold artifacts from the capture logic). The interlace stage then optionally halves luma on odd scan lines.

:::note
The dry signal path (for the Mix interpolator's "A" input) is the ***delayed*** original input, not the real-time input. An 8-clock shift register delays the original Y, U, V, and sync signals to align them with the processing pipeline's output. This ensures the wet/dry crossfade produces no timing artifacts.
:::


---

## Exercises

These exercises progress from the simplest border-flash effect through attribute clash quantization to a full 8-bit aesthetic combining all active parameters.
### Exercise 1: The Loading Ritual

![The Loading Ritual result](/img/instruments/videomancer/loadstar/loadstar_ex1_s1.png)
*The Loading Ritual — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A pulsing, animated border frame reminiscent of a C64 turbo loader, overlaid on an otherwise unprocessed video signal.

#### Key Concepts

- The border region is separate from the picture area
- Border Flash produces animated color cycling driven by the frame counter
- Border Spd controls the color advance rate

#### Video Source

A live camera feed or any recorded video with moderate brightness and color.

#### Steps

1. **Enable the border**: Set **Border Flash** (Switch 7) to **On**. The border region immediately begins cycling through colors.
2. **Slow it down**: Turn **Border Spd** (Knob 1) fully counterclockwise. The border pulses gently, advancing one color step per frame.
3. **Speed it up**: Slowly turn Border Spd clockwise. The cycling accelerates: at high values, the border becomes a rapid strobe of shifting hues.
4. **Clean center**: Confirm that **Attr Clash** (Switch 9) is **Off** and **Interlace** (Switch 10) is **Off**. The central picture area passes through cleanly while the border flashes around it.

#### Settings

| Control | Value |
|---------|-------|
| Border Spd | ~80% |
| Cell Size | 1 |
| Color Depth | 5 |
| Charset | 0 |
| Brightness | ~63% |
| Contrast | ~50% |
| Border Flash | On |
| Color Cycle | Off |
| Attr Clash | Off |
| Interlace | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Character-Mapped Display

![Character-Mapped Display result](/img/instruments/videomancer/loadstar/loadstar_ex2_s1.png)
*Character-Mapped Display — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A retro character-cell display where the video image is broken into flat-colored blocks, as though rendered on an 8-bit computer's text-mode screen.

#### Key Concepts

- Cell Size controls horizontal quantization granularity
- Attribute clash reduces luma to three bits and neutralizes chroma
- The combination produces a character-mapped display aesthetic

#### Video Source

Footage with strong, recognizable shapes: a face, a hand, or large geometric objects. High-contrast material works best.

#### Steps

1. **Enable attribute clash**: Set **Attr Clash** (Switch 9) to **On**. The image immediately snaps to eight discrete brightness levels with neutral (gray) chroma.
2. **Set cell width**: Turn **Cell Size** (Knob 2) to a midrange position. Each cell is now several pixels wide, and the image becomes a mosaic of flat blocks.
3. **Widen cells**: Increase Cell Size toward maximum. The blocks grow larger and the image becomes increasingly abstract (recognizable shapes dissolve into coarse tiles.)
4. **Narrow cells**: Decrease Cell Size to near-minimum. The blocks narrow to four pixels, and the image regains much of its detail while retaining the quantized brightness levels.
5. **Add scanlines**: Toggle **Interlace** (Switch 10) to **On**. Horizontal stripe artifacts appear across the image, adding a CRT-like texture to the character cells.

#### Settings

| Control | Value |
|---------|-------|
| Border Spd | ~38% |
| Cell Size | 5 |
| Color Depth | 5 |
| Charset | 0 |
| Brightness | ~63% |
| Contrast | ~50% |
| Border Flash | On |
| Color Cycle | Off |
| Attr Clash | On |
| Interlace | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Full 8-Bit Immersion

![Full 8-Bit Immersion result](/img/instruments/videomancer/loadstar/loadstar_ex3_s1.png)
*Full 8-Bit Immersion — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A complete Commodore 64 loading screen experience: flashing border, character-cell picture, interlaced scanlines, and a controlled mix with the original video.

#### Key Concepts

- All active stages combine to form a complete retro display emulation
- The Mix fader blends the 8-bit aesthetic with the original signal
- Border animation and picture processing work independently

#### Video Source

Any video source: camera feed, recorded footage, or even a test pattern. Material with a range of brightness values showcases the attribute clash quantization best.

#### Steps

1. **Full processing**: Enable **Border Flash** (Switch 7), **Attr Clash** (Switch 9), and **Interlace** (Switch 10). All three active processing modes engage simultaneously.
2. **Fast border**: Set **Border Spd** (Knob 1) to about 80%. The border cycles rapidly.
3. **Medium cells**: Set **Cell Size** (Knob 2) to a midrange value. The picture area shows clearly defined character blocks.
4. **Blend**: Lower the **Mix** fader (Fader 12) to about 85%. The character-cell effect blends with the underlying video, producing a ghostly overlay where the original image shows through the quantized blocks.
5. **A/B compare**: Toggle **Bypass** (Switch 11) to compare the full effect with the clean input. Toggle it back to return to the processed output.
6. **Explore**: Sweep Cell Size and Border Spd simultaneously while watching the result. The border animation and cell granularity change independently, letting you find the combination that best suits the source material.

#### Settings

| Control | Value |
|---------|-------|
| Border Spd | ~80% |
| Cell Size | 4 |
| Color Depth | 5 |
| Charset | 0 |
| Brightness | ~63% |
| Contrast | ~50% |
| Border Flash | On |
| Color Cycle | Off |
| Attr Clash | On |
| Interlace | On |
| Bypass | Off |
| Mix | ~85% |

---
## Glossary

- **Attribute Clash**: A visual artifact of 8-bit character-mapped displays where each cell is limited to a small number of colors, causing hard boundaries between adjacent cells

- **Border Region**: The frame area surrounding the central picture on a home computer display, separately programmable from the main screen content

- **Character Cell**: A fixed-width block of pixels treated as a single unit on a character-mapped display, typically 8×8 pixels on the Commodore 64

- **Chroma**: The color information in a video signal, encoded as U and V components in YUV color space

- **Interlaced**: A scanning method that displays each video frame in two alternating passes (odd lines then even lines), producing visible line structure on close inspection

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness

- **Quantization**: Mapping a continuous range of values to a smaller set of discrete levels, producing visible steps in gradients

- **Sample and Hold**: A technique that captures a signal value at a specific moment and holds it constant until the next sample point, used here to maintain a uniform brightness across each character cell

- **VIC-II**: The Video Interface Chip (model 6569/6567) used in the Commodore 64 to generate video output, managing character cells, sprites, and border color

---
