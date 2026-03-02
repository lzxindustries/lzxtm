---
draft: true
sidebar_position: 145
slug: /instruments/videomancer/jammer
title: "Jammer"
image: /img/instruments/videomancer/jammer/jammer_hero.png
description: "Every television signal travels through the air as radio waves, and the air is full of other radio waves."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import jammer_hero from '/img/instruments/videomancer/jammer/jammer_hero.png';
import jammer_control_panel from '/img/instruments/videomancer/jammer/jammer_control_panel.png';
import jammer_exercise1_result from '/img/instruments/videomancer/jammer/jammer_exercise1_result.png';
import jammer_exercise2_result from '/img/instruments/videomancer/jammer/jammer_exercise2_result.png';
import jammer_exercise3_result from '/img/instruments/videomancer/jammer/jammer_exercise3_result.png';
import jammer_source1_kodim15 from '/img/instruments/videomancer/jammer/jammer_source1_kodim15.png';
import jammer_source2_kodim01 from '/img/instruments/videomancer/jammer/jammer_source2_kodim01.png';
import jammer_source3_stream_bridge_512 from '/img/instruments/videomancer/jammer/jammer_source3_stream_bridge_512.png';

# Jammer

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: jammer_source1_kodim15, after: jammer_hero },
    { label: "Kodim01", before: jammer_source2_kodim01, after: jammer_hero },
    { label: "Stream Bridge", before: jammer_source3_stream_bridge_512, after: jammer_hero },
  ]}
/>
*Jammer applying herringbone beat patterns, rolling bars, and multipath ghosting to simulate broadcast RF interference.*

---

## Overview

Every television signal travels through the air as radio waves, and the air is full of other radio waves. When an unwanted signal is close in frequency to the desired broadcast, the two interact inside the receiver's tuner and produce structured visual artifacts — diagonal line patterns, rolling horizontal bars, displaced ghost images, and bright noise bursts. These interference signatures were a routine part of the analog television experience, and each type of artifact told a skilled engineer something specific about the source of the problem.

Jammer recreates this entire family of RF interference artifacts as a real-time video processing chain. A DDS (direct digital synthesis) phase accumulator generates herringbone or moire beat patterns at user-controlled spatial frequency and angle. A secondary vertical phase accumulator creates rolling horizontal bars that sweep the screen. Three 1024×10-bit line buffers produce a horizontally-displaced ghost copy of the input, simulating multipath reception from a reflected signal. A 16-bit LFSR generates impulsive noise bursts and per-line sync jitter. The name *Jammer* refers to the deliberate jamming of a signal — the intentional injection of interference to disrupt communication. Here the disruption becomes the creative medium.

At subtle settings, Jammer adds a faint herringbone texture and barely-visible ghost to an otherwise clean image — the equivalent of a marginal antenna on a windy day. At extreme settings, it reduces the signal to a chaotic overlay of competing patterns, rolling bars, displaced copies, and impulsive noise that overwhelms the source entirely. There is no bypass toggle — the Mix fader is the only way to attenuate the effect, which means the interference can never be fully separated from the signal, just as in real RF conditions.

---

## Background

### What Is Herringbone Interference?

When two RF carriers are close in frequency, the difference between them — the *beat frequency* — falls within the video bandwidth and appears on screen as a fine diagonal line pattern. The pattern is called **herringbone** because it resembles the V-shaped weave of herringbone cloth. The spatial frequency of the pattern corresponds to the frequency offset between the desired and interfering carriers, and the diagonal angle is determined by the phase relationship between the two signals per scan line. Television engineers used the angle and frequency of herringbone patterns to identify the source of interference: a pattern at exactly 920 kHz diagonal, for example, indicated that a nearby station's audio subcarrier was leaking into the video band.

### What Are Rolling Bars?

When the interfering signal is strong enough to affect the receiver's automatic gain control (AGC), it modulates the overall brightness of the image in broad horizontal bands. These bars *roll* vertically because the frequency offset between the two carriers causes the interference envelope to drift through successive scan lines at the beat rate. The visual effect is a slow, rhythmic pulsation of light and dark bands sweeping up or down the screen. The roll speed is directly proportional to the frequency offset — a larger offset means faster roll.

### What Is Multipath Ghosting?

A television antenna receives not only the direct signal from the transmitter, but also copies that have bounced off buildings, hills, or aircraft. These reflected copies arrive later than the direct signal, and the receiver displays them as horizontally-displaced duplicates — **ghosts**. The delay of the ghost corresponds to the extra path length of the reflected signal (approximately 1 microsecond per 300 meters). Ghost images always appear to the right of the main image because the reflected signal arrives later than the direct one. Jammer's line buffer BRAM implementation captures this horizontal delay with a 1024-sample depth, creating ghosts that can span up to half the screen width.

### What Is Impulse Noise?

Not all interference is continuous. Electric motors, ignition systems, power switches, and fluorescent lighting generate brief, intense bursts of radio-frequency energy that appear on screen as random bright specks — **impulse noise**. Unlike herringbone patterns, which are periodic and structured, impulse noise is stochastic. Jammer's LFSR-based impulse generator produces random bright pixel bursts whose density is controlled by the Interference parameter, simulating everything from a distant electric drill to a nearby arc welder.

### What Is Sync Disruption?

The horizontal sync pulse at the beginning of each scan line tells the receiver where to start drawing. When interference is strong enough to corrupt these pulses, the receiver's sync separator produces erratic timing, and the scan line starts at a slightly wrong horizontal position. The visible result is **horizontal jitter** — the image appears to shake or tear line-by-line. Jammer simulates this by displacing the write address of the line buffer by an LFSR-derived offset on each scan line when Sync Jam is enabled.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y/U/V Channels ─────────────────────────────────────────────
│   │
│   ├─ 1. Line Buffer Write     (write current pixel to BRAM)
│   │      └─ Sync Jam jitter   (LFSR-driven write-address displacement)
│   │
│   ├─ 2. Ghost Read            (read from BRAM at delayed address)
│   │      └─ Ghost Delay       (offset between write and read addresses)
│   │
│   ├─ 3. Ghost Blend           (attenuated ghost added to live input)
│   │      └─ Ghost Level       (scales ghost copy amplitude)
│   │      └─ Chroma Int        (ghost added to Y only or full YUV)
│   │
│   ├─ 4. Herringbone / Moire   (DDS phase accumulator → triangle wave)
│   │      ├─ Beat Freq          (per-pixel phase increment)
│   │      ├─ Angle              (per-line phase offset)
│   │      ├─ Pattern            (Herringbone diagonal vs. Moire circular)
│   │      └─ Interference       (scales pattern amplitude)
│   │
│   ├─ 5. Rolling Bars          (vertical phase accumulator → triangle wave)
│   │      ├─ Roll Rate          (per-frame phase increment)
│   │      ├─ Bar Mode           (additive or multiplicative overlay)
│   │      └─ Interference       (scales bar amplitude)
│   │
│   ├─ 6. Impulse Noise         (LFSR salt pattern, Y channel only)
│   │      └─ Interference       (density threshold for noise)
│   │
│   └─ 7. Compose               (final clamped Y/U/V output)
│
├── Interpolator (4 clk) ───────────────────────────────────────
│   └─ Wet/dry crossfade        (Mix fader: dry ↔ processed)
│
└── Sync Signals ───────────────────────────────────────────────
    └─ Pass-through (hsync, vsync, field, avid) via delay pipeline
```

The processing order matters significantly. The ghost image is blended first because it represents a displaced copy of the *clean* input, not of the interference pattern. The herringbone and rolling bar patterns are then added to the ghost-blended signal. Impulse noise is applied last (before the interpolator) so that the noise bursts sit on top of all prior processing. Sync jitter operates at the line buffer stage, displacing the *write* address, which means the ghost read is also affected by jitter — jitter on the ghost is doubled, as it is in real multipath reception with sync corruption.

The Chroma Int toggle controls whether the herringbone pattern and ghost image affect only the Y channel or the full YUV signal. In real television, chrominance is carried on a subcarrier at a known offset from the luminance carrier, so interference that affects luminance may or may not affect chroma depending on the frequency relationship. Y-only mode is more realistic for adjacent-channel interference; Full YUV mode produces a more dramatic, colorful distortion.

---

## Parameter Reference

<img src={jammer_control_panel} alt="Videomancer front panel with Jammer loaded"/>
*Videomancer's front panel with Jammer active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Beat Freq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the spatial frequency of the herringbone (or moire) interference pattern. This is the per-pixel phase increment of the DDS accumulator. Low values produce coarse, widely-spaced diagonal lines visible as broad bands. High values create fine, tightly-packed lines that appear as a dense texture or moire shimmer. In real RF interference, this parameter corresponds to the frequency offset between the desired and interfering carriers — a small offset produces slow, visible beats while a large offset produces rapid fine-grain texture.

---

#### Knob 2 — Angle
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the diagonal angle of the herringbone pattern by controlling the per-line phase offset added to the beat accumulator at each horizontal sync. At zero, the interference lines are purely vertical. As Angle increases, the lines tilt diagonally, creating the characteristic V-shaped herringbone weave. At maximum, the lines are nearly horizontal. In moire mode, Angle has no effect since the pattern is radially symmetric.

---

#### Knob 3 — Roll Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the vertical roll rate of the horizontal bar pattern. At zero, the bars are stationary (a fixed brightness modulation across the screen). As Roll Rate increases, the bars sweep vertically at increasing speed, creating the classic rolling-bar artifact of off-frequency interference. The roll direction depends on the polarity of the frequency offset. At high values, the bars scroll so fast they blur into a uniform brightness shift.

---

#### Knob 4 — Interference
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Master amplitude control for the interference effects. This parameter scales the herringbone pattern, the rolling bars, and the impulse noise density simultaneously. At zero, no interference is added regardless of other settings. At maximum, the interference overwhelms the source signal. Think of this as the power level of the interfering transmitter — a distant jammer produces faint artifacts, a nearby one produces severe disruption.

---

#### Knob 5 — Ghost Delay
| Property | Value |
|----------|-------|
| Range | 0 – 256 |
| Default | 0 |

Sets the horizontal displacement of the ghost image in samples. At zero, the ghost overlaps the original (no visible effect). As Ghost Delay increases, the ghost copy moves further to the right, creating a progressively more displaced duplicate. The maximum delay uses the full 1024-sample depth of the line buffer BRAMs, offsetting the ghost by roughly half the active picture width. In real television, ghost delay corresponds to the extra propagation distance of the reflected signal path.

---

#### Knob 6 — Ghost Level
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the brightness of the ghost image. At zero, the ghost is invisible even if Ghost Delay is active. As Ghost Level increases, the delayed copy becomes more prominent. The ghost is added to the live signal via saturating addition, so at high levels the combination of live and ghost can clip to white in bright areas. When Chroma Int is set to Full YUV, the ghost's color channels are also added, producing color fringing on the displaced copy.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Impulse** | Off | On |
| **8 — Sync Jam** | Off | On |
| **9 — Bar Mode** | Add | Multiply |
| **10 — Chroma Int** | Y Only | Full YUV |
| **11 — Pattern** | Herring | Moire |

Switches 7–11 control five independent binary processing options. There is intentionally no bypass toggle — the Mix fader is the only way to reduce the effect. Impulse and Sync Jam enable stochastic noise processes. Bar Mode selects the mathematical relationship between the rolling bars and the image. Chroma Int controls whether interference affects luminance only or all three channels. Pattern selects the geometry of the beat pattern.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade. At 0%, the output is the unprocessed input signal — no interference visible. At 100%, the output is the fully-processed signal with all enabled interference effects at full amplitude. Because there is no bypass toggle, this fader is the only way to attenuate the effect. Intermediate positions blend the clean and jammed signals, which can simulate the behavior of a receiver's automatic gain control as it partially suppresses an interfering signal.

---

## Guided Exercises

These exercises progress from a single interference artifact to the full signal-jamming experience. Each exercise adds another layer of disruption, building from recognizable broadcast artifacts to total signal degradation.

### Exercise 1: Herringbone and Rolling Bars

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: jammer_source1_kodim15, after: jammer_exercise1_result },
    { label: "Kodim01", before: jammer_source2_kodim01, after: jammer_exercise1_result },
    { label: "Stream Bridge", before: jammer_source3_stream_bridge_512, after: jammer_exercise1_result },
  ]}
/>
*Herringbone and Rolling Bars — simulated result across source images.*
**Source**: A live camera feed or recorded footage with well-defined horizontal and vertical structures — architecture, grids, or text.

**Objective**: Learn how Beat Freq, Angle, and Roll Rate create the two primary interference patterns.

1. **Herringbone**: Set Beat Freq to ~25% and Angle to ~25%. A diagonal line pattern appears over the image.
2. **Frequency**: Sweep Beat Freq from 0% to 100%. Watch the pattern transition from coarse bands to fine texture.
3. **Angle**: Sweep Angle from 0% to 100%. Watch the lines tilt from vertical to nearly horizontal.
4. **Rolling bars**: Set Roll Rate to ~25%. Broad horizontal bands begin scrolling vertically over the image.
5. **Bar mode**: Toggle Bar Mode between Add and Multiply. In Add, the bars brighten and darken the image. In Multiply, they modulate the image gain without shifting black level.
6. **Moire**: Toggle Pattern to Moire. The diagonal herringbone is replaced by concentric circular interference rings — note that Angle has no effect in this mode.

**Key concepts**: Herringbone comes from DDS beat frequency, angle comes from per-line phase offset, rolling bars are a vertical phase accumulator, multiplicative bars preserve black level

---

### Exercise 2: Multipath Ghosting

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: jammer_source1_kodim15, after: jammer_exercise2_result },
    { label: "Kodim01", before: jammer_source2_kodim01, after: jammer_exercise2_result },
    { label: "Stream Bridge", before: jammer_source3_stream_bridge_512, after: jammer_exercise2_result },
  ]}
/>
*Multipath Ghosting — simulated result across source images.*
**Source**: Footage with bright subjects against dark backgrounds — text on black, or a person against a dark wall.

**Objective**: Explore the ghost delay line and its interaction with the interference pattern.

1. **Prepare**: Set Interference to ~30%. Set Beat Freq and Roll Rate to low values for a visible but subtle pattern.
2. **Ghost delay**: Slowly increase Ghost Delay from 0 to ~50%. A displaced copy of the image appears to the right of the original.
3. **Ghost level**: Increase Ghost Level from 0% to ~60%. The ghost brightens. Note how bright areas of the ghost clip to white.
4. **Chroma ghost**: Toggle Chroma Int to Full YUV. The ghost now carries color, producing visible color fringing on the displaced copy.
5. **Sync jam**: Enable Sync Jam. The ghost tears horizontally as the per-line jitter displaces both the write and read addresses — the ghost displacement doubles on some lines.

**Key concepts**: Ghost delay is horizontal displacement via BRAM line buffer, ghost level is amplitude, chroma int extends ghost to color channels, sync jam jitters the buffer addresses

---

### Exercise 3: Total Signal Jamming

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: jammer_source1_kodim15, after: jammer_exercise3_result },
    { label: "Kodim01", before: jammer_source2_kodim01, after: jammer_exercise3_result },
    { label: "Stream Bridge", before: jammer_source3_stream_bridge_512, after: jammer_exercise3_result },
  ]}
/>
*Total Signal Jamming — simulated result across source images.*
**Source**: Any footage — the source will be almost completely obscured by interference.

**Objective**: Layer all interference artifacts together for full signal disruption.

1. **Strong pattern**: Set Beat Freq ~40%, Angle ~30%, Roll Rate ~35%, Interference ~80%.
2. **Ghost**: Set Ghost Delay ~80, Ghost Level ~50%.
3. **Noise**: Enable Impulse. Random bright specks appear across the image.
4. **Sync disruption**: Enable Sync Jam. The image tears horizontally with per-line jitter.
5. **Full chroma**: Toggle Chroma Int to Full YUV for colored interference.
6. **Multiply bars**: Toggle Bar Mode to Multiply. The bars now modulate the image gain, creating rhythmic fading bands.
7. **Mix recovery**: Lower Mix to ~60%. The clean image partially shows through the interference — simulating a receiver partially locking onto the desired signal despite jamming.

**Key concepts**: All artifacts layer simultaneously (ghost + herringbone + bars + impulse + jitter), interference is the master amplitude, mix is the only attenuation path (no bypass toggle)

---


## Tips

- **No bypass**: Unlike most programs, Jammer has no bypass toggle. Use the Mix fader to blend between clean and jammed signals — this is intentional, because real RF interference always blends.
- **Interference is the master amplitude**: The Interference knob scales herringbone, rolling bar, and impulse density simultaneously. Start here to set the overall severity.
- **Ghost before pattern**: The ghost is blended before the herringbone pattern, so the interference covers both the live and ghost images. To see the ghost clearly, reduce Beat Freq and Interference briefly.
- **Sync Jam is destructive**: Sync jitter affects the BRAM write address, which means it corrupts the ghost buffer as well. High jitter with large ghost delay produces severe tearing.
- **Multiply bars for realism**: Multiplicative rolling bars are closer to real AGC modulation, where interference suppresses gain rather than adding brightness. Additive bars are more dramatic visually.
- **Moire for circular patterns**: When subject matter has strong circular or radial features, switching to Moire mode creates concentric interference rings that interact with the content structure.
- **Feedback loops**: Routing Jammer's output back to the input creates self-referencing interference — the ghost ghosts itself, the herringbone interferes with the herringbone, and the signal degrades progressively.

---

## Glossary

| Term | Definition |
|------|------------|
| **AGC** | Automatic Gain Control; a receiver circuit that adjusts amplification to maintain constant signal level. Strong interference can overload AGC, causing brightness modulation. |
| **Beat Frequency** | The difference frequency produced when two signals close in frequency are mixed together. Appears as a visible pattern on screen. |
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for the 1024×10-bit line buffers that produce ghost delay. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms using a phase accumulator and lookup, used here for herringbone pattern generation. |
| **Ghost** | A displaced, attenuated copy of the television image caused by multipath signal reception (reflections off buildings, terrain, or aircraft). |
| **Herringbone** | A diagonal striped interference pattern caused by near-frequency beat interaction between desired and interfering RF carriers. |
| **Impulse Noise** | Short, intense bursts of radio interference from electrical switching, motors, or ignition systems, appearing as random bright specks. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used to produce impulse noise and sync jitter patterns. |
| **Moire** | Circular concentric interference rings produced by radial distance modulation, alternative to diagonal herringbone geometry. |
| **Multipath** | Signal reception via multiple propagation paths (direct + reflected), causing ghost images due to differential propagation delay. |
| **Pipeline** | A series of sequential processing stages; Jammer uses 8 clock cycles (4 processing + 4 interpolator). |
| **Sync Separator** | A receiver circuit that extracts horizontal and vertical sync pulses from the composite signal. Interference can corrupt separation and cause horizontal jitter. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
