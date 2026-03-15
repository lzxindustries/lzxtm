---
draft: true
sidebar_position: 319
slug: /instruments/videomancer/vectorscope
title: "Vectorscope"
image: /img/instruments/videomancer/vectorscope/vectorscope_hero_s1.png
description: "Vectorscope implements a real-time chrominance analysis display, plotting each pixel's U and V color coordinates as a dot on a two-dimensional grid."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import vectorscope_control_panel from '/img/instruments/videomancer/vectorscope/vectorscope_control_panel.png';
import vectorscope_source1_car from '/img/instruments/videomancer/vectorscope/vectorscope_source1_car.png';
import vectorscope_source2_boat from '/img/instruments/videomancer/vectorscope/vectorscope_source2_boat.png';
import vectorscope_source3_collage from '/img/instruments/videomancer/vectorscope/vectorscope_source3_collage.png';
import vectorscope_source4_pattern from '/img/instruments/videomancer/vectorscope/vectorscope_source4_pattern.png';
import vectorscope_source5_girl from '/img/instruments/videomancer/vectorscope/vectorscope_source5_girl.png';
import vectorscope_source6_paint from '/img/instruments/videomancer/vectorscope/vectorscope_source6_paint.png';
import vectorscope_hero_s1 from '/img/instruments/videomancer/vectorscope/vectorscope_hero_s1.png';
import vectorscope_hero_s2 from '/img/instruments/videomancer/vectorscope/vectorscope_hero_s2.png';
import vectorscope_hero_s3 from '/img/instruments/videomancer/vectorscope/vectorscope_hero_s3.png';
import vectorscope_hero_s4 from '/img/instruments/videomancer/vectorscope/vectorscope_hero_s4.png';
import vectorscope_hero_s5 from '/img/instruments/videomancer/vectorscope/vectorscope_hero_s5.png';
import vectorscope_hero_s6 from '/img/instruments/videomancer/vectorscope/vectorscope_hero_s6.png';
import vectorscope_ex1_s1 from '/img/instruments/videomancer/vectorscope/vectorscope_ex1_s1.png';
import vectorscope_ex1_s2 from '/img/instruments/videomancer/vectorscope/vectorscope_ex1_s2.png';
import vectorscope_ex1_s3 from '/img/instruments/videomancer/vectorscope/vectorscope_ex1_s3.png';
import vectorscope_ex1_s4 from '/img/instruments/videomancer/vectorscope/vectorscope_ex1_s4.png';
import vectorscope_ex1_s5 from '/img/instruments/videomancer/vectorscope/vectorscope_ex1_s5.png';
import vectorscope_ex1_s6 from '/img/instruments/videomancer/vectorscope/vectorscope_ex1_s6.png';
import vectorscope_ex2_s1 from '/img/instruments/videomancer/vectorscope/vectorscope_ex2_s1.png';
import vectorscope_ex2_s2 from '/img/instruments/videomancer/vectorscope/vectorscope_ex2_s2.png';
import vectorscope_ex2_s3 from '/img/instruments/videomancer/vectorscope/vectorscope_ex2_s3.png';
import vectorscope_ex2_s4 from '/img/instruments/videomancer/vectorscope/vectorscope_ex2_s4.png';
import vectorscope_ex2_s5 from '/img/instruments/videomancer/vectorscope/vectorscope_ex2_s5.png';
import vectorscope_ex2_s6 from '/img/instruments/videomancer/vectorscope/vectorscope_ex2_s6.png';
import vectorscope_ex3_s1 from '/img/instruments/videomancer/vectorscope/vectorscope_ex3_s1.png';
import vectorscope_ex3_s2 from '/img/instruments/videomancer/vectorscope/vectorscope_ex3_s2.png';
import vectorscope_ex3_s3 from '/img/instruments/videomancer/vectorscope/vectorscope_ex3_s3.png';
import vectorscope_ex3_s4 from '/img/instruments/videomancer/vectorscope/vectorscope_ex3_s4.png';
import vectorscope_ex3_s5 from '/img/instruments/videomancer/vectorscope/vectorscope_ex3_s5.png';
import vectorscope_ex3_s6 from '/img/instruments/videomancer/vectorscope/vectorscope_ex3_s6.png';

# Vectorscope

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Car", before: vectorscope_source1_car, after: vectorscope_hero_s1 },
    { label: "Boat", before: vectorscope_source2_boat, after: vectorscope_hero_s2 },
    { label: "Collage", before: vectorscope_source3_collage, after: vectorscope_hero_s3 },
    { label: "Pattern", before: vectorscope_source4_pattern, after: vectorscope_hero_s4 },
    { label: "Girl", before: vectorscope_source5_girl, after: vectorscope_hero_s5 },
    { label: "Paint", before: vectorscope_source6_paint, after: vectorscope_hero_s6 },
  ]}
/>
*Vectorscope rendering a real-time UV chrominance scatter plot on screen — a phosphor-glow display showing the color distribution of the input video as a two-dimensional dot cloud.*

---

## Overview

**Vectorscope** implements a real-time chrominance analysis display, plotting each pixel's U and V color coordinates as a dot on a two-dimensional grid. The result is the classic **vectorscope** — one of the standard measurement instruments in broadcast video engineering. Color-saturated content produces dots far from center; neutral content clusters around the origin. The spatial distribution of dots reveals the color balance, gamut utilization, and saturation characteristics of the input signal at a glance.

The implementation uses a 64×64×8-bit dual-port BRAM accumulator. During active video, each pixel's U and V values are quantized to 6 bits and used as a 2D address to increment the corresponding cell (saturating at 255). During vertical blanking, a decay sweep subtracts from all cells, implementing the phosphor persistence characteristic of analog vectorscope CRT displays. A second BRAM port reads the accumulator during rendering to draw the scope display at a fixed position on screen. The Intensity control scales the dot brightness, and four phosphor color options (Green, Amber, Blue, White) set the display colorimetry.

Vectorscope is in the **Analysis** category — a measurement and visualization tool rather than an effect.

---

## Quick Start

1. **Green for broadcast**: Green phosphor is the standard for professional vectorscope monitoring. Use it for technical accuracy checks.
2. **Persistence for music**: High persistence creates a glowing trace that builds up during a performance — excellent for visual art.
3. **Over Video for grading**: Overlay the scope on your video to simultaneously evaluate composition and color balance.

---

## Background

### What Is a Vectorscope?

A **vectorscope** is a specialized oscilloscope display used in video engineering to visualize the chrominance content of a signal. The horizontal axis represents the U (blue-difference) component and the vertical axis represents V (red-difference). A color bar test signal produces six dots at specific angles and radii corresponding to the primary and secondary colors. Live video produces a cloud of dots whose shape and position indicate the overall color balance. Vectorscopes are essential for color grading, white balance verification, and ensuring signals comply with broadcast transmission limits.

### What Is a Phosphor Display?

Classic analog vectorscopes used CRT (cathode ray tube) displays where the electron beam traces dots on a phosphor-coated screen. Each hit excites the phosphor, which glows and then slowly fades — this **persistence** creates a visible trace of recent data. Vectorscope simulates this with a decaying accumulator: cells are incremented by incoming pixels and decremented during blanking, so frequently-hit regions glow brightly while rarely-hit regions dim over time. The decay rate is controlled by the Persist knob.

### What Is a Graticule?

A **graticule** is the calibration overlay drawn on top of the vectorscope display — typically a crosshair at the center (representing zero chrominance / neutral gray) and optional circles at standard saturation levels. The crosshair helps identify whether the signal's color balance is centered (neutral white point) or shifted toward a particular hue. Vectorscope draws a crosshair at the midpoint of the 64×64 grid.

### What Is Over Video?

In broadcast monitoring, vectorscopes typically occupy their own dedicated display. Vectorscope's **Over Video** mode overlays the scope display directly on top of the input video at a fixed position, allowing simultaneous monitoring of the picture and its color analysis. When Over Video is disabled, the scope is rendered on a black background.


---

## Signal Flow

Accumulator Engine → Renderer → Output → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Accumulator Engine (Port A) ────────────────────────────────
│   ├─ 1. Quantize U → 6 bits  (upper 6 bits of 10-bit U)
│   ├─ 2. Quantize V → 6 bits  (upper 6 bits of 10-bit V)
│   ├─ 3. Address = {V[5:0], U[5:0]}  (4096 cells)
│   ├─ 4. Read current cell value
│   ├─ 5. Increment (saturate at 255)
│   ├─ 6. Write back
│   └─ 7. Decay sweep (vsync): subtract persistence delta from all cells
│
├── Renderer (Port B) ──────────────────────────────────────────
│   ├─ 1. Scope region: 64×64 pixels at (328, 88)
│   ├─ 2. Read accumulator at (scope_x, scope_y)
│   ├─ 3. Dot brightness = cell_value × Intensity
│   ├─ 4. Apply phosphor color (Green/Amber/Blue/White UV values)
│   ├─ 5. Graticule crosshair at center (32, 32)
│   └─ 6. Over Video: show input outside scope region
│
├── Output ─────────────────────────────────────────────────────
│   ├─ Inside scope: dot Y + phosphor UV
│   ├─ Outside scope: input (Over Video) or black
│   └─ Bypass mux
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through with 4-clock delay
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The dual-port BRAM is the key architectural element. Port A handles both accumulation (during active video) and decay (during vertical blanking) — these are time-multiplexed, never simultaneous. Port B handles the display readout, which occurs continuously during the renderer's active region. The accumulator operates at pixel clock rate: for each input pixel, it reads the cell at [V_quant][U_quant], increments it, and writes back. During the ~30-line vertical blanking interval, a sweep reads and decrements each of the 4096 cells by the persistence-derived delta. The renderer maps the 64×64 scope grid to a fixed screen position and converts cell values to brightness via the Intensity multiplier.

---

## Parameter Reference

<img src={vectorscope_control_panel} alt="Videomancer front panel with Vectorscope loaded"/>
*Videomancer's front panel with Vectorscope active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Intensity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At minimum, even heavily populated cells appear dim. At maximum, a single hit is bright. Higher intensity makes sparse signals visible but can over-expose dense color clusters. This is analogous to the beam intensity control on a CRT vectorscope. Internally, controls the display brightness scaling — the multiplier applied to each cell's accumulated value before rendering as luminance.

---

#### Knob 2 — Persist
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

At minimum, dots fade almost instantly (only the current frame's data is visible). At maximum, dots persist for many frames, building up a bright, slowly evolving trace. Higher persistence reveals the full color range of time-varying content but can obscure transient color events. The decay amount is subtracted from all 4096 cells during each vertical blanking interval. Internally, controls the phosphor persistence — how slowly accumulated dots decay.

---

#### Knob 3 — Gain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for future use (Gain). Currently has no effect on the output. May be connected to an input amplitude pre-scaler in a future revision.

---

#### Knob 4 — Grat Opac
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

At minimum, the crosshair is invisible. At maximum, the crosshair lines are drawn at full brightness. The graticule is rendered only within the scope region and overlays the dot display. Internally, controls the graticule overlay opacity.

---

#### Knob 5 — Hue Shift
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Reserved for future use. Currently has no effect on the output.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC brightness offset to the rendered scope display. At center (50%), no shift. Above center lifts the overall scope brightness; below center darkens it. This is useful for matching the scope visibility against the Over Video background.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Phosphor** | Green | White |
| **8 — Graticule** | Off | On |
| **9 — Over Video** | Off | On |
| **10 — I/Q Mode** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–8 select the phosphor color and graticule visibility. Switch 9 controls Over Video. Two switches (7) are combined for the 4-way phosphor selection. Switches 10–11 are unused and bypass, respectively.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the vectorscope display and the original input via the hardware interpolator. At 100%, the full vectorscope rendering is shown. Lowering the fader blends the vectorscope display with the input.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Vectorscope processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises demonstrate the vectorscope as a color analysis instrument and explore its display options for creative and technical use.

### Exercise 1: Color Bar Analysis

<BeforeAfterSlider
  sources={[
    { label: "Car", before: vectorscope_source1_car, after: vectorscope_ex1_s1 },
    { label: "Boat", before: vectorscope_source2_boat, after: vectorscope_ex1_s2 },
    { label: "Collage", before: vectorscope_source3_collage, after: vectorscope_ex1_s3 },
    { label: "Pattern", before: vectorscope_source4_pattern, after: vectorscope_ex1_s4 },
    { label: "Girl", before: vectorscope_source5_girl, after: vectorscope_ex1_s5 },
    { label: "Paint", before: vectorscope_source6_paint, after: vectorscope_ex1_s6 },
  ]}
/>
*Color Bar Analysis — simulated result across source images.*
**Source**: Color bar test pattern (SMPTE or EBU bars) — the standard calibration signal for vectorscope setup.

**What You'll Create**: Verify that the vectorscope correctly displays the 6 primary/secondary color positions.

1. **Feed bars**: Connect a color bar test pattern generator.
2. **Persistence**: Set Persist to ~40%. Dots accumulate clearly without excessive smearing.
3. **Intensity**: Set Intensity to ~60%. Bright enough to see all bar positions.
4. **Graticule**: Enable Graticule (Switch 8). The center crosshair marks neutral.
5. **Identify dots**: Six clusters of dots should appear at the standard vectorscope positions — corresponding to red, green, blue, cyan, magenta, and yellow.
6. **Center check**: The gray/white portions of the bars should cluster tightly at the center crosshair (neutral chrominance).

**Key concepts**: Color bars produce 6 dot clusters at known UV positions, neutral gray maps to center, scope is a UV scatter plot

---

### Exercise 2: Live Video Color Monitor

<BeforeAfterSlider
  sources={[
    { label: "Car", before: vectorscope_source1_car, after: vectorscope_ex2_s1 },
    { label: "Boat", before: vectorscope_source2_boat, after: vectorscope_ex2_s2 },
    { label: "Collage", before: vectorscope_source3_collage, after: vectorscope_ex2_s3 },
    { label: "Pattern", before: vectorscope_source4_pattern, after: vectorscope_ex2_s4 },
    { label: "Girl", before: vectorscope_source5_girl, after: vectorscope_ex2_s5 },
    { label: "Paint", before: vectorscope_source6_paint, after: vectorscope_ex2_s6 },
  ]}
/>
*Live Video Color Monitor — simulated result across source images.*
**Source**: Camera feed of a colorful scene (flowers, fabrics, art — saturated colors).

**What You'll Create**: Use the vectorscope as a real-time color balance monitor overlaid on the live picture.

1. **Over Video**: Enable Over Video (Switch 9). The scope appears as an overlay window.
2. **Persistence**: Set Persist to ~60%. The trace shows the overall color distribution across several frames.
3. **Color balance**: Observe the dot cloud position. A well-balanced scene clusters around center; a color cast shifts the cloud off-center.
4. **Saturation**: Highly saturated content produces dots far from center. Desaturated content clusters tightly near the middle.
5. **Switch phosphor**: Try Amber (warmer) or Blue (cooler) phosphor — which is most readable against your video content?
6. **Intensity**: Adjust Intensity to keep the scope visible without overwhelming the underlying video.

**Key concepts**: Over Video enables simultaneous content and analysis monitoring, dot cloud position reveals color balance, spread reveals saturation range

---

### Exercise 3: Phosphor Art (Creative Use)

<BeforeAfterSlider
  sources={[
    { label: "Car", before: vectorscope_source1_car, after: vectorscope_ex3_s1 },
    { label: "Boat", before: vectorscope_source2_boat, after: vectorscope_ex3_s2 },
    { label: "Collage", before: vectorscope_source3_collage, after: vectorscope_ex3_s3 },
    { label: "Pattern", before: vectorscope_source4_pattern, after: vectorscope_ex3_s4 },
    { label: "Girl", before: vectorscope_source5_girl, after: vectorscope_ex3_s5 },
    { label: "Paint", before: vectorscope_source6_paint, after: vectorscope_ex3_s6 },
  ]}
/>
*Phosphor Art (Creative Use) — simulated result across source images.*
**Source**: Any dynamic video — music performance, abstract visuals, or oscillating patterns.

**What You'll Create**: Use the vectorscope display itself as a creative visual element rather than a technical instrument.

1. **High persistence**: Set Persist to ~90%. Dots accumulate heavily, creating bright persistent trails.
2. **Maximum intensity**: Set Intensity to 100%. Every dot is bright.
3. **Amber phosphor**: Select Amber for a warm, retro oscilloscope glow.
4. **No Over Video**: Disable Over Video. The display is pure scope-on-black.
5. **Dynamic input**: Feed rapidly changing video. The dot cloud dances and traces out color space trajectories.
6. **Graticule crosshair**: Enable Graticule with high opacity — the crosshair becomes a structural element in the composition.
7. **Adjust brightness**: Use Brightness to lift the scope glow for a dreamy, analog-instrument aesthetic.

**Key concepts**: High persistence + intensity creates a glowing trace art, phosphor colors set the mood, dynamic input produces animated dot clouds, scope as visual element rather than instrument

---


## Tips

- **Graticule identifies shifts**: The crosshair marks neutral — if your dot cloud is consistently off-center, your white balance needs correction.
- **Chain with Whitebal**: Use Vectorscope to monitor color corrections applied by Whitebal — watch the dot cloud shift as you adjust Color Temp and Tint.
- **Low intensity for reading**: When using the scope as a technical tool, moderate intensity prevents over-saturation of the display.
- **Amber for atmosphere**: Amber phosphor evokes vintage analog test equipment — beautiful for retro-futuristic displays.

---

## Glossary

| Term | Definition |
|------|------------|
| **Accumulator** | A dual-port BRAM array that counts how many pixels in the current frame map to each UV quantization cell, building up the scatter-plot density. |
| **Chrominance** | The color information in a YUV signal, represented by U (blue-difference) and V (red-difference) components. |
| **CRT** | Cathode Ray Tube; the display technology used in classic analog vectorscopes, where an electron beam traces dots on a phosphor screen. |
| **Decay Sweep** | A per-frame operation during vertical blanking that subtracts a persistence-derived amount from all accumulator cells, simulating phosphor fade. |
| **Dual-Port BRAM** | Block RAM with two independent access ports, allowing simultaneous read/write operations. Vectorscope uses port A for accumulation and port B for display readout. |
| **Graticule** | The calibration overlay (crosshair) drawn on the vectorscope display to mark the neutral chrominance point and other reference positions. |
| **Phosphor** | The luminescent coating on a CRT screen that glows when struck by an electron beam. Different phosphor compounds produce different colors (P1=green, P43=yellow-green, etc.). |
| **Scatter Plot** | A display showing individual data points as dots in a two-dimensional coordinate space, here U vs V. |
| **Vectorscope** | A specialized oscilloscope display for visualizing the chrominance content of a video signal as a UV scatter plot. |

---
