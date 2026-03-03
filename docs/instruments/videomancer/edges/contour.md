---
draft: true
sidebar_position: 62
slug: /instruments/videomancer/contour
title: "Contour"
image: /img/instruments/videomancer/contour/contour_hero_s1.png
description: "A topographic map turns continuous terrain into a set of discrete elevation lines."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import contour_source1_field from '/img/instruments/videomancer/contour/contour_source1_field.png';
import contour_source2_ballerina from '/img/instruments/videomancer/contour/contour_source2_ballerina.png';
import contour_source3_turtle from '/img/instruments/videomancer/contour/contour_source3_turtle.png';
import contour_source4_pattern from '/img/instruments/videomancer/contour/contour_source4_pattern.png';
import contour_source5_boy from '/img/instruments/videomancer/contour/contour_source5_boy.png';
import contour_source6_berries from '/img/instruments/videomancer/contour/contour_source6_berries.png';
import contour_hero_s1 from '/img/instruments/videomancer/contour/contour_hero_s1.png';
import contour_hero_s2 from '/img/instruments/videomancer/contour/contour_hero_s2.png';
import contour_hero_s3 from '/img/instruments/videomancer/contour/contour_hero_s3.png';
import contour_hero_s4 from '/img/instruments/videomancer/contour/contour_hero_s4.png';
import contour_hero_s5 from '/img/instruments/videomancer/contour/contour_hero_s5.png';
import contour_hero_s6 from '/img/instruments/videomancer/contour/contour_hero_s6.png';
import contour_ex1_s1 from '/img/instruments/videomancer/contour/contour_ex1_s1.png';
import contour_ex1_s2 from '/img/instruments/videomancer/contour/contour_ex1_s2.png';
import contour_ex1_s3 from '/img/instruments/videomancer/contour/contour_ex1_s3.png';
import contour_ex1_s4 from '/img/instruments/videomancer/contour/contour_ex1_s4.png';
import contour_ex1_s5 from '/img/instruments/videomancer/contour/contour_ex1_s5.png';
import contour_ex1_s6 from '/img/instruments/videomancer/contour/contour_ex1_s6.png';
import contour_ex2_s1 from '/img/instruments/videomancer/contour/contour_ex2_s1.png';
import contour_ex2_s2 from '/img/instruments/videomancer/contour/contour_ex2_s2.png';
import contour_ex2_s3 from '/img/instruments/videomancer/contour/contour_ex2_s3.png';
import contour_ex2_s4 from '/img/instruments/videomancer/contour/contour_ex2_s4.png';
import contour_ex2_s5 from '/img/instruments/videomancer/contour/contour_ex2_s5.png';
import contour_ex2_s6 from '/img/instruments/videomancer/contour/contour_ex2_s6.png';
import contour_ex3_s1 from '/img/instruments/videomancer/contour/contour_ex3_s1.png';
import contour_ex3_s2 from '/img/instruments/videomancer/contour/contour_ex3_s2.png';
import contour_ex3_s3 from '/img/instruments/videomancer/contour/contour_ex3_s3.png';
import contour_ex3_s4 from '/img/instruments/videomancer/contour/contour_ex3_s4.png';
import contour_ex3_s5 from '/img/instruments/videomancer/contour/contour_ex3_s5.png';
import contour_ex3_s6 from '/img/instruments/videomancer/contour/contour_ex3_s6.png';

# Contour

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: contour_source1_field, after: contour_hero_s1 },
    { label: "Ballerina", before: contour_source2_ballerina, after: contour_hero_s2 },
    { label: "Turtle", before: contour_source3_turtle, after: contour_hero_s3 },
    { label: "Pattern", before: contour_source4_pattern, after: contour_hero_s4 },
    { label: "Boy", before: contour_source5_boy, after: contour_hero_s5 },
    { label: "Berries", before: contour_source6_berries, after: contour_hero_s6 },
  ]}
/>
*Contour rendering iso-luminance contour lines across a landscape, transforming video into a topographic elevation map.*

---

## Overview

A topographic map turns continuous terrain into a set of discrete elevation lines. Each line traces a path along the ground where every point is at the same altitude. Contour does the same thing to a video signal — but instead of altitude, it traces paths of equal *luminance*. Wherever brightness changes from one quantized level to the next, a contour line appears.

The program begins by quantizing the 10-bit luma channel into a reduced set of levels — effectively rounding every pixel's brightness to the nearest step on a staircase. It then compares each pixel's quantized value to its horizontal neighbor (one clock earlier) and vertical neighbor (from a line buffer storing the previous scan line). Wherever the quantized values differ, a contour line is drawn. The result is a network of lines that trace the iso-luminance contours of the source image, exactly as elevation lines trace iso-altitude contours on a map.

Every Nth contour can be promoted to an *index contour* — drawn brighter and more prominent, like the bold lines on a real topographic map that mark major elevation intervals. Between contour lines, the fill area can show the original source video or a flat-brightness surface. A color mode shifts the chroma of contour lines to create tinted cartographic effects. All of this runs through an 8-clock pipeline using a single BRAM tile for the vertical line buffer.

---

## Background

### Topographic Maps and Iso-Lines

The topographic contour map was invented in the 18th century as a way to represent three-dimensional terrain on a flat sheet of paper. The key insight is that if you slice a mountain with a series of horizontal planes at regular altitude intervals, the intersection of each plane with the terrain surface produces a closed curve — a *contour line* or *isoline*. Plotting all these curves from above produces a 2D map where the density and spacing of lines encodes the steepness of the terrain. Closely-spaced lines mean a steep slope; widely-spaced lines mean a gentle grade.

Contour applies this principle to video luminance. The "altitude" is brightness. The "horizontal planes" are the quantization levels created by the Interval control. The "contour lines" appear wherever the quantized brightness changes between adjacent pixels. A flat gray area produces no contours; a sharp brightness edge produces a dense cluster of lines; a gentle gradient produces evenly-spaced parallel contours.

### Index Contours and Cartographic Hierarchy

Real topographic maps use two weights of contour line. Regular (or *intermediate*) contour lines are drawn thin and light. Every 5th or 10th line is an *index contour* — drawn thicker and bolder, often with its altitude value printed alongside. This visual hierarchy lets the map reader quickly estimate elevation differences by counting bold lines rather than thin ones.

Contour implements this by applying a bitmask to the quantized level number. When the masked level equals zero, the contour is promoted to an index contour and drawn at full brightness. Regular contours are drawn at half brightness. The Major Frq control sets the bitmask threshold — every 2nd, 4th, 8th, or 16th contour becomes a major index line. This directly mirrors the cartographic convention of major and minor contour intervals.

### From Paper Maps to Video Synthesis

Cartographic contour rendering has been used as a creative tool since the earliest days of computer graphics. Iso-luminance contours turn a photographic image into something that looks like a hand-drawn map — abstract, schematic, and revealing of structure that the eye normally glosses over. In video synthesis, contour lines respond to motion: as objects move through the frame, the contour lines shift and flow around them, creating a dynamic topographic landscape that evolves in real time. Feeding the contoured output back into the input creates recursive elevation maps — contour lines tracing the contours of previous contour lines, building up intricate nested patterns.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Quantize Luma ─────────────────────
│   │
│   ├─ Capture Y, U, V from data_in
│   ├─ Quantize Y: shift right by quant_shift, shift left
│   │   (discard low bits → N discrete levels)
│   ├─ Store quantized Y → horizontal register (1-clock delay)
│   └─ Write quantized Y → video_line_buffer (for next line)
│
├── Stage 2: Contour Detection ──────────────────────────────────
│   │
│   ├─ Horizontal contour: quant_y ≠ quant_y_prev_h
│   ├─ Vertical contour: quant_y ≠ line_buffer_read
│   └─ Combined: contour = horizontal OR vertical
│
├── Stage 3: Classify + Color ───────────────────────────────────
│   │
│   ├─ Index test: (level AND index_mask) == 0 → index contour
│   ├─ Contour luma: index → full brightness, regular → half
│   ├─ Contour chroma: mono (U=V=512) or colored (U + offset)
│   └─ Fill selection: source video or flat-brightness grey
│
├── Stage 4: Composite Output ──────────────────────────────────
│   │
│   └─ if contour → contour Y/U/V, else → fill Y/U/V
│
├── Mix: Interpolator ×3 (4 clocks) ───────────────────────────
│   │
│   └─ Crossfade: dry (delayed original) ↔ wet (composite)
│
├── Sync Delay Pipeline (8 clocks) ─────────────────────────────
│   └─ hsync_n, vsync_n, field_n, Y, U, V delay registers
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ bypass=0 → mix output, bypass=1 → delayed original
```

The critical interaction is between quantization and neighbor comparison. The Interval control determines how many discrete luma levels exist — fewer levels means wider spacing between contour lines. A coarse quantization (6-bit shift, 16 levels) produces bold, widely-spaced contours like a large-scale map with 100-metre intervals. Fine quantization (1-bit shift, 512 levels) produces dense, tightly-packed contours like a detailed survey map with 1-metre intervals. The line buffer enables vertical contour detection: without it, only horizontal edges along each scan line would be visible. With it, contour lines form closed curves that trace the full perimeter of each iso-luminance region.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Interval
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the quantization interval — the spacing between adjacent contour levels. At low values (counter-clockwise), the luma channel is quantized coarsely into as few as 16 levels, producing bold, widely-spaced contour lines like a large-scale topographic map. As the control increases, the number of levels grows — 32, 64, 128, 256, up to 512 — and the contour lines pack closer together, revealing finer tonal detail in the source. At maximum, the contour density approaches the source resolution and nearly every pixel boundary becomes a contour, creating a dense texture of lines.

---

#### Knob 2 — Line Thk
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the brightness of the contour lines themselves. At maximum, contour lines are drawn at full white; at minimum, they are nearly invisible. Index contours always appear at the full brightness set by this control, while regular contours are drawn at half that brightness. This creates the visual hierarchy of bold and fine lines that makes the topographic structure readable. Setting this control low while keeping Fill Xpar high creates a subtle ghost-line effect where contours are barely visible against the fill.

---

#### Knob 3 — Major Frq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the frequency of index (major) contour lines. The control sets a bitmask threshold that determines how many regular contour levels appear between each bold index contour. At low values, every second contour is promoted to an index line — dense bold markings. At higher values, the spacing widens to every 4th, 8th, or 16th contour. This mirrors the cartographic convention of labeling every 5th or 10th elevation line as a bold index contour for fast visual reference. The effect is most visible when the Interval is set to produce many contour levels.

---

#### Knob 4 — Fill Xpar
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the fill brightness used when the Style toggle selects flat fill mode. In flat fill mode, the area between contour lines is rendered as a uniform grey whose brightness is set by this control. At low values the fill is dark, making bright contour lines stand out against a near-black background. At high values the fill approaches white and the contour lines appear as dark interruptions in a bright field. When the Style toggle selects source fill, this control has no visible effect — the original video fills the spaces between contour lines.

---

#### Knob 5 — Smooth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the chrominance of contour lines when the Fill toggle enables colored contour mode. At center position (512), no color shift is applied and contour lines take their chroma from the source pixel. Below center, the U component is reduced, tinting contour lines toward yellow-red. Above center, U is increased, tinting toward blue-cyan. This allows cartographic color coding — for example, brown contour lines on a terrain map or blue bathymetric contour lines on an ocean chart. When colored mode is off, contour lines are drawn monochrome (neutral chroma) regardless of this control.

---

#### Knob 6 — Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for future use. Adjusting this control has no effect on the current processing chain. The register is mapped in the ABI but not consumed by any stage in the pipeline.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Topo | Bathy |
| **8 — Color** | Brown | Green |
| **9 — Fill** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent aspects of the contour rendering. Style selects whether the fill between contour lines shows the original source video or a flat-brightness grey. Color enables or disables the index contour hierarchy. Fill enables or disables chroma tinting of contour lines. Animate is reserved. Bypass routes the original signal around the entire processing chain for A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the contour-processed signal and the original video. At 0% the output is the unprocessed source. At 100% the output is the full contour rendering. Intermediate positions create a transparent overlay effect where contour lines are blended over the source image at partial opacity. Three independent interpolator instances handle Y, U, and V channels in parallel, each adding 4 clocks of latency to the pipeline.

---

## Guided Exercises

These exercises introduce contour rendering from basic topographic line work through complex cartographic compositions. Each exercise uses a different source to highlight different aspects of the contouring algorithm.

### Exercise 1: Basic Topographic Map

<BeforeAfterSlider
  sources={[
    { label: "Field", before: contour_source1_field, after: contour_ex1_s1 },
    { label: "Ballerina", before: contour_source2_ballerina, after: contour_ex1_s2 },
    { label: "Turtle", before: contour_source3_turtle, after: contour_ex1_s3 },
    { label: "Pattern", before: contour_source4_pattern, after: contour_ex1_s4 },
    { label: "Boy", before: contour_source5_boy, after: contour_ex1_s5 },
    { label: "Berries", before: contour_source6_berries, after: contour_ex1_s6 },
  ]}
/>
*Basic Topographic Map — simulated result across source images.*
**Source**: A close-up of a face or portrait with smooth tonal gradients — skin tones produce well-spaced, readable contour lines.

**Objective**: Create a clean topographic contour rendering with bold index lines and fine intermediate contours.

1. **Set the contour interval**: Turn Interval to about 40% to create ~64 quantization levels — a moderate contour density.
2. **Enable flat fill**: Set Style to flat fill mode. Set Fill Xpar to about 10% for a dark background.
3. **Brighten contour lines**: Turn Line Thk to about 80% for clearly visible contour lines.
4. **Add index hierarchy**: Enable Color toggle to turn on index contours. Set Major Frq to about 50% so every 4th contour is bold.
5. **Monochrome lines**: Keep Fill (color contours) off for classic black-and-white cartographic rendering.
6. **Full wet mix**: Set Mix to 100%.
7. **Compare**: Toggle Bypass to see the original portrait, then switch back to see the topographic rendering.

**Key concepts**: Quantization creates discrete luma levels, contour detection finds level boundaries in both axes, index contours add visual hierarchy

---

### Exercise 2: Color Terrain Overlay

<BeforeAfterSlider
  sources={[
    { label: "Field", before: contour_source1_field, after: contour_ex2_s1 },
    { label: "Ballerina", before: contour_source2_ballerina, after: contour_ex2_s2 },
    { label: "Turtle", before: contour_source3_turtle, after: contour_ex2_s3 },
    { label: "Pattern", before: contour_source4_pattern, after: contour_ex2_s4 },
    { label: "Boy", before: contour_source5_boy, after: contour_ex2_s5 },
    { label: "Berries", before: contour_source6_berries, after: contour_ex2_s6 },
  ]}
/>
*Color Terrain Overlay — simulated result across source images.*
**Source**: A landscape or nature scene with broad tonal variation — hills, sky gradients, foliage.

**Objective**: Create a colored contour overlay on top of the original source video, like a terrain map printed on a satellite photograph.

1. **Source fill**: Set Style to source fill mode so the original video shows between contour lines.
2. **Moderate density**: Set Interval to about 55% for a comfortable contour spacing.
3. **Enable colored contours**: Turn on Fill (color contours). Turn Smooth to about 30% to tint contour lines warm brown — classic terrain map color.
4. **Index hierarchy**: Enable Color toggle. Set Major Frq to about 70% so every 8th contour is bold.
5. **Semi-transparent mix**: Set Mix to about 65% so contour lines are overlaid semi-transparently on the source.
6. **Adjust line brightness**: Set Line Thk to about 70%. Index lines should be clearly bold; regular lines subtler.
7. **Sweep interval**: Slowly sweep Interval from low to high. Watch the contour density change from bold elevation bands to fine survey lines.

**Key concepts**: Source fill preserves photographic content, color shift tints contour lines for cartographic effect, mix creates transparent overlay

---

### Exercise 3: Dense Contour Texture

<BeforeAfterSlider
  sources={[
    { label: "Field", before: contour_source1_field, after: contour_ex3_s1 },
    { label: "Ballerina", before: contour_source2_ballerina, after: contour_ex3_s2 },
    { label: "Turtle", before: contour_source3_turtle, after: contour_ex3_s3 },
    { label: "Pattern", before: contour_source4_pattern, after: contour_ex3_s4 },
    { label: "Boy", before: contour_source5_boy, after: contour_ex3_s5 },
    { label: "Berries", before: contour_source6_berries, after: contour_ex3_s6 },
  ]}
/>
*Dense Contour Texture — simulated result across source images.*
**Source**: Abstract video patterns, feedback loops, or color bars — high-contrast material with many brightness transitions.

**Objective**: Push the contouring into extreme density to create texture effects rather than readable maps.

1. **Maximum density**: Turn Interval fully clockwise for 512 quantization levels. The contour lines become so dense they form a texture.
2. **Flat dark fill**: Set Style to flat fill. Set Fill Xpar to about 5% for near-black background.
3. **Full brightness**: Set Line Thk to 100%.
4. **Disable index hierarchy**: Turn off Color toggle so all contour lines are equal weight.
5. **Enable color**: Turn on Fill (color contours). Sweep Smooth across its range to cycle the contour hue through warm and cool tones.
6. **Half mix**: Set Mix to about 50%. The dense contour texture merges with the source, creating a moire-like interference pattern.
7. **Sweep interval**: Slowly turn Interval counter-clockwise to reduce density. Watch the texture open up into distinct contour lines.

**Key concepts**: Extreme contour density creates texture rather than line work, color shift produces spectral effects on dense contour fields, mix creates interference patterns

---


## Tips

- **Start coarse, refine fine**: Begin with Interval low (16 levels) to see the broad contour structure, then increase to add detail. Dense contours on a busy source can be hard to read.
- **Index hierarchy is essential**: Enable the Color toggle and set Major Frq to create bold/fine line weight distinction. Without index hierarchy, dense contour fields become an undifferentiated mesh.
- **Source fill for overlay**: Use source fill mode (Style) when you want contour lines drawn on top of the original video, like a topographic overlay on a satellite photo.
- **Flat fill for isolation**: Use flat fill mode with a dark Fill Xpar to isolate the contour structure against a clean background — ideal for pure cartographic rendering.
- **Color coding**: Enable Fill toggle and use Smooth to tint contour lines brown (terrain), blue-green (bathymetric), or any intermediate hue for thematic cartographic effects.
- **Feedback creates nested contours**: Routing the contoured output back into the input creates contour lines *of* contour lines — recursive topographic structures that build up into intricate patterns.
- **Mix for transparency**: Partial Mix values create a translucent contour overlay where the line network is visible but the source image shows through, combining cartographic and photographic information.
- **Motion reveals flow**: Moving subjects cause contour lines to shift and flow in real time. The contour network breathes and ripples as brightness changes propagate through the frame.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; a dedicated memory resource on the FPGA used here for the video line buffer that stores quantized luma from the previous scan line. |
| **Contour Line** | A curve connecting points of equal value; in this program, points of equal quantized luminance. |
| **Index Contour** | A bold contour line marking a major interval, drawn at full brightness versus the half brightness of regular contour lines. |
| **Interpolator** | A hardware module that computes a weighted average between two values; used here for the wet/dry mix stage. |
| **Iso-Luminance** | A surface or line of constant brightness, analogous to an iso-altitude line on a topographic map. |
| **Line Buffer** | A BRAM-based delay that stores one full scan line of data, enabling vertical neighbor comparison between consecutive lines. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages where each stage operates on one clock cycle; this program uses an 8-clock pipeline. |
| **Quantization** | Mapping a continuous range of values to a smaller set of discrete levels by discarding low-order bits. |
| **Topographic Map** | A map that uses contour lines to represent the shape and elevation of terrain; the visual metaphor for this program. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |


---
