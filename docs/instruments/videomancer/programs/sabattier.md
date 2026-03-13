---
draft: false
sidebar_position: 254
slug: /instruments/videomancer/sabattier
title: "Sabattier"
image: /img/instruments/videomancer/sabattier/sabattier_hero_s1.png
description: "In the traditional photographic darkroom, the Sabattier effect occurs when a partially developed print is briefly re-exposed to light."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import sabattier_control_panel from '/img/instruments/videomancer/sabattier/sabattier_control_panel.png';
import sabattier_source1_sunset from '/img/instruments/videomancer/sabattier/sabattier_source1_sunset.png';
import sabattier_source2_castle from '/img/instruments/videomancer/sabattier/sabattier_source2_castle.png';
import sabattier_source3_elephant from '/img/instruments/videomancer/sabattier/sabattier_source3_elephant.png';
import sabattier_source4_pattern from '/img/instruments/videomancer/sabattier/sabattier_source4_pattern.png';
import sabattier_source5_boy from '/img/instruments/videomancer/sabattier/sabattier_source5_boy.png';
import sabattier_source6_paint from '/img/instruments/videomancer/sabattier/sabattier_source6_paint.png';
import sabattier_hero_s1 from '/img/instruments/videomancer/sabattier/sabattier_hero_s1.png';
import sabattier_hero_s2 from '/img/instruments/videomancer/sabattier/sabattier_hero_s2.png';
import sabattier_hero_s3 from '/img/instruments/videomancer/sabattier/sabattier_hero_s3.png';
import sabattier_hero_s4 from '/img/instruments/videomancer/sabattier/sabattier_hero_s4.png';
import sabattier_hero_s5 from '/img/instruments/videomancer/sabattier/sabattier_hero_s5.png';
import sabattier_hero_s6 from '/img/instruments/videomancer/sabattier/sabattier_hero_s6.png';
import sabattier_ex1_s1 from '/img/instruments/videomancer/sabattier/sabattier_ex1_s1.png';
import sabattier_ex1_s2 from '/img/instruments/videomancer/sabattier/sabattier_ex1_s2.png';
import sabattier_ex1_s3 from '/img/instruments/videomancer/sabattier/sabattier_ex1_s3.png';
import sabattier_ex1_s4 from '/img/instruments/videomancer/sabattier/sabattier_ex1_s4.png';
import sabattier_ex1_s5 from '/img/instruments/videomancer/sabattier/sabattier_ex1_s5.png';
import sabattier_ex1_s6 from '/img/instruments/videomancer/sabattier/sabattier_ex1_s6.png';
import sabattier_ex2_s1 from '/img/instruments/videomancer/sabattier/sabattier_ex2_s1.png';
import sabattier_ex2_s2 from '/img/instruments/videomancer/sabattier/sabattier_ex2_s2.png';
import sabattier_ex2_s3 from '/img/instruments/videomancer/sabattier/sabattier_ex2_s3.png';
import sabattier_ex2_s4 from '/img/instruments/videomancer/sabattier/sabattier_ex2_s4.png';
import sabattier_ex2_s5 from '/img/instruments/videomancer/sabattier/sabattier_ex2_s5.png';
import sabattier_ex2_s6 from '/img/instruments/videomancer/sabattier/sabattier_ex2_s6.png';
import sabattier_ex3_s1 from '/img/instruments/videomancer/sabattier/sabattier_ex3_s1.png';
import sabattier_ex3_s2 from '/img/instruments/videomancer/sabattier/sabattier_ex3_s2.png';
import sabattier_ex3_s3 from '/img/instruments/videomancer/sabattier/sabattier_ex3_s3.png';
import sabattier_ex3_s4 from '/img/instruments/videomancer/sabattier/sabattier_ex3_s4.png';
import sabattier_ex3_s5 from '/img/instruments/videomancer/sabattier/sabattier_ex3_s5.png';
import sabattier_ex3_s6 from '/img/instruments/videomancer/sabattier/sabattier_ex3_s6.png';

# Sabattier

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: sabattier_source1_sunset, after: sabattier_hero_s1 },
    { label: "Castle", before: sabattier_source2_castle, after: sabattier_hero_s2 },
    { label: "Elephant", before: sabattier_source3_elephant, after: sabattier_hero_s3 },
    { label: "Pattern", before: sabattier_source4_pattern, after: sabattier_hero_s4 },
    { label: "Boy", before: sabattier_source5_boy, after: sabattier_hero_s5 },
    { label: "Paint", before: sabattier_source6_paint, after: sabattier_hero_s6 },
  ]}
/>
*Sabattier applying pseudo-solarization with Mackie line edge glow and metallic tinting to create surreal darkroom-inspired tonal reversals.*

---

## Overview

In the traditional photographic darkroom, the Sabattier effect occurs when a partially developed print is briefly re-exposed to light. Midtones undergo a dramatic tonal reversal — they darken while shadows and highlights remain relatively stable — producing a surreal, otherworldly image with luminous borders at tonal boundaries. These bright halos, called Mackie lines, form where bromide ions migrate outward from developed regions into adjacent undeveloped areas, creating a thin luminous edge that traces every significant tonal transition.

Sabattier recreates this entire photographic phenomenon in the digital domain. The program applies a piecewise solarization curve that selectively inverts midtone luminance, producing the characteristic partial tonal reversal. A horizontal gradient detector identifies tonal boundaries and generates additive Mackie line edge glow with configurable gain and IIR-based width spread. An optional metallic tinting stage shifts chroma based on luminance to simulate the silvery, mercury-like sheen that characterizes well-executed solarized darkroom prints. The Y and UV channels can be solarized independently or together, and two curve shapes — single-fold S-curve and double-fold W-curve — offer different reversal patterns.

At subtle settings, Sabattier adds gentle edge luminosity and tonal compression that evokes vintage photographic prints. At extreme settings, it produces hard tonal inversions, vivid Mackie halos, and metallic color shifts that transform video into abstract graphic structures bearing little resemblance to the source material.

---

## Quick Start

1. **Start with Y Inversion alone**: Before engaging Mackie or Tint, explore the solarization curve by itself. The curve shape is the foundation of the entire effect.
2. **Threshold cleans up noise**: If the image looks too busy with Mackie lines everywhere, increase Threshold to suppress weak edges and keep only the major contours.
3. **Mackie Width vs Mackie Gain**: Gain controls *brightness* of the edge glow; Width controls *spread*. High Gain + low Width creates sharp bright lines. Low Gain + high Width creates soft diffuse halos.

---

## Background

### The Sabattier Effect in Photography

The Sabattier effect was first documented by Armand Sabattier in 1862, though it is often incorrectly attributed to Man Ray, who popularized it in the 1930s under the name "solarization." The true photographic process involves interrupting development, exposing the partially-processed emulsion to a controlled burst of light, and then continuing development. Unexposed silver halide crystals — those in areas that received little original exposure (highlights and bright midtones in the negative) — respond to the second exposure and begin developing, while already-developed areas are largely unaffected. The result is a partial reversal of tonal values concentrated in the midtone range.

### Mackie Lines

The most visually distinctive artifact of the Sabattier effect is the Mackie line: a thin, bright border that appears at every significant tonal boundary. During development, bromide ions are released as a byproduct of silver reduction. In regions of heavy development (dark areas of the print), these ions migrate laterally into adjacent lighter regions, locally inhibiting further development. This chemical diffusion creates a narrow zone of reduced density — a bright line — at every edge where dark meets light. In Videomancer's digital implementation, horizontal gradient detection identifies these tonal boundaries, and an IIR filter controls the width of the simulated line.

### Solarization Curves

A linear transfer function maps input brightness directly to output brightness with no tonal reversal. The Sabattier S-curve deviates from linearity by pulling midtone values downward: pixels near the midpoint (512 in 10-bit space) lose brightness proportional to their proximity to center. This creates a "dip" or valley in the transfer curve at the midpoint. The W-curve extends this concept with two dips centered at the quarter and three-quarter points (256 and 768), producing a double reversal that creates more complex tonal banding with additional contour lines.

### Equidensity Contours

When the equidensity mode is engaged, the solarization dip is doubled in magnitude, producing narrower, more sharply defined tonal bands. The resulting image resembles an equidensity plate — a photographic technique used in scientific imaging to visualize subtle brightness differences. In scientific applications, equidensity photography reveals structures invisible in standard prints by mapping narrow brightness ranges to distinct tonal bands. In Sabattier's artistic context, the effect produces bold graphic contour lines that outline tonal regions of the source.

### Metallic Tinting

Traditional solarized prints often exhibit a characteristic metallic sheen — a silvery, blue-gray quality that arises from the unusual distribution of developed silver in the emulsion. Sabattier's tinting stage simulates this by shifting the U and V chrominance channels in opposite directions as a function of luminance. Bright areas receive a warm silver shift (increased V, decreased U) while dark areas shift cooler. The magnitude of the shift is proportional to the tint control and the pixel's distance from neutral gray, creating a luminance-dependent coloration that evolves organically across the image.


---

## Signal Flow

Input → UV Solarization → Mackie Line Spread → Metallic Tint

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input + Polarity + Y Solarization ─────────────────
│   ├─ Polarity toggle → optional Y inversion (1023 − Y)
│   └─ Sabattier curve on Y (S-curve or W-curve, equidensity ×2)
│      Amount controlled by Y Inversion knob
│
├── Stage 2: UV Solarization + Mackie Gradient ──────────────────
│   ├─ If Channel = YUV: apply Sabattier curve to U and V
│   │   Amount controlled by UV Inversion knob
│   ├─ Delay Y by 2 samples for centered gradient
│   └─ Gradient = |Y[current] − Y[2-pixel-delayed]|
│      Gate: pass only if gradient > Threshold
│
├── Stage 3: Mackie Line Spread + Overlay ───────────────────────
│   ├─ Scale gradient by Mackie Gain
│   ├─ IIR width spread: blend = α × prev + (1−α) × new
│   │   α controlled by Mackie Width (top 4 bits → 0–15)
│   └─ Overlay: Y_out = clamp(Y_solarized + Mackie_glow, 0, 1023)
│
├── Stage 4: Metallic Tint ─────────────────────────────────────
│   ├─ Y passes through unchanged
│   ├─ tint_k = Tint >> 2 → tint_prod = tint_k × Y
│   ├─ U += tint_prod upper bits (shift toward blue-silver)
│   └─ V −= tint_prod upper bits (shift toward green-silver)
│
├── Interpolator (4 clk) ───────────────────────────────────────
│   └─ Mix: lerp(dry, wet, Mix fader)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

Two key interactions define the character of the output. First, the Mackie line detection operates on the *solarized* Y signal, not the original — this means edge glow appears at the tonal boundaries *created by* the solarization curve, not just at edges present in the source. As Y Inversion increases and the curve creates more midtone reversal, the gradient magnitude at newly-formed tonal boundaries increases, automatically generating stronger Mackie lines without changing the Mackie Gain setting. Second, the metallic tint is applied *after* Mackie overlay, so the bright Mackie glow lines receive their own luminance-dependent color shift, giving them a characteristic silvery gleam against the solarized background tones.

---

## Parameter Reference

<img src={sabattier_control_panel} alt="Videomancer front panel with Sabattier loaded"/>
*Videomancer's front panel with Sabattier active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Inversion
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At 0%, no midtone reversal occurs and the signal passes through with a linear transfer. As you increase the control, midtone values are progressively pulled downward — pulled toward black — while shadows and highlights remain stable. At maximum, the midtone dip is at its deepest, producing strong tonal reversal with pronounced contour boundaries. The shape of the dip is selected by the Curve Shape toggle (S-curve or W-curve). Internally, controls the depth of the Sabattier solarization curve applied to the Y (luminance) channel.

---

#### Knob 2 — UV Inversion
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the depth of Sabattier solarization applied to the U and V (chrominance) channels. This control only takes effect when the Channel toggle is set to YUV — in Y Only mode, chrominance passes through unmodified. When active, chroma solarization creates color reversals at midtone chroma values, producing surreal color shifts where moderately saturated areas invert toward their complementary hues while fully saturated and neutral regions remain stable.

---

#### Knob 3 — Mackie Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the brightness multiplier for the Mackie line edge glow. The raw gradient magnitude from the horizontal edge detector is multiplied by this gain value. At 0%, no Mackie lines are visible regardless of edge content. At moderate settings, subtle luminous borders appear at major tonal transitions. At high settings, the Mackie glow dominates the image, with bright halos overwhelming the solarized tones beneath. The gain product is clamped at 512 to prevent overflow artifacts.

---

#### Knob 4 — Mackie Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the spatial spread of Mackie lines via a horizontal IIR low-pass filter. The top 4 bits of the register set the blend ratio between the current Mackie value and the previous pixel's IIR output. At 0%, Mackie lines are sharp single-pixel edges. As you increase the width, the IIR feedback spreads the glow horizontally across multiple pixels, creating broad luminous halos. Very high settings can spread the glow across large portions of the scanline, creating a soft horizontal bloom.

---

#### Knob 5 — Tint
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At 0%, no tinting occurs. As you increase the control, bright regions shift toward blue-silver (U increases, V decreases) and dark regions shift in the opposite direction. The shift magnitude is proportional to both the tint setting and the pixel luminance, creating a smooth gradient of metallic coloration across the tonal range. Internally, controls the magnitude of luminance-dependent chrominance shift that simulates the metallic appearance of solarized prints.

---

#### Knob 6 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Sets the minimum gradient magnitude required for Mackie line detection to fire. Gradients below this threshold produce no edge glow. At 0%, even the slightest tonal transition generates Mackie lines, which can create a noisy, busy appearance. Increasing the threshold progressively eliminates weaker edges, leaving only the strongest tonal boundaries highlighted. Use this control to focus the Mackie effect on major contours while suppressing noise and fine texture.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Equidensity** | Off | On |
| **8 — Polarity** | Positive | Negative |
| **9 — Channel** | Y Only | YUV |
| **10 — Curve Shape** | S-Curve | W-Curve |
| **11 — Bypass** | Off | On |

The five toggles independently control the solarization character. Equidensity and Curve Shape modify the transfer curve itself. Polarity inverts the input before the curve is applied, which changes *which* tonal regions undergo reversal. Channel determines whether chrominance is solarized alongside luminance. Bypass provides instant A/B comparison. None of the toggles interact with each other in hardware — each independently gates or modifies a specific pipeline stage.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet crossfade between the original unprocessed signal and the fully solarized output. At 0%, the output is entirely dry (original). At 100%, the output is entirely wet (processed). Intermediate values blend the two, which can create subtle solarization effects where the Mackie lines and tonal reversals are partially transparent over the source.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Sabattier processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises progress from basic solarization curves to complex multi-parameter interactions, building familiarity with each stage of the processing pipeline.

### Exercise 1: Basic Solarization

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: sabattier_source1_sunset, after: sabattier_ex1_s1 },
    { label: "Castle", before: sabattier_source2_castle, after: sabattier_ex1_s2 },
    { label: "Elephant", before: sabattier_source3_elephant, after: sabattier_ex1_s3 },
    { label: "Pattern", before: sabattier_source4_pattern, after: sabattier_ex1_s4 },
    { label: "Boy", before: sabattier_source5_boy, after: sabattier_ex1_s5 },
    { label: "Paint", before: sabattier_source6_paint, after: sabattier_ex1_s6 },
  ]}
/>
*Basic Solarization — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a wide tonal range — faces, landscapes, or test charts with smooth gradients.

**What You'll Create**: Understand how the Sabattier curve creates midtone reversal and generates Mackie lines.

1. **Initialize**: Set all knobs to defaults. Verify bypass is Off and the image passes through unchanged.
2. **Engage Y solarization**: Slowly increase Y Inversion from 0% to about 50%. Watch midtones darken while shadows and highlights remain stable.
3. **Observe Mackie lines**: With Y Inversion at 50%, set Mackie Gain to about 50%. Bright edge halos appear at tonal boundaries.
4. **Adjust threshold**: Sweep Threshold from 0% toward 50%. Weaker edges disappear, leaving only major contour lines.
5. **Compare S vs W**: Toggle Curve Shape between S-Curve and W-Curve. W-Curve produces more complex banding with additional contour lines.

**Key concepts**: Sabattier solarization is midtone-specific tonal reversal, Mackie lines appear at tonal boundaries created by the curve, Threshold filters out weak edges

---

### Exercise 2: Metallic Portraiture

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: sabattier_source1_sunset, after: sabattier_ex2_s1 },
    { label: "Castle", before: sabattier_source2_castle, after: sabattier_ex2_s2 },
    { label: "Elephant", before: sabattier_source3_elephant, after: sabattier_ex2_s3 },
    { label: "Pattern", before: sabattier_source4_pattern, after: sabattier_ex2_s4 },
    { label: "Boy", before: sabattier_source5_boy, after: sabattier_ex2_s5 },
    { label: "Paint", before: sabattier_source6_paint, after: sabattier_ex2_s6 },
  ]}
/>
*Metallic Portraiture — simulated result across source images.*
**Source**: Close-up portrait footage or footage with strong facial features and varied skin tones.

**What You'll Create**: Create the characteristic metallic, mercury-like appearance of classic solarized prints.

1. **Set moderate solarization**: Y Inversion at about 50%, Mackie Gain at about 40%.
2. **Add Mackie width**: Increase Mackie Width to about 50% to create soft, broad halos around facial features.
3. **Engage metallic tint**: Slowly increase Tint from 0% to about 50%. Observe the silvery blue-green shift that appears across the tonal range.
4. **Enable polarity**: Toggle Polarity to Negative. The solarization character changes dramatically, often producing a more dramatic metallic look on skin tones.
5. **Refine threshold**: Set Threshold to about 15–20% to keep only the strongest Mackie lines active.

**Key concepts**: Metallic tinting is luminance-dependent chroma shift, Polarity inversion changes which tones are reversed, Mackie Width IIR controls edge glow spread

---

### Exercise 3: Equidensity Contour Map

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: sabattier_source1_sunset, after: sabattier_ex3_s1 },
    { label: "Castle", before: sabattier_source2_castle, after: sabattier_ex3_s2 },
    { label: "Elephant", before: sabattier_source3_elephant, after: sabattier_ex3_s3 },
    { label: "Pattern", before: sabattier_source4_pattern, after: sabattier_ex3_s4 },
    { label: "Boy", before: sabattier_source5_boy, after: sabattier_ex3_s5 },
    { label: "Paint", before: sabattier_source6_paint, after: sabattier_ex3_s6 },
  ]}
/>
*Equidensity Contour Map — simulated result across source images.*
**Source**: Footage with broad smooth gradients — skies, studio lighting sweeps, or gradient test patterns.

**What You'll Create**: Use equidensity mode with W-curve to produce topographic contour-like banding with full YUV processing.

1. **Enable equidensity**: Toggle Equidensity On.
2. **Select W-Curve**: Toggle Curve Shape to W-Curve for double-fold banding.
3. **Set high Y Inversion**: Increase Y Inversion to about 80%. The doubled W-curve creates sharply defined tonal bands.
4. **Enable YUV processing**: Toggle Channel to YUV, then increase UV Inversion to about 60%. Color bands appear alongside luminance contours.
5. **Mackie lines**: Set Mackie Gain to about 60%, Threshold to about 10%. The contour boundaries glow with bright Mackie lines.
6. **Tint**: Add about 30% Tint for a subtle metallic coloration of the contour bands.

**Key concepts**: Equidensity doubles solarization depth for sharper bands, W-curve creates two reversal zones, combined YUV solarization creates color contours, Mackie lines trace contour boundaries

---


## Tips

- **Polarity is not just inversion**: Polarity inverts *before* the solarization curve, which changes which tonal regions get reversed — it is fundamentally different from applying the curve and then inverting the result.
- **Equidensity + W-Curve is the most complex mode**: The doubled double-fold produces the highest density of tonal bands and Mackie contour lines. Start with S-Curve and Equidensity Off, then build up.
- **Feedback creates evolution**: Routing the output back to the input creates evolving solarization — the Mackie lines generate new tonal boundaries which in turn create new Mackie lines on the next pass.
- **UV Inversion needs Channel = YUV**: The UV Inversion knob has no effect when Channel is set to Y Only. Switch to YUV mode first.
- **Tint after solarization**: The metallic tint acts on the solarized luminance values, so the tint pattern follows the post-curve tonal structure, not the original.

---

## Glossary

| Term | Definition |
|------|------------|
| **Equidensity** | A photographic technique that produces narrow tonal bands by exaggerating brightness differences; in Sabattier, it doubles the solarization dip. |
| **IIR** | Infinite Impulse Response; a feedback filter where each output depends on previous outputs. Used for Mackie line width spread. |
| **Mackie Line** | A luminous border at tonal boundaries in solarized prints, caused by bromide ion migration during development. Simulated here via horizontal gradient detection. |
| **Midtone Reversal** | The defining characteristic of solarization: brightness values near the midpoint are pulled downward while extremes remain stable. |
| **Polarity** | The sign of the input signal. Negative polarity inverts Y before the solarization curve is applied. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage. Used internally for metallic tinting. |
| **Sabattier Effect** | Partial tonal reversal caused by re-exposing a developing photographic print to light, described by Armand Sabattier in 1862. |
| **Solarization** | Broadly, any tonal reversal in photography. In Videomancer, specifically the Sabattier pseudo-solarization curve. |
| **W-Curve** | A double-fold solarization curve with two midtone dips at the quarter and three-quarter points, producing more complex banding than the single-fold S-curve. |

---
