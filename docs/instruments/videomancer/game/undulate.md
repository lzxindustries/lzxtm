---
draft: true
sidebar_position: 313
slug: /instruments/videomancer/undulate
title: "Undulate"
image: /img/instruments/videomancer/undulate/undulate_hero.png
description: "The Super Nintendo's Horizontal DMA (HDMA) was a hardware feature that could reprogram video registers at the start of every scanline without CPU intervention."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import undulate_hero from '/img/instruments/videomancer/undulate/undulate_hero.png';
import undulate_control_panel from '/img/instruments/videomancer/undulate/undulate_control_panel.png';
import undulate_exercise1_result from '/img/instruments/videomancer/undulate/undulate_exercise1_result.png';
import undulate_exercise2_result from '/img/instruments/videomancer/undulate/undulate_exercise2_result.png';
import undulate_exercise3_result from '/img/instruments/videomancer/undulate/undulate_exercise3_result.png';
import undulate_source1_kodim15 from '/img/instruments/videomancer/undulate/undulate_source1_kodim15.png';
import undulate_source2_kodim03 from '/img/instruments/videomancer/undulate/undulate_source2_kodim03.png';
import undulate_source3_kodim15_bw from '/img/instruments/videomancer/undulate/undulate_source3_kodim15_bw.png';

# Undulate

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: undulate_source1_kodim15, after: undulate_hero },
    { label: "Kodim03", before: undulate_source2_kodim03, after: undulate_hero },
    { label: "Kodim15 B&W", before: undulate_source3_kodim15_bw, after: undulate_hero },
  ]}
/>
*Undulate applying SNES HDMA-style per-scanline brightness waves, hue rotation, and horizontal displacement to transform a static camera feed into a rippling, colour-shifting dreamscape.*

---

## Overview

The Super Nintendo's Horizontal DMA (HDMA) was a hardware feature that could reprogram video registers at the start of every scanline without CPU intervention. Developers used it to warp backgrounds with per-line scrolling, create underwater wobble effects, cycle colour palettes, and produce the wavy heat-haze distortions seen in RPG battle scenes. Undulate channels this technique into three independent per-scanline modulation channels — brightness, hue, and displacement — each with its own frequency, depth, and waveform shape, driven by a shared quarter-wave sine lookup table.

Each channel generates a waveform that varies from one horizontal line to the next. The brightness channel modulates the luminance of every pixel on a given scanline by a single value, creating bands of light and dark that ripple vertically through the frame. The hue channel applies a UV rotation per scanline, shifting colours in bands. The displacement channel horizontally shifts entire scanlines left or right, physically moving pixels to create the wobble effect. When all three channels are active at different frequencies, the image appears to undulate like fabric in water — hence the name.

At subtle settings, Undulate adds gentle luminance striping and a barely perceptible swim to the image. At extreme settings, the three modulation channels interact to produce violently distorted, colour-shifted, horizontally torn video that recalls broken CRT displays and corrupted video RAM — an effect that is equally useful for music video aesthetics and glitch art performances.

---

## Background

### SNES HDMA and Per-Scanline Effects

The Super Nintendo's DMA controller included a specialised mode called Horizontal DMA that could update PPU registers during the horizontal blanking interval between each scanline. This allowed the programmer to specify a table of values — one per scanline — that would be automatically loaded into any PPU register without interrupting game logic. The PPU contained registers for scroll position, colour math parameters, window boundaries, and mosaic size, among others. By targeting the scroll registers, HDMA created wavy backgrounds. By targeting colour math registers, it created per-scanline brightness fades and colour cycles. Undulate implements three such register-modification channels simultaneously, exceeding what was possible on original hardware.

### Waveform Generation from Quarter-Wave LUT

Generating smooth mathematical waveforms in FPGA logic without expensive multipliers requires a lookup table approach. Undulate stores a 256-entry quarter-wave sine table in BRAM. Full sine coverage comes from quadrant mirroring: the first quarter (0°–90°) reads the table directly, the second quarter (90°–180°) reads the table in reverse, the third quarter (180°–270°) negates the forward read, and the fourth quarter (270°–360°) negates the reverse read. From this single sine table, additional waveforms are derived: square waves by thresholding the sine at zero, triangle waves by using the linear address ramp itself, and sawtooth waves by using the raw phase accumulator value.

### Per-Scanline Modulation

The core idea is simple: for each scanline, evaluate a waveform function at a phase that depends on the line number and a global animation counter. The result is a single value — a brightness offset, a rotation angle, or a pixel displacement — that applies uniformly to every pixel on that line. Because the waveform varies from line to line, the effect appears as horizontal bands that travel vertically through the image as the animation counter advances. The frequency knob controls how many complete wave cycles fit within the frame height, while the depth knob controls the amplitude of the modulation.

### UV Hue Rotation

Rotating colour hue in YUV space is accomplished by applying a 2D rotation matrix to the U and V channels:

    U' = U·cos(θ) − V·sin(θ)
    V' = U·sin(θ) + V·cos(θ)

where θ is the per-scanline rotation angle from the hue channel waveform. This rotates the colour vector around the achromatic axis (the Y axis), shifting reds toward greens, greens toward blues, and so on. Because the rotation angle varies per scanline, different horizontal bands of the image shift to different hues, creating rainbow striping effects.

### Scanline Displacement

Horizontal displacement shifts an entire scanline left or right by a number of pixels determined by the displacement channel waveform value. This is equivalent to per-scanline horizontal scroll — the same technique used for the Mode 7-adjacent wavy distortions in games like Chrono Trigger and Secret of Mana. When the displacement varies sinusoidally from line to line, straight vertical edges become sinusoidal curves, and the entire image appears to wobble.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Timing / Phase Accumulators ──────────────────────────────
│   │
│   ├─ 1. Global animation counter (incremented per frame)
│   ├─ 2. Speed toggle: doubles animation increment rate
│   └─ 3. Per-scanline phase = line_number × frequency + anim_phase
│
├── Waveform Generation (3 channels) ────────────────────────
│   │
│   ├─ 4a. Brightness: sine or square, from quarter-wave LUT
│   ├─ 4b. Hue: sine or triangle, from quarter-wave LUT
│   └─ 4c. Displacement: sine or sawtooth, from quarter-wave LUT
│
├── Brightness Modulation ───────────────────────────────────
│   │
│   └─ 5. Y' = Y + brt_wave_value × brt_depth
│
├── Hue Rotation ────────────────────────────────────────────
│   │
│   └─ 6. U', V' = rotate(U, V) by hue_wave_value × hue_depth
│
├── Displacement Read ───────────────────────────────────────
│   │
│   └─ 7. pixel[x] = input[x + disp_wave_value × disp_depth]
│          (per-scanline horizontal shift via line buffer)
│
├── Mix ─────────────────────────────────────────────────────
│   └─ Interpolator: dry (original) ↔ wet (modulated)
│
└── Bypass ──────────────────────────────────────────────────
    └─ Select original or processed signal
```

The three modulation channels operate independently but share the same global animation counter, creating coherent visual motion even at different frequencies. The processing order matters: brightness modulation is applied first (modifying Y), then hue rotation (modifying U and V), then displacement (shifting pixel positions horizontally). This ordering means displaced pixels carry their already-brightness-and-hue-modified values, which is visually correct — it looks like the image was distorted as a whole rather than having its attributes independently scrambled. The two line buffers in BRAM store the current and previous scanlines, enabling the displacement stage to read pixels from shifted horizontal positions without corrupting the active output row.

---

## Parameter Reference

<img src={undulate_control_panel} alt="Videomancer front panel with Undulate loaded"/>
*Videomancer's front panel with Undulate active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Brt Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the spatial frequency of the brightness modulation waveform. At zero, the waveform completes no cycles within the frame and produces a uniform brightness shift. As Brt Freq increases, more complete wave cycles fit within the frame height, creating narrower brightness bands. At maximum, the bands are fine enough to produce a scanline-like striping effect reminiscent of CRT phosphor glow patterns.

---

#### Knob 2 — Brt Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls the amplitude of the brightness modulation. At zero, no brightness variation occurs regardless of frequency. As Brt Depth increases, the brightness bands become more pronounced — light areas become brighter and dark areas become darker in the wave trough. At maximum, the modulation can drive luminance from near-black to near-white, creating dramatic pulsing bands of light and shadow across the frame.

---

#### Knob 3 — Hue Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the spatial frequency of the hue rotation waveform. At zero, a single uniform hue shift applies to the entire frame. As Hue Freq increases, more rotation cycles fit within the frame, creating narrower bands of hue variation — rainbow striping when depth is high enough. The frequency relationship between the hue and brightness channels determines whether the colour bands align with or cut across the brightness bands.

---

#### Knob 4 — Hue Depth
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 106° |
| Suffix | ° |

Controls the maximum angle of per-scanline hue rotation. At 0°, no hue shift occurs. As Hue Depth increases, the angle of UV rotation grows, sweeping through more of the colour wheel per cycle. At 360°, a full revolution maps all hues within a single wave cycle, creating complete rainbow bands. The polar degree scale maps directly to the rotation matrix angle.

---

#### Knob 5 — Disp Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 19.6% |
| Suffix | % |

Controls the spatial frequency of the horizontal displacement waveform. At zero, the displacement is uniform across the frame (no wobble). As Disp Freq increases, the displacement varies more rapidly from line to line, creating tighter wobble patterns. At maximum, every few scanlines shift in opposing directions, producing a fine tearing effect.

---

#### Knob 6 — Disp Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Controls the amplitude of the horizontal displacement — how many pixels each scanline shifts. At zero, no displacement occurs. As Disp Depth increases, scanlines shift by progressively more pixels, creating wider wobble. At maximum, scanlines can shift by a substantial fraction of the frame width, tearing the image into jagged horizontal strips. The interaction between displacement frequency and depth determines whether the distortion looks like gentle underwater wobble or violent horizontal glitching.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Brt Wave** | Sine | Square |
| **8 — Hue Wave** | Sine | Tri |
| **9 — Speed** | Slow | Fast |
| **10 — Disp Wave** | Sine | Saw |
| **11 — Bypass** | Off | On |

The five toggles control the waveform shapes and animation speed of the three modulation channels. Each waveform toggle selects between two shapes optimised for different aesthetic effects: smooth sinusoidal motion versus sharp geometric modulation. The Speed toggle globally doubles the animation rate, and Bypass provides instant comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfade between the dry (original) and wet (modulated) signals. At 0%, the output is pure unprocessed video. At 100%, the output is the full per-scanline modulation with brightness, hue, and displacement effects. Intermediate values produce a proportional blend that can soften the intensity of the modulation without changing the waveform characteristics.

---

## Guided Exercises

These exercises build from single-channel modulation to complex multi-channel waveform interactions, exploring how per-scanline video processing creates motion from mathematics.

### Exercise 1: Brightness Bands

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: undulate_source1_kodim15, after: undulate_exercise1_result },
    { label: "Kodim03", before: undulate_source2_kodim03, after: undulate_exercise1_result },
    { label: "Kodim15 B&W", before: undulate_source3_kodim15_bw, after: undulate_exercise1_result },
  ]}
/>
*Brightness Bands — simulated result across source images.*
**Source**: A still image or camera feed with moderate contrast — a face, a landscape, or any subject with detail across the brightness range.

**Objective**: Create smooth horizontal brightness bands and understand frequency/depth interaction.

1. **Isolate brightness**: Set Brt Freq to ~25% and Brt Depth to ~50%. Leave Hue Depth and Disp Depth at 0%.
2. **Observe the bands**: Gentle bands of light and dark ripple across the image vertically.
3. **Increase frequency**: Push Brt Freq to ~75%. Watch the bands narrow and multiply.
4. **Try Square wave**: Toggle Brt Wave to Square. The smooth undulations snap to hard-edged stripes.
5. **Maximum depth**: Push Brt Depth to 100%. The bands now span near-black to near-white.

**Key concepts**: Frequency controls band count, depth controls band intensity, sine vs square changes the transition profile, single-channel modulation is clean and rhythmic

---

### Exercise 2: Rainbow Striping

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: undulate_source1_kodim15, after: undulate_exercise2_result },
    { label: "Kodim03", before: undulate_source2_kodim03, after: undulate_exercise2_result },
    { label: "Kodim15 B&W", before: undulate_source3_kodim15_bw, after: undulate_exercise2_result },
  ]}
/>
*Rainbow Striping — simulated result across source images.*
**Source**: A monochrome or desaturated scene — black-and-white photography, a grey wall, or a dim room.

**Objective**: Apply per-scanline hue rotation to paint rainbow bands across a neutral source, then combine with brightness modulation.

1. **Set up hue rotation**: Hue Freq ~30%, Hue Depth ~180°. Rainbow bands appear across the frame.
2. **Try Triangle wave**: Toggle Hue Wave to Tri. The smooth rainbow gradients sharpen into linear ramps.
3. **Add brightness**: Set Brt Freq to a different value (~40%) and Brt Depth to ~30%.
4. **Observe the interference**: Because the two channels run at different frequencies, their bands create a moire-like interference pattern — something not easily achievable with single-channel processing.
5. **Speed up**: Toggle Speed to Fast. The rainbow bands and brightness bands now ripple through the frame more quickly.

**Key concepts**: Hue rotation creates rainbow bands in achromatic or desaturated footage, triangle wave produces sharper colour boundaries, different channel frequencies create interference, speed toggle controls animation rate globally

---

### Exercise 3: Full Undulation

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: undulate_source1_kodim15, after: undulate_exercise3_result },
    { label: "Kodim03", before: undulate_source2_kodim03, after: undulate_exercise3_result },
    { label: "Kodim15 B&W", before: undulate_source3_kodim15_bw, after: undulate_exercise3_result },
  ]}
/>
*Full Undulation — simulated result across source images.*
**Source**: A high-detail scene with strong vertical lines — architecture, text, barcodes, or patterns with geometric regularity.

**Objective**: Engage all three modulation channels simultaneously to create the full per-scanline undulation effect.

1. **Start with displacement**: Set Disp Freq to ~40%, Disp Depth to ~30%. Watch the vertical lines wobble sinusoidally.
2. **Try Sawtooth**: Toggle Disp Wave to Saw. The smooth wobble becomes an asymmetric shear.
3. **Add brightness**: Brt Freq ~25%, Brt Depth ~40%, Sine wave.
4. **Add hue**: Hue Freq ~35%, Hue Depth ~120°, Sine wave.
5. **Observe the composite**: All three channels modulate the image simultaneously — it wobbles, brightens, and shifts colour in overlapping wave patterns.
6. **Speed for energy**: Toggle Speed to Fast for a dynamic, music-performance-ready effect.
7. **Back off Mix**: Lower Mix to ~60% to soften the composite while retaining the sense of motion.

**Key concepts**: Three-channel interaction creates complex visual textures from simple waveforms, sawtooth displacement creates glitch-like tearing, mismatched frequencies prevent visual repetition, mix acts as a global intensity control

---


## Tips

- **Start with one channel**: The three-channel interaction can be overwhelming. Master brightness modulation alone first, then add hue, then displacement.
- **Displacement makes it physical**: Brightness and hue feel like light effects; displacement physically moves the image, adding a sense of weight and substance to the modulation.
- **Mismatched frequencies create complexity**: Setting all three channels to the same frequency creates orderly, periodic bands. Setting them to different frequencies creates evolving interference patterns that never exactly repeat.
- **Square brightness for scanlines**: Setting Brt Wave to Square with high frequency and moderate depth produces a convincing CRT scanline effect — hard-edged horizontal stripes of alternating brightness.
- **Low displacement for underwater**: Disp Freq ~20%, Disp Depth ~10% with Sine wave produces the gentle wobble associated with viewing objects through moving water.
- **Sawtooth for glitch art**: Sawtooth displacement combined with fast speed and high depth tears the image apart with an aggressive, digital corruption aesthetic.
- **Hue on monochrome sources**: Applying hue rotation to a desaturated or black-and-white source paints the frame with pure synthetic colour bands — a powerful effect that adds colour to colourless material.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated FPGA memory used for the quarter-wave sine LUT and scanline line buffers. |
| **DDS** | Direct Digital Synthesis; a phase-accumulator method for generating periodic waveforms from a fixed-rate clock. |
| **HDMA** | Horizontal DMA; a Super Nintendo hardware feature that updates video registers at the start of each scanline. |
| **Hue Rotation** | A 2D rotation applied to the U and V chrominance channels, shifting all colours around the colour wheel. |
| **LFSR** | Linear-Feedback Shift Register; though not directly used in Undulate, it is a common waveform source in companion programs. |
| **Per-Scanline Modulation** | Applying a different processing parameter value to each horizontal line, creating vertically-varying effects. |
| **Phase Accumulator** | A counter that increments by a frequency-related value per clock cycle; its current value determines the waveform phase. |
| **Quarter-Wave LUT** | A lookup table storing one quarter of a sine wave period; full sine/cosine access is achieved through mirroring and sign-flipping. |
| **Sawtooth Wave** | A waveform that ramps linearly from minimum to maximum then resets, producing asymmetric modulation. |
| **Triangle Wave** | A waveform that ramps linearly up then linearly down, creating angular modulation with sharper peaks than sine. |
| **UV Rotation** | Synonymous with hue rotation; rotating the chrominance vector in the UV colour plane. |
| **YUV** | A colour encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
