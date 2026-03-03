---
draft: true
sidebar_position: 156
slug: /instruments/videomancer/kaleidoscope
title: "Kaleidoscope"
description: "Kaleidoscope is a faithful recreation of Li-Chen Wang's legendary 1976 demo for the Cromemco Dazzler — one of the earliest consumer video graphics boards."
---

import kaleidoscope_hero from '/img/instruments/videomancer/kaleidoscope/kaleidoscope_hero.png';
import kaleidoscope_animation from '/img/instruments/videomancer/kaleidoscope/kaleidoscope_animation.gif';
import kaleidoscope_control_panel from '/img/instruments/videomancer/kaleidoscope/kaleidoscope_control_panel.png';
import kaleidoscope_exercise1_result from '/img/instruments/videomancer/kaleidoscope/kaleidoscope_exercise1_result.png';
import kaleidoscope_exercise2_result from '/img/instruments/videomancer/kaleidoscope/kaleidoscope_exercise2_result.png';
import kaleidoscope_exercise3_result from '/img/instruments/videomancer/kaleidoscope/kaleidoscope_exercise3_result.png';

# Kaleidoscope

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={kaleidoscope_hero} alt="Kaleidoscope hero image"/>
*Kaleidoscope generating a 4-way symmetric color pattern on a 64x64 grid, with the Cromemco Dazzler 16-color palette painting concentric shapes across the display.*
<img src={kaleidoscope_animation} alt="Kaleidoscope animated output"/>
*Kaleidoscope output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Kaleidoscope is a faithful recreation of Li-Chen Wang's legendary 1976 demo for the Cromemco Dazzler — one of the earliest consumer video graphics boards. The original program fit in just 127 bytes of 8080 assembly and produced mesmerizing, endlessly evolving symmetric patterns on a 64x64 pixel display using only 16 colors. It was so captivating that it reportedly stopped traffic on New York City's Fifth Avenue when displayed in a storefront window. Videomancer's FPGA implementation preserves the original algorithm's elegant simplicity while presenting the output on modern HD video infrastructure.

The core algorithm is startlingly minimal. Two 8-bit coordinates (X and Y) are updated each iteration via a pair of masked shift-and-add operations: Y advances by a masked fraction of X, then X retreats by the same masked fraction of the new Y. The resulting coordinate, reduced to 5 bits in each axis, is plotted with 4-way mirror symmetry across the grid center. Colors cycle from 15 down to 1, with alternating iterations painting black — producing the characteristic interleaved color-and-void pattern. After 64 iterations at one color, the coordinates nudge by one unit and the next color begins. After all 15 colors have painted their 64 plots, the mask value increments, fundamentally altering the geometry of subsequent patterns.

The mask is the key to visual variety. It determines which bits of the shifted coordinate participate in the feedback equation. Low mask values produce simple, repetitive structures; high mask values create chaotic, space-filling trajectories. Because the mask auto-increments through all 256 values before cycling, the Kaleidoscope passes through the full spectrum of geometric complexity — from sparse radial lines through dense fractal-like tilings — in a continuous, hypnotic evolution.

---

## Background

### The Cromemco Dazzler

The Cromemco Dazzler, introduced in February 1976, was among the first affordable video graphics boards for personal computers. Designed by Harry Garland and Roger Melen at Cromemco (a company founded in a Stanford dormitory — Crothers Memorial Hall), the Dazzler plugged into the S-100 bus of an Altair 8800 or IMSAI 8080 and produced a 64x64 pixel display with either 16 colors or 512x512 monochrome resolution. The video buffer occupied 2 KB of system memory (addresses 0200h–09FFh), organized as four 32x32 quadrant pages. At a time when most microcomputers communicated through blinking LEDs and toggle switches, the Dazzler was a revelation.

### Li-Chen Wang's 127 Bytes

Li-Chen Wang, already known for creating Palo Alto Tiny BASIC, wrote Kaleidoscope as a demonstration program sold by Cromemco for $15 on paper tape. The entire program fits in 127 bytes of Intel 8080 machine code — fewer bytes than most HTTP headers today. Wang exploited the Dazzler's peculiar memory layout to achieve 4-way symmetry with minimal computation: the four quadrant pages starting at 0200h, 0400h, 0600h, and 0800h naturally mirror when addressed with complemented coordinates. The algorithm uses no multiplication, no division, no lookup tables — just shifts, masks, additions, and one complement operation per axis.

### Iterated Coordinate Feedback

The Kaleidoscope's visual complexity arises from a simple two-variable recurrence relation. Each iteration updates `Y += (X >> 2) & mask` then `X -= (Y >> 2) & mask`. This is structurally similar to a 2D linear congruential generator, but with the masking operation introducing nonlinear interactions between bit positions. The trajectory of (X, Y) through the 256x256 coordinate space depends entirely on the mask value: some masks produce short cycles (the coordinate returns to its starting point after a few dozen iterations), while others produce long, non-repeating orbits that fill large regions of the grid. The bit-level AND operation creates abrupt transitions between mask values — a single bit change can transform a simple orbit into a chaotic one.

### Mirror Symmetry and the Grid

Wang's 4-way symmetry exploits the Dazzler's page-based memory architecture, but the visual effect transcends implementation convenience. Each plotted pixel appears simultaneously in all four quadrants, creating bilateral symmetry across both the horizontal and vertical axes. This produces the kaleidoscopic appearance that gives the program its name — genuine optical kaleidoscopes work by the same principle of multi-axis reflection. The resulting patterns have the visual weight and balance of mandalas, snowflakes, and other naturally symmetric forms, emerging from an algorithm that contains no concept of symmetry whatsoever — only addressing arithmetic.

### Palette and Color Cycling

The Cromemco Dazzler's 16-color palette was an RGBI system: 3 bits of RGB with an additional intensity bit, producing 8 dim and 8 bright variants of each base color (including two blacks and two whites that are visually identical). Videomancer's implementation maps this palette to BT.601 YUV values, preserving the original Dazzler color character. The color cycling mechanism — painting 64 pixels at each of 15 non-black colors, with alternating black iterations — creates layered structures where newer colors overwrite older ones. As the mask evolves, earlier color layers are partially erased and replaced, producing the characteristic depth and visual history that makes Kaleidoscope patterns feel geological in their layered accumulation.


---

## Signal Flow

```
Synthesis Engine
|
+-- Parameter Mapping ------------------------------------------------
|   +- registers_in(0)  -> Speed (iterations per frame)
|   +- registers_in(1)  -> Seed X (initial X coordinate)
|   +- registers_in(2)  -> Seed Y (initial Y coordinate)
|   +- registers_in(3)  -> Mask (coordinate feedback AND mask)
|   +- registers_in(4)  -> Hue Shift (palette index rotation)
|   +- registers_in(5)  -> Brightness (Y channel scaling)
|   +- registers_in(6)  -> Toggles (run, auto mask, reset, grid, bypass)
|   +- registers_in(7)  -> Mix
|
+-- Iteration Engine (per vsync, when Run active) --------------------
|   +- 1. Coordinate Update
|   |      Y_new = Y + ((X >> 2) AND mask)
|   |      X_new = X - ((Y_new >> 2) AND mask)
|   +- 2. Pixel Address    (X_new[7:3], Y_new[7:3] -> 5-bit grid pos)
|   +- 3. Color Select     (color_ctr odd -> black, even -> color[4:1])
|   +- 4. Hue Shift        (non-black colors rotated by Hue Shift pot)
|   +- 5. 4-Way Mirror Write (4 FB addresses per iteration)
|   |      (+px, +py)  (+px, -py)  (-px, +py)  (-px, -py)
|   +- 6. Iteration Count  (64 per color -> decrement color counter)
|   +- 7. Color Cycle      (31 down to 1, then mask++)
|   +- 8. Frame Budget     (limited iterations per frame via Speed pot)
|
+-- Framebuffer (64x64 x 4-bit) -------------------------------------
|   +- Write: engine writes 4 mirrored pixels per iteration
|   +- Read:  rasterizer reads sequentially during active video
|
+-- Rasterizer (per pixel) ------------------------------------------
|   +- 9. Cell Lookup      (cell_col, cell_row -> FB read address)
|   +- 10. Palette LUT     (4-bit color index -> 10-bit YUV)
|   +- 11. Brightness Scale (palette Y * bright_pot / 1024)
|   +- 12. Grid Lines      (cell_px=0 or cell_py=0, when enabled)
|
+-- Output Stage ----------------------------------------------------
|   +- 13. Interpolator Mix  (3x interpolator_u wet/dry)
|
+-- Sync Pipeline ---------------------------------------------------
|   +- 8-clock shift register (hsync, vsync, avid, field)
|
+-- Bypass ----------------------------------------------------------
    +- Select processed or input signal
```

The iteration engine and the rasterizer operate in separate clock domains of the same process. The engine runs during the vsync blanking interval, advancing the Kaleidoscope state by writing new pixel colors to the 64x64 framebuffer. The rasterizer reads the framebuffer during active video, mapping each cell to a 30x16 pixel block on screen. Because writes happen during blanking and reads happen during active video, there is no read-write contention.

Each iteration produces five clock cycles of work: one cycle to compute the new coordinates and determine the color, then four cycles to write the four mirrored copies to the framebuffer. The Speed knob controls how many of these 5-cycle iterations execute per frame, governing the rate at which the pattern evolves. At maximum speed, over 100 iterations advance per frame; at minimum, only a handful — producing glacially slow evolution that lets each individual pixel placement be observed.

---

## Parameter Reference

<img src={kaleidoscope_control_panel} alt="Videomancer front panel with Kaleidoscope loaded"/>
*Videomancer's front panel with Kaleidoscope active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Speed controls how many Kaleidoscope iterations execute during each frame's vsync blanking interval. Higher values produce faster pattern evolution, with new colors and shapes appearing rapidly. Lower values slow the evolution to a crawl, making each individual pixel placement visible as it happens. At moderate settings (around 50%), the pattern evolves at roughly the same pace as the original 1976 program running on a 2 MHz 8080 processor — the historically authentic experience.

---

#### Knob 2 — Seed X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Seed X sets the initial X coordinate when the Reset toggle is activated. Together with Seed Y, it determines the starting point of the Kaleidoscope trajectory through its 256x256 coordinate space. Different seed positions produce different initial pattern geometries even at the same mask value, because the coordinate feedback path depends on the current (X, Y) position. The lower 8 bits of this 10-bit pot are used directly as the initial X byte value.

---

#### Knob 3 — Seed Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Seed Y sets the initial Y coordinate when Reset is activated. It works identically to Seed X but for the vertical coordinate. The combination of Seed X and Seed Y determines the full starting state of the system. Sweeping Seed Y while holding Seed X constant produces a family of related starting conditions that diverge as the iteration progresses — small initial differences are amplified by the masked feedback, producing visibly different patterns within a few dozen iterations.

---

#### Knob 4 — Mask
| Property | Value |
|----------|-------|
| Range | 0 – 255 |
| Default | 0 |

Mask directly sets the 8-bit AND mask used in the coordinate feedback equation when Auto Mask is set to Manual. The mask is the most powerful visual control: it determines which bit positions of the shifted coordinate contribute to the feedback. A mask of 0x00 produces no movement (delta is always zero). Low mask values like 0x01 or 0x03 create simple, repetitive radial patterns. Higher mask values introduce more bit interactions, creating increasingly complex and eventually chaotic trajectories. The full 8-bit range (0–255) is mapped from the 10-bit pot's upper bits.

---

#### Knob 5 — Hue Shift
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Hue Shift rotates the palette index for non-black pixels. The lower 4 bits of the pot value are added to each color index before the palette lookup, cycling through the 16-color Dazzler palette. This recolors the entire Kaleidoscope pattern without changing its geometry. A shift of 0 produces the original Dazzler color ordering; other values remap colors — for example, what was originally blue might appear as green or red. Because palette index 0 (black) is preserved, the spatial structure of color-versus-void is maintained regardless of the shift.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Bright scales the luminance output of all palette colors. The palette Y value is multiplied by the Bright pot value and the result is divided by 1024 (a 10-bit shift). At maximum brightness, palette whites reach near-peak luminance. At minimum, the entire pattern fades to black. This control is useful for matching the Dazzler output level to whatever is being mixed behind it via the fader, or for creating subtle, dim patterns that add texture without overwhelming the source video.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Run** | Pause | Run |
| **8 — Auto Mask** | Manual | Auto |
| **9 — Reset** | Off | Reset |
| **10 — Grid** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into three functional groups. Run and Reset control the iteration engine's execution: Run gates per-frame iteration, Reset re-initializes coordinates and optionally the mask. Auto Mask selects between the manual Mask pot and the original auto-incrementing behavior. Grid and Bypass are display controls — Grid renders cell boundaries as dim white lines, and Bypass routes input video directly to the output. Note that Reset is edge-triggered: the grid re-seeds on the rising edge of the toggle activation, so it acts as a momentary trigger.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix controls the wet/dry blend between the Kaleidoscope synthesis output and the input video signal. At full mix, only the Kaleidoscope pattern is visible against the default input background. Reducing mix fades the input video into view behind the pattern, creating a colored overlay effect. At zero mix, the Kaleidoscope is invisible and only the input signal passes through. The mix engages three interpolator_u instances for independent Y, U, and V channel blending.

---

## Guided Exercises

These exercises explore the Kaleidoscope's sensitivity to mask values, the effect of seed positions on pattern geometry, and the use of hue shifting to recolor the classic Dazzler palette.

### Exercise 1: Classic Dazzler Experience

<img src={kaleidoscope_exercise1_result} alt="Classic Dazzler Experience result"/>
*Classic Dazzler Experience — simulated result across source images.*
**Objective**: Reproduce the authentic 1976 Cromemco Dazzler Kaleidoscope experience with auto-incrementing mask and default palette.

1. Set Auto Mask to Auto for the original mask sweep behavior.
2. Set Speed to about 50% for historically authentic evolution rate.
3. Set Brightness to about 75% for vivid but not overdriven colors.
4. Leave Hue Shift at center (50%) — no palette rotation.
5. Disable Grid for the clean Dazzler look.
6. Set Mix to 100% for pure synthesis output.
7. Toggle Reset, then return Reset to Off.
8. Set Run to Run.
9. Watch as the mask auto-increments through all 256 values. Notice how simple radial patterns at low masks give way to complex, space-filling structures at higher masks before the cycle repeats.

**Key concepts**: Auto mask sweep, color cycling, 4-way symmetry, mask-dependent geometry, coordinate feedback

---

### Exercise 2: Manual Mask Exploration

<img src={kaleidoscope_exercise2_result} alt="Manual Mask Exploration result"/>
*Manual Mask Exploration — simulated result across source images.*
**Objective**: Manually explore specific mask values to understand how each bit position affects pattern geometry.

1. Set Auto Mask to Manual.
2. Set Speed to about 30% for detailed observation.
3. Set Mask to minimum (0). Notice no pattern evolves — the AND mask zeros all feedback.
4. Slowly increase Mask. At very low values (around 1–3%), observe simple radial spoke patterns.
5. Continue increasing. At moderate values (around 25–50%), patterns become more complex with interlocking arcs.
6. At high values (around 75–100%), the coordinate trajectory becomes chaotic and fills the grid densely.
7. Toggle Reset between mask changes to see each geometry from a fresh start.
8. Enable Grid to count exactly how many unique cells each mask value fills.

**Key concepts**: Manual mask control, bit-position geometry, simple vs chaotic trajectories, coordinate space coverage

---

### Exercise 3: Palette Cycling and Overlay

<img src={kaleidoscope_exercise3_result} alt="Palette Cycling and Overlay result"/>
*Palette Cycling and Overlay — simulated result across source images.*
**Objective**: Use Hue Shift to recolor the Kaleidoscope pattern and blend it as a textured overlay at partial mix.

1. Set Auto Mask to Auto for continuous evolution.
2. Set Speed to about 60% for lively animation.
3. Set Brightness to about 90% for vivid color output.
4. Slowly sweep Hue Shift from minimum to maximum. Watch the entire pattern recolor as palette indices rotate — the spatial structure remains identical while colors permute.
5. Find a hue setting that produces a pleasing color combination.
6. Reduce Mix to about 40% to blend the Kaleidoscope with input video.
7. Observe how the evolving colored pattern creates a dynamic, retro-styled texture over the source.
8. Try different Hue Shift values at the same Mix level to find complementary overlays.

**Key concepts**: Palette rotation, color remapping, partial mix, synthesis overlay, complementary color selection

---


## Tips

- **Start with Auto Mask**: The auto-incrementing mask is the heart of the classic Kaleidoscope experience. Let it sweep through all 256 values before switching to manual exploration.
- **Low masks for structure**: Mask values below about 15 produce the most visually distinctive, recognizable geometric patterns — radial spokes, concentric rings, and symmetric tilings.
- **High masks for chaos**: Mask values above 200 produce dense, space-filling trajectories that look more like noise. The visually interesting range is typically in the middle.
- **Reset doesn't clear**: The framebuffer retains old pixel data when Reset re-seeds the coordinates. This creates visual transitions where new patterns overwrite old ones layer by layer — an artistically interesting effect.
- **Seed position matters**: Different Seed X and Seed Y values produce different initial trajectories. Even small seed changes can dramatically alter the resulting pattern at the same mask value.
- **Hue Shift for variety**: The Dazzler palette has strong personality — cycling through Hue Shift values radically changes the mood from warm earth tones to cool blues to vivid primaries.
- **Grid for analysis**: Enable the grid overlay when studying how the algorithm distributes pixels across the 64x64 field. The grid reveals the discrete Dazzler pixel structure that gives the program its retro character.
- **Partial mix for depth**: At 30–50% mix, the Kaleidoscope pattern creates a vivid colored texture over input video — excellent for retro-styled visual performances.

---

## Glossary

| Term | Definition |
|------|------------|
| **8080** | Intel 8080 microprocessor, the CPU used in the IMSAI 8080 and Altair 8800 computers that hosted the Cromemco Dazzler. |
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric, used here for the 64x64x4-bit framebuffer. |
| **Coordinate Feedback** | The iterative update rule where X and Y modify each other through masked shift-and-add, producing the Kaleidoscope's characteristic trajectories. |
| **Cromemco Dazzler** | One of the first consumer video graphics boards (1976), producing 64x64 color or 512x512 monochrome display via the S-100 bus. |
| **LFSR** | Linear Feedback Shift Register; used here only for LFSR-like coordinate evolution via the masked feedback equation. |
| **Mask** | An 8-bit AND mask applied to the shifted coordinate in the feedback equation, controlling which bit positions participate; the primary source of pattern variety. |
| **Mirror Symmetry** | The 4-way reflection that plots each computed pixel in all four quadrants simultaneously, producing bilateral symmetry across both axes. |
| **Palette** | The 16-entry color lookup table mapping 4-bit indices to YUV video values, based on the Dazzler's RGBI color scheme. |
| **RGBI** | Red-Green-Blue-Intensity; the 4-bit color encoding used by the Cromemco Dazzler, with 3 base color bits and 1 intensity/brightness bit. |
| **S-100 Bus** | The 100-pin bus standard used by early microcomputers including the Altair 8800 and IMSAI 8080; the Dazzler connected via this bus. |
| **YUV** | Color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
