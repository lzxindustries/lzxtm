---
draft: true
sidebar_position: 145
slug: /instruments/videomancer/ledger
title: "Ledger"
image: /img/instruments/videomancer/ledger/ledger_hero.png
---

import ledger_before_after from '/img/instruments/videomancer/ledger/ledger_before_after.png';
import ledger_control_panel from '/img/instruments/videomancer/ledger/ledger_control_panel.png';
import ledger_exercise1_result from '/img/instruments/videomancer/ledger/ledger_exercise1_result.png';
import ledger_exercise2_result from '/img/instruments/videomancer/ledger/ledger_exercise2_result.png';
import ledger_exercise3_result from '/img/instruments/videomancer/ledger/ledger_exercise3_result.png';
import ledger_hero from '/img/instruments/videomancer/ledger/ledger_hero.png';
import ledger_source1_kodim15 from '/img/instruments/videomancer/ledger/ledger_source1_kodim15.png';
import ledger_source2_kodim15_bw from '/img/instruments/videomancer/ledger/ledger_source2_kodim15_bw.png';
import ledger_source3_male_1024 from '/img/instruments/videomancer/ledger/ledger_source3_male_1024.png';

# Ledger

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={ledger_hero} alt="Ledger hero image"/>
*Ledger overlaying green-bar ruled paper and column grids onto a live video feed, evoking the texture of continuous-form accounting printouts.*
<img src={ledger_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Ledger applied.*

---

## Overview

Before spreadsheets, before screens, accountants lived on paper. Not blank paper — green-bar paper. Eleven-by-fourteen-inch continuous-form sheets with alternating green and white stripes, horizontal rules every few lines, and a red left margin. Thousands of numbers marched across those pages in neat columns, and the green stripes kept your eyes from drifting to the wrong row.

Ledger recreates that texture as a video overlay. It generates ruled horizontal lines, optional column grids, and alternating tinted stripes, then composites the pattern over the incoming video at adjustable opacity. The result looks like your video feed is being displayed on vintage accounting paper — or engineering graph paper, or legal pad, or correction sheets, depending on the style selector.

The program is entirely combinatorial; it uses no BRAM. The pattern is generated from position counters that reset on each frame, making the rules perfectly stable from field to field. Row and column spacing snap to power-of-two steps (8, 16, 32, and 64 pixels) for clean alignment with HD video grids.

---

## Background

### Green-Bar Paper

Continuous-form green-bar paper was ubiquitous in data processing from the 1960s through the 1990s. The alternating green and white stripes — typically four or six lines each — helped the eye track across wide tabular printouts from dot-matrix or line printers. The paper was perforated along the edges for tractor-feed printing, and perforated between pages for separation. The green tint was chosen because it reduced eye strain under fluorescent office lighting. Ledger's default "Green" style replicates this look.

### Ruled Lines in Drafting and Accounting

Horizontal ruled lines serve as baselines — guides that establish consistent row heights. Vertical rules create columns. Together they form a grid, the fundamental organizing structure of tabular data. Accounting ledgers used thick horizontal rules to separate sections and thin vertical rules to delineate columns for debits, credits, and balances. Ledger's Line W control adjusts the rule thickness from a single-pixel hairline (1) to a bold 4-pixel bar.

### Paper Styles and Colors

Different professions used different colored papers. Green for general accounting, blue for engineering graph paper, yellow for legal pads, red for correction or audit markings. Each color carried a social meaning: yellow meant "draft — not final," red meant "this needs attention." Ledger's Style selector maps to these four traditions, adjusting the chroma tint of the stripe pattern.

### Opacity Compositing

Overlaying the paper pattern on video uses a simple shift-based opacity blend. The opacity control selects how many bits to shift the video contribution vs. the paper contribution. At zero opacity, the video dominates; at full opacity, the paper pattern overwhelms the video. Because the blend uses bit-shifting rather than multiplication, there are only four effective opacity levels — 0%, 25%, 50%, and 75% paper dominance. This is a deliberate hardware economy: four levels are enough to suggest the paper texture at various intensities without consuming multiplier resources.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ h_count: horizontal pixel position (reset per line)
│   └─ v_count: vertical line position (reset per frame)
│
├── Stage 1: Input + Grid Position ─────────────────────────────
│   ├─ Register input Y/U/V
│   ├─ Row height → 8/16/32/64 (power-of-2 snap)
│   ├─ Col width → 8/16/32/64 (power-of-2 snap)
│   ├─ Compute row_pos, col_pos (modular via bit mask)
│   ├─ Horizontal rule: row_pos < line_width
│   ├─ Vertical rule:   col_pos < line_width
│   ├─ Margin line:     h_count in [margin_x, margin_x+2)
│   └─ Row index parity for alternating stripes
│
├── Stage 2: Pattern Generation ────────────────────────────────
│   ├─ Grid mode select: Rows / Cols / Both / None
│   ├─ Stripe on/off (alternating rows if enabled)
│   ├─ Paper base Y = 900 (bright white)
│   └─ Style tint color (Green/Blue/Yellow/Red → U,V pairs)
│
├── Stage 3: Compose Paper + Video ─────────────────────────────
│   ├─ Rule line: Y=200, U=550, V=470 (dark line)
│   ├─ Tinted stripe: paper_y − (tint >> 2), style U/V
│   ├─ White paper: Y=900, U=512, V=512
│   └─ Opacity blend: video >> shift + paper − (paper >> shift)
│
├── Stage 4: Invert + Output ──────────────────────────────────
│   └─ Optional Y inversion (1023 − Y)
│
├── Interpolator (4 clk): Wet/dry mix ─────────────────────────
│   └─ lerp(dry, processed, mix_amount) per channel
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pattern is generated purely from position counters — no BRAM is consumed. Row and column spacing snap to power-of-two steps via bit masking, which means the grid is always pixel-aligned and perfectly stable. The opacity blend uses bit shifting instead of multipliers, yielding four discrete transparency steps rather than a continuous range. Rule lines are drawn in a fixed dark color regardless of style, providing contrast against any tint setting.

---

## Parameter Reference

<img src={ledger_control_panel} alt="Videomancer front panel with Ledger loaded"/>
*Videomancer's front panel with Ledger active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Row H
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the vertical spacing between horizontal rules. The pot range is quantized into four steps: values below 256 give 8-pixel rows (dense, fine rulings), 256–512 give 16-pixel rows, 512–768 give 32-pixel rows, and above 768 give 64-pixel rows (wide, ledger-style spacing). The step sizes are powers of two, chosen because position-within-row is computed by bit masking, not division.

---

#### Knob 2 — Col W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the horizontal spacing between vertical column rules. Quantized identically to Row H — four power-of-two steps from 8 to 64 pixels. When Grid is set to Cols or Both, these vertical rules create the column structure of the ledger. When set to Rows or None, this control has no visible effect but its value is still registered.

---

#### Knob 3 — Opacity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how much the paper pattern shows over the video. The pot is divided into four shift levels: at 0% the video dominates, at 100% the paper pattern overwhelms the video. Because the blend uses right-shifting rather than multiplication, the opacity steps are coarse — roughly 0%, 25%, 50%, and 75% paper dominance. This gives the paper that partially transparent overlay look, similar to a watermark or security underprint.

---

#### Knob 4 — Tint
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the strength of the color tint on alternating stripes. At 0%, stripes are the same brightness as the paper base (no visible tint). As the value increases, the tinted stripes darken — the pot value is right-shifted by 2 and subtracted from the paper base Y value, so higher settings push the stripe luminance down. The chroma components are set by the Style toggle, not by this control.

---

#### Knob 5 — Line W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the thickness of the rule lines. The pot is mapped to a 1–4 pixel range: 0–255 gives 1 pixel (hairline), 256–511 gives 2 pixels, 512–767 gives 3 pixels, and 768–1023 gives 4 pixels (bold). The lines are drawn at the boundary of each row or column cell, and both horizontal and vertical rules share the same width.

---

#### Knob 6 — Margin
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the horizontal position of the left margin line. The pot value is right-shifted by 2, giving a range of 0–255 pixels from the left edge. The margin line is always exactly 2 pixels wide, drawn as a fixed dark line that cuts across the horizontal rules regardless of grid mode. At 0%, the margin sits at the far left; at 100% it moves about a quarter of the way across the screen.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Green | Blue |
| **8 — Grid** | Rows | Cols |
| **9 — Stripes** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 each consume two bits of the toggle register because they have four selectable values each. This pushes subsequent toggles up: Stripes lands on bit 4, Invert on bit 5, and Bypass on bit 6 rather than the usual bit 4. This non-standard packing is transparent to the user — the controls appear as five independent switches on the front panel — but the firmware's toggle-to-register mapping differs from most programs.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original input and the processed output. At 0% the output is entirely dry (unprocessed video). At 100% the output is entirely wet (the ledger overlay). Intermediate values blend the two, allowing the paper texture to be dialed in as a subtle tint or a dominant overlay. The crossfade is performed by the 4-clock interpolator stage after all processing.

---

## Guided Exercises

These exercises explore Ledger's grid and tinting modes progressively, starting with simple ruled paper and building toward composited overlay effects.

### Exercise 1: Classic Green-Bar Paper

<img src={ledger_exercise1_result} alt="Classic Green-Bar Paper result"/>
*Classic Green-Bar Paper — simulated result across source images.*
**Source**: A live camera feed or talking-head video with moderate detail.

**Objective**: Recreate the look of classic continuous-form accounting paper.

1. **Set style**: Select Green (Toggle 7 to Green).
2. **Enable stripes**: Set Stripes to On.
3. **Grid mode**: Set Grid to Rows — we want horizontal rules only.
4. **Row spacing**: Turn Row H to about 60% (32-pixel rows).
5. **Line weight**: Set Line W to about 30% (2-pixel rules).
6. **Margin**: Turn Margin to about 15% to place a margin line near the left edge.
7. **Opacity**: Set Opacity to about 50% so the video shows through the paper.
8. **Tint**: Crank the Tint to about 70% to darken the green stripes.
9. **Mix fully wet**: Push the Mix fader to 100%.
10. **Compare**: Toggle Bypass to see the raw video, then back to see the overlay.

**Key concepts**: Green-bar paper is alternating tinted stripes with horizontal rules, opacity blend reveals the video underneath, margin and row spacing set the paper scale

---

### Exercise 2: Engineering Grid Paper

<img src={ledger_exercise2_result} alt="Engineering Grid Paper result"/>
*Engineering Grid Paper — simulated result across source images.*
**Source**: Geometric patterns, architecture footage, or oscilloscope traces.

**Objective**: Create a blue-grid overlay suitable for technical or engineering aesthetics.

1. **Set style**: Switch to Blue.
2. **Grid mode**: Set Grid to Both for full horizontal and vertical rules.
3. **Match spacing**: Set both Row H and Col W to about 40% (16-pixel grid).
4. **Bold lines**: Set Line W to about 60% (3-pixel rules).
5. **No margin**: Turn Margin fully counter-clockwise.
6. **Full opacity**: Set Opacity to about 75%.
7. **Subtle tint**: Set Tint to about 30%.
8. **Disable stripes** for clean grid: Set Stripes to Off.
9. **Compare the grid patterns**: Switch Grid between Rows, Cols, Both, and None to see each mode.

**Key concepts**: Both H and V rules create a full grid, equal row and column spacing create square cells, stripes can be disabled for a clean graph paper look

---

### Exercise 3: Inverted Legal Pad

<img src={ledger_exercise3_result} alt="Inverted Legal Pad result"/>
*Inverted Legal Pad — simulated result across source images.*
**Source**: Text, documents, or footage with high contrast.

**Objective**: Combine yellow legal-pad tinting with inversion for a dramatic negative overlay.

1. **Set style**: Switch to Yellow.
2. **Enable stripes and rows**: Stripes On, Grid to Rows.
3. **Coarse spacing**: Set Row H to about 80% (64-pixel rows).
4. **Moderate opacity**: Set Opacity to about 50%.
5. **Strong tint**: Set Tint to about 80%.
6. **Enable invert**: Set Invert to On.
7. **Observe the negative**: Dark paper becomes bright, bright rules become dark. The video content inverts within the overlay blend.
8. **Sweep opacity**: Watch how the opacity shift changes the balance between inverted paper and inverted video.
9. **Try Red style**: Switch to Red and compare the inverted color palette.
10. **Partial mix**: Pull Mix back to ~60% to blend some dry signal back in.

**Key concepts**: Inversion applies after compositing, all four style colors produce different inverted palettes, partial mix allows blending inverted and non-inverted signals

---


## Tips

- **Row height snaps to powers of two**: Don't expect continuous row spacing — the pot is quantized into four steps (8, 16, 32, 64 pixels). Sweep slowly and watch the snap points.
- **Opacity has four levels, not a gradient**: The shift-based blend creates discrete steps. If you need finer control over paper intensity, use the Mix fader in combination with Opacity.
- **Margin is always 2 pixels**: Unlike grid rules (which respond to Line W), the margin line is always exactly 2 pixels wide and drawn in the same dark rule color.
- **Grid None + Stripes Off = flat paper**: Setting both grid and stripes off leaves only the paper base color and the margin line. This can serve as a simple brightness overlay.
- **Invert reverses everything**: Because inversion is the last processing step before the interpolator, it flips the entire composited result — paper, rules, and video together.
- **Style only affects tinted stripes**: Rule lines and the margin line always use the same fixed dark color regardless of the style setting.
- **Feedback routing**: Sending the output back to the input creates recursive paper overlays where the grid pattern compounds each pass through, thickening the rules and deepening the tint.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bit Masking** | Using bitwise AND to extract a subset of bits from a counter, implementing efficient modular arithmetic (position within row/column). |
| **BRAM** | Block RAM; dedicated FPGA memory tiles. Ledger uses zero BRAMs because the pattern is generated from counters, not stored in memory. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Compositing** | Blending two image layers (paper pattern and video) together at a specified opacity. |
| **Continuous-Form Paper** | Fan-fold paper with tractor-feed perforations used by line printers. Green-bar paper is the most recognized variant. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Power-of-Two** | Values like 8, 16, 32, 64 that can be computed by bit shifting, avoiding expensive division or modulo operations. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
