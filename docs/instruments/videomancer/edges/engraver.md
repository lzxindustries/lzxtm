---
draft: true
sidebar_position: 97
slug: /instruments/videomancer/engraver
title: "Engraver"
image: /img/instruments/videomancer/engraver/engraver_hero.png
description: "In traditional engraving, a craftsman cuts lines into a metal plate."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import engraver_hero from '/img/instruments/videomancer/engraver/engraver_hero.png';
import engraver_control_panel from '/img/instruments/videomancer/engraver/engraver_control_panel.png';
import engraver_exercise1_result from '/img/instruments/videomancer/engraver/engraver_exercise1_result.png';
import engraver_exercise2_result from '/img/instruments/videomancer/engraver/engraver_exercise2_result.png';
import engraver_exercise3_result from '/img/instruments/videomancer/engraver/engraver_exercise3_result.png';
import engraver_source1_kodim02 from '/img/instruments/videomancer/engraver/engraver_source1_kodim02.png';
import engraver_source2_kodim07 from '/img/instruments/videomancer/engraver/engraver_source2_kodim07.png';
import engraver_source3_kodim01_bw from '/img/instruments/videomancer/engraver/engraver_source3_kodim01_bw.png';

# Engraver

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: engraver_source1_kodim02, after: engraver_hero },
    { label: "Kodim07", before: engraver_source2_kodim07, after: engraver_hero },
    { label: "Kodim01 B&W", before: engraver_source3_kodim01_bw, after: engraver_hero },
  ]}
/>
*Engraver reducing a video signal to flat posterized regions bounded by crisp edge lines, evoking intaglio printmaking and cartoon cel-shading.*

---

## Overview

In traditional engraving, a craftsman cuts lines into a metal plate. Ink fills the grooves, and the flat surface is wiped clean — so the printed image is made entirely of lines. Engraver applies this concept to a live video signal. It reduces the tonal range of each YUV channel to a small number of discrete levels (posterization), then detects the boundaries between those levels and draws explicit edge lines over the quantized fill. The result sits somewhere between a cartoon cel, a vintage line engraving, and a screen-printed poster.

The name *Engraver* references the intaglio printmaking family — etching, engraving, mezzotint — where the image is defined by incised lines rather than continuous tone. Unlike photographic reproduction, where the goal is smoothness, engraving embraces the discrete nature of its medium. Engraver does the same thing with digital video: it makes quantization visible, then draws the boundaries it creates.

At mild settings the effect is a subtle cel-shaded look — flat-shaded regions with thin dark outlines, like a hand-drawn animation cel. At extreme settings the image collapses to a handful of color bands separated by bold graphic lines, approaching the look of a woodblock print or a technical diagram.

---

## Background

### The Intaglio Family

Intaglio printing (from the Italian *intagliare*, "to cut") is a family of printmaking techniques in which the image is incised into a surface. Engraving uses a burin to cut V-shaped grooves directly into a copper or steel plate. Etching uses acid to bite lines into a wax-coated plate. Mezzotint roughens the entire plate surface and then smooths areas to create tone. In all cases the image is defined by the relationship between incised lines and flat surfaces — precisely the relationship Engraver creates by combining quantization with edge detection.

### Cel-Shading in Animation

Traditional animation cels use a small number of flat color regions bounded by ink outlines. The animator draws the outlines first, then fills the enclosed regions with uniform paint. Engraver reverses this workflow but arrives at a similar look: it quantizes the video to create flat regions, then extracts and overlays the boundaries. The fill-plus-edge model is a direct digital analogue of the ink-and-paint process.

### Posterization and Quantization

Posterization is the reduction of a continuous-tone image to a limited number of discrete tonal levels. The name comes from poster printing, where cost constraints limit the number of ink colors. Mathematically, posterization is uniform scalar quantization: the input range is divided into equal bins, and every value in a bin maps to the same output level. Engraver implements this with a bit-shift operation — right-shifting to discard low-order bits, then left-shifting to restore scale — which divides the 10-bit range into 2, 4, 8, 16, 32, 64, 128, 256, or 512 uniform levels.

### Horizontal Edge Detection

Edge detection identifies boundaries where a signal changes abruptly. Engraver uses the simplest possible edge detector: a one-pixel horizontal delay. If the quantized value of the current pixel differs from the quantized value of the previous pixel, an edge is declared. Because the input has already been quantized to a small number of levels, the edges are guaranteed to be clean single-pixel lines at every level boundary — no thresholding or gradient magnitude computation is needed. This horizontal-only detection produces vertical edge lines (at the boundaries of horizontal level transitions), which gives the output its characteristic engraved-line quality.

### Line Art and Contour Rendering

Contour rendering in computer graphics refers to drawing lines only at the silhouettes and creases of a 3D surface. Non-photorealistic rendering (NPR) research has explored many variations — variable-width contours, hatching, stippling. Engraver's edge-only mode is a real-time video analogue of contour rendering: it extracts the level boundaries and discards everything else, leaving only the line drawing.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register ────────────────────────────────────
│   ├─ Y: optional luma invert (bitwise complement)
│   ├─ U: pass-through
│   └─ V: pass-through
│
├── Stage 2: Quantization ──────────────────────────────────────
│   ├─ Single shift amount derived from Levels parameter
│   ├─ Y: right-shift then left-shift (mask lower bits)
│   ├─ U: same shift amount as Y
│   ├─ V: same shift amount as Y
│   └─ Store previous quantized values (1-pixel delay)
│
├── Stage 3: Edge Detection ────────────────────────────────────
│   ├─ Compare current quantized Y vs previous quantized Y
│   ├─ Compare current quantized U vs previous quantized U
│   ├─ Compare current quantized V vs previous quantized V
│   └─ edge_any = Y_edge OR U_edge OR V_edge
│
├── Stage 4: Compose Output ────────────────────────────────────
│   ├─ If edge_any:
│   │   ├─ Y = Edge Gain parameter
│   │   ├─ UV = Edge Color displacement from neutral (512)
│   │   └─ (edge pixel overrides fill)
│   ├─ Elif Edge Only mode:
│   │   ├─ Y = 0 (black)
│   │   └─ UV = 512 (neutral)
│   ├─ Elif Fill Mode (flat):
│   │   ├─ Y = Y Fill parameter
│   │   └─ UV = U Fill / V Fill parameters
│   └─ Else (quantized fill):
│       ├─ Y = quantized Y
│       └─ UV = quantized UV (or 512 if Chroma Kill)
│
├── Stage 5–8: Interpolator ×3 (wet/dry mix) ──────────────────
│   ├─ Y: lerp(dry_Y, comp_Y, mix_amount)
│   ├─ U: lerp(dry_U, comp_U, mix_amount)
│   └─ V: lerp(dry_V, comp_V, mix_amount)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field — delayed 8 clocks)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select delayed original or processed signal
```

The critical design choice is that all three YUV channels share a single quantization shift amount derived from the Levels parameter. This means edge boundaries align across channels — a level change in Y always co-occurs with the same spatial boundary in U and V. The edge detector fires when *any* channel's quantized value differs from its predecessor, so edges appear at the union of all three channel boundaries.

The compose stage uses a strict priority: edge pixels always win over fill. This guarantees that edge lines are never obscured by the fill — exactly as in traditional engraving, where the incised line is always visible against the wiped plate surface.

---

## Parameter Reference

<img src={engraver_control_panel} alt="Videomancer front panel with Engraver loaded"/>
*Videomancer's front panel with Engraver active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Levels
| Property | Value |
|----------|-------|
| Range | 2 – 32 |
| Default | 10 |

Controls the quantization depth applied uniformly to all three YUV channels. The 10-bit register is divided into nine zones, each selecting a different bit-shift amount. At minimum, only two levels remain — the image becomes a stark black-and-white silhouette. At maximum, 512 levels are retained and quantization is nearly invisible. The sweet spot for a visible engraving effect is typically between 4 and 16 levels, where posterization bands are clearly visible and edge lines mark every transition.

---

#### Knob 2 — U Levels
| Property | Value |
|----------|-------|
| Range | 2 – 32 |
| Default | 10 |

Controls the quantization depth for the U (blue-difference) chrominance channel. The firmware maps the Y Levels, U Levels, and V Levels pots to different VHDL registers, but the VHDL internally uses only a single Levels register (reg 0) for all three channels. When Link Levels is engaged, the three knobs track together. When disengaged, only Pot 1 controls the actual quantization depth — Pots 2 and 3 have no effect on the quantization shift in the current VHDL implementation.

---

#### Knob 3 — V Levels
| Property | Value |
|----------|-------|
| Range | 2 – 32 |
| Default | 10 |

Controls the quantization depth for the V (red-difference) chrominance channel. As with U Levels, this parameter feeds VHDL register 2 (V Fill), which sets the flat-fill V brightness rather than an independent quantization level. The per-channel level labels in the TOML provide future expansion points for independent channel quantization.

---

#### Knob 4 — Edge Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the luminance brightness of edge pixels. At zero, edge lines are black — dark grooves against lighter fill, like an etched copper plate. At maximum, edge lines are bright white — light lines against darker fill, resembling chalk on a blackboard or a photographic negative of an engraving. The edge brightness applies uniformly to all detected edge pixels regardless of which channel triggered the detection.

---

#### Knob 5 — Edge U
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the chrominance displacement of edge pixels along the U axis. At the 50% midpoint (register 512), edges are chromatically neutral. Turning the knob below center pushes edge color toward yellow; above center pushes toward blue. Combined with Edge V, this creates colored edge lines — a tinted-ink effect reminiscent of sepia or cyanotype printing.

---

#### Knob 6 — Edge V
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the chrominance displacement of edge pixels along the V axis. At the 50% midpoint, edges are neutral. Below center shifts toward cyan-green; above center shifts toward red-magenta. Together with Edge U, the two chroma controls let you dial in any edge line hue — gold, copper, blue-black, or any intermediate tint.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Edge Mode** | Fill+Edge | Edge Only |
| **8 — Edge Invert** | Off | On |
| **9 — Desaturate** | Off | On |
| **10 — Link Levels** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles partition into three functional groups. Toggles 7 and 8 control the fill-versus-edge composition: Edge Mode selects between showing fill with edge overlay or edges only, while Edge Invert swaps the luminance polarity of the input before quantization. Toggle 9 (Desaturate) kills chroma on the fill, and Toggle 10 (Link Levels) is a firmware-level feature linking the three level knobs. Toggle 11 is the standard bypass switch.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the fully processed (wet) output. At 0% the original signal passes through unchanged. At 100% the full engraving effect is applied. Intermediate values blend the two, which can produce a subtle embossed or relief look where the original image shows through the quantized regions with faint edge lines overlaid.

---

## Guided Exercises

These three exercises progress from basic posterization to full engraved line art, building familiarity with the interaction between quantization depth, edge detection, and fill composition.

### Exercise 1: Cartoon Cel-Shading

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: engraver_source1_kodim02, after: engraver_exercise1_result },
    { label: "Kodim07", before: engraver_source2_kodim07, after: engraver_exercise1_result },
    { label: "Kodim01 B&W", before: engraver_source3_kodim01_bw, after: engraver_exercise1_result },
  ]}
/>
*Cartoon Cel-Shading — simulated result across source images.*
**Source**: A camera feed or recorded footage with a human face or recognizable subject against a medium-contrast background.

**Objective**: Create a classic cel-shaded animation look with flat-colored regions bounded by dark outlines.

1. **Set quantization**: Turn Y Levels (Pot 1) to roughly 25% — about 8 visible tonal bands. The image should look like a poster with distinct flat regions.
2. **Dark edges**: Set Edge Y (Pot 4) to about 10% for thin dark outlines at every level boundary.
3. **Neutral edge color**: Center Edge U (Pot 5) and Edge V (Pot 6) at 50% for black edge lines.
4. **Full color fill**: Ensure Desaturate (Toggle 9) is Off and Edge Mode (Toggle 7) is Fill+Edge.
5. **Observe**: The output should resemble a hand-drawn animation cel — flat-shaded skin tones, hair, and background with ink outlines at every tonal transition.
6. **Adjust levels**: Sweep Y Levels to see how more levels create subtle shading while fewer levels create bold graphic regions.

**Key concepts**: Quantization creates flat regions, edge detection finds the boundaries between those regions, edge brightness controls line weight

---

### Exercise 2: Copper Plate Engraving

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: engraver_source1_kodim02, after: engraver_exercise2_result },
    { label: "Kodim07", before: engraver_source2_kodim07, after: engraver_exercise2_result },
    { label: "Kodim01 B&W", before: engraver_source3_kodim01_bw, after: engraver_exercise2_result },
  ]}
/>
*Copper Plate Engraving — simulated result across source images.*
**Source**: A still photograph or slow-moving footage with fine detail — architecture, foliage, or textured fabrics.

**Objective**: Simulate the look of an intaglio copper plate print using desaturated fill with warm-tinted edge lines.

1. **Moderate quantization**: Set Y Levels to about 40% for 16–32 visible tonal bands — enough to preserve some modeling in the fill.
2. **Bright edges**: Increase Edge Y (Pot 4) to about 70% for prominent white-on-dark edge lines.
3. **Warm edge tint**: Set Edge U (Pot 5) to about 35% and Edge V (Pot 6) to about 65% for a warm sepia-copper edge hue.
4. **Desaturate fill**: Enable Desaturate (Toggle 9) to make the fill monochrome. The colored edges stand out against the gray fill.
5. **Invert test**: Toggle Edge Invert (Toggle 8) to see how the edge pattern changes when the luminance polarity flips.
6. **Mix down**: Set Mix (Fader 12) to about 70% to blend some of the original image through the engraving.

**Key concepts**: Desaturation isolates edge color from fill color, warm edge tints simulate copper-plate ink, mix blending creates relief effects

---

### Exercise 3: Pure Line Drawing

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: engraver_source1_kodim02, after: engraver_exercise3_result },
    { label: "Kodim07", before: engraver_source2_kodim07, after: engraver_exercise3_result },
    { label: "Kodim01 B&W", before: engraver_source3_kodim01_bw, after: engraver_exercise3_result },
  ]}
/>
*Pure Line Drawing — simulated result across source images.*
**Source**: High-contrast footage — text on a screen, geometric objects, or a high-contrast face lit from the side.

**Objective**: Extract only edge lines with no fill, producing a contour line drawing.

1. **Coarse quantization**: Set Y Levels to about 15% for very few levels — bold, widely-spaced level transitions produce thick line clusters.
2. **Edge Only mode**: Switch Edge Mode (Toggle 7) to Edge Only. The fill disappears, replaced by black.
3. **Bright white edges**: Set Edge Y (Pot 4) to 100% for maximum brightness edge lines.
4. **Add edge color**: Sweep Edge U and Edge V away from center to tint the lines — try blue (Edge U high, Edge V low) for a blueprint look.
5. **Invert**: Toggle Edge Invert (Toggle 8). The edges now appear at different spatial locations because the inverted luminance quantizes differently.
6. **Sweep levels**: Slowly increase Y Levels. Watch the line drawing gain more detail as more quantization boundaries appear.

**Key concepts**: Edge Only mode discards fill to isolate contour lines, fewer quantization levels produce fewer but bolder edges, inversion changes which boundaries are detected

---


## Tips

- **Fewer levels = bolder lines**: Reducing the quantization depth creates wider tonal bands with edges at each boundary. Two or four levels produce dramatic bold outlines; 32 or more levels produce fine, hair-like lines.
- **Edge brightness is your line weight**: Edge Y (Pot 4) controls perceived line weight. Low values give thin, subtle lines that blend into dark fills. High values create bold, high-contrast outlines.
- **Colored edges emulate ink tints**: Setting Edge U and Edge V away from center tints the edge lines — sepia for warm, cyan for cool — while the fill can remain monochrome (with Desaturate on) for an authentic printed-engraving look.
- **Horizontal-only edges give vertical lines**: The edge detector compares each pixel with its left neighbor. This means it detects *horizontal transitions*, which produce *vertical edge lines*. Diagonal and horizontal structures in the source create the densest line patterns.
- **Edge Only for contour extraction**: Edge Only mode (Toggle 7) discards the fill entirely, leaving a pure line drawing on black. This is useful as a key source or overlay layer in a multi-program video chain.
- **Invert before quantizing**: Edge Invert flips luminance *before* the quantizer sees it, so the set of pixels assigned to each level changes. This repositions every edge in the image — a fast way to explore alternative line compositions from the same source.
- **Mix for embossed relief**: Setting Mix to 50–70% blends the original image underneath the engraved result, creating a raised-relief or embossed appearance where the original texture shows through the flat quantized regions.
- **Feedback creates recursive contours**: Routing the output back to the input re-quantizes the already-quantized signal. With enough feedback gain, edges accumulate into dense interference patterns.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU standard defining the color matrix used to convert between RGB and YUV in standard-definition video. Videomancer uses BT.601 coefficients throughout. |
| **Cel** | A transparent sheet (cellulose acetate) used in traditional animation, painted with flat colors and overlaid on backgrounds. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Contour** | A line drawn at the boundary of a region; in NPR rendering, contour lines mark silhouettes and creases. |
| **Edge Detection** | A signal processing technique that identifies abrupt transitions in value between adjacent samples. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Intaglio** | A family of printmaking techniques where the image is incised into a surface (engraving, etching, mezzotint). |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Posterization** | Reducing the number of distinct tonal levels in an image, creating flat areas of uniform color or brightness. |
| **Quantization** | Mapping a continuous range of values to a smaller set of discrete levels, producing visible steps in gradients. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
