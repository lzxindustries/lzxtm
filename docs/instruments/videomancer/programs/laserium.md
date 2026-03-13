---
draft: true
sidebar_position: 165
slug: /instruments/videomancer/laserium
title: "Laserium"
image: /img/instruments/videomancer/laserium/laserium_hero.png
description: "Laserium recreates the experience of Ivan Dryer's pioneering laser light shows at Los Angeles' Griffith Observatory, which began in 1973 and ran for over 30 years."
---

import laserium_hero from '/img/instruments/videomancer/laserium/laserium_hero.png';
import laserium_animation from '/img/instruments/videomancer/laserium/laserium_animation.gif';
import laserium_control_panel from '/img/instruments/videomancer/laserium/laserium_control_panel.png';
import laserium_exercise1_result from '/img/instruments/videomancer/laserium/laserium_exercise1_result.gif';
import laserium_exercise2_result from '/img/instruments/videomancer/laserium/laserium_exercise2_result.gif';
import laserium_exercise3_result from '/img/instruments/videomancer/laserium/laserium_exercise3_result.gif';

# Laserium

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<img src={laserium_hero} alt="Laserium hero image"/>
*Razor-thin beams of saturated laser light trace rosettes and spirals across a darkened canvas, leaving persistent phosphor trails that glow and decay.*
<img src={laserium_animation} alt="Laserium animated output"/>
*Laserium output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Laserium recreates the experience of Ivan Dryer's pioneering laser light shows at Los Angeles' Griffith Observatory, which began in 1973 and ran for over 30 years. Dryer used argon and krypton gas lasers steered by galvanometer-driven mirrors to trace geometric patterns — rosettes, spirals, Lissajous figures — on the observatory's hemispherical dome. The resulting imagery featured razor-thin lines of intense saturated colour with long persistence from the phosphor-coated projection surface.

This implementation uses a 128×128 BRAM canvas with 8-bit intensity per pixel. Three DDS oscillators drive beam X/Y position through eight selectable pattern algorithms — rosette, spiral, radial burst, cone, figure-8, star, folded, and chaos. The canvas decays each frame according to the Persist control, simulating phosphor burn-in and afterglow. Beam splitting creates a second trace at 180° phase offset. Thick mode writes neighbouring pixels for wider beams. Blanking alternates rendering on even/odd frames for a flickering scan effect.

The combination of continuous beam tracing during active video and per-frame decay creates the characteristic aesthetic of the laser light show: bright leading edges that soften into glowing trails, sharp geometric structure dissolving into diffuse luminous remnants.

---

## Quick Start

1. **Pattern 1 is iconic**: The rosette is the single most recognisable laser show pattern. Start here to calibrate your visual expectations.
2. **High Persist for ambient**: Persist above 80% causes patterns to accumulate into dense luminous fields suitable for ambient background projection.
3. **Low Speed reveals structure**: At very low speed you can watch the beam trace individual points, revealing the mathematical structure of each pattern.

---

## Background

### Ivan Dryer and Laserium

Ivan Dryer founded Laser Images Inc. in 1973 and debuted the first Laserium show at Griffith Observatory that same year. Unlike earlier laser displays that projected static interference patterns, Laserium used galvanometer mirrors to steer a laser beam in real time, creating dynamic geometric figures synchronised to music. The shows ran continuously for over 30 years at Griffith and toured planetariums worldwide. The visual vocabulary of Laserium — rosettes, spirals, expanding bursts, figure-eight patterns — became the defining aesthetic of an entire era of light entertainment.

### Galvanometer Mirror Scanning

A galvanometer is a small motor that can deflect a mirror rapidly through a limited angular range. By mounting two galvanometers at right angles (one for X, one for Y deflection), a laser beam can be steered to any point on a projection surface. The X and Y mirrors are driven by independent waveform generators — when fed sine waves at different frequencies, they trace Lissajous figures; when one is a ramp, the beam scans linearly. The speed of the galvanometers limits the trace rate, creating the characteristic "beam tracing" quality where you can see the point of light moving along its path.

### Phosphor Persistence

When a laser strikes a phosphor-coated dome surface, the illuminated point continues to glow after the beam moves on. This persistence creates visible trails behind the moving beam — the faster the beam moves, the longer and fainter the trail. Laserium's persistence parameter simulates this by decaying the canvas at a controllable rate: high persistence means slow decay (long glowing trails), low persistence means rapid decay (sharp dots with minimal trail).

### Pattern Geometry

The eight pattern types encode different Lissajous frequency ratios and oscillator combinations:
- **Rosette**: sin(a·t) vs sin(b·t) with near-integer ratios — produces multi-petalled flower patterns.
- **Spiral**: Lissajous with expanding amplitude — the beam traces an outward-growing curve.
- **Radial burst**: Two oscillators summed on the angular dimension — creates starburst effects.
- **Cone**: Circular motion (sine vs cosine) — traces a simple ellipse.
- **Figure-8**: sin(t) vs sin(2t) — the classic two-lobed curve.
- **Star**: Phase-folded rosette — creates pointed star shapes.
- **Folded**: sin(3t) vs sin(2t) — creates a 3:2 Lissajous with crossing loops.
- **Chaos**: Phase XOR between oscillators — creates unpredictable, aperiodic traces.

### Beam Splitting

In physical Laserium shows, beam splitters (partially reflective mirrors) could divide a single laser into multiple beams that traced the same pattern at different positions. This implementation generates a second beam by adding 128 (180°) to the oscillator phases, producing a mirror-symmetric trace that doubles the visual density.


---

## Signal Flow

```
  ┌──────────────────────────────────────────────┐
  │  DDS Oscillators (phase_a, phase_b, phase_c) │
  │  Advance per active pixel clock               │
  │  + per-frame vsync increment                  │
  └───────────────────┬──────────────────────────┘
                      │
  ┌───────────────────▼──────────────────────────┐
  │  Pattern Select (8 types from Pot 1)         │
  │  → beam X,Y from oscillator phases           │
  │  × Spread (amplitude scaling)                │
  │  → canvas address (bx, by) centred at 64,64  │
  └───────────────────┬──────────────────────────┘
                      │
  ┌───────────────────▼──────────────────────────┐
  │  Canvas Write: saturating add +55 at address  │
  │  Thick mode: +40 to right and below neighbors │
  │  Split mode: second beam at +128° phase       │
  │  Blanking: skip odd frames                    │
  └───────────────────┬──────────────────────────┘
                      │
  ┌───────────────────▼──────────────────────────┐
  │  Canvas Decay (during vblank)                 │
  │  Each pixel: val = max(val - decay_amt, 0)    │
  │  decay_amt = persist(9:2) clamped ≥ 1         │
  └───────────────────┬──────────────────────────┘
                      │
  ┌───────────────────▼──────────────────────────┐
  │  Canvas Readout: nearest-neighbour upscale    │
  │  8-bit pixel → 10-bit luminance               │
  │  Beam Width threshold (thin mode)             │
  │  Colour: sine_lookup(hue) → U/V              │
  │  Multi: hue varies with pixel intensity       │
  │  Suppress chroma when dark (< 32)             │
  └───────────────────┬──────────────────────────┘
                      │
  ┌───────────────────▼──────┐    ┌──────────┐
  │ wet Y/U/V                ├───►│ Interp   ├──► data_out
  └──────────────────────────┘    │ (dry/wet) │
                                  └──────────┘
```

Beam tracing and canvas decay are separated into different phases: decay runs during vertical blanking (scanning the full 16384-pixel canvas sequentially), while beam tracing runs during active video (using pixel clocks as trace steps). This means the beam traces ~1280 points per scanline during active video, accumulating intensity at each position. The oscillator phases advance continuously during active video, so the beam position evolves within each frame — producing long, continuous traces rather than isolated dots.

The canvas readout uses nearest-neighbour scaling from 128×128 to screen resolution, which gives the output a deliberately blocky, low-resolution quality appropriate to the aesthetic. The Beam Width control acts as a luminance threshold during readout: in thin mode, only pixels above the threshold are displayed, making the beam appear narrower by suppressing dim trail remnants.

---

## Parameter Reference

<img src={laserium_control_panel} alt="Videomancer front panel with Laserium loaded"/>
*Videomancer's front panel with Laserium active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Pattern
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 1 |

Pattern selects one of eight geometric patterns via a steps_8 control mode that maps the 10-bit knob range to 8 discrete states. The patterns progress from simple closed curves (rosette, cone) through classic Lissajous figures (figure-8, star) to complex multi-oscillator combinations (folded, chaos). Each pattern has a distinctive visual character determined by the oscillator frequency ratios and phase relationships used to compute beam X/Y.

---

#### Knob 2 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Speed controls the oscillator phase increment per pixel clock and per frame. Higher values cause the beam to trace faster, covering more of the pattern in each frame. At low speed, individual dots are visible and the beam position evolves slowly between frames. At high speed, the beam covers dense portions of the pattern each frame, rapidly filling the canvas with intersecting traces.

---

#### Knob 3 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Spread scales the amplitude of the oscillator outputs before mapping to canvas coordinates. At minimum the beam traces a tiny pattern near the canvas centre. At maximum the pattern fills the full 128×128 canvas. Because the canvas uses 7-bit coordinates centred at (64, 64), very large spreads can cause the beam to clip at the canvas edges.

---

#### Knob 4 — Beam Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Beam Width acts as a luminance threshold during canvas readout. In Thin mode, pixels below this threshold are suppressed to zero, making the beam appear narrower by hiding dim portions of the phosphor trail. Lower thresholds show more of the trail; higher thresholds reveal only the brightest recent trace positions. In Thick mode, the threshold is bypassed and all canvas intensity is displayed.

---

#### Knob 5 — Persist
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Persist controls the phosphor decay rate. Each frame, every canvas pixel is reduced by (Persist >> 2) intensity units, clamped to a minimum of 1. High Persist means slow decay — the beam leaves long glowing trails. Low Persist means rapid decay — only the most recent beam positions are visible. At maximum, trails persist for many seconds; at minimum, only the current frame's trace is visible.

---

#### Knob 6 — Hue
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 120d |
| Suffix | d |

Hue sets the beam colour. In Mono mode, a single sine-derived UV pair from the hue knob position colours all pixels uniformly. In Multi mode, the hue index is offset by each pixel's intensity, so bright leading edges have one colour while dim trails shift toward another — simulating the colour temperature variation of real laser phosphor interaction.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Beams** | Single | Split |
| **8 — Trace** | Thin | Thick |
| **9 — Color** | Mono | Multi |
| **10 — Blanking** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure beam splitting, line thickness, colour mode, strobe blanking, and bypass. Beams and Trace affect the drawing phase; Color affects readout; Blanking affects both. The combination of Split beams with Multi colour produces the most visually complex output, with two interleaving traces each cycling through intensity-dependent colour.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the input video (dry) and the laser synthesis (wet). At minimum the original video passes; at maximum only the laser pattern is visible. Intermediate positions overlay the laser traces on the video, creating a laser-over-image composite.





---

## Guided Exercises

These exercises demonstrate the range of laser deflection patterns, from gentle rosettes to chaotic multi-beam traces.

### Exercise 1: Classic Rosette

<img src={laserium_exercise1_result} alt="Classic Rosette result"/>
*Classic Rosette — simulated result across source images.*
**What You'll Create**: Create the iconic Laserium rosette — the most recognisable laser light show pattern.

1. Set Pattern to position 1 (Rosette).
2. Set Speed to 25%, Spread to 50%.
3. Set Persist to 75% for long glowing trails.
4. Set Hue to a green (≈120°) for classic argon laser colour.
5. Set Beams to Single, Trace to Thin, Color to Mono.
6. Observe the beam tracing a multi-petalled flower that gradually fills as oscillator phases evolve.

**Key concepts**: The rosette pattern uses two sine oscillators at different frequencies. The frequency ratio determines the number of petals. With persistence, the petals accumulate into a complete flower as the beam retraces slightly offset paths each frame.

---

### Exercise 2: Split Beam Spiral

<img src={laserium_exercise2_result} alt="Split Beam Spiral result"/>
*Split Beam Spiral — simulated result across source images.*
**What You'll Create**: Create an expanding spiral with beam splitting and multi-colour trails.

1. Set Pattern to position 2 (Spiral).
2. Set Speed to 35%, Spread to 60%.
3. Set Persist to 60%, Beam Width to 15%.
4. Enable Split and Multi colour.
5. Set Hue to 0° (red base).
6. Watch the dual beams spiral outward in mirror symmetry, leaving rainbow trails that encode their intensity history.

**Key concepts**: The spiral pattern uses expanding-amplitude Lissajous. Split beams create two spirals growing in opposite directions. Multi colour maps pixel intensity to hue, so the bright leading edges are red while the decaying trails shift through the spectrum.

---

### Exercise 3: Chaos Storm

<img src={laserium_exercise3_result} alt="Chaos Storm result"/>
*Chaos Storm — simulated result across source images.*
**What You'll Create**: Create a dense, unpredictable field of laser traces using the chaos pattern with thick beams and blanking.

1. Set Pattern to position 8 (Chaos).
2. Set Speed to 55%, Spread to 70%.
3. Set Persist to 50%, Beam Width to 30%.
4. Enable Thick trace and Blanking.
5. Set Color to Multi, Hue to 200°.
6. Enable Split for maximum density.
7. Observe the flickering, multi-coloured chaos field.

**Key concepts**: The chaos pattern XORs oscillator phases, producing non-repeating beam trajectories. Combined with thick trace, blanking strobe, and split beams, this creates the most dense and visually complex output — a flickering storm of coloured light.

---


## Tips

- **Split + Multi for maximum complexity**: Two beams with intensity-mapped colour produces the richest visual output.
- **Blanking at high Persist**: Blanking is most interesting at high persistence, where the flickering creates a subtle pulsing glow rather than an abrupt strobe.
- **Chaos is unpredictable**: Pattern 8 uses phase XOR, which produces non-repeating trajectories — every frame is unique.
- **Green for authenticity**: Set Hue to ~120° for argon laser green, the most common colour in original Laserium shows.
- **Beam Width as filter**: In Thin mode, increasing Beam Width suppresses the dimmest trail elements, acting as a visual noise floor.

---
