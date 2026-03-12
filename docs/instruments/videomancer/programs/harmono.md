---
draft: true
sidebar_position: 134
slug: /instruments/videomancer/harmono
title: "Harmono"
image: /img/instruments/videomancer/harmono/harmono_hero.png
description: "Harmono is a digital harmonograph — a device that draws the compound motion of two perpendicular oscillators as a continuous curve on a persistent canvas."
---

import harmono_hero from '/img/instruments/videomancer/harmono/harmono_hero.png';
import harmono_animation from '/img/instruments/videomancer/harmono/harmono_animation.gif';
import harmono_control_panel from '/img/instruments/videomancer/harmono/harmono_control_panel.png';
import harmono_exercise1_result from '/img/instruments/videomancer/harmono/harmono_exercise1_result.gif';
import harmono_exercise2_result from '/img/instruments/videomancer/harmono/harmono_exercise2_result.gif';
import harmono_exercise3_result from '/img/instruments/videomancer/harmono/harmono_exercise3_result.gif';

# Harmono

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={harmono_hero} alt="Harmono hero image"/>
*A pair of DDS oscillators trace a damped Lissajous curve on a phosphor-green canvas, the figure spiralling inward as harmonics slowly drift against each other.*
<img src={harmono_animation} alt="Harmono animated output"/>
*Harmono output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Harmono is a digital harmonograph — a device that draws the compound motion of two perpendicular oscillators as a continuous curve on a persistent canvas.  Physical harmonographs use pendulums with different frequencies and damping rates; the resulting figures range from simple ellipses (when the frequency ratio is exactly 1:1) to intricate rosette patterns (when the ratio is irrational).  Harmono implements two DDS (direct digital synthesis) oscillators whose outputs drive the X and Y coordinates of a drawing point on a 128×128 pixel BRAM canvas.

The Freq X and Freq Y knobs select the two oscillator frequencies from 16 discrete steps.  When the ratio is simple — 1:1, 2:1, 3:2 — the curve closes quickly and forms a recognisable Lissajous figure.  When the ratio is more complex — 7:5, 11:8 — the curve requires many revolutions to close and fills the canvas with dense tracery.  Detune adds a micro-frequency offset that prevents the figure from perfectly closing, causing it to drift slowly and explore new trajectories over time.

Damping simulates friction.  On each horizontal sync the trace step count decrements a damping counter, gradually reducing the oscillator amplitudes so the curve spirals inward toward the centre before being refreshed.  Beam Width controls the thickness of the drawn trace, and Hue rotates the output colour.  A quarter-wave sine lookup table provides smooth oscillator output without consuming DSP blocks.

---

## Quick Start

1. **Simple ratios first:** Start with 1:1 (circle/ellipse) and progress to 2:3, 3:4, etc. — learn the visual vocabulary of frequency ratios before exploring complex ones.
2. **Detune for life:** Even a tiny Detune value transforms a static figure into a living, breathing animation — essential for performance use.
3. **Fade for oscilloscope feel:** Fade mode with a moderate decay rate recreates the green-phosphor look of a vintage oscilloscope, especially in Mono green.

---

## Background

### Harmonographs and Lissajous Figures

The harmonograph was invented in the mid-19th century as a scientific demonstration instrument.  Two or more pendulums drive a pen in perpendicular directions; the drawn figure reveals the frequency and phase relationship between them.  Jules-Antoine Lissajous formalised the mathematics in 1857, showing that the curve `x = sin(at + δ), y = sin(bt)` with frequency ratio `a:b` and phase offset `δ` produces a family of figures from simple closed loops to space-filling curves.

### Direct Digital Synthesis (DDS)

DDS generates a sine wave by accumulating a phase value at each clock cycle and using it to index a lookup table.  The frequency is determined by the phase increment — larger increments produce higher frequencies.  The 16-step frequency select maps to 16 predefined phase increments, choosing ratios that produce musically or visually interesting Lissajous relationships.

### Quarter-Wave Sine LUT

A full sine period can be reconstructed from a single quarter-wave table by exploiting symmetry.  The top two bits of the phase accumulator select the quadrant; the remaining bits index into the 256-entry quarter-wave table, and the output is conditionally negated and/or mirrored.  This reduces BRAM usage by 75 % compared to a full-wave table.

### Damped Oscillation

Real pendulums lose energy to friction, causing their amplitude to decay exponentially.  Harmono simulates this by multiplying the oscillator amplitudes by a damping factor each hsync cycle.  The trace begins at full amplitude at the canvas edges and spirals inward over time.  After a configurable number of cycles the damping resets and the trace restarts from full amplitude.  The visual effect is a continuously refreshing spiral that emerges, tightens, and vanishes in a rhythmic cycle.

### Phosphor Persistence

The 128×128 canvas retains previous drawing positions with a configurable persistence.  The Trace toggle switches between Persist and Fade modes.  In Persist mode, drawn pixels remain bright indefinitely, building up a dense web of overlapping traces.  In Fade mode, the canvas decays slightly each frame, so only recent trace segments are bright while older ones fade to black — simulating the phosphor afterglow of an oscilloscope CRT.


---

## Signal Flow

```
      ┌──────────────┐    ┌──────────────┐
      │  DDS Osc X   │    │  DDS Osc Y   │
      │  (Freq X +   │    │  (Freq Y +   │
      │   Detune)     │    │   Detune)     │
      └──────┬───────┘    └──────┬───────┘
             │                   │
      ┌──────▼───────┐    ┌──────▼───────┘
      │  Sine LUT    │    │  Sine LUT    │
      │  (quarter-   │    │  (quarter-   │
      │   wave)       │    │   wave)       │
      └──────┬───────┘    └──────┬───────┘
             │                   │
      ┌──────▼───────┐    ┌──────▼───────┐
      │  × Damping   │    │  × Damping   │
      │  amplitude   │    │  amplitude   │
      └──────┬───────┘    └──────┬───────┘
             │                   │
             └────────┬──────────┘
                      │
          ┌───────────▼───────────┐
          │  Draw Point on Canvas │
          │  (128×128 BRAM)       │
          │  with beam width      │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │  Canvas Read + Colour │
          │  (Mono / Rainbow)     │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │    Interpolator Mix   │
          │    (dry / wet fader)  │
          └───────────┬───────────┘
                      │
                   Output Y/U/V
```

The DDS oscillators run at hsync rate — each horizontal sync triggers 256 trace steps, computing the sine LUT output for both X and Y, applying damping, and writing the resulting pixel position to the canvas.  This burst of 256 draw operations per line creates the illusion of a continuous, smoothly evolving curve.  The canvas read path scans out the 128×128 BRAM during active video, upscaling to the output resolution.

The dual oscillator outputs are combined as X and Y coordinates rather than summed as audio signals.  This is the fundamental difference between a harmonograph and an audio mixer: the two signals define a position in 2D space, not a single amplitude.

---

## Parameter Reference

<img src={harmono_control_panel} alt="Videomancer front panel with Harmono loaded"/>
*Videomancer's front panel with Harmono active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Freq X
| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 5 |

Freq X selects the X oscillator frequency from 16 discrete steps.  Each step corresponds to a different phase increment feeding the DDS accumulator.  The steps are chosen to produce musically interesting frequency ratios when paired with Freq Y — unison, octave, fifth, fourth, and progressively more complex intervals.  Changing Freq X alters the horizontal periodicity of the Lissajous figure.

---

#### Knob 2 — Freq Y
| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 7 |

Freq Y selects the Y oscillator frequency using the same 16-step scheme.  The visual complexity depends on the ratio between Freq X and Freq Y: simple ratios (1:1, 2:1) produce closed loops; complex ratios (7:5, 13:8) produce dense, near-filling curves.  Slowly stepping through Freq Y while holding Freq X constant creates a progression of increasingly intricate patterns.

---

#### Knob 3 — Damping
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Damping controls the amplitude decay rate.  At minimum, the oscillators maintain full amplitude and the trace draws a steady figure at the edges of the canvas.  Increasing Damping causes the amplitude to shrink more rapidly, spiralling the trace inward.  At maximum, the figure collapses to the centre within a few cycles and restarts — producing a rapid pulse-like refresh.

---

#### Knob 4 — Detune
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Detune adds a small frequency offset to both oscillators, preventing the Lissajous figure from perfectly closing.  At zero, the figure repeats exactly and appears static.  A small Detune value causes the figure to precess slowly, exploring new phase relationships and tracing out a slowly rotating or breathing pattern.  Larger Detune values accelerate the drift, creating a more dynamic, animated appearance.

---

#### Knob 5 — Beam Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Beam Width controls the thickness of the drawn trace.  At minimum, the trace is a single-pixel-wide line.  Increasing Beam Width draws a thicker dot at each position, producing a bold, ribbon-like curve.  Very wide beams cause adjacent trace segments to overlap, filling in regions of the canvas and converting fine tracery into broad sweeping forms.

---

#### Knob 6 — Hue
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

Hue rotates the output colour of the drawn trace.  In Mono mode this shifts the single-colour trace from green through cyan, blue, magenta, and red.  In Rainbow mode this rotates the baseline of the cycling colour mapping.  Hue offset is applied to the entire canvas uniformly.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Lateral | Rotary |
| **8 — Trace** | Persist | Fade |
| **9 — Color** | Mono | Rainbow |
| **10 — Phase** | Free | Locked |
| **11 — Bypass** | Off | On |

Mode switches between Lateral and Rotary oscillator coupling.  Trace controls the canvas persistence.  Color enables rainbow colouring keyed to trace position.  Phase locks the oscillators together or lets them run free.  Bypass passes the signal through.  The most impactful toggle is Phase: locking the oscillators forces perfectly repeating figures, while free-running phase allows natural drift and evolution.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the wet harmonograph output.  At zero, pure input; at maximum, pure harmonograph canvas.





---

## Guided Exercises

These exercises demonstrate the progression from simple Lissajous loops to complex damped harmonograph patterns, exploring frequency ratios, damping, and colour modes.

### Exercise 1: Classic Lissajous

<img src={harmono_exercise1_result} alt="Classic Lissajous result"/>
*Classic Lissajous — simulated result across source images.*
**What You'll Create**: Draw a clean 2:3 Lissajous figure with no damping or drift.

1. Set Freq X to step 3 and Freq Y to step 5 (approximately 2:3 ratio).
2. Set Damping to 0 % and Detune to 0 % for a static, repeating figure.
3. Select Mono colour, Persist trace, Locked phase.
4. Observe the closed Lissajous figure building up as the trace loops.
5. Step Freq Y up one notch and watch the figure change topology.

**Key concepts**: - Simple frequency ratios produce closed, repeating figures
- Zero Damping and Detune create a static pattern
- Locked phase ensures perfect repetition

---

### Exercise 2: Damped Spiral

<img src={harmono_exercise2_result} alt="Damped Spiral result"/>
*Damped Spiral — simulated result across source images.*
**What You'll Create**: Create a spiralling harmonograph that decays inward and refreshes periodically.

1. Set Freq X to step 4, Freq Y to step 7 for a 4:7 ratio.
2. Set Damping to 60 % for moderate decay.
3. Set Detune to 10 % for slow phase drift.
4. Select Fade trace mode so older segments dim.
5. Watch the figure spiral inward, fade, and restart with a new phase relationship.
6. Increase Damping to see faster collapse; decrease for longer spirals.

**Key concepts**: - Damping simulates pendulum friction, causing amplitude decay
- Detune prevents exact repetition, creating evolving figures
- Fade mode provides temporal depth through phosphor-like afterglow

---

### Exercise 3: Rainbow Rotary Rosette

<img src={harmono_exercise3_result} alt="Rainbow Rotary Rosette result"/>
*Rainbow Rotary Rosette — simulated result across source images.*
**What You'll Create**: Produce a continuously rotating rainbow rosette with rotary coupling.

1. Set Freq X to step 3, Freq Y to step 8 for a complex ratio.
2. Set Damping to 30 %, Detune to 5 %.
3. Switch Mode to Rotary and Color to Rainbow.
4. Watch the rosette rotate continuously with rainbow-striped petals.
5. Increase Beam Width to fill in the petals; decrease for fine tracery.

**Key concepts**: - Rotary mode adds 90° phase offset for continuous rotation
- Rainbow colour cycles along the trace length
- Complex ratios produce multi-petaled rosettes

---


## Tips

- **Thick beam for glow:** High Beam Width combined with Fade mode produces soft, glowing trails reminiscent of long-exposure photography of pendulum light paintings.
- **Rotary for motion graphics:** Rotary mode produces continuously spinning figures that work well as backgrounds or transitions in live video mixing.
- **Phase lock for precision:** When you need exact geometric figures for educational or demonstration purposes, lock the phase to prevent drift.
- **Chain with colouriser:** Feeding Harmono's monochrome output into Colorizer adds false-colour gradients to the figure's luminance.

---
