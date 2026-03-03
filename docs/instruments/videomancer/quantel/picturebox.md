---
draft: true
sidebar_position: 226
slug: /instruments/videomancer/picturebox
title: "Picturebox"
image: /img/instruments/videomancer/picturebox/picturebox_hero_s1.png
description: "In the control rooms of 1990s television studios, a wall of small monitors showed multiple camera feeds simultaneously — each screen a window into a different moment or angle."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import picturebox_source1_dog from '/img/instruments/videomancer/picturebox/picturebox_source1_dog.png';
import picturebox_source2_skull from '/img/instruments/videomancer/picturebox/picturebox_source2_skull.png';
import picturebox_source3_elephant from '/img/instruments/videomancer/picturebox/picturebox_source3_elephant.png';
import picturebox_source4_pattern from '/img/instruments/videomancer/picturebox/picturebox_source4_pattern.png';
import picturebox_source5_boy from '/img/instruments/videomancer/picturebox/picturebox_source5_boy.png';
import picturebox_source6_berries from '/img/instruments/videomancer/picturebox/picturebox_source6_berries.png';
import picturebox_hero_s1 from '/img/instruments/videomancer/picturebox/picturebox_hero_s1.png';
import picturebox_hero_s2 from '/img/instruments/videomancer/picturebox/picturebox_hero_s2.png';
import picturebox_hero_s3 from '/img/instruments/videomancer/picturebox/picturebox_hero_s3.png';
import picturebox_hero_s4 from '/img/instruments/videomancer/picturebox/picturebox_hero_s4.png';
import picturebox_hero_s5 from '/img/instruments/videomancer/picturebox/picturebox_hero_s5.png';
import picturebox_hero_s6 from '/img/instruments/videomancer/picturebox/picturebox_hero_s6.png';
import picturebox_ex1_s1 from '/img/instruments/videomancer/picturebox/picturebox_ex1_s1.png';
import picturebox_ex1_s2 from '/img/instruments/videomancer/picturebox/picturebox_ex1_s2.png';
import picturebox_ex1_s3 from '/img/instruments/videomancer/picturebox/picturebox_ex1_s3.png';
import picturebox_ex1_s4 from '/img/instruments/videomancer/picturebox/picturebox_ex1_s4.png';
import picturebox_ex1_s5 from '/img/instruments/videomancer/picturebox/picturebox_ex1_s5.png';
import picturebox_ex1_s6 from '/img/instruments/videomancer/picturebox/picturebox_ex1_s6.png';
import picturebox_ex2_s1 from '/img/instruments/videomancer/picturebox/picturebox_ex2_s1.png';
import picturebox_ex2_s2 from '/img/instruments/videomancer/picturebox/picturebox_ex2_s2.png';
import picturebox_ex2_s3 from '/img/instruments/videomancer/picturebox/picturebox_ex2_s3.png';
import picturebox_ex2_s4 from '/img/instruments/videomancer/picturebox/picturebox_ex2_s4.png';
import picturebox_ex2_s5 from '/img/instruments/videomancer/picturebox/picturebox_ex2_s5.png';
import picturebox_ex2_s6 from '/img/instruments/videomancer/picturebox/picturebox_ex2_s6.png';
import picturebox_ex3_s1 from '/img/instruments/videomancer/picturebox/picturebox_ex3_s1.png';
import picturebox_ex3_s2 from '/img/instruments/videomancer/picturebox/picturebox_ex3_s2.png';
import picturebox_ex3_s3 from '/img/instruments/videomancer/picturebox/picturebox_ex3_s3.png';
import picturebox_ex3_s4 from '/img/instruments/videomancer/picturebox/picturebox_ex3_s4.png';
import picturebox_ex3_s5 from '/img/instruments/videomancer/picturebox/picturebox_ex3_s5.png';
import picturebox_ex3_s6 from '/img/instruments/videomancer/picturebox/picturebox_ex3_s6.png';

# Picturebox

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: picturebox_source1_dog, after: picturebox_hero_s1 },
    { label: "Skull", before: picturebox_source2_skull, after: picturebox_hero_s2 },
    { label: "Elephant", before: picturebox_source3_elephant, after: picturebox_hero_s3 },
    { label: "Pattern", before: picturebox_source4_pattern, after: picturebox_hero_s4 },
    { label: "Boy", before: picturebox_source5_boy, after: picturebox_hero_s5 },
    { label: "Berries", before: picturebox_source6_berries, after: picturebox_hero_s6 },
  ]}
/>
*Picturebox dividing a single video input into a configurable grid of temporally-delayed panels with coloured borders and optional label strips.*

---

## Overview

In the control rooms of 1990s television studios, a wall of small monitors showed multiple camera feeds simultaneously — each screen a window into a different moment or angle. Picturebox recreates this aesthetic digitally, dividing a single video frame into a configurable grid where each panel shows the input at a different point in time. The result is a contact sheet or multi-up display built from a single video source.

The program stores incoming scanlines in three BRAM circular buffers (Y, U, V), each 2048 entries deep. During active video, each panel reads from the buffer at a different delay offset determined by its position in the grid, so panel 0 shows the most recent frame while panel 15 shows video from several scanlines in the past. The delay between adjacent panels is continuously adjustable, creating everything from a subtle echo effect (small spread) to a dramatic temporal fan where each tile seems to live in its own moment.

Four operating modes extend the grid concept beyond simple temporal mosaic. Spatial tile mode subsamples different regions of the frame into each panel. Freeze cascade mode sequentially freezes panels one per field, building a step-by-step still store. Hybrid mode combines temporal delay with alternating colour inversion, producing a pop-art quality where neighboring panels show inverted versions of each other. Configurable coloured borders and optional label strips at the bottom of each panel complete the broadcast monitor wall illusion.

---

## Background

### The Quantel Picturebox Legacy

The program takes its name from the Quantel Picturebox (circa 1990), one of the first digital still store systems used in television. The Picturebox could capture, store, and display multiple video frames simultaneously on a single monitor — a capability that previously required physical racks of video tape machines and monitor walls. The related Quantel Harriet system took this further, displaying grids of live and frozen video on a single output. Picturebox channels this multi-image display concept through the FPGA's BRAM resources.

### Circular Buffer Temporal Delay

The core mechanism is a circular buffer — a fixed-size block of memory where a write pointer continuously advances and wraps around. Reading from an address behind the write pointer retrieves data from the past. The delay depth equals the distance between the read and write pointers. Picturebox's three BRAM buffers (Y, U, V) each store 2048 scanline samples. Each grid panel reads from a different offset, computed as `write_addr - (panel_id × time_spread)`. Because the buffer wraps naturally, no boundary logic is needed — the unsigned subtraction automatically wraps modulo 2048.

### Grid Geometry and Panel Detection

The grid is decoded from the Grid Size pot at four discrete levels: 2×2 (4 panels), 3×3 (9 panels), 4×4 (16 panels), and 1×4 (4-panel horizontal strip). For power-of-two grids (2×2, 4×4), the panel column and row are extracted directly from the upper bits of the pixel counters — pure bit selection with no division. For the 3×3 grid, explicit comparison thresholds at 640 and 1280 pixels (horizontal) and 360 and 720 lines (vertical) approximate an even three-way split. Each pixel's panel ID, local x, and local y coordinates are computed in the first pipeline stage.

### Border Detection and Beveled Corners

A pixel is on the border if its local x or local y coordinate is less than the border width. For squared borders, this produces sharp right-angle corners where horizontal and vertical grid lines meet. The Bevel toggle adds a diagonal check: `local_x + local_y < 2 × border_width` — creating chamfered corners where the grid lines meet at 45° angles. Border pixels are filled with a colour selected from an 8-hue palette indexed by the upper 3 bits of the Border Hue pot.

### Freeze Cascade and Fill Order

In freeze cascade mode (mode 2), a single "live panel" counter advances each field. Only the designated live panel updates from the circular buffer; all other panels hold their last-read data. In sequential fill order, the counter advances linearly through panel IDs 0, 1, 2, ..., wrapping at the grid size. In random fill order, a single-bit LFSR rotation (`panel(2:0) & (panel(3) XOR panel(0))`) produces a pseudo-random traversal that visits panels in a non-obvious order. The effect is a slow-motion reveal where frozen panels accumulate like Polaroid photographs.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── BRAM Write (circular buffer)
│   └── buf_y/u/v[wr_addr] ← data_in; wr_addr += 1 per hsync
│
├── Timing Generator
│   └── h_count, v_count from video sync
│
├── Stage 1: Grid Geometry
│   ├── Grid decode: 2×2 / 3×3 / 4×4 / 1×4
│   ├── panel_col, panel_row, panel_id
│   └── local_x, local_y within panel
│
├── Stage 2: Address Mapping + Delay Tap
│   ├── Temporal: rd_addr = wr_addr - panel_id × time_spread
│   ├── Spatial: rd_addr = wr_addr (no delay)
│   └── Freeze: rd_addr = wr_addr (live panel only updates)
│
├── Stage 3: BRAM Read + Border/Label Detect
│   ├── BRAM read: panel_y/u/v = buf[rd_addr]
│   ├── Border: local_x < bw OR local_y < bw
│   │   └── Bevel: local_x + local_y < 2×bw
│   └── Label: local_y > panel_height - label_height
│
├── Stage 4: Output Mux
│   ├── Border → border_color (8-hue palette)
│   ├── Label → (label_bright, 512, 512) grey strip
│   ├── Hybrid inversion → 1023 - pixel (odd panel IDs)
│   └── Normal → panel pixel
│
├── Interpolator Mix (4 clocks)
│   └── lerp(source, composite, mix_amount)
│
├── Bypass Mux
│   └── Bypass toggle → pass input unchanged
│
└── Output (YUV 4:4:4)
```

The temporal delay is computed per-panel, not per-pixel — all pixels within a single panel read from the same BRAM offset. This means the delay is constant across each tile, creating a step-wise temporal fan rather than a smooth spatiotemporal gradient. The border and label detection happens after BRAM read, so borders overlay the panel content rather than replacing it — this matters because border colour is independent of the panel's temporal position. In hybrid mode (mode 3), only odd-numbered panels are inverted (panel_id bit 0 = 1), creating a checkerboard of normal and inverted tiles.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Grid Size
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Controls the grid configuration. The upper 2 bits of the register select one of four layouts: 2×2 (4 panels), 3×3 (9 panels), 4×4 (16 panels), or 1×4 (horizontal strip). The transition is stepped — there are exactly four positions with no interpolation between them. The 2×2 layout gives the largest individual panels suitable for detailed viewing. The 4×4 layout creates 16 small tiles that emphasise temporal spread over detail. The 1×4 strip mode is ideal for horizontal panoramic reveals.

---

#### Knob 2 — Time Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Controls the temporal delay between adjacent panels. The upper 6 bits scale the panel ID to compute the BRAM read offset. At 0, all panels show the same moment — no temporal spread. As you increase the value, each successive panel looks further into the past. At maximum, panel 15 in a 4×4 grid is delayed by approximately 62 scanlines relative to panel 0. The effect is most dramatic with moving subjects: as a figure crosses the frame, its motion is captured across the grid like frames of a filmstrip.

---

#### Knob 3 — Border Wid
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

Controls the width of the grid border lines. The upper 8 bits of the register set the pixel thickness of the horizontal and vertical dividers between panels. At 0, panels share edges with no visible gap. As you increase the value, prominent coloured bars separate the panels. Maximum width can consume a significant portion of each panel, creating an effect where the grid structure dominates the image content. The border extends inward from each panel's edge, reducing the visible content area.

---

#### Knob 4 — Border Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Selects the border colour from an 8-entry palette. The upper 3 bits of the register index into the palette: white (hue 0), blue-magenta, yellow, cyan, green-cyan, dark magenta, magenta, and bright white (hue 7). The palette entries are pre-computed YUV values stored in the VHDL as a combinational case statement. There is no interpolation between hues — the transition is abrupt at each boundary.

---

#### Knob 5 — Label Hgt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls an optional label strip at the bottom of each panel. The upper 8 bits set the strip height in pixels. At 0, no label is shown. As you increase the value, a neutral grey bar appears at the bottom of every panel, reminiscent of the label strips on broadcast monitor walls that identify camera feeds. The label strip replaces the panel content in that region — it does not overlay.

---

#### Knob 6 — Label Brt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness of the label strip (Y channel). At 0, the label is black. At 1023, the label is white. The U and V channels are fixed at 512 (neutral), so the label is always achromatic grey regardless of this setting. This control has no effect when Label Height is set to 0.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode A** | Off | On |
| **8 — Mode B** | Off | On |
| **9 — Grid Style** | Square | Bevel |
| **10 — Fill Order** | Seq | Random |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a 2-bit mode selector (4 modes). Toggle 9 affects border rendering style. Toggle 10 affects freeze cascade traversal order. Toggle 11 is the standard bypass. The mode selector and grid style interact at the visual level but operate on independent pipeline stages — mode controls temporal behaviour while grid style controls border rendering.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the wet/dry crossfade via the interpolator. At 0 the output is 100% dry (unprocessed source). At 1023 the output is 100% wet (full grid mosaic). Intermediate values produce a ghostly double-exposure where the grid panels are partially transparent against the full-frame source.

---

## Guided Exercises

These exercises progress from basic grid layout to temporal effects and freeze cascade. Each builds on the previous, gradually engaging more of the processing modes.

### Exercise 1: Broadcast Monitor Wall

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: picturebox_source1_dog, after: picturebox_ex1_s1 },
    { label: "Skull", before: picturebox_source2_skull, after: picturebox_ex1_s2 },
    { label: "Elephant", before: picturebox_source3_elephant, after: picturebox_ex1_s3 },
    { label: "Pattern", before: picturebox_source4_pattern, after: picturebox_ex1_s4 },
    { label: "Boy", before: picturebox_source5_boy, after: picturebox_ex1_s5 },
    { label: "Berries", before: picturebox_source6_berries, after: picturebox_ex1_s6 },
  ]}
/>
*Broadcast Monitor Wall — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and movement.

**Objective**: Learn how grid size and border controls create a multi-monitor display from a single input.

1. **2×2 grid**: Set Grid Size to minimum. Four large panels divide the screen.
2. **Add borders**: Increase Border Width. Coloured bars appear between panels.
3. **Colour the grid**: Sweep Border Hue to cycle through the 8-colour palette.
4. **Add labels**: Increase Label Height. Grey strips appear at the bottom of each panel, like broadcast monitor labels.
5. **Bevel the corners**: Toggle Grid Style to Bevel. Corners become chamfered.
6. **Increase density**: Sweep Grid Size to 3×3, then 4×4. More smaller panels fill the screen.

**Key concepts**: Grid geometry is decoded from upper 2 bits of the Grid Size register, border detection uses local coordinates within each panel, label strip is a fixed-brightness achromatic bar

---

### Exercise 2: Temporal Filmstrip

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: picturebox_source1_dog, after: picturebox_ex2_s1 },
    { label: "Skull", before: picturebox_source2_skull, after: picturebox_ex2_s2 },
    { label: "Elephant", before: picturebox_source3_elephant, after: picturebox_ex2_s3 },
    { label: "Pattern", before: picturebox_source4_pattern, after: picturebox_ex2_s4 },
    { label: "Boy", before: picturebox_source5_boy, after: picturebox_ex2_s5 },
    { label: "Berries", before: picturebox_source6_berries, after: picturebox_ex2_s6 },
  ]}
/>
*Temporal Filmstrip — simulated result across source images.*
**Source**: Footage with smooth, steady horizontal motion — a subject walking across frame.

**Objective**: Explore temporal mosaic mode where each panel shows a different moment in time.

1. **Set 4×4 grid**: Maximum Grid Size for 16 panels.
2. **Add time spread**: Slowly increase Time Spread. Adjacent panels begin showing the subject at different positions.
3. **Motion trail**: With a moving subject, the grid becomes a filmstrip — position 0 shows now, position 15 shows the past.
4. **Thin borders**: Reduce Border Width to thin lines so panels dominate.
5. **Maximum spread**: Crank Time Spread to maximum. Each panel is dramatically delayed from its neighbor.
6. **Mix transparency**: Reduce Mix to ~50%. The grid panels become semi-transparent over the full-frame source.

**Key concepts**: Temporal delay is panel_id × time_spread (scanline offset), circular buffer wraps naturally via unsigned subtraction, all pixels in a panel share the same delay

---

### Exercise 3: Freeze Cascade

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: picturebox_source1_dog, after: picturebox_ex3_s1 },
    { label: "Skull", before: picturebox_source2_skull, after: picturebox_ex3_s2 },
    { label: "Elephant", before: picturebox_source3_elephant, after: picturebox_ex3_s3 },
    { label: "Pattern", before: picturebox_source4_pattern, after: picturebox_ex3_s4 },
    { label: "Boy", before: picturebox_source5_boy, after: picturebox_ex3_s5 },
    { label: "Berries", before: picturebox_source6_berries, after: picturebox_ex3_s6 },
  ]}
/>
*Freeze Cascade — simulated result across source images.*
**Source**: Any moving footage — the effect is most visible with continuous motion.

**Objective**: Use freeze cascade mode to build a sequential still store where panels freeze one at a time.

1. **Set 3×3 grid**: 9 panels for a moderate cascade.
2. **Activate freeze mode**: Set Mode A = Off, Mode B = On (mode 10 = freeze cascade).
3. **Watch the cascade**: Panels freeze one per field in sequence. After 9 fields, the entire grid is frozen.
4. **Random fill**: Toggle Fill Order to Random. Panels freeze in a scrambled LFSR order.
5. **Add borders**: Increase Border Width and choose a bright Border Hue to distinguish panels.
6. **Hybrid mode**: Switch to Mode A = On, Mode B = On (mode 11 = hybrid). Odd panels invert colours, creating a pop-art checkerboard.

**Key concepts**: Freeze cascade advances one panel per field (vsync), sequential vs. LFSR traversal order, hybrid mode inverts odd panel IDs (bit 0 = 1)

---


## Tips

- **Grid size sets the mood**: 2×2 is intimate — each panel is large and detailed. 4×4 is surveillance — many small tiles create visual density. 1×4 is cinematic — a horizontal panorama strip.
- **Time Spread with movement**: The temporal mosaic is most effective with smooth, predictable motion. Fast cuts or scene changes produce discontinuities between panels that can be jarring or creative.
- **Freeze cascade as still store**: In freeze cascade mode, each panel captures a unique moment. Use with slowly changing content to build a contact sheet of distinct frames.
- **Borders as framing**: At very large Border Width, the border structure dominates the image and the panels become small windows in a coloured frame.
- **Hybrid mode pop art**: The alternating inversion in hybrid mode creates a Warhol-like grid where neighboring panels show complementary colours.
- **Label strips as overlays**: The label strip replaces content, not overlays — at large Label Height, the actual video content area within each panel shrinks significantly.
- **Mix for ghosting**: At intermediate Mix values, the grid panels become semi-transparent over the full-frame source, creating a ghostly multi-exposure effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric, used here as circular scanline delay buffers. |
| **Circular Buffer** | A fixed-size memory region with wrapping read/write pointers; enables temporal delay without boundary checks. |
| **Freeze Cascade** | A mode where panels sequentially stop updating from the live buffer, accumulating frozen snapshots. |
| **Grid Geometry** | The subdivision of video frame coordinates into panel column, row, and local position. |
| **Hybrid Mode** | Combines temporal delay with per-panel colour inversion for pop-art aesthetic. |
| **LFSR** | Linear Feedback Shift Register; produces a pseudo-random sequence used for scrambled freeze panel order. |
| **Manhattan Distance** | Sum of absolute coordinate differences; used in grid geometry calculations. |
| **Panel ID** | A 4-bit index derived from panel row and column, used to compute temporal delay offset. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Temporal Mosaic** | Displaying multiple time-delayed versions of a single video source in a grid arrangement. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
