---
draft: true
sidebar_position: 59
slug: /instruments/videomancer/colrspace
title: "Colrspace"
image: /img/instruments/videomancer/colrspace/colrspace_hero.png
description: "Colrspace recreates the expanding symmetrical colour patterns of Jeff Minter's 1985 Colourspace light synthesiser for the Atari 8-bit."
---

import colrspace_hero from '/img/instruments/videomancer/colrspace/colrspace_hero.png';
import colrspace_animation from '/img/instruments/videomancer/colrspace/colrspace_animation.gif';
import colrspace_control_panel from '/img/instruments/videomancer/colrspace/colrspace_control_panel.png';
import colrspace_exercise1_result from '/img/instruments/videomancer/colrspace/colrspace_exercise1_result.gif';
import colrspace_exercise2_result from '/img/instruments/videomancer/colrspace/colrspace_exercise2_result.gif';
import colrspace_exercise3_result from '/img/instruments/videomancer/colrspace/colrspace_exercise3_result.gif';

# Colrspace

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={colrspace_hero} alt="Colrspace hero image"/>
*Geometric colour pulses ripple outward from a central emitter, reflecting across four symmetry axes to form an evolving kaleidoscopic mandala on a persistent grid.*
<img src={colrspace_animation} alt="Colrspace animated output"/>
*Colrspace output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Colrspace recreates the expanding symmetrical colour patterns of Jeff Minter's 1985 Colourspace light synthesiser for the Atari 8-bit. Two independent emitters trace Lissajous paths across a 48 × 27 cell grid, stamping geometric shapes that persist and slowly decay. Where stamps overlap, their colour indices accumulate and wrap through a 16-colour hue wheel, producing unexpected secondary hues at intersection points.

The name is a contraction of "Colour Space" — the original Llamasoft title. Where Psychedelia (1984) used a single cursor and simple diamond stamps, Colourspace expanded the concept with dual emitters, a larger pattern vocabulary of eight geometric shapes, and mandatory four-way reflective symmetry that turns every stamp into a mirrored mandala.

In Videomancer's implementation the grid cells map to 40 × 40 pixel blocks on screen. Each cell stores a 4-bit colour index that decrements once per frame (unless refreshed by a new stamp), producing smooth organic decay trails. The 16-colour palette cycles continuously under knob control, so even a static pattern shifts hue over time.

---

## Background

### The Llamasoft Light Synthesisers

Between 1984 and 1994, Jeff Minter created a series of interactive light synthesisers — Psychedelia, Colourspace, Trip-a-Tron, and later the Atari Jaguar Virtual Light Machine — that treated the television screen as a musical instrument. Rather than games, these programs were designed for live audio-visual performance: the user moved a cursor (often mapped to a joystick) while music played, and patterns bloomed and faded on screen in response. Colourspace was the second in the series, adding a second emitter and reflective symmetry.

### Framebuffer Persistence and Decay

The core technical innovation across all Minter light synths is the persistent framebuffer with per-cell decay. Unlike conventional video effects that compute each frame from scratch, Colourspace carries state between frames: new stamps write maximum brightness into cells, and every frame a decay pass subtracts one from every non-zero cell. This produces the characteristic organic trails — a burst of colour expands outward, then fades through the palette from hot to cool as each cell's index counts down toward black.

### Lissajous Emitter Trajectories

Each emitter follows a Lissajous curve — the parametric path produced by two perpendicular sinusoidal oscillations at different frequencies. The frequency ratio and phase offset determine the shape: 1:1 produces an ellipse, 1:2 a figure-eight, 2:3 a pretzel, and irrational ratios fill the grid ergodically. The Speed knob scales the phase increment, controlling how quickly the emitter traverses its orbit, while the Spread knob adjusts the Lissajous amplitude.

### Stamp Shapes and Symmetry

Eight geometric stamp patterns are available, each defined by a Manhattan-distance or axis test applied to a small neighbourhood around the emitter position. Diamond, Cross, Star, X-shape, Box, Ring, Asterisk, and Large Diamond each produce a distinct spatial footprint. Four-way symmetry reflects every stamp across both the horizontal and vertical centre lines, so a single emitter position generates four simultaneous stamps, and with dual emitters enabled the grid receives eight stamps per frame.


---

## Signal Flow

```
 registers_in(0) ── Speed ──────────────────────────────────────────────────┐
 registers_in(1) ── Pattern (8 steps) ──────────────────────────────────────┤
 registers_in(2) ── Hue Speed ─────────────────────────────────────────────┤
 registers_in(3) ── Decay ─────────────────────────────────────────────────┤
 registers_in(4) ── Brightness ────────────────────────────────────────────┤
 registers_in(5) ── Spread ────────────────────────────────────────────────┤
 registers_in(6) ── Toggles [Emitters|Symmetry|Reset|ModVid|Bypass] ───────┤
 registers_in(7) ── Mix Fader ─────────────────────────────────────────────┤
                                                                            │
 ┌─────────────────────────────────────────────────────────────────────────┘
 │
 │    ┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
 ├───►│  DECAY PASS      │────►│  EMITTER UPDATE  │────►│  STAMP PASS     │
 │    │  for each cell:  │     │  Lissajous phase │     │  8 shape tests  │
 │    │  if val > 0:     │     │  advance per     │     │  4-way symmetry │
 │    │    val -= 1      │     │  emitter (×2)    │     │  write 15 to    │
 │    └──────────────────┘     └─────────────────┘     │  hit cells      │
 │                                                      └───────┬─────────┘
 │                                                              │
 │    ┌─────────────────────────────────────────────────────┐   │ 48×27×4-bit
 │    │   PALETTE LOOKUP                                    │◄──┘ framebuffer
 │    │   hue_offset cycles each frame                     │
 │    │   pal_idx = (cell_val + hue_offset) mod 16         │
 │    │   16-colour hue wheel → YUV                        │
 │    │   brightness scaling                               │
 │    └──────────────────────────┬──────────────────────────┘
 │                               │
 │    ┌──────────────────┐       │ processed YUV
 └───►│  INTERPOLATOR    │◄──────┘
      │  dry/wet mix     │
      └──────────────────┘
               │
               ▼
          data_out (YUV)
```

The processing pipeline executes three passes per frame in sequence. First the decay pass walks every cell of the 48 × 27 grid and decrements any non-zero value by one — the Decay knob does not control the decrement rate directly but rather the stamp replenishment cycle, so higher Decay values cause stamps to fire less frequently, producing longer trails. Second, each emitter advances its Lissajous phase and computes its grid-space position from sine lookups. Third, the stamp pass iterates a small neighbourhood around each emitter position and applies the selected shape test to decide which cells receive the maximum value of 15.

Four-way symmetry reflects each stamp position across the grid's horizontal and vertical centre lines, generating four simultaneous writes from each emitter. With dual emitters enabled, the grid receives up to eight stamps per frame, producing dense interlocking mandala patterns. The 16-colour hue wheel palette rotates continuously under the Hue Speed control, cycling all non-zero cells through the spectrum without rewriting the framebuffer.

---

## Parameter Reference

<img src={colrspace_control_panel} alt="Videomancer front panel with Colrspace loaded"/>
*Videomancer's front panel with Colrspace active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Speed controls the per-frame phase increment for both Lissajous emitters. At low values the cursors drift slowly across the grid, producing widely spaced stamps with visible decay trails between them. At high values the cursors race around their orbits, saturating the grid with overlapping stamps that blend into dense colour fields. Very high speeds can create near-uniform colour fills with subtle interference patterns at the symmetry boundaries.

---

#### Knob 2 — Pattern
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 1 |

Pattern selects one of eight geometric stamp shapes applied to the grid around each emitter position. The eight shapes progress from compact (Diamond, radius 2) to expansive (Large Diamond, radius 4), with crosses, stars, boxes, rings, and asterisks in between. Each shape produces a distinct visual texture when tiled across the grid by the moving emitters.

---

#### Knob 3 — Hue Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

Hue Speed controls how rapidly the palette offset cycles through the 16-colour hue wheel. At zero the colour mapping is static. At moderate values the entire pattern slowly shifts through the spectrum, creating a breathing colour effect. At maximum the hue cycles so rapidly that the pattern appears to shimmer with fast-moving rainbow bands.

---

#### Knob 4 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 34% |
| Suffix | % |

Decay adjusts the persistence of stamped cells. At low values cells fade quickly — each stamp produces a brief flash that vanishes within a few frames. At high values cells persist for many frames, and the grid fills with overlapping trails of colour. The visual character shifts from staccato bursts to flowing ribbons of light as Decay increases.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 78% |
| Suffix | % |

Brightness is a global intensity multiplier applied to the palette lookup. At zero the output is black regardless of grid content. At full value the 16-colour palette displays at maximum saturation and luminance. This control interacts with the Mix fader — at moderate Brightness with partial Mix, the mandala pattern becomes a translucent overlay.

---

#### Knob 6 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Spread adjusts the amplitude of the Lissajous emitter trajectories. At minimum the emitters stay near the grid centre, producing compact symmetrical patterns. At maximum the emitters sweep to the grid edges, covering the full 48 × 27 area. Combined with four-way symmetry, wider spread creates larger mandala structures with more open negative space between the reflected stamps.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Emitters** | Single | Dual |
| **8 — Symmetry** | Off | 4-Way |
| **9 — Reset** | Off | On |
| **10 — Mod Video** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the emitter count, symmetry mode, and output routing. Emitters switches between single and dual cursor operation — dual mode doubles the stamp density and creates interleaving patterns from two independent Lissajous paths. Symmetry enables or disables the four-way grid reflection. Reset clears the entire framebuffer to zero, useful for starting fresh patterns. Mod Video multiplies the synthesised luma with the input video luma, creating a window effect. Bypass passes the input through unmodified.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input signal and the synthesised mandala output. At minimum the output is entirely dry. At maximum the output is entirely wet. Intermediate positions blend the two, allowing the mandala to emerge gradually over the source material.

---

## Guided Exercises

These three exercises build from a minimal single-emitter configuration to a full dual-emitter mandala performance, exploring the interplay between stamp shapes, symmetry, decay, and hue cycling.

### Exercise 1: Single Emitter Diamond Pulse

<img src={colrspace_exercise1_result} alt="Single Emitter Diamond Pulse result"/>
*Single Emitter Diamond Pulse — simulated result across source images.*
**Objective**: Produce a minimal expanding diamond pattern from a single slow-moving emitter to understand the stamp-and-decay cycle.

1. Set Emitters to Single and Symmetry to 4-Way.
2. Set Pattern to 1 (Diamond).
3. Set Speed to approximately 25%.
4. Set Decay to approximately 35%.
5. Set Hue Speed to zero for static colour.
6. Set Brightness to approximately 80%.
7. Set Spread to approximately 50% for moderate orbit.
8. Set Mix to 100%.
9. Observe the diamond stamps appearing at four reflected positions and fading through the palette toward black.

**Key concepts**: Stamp geometry, four-way symmetry reflection, per-cell decay.

---

### Exercise 2: Dual Emitter Rainbow Mandala

<img src={colrspace_exercise2_result} alt="Dual Emitter Rainbow Mandala result"/>
*Dual Emitter Rainbow Mandala — simulated result across source images.*
**Objective**: Create a dense, continuously shifting mandala by combining dual emitters with fast hue cycling and a complex stamp shape.

1. Switch Emitters to Dual.
2. Set Pattern to 7 (Asterisk) for wide stamp coverage.
3. Increase Speed to approximately 40%.
4. Set Hue Speed to approximately 50% for visible colour rotation.
5. Set Decay to approximately 60% for long trails.
6. Set Spread to approximately 80% for wide orbits.
7. Set Brightness to approximately 75%.
8. Observe the two emitters creating interlocking reflected asterisks with shifting hue bands.

**Key concepts**: Dual emitter interference, hue cycling through decay trails, pattern density.

---

### Exercise 3: Video-Modulated Mandala Overlay

<img src={colrspace_exercise3_result} alt="Video-Modulated Mandala Overlay result"/>
*Video-Modulated Mandala Overlay — simulated result across source images.*
**Objective**: Use the Mod Video toggle to mask the mandala pattern with live video input, creating a real-time video-shaped window into the colour field.

1. Keep the Exercise 2 dual emitter mandala running.
2. Toggle Mod Video to On.
3. Set Mix to approximately 75%.
4. Feed a high-contrast video source (e.g., a face or text).
5. Observe the mandala appearing only in bright video regions.
6. Experiment with Brightness and Spread to control the interaction.
7. Toggle Mod Video off to compare with the un-modulated mandala.
8. Try reducing Mix to 50% for a more subtle overlay blend.

**Key concepts**: Luminance modulation, synthesis-processing hybrid, wet/dry blending.

---


## Tips

- **Start with Diamond**: The compact Diamond stamp (Pattern 1) is the clearest way to understand the stamp-and-decay cycle before moving to denser shapes.
- **Use Reset for transitions**: During live performance, toggling Reset provides an instant clean slate — more dramatic than waiting for decay to clear the grid.
- **Match Decay to Speed**: Faster emitter speeds fill the grid more quickly, so higher Decay values prevent the grid from saturating into a uniform colour field.
- **Hue Speed as rhythm**: Map the Hue Speed knob to an LFO synchronised with music to create colour pulsing that follows the beat.
- **Mod Video for masking**: The Mod Video toggle is most effective with high-contrast input — text, silhouettes, or oscilloscope patterns create dramatic windows into the mandala.
- **Dual emitters need wide Spread**: With two emitters and 4-way symmetry, eight stamps per frame can saturate a small area quickly. Increase Spread to distribute stamps across the full grid.
- **Combine with downstream effects**: The blocky grid output is an excellent source for downstream blur, feedback, or colouriser programs.

---
