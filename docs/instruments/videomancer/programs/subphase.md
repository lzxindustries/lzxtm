---
draft: true
sidebar_position: 292
slug: /instruments/videomancer/subphase
title: "Sub Phase"
image: /img/instruments/videomancer/subphase/subphase_hero_s1.png
description: "Subphase simulates the subcarrier phase errors that plague analog color television reception."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import subphase_control_panel from '/img/instruments/videomancer/subphase/subphase_control_panel.png';
import subphase_source1_parrot from '/img/instruments/videomancer/subphase/subphase_source1_parrot.png';
import subphase_source2_field from '/img/instruments/videomancer/subphase/subphase_source2_field.png';
import subphase_source3_clouds from '/img/instruments/videomancer/subphase/subphase_source3_clouds.png';
import subphase_source4_pattern from '/img/instruments/videomancer/subphase/subphase_source4_pattern.png';
import subphase_source5_girl from '/img/instruments/videomancer/subphase/subphase_source5_girl.png';
import subphase_source6_berries from '/img/instruments/videomancer/subphase/subphase_source6_berries.png';
import subphase_hero_s1 from '/img/instruments/videomancer/subphase/subphase_hero_s1.png';
import subphase_hero_s2 from '/img/instruments/videomancer/subphase/subphase_hero_s2.png';
import subphase_hero_s3 from '/img/instruments/videomancer/subphase/subphase_hero_s3.png';
import subphase_hero_s4 from '/img/instruments/videomancer/subphase/subphase_hero_s4.png';
import subphase_hero_s5 from '/img/instruments/videomancer/subphase/subphase_hero_s5.png';
import subphase_hero_s6 from '/img/instruments/videomancer/subphase/subphase_hero_s6.png';
import subphase_ex1_s1 from '/img/instruments/videomancer/subphase/subphase_ex1_s1.png';
import subphase_ex1_s2 from '/img/instruments/videomancer/subphase/subphase_ex1_s2.png';
import subphase_ex1_s3 from '/img/instruments/videomancer/subphase/subphase_ex1_s3.png';
import subphase_ex1_s4 from '/img/instruments/videomancer/subphase/subphase_ex1_s4.png';
import subphase_ex1_s5 from '/img/instruments/videomancer/subphase/subphase_ex1_s5.png';
import subphase_ex1_s6 from '/img/instruments/videomancer/subphase/subphase_ex1_s6.png';
import subphase_ex2_s1 from '/img/instruments/videomancer/subphase/subphase_ex2_s1.png';
import subphase_ex2_s2 from '/img/instruments/videomancer/subphase/subphase_ex2_s2.png';
import subphase_ex2_s3 from '/img/instruments/videomancer/subphase/subphase_ex2_s3.png';
import subphase_ex2_s4 from '/img/instruments/videomancer/subphase/subphase_ex2_s4.png';
import subphase_ex2_s5 from '/img/instruments/videomancer/subphase/subphase_ex2_s5.png';
import subphase_ex2_s6 from '/img/instruments/videomancer/subphase/subphase_ex2_s6.png';
import subphase_ex3_s1 from '/img/instruments/videomancer/subphase/subphase_ex3_s1.png';
import subphase_ex3_s2 from '/img/instruments/videomancer/subphase/subphase_ex3_s2.png';
import subphase_ex3_s3 from '/img/instruments/videomancer/subphase/subphase_ex3_s3.png';
import subphase_ex3_s4 from '/img/instruments/videomancer/subphase/subphase_ex3_s4.png';
import subphase_ex3_s5 from '/img/instruments/videomancer/subphase/subphase_ex3_s5.png';
import subphase_ex3_s6 from '/img/instruments/videomancer/subphase/subphase_ex3_s6.png';

# Sub Phase

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: subphase_source1_parrot, after: subphase_hero_s1 },
    { label: "Field", before: subphase_source2_field, after: subphase_hero_s2 },
    { label: "Clouds", before: subphase_source3_clouds, after: subphase_hero_s3 },
    { label: "Pattern", before: subphase_source4_pattern, after: subphase_hero_s4 },
    { label: "Girl", before: subphase_source5_girl, after: subphase_hero_s5 },
    { label: "Berries", before: subphase_source6_berries, after: subphase_hero_s6 },
  ]}
/>
*Subphase recreating the look of NTSC and PAL subcarrier phase errors, producing rainbow dot crawl, color drift, and chroma noise reminiscent of analog broadcast reception on a mistuned television.*

---

## Overview

**Subphase** simulates the subcarrier phase errors that plague analog color television reception. In the NTSC and PAL systems, color information is encoded by modulating a high-frequency carrier signal. If the receiver's color oscillator is not perfectly synchronized with the transmitter's, hue drifts, saturation fluctuates, and a pattern of colored dots (called **dot crawl**) appears along high-contrast edges. These artifacts defined the look of broadcast television for decades and are now prized in video art for their nostalgic, degraded aesthetic.

The implementation applies a 2D rotation matrix to the U and V chrominance channels using a 32-entry signed sine/cosine lookup table. The Phase Shift control rotates the UV vector, simulating a misaligned color burst reference. Phase Wobble adds a frame-rate sinusoidal perturbation to the base phase, mimicking oscillator drift. A dot-crawl pattern generator produces the characteristic NTSC (4-phase) or PAL (8-phase) pixel-level chroma artifacts using horizontal and vertical position counters. An LFSR-based noise generator adds broadband chroma noise for further analog degradation.

Subphase is in the **Signal** category — a family of effects that simulate analog signal impairments and processing characteristics.

---

## Quick Start

1. **Subtle phase for "tape" look**: Phase Shift at 5–10% with slight wobble produces the characteristic slightly-off color of VHS playback.
2. **NTSC vs PAL for character**: NTSC crawl is tighter and more aggressive; PAL crawl is broader and subtler. Choose based on the era and region you want to evoke.
3. **Combine with Kinescope**: Subphase for color degradation + Kinescope for scan lines creates a complete vintage TV simulation.

---

## Background

### What Is a Color Subcarrier?

In NTSC and PAL television, color is encoded by modulating a high-frequency sinusoidal carrier within the luminance bandwidth. The NTSC subcarrier frequency is approximately 3.58 MHz; PAL uses approximately 4.43 MHz. The **phase** of this carrier encodes hue, and its **amplitude** encodes saturation. A short burst of the subcarrier at the start of each line (the "color burst") provides the reference phase for the receiver's demodulator. If this reference drifts, all decoded hues rotate.

### What Is Phase Error?

When the receiver's local oscillator does not precisely track the transmitted color burst, a **phase error** develops — a constant or slowly varying angular offset between the transmitted and received color vectors. A static offset shifts all hues uniformly (flesh tones turn green, blue skies become purple). A drifting offset causes hues to rotate continuously over time. This is the artifact that NTSC's nickname "Never The Same Color" describes.

### What Is Dot Crawl?

**Dot crawl** is a visible pattern of alternating colored and luminance dots that appears along high-contrast horizontal edges in composite video. It arises because the chrominance subcarrier frequency is not perfectly orthogonal to the luminance sampling — the demodulator cannot completely separate them. The pattern has a period of 4 pixels in NTSC (because the subcarrier is at ¼ the pixel clock) and 8 pixels in PAL. With animation enabled, the dots appear to "crawl" along edges as the subcarrier phase advances each frame.

### What Is Chroma Noise?

In weak reception conditions, random noise contaminates the color signal more than the luminance because the chrominance occupies a narrower bandwidth with less signal power. The result is visible as random splotches of color shifting frame-to-frame — distinct from luminance noise (snow). Subphase simulates this with an LFSR-generated pseudorandom signal added to both U and V channels.


---

## Signal Flow

Position Counters → Phase Rotation Engine → Dot Crawl Generator → ... → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ X counter (per-pixel, reset on hsync)
│   ├─ Y counter (per-line, reset on vsync)
│   └─ Frame counter (wobble + crawl animation)
│
├── Phase Rotation Engine ──────────────────────────────────────
│   ├─ 1. Base phase         (Phase Shift pot → 0–360°)
│   ├─ 2. Phase wobble       (sin(frame) × wobble amount)
│   ├─ 3. Sine/Cosine LUT  (32-entry signed table)
│   ├─ 4. UV rotation        (U'=U·cos − V·sin; V'=U·sin + V·cos)
│   └─ 5. Burst scaling      (amplitude × Color Burst pot)
│
├── Dot Crawl Generator ────────────────────────────────────────
│   ├─ NTSC mode: period-4 (h_count bits 1:0)
│   ├─ PAL mode: period-8 (h_count bits 2:0) w/ line alternation
│   ├─ Animation: frame_count shifts pattern
│   └─ Modulation: sine LUT lookup → added to UV
│
├── Chroma Noise ───────────────────────────────────────────────
│   ├─ LFSR16 pseudorandom generator
│   ├─ Signed noise → scaled by Chroma Noise pot
│   └─ Added to both U and V channels
│
├── Chroma Kill (optional) ─────────────────────────────────────
│   └─ Force U = V = 512 (monochrome)
│
├── Output ─────────────────────────────────────────────────────
│   ├─ Y: input + brightness offset
│   ├─ U, V: rotated + crawl + noise (or killed)
│   └─ Bypass mux
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through with 6-clock delay
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The UV rotation is the core of the effect — it applies a 2×2 matrix rotation using precomputed sine and cosine values from the 32-entry table. The cosine is implemented as a sine lookup with an 8-entry phase offset (90° in 32-step resolution). After rotation, the Color Burst knob scales the rotated UV amplitudes — at zero, chrominance is zeroed (similar to Chroma Kill but via amplitude reduction). Dot crawl and chroma noise are additive perturbations applied after rotation. The order ensures that phase rotation affects the overall hue, while crawl and noise act as local impairments.

---

## Parameter Reference

<img src={subphase_control_panel} alt="Videomancer front panel with Sub Phase loaded"/>
*Videomancer's front panel with Sub Phase active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Phase Shift
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

At 0% (0°), no hue rotation — colors are unaffected. At 50% (~180°), all colors are rotated to their complement. Intermediate values produce the characteristic color drift of mistuned analog reception. Phase Shift interacts strongly with Phase Wobble — applying base rotation while wobble modulates around it. Internally, controls the color subcarrier phase offset in degrees (0–360° mapped across the full knob range).

---

#### Knob 2 — Phase Wobble
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

At zero, the phase is static. As wobble increases, the hue drifts back and forth sinusoidally over time, simulating an unstable color oscillator. At maximum, the wobble range is large enough to sweep through significant hue changes each second. Internally, controls the amplitude of the sinusoidal phase wobble — a slow frame-rate oscillation of the base phase.

---

#### Knob 3 — Dot Crawl
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

At zero, no dot crawl is visible. As the value increases, a pixel-level periodic pattern of colored dots becomes visible along high-contrast edges. The pattern period depends on the Standard toggle (Switch 7): 4 pixels for NTSC, 8 pixels for PAL. Maximum dot crawl produces an aggressive, visually dominant artifact. Internally, controls the intensity of the dot-crawl pattern.

---

#### Knob 4 — Color Burst
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the color burst amplitude scaling. This acts as a saturation control on the rotated UV channels. At 100%, the full rotated chroma is preserved. At lower values, chroma amplitude is reduced proportionally — at 0%, the output is effectively monochrome (similar to Chroma Kill). This simulates a weak or missing color burst reference signal.

---

#### Knob 5 — Chroma Noise
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

At zero, no noise. Increasing the value adds progressively more random color fluctuation, simulating weak-signal reception. At maximum, the chroma noise dominates the color signal, producing a heavily degraded, noisy image. Internally, controls the amplitude of the LFSR-based chroma noise added to U and V.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC brightness offset to the output luminance. At center (50%), no shift. Above center brightens, below center darkens. Luminance is not otherwise modified by the phase rotation — only chrominance is affected.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Standard** | NTSC | PAL |
| **8 — Crawl Anim** | Static | Animate |
| **9 — Tint Lock** | Off | On |
| **10 — Chroma Kill** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 select the broadcast standard, control crawl animation, lock tint, kill chroma entirely, and bypass. The Standard switch (7) is the most visually distinctive — it changes the dot-crawl periodicity from NTSC's 4-pixel pattern to PAL's 8-pixel pattern with line alternation.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the processed (phase-rotated, crawl, noise) signal and the original input via the hardware interpolator. At 100%, the full analog degradation is applied. Lowering the fader smoothly blends back toward the clean original.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Sub Phase processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises explore hue rotation, the NTSC/PAL dot-crawl artifact, and chroma noise for analog broadcast simulation.

### Exercise 1: Color Phase Drift

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: subphase_source1_parrot, after: subphase_ex1_s1 },
    { label: "Field", before: subphase_source2_field, after: subphase_ex1_s2 },
    { label: "Clouds", before: subphase_source3_clouds, after: subphase_ex1_s3 },
    { label: "Pattern", before: subphase_source4_pattern, after: subphase_ex1_s4 },
    { label: "Girl", before: subphase_source5_girl, after: subphase_ex1_s5 },
    { label: "Berries", before: subphase_source6_berries, after: subphase_ex1_s6 },
  ]}
/>
*Color Phase Drift — simulated result across source images.*
**Source**: Camera feed of a color chart, face, or scene with known natural colors (skin tones, foliage, sky).

**What You'll Create**: Demonstrate the effect of subcarrier phase error on perceived hue.

1. **Base phase rotation**: Slowly sweep Phase Shift from 0% to 100%. Watch all colors rotate through the spectrum — skin tones shift from natural to greenish to purple and back.
2. **90° offset**: Set Phase Shift to ~25% (≈90°). All colors are rotated by one quadrant — reds become blue-green, blues become orange.
3. **180° complement**: Set Phase Shift to ~50% (≈180°). All colors flip to their complement.
4. **Phase wobble**: Add Phase Wobble at ~30%. Colors begin to drift back and forth slowly. This is the "Never The Same Color" look.
5. **Color burst**: Lower Color Burst to ~50%. The rotated colors become less saturated, as if the receiver is losing color lock.
6. **Note**: Luminance (Y) is unaffected throughout — only hue and saturation change.

**Key concepts**: Phase rotation shifts all hues uniformly, wobble simulates oscillator drift, color burst controls saturation, luminance is independent of phase

---

### Exercise 2: NTSC Dot Crawl

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: subphase_source1_parrot, after: subphase_ex2_s1 },
    { label: "Field", before: subphase_source2_field, after: subphase_ex2_s2 },
    { label: "Clouds", before: subphase_source3_clouds, after: subphase_ex2_s3 },
    { label: "Pattern", before: subphase_source4_pattern, after: subphase_ex2_s4 },
    { label: "Girl", before: subphase_source5_girl, after: subphase_ex2_s5 },
    { label: "Berries", before: subphase_source6_berries, after: subphase_ex2_s6 },
  ]}
/>
*NTSC Dot Crawl — simulated result across source images.*
**Source**: High-contrast graphic content with sharp horizontal edges (text, horizontal bars, checkerboard) — dot crawl is most visible along these boundaries.

**What You'll Create**: Reproduce the characteristic NTSC dot-crawl artifact along high-contrast edges.

1. **Enable crawl**: Set Dot Crawl to ~60%. A periodic pattern of colored dots appears along sharp edges.
2. **Animate**: Set Crawl Anim to Animate (Switch 8). The dots begin to move along the edges, producing the classic crawling artifact.
3. **Compare NTSC/PAL**: Toggle Standard (Switch 7). NTSC shows a 4-pixel pattern; PAL shows an 8-pixel pattern with line alternation. The visual character is distinctly different.
4. **Phase + crawl**: Add a slight Phase Shift (~10%). The crawl dots take on the shifted hue character.
5. **Maximum crawl**: Push Dot Crawl to 100%. The artifact becomes dominant — the entire image shimmers with color fringing.
6. **Static freeze**: Set Crawl Anim back to Static. The dots freeze in place.

**Key concepts**: Dot crawl has standard-specific periodicity (4 vs 8 pixels), animation creates the "crawling" motion, crawl intensity is independently controllable

---

### Exercise 3: Weak Signal Reception

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: subphase_source1_parrot, after: subphase_ex3_s1 },
    { label: "Field", before: subphase_source2_field, after: subphase_ex3_s2 },
    { label: "Clouds", before: subphase_source3_clouds, after: subphase_ex3_s3 },
    { label: "Pattern", before: subphase_source4_pattern, after: subphase_ex3_s4 },
    { label: "Girl", before: subphase_source5_girl, after: subphase_ex3_s5 },
    { label: "Berries", before: subphase_source6_berries, after: subphase_ex3_s6 },
  ]}
/>
*Weak Signal Reception — simulated result across source images.*
**Source**: Any video content — the noise effect applies uniformly.

**What You'll Create**: Simulate the look of a weak analog broadcast signal with phase drift, crawl, and chroma noise combined.

1. **Phase wobble**: Set Phase Wobble to ~40%. Colors drift slowly.
2. **Dot crawl**: Set Dot Crawl to ~30%. Subtle edge crawl appears.
3. **Chroma noise**: Set Chroma Noise to ~50%. Random color splotches appear across the image.
4. **Reduced burst**: Lower Color Burst to ~60%. Colors become somewhat washed out.
5. **Animate crawl**: Enable crawl animation. The combination of wobble, crawl, and noise mimics a distant UHF station.
6. **Increase noise**: Push Chroma Noise to ~80%. The color signal is nearly buried in noise — reminiscent of rabbit-ear reception in a storm.
7. **Kill chroma**: Enable Chroma Kill (Switch 10). All color vanishes — pure monochrome with no noise or crawl visible.

**Key concepts**: Multiple analog impairments can be combined for layered degradation, chroma noise is independent of phase rotation, Chroma Kill overrides everything

---


## Tips

- **Chroma noise for atmosphere**: Even a small amount of chroma noise (~10–20%) adds organic analog texture without overwhelming the image.
- **Tint Lock for consistency**: Use Tint Lock when you want consistent color across a performance while still using Dot Crawl and Noise.
- **Chroma Kill for B&W**: Chroma Kill is a clean way to produce monochrome output while leaving all other processing intact.
- **Layer with feedback**: Feed Subphase output back through Feedback for accumulating hue drift — colors spiral through the spectrum.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chroma Noise** | Random fluctuations in the chrominance signal, simulating weak-signal reception quality. |
| **Color Burst** | A short sinusoidal reference signal at the beginning of each video line, used by receivers to lock their color demodulation oscillator. |
| **Color Subcarrier** | The high-frequency sinusoidal carrier (~3.58 MHz NTSC, ~4.43 MHz PAL) that carries encoded color information within the composite video signal. |
| **Dot Crawl** | A visible artifact of composite video where luminance/chrominance crosstalk creates a moving pattern of colored dots along high-contrast edges. |
| **LFSR** | Linear Feedback Shift Register; a pseudorandom number generator used to produce the chroma noise. |
| **NTSC** | National Television System Committee; the analog color TV standard used in North America and Japan, with a 4-pixel subcarrier period. |
| **PAL** | Phase Alternating Line; the analog color TV standard used in Europe and elsewhere, with line-by-line phase alternation to reduce hue sensitivity. |
| **Phase Error** | The angular offset between the transmitted color burst and the receiver's local oscillator, causing systematic hue rotation. |
| **UV Rotation** | A 2×2 matrix operation that rotates the chrominance vector (U, V) by a given angle, changing the perceived hue of all colors simultaneously. |

---
