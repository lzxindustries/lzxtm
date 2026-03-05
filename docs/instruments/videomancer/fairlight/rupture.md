---
draft: true
sidebar_position: 256
slug: /instruments/videomancer/rupture
title: "Rupture"
image: /img/instruments/videomancer/rupture/rupture_hero_s1.png
description: "Color folding is the video equivalent of bending sheet metal past its elastic limit — push a signal value beyond its maximum and, instead of clipping flat, it reflects back downward, creating a mirror-image contour inside the original gradient."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import rupture_control_panel from '/img/instruments/videomancer/rupture/rupture_control_panel.png';
import rupture_source1_car from '/img/instruments/videomancer/rupture/rupture_source1_car.png';
import rupture_source2_sunset from '/img/instruments/videomancer/rupture/rupture_source2_sunset.png';
import rupture_source3_collage from '/img/instruments/videomancer/rupture/rupture_source3_collage.png';
import rupture_source4_pattern from '/img/instruments/videomancer/rupture/rupture_source4_pattern.png';
import rupture_source5_man from '/img/instruments/videomancer/rupture/rupture_source5_man.png';
import rupture_source6_paint from '/img/instruments/videomancer/rupture/rupture_source6_paint.png';
import rupture_hero_s1 from '/img/instruments/videomancer/rupture/rupture_hero_s1.png';
import rupture_hero_s2 from '/img/instruments/videomancer/rupture/rupture_hero_s2.png';
import rupture_hero_s3 from '/img/instruments/videomancer/rupture/rupture_hero_s3.png';
import rupture_hero_s4 from '/img/instruments/videomancer/rupture/rupture_hero_s4.png';
import rupture_hero_s5 from '/img/instruments/videomancer/rupture/rupture_hero_s5.png';
import rupture_hero_s6 from '/img/instruments/videomancer/rupture/rupture_hero_s6.png';
import rupture_ex1_s1 from '/img/instruments/videomancer/rupture/rupture_ex1_s1.png';
import rupture_ex1_s2 from '/img/instruments/videomancer/rupture/rupture_ex1_s2.png';
import rupture_ex1_s3 from '/img/instruments/videomancer/rupture/rupture_ex1_s3.png';
import rupture_ex1_s4 from '/img/instruments/videomancer/rupture/rupture_ex1_s4.png';
import rupture_ex1_s5 from '/img/instruments/videomancer/rupture/rupture_ex1_s5.png';
import rupture_ex1_s6 from '/img/instruments/videomancer/rupture/rupture_ex1_s6.png';
import rupture_ex2_s1 from '/img/instruments/videomancer/rupture/rupture_ex2_s1.png';
import rupture_ex2_s2 from '/img/instruments/videomancer/rupture/rupture_ex2_s2.png';
import rupture_ex2_s3 from '/img/instruments/videomancer/rupture/rupture_ex2_s3.png';
import rupture_ex2_s4 from '/img/instruments/videomancer/rupture/rupture_ex2_s4.png';
import rupture_ex2_s5 from '/img/instruments/videomancer/rupture/rupture_ex2_s5.png';
import rupture_ex2_s6 from '/img/instruments/videomancer/rupture/rupture_ex2_s6.png';
import rupture_ex3_s1 from '/img/instruments/videomancer/rupture/rupture_ex3_s1.png';
import rupture_ex3_s2 from '/img/instruments/videomancer/rupture/rupture_ex3_s2.png';
import rupture_ex3_s3 from '/img/instruments/videomancer/rupture/rupture_ex3_s3.png';
import rupture_ex3_s4 from '/img/instruments/videomancer/rupture/rupture_ex3_s4.png';
import rupture_ex3_s5 from '/img/instruments/videomancer/rupture/rupture_ex3_s5.png';
import rupture_ex3_s6 from '/img/instruments/videomancer/rupture/rupture_ex3_s6.png';

# Rupture

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Car", before: rupture_source1_car, after: rupture_hero_s1 },
    { label: "Sunset", before: rupture_source2_sunset, after: rupture_hero_s2 },
    { label: "Collage", before: rupture_source3_collage, after: rupture_hero_s3 },
    { label: "Pattern", before: rupture_source4_pattern, after: rupture_hero_s4 },
    { label: "Man", before: rupture_source5_man, after: rupture_hero_s5 },
    { label: "Paint", before: rupture_source6_paint, after: rupture_hero_s6 },
  ]}
/>
*Rupture applying cascaded triangle-fold color inversion with hue-distributed offsets to create iridescent contour structures.*

---

## Overview

Color folding is the video equivalent of bending sheet metal past its elastic limit — push a signal value beyond its maximum and, instead of clipping flat, it reflects back downward, creating a mirror-image contour inside the original gradient. Rupture applies this principle to every pixel of every channel, folding brightness and chrominance values through configurable offset thresholds. The result is a prismatic decomposition of the source image into bands of inverted and re-inverted color — reminiscent of oil-on-water iridescence, solarization, or the split-primary color effects of the Fairlight CVI's "Break Colourize" function.

The program chains up to four fold stages in cascade. Each stage adds the same per-channel offset and folds any overflow back into range. Because the fold operation is nonlinear, cascading it produces increasingly complex contour structures — a single fold creates one mirror boundary; two folds create nested inversions; four folds produce fractal-like banding where every tonal gradient in the source is sliced into multiple reflected strips. The Hue knob distributes the fold offset across Y, U, and V channels in a four-quadrant rotation pattern, allowing the artist to target specific color axes.

The name *Rupture* evokes the moment a continuous surface tears open to reveal layered structure beneath — which is precisely what happens to smooth video gradients when they are repeatedly folded and reflected.

---

## Quick Start

1. **Start with one cascade**: A single fold stage is the easiest to understand — contour lines appear where the signal exceeds (1023 − offset). Add cascades only after you understand where the fold boundaries sit.
2. **ColDepth and Cascades compound**: A moderate ColDepth with 4 cascades can produce denser contours than maximum ColDepth with 1 cascade. Use Cascades for complexity, ColDepth for threshold position.
3. **Hue at 270° for monochromatic folds**: All three channels receive equal offset, producing contour-rich luminance banding without color shifting — useful as a foundation before experimenting with color.

---

## Background

### What Is Wavefolding?

Wavefolding originated in analog synthesizer design. When a signal exceeds the rails of an amplifier stage, instead of hard-clipping the excess portion is *reflected* back into range — like a ball bouncing off a wall. The sonic result is harmonic enrichment: a pure sine wave, when folded, develops odd and even harmonics depending on the fold symmetry. Rupture applies the same principle in the video domain. A smooth luminance ramp, when folded, develops visible contour lines at each fold boundary. The number of visible contours increases with fold depth and cascade count.

### Triangle Fold vs. Hard Clip

Rupture offers two fold behaviors. **Triangle fold** (mirror) reflects overflow symmetrically: a value of 1100 in a 0–1023 range becomes 1023 − (1100 − 1023) = 946. This preserves gradient continuity — the signal reverses direction smoothly at each boundary. **Hard clip** simply clamps overflow to 1023, producing flat plateaus wherever the signal exceeds the threshold. Triangle fold creates undulating contours; hard clip creates hard-edged posterized bands. The choice is aesthetic: fold for organic iridescence, clip for graphic posterization.

### Fairlight CVI Heritage

The Fairlight Computer Video Instrument (1984) pioneered real-time video effects including a "Break Colourize" function that decomposed video into color bands by folding and offsetting individual channels. Rupture extends this concept with configurable cascade depth and hue-angle distribution — features that were not possible with the CVI's fixed architecture. The Fairlight category in Videomancer's program library collects effects inspired by this lineage of per-channel nonlinear color processing.

### Cascade Depth and Harmonic Analogy

Each fold stage doubles the number of contour boundaries visible in a smooth gradient. One stage with moderate offset produces a single reflection — like a single overtone. Two stages produce four boundaries; three stages produce eight; four stages can create sixteen or more visible contour lines within the same gradient range. This exponential growth mirrors the harmonic series in audio synthesis: each additional folding stage adds higher-frequency spatial detail to the color structure.

### Hue Distribution and 4-Quadrant Rotation

Rather than applying the same offset to all three channels, Rupture distributes the fold offset across Y, U, and V using a four-quadrant scheme controlled by the Hue knob. In quadrant 0 (0°–90°), Y receives the primary offset while U and V receive attenuated secondary offsets. In quadrant 1 (90°–180°), U becomes primary. In quadrant 2 (180°–270°), V is primary. In quadrant 3 (270°–360°), all channels receive equal offset. This allows the artist to target specific color axes — folding only luminance for monochromatic contours, or folding only chrominance for psychedelic color shifts with preserved brightness structure.


---

## Signal Flow

Input Register → Per-Channel Offset → Cascaded Fold → ... → fold → Brightness Offset

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Luma Invert (optional)
│   └── Y = bitwise NOT(Y) if Luma Invert enabled
│
├── Stage 2: Per-Channel Offset Computation
│   ├── ColDepth × Value → base offset magnitude
│   ├── Channel Lock: all channels get same offset
│   └── Hue Distribution (4 quadrants):
│       ├── Q0: Y=primary, U=sat/2, V=sat/4
│       ├── Q1: U=primary, V=sat/2, Y=sat/4
│       ├── Q2: V=primary, Y=sat/2, U=sat/4
│       └── Q3: all=primary
│
├── Auto-Sweep DDS (adds +4 to hue accumulator per vsync)
│   └── Effective Hue = Hue pot + sweep accumulator
│
├── Stage 3: Cascaded Fold (1-4 stages, combinatorial)
│   ├── fold_channel(ch, offset, type):
│   │   ├── sum = ch + offset
│   │   ├── if sum ≤ 1023 → pass through
│   │   ├── if sum > 1023 AND type=Mirror → NOT(sum[9:0])
│   │   └── if sum > 1023 AND type=Clip → 1023
│   │
│   ├── Stage 1: fold(input, offset)
│   ├── Stage 2: fold(stage1, offset)
│   ├── Stage 3: fold(stage2, offset)
│   └── Stage 4: fold(stage3, offset)
│       └── Cascade selector picks output of stage 1/2/3/4
│
├── Stage 4: Brightness Offset + Output Register
│   └── Y = fold_Y + brightness - 512 (clamped 0-1023)
│
├── Interpolator (4 clocks) — wet/dry mix
│
└── Bypass Mux
    └── Select processed or pass-through
```

The fold function is the heart of Rupture. It adds an offset to the channel value, and if the 11-bit sum overflows (bit 10 set), it folds the lower 10 bits back by bitwise inversion. This creates a triangle-wave transfer function: as the input sweeps linearly from 0 to 1023, the output rises to (1023 − offset), then reverses direction and falls back. Cascading multiple fold stages compounds this reflection, creating nested inversions that slice the gradient into increasingly narrow alternating bands. The auto-sweep DDS slowly rotates the hue offset angle by adding a fixed increment to the sweep accumulator on each vertical sync, causing the color fold distribution to evolve continuously even with static input.

---

## Parameter Reference

<img src={rupture_control_panel} alt="Videomancer front panel with Rupture loaded"/>
*Videomancer's front panel with Rupture active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Controls the hue angle for the 4-quadrant offset distribution. This determines which color channel receives the primary fold offset. At 0°, Y (luminance) is the primary target — folds create monochromatic contours. At 90°, U (blue-yellow axis) is primary — folds shift the image toward split-primary blue/orange patterns. At 180°, V (red-cyan axis) is primary. At 270°, all channels receive equal offset for a more uniform, desaturated fold. Sweeping this knob rotates through the color wheel of fold effects.

---

#### Knob 2 — Saturaton
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the secondary channel offset via the saturation parameter. When the hue distribution assigns a primary channel, the other two channels receive an offset scaled by this control. At 0% the secondary channels are unaffected — only the primary channel folds. At 100% the secondary channels receive half the primary offset, creating multi-axis color splitting. This parameter controls how "iridescent" the fold effect appears — higher values produce more complex color interactions between channels.

---

#### Knob 3 — Value
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity scaling of the fold offset via the value parameter. The top 2 bits select a right-shift amount (0–3) applied to the ColDepth value before it becomes the per-channel offset. At maximum, the full ColDepth value is used. At minimum, the effective offset is divided by 8, producing subtle folding. This provides exponential control over fold intensity — a coarse sensitivity adjustment that complements the fine control of ColDepth.

---

#### Knob 4 — ColDepth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At 0% no offset is added and the signal passes through unchanged (no folding occurs). As the offset increases, the fold boundary moves lower into the tonal range: first only the brightest pixels fold, then progressively darker values are caught. At maximum offset, even mid-tones are folded multiple times per cascade stage, producing dense contour patterns. Internally, sets the primary fold offset magnitude — the amount added to each channel value before the fold test.

---

#### Knob 5 — Cascades
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Selects the number of fold cascade stages (1–4) using the top 2 bits of the register. At 1× cascade, each channel undergoes a single fold — smooth gradients develop one set of contour lines. At 2× cascade, the folded output is folded again, doubling the contour density. At 4× cascade, the signal is folded four times in series, producing complex interference-like banding. Higher cascade counts amplify the visual impact of even small offsets.

---

#### Knob 6 — Brightnss
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Applies a post-fold brightness offset to the Y channel. The register value is centered at 512 (no offset). Values above 512 brighten the folded output; values below 512 darken it. This bias is applied after the fold cascade, so it shifts the overall brightness of the contour pattern without affecting the fold geometry itself. Use it to balance the luminance of heavily-folded images that may have lost their original brightness structure.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — FoldType** | Triangle | Clip |
| **8 — ChanLock** | Indep | Locked |
| **9 — AutoSwep** | Off | On |
| **10 — Luma Inv** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control fold behavior, channel routing, temporal modulation, luminance preprocessing, and bypass. Fold Type (Toggle 7) selects between triangle mirror and hard clip modes. Channel Lock (Toggle 8) forces all three channels to receive identical offsets regardless of hue angle. Auto Sweep (Toggle 9) enables a slow DDS-driven rotation of the effective hue. Luma Invert (Toggle 10) inverts the luminance channel before folding. Bypass (Toggle 11) routes input directly to output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Rupture processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Rupture-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from a single gentle fold through multi-stage cascades to animated auto-sweep color evolution, building familiarity with Rupture's cascaded nonlinear processing.

### Exercise 1: Single-Stage Luminance Fold

<BeforeAfterSlider
  sources={[
    { label: "Car", before: rupture_source1_car, after: rupture_ex1_s1 },
    { label: "Sunset", before: rupture_source2_sunset, after: rupture_ex1_s2 },
    { label: "Collage", before: rupture_source3_collage, after: rupture_ex1_s3 },
    { label: "Pattern", before: rupture_source4_pattern, after: rupture_ex1_s4 },
    { label: "Man", before: rupture_source5_man, after: rupture_ex1_s5 },
    { label: "Paint", before: rupture_source6_paint, after: rupture_ex1_s6 },
  ]}
/>
*Single-Stage Luminance Fold — simulated result across source images.*
**Source**: A live camera feed or recorded footage with smooth tonal gradients — skies, skin tones, or gradient test patterns.

**What You'll Create**: Understand the basic triangle fold operation and how the ColDepth parameter controls contour placement.

1. Set Cascades to 1× (single fold stage).
2. Set Hue to 0° so that Y receives the primary offset.
3. Set Value to about 75% for strong fold intensity.
4. Slowly increase ColDepth from 0% upward. Watch contour lines appear first in the brightest areas, then migrate downward into mid-tones.
5. Toggle Fold Type between Triangle and Clip to see the difference — smooth V-shaped reversals vs. flat clipped bands.
6. Set Channel Lock (Toggle 8) on to see the monochromatic version, then off for color-differentiated folds.

**Key concepts**: Folding reflects overflow back into range, creating contour lines at tonal boundaries. Higher offset pushes the fold boundary lower into the image's dynamic range. Triangle fold is smooth; clip fold is flat.

---

### Exercise 2: Cascaded Color Iridescence

<BeforeAfterSlider
  sources={[
    { label: "Car", before: rupture_source1_car, after: rupture_ex2_s1 },
    { label: "Sunset", before: rupture_source2_sunset, after: rupture_ex2_s2 },
    { label: "Collage", before: rupture_source3_collage, after: rupture_ex2_s3 },
    { label: "Pattern", before: rupture_source4_pattern, after: rupture_ex2_s4 },
    { label: "Man", before: rupture_source5_man, after: rupture_ex2_s5 },
    { label: "Paint", before: rupture_source6_paint, after: rupture_ex2_s6 },
  ]}
/>
*Cascaded Color Iridescence — simulated result across source images.*
**Source**: High-contrast footage with varied colors — flowers, painted surfaces, or colorful graphics.

**What You'll Create**: Explore how cascading fold stages and hue distribution create complex iridescent color patterns.

1. Set Cascades to 3× for dense contour nesting.
2. Set Hue to about 90° so that U (blue-yellow axis) receives the primary fold.
3. Set Saturaton to about 60% to engage the secondary channels.
4. Set ColDepth to about 40% — moderate offset that cascading will amplify.
5. Slowly sweep Hue from 0° to 360° and observe how the dominant fold color rotates through the spectrum.
6. Increase Cascades to 4× and note how the contour bands multiply and narrow.
7. Toggle Luma Invert on to flip which tonal regions develop fold boundaries.

**Key concepts**: Cascading compounds folds exponentially, hue distribution targets specific color axes, secondary channel offsets create multi-axis iridescence, luma inversion reverses the tonal map before folding

---

### Exercise 3: Animated Auto-Sweep Evolution

<BeforeAfterSlider
  sources={[
    { label: "Car", before: rupture_source1_car, after: rupture_ex3_s1 },
    { label: "Sunset", before: rupture_source2_sunset, after: rupture_ex3_s2 },
    { label: "Collage", before: rupture_source3_collage, after: rupture_ex3_s3 },
    { label: "Pattern", before: rupture_source4_pattern, after: rupture_ex3_s4 },
    { label: "Man", before: rupture_source5_man, after: rupture_ex3_s5 },
    { label: "Paint", before: rupture_source6_paint, after: rupture_ex3_s6 },
  ]}
/>
*Animated Auto-Sweep Evolution — simulated result across source images.*
**Source**: Slow-moving or static footage with broad tonal areas — landscapes, architectural footage, or abstract color fields.

**What You'll Create**: Use Auto Sweep to create slowly-evolving iridescent surfaces that shift through the color spectrum over time.

1. Set Cascades to 2× for moderate contour complexity.
2. Set ColDepth to about 55% for well-defined fold boundaries.
3. Set Saturaton to about 70% for vivid secondary channel engagement.
4. Enable Auto Sweep (Toggle 9). Watch the color pattern begin to drift.
5. Set Hue to 0° as a starting point — Auto Sweep will rotate away from it.
6. Reduce Mix to about 70% to soften the effect, blending folded and original.
7. Let the sweep run for 30+ seconds to see a full rotation through all four quadrants.
8. Compare Triangle vs. Clip fold during the sweep — the evolving pattern has a very different character in each mode.

**Key concepts**: Auto-sweep adds a constant DDS increment to the hue each frame, causing continuous rotation through the 4-quadrant color distribution. the mix fader blends between folded and original for softer effects

---


## Tips

- **Auto Sweep for evolving textures**: Enable Auto Sweep and let the hue rotate slowly through the quadrants for continuously-changing iridescent surfaces — particularly effective with video feedback loops.
- **Clip mode for graphic posterization**: When you want hard-edged tonal bands rather than smooth contours, switch to Clip fold type. Combined with low cascade count, this produces clean posterized graphics.
- **Mix for subtlety**: Heavy fold settings can overwhelm the source. Pull the Mix fader down to 40–60% to blend the fold pattern with the original, creating subtle tonal texturing rather than aggressive color inversion.
- **Feedback amplifies folds**: Routing Rupture's output back to its input through an external feedback loop causes each frame's folds to compound on the previous frame's folds, producing rapidly-evolving fractal-like contour patterns.
- **Luma Invert shifts contour placement**: If the fold contours cluster in the wrong part of the image, toggling Luma Invert moves them to the opposite tonal region without changing any other parameter.

---

## Glossary

| Term | Definition |
|------|------------|
| **Auto Sweep** | A DDS-driven slow rotation of the effective hue parameter, causing the fold color distribution to evolve continuously over time. |
| **Cascade** | Multiple fold stages applied in series, where each stage's output feeds the next stage's input, compounding the nonlinear contour effect. |
| **CVI** | Computer Video Instrument; the Fairlight CVI (1984) pioneered real-time video effects including channel-based color folding. |
| **DDS** | Direct Digital Synthesis; a technique for generating continuously-variable waveforms from a fixed-rate accumulator and lookup table. |
| **Fold** | A nonlinear operation that reflects signal values exceeding a threshold back into range, creating contour boundaries in smooth gradients. |
| **Hue Distribution** | A 4-quadrant scheme that assigns different fold offsets to Y, U, and V channels based on the Hue parameter angle. |
| **Iridescence** | The appearance of shifting spectral colors, as seen in oil films, soap bubbles, or beetle shells — an apt visual metaphor for cascaded fold color patterns. |
| **Triangle Fold** | Fold mode where overflow is reflected by bitwise inversion, creating smooth V-shaped contour reversals. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
