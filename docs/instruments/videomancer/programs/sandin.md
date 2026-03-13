---
draft: true
sidebar_position: 255
slug: /instruments/videomancer/sandin
title: "Sandin"
image: /img/instruments/videomancer/sandin/sandin_hero_s1.png
description: "Sandin is a digital homage to the Sandin Image Processor (IP), the pioneering analogue video instrument built by Dan Sandin at the University of Illinois at Chicago in 1973."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import sandin_control_panel from '/img/instruments/videomancer/sandin/sandin_control_panel.png';
import sandin_source1_house from '/img/instruments/videomancer/sandin/sandin_source1_house.png';
import sandin_source2_ballerina from '/img/instruments/videomancer/sandin/sandin_source2_ballerina.png';
import sandin_source3_turtle from '/img/instruments/videomancer/sandin/sandin_source3_turtle.png';
import sandin_source4_pattern from '/img/instruments/videomancer/sandin/sandin_source4_pattern.png';
import sandin_source5_man from '/img/instruments/videomancer/sandin/sandin_source5_man.png';
import sandin_source6_knit from '/img/instruments/videomancer/sandin/sandin_source6_knit.png';
import sandin_hero_s1 from '/img/instruments/videomancer/sandin/sandin_hero_s1.png';
import sandin_hero_s2 from '/img/instruments/videomancer/sandin/sandin_hero_s2.png';
import sandin_hero_s3 from '/img/instruments/videomancer/sandin/sandin_hero_s3.png';
import sandin_hero_s4 from '/img/instruments/videomancer/sandin/sandin_hero_s4.png';
import sandin_hero_s5 from '/img/instruments/videomancer/sandin/sandin_hero_s5.png';
import sandin_hero_s6 from '/img/instruments/videomancer/sandin/sandin_hero_s6.png';
import sandin_ex1_s1 from '/img/instruments/videomancer/sandin/sandin_ex1_s1.png';
import sandin_ex1_s2 from '/img/instruments/videomancer/sandin/sandin_ex1_s2.png';
import sandin_ex1_s3 from '/img/instruments/videomancer/sandin/sandin_ex1_s3.png';
import sandin_ex1_s4 from '/img/instruments/videomancer/sandin/sandin_ex1_s4.png';
import sandin_ex1_s5 from '/img/instruments/videomancer/sandin/sandin_ex1_s5.png';
import sandin_ex1_s6 from '/img/instruments/videomancer/sandin/sandin_ex1_s6.png';
import sandin_ex2_s1 from '/img/instruments/videomancer/sandin/sandin_ex2_s1.png';
import sandin_ex2_s2 from '/img/instruments/videomancer/sandin/sandin_ex2_s2.png';
import sandin_ex2_s3 from '/img/instruments/videomancer/sandin/sandin_ex2_s3.png';
import sandin_ex2_s4 from '/img/instruments/videomancer/sandin/sandin_ex2_s4.png';
import sandin_ex2_s5 from '/img/instruments/videomancer/sandin/sandin_ex2_s5.png';
import sandin_ex2_s6 from '/img/instruments/videomancer/sandin/sandin_ex2_s6.png';
import sandin_ex3_s1 from '/img/instruments/videomancer/sandin/sandin_ex3_s1.png';
import sandin_ex3_s2 from '/img/instruments/videomancer/sandin/sandin_ex3_s2.png';
import sandin_ex3_s3 from '/img/instruments/videomancer/sandin/sandin_ex3_s3.png';
import sandin_ex3_s4 from '/img/instruments/videomancer/sandin/sandin_ex3_s4.png';
import sandin_ex3_s5 from '/img/instruments/videomancer/sandin/sandin_ex3_s5.png';
import sandin_ex3_s6 from '/img/instruments/videomancer/sandin/sandin_ex3_s6.png';

# Sandin

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "House", before: sandin_source1_house, after: sandin_hero_s1 },
    { label: "Ballerina", before: sandin_source2_ballerina, after: sandin_hero_s2 },
    { label: "Turtle", before: sandin_source3_turtle, after: sandin_hero_s3 },
    { label: "Pattern", before: sandin_source4_pattern, after: sandin_hero_s4 },
    { label: "Man", before: sandin_source5_man, after: sandin_hero_s5 },
    { label: "Knit", before: sandin_source6_knit, after: sandin_hero_s6 },
  ]}
/>
*Video-derived edge signals cascade through multiply and add stages, producing a self-referential feedback glow where bright edges reinforce and dark regions fold inward.*

---

## Overview

Sandin is a digital homage to the Sandin Image Processor (IP), the pioneering analogue video instrument built by Dan Sandin at the University of Illinois at Chicago in 1973.  The original IP featured a modular patch-cord architecture where video signals could be derived from themselves — extracted, inverted, offset, and recombined — to produce complex abstract imagery from a single source.  This program implements the IP's fundamental signal flow: a derivation stage that extracts edge, offset, or inverted versions of the input, followed by a cross-modulation stage that combines the original and derived signals through multiplication or division.

The derivation chain uses a per-scanline line buffer to compute horizontal differences (edges), adds a constant offset, and optionally inverts the result.  The cross-modulation stage multiplies or divides the derived signal with the original luminance, producing second-order interactions: edges brightened by overall scene luminance, or dark regions amplified by their own edge content.  A feedback path routes the output back into the derivation chain, creating self-referential signal loops that evolve over time.

The result ranges from subtle edge-enhanced video to intensely abstract, glowing forms that bear only a passing resemblance to the source — depending on the derivation amount, feedback level, and cross-modulation mode.

---

## Quick Start

1. **Start with zero Feedback:** Learn the derivation modes before adding feedback — each mode has a distinct character that is clearest without recursion.
2. **Divide for ethereal glow:** The Divide mode is Sandin's secret weapon — it reveals structure in shadows, creating an X-ray transparency effect.
3. **Double cascade for texture:** When the source has fine detail (fabrics, foliage, hair), Double cascade extracts textures that Single cascade misses.

---

## Background

### The Sandin Image Processor

Dan Sandin's Image Processor (1973) was one of the first open-architecture analogue video synthesis instruments.  Its design philosophy — "distribution religion" — made the schematics freely available, encouraging other artists to build their own.  The IP processed NTSC video through a chain of analogue modules: differentiators, offset generators, inverters, multipliers, and adders.  The key innovation was self-derivation: the output of one stage could be patched back into an earlier stage, creating feedback loops that transformed realistic video into abstract light paintings.

### Edge Derivation

The edge derivation stage computes the horizontal difference between adjacent pixels using the line buffer.  This is equivalent to a first-order spatial derivative — a discrete approximation of the signal's slope.  Bright edges (rising luminance) produce positive values; dark edges (falling luminance) produce negative values.  The absolute value of the derivative produces a symmetric edge map that highlights contours regardless of direction.

### Cross-Modulation

In the analogue domain, multiplying two video signals produces a result where bright areas of one signal selectively reveal or suppress the other.  Sandin's IP used four-quadrant multipliers for this purpose.  In Multiply mode, the derived signal is multiplied with the original: edges become visible only where the source is bright, producing a selective contour effect.  In Divide mode (implemented as the complement multiplication), edges appear preferentially in dark regions, creating an ethereal glow around shadows.

### Feedback and Self-Reference

The Feedback toggle routes the processed output back into the derivation chain's input.  This creates a recursive loop: edges are derived from a signal that already contains edges, producing second- and third-order derivatives.  The visual effect is a progressive sharpening and saturation of edge content — at low feedback levels, edges are crisply enhanced; at high levels, the image disintegrates into ringing oscillation patterns reminiscent of Larsen feedback in audio.

### Chroma Rotation

The Color Tint knob applies a hue rotation to the chrominance channels, shifting the colour cast of the processed output.  Combined with the single/double cascade toggle, this allows building complex colour-space transformations: a double cascade with different tints on each stage produces complementary colour fringing along edges.


---

## Signal Flow

```
      Input Video (Y/U/V)
             │
    ┌────────▼────────┐
    │  Line Buffer     │
    │  (1 scanline)    │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Derivation      │
    │  Edge / Offset / │
    │  Invert / Color  │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  × Derive Amt    │
    └────────┬────────┘
             │
    ┌────────▼────────────────┐
    │  Cross-Modulation       │
    │  (Multiply / Divide)    │
    │  derived × original     │
    └────────┬────────────────┘
             │
    ┌────────▼────────┐
    │  Feedback Path   │
    │  (output → input)│
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Clamp / Wrap    │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Colour Tint     │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Interpolator Mix│
    └────────┬────────┘
             │
          Output Y/U/V
```

The line buffer stores the previous scanline so the derivation stage can compute the horizontal difference between the current pixel and its left neighbour.  Vertical derivation is not directly computed — the vertical structure emerges indirectly when feedback is active, because the previous frame's edge content is fed back through the vertical scan.

The Cascade toggle doubles the derivation chain — two successive edge/offset/invert stages — producing a second derivative (laplacian-like) response that emphasises fine texture over broad edges.  The Clamp/Saturate toggle determines whether the cross-modulation result is clamped to the 0–1023 range (hard saturation) or wrapped modulo 1024 (producing false contours and colour inversions).

---

## Parameter Reference

<img src={sandin_control_panel} alt="Videomancer front panel with Sandin loaded"/>
*Videomancer's front panel with Sandin active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Derive Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Derive Amt sets the strength of the derivation effect.  At zero the derived signal is the original input unmodified; at maximum the horizontal edge derivative dominates entirely.  Moderate settings (30–50 %) produce a blended result that retains recognisable image structure while enhancing edges.  High settings (80–100 %) strip away broad luminance, leaving only contour lines.

---

#### Knob 2 — Offset H
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Offset H adds a horizontal pixel offset to the derivation — the delayed copy is shifted not by one pixel but by a variable amount.  At minimum the shift is a single pixel (fine edge detection).  Increasing Offset H widens the spatial derivative, producing broader, softer edge responses that detect luminance gradients over larger regions.

---

#### Knob 3 — Offset V
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Offset V adds a vertical component to the derivation by blending the current line with a vertically offset read of the line buffer.  At zero, derivation is purely horizontal.  Increasing Offset V introduces vertical edge sensitivity, producing a more isotropic (direction-independent) edge map.

---

#### Knob 4 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Threshold sets a minimum level below which the derived signal is zeroed.  This removes low-amplitude noise and weak edges, leaving only strong contours.  At zero all edges pass through; at maximum only the hardest transitions survive.  Useful for cleaning up noisy camera sources.

---

#### Knob 5 — Feedback
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Feedback controls how much of the processed output is fed back into the derivation chain's input.  At zero there is no feedback; the derivation sees only the source.  Increasing Feedback produces progressive edge reinforcement — at moderate levels, edges become crisp and haloed; at high levels, the image dissolves into ringing oscillation.

---

#### Knob 6 — Color Tint
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

Color Tint rotates the hue of the chrominance output.  This shifts the colour cast of the processed image through the entire spectrum.  Combined with the derivation and feedback, Colour Tint can produce vivid chromatic edge glows — green edges on a magenta field, cyan halos on an orange ground.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Derive** | Edge | Color |
| **8 — Math** | Multiply | Divide |
| **9 — Cascade** | Single | Double |
| **10 — Clamp** | Wrap | Saturate |
| **11 — Bypass** | Off | On |

Derive selects the derivation type (edge, offset, invert, or colour).  Math selects the cross-modulation mode.  Cascade doubles the chain.  Clamp handles overflow.  Bypass passes through.  The most creative toggle is Cascade — doubling the derivation chain transforms the effect from a first-order edge enhancer into a second-order texture analyser, revealing fine detail that the single stage misses.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the wet derived/modulated output.





---

## Guided Exercises

These exercises explore the Sandin IP's signal derivation chain, from clean edge enhancement to abstract feedback textures.

### Exercise 1: Clean Edge Enhancement

<BeforeAfterSlider
  sources={[
    { label: "House", before: sandin_source1_house, after: sandin_ex1_s1 },
    { label: "Ballerina", before: sandin_source2_ballerina, after: sandin_ex1_s2 },
    { label: "Turtle", before: sandin_source3_turtle, after: sandin_ex1_s3 },
    { label: "Pattern", before: sandin_source4_pattern, after: sandin_ex1_s4 },
    { label: "Man", before: sandin_source5_man, after: sandin_ex1_s5 },
    { label: "Knit", before: sandin_source6_knit, after: sandin_ex1_s6 },
  ]}
/>
*Clean Edge Enhancement — simulated result across source images.*
**Source**: A camera source with well-defined subjects — faces, text, or architecture.

**What You'll Create**: Enhance edges while preserving recognisable image structure.

1. Set Derive to Edge mode, Derive Amt to 40 %.
2. Set Offset H to 10 %, Offset V to 5 % for a slight spatial derivative.
3. Set Math to Multiply to brighten edges in light areas.
4. Set Threshold to 20 % to suppress noise.
5. Observe clean edge contours overlaid on the source.
6. Increase Derive Amt to see the image shift from enhancement to abstraction.

**Key concepts**: - Edge derivation computes horizontal luminance differences
- Multiply mode reveals edges proportionally to scene brightness
- Threshold removes weak, noisy edges

---

### Exercise 2: Feedback Oscillation

<BeforeAfterSlider
  sources={[
    { label: "House", before: sandin_source1_house, after: sandin_ex2_s1 },
    { label: "Ballerina", before: sandin_source2_ballerina, after: sandin_ex2_s2 },
    { label: "Turtle", before: sandin_source3_turtle, after: sandin_ex2_s3 },
    { label: "Pattern", before: sandin_source4_pattern, after: sandin_ex2_s4 },
    { label: "Man", before: sandin_source5_man, after: sandin_ex2_s5 },
    { label: "Knit", before: sandin_source6_knit, after: sandin_ex2_s6 },
  ]}
/>
*Feedback Oscillation — simulated result across source images.*
**Source**: A high-contrast graphic or colour bars.

**What You'll Create**: Push the derivation chain into self-reinforcing feedback oscillation.

1. Set Derive Amt to 70 %, Feedback to 60 %.
2. Set Cascade to Double for second-order derivation.
3. Set Clamp to Wrap to allow overflow ringing.
4. Observe the image dissolving into oscillating ringing patterns.
5. Adjust Threshold to control the onset point of oscillation.
6. Apply Color Tint to shift the ringing into vivid chromatic halos.

**Key concepts**: - Feedback creates recursive edge reinforcement
- Double cascade produces second-order derivatives
- Wrap overflow generates false contours from signal ringing

---

### Exercise 3: Shadow Glow with Divide

<BeforeAfterSlider
  sources={[
    { label: "House", before: sandin_source1_house, after: sandin_ex3_s1 },
    { label: "Ballerina", before: sandin_source2_ballerina, after: sandin_ex3_s2 },
    { label: "Turtle", before: sandin_source3_turtle, after: sandin_ex3_s3 },
    { label: "Pattern", before: sandin_source4_pattern, after: sandin_ex3_s4 },
    { label: "Man", before: sandin_source5_man, after: sandin_ex3_s5 },
    { label: "Knit", before: sandin_source6_knit, after: sandin_ex3_s6 },
  ]}
/>
*Shadow Glow with Divide — simulated result across source images.*
**Source**: A dimly lit scene with strong shadows and some bright highlights.

**What You'll Create**: Create an ethereal glow in shadow regions using Divide cross-modulation.

1. Set Math to Divide and Derive to Invert.
2. Set Derive Amt to 50 %, Feedback to 20 %.
3. Set Color Tint to 90° for cyan-green glow.
4. Observe edges appearing preferentially in dark regions — shadows glow with edge detail.
5. Increase Derive Amt and Feedback to intensify the X-ray effect.

**Key concepts**: - Divide mode brightens edges inversely to source luminance
- Invert derivation produces the complement of the source
- Low-level feedback adds depth without oscillation

---


## Tips

- **Wrap for controlled chaos:** Wrap overflow mode produces the wild false-colour ringing that is characteristic of pushed analogue circuits — use it deliberately, not accidentally.
- **Color Tint for drama:** A strong hue rotation on edge-enhanced video creates chromatic contours that pop against the neutral source.
- **Low Feedback + high Derive:** This combination produces clean, poster-like edge maps with no oscillation risk — ideal for graphic design or VJ work.
- **Chain with Wobbulator:** Feeding Sandin's edge-enhanced output into Wobbulator's warp creates organic, flow-like distortions that follow the image's contour structure.

---
