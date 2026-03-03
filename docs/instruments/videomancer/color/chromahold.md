---
draft: true
sidebar_position: 49
slug: /instruments/videomancer/chromahold
title: "Chroma Hold"
image: /img/instruments/videomancer/chromahold/chromahold_hero_s1.png
description: "Color is the first thing the eye tracks."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import chromahold_control_panel from '/img/instruments/videomancer/chromahold/chromahold_control_panel.png';
import chromahold_source1_field from '/img/instruments/videomancer/chromahold/chromahold_source1_field.png';
import chromahold_source2_parrot from '/img/instruments/videomancer/chromahold/chromahold_source2_parrot.png';
import chromahold_source3_elephant from '/img/instruments/videomancer/chromahold/chromahold_source3_elephant.png';
import chromahold_source4_pattern from '/img/instruments/videomancer/chromahold/chromahold_source4_pattern.png';
import chromahold_source5_girl from '/img/instruments/videomancer/chromahold/chromahold_source5_girl.png';
import chromahold_source6_knit from '/img/instruments/videomancer/chromahold/chromahold_source6_knit.png';
import chromahold_hero_s1 from '/img/instruments/videomancer/chromahold/chromahold_hero_s1.png';
import chromahold_hero_s2 from '/img/instruments/videomancer/chromahold/chromahold_hero_s2.png';
import chromahold_hero_s3 from '/img/instruments/videomancer/chromahold/chromahold_hero_s3.png';
import chromahold_hero_s4 from '/img/instruments/videomancer/chromahold/chromahold_hero_s4.png';
import chromahold_hero_s5 from '/img/instruments/videomancer/chromahold/chromahold_hero_s5.png';
import chromahold_hero_s6 from '/img/instruments/videomancer/chromahold/chromahold_hero_s6.png';
import chromahold_ex1_s1 from '/img/instruments/videomancer/chromahold/chromahold_ex1_s1.png';
import chromahold_ex1_s2 from '/img/instruments/videomancer/chromahold/chromahold_ex1_s2.png';
import chromahold_ex1_s3 from '/img/instruments/videomancer/chromahold/chromahold_ex1_s3.png';
import chromahold_ex1_s4 from '/img/instruments/videomancer/chromahold/chromahold_ex1_s4.png';
import chromahold_ex1_s5 from '/img/instruments/videomancer/chromahold/chromahold_ex1_s5.png';
import chromahold_ex1_s6 from '/img/instruments/videomancer/chromahold/chromahold_ex1_s6.png';
import chromahold_ex2_s1 from '/img/instruments/videomancer/chromahold/chromahold_ex2_s1.png';
import chromahold_ex2_s2 from '/img/instruments/videomancer/chromahold/chromahold_ex2_s2.png';
import chromahold_ex2_s3 from '/img/instruments/videomancer/chromahold/chromahold_ex2_s3.png';
import chromahold_ex2_s4 from '/img/instruments/videomancer/chromahold/chromahold_ex2_s4.png';
import chromahold_ex2_s5 from '/img/instruments/videomancer/chromahold/chromahold_ex2_s5.png';
import chromahold_ex2_s6 from '/img/instruments/videomancer/chromahold/chromahold_ex2_s6.png';
import chromahold_ex3_s1 from '/img/instruments/videomancer/chromahold/chromahold_ex3_s1.png';
import chromahold_ex3_s2 from '/img/instruments/videomancer/chromahold/chromahold_ex3_s2.png';
import chromahold_ex3_s3 from '/img/instruments/videomancer/chromahold/chromahold_ex3_s3.png';
import chromahold_ex3_s4 from '/img/instruments/videomancer/chromahold/chromahold_ex3_s4.png';
import chromahold_ex3_s5 from '/img/instruments/videomancer/chromahold/chromahold_ex3_s5.png';
import chromahold_ex3_s6 from '/img/instruments/videomancer/chromahold/chromahold_ex3_s6.png';

# Chroma Hold

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: chromahold_source1_field, after: chromahold_hero_s1 },
    { label: "Parrot", before: chromahold_source2_parrot, after: chromahold_hero_s2 },
    { label: "Elephant", before: chromahold_source3_elephant, after: chromahold_hero_s3 },
    { label: "Pattern", before: chromahold_source4_pattern, after: chromahold_hero_s4 },
    { label: "Girl", before: chromahold_source5_girl, after: chromahold_hero_s5 },
    { label: "Knit", before: chromahold_source6_knit, after: chromahold_hero_s6 },
  ]}
/>
*Chromahold isolating a targeted hue range and desaturating the surrounding image to create selective color emphasis.*

---

## Overview

Color is the first thing the eye tracks. A single red flower in a field of green, a blue neon sign against a gray cityscape — selective color draws the viewer's attention with surgical precision. Chromahold implements this cinematic technique in real time, isolating a user-selected hue range while desaturating everything outside it.

The program works by analyzing the chrominance angle of each pixel — its position on the color wheel defined by the U and V components. An octant-based hue detection system identifies pixels whose color falls within an adjustable angular window centered on the target hue. Pixels inside the window retain their full color; pixels outside are progressively desaturated according to the Desat Level control. The boundary between colored and desaturated regions can be made razor-sharp or feathered smooth using the Edge Soft control.

A saturation gate adds intelligence to the selection — low-saturation pixels (near-gray) are excluded from the color hold regardless of their nominal hue angle, preventing neutral areas from being falsely colored by noise. The Show Mask mode reveals the selection as a grayscale matte, making it easy to dial in precise hue targeting before committing to the final look.

---

## Background

### What Is Hue Angle?

In the YUV color space, hue is determined by the angle of the (U, V) vector in the chrominance plane. The U axis represents blue-yellow variation, and the V axis represents red-cyan variation. The angle θ = atan2(V − 512, U − 512) gives the hue of each pixel. Chromahold approximates this angular measurement using an octant decomposition — dividing the UV plane into eight 45° sectors and computing the angular distance from the target hue within each sector. This avoids expensive trigonometric computation while providing sufficient angular resolution for perceptual color selection.

### What Is Selective Desaturation?

**Selective desaturation** is a compositing technique where a chosen color range retains its saturation while the rest of the image is converted to grayscale. The effect became iconic through films like *Schindler's List* (the girl in the red coat) and *Sin City* (selective color accents in an otherwise black-and-white world). Chromahold implements this by computing a per-pixel "hold factor" — a value between 0 (fully desaturated) and 1 (fully saturated) — based on the angular distance between the pixel's hue and the target hue: pixels inside the window get hold factor 1, pixels outside get a value determined by the Desat Level control, and pixels in the edge-soft transition zone get a smoothly interpolated value.

### What Is a Saturation Gate?

A **saturation gate** is a threshold applied to the chrominance magnitude — the distance of a pixel's (U, V) from the neutral point (512, 512). Pixels with very low saturation are inherently ambiguous in hue: a nearly gray pixel might technically have any hue angle, but the measurement is dominated by noise. By gating out low-saturation pixels, Chromahold avoids false color assignments in neutral regions of the image. With Sat Gate enabled, only pixels with meaningful color content participate in the hue selection.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── UV Channels ────────────────────────────────────────────────
│   │
│   ├─ 1. Octant Decomposition   (determine UV quadrant/octant)
│   ├─ 2. Hue Angle Estimation   (angular distance from target hue)
│   ├─ 3. Window Comparison       (inside/outside hue window)
│   ├─ 4. Edge Soft Transition    (smooth feathering at window boundary)
│   ├─ 5. Saturation Gate         (reject low-saturation pixels, optional)
│   ├─ 6. Invert Selection        (optional: swap inside/outside)
│   ├─ 7. Hold Factor → Desat    (blend full color ↔ desaturated)
│   └─ 8. Sat Boost              (scale UV of held pixels)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Show Mask              (replace Y with hold factor, optional)
│   └─ 2. Brightness Offset      (DC shift)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The core of the algorithm is the octant-based hue detection. The UV plane is divided into eight 45° sectors, and the angular distance from the target hue is computed using only comparisons and subtractions — no division or trigonometry. The resulting angular distance is compared against the Hue Width to determine the hold factor. Edge Soft widens the transition zone, creating a gradual falloff rather than a hard boundary. The hold factor then controls how much the UV channels are attenuated toward neutral (512), producing the selective desaturation effect.

---

## Parameter Reference

<img src={chromahold_control_panel} alt="Videomancer front panel with Chroma Hold loaded"/>
*Videomancer's front panel with Chroma Hold active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Hue Select
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Selects the target hue angle on the color wheel. The full rotation of the knob covers 360° — sweeping through reds, yellows, greens, cyans, blues, and magentas. The selected hue defines the center of the hold window: pixels at this hue angle pass through with full color. The control maps linearly from 0° (red/orange) through 90° (green), 180° (cyan), 270° (blue/magenta), and back to 360° (red). Fine adjustment is critical for isolating specific hues.

---

#### Knob 2 — Hue Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the angular width of the hue window in degrees. At 0%, only pixels exactly matching the target hue are held — an impossibly narrow selection. At higher values, the window widens to accept a broader range of hues around the target. A width of ~30–40% typically captures a single perceptual color family (e.g., "red" or "green"). At 100%, the window is wide enough to accept nearly all hues, effectively disabling the color isolation.

---

#### Knob 3 — Edge Soft
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the softness of the transition between held (colored) and unheld (desaturated) regions. At 0%, the boundary is a hard step — pixels are either fully colored or fully desaturated. As Edge Soft increases, the transition zone widens, creating a gradual feathering where pixels near the window boundary receive partial desaturation. This prevents harsh, aliased edges in the color selection, producing a more natural-looking isolation.

---

#### Knob 4 — Sat Boost
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Boosts or cuts the saturation of pixels that pass the hue selection. At mid-position, held pixels retain their original saturation. Above center, the UV channels are amplified, making the selected colors more vivid and eye-catching. Below center, even the held pixels receive some desaturation. This control shapes the intensity of the color accent relative to the desaturated background.

---

#### Knob 5 — Desat Level
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets the desaturation level for pixels outside the hue window. At 0%, unselected pixels are fully desaturated — converted to pure grayscale. At mid-position, they retain roughly half their original saturation. At 100%, no desaturation occurs (the effect is disabled). This control determines the visual contrast between the held color accent and its surrounding context.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC offset to the output luminance channel. Use this to match the overall brightness of the processed output to the input level or to creatively darken/brighten the frame. The brightness shift applies equally to held and unheld regions.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Invert Sel** | Off | On |
| **8 — Show Mask** | Off | On |
| **9 — Sat Gate** | Off | On |
| **10 — Luma Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 provide selection modifiers and display modes. Invert Sel swaps the hold region. Show Mask reveals the selection matte for precise adjustment. Sat Gate prevents false-positive hue detection in neutral regions. Luma Invert provides a creative luminance reversal. Bypass enables instant comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the processed chromahold output and the original input signal. At 100%, the output is fully processed. Lowering the fader blends the original color back in, reducing the intensity of the selective desaturation effect. At 0%, the output is the unprocessed input.

---

## Guided Exercises

These exercises progress from basic single-hue isolation to advanced compositing techniques using the selection matte and saturation gate.

### Exercise 1: Single Hue Isolation

<BeforeAfterSlider
  sources={[
    { label: "Field", before: chromahold_source1_field, after: chromahold_ex1_s1 },
    { label: "Parrot", before: chromahold_source2_parrot, after: chromahold_ex1_s2 },
    { label: "Elephant", before: chromahold_source3_elephant, after: chromahold_ex1_s3 },
    { label: "Pattern", before: chromahold_source4_pattern, after: chromahold_ex1_s4 },
    { label: "Girl", before: chromahold_source5_girl, after: chromahold_ex1_s5 },
    { label: "Knit", before: chromahold_source6_knit, after: chromahold_ex1_s6 },
  ]}
/>
*Single Hue Isolation — simulated result across source images.*
**Source**: A scene with one dominant color and varied background — a red object against a neutral or mixed-color background works well.

**Objective**: Isolate a single color while desaturating the rest of the image.

1. **Find the hue**: Slowly sweep Hue Select through the full range. Watch for the target object to retain color while everything else goes gray.
2. **Narrow the window**: Reduce Hue Width until only the target hue is held. Too narrow and the selection becomes patchy; too wide and adjacent hues leak through.
3. **Soften the edge**: Increase Edge Soft to ~30% to smooth the boundary between color and gray. Look for natural-looking transitions.
4. **Full desaturation**: Set Desat Level to 0% for a full grayscale background.
5. **Boost the accent**: Increase Sat Boost above center to make the isolated color pop against the monochrome background.

**Key concepts**: Hue angle determines color identity, window width controls selectivity, edge softening creates natural transitions, desat level controls background saturation

---

### Exercise 2: Selection Matte Tuning

<BeforeAfterSlider
  sources={[
    { label: "Field", before: chromahold_source1_field, after: chromahold_ex2_s1 },
    { label: "Parrot", before: chromahold_source2_parrot, after: chromahold_ex2_s2 },
    { label: "Elephant", before: chromahold_source3_elephant, after: chromahold_ex2_s3 },
    { label: "Pattern", before: chromahold_source4_pattern, after: chromahold_ex2_s4 },
    { label: "Girl", before: chromahold_source5_girl, after: chromahold_ex2_s5 },
    { label: "Knit", before: chromahold_source6_knit, after: chromahold_ex2_s6 },
  ]}
/>
*Selection Matte Tuning — simulated result across source images.*
**Source**: Complex scene with multiple similar colors — a market stall, garden, or patterned fabric.

**Objective**: Use Show Mask mode to precisely tune hue selection parameters.

1. **Enable mask**: Turn on Show Mask (Switch 8). The output becomes a brightness map of the selection.
2. **Coarse target**: Sweep Hue Select to find the target hue — it appears as white regions in the mask.
3. **Width tuning**: Adjust Hue Width while watching the mask. Bright areas expand or contract as the window widens or narrows.
4. **Edge visibility**: Increase Edge Soft and observe the gray transition gradient around selected regions.
5. **Sat Gate effect**: Toggle Sat Gate (Switch 9). Watch neutral regions that were showing false white spots go black.
6. **Switch to color**: Disable Show Mask. The selection is now precisely tuned.

**Key concepts**: The selection matte reveals internal processing, saturation gating prevents false positives in neutral regions, mask tuning enables precise creative control

---

### Exercise 3: Inverted Selection and Creative Color

<BeforeAfterSlider
  sources={[
    { label: "Field", before: chromahold_source1_field, after: chromahold_ex3_s1 },
    { label: "Parrot", before: chromahold_source2_parrot, after: chromahold_ex3_s2 },
    { label: "Elephant", before: chromahold_source3_elephant, after: chromahold_ex3_s3 },
    { label: "Pattern", before: chromahold_source4_pattern, after: chromahold_ex3_s4 },
    { label: "Girl", before: chromahold_source5_girl, after: chromahold_ex3_s5 },
    { label: "Knit", before: chromahold_source6_knit, after: chromahold_ex3_s6 },
  ]}
/>
*Inverted Selection and Creative Color — simulated result across source images.*
**Source**: Multi-color footage with distinct color zones — video art, abstract animation, or painted surfaces.

**Objective**: Combine inverted selection, saturation boost, and luminance inversion for creative compositing.

1. **Invert selection**: Select a dominant hue, then enable Invert Sel (Switch 7). The dominant color becomes desaturated while everything else stays colored.
2. **Partial desaturation**: Set Desat Level to ~40% so the "removed" color retains some pastel saturation.
3. **Sat boost**: Push Sat Boost high to intensify the remaining colors against the muted target.
4. **Luma Invert**: Enable Luma Invert (Switch 10). The luminance structure inverts while the color selection pattern remains — a surreal negative-positive composite.
5. **Mix control**: Lower the Mix fader to ~60% to blend the effect with the original, creating a subtle color-shifted overlay.

**Key concepts**: Inverted selection removes rather than isolates a color, partial desaturation creates pastel effects, luminance inversion is independent of chroma selection

---


## Tips

- **Use Show Mask first**: Always tune your hue selection in mask mode before switching to the color output. The mask reveals exactly what the algorithm is selecting.
- **Sat Gate prevents noise**: Enable Sat Gate whenever working with real camera footage. Gray and near-gray regions produce unreliable hue angles that cause speckle artifacts without gating.
- **Edge Soft for realism**: A hard color boundary looks artificial. Even 20–30% edge softness creates a much more natural-looking isolation.
- **Invert for removal**: Use Invert Sel to remove a specific color rather than isolate it — useful for "everything except green" or "everything except skin tones."
- **Partial desat for subtlety**: Setting Desat Level to 30–50% instead of 0% creates a subtle color emphasis rather than the dramatic "one color in a gray world" effect.
- **Hue Select sweep for discovery**: Slowly sweeping the Hue Select knob across its full range reveals which hues are present in the source material.
- **Feedback for color cycling**: Route output to input. The selected hue feeds back at full saturation while everything else decays, creating a color-locked feedback loop.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chrominance** | The color information in a video signal, encoded as U (blue-yellow) and V (red-cyan) components in YUV color space. |
| **Desaturation** | Reducing the color intensity of a pixel toward neutral gray by moving the UV values toward (512, 512). |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Hold Factor** | A per-pixel value between 0 and 1 that determines how much of the original color is retained (1 = full color, 0 = fully desaturated). |
| **Hue Angle** | The angular position of a pixel's color on the UV color wheel, measured in degrees from 0° to 360°. |
| **Octant** | One of eight 45° sectors dividing the UV chrominance plane, used for efficient hue angle approximation without trigonometry. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Saturation** | The chrominance magnitude — the distance of a pixel's (U, V) from the neutral point (512, 512). |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
