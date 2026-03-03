---
draft: true
sidebar_position: 304
slug: /instruments/videomancer/tidepool
title: "Tidepool"
image: /img/instruments/videomancer/tidepool/tidepool_hero.png
description: "Drop a stone into still water and concentric circles expand outward."
---

import tidepool_hero from '/img/instruments/videomancer/tidepool/tidepool_hero.png';
import tidepool_animation from '/img/instruments/videomancer/tidepool/tidepool_animation.gif';
import tidepool_control_panel from '/img/instruments/videomancer/tidepool/tidepool_control_panel.png';
import tidepool_exercise1_result from '/img/instruments/videomancer/tidepool/tidepool_exercise1_result.gif';
import tidepool_exercise2_result from '/img/instruments/videomancer/tidepool/tidepool_exercise2_result.gif';
import tidepool_exercise3_result from '/img/instruments/videomancer/tidepool/tidepool_exercise3_result.gif';

# Tidepool

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={tidepool_hero} alt="Tidepool hero image"/>
*Tidepool generating four-source concentric ripple interference with constructive and destructive wave patterns overlaid on a live video feed.*
<img src={tidepool_animation} alt="Tidepool animated output"/>
*Tidepool output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Drop a stone into still water and concentric circles expand outward. Drop two stones and the circles overlap — where wave crests align, they reinforce; where a crest meets a trough, they cancel. This interference pattern is one of the most fundamental phenomena in physics, appearing everywhere from ocean waves to light diffraction to quantum mechanics. Tidepool brings this phenomenon into the video domain by simulating up to four point-source wave emitters whose concentric ripples interfere with each other across the frame.

Each source emits expanding rings computed via Manhattan-distance triangle waves. As the waves overlap, constructive interference produces bright fringes and destructive interference produces dark nodes. The resulting pattern is a continuously evolving lattice of light and shadow that responds to six parameter controls. Source positions are animated by independent DDS phase accumulators with irrational frequency ratios, ensuring the interference pattern never exactly repeats — it drifts, morphs, and breathes organically even though every pixel is computed from pure integer arithmetic.

In Overlay mode, the ripple amplitude modulates the input video brightness, embedding the interference lattice into the source material. In Replace mode, the ripples become the sole content — a self-illuminated pattern generator. The Color toggle adds rainbow chrominance derived from the wave phase, and the Depth control scales the overall effect intensity from subtle shimmer to full-contrast geometric structures.

---

## Background

### Wave Interference and Superposition

When two or more wave sources emit at similar frequencies, the waves they produce overlap and combine. At points where crests coincide, the amplitudes add (constructive interference), creating bright maxima. At points where a crest meets a trough, the amplitudes partially or fully cancel (destructive interference), creating dark minima or nodes. The resulting spatial pattern of reinforcement and cancellation is called an interference pattern. Tidepool computes this superposition numerically: each source generates a triangle wave as a function of distance, and the per-pixel sum of all active sources determines the final brightness.

### Triangle Waves as Approximation

True circular ripples are sinusoidal — each wavefront follows a cosine profile as a function of radial distance. Computing sine or cosine on an FPGA without dedicated DSP blocks requires lookup tables or CORDIC algorithms. Tidepool uses a simpler approach: a triangle wave function that maps a 12-bit unsigned phase to a signed 10-bit amplitude. The triangle wave approximates a sine wave closely enough to produce recognizable interference fringes while requiring only bit manipulation and conditional negation. The four quadrants of the phase map to rising positive, falling positive, rising negative, and falling negative segments.

### Manhattan Distance and Concentric Rings

True circular ripples require Euclidean distance (square root of the sum of squares), which is expensive in combinational FPGA logic. Tidepool uses Manhattan distance (|dx| + |dy|) instead. Manhattan distance produces diamond-shaped contours rather than circles, but at the spatial frequencies typically used for video effects, the diamond shape is barely perceptible — the eye registers the overall concentric ring structure rather than the precise contour geometry. This tradeoff saves hundreds of LUTs compared to a square-root implementation.

### DDS Source Animation

Each source's position is driven by a pair of DDS (Direct Digital Synthesis) phase accumulators — one for X, one for Y. The phase accumulators are incremented each frame by unique frequency constants. The accumulated phase passes through a triangle wave function, which maps it to a smooth oscillation. The triangle wave output is then scaled by the Spread parameter and offset from the frame center (640, 360) to produce the source's pixel coordinates.

The frequency constants are chosen to be co-prime and irrational in ratio: (137, 193), (211, 157), (173, 229), (251, 181). Because no two sources share a common frequency, their position trajectories never synchronize — the pattern continuously evolves without repeating on any human-observable timescale.

### Moire Patterns in Multi-Source Interference

When two sets of concentric rings overlap with slightly different spatial frequencies, a secondary large-scale pattern emerges — the Moire effect. Tidepool's multi-source interference naturally produces Moire fringes as a byproduct of wave superposition. The Wavelength control changes the spatial frequency of all sources simultaneously, but the frequency ratios between sources remain fixed by the DDS constants, so the Moire patterns shift and scale as Wavelength is swept.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Source Position DDS ───────────────────────────────────────
│   ├─ 4 × (phase_x, phase_y) accumulators
│   ├─ Increment rates: unique per source (co-prime constants)
│   ├─ Triangle wave on phase → position offset
│   └─ Scale by Spread → center at (640, 360)
│
├── Stage 1: dx/dy for sources 0, 1 ──────────────────────────
│   └─ |pixel_x − src_x|, |pixel_y − src_y|
│
├── Stage 2: dist(0,1) + dx/dy for sources 2, 3 ──────────────
│   └─ Manhattan distance = |dx| + |dy|
│
├── Stage 3: dist(2,3) + triangle_wave for sources 0, 1 ──────
│   └─ wave(i) = tri(dist(i) << wavelength_shift)
│
├── Stage 4: triangle_wave for sources 2, 3 + sum ─────────────
│   └─ wave_sum = Σ active source waves (signed sum)
│
├── Stage 5: Scale + Compose ──────────────────────────────────
│   ├─ abs_sum = |wave_sum|
│   ├─ scaled = abs_sum × depth / 1024
│   ├─ Invert: scaled = 1023 − scaled
│   ├─ Replace mode: Y = scaled; UV = wave-derived or mid
│   └─ Overlay mode: Y = input_Y × scaled / 1024; UV = input
│
├── Interpolator ──────────────────────────────────────────────
│   └─ Mix(dry=delayed_input, wet=composite, t=mix_amount)
│
└── Bypass Mux ────────────────────────────────────────────────
    └─ bypass=1 → delayed input; bypass=0 → mix result
```

The key architectural feature is that distance computation and triangle wave evaluation are split across pipeline stages to meet timing. Sources 0 and 1 compute dx/dy in stage 1 and distance in stage 2, while sources 2 and 3 compute dx/dy in stage 2 and distance in stage 3. This interleaving keeps the critical path short while processing all four sources within the pipeline depth.

The triangle wave function is the waveshaping core. It maps a 12-bit unsigned phase angle into a signed 10-bit amplitude by mirroring and folding the phase through four quadrants. The wavelength parameter controls how many cycles of this triangle wave fit across a given distance — higher wavelength values left-shift the distance before the triangle lookup, compressing more cycles into the same physical space.

---

## Parameter Reference

<img src={tidepool_control_panel} alt="Videomancer front panel with Tidepool loaded"/>
*Videomancer's front panel with Tidepool active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Wavelength
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial frequency of the ripple rings. The register value is right-shifted by 7 and clamped to 0–8 to derive a left-shift amount applied to the distance before the triangle wave lookup. At 0 the rings are very widely spaced — only one or two cycles visible across the full frame. At maximum the rings are tightly packed, producing fine concentric line patterns. Higher values create more visible Moire interference where sources overlap.

---

#### Knob 2 — Drift Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the animation speed of the source positions. This value scales the DDS frequency constants before they are added to the phase accumulators each frame. At 0 the sources are frozen in place. At maximum they drift rapidly, creating a constantly evolving interference pattern. Because each source has unique frequency constants, increasing Drift Sp accelerates all sources proportionally while preserving their irrational frequency ratios.

---

#### Knob 3 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls amplitude attenuation with distance from each source. In the VHDL, the decay parameter is available for future use in scaling the wave amplitude as a function of distance, simulating the natural falloff of ripples in water. The current implementation applies uniform amplitude regardless of distance, but the register is mapped and ready for decay scaling.

---

#### Knob 4 — Sources
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Selects how many wave sources are active: 1, 2, 3, or 4. The register is divided into four equal zones (0–255 = 1 source, 256–511 = 2, 512–767 = 3, 768–1023 = 4). With a single source, the output is simple concentric rings. Each additional source adds another set of rings, and the interference between them creates progressively more complex patterns — from simple two-slit fringes to intricate four-source lattice structures.

---

#### Knob 5 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how far the source positions wander from the frame center. The triangle-wave-modulated DDS output is multiplied by this value and divided by 512 before being added to the center coordinates (640, 360). At 0 all sources collapse to the center, producing identical overlapping rings (constructive reinforcement). At maximum the sources roam widely, producing asymmetric interference with constantly shifting node positions.

---

#### Knob 6 — Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the overall brightness amplitude of the ripple effect. The absolute value of the summed wave is multiplied by this register and right-shifted by 10. At 0 the effect is invisible (zero amplitude). At maximum the ripples span the full 0–1023 luma range. In Overlay mode, this determines how strongly the interference pattern modulates the input video. In Replace mode, it controls the contrast of the standalone ripple output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Color** | Mono | Rainbow |
| **9 — Render** | Overlay | Replace |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control animation enable, color mode, render mode, luma inversion, and bypass. Animate and Render dramatically change the character of the output: Animate frozen + Overlay produces a static spatial filter on the input; Animate on + Replace produces a self-animating pattern generator. Color adds chrominance derived from the wave phase values.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfade between the unprocessed input (dry) and the fully processed ripple output (wet). At 0% the output is pure dry signal. At 100% the output is fully processed. Intermediate values blend the interference pattern transparently over the source video.

---

## Guided Exercises

These exercises progress from simple single-source rings to complex four-source interference with animation and color. Each exercise builds on the previous, gradually engaging more of the wave engine.

### Exercise 1: Concentric Rings

<img src={tidepool_exercise1_result} alt="Concentric Rings result"/>
*Concentric Rings — simulated result across source images.*
**Objective**: Understand how a single wave source produces concentric rings and how Wavelength and Depth control their appearance.

1. **Single source**: Set Sources to 1 (fully counter-clockwise). A single set of concentric diamond-shaped rings appears centered on the frame.
2. **Wavelength sweep**: Slowly increase Wavelength from minimum. Watch the rings compress — more cycles appear per unit distance.
3. **Depth sweep**: Increase Depth to strengthen the ring contrast. At maximum, bright and dark rings are at full video levels.
4. **Overlay mode**: With Render set to Overlay, the rings modulate the input video — bright source regions are sculpted by the ring pattern.
5. **Replace mode**: Switch Render to Replace. The input video vanishes; only the ring pattern remains as self-illuminated content.

**Key concepts**: Concentric rings are triangle waves as a function of Manhattan distance, Wavelength controls spatial frequency, Depth controls amplitude, Overlay modulates video while Replace generates standalone patterns

---

### Exercise 2: Two-Source Interference

<img src={tidepool_exercise2_result} alt="Two-Source Interference result"/>
*Two-Source Interference — simulated result across source images.*
**Objective**: Observe constructive and destructive interference between two wave sources.

1. **Start from Exercise 1 settings** with Wavelength at ~50% and Depth at ~60%.
2. **Add second source**: Increase Sources to 2. A second set of rings appears, centered at a different position.
3. **Observe interference**: Between the two sources, bright and dark fringes form where the ring patterns overlap. These are the hallmark of two-source interference.
4. **Enable animation**: Turn Animate on, set Drift Sp to ~30%. The sources begin to drift, and the interference fringes continuously reshape.
5. **Increase Spread**: Sweep Spread higher. The sources wander further apart, stretching the interference zone.
6. **Enable color**: Switch Color to Rainbow. The interference fringes gain chromatic variation — different spatial regions display different hues.

**Key concepts**: Two-source interference creates alternating bright/dark fringes, source animation via DDS creates continuously evolving patterns, Spread controls source separation distance

---

### Exercise 3: Full Four-Source Lattice

<img src={tidepool_exercise3_result} alt="Full Four-Source Lattice result"/>
*Full Four-Source Lattice — simulated result across source images.*
**Objective**: Explore the rich interference lattice produced by four animated sources with color and mode variations.

1. **Four sources**: Set Sources to 4 (fully clockwise). Four independent ring patterns overlap, creating a complex lattice.
2. **Moderate wavelength**: Set Wavelength to ~40%. This produces enough ring density for visible Moire patterns between source pairs.
3. **Full depth**: Set Depth to ~80% for strong contrast.
4. **Animate**: Enable Animate with Drift Sp at ~50%. The lattice evolves continuously — nodes appear, merge, split, and dissolve.
5. **Replace + Rainbow**: Switch to Replace mode with Color = Rainbow. The output is a pure interference pattern with chromatic fringes — no input video.
6. **Invert**: Toggle Invert. Bright fringes become dark; dark nodes become bright. The overall structure is the same but the polarity reverses.
7. **Mix layering**: Switch back to Overlay mode. Lower Mix to ~60% to blend the interference pattern transparently over the source video.

**Key concepts**: Four sources produce a 2D lattice with Moire fringes, irrational DDS ratios ensure non-repeating evolution, Replace mode generates standalone patterns, Invert reverses fringe polarity

---


## Tips

- **Start with Overlay mode**: Overlay embeds the interference pattern into the source video, making it easier to see how the rings interact with real content.
- **Single source first**: Begin with one source to understand the basic ring structure before adding more sources and complexity.
- **Low Drift Sp for contemplative patterns**: Speed around 10–20% creates slowly evolving interference that is mesmerizing without being frantic.
- **Spread controls interference complexity**: At Spread = 0, all sources overlap at the center, producing simple reinforced rings. Increasing Spread separates the sources and creates richer interference zones.
- **Wavelength and Sources compound**: More sources with tighter wavelength produce the most complex lattice structures.
- **Replace + Rainbow for standalone pattern generation**: This combination produces a self-illuminated chromatic interference pattern suitable for direct output or downstream compositing.
- **Invert for complementary compositing**: In Overlay mode, Invert changes whether constructive interference brightens or darkens the source, giving two complementary composite looks from the same pattern.
- **Feedback loops**: Routing the output back to the input creates recursive interference — the ripple pattern modulates itself, producing fractal-like self-similar structures that evolve over time.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation BT.601 defining standard-definition YUV color encoding with separate luminance and chrominance channels. |
| **Constructive Interference** | The reinforcement that occurs when two or more wave crests coincide, producing a combined amplitude greater than either wave alone. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms using a phase accumulator incremented by a fixed frequency constant each clock cycle. |
| **Destructive Interference** | The cancellation that occurs when a wave crest coincides with a wave trough, reducing the combined amplitude. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable IC executing the Tidepool processing pipeline. |
| **Interference Pattern** | The spatial distribution of constructive and destructive wave interactions, producing alternating bright and dark fringes. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Manhattan Distance** | The sum of absolute differences in X and Y coordinates (|dx| + |dy|); produces diamond-shaped contours instead of circular. |
| **Moire Pattern** | A secondary large-scale pattern that emerges when two sets of fine periodic structures overlap with slightly different frequencies. |
| **Pipeline** | Sequential processing stages where each stage's output feeds the next on each clock cycle. |
| **Superposition** | The principle that the combined amplitude of overlapping waves equals the sum of their individual amplitudes at each point. |
| **Triangle Wave** | A periodic waveform that ramps linearly up and down, used as an approximation to a sine wave for distance-to-amplitude mapping. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
