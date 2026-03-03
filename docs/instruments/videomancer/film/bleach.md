---
draft: true
sidebar_position: 21
slug: /instruments/videomancer/bleach
title: "Bleach"
image: /img/instruments/videomancer/bleach/bleach_hero_s1.png
description: "Bleach simulates the photochemical bleach bypass (also known as skip bleach or ENR) process — a film lab technique where the bleach step in colour negative development is partially or fully omitted, leaving metallic silver in the emulsion alongside the colour dyes."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import bleach_control_panel from '/img/instruments/videomancer/bleach/bleach_control_panel.png';
import bleach_source1_cat from '/img/instruments/videomancer/bleach/bleach_source1_cat.png';
import bleach_source2_field from '/img/instruments/videomancer/bleach/bleach_source2_field.png';
import bleach_source3_clouds from '/img/instruments/videomancer/bleach/bleach_source3_clouds.png';
import bleach_source4_pattern from '/img/instruments/videomancer/bleach/bleach_source4_pattern.png';
import bleach_source5_woman from '/img/instruments/videomancer/bleach/bleach_source5_woman.png';
import bleach_source6_knit from '/img/instruments/videomancer/bleach/bleach_source6_knit.png';
import bleach_hero_s1 from '/img/instruments/videomancer/bleach/bleach_hero_s1.png';
import bleach_hero_s2 from '/img/instruments/videomancer/bleach/bleach_hero_s2.png';
import bleach_hero_s3 from '/img/instruments/videomancer/bleach/bleach_hero_s3.png';
import bleach_hero_s4 from '/img/instruments/videomancer/bleach/bleach_hero_s4.png';
import bleach_hero_s5 from '/img/instruments/videomancer/bleach/bleach_hero_s5.png';
import bleach_hero_s6 from '/img/instruments/videomancer/bleach/bleach_hero_s6.png';
import bleach_ex1_s1 from '/img/instruments/videomancer/bleach/bleach_ex1_s1.png';
import bleach_ex1_s2 from '/img/instruments/videomancer/bleach/bleach_ex1_s2.png';
import bleach_ex1_s3 from '/img/instruments/videomancer/bleach/bleach_ex1_s3.png';
import bleach_ex1_s4 from '/img/instruments/videomancer/bleach/bleach_ex1_s4.png';
import bleach_ex1_s5 from '/img/instruments/videomancer/bleach/bleach_ex1_s5.png';
import bleach_ex1_s6 from '/img/instruments/videomancer/bleach/bleach_ex1_s6.png';
import bleach_ex2_s1 from '/img/instruments/videomancer/bleach/bleach_ex2_s1.png';
import bleach_ex2_s2 from '/img/instruments/videomancer/bleach/bleach_ex2_s2.png';
import bleach_ex2_s3 from '/img/instruments/videomancer/bleach/bleach_ex2_s3.png';
import bleach_ex2_s4 from '/img/instruments/videomancer/bleach/bleach_ex2_s4.png';
import bleach_ex2_s5 from '/img/instruments/videomancer/bleach/bleach_ex2_s5.png';
import bleach_ex2_s6 from '/img/instruments/videomancer/bleach/bleach_ex2_s6.png';
import bleach_ex3_s1 from '/img/instruments/videomancer/bleach/bleach_ex3_s1.png';
import bleach_ex3_s2 from '/img/instruments/videomancer/bleach/bleach_ex3_s2.png';
import bleach_ex3_s3 from '/img/instruments/videomancer/bleach/bleach_ex3_s3.png';
import bleach_ex3_s4 from '/img/instruments/videomancer/bleach/bleach_ex3_s4.png';
import bleach_ex3_s5 from '/img/instruments/videomancer/bleach/bleach_ex3_s5.png';
import bleach_ex3_s6 from '/img/instruments/videomancer/bleach/bleach_ex3_s6.png';

# Bleach

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: bleach_source1_cat, after: bleach_hero_s1 },
    { label: "Field", before: bleach_source2_field, after: bleach_hero_s2 },
    { label: "Clouds", before: bleach_source3_clouds, after: bleach_hero_s3 },
    { label: "Pattern", before: bleach_source4_pattern, after: bleach_hero_s4 },
    { label: "Woman", before: bleach_source5_woman, after: bleach_hero_s5 },
    { label: "Knit", before: bleach_source6_knit, after: bleach_hero_s6 },
  ]}
/>
*Desaturated, silver-dense highlights surge through high-contrast shadows, recreating the bleach bypass look of war films and noir thrillers.*

---

## Overview

Bleach simulates the photochemical bleach bypass (also known as skip bleach or ENR) process — a film lab technique where the bleach step in colour negative development is partially or fully omitted, leaving metallic silver in the emulsion alongside the colour dyes. The result is a distinctive high-contrast, desaturated image with dense, luminous highlights and crushed shadows. This look was famously used in *Saving Private Ryan* (1998), *Se7en* (1995), *Minority Report* (2002), and many war and noir films.

The entire processing pipeline uses only shift-based arithmetic — no multiplications — ensuring reliable timing closure on the iCE40 HX4K at 74.25 MHz. This gives the pipeline an angular, stepped character that actually enhances the photochemical feel, since film grain and developing chemistry are inherently nonlinear processes.

The name directly references the bleach chemistry step. In standard C-41 film processing, the bleach bath removes the metallic silver after colour dyes have formed, leaving only the transparent dye layers. Omitting or shortening this step retains the opaque silver, which adds density, reduces saturation, and increases perceived contrast. Bleach puts this chemical decision into the hands of the video artist as a bank of real-time controls.

---

## Background

### The Bleach Bypass Process

In conventional photochemical colour film processing, exposed silver halide crystals are developed into metallic silver, colour couplers form transparent dyes around the silver, then the bleach bath dissolves the silver away, leaving only the colour dye image. When the bleach step is skipped or shortened, the metallic silver remains in the emulsion — superimposed on the colour dyes. This silver acts as a neutral-density filter that (1) reduces colour saturation because the opaque silver overlaps the transparent dyes, (2) increases contrast because silver density adds to the existing dye density, and (3) changes highlight character because silver grains have a different reflective quality than dye layers.

### ENR vs Skip Bleach

Two historical variants exist. The **ENR** process (named after its inventor Ernesto Novelli Rizzoli at Technicolor Rome) uses a secondary silver developer bath to *add* silver rather than skip the bleach entirely. This provides finer control — the silver density can be adjusted by varying the developer time. The **skip bleach** variant simply omits or shortens the bleach bath, producing a more aggressive effect with stronger silver retention. Bleach's Process toggle selects between these two approaches, with ENR applying a more proportional luma boost and Skip applying a stronger fixed boost.

### Shift-Based Arithmetic

The entire pipeline avoids hardware multipliers. Desaturation pulls chroma toward the midpoint by subtracting shifted versions of the offset. Silver boost adds the luma shifted right by 0–4 bits. Contrast stretches the midpoint deviation by adding its own shifted copy. This shift-only approach creates characteristic threshold steps at pot values 256, 512, and 768, producing a stepwise "chemical" feel where the process amount jumps between discrete developing times rather than sliding continuously.

### Film Grain

Real film grain arises from the random spatial distribution of silver halide crystals in the emulsion. Faster film stocks have larger crystals, producing coarser, more visible grain. Bleach's grain injection uses a 16-bit LFSR pseudo-random noise source, with the Fine/Coarse toggle selecting either 6-bit or shifted 6-bit ranges for subtle versus prominent grain textures.

### Tone Shift

Retained silver has a slight colour cast depending on the emulsion chemistry and development temperature. Bleach models this as a fixed additive offset — Cold adds blue (U+12, V−8) and Warm adds amber (U−8, V+12) — creating the characteristic cool steel or warm sepia tone associated with different bleach bypass implementations.


---

## Signal Flow

```
                              ┌────────────────────┐
data_in ─────────────────────►│ Input Register      │
                              └──────┬─────────────┘
                                     │ Stage 1
                                     ▼
                              ┌────────────────────┐
                              │ Desaturation        │
                              │ (shift chroma       │
                              │  toward 512)        │
                              └──────┬─────────────┘
                                     │ Stage 2
                                     ▼
                              ┌────────────────────┐
                              │ Silver Blend        │
                              │ (shift-add Y boost  │
                              │  ENR vs Skip)       │
                              └──────┬─────────────┘
                                     │ Stage 3
                                     ▼
                              ┌────────────────────┐
                              │ Contrast Stretch    │
                              │ (shift from         │
                              │  midpoint 512)      │
                              └──────┬─────────────┘
                                     │ Stage 4
                                     ▼
                              ┌────────────────────┐
                              │ Hi Protect + Black  │
                              │ Pt + Grain + Tone   │
                              │ + Invert + Output   │
                              └──────┬─────────────┘
                                     │ Stage 5
                                     ▼
data_in ──► [sync delay] ──► dry ──► Interpolator ◄── wet
                                       (4 clk)
                                          │
                                          ▼
                                      data_out
```

The pipeline is strictly serial — each stage modifies the signal and passes it to the next. The desaturation stage reduces chroma saturation before any luma processing, mirroring the chemistry where silver overlaps the dyes. The silver blend stage then boosts luma proportionally to its current value (modelling the density of retained silver, which is proportional to exposure). The contrast stage expands the tonal range around the midpoint. Finally, Stage 5 applies four independent corrections: highlight protection blends bright pixels back toward the original to prevent clipping, black point lift prevents shadows from crushing to zero, grain adds LFSR noise, and tone shift adds a colour cast.

The signal path for the original Y value is carried through as `s_y_orig` for the highlight protection blend in Stage 5, creating a parallel data path that preserves the pre-silver, pre-contrast brightness for selective blending in the highlights.

---

## Parameter Reference

<img src={bleach_control_panel} alt="Videomancer front panel with Bleach loaded"/>
*Videomancer's front panel with Bleach active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Bypass Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls the amount of bleach bypass (silver retention) applied, affecting primarily the desaturation depth. The pot value is decoded into four threshold zones: at low values (0–255), chroma passes through unaffected; at 256–511, light desaturation removes 12.5% of chroma offset; at 512–767, moderate desaturation removes 25%; at high values (768–1023), strong desaturation removes 50%, leaving only half the original colour saturation. This models the duration of the bleach bath — less bleaching means more retained silver and thus more desaturation.

---

#### Knob 2 — Silver
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the silver density — how much additional luminance is added by the retained metallic silver. The pot is decoded into four zones with shift-based boost amounts. In ENR mode, the boost is proportional to the pixel's own brightness (modelling the chemistry where silver formation tracks exposure). In Skip mode, the boost is approximately twice as strong at each threshold. At low values (0–255), the boost is Y>>4 (about 6%); at high values (768–1023) in ENR mode, the boost is Y>>1 (50%). The result is saturating-added to the current luma.

---

#### Knob 3 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

Applies a contrast stretch centred at midpoint 512. The deviation from 512 is calculated, then a shifted copy of that deviation is added back. At low values, no stretch is applied (1.0× gain). At 256–511, a 1.125× stretch; at 512–767, a 1.25× stretch; at high values, a 1.5× stretch. The result is clamped to 0–1023. This models how retained silver increases the gamma of the film stock, pushing shadows darker and highlights brighter.

---

#### Knob 4 — Grain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Injects film grain noise from the LFSR. Below 256, no grain is added. From 256–511, moderate grain is injected using 5-bit (Fine) or 5-bit shifted (Coarse) LFSR samples. From 512–1023, stronger grain uses 6-bit (Fine) or 6-bit shifted (Coarse) samples. Fine grain produces a tight, subtle texture; Coarse grain produces larger, more prominent speckle. The grain is added as a signed value to luma, creating both bright and dark noise particles.

---

#### Knob 5 — Hi Prot
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Protects highlights from clipping. When both the original (pre-silver, pre-contrast) Y value exceeds 768 and this pot exceeds 256, the output luma is averaged with the original brightness. This pulls blown highlights back toward their natural level, preventing the silver boost and contrast stretch from pushing bright areas into hard clipping. At 0%, no protection is applied and highlights may clip aggressively. At higher values, the blend kicks in for any pixel originally brighter than 75% luma.

---

#### Knob 6 — Black Pt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Lifts the black point, setting a minimum floor for luma. The pot value shifted right by 3 gives a floor from 0 to 127. At 0%, the floor is zero and deep blacks are preserved. At higher values, the darkest shadows are lifted, reducing contrast in the shadow range. This models the "fog" level in under-bleached prints, where residual silver adds a slight overall density even in unexposed areas.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Process** | ENR | Skip |
| **8 — Grain Sz** | Fine | Coarse |
| **9 — Tone** | Cold | Warm |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control the chemical variant, grain character, colour tone, inversion, and bypass. Each affects an independent aspect of the bleach bypass simulation. Toggle 7 selects the processing variant (ENR vs Skip), Toggle 8 and Grain pot together control grain texture, Toggle 9 adds a colour cast, Toggle 10 inverts luma, and Toggle 11 bypasses all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) and wet (processed) signal at the output stage using three parallel interpolators. At 0% the output is the unmodified input; at 100% the output is fully processed with bleach bypass effects. Intermediate values blend the processed look with the original, useful for dialing in a subtle desaturated, contrasty look without fully committing to the bleach bypass aesthetic.

---

## Guided Exercises

These exercises progress from basic desaturation through full silver retention to the complete bleach bypass aesthetic with grain and tone.

### Exercise 1: Basic Desaturation

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: bleach_source1_cat, after: bleach_ex1_s1 },
    { label: "Field", before: bleach_source2_field, after: bleach_ex1_s2 },
    { label: "Clouds", before: bleach_source3_clouds, after: bleach_ex1_s3 },
    { label: "Pattern", before: bleach_source4_pattern, after: bleach_ex1_s4 },
    { label: "Woman", before: bleach_source5_woman, after: bleach_ex1_s5 },
    { label: "Knit", before: bleach_source6_knit, after: bleach_ex1_s6 },
  ]}
/>
*Basic Desaturation — simulated result across source images.*
**Source**: Colourful footage — flowers, clothing, or colourful scenery.

**Objective**: Understand how the Bypass Amt control desaturates chroma in stepped thresholds.

1. **Full colour**: Start with Bypass Amt at 0%. The image passes through with no desaturation.
2. **Light desat**: Increase Bypass Amt past 25%. A subtle reduction in saturation appears.
3. **Moderate**: Push past 50%. Colours lose about a quarter of their intensity.
4. **Strong**: Push past 75%. Colours are now only half their original saturation — clearly washed out.
5. **Compare**: Toggle Bypass on and off to compare the desaturated result with the original.
6. **Threshold steps**: Move Bypass Amt slowly and notice the step-like transitions at 25%, 50%, 75%.

**Key concepts**: Desaturation pulls chroma toward neutral 512 using shifted offsets, four discrete thresholds model different bleach bath durations, the effect is most visible on saturated colours

---

### Exercise 2: Silver Density and Contrast

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: bleach_source1_cat, after: bleach_ex2_s1 },
    { label: "Field", before: bleach_source2_field, after: bleach_ex2_s2 },
    { label: "Clouds", before: bleach_source3_clouds, after: bleach_ex2_s3 },
    { label: "Pattern", before: bleach_source4_pattern, after: bleach_ex2_s4 },
    { label: "Woman", before: bleach_source5_woman, after: bleach_ex2_s5 },
    { label: "Knit", before: bleach_source6_knit, after: bleach_ex2_s6 },
  ]}
/>
*Silver Density and Contrast — simulated result across source images.*
**Source**: A high-dynamic-range scene — a window looking outdoors, or a face lit from one side.

**Objective**: Explore how Silver and Contrast controls interact to create the signature bleach bypass look.

1. **Set desaturation**: Bypass Amt at about 70%.
2. **Add silver**: Increase Silver from 0% to 80%. Watch the highlights surge brighter as retained silver adds density.
3. **ENR vs Skip**: Toggle Process between ENR and Skip. Skip mode is noticeably more aggressive.
4. **Contrast stretch**: Now increase Contrast from 0% to about 60%. Shadows drop darker while highlights push brighter.
5. **Highlight blow-out**: Notice that extreme Silver + Contrast clips the highlights. Increase Hi Prot to pull them back.
6. **Black floor**: Increase Black Pt slightly. The deepest shadows lift off true black, adding a "fog" floor.

**Key concepts**: Silver adds density (luma boost) proportional to brightness, ENR is proportional while Skip is aggressive, Contrast expands the midpoint deviation, Hi Prot prevents highlight clipping

---

### Exercise 3: Full Film Look

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: bleach_source1_cat, after: bleach_ex3_s1 },
    { label: "Field", before: bleach_source2_field, after: bleach_ex3_s2 },
    { label: "Clouds", before: bleach_source3_clouds, after: bleach_ex3_s3 },
    { label: "Pattern", before: bleach_source4_pattern, after: bleach_ex3_s4 },
    { label: "Woman", before: bleach_source5_woman, after: bleach_ex3_s5 },
    { label: "Knit", before: bleach_source6_knit, after: bleach_ex3_s6 },
  ]}
/>
*Full Film Look — simulated result across source images.*
**Source**: Any footage — this exercise creates the complete bleach bypass film look.

**Objective**: Combine all processing stages for a war-film or noir aesthetic.

1. **Base look**: Bypass Amt ~75%, Silver ~60%, Contrast ~55%.
2. **Add grain**: Set Grain to about 40%. Fine grain appears as a subtle photographic noise.
3. **Coarse grain**: Toggle Grain Sz to Coarse. The grain becomes chunkier and more prominent.
4. **Cold tone**: Ensure Tone is set to Cold. The image takes on a steely blue cast — the *Saving Private Ryan* look.
5. **Switch to warm**: Toggle Tone to Warm. The cast shifts to amber — more *The Aviator* than *Saving Private Ryan*.
6. **Hi Prot + Black Pt**: Set Hi Prot to about 50%, Black Pt to about 10%.
7. **Mix for subtlety**: Reduce Mix to about 70% to blend the processed look with the original.

**Key concepts**: All stages compound: desaturation + silver + contrast + grain + tone create a unified photochemical aesthetic, Mix blending allows subtle application, tone shift establishes colour temperature

---


## Tips

- **Start with desaturation**: The bleach bypass look is primarily about *reduced colour*, not about contrast. Set Bypass Amt first, then add Silver and Contrast to taste.
- **ENR for subtlety, Skip for impact**: ENR mode produces a more controlled lift suitable for narrative filmmaking; Skip mode is more aggressive, better for music videos and stylised work.
- **Highlight protection saves detail**: If Silver and Contrast push highlights too hard, Hi Prot at 40–60% brings them back without reducing the impact in midtones and shadows.
- **Black Pt as "film fog"**: A small Black Pt lift (5–15%) adds the look of under-developed print stock — shadows never reach true black.
- **Fine grain + Mix = photographic subtlety**: Fine grain at 25–35% with Mix at 70–80% creates a naturalistic film look that integrates seamlessly with video.
- **Cold + desaturated = war film**: The *Saving Private Ryan* look is primarily high desaturation + moderate silver + cold tone.
- **Use Invert for textures**: Invert + high contrast + grain creates abstract video textures suitable for overlay compositing.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bleach bypass** | A photochemical film processing technique in which the bleach bath is partially or fully omitted, leaving metallic silver in the emulsion alongside colour dyes to increase contrast and reduce saturation. |
| **C-41** | The standard chemical process for developing colour negative film, consisting of developer, bleach, and fixer baths. |
| **Chroma** | The colour-difference components (U and V) of a YUV video signal, representing hue and saturation independently of brightness. |
| **Clamping** | Limiting a signal value to a fixed range (typically 0–1023 in 10-bit video) to prevent overflow or underflow artifacts. |
| **ENR** | Ernesto Novelli Rizzoli process; a controlled secondary silver development technique invented at Technicolor Rome that adds metallic silver proportionally to exposure. |
| **Interpolator** | A hardware mixing block that crossfades between two input signals using a weighted average, used here for dry/wet blending. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function of its previous state, producing a pseudo-random bit sequence used for film grain noise. |
| **Luma** | The brightness component (Y) of a YUV video signal, independent of colour information. |
| **Saturating add** | An addition operation that clamps the result at the maximum representable value rather than wrapping around on overflow. |
| **Silver halide** | Light-sensitive crystalline compound (such as silver bromide) embedded in photographic film emulsion that forms the latent image upon exposure. |
| **Skip bleach** | A variant of bleach bypass that omits the bleach bath entirely rather than shortening it, producing a more aggressive high-contrast effect than ENR. |
| **YUV** | A colour encoding system that separates brightness (Y) from two colour-difference components (U and V), used as the native signal format in Videomancer. |

---
