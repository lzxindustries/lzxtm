---
draft: true
sidebar_position: 2
slug: /instruments/videomancer/afterimage
title: "Afterimage"
image: /img/instruments/videomancer/afterimage/afterimage_hero_s1.png
description: "Afterimage recreates the physiological phenomenon where prolonged viewing of a stimulus produces a persistent colour-negative ghost when the stimulus is removed or the gaze shifts."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import afterimage_control_panel from '/img/instruments/videomancer/afterimage/afterimage_control_panel.png';
import afterimage_source1_boat from '/img/instruments/videomancer/afterimage/afterimage_source1_boat.png';
import afterimage_source2_runner from '/img/instruments/videomancer/afterimage/afterimage_source2_runner.png';
import afterimage_source3_turtle from '/img/instruments/videomancer/afterimage/afterimage_source3_turtle.png';
import afterimage_source4_pattern from '/img/instruments/videomancer/afterimage/afterimage_source4_pattern.png';
import afterimage_source5_man from '/img/instruments/videomancer/afterimage/afterimage_source5_man.png';
import afterimage_source6_wood from '/img/instruments/videomancer/afterimage/afterimage_source6_wood.png';
import afterimage_hero_s1 from '/img/instruments/videomancer/afterimage/afterimage_hero_s1.png';
import afterimage_hero_s2 from '/img/instruments/videomancer/afterimage/afterimage_hero_s2.png';
import afterimage_hero_s3 from '/img/instruments/videomancer/afterimage/afterimage_hero_s3.png';
import afterimage_hero_s4 from '/img/instruments/videomancer/afterimage/afterimage_hero_s4.png';
import afterimage_hero_s5 from '/img/instruments/videomancer/afterimage/afterimage_hero_s5.png';
import afterimage_hero_s6 from '/img/instruments/videomancer/afterimage/afterimage_hero_s6.png';
import afterimage_ex1_s1 from '/img/instruments/videomancer/afterimage/afterimage_ex1_s1.png';
import afterimage_ex1_s2 from '/img/instruments/videomancer/afterimage/afterimage_ex1_s2.png';
import afterimage_ex1_s3 from '/img/instruments/videomancer/afterimage/afterimage_ex1_s3.png';
import afterimage_ex1_s4 from '/img/instruments/videomancer/afterimage/afterimage_ex1_s4.png';
import afterimage_ex1_s5 from '/img/instruments/videomancer/afterimage/afterimage_ex1_s5.png';
import afterimage_ex1_s6 from '/img/instruments/videomancer/afterimage/afterimage_ex1_s6.png';
import afterimage_ex2_s1 from '/img/instruments/videomancer/afterimage/afterimage_ex2_s1.png';
import afterimage_ex2_s2 from '/img/instruments/videomancer/afterimage/afterimage_ex2_s2.png';
import afterimage_ex2_s3 from '/img/instruments/videomancer/afterimage/afterimage_ex2_s3.png';
import afterimage_ex2_s4 from '/img/instruments/videomancer/afterimage/afterimage_ex2_s4.png';
import afterimage_ex2_s5 from '/img/instruments/videomancer/afterimage/afterimage_ex2_s5.png';
import afterimage_ex2_s6 from '/img/instruments/videomancer/afterimage/afterimage_ex2_s6.png';
import afterimage_ex3_s1 from '/img/instruments/videomancer/afterimage/afterimage_ex3_s1.png';
import afterimage_ex3_s2 from '/img/instruments/videomancer/afterimage/afterimage_ex3_s2.png';
import afterimage_ex3_s3 from '/img/instruments/videomancer/afterimage/afterimage_ex3_s3.png';
import afterimage_ex3_s4 from '/img/instruments/videomancer/afterimage/afterimage_ex3_s4.png';
import afterimage_ex3_s5 from '/img/instruments/videomancer/afterimage/afterimage_ex3_s5.png';
import afterimage_ex3_s6 from '/img/instruments/videomancer/afterimage/afterimage_ex3_s6.png';

# Afterimage

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: afterimage_source1_boat, after: afterimage_hero_s1 },
    { label: "Runner", before: afterimage_source2_runner, after: afterimage_hero_s2 },
    { label: "Turtle", before: afterimage_source3_turtle, after: afterimage_hero_s3 },
    { label: "Pattern", before: afterimage_source4_pattern, after: afterimage_hero_s4 },
    { label: "Man", before: afterimage_source5_man, after: afterimage_hero_s5 },
    { label: "Wood", before: afterimage_source6_wood, after: afterimage_hero_s6 },
  ]}
/>
*Afterimage rendering a color-negative persistence trail over a moving hand — the IIR temporal filter retains a ghostly complementary-color echo of prior motion against the current frame.*

---

## Overview

Afterimage recreates the physiological phenomenon where prolonged viewing of a stimulus produces a persistent colour-negative ghost when the stimulus is removed or the gaze shifts. The program uses per-pixel IIR (infinite impulse response) low-pass filtering to build a temporal average of the input video, then computes a colour-negative of that average and blends it back into the current frame. Moving subjects leave behind trails of their complementary colours — a red object deposits a cyan ghost, a bright region leaves a dark shadow.

The name *Afterimage* references the neurological phenomenon described by Hermann von Helmholtz in *Handbuch der physiologischen Optik* (1856). Negative afterimages occur because cone cells in the retina become fatigued by sustained stimulation and temporarily reduce their sensitivity — when the stimulus changes, the fatigued cones respond less than their neighbours, producing the perception of the complementary colour. This program externalises that retinal process as a real-time video effect.

At conservative settings — slow persistence with low negative strength — the program produces subtle ghostly trails that add a dreamlike quality to motion. At extreme settings — fast persistence, full negative strength, and chroma-only channel mode — the output becomes a violent palette inversion that constantly fights the input signal, creating psychedelic colour fields that pulse and breathe with any movement.

---

## Background

### What Is a Negative Afterimage?

A **negative afterimage** is a visual phenomenon where staring at a coloured stimulus for an extended period, then looking away, produces a ghost image in the complementary colour. Stare at a red square for 30 seconds, then look at a white wall — you see a cyan square. This occurs because the cone cells sensitive to red become fatigued and temporarily reduce their response, making the remaining (green and blue) cones relatively more active.

The effect was first systematically studied by Jan Evangelista Purkyně in the 1820s and later formalised by Helmholtz. Artists including Jasper Johns and Bridget Riley have incorporated afterimage effects into their work, creating paintings designed to produce vivid complementary ghosts when viewed.

### What Is IIR Temporal Filtering?

An **IIR (Infinite Impulse Response) filter** is a feedback system where the output depends not only on the current input but also on previous output values. In the context of video processing, an IIR temporal filter maintains a running average that accumulates over time — each new frame nudges the average toward the current input, but the average retains memory of all prior frames with exponentially decaying influence.

The specific IIR used in Afterimage is a first-order exponential moving average: `average += (input - average) >> shift`. The shift amount controls the time constant — larger shifts produce slower response (longer persistence). This architecture requires no frame buffer: each pixel's accumulator is stored in a single register that is updated every time that pixel position is clocked through the pipeline. Because the FPGA processes pixels in raster order, the accumulator operates per-column (not per-pixel), producing a columnar temporal smear rather than true per-pixel persistence.

### What Are Complementary Colours in YUV?

In YUV colour space, the complement of a colour is formed by inverting the chrominance channels (U and V) around the midpoint (512 in 10-bit). A colour at (Y, U, V) has its complement at (1023-Y, 1023-U, 1023-V) for full negative, or various partial inversions for the other modes. The luminance complement inverts bright to dark, while the chrominance complement swaps warm for cool and vice versa.


---

## Signal Flow

Y/U/V Channels → Sync Signals → Interpolator → Output

```
Input Video (YUV 4:4:4 30-bit)
│
├── Y/U/V Channels ─────────────────────────────────────────────────
│   │
│   ├─ 1.  IIR accumulator           (per-channel running average,
│   │       (per column)               shift controlled by Persist pot
│   │                                  + Speed toggle)
│   ├─ 2.  Decay toward midpoint     (pull accum toward 512 at vsync,
│   │                                  shift 5-8 from Decay pot)
│   ├─ 3.  Negative computation      (Mode select:
│   │                                  Negative = 1023 - avg
│   │                                  Complement = mirror around 512
│   │                                  Invert = 1023 - current input
│   │                                  Ghost = passthrough average)
│   ├─ 4.  Channel selector          (All / Luma / Chroma / Hue from
│   │                                  Toggle 8 — selects which
│   │                                  channels receive processing)
│   ├─ 5.  Blend                     (input + (neg - input) × neg_str
│   │                                  from Blend pot)
│   ├─ 6.  Brightness offset         (add Bright pot - 512)
│   ├─ 7.  Saturation scale          (scale chroma deviation from 512
│   │                                  by Saturate pot)
│   └─ 8.  Output register
│
├── Sync Signals ───────────────────────────────────────────────────
│   └─ 9-clock delay pipeline         (align with processing depth)
│
├── Interpolator (4 clocks per channel) ────────────────────────────
│   └─ Mix = lerp(input_delayed, processed, mix_amount)
│
└── Output ─────────────────────────────────────────────────────────
    └─ Y/U/V from interpolator mix
```

The IIR accumulator operates per-column rather than per-pixel because there is no full frame buffer — each pixel position's history is stored in a single register that gets updated once per frame when that column passes through the pipeline. This means vertical objects produce clean persistence while horizontal motion creates slightly different trails depending on scan direction.

The Speed toggle selects between two shift-amount ranges for the IIR: Fast mode (shifts 1-4) adapts quickly for rapid stuttery persistence, while Slow mode (shifts 3-7) builds gradual ghostly trails that fade over seconds. The Decay mechanism separately pulls the accumulator toward the midpoint at each vsync pulse, ensuring that the ghost eventually fades even if the input becomes static.

---

## Parameter Reference

<img src={afterimage_control_panel} alt="Videomancer front panel with Afterimage loaded"/>
*Videomancer's front panel with Afterimage active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Persist
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At minimum, the accumulator adapts almost instantly — persistence is barely visible. At maximum, the accumulator changes extremely slowly, retaining ghosts of previously displayed content for many seconds. The persist value maps to a bit-shift amount that divides the difference between the current input and the running average: higher persist = larger shift = slower adaptation. Combined with the Speed toggle, this provides a wide range from sub-frame response to multi-second persistence. Internally, controls the time constant of the IIR temporal filter.

---

#### Knob 2 — Neg Str
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, no negative component is added and the output matches the input (the IIR runs but its result is not visible). At maximum, the full computed negative replaces the input. Intermediate values blend between the input pixel and the negative pixel, allowing the afterimage ghost to appear at any opacity from a faint whisper to a full colour inversion. Internally, controls the intensity of the negative colour computation blended into the output.

---

#### Knob 3 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At minimum, there is no decay — ghosts persist indefinitely until overwritten by new input. At maximum, the accumulator is aggressively pulled toward neutral every frame, causing ghosts to fade rapidly. This interacts with Persist: high persist with low decay creates long-lived afterimages, while high persist with high decay creates a constantly shifting, breathing ghost field. Internally, controls the rate at which the IIR accumulator decays toward the neutral midpoint (512) during vertical blanking.

---

#### Knob 4 — Blend
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, the output is pure input with no afterimage effect. At 100%, the output is purely the negative of the temporal average. This differs from Neg Str in that Blend controls the final mix ratio while Neg Str controls the intensity of the negative computation itself — using both at moderate levels produces subtler, more layered results than either at maximum. Internally, controls the crossfade between the original input and the negative-processed signal.

---

#### Knob 5 — Saturate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scales the chrominance channels of the processed output. The saturation control operates after mode processing, scaling the distance of U and V values from the chroma midpoint (512). At 0%, the output is fully monochrome — luminance-only afterimage effects. At moderate values, natural colour persistence appears. Boosted above 50%, the afterimage colours become hyper-vivid, exaggerating the complementary colour effect beyond what physiological afterimages would produce.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a constant brightness offset to the processed output. At 50% (512), brightness is neutral. Below 50%, the image is darkened; above 50%, it is brightened. The offset is applied after the negative computation and blend, so it shifts the overall luminance of the afterimage-processed image without affecting the IIR accumulator or negative calculation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Negative | Ghost |
| **8 — Channel** | All | Hue |
| **9 — Speed** | Slow | Fast |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Toggle 7 provides a **4-position mode selector** controlling how the temporal average is processed into a negative: Negative (full inversion: 1023 minus average), Complement (mirror around midpoint 512), Invert (invert the current input pixel rather than the average), and Ghost (passthrough of the raw temporal average with no inversion). Toggle 8 provides a **4-position channel selector** determining which channels receive processing: All (Y+U+V), Luma (Y only, chroma passes through), Chroma (U+V only, luma passes through), and Hue (chroma with modified routing). Toggles 9-11 are **independent binary controls**.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Afterimage-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from basic negative persistence observation through channel-isolated effects to complex multi-mode interaction, building familiarity with the IIR temporal filter behavior.

### Exercise 1: Basic Negative Persistence

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: afterimage_source1_boat, after: afterimage_ex1_s1 },
    { label: "Runner", before: afterimage_source2_runner, after: afterimage_ex1_s2 },
    { label: "Turtle", before: afterimage_source3_turtle, after: afterimage_ex1_s3 },
    { label: "Pattern", before: afterimage_source4_pattern, after: afterimage_ex1_s4 },
    { label: "Man", before: afterimage_source5_man, after: afterimage_ex1_s5 },
    { label: "Wood", before: afterimage_source6_wood, after: afterimage_ex1_s6 },
  ]}
/>
*Basic Negative Persistence — simulated result across source images.*
**Source**: Camera feed with a moving subject against a static background — a hand waving slowly works well.

**What You'll Create**: Observe how the IIR temporal filter creates colour-negative ghosts of moving subjects and how Persist and Neg Str control the trail intensity and duration.

1. **Default mode**: Set Mode to Negative, Channel to All, Speed to Fast, Animate off. Mix at 100%.
2. **Moderate persistence**: Set Persist to ~60%, Neg Str to ~50%, Decay to ~30%, Blend to ~70%.
3. **Observe motion**: Move your hand across the camera. After your hand passes, a cyan/blue ghost remains where the warm skin tones were — the complementary colour of the skin.
4. **Increase persist**: Raise Persist to ~90%. The ghost lingers much longer. Move your hand and wait — the afterimage persists for several seconds before fading.
5. **Reduce decay**: Drop Decay to ~10%. Now the ghost barely fades at all — the IIR accumulator retains information almost indefinitely.
6. **Maximum negative**: Push Neg Str to 100%, Blend to 100%. The afterimage dominates the output — moving objects leave violently inverted trails.

**Key concepts**: IIR temporal averaging, complementary colour persistence, persist time constant, decay rate, negative blending

---

### Exercise 2: Chroma-Only Afterimage

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: afterimage_source1_boat, after: afterimage_ex2_s1 },
    { label: "Runner", before: afterimage_source2_runner, after: afterimage_ex2_s2 },
    { label: "Turtle", before: afterimage_source3_turtle, after: afterimage_ex2_s3 },
    { label: "Pattern", before: afterimage_source4_pattern, after: afterimage_ex2_s4 },
    { label: "Man", before: afterimage_source5_man, after: afterimage_ex2_s5 },
    { label: "Wood", before: afterimage_source6_wood, after: afterimage_ex2_s6 },
  ]}
/>
*Chroma-Only Afterimage — simulated result across source images.*
**Source**: Footage with saturated primary colours — a colourful painting, fruit, or clothing.

**What You'll Create**: Use the channel selector to isolate afterimage processing to chrominance only, preserving luminance detail while producing colour-shift ghosts.

1. **Set Chroma mode**: Toggle Channel to Chroma (position 3). Mode stays at Negative.
2. **Moderate settings**: Persist ~50%, Neg Str ~70%, Decay ~20%, Blend ~80%, Mix 100%.
3. **Observe static**: With static input, the chroma channels slowly accumulate and invert — reds shift toward cyan, blues toward yellow, while the brightness detail of the image remains sharp.
4. **Add movement**: Move the camera or subject. Only the colour information ghosts — edges and brightness remain crisp while complementary colour trails follow motion.
5. **Compare with All**: Switch Channel back to All. Now luminance also ghosts — the image becomes darker or brighter inversions. Switch back to Chroma to see the difference.
6. **Boost saturation**: Push Saturate to ~90%. The chroma-only ghosts become hyper-vivid complementary colour fields.

**Key concepts**: Channel-isolated processing, chroma vs luminance persistence, complementary colour generation in UV space

---

### Exercise 3: Slow Ghost Mode with Breathing Animation

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: afterimage_source1_boat, after: afterimage_ex3_s1 },
    { label: "Runner", before: afterimage_source2_runner, after: afterimage_ex3_s2 },
    { label: "Turtle", before: afterimage_source3_turtle, after: afterimage_ex3_s3 },
    { label: "Pattern", before: afterimage_source4_pattern, after: afterimage_ex3_s4 },
    { label: "Man", before: afterimage_source5_man, after: afterimage_ex3_s5 },
    { label: "Wood", before: afterimage_source6_wood, after: afterimage_ex3_s6 },
  ]}
/>
*Slow Ghost Mode with Breathing Animation — simulated result across source images.*
**Source**: Any video source — slow-moving content like landscapes or abstract video works best.

**What You'll Create**: Combine Ghost mode (raw temporal average passthrough) with Slow speed and animation to create an ethereal, breathing echo layer.

1. **Set Ghost mode**: Toggle Mode to Ghost (position 4). Channel to All. Speed to Slow. Animate On.
2. **Long persistence**: Persist at ~80%, Blend at ~60%, Decay at ~15%.
3. **Observe**: The output shows a softened, time-averaged version of the input blended over the live signal — moving objects leave faded echoes that drift and pulse as the animate modulation varies the time constant.
4. **Reduce brightness**: Pull Bright to ~35%. The ghost layer darkens, creating a shadowy overlay.
5. **Increase blend**: Push Blend to ~90%. The temporal average dominates — the image smears and blurs temporally, with the breathing animation creating a gently pulsing quality.
6. **Switch to Complement**: Toggle Mode to Complement. Now the echoes are colour-shifted rather than ghost-faded — a more psychedelic rendering of the same temporal data.

**Key concepts**: Ghost mode (non-inverted temporal average), slow IIR response, animate modulation, complement vs ghost mode comparison

---


## Tips

- **Speed and Persist interact**: Fast+high persist ≈ Slow+medium persist in trail duration, but with different character. Fast mode produces stuttery, frame-stepping trails while Slow mode produces smooth, flowing ghosts.
- **Feedback routing amplifies afterimage**: Routing the output back through the input creates recursive afterimage processing that rapidly builds intense colour inversion fields. Start with low Neg Str and Blend when using feedback.
- **Chroma-only is subtle but powerful**: Channel set to Chroma produces colour shifts without luminance inversion — useful for augmenting live performance footage without destroying the visual clarity.
- **Decay controls the floor**: Even with maximum persistence, high decay ensures ghosts eventually fade. For permanent screen-burn style effects, minimize decay.
- **Blend vs Mix**: Blend controls the processing intensity (before output). Mix (fader) controls the wet/dry balance (after processing). Use Blend for creative control and Mix for A/B comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **Accumulator** | A register that stores a running total updated each frame; in Afterimage the IIR accumulators hold the per-column temporal average. |
| **Chrominance (Chroma)** | The colour-difference components of a video signal (U and V channels), encoding hue and saturation independently of brightness. |
| **Complementary Colour** | The colour produced by inverting a given colour around the neutral midpoint; red's complement is cyan, yellow's complement is blue. |
| **Exponential Moving Average (EMA)** | A weighted running average where each new sample adjusts the average by a fraction controlled by a bit-shift amount. Recent samples have more influence than older ones. |
| **IIR (Infinite Impulse Response)** | A filter type whose output depends on both the current input and its own previous output, producing persistent memory of past values. |
| **Luminance (Luma)** | The brightness component (Y channel) of a YUV video signal, representing perceived light intensity independent of colour. |
| **Midpoint** | The centre value of the 10-bit range (512); in YUV processing, U and V at 512 represent zero colour difference (neutral grey). |
| **Vsync (Vertical Sync)** | The blanking interval at the end of each video frame, used here as the timing reference for the decay mechanism that pulls accumulators toward neutral. |
| **Wet/Dry** | A mixing convention where "wet" is the fully processed signal and "dry" is the unprocessed original; the fader crossfades between them. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
