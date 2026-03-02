---
draft: true
sidebar_position: 42
slug: /instruments/videomancer/charset
title: "Charset"
image: /img/instruments/videomancer/charset/charset_hero.png
description: "Every screen you have ever read — every terminal, every text editor, every status display — renders characters on a fixed grid."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import charset_hero from '/img/instruments/videomancer/charset/charset_hero.png';
import charset_control_panel from '/img/instruments/videomancer/charset/charset_control_panel.png';
import charset_exercise1_result from '/img/instruments/videomancer/charset/charset_exercise1_result.png';
import charset_exercise2_result from '/img/instruments/videomancer/charset/charset_exercise2_result.png';
import charset_exercise3_result from '/img/instruments/videomancer/charset/charset_exercise3_result.png';
import charset_source1_kodim15 from '/img/instruments/videomancer/charset/charset_source1_kodim15.png';
import charset_source2_kodim03 from '/img/instruments/videomancer/charset/charset_source2_kodim03.png';
import charset_source3_kodim15_bw from '/img/instruments/videomancer/charset/charset_source3_kodim15_bw.png';

# Charset

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: charset_source1_kodim15, after: charset_hero },
    { label: "Kodim03", before: charset_source2_kodim03, after: charset_hero },
    { label: "Kodim15 B&W", before: charset_source3_kodim15_bw, after: charset_hero },
  ]}
/>
*Charset rendering video luminance as density-mapped glyph patterns on an 8×8 cell grid, transforming continuous imagery into typographic texture.*

---

## Overview

Every screen you have ever read — every terminal, every text editor, every status display — renders characters on a fixed grid. Each cell in the grid maps a code point to a bitmap, painting a small cluster of pixels in a pattern that your brain reads as a letter, a digit, a symbol. Charset applies this same principle to live video: it divides the frame into 8×8 pixel cells, samples the brightness of the input at each cell boundary, and replaces the cell contents with a density pattern chosen to approximate that brightness.

The program does not contain an actual character ROM or font table. Instead, it uses a set of eight procedurally generated fill patterns — from empty to solid — based on combinatorial logic of the local pixel coordinates within each cell. The patterns include checkerboards at varying scales and boolean combinations (AND, OR, XOR, NAND) of coordinate bits. From a distance, the result reads as a mosaic of typographic density, evoking the look of ASCII art, dot-matrix printouts, or early character-generator video.

At conservative settings, Charset is a stylized mosaic effect — a grid of tiles with brightness-appropriate fill. With the controls pushed further, it becomes a binary texture engine: grid lines delineate the cells, inversion flips the density map, mono strips all color, and the mix fader lets the original video bleed through the pattern structure.

---

## Background

### ASCII Art and Character Density

The tradition of representing images with text characters dates to the earliest computer terminals. Operators discovered that certain characters — `@`, `#`, `%`, `.`, ` ` — have different visual densities when viewed on a monospaced grid. By mapping image brightness to characters of corresponding density, a recognizable image could be "printed" using nothing but the ASCII character set. Charset automates this principle in hardware: each cell's brightness is classified into one of eight density levels, and a corresponding fill pattern is rendered in place of the original pixels.

### The Character Cell Grid

Early computer displays were organized as grids of fixed-size character cells — typically 8×8 or 8×16 pixels. The display hardware read a character code from video memory, looked up the corresponding bitmap in a character generator ROM, and painted the bitmap into the cell. This cell-grid structure is the foundation of Charset's spatial organization. The program divides every video frame into 8×8 pixel cells, creating a grid of 240×135 cells in a 1920×1080 raster (or proportionally fewer at lower resolutions). The grid is tracked by a pair of 3-bit counters that cycle from 0 to 7 in each axis, wrapping at cell boundaries.

### Dithering via Density Patterns

Charset's eight fill patterns form a **density ramp** — a sequence of spatial patterns with progressively higher fill ratios. This is a form of **spatial dithering**: representing a continuous range of brightness values using only binary (on/off) pixel states arranged in specific geometric patterns. The technique is identical in principle to the halftone screens used in newspaper printing, where varying dot sizes create the illusion of gray tones from pure black ink. The eight levels provide a coarse but visually effective approximation of continuous luminance.

### Checkerboard Patterns and Boolean Logic

The fill patterns in Charset are not stored as bitmaps — they are generated on the fly using combinatorial logic on the local x and y coordinates within each cell. By selecting different bits of the 3-bit coordinates and combining them with AND, OR, XOR, and NAND operations, the hardware produces patterns ranging from sparse corner fills (density 1) through fine checkerboards (density 4) to nearly solid fills (density 6). This approach requires zero memory — no BRAM, no lookup tables — and produces perfectly repeating, aliasing-free patterns at zero additional latency.

### From CRT Character Generators to FPGA

The original character generator chips of the 1970s and 1980s — the Motorola MC6847, the Commodore VIC, the Signetics 2513 — used mask-programmed ROMs to store glyph bitmaps. A character code was fetched from video RAM and used as an address into the ROM, producing one scanline of pixels per clock. Charset replaces the ROM with combinatorial logic, and replaces the character code lookup with a luminance-to-density classification. The result is a pipeline that echoes the architecture of those vintage chips while processing live video at 74.25 MHz.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Sync Detection ─────────────────────────────────────────────
│   ├─ hsync_n / vsync_n falling-edge detection
│   └─ x_counter, y_counter frame position tracking
│
├── Cell Grid Tracking ─────────────────────────────────────────
│   ├─ local_x (0–7), local_y (0–7) within each cell
│   ├─ cell_x, cell_y cell-index counters
│   └─ Sample & hold: latch input Y when local_x wraps to 0
│
├── Density Classification ─────────────────────────────────────
│   └─ v_density = held_y[9:7]  (top 3 bits → 8 levels)
│
├── Pattern Generation ─────────────────────────────────────────
│   ├─ density 0: empty
│   ├─ density 1: local_x[2] AND local_y[2]        (corner fill)
│   ├─ density 2: local_x[1] XOR local_y[1]        (2×2 checker)
│   ├─ density 3: local_x[1] AND local_y[1]        (2×2 grid)
│   ├─ density 4: local_x[0] XOR local_y[0]        (fine checker)
│   ├─ density 5: local_x[0] OR  local_y[0]        (dense fill)
│   ├─ density 6: local_x[0] NAND local_y[0]       (near-solid)
│   └─ density 7: solid
│
├── Post-Processing ────────────────────────────────────────────
│   ├─ Invert toggle (complement pattern bit)
│   ├─ Grid lines (force pattern = 1 at cell boundary)
│   ├─ Y output: pattern = 1 → brightness, pattern = 0 → 64
│   └─ Mono: U, V → 512 (mid-gray) or pass-through
│
├── Mix ────────────────────────────────────────────────────────
│   └─ 3× interpolator_u (Y, U, V wet/dry blend)
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock shift register (hsync, vsync, field, Y, U, V)
│
└── Output Assignment ──────────────────────────────────────────
    └─ bypass = 0 → mixed output, bypass = 1 → delayed dry
```

The critical timing interaction is the sample-and-hold at cell boundaries. When the `local_x` counter wraps from 7 back to 0, the current input Y value is latched into `s_held_y`. This held value persists for all 64 pixels of the cell, providing a single brightness measurement for density classification. The 3-bit density index is simply the top three bits of the held luminance — a direct, zero-latency quantization that splits the 10-bit luminance range into eight equal bands of 128 counts each.

The pattern generator is purely combinatorial: no ROM, no memory, no BRAM. Each of the eight patterns is a single boolean function of `local_x` and `local_y`. The 8-clock processing delay through the main pipeline is matched by a parallel shift-register delay on the dry input signal, ensuring the interpolator mixes temporally aligned samples at the output.

---

## Parameter Reference

<img src={charset_control_panel} alt="Videomancer front panel with Charset loaded"/>
*Videomancer's front panel with Charset active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

Cell Size selects the dimensions of the character cell grid. The `steps_8` control mode quantizes the knob into eight discrete positions, selecting cell divisions from 1 (where each pixel gets its own density classification, effectively a per-pixel posterizer) to 8 (the classic character generator cell size). Smaller values preserve more spatial detail from the source image because the density is re-evaluated more frequently across the frame. Larger values create a coarser, more abstract mosaic where individual fill patterns are clearly visible as distinct tiles.

---

#### Knob 2 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Threshold sets a luminance floor for density classification. Below this level, all cells are forced to the empty pattern regardless of input brightness. At 0%, the full luminance range maps to density patterns. As you increase the threshold, progressively brighter regions of the source are driven to density zero, carving away the darker portions of the image. This is useful for isolating bright elements against a dark field or for creating a hard cutoff that separates filled cells from empty ones.

---

#### Knob 3 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

Brightness controls the luminance value assigned to "lit" pixels — those where the density pattern outputs a 1. At full value, lit pixels reach peak white. Reducing brightness dims the pattern output, creating a softer, lower-contrast character display. The dark pixels (pattern = 0) are fixed at a low luminance level of 64 out of 1023, so this control sets the effective dynamic range of the character rendering. It determines how boldly the glyph patterns stand out against their dark background.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Contrast adjusts the luminance difference between lit and unlit pixels within each cell. At minimum, the pattern structure disappears as lit and unlit pixels converge to the same level. At maximum, the binary pattern snaps to its full black-and-white range. This control works independently of Brightness: you can have bright but low-contrast characters (light gray on slightly darker gray) or dim but high-contrast characters (dark on black). The interplay between Brightness and Contrast shapes the visual weight of the typographic texture.

---

#### Knob 5 — Font Weight
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Font Weight shifts the density classification curve, making all patterns heavier or lighter across the entire frame. Increasing font weight biases each cell toward a higher density level — cells that would render as empty become sparse, sparse cells become medium, and medium cells become dense. The effect is analogous to selecting a heavier typeface weight: the same spatial structure carries more visual mass. At maximum weight, nearly all cells render at density 7 (solid), flooding the frame with the brightness value.

---

#### Knob 6 — Spacing
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Spacing introduces a gap between adjacent character cells by blanking pixels near cell boundaries. At 0%, cells are tightly packed with no visible separation between them. As spacing increases, a progressively wider border of empty pixels appears around each cell, isolating the density pattern within a smaller region. At maximum spacing, the patterns shrink to small clusters at the center of each cell, surrounded by dark borders. This transforms the look from a continuous mosaic into a dot-matrix display with visible inter-character gaps.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Invert** | Off | On |
| **8 — Mono** | Off | On |
| **9 — Grid Lines** | Off | On |
| **10 — Bold** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control independent binary processing options. Invert and Grid Lines modify the pattern output. Mono affects the chrominance channels. Bold modifies the density classification. Bypass routes the signal around the entire processing chain. These switches can be combined freely — for example, Invert + Grid Lines + Mono creates a white-on-black terminal aesthetic with visible cell boundaries.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix controls the wet/dry blend between the processed character display and the original video signal. At 100% (full clockwise), the output is entirely the character-rendered version. At 0%, the output is the unprocessed input. Intermediate positions create a translucent overlay where the character patterns float above or blend into the source imagery. Three parallel interpolator instances handle Y, U, and V independently, maintaining correct color blending through the crossfade. A subtle mix setting around 50–70% can produce a ghostly overlay of typographic texture on live video.

---

## Guided Exercises

These exercises explore Charset's character density rendering from basic grid visualization through creative typographic textures. Each exercise demonstrates a different aspect of the luminance-to-pattern mapping and its interaction with the processing controls.

### Exercise 1: Terminal Display

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: charset_source1_kodim15, after: charset_exercise1_result },
    { label: "Kodim03", before: charset_source2_kodim03, after: charset_exercise1_result },
    { label: "Kodim15 B&W", before: charset_source3_kodim15_bw, after: charset_exercise1_result },
  ]}
/>
*Terminal Display — simulated result across source images.*
**Source**: A talking-head interview or portrait footage with clear tonal separation between subject and background.

**Objective**: Create a classic terminal-style character display where the subject is rendered in visible density patterns on a monochrome grid.

1. **Establish the grid**: Start with all controls at default positions. The video should appear as a grid of brightness-mapped tiles.
2. **Go monochrome**: Enable Mono (Toggle 8) to strip color, creating a phosphor-terminal aesthetic.
3. **Add grid lines**: Enable Grid Lines (Toggle 9) to outline each cell, making the character matrix explicit.
4. **Adjust brightness**: Sweep Brightness (Knob 3) upward to find a level where the lit pixels are clearly visible against the dark background — the text should "pop."
5. **Blend the source**: Pull the Mix fader to about 70% to let a ghost of the original video show through the character grid, anchoring the patterns to the underlying subject.

**Key concepts**: Density classification maps continuous luminance to discrete pattern levels, mono mode strips chroma to emulate monochrome terminals, grid lines delineate the cell structure

---

### Exercise 2: Inverted Dot Matrix

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: charset_source1_kodim15, after: charset_exercise2_result },
    { label: "Kodim03", before: charset_source2_kodim03, after: charset_exercise2_result },
    { label: "Kodim15 B&W", before: charset_source3_kodim15_bw, after: charset_exercise2_result },
  ]}
/>
*Inverted Dot Matrix — simulated result across source images.*
**Source**: High-contrast footage with strong shapes — stage lighting, silhouettes, or graphic title cards.

**Objective**: Explore inverted density mapping with spacing to create a dot-matrix printer effect where dark source areas appear as dense clusters.

1. **Invert the density**: Enable Invert (Toggle 7). Bright areas now appear empty and dark areas appear filled — the density map is reversed.
2. **Add spacing**: Increase Spacing (Knob 6) to about 50%. Each cell's pattern shrinks away from the borders, creating visible gaps between character glyphs.
3. **Increase font weight**: Push Font Weight (Knob 5) up to about 70% to fill out the patterns, adding ink to each cell.
4. **Enable bold**: Toggle Bold (Toggle 10) on for an additional density step, stacking with font weight.
5. **Apply threshold**: Raise Threshold (Knob 2) to about 30% to carve away the weakest density levels, leaving only the strongest patterns.

**Key concepts**: Invert reverses the brightness-to-density mapping, spacing isolates cells into individual dot clusters, font weight and bold stack to control visual density

---

### Exercise 3: Color Character Mosaic

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: charset_source1_kodim15, after: charset_exercise3_result },
    { label: "Kodim03", before: charset_source2_kodim03, after: charset_exercise3_result },
    { label: "Kodim15 B&W", before: charset_source3_kodim15_bw, after: charset_exercise3_result },
  ]}
/>
*Color Character Mosaic — simulated result across source images.*
**Source**: Colorful footage — flowers, graffiti, abstract art, or a color bar test pattern.

**Objective**: Create a colored character mosaic where density patterns carry the source's original chrominance, producing stained-glass-like tiles.

1. **Disable mono**: Ensure Mono (Toggle 8) is Off so chrominance passes through the pattern pipeline.
2. **Enable grid lines**: Turn on Grid Lines (Toggle 9) for a structured grid look that separates each chromatic tile.
3. **Adjust brightness and contrast**: Balance Brightness (Knob 3) at about 60% and Contrast (Knob 4) at about 70% so patterns are vivid but not washed out.
4. **Full mix**: Set Mix to 100%. The output is entirely the character display, but each cell carries the source's original color — density from Y, hue from UV.
5. **Sweep font weight**: Slowly increase Font Weight (Knob 5) to watch the mosaic fill in, revealing how density and color interact as patterns grow heavier.

**Key concepts**: Leaving mono off preserves source chrominance through the pattern pipeline, density is driven by luminance only while color flows through independently, grid lines create the aesthetic of a colored character display

---


## Tips

- **Start with Mono + Grid Lines**: This combination immediately reveals the character grid structure and makes density patterns easy to read without color distraction. It is the fastest way to understand the effect.
- **Brightness controls the ink**: Think of Brightness as the ink density on a dot-matrix printer. Higher values produce bolder, more visible characters; lower values create a faded printout look.
- **Cell Size is your resolution control**: Smaller cells preserve more of the source image's spatial detail but reduce the visibility of individual patterns. Larger cells abstract the image further into coarse typography.
- **Use Mix for overlays**: A Mix setting around 50–70% lets the source video show through the character grid, creating the look of text or a heads-up display overlaid on live footage.
- **Invert for negative prints**: Enabling Invert produces the look of a photographic negative rendered in characters — bright objects appear as voids in a dense field. This is especially effective with high-contrast sources.
- **Grid Lines + Spacing together**: Combining these two controls creates strongly delineated cells with visible gaps, evoking the aesthetic of LED matrix displays, tiled mosaic art, or retro grid-based games.
- **Feedback routing**: Routing the output back to the input creates recursive character rendering — each successive pass re-classifies the density patterns into new patterns, generating self-similar typographic textures that evolve over time.
- **Bold vs. Font Weight**: Bold is a binary one-step density shift (toggle); Font Weight is a continuous sweep (knob). Use Bold for quick A/B comparison of pattern heaviness, Font Weight for precise creative adjustment.

---

## Glossary

| Term | Definition |
|------|------------|
| **ASCII Art** | A graphic design technique using printable characters from the ASCII character set, arranged on a monospaced text grid to approximate images through varying character density. |
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric. Charset uses zero BRAMs — all patterns are generated combinatorially. |
| **Cell** | A fixed-size rectangular region of pixels (8×8 by default) within the character grid. Each cell receives a single density classification and renders the corresponding fill pattern. |
| **Character Generator** | A hardware subsystem that converts character codes to pixel bitmaps, historically implemented as a ROM chip (e.g., Motorola MC6847, Signetics 2513). |
| **Chroma** | The color difference components (U and V) of a YUV video signal, representing hue and saturation. |
| **Density** | The proportion of lit pixels within a cell pattern. Higher density means more filled area and a brighter apparent cell when viewed from a distance. |
| **Density Ramp** | A sequence of fill patterns with increasing visual weight, used to represent continuous brightness values as binary on/off spatial patterns. |
| **Dot Matrix** | A display or printing technology that forms characters and images from a rectangular grid of individual dots, with visible spacing between elements. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable integrated circuit that executes the video processing pipeline in real time. |
| **Halftone** | A reprographic technique simulating continuous tones through varying dot sizes or spacing; the printing-press equivalent of density-based character rendering. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages, each producing one output per clock cycle with fixed total latency. |
| **Sample and Hold** | A technique that captures an input value at a specific moment and maintains that value at the output until the next sampling event. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer processing pipeline. |

---
