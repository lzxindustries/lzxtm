---
draft: true
sidebar_position: 199
slug: /instruments/videomancer/munching
title: "Munching"
image: /img/instruments/videomancer/munching/munching_hero.png
description: "Munching recreates the classic \"munching squares\" pattern from MIT's HAKMEM memo #146, originally demonstrated on the PDP-1 computer in the early 1970s."
---

import munching_hero from '/img/instruments/videomancer/munching/munching_hero.png';
import munching_animation from '/img/instruments/videomancer/munching/munching_animation.gif';
import munching_control_panel from '/img/instruments/videomancer/munching/munching_control_panel.png';
import munching_exercise1_result from '/img/instruments/videomancer/munching/munching_exercise1_result.gif';
import munching_exercise2_result from '/img/instruments/videomancer/munching/munching_exercise2_result.gif';
import munching_exercise3_result from '/img/instruments/videomancer/munching/munching_exercise3_result.gif';

# Munching

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={munching_hero} alt="Munching hero image"/>
*Geometric bitwise patterns tessellate the screen in 16-colour grids, recreating the legendary PDP-1 HAKMEM #146 munching squares display.*
<img src={munching_animation} alt="Munching animated output"/>
*Munching output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Munching recreates the classic "munching squares" pattern from MIT's HAKMEM memo #146, originally demonstrated on the PDP-1 computer in the early 1970s. The effect generates intricate geometric tessellations by applying bitwise operations to screen coordinates — for each pixel, the XOR (or AND) of its x and y coordinates produces a self-similar pattern that tiles the screen in recursive fractal-like structures.

The name comes directly from the PDP-1 display hack terminology. "Munching" referred to the visual impression of the pattern as it animated: squares appeared to be consumed and regenerated in an endlessly recursive cascade. HAKMEM (an acronym for "hacks memo") was a legendary collection of algorithms compiled at MIT's AI Lab — item #146 described the XOR coordinate pattern and its mesmerising animation when the time parameter sweeps linearly.

Videomancer's FPGA implementation extends the original monochrome display hack with a 16-colour palette, variable scaling via bit-select, an Op Blend control that crossfades between XOR and AND operations, and optional video modulation. The animated time parameter cycles through all 256 possible XOR masks, producing a continuously evolving geometric display.

---

## Quick Start

1. **Scale for composition**: Lower Scale values create bold geometric blocks suitable for background textures; higher values add noise-like fine detail.
2. **Mask as preset**: In Static mode, specific Mask values produce distinct patterns — 0, 85, 170, and 255 are good starting points for exploration.
3. **Op Blend for morphing**: Automate Op Blend via CV to smoothly morph between square and triangular tessellations during performance.

---

## Background

### HAKMEM and the PDP-1

HAKMEM (AI Memo 239, February 1972) was a collection of number theory results, algorithms, and hardware hacks compiled by Bill Gosper, Richard Greenblatt, and others at the MIT AI Laboratory. Item #146 described a display program where the value plotted at screen position (x, y) is x XOR y — a trivially simple calculation that produces surprisingly complex recursive square patterns. The PDP-1's Type 30 CRT display rendered this as a point-plotting program, and the visual result became one of the earliest examples of generative computer art.

### Bitwise Coordinate Operations

The core algorithm evaluates f(x, y) = (x ⊕ y) at every pixel, where ⊕ represents the XOR operation. XOR of two coordinates produces a pattern where each bit of the result corresponds to a spatial frequency doubling — the least significant bit creates a checkerboard at single-pixel scale, the next bit creates 2×2 blocks, and so on. The superposition of all bits generates the characteristic recursive nested-square pattern. Replacing XOR with AND produces a different but related Sierpiński-triangle-like pattern.

### Scale and Bit Selection

The Scale parameter selects which bits of the coordinate values are used in the bitwise operation. Lower scales use the most significant bits, producing large-scale block patterns. Higher scales include lower bits, revealing finer detail. This is equivalent to zooming into different levels of the self-similar fractal structure — the pattern repeats at every power-of-two scale.

### Animated Time Parameter

When Time mode is set to Anim, a frame counter (the Mask value swept automatically) is XORed with the coordinate result before palette lookup. As this counter advances, different subsets of the pattern illuminate and extinguish in sequence, producing the "munching" animation that gives the effect its name. The pattern appears to flow and reconfigure itself continuously.


---

## Signal Flow

```
 registers_in(0) ── Speed ─────────────────────────────────────────────────┐
 registers_in(1) ── Mask (0–255) ──────────────────────────────────────────┤
 registers_in(2) ── Scale (8 steps) ───────────────────────────────────────┤
 registers_in(3) ── Hue Shift ─────────────────────────────────────────────┤
 registers_in(4) ── Bright ────────────────────────────────────────────────┤
 registers_in(5) ── Op Blend ──────────────────────────────────────────────┤
 registers_in(6) ── Toggles [Op XOR/AND|Time Static/Anim|Invert|ModVid|Bypass]
 registers_in(7) ── Mix Fader ─────────────────────────────────────────────┤
                                                                            │
 ┌─────────────────────────────────────────────────────────────────────────┘
 │
 │    ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
 ├───►│  COORDINATE GEN  │────►│  BITWISE OP      │────►│  PALETTE LOOKUP  │
 │    │  x, y from sync  │     │  x OP y ⊕ mask   │     │  4-bit index     │
 │    │  scale bit-shift  │     │  XOR / AND blend │     │  → 16 RGB        │
 │    └──────────────────┘     └──────────────────┘     │  → YUV 10-bit    │
 │                                                       └───────┬─────────┘
 │                                                               │
 │    ┌──────────────────┐       │ coloured YUV
 │    │  BRIGHTNESS &    │◄──────┘
 │    │  INVERT CONTROL  │
 │    │  proc_amp style  │
 │    └──────────┬───────┘
 │               │
 │    ┌──────────┴───────┐
 └───►│  INTERPOLATOR    │
      │  dry/wet mix     │
      └──────────────────┘
               │
               ▼
          data_out (YUV)
```

The pipeline is purely combinational per pixel: screen coordinates are right-shifted by the Scale parameter, then the selected bitwise operation (XOR or AND) is applied. The result is XORed with the current Mask value (animated or static) and the lowest 4 bits index into a 16-entry colour palette. Op Blend crossfades between the XOR and AND results, allowing smooth morphing between the two pattern families.

The Hue Shift parameter rotates the palette index, effectively shifting which colour band maps to which geometric region. Combined with the animated time parameter, this creates the effect of colours flowing through the fixed geometric structure. The Invert toggle complements the index bits, producing a negative image of the pattern.

---

## Parameter Reference

<img src={munching_control_panel} alt="Videomancer front panel with Munching loaded"/>
*Videomancer's front panel with Munching active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Speed controls the rate at which the animated time parameter advances through its 256-step cycle. At zero the animation is frozen (equivalent to Static mode at the current mask). At maximum the pattern cycles so rapidly that the munching animation becomes a shimmering blur of evolving geometry.

---

#### Knob 2 — Mask
| Property | Value |
|----------|-------|
| Range | 0 – 255 |
| Default | 255 |

Mask sets the XOR mask applied to the bitwise coordinate result before palette lookup. Each of the 8 mask bits selectively inverts a corresponding spatial frequency band, producing 256 distinct pattern variations. In Static time mode this value is set manually; in Anim mode it is overridden by the animated counter.

---

#### Knob 3 — Scale
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 3 |

Scale selects the coordinate bit range used in the bitwise operation, from 0 (coarsest, using only the most significant bits) to 7 (finest, including the least significant bits). Low values produce large blocky squares. High values reveal the full recursive detail of the pattern. This is equivalent to choosing the zoom level within the self-similar fractal.

---

#### Knob 4 — Hue Shift
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Hue Shift rotates the 16-entry colour palette index. As the knob sweeps from minimum to maximum, the geometric regions cycle through different palette colours while the pattern structure remains fixed. This decouples colour from geometry, allowing independent colour animation.

---

#### Knob 5 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Bright is a global luminance multiplier applied after palette lookup. At zero the output is black. At full value the palette colours appear at their maximum defined intensity. Intermediate values uniformly dim the output.

---

#### Knob 6 — Op Blend
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Op Blend crossfades between the XOR and AND bitwise operation results. At minimum, the output is pure XOR (classic munching squares). At maximum, the output is pure AND (Sierpiński-like triangular tiling). Intermediate positions blend the two patterns, producing hybrid geometries that morph smoothly between the two families.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Op** | XOR | AND |
| **8 — Time** | Static | Anim |
| **9 — Invert** | Off | On |
| **10 — Mod Vid** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control the pattern generation and rendering mode. Op selects the baseline bitwise operation. Time switches between static and animated mask modes. Invert complements the palette index. Mod Video and Bypass control video compositing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the processed munching output. At minimum the output is entirely dry. At maximum the output is entirely wet. Intermediate values blend the geometric pattern over the source material.





---

## Guided Exercises

These three exercises move from a static single-operation exploration to a fully animated blended composition, progressively revealing the munching squares' generative depth.

### Exercise 1: Classic XOR Squares

<img src={munching_exercise1_result} alt="Classic XOR Squares result"/>
*Classic XOR Squares — simulated result across source images.*
**What You'll Create**: Reproduce the original HAKMEM #146 monochrome munching squares pattern at full resolution.

1. Set Op to XOR.
2. Set Time to Static.
3. Set Scale to 7 (finest detail).
4. Set Mask to 0 (no modification).
5. Set Hue Shift to 0.
6. Set Bright to full.
7. Set Invert to Off.
8. Set Mix to 100%.
9. Slowly sweep the Mask knob from 0 to 1023 and observe 256 distinct pattern states.
10. Note the recursive square structure at each mask value.

**Key concepts**: Bitwise XOR of coordinates, recursive self-similarity, mask as pattern selector.

---

### Exercise 2: Animated AND Sierpiński

<img src={munching_exercise2_result} alt="Animated AND Sierpiński result"/>
*Animated AND Sierpiński — simulated result across source images.*
**What You'll Create**: Create an animated Sierpiński-triangle pattern using the AND operation with time cycling.

1. Set Op to AND.
2. Set Time to Anim.
3. Set Speed to approximately 30%.
4. Set Scale to 5 (moderate detail).
5. Set Hue Shift to approximately 50%.
6. Set Bright to approximately 80%.
7. Set Op Blend to maximum (pure AND).
8. Observe the triangular tiling pattern cycling through mask values.
9. Experiment with Scale — lower values create larger triangle hierarchies.

**Key concepts**: AND coordinate patterns, Sierpiński geometry, animated colour cycling.

---

### Exercise 3: XOR/AND Morph with Video

<img src={munching_exercise3_result} alt="XOR/AND Morph with Video result"/>
*XOR/AND Morph with Video — simulated result across source images.*
**What You'll Create**: Blend between XOR and AND patterns over live video to create an evolving geometric overlay.

1. Set Time to Anim.
2. Set Speed to approximately 20%.
3. Set Scale to 6.
4. Set Op Blend to approximately 50% (midpoint between XOR and AND).
5. Enable Mod Video.
6. Set Mix to approximately 65%.
7. Feed a video source with clear shapes.
8. Slowly sweep Op Blend from 0 to 1023 to morph between XOR squares and AND triangles.
9. Toggle Invert for negative/positive comparison.
10. Adjust Hue Shift to change which colours dominate.

**Key concepts**: Operation blending, XOR/AND morphing, video modulation masking.

---


## Tips

- **Hue Shift decouples colour**: Animate Hue Shift independently of the time parameter to create two layers of visual motion — geometry and colour.
- **Invert for contrast**: Toggle Invert to swap foreground and background when the default colour mapping doesn't contrast well with your video source.
- **Low Speed for meditation**: Very slow animation rates (5–10%) create gradually evolving wallpaper-like textures suitable for ambient installations.
- **AND mode for triangles**: Switch to AND mode for Sierpiński-like diagonal fractal patterns — visually distinct from the square-based XOR patterns.

---
