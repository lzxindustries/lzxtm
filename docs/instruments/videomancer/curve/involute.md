---
draft: true
sidebar_position: 129
slug: /instruments/videomancer/involute
title: "Involute"
image: /img/instruments/videomancer/involute/involute_hero.png
description: "A Spirograph on the kitchen table, a coin rolling around the rim of a plate, a point on a gear tooth tracing its path through space — all of these draw ..."
---

import involute_animation from '/img/instruments/videomancer/involute/involute_animation.gif';
import involute_control_panel from '/img/instruments/videomancer/involute/involute_control_panel.png';
import involute_exercise1_result from '/img/instruments/videomancer/involute/involute_exercise1_result.gif';
import involute_exercise2_result from '/img/instruments/videomancer/involute/involute_exercise2_result.gif';
import involute_exercise3_result from '/img/instruments/videomancer/involute/involute_exercise3_result.gif';
import involute_hero from '/img/instruments/videomancer/involute/involute_hero.png';

# Involute

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={involute_hero} alt="Involute hero image"/>
*Involute tracing a rainbow-hued epicycloid with phosphor persistence, the petals blooming outward like a luminous mathematical flower.*
<img src={involute_animation} alt="Involute animated output"/>
*Involute output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

A Spirograph on the kitchen table, a coin rolling around the rim of a plate, a point on a gear tooth tracing its path through space — all of these draw the same family of curves. Mathematicians call them *roulettes*: the trajectories traced by a point attached to a circle rolling around another circle. When the rolling circle travels the outside, the result is an epicycloid. When it rolls on the inside, a hypocycloid. The shape — the number of petals, cusps, or lobes — depends entirely on the ratio of the two circle radii.

Involute implements a parametric roulette engine using two Direct Digital Synthesis phase accumulators driving a quarter-wave sine lookup table stored in BRAM. During each vertical blanking interval, the DDS computes new curve coordinates and plots them onto a 64×64 pixel canvas with 4-bit phosphor intensity. During active video, the canvas is read out, scaled, and composited with the input signal. The phosphor decay mechanism fades previously drawn points each frame, creating a persistence effect that lets the curve's history remain visible as it evolves. The result is an animated mathematical drawing that builds up over time — a continuously rotating Spirograph rendered in real-time video.

At integer ratios, the curves close into perfect rosettes. At near-integer or irrational ratios (via the Open toggle), the tracing point never quite returns to its starting position, producing dense, slowly-drifting fill patterns. The Offset control shifts the tracing point away from the rolling circle's circumference, transforming petals into loops or elongated cusps. Rainbow mode assigns a rotating hue phase to the drawn trace, coloring the curve as it evolves.

---

## Background

### Roulette Curves and the Spirograph

The Spirograph toy, patented by Denys Fisher in 1965, is a mechanical implementation of roulette geometry. A small gear rolls inside or outside a larger ring, and a pen inserted into one of the gear's holes traces a curve on paper. The shape depends on two integers — the tooth counts of gear and ring — which determine the radius ratio. At simple ratios like 3:1, you get a three-petaled curve; at complex ratios like 13:8, the pattern becomes intricate and dense. Involute computes these curves digitally using the same parametric equations, but with continuous ratio control and real-time animation that a mechanical Spirograph cannot achieve.

### Epicycloids and Hypocycloids

An epicycloid is the curve traced by a point on a circle of radius *r* rolling around the outside of a fixed circle of radius *R*. The parametric equations are: $x = (R+r)\cos t - r\cos((R+r)t/r)$ and $y = (R+r)\sin t - r\sin((R+r)t/r)$. The number of cusps equals *R/r* when that ratio is an integer. A hypocycloid is the inside-rolling variant: $x = (R-r)\cos t + r\cos((R-r)t/r)$ and $y = (R-r)\sin t - r\sin((R-r)t/r)$. At ratio 3, a hypocycloid produces a deltoid (three-cusped curve); at ratio 4, an astroid (four cusps). Involute switches between these two families with a single toggle.

### DDS Phase Accumulators

Direct Digital Synthesis is the standard technique for generating periodic waveforms in digital hardware. A phase accumulator — a binary counter that overflows naturally — increments by a frequency word on every clock cycle. The accumulator's value represents the instantaneous phase angle, which is fed into a waveform lookup table. In Involute, two coupled DDS accumulators run during vertical blanking: the primary accumulates at the animation speed rate, and the secondary accumulates at a rate proportional to the ratio N parameter times the primary frequency. The two phases drive four trigonometric lookups (sin and cos of each) through a quarter-wave sine table stored in BRAM.

### Phosphor Persistence

Early oscilloscopes and radar displays used long-persistence phosphors — coatings that continued to glow after the electron beam moved on. The afterglow allowed the viewer to see the entire trace of a waveform or sweep, not just the instantaneous beam position. Involute emulates this behavior digitally. Each pixel on the 64×64 canvas holds a 4-bit intensity value (0–15). When the curve engine plots a new point, it writes maximum intensity. Once per frame, a decay pass subtracts a programmable amount from every non-zero pixel. High decay rates produce a sharp, transient trace; low decay rates allow the entire curve history to accumulate as a glowing phosphor trail.

### Closed vs. Open Curves

When the ratio R/r is a rational number (an integer, in Involute's quantized domain), the tracing point returns exactly to its starting position after a finite number of revolutions. The curve *closes* — it forms a repeating rosette. When R/r is irrational, the curve never closes; it continues to fill the annular region between its inner and outer radii with an infinitely dense path. Involute's Open toggle adds a fractional offset to the secondary phase accumulator, preventing exact closure and producing open, space-filling patterns that evolve endlessly without repeating.


---

## Signal Flow

```
Vertical Blanking Phase (sequential, not pipelined):
│
├── DDS Phase Accumulators ─────────────────────────────────────
│   ├─ phase_t += freq_primary           (primary DDS)
│   ├─ phase_s = phase_t × (ratio_n+1)  (secondary DDS)
│   └─ [Open mode: phase_s += phase_t/2] (irrational offset)
│
├── Trig Lookups ───────────────────────────────────────────────
│   ├─ cos_t = quarter_wave_cos(phase_t)
│   ├─ sin_t = quarter_wave_sin(phase_t)
│   ├─ cos_s = quarter_wave_cos(phase_s)
│   └─ sin_s = quarter_wave_sin(phase_s)
│
├── Roulette Equations ─────────────────────────────────────────
│   ├─ Epi:  x = sum_rad×cos_t - (r+offset)×cos_s
│   │        y = sum_rad×sin_t - (r+offset)×sin_s
│   └─ Hypo: x = sum_rad×cos_t + (r+offset)×cos_s
│            y = sum_rad×sin_t - (r+offset)×sin_s
│
├── Scale + Center ─────────────────────────────────────────────
│   └─ px,py = (curve_xy >> 7) + 32   → [0,63] canvas coords
│
├── Canvas Plot (thickness-aware) ──────────────────────────────
│   └─ canvas[py][px] = 15   (max brightness, 4-bit)
│
├── Phosphor Decay Pass ────────────────────────────────────────
│   └─ for all pixels: canvas[i] = max(0, canvas[i] - decay_rate)
│
Active Video Phase (8-clock pipeline):
│
├── Clock 1: Input Register + Canvas Address ───────────────────
│   ├─ canvas_x = h_count >> 5
│   └─ canvas_y = v_count >> 4
│
├── Clock 2: Canvas BRAM Read ──────────────────────────────────
│   └─ pixel_val = canvas[canvas_y][canvas_x]
│
├── Clock 3: Brightness Scale ──────────────────────────────────
│   └─ trace_bright = pixel_val << 6   (4-bit → 10-bit)
│
├── Clock 4: Compose ───────────────────────────────────────────
│   ├─ Overlay: Y = clamp(Y_in + trace_bright)
│   │           U,V = [rainbow ? hue_rotate : pass-through]
│   └─ Mask:    Y = Y_in where pixel > 0, else black
│               U,V = pass-through or mid-gray
│
├── Clocks 5–8: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(delayed_input, composed, mix_amount)
│
└── Output: Y, U, V, sync
```

The engine operates in two distinct phases per frame. During vertical blanking, the DDS accumulators advance and the roulette equations compute new X,Y coordinates that are plotted onto the canvas BRAM. The decay pass also runs during blanking, dimming old trace points. During active video, the canvas is read out synchronously with the raster scan — pixel coordinates are divided down to canvas resolution, the 4-bit canvas values are scaled to 10-bit luma, and the result is composited with the delayed input video. The key interaction is between animation speed and decay rate: fast animation with slow decay fills the canvas quickly, creating dense phosphor trails; slow animation with fast decay produces a sharp, sparse trace that fades rapidly.

---

## Parameter Reference

<img src={involute_control_panel} alt="Videomancer front panel with Involute loaded"/>
*Videomancer's front panel with Involute active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Ratio N
| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 5 |

Selects the integer ratio R/r, which determines the number of petals (epicycloid) or cusps (hypocycloid) in the curve. At ratio 1, the epicycloid is a cardioid; at ratio 2, a nephroid with two cusps; at ratio 3, a trefoil. Higher ratios produce more lobes and finer structural detail. Because this control is quantized to 16 steps, each position snaps to a specific curve geometry — there are no intermediate shapes between adjacent ratios.

---

#### Knob 2 — Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the tracing point away from the circumference of the rolling circle. At 0%, the pen is on the circle itself, producing a standard epicycloid or hypocycloid with sharp cusps. As the offset increases, the cusps round out into smooth loops, and the overall curve shape becomes more rounded and flower-like. At extreme values, the loops become so large that they dominate the figure, creating a dense, overlapping petal structure.

---

#### Knob 3 — AnimSpd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the DDS phase increment — how fast the curve is drawn. At minimum, the curve advances very slowly, with individual points appearing one at a time. At higher speeds, the curve sweeps rapidly through its trajectory, filling in the pattern within a few frames. The visual character changes dramatically with speed: slow animation reveals the sequential construction of the curve, while fast animation shows the complete figure as a continuous glow.

---

#### Knob 4 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

Controls the phosphor decay rate — how quickly previously drawn points fade. At 0%, there is no decay, and the canvas accumulates indefinitely, eventually saturating to a uniform glow. At low values, old traces persist for many frames, building up layered history. At high values, only the most recent few frames remain visible, producing a sharp, transient trace that sweeps across the canvas like an oscilloscope beam.

---

#### Knob 5 — Thick
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 2 |

Sets the beam width for canvas plotting, from 1 pixel (fine hairline) to 4 pixels (thick stroke). Thicker lines fill more of the canvas per DDS step, producing bolder, more visible curves at the cost of fine detail. At thickness 4, even low-ratio curves can fill most of the canvas area.

---

#### Knob 6 — Scale
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the display zoom — how much of the screen the curve occupies. At low values, the curve is rendered small in the center of the frame. At high values, it fills the entire raster. Because the canvas resolution is fixed at 64×64, extreme scaling produces a visibly blocky, pixelated rendering — each canvas cell becomes a large rectangular block on screen.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Curve** | Epi | Hypo |
| **8 — Compose** | Overlay | Mask |
| **9 — Color** | Mono | Rainbow |
| **10 — Open** | Closed | Open |
| **11 — Bypass** | Off | On |

The five toggles select independent binary options across the curve engine and compositor. Curve type selects the mathematical family (epicycloid vs. hypocycloid). Compose mode selects how the canvas interacts with the input video (additive overlay vs. keyed mask). Color and Open modify the rendering and mathematical behavior of the trace itself. Bypass disables all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed (curve-composited) signal and the delayed original input. At 0%, only the original signal passes through. At 100%, only the curve composite is visible. Intermediate positions blend the two, allowing partial overlay of the curve pattern onto the source material.

---

## Guided Exercises

These exercises explore the mathematical and visual range of the roulette engine, progressing from simple closed curves to complex animated phosphor compositions.

### Exercise 1: Classic Spirograph Rosettes

<img src={involute_exercise1_result} alt="Classic Spirograph Rosettes result"/>
*Classic Spirograph Rosettes — simulated result across source images.*
**Objective**: Explore how the ratio N control determines curve geometry, comparing epicycloids and hypocycloids at several integer ratios.

1. Set Ratio N to 3 (three petals). Set Decay to ~50% for moderate persistence. Set AnimSpd to ~30%.
2. Watch the three-petaled epicycloid trace itself onto the canvas.
3. Increase Ratio N through 4, 5, 6, 8 — observe how each bump adds one petal.
4. Toggle Curve to Hypo. At ratio 3, the trefoil becomes a deltoid; at ratio 4, an astroid.
5. Return to Epi. Set Ratio N to 8 and slowly increase Offset — watch the sharp cusps round into loops.
6. Toggle Bypass on and off to compare the curve against the input.

**Key concepts**: Integer ratio determines the number of petals/cusps, epicycloids face outward while hypocycloids face inward, offset transforms cusps into loops

---

### Exercise 2: Phosphor Persistence and Animation

<img src={involute_exercise2_result} alt="Phosphor Persistence and Animation result"/>
*Phosphor Persistence and Animation — simulated result across source images.*
**Objective**: Learn how animation speed and decay rate interact to control the density and character of the phosphor trail.

1. Set Ratio N to 5. Set AnimSpd to minimum (~5%). Set Decay to maximum (100%). Observe a sharp, slowly-sweeping trace.
2. Gradually reduce Decay toward 0%. The trail lengthens, revealing the curve's history.
3. At Decay ~20%, increase AnimSpd to ~80%. The curve fills in rapidly, creating a dense glow.
4. Enable Rainbow mode — the evolving trace picks up cycling hue.
5. Set Decay back to ~70% and AnimSpd to ~40% for a balanced, breathing phosphor effect.
6. Toggle Open on — the curve stops closing, gradually filling the annular region.

**Key concepts**: Decay rate controls persistence memory depth, animation speed controls how fast the curve is drawn, the interaction between speed and decay determines visual density

---

### Exercise 3: Mask Mode Compositions

<img src={involute_exercise3_result} alt="Mask Mode Compositions result"/>
*Mask Mode Compositions — simulated result across source images.*
**Objective**: Use the curve as a dynamic window into the input video, creating evolving geometric keys.

1. Set Compose to Mask. Set Ratio N to 4 (four-lobed figure). Set Decay to ~30% for wide persistence.
2. Feed any video source. The curve acts as a window — only regions where the trace has been drawn reveal the source.
3. Increase Thick to 3 or 4 to widen the window area.
4. Set AnimSpd to ~50% and watch the window evolve, revealing different parts of the source over time.
5. Toggle between Epi and Hypo to change the window shape.
6. Switch to Open mode — the never-closing curve gradually opens the entire canvas area.
7. Reduce Mix to ~50% to blend the masked result with the full source.

**Key concepts**: Mask mode uses the canvas as a binary key, thick lines create wider windows, open curves gradually fill the entire mask area

---


## Tips

- **Start simple**: Begin with Ratio N = 3 or 4, Closed mode, Mono color, Overlay compose. Learn the basic curve geometry before adding complexity.
- **Decay is memory**: Think of decay as the depth of the curve's visual memory. Zero decay = infinite memory (full trail). Maximum decay = no memory (beam only).
- **Offset transforms shape**: Small offsets smooth the cusps. Large offsets create loops. The transition is continuous and dramatic.
- **Open mode for density**: When you want the curve to fill space rather than trace a clean rosette, enable Open. The fractional offset prevents repetition.
- **Rainbow reads time**: In Rainbow mode, the hue encodes time — you can see the chronological order in which regions of the curve were drawn.
- **Mask mode for keying**: Use the evolving curve as a dynamic key over another video source. The shape of the window changes with every parameter.
- **Scale reveals resolution**: At high Scale values, the 64×64 canvas grid becomes visible as blocky pixels. This can be an aesthetic choice or a signal to reduce scale.
- **Feedback potential**: Routing the output back to the input creates recursive curve-on-curve structures. The phosphor persistence interacts with itself across feedback iterations.

---

## Glossary

| Term | Definition |
|------|------------|
| **Astroid** | A four-cusped hypocycloid traced when the radius ratio is 4:1; shaped like a four-pointed star. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **Canvas** | The 64×64 pixel framebuffer with 4-bit intensity per pixel, used to store the curve trace and its phosphor history. |
| **Cardioid** | A single-cusped epicycloid traced when the radius ratio is 1:1; heart-shaped. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator and using the result to index a lookup table. |
| **Decay** | The per-frame subtraction applied to all canvas pixels, simulating phosphor fade-out. |
| **Deltoid** | A three-cusped hypocycloid traced when the radius ratio is 3:1. |
| **Epicycloid** | The curve traced by a point on a circle rolling around the outside of a fixed circle. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Hypocycloid** | The curve traced by a point on a circle rolling around the inside of a fixed circle. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **Nephroid** | A two-cusped epicycloid traced when the radius ratio is 2:1; kidney-shaped. |
| **Phosphor** | A material that emits light after excitation; here used metaphorically for the canvas persistence mechanism. |
| **Quarter-wave LUT** | A sine lookup table storing only one quarter-cycle, reconstructing the full waveform via quadrant mirroring. |
| **Roulette** | The family of curves traced by a point on a circle rolling along another circle. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
