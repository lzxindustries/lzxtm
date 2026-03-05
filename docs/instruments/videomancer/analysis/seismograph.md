---
draft: true
sidebar_position: 264
slug: /instruments/videomancer/seismograph
title: "Seismograph"
image: /img/instruments/videomancer/seismograph/seismograph_hero_s1.png
description: "Before digital oscilloscopes and computer displays, scientific instruments recorded data by dragging an inked pen across a moving strip of paper."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import seismograph_control_panel from '/img/instruments/videomancer/seismograph/seismograph_control_panel.png';
import seismograph_source1_runner from '/img/instruments/videomancer/seismograph/seismograph_source1_runner.png';
import seismograph_source2_ballerina from '/img/instruments/videomancer/seismograph/seismograph_source2_ballerina.png';
import seismograph_source3_elephant from '/img/instruments/videomancer/seismograph/seismograph_source3_elephant.png';
import seismograph_source4_pattern from '/img/instruments/videomancer/seismograph/seismograph_source4_pattern.png';
import seismograph_source5_woman from '/img/instruments/videomancer/seismograph/seismograph_source5_woman.png';
import seismograph_source6_wood from '/img/instruments/videomancer/seismograph/seismograph_source6_wood.png';
import seismograph_hero_s1 from '/img/instruments/videomancer/seismograph/seismograph_hero_s1.png';
import seismograph_hero_s2 from '/img/instruments/videomancer/seismograph/seismograph_hero_s2.png';
import seismograph_hero_s3 from '/img/instruments/videomancer/seismograph/seismograph_hero_s3.png';
import seismograph_hero_s4 from '/img/instruments/videomancer/seismograph/seismograph_hero_s4.png';
import seismograph_hero_s5 from '/img/instruments/videomancer/seismograph/seismograph_hero_s5.png';
import seismograph_hero_s6 from '/img/instruments/videomancer/seismograph/seismograph_hero_s6.png';
import seismograph_ex1_s1 from '/img/instruments/videomancer/seismograph/seismograph_ex1_s1.png';
import seismograph_ex1_s2 from '/img/instruments/videomancer/seismograph/seismograph_ex1_s2.png';
import seismograph_ex1_s3 from '/img/instruments/videomancer/seismograph/seismograph_ex1_s3.png';
import seismograph_ex1_s4 from '/img/instruments/videomancer/seismograph/seismograph_ex1_s4.png';
import seismograph_ex1_s5 from '/img/instruments/videomancer/seismograph/seismograph_ex1_s5.png';
import seismograph_ex1_s6 from '/img/instruments/videomancer/seismograph/seismograph_ex1_s6.png';
import seismograph_ex2_s1 from '/img/instruments/videomancer/seismograph/seismograph_ex2_s1.png';
import seismograph_ex2_s2 from '/img/instruments/videomancer/seismograph/seismograph_ex2_s2.png';
import seismograph_ex2_s3 from '/img/instruments/videomancer/seismograph/seismograph_ex2_s3.png';
import seismograph_ex2_s4 from '/img/instruments/videomancer/seismograph/seismograph_ex2_s4.png';
import seismograph_ex2_s5 from '/img/instruments/videomancer/seismograph/seismograph_ex2_s5.png';
import seismograph_ex2_s6 from '/img/instruments/videomancer/seismograph/seismograph_ex2_s6.png';
import seismograph_ex3_s1 from '/img/instruments/videomancer/seismograph/seismograph_ex3_s1.png';
import seismograph_ex3_s2 from '/img/instruments/videomancer/seismograph/seismograph_ex3_s2.png';
import seismograph_ex3_s3 from '/img/instruments/videomancer/seismograph/seismograph_ex3_s3.png';
import seismograph_ex3_s4 from '/img/instruments/videomancer/seismograph/seismograph_ex3_s4.png';
import seismograph_ex3_s5 from '/img/instruments/videomancer/seismograph/seismograph_ex3_s5.png';
import seismograph_ex3_s6 from '/img/instruments/videomancer/seismograph/seismograph_ex3_s6.png';

# Seismograph

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: seismograph_source1_runner, after: seismograph_hero_s1 },
    { label: "Ballerina", before: seismograph_source2_ballerina, after: seismograph_hero_s2 },
    { label: "Elephant", before: seismograph_source3_elephant, after: seismograph_hero_s3 },
    { label: "Pattern", before: seismograph_source4_pattern, after: seismograph_hero_s4 },
    { label: "Woman", before: seismograph_source5_woman, after: seismograph_hero_s5 },
    { label: "Wood", before: seismograph_source6_wood, after: seismograph_hero_s6 },
  ]}
/>
*Seismograph rendering live video luminance as multi-channel pen traces on a scrolling chart recorder with persistence and fill-under.*

---

## Overview

Before digital oscilloscopes and computer displays, scientific instruments recorded data by dragging an inked pen across a moving strip of paper. Seismographs, electrocardiographs, chart recorders in chemical plants, and Richter-scale drum recorders all used this principle — a pen deflected by a measured quantity traces a continuous line on paper advancing at a constant speed. The resulting traces are simultaneously data visualizations and beautiful graphic objects in their own right.

Seismograph recreates this analog recording aesthetic inside the Videomancer video pipeline. The program divides the screen into horizontal bands — 2, 4, 8, or 16 — and within each band, a pen is deflected vertically by the source luminance sampled at that band's vertical position. The horizontal axis becomes the time axis. Configurable paper backgrounds, ink colors, grid ruling lines, fill-under shading, and IIR persistence trails complete the illusion of a multi-channel strip chart recorder rendering video content in real time.

The name references both the scientific instrument and the Greek *seismos* (shaking) — the program visualizes the "tremors" of luminance variation across the image, transforming video into a set of synchronized waveform traces that scroll, persist, and fill like a physical chart recording.

---

## Quick Start

1. **Trace count sets the analysis granularity**: 2 traces give a broad overview of top-half vs. bottom-half luminance; 16 traces give a fine-grained spatial luminance profile.
2. **Deflection sensitivity is your gain knob**: Low deflection for subtle modulation, high deflection for dramatic waveform swings. Clipping at band edges is normal and expected at high sensitivity.
3. **Black paper + colored ink = oscilloscope**: The combination of dark background with bright, thin traces and high persistence recreates the phosphor-glow aesthetic of analog test instruments.

---

## Background

### Strip Chart Recorders

The strip chart recorder is one of the oldest continuous data recording instruments. A roll of paper advances at a constant speed past a pen or set of pens, each connected to a galvanometer or other transducer. As the measured variable changes, the pen deflects, leaving a permanent ink trace on the paper. Multiple channels can be recorded simultaneously by stacking pens at different vertical offsets. The paper often carries pre-printed grid lines — sometimes in a distinctive green or blue — to aid quantitative reading. Seismograph's grid overlay, paper color selection, and multi-channel band layout all reference this design tradition.

### Oscilloscope Aesthetics

While strip chart recorders are continuous-time instruments, oscilloscopes are triggered-sweep instruments that repeatedly paint a trace across a phosphor screen. The visual language is similar — a bright line (the trace) moves across a darker background — but oscilloscopes add phosphor persistence, where old traces fade gradually rather than disappearing instantly. Seismograph's persistence control implements a similar effect via IIR feedback through a line buffer: the previous frame's pen positions are stored and blended with the current frame's, creating ghostly trails that fade over time.

### Pen Physics and Manhattan Distance Rendering

On a real chart recorder, the pen is a physical object with finite width — a felt-tip, ball-point, or capillary tube that lays down a line several pixels wide. Seismograph simulates this by rendering the pen trace as a distance field: for each output pixel, the program computes the Manhattan distance from the pixel to the pen position, and if that distance falls within the configurable pen width, the pixel is inked. This produces a characteristic diamond-shaped cross-section rather than a perfectly round one, which subtly evokes the anisotropic marks of real recording pens.

### Horizontal Scrolling

Physical chart recorders move the paper past the pen at a constant speed, so the temporal axis scrolls continuously. In Seismograph's VHDL implementation, a horizontal offset accumulator increments each frame, shifting the effective sample position. When freeze is engaged, the accumulator stops and the chart holds its current state — analogous to stopping the paper motor on a recorder to examine a particular section of the trace.

### Fill-Under and Area Charts

Area charts — traces with the region between the curve and a baseline filled with color — were popularized by William Playfair in the late 18th century. Seismograph's fill-under mode fills the region between each pen trace and its band center, creating a stacked area visualization. The fill uses a semi-transparent blend (approximately 75% paper, 25% ink), so the paper and grid remain partially visible beneath the fill, preserving readability.


---

## Signal Flow

Input Register + Counters → Band Compute → Deflection → Pen Compare + Grid + Fill → Color Compose

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Counters ─────────────────────────
│   ├─ Register input luma (Y)
│   ├─ Position counters: h_count, v_count
│   └─ Scroll offset accumulator (advances each frame unless frozen)
│
├── Stage 2: Band Compute ──────────────────────────────────────
│   ├─ Power-of-2 band heights: 1080 / {2,4,8,16} traces
│   ├─ band_index = v_count >> log2(band_height)
│   ├─ band_center = (v_count & mask) + half_height
│   └─ Pre-compute |luma − 512| and sign
│
├── Stage 3: Deflection + Line Buffer Write ────────────────────
│   ├─ Scale |luma − 512| by 8 deflection levels (shift-based)
│   ├─ pen_target = band_center ± scaled_value (clamp 0–1079)
│   └─ Write pen_target to line buffer (BRAM)
│
├── Stages 4–5: BRAM Read Latency ─────────────────────────────
│   └─ 2-clock pipeline delay for line buffer read
│
├── Stage 6: Pen Compare + Grid + Fill ─────────────────────────
│   ├─ pen_hit: |v_count − pen_target| ≤ pen_half
│   ├─ fill_hit: v_count between pen_target and band_center
│   └─ grid_hit: h_count or v_count on grid spacing boundary
│
├── Stage 7: Color Compose ─────────────────────────────────────
│   ├─ Priority: pen > fill > grid > paper
│   ├─ Paper color: White / Grid Gray / Sepia / Black
│   ├─ Ink color: Dark / Red / Green / Blue (from pen hue)
│   └─ Fill: 75% paper + 25% ink blend
│
├── Interpolator: Wet/Dry Mix ──────────────────────────────────
│   └─ 3× interpolator_u: crossfade original ↔ chart (4 clocks)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical design feature is the **shift-based band computation** in stage 2. Because the trace count is always a power of two (2, 4, 8, 16), the band height is always a power of two (540, 270, 135, 67.5 — rounded), and the band index can be computed by bit-shifting v_count rather than dividing. This eliminates all division hardware and keeps the pipeline purely combinational at each stage. The **line buffer** in stage 3 stores pen positions from the previous frame for persistence rendering. The BRAM requires 2 clock cycles of read latency (stages 4–5), which is absorbed into the pipeline as transparent delay stages. The **color composition** in stage 7 uses a strict priority order — pen trace line on top, then fill-under region, then grid ruling, then paper background — matching the physical layering of ink-on-paper-on-grid in a real chart recorder.

---

## Parameter Reference

<img src={seismograph_control_panel} alt="Videomancer front panel with Seismograph loaded"/>
*Videomancer's front panel with Seismograph active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Traces
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 9 |

Selects the number of horizontal trace bands: 2, 4, 8, or 16. With 2 traces, each band occupies roughly half the screen height — a wide-format two-channel recorder. With 16 traces, each band is only about 67 pixels tall, creating a dense multi-channel display. The trace count determines the spatial resolution of the luminance sampling — fewer traces means each trace integrates a wider vertical stripe of the source video, more traces means finer vertical sampling.

---

#### Knob 2 — Deflect
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At low deflection, the pen traces stay near their band centers — small, subtle wiggles. At high deflection, the pen swings far from center and can even clip against the band edges, producing waveforms that fold over themselves. The deflection scale directly controls how dramatically the video luminance is visualized. Internally, controls the vertical deflection amplitude via 8 shift-based sensitivity levels, ranging from 0.125× to 4× gain.

---

#### Knob 3 — Pen Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At minimum, the pen is a single-pixel hairline trace. As pen width increases, the trace becomes a thicker line with a diamond-shaped cross-section. Very wide pen settings create bold, graphic traces that dominate the visual field and begin to overlap between adjacent bands. Internally, sets the pen thickness by controlling the Manhattan distance threshold for pen-hit detection.

---

#### Knob 4 — Scroll Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At zero, the chart does not scroll — the traces are static waveforms. As speed increases, the chart scrolls leftward like advancing paper, and the luminance sampling position shifts horizontally across the source image. Higher speeds produce faster apparent motion and more compressed waveforms in the time axis. Internally, controls the horizontal scroll speed by setting the per-frame increment of the scroll offset accumulator.

---

#### Knob 5 — Persist
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At zero persistence, only the current frame's pen position is visible — a sharp, instantaneous trace. As persistence increases, previous pen positions remain visible as ghostly afterimages, creating trailing tails behind the moving pen. At maximum, traces accumulate into dense overlapping bands showing the full history of pen motion. Internally, sets the persistence / trail length by controlling the IIR feedback through the line buffer.

---

#### Knob 6 — Pen Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Controls the ink color by selecting hue-based presets. The parameter is divided into four zones: dark ink (near-black), red ink, green ink, and blue ink. Each preset defines a full YUV triplet tuned to produce a saturated, high-contrast trace against the paper backgrounds. The ink color affects pen traces, fill-under regions, and — at reduced opacity — the grid ruling lines.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Multi | Envelope |
| **8 — Paper** | White | Black |
| **9 — Fill Under** | Off | On |
| **10 — Freeze** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 are each 2-bit selectors (using adjacent register bits) that select the operating mode and paper style respectively. Toggle 9 enables fill-under, toggle 10 freezes the scroll, and toggle 11 provides bypass. The mode and paper toggles each select from four options, unlike standard on/off toggles.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) and wet (processed) signal via three interpolator_u instances. At 100% the full chart recorder effect is visible. At 0% the original video passes through unaltered. Intermediate values create a ghostly overlay of chart traces on top of recognizable video content, which can produce interesting composite visualizations where the source image is partially visible behind the traces.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Seismograph processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from a simple two-channel trace to a dense multi-band visualization. Each exercise demonstrates different aspects of the chart recorder — trace count, deflection, paper styles, and fill-under interactions.

### Exercise 1: Two-Channel Waveform

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: seismograph_source1_runner, after: seismograph_ex1_s1 },
    { label: "Ballerina", before: seismograph_source2_ballerina, after: seismograph_ex1_s2 },
    { label: "Elephant", before: seismograph_source3_elephant, after: seismograph_ex1_s3 },
    { label: "Pattern", before: seismograph_source4_pattern, after: seismograph_ex1_s4 },
    { label: "Woman", before: seismograph_source5_woman, after: seismograph_ex1_s5 },
    { label: "Wood", before: seismograph_source6_wood, after: seismograph_ex1_s6 },
  ]}
/>
*Two-Channel Waveform — simulated result across source images.*
**Source**: A high-contrast video feed with distinct bright and dark regions — black-and-white patterns, silhouettes, or text on a bright background.

**What You'll Create**: Learn how luminance drives pen deflection across two wide trace bands, and how deflection sensitivity controls the visual drama.

1. **Set up 2 traces**: Set Traces to the first step (2 bands). The screen splits into two wide horizontal bands.
2. **Low deflection**: Set Deflect to about 20%. The pen traces show subtle wiggles near the band centers.
3. **Increase deflection**: Sweep Deflect toward 80%. The traces respond dramatically, swinging far from center as the source luminance varies.
4. **Pen width**: Start with Pen Width at minimum (hairline). Increase to about 40% — the traces thicken into bold graphic strokes.
5. **Paper selection**: Try White paper, then switch to Grid (toggle 8). Ruling lines appear behind the traces, providing a measurement scale.
6. **Scroll**: Enable scrolling with moderate speed (~40%). Watch the traces advance horizontally like a chart recorder printout.

**Key concepts**: Each band samples luma from a vertical stripe of the source, deflection maps luma to pen displacement from band center, Manhattan distance determines pen hit

---

### Exercise 2: Multi-Channel Area Chart

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: seismograph_source1_runner, after: seismograph_ex2_s1 },
    { label: "Ballerina", before: seismograph_source2_ballerina, after: seismograph_ex2_s2 },
    { label: "Elephant", before: seismograph_source3_elephant, after: seismograph_ex2_s3 },
    { label: "Pattern", before: seismograph_source4_pattern, after: seismograph_ex2_s4 },
    { label: "Woman", before: seismograph_source5_woman, after: seismograph_ex2_s5 },
    { label: "Wood", before: seismograph_source6_wood, after: seismograph_ex2_s6 },
  ]}
/>
*Multi-Channel Area Chart — simulated result across source images.*
**Source**: Slowly moving footage with gradual luminance variations — landscapes, cloud formations, or abstract gradients.

**What You'll Create**: Explore fill-under mode and how it transforms line traces into area charts across 8 or 16 bands.

1. **Set 8 traces**: Increase Traces to step 3 (8 bands). The screen divides into 8 narrow bands.
2. **Moderate deflection**: Set Deflect to about 50%.
3. **Enable fill-under**: Toggle Fill Under on. The area between each trace and its band center fills with semi-transparent ink.
4. **Add persistence**: Increase Persist to ~60%. Previous pen positions leave ghostly trails, and the filled areas accumulate into dense overlapping regions.
5. **Change ink**: Switch Pen Hue through the four color options — dark, red, green, blue. Each produces a dramatically different area chart aesthetic.
6. **Try Sepia paper**: Switch Paper to Sepia for a vintage chart recorder look.
7. **16 traces**: Increase Traces to the maximum (16). The bands become very narrow and the filled areas create a dense striped visualization.

**Key concepts**: Fill-under creates area charts from line traces, persistence accumulates trace history, narrow bands with fill produce stripe-like patterns

---

### Exercise 3: Oscilloscope Display

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: seismograph_source1_runner, after: seismograph_ex3_s1 },
    { label: "Ballerina", before: seismograph_source2_ballerina, after: seismograph_ex3_s2 },
    { label: "Elephant", before: seismograph_source3_elephant, after: seismograph_ex3_s3 },
    { label: "Pattern", before: seismograph_source4_pattern, after: seismograph_ex3_s4 },
    { label: "Woman", before: seismograph_source5_woman, after: seismograph_ex3_s5 },
    { label: "Wood", before: seismograph_source6_wood, after: seismograph_ex3_s6 },
  ]}
/>
*Oscilloscope Display — simulated result across source images.*
**Source**: Any active video input — waveform generators, live camera, or recorded footage with motion.

**What You'll Create**: Create an oscilloscope-style display using black paper, green ink, and high persistence.

1. **Black paper**: Switch Paper to Black. The background goes dark.
2. **Green ink**: Set Pen Hue to approximately 270° (green ink zone).
3. **4 traces**: Set Traces to step 2 (4 bands).
4. **High persistence**: Set Persist to ~80%. Traces leave long, phosphor-like trails.
5. **Thin pen**: Set Pen Width to ~15% for a sharp CRT-like scan line.
6. **High deflection**: Set Deflect to ~70% for dramatic waveform swings.
7. **Scroll speed**: Set a moderate scroll speed (~50%) to create the classic oscilloscope sweep.
8. **Freeze and examine**: Toggle Freeze on to hold the display, then off to resume. This mimics the single-shot trigger on a real oscilloscope.

**Key concepts**: Paper color transforms the display character — black paper with bright ink creates an oscilloscope aesthetic, persistence simulates phosphor afterglow, freeze acts as a trigger hold

---


## Tips

- **Fill-under reveals amplitude**: Line traces show instantaneous position; fill-under shows *magnitude* by coloring the area between trace and baseline. Use it to make quiet vs. loud luminance regions visually obvious.
- **Freeze is your capture button**: Stop the chart to examine a particular moment. Resume to continue recording. This mimics single-shot triggering on a real oscilloscope.
- **Pen Width and Traces interact**: Wide pens with many narrow bands can cause traces to overlap, creating a dense, textured field rather than distinct individual channels.
- **Persistence blurs fast transients**: High persistence smears rapidly changing signals into broad trails. Use low persistence for sharp, responsive traces and high persistence for smooth, flowing visualizations.
- **Grid lines only appear in Grid paper mode**: The grid is enabled by the paper toggle's least significant bit, so only the Grid preset (01) shows ruling lines.

---

## Glossary

| Term | Definition |
|------|------------|
| **Band** | One horizontal subdivision of the screen, containing a single trace channel; height = screen height / trace count. |
| **Chart Recorder** | An analog instrument that records measured values as continuous pen traces on advancing paper. |
| **Deflection** | The vertical displacement of the pen from the band center, proportional to the sampled luminance value. |
| **Fill-Under** | Coloring the area between a trace curve and its baseline (band center), creating an area chart visualization. |
| **Galvanometer** | An electromagnetic instrument that converts electrical current to mechanical pen deflection in analog recorders. |
| **Grid** | Pre-printed or rendered horizontal and vertical ruling lines on chart recorder paper, aiding quantitative reading. |
| **IIR** | Infinite Impulse Response; a feedback-based filter structure; used here to describe the persistence trail decay. |
| **Line Buffer** | A BRAM-based storage element that holds one line's worth of pen position data for use in the next frame. |
| **Manhattan Distance** | The sum of absolute differences along horizontal and vertical axes; used for pen-hit detection (producing diamond-shaped cross-sections). |
| **Pen Hit** | The condition where a pixel is within the pen width threshold of the trace position, causing it to be rendered in ink color. |
| **Persistence** | The visual trail left by a trace as it moves, created by blending current and previous pen positions — analogous to phosphor afterglow. |
| **Scroll** | The continuous horizontal advancement of the chart, simulating paper advancing past a stationary pen. |
| **Trace** | A continuous line drawn by the pen, representing the sampled luminance value over the horizontal extent of each band. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
