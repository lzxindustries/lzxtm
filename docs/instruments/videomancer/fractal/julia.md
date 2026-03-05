---
draft: true
sidebar_position: 154
slug: /instruments/videomancer/julia
title: "Julia"
image: /img/instruments/videomancer/julia/julia_hero.png
description: "In 1918, the French mathematician Gaston Julia explored the behavior of iterated rational functions in the complex plane."
---

import julia_hero from '/img/instruments/videomancer/julia/julia_hero.png';
import julia_animation from '/img/instruments/videomancer/julia/julia_animation.gif';
import julia_control_panel from '/img/instruments/videomancer/julia/julia_control_panel.png';
import julia_exercise1_result from '/img/instruments/videomancer/julia/julia_exercise1_result.gif';
import julia_exercise2_result from '/img/instruments/videomancer/julia/julia_exercise2_result.gif';
import julia_exercise3_result from '/img/instruments/videomancer/julia/julia_exercise3_result.gif';

# Julia

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={julia_hero} alt="Julia hero image"/>
*Julia rendering an intricate fractal boundary in blue-gold palette, the infinite complexity of z²+c made visible at video rate.*
<img src={julia_animation} alt="Julia animated output"/>
*Julia output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1918, the French mathematician Gaston Julia explored the behavior of iterated rational functions in the complex plane. For each point, the question is simple: does the sequence z₀, z₁ = z₀² + c, z₂ = z₁² + c, … remain bounded, or does it escape to infinity? The boundary between bounded and escaping points is infinitely detailed at every scale — a fractal curve whose shape depends entirely on the constant c. Julia renders this boundary in real time on an FPGA-based video pipeline.

The program divides the screen into an 80×45 grid of blocks, maps each block center to a coordinate in the complex plane, and runs the escape-time iteration z² + c for up to 32 iterations per block. The iteration count at escape is stored in BRAM and mapped through a 32-entry color palette to produce the output image. Blocks whose sequences never escape — the interior of the set — are rendered as black. The palette can be cycled to animate the coloring without recomputing the fractal, and the c parameter can auto-orbit in a circle on the complex plane to continuously evolve the fractal shape.

Two modes are available. In Julia mode, c is a user-controlled constant and z₀ is the pixel coordinate — each point on the screen starts from its own position but shares the same c. In Mandelbrot mode, c equals the pixel coordinate and z₀ starts at the origin — each point uses itself as the constant, producing the famous Mandelbrot set with its cardioid and bulbs.

---

## Quick Start

1. **C parameter space is the map**: The Mandelbrot set is a catalog of all Julia sets. Points inside the Mandelbrot set produce connected Julia sets; points outside produce disconnected "dust." The most interesting shapes lie near the Mandelbrot boundary.
2. **Palette cycling is free animation**: Once the fractal is computed, cycling the palette offset creates vivid color flow without any additional computation. Combine with a static Julia shape for performance-ready visuals.
3. **MaxIter trades detail for speed**: Higher iteration counts reveal finer boundary structure but require more computation time per frame. At 32 iterations maximum, the engine comfortably fits within one frame period.

---

## Background

### The Julia Set

For a given complex constant c, the Julia set is the boundary of the set of points z₀ in the complex plane for which the iteration zₙ₊₁ = zₙ² + c remains bounded. Points inside the set (the "filled Julia set") never escape; points outside diverge to infinity. The fractal boundary between these two regions is the Julia set proper — a curve of infinite length and zero area that exhibits self-similarity at all magnifications. Different values of c produce radically different Julia sets: connected and lacy for c values inside the Mandelbrot set, disconnected "Fatou dust" for c values outside it.

### The Mandelbrot Set

While the Julia set holds c fixed and varies z₀, the Mandelbrot set does the opposite: it holds z₀ = 0 and varies c. Each point c in the complex plane is colored according to whether the iteration starting from the origin remains bounded. The resulting figure — the iconic "bug" shape with its cardioid body and circular buds — is a catalog of all possible Julia sets. Points inside the Mandelbrot set produce connected Julia sets; points outside produce disconnected ones. The boundary of the Mandelbrot set is itself fractal, with miniature copies of the whole figure embedded at every scale.

### Escape-Time Algorithm

The practical algorithm for rendering these sets is called the escape-time method. For each point, iterate z² + c and test whether |z|² exceeds a chosen escape radius (here, 4.0). If the magnitude exceeds the radius within the maximum iteration count, the point has escaped — its iteration count at escape determines its color. If it never escapes, it is inside the set and rendered as black. The iteration count creates bands of equal escape time surrounding the set, which the palette maps to a smooth color gradient. Higher maximum iteration counts reveal finer detail near the boundary at the cost of more computation.

### Fixed-Point Arithmetic on FPGA

Floating-point multiplication is expensive in FPGA fabric. Julia uses signed 4.12 fixed-point arithmetic — 16-bit values with 4 integer bits and 12 fractional bits, representing the range approximately −8.0 to +8.0. The z² + c iteration requires three 16×16-bit multiplications per step (a², b², and a×b for the real and imaginary parts). The escape check compares the upper bits of the 32-bit squared magnitude against a fixed threshold. This format provides sufficient precision for the −2 to +2 coordinate range of the classic fractal views while fitting within the iCE40's multiplier and LUT budget.

### Palette Cycling

Once the iteration grid is computed, the visual appearance can be changed instantly by shifting the palette index. Adding an offset to each block's iteration count before the palette lookup rotates the color bands around the fractal boundary without recomputing any iterations. This is a classic demoscene technique that creates the illusion of flowing color even when the underlying fractal shape is static.


---

## Signal Flow

C Real / C Imag → Mandelbrot toggle → AnimC toggle → Display Pipeline → Interpolator

```
Parameter Registers
│
├── C Real / C Imag ─── pot→signed 4.12 ──┐
├── Mandelbrot toggle ───────────────────┐ │
├── AnimC toggle ────────────────────────┤ │
│                                        │ │
│   ┌────────────────────────────────────┘ │
│   │  Iteration Engine (sequential)       │
│   │  ┌──────────────────────────┐        │
│   │  │ For each of 80×45 blocks │        │
│   │  │  Map block → complex     │◄───────┘
│   │  │  z₀, c assignment        │
│   │  │  Iterate z² + c (≤32×)   │
│   │  │  Escape check |z|²>4.0   │
│   │  │  Store iter count → BRAM │
│   │  └──────────────────────────┘
│   │
├── Display Pipeline (per pixel, 4 clk) ──────────────────
│   │
│   ├─ Stage 1: Pixel → block coord → BRAM read address
│   ├─ Stage 2: BRAM read (iteration count)
│   ├─ Stage 3: Palette lookup (color/mono) + cycle offset
│   └─ Stage 4: Inside-set → black; compose output
│
├── Interpolator (4 clk) ────────────────────────────────
│   └─ Wet/dry mix per Y, U, V channel
│
└── Output: bypass mux → data_out
```

The iteration engine and display pipeline operate in parallel. The engine runs sequentially through all 3600 blocks, computing during both active video and blanking periods — at 32 iterations maximum, it needs at most 115,200 clocks out of roughly 1.2 million available per frame at 74.25 MHz. The display pipeline reads results from the previous frame's BRAM, so there is a one-frame latency between parameter changes and visible fractal updates. The palette lookup uses the iteration count plus the PalCycl offset as a 5-bit index into constant arrays, producing YUV triplets directly without any intermediate RGB conversion.

---

## Parameter Reference

<img src={julia_control_panel} alt="Videomancer front panel with Julia loaded"/>
*Videomancer's front panel with Julia active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — C Real
| Property | Value |
|----------|-------|
| Range | -200 – 200 |
| Default | -80 |

Controls the real part of the complex constant c. The 10-bit pot value is mapped linearly from −2.0 to +2.0 in the complex plane. In Julia mode, this directly shapes the fractal — sweeping C Real smoothly morphs the Julia set from connected spirals through dendrites to disconnected dust. In Mandelbrot mode, C Real is ignored because c is determined by the pixel coordinate. The default value places c near the classic "rabbit" Julia set.

---

#### Knob 2 — C Imag
| Property | Value |
|----------|-------|
| Range | -200 – 200 |
| Default | 52 |

Controls the imaginary part of c. Together with C Real, this selects a specific point in the complex plane as the Julia constant. The most visually interesting Julia sets occur near the boundary of the Mandelbrot set — roughly within the ring from |c| ≈ 0.5 to |c| ≈ 1.0. Values deep inside the Mandelbrot set produce simple filled shapes; values well outside produce sparse clouds of disconnected points.

---

#### Knob 3 — Zoom
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Labeled "Zoom" on the panel but not applied in the current VHDL implementation. The register is read and stored but the coordinate mapping uses a fixed −2 to +2 range regardless of this control's value. Turning this knob has no visible effect. It is reserved for a future firmware revision that may implement viewport scaling.

---

#### Knob 4 — MaxIter
| Property | Value |
|----------|-------|
| Range | 4 – 32 |
| Default | 18 |

Controls the maximum iteration depth using 8-step quantization. Higher values reveal finer detail near the fractal boundary — the color bands become thinner and more numerous, and small features that would otherwise be classified as "inside the set" get resolved. Lower values produce coarser, blockier boundaries with fewer color bands. At the minimum setting the fractal is reduced to a few broad colored regions; at maximum the boundary becomes a rich web of fine structure.

---

#### Knob 5 — PalCycl
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Rotates the color palette by adding an offset to the iteration count before the palette lookup. At 0% the palette is unshifted; increasing the value cycles the color bands around the fractal boundary. Because the palette wraps at 32 entries, the cycling is periodic — a full sweep of the knob rotates through the entire palette approximately once. This creates vivid color animation without any change to the underlying fractal geometry.

---

#### Knob 6 — VidBlnd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Labeled "VidBlnd" on the panel but not referenced in the current pipeline. The register is declared and read from the SPI bus but no processing stage uses its value. Turning this knob has no visible effect. It is reserved for a future revision that may blend the fractal output with the input video signal.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mandel** | Julia | Mandlbrt |
| **8 — VidSeed** | Off | On |
| **9 — AnimC** | Manual | Auto |
| **10 — Palette** | Color | Mono |
| **11 — Bypass** | Off | On |

The five toggles control mode selection, animation, and visual style. Mandel and AnimC interact: in AnimC+Julia mode, the c parameter auto-orbits, continuously transforming the Julia set shape. In AnimC+Mandelbrot mode, the auto-orbit has no effect because c is determined per-pixel. Palette selects between the blue-gold color scheme and a monochrome luminance ramp. VidSeed is declared but not referenced in the current VHDL — it has no visible effect.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Julia processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Julia-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from static fractal exploration through palette animation to continuous shape morphing. Each reveals a different aspect of the escape-time algorithm and its visual vocabulary.

### Exercise 1: Exploring Julia Sets

<img src={julia_exercise1_result} alt="Exploring Julia Sets result"/>
*Exploring Julia Sets — simulated result across source images.*
**What You'll Create**: Navigate the c-parameter space to discover different Julia set shapes, learning how C Real and C Imag determine fractal geometry.

1. **Default view**: Start with default settings. A Julia set should appear in blue-gold coloring.
2. **Sweep C Real**: Slowly rotate knob 1 from center to the right. Watch the fractal morph — connected regions break apart, tendrils form and dissolve.
3. **Sweep C Imag**: Return C Real to center. Now sweep knob 2. The fractal rotates and distorts along the imaginary axis.
4. **Find the "rabbit"**: Set C Real to approximately −12% and C Imag to approximately +75%. The classic "Douady rabbit" Julia set should appear — three connected lobes with spiral arms.
5. **Find the "dendrite"**: Set C Real to approximately 0% and C Imag to approximately +100%. A tree-like branching structure appears — the Julia set at c = i.
6. **Increase MaxIter**: Turn knob 4 to maximum. Fine boundary detail emerges that was previously classified as "inside the set."

**Key concepts**: C Real and C Imag select a point in the complex plane, each point produces a unique Julia set, connected sets occur for c inside the Mandelbrot set, increasing iterations reveals finer boundary detail

---

### Exercise 2: Palette Cycling Animation

<img src={julia_exercise2_result} alt="Palette Cycling Animation result"/>
*Palette Cycling Animation — simulated result across source images.*
**What You'll Create**: Create vivid color animation by cycling the palette offset while the fractal shape remains static.

1. **Set an interesting Julia set**: Use the "rabbit" coordinates from Exercise 1 or find another connected shape you like.
2. **Freeze the shape**: Ensure AnimC is Manual so the fractal stays fixed.
3. **Sweep PalCycl**: Slowly rotate knob 5. The color bands shift around the fractal boundary, creating a flowing, psychedelic animation even though the geometry is completely static.
4. **Try monochrome**: Toggle Palette to Mono. The grayscale ramp produces a subtler, more scientific animation as the brightness contours rotate.
5. **Change MaxIter**: Increase iteration depth to create more color bands, then sweep PalCycl again. More bands means a richer cycling animation.
6. **Mix blend**: Pull the Mix fader to about 60% and feed a camera signal to the input. The cycling fractal colors overlay the live video.

**Key concepts**: Palette cycling shifts the color lookup without recomputing the fractal, more iteration bands create richer cycling animation, monochrome and color palettes produce different visual textures

---

### Exercise 3: AnimC Auto-Orbit

<img src={julia_exercise3_result} alt="AnimC Auto-Orbit result"/>
*AnimC Auto-Orbit — simulated result across source images.*
**What You'll Create**: Engage the automatic c-parameter orbit to produce continuously evolving fractal shapes without manual input.

1. **Enable AnimC**: Toggle AnimC to Auto. The Julia set begins to morph on its own as c orbits in the complex plane.
2. **Observe transitions**: Watch the fractal pass through connected and disconnected phases. Some frames show intricate lace; others show scattered points.
3. **Add palette cycling**: Turn PalCycl to about 50%. Now both the shape and the coloring are animated simultaneously.
4. **Switch to Mandelbrot**: Toggle Mandel to Mandlbrt. The display locks to the fixed Mandelbrot set — AnimC has no visible effect because c is determined per pixel, not by the orbit.
5. **Return to Julia**: Toggle back to Julia. The orbit animation resumes.
6. **Try monochrome orbit**: Toggle Palette to Mono. The shape-morphing animation stands out more clearly in grayscale without the distraction of color cycling.

**Key concepts**: AnimC orbits c in a circle on the complex plane, the orbit crosses the Mandelbrot set boundary producing connected/disconnected transitions, AnimC has no effect in Mandelbrot mode because c equals the pixel coordinate

---


## Tips

- **AnimC for hands-free morphing**: The auto-orbit continuously transforms the Julia set shape, crossing between connected and disconnected phases. Ideal for installations or live performance backgrounds.
- **Unused controls are harmless**: Zoom, VidBlnd, and VidSeed are declared but unconnected in the current firmware. Turning these knobs will not cause any visual change or instability.
- **Mix for overlay compositing**: At intermediate Mix values, the fractal is superimposed over the input video as a translucent layer. This is effective for blending mathematical graphics with live camera feeds.
- **Block resolution is intentional**: The 80×45 grid creates a chunky, retro aesthetic. Each "pixel" of the fractal covers a 24×12 screen-pixel block, giving the output a mosaic quality that references early computer graphics.

---

## Glossary

| Term | Definition |
|------|------------|
| **Complex Plane** | A two-dimensional number system where horizontal position represents the real part and vertical position represents the imaginary part of a complex number. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms by incrementing a phase accumulator at a fixed rate. |
| **Escape Radius** | The magnitude threshold (|z|² > 4.0) beyond which a sequence is declared divergent. Choosing 4.0 is sufficient because once |z| > 2, the sequence is guaranteed to escape for the z² + c formula. |
| **Fixed-Point** | A number representation where the binary point is at a fixed position (here, signed 4.12 — 4 integer bits, 12 fractional bits). Provides predictable precision without the hardware cost of floating-point. |
| **Iteration Count** | The number of z² + c steps required for a point to exceed the escape radius. Determines the color assigned to that point. |
| **Julia Set** | The fractal boundary in the complex plane between points whose iteration sequences remain bounded and those that escape, for a fixed constant c. |
| **Mandelbrot Set** | The set of complex constants c for which the iteration z² + c starting from z₀ = 0 remains bounded. Acts as a catalog of all Julia sets. |
| **Palette** | A lookup table mapping iteration counts to YUV color values. Julia uses a 32-entry palette with color and monochrome variants. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
