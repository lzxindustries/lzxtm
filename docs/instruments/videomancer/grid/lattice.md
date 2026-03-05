---
draft: true
sidebar_position: 167
slug: /instruments/videomancer/lattice
title: "Lattice"
image: /img/instruments/videomancer/lattice/lattice_hero.png
description: "Lattice is a geometric pattern synthesizer that generates two-dimensional grid structures from a pair of orthogonal frequency accumulators."
---

import lattice_hero from '/img/instruments/videomancer/lattice/lattice_hero.png';
import lattice_animation from '/img/instruments/videomancer/lattice/lattice_animation.gif';
import lattice_control_panel from '/img/instruments/videomancer/lattice/lattice_control_panel.png';
import lattice_exercise1_result from '/img/instruments/videomancer/lattice/lattice_exercise1_result.gif';
import lattice_exercise2_result from '/img/instruments/videomancer/lattice/lattice_exercise2_result.gif';
import lattice_exercise3_result from '/img/instruments/videomancer/lattice/lattice_exercise3_result.gif';

# Lattice

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lattice_hero} alt="Lattice hero image"/>
*Lattice projecting a luminous XOR checkerboard grid — animated phase offsets ripple through interlocking horizontal and vertical bar patterns at high contrast.*
<img src={lattice_animation} alt="Lattice animated output"/>
*Lattice output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Lattice is a geometric pattern synthesizer that generates two-dimensional grid structures from a pair of orthogonal frequency accumulators. The name evokes the mathematical concept of a lattice — a regular, repeating arrangement of points in space — and the visual output delivers exactly that: clean intersecting lines, moire interference fields, and tessellated checkerboards built from pure arithmetic.

Two DDS (Direct Digital Synthesis) accumulators run along the horizontal and vertical axes of the video raster. Each produces a sawtooth ramp whose frequency is set by its respective pot. The ramps can optionally be folded into triangle waves via the frequency doubler module, which reflects the upper half of the waveform around the midpoint. The two resulting patterns are then combined through a selectable boolean operation — AND produces grid intersections while XOR produces alternating checkerboard regions. A line width threshold controls the duty cycle of each pattern, determining the ratio of foreground to background. The combined mask keys between a configurable fill color and the input video, and a free-running animation accumulator adds temporal scrolling to the pattern. The final result passes through a wet/dry crossfader.

Despite its apparent simplicity, Lattice occupies a sweet spot between utility and generative art. At integer frequency ratios and narrow line widths it produces pixel-precise test grids. At irrational ratios with XOR combining, it generates complex moire interference patterns that shift continuously under animation — a digital analogue of the optical beat patterns seen when overlapping two fine screens of differing pitch.

---

## Quick Start

1. **TOML labels are misleading**: The knob labels on the control panel do not match VHDL behavior. "Bar Width" is actually animation speed, "Fill Y" through "Fill V" are actually line width, fill brightness, and fill hue respectively. Refer to this guide for accurate control descriptions.
2. **Equal H and V frequencies produce square grids**: For pixel-perfect test patterns, match both frequency knobs. Unequal values create rectangular cells.
3. **XOR creates more pattern density than AND**: If the output looks too sparse, switch from AND to XOR. XOR fills approximately twice the area for the same threshold setting.

---

## Background

### Direct Digital Synthesis and Phase Accumulators

A **phase accumulator** is the core of Direct Digital Synthesis. On every clock strobe (once per pixel horizontally, or once per line vertically), the accumulator adds a fixed step value to a running total. When the total overflows, the ramp wraps and a new cycle begins. The step value directly controls the output frequency: larger steps produce higher frequencies with fewer pixels per cycle. Because the accumulator wraps at a power of two, the resulting waveform is always periodic, and its frequency is always a rational fraction of the clock rate. This makes DDS inherently alias-free within its Nyquist band.

### Frequency Folding and Triangle Waves

A **frequency doubler** (sometimes called a full-wave rectifier or fold circuit) takes a sawtooth ramp and reflects its upper half around the midpoint. Values below half-scale are doubled; values above half-scale are mirrored and doubled. The result is a triangle wave at twice the spatial frequency of the original ramp. In bypass mode, the raw sawtooth passes through unchanged, producing sharp edges where the waveform wraps from maximum to zero.

### Boolean Mask Operations

When two binary patterns are combined with **AND**, only the pixels where both patterns are active survive — producing isolated grid intersection points or narrow cross-hatch lines. When combined with **XOR**, pixels that are active in exactly one pattern (but not both) survive — producing an alternating checkerboard or tiled mosaic. XOR is its own inverse: applying it twice restores the original, which creates interesting visual symmetry properties.

### Moire Interference

When two periodic patterns of slightly different frequency overlap, they produce **moire fringes** — large-scale beat patterns whose spatial frequency equals the difference between the two source frequencies. Lattice generates moire naturally whenever the H and V frequencies differ from simple integer multiples of each other. The animation accumulator shifts these beat patterns over time, creating slowly undulating visual textures reminiscent of watered silk or the iridescence on a compact disc surface.

### Video Keying

The grid mask acts as a binary key signal. Where the mask is active, the output shows the fill color (a user-defined brightness and hue). Where the mask is inactive, the delayed input video passes through. This keying operation allows the lattice pattern to be overlaid on live footage, creating graphic overlays, scan-line grids, and spatial modulation patterns.


---

## Signal Flow

```
┌────────────────────────────────────────────────────────────────────┐
│  Video Timing Generator (~2 clk)                                   │
│     └─ Extracts hsync, vsync, avid from input data_in              │
│                                                                    │
│  Phase Accumulators (~2 clk each)                                  │
│     ├─ H Accumulator: 16-bit, resets at line start, adds h_freq   │
│     │   per pixel → s_h_acc_out                                    │
│     ├─ V Accumulator: 16-bit, resets at frame start, adds v_freq  │
│     │   per line → s_v_acc_out                                     │
│     └─ Anim Accumulator: 16-bit free-running, adds anim_speed     │
│         per field → s_anim_acc_out                                 │
│           ◄── H Freq (reg 0), V Freq (reg 1), Anim Speed (reg 2)  │
│                                                                    │
│  Ramp Extraction                                                   │
│     └─ Upper 10 bits of each 16-bit accumulator → 10-bit ramps    │
│                                                                    │
│  Frequency Doubler (2 clk each)                                    │
│     ├─ fold_h: sawtooth → triangle (or bypass) → s_fold_h_result  │
│     └─ fold_v: sawtooth → triangle (or bypass) → s_fold_v_result  │
│           ◄── Fold Bypass H (reg 6 bit 1), Fold Bypass V (bit 2)  │
│                                                                    │
│  Threshold + Boolean Combine (1 clk)                               │
│     ├─ v_h_val = fold_h_result + anim_ramp (scrolling offset)     │
│     ├─ h_line = (v_h_val > line_width) ? 1 : 0                    │
│     ├─ v_line = (fold_v_result > line_width) ? 1 : 0              │
│     └─ grid_mask = bool_mode ? (h XOR v) : (h AND v)              │
│           ◄── Line Width (reg 3), Bool Mode (reg 6 bit 0)         │
│                                                                    │
│  Key Compose (1 clk)                                               │
│     ├─ mask = key_invert ? NOT grid_mask : grid_mask               │
│     ├─ If mask=1: output fill color (fill_y, fill_u, fill_v)      │
│     └─ If mask=0: output delayed input video                       │
│           ◄── Fill Y (reg 4), Fill Hue (reg 5),                   │
│               Key Invert (reg 6 bit 3)                             │
│                                                                    │
│  Interpolator (4 clk, per Y/U/V)                                  │
│     └─ mix = lerp(input_delayed, composed, mix_amount)             │
│           ◄── Mix (reg 7)                                          │
└────────────────────────────────────────────────────────────────────┘

 Output = bypass ? input_delayed : mix_result
           ◄── Bypass (reg 6 bit 4)
```

The critical insight in Lattice's pipeline is that the animation offset is added only to the horizontal folded ramp, not to the vertical. This means animation scrolls the horizontal bar pattern sideways while the vertical pattern remains locked in place, producing a distinctive diagonal ripple when both axes are active. The fill chroma is derived from a single Hue parameter: U takes the hue value directly, while V takes its complement (1023 − hue), so sweeping the hue pot rotates through complementary color pairs around the neutral axis. The line width threshold applies identically to both axes, so H and V bars always share the same duty cycle. The key compose stage uses an 8-clock video delay line to align the input data with the grid computation pipeline before keying.

---

## Parameter Reference

<img src={lattice_control_panel} alt="Videomancer front panel with Lattice loaded"/>
*Videomancer's front panel with Lattice active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — H Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the horizontal pattern frequency. The 10-bit register value is zero-extended to 16 bits and used as the step size for the horizontal phase accumulator, which increments once per pixel clock during active video and resets at each line start. At low values, the horizontal pattern has very few cycles across the screen — wide, slowly varying bars. At high values, many cycles appear per line, creating fine vertical stripes. Because the accumulator is 16 bits wide but only the upper 10 bits are extracted as the ramp, the effective spatial frequency is register_value / 64 cycles per line. Setting this to zero produces a static DC level with no horizontal pattern.

---

#### Knob 2 — V Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the vertical pattern frequency. Operates identically to H Freq but the accumulator increments once per line (at avid_start) and resets at each field start. Low values produce wide horizontal bands; high values create fine horizontal stripes. The interaction between H Freq and V Freq determines the overall grid geometry: equal values produce square cells, unequal values produce rectangular cells, and non-integer ratios produce complex moire beat patterns.

---

#### Knob 3 — Bar Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the animation speed. Despite the TOML label "Bar Width," this register actually drives the step size of a free-running animation accumulator that increments once per field and never resets. The upper 10 bits of this accumulator are added to the folded horizontal ramp in the threshold stage, creating a continuously scrolling phase offset on the horizontal bars. At zero, the pattern is static. At low values, the pattern drifts slowly. At high values, it scrolls rapidly, creating a kinetic flickering effect. This control has no effect on bar thickness — that is determined by the Line Width parameter (reg 3).

---

#### Knob 4 — Fill Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the grid line thickness. Despite the TOML label "Fill Y," this register is the threshold comparator for both H and V bar patterns. The folded ramp values are compared against this threshold: pixels above the threshold become grid lines, pixels below become background. At 0, the entire field passes the threshold and the screen fills with the foreground color. At maximum, nothing passes and the screen is entirely background. The midpoint (~50%) produces equal-width bars and gaps. Because the same threshold applies to both axes, horizontal and vertical bars always have matching duty cycles.

---

#### Knob 5 — Fill U
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the fill luma brightness. Despite the TOML label "Fill U," this register sets the Y (luminance) channel of the fill color used for grid line regions. At 0, grid lines are black. At maximum, grid lines are full brightness. This is independent of the chroma hue — you can have bright colored lines, dim colored lines, or pure black grid lines.

---

#### Knob 6 — Fill V
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the fill chroma hue. Despite the TOML label "Fill V," this register determines both the U and V chrominance channels of the fill color. U is set directly to the register value, while V is set to its complement (1023 − value). This creates a complementary color sweep: at 0 the fill is warm (low U, high V), at 512 it is neutral gray (both channels at midpoint), and at 1023 it is cool (high U, low V). The sweep passes through a full range of saturated hues as you rotate from one extreme to the other.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — H Shape** | Ramp | Triangle |
| **8 — V Shape** | Ramp | Triangle |
| **9 — Combine** | AND | XOR |
| **10 — Soft Edge** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles each map to a single bit in register 6, but their TOML labels are misleading. In practice: bit 0 selects the boolean combine mode (AND vs XOR), bits 1 and 2 bypass the frequency doubler on the horizontal and vertical axes respectively (letting raw sawtooth through instead of triangle), bit 3 inverts the key mask (swapping foreground and background), and bit 4 is the global bypass. These five binary options combine to produce 16 distinct grid character variations.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Anim Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Wet/dry crossfade between the delayed input video and the keyed grid output. Despite the TOML label "Anim Rate," this register controls the interpolator mix amount. At 0% (fully down), the output is pure input video. At 100% (fully up), the output is pure Lattice grid. Intermediate positions blend the grid pattern over the input at variable opacity, useful for creating subtle overlay effects.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Lattice processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore Lattice's geometric capabilities, from basic grid generation through complex moire interference to animated pattern synthesis. Because Lattice is a synthesis program, each exercise produces patterns from scratch — allow a few seconds for the animation to develop.

### Exercise 1: Perfect Cross-Hatch Grid

<img src={lattice_exercise1_result} alt="Perfect Cross-Hatch Grid result"/>
*Perfect Cross-Hatch Grid — simulated result across source images.*
**What You'll Create**: Create a clean, high-contrast grid pattern using AND combination and triangle wave folding.

1. **Set equal frequencies**: Set H Freq and V Freq to ~25%, creating a moderate grid density with equal horizontal and vertical spacing.
2. **Triangle mode**: Ensure both fold bypasses are off (H Shape = Ramp position means doubler active, creating triangles). The waveforms fold smoothly.
3. **Narrow lines**: Set Line Width (Bar Width knob) to ~70%. Only the peaks of the triangle waves exceed the threshold, producing thin clean grid lines.
4. **Bright white fill**: Set Fill Y (Fill Y knob) to 100% and Fill Hue (Fill V knob) to ~50% (neutral). The grid lines glow white against black.
5. **AND combine**: Set Combine to AND. Only intersection points where both H and V bars overlap produce output — a clean rectangular lattice.
6. **Full mix**: Set Mix (Anim Rate fader) to 100%. No animation — set Anim Speed (Bar Width knob) to 0%.

**Key concepts**: Phase accumulator frequency controls grid density, frequency doubler creates triangle (fold) waveforms from sawtooth, AND combination isolates intersection points, threshold controls line width duty cycle

---

### Exercise 2: XOR Moire Interference

<img src={lattice_exercise2_result} alt="XOR Moire Interference result"/>
*XOR Moire Interference — simulated result across source images.*
**What You'll Create**: Generate complex moire beat patterns by combining incommensurate frequencies with XOR logic.

1. **Mismatched frequencies**: Set H Freq to ~35% and V Freq to ~42%. The non-integer ratio creates spatial beat frequencies.
2. **XOR combine**: Switch Combine to XOR. The alternating pattern fills more area than AND, making the moire fringes visible.
3. **Sawtooth mode**: Enable both fold bypasses (H Shape = Triangle, V Shape = Triangle in TOML terms, which actually bypasses the doubler). Raw sawtooth wraps create hard edges that enhance the moire contrast.
4. **Medium threshold**: Set Line Width to ~50% for equal foreground/background duty cycle.
5. **Add color**: Set Fill Y to ~80%, Fill Hue to ~20% (warm tint). The colored XOR pattern creates an iridescent tile mosaic.
6. **Animate slowly**: Set Anim Speed to ~10%. Watch the moire fringes drift horizontally, creating shimmering interference bands.

**Key concepts**: Non-integer frequency ratios produce moire beat patterns, XOR produces alternating checkerboard tiling, sawtooth wrap edges enhance interference contrast, animation shifts the beat pattern over time

---

### Exercise 3: Scrolling Colored Bars

<img src={lattice_exercise3_result} alt="Scrolling Colored Bars result"/>
*Scrolling Colored Bars — simulated result across source images.*
**What You'll Create**: Use animation and key inversion to create a continuously scrolling colored bar pattern.

1. **Horizontal only**: Set H Freq to ~30%, V Freq to 0%. With no vertical frequency, only horizontal bars appear.
2. **Triangle fold**: Ensure H fold bypass is off. The triangle waveform creates smooth symmetric bars.
3. **Moderate width**: Set Line Width to ~45% for wide colorful bands.
4. **Saturated color**: Set Fill Y to ~90% and Fill Hue to ~75% (cool blue-violet).
5. **Invert key**: Enable Key Invert (Soft Edge toggle). Now the bars show fill color and the gaps show black.
6. **Fast scroll**: Set Anim Speed to ~60%. The bars scroll continuously across the screen.
7. **Full mix**: Set Mix to 100%.

**Key concepts**: Setting one frequency to zero creates a 1D bar pattern, animation adds continuous horizontal scrolling, key invert swaps foreground and background, fill hue creates complementary color pairs from single parameter

---


## Tips

- **Animation only affects horizontal**: The scrolling offset adds to the horizontal ramp only, so vertical bars are always stationary. Use this to create directional motion effects.
- **Triangle vs sawtooth changes the character**: Triangle mode (fold active) produces smooth, symmetric gradients with soft edges. Sawtooth mode (fold bypassed) produces hard wrap edges with aliased transitions. Triangle generally looks cleaner at low frequencies.
- **Key invert is the fastest way to swap density**: Rather than adjusting the threshold, toggle key invert to instantly swap filled and empty regions.
- **Mix fader creates overlay effects**: At partial mix values, the lattice grid appears as a semi-transparent overlay on the input video — useful for calibration grids and graphic overlays.
- **Moire patterns emerge at irrational frequency ratios**: The most interesting generative textures come from slightly mismatched H and V frequencies combined with XOR and slow animation.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms by incrementing a phase accumulator at a fixed step rate, producing precise frequency control via integer arithmetic. |
| **Duty cycle** | The ratio of foreground (active) to background (inactive) time within one waveform period, controlled by the line width threshold comparator. |
| **Frequency doubler** | A circuit that folds a sawtooth ramp into a triangle wave by reflecting the upper half around the midpoint, effectively doubling the spatial frequency. |
| **Moire** | An interference pattern produced when two periodic structures of slightly different frequency overlap, creating large-scale beat fringes at the difference frequency. |
| **Phase accumulator** | A digital counter that increments by a configurable step value on each clock strobe and wraps at overflow, producing a repeating sawtooth ramp whose frequency is proportional to the step size. |
| **Sawtooth** | A waveform that ramps linearly from zero to maximum and then wraps sharply back to zero, produced by the raw phase accumulator output. |
| **Triangle wave** | A waveform that ramps linearly from zero to maximum and then ramps linearly back to zero, produced by folding a sawtooth through the frequency doubler. |
| **XOR** | Exclusive OR; a boolean operation that is true when exactly one of two inputs is true, producing an alternating checkerboard pattern when applied to two periodic binary masks. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
