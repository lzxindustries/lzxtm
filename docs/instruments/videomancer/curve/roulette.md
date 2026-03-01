---
draft: true
sidebar_position: 222
slug: /instruments/videomancer/roulette
title: "Roulette"
image: /img/instruments/videomancer/roulette/roulette_hero.png
description: "A roulette curve is the path traced by a point fixed to a circle as it rolls around the outside or inside of another circle."
---

import roulette_animation from '/img/instruments/videomancer/roulette/roulette_animation.gif';
import roulette_control_panel from '/img/instruments/videomancer/roulette/roulette_control_panel.png';
import roulette_exercise1_result from '/img/instruments/videomancer/roulette/roulette_exercise1_result.gif';
import roulette_exercise2_result from '/img/instruments/videomancer/roulette/roulette_exercise2_result.gif';
import roulette_exercise3_result from '/img/instruments/videomancer/roulette/roulette_exercise3_result.gif';
import roulette_hero from '/img/instruments/videomancer/roulette/roulette_hero.png';

# Roulette

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={roulette_hero} alt="Roulette hero image"/>
*Roulette drawing a multi-lobed epitrochoid curve with DDS-driven phase accumulation and Manhattan-distance line rendering.*
<img src={roulette_animation} alt="Roulette animated output"/>
*Roulette output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

A roulette curve is the path traced by a point fixed to a circle as it rolls around the outside or inside of another circle. When the rolling circle travels outside the fixed circle the result is an *epitrochoid*; when it rolls inside, the result is a *hypotrochoid*. These are the same mathematical figures drawn by the popular Spirograph toy — but here they are rendered in real time on the FPGA's video raster using a direct digital synthesis (DDS) phase accumulator and a quarter-wave sine lookup table.

Roulette generates its imagery entirely from mathematics — no input video is required. The program computes a single moving point on the roulette curve each frame, tests every pixel against that point using Manhattan distance, and lights pixels that fall within the configurable line width. The result is a luminous dot that traces the chosen curve across the screen. With persistence enabled, previous positions accumulate into the classic spirograph figure. With trail fade, older positions gradually dim, creating a comet-like tail.

The name *Roulette* is the formal mathematical term for the family of curves produced by rolling circles — encompassing epitrochoids, hypotrochoids, epicycloids, and hypocycloids as special cases.

---

## Background

### Roulette Geometry

A roulette is defined by three parameters: the radius of the fixed circle (*R*), the radius of the rolling circle (*r*), and the distance from the center of the rolling circle to the drawing point (*d*). When *d = r*, the curve is an epicycloid or hypocycloid (the pen is on the rim). When *d ≠ r*, the curve is an epitrochoid or hypotrochoid (the pen is offset from the rim). The ratio *R/r* determines how many lobes the curve has and whether it closes. Rational ratios produce closed figures; irrational ratios produce curves that never exactly repeat.

### Direct Digital Synthesis

DDS is a technique borrowed from RF engineering for generating precise waveforms from a fixed clock. A phase accumulator adds a tuning word on every clock cycle, and the accumulated phase indexes into a waveform lookup table. Roulette uses a 16-bit phase accumulator whose increment is controlled by the Speed parameter. The upper bits of the accumulator address a 64-entry quarter-wave sine table, from which full sine and cosine values are reconstructed by quadrant mirroring. This produces smooth, continuously-variable frequency with no discontinuities.

### Quarter-Wave Sine Table

Storing a full sine wave would require 256 or more entries to avoid visible stepping. By exploiting the four-fold symmetry of the sine function, only one quarter of the wave (0 to π/2) needs to be stored. The other three quadrants are reconstructed by mirroring and negation. Roulette's 64-entry quarter-wave table provides 256-point effective resolution with 9-bit amplitude (peak value 511), using zero BRAM — the table fits entirely in LUT fabric.

### Manhattan Distance

True Euclidean distance requires a square root, which is expensive in FPGA logic. Manhattan distance — the sum of absolute differences along each axis — is a computationally cheap alternative. It produces diamond-shaped contours rather than circles, but for thin line widths the visual difference is negligible. The comparison `|dx| + |dy| < threshold` requires only subtraction, absolute value, and addition — all single-cycle operations.

### Spirograph History

The Spirograph toy was invented by British engineer Denys Fisher in 1965 and became one of the best-selling drawing toys of all time. The toothed plastic gears constrain the pen to trace mathematically precise roulette curves. Roulette brings this mechanical principle into the electronic video domain, replacing plastic gears with DDS oscillators and ink with luminous pixels.


---

## Signal Flow

```
DDS Phase Accumulator (16-bit)
│
├── Speed register → phase increment per vsync
│
├── Quarter-Wave Sine LUT (64 entries × 9 bits)
│   ├── sin(phase) → curve_x offset
│   └── sin(phase + π/4) → curve_y offset
│
├── Curve Point Calculation
│   ├── curve_x = 640 + sin_value  (center + offset)
│   └── curve_y = 360 + cos_value  (center + offset)
│
├── Per-Pixel Manhattan Distance
│   ├── dx = |pixel_x - curve_x|
│   ├── dy = |pixel_y - curve_y|
│   └── dist = dx + dy
│
├── Line Width Comparison
│   └── on_curve = (dist < line_width_threshold)
│
├── Color Assignment
│   ├── On curve: Y = brightness, U/V = color (mono or RGB mode)
│   └── Off curve: Y = 64 (near black), U/V = 512 (neutral)
│
├── Interpolator (4 clocks) — brightness/mix control
│
└── Bypass Mux
    └── Select processed or pass-through
```

The simplified single-point orbital approach in the current VHDL does not compute a full parametric epitrochoid equation. Instead, the phase accumulator drives a single sine/cosine pair that orbits a point around the screen center. The visual result resembles a spirograph tracing when persistence is conceptually enabled, but the actual VHDL persistence mechanism relies on the frame-to-frame behavior of the interpolator mix stage rather than explicit frame buffer storage. The Manhattan distance test creates diamond-shaped "dots" at each curve position, which at narrow line widths appear circular.

---

## Parameter Reference

<img src={roulette_control_panel} alt="Videomancer front panel with Roulette loaded"/>
*Videomancer's front panel with Roulette active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Radius R
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the outer radius of the roulette curve — the radius of the fixed circle in the geometric model. At 0% the curve collapses to a point at the center of the screen. At 100% the curve's lobes extend to the edges of the active picture. This parameter scales the amplitude of the sine component that drives the horizontal position of the curve point. Combined with Radius r, it determines the ratio R/r which controls lobe count and symmetry.

---

#### Knob 2 — Radius r
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the inner radius — the radius of the rolling circle. The ratio between the outer and inner radii determines the number of lobes in the roulette figure. When R and r are close in value, the curve has few large lobes. When r is much smaller than R, the curve develops many small-amplitude cusps. In the current simplified orbital VHDL, this parameter modulates the offset phase between the sine component driving x and the cosine component driving y.

---

#### Knob 3 — Pen Dist
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

Sets the pen distance — the offset of the drawing point from the center of the rolling circle. When the pen distance matches the inner radius, the curve develops sharp cusps (epicycloid/hypocycloid). When the pen is closer to the center, the lobes become rounded. When the pen extends beyond the rolling circle's rim, the loops self-intersect. This is the parameter most responsible for the visual character of the figure.

---

#### Knob 4 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the speed of curve tracing — the DDS phase accumulator increment applied once per vertical sync pulse. At 0% the curve point is stationary. At moderate settings the dot traces the figure slowly enough to follow. At high settings the dot races around the curve, and with persistence the figure fills in rapidly. The upper 8 bits of the 10-bit register value are used as the increment to the 16-bit accumulator.

---

#### Knob 5 — Line Width
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

Sets the line width used in the Manhattan distance comparison. The top 3 bits of the register select a threshold from 1 to 8 pixels. At narrow widths (1–2), the curve appears as a thin, precise trace. At wide widths (6–8), the curve becomes a broad luminous band. Wider lines are more visible on high-resolution displays but reduce geometric precision — the diamond-shaped Manhattan distance contour becomes apparent at large thresholds.

---

#### Knob 6 — Color
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the chrominance of the curve line. In Mono mode (Toggle 8 off), the curve is drawn as a pure white or gray line with neutral chroma. In RGB mode (Toggle 8 on), this parameter sets the U and V values of the curve — U receives the raw register value while V receives the complement (1023 − value), creating a rotating color palette as the knob sweeps. At 50% the result is near-neutral; extreme positions produce saturated cyan/magenta or yellow/blue tones.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Epi | Hypo |
| **8 — Color** | Mono | RGB |
| **9 — Trail** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches configure the curve type, colorization mode, trail persistence, animation, and bypass. Toggle 7 selects between epitrochoid and hypotrochoid geometry. Toggle 8 chooses monochrome or color rendering. Toggle 9 enables visual persistence of the traced path. Toggle 10 controls whether the DDS accumulator advances each frame. Toggle 11 bypasses all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls the overall brightness of the synthesized output via the interpolator mix stage. At 100% the curve is drawn at full intensity against the dark background. At 0% the output is fully attenuated. Intermediate values dim both the curve and the background proportionally, which can be used to blend the synthesis output with external video when the Bypass is off.

---

## Guided Exercises

These exercises explore Roulette's curve geometry from simple circles through complex multi-lobed spirograph figures to animated color traces.

### Exercise 1: Simple Orbit

<img src={roulette_exercise1_result} alt="Simple Orbit result"/>
*Simple Orbit — simulated result across source images.*
**Objective**: Produce a basic circular orbit to understand the DDS phase accumulator and Manhattan distance rendering.

1. Set Radius R to about 50% for moderate horizontal amplitude.
2. Set Radius r to about 50% to match, producing a circular path.
3. Set Pen Dist to about 50% for a smooth, rounded lobe.
4. Set Speed to about 30% so the dot moves slowly enough to observe.
5. Set Line Width to about 3 to produce a visible but precise dot.
6. Enable Animate (Toggle 10) and observe the dot tracing a rough circle.
7. Toggle Trail (Toggle 9) on and watch the circle fill in over successive frames.

**Key concepts**: The DDS phase accumulator produces a continuously-advancing angle, the quarter-wave sine LUT converts phase to position, Manhattan distance creates diamond-shaped line cross-sections

---

### Exercise 2: Multi-Lobed Spirograph

<img src={roulette_exercise2_result} alt="Multi-Lobed Spirograph result"/>
*Multi-Lobed Spirograph — simulated result across source images.*
**Objective**: Create a classic spirograph figure by adjusting the radius ratio for multiple lobes.

1. Set Radius R to about 70% for a large fixed circle.
2. Set Radius r to about 25% for a small rolling circle — this ratio produces a multi-lobed figure.
3. Set Pen Dist to about 60% to extend the pen beyond the rolling circle's rim, creating self-intersecting loops.
4. Set Speed to about 50% for brisk tracing.
5. Enable Trail mode to accumulate the figure.
6. Switch to Hypo mode (Toggle 7) and observe how the lobes fold inward instead of outward.
7. Enable RGB color (Toggle 8) and sweep the Color knob to tint the figure.

**Key concepts**: The R/r ratio determines lobe count, pen distance controls whether the curve has cusps or loops, epitrochoid vs hypotrochoid changes the direction of lobe folding

---

### Exercise 3: Animated Color Trace

<img src={roulette_exercise3_result} alt="Animated Color Trace result"/>
*Animated Color Trace — simulated result across source images.*
**Objective**: Use high speed, color mode, and trail fade to create an evolving luminous trace that builds and decays.

1. Set Radius R to about 60% and Radius r to about 40% for an asymmetric figure.
2. Set Pen Dist to about 80% for large self-intersecting loops.
3. Set Speed to about 80% for rapid tracing.
4. Set Line Width to about 5 for a bold stroke.
5. Enable RGB mode and set Color to about 20% for a deep blue-violet trace.
6. Enable both Trail and Animate.
7. Slowly sweep the Color knob while the curve traces — the figure shifts hue as new segments are drawn in changing colors.
8. Reduce Brightness to about 50% to create a ghostly, decaying trail effect.

**Key concepts**: Color sweeping during animation creates hue gradients along the curve path, the interpolator mix stage controls trail brightness and decay rate, wide line widths make the Manhattan distance diamond shape visible

---


## Tips

- **Start with Trail on**: Without persistence, Roulette shows only a single moving dot — interesting for probing geometry, but the classic spirograph look requires trail accumulation.
- **Rational ratios produce closed figures**: When the outer and inner radius controls are set to values whose ratio is a simple fraction (e.g., 2:1, 3:2), the curve closes on itself after a finite number of lobes. Irrational ratios produce figures that never exactly repeat.
- **Speed affects density**: Faster tracing fills the figure more quickly but can skip positions if the increment is too large relative to the line width, producing dotted rather than continuous lines.
- **Wide lines reveal Manhattan geometry**: The diamond shape of the Manhattan distance test is visible at line widths above 4. This can be a desirable aesthetic — or you can keep widths narrow for a Euclidean approximation.
- **Color sweep during animation**: Slowly rotating the Color knob while the curve traces in RGB mode paints the figure in a gradient of hues, creating a rainbow spirograph effect.
- **Combine with external video**: Turn Bypass off and set Brightness below 100% to overlay the curve on external video input via the interpolator mix.
- **Use slow speed for teaching**: At Speed ~10%, the dot moves slowly enough to watch the geometry unfold — useful for demonstrating roulette mathematics in educational settings.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator and using the result to index a lookup table. |
| **Epitrochoid** | The curve traced by a point attached to a circle rolling around the outside of a fixed circle. |
| **Hypotrochoid** | The curve traced by a point attached to a circle rolling around the inside of a fixed circle. |
| **Manhattan Distance** | The sum of absolute differences along horizontal and vertical axes; a computationally cheap approximation to Euclidean distance that produces diamond-shaped contours. |
| **Phase Accumulator** | A register that adds a fixed increment on every clock cycle, wrapping at its maximum value to produce a repeating sawtooth phase ramp. |
| **Quarter-Wave Sine LUT** | A lookup table storing only the first quarter (0 to π/2) of the sine function; the remaining three quarters are reconstructed by quadrant mirroring and sign inversion. |
| **Roulette** | The mathematical family of curves generated by rolling one circle on another, including epitrochoids, hypotrochoids, epicycloids, and hypocycloids. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
