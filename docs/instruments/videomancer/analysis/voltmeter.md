---
draft: true
sidebar_position: 282
slug: /instruments/videomancer/voltmeter
title: "Voltmeter"
image: /img/instruments/videomancer/voltmeter/voltmeter_hero.png
description: "Before digital meters conquered the audio world, every studio console featured a row of illuminated VU meters — those satisfying semicircular gauges wit..."
---

import voltmeter_before_after from '/img/instruments/videomancer/voltmeter/voltmeter_before_after.png';
import voltmeter_control_panel from '/img/instruments/videomancer/voltmeter/voltmeter_control_panel.png';
import voltmeter_exercise1_result from '/img/instruments/videomancer/voltmeter/voltmeter_exercise1_result.png';
import voltmeter_exercise2_result from '/img/instruments/videomancer/voltmeter/voltmeter_exercise2_result.png';
import voltmeter_exercise3_result from '/img/instruments/videomancer/voltmeter/voltmeter_exercise3_result.png';
import voltmeter_hero from '/img/instruments/videomancer/voltmeter/voltmeter_hero.png';
import voltmeter_source1_grayscale_ramp_h_1920x1080 from '/img/instruments/videomancer/voltmeter/voltmeter_source1_grayscale_ramp_h_1920x1080.png';
import voltmeter_source2_grayscale_ramp_v_1920x1080 from '/img/instruments/videomancer/voltmeter/voltmeter_source2_grayscale_ramp_v_1920x1080.png';
import voltmeter_source3_step_wedge_21level_512 from '/img/instruments/videomancer/voltmeter/voltmeter_source3_step_wedge_21level_512.png';

# Voltmeter

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={voltmeter_hero} alt="Voltmeter hero image"/>
*Voltmeter projecting an analog VU gauge over a live video feed, the needle tracking average frame luminance in real time.*
<img src={voltmeter_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Voltmeter applied.*

---

## Overview

Before digital meters conquered the audio world, every studio console featured a row of illuminated VU meters — those satisfying semicircular gauges with swinging needles that danced to the music. Voltmeter brings that same analog metering aesthetic into the video domain. Instead of measuring audio levels, it measures the average brightness of the incoming video frame and displays the result as a graphical gauge overlay composited onto the live image.

The name *Voltmeter* nods to the original electrical measurement instruments from which VU meters descended. The program implements a leaky integrator that accumulates luminance values across each frame, producing a running average brightness reading. This average drives a needle whose horizontal position sweeps across a semicircular arc drawn with Manhattan distance approximation. Tick marks at regular angular intervals provide a graduated scale, and the entire gauge — arc, ticks, and needle — is rendered as an additive overlay with configurable brightness and optional color tinting.

At low damping settings the needle responds rapidly, jumping with every scene change. At high damping the needle drifts slowly, tracking long-term brightness trends like a thermal meter. The peak hold mode retains the maximum reading as a secondary indicator with slow decay, giving the classic "peak plus average" display familiar from professional audio hardware.

---

## Background

### VU Meters and Analog Instrumentation

The Volume Unit meter was standardized in 1939 by a joint committee of Bell Telephone Laboratories, CBS, and NBC. Its defining characteristic was a specific ballistic response — a 300-millisecond rise time to 99% of a sustained signal — achieved through the mechanical inertia of its D'Arsonval galvanometer movement. This deliberate sluggishness was a feature, not a bug: it produced readings that correlated well with perceived loudness. Voltmeter's leaky integrator serves the same purpose, providing a damped response that tracks the subjective impression of overall image brightness rather than instantaneous pixel values.

### Leaky Integrators in Signal Processing

A leaky integrator (also called an exponential moving average or first-order IIR low-pass filter) is the simplest useful averaging filter. The update rule is: accumulator = accumulator + (input - accumulator) >> shift. The shift amount controls the time constant — larger shifts produce slower, smoother response. Voltmeter implements this with a 20-bit accumulator, where the upper 10 bits represent the average luma. The shift of 3–12 (selected by the Damping knob) provides time constants ranging from a few frames to several seconds at 60 fps.

### Manhattan Distance Rendering

Drawing a perfect circle on an integer grid requires evaluating sqrt(dx² + dy²), which is expensive in hardware. Voltmeter instead uses the Manhattan-octagonal approximation: distance ≈ max(|dx|, |dy|) + min(|dx|, |dy|) / 4. This produces an octagonal shape that approximates a circle within about 8% error — close enough for a gauge arc that needs to look round on a low-resolution overlay. The arc, needle, and tick tests are all simple integer comparisons requiring no multiplication.

### Peak Hold Metering

Professional audio meters often display two simultaneous readings: the average level (the moving needle) and the peak level (a held indicator that captures transient spikes). The peak indicator rises instantly to the highest value and then decays slowly — typically 1–3 dB per second. Voltmeter implements this by maintaining a separate peak register that tracks the maximum of the average luma, decrementing by 1 per frame when the current average falls below the peak. This gives a decay rate proportional to frame rate, providing a visual history of brightness peaks.

### Additive Overlay Compositing

The gauge graphics are rendered additively — the overlay brightness is added to the underlying video rather than replacing it. This means the gauge is always visible regardless of the underlying content, appearing as a bright line over dark areas and a glowing highlight over bright areas. The technique mirrors how oscilloscope and CRT vector displays work: the electron beam simply adds light to whatever is already on the phosphor.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Luma Accumulation ──────────────────────────────────────────
│   └─ Leaky integrator IIR        (20-bit acc, shift by Damping)
│      └─ Average luma              (upper 10 bits of accumulator)
│         └─ Peak hold register     (max tracking with slow decay)
│
├── Gauge Geometry ─────────────────────────────────────────────
│   ├─ 1. dx/dy from gauge center   (Position toggle selects cy)
│   ├─ 2. Manhattan arc distance    (max + min/4 vs radius)
│   ├─ 3. Needle position test      (hcount near needle_h)
│   └─ 4. Tick mark test            (dx_abs mod tick_spacing == 0)
│
├── Overlay Composite ──────────────────────────────────────────
│   ├─ 5. Needle brightness         (full bright_reg)
│   ├─ 6. Arc brightness            (bright_reg / 2)
│   ├─ 7. Tick brightness           (bright_reg / 4)
│   └─ 8. Additive blend + color    (white or amber/red tint)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ Interpolator × 3             (wet/dry crossfade per channel)
│
└── Sync Signals ───────────────────────────────────────────────
    └─ 8-clock delay pipeline        (hsync, vsync, field)
```

The luma accumulator runs continuously during active video, updating the 20-bit IIR register on every pixel. At vsync the accumulator's upper 10 bits are sampled as the average luma, and the needle position is computed as a horizontal screen coordinate mapped from the luma value scaled by the Scale Range parameter. The peak hold register updates simultaneously, capturing the maximum and decaying by 1 per frame when the current average drops.

The gauge rendering pipeline operates on a pixel-by-pixel basis in stages 1–4. Each pixel computes its distance from the gauge center and checks three conditions: arc membership (within 3 pixels of the radius), needle proximity (within 2 pixels horizontally and inside the arc), and tick alignment (horizontal position is a multiple of the tick spacing). The brightest matching element wins, and its brightness is added to the input luma. The Arc Color toggle optionally tints the overlay amber/red for the needle and a subtler orange-amber for the arc and ticks.

---

## Parameter Reference

<img src={voltmeter_control_panel} alt="Videomancer front panel with Voltmeter loaded"/>
*Videomancer's front panel with Voltmeter active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Position
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Position controls where the gauge appears on screen. The VHDL maps this parameter to gauge size (radius), setting the overall diameter of the semicircular arc. At minimum the gauge is a small indicator; at maximum it spans almost the full screen width. The gauge center is locked to mid-screen horizontally, with the vertical position selected by the Style toggle between bottom-of-frame (classic VU) and screen center.

---

#### Knob 2 — Damping
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Damping sets the time constant of the leaky integrator that averages the input luma. Low damping makes the needle responsive and jumpy, reacting to every scene cut and flash. High damping produces a slow, deliberate sweep that tracks long-term brightness trends. The implementation uses a shift-based IIR filter where the shift amount ranges from 3 (fast, ~8 frame averaging) to 12 (very slow, ~4000 frame averaging). Mid-range settings around 50% provide a natural, visually satisfying needle motion.

---

#### Knob 3 — Scale Rng
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scale Range sets the sweep extent of the needle across the gauge arc. At low values the needle barely moves, covering a narrow arc even with large brightness changes. At high values the full arc is utilized, mapping the entire 0–1023 luma range across the visible sweep. This is analogous to the sensitivity or range selector on a physical multimeter — you adjust it to match the dynamic range of your input signal.

---

#### Knob 4 — Arc Rad
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Arc Radius controls the brightness of the needle itself, which is the most prominent element of the gauge overlay. At low settings the needle is a subtle ghost over the video; at maximum it blazes white (or bright red/amber when color tinting is enabled). The needle receives the full brightness value while the arc and tick marks receive half and quarter brightness respectively, maintaining a natural visual hierarchy.

---

#### Knob 5 — Tick Den
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Tick Density sets the angular spacing of the scale markings around the gauge arc. At low density only a few widely-spaced tick marks appear, creating a clean minimalist look. At high density the arc is crowded with fine graduations like a precision instrument. The spacing is implemented as a power-of-two modulus test on the horizontal pixel distance from the gauge center, so tick positions jump in discrete steps as you sweep the knob.

---

#### Knob 6 — Needle Br
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Needle Brightness provides a secondary brightness control. In the VHDL implementation this register is unused (the needle brightness comes from Pot 4), so adjusting this parameter has no visible effect. It is reserved for future firmware revisions that may add additional gauge rendering features or a secondary brightness layer.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | VU | Ampmeter |
| **8 — Needle** | Thin | Wide |
| **9 — Peak** | Off | Hold |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into three functional groups: gauge appearance (Style and Needle), behavior modifiers (Peak and Animate), and signal routing (Bypass). Style and Needle configure the visual rendering, Peak enables the secondary peak indicator, Animate activates a test sweep for setup purposes, and Bypass routes the input directly to the output for A/B comparison. In the VHDL implementation, the toggle bit assignments differ from the TOML labels — the hardware uses Style (bit 0) for VU/peak hold, Position (bit 1) for gauge placement, and Arc Color (bit 2) for tinting.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the dry input signal and the wet gauge-overlaid output. At 0% the output is pure dry input with no gauge visible. At 100% the output shows the full gauge overlay at the brightness set by the Needle Brightness control. Intermediate settings produce a subtle, partially-transparent gauge overlay. The crossfade is implemented by three interpolator_u instances operating independently on Y, U, and V channels with 4-clock latency each.

---

## Guided Exercises

These exercises explore Voltmeter's metering capabilities, from basic brightness monitoring through peak detection and creative overlay effects.

### Exercise 1: Studio Brightness Monitor

<img src={voltmeter_exercise1_result} alt="Studio Brightness Monitor result"/>
*Studio Brightness Monitor — simulated result across source images.*
**Source**: Feed a camera signal or dynamic video clip with varying scene brightness — ideally content with distinct bright and dark scenes.

**Objective**: Set up Voltmeter as a functional brightness monitor with natural needle motion and clear scale markings.

1. Set Position to 50% for a medium-sized gauge
2. Set Damping to 40% for responsive but smooth needle motion
3. Set Scale Range to 75% for good deflection range
4. Flip Style to VU mode for continuous tracking
5. Observe the needle tracking scene brightness in real time
6. Increase Damping to 80% and notice the slower, more deliberate response

**Key concepts**: The leaky integrator averaging, IIR time constants, and the relationship between damping and perceived responsiveness.

---

### Exercise 2: Peak Detection Display

<img src={voltmeter_exercise2_result} alt="Peak Detection Display result"/>
*Peak Detection Display — simulated result across source images.*
**Source**: Feed a music video or content with dramatic flash cuts and sudden brightness changes — ideal for triggering peak holds.

**Objective**: Configure peak hold metering to capture brightness transients and observe the slow decay behavior.

1. Start from Exercise 1 settings
2. Flip Style to Peak Hold mode (toggle position 2)
3. Set Damping to 20% for fast peak capture
4. Set Scale Range to 90% for maximum deflection
5. Watch the needle jump to brightness peaks and slowly decay
6. Toggle Peak (toggle 9) to the amber color scheme for classic VU aesthetics
7. Compare peak behavior across different content — steady footage vs. strobe-like cuts

**Key concepts**: Peak hold metering, transient capture, decay rates, and the visual distinction between average and peak readings.

---

### Exercise 3: Full-Screen Overlay Art

<img src={voltmeter_exercise3_result} alt="Full-Screen Overlay Art result"/>
*Full-Screen Overlay Art — simulated result across source images.*
**Source**: Feed abstract or geometric video content — color bars, gradients, or generative patterns work well.

**Objective**: Use Voltmeter as a creative overlay element, making the gauge itself a dominant visual component rather than just an indicator.

1. Set Position to 100% for maximum gauge size
2. Set Scale Range to maximum for full sweep
3. Set Arc Radius to maximum brightness
4. Set Tick Density to maximum for dense graduations
5. Flip Needle (toggle 8) to center-screen position
6. Flip Peak (toggle 9) to amber/red coloring
7. Set Damping to 60% for smooth, cinematic needle motion
8. Set Mix to 70% and observe the gauge as a semi-transparent HUD element

**Key concepts**: Using analysis programs as creative visual elements, additive overlay blending, and the aesthetic quality of analog instrumentation graphics.

---


## Tips

- **Use low damping for live monitoring** — settings around 20-30% give responsive needle motion that tracks scene changes without excessive jitter.
- **Peak hold reveals transients** — enable peak mode when looking for unexpected brightness spikes that the average-tracking needle might miss.
- **Center position for HUD effects** — placing the gauge mid-screen creates a compelling heads-up display aesthetic for live performance visuals.
- **Amber coloring adds warmth** — the red/amber tint option gives the gauge a classic VU meter look that blends well with warm-toned video content.
- **Maximum tick density for precision** — dense graduations help identify small brightness differences when using Voltmeter as a serious analysis tool.
- **Mix as fade control** — rather than using bypass, gradually reducing the Mix fader lets you preview the gauge at various opacity levels.
- **Pair with high-contrast sources** — Voltmeter is most dramatic when the input has a wide dynamic range, causing the needle to sweep through a large arc.
- **Bypass for instant comparison** — toggle bypass on and off rapidly to compare the overlaid and clean versions without touching any other settings.
