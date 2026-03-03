---
draft: true
sidebar_position: 71
slug: /instruments/videomancer/cymatics
title: "Cymatics"
image: /img/instruments/videomancer/cymatics/cymatics_hero.png
description: "Cymatics synthesises the standing-wave patterns that form on vibrating liquid surfaces — concentric rings expanding from point sources, colliding, reinforcing at nodes, and focusing into bright caustic lines."
---

import cymatics_hero from '/img/instruments/videomancer/cymatics/cymatics_hero.png';
import cymatics_animation from '/img/instruments/videomancer/cymatics/cymatics_animation.gif';
import cymatics_control_panel from '/img/instruments/videomancer/cymatics/cymatics_control_panel.png';
import cymatics_exercise1_result from '/img/instruments/videomancer/cymatics/cymatics_exercise1_result.gif';
import cymatics_exercise2_result from '/img/instruments/videomancer/cymatics/cymatics_exercise2_result.gif';
import cymatics_exercise3_result from '/img/instruments/videomancer/cymatics/cymatics_exercise3_result.gif';

# Cymatics

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={cymatics_hero} alt="Cymatics hero image"/>
*Concentric ripples from drifting wave sources collide and focus, tracing the nodal geometries of vibrating liquid surfaces.*
<img src={cymatics_animation} alt="Cymatics animated output"/>
*Cymatics output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Cymatics synthesises the standing-wave patterns that form on vibrating liquid surfaces — concentric rings expanding from point sources, colliding, reinforcing at nodes, and focusing into bright caustic lines. The program is inspired by Hans Jenny's phonodeik experiments of the 1960s, in which he photographed sand, paste, and water vibrating on metal plates to reveal the geometry hidden inside sound.

Up to four wave sources drift slowly across the screen, each emitting concentric sine-wave rings whose spacing is set by the Frequency knob. Where waves from different sources arrive in phase, constructive interference creates bright peaks; where they cancel, dark nodal lines form. A Caustic toggle brightens the constructive peaks further, simulating the optical focusing effect seen in sunlight through shallow water.

Two surface modes change the visual character: Water shows both positive and negative wave displacement (bright peaks and dark troughs), while Mercury takes the absolute value, producing a symmetric double-frequency pattern reminiscent of vibrating metallic fluid. When Video Seed is engaged, the accumulated wave sum is multiplied by the input luminance, letting external imagery texture the interference field.

---

## Background

### Hans Jenny and Cymatics

Swiss physician Hans Jenny spent decades vibrating plates, membranes, and liquid surfaces at controlled frequencies, photographing the resulting standing-wave patterns. His 1967 book *Cymatics* documented concentric rings, radial star patterns, and chaotic turbulence, all arising from simple sinusoidal excitation. This program reproduces the concentric-ring interference computationally.

### Wave Interference and Nodal Lines

When two circular waves from different sources overlap, the resulting amplitude at any point is the sum of the individual wave values. Points where both waves have the same sign produce constructive interference (bright); where they have opposite sign, destructive interference (dark). The loci of zero amplitude — nodal lines — form beautiful hyperbolic curves between the sources.

### Caustic Focusing

In physical optics a caustic is an envelope of light rays, creating bright concentrated lines where many rays converge. In the context of water waves, a caustic appears where the wave amplitude is exceptionally high due to constructive focus. Cymatics simulates this by detecting peak amplitude and additively brightening those pixels.

### Manhattan Distance Approximation

The FPGA computes distance from each pixel to each source using Manhattan distance (|Δx| + |Δy|) rather than Euclidean distance. This is a common FPGA simplification that uses no multipliers. The resulting "circular" waves are actually diamond-shaped, but at screen scale and with multiple interfering sources the visual difference is subtle.

### DDS Source Drift

Each source's (x, y) position is driven by a pair of DDS phase accumulators whose rates differ by small prime-number offsets (37, 53, etc.), ensuring no two sources follow the same path. The sources trace slow Lissajous-like orbits across the screen, continuously changing the interference pattern.


---

## Signal Flow

```
                     ┌──────────────────────────┐
   Drift DDS ×4 ───▸│  Source positions (x, y)  │
                     └──────────┬───────────────┘
                                │ 4 sources
              for each source:  │
                                ▼
          ┌──────────────────────────────────────┐
          │  dist = |px - src_x| + |py - src_y|  │
          │  phase = dist × wavelength + time     │
          │  wave = sine_LUT(phase)               │
          │  attenuation by damping               │
          └──────────────────┬───────────────────┘
                             │ v_sum (accumulate)
                             ▼
          ┌──────────────────────────────────────┐
          │  Video Seed: v_sum × input luma      │
          │  Amplitude scaling                   │
          │  Surface: Water (signed) / Plate (|x|)│
          │  Caustic brightening                 │
          └──────────────────┬───────────────────┘
                             │ Y, U, V wet
                             ▼
              ┌─────────────────────────┐
    dry ─────▸│  interpolator mix       │──▸ data_out
              └─────────────────────────┘
```

The wave sum is accumulated in a 13-bit signed variable to avoid clipping during multi-source addition. After the loop, amplitude scaling and optional video-seed modulation are applied. The caustic brightener detects peaks where the absolute sum exceeds a threshold and adds extra brightness. Colour is derived by XOR-ing the unsigned wave sum with the Hue register, creating a pseudo-palette effect that shifts dramatically with wave height.

---

## Parameter Reference

<img src={cymatics_control_panel} alt="Videomancer front panel with Cymatics loaded"/>
*Videomancer's front panel with Cymatics active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Frequency
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

**Frequency** sets the wavelength of the concentric rings — the spatial distance between successive wave crests emitted by each source. Low values produce widely spaced rings; high values create fine gratings that interfere into dense textures.

---

#### Knob 2 — Amplitude
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**Amplitude** scales the overall wave brightness. At low values the interference pattern is subtle; at high values the constructive peaks clip to white and the destructive troughs clip to black.

---

#### Knob 3 — Damping
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

**Damping** controls how far waves travel before attenuating. Low damping allows waves to reach the screen edges, creating a fully filled interference field. High damping confines the visible ripple pattern to a small region around each source.

---

#### Knob 4 — Sources
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

**Sources** selects the number of active wave emitters from 1 to 4 using a stepped control. One source produces simple concentric rings. Two sources create classic two-slit interference fringes. Three and four sources generate complex nodal lattices.

---

#### Knob 5 — Caustic
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**Caustic** controls the brightness boost applied to constructive interference peaks. At zero, peaks are rendered at normal amplitude. Increasing the control makes the bright focusing lines glow more intensely, simulating optical caustics.

---

#### Knob 6 — Hue
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

**Hue** rotates the colour mapping applied to the wave displacement through 360° of hue angle. The chroma is derived from the wave sum XOR-ed with this register, creating a pseudo-palette effect.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Surface** | Water | Mercury |
| **8 — Symmetry** | Free | Radial |
| **9 — Nodes** | Off | On |
| **10 — Video Seed** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles set the physical analogy and visual style: Surface chooses between two media types (water with signed waves, mercury with absolute-value waves). Symmetry mirrors sources for radial patterns. Nodes enables enhanced dark-line rendering. Video Seed injects external imagery, and Bypass disables the effect.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

**Mix** crossfades between the dry input and the cymatics synthesis. At zero the input passes through; at maximum the output is entirely the interference pattern.

---

## Guided Exercises

These exercises explore Cymatics from simple single-source ripples to complex multi-source caustic fields.

### Exercise 1: Single-Source Ripple Ring

<img src={cymatics_exercise1_result} alt="Single-Source Ripple Ring result"/>
*Single-Source Ripple Ring — simulated result across source images.*
**Objective**: Generate a clean set of concentric rings from a single source and observe wavelength control.

1. Set Frequency to 30 %, Amplitude to 60 %, Damping to 30 %.
2. Set Sources to 1.
3. Caustic 0 %, Hue 0°.
4. Select Water surface, Free symmetry.
5. Nodes Off, Video Seed Off, Bypass Off, Mix 100 %.
6. Observe concentric diamond-shaped rings drifting slowly across the screen.
7. Sweep Frequency to see ring spacing change.

**Key concepts**: Concentric wave emission, wavelength, Manhattan distance diamonds.

---

### Exercise 2: Two-Source Interference Fringes

<img src={cymatics_exercise2_result} alt="Two-Source Interference Fringes result"/>
*Two-Source Interference Fringes — simulated result across source images.*
**Objective**: Create a classic two-slit interference pattern with visible nodal lines.

1. Set Frequency to 40 %, Amplitude to 70 %, Damping to 50 %.
2. Set Sources to 2.
3. Set Caustic to 40 %, Hue to 120°.
4. Select Water surface, Radial symmetry (mirrors source 2).
5. Enable Nodes for enhanced dark lines.
6. Watch the hyperbolic nodal curves form between the two sources.

**Key concepts**: Two-source interference, nodal hyperbolas, constructive/destructive cancellation.

---

### Exercise 3: Caustic Field with Video Seed

<img src={cymatics_exercise3_result} alt="Caustic Field with Video Seed result"/>
*Caustic Field with Video Seed — simulated result across source images.*
**Objective**: Overlay a dense four-source interference field onto source video, using Video Seed to mask the pattern.

1. Set Frequency to 50 %, Amplitude to 80 %, Damping to 40 %.
2. Set Sources to 4.
3. Set Caustic to 70 %, Hue to 240°.
4. Select Mercury surface for maximum density.
5. Enable Video Seed — the pattern appears only in bright source regions.
6. Set Mix to 75 % to retain some dry signal.

**Key concepts**: Multi-source caustic focusing, video-seed masking, Mercury absolute-value mode.

---


## Tips

- **Single source for meditation**: One source with low frequency and high damping produces a gentle pulsing mandala.
- **Near-equal frequencies**: Set two sources with slightly different drift speeds for slowly evolving moiré.
- **Mercury for density**: Mercury mode's absolute value doubles the apparent ring density.
- **Caustic as bloom**: Use Caustic at 30–50 % for subtle glowing peaks without overwhelming the pattern.
- **Video Seed transparency**: At Mix 50 % with Video Seed, the interference field acts as a luminance-dependent overlay.
- **Hue XOR palette**: Because the chroma is derived via XOR, sweeping Hue creates dramatic palette jumps rather than smooth gradients.

---
