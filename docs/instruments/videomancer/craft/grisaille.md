---
draft: true
sidebar_position: 116
slug: /instruments/videomancer/grisaille
title: "Grisaille"
image: /img/instruments/videomancer/grisaille/grisaille_hero.png
description: "Oil painters of the Renaissance did not paint color directly onto canvas."
---

import grisaille_hero from '/img/instruments/videomancer/grisaille/grisaille_hero.png';
import grisaille_before_after from '/img/instruments/videomancer/grisaille/grisaille_before_after.png';
import grisaille_control_panel from '/img/instruments/videomancer/grisaille/grisaille_control_panel.png';
import grisaille_exercise1_result from '/img/instruments/videomancer/grisaille/grisaille_exercise1_result.png';
import grisaille_exercise2_result from '/img/instruments/videomancer/grisaille/grisaille_exercise2_result.png';
import grisaille_exercise3_result from '/img/instruments/videomancer/grisaille/grisaille_exercise3_result.png';

# Grisaille

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={grisaille_hero} alt="Grisaille hero image"/>
*Grisaille applying luminance-dependent oil glaze simulation with craquelure cracks and patina yellowing to a richly textured source.*
<img src={grisaille_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Grisaille applied.*

---

## Overview

Oil painters of the Renaissance did not paint color directly onto canvas. They began with a monochrome underpainting — a **grisaille** — that established the tonal structure of the composition in shades of gray. Once dry, they applied thin, translucent layers of pigmented oil called **glazes** over the grisaille, gradually reintroducing color. Shadows received fewer glaze layers and remained nearly monochrome; highlights received more and bloomed with saturated hue. Grisaille recreates this centuries-old layering process in real time on a live video signal.

The program chains five processing stages: a piecewise-linear grisaille tone curve (shadow lift, midtone compression, highlight handling), a luminance-dependent chroma glaze with four selectable gamma exponents, an imprimatura ground tint, an aged oil patina that shifts color toward yellow, and a procedural craquelure crack overlay that darkens pixels along a modular grid. The name *grisaille* comes from the French *gris* (gray) — the monochrome technique that forms the foundation of this program's signal flow.

At conservative settings — moderate shadow lift, linear glaze curve, no patina — Grisaille produces a subtle desaturation of shadows while preserving full color in bright areas, much like a well-preserved Vermeer interior. At extreme settings — full grisaille mode, heavy craquelure, deep patina — the image resembles a cracked and yellowed Old Master painting viewed through museum glass.

---

## Background

### What Is Grisaille Underpainting?

In European oil painting from the 14th century onward, artists constructed their images in layers. The first layer was the **grisaille** — a monochrome underpainting in earth tones or pure gray that established the composition's value structure: where light falls, where shadow lies, how forms recede into space. The grisaille was not meant to be seen in the finished work; it was the skeleton beneath the skin of color. Grisaille uses the same approach: it can optionally strip the video signal down to pure luminance, creating a monochrome underpainting that subsequent stages rebuild with controlled color.

### What Is an Oil Glaze?

An oil **glaze** is a thin, translucent layer of pigment suspended in a slow-drying medium like linseed oil. Because the layer is translucent, the grisaille underpainting shows through, and the perceived color is a mixture of the glaze hue and the gray value beneath. Crucially, shadows — where the underpainting is dark — absorb most of the glaze light and remain nearly monochrome, while highlights — where the underpainting is bright — reflect the full glaze color. This luminance-dependent color saturation is the core of the Grisaille program's Stage 2, where chroma is scaled by a function of luminance using one of four gamma curves.

### What Are Gamma Curves?

A **gamma curve** is a power function that remaps values nonlinearly. In this program, gamma controls how the glaze opacity depends on luminance. A gamma of 0.5 (square root) lifts shadow opacity — more color survives in dark areas. A gamma of 1.0 is linear — opacity tracks brightness proportionally. A gamma of 1.5 or 2.0 (quadratic) suppresses shadow opacity aggressively — only the brightest areas retain color, producing the deep chiaroscuro look associated with Flemish painters like Jan van Eyck.

### What Is Craquelure?

Over centuries, the oil medium in a painting dries, shrinks, and cracks. The resulting network of fine fissures is called **craquelure**. Art conservators study crack patterns to date and authenticate paintings — different media, grounds, and climates produce characteristic crack geometries. Grisaille simulates craquelure with a modular-arithmetic grid: pixel coordinates are divided by a period (24 or 48 pixels), and positions near the grid boundaries are darkened proportionally. The result is a regular network of dark lines overlaid on the processed image.

### What Is Patina?

Linseed oil, the most common binding medium in European oil painting, yellows as it ages. This slow chemical shift pushes the color balance of old paintings toward warm amber — a change conservators call **patina**. In Grisaille, the patina stage shifts the chrominance toward yellow by decreasing U (blue-yellow axis) and slightly increasing V (red-cyan axis). The effect is cumulative with the glaze and ground tint stages.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Grisaille Tone Curve     (piecewise-linear shadow lift + highlight compress)
│   ├─ 2. Glaze Pass-Through       (Y unchanged; glaze affects only chroma)
│   ├─ 3. Craquelure Overlay       (darken Y on modular grid crack lines)
│   └─ 4. Output Composite         (→ interpolator_u mix)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Ground Tint              (warm: U−20 V+15 / cool: no offset)
│   ├─ 2. Luminance-Dependent Glaze (scale chroma toward neutral by f(Y) × opacity)
│   ├─ 3. Patina                   (shift U down, V up — oil yellowing)
│   └─ 4. Output Composite         (→ interpolator_u mix)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay pipeline (matched to processing + interpolator)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical interaction is between the Y tone curve (Stage 1) and the luminance-dependent glaze (Stage 2). The tone curve reshapes luminance *before* it is used to compute glaze opacity, so raising the shadow floor with Knob 1 changes how much color the glaze will restore to shadow regions. A second key path is the ground tint, which offsets U/V in Stage 1 *before* the glaze attenuates chroma, so the warm earth tone is partially preserved even when glaze opacity is low. Craquelure operates on the already-glazed luminance, so cracks darken through both the tonal and color-processed result.

---

## Parameter Reference

<img src={grisaille_control_panel} alt="Videomancer front panel with Grisaille loaded"/>
*Videomancer's front panel with Grisaille active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Shadow Lift
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the shadow floor of the grisaille tone curve. The pot value is right-shifted by 2 to produce a floor in the range 0–255. Shadow-region pixels (Y < 256) are lifted toward this floor, compressing the darkest tones upward. The midtone and highlight regions are remapped proportionally above the new floor. At zero, shadows remain black; at maximum, the entire tonal range compresses into the upper half, producing a washed-out, underexposed look. This control has the strongest visible effect on dark source material — faces lit from one side, deep architectural shadows, or nighttime scenes.

---

#### Knob 2 — Glaze Opacity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Sets the base chroma opacity for the glaze stage. The glaze multiplies this opacity by a luminance-dependent function (selected by Knob 3) to determine how much original color survives at each brightness level. At zero, the output is fully monochrome regardless of the gamma curve — no color passes through the glaze. At maximum, the glaze allows nearly full saturation at bright luminance values. The interaction with the Glaze Curve control is fundamental: opacity sets the *amount* of color, while the curve sets the *distribution* of color across the tonal range.

---

#### Knob 3 — Glaze Curve
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Selects one of four gamma exponents for the luminance-dependent glaze function. The pot range is divided into four equal zones. The lowest zone applies a gamma of approximately 0.5 (square root), which lifts shadow opacity and distributes color more evenly across the tonal range. The second zone applies gamma 1.0 (linear). The third applies gamma 1.5, and the fourth applies gamma 2.0 (quadratic), which concentrates color in the highlights and desaturates shadows aggressively. The higher gamma values produce the deep chiaroscuro look of Flemish oil painting.

---

#### Knob 4 — Patina
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of the patina (aged oil yellowing) effect. The pot value is right-shifted by 2 and used to decrease U (shifting toward yellow on the blue-yellow axis) and slightly increase V (adding a touch of warmth). At zero, no yellowing is applied. At maximum, the image acquires a strong amber cast reminiscent of centuries-old oil paintings. Patina is applied after the glaze stage, so it yellows whatever chroma the glaze has allowed through — heavily glazed highlights yellow more visibly than desaturated shadows.

---

#### Knob 5 — Craquelure
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the darkness of the procedural craquelure crack overlay. The VHDL computes crack positions using modular arithmetic on the horizontal and vertical pixel counters — pixels whose position modulo the crack period falls below the crack width are identified as crack pixels. For those pixels, luminance is reduced by a fraction proportional to this control: the darkening amount is (craquelure × Y) >> 10. At zero, no cracks are visible. At maximum, crack-line pixels are significantly darkened, creating a visible grid of age lines across the image.

---

#### Knob 6 — Ground Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Labelled Ground Tint and configured as a 360° polar control in the TOML. In the current VHDL implementation, this register is mapped to the signal `s_ground_tint` but is not used in any processing stage — the ground tinting is controlled entirely by the Ground Type toggle (Switch 7), which applies fixed warm or cool offsets. This pot is reserved for a future firmware revision that may add continuous imprimatura hue rotation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Ground Type** | Warm | Cool |
| **8 — Crack Scale** | Fine | Coarse |
| **9 — Color Mode** | Full | Grisaille |
| **10 — Impasto** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent options. Switch 7 selects a fixed ground tint. Switch 8 changes the craquelure grid resolution. Switch 9 selects between full-color and pure grisaille (monochrome) output. Switch 10 enables impasto highlight clipping. Switch 11 bypasses all processing. None of the toggles form a combined mode selector — each operates independently on a different stage of the pipeline.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade via three interpolator_u instances (one per YUV channel). At maximum (default), the output is fully processed. At minimum, the output is the unprocessed input (delayed by 8 clocks to match pipeline latency). Intermediate values produce a proportional blend, which is useful for reducing the intensity of heavy craquelure or patina effects without changing individual control settings.

---

## Guided Exercises

These exercises progress from the foundational grisaille underpainting through glaze layering to the full aged-painting simulation with cracks and patina.

### Exercise 1: The Grisaille Underpainting

<img src={grisaille_exercise1_result} alt="The Grisaille Underpainting result"/>
*The Grisaille Underpainting — simulated result across source images.*
**Source**: A portrait or still life with strong directional lighting — faces, fruit, or architectural details with clear shadow and highlight separation.

**Objective**: Learn how the grisaille tone curve and shadow lift interact to create a monochrome underpainting.

1. **Force monochrome**: Set Color Mode (Switch 9) to Grisaille. The image drops to pure gray — this is the underpainting.
2. **Observe the tone curve**: With Shadow Lift at its default (~25%), notice that the deepest shadows are not quite black — they have been lifted off the floor.
3. **Sweep shadow lift**: Turn Shadow Lift slowly from 0% to 100%. Watch the shadow regions compress upward, reducing overall contrast. At maximum, the image becomes flat and washed out.
4. **Set a moderate floor**: Return Shadow Lift to approximately 20%. The shadows should have visible detail without losing the sense of depth.
5. **Enable impasto**: Turn on Impasto (Switch 10). Highlights above ~75% brightness snap to pure white — flat, bright plateaus against the modulated shadows.

**Key concepts**: Grisaille underpainting separates tonal structure from color, shadow lift controls the black point, impasto creates opaque highlight regions

---

### Exercise 2: Glazing the Underpainting

<img src={grisaille_exercise2_result} alt="Glazing the Underpainting result"/>
*Glazing the Underpainting — simulated result across source images.*
**Source**: The same source as Exercise 1, or any footage with a range of skin tones, warm fabrics, and cool shadows.

**Objective**: Explore how the luminance-dependent glaze reintroduces color over the monochrome foundation.

1. **Return to full color**: Set Color Mode (Switch 9) back to Full. Color returns, modulated by the glaze.
2. **Set linear glaze**: Turn Glaze Curve to zone 2 (gamma 1.0). Color is distributed proportionally — bright areas get proportionally more color.
3. **Sweep glaze opacity**: Turn Glaze Opacity from 0% (fully monochrome) to 100%. Watch color fade in from the highlights down through the midtones.
4. **Try chiaroscuro**: Move Glaze Curve to zone 4 (gamma 2.0). Shadows become deeply desaturated while highlights bloom with full color. This is the van Eyck look.
5. **Warm ground**: Ensure Ground Type (Switch 7) is set to Warm. Notice the subtle amber warmth in the midtones — the imprimatura showing through the glaze.
6. **Compare cool**: Switch Ground Type to Cool. The warmth disappears, replaced by a cooler, more neutral gray.

**Key concepts**: Glaze opacity controls how much color passes through, gamma curve shapes the luminance-to-color relationship, ground tint adds a fixed color bias before the glaze

---

### Exercise 3: The Aging Master

<img src={grisaille_exercise3_result} alt="The Aging Master result"/>
*The Aging Master — simulated result across source images.*
**Source**: Any richly detailed source — landscapes, interiors, or textured surfaces work well.

**Objective**: Combine all processing stages to create the appearance of a centuries-old oil painting.

1. **Establish base**: Set Shadow Lift ~25%, Glaze Opacity ~60%, Glaze Curve to zone 3 (gamma 1.5).
2. **Apply patina**: Turn Patina to approximately 50%. Watch the color balance shift toward amber-yellow — the image begins to look aged.
3. **Add fine cracks**: Increase Craquelure to approximately 60%. A grid of dark hairline cracks appears across the image.
4. **Switch to coarse**: Toggle Crack Scale (Switch 8) to Coarse. The crack network becomes wider and more widely spaced.
5. **Combine with impasto**: Enable Impasto (Switch 10). The bright highlights clip to white, creating maximum contrast at crack boundaries.
6. **Reduce mix**: Pull the Mix fader down to approximately 70%. The raw source bleeds back in, softening the effect as if viewing the painting through restoration varnish.
7. **A/B comparison**: Toggle Bypass (Switch 11) to compare the aged painting with the original source.

**Key concepts**: Patina yellows the color balance, craquelure creates age-related crack textures, impasto and craquelure interact at highlight boundaries, mix allows partial blending with the source

---


## Tips

- **Order matters**: Tone curve → Ground tint → Glaze → Patina → Craquelure → Impasto → Mix. The tone curve shapes luminance *before* the glaze uses it to compute color opacity, so shadow lift directly changes how much color the glaze restores.
- **Gamma 2.0 is the signature effect**: The quadratic glaze curve produces deep shadow desaturation with rich highlight color — the chiaroscuro look that defines Renaissance oil painting simulation.
- **Grisaille mode is an override**: Setting Color Mode to Grisaille forces zero chroma opacity regardless of Knob 2. Use it to preview the tone curve and craquelure without color distraction.
- **Patina stacks with ground tint**: Both shift U/V — patina yellows, ground tint warms. Together they produce a strong amber bias. Use one or the other for subtlety.
- **Craquelure follows screen coordinates**: The crack grid is locked to pixel position, not video content. Moving the source does not move the cracks — they act as a fixed overlay, like real cracks in a painted canvas.
- **Pot 6 is reserved**: The Ground Tint potentiometer is mapped in the TOML as a 360° polar control, but the VHDL does not currently use it. Ground tinting is controlled entirely by Switch 7 (Warm/Cool).
- **Feedback loops**: Routing the output back to the input accumulates shadow lift and patina yellowing frame over frame, progressively aging the image until it saturates.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed signal.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chiaroscuro** | An artistic technique using strong contrast between light and dark to model three-dimensional form. Literally "light-dark" in Italian. |
| **Craquelure** | The network of fine cracks that forms on the surface of old oil paintings as the medium dries and shrinks over centuries. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Gamma Curve** | A power function that remaps values nonlinearly; used here to control how glaze opacity depends on luminance. |
| **Glaze** | A thin, translucent layer of pigment in oil medium applied over an underpainting to build up color gradually. |
| **Grisaille** | A monochrome painting technique using shades of gray, used as an underpainting foundation for oil glazing. |
| **Impasto** | A painting technique where pigment is applied thickly enough to stand up from the canvas surface, creating textured, opaque highlights. |
| **Imprimatura** | A tinted ground layer applied to the canvas before painting begins, establishing a color bias that shows through subsequent layers. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **LUT** | Look-Up Table; a fundamental FPGA logic resource used to implement combinational functions. |
| **Patina** | The gradual yellowing of linseed oil in old paintings, shifting color balance toward warm amber tones. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
