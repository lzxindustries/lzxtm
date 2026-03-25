---
draft: true
sidebar_position: 13
slug: /instruments/videomancer/backrooms
title: "Backrooms"
image: /img/instruments/videomancer/backrooms/backrooms_hero.png
description: "Every generation discovers its own image of infinitely repeating, inescapable architecture."
---

![Backrooms hero image](/img/instruments/videomancer/backrooms/backrooms_hero_s1.png)
*Backrooms generating an infinite scrolling labyrinth from pure mathematics: corridors carved by recursive hash functions reveal the input video beneath.*

---

## Overview

**Backrooms** is a procedural maze synthesizer that builds infinite, scrollable labyrinths entirely from per-pixel arithmetic. There are no stored patterns, no lookup tables, and no frame buffers: every wall and corridor is computed fresh at each clock cycle using a cascade of ***hash functions*** seeded by a single parameter. The result is a dense, fractal-like grid of corridors that the input video shows through, as if you're peering through the floor plan of an impossible building.

The maze structure shifts completely whenever you change the **Seed** parameter. Each seed value produces a unique, deterministic maze topology: the same seed always generates the same labyrinth. Toggle the **Animate** switch and the entire structure scrolls continuously in a direction and speed you control, creating the sensation of drifting through an endless architectural space. Switch from **Grid** to **Organic** mode and the strict right angles soften into rougher, more natural passages.

:::tip
Backrooms is a ***synthesis*** program. It generates its own pattern from scratch rather than transforming the input. The input video is visible through the maze corridors, but the maze structure itself is wholly procedural (feed it a black screen and you still get a labyrinth.)
:::

### What's In a Name?

The name ***Backrooms*** references the internet urban legend of an infinite, monotonous labyrinth of empty office rooms accessible by "noclipping" through reality. The legend describes an architecturally impossible space: yellowed fluorescent lighting, damp carpet, and hallways that never end. This program captures that unnerving spatial quality: the mazes it generates scroll forever, repeat without tiling, and shift their entire topology with a single knob turn, as if the building itself is rearranging around you.

---

## Quick Start

1. Turn **Seed** (Knob 6) slowly. Watch the entire maze pattern change with each step: walls appear and disappear as the hash function reseeds. Every position of the knob produces a completely different labyrinth.
2. Adjust **Cell Size** (Knob 1) to change the scale of the grid. Smaller cells produce dense, intricate mazes. Larger cells produce wide corridors and big rooms.
3. Dial in **Wall Width** (Knob 2) to thicken or thin the walls. At low values, the walls are hairline-thin. At high values, the corridors narrow to slits.
4. Flip **Animate** (Switch 7) to **On**, then sweep **Scroll X** (Knob 3) and **Scroll Y** (Knob 4). The labyrinth glides across the screen (an infinite floor plan, endlessly unfolding.)

---

## Parameters

![Videomancer front panel with Backrooms loaded](/img/instruments/videomancer/backrooms/backrooms_control_panel.png)
*Videomancer's front panel with Backrooms active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Cell Size

| Property | Value |
|----------|-------|
| Range | 4px – 64px |
| Default | 27px |

**Cell Size** sets the spatial scale of the maze grid. The maze is built from square cells, and this knob selects the cell width in pixels across eight discrete steps. At the smallest setting the cells are just 4 pixels wide: a tight, claustrophobic weave of walls that fills the screen with microscopic detail. Each step doubles the cell size through 8, 16, 32, and 64 pixels, all the way up to 128-pixel cells that create wide, open corridors.

:::note
Because cell sizes are powers of two, the transitions between steps are discrete jumps. You won't see a smooth scaling (the maze snaps to the next size as you turn the knob.)
:::

---

### Knob 2 — Wall Width

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Wall Width** controls how thick the walls are within each cell. At the minimum, walls are just one pixel wide: barely visible hairlines that divide the space. As you increase the value, walls grow proportionally thicker relative to the cell size, squeezing the corridors thinner and thinner. At the maximum, walls dominate and corridors almost vanish, leaving only narrow gaps between solid blocks.

The wall thickness is scaled automatically to the current **Cell Size** setting. Whether cells are 4 pixels or 128 pixels across, the wall width parameter sweeps from no wall to maximum wall within that cell.

---

### Knob 3 — Scroll X

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |

**Scroll X** controls horizontal position or scroll speed, depending on the state of the **Animate** switch. When Animate is off, Scroll X sets a fixed horizontal offset: the entire maze shifts left or right as you turn the knob. The center position (180°) is neutral. When Animate is on, Scroll X becomes a speed control. The center position stops horizontal scrolling. Turning left of center scrolls the maze to the left; turning right scrolls it to the right. The further from center, the faster the scroll.

---

### Knob 4 — Scroll Y

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |

**Scroll Y** mirrors the behavior of **Scroll X** in the vertical axis. When Animate is off, it sets a fixed vertical offset. When Animate is on, it sets vertical scroll speed: center is stopped, and deviation from center controls direction and velocity.

Together, Scroll X and Scroll Y define a 2D drift vector that carries the maze across the screen. Setting both off-center produces diagonal scrolling.

---

### Knob 5 — Wall Color

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Wall Color** adjusts the brightness of the maze walls when **Wall Luma** is set to **Color** mode. At zero the walls are black, vanishing into darkness. As you increase the value, walls brighten through gray toward white. The walls also carry a subtle warm tint: a faint shift in the chrominance channels that gives them a slightly amber quality, reminiscent of aged concrete or old fluorescent lighting.

:::tip
When **Wall Luma** is set to **Video**, this knob has no effect (the input video's own brightness fills the walls instead.)
:::

---

### Knob 6 — Seed

| Property | Value |
|----------|-------|
| Range | 0 – 255 |
| Default | 0 |

**Seed** selects one of 256 distinct maze topologies. Each seed value produces a completely different arrangement of walls and corridors by initializing the hash cascade with a different starting value. Seed 0 might produce a labyrinth dense with dead ends; seed 127 might open wide boulevards and sparse intersections. Every seed is deterministic (return to the same value and the same maze reappears.)

Because the hash function has strong ***avalanche*** properties, adjacent seed values produce mazes that bear no visible resemblance to each other. Turning the knob slowly feels like channel-surfing through parallel architectures.

---

### Switch 7 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Animate** enables continuous scrolling of the maze. When set to **Off**, the **Scroll X** and **Scroll Y** knobs control a fixed spatial offset: you can position the maze manually, but it does not move on its own. When set to **On**, the scroll parameters become velocity controls, and the maze drifts continuously across the screen. The scroll accumulators update once per video frame, so the movement is smooth and frame-locked.

---

### Switch 8 — Maze Style

| Property | Value |
|----------|-------|
| Off | Grid |
| On | Organic |
| Default | Grid |

**Maze Style** selects between two structural algorithms. In **Grid** mode, walls are strictly orthogonal: only horizontal and vertical segments, creating clean right-angle intersections. In **Organic** mode, the hash cascade introduces diagonal adjacency checks and random wall fragments ("nubs") that roughen the edges and break the perfect grid into something more natural and weathered-looking, like crumbling stonework or eroded cave passages.

:::note
Organic mode does not change the underlying cell grid: cells are still square. It only modifies how walls are drawn within and between cells, adding texture and irregularity at cell boundaries.
:::

---

### Switch 9 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** swaps walls and corridors. Normally, walls are rendered with the wall color and corridors reveal the input video. When Invert is set to **On**, the roles reverse: the maze structure itself becomes transparent (showing the input video), and the corridor areas are filled with the wall color. The result is a negative-space labyrinth (you see the video only where walls used to be.)

---

### Switch 10 — Wall Luma

| Property | Value |
|----------|-------|
| Off | Color |
| On | Video |
| Default | Color |

**Wall Luma** selects the source of wall brightness. In **Color** mode, walls are filled with a solid color determined by the **Wall Color** knob, with a subtle warm chrominance tint. In **Video** mode, walls are filled with the input video's luminance value at that pixel, but stripped of chrominance: the walls become a monochrome ghost of the source image, visible only through the maze structure.

:::tip
***Video mode creates a double-image effect.*** The input video is visible through the corridors in full color *and* through the walls in monochrome. Adjusting **Mix** to blend between these two layers produces a textured overlay look.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input video directly to the output, bypassing all maze generation and mixing stages. Sync timing is still aligned via the delay pipeline, so switching Bypass on and off is glitch-free. Use it for instant A/B comparison.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0 – 100.0 |
| Default | 100.0 |

**Mix** crossfades between the dry input signal and the wet maze-composited output. At the minimum (fully left), the output is the unprocessed input video: no maze visible. At the maximum (fully right), the output is the full maze composite. Intermediate positions blend the two together, letting the maze structure fade in and out of the source image like a ghostly overlay.

---

## Background

### Binary Space Partitioning

The maze-generation algorithm behind Backrooms is a form of ***binary space partitioning*** (BSP), a technique from computer graphics where a space is recursively divided in half along alternating axes. Traditional BSP works on stored geometry; Backrooms implements it as a per-pixel decision function that requires no memory at all.

Each pixel is assigned to a grid cell based on its coordinates. The cell's address is fed through a four-level hash cascade, and at each level, certain walls are "opened" or "closed" based on specific bits of the hash output. The result is a hierarchical maze: coarse structure is determined at level 0, and each successive level refines the corridors by selectively removing walls. Because each hash level operates on the *output* of the previous level, the structure has true hierarchical dependency (it isn't just four independent grids superimposed.)

### The Hash Cascade

The core of the maze generation is a custom `hash_combine` function that mixes two 16-bit values through XOR, bit rotation, addition, and a fixed avalanche constant. The function is cascaded four times per pixel:

1. **Level 0** hashes the seed with the cell X coordinate, then combines the result with the cell Y coordinate. This determines the coarse wall structure (which cell edges have walls.)
2. **Level 1** refines the result by hashing with half-cell coordinates XORed with full-cell coordinates. Specific bits of the level-0 hash open corridors through coarse walls.
3. **Level 2** adds style-dependent variation. In Grid mode, it selectively removes walls for additional openings. In Organic mode, it checks diagonal adjacency bits to create curved, non-orthogonal passages.
4. **Level 3** produces the final hash for fine texture and feeds the pixel-level wall/corridor decision.

The ***avalanche property*** of the hash function: where changing one input bit changes roughly half the output bits: is what makes adjacent seed values produce completely different maze topologies.

### Scrolling and Animation

The maze's position is controlled by two 12-bit accumulators: one per axis. When animation is disabled, the scroll parameters map directly to accumulator values, giving a fixed offset. When animation is enabled, the parameters become signed velocities: the accumulator adds a speed-proportional value each frame, creating smooth, continuous drift.

Because the maze is computed from coordinates (not stored in memory), the scroll range is theoretically infinite. The accumulators wrap around at 12 bits (4096 pixels), but the hash function ensures no visible tiling: the maze on the far side of the wrap looks nothing like the maze at the origin.


---

## Signal Flow

### Signal Flow Notes

The defining characteristic of Backrooms is that the entire maze is computed ***combinationally from pixel coordinates***: there is no frame buffer, no BRAM, and no stored geometry. Every wall is a real-time function of the pixel's position and the seed. This is fundamentally different from programs that use delay lines or line buffers to create spatial effects.

Two key signal paths interact in the color output stage. The ***wall/corridor decision*** (an XOR gate combining the hash-derived wall flag with the Invert toggle) selects between two sources: the wall color generator and the delayed input video. In Color mode, wall pixels receive a solid luma value with a subtle warm tint (U offset negative, V offset positive). In Video mode, wall pixels receive the input's luminance with neutral chrominance. Corridor pixels always pass through the full input YUV unchanged. This dual-source architecture means the maze acts as a ***spatial key***: a binary mask that switches between two video layers on a pixel-by-pixel basis.


---

## Exercises

These exercises explore Backrooms from basic maze generation through animation and compositing. Since Backrooms is a synthesis program, no external source video is required: though patching an input signal into Videomancer reveals the maze's corridor-keying behavior.
### Exercise 1: Seed Surfing

![Seed Surfing result](/img/instruments/videomancer/backrooms/backrooms_ex1_s1.png)
*Seed Surfing — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A gallery of distinct maze architectures, exploring how the seed and cell parameters sculpt labyrinth structure.

#### Key Concepts

- Each seed produces a unique, deterministic maze topology
- Cell size and wall width shape the visual density of the labyrinth
- The hash function's avalanche property makes adjacent seeds look completely different

#### Steps

1. **Default maze**: With all settings at default, observe the maze pattern filling the screen. The corridors reveal whatever is patched to the input (or black if nothing is connected.)
2. **Seed walk**: Slowly turn **Seed** (Knob 6) through its full range. Each step produces a radically different labyrinth. Pause on a few favorites and study how walls connect and corridors branch.
3. **Scale up**: Turn **Cell Size** (Knob 1) clockwise to increase cell size. The maze opens up: corridors become wide, rooms become spacious. The labyrinth starts to feel architectural rather than fractal.
4. **Fatten the walls**: Increase **Wall Width** (Knob 2). Corridors narrow as walls thicken, until only thin slits remain. Back off to find a balance between wall and corridor.
5. **Wall brightness**: Sweep **Wall Color** (Knob 5) to set the brightness of the maze walls. Notice the subtle warm tint that gives the walls a slightly amber tone.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | 32 px |
| Wall Width | 50% |
| Scroll X | 180° |
| Scroll Y | 180° |
| Wall Color | 50% |
| Seed | (explore) |
| Animate | Off |
| Maze Style | Grid |
| Invert | Off |
| Wall Luma | Color |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Infinite Scroll

![Infinite Scroll result](/img/instruments/videomancer/backrooms/backrooms_ex2_s1.png)
*Infinite Scroll — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A continuously scrolling labyrinth that drifts diagonally across the screen, transitioning between rigid and organic maze styles.

#### Key Concepts

- Animate mode converts position knobs to velocity controls
- The maze is computed from coordinates, so scrolling is truly infinite
- Grid vs. Organic mode changes the structural character of the maze

#### Steps

1. **Enable animation**: Flip **Animate** (Switch 7) to **On**. Nothing moves yet (both scroll speeds default to center (stopped).)
2. **Horizontal drift**: Turn **Scroll X** (Knob 3) slightly clockwise from center. The maze begins to slide leftward. Turn it further and the speed increases.
3. **Diagonal motion**: Now adjust **Scroll Y** (Knob 4) off-center. The maze drifts diagonally. Experiment with the ratio between X and Y speed to change the drift angle.
4. **Go organic**: Flip **Maze Style** (Switch 8) to **Organic**. The clean right angles break apart into rougher, weathered-looking passages with random nubs at cell boundaries.
5. **Small cells, fast scroll**: Reduce **Cell Size** to its smallest setting (4 px) and increase scroll speed. The screen fills with a dense, rapidly scrolling texture (almost like a digital fabric unrolling.)

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | 8 px |
| Wall Width | 40% |
| Scroll X | ~210° |
| Scroll Y | ~240° |
| Wall Color | 30% |
| Seed | 42 |
| Animate | On |
| Maze Style | Organic |
| Invert | Off |
| Wall Luma | Color |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Labyrinth Keyer

![Labyrinth Keyer result](/img/instruments/videomancer/backrooms/backrooms_ex3_s1.png)
*Labyrinth Keyer — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A composited overlay where the maze structure keys between two video appearances: patch a live camera or pattern generator into the Videomancer input for best results.

#### Key Concepts

- The maze acts as a binary spatial key between wall color and corridor video
- Invert swaps which layer appears through which mask
- Video mode fills walls with input luma, creating a double-image effect

#### Steps

1. **Patch a source**: Connect a video signal to Videomancer's input. Feed something with recognizable shapes (a face, geometric patterns, or colorful footage.)
2. **See the corridors**: With default settings, the input video is visible through the maze corridors. Adjust **Cell Size** and **Wall Width** until the source is clearly recognizable through the grid.
3. **Invert the key**: Flip **Invert** (Switch 9) to **On**. Now the video appears where the walls were, and the wall color fills the corridors. The negative-space view of the same maze creates a very different composition.
4. **Video-modulated walls**: Flip **Wall Luma** (Switch 10) to **Video**. Both walls and corridors now show the input, but walls are stripped of chrominance (a full-color image behind a monochrome grid of itself.)
5. **Blend**: Reduce **Mix** (Fader 12) to about 50%. The maze structure softens into a ghostly overlay on top of the source. Combined with slow animation, the effect is of drifting architecture superimposed on the video.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | 32 px |
| Wall Width | 40% |
| Scroll X | 180° |
| Scroll Y | 180° |
| Wall Color | 50% |
| Seed | 168 |
| Animate | Off |
| Maze Style | Grid |
| Invert | On |
| Wall Luma | Video |
| Bypass | Off |
| Mix | 50% |

---
## Glossary

- **Avalanche Effect**: A property of hash functions where a small change in input (e.g., one bit) produces a large, unpredictable change in output. This is why adjacent seed values generate completely different mazes.

- **Binary Space Partitioning (BSP)**: A method for recursively subdividing a space into two halves. Backrooms uses a hash-based variant that computes subdivisions per-pixel without storing any geometry.

- **Cell**: A single square unit of the maze grid. Each cell may have walls on its edges or be open to its neighbors.

- **Corridor**: The open, passable regions of the maze where the input video (or black) shows through.

- **Fractal**: A structure that exhibits self-similarity at multiple scales. The four-level hash cascade gives the maze a fractal-like quality: coarse structure at level 0, finer detail at each subsequent level.

- **Hash Function**: A mathematical function that maps input data to a fixed-size output in a deterministic but seemingly random way. Backrooms uses XOR-rotate-add hashing.

- **Interpolator**: A hardware module that blends between two values based on a mix parameter. Three interpolators (one per YUV channel) implement the wet/dry crossfade.

- **Phase Accumulator**: A counter that adds a fixed increment each frame to produce smooth animation. The scroll accumulators are phase accumulators.

- **Seed**: An initial value fed into a deterministic algorithm to select one of many possible outputs. Different seeds produce different maze topologies from the same algorithm.

- **Spatial Key**: A binary mask that selects between two video sources on a per-pixel basis based on spatial position rather than signal content.

---
