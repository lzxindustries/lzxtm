---
draft: true
sidebar_position: 208
slug: /instruments/videomancer/punchcard
title: "Punchcard"
image: /img/instruments/videomancer/punchcard/punchcard_hero.png
description: "Program guide for Punchcard, a Videomancer text program for the LZX video synthesizer."
---

import punchcard_before_after from '/img/instruments/videomancer/punchcard/punchcard_before_after.png';
import punchcard_control_panel from '/img/instruments/videomancer/punchcard/punchcard_control_panel.png';
import punchcard_exercise1_result from '/img/instruments/videomancer/punchcard/punchcard_exercise1_result.png';
import punchcard_exercise2_result from '/img/instruments/videomancer/punchcard/punchcard_exercise2_result.png';
import punchcard_exercise3_result from '/img/instruments/videomancer/punchcard/punchcard_exercise3_result.png';
import punchcard_hero from '/img/instruments/videomancer/punchcard/punchcard_hero.png';
import punchcard_source1_kodim15 from '/img/instruments/videomancer/punchcard/punchcard_source1_kodim15.png';
import punchcard_source2_kodim15_bw from '/img/instruments/videomancer/punchcard/punchcard_source2_kodim15_bw.png';
import punchcard_source3_male_1024 from '/img/instruments/videomancer/punchcard/punchcard_source3_male_1024.png';

# Punchcard

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={punchcard_hero} alt="Punchcard hero image"/>
*Punchcard rendering a luma-thresholded punch hole grid over source video with adjustable cell geometry and card stock overlay.*
<img src={punchcard_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Punchcard applied.*

---

## Overview

The IBM punched card — 80 columns, 12 rows, one character per column — was the dominant data storage medium from the 1920s through the 1970s. Each card encoded information by the *absence* of material: rectangular holes punched through stiff card stock, read by mechanical or optical sensors that detected light passing through. Punchcard brings this encoding metaphor to video: the frame is divided into a grid of rectangular cells, and each cell is classified as "punched" or "card stock" based on the source luminance at the cell boundary.

The program divides the screen into a power-of-2 cell grid (8×8 to 128×128 pixels per cell), samples the source luma at the left edge of each cell column, and compares it to a threshold. Where the luma exceeds the threshold, the cell is punched — a rectangular hole reveals the source video underneath. Where it falls below, the cell is filled with a flat "card stock" color (a configurable-brightness beige). An edge inset control creates bordered holes by shrinking the transparent region within each cell, and a density toggle halves the cell size for finer grids.

At large cell sizes and high contrast, the effect is a coarse binary interpretation of the image — large opaque rectangles of card stock separated by transparent punched windows. At small cell sizes with moderate thresholds, it becomes a textured grid overlay that reveals and conceals the source in a data-visualization pattern.

---

## Background

### The Hollerith Punch Card

Herman Hollerith's punched card system, developed for the 1890 United States Census, used the presence or absence of holes at specific grid positions to encode information. Each column represented a character, each row a possible value. The system was elegant in its simplicity: information was binary — hole or no hole — and could be read mechanically at high speed. IBM standardized the format at 80 columns × 12 rows with rectangular holes, and this format persisted essentially unchanged for 80 years.

### Spatial Quantization as Data Encoding

Punchcard implements a spatial version of the Hollerith concept. Instead of encoding alphanumeric data, it quantizes the video image into a grid of binary decisions: is this cell "bright enough" to punch? The threshold comparison converts continuous luminance into a one-bit representation per cell — the same information density as a single punch position on a physical card. The visual result resembles a data readout of the video content, with the underlying image visible through the punched holes.

### Power-of-Two Cell Sizing

The VHDL uses bit-masking rather than modular arithmetic to compute intra-cell positions, which restricts cell dimensions to powers of two (8, 16, 32, 64, 128 pixels). This is both a hardware optimization — bit extraction is free logic in an FPGA — and an aesthetic constraint that produces clean, evenly divisible grids. The density toggle subtracts one from the shift exponent, halving the cell size for a denser grid without changing the pot position.

### Edge Inset and Hole Borders

Physical punch cards have a visible border of card stock around each hole — the material between adjacent punch positions. Punchcard's edge inset control replicates this by shrinking the "transparent" region within each cell. At an inset of zero, the hole fills the entire cell; at higher insets, a visible border of card stock color remains around each hole, creating the distinctive grid-line appearance of a real punched card.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Video Timing Generator ─────────────────────────────────────
│   └─ Derive h_count, v_count from sync signals
│
├── Parameter Derivation ───────────────────────────────────────
│   ├─ Cell Width pot → shift (3-7) → cell size (8-128 px)
│   ├─ Cell Height pot → shift (3-7) → cell size (8-128 lines)
│   ├─ Density toggle → shift - 1 (minimum 3)
│   ├─ Edge Inset pot → raw >> 5 (0-31 px)
│   └─ Style toggle → force inset = 0 (borderless)
│
├── Stage 1: Input Register + Cell Position        [1 clk]
│   ├─ Compute intra-cell X from h_count
│   ├─ Compute intra-cell Y from v_count
│   └─ Capture source Y at left edge (intra_x == 0)
│
├── Stage 2: Threshold + Hole Region Test          [1 clk]
│   ├─ Punch test: cell_luma > threshold?
│   ├─ Apply Invert toggle
│   └─ Hole test: pixel inside inset border?
│
├── Stage 3: Source vs Card Stock Composition      [1 clk]
│   └─ Punched AND in-hole → source; else → card stock
│
├── Stage 4: Final Output Register                 [1 clk]
│   ├─ Punched hole: pass source Y/U/V
│   └─ Card stock: Y=card_bright, U=500, V=520 (beige)
│
├── Wet/Dry Mix (3x interpolator_u)                [4 clk]
│   └─ Crossfade between delayed original and composite
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock delay pipeline (hsync, vsync, field, Y/U/V)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original (delayed) or mixed signal
```

The critical subtlety is *where* the luma is sampled for the punch decision: at the left edge of each cell column (intra_x == 0), the source Y value is captured and held for the entire cell width. This means the punch decision is based on a single pixel per cell column, not an average — a thin bright stripe at the cell boundary will punch the entire column even if the rest of the cell is dark. The card stock color has fixed chroma constants (U=500, V=520), giving it a slightly warm off-white tint regardless of the Card Color knob, which controls only the Y (brightness) component.

**TOML label discrepancies**: Several TOML parameter labels do not match their VHDL function. The supplement describes the actual VHDL behavior for each control. Additionally, bypass is mapped to toggle bit 3 (the hardware position of toggle 10, labeled "Animate" in the TOML), while toggle 11 (labeled "Bypass") is not connected. The fader (labeled "Mix") is also not connected in the VHDL — the actual wet/dry mix is on potentiometer 6 (labeled "Threshold" in the TOML).

---

## Parameter Reference

<img src={punchcard_control_panel} alt="Videomancer front panel with Punchcard loaded"/>
*Videomancer's front panel with Punchcard active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Hole Sz
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**VHDL function: Cell Width (s_cell_w_raw).** Controls the horizontal size of grid cells. The pot value is mapped through five thresholds to a power-of-two shift amount: values 0–204 produce 8-pixel cells, 205–409 produce 16-pixel, 410–614 produce 32-pixel, 615–819 produce 64-pixel, and 820–1023 produce 128-pixel cells. Combined with the Density toggle (which subtracts one from the shift), the effective range is 8 to 128 pixels. At the smallest setting, the grid is dense — many narrow columns. At the largest, each cell spans a significant portion of the frame.

---

#### Knob 2 — Rows
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**VHDL function: Cell Height (s_cell_h_raw).** Controls the vertical size of grid cells using the same five-threshold mapping as Cell Width. Cells need not be square — setting a large width with a small height produces wide, short cells (horizontal bar pattern), while the reverse produces tall, narrow cells (vertical column pattern). At matched settings, the cells are square.

---

#### Knob 3 — Columns
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**VHDL function: Threshold (s_threshold).** Sets the luma level at which the punch decision flips. Source luminance captured at each cell boundary is compared to this value — cells brighter than the threshold are punched (transparent), cells darker remain card stock. At a low threshold, most cells are punched and the source dominates. At a high threshold, most cells are card stock and little source shows through. The Invert toggle reverses this logic.

---

#### Knob 4 — Spacing
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**VHDL function: Card Color (s_card_bright).** Sets the luminance of the card stock background. This controls only the Y component — the chroma is fixed at U=500, V=520, giving a slightly warm beige tone. At low values, the card stock is dark brown; at high values, bright cream. At the extremes, the card stock becomes black (0) or near-white (1023) while retaining its slight warm tint.

---

#### Knob 5 — Card Clr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**VHDL function: Edge Inset (s_edge_inset_raw).** Controls the border width around each punched hole. The pot value is shifted right by 5 bits, giving an effective range of 0–31 pixels of inset. At zero, the hole fills the entire cell. At higher values, a visible border of card stock color surrounds each hole. When the Style toggle is active (borderless mode), this control is overridden — the inset is forced to zero regardless of the pot position.

---

#### Knob 6 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**VHDL function: Mix (s_mix_amount).** This is the wet/dry crossfade control, despite being labeled "Threshold" in the TOML. The three `interpolator_u` instances crossfade between the delayed original signal and the punch card composite. At 1023 (fully clockwise), the output is 100% processed. At 0, the output is 100% original. Note: the linear fader (labeled "Mix" in the TOML) is **not connected** in the VHDL — this potentiometer is the actual mix control.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Card** | IBM | Hollerth |
| **8 — Holes** | Round | Rect |
| **9 — Fill** | Source | Solid |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The four active toggles control cell density, hole border style, punch logic inversion, and bypass. **Important**: the TOML labels for these toggles are incorrect. Toggle 7 ("Card" in TOML) is actually Density, toggle 8 ("Holes") is Style, toggle 9 ("Fill") is Invert, and toggle 10 ("Animate") is actually Bypass. Toggle 11 (labeled "Bypass" in TOML) is not connected to anything in the VHDL. The fader (labeled "Mix") is also not connected.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

**Not connected in VHDL.** Despite being labeled "Mix" in the TOML, the linear fader (register 7) is not used in the Punchcard architecture. The actual wet/dry mix control is potentiometer 6 (register 5, labeled "Threshold" in the TOML). Moving this fader has no effect.

---

## Guided Exercises

These exercises explore the punch card grid from basic binary quantization through complex threshold interactions. Because several TOML labels are incorrect, the Settings tables below use the TOML labels (what you see on the panel), with the actual VHDL function noted in parentheses where they differ.

### Exercise 1: Basic Punch Card Grid

<img src={punchcard_exercise1_result} alt="Basic Punch Card Grid result"/>
*Basic Punch Card Grid — simulated result across source images.*
**Source**: A well-lit face or scene with clear bright and dark regions — high contrast footage works best.

**Objective**: Create a classic punch card readout and learn how cell size and threshold interact.

1. **Large cells**: Set Hole Sz (Cell Width) and Rows (Cell Height) to ~60% for 32-pixel cells. Feed the source and observe the coarse grid.
2. **Threshold sweep**: Slowly turn Columns (Threshold) from fully counter-clockwise to fully clockwise. Watch as more cells flip from punched to card stock. Find the threshold that best separates the subject from the background.
3. **Card brightness**: Adjust Spacing (Card Color) to change the card stock from dark to light. Note the warm beige tint from the fixed chroma.
4. **Add borders**: Set Card Clr (Edge Inset) to ~40%. Visible borders appear around each hole, creating the classic punch card grid look.
5. **Density double**: Toggle Card (Density) on. Cell count quadruples — the grid becomes much finer with the same pot positions.

**Key concepts**: Cell size is power-of-two (8/16/32/64/128 px), threshold converts continuous luma to binary punch decision, card stock has fixed warm chroma, Density toggle halves cell size

---

### Exercise 2: Binary Mosaic

<img src={punchcard_exercise2_result} alt="Binary Mosaic result"/>
*Binary Mosaic — simulated result across source images.*
**Source**: Abstract video synthesis output or colorful patterns — something with varied colors and brightness.

**Objective**: Create a borderless binary mosaic that uses the source color in punched regions.

1. **Small cells**: Set Hole Sz (Cell Width) and Rows (Cell Height) to ~20% for 8–16 pixel cells.
2. **Borderless**: Toggle Holes (Style) on to remove hole borders. Each cell is now entirely source or entirely card stock.
3. **Find the balance**: Adjust Columns (Threshold) until roughly half the cells are punched, creating a balanced mosaic.
4. **Dark card stock**: Set Spacing (Card Color) low (~20%). The unpunched cells become dark, creating a binary pattern where source color pops against a dark grid.
5. **Invert**: Toggle Fill (Invert) to swap which cells show source. The pattern reverses — bright areas become card stock and dark areas become punched holes.
6. **Blend**: Use Threshold (Mix) at ~60% to partially blend the original signal back through the effect.

**Key concepts**: Borderless mode removes inset borders for a clean binary mosaic, invert swaps the punch logic, the mix pot (labeled "Threshold") blends processed and original

---

### Exercise 3: Animated Data Stream

<img src={punchcard_exercise3_result} alt="Animated Data Stream result"/>
*Animated Data Stream — simulated result across source images.*
**Source**: Slowly moving or evolving footage — a camera pan, time-lapse, or modulated synthesis.

**Objective**: Create a data-stream visualization that responds to the source content in real time.

1. **Dense grid**: Set Hole Sz and Rows to ~10% (8-pixel cells) and toggle Card (Density) on for maximum grid density.
2. **Moderate threshold**: Set Columns (Threshold) to ~40% so the punch pattern is responsive to the source content.
3. **Bright card stock**: Set Spacing (Card Color) to ~80% for high contrast between card stock and punched holes.
4. **Visible borders**: Set Card Clr (Edge Inset) to ~25% for thin grid lines between cells.
5. **Observe motion**: As the source moves, watch the punch pattern ripple across the grid. Each cell column re-evaluates at its left boundary, creating a scanning update pattern.
6. **Threshold animation**: Slowly sweep Columns (Threshold) while the source plays. The punch pattern grows and shrinks as the threshold passes through different brightness levels.

**Key concepts**: Luma is sampled at the left edge of each cell column (not averaged), so the punch pattern has a left-edge sampling bias; motion in the source creates animated punch patterns; dense grids produce a data-readout aesthetic

---


## Tips

- **TOML label cheat sheet**: Pot 6 ("Threshold" label) = Mix. Toggle 10 ("Animate" label) = Bypass. Toggle 11 ("Bypass" label) = not connected. Fader ("Mix" label) = not connected.
- **Bypass workaround**: If you expect Bypass on toggle 11, set pot 6 to fully counter-clockwise instead to get a 100% dry signal.
- **Cell size steps**: Cell sizes snap between powers of two (8/16/32/64/128), so sweep the pot slowly to find each transition point.
- **Density for quick compare**: The Density toggle is a one-switch preview of a finer grid — useful for quickly evaluating whether smaller cells improve the look.
- **Card stock always has color**: Even at Y=0 or Y=1023, the card stock retains its U=500/V=520 warm tint. For pure neutral card stock, chain with a downstream desaturation program.
- **Threshold at edges**: The luma threshold is very sensitive at high contrast boundaries. Small threshold changes produce large visual shifts at content edges.
- **Power-of-two alignment**: Cell boundaries always align to pixel positions that are multiples of the cell size, creating perfectly regular grids at all sizes.

---

## Glossary

| Term | Definition |
|------|------------|
| **Card Stock** | The opaque background surface of a punch card; in the VHDL, a flat color (configurable Y, fixed U=500/V=520) shown in unpunched cells. |
| **Cell** | A rectangular grid element defined by the cell width and height parameters; each cell is independently classified as punched or unpunched. |
| **Edge Inset** | The number of pixels of card stock border around each punched hole, creating the visible border between adjacent holes. |
| **Hollerith** | Herman Hollerith, inventor of the punch card tabulating system used in the 1890 US Census; the format was later standardized by IBM. |
| **Interpolator** | A pipelined hardware unit computing a + (b − a) × t for crossfading between two signals. |
| **Intra-Cell Position** | The pixel's coordinates within its containing cell, computed via bit masking from the global pixel counters. |
| **Luma Threshold** | The Y value above which a cell is classified as "punched"; sampled at the left edge of each cell column. |
| **Power-of-Two** | Cell sizes restricted to 2^n (8, 16, 32, 64, 128) for efficient bit-mask computation in FPGA logic. |
| **Punch** | A transparent opening in the card stock that reveals the source video underneath; determined by the luma threshold comparison. |
| **Shift Amount** | The bit-shift exponent (3–7) used to derive cell size; pot value is mapped through five thresholds to select the exponent. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
