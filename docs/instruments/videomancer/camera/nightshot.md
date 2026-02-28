---
draft: true
sidebar_position: 179
slug: /instruments/videomancer/nightshot
title: "Nightshot"
image: /img/instruments/videomancer/nightshot/nightshot_hero.png
description: "Program guide for Nightshot, a Videomancer camera program for the LZX video synthesizer."
---

import nightshot_before_after from '/img/instruments/videomancer/nightshot/nightshot_before_after.png';
import nightshot_control_panel from '/img/instruments/videomancer/nightshot/nightshot_control_panel.png';
import nightshot_exercise1_result from '/img/instruments/videomancer/nightshot/nightshot_exercise1_result.png';
import nightshot_exercise2_result from '/img/instruments/videomancer/nightshot/nightshot_exercise2_result.png';
import nightshot_exercise3_result from '/img/instruments/videomancer/nightshot/nightshot_exercise3_result.png';
import nightshot_hero from '/img/instruments/videomancer/nightshot/nightshot_hero.png';
import nightshot_source1_kodim05 from '/img/instruments/videomancer/nightshot/nightshot_source1_kodim05.png';
import nightshot_source2_kodim15 from '/img/instruments/videomancer/nightshot/nightshot_source2_kodim15.png';
import nightshot_source3_kodim15_bw from '/img/instruments/videomancer/nightshot/nightshot_source3_kodim15_bw.png';

# Nightshot

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={nightshot_hero} alt="Nightshot hero image"/>
*Nightshot rendering infrared-style green phosphor night vision with gain boost, noise grain, horizontal bloom, and auto-gain pumping across the video signal.*
<img src={nightshot_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Nightshot applied.*

---

## Overview

In 1998, Sony introduced NightShot on the Handycam DCR-TRV103 — a mode that disabled the infrared cut filter and boosted CCD gain, producing the distinctive green-tinted night vision imagery that became a cultural icon of late-90s camcorder footage. Nightshot recreates this aesthetic digitally. It strips chrominance, applies massive luma gain with a non-linear IR response curve, injects LFSR-generated noise to simulate high-ISO grain, adds horizontal IIR bloom for CCD charge smear, maps the monochrome result to green phosphor or gray, and optionally overlays a center crosshair.

The program's name references the Sony NightShot feature directly. The Super NightShot variant added infrared LED illumination for total darkness — the "IR Gain" and "IR Curve" controls simulate this extended sensitivity by lifting shadows and compressing highlights, replicating the CCD response to infrared illumination where dark areas become visible but bright areas clip. An auto-gain pump oscillator creates periodic gain fluctuations that mimic the AGC (Automatic Gain Control) hunting visible in real low-light camcorder footage.

All processing is purely per-pixel with zero BRAM usage. The LFSR16 generates pseudo-random noise. The IIR bloom is a single horizontal accumulator that tracks the maximum of input and decayed previous value, creating rightward charge smear from bright pixels. The entire chain runs in 8 clocks: 4 processing stages plus a 4-clock interpolator mix.

---

## Background

### CCD Gain and Infrared Response

Consumer CCD sensors have a cut filter that blocks infrared wavelengths above ~700 nm. Removing this filter (as NightShot does) lets IR light reach the sensor, dramatically increasing sensitivity in dark scenes. The CCD's IR response is non-linear: it lifts shadows strongly (because dark current and ambient IR contribute proportionally more in shadows) while highlights compress as the sensor wells approach saturation. Nightshot models this with a two-stage gain: a linear boost (IR Gain) followed by a shadow-lifting curve (IR Curve) that adds a fraction of the inverted luma back to itself.

### LFSR Noise Generation

A 16-bit Linear Feedback Shift Register produces pseudo-random values by XORing taps at positions 15, 14, 12, and 3, then shifting the result. This creates a maximal-length sequence of 65535 values before repeating. The bottom 10 bits are scaled by the Noise pot and added to the luma signal with a DC offset subtraction (noise/4) to keep the noise centered around zero rather than biasing the image brighter. The noise amplitude scales with the Noise parameter, simulating how real CCD noise increases with gain.

### Horizontal IIR Bloom

CCD charge smear occurs when bright pixels overflow their potential wells and bleed charge into adjacent cells along the readout register — always horizontally. Nightshot simulates this with a per-scanline IIR accumulator: each pixel, the accumulator is set to max(input_luma, acc × bloom / 1024). This "sticky maximum" creates a rightward trailing bloom from any bright feature. The bloom signal is then mixed back into the luma additively, scaled by bloom/4. The accumulator resets at each hsync, preventing inter-line bleed.

### Auto-Gain Pumping

Consumer camcorder AGC (Automatic Gain Control) circuits adjust gain to maintain a target average brightness. In low-light scenes, the AGC hunts — oscillating the gain up and down as it chases a target it can never quite reach. Nightshot models this with a triangle-wave oscillator driven by a 16-bit accumulator. Each frame (at vsync), the accumulator increments or decrements by the Pump Rate value, reversing direction at upper (60000) and lower (5000) bounds. The resulting triangle wave is scaled by Pump Depth and added to the IR Gain, creating periodic brightness pulsing.

### Green Phosphor Color Mapping

Classic night vision devices display their amplified image on a phosphor screen tinted green (P43 phosphor), chosen because the human eye has maximum sensitivity to green wavelengths. Nightshot maps the monochrome luma to green by interpolating the U and V channels from the neutral midpoint (512, 512) toward fixed green values (U=350, V=160) proportionally to the pixel brightness. Brighter pixels receive stronger green tint. In Gray mode, U and V remain at 512 for pure monochrome output.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── State ─────────────────────────────────────────────────────
│   ├─ H/V position counters  (hsync/vsync edge detect)
│   ├─ LFSR16 advance         (every clock cycle)
│   └─ Auto-gain pump         (triangle wave, updated per vsync)
│
├── Processing Pipeline ───────────────────────────────────────
│   │
│   ├─ 1. Luma Extract + Gain  (Y × (1 + ir_gain/2 + pump_value))
│   │                           Clamp to 1023
│   ├─ 2. IR Response Curve     (Y + (1023−Y) × ir_curve / 4 / 1024)
│   │     Invert                (if enabled: 1023 − Y)
│   ├─ 3. Noise Injection       (Y + lfsr×noise/1024/2 − noise/4)
│   │                           Clamp 0–1023
│   ├─ 4. Bloom IIR             (acc = max(Y, acc×bloom/1024))
│   │     Additive merge        (Y + acc × bloom/4 / 1024)
│   │     Hot Spots             (if Y>768: Y + (Y−768)/2)
│   ├─ 5. Color Map             (green: U→350, V→160 scaled by Y)
│   │                           (gray: U=V=512)
│   │     Crosshair Overlay     (white cross at frame center)
│   └─ 6–9. Interpolator Mix    (4 clocks, dry/wet crossfade)
│
├── Sync Signals ──────────────────────────────────────────────
│   └─ 8-stage delay pipeline (hsync, vsync, field, Y/U/V)
│
└── Output ────────────────────────────────────────────────────
    └─ Mixed Y/U/V (no bypass toggle — mix at 0 serves as bypass)
```

The processing chain is strictly per-pixel with no line buffers. The IIR bloom accumulator is the only inter-pixel state, and it resets at each hsync, so there is no vertical or frame-to-frame memory in the bloom path. The auto-gain pump, by contrast, does have frame-to-frame memory — its triangle-wave accumulator persists across frames, creating the slow periodic gain oscillation.

The invert operation is applied after the IR response curve but before noise injection. This means inverted output still receives noise and bloom, creating a negative-image night vision look where dark areas become bright and noisy. The crosshair overlay is applied last (after color mapping), drawing white lines regardless of the green/gray mode selection.

---

## Parameter Reference

<img src={nightshot_control_panel} alt="Videomancer front panel with Nightshot loaded"/>
*Videomancer's front panel with Nightshot active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — IR Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

IR Gain controls the luma amplification factor. The gain value (plus any auto-gain pump contribution) is halved and added to 1.0, then multiplied by the input luma: output = Y × (1 + gain/2). At minimum (0), the image passes at unity gain. At maximum (1023), the effective multiplier exceeds 512×, massively boosting dark scenes but clipping highlights. This is the primary "night vision sensitivity" control — higher values reveal more shadow detail at the cost of increased noise visibility and highlight saturation.

---

#### Knob 2 — Noise
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Noise controls the amplitude of the LFSR16-generated pseudo-random noise added to the luma channel. The LFSR output is scaled by the noise pot value (noise × lfsr / 1024) and added with a DC offset subtraction (noise/4) to center the noise around zero. At zero, the image is clean. At maximum, heavy grain covers the entire image, simulating the high-ISO CCD noise characteristic of real NightShot footage. The noise is frame-unique because the LFSR advances every clock cycle.

---

#### Knob 3 — Bloom
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Bloom controls the horizontal IIR charge-smear simulation. The accumulator decay factor is bloom/1024 — at high values, bright pixels trail far to the right before decaying. The bloom signal is then mixed back into the luma at bloom/4 strength. At zero, no bloom is applied. At maximum, bright features produce long horizontal streaks that gradually fade, closely mimicking CCD well overflow in overdriven camera sensors.

---

#### Knob 4 — Pump Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Pump Rate sets the speed of the auto-gain triangle-wave oscillator. The pot value is added to (or subtracted from) a 16-bit accumulator each frame. Higher values cause faster oscillation between the gain bounds, creating rapid brightness pulsing. Lower values produce slow, breathing-like gain variations. This parameter has no effect when Auto Gain is toggled off.

---

#### Knob 5 — Pump Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Pump Depth scales the triangle-wave amplitude before it is added to the IR Gain. The accumulator's top 10 bits are multiplied by the depth pot value, so higher depth creates wider gain swings. At zero depth, the pump oscillator runs but produces no visible effect. At maximum, the gain oscillates dramatically, creating the aggressive AGC hunting visible in very dark NightShot footage.

---

#### Knob 6 — IR Curve
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

IR Curve controls the shape of the non-linear IR response. The curve adds (1023 − luma) × ir_curve / 4 / 1024 back to the luma — effectively lifting shadows proportionally more than highlights. At zero, the response is linear (gain only). At maximum, dark areas are strongly lifted toward mid-gray while highlights remain near clipping, compressing the dynamic range in a way that mimics infrared CCD response characteristics.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color Mode** | Green | Gray |
| **8 — Hot Spots** | Off | On |
| **9 — Auto Gain** | Off | On |
| **10 — Crosshair** | Off | On |
| **11 — Invert** | Off | On |

The five toggles control independent rendering options. Color Mode selects between green phosphor tint and pure gray monochrome. Hot Spots adds highlight emphasis. Auto Gain enables the pump oscillator. Crosshair overlays targeting lines. Invert flips luma polarity. There is no bypass toggle — setting the Mix fader to 0% serves as an effective bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix controls the interpolator crossfade between the dry (original) and wet (processed) signals. At 0, the output is entirely the original video. At 1023, the output is the full night vision effect. Because Nightshot has no bypass toggle, setting Mix to 0 is the only way to pass the original signal through cleanly. The interpolator operates independently on Y, U, and V with 4-clock latency.

---

## Guided Exercises

These exercises build the NightShot aesthetic from basic green monochrome through noisy gain-boosted night vision to full AGC simulation with bloom and hot spots.

### Exercise 1: Basic Green Night Vision

<img src={nightshot_exercise1_result} alt="Basic Green Night Vision result"/>
*Basic Green Night Vision — simulated result across source images.*
**Source**: A moderately lit camera feed — indoor scene, face, or room with visible shadow areas.

**Objective**: Create the classic green phosphor NightShot look with moderate gain boost and minimal noise.

1. Start with defaults. Observe the green-tinted monochrome image.
2. Increase IR Gain to ~60%. Shadow areas brighten significantly.
3. Set Noise to ~20% for subtle grain texture.
4. Observe how the green tint intensifies on brighter areas and fades toward gray in shadows.
5. Toggle Color Mode to Gray — the image becomes pure monochrome. Toggle back to Green.
6. Sweep IR Curve from 0% to ~50%. Watch shadows lift further while highlights remain compressed.

**Key concepts**: Green phosphor mapping scales with pixel brightness, IR gain is multiplicative, IR curve lifts shadows non-linearly

---

### Exercise 2: Noisy Surveillance with Bloom

<img src={nightshot_exercise2_result} alt="Noisy Surveillance with Bloom result"/>
*Noisy Surveillance with Bloom — simulated result across source images.*
**Source**: A dark scene — dimly lit hallway, nighttime exterior, or underexposed footage.

**Objective**: Push the gain hard to reveal detail in a dark source, adding noise and bloom for authentic low-light camcorder artifacts.

1. Set IR Gain to ~85% to dramatically boost the dark scene.
2. Increase Noise to ~60%. Heavy grain appears, simulating high-ISO CCD noise.
3. Set Bloom to ~50%. Bright features (lights, reflections) develop rightward horizontal streaks.
4. Enable Hot Spots. Any bright pixel above 768 flares further, creating overexposed highlights.
5. Increase IR Curve to ~60%. Remaining shadow detail is lifted, but highlights clip hard.
6. Switch Color Mode to Gray for a CCTV surveillance aesthetic.

**Key concepts**: Gain + noise scales together (noise becomes more visible at higher gain), bloom simulates CCD charge smear, hot spots emphasize IR-reflective surfaces

---

### Exercise 3: Full NightShot with AGC Hunting

<img src={nightshot_exercise3_result} alt="Full NightShot with AGC Hunting result"/>
*Full NightShot with AGC Hunting — simulated result across source images.*
**Source**: A moving subject in mixed lighting — hand-held camera footage, a person walking through light and shadow.

**Objective**: Engage the auto-gain pump to create the distinctive AGC hunting visible in real late-90s NightShot footage.

1. Set IR Gain to ~50% as a baseline.
2. Enable Auto Gain. Set Pump Rate to ~25% for slow oscillation.
3. Set Pump Depth to ~40%. Observe the brightness gradually pulsing up and down.
4. Increase Pump Rate to ~60%. The pulsing accelerates.
5. Add Noise at ~40% and Bloom at ~30% for full authenticity.
6. Enable Crosshair. A white targeting cross appears at frame center.
7. Enable Hot Spots. Observe how bright areas flare during the gain peaks.

**Key concepts**: Triangle-wave pump oscillator creates periodic gain variation, pump depth scales the oscillation amplitude, crosshair overlay is independent of color mode

---


## Tips

- **Start with IR Gain before adding noise**: Noise visibility scales with gain — adding noise before finding the right gain level makes it hard to judge the base sensitivity.
- **Use IR Curve to recover shadow detail**: The curve lifts shadows without further boosting already-bright areas. Combine moderate gain with high curve for the most natural NightShot look.
- **Bloom is directional**: The IIR accumulator runs left-to-right only, so bloom trails always extend to the right. Position light sources on the left side of frame for the most visible charge smear.
- **Pump Rate and Depth work together**: Rate controls speed, depth controls amplitude. Fast rate with low depth creates subtle flickering; slow rate with high depth creates dramatic breathing.
- **Hot Spots emphasize skin and eyes**: In real NightShot footage, skin and eyes appear as bright hotspots due to IR reflectivity. The hot spot boost above 768 recreates this effect on any bright feature.
- **Green mode tint scales with brightness**: Dark pixels remain nearly neutral, so the green tint is most visible on mid-tones and highlights. For uniform green across all levels, boost IR Gain to push everything brighter.
- **Crosshair is always white**: The crosshair overlay forces Y=1023 and neutral UV, cutting through the green tint. It is drawn after all color mapping.
- **No bypass toggle exists**: Use Mix at 0% for clean passthrough. This is the only program feature that differs from the standard Videomancer toggle layout.

---

## Glossary

| Term | Definition |
|------|------------|
| **AGC** | Automatic Gain Control; a feedback circuit in cameras that adjusts amplification to maintain target brightness, often causing visible gain hunting in low light. |
| **Bloom** | Horizontal brightness smear caused by CCD charge well overflow bleeding along the readout register. |
| **BT.601** | ITU-R BT.601 standard defining the YUV color encoding used in the Videomancer video pipeline. |
| **CCD** | Charge-Coupled Device; the image sensor technology used in late-1990s camcorders. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip executing the video processing pipeline at 74.25 MHz. |
| **IIR** | Infinite Impulse Response; a feedback filter whose output depends on its own previous output. |
| **Interpolator** | A linear crossfade module that blends two 10-bit values based on a mix parameter over 4 clock cycles. |
| **IR** | Infrared; electromagnetic radiation with wavelength longer than visible red light (~700 nm+). |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input is a linear function (XOR) of selected bit positions, producing a pseudo-random sequence. |
| **Luminance** | The brightness component (Y) of a YUV signal, range 0–1023 in 10-bit representation. |
| **NightShot** | Sony Handycam feature (1998+) that disabled the IR cut filter and boosted CCD gain for night recording. |
| **P43** | Green phosphor compound used in image intensifier tubes and night vision devices. |
| **Pipeline** | Sequential processing stages where each stage's output feeds the next on every clock cycle. |
| **Triangle Wave** | A periodic waveform that linearly ramps up and down between bounds, used here for the AGC pump oscillator. |
| **YUV** | Color encoding separating luminance (Y) from chrominance (U, V), the native format of the Videomancer video pipeline. |
