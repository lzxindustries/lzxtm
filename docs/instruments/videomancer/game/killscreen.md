---
draft: true
sidebar_position: 138
slug: /instruments/videomancer/killscreen
title: "Killscreen"
image: /img/instruments/videomancer/killscreen/killscreen_hero.png
---

import killscreen_before_after from '/img/instruments/videomancer/killscreen/killscreen_before_after.png';
import killscreen_control_panel from '/img/instruments/videomancer/killscreen/killscreen_control_panel.png';
import killscreen_exercise1_result from '/img/instruments/videomancer/killscreen/killscreen_exercise1_result.png';
import killscreen_exercise2_result from '/img/instruments/videomancer/killscreen/killscreen_exercise2_result.png';
import killscreen_exercise3_result from '/img/instruments/videomancer/killscreen/killscreen_exercise3_result.png';
import killscreen_hero from '/img/instruments/videomancer/killscreen/killscreen_hero.png';
import killscreen_source1_kodim15 from '/img/instruments/videomancer/killscreen/killscreen_source1_kodim15.png';
import killscreen_source2_kodim03 from '/img/instruments/videomancer/killscreen/killscreen_source2_kodim03.png';
import killscreen_source3_kodim15_bw from '/img/instruments/videomancer/killscreen/killscreen_source3_kodim15_bw.png';

# Killscreen

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={killscreen_hero} alt="Killscreen hero image"/>
*Killscreen corrupting a video feed into tile-mapped glitch patterns inspired by the Pac-Man level 256 overflow bug.*
<img src={killscreen_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Killscreen applied.*

---

## Overview

On September 21, 1982, Billy Mitchell became the first person to reach screen 256 of Pac-Man — and discovered that the game's level counter overflowed its 8-bit storage. The right half of the maze dissolved into a chaos of misplaced tiles, scrambled sprites, and random symbols. That broken screen became one of the most famous glitches in video game history. Killscreen recreates this phenomenon as a deliberate artistic effect.

The program divides the input video into a configurable grid of rectangular tiles and selectively corrupts them. A position-seeded hash function derived from a master LFSR determines which tiles are corrupted and how. Corruption spreads progressively across the screen from one side to the other, controlled by the Corrupt Amt knob — just as the Pac-Man kill screen's corruption spread from the right side of the maze. Six corruption modes simulate different kinds of tile map failure: clean passthrough, address offset (reading from the wrong tile), palette/channel swap, horizontal bit shift, luminance inversion, and solid color fill.

The result ranges from subtle glitch accents — a few corrupted tiles scattered across an otherwise clean image — to total visual breakdown where the entire frame is a mosaic of mangled tile data. The corruption pattern changes over time as the master LFSR evolves, so the glitch is alive rather than static.

---

## Background

### The Pac-Man Kill Screen

In the original Pac-Man arcade hardware (Namco, 1980), a single unsigned 8-bit byte stores the current level number. When the player clears level 255, the counter wraps to 0, but the fruit-drawing subroutine interprets it as level 256 and attempts to draw 256 fruit symbols on the bottom of the screen. The code overflows its allocated screen memory, writing tile data into adjacent RAM. The right half of the maze — from column 16 onward — is overwritten with garbage data: random tile indices, partial sprite data, and color palette entries pulled from unrelated memory locations. The left half remains playable but the right half is an impassable wall of visual noise. This accidental corruption pattern — progressive left-to-right decay — is exactly what Killscreen's threshold system replicates.

### LFSR-Based Pseudo-Random Hashing

Killscreen uses a 16-bit Galois Linear Feedback Shift Register as its randomness source. The LFSR evolves once per frame (at a rate controlled by the Speed knob), producing a different master state each frame. For each tile, the master LFSR value is XORed with the tile's (x, y) coordinates to produce a per-tile hash. This hash determines both whether the tile is corrupted and which corruption mode is applied. The XOR-based hashing ensures that adjacent tiles get different corruption states even though they share the same master LFSR, creating the characteristic patchwork pattern of a corrupted tile map.

### Tile Map Architecture

Classic 2D game hardware divides the screen into a grid of fixed-size tiles — typically 8×8 pixels each. A tile map in memory stores an index for each grid position, pointing to a tile pattern in a character ROM. The visual appearance of the screen is determined not by individual pixels but by which tile pattern is placed at each grid position. When the tile map is corrupted — wrong indices, out-of-range lookups, or overwritten data — the visual result is a patchwork of misplaced patterns, not random pixel noise. Killscreen simulates this by applying different corruption modes per tile rather than per pixel.

### Corruption Modes as Memory Faults

Each of Killscreen's six corruption modes corresponds to a different kind of memory or addressing fault:
- **Passthrough** (mode 0): The tile data is read correctly — some tiles survive even in corrupted regions.
- **Address offset** (mode 1): The tile reads data from the wrong address — shifted one pixel position, simulating an off-by-one pointer error.
- **Palette swap** (mode 2): The color channels are remapped, simulating a corrupted palette table lookup.
- **Bit shift** (mode 3): The luminance data is bit-shifted, simulating a data bus misalignment.
- **Inversion** (mode 4): Luminance is inverted, simulating a stuck address line that flips the MSB.
- **Solid fill** (mode 5): The tile is replaced entirely, simulating a read from zeroed or constant memory.

### Grid Lines and Tile Boundaries

Killscreen can overlay visible grid lines at tile boundaries. In real arcade hardware, tile boundaries are invisible — they are an addressing abstraction, not a visual element. But making them visible in Killscreen serves two purposes: it reveals the underlying grid structure of the corruption pattern, and it creates an additional graphical element (a grid overlay) that can be used compositionally. The grid line brightness is controllable, from invisible to prominent.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y / U / V Channels ────────────────────────────────────────
│   │
│   ├─ 1. Input Register        (latch incoming pixel)
│   ├─ 2. Tile Coordinate Calc  (divide pixel position by tile size)
│   ├─ 3. LFSR Hash             (XOR master LFSR with tile coords)
│   ├─ 4. Threshold Test        (compare tile_x against corruption threshold)
│   ├─ 5. Mode Selection        (hash bits → corruption mode + param)
│   ├─ 6. Corruption Apply      (6 modes: pass/offset/swap/shift/invert/fill)
│   ├─ 7. Grid Line Overlay     (dim pixel + add border brightness)
│   └─ 8. Interpolator Mix      (4 clk: dry/wet crossfade)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline (matched to processing latency)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The corruption decision is made per tile, not per pixel. The LFSR hash is computed from the tile coordinates (derived by right-shifting the pixel counters), so every pixel within the same tile receives the same corruption treatment. The threshold test compares the tile's X coordinate against a corruption boundary derived from the Corrupt Amt knob: tiles beyond the boundary are candidates for corruption. The Direction toggle reverses whether corruption spreads left-to-right or right-to-left.

One notable hardware detail: the Tile Size toggle and Mode Bias toggle share bit 1 of the toggle register. This means that changing Tile Size can also affect Mode Bias, and vice versa. In practice, the "24×24" tile size option always has Pac-Man bias enabled, and the "8×8" and "32×32" options always have it disabled.

---

## Parameter Reference

<img src={killscreen_control_panel} alt="Videomancer front panel with Killscreen loaded"/>
*Videomancer's front panel with Killscreen active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Corrupt Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the corruption threshold — how far across the screen the corruption extends. At 0% no tiles are corrupted. As you increase the value, corruption spreads progressively from one side of the screen to the other (direction depends on the Direction toggle). At 100% the entire screen is within the corruption zone. Tiles within the corruption zone are not all corrupted — the hash function determines which specific tiles are affected — but the probability increases with the threshold.

---

#### Knob 2 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the rate at which the master LFSR evolves. At 0% the LFSR changes very slowly — the corruption pattern is nearly static, changing only once every many frames. At higher values the LFSR cycles faster, causing the corruption pattern to shift and shimmer rapidly. The LFSR advances once per frame at a rate modulated by this control, so the speed is tied to the video frame rate.

---

#### Knob 3 — Offset Range
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Labeled "Offset Range" on the panel. This register is read from the SPI bus but is not referenced anywhere in the processing pipeline. Turning this knob has no effect on the output. It is a vestigial parameter left from an earlier revision of the program.

---

#### Knob 4 — Color Intns
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Labeled "Color Intns" on the panel. Like Offset Range, this register is read but never used in the processing logic. It has no effect on the output. A future firmware revision could connect these unused registers to new corruption behaviors.

---

#### Knob 5 — Border Brt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the brightness of the tile grid lines when Grid Lines is enabled. At 0% the grid lines are invisible (the overlay has no additive brightness). At higher values the grid lines become progressively brighter. The grid line rendering dims the underlying pixel by half and adds the border brightness, so even at maximum the incoming image content remains partially visible through the grid.

---

#### Knob 6 — Fill Color
| Property | Value |
|----------|-------|
| Range | 0.0d – 360.0d |
| Default | 0.0d |
| Suffix | d |

Controls the hue of solid-fill corrupted tiles (mode 5). The fill color is derived from this pot value as a simple chroma offset from neutral gray. Low values produce cool-tinted fills; high values produce warm-tinted fills. The mid-point produces neutral gray. Only tiles that land on corruption mode 5 (solid fill) are affected — this control has no effect on the other five corruption modes.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Tile Size** | 8x8 | 16x16 |
| **8 — Mode Bias** | All Equal | Pac-Man |
| **9 — Direction** | L-to-R | R-to-L |
| **10 — Grid Lines** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the tile grid geometry, corruption behavior, and display options. Tile Size and Mode Bias share physical encoding in the toggle register — see the note about the bit overlap. Direction controls the corruption spread order, Grid Lines enables the tile boundary overlay, and Bypass routes the signal around all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet crossfade between the original input and the corrupted output. At 0% the output is entirely clean (original). At 100% the output is entirely corrupted. Intermediate values blend the two, which can create a ghostly effect where corruption patterns are overlaid semi-transparently on the clean image. This is especially effective with the grid lines enabled — the grid appears as a subtle overlay even at low mix values.

---

## Guided Exercises

These exercises progress from gentle glitch accents to full kill-screen breakdown, gradually engaging more corruption modes and controls.

### Exercise 1: Split-Screen Corruption

<img src={killscreen_exercise1_result} alt="Split-Screen Corruption result"/>
*Split-Screen Corruption — simulated result across source images.*
**Source**: A camera feed or recorded footage with recognizable subjects and saturated color.

**Objective**: Learn how Corrupt Amt and Direction create a progressive split-screen corruption effect.

1. **Minimal corruption**: Set Corrupt Amt to about 20%. Only a few columns of tiles near the edge of the screen are corrupted.
2. **Spread**: Slowly increase Corrupt Amt toward 50%. Watch the corruption front advance across the screen, tile column by tile column.
3. **Full corruption**: Push to 100%. The entire screen is within the corruption zone — about half the tiles are visually corrupted (the others land on passthrough mode).
4. **Reverse direction**: Toggle Direction. The corruption front moves to the opposite side.
5. **Enable grid**: Toggle Grid Lines On and set Border Brt to about 50%. The tile grid becomes visible, revealing the underlying structure of the corruption map.

**Key concepts**: Corruption spreads column-by-column via threshold comparison, direction toggle reverses the spread, tile hash means not every tile in the corruption zone is affected

---

### Exercise 2: Pac-Man Mode

<img src={killscreen_exercise2_result} alt="Pac-Man Mode result"/>
*Pac-Man Mode — simulated result across source images.*
**Source**: Footage with geometric patterns or text — anything where tile displacement is clearly visible.

**Objective**: Experience the Pac-Man kill screen's characteristic address-offset corruption pattern.

1. **Set tile size**: Choose 16×16 tiles for a classic arcade feel.
2. **Enable Pac-Man bias**: Toggle Mode Bias to Pac-Man. This heavily favors the address-offset corruption mode.
3. **Set corruption**: Corrupt Amt to about 60%. The right portion of the screen shows predominantly shifted tiles — the image appears to be reading from slightly wrong positions, just like the Pac-Man kill screen.
4. **Fill color**: Set Fill Color to about 120d. The occasional solid-fill tile now has a distinct green-ish tint, adding color accents to the glitch.
5. **Animate**: Increase Speed to about 40%. The corruption pattern shifts frame by frame, creating an animated glitch that evolves over time.

**Key concepts**: Mode bias favors address offset (tile displacement), fill color only affects solid-fill mode tiles, LFSR speed controls how quickly the glitch pattern changes

---

### Exercise 3: 8-Bit Breakdown

<img src={killscreen_exercise3_result} alt="8-Bit Breakdown result"/>
*8-Bit Breakdown — simulated result across source images.*
**Source**: Any dynamic video — music performance, abstract patterns, or live camera.

**Objective**: Combine all corruption controls for maximum visual destruction.

1. **Small tiles**: Set Tile Size to 8×8 for fine-grained corruption.
2. **Full corruption**: Corrupt Amt to 100%.
3. **Fast evolution**: Speed to about 80%. The corruption pattern changes rapidly, creating animated visual chaos.
4. **Grid overlay**: Enable Grid Lines with Border Brt at about 70%. The fine 8-pixel grid becomes prominently visible, creating a retro tile-map aesthetic.
5. **Fill color**: Sweep Fill Color through its full range. Watch the solid-fill tiles shift through different color tints.
6. **Mix blend**: Lower Mix to about 60%. The corruption becomes semi-transparent, blending with the clean image underneath for a ghostly data-corruption effect.
7. **Direction toggle**: Flip Direction mid-performance. The corruption front jumps to the opposite side of the screen.

**Key concepts**: Smaller tiles create finer corruption grain, high speed creates animated chaos, mix blend creates semi-transparent glitch overlay

---


## Tips

- **Start subtle**: Begin with Corrupt Amt around 20–30% to create a gentle glitch accent on one side of the screen, then increase for more destruction.
- **Pac-Man mode is authentic**: The Mode Bias "Pac-Man" setting recreates the original kill screen's visual character — predominantly displaced tiles with occasional color errors. Use it for retro authenticity.
- **Unused knobs are safe**: Offset Range and Color Intns have no effect. You can use them as visual placeholders or ignore them.
- **Grid lines reveal structure**: Enable Grid Lines at low brightness to subtly reveal the tile map underlying the corruption, adding an extra layer of retro-game aesthetic.
- **Speed controls drama**: Very low Speed creates a slow, menacing corruption that shifts every few seconds. Very high Speed creates frenetic, animated chaos. Match the speed to your performance tempo.
- **Mix for layering**: At 40–60% Mix, the corruption becomes a semi-transparent overlay on the clean image — effective for creating data-corruption atmospherics without obliterating the source.
- **Direction for composition**: Use Direction to place the clean portion of the screen where your subject is, and the corruption on the background or periphery.
- **Tile size matters**: 8×8 tiles create fine-grained noise-like corruption. 32×32 tiles create bold, blocky corruption patches. Match tile size to the visual scale of your source material.

---

## Glossary

| Term | Definition |
|------|------------|
| **Corruption** | Deliberate introduction of data errors into the video signal to produce glitch aesthetics. |
| **Galois LFSR** | A Linear Feedback Shift Register using XOR taps on the output bit; produces a pseudo-random binary sequence used for tile hashing. |
| **Hash** | A deterministic function that maps tile coordinates to a pseudo-random value, ensuring repeatable per-tile corruption decisions. |
| **Kill Screen** | A level in an arcade game where a software bug causes the display to become unplayable due to memory corruption; most famously, Pac-Man level 256. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function (XOR) of its previous state, producing a repeating pseudo-random sequence. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **Tile** | A fixed-size rectangular block of pixels (e.g., 8×8 or 16×16) treated as a single unit in a tile-based graphics system. |
| **Tile Map** | A data structure mapping screen grid positions to pattern indices in a character ROM; the addressing scheme corrupted by kill-screen bugs. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
