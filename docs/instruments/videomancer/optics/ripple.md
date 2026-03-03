---
draft: true
sidebar_position: 251
slug: /instruments/videomancer/ripple
title: "Ripple"
image: /img/instruments/videomancer/ripple/ripple_hero_s1.png
description: "Ripple recreates the wave interference patterns seen in ripple tanks — the shallow-water wave demonstration trays used in physics classrooms to illustrate wave phenomena."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import ripple_control_panel from '/img/instruments/videomancer/ripple/ripple_control_panel.png';
import ripple_source1_sunset from '/img/instruments/videomancer/ripple/ripple_source1_sunset.png';
import ripple_source2_parrot from '/img/instruments/videomancer/ripple/ripple_source2_parrot.png';
import ripple_source3_elephant from '/img/instruments/videomancer/ripple/ripple_source3_elephant.png';
import ripple_source4_pattern from '/img/instruments/videomancer/ripple/ripple_source4_pattern.png';
import ripple_source5_man from '/img/instruments/videomancer/ripple/ripple_source5_man.png';
import ripple_source6_paint from '/img/instruments/videomancer/ripple/ripple_source6_paint.png';
import ripple_hero_s1 from '/img/instruments/videomancer/ripple/ripple_hero_s1.png';
import ripple_hero_s2 from '/img/instruments/videomancer/ripple/ripple_hero_s2.png';
import ripple_hero_s3 from '/img/instruments/videomancer/ripple/ripple_hero_s3.png';
import ripple_hero_s4 from '/img/instruments/videomancer/ripple/ripple_hero_s4.png';
import ripple_hero_s5 from '/img/instruments/videomancer/ripple/ripple_hero_s5.png';
import ripple_hero_s6 from '/img/instruments/videomancer/ripple/ripple_hero_s6.png';
import ripple_ex1_s1 from '/img/instruments/videomancer/ripple/ripple_ex1_s1.png';
import ripple_ex1_s2 from '/img/instruments/videomancer/ripple/ripple_ex1_s2.png';
import ripple_ex1_s3 from '/img/instruments/videomancer/ripple/ripple_ex1_s3.png';
import ripple_ex1_s4 from '/img/instruments/videomancer/ripple/ripple_ex1_s4.png';
import ripple_ex1_s5 from '/img/instruments/videomancer/ripple/ripple_ex1_s5.png';
import ripple_ex1_s6 from '/img/instruments/videomancer/ripple/ripple_ex1_s6.png';
import ripple_ex2_s1 from '/img/instruments/videomancer/ripple/ripple_ex2_s1.png';
import ripple_ex2_s2 from '/img/instruments/videomancer/ripple/ripple_ex2_s2.png';
import ripple_ex2_s3 from '/img/instruments/videomancer/ripple/ripple_ex2_s3.png';
import ripple_ex2_s4 from '/img/instruments/videomancer/ripple/ripple_ex2_s4.png';
import ripple_ex2_s5 from '/img/instruments/videomancer/ripple/ripple_ex2_s5.png';
import ripple_ex2_s6 from '/img/instruments/videomancer/ripple/ripple_ex2_s6.png';
import ripple_ex3_s1 from '/img/instruments/videomancer/ripple/ripple_ex3_s1.png';
import ripple_ex3_s2 from '/img/instruments/videomancer/ripple/ripple_ex3_s2.png';
import ripple_ex3_s3 from '/img/instruments/videomancer/ripple/ripple_ex3_s3.png';
import ripple_ex3_s4 from '/img/instruments/videomancer/ripple/ripple_ex3_s4.png';
import ripple_ex3_s5 from '/img/instruments/videomancer/ripple/ripple_ex3_s5.png';
import ripple_ex3_s6 from '/img/instruments/videomancer/ripple/ripple_ex3_s6.png';

# Ripple

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: ripple_source1_sunset, after: ripple_hero_s1 },
    { label: "Parrot", before: ripple_source2_parrot, after: ripple_hero_s2 },
    { label: "Elephant", before: ripple_source3_elephant, after: ripple_hero_s3 },
    { label: "Pattern", before: ripple_source4_pattern, after: ripple_hero_s4 },
    { label: "Man", before: ripple_source5_man, after: ripple_hero_s5 },
    { label: "Paint", before: ripple_source6_paint, after: ripple_hero_s6 },
  ]}
/>
*Ripple generating animated concentric wave interference from two independent sources, producing the classic ripple-tank caustic patterns used in physics demonstrations.*

---

## Overview

**Ripple** recreates the wave interference patterns seen in ripple tanks — the shallow-water wave demonstration trays used in physics classrooms to illustrate wave phenomena. Two point sources emit concentric circular waves that propagate outward and interact: where crests meet, **constructive interference** produces bright ridges; where a crest meets a trough, **destructive interference** produces dark nulls. The resulting pattern of bright and dark bands is called an **interference pattern**, and it is one of the most visually striking demonstrations of wave physics.

The implementation uses a 32-entry sine lookup table to map radial distance from each source to wave amplitude. Distance is computed using Manhattan (taxicab) distance for hardware efficiency — this produces diamond-shaped rather than circular wavefronts, giving the pattern a distinctive geometric character. The Wavelength control selects between 32, 64, 128, and 256-pixel wavelengths via bit-shifting, and a 16-bit frame counter drives animation by adding a speed-scaled time offset to the phase computation.

Ripple supports single-source and dual-source modes. In dual-source mode, the second source's position is controlled by the Src2 X and Y Offset knobs, allowing the interference pattern to be reshaped in real time. Color modes include monochrome (pure luminance waves), rainbow (phase-derived UV modulation), and an overlay mode that blends the wave pattern on top of the input video.

---

## Background

### What Is Wave Interference?

When two waves occupy the same space, their amplitudes add together. If two crests arrive at the same point simultaneously, they reinforce each other (**constructive interference**) and the combined amplitude is larger. If a crest arrives with a trough, they cancel (**destructive interference**) and the combined amplitude is reduced or zero. The spatial pattern of constructive and destructive zones creates the characteristic bright-and-dark fringe pattern. The spacing and curvature of the fringes encode the wavelength, source separation, and propagation medium.

### What Is Manhattan Distance?

**Manhattan distance** (also called taxicab or L1 distance) measures the distance between two points as the sum of absolute differences of their coordinates: `d = |x₁ - x₂| + |y₁ - y₂|`. Unlike Euclidean distance (which produces circular wavefronts), Manhattan distance produces diamond-shaped (45°-rotated square) wavefronts. This metric is vastly simpler to compute in hardware — no multiplication or square root needed — while still producing visually compelling and geometrically interesting wave patterns.

### What Is a Sine Lookup Table?

Computing the sine function in real-time FPGA hardware is expensive. A **sine lookup table** (LUT) stores precomputed sine values at evenly spaced phase angles. The phase (from the distance computation) is used as an index into the table, returning the corresponding wave amplitude. Ripple uses 32 entries covering one full cycle (0° to 360°), mapped to unsigned values 0–1023 (with 512 as the zero crossing). The table wraps naturally because phase is extracted from the lower 5 bits of the distance, providing automatic modular arithmetic.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ X counter (per-pixel, reset on hsync)
│   ├─ Y counter (per-line, reset on vsync)
│   └─ Frame counter (animation timebase)
│
├── Wave Engine ────────────────────────────────────────────────
│   ├─ 1. Manhattan Distance     (source 1: screen center)
│   ├─ 2. Manhattan Distance     (source 2: offset from center)
│   ├─ 3. Wavelength Shift       (32/64/128/256 pixel period)
│   ├─ 4. Phase = distance + time_offset
│   ├─ 5. Sine LUT Lookup        (32-entry ROM, 0–1023)
│   ├─ 6. Wave Sum               (single: wave1; dual: avg of 1+2)
│   ├─ 7. Amplitude Scaling      (multiply by Amplitude knob)
│   ├─ 8. Brightness Offset      (DC shift)
│   ├─ 9. Invert (optional)      (complement output)
│   └─ 10. Color Mode Output     (mono / rainbow / over video)
│
├── Wet/Dry Mix ────────────────────────────────────────────────
│   └─ Interpolator blend with delayed original
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through with 6-clock delay
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The wave engine computes everything from pixel position and time — no memory of previous frames is needed. Source 1 is fixed at screen center (360, 120 for SD). Source 2's position is computed by adding the Src2 X/Y Offset knob values (centered at zero) to the screen center. The wavelength control is a bit-shifter, not a multiplier: shifting the distance right by 0, 1, 2, or 3 bits selects wavelengths of 32, 64, 128, or 256 pixels respectively. Animation adds a speed-scaled time offset to the phase, causing the wave pattern to move outward from each source.

---

## Parameter Reference

<img src={ripple_control_panel} alt="Videomancer front panel with Ripple loaded"/>
*Videomancer's front panel with Ripple active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Wavelength
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Controls the wavelength of the wave pattern. The knob selects between four discrete wavelength settings via threshold comparison: shortest (32 pixels — the most tightly spaced) through longest (256 pixels — broad, sweeping rings). Shorter wavelengths produce closely packed fringes; longer wavelengths produce wide, gentle undulations. This is a stepped control, not continuous, because it selects a bit-shift amount.

---

#### Knob 2 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the animation speed. The frame counter is multiplied by the Speed value to compute the time offset added to each wave's phase. At minimum, the pattern is static (frozen in time). As Speed increases, the waves propagate outward faster. At maximum, the pattern animates rapidly, producing flowing, liquid-like motion. Speed has no effect on the spatial pattern when the frame is frozen — it only affects the temporal evolution.

---

#### Knob 3 — Amplitude
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls the wave amplitude — the peak-to-trough brightness range of the wave pattern. At minimum, the waves are flat (invisible — all pixels at midpoint). At maximum, the waves swing the full 0–1023 range from black to white. This control is a simple multiplier applied after the sine lookup.

---

#### Knob 4 — Src2 X Ofs
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls the horizontal offset of the second wave source from the screen center. At center (512), source 2 is co-located with source 1 (producing concentric rings identical to single-source mode). Moving the knob away from center moves source 2 left or right, spreading the interference pattern. The farther the sources are separated, the more distinct hyperbolic interference fringes appear between them.

---

#### Knob 5 — Src2 Y Ofs
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the vertical offset of the second wave source from the screen center. Functions identically to the X offset but along the vertical axis. Combine X and Y offsets to position source 2 anywhere relative to the center of the screen.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC brightness offset to the wave output. At center, no offset — the wave oscillates around midpoint. Above center, the entire pattern shifts brighter. Below center, it shifts darker. This is useful for lifting the wave pattern out of the black range or pushing it into a specific brightness zone for compositing.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color** | Mono | Rainbow |
| **8 — Over Video** | Off | On |
| **9 — Invert** | Off | On |
| **10 — Single Src** | Dual | Single |
| **11 — Bypass** | Off | On |

Switches 7–11 control color mode, video overlay, inversion, source count, and bypass. The Color and Single Src switches have the most dramatic impact on the visual output. Over Video allows the wave pattern to be composited onto the input signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the wave pattern and the original input. At 100%, the full wave pattern (or Over Video composite) is output. Lowering the fader blends the original input back in.

---

## Guided Exercises

These exercises explore single-source concentric waves, dual-source interference, and creative color and overlay modes.

### Exercise 1: Concentric Rings (Single Source)

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: ripple_source1_sunset, after: ripple_ex1_s1 },
    { label: "Parrot", before: ripple_source2_parrot, after: ripple_ex1_s2 },
    { label: "Elephant", before: ripple_source3_elephant, after: ripple_ex1_s3 },
    { label: "Pattern", before: ripple_source4_pattern, after: ripple_ex1_s4 },
    { label: "Man", before: ripple_source5_man, after: ripple_ex1_s5 },
    { label: "Paint", before: ripple_source6_paint, after: ripple_ex1_s6 },
  ]}
/>
*Concentric Rings (Single Source) — simulated result across source images.*
**Source**: Any input (ripple generates its own pattern; input is used for sync only unless Over Video is enabled).

**Objective**: Explore the basic concentric wave pattern from a single source and understand wavelength and speed controls.

1. **Single source**: Set Single Src to Single (Switch 10). Simple concentric rings appear centered on screen.
2. **Wavelength**: Sweep Wavelength from minimum to maximum. Observe the spacing of rings — 32-pixel (tight) to 256-pixel (wide).
3. **Amplitude**: Sweep Amplitude from 0% to 100%. The rings grow from invisible to full contrast.
4. **Speed**: Increase Speed from 0% to ~50%. The rings begin to propagate outward from the center.
5. **Invert**: Toggle Invert (Switch 9). Dark rings on a bright background become bright rings on dark.
6. **Brightness**: Adjust Brightness to shift the overall pattern lighter or darker.

**Key concepts**: Single source produces concentric rings, wavelength selects ring spacing in 4 discrete steps, speed animates outward propagation, Manhattan distance creates diamond-shaped wavefronts

---

### Exercise 2: Dual-Source Interference

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: ripple_source1_sunset, after: ripple_ex2_s1 },
    { label: "Parrot", before: ripple_source2_parrot, after: ripple_ex2_s2 },
    { label: "Elephant", before: ripple_source3_elephant, after: ripple_ex2_s3 },
    { label: "Pattern", before: ripple_source4_pattern, after: ripple_ex2_s4 },
    { label: "Man", before: ripple_source5_man, after: ripple_ex2_s5 },
    { label: "Paint", before: ripple_source6_paint, after: ripple_ex2_s6 },
  ]}
/>
*Dual-Source Interference — simulated result across source images.*
**Source**: Any input (sync reference only).

**Objective**: Create and explore the classic two-source interference pattern.

1. **Enable dual**: Set Single Src to Dual (Switch 10). A second set of rings appears.
2. **Separate sources**: Move Src2 X Ofs to ~75%. The two sources separate horizontally and hyperbolic interference fringes appear between them.
3. **Observe fringes**: The bright bands between the sources are constructive interference (crests meeting crests). The dark bands are destructive interference.
4. **Vary wavelength**: Change Wavelength and observe how the fringe spacing changes. Shorter wavelengths produce more fringes.
5. **Y offset**: Move Src2 Y Ofs away from center. The fringe pattern rotates as the source geometry changes.
6. **Animate**: Set Speed to ~30%. The interference pattern flows dynamically as both sources emit traveling waves.

**Key concepts**: Dual sources create interference fringes, source separation controls fringe geometry, constructive/destructive interference creates bright/dark bands

---

### Exercise 3: Rainbow Interference over Video

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: ripple_source1_sunset, after: ripple_ex3_s1 },
    { label: "Parrot", before: ripple_source2_parrot, after: ripple_ex3_s2 },
    { label: "Elephant", before: ripple_source3_elephant, after: ripple_ex3_s3 },
    { label: "Pattern", before: ripple_source4_pattern, after: ripple_ex3_s4 },
    { label: "Man", before: ripple_source5_man, after: ripple_ex3_s5 },
    { label: "Paint", before: ripple_source6_paint, after: ripple_ex3_s6 },
  ]}
/>
*Rainbow Interference over Video — simulated result across source images.*
**Source**: Live camera feed or graphic content with clear shapes and colors.

**Objective**: Combine rainbow color mode with video overlay for psychedelic compositing effects.

1. **Rainbow mode**: Set Color to Rainbow (Switch 7). The interference pattern now displays in vivid colors derived from wave phase.
2. **Over Video**: Enable Over Video (Switch 8). The wave luminance pattern modulates the input video while the rainbow UV replaces source chroma.
3. **Adjust amplitude**: Lower Amplitude to ~50%. The wave modulation becomes more subtle against the video.
4. **Animate**: Set Speed to ~20%. The color-shifting waves flow across the video surface.
5. **Mix blend**: Lower Mix to ~50%. The rainbow wave overlays the original at reduced intensity.
6. **Dual source**: Toggle to Dual and separate sources. The rainbow interference fringes create complex chromatic patterns over the video.

**Key concepts**: Rainbow maps phase to hue, Over Video composites waves on input, mixing controls overlay intensity, dual-source rainbow creates chromatic interference

---


## Tips

- **Manhattan diamonds**: The diamond-shaped wavefronts (from Manhattan distance) give Ripple a unique geometric character — embrace them rather than expecting circles.
- **Separate sources for fringes**: The interference pattern only appears when sources are separated. Use Src2 X Ofs to spread them.
- **Static for composition**: Set Speed to 0 for a frozen wave pattern useful as a compositing element or texture.
- **Rainbow for psychedelia**: Rainbow mode maps phase to hue, creating vivid color interference that evolves with animation.
- **Over Video for texturing**: Use Over Video at moderate amplitude and mix to add a ripple texture to any live video source.
- **Wavelength and source spacing interact**: Shorter wavelengths with wide source separation produce more fringes; longer wavelengths with close sources produce broad patterns.
- **Brightness centers the pattern**: Use Brightness to shift the wave's DC level for compositing over other video sources.

---

## Glossary

| Term | Definition |
|------|------------|
| **Constructive Interference** | Two waves arriving in phase, reinforcing each other to produce a brighter combined amplitude. |
| **Destructive Interference** | Two waves arriving out of phase, canceling each other to produce a darker combined amplitude. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interference Pattern** | The spatial pattern of bright and dark fringes created by the superposition of two or more waves. |
| **Manhattan Distance** | Distance measured as the sum of absolute differences of coordinates: |Δx| + |Δy|. Produces diamond-shaped wavefronts. |
| **Phase** | The position within a wave's cycle, determining its instantaneous amplitude (crest, trough, or in between). |
| **Ripple Tank** | A physics demonstration apparatus using shallow water to visualize wave phenomena: reflection, refraction, diffraction, and interference. |
| **Sine LUT** | A lookup table containing precomputed sine values, used instead of real-time trigonometric computation. |
| **Wavelength** | The distance between successive wave crests; determines the spatial frequency of the wave pattern. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
