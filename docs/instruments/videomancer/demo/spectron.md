---
draft: true
sidebar_position: 264
slug: /instruments/videomancer/spectron
title: "Spectron"
image: /img/instruments/videomancer/spectron/spectron_hero.png
description: "Spectron is a multi-oscillator interference synthesizer that generates slowly evolving moire patterns, standing waves, and diagonal colour bands purely from the interaction of three DDS sine or square waves with the raster scan."
---

import spectron_hero from '/img/instruments/videomancer/spectron/spectron_hero.png';
import spectron_animation from '/img/instruments/videomancer/spectron/spectron_animation.gif';
import spectron_control_panel from '/img/instruments/videomancer/spectron/spectron_control_panel.png';
import spectron_exercise1_result from '/img/instruments/videomancer/spectron/spectron_exercise1_result.gif';
import spectron_exercise2_result from '/img/instruments/videomancer/spectron/spectron_exercise2_result.gif';
import spectron_exercise3_result from '/img/instruments/videomancer/spectron/spectron_exercise3_result.gif';

# Spectron

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={spectron_hero} alt="Spectron hero image"/>
*Three interlocked oscillators beat against scan timing to weave shimmering moire fields of crawling colour.*
<img src={spectron_animation} alt="Spectron animated output"/>
*Spectron output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Spectron is a multi-oscillator interference synthesizer that generates slowly evolving moire patterns, standing waves, and diagonal colour bands purely from the interaction of three DDS sine or square waves with the raster scan. Each oscillator multiplies a position counter by its frequency register, producing spatial sinusoids whose beat frequencies with one another create the rich, slowly crawling structures associated with analog video synthesizers of the 1970s.

The three oscillators can be combined additively — producing luminance washes that shift gently across the screen — or via ring modulation, where the product of two oscillators is scaled by the third to create dense harmonic textures. A per-frame drift counter offsets the phases of oscillators 2 and 3, so the pattern never quite repeats. Colour is painted directly from the oscillator phases: one oscillator maps to U, another to V, with a spread control widening or narrowing the chroma palette.

When Video Mod is engaged the first oscillator's output is amplitude-modulated by the incoming luminance, letting external imagery punch through the interference field and merge with the synthesized pattern.

---

## Background

### The Spectron Heritage

The Spectron name evokes a lineage of electronic instruments designed to turn frequency into visible form. In the 1970s, organisations like EMS and individual experimenters built oscillator banks that generated video-rate sine and square waves directly in the analog domain, beating them against horizontal and vertical sync to produce geometric colour fields. Spectron continues this tradition in the digital domain using DDS oscillators clocked at pixel rate.

### DDS and Spatial Frequency

A Direct Digital Synthesis accumulator adds a frequency word to a phase register every clock. Because the clock here is the pixel clock, and the position counter tracks where the beam is on screen, the oscillator frequency maps directly to a spatial frequency — cycles per scan line or cycles per frame. Small register values produce wide bars; large values produce fine interference fringes.

### Ring Modulation and Moire

When two sine waves at frequencies f₁ and f₂ are multiplied, the result contains components at f₁+f₂ and f₁−f₂. Visually this produces moire — a coarser pattern emerges from two finer gratings. Spectron chains three oscillators so the ring-modulation path yields second-order beats, generating complex textures that a simple sum cannot reach.

### Drift and Near-Harmonic Beating

The drift phase counter advances once per frame, slowly offsetting oscillators 2 and 3. This means a pattern that looks static at first will, over seconds, slowly translate across the screen as the phase relationships wander. The visual effect resembles oil on water or the shimmer of heat haze — a hallmark of analog video synthesis.

### Video Modulation Bridge

Engaging Video Mod multiplies oscillator 1's sine output by the input image's luminance on a per-pixel basis. Bright areas of the source image allow the oscillator through; dark areas suppress it. The result is an interference field that is shaped by the camera image, merging synthesis and processing.


---

## Signal Flow

```
 ┌──────────────┐    ┌──────────────────────────────┐
 │  Position    │───▸│  DDS Phase × Freq Word       │
 │  H + V count │    │  3 independent oscillators    │
 └──────────────┘    └───────┬──────┬──────┬────────┘
                         osc1│  osc2│  osc3│
                             ▼      ▼      ▼
                     ┌───────────────────────────┐
                     │  Sine / Square LUT        │
                     └───────┬──────┬──────┬─────┘
                             │      │      │
                   ┌─────────┴──────┴──────┴─────────┐
                   │  Combine (Sum | Ring Mod)        │
                   │  + Coupling for ring path        │
                   └─────────────────┬───────────────┘
                                     │ Y
                   ┌─────────────────┤
                   │                 ▼
   Video Mod ─────▸│  Luma from osc phases
                   │  U ← osc2 + spread
                   │  V ← osc3 − spread
                   └─────────────────┬───────────────┘
                                     │ YUV wet
                                     ▼
                      ┌─────────────────────────┐
           dry ──────▸│  interpolator mix        │──▸ data_out
                      └─────────────────────────┘
```

The position value fed to the oscillators is the sum of horizontal and vertical pixel counters. When the Axis toggle selects Diagonal mode, the vertical counter is right-shifted by one before adding, tilting the interference fringes. The drift phase is added only to oscillators 2 and 3 (with a 2× multiplier on osc 3), so oscillator 1 remains the spatial reference against which the other two beat. This asymmetry is what makes the pattern evolve rather than simply scroll.

---

## Parameter Reference

<img src={spectron_control_panel} alt="Videomancer front panel with Spectron loaded"/>
*Videomancer's front panel with Spectron active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Osc 1 Freq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

**Osc 1 Freq** sets the spatial frequency of the first oscillator. Low values produce a few broad vertical bands; high values create fine gratings. Because oscillator 1 is the unshifted reference, changing its frequency redefines the fundamental spatial pitch of the entire pattern.

---

#### Knob 2 — Osc 2 Freq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

**Osc 2 Freq** controls the second oscillator. Its phase is offset by the drift counter, so it slowly wanders relative to oscillator 1. The beat frequency between oscillators 1 and 2 determines the primary moire spacing — small frequency differences create very wide, slowly crawling interference bands.

---

#### Knob 3 — Osc 3 Freq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**Osc 3 Freq** controls the third oscillator. Its drift offset is doubled relative to oscillator 2, so it wanders faster. In sum mode the three sine waves produce luminance that varies smoothly across the screen. In ring mode, oscillator 3 acts as a coupling depth for the product of 1 and 2.

---

#### Knob 4 — Coupling
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

**Coupling** scales the ring-modulation product when Combine is set to Ring Mod. At zero the ring path is silent; at maximum the full osc1×osc2×osc3 product passes. In sum mode this register is unused — the three oscillators add equally.

---

#### Knob 5 — Saturation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

**Saturation** controls the chroma intensity by adjusting mapping spread. Higher values push U and V further from mid-code, creating vivid colour banding. Low values keep the output closer to monochrome.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**Brightness** adjusts the bias and gain applied after combination. This shifts the overall luminance of the synthesized pattern, complementing the saturation control for final tonal balance.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Routing** | Sum | Ring Mod |
| **8 — Waveform** | Sine | Square |
| **9 — Color Map** | RGB | YUV |
| **10 — Video Mod** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles define the synthesis character: Routing chooses between smooth additive beating and harsh harmonic-rich ring modulation. Waveform changes the oscillator shape from smooth sines to hard-edged square waves, dramatically increasing harmonic content. Color Map switches how oscillator phases are mapped to the chroma plane. Video Mod engages external image modulation, and Bypass disables the effect entirely.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

**Mix** crossfades between the dry input and the synthesized interference pattern. At zero the output is the unaltered input; at maximum it is entirely the Spectron synthesis.

---

## Guided Exercises

These exercises explore Spectron's range from gentle drifting colour fields to aggressive high-contrast moire, with and without external video.

### Exercise 1: Slow Colour Drift

<img src={spectron_exercise1_result} alt="Slow Colour Drift result"/>
*Slow Colour Drift — simulated result across source images.*
**Objective**: Create a slowly evolving pastel colour field with gentle moire beating.

1. Set Osc 1 Freq to 25 % and Osc 2 Freq to 26 % — the 1 % difference creates a wide, slowly drifting beat.
2. Set Osc 3 Freq to 50 % for a secondary spatial structure.
3. Set Coupling to 25 % — unused in sum mode but ready for comparison.
4. Set Saturation to 60 % for moderate colour.
5. Set Brightness to 50 %.
6. Select Sum routing, Sine waveform, RGB Color Map.
7. Leave Video Mod and Bypass off, Mix at 100 %.
8. Observe the broad pastel bands slowly shifting across the screen.

**Key concepts**: Near-harmonic beating, spatial frequency, drift phase offset.

---

### Exercise 2: Hard Moire Grid

<img src={spectron_exercise2_result} alt="Hard Moire Grid result"/>
*Hard Moire Grid — simulated result across source images.*
**Objective**: Produce a high-contrast diagonal moire grid using ring modulation and square waves.

1. Set Osc 1 Freq and Osc 2 Freq to 50 % each.
2. Set Osc 3 Freq to 75 %.
3. Set Coupling to 80 %.
4. Set Saturation and Brightness to 75 %.
5. Switch Routing to Ring Mod, Waveform to Square, Color Map to YUV.
6. The screen fills with a dense black/white/colour checkerboard.
7. Slowly reduce Osc 2 Freq toward 48 % and watch the beat pattern emerge.

**Key concepts**: Ring modulation, spatial harmonics, square-wave clipping, moire interference.

---

### Exercise 3: Video-Modulated Interference

<img src={spectron_exercise3_result} alt="Video-Modulated Interference result"/>
*Video-Modulated Interference — simulated result across source images.*
**Objective**: Use the input image's luminance to carve the interference pattern, revealing the subject as a shimmering outline.

1. Set Osc 1 Freq to 40 %, Osc 2 Freq to 42 %, Osc 3 Freq to 60 %.
2. Set Coupling to 50 %, Saturation to 80 %, Brightness to 50 %.
3. Select Sum routing, Sine waveform.
4. Enable Video Mod — the bright areas of the source allow the oscillator through.
5. Set Mix to 80 % for a subtle blend of dry source underneath.
6. Try switching to Ring Mod — notice how dark areas now create voids in the moire.

**Key concepts**: Amplitude modulation, image masking via oscillator scaling, synthesis-processing bridge.

---


## Tips

- **Near-unison beating**: Set two oscillators within 1–2 % of each other for slow, wide moire bands.
- **Harmonic ratios**: Set oscillators at 1:2:3 ratio (e.g., 25 %, 50 %, 75 %) for stable standing-wave geometric patterns.
- **Square + ring**: This combination produces the highest contrast; use Coupling below 50 % to keep it from clipping harshly.
- **Saturation zoning**: Back off saturation to zero for monochrome interference, then add colour gradually.
- **Video Mod as masking**: Feed a graphic with clear silhouettes — the oscillator pattern appears only inside bright regions.
- **Mix for layering**: At 30–50 % mix the interference pattern acts as a subtle texture overlay on the source.

---
