---
draft: true
sidebar_position: 162
slug: /instruments/videomancer/labyrinth
title: "Labyrinth"
image: /img/instruments/videomancer/labyrinth/labyrinth_hero.png
description: "Labyrinth is a real-time procedural maze generator that draws its entire structure from a single hash function — no frame buffer, no stored map, zero BRAM."
---

![Labyrinth hero image](/img/instruments/videomancer/labyrinth/labyrinth_hero_s1.png)
*A procedural binary-tree maze wrapping the screen in glowing corridors, its walls shifting and reforming as the seed evolves frame by frame.*

---

## Overview

**Labyrinth** is a real-time maze synthesizer that draws an infinite, self-consistent grid of corridors and walls directly onto the video output. Unlike most maze programs that pre-compute a layout and store it in memory, Labyrinth generates its pattern ***procedurally***: every wall is a pure function of its grid position and a seed value, requiring zero block RAM. The result is a maze you can reshape instantly by turning a single knob.

At its simplest, Labyrinth overlays a static maze pattern in a chosen luminance over the incoming video. Turning up the **Evolve** control causes the seed to increment automatically, and the maze topology mutates in real time: walls dissolve and reform as corridors reroute themselves across the screen. Switch to **Invert** wall mode and the maze walls become inverted copies of the underlying video, creating a stained-glass window effect. Enable the **Explorer** and a bright green dot wanders the corridors on its own, tracing a path through the structure at a speed you control.

Because the maze is computed per-pixel with no frame buffer, Labyrinth is extremely lightweight on FPGA resources. It uses roughly 600 logic cells and zero BRAMs, leaving plenty of room for signal chain stacking with other programs.

### What's In a Name?

The name ***Labyrinth*** nods to the ancient architectural puzzle: a structure of branching corridors designed to confuse and contain. In mythology, the Labyrinth of Crete held the Minotaur at its center. Here, the maze holds your video signal. The program's algorithm is a ***binary tree maze***, one of the simplest procedural generators, where each cell opens a passage either east or south. The result is a perfect maze with exactly one path between any two cells: a true labyrinth.

---

## Quick Start

1. With video flowing through Videomancer, load **Labyrinth**. You should see a grid of white walls overlaid on your input signal. The default cell size is 16 pixels, creating a fine lattice.
2. Turn **Cell Size** (Knob 1) clockwise to enlarge the grid cells. The maze structure becomes bold and architectural. Turn **Wall Thk** (Knob 2) to fatten or slim the walls.
3. Now increase **Evolve** (Knob 4) past zero. The maze begins to shift: walls dissolve and reform as the seed advances. The faster you turn, the more frantic the mutation.
4. Flip **Explorer** (Switch 9) to **On**. A bright green dot appears in one of the cells and begins navigating the corridors. Adjust **Exp Speed** (Knob 6) to control how many cells it traverses per second.

---

## Parameters

![Videomancer front panel with Labyrinth loaded](/img/instruments/videomancer/labyrinth/labyrinth_control_panel.png)
*Videomancer's front panel with Labyrinth active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Cell Size

| Property | Value |
|----------|-------|
| Range | 8px – 64px |
| Default | 29px |

**Cell Size** sets the width and height of each maze cell in pixels. The control snaps to eight discrete sizes: at the smallest setting the maze is a fine mesh of tiny corridors, and at the largest it becomes a bold architectural grid with wide open rooms. Larger cells make the maze structure more legible from a distance, while smaller cells create a dense, textile-like pattern that can obscure the video beneath almost entirely.

:::tip
Cell size also determines how many cells fit on screen, which changes the ***complexity*** of the maze. Smaller cells pack more decision points into the frame, producing more intricate pathways.
:::

---

### Knob 2 — Wall Thk

| Property | Value |
|----------|-------|
| Range | 1px – 4px |
| Default | 2px |

**Wall Thk** (wall thickness) selects how many pixels wide each wall segment is, from a single-pixel hairline to a chunky four-pixel bar. Thicker walls emphasize the grid structure and reduce the visible corridor area, while thinner walls let more of the underlying video show through. The visual weight of the maze shifts dramatically between the extremes.

---

### Knob 3 — Seed

| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

**Seed** determines the maze topology. Each seed value produces a completely different arrangement of walls and corridors. Because the maze is generated procedurally from the seed, sweeping this control smoothly redraws the entire maze pattern in real time. Two different seed values will never produce the same layout.

:::note
Seed operates as a direct 10-bit value fed into the hash function. There are 1,024 distinct static maze patterns available.
:::

---

### Knob 4 — Evolve

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Evolve** controls the rate at which the seed automatically increments over time. At zero the maze is completely static: it holds a single frozen pattern determined by the **Seed** knob. As you increase Evolve, the seed advances by a small amount each video frame, causing walls to appear and disappear in a slow, organic mutation. At high values the maze transforms rapidly, producing a flickering, kaleidoscopic effect where no pattern persists for more than a few frames.

---

### Knob 5 — Wall Luma

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Wall Luma** sets the brightness of maze walls when **Wall Mode** is set to **Solid**. At zero the walls are black, becoming invisible against a dark background. At maximum the walls are peak white. This control has no effect when Wall Mode is set to **Invert**, because in that mode walls take their color from the inverted video signal instead of a flat luminance value.

---

### Knob 6 — Exp Speed

| Property | Value |
|----------|-------|
| Range | 0c/s – 64c/s |
| Default | 0c/s |

**Exp Speed** (explorer speed) controls how many cells per second the explorer dot traverses. The control snaps to eight discrete speeds. At the lowest non-zero setting the dot crawls through one cell per second; at maximum it races through up to 64 cells per second, streaking across the screen. When set to zero, the explorer is frozen in place even if it is visible.

:::tip
The explorer uses a simple directional walk through the maze topology. If it gets stuck in a loop, changing the **Seed** or enabling **Evolve** will alter the maze around it and free it into new corridors.
:::

---

### Switch 7 — Wall Mode

| Property | Value |
|----------|-------|
| Off | Solid |
| On | Invert |
| Default | Solid |

**Wall Mode** selects how maze walls are colored. In **Solid** mode, each wall pixel is drawn at the luminance set by **Wall Luma**, producing clean monochrome lines. In **Invert** mode, wall pixels display the ***complement*** of the underlying video: luminance is inverted and chroma channels are negated, creating a photographic-negative effect confined to the wall pattern. Invert mode turns the maze into a stained-glass overlay where corridors show the original image and walls show its negative.

---

### Switch 8 — Corridor

| Property | Value |
|----------|-------|
| Off | Video |
| On | Dimmed |
| Default | Video |

**Corridor** determines how the open areas between walls are rendered. In **Video** mode, corridors pass the input signal through unchanged: you see the original video in the open spaces. In **Dimmed** mode, corridor pixels are attenuated to roughly 70% brightness, creating a subtle shadow that makes the maze structure more visible against bright source material.

---

### Switch 9 — Explorer

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Explorer** enables or disables the animated explorer dot. When **On**, a bright green dot appears at a cell position and walks through the maze corridors according to the current direction and speed. The dot occupies a small cluster of pixels at the center of its current cell. When **Off**, no dot is drawn and the explorer logic is idle.

---

### Switch 10 — Border

| Property | Value |
|----------|-------|
| Off | Thin |
| On | Thick |
| Default | Thin |

**Border** selects between a thin and thick outer border around the entire maze frame. In **Thin** mode, the maze edge is defined only by the outermost cell walls. In **Thick** mode, a four-pixel-wide solid border is drawn around the entire active video area, giving the maze a distinct frame. The thick border is purely decorative and does not affect the internal maze topology.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all maze rendering. The sync delay pipeline still runs, so there is no timing glitch when toggling. Use Bypass for instant A/B comparison between the maze overlay and the clean input.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry input signal and the wet maze output. At zero the output is pure dry: identical to the unprocessed input. At maximum the output is pure wet: the full maze overlay. Intermediate values blend the two, allowing the maze pattern to be subtly ghosted over the video rather than stamped on at full opacity.

:::tip
Mix is implemented as a per-channel linear interpolation across Y, U, and V simultaneously. Partial mix values with **Invert** wall mode create dreamy double-exposure effects where the maze walls are translucent negatives.
:::

---

## Background

### Binary Tree Mazes

The ***binary tree maze*** is one of the simplest procedural maze algorithms. For every cell in the grid, a single binary decision is made: open a passage to the east, or open a passage to the south. That's it: one bit of information per cell. Despite this extreme simplicity, the result is a ***perfect maze***: a connected graph with exactly one path between any two cells and no loops.

Binary tree mazes have a characteristic visual signature: the north and west borders are always solid walls (because no cell ever opens northward or westward), and there is a strong diagonal bias running from the northwest corner toward the southeast. This diagonal texture is part of the charm: it gives the maze a windswept, organic quality that belies its mechanical origin.

The algorithm was popularized in the 1980s by one-line maze generators on the Commodore 64, where the program simply printed a random choice of "/" or "\" for each character position. Labyrinth implements the same principle in hardware, replacing the character grid with a pixel grid and the random number generator with a deterministic hash function seeded by the grid coordinates.

### Procedural Generation via Hashing

Labyrinth avoids storing the maze in memory entirely. Instead, it computes each cell's wall configuration ***on the fly*** as the video raster scans across the screen. For each pixel, the pipeline determines which grid cell it belongs to, hashes the cell coordinates together with the seed value, and reads a single bit of the result to decide whether the passage opens east or south.

The hash function combines the cell's X and Y coordinates with the seed using XOR and addition: a lightweight mixing operation that fits in a handful of logic cells. Because the same inputs always produce the same output, the maze is perfectly stable from frame to frame as long as the seed doesn't change. Changing the seed by even one count produces a completely different maze topology, which is what makes the **Evolve** control so visually striking.

:::note
Because the maze is a pure function of position and seed, there is no startup time and no initialization sequence. The maze appears fully formed on the very first frame after the program loads.
:::

### The Explorer

The explorer is an autonomous agent that walks through the maze topology one cell at a time. On each vertical sync pulse, it advances a configurable number of steps. At each step, it checks whether the passage ahead is open by evaluating the same hash function used to draw the walls. If the path is clear, it moves forward. If blocked, it turns and tries another direction.

The explorer's position is tracked as a pair of cell coordinates and a two-bit direction register (north, east, south, west). Its rendering is simple: when the raster scan reaches the cell matching the explorer's coordinates, a small cluster of bright green pixels is drawn at the cell center. The green color is fixed in hardware: Y=800, U=300, V=350: chosen for maximum visibility against both light and dark backgrounds.


---

## Signal Flow

### Signal Flow Notes

The maze pipeline is a six-clock-cycle cascade. The first clock captures the input and extracts sync edges. The second computes which grid cell the current pixel falls in by dividing the horizontal and vertical counters by the cell width. The third hashes the cell coordinates with the seed to determine whether the east or south passage is open, and evaluates neighbor hashes for the north and west walls. The fourth clock tests the pixel's local position within the cell against the wall thickness to produce a binary is-wall flag. The fifth overlays the explorer dot if applicable, and the sixth selects the output color: explorer green, wall color (solid or inverted), or corridor video (full or dimmed).

The explorer update runs ***once per frame*** on the vsync pulse, not per pixel. It evaluates the same `cell_hash` function to determine passability, advancing up to 64 steps per frame depending on the speed control. Because it shares the hash function with the rendering pipeline, the explorer's path is always consistent with the drawn walls (it never walks through a visible wall.)

:::tip
The data delay pipeline keeps a six-clock copy of the raw input Y, U, and V channels. The **Mix** fader interpolates between this delayed dry signal and the maze-rendered wet signal, so partial mix values always produce correctly timed blends with no horizontal smearing.
:::


---

## Exercises

These exercises progress from static mazes through evolving patterns to animated explorer journeys. Each one layers in more of Labyrinth's controls.
### Exercise 1: The Frozen Maze

![The Frozen Maze result](/img/instruments/videomancer/labyrinth/labyrinth_ex1_s1.png)
*The Frozen Maze — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A static, architectural maze overlay on top of live video (clean white corridors carved into the image.)

#### Key Concepts

- Binary tree mazes are generated procedurally from a seed
- Cell size controls maze complexity
- Wall thickness changes the visual weight of the structure

#### Steps

1. Load **Labyrinth** with video flowing. You should see a lattice of white walls.
2. Turn **Cell Size** (Knob 1) to its maximum setting. The maze becomes a bold grid of large rooms and wide corridors.
3. Set **Wall Thk** (Knob 2) to its maximum (4 px). The walls become thick bars, giving the maze a heavy, architectural feel.
4. Slowly sweep **Seed** (Knob 3) from one end to the other. Watch the entire maze topology change (every wall rearranges with each new seed value.)
5. Reduce **Cell Size** back to a middle setting. The maze becomes denser, with more corridors and decision points filling the screen.
6. Toggle **Border** (Switch 10) to **Thick** to add a solid frame around the maze.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | 64 px |
| Wall Thk | 4 px |
| Seed | ~500 |
| Evolve | 0% |
| Wall Luma | 100% |
| Exp Speed | 0 c/s |
| Wall Mode | Solid |
| Corridor | Video |
| Explorer | Off |
| Border | Thick |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Evolving Corridors

![Evolving Corridors result](/img/instruments/videomancer/labyrinth/labyrinth_ex2_s1.png)
*Evolving Corridors — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A living, breathing maze that mutates in real time: walls dissolving and reforming in an endless architectural animation.

#### Key Concepts

- Evolve increments the seed automatically each frame
- Wall Mode Invert creates photographic-negative walls
- Corridor Dimmed mode adds depth to the overlay

#### Steps

1. Start from a medium **Cell Size** (around 24 px) and moderate **Wall Thk** (2 px).
2. Increase **Evolve** (Knob 4) slowly from zero. The maze begins to shift. At low values, walls change gradually: one or two walls flicker per frame. At higher values the entire maze reshuffles continuously.
3. Set **Corridor** (Switch 8) to **Dimmed**. The open corridors darken slightly, giving the maze a sense of depth (as though you're looking down into recessed passageways.)
4. Flip **Wall Mode** (Switch 7) to **Invert**. The walls now display a photographic negative of the video passing beneath them. The evolving maze becomes a shifting kaleidoscope of inverted color.
5. Adjust **Wall Luma** (Knob 5): notice it has no effect while in Invert mode. Switch back to **Solid** and sweep Wall Luma to confirm it controls wall brightness in Solid mode only.
6. Reduce **Mix** (Fader 12) to about 50%. The maze becomes a semi-transparent ghost layer drifting over the video.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | 24 px |
| Wall Thk | 2 px |
| Seed | 0 |
| Evolve | ~40% |
| Wall Luma | 100% |
| Exp Speed | 0 c/s |
| Wall Mode | Invert |
| Corridor | Dimmed |
| Explorer | Off |
| Border | Thin |
| Bypass | Off |
| Mix | 50% |

---

### Exercise 3: The Explorer's Journey

![The Explorer's Journey result](/img/instruments/videomancer/labyrinth/labyrinth_ex3_s1.png)
*The Explorer's Journey — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated dot tracing a path through a slowly evolving maze: a tiny autonomous agent exploring an infinite procedural world.

#### Key Concepts

- The explorer navigates the maze topology autonomously
- Explorer speed is quantized into eight discrete rates
- Evolve and Explorer interact: the maze changes around the moving dot

#### Steps

1. Set a medium **Cell Size** (around 20 px) with **Wall Thk** at 2 px.
2. Set **Seed** to any value you like (this determines the starting maze.)
3. Enable **Explorer** (Switch 9). A bright green dot appears in one of the cells.
4. Increase **Exp Speed** (Knob 6) to a moderate rate (around 8 c/s). The dot begins moving through the corridors, turning at walls and navigating intersections.
5. Now slowly increase **Evolve** (Knob 4). The maze begins mutating around the explorer. Walls the dot was heading toward may vanish; new walls appear behind it. The explorer adapts in real time, always respecting the current maze state.
6. Set **Wall Mode** to **Solid** and reduce **Wall Luma** (Knob 5) to about 50%. The walls become a medium gray, making the green explorer dot stand out vividly against both walls and corridors.
7. Watch the dot's journey unfold. Each combination of Seed and Evolve rate produces a different behavioral pattern: sometimes the dot explores widely, sometimes it loops in a small region.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | 20 px |
| Wall Thk | 2 px |
| Seed | ~250 |
| Evolve | ~20% |
| Wall Luma | 50% |
| Exp Speed | 8 c/s |
| Wall Mode | Solid |
| Corridor | Video |
| Explorer | On |
| Border | Thin |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Binary Tree Maze**: A maze algorithm where each cell opens exactly one passage: either east or south: producing a perfect maze with a characteristic diagonal bias.

- **Cell**: A single rectangular unit of the maze grid, defined by **Cell Size**. Each cell contains one wall-decision bit.

- **Corridor**: The open passageway between walls where the underlying video (or a dimmed version of it) is visible.

- **Evolve**: The automatic seed increment that causes the maze topology to change over time, frame by frame.

- **Explorer**: An animated dot that autonomously navigates the maze corridors using directional walking logic.

- **Hash Function**: A deterministic mixing operation that converts cell coordinates and a seed into a wall decision, ensuring the same inputs always produce the same maze.

- **Perfect Maze**: A maze with exactly one path between any two cells and no loops (every cell is reachable from every other cell.)

- **Procedural Generation**: Creating content algorithmically at runtime rather than storing it in memory. Labyrinth's maze exists only as a function, never as stored data.

- **Seed**: A numeric value that determines the maze topology. Different seeds produce completely different wall arrangements.

---
