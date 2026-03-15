---
draft: true
sidebar_position: 117
slug: /instruments/videomancer/floorplan
title: "Floorplan"
image: /img/instruments/videomancer/floorplan/floorplan_hero.png
description: "Every video image is full of boundaries — places where brightness changes abruptly across adjacent pixels."
---

import floorplan_hero from '/img/instruments/videomancer/floorplan/floorplan_hero.png';
import floorplan_animation from '/img/instruments/videomancer/floorplan/floorplan_animation.gif';
import floorplan_control_panel from '/img/instruments/videomancer/floorplan/floorplan_control_panel.png';
import floorplan_exercise1_result from '/img/instruments/videomancer/floorplan/floorplan_exercise1_result.gif';
import floorplan_exercise2_result from '/img/instruments/videomancer/floorplan/floorplan_exercise2_result.gif';
import floorplan_exercise3_result from '/img/instruments/videomancer/floorplan/floorplan_exercise3_result.gif';

# Floorplan

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={floorplan_hero} alt="Floorplan hero image"/>
*Floorplan extracting luminance edges from a video source to render architectural wall-line drawings with blueprint grid overlay.*
<img src={floorplan_animation} alt="Floorplan animated output"/>
*Floorplan output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Every video image is full of boundaries — places where brightness changes abruptly across adjacent pixels. Floorplan treats those brightness edges as structural walls and renders them as dark (or bright) lines on a clean background, transforming live video into something that looks like an architectural drawing pulled from a drafting table.

The program works by computing two gradient measurements for every pixel on every frame: a horizontal difference (current pixel minus the previous pixel) and a vertical difference (current pixel minus the pixel on the previous scan line, stored in a dedicated BRAM line buffer). These gradients are summed, optionally amplified, and compared against two configurable thresholds — a primary threshold for strong walls and a secondary threshold that adds body to the line work. Non-edge pixels are replaced with a uniform background, and an optional grid overlay adds ruled dimension lines at fixed 32-pixel intervals.

Two rendering styles are available: a classic black-on-white drafting style (dark ink lines on bright paper) and a white-on-blue style that mimics cyanotype blueprints. A wet/dry crossfade lets you blend any amount of the floorplan rendering with the original source signal.

---

## Quick Start

1. **Start with Wall Thk and Bg Bright at center**: The dual-threshold system works best when both thresholds are active. Extreme settings on either knob can make the other ineffective.
2. **Door Gap is the detail control**: When you want fine surface textures to appear as architectural line work, increase Door Gap rather than lowering the thresholds — amplification preserves the threshold hierarchy while boosting weak gradients.
3. **Dim Sp has three discrete levels**: Rather than a smooth gradient, the contrast control jumps between heavy, medium, and light line weights. Sweep it slowly to find each level.

---

## Background

### Architectural Drafting and Blueprint History

Before computer-aided design, every building began as a hand-drafted ink drawing on translucent paper. Architects used ruling pens, T-squares, and parallel rulers to produce precise wall outlines on gridded sheets. When copies were needed, the original was placed over light-sensitive paper and exposed to strong light — the cyanotype (blueprint) process turned unexposed areas dark blue while areas blocked by ink lines remained white. The result: white wall lines on a deep blue background. Floorplan's two rendering styles — black-on-white and white-on-blue — directly echo these two historical states of the architectural drawing.

### Edge Detection as Line Extraction

Edge detection is one of the oldest techniques in image processing. The basic idea is that a sharp boundary in an image corresponds to a large change in pixel brightness over a short distance — a steep gradient. Floorplan uses the simplest possible gradient operator: a first-order difference. The horizontal gradient is the absolute difference between adjacent pixels on the same scan line; the vertical gradient is the absolute difference between corresponding pixels on consecutive lines. Summing these two gradients gives an omnidirectional edge strength that responds to boundaries at any angle.

### Dual-Threshold Wall Detection

A single threshold divides every pixel into "edge" or "not edge," producing crisp but thin one-pixel-wide outlines. Floorplan adds a second, lower threshold that catches pixels just below the primary detection level — the weaker gradient echoes that exist next to every strong edge. Together, the two thresholds produce variable-width wall lines: strong edges draw a core line via the primary test, and the secondary test fills in neighboring pixels to create heavier, more architectural strokes. The two thresholds are independently adjustable, so you can render anything from single-pixel hairlines to broad structural walls.

### Grid Overlays in Technical Illustration

Architectural and engineering drawings are almost always ruled with a background grid — evenly spaced lines that provide dimensional reference without obscuring the primary geometry. Floorplan implements a fixed 32-pixel grid using a bitmask test on the horizontal and vertical position counters. When enabled, every 32nd column and every 32nd row is drawn at a slightly different brightness than the paper background, creating a subtle ruled pattern behind the wall outlines. The grid is drawn only where no wall line exists, so structural edges always take priority.

### Contrast Scaling and Line Weight

In hand drafting, line weight communicates hierarchy: thick lines mark primary walls, thinner lines mark interior partitions, and the thinnest lines mark dimension leaders and grid rules. Floorplan approximates this through a contrast control that scales the darkness of detected edges. The VHDL implements three discrete line weight levels using bit-shift divisions: heavy (÷4 scaling, producing the darkest lines), medium (÷2), and light (no scaling). The transitions between these levels occur at fixed control positions, giving the user three distinct drafting pen weights rather than a smooth gradient.


---

## Signal Flow

Y Channel → UV Channels → Interpolator → Sync Delay → Bypass Mux

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ Stage 1: Input Register (1 clk)
│   │   ├─ Current Y registered
│   │   ├─ Previous-pixel Y (1-clock delay)
│   │   └─ Line buffer write/read (previous-line Y via BRAM)
│   │
│   ├─ Stage 2: Raw Differencing (1 clk)
│   │   ├─ H diff = current Y − previous pixel Y
│   │   └─ V diff = current Y − previous line Y
│   │
│   ├─ Stage 3: Edge Detect + Threshold (1 clk)
│   │   ├─ edge_strength = |H diff| + |V diff|
│   │   ├─ Sensitivity amplification (×1 / ×2 / ×4 / ×8)
│   │   ├─ Primary wall test   (strength > threshold)
│   │   ├─ Thick wall test     (strength > lower threshold)
│   │   └─ Grid overlay test   (32-pixel spacing bitmask)
│   │
│   └─ Stage 4: Composite (1 clk)
│       ├─ Wall pixels:  contrast-scaled edge darkness
│       ├─ Grid pixels:  slightly dimmed background
│       └─ Background:   bright paper fill
│
├── UV Channels ────────────────────────────────────────────────
│   └─ Set by style: neutral gray (black-on-white)
│       or blue tint U=650, V=350 (white-on-blue)
│
├── Interpolator (4 clk) ──────────────────────────────────────
│   └─ 3× interpolator_u: wet/dry crossfade (Y, U, V)
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock delay alignment for hsync, vsync, field
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed or original signal
```

The pipeline is a straightforward four-stage detect-and-composite chain followed by four interpolator clocks. Two key points: (1) **Edge detection is purely luminance-based** — the U and V channels of the input are not analyzed; only the Y channel drives the gradient computation. The output chroma is entirely synthetic, set by the rendering style. (2) **Dual thresholds are OR-combined** — a pixel is drawn as a wall line if it exceeds *either* the primary or the secondary threshold, which means the secondary threshold always adds to the primary detection, never subtracts.

---

## Parameter Reference

<img src={floorplan_control_panel} alt="Videomancer front panel with Floorplan loaded"/>
*Videomancer's front panel with Floorplan active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Wall Thk
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At low settings, the detector responds to subtle brightness gradients throughout the image, drawing wall lines around nearly every tonal boundary — the result looks like an over-inked pen saturating the paper. As you turn Wall Thk higher, only the strongest gradient transitions qualify as walls, revealing just the dominant structural boundaries. This is the primary control for how many wall lines appear in the output. Internally, sets the primary edge detection threshold via a scaled comparison level.

---

#### Knob 2 — Bg Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls a secondary detection threshold that fills in additional edge pixels around the primary wall detections. When set low, the program aggressively catches weak gradient echoes near every detected edge, producing heavy line work with thick architectural strokes. As you increase this control, the secondary detector tightens its selectivity, and fewer marginal pixels qualify — wall outlines become thinner and more precise. The interaction with Wall Thk determines the overall wall weight: high Wall Thk with low Bg Bright produces the most dramatic thick-on-thin line contrast.

---

#### Knob 3 — Sensitiv
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At maximum, the paper is bright white (in the default style) or a luminous blue (in the blue style). Lower settings create a dimmer background, reducing the overall contrast between wall lines and paper — useful for blending the floorplan rendering into a darker color palette or for creating an aged-paper look. Because wall darkness is computed relative to this value, changing the background brightness also subtly affects how dark the wall lines appear. Internally, sets the brightness of the background paper that fills all non-edge, non-grid areas.

---

#### Knob 4 — Dim Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At low settings, wall lines receive maximum darkening, producing the heaviest pen-stroke appearance — bold structural walls suitable for primary floor plans. At mid-range settings, the darkening reduces by half, creating medium-weight lines. At high settings, wall darkness follows the raw edge strength without additional scaling, producing the lightest line weight with the most tonal variation. These three levels correspond to the traditional drafting hierarchy of thick, medium, and thin pen strokes. Internally, controls the line weight of the wall rendering through three discrete scaling levels.

---

#### Knob 5 — Door Gap
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls gradient pre-amplification before the threshold tests. The amplification operates in four discrete steps: no gain, ×2, ×4, and ×8. At low settings, the detector relies on naturally occurring strong gradients — only bold boundaries in the source produce wall lines. As you increase this control, progressively weaker gradients are boosted into the detection range. At maximum amplification (×8), even subtle shading variations register as wall lines, rendering fine surface textures and soft transitions as architectural detail.

---

#### Knob 6 — Scale
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for future functionality. In the current firmware implementation, this control has no effect on the processed output. Adjusting it produces no visible change.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Modern | Sketch |
| **8 — Lines** | Black | Source |
| **9 — Dims** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control rendering style, visual mode, grid overlay, and signal routing. Style and Lines select the detection approach and color scheme. Dims enables the 32-pixel architectural grid. Animate is reserved. Bypass routes the original signal directly to the output for A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed floorplan rendering and the original source signal. At 100%, the output is purely the architectural rendering. As you lower the fader, the original video progressively blends through, creating a semi-transparent overlay effect where wall outlines appear superimposed on the live image. At 0%, the output is the unmodified source.





---

## Guided Exercises

These exercises progress from basic wall extraction to full blueprint styling. Each builds on the previous, gradually engaging the threshold, style, and grid controls.

### Exercise 1: Wall Extraction

<img src={floorplan_exercise1_result} alt="Wall Extraction result"/>
*Wall Extraction — simulated result across source images.*
**What You'll Create**: Learn how the dual-threshold edge detection extracts wall lines from a video source.

1. **Default detection**: With all controls at default, observe the initial wall rendering. Edges from the source appear as dark lines on a bright background.
2. **Primary threshold**: Slowly increase Wall Thk from center. Watch as weaker edges disappear and only the strongest boundaries remain — major walls and high-contrast edges.
3. **Secondary fill**: Now lower Bg Bright toward zero. The secondary threshold catches weaker gradients near every detected edge, thickening the wall lines. Return to center.
4. **Sensitivity boost**: Increase Door Gap past center. Subtle gradients are amplified into the detection range — surface textures and soft shading begin to appear as fine hairline details.
5. **Line weight**: Sweep Dim Sp from low to high. At low settings, wall lines are bold and dark. At high settings, they carry tonal variation reflecting the underlying edge strength.
6. **Compare**: Toggle Bypass on and off to see the raw source versus the extracted wall rendering.

**Key concepts**: Dual-threshold edge detection produces variable wall thickness, sensitivity amplification reveals finer gradients, contrast scaling controls line darkness

---

### Exercise 2: Blueprint Rendering

<img src={floorplan_exercise2_result} alt="Blueprint Rendering result"/>
*Blueprint Rendering — simulated result across source images.*
**What You'll Create**: Explore the blue rendering style and grid overlay to create a classic blueprint look.

1. **Switch to blue**: Set Lines to Blue. The rendering inverts: bright white wall lines on a dark blue background.
2. **Enable grid**: Set Dims to On. Faint ruled lines appear at 32-pixel intervals, creating an engineering grid behind the wall outlines.
3. **Paper brightness**: Sweep Sensitiv. At high settings, the blue background is brighter and more saturated. At low settings, it becomes a deep midnight blue.
4. **Heavy walls**: Lower Dim Sp to the first third. Wall lines become bold white strokes — primary structural walls in a construction drawing.
5. **Light detail**: Raise Dim Sp to the upper third. Wall lines thin out and show tonal variation, like pencil preliminary lines on a blueprint.
6. **Mix overlay**: Lower Mix to ~50%. The original source video appears as a ghost image behind the blueprint rendering — a useful effect for video overlay compositions.

**Key concepts**: Blue style inverts the brightness relationship (bright lines on dark background), grid overlay provides dimensional reference, mix blends processed and source signals

---

### Exercise 3: Detail Enhancement

<img src={floorplan_exercise3_result} alt="Detail Enhancement result"/>
*Detail Enhancement — simulated result across source images.*
**What You'll Create**: Push the sensitivity and threshold controls to render fine surface detail as architectural line work.

1. **Maximum sensitivity**: Set Door Gap to ~90%. The ×8 amplification boosts even minor brightness variations into the detection range.
2. **Low threshold**: Lower Wall Thk to ~20%. Combined with high sensitivity, nearly every gradient in the image produces a wall line. The result is a dense, ink-saturated rendering.
3. **Secondary thinning**: Raise Bg Bright to ~80%. The thick wall threshold tightens, removing the weakest secondary detections and cleaning up the line work slightly.
4. **Grid reference**: Enable Dims. The 32-pixel grid provides spatial reference among the dense line work.
5. **Contrast sculpt**: Sweep Dim Sp slowly. At low settings, the dense line field is uniformly dark. At high settings, individual line weights emerge, and the rendering begins to look like a detailed technical illustration.
6. **Blue inversion**: Switch Lines to Blue. The dense line field inverts to white-on-blue, creating a saturated blueprint texture from the source detail.

**Key concepts**: High sensitivity reveals surface micro-gradients as line work, low threshold produces dense ink-saturated renderings, contrast scaling differentiates line weights within dense detail

---


## Tips

- **Blue mode inverts the brightness logic**: In Black mode, strong edges are dark lines on bright paper. In Blue mode, strong edges are bright white lines on dark blue paper. All other controls behave identically, but the visual hierarchy reverses.
- **Grid spacing is fixed at 32 pixels**: The grid cannot be rescaled. Use Sensitiv (background brightness) to control how visibly the grid stands out against the paper.
- **Mix for overlay compositing**: At 50%, the floorplan rendering acts as a semi-transparent overlay on the source video — useful for creating annotated live video effects where wall outlines trace the original scene.
- **Feedback routing**: Sending the output back through the input creates recursive line detection — wall lines from the first pass become the source edges for the second pass, progressively simplifying the image toward its dominant structural forms.

---

## Glossary

| Term | Definition |
|------|------------|
| **Blueprint** | A cyanotype reproduction of a technical drawing, producing white lines on a blue background; the color scheme replicated by Floorplan's Blue rendering style. |
| **Edge Detection** | The process of identifying sharp brightness transitions in an image by computing pixel-to-pixel gradient differences. |
| **Gradient** | The rate of change of pixel brightness across a spatial distance; stronger gradients correspond to sharper image edges. |
| **Line Buffer** | A single-BRAM memory that stores one horizontal line of video data, enabling vertical comparisons between consecutive scan lines. |
| **Luma** | The brightness component (Y) of a YUV video signal; the only channel analyzed for edge detection in Floorplan. |
| **Threshold** | A comparison level that divides edge strengths into "wall" and "not wall" categories; Floorplan uses two thresholds for variable wall thickness. |

---
