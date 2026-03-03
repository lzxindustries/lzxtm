---
draft: true
sidebar_position: 293
slug: /instruments/videomancer/strobe
title: "Strobe"
image: /img/instruments/videomancer/strobe/strobe_hero_s1.png
description: "Stroboscopic photography freezes motion at impossible intervals — a dancer captured ten times in a single exposure, each ghost slightly advanced from the last."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import strobe_control_panel from '/img/instruments/videomancer/strobe/strobe_control_panel.png';
import strobe_source1_runner from '/img/instruments/videomancer/strobe/strobe_source1_runner.png';
import strobe_source2_dog from '/img/instruments/videomancer/strobe/strobe_source2_dog.png';
import strobe_source3_collage from '/img/instruments/videomancer/strobe/strobe_source3_collage.png';
import strobe_source4_pattern from '/img/instruments/videomancer/strobe/strobe_source4_pattern.png';
import strobe_source5_boy from '/img/instruments/videomancer/strobe/strobe_source5_boy.png';
import strobe_source6_knit from '/img/instruments/videomancer/strobe/strobe_source6_knit.png';
import strobe_hero_s1 from '/img/instruments/videomancer/strobe/strobe_hero_s1.png';
import strobe_hero_s2 from '/img/instruments/videomancer/strobe/strobe_hero_s2.png';
import strobe_hero_s3 from '/img/instruments/videomancer/strobe/strobe_hero_s3.png';
import strobe_hero_s4 from '/img/instruments/videomancer/strobe/strobe_hero_s4.png';
import strobe_hero_s5 from '/img/instruments/videomancer/strobe/strobe_hero_s5.png';
import strobe_hero_s6 from '/img/instruments/videomancer/strobe/strobe_hero_s6.png';
import strobe_ex1_s1 from '/img/instruments/videomancer/strobe/strobe_ex1_s1.png';
import strobe_ex1_s2 from '/img/instruments/videomancer/strobe/strobe_ex1_s2.png';
import strobe_ex1_s3 from '/img/instruments/videomancer/strobe/strobe_ex1_s3.png';
import strobe_ex1_s4 from '/img/instruments/videomancer/strobe/strobe_ex1_s4.png';
import strobe_ex1_s5 from '/img/instruments/videomancer/strobe/strobe_ex1_s5.png';
import strobe_ex1_s6 from '/img/instruments/videomancer/strobe/strobe_ex1_s6.png';
import strobe_ex2_s1 from '/img/instruments/videomancer/strobe/strobe_ex2_s1.png';
import strobe_ex2_s2 from '/img/instruments/videomancer/strobe/strobe_ex2_s2.png';
import strobe_ex2_s3 from '/img/instruments/videomancer/strobe/strobe_ex2_s3.png';
import strobe_ex2_s4 from '/img/instruments/videomancer/strobe/strobe_ex2_s4.png';
import strobe_ex2_s5 from '/img/instruments/videomancer/strobe/strobe_ex2_s5.png';
import strobe_ex2_s6 from '/img/instruments/videomancer/strobe/strobe_ex2_s6.png';
import strobe_ex3_s1 from '/img/instruments/videomancer/strobe/strobe_ex3_s1.png';
import strobe_ex3_s2 from '/img/instruments/videomancer/strobe/strobe_ex3_s2.png';
import strobe_ex3_s3 from '/img/instruments/videomancer/strobe/strobe_ex3_s3.png';
import strobe_ex3_s4 from '/img/instruments/videomancer/strobe/strobe_ex3_s4.png';
import strobe_ex3_s5 from '/img/instruments/videomancer/strobe/strobe_ex3_s5.png';
import strobe_ex3_s6 from '/img/instruments/videomancer/strobe/strobe_ex3_s6.png';

# Strobe

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: strobe_source1_runner, after: strobe_hero_s1 },
    { label: "Dog", before: strobe_source2_dog, after: strobe_hero_s2 },
    { label: "Collage", before: strobe_source3_collage, after: strobe_hero_s3 },
    { label: "Pattern", before: strobe_source4_pattern, after: strobe_hero_s4 },
    { label: "Boy", before: strobe_source5_boy, after: strobe_hero_s5 },
    { label: "Knit", before: strobe_source6_knit, after: strobe_hero_s6 },
  ]}
/>
*Strobe freezing a moving subject into layered multi-exposure echoes with DDS-driven periodic flash and IIR persistence trails.*

---

## Overview

Stroboscopic photography freezes motion at impossible intervals — a dancer captured ten times in a single exposure, each ghost slightly advanced from the last. Strobe brings this technique into the real-time video domain. A numerically-controlled oscillator (DDS accumulator) generates a periodic flash trigger, alternating between bright "flash" phases where source video passes at boosted brightness and dim "dark" phases where the signal is attenuated to simulate the darkness between exposures.

Between the flash gate and the output, an IIR (infinite impulse response) persistence stage blends the current pixel with its own decaying history. During flash phases, the persistence buffer tracks the source; during dark phases, it holds a fading afterimage. The result is a continuously evolving multi-exposure composite where moving subjects leave luminous trails. An LFSR noise generator injects film-grain texture during dark phases, and an optional monochrome mode desaturates the entire output. A double-flash toggle fires two pulses per cycle for denser layering.

At conservative settings — slow strobe rate, long flash duration, moderate persistence — the effect is a gentle temporal softness, as if the camera shutter were held open a fraction too long. At extreme settings — fast rate, narrow flash, deep persistence — the image fractures into rhythmic staccato bursts separated by noisy voids, an aggressive visual rhythm that transforms any source into pulsating abstraction.

---

## Background

### Direct Digital Synthesis (DDS)

Strobe's timing engine uses a technique borrowed from RF signal generation. A **direct digital synthesizer** is nothing more than a counter that wraps around at a fixed bit width (here 16 bits), advanced by a configurable increment on each vertical sync pulse. The most significant bits of the accumulator determine the current phase of the strobe cycle. When the phase is below a threshold, the strobe is "on" (flash); otherwise it is "off" (dark). The ratio of flash-to-dark time is the duty cycle, and the DDS increment sets the fundamental frequency. Because the increment is a continuously variable 10-bit value scaled into 16-bit phase space, the strobe frequency sweeps smoothly rather than jumping between integer subdivisions.

### IIR Persistence and Temporal Feedback

The persistence stage is a first-order IIR low-pass filter applied per pixel. On each clock cycle, the filter computes `output = previous + (current − previous) >> shift`, where the shift value (1–9) determines the decay rate. Small shifts (fast response) mean the output tracks the input closely; large shifts (slow response) mean the output decays gradually, holding afterimages for many frames. This is mathematically equivalent to an exponential moving average with alpha = 1/2^shift. The blend stage then takes the brighter of the IIR output and the current scaled pixel, ensuring that flash frames punch through the persistence trail rather than being averaged away.

### LFSR Film Grain

A 16-bit **linear feedback shift register** produces a pseudo-random bit sequence at pixel rate. During dark phases, the lower 10 bits are AND-masked by a noise-scale parameter and added to luma, producing a film-grain texture that breaks up the flat darkness between strobes. The LFSR runs continuously regardless of phase, maintaining its statistical properties even when its output is not used. The fixed seed ensures repeatable noise patterns across power cycles.

### Stroboscopic Photography and Chronophotography

The strobe effect descends from Étienne-Jules Marey's chronophotographic method (1882) and Harold Edgerton's electronic stroboscope (1931). Marey layered multiple exposures of a moving subject onto a single photographic plate to study locomotion. Edgerton's xenon flash tube could fire at kilohertz rates, freezing bullets in flight. Strobe's DDS accumulator plays the role of Edgerton's oscillator, and the IIR persistence plays the role of the photographic plate: each flash "exposes" the persistence buffer, and the buffer decays between flashes just as phosphor decays on an oscilloscope screen.

### Mono and Desaturation

Stroboscopic effects in the analog darkroom are inherently monochrome — the photographic plate records only intensity. Strobe's monochrome toggle forces the U and V channels to the neutral midpoint (512), producing a silver-halide aesthetic. Even in color mode, the dark-phase chroma is partially desaturated toward neutral, simulating the loss of color fidelity that occurs when exposures are layered and attenuation applied. This desaturation-during-darkness creates a visual distinction between the vivid flash moments and the ghostly dark-phase trails.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── DDS Phase Accumulator ──────────────────────────────────────
│   └─ Vsync-driven increment (Strobe Rate × 64)
│      → s_dds_phase (16-bit wrapping counter)
│      → Flash detect: phase < threshold → flash; else dark
│      → Double flash: also check second half of cycle
│
├── Stage 1: Input Register ────────────────────────────────────
│   └─ Y, U, V latched
│
├── Stage 2: Flash/Dark Classification + Brightness ────────────
│   ├─ Flash → Y boosted (Y + Tint Hue/2, clamped)
│   │          U, V pass through
│   └─ Dark  → Y attenuated (shift-based dimming from Decay)
│              U, V desaturated toward midpoint
│
├── Stage 3: Persistence Diff + Shift ──────────────────────────
│   └─ diff = (Y_scaled − persist_Y) >> shift
│      shift (1–9) selected by Brightness knob
│
├── Stage 4: IIR Update ────────────────────────────────────────
│   └─ persist_Y += diff_shifted
│
├── Stage 5: Blend + Noise + Mono ──────────────────────────────
│   ├─ Y = max(persist_Y, Y_scaled)
│   ├─ Dark phase + Color Trail → add LFSR noise (Persist amt)
│   ├─ Chroma desaturated toward midpoint
│   └─ Sync=mono → U, V = 512
│
├── Mix Stage (interpolator_u × 3) ─────────────────────────────
│   └─ wet/dry crossfade by Mix fader
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Bypass → pass delayed input directly
```

The critical interaction is between the DDS flash gate and the IIR persistence. During flash phases, the persistence buffer is driven toward the boosted input; during dark phases, it decays exponentially. The blend stage takes the *maximum* of the IIR output and the current scaled input, which means flash frames always punch through — the persistence trail never masks a new flash, only fills in the darkness between them. The noise injection occurs after this max-blend, so grain appears on top of the persistence trail rather than being averaged away by the IIR. The double-flash mode checks both halves of the DDS cycle, effectively doubling the pulse rate within the same fundamental period.

---

## Parameter Reference

<img src={strobe_control_panel} alt="Videomancer front panel with Strobe loaded"/>
*Videomancer's front panel with Strobe active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Strobe Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the strobe flash frequency by setting the DDS phase increment. At low values, the DDS advances slowly and the strobe cycle is long — many frames between flashes. At high values, the DDS increment is large and the strobe fires rapidly, approaching a continuous flash at maximum. The frequency relationship is linear: doubling the register value doubles the strobe rate. At very low settings, individual flash events become visible as distinct brightening pulses. At very high settings, the strobe frequency exceeds the persistence decay rate and the output appears continuously lit with subtle pulsation.

---

#### Knob 2 — Exposures
| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 5 |

Sets the flash duration — the proportion of each strobe cycle spent in the bright "flash" phase. At low values, the flash is a narrow pulse: the image flickers on for a brief instant then goes dark. At high values, the flash occupies most of the cycle, and the dark phase becomes a brief dip. This control directly shapes the duty cycle of the stroboscopic pattern. Narrow flashes produce crisp, staccato multi-exposure freezes; wide flashes produce a gentler brightness modulation closer to a flicker effect.

---

#### Knob 3 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness floor during the dark phase between strobe flashes. At minimum, the dark phase is nearly black — only the persistence trail provides any light. At higher values, the source video remains partially visible even during dark phases, producing a softer contrast between flash and dark. This parameter determines how much of the original image "leaks through" between exposures. Setting it high reduces the strobe contrast to a gentle flickering overlay; setting it low creates dramatic black gaps between flashes.

---

#### Knob 4 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Governs the IIR persistence decay speed. This control selects a bit-shift value (1–9) that determines how quickly the persistence buffer responds to new input. At low values, the shift is small and the buffer tracks the input rapidly — persistence trails are short and crisp. At high values, the shift is large and the buffer decays very slowly — trails linger for many frames, building up ghost images of previous flash exposures. This is the core control for the multi-exposure layering quality: low values give two or three sharp echoes, high values give long luminous smears.

---

#### Knob 5 — Persist
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the amplitude of LFSR noise injected during dark phases. At minimum, the dark phase is a clean attenuation — smooth and silent. As the value increases, progressively stronger film-grain noise fills the darkness between strobe flashes. The noise is AND-masked with this parameter's top bits, so the amplitude scales in powers of two. At maximum, the noise is clearly visible as a coarse grain pattern. This control has no effect during flash phases — noise is gated by the flash detector.

---

#### Knob 6 — Tint Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the brightness boost applied to the source video during flash phases. At the midpoint, the flash passes the source at its original brightness. Higher values add a positive offset, pushing the flash exposure toward white — simulating an overdriven xenon strobe. Lower values produce a dimmer flash. This control interacts with persistence: brighter flashes punch higher into the persistence buffer, creating more intense afterimages that take longer to decay. When combined with high persistence and low dark level, a strong brightness boost creates intense, blooming multi-exposure composites.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Add | Blend |
| **8 — Sync** | Free | Frame |
| **9 — Color Trail** | Off | On |
| **10 — Freeze** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent processing modes. Mode selects between normal stroboscopic cycling and a freeze function. Sync switches between full-color output and monochrome desaturation. Color Trail enables LFSR noise injection during dark phases. Freeze activates double-flash mode for denser exposure layering. Bypass routes the input directly to the output. These toggles do not interact combinatorially — each enables or disables a single processing feature.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (unprocessed) input and the wet (strobed) output. At 100%, only the processed strobe signal is output. At 0%, the original input passes through unchanged. Intermediate positions create a transparent overlay of the strobe effect on top of the source, useful for subtle ghost-trail additions without full stroboscopic darkness. The interpolation is linear per-channel (Y, U, V independently).

---

## Guided Exercises

These exercises build from basic single-flash freeze effects through multi-exposure layering to full stroboscopic abstraction with noise and persistence modulation.

### Exercise 1: Basic Strobe Freeze

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: strobe_source1_runner, after: strobe_ex1_s1 },
    { label: "Dog", before: strobe_source2_dog, after: strobe_ex1_s2 },
    { label: "Collage", before: strobe_source3_collage, after: strobe_ex1_s3 },
    { label: "Pattern", before: strobe_source4_pattern, after: strobe_ex1_s4 },
    { label: "Boy", before: strobe_source5_boy, after: strobe_ex1_s5 },
    { label: "Knit", before: strobe_source6_knit, after: strobe_ex1_s6 },
  ]}
/>
*Basic Strobe Freeze — simulated result across source images.*
**Source**: A slowly moving subject — a hand waving, a pendulum, or scrolling text.

**Objective**: Understand the relationship between strobe rate, flash duration, and the resulting freeze effect.

1. **Single slow flash**: Set Strobe Rate to ~15%. The strobe fires infrequently. Watch the source alternate between bright flash moments and dark gaps.
2. **Narrow pulse**: Reduce Exposures to ~10%. The flash becomes a brief burst — crisp snapshots separated by long darkness.
3. **Wide pulse**: Increase Exposures to ~80%. The flash dominates the cycle, and the dark phase becomes a brief dip.
4. **Frequency sweep**: Slowly increase Strobe Rate from 10% to 80%. Watch the flash rhythm accelerate from a slow blink to a rapid flicker.
5. **Dark level**: Adjust Decay to control how visible the source is between flashes. Low values create dramatic black-and-bright alternation; high values create gentle brightness modulation.

**Key concepts**: DDS frequency control is linear, flash duration controls duty cycle, dark level sets the floor brightness between exposures

---

### Exercise 2: Persistence Trails

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: strobe_source1_runner, after: strobe_ex2_s1 },
    { label: "Dog", before: strobe_source2_dog, after: strobe_ex2_s2 },
    { label: "Collage", before: strobe_source3_collage, after: strobe_ex2_s3 },
    { label: "Pattern", before: strobe_source4_pattern, after: strobe_ex2_s4 },
    { label: "Boy", before: strobe_source5_boy, after: strobe_ex2_s5 },
    { label: "Knit", before: strobe_source6_knit, after: strobe_ex2_s6 },
  ]}
/>
*Persistence Trails — simulated result across source images.*
**Source**: A subject with clear motion trails — a dancer, a bouncing ball, or a slow camera pan across a high-contrast scene.

**Objective**: Learn how IIR persistence creates multi-exposure ghost echoes.

1. **Enable persistence**: Set Brightness (persistence control) to ~60%. Previous flash frames now leave decaying afterimages.
2. **Fast strobe**: Increase Strobe Rate to ~40%. Multiple flash frames accumulate in the persistence buffer, creating overlapping echoes.
3. **Long trails**: Increase Brightness further to ~85%. Trails linger for many frames, building up dense ghost composites.
4. **Short trails**: Reduce Brightness to ~20%. Trails decay quickly, showing only one or two sharp echoes behind the current position.
5. **Boost flash**: Increase Tint Hue (brightness boost) to ~70%. Flash frames punch brighter, creating more intense afterimages.
6. **Add noise**: Enable Color Trail and set Persist to ~40%. Film grain fills the dark gaps, giving the trails an organic texture.

**Key concepts**: IIR persistence is an exponential moving average, higher shift values create longer trails, the blend stage takes the maximum of persistence and current input so flashes always punch through

---

### Exercise 3: Stroboscopic Abstraction

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: strobe_source1_runner, after: strobe_ex3_s1 },
    { label: "Dog", before: strobe_source2_dog, after: strobe_ex3_s2 },
    { label: "Collage", before: strobe_source3_collage, after: strobe_ex3_s3 },
    { label: "Pattern", before: strobe_source4_pattern, after: strobe_ex3_s4 },
    { label: "Boy", before: strobe_source5_boy, after: strobe_ex3_s5 },
    { label: "Knit", before: strobe_source6_knit, after: strobe_ex3_s6 },
  ]}
/>
*Stroboscopic Abstraction — simulated result across source images.*
**Source**: Any high-contrast, moving footage — concert visuals, feedback loops, or oscilloscope patterns.

**Objective**: Combine all parameters for full stroboscopic deconstruction.

1. **Double flash**: Enable Freeze (double-flash mode). The strobe fires twice per cycle for denser layering.
2. **Fast rate**: Set Strobe Rate to ~60% and Exposures to ~15% for rapid narrow pulses.
3. **Deep persistence**: Set Brightness to ~90% for long-decaying trails.
4. **Heavy noise**: Enable Color Trail and set Persist to ~70%. Dense grain fills every dark gap.
5. **Monochrome**: Enable Sync (mono mode). The grayscale output emphasizes the stroboscopic structure.
6. **Low dark level**: Set Decay to ~10% for maximum contrast between flash and dark.
7. **Mix modulation**: Sweep the Mix fader to blend between the raw source and the strobed abstraction.

**Key concepts**: Double flash creates denser exposure layers, monochrome emphasizes temporal structure over color, noise texture interacts with persistence trails to create organic grain patterns

---


## Tips

- **Strobe Rate and Exposures are independent**: Rate sets how often the strobe fires; Exposures sets how long each flash lasts. Adjust both to find the rhythm.
- **Persistence is the key to multi-exposure**: Turn up Brightness (pot 4) to build up ghost trails. Low values give crisp double-exposures; high values give long luminous smears.
- **Dark level shapes the contrast**: Decay controls how deep the darkness goes between flashes. For dramatic results, keep it low; for subtle flickering, keep it high.
- **Noise adds texture to darkness**: Enable Color Trail and increase Persist (pot 5) to fill the dark gaps with film grain. The grain sits on top of persistence trails for an organic feel.
- **Double flash for density**: Enable Freeze (toggle 10) to fire two pulses per cycle, creating tighter multi-exposure layering.
- **Mono for clarity**: Enable Sync (mono) to strip color and focus on the temporal structure of the strobe pattern.
- **Mix for transparency**: Use the Mix fader to overlay the strobe effect at partial opacity on the source for subtle ghost-trail additions.
- **Feedback loops**: Route the output back to the input for self-referencing stroboscopic recursion — persistence feeds back into the flash gate.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDS** | Direct Digital Synthesis; a numerically-controlled oscillator using a phase accumulator to generate periodic waveforms at arbitrary frequencies. |
| **Duty Cycle** | The ratio of flash-on time to total cycle time; controlled by the Exposures parameter. |
| **IIR** | Infinite Impulse Response; a filter type where the output depends on both current input and previous output, creating exponential decay. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function of its previous state, producing a pseudo-random bit sequence. |
| **Persistence** | The IIR-based temporal memory that holds decaying afterimages of previous flash frames, creating multi-exposure layering. |
| **Phase Accumulator** | A counter that wraps at a fixed bit width, with the increment determining the output frequency of the DDS oscillator. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage applying brightness and contrast adjustment to a signal. |
| **Stroboscope** | A device that produces brief periodic flashes of light, used to freeze apparent motion at the flash rate. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
