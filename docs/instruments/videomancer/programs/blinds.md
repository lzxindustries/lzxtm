---
draft: true
sidebar_position: 22
slug: /instruments/videomancer/blinds
title: "Blinds"
image: /img/instruments/videomancer/blinds/blinds_hero_s1.png
description: "Every broadcast engineer knows the venetian blind wipe — a grid of horizontal or vertical slats that open or close to reveal or conceal a video source."
---

![Blinds hero image](/img/instruments/videomancer/blinds/blinds_hero_s1.png)
*Blinds slicing a video feed into horizontal slats that cascade open in sequence, revealing the source image through a rolling venetian shutter.*

---

## Overview

**Blinds** is a broadcast-style transition effect that divides your video into parallel slats: like a set of venetian blinds: and opens or closes them to reveal or conceal the source image. Each slat has an adjustable opening that grows from its center outward. At full open, the video passes through untouched; at full close, each slat collapses to a narrow gap, and the image vanishes behind a configurable background.

What gives Blinds its character is the ***cascade*** control. Rather than all slats opening at once, a cascade introduces a progressive delay: the first slat opens fully before the next one begins, creating a rolling reveal that sweeps across the frame. Combined with a built-in triangle-wave ***oscillator***, the cascade can animate automatically, producing the classic television wipe effect used in broadcast reveals and live video mixing.

Blinds operates in both horizontal and vertical orientations and offers edge softness for smooth boundaries rather than hard pixel cuts. It can run in manual mode: controlled entirely by knob position: or in auto-animation mode where the opening sweeps back and forth at a configurable speed. The background behind each closed slat is either solid black or a dimmed copy of the source video.

### What's In a Name?

The name ***Blinds*** refers to venetian blinds, the slatted window coverings that tilt open and closed in parallel. The visual analogy is direct: the effect literally slices the image into horizontal or vertical strips and opens them from the center, just as you would twist the rod on a set of window blinds to let in light.

---

## Quick Start

1. Turn **Open** (Knob 1) fully counterclockwise. The screen goes dark: all slats are closed. Slowly turn the knob clockwise and watch the image appear through narrow horizontal gaps that widen into full slats.
2. Increase **Slats** (Knob 2) to raise the count. More slats means more cuts through the image, creating a finely divided shutter grid.
3. Advance **Cascade** (Knob 3) from zero. The slats no longer open simultaneously: the topmost slat opens first and each successive slat follows with a delay, creating a rolling curtain reveal.
4. Flip **Animate** (Switch 8) to **Auto**. The opening sweeps back and forth automatically. Adjust **Speed** (Knob 5) to control the animation rate.

---

## Parameters

![Videomancer front panel with Blinds loaded](/img/instruments/videomancer/blinds/blinds_control_panel.png)
*Videomancer's front panel with Blinds active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Open

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Open** controls how wide each slat's opening is. At minimum, every slat is fully closed: the video is completely hidden behind the background. At maximum, every slat is fully open: the video passes through without interruption. The opening grows symmetrically from the center of each slat, so at intermediate values you see a bright stripe of video in the middle of each slat with background visible at the top and bottom edges.

:::tip
In manual mode, sweeping Open from minimum to maximum with the cascade set to zero produces a uniform venetian blind wipe: all slats open at the same time, creating even horizontal bars of video.
:::

---

### Knob 2 — Slats

| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 7 |

**Slats** sets the number of parallel divisions. The count snaps to even values between 2 and 16. At the lowest setting you get two large panels splitting the frame in half; at the highest setting the frame is divided into sixteen narrow strips. Increasing the slat count makes the grid finer and the individual openings narrower for any given Open percentage.

---

### Knob 3 — Cascade

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Cascade** introduces a per-slat phase offset to the opening. At zero, all slats share the same opening width: they move in unison. As cascade increases, each successive slat receives a larger delay before it begins to open. This creates the characteristic rolling reveal: the first slat opens fully, then the second begins, then the third, and so on. At maximum cascade, only one slat is open at a time while the others remain closed.

:::note
Cascade subtracts from each slat's effective opening in proportion to its index. A slat near the end of the sequence may remain completely closed even when the first slat is fully open, depending on the cascade amount.
:::

---

### Knob 4 — Edge Soft

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 6% |

**Edge Soft** smooths the transition at slat boundaries. At minimum, each slat has a hard pixel-perfect cutoff: the video is either fully visible or fully hidden. Increasing Edge Soft introduces a brightness ramp at the edges of each opening, creating a gentle fade between the revealed video and the background rather than an abrupt cut.

---

### Knob 5 — Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Speed** governs the rate of the triangle-wave ***oscillator*** that drives the auto-animation mode. At minimum, the sweep is extremely slow, taking many seconds to complete a full open-close cycle. At maximum, the sweep is fast enough to create a rapid flutter. Speed has no effect when Animate (Switch 8) is set to Manual: in that mode, the Open knob directly controls the opening width.

---

### Knob 6 — Bg Level

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Bg Level** sets the brightness of the background behind closed slat regions. At minimum, closed regions are solid black. Increasing the value raises the background brightness. When Bg Mode (Switch 9) is set to Black, this value is an absolute luminance level applied flat across all hidden areas. When Bg Mode is set to Dim Vid, the value acts as a ***gain multiplier*** applied to the source video itself, producing a dimmed version of the image behind the blinds.

---

### Switch 7 — Orient

| Property | Value |
|----------|-------|
| Off | Horiz |
| On | Vert |
| Default | Horiz |

**Orient** selects the axis of the slat divisions. In the default **Horiz** position, slats run horizontally across the frame and divide the image into rows: the classic venetian blind look. Flipping to **Vert** rotates the slats ninety degrees so they run vertically, dividing the image into columns. The entire cascade and opening logic follows the chosen orientation.

---

### Switch 8 — Animate

| Property | Value |
|----------|-------|
| Off | Manual |
| On | Auto |
| Default | Manual |

**Animate** selects between manual and auto-animation modes. In **Manual** mode, the Open knob directly controls the opening width: what you dial is what you see. In **Auto** mode, the opening sweeps back and forth automatically using a triangle-wave oscillator, and the Speed knob (Knob 5) controls the sweep rate. The Open knob is ignored in Auto mode.

---

### Switch 9 — Bg Mode

| Property | Value |
|----------|-------|
| Off | Black |
| On | Dim Vid |
| Default | Black |

**Bg Mode** determines what is visible in the hidden regions behind closed slats. In **Black** mode, closed areas show a flat background whose brightness is set by Bg Level (Knob 6). In **Dim Vid** mode, closed areas show a dimmed copy of the source video: the dimming level is controlled by Bg Level. Dim Vid mode preserves the chrominance of the source in hidden areas, while Black mode forces chrominance to neutral gray.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** swaps the reveal and hide regions of each slat. Normally, the center of each slat is revealed and the edges are hidden. With Invert enabled, the center is hidden and the edges are revealed. This effectively turns the blinds inside-out: instead of strips of video separated by dark gaps, you see strips of darkness separated by video edges.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Blinds processing. The sync delay pipeline still aligns timing, so switching Bypass on and off does not cause glitches. Use Bypass for instant A/B comparison between the raw input and the blinds effect.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (blinds-processed) output. At minimum, the output is entirely dry: the raw input video. At maximum, the output is entirely the blinds effect. Intermediate values blend the two, which can create a ghostly double-exposure where the blinds pattern is superimposed over the original image at reduced opacity.

---

## Background

### Broadcast wipe effects

The venetian blind wipe is one of the oldest transition effects in television production. Early video switchers: hardware mixers used in broadcast studios: included a bank of ***wipe pattern generators*** that could reveal a new video source through geometric shapes: circles, diamonds, boxes, and slats. The venetian blind pattern was popular because it divided the frame evenly and produced a clean, professional reveal. Videomancer's Blinds program recreates this effect digitally, using the FPGA to compute per-pixel reveal masks at full video rate.

### Cascade and phase offset

The cascade feature extends the basic blind wipe into something more dynamic. By introducing a ***phase offset*** that increases with each slat's index, the effect transforms from a simultaneous reveal into a sequential one. This is mathematically simple: each slat's effective opening is calculated as `open - (cascade × slat_index)`, clamped to the valid range. But visually, it produces a compelling rolling motion that can evoke curtains parting, shutters clicking, or dominoes falling.

### Triangle-wave oscillator

The auto-animation mode uses a ***direct digital synthesis*** (DDS) accumulator to generate a triangle wave. A 16-bit phase register increments once per video field (vsync). The upper bit determines the ramp direction: when it is low, the phase ramps up; when it is high, the phase ramps down (by bit inversion). This produces a smooth, symmetric back-and-forth sweep without any discontinuities. The Speed knob controls how much the phase register advances per field, directly setting the animation frequency.


---

## Signal Flow

### Signal Flow Notes

The pipeline is a pure registered design with no BRAM: all computation is combinational logic registered through four pipeline stages plus four interpolator clocks, for a total latency of eight clock cycles. The sync delay pipeline shifts the input video data by the same eight clocks so that the dry signal aligns with the processed signal at the mix stage.

Two key interactions define the visual behavior. First, the ***cascade-to-slat-index*** relationship: the cascade offset scales linearly with each slat's ordinal position, so the last slat in the sequence receives the largest delay. This means the effect naturally flows from one edge of the frame to the other. Second, the ***reveal-to-compose*** path: the reveal value computed in Stage 3 serves double duty: it gates the video luminance (multiplicative blend) and it selects the chrominance source (threshold at 512). This means that partially revealed areas show full-color video while fully hidden areas show either neutral gray or a dimmed version of the source, with no color bleeding at boundaries.

:::note
The chrominance switching threshold is fixed at reveal = 512 (50%). Below that point in Black mode, UV snaps to neutral gray. This prevents unnatural color artifacts in mostly-hidden slat regions where the luminance multiplication would produce very dark pixels with potentially misleading chrominance.
:::


---

## Exercises

These exercises progress from a basic manual wipe to an animated cascade reveal to a creative layered composition. Each builds on the previous one, gradually engaging more of the processing chain.
### Exercise 1: Manual Venetian Wipe

![Manual Venetian Wipe result](/img/instruments/videomancer/blinds/blinds_ex1_s1.png)
*Manual Venetian Wipe — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic venetian blind wipe that you control by hand, sweeping from fully closed to fully open.

#### Key Concepts

- The Open knob controls a center-outward reveal within each slat
- Slat count and orientation define the grid geometry
- Manual mode gives you direct, real-time control

#### Video Source

Any video source with recognizable content: a camera feed pointed at a colorful subject works well. High contrast between subject and background makes the slat boundaries more visible.

#### Steps

1. Set **Slats** (Knob 2) to maximum to create a finely divided grid of sixteen horizontal strips.
2. Turn **Open** (Knob 1) fully counterclockwise. The screen goes black (all slats are closed.)
3. Slowly turn **Open** clockwise. Watch narrow bright lines appear at the center of each slat and widen symmetrically.
4. Flip **Orient** (Switch 7) to **Vert**. The slats rotate ninety degrees, creating a vertical blind effect.
5. Return to **Horiz** and reduce **Slats** to minimum. Two large panels split the frame in half (a simple curtain split.)

#### Settings

| Control | Value |
|---------|-------|
| Open | Sweep 0 to 100% |
| Slats | 16 |
| Cascade | 0% |
| Edge Soft | 0% |
| Speed | 0% |
| Bg Level | 0% |
| Orient | Horiz |
| Animate | Manual |
| Bg Mode | Black |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Cascading Reveal

![Cascading Reveal result](/img/instruments/videomancer/blinds/blinds_ex2_s1.png)
*Cascading Reveal — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated rolling reveal where slats open one after another in a wave that sweeps across the frame.

#### Key Concepts

- Cascade offsets each slat's opening in sequence
- Auto-animation sweeps the opening with a triangle wave
- Edge softness creates gentle transitions at slat boundaries

#### Video Source

Footage with large areas of color and movement (a slow pan across a landscape or a performer on stage.)

#### Steps

1. Set **Slats** (Knob 2) to about eight divisions and **Open** (Knob 1) to roughly 40%.
2. Increase **Cascade** (Knob 3) until only the first few slats are open and the rest remain closed. Notice how the cascade creates a rolling gradient of openness.
3. Now flip **Animate** (Switch 8) to **Auto** and set **Speed** (Knob 5) to a moderate value. The cascade washes back and forth across the frame.
4. Increase **Edge Soft** (Knob 4) to about 70%. The hard slat boundaries soften into gentle gradients.
5. Flip **Orient** (Switch 7) to **Vert** to see the cascade sweep horizontally instead of vertically.
6. Try **Invert** (Switch 10): the reveal logic flips inside-out, punching dark stripes through the visible areas.

#### Settings

| Control | Value |
|---------|-------|
| Open | ~40% |
| Slats | 8 |
| Cascade | ~60% |
| Edge Soft | ~70% |
| Speed | ~25% |
| Bg Level | 0% |
| Orient | Horiz |
| Animate | Auto |
| Bg Mode | Black |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Dimmed Background Layers

![Dimmed Background Layers result](/img/instruments/videomancer/blinds/blinds_ex3_s1.png)
*Dimmed Background Layers — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A layered composition where partially hidden slat regions show a dimmed, ghostly version of the source video behind the bright revealed strips.

#### Key Concepts

- Bg Mode selects between flat black and dimmed video as the hidden-area fill
- Bg Level controls the brightness of the dimmed video
- Mix creates a double-exposure blend between processed and dry signals

#### Video Source

Footage with rich color and moderate contrast (a garden scene, an aquarium, or a neon-lit street.)

#### Steps

1. Set **Slats** (Knob 2) to about 12 divisions and **Open** (Knob 1) to roughly 50%.
2. Flip **Bg Mode** (Switch 9) to **Dim Vid**. The background is no longer black (it shows a dimmed version of the source.)
3. Increase **Bg Level** (Knob 6) to about 40%. The hidden areas brighten into a soft ghost image of the video.
4. Add moderate **Cascade** (Knob 3, ~30%) and **Edge Soft** (Knob 4, ~70%) for a rolling, soft-edged reveal.
5. Pull **Mix** (Fader 12) to about 60%. The blinds effect blends with the raw video, creating a ghostly double-exposure.
6. Flip **Orient** (Switch 7) to **Vert** and observe how the vertical orientation changes the composition's character.

#### Settings

| Control | Value |
|---------|-------|
| Open | ~50% |
| Slats | 12 |
| Cascade | ~30% |
| Edge Soft | ~70% |
| Speed | 0% |
| Bg Level | ~40% |
| Orient | Vert |
| Animate | Manual |
| Bg Mode | Dim Vid |
| Invert | Off |
| Bypass | Off |
| Mix | ~60% |

---
## Glossary

- **Cascade**: A progressive delay applied to sequential elements, causing them to activate one after another rather than simultaneously.

- **DDS (Direct Digital Synthesis)**: A technique for generating waveforms by incrementing a phase accumulator at a fixed rate; used here to produce the triangle-wave animation.

- **Interpolator**: A circuit that blends between two values based on a mixing coefficient; used for the wet/dry crossfade.

- **Oscillator**: A circuit that produces a repeating waveform; Blinds uses a triangle-wave oscillator for auto-animation.

- **Phase Offset**: A delay added to a periodic signal that shifts its timing relative to a reference; cascade uses per-slat phase offsets.

- **Sample and Hold**: A technique that captures a signal value at a specific moment and holds it constant until the next sample; the slat reveal mask operates frame-by-frame.

- **Slat**: One horizontal or vertical division of the frame in the venetian blind pattern.

- **Triangle Wave**: A periodic waveform that ramps linearly up and then linearly down, producing a symmetric back-and-forth sweep.

- **Wipe**: A video transition where one image is progressively revealed or concealed by a geometric pattern moving across the frame.

---
