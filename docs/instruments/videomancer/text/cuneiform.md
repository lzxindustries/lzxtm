---
draft: true
sidebar_position: 71
slug: /instruments/videomancer/cuneiform
title: "Cuneiform"
image: /img/instruments/videomancer/cuneiform/cuneiform_hero_s1.png
description: "Five thousand years ago, Mesopotamian scribes pressed a reed stylus into wet clay to record the world's first written language."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import cuneiform_control_panel from '/img/instruments/videomancer/cuneiform/cuneiform_control_panel.png';
import cuneiform_source1_house from '/img/instruments/videomancer/cuneiform/cuneiform_source1_house.png';
import cuneiform_source2_dog from '/img/instruments/videomancer/cuneiform/cuneiform_source2_dog.png';
import cuneiform_source3_clouds from '/img/instruments/videomancer/cuneiform/cuneiform_source3_clouds.png';
import cuneiform_source4_pattern from '/img/instruments/videomancer/cuneiform/cuneiform_source4_pattern.png';
import cuneiform_source5_woman from '/img/instruments/videomancer/cuneiform/cuneiform_source5_woman.png';
import cuneiform_source6_berries from '/img/instruments/videomancer/cuneiform/cuneiform_source6_berries.png';
import cuneiform_hero_s1 from '/img/instruments/videomancer/cuneiform/cuneiform_hero_s1.png';
import cuneiform_hero_s2 from '/img/instruments/videomancer/cuneiform/cuneiform_hero_s2.png';
import cuneiform_hero_s3 from '/img/instruments/videomancer/cuneiform/cuneiform_hero_s3.png';
import cuneiform_hero_s4 from '/img/instruments/videomancer/cuneiform/cuneiform_hero_s4.png';
import cuneiform_hero_s5 from '/img/instruments/videomancer/cuneiform/cuneiform_hero_s5.png';
import cuneiform_hero_s6 from '/img/instruments/videomancer/cuneiform/cuneiform_hero_s6.png';
import cuneiform_ex1_s1 from '/img/instruments/videomancer/cuneiform/cuneiform_ex1_s1.png';
import cuneiform_ex1_s2 from '/img/instruments/videomancer/cuneiform/cuneiform_ex1_s2.png';
import cuneiform_ex1_s3 from '/img/instruments/videomancer/cuneiform/cuneiform_ex1_s3.png';
import cuneiform_ex1_s4 from '/img/instruments/videomancer/cuneiform/cuneiform_ex1_s4.png';
import cuneiform_ex1_s5 from '/img/instruments/videomancer/cuneiform/cuneiform_ex1_s5.png';
import cuneiform_ex1_s6 from '/img/instruments/videomancer/cuneiform/cuneiform_ex1_s6.png';
import cuneiform_ex2_s1 from '/img/instruments/videomancer/cuneiform/cuneiform_ex2_s1.png';
import cuneiform_ex2_s2 from '/img/instruments/videomancer/cuneiform/cuneiform_ex2_s2.png';
import cuneiform_ex2_s3 from '/img/instruments/videomancer/cuneiform/cuneiform_ex2_s3.png';
import cuneiform_ex2_s4 from '/img/instruments/videomancer/cuneiform/cuneiform_ex2_s4.png';
import cuneiform_ex2_s5 from '/img/instruments/videomancer/cuneiform/cuneiform_ex2_s5.png';
import cuneiform_ex2_s6 from '/img/instruments/videomancer/cuneiform/cuneiform_ex2_s6.png';
import cuneiform_ex3_s1 from '/img/instruments/videomancer/cuneiform/cuneiform_ex3_s1.png';
import cuneiform_ex3_s2 from '/img/instruments/videomancer/cuneiform/cuneiform_ex3_s2.png';
import cuneiform_ex3_s3 from '/img/instruments/videomancer/cuneiform/cuneiform_ex3_s3.png';
import cuneiform_ex3_s4 from '/img/instruments/videomancer/cuneiform/cuneiform_ex3_s4.png';
import cuneiform_ex3_s5 from '/img/instruments/videomancer/cuneiform/cuneiform_ex3_s5.png';
import cuneiform_ex3_s6 from '/img/instruments/videomancer/cuneiform/cuneiform_ex3_s6.png';

# Cuneiform

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "House", before: cuneiform_source1_house, after: cuneiform_hero_s1 },
    { label: "Dog", before: cuneiform_source2_dog, after: cuneiform_hero_s2 },
    { label: "Clouds", before: cuneiform_source3_clouds, after: cuneiform_hero_s3 },
    { label: "Pattern", before: cuneiform_source4_pattern, after: cuneiform_hero_s4 },
    { label: "Woman", before: cuneiform_source5_woman, after: cuneiform_hero_s5 },
    { label: "Berries", before: cuneiform_source6_berries, after: cuneiform_hero_s6 },
  ]}
/>
*Cuneiform converting luminance gradients into oriented wedge impressions on a simulated clay tablet surface.*

---

## Overview

Five thousand years ago, Mesopotamian scribes pressed a reed stylus into wet clay to record the world's first written language. The marks they made — small, triangular wedge impressions — became known as cuneiform, from the Latin *cuneus* (wedge). Cuneiform takes the principle literally: it divides each frame of video into a grid of cells and replaces every cell with a single oriented wedge mark whose angle follows the dominant luminance gradient and whose size is proportional to the cell's brightness.

Dark regions of the source produce large, heavy impressions that fill the cell. Bright regions produce thin, delicate marks. Pixels outside the mark are rendered in a warm clay surface color with an LFSR grain texture that simulates the rough surface of a dried tablet. The result is a video image re-encoded as if it were pressed into clay — recognizable in structure, but translated into a radically different visual medium.

At small cell sizes the effect is subtle, producing a textured overlay that hints at cuneiform writing. At large cell sizes the image dissolves into a sparse field of oversized wedge impressions whose orientations trace the edge structure of the source. Register separator lines and a tablet edge border complete the illusion of an inscribed artifact.

---

## Quick Start

1. **Start with 8×8 cells**: The default 4×4 grid is dense enough that marks are hard to see individually. Step up to 8×8 or 12×12 for clearly visible wedge impressions before fine-tuning.
2. **Grain sells the surface**: Even a small amount of surface grain (20–30%) dramatically increases the realism of the clay surface effect. The contrast between rough clay and smooth impressions is key.
3. **Fixed mode for texture**: When you want a uniform graphic texture rather than a gradient-responsive rendering, switch to Fixed direction. All marks align the same way, emphasizing tonal variation over spatial structure.

---

## Background

### Cuneiform Writing

Cuneiform is among the oldest known writing systems, emerging in Sumer around 3400 BC and remaining in use for over three millennia. The name refers not to a specific language but to the physical technique: impressing a triangular-tipped reed stylus into soft clay at various angles and depths to produce wedge-shaped marks. The Standard of Ur and the Code of Hammurabi stele — both referenced in the program's VHDL header — are iconic examples of cuneiform inscription on different substrates.

### Stylus Technique and Mark Orientation

A Sumerian scribe controlled three variables with each impression: the angle of the stylus relative to the tablet surface, the rotation of the stylus around its long axis, and the pressure applied. These three variables produced marks of different orientations and sizes. Cuneiform digitizes this process — the cell's luminance gradient determines the rotation (angle), and the cell's brightness determines the depth (size). The four cardinal orientations in the program (rightward, downward, leftward, upward) correspond to the principal stylus positions used in Old Babylonian script.

### Tessellation and Gradient Encoding

The program divides the frame into a regular rectangular grid — a tessellation. Each cell in the tessellation becomes a single glyph whose properties encode local image statistics. This is conceptually similar to how halftone printing encodes grayscale information in dot sizes, but with the added dimension of angle. The gradient direction within each cell determines which way the wedge points, creating a field of oriented marks that collectively trace the edge structure of the source image.

### Clay Surface Simulation

The warm, matte background on which marks appear is modeled after unfired river clay — the medium of historical cuneiform tablets. The LFSR pseudo-random noise generator adds surface grain, simulating the irregularities of hand-shaped clay. The clay tint control rotates the hue of this surface, shifting it from its default warm ochre toward cooler or warmer tones.


---

## Signal Flow

Cell Sampling → Gradient + Wedge Size → Triangle Inside Test → Clay Surface Render

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   └─ h_count, v_count from hsync/vsync
│
├── Cell Coordinate Logic ──────────────────────────────────────
│   ├─ cell_x, cell_y     (grid position)
│   ├─ in_cell_x, in_cell_y  (position within cell)
│   └─ sample_now          (trigger at cell center)
│
├── LFSR ───────────────────────────────────────────────────────
│   └─ 16-bit linear feedback shift register for grain noise
│
├── Stage 1: Cell Sampling ─────────────────────────────────────
│   ├─ Sample-and-hold Y at cell center
│   ├─ Store previous cell Y for gradient estimation
│   └─ Pipeline cell coordinates forward
│
├── Stage 2: Gradient + Wedge Size ─────────────────────────────
│   ├─ Horizontal gradient: |current_cell_Y − prev_cell_Y|
│   ├─ Orientation: 4 directions from gradient comparison
│   │   (fixed_dir → all wedges point right)
│   └─ Wedge size: (1023 − luma) × impression / 1024
│       (invert toggle reverses dark/bright relationship)
│
├── Stage 3: Triangle Inside Test ──────────────────────────────
│   ├─ Wedge mode: triangular taper test per orientation
│   └─ Bar mode: rectangular mark test per orientation
│
├── Stage 4: Clay Surface Render ───────────────────────────────
│   ├─ Impression pixels → dark shadow color (Y=140)
│   ├─ Surface pixels → clay color (Y=640) + LFSR grain
│   ├─ Register separator lines (horizontal bands)
│   └─ Tablet edge border (12px darkened rim)
│
├── Interpolator Stage (4 clocks) ──────────────────────────────
│   └─ Wet/dry mix: lerp(dry, wet, mix_amount) per Y, U, V
│
├── Sync Delay Pipeline ────────────────────────────────────────
│   └─ 8-clock shift register for hsync, vsync, field, data
│
└── Output ─────────────────────────────────────────────────────
    └─ Bypass mux: processed or passthrough
```

The program uses zero BRAM — all processing is purely combinational per-pixel coordinate math with a sample-and-hold latch. Because there is no line buffer, vertical gradient estimation is simplified to zero; the orientation is driven entirely by horizontal gradient differences between adjacent cells. This means wedge orientations tend to track vertical edges in the source (where horizontal luminance change is greatest) more strongly than horizontal edges.

The contrast and clay tint parameters modulate the range and hue of the rendered surface respectively, while the impression depth and LFSR grain control the visual weight and texture of the marks. Register lines and the tablet edge sit in the final render stage, overriding the clay/impression color at specific screen coordinates.

---

## Parameter Reference

<img src={cuneiform_control_panel} alt="Videomancer front panel with Cuneiform loaded"/>
*Videomancer's front panel with Cuneiform active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 1 |

Selects the cell grid resolution from four sizes: 4×4, 8×8, 12×12, or 16×16 pixels. At the smallest size, the grid is dense and the wedge marks are tiny — the image retains significant detail through sheer spatial density. At the largest size, each cell covers 16×16 pixels and the wedge marks become prominent sculptural elements. The cell size also determines the granularity of gradient estimation: larger cells sample luminance over a wider area, smoothing the orientation field.

---

#### Knob 2 — Impress Dep
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At zero, all marks vanish — the entire frame becomes unmarked clay surface. At maximum, wedge marks fill their cells completely, leaving almost no clay visible. The impression depth interacts with cell luminance: the per-cell brightness sets the baseline wedge size, and this control scales that baseline. Increasing depth on a high-contrast source produces a dramatic range from hairline strokes in bright areas to solid filled cells in shadows. Internally, controls the depth of each wedge impression by scaling the wedge's half-width within its cell.

---

#### Knob 3 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At lower values, the difference between light and dark cells is compressed — all wedges appear similar in size. At higher values, the full dynamic range of the source is exploited, producing a wider variation between thin bright-area marks and heavy dark-area impressions. Internally, adjusts the overall contrast of the rendered output by modulating the luminance range used for wedge size calculation.

---

#### Knob 4 — Surf Grain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

At zero, the clay is perfectly smooth and uniform. As you increase the control, the surface develops an increasingly rough, granular texture that simulates the natural irregularities of hand-shaped clay. The grain is applied only to non-impression pixels — the wedge marks themselves remain smooth, creating a visual contrast between the polished impression and the rough surrounding surface. Internally, controls the intensity of the LFSR pseudo-random grain texture applied to the clay surface.

---

#### Knob 5 — Clay Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Rotates the hue of the clay surface color through 360 degrees. At its default position the surface is a warm ochre — the color of river clay dried in the Mesopotamian sun. Rotating the control shifts the tint through amber, sienna, terra cotta, olive, and slate tones. This affects only the U and V components of the clay and impression colors, leaving the luminance relationship between mark and surface unchanged.

---

#### Knob 6 — Registers
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

Adds horizontal register separator lines across the tablet surface. Cuneiform tablets were divided into horizontal bands called registers — each register contained a row of text. This control selects between zero, three, four, or five register dividers. The dividers are rendered as thin dark lines that override both clay surface and wedge impression pixels. When combined with the tablet edge border, the register lines complete the illusion of a sectioned clay tablet.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Direction** | Gradient | Fixed |
| **8 — Mark Style** | Wedge | Bar |
| **9 — Invert** | Off | On |
| **10 — Tablet Edge** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the rendering mode and output routing. Direction and Mark Style define the geometric properties of each wedge mark. Invert reverses the luminance-to-size mapping. Tablet Edge adds a decorative border. Bypass routes the signal around all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the original (dry) video signal and the cuneiform-rendered (wet) signal. At 0% the output is pure dry — the original video. At 100% the output is pure wet — fully rendered clay tablet. Intermediate values blend the two, allowing the cuneiform texture to float as a semi-transparent overlay on the source. This is particularly effective at low mix values where the wedge marks appear as subtle textural annotations on an otherwise normal image.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Cuneiform processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from basic grid rendering to full tablet composition. Each introduces a new aspect of the cuneiform effect.

### Exercise 1: Reed Impressions

<BeforeAfterSlider
  sources={[
    { label: "House", before: cuneiform_source1_house, after: cuneiform_ex1_s1 },
    { label: "Dog", before: cuneiform_source2_dog, after: cuneiform_ex1_s2 },
    { label: "Clouds", before: cuneiform_source3_clouds, after: cuneiform_ex1_s3 },
    { label: "Pattern", before: cuneiform_source4_pattern, after: cuneiform_ex1_s4 },
    { label: "Woman", before: cuneiform_source5_woman, after: cuneiform_ex1_s5 },
    { label: "Berries", before: cuneiform_source6_berries, after: cuneiform_ex1_s6 },
  ]}
/>
*Reed Impressions — simulated result across source images.*
**Source**: A portrait or figure with strong tonal contrast — face, hands, or a figure against a background.

**What You'll Create**: Learn how cell size and impression depth interact to create wedge-mark density and weight.

1. **Large grid**: Set Cell Size to step 3 (16×16). The image dissolves into a sparse field of large wedge marks.
2. **Impression depth**: Sweep Impress Dep from 0 to 100%. Watch marks grow from invisible to cell-filling.
3. **Reduce grid**: Step Cell Size down to 2 (12×12), then 1 (8×8), then 0 (4×4). At each step, the image becomes more legible as the mark density increases.
4. **Grain**: Add surface texture — increase Surf Grain to about 60%.
5. **Register lines**: Set Registers to step 2 (4 dividers). Horizontal bands appear across the tablet.

**Key concepts**: Cell size determines spatial resolution, impression depth determines mark weight, grain adds physical surface texture, register lines divide the tablet into sections

---

### Exercise 2: Gradient Tracing

<BeforeAfterSlider
  sources={[
    { label: "House", before: cuneiform_source1_house, after: cuneiform_ex2_s1 },
    { label: "Dog", before: cuneiform_source2_dog, after: cuneiform_ex2_s2 },
    { label: "Clouds", before: cuneiform_source3_clouds, after: cuneiform_ex2_s3 },
    { label: "Pattern", before: cuneiform_source4_pattern, after: cuneiform_ex2_s4 },
    { label: "Woman", before: cuneiform_source5_woman, after: cuneiform_ex2_s5 },
    { label: "Berries", before: cuneiform_source6_berries, after: cuneiform_ex2_s6 },
  ]}
/>
*Gradient Tracing — simulated result across source images.*
**Source**: Footage with strong directional edges — architecture, geometric patterns, or diagonal lines.

**What You'll Create**: Explore how gradient-driven wedge orientation traces edge structure in the source.

1. **Prepare**: Set Cell Size to step 1 (8×8), Impress Dep to ~60%, Contrast to ~50%.
2. **Observe orientations**: Look at how wedge marks point in different directions across the frame. Near vertical edges, marks point horizontally. In uniform areas, marks follow diagonal patterns based on cell position.
3. **Fixed vs Gradient**: Toggle Direction to Fixed. All marks snap to horizontal orientation. Toggle back to Gradient — the orientation field returns.
4. **Bar mode**: Switch Mark Style to Bar. The triangular wedges become rectangular strokes, clarifying the orientation pattern.
5. **Tablet frame**: Enable Tablet Edge. The darkened border frames the image like an archaeological photograph.

**Key concepts**: Gradient mode encodes local edge direction in mark orientation, fixed mode removes directional information, bar mode simplifies the mark geometry, tablet edge adds artifact framing

---

### Exercise 3: Ancient Artifact

<BeforeAfterSlider
  sources={[
    { label: "House", before: cuneiform_source1_house, after: cuneiform_ex3_s1 },
    { label: "Dog", before: cuneiform_source2_dog, after: cuneiform_ex3_s2 },
    { label: "Clouds", before: cuneiform_source3_clouds, after: cuneiform_ex3_s3 },
    { label: "Pattern", before: cuneiform_source4_pattern, after: cuneiform_ex3_s4 },
    { label: "Woman", before: cuneiform_source5_woman, after: cuneiform_ex3_s5 },
    { label: "Berries", before: cuneiform_source6_berries, after: cuneiform_ex3_s6 },
  ]}
/>
*Ancient Artifact — simulated result across source images.*
**Source**: A slowly moving camera feed or nature footage with organic textures — water, foliage, or clouds.

**What You'll Create**: Combine all parameters to create a convincing clay tablet artifact from live video.

1. **Base**: Cell Size step 2 (12×12), Impress Dep ~80%, Contrast ~60%.
2. **Surface**: Set Surf Grain to ~70% for heavy clay texture. Rotate Clay Tint to ~45° for a warm amber tone.
3. **Structure**: Enable Tablet Edge. Add 3 register lines (Registers step 1).
4. **Invert**: Toggle Invert to see how the tonal mapping reverses — formerly dark shadows become unmarked clay.
5. **Mix blend**: Lower Mix to ~60%. The original video shows through the clay surface, creating a palimpsest effect where the source and the inscription coexist.
6. **Animate**: Let the live video run. The wedge orientations track moving edges in real time, creating a continuously evolving inscription.

**Key concepts**: Clay tint shifts the surface hue, invert reverses the luminance-to-size mapping, partial mix creates a palimpsest blend, live video produces continuously evolving inscription patterns

---


## Tips

- **Mix for overlay**: At 30–50% mix, the cuneiform marks appear as a translucent annotation layer over the original video — useful for creating a palimpsest or archaeological overlay aesthetic.
- **Register lines for composition**: The horizontal dividers create natural reading bands. Use 3 or 4 for a classic Sumerian tablet layout.
- **Feedback loops**: Route the output back to the input for recursive inscription — wedge marks are re-tessellated and re-impressed, creating increasingly abstract geometric structures.
- **Tablet Edge for framing**: Enable the border when presenting the effect as a standalone artifact rather than a full-screen texture.
- **Bar mode for boldness**: Switch to Bar style for a heavier, more graphic mark that reads clearly even at small cell sizes.

---

## Glossary

| Term | Definition |
|------|------------|
| **Cell** | A rectangular region of the pixel grid; each cell is replaced by a single oriented mark. |
| **Cuneiform** | From Latin *cuneus* (wedge); the oldest known writing system, produced by pressing a reed stylus into wet clay. |
| **Gradient** | The rate of change of luminance between adjacent cells; used to determine wedge orientation. |
| **Impression** | The wedge or bar mark rendered within each cell, simulating a stylus pressed into clay. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used to produce surface grain noise. |
| **Register** | In cuneiform scholarship, a horizontal band or section of a clay tablet containing a row of text; replicated here as separator lines. |
| **Sample-and-Hold** | A circuit that captures an input value at a specific moment and holds it constant until the next sample trigger. |
| **Stylus** | The reed writing implement used to make cuneiform impressions; the tip was typically triangular in cross-section. |
| **Tablet** | The clay slab on which cuneiform was inscribed; simulated here by the warm-toned background surface. |
| **Tessellation** | Dividing a plane into non-overlapping regular shapes (here, rectangles) that cover the entire surface. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
