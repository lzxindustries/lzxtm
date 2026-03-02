---
draft: true
sidebar_position: 161
slug: /instruments/videomancer/lichen
title: "Lichen"
image: /img/instruments/videomancer/lichen/lichen_hero.png
description: "Lichen is a synthesis program that grows circular patches from random positions on a blank canvas, frame by frame."
---

import lichen_hero from '/img/instruments/videomancer/lichen/lichen_hero.png';
import lichen_animation from '/img/instruments/videomancer/lichen/lichen_animation.gif';
import lichen_control_panel from '/img/instruments/videomancer/lichen/lichen_control_panel.png';
import lichen_exercise1_result from '/img/instruments/videomancer/lichen/lichen_exercise1_result.gif';
import lichen_exercise2_result from '/img/instruments/videomancer/lichen/lichen_exercise2_result.gif';
import lichen_exercise3_result from '/img/instruments/videomancer/lichen/lichen_exercise3_result.gif';

# Lichen

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lichen_hero} alt="Lichen hero image"/>
*Lichen growing irregular organic patches across a black field, their crusty edges and overlapping tints recalling colonies spreading across stone.*
<img src={lichen_animation} alt="Lichen animated output"/>
*Lichen output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Lichen is a synthesis program that grows circular patches from random positions on a blank canvas, frame by frame. Each patch expands outward at a controllable rate, and a 16-bit LFSR noise source breaks the smooth Manhattan-distance contour of each patch into ragged, organic edges — emulating the irregular boundary of a real lichen colony encrusting a rock face. The name refers directly to the organism: a symbiotic composite of fungi and algae that colonises surfaces in slow, crusty, spreading formations.

Four patches can be active simultaneously, each with its own centre position seeded from the LFSR at reset. When patches overlap, their tinting darkens cumulatively — a single overlap dims the output slightly, while four overlapping patches produce deep, dark regions. The patch colour shifts between a cool green and a warm amber depending on a toggle, evoking different species of biological lichen. Boundary pixels receive a subtle luma highlight, giving the effect of ridged, textured edges.

At low growth rates and small spreads, Lichen produces compact, slowly evolving spots of color on a dark field. At high growth rates and maximum spread, the patches quickly flood the frame, merging into large overlapping tinted zones. The Edge Irregularity control determines how much the LFSR noise disrupts the diamond-shaped boundary — at zero, patches are clean diamonds; at maximum, they become rough, ragged shapes that change every pixel.

---

## Background

### What Is Manhattan Distance?

The Manhattan distance between two points is the sum of the absolute differences of their coordinates: $|x_1 - x_2| + |y_1 - y_2|$. Unlike Euclidean distance (which produces circular contours), Manhattan distance produces diamond-shaped contours centred on the origin. This is the metric Lichen uses to determine whether a pixel is inside or outside each patch. The diamond shape is a natural consequence of the discrete, axis-aligned nature of digital pixel grids — and on an FPGA, Manhattan distance is trivially cheap compared to the multiplications required for Euclidean distance.

### LFSR Edge Noise

A 16-bit Linear Feedback Shift Register produces a pseudo-random bit sequence that repeats every $2^{16} - 1 = 65535$ clocks. Lichen uses this LFSR output as a per-pixel noise source. Near the boundary of each patch, the LFSR bits are XORed with the inside/outside comparison, randomly flipping some boundary pixels from inside to outside (or vice versa). The Edge Irregularity control acts as an AND mask on the LFSR output, governing how many noise bits participate. At zero, the mask zeros out all noise, leaving clean diamond boundaries. At maximum, all noise bits contribute, producing the most ragged edges.

### Patch Growth and Frame Accumulation

Lichen is a frame-stateful program: each patch's radius is stored as a 12-bit register that persists across frames and increments on every vertical sync pulse. Growth rate is derived from the pot value as $1 + \text{pot}>>7$, giving a range of 1 to 8 pixels per frame. The maximum radius is similarly derived as $32 + \text{pot}>>1$, clamping growth so patches cannot exceed the specified spread. This stateful, incrementally evolving behaviour is what makes Lichen a *synthesis* program — it generates imagery from internal state rather than transforming an input signal.

### Overlapping Tint Accumulation

When a pixel falls inside multiple patches simultaneously, Lichen counts the number of overlaps (1 through 4) and applies increasing darkening to the luma channel. A single overlap shifts the chroma gently toward the target lichen colour and dims the luma slightly. Four overlapping patches apply the full tint strength and strong darkening. This additive overlap model creates natural-looking density variations as patches meet and merge, similar to how real lichen colonies darken and thicken where they grow into one another.

### Colour Tinting in YUV

The tinting stage shifts the U and V chroma channels toward a target colour — green (U≈420, V≈480) or amber (U≈440, V≈580) — while dimming the Y channel. The shift is proportional to the Tint Strength parameter, which selects one of four shift amounts (6.25%, 12.5%, 25%, or 50% of the way toward the target). Working in YUV allows the program to separate the colour shift (UV) from the darkening (Y), tinting without destroying the underlying luminance structure of the synthesized patches.


---

## Signal Flow

```
Video Timing Generator
│
├── Pixel Counters (h_count, v_count) ────────────────────────
│               │
│   ┌───────────┴──────────────────────────┐
│   │    Patch State (4× centre + radius)  │
│   │    Updated per vsync (growth/reset)  │
│   └────────────┬─────────────────────────┘
│                │
├── Stage 1: Input Register + Parameter Latch ────────────────
│   (data_in → s_y/u/v_st1)
│
├── Stage 2: Manhattan Distance (4 patches) ──────────────────
│   |h - cx(i)| + |v - cy(i)| → s_man_dist(0..3)
│
├── Stage 3: Edge Noise + Hit Classify + Overlap Count ───────
│   LFSR(16) → noise_mask AND → XOR boundary test
│   Count inside patches → s_overlap_cnt (0..4)
│   Detect boundary → s_on_boundary
│
├── Stage 4: Colour Tinting + Composite ──────────────────────
│   Y: darken by overlap_cnt × tint_strength
│   U,V: shift toward target colour (green/amber)
│   Boundary highlight: +32 luma at edges
│   Outside patches: black (synthesis source = 0)
│
├── Interpolator (4 clks): wet/dry mix ───────────────────────
│   lerp(black_source, tinted_output, mix_amount)
│
└── Output (bypass mux) ──────────────────────────────────────
```

The critical interaction is between the LFSR noise and the boundary comparison in stage 3. When a pixel lies near the edge of a patch (within the boundary range), the LFSR bits are XORed with distance comparisons to probabilistically flip the inside/outside decision. Pixels well inside the patch are always classified as inside regardless of noise. Pixels just outside the radius can also be pulled inward when specific LFSR conditions are met, creating an asymmetric boundary that extends slightly beyond the mathematical radius. The overlap count feeds directly into stage 4's darkening logic, where multiple patches compound their tint effect.

---

## Parameter Reference

<img src={lichen_control_panel} alt="Videomancer front panel with Lichen loaded"/>
*Videomancer's front panel with Lichen active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Grow Rat
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the frame-by-frame growth increment of all patches. The VHDL maps this as $1 + \text{pot}>>7$, giving a range of 1 to 8 pixels per frame. At minimum, patches expand one pixel per frame — slow, deliberate colonisation. At maximum, patches visibly leap outward, flooding the screen in seconds. Because growth is applied at each vsync, the visual rate depends on the frame rate — 60 fps makes growth twice as fast as 30 fps. After patches reach the maximum radius (set by Knob 2), this control has no further effect until a reset.

---

#### Knob 2 — Patches
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the maximum radius that any patch can reach before growth stops. The VHDL derivation is $32 + \text{pot}>>1$, producing a range from 32 to roughly 543 pixels. At minimum, patches remain small isolated spots. At maximum, a single patch can span nearly a third of the 1920-pixel frame width. This control interacts directly with Growth Rate — faster growth reaches the limit sooner, but the final coverage is determined by Spread alone.

---

#### Knob 3 — Edge Irr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the amount of LFSR noise applied to the patch boundaries. The pot value is used as a bitwise AND mask on the 12-bit noise extracted from the LFSR. At zero, the mask suppresses all noise, producing clean diamond-shaped patches. At maximum, all noise bits pass through, creating heavily irregular, crusty boundaries that change every pixel. Intermediate values produce partially noisy edges — some sections of the boundary are smooth, others jagged.

---

#### Knob 4 — Bnd Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Despite its TOML label "Bnd Width," this register actually controls the colour tinting strength applied to pixels inside patches. The VHDL signal `s_tint_strength` selects one of four levels of chroma shift toward the target lichen colour (6.25%, 12.5%, 25%, or 50%). Higher values push inside-patch pixels more aggressively toward pure green or amber, while lower values produce a subtle, barely perceptible colour wash. This control also scales the luma darkening applied by the overlap count — higher tint strength means stronger dimming in overlap regions.

---

#### Knob 5 — Color Var
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Despite its TOML label "Color Var," this register controls the boundary transition width in pixels. The VHDL derives this as $4 + \text{pot}>>6$, giving a range of approximately 4 to 19 pixels. The boundary width determines how wide the zone is around each patch's mathematical radius where LFSR noise can flip the inside/outside classification. A narrow boundary produces sharp-edged patches with noise only right at the edge. A wide boundary creates a broad, fuzzy transition zone where the patch dissolves into ragged tendrils.

---

#### Knob 6 — Texture
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Despite its TOML label "Texture," this register is mapped to `s_mix_pot` in the VHDL — the interpolator wet/dry blend amount for the secondary mix stage. In practice, this provides an additional mix control that modulates the effect intensity alongside the main Mix fader (Knob 12). Setting this to zero suppresses the lichen effect through the secondary mix path; setting it to maximum passes the full synthesized output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Species** | Crust | Foliose |
| **8 — Surface** | Rock | Bark |
| **9 — Merge** | Border | Blend |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 each use only the lowest bit of their respective 10-bit registers, despite the TOML defining four value labels for each. The VHDL uses `registers_in(6)(0)` and `registers_in(6)(1)` as single-bit selectors. Toggle 9 is labelled "Merge" in the TOML but actually triggers a reset of all patch positions on its rising edge — not a merge operation. Toggle 10 ("Animate") is completely unused in the VHDL; the register bit is read but never connected to any logic.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Master wet/dry crossfade. At 0%, the output is entirely the delayed dry input (typically black for a synthesis program). At 100%, the output is the fully synthesized lichen texture. Intermediate values blend the two, allowing the lichen patches to be subtly composited atop any incoming video signal. The interpolation is linear across all three YUV channels simultaneously.

---

## Guided Exercises

These exercises explore Lichen as a slowly evolving synthesis source, progressing from basic patch growth through edge texturing to full multi-patch layered compositions with colour tinting.

### Exercise 1: First Colonies

<img src={lichen_exercise1_result} alt="First Colonies result"/>
*First Colonies — simulated result across source images.*
**Objective**: Observe basic patch growth, understand growth rate and spread limits.

1. Set Growth Rate (Knob 1) to about 30% for slow, observable expansion.
2. Set Spread (Knob 2) to about 40% so patches stop at a moderate size.
3. Set Edge Irregularity (Knob 3) to 0% — clean diamond patches.
4. Watch the patches emerge and grow from their starting positions.
5. Toggle Species (Switch 7) to switch between 2 and 4 patches.
6. When patches reach their maximum radius, toggle Reset (Switch 9) to restart from new positions.
7. Increase Growth Rate to 80% and observe how quickly the patches flood.

**Key concepts**: Manhattan distance produces diamond shapes, growth is per-frame and frame-rate dependent, spread sets the ceiling

---

### Exercise 2: Organic Boundaries

<img src={lichen_exercise2_result} alt="Organic Boundaries result"/>
*Organic Boundaries — simulated result across source images.*
**Objective**: Use LFSR noise to break diamond patches into organic, lichen-like shapes.

1. Start with the Exercise 1 settings, but set Growth Rate to ~20% for slow observation.
2. Slowly increase Edge Irregularity (Knob 3) from 0% to 100%. Watch the clean diamond edges dissolve into ragged, crusty contours.
3. Adjust Boundary Width (Knob 5 — labelled "Color Var") to widen or narrow the noisy transition zone.
4. Set Boundary Width to minimum (~0%) — noise is confined to a thin ring at the patch edge.
5. Set Boundary Width to maximum (~100%) — the entire patch interior becomes partially affected by noise.
6. Toggle Reset (Switch 9) several times to observe different random boundary patterns at different positions.

**Key concepts**: LFSR noise creates pseudo-random pixel-level variation, AND masking controls noise density, boundary width sets the spatial extent of the noisy zone

---

### Exercise 3: Overlapping Colonies

<img src={lichen_exercise3_result} alt="Overlapping Colonies result"/>
*Overlapping Colonies — simulated result across source images.*
**Objective**: Explore tinting, overlap darkening, and colour modes with maximum patch count.

1. Enable all 4 patches (Switch 7 on).
2. Set Spread (Knob 2) to ~80% so patches grow large enough to overlap.
3. Set Growth Rate (Knob 1) to ~40% — moderate speed.
4. Increase Tint Strength (Knob 4 — labelled "Bnd Width") to ~80%. Observe the colour shift in inside-patch pixels.
5. Toggle Surface (Switch 8) between green and amber colours. Note how the tint target changes.
6. Watch the overlap regions darken as patches meet. With 4 overlapping patches, the luma drops significantly.
7. Use Mix (Knob 12) at ~60% to blend the lichen texture over an incoming video source.
8. Use Reset (Switch 9) to restart — observe how different starting positions create different overlap patterns.

**Key concepts**: Overlap count drives cumulative darkening, tint strength controls both chroma shift and luma dimming, colour mode selects green vs amber target

---


## Tips

- **Reset is your friend**: When patches grow stale or the composition feels crowded, toggling the Reset switch (labelled "Merge") restarts all patches from new random positions instantly.
- **Start slow**: Growth Rate at 10–20% lets you watch the boundary evolve pixel by pixel — essential for understanding how edge noise interacts with the expanding radius.
- **Boundary width shapes the texture**: A narrow boundary width produces crisp, well-defined patch edges. A wide boundary produces diffuse, moss-like transitions. The visual difference is dramatic.
- **Overlap creates depth**: With 4 patches and high spread, the darkened overlap regions create a sense of layered density. Adjust Tint Strength to control how extreme the darkening is.
- **Green vs amber**: The two colour modes are not simply palette swaps — they target different U/V coordinates, producing distinct colour relationships against various backgrounds.
- **Mix for compositing**: Because Lichen is a synthesis source, the Mix fader controls how much of the generated texture appears in the final output. At partial mix values, lichen patches float over whatever video is passing through the input.
- **Frame rate matters**: Growth rate is per-frame, so the visual speed of patch expansion is directly proportional to the video standard's frame rate.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA. Lichen uses zero BRAM. |
| **Chroma** | The colour component of a video signal, encoded as U (Cb) and V (Cr) in YUV colour space. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms from a phase accumulator. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit executing the video processing pipeline. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function of its previous state, producing a pseudo-random bit sequence. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Manhattan Distance** | The sum of horizontal and vertical distances between two points, $|x_1-x_2|+|y_1-y_2|$, producing diamond-shaped contours. |
| **Pipeline** | A series of sequential processing stages, each operating in one clock cycle. |
| **Synthesis** | Generation of video imagery from internal state and parameters, without requiring an input video source. |
| **YUV** | A colour encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
