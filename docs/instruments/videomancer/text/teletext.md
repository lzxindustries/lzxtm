---
draft: true
sidebar_position: 257
slug: /instruments/videomancer/teletext
title: "Teletext"
image: /img/instruments/videomancer/teletext/teletext_hero.png
description: "Every pixel in a video frame carries brightness information."
---

import teletext_before_after from '/img/instruments/videomancer/teletext/teletext_before_after.png';
import teletext_control_panel from '/img/instruments/videomancer/teletext/teletext_control_panel.png';
import teletext_exercise1_result from '/img/instruments/videomancer/teletext/teletext_exercise1_result.png';
import teletext_exercise2_result from '/img/instruments/videomancer/teletext/teletext_exercise2_result.png';
import teletext_exercise3_result from '/img/instruments/videomancer/teletext/teletext_exercise3_result.png';
import teletext_hero from '/img/instruments/videomancer/teletext/teletext_hero.png';
import teletext_source1_kodim15 from '/img/instruments/videomancer/teletext/teletext_source1_kodim15.png';
import teletext_source2_kodim15_bw from '/img/instruments/videomancer/teletext/teletext_source2_kodim15_bw.png';
import teletext_source3_male_1024 from '/img/instruments/videomancer/teletext/teletext_source3_male_1024.png';

# Teletext

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={teletext_hero} alt="Teletext hero image"/>
*Teletext rendering live video as density-sorted ASCII art through four selectable character sets — sixel mosaics, PETSCII semigraphics, CP437 shading, and Braille dot patterns.*
<img src={teletext_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Teletext applied.*

---

## Overview

Every pixel in a video frame carries brightness information. Teletext takes that brightness and translates it into a grid of typographic symbols — dense characters for bright areas, sparse characters for dark areas. The result is a live video image rendered entirely in text, recalling the character-mode graphics of 1970s Teletext broadcast services, Commodore 64 PETSCII art, and IBM PC ANSI art terminals.

The program divides the screen into a grid of rectangular cells, each mapped to one of sixteen density-sorted glyphs from a selectable character ROM. Four character sets are available: Teletext sixel mosaics (2×3 block graphics), PETSCII semigraphics (C64-style shapes), CP437 density ramp (IBM PC ASCII art characters), and Braille dot patterns (2×4 dot matrix). All glyphs are 8×8 pixels stored as synthesis-time constants — no BRAM is consumed by the font data. A single BRAM stores per-column luma samples and source color values for the character mapping process.

The name references the **Teletext** broadcast data service that transmitted pages of blocky text graphics alongside analog television signals throughout Europe from the 1970s onward. In that system, character cells on screen were selected by data codes embedded in the vertical blanking interval — a grid of glyphs painted over the broadcast image. Teletext does something analogous: it *reads* the video image and *writes* it back as a grid of typographic symbols.

---

## Background

### Character Cell Graphics

Before pixel-addressable frame buffers became affordable, home computers and broadcast systems displayed information using **character cell graphics** — a fixed grid of small tiles, each showing one glyph from a built-in ROM. The Commodore 64's PETSCII character set included geometric shapes (triangles, circles, diagonal lines) alongside letters, enabling surprisingly detailed artwork within the 40×25 character grid. The IBM PC's CP437 code page included block-shading characters (░▒▓█) used extensively in DOS-era user interfaces and ANSI art. Teletext broadcast services used 2×3 sixel mosaics — each character position divided into six sub-blocks that could be independently filled or empty, producing 64 possible patterns.

### Density-Sorted Glyph Mapping

The key to converting a continuous-tone image into character art is **density sorting**: arranging glyphs in order from empty (fewest lit pixels) to full (all pixels lit). When the source luminance is quantized to match the number of available glyphs, each brightness level maps directly to a glyph of matching visual density. Dark regions get sparse glyphs (periods, dots), bright regions get dense glyphs (full blocks, dense cross-hatching). Viewed from a distance, the varying density of the character grid reconstructs the tonal structure of the original image.

### The Sixel System

The Teletext sixel mosaic divides each 8×8 character cell into a 2×3 grid of rectangular sub-blocks — six blocks total. Each block is either filled or empty, giving $2^6 = 64$ possible patterns. When sorted by the number of filled blocks (density), these 64 patterns form a remarkably smooth tonal ramp from white (no blocks filled) to black (all six filled). Teletext uses a curated selection of sixteen of these patterns, ordered by visual density, to provide a practical working range for luminance mapping.

### Braille as a Display Medium

Unicode Braille patterns encode information in a 2×4 dot matrix per character cell. Each of the eight dot positions can be raised or lowered, giving $2^8 = 256$ possible patterns. When sorted by the number of raised dots, these patterns create an extremely fine-grained density ramp — finer than any of the other three character sets. Teletext's Braille mode uses sixteen density-sorted selections from this space, producing a delicate pointillist texture quite different from the bold block shapes of the other fonts.

### Source Color Mode

Most classic character-cell systems used a single foreground color (green phosphor, amber phosphor, or white) against a uniform background. Teletext's Source Color mode breaks from this tradition: instead of applying a fixed foreground hue, it samples the source video's U and V chroma components at the center of each character cell and uses those values to color the rendered glyphs. The result resembles an ANSI art terminal displaying colored text — character shapes rendered in the hues of the original video content.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Contrast Curve ─────────────────────────────────────────────
│   └─ Scale luma deviation from midpoint (shift-add)
│
├── Cell Grid Counter ──────────────────────────────────────────
│   ├─ Divide screen into cells (8 sizes: 4 to 20 pixels)
│   ├─ Track sub-position within cell (x, y)
│   └─ Sample luma + U/V at cell center → column BRAM
│
├── Stage 1: Glyph Index ──────────────────────────────────────
│   ├─ Quantize sampled luma → 16-level glyph index
│   ├─ Optional invert (15 − index)
│   └─ Sub-position → 8×8 glyph coordinate via remap ROM
│
├── Stage 2: ROM Lookup ────────────────────────────────────────
│   ├─ Select font: Teletext / PETSCII / CP437 / Braille
│   ├─ Address = glyph_index × 8 + row
│   └─ Extract column bit → pixel_on
│
├── Stage 3: Color Composite ───────────────────────────────────
│   ├─ pixel_on=1 → foreground (Fg Luma + Fg Hue or source UV)
│   └─ pixel_on=0 → background (Bg Luma + Bg Hue or source UV)
│
├── Mix (interpolator_u × 3) ──────────────────────────────────
│   └─ Crossfade between dry input and processed output
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical interaction is between the **contrast curve** and the **glyph index quantizer**. The contrast parameter scales the deviation of each pixel's luma from midpoint (512) before the value is sampled into the column BRAM. Higher contrast spreads the luma range, causing more of the sixteen glyph levels to be used. Lower contrast compresses the range toward the center, so fewer distinct glyphs appear — the image becomes flatter and more uniform. The source color mode adds a second data path: U and V samples are stored alongside luma in per-column buffers, then applied to the rendered glyph pixels in place of the fixed foreground hue.

---

## Parameter Reference

<img src={teletext_control_panel} alt="Videomancer front panel with Teletext loaded"/>
*Videomancer's front panel with Teletext active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 2 |

Selects one of eight character cell sizes: 4×4, 6×6, 8×8, 10×10, 12×12, 14×14, 16×16, and 20×20 pixels. Smaller cells produce finer character grids with more detail but less readable individual glyphs. Larger cells produce bolder, more legible characters but with less spatial resolution. At the smallest setting (4×4), the screen contains roughly 480×270 character cells in HD — fine enough to reproduce recognizable faces. At the largest setting (20×20), the grid is approximately 96×54 cells, creating large blocky mosaic tiles.

---

#### Knob 2 — Fg Luma
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Sets the luminance of the foreground — the brightness of the glyph pixels themselves. At 100%, glyphs are rendered at full white. At 0%, glyph pixels are black, making the characters invisible against a dark background. The foreground luma interacts with the source color toggle: in fixed mode, this pot directly controls character brightness. In video mode, the source luma is used instead, and this pot has no visible effect on the foreground channel.

---

#### Knob 3 — Fg Hue
| Property | Value |
|----------|-------|
| Range | -180° – 180° |
| Default | 0° |
| Suffix | ° |

Controls the foreground chroma hue angle. The 10-bit register is mapped through a quadrant-based triangle-wave approximation of the color circle, producing U and V offsets from the neutral center (512). At the center position, the foreground is achromatic (pure gray/white). Sweeping the pot cycles through colored foregrounds — green, cyan, blue, magenta, red, yellow — allowing the character grid to be rendered in any hue. Only active when Source Color is set to Fixed.

---

#### Knob 4 — Bg Luma
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the luminance of the background — the brightness of the space between and behind glyphs. At 0%, the background is pure black, creating high-contrast white-on-black text. At 100%, the background is full white, creating black-on-white text (when combined with a dark foreground). Setting foreground and background luma to similar values reduces contrast and makes the character structure subtle.

---

#### Knob 5 — Bg Hue
| Property | Value |
|----------|-------|
| Range | -180° – 180° |
| Default | 0° |
| Suffix | ° |

Controls the background chroma hue angle using the same quadrant-based color circle mapping as the foreground hue pot. This allows colored paper — amber, green, blue — behind the character grid. Combining colored foreground and background hues creates the look of vintage terminal displays: green characters on dark green, amber text on black, or white text on deep blue.

---

#### Knob 6 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Pre-quantization contrast curve applied to the source luma before character mapping. The VHDL implements a shift-add approximation: the deviation of each pixel from midpoint (512) is scaled by the top three bits of the contrast register. Higher contrast spreads the tonal range, engaging more of the sixteen density levels and producing greater glyph variety. Lower contrast compresses the range, causing most cells to map to similar mid-density glyphs. At minimum, the image appears as a nearly uniform field of the same character.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Charset Lo** | 0 | 1 |
| **8 — Charset Hi** | 0 | 1 |
| **9 — Invert** | Off | On |
| **10 — Source Color** | Fixed | Video |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a 2-bit charset selector (bit 0 and bit 1 respectively), choosing among four font ROMs. Toggle 9 inverts the glyph density mapping. Toggle 10 switches between fixed-color and source-color rendering. Toggle 11 bypasses all processing. Unlike programs with independent toggle actions, the charset selection here requires both toggles to be considered together as a combined binary value.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input video and the processed character-art output. At 100%, the output is entirely the rendered character grid. At 0%, the original video passes through unchanged. Intermediate values blend the two, creating a ghostly overlay of text characters on top of the source image — useful for subtle texturing effects where the character structure is visible but the source content dominates.

---

## Guided Exercises

These exercises progress from basic character rendering to advanced color and contrast techniques. Each builds on the previous, introducing new controls and interactions.

### Exercise 1: Classic Terminal Text

<img src={teletext_exercise1_result} alt="Classic Terminal Text result"/>
*Classic Terminal Text — simulated result across source images.*
**Source**: A well-lit portrait or still life with clear tonal separation.

**Objective**: Learn the basics of cell size, font selection, and foreground/background color to create a classic green-screen terminal look.

1. **Set cell size**: Start at size index 2 (8×8 cells) for a balance of detail and readability.
2. **Green terminal**: Set Fg Luma to ~80%, Fg Hue to ~120° (green), Bg Luma to ~5%, Bg Hue to ~120° (dark green).
3. **Fonts**: Cycle through the four character sets using Charset Lo and Charset Hi. Note how Teletext sixels create bold mosaic blocks while Braille creates a fine pointillist texture.
4. **Contrast**: Sweep the Contrast knob. At low values, the image flattens to a uniform character. At high values, all sixteen density levels are active.
5. **Inversion**: Toggle Invert to see the negative version — bright areas become sparse characters.

**Key concepts**: Cell size determines spatial resolution, charset selection changes visual texture, contrast controls how many glyph density levels are active

---

### Exercise 2: ANSI Art Color Mode

<img src={teletext_exercise2_result} alt="ANSI Art Color Mode result"/>
*ANSI Art Color Mode — simulated result across source images.*
**Source**: Brightly colored footage — flowers, graffiti, or animated graphics with saturated hues.

**Objective**: Explore the Source Color mode to create full-color character-art renderings that inherit the hues of the source video.

1. **Base setup**: Cell Size index 3 (10×10), Contrast ~60%.
2. **Enable source color**: Flip Source Color toggle to Video. Each character cell now inherits the hue of the source video.
3. **Font exploration**: Try CP437 (Charset Lo=0, Hi=1) for the classic DOS look, then PETSCII (Lo=1, Hi=0) for geometric blocks.
4. **Large cells**: Increase Cell Size to index 6 (16×16). The color mapping becomes bolder — each cell is a single solid hue.
5. **Mix blend**: Lower Mix to ~50% to overlay the character grid semi-transparently on the source.

**Key concepts**: Source color mode samples U/V per cell center, larger cells produce bolder monochromatic tiles, mix allows overlay blending

---

### Exercise 3: Braille Pointillism

<img src={teletext_exercise3_result} alt="Braille Pointillism result"/>
*Braille Pointillism — simulated result across source images.*
**Source**: A high-contrast black-and-white image or footage with strong graphic shapes.

**Objective**: Use the Braille character set with small cell sizes to create a fine-grained pointillist rendering.

1. **Braille mode**: Set Charset Lo=1, Charset Hi=1 to select the Braille dot pattern font.
2. **Fine grid**: Set Cell Size to index 0 (4×4). The screen fills with thousands of tiny dot clusters.
3. **High contrast**: Set Contrast to ~90% to spread across all sixteen density levels.
4. **White on black**: Fg Luma=100%, Bg Luma=0%, both hues neutral.
5. **Invert**: Toggle Invert to see how the dot density relationship reverses — bright becomes sparse, dark becomes dense.
6. **Scale up**: Gradually increase Cell Size to watch the dot patterns grow from a fine texture into individually visible Braille cells.

**Key concepts**: Braille patterns provide the finest density graduation, small cell sizes create near-photographic detail in text, inversion reverses the entire tonal mapping

---


## Tips

- **Start with high contrast**: Set Contrast to ~70% or higher to see the full range of sixteen glyph densities. Low contrast compresses everything into a few similar characters.
- **Cell size vs. detail trade-off**: Smaller cells (4×4, 6×6) reproduce more image detail but individual glyphs become illegible. Larger cells (16×16, 20×20) produce bold, readable characters but lose fine spatial information.
- **Font personality**: Teletext sixels produce geometric mosaics. PETSCII creates diagonal-heavy compositions. CP437 gives the classic DOS ANSI art look. Braille produces delicate pointillist textures. Choose the font that matches your aesthetic intent.
- **Source color for live performance**: Video mode inherits the hue of whatever is on camera, making the character-art output respond to colored lighting changes in real time.
- **Feedback loops**: Route the output back to the input for recursive character rendering — characters made of characters. Use moderate Mix values to prevent the image from collapsing to a uniform field.
- **Background hue for atmosphere**: Colored backgrounds create the feel of vintage terminals — green phosphor, amber CRT, or blue mainframe screens.
- **Mix for texture overlay**: At 30–50% mix, the character grid becomes a subtle texture over the source video rather than a full replacement.

---

## Glossary

| Term | Definition |
|------|------------|
| **Braille** | A tactile writing system using raised dot patterns in a 2×4 matrix, repurposed here as a fine-grained display font. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **Cell** | A rectangular region of the screen grid mapped to a single character glyph. |
| **CP437** | Code Page 437; the original IBM PC character set including block-shading characters (░▒▓█). |
| **Density sorting** | Ordering glyphs from fewest lit pixels (sparse) to most lit pixels (dense) for luminance mapping. |
| **Glyph** | A single character bitmap (8×8 pixels) from the font ROM. |
| **PETSCII** | The Commodore 64 character set, including geometric shapes and semigraphic blocks. |
| **Sixel** | A 2×3 grid of sub-blocks within a character cell; the fundamental building block of Teletext mosaic graphics. |
| **Source Color** | A rendering mode that inherits the hue of the input video per cell, rather than using a fixed foreground color. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
