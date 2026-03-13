---
draft: true
sidebar_position: 273
slug: /instruments/videomancer/sketch
title: "Sketch"
image: /img/instruments/videomancer/sketch/sketch_hero.png
description: "The Etch A Sketch is one of the most recognizable toys in history, introduced by the Ohio Art Company in 1960."
---

import sketch_hero from '/img/instruments/videomancer/sketch/sketch_hero.png';
import sketch_animation from '/img/instruments/videomancer/sketch/sketch_animation.gif';
import sketch_control_panel from '/img/instruments/videomancer/sketch/sketch_control_panel.png';
import sketch_exercise1_result from '/img/instruments/videomancer/sketch/sketch_exercise1_result.gif';
import sketch_exercise2_result from '/img/instruments/videomancer/sketch/sketch_exercise2_result.gif';
import sketch_exercise3_result from '/img/instruments/videomancer/sketch/sketch_exercise3_result.gif';

# Sketch

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<img src={sketch_hero} alt="Sketch hero image"/>
*Sketch rendering a freehand drawing traced across a 96x54 canvas grid, with a cursor marker and luminous strokes over dark background.*
<img src={sketch_animation} alt="Sketch animated output"/>
*Sketch output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

The Etch A Sketch is one of the most recognizable toys in history, introduced by the Ohio Art Company in 1960. Its mechanical drawing interface — two knobs controlling horizontal and vertical stylus movement through aluminum powder — has become an icon of constrained creativity. Videomancer's Sketch program digitizes this concept on a 96x54 cell canvas where each cell occupies 20x20 pixels at 1080p. Two potentiometers control the cursor position, and the pen continuously draws or erases as the cursor moves across the grid.

The canvas is stored as a 5184-bit register array — one bit per cell — with the pen writing or clearing bits as the cursor traverses the grid. Pen Size (Knob 3) controls the brush width from 1 to 4 cells, allowing both fine detail and broad strokes. An optional fade mechanism (Knob 4) gradually dims older strokes over time, creating a trail decay effect. The Pen toggle switches between Draw mode (setting bits) and Erase mode (clearing bits), and a Cursor Visible toggle optionally highlights the current cursor position with a blinking or solid marker.

At full mix, Sketch displays the canvas drawing on a black background. Reducing the mix fader blends the drawing with input video, creating a live annotation overlay where the performer draws directly over moving footage. The grid toggle shows cell boundaries, and the color toggle switches between monochrome white strokes and hue-tinted rendering.

---

## Quick Start

1. **Slow sweeps for clean lines**: Move the cursor knobs slowly to draw continuous lines without gaps. Rapid knob turns may skip cells, producing dotted or broken strokes.
2. **Grid for precision**: Enable Grid when precision matters — the cell boundaries show exactly where each mark will be placed.
3. **Erase selectively**: Unlike the original Etch A Sketch, you can selectively erase portions of your drawing without clearing the entire canvas.

---

## Background

### The Original Etch A Sketch

André Cassagnes invented the Etch A Sketch (originally named L'Ecran Magique) in the late 1950s, and Ohio Art acquired the rights in 1959. The toy's defining constraint — the inability to draw diagonal lines easily, and the shake-to-erase reset — made it simultaneously frustrating and compelling. The aluminum powder medium allowed drawing by displacement but not selective erasure. Videomancer's digital version preserves the dual-knob control paradigm while adding features the mechanical original lacked: variable pen size, selective draw/erase modes, trail fade, and color.

### Grid-Based Drawing

Sketch operates on a discrete 96x54 grid, substantially finer than the game grids used by Snake (48x27) or Conway (64x36). Each cell's 20x20 pixel footprint provides reasonable resolution for freehand drawing at 1080p. The drawing surface holds 5184 cells — enough for recognizable shapes and text, though far from pixel-level precision. The grid discretization creates a distinctive aesthetic where all lines are axis-aligned and all curves are approximated with staircase patterns, reminiscent of pixel art and early computer graphics.

### Dual-Pot Cursor Control

The cursor position maps directly from two potentiometers: Knob 1 controls X (horizontal, 0-95) and Knob 2 controls Y (vertical, 0-53). The full pot range covers the full grid dimension, providing continuous, proportional cursor control. Unlike the Etch A Sketch's incremental mechanism (where each knob turn moves a fixed distance), Videomancer's absolute position mapping means the cursor jumps to wherever the knobs point. This makes drawing a fundamentally different experience — sweeping motions create continuous strokes, while abrupt knob changes produce gaps.

### Variable Pen Size

The Pen Size knob maps to a brush width of 1 to 4 cells. A 1-cell pen draws single-pixel-width lines for fine detail. A 4-cell pen fills a 4x4 block per position, useful for broad strokes and filling areas. Intermediate sizes provide a gradient of width options. The pen write operation sets (or clears, in erase mode) all cells within the pen square centered at the cursor position, meaning larger pen sizes can draw faster but with less control.

### Fade as Temporal Texture

The Fade knob introduces temporal decay to the canvas: older strokes gradually dim over successive frames. At zero fade, the canvas is permanent — strokes remain until explicitly erased. At full fade, strokes disappear within a few frames, creating a persistence-of-motion trail effect. Intermediate fade values create a controlled decay where recent strokes are bright and older strokes dim before vanishing. This transforms Sketch from a static drawing tool into a dynamic motion trace, where the cursor's path through the grid leaves a fading trail.


---

## Signal Flow

```
Synthesis Engine
|
+-- Parameter Mapping ------------------------------------------------
|   +- registers_in(0)  -> Cursor X (horizontal position 0-95)
|   +- registers_in(1)  -> Cursor Y (vertical position 0-53)
|   +- registers_in(2)  -> Pen Size (1-4 cell brush width)
|   +- registers_in(3)  -> Fade (trail decay rate)
|   +- registers_in(4)  -> Draw Hue (chroma offset)
|   +- registers_in(5)  -> Brightness (stroke Y level)
|   +- registers_in(6)  -> Toggles (pen mode, grid, cursor, color, bypass)
|   +- registers_in(7)  -> Mix
|
+-- Drawing Logic (per vsync) ----------------------------------------
|   +- 1. Cursor Map     (pot value → grid coordinate)
|   +- 2. Pen Write      (set/clear cells within pen size at cursor)
|   +- 3. Fade Scan      (optional: iterate canvas, reduce cell age)
|
+-- Rasterizer (per pixel) -------------------------------------------
|   +- 4. Cell Lookup    (h_count/20, v_count/20 → grid position)
|   +- 5. Canvas Test    (bitmap bit at (col, row))
|   +- 6. Grid Line      (cell_px < 1 or cell_py < 1, when enabled)
|   +- 7. Cursor Test    (current pixel in cursor cell range)
|   +- 8. Color Mux      (priority: cursor > stroke > grid > background)
|
+-- Output Stage ----------------------------------------------------
|   +- 9. Interpolator Mix  (3x interpolator_u wet/dry)
|
+-- Sync Pipeline ---------------------------------------------------
|   +- 6-clock shift register (hsync, vsync, avid, field)
|
+-- Bypass ----------------------------------------------------------
    +- Select processed or input signal
```

The drawing logic executes during vsync blanking. The cursor position is derived from the potentiometer values by scaling the 10-bit register range (0-1023) to the grid dimensions (0-95 for X, 0-53 for Y). The pen write operation sets or clears a square of cells centered at the cursor, with size determined by the Pen Size knob. Boundary clamping prevents the pen from writing outside the grid.

The rasterizer converts pixel coordinates to grid coordinates by integer division (h_count / 20, v_count / 20), then looks up the canvas bitmap. The cursor overlay renders on top of the canvas, appearing as a distinct marker (typically inverted or at elevated brightness) at the current cursor cell. When grid lines are enabled, the first pixel of each cell renders at reduced brightness to show cell boundaries.

---

## Parameter Reference

<img src={sketch_control_panel} alt="Videomancer front panel with Sketch loaded"/>
*Videomancer's front panel with Sketch active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cursor X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Cursor X controls the horizontal position of the drawing cursor on the 96-column canvas. The full pot range (0-1023) maps proportionally to columns 0-95. The cursor position updates every frame, so sweeping the knob traces a horizontal line across the canvas. Holding the knob steady keeps the cursor stationary. This absolute position mapping means the cursor jumps to wherever the knob points — there is no relative or incremental motion.

---

#### Knob 2 — Cursor Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Cursor Y controls the vertical position of the drawing cursor on the 54-row canvas. The full pot range maps to rows 0-53, with minimum at the top and maximum at the bottom. Combined with Cursor X, the two knobs provide full 2D positioning of the cursor. Simultaneous X and Y motion traces diagonal lines across the canvas, with the diagonal angle determined by the relative sweep rates.

---

#### Knob 3 — Pen Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Pen Size controls the brush width in cells. At minimum, the pen is 1 cell wide, drawing thin single-cell strokes. At maximum, the pen covers a 4x4 cell block, filling 16 cells per position. Larger pen sizes draw faster and fill area more efficiently but sacrifice fine control. The pen size applies equally in Draw and Erase modes.

---

#### Knob 4 — Fade
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Fade controls the temporal decay rate of canvas strokes. At zero, strokes are permanent — once drawn, they remain until explicitly erased. At higher values, strokes decay over time, with older marks dimming and eventually disappearing. At maximum fade, strokes vanish within a few frames, creating a short-lived trail effect. Intermediate fade values produce a controlled persistence where the drawing gradually dissolves, leaving only the most recent strokes visible.

---

#### Knob 5 — Draw Hue
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Draw Hue sets the chroma offset for drawn strokes when Color mode is active. Sweeping this knob rotates through the YUV color wheel, coloring canvas marks in any hue. In Mono mode, this knob has no visible effect — all strokes render as achromatic white. Color mode combined with hue control allows creating drawings in specific colors, though all strokes share the same hue at any given moment.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Bright controls the luminance (Y channel) of drawn strokes and the cursor marker. Grid lines render at a fraction of the brightness value. Higher brightness creates bold, vivid strokes against the dark background. Lower brightness produces subtle, faint marks. The brightness level also affects the cursor visibility — at very low brightness, both strokes and cursor may become difficult to distinguish from the background.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pen** | Draw | Erase |
| **8 — Grid** | Off | On |
| **9 — Cursor** | Off | On |
| **10 — Color** | Mono | Hue |
| **11 — Bypass** | Off | On |

The five toggles divide into drawing control (Pen mode), display options (Grid, Cursor, Color), and signal routing (Bypass). Pen mode directly affects how the cursor interacts with the canvas — drawing versus erasing. Grid and Cursor are display-only toggles that do not modify the canvas bitmap. Color selects between monochrome and colorized stroke rendering. Bypass routes input signal past the overlay.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix controls the wet/dry blend between the canvas drawing and the input video. At full mix, only the Sketch canvas is visible against black. Reducing mix fades in the input video behind the drawing, creating a transparent annotation overlay on live footage. At zero mix, the drawing is invisible and only the input signal passes through. The mix engages three interpolator_u instances for Y, U, and V channels independently.





---

## Guided Exercises

These exercises explore Sketch's drawing and erasing mechanics, the fade trail effect, and the use of the canvas as a live video annotation overlay.

### Exercise 1: First Lines

<img src={sketch_exercise1_result} alt="First Lines result"/>
*First Lines — simulated result across source images.*
**What You'll Create**: Draw simple shapes on the canvas using the dual-knob cursor interface.

1. Enable Cursor visibility to see where you are drawing.
2. Enable Grid to see cell boundaries.
3. Set Pen mode to Draw.
4. Set Pen Size to minimum for fine lines.
5. Turn Cursor X slowly from left to right while holding Cursor Y steady — a horizontal line appears.
6. Hold Cursor X steady and sweep Cursor Y to draw a vertical line.
7. Try sweeping both simultaneously for a diagonal.
8. Switch Pen to Erase and trace over a portion of your drawing to remove it.

**Key concepts**: Absolute cursor positioning, draw mode, erase mode, horizontal/vertical/diagonal strokes, grid resolution

---

### Exercise 2: Fade Trails

<img src={sketch_exercise2_result} alt="Fade Trails result"/>
*Fade Trails — simulated result across source images.*
**What You'll Create**: Use the Fade control to create a dynamic motion trail effect where strokes dissolve over time.

1. Set Pen mode to Draw and Pen Size to about 25% (2-cell brush).
2. Set Fade to about 50% for a moderate decay rate.
3. Sweep Cursor X and Cursor Y to trace shapes on the canvas.
4. Observe how the trail behind the cursor fades away, leaving only the most recent strokes visible.
5. Increase Fade to see faster dissolution. Decrease Fade to see longer persistence.
6. At maximum Fade, the canvas becomes a real-time motion trace with very short persistence.

**Key concepts**: Temporal decay, trail persistence, motion trace, fade rate control, dynamic drawing

---

### Exercise 3: Video Annotation Overlay

<img src={sketch_exercise3_result} alt="Video Annotation Overlay result"/>
*Video Annotation Overlay — simulated result across source images.*
**What You'll Create**: Draw annotations over live input video using the canvas as a transparent overlay.

1. Reduce Mix to about 55% to blend the canvas with input video.
2. Set Pen mode to Draw with a large Pen Size (~75%) for bold annotations.
3. Switch Color to Hue and set Draw Hue to a bright, contrasting color.
4. Set Bright to ~95% for vivid marks visible through the mix.
5. Draw circles, arrows, or text-like shapes over the video by coordinating Cursor X and Y.
6. Use Erase mode to remove mistakes without affecting the rest of the drawing.
7. Set Fade to 0 for permanent annotations, or ~30% for marks that slowly fade.

**Key concepts**: Partial mix compositing, video annotation, bold pen strokes, hue contrast, overlay persistence

---


## Tips

- **Fade for animation**: Set Fade to a moderate value and draw continuously — the fading trail creates a dynamic, animated effect from static knob movements.
- **Large pen for fills**: Use maximum Pen Size to fill large areas quickly. Switch to minimum Pen Size for outlines and details.
- **Color for emphasis**: Use Hue mode with a bright, saturated hue when overlaying drawings on video — the colored strokes visually separate from the underlying footage.
- **Bypass preserves**: Toggle Bypass to temporarily hide your drawing without losing it. Useful for reveal moments during performances.
- **Double-knob coordination**: Practice smooth, coordinated movements of both cursor knobs simultaneously for fluid diagonal and curved strokes.

---

## Glossary

| Term | Definition |
|------|------------|
| **Canvas Bitmap** | A 5184-bit array (96x54 cells) where each bit represents whether a cell is drawn (1) or empty (0). |
| **Cell** | One 20x20 pixel region within the 96x54 canvas grid, the fundamental unit of drawing. |
| **Cursor** | The current drawing position on the canvas, controlled by two potentiometers (X and Y). |
| **Draw Mode** | Pen mode where cursor movement sets canvas bits, creating visible strokes. |
| **Erase Mode** | Pen mode where cursor movement clears canvas bits, removing previously drawn marks. |
| **Fade** | Temporal decay mechanism that gradually reduces the age/brightness of drawn cells, causing strokes to dissolve over time. |
| **Pen Size** | The brush width in cells (1-4), determining how many cells are affected per cursor position. |
| **Trail** | The visible mark left by cursor movement in Draw mode; decays over time when Fade is active. |
| **Vsync** | Vertical synchronization pulse marking the start of a new video frame, used to clock drawing operations. |

---
