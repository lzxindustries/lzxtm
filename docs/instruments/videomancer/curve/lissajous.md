---
draft: true
sidebar_position: 175
slug: /instruments/videomancer/lissajous
title: "Lissajous"
image: /img/instruments/videomancer/lissajous/lissajous_hero.png
description: "In 1855, the French physicist Jules Antoine Lissajous aimed a beam of light at a mirror attached to one vibrating tuning fork, then bounced it off a second mirror on another fork vibrating at a different frequency."
---

import lissajous_hero from '/img/instruments/videomancer/lissajous/lissajous_hero.png';
import lissajous_animation from '/img/instruments/videomancer/lissajous/lissajous_animation.gif';
import lissajous_control_panel from '/img/instruments/videomancer/lissajous/lissajous_control_panel.png';
import lissajous_exercise1_result from '/img/instruments/videomancer/lissajous/lissajous_exercise1_result.gif';
import lissajous_exercise2_result from '/img/instruments/videomancer/lissajous/lissajous_exercise2_result.gif';
import lissajous_exercise3_result from '/img/instruments/videomancer/lissajous/lissajous_exercise3_result.gif';

# Lissajous

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lissajous_hero} alt="Lissajous hero image"/>
*Lissajous tracing glowing parametric curves across a dark field, green phosphor dots orbiting in a 3:2 frequency ratio.*
<img src={lissajous_animation} alt="Lissajous animated output"/>
*Lissajous output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1855, the French physicist Jules Antoine Lissajous aimed a beam of light at a mirror attached to one vibrating tuning fork, then bounced it off a second mirror on another fork vibrating at a different frequency. The reflected beam traced luminous curves on a screen — closed loops when the frequencies were in simple ratios (1:1 for a circle, 2:1 for a figure-eight), and slowly rotating open curves when the ratio was irrational. These *Lissajous figures* became a standard tool for visualizing the relationship between two oscillating signals, appearing on every oscilloscope screen for the next century and a half.

This program recreates the phenomenon digitally. Two DDS (Direct Digital Synthesis) phase accumulators generate independent X and Y oscillations using a triangle-wave approximation of a sine function. Four equally-spaced dots trace positions along the parametric curve simultaneously, their screen coordinates computed by evaluating the triangle wave at phase offsets of 0, π/2, π, and 3π/2. At each pixel, the Manhattan distance to the nearest dot is computed; pixels within the trace width threshold are brightened, producing glowing points that sweep along the Lissajous path as the DDS phases advance. A phase offset control shifts the Y oscillator's starting angle, morphing between different curve shapes at the same frequency ratio. Green phosphor mode and soft glow mode emulate the look of a classic analog oscilloscope display.

The result is a living mathematical drawing — a parametric curve rendered in real time at video rate, overlaid on the input video or drawn on a black field. The curve drifts and evolves continuously as the DDS accumulators wrap, creating mesmerizing orbital motion that never exactly repeats unless the frequencies are in a perfect integer ratio.

---

## Quick Start

1. **Rational ratios lock, irrational ratios drift**: When Freq X and Freq Y are in a simple ratio (1:1, 2:1, 3:2), the figure closes into a stable pattern. Slightly detuning produces slow precession — a visual beating effect that creates mesmerizing orbital motion.
2. **Phase offset is the shape morpher**: At any fixed frequency ratio, the phase offset determines whether the curve is collapsed (line), partially open (ellipse), or fully open. The most dramatic shape changes happen near 0 and π.
3. **Trace width controls visual weight**: Small trace widths produce delicate points; large widths produce overlapping diamonds that merge into continuous bands. In glow mode, large widths create luminous halos.

---

## Background

### Jules Antoine Lissajous and Parametric Curves

Jules Antoine Lissajous (1822–1880) did not invent the mathematics of parametric curves — those trace back to Nathaniel Bowditch's work in 1815 — but he developed the optical apparatus that made them visible and popularized their use in acoustic research. The key insight is that any two simple harmonic motions applied to orthogonal axes produce a curve whose shape depends entirely on three parameters: the frequency ratio ($a/b$), the phase difference ($\delta$), and the amplitude ratio. When $a/b$ is rational, the curve closes after a finite number of periods; when irrational, it fills a rectangular region densely without ever closing. The Lissajous figure became the canonical visualization of frequency relationships — musicians, engineers, and physicists all learned to read the ratio from the curve's shape.

### Oscilloscope Display Aesthetics

The cathode-ray oscilloscope rendered Lissajous figures as glowing phosphor traces — bright dots sweeping along the curve, their persistence creating a continuous line on the screen. The characteristic green glow of P1 phosphor, the slight halo around bright points, and the way the trace faded as the beam moved past became an iconic visual language of electronics. This program's green phosphor and glow modes deliberately emulate that aesthetic: the green tint shifts U and V away from neutral to create the characteristic color, while glow mode produces a distance-dependent brightness falloff that simulates the phosphor's radial spread.

### Triangle Wave Approximation of Sine

A true Lissajous figure uses sinusoidal oscillations, but computing $\sin(\theta)$ in FPGA hardware requires either a lookup table (consuming BRAM) or a CORDIC algorithm (consuming many clock cycles). The triangle wave is a computationally cheap alternative: it matches the sine's periodicity, symmetry, and zero crossings exactly, differing only in the curvature of the waveform between peaks. The visual difference is subtle — triangle-wave Lissajous figures have slightly more angular curves than their sinusoidal counterparts, with the most visible deviation near the extremes where the sine rounds off but the triangle maintains a constant slope. This program uses zero BRAMs by accepting this approximation, allocating all its resources to the distance computation and compositing logic.

### Manhattan Distance and Dot Rendering

Each dot is rendered by computing the **Manhattan distance** (also called taxicab or L1 distance) from every pixel to the dot's screen position: $d = |x - x_{\text{dot}}| + |y - y_{\text{dot}}|$. This is cheaper than Euclidean distance (which requires a square root) and produces diamond-shaped dot profiles rather than circular ones. The trace width threshold determines how large each dot appears — pixels with Manhattan distance below the threshold are considered "on the trace" and receive the overlay brightness. In glow mode, the brightness falls off linearly with distance rather than cutting off sharply, producing a softer, more phosphor-like appearance.

### DDS Phase Accumulation at Pixel Rate

Unlike most DDS implementations that accumulate phase at a fixed sample rate, this program advances its phase accumulators *every pixel clock* during active video. This means the X and Y frequencies are spatial frequencies — the number of oscillation cycles per screen width — rather than temporal frequencies. The Lissajous figure is drawn in screen space, recomputed for every frame. Temporal animation arises because the accumulators are *not* reset between frames: the residual phase from the end of one frame carries into the beginning of the next, causing the dot positions to shift slightly each frame and trace out the parametric curve over time.


---

## Signal Flow

Manhattan Distance → Minimum Distance → Threshold → Output Valid

```
Input Video (YUV 4:4:4)
│
├── Parameter Pre-registration (at vsync) ──────────────────────
│   ├─ x_inc = x_freq << 6       (10-bit → 16-bit DDS increment)
│   ├─ y_inc = y_freq << 6
│   ├─ width = trace_width       (Manhattan distance threshold)
│   ├─ bright = brightness       (overlay dot brightness)
│   ├─ phoff = phase_offset << 6 (10-bit → 16-bit Y phase offset)
│   ├─ two_dots = dot_count_sel  (0=4 dots, 1=2 dots only)
│   ├─ color = color_mode        (0=white, 1=green phosphor)
│   └─ glow = glow_mode          (0=hard dot, 1=soft gradient)
│
├── DDS Phase Accumulators (per pixel clock) ───────────────────
│   ├─ phase_x += x_inc          (16-bit wrapping accumulator)
│   └─ phase_y += y_inc
│
├── Dot Position Computation (4 dots) ──────────────────────────
│   ├─ Dot 0: tri(phase_x + 0)     , tri(phase_y + phoff + 0)
│   ├─ Dot 1: tri(phase_x + π/2)   , tri(phase_y + phoff + π/2)
│   ├─ Dot 2: tri(phase_x + π)     , tri(phase_y + phoff + π)
│   └─ Dot 3: tri(phase_x + 3π/2)  , tri(phase_y + phoff + 3π/2)
│   each: screen_x = 960 + amp_x>>1, screen_y = 540 + amp_y>>2
│
├── Stage 1: Manhattan Distance Computation ────────────────────
│   ├─ d[i] = |hpos − dot_x[i]| + |vpos − dot_y[i]|  (i=0..3)
│   └─ (Note: dot 2 has VHDL copy-paste bug in dx else branch)
│
├── Stage 2: Minimum Distance Selection ────────────────────────
│   ├─ 4-dot mode: min(d[0], d[1], d[2], d[3])
│   └─ 2-dot mode: min(d[0], d[1])
│
├── Stage 3: Threshold + Color Composite ───────────────────────
│   ├─ thresh = width >> 4  (upper 6 bits: 0..63 pixels)
│   ├─ min_dist < thresh → on trace:
│   │   ├─ glow=0: overlay_y = brightness (hard dot)
│   │   └─ glow=1: overlay_y = brightness − f(distance) (soft)
│   │   ├─ out_y = clamp(input_y + overlay_y, 0, 1023)
│   │   ├─ color=0: out_u/v = input_u/v  (white overlay)
│   │   └─ color=1: out_u = 448, out_v = 480 (green phosphor)
│   └─ min_dist ≥ thresh → off trace: passthrough input
│
├── Stage 4: Output Valid ──────────────────────────────────────
│
├── Clocks 5–8: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(dry, wet, mix_amount) ×3 channels (4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-stage delay pipeline (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal (bit 4)
```

The critical insight is that the DDS accumulators advance every pixel clock, not every frame. This means the dots' positions change continuously across each frame as well as between frames. Within a single frame, each dot traces a tiny segment of the Lissajous curve — the segment visible at that instant depends on the accumulated phase. Between frames, the residual phase creates the illusion of dots orbiting along the curve. The four dots are spaced at 90° phase intervals (0, π/2, π, 3π/2), distributing them evenly around the parametric path. In 2-dot mode only dots 0 and 1 are considered, reducing visual density while preserving the curve's shape. A known VHDL copy-paste bug in the dot 2 distance calculation assigns `v_dy` to `v_abs_dx` in the else branch, causing dot 2's diamond to be slightly asymmetric — this is replicated faithfully in the simulator.

---

## Parameter Reference

<img src={lissajous_control_panel} alt="Videomancer front panel with Lissajous loaded"/>
*Videomancer's front panel with Lissajous active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Freq X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the X oscillator's DDS frequency increment. The 10-bit register value is left-shifted by 6 to produce a 16-bit increment, giving a range of 0 to 65,472 phase steps per pixel clock. At zero, the X oscillator is frozen and all dots collapse to the vertical center line. As Freq X increases, the dots spread horizontally and begin tracing wider curves. The frequency ratio between X and Y determines the curve's topology: equal frequencies produce ellipses or circles (depending on phase offset), while integer ratios like 2:1 or 3:2 produce the classic Lissajous figures with characteristic loop counts. Sweeping this knob slowly reveals the curve locking into and out of harmonic ratios — a visual analog of musical consonance and dissonance.

---

#### Knob 2 — Freq Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the Y oscillator's DDS frequency increment, behaving identically to Freq X but along the vertical axis. The frequency ratio Freq X : Freq Y is the primary determinant of the Lissajous figure's shape. When both knobs are at the same position, the dots trace an ellipse (or circle with appropriate phase offset). Setting Freq Y to twice Freq X produces a figure-eight. The most visually complex and interesting figures occur at ratios like 3:4 or 5:7 where the curve must complete many loops before closing. Near-rational ratios produce curves that almost close but slowly precess — a visual beating effect analogous to acoustic beats between slightly detuned oscillators.

---

#### Knob 3 — Phase
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the trace width — the Manhattan distance threshold below which a pixel is considered "on the trace." Despite the TOML label "Phase," this register feeds the threshold computation, not a phase offset. The upper 6 bits of the value are used, giving an effective range of 0 to 63 pixels. At zero, the dots are sub-pixel and may be invisible. At moderate values (20–40%), the dots appear as small diamonds visible against the background. At high values, the dots expand into large diamond-shaped regions that can overlap and merge, transforming discrete points into a continuous glowing band tracing the Lissajous path. In glow mode, this parameter also determines the falloff radius of the soft gradient.

---

#### Knob 4 — Trace Br
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At zero, the dots are invisible (no brightness added). At 512, the dots add a moderate highlight that lets the underlying video show through. At 1023, the dots are at maximum brightness, clipping to white on anything but the darkest backgrounds. The brightness is additive — it stacks on top of the input video's luminance rather than replacing it. In glow mode, this value represents the peak brightness at the center of each dot, with the glow falling off toward zero at the trace width boundary. Internally, controls the overlay brightness — the luminance value added to pixels on the trace.

---

#### Knob 5 — Line Thk
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the Y oscillator's phase offset. Despite the TOML label "Line Thk," this register maps to the DDS phase offset added to the Y accumulator before the dot position computation. The 10-bit value is left-shifted by 6 to produce a 16-bit offset spanning the full 0–2π range. At zero, the X and Y oscillators are in phase — a 1:1 frequency ratio produces a diagonal line. At quarter-turn (256), the phase difference is π/2 and the same ratio produces a circle. Sweeping this control morphs the Lissajous figure continuously between its degenerate (line) and fully open (circle/ellipse) forms. The effect is most dramatic at simple frequency ratios where the figure's topology changes visibly with small phase adjustments.

---

#### Knob 6 — Fig Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Listed in the TOML as "Fig Size" but never read by the VHDL. The register value at `registers_in(5)` is not assigned to any signal in the architecture. Moving this knob has no effect on the output. The figure's size is instead determined by the fixed scaling factors in the dot position computation (amplitude >> 1 for X, >> 2 for Y), which map the triangle wave's ±1023 range to approximately ±480 pixels horizontally and ±255 pixels vertically.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Ratio** | 1:1 | 3:4 |
| **8 — Style** | Dot | Fade |
| **9 — Input** | Free | Luma |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control dot count, color mode, glow mode, and bypass. Switches 7 and 8 each have four TOML labels but only 1 bit in the VHDL — only the first two labels are meaningful. Switch 9 ("Input") maps to glow mode, not an input selector. Switch 10 ("Animate") is listed in TOML but the corresponding bit 3 is never read by the VHDL. Bypass is on bit 4 (Switch 11), following the conventional mapping. The fader (reg 7) provides the wet/dry mix.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix via `registers_in(7)`. At 0, the output is entirely the unprocessed input (dry). At 1023, the output is entirely the Lissajous-processed result (wet). Intermediate values linearly interpolate between the two across all three YUV channels simultaneously. This control is functional and correctly mapped — unlike some other programs, the fader register is read and used by this program's VHDL.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from simple frequency-ratio exploration through phase morphing to oscilloscope emulation. Each reveals a different aspect of the parametric curve's geometry and the rendering engine's visual vocabulary.

### Exercise 1: Frequency Ratio Exploration

<img src={lissajous_exercise1_result} alt="Frequency Ratio Exploration result"/>
*Frequency Ratio Exploration — simulated result across source images.*
**What You'll Create**: Discover how the X:Y frequency ratio determines the Lissajous figure's topology.

1. **Set equal frequencies**: Turn both Freq X and Freq Y to ~50%. An ellipse (or circle, depending on phase) should appear.
2. **Moderate trace width**: Set Phase (trace width) to ~30% for visible dots.
3. **Full brightness**: Set Trace Br to ~80%.
4. **Default phase**: Set Line Thk (phase offset) to 0%.
5. **4 dots active**: Set Ratio to the first position.
6. **White overlay**: Set Style to the first position.
7. **Hard dot mode**: Set Input to the first position.
8. **Full mix**: Set Mix to ~100%.
9. **Slowly sweep Freq Y**: While holding Freq X fixed, slowly turn Freq Y. Watch the figure morph from ellipse (1:1) through figure-eight (2:1) through more complex loops (3:2, 5:3) as the ratio changes.
10. **Listen for locks**: Notice how the figure briefly stabilizes at rational ratios and drifts at irrational ones.

**Key concepts**: Frequency ratio is the primary shape determinant, rational ratios produce closed curves, irrational ratios produce open precessing curves

---

### Exercise 2: Phase Morphing

<img src={lissajous_exercise2_result} alt="Phase Morphing result"/>
*Phase Morphing — simulated result across source images.*
**What You'll Create**: Explore how the Y phase offset morphs the Lissajous figure between degenerate (line) and fully open (circle/ellipse) forms.

1. **Lock frequencies**: Set both Freq X and Freq Y to ~50% for a 1:1 ratio.
2. **Start at zero phase**: Set Line Thk (phase offset) to 0%. The figure should appear as a diagonal line.
3. **Slowly increase phase**: Turn Line Thk clockwise. Watch the line open into an ellipse, reach maximum width at ~25% (π/2 phase offset), then close back to a line at ~50% (π), open again at ~75% (3π/2), and close at 100% (2π = 0).
4. **Try with 2:1 ratio**: Set Freq Y to ~100% (double Freq X). The figure-eight morphs through butterfly-like forms as phase changes.
5. **Enable glow**: Set Input to the second position. The dots acquire soft halos that make the phase morphing smoother and more visually appealing.

**Key concepts**: Phase offset determines the openness of the curve at any frequency ratio, π/2 offset maximizes the figure's span, 0 and π collapse it to a line

---

### Exercise 3: Oscilloscope Emulation

<img src={lissajous_exercise3_result} alt="Oscilloscope Emulation result"/>
*Oscilloscope Emulation — simulated result across source images.*
**What You'll Create**: Configure the full oscilloscope aesthetic — green phosphor glow on a dark background with soft-edged dots.

1. **Green phosphor**: Set Style to the second position.
2. **Soft glow**: Set Input to the second position.
3. **High brightness**: Set Trace Br to ~90%.
4. **Wide trace**: Set Phase (trace width) to ~50% for broad, overlapping halos.
5. **2 dots**: Set Ratio to the second position for a cleaner trace.
6. **Interesting ratio**: Set Freq X to ~40%, Freq Y to ~60% for a 2:3 ratio with slow precession.
7. **Add phase offset**: Set Line Thk (phase offset) to ~25% for an open figure.
8. **Darken background**: If input is bright, reduce Mix to ~70% to let the dark background dominate and make the phosphor glow stand out.
9. **Observe**: The green glowing dots orbit along a complex Lissajous path, their soft halos leaving phosphor-like trails in the eye's persistence of vision. The effect should closely resemble a real analog oscilloscope in XY mode.

**Key concepts**: Green phosphor tint shifts chrominance to P1-phosphor green, glow mode creates distance-dependent brightness falloff simulating beam spread, 2-dot mode produces cleaner traces

---


## Tips

- **Green phosphor for oscilloscope aesthetics**: Combine green phosphor mode with glow mode for the closest approximation of a real analog oscilloscope's CRT display. Reduce the input video brightness or use a dark source to let the phosphor glow dominate.
- **2-dot mode for clarity**: When the curve is complex (high frequency ratios), four dots can create visual clutter. Switch to 2-dot mode for cleaner traces where individual dot motion is easier to follow.
- **The figure size is fixed**: Despite the "Fig Size" knob label, the Lissajous figure's size cannot be changed — it is determined by the hardcoded shift factors in the VHDL (>>1 for X, >>2 for Y). The figure spans approximately ±480 pixels horizontally and ±255 pixels vertically, centered at (960, 540).
- **Feedback amplifies the trace**: Route the output back to the input. Each pass adds more brightness to the trace, building up a persistent phosphor-like trail of the curve's history.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bezier** | A parametric curve type distinct from Lissajous; both are evaluated from parameter equations but Bezier curves use polynomial blending rather than trigonometric oscillation. |
| **DDS** | Direct Digital Synthesis; a phase-accumulator technique for generating periodic waveforms, used here to drive the X and Y oscillators at pixel rate. |
| **Lissajous figure** | A parametric curve produced by two perpendicular sinusoidal (or triangle-wave) oscillations: $x = A\sin(at + \delta)$, $y = B\sin(bt)$. |
| **Manhattan distance** | The L1 or taxicab distance metric: $d = |x_1 - x_2| + |y_1 - y_2|$, producing diamond-shaped equidistant contours rather than circular ones. |
| **P1 phosphor** | The green phosphor used in classic oscilloscope CRTs, with medium persistence and a characteristic green-yellow glow. |
| **Phase accumulator** | A register that increments by a fixed value each clock cycle, wrapping at its maximum. Its upper bits represent the instantaneous phase of a periodic waveform. |
| **Triangle wave** | A periodic waveform with linear rise and fall, used as a zero-BRAM approximation of a sine wave in this program's oscillator. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
