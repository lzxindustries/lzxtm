---
draft: true
sidebar_position: 178
slug: /instruments/videomancer/loadstar
title: "Loadstar"
image: /img/instruments/videomancer/loadstar/loadstar_hero_s1.png
description: "There was a ritual shared by an entire generation of home computer users."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import loadstar_control_panel from '/img/instruments/videomancer/loadstar/loadstar_control_panel.png';
import loadstar_source1_fruit from '/img/instruments/videomancer/loadstar/loadstar_source1_fruit.png';
import loadstar_source2_boat from '/img/instruments/videomancer/loadstar/loadstar_source2_boat.png';
import loadstar_source3_clouds from '/img/instruments/videomancer/loadstar/loadstar_source3_clouds.png';
import loadstar_source4_pattern from '/img/instruments/videomancer/loadstar/loadstar_source4_pattern.png';
import loadstar_source5_man from '/img/instruments/videomancer/loadstar/loadstar_source5_man.png';
import loadstar_source6_berries from '/img/instruments/videomancer/loadstar/loadstar_source6_berries.png';
import loadstar_hero_s1 from '/img/instruments/videomancer/loadstar/loadstar_hero_s1.png';
import loadstar_hero_s2 from '/img/instruments/videomancer/loadstar/loadstar_hero_s2.png';
import loadstar_hero_s3 from '/img/instruments/videomancer/loadstar/loadstar_hero_s3.png';
import loadstar_hero_s4 from '/img/instruments/videomancer/loadstar/loadstar_hero_s4.png';
import loadstar_hero_s5 from '/img/instruments/videomancer/loadstar/loadstar_hero_s5.png';
import loadstar_hero_s6 from '/img/instruments/videomancer/loadstar/loadstar_hero_s6.png';
import loadstar_ex1_s1 from '/img/instruments/videomancer/loadstar/loadstar_ex1_s1.png';
import loadstar_ex1_s2 from '/img/instruments/videomancer/loadstar/loadstar_ex1_s2.png';
import loadstar_ex1_s3 from '/img/instruments/videomancer/loadstar/loadstar_ex1_s3.png';
import loadstar_ex1_s4 from '/img/instruments/videomancer/loadstar/loadstar_ex1_s4.png';
import loadstar_ex1_s5 from '/img/instruments/videomancer/loadstar/loadstar_ex1_s5.png';
import loadstar_ex1_s6 from '/img/instruments/videomancer/loadstar/loadstar_ex1_s6.png';
import loadstar_ex2_s1 from '/img/instruments/videomancer/loadstar/loadstar_ex2_s1.png';
import loadstar_ex2_s2 from '/img/instruments/videomancer/loadstar/loadstar_ex2_s2.png';
import loadstar_ex2_s3 from '/img/instruments/videomancer/loadstar/loadstar_ex2_s3.png';
import loadstar_ex2_s4 from '/img/instruments/videomancer/loadstar/loadstar_ex2_s4.png';
import loadstar_ex2_s5 from '/img/instruments/videomancer/loadstar/loadstar_ex2_s5.png';
import loadstar_ex2_s6 from '/img/instruments/videomancer/loadstar/loadstar_ex2_s6.png';
import loadstar_ex3_s1 from '/img/instruments/videomancer/loadstar/loadstar_ex3_s1.png';
import loadstar_ex3_s2 from '/img/instruments/videomancer/loadstar/loadstar_ex3_s2.png';
import loadstar_ex3_s3 from '/img/instruments/videomancer/loadstar/loadstar_ex3_s3.png';
import loadstar_ex3_s4 from '/img/instruments/videomancer/loadstar/loadstar_ex3_s4.png';
import loadstar_ex3_s5 from '/img/instruments/videomancer/loadstar/loadstar_ex3_s5.png';
import loadstar_ex3_s6 from '/img/instruments/videomancer/loadstar/loadstar_ex3_s6.png';

# Loadstar

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: loadstar_source1_fruit, after: loadstar_hero_s1 },
    { label: "Boat", before: loadstar_source2_boat, after: loadstar_hero_s2 },
    { label: "Clouds", before: loadstar_source3_clouds, after: loadstar_hero_s3 },
    { label: "Pattern", before: loadstar_source4_pattern, after: loadstar_hero_s4 },
    { label: "Man", before: loadstar_source5_man, after: loadstar_hero_s5 },
    { label: "Berries", before: loadstar_source6_berries, after: loadstar_hero_s6 },
  ]}
/>
*Loadstar applying animated border color cycling and attribute clash quantization to recreate the look of an 8-bit home computer loading screen.*

---

## Overview

There was a ritual shared by an entire generation of home computer users. You pressed play on the cassette deck, typed LOAD, and waited. While the machine's tape interface screamed and chirped, the screen border flickered through a hypnotic sequence of colors — a side effect of the loading protocol toggling I/O lines that happened to be mapped to the border color register. On the ZX Spectrum, the border strobed through all eight palette colors in rapid succession. On the Commodore 64, it cycled more slowly. Either way, the flashing border became the visual signature of the loading process — an accidental light show that an entire generation associates with anticipation.

Loadstar recreates this experience as a video processing effect. The program divides the screen into a border region and a content area. The border cycles through a palette of synthetic colors at a user-controlled speed, emulating the tape-loading animation. Within the content area, the input video is quantized into character cells — rectangular blocks that sample and hold a single brightness value, exactly as an 8-bit computer's text mode display would render graphics. The Attr Clash toggle applies the most infamous limitation of 1980s display hardware: restricting each character cell to a single color from an eight-level palette, producing the characteristic "attribute clash" where fine detail is lost to block-level color quantization.

This is an early prototype with four of six potentiometers and one toggle unused. The active controls — Border Spd, Cell Size, Border Flash, Attr Clash, Interlace, and Mix — are sufficient to produce convincing retro-computing aesthetics, but the full vision of the program (character set rendering, brightness/contrast adjustment, color cycling within the content area) remains unimplemented.

---

## Quick Start

1. **Border Flash is the signature**: The animated border color cycling is the program's most distinctive effect. It creates an instant nostalgia trigger for anyone who grew up with 8-bit computers.
2. **Attr Clash creates the retro look**: Without attribute clash, the cell quantization is subtle. With it enabled, the eight-color palette restriction dominates the image and creates the authentic ZX Spectrum aesthetic.
3. **Cell Size matters**: Smaller cells (4–5 px) produce a subtle texture overlay. Larger cells (9–11 px) produce a dramatic mosaic. Match the cell size to the viewing distance — larger displays benefit from larger cells.

---

## Background

### The Tape Loading Border Effect

When a ZX Spectrum loaded data from cassette tape, the CPU interpreted the audio signal by monitoring the state of a single I/O port. Each bit transition toggled the border color register as a side effect of the decoding algorithm. The result was a rapid, seemingly random sequence of color changes — cyan, red, blue, yellow — that strobed across the screen border at audio frequency rates. Users quickly learned to read these patterns: steady alternation meant good data; erratic flashing meant a loading error. The Commodore 64 had a similar effect, though its border color changes were driven by different mechanisms. Loadstar abstracts this into a simple counter-based animation: every vertical sync, the border color advances by an increment derived from the Border Spd parameter, cycling through a palette of synthetic hues.

### Character Cells and Text Mode Graphics

Early home computers could not afford enough memory for a full bitmap display. Instead, they divided the screen into a grid of character cells — typically 8×8 pixels — and stored only a character code and color attribute for each cell. This meant that within any single cell, all pixels shared the same foreground and background colors. To display graphics, programmers either designed custom character sets that approximated shapes, or accepted the blocky limitations of the text mode. Loadstar emulates this by dividing the screen into cells of configurable width (4–11 pixels) and sample-and-holding the input luma at the start of each cell. Every pixel within the cell displays the same brightness, producing the characteristic blocky appearance.

### Attribute Clash

The ZX Spectrum's most notorious display limitation was attribute clash (sometimes called "colour clash" or "attribute bleed"). The Spectrum stored one foreground and one background color per 8×8 character cell — just two colors shared by all 64 pixels in the cell. When a sprite or graphic moved across a cell boundary, it was forced to adopt the color attribute of the cell it entered, causing bright objects to suddenly change color as they crossed the invisible grid. Game developers spent enormous effort working around this limitation — designing monochrome games, keeping sprites on cell boundaries, or embracing the clash as a stylistic feature. Loadstar's Attr Clash toggle applies a similar quantization: the held luma value is reduced to three bits (eight levels), and chroma is forced to neutral. The result is an eight-color palette constrained per cell.

### Interlace and CRT Simulation

Home computers of the 1980s displayed their output on cathode ray tube televisions. The CRT's electron beam scanned alternate lines on successive fields, and the inherent phosphor persistence and beam width created a characteristic visual texture where odd and even scan lines were not equally bright. Loadstar's Interlace toggle approximates this by dimming every other scan line — halving the luma of odd-numbered lines. The effect is subtle on its own but adds an authentic CRT quality when combined with cell quantization and attribute clash.

### LFSR Hashing for Per-Cell Color

In the VHDL implementation, the held luma sample at the start of each cell is used as a hash input to derive a three-bit color index. The top three bits of the held luminance value directly determine which of eight palette levels the cell receives. This is not a true LFSR hash but rather a simple truncation that maps the continuous luminance range into eight coarse buckets. The mapping is deterministic — the same input brightness always produces the same cell color — but because the input video varies spatially, the result looks like a mosaic of pseudo-randomly assigned colors across the screen.


---

## Signal Flow

Clock 1: Sync Edge → Clock 2: Cell Tracking → Clock 3: Border Detection → ... → Sync Delay → Output Mux

```
Input Video (YUV 4:4:4)
│
├── Clock 1: Sync Edge Detection ───────────────────────────────
│   ├─ Detect falling edge of hsync_n → reset x_counter
│   ├─ Detect falling edge of vsync_n → reset y_counter
│   └─ Increment frame_counter, update border_color
│
├── Clock 2: Cell Tracking ─────────────────────────────────────
│   ├─ v_cell_w = cell_size(9:7) + 4  (cell width: 4..11 px)
│   ├─ Track local_x within cell, cell_x across line
│   └─ Sample-and-hold: latch data_in.y at cell boundary
│
├── Clock 3: Border Detection ──────────────────────────────────
│   └─ v_in_border = 1 if x<48 or x>1232 or y<36 or y>684
│
├── Clock 4: Color Assignment ──────────────────────────────────
│   ├─ Border region → animated border color (Y, U, V)
│   ├─ Attr Clash on → quantized 3-bit Y, neutral U/V
│   └─ Attr Clash off → passthrough input Y, U, V
│
├── Clock 5: Interlace Dimming ─────────────────────────────────
│   └─ If interlace on and odd line → Y >>= 1
│
├── Clocks 5–8: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(delayed_input, processed, mix_amount) per channel
│
├── Sync Delay (8 clocks) ──────────────────────────────────────
│   └─ Shift registers for hsync, vsync, field, Y, U, V
│
└── Output Mux ─────────────────────────────────────────────────
    ├─ Bypass off → mixed output
    └─ Bypass on  → delayed input
```

The pipeline does not instantiate a `video_timing_generator` entity. Instead, it manually detects hsync and vsync falling edges to track pixel position using 12-bit x and y counters. The cell tracking logic uses modular arithmetic — a local counter `s_local_x` counts pixels within the current cell and resets when it reaches the cell width, at which point the held luma value is updated. The border region is defined by fixed pixel coordinate thresholds (x range 48–1232, y range 36–684), creating a border frame approximately 48 pixels wide on each side. Four of the six potentiometer registers (`s_color_depth`, `s_charset`, `s_brightness`, `s_contrast`) and one toggle (`s_color_cycle`) are registered but never referenced in the processing pipeline — they are reserved for future implementation.

---

## Parameter Reference

<img src={loadstar_control_panel} alt="Videomancer front panel with Loadstar loaded"/>
*Videomancer's front panel with Loadstar active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Border Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Border cycling speed. Controls how fast the border color advances per frame. The speed is derived from bits 9:7 of the register plus 1, giving an increment range of 1–8 per vertical sync. At minimum, the border color changes slowly — one palette step per frame. At maximum, it advances eight steps per frame, producing a rapid strobe that closely resembles the ZX Spectrum's tape loading animation. The effect is only visible when Border Flash is enabled.

---

#### Knob 2 — Cell Size
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

Character cell width. The register value is quantized to eight steps — the top three bits plus four give a cell width of 4 to 11 pixels. At the minimum (4 pixels), cells are narrow and the sample-and-hold effect is subtle. At the maximum (11 pixels), cells are wide and the blocky character-cell appearance is pronounced. The cell height is not independently controllable — vertical quantization is achieved only through interlace dimming, not through vertical sample-and-hold.

---

#### Knob 3 — Color Depth
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

Color Depth — currently unused. The register is read and stored in `s_color_depth` but never referenced in the processing pipeline. Reserved for future implementation of variable color palette depth.

---

#### Knob 4 — Charset
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Charset — currently unused. The register is read and stored in `s_charset` but never referenced. Reserved for future implementation of character set overlay rendering.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

Brightness — currently unused. The register is read and stored in `s_brightness` but never referenced. Reserved for future implementation of a brightness offset stage.

---

#### Knob 6 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Contrast — currently unused. The register is read and stored in `s_contrast` but never referenced. Reserved for future implementation of a contrast gain stage.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Border Flash** | Off | On |
| **8 — Color Cycle** | Off | On |
| **9 — Attr Clash** | Off | On |
| **10 — Interlace** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five binary options. Only three are actively wired into the processing pipeline — Border Flash, Attr Clash, and Interlace. The Color Cycle toggle (Switch 8) is registered but has no effect on the output. Bypass (Switch 11) is the standard signal routing switch. The active toggles are independent: each controls a different stage of the pipeline with no interaction between them.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry mix crossfade. At 0%, only the delayed dry input is passed through. At 100%, the fully processed signal (border animation, cell quantization, attribute clash, interlace) is output. Intermediate values blend the two proportionally, allowing subtle application of the retro effect over the clean source.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore the program's active controls, progressing from simple border animation to full 8-bit display emulation. The unused controls (Color Depth, Charset, Brightness, Contrast, Color Cycle) are left at their defaults throughout.

### Exercise 1: Tape Loading Border

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: loadstar_source1_fruit, after: loadstar_ex1_s1 },
    { label: "Boat", before: loadstar_source2_boat, after: loadstar_ex1_s2 },
    { label: "Clouds", before: loadstar_source3_clouds, after: loadstar_ex1_s3 },
    { label: "Pattern", before: loadstar_source4_pattern, after: loadstar_ex1_s4 },
    { label: "Man", before: loadstar_source5_man, after: loadstar_ex1_s5 },
    { label: "Berries", before: loadstar_source6_berries, after: loadstar_ex1_s6 },
  ]}
/>
*Tape Loading Border — simulated result across source images.*
**Source**: Any video source — the border effect is independent of the content area.

**What You'll Create**: Recreate the classic tape-loading border strobe from 8-bit home computers.

1. **Enable Border Flash**: Turn on Switch 7. The border region immediately begins cycling through colors.
2. **Slow strobe**: Set Border Spd to minimum. The border color changes once per frame — a slow, deliberate pulse.
3. **Fast strobe**: Increase Border Spd toward maximum. The border flashes rapidly through the palette, closely approximating the ZX Spectrum's loading animation.
4. **A/B compare**: Toggle Bypass (Switch 11) to see the unprocessed signal, then back to see the border effect.
5. **Mix blend**: Reduce Mix to ~50% to see the border animation blended with the clean border area.

**Key concepts**: Border color is a 4-bit counter incremented per frame, speed is derived from top 3 register bits plus 1, effect is gated by the Border Flash toggle

---

### Exercise 2: Character Cell Mosaic

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: loadstar_source1_fruit, after: loadstar_ex2_s1 },
    { label: "Boat", before: loadstar_source2_boat, after: loadstar_ex2_s2 },
    { label: "Clouds", before: loadstar_source3_clouds, after: loadstar_ex2_s3 },
    { label: "Pattern", before: loadstar_source4_pattern, after: loadstar_ex2_s4 },
    { label: "Man", before: loadstar_source5_man, after: loadstar_ex2_s5 },
    { label: "Berries", before: loadstar_source6_berries, after: loadstar_ex2_s6 },
  ]}
/>
*Character Cell Mosaic — simulated result across source images.*
**Source**: Live camera or footage with recognizable subjects — faces, text, or geometric patterns.

**What You'll Create**: Explore the cell-based sample-and-hold quantization and attribute clash.

1. **Enable Attr Clash**: Turn on Switch 9. The content area is immediately quantized to eight brightness levels with no color.
2. **Small cells**: Set Cell Size to step 1 (minimum). The quantization is subtle — narrow 4-pixel cells retain much spatial detail.
3. **Large cells**: Increase Cell Size to step 8 (maximum). The image becomes a coarse mosaic of 11-pixel-wide blocks, each holding a single brightness level.
4. **Without Attr Clash**: Turn off Switch 9. The same cell structure is visible (sample-and-hold luma) but with full brightness resolution and preserved chroma.
5. **Add Interlace**: Turn on Switch 10. Alternate scan lines dim, adding CRT texture to the mosaic.
6. **Add Border Flash**: Turn on Switch 7 with Border Spd at ~50%. The border flashes while the content area displays the cell mosaic.

**Key concepts**: Cell width is quantized to 8 steps (4–11 pixels), attribute clash reduces luma to 3 bits and kills chroma, interlace dims odd lines

---

### Exercise 3: Full 8-Bit Emulation

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: loadstar_source1_fruit, after: loadstar_ex3_s1 },
    { label: "Boat", before: loadstar_source2_boat, after: loadstar_ex3_s2 },
    { label: "Clouds", before: loadstar_source3_clouds, after: loadstar_ex3_s3 },
    { label: "Pattern", before: loadstar_source4_pattern, after: loadstar_ex3_s4 },
    { label: "Man", before: loadstar_source5_man, after: loadstar_ex3_s5 },
    { label: "Berries", before: loadstar_source6_berries, after: loadstar_ex3_s6 },
  ]}
/>
*Full 8-Bit Emulation — simulated result across source images.*
**Source**: High-contrast footage — retro games, pixel art, or text-heavy material for maximum authenticity.

**What You'll Create**: Combine all active effects for a complete 8-bit home computer display simulation.

1. **Set up cell grid**: Cell Size to step 5–6 (moderate blocks). Enable Attr Clash.
2. **Add scan lines**: Enable Interlace for CRT texture.
3. **Add border strobe**: Enable Border Flash. Set Border Spd to ~60% for a medium-speed cycling rate.
4. **Mix adjustment**: Reduce Mix to ~85% for a subtle blend that lets some original detail show through the retro effect.
5. **Observe cell boundaries**: Watch how moving subjects cause attribute clash as their brightness changes the quantized cell color — exactly as sprites moving across cell boundaries on a ZX Spectrum.
6. **Speed variation**: Sweep Border Spd from minimum to maximum while watching the border. Find the speed that most closely matches your memory of loading a game from tape.

**Key concepts**: The combination of cell quantization, attribute clash, interlace dimming, and border animation recreates the full visual experience of an 8-bit display, four unused controls remain for future expansion

---


## Tips

- **Interlace adds depth**: The scan line dimming is subtle but essential for CRT authenticity. It works best in combination with attribute clash, where the alternating bright/dim lines break up the flat cell blocks.
- **Unused controls are safe to ignore**: Four potentiometers and one toggle are wired but inert. Move them freely — they have no effect on the output.
- **Mix for subtlety**: At 100% mix, the retro effect is total. At 50–70%, the original image shows through the cell grid, creating a ghostly overlay effect that suggests a computer display composited over live video.
- **Feedback routing**: Sending the output back to the input creates recursive cell quantization — each pass reduces the image further toward the eight-color palette, eventually converging to a stable mosaic.

---

## Glossary

| Term | Definition |
|------|------------|
| **Attribute Clash** | A display limitation of the ZX Spectrum where each 8×8 character cell could contain only two colors (foreground and background), causing color bleeding at cell boundaries when objects moved across them. |
| **Cell** | A rectangular block of pixels that shares a single brightness and color value, emulating the character cells of 8-bit text mode displays. |
| **Chroma** | The color information in a video signal, encoded as U and V components. Loadstar forces chroma to neutral (512, 512) in attribute clash mode. |
| **CRT** | Cathode Ray Tube; the display technology used by 8-bit home computers. Loadstar's interlace mode simulates the visible scan line structure of CRT displays. |
| **Interlace** | A scanning technique where alternate lines are drawn on successive fields. Loadstar approximates this by dimming odd-numbered lines. |
| **LFSR** | Linear Feedback Shift Register; a hardware pseudo-random number generator. Referenced in the VHDL header but not used in the current implementation. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Sample-and-Hold** | A technique where a signal value is captured (sampled) at a specific moment and held constant until the next sample point. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
