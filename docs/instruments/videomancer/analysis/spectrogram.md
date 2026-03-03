---
draft: true
sidebar_position: 281
slug: /instruments/videomancer/spectrogram
title: "Spectrogram"
image: /img/instruments/videomancer/spectrogram/spectrogram_hero_s1.png
description: "Spectrogram converts a video signal into a scrolling waterfall display, treating each incoming scanline as a row of \"spectral\" data that is colour-mapped, written into a framebuffer, and scrolled vertically over time."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import spectrogram_control_panel from '/img/instruments/videomancer/spectrogram/spectrogram_control_panel.png';
import spectrogram_source1_dog from '/img/instruments/videomancer/spectrogram/spectrogram_source1_dog.png';
import spectrogram_source2_runner from '/img/instruments/videomancer/spectrogram/spectrogram_source2_runner.png';
import spectrogram_source3_clouds from '/img/instruments/videomancer/spectrogram/spectrogram_source3_clouds.png';
import spectrogram_source4_pattern from '/img/instruments/videomancer/spectrogram/spectrogram_source4_pattern.png';
import spectrogram_source5_boy from '/img/instruments/videomancer/spectrogram/spectrogram_source5_boy.png';
import spectrogram_source6_paint from '/img/instruments/videomancer/spectrogram/spectrogram_source6_paint.png';
import spectrogram_hero_s1 from '/img/instruments/videomancer/spectrogram/spectrogram_hero_s1.png';
import spectrogram_hero_s2 from '/img/instruments/videomancer/spectrogram/spectrogram_hero_s2.png';
import spectrogram_hero_s3 from '/img/instruments/videomancer/spectrogram/spectrogram_hero_s3.png';
import spectrogram_hero_s4 from '/img/instruments/videomancer/spectrogram/spectrogram_hero_s4.png';
import spectrogram_hero_s5 from '/img/instruments/videomancer/spectrogram/spectrogram_hero_s5.png';
import spectrogram_hero_s6 from '/img/instruments/videomancer/spectrogram/spectrogram_hero_s6.png';
import spectrogram_ex1_s1 from '/img/instruments/videomancer/spectrogram/spectrogram_ex1_s1.png';
import spectrogram_ex1_s2 from '/img/instruments/videomancer/spectrogram/spectrogram_ex1_s2.png';
import spectrogram_ex1_s3 from '/img/instruments/videomancer/spectrogram/spectrogram_ex1_s3.png';
import spectrogram_ex1_s4 from '/img/instruments/videomancer/spectrogram/spectrogram_ex1_s4.png';
import spectrogram_ex1_s5 from '/img/instruments/videomancer/spectrogram/spectrogram_ex1_s5.png';
import spectrogram_ex1_s6 from '/img/instruments/videomancer/spectrogram/spectrogram_ex1_s6.png';
import spectrogram_ex2_s1 from '/img/instruments/videomancer/spectrogram/spectrogram_ex2_s1.png';
import spectrogram_ex2_s2 from '/img/instruments/videomancer/spectrogram/spectrogram_ex2_s2.png';
import spectrogram_ex2_s3 from '/img/instruments/videomancer/spectrogram/spectrogram_ex2_s3.png';
import spectrogram_ex2_s4 from '/img/instruments/videomancer/spectrogram/spectrogram_ex2_s4.png';
import spectrogram_ex2_s5 from '/img/instruments/videomancer/spectrogram/spectrogram_ex2_s5.png';
import spectrogram_ex2_s6 from '/img/instruments/videomancer/spectrogram/spectrogram_ex2_s6.png';
import spectrogram_ex3_s1 from '/img/instruments/videomancer/spectrogram/spectrogram_ex3_s1.png';
import spectrogram_ex3_s2 from '/img/instruments/videomancer/spectrogram/spectrogram_ex3_s2.png';
import spectrogram_ex3_s3 from '/img/instruments/videomancer/spectrogram/spectrogram_ex3_s3.png';
import spectrogram_ex3_s4 from '/img/instruments/videomancer/spectrogram/spectrogram_ex3_s4.png';
import spectrogram_ex3_s5 from '/img/instruments/videomancer/spectrogram/spectrogram_ex3_s5.png';
import spectrogram_ex3_s6 from '/img/instruments/videomancer/spectrogram/spectrogram_ex3_s6.png';

# Spectrogram

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: spectrogram_source1_dog, after: spectrogram_hero_s1 },
    { label: "Runner", before: spectrogram_source2_runner, after: spectrogram_hero_s2 },
    { label: "Clouds", before: spectrogram_source3_clouds, after: spectrogram_hero_s3 },
    { label: "Pattern", before: spectrogram_source4_pattern, after: spectrogram_hero_s4 },
    { label: "Boy", before: spectrogram_source5_boy, after: spectrogram_hero_s5 },
    { label: "Paint", before: spectrogram_source6_paint, after: spectrogram_hero_s6 },
  ]}
/>
*A waterfall display scrolls upward, painting false-colour spectral bands over the incoming video field — bright luma spikes burn yellow-white while dark regions cool to deep indigo.*

---

## Overview

Spectrogram converts a video signal into a scrolling waterfall display, treating each incoming scanline as a row of "spectral" data that is colour-mapped, written into a framebuffer, and scrolled vertically over time.  The result is a time-vs-frequency-like visualisation where the horizontal axis represents spatial position and the vertical axis represents time — the most recent data appears at the top (or bottom, depending on axis orientation) and older data scrolls away.

The program analyses the luminance of each incoming pixel, applies an adjustable gain stage and a bandwidth filter, then maps the result to a false-colour palette.  The heat palette runs from black through red and yellow to white; the spectral palette traverses violet, blue, green, yellow, and red.  Brightness, Hue, and Persistence controls further shape the visual output, and an Over Video toggle allows the spectrogram to be composited atop the original source rather than replacing it entirely.

Spectrogram borrows the visual language of scientific instrumentation — sonar waterfalls, seismographs, and audio spectrum analysers — and applies it to video, turning temporal changes in scene brightness into a permanent, scrolling historical record.

---

## Background

### Waterfall Displays

A waterfall display plots successive time slices of a signal as rows of colour-mapped data that scroll continuously in one direction.  Originated in sonar and radar (the "B-scan" display), the format was adopted by audio engineers for spectrograms — also called "sonograms" — where the horizontal axis shows frequency, the vertical axis shows time, and colour or intensity shows amplitude.  This program inverts the convention: the "frequency" axis is replaced by horizontal pixel position, and amplitude is mapped from the video luminance.

### False-Colour Mapping

Scientific visualisation often maps a scalar quantity to a colour ramp to make subtle magnitude variations visible.  The Heat palette mimics infrared thermal imaging: low values are black (cold), mid values orange-red (warm), and high values white (hot).  The Spectral palette uses the visible light spectrum ordering: violet for low, blue-green for mid, yellow-red for high.  Both palettes are implemented as threshold bands — a series of comparators quantise the luminance into discrete colour steps.

### Framebuffer Scrolling

The FPGA implements a 128×128 pixel framebuffer in block RAM.  On each vsync the scroll offset increments, so the write address for the current field advances by one row.  When the buffer wraps around, old data is overwritten — but visually the scroll appears seamless because the read offset tracks the write offset.  Gain rescales the input luminance before writing, and Bandwidth sets how many horizontal pixels from the source are averaged into each framebuffer column.

### Decay and Persistence

The Persistence control blends the newly written row with the existing framebuffer content rather than overwriting it.  This creates a trailing glow behind the leading scanline, simulating the phosphor persistence of a CRT-based spectrum analyser.  At zero persistence, each new row fully replaces the old; at maximum, the waterfall smears into a near-static heat map of long-term average brightness.

### Over Video Compositing

When the Over Video toggle is enabled, the spectrogram is alpha-blended over the original source video.  The spectrogram's brightness modulates the blend factor, so bright spectral peaks appear prominently while dark regions remain transparent, allowing the source to show through.  This creates a heads-up-display effect, overlaying analytical data on the live feed.


---

## Signal Flow

```
       Input Video (Y/U/V)
              │
     ┌────────▼─────────┐
     │  Luma Extract     │
     │  + Gain scaling   │
     └────────┬─────────┘
              │
     ┌────────▼─────────┐
     │  Bandwidth Filter │
     │  (horizontal avg) │
     └────────┬─────────┘
              │
     ┌────────▼─────────┐
     │  Scroll Offset    │
     │  (vsync counter)  │
     └────────┬─────────┘
              │
     ┌────────▼─────────┐
     │  FB Write (128×128)│
     │  with decay blend │
     └────────┬─────────┘
              │
     ┌────────▼─────────┐
     │  FB Read + Palette │
     │  (Heat / Spectral) │
     └────────┬─────────┘
              │
     ┌────────▼─────────┐
     │  Brightness + Hue │
     └────────┬─────────┘
              │
     ┌────────▼─────────┐
     │  Interpolator Mix │
     │  (dry/wet fader)  │
     └────────┬─────────┘
              │
           Output Y/U/V
```

The framebuffer is 128 columns × 128 rows of 10-bit values, requiring 4 block RAMs.  Input pixels are downsampled horizontally to fit 128 columns; vertical scrolling writes one new row per field.  The false-colour palette lookup is performed on the read path, converting the stored scalar luminance to a three-channel YUV colour.  The palette choice (Heat vs Spectral) is a per-pixel mapping, not a lookup table — it uses a chain of threshold comparators to assign colour bands.

When Scale is set to Log, the luminance value is compressed through a piecewise-linear approximation of a logarithmic curve before palette mapping, emphasising low-level detail at the expense of peak headroom.

---

## Parameter Reference

<img src={spectrogram_control_panel} alt="Videomancer front panel with Spectrogram loaded"/>
*Videomancer's front panel with Spectrogram active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Scroll Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Scroll Spd controls how quickly the waterfall advances.  At low values the scroll is slow, giving each horizontal strip of data a long visible lifetime before it scrolls off-screen.  At high values the waterfall races upward (or downward), compressing the time history and emphasising rapid changes.  The scroll counter increments by the Scroll Spd value at each vsync, so the rate is directly proportional.

---

#### Knob 2 — Gain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Gain rescales the input luminance before it is written to the framebuffer.  Low Gain produces a dim, subtle waterfall even from bright sources.  High Gain saturates the palette with modest input levels, making faint luminance variations visible as vivid colour changes.  For maximum dynamic range, set Gain so that the brightest parts of the source just reach the top of the colour ramp without clipping.

---

#### Knob 3 — Bandwidth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Bandwidth sets the horizontal averaging window.  At minimum, each framebuffer column represents a narrow strip of the source — essentially a one-to-one spatial mapping.  Increasing Bandwidth widens the averaging, blurring spatial detail into broader horizontal bands.  At maximum the entire scanline is averaged into a single column, producing a flat vertical stripe whose colour tracks the overall scene brightness.

---

#### Knob 4 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Brightness adds a uniform offset to the palette-mapped output, lifting dark regions and shifting the entire waterfall toward the bright end of the colour ramp.  At zero, dark regions remain black; at maximum, even the coolest palette bands glow visibly.  Useful for maintaining visibility of low-energy signals on a dim display.

---

#### Knob 5 — Hue
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

Hue rotates the colour of the false-colour palette output, shifting the entire spectrum around the colour wheel.  On the Heat palette this transforms the red-yellow gradient into green-cyan or blue-magenta variants.  On the Spectral palette it rotates the rainbow ordering.

---

#### Knob 6 — Persist
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Persist controls the temporal decay blend.  At zero, each new scanline fully replaces the previous framebuffer row — the waterfall is crisp and each historical row is independent.  Increasing Persist blends the new data with the existing content, creating trailing afterglow.  At maximum the waterfall smears into a near-static accumulation of long-term average luminance.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Heat | Spectral |
| **8 — Scale** | Linear | Log |
| **9 — Axis** | Vertical | Horizontal |
| **10 — Over Video** | Off | On |
| **11 — Bypass** | Off | On |

Palette and Scale define the visual character of the waterfall.  Axis selects whether it scrolls vertically or horizontally.  Over Video and Bypass provide compositing and passthrough options.  The most impactful combination is Palette + Scale: Heat/Log emphasises low-level detail in warm tones, while Spectral/Linear preserves full dynamic range in rainbow colours.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the wet spectrogram output.  At zero, pure source video; at maximum, pure spectrogram.

---

## Guided Exercises

These exercises demonstrate Spectrogram's waterfall display in different configurations, from scientific instrumentation to artistic overlay.

### Exercise 1: Classic Thermal Waterfall

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: spectrogram_source1_dog, after: spectrogram_ex1_s1 },
    { label: "Runner", before: spectrogram_source2_runner, after: spectrogram_ex1_s2 },
    { label: "Clouds", before: spectrogram_source3_clouds, after: spectrogram_ex1_s3 },
    { label: "Pattern", before: spectrogram_source4_pattern, after: spectrogram_ex1_s4 },
    { label: "Boy", before: spectrogram_source5_boy, after: spectrogram_ex1_s5 },
    { label: "Paint", before: spectrogram_source6_paint, after: spectrogram_ex1_s6 },
  ]}
/>
*Classic Thermal Waterfall — simulated result across source images.*
**Source**: A camera source with a mix of slowly changing and rapidly flickering elements — a person moving against a static background works well.

**Objective**: Produce a classic infrared-style waterfall showing temporal brightness changes as colour bands.

1. Set Scroll Spd to 40 %, Gain to 60 %, Bandwidth to 30 %.
2. Set Brightness to 20 % and Persist to 30 %.
3. Select Heat palette, Linear scale, Vertical axis.
4. Observe the waterfall building up as the scene evolves — static regions produce horizontal streaks, moving objects create slanted trails.
5. Increase Scroll Spd and see the history compress; decrease it and the waterfall stretches out.

**Key concepts**: - Heat palette maps luminance to black → red → yellow → white
- Scroll speed determines the time compression of the waterfall
- Persistence adds temporal blurring to the scrolling rows

---

### Exercise 2: Spectral Logarithmic Analysis

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: spectrogram_source1_dog, after: spectrogram_ex2_s1 },
    { label: "Runner", before: spectrogram_source2_runner, after: spectrogram_ex2_s2 },
    { label: "Clouds", before: spectrogram_source3_clouds, after: spectrogram_ex2_s3 },
    { label: "Pattern", before: spectrogram_source4_pattern, after: spectrogram_ex2_s4 },
    { label: "Boy", before: spectrogram_source5_boy, after: spectrogram_ex2_s5 },
    { label: "Paint", before: spectrogram_source6_paint, after: spectrogram_ex2_s6 },
  ]}
/>
*Spectral Logarithmic Analysis — simulated result across source images.*
**Source**: A high-dynamic-range source — window with daylight behind a dimly lit interior, or a candle in a dark room.

**Objective**: Use log scale and spectral palette to reveal low-level luminance detail.

1. Set Gain to 50 %, Bandwidth to 10 % for detailed spatial resolution.
2. Switch Scale to Log and Palette to Spectral.
3. Observe how dim areas that were invisible on the Heat/Linear display now appear as blue-violet bands.
4. Adjust Gain upward and watch the mid-range expand from green into yellow.
5. Compare by toggling Scale back to Linear — notice how the dark-region detail collapses.

**Key concepts**: - Log scale compresses peaks and expands low-level detail
- Spectral palette provides maximum chrominance separation
- Bandwidth at low values preserves spatial structure in the waterfall

---

### Exercise 3: Heads-Up Overlay

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: spectrogram_source1_dog, after: spectrogram_ex3_s1 },
    { label: "Runner", before: spectrogram_source2_runner, after: spectrogram_ex3_s2 },
    { label: "Clouds", before: spectrogram_source3_clouds, after: spectrogram_ex3_s3 },
    { label: "Pattern", before: spectrogram_source4_pattern, after: spectrogram_ex3_s4 },
    { label: "Boy", before: spectrogram_source5_boy, after: spectrogram_ex3_s5 },
    { label: "Paint", before: spectrogram_source6_paint, after: spectrogram_ex3_s6 },
  ]}
/>
*Heads-Up Overlay — simulated result across source images.*
**Source**: A live camera feed with moderate motion.

**Objective**: Overlay the spectrogram on the source video for a heads-up-display effect.

1. Enable Over Video and set Mix to 70 %.
2. Set Gain to 40 %, Persist to 50 %, Palette to Heat.
3. Observe the waterfall burning over the live video — bright regions of the spectrogram tint the source.
4. Increase Persist to see the waterfall smear and accumulate over the source.
5. Adjust Hue to shift the overlay colour and find a tint that complements the source content.

**Key concepts**: - Over Video composites the spectrogram as a translucent overlay
- Persistence affects how long overlay data remains visible on the source
- Hue rotation allows colour-matching the overlay to the source

---


## Tips

- **Gain calibration:** Set Gain so that the brightest source regions just reach the top of the colour ramp — this maximises dynamic range without clipping.
- **Slow scroll for installations:** A low Scroll Spd produces a meditative, slowly evolving tapestry of colour bands — ideal for gallery or ambient use.
- **Log for night scenes:** Logarithmic scale reveals detail in shadows that would be invisible on the linear Heat display.
- **Bandwidth for abstraction:** At maximum Bandwidth the entire scanline averages into a single column, transforming the waterfall into an abstract vertical colour stripe — a form of temporal colour coding.
- **Hue for mood:** Rotating Hue 180° on the Heat palette turns it into a cool cyan-blue gradient, completely changing the emotional tone without altering the data.
- **Over Video for analysis:** Use the overlay mode to spot brightness patterns in a live camera feed — motion trails, flickering lights, and gradual exposure changes all become visible.
- **Pair with Slit Scan:** Feeding Spectrogram's output into Slit Scan creates a double-temporal effect — the spectrogram's scrolling time history gets further time-sliced and accumulated.

---
