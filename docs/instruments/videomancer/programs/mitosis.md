---
draft: true
sidebar_position: 195
slug: /instruments/videomancer/mitosis
title: "Mitosis"
image: /img/instruments/videomancer/mitosis/mitosis_hero.png
description: "Mitosis is a 2D cellular automaton engine that evolves a pixel grid through discrete generations according to configurable birth and survival rules."
---

![Mitosis hero image](/img/instruments/videomancer/mitosis/mitosis_hero_s1.png)
*Mitosis growing luminance-seeded cellular automaton colonies that bloom, decay, and recolor across the video frame.*

---

## Overview

Mitosis is a real-time cellular automaton synthesizer that grows organic, self-replicating visual structures from living video. It analyzes the brightness of incoming video to decide where new cells are born, then evolves those cells through configurable birth, survival, and decay rules: producing patterns that crawl, sparkle, pulse, and cascade across the screen like digital organisms. The result is a constantly shifting landscape where the boundaries between "image" and "effect" dissolve into something alive.

Four selectable rule sets give Mitosis distinctly different personalities. Growth mode produces stable, expanding colonies. Seeds mode creates ephemeral sparkles that flash and vanish. Brain mode introduces a three-state lifecycle: alive, dying, dead: for pulsing, wave-like textures. Cascade mode is aggressive, spreading life across the frame with minimal input. Each rule set responds differently to the same video, making Mitosis feel like four programs in one.

:::tip
Because Mitosis seeds its cells from your input video's brightness, the content of whatever you feed it ***shapes*** the automaton's behavior. A face becomes a colony. A waveform becomes a trail of sparks. Mitosis turns every video signal into a living petri dish.
:::

### What's In a Name?

***Mitosis*** is the biological process by which a single cell divides into two identical daughter cells. In biology, mitosis is the engine of growth: every organism you've ever seen exists because of trillions of successful cell divisions. This program borrows that metaphor: bright pixels in the input video act as seeds, and the cellular automaton rules govern how those seeds divide, spread, and eventually die. The visual result: clusters of cells blooming outward from points of brightness: mirrors the look of cell cultures growing under a microscope.

---

## Quick Start

1. Set **Birth Thresh** (Knob 1) to about 50% and feed in a video signal with some bright areas. Wherever the video is bright enough, new cells are born (you'll see bright patches appear against a dark background.)
2. Set both **Rule Bit 0** (Switch 7) and **Rule Bit 1** (Switch 8) to **Off** to select the Growth rule. Cells spread outward from the bright seed points, forming stable colonies.
3. Turn **Color Map** (Knob 3) clockwise past the midpoint. The monochrome cells gain color: green, then warm orange, then electric blue as you sweep through the four color zones.
4. Adjust **Evolve Rate** (Knob 2) to slow down or speed up the automaton's evolution. Watch the colonies grow in slow motion or race across the frame.

---

## Parameters

![Videomancer front panel with Mitosis loaded](/img/instruments/videomancer/mitosis/mitosis_control_panel.png)
*Videomancer's front panel with Mitosis active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Birth Thresh

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Birth Thresh** sets the luminance threshold for seeding new cells from the input video. At 0%, fully counterclockwise, even the dimmest pixels in the input signal are bright enough to birth new cells: the entire frame becomes a seed bed. As the threshold rises, only progressively brighter regions of the input can inject life into the automaton. At 100%, fully clockwise, only the absolute brightest pixels trigger cell birth.

Think of Birth Thresh as a sensitivity dial. Low values mean the automaton responds to everything in the input video. High values mean it responds only to highlights: a spotlight, a bright edge, a specular reflection. The character of the automaton's growth changes dramatically based on how many seed points it receives.

:::note
Birth Thresh interacts with **Seed Mode** (Switch 9). In Continuous mode, cells are seeded every frame based on the threshold. In Evolve mode, seeding happens only once, and then the automaton runs autonomously on whatever cells were initially born.
:::

---

### Knob 2 — Evolve Rate

| Property | Value |
|----------|-------|
| Range | 1 – 60 |
| Default | 31 |

**Evolve Rate** controls how frequently the cellular automaton updates its state. At the lowest values (counterclockwise), the automaton evolves on every single video frame: cells are born, live, and die at full speed. As you turn the knob clockwise, evolution slows: the automaton updates every second frame, then every fourth, then every eighth, and finally every sixteenth frame at maximum.

Slow evolution rates let you observe the automaton's behavior in detail. Fast rates produce fluid, animated textures. At medium settings, the automaton has a deliberate, pulsing quality (each generation is visible as a distinct step.)

---

### Knob 3 — Color Map

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Color Map** selects the chroma palette applied to living and dying cells. The knob sweeps through four color zones arranged in order from counterclockwise to clockwise:

1. **Monochrome** (0 to 25%): no color is added. Cells appear as pure luminance: white when alive, gray when dying, black when dead.
2. **Green-Cyan** (25 to 50%): cells acquire a cool, organic tint. The U channel shifts below neutral and V follows slightly, producing colors reminiscent of algae or mold growing under a microscope.
3. **Warm Plasma** (50 to 75%): U drops while V rises, creating warm oranges and magentas. The overall look is fiery and visceral, like plasma or molten glass.
4. **Electric Blue** (75 to 100%): U rises while V drops, producing vivid blues and cyans. The effect is cold, digital, and electric.

:::tip
The color mapping is applied to the cell's ***state value***, not the input video. An alive cell at full brightness gets the strongest chroma. A dying cell fading toward zero gets progressively less color. This means color intensity tracks the lifecycle of each cell.
:::

---

### Knob 4 — Dead Opacity

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Dead Opacity** controls how much of the original input video is visible where cells are dead. At 0%, fully counterclockwise (the default), dead cells are completely black: the original video is invisible behind the automaton. As you increase Dead Opacity, the input video bleeds through in the dead zones, creating a composite where the automaton sits on top of the source material.

At 100%, dead areas show the full input video at original brightness. The automaton's living and dying cells still overlay the image in their assigned colors, but the background is no longer black (it's the video itself.)

---

### Knob 5 — Neighborhood

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Neighborhood** adjusts the structure of the cellular automaton's neighborhood by controlling whether the diagonal (north-west) neighbor is included in the alive-neighbor count. Below 50%, only the north and west neighbors are counted: a two-neighbor ***Von Neumann***-style neighborhood tilted by 45 degrees. Above 50%, the north-west neighbor is also counted, expanding the effective neighborhood to three cells.

This seemingly small change has large effects on the automaton's behavior. With two neighbors, birth and survival conditions are harder to satisfy, producing sparser, more structured patterns. With three neighbors, more cells participate in each decision, producing denser growth and more chaotic evolution.

:::note
The streaming nature of the FPGA means only ***causal*** neighbors are available: north (previous line), north-west (previous line, previous pixel), and west (current line, previous pixel). This creates a natural directional bias (patterns tend to grow toward the south-east.)
:::

---

### Knob 6 — Decay Rate

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Decay Rate** controls how quickly dying cells fade to black. When a cell transitions from alive to dying, its state value begins at 511 and decreases each generation. The Decay Rate parameter sets how much is subtracted per generation. At low values (counterclockwise), cells fade slowly, leaving long luminous trails. At high values (clockwise), cells snap from alive to dead almost instantly, with little or no visible dying phase.

Decay Rate interacts differently with each rule set. In Growth mode, decay creates glowing halos around stable colonies. In Seeds mode, it controls the length of the sparkle trails. In Brain mode, it determines the width of the "dying" wavefront that separates alive and dead regions.

---

### Switch 7 — Rule Bit 0

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |


---

### Switch 8 — Rule Bit 1

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |


---

### Switch 9 — Seed Mode

| Property | Value |
|----------|-------|
| Off | Cont. |
| On | Evolve |
| Default | Cont. |

**Seed Mode** controls whether the input video continuously injects new cells into the automaton (**Cont.**) or seeds it only once and then lets it evolve autonomously (**Evolve**). In Continuous mode, bright pixels in every frame can birth new cells, creating a perpetual interaction between the live video and the automaton. In Evolve mode, cells are seeded from the input video until the first vertical sync boundary, after which the automaton runs on its own: no new cells are injected regardless of what the input video shows.

Evolve mode is useful for observing pure automaton dynamics without ongoing interference from the video signal. Continuous mode keeps the automaton tethered to the input, constantly refreshing and reshaping its colonies.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** reverses the brightness mapping of the color output stage. When enabled, a cell with a state value of 1023 (fully alive) is mapped to minimum brightness, and a cell at state 0 (dead) would be mapped to maximum brightness. This effectively creates a negative image of the automaton's state (what was bright becomes dark, and vice versa.)

Invert does not affect the automaton's internal logic. Cells still live and die by the same rules. It only changes how the state values are translated into visible luminance and chroma during the color mapping stage.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all cellular automaton processing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the automaton output.

---

:::note Toggle Group Notes

**Rule Bit 0** (Switch 7) and **Rule Bit 1** (Switch 8) combine to form a two-bit rule selector. Together they choose one of four cellular automaton rule sets:

| Rule Bit 1 | Rule Bit 0 | Rule | Behavior |
|------------|------------|------|----------|
| Off | Off | Growth | Birth if exactly 2 alive neighbors. Survive if 1 or more. Stable, expanding colonies. |
| Off | On | Seeds | Birth if exactly 2 alive neighbors. Never survive — alive cells die immediately. Ephemeral sparkles. |
| On | Off | Brain | Three-state lifecycle: alive → dying → dead. Birth if exactly 2 alive neighbors. Pulsing wavefronts. |
| On | On | Cascade | Birth if 1 or more alive neighbors. Survive if 2 or more. Aggressive, rapid spread. |

:::tip
The four rules are dramatically different. **Growth** is the most stable and predictable. **Seeds** is the most chaotic and transient. **Brain** produces the most visually complex wave patterns. **Cascade** fills the screen the fastest. Try each one with the same input to see how profoundly the rules shape the automaton's personality.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the delayed dry input signal and the wet cellular automaton output. At 0%, only the original input video is visible. At 100% (the default), only the automaton output is visible. Intermediate values blend the two, creating a ghostly overlay where the automaton's living cells float on top of the source video.

:::tip
**Mix** and **Dead Opacity** offer two different ways to reveal the input video behind the automaton. **Dead Opacity** shows the input only where cells are dead, creating a figure/ground separation. **Mix** blends the input uniformly across the entire frame. Combining both produces complex layered composites.
:::

---

## Background

### Cellular Automata

A ***cellular automaton*** (CA) is a grid of cells, each of which can be in one of several states. At each time step, every cell examines its neighbors and applies a fixed rule to decide its next state. Despite this simplicity, cellular automata can produce astonishingly complex behavior: from stable structures to chaotic patterns to self-replicating organisms. The most famous cellular automaton is John Conway's ***Game of Life***, invented in 1970, which demonstrated that a handful of simple rules on a grid could produce structures that move, grow, and even compute.

Mitosis implements a variation on these ideas. Instead of the traditional eight-neighbor Moore neighborhood, it uses a three-neighbor causal neighborhood (north, north-west, west) dictated by the FPGA's streaming architecture. This constraint gives the automaton its characteristic directional bias: patterns flow toward the south-east like ink spreading across wet paper.

### Birth, Survival, and Decay

Classical cellular automata operate on binary states: a cell is either alive or dead. Mitosis extends this to a 10-bit state space. Values from 512 to 1023 represent "alive" cells. Values from 1 to 511 represent "dying" cells in various stages of decay. Zero is dead. This graduated state space allows for smooth visual transitions between life and death, producing glowing trails, fading wavefronts, and luminous halos that pure binary automata cannot achieve.

The four rule sets implement different ***birth/survival*** specifications (a notation borrowed from the Life-like automaton community, where "B2/S1" means "birth if 2 alive neighbors, survive if 1 or more"). Each rule set creates fundamentally different dynamics from the same underlying grid.

### Video Seeding

Traditional cellular automata start from a fixed initial condition: a hand-drawn pattern or a random scatter. Mitosis instead seeds its cells from the incoming video signal. The Birth Thresh parameter acts as a luminance gate: pixels brighter than the threshold inject alive cells into the grid. This creates a feedback loop where the video content shapes the automaton's growth, and the automaton's output color-maps the result back to video. The input signal becomes the DNA of the organism.


---

## Signal Flow

### Signal Flow Notes

The pipeline processes video in a six-stage streaming architecture, followed by a four-clock interpolator mix (ten clocks total). The critical path runs through the cellular automaton's state machine: each pixel reads its north neighbor from BRAM (previous scanline), gathers its north-west and west neighbors from pipeline registers, counts alive neighbors, applies the selected rule, writes the new state back to BRAM, and then maps the result to color (all within the active video region.)

Two design details shape the visual output. First, the neighbourhood is ***causal***: the FPGA can only look at pixels it has already processed (north, north-west, west), never south or east. This means patterns always grow toward the south-east corner of the frame, giving the automaton a distinctive directional flow. Second, the ping-pong BRAM arrangement means each scanline reads the *previous* generation's data and writes the *current* generation's data to the alternate bank. The bank selector toggles at the start of each active line, so the north neighbor always comes from the immediately preceding scanline's output.

:::note
Because the automaton processes one pixel per clock in raster order, the "west" neighbor is actually the cell computed one clock cycle ago on the ***current*** line: not the previous generation. This means horizontal propagation is instantaneous within a single generation, while vertical propagation takes one full frame. This asymmetry is what gives Mitosis its characteristic cascading, waterfall-like motion.
:::


---

## Exercises

These exercises explore Mitosis's four rule sets and their interactions with seeding, color, and decay. Each exercise produces a different class of organic visual texture.
### Exercise 1: Growing Colonies

![Growing Colonies result](/img/instruments/videomancer/mitosis/mitosis_ex1_s1.png)
*Growing Colonies — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Grow stable colonies of cells that expand from bright regions of the input video, surrounded by luminous halos of dying cells.

#### Key Concepts

- The Growth rule produces stable, expanding cellular structures
- Birth Thresh controls where cells are born from input video
- Decay Rate shapes the glowing halo around living colonies

#### Steps

1. Set **Birth Thresh** (Knob 1) to about 50%. Bright areas in the input video begin spawning cells.
2. Both rule toggles should be **Off** (this selects Growth mode.)
3. Set **Evolve Rate** (Knob 2) to a low value for fast evolution. Watch colonies expand outward from the seed points.
4. Turn **Decay Rate** (Knob 6) to about 40%. Dying cells now leave visible trails (a glowing halo appears around each colony.)
5. Sweep **Color Map** (Knob 3) through the four color zones. The colonies shift from monochrome to green, warm plasma, and electric blue.
6. Increase **Dead Opacity** (Knob 4) to about 30%. The input video appears in the dead zones between colonies, creating a composite.

#### Settings

| Control | Value |
|---------|-------|
| Birth Thresh | 50% |
| Evolve Rate | ~20 |
| Color Map | 60% |
| Dead Opacity | 30% |
| Neighborhood | 50% |
| Decay Rate | 40% |
| Rule Bit 0 | Off |
| Rule Bit 1 | Off |
| Seed Mode | Cont. |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Sparkling Seeds

![Sparkling Seeds result](/img/instruments/videomancer/mitosis/mitosis_ex2_s1.png)
*Sparkling Seeds — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated field of short-lived sparkles: cells that flash into existence and immediately die, leaving brief luminous trails that follow the contours of the input video.

#### Key Concepts

- The Seeds rule creates ephemeral sparkles that never survive
- Continuous seeding produces an ongoing rain of flashes
- Decay Rate controls how long each sparkle trails

#### Steps

1. Set **Rule Bit 0** (Switch 7) to **On** and **Rule Bit 1** (Switch 8) to **Off** to select Seeds mode.
2. Set **Birth Thresh** (Knob 1) to about 40%. Seed points appear wherever the video is moderately bright.
3. Set **Seed Mode** (Switch 9) to **Cont.** so new sparkles are born every frame.
4. Reduce **Decay Rate** (Knob 6) to about 25%. Each sparkle leaves a visible trail before fading to black.
5. Set **Color Map** (Knob 3) to about 80% for electric blue sparkles against a dark background.
6. Now toggle **Invert** (Switch 10). The sparkles become dark flashes against a bright field (a photographic negative of the effect.)

#### Settings

| Control | Value |
|---------|-------|
| Birth Thresh | 40% |
| Evolve Rate | ~15 |
| Color Map | 80% |
| Dead Opacity | 0% |
| Neighborhood | 50% |
| Decay Rate | 25% |
| Rule Bit 0 | On |
| Rule Bit 1 | Off |
| Seed Mode | Cont. |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Brain Waves

![Brain Waves result](/img/instruments/videomancer/mitosis/mitosis_ex3_s1.png)
*Brain Waves — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Pulsing wave patterns that radiate outward from initial seed points. Once seeded, the automaton runs on its own, producing expanding rings and interference patterns reminiscent of chemical reaction-diffusion systems.

#### Key Concepts

- The Brain rule creates three-state wavefronts (alive → dying → dead)
- Evolve-only seed mode lets the automaton run autonomously
- Neighborhood changes the density and character of wave propagation

#### Steps

1. Set **Rule Bit 0** (Switch 7) to **Off** and **Rule Bit 1** (Switch 8) to **On** to select Brain mode.
2. Set **Seed Mode** (Switch 9) to **Evolve**. The automaton will seed once from the input video and then run autonomously.
3. Set **Birth Thresh** (Knob 1) to about 30% to provide a generous initial scatter of seed cells.
4. Set **Decay Rate** (Knob 6) to about 50%. The dying wavefront is visible as a band of intermediate brightness trailing behind the alive wavefront.
5. Sweep **Neighborhood** (Knob 5) from low to high. Below the midpoint, waves are sparse and angular. Above the midpoint, waves become fuller and more complex as the diagonal neighbor participates.
6. Set **Color Map** (Knob 3) to about 40% for a green-cyan palette. The three-state lifecycle becomes visually distinct: bright alive cells, green-tinted dying cells, and black dead cells.
7. Slowly increase **Evolve Rate** (Knob 2) to watch the waves in slow motion.

#### Settings

| Control | Value |
|---------|-------|
| Birth Thresh | 30% |
| Evolve Rate | ~30 |
| Color Map | 40% |
| Dead Opacity | 0% |
| Neighborhood | 75% |
| Decay Rate | 50% |
| Rule Bit 0 | Off |
| Rule Bit 1 | On |
| Seed Mode | Evolve |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Birth**: The transition of a dead cell to an alive state, triggered when the cell's alive-neighbor count satisfies the active rule's birth condition.

- **Causal Neighborhood**: A neighborhood that includes only pixels already processed in raster scan order: north, north-west, and west: producing a directional bias in the automaton's growth.

- **Cellular Automaton**: A system of cells on a grid, each updating its state at each time step according to fixed rules based on neighbor states. Abbreviated CA.

- **Decay**: The gradual reduction of a dying cell's state value toward zero, controlled by the Decay Rate parameter.

- **Dying**: An intermediate cell state (values 1 to 511) between alive and dead, producing visible luminous trails during the transition.

- **Interpolator**: A hardware component that performs linear crossfading between two signals, used here for the wet/dry mix.

- **Neighborhood**: The set of adjacent cells examined when computing a cell's next state. Mitosis uses a three-cell causal neighborhood: north, north-west, and west.

- **Ping-Pong Buffer**: A dual-bank memory strategy where one bank is read while the other is written, alternating each scanline to store the previous generation's cell states.

- **Rule Set**: A specific combination of birth and survival conditions that governs the cellular automaton's behavior. Mitosis offers four: Growth, Seeds, Brain, and Cascade.

- **Seed**: A cell injected into the alive state by the input video's luminance exceeding the Birth Thresh parameter.

- **Survival**: The condition that allows an alive cell to remain alive in the next generation, rather than transitioning to dying or dead.

---
