---
draft: true
sidebar_position: 237
slug: /instruments/videomancer/riso
title: "Riso"
image: /img/instruments/videomancer/riso/riso_hero.png
description: "Risograph printing is a stencil-based duplicating process beloved by artists and zine-makers for its vivid spot inks, imperfect registration, and textured grain."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import riso_hero from '/img/instruments/videomancer/riso/riso_hero.png';
import riso_control_panel from '/img/instruments/videomancer/riso/riso_control_panel.png';
import riso_exercise1_result from '/img/instruments/videomancer/riso/riso_exercise1_result.png';
import riso_exercise2_result from '/img/instruments/videomancer/riso/riso_exercise2_result.png';
import riso_exercise3_result from '/img/instruments/videomancer/riso/riso_exercise3_result.png';
import riso_source1_kodim02 from '/img/instruments/videomancer/riso/riso_source1_kodim02.png';
import riso_source2_kodim07 from '/img/instruments/videomancer/riso/riso_source2_kodim07.png';
import riso_source3_kodim01_bw from '/img/instruments/videomancer/riso/riso_source3_kodim01_bw.png';

# Riso

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: riso_source1_kodim02, after: riso_hero },
    { label: "Kodim07", before: riso_source2_kodim07, after: riso_hero },
    { label: "Kodim01 B&W", before: riso_source3_kodim01_bw, after: riso_hero },
  ]}
/>
*Riso applying dual-ink subtractive spot color separation with stencil grain texture and horizontal misregistration offset.*

---

## Overview

Risograph printing is a stencil-based duplicating process beloved by artists and zine-makers for its vivid spot inks, imperfect registration, and textured grain. Each pass through a risograph machine lays down a single ink color through a wax-paper master — shadows in one color, highlights in another, midtones in a third. The layers stack subtractively on uncoated paper, and because each pass feeds the sheet through the machine independently, inter-pass alignment is never perfect. The result is a characteristic look: bold, slightly misregistered color separations with a rough, organic grain.

Riso recreates this process electronically. It separates the input luminance into two or three tonal layers (shadows, highlights, and optionally midtones), assigns each layer an independent ink color from a palette of four risograph-inspired spot inks, then composites the layers subtractively against a warm paper base. Per-layer horizontal misregistration shifts layers B and C by a configurable number of pixels — up to seven — to simulate the alignment error of a real risograph drum. An LFSR-driven stencil grain adds the irregular ink porosity that gives riso prints their tactile character. The name is a direct abbreviation of *risograph*, the Japanese drum-based duplicator that became a creative tool for independent publishers and poster artists worldwide.

At subtle settings, Riso adds a gentle duotone warmth with barely perceptible grain. At extreme settings, it produces the oversaturated, wildly misregistered, gritty look of a fourth-generation zine printed on cheap newsprint — a digital artifact that feels decidedly analog.

---

## Background

### What Is Risograph Printing?

The risograph is a high-speed digital duplicator manufactured by Riso Kagaku Corporation. Unlike inkjet or laser printers, it burns a stencil master for each ink color, wraps the master around a rotating drum filled with soy-based ink, and presses copies through a simple mechanical feeder. Each color requires a separate pass — the paper physically re-enters the machine for each additional ink layer. This single-color-per-pass workflow means alignment between layers is always slightly imperfect, and ink coverage is always slightly inconsistent. These "flaws" became the aesthetic signature of risograph art.

### Subtractive Color Mixing

In subtractive color mixing, each additional ink layer absorbs more light from the paper. White paper reflects all wavelengths; each ink selectively absorbs certain wavelengths and reflects others. When two semi-transparent inks overlap, the result is darker than either alone, because both layers are subtracting from the reflected light. Riso implements this by computing per-layer absorption (the difference between paper brightness and ink brightness, scaled by the density mask) and subtracting the combined absorption from the paper base color. This is the same principle used in CMYK offset printing, silk screening, and watercolor painting.

### Tonal Separation and Masking

A risograph print begins with separating the source image into tonal zones. Riso uses a luminance threshold to split the input into shadows (below threshold) and highlights (above threshold), with an optional midtone band when three-color mode is enabled. Each zone gets its own density mask — darker shadow areas produce stronger ink coverage for ink A, brighter highlight areas produce stronger ink coverage for ink B. The masks modulate how much of each ink is applied pixel-by-pixel, simulating the way a real riso stencil burns thicker or thinner depending on the source image density.

### Stencil Grain and Registration Error

Two imperfections define the risograph aesthetic. First, *stencil grain*: the wax master has a porous texture, and ink doesn't pass through uniformly. Riso simulates this with LFSR pseudo-random noise added to the density mask before compositing — each pixel's ink coverage is slightly randomized, producing the granular texture of a real print. Second, *registration error*: because each color pass feeds the paper independently, the layers never align perfectly. Riso models this with a per-layer horizontal pixel shift — layer B and layer C read from a shift-register-delayed version of the input, offsetting the pixel position by up to 7 pixels horizontally.

### Spot Color Palettes

Risograph machines are known for their vivid, unconventional ink palette. Riso provides four ink presets per layer: Fluorescent Pink (the iconic riso color — a bright magenta-pink), Teal, Blue, and Black. The two layers use independent color selectors, so any combination of two spot colors can be used. Popular risograph duotone pairings like Fluorescent Pink + Teal or Blue + Black are directly available.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register + Shift Register Write
│   │      (current pixel written to 8-deep shift register)
│   │
│   ├─ 2. Layer Read + Threshold Separation
│   │      Layer A: current pixel (no offset)
│   │      Layer B: shift register at B H-Offset index (0-7)
│   │      Layer C: shift register at C H-Offset index (3-color only)
│   │      Shadow mask: Y < threshold → (1023 - Y)
│   │      Highlight mask: Y ≥ threshold → Y
│   │      Midtone mask: threshold ≤ Y < midpoint (3-color only)
│   │
│   ├─ 3. Ink Color + Stencil Grain
│   │      LFSR ±32 noise × grain_amount added to each mask
│   │      Per-layer ink absorption = (paper - ink) × mask / 1024
│   │
│   ├─ 4. Subtractive Compositing + Paper Base
│   │      Output = paper_color − Σ(absorption_per_layer)
│   │      Chroma: directional absorption toward each ink hue
│   │
│   └─ 5-8. Interpolator (wet/dry mix, 4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (delayed to match processing latency)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal via Mix fader
```

The key architectural insight is that Riso is a *luminance-only* separation engine operating in the Y domain. The input chroma (U, V) is not used for layer separation — only the brightness determines which tonal zone each pixel falls into. Color is reintroduced entirely from the ink palette during the compositing stage, where each layer's ink YUV values are subtracted from the warm paper base. The horizontal misregistration operates on the luminance shift register, so layers B and C see the same tonal content as layer A but shifted rightward by a configurable number of pixels. This means misregistration is visible as a colored fringe at tonal transitions, exactly as in a real risograph print where inter-pass alignment error shows up most at edges.

---

## Parameter Reference

<img src={riso_control_panel} alt="Videomancer front panel with Riso loaded"/>
*Videomancer's front panel with Riso active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the luminance threshold that divides the input into shadow and highlight zones. At low values, almost the entire image falls into the highlight zone and receives ink B. At high values, almost everything falls into the shadow zone and receives ink A. At the midpoint (~50%), the tonal split is roughly even, and both inks contribute equally. In three-color mode, the threshold also defines the lower boundary of the midtone band. Finding the right threshold for a given source image is the essential first step — it determines the "plate separation" that defines the entire risograph character.

---

#### Knob 2 — Grain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of the LFSR stencil grain texture applied to both layer masks before compositing. At 0%, the masks are smooth and the ink coverage is perfectly uniform — a clinical separation without any of the organic risograph texture. As you increase grain, the LFSR noise increasingly randomizes ink coverage pixel-by-pixel, producing the characteristic porous, stippled texture of ink pressed through a wax stencil. High grain values create heavy texturization where the ink appears to have been applied with a sponge.

---

#### Knob 3 — B H-Offset
| Property | Value |
|----------|-------|
| Range | -16px – 16px |
| Default | 1px |
| Suffix | px |

Sets the horizontal pixel offset for layer B. The top 3 bits of the register select an index from 0 to 7 into the Y pixel shift register, shifting layer B's read position rightward by that many pixels. At 0 offset, layers A and B are perfectly registered. As the offset increases, layer B's ink color separates horizontally from layer A, producing the misregistration fringe effect at tonal edges. This is the primary control for the risograph alignment-error aesthetic.

---

#### Knob 4 — B V-Offset
| Property | Value |
|----------|-------|
| Range | -8ln – 8ln |
| Default | 1ln |
| Suffix | ln |

Reserved for layer B vertical offset (not implemented in the current VHDL due to iCE40 BRAM constraints). The parameter is present for forward compatibility. Adjusting this control has no visible effect. In a future revision with additional BRAM resources, this would shift layer B vertically by a number of scanlines, adding vertical misregistration to the horizontal shift.

---

#### Knob 5 — C H-Offset
| Property | Value |
|----------|-------|
| Range | -16px – 16px |
| Default | -1px |
| Suffix | px |

Sets the horizontal pixel offset for layer C — the midtone layer, active only when the Layers switch is set to 3-Color. Works identically to B H-Offset: top 3 bits select an index (0–7) into the shift register. When used together with B H-Offset, the two offset controls produce a three-way color fringe — each tonal zone (shadow, midtone, highlight) can be horizontally displaced from the others.

---

#### Knob 6 — C V-Offset
| Property | Value |
|----------|-------|
| Range | -8ln – 8ln |
| Default | 0ln |
| Suffix | ln |

Reserved for layer C vertical offset (not implemented). Like B V-Offset, this is a placeholder for future vertical misregistration capability. Currently has no effect.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color A Hi** | Off | On |
| **8 — Color A Lo** | Off | On |
| **9 — Color B Hi** | Off | On |
| **10 — Color B Lo** | Off | On |
| **11 — Layers** | 2-Color | 3-Color |

The five toggles form two independent 2-bit color selectors (one for ink A and one for ink B) plus a layer count mode switch. Toggles 7–8 select ink A's color from the four-entry palette. Toggles 9–10 select ink B's color. Toggle 11 switches between 2-color mode (shadow + highlight) and 3-color mode (shadow + midtone + highlight). In 2-color mode, layer C is disabled and only inks A and B are composited. In 3-color mode, ink B is used for both the highlight layer and the midtone layer.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix crossfade between the original input video (dry) and the risograph-processed output (wet). At 0%, the output is the unprocessed input. At 100%, the output is the fully processed riso print simulation. Intermediate values blend between the two, which can be used for a subtle duotone wash effect where the spot colors tint the original image without fully replacing it.

---

## Guided Exercises

These exercises progress from simple duotone separation to full multi-layer misregistered prints, building familiarity with the risograph simulation parameters.

### Exercise 1: Classic Duotone

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: riso_source1_kodim02, after: riso_exercise1_result },
    { label: "Kodim07", before: riso_source2_kodim07, after: riso_exercise1_result },
    { label: "Kodim01 B&W", before: riso_source3_kodim01_bw, after: riso_exercise1_result },
  ]}
/>
*Classic Duotone — simulated result across source images.*
**Source**: A portrait or still life with clear tonal range — visible shadows, midtones, and highlights.

**Objective**: Learn how threshold separation and ink color selection interact to create a classic risograph duotone.

1. **Set ink colors**: Set Color A to Fluorescent Pink (Tog 7 Off, Tog 8 Off). Set Color B to Teal (Tog 9 Off, Tog 10 On).
2. **Find the threshold**: Slowly sweep Threshold from left to right. Watch the image split into pink shadows and teal highlights. Find the point where the subject reads clearly.
3. **Add grain**: Increase Grain to ~25%. Watch the smooth ink coverage break up into a stencil-like texture.
4. **Compare**: Set Mix to 50% to see the duotone overlay blended with the original. Return to 100% for the full riso look.

**Key concepts**: Threshold controls the tonal split between two ink colors, grain adds stencil porosity texture, subtractive ink overlap darkens where layers meet

---

### Exercise 2: Misregistered Print

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: riso_source1_kodim02, after: riso_exercise2_result },
    { label: "Kodim07", before: riso_source2_kodim07, after: riso_exercise2_result },
    { label: "Kodim01 B&W", before: riso_source3_kodim01_bw, after: riso_exercise2_result },
  ]}
/>
*Misregistered Print — simulated result across source images.*
**Source**: High-contrast footage with strong edges — text overlays, architectural details, or graphic patterns.

**Objective**: Explore horizontal misregistration and its effect on edge fringing.

1. **Start with a clean duotone**: Use the settings from Exercise 1 (Pink + Teal, Threshold ~50%).
2. **Add B offset**: Slowly increase B H-Offset. Watch the teal highlight layer slide rightward, creating a colored fringe at every tonal edge.
3. **Switch to 3-Color**: Toggle Layers to 3-Color. A midtone band appears.
4. **Add C offset**: Increase C H-Offset in the opposite direction from B. The three layers now separate horizontally, producing a triple color fringe.
5. **Heavy grain**: Increase Grain to ~60% for a rough, distressed print texture that combines with the misregistration.

**Key concepts**: Horizontal misregistration shifts layers independently, misregistration is most visible at tonal edges, 3-color mode adds a midtone layer

---

### Exercise 3: Overinked Poster

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: riso_source1_kodim02, after: riso_exercise3_result },
    { label: "Kodim07", before: riso_source2_kodim07, after: riso_exercise3_result },
    { label: "Kodim01 B&W", before: riso_source3_kodim01_bw, after: riso_exercise3_result },
  ]}
/>
*Overinked Poster — simulated result across source images.*
**Source**: Any footage — works especially well with bold graphic content or live camera feeds.

**Objective**: Push the risograph simulation to its extremes for a heavily textured, overinked poster aesthetic.

1. **Choose dark inks**: Set Color A to Blue (Tog 7 On, Tog 8 Off). Set Color B to Black (Tog 9 On, Tog 10 On).
2. **Low threshold**: Set Threshold to ~25% so most of the image receives ink A (Blue), creating a heavily inked dark print.
3. **Maximum grain**: Set Grain to ~80%. The stencil texture becomes very aggressive.
4. **Strong misregistration**: Set B H-Offset to maximum (~7 px). The black highlight layer slides far from the blue shadow layer.
5. **3-Color mode**: Enable for an additional midtone band. Adjust C H-Offset for a triple offset.
6. **Partial mix**: Try Mix at ~70% to let some of the original image show through the heavy ink layers.

**Key concepts**: Low threshold creates heavy shadow ink coverage, high grain produces extreme stencil texture, strong misregistration creates wide color fringe bands

---


## Tips

- **Threshold is the master control**: Finding the right shadow/highlight split for your source material is the single most important adjustment. Start there before touching anything else.
- **Grain needs contrast**: Stencil grain is most visible in areas of moderate ink density. Fully saturated shadows and fully exposed highlights mask the grain texture because they're at the extremes.
- **Classic duotone combinations**: Fluorescent Pink + Teal is the quintessential risograph pairing. Blue + Black produces a stark, cold print. Pink + Black is bold and graphic.
- **Misregistration tells a story**: Even a 1–2 pixel offset produces a subtle but visible color fringe that immediately reads as "printed." Larger offsets create an increasingly exaggerated, poster-like misalignment.
- **3-Color fills the middle**: If your duotone looks too contrasty — too much hard switching between shadow and highlight — enable 3-Color mode. The midtone band adds tonal richness.
- **Mix for subtlety**: At 50–70% Mix, the risograph colors tint the original image rather than replacing it. This produces a warm, printed-overlay look that's more subtle than the full simulation.
- **Feedback loops**: Routing the output back through the input accumulates ink layers, simulating over-printing on a real risograph where the same sheet runs through the machine multiple times.

---

## Glossary

| Term | Definition |
|------|------------|
| **Absorption** | In subtractive color mixing, the amount of light energy removed by an ink layer; computed as (paper brightness − ink brightness) × coverage. |
| **Duotone** | A printing technique using two ink colors to reproduce a tonal image, typically one dark and one mid-tone or accent color. |
| **LFSR** | Linear Feedback Shift Register; a hardware pseudo-random number generator used to create the stencil grain noise pattern. |
| **Misregistration** | Spatial misalignment between separately printed ink layers, visible as colored fringe at tonal edges. |
| **Risograph** | A high-speed stencil-based digital duplicator manufactured by Riso Kagaku Corporation, widely adopted for art printing. |
| **Spot Color** | A single pre-mixed ink color (as opposed to CMYK process color), applied as a uniform hue across the entire print. |
| **Stencil** | A perforated master sheet through which ink is pressed; in risograph printing, a wax thermal master with variable porosity. |
| **Subtractive Mixing** | Color mixing where layered pigments or inks absorb light, producing darker results as more layers are added. |
| **Tonal Separation** | Dividing a continuous-tone image into discrete brightness zones, each assigned a specific treatment or ink color. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
