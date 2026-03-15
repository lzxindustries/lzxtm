---
draft: true
sidebar_position: 90
slug: /instruments/videomancer/dotmatrix
title: "Dotmatrix"
image: /img/instruments/videomancer/dotmatrix/dotmatrix_hero_s1.png
description: "Before inkjet printers and laser engines, the dominant output device for personal computers was the impact dot-matrix printer."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import dotmatrix_control_panel from '/img/instruments/videomancer/dotmatrix/dotmatrix_control_panel.png';
import dotmatrix_source1_castle from '/img/instruments/videomancer/dotmatrix/dotmatrix_source1_castle.png';
import dotmatrix_source2_car from '/img/instruments/videomancer/dotmatrix/dotmatrix_source2_car.png';
import dotmatrix_source3_turtle from '/img/instruments/videomancer/dotmatrix/dotmatrix_source3_turtle.png';
import dotmatrix_source4_pattern from '/img/instruments/videomancer/dotmatrix/dotmatrix_source4_pattern.png';
import dotmatrix_source5_girl from '/img/instruments/videomancer/dotmatrix/dotmatrix_source5_girl.png';
import dotmatrix_source6_berries from '/img/instruments/videomancer/dotmatrix/dotmatrix_source6_berries.png';
import dotmatrix_hero_s1 from '/img/instruments/videomancer/dotmatrix/dotmatrix_hero_s1.png';
import dotmatrix_hero_s2 from '/img/instruments/videomancer/dotmatrix/dotmatrix_hero_s2.png';
import dotmatrix_hero_s3 from '/img/instruments/videomancer/dotmatrix/dotmatrix_hero_s3.png';
import dotmatrix_hero_s4 from '/img/instruments/videomancer/dotmatrix/dotmatrix_hero_s4.png';
import dotmatrix_hero_s5 from '/img/instruments/videomancer/dotmatrix/dotmatrix_hero_s5.png';
import dotmatrix_hero_s6 from '/img/instruments/videomancer/dotmatrix/dotmatrix_hero_s6.png';
import dotmatrix_ex1_s1 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex1_s1.png';
import dotmatrix_ex1_s2 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex1_s2.png';
import dotmatrix_ex1_s3 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex1_s3.png';
import dotmatrix_ex1_s4 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex1_s4.png';
import dotmatrix_ex1_s5 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex1_s5.png';
import dotmatrix_ex1_s6 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex1_s6.png';
import dotmatrix_ex2_s1 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex2_s1.png';
import dotmatrix_ex2_s2 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex2_s2.png';
import dotmatrix_ex2_s3 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex2_s3.png';
import dotmatrix_ex2_s4 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex2_s4.png';
import dotmatrix_ex2_s5 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex2_s5.png';
import dotmatrix_ex2_s6 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex2_s6.png';
import dotmatrix_ex3_s1 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex3_s1.png';
import dotmatrix_ex3_s2 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex3_s2.png';
import dotmatrix_ex3_s3 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex3_s3.png';
import dotmatrix_ex3_s4 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex3_s4.png';
import dotmatrix_ex3_s5 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex3_s5.png';
import dotmatrix_ex3_s6 from '/img/instruments/videomancer/dotmatrix/dotmatrix_ex3_s6.png';

# Dotmatrix

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: dotmatrix_source1_castle, after: dotmatrix_hero_s1 },
    { label: "Car", before: dotmatrix_source2_car, after: dotmatrix_hero_s2 },
    { label: "Turtle", before: dotmatrix_source3_turtle, after: dotmatrix_hero_s3 },
    { label: "Pattern", before: dotmatrix_source4_pattern, after: dotmatrix_hero_s4 },
    { label: "Girl", before: dotmatrix_source5_girl, after: dotmatrix_hero_s5 },
    { label: "Berries", before: dotmatrix_source6_berries, after: dotmatrix_hero_s6 },
  ]}
/>
*Dotmatrix rendering photographic video as discrete ink impacts on tinted paper through grid-based halftone printing simulation.*

---

## Overview

Before inkjet printers and laser engines, the dominant output device for personal computers was the impact dot-matrix printer. A print head containing a vertical column of pins (typically 9 or 24) swept horizontally across the page, striking an ink ribbon to leave dots on paper. Images were rendered as halftone grids — dark areas received large, closely spaced dots while bright areas received small, sparse ones. The result was a distinctive mechanical aesthetic: visible grid structure, limited tonal range, and the characteristic sound of pins hammering at high speed.

Dotmatrix recreates this process as a real-time video effect. The screen is divided into a regular grid of cells at power-of-two spacing (4×4, 8×8, or 16×16 pixels depending on head type). Within each cell, a dot is placed at the grid intersection whose radius is proportional to the inverse of source luminance — dark source regions produce large dots, bright regions produce small dots or no dot at all. The result is a halftone rendering where the video image emerges from the pattern of dots on a colored paper background. The name references both the printer technology and the literal matrix of dots that constitutes the output.

At subtle settings with high ink density and full mix, Dotmatrix produces a convincing simulation of printed output complete with paper tint and ribbon fade. At extreme settings — large grid, heavy jitter, draft mode — the image dissolves into a loose field of scattered ink spots that only suggest their source material from a distance.

---

## Quick Start

1. **Head type is the coarsest control**: Before adjusting anything else, choose the grid resolution. 24-Pin for detail, 9-Pin/Inkjet for balanced, Thermal for bold graphic impact.
2. **Ink and ribbon stack**: Both controls affect dot darkness independently. Maximum contrast requires high Ink Density *and* high Ribbon. Use Ribbon alone to simulate wear without changing base ink color.
3. **Draft mode halves density**: Draft skips every other column, creating a lighter, faster-looking print. Combine with high Dot Size to maintain tonal range despite the gaps.

---

## Background

### Impact Printing and the Epson MX-80

The dot-matrix printer era began in earnest with the Epson MX-80, introduced in 1980. Its 9-pin print head could produce text and simple graphics by selectively firing solenoid-driven pins against an ink ribbon. The key insight was that any image could be represented as a grid of dots — the same principle behind newspaper halftone printing, but executed mechanically rather than photographically. Later 24-pin models like the Epson LQ-1500 dramatically improved resolution by packing more pins into the same head height, producing what was marketed as "near letter quality" output.

### Halftone Dot Rendering

Halftone printing represents continuous tones through dots of varying size arranged on a regular grid. In a halftone cell, each intersection point can hold a dot whose area is proportional to the desired darkness. The human visual system spatially averages these dots at normal viewing distances, perceiving smooth tonal gradations. Dotmatrix implements this principle using Manhattan distance from cell center as the dot shape metric — producing diamond-shaped dots rather than circular ones, which is computationally efficient and visually distinctive.

### Manhattan Distance and Grid Geometry

The Manhattan distance (also called taxicab distance or L1 norm) between two points is the sum of the absolute differences of their coordinates: |dx| + |dy|. Unlike Euclidean distance, which produces circular contours, Manhattan distance produces diamond-shaped (rotated square) contours. This metric is natural for FPGA implementation because it requires only addition and subtraction — no multiplication or square root. The diamond-shaped dots it produces are reminiscent of the slightly irregular impact marks left by physical printer pins striking through a ribbon.

### Bidirectional Printing

Early dot-matrix printers printed in one direction only (left-to-right), then returned the carriage before printing the next line. Bidirectional printing doubled throughput by printing in both directions — left-to-right on even rows, right-to-left on odd rows. This introduced a characteristic visual artifact: slight horizontal misalignment between adjacent rows due to mechanical backlash in the carriage mechanism. Dotmatrix simulates the directional alternation through its DDS-driven sweep reveal, reversing the fill direction on alternate grid rows when bidirectional mode is enabled.

### Ribbon Fade and Ink Density

Impact printers used a continuous loop of inked fabric ribbon. As the ribbon cycled through the print head, its ink supply gradually depleted, producing progressively lighter impressions. Fresh ribbon produced dense, saturated black dots; worn ribbon produced faded gray-brown marks. This gradual degradation was a defining characteristic of dot-matrix output — documents printed on aging ribbon had a distinctive washed-out quality. Dotmatrix models this through separate Ink Density and Ribbon controls that independently set the base dot darkness and the fade attenuation applied on top.


---

## Signal Flow

Input Register → Grid Position → Dot Threshold Compare → Colour Composite

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Parameter Latch
│   ├─ Latch parameters from SPI registers
│   ├─ Derive grid mask, shift, half_cell from head_type
│   ├─ Compute paper colour (Y/U/V) from paper_hue
│   ├─ Compute ink colour (Y/U/V) from ink_dens + ribbon fade
│   ├─ Position counters (h_count, v_count)
│   ├─ LFSR advance (16-bit Galois, taps 16,14,13,11)
│   └─ DDS sweep position advance (per frame)
│
├── Stage 2: Grid Position + Manhattan Distance
│   ├─ Cell position: v_px = h_count AND grid_mask
│   ├─ Cell position: v_py = v_count AND grid_mask
│   ├─ v_dx = |v_px - half_cell|
│   ├─ v_dy = |v_py - half_cell|
│   ├─ s_manhattan = v_dx + v_dy
│   ├─ Dot radius = inverse luma (1023 - Y) >> 5, clamped to max_radius
│   ├─ Jitter: if jitter > 256, add LFSR[1:0] to radius
│   └─ s_is_odd_row = v_count(grid_shift)
│
├── Stage 3: Dot Threshold Compare
│   ├─ s_is_dot = (manhattan < dot_radius)
│   ├─ s_is_draft_skip = draft AND h_count(0)
│   └─ s_is_swept = sweep reveal check (row + column, bidi alternation)
│
├── Stage 4: Colour Composite
│   ├─ if (is_dot AND NOT draft_skip AND is_swept): output ink colour
│   └─ else: output paper colour
│
├── Interpolator Stage (4 clocks × 3 channels)
│   ├─ mix_y: lerp(dry_y, comp_y, mix_amount)
│   ├─ mix_u: lerp(dry_u, comp_u, mix_amount)
│   └─ mix_v: lerp(dry_v, comp_v, mix_amount)
│
├── Sync Delay Pipeline (8 clocks)
│   └─ hsync_n, vsync_n, field_n, Y, U, V delayed to match processing
│
└── Output Assignment
    ├─ Bypass off: output = mix result
    └─ Bypass on: output = delayed input
```

The critical path through Dotmatrix is the relationship between source luminance and dot radius. The inverse mapping — dark source produces large dot — is the fundamental halftone principle, and it occurs in Stage 2 where `(1023 - Y_in) >> 5` produces a 5-bit radius that is compared against Manhattan distance in Stage 3. The grid geometry (cell size and half-cell offset) is derived combinatorially from the head type toggle, meaning grid resolution changes take effect immediately without any pipeline flush.

The sweep reveal mechanism operates independently from the dot rendering pipeline. It is a frame-rate DDS accumulator that advances the virtual print head position, gating which dots appear based on whether the head has "reached" that screen position. When feed mode is disabled, the full image is revealed immediately. Bidirectional mode reverses the sweep direction on alternate grid rows, producing the characteristic striped reveal pattern of real bidirectional printers.

---

## Parameter Reference

<img src={dotmatrix_control_panel} alt="Videomancer front panel with Dotmatrix loaded"/>
*Videomancer's front panel with Dotmatrix active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Print Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, the sweep advances very slowly, revealing the image one narrow column at a time. At 100%, the sweep races across the frame in a few fields, producing rapid progressive disclosure. When Feed is off, the entire image is printed instantly regardless of this setting. The sweep is a DDS accumulator that advances by a scaled version of this register every frame, wrapping back to column zero and advancing one grid row each time it reaches the right edge of the screen. Internally, controls the speed of the horizontal print head sweep when Feed mode is active.

---

#### Knob 2 — Dot Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, dots are vanishingly small — the output is essentially blank paper. At 100%, dots can fill their entire cell, producing solid ink coverage in dark source areas. The actual dot size at any pixel is the minimum of this maximum and the inverse-luma-derived radius, so this control acts as a ceiling on dot density. Moderate settings (40–60%) produce the most visually interesting halftone textures where tonal variation is clearly visible as dot size variation. Internally, sets the maximum dot radius within each grid cell.

---

#### Knob 3 — Ink Dens
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, ink is nearly transparent — dots are barely visible against the paper background. At 100%, ink is solid black. The VHDL computes ink luma as `(1023 - ink_dens) >> 1`, so this is a direct brightness control for the dot color. High ink density with low ribbon fade produces the dense, saturated marks of a fresh ribbon; low ink density simulates faded or diluted ink. Internally, controls the darkness of the ink.

---

#### Knob 4 — Ribbon
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies a secondary fade attenuation to the ink color, simulating the gradual depletion of ink from a ribbon cartridge. When this control is below 50%, additional brightness is added to the ink luma: `ink_y + (1023 - ribbon) >> 2`. At 100%, no fade is applied. Reducing this control progressively washes out the dots, mimicking the way a well-used ribbon produces lighter and less distinct impacts. The interaction with Ink Density is additive — both contribute to the final ink brightness independently.

---

#### Knob 5 — Jitter
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds pseudo-random perturbation to the dot radius on a per-pixel basis. The LFSR provides 2 bits of jitter that are added to the computed radius when this control exceeds 25%. At low settings, dots have precise, uniform edges. As jitter increases, dot boundaries become irregular and ragged, simulating the mechanical imprecision of pin impacts — variations in ribbon contact pressure, paper surface texture, and solenoid timing that cause real dot-matrix output to look slightly different on every pass.

---

#### Knob 6 — Paper Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

At 0° (register 0), paper is pure white (Y=940, neutral chroma). From 90° to 180°, paper takes on a green tint simulating recycled or colored stock. Above 180° to 270°, paper shifts to a cool blue-white tone. Above 270°, paper becomes warm cream-yellow, simulating aged or thermal paper. The tinting is applied to all three YUV channels of the paper color, so the background has both brightness and chroma variation. Internally, selects the paper background color by cycling through four tint zones.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Head** | 9-Pin | Inkjet |
| **8 — Dir** | Uni | Bidi |
| **9 — Draft** | Off | On |
| **10 — Feed** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches form a mixed-function group. Toggle 7 selects the print head type from four options, which directly determines the grid cell size and thus the spatial resolution of the halftone pattern. Toggles 8–10 are independent binary switches controlling directional printing, draft quality, and feed animation respectively. Toggle 11 is the standard bypass switch. The head type toggle uses a 2-bit encoding (bits 1:0 of the toggle register), while the remaining toggles occupy individual bits (2–5).

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Dotmatrix-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from basic halftone rendering to animated print simulations. Each explores a different aspect of the dot-matrix printing model.

### Exercise 1: Classic Halftone

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: dotmatrix_source1_castle, after: dotmatrix_ex1_s1 },
    { label: "Car", before: dotmatrix_source2_car, after: dotmatrix_ex1_s2 },
    { label: "Turtle", before: dotmatrix_source3_turtle, after: dotmatrix_ex1_s3 },
    { label: "Pattern", before: dotmatrix_source4_pattern, after: dotmatrix_ex1_s4 },
    { label: "Girl", before: dotmatrix_source5_girl, after: dotmatrix_ex1_s5 },
    { label: "Berries", before: dotmatrix_source6_berries, after: dotmatrix_ex1_s6 },
  ]}
/>
*Classic Halftone — simulated result across source images.*
**Source**: A portrait or still image with a wide range of tones from deep shadows to bright highlights.

**What You'll Create**: Learn how inverse-luma dot sizing creates a halftone rendering and how grid resolution affects the result.

1. **Initialize**: Set all controls to default positions. Feed off, bypass off, mix at 100%.
2. **Basic halftone**: Increase Dot Size to about 60%. Dark areas fill with large dots, bright areas remain mostly paper. This is the fundamental halftone effect.
3. **Grid resolution**: Switch Head from 9-Pin to 24-Pin. Note how the finer 4×4 grid resolves more image detail. Switch to Thermal (16×16) to see the coarsest grid — individual dots are clearly visible as diamond shapes.
4. **Ink and paper**: Increase Ink Density to 80% for solid black dots. Then rotate Paper Hue past 270° to switch from white paper to warm cream — the image now looks like it was printed on aged continuous-feed paper.
5. **Ribbon wear**: Reduce Ribbon to 30%. The dots fade to gray, simulating a depleted ink ribbon. Increase Ink Density to compensate partially.

**Key concepts**: Inverse-luma dot sizing is the halftone principle, grid cell size determines spatial resolution, ink and paper colors are independent parameters

---

### Exercise 2: Bidirectional Sweep Animation

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: dotmatrix_source1_castle, after: dotmatrix_ex2_s1 },
    { label: "Car", before: dotmatrix_source2_car, after: dotmatrix_ex2_s2 },
    { label: "Turtle", before: dotmatrix_source3_turtle, after: dotmatrix_ex2_s3 },
    { label: "Pattern", before: dotmatrix_source4_pattern, after: dotmatrix_ex2_s4 },
    { label: "Girl", before: dotmatrix_source5_girl, after: dotmatrix_ex2_s5 },
    { label: "Berries", before: dotmatrix_source6_berries, after: dotmatrix_ex2_s6 },
  ]}
/>
*Bidirectional Sweep Animation — simulated result across source images.*
**Source**: A slowly moving video feed or a static image with strong horizontal structure.

**What You'll Create**: Explore the sweep reveal and bidirectional printing animation.

1. **Enable feed**: Turn Feed on. Set Print Speed to about 30%. The image begins to reveal from the top-left, one column at a time as the virtual head sweeps across.
2. **Watch the sweep**: The head sweeps left-to-right, then jumps back to start a new row. The image builds up progressively like a real printer scanning across paper.
3. **Enable bidi**: Switch Dir to Bidi. Now even rows fill left-to-right and odd rows fill right-to-left. The reveal pattern becomes a zigzag, more closely matching real bidirectional printers.
4. **Speed variation**: Increase Print Speed to 80% for rapid printing. Reduce to 10% for a slow, dramatic reveal.
5. **Draft mode**: Enable Draft. The dots become sparser, creating visible gaps that let the paper show through — mimicking the speed/quality tradeoff of real draft printing.

**Key concepts**: DDS sweep reveal simulates print head traversal, bidirectional alternation doubles effective speed, draft mode skips columns for a lighter texture

---

### Exercise 3: Textured Print Artifacts

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: dotmatrix_source1_castle, after: dotmatrix_ex3_s1 },
    { label: "Car", before: dotmatrix_source2_car, after: dotmatrix_ex3_s2 },
    { label: "Turtle", before: dotmatrix_source3_turtle, after: dotmatrix_ex3_s3 },
    { label: "Pattern", before: dotmatrix_source4_pattern, after: dotmatrix_ex3_s4 },
    { label: "Girl", before: dotmatrix_source5_girl, after: dotmatrix_ex3_s5 },
    { label: "Berries", before: dotmatrix_source6_berries, after: dotmatrix_ex3_s6 },
  ]}
/>
*Textured Print Artifacts — simulated result across source images.*
**Source**: High-contrast footage with sharp edges — text overlays, graphic patterns, or architectural subjects.

**What You'll Create**: Combine jitter, draft mode, and ribbon fade to create rich print-like textures.

1. **High jitter**: Set Jitter to about 70%. Dot edges become ragged and irregular, breaking up the clean diamond shapes into rough, organic marks.
2. **Draft gaps**: Enable Draft mode. The combination of jitter and draft skipping creates a loose, stippled texture.
3. **Worn ribbon**: Reduce Ribbon to about 20% and increase Ink Density to 90%. The dots are faded but dense — the look of aggressively used, nearly exhausted ribbon on cheap paper.
4. **Paper color**: Rotate Paper Hue to the green zone (about 120°) for colored stock, or to warm cream (about 300°) for the classic continuous-feed tractor paper look.
5. **Mix overlay**: Reduce Mix to about 50%. The halftone pattern blends with the original video, creating a semi-transparent overlay effect.
6. **Head comparison**: Cycle through all four Head modes to see how grid resolution interacts with the texture settings.

**Key concepts**: Jitter breaks geometric regularity, draft mode creates intentional sparsity, ribbon fade and ink density combine additively, mix allows halftone overlay

---


## Tips

- **Feed creates animation**: The sweep reveal is the program's most distinctive temporal effect. Slow print speeds create dramatic progressive disclosure; fast speeds quickly fill the frame.
- **Jitter has a threshold**: The jitter effect activates abruptly when the control exceeds 25%. Below that, dots are geometrically perfect. Use zero jitter for clean halftone, moderate jitter for organic texture.
- **Paper Hue for era styling**: White paper = modern laser print. Warm cream = continuous-feed tractor paper. Green tint = vintage greenbar paper. Cool blue = blueprint stock.
- **Mix for overlay effects**: Reducing Mix below 100% blends the halftone with the original video, useful for semi-transparent print overlay or watermark-style effects.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bidirectional Printing** | A printing mode where the head prints in both directions (left-to-right and right-to-left) to increase throughput, potentially introducing slight row misalignment. |
| **DDS** | Direct Digital Synthesis; a frequency accumulator technique used here to generate the sweep position at a programmable rate. |
| **Draft Mode** | A reduced-quality print mode that skips alternate columns to double effective printing speed at the cost of horizontal resolution. |
| **Halftone** | A reprographic technique that simulates continuous tone through dots of varying size arranged on a regular grid. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator that produces deterministic noise sequences used for dot jitter. |
| **Manhattan Distance** | The sum of absolute differences along each axis (|dx| + |dy|), producing diamond-shaped distance contours rather than circles. |
| **Ribbon Fade** | The gradual depletion of ink from a printer ribbon with use, producing progressively lighter dot impacts. |

---
