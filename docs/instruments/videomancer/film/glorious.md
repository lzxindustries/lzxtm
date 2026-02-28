---
draft: true
sidebar_position: 113
slug: /instruments/videomancer/glorious
title: "Glorious"
image: /img/instruments/videomancer/glorious/glorious_hero.png
description: "Program guide for Glorious, a Videomancer film program for the LZX video synthesizer."
---

import glorious_hero from '/img/instruments/videomancer/glorious/glorious_hero.png';
import glorious_before_after from '/img/instruments/videomancer/glorious/glorious_before_after.png';
import glorious_control_panel from '/img/instruments/videomancer/glorious/glorious_control_panel.png';
import glorious_exercise1_result from '/img/instruments/videomancer/glorious/glorious_exercise1_result.png';
import glorious_exercise2_result from '/img/instruments/videomancer/glorious/glorious_exercise2_result.png';
import glorious_exercise3_result from '/img/instruments/videomancer/glorious/glorious_exercise3_result.png';

# Glorious

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={glorious_hero} alt="Glorious hero image"/>
*Glorious applying three-strip Technicolor dye transfer simulation with per-channel exposure, H&D S-curve response, and fringe misregistration to a studio portrait.*
<img src={glorious_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Glorious applied.*

---

## Overview

Glorious recreates the look of **Technicolor Process 4** — the three-strip dye transfer printing system that defined the color aesthetic of Hollywood cinema from the 1930s through the 1960s. The program converts the input video from YUV to RGB, processes each color channel as an independent film strip with its own exposure and tonal response curve, simulates the mechanical imprecision of dye alignment between strips, adds inter-channel dye contamination, and converts back to YUV. The entire pipeline runs in the RGB domain, where each channel can be treated as a separate photographic negative.

The name *Glorious* is a nod to the marketing language of the Technicolor era — films were advertised as being photographed "in Glorious Technicolor." The program captures not just the idealized color science but the physical imperfections of the process: the slight misregistration between color records (fringe), the dye bleeding between adjacent strips (matrix bleed), and the characteristic S-shaped density response of photographic film stock (the Hurter–Driffield curve).

At conservative settings — balanced exposure, moderate contrast, zero fringe — Glorious produces a warm, saturated film-like grade with gently compressed shadows and highlights. At extreme settings — heavy red exposure, maximum fringe, high bleed with aging enabled — it produces the faded, cyan-shifted look of a deteriorating vintage Technicolor print.

---

## Background

### The Three-Strip Technicolor Process

From 1932 to 1955, Technicolor cameras used a beam-splitting prism to expose three strips of black-and-white film simultaneously through red, green, and blue filters. Each strip captured one color record of the scene. In the printing lab, complementary dye matrices (cyan from the red record, magenta from the green record, yellow from the blue record) were transferred onto a single blank film strip in a process called **imbibition printing** — dye soaked into gelatin relief matrices was pressed onto the final print. The result was a color image built from three overlapping dye layers. Glorious models this separation-and-recombination pipeline digitally.

### Hurter–Driffield Response Curves

Every photographic film stock has a characteristic relationship between the amount of light it receives (exposure) and the optical density of the developed image. This relationship, plotted on a graph, is called the **Hurter–Driffield (H&D) curve** — named after the Swiss-born photochemists Ferdinand Hurter and Vero Charles Driffield who first systematized the measurement in 1890. The curve has three regions: the **toe** (shadow compression, where low exposures produce little density change), the **straight section** (a linear relationship between exposure and density), and the **shoulder** (highlight compression, where high exposures saturate the film). Glorious implements a piecewise approximation of this S-curve, with the Contrast control widening or narrowing the straight section.

### Dye Registration and Fringe

In the imbibition printing process, three separate dye matrices were pressed onto the final print in sequence. If any matrix was slightly misaligned — even by a fraction of a millimeter — the corresponding color record would be horizontally shifted relative to the others. This misalignment is called **dye registration error** and produces visible colored fringes along high-contrast edges: a red halo on one side and a cyan halo on the other. Glorious models this by passing the red and blue channels through horizontal shift registers of configurable depth (0–7 pixels), with the green channel held as the undelayed reference. Red is shifted forward and blue backward, creating the characteristic opposing color fringes.

### Matrix Bleed and Dye Contamination

Even with perfect registration, the imbibition process allowed some dye to migrate between adjacent layers. **Matrix bleed** describes this inter-channel contamination: some cyan dye bleeds into the magenta layer, some magenta into the yellow, and so on. The result is a subtle desaturation and color crosstalk that distinguishes Technicolor prints from modern digital color. Glorious implements a 4-bit crosstalk matrix where each channel receives a weighted fraction of the other two channels, with the bleed amount globally controlled. The asymmetric weighting (green receives less crosstalk than red or blue) matches the physical reality that the middle dye layer was sandwiched between the other two.

### Film Aging and Magenta Fade

Technicolor prints stored in non-ideal conditions undergo differential dye fading. The cyan dye (derived from the red record) is typically the most stable, while the magenta and yellow dyes fade faster. As a result, aged Technicolor prints develop a characteristic **cyan-green color shift** — shadows that were once neutral drift toward teal, and skin tones lose their warmth. Glorious simulates this by halving the red channel when the Film Fade toggle is set to Aged, which shifts the overall color balance toward cyan.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── All Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. YUV → RGB              (matrix multiply: BT.601 inverse)
│   ├─ 2. Strip Exposure          (per-channel 5-bit gain: R, G=avg, B)
│   ├─ 3. H&D Film Curve          (piecewise S-curve: toe, straight, shoulder)
│   ├─ 4. Fringe                  (R/B shift registers ±0–7 px vs G reference)
│   ├─ 5. Matrix Bleed            (4-bit inter-channel crosstalk)
│   ├─ 6. RGB → YUV              (matrix multiply: BT.601 forward)
│   │      └─ Mono Separation     (optional: zero chroma, Y = G channel)
│   ├─ 7. Saturation Boost        (4-bit multiply on U/V)
│   └─ 8. Inline Mix              (4-bit alpha dry/wet blend)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delayed by 10 clocks
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The entire signal processing chain operates in the RGB domain. The input YUV signal is converted to RGB at Stage 1, processed through four RGB stages (exposure, H&D curve, fringe, bleed), and then converted back to YUV at Stage 6. This RGB-domain processing is essential because the Technicolor process operates on independent color separations — each strip is a separate film negative with its own exposure and response. The green channel's exposure is automatically derived as the average of red and blue exposure settings, matching the Technicolor convention where the green record's printer light was held as the reference. The fringe stage uses separate 8-deep shift register pipelines for red and blue, with green undelayed, so the horizontal misregistration is always measured relative to the green record. The inline 4-bit mix replaces the usual interpolator_u entities, providing a slightly coarser but resource-efficient dry/wet blend.

---

## Parameter Reference

<img src={glorious_control_panel} alt="Videomancer front panel with Glorious loaded"/>
*Videomancer's front panel with Glorious active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Red Exp
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the red strip exposure — analogous to the red **printer light** intensity in a Technicolor lab. The 10-bit register value is reduced to a 5-bit multiplier (0–31), with unity gain at approximately the midpoint (multiplier = 16). Increasing the red exposure brightens the red channel, producing warmer skin tones and richer reds. Decreasing it shifts the image toward cyan (the complement of red). This control works independently of the blue exposure, allowing differential color grading of the warm and cool axes of the image.

---

#### Knob 2 — Blue Exp
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the blue strip exposure, matching the Red Exp control but for the blue channel. Increasing blue exposure produces cooler shadows and more vivid blues. Decreasing it shifts the image toward yellow. The green channel's exposure is automatically computed as the average of the red and blue exposure values, so adjusting either the red or blue exposure also affects green — just as a Technicolor timer would adjust all three printer lights together to maintain overall density.

---

#### Knob 3 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the steepness of the H&D response curve. At the midpoint, the toe and shoulder thresholds sit at comfortable positions, producing a gentle S-curve. Increasing contrast widens the straight section (pushing the toe and shoulder thresholds further apart), which steepens the overall response and increases tonal contrast. Decreasing it narrows the straight section, creating a flatter, more compressed tonal response. The toe and shoulder always apply symmetrically — shadows compress and highlights compress by the same proportion.

---

#### Knob 4 — Fringe
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 1 |

Controls the amount of dye registration misalignment between color strips. The 10-bit register value is quantized to a 3-bit integer (0–7) extracted from the upper three bits, representing the number of pixel positions the red and blue channels are shifted relative to green. At zero, all three channels are perfectly aligned. At higher values, red shifts forward and blue shifts backward by the selected number of pixels, creating increasingly visible colored fringes along high-contrast edges. In single-strip era mode, the fringe amount is automatically halved.

---

#### Knob 5 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 150.1% |
| Suffix | % |

Controls the saturation boost applied after the RGB-to-YUV conversion. The 10-bit register is reduced to a 4-bit multiplier applied to the U and V chroma channels. At the default position (approximately 75% of range), saturation is moderately boosted beyond unity, emulating the vivid, slightly oversaturated look of fresh Technicolor prints. At the midpoint, saturation is approximately unity. At maximum, the boost approaches 2×, producing intensely saturated colors that can clip.

---

#### Knob 6 — Matrix Bleed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the amount of inter-channel dye contamination. A 4-bit bleed coefficient determines how much of each channel leaks into the other two. At zero, the channels are perfectly isolated. As you increase Matrix Bleed, red receives green and blue contamination, green receives red and blue, and blue receives red and green — with an asymmetric weighting that matches the physical dye sandwich (green receives half the crosstalk that red and blue receive). The result is a progressive softening and desaturation of color, mimicking the dye migration of a real imbibition print.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Era** | 3-Strip | 1-Strip |
| **8 — Toe Lift** | Crushed | Lifted |
| **9 — Mono Sep** | Color | Mono |
| **10 — Film Fade** | Fresh | Aged |
| **11 — Bypass** | Off | On |

The five toggles control independent aspects of the Technicolor simulation. Era selects between the classic three-strip process and the later single-strip monopack (which reduces fringe). Toe Lift adjusts the shadow response of the H&D curve. Mono Sep isolates the green separation record. Film Fade simulates print aging. Bypass routes the input signal directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet blend between the Technicolor-processed signal and the original input. The mix uses an inline 4-bit alpha implementation (16 steps of blending precision) rather than the interpolator_u entities used by most programs. At maximum (default), the output is fully the Technicolor-graded signal. At zero, the output is the unprocessed input. Intermediate positions blend between the two, useful for dialing in subtle film-look enhancements without committing to the full effect.

---

## Guided Exercises

These exercises progress from basic exposure grading to full vintage Technicolor simulation, building familiarity with each stage of the film emulation pipeline.

### Exercise 1: Strip Exposure Color Grading

<img src={glorious_exercise1_result} alt="Strip Exposure Color Grading result"/>
*Strip Exposure Color Grading — simulated result across source images.*
**Source**: A camera feed or recorded footage with recognizable skin tones and a mix of warm and cool colors.

**Objective**: Learn how the independent red and blue exposure controls affect overall color balance, and observe the automatic green tracking.

1. **Default balance**: Leave both Red Exp and Blue Exp at their default midpoint. The image should appear neutral with moderate film-like warmth.
2. **Warm shift**: Increase Red Exp to about 75%. Skin tones warm visibly, reds intensify, and the overall image takes on an amber cast.
3. **Cool shift**: Return Red Exp to center and increase Blue Exp to about 75%. The image cools — shadows shift toward blue, highlights toward ice-white.
4. **Cross-process**: Set Red Exp to about 80% and Blue Exp to about 20%. The green auto-exposure (average of red and blue) sits at the midpoint. The result is a split-toned image: warm highlights, neutral shadows.
5. **Observe green tracking**: Note how the overall brightness tracks the average of red and blue — the green channel is never directly controlled.

**Key concepts**: Per-channel exposure as printer light control, automatic green derivation, differential color grading

---

### Exercise 2: H&D Curve and Fringe

<img src={glorious_exercise2_result} alt="H&D Curve and Fringe result"/>
*H&D Curve and Fringe — simulated result across source images.*
**Source**: Footage with strong contrast — backlit subjects, bright windows, or text on dark backgrounds.

**Objective**: Explore how the H&D tonal response and fringe misregistration interact to create the characteristic Technicolor look.

1. **Flat response**: Set Contrast to about 20%. The image appears flat with compressed shadows and highlights — everything sits in the midtones.
2. **Steep S-curve**: Increase Contrast to about 80%. Shadows crush deeper, highlights clip earlier, and the straight section steepens. High-contrast edges become more defined.
3. **Toe lift**: Toggle Toe Lift to Lifted. The deepest shadows rise to a dark gray, revealing detail that was crushed. This emulates a slightly fogged print.
4. **Add fringe**: Increase Fringe to about 4 (step 4 of 8). Colored halos appear along high-contrast edges — red on one side, cyan on the other. The effect is most visible where dark and light regions meet.
5. **Maximum fringe**: Increase Fringe to 7. The color separation is now dramatic and visually dominant, as if the dye matrices were badly misaligned.
6. **Single-strip**: Switch Era to 1-Strip. The fringe amount halves automatically, producing a subtler misregistration.

**Key concepts**: Piecewise S-curve response, toe/straight/shoulder regions, dye registration misalignment, era-dependent fringe scaling

---

### Exercise 3: Vintage Aged Print

<img src={glorious_exercise3_result} alt="Vintage Aged Print result"/>
*Vintage Aged Print — simulated result across source images.*
**Source**: Any footage — the aging effect transforms the entire tonal palette.

**Objective**: Combine all processing stages to create the look of a deteriorating vintage Technicolor print.

1. **Base grade**: Set Red Exp ~60%, Blue Exp ~50%, Contrast ~65%.
2. **Add fringe**: Set Fringe to about 3 for moderate misregistration.
3. **Increase bleed**: Set Matrix Bleed to about 40%. Colors soften and desaturate as inter-channel contamination increases.
4. **Boost saturation**: Increase Saturation to about 85% to compensate for the desaturation caused by bleed, producing the slightly garish quality of a well-used print.
5. **Enable aging**: Switch Film Fade to Aged. The image shifts toward cyan-green as the red channel fades. Skin tones lose warmth and shadows develop a teal cast.
6. **Lift toe**: Enable Toe Lift. The combination of lifted shadows and faded red creates the characteristic look of a print pulled from a poorly maintained archive.
7. **Dial mix**: Lower Mix to about 70% to blend the aged look with the clean original, producing a subtle vintage treatment rather than a full period recreation.

**Key concepts**: Layered film simulation (exposure + curve + fringe + bleed + fade), differential dye fading, compensating bleed with saturation

---


## Tips

- **Processing order matters**: YUV→RGB → exposure → H&D curve → fringe → bleed → RGB→YUV → saturation → mix. Exposure happens before the curve, so heavy exposure pushes values into the toe and shoulder regions of the H&D curve.
- **Green is automatic**: The green channel's exposure is always the average of red and blue. To independently control green, adjust both red and blue equally and use the Saturation control to fine-tune color intensity.
- **Fringe creates period-accurate imperfection**: Even 1–2 pixels of fringe adds a subtle organic quality that instantly separates digital video from its Technicolor-era inspiration. Maximum fringe is intentionally extreme — dial it back for realism.
- **Bleed and saturation compensate each other**: Increasing Matrix Bleed desaturates because crosstalk pushes all channels toward the same average value. Increasing Saturation after bleed restores color intensity while keeping the soft, dye-like quality.
- **Film Fade for vintage looks**: Combining Film Fade (Aged) with Toe Lift (Lifted) and moderate bleed produces the look of a faded 1950s release print — cyan-shifted, low contrast, with milky shadows.
- **Mono Sep for B&W reference**: Switching to Mono shows the green separation record, which was the sharpest and most detailed. Use it to evaluate the tonal quality of the H&D curve without color distractions.
- **Feedback loops**: Routing the output back to the input creates recursive film grading — each pass adds another layer of exposure, curve, and bleed, compounding the Technicolor look until it clips to saturated primary blocks.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed signal for before/after comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation BT.601; the standard defining the YUV-to-RGB matrix coefficients used in standard-definition video, also used here for HD. |
| **Dye Transfer** | The imbibition printing process in which dye from a relief matrix is transferred onto a receiving film strip. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Fringe** | Horizontal color offset caused by misalignment of separate dye layers during printing; produces colored halos at high-contrast edges. |
| **H&D Curve** | Hurter–Driffield curve; the S-shaped relationship between photographic exposure and resulting optical density, with toe, straight, and shoulder regions. |
| **Imbibition** | A printing technique where dye soaks from a gelatin relief matrix into a receiving layer; the method used in Technicolor Process 4. |
| **Matrix Bleed** | Inter-channel dye contamination where one color layer's dye migrates into adjacent layers, producing color crosstalk. |
| **Mono Separation** | Isolating a single color record (here, the green channel) to produce a monochrome image representing one strip of the three-strip process. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Printer Light** | In photochemical film timing, the intensity of light used to expose each color record during printing; higher intensity increases that channel's density. |
| **Saturation** | The intensity of color in an image; higher saturation produces more vivid colors, lower saturation tends toward gray. |
| **Shoulder** | The high-exposure region of the H&D curve where density increase diminishes — represents highlight compression. |
| **Technicolor Process 4** | The three-strip camera and dye-transfer printing system used from 1932–1955, defining the "Technicolor look." |
| **Toe** | The low-exposure region of the H&D curve where density increase is minimal — represents shadow compression. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
