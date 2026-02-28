---
draft: true
sidebar_position: 185
slug: /instruments/videomancer/origami
title: "Origami"
image: /img/instruments/videomancer/origami/origami_hero.png
description: "Origami takes an input video signal and tiles it into a grid of folded panels, simulating the appearance of a sheet of paper folded and unfolded to reve..."
---

import origami_animation from '/img/instruments/videomancer/origami/origami_animation.gif';
import origami_control_panel from '/img/instruments/videomancer/origami/origami_control_panel.png';
import origami_exercise1_result from '/img/instruments/videomancer/origami/origami_exercise1_result.gif';
import origami_exercise2_result from '/img/instruments/videomancer/origami/origami_exercise2_result.gif';
import origami_exercise3_result from '/img/instruments/videomancer/origami/origami_exercise3_result.gif';
import origami_hero from '/img/instruments/videomancer/origami/origami_hero.png';

# Origami

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={origami_hero} alt="Origami hero image"/>
*Origami dividing a video frame into mirrored geometric fold panels with crease highlights, gap borders, and facet-dependent shadow gradients.*
<img src={origami_animation} alt="Origami animated output"/>
*Origami output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Origami takes an input video signal and tiles it into a grid of folded panels, simulating the appearance of a sheet of paper folded and unfolded to reveal repeated, mirrored copies of the original image. The fold count is independently adjustable for horizontal and vertical axes, producing grids from a single full-frame panel up to fine lattices of tiny repeated tiles. Optional mirror reflection on each axis creates kaleidoscopic symmetry — adjacent panels flip to produce seamless, reflected patterns rather than hard-edged repetition.

Despite being categorised as a Grid program (which normally implies synthesis), Origami **processes input video** — the fold panels contain transformed copies of the source signal, not procedurally generated imagery. Every pixel in the output is sampled from the input via modular address wrapping, with optional mirror reflection at fold boundaries. Gap insertion, shadow gradients, crease highlights, and diagonal fold modes add visual depth and paper-like texture to the tiled result.

The Scale parameter (Knob 6, `registers_in(5)`) is declared in the VHDL register mapping but is **not connected** to any processing logic. Adjusting this control has no effect on the output.

---

## Background

### Modular Address Wrapping

The core technique behind Origami is modular arithmetic applied to pixel coordinates. For each output pixel, the horizontal position is divided by the fold period (frame width ÷ fold count). The remainder determines which position within the source panel to sample. This produces exact repetitions of the first fold cell across the entire frame — the same principle used in texture tiling in 3D graphics, applied here to live video.

### Mirror Reflection at Fold Boundaries

When a mirror toggle is active, odd-numbered fold cells reverse their sampling direction. The remainder is subtracted from the period width, so the second panel is a mirror image of the first, the third is normal again, and so on. This creates bilateral symmetry at every fold boundary — the visual equivalent of unfolding a piece of paper that was folded along vertical or horizontal creases. Combined on both axes, mirroring produces four-way symmetry reminiscent of kaleidoscope patterns.

### Gap and Border Effects

Real paper folds have physical thickness. Origami simulates this by inserting narrow strips of dark or neutral color between adjacent fold panels. The Gap Width control sets the width of these dead zones. When the Border toggle is active, the gap edges are drawn as thin bright lines, simulating the visible edge of folded paper catching light. These border lines provide visual structure that makes the fold grid legible even when the source material is complex.

### Shadow and Crease Shading

To simulate directional lighting on a three-dimensional folded surface, Origami applies a luma gradient near each fold edge (shadow) and a brightness spike at the fold center (crease). The shadow control sets the depth of the darkening at fold boundaries; the crease control sets the intensity of the ridge highlight. Together, they create a tangible paper-fold illusion where even flat video content appears to occupy physical space.

### Diagonal Folding

The Diagonal toggle rotates the fold grid by 45 degrees, computing fold cells along the (h+v) and (h−v) diagonal axes rather than the horizontal and vertical axes. This transforms the rectangular grid into a diamond lattice, producing more complex geometric patterns. Diagonal folding interacts with the mirror toggles to create additional symmetry axes.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Address Generation ─────────────────────────────────────────
│   │
│   ├─ 1. Fold Period Compute   (frame ÷ fold count per axis)
│   ├─ 2. Modular Remainder     (position mod period → cell position)
│   ├─ 3. Mirror Reflection     (odd cells: period − remainder)
│   ├─ 4. Diagonal Rotation     (optional 45° axis swap)
│   └─ 5. Source Sampling       (read input at computed address)
│
├── Shading ────────────────────────────────────────────────────
│   │
│   ├─ 6. Gap Insertion         (zero-out pixels in gap zone)
│   ├─ 7. Border Lines          (optional bright edge at gap)
│   ├─ 8. Shadow Gradient       (darken near fold edges)
│   └─ 9. Crease Highlight      (brighten at fold center)
│
├── Dry/Wet Mix ────────────────────────────────────────────────
│   └─ Interpolator × 3 (Y, U, V crossfade)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or folded signal
```

The critical path divides into two domains: **address computation** (stages 1–5) determines which source pixel is sampled for each output pixel, while **shading** (stages 6–9) modifies the sampled value based on position within the fold cell. These two domains are independent — the address wrapping and mirror logic operate on coordinate counters, while shading operates on the sampled YUV values. The gap and border effects override sampled data entirely for pixels that fall within the dead zone; shadow and crease modify luma without changing chroma.

---

## Parameter Reference

<img src={origami_control_panel} alt="Videomancer front panel with Origami loaded"/>
*Videomancer's front panel with Origami active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Fold Den
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Horizontal fold count. At 0%, a single full-width panel (no horizontal folding). As the control increases, the frame is divided into progressively more horizontal panels — 2, 4, 8, up to 16, each a narrower slice of the source. The fold period is the frame width divided by this count, so higher values produce smaller, more finely repeated tiles.

---

#### Knob 2 — Crease Vs
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Vertical fold count. Functions identically to H Folds but along the vertical axis. Combined with H Folds, the two controls define a 2D grid of fold cells. Equal values produce square cells; unequal values produce rectangular cells — wide horizontal strips or tall vertical columns.

---

#### Knob 3 — Flatness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Gap width between fold panels. At 0%, panels tile seamlessly with no visible separation. As the control increases, a dark gap appears between adjacent panels. The gap is rendered as a neutral strip (luma near zero) that interrupts the fold pattern. Large gap values create a window-pane effect where the source tiles appear as discrete frames separated by dark borders.

---

#### Knob 4 — Fold Ang
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shadow depth at fold edges. Controls the intensity of the luma darkening gradient applied near the boundary of each fold cell. At 0%, no shadow — panels have uniform brightness. At high values, the edges of each panel darken significantly, creating a strong 3D paper-fold illusion. The shadow gradient is linear, fading from full darkening at the edge to no effect at the center of the cell.

---

#### Knob 5 — Paper Tx
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Crease highlight brightness at fold centers. Controls the intensity of a narrow luma spike at the center of each fold cell, simulating the ridge of a paper fold catching light. At 0%, no crease line. At high values, a bright line bisects each panel. The crease is narrower than the shadow gradient, producing a sharp ridge rather than a broad highlight.

---

#### Knob 6 — Shadow
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scale — **this parameter is declared in the register mapping but is not connected to any processing stage**. Adjusting this knob has no effect on the output. It is documented here for completeness and may be connected in a future firmware revision.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Crane | Star |
| **8 — Paper** | White | Washi |
| **9 — Folds** | Valley | Mountain |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the fold geometry and rendering style. Mirror H and Mirror V control whether adjacent panels repeat or reflect. Diagonal rotates the fold grid to a diamond orientation. Border adds visible edge lines at gap boundaries. Bypass routes the input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input signal and the folded output. At 0%, the output is the unmodified input. At 100%, the output is the fully processed fold + shading result. Intermediate values blend the fold pattern over the source, useful for subtle texture overlay effects.

---

## Guided Exercises

These exercises progress from simple tiling to complex mirrored diamond lattices with full shading. Each builds on the previous, gradually engaging more of the fold engine.

### Exercise 1: Basic Fold Grid

<img src={origami_exercise1_result} alt="Basic Fold Grid result"/>
*Basic Fold Grid — simulated result across source images.*
**Objective**: Learn how H Folds and V Folds divide the frame into a grid of repeated tiles.

1. **Single fold**: Set H Folds to ~25%. The frame splits into two side-by-side copies of the left half.
2. **More folds**: Increase H Folds to ~50%. Four copies appear. Continue to ~75% for eight copies.
3. **Vertical folds**: Now increase V Folds to ~50%. The grid becomes 2D — tiles repeat both horizontally and vertically.
4. **Enable mirror**: Turn on Mirror H (Switch 7). Adjacent columns now reflect — the face in every other column is flipped.
5. **Both mirrors**: Turn on Mirror V (Switch 8). Four-way symmetry appears at every intersection.
6. **Observe symmetry**: Notice how the mirror boundaries create seamless transitions — no hard edges between adjacent panels.

**Key concepts**: Fold count defines grid density, modular address wrapping repeats the source tile, mirror toggles create bilateral symmetry at fold boundaries

---

### Exercise 2: Paper Fold Illusion

<img src={origami_exercise2_result} alt="Paper Fold Illusion result"/>
*Paper Fold Illusion — simulated result across source images.*
**Objective**: Explore gap, shadow, and crease shading to create a 3D paper-fold appearance.

1. **Set grid**: H Folds ~50%, V Folds ~50%, Mirror H on, Mirror V on.
2. **Add gaps**: Increase Gap Width to ~30%. Dark strips appear between panels.
3. **Add borders**: Turn on Border (Switch 10). Thin bright lines appear at gap edges.
4. **Shadow**: Increase Shadow to ~50%. The edges of each panel darken, creating depth.
5. **Crease**: Increase Crease to ~40%. A bright ridge line appears at the centre of each panel.
6. **Combine**: Adjust Shadow and Crease together. The panels now look like folded paper — dark edges, bright ridges, gaps between cells.

**Key concepts**: Gap insertion separates panels, border lines mark fold edges, shadow gradient creates depth, crease highlight simulates ridge, all effects applied after address sampling

---

### Exercise 3: Diamond Lattice

<img src={origami_exercise3_result} alt="Diamond Lattice result"/>
*Diamond Lattice — simulated result across source images.*
**Objective**: Combine diagonal folding with mirroring for complex diamond kaleidoscope patterns.

1. **Diagonal mode**: Set H Folds ~60%, V Folds ~60%, enable Diagonal (Switch 9).
2. **Enable mirrors**: Turn on both Mirror H and Mirror V. Diamond-shaped reflections appear.
3. **Add shading**: Increase Shadow to ~40%, Crease to ~30%.
4. **Gap and border**: Set Gap Width ~20%, enable Border.
5. **Source exploration**: Try different source material. Geometric inputs produce structured diamonds; organic inputs produce mandala-like forms.
6. **Fine tuning**: Adjust H and V Folds independently to create elongated diamond shapes.

**Key concepts**: Diagonal mode rotates fold axes by 45°, diamond patterns combine both diagonals, mirror + diagonal produces 8-way symmetry, source content determines aesthetic character

---


## Tips

- **Start simple**: Begin with one axis of folding and no shading. Add complexity incrementally — mirror, then gap, then shadow and crease.
- **Mirror is the signature effect**: Without mirroring, Origami is a simple tiler. With mirroring, fold boundaries become symmetry axes that create kaleidoscope-like patterns.
- **Gap width defines visual rhythm**: Small gaps create subtle panel separation; large gaps create a window-pane grid where the tiles appear as framed pictures.
- **Scale does nothing**: Do not expect Knob 6 to affect the output. The scale feature is unimplemented.
- **Diagonal + mirror = mandala**: Diagonal folding combined with both mirrors produces 8-way symmetric diamond patterns that resemble mandala or Islamic geometric art.
- **Shadow and crease sell the illusion**: Even a small amount of shadow and crease transforms flat tiling into a convincing paper-fold appearance.
- **Feedback loops**: Route the output back to the input for recursive folding. Each iteration doubles the fold count, quickly creating fractal-like subdivisions.
- **Mix for overlay tiling**: Partial mix values superimpose the fold grid over the source as a transparent texture layer.

---

## Glossary

| Term | Definition |
|------|------------|
| **Address Wrapping** | Computing source pixel coordinates using modular arithmetic so that the fold pattern repeats seamlessly across the frame. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Fold Cell** | A single rectangular (or diamond) region of the fold grid, containing one copy of the source tile. |
| **Fold Period** | The width (or height) of a single fold cell in pixels, equal to the frame dimension divided by the fold count. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Kaleidoscope** | An optical instrument using mirrors to create symmetric patterns; Origami's mirror mode produces similar bilateral symmetry. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived luminance. |
| **Mirror Reflection** | Reversing the sampling direction in alternate fold cells to create bilateral symmetry at fold boundaries. |
| **Modular Arithmetic** | Division with remainder, used to wrap pixel coordinates into repeating fold cells. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
