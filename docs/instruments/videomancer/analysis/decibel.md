---
draft: true
sidebar_position: 76
slug: /instruments/videomancer/decibel
title: "Decibel"
image: /img/instruments/videomancer/decibel/decibel_hero_s1.png
description: "Every sound engineer knows the VU meter — a swinging needle that follows the loudness of audio in near-real-time, giving an immediate, visceral sense of energy."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import decibel_control_panel from '/img/instruments/videomancer/decibel/decibel_control_panel.png';
import decibel_source1_runner from '/img/instruments/videomancer/decibel/decibel_source1_runner.png';
import decibel_source2_fruit from '/img/instruments/videomancer/decibel/decibel_source2_fruit.png';
import decibel_source3_clouds from '/img/instruments/videomancer/decibel/decibel_source3_clouds.png';
import decibel_source4_pattern from '/img/instruments/videomancer/decibel/decibel_source4_pattern.png';
import decibel_source5_man from '/img/instruments/videomancer/decibel/decibel_source5_man.png';
import decibel_source6_paint from '/img/instruments/videomancer/decibel/decibel_source6_paint.png';
import decibel_hero_s1 from '/img/instruments/videomancer/decibel/decibel_hero_s1.png';
import decibel_hero_s2 from '/img/instruments/videomancer/decibel/decibel_hero_s2.png';
import decibel_hero_s3 from '/img/instruments/videomancer/decibel/decibel_hero_s3.png';
import decibel_hero_s4 from '/img/instruments/videomancer/decibel/decibel_hero_s4.png';
import decibel_hero_s5 from '/img/instruments/videomancer/decibel/decibel_hero_s5.png';
import decibel_hero_s6 from '/img/instruments/videomancer/decibel/decibel_hero_s6.png';
import decibel_ex1_s1 from '/img/instruments/videomancer/decibel/decibel_ex1_s1.png';
import decibel_ex1_s2 from '/img/instruments/videomancer/decibel/decibel_ex1_s2.png';
import decibel_ex1_s3 from '/img/instruments/videomancer/decibel/decibel_ex1_s3.png';
import decibel_ex1_s4 from '/img/instruments/videomancer/decibel/decibel_ex1_s4.png';
import decibel_ex1_s5 from '/img/instruments/videomancer/decibel/decibel_ex1_s5.png';
import decibel_ex1_s6 from '/img/instruments/videomancer/decibel/decibel_ex1_s6.png';
import decibel_ex2_s1 from '/img/instruments/videomancer/decibel/decibel_ex2_s1.png';
import decibel_ex2_s2 from '/img/instruments/videomancer/decibel/decibel_ex2_s2.png';
import decibel_ex2_s3 from '/img/instruments/videomancer/decibel/decibel_ex2_s3.png';
import decibel_ex2_s4 from '/img/instruments/videomancer/decibel/decibel_ex2_s4.png';
import decibel_ex2_s5 from '/img/instruments/videomancer/decibel/decibel_ex2_s5.png';
import decibel_ex2_s6 from '/img/instruments/videomancer/decibel/decibel_ex2_s6.png';
import decibel_ex3_s1 from '/img/instruments/videomancer/decibel/decibel_ex3_s1.png';
import decibel_ex3_s2 from '/img/instruments/videomancer/decibel/decibel_ex3_s2.png';
import decibel_ex3_s3 from '/img/instruments/videomancer/decibel/decibel_ex3_s3.png';
import decibel_ex3_s4 from '/img/instruments/videomancer/decibel/decibel_ex3_s4.png';
import decibel_ex3_s5 from '/img/instruments/videomancer/decibel/decibel_ex3_s5.png';
import decibel_ex3_s6 from '/img/instruments/videomancer/decibel/decibel_ex3_s6.png';

# Decibel

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: decibel_source1_runner, after: decibel_hero_s1 },
    { label: "Fruit", before: decibel_source2_fruit, after: decibel_hero_s2 },
    { label: "Clouds", before: decibel_source3_clouds, after: decibel_hero_s3 },
    { label: "Pattern", before: decibel_source4_pattern, after: decibel_hero_s4 },
    { label: "Man", before: decibel_source5_man, after: decibel_hero_s5 },
    { label: "Paint", before: decibel_source6_paint, after: decibel_hero_s6 },
  ]}
/>
*Decibel rendering a 16-segment rainbow bar meter across a live video feed, with peak hold markers tracing transient brightness spikes in red.*

---

## Overview

Every sound engineer knows the VU meter — a swinging needle that follows the loudness of audio in near-real-time, giving an immediate, visceral sense of energy. Decibel brings that same concept to the video domain. Instead of measuring sound pressure, it measures luminance intensity: how bright the image is at each scanline or each column. The result is a classic bar-graph meter display rendered directly over the video signal — a live visualization of the signal's own energy.

The program implements a complete metering pipeline: an IIR (infinite impulse response) envelope follower smooths the raw luminance into a stable level reading, a peak tracker remembers transient spikes, and a segment quantizer maps the continuous level to discrete bar segments. Four display styles — Bar, Dot, Peak, and Fill — offer different visual interpretations: a solid running bar, a bouncing single-point indicator, a persistent peak marker, or a combined bar-plus-peak display. A configurable green-to-red color gradient follows the conventions of professional LED meter bridges, where green indicates safe headroom and red warns of clipping.

The name *Decibel* — the logarithmic unit of signal level — places this program squarely in the tradition of metering and analysis tools. At conservative settings, it produces clean, functional level displays. At extreme settings — high sensitivity, fast attack, slow decay, maximum segments — it transforms the video into a pulsating grid of colored bars that respond to every flicker and flash in the source material.

---

## Background

### VU and PPM Meter Standards

The Volume Unit meter was standardized in 1939 by Bell Labs, CBS, and NBC as a way to monitor audio levels during broadcast. Its defining characteristic is a ballistic response — a 300-millisecond integration time that gives the needle a smooth, averaged reading rather than tracking every transient. The Peak Programme Meter (PPM), developed by the BBC, takes the opposite approach: fast attack (under 10 ms) captures transient peaks, while a slow decay (1.5 seconds per 20 dB) holds the reading long enough for the operator to notice. Decibel's Attack and Decay controls let you dial in anything from VU-like sluggish ballistics to PPM-like peak-catching behavior, or invent entirely new response curves.

### IIR Envelope Followers

An infinite impulse response filter maintains a running estimate of the signal level by blending the current sample with the previous estimate. When the input exceeds the estimate, the filter rises at a rate controlled by the attack coefficient; when the input drops below, the filter falls at a rate controlled by the decay coefficient. This asymmetric filtering is the heart of every audio compressor, gate, and level meter. Decibel implements this in hardware with shift-based division — the attack and decay rates select different power-of-two divisors applied to the difference between input and envelope, producing four discrete time-constant bands per parameter.

### Peak Tracking and Hold

Peak indicators serve a fundamentally different purpose from envelope followers. While the envelope shows the average energy, the peak marker catches the highest instantaneous value and holds it visible for a configurable time. In professional audio, peak hold times of one to four seconds are typical, allowing the engineer to spot brief transients that the VU meter would miss. Decibel's peak tracker latches whenever the envelope exceeds the previous peak, starts a countdown timer, and then allows the peak marker to decay slowly back toward zero once the timer expires.

### LED Bar Displays

The segmented LED bar-graph meter replaced the moving-coil VU meter in most professional equipment during the 1980s. Each LED represents a fixed level range — typically 3 dB per segment — and the display lights all segments up to the current level (bar mode) or only the single segment at the current level (dot mode). Bar mode gives a solid, easy-to-read indication; dot mode is more compact and draws less power. The hybrid "peak + bar" mode combines a solid bar for the envelope with a floating dot for the peak. Decibel's four display styles — Bar, Dot, Peak, and Fill — replicate these conventions, with Fill combining the bar and peak marker.

### Color Grading Conventions

Professional meter bridges use a universal color language: green for safe operating levels, yellow for caution, and red for clipping or overload. This convention is so deeply embedded in audio engineering culture that a glance at a meter across the room instantly communicates whether a channel is healthy. Decibel's Rainbow color mode implements this convention as a four-zone lookup — green at the bottom segments, transitioning through yellow and orange to red at the top. Green mode lights all segments in uniform green, useful when the graduated color would be distracting.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register        (latch Y + compute position)
│   ├─ 2. Sensitivity Gain      (shift-based amplification)
│   ├─ 3. IIR Envelope Follower (attack/decay smoothing)
│   ├─ 4. Peak Tracker          (latch max + timeout decay)
│   ├─ 5. Segment Quantization  (divide into 2/4/8/16 segments)
│   ├─ 6. Display Render        (bar/dot/peak/fill selector)
│   ├─ 7. Color Grading         (green or green→red gradient)
│   ├─ 8. Brightness Offset     (±512 additive adjustment)
│   └─ 9. Invert                (optional 1023 − Y complement)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   └─ Color assigned by display render (neutral gray or graded)
│
├── Wet/Dry Mix ────────────────────────────────────────────────
│   └─ 3× interpolator_u: blend processed ↔ delayed original
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline (8 clocks) pass-through
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select delayed original or mixed output
```

The critical path runs through the IIR envelope follower, which maintains state across pixels. The envelope tracks luminance continuously — it does not reset per scanline or per frame — so the meter reading is a running average of all luminance values the filter has seen. The position counter determines *where* in the meter each pixel falls: in horizontal mode, the x-coordinate maps to the segment position; in vertical mode, the y-coordinate maps instead. The display render then compares each pixel's segment index against the quantized envelope level and peak level to decide whether that pixel is lit, dark, or a peak marker.

---

## Parameter Reference

<img src={decibel_control_panel} alt="Videomancer front panel with Decibel loaded"/>
*Videomancer's front panel with Decibel active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sensitiv
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the input gain applied to the raw luminance before it enters the envelope follower. At the default midpoint, the signal passes through at unity. Below 25%, a right-shift halves the effective input, making the meter respond only to very bright sources. Above 75%, a left-shift by two quadruples the input, causing the meter to slam to full-scale on moderate signals. This is the master sensitivity of the entire metering chain — set it so that your typical source material lights about two-thirds of the bar.

---

#### Knob 2 — Segments
| Property | Value |
|----------|-------|
| Range | 2 – 32 |
| Default | 17 |

Selects the number of discrete meter segments. The VHDL implementation quantizes into four fixed tiers: 2, 4, 8, or 16 segments depending on the register value range. Fewer segments produce a coarse, chunky meter with large blocks; more segments produce a fine-grained display closer to a professional LED bar-graph. At 16 segments, each segment covers approximately 64 units of the 10-bit range, matching the precision of a typical studio meter bridge.

---

#### Knob 3 — Attack
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Sets the attack rate of the IIR envelope follower — how quickly the meter rises when the input brightens. The top two bits of the register select one of four power-of-two divisors applied to the positive difference between input and envelope: at maximum, the envelope tracks the input instantly (divisor of 1); at minimum, the envelope rises at 1/32 of the difference per sample. Fast attack catches transients; slow attack gives a smooth, averaged reading similar to a VU meter's integration behavior.

---

#### Knob 4 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the decay rate of the IIR envelope follower — how quickly the meter falls when the input dims. The same four-tier power-of-two structure as attack. Slow decay keeps the meter "hanging" at the last high reading, giving you time to observe peak levels even as the source fluctuates. Fast decay makes the bar snap back to silence immediately after a transient, creating a more responsive, jumpy display.

---

#### Knob 5 — Peak Hld
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness of the peak hold marker. The peak tracker maintains a separate level that latches at the envelope's highest value and holds there while a countdown timer runs. This control does not set the hold duration directly — it sets the luminance of the peak marker itself. At minimum, the peak dot is invisible; at maximum, it glows as a bright accent at the top of the meter, drawing the eye to where the hottest transient occurred.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies an additive brightness offset to the meter display. The offset is centered at the midpoint: values below 50% darken the entire meter overlay, values above 50% brighten it. This does not affect the unlit (background) segments — it shifts the rendered bar and peak colors. Use it to balance the meter overlay against the video when using wet/dry mix to composite the meter display over the source material.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Bar | Dot |
| **8 — Orient** | Horiz | Vert |
| **9 — Color** | Green | Rainbow |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control display style, orientation, color mode, polarity inversion, and bypass. Style and Orient are multi-value — they use two toggle bits combined to select among four options each, while Color, Invert, and Bypass are simple two-state switches.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix ratio via three interpolator instances (one per YUV channel). At 0%, the output is entirely the delayed original video — no meter visible. At 100%, the output is entirely the rendered meter — the source video is replaced. Intermediate values composite the meter over the source, allowing you to overlay a semi-transparent level display on the live video. The default is 100% (full wet) for standalone meter display.

---

## Guided Exercises

These exercises walk through Decibel's metering pipeline from basic bar displays to complex composited overlays. Each exercise reveals a different layer of the program's design.

### Exercise 1: Classic Bar Meter

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: decibel_source1_runner, after: decibel_ex1_s1 },
    { label: "Fruit", before: decibel_source2_fruit, after: decibel_ex1_s2 },
    { label: "Clouds", before: decibel_source3_clouds, after: decibel_ex1_s3 },
    { label: "Pattern", before: decibel_source4_pattern, after: decibel_ex1_s4 },
    { label: "Man", before: decibel_source5_man, after: decibel_ex1_s5 },
    { label: "Paint", before: decibel_source6_paint, after: decibel_ex1_s6 },
  ]}
/>
*Classic Bar Meter — simulated result across source images.*
**Source**: A live camera feed or test pattern with varying brightness regions — color bars or a gradient ramp are ideal.

**Objective**: Set up a basic horizontal bar meter and understand sensitivity, segment count, and attack/decay ballistics.

1. **Initialize**: Start with default settings. The meter renders as a horizontal bar.
2. **Sensitivity**: Slowly turn Sensitiv clockwise. Watch the bar extend further across the screen as the gain increases. Find the point where your source material lights roughly two-thirds of the display.
3. **Segments**: Sweep the Segments knob from minimum to maximum. Observe the meter changing from a coarse 2-segment split to a fine 16-segment bar graph.
4. **Attack**: Set Attack high (fast). Move your hand in front of the camera to create brightness changes. The bar snaps up instantly. Now set Attack low — the bar rises sluggishly, averaging out rapid transients.
5. **Decay**: Set Decay low (slow). After a bright flash, the bar hangs at the high reading before slowly descending. Set Decay high — the bar drops instantly when brightness falls.

**Key concepts**: IIR envelope follower with asymmetric attack/decay, segment quantization as visual resolution, sensitivity as input gain staging

---

### Exercise 2: Peak Hold and Rainbow Color

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: decibel_source1_runner, after: decibel_ex2_s1 },
    { label: "Fruit", before: decibel_source2_fruit, after: decibel_ex2_s2 },
    { label: "Clouds", before: decibel_source3_clouds, after: decibel_ex2_s3 },
    { label: "Pattern", before: decibel_source4_pattern, after: decibel_ex2_s4 },
    { label: "Man", before: decibel_source5_man, after: decibel_ex2_s5 },
    { label: "Paint", before: decibel_source6_paint, after: decibel_ex2_s6 },
  ]}
/>
*Peak Hold and Rainbow Color — simulated result across source images.*
**Source**: Dynamic footage with bright transients — strobes, flashing lights, or a performer moving between bright and dark areas.

**Objective**: Explore the peak tracking system and color grading, and compare display styles.

1. **Enable peak**: Switch Style to Fill (bar + peak). Set Peak Hld to about 50% so the peak marker is clearly visible.
2. **Observe transients**: Feed dynamic video. Watch the solid bar bounce with the envelope while the peak dot sticks at the highest transient, then slowly decays.
3. **Switch to Peak-only**: Change Style to Peak. Now only the floating peak marker is visible — a minimal, elegant display.
4. **Rainbow color**: Switch Color from Green to Rainbow. The segments now grade from green (low) through yellow and orange to red (high).
5. **Vertical orientation**: Switch Orient to Vert. The same meter now runs vertically — a tower-style display.
6. **Brightness**: Sweep the Bright knob to adjust the meter overlay brightness for visual clarity.

**Key concepts**: Peak tracking holds transient maxima, color grading encodes level information chromatically, orientation transforms the spatial mapping axis

---

### Exercise 3: Composited Meter Overlay

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: decibel_source1_runner, after: decibel_ex3_s1 },
    { label: "Fruit", before: decibel_source2_fruit, after: decibel_ex3_s2 },
    { label: "Clouds", before: decibel_source3_clouds, after: decibel_ex3_s3 },
    { label: "Pattern", before: decibel_source4_pattern, after: decibel_ex3_s4 },
    { label: "Man", before: decibel_source5_man, after: decibel_ex3_s5 },
    { label: "Paint", before: decibel_source6_paint, after: decibel_ex3_s6 },
  ]}
/>
*Composited Meter Overlay — simulated result across source images.*
**Source**: Visually interesting footage — a live performance, nature scene, or abstract video source.

**Objective**: Composite the meter display over the source video using wet/dry mix, creating a heads-up display (HUD) aesthetic.

1. **Set up meter**: Choose Fill style, Rainbow color, 16 segments, vertical orientation for a tower-style meter.
2. **Lower mix**: Bring the Mix fader down to about 50%. The source video becomes visible beneath the meter overlay, creating a composite.
3. **Adjust brightness**: Use the Bright control to make the meter overlay stand out against the video without washing out the source.
4. **Invert for contrast**: Try enabling Invert. The meter becomes a dark silhouette against the bright source — useful when the source is predominantly bright.
5. **Ballistics for drama**: Set Attack fast, Decay very slow. The meter bars build up and hang at peak levels, creating dramatic streaks of color that persist over the source video.
6. **Dot mode overlay**: Switch to Dot style with high mix. A single bouncing indicator traces the signal level across the source, like a spotlight tracking the brightness.

**Key concepts**: Wet/dry mix enables non-destructive overlay compositing, brightness offset balances overlay against source, invert creates negative-space meter aesthetics

---


## Tips

- **Sensitivity is your gain stage**: Set it so typical source material lights about two-thirds of the meter. If the bar is always at full scale, lower sensitivity; if the bar barely moves, raise it.
- **VU vs. PPM response**: For VU-like behavior, set Attack to ~30% and Decay to ~30%. For PPM-like behavior, set Attack to ~90% and Decay to ~10%. The difference in how the meter "feels" is dramatic.
- **Fill mode is the most informative**: It shows both the smoothed envelope (bar) and the transient peak (dot), giving you two readings in one display — just like a professional meter bridge.
- **Rainbow color is a level indicator**: Green means low, red means high. You can read the approximate level from across the room just by looking at the color of the topmost lit segment.
- **Overlay with low mix**: Setting Mix to 30–60% composites the meter over the source video, creating a heads-up display effect. Use Bright to balance the overlay against the source.
- **Vertical meters for tall compositions**: Switch Orient to Vert for a tower-style meter that complements portrait-oriented or vertically structured source material.
- **Invert for bright sources**: When the source video is predominantly bright, enabling Invert makes the meter a *dark* silhouette against the light background — often more legible than bright bars over a bright image.
- **Peak Hld as transient memory**: Even at low brightness, the peak marker acts as a visual record of the hottest signal level from the recent past.

---

## Glossary

| Term | Definition |
|------|------------|
| **Attack** | The rate at which a filter's output rises toward a new, higher input level; fast attack tracks transients, slow attack averages them out. |
| **Ballistics** | The dynamic response characteristics of a meter, defined by its attack and decay time constants. |
| **Bypass** | A signal routing option that sends the original input directly to the output, skipping all processing stages. |
| **Decay** | The rate at which a filter's output falls when the input drops below the current level; slow decay holds readings, fast decay tracks closely. |
| **Envelope Follower** | A filter that tracks the amplitude contour of a signal, smoothing out rapid fluctuations to produce a slowly varying level estimate. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **IIR** | Infinite Impulse Response; a filter type whose output depends on both the current input and previous outputs, creating memory-like behavior. |
| **Interpolator** | A hardware module that blends two values (wet and dry) according to a mix parameter, used for crossfading processed and original signals. |
| **Luma / Luminance** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Peak Hold** | A metering feature that latches the highest observed level and holds it visible for a configurable duration. |
| **PPM** | Peak Programme Meter; a broadcast metering standard with fast attack and slow decay designed to catch transient peaks. |
| **Quantization** | Mapping a continuous range of values to a smaller set of discrete levels — here, mapping the 10-bit envelope to a fixed number of segments. |
| **Segment** | One discrete step of the bar-graph meter display; the number of segments determines the visual resolution of the level reading. |
| **VU** | Volume Unit; a broadcast metering standard with 300 ms integration time, measuring average signal level rather than peaks. |
| **Wet/Dry Mix** | The ratio between processed (wet) and original (dry) signals at the output; 0% = all original, 100% = all processed. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |


---
