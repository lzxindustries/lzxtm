---
draft: true
sidebar_position: 87
slug: /instruments/videomancer/dolly
title: "Dolly"
image: /img/instruments/videomancer/dolly/dolly_hero_s1.png
description: "Every broadcast control room has a button that shrinks the on-screen talent into a box and slides that box to any corner of the frame — usually to make room for a map, a graphic, or a second camera feed."
---

![Dolly hero image](/img/instruments/videomancer/dolly/dolly_hero_s1.png)
*Dolly shrinking and repositioning a live video feed into a bordered picture-in-picture window over a hue-tinted background.*

---

## Overview

**Dolly** is a real-time ***digital video effects*** (DVE) processor. It takes the input video and repositions, resizes, and reshapes it within the output frame: the fundamental broadcast effect used for picture-in-picture inserts, split-screen compositions, and on-air graphics. Behind the floating window sits a colored background whose hue you choose, and around the window's edge you can draw a crisp border in white or black.

The effect is straightforward but the creative range is wide. At subtle settings, Dolly places a reduced copy of the input in one corner of the screen: the classic news-anchor cutaway. Push it further, and the image compresses into a thin horizontal sliver or a tall vertical stripe. Flip it with mirror, dissolve it with mix, or let it breathe against a vivid colored field. Everything updates per frame, so sweeping the position and size knobs produces smooth, animated camera-move effects in real time.

:::tip
Because Dolly writes each scanline into a ***line buffer*** before reading it back at a different rate, horizontal scaling is truly resampled: not just cropped. The image genuinely shrinks or stretches, preserving all its content at any size.
:::

### What's In a Name?

A ***dolly*** is the wheeled cart that carries a film camera for smooth tracking shots. "Dolly in" pushes the camera toward the subject; "dolly out" pulls it away. The name fits because this program moves the image through the frame and changes its apparent size: like a camera on rails, sliding the viewer's window of attention across the scene.

---

## Quick Start

1. Turn **Size** (Knob 1) clockwise past the first quarter. The input video shrinks into a floating rectangle surrounded by a dark background. You're looking at a picture-in-picture.
2. Sweep **Position X** (Knob 3) and **Position Y** (Knob 4) to slide the floating image around the frame. The background fills in wherever the image isn't.
3. Turn up **Border Width** (Knob 6) to draw a white frame around the image. Toggle **Border Color** (Switch 7) to flip it to black.
4. Rotate **BKG Hue** (Knob 2) through the full circle. The background color sweeps through the spectrum while the image window rides on top.

---

## Parameters

![Videomancer front panel with Dolly loaded](/img/instruments/videomancer/dolly/dolly_control_panel.png)
*Videomancer's front panel with Dolly active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Size

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Size** controls how much of the output frame the input image occupies. At the minimum setting, the image fills the entire screen: no background is visible and the effect is essentially transparent. As you turn the knob clockwise, the image shrinks toward a small rectangle. At maximum, the image reduces to a tiny point.

Size is the gateway to everything else in Dolly. Until the image is smaller than full screen, the background, border, position, and aspect controls have nothing to act on. Start here.

---

### Knob 2 — BKG Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |

**BKG Hue** selects the hue angle of the background color that fills the space around the image window. Sweeping through the full rotation cycles the background through reds, yellows, greens, cyans, blues, and magentas. The hue is generated from a pair of cosine and sine lookup tables that drive the U and V chroma channels directly.

:::note
BKG Hue controls only the chrominance of the background. Use the **BKG Lum** toggle (Switch 8) to set its brightness. At the Dark setting, the background is deeply saturated. At the Bright setting, the colors wash out toward pastels.
:::

---

### Knob 3 — Position X

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Position X** sets the horizontal center of the image window. At the minimum value, the image is anchored to the left edge of the frame. At the midpoint, it sits centered. At the maximum, it rides against the right edge. The position maps linearly across the full active width of the output raster.

---

### Knob 4 — Position Y

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Position Y** sets the vertical center of the image window. At the minimum value, the image sits at the top of the frame. At the midpoint, it is vertically centered. At the maximum, it drops to the bottom. Combined with **Position X**, you can place the image anywhere in the output frame.

---

### Knob 5 — Aspect

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Aspect** adjusts the horizontal width of the image window independently of its height, distorting the ***aspect ratio***. At the midpoint, the image has its natural proportions: the horizontal and vertical scales match. Turning counterclockwise squeezes the image horizontally into a tall, narrow column. Turning clockwise stretches it into a wide, flat strip.

:::tip
Extreme aspect settings combined with a colored background and bold border can create striking split-screen or letterbox-style compositions without any external routing.
:::

---

### Knob 6 — Border Width

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Border Width** controls the thickness of a decorative frame drawn around the image window. At the minimum value, no border is visible. As you increase the control, a solid-color border appears and grows outward from the image edges. The border expands equally on all four sides.

---

### Switch 7 — Border Color

| Property | Value |
|----------|-------|
| Off | White |
| On | Black |
| Default | White |

**Border Color** selects the color of the border frame. In the first position, the border is bright white: maximum luminance with neutral chroma. In the second position, the border is solid black. Both are achromatic: the border carries no color information.

---

### Switch 8 — BKG Lum

| Property | Value |
|----------|-------|
| Off | Dark |
| On | Bright |
| Default | Dark |

**BKG Lum** sets the luminance of the background. In the first position, the background is dark: a low luminance value that produces deep, saturated versions of the hue selected by **BKG Hue**. In the second position, the background is bright: a high luminance value that produces lighter, pastel versions of the same hue.

---

### Switch 9 — Edge Clamp

| Property | Value |
|----------|-------|
| Off | Clamp |
| On | Black |
| Default | Clamp |

**Edge Clamp** determines what happens when the horizontal scaling engine reads beyond the boundaries of the original image data. In the first position, the last valid pixel repeats along the edge: a ***clamping*** behavior that extends the image border naturally. In the second position, out-of-bounds reads return black. The difference is most visible when the aspect ratio is pushed to extremes and the DDA read address overshoots the source line.

---

### Switch 10 — Mirror

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mirror** horizontally flips the image within the DVE window. In the first position, the image is normal. In the second position, the read address runs backward: the ***DDA*** (Digital Differential Analyzer) counts from right to left: producing a mirror reflection. Only the image content is mirrored; the border and background are unaffected.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Dolly processing. The sync delay pipeline still runs, so there is no timing glitch on transition. Use Bypass for instant A/B comparison between the raw input and the DVE composited result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original dry input and the wet DVE output. At the minimum value, the output is entirely the unprocessed input: the DVE window, border, and background are invisible. At the maximum value, the output is entirely the composited DVE result. Intermediate values blend the two, producing a ghostly overlay where the input video shows through the background and border regions.

:::tip
Mix at an intermediate setting lets the source video bleed through the background, creating a translucent picture-in-picture effect. This is especially striking with a saturated **BKG Hue** (the background tints the input without fully hiding it.)
:::

---

## Background

### Digital video effects

The ***DVE***: digital video effect: is one of the foundational tools of broadcast television production. Introduced in the late 1970s with hardware like the Ampex ADO and Quantel Mirage, the DVE made it possible to shrink, position, rotate, and fly video images around the screen in real time. Before DVEs, compositing two video sources required analog switching or chroma keying. The DVE gave directors the ability to place a reduced copy of one source over another: the picture-in-picture technique that became a staple of news, sports, and entertainment programming.

Dolly implements the core DVE operation: positioning a scaled copy of the input within the output raster, surrounded by a configurable background and border. It doesn't rotate or apply perspective, but its position, size, aspect, and mix controls cover the most commonly used DVE functions.

### Line buffer architecture

Traditional frame-based DVEs store entire frames of video in memory and read them back at arbitrary positions. Dolly takes a more constrained but resource-efficient approach: it uses ***line buffers***: dual-port BRAMs that store one scanline at a time. Each input line is written sequentially into the buffer. The output reads from the same buffer at addresses computed by a horizontal scaling engine.

This architecture means that vertical scaling is implicit: the same input line is simply repeated or skipped as needed: while horizontal scaling is explicit, driven by a ***DDA*** (Digital Differential Analyzer) that computes a new read address for every output pixel.

:::note
Because the line buffer holds only one scanline, Dolly cannot perform vertical interpolation. Vertical scaling is nearest-neighbor: lines are either duplicated or dropped. Horizontal scaling, however, is address-accurate: each output pixel reads from a precisely computed source position.
:::

### DDA horizontal scaling

The ***DDA*** (Digital Differential Analyzer) is a classic algorithm for drawing lines and computing uniformly spaced samples. In Dolly, it computes the source read address for each output pixel during the horizontal active region.

A DDA works by accumulating a fixed step value on every pixel clock. The integer part of the accumulator becomes the read address into the line buffer. If the step is less than one, several output pixels read the same source pixel: the image is magnified. If the step is greater than one, some source pixels are skipped: the image is minified.

To avoid expensive runtime division, Dolly uses a ***reciprocal lookup table*** with 32 entries. The image width (after size and aspect scaling) selects an entry from the table, and that entry becomes the DDA step. This replaces a divide-per-frame with a single table read (an important optimization on a small FPGA.)

### Hue generation

The background color is generated from a pair of lookup tables that encode a quarter-cosine and quarter-sine wave, each with 64 entries at 10-bit resolution. The **BKG Hue** knob selects an index into these tables, producing U and V chroma values that trace a circle through color space as the knob sweeps from minimum to maximum. The luminance is set independently by the **BKG Lum** toggle: either a low value for dark, saturated backgrounds or a high value for bright, pastel backgrounds.

This approach produces smooth, continuous color sweeps without requiring a full HSV-to-YUV conversion on the FPGA.


---

## Signal Flow

### Signal Flow Notes

The critical feature of Dolly's pipeline is the ***dual path*** through the line buffer. Input data is written into the buffer sequentially: one pixel per clock, advancing linearly along the scanline. Simultaneously, the output reads from the buffer at addresses computed by the DDA, which may advance faster, slower, or even backward relative to the write pointer. This decoupled read/write architecture is what allows horizontal scaling and mirroring within a single scanline's worth of storage.

The compositor sits downstream of the line buffer read and selects among three sources: image data, border color, or background color: based on a region code computed two clocks earlier (the pipeline delay matches the line buffer's two-clock read latency). The mix stage then blends the composited result with the delayed original input, preserving the option to dissolve between the DVE output and the unprocessed source.


---

## Exercises

These exercises progress from basic picture-in-picture to creative compositions. Each builds on the previous, introducing more controls.
### Exercise 1: Classic Picture-in-Picture

![Classic Picture-in-Picture result](/img/instruments/videomancer/dolly/dolly_ex1_s1.png)
*Classic Picture-in-Picture — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A traditional broadcast-style picture-in-picture insert: the input video miniaturized in one corner of the screen with a white border.

#### Key Concepts

- Size shrinks the image within the frame
- Position X and Position Y place the image anywhere on screen
- Border Width draws a frame around the image window

#### Video Source

A camera feed or recorded footage with a clear subject: a talking head, a scene with visible details. Choose material where you can easily tell the image has been repositioned and reduced.

#### Steps

1. Turn **Size** (Knob 1) clockwise to about 40%. The input video shrinks into a rectangle centered on screen, surrounded by a dark background.
2. Sweep **Position X** (Knob 3) clockwise to push the image toward the upper-right corner of the screen.
3. Sweep **Position Y** (Knob 4) counterclockwise to raise the image toward the top of the frame.
4. Turn up **Border Width** (Knob 6) to about 20%. A white border appears around the miniaturized image.
5. Observe how the image content is preserved at the smaller size (details are visible, not cropped.)

#### Settings

| Control | Value |
|---------|-------|
| Size | ~40% |
| BKG Hue | 180° |
| Position X | ~80% |
| Position Y | ~20% |
| Aspect | 50% |
| Border Width | ~20% |
| Border Color | White |
| BKG Lum | Dark |
| Edge Clamp | Clamp |
| Mirror | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Colored Background Composition

![Colored Background Composition result](/img/instruments/videomancer/dolly/dolly_ex2_s1.png)
*Colored Background Composition — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A picture-in-picture window floating over a vivid colored background, then explore dissolving the background with the Mix fader.

#### Key Concepts

- BKG Hue sweeps the background through the color spectrum
- BKG Lum switches between dark saturated and bright pastel tones
- Mix crossfades between the DVE composite and the raw input

#### Video Source

High-contrast footage: bold shapes and strong edges work well to distinguish the image from the background. Geometric patterns or colorful subjects are ideal.

#### Steps

1. Set **Size** (Knob 1) to about 30% to create a small floating image.
2. Center the image with **Position X** (Knob 3) and **Position Y** (Knob 4) at their midpoints.
3. Rotate **BKG Hue** (Knob 2) slowly through a full turn. The background color sweeps through the spectrum: red, yellow, green, cyan, blue, magenta, and back. Choose a hue you like.
4. Toggle **BKG Lum** (Switch 8) to **Bright**. The background shifts from deep, saturated color to a lighter, pastel version of the same hue.
5. Pull **Mix** (Fader 12) down to about 50%. The source video bleeds through the background, creating a translucent overlay.
6. Add **Border Width** (Knob 6) at about 15% with **Border Color** (Switch 7) set to **Black** for a contrasting frame.

#### Settings

| Control | Value |
|---------|-------|
| Size | ~30% |
| BKG Hue | ~120° |
| Position X | 50% |
| Position Y | 50% |
| Aspect | 50% |
| Border Width | ~15% |
| Border Color | Black |
| BKG Lum | Bright |
| Edge Clamp | Clamp |
| Mirror | Off |
| Bypass | Off |
| Mix | ~50% |

---

### Exercise 3: Anamorphic Mirror Strip

![Anamorphic Mirror Strip result](/img/instruments/videomancer/dolly/dolly_ex3_s1.png)
*Anamorphic Mirror Strip — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A stretched, mirrored image strip: reminiscent of a funhouse mirror or anamorphic film format: with a bold border and colored background.

#### Key Concepts

- Aspect distorts the image proportions for dramatic effect
- Mirror flips the image horizontally within the DVE window
- Edge Clamp controls what appears at the boundaries of the distorted image

#### Video Source

Footage with strong horizontal features: landscapes, architecture, or subjects with recognizable left-right symmetry. A face works dramatically with the mirror effect.

#### Steps

1. Set **Size** (Knob 1) to about 30% and center the image with **Position X** and **Position Y** at their midpoints.
2. Turn **Aspect** (Knob 5) fully clockwise. The image stretches horizontally into a wide, flat strip.
3. Toggle **Mirror** (Switch 10) to **On**. The image flips horizontally within the window (text reads backward, left and right swap.)
4. Toggle **Edge Clamp** (Switch 9) to **Black**. If the DDA reads beyond the source bounds, the edges go to black instead of repeating the last pixel.
5. Add a thick border: turn **Border Width** (Knob 6) to about 40% and set **Border Color** (Switch 7) to **White**.
6. Choose a complementary **BKG Hue** (Knob 2) and toggle **BKG Lum** (Switch 8) to **Bright** for a pastel field behind the strip.
7. Slowly sweep **Aspect** (Knob 5) back toward the center and watch the image progressively restore its natural proportions.

#### Settings

| Control | Value |
|---------|-------|
| Size | ~30% |
| BKG Hue | ~270° |
| Position X | 50% |
| Position Y | 50% |
| Aspect | ~90% |
| Border Width | ~40% |
| Border Color | White |
| BKG Lum | Bright |
| Edge Clamp | Black |
| Mirror | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Aspect Ratio**: The proportional relationship between the width and height of an image; distorting it stretches or squeezes the picture.

- **BRAM**: Block RAM; dedicated memory blocks on the FPGA used to store scanline data for the line buffer.

- **Compositor**: A stage that combines multiple visual sources (image, border, background) into a single output based on spatial region.

- **DDA**: Digital Differential Analyzer; an algorithm that computes uniformly spaced sample positions by accumulating a fixed step value per clock cycle.

- **DVE**: Digital Video Effect; a broadcast technology for resizing, repositioning, and transforming video images in real time.

- **Line Buffer**: A dual-port memory that stores one scanline of video; input writes sequentially while output reads at computed addresses for scaling.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness.

- **Picture-in-Picture**: A display technique placing a reduced copy of one video source over another, commonly used in news and sports broadcasts.

- **Raster**: The grid of horizontal scanlines that make up a video frame, scanned left-to-right, top-to-bottom.

- **Reciprocal LUT**: A lookup table that stores precomputed 1/x values, replacing expensive runtime division with a single table read.

---
