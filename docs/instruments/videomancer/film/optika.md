---
draft: true
sidebar_position: 210
slug: /instruments/videomancer/optika
title: "Optika"
image: /img/instruments/videomancer/optika/optika_hero_s1.png
description: "Before digital compositing, optical printers were the primary tool for combining multiple film elements into a single image."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import optika_control_panel from '/img/instruments/videomancer/optika/optika_control_panel.png';
import optika_source1_cat from '/img/instruments/videomancer/optika/optika_source1_cat.png';
import optika_source2_skull from '/img/instruments/videomancer/optika/optika_source2_skull.png';
import optika_source3_collage from '/img/instruments/videomancer/optika/optika_source3_collage.png';
import optika_source4_pattern from '/img/instruments/videomancer/optika/optika_source4_pattern.png';
import optika_source5_girl from '/img/instruments/videomancer/optika/optika_source5_girl.png';
import optika_source6_paint from '/img/instruments/videomancer/optika/optika_source6_paint.png';
import optika_hero_s1 from '/img/instruments/videomancer/optika/optika_hero_s1.png';
import optika_hero_s2 from '/img/instruments/videomancer/optika/optika_hero_s2.png';
import optika_hero_s3 from '/img/instruments/videomancer/optika/optika_hero_s3.png';
import optika_hero_s4 from '/img/instruments/videomancer/optika/optika_hero_s4.png';
import optika_hero_s5 from '/img/instruments/videomancer/optika/optika_hero_s5.png';
import optika_hero_s6 from '/img/instruments/videomancer/optika/optika_hero_s6.png';
import optika_ex1_s1 from '/img/instruments/videomancer/optika/optika_ex1_s1.png';
import optika_ex1_s2 from '/img/instruments/videomancer/optika/optika_ex1_s2.png';
import optika_ex1_s3 from '/img/instruments/videomancer/optika/optika_ex1_s3.png';
import optika_ex1_s4 from '/img/instruments/videomancer/optika/optika_ex1_s4.png';
import optika_ex1_s5 from '/img/instruments/videomancer/optika/optika_ex1_s5.png';
import optika_ex1_s6 from '/img/instruments/videomancer/optika/optika_ex1_s6.png';
import optika_ex2_s1 from '/img/instruments/videomancer/optika/optika_ex2_s1.png';
import optika_ex2_s2 from '/img/instruments/videomancer/optika/optika_ex2_s2.png';
import optika_ex2_s3 from '/img/instruments/videomancer/optika/optika_ex2_s3.png';
import optika_ex2_s4 from '/img/instruments/videomancer/optika/optika_ex2_s4.png';
import optika_ex2_s5 from '/img/instruments/videomancer/optika/optika_ex2_s5.png';
import optika_ex2_s6 from '/img/instruments/videomancer/optika/optika_ex2_s6.png';
import optika_ex3_s1 from '/img/instruments/videomancer/optika/optika_ex3_s1.png';
import optika_ex3_s2 from '/img/instruments/videomancer/optika/optika_ex3_s2.png';
import optika_ex3_s3 from '/img/instruments/videomancer/optika/optika_ex3_s3.png';
import optika_ex3_s4 from '/img/instruments/videomancer/optika/optika_ex3_s4.png';
import optika_ex3_s5 from '/img/instruments/videomancer/optika/optika_ex3_s5.png';
import optika_ex3_s6 from '/img/instruments/videomancer/optika/optika_ex3_s6.png';

# Optika

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: optika_source1_cat, after: optika_hero_s1 },
    { label: "Skull", before: optika_source2_skull, after: optika_hero_s2 },
    { label: "Collage", before: optika_source3_collage, after: optika_hero_s3 },
    { label: "Pattern", before: optika_source4_pattern, after: optika_hero_s4 },
    { label: "Girl", before: optika_source5_girl, after: optika_hero_s5 },
    { label: "Paint", before: optika_source6_paint, after: optika_hero_s6 },
  ]}
/>
*Optika building up multi-exposure accumulation trails with printer light color balance and film halation bloom over a live video source.*

---

## Overview

Before digital compositing, optical printers were the primary tool for combining multiple film elements into a single image. A strip of developed negative was projected frame by frame onto unexposed raw stock, and by rewinding and re-exposing with different elements, multiple layers could be accumulated onto a single piece of film. Each additional pass added density — bright areas built up toward overexposure while dark areas remained transparent. The result was a photochemical double-exposure with a distinctive look: soft bloom around highlights, color shifts from printer light filters, and the characteristic additive density build-up of silver halide emulsion.

Optika recreates this process in real time using BRAM-based scanline accumulation. A per-pixel buffer stores an 8-bit luminance accumulator that blends live input with decaying previous values. Exposure amount controls how much new input is layered on each capture cycle, while fade rate controls how quickly old accumulation decays. The result is a temporal composite where moving objects leave luminous trails and static elements build up to saturation. Printer light simulation adds brightness offset and warm/cool color balance. A 4-tap moving-average bloom stage simulates the halation glow that occurs on overexposed film.

The program can operate in additive mode (each frame adds to the accumulator) or replace mode (each frame overwrites). A frame-skip gate provides step-print speed control, and freeze and clear toggles give direct buffer manipulation. The bypass toggle is declared in the register map but not connected to the output mux — only the fader mix provides wet/dry control.

---

## Background

### The Optical Printer

The Acme-Dunn optical printer, developed in the 1940s, was the workhorse of Hollywood visual effects for half a century. It consisted of a projector head and a camera head precisely aligned so that one frame of existing film could be re-photographed onto new stock. By rewinding the raw stock and feeding different source elements, effects artists could create double exposures, dissolves, wipes, matte composites, and title overlays — all through photochemical additive exposure.

### Additive vs. Replace Accumulation

In real optical printing, each exposure adds to the accumulated density on the film — light is additive. A highlight that appears in multiple passes builds up brighter and brighter, eventually saturating the emulsion. Optika's additive mode mimics this: the faded previous value plus the new exposure are summed, saturating at maximum. Replace mode instead overwrites the buffer with each new frame, creating a step-print effect without temporal build-up.

### Printer Light Color Timing

Film color grading was originally done at the printing stage by adjusting the intensity of red, green, and blue light sources in the optical printer — hence "printer lights." Videomancer's Optika simplifies this to a single color balance axis: values below center shift the image toward warm (boosting V, reducing U), while values above center shift toward cool (boosting U, reducing V). The brightness control adds a signed offset to the accumulated luminance, simulating the overall printer light intensity.

### Film Halation and Bloom

When bright light hits photographic film, it can scatter within the emulsion layers and reflect off the film base, creating a soft glow around overexposed areas. This "halation" effect is a signature characteristic of film exposure that is difficult to recreate digitally. Optika approximates it with a 4-tap horizontal moving average that is gated to activate only where the accumulated signal exceeds a brightness threshold. The bloom amount control scales the glow intensity.

### Temporal Persistence and Frame Skip

Real step-printing involved advancing the raw stock while holding the source at a fixed frame, creating freeze-frame effects and speed ramps. Optika's capture rate control implements this: a frame counter skips N frames between captures, so the buffer only updates at intervals. Combined with the fade rate, this creates speed-ramped accumulation where the temporal decay continues even during skip frames.


---

## Signal Flow

```
Input Video (YUV 4:4:4, 10-bit)
│
├── Y Channel ─────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register        (10-bit → 8-bit: Y >> 2)
│   ├─ 2. Accumulation          (BRAM read-modify-write)
│   │      ├─ Clear: write zeros
│   │      ├─ Freeze: write back unchanged
│   │      ├─ Additive: faded_prev + scaled_input (saturate 255)
│   │      └─ Replace: scaled_input only
│   ├─ 3. Temporal Blend        (current + previous frame line, >> 1)
│   ├─ 4. Printer Light         (brightness offset, ±128 range)
│   ├─ 5. Bloom                 (4-tap MA, gated on bright pixels)
│   └─ 6. Clamp                 (0..1023)
│
├── UV Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Input Register        (pipeline delay)
│   ├─ 2–3. Pass-through delay  (4 pipeline stages)
│   └─ 4. Color Balance         (warm ↔ cool shift: ±U, ∓V)
│
├── Wet/Dry Mix ───────────────────────────────────────────────
│   └─ 3× interpolator_u       (source ↔ processed, fader controls mix)
│
├── Exposure Gate ─────────────────────────────────────────────
│   └─ Frame skip counter       (capture every N frames per Capture Rate)
│
└── Sync ──────────────────────────────────────────────────────
    └─ Delayed pass-through     (hsync, vsync, field, 8-clock pipeline)
```

The pipeline's core is the BRAM-based scanline accumulator. On each active pixel clock, the accumulator reads the previous value from BRAM, applies fade (multiply by fade rate >> 2), adds the exposure-scaled input (multiply by exposure >> 2), and writes the result back — a classic read-modify-write cycle. The accumulator operates at 8-bit precision (the input Y is truncated from 10 to 8 bits), which creates a natural density ceiling matching the limited dynamic range of real photographic emulsion.

A second BRAM stores the previous frame's scanline data for temporal blending. The current accumulated value is averaged with the previous frame's value, creating smoother persistence across frames. The bloom stage operates on the printer-light-adjusted result, adding a gated horizontal glow only where the accumulated brightness exceeds a threshold of approximately 384 (out of 1023). Chrominance passes through a 4-stage pipeline delay with color balance applied at stage 3 — the printer light shifts U and V in opposite directions to simulate warm/cool filter adjustments.

---

## Parameter Reference

<img src={optika_control_panel} alt="Videomancer front panel with Optika loaded"/>
*Videomancer's front panel with Optika active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Exposure
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the exposure amount — how strongly each new input frame contributes to the accumulation buffer. The upper 8 bits of the 10-bit register multiply the 8-bit input luminance. At zero, no new input reaches the buffer and only the decaying previous accumulation is visible. At maximum, each frame deposits a strong imprint that builds rapidly toward saturation. In additive mode, moderate exposure values allow many frames to layer before clipping; high values saturate quickly, producing hard silhouettes rather than soft ghosts.

---

#### Knob 2 — Fade Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the fade rate — the decay factor applied to the accumulation buffer on each frame. The upper 8 bits multiply the previous accumulated value. At minimum the buffer fades immediately, showing only the most recent capture. At maximum the buffer retains accumulated density indefinitely, building up layer after layer without decay. At approximately 75% the fade time roughly matches a natural film exposure series, where each layer persists for several seconds before decaying.

---

#### Knob 3 — Capture Rate
| Property | Value |
|----------|-------|
| Range | 1 – 64 |
| Default | 1 |

Sets the capture rate — the number of frames to skip between buffer updates. The upper 6 bits of the register define a frame counter threshold (0–63). At zero, every frame is captured. At maximum, only every 64th frame is captured, creating a step-print effect where the buffer builds up from widely spaced temporal samples. During skip frames the buffer still applies fade decay, so the previously accumulated image continues to dim while waiting for the next capture.

---

#### Knob 4 — Brightness
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Printer light brightness offset. The 10-bit register is mapped to a signed value centered at 512 — values below center darken the accumulated image, values above center brighten it. The offset is halved (right-shifted by 1) before being added to the 8-bit expanded accumulator, providing ±128 levels of brightness adjustment. This simulates adjusting the intensity of the printer light source in an optical printer — a fundamental grading control that affects overall density without changing the exposure or fade dynamics.

---

#### Knob 5 — Color Bal
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Color balance control simulating printer light filter adjustment. The 10-bit register is centered at 512: values below center warm the image by shifting UV toward red-amber (positive V offset, negative U offset), and values above center cool the image toward blue (positive U offset, negative V offset). The shift is right-shifted by 2 (divided by 4) before application, providing a subtle range of ±64 chrominance levels. The U and V channels shift in opposite directions, maintaining roughly constant saturation while rotating the color temperature.

---

#### Knob 6 — Bloom Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Bloom amount — the intensity of the halation glow applied to bright accumulated areas. The bloom is computed as a 4-tap horizontal moving average of the printer-light-adjusted luminance, gated to activate only where the average exceeds a brightness threshold. The bloom amount register scales this glow before it is added to the output. At zero the bloom stage is effectively disabled. At maximum, bright accumulated areas spread a strong horizontal glow into adjacent pixels, simulating the soft halation halos visible on overexposed film.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Accum Mode** | Additive | Replace |
| **8 — Clear Buf** | Normal | Clear |
| **9 — Freeze** | Run | Freeze |
| **10 — Mono** | Color | Mono |
| **11 — Bypass** | Off | On |

Five toggles (7–11) control accumulation mode, buffer management, temporal behavior, colorimetry, and bypass. Each operates independently. The Clear Buffer toggle is momentary — while active it continuously writes zeros to the accumulator BRAM, and when released the buffer begins accumulating fresh input. Note that the Bypass toggle (Toggle 11) is declared in the register map and assigned to an internal signal, but the bypass signal is never checked in the output path — the output always routes through the interpolator. Only the fader provides wet/dry control.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade. This register drives the interpolation parameter of all three interpolator_u instances. At 0 the output is pure dry (original input signal). At 1023 the output is pure wet (the accumulated, printer-light-graded, bloom-enhanced result). Intermediate values blend between the two. Because the bypass toggle is non-functional, this fader is the only control for comparing the processed signal to the original.

---

## Guided Exercises

These exercises progress from basic temporal accumulation through printer light grading to full multi-exposure compositing with bloom. Each reveals a different aspect of Optika's optical printer simulation.

### Exercise 1: Ghostly Trails

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: optika_source1_cat, after: optika_ex1_s1 },
    { label: "Skull", before: optika_source2_skull, after: optika_ex1_s2 },
    { label: "Collage", before: optika_source3_collage, after: optika_ex1_s3 },
    { label: "Pattern", before: optika_source4_pattern, after: optika_ex1_s4 },
    { label: "Girl", before: optika_source5_girl, after: optika_ex1_s5 },
    { label: "Paint", before: optika_source6_paint, after: optika_ex1_s6 },
  ]}
/>
*Ghostly Trails — simulated result across source images.*
**Source**: A live camera with slow hand movements, or recorded footage of a person walking across the frame.

**Objective**: Understand how exposure and fade interact to create temporal persistence trails.

1. **Set exposure**: Turn Exposure to ~40%. A moderate amount of each frame is deposited into the buffer.
2. **Set fade**: Turn Fade Rate to ~80%. Previous accumulation decays slowly, leaving visible trails behind moving objects.
3. **Observe trails**: Move slowly in front of the camera. Ghost images of your previous positions persist for several seconds before fading.
4. **Adjust decay**: Reduce Fade Rate to ~50%. Trails shorten — only the most recent positions are visible. Increase to ~95% and trails persist much longer.
5. **Additive build-up**: With high fade rate, stay still for a few seconds. Your static image builds up toward maximum brightness as exposure adds frame after frame.
6. **Clear and restart**: Activate Clear Buffer (Toggle 8) briefly, then release. The trails vanish and begin accumulating fresh.

**Key concepts**: Exposure controls input strength per frame, fade controls temporal decay, additive accumulation builds density toward saturation

---

### Exercise 2: Step-Print Speed Ramp

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: optika_source1_cat, after: optika_ex2_s1 },
    { label: "Skull", before: optika_source2_skull, after: optika_ex2_s2 },
    { label: "Collage", before: optika_source3_collage, after: optika_ex2_s3 },
    { label: "Pattern", before: optika_source4_pattern, after: optika_ex2_s4 },
    { label: "Girl", before: optika_source5_girl, after: optika_ex2_s5 },
    { label: "Paint", before: optika_source6_paint, after: optika_ex2_s6 },
  ]}
/>
*Step-Print Speed Ramp — simulated result across source images.*
**Source**: A moving subject — spinning record, pendulum, or a hand waving rhythmically.

**Objective**: Explore frame-skip capture rate and replace mode for step-print effects.

1. **Enable replace mode**: Set Accum Mode to Replace (Toggle 7 on). Each captured frame overwrites instead of accumulating.
2. **Set capture rate**: Turn Capture Rate to ~30% (~20 frame skip). The buffer updates every 20 frames, creating a choppy slow-motion effect.
3. **Observe step print**: Moving objects jump between positions. The motion becomes staccato rather than smooth.
4. **Adjust speed**: Reduce Capture Rate toward 0 for smooth motion. Increase toward 100% for extreme freeze-frame jumps.
5. **Switch to additive**: Disable replace mode (Toggle 7 off). Now each capture adds to the buffer instead of overwriting, creating multiple overlapping exposures of the same moving object.
6. **Fade tuning**: With additive mode and high capture rate skip, adjust Fade Rate so that old exposures decay just before new ones arrive. This creates evenly-spaced temporal echoes.

**Key concepts**: Capture rate implements step-printing frame skip, replace mode overwrites instead of accumulating, fade continues during skip frames

---

### Exercise 3: Film Look Composite

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: optika_source1_cat, after: optika_ex3_s1 },
    { label: "Skull", before: optika_source2_skull, after: optika_ex3_s2 },
    { label: "Collage", before: optika_source3_collage, after: optika_ex3_s3 },
    { label: "Pattern", before: optika_source4_pattern, after: optika_ex3_s4 },
    { label: "Girl", before: optika_source5_girl, after: optika_ex3_s5 },
    { label: "Paint", before: optika_source6_paint, after: optika_ex3_s6 },
  ]}
/>
*Film Look Composite — simulated result across source images.*
**Source**: High-contrast footage with bright highlights — candle flames, spotlights, or bright windows in dark rooms.

**Objective**: Combine accumulation, printer light grading, and halation bloom for a classic film optical-print look.

1. **Moderate accumulation**: Set Exposure ~30%, Fade Rate ~85%. Subtle temporal persistence without heavy ghosting.
2. **Warm printer light**: Shift Color Balance below center (~35%). The image warms to a golden-amber tone, simulating tungsten printer lights.
3. **Brightness offset**: Adjust Brightness slightly above center (~55%) to lift the shadows, simulating a print with higher base density.
4. **Enable bloom**: Turn Bloom Amount to ~50%. Watch the glow appear around bright highlights — the halation halo spreads horizontally from overexposed areas.
5. **Bloom sweep**: Increase Bloom Amount toward 100%. The glow intensifies, spreading further into the highlights. Find a natural-looking level around 40–60%.
6. **Freeze and grade**: Activate Freeze (Toggle 9) to hold a frame, then adjust Color Balance and Brightness to grade the frozen composite without new input disturbing it.

**Key concepts**: Printer light adjusts brightness offset and color temperature, bloom simulates film halation on bright areas, freeze holds the buffer for static grading

---


## Tips

- **Bypass is broken — use the fader**: The Bypass toggle (Toggle 11) has no effect. Set the Mix fader to 0% for instant A/B comparison with the dry signal.
- **Clear before scene changes**: Use the momentary Clear Buffer toggle to reset accumulated content when switching input sources, otherwise the old scene will persist as ghost overlay.
- **Fade rate is the persistence knob**: Low fade = short trails (recent only). High fade = long trails (history accumulates). At 100%, nothing fades and the buffer accumulates indefinitely toward saturation.
- **Bloom requires bright accumulation**: The halation bloom only activates above a brightness threshold. Low exposure or rapid fade prevents the accumulator from reaching bloom territory.
- **Freeze + grade**: Use freeze to lock a multi-exposure composite, then adjust printer light brightness and color balance to grade the frozen image at leisure.
- **Step-print with additive**: Combining frame skip (high capture rate) with additive mode creates evenly-spaced temporal echoes — multiple exposures of a moving object at discrete time steps.
- **Feedback amplifies accumulation**: Routing the output back to the input creates recursive multi-exposure build-up, rapidly saturating but producing extreme halation effects along the way.

---

## Glossary

| Term | Definition |
|------|------------|
| **Accumulation Buffer** | A BRAM-based per-pixel storage array that retains and blends luminance values across multiple video frames. |
| **Additive Exposure** | A blending mode where new input is summed with the existing buffer content, building up density with each frame. |
| **Bloom** | A glow effect around bright areas simulating optical halation, implemented as a gated moving-average filter. |
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for scanline and frame accumulation storage. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms by incrementing a phase accumulator. |
| **Emulsion** | The light-sensitive chemical layer on photographic film that records exposure through density changes. |
| **Fade Rate** | The decay factor applied to the accumulation buffer per frame, controlling temporal persistence. |
| **Halation** | Light scattering within photographic film causing a soft glow around bright areas; simulated by the bloom stage. |
| **Interpolator** | A linear blending circuit that crossfades between two input values based on a mix parameter. |
| **Optical Printer** | A mechanical device for re-photographing film elements to create composites, dissolves, and effects. |
| **Printer Light** | The illumination source in an optical printer; adjusting its color temperature and intensity is the original form of film color grading. |
| **Step-Print** | A printing technique where frames are skipped during exposure to create speed changes. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
