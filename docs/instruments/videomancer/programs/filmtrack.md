---
draft: true
sidebar_position: 112
slug: /instruments/videomancer/filmtrack
title: "Film Track"
image: /img/instruments/videomancer/filmtrack/filmtrack_hero_s1.png
description: "Film Track converts input video luminance into scrolling horizontal stripe patterns inspired by the optical sound tracks found on 35 mm motion picture film."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import filmtrack_control_panel from '/img/instruments/videomancer/filmtrack/filmtrack_control_panel.png';
import filmtrack_source1_car from '/img/instruments/videomancer/filmtrack/filmtrack_source1_car.png';
import filmtrack_source2_ballerina from '/img/instruments/videomancer/filmtrack/filmtrack_source2_ballerina.png';
import filmtrack_source3_elephant from '/img/instruments/videomancer/filmtrack/filmtrack_source3_elephant.png';
import filmtrack_source4_pattern from '/img/instruments/videomancer/filmtrack/filmtrack_source4_pattern.png';
import filmtrack_source5_woman from '/img/instruments/videomancer/filmtrack/filmtrack_source5_woman.png';
import filmtrack_source6_knit from '/img/instruments/videomancer/filmtrack/filmtrack_source6_knit.png';
import filmtrack_hero_s1 from '/img/instruments/videomancer/filmtrack/filmtrack_hero_s1.png';
import filmtrack_hero_s2 from '/img/instruments/videomancer/filmtrack/filmtrack_hero_s2.png';
import filmtrack_hero_s3 from '/img/instruments/videomancer/filmtrack/filmtrack_hero_s3.png';
import filmtrack_hero_s4 from '/img/instruments/videomancer/filmtrack/filmtrack_hero_s4.png';
import filmtrack_hero_s5 from '/img/instruments/videomancer/filmtrack/filmtrack_hero_s5.png';
import filmtrack_hero_s6 from '/img/instruments/videomancer/filmtrack/filmtrack_hero_s6.png';
import filmtrack_ex1_s1 from '/img/instruments/videomancer/filmtrack/filmtrack_ex1_s1.png';
import filmtrack_ex1_s2 from '/img/instruments/videomancer/filmtrack/filmtrack_ex1_s2.png';
import filmtrack_ex1_s3 from '/img/instruments/videomancer/filmtrack/filmtrack_ex1_s3.png';
import filmtrack_ex1_s4 from '/img/instruments/videomancer/filmtrack/filmtrack_ex1_s4.png';
import filmtrack_ex1_s5 from '/img/instruments/videomancer/filmtrack/filmtrack_ex1_s5.png';
import filmtrack_ex1_s6 from '/img/instruments/videomancer/filmtrack/filmtrack_ex1_s6.png';
import filmtrack_ex2_s1 from '/img/instruments/videomancer/filmtrack/filmtrack_ex2_s1.png';
import filmtrack_ex2_s2 from '/img/instruments/videomancer/filmtrack/filmtrack_ex2_s2.png';
import filmtrack_ex2_s3 from '/img/instruments/videomancer/filmtrack/filmtrack_ex2_s3.png';
import filmtrack_ex2_s4 from '/img/instruments/videomancer/filmtrack/filmtrack_ex2_s4.png';
import filmtrack_ex2_s5 from '/img/instruments/videomancer/filmtrack/filmtrack_ex2_s5.png';
import filmtrack_ex2_s6 from '/img/instruments/videomancer/filmtrack/filmtrack_ex2_s6.png';
import filmtrack_ex3_s1 from '/img/instruments/videomancer/filmtrack/filmtrack_ex3_s1.png';
import filmtrack_ex3_s2 from '/img/instruments/videomancer/filmtrack/filmtrack_ex3_s2.png';
import filmtrack_ex3_s3 from '/img/instruments/videomancer/filmtrack/filmtrack_ex3_s3.png';
import filmtrack_ex3_s4 from '/img/instruments/videomancer/filmtrack/filmtrack_ex3_s4.png';
import filmtrack_ex3_s5 from '/img/instruments/videomancer/filmtrack/filmtrack_ex3_s5.png';
import filmtrack_ex3_s6 from '/img/instruments/videomancer/filmtrack/filmtrack_ex3_s6.png';

# Film Track

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Car", before: filmtrack_source1_car, after: filmtrack_hero_s1 },
    { label: "Ballerina", before: filmtrack_source2_ballerina, after: filmtrack_hero_s2 },
    { label: "Elephant", before: filmtrack_source3_elephant, after: filmtrack_hero_s3 },
    { label: "Pattern", before: filmtrack_source4_pattern, after: filmtrack_hero_s4 },
    { label: "Woman", before: filmtrack_source5_woman, after: filmtrack_hero_s5 },
    { label: "Knit", before: filmtrack_source6_knit, after: filmtrack_hero_s6 },
  ]}
/>
*Moving video becomes a scrolling strip of optical sound tracks — variable-area and variable-density stripes flowing downward like a film projector frozen mid-frame.*

---

## Overview

Film Track converts input video luminance into scrolling horizontal stripe patterns inspired by the optical sound tracks found on 35 mm motion picture film. In variable-area mode the stripe width is proportional to the sampled brightness, producing the transparent wedge shapes familiar from any analog film print. In variable-density mode every column within the track region carries the sampled brightness as opacity, creating a uniform-width band whose shade undulates with the signal. The stripes are written into a 64 × 256 framebuffer that scrolls vertically, building a marching spectrogram-like display of the input over time.

The inspiration draws from Norman McLaren, Oskar Fischinger, and the Whitney brothers, who hand-painted and scratched marks directly onto the sound-track area of 35 mm film, inventing "drawn sound" before electronic synthesis existed. Film Track reverses the process: instead of marks creating sound, video creates marks.

Colour tinting lets the stripes take on the warm amber of silver-nitrate stock or cool cyan of safety film. A border toggle adds dark edge strips that mimic the sprocket-hole area, completing the physical-film aesthetic.

---

## Quick Start

1. **Sample point as scanner**: Sweeping Exposure while scrolling converts the display into a slow spatial scan of the source image.
2. **Unilateral for waveform display**: Unilateral profile produces a classic single-sided waveform trace, more legible than bilateral for amplitude analysis.
3. **Amber tinting**: Film Tint around 30–60° recreates the warm amber of vintage nitrate film stock.

---

## Background

### Optical Sound Tracks

From the late 1920s until the transition to digital cinema, most 35 mm prints carried an optical sound track — a narrow strip along the edge of the film that encoded an audio waveform optically. A variable-area track varies the width of a transparent slit; a variable-density track varies the opacity of a fixed-width band. Both methods convert light passing through the film into an electrical audio signal at the projector's sound-head.

### Norman McLaren's Drawn Sound

McLaren at the National Film Board of Canada pioneered drawing, scratching, and photographing marks directly onto the optical sound-track area. By controlling the shape, spacing, and density of these marks, he could synthesise audio without any electronic equipment — a visual music technique that predated modern digital synthesis by decades.

### Framebuffer Scroll Mechanism

Film Track writes one row of the framebuffer per scan line (at the luminance sampled from a configurable horizontal position). The write pointer advances down the buffer. During readout, each screen pixel maps into the buffer with a row offset that keeps the content scrolling vertically. The scroll speed register controls how many rows the write pointer jumps per frame.

### Variable-Area vs Variable-Density Geometry

In variable-area mode, the width of the bright stripe is proportional to the sampled luminance. Each row is binary — fully bright inside the stripe, black outside. In variable-density mode, the stripe width is fixed (set by the Track Width knob) but every pixel within the stripe is set to the sampled brightness, producing a smooth grey-level encoding.

### Film-Stock Colour Tinting

Early film prints were tinted by immersing the stock in coloured dye baths — sepia for interiors, blue for night scenes, amber for sunlight. The Film Tint control applies a similar colour rotation to the chroma channels, letting the output evoke different eras of film processing.


---

## Signal Flow

```
 data_in.y ─────┐
                 ▼
      ┌─────────────────────┐
      │  Luminance Sampler  │
      │  (at sample_point)  │
      └────────┬────────────┘
               │ sampled_luma
               ▼
      ┌─────────────────────────────┐
      │  Track Writer (per line)    │
      │  Var.Area: width ∝ luma    │
      │  Var.Dens: opacity = luma  │
      └────────┬────────────────────┘
               │ write to FB
               ▼
      ┌─────────────────────────────┐
      │  64 × 256 Framebuffer      │
      │  (scroll ptr per frame)    │
      └────────┬────────────────────┘
               │ read per pixel
               ▼
      ┌─────────────────────┐
      │  Negative inversion │
      │  Border overlay     │
      │  Brightness gain    │
      │  Hue tinting (U/V)  │
      └────────┬────────────┘
               │ YUV wet
               ▼
      ┌─────────────────────────┐
 dry ▸│  interpolator mix       │──▸ data_out
      └─────────────────────────┘
```

The sampler captures the input luminance at a horizontal position controlled by the Exposure register each scan line, and a mirrored position for the stereo channel. The framebuffer is 64 columns wide — the screen's horizontal axis is right-shifted by 5 to index into it. The scroll write pointer wraps at 256, so the visible history is approximately 256 lines deep. Negative inversion applies a simple byte complement before brightness scaling. Hue tinting sets the U/V chroma only where the track pixel exceeds a minimum brightness threshold, keeping the background achromatic.

---

## Parameter Reference

<img src={filmtrack_control_panel} alt="Videomancer front panel with Film Track loaded"/>
*Videomancer's front panel with Film Track active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Scroll Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

**Scroll Spd** sets the vertical scroll rate by controlling how many rows the write pointer advances per frame. Low values produce a slow waterfall; high values create a fast-scrolling display where new data rapidly pushes old data off screen.

---

#### Knob 2 — Amplitude
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**Amplitude** controls the stripe width in variable-area mode and the overall track region width in variable-density mode. Higher values create wider stripes that span more of the framebuffer columns; lower values produce thin, delicate traces.

---

#### Knob 3 — Band Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

**Band Width** adjusts the horizontal extent of the active track region within the framebuffer, setting a baseline width that the amplitude then modulates.

---

#### Knob 4 — Exposure
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**Exposure** sets the horizontal position on each input scan line where the luminance sample is captured. Sweeping this control scans the sample point across the source image, changing which part of the video feeds the sound-track pattern.

---

#### Knob 5 — Film Tint
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

**Film Tint** rotates the chroma colour applied to bright track pixels through 360° of hue angle. At 0° the tint is neutral; swept through the range it passes through amber, cyan, magenta, and green, evoking different film-stock dye tints.

---

#### Knob 6 — Track Count
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 2 |

**Track Count** selects 1 to 4 parallel sound tracks rendered side by side across the framebuffer, splitting the display into multiple lanes for a multi-channel soundtrack appearance.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Var Area | Var Density |
| **8 — Profile** | Bilateral | Unilateral |
| **9 — Film Base** | Clear | Tinted |
| **10 — Sprockets** | Off | On |
| **11 — Bypass** | Off | On |

The toggles define the optical-soundtrack aesthetic: Mode picks the encoding method (area vs density). Profile selects bilateral (symmetric about centreline) or unilateral (one-sided) stripe geometry. Film Base determines whether the background is clear (black) or tinted to the Film Tint hue. Sprockets adds border lines mimicking the sprocket-hole area of 35 mm film. Bypass disables the effect.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

**Mix** crossfades between the dry input and the film-track output. At zero the input is passed through; at maximum the output is fully the scrolling sound-track pattern.





---

## Guided Exercises

These exercises explore Film Track's visual vocabulary from minimal mono traces to multi-channel tinted film-strip displays.

### Exercise 1: Classic Mono Variable-Area

<BeforeAfterSlider
  sources={[
    { label: "Car", before: filmtrack_source1_car, after: filmtrack_ex1_s1 },
    { label: "Ballerina", before: filmtrack_source2_ballerina, after: filmtrack_ex1_s2 },
    { label: "Elephant", before: filmtrack_source3_elephant, after: filmtrack_ex1_s3 },
    { label: "Pattern", before: filmtrack_source4_pattern, after: filmtrack_ex1_s4 },
    { label: "Woman", before: filmtrack_source5_woman, after: filmtrack_ex1_s5 },
    { label: "Knit", before: filmtrack_source6_knit, after: filmtrack_ex1_s6 },
  ]}
/>
*Classic Mono Variable-Area — simulated result across source images.*
**Source**: A talking head with moderate contrast, or any source with clear brightness changes.

**What You'll Create**: Create a single-track variable-area display with a slow scroll.

1. Set Scroll Spd to 25 %, Amplitude to 50 %, Band Width to 40 %.
2. Set Exposure to 50 % (sample from image centre).
3. Set Film Tint to 0° (neutral), Track Count to 1.
4. Select Var Area mode, Bilateral profile.
5. Film Base Clear, Sprockets Off, Mix 100 %.
6. Watch the sound track build line by line as the source moves.

**Key concepts**: Luminance sampling, variable-area encoding, scroll speed.

---

### Exercise 2: Tinted Film Strip

<BeforeAfterSlider
  sources={[
    { label: "Car", before: filmtrack_source1_car, after: filmtrack_ex2_s1 },
    { label: "Ballerina", before: filmtrack_source2_ballerina, after: filmtrack_ex2_s2 },
    { label: "Elephant", before: filmtrack_source3_elephant, after: filmtrack_ex2_s3 },
    { label: "Pattern", before: filmtrack_source4_pattern, after: filmtrack_ex2_s4 },
    { label: "Woman", before: filmtrack_source5_woman, after: filmtrack_ex2_s5 },
    { label: "Knit", before: filmtrack_source6_knit, after: filmtrack_ex2_s6 },
  ]}
/>
*Tinted Film Strip — simulated result across source images.*
**Source**: Music video or animated source with rhythmic brightness variation.

**What You'll Create**: Create a multi-track amber-tinted film strip with border sprockets.

1. Set Scroll Spd to 40 %, Amplitude to 60 %, Band Width to 50 %.
2. Set Exposure to 50 %, Film Tint to 45° (warm amber), Track Count to 4.
3. Select Var Density mode, Bilateral profile.
4. Enable Tinted Film Base and Sprockets.
5. Mix at 100 %. The display resembles the edge of a 35 mm optical sound print.

**Key concepts**: Variable density, multi-track, film-stock tinting, sprocket border.

---

### Exercise 3: Dynamic Scan Sweep

<BeforeAfterSlider
  sources={[
    { label: "Car", before: filmtrack_source1_car, after: filmtrack_ex3_s1 },
    { label: "Ballerina", before: filmtrack_source2_ballerina, after: filmtrack_ex3_s2 },
    { label: "Elephant", before: filmtrack_source3_elephant, after: filmtrack_ex3_s3 },
    { label: "Pattern", before: filmtrack_source4_pattern, after: filmtrack_ex3_s4 },
    { label: "Woman", before: filmtrack_source5_woman, after: filmtrack_ex3_s5 },
    { label: "Knit", before: filmtrack_source6_knit, after: filmtrack_ex3_s6 },
  ]}
/>
*Dynamic Scan Sweep — simulated result across source images.*
**Source**: Any source with horizontal variation (panorama, landscape, scrolling text).

**What You'll Create**: Sweep the sample point across the image while the track scrolls, producing a spatial scan of the source.

1. Set Scroll Spd to 50 %, Amplitude to 70 %, Band Width to 40 %.
2. Set Film Tint to 200° (cyan), Track Count to 2.
3. Select Var Area, Unilateral profile.
4. Begin with Exposure at 0 % (left edge) and slowly sweep to 100 % (right edge).
5. Observe how the stripe width pattern changes as different parts of the source are sampled.

**Key concepts**: Sample position, unilateral encoding, spatial scanning.

---


## Tips

- **Cyan for night**: Film Tint around 180–210° gives a cool blue-grey evocative of night-scene tinting.
- **Sprockets for framing**: Enabling sprocket borders helps visually anchor the display and sells the "film strip" illusion.
- **Mix for overlay**: At 50 % mix the film-track scrolls on top of the source, creating a diegetic soundtrack effect.
- **Fast scroll**: High Scroll Spd with Var Area produces a cascading waterfall effect useful as a rhythmic visual.

---
