---
draft: true
sidebar_position: 313
slug: /instruments/videomancer/truchet
title: "Truchet"
image: /img/instruments/videomancer/truchet/truchet_hero.png
description: "In 1704, the Dominican priest Sébastien Truchet noticed something remarkable about square tiles decorated with a simple diagonal line: when placed on a grid with random orientations, the lines connect across tile boundaries to form intricate, maze-like patterns that appear far more complex than the individual tiles that compose them."
---

import truchet_hero from '/img/instruments/videomancer/truchet/truchet_hero.png';
import truchet_animation from '/img/instruments/videomancer/truchet/truchet_animation.gif';
import truchet_control_panel from '/img/instruments/videomancer/truchet/truchet_control_panel.png';
import truchet_exercise1_result from '/img/instruments/videomancer/truchet/truchet_exercise1_result.gif';
import truchet_exercise2_result from '/img/instruments/videomancer/truchet/truchet_exercise2_result.gif';
import truchet_exercise3_result from '/img/instruments/videomancer/truchet/truchet_exercise3_result.gif';

# Truchet

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={truchet_hero} alt="Truchet hero image"/>
*Truchet tile mosaic with quarter-circle arcs forming emergent meandering curves across a grid of LFSR-oriented tiles.*
<img src={truchet_animation} alt="Truchet animated output"/>
*Truchet output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1704, the Dominican priest Sébastien Truchet noticed something remarkable about square tiles decorated with a simple diagonal line: when placed on a grid with random orientations, the lines connect across tile boundaries to form intricate, maze-like patterns that appear far more complex than the individual tiles that compose them. Truchet implements this principle in real-time video hardware, dividing the screen into a configurable grid of square tiles and assigning each tile a pseudo-random orientation via a 16-bit LFSR.

The default mode draws quarter-circle arcs from opposite corners of each tile. When adjacent tiles have complementary orientations, the arcs connect seamlessly, creating sinuous, meandering curves that weave across the display. The LFSR-based orientation assignment produces a spatially coherent pseudo-random field — deterministic per frame, but controllable via the Seed parameter. Four tile types are available: classic quarter-circle arcs, straight diagonals, corner triangles, and a Smith-style 2×2 checkerboard partitioning. Each creates a distinctly different visual texture from the same underlying grid.

At small tile sizes, the pattern appears as a dense, organic texture. At large tile sizes, individual tiles and their connecting structures become clearly visible. The Fill Mode toggle switches between outline rendering (arcs/lines only) and filled region rendering, producing dramatically different visual weight. An animation system cycles the LFSR seed over time, causing the tile orientations to shift frame by frame — the maze continuously reshuffles.

---

## Quick Start

1. **Seed is your creative palette**: Each seed value produces a completely unique global pattern. Spend time exploring — some seeds produce mesmerizing connected loops, others produce fragmented islands.
2. **Small tiles for texture, large tiles for structure**: At 8 pixels, the pattern looks like a woven fabric. At 64 pixels, you can trace individual arcs and their connections. Choose the scale that matches your compositional intent.
3. **Fill mode is a dramatic toggle**: Switching from outline to filled rendering changes the pattern from delicate linework to bold graphic blocks. Use fill for high-impact visual compositions.

---

## Background

### Truchet Tiles and Combinatorial Geometry

Sébastien Truchet's original observation concerned square tiles split diagonally into two colored triangles. With just two possible orientations per tile, an N×N grid has 2^(N²) possible configurations — an enormous combinatorial space explored by a single parameter (the orientation). Cyril Stanley Smith expanded on this in 1987, cataloguing all possible two-coloring patterns of a square halved by arcs or lines. Videomancer's four tile types correspond to subsets of Smith's classification: arc (quarter-circle), diagonal (straight line), triangle (corner region), and Smith (2×2 checkerboard sub-partitioning).

### Octagonal Distance Approximation

True quarter-circle arcs require computing Euclidean distance (√(x² + y²)), which involves multiplication and square root — expensive operations on an FPGA without dedicated DSP multipliers. Truchet uses the **octagonal approximation**: dist ≈ max(|dx|, |dy|) + 3/8 × min(|dx|, |dy|). This produces an octagon-shaped isodistance contour rather than a circle, but is close enough for visual purposes — the maximum error is about 4%. The approximation requires only comparisons, shifts, and additions, fitting comfortably in FPGA LUT fabric.

### LFSR-Based Pseudo-Random Fields

A 16-bit linear feedback shift register generates the pseudo-random bit stream that assigns tile orientations. The LFSR is re-seeded at the start of each tile row (from a row counter plus the Seed parameter) and advanced once at each tile column boundary. This produces a 2D pseudo-random field that is spatially coherent (neighboring tiles have independent but deterministic orientations) and temporally stable (same seed produces same pattern). The animation system increments the seed phase each frame, causing the entire field to evolve.

### Emergent Connectivity

The deepest visual property of Truchet tilings is **emergent connectivity**: local tile orientations create global structures. In the arc mode, connected arcs form closed loops and meandering paths that can span the entire display. These structures are not designed — they emerge from the random orientation assignment. At certain tile sizes and seed values, the pattern self-organizes into recognizable forms: rivers, islands, labyrinths. This is a powerful demonstration of how simple local rules can generate complex global behavior.

### Four Tile Types

The four selectable tile types produce distinct visual textures: **Arc** draws quarter-circle arcs connecting adjacent tile edges, creating smooth, organic curves. **Diagonal** draws straight lines from corner to corner, producing angular, crystalline patterns. **Triangle** fills corner regions, creating a fragmented mosaic. **Smith** partitions each tile into four quadrants, producing a blocky checkerboard texture that references Cyril Stanley Smith's generalized Truchet classifications.


---

## Signal Flow

Generated Pattern → Mix Stage → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Generated Pattern ──────────────────────────────────────
│   │
│   ├─ 1. Pixel Counters        h_count, v_count from timing generator
│   ├─ 2. Animation Phase       DDS accumulator incremented per vsync
│   │
│   ├─ 3. Tile Position         local_x = h_count mod tile_size
│   │                           local_y = v_count mod tile_size
│   │                           LFSR re-seeded per row, advanced per column
│   │
│   ├─ 4. Tile Orientation      s_orientation = LFSR bit 0 (per tile)
│   │
│   ├─ 5. Distance Compute      octagonal approx from 4 tile corners:
│   │                           dist ≈ max + min/4 + min/8
│   │
│   ├─ 6. Pattern Test          Select by tile type:
│   │      Arc:  |dist_corner - half_tile| < line_width → on_arc
│   │      Diag: |lx - ly| or |lx + ly - size| < line_width
│   │      Tri:  corner quadrant test
│   │      Smith: 2×2 checkerboard XOR
│   │
│   ├─ 7. Fill + Invert         fill_mode: outline only or filled regions
│   │                           invert: flip on/off
│   │
│   ├─ 8. Contrast Scale        gen_y × contrast → comp_y
│   │
│   └─ 9. Colorization          orientation → UV tint via color_amt
│
├── Mix Stage ──────────────────────────────────────────────
│   └─ Interpolator: dry (input YUV) ↔ wet (generated YUV)
│
├── Sync Signals ───────────────────────────────────────────
│   └─ Pass-through with 8-clock delay
│
└── Bypass ─────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pattern is generated entirely from pixel position and LFSR state — the input video is only used for the dry path of the mix interpolator (and is ignored unless Mix < 100%). The octagonal distance approximation (max + min/4 + min/8) is computed for all four tile corners simultaneously in Stage 5, but only two corners are used per tile based on the orientation bit from Stage 4. The line width threshold maps the 10-bit pot value to a 1–16 pixel range via `line_width(9 downto 6) + 1`. Colorization in Stage 9 applies complementary UV shifts based on tile orientation — orientation 0 gets one tint, orientation 1 gets the opposite — creating a two-tone color effect controlled by the Color Amount parameter.

---

## Parameter Reference

<img src={truchet_control_panel} alt="Videomancer front panel with Truchet loaded"/>
*Videomancer's front panel with Truchet active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 4 – 64 |
| Default | 27 |

Selects the tile dimension from 8 discrete sizes: 8, 12, 16, 20, 24, 32, 48, or 64 pixels. Small tiles create dense, fine-grained patterns where individual arcs are barely visible and the overall texture dominates. Large tiles make each tile's arc structure clearly legible, with obvious connections between adjacent tiles forming large-scale curves. The choice of tile size fundamentally changes the character of the pattern — from organic texture to architectural grid.

---

#### Knob 2 — Line Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the thickness of the rendered arcs, diagonals, or grid lines. The line width maps to 1–16 pixels via a right-shift of the register value. Thin lines produce delicate, wireframe-like patterns. Thick lines create bold strokes that begin to fill the tile area even without Fill Mode active. At maximum width with small tile sizes, the arcs overlap and merge, producing a textured mass rather than distinct curves.

---

#### Knob 3 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the output luminance. The generated pattern is binary (full white or black before contrast), and this control multiplies the white level: `result = gen_y × contrast / 1024`. At 50%, the bright regions output at half brightness. At 100%, full white. This is particularly useful when mixing the Truchet pattern with input video — reducing contrast prevents the pattern from overwhelming the source.

---

#### Knob 4 — Anim Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the speed of animation when the Animate toggle is active. The animation system uses a DDS (direct digital synthesis) phase accumulator that increments by the speed value at each vertical sync. This phase offset is added to the LFSR seed, causing tile orientations to change over time. At low speeds, the pattern shifts slowly — individual tiles flip orientation one by one. At high speeds, the entire grid reshuffles rapidly, creating a boiling, chaotic texture.

---

#### Knob 5 — Color Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

At 0%, the output is monochrome (U=512, V=512). As the value increases, tiles with orientation 0 receive a warm tint (U shifted up, V shifted down) and tiles with orientation 1 receive a cool tint (U shifted down, V shifted up). This creates a two-tone color map that visually distinguishes the two orientation populations and their emergent connected structures. Internally, controls the amount of chrominance colorization applied to the pattern.

---

#### Knob 6 — Seed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the base LFSR seed offset. Different seed values produce completely different tile orientation patterns — the same grid structure but with different random assignments. This is the primary way to explore the combinatorial space of Truchet tilings without changing any other parameter. Small changes in seed can produce dramatically different global structures (connected loops, isolated islands, rivers).

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Tile Type** | Arc | Smith |
| **8 — Fill Mode** | Lines | Filled |
| **9 — Invert** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control the tile rendering mode (4 types via 2-bit selector), fill/outline mode, luminance inversion, animation enable, and bypass. Tile Type uses two bits of the toggle register, selecting among Arc, Diagonal, Triangle, and Smith patterns. Fill Mode and Invert are independent binary options. Animate enables the DDS seed cycling. Bypass passes input video through unprocessed.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original input video and the generated Truchet pattern. At 100%, the output is fully the generated pattern. At 0%, the input video passes through. Intermediate values blend the pattern over the source, creating a textured overlay effect — the Truchet grid modulates the underlying video.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Truchet processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises progress from basic tile exploration to animated, colorized pattern compositions using all four tile types.

### Exercise 1: Classic Truchet Arcs

<img src={truchet_exercise1_result} alt="Classic Truchet Arcs result"/>
*Classic Truchet Arcs — simulated result across source images.*
**What You'll Create**: Explore how tile size, line width, and seed interact to create emergent arc structures.

1. **Set Arc mode**: Ensure Tile Type is set to Arc. Set Fill Mode to Lines.
2. **Medium tiles**: Set Cell Size to position 3 (16 pixels). Observe the quarter-circle arcs connecting across tile boundaries.
3. **Sweep seed**: Slowly turn the Seed knob. Watch how different seeds produce completely different global patterns — loops, rivers, isolated islands.
4. **Vary tile size**: Step through all 8 tile sizes. Notice how small tiles create dense organic textures while large tiles reveal individual arc geometry.
5. **Line width**: Increase Line Width to about 60%. The arcs thicken, beginning to overlap at small tile sizes.
6. **Fill mode**: Toggle Fill Mode to Filled. The regions between arcs fill in, dramatically changing the pattern's visual weight.

**Key concepts**: Tile orientation is pseudo-random via LFSR, emergent connectivity arises from local random choices, tile size controls spatial frequency, line width controls stroke weight

---

### Exercise 2: Animated Diagonal Grid

<img src={truchet_exercise2_result} alt="Animated Diagonal Grid result"/>
*Animated Diagonal Grid — simulated result across source images.*
**What You'll Create**: Use animation and diagonal tiles to create a dynamic crystalline texture overlay.

1. **Switch to Diagonal**: Set Tile Type to Diag. The arcs become straight lines connecting opposite corners.
2. **Enable animation**: Toggle Animate to On. Set Anim Speed to about 30%.
3. **Watch evolution**: The diagonal pattern shifts and reshuffles continuously, creating a kaleidoscopic effect.
4. **Add color**: Increase Color Amt to about 50%. The two tile orientations separate into warm and cool tints.
5. **Overlay on video**: Reduce Mix to about 40%. The diagonal grid overlays the input video as a textured screen.
6. **Try other types**: Cycle through Tri and Smith tiles with animation active. Each produces a distinct animated texture.

**Key concepts**: Animation cycles the LFSR seed via DDS, diagonal tiles create angular structures, colorization separates orientation populations, mix controls overlay opacity

---

### Exercise 3: Filled Smith Mosaic

<img src={truchet_exercise3_result} alt="Filled Smith Mosaic result"/>
*Filled Smith Mosaic — simulated result across source images.*
**What You'll Create**: Create a bold, graphic mosaic using filled Smith tiles with inversion and contrast control.

1. **Smith mode**: Set Tile Type to Smith. Set Fill Mode to Filled.
2. **Large tiles**: Set Cell Size to position 6 (48 pixels) for clearly visible partitioned blocks.
3. **Full contrast**: Set Contrast to about 90% for maximum graphic impact.
4. **Add color**: Set Color Amt to about 70% for strong two-tone coloring.
5. **Invert**: Toggle Invert on. The pattern flips — filled regions become cutouts.
6. **Animate slowly**: Enable Animate at about 15% speed. The checkerboard blocks slowly reshuffle.
7. **Mix with source**: Set Mix to about 60%. The bold mosaic overlays the source with graphic authority.

**Key concepts**: Smith tiles create 2×2 sub-partitioning, filled mode maximizes visual weight, inversion creates complementary patterns, large tiles produce bold graphic blocks

---


## Tips

- **Animation creates organic movement**: Even low animation speeds produce a slowly shifting, breathing pattern. High speeds create frenetic visual noise — useful as a modulation source.
- **Color separates orientation populations**: When colorization is applied, the two-tone tinting makes the emergent connectivity structures visually obvious. Connected arcs share the same color, revealing the large-scale topology.
- **Mix for pattern overlay**: At 30–50% mix, the Truchet grid serves as a textured screen over live video — a geometric veil that adds structure without obscuring the source.
- **Combine tile types with animation**: Each tile type produces a distinct animation character. Arcs morph smoothly; diagonals snap between orientations; Smith blocks shuffle like cards.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDS** | Direct Digital Synthesis; a technique using a phase accumulator to generate periodic waveforms, used here to cycle the animation seed. |
| **Emergent Connectivity** | Global structures (loops, paths, mazes) that arise from local random tile orientations connecting across boundaries. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used to assign tile orientations. |
| **LUT** | Look-Up Table; the basic logic element of the FPGA fabric, used for combinational logic. |
| **Octagonal Approximation** | A computationally cheap distance estimate: max(|dx|, |dy|) + 3/8 × min(|dx|, |dy|), producing an octagon instead of a circle. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage for contrast and brightness adjustment. |
| **Truchet Tiling** | A tiling pattern where identical square tiles with asymmetric decoration are placed in random orientations to create emergent global patterns. |

---
