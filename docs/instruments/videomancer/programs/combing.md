---
draft: true
sidebar_position: 61
slug: /instruments/videomancer/combing
title: "Combing"
image: /img/instruments/videomancer/combing/combing_hero_s1.png
description: "Before the world went progressive, all television was interlaced."
---

![Combing hero image](/img/instruments/videomancer/combing/combing_hero_s1.png)
*Combing applying interlace comb-teeth artifacts to a live video source, rendering alternating scanlines as shimmering striped fringes along motion edges.*

---

## Overview

**Combing** recreates the visual artifact that occurs when interlaced video is displayed on a progressive monitor without deinterlacing. In the real world, this effect appears as a series of fine horizontal teeth along the edges of moving objects: each pair of adjacent lines shows data from a different moment in time, and the mismatch creates a distinctive fringe. Combing takes this broadcast-era glitch and turns it into a controllable visual tool: every other scanline is replaced with data from the previous line, producing the characteristic sawtooth edges that television engineers once struggled to eliminate.

At subtle settings, the comb teeth are delicate, appearing only where motion creates a difference between adjacent lines. Cranked up, Combing transforms the entire image into a bold striped pattern, alternating between the current picture and its one-line-delayed ghost. A checkerboard mode toggles per-pixel in addition to per-line, dissolving the image into a fine grid. With animation enabled, the comb pattern shifts each frame, creating a shimmering, flickering texture that evokes the look of unstable analog video.

:::tip
Combing is most visible when there is ***motion*** in the source video. With a still image, the current and previous scanlines are identical, so no comb teeth appear. Feed it a moving camera or animated source for the full effect.
:::

### What's In a Name?

The name directly references ***combing artifacts***, the horizontal fringe pattern that appears when interlaced video fields are displayed simultaneously on a progressive screen. The alternating lines look like the teeth of a comb: hence the name. In broadcast television, combing is considered a defect, something to be eliminated by proper deinterlacing. Videomancer's **Combing** program flips that relationship: the artifact is no longer a mistake but an instrument, conjuring the spectral shimmer of old analog signals on command.

---

## Quick Start

1. Feed a video signal with visible movement. **Comb Depth** (Knob 1) starts at maximum: every other scan line is replaced with data from the previous line, creating visible comb teeth along motion edges.
2. Flip **Pattern** (Switch 8) to **Checker**. The alternating pattern now toggles per-pixel as well as per-line, breaking the image into a fine checkerboard of live and delayed pixels.
3. Turn on **Animate** (Switch 9). The comb pattern shifts by one line each frame, creating a shimmering, flickering texture across the image.
4. Sweep **Line Offset** (Knob 3) to shift the vertical phase of the comb pattern. The stripe grid slides up and down the screen as you turn.

---

## Parameters

![Videomancer front panel with Combing loaded](/img/instruments/videomancer/combing/combing_control_panel.png)
*Videomancer's front panel with Combing active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Comb Depth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Comb Depth** controls the strength of the alternate-line replacement. At its minimum, selected lines pass live data through unchanged: no visible combing occurs. As the value increases, selected lines blend progressively more of the delayed scanline data into the output. At maximum (the default), selected lines display 100% of the previous scanline's data, creating full-strength comb teeth wherever the image differs between adjacent lines.

---

### Knob 2 — Blend

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Blend** softens the transition between live and delayed scan lines. At its minimum (the default), the comb pattern is a hard, binary alternation: each line is either fully live or fully delayed. As Blend increases, neighboring lines receive a partial cross-fade of live and delayed data, smoothing the sharp comb teeth into a gentler vertical gradient. At maximum, the distinction between live and delayed lines dissolves into a uniform average.

---

### Knob 3 — Line Offset

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Line Offset** shifts the vertical phase of the comb pattern. At minimum, the pattern begins at the first line of the frame. As Line Offset increases, the odd/even assignment of lines shifts downward, changing which lines display live data and which display delayed data. This creates a scrolling effect as you sweep the knob.

:::tip
Combine **Line Offset** with **Animate** for emergent visual effects. Animation shifts the pattern by one line per frame; Line Offset adds a fixed displacement on top. Together they create patterns that drift and shimmer in complex ways.
:::

---

### Knob 4 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contrast** adjusts the tonal range of the processed output. At the default center position, contrast is at unity: the signal passes through without gain alteration. Turning counterclockwise compresses the tonal range toward mid-gray, flattening the image. Turning clockwise expands the tonal range, increasing the separation between bright and dark areas and making comb teeth more visually prominent against the background.

---

### Knob 5 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** shifts the overall luminance of the processed output. At the default center position, no shift occurs. Turning counterclockwise darkens the image; turning clockwise brightens it. Brightness is applied to both live and delayed lines equally, shifting the entire image up or down the tonal scale without changing the comb pattern itself.

---

### Knob 6 — Fade

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Fade** attenuates the overall brightness of the output. At maximum (the default), the image passes through at full intensity. As Fade decreases, the output dims uniformly toward black. Fade operates independently of **Contrast** and **Brightness**, providing a simple master dimmer for the result.

---

### Switch 7 — Field

| Property | Value |
|----------|-------|
| Off | Odd |
| On | Even |
| Default | Odd |

**Field** selects which set of scan lines is treated as the delayed field. When set to **Odd**, odd-numbered lines display delayed data and even lines pass live data through. Flipping to **Even** reverses this assignment. The visual effect is a one-line vertical shift of the entire comb pattern (the same stripes, just moved up or down by a single line.)

---

### Switch 8 — Pattern

| Property | Value |
|----------|-------|
| Off | Lines |
| On | Checker |
| Default | Lines |

**Pattern** selects between two comb modes. In **Lines** mode, the alternation is strictly by scan line: each line is either fully live or fully delayed. In **Checker** mode, the alternation also toggles per-pixel along each line, creating a fine ***checkerboard*** pattern where adjacent pixels within the same line can differ. Checkerboard mode produces a denser, more textured artifact compared to the broad horizontal stripes of Lines mode.

---

### Switch 9 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Animate** enables per-frame animation of the comb pattern. When **Off**, the pattern is static: each line is consistently assigned to live or delayed data from frame to frame. When set to **On**, the pattern shifts by one line each frame, causing the comb teeth to scroll vertically through the image. The animation cycles every 256 frames.

:::note
Animation is most visible in **Lines** mode. In **Checker** mode, the per-frame shift creates a rapid flickering that can appear as a uniform shimmer rather than a discernible scroll.
:::

---

### Switch 10 — Invert Y

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert Y** applies a bitwise complement to the luminance channel before comb processing. When **Off**, the Y channel passes to the comb decision stage unchanged. When set to **On**, every luminance value is inverted: bright becomes dark and dark becomes bright. This inversion happens ***before*** the line buffers, so the delayed scanline data stored in block RAM also reflects the inverted luminance.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Combing processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the combed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** blends between the dry (unprocessed) signal and the wet (combed) signal. At minimum, the output is 100% dry: you see the original input with no combing visible. At maximum (the default), the output is 100% wet: you see the full comb effect. Intermediate positions produce a transparent overlap of the original and processed images, useful for dialing in subtle combing textures.

---

## Background

### Interlaced video

Before the age of flat screens and digital displays, all television was ***interlaced***. Each frame was split into two ***fields***: one containing the odd-numbered scan lines, the other containing the even-numbered lines. The fields were transmitted and displayed in rapid alternation: 60 fields per second in NTSC, 50 in PAL: but each complete frame only appeared 30 or 25 times per second. This halved the bandwidth required to transmit smooth motion, because the human eye is more sensitive to flicker than to fine spatial detail. It was one of the most elegant engineering compromises in the history of broadcasting.

### Comb artifacts

When interlaced footage is displayed on a ***progressive*** monitor: one that draws every line in each frame: both fields must be shown simultaneously. If the image is perfectly still, the two fields mesh seamlessly. But if the subject has moved between fields, the odd and even lines no longer align. The result is a series of fine horizontal fringes along motion edges that look like the teeth of a comb. Broadcast engineers call this a ***combing artifact***, and it's one of the defining visual signatures of improperly deinterlaced video.

Videomancer's Combing program recreates this effect digitally. Instead of storing two temporal fields, it uses a one-line delay buffer: the previous scanline's data is stored in ***block RAM*** and read back as the current scanline arrives. On alternating lines, the delayed data replaces (or blends with) the live data, producing the characteristic comb teeth wherever the image differs from one line to the next.

### Line buffers

The heart of the Combing program is a set of three ***line buffers***: one for each of the Y, U, and V video channels. Each buffer is a block RAM inside the FPGA, holding up to 1,024 pixels of 10-bit data. As each scanline arrives, its pixel values are written into the buffer. At the same horizontal position, the buffer provides the data from the previous scanline. This one-line delay is what makes the comb pattern possible: selected lines can substitute "old" pixel data while non-selected lines display the live input. The write and read happen simultaneously, one clock cycle apart, so the previous line's data is always available in time for the current pixel decision.


---

## Signal Flow

### Signal Flow Notes

The core interaction is between the line buffers and the comb pattern decision. At each pixel clock, the FPGA writes the current input to block RAM and reads the value stored there from the previous scanline. The pattern decision then selects: per-line, or per-pixel in checkerboard mode: whether that pixel should show the live input or a weighted blend of delayed and live data controlled by **Comb Depth**.

The comb pattern is position-dependent: the current line number (offset by **Line Offset** and optionally incremented by the frame counter) determines the line phase. In checkerboard mode, the horizontal pixel position also contributes, creating a two-dimensional alternation. The original video data is separately piped through a six-clock shift register to align with the processing pipeline, and this delayed copy serves as the dry input to the final wet/dry interpolator mix. All three channels (Y, U, V) pass through identical comb processing: the only channel-specific operation is **Invert Y**, which inverts luminance before combing without affecting chrominance.

:::tip
**Processing order matters.** Y inversion happens *before* the line buffer write, so delayed data in the BRAMs is already inverted when Invert Y is active. Toggling Invert Y mid-stream causes a one-line transition artifact as the buffer flushes old data.
:::


---

## Exercises

These exercises progress from basic line combing to complex animated textures. Each builds on the previous, gradually engaging more of the comb pattern engine.
### Exercise 1: Classic Comb Teeth

![Classic Comb Teeth result](/img/instruments/videomancer/combing/combing_ex1_s1.png)
*Classic Comb Teeth — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Recreate the classic interlace combing artifact: fine horizontal fringes along motion edges.

#### Key Concepts

- Combing replaces alternating scanlines with previous-line data
- Comb Depth controls the strength of the replacement
- The effect is most visible on moving subjects

#### Video Source

A live camera feed with a slowly moving subject (a hand waving, a person walking, or a swinging pendulum.)

#### Steps

1. **Full combing**: With **Comb Depth** (Knob 1) at maximum, observe the comb teeth along edges where the subject is moving. Still areas of the frame appear clean.
2. **Reduce depth**: Slowly turn Comb Depth counterclockwise. The teeth grow fainter as less delayed data is mixed in. At minimum, the comb effect disappears entirely.
3. **Flip field**: Toggle **Field** (Switch 7) from **Odd** to **Even**. The stripe pattern shifts by one line (lines that were live become delayed, and vice versa.)
4. **Shift phase**: Sweep **Line Offset** (Knob 3) from minimum to maximum. The entire comb pattern slides vertically through the screen.

#### Settings

| Control | Value |
|---------|-------|
| Comb Depth | 100% |
| Blend | 0% |
| Line Offset | 0% |
| Contrast | ~50% |
| Brightness | ~50% |
| Fade | 100% |
| Field | Odd |
| Pattern | Lines |
| Animate | Off |
| Invert Y | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Checkerboard Shimmer

![Checkerboard Shimmer result](/img/instruments/videomancer/combing/combing_ex2_s1.png)
*Checkerboard Shimmer — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Transform the source video into an animated checkerboard texture by combining per-pixel alternation with per-frame animation.

#### Key Concepts

- Checker mode alternates per-pixel in addition to per-line
- Animation shifts the pattern every frame
- Y inversion changes the contrast of the comb effect

#### Video Source

A video source with strong color contrasts and slow movement: close-up of colorful objects, fruit, or an abstract pattern.

#### Steps

1. **Enable checkerboard**: Set **Pattern** (Switch 8) to **Checker**. The comb effect now alternates per-pixel along each line, breaking the image into a fine grid of live and delayed pixels.
2. **Animate the grid**: Turn on **Animate** (Switch 9). The checkerboard pattern shifts each frame, creating a shimmering, vibrating texture across the entire image.
3. **Invert luminance**: Toggle **Invert Y** (Switch 10) to **On**. Brightness values flip before entering the comb engine, changing the contrast relationship between live and delayed pixels.
4. **Half-strength mix**: Pull **Mix** (Fader 12) back to about 60%. The checkerboard texture becomes semi-transparent, letting the original image show through underneath.
5. **Offset**: Sweep **Line Offset** (Knob 3) to about 50%. The checkerboard grid shifts vertically, changing which pixels are live and which are delayed.

#### Settings

| Control | Value |
|---------|-------|
| Comb Depth | 100% |
| Blend | 0% |
| Line Offset | ~50% |
| Contrast | ~50% |
| Brightness | ~50% |
| Fade | 100% |
| Field | Odd |
| Pattern | Checker |
| Animate | On |
| Invert Y | On |
| Bypass | Off |
| Mix | ~60% |

---

### Exercise 3: Drifting Interference

![Drifting Interference result](/img/instruments/videomancer/combing/combing_ex3_s1.png)
*Drifting Interference — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Produce a drifting interference pattern using partial comb depth, animation, and reduced mix (a vintage video texture that hums gently across the frame.)

#### Key Concepts

- Partial Comb Depth produces translucent comb teeth
- Combining Line Offset with Animate produces drifting, organic textures
- The wet/dry mix allows subtle layered blending of the effect

#### Video Source

Any video footage. High-detail material like landscapes, architecture, or close-up textures works especially well.

#### Steps

1. **Moderate depth**: Set **Comb Depth** (Knob 1) to about 60%. The comb teeth are present but not fully opaque (you can still see through them to the live data underneath.)
2. **Set offset**: Turn **Line Offset** (Knob 3) to about 40%. The comb pattern shifts vertically, creating a misalignment between the comb grid and the video content.
3. **Animate**: Enable **Animate** (Switch 9). The pattern now drifts steadily through the image at one line per frame.
4. **Invert luminance**: Toggle **Invert Y** (Switch 10) to **On**. The tonal inversion interacts with the partial comb depth, creating a ghostly negative-image texture on selected lines.
5. **Soften the blend**: Pull **Mix** (Fader 12) back to about 80%. The overall effect softens into a subtle, translucent texture (a vintage video haze layered over the source.)

#### Settings

| Control | Value |
|---------|-------|
| Comb Depth | ~60% |
| Blend | ~70% |
| Line Offset | ~40% |
| Contrast | ~50% |
| Brightness | ~40% |
| Fade | ~60% |
| Field | Odd |
| Pattern | Lines |
| Animate | On |
| Invert Y | On |
| Bypass | Off |
| Mix | ~80% |

---
## Glossary

- **Block RAM (BRAM)**: A dedicated memory block inside the FPGA used for storing scanline data at high speed, without consuming general-purpose logic cells

- **Checkerboard**: A two-dimensional alternation pattern where adjacent pixels differ both horizontally and vertically, like the squares of a chessboard

- **Comb Artifact**: A visual distortion that appears when interlaced video fields are displayed simultaneously on a progressive monitor, creating horizontal fringe patterns along moving edges

- **Field**: One half of an interlaced video frame, containing either the odd-numbered or even-numbered scan lines

- **Interlacing**: A video display technique that splits each frame into two interleaved fields, transmitting odd and even lines separately to reduce bandwidth

- **Line Buffer**: A block RAM that stores one complete scanline of video data, allowing the program to compare or combine the current line with the previous one

- **Pipeline**: A series of sequential processing stages inside the FPGA where data passes from one stage to the next on each clock cycle

- **Progressive**: A video display method that draws every scan line in sequence from top to bottom, as opposed to interlacing

- **Scan Line**: A single horizontal row of pixels in a video frame

---
