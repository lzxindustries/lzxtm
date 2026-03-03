---
draft: true
sidebar_position: 144
slug: /instruments/videomancer/inferno
title: "Inferno"
image: /img/instruments/videomancer/inferno/inferno_hero.png
description: "Fire is one of the oldest and most beloved effects in the demoscene — the underground computer art movement that emerged in the 1980s alongside cracking groups and BBS culture."
---

import inferno_hero from '/img/instruments/videomancer/inferno/inferno_hero.png';
import inferno_animation from '/img/instruments/videomancer/inferno/inferno_animation.gif';
import inferno_control_panel from '/img/instruments/videomancer/inferno/inferno_control_panel.png';
import inferno_exercise1_result from '/img/instruments/videomancer/inferno/inferno_exercise1_result.gif';
import inferno_exercise2_result from '/img/instruments/videomancer/inferno/inferno_exercise2_result.gif';
import inferno_exercise3_result from '/img/instruments/videomancer/inferno/inferno_exercise3_result.gif';

# Inferno

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={inferno_hero} alt="Inferno hero image"/>
*Inferno generating a classic demoscene fire simulation with scanline propagation, cooling gradients, and the Classic red-orange-yellow palette.*
<img src={inferno_animation} alt="Inferno animated output"/>
*Inferno output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Fire is one of the oldest and most beloved effects in the demoscene — the underground computer art movement that emerged in the 1980s alongside cracking groups and BBS culture. Inferno recreates this iconic algorithm in real-time FPGA hardware. A grid of temperature values is maintained in registers. Each frame, the bottom row is seeded with random heat and every cell propagates upward, averaging its three neighbors below and subtracting a cooling factor. The resulting temperature values are mapped through a 64-entry color palette to produce the final image: black at the base cools through deep reds to oranges, yellows, and white at the hottest points.

The name *Inferno* refers both to the Latin word for a great fire and to the first canticle of Dante's *Divine Comedy*, where the poet descends through nine circles of increasingly intense flame. Here, the "descent" is inverted — fire rises from the bottom of the screen, cooling as it climbs. Four selectable palettes — Classic (red-orange-yellow), Blue (blue-cyan-white), Green (green-yellow-green-white), and Purple (purple-magenta-pink-white) — offer distinct visual moods from the same underlying simulation.

At conservative settings — moderate intensity, low turbulence, no wind — Inferno produces a gentle, flickering hearth fire. Increasing intensity fills the screen with white-hot heat. Raising turbulence adds chaotic cooling variation, making the flames jagged and unpredictable. Wind tilts the flames laterally. At extreme settings, the entire screen becomes a roiling mass of color. The optional Video Burn mode adds the input video's luminance to the fire output, creating a composite where real footage appears to burn through the synthesized flames.

---

## Background

### The Demoscene Fire Algorithm

The **fire effect** first appeared in the late 1980s as part of the demoscene — a subculture of programmers who created real-time audiovisual demonstrations ("demos") to showcase their technical skills, often on hardware with severe limitations like the Commodore 64, Amiga, and early PCs. The core algorithm is deceptively simple: maintain a 2D buffer of temperature values, seed the bottom row with random hot values, and propagate upward by averaging neighbors and subtracting a cooling constant. Map the resulting temperature through a color gradient and display. The effect runs at interactive frame rates because it requires only additions and shifts — no multiplication, no floating-point math. Inferno adapts this algorithm to FPGA hardware, running at 74.25 MHz clock rate.

### Temperature Propagation and Cooling

Each cell in the fire grid is updated once per frame during the vertical blanking interval. The new temperature for a cell is computed by averaging three neighbors (the cell directly below and its two horizontal neighbors), then subtracting a cooling value. The cooling determines how quickly the fire dies as it rises — low cooling produces tall, towering flames that reach the top of the screen; high cooling produces short, stubby flames that barely clear the base. In the VHDL implementation, the "average" uses a right-shift by 1 (dividing by 2) rather than dividing by 3, which makes the sum slightly hotter than a true average and produces visually fuller flames.

### LFSR-Based Turbulence

A **Linear Feedback Shift Register** (LFSR) generates pseudo-random noise at hardware speed without requiring a multiplier or memory lookup. Inferno uses a 16-bit LFSR seeded at 0xACE1 to produce two sources of randomness: the heat values for the bottom-row seed, and the turbulence added to the cooling factor. When turbulence is active, random bits from the LFSR are added to the cooling value, causing irregular attenuation that makes the flames jitter and flicker rather than decaying smoothly.

### Palette Mapping

Each temperature value (0–63) indexes a 64-entry lookup table of YUV color constants, computed at FPGA synthesis time. The four palettes trace different color trajectories through the YUV color space, all starting at black (Y=0, neutral chroma) and ending at white (Y=1023, neutral chroma). The Classic palette passes through dark red → red → orange → yellow → white, following the chromaticity of incandescent thermal emission. The Blue palette follows blue → cyan → white, evoking natural gas or chemical flames. Green and Purple palettes are purely aesthetic departures.

### Video Burn Compositing

In Video Burn mode, the input video's luminance channel is added (at half intensity) to the fire output. This creates a layered composite: bright areas of the source video appear to glow through the fire, while dark areas are dominated by the flame simulation. The addition is clamped at 1023 to prevent overflow. This mode transforms Inferno from a pure synthesis program into a hybrid processing/synthesis effect.


---

## Signal Flow

```
Fire Simulation Engine (per-frame, during blanking)
│
├── 1. Seed Bottom Row       (LFSR random heat, clamped by Intensity)
├── 2. Propagate Upward      (avg 3 neighbors − cooling ± turbulence)
│      └─ Wind shifts neighbor column indices ±1
│
Active Video Readout Pipeline
│
├── 3. Coordinate Quantize    (hcount/vcount → fire grid column/row
│      + LFSR jitter for lateral variation)
├── 4. Temperature Read       (6-bit value from fire grid)
├── 5. Palette Lookup         (temp → Y, U, V from selected palette)
├── 6. Brightness Scale       (Y × Brightness register / 1024)
├── 7. Video Burn             (optional: add half of input luma)
├── 8. Registered Output
│
├── Interpolator (wet/dry mix) ─────────────────────────────────
│   └─ 4 clocks per channel: crossfade between input and fire
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select input or fire output
```

The fire simulation and the video readout pipeline operate in different phases of the frame. Fire propagation runs during the vertical blanking interval — the update state machine iterates through all 4 columns × 68 rows, seeding the bottom row (or top row in inverted mode) and propagating cell by cell. During active video, pixel coordinates are quantized to the coarse fire grid and the temperature at that grid cell is looked up, palette-mapped, and brightness-scaled. Because the grid is only 4 columns wide, horizontal pixels are hashed into one of the 4 columns with LFSR-based jitter, creating lateral variation from the small data set.

---

## Parameter Reference

<img src={inferno_control_panel} alt="Videomancer front panel with Inferno loaded"/>
*Videomancer's front panel with Inferno active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Intensity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the heat injected into the seed row at the bottom of the fire grid (or top, when inverted). At low values, the LFSR-generated random heat is clamped to a low ceiling, producing sparse, cool flames that barely register. Above 50%, the seed saturates at maximum heat (63), filling the base with white-hot values that propagate upward as tall, bright flames. This is the primary control for flame height and overall visual energy.

---

#### Knob 2 — Cooling
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Sets the base cooling factor subtracted from each cell during upward propagation. At zero, flames rise unattenuated to the top of the screen — the entire display fills with hot colors. At high values, each row of propagation strips away more heat, producing short flames confined to the lower portion of the screen. Cooling interacts multiplicatively with Turbulence: when both are high, the flames become chaotic and very short.

---

#### Knob 3 — Turbulence
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Adds random variation to the cooling factor via LFSR noise bits. At zero, cooling is uniform and the flames decay smoothly. As Turbulence increases, random noise is added to the cooling value, causing some cells to cool faster than their neighbors. This breaks the smooth propagation into jagged, flickering tongues. The visual effect resembles the random air currents that make real fire unpredictable.

---

#### Knob 4 — Wind
| Property | Value |
|----------|-------|
| Range | -90deg – 90deg |
| Default | 0deg |
| Suffix | deg |

Shifts the neighbor column selection used during propagation, tilting the flames laterally. At center, the three-neighbor average uses the cell directly below and its immediate left and right neighbors — fire propagates straight up. Moving the control away from center shifts the neighbor indices left or right by one column, causing the fire to lean in that direction. The effect simulates wind blowing across the flames.

---

#### Knob 5 — Spread
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

This control is registered in the VHDL as `s_flame_width` but is not connected to any processing stage. Adjusting it has no visible effect on the output. The register is mapped and the signal exists in hardware, but no downstream logic reads it. A future firmware revision may implement horizontal spread control.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the luminance component of the palette-mapped output. The palette lookup produces a base Y value, which is then multiplied by this control and right-shifted by 10, effectively scaling brightness from 0% to ~100%. At low values, the fire appears dim and deep-colored. At high values, the fire is bright and the palette's full dynamic range is visible. This control does not affect chrominance — only the luminance channel is scaled.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Classic | Blue |
| **8 — Direction** | Up | Down |
| **9 — Video Burn** | Off | On |
| **10 — Resolution** | Coarse | Fine |
| **11 — Bypass** | Off | On |

Switches 7–11 are not all independent binary options. Switch 7 (Palette) is a **2-bit selector** occupying bits 0 and 1 of the toggle register, providing four palette choices. Switch 8 (Direction) occupies bit 3. Switch 9 (Video Burn) occupies bit 2. Switch 10 (Resolution) is mapped but not implemented in the VHDL. Switch 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfade between the dry (input) signal and the wet (fire) signal. At 0% the output is entirely the unprocessed input. At 100% the output is entirely the fire synthesis. Intermediate values blend the two, creating a translucent fire overlay on the input video — distinct from Video Burn mode, which adds luma rather than crossfading.

---

## Guided Exercises

These exercises progress from a basic fire to full creative control with palette selection, wind, inversion, and video compositing.

### Exercise 1: Classic Campfire

<img src={inferno_exercise1_result} alt="Classic Campfire result"/>
*Classic Campfire — simulated result across source images.*
**Objective**: Learn how Intensity, Cooling, and Brightness interact to shape the basic fire.

1. **Ignite**: With Intensity at ~75% and Cooling at ~35%, observe the fire rising from the bottom of the screen — tongues of flame in the Classic palette.
2. **Cooling sweep**: Slowly increase Cooling. Watch the flames shorten as more heat is stripped per row. At very high cooling, only a thin band of embers remains at the base.
3. **Intensity sweep**: Return Cooling to ~35%. Increase Intensity to maximum. The fire fills the screen — nearly every pixel is hot.
4. **Brightness**: Lower Brightness to ~40%. The fire dims without changing its height or shape — colors shift toward deeper, richer hues.
5. **Balance**: Find a setting where the fire has visible structure: tall enough to show the full palette gradient, bright enough to read the colors, with enough cooling to create gaps and variation.

**Key concepts**: Intensity seeds the base row heat, Cooling determines flame height, Brightness scales luminance without altering simulation behavior

---

### Exercise 2: Turbulent Wind Fire

<img src={inferno_exercise2_result} alt="Turbulent Wind Fire result"/>
*Turbulent Wind Fire — simulated result across source images.*
**Objective**: Explore turbulence and wind for dynamic, asymmetric flames.

1. **Prepare**: Start from the Exercise 1 campfire (Intensity ~75%, Cooling ~35%).
2. **Add turbulence**: Slowly increase Turbulence. The smooth flame edges become jagged and flickering — random LFSR noise disrupts the regular decay pattern.
3. **Wind right**: Turn Wind clockwise. The flames lean to one side, as if blown by a horizontal breeze. The neighbor column lookup shifts, pulling heat from one direction.
4. **Wind left**: Turn Wind counter-clockwise past center. The flames lean the other direction.
5. **Palette switch**: Try the Blue palette (Switch 7). The same turbulent, wind-blown simulation now appears as ghostly blue flames.
6. **Green palette**: Switch again. Each palette applies a completely different color trajectory to the same temperature data.

**Key concepts**: Turbulence adds LFSR noise to cooling, Wind shifts neighbor columns for lateral lean, palette selection recolors the same simulation data

---

### Exercise 3: Inverted Video Burn

<img src={inferno_exercise3_result} alt="Inverted Video Burn result"/>
*Inverted Video Burn — simulated result across source images.*
**Objective**: Combine inverted fire direction with video burn compositing for a dramatic layered effect.

1. **Invert**: Switch Direction to Down (Switch 8). The fire now falls from the top of the screen, like molten material dripping downward.
2. **Adjust**: Set Intensity to ~80% and Cooling to ~30% to ensure the inverted fire has enough height to reach mid-screen.
3. **Video Burn**: Enable Video Burn (Switch 9). Input video luminance begins to glow through the flames — bright objects in the video punch through as highlights.
4. **Purple palette**: Switch to the Purple palette for a surreal, magenta-tinted overlay.
5. **Mix sweep**: Pull Mix down to ~60%. The fire overlay becomes translucent — the input video is visible underneath with purple fire cascading from above.
6. **Turbulence**: Add moderate turbulence (~40%) to break the flames into smaller, more chaotic tongues. The video burn highlights flicker with the fire.

**Key concepts**: Inverted mode seeds the top row instead of bottom, Video Burn adds input luma to fire output (not crossfade), Mix crossfades between dry input and processed fire

---


## Tips

- **Intensity is the master valve**: Below ~50%, the fire is sparse and dim. Above ~75%, the screen fills with flame. Start at ~75% and adjust Cooling to shape the flame height.
- **Cooling controls flame height**: Think of Cooling as the atmosphere above the fire — high cooling = cold air that quenches flames quickly, giving short fire. Low cooling = still, warm air that lets flames rise.
- **Turbulence needs Cooling to be visible**: At zero Cooling, everything is max heat regardless of turbulence noise. Set moderate Cooling first, then add Turbulence for the jagged, flickering quality.
- **Video Burn vs. Mix**: These are different operations. Mix crossfades between input and fire (linear blend). Video Burn *adds* input luma to fire output (additive composite). They can be used simultaneously — Video Burn composites the video into the fire, then Mix controls how much of that composite appears in the output.
- **Spread and Resolution are placeholders**: Knob 5 and Switch 10 are registered but have no effect. The fire resolution is fixed at 4×68.
- **Palette is post-simulation**: Switching palettes changes colors without affecting the simulation — you can switch mid-performance with no discontinuity in flame behavior.
- **Feedback loops**: Routing Inferno's output back to its input with Video Burn enabled creates recursive fire — each frame's fire adds to the previous, building toward saturation.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed input for before/after comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **Blanking Interval** | The period between active video frames when no pixels are displayed; used here for fire grid propagation. |
| **Compositing** | Combining two image layers into one; Video Burn mode uses additive compositing. |
| **Demoscene** | A computer art subculture originating in the 1980s, focused on creating real-time audiovisual demonstrations. |
| **Elaboration** | The FPGA synthesis stage where constant values (like palette tables) are computed and embedded as fixed logic. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip executing the video processing pipeline. |
| **Interpolator** | A crossfade module that linearly blends between two signals based on a mix coefficient. |
| **LFSR** | Linear Feedback Shift Register; a hardware-efficient pseudo-random number generator using XOR feedback taps. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Palette** | A lookup table mapping temperature index values to specific Y, U, V color constants. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next on each clock cycle. |
| **Propagation** | The per-frame process of updating each fire grid cell from its neighbors, simulating heat transfer. |
| **Quantization** | Here, reducing screen coordinates to the coarse fire grid resolution (1920×1080 → 120×68 equivalent). |
| **Temperature** | A 6-bit unsigned value (0–63) stored per fire grid cell, representing heat intensity. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
