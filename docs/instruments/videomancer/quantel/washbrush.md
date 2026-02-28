---
draft: true
sidebar_position: 283
slug: /instruments/videomancer/washbrush
title: "Washbrush"
image: /img/instruments/videomancer/washbrush/washbrush_hero.png
description: "The Quantel Paintbox, introduced in 1981, was the first commercially successful digital paint system for broadcast television."
---

import washbrush_before_after from '/img/instruments/videomancer/washbrush/washbrush_before_after.png';
import washbrush_control_panel from '/img/instruments/videomancer/washbrush/washbrush_control_panel.png';
import washbrush_exercise1_result from '/img/instruments/videomancer/washbrush/washbrush_exercise1_result.png';
import washbrush_exercise2_result from '/img/instruments/videomancer/washbrush/washbrush_exercise2_result.png';
import washbrush_exercise3_result from '/img/instruments/videomancer/washbrush/washbrush_exercise3_result.png';
import washbrush_hero from '/img/instruments/videomancer/washbrush/washbrush_hero.png';
import washbrush_source1_kodim15 from '/img/instruments/videomancer/washbrush/washbrush_source1_kodim15.png';
import washbrush_source2_kodim01 from '/img/instruments/videomancer/washbrush/washbrush_source2_kodim01.png';
import washbrush_source3_kodim01_bw from '/img/instruments/videomancer/washbrush/washbrush_source3_kodim01_bw.png';

# Washbrush

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={washbrush_hero} alt="Washbrush hero image"/>
*Washbrush painting translucent airbrush strokes along a Lissajous orbit onto a persistent BRAM canvas, with warm hues accumulating over time.*
<img src={washbrush_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Washbrush applied.*

---

## Overview

The Quantel Paintbox, introduced in 1981, was the first commercially successful digital paint system for broadcast television. Its most memorable feature was the electronic airbrush — a pressure-sensitive stylus that painted translucent color onto a frame buffer, building up layers of pigment just like physical paint on canvas. Washbrush channels this legacy, implementing a DDS-animated radial brush that traces Lissajous curves across a persistent framebuffer, laying down continuous strokes of translucent color that accumulate and decay over time.

The name *Washbrush* refers to two of its four media textures: the smooth airbrush and the directional wash, both staples of digital painting. The program stores a persistent canvas in three BRAMs (one each for Y, U, V), and on every frame the brush deposits a new stamp at a position computed from two DDS phase accumulators driving sine lookups — the X and Y frequency ratios determine the Lissajous figure traced by the brush. An IIR decay stage slowly erodes the existing canvas, so old paint fades unless Permanence is set high enough to preserve it. The result is a continuously evolving painting that builds, layers, and gradually dissolves.

Four media textures — airbrush, wash, chalk, and pastel — each produce a distinct character by modifying how the radial brush falloff is translated into opacity. An airbrush creates smooth Gaussian-like gradients; a wash streaks directionally along the brush path; chalk adds LFSR-driven noise for a granular, textured look; pastel applies wide, faint strokes that build up gradually through repeated layering.

---

## Background

### The Quantel Paintbox

The Quantel Paintbox (1981) was a £100,000 digital video effects system that brought electronic painting to broadcast production. Its framebuffer stored a single HD video frame, and operators used a pressure-sensitive stylus to paint directly onto this buffer. The output — live from the framebuffer — was broadcast-quality video, making it possible to create title cards, weather graphics, and artistic compositions in real time. The Paintbox's airbrush mode, which laid down translucent circular dabs along the stylus path, was its most iconic feature and directly inspires Washbrush's radial brush engine.

### Lissajous Figures

A Lissajous figure is the path traced by a point whose X and Y coordinates are driven by sinusoidal oscillations at potentially different frequencies. When the frequency ratio is rational (e.g., 3:2, 4:3), the path forms a closed loop with a distinctive knotted shape. When the ratio is irrational, the path never exactly repeats and gradually fills a rectangular region. Washbrush exploits this by using two DDS phase accumulators — one for X, one for Y — whose frequency ratio is set by the X Freq and Y Freq knobs. Simple ratios (1:1, 2:1) produce clean, repeating paths; complex ratios (5:7, 3:8) produce intricate, space-filling orbits that paint across the entire canvas.

### IIR Persistent Canvas

The canvas persistence uses an IIR (Infinite Impulse Response) feedback loop: on each frame, every pixel's value is multiplied by the Permanence factor (0–1023 mapped to a decay coefficient) and then the new brush contribution is added. When Permanence is high, old paint decays very slowly, allowing thick buildup over many frames — like oil paint on canvas. When Permanence is low, paint fades rapidly, creating a watercolor-like wash that evaporates almost as fast as it is laid down. At Permanence = 0, only the current brush stroke is visible at any moment.

### LFSR Texture Noise

The chalk and pastel media textures use a 16-bit Linear Feedback Shift Register (LFSR) to generate pseudo-random noise that modulates the brush opacity. The LFSR produces a repeating sequence of 65535 values before cycling — functionally random at video pixel rates. For chalk, the noise directly modulates the radial falloff, creating a granular, crayon-like texture with random gaps in the stroke. For pastel, the noise is attenuated, producing a softer, more uniform texture with subtle grain.

### Eight-Hue Color Palette

When the Color Source is set to Hue mode, the brush color is selected from an eight-entry palette indexed by the upper three bits of the Brush Hue parameter. This produces eight discrete hues spanning the color wheel: white, blue-violet, yellow, green, orange, purple-blue, magenta, and bright white. The quantization is deliberate — it mirrors the limited palette approach of early digital paint systems and makes color selection quick and predictable during live performance.


---

## Signal Flow

```
DDS Phase Accumulators (X Freq, Y Freq)
│
├── Brush Position ─────────────────────────────────────────────
│   ├─ Sine LUT × 2         (32-entry signed, phase → position)
│   └─ Path Mode             Orbit: Lissajous / Sweep: linear scan
│
├── Distance + Falloff ─────────────────────────────────────────
│   ├─ 1. dx, dy from brush center
│   ├─ 1. dist² = dx² + dy²
│   └─ 1. radius² from Brush Size
│
├── Media Texture ──────────────────────────────────────────────
│   ├─ 2. Radial falloff     (linear: (r² − d²) / r²)
│   ├─ 2. Media mode:
│   │     00: Airbrush       (smooth radial gradient)
│   │     01: Wash           (directional streak × |dx|)
│   │     10: Chalk          (falloff × LFSR noise)
│   │     11: Pastel         (half-scale, gradual build)
│   └─ 2. Alpha = falloff × Intensity
│
├── Canvas IIR ─────────────────────────────────────────────────
│   ├─ 3. Read BRAM          (existing canvas Y/U/V)
│   ├─ 3. Decay: existing × Permanence / 1024
│   └─ 3. Accumulate: decayed + brush_color × alpha
│         └─ Write BRAM      (updated canvas Y/U/V)
│
├── Brush Color ────────────────────────────────────────────────
│   └─ Color Src: Hue (8-entry palette) / Video (sample input)
│
├── Over Composite ─────────────────────────────────────────────
│   └─ 4. canvas × alpha + input × (1 − alpha)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ Interpolator × 3      (wet/dry crossfade per channel)
│
└── Sync Signals ───────────────────────────────────────────────
    └─ 8-clock delay pipeline  (hsync, vsync, field)
```

The DDS path generator updates once per field (vsync edge). The X and Y phase accumulators advance by a frequency-dependent step: the upper 3 bits of the frequency pot select a multiplier from 1 to 8, giving rational Lissajous frequency ratios. In Sweep mode the DDS is replaced with a simple linear ramp — X advances at a fixed rate while Y increments by 1 each field, scanning the brush across the canvas row by row. The sine LUT (32 entries, signed 8-bit) maps the phase to brush position, scaled to cover the active video region.

The canvas IIR is the critical feedback path. For each active pixel, the BRAM is read, the stored value is multiplied by the Permanence factor (dividing by 1024), and the new brush contribution (brush color × alpha) is added. The result is written back to the same BRAM address. Because the BRAM has single-port access, the read and write occur in sequential pipeline stages. The self-alpha compositing in Stage 4 uses the canvas Y brightness as the alpha key for the over-composite, so bright canvas regions dominate the output and dark regions let the underlying video show through.

---

## Parameter Reference

<img src={washbrush_control_panel} alt="Videomancer front panel with Washbrush loaded"/>
*Videomancer's front panel with Washbrush active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — X Freq
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

X Frequency selects the horizontal oscillation rate for the Lissajous path. The upper 3 bits of the 10-bit register select frequencies 1 through 8, so the knob has 8 discrete positions. At frequency 1 the brush traces a simple back-and-forth arc. At higher frequencies it traces multiple loops per cycle, creating more complex figures. The relationship between X and Y frequencies determines the Lissajous pattern — matching frequencies produce a circle or ellipse, while different frequencies create figure-eight, pretzel, and knot patterns.

---

#### Knob 2 — Y Freq
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 4 |

Y Frequency selects the vertical oscillation rate independently of X. The same 8-step quantization applies. Setting X=1 and Y=2 produces a figure-eight; X=3 and Y=2 produces a three-lobed trefoil; X=1 and Y=1 produces a diagonal line or circle depending on phase relationship. Experimentation with different ratios is the primary creative tool for controlling the brush path shape.

---

#### Knob 3 — Brush Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Brush Size sets the radius of the radial brush stamp. At minimum the brush is a tiny point producing fine lines. At maximum it is a wide, sweeping daub that covers a large portion of the canvas. The radial falloff (Stage 2) is computed as the normalized distance from the brush center — larger brushes produce softer, more gradual gradients because the falloff extends over more pixels. The brush radius squared is used in the distance comparison to avoid a square root operation.

---

#### Knob 4 — Brush Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 60° |
| Suffix | ° |

Brush Hue selects the brush color when Color Source is set to Hue mode. The upper 3 bits of the register index into an eight-entry palette: bright neutral, blue-violet, warm yellow, cool green, orange, deep blue-purple, magenta, and bright white. The quantized palette provides quick, predictable color selection. When Color Source is set to Video, this parameter is ignored and the brush color is sampled from the input video at the current pixel position.

---

#### Knob 5 — Permanence
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 88% |
| Suffix | % |

Permanence controls the IIR decay rate of the canvas. At minimum (0) the canvas decays completely each frame, showing only the current brush stroke — a watercolor-like ephemeral wash. At maximum (1023) the canvas retains virtually everything, building up thick layers of paint like oil on canvas. Mid-range values (400–600) produce an interesting balance where recent strokes are vivid and older strokes gradually fade, creating a visible history of the brush path.

---

#### Knob 6 — Intensity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |
| Suffix | % |

Intensity controls the opacity of each brush stamp. At minimum the brush deposits almost no paint per frame, requiring many passes to build up visible color. At maximum each brush stamp is fully opaque at the center, creating bold, immediate marks. Intensity interacts multiplicatively with the media texture's falloff — the final alpha at any pixel is falloff × intensity / 1024. Low intensity with high permanence creates soft, gradually accumulating washes; high intensity with low permanence creates vivid but quickly fading strokes.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Media A** | Off | On |
| **8 — Media B** | Off | On |
| **9 — Color Src** | Hue | Video |
| **10 — Path Mode** | Orbit | Sweep |
| **11 — Bypass** | Off | On |

The toggles divide into a media selection pair (Media A + Media B, forming a 2-bit mode selector), a color source toggle, a path mode toggle, and bypass. Media A and B together select one of four brush textures. Color Source switches between the fixed palette and video sampling. Path Mode switches between the Lissajous orbit and a linear sweep scan. All four creative toggles are independent, producing 16 possible combinations of media, color, and path behavior.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Mix crossfades between the dry input signal and the wet canvas-composited output. At 0% the output is pure input video. At 100% the output shows the canvas fully composited over the input. This fader is particularly useful for controlling the canvas intensity in live performance — blending the painting in and out over the underlying video without affecting the ongoing DDS animation or canvas accumulation.

---

## Guided Exercises

These exercises explore Washbrush's paint engine from basic brush strokes through complex Lissajous calligraphy and persistent canvas techniques.

### Exercise 1: Simple Airbrush Circle

<img src={washbrush_exercise1_result} alt="Simple Airbrush Circle result"/>
*Simple Airbrush Circle — simulated result across source images.*
**Objective**: Create a basic circular Lissajous path with the airbrush media, observing how the persistent canvas accumulates paint over time.

1. Set X Freq and Y Freq both to position 1 (matching frequencies = circle)
2. Set Brush Size to 50% for a medium daub
3. Set Permanence to 70% for moderate persistence
4. Set Intensity to 60% for visible but not overwhelming strokes
5. Set Color Source to Hue and Brush Hue to select a warm color
6. Watch the brush trace a circular orbit, leaving a persistent trail
7. After 10–15 seconds, reduce Permanence to 20% and watch old paint fade

**Key concepts**: Lissajous frequency ratios, IIR canvas persistence, radial brush falloff, and the Permanence/Intensity balance.

---

### Exercise 2: Chalk Calligraphy

<img src={washbrush_exercise2_result} alt="Chalk Calligraphy result"/>
*Chalk Calligraphy — simulated result across source images.*
**Objective**: Use complex Lissajous ratios with the chalk texture to create intricate, textured calligraphic patterns.

1. Set X Freq to 5 and Y Freq to 3 for a 5:3 Lissajous ratio
2. Switch to Chalk mode (Media A = Off, Media B = On)
3. Set Brush Size to 30% for fine strokes
4. Set Permanence to 90% for near-permanent marks
5. Set Intensity to 80% for bold chalk marks
6. Observe the intricate knotted Lissajous traced with granular chalk texture
7. Try different frequency ratios (3:7, 5:8) for more complex patterns

**Key concepts**: Complex Lissajous ratios, LFSR noise modulation, high-permanence accumulation, and the relationship between brush size and path complexity.

---

### Exercise 3: Video-Sampled Wash Sweep

<img src={washbrush_exercise3_result} alt="Video-Sampled Wash Sweep result"/>
*Video-Sampled Wash Sweep — simulated result across source images.*
**Objective**: Use Sweep path mode with Video color sampling and the Wash media to create a painterly impression of the input video across the entire canvas.

1. Feed a colorful video source (nature footage, art, or color bars)
2. Switch Path Mode to Sweep for linear scanning
3. Switch Color Source to Video
4. Switch to Wash media (Media A = On, Media B = Off)
5. Set Brush Size to 60% for wide strokes
6. Set Permanence to 50% for medium fade
7. Set Intensity to 70%
8. Watch the canvas gradually fill with video-sampled colors in directional wash strokes
9. Set Mix to 60% to blend the painted canvas over the live video

**Key concepts**: Video color sampling, linear sweep scanning, directional media texture, and layered wet/dry blending.

---


## Tips

- **Match frequencies for clean shapes** — 1:1 gives circles, 2:1 gives figure-eights; start with simple ratios before exploring complex ones.
- **Permanence is your paint thickness** — low values create watercolor effects that fade within seconds; high values build up like oil paint with lasting marks.
- **Chalk mode adds realism** — the LFSR noise breaks up the smooth radial falloff, producing strokes that look like actual dry media on textured paper.
- **Sweep mode for full coverage** — when you need the brush to visit every part of the canvas, switch to Sweep mode for systematic left-to-right scanning.
- **Video sampling creates portraits** — feeding a face or landscape into Video color mode while tracing a space-filling Lissajous creates an impressionistic color reproduction of the source.
- **Low Intensity + High Permanence = glazing** — many translucent layers building up slowly mimics the glazing technique used in oil painting.
- **Mix for layering control** — keep Mix at 50–70% to see the canvas strokes layered over the live video input in real time.
