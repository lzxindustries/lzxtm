---
draft: true
sidebar_position: 283
slug: /instruments/videomancer/telex
title: "Telex"
image: /img/instruments/videomancer/telex/telex_hero.png
description: "Before screens, before pixels, there was the teleprinter — a machine that converted electrical signals into typed characters on a continuous roll of paper."
---

import telex_hero from '/img/instruments/videomancer/telex/telex_hero.png';
import telex_before_after from '/img/instruments/videomancer/telex/telex_before_after.png';
import telex_control_panel from '/img/instruments/videomancer/telex/telex_control_panel.png';
import telex_exercise1_result from '/img/instruments/videomancer/telex/telex_exercise1_result.png';
import telex_exercise2_result from '/img/instruments/videomancer/telex/telex_exercise2_result.png';
import telex_exercise3_result from '/img/instruments/videomancer/telex/telex_exercise3_result.png';

# Telex

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={telex_hero} alt="Telex hero image"/>
*Telex rendering live video as a Baudot teleprinter page — density-sorted 5×7 glyphs typed across the screen by a DDS-driven reveal cursor on colored paper.*
<img src={telex_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Telex applied.*

---

## Overview

Before screens, before pixels, there was the teleprinter — a machine that converted electrical signals into typed characters on a continuous roll of paper. Telex recreates this experience as a live video effect. Input video luminance is quantized to sixteen levels, each mapped to a density-sorted glyph from a built-in pattern ROM. The characters are rendered onto a virtual page with selectable paper colors — white bond, aged yellow, green-screen phosphor, or blue terminal — and printed by a DDS-driven cursor that advances left-to-right, top-to-bottom like a real teletype machine.

The program divides the screen into a grid of power-of-two sized cells (8×8, 16×16, 32×32, or 64×64 pixels). Each cell displays a 5×7 glyph selected by the source luminance at that position. The reveal animation creates the distinctive teleprinter experience: characters appear sequentially across the page at a rate controlled by the Baud Rate knob, as though printed by an unseen mechanical head. When all positions are filled, the Roll toggle can reset the cursor to start again.

The name **Telex** references the international teleprinter exchange network that connected businesses and governments from the 1930s through the 1990s. Telex machines transmitted text as 5-bit Baudot codes at 50 baud — roughly 6.7 characters per second — producing the characteristic slow-reveal rhythm that this program recreates visually.

---

## Background

### The Baudot Code

The Baudot code, invented by Émile Baudot in 1870 and later standardized as ITA2, uses just 5 bits to represent each character — enough for 32 symbols. By using a shift mechanism (LTRS and FIGS shift characters), the code expands to cover the full alphabet plus numerals and punctuation. Telex machines worldwide communicated using this code at speeds between 45.5 and 75 baud. The program's glyph ROM doesn't literally implement Baudot encoding, but its sixteen density-sorted patterns echo the limited character vocabulary of teleprinter systems — a small set of visual symbols doing maximum representational work.

### Teleprinter Typography

Physical teleprinters used fixed-width typefaces struck through an inked ribbon onto paper. Each character occupied the same horizontal space regardless of its shape, creating the distinctive monospaced grid that became a hallmark of computer output. Telex renders its glyphs at fixed pitch within the cell grid, maintaining this monospaced regularity. The 5×7 glyph matrix within each cell leaves a 1-pixel border on the right and bottom edges, creating the visual separation between characters that was inherent in physical type mechanisms.

### Paper as a Display Medium

Before CRT displays became common, the teleprinter's paper roll *was* the display. The paper color, weight, and condition communicated information about the environment: white bond paper for formal correspondence, yellow thermal paper for quick messages, green-bar paper for computer printouts, blue paper for carbon copies. Telex's four paper modes reference these physical media — each with distinct luminance and chrominance values that tint the background behind the character grid.

### DDS-Driven Sequential Reveal

Direct Digital Synthesis (DDS) provides a phase accumulator that advances at a programmable rate. In Telex, the DDS accumulator drives a cursor position that determines which characters have been "printed" on the page. Characters before the cursor are visible; characters after it remain blank (showing paper only). The Baud Rate knob controls the DDS increment, setting how quickly the cursor advances. At low baud rates, characters appear slowly — one every few frames — mimicking a sluggish mechanical printer. At high baud rates, the entire page fills almost instantly.

### Color Terminal Emulation

The four paper modes and two hue controls allow Telex to emulate a wide range of historical display technologies. White paper with dark ink recreates the printed page. Green paper with bright green ink recreates the early VT100 and IBM 3270 terminal aesthetic. Blue paper with white ink evokes mainframe console displays. Yellow "aged" paper creates a nostalgic, archival look — as though the teleprinter output has been stored in a folder for decades.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Parameter Latch ──────────────────
│   ├─ Latch all register parameters
│   ├─ Position counters (h_count, v_count)
│   └─ Cell scale derivation (8/16/32/64 from Char Size)
│
├── Stage 2: Grid Position + Glyph Index + Reveal ──────────────
│   ├─ Compute cell column/row from pixel position
│   ├─ Compute glyph sub-column/row via bit selection
│   ├─ Quantize source Y → 4-bit glyph index (16 levels)
│   │   └─ Contrast scaling applied before quantization
│   ├─ Check if pixel within 5×7 glyph area
│   └─ Compare cell position against reveal cursor
│
├── Stage 3: Glyph ROM Lookup ─────────────────────────────────
│   ├─ Address ROM: row data = C_G_Rn(glyph_index)
│   ├─ Extract column bit (bit 4 = column 0 leftmost)
│   └─ pixel_on = column_bit AND in_glyph AND revealed
│
├── Stage 4: Colour Composite ─────────────────────────────────
│   ├─ pixel_on=1 → ink colour (Ink Dens + Ink Hue)
│   └─ pixel_on=0 → paper colour (from Paper mode + Paper Hue)
│
├── Paper/Ink Colour Derivation ────────────────────────────────
│   ├─ Paper Y/U/V from paper_mode toggle (White/Yellow/Green/Blue)
│   ├─ Paper U tinted by Paper Hue parameter
│   ├─ Ink Y from Ink Dens parameter
│   └─ Ink U/V from Ink Hue parameter
│
├── Reveal Cursor (DDS) ────────────────────────────────────────
│   ├─ 24-bit accumulator advances per frame by Baud Rate
│   ├─ Bit 13 overflow → advance column
│   ├─ Column overflow → advance row
│   └─ Roll toggle → reset cursor when row wraps
│
├── Mix (interpolator_u × 3) ──────────────────────────────────
│   └─ Crossfade between dry input and processed output
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select original or processed signal
```

The reveal cursor and the glyph rendering operate independently. The glyph index is computed for every cell on every frame (based on current source luminance), but the colour composite stage only draws ink for cells where the reveal cursor has passed. This means the character content updates live even as the reveal animation progresses — if the source video changes, already-revealed characters update to reflect the new content. The contrast parameter affects glyph selection by scaling the source luma before quantization: higher contrast spreads values across more of the sixteen glyph levels, while lower contrast compresses them toward the middle densities.

---

## Parameter Reference

<img src={telex_control_panel} alt="Videomancer front panel with Telex loaded"/>
*Videomancer's front panel with Telex active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Baud Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the reveal animation speed via the DDS accumulator increment. At 0%, the cursor is nearly frozen — characters appear imperceptibly slowly. At higher values, the cursor advances faster, filling the page in seconds or less. The reveal advances left-to-right within each row, then wraps to the next row below — mimicking the carriage return and line feed of a physical teleprinter. At maximum, the page fills almost instantly and the sequential nature of the animation becomes barely perceptible.

---

#### Knob 2 — Char Size
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Selects one of four character cell sizes: 8×8, 16×16, 32×32, or 64×64 pixels. At 8×8, the screen accommodates 240×135 character cells in HD — a dense grid with fine detail. At 64×64, only about 30×17 cells fit — enormous block characters with very coarse spatial resolution. The cell size affects the reveal animation pacing: larger cells mean fewer total cells to fill, so the page fills faster at the same baud rate.

---

#### Knob 3 — Ink Dens
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the ink darkness — the luminance of glyph pixels. At 100%, ink is full white (bright characters on paper). At 0%, ink is black (invisible on dark paper, visible as dark marks on light paper). The ink density works with the Paper mode to create the desired contrast relationship: high ink on white paper creates light-on-light (low contrast), while high ink on dark paper (green or blue mode) creates the classic bright-on-dark terminal look.

---

#### Knob 4 — Paper Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Applies a chroma tint to the paper background. The 10-bit register is mapped to U/V offsets from the paper's base color. This allows fine-tuning of paper hue beyond the four discrete modes — adding warmth to white paper, shifting the green screen toward cyan, or tinting the blue terminal toward purple. The tinting is additive to the paper mode's base colour.

---

#### Knob 5 — Ink Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Controls the ink chroma hue. The register maps to U/V offsets that color the glyph pixels. At the neutral position, ink is achromatic (gray/white). Sweeping the pot shifts the ink through colored hues, enabling green-on-black, amber-on-black, or cyan-on-blue terminal aesthetics. Combined with the Paper Hue pot, this provides full control over the two-tone color scheme of the rendered page.

---

#### Knob 6 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Pre-quantization contrast scaling applied to the source luminance before glyph index computation. The VHDL uses contrast step thresholds to select between four quantization ranges: at high contrast, the full top-4-bit range of source luma maps across all sixteen glyph densities. At low contrast, only the top 2 bits are used, compressing the image into just four distinct glyph levels. This directly controls how many different characters appear in the rendered output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Charset** | Baudot | ASCII |
| **8 — Paper** | White | Yellow |
| **9 — Animate** | Off | On |
| **10 — Roll** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 are each 2-bit multi-value selectors packed into register bits — Toggle 7 selects among four charsets (bits 1:0) and Toggle 8 selects among four paper modes (bits 3:2). Toggles 9 and 10 are single-bit flags for animation and cursor rollover. Toggle 11 is the standard bypass. The non-standard multi-value toggle mapping means the physical switch positions cycle through four states rather than the usual two, using the TOML value_labels to name each position.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input and the processed teleprinter output. At 100%, the output is entirely the rendered character page. At 0%, the original video passes through unchanged. Intermediate values create a translucent overlay of the character grid on the source — the typing appears superimposed on the underlying video.

---

## Guided Exercises

These exercises progress from basic teleprinter output to animated reveals and vintage terminal aesthetics. Each explores a different aspect of the Telex rendering engine.

### Exercise 1: White Paper Teleprinter

<img src={telex_exercise1_result} alt="White Paper Teleprinter result"/>
*White Paper Teleprinter — simulated result across source images.*
**Source**: A high-contrast portrait or document scan with clear tonal separation.

**Objective**: Create a clean teleprinter printout on white paper with dark ink, resembling a physical teletype output.

1. **White paper**: Set Paper to White, Contrast to ~60%.
2. **Dark ink**: Set Ink Dens to ~20%, Ink Hue to neutral (center position).
3. **Cell size**: Set Char Size to step 2 (16×16) for readable characters.
4. **No animation**: Set Animate to Off to see all characters at once.
5. **Adjust contrast**: Sweep Contrast to control how many glyph densities appear.
6. **Paper tint**: Slightly nudge Paper Hue to add warmth for an aged-paper feel.

**Key concepts**: Ink density controls foreground brightness, paper mode sets background color, contrast controls glyph density distribution

---

### Exercise 2: Green Screen Terminal

<img src={telex_exercise2_result} alt="Green Screen Terminal result"/>
*Green Screen Terminal — simulated result across source images.*
**Source**: Abstract or geometric footage with strong graphic shapes.

**Objective**: Recreate the look of an early CRT terminal with bright green characters on a dark green background.

1. **Green paper**: Set Paper to Green.
2. **Bright green ink**: Set Ink Dens to ~90%, Ink Hue slightly green.
3. **Small cells**: Set Char Size to step 1 (8×8) for a dense character grid.
4. **Enable animation**: Turn Animate on. Watch characters type across the screen.
5. **Baud rate**: Sweep Baud Rate from low (slow typing) to high (rapid fill).
6. **Roll**: Enable Roll to create a continuously repeating print cycle.

**Key concepts**: Paper mode defines terminal background aesthetic, animation speed is DDS-driven, roll creates repeating cycle

---

### Exercise 3: Animated Typewriter Page Fill

<img src={telex_exercise3_result} alt="Animated Typewriter Page Fill result"/>
*Animated Typewriter Page Fill — simulated result across source images.*
**Source**: Slowly moving footage with evolving content — clouds, water, or time-lapse.

**Objective**: Use the reveal animation at a medium baud rate to create a typewriter effect where the page fills gradually, revealing the video content as characters.

1. **Yellow paper**: Set Paper to Yellow for an aged-document aesthetic.
2. **Dark ink**: Ink Dens ~30%, Ink Hue slightly warm.
3. **Large cells**: Char Size step 3 (32×32) for bold, easily visible character printing.
4. **Moderate baud**: Set Baud Rate to ~30% for visible character-by-character reveal.
5. **Observe**: Watch as characters appear left-to-right, row by row, revealing the video content.
6. **No roll**: Keep Roll off — let the page fill once and hold.
7. **Source changes**: Notice how already-revealed characters update their glyph as the source video changes.

**Key concepts**: DDS reveal is independent of glyph content, already-printed characters update live, slow baud rates create dramatic reveal effects

---


## Tips

- **Baud rate sets the mood**: Very low baud rates create dramatic, cinematic character-by-character reveals. High baud rates produce rapid page fills useful for live performance.
- **Paper mode is the fastest aesthetic change**: Switching between White, Yellow, Green, and Blue paper instantly transforms the entire visual character — from antique document to sci-fi terminal.
- **Cell size determines readability**: 8×8 cells create dense text that reads as texture from a distance. 32×32 and 64×64 cells create bold, individually distinguishable character blocks.
- **Contrast is the key to glyph variety**: If the output looks too uniform (all cells showing similar characters), increase Contrast to spread the luma range across more glyph density levels.
- **Live content updates through reveal**: Already-revealed characters update their glyph in real time as the source video changes. The reveal animation only controls visibility, not content.
- **Ink Hue + Paper mode for terminal aesthetics**: Green ink on Green paper = VT100. White ink on Blue paper = IBM mainframe. Dark ink on White paper = printed page. Amber ink on dark background = vintage Wyse terminal.
- **Roll for continuous animation**: Enable both Animate and Roll for a perpetually cycling print sequence — useful as a continuously evolving visual element in live performance.
- **Mix overlay for subtle texture**: At 20–40% mix, the character grid becomes a subtle typographic texture overlaid on the source video.

---

## Glossary

| Term | Definition |
|------|------------|
| **Baud rate** | The number of signal changes per second in a communication channel; in Telex, controls the DDS-driven reveal speed. |
| **Baudot** | A 5-bit character encoding system invented in 1870, used by teleprinter networks worldwide until digital communications replaced them. |
| **DDS** | Direct Digital Synthesis; a phase accumulator technique used here to generate a programmable-rate cursor advance. |
| **Glyph** | A single character pattern (5×7 pixels within a cell) from the built-in pattern ROM. |
| **Ink** | The foreground colour applied to glyph pixels (where the bit pattern is set). |
| **ITA2** | International Telegraph Alphabet No. 2; the international standard Baudot code used on Telex networks. |
| **Paper** | The background colour applied behind and between glyphs. |
| **Reveal cursor** | A DDS-driven position tracker that determines which character cells have been "printed" and are therefore visible. |
| **Teletype** | A teleprinter or teletypewriter; an electromechanical device that transmitted and received typed text over telegraph lines. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
