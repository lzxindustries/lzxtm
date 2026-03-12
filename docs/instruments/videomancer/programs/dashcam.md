---
draft: true
sidebar_position: 75
slug: /instruments/videomancer/dashcam
title: "Dashcam"
image: /img/instruments/videomancer/dashcam/dashcam_hero_s1.png
description: "Dashcam emulates the look of footage recorded by a low-cost dashboard-mounted camera."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import dashcam_control_panel from '/img/instruments/videomancer/dashcam/dashcam_control_panel.png';
import dashcam_source1_boat from '/img/instruments/videomancer/dashcam/dashcam_source1_boat.png';
import dashcam_source2_dog from '/img/instruments/videomancer/dashcam/dashcam_source2_dog.png';
import dashcam_source3_turtle from '/img/instruments/videomancer/dashcam/dashcam_source3_turtle.png';
import dashcam_source4_pattern from '/img/instruments/videomancer/dashcam/dashcam_source4_pattern.png';
import dashcam_source5_man from '/img/instruments/videomancer/dashcam/dashcam_source5_man.png';
import dashcam_source6_paint from '/img/instruments/videomancer/dashcam/dashcam_source6_paint.png';
import dashcam_hero_s1 from '/img/instruments/videomancer/dashcam/dashcam_hero_s1.png';
import dashcam_hero_s2 from '/img/instruments/videomancer/dashcam/dashcam_hero_s2.png';
import dashcam_hero_s3 from '/img/instruments/videomancer/dashcam/dashcam_hero_s3.png';
import dashcam_hero_s4 from '/img/instruments/videomancer/dashcam/dashcam_hero_s4.png';
import dashcam_hero_s5 from '/img/instruments/videomancer/dashcam/dashcam_hero_s5.png';
import dashcam_hero_s6 from '/img/instruments/videomancer/dashcam/dashcam_hero_s6.png';
import dashcam_ex1_s1 from '/img/instruments/videomancer/dashcam/dashcam_ex1_s1.png';
import dashcam_ex1_s2 from '/img/instruments/videomancer/dashcam/dashcam_ex1_s2.png';
import dashcam_ex1_s3 from '/img/instruments/videomancer/dashcam/dashcam_ex1_s3.png';
import dashcam_ex1_s4 from '/img/instruments/videomancer/dashcam/dashcam_ex1_s4.png';
import dashcam_ex1_s5 from '/img/instruments/videomancer/dashcam/dashcam_ex1_s5.png';
import dashcam_ex1_s6 from '/img/instruments/videomancer/dashcam/dashcam_ex1_s6.png';
import dashcam_ex2_s1 from '/img/instruments/videomancer/dashcam/dashcam_ex2_s1.png';
import dashcam_ex2_s2 from '/img/instruments/videomancer/dashcam/dashcam_ex2_s2.png';
import dashcam_ex2_s3 from '/img/instruments/videomancer/dashcam/dashcam_ex2_s3.png';
import dashcam_ex2_s4 from '/img/instruments/videomancer/dashcam/dashcam_ex2_s4.png';
import dashcam_ex2_s5 from '/img/instruments/videomancer/dashcam/dashcam_ex2_s5.png';
import dashcam_ex2_s6 from '/img/instruments/videomancer/dashcam/dashcam_ex2_s6.png';
import dashcam_ex3_s1 from '/img/instruments/videomancer/dashcam/dashcam_ex3_s1.png';
import dashcam_ex3_s2 from '/img/instruments/videomancer/dashcam/dashcam_ex3_s2.png';
import dashcam_ex3_s3 from '/img/instruments/videomancer/dashcam/dashcam_ex3_s3.png';
import dashcam_ex3_s4 from '/img/instruments/videomancer/dashcam/dashcam_ex3_s4.png';
import dashcam_ex3_s5 from '/img/instruments/videomancer/dashcam/dashcam_ex3_s5.png';
import dashcam_ex3_s6 from '/img/instruments/videomancer/dashcam/dashcam_ex3_s6.png';

# Dashcam

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: dashcam_source1_boat, after: dashcam_hero_s1 },
    { label: "Dog", before: dashcam_source2_dog, after: dashcam_hero_s2 },
    { label: "Turtle", before: dashcam_source3_turtle, after: dashcam_hero_s3 },
    { label: "Pattern", before: dashcam_source4_pattern, after: dashcam_hero_s4 },
    { label: "Man", before: dashcam_source5_man, after: dashcam_hero_s5 },
    { label: "Paint", before: dashcam_source6_paint, after: dashcam_hero_s6 },
  ]}
/>
*Barrel distortion, edge vignette, LFSR noise, and a blinking recording indicator transform clean video into convincing dashboard camera footage.*

---

## Overview

Dashcam emulates the look of footage recorded by a low-cost dashboard-mounted camera. It combines barrel distortion, vignette darkening, pseudo-random noise, night-vision tinting, sub-pixel jitter, and a blinking recording indicator dot into a single eight-clock pipeline. Every artefact is independently controllable, so you can dial in anything from a subtle lens-quality reduction to a full blown surveillance-tape aesthetic.

The pipeline processes the Y, U, and V channels through five composited stages: exposure adjustment, radial vignette, LFSR-driven noise injection, night-mode color shift, and overlay compositing. A 16-bit linear feedback shift register (seed 0xACE1, taps at bits 15, 13, 12, 10) provides the pseudo-random sequence used for both noise and stabilisation jitter. A final four-clock interpolator blends the processed signal with the dry input for wet/dry mix control.

The name references the ubiquitous dashboard cameras found in vehicles worldwide — inexpensive wide-angle cameras that record continuously through a windscreen, producing footage characterised by barrel distortion, peripheral darkening, sensor noise, and persistent recording overlays.

---

## Quick Start

1. **Night + Noise = surveillance**: Enable Night Mode and set Noise to 30–40% for the most convincing night-vision dashcam look. The green tint makes the noise grain more visible and atmospheric.
2. **Vignette before noise**: The vignette darkens the edges, and then noise is added on top. This means edge regions show less absolute noise — just like a real lens with light falloff.
3. **Indicator positioning**: Use Indicator X and Indicator Y at default positions (87%/12%) for a realistic upper-right recording dot. Move them to centre-bottom for a different camera model style.

---

## Background

### Dashboard Camera Optics

Dashboard cameras use very wide-angle lenses — typically 120° to 170° field of view — to capture as much of the road as possible. These wide lenses introduce **barrel distortion**, where straight lines near the frame edges bow outward like the sides of a barrel. The distortion is strongest at the periphery and nearly invisible at the optical centre. Dashcam models this radial displacement by computing each pixel's squared distance from the frame centre and scaling the result against the Distortion parameter. With Wide Angle enabled, the distortion coefficient increases, simulating an even cheaper or wider lens.

### Vignette and Peripheral Darkening

All lenses transmit less light at the edges of the image circle than at the centre — a phenomenon called **vignette** (from the French *vignette*, a decorative border). In expensive camera lenses this is corrected optically; in dashboard cameras it is left uncorrected or even exaggerated by the plastic lens housing. Dashcam computes a vignette factor from the horizontal distance to the frame centre, darkening pixels whose squared distance exceeds a threshold set by the Distortion control. The result is a smooth brightness rolloff toward the left and right edges.

### CCD Sensor Noise

Inexpensive CMOS and CCD sensors generate visible noise, especially in low-light conditions. The noise is a combination of shot noise (random photon arrival), read noise (amplifier thermal fluctuations), and fixed-pattern noise (pixel-to-pixel sensitivity variation). Dashcam injects additive luminance noise using a 16-bit Galois LFSR, producing a pseudo-random bit sequence that is AND-masked with the Noise parameter to control amplitude. The result resembles the grainy, shimmering texture of real low-cost sensor footage.

### Recording Indicator and Timestamp Overlays

Nearly all dashboard cameras burn a recording indicator and timestamp directly into the video stream — the data is part of the image, not metadata. The indicator is typically a small coloured dot or icon that blinks at a fixed rate to confirm the camera is recording. Dashcam draws a small red dot at a configurable position in the frame, flashing at approximately 1 Hz using bit 4 of the frame counter. The Timestamp toggle enables the overlay, and the Indicator X and Indicator Y controls position it within the frame.

### Night Vision Mode

Many dashboard cameras include an infrared LED array and a monochrome sensor mode for night recording. The resulting footage has a characteristic desaturated, green-tinted appearance — green because early night-vision systems used P43 green phosphor screens, and the convention persists in digital emulations. Dashcam's Night Mode forces the U channel to neutral (512) and shifts the V channel toward green (612), while leaving luma untouched. The result is an immediate monochrome-green transformation regardless of the input colour content.


---

## Signal Flow

Y Channel → U/V Channels → Sync Signals → Interpolator → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Sync Edge Detection      (hsync/vsync fall → counters)
│   ├─ 2. Position Counters        (x_counter, y_counter, frame)
│   ├─ 3. LFSR Update              (16-bit Galois, taps 15/13/12/10)
│   ├─ 4. Vignette Compute         (dist_x² vs Distortion threshold)
│   ├─ 5. Noise Injection          (LFSR AND Noise mask → additive Y)
│   ├─ 6. Recording Indicator      (red dot when Timestamp enabled)
│   ├─ 7. Night Mode Y             (pass-through)
│   └─ 8. Clamp to [0, 1023]
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Recording Indicator      (force U=400, V=800 at dot)
│   ├─ 2. Night Mode               (U→512 neutral, V→612 green)
│   └─ 3. Else pass-through
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay pipeline (hsync, vsync, field)
│
├── Interpolator (4 clocks) ────────────────────────────────────
│   └─ Wet/dry blend: lerp(delayed_in, processed, Mix)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The vignette and noise injection both operate on the Y channel only — chroma passes through unmodified except when overridden by the recording indicator or night mode. The recording indicator has the highest compositing priority: when the pixel falls within the indicator region and the frame counter's bit 4 is high, Y/U/V are forced to fixed values (256/400/800) producing a blinking red dot. Night mode has the next priority, forcing chroma to a neutral-green tint. The LFSR runs continuously regardless of which effects are enabled, ensuring a consistent noise floor and avoiding start-up correlation.

---

## Parameter Reference

<img src={dashcam_control_panel} alt="Videomancer front panel with Dashcam loaded"/>
*Videomancer's front panel with Dashcam active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Exposure
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0% the image is darkened, simulating an underexposed sensor. At 50% (mid-position) the signal passes at unity. Higher values brighten the image, simulating the automatic gain control boost that cheap cameras apply in dim conditions. Combine with Noise for a realistic low-light look where gain boost makes sensor noise more visible. Internally, controls the overall exposure level — a brightness offset applied to the luma channel.

---

#### Knob 2 — Distortion
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the vignette and barrel distortion intensity. The value sets the squared-distance threshold at which peripheral darkening begins. At 0% the vignette is severe — only the centre of the frame retains full brightness. At higher values the darkening threshold pushes outward, reducing the visible vignette. This parameter also influences the apparent barrel distortion when Wide Angle is enabled, since the radial distance calculation feeds both effects.

---

#### Knob 3 — Noise
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

At 0% no noise is added. As the value increases, the AND mask opens more bits of the LFSR output, allowing larger noise excursions. At maximum the full 10-bit LFSR sample is added, producing aggressive grain that dominates the image. The noise is additive and unsigned, so it biases luma upward — a characteristic of real sensor noise at high gain. Internally, controls the amplitude of LFSR noise injected into the luma channel.

---

#### Knob 4 — Flicker
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 6% |
| Suffix | % |

Controls a brightness flicker effect that simulates the frame-to-frame exposure variation of a cheap auto-exposure system. At 0% the brightness is stable. Higher values introduce periodic brightness modulation driven by the frame counter, creating the stuttering exposure shifts visible in low-cost camera footage. The flicker frequency is tied to the frame counter's lower bits and the register value.

---

#### Knob 5 — Indicator X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 88% |
| Suffix | % |

At 0% the dot sits at the left edge of the frame. At 100% it moves to the right edge. The default position (approximately 87%) places the dot in the upper-right corner, matching the convention of most dashboard camera firmware. The indicator is only visible when the Timestamp toggle is enabled. Internally, sets the horizontal position of the recording indicator dot.

---

#### Knob 6 — Indicator Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

At 0% the dot is at the top of the frame. At 100% it moves to the bottom. The default (approximately 12%) places it near the top. Combined with Indicator X, this allows the recording dot to be positioned anywhere in the frame — useful for matching specific camera models or for creative overlay placement. Internally, sets the vertical position of the recording indicator dot.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Night Mode** | Off | On |
| **8 — Wide Angle** | Off | On |
| **9 — Stabilize** | Off | On |
| **10 — Timestamp** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control binary processing modes that layer on top of the continuous parameter controls. Night Mode, Wide Angle, and Stabilize each enable a distinct artefact. Timestamp enables the recording indicator overlay. Bypass routes the input directly to output. Unlike programs where toggles form a combined selector, each Dashcam toggle is independent — any combination of modes can be active simultaneously.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Dashcam processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Dashcam-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These three exercises progress from basic lens emulation to full surveillance-tape reconstruction. Each adds more artefact layers and explores how they interact.

### Exercise 1: Wide-Angle Lens Look

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: dashcam_source1_boat, after: dashcam_ex1_s1 },
    { label: "Dog", before: dashcam_source2_dog, after: dashcam_ex1_s2 },
    { label: "Turtle", before: dashcam_source3_turtle, after: dashcam_ex1_s3 },
    { label: "Pattern", before: dashcam_source4_pattern, after: dashcam_ex1_s4 },
    { label: "Man", before: dashcam_source5_man, after: dashcam_ex1_s5 },
    { label: "Paint", before: dashcam_source6_paint, after: dashcam_ex1_s6 },
  ]}
/>
*Wide-Angle Lens Look — simulated result across source images.*
**Source**: A live camera feed or recorded footage with visible straight lines — architecture, grids, or tiled surfaces.

**What You'll Create**: Learn how barrel distortion and vignette interact to create a cheap wide-angle lens simulation.

1. **Centre the vignette**: Set Distortion to about 50%. Observe the peripheral darkening — the frame edges are dimmer than the centre.
2. **Increase distortion**: Lower Distortion toward 20%. The vignette tightens, darkening more of the frame. Watch for the barrel curvature effect on straight lines.
3. **Wide angle**: Enable Wide Angle (Toggle 8). The distortion becomes more pronounced. Straight lines near the edges bow outward visibly.
4. **Noise floor**: Add a touch of Noise (about 15%). The combination of vignette and noise creates a convincing cheap-lens look.
5. **Mix blend**: Pull Mix down to about 70% to soften the effect slightly.

**Key concepts**: Barrel distortion bows straight lines outward from the optical centre, vignette darkens the periphery due to lens light falloff, wide-angle lenses exaggerate both effects

---

### Exercise 2: Night Surveillance

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: dashcam_source1_boat, after: dashcam_ex2_s1 },
    { label: "Dog", before: dashcam_source2_dog, after: dashcam_ex2_s2 },
    { label: "Turtle", before: dashcam_source3_turtle, after: dashcam_ex2_s3 },
    { label: "Pattern", before: dashcam_source4_pattern, after: dashcam_ex2_s4 },
    { label: "Man", before: dashcam_source5_man, after: dashcam_ex2_s5 },
    { label: "Paint", before: dashcam_source6_paint, after: dashcam_ex2_s6 },
  ]}
/>
*Night Surveillance — simulated result across source images.*
**Source**: Dark or dimly-lit footage, or any footage where the contrast between bright and dark areas is prominent.

**What You'll Create**: Combine night mode, noise, and the recording indicator for a convincing night-vision dashcam look.

1. **Night mode**: Enable Night Mode (Toggle 7). The image immediately shifts to a green-tinted monochrome.
2. **Boost exposure**: Increase Exposure to about 65%. The image brightens, simulating AGC gain boost.
3. **Sensor noise**: Increase Noise to about 40%. The noise becomes very visible in the green-tinted image — this is the signature look of night-vision footage.
4. **Recording indicator**: Enable Timestamp (Toggle 10). The blinking red dot appears in the corner.
5. **Position the dot**: Adjust Indicator X and Indicator Y to place the dot in the upper-right corner.
6. **Stabilisation jitter**: Enable Stabilize (Toggle 9) for subtle frame-to-frame tremor.

**Key concepts**: Night mode desaturates and green-tints via forced chroma values, noise is more visible at boosted exposure, the recording indicator composites on top of all other effects

---

### Exercise 3: Full Dashcam Reconstruction

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: dashcam_source1_boat, after: dashcam_ex3_s1 },
    { label: "Dog", before: dashcam_source2_dog, after: dashcam_ex3_s2 },
    { label: "Turtle", before: dashcam_source3_turtle, after: dashcam_ex3_s3 },
    { label: "Pattern", before: dashcam_source4_pattern, after: dashcam_ex3_s4 },
    { label: "Man", before: dashcam_source5_man, after: dashcam_ex3_s5 },
    { label: "Paint", before: dashcam_source6_paint, after: dashcam_ex3_s6 },
  ]}
/>
*Full Dashcam Reconstruction — simulated result across source images.*
**Source**: Any moving footage — particularly driving footage or POV video.

**What You'll Create**: Layer all artefacts simultaneously to produce a complete dashboard camera emulation.

1. **Lens simulation**: Set Distortion to about 30%, enable Wide Angle.
2. **Noise and flicker**: Set Noise to about 25%, Flicker to about 15%.
3. **Exposure**: Set Exposure to about 55% for a slightly hot look.
4. **Recording overlay**: Enable Timestamp, position the indicator with Indicator X at 87% and Indicator Y at 12%.
5. **Night mode**: Optionally enable Night Mode for the green surveillance look.
6. **Stabilisation**: Enable Stabilize for vehicle-mounted camera jitter.
7. **Observe the composite**: Note how all artefacts layer — vignette + noise + indicator + night tint.
8. **A/B compare**: Toggle Bypass on and off to compare the degraded output with the clean input.

**Key concepts**: All dashcam artefacts can be active simultaneously, the recording indicator always composites on top, bypass provides instant A/B comparison regardless of settings

---


## Tips

- **Subtle degradation**: Set Mix to 50–60% for a hint of dashcam character without fully committing. Useful for adding just a touch of vignette and noise to clean footage.
- **Wide Angle stacks**: Wide Angle multiplies the Distortion effect. For extreme barrel distortion, set Distortion low and enable Wide Angle. For minimal distortion, set Distortion high and leave Wide Angle off.
- **Flicker for realism**: Small amounts of Flicker (5–15%) add the exposure instability characteristic of cheap auto-exposure systems. Too much creates an obvious strobe effect.
- **Feedback loops**: Route the output back through the input for recursive degradation — each pass adds more noise, tightens the vignette, and accumulates the dashcam aesthetic.
- **Bypass for live performance**: Use Toggle 11 to cut between clean and degraded footage in a live performance context. The transition is instantaneous.

---

## Glossary

| Term | Definition |
|------|------------|
| **AGC** | Automatic Gain Control; circuitry that boosts signal amplitude in low-light conditions, increasing both signal and noise. |
| **Barrel Distortion** | Optical aberration where straight lines near the image edges bow outward, caused by wide-angle lens geometry. |
| **BT.601** | ITU-R standard defining the YUV colour encoding used in standard-definition video and by the Videomancer pipeline. |
| **Chroma** | The colour information in a video signal, encoded as U and V components in YUV colour space. |
| **EIS** | Electronic Image Stabilisation; digital processing that compensates for camera shake by shifting the frame. |
| **LFSR** | Linear Feedback Shift Register; a digital circuit producing a deterministic pseudo-random bit sequence. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Vignette** | Peripheral darkening in an image caused by light falloff at the edges of the lens image circle. |

---
