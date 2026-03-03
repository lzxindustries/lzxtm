---
draft: true
sidebar_position: 229
slug: /instruments/videomancer/plasma
title: "Plasma"
image: /img/instruments/videomancer/plasma/plasma_hero.png
description: "Somewhere in the early 1990s, a coder with a 386 and a VGA framebuffer discovered that if you sum a handful of sine waves across the screen, each with a different spatial orientation, and map the result through a colour table, the screen fills with the iconic flowing, swirling colour fields that would become the most recognized effect in the demoscene."
---

import plasma_hero from '/img/instruments/videomancer/plasma/plasma_hero.png';
import plasma_animation from '/img/instruments/videomancer/plasma/plasma_animation.gif';
import plasma_control_panel from '/img/instruments/videomancer/plasma/plasma_control_panel.png';
import plasma_exercise1_result from '/img/instruments/videomancer/plasma/plasma_exercise1_result.gif';
import plasma_exercise2_result from '/img/instruments/videomancer/plasma/plasma_exercise2_result.gif';
import plasma_exercise3_result from '/img/instruments/videomancer/plasma/plasma_exercise3_result.gif';

# Plasma

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={plasma_hero} alt="Plasma hero image"/>
*A flowing psychedelic colour field — four sine terms collide to produce rippling plasma bands streaming through a Fire palette, the radial oscillator pulling concentrically toward a drifting center point.*
<img src={plasma_animation} alt="Plasma animated output"/>
*Plasma output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Somewhere in the early 1990s, a coder with a 386 and a VGA framebuffer discovered that if you sum a handful of sine waves across the screen, each with a different spatial orientation, and map the result through a colour table, the screen fills with the iconic flowing, swirling colour fields that would become the most recognized effect in the demoscene. Plasma recreates that effect in dedicated FPGA hardware, evaluating four sine terms per pixel at 74.25 MHz with zero BRAM and approximately 600 logic cells.

Four oscillators contribute to each pixel's value: a horizontal sine, a vertical sine, a diagonal sine (the sum of x and y coordinates), and a radial term computed from the Chebyshev distance to a slowly drifting center point. The four sine outputs are summed into a 12-bit signed accumulator, then mapped to one of 32 palette entries within the selected colour table. Eight palettes — Classic rainbow, Fire, Ocean, Acid, Neon, Mono, Sunset, and Ice — are stored as 32-entry RGB 3-3-3 colour ramps converted to YUV at synthesis time. Phase accumulators increment on each frame tick, producing the characteristic streaming animation, while a separate palette cycling offset shifts the colour index continuously to create the illusion of flowing colour independent of the spatial pattern.

At conservative settings, Plasma produces gently undulating colour fields suitable for background layering. At high frequency and speed with the radial component engaged, the screen fills with complex interference fringes that morph rapidly through the colour space. The name *Plasma* is the universal demoscene label for this class of sine-sum colour field generators.

---

## Background

### The Demoscene Plasma Effect

The plasma effect emerged from the European home computer demoscene in the late 1980s and early 1990s. On machines like the Amiga, Atari ST, and early PCs running DOS, coders discovered that a few trigonometric evaluations per pixel — trivially cheap on modern hardware but requiring careful optimization on 16-bit processors — could produce organic, liquid colour fields that appeared far more complex than their mathematical description. Groups like Future Crew, Triton, and Sanity featured plasma routines in their demos, and the effect became a standard "hello world" for graphics programming. Plasma's appeal lies in the gap between its simplicity (addition of sine waves) and its visual complexity (an apparently infinite variety of flowing chromatic patterns).

### Sine-Sum Interference

The mathematical basis of the plasma effect is constructive and destructive interference of periodic functions. When two sine waves of different spatial frequency or orientation are summed, they produce a new waveform with amplitude peaks where the waves reinforce and nulls where they cancel. Four sine terms — horizontal, vertical, diagonal, and radial — create a two-dimensional interference pattern with no repeating tile boundary. The spatial frequency of each term determines how many cycles appear across the screen, while the relative phase offsets between terms control where the peaks and nulls fall. Animating those phases causes the interference pattern to evolve continuously.

### Quarter-Wave LUT and Quadrant Mirroring

A full sine table for 10-bit phase resolution would require 1024 entries. Plasma exploits the symmetry of the sine function to store only one quarter of the waveform: a 256-entry table covering the first quadrant ($0$ to $\pi/2$). The full sine is reconstructed by mirroring the index for quadrants 1 and 3 (reading the table backward) and negating the output for quadrants 2 and 3. This reduces storage by 4× while preserving full 10-bit phase precision. The output is a signed 10-bit value ranging from $-511$ to $+511$.

### DDS Phase Accumulators

Animation is driven by four 16-bit phase accumulators, each incremented by a rate derived from the Speed parameter plus a fixed per-term offset (+0, +3, +7, +11). The accumulated phase is truncated to 10 bits before being added to the per-pixel spatial argument. Because each accumulator has a slightly different rate, the four sine terms drift in and out of alignment over time, producing the characteristic evolving interference patterns. A fifth accumulator drives the palette cycling offset, allowing the colour mapping to flow independently of the spatial pattern.

### Palette Cycling and Colour Mapping

The plasma sum (a signed 12-bit value) is mapped to a 5-bit index (0–31) by shifting and clamping. This index then passes through the palette cycling offset — a continuously incrementing 5-bit value — producing a rotating window into the 32-entry palette. Because the palette entries wrap cyclically, the colours appear to flow through the spatial pattern like a river of light. The eight palettes provide dramatically different characters: Classic produces a full rainbow cycle, Fire ramps from black through red-orange to white, Ocean oscillates between deep blue and cyan, and Mono reduces the effect to a pure grayscale interference pattern.


---

## Signal Flow

```
registers_in
│
├─ reg(0) → Speed           (animation DDS rate)
├─ reg(1) → Frequency       (H/V phase offset)
├─ reg(2) → Radial          (distance term weight)
├─ reg(3) → Distortion      (X/Y frequency asymmetry)
├─ reg(4) → Pal Speed       (palette cycling rate)
├─ reg(5) → Brightness      (output luma scaling)
├─ reg(6)(2:0) → Palette Select (3-bit: 8 palettes)
├─ reg(6)(1) → Video Mod    (shares bit 1 with palette)
├─ reg(6)(2) → Waveshape    (shares bit 2 with palette)
├─ reg(6)(3) → Lo-Res
├─ reg(6)(4) → Bypass
└─ reg(7) → Mix Amount

Video Input (YUV 4:4:4)
│
├─ Timing Generator            (hsync/vsync → hcount, vcount)
│
├─ Phase Accumulators (per-frame, on vsync_start)
│   ├─ phase1 += speed >> 2
│   ├─ phase2 += speed >> 2 + 3
│   ├─ phase3 += speed >> 2 + 7
│   ├─ phase4 += speed >> 2 + 11
│   ├─ pal_offset += pal_speed >> 2
│   ├─ center_x = 960 + sine(cx_phase >> 6)   (drifting center)
│   └─ center_y = 540 + sine(cy_phase >> 6)
│
├─ Stage 1: Argument Calculation (per-pixel)
│   ├─ if lo_res: quantize hc, vc to 4×4 blocks
│   ├─ freq_x, freq_y adjusted by Distortion
│   ├─ arg1 = hc[9:0] + freq_x[9:4] + phase1[15:6]
│   ├─ arg2 = vc[9:0] + freq_y[9:4] + phase2[15:6]
│   ├─ arg3 = (hc + vc)[9:0] + phase3[15:6]
│   └─ arg4 = chebyshev_dist(hc, vc, center) + phase4[15:6]
│       ◄── Frequency, Distortion, Lo-Res
│
├─ Stages 2–5: TDM Sine Evaluation (4 clocks, 1 term per clock)
│   ├─ accum  = sine(arg1)
│   ├─ accum += sine(arg2)
│   ├─ accum += sine(arg3)
│   └─ accum += sine(arg4) × (radial >> 2) >> 7
│       ◄── Radial
│
├─ Stage 6: Summation + Palette Index
│   ├─ if square_mode: index = (sum ≥ 0) ? 31 : 0
│   ├─ else: index = clamp((sum + 2048) >> 7, 0, 31)
│   └─ pal_idx = palette_sel(2:0) & (index + pal_offset[15:11])
│       ◄── Waveshape, Palette, Pal Speed
│
├─ Stage 7: Palette Lookup + Composite
│   ├─ plasma_y/u/v = palette[pal_idx]
│   ├─ if video_mod: comp_y = plasma_y × input_y >> 10
│   │                 comp_u/v = avg(plasma, input)
│   └─ else: comp = plasma
│       ◄── Video Mod
│
├─ Stage 8: Brightness Scaling
│   └─ bright_y = comp_y × brightness >> 10
│       ◄── Brightness
│
├─ Stages 9–12: Interpolator Mix (×3 channels, 4 clk)
│   └─ mix = lerp(delayed_input, bright, mix_amount)
│       ◄── Mix
│
├─ Sync Delay Pipeline (13-clock shift register)
│
└─ Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → delayed input Y/U/V + aligned sync
        ◄── Bypass
```

The four sine terms are evaluated sequentially in a TDM (time-division multiplexed) pipeline that completes one term per clock cycle. This reuses a single sine lookup function across four arguments, saving area at the cost of 4 clocks of latency. The accumulator is 12 bits signed, accommodating the sum of up to four full-amplitude sine outputs (each ±511) plus the radial scaling, which can amplify the fourth term up to 2× when the Radial control is at maximum.

Bits 1 and 2 of register 6 are triple-mapped: they simultaneously select palette bits (contributing to the 3-bit palette index), enable video modulation (bit 1), and select sine/square waveshape (bit 2). This means enabling Video Mod or switching to Square mode also changes which palette is active. The eight palette labels listed in the TOML represent the combined state of toggles 7, 8, and 9.

---

## Parameter Reference

<img src={plasma_control_panel} alt="Videomancer front panel with Plasma loaded"/>
*Videomancer's front panel with Plasma active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the rate at which the four phase accumulators advance per frame. The register value is right-shifted by 2 to produce a base increment; each oscillator adds a fixed per-term offset (+0, +3, +7, +11) to this base, so smaller speed values still produce relative drift between terms. At 0%, the pattern is frozen in time. At 100%, the phases advance rapidly, producing fast swirling animation. The nonlinear visual response is logarithmic — doubling the knob value doubles the apparent animation rate. Intermediate values around 35-40% produce a gentle, hypnotic drift suitable for ambient backdrops.

---

#### Knob 2 — Frequency
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Shifts the horizontal and vertical sine arguments by adding a phase offset derived from the upper 6 bits of the register. This does not change the spatial frequency of the sine terms (which is fixed by the 10-bit pixel counter wrapping at 1024) but alters the interference pattern by repositioning the horizontal and vertical terms relative to each other and the screen edges. At centre, the default pattern appears. Turning the knob shifts the pattern in both axes, producing different spatial configurations. When combined with Distortion, Frequency controls the baseline pattern symmetry while Distortion introduces directional asymmetry.

---

#### Knob 3 — Radial
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scales the contribution of the radial sine term to the total sum. The radial term is computed from the Chebyshev distance (max of |Δx|, |Δy|) between the current pixel and a drifting center point. At 0%, the fourth term contributes nothing and the pattern is purely planar — composed of horizontal, vertical, and diagonal sine components. At 100%, the radial term is weighted at approximately 2× the base amplitude, dominating the pattern and pulling it toward concentric rings centered on the drifting point. At intermediate values around 50%, the radial component adds a gentle curvature to the otherwise linear interference fringes.

---

#### Knob 4 — Distortion
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Introduces asymmetry between the horizontal and vertical sine frequencies. At the center position (50%), both axes receive the same frequency offset and the pattern has roughly equal X/Y periodicity. Above centre, the X frequency offset increases while Y remains constant, stretching the pattern horizontally. Below centre, the Y frequency offset increases while X remains constant, stretching the pattern vertically. This control is most visible at low Frequency settings where the spatial periodicity is large enough to see the directional bias clearly. At extreme settings, the pattern becomes strongly oriented in one axis, producing banded rather than cellular structures.

---

#### Knob 5 — Pal Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the rate of palette cycling — the continuous rotation of the colour lookup index that makes the plasma colours appear to flow through the spatial pattern. A separate 16-bit accumulator advances by this parameter's upper 8 bits on each frame, and the accumulated offset is added to the spatial palette index before lookup. At 0%, colours are fixed and only the spatial pattern moves. At 100%, colours stream rapidly through the palette, creating a second layer of animation independent of the pattern shape. The palette offset wraps modulo 32, so all palette entries are visited cyclically. Moderate values around 35% produce a gentle colour drift that complements the spatial motion.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the final output luminance by multiplying the composed Y channel by this register value. At 0%, the output is black regardless of the palette colours. At 100%, the palette colours appear at full intensity. The multiplication is a 10×10-bit product with the upper 10 bits taken as the result, providing smooth analogue-style dimming. This control affects only luminance — chroma (U, V) passes through unscaled, so reducing brightness desaturates the visual appearance slightly as the colour signal remains relative to a dimming luma carrier. Default is 75%, leaving headroom for video modulation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Classic | Fire |
| **8 — Video Mod** | Off | On |
| **9 — Waveshape** | Sine | Square |
| **10 — Lo-Res** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into three functional groups with an important hardware interaction. Palette (toggle 7), Video Mod (toggle 8), and Waveshape (toggle 9) all read from the same toggle register: Palette uses bits 2:0 as a 3-bit palette selector, while Video Mod reads bit 1 and Waveshape reads bit 2. This means enabling Video Mod or switching to Square waveshape simultaneously changes the active palette. The eight palette names in the TOML describe the combined state of all three toggles:

| Palette | Tog 7 | Video Mod | Waveshape |
|---------|-------|-----------|-----------|
| Classic | 0 | Off | Sine |
| Fire | 1 | Off | Sine |
| Ocean | 0 | On | Sine |
| Acid | 1 | On | Sine |
| Neon | 0 | Off | Square |
| Mono | 1 | Off | Square |
| Sunset | 0 | On | Square |
| Ice | 1 | On | Square |

Lo-Res (toggle 10) operates independently, quantizing pixel coordinates to 4×4 blocks. Bypass (toggle 11) overrides everything at the output mux.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the delayed input video and the brightness-scaled plasma output. At 0% (fader down), the output is pure dry input — no plasma is visible. At 100% (fader up), the output is the fully composed plasma pattern. Intermediate positions blend the two, allowing the plasma to appear as a semi-transparent colour overlay. In Video Mod mode at 50% mix, the input video shows through with a ghosted plasma texture — useful for subtle chromatic effects.

---

## Guided Exercises

These exercises build from a static colour field through animated streaming to complex video modulation. Because Plasma is a generative synthesis program, each exercise produces output from scratch — allow a few seconds for the animation to settle before evaluating the visual result.

### Exercise 1: Static Interference Pattern

<img src={plasma_exercise1_result} alt="Static Interference Pattern result"/>
*Static Interference Pattern — simulated result across source images.*
**Objective**: Understand how the four sine terms combine to produce the plasma pattern, and how Frequency and Distortion shape the interference field.

1. **Freeze motion**: Set Speed to 0% and Pal Speed to 0%. The pattern should be completely static.
2. **Default palette**: Set Palette toggle to the leftmost position (Classic). Leave Video Mod Off and Waveshape at Sine.
3. **Observe base pattern**: With Frequency at ~40% and Distortion at ~50% (centre), note the smooth flowing colour gradients across the frame.
4. **Add radial**: Increase Radial to ~60%. Concentric rings appear, centred on the drifting center point (which is frozen since Speed is 0).
5. **Introduce distortion**: Move Distortion toward ~80%. The pattern stretches horizontally as the X frequency offset increases.
6. **Sweep frequency**: Slowly turn Frequency from minimum to maximum. Watch how the interference pattern shifts and reconfigures through different symmetry states.
7. **Full brightness**: Ensure Brightness is at ~75% for vivid colours.

**Key concepts**: Four sine terms produce the 2D interference pattern, Frequency shifts the H/V phase offsets, Distortion breaks X/Y symmetry, Radial adds concentric rings from drifting center, palette maps the sum to colour

---

### Exercise 2: Streaming Fire Plasma

<img src={plasma_exercise2_result} alt="Streaming Fire Plasma result"/>
*Streaming Fire Plasma — simulated result across source images.*
**Objective**: Explore animation controls and palette cycling to produce the classic flowing plasma effect with the Fire palette.

1. **Select Fire palette**: Toggle Palette to position 2 (with Video Mod Off and Waveshape Sine, this selects "Fire").
2. **Enable animation**: Set Speed to ~40%. The interference pattern begins flowing.
3. **Add palette cycling**: Set Pal Speed to ~35%. Colours stream through the spatial pattern independently of its motion.
4. **Engage radial**: Set Radial to ~50%. The pattern acquires concentric depth, with fire colours pooling at the center.
5. **Increase speed**: Push Speed to ~70%. The pattern swirls rapidly, blending multiple colour bands into a continuous flow.
6. **Try square mode**: Flip Waveshape to Square. Hard-edged contours carve the flowing field into two-tone regions. Note: switching Waveshape also changes the palette to a Neon-family variant.
7. **Reduce brightness**: Pull Brightness down to ~50%. The fire dims to glowing embers.

**Key concepts**: Speed controls phase accumulator rate, Pal Speed adds independent colour flow, Fire palette ramps black-red-yellow-white, Waveshape quantizes smooth gradients to hard edges, Waveshape toggle also changes the active palette

---

### Exercise 3: Video-Modulated Lo-Res Plasma

<img src={plasma_exercise3_result} alt="Video-Modulated Lo-Res Plasma result"/>
*Video-Modulated Lo-Res Plasma — simulated result across source images.*
**Objective**: Combine video modulation with low-resolution mode to texture a live video source with a chunky plasma overlay.

1. **Enable Video Mod**: Flip Video Mod toggle to On. Note: this changes the active palette to an Ocean-family variant.
2. **Enable Lo-Res**: Flip Lo-Res to On. The plasma pixelates into 4×4 blocks.
3. **Moderate speed**: Set Speed to ~30%. A gentle animation flows through the chunky blocks.
4. **Set mix**: Push Mix fader to ~80%. The modulated video dominates with the plasma texture stamped on it.
5. **Adjust brightness**: Set Brightness to ~90%. Maximum brightness ensures the modulation is clearly visible.
6. **Slow palette cycling**: Set Pal Speed to ~20%. Colours drift slowly through the chunky grid.
7. **Sweep Radial**: Move Radial from 0% to 100%. Watch how the concentric component interacts with the pixelated grid — at high radial, rings are visible as stair-stepped concentric arcs.

**Key concepts**: Video Mod multiplies plasma luma by input video Y, Lo-Res quantizes to 4×4 blocks, combined modes interact with palette selection, Mix fader controls modulation intensity, radial component visible as stair-stepped rings in low-res mode

---


## Tips

- **Start with Speed 0%**: Freezing the pattern helps understand the spatial interference structure before adding temporal animation.
- **Use Pal Speed for colour flow**: Palette cycling adds a second layer of animation independent of the spatial pattern motion — it makes the plasma look more liquid.
- **Radial for depth**: The radial component adds a 3D quality. Keep it around 40–60% for subtle curvature without overwhelming the planar terms.
- **Distortion for directionality**: Push Distortion away from centre to create banded patterns oriented along one axis — useful for horizontal or vertical streaming effects.
- **Lo-Res for retro aesthetic**: Low-resolution mode with Fire or Neon palette faithfully recreates the chunky 320×200 plasma from DOS demos.
- **Square mode for contours**: Square waveshape turns the plasma into a topographic map with hard boundaries — effective for creating high-contrast key signals.
- **Mix for overlay**: At 50% Mix with a video source, the plasma acts as a soft chromatic overlay. Combine with Video Mod for multiplicative texturing.
- **Watch palette interactions**: Toggling Video Mod or Waveshape also changes the palette. Explore all 8 combinations to find the colour scheme that fits your composition.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chebyshev distance** | A distance metric defined as the maximum of the absolute differences along each axis: $d = \max(|x_1 - x_2|, |y_1 - y_2|)$. Also called chessboard distance, it produces square contours rather than circular ones. |
| **DDS (Direct Digital Synthesis)** | A technique for generating periodic waveforms using a phase accumulator and a lookup table. Each clock cycle, the accumulator advances by a fixed increment (the tuning word), and the accumulated phase indexes the waveform table. |
| **Demoscene** | A computer art subculture focused on producing real-time audio-visual demonstrations that push hardware capabilities, originating on 1980s home computers. |
| **Interference pattern** | The spatial pattern produced when two or more periodic signals are summed, exhibiting constructive reinforcement at some locations and destructive cancellation at others. |
| **Palette cycling** | A technique from indexed-colour display systems where the colour lookup table entries are rotated over time, creating the illusion of motion or colour flow without changing pixel values. |
| **Quarter-wave LUT** | A lookup table storing only the first quadrant ($0$ to $\pi/2$) of a sine wave. The full waveform is reconstructed via index mirroring and output negation based on the quadrant of the input phase. |
| **TDM (Time-Division Multiplexing)** | A technique where a single hardware resource is shared among multiple operations by processing them sequentially across different clock cycles. |
| **YUV** | A colour model that separates luminance (Y) from two chrominance components (U and V), widely used in video signal processing. |

---
