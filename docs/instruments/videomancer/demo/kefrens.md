---
draft: true
sidebar_position: 158
slug: /instruments/videomancer/kefrens
title: "Kefrens"
image: /img/instruments/videomancer/kefrens/kefrens_hero.png
description: "Kefrens recreates the classic copper bar effect popularised by the Amiga demoscene group Kefrens in their legendary 1991 demo \"Desert Dream.\" The effect renders multiple horizontal colour bars whose vertical positions are modulated by independent sinusoidal oscillators, producing the characteristic liquid-metal undulation that became a signature of 16-bit demo coding."
---

import kefrens_hero from '/img/instruments/videomancer/kefrens/kefrens_hero.png';
import kefrens_animation from '/img/instruments/videomancer/kefrens/kefrens_animation.gif';
import kefrens_control_panel from '/img/instruments/videomancer/kefrens/kefrens_control_panel.png';
import kefrens_exercise1_result from '/img/instruments/videomancer/kefrens/kefrens_exercise1_result.gif';
import kefrens_exercise2_result from '/img/instruments/videomancer/kefrens/kefrens_exercise2_result.gif';
import kefrens_exercise3_result from '/img/instruments/videomancer/kefrens/kefrens_exercise3_result.gif';

# Kefrens

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={kefrens_hero} alt="Kefrens hero image"/>
*Brightly coloured horizontal bars undulate across the screen in smooth sinusoidal waves, recreating the iconic Amiga demoscene copper bar effect.*
<img src={kefrens_animation} alt="Kefrens animated output"/>
*Kefrens output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Kefrens recreates the classic copper bar effect popularised by the Amiga demoscene group Kefrens in their legendary 1991 demo "Desert Dream." The effect renders multiple horizontal colour bars whose vertical positions are modulated by independent sinusoidal oscillators, producing the characteristic liquid-metal undulation that became a signature of 16-bit demo coding.

The name pays homage to the Danish demo group Kefrens, whose innovative use of the Amiga's copper coprocessor to reprogram palette registers mid-scanline made complex colour bar effects possible on consumer hardware. The copper chip could execute a simple program synchronised to the video beam, changing colours at exact horizontal positions — a technique that defined the visual language of the early demoscene.

In Videomancer's FPGA implementation, up to 8 independent bars are rendered per scanline, each with its own sinusoidal vertical displacement, gradient shading, and palette colour. The bars can mirror horizontally, cascade in rainbow order, and overlay live video input through wet/dry mixing.

---

## Background

### Copper Bars and the Amiga

The Amiga's copper coprocessor was a programmable DMA engine that could write to hardware registers at specific beam positions. Demo coders exploited this to change palette entries multiple times per scanline, creating the illusion of far more simultaneous colours than the hardware officially supported. Copper bars — horizontal stripes of smoothly graduated colour — were among the earliest and most popular demonstrations of this technique, appearing in virtually every Amiga demo from 1987 onward.

### Per-Scanline Sinusoidal Modulation

The vertical position of each bar is determined by evaluating a sine function at a phase offset determined by the bar's index and the global animation counter. This produces smooth wavelike motion: bars slide up and down the screen in interlocking sine curves, occasionally crossing and overlapping. The Frequency knob controls the spatial frequency of the sine wave, while Amplitude controls the displacement range.

### Gradient Shading

Each bar can display either a flat colour or a vertical gradient. In gradient mode the bar's centre is brightest and its edges fade to black, creating a 3D rounded-tube appearance. The gradient is computed as a linear distance from the bar centre, scaled by the Width parameter. This simple shading technique was a hallmark of polished demoscene productions.

### Rainbow Palette Cycling

When rainbow mode is enabled, each bar receives a hue from an 8-colour palette that cycles around the colour wheel. The palette entries are spaced at 45-degree intervals (red, orange, yellow, green, cyan, blue, indigo, violet), and the palette offset advances each frame, so the bars appear to cycle through the spectrum continuously.


---

## Signal Flow

```
 registers_in(0) ── Speed ─────────────────────────────────────────────────┐
 registers_in(1) ── Bars (8 steps) ────────────────────────────────────────┤
 registers_in(2) ── Amplitude ─────────────────────────────────────────────┤
 registers_in(3) ── Frequency ─────────────────────────────────────────────┤
 registers_in(4) ── Width ─────────────────────────────────────────────────┤
 registers_in(5) ── Bright ────────────────────────────────────────────────┤
 registers_in(6) ── Toggles [Gradient|Mirror|Rainbow|ModVid|Bypass] ───────┤
 registers_in(7) ── Mix Fader ─────────────────────────────────────────────┤
                                                                            │
 ┌─────────────────────────────────────────────────────────────────────────┘
 │
 │    ┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
 ├───►│  VBLANK UPDATE   │────►│  PER-SCANLINE   │────►│  BAR SHADING    │
 │    │  advance anim    │     │  for each bar:  │     │  gradient or    │
 │    │  phase counter   │     │  sine position  │     │  flat colour    │
 │    └──────────────────┘     │  distance test  │     │  × brightness   │
 │                             └─────────────────┘     └───────┬─────────┘
 │                                                             │
 │    ┌────────────────────────────────────────────────────┐    │ nearest bar
 │    │   COLOUR COMPOSE                                  │◄───┘ + distance
 │    │   rainbow hue or monochrome                       │
 │    │   mirror mode: abs(y - center)                    │
 │    │   multiply by brightness knob                     │
 │    └──────────────────────────┬─────────────────────────┘
 │                               │
 │    ┌──────────────────┐       │ processed YUV
 └───►│  INTERPOLATOR    │◄──────┘
      │  dry/wet mix     │
      └──────────────────┘
               │
               ▼
          data_out (YUV)
```

Each scanline evaluates all active bars (1–8) in parallel. For each bar, the sine LUT produces a vertical centre position based on the bar's phase offset and the global animation counter. The absolute vertical distance from the current scanline to each bar's centre is compared against the Width parameter — pixels within range are shaded, pixels outside are passed through. When multiple bars overlap at a scanline, their contributions are summed additively.

Mirror mode reflects the bar pattern around the screen's vertical centre, doubling the apparent bar count. The rainbow palette assigns each bar a hue from the 8-entry colour table with indices spaced evenly, so the bars form a spectral sequence. The palette offset advances each frame under the Speed control, creating the animated colour cycling.

---

## Parameter Reference

<img src={kefrens_control_panel} alt="Videomancer front panel with Kefrens loaded"/>
*Videomancer's front panel with Kefrens active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Speed controls the animation rate — how quickly the sine phases advance per frame. At zero the bars are frozen in their current positions. At moderate values they undulate smoothly. At maximum the bars oscillate so rapidly they blur into shimmering horizontal bands.

---

#### Knob 2 — Bars
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

Bars selects the number of active copper bars from 1 to 8. A single bar produces a clean solitary wave. Eight bars fill the screen with interlocking sinusoidal stripes, and their overlapping gradients create complex interference patterns at crossing points.

---

#### Knob 3 — Amplitude
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Amplitude sets the vertical displacement range of the sine modulation. At zero the bars sit at evenly spaced fixed positions. At maximum each bar sweeps nearly the full screen height, with descending bars crossing ascending ones in a weaving pattern.

---

#### Knob 4 — Frequency
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Frequency controls the spatial frequency of the sinusoidal displacement. Low frequency produces slow, wide oscillations — the bars move gently over large timescales. High frequency creates tight, rapid undulations where each bar traces a fast zigzag path vertically.

---

#### Knob 5 — Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Width sets the vertical thickness of each bar in scanlines. Thin bars produce sharp horizontal lines reminiscent of actual CRT raster bars. Wide bars create broad colour bands that merge and overlap, filling more of the screen with gradient colour.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Bright is a global intensity multiplier applied to all bar colour output. At zero the bars vanish. At full value the bar centres reach maximum luminance and the gradient tails remain visible. This interacts with the gradient shading — lower brightness emphasises the centre-only portion of each bar.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Gradient** | Flat | Grad |
| **8 — Mirror** | Off | On |
| **9 — Rainbow** | Off | On |
| **10 — Mod Vid** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the bar appearance and rendering mode. Gradient switches between flat and shaded bars. Mirror reflects the pattern vertically, creating kaleidoscopic symmetry. Rainbow enables the cycling 8-colour palette. Mod Video multiplies bar brightness with input video luminance for masking effects. Bypass passes the input through unmodified.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the processed bar output. At minimum the output is entirely dry. At maximum the output is entirely wet. Intermediate positions blend the bars over the source material for overlay effects.

---

## Guided Exercises

These exercises progress from a single monochrome bar to a full rainbow copper-bar animation, exploring the interaction between bar count, gradient, and mirror modes.

### Exercise 1: Single Gradient Bar

<img src={kefrens_exercise1_result} alt="Single Gradient Bar result"/>
*Single Gradient Bar — simulated result across source images.*
**Objective**: Produce a single smoothly oscillating gradient bar to study the core shading and animation mechanics.

1. Set Bars to 1.
2. Set Gradient to Grad for tube-like shading.
3. Set Rainbow to Off for monochrome white.
4. Set Amplitude to approximately 50%.
5. Set Frequency to approximately 25%.
6. Set Width to approximately 40%.
7. Set Speed to approximately 35%.
8. Set Bright to approximately 80%.
9. Set Mix to 100%.
10. Observe the single bar gliding smoothly up and down with gradient shading.

**Key concepts**: Sinusoidal displacement, gradient shading, animation speed.

---

### Exercise 2: Full Rainbow Stack

<img src={kefrens_exercise2_result} alt="Full Rainbow Stack result"/>
*Full Rainbow Stack — simulated result across source images.*
**Objective**: Create the iconic multi-bar rainbow copper bar effect with maximum visual density.

1. Set Bars to 8 for maximum bar count.
2. Enable Rainbow for spectral colour cycling.
3. Set Gradient to Grad.
4. Increase Amplitude to approximately 60%.
5. Set Width to approximately 35% to avoid total overlap.
6. Set Speed to approximately 40%.
7. Set Frequency to approximately 30%.
8. Set Bright to approximately 75%.
9. Observe 8 coloured bars weaving through each other.

**Key concepts**: Multi-bar overlap, rainbow palette cycling, bar crossing.

---

### Exercise 3: Mirrored Video Overlay

<img src={kefrens_exercise3_result} alt="Mirrored Video Overlay result"/>
*Mirrored Video Overlay — simulated result across source images.*
**Objective**: Layer mirrored rainbow bars over live video input for a performance-ready composite.

1. Keep the Exercise 2 rainbow stack running.
2. Enable Mirror for vertical symmetry.
3. Toggle Mod Video On to mask bars with input brightness.
4. Set Mix to approximately 70%.
5. Feed a high-contrast video source.
6. Adjust Amplitude and Width to balance bar visibility with video clarity.
7. Experiment with Speed for pulsing vs steady motion.
8. Toggle Mirror off to compare asymmetric vs symmetric looks.

**Key concepts**: Vertical mirror symmetry, video modulation masking, overlay blending.

---


## Tips

- **Start with Gradient**: The tube-like shading makes individual bars much easier to distinguish, especially with multiple overlapping bars.
- **Rainbow needs multiple bars**: A single bar with rainbow enabled still only shows one hue — use 4+ bars to see the full spectral effect.
- **Mirror doubles density cheaply**: Enable Mirror to double the visual bar count without consuming additional processing resources.
- **Width vs Amplitude**: Wide bars with small amplitude create a screen-filling colour wash; thin bars with large amplitude create dynamic weaving patterns.
- **Use Mod Video with faces**: High-contrast faces or silhouettes create dramatic video-shaped windows into the bar animation.
- **Frequency as texture**: High frequency values create a textured, almost static-looking pattern as quick oscillations blend into standing waves.
- **Speed for performance**: Map Speed to a control voltage for rhythmically synchronised bar animation.

---
