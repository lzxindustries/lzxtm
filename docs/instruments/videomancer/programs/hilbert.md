---
draft: true
sidebar_position: 136
slug: /instruments/videomancer/hilbert
title: "Hilbert"
image: /img/instruments/videomancer/hilbert/hilbert_hero.png
description: "The screen is divided into a grid of square blocks."
---

![Hilbert hero image](/img/instruments/videomancer/hilbert/hilbert_hero_s1.png)
*Hilbert tracing a space-filling curve across the screen, progressively revealing video blocks in fractal order against a dark background.*

---

## Overview

**Hilbert** generates a living mosaic from the Hilbert curve: a single, continuous line that visits every cell in a grid without crossing itself. The image is divided into rectangular blocks, and each block's position along the curve determines when and how it appears. A reveal animation traces the curve from beginning to end, uncovering blocks one by one in their Hilbert-curve order. Unrevealed blocks show a solid background, revealed blocks show the source video, and the boundary between the two sweeps across the screen in the distinctive serpentine path of the fractal.

Beyond the reveal, Hilbert applies a distance-based color shift: blocks farther along the curve accumulate more and more chroma offset, painting a rainbow gradient that follows the curve's path through space. Block outlines can be drawn over the grid to make the structure visible, turning the screen into a map of the fractal traversal.

Because Hilbert operates on blocks rather than individual pixels, it needs no frame buffer at all: zero BRAMs. Everything is computed on the fly from the pixel's position, making it one of the lightest programs in the Videomancer library despite its mathematical depth.

:::note
Hilbert is classified as a ***synthesis*** program. Even though it reveals source video in the blocks, its primary creative purpose is to generate the fractal structure, grid overlay, and animated reveal choreography.
:::

### What's In a Name?

The ***Hilbert curve*** is named after the German mathematician David Hilbert, who described it in 1891 as an example of a ***space-filling curve***: a continuous path that passes through every point in a two-dimensional square. Unlike a simple raster scan that sweeps left to right, top to bottom, the Hilbert curve snakes through the grid in an elaborate, self-similar pattern. Each increase in the curve's ***order*** subdivides the grid into four smaller copies of itself, each rotated and reflected to preserve the single unbroken path. It's fractal geometry at its most elegant: infinite complexity built from one simple rule applied recursively.

---

## Quick Start

1. Turn **Outline** (Switch 10) to **On** and set **Order** (Knob 1) to a medium value. A grid of bright rectangles appears over the image (that's the block structure the Hilbert curve will traverse.)
2. Set **Animate** (Switch 7) to **On** and adjust **RevlSpd** (Knob 3) to a moderate value. Blocks begin appearing one by one, tracing the Hilbert curve's serpentine path across the screen.
3. Increase **ClrShft** (Knob 6). A rainbow gradient blooms along the curve: blocks near the beginning stay close to the original color, while blocks farther along the path shift through progressively warmer or cooler hues.
4. Try different **BlkSize** (Knob 2) values. Larger blocks make the structure coarse and architectural; smaller blocks make it fine and textile-like.

---

## Parameters

![Videomancer front panel with Hilbert loaded](/img/instruments/videomancer/hilbert/hilbert_control_panel.png)
*Videomancer's front panel with Hilbert active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Order

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

**Order** sets the complexity of the Hilbert curve by choosing how many times the basic U-shape is subdivided. At the minimum, order 1, the grid is just 2×2: four large quadrants visited in a simple U. At higher orders, the grid subdivides into 4×4, 8×8, and eventually 16×16 cells, and the curve's path becomes increasingly intricate. Higher orders create finer spatial detail in the reveal and color-shift patterns. The total number of blocks grows as the square of the grid side: order 2 has 16 blocks, order 3 has 64, and order 4 has 256.

:::tip
Very high orders with small block sizes create grids so fine that the curve's structure becomes almost invisible. Start with order 2 or 3 and **Outline** enabled to see the pattern clearly before increasing.
:::

---

### Knob 2 — BlkSize

| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 2 |

**BlkSize** controls the size of each grid cell in pixels. At the minimum, each block is 8×8 pixels: compact tiles that pack tightly into the frame. Stepping up gives 16×16, 32×32, and 64×64 pixel blocks. Larger blocks make the mosaic structure bold and architectural, while smaller blocks create a fine weave. Because blocks beyond the grid boundary simply repeat, the combination of Order and BlkSize determines how many distinct cells are visible on screen.

---

### Knob 3 — RevlSpd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**RevlSpd** controls the speed of the reveal animation when **Animate** is enabled. At 0%, the animation is frozen. As the value increases, the reveal sweeps faster along the Hilbert curve path, uncovering more and more blocks per frame. At high values the entire image appears almost instantly. The animation advances once per video field (vertical sync), so even moderate settings produce a smooth, visible trace.

:::note
When **Animate** is turned off, RevlSpd has no effect. The reveal position is controlled entirely by **RevlPos** (Knob 4) in manual mode.
:::

---

### Knob 4 — RevlPos

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**RevlPos** sets the reveal position manually when **Animate** is off. Fully clockwise, all blocks are revealed and the full image is visible. Turning counterclockwise hides blocks in reverse Hilbert-curve order, progressively replacing them with the background color. This lets you freeze-frame the reveal at any point along the curve and study its structure. When **Animate** is on, RevlPos is ignored (the internal counter takes over.)

---

### Knob 5 — BgLuma

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**BgLuma** sets the brightness of unrevealed blocks. At 0%, hidden blocks are pure black, creating a stark figure-ground contrast with the revealed video. Increasing the value lifts the background toward mid-gray and beyond. With **Outline** enabled, the combination of background brightness and grid lines creates an X-ray or architectural blueprint look.

---

### Knob 6 — ClrShft

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**ClrShft** adds a progressive hue shift along the Hilbert curve. At 0%, no color modification occurs: revealed blocks show the original video colors. As the value increases, each block's chroma channels are offset in proportion to its distance along the curve: the U channel gains a positive offset while the V channel gains a negative offset, creating a gradual color rotation from the curve's start to its end. At high values the effect paints a vivid rainbow gradient that traces the curve's path.

:::tip
ClrShft is most visible on desaturated or neutral source material. On highly saturated sources, the offset compounds with existing chroma and can clip.
:::

---

### Switch 7 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Animate** selects between automatic and manual reveal modes. When set to **On**, the reveal counter advances automatically once per video field, tracing the Hilbert curve at the speed set by **RevlSpd**. When set to **Off**, the counter is locked to the position set by **RevlPos**. Switching from On to Off freezes the animation at its current position.

---

### Switch 8 — Dir

| Property | Value |
|----------|-------|
| Off | Forward |
| On | Reverse |
| Default | Forward |

**Dir** sets the direction of the reveal animation. **Forward** traces the curve from its starting corner toward the end, revealing blocks in their natural Hilbert order. **Reverse** traces backward, hiding blocks from the end toward the start. Reversing mid-animation creates a satisfying "unpainting" effect (blocks vanish one by one along the curve's path.)

---

### Switch 9 — Map

| Property | Value |
|----------|-------|
| Off | Shuffle |
| On | Inverse |
| Default | Shuffle |

**Map** selects between two Hilbert mapping modes. In **Shuffle** mode, block positions are remapped according to the xy-to-d conversion: each block's screen position determines its curve distance, and that distance drives the reveal and color shift. In **Inverse** mode, the mapping is reversed, producing a different spatial permutation. The visual result is a mirrored or rotated version of the curve's path through space.

---

### Switch 10 — Outline

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Outline** draws bright border lines at every block boundary. When **On**, the left and top edges of each block are highlighted: revealed blocks get a bright white outline (luma 800), while unrevealed blocks get a dim outline (luma 300). This makes the grid structure explicitly visible and is essential for understanding how the Hilbert curve maps onto the screen. When **Off**, blocks blend seamlessly into their neighbors.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Hilbert processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the source and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (Hilbert-processed) output. At 0%, only the original video is visible. At 100%, the full Hilbert effect is applied. Intermediate values blend the two, which can soften the grid structure and create a translucent overlay of the fractal reveal on top of the source image.

---

## Background

### Space-filling curves

A ***space-filling curve*** is a continuous path that visits every point in a region: in this case, every cell of a two-dimensional grid. The idea seems paradoxical: a one-dimensional line somehow fills a two-dimensional area. The trick is self-similarity. At order 1, the Hilbert curve visits four cells in a U-shaped path. At order 2, each of those four cells is subdivided into four smaller cells, and a miniature, rotated copy of the U-shape is placed in each one. The copies are connected end-to-end to form a single continuous path through all 16 cells. Repeat this process indefinitely and the curve fills the entire plane.

This self-similar structure gives the Hilbert curve a remarkable property: ***locality preservation***. Points that are close together along the one-dimensional curve tend to be close together in two-dimensional space. This is why the reveal animation appears to "paint" the screen in smooth, connected patches rather than jumping randomly: the curve's path stays in one neighborhood before moving on.

### Block-level computation

Hilbert avoids the need for a frame buffer by operating at the block level. Instead of rearranging individual pixels (which would require storing an entire frame), it computes the Hilbert distance for each block's grid coordinate on the fly. The algorithm is an unrolled iterative version of the standard xy-to-d conversion, supporting orders 1 through 4: grids of 2×2 up to 16×16 blocks. This purely ***combinational*** logic evaluates in a single clock cycle, a feat made possible by the small grid sizes involved.

### Reveal animation

The reveal works by comparing each block's Hilbert distance against a threshold. Blocks whose distance is at or below the threshold are "revealed" (showing source video); blocks above the threshold stay hidden (showing the background). The threshold is stored in a 16-bit counter that advances once per video field. At 60 fields per second, even a modest speed setting produces a smooth, visible sweep.

Because the Hilbert curve preserves locality, the reveal tends to fill the screen in contiguous patches. This is visually distinct from a raster reveal (which would sweep left to right, top to bottom) or a random reveal (which would scatter blocks unpredictably). The curve's serpentine path creates a unique choreography that is neither orderly nor chaotic (it's fractal.)


---

## Signal Flow

### Signal Flow Notes

The pipeline has two key features worth noting.

First, the **color shift is distance-dependent**: the hue offset applied to each block is proportional to that block's Hilbert distance. This means blocks near the start of the curve stay close to the original color, while blocks near the end accumulate the maximum offset. The shift works by adding a scaled offset to the U channel and subtracting from the V channel, creating a rotation in the color plane. This only activates when ClrShft is above zero, so it can be disabled without cost.

Second, the **outline is drawn in the compose stage**, after the reveal test but before the mix. This means outlines appear on both revealed and unrevealed blocks, but at different brightness levels: bright white (luma 800) for revealed blocks, dim gray (luma 300) for unrevealed. The outline detection is purely spatial: it fires whenever the sub-pixel coordinate on either axis is zero, marking the top and left edge of every block. The Mix fader crossfades the entire composed result against the dry input, so outlines fade along with everything else.


---

## Exercises

These exercises explore the Hilbert curve from simple grid visualization through animated reveal to color-gradient composition. Each builds on the previous exercise's understanding of the curve's spatial structure.
### Exercise 1: Visualizing the Grid

![Visualizing the Grid result](/img/instruments/videomancer/hilbert/hilbert_ex1_s1.png)
*Visualizing the Grid — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A static Hilbert grid overlay showing the curve's block structure, with half the blocks revealed and half hidden.

#### Key Concepts

- Block size and order define the grid granularity
- Outlines make the spatial structure visible
- The reveal position determines which blocks show video

#### Steps

1. Turn **Outline** (Switch 10) to **On**. A grid of bright lines appears over the image.
2. Set **BlkSize** (Knob 2) fully clockwise for the largest blocks (64×64). The grid is coarse: only a few large rectangles. Now turn it counterclockwise toward the smallest blocks (8×8). The grid becomes fine and textile-like.
3. Set **Order** (Knob 1) to a medium value (order 3). You should see an 8×8 grid of blocks.
4. Make sure **Animate** (Switch 7) is **Off**. Turn **RevlPos** (Knob 4) slowly counterclockwise from fully clockwise. Blocks disappear one by one in Hilbert-curve order. Stop halfway (half the screen shows video, half shows background.)
5. Adjust **BgLuma** (Knob 5) to change the brightness of the hidden blocks. At 0% they are black; lift it toward mid-gray to see the full grid as a ghostly overlay.

#### Settings

| Control | Value |
|---------|-------|
| Order | ~50% |
| BlkSize | ~50% |
| RevlSpd | 0% |
| RevlPos | ~50% |
| BgLuma | 0% |
| ClrShft | 0% |
| Animate | Off |
| Dir | Forward |
| Map | Shuffle |
| Outline | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Animated Reveal

![Animated Reveal result](/img/instruments/videomancer/hilbert/hilbert_ex2_s1.png)
*Animated Reveal — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A continuously animated reveal that paints and unpaints the screen along the Hilbert curve, showing the fractal path in motion.

#### Key Concepts

- The reveal traces the Hilbert curve's serpentine path
- Speed and direction control the animation
- Locality preservation makes the sweep coherent

#### Steps

1. Start from the Exercise 1 settings. Set **Animate** (Switch 7) to **On**.
2. Turn **RevlSpd** (Knob 3) slowly clockwise. Blocks begin appearing one by one, tracing the curve's path. Notice how the reveal fills the screen in smooth, connected patches (it doesn't jump randomly.)
3. Set **Dir** (Switch 8) to **Reverse**. The animation reverses: blocks vanish in the opposite order. Switch back to **Forward**.
4. Increase **Order** (Knob 1) to order 4. The path becomes much more intricate, and the reveal takes longer to complete the full cycle.
5. Turn **Outline** off (Switch 10). Without the grid lines, the reveal becomes a mysterious, organic-looking animation as blocks melt into and out of the background.
6. Adjust **BgLuma** (Knob 5) to a mid-gray value. The contrast between revealed video and hidden background softens, creating a ghostly emergence effect.

#### Settings

| Control | Value |
|---------|-------|
| Order | ~75% |
| BlkSize | ~50% |
| RevlSpd | ~25% |
| RevlPos | 100% |
| BgLuma | ~10% |
| ClrShft | 0% |
| Animate | On |
| Dir | Forward |
| Map | Shuffle |
| Outline | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Color Curve Composition

![Color Curve Composition result](/img/instruments/videomancer/hilbert/hilbert_ex3_s1.png)
*Color Curve Composition — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A color-graded mosaic where each block's hue depends on its position along the Hilbert curve, producing a fractal rainbow.

#### Key Concepts

- Color shift paints a gradient along the curve's path
- The distance along the curve maps to hue offset
- Combining color shift with reveal creates layered compositions

#### Steps

1. Set **RevlPos** (Knob 4) fully clockwise so all blocks are revealed. Turn **Animate** off.
2. Set **ClrShft** (Knob 6) to about 80%. A color gradient appears across the image: blocks at different curve distances shift toward different hues.
3. Set **Outline** (Switch 10) to **On**. The grid makes the color boundaries visible. You can trace the Hilbert curve's path by following the color progression from block to block.
4. Increase **Order** (Knob 1) to the maximum. The color gradient becomes smoother as more blocks subdivide the curve.
5. Now turn **Animate** on and set **RevlSpd** (Knob 3) to a slow value. The color-shifted blocks emerge one by one, revealing the rainbow in curve order.
6. Adjust **Mix** (Fader 12) to about 60%. The color-shifted fractal grid blends with the dry input, creating a translucent overlay of the Hilbert pattern on top of the source video.

#### Settings

| Control | Value |
|---------|-------|
| Order | ~100% |
| BlkSize | ~75% |
| RevlSpd | ~15% |
| RevlPos | 100% |
| BgLuma | ~30% |
| ClrShft | ~80% |
| Animate | On |
| Dir | Forward |
| Map | Shuffle |
| Outline | On |
| Bypass | Off |
| Mix | ~60% |

---
## Glossary

- **Block**: A rectangular region of pixels treated as a single unit by Hilbert. All pixels in a block share the same Hilbert distance and reveal state.

- **Chroma**: The color information in a video signal, encoded as U and V components in YUV color space.

- **Combinational Logic**: Digital logic whose output depends only on the current inputs, not on any stored state. Hilbert's xy-to-d converter evaluates in one clock cycle with no memory.

- **Hilbert Curve**: A continuous, self-similar space-filling curve described by David Hilbert in 1891. It visits every cell of a grid without crossing itself.

- **Interpolator**: A linear-blend module that crossfades between two values. Hilbert uses three interpolators (Y, U, V) for the wet/dry mix.

- **Locality Preservation**: The property that points close together on the one-dimensional curve tend to be close together in two-dimensional space. This makes the Hilbert reveal sweep in coherent patches.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness.

- **Order**: The recursion depth of the Hilbert curve. Order N creates a 2^N × 2^N grid of blocks, with 4^N total cells.

- **Reveal**: The progressive unveiling of blocks along the curve's path. Blocks whose Hilbert distance is at or below the reveal threshold become visible.

- **Space-Filling Curve**: A continuous curve that passes through every point of a higher-dimensional region. The Hilbert curve fills a square.

---
