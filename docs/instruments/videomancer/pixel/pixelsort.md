---
draft: true
sidebar_position: 231
slug: /instruments/videomancer/pixelsort
title: "Pixel Sort"
image: /img/instruments/videomancer/pixelsort/pixelsort_hero_s1.png
description: "Pixel sorting is one of the most recognizable techniques in glitch art — a computational process where pixels within a region are reordered by their brightness (or color) value, producing flowing streaks, melting edges, and crystalline bands that look like a digital image caught in the act of dissolving."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import pixelsort_control_panel from '/img/instruments/videomancer/pixelsort/pixelsort_control_panel.png';
import pixelsort_source1_sunset from '/img/instruments/videomancer/pixelsort/pixelsort_source1_sunset.png';
import pixelsort_source2_ballerina from '/img/instruments/videomancer/pixelsort/pixelsort_source2_ballerina.png';
import pixelsort_source3_turtle from '/img/instruments/videomancer/pixelsort/pixelsort_source3_turtle.png';
import pixelsort_source4_pattern from '/img/instruments/videomancer/pixelsort/pixelsort_source4_pattern.png';
import pixelsort_source5_man from '/img/instruments/videomancer/pixelsort/pixelsort_source5_man.png';
import pixelsort_source6_wood from '/img/instruments/videomancer/pixelsort/pixelsort_source6_wood.png';
import pixelsort_hero_s1 from '/img/instruments/videomancer/pixelsort/pixelsort_hero_s1.png';
import pixelsort_hero_s2 from '/img/instruments/videomancer/pixelsort/pixelsort_hero_s2.png';
import pixelsort_hero_s3 from '/img/instruments/videomancer/pixelsort/pixelsort_hero_s3.png';
import pixelsort_hero_s4 from '/img/instruments/videomancer/pixelsort/pixelsort_hero_s4.png';
import pixelsort_hero_s5 from '/img/instruments/videomancer/pixelsort/pixelsort_hero_s5.png';
import pixelsort_hero_s6 from '/img/instruments/videomancer/pixelsort/pixelsort_hero_s6.png';
import pixelsort_ex1_s1 from '/img/instruments/videomancer/pixelsort/pixelsort_ex1_s1.png';
import pixelsort_ex1_s2 from '/img/instruments/videomancer/pixelsort/pixelsort_ex1_s2.png';
import pixelsort_ex1_s3 from '/img/instruments/videomancer/pixelsort/pixelsort_ex1_s3.png';
import pixelsort_ex1_s4 from '/img/instruments/videomancer/pixelsort/pixelsort_ex1_s4.png';
import pixelsort_ex1_s5 from '/img/instruments/videomancer/pixelsort/pixelsort_ex1_s5.png';
import pixelsort_ex1_s6 from '/img/instruments/videomancer/pixelsort/pixelsort_ex1_s6.png';
import pixelsort_ex2_s1 from '/img/instruments/videomancer/pixelsort/pixelsort_ex2_s1.png';
import pixelsort_ex2_s2 from '/img/instruments/videomancer/pixelsort/pixelsort_ex2_s2.png';
import pixelsort_ex2_s3 from '/img/instruments/videomancer/pixelsort/pixelsort_ex2_s3.png';
import pixelsort_ex2_s4 from '/img/instruments/videomancer/pixelsort/pixelsort_ex2_s4.png';
import pixelsort_ex2_s5 from '/img/instruments/videomancer/pixelsort/pixelsort_ex2_s5.png';
import pixelsort_ex2_s6 from '/img/instruments/videomancer/pixelsort/pixelsort_ex2_s6.png';
import pixelsort_ex3_s1 from '/img/instruments/videomancer/pixelsort/pixelsort_ex3_s1.png';
import pixelsort_ex3_s2 from '/img/instruments/videomancer/pixelsort/pixelsort_ex3_s2.png';
import pixelsort_ex3_s3 from '/img/instruments/videomancer/pixelsort/pixelsort_ex3_s3.png';
import pixelsort_ex3_s4 from '/img/instruments/videomancer/pixelsort/pixelsort_ex3_s4.png';
import pixelsort_ex3_s5 from '/img/instruments/videomancer/pixelsort/pixelsort_ex3_s5.png';
import pixelsort_ex3_s6 from '/img/instruments/videomancer/pixelsort/pixelsort_ex3_s6.png';

# Pixel Sort

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: pixelsort_source1_sunset, after: pixelsort_hero_s1 },
    { label: "Ballerina", before: pixelsort_source2_ballerina, after: pixelsort_hero_s2 },
    { label: "Turtle", before: pixelsort_source3_turtle, after: pixelsort_hero_s3 },
    { label: "Pattern", before: pixelsort_source4_pattern, after: pixelsort_hero_s4 },
    { label: "Man", before: pixelsort_source5_man, after: pixelsort_hero_s5 },
    { label: "Wood", before: pixelsort_source6_wood, after: pixelsort_hero_s6 },
  ]}
/>
*Pixel Sort reordering pixels by brightness within a sliding 8-element window, producing the glitch-art melt and crystalline streak effects that define the pixel sorting aesthetic.*

---

## Overview

**Pixel sorting** is one of the most recognizable techniques in glitch art — a computational process where pixels within a region are reordered by their brightness (or color) value, producing flowing streaks, melting edges, and crystalline bands that look like a digital image caught in the act of dissolving. The effect emerged from creative coding and Processing sketches in the early 2010s, where artists like Kim Asendorf popularized algorithms that sort horizontal runs of pixels when certain threshold conditions are met.

Pixel Sort implements this technique in real-time FPGA hardware using an 8-element sliding window and a 3-pass **odd-even transposition sort** — a simple parallel sorting network where adjacent elements are compared and swapped in alternating pairs. The sort key can be either luminance (Y) or chrominance (U), and the Window knob selects which position in the sorted array is output (from the minimum to the maximum). A luminance threshold gate controls which pixel runs participate in sorting, allowing clean areas to pass through while regions above the threshold dissolve into sorted streaks.

The combination of sort direction (ascending vs descending), threshold gating, window position selection, and chroma-key sorting gives Pixel Sort a surprising range of expression — from subtle edge-softening at low settings to full horizontal pixel meltdown at extreme values. The 8-pixel window is small enough to preserve the general structure of the image while large enough to create visible reordering artifacts.

---

## Background

### What Is Pixel Sorting?

**Pixel sorting** rearranges pixels within defined regions (typically horizontal scanline segments) by a sort key, usually brightness. Bright pixels migrate to one end of the sorted run, dark pixels to the other, creating characteristic streaks that align with the sort direction. The artistic effect depends on which pixels are included in each sorting run — thresholds, masks, and window sizes all control the boundary between sorted and unsorted regions.

### What Is an Odd-Even Transposition Sort?

The **odd-even transposition sort** (also known as brick sort) is a parallel sorting algorithm well-suited to hardware implementation. It works by alternating between "even" passes (comparing and swapping pairs at positions 0-1, 2-3, 4-5, 6-7) and "odd" passes (comparing pairs at 1-2, 3-4, 5-6). After N/2 passes, any array of N elements is guaranteed sorted. The algorithm requires only local compare-and-swap operations with no data routing, making it efficient in FPGA fabric. Pixel Sort uses 3 passes on 8 elements, which produces a partially sorted result — not perfectly sorted, but sufficiently ordered to create the desired visual effect.

### What Is Threshold Gating?

**Threshold gating** in pixel sorting determines which pixels participate in the sort. When a pixel's luminance is below the threshold, it passes through unchanged. When above, it enters the sorting window. This creates the characteristic pixel-sort look where dark areas of the image remain intact while bright areas dissolve into sorted streaks. The threshold is what separates pixel sorting from simple blur — it creates the boundary between order and disorder.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y, U, V ────────────────────────────────────────────────────
│   │
│   ├─ 1. Invert (optional)       (complement Y before sort)
│   ├─ 2. 8-Pixel Shift Register  (sliding window capture)
│   ├─ 3. Sort Key Selection      (luma or chroma U)
│   ├─ 4. Threshold Gate           (pass-through if below threshold)
│   ├─ 5. Odd-Even Sort (3 pass)  (parallel compare-and-swap)
│   ├─ 6. Window Position Select  (output pixel 0–7 from sorted array)
│   └─ 7. Wet/Dry Mix             (blend with delayed original)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through with 8-clock delay
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The 8-pixel shift register captures consecutive horizontal pixels and feeds them simultaneously to the sort network. The sort key determines which channel drives the ordering — in Luma mode, pixels are sorted by brightness; in Chroma mode, they're sorted by U value, which can produce surprising color-grouping effects. The Window knob selects which position in the sorted array is output: position 0 is the minimum (darkest), position 7 is the maximum (brightest), and intermediate positions blend between. This position selection is the key creative control — it determines whether the output favors darks, lights, or medians.

---

## Parameter Reference

<img src={pixelsort_control_panel} alt="Videomancer front panel with Pixel Sort loaded"/>
*Videomancer's front panel with Pixel Sort active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the luminance threshold below which pixels pass through the sort network unchanged. At 0%, all pixels participate in sorting regardless of brightness. As Threshold increases, only pixels brighter than the threshold enter the sort window — darker pixels pass through untouched. This creates the signature pixel-sort boundary between intact image and dissolved streaks. At maximum, only the very brightest highlights are sorted.

---

#### Knob 2 — Window
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls which position in the sorted 8-pixel window is output. The knob maps to positions 0–7 using the top 3 bits. At minimum (position 0), the output is the darkest pixel in the window — an erosion-like effect. At maximum (position 7), the output is the brightest pixel — a dilation-like effect. Middle positions output median values, producing a smoothing or averaging effect. This is the primary creative control for the sort's visual character.

---

#### Knob 3 — Intensity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the overall intensity of the sorting effect. At maximum (default), the sorted output is used at full strength. As Intensity decreases, the sorted result is blended with the original pixel, reducing the visual impact of the reordering. This provides a more gradual control than the wet/dry mix fader, allowing subtle sorting artifacts to be introduced.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies contrast gain around the midpoint (512) to the sorted output. Higher values increase the tonal separation between sorted pixels, making the sorting artifacts more defined. Lower values compress the tonal range, softening the sorted streaks.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC brightness offset to the output. At center, no offset. Above center brightens; below center darkens.

---

#### Knob 6 — Bias
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the threshold center point. Bias offsets the threshold value, allowing you to fine-tune exactly which brightness range triggers sorting without changing the Threshold knob position. This is useful for dialing in the precise boundary between sorted and unsorted regions.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Sort Dir** | Ascend | Descend |
| **8 — Channel** | Luma | Chroma |
| **9 — Mode** | Sort | Threshold |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control sort direction, sorting key, gating mode, luminance inversion, and bypass. The Sort Dir and Channel switches have the most dramatic impact on the visual character. Mode selects whether sorting is continuous or threshold-gated.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the sorted output and the original input. At 100%, the full sorting effect is visible. Lowering the fader blends the original back in, allowing subtle sorting artifacts to be overlaid on the intact image.

---

## Guided Exercises

These exercises progress from basic pixel sorting with threshold gating to creative uses of window position, chroma sorting, and sort direction for glitch-art effects.

### Exercise 1: Classic Pixel Sort with Threshold

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: pixelsort_source1_sunset, after: pixelsort_ex1_s1 },
    { label: "Ballerina", before: pixelsort_source2_ballerina, after: pixelsort_ex1_s2 },
    { label: "Turtle", before: pixelsort_source3_turtle, after: pixelsort_ex1_s3 },
    { label: "Pattern", before: pixelsort_source4_pattern, after: pixelsort_ex1_s4 },
    { label: "Man", before: pixelsort_source5_man, after: pixelsort_ex1_s5 },
    { label: "Wood", before: pixelsort_source6_wood, after: pixelsort_ex1_s6 },
  ]}
/>
*Classic Pixel Sort with Threshold — simulated result across source images.*
**Source**: High-contrast portrait or landscape with distinct bright and dark regions — faces, skylines, or architectural shots.

**Objective**: Create the classic pixel-sort look where bright areas dissolve into horizontal streaks while dark areas remain intact.

1. **Enable threshold**: Set Mode to Threshold (Switch 9). Set Threshold to ~40%.
2. **Full window**: Set Window to maximum (position 7, output brightest pixel).
3. **Observe sorting**: Bright areas of the image dissolve into horizontal streaks while darker areas remain intact.
4. **Adjust threshold**: Lower Threshold to include more of the image in sorting. Raise it to restrict sorting to highlights only.
5. **Try ascending**: Set Sort Dir to Ascend (Switch 7), Window to minimum (position 0). Now you see the darkest pixel in each window — a darker, erosion-like effect.
6. **Invert boundary**: Toggle Invert (Switch 10). The threshold boundary flips — formerly intact regions now sort, and vice versa.

**Key concepts**: Threshold creates the sort boundary, window position selects min/max/median from sorted array, sort direction reverses the ordering

---

### Exercise 2: Window Position Exploration

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: pixelsort_source1_sunset, after: pixelsort_ex2_s1 },
    { label: "Ballerina", before: pixelsort_source2_ballerina, after: pixelsort_ex2_s2 },
    { label: "Turtle", before: pixelsort_source3_turtle, after: pixelsort_ex2_s3 },
    { label: "Pattern", before: pixelsort_source4_pattern, after: pixelsort_ex2_s4 },
    { label: "Man", before: pixelsort_source5_man, after: pixelsort_ex2_s5 },
    { label: "Wood", before: pixelsort_source6_wood, after: pixelsort_ex2_s6 },
  ]}
/>
*Window Position Exploration — simulated result across source images.*
**Source**: Geometric or graphic content with clear edges and varied brightness — text, patterns, or UI elements.

**Objective**: Understand how the Window knob selects different positions in the sorted pixel array, from erosion to dilation effects.

1. **Continuous sort**: Set Mode to Sort (Switch 9). All pixels participate.
2. **Minimum window** (position 0): The output is the darkest pixel in each 8-pixel neighborhood. This is morphological erosion — bright features shrink.
3. **Maximum window** (position 7): The output is the brightest pixel — morphological dilation. Bright features expand.
4. **Mid window** (~50%, position 3-4): The output is the median — a powerful noise-reduction and smoothing filter.
5. **Sweep slowly**: Move Window from 0 to 100% and observe the transition from erosion through median to dilation.
6. **Add Contrast**: Set Contrast to ~70% to sharpen the sorted artifacts.

**Key concepts**: Position 0 = local minimum (erosion), position 7 = local maximum (dilation), middle positions = median filtering, window becomes a morphological operator

---

### Exercise 3: Chroma Sorting and Creative Glitch

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: pixelsort_source1_sunset, after: pixelsort_ex3_s1 },
    { label: "Ballerina", before: pixelsort_source2_ballerina, after: pixelsort_ex3_s2 },
    { label: "Turtle", before: pixelsort_source3_turtle, after: pixelsort_ex3_s3 },
    { label: "Pattern", before: pixelsort_source4_pattern, after: pixelsort_ex3_s4 },
    { label: "Man", before: pixelsort_source5_man, after: pixelsort_ex3_s5 },
    { label: "Wood", before: pixelsort_source6_wood, after: pixelsort_ex3_s6 },
  ]}
/>
*Chroma Sorting and Creative Glitch — simulated result across source images.*
**Source**: Colorful footage with saturated hues — flowers, graffiti, color bars, or abstract video art.

**Objective**: Explore chroma-key sorting and combine with inversion and sort direction for creative glitch effects.

1. **Chroma sort**: Set Channel to Chroma (Switch 8). Pixels are now sorted by U (blue-yellow) instead of brightness.
2. **Observe color banding**: Colors group into horizontal bands — blues cluster together, yellows cluster separately. Very different from luma sorting.
3. **Descending**: Switch Sort Dir to Descend (Switch 7). The color band ordering reverses.
4. **Threshold chroma**: Switch Mode to Threshold. Only highly saturated regions sort by chroma.
5. **Invert + chroma**: Enable Invert. The sort boundary in chroma mode creates unusual color separation.
6. **Mix blend**: Lower Mix to ~40%. The chroma-sorted texture overlays the original, creating subtle color displacement.

**Key concepts**: Chroma sorting groups by color instead of brightness, creates color banding effects, inversion and threshold in chroma mode produce unique results

---


## Tips

- **Threshold is the composition tool**: The threshold boundary between sorted and unsorted is where the magic happens — place it at the edge of highlights for subtle melt, at midtones for dramatic dissolution.
- **Window as morphology**: With continuous sorting, position 0 is erosion and position 7 is dilation — use this as a fast morphological operator.
- **Median filtering**: Window at ~50% in Sort mode acts as an effective noise reducer (median of 8).
- **Chroma creates color banding**: Chroma sorting produces effects impossible with brightness sorting — use on colorful sources.
- **Mix for subtlety**: Heavy sorting at 20-30% mix adds a subtle digital texture without destroying the image.
- **Bias fine-tunes threshold**: When the Threshold knob position is right but the boundary isn't quite where you want it, adjust Bias instead.
- **Invert flips everything**: Inversion reverses both the sort order and the threshold boundary, creating complementary effects.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bitonic Network** | A type of parallel sorting network; Pixel Sort uses a simpler odd-even transposition variant. |
| **Compare-and-Swap** | The fundamental sorting operation: compare two elements and exchange them if they're out of order. |
| **Dilation** | Morphological operation that outputs the local maximum, expanding bright features. |
| **Erosion** | Morphological operation that outputs the local minimum, shrinking bright features. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Glitch Art** | An art form that exploits digital or analog errors for aesthetic effect. |
| **Median** | The middle value in a sorted set; outputs moderate values that reject outliers. |
| **Odd-Even Transposition Sort** | A parallel sorting algorithm that alternates between comparing even-indexed and odd-indexed adjacent pairs. |
| **Pixel Sorting** | The practice of reordering pixels within image regions by a sort key (usually brightness) for glitch-art effects. |
| **Shift Register** | A chain of flip-flops that creates a sliding window over consecutive data values. |
| **Sort Key** | The value used to determine ordering; either luminance (Y) or chrominance (U) in Pixel Sort. |
| **Threshold** | A brightness value below which pixels bypass sorting, creating the boundary between intact and dissolved regions. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
