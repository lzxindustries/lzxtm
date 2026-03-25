---
draft: true
sidebar_position: 65
slug: /instruments/videomancer/conway
title: "Conway"
image: /img/instruments/videomancer/conway/conway_hero.png
description: "Conway's Game of Life is the most famous cellular automaton, devised by mathematician John Horton Conway in 1970."
---

![Conway hero image](/img/instruments/videomancer/conway/conway_hero_s1.png)
*Conway's Game of Life cellular automaton rendered as luminous cells on a 16×16 toroidal grid, evolving generation by generation into emergent patterns of digital life.*

---

## Overview

Conway is a self-contained ***cellular automaton*** synthesizer that runs a complete implementation of Conway's Game of Life on a 16×16 toroidal grid. Rather than processing incoming video, it generates its own imagery from scratch: a colony of living and dead cells evolving according to simple mathematical rules that produce surprisingly complex, unpredictable behavior. The grid wraps around at every edge, so patterns that drift off the right side reappear on the left, and patterns that fall off the bottom emerge from the top.

Each cell occupies a rectangular tile of pixels, scaled to fit the current video resolution. Living cells glow with adjustable brightness and optional color. Dead cells are black. The simulation advances at a speed you control, from glacially slow single steps to a rapid cascade of generations. A density control determines how many cells are alive when the grid is first seeded, and two seed parameters let you dial in different starting arrangements for repeatable or exploratory results.

:::tip
Conway is a ***synthesis*** program. It generates its own visuals rather than processing an input signal. However, the **Mix** fader lets you blend the cellular automaton output with any incoming video for layered compositions.
:::

### What's In a Name?

**Conway** is named after the British mathematician John Horton Conway, who invented the ***Game of Life*** in 1970. Despite its name, it isn't a game you play: it's a ***zero-player game***, a simulation you set in motion and observe. Conway designed the rules to be as simple as possible while still producing behavior complex enough to be interesting. He succeeded spectacularly: patterns in the Game of Life can compute, replicate, and organize in ways that continue to surprise mathematicians and hobbyists alike, more than fifty years later.

---

## Quick Start

1. The grid begins with a random population of living cells. Watch the colony evolve as generations tick forward automatically.
2. Turn **Density** (Knob 2) counter-clockwise to thin the initial population, then flip **Reset** (Switch 9) to **On** and back to **Off** to reseed the grid. A sparse starting population tends to produce more recognizable patterns and ***still lifes***.
3. Enable **Grid** (Switch 8) to see faint lines outlining each cell. This makes it easier to follow individual cells as they are born and die.
4. Flip **Color** (Switch 10) to **Hue** and sweep **Cell Hue** (Knob 5) to paint the living cells in shifting colors.

---

## Parameters

![Videomancer front panel with Conway loaded](/img/instruments/videomancer/conway/conway_control_panel.png)
*Videomancer's front panel with Conway active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Speed** controls how many video frames elapse between each generation of the simulation. At 0%, the automaton advances at its fastest rate: roughly one generation per frame. As **Speed** increases toward 100%, a frame divider stretches the interval between updates, slowing the evolution to a leisurely crawl. At maximum, dozens of frames pass between each generation tick.

:::note
The speed control is inverted relative to what you might expect: lower values produce faster evolution; higher values produce slower evolution. Think of it as a "deliberation time" knob (how long the colony pauses to consider its next move.)
:::

---

### Knob 2 — Density

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Density** sets the probability that each cell starts alive when the grid is seeded. At 0%, the grid begins nearly empty: only a few scattered survivors. At 50%, roughly half the cells spring to life. At 100%, the grid starts almost completely full. Very low and very high densities tend to collapse quickly into stable or dead configurations; moderate densities between 20% and 50% produce the longest-lived, most interesting evolutions.

---

### Knob 3 — Seed X

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Seed X** controls the horizontal component of the ***LFSR*** seed value that determines the initial random arrangement of cells. Changing this knob produces a completely different starting pattern, even when **Density** stays the same. Combined with **Seed Y**, these two controls give you access to over a million distinct starting arrangements.

---

### Knob 4 — Seed Y

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Seed Y** controls the vertical component of the LFSR seed value. Together with **Seed X**, it determines the exact initial configuration of living and dead cells. If you find a starting pattern you like, note both seed positions: returning to the same **Seed X** and **Seed Y** values with the same **Density** will reproduce the identical starting grid.

:::tip
**Seed X** and **Seed Y** are concatenated to form a 16-bit LFSR seed. The upper 10 bits come from **Seed X** and the lower 6 bits from **Seed Y**, so **Seed X** has finer control over the starting pattern.
:::

---

### Knob 5 — Cell Hue

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Cell Hue** sets the chrominance of living cells when **Color** (Switch 10) is set to **Hue** mode. At 0%, cells take on one extreme of the hue spectrum. At 100%, they shift to the opposite extreme. Sweeping this knob smoothly rotates through the available color range. In **Mono** mode, this control has no visible effect (cells remain neutral gray.)

The hue is applied by mapping the pot value to the U channel and its complement to the V channel, producing a diagonal sweep through YUV color space rather than a full 360° hue rotation.

---

### Knob 6 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Bright** controls the luminance of living cells. At 0%, living cells are completely black: indistinguishable from dead cells. At 100%, living cells glow at maximum brightness. When **Grid** is enabled, the grid lines are drawn at 1/16th of the **Bright** value, so they remain visible but subdued relative to the cells.

---

### Switch 7 — Run

| Property | Value |
|----------|-------|
| Off | Pause |
| On | Run |
| Default | Run |

**Run** controls whether the simulation advances. In the **Run** position, the automaton computes new generations at the rate set by **Speed**. In the **Pause** position, the current generation is frozen on screen: no cells are born or die until you flip back to **Run**. Pausing is useful for studying a particular arrangement of cells, or for dramatic live performance timing.

---

### Switch 8 — Grid

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Grid** enables thin lines drawn at the boundary of every cell, creating a visible lattice over the playing field. With **Grid** set to **Off**, only the living cells themselves are visible, floating on a black background. With **Grid** set to **On**, a faint framework outlines the full 16×16 grid, making it easier to count neighbors and track individual cell fates across generations.

---

### Switch 9 — Reset

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Reset** re-seeds the grid with a new random population when toggled from **Off** to **On**. The new population is determined by the current **Density**, **Seed X**, and **Seed Y** values. After the grid has been re-seeded, flip **Reset** back to **Off** to allow the simulation to proceed. The reset is edge-triggered (only the transition from Off to On initiates the reseed.)

:::note
**Reset** also restarts after power-on if the grid hasn't been seeded yet. The very first seed happens automatically at startup using the default **Seed X**, **Seed Y**, and **Density** values.
:::

---

### Switch 10 — Color

| Property | Value |
|----------|-------|
| Off | Mono |
| On | Hue |
| Default | Mono |

**Color** selects between **Mono** and **Hue** rendering modes. In **Mono** mode, living cells are rendered as neutral gray at the brightness set by **Bright**: the U and V channels sit at the midpoint (512), producing no color. In **Hue** mode, the **Cell Hue** knob controls the chrominance of living cells, painting them in color. Dead cells and grid lines are always neutral regardless of this toggle.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input video directly to the output, bypassing Conway's cellular automaton rendering entirely. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use **Bypass** for instant A/B comparison between the raw input and the Conway overlay.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the delayed input video and the cellular automaton output. At 0%, only the original input is visible: the automaton is completely hidden. At 100%, only the Conway output is visible. Intermediate positions blend the two, allowing you to layer the grid of evolving cells over incoming footage for composite effects.

:::tip
With **Mix** at around 50%, living cells appear as bright overlays on top of your input video, creating a compelling interaction between the geometric automaton grid and organic video content.
:::

---

## Background

### Cellular automata

A ***cellular automaton*** is a grid of cells, each in one of a finite number of states, that evolves in discrete time steps according to a fixed set of rules. The idea was pioneered by John von Neumann and Stanislaw Ulam in the 1940s as a way to study self-reproducing systems. Each cell's next state depends only on its current state and the states of its immediate neighbors. Despite this radical simplicity, cellular automata can produce behavior of extraordinary complexity: oscillating patterns, traveling structures, and even universal computation.

### The B3/S23 rule

Conway's Game of Life uses the ***B3/S23*** rule set, which means:

- **Birth (B3)**: A dead cell with exactly 3 living neighbors becomes alive.
- **Survival (S23)**: A living cell with 2 or 3 living neighbors stays alive.
- **Death**: A living cell with fewer than 2 neighbors dies of isolation. A living cell with more than 3 neighbors dies of overcrowding.

These three rules, applied simultaneously to every cell on the grid, are sufficient to produce ***gliders*** (patterns that translate across the grid), ***oscillators*** (patterns that cycle between states), ***still lifes*** (stable patterns that never change), and even ***glider guns*** (oscillators that periodically emit traveling gliders). On a 16×16 grid these larger structures are rare, but small oscillators and still lifes appear constantly.

### Toroidal topology

Conway's grid on Videomancer is ***toroidal***: the top edge wraps to the bottom, and the left edge wraps to the right. Imagine folding the grid into a doughnut shape. This means every cell always has exactly 8 neighbors, even the corner cells. The toroidal topology prevents edge effects and allows gliders and other traveling patterns to loop around the grid indefinitely rather than crashing into walls.

### Double buffering

The FPGA implements ***double buffering***: two complete copies of the 16×16 grid are stored in registers. While one buffer is being displayed on screen, the next generation is computed and written into the other buffer. At the next vertical sync, the buffers swap. This ensures the display never shows a partially computed generation (every frame shows a complete, consistent state.)


---

## Signal Flow

### Signal Flow Notes

The engine operates in two phases synchronized to the video timing. During ***vertical blanking***, the game engine runs: either seeding the grid with LFSR-generated random values, or computing the next generation by scanning all 256 cells sequentially (one cell per clock cycle). During ***active video***, the renderer reads the front buffer and maps each pixel's position to its corresponding cell, looking up whether that cell is alive or dead.

The LFSR seed is constructed by concatenating the 10-bit **Seed X** pot value with the lower 6 bits of the **Seed Y** pot value. The density threshold comparison (`lfsr(9:0) < density_pot`) means that higher **Density** values admit more cells. The speed divider subtracts a scaled pot value from 60 to determine the number of frames between generations, so lower pot values yield faster simulation rates.

:::note
The generation compute is entirely sequential: 256 clock cycles to process all cells. On a 74.25 MHz clock, this takes roughly 3.4 microseconds, well within the vertical blanking interval of any supported video standard.
:::


---

## Exercises

These exercises explore Conway's Game of Life from sparse, contemplative starting conditions through dense, chaotic populations, culminating in a mixed-media composition with incoming video.
### Exercise 1: Still Lifes and Oscillators

![Still Lifes and Oscillators result](/img/instruments/videomancer/conway/conway_ex1_s1.png)
*Still Lifes and Oscillators — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A sparse colony that evolves quickly into a collection of ***still lifes*** (stable blocks, beehives) and ***oscillators*** (blinkers, toads) scattered across the grid.

#### Key Concepts

- Sparse populations tend to settle into stable or oscillating patterns
- The B3/S23 rules produce recognizable structures at low density
- Grid overlay helps track individual cell behavior

#### Steps

1. Set **Density** (Knob 2) to about 15% (just a few dozen cells alive.)
2. Flip **Reset** (Switch 9) to **On** and back to **Off** to seed a sparse grid.
3. Enable **Grid** (Switch 8) to see the cell boundaries.
4. Set **Speed** (Knob 1) to about 50% so generations advance slowly enough to follow.
5. Watch the colony settle. Within a few dozen generations, most activity will stop, leaving isolated clusters that either sit still or blink.
6. Try different **Seed X** and **Seed Y** values and reset again. Each seed produces a different family of survivors.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 50% |
| Density | 15% |
| Seed X | 50% |
| Seed Y | 50% |
| Cell Hue | 50% |
| Bright | 75% |
| Run | Run |
| Grid | On |
| Reset | Off |
| Color | Mono |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Dense Chaos in Color

![Dense Chaos in Color result](/img/instruments/videomancer/conway/conway_ex2_s1.png)
*Dense Chaos in Color — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dense, turbulent colony rendered in vivid color, evolving at high speed into a restless, ever-changing mosaic.

#### Key Concepts

- High density creates turbulent, rapidly evolving populations
- Color mode visualizes cells with chromatic hue
- Speed control shapes the rhythm of evolution

#### Steps

1. Set **Density** (Knob 2) to about 80%.
2. Flip **Reset** (Switch 9) to reseed the grid with a packed starting population.
3. Set **Speed** (Knob 1) to about 10% for fast evolution.
4. Switch **Color** (Switch 10) to **Hue** and sweep **Cell Hue** (Knob 5) to find a color you like.
5. Turn **Bright** (Knob 6) to about 90% so cells glow intensely.
6. Watch the dense population roil: large swaths of cells flicker between life and death before the population stabilizes or dies out.
7. If the grid goes completely dead, try a different **Seed X** or **Seed Y** and reset again.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 10% |
| Density | 80% |
| Seed X | 50% |
| Seed Y | 50% |
| Cell Hue | 40% |
| Bright | 90% |
| Run | Run |
| Grid | On |
| Reset | Off |
| Color | Hue |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Living Texture Overlay

![Living Texture Overlay result](/img/instruments/videomancer/conway/conway_ex3_s1.png)
*Living Texture Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A composite image where the Conway grid is layered over incoming video, adding a rhythmic, evolving digital texture to the source material.

#### Key Concepts

- Mix fader blends automaton output with input video
- Cellular automaton as a generative texture layer
- Pause allows freezing a pattern for static overlay

#### Steps

1. Connect a video source to Videomancer's input.
2. Set **Density** (Knob 2) to about 30% and **Speed** (Knob 1) to about 25% for a moderate, rhythmic evolution.
3. Enable **Color** (Switch 10) in **Hue** mode and set **Cell Hue** (Knob 5) to complement your source footage.
4. Lower **Mix** (Fader 12) to about 50%. The cellular automaton grid appears as a translucent overlay on top of the incoming video.
5. Adjust **Bright** (Knob 6) to balance the cell brightness against the video content.
6. When you see an interesting pattern, flip **Run** (Switch 7) to **Pause** to freeze it as a static texture overlay.
7. Resume with **Run** to let the pattern continue evolving.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 25% |
| Density | 30% |
| Seed X | 50% |
| Seed Y | 50% |
| Cell Hue | 40% |
| Bright | 75% |
| Run | Run |
| Grid | Off |
| Reset | Off |
| Color | Hue |
| Bypass | Off |
| Mix | 50% |

---
## Glossary

- **B3/S23**: The specific rule set used by Conway's Game of Life: birth on exactly 3 neighbors, survival on 2 or 3 neighbors.

- **Cellular Automaton**: A grid of cells that evolves in discrete steps according to fixed rules based on neighbor states.

- **Double Buffering**: A technique where two copies of the grid are maintained so the display always shows a complete generation while the next is computed.

- **Glider**: A small pattern in the Game of Life that translates across the grid, appearing to move.

- **LFSR**: Linear Feedback Shift Register; a hardware-efficient pseudo-random number generator used here to seed the initial grid.

- **Oscillator**: A pattern that cycles between two or more states indefinitely, such as a blinker (period 2) or a toad (period 2).

- **Still Life**: A stable pattern that does not change from one generation to the next, such as a 2×2 block or a beehive.

- **Toroidal**: A topology where opposite edges of the grid are connected, forming the surface of a torus (doughnut shape).

---
