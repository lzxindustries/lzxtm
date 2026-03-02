---
draft: true
sidebar_position: 65
slug: /instruments/videomancer/crosshatch
title: "Crosshatch"
image: /img/instruments/videomancer/crosshatch/crosshatch_hero.png
description: "Every illustrator and printmaker who has worked without continuous tone knows the challenge: reproduce the full range of light and shadow using only marks and blank surface."
---

import crosshatch_hero from '/img/instruments/videomancer/crosshatch/crosshatch_hero.png';
import crosshatch_before_after from '/img/instruments/videomancer/crosshatch/crosshatch_before_after.png';
import crosshatch_control_panel from '/img/instruments/videomancer/crosshatch/crosshatch_control_panel.png';
import crosshatch_exercise1_result from '/img/instruments/videomancer/crosshatch/crosshatch_exercise1_result.png';
import crosshatch_exercise2_result from '/img/instruments/videomancer/crosshatch/crosshatch_exercise2_result.png';
import crosshatch_exercise3_result from '/img/instruments/videomancer/crosshatch/crosshatch_exercise3_result.png';

# Crosshatch

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={crosshatch_hero} alt="Crosshatch hero image"/>
*Crosshatch rendering diagonal ink strokes at variable density across a luminance-graded portrait, emulating copperplate engraving.*
<img src={crosshatch_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Crosshatch applied.*

---

## Overview

Every illustrator and printmaker who has worked without continuous tone knows the challenge: reproduce the full range of light and shadow using only marks and blank surface. The traditional answer is hatching — parallel strokes laid at regular intervals whose spacing encodes brightness. Where highlights fall, the surface stays bare; where shadows deepen, strokes pile up in multiple crossing layers until the ink fills most of the area. Crosshatch converts a live video signal into this graphic language in real time.

The program generates up to four independent layers of lines — 45° diagonal, 135° diagonal, horizontal, and vertical — and composites them over a user-configurable flat "paper" wash. Each line layer is produced entirely by bitmask logic applied to pixel position counters: a pixel lies on a hatch line whenever the bitwise AND of its counter value with a spacing mask equals zero. No division, no modulus, no multiplication — just combinational AND gates operating at full clock rate. The spacing mask is a power-of-two function of the Stroke W knob, and the thickness mask zeroes progressively more low-order bits as Line Width increases, widening every stroke in lockstep.

After compositing, the hatch pattern is blended with the original video through three parallel interpolators controlled by the Mix fader, producing anything from a subtle textured overlay to a full ink-on-paper replacement of the source image.

---

## Background

### A Brief History of Cross-Hatching

Cross-hatching is among the oldest techniques in Western graphic art. Albrecht Dürer perfected it in the late fifteenth century for woodcuts and copper engravings, building tone through carefully angled parallel cuts. Rembrandt used it extensively in etching, varying stroke density and angle across a single plate to achieve extraordinary tonal range. The technique transfers naturally to pen-and-ink illustration, where an artist controls shade by choosing how many stroke layers to overlap: a single set of parallel lines for light tone, two crossing sets for mid-tone, three or four for deep shadow.

### Line-Based Shading in Print

In commercial print, line-based shading remained dominant until photographic halftone screens replaced it in the late nineteenth century. Engraved banknotes, steel engravings, and hand-ruled maps all rely on the principle that evenly spaced lines of uniform width create a perceived gray whose darkness depends solely on the ratio of ink area to paper area. Crosshatch applies this principle at video rate: the spacing parameter controls the line pitch, the width parameter controls the stroke thickness, and the combination determines the effective ink coverage.

### Bitmask Geometry

The VHDL implementation avoids modular arithmetic entirely. A line appears wherever the result of counter AND mask is zero. For a mask of 7 (binary 0000_0111), every eighth pixel sits on a line. For a mask of 31 (binary 0001_1111), every thirty-second pixel qualifies. Diagonal lines emerge from the same test applied to (h_count + v_count) for 45° or (h_count − v_count) for 135°. The thickness mask then broadens each hit by ignoring additional low-order bits, effectively allowing neighboring pixels to also pass the gate. This all-combinational approach uses approximately 700 LUTs and zero BRAM.

### Wash and Ink

Traditional printmaking separates ink from paper. The artist chooses an ink color and a paper stock — the strokes are ink, the gaps are paper. Crosshatch models this with independent wash controls (Y, U, V for the background) and a line brightness parameter for the stroke color. The Ink Tint and Paper Tint hue rotations extend this metaphor into chromatic territory: warm sepia ink on cold blue-gray paper, or vice versa.

### The Mix Interpolator

Three parallel instances of `interpolator_u` perform the wet/dry crossfade. Each interpolator computes `a + (b − a) × t` in four pipelined clocks, where `a` is the delayed source, `b` is the composited hatch image, and `t` is the Mix fader value. At t = 0 the output is pure source; at t = 1023 the output is pure hatch. Intermediate values produce a superimposition of strokes over the original video.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Timing Generator ─────────────────────────────────────────
│   └─ edge_detector → video_timing_generator → h_count, v_count
│
├── Stage 1: Counter Sums ────────────────────────────────────
│   ├─ sum_45  = h_count + v_count   (diagonal 45°)
│   └─ diff_135 = h_count − v_count  (diagonal 135°)
│
├── Stage 2: Hatch Detection (bitmask AND) ───────────────────
│   ├─ on_diag45  = ((sum_45 AND hatch_mask) AND thick_mask) == 0
│   ├─ on_diag135 = ((diff_135 AND hatch_mask) AND thick_mask) == 0
│   ├─ on_horiz   = ((v_count AND hatch_mask) AND thick_mask) == 0
│   ├─ on_vert    = ((h_count AND hatch_mask) AND thick_mask) == 0
│   └─ on_any_hatch = diag45 OR diag135 OR horiz OR vert
│
├── Stage 3: Colour Composite ───────────────────────────────
│   ├─ if on_any_hatch → (line_bright, 512, 512)
│   └─ else            → (wash_y, wash_u, wash_v)
│
├── Stages 4–7: Interpolator Mix (4 clocks) ─────────────────
│   ├─ mix_y = lerp(source_y, comp_y, mix_amount)
│   ├─ mix_u = lerp(source_u, comp_u, mix_amount)
│   └─ mix_v = lerp(source_v, comp_v, mix_amount)
│
├── Sync Delay Pipeline (8 clocks) ──────────────────────────
│   └─ hsync_n, vsync_n, field_n, Y, U, V delayed to match
│
└── Bypass Mux ──────────────────────────────────────────────
    └─ bypass=0 → mixed output | bypass=1 → delayed source
```

The critical design insight is that all line detection happens in a single combinational step per clock: the bitmask AND simultaneously tests spacing and thickness without any sequential counters or comparators beyond the position counters themselves. The hatch mask converts the Stroke W knob into a power-of-two spacing (8, 16, 32, 64, 128, or 256 pixels), and the thickness mask widens each line by clearing 0, 1, 2, or 3 low-order bits. Four enable flags (one per line direction from toggles 7–10) gate each detection result independently. The composition stage then selects either the ink color (line brightness on Y, neutral on U/V) or the wash color for every pixel, and the downstream interpolator blends this against the time-aligned source.

---

## Parameter Reference

<img src={crosshatch_control_panel} alt="Videomancer front panel with Crosshatch loaded"/>
*Videomancer's front panel with Crosshatch active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Stroke W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial period of all hatch lines. At low values the mask is narrow (period of 8 pixels) — lines are densely packed, producing dark fields of closely spaced strokes. As the knob increases, the mask widens through 16, 32, 64, 128, and 256 pixel periods, spreading the lines further apart and letting more of the background wash show through. This is the primary "density" control in the traditional hatching sense: tight spacing for shadow, wide spacing for highlight.

---

#### Knob 2 — Density
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the overall density of the line pattern by adjusting the brightness of the hatch strokes relative to the wash background. At 0% the stroke luma is black, creating maximum contrast against a bright wash. At 100% the stroke luma matches full white, which against a dark wash creates bright lines on a dark field — an inversion of the traditional ink-on-paper relationship. Mid values produce soft gray strokes useful for pencil-like effects.

---

#### Knob 3 — Angle
| Property | Value |
|----------|-------|
| Range | 0° – 90° |
| Default | 45° |
| Suffix | ° |

Rotates the hatch angle smoothly from 0° to 90°. At 0° the active diagonal is flat (effectively horizontal); at 45° it crosses the frame at a true 45° diagonal; at 90° it reaches vertical orientation. The angle applies to the primary detected stroke direction and interacts with the Cross toggle — when Cross mode is active, the perpendicular set of strokes rotates symmetrically. This gives continuous control over the stroke geometry from horizontal bands to diagonal lattices to vertical columns.

---

#### Knob 4 — Levels
| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 5 |

Selects the number of luminance quantization levels used to map input brightness to hatching density. At the minimum setting (2 levels), the image divides into pure highlight and pure shadow — a stark two-tone rendering. At the maximum (8 levels), a smoother staircase of hatch densities reproduces a wider tonal range. Higher level counts approach continuous tone; lower counts create bold graphic contrasts reminiscent of woodblock printing.

---

#### Knob 5 — Ink Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Applies a hue rotation to the ink (stroke) color. At 0° the strokes are neutral (achromatic). Rotating through 360° cycles the ink tint through the full color wheel — warm amber at 30°, red at 0°/360°, teal at 180°. This allows emulation of sepia ink, blue ballpoint, red sanguine crayon, or any other chromatic ink color while the paper tint remains independent.

---

#### Knob 6 — Paper Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Applies a hue rotation to the paper (wash background) color, independently of the ink tint. Combining a warm ink tint with a cool paper tint recreates the look of toned printmaking paper. Setting both tints to the same hue but different saturations creates subtle monochromatic studies. At 0° the wash is neutral gray, controlled solely by the Wash Y/U/V parameters.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Pen | Pencil |
| **8 — Cross** | Single | Cross |
| **9 — Color Ink** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 control the stroke geometry (line direction selection and crossing). Toggle 9 enables chromatic ink derived from the source video rather than the flat ink tint. Toggle 10 inverts the luminance-to-density mapping. Toggle 11 is the standard bypass. Together they determine the visual style: single-direction pen lines, crossed engraving patterns, color-keyed strokes, or inverted negative etchings.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original video and the crosshatch composite. At 0% the output is pure source video with no hatching visible. At 100% the output is entirely the ink-and-paper composite. Intermediate positions superimpose the hatch pattern over the source with adjustable opacity, allowing subtle textured overlays where the original image remains recognizable beneath the strokes.

---

## Guided Exercises

These exercises progress from simple parallel strokes to full multi-layer crosshatched renderings with chromatic ink, exploring how spacing, width, angle, and style interact. Each exercise uses a different source type to demonstrate a distinct hatching technique.

### Exercise 1: Pen Sketch

<img src={crosshatch_exercise1_result} alt="Pen Sketch result"/>
*Pen Sketch — simulated result across source images.*
**Source**: A head-and-shoulders portrait or bust shot with directional lighting creating clear highlight and shadow regions.

**Objective**: Create a clean pen-and-ink sketch with a single family of diagonal strokes varying in density from highlight to shadow.

1. **Set stroke direction**: Select Style → Pen (Toggle 7). Confirm Cross → Single (Toggle 8).
2. **Adjust spacing**: Turn Stroke W to approximately 40%. Lines should be clearly separated.
3. **Set density**: Turn Density to approximately 30% for dark stroke lines.
4. **Angle the strokes**: Set Angle to approximately 45° for classic diagonal hatching.
5. **Full mix**: Set Mix to 100% to see the pure hatched rendering.
6. **Adjust levels**: Sweep the Levels knob to see how the tonal staircase affects the distribution of stroke densities across the face.

**Key concepts**: Single-direction hatching controls tone through spacing alone, the Levels parameter quantizes the luminance-to-density mapping, Pen style uses diagonal strokes only

---

### Exercise 2: Copperplate Engraving

<img src={crosshatch_exercise2_result} alt="Copperplate Engraving result"/>
*Copperplate Engraving — simulated result across source images.*
**Source**: Architectural footage or a still life with clear geometric forms and strong contrast.

**Objective**: Build a multi-layer crosshatched rendering that emulates copperplate engraving with warm sepia ink on ivory paper.

1. **Set style**: Select Style → Engrave (Toggle 7). Set Cross → Cross (Toggle 8).
2. **Tighten spacing**: Turn Stroke W to approximately 25% for closer line pitch.
3. **Darken strokes**: Set Density to approximately 15% for deep ink lines.
4. **Set angle**: Adjust Angle to approximately 30° for a slightly tilted lattice.
5. **Tint the ink**: Rotate Ink Tint to approximately 30° for a warm sepia tone.
6. **Tint the paper**: Rotate Paper Tint to approximately 50° for an ivory/cream background.
7. **Increase levels**: Set Levels to 6 for a smoother tonal gradation across the architecture.

**Key concepts**: Cross mode doubles line density by adding a perpendicular stroke family, Engrave style activates all four line directions for maximum tonal coverage, Ink Tint and Paper Tint separate the color of marks from the color of ground

---

### Exercise 3: Color-Keyed Etch

<img src={crosshatch_exercise3_result} alt="Color-Keyed Etch result"/>
*Color-Keyed Etch — simulated result across source images.*
**Source**: Colorful footage — flowers, painted walls, neon signage, or a color bar test pattern.

**Objective**: Create a color etching where the stroke color is derived from the source video's chrominance, producing hand-tinted crosshatch artwork.

1. **Set style**: Select Style → Etch (Toggle 7). Set Cross → Cross (Toggle 8).
2. **Medium spacing**: Turn Stroke W to approximately 35%.
3. **Set density**: Turn Density to approximately 20%.
4. **Enable Color Ink**: Toggle Color Ink → On (Toggle 9). The strokes now carry the source's hue.
5. **Set angle**: Adjust Angle to approximately 60° for a steep lattice.
6. **Partial mix**: Set Mix to approximately 70% to let some source detail show through the hatching.
7. **Experiment with inversion**: Toggle Invert → On (Toggle 10) to see color strokes in the highlight regions instead of the shadow regions.

**Key concepts**: Color Ink mode replaces the flat ink tint with per-pixel chrominance from the source video, partial Mix values create a superimposition effect where source detail is visible beneath the strokes, Invert reverses the luminance-to-density mapping

---


## Tips

- **Start with Pen + Single**: The simplest configuration — one family of diagonal strokes. Add complexity (Cross, Engrave, Etch) only after you understand the base spacing and density controls.
- **Spacing before width**: Adjust Stroke W first to set the overall line pitch, then use Density to darken or lighten the strokes. These two controls together determine the perceived gray level.
- **Sepia ink recipe**: Ink Tint ≈ 30°, Paper Tint ≈ 50°, Density ≈ 20%. This combination closely resembles aged copperplate prints.
- **Color Ink for watercolor effect**: Toggle Color Ink On and set Mix to 60–80%. The source's color bleeds through the hatching, creating a hand-tinted illustration look.
- **Feedback loops**: Route the crosshatched output back to the input for recursive hatching — strokes on strokes, building up layered graphic textures.
- **Invert for white ink**: Toggle Invert On with a dark wash to simulate white ink or chalk on dark paper.
- **Levels as a tonal compressor**: Low Levels values (2–3) flatten the image to stark light-and-dark zones. High values (6–8) preserve subtle gradation. Use low values for bold graphic impact.
- **Mix for texture overlays**: At 20–40% Mix, the hatching acts as a subtle texture layer over otherwise clean video — useful for adding an analog print feel to digital sources.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bitmask** | A binary pattern used with AND logic to test specific bit positions in a counter; in Crosshatch, determines whether a pixel lies on a hatch line. |
| **BRAM** | Block RAM; dedicated FPGA memory. Crosshatch uses zero BRAM because all line detection is combinational. |
| **Chroma** | The color information in a video signal, encoded as U (Cb) and V (Cr) in YUV color space. |
| **Copperplate** | An engraving technique where lines are incised into a copper plate; Crosshatch's Engrave style emulates this multi-directional line pattern. |
| **Cross-Hatching** | A shading technique using two or more sets of intersecting parallel lines to build tone. Denser overlap produces darker values. |
| **Hatching** | A shading technique using parallel lines at regular spacing; a single family of strokes without crossing. |
| **Interpolator** | A pipelined arithmetic unit that computes `a + (b − a) × t`; used here for the wet/dry mix between source and hatch composite. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **LUT** | Look-Up Table; the fundamental logic element in an FPGA, used for combinational functions. |
| **Pipeline** | A series of clocked processing stages where each stage's output feeds the next stage's input. |
| **Power-of-Two** | A spacing value that is a power of 2 (8, 16, 32, …), enabling detection via bitmask AND rather than division. |
| **Wash** | The background color that appears between hatch strokes; analogous to paper color in printmaking. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
