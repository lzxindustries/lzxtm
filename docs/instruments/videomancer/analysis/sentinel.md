---
draft: true
sidebar_position: 248
slug: /instruments/videomancer/sentinel
title: "Sentinel"
image: /img/instruments/videomancer/sentinel/sentinel_hero.png
description: "Surveillance cameras generate vast quantities of footage in which nothing happens."
---

import sentinel_hero from '/img/instruments/videomancer/sentinel/sentinel_hero.png';
import sentinel_before_after from '/img/instruments/videomancer/sentinel/sentinel_before_after.png';
import sentinel_control_panel from '/img/instruments/videomancer/sentinel/sentinel_control_panel.png';
import sentinel_exercise1_result from '/img/instruments/videomancer/sentinel/sentinel_exercise1_result.png';
import sentinel_exercise2_result from '/img/instruments/videomancer/sentinel/sentinel_exercise2_result.png';
import sentinel_exercise3_result from '/img/instruments/videomancer/sentinel/sentinel_exercise3_result.png';

# Sentinel

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={sentinel_hero} alt="Sentinel hero image"/>
*Sentinel detecting lateral pixel motion with IIR background subtraction, highlighting moving regions in false colour while dimming the static scene.*
<img src={sentinel_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Sentinel applied.*

---

## Overview

Surveillance cameras generate vast quantities of footage in which nothing happens. The real information isn't the image itself — it's the *change*. Sentinel turns that principle into a visual instrument. It builds an adaptive background model of the video signal pixel by pixel, compares each incoming sample against its own smoothed history, and classifies every pixel as either "motion" or "static." The classification drives a false-colour overlay: moving regions are highlighted in vivid green or red, while the static background is dimmed and desaturated to recede.

The name *Sentinel* evokes a watchful guardian scanning for intrusion — the same metaphor that gave "motion detection" its place in security engineering. But where a security system outputs a binary alarm, Sentinel outputs video. The threshold, adaptation rate, highlight colour, and persistence controls let you tune the detection from a hair-trigger strobe to a gentle thermal-camera glow. At extreme settings the effect inverts, revealing the static scene and hiding the movement entirely.

The entire pipeline is purely combinational and register-based — zero BRAM. A 16-bit LFSR adds noise-floor dithering to the threshold comparator, preventing false triggers on digitally flat regions where quantisation noise alone could cross a tight threshold. Persistence mode holds motion highlights with a -4 per-clock decay, creating comet-like trails behind moving objects.

---

## Background

### IIR Background Modelling

The core of Sentinel is an infinite impulse response (IIR) filter that tracks the slowly-changing background. Each pixel's luminance is compared against a running exponential average: `y_avg = y_avg + (y_in - y_avg) >> shift`. The shift value (1–9) controls the adaptation speed — small shifts respond quickly but amplify noise; large shifts create a stable background estimate but lag behind genuine scene changes. This is the same algorithm used in Stauffer-Grimson background subtraction, simplified to single-tap IIR for real-time FPGA execution.

### Difference Thresholding and Noise Dithering

Motion is declared when the absolute difference between the current pixel and the IIR average exceeds a threshold. In digital video, flat regions produce quantisation noise that hovers at ±1 LSB, which can trigger false positives at tight thresholds. Sentinel injects a pseudo-random noise floor from a 16-bit LFSR into the threshold comparison — effectively dithering the decision boundary so that a single noisy pixel doesn't oscillate between "motion" and "static" from frame to frame. The noise amplitude is user-controllable.

### False-Colour Overlay

Once motion is classified, the pipeline applies false colour to the detected regions. In green mode, luma is replaced by the Highlight parameter and chrominance is shifted toward green (U and V both pushed below mid). In red/white mode, V is pushed above mid to create a red tint. The highlight brightness is directly controlled by the user, making it possible to create subtle tinted outlines or blazing white flashes.

### Persistence and Decay

Persistence mode converts the binary motion flag into a decaying analogue trail. When a pixel transitions from motion to static, the brightness doesn't snap to the dimmed background level — instead, a persistence accumulator starts at the Highlight value and subtracts 4 counts per clock cycle, fading the overlay gradually. This creates temporal smear behind moving objects, much like the phosphor persistence of a CRT screen.

### Background Dimming and Desaturation

Pixels classified as non-motion are suppressed with a two-stage treatment. First, luminance is scaled down in four tiers (25%, 50%, 75%, or ~100%) depending on the BG Alpha parameter. Second, chrominance is pushed toward neutral by shifting U and V toward 512 with a right-shift of 2. The combined effect creates a desaturated, darkened background against which the highlighted motion regions stand out vividly — analogous to a thermal imaging palette.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Parameter Latch
│   └─ Latch Y, U, V; derive adapt_shift (1–9), threshold with sensitivity, noise amplitude, dim factor
│
├── Stage 2: IIR Difference + Threshold
│   ├─ IIR update: y_avg += (y_in − y_avg) >> adapt_shift
│   ├─ Absolute difference: |y_in − y_avg|
│   ├─ LFSR noise dither: noise = lfsr(9:0) AND noise_amp
│   └─ Motion flag: (|diff| > threshold + noise) ? 1 : 0
│
├── Stage 3: Classify + Highlight Colour
│   ├─ Invert toggle: optionally flip motion flag
│   ├─ Persistence: hold highlight brightness with −4/clk decay
│   └─ Colour select: green (U−, V−) or red/white (V+)
│
├── Stage 4: Composite Output
│   ├─ Motion pixels → highlight Y, highlight U/V
│   ├─ Persistence pixels → decaying Y, highlight U/V
│   ├─ Motion-only mode → non-motion = black (Y=0, UV=512)
│   └─ Normal mode → non-motion = dim Y (25/50/75/100%) + desat UV (>>2)
│
├── Stages 5–8: interpolator_u ×3 Wet/Dry Mix
│   └─ a=delayed dry, b=composite, t=mix_amount
│
└── Output (bypass mux)
```

Two architectural features dominate the signal path. First, the IIR average tracks the *previous pixel* horizontally — not the same pixel in a previous frame — because the FPGA has no frame buffer. Motion is therefore detected as *lateral change* along a scanline, not temporal change between frames. This makes Sentinel sensitive to horizontal edges and moving vertical boundaries. Second, the threshold comparator adds LFSR noise before the comparison, not after, which dithers the *decision* rather than the *signal*. This prevents the motion flag from chattering on flat regions without adding visible noise to the output.

---

## Parameter Reference

<img src={sentinel_control_panel} alt="Videomancer front panel with Sentinel loaded"/>
*Videomancer's front panel with Sentinel active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sensitiv
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Maps to `registers_in(0)`, the motion detection threshold in the VHDL. Higher values require a larger absolute difference between the current pixel and the IIR average before motion is declared. At 0% the detector triggers on the slightest tonal change — nearly every pixel lights up. At 100% only strong edges and high-contrast movement cross the threshold. The sensitivity knob (Pot 5) adds a scaled offset to this value, extending the effective range.

---

#### Knob 2 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Maps to `registers_in(1)`, the IIR adaptation rate. This is converted to a bit-shift amount from 1 (fastest) to 9 (slowest). At low values the IIR average chases the input rapidly, meaning only sudden changes register as motion. At high values the average lags behind gradual changes, making the detector more sensitive to slow drifts but also more prone to false positives during scene transitions.

---

#### Knob 3 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Maps to `registers_in(2)`, the highlight brightness. This sets the luminance value applied to motion-detected pixels and serves as the starting level for the persistence decay. At full value, motion regions blaze at peak white; at low values, they glow with a subtle tint. The highlight colour (green or red) is set by Toggle 7.

---

#### Knob 4 — Highlight
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Maps to `registers_in(3)`, the background dimming level. Higher values leave the non-motion background closer to its original brightness; lower values darken it more aggressively. The VHDL implements four dimming tiers: above 768 → ~100%; 512–768 → 75%; 256–512 → 50%; below 256 → 25%. This tiered approach avoids multiplier resources on the iCE40.

---

#### Knob 5 — Alert Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Maps to `registers_in(4)`, the sensitivity scaling factor. A quarter of this value is added to the threshold (Pot 1), effectively raising the detection floor. When both Sensitiv and Alert Hue are at their defaults, the combined threshold sits near the midpoint of the 10-bit range. In practice, use Sensitiv for coarse threshold setting and this control for fine-tuning the trigger level against a specific scene.

---

#### Knob 6 — BG Alpha
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Maps to `registers_in(5)`, the LFSR noise-floor amplitude. The noise value is formed by ANDing the bottom 10 bits of the LFSR with `noise_floor >> 4`, so the maximum noise amplitude is about 64 counts. At zero, the threshold comparator is deterministic — any pixel whose difference is exactly at the threshold will oscillate between motion and static. Increasing this control widens the threshold's stochastic zone, stabilising the motion mask on noisy or compressed source material.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Outline | Fill |
| **8 — Channel** | Luma | Chroma |
| **9 — Invert** | Off | On |
| **10 — Freeze BG** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–10 configure independent binary processing options. Toggle 7 selects the highlight colour palette. Toggle 8 masks non-motion pixels to black instead of dimming them. Toggle 9 inverts the motion classification so that *static* regions are highlighted. Toggle 10 enables persistence decay on the motion highlight. Toggle 11 is bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original delayed signal and the composite output. At 100% (fully wet), the motion overlay replaces the original. At 0% (fully dry), the original signal passes through unaltered. Intermediate values blend the two, creating a subtle motion-tinted overlay on top of the source — useful for monitoring applications where you want to see the original scene with motion indicated transparently.

---

## Guided Exercises

These exercises progress from basic motion detection through false-colour tuning to advanced persistence and masking techniques.

### Exercise 1: Basic Motion Detection

<img src={sentinel_exercise1_result} alt="Basic Motion Detection result"/>
*Basic Motion Detection — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a slow-moving subject against a mostly static background.

**Objective**: Learn how the threshold and adaptation rate interact to isolate motion.

1. Start with all pots at their defaults and all toggles off.
2. Slowly lower Sensitiv (Pot 1) from 50% toward 0%. Watch as more pixels cross the motion threshold and light up green.
3. Raise Decay (Pot 2) toward 80%. The IIR average now lags behind the input, making the detector more sensitive to slow movement.
4. Adjust Threshold (Pot 3) to set highlight brightness — a bright highlight is easier to see against the dimmed background.
5. Try raising BG Alpha (Pot 6) to reduce noise-floor dithering and observe the threshold instability on flat regions.

**Key concepts**: IIR adaptation rate controls the memory horizon, threshold sets the minimum detectable contrast, LFSR noise floor stabilises the binary decision on flat regions

---

### Exercise 2: False-Colour Tuning

<img src={sentinel_exercise2_result} alt="False-Colour Tuning result"/>
*False-Colour Tuning — simulated result across source images.*
**Source**: Footage with multiple moving elements at different speeds — a busy street, dancers, or waving hands.

**Objective**: Explore highlight colour modes and background dimming to create a surveillance-camera aesthetic.

1. Use settings from Exercise 1 as a baseline.
2. Toggle Mode (Switch 7) to switch between green and red/white highlights. Note how the colour palette changes the emotional tone of the image.
3. Lower Highlight (Pot 4) to create a dim background — motion pops against a nearly black scene.
4. Raise Highlight back and switch Channel (Switch 8) to motion-only mode. The background disappears and only the motion regions are visible.
5. Toggle Invert (Switch 9). The static background glows while the moving regions darken — a negative-space composition.

**Key concepts**: Green vs red colour modes change the false-colour palette, motion-only mode masks non-motion to black, inversion swaps which regions are highlighted

---

### Exercise 3: Persistence Trails

<img src={sentinel_exercise3_result} alt="Persistence Trails result"/>
*Persistence Trails — simulated result across source images.*
**Source**: A single moving object against a clean background — a swinging pendulum, a hand, or a slow pan across a contrasting edge.

**Objective**: Use persistence mode to create motion trails and explore the wet/dry mix for transparent overlay.

1. Enable Freeze BG (Toggle 10) to activate persistence.
2. Set Threshold (Pot 3) high (~80%) so that motion highlights start bright.
3. Move the subject slowly. Watch the highlight trail decay behind the moving edge with a gradual fade.
4. Lower Mix (Fader 12) to ~50%. The motion trail now overlays transparently on the original source, creating a ghostly double-exposure effect.
5. Reduce Decay (Pot 2) to ~30% for a faster IIR. The motion mask sharpens and the persistence trail shortens because the IIR catches up faster.
6. Toggle Invert (Switch 9) for inverted persistence — the static scene glows and fades only when something begins to move.

**Key concepts**: Persistence accumulator decays at 4 counts per clock, creating comet trails; wet/dry mix enables transparent overlay on the original signal; adaptation rate determines how quickly the IIR average follows the source

---


## Tips

- **Sensitiv and Alert Hue combine**: Both contribute to the effective threshold. Use Sensitiv for coarse adjustment and Alert Hue for fine-tuning against a specific scene's noise floor.
- **Noise floor prevents chatter**: Increase BG Alpha when the motion mask flickers on flat or compressed source material. A small amount of threshold dithering eliminates binary oscillation.
- **Persistence creates trails**: Enable Freeze BG to add comet-like decay behind moving objects. The trail length is fixed at −4 counts/clk, so brighter highlights produce longer trails.
- **Motion-only for keying**: Switch Channel to Chroma (motion-only) to output pure motion highlights against black — perfect for downstream compositing or keying in the signal chain.
- **Invert for negative-space compositions**: Switch 9 reveals the *static* world and hides the moving parts, creating an eerie inverted surveillance view.
- **Mix for transparent overlay**: Lower the Mix fader to blend the motion overlay transparently on top of the original signal, creating a heads-up-display monitoring effect.
- **Dim factor tiers**: The background dimming is stepped (25/50/75/100%), not smooth. This is a deliberate resource-saving design on the iCE40 — choose the tier that balances legibility against contrast.

---

## Glossary

| Term | Definition |
|------|------------|
| **Background Subtraction** | An image analysis technique that separates foreground (motion) from background (static) by maintaining and comparing against a reference model. |
| **BRAM** | Block RAM; dedicated memory in the FPGA fabric. Sentinel uses zero BRAM; all state is register-based. |
| **Chroma** | The colour components (U, V) of a YUV signal, representing hue and saturation. |
| **Desaturation** | Reducing chrominance toward neutral (U=512, V=512), making the image appear greyscale. |
| **False Colour** | A visualisation technique that maps data values to an arbitrary colour palette for enhanced visibility. |
| **IIR** | Infinite Impulse Response; a recursive filter whose output depends on its own previous values, creating exponential smoothing. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used for noise-floor dithering. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Persistence** | Temporal smearing created by decaying a highlight value gradually rather than snapping it off. |
| **Pipeline** | Sequential processing stages where each stage's output feeds the next on every clock cycle. |
| **Threshold** | The minimum absolute difference required to classify a pixel as "motion." |
| **YUV** | A colour encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
