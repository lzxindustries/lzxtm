---
draft: true
sidebar_position: 160
slug: /instruments/videomancer/kinescope
title: "Kinescope"
image: /img/instruments/videomancer/kinescope/kinescope_hero_s1.png
description: "Before videotape existed, the only way to preserve a live television broadcast was to point a film camera at a television monitor and record the screen."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import kinescope_control_panel from '/img/instruments/videomancer/kinescope/kinescope_control_panel.png';
import kinescope_source1_sunset from '/img/instruments/videomancer/kinescope/kinescope_source1_sunset.png';
import kinescope_source2_car from '/img/instruments/videomancer/kinescope/kinescope_source2_car.png';
import kinescope_source3_elephant from '/img/instruments/videomancer/kinescope/kinescope_source3_elephant.png';
import kinescope_source4_pattern from '/img/instruments/videomancer/kinescope/kinescope_source4_pattern.png';
import kinescope_source5_woman from '/img/instruments/videomancer/kinescope/kinescope_source5_woman.png';
import kinescope_source6_berries from '/img/instruments/videomancer/kinescope/kinescope_source6_berries.png';
import kinescope_hero_s1 from '/img/instruments/videomancer/kinescope/kinescope_hero_s1.png';
import kinescope_hero_s2 from '/img/instruments/videomancer/kinescope/kinescope_hero_s2.png';
import kinescope_hero_s3 from '/img/instruments/videomancer/kinescope/kinescope_hero_s3.png';
import kinescope_hero_s4 from '/img/instruments/videomancer/kinescope/kinescope_hero_s4.png';
import kinescope_hero_s5 from '/img/instruments/videomancer/kinescope/kinescope_hero_s5.png';
import kinescope_hero_s6 from '/img/instruments/videomancer/kinescope/kinescope_hero_s6.png';
import kinescope_ex1_s1 from '/img/instruments/videomancer/kinescope/kinescope_ex1_s1.png';
import kinescope_ex1_s2 from '/img/instruments/videomancer/kinescope/kinescope_ex1_s2.png';
import kinescope_ex1_s3 from '/img/instruments/videomancer/kinescope/kinescope_ex1_s3.png';
import kinescope_ex1_s4 from '/img/instruments/videomancer/kinescope/kinescope_ex1_s4.png';
import kinescope_ex1_s5 from '/img/instruments/videomancer/kinescope/kinescope_ex1_s5.png';
import kinescope_ex1_s6 from '/img/instruments/videomancer/kinescope/kinescope_ex1_s6.png';
import kinescope_ex2_s1 from '/img/instruments/videomancer/kinescope/kinescope_ex2_s1.png';
import kinescope_ex2_s2 from '/img/instruments/videomancer/kinescope/kinescope_ex2_s2.png';
import kinescope_ex2_s3 from '/img/instruments/videomancer/kinescope/kinescope_ex2_s3.png';
import kinescope_ex2_s4 from '/img/instruments/videomancer/kinescope/kinescope_ex2_s4.png';
import kinescope_ex2_s5 from '/img/instruments/videomancer/kinescope/kinescope_ex2_s5.png';
import kinescope_ex2_s6 from '/img/instruments/videomancer/kinescope/kinescope_ex2_s6.png';
import kinescope_ex3_s1 from '/img/instruments/videomancer/kinescope/kinescope_ex3_s1.png';
import kinescope_ex3_s2 from '/img/instruments/videomancer/kinescope/kinescope_ex3_s2.png';
import kinescope_ex3_s3 from '/img/instruments/videomancer/kinescope/kinescope_ex3_s3.png';
import kinescope_ex3_s4 from '/img/instruments/videomancer/kinescope/kinescope_ex3_s4.png';
import kinescope_ex3_s5 from '/img/instruments/videomancer/kinescope/kinescope_ex3_s5.png';
import kinescope_ex3_s6 from '/img/instruments/videomancer/kinescope/kinescope_ex3_s6.png';

# Kinescope

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: kinescope_source1_sunset, after: kinescope_hero_s1 },
    { label: "Car", before: kinescope_source2_car, after: kinescope_hero_s2 },
    { label: "Elephant", before: kinescope_source3_elephant, after: kinescope_hero_s3 },
    { label: "Pattern", before: kinescope_source4_pattern, after: kinescope_hero_s4 },
    { label: "Woman", before: kinescope_source5_woman, after: kinescope_hero_s5 },
    { label: "Berries", before: kinescope_source6_berries, after: kinescope_hero_s6 },
  ]}
/>
*Kinescope simulating the CRT-to-film transfer process with rolling bar interference, phosphor bloom, film grain, and vignette darkening.*

---

## Overview

Before videotape existed, the only way to preserve a live television broadcast was to point a film camera at a television monitor and record the screen. This process was called a **kinescope** (or "kine"), and it introduced a distinctive set of artifacts. The film camera's mechanical shutter was rarely synchronized perfectly with the CRT's electronic scanning, producing a dark horizontal band — the **rolling bar** — that drifted vertically through the image. The CRT's phosphors bloomed in highlights, the film stock added its own grain structure, and the camera lens darkened the corners through natural vignetting.

Kinescope recreates these artifacts as a multi-stage video processing chain. The rolling bar is simulated as a soft-edged brightness attenuation that moves vertically through the frame at an adjustable speed. Phosphor bloom adds a glow to pixels above a brightness threshold. Film grain injects LFSR-generated noise with adjustable intensity. Vignette applies a corner-darkening function based on distance from the screen center. Frame flicker adds a per-frame random brightness variation. The result convincingly evokes the look of telerecordings from the 1950s and 1960s — the primary visual record of early television's golden age.

---

## Quick Start

1. **Slow bar, low depth for subtlety**: A barely visible, slowly drifting bar with 15–20% depth creates a subliminal kinescope feel.
2. **Grain scale matters**: 10–20% grain provides texture without dominating. Above 40%, the grain becomes the primary visual element.
3. **Bloom needs highlights**: Bloom is only visible on bright content. On already-dark footage, it does nothing.

---

## Background

### What Is a Kinescope Recording?

A **kinescope** is a film recording of a television broadcast made by pointing a motion picture camera at a CRT monitor. Before magnetic videotape became practical in the late 1950s, kinescopes were the only method of preserving live television programs. Famous early kinescopes include recordings of *I Love Lucy* rehearsals, *The Ed Sullivan Show*, and BBC broadcasts of the 1953 Coronation. Because the film camera operated at 24 fps while the television scanned at 50 or 60 fields per second, and because the camera's shutter exposure didn't perfectly match the CRT refresh, kinescopes carry distinctive artifacts — most notably the rolling bar caused by the phase difference between camera and monitor refresh rates.

### What Is a Rolling Bar?

The CRT phosphors are refreshed line by line from top to bottom. At any given instant, some portion of the screen is brighter (recently refreshed) and some is dimmer (phosphors decaying). When a film camera exposes a frame, its shutter captures the screen at a moment when the bright band is at a specific vertical position. If the camera and CRT are not perfectly synchronized, the bright band appears at a *different* position on each successive film frame, creating the illusion of a dark bar rolling continuously through the image. Kinescope simulates this with a bar attenuation function whose vertical position advances each frame.

### What Is Phosphor Bloom?

CRT phosphors emit light proportional to the electron beam current. At very high beam currents (bright areas of the image), the phosphor spot size increases — the beam "blooms" beyond its intended area, creating a soft glow around highlights. This effect is characteristic of direct-view CRT monitors and is particularly visible in kinescope recordings where the film captures the actual phosphor luminescence. Kinescope simulates bloom by adding a brightness boost to pixels that exceed a threshold.

### What Is Film Grain?

All photographic film has a granular structure caused by the random distribution of silver halide crystals in the emulsion. When a kinescope camera records the CRT image, the film grain is superimposed on the electronic picture, adding a fine noise texture that varies from frame to frame. The grain is most visible in mid-tones and shadows. Kinescope uses an LFSR (linear feedback shift register) to generate pseudo-random noise that mimics the statistical character of film grain.


---

## Signal Flow

Y Channel → U/V Channels → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Rolling Bar           (distance from bar center → attenuation)
│   ├─ 2. Phosphor Bloom        (if Y > 512: additive glow)
│   ├─ 3. Film Grain            (LFSR16 noise × grain_amount, optional)
│   ├─ 4. Vignette              (Chebyshev distance darkening, optional)
│   ├─ 5. Brightness Offset     (DC shift)
│   └─ 6. Frame Flicker         (per-frame random offset, optional)
│
├── U/V Channels ───────────────────────────────────────────────
│   └─ Pass-through (no chroma processing)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The effects chain is strictly serial — each stage modifies the luminance before the next stage sees it. The rolling bar operates first, attenuating brightness based on vertical distance from the bar position. Bloom then expands highlights in the already-attenuated signal (so the bar can modulate which regions bloom). Grain is added after bloom, sitting on top of both the bar and bloom effects. Vignette is applied last in the spatial domain, darkening corners of the entire processed image. Finally, brightness and flicker apply global shifts. This ordering ensures the artifacts layer naturally — grain sits on top of the bar, and vignette darkens the grain-textured result.

---

## Parameter Reference

<img src={kinescope_control_panel} alt="Videomancer front panel with Kinescope loaded"/>
*Videomancer's front panel with Kinescope active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Bar Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

At 0%, the bar is extremely narrow — a thin dark line rolling through the frame. At higher values, the bar widens to cover a larger vertical portion of the image. Very wide bars (70%+) can darken most of the frame, with only a narrow bright strip visible as the bar passes. The bar edges are soft, transitioning gradually between full brightness and full attenuation. Internally, controls the width of the rolling bar as a fraction of the frame height.

---

#### Knob 2 — Bar Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

At 0%, the bar is stationary. At low values, the bar drifts slowly through the frame, mimicking a nearly-synchronized kinescope camera. At higher values, the bar races through the frame multiple times per second, creating rapid flickering characteristic of badly mismatched camera/CRT timing. The most realistic kinescope look uses a slow-to-moderate speed. Internally, sets the speed at which the bar position advances per frame.

---

#### Knob 3 — Bar Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, the bar is invisible. At moderate values, the bar creates a subtle brightness variation. At high values, the bar creates deep darkening, nearly blacking out the affected region. This control determines the severity of the kinescope artifact — higher values suggest a greater synchronization mismatch. Internally, controls the depth of the bar's attenuation — how much the bar darkens the image.

---

#### Knob 4 — Grain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

At 0%, no grain is added. At moderate values, a subtle texture appears across the image, mimicking medium-speed film stock. At maximum, the grain becomes coarse and dominant, suggesting high-speed push-processed film. The grain pattern changes every pixel (LFSR16 pseudo-random) and varies from frame to frame with seed advancement. Internally, sets the intensity of the film grain noise.

---

#### Knob 5 — Bloom
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

At 0%, no bloom. At moderate values, highlights above mid-gray receive a soft additive glow. At high values, the bloom significantly expands, pushing highlights toward clipping and creating a soft, glowing quality characteristic of direct-view CRT monitors. Bloom is purely additive — it can only brighten, never darken. Internally, controls the intensity of the phosphor bloom effect.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC offset to the final output luminance. At center, no offset. Above center, the image brightens. Below center, it darkens. This control compensates for the overall darkening caused by the rolling bar and vignette, or creatively adjusts the final exposure.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Bar Dir** | Down | Up |
| **8 — Grain** | Off | On |
| **9 — Vignette** | Off | On |
| **10 — Flicker** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 enable or configure independent elements of the kinescope simulation. Bar Dir sets the rolling direction. Grain enables film texture. Vignette enables lens darkening. Flicker enables per-frame brightness variation. Bypass provides instant comparison.

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

Routes the unprocessed input signal directly to the output, bypassing all Kinescope processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Kinescope-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from the fundamental rolling bar to a complete kinescope simulation with all artifacts layered together.

### Exercise 1: The Rolling Bar

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: kinescope_source1_sunset, after: kinescope_ex1_s1 },
    { label: "Car", before: kinescope_source2_car, after: kinescope_ex1_s2 },
    { label: "Elephant", before: kinescope_source3_elephant, after: kinescope_ex1_s3 },
    { label: "Pattern", before: kinescope_source4_pattern, after: kinescope_ex1_s4 },
    { label: "Woman", before: kinescope_source5_woman, after: kinescope_ex1_s5 },
    { label: "Berries", before: kinescope_source6_berries, after: kinescope_ex1_s6 },
  ]}
/>
*The Rolling Bar — simulated result across source images.*
**Source**: Any footage — the rolling bar is clearly visible against any content.

**What You'll Create**: Understand how the rolling bar width, speed, and depth interact to create the fundamental kinescope artifact.

1. **Basic bar**: Set Bar Width ~50%, Bar Speed ~30%, Bar Depth ~80%. A dark band rolls slowly down the frame.
2. **Width**: Sweep Bar Width from narrow (10%) to wide (90%). Narrow bars look like scanning lines; wide bars dominate the frame.
3. **Speed**: Increase Bar Speed. The bar accelerates, creating faster flickering. Reduce to ~10% for the slowest, most cinematic drift.
4. **Depth**: Reduce Bar Depth to ~30%. The bar becomes a subtle brightness modulation rather than a deep shadow.
5. **Direction**: Toggle Bar Dir (Switch 7) to reverse the rolling direction.

**Key concepts**: The rolling bar is caused by phase mismatch between camera shutter and CRT refresh, width controls bar coverage, speed controls drift rate, depth controls darkening intensity

---

### Exercise 2: Film Texture and Bloom

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: kinescope_source1_sunset, after: kinescope_ex2_s1 },
    { label: "Car", before: kinescope_source2_car, after: kinescope_ex2_s2 },
    { label: "Elephant", before: kinescope_source3_elephant, after: kinescope_ex2_s3 },
    { label: "Pattern", before: kinescope_source4_pattern, after: kinescope_ex2_s4 },
    { label: "Woman", before: kinescope_source5_woman, after: kinescope_ex2_s5 },
    { label: "Berries", before: kinescope_source6_berries, after: kinescope_ex2_s6 },
  ]}
/>
*Film Texture and Bloom — simulated result across source images.*
**Source**: Footage with a mix of highlights and shadows — talking head against a bright background, or a window scene.

**What You'll Create**: Layer film grain and phosphor bloom onto the rolling bar for a more complete kinescope look.

1. **Base bar**: Set a moderate rolling bar (Width ~40%, Speed ~25%, Depth ~60%).
2. **Add grain**: Enable Grain (Switch 8). Set Grain intensity to ~30%. A fine noise texture appears across the image.
3. **Bloom highlights**: Increase Bloom to ~40%. Bright areas (windows, lamps, reflections) develop a soft glow.
4. **Balance**: Adjust Brightness to compensate for the overall darkening from the bar and grain.
5. **Increase grain**: Push Grain to ~60% for a coarser, more obviously filmic texture. Note how the grain is visible within the rolling bar's dark zone.

**Key concepts**: Film grain adds photographic texture, bloom simulates phosphor glow in highlights, grain and bloom layer on top of the bar attenuation

---

### Exercise 3: Full Kinescope Simulation

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: kinescope_source1_sunset, after: kinescope_ex3_s1 },
    { label: "Car", before: kinescope_source2_car, after: kinescope_ex3_s2 },
    { label: "Elephant", before: kinescope_source3_elephant, after: kinescope_ex3_s3 },
    { label: "Pattern", before: kinescope_source4_pattern, after: kinescope_ex3_s4 },
    { label: "Woman", before: kinescope_source5_woman, after: kinescope_ex3_s5 },
    { label: "Berries", before: kinescope_source6_berries, after: kinescope_ex3_s6 },
  ]}
/>
*Full Kinescope Simulation — simulated result across source images.*
**Source**: Black-and-white or low-saturation footage for the most authentic kinescope look.

**What You'll Create**: Combine all five kinescope elements for a convincing telerecording simulation.

1. **All layers**: Set moderate Rolling Bar (Width ~45%, Speed ~20%, Depth ~50%), Grain ~25%, Bloom ~35%.
2. **Enable vignette**: Switch on Vignette (Switch 9). The corners darken, framing the image the way a real kinescope camera lens would.
3. **Enable flicker**: Switch on Flicker (Switch 10). A subtle per-frame brightness pulse appears, mimicking camera shutter variation.
4. **Adjust brightness**: Set Brightness slightly above center (~55%) to compensate for the cumulative darkening of bar, vignette, and flicker.
5. **Final mix**: Adjust Mix fader to ~85% to let a hint of the clean original through, simulating a higher-quality kinescope with better camera alignment.
6. **Compare**: Toggle Bypass for before/after. The processed image should evoke the look of a 1950s telerecording.

**Key concepts**: All artifacts layer cumulatively, vignette simulates lens optics, flicker simulates shutter variation, partial mix simulates recording quality

---


## Tips

- **Vignette frames the image**: Even without other effects, the vignette alone adds a cinematic lens quality.
- **Flicker is subtle by design**: The per-frame brightness variation is intentionally small. It's most visible on dark scenes.
- **Black-and-white sells the effect**: For the most convincing kinescope look, feed desaturated or monochrome input. Kinescopes of color broadcasts existed but were rare.
- **Mix for quality**: Lower Mix values simulate a better-quality kinescope where the camera was more precisely aligned with the monitor.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bloom** | The spreading of a CRT's phosphor spot at high beam current, creating a soft glow around bright areas. |
| **Chebyshev Distance** | The maximum of horizontal and vertical distance; used here for the vignette falloff function. |
| **CRT** | Cathode Ray Tube; a display technology using an electron beam to excite phosphors on a glass screen. |
| **Film Grain** | The random texture in photographic film caused by the distribution of silver halide crystals in the emulsion. |
| **Kinescope** | A film recording made by pointing a movie camera at a television monitor, the primary preservation method for live TV before videotape. |
| **LFSR** | Linear Feedback Shift Register; a digital circuit that generates a pseudo-random bit sequence for noise generation. |
| **Rolling Bar** | A dark horizontal band that appears to drift through the image when a film camera is not synchronized with a CRT's refresh rate. |
| **Vignette** | Darkening of the image corners and edges caused by lens light falloff, characteristic of camera optics. |

---
