---
draft: true
sidebar_position: 13
slug: /instruments/videomancer/backrooms
title: "Backrooms"
image: /img/instruments/videomancer/backrooms/backrooms_hero.png
description: "Every generation discovers its own image of infinitely repeating, inescapable architecture."
---

import backrooms_hero from '/img/instruments/videomancer/backrooms/backrooms_hero.png';
import backrooms_animation from '/img/instruments/videomancer/backrooms/backrooms_animation.gif';
import backrooms_control_panel from '/img/instruments/videomancer/backrooms/backrooms_control_panel.png';
import backrooms_exercise1_result from '/img/instruments/videomancer/backrooms/backrooms_exercise1_result.gif';
import backrooms_exercise2_result from '/img/instruments/videomancer/backrooms/backrooms_exercise2_result.gif';
import backrooms_exercise3_result from '/img/instruments/videomancer/backrooms/backrooms_exercise3_result.gif';

# Backrooms

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={backrooms_hero} alt="Backrooms hero image"/>
*Backrooms generating infinite recursive maze corridors with video fill, revealing source imagery through procedural labyrinth geometry.*
<img src={backrooms_animation} alt="Backrooms animated output"/>
*Backrooms output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Every generation discovers its own image of infinitely repeating, inescapable architecture. For the internet era that image is the Backrooms — an endlessly recursing set of empty office corridors, fluorescent-lit and yellow-carpeted, stretching in every direction with no exit and no center. Backrooms takes that concept and builds it in hardware: a real-time procedural maze generator that creates infinite scrolling labyrinths from pure computation, with no memory storage whatsoever.

The maze is computed per-pixel using a cascade of XOR-rotate hash functions seeded by a user-selectable Seed parameter. Four levels of recursive hashing create fractal-like corridor structures from hierarchical cell coordinates. Input video is visible through the corridors while walls render in configurable solid color (or modulated by input luma), producing a layered mashup where recognizable imagery peers through procedurally generated geometry. The entire maze can scroll continuously in any direction, creating the sensation of navigating an endless architectural space.

At small cell sizes, the maze reads as an intricate grid texture overlaid on the source. At large cell sizes, it becomes an architecturally scaled labyrinth where entire objects in the source video become visible through corridor openings. The Seed parameter completely changes the maze topology — each of the 256 seeds produces a deterministically different layout, so the same source video can be viewed through entirely different spatial configurations.

---

## Background

### Binary Space Partitioning and Maze Generation

The classic algorithm for generating mazes involves recursively subdividing a grid of cells by removing walls to create connected passages. Backrooms implements a variation of this concept entirely in combinational logic: rather than storing a maze in memory and reading it back, the program *recomputes* whether each pixel is a wall or corridor on the fly, using the pixel's cell coordinates as input to a hash function. The hash is deterministic — the same cell coordinates with the same seed always produce the same wall configuration — so the maze is stable and repeatable even though nothing is stored.

### Hash Functions and Procedural Generation

Procedural content generation in computer graphics relies heavily on hash functions: algorithms that take a set of coordinates and produce a pseudo-random but deterministic output. Backrooms uses a cascade of XOR-rotate-add operations — a common technique in fast integer hashing. The hash takes the seed, the cell's X coordinate, and the cell's Y coordinate, then combines them through four stages of nonlinear mixing. Different bits of the hash output control different properties: whether horizontal or vertical walls exist, whether corridors open at specific locations, and whether extra texture fragments appear in organic mode.

### Scrolling Coordinate Spaces

When the Animate toggle is engaged, the maze scrolls continuously by adding a per-frame accumulator offset to the pixel coordinates before hashing. Because the hash function operates on the *scrolled* coordinates, the maze pattern appears to slide smoothly across the frame. The scroll speed is derived from the Scroll X/Y knobs interpreted as signed velocity values — 180° (center) is stationary, and values above or below move in opposite directions. In manual mode the same knobs set a fixed position offset, allowing precise framing of a static maze.

### Grid vs. Organic Topology

The Maze Style toggle fundamentally changes the maze's visual character. In Grid mode, walls are strictly orthogonal — only horizontal and vertical segments appear, creating clean right-angle labyrinths. In Organic mode, diagonal hash values are folded into the wall decision logic, and extra wall fragments are added at sub-threshold coordinates. The result is a rougher, more cave-like topology with irregular passages and textured wall surfaces, as though the corridors have eroded over time.

### Video Through Architecture

The compositing model is spatially binary: each pixel is either a corridor (showing input video) or a wall (showing generated color). The Wall Color knob controls wall luma intensity, and the Wall Luma toggle switches between solid color walls and video-modulated walls. In video-modulated mode, wall pixels use the input luma but discard chroma, creating a monochromatic ghosting effect where the source content is visible everywhere but with different color treatment in wall versus corridor regions.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Pixel Position ─────────────────────────────────────────────
│   │
│   ├─ 1. Pixel/Line Counters    (h_count, v_count from timing)
│   ├─ 2. Scroll Offset          (accumulate or direct from pots)
│   ├─ 3. Scrolled Coordinates   (pixel + scroll_offset)
│   └─ 4. Cell Decomposition     (cell_xy = pixel >> shift,
│                                  frac_xy = pixel AND mask)
│
├── Maze Computation ───────────────────────────────────────────
│   │
│   ├─ 5. Hash Level 0           (seed × cell_x × cell_y → coarse grid)
│   ├─ 6. Hash Level 1           (refine with half-cell coords)
│   ├─ 7. Hash Level 2           (organic diagonal mixing)
│   ├─ 8. Hash Level 3           (fine detail + final wall bits)
│   └─ 9. Wall Decision          (frac_xy vs threshold → is_wall)
│
├── Color Output ───────────────────────────────────────────────
│   │
│   ├─ 10. Invert                (swap wall/corridor)
│   ├─ 11. Wall Color Gen        (solid or video-modulated luma)
│   └─ 12. Corridor Passthrough  (input video for non-wall pixels)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ 13. Interpolator × 3      (dry/wet crossfade Y, U, V)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical design insight is that the entire maze is computed *combinationally* from pixel coordinates — no BRAMs, no LFSRs, no delay lines. Each pixel's wall/corridor status is determined by hashing its cell coordinates through four cascaded XOR-rotate stages. The wall thickness comparison happens at stage 6 (hash level 3), where the pixel's fractional position within its cell is compared against a threshold derived from the Wall Width parameter scaled to the current cell size. The Invert toggle simply XORs the final wall decision bit, swapping which regions show video and which show wall color.

---

## Parameter Reference

<img src={backrooms_control_panel} alt="Videomancer front panel with Backrooms loaded"/>
*Videomancer's front panel with Backrooms active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 4px – 64px |
| Default | 27px |
| Suffix | px |

Controls the maze cell size in discrete steps from 4 to 128 pixels. Smaller cells create denser, more intricate mazes with narrow corridors and many intersections. Larger cells create architecturally scaled labyrinths where each corridor is wide enough to frame entire objects in the source video. The stepped control ensures cells align to power-of-two boundaries, which is essential for the integer hash function to produce clean wall edges without sub-pixel artifacts.

---

#### Knob 2 — Wall Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls wall thickness as a proportion of cell size. At low values, walls are thin hairlines with wide corridors — the source video dominates and the maze reads as a delicate overlay grid. At high values, the walls thicken and corridors narrow to slits, inverting the visual balance so the maze structure dominates with only glimpses of video visible through tight passages. Combined with Invert, this control defines whether the program feels like video-with-grid or grid-with-video.

---

#### Knob 3 — Scroll X
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |
| Suffix | ° |

Sets the horizontal scroll position or speed depending on the Animate toggle state. In manual mode, the knob directly positions the maze horizontally — useful for precisely framing a static composition. In animate mode, the knob controls scroll velocity: center (180°) is stationary, left of center scrolls leftward, right of center scrolls rightward. Higher offsets from center produce faster scrolling. The scroll wraps seamlessly because the hash function operates on the scrolled coordinates modulo the cell grid.

---

#### Knob 4 — Scroll Y
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |
| Suffix | ° |

Sets the vertical scroll position or speed, operating identically to Scroll X but on the vertical axis. Combined horizontal and vertical scrolling creates diagonal movement through the maze — the direction and speed of diagonal motion depend on the vector sum of both scroll rates. In animate mode, setting both knobs off-center produces continuous diagonal scrolling that reveals new maze topology flowing into the frame from one corner.

---

#### Knob 5 — Wall Color
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the brightness of wall surfaces when in Color mode (Wall Luma toggle set to Color). At 0%, walls are black — the maze reads as a dark grid over bright video. At 100%, walls are maximum brightness — the maze reads as a bright grid. The wall color includes a subtle warm tint (slightly shifted U and V) that prevents walls from looking purely neutral, giving the maze surfaces a faintly architectural quality.

---

#### Knob 6 — Seed
| Property | Value |
|----------|-------|
| Range | 0 – 255 |
| Default | 0 |

Selects one of 256 maze topology seeds. Each seed value produces a completely different maze layout — different wall placements, different corridor configurations, different connectivity. Because the hash function has good avalanche properties, even adjacent seed values produce visually unrelated mazes. This parameter is the creative "dice roll": when you find a source image you like, scrolling through seeds lets you audition completely different maze structures around the same content.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Maze Style** | Grid | Organic |
| **9 — Invert** | Off | On |
| **10 — Wall Luma** | Color | Video |
| **11 — Bypass** | Off | On |

The five toggle switches control independent binary features that shape the maze's visual character and compositing behavior. Animate enables continuous scrolling versus manual positioning. Maze Style selects between clean orthogonal Grid corridors and rough Organic cave-like passages. Invert swaps wall and corridor regions, fundamentally changing which parts of the image show source video. Wall Luma switches wall surfaces between solid generated color and input video luma (monochromatic). Bypass passes the input signal through unprocessed.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0 – 100.0 |
| Default | 100.0 |

Controls the dry/wet mix between the original input video and the maze-processed output. At 0% (fully dry), the output is the unprocessed input. At 100% (fully wet), the output is the full maze composite. Intermediate values crossfade between the two, allowing the maze to be blended subtly over the source as a semi-transparent overlay.

---

## Guided Exercises

These exercises progress from a simple static overlay to an animated infinite labyrinth, exploring how cell size, wall thickness, topology, and scroll interact to create different spatial relationships between maze and source content.

### Exercise 1: Architectural Grid

<img src={backrooms_exercise1_result} alt="Architectural Grid result"/>
*Architectural Grid — simulated result across source images.*
**Objective**: Create a clean geometric grid overlay that frames the source architecture through maze corridors.

1. Set Cell Size to step 5 (64 px) for architecturally scaled corridors.
2. Set Wall Width to 25% for thin but visible walls.
3. Center Scroll X and Scroll Y at 180° for a static maze.
4. Set Animate to Off.
5. Set Maze Style to Grid for clean right angles.
6. Adjust Wall Color to 50% for mid-gray walls.
7. Set Wall Luma to Color for uniform wall surfaces.
8. Leave Invert Off — corridors show the source video.
9. Set Mix to 100% for full effect.
10. Slowly turn the Seed knob to audition different maze layouts until the corridors frame interesting portions of the source architecture.

**Key concepts**: Cell size determines the spatial relationship between maze and source. At 64 pixels, corridors are wide enough to frame architectural details like individual windows. The Seed knob is the creative selector — it cycles through completely different maze topologies while keeping all other parameters constant.

---

### Exercise 2: Infinite Scrolling Labyrinth

<img src={backrooms_exercise2_result} alt="Infinite Scrolling Labyrinth result"/>
*Infinite Scrolling Labyrinth — simulated result across source images.*
**Objective**: Create a continuously scrolling infinite maze with organic topology, demonstrating the procedural nature of the generation.

1. Set Cell Size to step 4 (32 px) for medium-density corridors.
2. Set Wall Width to 40% for balanced wall/corridor ratio.
3. Set Animate to On to enable continuous scrolling.
4. Set Scroll X to about 220° (moderate rightward drift).
5. Set Scroll Y to about 240° (moderate downward drift).
6. Switch Maze Style to Organic for rough cave-like passages.
7. Set Wall Color to 15% for dark walls that recede visually.
8. Set Seed to 128 for a mid-range topology.
9. Set Mix to 100%.
10. Observe the infinite scroll — new maze structure flows continuously into frame.

**Key concepts**: Organic mode adds diagonal hash mixing and wall texture fragments, creating passages that feel eroded and natural rather than architectural. The continuous scroll demonstrates that the maze extends infinitely — the hash function generates consistent topology at every coordinate, with no visible tiling or repetition within the practical scroll range.

---

### Exercise 3: Video-Modulated Maze Inversion

<img src={backrooms_exercise3_result} alt="Video-Modulated Maze Inversion result"/>
*Video-Modulated Maze Inversion — simulated result across source images.*
**Objective**: Explore the Invert and Wall Luma Video modes to create a dual-layer effect where the source content is visible in both wall and corridor regions with different color treatment.

1. Set Cell Size to step 3 (16 px) for dense, fine corridors.
2. Set Wall Width to 50% to equalize wall and corridor area.
3. Set Scroll X and Scroll Y to 180° (static).
4. Set Animate to Off.
5. Set Maze Style to Grid.
6. Switch Wall Luma to Video — walls now show monochromatic source luma.
7. Set Wall Color to 80% (controls intensity modulation in video mode).
8. Enable Invert — now corridors show the wall color and walls show video.
9. Observe the dual rendering: the face is visible in both regions, colored in one and monochromatic in the other.
10. Slowly sweep Seed to find a layout where the maze grid creates interesting tonal separations through the face.

**Key concepts**: With Wall Luma set to Video, wall pixels inherit the input's brightness while discarding chroma. When combined with Invert, this creates a figure-ground reversal where both regions show the same image but with different color treatment — full color in one, monochrome in the other. The maze becomes a per-pixel color/mono masking system driven by procedural geometry.

---


## Tips

- **Start with large cells**: Begin at 64 px cell size to understand the maze structure before reducing to denser configurations. The maze is easier to read when corridors are wide.
- **Use Seed as a creative tool**: Different seeds produce radically different mazes. When you find a good combination of source content and parameter settings, scroll through seeds to find the best spatial arrangement.
- **Organic mode pairs with scrolling**: The rough, textured corridors of Organic mode look most effective when the maze is continuously scrolling — the irregular wall surfaces create a dynamic, living quality.
- **Invert changes everything**: The visual character switches dramatically between normal and inverted modes. Try both for every composition — sometimes the "negative space" version is more compelling.
- **Wall Color for mood**: Dark walls (10-20%) create receding, shadowy corridors; bright walls (80-100%) create glowing grids; mid-gray walls (40-60%) create neutral architectural overlays.
- **Video walls for texture**: Switching Wall Luma to Video mode makes walls show a monochromatic ghost of the source — useful for maintaining image readability across both wall and corridor regions.
- **Combine with motion sources**: Feeding a moving video source while scrolling the maze in the opposite direction creates a compelling parallax effect where foreground maze and background video move independently.
- **Mix for subtlety**: At 30-50% mix, the maze becomes a semi-transparent grid overlay that adds texture without obscuring the source — effective for broadcast-style frame treatments.

---

## Glossary

| Term | Definition |
|------|------------|
| **Avalanche property** | A desirable hash function characteristic where a small change in input produces a large, unpredictable change in output, ensuring adjacent seeds generate unrelated mazes. |
| **Binary space partitioning** | A method of recursively subdividing a spatial region into two halves; used conceptually here to generate maze corridor structures from coordinate-based hash decisions. |
| **Chrominance** | The colour difference components of a video signal (U and V channels); discarded in Video wall mode to produce monochromatic wall rendering. |
| **Combinational logic** | Digital circuitry whose output depends solely on current inputs with no clock or stored state; the entire maze is computed combinationally per pixel. |
| **Figure-ground** | A perceptual relationship describing which region of an image reads as the foreground object versus the background space; the Invert toggle swaps this relationship. |
| **Hash function** | An algorithm that maps input coordinates to a deterministic but pseudo-random output value, used here to decide wall or corridor status for each pixel. |
| **Luma** | Short for luminance; the brightness component of a video signal, used in Video wall mode to render monochromatic wall surfaces. |
| **Parallax** | The visual effect of foreground and background elements appearing to move at different speeds, created when maze scroll direction opposes video motion. |
| **Procedural generation** | The algorithmic creation of content from mathematical rules rather than stored data; the maze is generated per-pixel from cascaded hash computations. |
| **Topology** | The spatial arrangement and connectivity of corridors and walls within the maze; each seed value produces a unique topology. |
| **XOR-rotate** | A fast integer mixing operation combining bitwise exclusive-OR with bit rotation, used in cascade to build the maze's deterministic hash function. |
| **YUV** | A colour model separating luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
