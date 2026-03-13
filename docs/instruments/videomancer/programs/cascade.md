---
draft: true
sidebar_position: 39
slug: /instruments/videomancer/cascade
title: "Cascade"
image: /img/instruments/videomancer/cascade/cascade_hero_s1.png
description: "A CRT phosphor does not turn off instantly."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import cascade_control_panel from '/img/instruments/videomancer/cascade/cascade_control_panel.png';
import cascade_source1_house from '/img/instruments/videomancer/cascade/cascade_source1_house.png';
import cascade_source2_skull from '/img/instruments/videomancer/cascade/cascade_source2_skull.png';
import cascade_source3_clouds from '/img/instruments/videomancer/cascade/cascade_source3_clouds.png';
import cascade_source4_pattern from '/img/instruments/videomancer/cascade/cascade_source4_pattern.png';
import cascade_source5_woman from '/img/instruments/videomancer/cascade/cascade_source5_woman.png';
import cascade_source6_knit from '/img/instruments/videomancer/cascade/cascade_source6_knit.png';
import cascade_hero_s1 from '/img/instruments/videomancer/cascade/cascade_hero_s1.png';
import cascade_hero_s2 from '/img/instruments/videomancer/cascade/cascade_hero_s2.png';
import cascade_hero_s3 from '/img/instruments/videomancer/cascade/cascade_hero_s3.png';
import cascade_hero_s4 from '/img/instruments/videomancer/cascade/cascade_hero_s4.png';
import cascade_hero_s5 from '/img/instruments/videomancer/cascade/cascade_hero_s5.png';
import cascade_hero_s6 from '/img/instruments/videomancer/cascade/cascade_hero_s6.png';
import cascade_ex1_s1 from '/img/instruments/videomancer/cascade/cascade_ex1_s1.png';
import cascade_ex1_s2 from '/img/instruments/videomancer/cascade/cascade_ex1_s2.png';
import cascade_ex1_s3 from '/img/instruments/videomancer/cascade/cascade_ex1_s3.png';
import cascade_ex1_s4 from '/img/instruments/videomancer/cascade/cascade_ex1_s4.png';
import cascade_ex1_s5 from '/img/instruments/videomancer/cascade/cascade_ex1_s5.png';
import cascade_ex1_s6 from '/img/instruments/videomancer/cascade/cascade_ex1_s6.png';
import cascade_ex2_s1 from '/img/instruments/videomancer/cascade/cascade_ex2_s1.png';
import cascade_ex2_s2 from '/img/instruments/videomancer/cascade/cascade_ex2_s2.png';
import cascade_ex2_s3 from '/img/instruments/videomancer/cascade/cascade_ex2_s3.png';
import cascade_ex2_s4 from '/img/instruments/videomancer/cascade/cascade_ex2_s4.png';
import cascade_ex2_s5 from '/img/instruments/videomancer/cascade/cascade_ex2_s5.png';
import cascade_ex2_s6 from '/img/instruments/videomancer/cascade/cascade_ex2_s6.png';
import cascade_ex3_s1 from '/img/instruments/videomancer/cascade/cascade_ex3_s1.png';
import cascade_ex3_s2 from '/img/instruments/videomancer/cascade/cascade_ex3_s2.png';
import cascade_ex3_s3 from '/img/instruments/videomancer/cascade/cascade_ex3_s3.png';
import cascade_ex3_s4 from '/img/instruments/videomancer/cascade/cascade_ex3_s4.png';
import cascade_ex3_s5 from '/img/instruments/videomancer/cascade/cascade_ex3_s5.png';
import cascade_ex3_s6 from '/img/instruments/videomancer/cascade/cascade_ex3_s6.png';

# Cascade

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "House", before: cascade_source1_house, after: cascade_hero_s1 },
    { label: "Skull", before: cascade_source2_skull, after: cascade_hero_s2 },
    { label: "Clouds", before: cascade_source3_clouds, after: cascade_hero_s3 },
    { label: "Pattern", before: cascade_source4_pattern, after: cascade_hero_s4 },
    { label: "Woman", before: cascade_source5_woman, after: cascade_hero_s5 },
    { label: "Knit", before: cascade_source6_knit, after: cascade_hero_s6 },
  ]}
/>
*Cascade painting tinted scanline echoes across a portrait, each delay tap accumulating warm phosphor trails that bleed through the frame.*

---

## Overview

A CRT phosphor does not turn off instantly. When the electron beam moves on, the phosphor dot continues to glow — fading over microseconds or milliseconds depending on the chemistry. That afterglow produces ghostly trails that follow moving objects, a persistence that became part of the visual language of analogue television and early computer monitors. Cascade recreates that persistence digitally, using BRAM delay lines to store and replay scanline data with configurable read offsets.

The program provides two independent echo taps, each with its own delay control. The echoed signal can be tinted per-channel — luma gain for brightness control, and additive U/V offsets for colour shifting — producing coloured afterimage trails that evoke the warm amber of P1 phosphor, the cool blue of P11, or any arbitrary hue. A feedback toggle routes the mixed output back into the delay line input, creating iterative echo accumulation where each pass adds another layer of displaced, tinted imagery. The name *Cascade* refers to this waterfall of layered echoes, each one displaced further from the original and tinted deeper into the chosen colour.

At conservative settings, Cascade adds subtle ghost trails behind moving objects. At extreme settings with feedback enabled, it builds dense, recursive echo structures that fill the frame with displaced copies of the source — a digital stutter effect where the image trips over its own reflections. Freeze holds the contents of the delay buffer, mirror-read reverses the scan direction for kaleidoscopic symmetry, and luma modulation lets the source brightness dynamically warp the delay offset.

---

## Quick Start

1. **Start with one tap**: Set Echo 2 Delay to 0% while learning the controls. The interlaced dual-tap behaviour can be confusing — start with a clean single echo.
2. **Mix controls feedback intensity**: The Echo Mix fader doubles as a feedback gain control. Lower mix values create gentle decay trails; 100% mix creates sustained, non-decaying feedback loops.
3. **Tint after delay, before mix**: The tint is applied to the echo only — the dry signal passes through untouched. This means you can colour the trail without affecting the live image.

---

## Background

### Phosphor Persistence and CRT Afterimage

Cathode ray tubes create images by sweeping an electron beam across a phosphor-coated screen. Different phosphor compounds produce different persistence characteristics — the time the dot continues to emit light after the beam passes. Short-persistence phosphors (like P4, used in television) decay in microseconds, producing clean motion with minimal trailing. Long-persistence phosphors (like P7 or P39, used in radar displays) maintain a visible afterimage for seconds, creating green or amber ghost trails behind any moving feature. Cascade simulates this persistence by reading data from earlier positions in the scanline buffer, producing a displaced echo that overlays the current image like a phosphor trail frozen mid-decay.

### BRAM Ping-Pong Delay Lines

The delay effect is built on a `mirror_delay_line_slv` — a dual-bank BRAM structure that operates in a ping-pong configuration. While one bank writes the current scanline, the other bank serves reads from a configurable offset address. At the end of each line, the roles swap. This architecture provides sample-accurate random-access delay without stalling the video pipeline. The delay depth is 2048 samples (11-bit address space), consuming four BRAMs for the 30-bit packed YUV data path. Two independent read taps (A and B) share the structure, selected by the vertical accumulator alternating each line.

### Feedback Topology

In a standard delay configuration, the delay line input comes from the source video. The feedback toggle reroutes the delay line input to receive the *mixed output* — the result of blending dry signal with the tinted echo. Each frame, the echo feeds back through the delay and tint stages again, accumulating displacement and colour shift. The intensity of this feedback loop depends on the Echo Mix fader: at 100% wet, the feedback is maximum and echoes build rapidly; at lower mix values, each pass is attenuated, producing a more gradual trail that fades over several frames. Feedback combined with freeze creates a snapshot that the delay line replays indefinitely.

### Luma-Modulated Delay Offset

The Luma Mod control multiplies the input luminance by a scaling factor and adds the result to both echo delay offsets. This makes the delay distance dependent on the brightness of the source image — bright regions read from different delay positions than dark regions, warping the echo pattern across the frame. With luma inversion active, the brightness-to-delay mapping reverses: dark areas get maximum displacement while bright areas read from nearby positions. The modulation is computed as a 10-bit × 10-bit multiply, with the top 11 bits extracted as the offset.

### Colour Tinting

The echo signal passes through a per-channel tint stage before mixing. Luma tinting is multiplicative — the Echo Y Tint control acts as a gain factor, with 512 (midpoint) representing unity gain. Values below 512 darken the echo; values above brighten it toward clipping. Chroma tinting is additive — the Echo U Tint and Echo V Tint controls add signed offsets to the echo's colour channels, with 512 representing zero offset. This asymmetry matches the different natures of the channels: luma is a magnitude (gain is natural), while chroma is a signed deviation from neutral grey (offset is natural). Saturation clamping on all three channels prevents overflow.


---

## Signal Flow

Input Register → Feedback Mux → Luma Modulation → ... → Tint Stage 2 — Saturate → Interpolator Mix

```
Input Video (YUV 4:4:4)
│
├─ 1. Input Register + Luma Invert     (optional bitwise complement of Y)
│
├─ 2. Feedback Mux                     (select: input / previous mix output / freeze)
│      └─ if feedback=on & freeze=off → previous mix output → delay input
│      └─ if freeze=on → delay input held (zero Y, neutral UV)
│      └─ otherwise → input Y/U/V → delay input
│
├─ 3. Luma Modulation                  (Y × Luma Mod → delay offset)
│
├─ 4. YUV Pack → Mirror Delay Line     (30-bit packed, 2×2048 BRAM, dual taps A/B)
│      ├─ rd_offset_a = Echo Delay + luma mod offset
│      ├─ rd_offset_b = Echo 2 Delay + luma mod offset
│      ├─ mirror_a = Mirror Read toggle
│      └─ AB bank selected by vertical accumulator (alternates each line)
│
├─ 5. Echo Unpack + Register           (30-bit → Y + U + V, 1 clock)
│
├─ 6. Tint Stage 1 — Multiply / Add    (1 clock)
│      ├─ echo_Y × Echo Y Tint         (multiplicative gain)
│      ├─ echo_U + (Echo U Tint − 512) (additive offset)
│      └─ echo_V + (Echo V Tint − 512) (additive offset)
│
├─ 7. Tint Stage 2 — Saturate          (1 clock, clamp 0–1023)
│
├─ 8. Interpolator Mix (×3 channels)   (4 clocks — dry/wet crossfade)
│      └─ t = Echo Mix: 0 = dry (input), 1023 = wet (tinted echo)
│
├─ Sync/Data Delay Pipeline             (11-clock shift register for sync alignment)
│
└─ Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → delayed input Y/U/V + aligned sync
```

The critical feedback path runs from the interpolator output (stage 8) back to the feedback mux (stage 2). When feedback is enabled, the signal that was just mixed — already containing one iteration of delay and tint — becomes the input for the next frame's delay line. Each pass through the loop adds another layer of displacement and tint, with the mix fader controlling how much of each iteration survives. This creates exponential decay when mix is below 100%, or sustained accumulation at 100%.

The freeze mechanism works by blocking new data from entering the delay line — the feedback mux outputs black Y and neutral chroma, effectively holding whatever is already stored in the BRAM buffers. The frozen echo continues to be read and tinted, creating a static afterimage that the live signal paints over. When freeze is released, new data immediately begins overwriting the buffer.

The two echo taps (A and B) are not blended in parallel — the delay line selects between them using the vertical accumulator, alternating the active tap on each scanline. This creates an interlaced echo effect where odd and even lines can show different delay depths, producing a subtle spatial texture in the echo pattern.

---

## Parameter Reference

<img src={cascade_control_panel} alt="Videomancer front panel with Cascade loaded"/>
*Videomancer's front panel with Cascade active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Echo Delay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At 0% the echo reads from the current write position, producing no visible displacement. At 100% the echo reads from the maximum offset (2048 samples back), creating the longest possible trail. Because the delay line operates on packed scanlines, the displacement appears as a horizontal shift of the echoed image. The luma modulation offset is added on top of this base value, so the actual read position varies pixel-by-pixel when Luma Mod is active. Internally, sets the read offset for echo tap A — the primary delay distance measured in scanline samples.

---

#### Knob 2 — Echo 2 Delay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the read offset for echo tap B — the secondary delay distance. Tap B alternates with tap A on successive scanlines, so setting different values for the two taps creates a vertically interlaced echo where odd and even lines show different displacement depths. When both taps are set to the same value, the echo is uniform; when they differ, the echo acquires a horizontal-stripe texture that becomes more pronounced as the difference increases.

---

#### Knob 3 — Luma Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls how strongly the input luminance modulates the delay read offset. At 0% the delay offset is uniform across the frame, determined solely by the Echo Delay knobs. As Luma Mod increases, bright pixels read from further positions in the delay line while dark pixels read from closer positions, warping the echo pattern to follow the tonal structure of the source. With Luma Invert active, this mapping reverses — dark areas get maximum displacement. The modulation is a full 10×10-bit multiply, providing smooth control over the modulation depth.

---

#### Knob 4 — Echo Y Tint
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Controls the brightness gain applied to the echo signal. The tint stage multiplies the echo luma by this value, with 512 (centre position) representing unity gain — the echo retains its original brightness. Turning below centre darkens the echo toward black; turning above brightens it toward clipping. This lets you control how prominently the echo appears independently of the mix fader, creating subtle ghost trails (low gain) or bright afterimage flashes (high gain). The gain is applied after the delay line read but before the wet/dry mix.

---

#### Knob 5 — Echo U Tint
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Adds a signed colour offset to the echo's U (blue-yellow) channel. At centre position (512) the offset is zero — no colour shift. Turning counter-clockwise shifts the echo toward yellow; clockwise shifts toward blue. Combined with the V Tint, this lets you place the echo's colour anywhere in the UV colour plane. A warm amber phosphor look uses negative U and positive V; a cool blue-green uses positive U and negative V.

---

#### Knob 6 — Echo V Tint
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Adds a signed colour offset to the echo's V (red-cyan) channel. At centre position (512) the offset is zero. Counter-clockwise shifts the echo toward cyan; clockwise toward red-magenta. The U and V tint controls are independent and additive, so any combination of the two reaches any hue in the colour circle. Both offsets are clamped to the 0–1023 range after addition, preventing wraparound artifacts.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Feedback** | Off | On |
| **8 — Mirror Read** | Off | On |
| **9 — Luma Invert** | Off | On |
| **10 — Freeze** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control independent binary features that can be combined freely. Feedback (7) and Freeze (10) interact directly with the delay line input path — feedback routes mixed output back to the delay, while freeze blocks all input. Mirror Read (8) affects only the delay line read address. Luma Invert (9) affects the input luma before it enters both the delay line and the modulation calculation. Bypass (11) overrides the entire processing chain. All five can be active simultaneously, though freeze overrides feedback's input routing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Echo Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Crossfades between the dry input signal and the tinted echo signal. At 0% (fader down), the output is pure dry — no echo is audible. At 100% (fader up), the output is pure wet — only the tinted echo signal passes through. Intermediate positions blend the two. This is the master control for echo intensity and, when feedback is enabled, also controls the feedback gain — lower mix values attenuate each feedback iteration, creating a natural decay envelope for the echo trail.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Cascade processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises build from a simple single-tap echo through tinted delay trails to full feedback loop structures. Each one introduces a new feature of the echo engine while reinforcing the controls learned earlier.

### Exercise 1: Basic Echo Trail

<BeforeAfterSlider
  sources={[
    { label: "House", before: cascade_source1_house, after: cascade_ex1_s1 },
    { label: "Skull", before: cascade_source2_skull, after: cascade_ex1_s2 },
    { label: "Clouds", before: cascade_source3_clouds, after: cascade_ex1_s3 },
    { label: "Pattern", before: cascade_source4_pattern, after: cascade_ex1_s4 },
    { label: "Woman", before: cascade_source5_woman, after: cascade_ex1_s5 },
    { label: "Knit", before: cascade_source6_knit, after: cascade_ex1_s6 },
  ]}
/>
*Basic Echo Trail — simulated result across source images.*
**Source**: A live camera feed or recorded footage with moving subjects and clear edges.

**What You'll Create**: Understand how the two delay taps create displaced echo images and how the mix fader controls echo visibility.

1. **Single echo**: Set Echo Delay to ~40%. Leave Echo 2 Delay at 0%. Push Echo Mix fader to ~60%. A ghost copy of the image appears horizontally displaced.
2. **Dual echo**: Increase Echo 2 Delay to ~70%. Alternate lines now show two different echo distances, creating a vertically interlaced double-echo.
3. **Mix balance**: Sweep the Echo Mix fader from 0% to 100%. At 0%, the echo vanishes; at 100%, only the echo is visible and the dry signal disappears.
4. **Luma modulation**: Slowly increase Luma Mod from 0% to ~50%. The echo displacement begins to follow the brightness contours of the source, warping the trail around bright and dark areas.
5. **Mirror**: Enable Mirror Read (Toggle 8). The echo becomes a reversed reflection, creating symmetry effects.

**Key concepts**: Two independent delay taps alternate per scanline, the mix fader controls echo visibility and feedback gain, luma modulation warps echo displacement with image brightness

---

### Exercise 2: Phosphor Tint Trails

<BeforeAfterSlider
  sources={[
    { label: "House", before: cascade_source1_house, after: cascade_ex2_s1 },
    { label: "Skull", before: cascade_source2_skull, after: cascade_ex2_s2 },
    { label: "Clouds", before: cascade_source3_clouds, after: cascade_ex2_s3 },
    { label: "Pattern", before: cascade_source4_pattern, after: cascade_ex2_s4 },
    { label: "Woman", before: cascade_source5_woman, after: cascade_ex2_s5 },
    { label: "Knit", before: cascade_source6_knit, after: cascade_ex2_s6 },
  ]}
/>
*Phosphor Tint Trails — simulated result across source images.*
**Source**: Footage with strong subject outlines — a person walking, a hand waving, or scrolling text.

**What You'll Create**: Use the tint controls to colour the echo trail and create phosphor-inspired afterimages.

1. **Prepare echo**: Set Echo Delay ~50%, Echo Mix ~70%, Feedback off.
2. **Darken echo**: Turn Echo Y Tint below centre (~30%). The echo becomes a dim shadow trailing the source.
3. **Warm phosphor**: Set Echo U Tint to ~35% (shift toward yellow) and Echo V Tint to ~65% (shift toward red). The echo acquires a warm amber tint reminiscent of P1 long-persistence phosphor.
4. **Cool phosphor**: Try Echo U Tint ~70% (toward blue) and Echo V Tint ~35% (toward cyan). The echo shifts to a cool blue-green, evoking P11 phosphor.
5. **Bright flash**: Push Echo Y Tint above centre (~80%). The echo becomes brighter than the source, creating hot afterimage flashes.
6. **Enable feedback**: Toggle Feedback (Toggle 7). The tinted echo feeds back into the delay, and each iteration tints further — the colour deepens with each pass.

**Key concepts**: Y tint is multiplicative gain controlling echo brightness, U and V tints are additive offsets that colour-shift the echo, feedback accumulates tint over multiple iterations

---

### Exercise 3: Feedback Stutter and Freeze

<BeforeAfterSlider
  sources={[
    { label: "House", before: cascade_source1_house, after: cascade_ex3_s1 },
    { label: "Skull", before: cascade_source2_skull, after: cascade_ex3_s2 },
    { label: "Clouds", before: cascade_source3_clouds, after: cascade_ex3_s3 },
    { label: "Pattern", before: cascade_source4_pattern, after: cascade_ex3_s4 },
    { label: "Woman", before: cascade_source5_woman, after: cascade_ex3_s5 },
    { label: "Knit", before: cascade_source6_knit, after: cascade_ex3_s6 },
  ]}
/>
*Feedback Stutter and Freeze — simulated result across source images.*
**Source**: High-contrast footage — strong outlines against a plain background work best.

**What You'll Create**: Explore feedback accumulation and freeze to create dense recursive echo structures.

1. **Prepare feedback loop**: Set Echo Delay ~60%, Echo Mix ~85%, Feedback on.
2. **Watch accumulation**: With live video, observe how the echo builds over time — each frame adds another displaced, tinted layer.
3. **Modulate the offset**: Increase Luma Mod to ~60%. The feedback trail warps around the brightness structure, creating a zig-zag cascade pattern.
4. **Freeze snapshot**: While a rich echo pattern is on screen, enable Freeze (Toggle 10). The buffer holds its contents — any accumulated echo structure becomes a static afterimage.
5. **Overlay freeze**: With freeze held, the live input continues to mix with the frozen echo. Adjust Echo Mix to balance the frozen pattern against the live signal.
6. **Release and repeat**: Disable Freeze. New video immediately begins overwriting the buffer. Enable Freeze again at a different moment to capture a different pattern.
7. **Luma Invert feedback**: Enable Luma Invert (Toggle 9) while feedback is active. The brightness mapping reverses — echoes now accumulate with inverted modulation.

**Key concepts**: Feedback routes mixed output back to delay input creating iterative accumulation, freeze holds the BRAM buffer as a static afterimage, luma invert reverses the modulation mapping within the feedback loop

---


## Tips

- **Freeze captures the moment**: Freeze the buffer when an interesting feedback pattern appears. The frozen echo becomes a persistent overlay that you can composite against new live footage.
- **Luma Mod follows brightness**: Luma modulation makes the echo displacement content-dependent — bright areas get longer trails. This creates organic, image-aware displacement patterns.
- **Mirror for symmetry**: Mirror Read reverses the echo on tap A only, creating partial symmetry effects that are more interesting than full-frame mirroring.
- **Invert changes the modulation map**: Luma Invert doesn't just negate the echo — it reverses which part of the image gets displaced furthest by luma modulation.
- **Bypass for comparison**: Use Toggle 11 for instant before/after comparison. There is no glitch on transition.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM (Block RAM)** | Dedicated memory blocks embedded in the FPGA fabric, used here for the dual-bank scanline delay line. |
| **Chrominance** | The colour-difference components (U and V) of a YUV video signal, encoding hue and saturation independently of brightness. |
| **CRT (Cathode Ray Tube)** | A vacuum tube display technology in which an electron beam excites phosphor dots on a coated screen to produce an image. |
| **Echo tap** | A read point in a delay line that retrieves stored data from a configurable offset, producing a time-displaced copy of the signal. |
| **Feedback topology** | A signal routing configuration in which the processed output is fed back to the input, creating iterative accumulation with each pass through the loop. |
| **Luma** | Short for luminance; the brightness component (Y channel) of a YUV video signal. |
| **Phosphor persistence** | The duration a CRT phosphor dot continues to glow after the electron beam moves on, producing visible afterimage trails behind moving objects. |
| **Ping-pong buffer** | A dual-bank memory architecture in which one bank is written while the other is read, swapping roles each cycle to provide continuous access without stalling. |
| **Saturation clamping** | Limiting a signal value to a valid range (0–1023) to prevent arithmetic overflow or wraparound artefacts. |
| **Scanline** | A single horizontal line of video data, scanned left to right by the display system. |

---
