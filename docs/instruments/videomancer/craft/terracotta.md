---
draft: true
sidebar_position: 260
slug: /instruments/videomancer/terracotta
title: "Terracotta"
image: /img/instruments/videomancer/terracotta/terracotta_hero.png
description: "The Terracotta Army of Emperor Qin Shi Huang contains over eight thousand life-sized warriors, no two of them identical."
---

import terracotta_before_after from '/img/instruments/videomancer/terracotta/terracotta_before_after.png';
import terracotta_control_panel from '/img/instruments/videomancer/terracotta/terracotta_control_panel.png';
import terracotta_exercise1_result from '/img/instruments/videomancer/terracotta/terracotta_exercise1_result.png';
import terracotta_exercise2_result from '/img/instruments/videomancer/terracotta/terracotta_exercise2_result.png';
import terracotta_exercise3_result from '/img/instruments/videomancer/terracotta/terracotta_exercise3_result.png';
import terracotta_hero from '/img/instruments/videomancer/terracotta/terracotta_hero.png';
import terracotta_source1_kodim03 from '/img/instruments/videomancer/terracotta/terracotta_source1_kodim03.png';
import terracotta_source2_kodim13 from '/img/instruments/videomancer/terracotta/terracotta_source2_kodim13.png';
import terracotta_source3_kodim13_bw from '/img/instruments/videomancer/terracotta/terracotta_source3_kodim13_bw.png';

# Terracotta

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={terracotta_hero} alt="Terracotta hero image"/>
*Terracotta replicating a video frame into a grid of individually varied tiles, each bearing a unique luminance and hue signature derived from XOR hashing.*
<img src={terracotta_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Terracotta applied.*

---

## Overview

The Terracotta Army of Emperor Qin Shi Huang contains over eight thousand life-sized warriors, no two of them identical. Craftsmen working from a limited set of molds introduced subtle variations in expression, posture, and pigment that gave each figure an individual presence. Terracotta applies the same principle to video: it divides the frame into a grid of tiles, displays a copy of the source image inside each tile, and then applies per-tile variation so that every replica is slightly different.

The variation engine is deterministic. An XOR hash of the tile's column and row indices produces an 8-bit signature that drives luminance and hue offsets. Because the hash is purely combinational — no BRAM, no LFSR, no state — the variation pattern is locked to the grid geometry. Moving the Grid Size knob changes the number of tiles and simultaneously reshuffles all the variations. The result is a kaleidoscope of tinted, brightened, and darkened copies that reformulate with every grid change.

At conservative settings, Terracotta produces clean mosaic walls with faint tile-to-tile shading differences. At extreme settings, the luminance and hue offsets become dramatic, and the staggered brick layout, grid lines, and depth shading transform the frame into an architectural relief — a video wall made of terracotta bricks.

---

## Background

### Grid Replication and Modular Arithmetic

Terracotta's tiling engine uses integer division and modulo operations on the pixel coordinates to remap every pixel into a repeating grid. Given a frame of width $W$ and a grid of $N$ columns, each tile has a width of $W / N$. For any pixel at horizontal position $x$, the tile column is $\lfloor x \cdot N / W \rfloor$ and the position within the tile is $x \bmod (W / N)$. This modular coordinate remapping means the source image is effectively downsampled and replicated into each tile — a purely combinational operation that requires no framebuffer or BRAM.

### XOR Hashing for Deterministic Variation

Each tile receives a unique 8-bit hash computed as `tile_x XOR tile_y XOR (tile_x ROL 3)`. The XOR operation is the simplest nontrivial hash that produces a well-distributed pattern across a 2D grid. The rotate-left by 3 bits breaks the symmetry that would otherwise make tiles on the main diagonal identical. Because XOR is a bitwise operation, it costs only a handful of LUTs and completes in a single clock cycle.

### Staggered Brick Layouts

In traditional brickwork, alternating courses are offset by half a brick width. This "running bond" pattern breaks the monotony of a rectangular grid and strengthens the wall by staggering the vertical joints. Terracotta's Stagger toggle offsets every odd row by half a tile width, producing the same running bond pattern. The offset changes the XOR hash inputs, so staggering also reshuffles the per-tile variation — a single toggle simultaneously alters both geometry and color.

### Depth Shading in Relief Sculpture

Ancient terracotta reliefs and tile walls often exhibit a gradient in perceived brightness: tiles near the top of a wall catch more light, while tiles near the base fall into shadow. Terracotta's Depth Shade control simulates this effect by progressively darkening tiles as the row index increases. The attenuation is proportional to both the depth pot value and the tile's row position, creating a top-to-bottom gradient that can range from subtle to dramatic.

### Earth Tone Color Mapping

The Color toggle blends the source video toward a fixed earth-tone YUV value — a warm terracotta hue with slight orange shift. The blend is a 50/50 average between the original pixel and the earth constant, producing a desaturated, sepia-like appearance that evokes fired clay and ancient pigments. This operates before the per-tile variation stage, so the hash-based hue offsets still individuate each tile within the earth-tone palette.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Tile Coordinate Computation ───────────────────
│   ├─ Divide frame into N×N grid (integer division + modulo)
│   ├─ Compute tile_x, tile_y (tile index)
│   ├─ Compute in_tile_x, in_tile_y (position within tile)
│   └─ Apply stagger offset on odd rows (half tile width)
│
├── Stage 2: XOR Hash ──────────────────────────────────────
│   └─ hash = tile_x XOR tile_y XOR (tile_x ROL 3)
│
├── Stage 3: Per-Tile Variation ────────────────────────────
│   ├─ Earth color blend (optional — 50/50 with earth tone)
│   ├─ Luma offset = hash[3:0] × Luma Var pot
│   ├─ Hue offset = hash[7:4] × Hue Var pot (U ↑, V ↓)
│   ├─ Invert (optional bitwise complement of Y)
│   └─ Clamp all channels [0, 1023]
│
├── Stage 4: Grid Lines + Depth Shading ────────────────────
│   ├─ Grid line detect (pixel at tile edge < grid_width)
│   ├─ Crop detect (pixel in tile margin > crop_margin)
│   ├─ Grid → dark neutral color (Y=180, U=500, V=520)
│   ├─ Crop → black (Y=80, U=512, V=512)
│   └─ Depth shade: Y -= depth_pot × tile_row / 64
│
├── Mix (interpolator_u × 3) ──────────────────────────────
│   └─ Wet/dry crossfade: lerp(dry, wet, mix_amount)
│
└── Bypass Mux ─────────────────────────────────────────────
    └─ Select original or processed signal
```

The key architectural feature is that Terracotta uses zero BRAM. The entire tiling operation is combinational: modular coordinate remapping replaces framebuffer-based scaling. The XOR hash, variation offsets, and grid line detection all complete in four clock cycles before the 4-cycle interpolator mix stage. The earth color blend and per-tile variation occur at stage 3, after the hash is computed but before grid line rendering, so grid lines always appear in a fixed neutral color regardless of the variation settings.

---

## Parameter Reference

<img src={terracotta_control_panel} alt="Videomancer front panel with Terracotta loaded"/>
*Videomancer's front panel with Terracotta active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Grid Size
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 3 |

Controls the number of tile columns across the frame. The steps_8 decode maps the pot to column counts from 2 (at minimum) to 10 (at maximum). Because tiles are square, increasing the column count also increases the row count proportionally. At 2 columns, each tile is 960 pixels wide — nearly half the frame. At 10 columns, each tile is 192 pixels wide and highly pixelated. Because the XOR hash uses the tile coordinates as input, changing the grid size reshuffles all per-tile variations simultaneously.

---

#### Knob 2 — Tile Crop
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets the crop margin within each tile. At 0%, the entire tile area displays the replicated source. As you increase Tile Crop, the outer edges of each tile are replaced with a dark fill, creating a visible gap between the source content and the grid lines. This gives the tiles a recessed, inset appearance — like ceramic tiles set behind a frame. The crop margin is applied symmetrically on all four sides of each tile.

---

#### Knob 3 — Luma Var
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the strength of per-tile luminance variation. The lower 4 bits of the XOR hash generate a signed offset in the range ±32 counts. This pot scales that offset — at 0%, all tiles have identical brightness; at 100%, bright tiles can be nearly 6% brighter and dark tiles 6% darker than the source. The effect is subtle at low settings, creating a gentle shimmer across the grid, and becomes dramatically architectural at higher values.

---

#### Knob 4 — Hue Var
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Controls the strength of per-tile hue variation. The upper 4 bits of the XOR hash generate a signed offset applied in opposite directions to U and V channels, producing a hue rotation. At 0%, all tiles share the same color. As you increase Hue Var, each tile shifts toward a slightly different hue — some warmer, some cooler. Combined with Luma Var, this creates the individuality effect: each tile becomes a unique tonal interpretation of the same source.

---

#### Knob 5 — Grid Lines
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the width of the grid lines rendered at tile boundaries. At 0%, no grid lines appear and tiles merge seamlessly. As you increase Grid Lines, visible dark bars (Y=180, neutral chroma) appear at the edges of each tile, defining the grid structure. The grid line width is derived from the upper bits of the pot value, giving a range from 0 to approximately 16 pixels. Grid lines render on top of the tile content, so they always appear regardless of variation or crop settings.

---

#### Knob 6 — Depth Shade
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the depth shading gradient applied across tile rows. At 0%, all rows are equally bright. As you increase Depth Shade, tiles in lower rows become progressively darker, simulating the top-lit appearance of a physical tile wall. The attenuation is computed as `depth_pot × tile_row_index / 64`, so the bottom tiles of a 10-row grid receive significantly more darkening than the bottom tiles of a 3-row grid. This interacts with luma variation: individual tile brightness offsets combine with the row-based gradient.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Stagger** | Aligned | Staggered |
| **8 — Style** | Clean | Aged |
| **9 — Color** | Full | Mono |
| **10 — Invert** | Dark BG | Light BG |
| **11 — Bypass** | Off | On |

The five toggles each enable an independent processing mode. Stagger and Style interact most strongly — Stagger changes the grid geometry, which changes the XOR hash inputs, which changes the variation pattern, so enabling Stagger reshuffles the per-tile colors. Color operates independently before the variation stage. Invert is a simple luminance complement applied after variation but before grid lines.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the dry (original) signal and the wet (tiled) signal using three parallel interpolator instances. At 0%, the output is entirely dry — identical to the source. At 100%, the output is the fully processed tiled image. Intermediate values blend the two, creating a ghost-overlay effect where the grid structure fades in over the source. This is applied after all processing stages, so the grid lines and variation are included in the wet signal.

---

## Guided Exercises

These exercises explore Terracotta's grid replication from simple tiling to complex architectural compositions. Each builds on the previous, introducing variation, color, and depth controls progressively.

### Exercise 1: Basic Grid Tiling

<img src={terracotta_exercise1_result} alt="Basic Grid Tiling result"/>
*Basic Grid Tiling — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and good contrast.

**Objective**: Learn how the grid size control works and how stagger alters the tile geometry.

1. **Start simple**: Set Grid Size to its minimum (2 columns). The frame splits into two large square tiles, each showing a compressed copy of the full source.
2. **Increase grid**: Slowly increase Grid Size through the 8 steps. Watch the frame subdivide into progressively finer grids. At 10 columns, the tiles are small and highly pixelated.
3. **Add grid lines**: Increase Grid Lines to about 50%. Visible dark lines appear at tile boundaries, defining the grid structure.
4. **Stagger**: Toggle Stagger to On. Watch the odd rows shift by half a tile width, and notice how the overall pattern changes character from a regular grid to a brick wall.
5. **Tile crop**: Increase Tile Crop to about 30%. The edges of each tile darken, creating an inset appearance with visible gaps between content and grid lines.

**Key concepts**: Modular coordinate remapping creates tile copies without a framebuffer, grid size simultaneously changes tile count and tile resolution, stagger offset reshuffles hash inputs

---

### Exercise 2: Terracotta Variation

<img src={terracotta_exercise2_result} alt="Terracotta Variation result"/>
*Terracotta Variation — simulated result across source images.*
**Source**: Footage with varied tonal content — faces, landscapes, or architectural subjects.

**Objective**: Explore the per-tile variation engine and earth tone color mode.

1. **Enable variation**: Set Style to Aged. Slowly increase Luma Var from 0 to about 50%. Watch individual tiles brighten and darken relative to their neighbors.
2. **Add hue variation**: Increase Hue Var to about 50%. Each tile shifts toward a slightly different hue — some warmer, some cooler.
3. **Earth color**: Toggle Color to Mono. The entire image shifts toward a warm terracotta palette. The hue variations now create subtle tonal differences within the earth-tone family.
4. **Depth shading**: Increase Depth Shade to about 40%. The bottom rows darken, creating a top-lit relief effect.
5. **Compare**: Toggle Style between Clean and Aged to see the before/after difference in tile individuality.

**Key concepts**: XOR hash produces deterministic per-tile signatures, variation is scaled by pot values, earth color blends before variation so offsets still differentiate tiles

---

### Exercise 3: Architectural Relief

<img src={terracotta_exercise3_result} alt="Architectural Relief result"/>
*Architectural Relief — simulated result across source images.*
**Source**: A static camera shot or slow-moving footage — architectural details, textures, or still life.

**Objective**: Combine all controls to create a dramatic tile wall with full depth and variation.

1. **Set grid**: Grid Size at about 6 columns. Enable Stagger for a brick layout.
2. **Maximum variation**: Set both Luma Var and Hue Var to about 80%.
3. **Earth tones**: Set Color to Mono for the terracotta palette.
4. **Grid and crop**: Grid Lines at about 60%, Tile Crop at about 20%.
5. **Deep relief**: Increase Depth Shade to about 70%. The bottom rows become dramatically dark.
6. **Invert**: Toggle Invert to Light BG. The entire relief inverts, creating a light-ground version.
7. **Half mix**: Lower Mix to about 50%. The tiled relief overlays ghostly on the original source, creating a double-exposure architectural effect.

**Key concepts**: All processing stages combine to create a composite effect, depth shading simulates physical top-lighting, mix crossfade enables overlay compositions

---


## Tips

- **Grid Size is the master control**: Changing the grid count reshuffles all per-tile variations, changes tile resolution, and redefines grid line positions — it is the single most impactful parameter.
- **Style must be Aged for variation**: The Clean/Aged toggle is the master enable for the XOR hash variation engine. Leave it on Clean for uniform tiling grids, switch to Aged for individuated terracotta tiles.
- **Earth color works best with variation**: The Mono (Earth) color mode creates a unified warm palette that makes per-tile hue and luma offsets read as natural clay pigment differences.
- **Stagger changes everything**: The brick offset doesn't just shift rows — it changes the XOR hash inputs, so enabling Stagger reshuffles the entire variation pattern.
- **Depth Shade simulates lighting**: Use moderate depth values (20–40%) to create a subtle top-lit relief effect. High values can push bottom tiles to near-black.
- **Feedback routing**: Send the output back to the input for recursive tiling — tiles within tiles within tiles. The variation compounds with each recursion level.
- **Use Tile Crop for inset frames**: Even small crop margins (10–20%) significantly change the character of the grid, creating recessed tile appearances.
- **Mix for overlay compositing**: At intermediate Mix values, the tiled grid overlays ghostly on the source, creating double-exposure architectural textures.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **Combinational** | Logic that produces output purely from current inputs, without memory elements or clock-dependent state. |
| **Earth Tone** | A warm, desaturated YUV color (Y=560, U=460, V=580) resembling fired clay. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Grid Line** | A rendered dark bar at tile boundaries with fixed color (Y=180, U=500, V=520). |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **LUT** | Look-Up Table; the basic logic element of an FPGA, used here for division, modulo, and XOR. |
| **Modular Arithmetic** | Division and modulo operations that remap pixel coordinates into repeating tile coordinates. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **Running Bond** | A brick laying pattern where alternating courses are offset by half a brick width. |
| **Stagger** | Horizontal offset of odd rows by half a tile width, producing a brick layout. |
| **XOR Hash** | A bitwise exclusive-OR function used to generate deterministic per-tile variation signatures. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
