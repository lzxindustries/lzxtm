---
draft: true
sidebar_position: 126
slug: /instruments/videomancer/gazette
title: "Gazette"
image: /img/instruments/videomancer/gazette/gazette_hero_s1.png
description: "Every home computer of the early 1980s faced the same engineering constraint: memory was expensive, and storing a unique color for every pixel on screen was a luxury none of them could afford."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import gazette_control_panel from '/img/instruments/videomancer/gazette/gazette_control_panel.png';
import gazette_source1_castle from '/img/instruments/videomancer/gazette/gazette_source1_castle.png';
import gazette_source2_car from '/img/instruments/videomancer/gazette/gazette_source2_car.png';
import gazette_source3_turtle from '/img/instruments/videomancer/gazette/gazette_source3_turtle.png';
import gazette_source4_pattern from '/img/instruments/videomancer/gazette/gazette_source4_pattern.png';
import gazette_source5_man from '/img/instruments/videomancer/gazette/gazette_source5_man.png';
import gazette_source6_knit from '/img/instruments/videomancer/gazette/gazette_source6_knit.png';
import gazette_hero_s1 from '/img/instruments/videomancer/gazette/gazette_hero_s1.png';
import gazette_hero_s2 from '/img/instruments/videomancer/gazette/gazette_hero_s2.png';
import gazette_hero_s3 from '/img/instruments/videomancer/gazette/gazette_hero_s3.png';
import gazette_hero_s4 from '/img/instruments/videomancer/gazette/gazette_hero_s4.png';
import gazette_hero_s5 from '/img/instruments/videomancer/gazette/gazette_hero_s5.png';
import gazette_hero_s6 from '/img/instruments/videomancer/gazette/gazette_hero_s6.png';
import gazette_ex1_s1 from '/img/instruments/videomancer/gazette/gazette_ex1_s1.png';
import gazette_ex1_s2 from '/img/instruments/videomancer/gazette/gazette_ex1_s2.png';
import gazette_ex1_s3 from '/img/instruments/videomancer/gazette/gazette_ex1_s3.png';
import gazette_ex1_s4 from '/img/instruments/videomancer/gazette/gazette_ex1_s4.png';
import gazette_ex1_s5 from '/img/instruments/videomancer/gazette/gazette_ex1_s5.png';
import gazette_ex1_s6 from '/img/instruments/videomancer/gazette/gazette_ex1_s6.png';
import gazette_ex2_s1 from '/img/instruments/videomancer/gazette/gazette_ex2_s1.png';
import gazette_ex2_s2 from '/img/instruments/videomancer/gazette/gazette_ex2_s2.png';
import gazette_ex2_s3 from '/img/instruments/videomancer/gazette/gazette_ex2_s3.png';
import gazette_ex2_s4 from '/img/instruments/videomancer/gazette/gazette_ex2_s4.png';
import gazette_ex2_s5 from '/img/instruments/videomancer/gazette/gazette_ex2_s5.png';
import gazette_ex2_s6 from '/img/instruments/videomancer/gazette/gazette_ex2_s6.png';
import gazette_ex3_s1 from '/img/instruments/videomancer/gazette/gazette_ex3_s1.png';
import gazette_ex3_s2 from '/img/instruments/videomancer/gazette/gazette_ex3_s2.png';
import gazette_ex3_s3 from '/img/instruments/videomancer/gazette/gazette_ex3_s3.png';
import gazette_ex3_s4 from '/img/instruments/videomancer/gazette/gazette_ex3_s4.png';
import gazette_ex3_s5 from '/img/instruments/videomancer/gazette/gazette_ex3_s5.png';
import gazette_ex3_s6 from '/img/instruments/videomancer/gazette/gazette_ex3_s6.png';

# Gazette

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: gazette_source1_castle, after: gazette_hero_s1 },
    { label: "Car", before: gazette_source2_car, after: gazette_hero_s2 },
    { label: "Turtle", before: gazette_source3_turtle, after: gazette_hero_s3 },
    { label: "Pattern", before: gazette_source4_pattern, after: gazette_hero_s4 },
    { label: "Man", before: gazette_source5_man, after: gazette_hero_s5 },
    { label: "Knit", before: gazette_source6_knit, after: gazette_hero_s6 },
  ]}
/>
*Gazette imposing ZX Spectrum-style attribute cell restrictions on live video, producing characteristic two-color-per-cell patterns with chroma bleed artifacts.*

---

## Overview

Every home computer of the early 1980s faced the same engineering constraint: memory was expensive, and storing a unique color for every pixel on screen was a luxury none of them could afford. The solution — used independently by Sinclair, IBM, Commodore, and the MSX consortium — was the **attribute cell**: divide the screen into a grid of small tiles and assign each tile just two colors from a fixed palette. Gazette recreates this restriction in real time on live video.

The program divides the incoming frame into character cells (4, 8, 16, or 32 pixels wide), samples the luminance at the center of each cell, and uses that measurement to pick two palette colors — an "ink" for bright pixels and a "paper" for dark pixels. Each pixel within the cell is then thresholded against the cell's reference luma and colored accordingly. The result is the distinctive banded, clashing look of 8-bit computer graphics applied to any video source. The name *Gazette* references the newspaper-like quality of the output: coarse halftone structure, limited color, and a blocky grid that recalls newsprint or early teletext pages.

At default settings Gazette produces clean retro-computing aesthetics with sharp cell boundaries and a well-defined palette. Pushing the Ink Bias and Paper Bias controls introduces intentional palette mismatches and color distortion. Enabling Color Bleed smears chroma horizontally across cell boundaries, replicating the analog artifact that plagued composite video connections on real 8-bit hardware. The Flash toggle swaps ink and paper colors on a half-second cycle, directly modeling the ZX Spectrum's FLASH attribute bit.

---

## Quick Start

1. **8px cells for authenticity**: The ZX Spectrum used 8 × 8 character cells. Setting Cell Size to 8px in Square mode produces the most historically accurate attribute clash pattern.
2. **Black Paper for clarity**: Enable Black Paper when you want the palette colors to stand out against a clean background. This avoids the muddy look that comes from mismatched paper colors in adjacent cells.
3. **Color Bleed transforms aesthetics**: Even a small amount of color bleed softens the harsh cell boundaries and adds an analog warmth. High bleed at large cell sizes produces wide rainbow streaks reminiscent of badly tuned PAL decoders.

---

## Background

### The ZX Spectrum Attribute Cell

The Sinclair ZX Spectrum (1982) stored its display in a notoriously quirky format. The pixel bitmap occupied 6144 bytes — one bit per pixel across 256 × 192 resolution — but color information was stored separately in a 768-byte **attribute area**, one byte per 8 × 8 character cell. Each attribute byte specified an ink color (foreground), a paper color (background), a bright flag, and a flash flag, all drawn from a fixed palette of 8 colors (15 with the bright variant). This meant every 8 × 8 block of pixels could show at most two colors. When the image content didn't align neatly with the cell grid, adjacent cells displayed clashing color pairs — the infamous **attribute clash** that became the Spectrum's visual signature. Game artists spent enormous effort designing graphics that worked within or artistically exploited this limitation.

### CGA, C64, and MSX Palette Comparisons

Other platforms imposed similar constraints with different palettes. IBM's CGA adapter (1981) offered 16 colors but typically displayed only 4 at a time in graphics modes — a restriction that forced distinctive cyan-magenta-white or red-green-yellow color schemes. The Commodore 64 (1982) had a fixed 16-color palette with earth tones and muted blues derived from the VIC-II chip's analog color generation. The MSX standard (1983) used Texas Instruments' TMS9918A video display processor with its own 15-color palette plus transparent, characterized by saturated primaries and limited intermediate tones. Gazette packs all four palettes into a single 64-entry ROM, selectable with one knob. Each platform's entries are sorted by luminance and split into normal (indices 0–7) and bright (indices 8–15) halves, allowing the Bright toggle to select the vivid variant.

### Threshold-Based Ink and Paper Assignment

Within each cell, Gazette must decide which pixels get the ink color and which get the paper color. It does this by comparing each pixel's luminance to an adaptive **cutoff** value: the cell's sampled center luma plus a user-adjustable offset from the Threshold knob. Pixels brighter than the cutoff become ink; pixels darker become paper. The Ink Bias knob shifts the palette index for ink colors by adding an offset to the sampled cell luma before the palette lookup, allowing you to push ink assignments toward brighter or dimmer palette entries. Paper Bias independently selects which palette entry the paper pixels receive — at the default midpoint, paper tends toward a mid-palette color; fully counter-clockwise, paper becomes the darkest available color. The Black Paper toggle overrides this entirely, forcing paper to index 0 (always black) regardless of the bias setting.

### Color Bleed and Attribute Clash Artifacts

On real 8-bit hardware, attribute clash was a spatial artifact — colors bled across cell boundaries because the hardware painted each cell's attribute across all its pixels. But a second artifact occurred when these computers were connected to a television via composite video: the chrominance signal smeared horizontally because of the limited bandwidth of the NTSC or PAL chroma subcarrier. Gazette replicates this with a four-level horizontal IIR (infinite impulse response) filter on the U and V chroma channels. At the lowest bleed setting ("Off"), chroma transitions are sharp at cell boundaries. At "Low" (50% IIR coefficient), chroma smears gently into adjacent cells. At "Med" (75%) and "High" (~94%), the smear extends across multiple cells, producing the rainbow fringing and color bleeding characteristic of composite video on vintage hardware. The luma channel is never bled — only chroma — matching the behavior of real composite decoders.

### The FLASH Attribute

The ZX Spectrum's attribute byte included a single FLASH bit. When set, the hardware automatically swapped the ink and paper colors of that cell at a rate of approximately once per second (alternating every 16 frames at 50 Hz). Programmers used it for blinking cursors, flashing warning messages, and simple animation effects. Gazette's Flash toggle simulates this behavior globally: when enabled, all cells swap their ink and paper assignments every 16 frames (based on an internal frame counter), producing a rhythmic color inversion across the entire image.


---

## Signal Flow

Input Registration → Palette Index + Threshold → Output Registration

```
Input Video (YUV 4:4:4)
│
├── Cell Tracking ──────────────────────────────────────────────
│   ├─ Pixel counter + cell column index
│   ├─ Cell sub-row counter (square mode)
│   └─ Center detection → BRAM write (column luma buffer)
│
├── Stage 1: Input Registration + BRAM Read/Write ──────────────
│   └─ Sample cell center luma → s_col_samples[cell_col]
│
├── Stage 2: Palette Index + Threshold ─────────────────────────
│   ├─ ink_half = (cell_luma + ink_bias) >> 7     (3-bit)
│   ├─ paper_half = paper_bias >> 7               (3-bit)
│   ├─ Black Paper override → paper_half = 0
│   ├─ ink_full = bright & ink_half               (4-bit)
│   ├─ paper_full = bright & paper_half           (4-bit)
│   ├─ ink_addr = palette_sel & ink_full           (6-bit)
│   ├─ paper_addr = palette_sel & paper_full       (6-bit)
│   └─ Threshold: pixel_Y >= cell_luma + (threshold - 512) → INK
│
├── Stage 2b: Flash Swap + Address Selection ───────────────────
│   ├─ Flash toggle + frame_count(4) → swap ink/paper
│   └─ Select final palette address
│
├── Stage 3a: Palette ROM Lookup ───────────────────────────────
│   └─ 64-entry YUV palette → (Y, U, V) from address
│
├── Stage 3b: Color Bleed IIR ──────────────────────────────────
│   ├─ Y: direct pass-through (no bleed)
│   └─ U, V: horizontal IIR (0% / 50% / 75% / ~94%)
│
├── Stage 4: Output Registration ───────────────────────────────
│   └─ comp_y, comp_u, comp_v → interpolator inputs
│
├── Mix Stage: Interpolator (4 clk) ────────────────────────────
│   └─ 3× interpolator_u: wet/dry crossfade per channel
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 10-clock shift register for hsync, vsync, field, YUV
│
└── Output ─────────────────────────────────────────────────────
    └─ Bypass mux: processed or delayed original
```

The pipeline has two critical data paths that converge at Stage 2. The **cell luma path** samples the input Y value at each cell's center pixel and stores it in a 256-entry BRAM column buffer; the stored value becomes the reference for the entire cell. The **pixel path** carries each pixel's own Y value through a one-clock register. At Stage 2, the pixel Y is compared against the cell reference (offset by Threshold) to produce the ink/paper decision, while the cell reference simultaneously drives the ink palette index computation via Ink Bias. This means a single sampled pixel at the cell center determines both *which* colors the cell uses and *where* the boundary between them falls.

The Color Bleed IIR filter at Stage 3b operates only on chroma, leaving luma sharp. This matches the physical behavior of composite video: luminance bandwidth is high, chrominance bandwidth is low. The IIR state resets at the start of each scan line, preventing color from the right edge of one line from bleeding into the left edge of the next.

---

## Parameter Reference

<img src={gazette_control_panel} alt="Videomancer front panel with Gazette loaded"/>
*Videomancer's front panel with Gazette active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 2 |

Selects the character cell width in pixels: 4, 8, 16, or 32. Smaller cells produce finer detail and more accurate color reproduction but create a busier grid. Larger cells create bold, blocky graphics with more dramatic attribute clash — each cell covers more of the image, so the two-color restriction becomes more visually apparent. The 8-pixel setting most closely matches the ZX Spectrum's original 8 × 8 character cells. In Square cell shape mode, the cell height matches the width; in 8×1 Row mode, each scan line acts as its own cell row regardless of this setting.

---

#### Knob 2 — Ink Bias
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Biases the ink (foreground) palette index by adding an offset to the cell's sampled luma before the palette lookup. At the default three-quarter position, ink colors track the cell brightness naturally — bright cells get bright ink, dark cells get dark ink. Turning counter-clockwise compresses the ink range toward darker palette entries; turning clockwise pushes it toward brighter entries. Extreme settings cause all cells to share similar ink colors regardless of their actual brightness, which flattens the tonal structure but can create striking uniform color fields.

---

#### Knob 3 — Paper Bias
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Selects which palette entry is used for the paper (background) color. Unlike Ink Bias, Paper Bias is independent of the cell's sampled luma — it directly maps a range of the knob position to one of 8 (or 16 with Bright) palette entries. At the default one-quarter position, paper tends toward darker entries. Turning clockwise selects progressively brighter paper colors. Combined with the Black Paper toggle, this control lets you choose between a uniform black background (toggle on) or a colored background that varies across the palette range (toggle off, knob sweeping).

---

#### Knob 4 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Adjusts the luminance threshold that separates ink pixels from paper pixels within each cell. At the default center position, the cutoff equals the cell's sampled center luma — pixels brighter than the cell center become ink, pixels darker become paper. Turning counter-clockwise lowers the cutoff, making more pixels qualify as ink (brighter overall appearance). Turning clockwise raises the cutoff, making more pixels qualify as paper (darker overall appearance). This control interacts directly with the source material's contrast: high-contrast footage produces clean ink/paper separation at any threshold setting, while low-contrast footage may need careful threshold adjustment to produce a readable pattern.

---

#### Knob 5 — Palette
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

Selects one of four classic computer palettes. **ZX** provides the Sinclair Spectrum's 8-color palette (plus bright variants) with its strong primaries and characteristic cyan, magenta, and green. **CGA** reproduces IBM's 16-color graphics palette with its distinctive browns and dark gray. **C64** offers the Commodore 64's muted, earth-toned palette with its unique light blue and gray shades. **MSX** provides the TMS9918A's saturated, slightly warm palette. Each palette contains 16 entries split into normal (0–7, dim) and bright (8–15, vivid) halves, selected by the Bright toggle.

---

#### Knob 6 — Color Bleed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the strength of horizontal chroma smearing applied after the palette lookup. At the fully counter-clockwise position, chroma transitions are pixel-sharp at cell boundaries. Increasing the control engages a progressively stronger IIR lowpass on the U and V channels: "Low" blends 50% of the previous pixel's chroma with the current value, "Med" blends 75%, and "High" blends approximately 94%. The luma channel is never affected — only color bleeds. Higher settings replicate the rainbow fringing and chroma crawl visible on composite video connections to real 8-bit computers. The IIR state resets at the start of each scan line.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Bright** | Normal | Bright |
| **8 — Cell Shape** | 8x1 Row | Square |
| **9 — Black Paper** | Off | On |
| **10 — Flash** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles provide independent control over palette brightness, cell geometry, paper color forcing, color animation, and signal bypass. Bright and Black Paper interact with the palette index computation at Stage 2. Cell Shape affects the cell counter and BRAM write timing. Flash acts at Stage 2b after the ink/paper decision. Bypass operates at the final output mux after the interpolator.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the original input and the palette-restricted output. At 100% (fully up), the output is entirely the cell-colored signal. Pulling the fader down crossfades toward the original video, with 0% reproducing the input exactly. Intermediate positions create a translucent overlay effect where the cell grid is visible but the original image shows through. Three parallel `interpolator_u` instances handle Y, U, and V channels independently with 10-bit fractional precision.





---

## Guided Exercises

These exercises progress from exploring basic palette restriction to combining controls for complex retro-computing aesthetics. Each introduces new interactions between the cell grid, palette selection, and analog artifacts.

### Exercise 1: ZX Spectrum Text Screen

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: gazette_source1_castle, after: gazette_ex1_s1 },
    { label: "Car", before: gazette_source2_car, after: gazette_ex1_s2 },
    { label: "Turtle", before: gazette_source3_turtle, after: gazette_ex1_s3 },
    { label: "Pattern", before: gazette_source4_pattern, after: gazette_ex1_s4 },
    { label: "Man", before: gazette_source5_man, after: gazette_ex1_s5 },
    { label: "Knit", before: gazette_source6_knit, after: gazette_ex1_s6 },
  ]}
/>
*ZX Spectrum Text Screen — simulated result across source images.*
**Source**: A camera pointed at printed text, a title card, or any high-contrast monochrome source.

**What You'll Create**: Recreate the ZX Spectrum's characteristic BASIC screen appearance — white text on a black background with sharp 8-pixel cells.

1. **Set the palette**: Turn Palette (Knob 5) to "ZX" (fully counter-clockwise).
2. **8-pixel cells**: Set Cell Size (Knob 1) to "8px" (one step from minimum).
3. **Black paper**: Enable Black Paper (Toggle 9) for a clean black background.
4. **Bright mode**: Enable Bright (Toggle 7) for full-intensity colors.
5. **Center threshold**: Set Threshold (Knob 4) to 50% — ink and paper divide at mid-gray.
6. **No bleed**: Set Color Bleed (Knob 6) fully counter-clockwise.
7. **Observe**: The source resolves into a grid of colored text-like blocks on a black field. Adjust Threshold to control how much of the image appears as "ink."
8. **Add flash**: Enable Flash (Toggle 10) — the entire screen blinks between ink and paper, like a ZX Spectrum FLASH attribute.

**Key concepts**: Attribute cell restriction limits each block to two colors, threshold controls which pixels become ink vs. paper, Black Paper forces a uniform background

---

### Exercise 2: Commodore Color Clash

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: gazette_source1_castle, after: gazette_ex2_s1 },
    { label: "Car", before: gazette_source2_car, after: gazette_ex2_s2 },
    { label: "Turtle", before: gazette_source3_turtle, after: gazette_ex2_s3 },
    { label: "Pattern", before: gazette_source4_pattern, after: gazette_ex2_s4 },
    { label: "Man", before: gazette_source5_man, after: gazette_ex2_s5 },
    { label: "Knit", before: gazette_source6_knit, after: gazette_ex2_s6 },
  ]}
/>
*Commodore Color Clash — simulated result across source images.*
**Source**: Footage with varied colors and moderate contrast — flowers, market scenes, or colorful patterns.

**What You'll Create**: Explore how different palettes and cell sizes generate "attribute clash" — the visible seams between adjacent cells that use different color pairs.

1. **C64 palette**: Turn Palette (Knob 5) to "C64" (two steps from minimum).
2. **Large cells**: Set Cell Size (Knob 1) to "32px" for dramatic cell boundaries.
3. **Square mode**: Enable Square cell shape (Toggle 8) for true tile appearance.
4. **Colored paper**: Turn off Black Paper (Toggle 9). Set Paper Bias (Knob 3) to ~50%.
5. **Observe the clash**: Scan across the image and note where adjacent cells use different color pairs. The boundary between them is hard and abrupt — this is attribute clash.
6. **Reduce cell size**: Step Cell Size down to 16px, then 8px. Watch attribute clash become finer-grained and less visible.
7. **Add color bleed**: Slowly increase Color Bleed (Knob 6) from Off through Low, Med, High. The chroma smears across cell boundaries, softening the clash.
8. **Compare palettes**: Switch between ZX, CGA, C64, and MSX. Each palette colors the same scene differently.

**Key concepts**: Larger cells create more visible attribute clash, color bleed softens chroma transitions between cells, each platform palette has a distinct color character

---

### Exercise 3: Composite Artifact Machine

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: gazette_source1_castle, after: gazette_ex3_s1 },
    { label: "Car", before: gazette_source2_car, after: gazette_ex3_s2 },
    { label: "Turtle", before: gazette_source3_turtle, after: gazette_ex3_s3 },
    { label: "Pattern", before: gazette_source4_pattern, after: gazette_ex3_s4 },
    { label: "Man", before: gazette_source5_man, after: gazette_ex3_s5 },
    { label: "Knit", before: gazette_source6_knit, after: gazette_ex3_s6 },
  ]}
/>
*Composite Artifact Machine — simulated result across source images.*
**Source**: Any dynamic footage with motion — panning cameras, moving subjects, or scrolling graphics.

**What You'll Create**: Combine color bleed, palette bias, and flash to replicate the full experience of 8-bit computer graphics on a composite video connection.

1. **CGA palette**: Set Palette to "CGA" — its browns and magentas are especially prone to composite artifacts.
2. **8-pixel cells**: Set Cell Size to "8px" and enable Square mode for a character-cell grid.
3. **Strong bleed**: Set Color Bleed (Knob 6) to "High" — chroma smears heavily across cells.
4. **Skewed bias**: Set Ink Bias high (~80%) and Paper Bias low (~20%) for strong contrast between foreground and background colors.
5. **Enable flash**: Toggle Flash (Toggle 10). Watch the color grid pulse as ink and paper swap every half second.
6. **Mix down**: Pull the Mix fader to ~60%. The processed grid becomes a translucent overlay on the original video — the cell structure is visible but the source shines through.
7. **Sweep threshold**: Slowly move Threshold (Knob 4) across its full range while flash is active. The proportion of ink to paper shifts, changing the density and rhythm of the blinking pattern.

**Key concepts**: High Color Bleed replicates composite video chroma smear, Flash creates rhythmic color inversion, Mix crossfades between processed and original signal, Ink and Paper Bias control the palette distribution

---


## Tips

- **Threshold tracks contrast**: High-contrast source material works best at the default 50% threshold. For low-contrast footage, lower the threshold to ensure enough pixels qualify as ink to produce visible detail.
- **Flash as performance tool**: Flash creates a rhythmic visual pulse that works well synchronized to music or other temporal events. The ~0.5-second cycle is slow enough to read but fast enough to feel energetic.
- **Mix for layering**: Use the fader at 40–60% to overlay the cell grid on the original video. The retro-computing aesthetic bleeds through the live image, creating a palimpsest effect.
- **Palette choice shapes mood**: ZX and CGA palettes are vivid and graphic; C64 is muted and earthy; MSX sits between them. Each palette imposes a different emotional character on the same footage.
- **Row mode for video**: 8×1 Row cell shape mode treats each scan line independently, which often looks better on moving video because vertical motion doesn't cause entire square cells to change color abruptly.

---

## Glossary

| Term | Definition |
|------|------------|
| **Attribute Cell** | A rectangular region of the screen that shares a single foreground (ink) and background (paper) color pair, as used by 1980s home computers. |
| **Attribute Clash** | The visible discontinuity at the boundary between adjacent attribute cells that use different color pairs, producing hard color seams in the image. |
| **BT.601** | ITU-R standard defining the YUV color matrix used for standard-definition video encoding and decoding. |
| **C64** | Commodore 64; a home computer (1982) whose VIC-II video chip produced a distinctive 16-color palette. |
| **CGA** | Color Graphics Adapter; IBM's first color display standard (1981) with a fixed 16-color palette. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Composite Video** | An analog video format that encodes luminance and chrominance on a single wire, causing chroma bandwidth limitations and color bleeding. |
| **FLASH** | An attribute flag on the ZX Spectrum that caused the ink and paper colors of a cell to swap at approximately 1 Hz. |
| **IIR** | Infinite Impulse Response; a filter structure where the output feeds back into the computation, creating exponential decay. |
| **Ink** | The foreground color assigned to bright pixels within an attribute cell. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **MSX** | A standardized home computer architecture (1983) using the TMS9918A video processor with a 15+1 color palette. |
| **Paper** | The background color assigned to dark pixels within an attribute cell. |
| **ROM** | Read-Only Memory; here, a lookup table of pre-computed palette values synthesized into FPGA logic at build time. |
| **ZX Spectrum** | A home computer by Sinclair Research (1982) famous for its attribute cell color system and resulting attribute clash. |

---
