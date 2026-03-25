---
draft: true
sidebar_position: 184
slug: /instruments/videomancer/macrobloc
title: "Macrobloc"
image: /img/instruments/videomancer/macrobloc/macrobloc_hero_s1.png
description: "Digital video compression divides every frame into small rectangular blocks and encodes each one independently."
---

![Macrobloc hero image](/img/instruments/videomancer/macrobloc/macrobloc_hero_s1.png)
*Macrobloc simulating MPEG codec failure with displaced blocks, frozen regions, and chroma separation artifacts across a live video signal.*

---

## Overview

**Macrobloc** recreates the visual language of digital video compression failure: the blocky, fractured artifacts that appear when an MPEG stream loses data or a satellite signal drops below threshold. It divides the incoming image into a grid of square blocks (8×8 or 16×16 pixels) and selectively corrupts them, replacing clean picture data with displaced pixels, frozen frames, flat color fills, and separated chroma channels. The result is a convincing simulation of ***macroblocking***, the signature failure mode of block-based video codecs.

Unlike real codec failure, Macrobloc gives you full artistic control over the corruption. You choose how many blocks break, how far they shift, whether they freeze in place, and how aggressively the color channels separate. A 16-bit ***linear feedback shift register (LFSR)*** determines which blocks are corrupted, and you can lock the pattern in place or let it evolve frame by frame. An optional luminance modulation path makes dark regions of the image more susceptible to corruption, creating content-aware glitch patterns that track the source material.

At low settings, Macrobloc introduces subtle digital imperfections: the occasional misplaced block or frozen tile that gives the image a lived-in, compressed quality. At extreme settings, the picture dissolves into a churning field of displaced fragments, frozen ghosts, and color-separated debris that bear only a passing resemblance to the original signal.

### What's In a Name?

The name ***Macrobloc*** is a direct reference to the ***macroblock***, the fundamental unit of block-based video compression standards like MPEG-2 and H.264. In these codecs, the image is divided into blocks (typically 8×8 or 16×16 pixels) that are independently compressed. When data is lost during transmission: a scratched DVD, a weak satellite signal, a corrupted network stream: individual macroblocks fail while their neighbors survive, producing the distinctive blocky artifacts that Macrobloc recreates. The French-influenced spelling nods to the Bloc as both a structural unit and a cinematic reference.

---

## Quick Start

1. Turn **Corruption** (Knob 1) clockwise to about 40%. Random blocks across the image begin to glitch: some fill with flat color, some shift sideways, some show separated color channels. The grid of corruption has begun.
2. Increase **Displacement** (Knob 2) to about 50%. Corrupted blocks now read their pixel data from the wrong location, creating a jittery, displaced mosaic where fragments of the image appear in the wrong place.
3. Toggle **Animate** (Switch 10) to **Static**. The corruption pattern freezes in place. Toggle it back to **Animate** and the pattern re-rolls every frame, creating a dynamic, living glitch texture.
4. Enable **Block Edge** (Switch 9). Black grid lines appear at the boundaries of every block, making the underlying block grid visible. This is the skeleton of a digital codec laid bare.

---

## Parameters

![Videomancer front panel with Macrobloc loaded](/img/instruments/videomancer/macrobloc/macrobloc_control_panel.png)
*Videomancer's front panel with Macrobloc active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Corruption

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Corruption** controls the probability that any given block will be corrupted. At 0%, fully counterclockwise, no blocks are affected and the image passes through clean. As Corruption increases, more blocks are selected for corruption by the LFSR. At high values, the majority of the image is replaced with glitch artifacts. The LFSR compares its value against the Corruption threshold: blocks whose random value falls below the threshold are corrupted.

:::tip
Start with Corruption around 30–40% for a natural-looking codec failure. At 100%, essentially every block is corrupted and the original image is almost entirely destroyed: great for abstract textures, but you lose the contrast between clean and corrupted regions that makes low settings so compelling.
:::

---

### Knob 2 — Displacement

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Displacement** controls how far corrupted blocks are spatially shifted from their correct position. At 0%, displaced blocks read from their normal location (no visible displacement). As the value increases, the read offset grows, pulling pixel data from increasingly distant horizontal positions. This simulates ***motion vector errors*** in inter-frame prediction: the decoder tries to reconstruct a block from a reference frame but uses the wrong offset, producing a spatially scrambled image.

The displacement magnitude is modulated by the LFSR, so each corrupted block shifts by a different amount. Not all corruption types use displacement: only types "01" and "11" (displacement and chroma-shift) apply the read offset.

---

### Knob 3 — Freeze Rate

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Freeze Rate** controls the probability that block columns toggle into a frozen state at each frame boundary. Frozen blocks hold their previously stored pixel values instead of updating, simulating ***I-frame loss***: the decoder's reference frame becomes stale, and parts of the image stop responding to changes in the source. At 0%, no blocks freeze. As the value increases, more columns are toggled each frame, creating patches of stale imagery that persist while the rest of the image updates normally.

:::note
Freeze operates per-column, not per-individual-block. When a column is frozen, all blocks in that column hold their previous values. The freeze toggle is probabilistic: each frame, the LFSR decides whether to flip each column's freeze flag, so the frozen regions shift over time.
:::

---

### Knob 4 — Chroma Shift

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Chroma Shift** introduces an independent spatial offset for the U and V (chroma) channels, separate from the Y (luma) displacement. At 0%, the chroma channels read from the same position as luma. As the value increases, chroma reads from an increasingly different horizontal position, producing green and magenta fringing artifacts that simulate ***chroma subsampling errors***: the decoder reconstructs color from the wrong spatial location relative to brightness. This creates the characteristic color-bleed look of a badly decoded MPEG stream.

The chroma offset is derived from a different slice of the LFSR than the luma displacement, so each corrupted block gets an independent chroma shift direction and magnitude.

---

### Knob 5 — Seed

| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 512 |

**Seed** determines the initial state of the LFSR that drives all corruption decisions. Changing the Seed produces a completely different spatial pattern of corruption while keeping the density and behavior otherwise identical. In **Static** mode (Switch 10), the LFSR resets to the Seed value every frame, so this control directly selects which specific blocks are corrupted. In **Animate** mode, the Seed sets the starting point for an evolving sequence.

:::tip
In Static mode, slowly sweeping Seed creates a scrolling, kaleidoscopic effect as different block patterns cycle through. Find a pattern you like, then lock it in place.
:::

---

### Knob 6 — DC Fill

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**DC Fill** sets the luminance level of blocks that receive DC-fill corruption. At 0%, DC-filled blocks appear black. At 50%, they appear mid-gray. At 100%, they appear white. The chroma channels of DC-filled blocks are always set to neutral (U=512, V=512), so the fill color is always a shade of gray regardless of the DC Fill level.

When **Corr Type** (Switch 8) is set to **DC Fill**, all corrupted blocks use this flat-fill mode instead of random corruption types. This creates a clean, geometric pattern of gray rectangles punched through the image.

---

### Switch 7 — Block Size

| Property | Value |
|----------|-------|
| Off | 8x8 |
| On | 16x16 |
| Default | 8x8 |

**Block Size** selects between two grid sizes: **8×8** and **16×16** pixels per block. Smaller blocks create a finer corruption grid with more numerous, smaller artifacts. Larger blocks create a coarser grid with fewer, more prominent corrupted regions. The 16×16 setting more closely matches the macroblock size used in H.264 and other modern codecs. The 8×8 setting matches the DCT block size used internally within those macroblocks, as well as older MPEG-2 and JPEG standards.

---

### Switch 8 — Corr Type

| Property | Value |
|----------|-------|
| Off | Random |
| On | DC Fill |
| Default | Random |

**Corr Type** selects between two corruption strategies. In **Random** mode, each corrupted block is assigned one of four corruption types by the LFSR: DC fill, displacement, freeze, or chroma-shift. The type varies from block to block, creating a diverse mix of failure modes across the image. In **DC Fill** mode, all corrupted blocks use DC fill exclusively: the corruption pattern becomes a clean grid of flat gray rectangles, ignoring displacement, freeze, and chroma shift entirely.

---

### Switch 9 — Block Edge

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Block Edge** enables a visible black grid line at the boundary of every block in the image: both corrupted and clean blocks. When On, the first pixel row and first pixel column of each block are replaced with black (Y=0, U=512, V=512). This makes the underlying block decomposition visible, revealing the spatial grid that the corruption algorithm operates on. The grid lines persist even when Corruption is at 0%, so you can see the block structure without any active corruption.

:::tip
Block Edge is useful for understanding how Block Size, Displacement, and Corruption interact. Enable it while adjusting other parameters to see exactly where block boundaries fall and which blocks are selected for corruption.
:::

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Static |
| On | Animate |
| Default | Animate |

**Animate** controls whether the corruption pattern changes from frame to frame. In **Animate** mode, the LFSR advances its state at each frame boundary, producing a new corruption pattern every frame: the glitch artifacts shift, flicker, and evolve continuously. In **Static** mode, the LFSR resets to the Seed value every frame, so the same blocks are corrupted in the same way on every frame. Static mode is useful for examining a specific corruption pattern or creating a stable, repeating texture.

---

### Switch 11 — Luma Mod

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Luma Mod** enables luminance-dependent corruption density. When On, dark regions of the source image are more likely to be corrupted than bright regions. The corruption threshold is increased by an amount proportional to the inverse of the pixel's brightness, so dark areas effectively see a higher Corruption setting than bright areas. When Off, the Corruption threshold is uniform across the image.

This creates a content-aware corruption pattern that ***follows the shadows***: dark regions dissolve into glitch artifacts while highlights remain relatively intact. We can think of this as a simulation of signal-level-dependent error rates, where weak (dark) portions of the signal are more susceptible to noise and data loss.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (original) and wet (corrupted) signal. At 0%, fully down, the output is the unprocessed input: all corruption is hidden. At 100%, fully up, the output is the fully corrupted signal. Intermediate positions create a transparent overlay of corruption over the clean image, which can produce a subtle, ghostly quality where glitch artifacts are visible but the underlying image remains legible.

---

## Background

### Block-based video compression

Modern digital video compression: MPEG-2, H.264, HEVC: works by dividing each frame into a grid of rectangular blocks and compressing each block independently. Typically these blocks are 8×8 or 16×16 pixels, called ***macroblocks***. Within each macroblock, the codec applies a ***discrete cosine transform (DCT)*** that converts the spatial pixel data into frequency components, discards the components the human eye is least sensitive to, and encodes only the survivors. Adjacent frames share information through ***inter-frame prediction***: the codec describes each block as a displacement from a block in a reference frame, transmitting only the difference. This is enormously efficient when it works.

When it fails, it fails in blocks.

### How codec failure looks

A lost data packet, a scratched disc surface, a weak signal: any interruption to the compressed data stream corrupts the decoded picture in characteristic ways. Because the codec operates on independent blocks, errors affect discrete rectangular regions while leaving their neighbors untouched. The most common failure modes are:

- **DC fill**: the block's frequency data is lost, and the decoder fills it with a flat average color
- **Displacement**: an inter-frame prediction references the wrong position, pulling pixel data from the wrong part of the reference frame
- **Freeze**: a reference frame is lost entirely, and blocks continue displaying stale data from the last good frame
- **Chroma separation**: the codec's chroma subsampling reconstructs color from the wrong spatial location relative to brightness, producing green and magenta fringing

Macrobloc implements all four of these failure modes, composing them into a controllable simulation of digital video degradation.

### The LFSR engine

All corruption decisions in Macrobloc are driven by a 16-bit ***linear feedback shift register (LFSR)***: a fast, deterministic pseudo-random number generator implemented in just a few logic cells. The LFSR produces a stream of values that appear random but are fully repeatable from any given seed. At the start of each block, the LFSR advances one step. The new value is compared against the Corruption threshold: if it falls below the threshold, the block is corrupted. The same LFSR value also determines the corruption type and the displacement magnitude, so everything is derived from a single pseudo-random stream.

In **Animate** mode, the LFSR's starting state advances each frame, producing an evolving corruption pattern. In **Static** mode, the LFSR resets to the Seed value every frame, so the pattern is frozen in place.


---

## Signal Flow

### Signal Flow Notes

The pipeline splits into two parallel paths early on. The incoming video is simultaneously written into three line-buffer BRAMs and fed into an 8-clock delay line. The line buffers allow corrupted blocks to read pixel data from displaced horizontal positions: the read address is offset by a displacement computed from the LFSR and the Displacement parameter. A second, independent read address is computed for the U and V channels, adding the Chroma Shift offset on top of the displacement offset. This means chroma and luma can read from different spatial locations, simulating the color-separation artifacts of chroma subsampling failure.

The corruption compose stage selects the output for each pixel based on the corruption type assigned to the current block. Four types are possible: DC fill (flat gray), displacement (spatially shifted), freeze (held from previous frame), and chroma shift (Y normal, UV shifted). Block edge lines are overlaid last, drawing black grid lines at the first pixel of each block row and column.

:::note
The freeze mechanism operates per-column rather than per-block. A 128-entry freeze map stores one flag per block column, and the LFSR probabilistically toggles each column's flag at each frame boundary. When a column's flag is set, all blocks in that column output held (stale) pixel values instead of the current frame.
:::


---

## Exercises

These exercises progress from basic block corruption through displacement and freeze effects to full codec failure simulation. Each builds on the previous one, engaging more of the corruption engine.
### Exercise 1: Basic Block Corruption

![Basic Block Corruption result](/img/instruments/videomancer/macrobloc/macrobloc_ex1_s1.png)
*Basic Block Corruption — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean grid of gray rectangles punched through a live video signal, simulating the most basic form of macroblock failure.

#### Key Concepts

- The LFSR selects blocks for corruption based on a threshold
- DC Fill replaces blocks with a flat gray level
- Block Edge reveals the underlying grid structure

#### Video Source

A live camera feed or recorded footage with recognizable subjects and moderate contrast.

#### Steps

1. **Set corruption type**: Toggle **Corr Type** (Switch 8) to **DC Fill** so every corrupted block becomes a flat rectangle.
2. **Enable edges**: Toggle **Block Edge** (Switch 9) to **On** to see the block grid.
3. **Add corruption**: Slowly turn **Corruption** (Knob 1) clockwise. Gray rectangles begin appearing across the image as blocks are selected for DC fill.
4. **Adjust fill level**: Sweep **DC Fill** (Knob 6) from 0% to 100%. The fill rectangles change from black through gray to white.
5. **Change block size**: Toggle **Block Size** (Switch 7) to **16×16**. The rectangles become larger and fewer. Toggle back to **8×8** to compare.
6. **Change the pattern**: Slowly sweep **Seed** (Knob 5). Different blocks are selected for corruption as the LFSR starting state changes.

#### Settings

| Control | Value |
|---------|-------|
| Corruption | ~40% |
| Displacement | 0% |
| Freeze Rate | 0% |
| Chroma Shift | 0% |
| Seed | 512 |
| DC Fill | ~50% |
| Block Size | 8x8 |
| Corr Type | DC Fill |
| Block Edge | On |
| Animate | Static |
| Luma Mod | Off |
| Mix | 100% |

---

### Exercise 2: Motion Vector Chaos

![Motion Vector Chaos result](/img/instruments/videomancer/macrobloc/macrobloc_ex2_s1.png)
*Motion Vector Chaos — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dynamic, jittery corruption pattern where blocks are displaced and color-separated, simulating a streaming video with severe packet loss.

#### Key Concepts

- Displacement simulates inter-frame prediction failure
- Chroma Shift separates color channels from brightness
- Animate mode creates evolving corruption patterns

#### Video Source

Footage with strong horizontal features (text, geometric patterns, or architecture.)

#### Steps

1. **Prepare**: Set **Corruption** (Knob 1) to about 50% and **Corr Type** (Switch 8) to **Random** so the engine uses all four corruption modes.
2. **Displacement**: Turn **Displacement** (Knob 2) clockwise to about 60%. Corrupted blocks now read from wrong positions: fragments of the image jump sideways into neighboring blocks.
3. **Chroma separation**: Increase **Chroma Shift** (Knob 4) to about 50%. Color channels separate from brightness in corrupted blocks, creating green and magenta fringing.
4. **Animate**: Set **Animate** (Switch 10) to **Animate**. The corruption pattern now changes every frame, creating a flickering, jittery glitch texture.
5. **Block size**: Toggle **Block Size** (Switch 7) to **16×16** for larger, more dramatic displacements. The bigger blocks make the spatial scrambling more visible.
6. **Luma modulation**: Enable **Luma Mod** (Switch 11). Dark regions of the image now corrupt more heavily, as if the signal degrades where it's weakest.

#### Settings

| Control | Value |
|---------|-------|
| Corruption | ~50% |
| Displacement | ~60% |
| Freeze Rate | 0% |
| Chroma Shift | ~50% |
| Seed | 50 |
| DC Fill | ~50% |
| Block Size | 16x16 |
| Corr Type | Random |
| Block Edge | Off |
| Animate | Animate |
| Luma Mod | On |
| Mix | 100% |

---

### Exercise 3: Frozen Broadcast

![Frozen Broadcast result](/img/instruments/videomancer/macrobloc/macrobloc_ex3_s1.png)
*Frozen Broadcast — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A broadcast signal that partially freezes: some regions update normally while others hold stale imagery from previous frames, with displaced blocks and color artifacts layered on top.

#### Key Concepts

- Freeze simulates I-frame loss in inter-frame prediction
- Combining freeze with displacement creates layered temporal artifacts
- Mix allows transparent corruption overlay

#### Video Source

Footage with visible motion (a moving subject, panning camera, or scrolling graphics.)

#### Steps

1. **Enable freeze**: Set **Corruption** (Knob 1) to about 70% and **Freeze Rate** (Knob 3) to about 40%. Columns of blocks begin holding their previous values while the rest of the image updates.
2. **Add displacement**: Set **Displacement** (Knob 2) to about 30%. Displaced blocks now coexist with frozen blocks: some regions show scrambled current data, others show stale past data.
3. **Chroma fringing**: Set **Chroma Shift** (Knob 4) to about 30%. Subtle color separation appears in the displaced and chroma-shifted corruption types.
4. **Partial mix**: Lower **Mix** (Fader 12) to about 60%. The corruption becomes semi-transparent: you can see the clean image ghosting through the corrupted regions.
5. **Static freeze pattern**: Set **Animate** (Switch 10) to **Static**. The corruption pattern locks in place. Move the camera or change the source. Frozen blocks continue showing old imagery while displaced blocks track the new source.
6. **Observe column behavior**: Watch how freeze affects entire columns of blocks simultaneously. When a column freezes, all blocks in that column hold their old data.

#### Settings

| Control | Value |
|---------|-------|
| Corruption | ~70% |
| Displacement | ~30% |
| Freeze Rate | ~40% |
| Chroma Shift | ~30% |
| Seed | 250 |
| DC Fill | ~50% |
| Block Size | 8x8 |
| Corr Type | Random |
| Block Edge | Off |
| Animate | Static |
| Luma Mod | Off |
| Mix | ~60% |

---
## Glossary

- **Chroma Subsampling**: A compression technique that stores color information at lower resolution than brightness, exploiting the eye's lower sensitivity to color detail.

- **DC Fill**: Replacement of a block's content with a single flat color value, simulating the loss of all spatial frequency data in a compressed block.

- **DCT (Discrete Cosine Transform)**: The mathematical transform at the heart of JPEG and MPEG compression, converting spatial pixel data into frequency components.

- **I-Frame**: An intra-coded frame in video compression that contains a complete image without reference to other frames; loss of an I-frame causes subsequent frames to display stale data.

- **Inter-Frame Prediction**: A compression technique where blocks are described as spatial offsets from a reference frame, transmitting only the difference.

- **LFSR (Linear Feedback Shift Register)**: A simple, hardware-efficient pseudo-random number generator that produces a deterministic sequence from a given seed.

- **Macroblock**: The fundamental rectangular unit (typically 8×8 or 16×16 pixels) in block-based video compression standards.

- **Macroblocking**: The visible artifact of block-based codec failure, where individual rectangular blocks display incorrect data while their neighbors remain intact.

- **Motion Vector**: The displacement offset used in inter-frame prediction to indicate where a block's reference data is located in a previous frame.

---
