---
draft: true
sidebar_position: 168
slug: /instruments/videomancer/minitel
title: "Minitel"
image: /img/instruments/videomancer/minitel/minitel_hero.png
description: "The Minitel was France's pre-internet information terminal — a small beige box with a keyboard and a 40-column text display that connected millions of F..."
---

import minitel_before_after from '/img/instruments/videomancer/minitel/minitel_before_after.png';
import minitel_control_panel from '/img/instruments/videomancer/minitel/minitel_control_panel.png';
import minitel_exercise1_result from '/img/instruments/videomancer/minitel/minitel_exercise1_result.png';
import minitel_exercise2_result from '/img/instruments/videomancer/minitel/minitel_exercise2_result.png';
import minitel_exercise3_result from '/img/instruments/videomancer/minitel/minitel_exercise3_result.png';
import minitel_hero from '/img/instruments/videomancer/minitel/minitel_hero.png';
import minitel_source1_kodim15 from '/img/instruments/videomancer/minitel/minitel_source1_kodim15.png';
import minitel_source2_kodim03 from '/img/instruments/videomancer/minitel/minitel_source2_kodim03.png';
import minitel_source3_kodim15_bw from '/img/instruments/videomancer/minitel/minitel_source3_kodim15_bw.png';

# Minitel

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={minitel_hero} alt="Minitel hero image"/>
*Minitel reducing a video stream to eight-color mosaic blocks with sample-and-hold quantization and scanline darkening.*
<img src={minitel_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Minitel applied.*

---

## Overview

The Minitel was France's pre-internet information terminal — a small beige box with a keyboard and a 40-column text display that connected millions of French households to online services from 1982 until its retirement in 2012. Its screen used a low-resolution character matrix rendered in a handful of colors, creating a distinctive blocky visual language that became a cultural icon. The Minitel program recreates that aesthetic by quantizing live video into coarse mosaic cells with a severely limited color palette.

The processing chain is deliberately sparse. Video is divided into rectangular cells using a pixel counter with configurable cell size. At each cell boundary, the input Y, U, and V values are latched (sample-and-hold), then quantized to 3-bit resolution — eight brightness levels and eight color combinations. A color/mono switch strips the chroma channels to mid-gray. An inverse toggle flips the quantized luma. Scanline darkening dims alternate rows within each cell by shifting right one bit. The result is a hard-edged, low-resolution mosaic that evokes CRT teletext and early character graphics.

Of the six rotary potentiometers, only the Cell Size knob (Pot 1) is wired into the processing pipeline in the current VHDL implementation. The remaining five pots (Brightness, Contrast, Scanline, Mosaic, Glow) are declared as register signals but are not connected to any processing logic. This makes Minitel a focused, switch-driven program where the primary creative controls are the five toggles and the fader.

---

## Background

### The French Minitel System

The Minitel was a videotex terminal distributed free of charge by France Télécom starting in 1982. At its peak in the late 1990s, over 9 million terminals were in use across France, providing directory services, messaging, banking, and entertainment over standard phone lines. The display used a 40-column by 25-row character matrix rendered in a fixed 8-color palette (black, red, green, yellow, blue, magenta, cyan, white). Graphics were constructed from sixel-style mosaic blocks — each character cell divided into a 2×3 sub-grid that could be individually filled or empty. The visual result was a coarse, blocky, distinctly digital aesthetic that predated the World Wide Web by a decade.

### Sample-and-Hold Quantization

The core of Minitel's spatial effect is sample-and-hold: at the start of each cell, the current pixel value is captured and then replicated across every pixel within that cell's boundaries. This is identical to nearest-neighbor downsampling — no interpolation, no averaging, just a single sample repeated. The result is a grid of uniform rectangular blocks. The cell size control determines the block dimensions: smaller cells preserve more spatial detail; larger cells create a coarser, more abstract mosaic.

### Three-Bit Color Palette

The Minitel's 8-color palette corresponds to 3-bit quantization — one bit each for the presence or absence of red, green, and blue at full intensity. In the YUV domain used by Videomancer, this is approximated by truncating Y, U, and V to their three most significant bits and zeroing the remaining seven. The quantization creates hard tonal boundaries: smooth gradients collapse into flat plateaus, and subtle color variations snap to the nearest of eight discrete hues.

### Scanline Darkening

CRT displays draw the image as a series of horizontal lines separated by thin gaps. On low-resolution displays like the Minitel terminal, these scanline gaps were visible, giving the image a characteristic horizontal striping. The VHDL implements this by detecting alternate rows within each cell (using the least significant bit of the local Y counter) and applying a right-shift by one bit to the luma — effectively halving the brightness of every other row. The effect is purely cosmetic, adding a CRT texture to the mosaic blocks.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ h_count, v_count (absolute pixel position)
│   ├─ local_x, local_y (position within current cell)
│   ├─ cell_x, cell_y (cell grid index)
│   └─ cell_size derived from Pot 1 bits [9:7] + 4 → range 4–11
│
├── Sample-and-Hold ────────────────────────────────────────────
│   └─ Latch Y/U/V at local_x rollover (cell boundary)
│
├── 3-Bit Quantization ────────────────────────────────────────
│   ├─ Y: held_y[9:7] & "0000000" (8 luma levels)
│   ├─ U: held_u[9:7] & "0000000" (Color mode only)
│   └─ V: held_v[9:7] & "0000000" (Color mode only)
│
├── Mono/Color Switch (Toggle 7) ──────────────────────────────
│   └─ Mono: U=512, V=512 (neutral chroma)
│
├── Inverse (Toggle 8) ────────────────────────────────────────
│   └─ Y = 1023 − quantized_Y
│
├── Scanline Darkening (Toggle 10, labeled "Blink") ───────────
│   └─ If local_y[0]=1: Y = Y >> 1
│
├── Wet/Dry Mix (3× interpolator_u, Fader) ────────────────────
│   └─ lerp(dry, wet, mix_amount) per channel
│
└── Bypass (Toggle 11) ────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline is intentionally minimal: sample-and-hold feeds directly into quantization with no intermediate processing. The critical subtlety is the processing order for luma — quantization happens first, then inverse is applied, then scanline darkening. This means inverse flips the quantized levels (not the raw input), and scanline darkening dims the already-inverted result. Note that Toggle 10 is labeled "Blink" in the TOML parameter definition but is wired to the scanline darkening logic in the VHDL — it does not produce any blinking animation.

---

## Parameter Reference

<img src={minitel_control_panel} alt="Videomancer front panel with Minitel loaded"/>
*Videomancer's front panel with Minitel active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 4 |

Controls the mosaic cell size in pixels. The cell dimension is derived from the upper three bits of the register value plus an offset of four, yielding a range of 4 to 11 pixels per cell side. At minimum, the cells are small enough to preserve recognizable image structure. At maximum, the image becomes a very coarse grid of large uniform blocks where only the broadest shapes and colors remain. Because the cell counter resets at each horizontal and vertical sync, the cell grid is always aligned to the top-left corner of the active video area.

---

#### Knob 2 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

Declared as "Brightness" in the register mapping but not connected to any processing logic in the current VHDL implementation. Adjusting this knob has no effect on the output. It is reserved for a future firmware revision that may add brightness offset to the quantized signal.

---

#### Knob 3 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Declared as "Contrast" in the register mapping but not connected to any processing logic in the current VHDL implementation. Adjusting this knob has no effect on the output. It is reserved for a future firmware revision.

---

#### Knob 4 — Scanline
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Declared as "Scanline" in the register mapping but not connected to any processing logic in the current VHDL implementation. Adjusting this knob has no effect on the output — the scanline effect is controlled entirely by Toggle 10 (on/off) with a fixed darkening amount (right-shift by 1). A future revision may use this pot to control scanline intensity.

---

#### Knob 5 — Mosaic
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Declared as "Mosaic" in the register mapping but not connected to any processing logic in the current VHDL implementation. Adjusting this knob has no effect on the output. It is reserved for a future firmware revision.

---

#### Knob 6 — Glow
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Declared as "Glow" in the register mapping but not connected to any processing logic in the current VHDL implementation. Adjusting this knob has no effect on the output. It is reserved for a future revision that may add a phosphor glow simulation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color** | Mono | Color |
| **8 — Inverse** | Off | On |
| **9 — Double Ht** | Off | On |
| **10 — Blink** | Off | On |
| **11 — Bypass** | Off | On |

Of the five toggles, three are actively wired in the VHDL: Color/Mono (Toggle 7) selects whether chroma quantization is applied or stripped, Inverse (Toggle 8) flips the quantized luma, and the toggle labeled "Blink" (Toggle 10) actually controls scanline darkening on alternate rows. Toggle 9 (Double Height) is declared but not connected to any processing logic. Toggle 11 is the standard bypass switch.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry crossfade between the original video signal and the mosaic-quantized result. At 0%, the output is the unprocessed input. At 100%, the output is the fully quantized mosaic. Intermediate values blend the two, which can create a ghostly overlay where the original image detail is faintly visible through the mosaic blocks. Because the blend operates independently on Y, U, and V, you can get interesting color artifacts at mid-mix positions where the quantized palette partially shows through.

---

## Guided Exercises

These exercises explore the Minitel effect from basic mosaic quantization to creative uses of the limited control set. Since most pots are inactive in this implementation, the focus is on cell size, the toggles, and the mix fader.

### Exercise 1: Basic Mosaic Grid

<img src={minitel_exercise1_result} alt="Basic Mosaic Grid result"/>
*Basic Mosaic Grid — simulated result across source images.*
**Source**: A colorful, detailed scene — a garden, a bookshelf, or a busy street.

**Objective**: Learn how cell size and color mode affect the mosaic quantization.

1. Start with Cell Size at minimum. The image shows recognizable content with visible quantization banding.
2. Slowly increase Cell Size. Watch the image dissolve into larger and larger uniform blocks.
3. Toggle Color (Switch 7) between Mono and Color. In Mono, only brightness is quantized — the eight shades of gray. In Color, the 8-color RGB palette appears.
4. Sweep the Mix fader from 0% to 100% and observe the blend between clean and quantized signal.

**Key concepts**: Sample-and-hold decimation, 3-bit quantization creates 8 levels per channel, cell size determines spatial resolution of the mosaic

---

### Exercise 2: Inverted Scanline Terminal

<img src={minitel_exercise2_result} alt="Inverted Scanline Terminal result"/>
*Inverted Scanline Terminal — simulated result across source images.*
**Source**: High-contrast text, graphics, or a face against a dark background.

**Objective**: Combine inverse video and scanline darkening for a CRT terminal look.

1. Set Cell Size to a medium value (around step 5).
2. Enable Inverse (Switch 8). The tonal structure flips — what was dark becomes bright.
3. Enable Blink/Scanlines (Switch 10). Alternating rows within each cell darken, creating visible horizontal striping.
4. Toggle Color to Mono for a classic green-screen terminal aesthetic.
5. Sweep Mix to about 70% — the original image ghosts through the terminal overlay.

**Key concepts**: Inverse is applied after quantization (flips 8 discrete levels), scanline darkening halves luma on alternate rows, processing order: quantize → invert → scanline darken

---

### Exercise 3: Teletext Color Blocks

<img src={minitel_exercise3_result} alt="Teletext Color Blocks result"/>
*Teletext Color Blocks — simulated result across source images.*
**Source**: A slowly moving abstract video or colorful geometries.

**Objective**: Push the 8-color palette to maximum abstraction for a teletext broadcast look.

1. Set Cell Size to maximum (step 8) for the coarsest possible blocks.
2. Set Color mode to Color (Switch 7) for the full 8-color palette.
3. Disable Inverse and Blink — observe the raw quantized palette: black, red, green, yellow, blue, magenta, cyan, white.
4. Enable Blink/Scanlines (Switch 10) to add horizontal texture within the large blocks.
5. Set Mix to 100%. The source video is completely replaced by flat color blocks.
6. Now enable Inverse (Switch 8). The palette inverts — dark blocks become white, bright blocks become black.
7. Compare Bypass On/Off (Switch 11) to see how much information the quantization discards.

**Key concepts**: 3-bit YUV quantization approximates the Minitel 8-color palette, large cells maximize abstraction, inverse reverses the quantized palette, bypass allows instant comparison

---


## Tips

- **Only one knob and one fader matter**: In the current implementation, Cell Size (Pot 1) and Mix (Fader) are the only continuous controls. The creative variation comes from the toggles.
- **Toggle 10 is mislabeled**: Despite the "Blink" label, this toggle controls scanline darkening — a spatial stripe pattern, not a temporal blink. Ignore the label and think of it as "Scanlines."
- **Mono mode for classic terminal look**: Switching to Mono and enabling scanlines creates a convincing vintage CRT terminal aesthetic.
- **Large cells for abstraction**: Maximum Cell Size reduces the image to roughly 100×60 blocks — coarse enough that only broad shapes are recognizable.
- **Inverse + scanlines for phosphor glow**: Combining inverse with scanline darkening creates a look where bright mosaic cells have visible scan gaps — similar to a close-up of an old TV screen.
- **Mid-mix for ghosting**: Setting Mix around 40–60% lets the original image show through the mosaic quantization, creating a double-exposure effect between the clean and quantized signals.
- **Feedback potential**: Routing the output back to the input through a feedback loop creates recursive quantization — the 8-level palette becomes the source, producing a self-referencing digital texture.

---

## Glossary

| Term | Definition |
|------|------------|
| **Cell** | A rectangular region of pixels that are all assigned the same color value through sample-and-hold quantization. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator and using the result to index a lookup table. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived luminance. |
| **Minitel** | A French videotex online service and terminal system operated from 1982 to 2012 by France Télécom. |
| **Quantization** | Mapping a continuous range of values to a smaller set of discrete levels, producing visible steps in gradients. |
| **Sample-and-Hold** | A technique where one input sample is captured and its value is replicated across subsequent samples until the next capture point. |
| **Scanline** | A single horizontal line of pixels in a video frame; scanline darkening simulates the visible gaps between lines on a CRT display. |
| **Sixel** | A block-mosaic graphics encoding used by videotex and early terminal systems, subdividing character cells into a 2×3 grid. |
| **Videotex** | A family of pre-internet interactive information systems using telephone lines and dedicated terminals, including France's Minitel. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
