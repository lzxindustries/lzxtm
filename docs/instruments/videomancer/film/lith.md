---
draft: true
sidebar_position: 166
slug: /instruments/videomancer/lith
title: "Lith"
image: /img/instruments/videomancer/lith/lith_hero.png
description: "In the photographic darkroom, lith printing is a process that defies conventional wisdom."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import lith_hero from '/img/instruments/videomancer/lith/lith_hero.png';
import lith_control_panel from '/img/instruments/videomancer/lith/lith_control_panel.png';
import lith_exercise1_result from '/img/instruments/videomancer/lith/lith_exercise1_result.png';
import lith_exercise2_result from '/img/instruments/videomancer/lith/lith_exercise2_result.png';
import lith_exercise3_result from '/img/instruments/videomancer/lith/lith_exercise3_result.png';
import lith_source1_kodim03 from '/img/instruments/videomancer/lith/lith_source1_kodim03.png';
import lith_source2_kodim13 from '/img/instruments/videomancer/lith/lith_source2_kodim13.png';
import lith_source3_kodim13_bw from '/img/instruments/videomancer/lith/lith_source3_kodim13_bw.png';

# Lith

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: lith_source1_kodim03, after: lith_hero },
    { label: "Kodim13", before: lith_source2_kodim13, after: lith_hero },
    { label: "Kodim13 B&W", before: lith_source3_kodim13_bw, after: lith_hero },
  ]}
/>
*Lith applying infectious development processing to transform video into ultra-high-contrast prints with warm brown shadow tones and papery highlights.*

---

## Overview

In the photographic darkroom, lith printing is a process that defies conventional wisdom. You deliberately overexpose silver gelatin paper by two to four stops, then develop the print in extremely dilute lith developer — so dilute that development proceeds at a glacial pace. The chemistry exhausts differently in shadows than in highlights, creating a phenomenon called *infectious development*: once a dark area begins to develop, it accelerates its own development and the development of neighboring areas, producing an abrupt, almost binary transition between black and white. The highlights, meanwhile, develop slowly and never reach full density, settling into soft, creamy tones — the characteristic "papery" whites that lith printers prize.

Lith recreates this photochemical process in the digital domain. The program constructs a nonlinear transfer curve that mimics the infectious development step function: below the exposure threshold, values collapse to black; above it, they rise rapidly to a configurable paper white. The mid-tone transition zone — where the chemistry fights between development and exhaustion — is where the most interesting things happen. Grain concentrates in this transition zone, warm brown toning appears in the shadows, and optional split-tone processing adds cool blue-grey accents to the highlights. The name is simply the darkroom shorthand for the technique itself.

At moderate settings, Lith produces the subtle warmth and gentle grain of a carefully processed darkroom print. At extreme settings, it reduces the image to stark black-and-white silhouettes with hot paper whites and deep, warm blacks — the signature lith aesthetic that photographers spend hours chasing in the darkroom.

---

## Background

### Infectious Development

The key to lith printing is the developer chemistry. Standard photographic developers work linearly — exposed silver halide crystals develop at a rate proportional to their exposure. Lith developer works differently. It contains a low concentration of hydroquinone as the sole active developing agent, and development is *autocatalytic*: the byproducts of the reduction reaction (bromide ions and oxidized hydroquinone) alter the local pH, which accelerates the reaction. In areas of heavy exposure, this feedback loop causes development to accelerate exponentially once it passes a critical threshold. Areas just below that threshold barely develop at all. The result is an extremely steep transfer curve in the mid-tones — a cliff rather than a slope. This is the "infection" that gives the technique its name.

### Exposure and Paper White

In the darkroom, lith printers control two key variables: the enlarger exposure time (which sets where the threshold falls on the tonal scale) and the development time (which determines the paper white — how bright the highlights get before you pull the print from the developer). Lith's Exposure knob maps directly to the enlarger exposure bias, shifting the threshold up or down the luminance range. The Paper knob maps to the development endpoint, setting the maximum brightness that highlights can reach. Together, these two controls define the basic "negative space" of the lith print — how much of the image is black, how much is paper white, and where the cliff falls between them.

### Dilute vs. Strong Developer

Real lith printing uses dilute developer — typically 1:4 to 1:9 dilutions of a standard stock solution. The more dilute the chemistry, the more gradual the onset of infectious development and the wider the transition zone. Concentrated developer produces a harder, more abrupt step. Lith's Developer toggle switches between these two behaviors: Dilute mode preserves a wider range of mid-tone values through the transition (using the Infection control to set the steepness), while Strong mode creates a harder binary step that collapses the mid-tones more aggressively.

### Toning and Split Tone

Lith prints are naturally warm-toned because the image is formed primarily by the lower-contrast developing agent (hydroquinone) rather than the faster, cooler-toned agents used in standard developers. The warm brown color is most visible in the shadow regions where infectious development has run to completion. Lith's Warmth control simulates this by shifting the U and V chroma channels toward brown in areas where luma falls below the mid-tone threshold. The Split Tone toggle adds a complementary cool shift to the highlight regions, creating the classic warm-shadow / cool-highlight aesthetic sought by fine-art printers.

### Film Grain

Lith prints exhibit pronounced grain, but it is not uniformly distributed. The grain concentrates in the transition zone — the narrow band of tones where the chemistry is indecisive, hovering between development and exhaustion. Fully developed (black) areas and undeveloped (paper white) areas show minimal grain. Lith replicates this behavior by gating the LFSR noise signal with a mid-tone flag, applying grain only to pixels that fall within the transition zone between the low and high threshold edges.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register            (1 clk — latch Y)
│   ├─ 2. Threshold Edge Calc       (1 clk — low/mid/high edges from Exposure + Spread)
│   ├─ 3. Transfer Curve            (1 clk — infectious dev step function + mid-tone flag)
│   ├─ 4. Toning + Grain Calc       (1 clk — warm brown U/V shift + LFSR grain)
│   ├─ 5. Grain Apply + Split Tone  (1 clk — mid-tone grain + cool highlights + invert)
│   └─ 6. Interpolator              (4 clk — wet/dry mix)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 4. Warm Tone (shadows)       (brown shift from Warmth, neutral in highlights)
│   ├─ 5. Split Tone (highlights)   (cool shift when enabled, warm shadows preserved)
│   └─ 6. Interpolator              (4 clk — wet/dry mix)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline (9 clk matched)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical interaction is between the threshold edge calculation (Stage 2) and the transfer curve (Stage 3). Exposure sets the center point of the transition, Spread sets its width, Infection controls the steepness within that zone, and Developer selects between two families of curves. The mid-tone flag generated in Stage 3 gates the grain in Stage 5, ensuring grain appears only in the transition zone — exactly where real lith chemistry produces visible grain. Toning in Stage 4 is gated by a fixed luma threshold of 400 (roughly 39% brightness), placing warm brown color only in the shadow regions regardless of where the Exposure control is set.

---

## Parameter Reference

<img src={lith_control_panel} alt="Videomancer front panel with Lith loaded"/>
*Videomancer's front panel with Lith active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Exposure
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Exposure sets the center point of the lith threshold — the luminance value around which the infectious development transition occurs. Think of it as the enlarger exposure dial in the darkroom. Low values place the threshold near black, leaving most of the image as paper white. High values push the threshold up, sending more of the image into the developed (dark) zone. The Spread control widens the transition zone around this center point, and the Infection control determines how steep the curve is within that zone.

---

#### Knob 2 — Infectn
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 68% |
| Suffix | % |

Infection controls the steepness of the infectious development transfer curve within the transition zone. At low values, the transition from black to paper white is gradual — a soft slope with multiple intermediate tones. At high values, the transition becomes abrupt — a near-vertical cliff that mimics the autocatalytic feedback of real lith chemistry. The behavior changes depending on the Developer toggle: in Dilute mode, four discrete steepness levels produce a range of gradual transitions; in Strong mode, the curve snaps between a hard binary step and a slightly softer step.

---

#### Knob 3 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Spread controls the width of the mid-tone transition zone — the range of input luminance values that fall between pure black and paper white. Wide spread creates a broad transition with more room for grain, toning, and intermediate tones. Narrow spread compresses the transition to a thin band, producing a harder silhouette effect. The minimum spread is 16 counts (the +8 offset ensures there is always a finite transition zone even at the zero setting).

---

#### Knob 4 — Grain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

Grain controls the intensity of the LFSR-based noise added to the transition zone. The noise is only applied where the mid-tone flag is active — pixels that fall between the low and high threshold edges. At zero, the lith effect is clean and graphic. As grain increases, the transition zone fills with random texture that breaks up the hard edge between black and white. The Grain toggle (Switch 8) selects between fine grain (6-bit LFSR range, subtle) and coarse grain (wider bit extraction, more aggressive).

---

#### Knob 5 — Warmth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |
| Suffix | % |

Warmth controls the intensity of warm brown toning applied to shadow regions. The toning shifts U (blue-yellow axis) downward and V (red-cyan axis) upward, creating a sepia-brown color cast in areas where the lith Y value falls below 400. At zero, the shadows are neutral black. At maximum, deep shadows carry a rich brown tint characteristic of lith chemistry. The shift is proportional — Warmth divided by 16 sets the U displacement, and Warmth divided by 32 adds an extra V push for a redder brown.

---

#### Knob 6 — Paper
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 88% |
| Suffix | % |

Paper sets the maximum brightness that the paper white can reach — the ceiling of the transfer curve. In the darkroom, this corresponds to the point at which you pull the print from the developer: pull early and the highlights are soft, creamy, and subdued; let development run longer and the paper brightens to full white. At low Paper values, the entire processed image is compressed into a dark, moody range. At maximum, highlights reach full brightness (1023). This control interacts with every other parameter because the entire transfer curve scales proportionally with Paper.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Developer** | Dilute | Strong |
| **8 — Grain** | Fine | Coarse |
| **9 — Split** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options that modify different stages of the pipeline. Developer (Switch 7) and Grain (Switch 8) affect the mid-tone processing character. Split (Switch 9) adds post-processing highlight toning. Invert (Switch 10) applies a full-scale luminance complement at the output stage. Bypass (Switch 11) routes the original signal directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry crossfade between the original input and the processed lith output. At 0%, the output is entirely the original (dry) signal. At 100%, the output is entirely the processed (wet) signal. Intermediate values blend the two, which can create a subtle lith-tinted overlay on the original — a gentler version of the effect that preserves some of the source's tonal range while adding warmth and grain.

---

## Guided Exercises

These exercises progress from basic threshold printing to full lith darkroom emulation with toning, grain, and split-tone processing.

### Exercise 1: Basic Lith Threshold

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: lith_source1_kodim03, after: lith_exercise1_result },
    { label: "Kodim13", before: lith_source2_kodim13, after: lith_exercise1_result },
    { label: "Kodim13 B&W", before: lith_source3_kodim13_bw, after: lith_exercise1_result },
  ]}
/>
*Basic Lith Threshold — simulated result across source images.*
**Source**: A portrait or figure with a full tonal range — both deep shadows and bright highlights.

**Objective**: Learn the fundamental lith threshold behavior: Exposure, Spread, and their interaction with Paper white.

1. **Set Paper to maximum**: Turn Paper fully clockwise to set the brightest possible highlight.
2. **Center the threshold**: Set Exposure to about 50%. The image should show a clear division between black and white regions.
3. **Widen the spread**: Increase Spread from minimum. Watch the abrupt black/white boundary soften into a transition zone with intermediate tones.
4. **Shift the exposure**: Sweep Exposure slowly from low to high. Watch the boundary slide across the image — more of the frame goes dark as exposure increases.
5. **Lower Paper**: Pull Paper back to about 50%. The highlights dim to a soft grey rather than blinding white.

**Key concepts**: Exposure sets threshold center, Spread controls transition width, Paper sets highlight ceiling, these three controls define the fundamental lith print geometry

---

### Exercise 2: Infectious Development and Toning

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: lith_source1_kodim03, after: lith_exercise2_result },
    { label: "Kodim13", before: lith_source2_kodim13, after: lith_exercise2_result },
    { label: "Kodim13 B&W", before: lith_source3_kodim13_bw, after: lith_exercise2_result },
  ]}
/>
*Infectious Development and Toning — simulated result across source images.*
**Source**: Footage with gradual tonal transitions — overcast skies, fog, or soft lighting.

**Objective**: Explore the infectious development curve and warm brown toning.

1. **Set a moderate threshold**: Exposure ~50%, Spread ~40%, Paper ~90%.
2. **Sweep Infection**: Slowly increase Infection from zero. Watch the mid-tone transition steepen — smooth gradients collapse into sharper divisions.
3. **Toggle Developer**: Switch from Dilute to Strong. Notice how the same Infection setting produces a much harder step.
4. **Add warmth**: Increase Warmth from zero. The dark regions take on a brown-sepia cast while the paper whites remain neutral.
5. **Enable split tone**: Toggle Split On. The highlights shift to a cool blue-grey, creating warm/cool contrast.
6. **Add grain**: Increase Grain to about 30%. Texture appears in the transition zone — the narrow band between black and paper white.

**Key concepts**: Infection shapes the transfer curve steepness, Developer selects the curve family, Warmth tones shadows independently, Split adds cool counterpoint to warm shadows, grain concentrates in mid-tones

---

### Exercise 3: Full Lith Darkroom

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: lith_source1_kodim03, after: lith_exercise3_result },
    { label: "Kodim13", before: lith_source2_kodim13, after: lith_exercise3_result },
    { label: "Kodim13 B&W", before: lith_source3_kodim13_bw, after: lith_exercise3_result },
  ]}
/>
*Full Lith Darkroom — simulated result across source images.*
**Source**: High-contrast material — backlit silhouettes, stage lighting, or architectural shadows.

**Objective**: Combine all controls for a complete lith darkroom print with grain, toning, and split-tone.

1. **Establish the print**: Exposure ~60%, Spread ~30%, Infection ~80%, Paper ~85%.
2. **Strong developer**: Toggle Developer to Strong for maximum infectious contrast.
3. **Full warmth**: Set Warmth to ~80%. Deep shadows glow brown.
4. **Split tone**: Enable Split for cool highlight accents.
5. **Coarse grain**: Set Grain to ~40%, toggle Grain to Coarse. Heavy texture fills the transition zone.
6. **Invert**: Toggle Invert to see the print as a negative — warm highlights, cool shadows.
7. **Mix**: Pull Mix back to ~70% to blend lith processing with the original, creating a tinted overlay.

**Key concepts**: All lith parameters interact — Exposure and Spread define the threshold geometry, Infection and Developer shape the curve within it, Warmth and Split color the result, grain concentrates in the transition zone, and Mix blends with the dry signal

---


## Tips

- **Start with Paper at maximum**: The Paper control scales the entire transfer curve. Set it high first, then adjust Exposure and Spread to place the threshold where you want it.
- **Dilute developer for subtlety**: Dilute mode gives you four gradual steepness levels via the Infection knob. Strong mode is dramatic but leaves little room for nuance.
- **Grain follows the transition zone**: The grain noise only appears in the mid-tone band between the low and high threshold edges. Widening the Spread widens the grain band.
- **Warmth is fixed at Y=400**: The warm brown toning always activates below lith Y=400 regardless of the Exposure setting. This means the color boundary is independent of the contrast boundary.
- **Split tone adds depth**: Enabling Split creates a warm-shadow / cool-highlight contrast that prevents the image from looking monotone even at extreme settings.
- **Mix for tinted overlay**: Pulling Mix back from 100% blends the lith processing with the original, creating a color-tinted version of the source rather than a full replacement.
- **Invert for negatives**: Toggling Invert produces a lith negative — dark paper with bright grain and inverted toning. The visual character is very different from simply inverting the source before processing.
- **Feedback loops**: Route the output back to the input for recursive lith processing. Each pass narrows the transition zone further, eventually collapsing the image to pure black and white.

---

## Glossary

| Term | Definition |
|------|------------|
| **Autocatalytic** | A chemical reaction whose products accelerate the same reaction, creating positive feedback. |
| **BT.601** | The ITU-R standard defining the YUV color space used by standard-definition video and throughout the Videomancer pipeline. |
| **Dilute Developer** | Lith chemistry diluted to slow the development process and widen the transition between developed and undeveloped regions. |
| **Infectious Development** | The autocatalytic behavior of lith developer where heavily exposed areas accelerate the development of neighboring areas. |
| **LFSR** | Linear Feedback Shift Register; a deterministic pseudo-random number generator used for grain noise. |
| **Lith Printing** | A photographic darkroom process using dilute lith developer and overexposure to produce extreme contrast with warm-toned shadows. |
| **Mid-tone Flag** | A per-pixel boolean indicating that the input luminance falls within the transition zone between the low and high threshold edges. |
| **Paper White** | The maximum brightness of the unexposed paper surface in a photographic print; in Lith, the ceiling of the transfer curve. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Split Tone** | A toning technique where shadows and highlights receive different color casts — typically warm shadows and cool highlights. |
| **Transfer Curve** | The mathematical function mapping input luminance to output luminance, here shaped by infectious development dynamics. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
