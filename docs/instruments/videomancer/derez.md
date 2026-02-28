---
draft: true
sidebar_position: 70
slug: /instruments/videomancer/derez
title: "Derez"
image: /img/instruments/videomancer/derez/derez_hero.png
---

import derez_hero from '/img/instruments/videomancer/derez/derez_hero.png';
import derez_before_after from '/img/instruments/videomancer/derez/derez_before_after.png';
import derez_control_panel from '/img/instruments/videomancer/derez/derez_control_panel.png';
import derez_exercise1_result from '/img/instruments/videomancer/derez/derez_exercise1_result.png';
import derez_exercise2_result from '/img/instruments/videomancer/derez/derez_exercise2_result.png';
import derez_exercise3_result from '/img/instruments/videomancer/derez/derez_exercise3_result.png';

# Derez

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={derez_hero} alt="Derez hero image"/>
*Derez corrupting spatial addressing and data bus integrity to produce geometric mirroring, bit-plane separation, and dead-line dropout artifacts.*
<img src={derez_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Derez applied.*

---

## Overview

Real memory corruption is never random. When a VRAM chip fails, the damage follows the physical architecture of the silicon — address lines stick, data bus pins float, row decoders misfire. The result is not noise but structured distortion: geometric folding, tiled repetition, banded posterization, and ruled lines of dead pixels that betray the binary skeleton of the display system.

Derez simulates these failure modes in hardware. Six processing stages run simultaneously — address bit corruption (XOR or stuck), data bus stuck bits, bit-plane spatial shift, and dead row/column injection — all governed by a 16-bit LFSR that can be frozen to a deterministic seed or left to animate frame by frame. The name comes from the Tron universe, where *deresolution* is the disintegration of a digital entity back into raw data. Here, an intact video signal is deresolved into the artifacts of its own storage medium.

At low settings, Derez introduces subtle geometric doubling and faint ruled lines — the barely perceptible hum of failing hardware. At high settings, the image shatters into tiled fragments, banded value clamps, and staggered bit-plane rainbows that look like a ROM dump rendered as pixels.

---

## Background

### VRAM Corruption and the Kill Screen

The most famous examples of address corruption in video hardware come from arcade kill screens. When Pac-Man reaches level 256, the 8-bit level counter overflows and corrupts the fruit drawing routine's memory read addresses. The result is not random garbage — it is the game's own tile graphics read from wrong locations, producing a structured collage of misplaced sprites. This happens because specific address bits are stuck or inverted, causing the hardware to fold, mirror, and repeat regions of tile memory. Derez's address corruption modes reproduce exactly this class of fault: XOR mode mirrors and folds the image by flipping address bits, while Stuck mode forces addresses high or low to create tiled repetition and spatial decimation.

### Glitch Art and Data Bending

Glitch art emerged in the 2000s as artists deliberately introduced faults into digital media — hex-editing JPEG headers, corrupting codec state, or physically damaging storage media. The aesthetic is not destruction but *structured* destruction: the artifacts reveal the hidden architecture of the medium. A corrupted JPEG shows the block boundaries of its DCT compression. A damaged CD skips along sector boundaries. Derez brings this practice to real-time video by offering precise control over which bits fail and how.

### Bit-Plane Graphics and Planar Memory

Early computer graphics systems stored images in bit planes — separate memory arrays for each bit of pixel depth. The Amiga's planar display memory, the Apple II's high-resolution mode, and bitmap-mode CGA all used this architecture. When one plane was corrupted or delayed relative to the others, the visual result was colored banding along edges where different bit weights separated spatially. Derez's bit-plane shift stage recreates this artifact by independently delaying each of the 10 luminance bits through separate shift registers, with the MSB getting zero delay and the LSB getting maximum delay.

### Stuck Data Buses

In digital electronics, a "stuck-at" fault is one of the fundamental failure modes. A data bus pin that is stuck high permanently forces its bit to 1; stuck low forces it to 0. The visual effect depends on which bit is stuck — a stuck MSB clamps half the dynamic range, while a stuck LSB is nearly invisible. Derez's stuck mask control lets you select exactly which bits are frozen, and the polarity toggle chooses stuck-high (OR mask) or stuck-low (AND-NOT mask). With animation enabled, the stuck mask rotates one position per frame, creating a scanning wave of corruption across the bit weights.

### ROM Dumps and Memory Viewers

Hex editors and ROM dump viewers display raw memory as grids of values. When viewed as pixel data, ROM contents become abstract patterns — repeating tile structures from graphics ROMs, sinusoidal waves from audio lookup tables, or apparently random textures from code segments. The visual language is unmistakable: ruled grids, hard-edged value bands, and periodic repetition at power-of-two intervals. Derez's combination of address corruption, data bus faults, and dead line injection produces imagery that inhabits this same visual territory.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├─ 1. Line Buffer Write ────────────────────────────────────────
│     Write Y/U/V at linear address (h_count)
│
├─ 2. Address Corruption ───────────────────────────────────────
│     Generate mask from Corrupt Bits + Bit Select
│     XOR mode:   read_addr = h_count XOR mask
│     Stuck mode:  High → read_addr = h_count OR mask
│                  Low  → read_addr = h_count AND (NOT mask)
│
├─ 3. Line Buffer Read ─────────────────────────────────────────
│     Read Y/U/V from corrupted address
│
├─ 4. Bit-Plane Shift (Y only) ─────────────────────────────────
│     10 independent shift registers (64 deep each)
│     Bit 9 (MSB): 0 delay → Bit 0 (LSB): max delay
│     Delay[i] = (9 − i) × plane_shift >> 4, clamped to 63
│
├─ 5. Data Bus Stuck Bits ──────────────────────────────────────
│     Stuck High: out = out OR stuck_hi_mask
│     Stuck Low:  out = out AND (NOT stuck_lo_mask)
│     All channels or Y only (toggle)
│     Animate: mask rotates left 1 bit per frame
│
├─ 6. Dead Line Injection ──────────────────────────────────────
│     LFSR(9:0) < dead_lines threshold → black pixel
│     Rows: LFSR advance per hsync
│     Columns: LFSR advance per pixel
│     Dead → Y=0, U=512, V=512
│
├─ 7. Wet/Dry Mix ──────────────────────────────────────────────
│     3× interpolator_u crossfade (dry=delayed input, wet=processed)
│
└── Output Video (YUV 4:4:4)
```

The address corruption operates on horizontal pixel positions within a single scan line — the line buffer stores one line of 1024 pixels, written linearly and read from a corrupted address. This means all mirroring, folding, and tiling effects are horizontal. The bit-plane shift is also horizontal, delaying bit planes by pixel positions along the scan line. Dead line injection is the only stage that operates on both axes — rows are detected at hsync boundaries and columns at per-pixel LFSR ticks, but the detection is binary (alive or dead), not a spatial transform.

The LFSR is re-seeded from the Glitch Seed pot at every vsync. In Static mode this produces identical corruption patterns every frame. In Animate mode, the data bus stuck mask rotates one position per frame, creating an evolving corruption wave across bit weights while the spatial corruption pattern (address, dead lines) remains deterministic per seed.

---

## Parameter Reference

<img src={derez_control_panel} alt="Videomancer front panel with Derez loaded"/>
*Videomancer's front panel with Derez active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Corrupt Bits
| Property | Value |
|----------|-------|
| Range | 0 – 10 |
| Default | 0 |

Controls the number of address bits affected by corruption. The pot's upper 3 bits select 0 through 7 bits. At zero, no address bits are modified and the line buffer reads back the original pixel positions. Each additional bit doubles the spatial scale of the corruption — one bit creates fine pixel-level interleaving, while seven bits fold or tile the image across the entire line width. The effect is dramatic: even a single corrupted address bit mirrors or offsets half the image.

---

#### Knob 2 — Bit Select
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Selects which address bits are targeted. The pot's upper 3 bits set a bit offset (0–7), and the mask window set by Corrupt Bits starts from that offset. Sweeping this control slides the corruption window through the address space — low offsets affect the least significant address bits (fine spatial detail, pixel-level interleaving), while high offsets affect the most significant bits (large-scale mirroring and folding). The interplay between Corrupt Bits and Bit Select lets you target corruption precisely in the spatial frequency domain.

---

#### Knob 3 — Stuck Mask
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets the data bus stuck-bit mask. Each bit in the 10-bit register value corresponds to one bit of the pixel data bus. The Stuck Polarity toggle determines whether set bits force data lines high (OR mask) or low (AND-NOT mask). Stuck-high on the MSB clamps all values above 512; stuck-low on the MSB forces all values below 512. Multiple stuck bits create successively harsher banding and posterization. With animation enabled, this mask rotates left one position per frame, sweeping the corruption across bit weights.

---

#### Knob 4 — Plane Shift
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the magnitude of bit-plane spatial displacement. At zero, all 10 luminance bit planes are aligned and the image appears normal. As the value increases, lower-order bit planes are progressively delayed relative to higher-order planes — the MSB (bit 9) always has zero delay, while the LSB (bit 0) receives the maximum delay. This creates rainbow-like banding along horizontal edges where the bit weights separate spatially, producing the distinctive visual signature of planar memory corruption.

---

#### Knob 5 — Dead Lines
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets the probability threshold for dead line injection. The 16-bit LFSR's lower 10 bits are compared against this value — when the LFSR output falls below the threshold, the current row (or column) is killed. At zero, no lines are dead. As you increase the pot, more lines are replaced with black (Y=0) and neutral color (U=V=512). At maximum, nearly every line is dead and the image disappears into ruled darkness.

---

#### Knob 6 — Glitch Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 512 |

Seeds the 16-bit LFSR that drives dead line positioning and animation. The seed is loaded at every vertical sync, so in Static mode the dead line pattern is perfectly deterministic and repeatable for a given seed value. Different seeds produce completely different spatial distributions of dead lines but with the same density (set by Dead Lines). Sweeping the seed while watching the output reveals the LFSR's pseudo-random sequence as shifting patterns of ruled lines.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Addr Mode** | XOR | Stuck |
| **8 — Stuck Pol** | High | Low |
| **9 — Dead Axis** | Rows | Columns |
| **10 — Animate** | Static | Animate |
| **11 — Channel** | All | Y Only |

Toggles 7–11 configure the corruption modes. Toggles 7 and 8 interact as a pair to set the address corruption behavior (XOR with bit-flip, or Stuck with polarity). Toggle 9 selects the dead line axis. Toggle 10 enables frame-to-frame animation of the stuck mask. Toggle 11 restricts data bus corruption to the Y channel only, leaving chrominance intact for color-preserving glitch effects.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the delayed original signal and the fully processed output. At maximum (100%), the output is entirely the corrupted signal. At zero, the original signal passes through unmodified. Intermediate values blend the two, which can create ghostly double-exposure effects where the original image is visible beneath the corrupted version. The dry signal is delayed by 8 clock cycles to align with the processing pipeline latency.

---

## Guided Exercises

These exercises progress from single-stage corruption to full multi-stage failure simulation. Each isolates a different failure mode before combining them.

### Exercise 1: Address Line Failure

<img src={derez_exercise1_result} alt="Address Line Failure result"/>
*Address Line Failure — simulated result across source images.*
**Source**: A test pattern or graphic with strong geometric structure — grid patterns, text, or architectural footage.

**Objective**: Learn how XOR and Stuck address corruption modes create different spatial distortion patterns.

1. **Single bit XOR**: Set Corrupt Bits to ~15% (1 bit) and Bit Select to ~85% (high offset targeting MSB). Observe the image folding at the horizontal midpoint — the right half mirrors onto the left.
2. **Multiple bit XOR**: Increase Corrupt Bits to ~30% (2 bits). The folding becomes more complex, with nested mirror zones.
3. **Sweep Bit Select**: Hold Corrupt Bits at ~30% and slowly sweep Bit Select from maximum to minimum. Watch the folding pattern shift from large-scale mirroring (MSBs) to fine pixel interleaving (LSBs).
4. **Switch to Stuck mode**: Toggle Addr Mode to Stuck. The mirroring transforms into tiling and repetition. With Stuck Polarity on High, regions are offset; on Low, regions are decimated.
5. **Compare polarities**: Toggle Stuck Polarity back and forth to see the difference between force-high (offset/repeat) and force-low (tiling/decimation).

**Key concepts**: XOR produces mirroring by flipping address bits, Stuck produces tiling by clamping address bits, MSB corruption creates large-scale geometric distortion while LSB corruption creates fine detail interleaving

---

### Exercise 2: Data Bus Failure and Bit-Plane Separation

<img src={derez_exercise2_result} alt="Data Bus Failure and Bit-Plane Separation result"/>
*Data Bus Failure and Bit-Plane Separation — simulated result across source images.*
**Source**: A camera feed or footage with smooth gradients and recognizable subjects.

**Objective**: Explore data bus stuck bits, animation, and bit-plane spatial shift.

1. **Stuck MSB high**: Set Stuck Mask to ~50% (setting bit 9). All dark values jump to mid-range. The image looks washed out with hard clipping.
2. **Stuck LSB low**: Switch Stuck Polarity to Low and reduce Stuck Mask to ~5% (affecting only the lowest bits). Subtle banding appears in smooth gradients.
3. **Animate the mask**: Toggle Animate to on. The stuck-bit pattern rotates through the 10 bit positions, creating a scanning wave of corruption that cycles every 10 frames.
4. **Bit-plane shift**: Return Stuck Mask to 0%. Slowly increase Plane Shift from zero. On horizontal edges, rainbow-like color banding appears as the lower bit planes shift right relative to the MSBs.
5. **Y Only mode**: Toggle Channel to Y Only. The bit-plane separation affects only brightness — chrominance remains aligned, preserving color fidelity.

**Key concepts**: Stuck-high clamps the lower half of the dynamic range, stuck-low clips the upper half, bit-plane shift separates luminance into independently delayed layers producing edge banding

---

### Exercise 3: Full Memory Failure

<img src={derez_exercise3_result} alt="Full Memory Failure result"/>
*Full Memory Failure — simulated result across source images.*
**Source**: Any active video — the more visually complex, the more interesting the corruption patterns.

**Objective**: Combine all corruption stages for comprehensive memory failure simulation.

1. **Address corruption**: Set Corrupt Bits ~25%, Bit Select ~50%, Addr Mode to XOR. The image folds and mirrors.
2. **Data bus faults**: Add Stuck Mask ~30% with Stuck Polarity High. Value clamping bands appear over the mirrored image.
3. **Bit-plane shift**: Increase Plane Shift to ~40%. Edges develop staggered banding as bit planes separate.
4. **Dead rows**: Set Dead Lines to ~20%, Dead Axis to Rows. Horizontal black bars appear randomly across the image.
5. **Dead columns**: Switch Dead Axis to Columns. The ruled bars become vertical stripes.
6. **Animate**: Enable Animate. The stuck mask rotates frame-to-frame while dead lines remain deterministic.
7. **Seed exploration**: Slowly sweep Glitch Seed while watching the dead line pattern reorganize. Each seed produces a unique spatial distribution.
8. **Mix blend**: Pull the Mix fader down to ~60% to ghost the original image beneath the corruption.

**Key concepts**: Multiple failure modes compound — address corruption distorts geometry, stuck bits distort values, plane shift separates bit weights, dead lines mask regions, and the LFSR seed determines the spatial pattern

---


## Tips

- **Start with one stage**: Isolate each corruption mode before combining. Address corruption alone produces dramatic geometric effects — add data bus and plane shift one at a time.
- **Seed is your recall**: In Static mode, the Glitch Seed pot fully determines the dead line pattern. Note your seed values for repeatable compositions.
- **MSB vs LSB corruption**: Address or data bus corruption of the most significant bits creates dramatic, large-scale visual changes. Corruption of the least significant bits is subtle and textural. Bit Select and Stuck Mask let you target either end.
- **Y Only for color preservation**: Set Channel to Y Only to corrupt brightness while preserving the original color palette — a useful constraint for keeping the output recognizable.
- **Animate for evolving textures**: The rotating stuck mask creates a 10-frame cycle of scanning corruption. Combined with static address corruption, this produces a structured evolution rather than random noise.
- **Low Mix for ghosting**: Pulling the Mix fader to 40–60% ghosts the original image beneath the corruption, creating a double-exposure effect that preserves spatial context.
- **Plane Shift on edges only**: Bit-plane shift is most visible at luminance transitions. On flat fields it is nearly invisible. Feed high-contrast material to see the effect clearly.
- **Dead Lines as ruled texture**: At low thresholds, dead lines create ruled horizontal or vertical textures overlaid on the image — a structured grid effect distinct from noise.

---

## Glossary

| Term | Definition |
|------|------------|
| **Address Corruption** | Modifying the read address of a memory buffer so that pixels are read from incorrect locations, producing spatial mirroring, folding, tiling, or decimation. |
| **AND-NOT Mask** | A bitwise operation that clears specified bits to zero; used for stuck-low address and data bus simulation. |
| **Bit Plane** | A single binary layer of a multi-bit pixel value; in a 10-bit signal, there are 10 bit planes from MSB (weight 512) to LSB (weight 1). |
| **BRAM** | Block RAM; dedicated memory on the FPGA used for line buffer storage. |
| **Data Bus** | The parallel conductors carrying pixel values; a stuck data bus pin permanently forces one bit to a fixed state. |
| **Kill Screen** | A game-breaking display corruption caused by counter overflow or address bus failure, most famously in Pac-Man level 256. |
| **LFSR** | Linear Feedback Shift Register; a hardware pseudo-random number generator using XOR feedback taps, producing a deterministic sequence from a given seed. |
| **OR Mask** | A bitwise operation that forces specified bits to one; used for stuck-high address and data bus simulation. |
| **Shift Register** | A chain of flip-flops that delays a signal by a fixed number of clock cycles; Derez uses 10 independent 64-deep shift registers for bit-plane delay. |
| **Stuck-At Fault** | A hardware failure mode where a signal line is permanently fixed to logic 0 or logic 1, regardless of the intended value. |
| **XOR** | Exclusive OR; a bitwise operation that flips bits where the mask is 1, used for address mirroring and folding. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
