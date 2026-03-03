---
draft: true
sidebar_position: 163
slug: /instruments/videomancer/labyrinth
title: "Labyrinth"
image: /img/instruments/videomancer/labyrinth/labyrinth_hero.png
description: "Labyrinth is a real-time procedural maze generator that draws its entire structure from a single hash function — no frame buffer, no stored map, zero BRAM."
---

import labyrinth_hero from '/img/instruments/videomancer/labyrinth/labyrinth_hero.png';
import labyrinth_animation from '/img/instruments/videomancer/labyrinth/labyrinth_animation.gif';
import labyrinth_control_panel from '/img/instruments/videomancer/labyrinth/labyrinth_control_panel.png';
import labyrinth_exercise1_result from '/img/instruments/videomancer/labyrinth/labyrinth_exercise1_result.gif';
import labyrinth_exercise2_result from '/img/instruments/videomancer/labyrinth/labyrinth_exercise2_result.gif';
import labyrinth_exercise3_result from '/img/instruments/videomancer/labyrinth/labyrinth_exercise3_result.gif';

# Labyrinth

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={labyrinth_hero} alt="Labyrinth hero image"/>
*Labyrinth generating a procedural binary-tree maze with luminous corridors and an explorer dot traversing the passages.*
<img src={labyrinth_animation} alt="Labyrinth animated output"/>
*Labyrinth output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Labyrinth is a real-time procedural maze generator that draws its entire structure from a single hash function — no frame buffer, no stored map, zero BRAM. Every pixel on every frame computes its own wall-or-corridor status from its grid coordinates and a seed value. The result is a perfect binary-tree maze that fills the screen with configurable cell sizes, wall thicknesses, and wall brightness, all generated at pixel clock speed.

The name refers to the mythological labyrinth of Crete — the maze built by Daedalus to contain the Minotaur. In computing, maze generation is a classic algorithmic problem dating to the earliest days of personal computing. Labyrinth's approach is inspired by the legendary one-line Commodore 64 BASIC maze: `10 PRINT CHR$(205.5+RND(1)); : GOTO 10`, which generates a maze-like pattern by randomly choosing between two diagonal characters. Labyrinth applies a similar principle — each cell independently decides whether to open a passage east or south based on a deterministic hash — but extends it to a proper binary-tree maze with navigable corridors and an optional animated explorer dot.

At conservative settings — small cells, thin walls, moderate luminance — Labyrinth produces a fine grid overlay suitable for compositing or texture generation. At extreme settings — large cells, thick walls, full brightness — it generates bold architectural structures that command the screen. The Evolve parameter slowly mutates the seed, causing the maze topology to morph in real time, walls dissolving and reforming in an endless architectural dream.

---

## Background

### Binary-Tree Mazes

A **binary-tree maze** is one of the simplest perfect maze algorithms. For each cell in the grid, the generator makes exactly one random decision: open a passage either east or south (but not both). This single-bit choice per cell guarantees a connected, acyclic graph — a perfect maze with exactly one path between any two cells. The algorithm has a distinctive visual bias: the north and west borders are always solid (no cell can open northward or westward), creating two unbroken walls along the top and left edges. Labyrinth implements this by hashing each cell's coordinates with a seed to produce the east-or-south decision, making the entire maze a pure function of position and seed.

### Hash-Based Procedural Generation

Rather than storing a maze map in memory, Labyrinth computes each cell's wall configuration on the fly using a **hash function**. The hash takes the cell's X coordinate, Y coordinate, and a seed value, and produces a 16-bit result. Bit 0 of the hash determines whether the cell opens east or south. Because the hash is deterministic, the same seed always produces the same maze, and changing the seed produces a completely different topology. This approach requires zero BRAM — the maze exists only as a mathematical function evaluated at each pixel position.

### The Explorer

Labyrinth includes an optional animated explorer — a bright dot that moves through the maze corridors. On each frame (vsync), the explorer attempts to advance in its current direction. If a wall blocks the path, it turns. The explorer's speed is configurable in discrete steps, from stationary to 64 cells per second. The explorer provides visual proof that the generated structure is a navigable maze, not just a random wall pattern, and adds a dynamic element to an otherwise static pattern.

### Maze Generation in Computing History

The connection between maze generation and early computing runs deep. The Commodore 64 one-liner `10 PRINT CHR$(205.5+RND(1)); : GOTO 10` is perhaps the most famous single line of BASIC ever written — it fills the screen with a random pattern of forward and backward slash characters that reads as a maze-like texture. Labyrinth elevates this concept from a character-mode trick to a proper pixel-level maze with navigable corridors, configurable geometry, and real-time evolution.

### Video Overlay and Compositing

Although classified as a synthesis program, Labyrinth's Mix fader and corridor dimming options create hybrid possibilities. When Corridor mode is set to Video, the corridors pass the incoming video signal through — the maze becomes an overlay grid. When set to Dimmed, corridors show a darkened version of the input. Combined with the Wall Mode invert option, which replaces solid-color walls with inverted video, Labyrinth can function as a complex compositing tool that segments the screen into maze-defined regions.


---

## Signal Flow

```
Video Input (YUV 4:4:4) — used for corridor fill and bypass
│
├── Timing Detection ───────────────────────────────────────────
│   ├─ video_timing_generator (sync edge detection)
│   ├─ H counter (pixel position within scanline)
│   └─ V counter (scanline number within frame)
│
├── Seed Evolution ─────────────────────────────────────────────
│   └─ Accumulator: seed = seed_pot + evolve_counter(23..14)
│       (evolve_counter increments each vsync by evolve_pot)
│
├── Stage 1: Cell Coordinate Computation ───────────────────────
│   ├─ cell_x = h_count / cell_width
│   ├─ cell_y = v_count / cell_width
│   ├─ local_x = h_count mod cell_width
│   └─ local_y = v_count mod cell_width
│
├── Stage 2: Hash + Wall Decision ──────────────────────────────
│   ├─ hash = cell_hash(cell_x, cell_y, seed)
│   ├─ open_east = hash(0)
│   ├─ wall_east = NOT hash(0)
│   ├─ wall_south = hash(0)
│   ├─ wall_west = NOT cell_hash(cell_x-1, cell_y, seed)(0)
│   └─ wall_north = cell_hash(cell_x, cell_y-1, seed)(0)
│
├── Stage 3: Wall Rasterisation ────────────────────────────────
│   ├─ North wall: local_y < wall_thick AND wall_north
│   ├─ West wall: local_x < wall_thick AND wall_west
│   ├─ East wall: local_x >= cell_w - wall_thick AND wall_east
│   ├─ South wall: local_y >= cell_w - wall_thick AND wall_south
│   └─ Thick border: optional 4px outer frame
│
├── Stage 4: Explorer Overlay ──────────────────────────────────
│   └─ Bright green dot at cell center if explorer enabled and
│       pixel is in explorer's current cell
│
├── Stage 5: Color Mux ────────────────────────────────────────
│   ├─ Explorer pixel: Y=800, U=300, V=350 (bright green)
│   ├─ Wall pixel:
│   │   ├─ Solid (normal): Y = Wall Luma, U = 512, V = 512
│   │   └─ Invert: Y = 1023−input_Y, U = 1023−input_U, V = 1023−input_V
│   └─ Corridor pixel:
│       ├─ Video: pass-through input Y, U, V
│       └─ Dimmed: Y = input_Y × 700/1024, U/V pass-through
│
├── Interpolator Mix ───────────────────────────────────────────
│   └─ 3× interpolator_u: crossfade delayed input ↔ maze output
│
├── Sync / Data Delay (6 clocks) ───────────────────────────────
│   └─ Shift registers for sync signals and Y, U, V
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed (mix output) or raw input
```

The maze is entirely stateless — every pixel recomputes its wall membership from scratch using the `cell_hash` function. Neighboring cells' walls are also recomputed to determine the current cell's north and west boundaries (a cell's north wall is the south wall of the cell above; a cell's west wall is the east wall of the cell to the left). The hash function XORs bit-rotated coordinates with the seed, producing a pseudo-random but deterministic wall pattern. The explorer updates its position once per vsync (frame), attempting up to 4 movement steps per frame depending on the speed setting. The seed evolution accumulator adds the Evolve register value on each frame, so even small Evolve settings eventually cause the maze to change — higher values cause faster mutation. The thick border option draws a 4-pixel solid frame around the entire screen, ensuring the maze has a visible outer boundary.

---

## Parameter Reference

<img src={labyrinth_control_panel} alt="Videomancer front panel with Labyrinth loaded"/>
*Videomancer's front panel with Labyrinth active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 8px – 64px |
| Default | 29px |
| Suffix | px |

Controls the width of each maze cell in pixels. The register is quantized to 8 discrete steps mapping to cell widths of 8, 12, 16, 20, 24, 32, 48, and 64 pixels. At the smallest setting, hundreds of tiny cells fill the screen in a dense labyrinthine mesh. At the largest, only a handful of cells are visible — each corridor is wide enough to pass a bus through. Cell width also determines cell height (cells are square), so changing this parameter uniformly scales the entire maze geometry.

---

#### Knob 2 — Wall Thk
| Property | Value |
|----------|-------|
| Range | 1px – 4px |
| Default | 2px |
| Suffix | px |

Controls the thickness of maze walls in pixels. Quantized to 4 discrete steps: 1, 2, 3, or 4 pixels. At 1 pixel, the walls are hairline-thin and the corridors dominate. At 4 pixels, the walls become substantial structural elements. Wall thickness interacts with cell size — at small cell sizes, thick walls can consume a significant fraction of the cell area, leaving only narrow corridors. At large cell sizes, even 4-pixel walls appear as fine lines relative to the corridor width.

---

#### Knob 3 — Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Sets the initial seed for the maze hash function. Different seed values produce entirely different maze topologies — every wall in the grid changes when the seed changes. This is the primary pattern selection control. Because the hash is deterministic, returning to the same seed value always reproduces the same maze. When Evolve is active, this provides the starting point for the evolution sequence.

---

#### Knob 4 — Evolve
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the speed of maze evolution. When set above zero, an accumulator adds the register value to an internal counter on each frame. The upper bits of this counter are added to the seed, causing the maze topology to slowly mutate over time. At low values, the maze changes imperceptibly — walls shift every few seconds. At high values, the maze morphs rapidly, walls dissolving and reforming in a continuous architectural flux. At zero, the maze is static, locked to the Seed parameter value.

---

#### Knob 5 — Wall Luma
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Sets the luminance of wall pixels when Wall Mode is set to Solid (normal). At 0%, walls are black — invisible against a dark corridor background but visible when corridors pass video. At 100%, walls are maximum white. This control has no effect when Wall Mode is set to Invert, because inverted walls derive their brightness from the input video signal rather than this parameter.

---

#### Knob 6 — Exp Speed
| Property | Value |
|----------|-------|
| Range | 0c/s – 64c/s |
| Default | 0c/s |
| Suffix | c/s |

Controls the speed of the explorer dot in discrete steps. The register is quantized to 8 levels: 0 (stationary), 1, 2, 4, 8, 16, 32, and 64 cells per second. At zero, the explorer remains fixed at its starting position. At higher speeds, it moves through the corridors more quickly, changing direction when it encounters walls. The explorer is only visible when the Explorer toggle (Toggle 9) is enabled.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Wall Mode** | Solid | Invert |
| **8 — Corridor** | Video | Dimmed |
| **9 — Explorer** | Off | On |
| **10 — Border** | Thin | Thick |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options. Wall Mode and Corridor mode affect how walls and corridors are rendered. Explorer enables the animated dot. Border adds a thick outer frame. Bypass is the standard signal routing switch. Each bit is decoded independently from `registers_in(6)`.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the delayed input signal and the maze output via three `interpolator_u` instances (one per Y/U/V channel). At 0% (register 0), the output is the delayed input — no maze visible. At 100% (register 1023), the output is fully the maze signal. Intermediate values create a semi-transparent maze overlay where the wall structure is partially blended with the input video.

---

## Guided Exercises

These exercises progress from a basic static maze to an evolving labyrinth with an animated explorer, exploring the interactions between cell geometry, wall rendering, and seed evolution.

### Exercise 1: Static Maze Grid

<img src={labyrinth_exercise1_result} alt="Static Maze Grid result"/>
*Static Maze Grid — simulated result across source images.*
**Objective**: Learn how cell size, wall thickness, and seed define the maze structure.

1. **Default maze**: With all controls at default, observe the maze pattern. Note the square cells with walls connecting in a tree-like pattern.
2. **Cell size sweep**: Turn Cell Size from minimum to maximum. Watch the maze transition from a dense fine mesh to a few large corridors. Count the approximate number of cells at each extreme.
3. **Wall thickness**: Starting with Cell Size at step 3 (~16px), sweep Wall Thickness through all 4 steps. Note the discrete jumps — 1px hairlines to 4px solid walls.
4. **Seed exploration**: Slowly sweep the Seed knob. Each position produces a completely different maze topology. Note how the change is instantaneous — the entire grid reconfigures simultaneously.
5. **Wall luminance**: Sweep Wall Luma from 0% to 100%. The walls fade from invisible black to bright white. This confirms that corridor brightness is independent of wall brightness.

**Key concepts**: Binary-tree maze algorithm, hash-based procedural generation, deterministic seed-to-topology mapping, discrete parameter quantization

---

### Exercise 2: Evolving Corridors

<img src={labyrinth_exercise2_result} alt="Evolving Corridors result"/>
*Evolving Corridors — simulated result across source images.*
**Objective**: Explore seed evolution to create a maze that morphs over time, and use the explorer to navigate it.

1. **Start evolution**: Set Evolve to ~20%. The maze begins to slowly mutate — walls dissolve and new ones form. Watch for several seconds to see the transformation.
2. **Speed up**: Increase Evolve to ~60%. The mutation accelerates — the maze becomes a continuously shifting structure.
3. **Enable explorer**: Turn Explorer (Toggle 9) On. A bright green dot appears and begins navigating the corridors.
4. **Explorer speed**: Increase Exp Speed to step 4 (~50%). The explorer moves faster, visibly navigating passages and turning at walls.
5. **Thick border**: Enable Border (Toggle 10). A solid frame appears around the screen, enclosing the maze and preventing edge corridors from appearing to extend off-screen.
6. **Freeze**: Set Evolve back to 0%. The maze freezes, but the explorer continues navigating the static structure, demonstrating that evolution and navigation are independent.

**Key concepts**: Evolve accumulator adds to seed over time, explorer uses wall-following navigation, border provides visual frame, evolution and navigation are independent

---

### Exercise 3: Inverted Maze Compositing

<img src={labyrinth_exercise3_result} alt="Inverted Maze Compositing result"/>
*Inverted Maze Compositing — simulated result across source images.*
**Objective**: Use Wall Mode invert and Corridor dimming to create a complex compositing effect where the maze segments the video into complementary regions.

1. **Feed live video**: Ensure an active video source is connected for corridor pass-through.
2. **Enable invert**: Set Wall Mode to Invert. Walls now display the inverted video signal — wherever the corridor shows normal video, the adjacent wall shows its negative.
3. **Dim corridors**: Set Corridor to Dimmed. The corridor (normal) video darkens, making the inverted walls more prominent by contrast.
4. **Large cells**: Set Cell Size to step 6 (~75%). The large cells create bold geometric partitions of the screen — each corridor region shows dimmed video, each wall region shows inverted video.
5. **Mix blend**: Lower Mix to ~60%. The maze overlay becomes semi-transparent, blending the segmented regions with the original input.
6. **Evolve**: Set Evolve to ~15%. The segmentation boundaries slowly shift as walls dissolve and reform, creating an ever-changing compositing map.

**Key concepts**: Inverted walls create complementary video regions, corridor dimming enhances wall/corridor contrast, large cells as compositional partitions, evolving segmentation

---


## Tips

- **Seed is your starting point**: Each seed value produces a unique maze. Sweep the Seed knob slowly to browse maze topologies and find one that fits your composition.
- **Evolve at low values for subtlety**: Even very low Evolve settings create gradual maze mutation — walls shift over seconds or minutes, adding organic temporal variation without disorienting rapid change.
- **Cell Size defines the scale**: Small cells create fine texture; large cells create bold architecture. The 8 discrete steps provide a good range from dense mesh to wide-open corridors.
- **Wall Mode Invert for compositing**: Inverted walls turn the maze into a video segmentation tool — corridors and walls show complementary views of the source, creating a split-reality effect.
- **Explorer proves navigability**: The green explorer dot is more than decoration — it visually demonstrates that the generated structure is a valid, navigable maze with connected corridors.
- **Corridor dim enhances contrast**: When corridors pass video through unchanged, they can overpower the wall structure. Dimming the corridors makes the maze pattern more visible without completely hiding the video content.
- **Mix for transparency**: At 50% mix with a live video source, the maze becomes a semi-transparent overlay — useful for subtle grid effects without dominating the composition.
- **Feedback creates fractal mazes**: Routing Labyrinth's output back to its input creates recursive maze-on-maze patterns — corridors within corridors, walls within walls.

---

## Glossary

| Term | Definition |
|------|------------|
| **Binary-tree maze** | A maze generation algorithm where each cell opens exactly one passage (east or south), producing a perfect maze with a single path between any two cells. |
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric. Labyrinth uses zero BRAM — the maze is computed procedurally. |
| **Cell** | One unit of the maze grid. Each cell has four potential walls (north, south, east, west) and an interior corridor. |
| **Deterministic** | A process that always produces the same output for the same input. Labyrinth's hash function is deterministic — the same seed always produces the same maze. |
| **Explorer** | An animated dot that navigates the maze corridors, changing direction upon encountering walls. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable integrated circuit that generates the maze pattern at pixel clock speed. |
| **Hash function** | A mathematical function that maps input values to pseudo-random output values. Used here to determine wall placement from cell coordinates and seed. |
| **Interpolator** | A linear crossfade module (`interpolator_u`) that blends two signals based on a mix parameter. |
| **Perfect maze** | A maze with exactly one path between any two cells — no loops and no isolated regions. |
| **Pipeline** | A series of sequential processing stages on each clock cycle; Labyrinth uses a 6-clock pipeline. |
| **Procedural generation** | Creating content algorithmically rather than storing it in memory. Labyrinth generates the entire maze from a hash function with zero storage. |
| **Seed** | An initial value fed to the hash function that determines the maze topology. Different seeds produce different mazes. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
