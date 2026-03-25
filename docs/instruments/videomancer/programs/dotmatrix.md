---
draft: true
sidebar_position: 90
slug: /instruments/videomancer/dotmatrix
title: "Dotmatrix"
image: /img/instruments/videomancer/dotmatrix/dotmatrix_hero_s1.png
description: "Before inkjet printers and laser engines, the dominant output device for personal computers was the impact dot-matrix printer."
---

![Dotmatrix hero image](/img/instruments/videomancer/dotmatrix/dotmatrix_hero_s1.png)
*Dotmatrix transforming a live video feed into a simulated impact-printer page, each pixel rendered as a discrete ink dot on tinted paper.*

---

## Overview

**Dotmatrix** is a real-time dot-matrix printer emulation that replaces every pixel with a discrete ink dot stamped onto a virtual page. The screen is divided into a regular grid of cells, and within each cell a single dot is placed whose size depends on the brightness of the source image. Dark areas produce large dots: more ink: while bright areas produce tiny dots or none at all. The result is a ***halftone*** rendering, the same technique used by newspapers and impact printers to reproduce photographic images with only a single color of ink.

Beyond static halftoning, Dotmatrix simulates the physical behavior of a printer head sweeping across the page. When the **Feed** animation is enabled, you can watch the image emerge line by line, with the print head marching horizontally and advancing to the next row. The **Dir** toggle adds ***bidirectional printing***, where even rows print left-to-right and odd rows print right-to-left: exactly as a real impact printer optimizes for speed. Ink density, ribbon wear, paper color, and even mechanical jitter are all adjustable, making Dotmatrix a rich and tactile simulation of a bygone technology.

:::tip
***Halftoning is the core trick.*** Dark source areas become big dots; bright areas become small dots. Your eye blends them into continuous tones at a distance. Dotmatrix makes this process visible and controllable in real time.
:::

### What's In a Name?

A ***dot matrix*** printer creates characters and images by striking an ink ribbon with a column of tiny pins arranged in a vertical line. As the print head sweeps across the page, the pins fire in rapid patterns, leaving a grid of ink dots that combine into recognizable shapes. The name ***Dotmatrix*** is a direct reference to this technology: each pixel of source video is translated into a single dot in a matrix grid, just as a printer head would stamp them onto continuous-feed paper.

---

## Quick Start

1. Start with all knobs at noon and all switches in the Off position. Your video feed is now rendered as a grid of ink dots on white paper: a monochrome halftone print. Notice how dark areas of the source image have large, closely packed dots while bright areas have smaller dots or bare paper.
2. Turn **Dot Size** (Knob 2) counterclockwise. The maximum dot radius shrinks, making the print look lighter and more airy. Turn it clockwise and the dots grow to fill their cells, producing a denser print.
3. Flip **Feed** (Switch 10) to On, then sweep **Print Sp** (Knob 1). The image reveals itself line by line as the virtual print head sweeps across the page. Faster speeds fill the page in a few frames; slower speeds let you watch each row appear.
4. Flip **Dir** (Switch 8) to Bidi. Now even rows print left-to-right while odd rows print right-to-left, just like a real bidirectional impact printer.

---

## Parameters

![Videomancer front panel with Dotmatrix loaded](/img/instruments/videomancer/dotmatrix/dotmatrix_control_panel.png)
*Videomancer's front panel with Dotmatrix active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Print Sp

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Print Sp** controls the speed of the horizontal print-head sweep when the **Feed** animation is active. At 0%, the sweep barely advances between frames; the image builds up slowly, one sliver at a time. At 100%, the head races across in just a few frames and the full image is revealed almost instantly. When Feed is disabled (Switch 10 Off), the entire image is always fully printed regardless of this setting.

:::note
Print speed only has an observable effect when **Feed** (Switch 10) is set to On. With Feed off, the sweep position is maxed out and the full image is always present.
:::

---

### Knob 2 — Dot Size

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Dot Size** sets the maximum radius a dot can reach. Each dot's actual size is determined by the source luminance: dark pixels produce large dots, bright pixels produce small ones: but no dot can exceed the limit set here. At 0%, dots are at their smallest, creating a faint, airy halftone. At 100%, dots can grow to fill their entire grid cell, producing dense, inky coverage. The internal computation shifts the 10-bit parameter to a 5-bit maximum radius, giving 32 distinct size steps.

---

### Knob 3 — Ink Dens

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Ink Dens** controls the darkness of the ink itself: how black the black gets. At 0%, the ink prints as a light gray, as though the ribbon has almost run dry. As you increase Ink Dens, the ink color deepens toward full black. At 100%, dots are rendered in the darkest possible tone. Think of it as adjusting how much ink is loaded onto the ribbon before each print pass.

---

### Knob 4 — Ribbon

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Ribbon** simulates the gradual exhaustion of an ink ribbon. A real impact printer's ribbon fades as it's used, producing lighter impressions over time. At 100%, the ribbon is fresh and the ink is at full strength. As you reduce the value below 50%, the ink begins to lighten as though the ribbon is wearing out by adding brightness to the ink color. At 0%, the ribbon fade effect is at its strongest, producing very faint impressions that almost disappear into the paper.

:::tip
Combining a low **Ribbon** value with a high **Ink Dens** creates an interesting tension: you're telling the program to use strong ink on a worn-out ribbon. The result is a mid-gray tone that feels authentically degraded.
:::

---

### Knob 5 — Jitter

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Jitter** introduces a random perturbation to each dot's radius, simulating the mechanical imprecision of a real print head. At 0%, dots are perfectly sized according to the source brightness, resulting in a clean, precise halftone. Above approximately 25%, the LFSR-based pseudo-random generator adds a small random offset (0 to 3 units) to each dot's computed radius. The effect is subtle: a gentle roughening of the dot field that makes the print look more organic and less mathematically perfect. Even at 100%, jitter is clamped to the **Dot Size** maximum, so dots never exceed their cell boundaries.

---

### Knob 6 — Paper Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Paper Hue** tints the background paper color, rotating through four distinct paper stocks as a ***hue wheel***. At 0° (fully counterclockwise), the paper is pure white. Rotating clockwise through 90° shifts to a green-tinted paper, reminiscent of old greenbar continuous-feed stock. Continuing to 180° produces a cool, bluish paper like carbon copy paper. Past 270°, the paper warms to a creamy yellow, evoking aged parchment. The rotation is divided into four discrete color zones rather than a continuous gradient.

---

### Switch 7 — Head

| Property | Value |
|----------|-------|
| Off | 9-Pin |
| On | Inkjet |
| Default | 9-Pin |

**Head** selects between two print-head emulations that differ in grid cell size. In the **9-Pin** position, the screen is divided into an 8×8 pixel grid, producing a characteristic coarse halftone with visible, chunky dots: the classic look of a 1980s impact printer. In the **Inkjet** position, the grid switches to a finer 4×4 pixel pitch, doubling the spatial frequency. Inkjet mode produces a smoother, denser dot field that more closely resembles modern inkjet output, though the halftone principle remains the same.

---

### Switch 8 — Dir

| Property | Value |
|----------|-------|
| Off | Uni |
| On | Bidi |
| Default | Uni |

**Dir** selects between ***unidirectional*** and ***bidirectional*** printing. In the **Uni** position, the virtual print head always sweeps in the same direction (left to right) for every row. In the **Bidi** position, even-numbered rows print left-to-right while odd-numbered rows print right-to-left, just as a real bidirectional printer saves time by printing in both directions. The visual effect is most apparent when **Feed** is active (you can watch the sweep direction alternate row by row.)

:::note
Bidirectional mode is a subtle effect. It's most visible during the **Feed** animation, where you can watch the print head reverse direction on each new line.
:::

---

### Switch 9 — Draft

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Draft** activates a reduced-density print mode that skips every other dot column, simulating the "draft quality" setting found on real dot-matrix printers. Draft mode was used to save ink and increase print speed at the expense of image quality. With Draft On, the halftone pattern takes on a vertically striped appearance as alternating columns are left blank. The effect is especially prominent with larger **Dot Size** values, where the missing columns create visible gaps.

---

### Switch 10 — Feed

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Feed** enables the print-head sweep animation. With Feed **Off**, the full image is rendered as a complete halftone print every frame: no animation, no reveal. With Feed **On**, the image builds up progressively as a virtual print head sweeps across the page. The **Print Sp** knob controls sweep speed, and the **Dir** toggle controls whether the head reverses on alternate rows. The animation resets to the top of the page when the sweep reaches the bottom.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Dotmatrix processing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the halftone print.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (halftoned) output. At 0%, the output is entirely the original input video. At 100%, the output is the full Dotmatrix halftone. Intermediate positions blend the two, which can produce interesting ghostly overlays where the original image shows through the dot grid. Mix uses three parallel interpolators operating independently on Y, U, and V channels.

---

## Background

### Halftone printing

The ***halftone*** process was invented in the 1880s to reproduce photographic images in print media that could only deposit uniform ink. The trick is to break the image into a grid of dots whose ***sizes*** encode brightness. Large dots in dark areas merge together and appear solid; tiny dots in bright areas leave mostly bare paper. At reading distance, your eye averages the dots and paper together, perceiving continuous tones from a purely binary medium.

Impact dot-matrix printers adopted this principle in simplified form. A column of pins (9 or 24 in typical consumer models) strikes an inked ribbon against paper as a carriage sweeps horizontally. By selectively firing pins during the sweep, the printer builds up characters and graphics from a matrix of discrete impact marks. The result has a distinctive textured quality (slightly rough, imprecise, charming.)

### Manhattan distance and diamond dots

Dotmatrix computes the distance from each pixel to the center of its grid cell using the ***Manhattan distance*** (also called ***taxicab distance***): the sum of the absolute horizontal and vertical offsets, $|dx| + |dy|$. Unlike Euclidean distance, which produces circular contours, Manhattan distance produces diamond-shaped contours rotated 45° from the pixel grid. This gives the dots their characteristic angular shape.

The Manhattan metric was chosen for efficiency. Euclidean distance requires a square root (expensive on an iCE40 FPGA), while Manhattan distance needs only addition and absolute value: both cheap in hardware. The diamond shape also complements the rectangular grid structure, creating a tessellation that fills space more uniformly than circles would at this resolution.

### Ink, ribbon, and paper

Real printers have distinct physical properties that Dotmatrix simulates independently. The ***ink*** has a darkness controlled by how heavily the ribbon is inked. The ***ribbon*** itself degrades over time, producing lighter impressions as its ink supply is consumed. The ***paper*** has its own color: from pure white stock to greenbar fan-fold to yellow legal pads.

In Dotmatrix, the dot color is computed from the Ink Dens and Ribbon parameters. Ink darkness is the inverse of the Ink Dens value, placed at mid-range. The Ribbon parameter applies an additional lightening when set below 50%, simulating a depleted ribbon. Paper color is selected from four preset tints indexed by the Paper Hue wheel.


---

## Signal Flow

### Signal Flow Notes

Two key interactions define Dotmatrix's behavior:

1. **Luminance-to-radius mapping**: The source luma channel is the sole driver of dot size. The VHDL computes the inverse of input luminance (1023 − Y), extracts the top 5 bits as a base radius, clamps it to the **Dot Size** parameter's maximum, and optionally adds LFSR-based jitter. This inverse relationship: dark source equals large dot: is the fundamental halftone principle.

2. **Sweep animation**: When **Feed** is active, a DDS-style accumulator tracks the print head's horizontal position across the page. Each video frame, the sweep position advances by a scaled version of the **Print Sp** parameter. When the head reaches the active width, it wraps to zero and advances to the next row. In bidirectional mode, odd rows reverse the sweep direction. Pixels beyond the current sweep position are rendered as bare paper, creating the progressive reveal effect.

:::tip
**All dots are monochrome.** Dotmatrix uses a single ink color (controlled by Ink Dens and Ribbon) on a tinted paper background. There is no per-dot color variation from the source: color information is only preserved through the wet/dry **Mix** crossfade. To see the source colors bleed through the halftone pattern, pull Mix below 100%.
:::


---

## Exercises

These exercises progress from basic halftone output to animated printing effects. Each builds on the previous, gradually engaging more of Dotmatrix's physical-simulation features.
### Exercise 1: Classic Halftone Print

![Classic Halftone Print result](/img/instruments/videomancer/dotmatrix/dotmatrix_ex1_s1.png)
*Classic Halftone Print — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A static halftone print that resembles a newspaper photograph or vintage computer printout.

#### Key Concepts

- Inverse-luma dot sizing (dark = big dot)
- Grid cell size determines halftone coarseness
- Ink density and paper color set the print's character

#### Video Source

A live camera feed or recorded footage with a good range of tones (faces, landscapes, or high-contrast subjects work well.)

#### Steps

1. **Basic halftone**: Start with all knobs at noon and all switches Off. The image appears as a grid of dots on white paper. Dark areas are dense; bright areas are sparse.
2. **Coarseness**: Flip **Head** (Switch 7) between 9-Pin and Inkjet. The 9-Pin mode creates a coarser grid; Inkjet creates a finer, denser dot field.
3. **Dot range**: Sweep **Dot Size** (Knob 2) from 0% to 100%. Watch how the tonal range expands: at low values, even dark areas have tiny dots; at high values, dark areas become solid blocks of ink.
4. **Ink and paper**: Turn **Ink Dens** (Knob 3) to about 80% for a strong, dark print. Then rotate **Paper Hue** (Knob 6) slowly through its full range to audition white, green, blue, and cream paper stocks.
5. **Worn ribbon**: Pull **Ribbon** (Knob 4) down to about 20%. The print fades as though the ribbon is exhausted. Now push it back up to 100% (fresh ribbon, strong impression.)

#### Settings

| Control | Value |
|---------|-------|
| Print Sp | 50% |
| Dot Size | 75% |
| Ink Dens | 80% |
| Ribbon | 100% |
| Jitter | 0% |
| Paper Hue | 270° |
| Head | 9-Pin |
| Dir | Uni |
| Draft | Off |
| Feed | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Animated Bidirectional Printing

![Animated Bidirectional Printing result](/img/instruments/videomancer/dotmatrix/dotmatrix_ex2_s1.png)
*Animated Bidirectional Printing — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated print sequence that mimics a real dot-matrix printer in action, complete with bidirectional sweeps and draft-quality speed.

#### Key Concepts

- The sweep animation reveals the image progressively
- Bidirectional printing alternates direction per row
- Draft mode reduces dot density for a speed effect

#### Video Source

Footage with moderate movement: a slowly rotating object, drifting clouds, or a person speaking. Movement helps you see the print head "chasing" the action.

#### Steps

1. **Enable feed**: Flip **Feed** (Switch 10) to On. The image now builds up line by line as the print head sweeps across. Set **Print Sp** (Knob 1) to about 30% so you can watch the sweep progress.
2. **Bidirectional**: Flip **Dir** (Switch 8) to Bidi. Even rows now print left-to-right, odd rows right-to-left. Watch the sweep alternate direction with each new line.
3. **Draft mode**: Flip **Draft** (Switch 9) to On. Every other dot column is skipped, creating a vertically striped pattern. Just like a real printer in draft mode (faster, lighter, more economical.)
4. **Add jitter**: Turn **Jitter** (Knob 5) to about 40%. The dots wobble slightly, adding organic imprecision to the mechanical sweep.
5. **Old paper**: Set **Paper Hue** (Knob 6) past 270° for warm, yellowed paper. Lower **Ribbon** (Knob 4) to about 35%. The combination looks like an old printout found in a filing cabinet.

#### Settings

| Control | Value |
|---------|-------|
| Print Sp | 30% |
| Dot Size | 60% |
| Ink Dens | 70% |
| Ribbon | 35% |
| Jitter | 40% |
| Paper Hue | 300° |
| Head | 9-Pin |
| Dir | Bidi |
| Draft | On |
| Feed | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Ghost Print Overlay

![Ghost Print Overlay result](/img/instruments/videomancer/dotmatrix/dotmatrix_ex3_s1.png)
*Ghost Print Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A hybrid image where the original video shows through a semi-transparent halftone grid, creating a textured overlay that adds depth without fully replacing the source.

#### Key Concepts

- The Mix fader blends halftone with original video
- Partial mix creates a translucent overlay effect
- Fine dot grid (Inkjet mode) integrates more smoothly

#### Video Source

High-color footage: flowers, neon signs, painted surfaces, or anything with rich saturation. The color contrast between the monochrome dots and the original video is essential.

#### Steps

1. **Fine grid**: Set **Head** (Switch 7) to Inkjet. The smaller 4×4 grid creates a denser, smoother dot field that blends more naturally with the source.
2. **Strong halftone**: Set **Dot Size** (Knob 2) to about 70%, **Ink Dens** (Knob 3) to about 90%. You want a bold halftone to blend against.
3. **Paper contrast**: Rotate **Paper Hue** (Knob 6) to about 180° for cool blue paper. The tinted paper provides color contrast against the warm tones of the source.
4. **Blend**: Now slowly pull the **Mix** fader (Fader 12) down from 100% toward 50%. The original colors begin to show through the halftone dots, creating a layered visual where ink dots and source video coexist.
5. **Sweet spot**: Find the balance point where the halftone texture is clearly visible but the source content is still recognizable. Typically this is around 50–65%.
6. **Animate**: Enable **Feed** (Switch 10) with a moderate **Print Sp** to watch the halftone layer build up over the live source.

#### Settings

| Control | Value |
|---------|-------|
| Print Sp | 50% |
| Dot Size | 70% |
| Ink Dens | 90% |
| Ribbon | 80% |
| Jitter | 15% |
| Paper Hue | 180° |
| Head | Inkjet |
| Dir | Uni |
| Draft | Off |
| Feed | On |
| Bypass | Off |
| Mix | 55% |

---
## Glossary

- **Bidirectional Printing**: A printing technique where the print head prints in both directions (left-to-right and right-to-left) on alternating rows to save time.

- **DDS (Direct Digital Synthesis)**: A technique for generating a position or frequency using an accumulator that wraps around at a fixed boundary, used here to drive the sweep animation.

- **Draft Mode**: A reduced-quality print setting that skips dots to increase printing speed, producing a lighter, vertically striped output.

- **Halftone**: A reproduction technique that simulates continuous tones using dots of varying size; large dots create dark areas, small dots create light areas.

- **LFSR (Linear Feedback Shift Register)**: A hardware-efficient pseudo-random number generator that produces a repeating but unpredictable bit sequence, used here for dot jitter.

- **Manhattan Distance**: The sum of absolute differences along each axis ($|dx| + |dy|$), producing diamond-shaped contours; an efficient alternative to Euclidean distance for FPGA implementation.

- **Print Head**: The mechanical component of a dot-matrix printer that sweeps horizontally across paper, striking pins through an inked ribbon to form dots.

- **Ribbon Fade**: The gradual weakening of ink impressions as a printer ribbon's ink supply is depleted through repeated use.

---
