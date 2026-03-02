---
draft: true
sidebar_position: 124
slug: /instruments/videomancer/gravure
title: "Gravure"
image: /img/instruments/videomancer/gravure/gravure_hero.png
description: "Before photographic reproduction, the finest printed images were made by photogravure — an intaglio process where an image is etched into a copper plate, ink is pressed into the recesses, and the plate is run through a press to transfer the image onto dampened paper."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import gravure_hero from '/img/instruments/videomancer/gravure/gravure_hero.png';
import gravure_control_panel from '/img/instruments/videomancer/gravure/gravure_control_panel.png';
import gravure_exercise1_result from '/img/instruments/videomancer/gravure/gravure_exercise1_result.png';
import gravure_exercise2_result from '/img/instruments/videomancer/gravure/gravure_exercise2_result.png';
import gravure_exercise3_result from '/img/instruments/videomancer/gravure/gravure_exercise3_result.png';
import gravure_source1_kodim02 from '/img/instruments/videomancer/gravure/gravure_source1_kodim02.png';
import gravure_source2_kodim07 from '/img/instruments/videomancer/gravure/gravure_source2_kodim07.png';
import gravure_source3_kodim01_bw from '/img/instruments/videomancer/gravure/gravure_source3_kodim01_bw.png';

# Gravure

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: gravure_source1_kodim02, after: gravure_hero },
    { label: "Kodim07", before: gravure_source2_kodim07, after: gravure_hero },
    { label: "Kodim01 B&W", before: gravure_source3_kodim01_bw, after: gravure_hero },
  ]}
/>
*Gravure transforming a photographic source into a warm-toned intaglio print with aquatint grain visible in the midtones and a crisp plate mark border.*

---

## Overview

Before photographic reproduction, the finest printed images were made by **photogravure** — an intaglio process where an image is etched into a copper plate, ink is pressed into the recesses, and the plate is run through a press to transfer the image onto dampened paper. The result has a character that no other printing method can match: rich, luminous shadows with visible depth, a stochastic grain texture from the aquatint ground, and warm ink tones that vary from deep sepia to cool blue-black depending on the chemistry.

Gravure recreates this process as a real-time video effect. The program chains together a concave shadow tone curve (modeling the copper etch depth), density-dependent aquatint grain from an LFSR noise source, ink colorization with four historical presets, ink pooling in the deepest shadows, paper warmth tinting, and optional paper surface texture. The name is short for *photogravure* — the French term for the process, literally "photo-engraving." Every stage works simultaneously on every pixel of every frame, transforming any video signal into a convincing facsimile of a hand-pulled intaglio print.

At conservative settings — moderate grain, warm sepia ink, plate mark enabled — Gravure produces images that closely resemble actual photogravure prints, with their characteristic tonal warmth and fine stochastic texture. At extreme settings — maximum grain, iron gall ink, heavy pooling — the effect becomes more expressive and stylized, with pronounced noise patterns and dramatic ink effects that push beyond photographic realism into the territory of printmaking as a creative medium.

---

## Background

### What Is Photogravure?

**Photogravure** (also called *héliogravure*) is a photomechanical printing process invented by Karel Klíč in 1878. A copper plate is coated with a light-sensitive gelatin resist, exposed through a photographic positive, and etched in ferric chloride acid baths of varying strengths. The acid penetrates deeper where the gelatin is thinnest (corresponding to the darkest areas of the image), creating microscopic wells of varying depth. When inked and wiped, the deeper wells hold more ink, producing richer, denser tones. The tonal range of a photogravure print exceeds that of any half-tone process because it encodes continuous tone as ink *depth* rather than dot *size*. Gravure's concave tone curve emulates this etch-depth response — shadows are extended and enriched while highlights are gently compressed.

### What Is Aquatint Grain?

The defining visual texture of photogravure is **aquatint grain** — a fine, irregular pattern visible throughout the midtones of the print. In the physical process, this comes from the aquatint ground: a layer of rosin or asphaltum dust fused to the copper plate before etching. The individual grains resist the acid, creating a network of tiny cells separated by unetched copper walls. This produces a stochastic (random) texture distinctly different from the regular dots of halftone printing. Gravure simulates this with an LFSR noise source whose amplitude is modulated by how close each pixel's luminance is to midgray — maximum grain at mid-tones, suppressed at the highlights and deep shadows, exactly matching the physics of the real process where very light and very dark areas have less visible grain structure.

### What Is Ink Colorization?

Real gravure prints are not simply black-and-white. The ink chemistry determines the color of the printed image. **Warm sepia** tones come from sulfide-toned prints (like Alfred Stieglitz's *Camera Work* portfolios). **Neutral brown** is characteristic of Edward Curtis's *The North American Indian* plates. **Cool black** appears in newspaper rotogravure sections. **Iron gall** ink produces a distinctive blue-black that deepens with age. Gravure provides these four presets as a 2-bit selector, each mapping to specific YUV delta values: the density signal is multiplied by per-preset U and V offsets to produce the characteristic hue of each ink type.

### What Is Ink Pooling?

In intaglio printing, areas of the plate with the deepest etch hold the most ink. When these areas are very deep — the darkest shadows of the image — the excess ink can produce a subtle surface sheen or gloss that catches light differently from the matte surface of lighter areas. This **ink pooling** effect gives photogravure prints their characteristic sense of physical depth. Gravure simulates this as a luminance boost in the deepest shadow regions (below Y=128), controlled by the Ink Pooling knob. It creates a gentle lift in the darkest tones that prevents the shadows from going to pure black, mimicking the reflective quality of thick ink deposits.

### What Is Paper Warmth?

The color of the paper stock affects the overall appearance of a print. Photogravure was traditionally printed on warm-toned laid or wove papers — slightly yellowish whites that produced a harmonious foundation for warm ink tones. Gravure simulates this by shifting the U/V chrominance toward warm (lower U, higher V) or cool based on the Paper Warmth control. The shift is applied as a quadratic function of the control value, producing a gentle, naturalistic warmth at moderate settings and a more pronounced tint at extremes.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register           (latch input Y)
│   ├─ 2. Gravure Tone Curve       (concave shadow extension, highlight compression)
│   ├─ 3. Aquatint Grain           (LFSR noise, density-dependent amplitude)
│   ├─ 4. Ink Colorization         (density → YUV via ink preset mapping)
│   ├─ 5. Ink Density Scaling      (overall ink coverage scaling)
│   ├─ 6. Ink Pooling              (shadow luminance boost < Y=128)
│   ├─ 7. Paper Warmth             (U/V chrominance shift)
│   └─ 8. Mix                      (3× interpolator_u, wet/dry crossfade)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Ink Color Preset         (2-bit selector → delta U/V constants)
│   ├─ 2. Density × Delta          (ink density modulates chroma)
│   └─ 3. Paper Warmth Shift       (quadratic U/V offset)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay alignment (pass-through)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The processing chain converts the input luminance into an ink density value and then maps that density through the ink color preset to produce colored output. This inversion is critical: a bright pixel in the input (high Y) becomes a low density value (light ink / paper showing through), while a dark pixel becomes high density (heavy ink). The LFSR aquatint grain is injected *before* the density inversion and ink mapping, so it perturbs the natural brightness of the input signal. After inversion, the grain appears in the printed density domain — visible in the midtones where the physical aquatint process also produces the most visible texture. The U and V channels are not processed from the input — they are synthesized entirely from the ink color preset deltas multiplied by the computed density, producing monochromatic ink-colored output regardless of the input's original color content.

---

## Parameter Reference

<img src={gravure_control_panel} alt="Videomancer front panel with Gravure loaded"/>
*Videomancer's front panel with Gravure active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Shadow Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the depth of the concave tone curve applied to the input luminance. At zero, the tone curve is a straight passthrough — no shadow extension. As the control increases, the shadow region (below midpoint 512) is progressively darkened by subtracting a scaled offset proportional to the distance from midgray. Highlights above midpoint receive a gentler compression. The net effect models the etch-depth response of a copper plate: shadows gain richness and density while the overall tonal range compresses in a way characteristic of intaglio printing.

---

#### Knob 2 — Grain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the amplitude of the aquatint grain texture. The grain is generated by a 16-bit LFSR (seed 0x7E5D) running at pixel rate, producing a new pseudo-random value for every pixel. The noise amplitude is modulated by how close each pixel's tone-curved luminance is to midgray (512) — maximum grain at mid-tones, zero grain at the extremes. At zero, no grain is applied and the image is perfectly smooth. At maximum, the grain becomes a coarse, visible stipple that dominates the midtone regions.

---

#### Knob 3 — Plate Margin
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 19.6% |
| Suffix | % |

Controls the width of the plate mark border. In traditional photogravure, the copper plate leaves a physical impression — a **plate mark** — in the paper surrounding the image, visible as a rectangular embossed border. This control sets how wide that decorative border appears on screen. The VHDL reserves this control for the plate mark feature, which is enabled or disabled by toggle switch 9.

---

#### Knob 4 — Ink Pooling
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of the ink pooling effect in the deepest shadows. Ink pooling adds a luminance boost to pixels below Y=128 in the colorized output, simulating the reflective sheen of thick ink deposits. At zero, deep shadows go fully dark. As the control increases, the darkest areas receive a gentle lift that prevents them from reaching pure black — the highlight is proportional to the difference between the pixel value and the 128 threshold, scaled by this control.

---

#### Knob 5 — Paper Warmth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the paper warmth tinting. The value is squared and then used to shift the U channel downward and the V channel upward, producing a warm yellowish-brown paper tone. At zero, no warmth is applied and the paper appears neutral white. At moderate settings, the paper acquires the golden warmth characteristic of traditional wove and laid papers used in fine-art photogravure printing. At maximum, the warmth becomes a strong amber tint.

---

#### Knob 6 — Ink Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the overall ink density — how much ink coverage the print appears to have. This is a final scaling stage applied to the colorized luminance output. At zero, the "ink" is fully transparent and only the paper base tone remains (producing a nearly white image). At maximum, the full tonal range of the colorized density is expressed. The multiplication blends between the paper base luminance (C_PAPER_Y = 940) and the ink-darkened luminance.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Ink Color A** | Off | On |
| **8 — Ink Color B** | Off | On |
| **9 — Plate Mark** | Off | On |
| **10 — Paper Type** | Smooth | Textured |
| **11 — Bypass** | Off | On |

Switches 7 and 8 form a **combined 2-bit ink color selector** — the combination of Ink Color A and Ink Color B selects one of four historical ink presets. Switch 9 enables the plate mark border (independent binary option). Switch 10 selects between smooth and textured paper (independent binary option). Switch 11 is the standard bypass. Unlike some programs where each toggle controls a separate processing stage, here the first two toggles work together to choose a single ink formula.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the gravure-processed output and the delayed original input. Three interpolator instances crossfade Y, U, and V independently. At zero, only the original input passes through. At maximum, only the gravure effect is visible. Intermediate positions create a ghostly overlay where the original video shows through the print texture — useful for partially grounding the print effect in photographic reality.

---

## Guided Exercises

These exercises build from basic tone curve exploration to full print simulation, progressively engaging more of the processing chain.

### Exercise 1: Shadow Tone Curve

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: gravure_source1_kodim02, after: gravure_exercise1_result },
    { label: "Kodim07", before: gravure_source2_kodim07, after: gravure_exercise1_result },
    { label: "Kodim01 B&W", before: gravure_source3_kodim01_bw, after: gravure_exercise1_result },
  ]}
/>
*Shadow Tone Curve — simulated result across source images.*
**Source**: A portrait or still life with a full tonal range — deep shadows, smooth midtones, and clean highlights.

**Objective**: Understand how the concave tone curve reshapes shadow density to emulate the copper etch-depth response.

1. **Neutral baseline**: Set all toggles off, Grain to 0%, and Mix to 100%. Set Ink Density to ~75%. You should see a monochromatic version of the input in warm sepia (the default ink preset).
2. **Sweep shadow depth**: Slowly increase Shadow Depth from 0% to 100%. Watch the shadow regions darken and gain richness while highlights compress gently. This is the gravure etch-depth response.
3. **Observe midtones**: At moderate Shadow Depth (~50%), notice how midtones shift slightly darker — the concave curve pulls everything below center downward.
4. **Paper as white point**: The lightest areas approach the paper base color (Y=940, a warm off-white) rather than pure white. This is characteristic of real prints on uncoated paper.
5. **Compare ink presets**: Switch through all four combinations of Ink Color A and B. Each produces a distinctly different tonal character while the shadow curve remains the same.

**Key concepts**: Concave tone curve extends shadows while compressing highlights, the paper base defines the white point, ink presets change color without changing the tonal mapping

---

### Exercise 2: Aquatint Grain and Ink Pooling

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: gravure_source1_kodim02, after: gravure_exercise2_result },
    { label: "Kodim07", before: gravure_source2_kodim07, after: gravure_exercise2_result },
    { label: "Kodim01 B&W", before: gravure_source3_kodim01_bw, after: gravure_exercise2_result },
  ]}
/>
*Aquatint Grain and Ink Pooling — simulated result across source images.*
**Source**: A landscape or architectural image with broad midtone areas (sky, walls, foliage) and some deep shadows.

**Objective**: Explore the density-dependent aquatint grain texture and the ink pooling effect in deep shadow regions.

1. **Add grain**: Starting from Exercise 1's settings, increase Grain to ~40%. A fine stochastic texture appears in the midtone areas. Notice that highlights and deep shadows remain relatively smooth — the grain is concentrated where the physical aquatint process also produces the most visible texture.
2. **Increase grain**: Push Grain to ~80%. The stipple becomes coarser and more visible, dominating the midtones.
3. **Observe shadow clarity**: Even at high grain, the deepest shadows remain relatively free of noise. This matches real photogravure, where the deepest etch holds so much ink that individual grain cells blur together.
4. **Enable ink pooling**: Set Ink Pooling to ~50%. Watch the deepest shadow areas receive a subtle luminance lift — a gentle brightening that prevents pure black. This simulates the surface sheen of thick ink.
5. **Maximum pooling**: Push to ~100%. The pooling becomes more pronounced, creating a slightly veiled quality in the darkest tones.
6. **Try textured paper**: Switch Paper Type to Textured. A secondary texture layer appears that is visible even in highlights, simulating the physical fiber structure of printmaking paper.

**Key concepts**: Aquatint grain is density-dependent (strongest at midtones), LFSR noise is stochastic (not ordered), ink pooling lifts deep shadows to simulate surface sheen, paper texture is independent of aquatint grain

---

### Exercise 3: Full Photogravure Emulation

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: gravure_source1_kodim02, after: gravure_exercise3_result },
    { label: "Kodim07", before: gravure_source2_kodim07, after: gravure_exercise3_result },
    { label: "Kodim01 B&W", before: gravure_source3_kodim01_bw, after: gravure_exercise3_result },
  ]}
/>
*Full Photogravure Emulation — simulated result across source images.*
**Source**: A high-contrast portrait (studio lighting, dark background) — the kind of subject that showcases intaglio printing at its finest.

**Objective**: Combine all processing stages to create a complete photogravure print emulation with plate mark, grain, ink color, and paper warmth.

1. **Set shadow depth**: Shadow Depth to ~60%. Rich, extended shadows.
2. **Add grain**: Grain to ~40%. Fine midtone texture.
3. **Enable plate mark**: Turn Plate Mark on and set Plate Margin to ~20%. A rectangular border frames the image.
4. **Select iron gall ink**: Set both Ink Color A and B to On (preset "11"). The print takes on the distinctive blue-black tone of antique iron gall ink.
5. **Warm the paper**: Increase Paper Warmth to ~60%. The paper base shifts from neutral white to a golden cream, contrasting beautifully with the cool iron gall ink.
6. **Add pooling**: Set Ink Pooling to ~25%. A subtle lift in the deepest shadows adds physical dimension.
7. **Final density**: Adjust Ink Density to ~80%. The print should have rich, saturated darks without blocking up.
8. **A/B compare**: Toggle Bypass to compare the original video with the gravure rendition.

**Key concepts**: All processing stages compound to create a complete print simulation, ink color and paper warmth interact to define the emotional temperature of the print, plate mark adds compositional framing, bypass enables instant comparison

---


## Tips

- **Sepia for warmth, iron gall for drama**: The four ink presets serve different aesthetic purposes. Warm Sepia and Neutral Brown evoke fine-art portraiture; Cool Black suits documentary or newspaper aesthetics; Iron Gall adds an antique, archival quality.
- **Grain reveals midtone content**: Because aquatint grain is strongest in the midtones and absent at extremes, it naturally draws the eye to the tonal regions where photographic detail is richest.
- **Paper warmth interacts with ink colour**: Warm paper with warm ink (sepia) produces a harmonious golden tone. Warm paper with cool ink (iron gall) creates a tension between the blue-black ink and the golden paper — historically authentic and visually striking.
- **Pooling prevents crushed blacks**: A small amount of ink pooling (10–20%) prevents deep shadows from going to solid black, maintaining the sense of physical depth that distinguishes gravure prints from digital reproductions.
- **Plate mark as framing**: Enable Plate Mark whenever using Gravure for still image presentation — the rectangular border provides compositional grounding and immediately signals "print" to the viewer.
- **Feedback loops**: Routing the gravure output back to the input creates a progressively more stylized print effect — each pass deepens the shadow curve and reapplies the grain, producing a woodcut-like quality after several iterations.
- **Bypass for A/B**: Switch 11 provides instant comparison between the original video and the gravure rendition — essential for calibrating shadow depth and grain intensity to taste.

---

## Glossary

| Term | Definition |
|------|------------|
| **Aquatint** | A printmaking technique using granular resin to create tonal areas; in Gravure, the stochastic grain texture derived from LFSR noise. |
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric (Gravure uses zero BRAMs). |
| **Concave Curve** | A tone curve where the output falls below the identity line, deepening shadows relative to a linear mapping. |
| **Density** | In printmaking, the amount of ink deposited; higher density = darker areas. The VHDL inverts luminance to create density. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Intaglio** | A family of printing techniques where ink is held in recessed areas of a plate, including photogravure, etching, and engraving. |
| **Iron Gall** | A historical ink made from iron salts and tannic acid, producing a blue-black color that deepens with age. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used here to produce the aquatint grain pattern (seed 0x7E5D). |
| **Photogravure** | An intaglio printing process using acid-etched copper plates to transfer photographic images onto paper with continuous-tone fidelity. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Plate Mark** | The rectangular impression left in the paper by the edge of a copper printing plate; a hallmark of intaglio prints. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **Rotogravure** | The industrial cylinder-based variant of gravure used for high-volume printing (newspapers, magazines, packaging). |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
