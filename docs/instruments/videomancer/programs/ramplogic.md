---
draft: true
sidebar_position: 241
slug: /instruments/videomancer/ramplogic
title: "Ramp Logic"
image: /img/instruments/videomancer/ramplogic/ramplogic_hero.png
description: "Ramplogic builds its imagery entirely from the horizontal and vertical pixel counters of the video raster."
---

import ramplogic_hero from '/img/instruments/videomancer/ramplogic/ramplogic_hero.png';
import ramplogic_animation from '/img/instruments/videomancer/ramplogic/ramplogic_animation.gif';
import ramplogic_control_panel from '/img/instruments/videomancer/ramplogic/ramplogic_control_panel.png';
import ramplogic_exercise1_result from '/img/instruments/videomancer/ramplogic/ramplogic_exercise1_result.gif';
import ramplogic_exercise2_result from '/img/instruments/videomancer/ramplogic/ramplogic_exercise2_result.gif';
import ramplogic_exercise3_result from '/img/instruments/videomancer/ramplogic/ramplogic_exercise3_result.gif';

# Ramp Logic

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<img src={ramplogic_hero} alt="Ramp Logic hero image"/>
*Eight ramp-logic operators tile the screen with saw-tooth and triangle waveform patterns — crisp geometric testcard geometry built from horizontal and vertical pixel counters alone.*
<img src={ramplogic_animation} alt="Ramp Logic animated output"/>
*Ramp Logic output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Ramplogic builds its imagery entirely from the horizontal and vertical pixel counters of the video raster.  No framebuffer is needed — every pixel's value is computed combinatorially from its screen coordinates, the selected frequency, and one of eight mathematical operators.  The result is a family of geometric test-card patterns: diagonal stripes, moire grids, radial starbursts, and checkerboard fields, all generated in real time with zero latency.

The program revives a core technique of early analogue video synthesis, where horizontal and vertical ramp generators — sawtooth waveforms locked to the scan — were combined through voltage comparators and logic gates to produce abstract imagery.  The Sandin Image Processor and ETC's Direct Video Synthesiser used precisely this approach.  Ramplogic implements eight operators: sum, difference, product, XOR, maximum, minimum, AND, and OR.  Each combines the H and V ramp signals in a different way, producing distinct visual characters.

The Freq H and Freq V knobs set the spatial frequency of the ramps — effectively the number of "teeth" across the screen in each direction.  Threshold clips the result against a comparator, converting smooth gradients into hard-edged binary shapes.  Phase offsets the ramp starting point, scrolling the pattern across the screen.  The Animate toggle routes the DDS phase accumulator into the ramp counters, making the pattern drift continuously.

---

## Quick Start

1. **XOR for fractals:** The XOR operator is uniquely powerful — it produces self-similar fractal patterns from simple ramp counters, a property of binary arithmetic that was a foundational discovery in early digital art.
2. **Equal frequencies for symmetry:** Setting Freq H = Freq V produces axis-symmetric patterns; any asymmetry tilts or stretches the geometry.
3. **Threshold as sculptor:** Think of Threshold as sculpting a 3D landscape — the operator output is a height map, and Threshold sets the water level.

---

## Background

### Ramp Generators in Analogue Synthesis

In analogue video synthesis, a ramp generator produces a sawtooth wave synchronised to horizontal or vertical sync.  The H ramp rises from 0 V to peak once per scan line; the V ramp rises once per field.  By combining these two ramps through comparators, summing amplifiers, and logic gates, a synthesist can build geometric patterns without any memory or signal source.  This is the most fundamental form of video synthesis — imagery from raw timing alone.

### Combinatorial Operators

Ramplogic offers eight ways to combine the H and V ramps:
- **Sum**: `H + V` — diagonal gradient, 45° stripes
- **Difference**: `|H − V|` — V-shaped chevrons
- **Product**: `H × V` — hyperbolic curves, moire
- **XOR**: `H ⊕ V` — Sierpinski-like fractal checkerboard
- **Maximum**: `max(H, V)` — diamond highlight
- **Minimum**: `min(H, V)` — diamond shadow
- **AND**: `H & V` — rectangular grid intersections
- **OR**: `H | V` — broad rectangular fills

### Threshold Comparator

The threshold comparator converts the continuous operator output into a binary black-or-white pattern.  Values above the threshold become white; below become black.  Sweeping the threshold over a gradient slices the pattern at different levels, revealing internal contours.  When the operator output is XOR or product, the threshold cuts through fractal-like structures, producing evolving families of shapes.

### Colour Keying

The Color knob and the two-colour keying system assign distinct hues to the above-threshold and below-threshold regions.  At 50 % the output is monochrome black-and-white; rotating Color shifts the "white" key colour through the spectrum while the "black" regions remain dark.  This produces bold, poster-like images with strong graphic impact.

### Animation via DDS

When Animate is enabled, an internal DDS phase accumulator adds a continuously incrementing offset to the H and V ramp counters.  The pattern scrolls diagonally (or in whatever direction the operator geometry implies), creating a kinetic version of the static test-card image.  Phase sets the starting offset; the animation speed is proportional to the DDS increment rate.


---

## Signal Flow

```
   ┌────────────────┐    ┌────────────────┐
   │  H Ramp Counter │    │  V Ramp Counter │
   │  × Freq H       │    │  × Freq V       │
   └───────┬────────┘    └───────┬────────┘
           │                     │
           │   ┌─────────────┐   │
           └──►│  Operator    │◄──┘
               │ (8 modes)   │
               └──────┬──────┘
                      │
           ┌──────────▼──────────┐
           │  Threshold Compare   │
           │  (smooth / hard)     │
           └──────────┬──────────┘
                      │
           ┌──────────▼──────────┐
           │  Colour Key Mapping  │
           │  (above → colour,    │
           │   below → black)     │
           └──────────┬──────────┘
                      │
           ┌──────────▼──────────┐
           │   Interpolator Mix   │
           │   (dry / wet fader)  │
           └──────────┬──────────┘
                      │
                   Output Y/U/V
```

Everything is combinatorial — the operator output is computed fresh for every pixel from the position counters, with no memory dependency.  This means latency is minimal (one multiply/add cycle plus the threshold compare) and the pattern cannot accumulate artefacts over time.  The sawtooth/triangle toggle selects whether the ramp counters produce a one-directional sawtooth or a bidirectional triangle wave; triangle produces mirror-symmetric patterns.

The Combine toggle provides a secondary logical operation between two instances of the primary operator — one at the base frequency and one at double frequency — producing layered interference patterns.

---

## Parameter Reference

<img src={ramplogic_control_panel} alt="Videomancer front panel with Ramp Logic loaded"/>
*Videomancer's front panel with Ramp Logic active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Func Select
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 1 |

Func Select cycles through the eight operators: sum, difference, product, XOR, max, min, AND, OR.  Each operator produces a fundamentally different geometric character.  Sum produces diagonal stripes; XOR produces fractal checkerboards; product produces hyperbolic curves.  The 8-step quantisation means each knob position selects a cleanly defined operator with no interpolation between modes.

---

#### Knob 2 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Threshold sets the comparator level that slices the continuous operator output into black and white.  At 50 %, the pattern is evenly split.  Low threshold values let most of the image through as white; high values suppress most of the image to black.  Sweeping threshold across a complex operator like product reveals evolving families of contour lines within the pattern.

---

#### Knob 3 — Freq H
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Freq H sets the horizontal spatial frequency — the number of ramp periods across one scan line.  Low values produce wide stripes; high values produce narrow, tightly packed lines.  Because the ramp counter wraps at the frequency boundary, increasing Freq H multiplies the number of pattern repetitions horizontally.

---

#### Knob 4 — Freq V
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Freq V sets the vertical spatial frequency.  Combined with Freq H, this controls the aspect ratio of the patterns.  Equal H and V frequencies produce square-symmetric patterns; unequal frequencies produce elongated or compressed geometries.

---

#### Knob 5 — Phase
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

Phase offsets the starting point of both ramp counters, shifting the pattern's position on screen.  In static mode this translates the pattern left/right and up/down.  When Animate is enabled, Phase sets the initial position from which the animated scroll begins.

---

#### Knob 6 — Color
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 90d |
| Suffix | d |

Color shifts the hue of the above-threshold key colour.  At zero the output is monochrome white-on-black.  Rotating Color moves the key through the colour wheel — red, yellow, green, cyan, blue, magenta — producing bold, poster-like two-colour images.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Combine** | AND | XOR |
| **8 — Polarity** | Normal | Invert |
| **9 — Animate** | Off | On |
| **10 — Video Mod** | Off | On |
| **11 — Bypass** | Off | On |

Combine and Polarity alter the mathematical pipeline.  Animate enables kinetic scrolling.  Video Mod reintroduces source video.  Bypass passes through clean.  The most transformative toggle is Func Select (the knob), but among the toggles, Combine has the greatest impact — doubling the pattern complexity instantly through frequency-doubled overlay.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the wet ramp-logic output.  At zero, pure source; at maximum, pure ramp-logic patterns.





---

## Guided Exercises

These exercises demonstrate the eight operator modes and the visual vocabulary of ramp-logic synthesis, from simple stripes to complex fractal lattices.

### Exercise 1: Diagonal Stripes via Sum

<img src={ramplogic_exercise1_result} alt="Diagonal Stripes via Sum result"/>
*Diagonal Stripes via Sum — simulated result across source images.*
**What You'll Create**: Generate clean 45° diagonal stripes using the sum operator.

1. Set Func Select to the first position (Sum).
2. Set Freq H and Freq V to 40 % for moderate stripe density.
3. Set Threshold to 50 % for even black/white split.
4. Observe the 45° diagonal stripe pattern.
5. Adjust Freq H independently to tilt the stripes — unequal frequencies change the angle.
6. Rotate Color to shift the stripe colour from white to green, blue, etc.

**Key concepts**: - Sum operator adds H and V ramps → diagonal gradient
- Equal H/V frequencies → exactly 45° angle
- Threshold at 50 % produces even stripe width

---

### Exercise 2: XOR Fractal Checkerboard

<img src={ramplogic_exercise2_result} alt="XOR Fractal Checkerboard result"/>
*XOR Fractal Checkerboard — simulated result across source images.*
**What You'll Create**: Produce a Sierpinski-triangle-like fractal pattern using XOR.

1. Set Func Select to step 4 (XOR).
2. Set Freq H and Freq V to 50 % for dense grid.
3. Set Threshold to 50 %.
4. Observe the fractal checkerboard pattern — nested self-similar squares.
5. Enable Combine (AND mode) to overlay a double-frequency XOR grid, creating even more intricate fractal detail.
6. Toggle Polarity to swap black/white and see the complementary pattern.

**Key concepts**: - XOR of ramp counters produces Sierpinski-like fractal geometry
- Combine overlays two XOR patterns at different frequencies
- The fractal structure arises naturally from binary arithmetic

---

### Exercise 3: Animated Moire with Video Mod

<img src={ramplogic_exercise3_result} alt="Animated Moire with Video Mod result"/>
*Animated Moire with Video Mod — simulated result across source images.*
**What You'll Create**: Create a scrolling moire pattern modulated by the input video.

1. Set Func Select to step 3 (Product).
2. Set Freq H to 60 %, Freq V to 45 % for asymmetric moire.
3. Enable Animate and set Phase to 20 %.
4. Enable Video Mod — the moire pattern appears preferentially in bright regions of the source.
5. Adjust Threshold to control how much of the source is "filled" with the pattern.
6. Set Mix to 70 % to blend the patterned video with the clean source.

**Key concepts**: - Product operator creates hyperbolic moire curves
- Animate scrolls the pattern continuously
- Video Mod uses source luminance as a spatially varying threshold

---


## Tips

- **Animate for kinetics:** Even slow animation transforms static patterns into hypnotic, scrolling visual music — pair with a slow Threshold sweep for maximum evolution.
- **Video Mod for compositing:** Video Mod effectively "stamps" the ramp pattern onto the source video, creating a graphic overlay effect without needing a separate keyer.
- **Product for moire:** The product operator is the fastest route to moire interference patterns — the hyperbolic curves create beating frequencies as Freq H and Freq V approach each other.
- **Chain with other effects:** Ramplogic's hard-edged output is an ideal key source — feed it into another program's Video Mod input to use geometric patterns as a control signal.

---
