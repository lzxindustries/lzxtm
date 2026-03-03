---
draft: true
sidebar_position: 198
slug: /instruments/videomancer/morpho
title: "Morpho"
image: /img/instruments/videomancer/morpho/morpho_hero_s1.png
description: "Mathematical morphology is a branch of image processing based on set theory — it treats images as collections of shapes and applies operations that expand, shrink, or extract boundaries."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import morpho_control_panel from '/img/instruments/videomancer/morpho/morpho_control_panel.png';
import morpho_source1_car from '/img/instruments/videomancer/morpho/morpho_source1_car.png';
import morpho_source2_sunset from '/img/instruments/videomancer/morpho/morpho_source2_sunset.png';
import morpho_source3_elephant from '/img/instruments/videomancer/morpho/morpho_source3_elephant.png';
import morpho_source4_pattern from '/img/instruments/videomancer/morpho/morpho_source4_pattern.png';
import morpho_source5_boy from '/img/instruments/videomancer/morpho/morpho_source5_boy.png';
import morpho_source6_berries from '/img/instruments/videomancer/morpho/morpho_source6_berries.png';
import morpho_hero_s1 from '/img/instruments/videomancer/morpho/morpho_hero_s1.png';
import morpho_hero_s2 from '/img/instruments/videomancer/morpho/morpho_hero_s2.png';
import morpho_hero_s3 from '/img/instruments/videomancer/morpho/morpho_hero_s3.png';
import morpho_hero_s4 from '/img/instruments/videomancer/morpho/morpho_hero_s4.png';
import morpho_hero_s5 from '/img/instruments/videomancer/morpho/morpho_hero_s5.png';
import morpho_hero_s6 from '/img/instruments/videomancer/morpho/morpho_hero_s6.png';
import morpho_ex1_s1 from '/img/instruments/videomancer/morpho/morpho_ex1_s1.png';
import morpho_ex1_s2 from '/img/instruments/videomancer/morpho/morpho_ex1_s2.png';
import morpho_ex1_s3 from '/img/instruments/videomancer/morpho/morpho_ex1_s3.png';
import morpho_ex1_s4 from '/img/instruments/videomancer/morpho/morpho_ex1_s4.png';
import morpho_ex1_s5 from '/img/instruments/videomancer/morpho/morpho_ex1_s5.png';
import morpho_ex1_s6 from '/img/instruments/videomancer/morpho/morpho_ex1_s6.png';
import morpho_ex2_s1 from '/img/instruments/videomancer/morpho/morpho_ex2_s1.png';
import morpho_ex2_s2 from '/img/instruments/videomancer/morpho/morpho_ex2_s2.png';
import morpho_ex2_s3 from '/img/instruments/videomancer/morpho/morpho_ex2_s3.png';
import morpho_ex2_s4 from '/img/instruments/videomancer/morpho/morpho_ex2_s4.png';
import morpho_ex2_s5 from '/img/instruments/videomancer/morpho/morpho_ex2_s5.png';
import morpho_ex2_s6 from '/img/instruments/videomancer/morpho/morpho_ex2_s6.png';
import morpho_ex3_s1 from '/img/instruments/videomancer/morpho/morpho_ex3_s1.png';
import morpho_ex3_s2 from '/img/instruments/videomancer/morpho/morpho_ex3_s2.png';
import morpho_ex3_s3 from '/img/instruments/videomancer/morpho/morpho_ex3_s3.png';
import morpho_ex3_s4 from '/img/instruments/videomancer/morpho/morpho_ex3_s4.png';
import morpho_ex3_s5 from '/img/instruments/videomancer/morpho/morpho_ex3_s5.png';
import morpho_ex3_s6 from '/img/instruments/videomancer/morpho/morpho_ex3_s6.png';

# Morpho

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Car", before: morpho_source1_car, after: morpho_hero_s1 },
    { label: "Sunset", before: morpho_source2_sunset, after: morpho_hero_s2 },
    { label: "Elephant", before: morpho_source3_elephant, after: morpho_hero_s3 },
    { label: "Pattern", before: morpho_source4_pattern, after: morpho_hero_s4 },
    { label: "Boy", before: morpho_source5_boy, after: morpho_hero_s5 },
    { label: "Berries", before: morpho_source6_berries, after: morpho_hero_s6 },
  ]}
/>
*Morpho applying 3-tap horizontal erosion, dilation, and morphological gradient operations to extract and transform edge structures in the video signal.*

---

## Overview

**Mathematical morphology** is a branch of image processing based on set theory — it treats images as collections of shapes and applies operations that expand, shrink, or extract boundaries. The two fundamental operations are **erosion** (which shrinks bright regions and widens dark regions) and **dilation** (which expands bright regions and fills dark gaps). From these two primitives, a rich set of derived operations emerges: **gradient** (dilation minus erosion, revealing edges), **opening** (erosion followed by dilation, smoothing without expanding), and **closing** (dilation followed by erosion, filling gaps without shrinking).

Morpho implements the erosion and dilation primitives using a 3-pixel horizontal sliding window. The structuring element — the shape that defines the neighborhood — is either a cross (3 horizontal pixels) or a full square (the same 3 pixels — since only one line is buffered, the vertical extent is limited). On every pixel, the algorithm computes the local minimum (erosion) and local maximum (dilation) across the 3-tap window. The operation selector chooses which result to output. The gradient operation computes the difference between max and min, extracting horizontal edge information.

Because Morpho operates on a 1D (horizontal) kernel without vertical line buffers, it is a pure **horizontal morphology** operator. The effects are most visible along vertical edges in the source image, where the horizontal kernel crosses brightness transitions. Despite this limitation, the program produces striking edge-detection and structural effects when combined with contrast, threshold, and edge gain controls.

---

## Background

### What Are Erosion and Dilation?

**Erosion** replaces each pixel with the minimum value in its neighborhood. Bright features smaller than the structuring element disappear, and dark regions expand. The effect is like acid eating away at the edges of bright objects. **Dilation** is the dual operation — it replaces each pixel with the maximum in its neighborhood. Dark features smaller than the structuring element disappear, and bright regions expand. The effect is like spreading paint outward from bright edges. Together, erosion and dilation form the foundation of mathematical morphology.

### What Is a Morphological Gradient?

The **morphological gradient** is the difference between dilation and erosion: `gradient(x) = dilate(x) − erode(x)`. This quantity is zero in flat regions (where the local max equals the local min) and large at edges (where the max and min differ significantly). The result is an edge-detection map that highlights boundaries proportional to the local contrast. Unlike differential edge detectors (Sobel, Prewitt), the morphological gradient is inherently non-negative and bounded, making it well-suited for direct video display.

### What Is a Structuring Element?

The **structuring element** defines the shape and size of the neighborhood used for morphological operations. Common shapes include crosses, squares, disks, and lines. Morpho offers two choices: a horizontal cross (3 adjacent pixels on the same scanline) and a square (which, given the 1D implementation, functions identically). The structuring element determines which features the operation affects — smaller elements detect finer detail, larger elements affect broader structures.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel (or All Channels) ────────────────────────────────
│   │
│   ├─ 1. 3-Pixel Shift Register  (prev, curr, next)
│   ├─ 2. min3 / max3             (local minimum and maximum)
│   ├─ 3. Operation Select         (erode / dilate / gradient / open)
│   ├─ 4. Edge Gain               (scale gradient output)
│   ├─ 5. Threshold               (clip low values to zero)
│   ├─ 6. Contrast                (gain around midpoint)
│   └─ 7. Brightness              (DC offset)
│
├── UV Channels (Luma mode) ────────────────────────────────────
│   └─ Pass-through (original chroma preserved)
│
├── UV Channels (All mode) ─────────────────────────────────────
│   └─ Same morphological processing as Y
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The 3-pixel shift register is the core of the operation — it maintains three consecutive horizontal pixels and feeds them to the min3 and max3 functions simultaneously. The operation selector then chooses which result to output: erosion (min3 result), dilation (max3 result), gradient (max3 − min3 scaled by edge gain), or open (an approximation using only the min3 result). The Channel switch determines whether the morphological operation is applied only to Y (preserving original chroma) or to all three YUV channels independently.

---

## Parameter Reference

<img src={morpho_control_panel} alt="Videomancer front panel with Morpho loaded"/>
*Videomancer's front panel with Morpho active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Erode Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the erosion amount — how strongly the min3 result influences the output when the Erode operation is selected. At center, the erosion passes at unity (full local minimum replacement). Below center, the erosion effect is blended with the original signal. Above center, the erosion is exaggerated, further darkening eroded regions. In gradient mode, this control modulates the erosion component of the difference.

---

#### Knob 2 — Dilate Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the dilation amount — how strongly the max3 result influences the output when the Dilate operation is selected. Functions symmetrically to the Erode Amt control but for the maximum operation. Higher values create stronger dilation (brighter expansion). In gradient mode, this modulates the dilation component.

---

#### Knob 3 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets a minimum brightness threshold below which the processed output is forced to zero (black). At 0%, no thresholding — the full range passes through. As Threshold increases, progressively brighter values are cut, leaving only the strongest features. This is particularly effective in gradient mode, where it removes weak edges and leaves only strong boundaries.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies gain around the midpoint (512) to the morphologically processed signal. Values above center increase contrast, making the morphological features more defined. Values below center compress the tonal range. This control shapes the visual weight of the eroded, dilated, or gradient features.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC offset to the output luminance after all morphological processing. At center, no offset. Above center, the image brightens. Below center, it darkens.

---

#### Knob 6 — Edge Gain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scales the morphological gradient output. At center, the gradient (max − min) passes at unity. Above center, the edge signal is amplified, making edges brighter and more prominent. Below center, the edge signal is attenuated. This control is most relevant when the Gradient operation is selected and has minimal effect in pure erode/dilate modes.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Operation** | Erode | Dilate |
| **8 — Channel** | Luma | All |
| **9 — Struct Elm** | Cross | Square |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control the morphological operation and processing scope. Operation selects the morphological function. Channel determines whether morphology is applied to Y only or all channels. Struct Elm chooses the neighborhood shape. Invert reverses the luminance polarity. Bypass enables comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the morphologically processed output and the original input. At 100%, the full morphological result passes. Lowering the fader blends the original back in. At 0%, the output is the unprocessed input.

---

## Guided Exercises

These exercises progress from basic erosion/dilation to morphological gradient edge detection and creative structural effects.

### Exercise 1: Erosion and Dilation

<BeforeAfterSlider
  sources={[
    { label: "Car", before: morpho_source1_car, after: morpho_ex1_s1 },
    { label: "Sunset", before: morpho_source2_sunset, after: morpho_ex1_s2 },
    { label: "Elephant", before: morpho_source3_elephant, after: morpho_ex1_s3 },
    { label: "Pattern", before: morpho_source4_pattern, after: morpho_ex1_s4 },
    { label: "Boy", before: morpho_source5_boy, after: morpho_ex1_s5 },
    { label: "Berries", before: morpho_source6_berries, after: morpho_ex1_s6 },
  ]}
/>
*Erosion and Dilation — simulated result across source images.*
**Source**: High-contrast footage with clear edges — text, graphic elements, or architectural subjects.

**Objective**: Understand the fundamental erosion and dilation operations and how they reshape image features.

1. **Erode**: Set Operation to Erode (Switch 7). Observe how bright features shrink horizontally — text becomes thinner, bright lines narrow. Dark regions expand.
2. **Dilate**: Switch Operation to Dilate. Observe the opposite effect — bright features expand, dark lines fill, and small dark details disappear.
3. **Compare**: Toggle between Erode and Dilate using Switch 7. Notice how they are symmetrically opposite operations.
4. **Amount control**: With Erode selected, sweep Erode Amt and observe how the erosion intensity varies.
5. **All channels**: Switch Channel to All mode (Switch 8). The erosion/dilation now affects color as well — edges show color bleeding effects.

**Key concepts**: Erosion replaces with local minimum (shrinks bright), dilation replaces with local maximum (expands bright), they are dual operations

---

### Exercise 2: Morphological Gradient (Edge Detection)

<BeforeAfterSlider
  sources={[
    { label: "Car", before: morpho_source1_car, after: morpho_ex2_s1 },
    { label: "Sunset", before: morpho_source2_sunset, after: morpho_ex2_s2 },
    { label: "Elephant", before: morpho_source3_elephant, after: morpho_ex2_s3 },
    { label: "Pattern", before: morpho_source4_pattern, after: morpho_ex2_s4 },
    { label: "Boy", before: morpho_source5_boy, after: morpho_ex2_s5 },
    { label: "Berries", before: morpho_source6_berries, after: morpho_ex2_s6 },
  ]}
/>
*Morphological Gradient (Edge Detection) — simulated result across source images.*
**Source**: Footage with distinct objects and clear boundaries — outdoor scenes, product shots, or geometric patterns.

**Objective**: Use the morphological gradient to extract edge information from the image.

1. **Select gradient**: Set Operation to Gradient (Switch 7). The output shows edges as bright lines on a dark background.
2. **Edge gain**: Increase Edge Gain to amplify the edge signal. The edges become brighter and more visible.
3. **Threshold clean**: Increase Threshold to remove weak edges and noise, leaving only strong boundaries.
4. **Contrast**: Push Contrast to ~70% to sharpen the edge map.
5. **Invert**: Toggle Invert (Switch 10). The edge map becomes dark lines on a bright background — a line-drawing effect.
6. **Color edges**: Switch Channel to All mode. The gradient now shows color differences at edges, producing rainbow-fringed edge detection.

**Key concepts**: Gradient = dilation − erosion, reveals edges proportional to local contrast, threshold removes weak edges, edge gain amplifies the detection

---

### Exercise 3: Creative Structural Effects

<BeforeAfterSlider
  sources={[
    { label: "Car", before: morpho_source1_car, after: morpho_ex3_s1 },
    { label: "Sunset", before: morpho_source2_sunset, after: morpho_ex3_s2 },
    { label: "Elephant", before: morpho_source3_elephant, after: morpho_ex3_s3 },
    { label: "Pattern", before: morpho_source4_pattern, after: morpho_ex3_s4 },
    { label: "Boy", before: morpho_source5_boy, after: morpho_ex3_s5 },
    { label: "Berries", before: morpho_source6_berries, after: morpho_ex3_s6 },
  ]}
/>
*Creative Structural Effects — simulated result across source images.*
**Source**: Abstract or textured footage — flowing water, smoke, foliage, or video feedback.

**Objective**: Combine morphological operations with contrast and inversion for creative visual effects.

1. **Strong erosion**: Set Operation to Erode, Erode Amt to ~80%, Contrast to ~80%. The image reduces to its darkest structures.
2. **All channels**: Switch to All mode. Color channels erode independently, creating color fringing.
3. **Invert**: Enable Invert. The eroded negative creates a bold, high-contrast graphic.
4. **Threshold sculpting**: Increase Threshold to ~40%. Only the strongest dark structures survive the erosion.
5. **Mix blend**: Lower Mix to ~50%. The eroded structure overlays the original, creating a combined texture.
6. **Open mode**: Switch to Open (Switch 7, 4th position). This smooths fine detail while preserving larger structures.

**Key concepts**: Morphological operations reshape image structure, all-channel mode creates color effects, inversion reveals complementary structure, open mode smooths noise

---


## Tips

- **Gradient for edge detection**: Morphological gradient is one of the cleanest edge detectors — non-negative, bounded, and noise-resistant.
- **Threshold cleans noise**: In gradient mode, threshold removes weak micro-edges caused by noise, leaving only meaningful boundaries.
- **Edge Gain amplifies subtlety**: Low-contrast edges can be brought out by increasing Edge Gain without affecting flat regions.
- **All-channel mode for color**: Applying morphology to UV channels creates color bleeding and fringing effects that can be striking on graphic input.
- **Erosion for dark structures**: Erosion reveals the dark skeleton of an image — the network of dark lines and shadows.
- **Dilation for glow**: Dilation spreads bright regions, creating a blooming glow effect on highlights.
- **Mix for overlay**: Use 40–60% Mix to overlay the morphological result on the original, combining edge structure with source detail.

---

## Glossary

| Term | Definition |
|------|------------|
| **Dilation** | A morphological operation that replaces each pixel with the local maximum, expanding bright regions. |
| **Erosion** | A morphological operation that replaces each pixel with the local minimum, shrinking bright regions. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Gradient** | The morphological gradient: dilation minus erosion, producing an edge-detection map. |
| **Morphology** | Mathematical morphology; a branch of image processing based on set-theoretic operations on image shapes. |
| **Opening** | Erosion followed by dilation; smooths features smaller than the structuring element without expanding larger ones. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Shift Register** | A chain of flip-flops that delays data by one clock per stage, forming a sliding window over consecutive pixels. |
| **Structuring Element** | The shape and size of the neighborhood used for morphological operations (cross, square, etc.). |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
