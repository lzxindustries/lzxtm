---
draft: true
sidebar_position: 180
slug: /instruments/videomancer/ludosphere
title: "Ludosphere"
image: /img/instruments/videomancer/ludosphere/ludosphere_hero_s1.png
description: "Take three spinning wheels — one sweeping left to right across the screen, one sweeping top to bottom, and one pulsing forward through time."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import ludosphere_control_panel from '/img/instruments/videomancer/ludosphere/ludosphere_control_panel.png';
import ludosphere_source1_dog from '/img/instruments/videomancer/ludosphere/ludosphere_source1_dog.png';
import ludosphere_source2_runner from '/img/instruments/videomancer/ludosphere/ludosphere_source2_runner.png';
import ludosphere_source3_collage from '/img/instruments/videomancer/ludosphere/ludosphere_source3_collage.png';
import ludosphere_source4_pattern from '/img/instruments/videomancer/ludosphere/ludosphere_source4_pattern.png';
import ludosphere_source5_girl from '/img/instruments/videomancer/ludosphere/ludosphere_source5_girl.png';
import ludosphere_source6_wood from '/img/instruments/videomancer/ludosphere/ludosphere_source6_wood.png';
import ludosphere_hero_s1 from '/img/instruments/videomancer/ludosphere/ludosphere_hero_s1.png';
import ludosphere_hero_s2 from '/img/instruments/videomancer/ludosphere/ludosphere_hero_s2.png';
import ludosphere_hero_s3 from '/img/instruments/videomancer/ludosphere/ludosphere_hero_s3.png';
import ludosphere_hero_s4 from '/img/instruments/videomancer/ludosphere/ludosphere_hero_s4.png';
import ludosphere_hero_s5 from '/img/instruments/videomancer/ludosphere/ludosphere_hero_s5.png';
import ludosphere_hero_s6 from '/img/instruments/videomancer/ludosphere/ludosphere_hero_s6.png';
import ludosphere_ex1_s1 from '/img/instruments/videomancer/ludosphere/ludosphere_ex1_s1.png';
import ludosphere_ex1_s2 from '/img/instruments/videomancer/ludosphere/ludosphere_ex1_s2.png';
import ludosphere_ex1_s3 from '/img/instruments/videomancer/ludosphere/ludosphere_ex1_s3.png';
import ludosphere_ex1_s4 from '/img/instruments/videomancer/ludosphere/ludosphere_ex1_s4.png';
import ludosphere_ex1_s5 from '/img/instruments/videomancer/ludosphere/ludosphere_ex1_s5.png';
import ludosphere_ex1_s6 from '/img/instruments/videomancer/ludosphere/ludosphere_ex1_s6.png';
import ludosphere_ex2_s1 from '/img/instruments/videomancer/ludosphere/ludosphere_ex2_s1.png';
import ludosphere_ex2_s2 from '/img/instruments/videomancer/ludosphere/ludosphere_ex2_s2.png';
import ludosphere_ex2_s3 from '/img/instruments/videomancer/ludosphere/ludosphere_ex2_s3.png';
import ludosphere_ex2_s4 from '/img/instruments/videomancer/ludosphere/ludosphere_ex2_s4.png';
import ludosphere_ex2_s5 from '/img/instruments/videomancer/ludosphere/ludosphere_ex2_s5.png';
import ludosphere_ex2_s6 from '/img/instruments/videomancer/ludosphere/ludosphere_ex2_s6.png';
import ludosphere_ex3_s1 from '/img/instruments/videomancer/ludosphere/ludosphere_ex3_s1.png';
import ludosphere_ex3_s2 from '/img/instruments/videomancer/ludosphere/ludosphere_ex3_s2.png';
import ludosphere_ex3_s3 from '/img/instruments/videomancer/ludosphere/ludosphere_ex3_s3.png';
import ludosphere_ex3_s4 from '/img/instruments/videomancer/ludosphere/ludosphere_ex3_s4.png';
import ludosphere_ex3_s5 from '/img/instruments/videomancer/ludosphere/ludosphere_ex3_s5.png';
import ludosphere_ex3_s6 from '/img/instruments/videomancer/ludosphere/ludosphere_ex3_s6.png';

# Ludosphere

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: ludosphere_source1_dog, after: ludosphere_hero_s1 },
    { label: "Runner", before: ludosphere_source2_runner, after: ludosphere_hero_s2 },
    { label: "Collage", before: ludosphere_source3_collage, after: ludosphere_hero_s3 },
    { label: "Pattern", before: ludosphere_source4_pattern, after: ludosphere_hero_s4 },
    { label: "Girl", before: ludosphere_source5_girl, after: ludosphere_hero_s5 },
    { label: "Wood", before: ludosphere_source6_wood, after: ludosphere_hero_s6 },
  ]}
/>
*Ludosphere applying three-axis oscillator modulation to produce spherical color patterns across the video frame.*

---

## Overview

Take three spinning wheels — one sweeping left to right across the screen, one sweeping top to bottom, and one pulsing forward through time. Each wheel generates a smooth waveform that can modulate the brightness of the source video or paint new color across it. Ludosphere is a three-axis oscillator colorizer: a direct digital synthesis (DDS) engine that layers spatial and temporal waveforms onto the video signal.

The name evokes *ludo* (play) and *sphere* — a playful sphere of oscillating color. The three oscillators are completely independent. Each has its own frequency (Clock), its own modulation depth (Mod), and its own waveshape selector (Flip). At zero modulation depth the oscillator output replaces the video entirely, producing pure geometric ramp or triangle patterns. As modulation increases, the source video and oscillator blend additively, creating luminance-dependent patterning. Colorize mode routes the vertical and frame-rate oscillators into the chroma channels, transforming the pattern from monochrome undulation into full-spectrum color.

This is a ported program that predates the Videomancer ABI standard. Several toggles and the fader read from registers that fall outside the 8-register hardware interface, meaning F Flip, Colorize, Bypass, and Shift will respond to unpredictable data in the current ABI. Despite this limitation, the horizontal and vertical oscillator controls function correctly and produce the program's signature spatial modulation effects.

---

## Quick Start

1. **Start with one axis**: Ludosphere is most intuitive when you build the pattern one axis at a time — set H Clock and H Mod first, then add vertical, then temporal.
2. **Zero Mod for pure geometry**: Setting all Mod knobs to zero removes source video entirely, turning Ludosphere into a pure geometric pattern generator ideal for texture backgrounds.
3. **Frequency ratios create structure**: Integer ratios between H Clock and V Clock (1:1, 2:1, 3:2) produce regular grid and diamond tilings; irrational ratios produce more organic, continuously varying patterns.

---

## Background

### Direct Digital Synthesis

Ludosphere's oscillators are built on DDS phase accumulators — a technique borrowed from RF signal generation. A 16-bit accumulator adds a frequency word on every relevant video event (pixel clock, line start, or frame start). The upper bits of the accumulator form a sawtooth ramp. The frequency word sets how fast the ramp sweeps: small values produce slow, wide patterns; large values produce dense, rapid oscillation. Because the accumulator is purely integer arithmetic, the frequency is perfectly stable — no drift, no jitter, no analog tuning errors.

### Sawtooth-to-Triangle Conversion

The frequency doubler module folds a sawtooth ramp at its midpoint. Values below 512 are scaled upward; values above 512 are mirrored downward. The result is a symmetric triangle wave — zero at the edges, peak in the center. Visually, this transforms a hard-edged ramp gradient into a smooth undulation that rises and falls symmetrically. The Flip toggle on each axis selects between the raw sawtooth (sharp discontinuity at wrap-around) and the folded triangle (smooth peaks and valleys).

### Proc Amp as Modulator

The proc_amp_u module is normally a brightness/contrast stage, but Ludosphere repurposes it as a modulator. The input video's luminance feeds the contrast port while the oscillator waveform feeds the brightness port. When modulation depth (contrast) is zero, the output equals the oscillator waveform — pure pattern, no source video. When modulation depth is at midpoint (512), the source luma is added at unity gain. The result is an additive blend where the oscillator provides a base pattern and the source video rides on top. This creates the characteristic effect where brighter regions of the source push through the oscillator pattern more visibly than darker regions.

### Chroma Shift and Color Space Rotation

The Shift control adds a signed offset to the U and V chroma channels when Colorize is active. Because YUV chroma is circular (values that exceed the range wrap around), shifting the offset smoothly rotates the generated color through the chroma plane. A slow sweep of Shift produces a continuously cycling color palette in the oscillator-driven regions.

### Video Timing and Accumulator Ranges

Each DDS accumulator operates on a different timing domain. The horizontal accumulator advances on every pixel clock, resetting at the start of each active line — it creates patterns that repeat across the width of the frame. The vertical accumulator advances once per line, resetting at the top of each field — it creates patterns that repeat vertically. The frame accumulator advances once per field and never resets, producing slow temporal variation that evolves over many seconds.


---

## Signal Flow

Video Timing Generator → Phase Accumulators → Waveshapers → Luma Modulation → Shift Offset → Output Mux

```
Input Video (YUV 4:4:4)
│
├── Video Timing Generator ─────────────────────────────────────
│   └─ Extract hsync/vsync/avid edges → t_video_timing_port
│
├── Phase Accumulators (3× video_timing_accumulator) ───────────
│   ├─ H: pixel-rate DDS       (freq = H Clock, resets per line)
│   ├─ V: line-rate DDS        (freq = V Clock, resets per field)
│   └─ F: frame-rate DDS       (freq = F Clock, free-running)
│
├── Waveshapers (3× frequency_doubler) ─────────────────────────
│   ├─ H Flip off: sawtooth    │  H Flip on: triangle
│   ├─ V Flip off: sawtooth    │  V Flip on: triangle
│   └─ F Flip off: sawtooth    │  F Flip on: triangle
│
├── Luma Modulation (3× proc_amp_u) ────────────────────────────
│   ├─ H: wave_h × input Y     (depth = H Mod)
│   ├─ V: wave_v × input Y     (depth = V Mod)
│   └─ F: wave_f × input Y     (depth = F Mod)
│
├── Shift Offset (Colorize path) ───────────────────────────────
│   ├─ U out = mod_v + Shift − 512   (wrapping add)
│   └─ V out = mod_f + Shift − 512   (wrapping add)
│
└── Output Mux ─────────────────────────────────────────────────
    ├─ Bypass=1: pass input unchanged
    ├─ Colorize=1: Y=mod_h, U=shifted_v, V=shifted_f
    └─ Colorize=0: Y=mod_h, U=input_U, V=input_V
```

The three oscillators share no state — each operates on an independent phase accumulator at a different timing scale. The horizontal oscillator creates patterns tied to horizontal position within each line, the vertical to line position, and the frame-rate to temporal position across frames. When all three modulation depths are set to moderate values, the source video appears multiplied by a three-dimensional standing wave that creates the program's signature spherical interference patterns. The Colorize output mux separates concerns: the horizontal axis always drives luminance, while the vertical and frame-rate axes drive chrominance (with the Shift offset rotating hue).

---

## Parameter Reference

<img src={ludosphere_control_panel} alt="Videomancer front panel with Ludosphere loaded"/>
*Videomancer's front panel with Ludosphere active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — H Clock
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Horizontal oscillator frequency word. Low values produce a single wide gradient across the frame — the ramp cycles slowly from left to right. Higher values compress the pattern into multiple oscillation cycles per line, creating vertical stripe patterns. Because the accumulator resets at each active-video start, the horizontal pattern is always phase-locked to the left edge of the frame. At very high values the pattern aliases, producing moire-like interference with the pixel grid.

---

#### Knob 2 — V Clock
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Vertical oscillator frequency word. Low values produce a single gradient from top to bottom of the frame. Higher values create horizontal stripe patterns by completing multiple accumulator cycles across the field height. The vertical accumulator resets at each vsync, so the pattern is phase-locked to the top of the frame. Combined with H Clock, these two controls define the spatial frequency grid of the oscillator pattern.

---

#### Knob 3 — F Clock
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Frame-rate oscillator frequency word. This accumulator advances once per field (approximately 60 Hz for HD, 50 Hz for PAL) and never resets. Low values create a very slow temporal pulsation — the entire frame brightens and dims over several seconds. Higher values create faster flicker that can appear as a strobe or rapid color cycling when Colorize is active. Because it is free-running, the frame oscillator produces continuous temporal evolution independent of spatial position.

---

#### Knob 4 — H Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Horizontal luma modulation depth. At zero, the proc_amp output equals the H oscillator waveform — pure horizontal pattern with no source video contribution. As the value increases, the source video luminance is additively blended with the oscillator. At midpoint, the source and oscillator contribute equally. Higher values further emphasize the source content riding on the oscillator wave. This control sets the balance between abstract generated pattern and video-modulated texture on the Y output channel.

---

#### Knob 5 — V Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Vertical luma modulation depth. Functions identically to H Mod but applies to the vertical oscillator. When Colorize is active, this axis drives the U chroma channel after shift offset is applied. At zero modulation, the U output is a pure vertical oscillator pattern. Increasing V Mod blends source luminance into the chroma pattern, creating luminance-keyed color bands.

---

#### Knob 6 — F Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Frame-rate luma modulation depth. Applies to the temporal oscillator which drives the V chroma channel when Colorize is active. At zero, the V output pulses as a pure frame-rate oscillation. Increasing F Mod ties the temporal pulsation to source brightness — bright areas pulse at full amplitude while dark areas remain near neutral. This creates content-dependent color animation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — H Flip** | Off | On |
| **8 — V Flip** | Off | On |
| **9 — F Flip** | Off | On |
| **10 — Colorize** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles have split responsibilities. H Flip and V Flip control waveshape on their respective spatial axes and function correctly through the standard ABI registers. F Flip, Colorize, and Bypass read from out-of-bounds registers (8, 9, 10) and will not respond to the physical toggle switches — their effective values depend on whatever data the FPGA bus presents at those addresses. The fader (register 7) has its bit 0 read as V Flip, which means the fader position can inadvertently affect the vertical waveshape.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Shift
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Chroma shift offset. Adds a signed value (register value minus 512) to both U and V channels when Colorize is active. Sweeping the fader rotates the generated chroma through the YUV color wheel — a full sweep covers approximately one complete hue rotation. Reads from register 11 (out of bounds) so the physical fader does not control this parameter in the current ABI.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises focus on the working controls (H Clock, V Clock, F Clock, H Mod, V Mod, F Mod, H Flip) to explore Ludosphere's spatial and temporal oscillation effects.

### Exercise 1: Spatial Interference Grid

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: ludosphere_source1_dog, after: ludosphere_ex1_s1 },
    { label: "Runner", before: ludosphere_source2_runner, after: ludosphere_ex1_s2 },
    { label: "Collage", before: ludosphere_source3_collage, after: ludosphere_ex1_s3 },
    { label: "Pattern", before: ludosphere_source4_pattern, after: ludosphere_ex1_s4 },
    { label: "Girl", before: ludosphere_source5_girl, after: ludosphere_ex1_s5 },
    { label: "Wood", before: ludosphere_source6_wood, after: ludosphere_ex1_s6 },
  ]}
/>
*Spatial Interference Grid — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and moderate contrast.

**What You'll Create**: Learn how horizontal and vertical oscillators create a spatial modulation grid that interacts with the source video.

1. **Single horizontal ramp**: Set H Clock to about 20%. A single wide gradient sweeps across the frame from left to right.
2. **Add vertical**: Set V Clock to about 20%. A second gradient sweeps top to bottom. The two multiply together, creating a diagonal pattern.
3. **Increase frequencies**: Raise both H Clock and V Clock to about 60%. The pattern becomes a tighter grid of bright and dark regions.
4. **Triangle mode**: Toggle H Flip on. The horizontal hard-edged ramp becomes a smooth undulation. Compare the two textures.
5. **Add modulation**: Raise H Mod and V Mod to about 50%. The source video begins to appear within the oscillator pattern — brighter regions of the source push through the grid.

**Key concepts**: DDS phase accumulators create perfectly stable spatial frequency patterns, the frequency_doubler converts sawtooth to triangle for different visual textures, modulation depth controls the balance between generated pattern and source video content

---

### Exercise 2: Temporal Pulsation

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: ludosphere_source1_dog, after: ludosphere_ex2_s1 },
    { label: "Runner", before: ludosphere_source2_runner, after: ludosphere_ex2_s2 },
    { label: "Collage", before: ludosphere_source3_collage, after: ludosphere_ex2_s3 },
    { label: "Pattern", before: ludosphere_source4_pattern, after: ludosphere_ex2_s4 },
    { label: "Girl", before: ludosphere_source5_girl, after: ludosphere_ex2_s5 },
    { label: "Wood", before: ludosphere_source6_wood, after: ludosphere_ex2_s6 },
  ]}
/>
*Temporal Pulsation — simulated result across source images.*
**Source**: A static image or slow-moving footage so the temporal effect is clearly visible.

**What You'll Create**: Explore how the frame-rate oscillator adds temporal animation to the spatial modulation pattern.

1. **Spatial base**: Set H Clock ~40%, V Clock ~40%, both Mod controls at ~50%. Establish a visible spatial grid modulating the source.
2. **Slow pulse**: Set F Clock to about 10%. The entire frame slowly brightens and dims over several seconds as the frame accumulator sweeps.
3. **Faster pulse**: Raise F Clock to about 40%. The pulsation quickens to a visible strobe-like flicker.
4. **Frame modulation**: Set F Mod to about 50%. Now the temporal pulse is modulated by source brightness — bright areas pulse while dark areas remain steady.
5. **All three axes**: With all three oscillators running, the pattern becomes a three-dimensional standing wave that evolves over time. Adjust the three Clock controls to find rhythmic interference patterns.

**Key concepts**: The frame-rate accumulator advances once per field and never resets, creating temporal evolution independent of spatial position; three independent oscillators interfere constructively and destructively to produce complex evolving patterns

---

### Exercise 3: Pure Oscillator Patterns

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: ludosphere_source1_dog, after: ludosphere_ex3_s1 },
    { label: "Runner", before: ludosphere_source2_runner, after: ludosphere_ex3_s2 },
    { label: "Collage", before: ludosphere_source3_collage, after: ludosphere_ex3_s3 },
    { label: "Pattern", before: ludosphere_source4_pattern, after: ludosphere_ex3_s4 },
    { label: "Girl", before: ludosphere_source5_girl, after: ludosphere_ex3_s5 },
    { label: "Wood", before: ludosphere_source6_wood, after: ludosphere_ex3_s6 },
  ]}
/>
*Pure Oscillator Patterns — simulated result across source images.*
**Source**: Any footage — the source video will be overwhelmed by the oscillator output.

**What You'll Create**: Explore the raw geometric patterns produced when modulation depth is at zero, removing source video contribution entirely.

1. **Zero modulation**: Set H Mod, V Mod, and F Mod all to 0%. The proc_amp now outputs pure oscillator waveform with no source video content.
2. **Horizontal ramp**: Set H Clock to about 30%, V Clock and F Clock to 0%. A single horizontal gradient fills the frame.
3. **Cross pattern**: Raise V Clock to about 30%. The horizontal and vertical ramps multiply to form a diagonal cross pattern.
4. **Triangle folding**: Toggle H Flip on. The sharp ramp becomes a smooth hill. The cross pattern becomes a diamond or ellipse.
5. **Frequency ratios**: Set H Clock to exactly 2× V Clock. The horizontal pattern has twice as many cycles as the vertical, creating a 2:1 Lissajous-like grid. Try 3:1 and 4:1 ratios for more complex geometric tilings.

**Key concepts**: At zero modulation depth the proc_amp outputs pure oscillator waveform, frequency ratios between H and V create different geometric tilings, sawtooth vs triangle waveshape dramatically changes the visual character of the pattern

---


## Tips

- **Triangle smooths, sawtooth edges**: Use H Flip to choose between smooth undulations (triangle) and hard gradient edges (sawtooth). Triangle mode is gentler on the eye; sawtooth creates sharper geometric edges.
- **Temporal animation is free-running**: The frame oscillator never resets, so it drifts continuously. This is ideal for slowly evolving texture but means the pattern never returns to exactly the same state.
- **Working controls only**: In the current ABI, only pots 1–6 and toggle 7 (H Flip) respond predictably. Plan your patches around these controls.
- **Feedback loops**: Routing Ludosphere output back into its input creates recursive oscillator patterns that evolve chaotically and can produce video fractals at certain frequency ratios.

---

## Glossary

| Term | Definition |
|------|------------|
| **ABI** | Application Binary Interface; the 8-register communication protocol between the firmware and FPGA program. Ludosphere reads beyond this range. |
| **Accumulator** | A register that sums a frequency word on each clock event, producing a linearly sweeping ramp. |
| **Chroma** | The color information in a video signal, encoded as U and V channels in YUV color space. |
| **DDS** | Direct Digital Synthesis; a technique for generating precise waveforms using a phase accumulator and frequency word. |
| **Frequency Doubler** | A waveshaper that folds a sawtooth ramp at its midpoint to produce a symmetric triangle wave. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Phase Accumulator** | An integer register that adds a fixed increment on each event, sweeping through its range to produce a ramp waveform. |
| **Proc Amp** | Processing Amplifier; a brightness/contrast stage. In Ludosphere, repurposed as a modulator blending oscillator and source. |
| **Triangle Wave** | A symmetric waveform that ramps linearly up then linearly down, with no discontinuity at the peaks. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
