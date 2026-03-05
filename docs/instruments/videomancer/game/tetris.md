---
draft: true
sidebar_position: 307
slug: /instruments/videomancer/tetris
title: "Tetris"
image: /img/instruments/videomancer/tetris/tetris_hero.png
description: "Tetris implements the classic falling-block puzzle game entirely within FPGA logic."
---

import tetris_hero from '/img/instruments/videomancer/tetris/tetris_hero.png';
import tetris_animation from '/img/instruments/videomancer/tetris/tetris_animation.gif';
import tetris_control_panel from '/img/instruments/videomancer/tetris/tetris_control_panel.png';
import tetris_exercise1_result from '/img/instruments/videomancer/tetris/tetris_exercise1_result.gif';
import tetris_exercise2_result from '/img/instruments/videomancer/tetris/tetris_exercise2_result.gif';
import tetris_exercise3_result from '/img/instruments/videomancer/tetris/tetris_exercise3_result.gif';

# Tetris

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={tetris_hero} alt="Tetris hero image"/>
*Tetris rendering a mid-game playfield with row-based hue coloring, grid lines enabled, and a two-digit score display beside the playing area.*
<img src={tetris_animation} alt="Tetris animated output"/>
*Tetris output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Tetris implements the classic falling-block puzzle game entirely within FPGA logic. Seven tetrominoes — I, O, T, S, Z, L, and J — descend onto a 10×20 playfield where the player positions and rotates them using voltage-controlled potentiometers. Completed rows are cleared, the cells above collapse downward under gravity, and a two-digit BCD score tracks the number of lines removed. The playfield is rendered as a 480×960 pixel grid centered on screen, with each cell occupying a 48×48 pixel square.

The game's state lives in a 200-bit alive register — one bit per cell in the 10×20 grid — updated once per vertical sync interval. A 16-bit Galois LFSR selects the next piece type pseudo-randomly, with its seed influenced by the Next Seed pot for repeatable or varying sequences. The rendering pipeline examines each pixel to determine whether it falls within a locked cell, the active piece overlay, a grid line, the border, or the score display, then assigns luminance and optional row-based chrominance through a priority-encoded color mux.

Unlike traditional software implementations that run a game loop on a CPU, this Tetris executes entirely in synchronous clocked logic with zero BRAM usage. All game state, collision detection, line clearing, and score tracking happen within a single vsync-triggered process. The 6-stage rendering pipeline produces pixel-perfect output at full HD resolution with fixed latency, making the game playable through analog voltage control rather than discrete button presses.

---

## Quick Start

1. **Speed as difficulty**: The Drop Spd pot is the most direct difficulty control. Start slow to learn piece placement, then increase speed for challenge. The drop interval scales from approximately 60 frames at minimum to 4 frames at maximum.
2. **Hard drop for precision**: Use the Drop toggle's rising edge for instant placement once you have positioned and rotated the piece. This avoids waiting for the auto-drop timer and allows rapid stacking.
3. **Seed for repeatability**: In a performance context, setting Next Seed to a known position produces a repeatable piece sequence. Two Videomancers with identical seed settings will play the same game, enabling synchronized dual-screen compositions.

---

## Background

### The Tetromino as Combinatorial Object

A tetromino is a geometric shape composed of exactly four unit squares connected edge-to-edge. There are five distinct free tetrominoes (I, O, T, S, Z) plus two mirror pairs (L/J, S/Z) yielding seven one-sided pieces when reflections are counted as distinct. Tetris stores each piece as a 4×4 bitmap with four rotation states, accessed through a ROM array indexed by piece type (0–6) and rotation (0–3). The 4×4 grid is intentionally larger than any piece — the I piece is the longest at 4 cells — to allow all rotations to fit within a uniform data structure.

### Playfield as Bit Array

The 10×20 grid uses a flat bit-per-cell representation where each row is a 10-bit `std_logic_vector` and the full field is a 20-element array. This encoding is compact (200 flip-flops, no BRAM) and allows collision detection and line clearing through simple bitwise operations. A row is complete when all 10 bits are high — a single AND reduction. Gravity after a line clear is implemented as a downward shift of the row array, copying each row to the position below and inserting an empty row at the top.

### LFSR Piece Selection

The random piece generator uses a 16-bit Galois linear feedback shift register with taps at positions 16, 14, 13, and 11 (a maximal-length polynomial). The LFSR advances once per vsync, and the bottom 3 bits select a piece type (0–6); values of 7 wrap to 0. The Next Seed pot can reseed the LFSR when it reaches zero, allowing the player to influence the randomness of the piece sequence — a form of voltage-controlled stochastic composition.

### Raster Rendering Without Frame Buffers

The rendering pipeline operates per-pixel in real time, computing playfield membership, grid-cell coordinates, piece overlay, border detection, and score glyph lookup on every clock cycle. There is no frame buffer — the color mux makes its decision combinationally from the current pixel position and the 200-bit grid state. This is the same raster-chasing approach used by 1980s arcade hardware, where the display is painted one scanline at a time. The 6-clock pipeline latency is compensated by a sync delay chain that keeps video timing aligned with the rendered output.

### BCD Score and Dot-Matrix Font

The score is stored as two 4-bit BCD digits (tens and ones), counting from 00 to 99 before wrapping. Each digit is rendered using a 5×7 dot-matrix font ROM at 4× pixel scale, producing 20×28 pixel characters positioned to the right of the playfield. The font is a classic monospaced bitmap design stored as 10 entries of 7 rows of 5 bits each — the same glyph geometry used in LED matrix displays and early computer terminals.


---

## Signal Flow

```
┌─────────────────────────────────────────────────────┐
│  Video Timing Generator                             │
│  ├─ h_count, v_count (pixel position counters)      │
│  └─ vsync_start (game tick trigger)                 │
└───────────────┬─────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────┐
│  Game Logic (per-vsync)                             │
│  ├─ Piece position from pos_pot → column (0–8)      │
│  ├─ Piece rotation from rot_pot → 0–3               │
│  ├─ LFSR advance → next piece type (0–6)            │
│  ├─ Auto-drop timer (speed_pot → interval)          │
│  ├─ Hard drop edge detect (drop_trig)               │
│  ├─ Collision check (4×4 piece vs grid alive)       │
│  ├─ Lock piece into grid (200-bit register)         │
│  ├─ Row clear scan + gravity shift                  │
│  └─ BCD score increment                             │
└───────────────┬─────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────┐
│  Rendering Pipeline (per-pixel)                     │
│  ├─ Stage 1: input registers + sync edge detect     │
│  ├─ Stage 2: playfield coords, cell col/row         │
│  ├─ Stage 3: grid alive lookup + piece overlay      │
│  │           + border + score glyph check            │
│  ├─ Stage 4: color mux (cell/piece → hue/mono,      │
│  │           score → white, grid → dim, border)     │
│  ├─ Stage 5: interpolator input (mix control)       │
│  └─ Stage 6: output register                        │
└───────────────┬─────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────┐
│  Mix (3× interpolator_u) + Bypass                   │
│  └─ lerp(dry, wet, mix) → Output                   │
└─────────────────────────────────────────────────────┘
```

The critical design separation is between the game logic process — which runs once per vertical sync and modifies the 200-bit grid register, piece state, and score — and the rendering process, which runs every pixel clock and reads those registers without modifying them. This ensures the playfield never changes mid-frame, avoiding visual tearing. The collision detection loop iterates over the 4×4 piece bitmap and checks each occupied cell against both the grid bounds and the alive register, producing a single `v_can_drop` flag that gates all downward movement. The color mux assigns priority as: filled cell or active piece (highest), score glyph, grid line, border, background (lowest).

---

## Parameter Reference

<img src={tetris_control_panel} alt="Videomancer front panel with Tetris loaded"/>
*Videomancer's front panel with Tetris active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Drop Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls how quickly pieces descend automatically. The drop interval is computed by subtracting a scaled version of this pot from a base value, so higher settings produce shorter intervals and faster drops. At rest, pieces descend at a leisurely rate suitable for careful placement. Cranked high, they plummet almost immediately, demanding quick reflexes. This parameter functions as the game's difficulty dial — a direct voltage-to-challenge mapping.

---

#### Knob 2 — Position
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the horizontal column position of the active piece. The 10-bit register value is scaled to the range 0–8 (clamped so the rightmost 4×4 piece cells do not exceed the grid boundary). Because this is a continuous analog control rather than discrete left/right buttons, the piece can be swept across the playfield in a single gesture. Fine adjustments near column boundaries require steady hands, making the pot's mechanical response curve part of the gameplay feel.

---

#### Knob 3 — Rotate
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

Selects the rotation state of the active piece using four discrete steps mapped to 0°, 90°, 180°, and 270°. The top two bits of the register select one of the four ROM entries in the tetromino shape table. Each rotation is a pre-computed 4×4 bitmap — there is no runtime rotation algorithm. The stepped control mode makes each position a definite detent, avoiding ambiguity about which orientation is selected.

---

#### Knob 4 — Next Seed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Seeds the 16-bit Galois LFSR that generates the pseudo-random piece sequence. When the LFSR reaches zero, this pot's value is OR'd with 0x0001 to reseed it, ensuring the register never locks up. Different seed values produce entirely different piece sequences, allowing the player to "dial in" a repeatable game or continuously perturb the randomness. In a performance context, two players with identical seed settings will receive identical piece sequences.

---

#### Knob 5 — Field Hue
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Offsets the chrominance values assigned to filled cells when Color mode is active. Each row of the playfield receives a hue shifted by its row index multiplied by a fixed step, creating a rainbow gradient from top to bottom. This pot shifts the entire gradient around the color wheel — rotating the hue assignment so that the top row can start at any color. In Mono mode, this parameter has no visible effect since chrominance is locked to the neutral midpoint.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Sets the luminance level for all foreground elements: filled cells, the active piece, score digits, grid lines, and the border. Grid lines render at one-eighth brightness and the border at one-quarter brightness relative to this value, maintaining visual hierarchy. At zero, the entire playfield goes dark. At maximum, cells are rendered at full white. This parameter does not affect the background, which is always black.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Drop** | Off | On |
| **8 — Grid** | Off | On |
| **9 — Score** | Off | On |
| **10 — Color** | Mono | Hue |
| **11 — Bypass** | Off | On |

Toggle 7 provides a hard-drop trigger activated on its rising edge, instantly advancing the piece one row. Toggle 8 enables the 2-pixel grid lines that subdivide the playfield into visible cells. Toggle 9 enables the two-digit BCD score display rendered to the right of the playfield. Toggle 10 selects between monochrome (achromatic) and hue (row-based chrominance) coloring for filled cells. Toggle 11 bypasses all synthesis and passes the input signal through unchanged.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input signal and the synthesized game output using three parallel interpolators (Y, U, V). At minimum, the output is pure input video with no game visible. At maximum, the output is the full Tetris rendering. Intermediate positions superimpose the game at partial opacity over the source footage, allowing the playfield to float transparently over live video — useful for picture-in-picture style compositions.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore Tetris as a voltage-controlled visual instrument, progressing from basic gameplay through color manipulation to performance-oriented techniques.

### Exercise 1: First Lines

<img src={tetris_exercise1_result} alt="First Lines result"/>
*First Lines — simulated result across source images.*
**What You'll Create**: Clear three lines and observe the gravity mechanic and score counter.

1. **Set moderate speed**: Adjust Drop Spd to roughly one-third so pieces fall slowly enough to place deliberately.
2. **Enable display aids**: Turn on Grid and Score so you can see cell boundaries and track progress.
3. **Fill a row**: Use Position to sweep pieces across the bottom, using Rotate to orient them for tight packing.
4. **Complete a line**: When all 10 cells in a row are filled, the row vanishes and everything above shifts down by one.
5. **Watch the score**: Each cleared line increments the ones digit. Clear three lines total to complete the exercise.
6. **Hard drop**: Use the Drop toggle to accelerate placement once you are confident in the column and rotation.

**Key concepts**: 200-bit alive register, per-row AND reduction for line detection, gravity as row-array downshift, BCD scoring

---

### Exercise 2: Rainbow Playfield

<img src={tetris_exercise2_result} alt="Rainbow Playfield result"/>
*Rainbow Playfield — simulated result across source images.*
**What You'll Create**: Build a tall stack of partial rows to showcase the row-based hue gradient across the full playfield height.

1. **Enable hue mode**: Set Color to Hue and adjust Field Hue to a starting offset you find visually appealing.
2. **Slow the game down**: Set Drop Spd to minimum so pieces descend as slowly as possible.
3. **Stack without clearing**: Deliberately leave gaps in each row so no line completes. Build upward toward the top.
4. **Observe the gradient**: As the stack grows taller, more rows become visible and the chrominance gradient spans from top to bottom.
5. **Sweep the hue**: Slowly rotate Field Hue through its full range. The entire rainbow shifts around the color wheel in real time.
6. **Brightness sweep**: Lower Bright gradually to see the gradient shift into darker, more saturated tones, then raise it to watch the colors wash out toward pastel.

**Key concepts**: Row-index-based chrominance, hue pot as color wheel offset, U/V complement calculation, luminance-chroma interaction

---

### Exercise 3: Transparent Overlay

<img src={tetris_exercise3_result} alt="Transparent Overlay result"/>
*Transparent Overlay — simulated result across source images.*
**What You'll Create**: Superimpose the Tetris playfield over a live video source using the Mix fader.

1. **Connect a video source**: Feed a camera or playback signal into the Videomancer input.
2. **Set full game**: Ensure Bypass is Off and Mix is at 100%. The game renders at full opacity over black.
3. **Reduce Mix to ~60%**: The playfield becomes semi-transparent, revealing the source video beneath the game.
4. **Play a few lines**: The game is now visually composited over the source footage. Filled cells tint the underlying video.
5. **Try monochrome**: Switch Color to Mono. The achromatic cells act as luminance masks over the source material.
6. **Adjust Mix in real time**: Sweep the fader during gameplay. The playfield fades in and out of the source, creating a live compositing effect.

**Key concepts**: Interpolator-based wet/dry crossfade, per-channel lerp, synthesis-over-source compositing, luminance masking

---


## Tips

- **Hue as visual score**: Enable Color mode and leave rows partially filled. As the stack grows, the expanding rainbow gradient functions as a visual progress indicator — taller stacks reveal more of the color wheel.
- **Grid lines for alignment**: Enable Grid when learning the game to see cell boundaries clearly. Disable it for a cleaner abstract composition where only the filled cells and piece are visible.
- **Mix for compositing**: The fader allows Tetris to function as a video overlay. Set Mix to 50–70% to superimpose the game over live footage, creating an interactive picture-in-picture effect.
- **Rotation is quantized**: The Rotate pot uses `steps_4` mode, producing exactly four states. There is no interpolation between rotations — each step snaps to a pre-computed 4×4 bitmap. Turn the pot decisively to avoid lingering between detents.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alive Register** | The 200-bit (10×20) grid of flip-flops storing the playfield state, where each bit indicates whether a cell is occupied by a locked piece. |
| **BCD** | Binary-Coded Decimal; a number encoding where each decimal digit is stored as a separate 4-bit nibble, simplifying decimal display without binary-to-decimal conversion. |
| **Cell** | A single unit square in the 10×20 playfield grid, rendered as a 48×48 pixel block on screen. |
| **Collision Detection** | The process of checking whether a piece's occupied cells overlap with filled grid positions or exceed the playfield boundaries before allowing movement. |
| **Color Mux** | The priority-encoded output stage that selects luminance and chrominance based on whether the current pixel belongs to a filled cell, active piece, score glyph, grid line, border, or background. |
| **Dot-Matrix Font** | A 5×7 pixel bitmap font stored as ROM, used to render the score digits at 4× magnification. |
| **Galois LFSR** | A linear feedback shift register using XOR taps on the output bit, producing a maximal-length pseudo-random sequence with compact logic. |
| **Gravity** | The row-shifting mechanic that moves all rows above a cleared line down by one position, implemented as a sequential copy of the `std_logic_vector` array. |
| **Hard Drop** | An edge-triggered action that immediately advances the active piece one row downward, bypassing the auto-drop timer. |
| **Playfield** | The 480×960 pixel region (10×20 cells of 48×48 pixels each) centered on screen where the game is rendered. |
| **Tetromino** | A geometric shape composed of four unit squares connected edge-to-edge. Seven distinct tetrominoes (I, O, T, S, Z, L, J) comprise the standard piece set. |
| **Tetromino ROM** | A constant array storing 7 pieces × 4 rotations × 4 rows × 4 bits of bitmap data, encoding all possible piece shapes. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
