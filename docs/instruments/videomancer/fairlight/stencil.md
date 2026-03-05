---
draft: true
sidebar_position: 287
slug: /instruments/videomancer/stencil
title: "Stencil"
image: /img/instruments/videomancer/stencil/stencil_hero_s1.png
description: "Stencil converts the input video into a binary mask based on luminance threshold, then uses that mask to selectively reveal either a solid fill colour or the original image — creating bold, graphic compositions reminiscent of screen-printed posters and paper stencil art."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import stencil_control_panel from '/img/instruments/videomancer/stencil/stencil_control_panel.png';
import stencil_source1_sunset from '/img/instruments/videomancer/stencil/stencil_source1_sunset.png';
import stencil_source2_cat from '/img/instruments/videomancer/stencil/stencil_source2_cat.png';
import stencil_source3_clouds from '/img/instruments/videomancer/stencil/stencil_source3_clouds.png';
import stencil_source4_pattern from '/img/instruments/videomancer/stencil/stencil_source4_pattern.png';
import stencil_source5_girl from '/img/instruments/videomancer/stencil/stencil_source5_girl.png';
import stencil_source6_wood from '/img/instruments/videomancer/stencil/stencil_source6_wood.png';
import stencil_hero_s1 from '/img/instruments/videomancer/stencil/stencil_hero_s1.png';
import stencil_hero_s2 from '/img/instruments/videomancer/stencil/stencil_hero_s2.png';
import stencil_hero_s3 from '/img/instruments/videomancer/stencil/stencil_hero_s3.png';
import stencil_hero_s4 from '/img/instruments/videomancer/stencil/stencil_hero_s4.png';
import stencil_hero_s5 from '/img/instruments/videomancer/stencil/stencil_hero_s5.png';
import stencil_hero_s6 from '/img/instruments/videomancer/stencil/stencil_hero_s6.png';
import stencil_ex1_s1 from '/img/instruments/videomancer/stencil/stencil_ex1_s1.png';
import stencil_ex1_s2 from '/img/instruments/videomancer/stencil/stencil_ex1_s2.png';
import stencil_ex1_s3 from '/img/instruments/videomancer/stencil/stencil_ex1_s3.png';
import stencil_ex1_s4 from '/img/instruments/videomancer/stencil/stencil_ex1_s4.png';
import stencil_ex1_s5 from '/img/instruments/videomancer/stencil/stencil_ex1_s5.png';
import stencil_ex1_s6 from '/img/instruments/videomancer/stencil/stencil_ex1_s6.png';
import stencil_ex2_s1 from '/img/instruments/videomancer/stencil/stencil_ex2_s1.png';
import stencil_ex2_s2 from '/img/instruments/videomancer/stencil/stencil_ex2_s2.png';
import stencil_ex2_s3 from '/img/instruments/videomancer/stencil/stencil_ex2_s3.png';
import stencil_ex2_s4 from '/img/instruments/videomancer/stencil/stencil_ex2_s4.png';
import stencil_ex2_s5 from '/img/instruments/videomancer/stencil/stencil_ex2_s5.png';
import stencil_ex2_s6 from '/img/instruments/videomancer/stencil/stencil_ex2_s6.png';
import stencil_ex3_s1 from '/img/instruments/videomancer/stencil/stencil_ex3_s1.png';
import stencil_ex3_s2 from '/img/instruments/videomancer/stencil/stencil_ex3_s2.png';
import stencil_ex3_s3 from '/img/instruments/videomancer/stencil/stencil_ex3_s3.png';
import stencil_ex3_s4 from '/img/instruments/videomancer/stencil/stencil_ex3_s4.png';
import stencil_ex3_s5 from '/img/instruments/videomancer/stencil/stencil_ex3_s5.png';
import stencil_ex3_s6 from '/img/instruments/videomancer/stencil/stencil_ex3_s6.png';

# Stencil

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: stencil_source1_sunset, after: stencil_hero_s1 },
    { label: "Cat", before: stencil_source2_cat, after: stencil_hero_s2 },
    { label: "Clouds", before: stencil_source3_clouds, after: stencil_hero_s3 },
    { label: "Pattern", before: stencil_source4_pattern, after: stencil_hero_s4 },
    { label: "Girl", before: stencil_source5_girl, after: stencil_hero_s5 },
    { label: "Wood", before: stencil_source6_wood, after: stencil_hero_s6 },
  ]}
/>
*Hard-edged luminance masks carve vivid fill colours from the video stream, turning every frame into a cut-paper silhouette.*

---

## Overview

Stencil converts the input video into a binary mask based on luminance threshold, then uses that mask to selectively reveal either a solid fill colour or the original image — creating bold, graphic compositions reminiscent of screen-printed posters and paper stencil art. The two primary modes — Cut and Stamp — invert the relationship between mask and image: Cut reveals the fill colour where the mask is active (bright areas become solid colour), while Stamp reveals the original image through the mask (bright areas retain detail, dark areas become fill).

The pipeline operates entirely on the Y (luminance) channel for mask generation, but applies independently coloured fill and edge overlays in the UV domain using hue-to-UV conversion. An optional edge detector traces the boundary between masked and unmasked regions, outlining the stencil shape in a second independently coloured hue. Soft edge mode feathers the transition from hard binary to a smooth gradient proportional to the distance from the threshold, creating a more organic, airbrushed look.

The name references the physical stencil — a sheet with cut-out shapes through which ink or paint is applied. In traditional printmaking, the stencil defines hard boundaries between inked and un-inked areas. Stencil applies the same principle to video: the luminance threshold is the knife, the fill colour is the ink, and the live video is the paper beneath.

---

## Quick Start

1. **Start with contrast**: Feed Stencil a high-contrast source for the cleanest mask edges. Low-contrast material produces indistinct, noisy masks.
2. **Cut for graphics, Stamp for compositing**: Cut mode creates bold flat-colour graphics; Stamp mode retains video detail for overlay-style compositions.
3. **Edge adds dimension**: Even a thin edge outline (10–15%) adds visual definition to the stencil boundary, separating fill from image.

---

## Background

### Luminance Keying

Luminance keying (also called luma keying) is the foundation of Stencil's mask generation. Unlike chroma keying, which isolates colours, luma keying separates pixels based on brightness alone. The technique dates back to early television, where high-contrast title cards were shot against black backgrounds and keyed into the programme signal. Stencil generalises this by allowing the threshold to be set anywhere from 0 to 1023, turning any luminance boundary into a key edge.

### Screen Printing and Pochoir

The visual effect of Stencil directly parallels screen printing (serigraphy), where ink is forced through a mesh stencil onto the substrate. The pochoir technique, used extensively in Art Deco illustration, employed hand-cut metal stencils to apply flat areas of colour. Stencil's Cut mode mirrors pochoir: bright areas become flat ink, dark areas reveal the underlying surface. The Edge overlay adds a contour line similar to the registration marks used in multi-colour print passes.

### Edge Detection

Stencil's edge detector operates on the horizontal difference between adjacent mask values. When the binary mask transitions from 0 to 1 (or vice versa), the difference is non-zero, marking an edge pixel. The Edge Width parameter controls the thickness of this detection zone — wider values capture more gradual transitions, producing thicker outlines. This is a simplified form of the Sobel or Roberts cross operator, operating only in the horizontal direction for single-clock-cycle evaluation.

### Proc Amp Model

The final contrast and offset stage uses the standard proc_amp formula: `(Y − 512) × contrast / 512 + offset`. This centres the gain around the midpoint, allowing the contrast pot to expand or compress the tonal range symmetrically. The offset pot then shifts the entire result up or down, functioning as a brightness control. This two-stage adjustment after masking allows fine-tuning of the stencil output density without affecting the threshold or fill colours.

### Feathered Edges in Video Art

Hard binary masks produce the characteristic look of pop art and punk-era graphics — bold, uncompromising silhouettes. But video art often demands smoother transitions. Stencil's Soft Edge mode replaces the binary step function with a distance-based gradient: pixels near the threshold receive partial mask values proportional to their distance from the threshold boundary. This feathering technique is the same principle used in alpha channel anti-aliasing, applied here as a real-time luminance effect.


---

## Signal Flow

```
                              ┌────────────────────┐
data_in ─────────────────────►│ Stage 0: Extract Y  │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 1: Threshold  │
                              │ Y vs threshold →    │
                              │ binary mask +       │
                              │ soft distance       │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 2: Edge Detect│
                              │ horizontal diff of  │
                              │ mask values          │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 3: Mode Apply │
                              │ Cut: mask→fill      │
                              │ Stamp: mask→input   │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 4: Edge Overl.│
                              │ edge region →       │
                              │ edge_color          │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 5: Proc Amp   │
                              │ (Y-512)*con/512     │
                              │  + offset           │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 6: Invert+Mix │
                              └──────┬─────────────┘
                                     │
data_in ──► [sync delay] ──► dry ──► Interpolator ◄── wet
                                       (4 clk)
                                          │
                                          ▼
                                      data_out
```

The pipeline splits into two conceptual branches after Stage 1: the binary mask drives pattern placement (Stages 3–4), while the original Y value is consumed by the proc_amp stage (Stage 5) for final tonal adjustment. The edge detector in Stage 2 examines the mask itself — not the original luminance — so edge thickness is relative to the mask transition, not to the source brightness gradient. This means a slowly varying luminance ramp produces a thin edge, while a sharp brightness step produces a thick edge, which mirrors the physical stencil where a clean cut yields a sharp boundary.

The Fill Color and Edge Color pots generate UV pairs from hue angles (0–360°), creating fully saturated colour fills that replace the input chroma in masked or edge regions. The luminance of fill regions comes from the contrast/offset-adjusted Y, allowing the fill colour to retain tonal variation across the stencil.

---

## Parameter Reference

<img src={stencil_control_panel} alt="Videomancer front panel with Stencil loaded"/>
*Videomancer's front panel with Stencil active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At low values, only the darkest pixels fall below the threshold, so most of the image is masked. At high values, only the brightest pixels exceed the threshold, revealing only the highlights. The midpoint at 50% provides a balanced split for typical video content. The threshold operates on the raw Y channel before any contrast or offset processing, making it independent of the output tonal adjustments. Internally, sets the luminance threshold that divides the image into masked and unmasked regions.

---

#### Knob 2 — Mask Mode
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Controls the width of the edge detection zone around the mask boundary. At the minimum, edges are one pixel wide — a single-sample transition. Increasing the width broadens the detection region, producing thicker outlines that trace the stencil boundary. In Soft Edge mode, this parameter also influences the feathering gradient distance: wider edges produce a broader transition zone between fully masked and fully unmasked regions. At maximum, the edge can consume a significant portion of the image, creating bold graphic outlines.

---

#### Knob 3 — Process
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Selects the hue angle for the fill colour applied to masked regions. The pot sweeps through 360° of hue, converting the angle to U and V chrominance values at full saturation. At 0° the fill is red, 120° is green, and 240° is blue, with all intermediate hues available. The fill colour appears wherever the mask dictates — in Cut mode, this is where the source luminance exceeds the threshold; in Stamp mode, it fills the areas where luminance is below threshold.

---

#### Knob 4 — Tint Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Selects the hue angle for the edge outline colour, independently from the fill hue. This allows the edge contour to contrast with both the fill and the original image, creating a three-colour composition: original, fill, and edge. The initial value of 180° places the edge colour opposite the default fill hue on the colour wheel, providing natural contrast. The edge colour only appears when the Edge toggle is enabled.

---

#### Knob 5 — Chroma U
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Applies contrast scaling to the output luminance using the proc_amp formula. The Y channel is centred at 512, scaled by the contrast factor, then re-centred. At the initial midpoint value, contrast is unity (no change). Below midpoint, contrast is reduced, compressing the tonal range toward mid-gray. Above midpoint, contrast is increased, pushing whites brighter and blacks darker. This operates after the mask and edge stages, allowing separate control of the stencil's overall density.

---

#### Knob 6 — Chroma V
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Shifts the output brightness up or down after contrast scaling. At the midpoint, no offset is applied. Below midpoint, the image darkens; above, it brightens. Combined with contrast, this allows precise control of the stencil output density — for example, high contrast with low offset creates a dramatic, shadow-heavy poster look, while moderate contrast with high offset produces a washed-out, overexposed aesthetic.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Chain B** | Normal | Invert |
| **8 — Inv Mask** | Off | On |
| **9 — Luma Inv** | Off | On |
| **10 — ChromaKill** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles define the stencil's fundamental character. Mode (Cut/Stamp) determines what the mask reveals. Edge enables the contour outline. Soft chooses between hard binary and feathered transitions. Invert flips the final luminance. Bypass disables all processing. Together, Mode and Soft produce four distinct visual modes: hard cut, soft cut, hard stamp, and soft stamp — each with a fundamentally different look.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) and wet (processed) signal using three parallel interpolators. At 0% the output is the unmodified input; at 100% the output is the fully processed stencil effect. Intermediate values blend the stencil result with the original, useful for reducing the intensity of the effect or for creating semi-transparent overlay compositions where the stencil colour is visible but the original image shows through.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Stencil processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from basic threshold masking through coloured stencil compositions to edge-traced graphic overlays.

### Exercise 1: Basic Threshold Mask

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: stencil_source1_sunset, after: stencil_ex1_s1 },
    { label: "Cat", before: stencil_source2_cat, after: stencil_ex1_s2 },
    { label: "Clouds", before: stencil_source3_clouds, after: stencil_ex1_s3 },
    { label: "Pattern", before: stencil_source4_pattern, after: stencil_ex1_s4 },
    { label: "Girl", before: stencil_source5_girl, after: stencil_ex1_s5 },
    { label: "Wood", before: stencil_source6_wood, after: stencil_ex1_s6 },
  ]}
/>
*Basic Threshold Mask — simulated result across source images.*
**Source**: High-contrast footage — a face lit from one side, or text on a white background.

**What You'll Create**: Understand how the Threshold control divides the image into masked and unmasked regions in Cut mode.

1. **Set to Cut mode**: Ensure Mode is set to Cut.
2. **Sweep threshold**: Slowly increase Threshold from 0% to 100%. Watch the mask boundary move across the luminance range, progressively revealing more fill colour.
3. **Observe binary mask**: At around 50%, roughly half the image is fill colour and half is original video — a clear stencil effect.
4. **Invert for reverse**: Toggle Invert On. The stencil relationship flips — formerly bright areas are now dark.
5. **Compare**: Use Bypass to compare against the raw input.

**Key concepts**: Luminance threshold creates a binary mask that divides the image at a single brightness level, Cut mode replaces bright areas with fill colour, the threshold is independent of contrast/offset

---

### Exercise 2: Coloured Stencil with Edge

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: stencil_source1_sunset, after: stencil_ex2_s1 },
    { label: "Cat", before: stencil_source2_cat, after: stencil_ex2_s2 },
    { label: "Clouds", before: stencil_source3_clouds, after: stencil_ex2_s3 },
    { label: "Pattern", before: stencil_source4_pattern, after: stencil_ex2_s4 },
    { label: "Girl", before: stencil_source5_girl, after: stencil_ex2_s5 },
    { label: "Wood", before: stencil_source6_wood, after: stencil_ex2_s6 },
  ]}
/>
*Coloured Stencil with Edge — simulated result across source images.*
**Source**: Colourful scenery or abstract video — anything with a broad luminance range.

**What You'll Create**: Create a three-colour composition using fill, edge, and original image.

1. **Set threshold**: Threshold at about 45% to capture a broad stencil.
2. **Choose fill hue**: Set Fill Color to about 60° (yellow-green).
3. **Enable edge**: Toggle Edge On. A contour line appears around the stencil boundary.
4. **Set edge hue**: Set Edge Color to about 300° (magenta). The contour contrasts with the fill.
5. **Widen edge**: Increase Edge Width to about 40%. The contour thickens into a bold outline.
6. **Stamp mode**: Toggle Mode to Stamp. The relationship reverses — the original video now appears through the bright areas.
7. **Adjust contrast**: Increase Contrast to about 70% for a punchier look.

**Key concepts**: Fill and edge hues are independent, edge width controls contour thickness, Cut and Stamp invert the mask-to-image relationship, three-colour composition from two hue controls plus the source

---

### Exercise 3: Soft Stencil with Offset

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: stencil_source1_sunset, after: stencil_ex3_s1 },
    { label: "Cat", before: stencil_source2_cat, after: stencil_ex3_s2 },
    { label: "Clouds", before: stencil_source3_clouds, after: stencil_ex3_s3 },
    { label: "Pattern", before: stencil_source4_pattern, after: stencil_ex3_s4 },
    { label: "Girl", before: stencil_source5_girl, after: stencil_ex3_s5 },
    { label: "Wood", before: stencil_source6_wood, after: stencil_ex3_s6 },
  ]}
/>
*Soft Stencil with Offset — simulated result across source images.*
**Source**: A slowly-moving abstract video or camera feedback loop.

**What You'll Create**: Combine Soft edge mode with contrast and offset for a smooth, painterly stencil composition.

1. **Enable soft mode**: Toggle Soft to Soft. The stencil transitions become feathered gradients.
2. **Set threshold**: Around 55%.
3. **Choose fill hue**: Set Fill Color to about 200° (cyan-blue).
4. **Low contrast**: Set Contrast to about 30%. The tonal range compresses, softening the overall look.
5. **High offset**: Set Offset to about 70%. The image brightens, creating a washed, overexposed quality.
6. **Enable edge**: Toggle Edge On with Edge Width at about 25%. The edge appears as a soft halo rather than a hard line.
7. **Reduce mix**: Set Mix to about 75% to show the original image through the soft stencil.

**Key concepts**: Soft mode creates feathered transitions proportional to distance from threshold, low contrast + high offset produces a washed look, soft edge produces a halo effect, mix blending integrates the stencil with the original

---


## Tips

- **Complementary hues**: Set Fill and Edge colours 180° apart on the colour wheel for maximum visual contrast in the contour.
- **Soft mode for organic looks**: Feathered transitions suit organic footage (faces, nature) better than hard binary masks.
- **Use Offset to lighten fills**: Increasing Offset brightens the fill region, creating pastel tones instead of deep saturated colours.
- **Invert for reverse-out**: Invert + high threshold creates bright shapes on a dark field — useful for title card compositions.
- **Mix for subtlety**: Blend at 60–80% for a look where the stencil colour tints the image rather than replacing it.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha channel** | A per-pixel transparency value used in digital compositing to blend layers; related to Stencil's soft mask gradient. |
| **Binary mask** | A per-pixel map containing only two values (0 or 1), used to select between two signal sources at each pixel. |
| **BT.601** | The ITU-R standard defining the YUV colour encoding used in standard-definition video and as the native colour space in Videomancer. |
| **Feathering** | Gradually blending the edge of a mask from fully opaque to fully transparent, creating a smooth transition rather than a hard step. |
| **Hue** | The attribute of colour that determines its position on the colour wheel, measured in degrees from 0° (red) through 120° (green) to 240° (blue). |
| **Luma keying** | A compositing technique that generates a matte (mask) from the brightness of the source signal rather than its colour. |
| **Pochoir** | An Art Deco illustration technique using hand-cut metal stencils to apply flat areas of colour through the openings. |
| **Screen printing** | A printing technique where ink is forced through a mesh stencil onto the substrate, producing flat areas of solid colour. |
| **Serigraphy** | The fine-art term for screen printing, especially when used for artistic rather than commercial reproduction. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
