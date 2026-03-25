---
draft: true
sidebar_position: 49
slug: /instruments/videomancer/chromahold
title: "Chroma Hold"
image: /img/instruments/videomancer/chromahold/chromahold_hero_s1.png
description: "Color is the first thing the eye tracks."
---

![Chroma Hold hero image](/img/instruments/videomancer/chromahold/chromahold_hero_s1.png)
*Chroma Hold isolating a narrow band of red hues from a busy street scene, leaving everything else desaturated.*

---

## Overview

**Chroma Hold** is a selective color isolation effect. It strips the color from your entire image except for pixels whose hue falls within a window you define. The result is that striking "pop of color" look: a red umbrella against a grey cityscape, a single blue flower in a monochrome field. You control *where* on the color wheel the window sits, *how wide* it opens, and *how softly* its edges feather into desaturation.

Under the hood, Chroma Hold approximates hue without a costly ***CORDIC*** (coordinate rotation) engine. Instead it uses a quadrant-based lookup on the U and V chroma axes, computing angular distance with nothing but shifts, adds, and a single multiply per channel. This keeps the design small: roughly 400 logic cells and zero block RAMs: while still delivering smooth hue detection across the full 360° color wheel.

:::note
Three knobs: **Sat Boost**, **Desat Level**, and **Brightness**: appear on the panel but are reserved for a future firmware update. They are mapped to registers in the hardware but are not yet connected to the processing pipeline.
:::

### What's In a Name?

The name ***Chroma Hold*** describes exactly what the effect does: it ***holds*** the ***chroma***: the color: for a chosen hue range and lets everything else fall to grey. In broadcast engineering, a "chroma key" removes a specific color to composite one image over another. Chroma Hold flips that idea: instead of removing a color, it *preserves* one and removes everything else. The word "hold" also echoes sample-and-hold circuits in analog synthesis, where a voltage is captured and held steady: here, the color itself is the captured value.

---

## Quick Start

1. Feed a colorful video signal into your Videomancer while **Chroma Hold** is loaded. The image starts fully colored because **Hue Width** (Knob 2) defaults to a moderately open window.
2. Turn **Hue Width** (Knob 2) counterclockwise toward zero. The image becomes almost entirely desaturated (only a narrow sliver of hue remains in color.)
3. Slowly rotate **Hue Select** (Knob 1) through its full range. Watch the surviving color band sweep around the color wheel: reds, yellows, greens, cyans, blues, magentas, and back to red.
4. Widen the window with **Hue Width** (Knob 2) and soften the boundary with **Edge Soft** (Knob 3). The transition between color and grey becomes gradual instead of a hard cutoff.

---

## Parameters

![Videomancer front panel with Chroma Hold loaded](/img/instruments/videomancer/chromahold/chromahold_control_panel.png)
*Videomancer's front panel with Chroma Hold active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Hue Select

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Hue Select** chooses the target hue angle on the color wheel. Rotating the knob sweeps through the full 360° of hue: reds near the bottom of the range, greens in the middle, blues and magentas higher up. The selected angle becomes the center of the hold window. Only pixels whose hue is close to this angle retain their color; everything else desaturates.

:::tip
Because the color wheel wraps around, the window crosses the 0°/360° boundary seamlessly. You can park the knob near either extreme to isolate reds (they'll wrap correctly.)
:::

---

### Knob 2 — Hue Width

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Hue Width** sets the angular width of the hue acceptance window, centered on the angle chosen by Hue Select. At minimum, the window is extremely narrow: almost no pixels qualify, and the image appears nearly monochrome. As you increase Hue Width, the window opens wider and more hues are admitted. At maximum, the window is so broad that most of the image retains its original color.

---

### Knob 3 — Edge Soft

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Edge Soft** controls the feathering at the boundaries of the hue window. At minimum, the transition from full color to full desaturation is an abrupt, hard edge. Increasing Edge Soft introduces a linear ramp: pixels near the boundary receive partial saturation, blending smoothly between the held color and the desaturated surroundings. This softens the visual cutoff and avoids the "cookie cutter" look of a hard mask.

---

### Knob 4 — Sat Boost

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Sat Boost** is reserved for a future update. The knob is mapped to a hardware register but is not yet connected to the processing pipeline. Adjusting it has no visible effect.

---

### Knob 5 — Desat Level

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Desat Level** is reserved for a future update. It is intended to control the residual chroma in rejected (desaturated) regions, but the underlying logic is not yet implemented. Adjusting it has no visible effect.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** is reserved for a future update. The register is assigned but no brightness offset or gain stage is connected in the processing pipeline. Adjusting it has no visible effect.

---

### Switch 7 — Invert Sel

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert Sel** reverses the hue window selection. When set to On, pixels *inside* the window are desaturated and pixels *outside* retain their color: the exact opposite of the default behavior. This is useful when you want to remove a single hue rather than isolate one.

:::tip
Combined with a narrow **Hue Width**, **Invert Sel** lets you surgically remove a single color from your image while keeping everything else vibrant.
:::

---

### Switch 8 — Show Mask

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Show Mask** replaces the normal video output with a grayscale visualization of the hold factor. White regions represent pixels that retain full color (hold factor = max); black regions represent fully desaturated pixels. Intermediate gray values show the feathered edge region. This is a diagnostic mode for dialing in precise hue selections.

---

### Switch 9 — Sat Gate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Sat Gate** enables a saturation threshold that rejects low-saturation pixels regardless of their hue angle. When enabled, pixels with very little chroma: near-grey tones: are forced to desaturate even if their nominal hue falls within the selection window. This prevents noisy, ambiguous hues in grey regions from "leaking" color.

:::note
The saturation gate threshold is fixed internally at a magnitude of 64 (out of 1023). It cannot be adjusted by the user.
:::

---

### Switch 10 — Luma Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Luma Invert** applies a bitwise complement to the luminance channel before output. The brightness values of the image flip: darks become lights and lights become darks. This inversion applies only to the Y channel; chroma is unaffected. In Show Mask mode, Luma Invert has no visible effect on the mask itself because the mask replaces the Y channel.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the delayed input signal directly to the output, skipping all Chroma Hold processing. The sync delay pipeline still operates, so toggling Bypass does not cause a glitch or timing disruption. Use Bypass for instant A/B comparison between the original video and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the wet/dry blend between the processed output and the original input. At maximum, the output is entirely the processed (held/desaturated) result. At minimum, the output is the unprocessed input. Intermediate values produce a crossfade, which can create a partial desaturation effect that is subtler than the full-strength hold.

---

## Background

### Hue in YUV color space

Video arriving at Chroma Hold is encoded in ***YUV 4:4:4*** format: a luminance (Y) channel carrying brightness, and two chrominance channels (U and V) carrying color information. Hue: the perceived color: is encoded as the angle formed by the U and V values relative to the neutral point (U = 512, V = 512). Red, for instance, sits at one angle, green at another, and blue at yet another. Saturation is the distance from the neutral point: a vivid color sits far from center, and a grey sits near it.

Computing the true angle normally requires a ***CORDIC*** (Coordinate Rotation Digital Computer) or an arctangent lookup table, both of which are expensive in a small FPGA. Chroma Hold sidesteps this by using a quadrant-based approximation: it determines which of four UV quadrants the pixel sits in, computes the ratio of the smaller axis to the larger, and applies a quadrant offset. The result maps the full 360° of hue onto a 0–1023 integer range with reasonable accuracy and no multiply-heavy math.

### Selective desaturation

Once the hue angle of each pixel is known, Chroma Hold computes the angular distance between that pixel's hue and the target set by **Hue Select**. The distance wraps correctly across the 0°/360° boundary. If the distance falls inside half the **Hue Width**, the pixel receives a ***hold factor*** of 1023 (full color). If it falls outside the width plus the **Edge Soft** ramp, the hold factor is zero (full desaturation). In between, the factor ramps linearly, producing a smooth feather.

The hold factor multiplies each chroma axis independently: |U| and |V| are scaled by the factor, then re-centered on 512 with the original sign restored. This preserves the hue angle of held pixels while progressively collapsing rejected pixels to neutral grey.

### Saturation gating

Near-grey pixels have very small U and V offsets. Their hue angle is essentially random: dominated by noise rather than meaningful color. Without a guard, these noisy hues can flicker in and out of the selection window, creating speckle artifacts in grey regions. The **Sat Gate** toggle addresses this by forcing the hold factor to zero whenever the Manhattan-distance saturation magnitude falls below a threshold. Only pixels with enough chroma saturation to have a reliable hue angle are candidates for color holding.


---

## Signal Flow

### Signal Flow Notes

The processing pipeline is two stages deep: one clock for hue approximation and one for the hold-factor computation plus chroma multiply. Three parallel interpolator instances then blend the wet (processed) and dry (delayed original) signals over four additional clocks, for a total latency of six clocks from pixel input to mixed output. A separate delay pipeline holds the sync signals and original pixel data for seven clocks to align them with the interpolator output.

The most critical interaction is the relationship between **Hue Select**, **Hue Width**, and **Edge Soft**. Hue Select sets the window's center, Hue Width sets the hard boundary on each side, and Edge Soft extends a linear ramp beyond that boundary. The ramp calculation `1023 − (distance − half_width) × 2` produces a graceful falloff when Edge Soft is nonzero, but with Edge Soft at zero the transition is a single-sample step from full color to grey.

:::warning
Because hue approximation uses a ratio-based estimate rather than a true arctangent, the angular accuracy degrades slightly for very low-saturation pixels. The **Sat Gate** toggle is designed to mitigate this: enable it whenever your source contains large grey or near-neutral regions.
:::


---

## Exercises

These exercises progress from basic hue isolation to creative uses of the selection mask and inversion controls. Each builds on the previous, exploring more of Chroma Hold's signal chain.
### Exercise 1: Single-Color Pop

![Single-Color Pop result](/img/instruments/videomancer/chromahold/chromahold_ex1_s1.png)
*Single-Color Pop — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic "color pop" shot: one vivid color stands out against a desaturated background.

#### Key Concepts

- Hue selection isolates a narrow band of the color wheel
- Edge softening controls the transition between color and grey
- Saturation gating prevents noise in neutral regions

#### Video Source

A scene with a single strong primary color against a varied background: a red flower in a garden, a blue car on a grey street, or someone wearing a bright jacket.

#### Steps

1. Load **Chroma Hold** and feed your source signal. The image starts mostly colored.
2. Turn **Hue Width** (Knob 2) fully counterclockwise to narrow the window down. The image becomes nearly monochrome.
3. Slowly rotate **Hue Select** (Knob 1) until the color you want "pops" back into the image. Fine-tune until only that hue survives.
4. Open **Hue Width** (Knob 2) slightly to let the full range of your target color through. Reds, for instance, span a wider range than you might expect.
5. Increase **Edge Soft** (Knob 3) from zero. Watch the harsh boundary between color and grey soften into a smooth transition.
6. Enable **Sat Gate** (Switch 9). Any speckled color noise in grey regions disappears.

#### Settings

| Control | Value | Notes |
|---------|-------|-------|
| Hue Select | ~30% | Adjust to target hue |
| Hue Width | ~30% | Narrow window |
| Edge Soft | ~30% | Gentle feather |
| Sat Boost | Any | Reserved — no effect |
| Desat Level | Any | Reserved — no effect |
| Brightness | Any | Reserved — no effect |
| Invert Sel | Off | Normal selection |
| Show Mask | Off | View result |
| Sat Gate | On | Clean grey regions |
| Luma Invert | Off | Normal brightness |
| Bypass | Off | Processing active |
| Mix | 100% | Full effect |

---

### Exercise 2: Selection Matte Preview

![Selection Matte Preview result](/img/instruments/videomancer/chromahold/chromahold_ex2_s1.png)
*Selection Matte Preview — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Use the mask preview to build a clean selection matte, then switch to the final processed view.

#### Key Concepts

- Show Mask visualizes the hold factor as a grayscale key
- The mask is useful for dialing in precise hue selections before viewing the final result
- Edge Soft and Hue Width are easier to tune while watching the mask

#### Video Source

Footage with a clearly defined colored subject against a contrasting background (for example, green foliage against a brown fence.)

#### Steps

1. Enable **Show Mask** (Switch 8). The output becomes grayscale (white where color is held, black where it's desaturated.)
2. Rotate **Hue Select** (Knob 1) until the subject appears as a bright white shape against a dark background.
3. Widen **Hue Width** (Knob 2) until the entire subject is solidly white.
4. Increase **Edge Soft** (Knob 3) to smooth jagged edges in the mask. You should see a gentle gradient at the boundary.
5. Enable **Sat Gate** (Switch 9) and observe any speckle in the dark regions disappearing.
6. Disable **Show Mask** (Switch 8) to see the final color-isolated result with the selection you just tuned.

#### Settings

| Control | Value | Notes |
|---------|-------|-------|
| Hue Select | ~50% | Adjust to target hue |
| Hue Width | ~50% | Wide enough for full subject |
| Edge Soft | ~50% | Smooth boundary |
| Sat Boost | Any | Reserved — no effect |
| Desat Level | Any | Reserved — no effect |
| Brightness | Any | Reserved — no effect |
| Invert Sel | Off | Normal selection |
| Show Mask | On | Mask preview active |
| Sat Gate | On | Clean dark regions |
| Luma Invert | Off | Normal brightness |
| Bypass | Off | Processing active |
| Mix | 100% | Full effect |

---

### Exercise 3: Inverted Hue Removal

![Inverted Hue Removal result](/img/instruments/videomancer/chromahold/chromahold_ex3_s1.png)
*Inverted Hue Removal — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Remove a single color from the scene while keeping everything else vibrant, then add a luma inversion for a surreal negative-color look.

#### Key Concepts

- Invert Sel reverses which pixels are held and which are desaturated
- Luma Invert provides a dramatic tonal contrast against the color manipulation
- Partial mix blends the effect with the original for subtlety

#### Video Source

A scene with one dominant color that you want to remove: a large blue sky above a colorful landscape, or a green screen backdrop behind a subject.

#### Steps

1. Start with a moderate **Hue Width** (Knob 2 ~60%) and no edge softening.
2. Rotate **Hue Select** (Knob 1) to target the color you want to remove.
3. Enable **Invert Sel** (Switch 7). The targeted color desaturates and everything else remains vibrant (the opposite of a color pop.)
4. Add **Edge Soft** (Knob 3 ~60%) to blend the boundary smoothly.
5. Enable **Luma Invert** (Switch 10). The brightness values flip, creating a negative-image effect in luminance while the chroma manipulation continues independently.
6. Lower **Mix** (Fader 12) to roughly 60%. The processed result blends with the original input, producing a partially desaturated, partially inverted composite.

#### Settings

| Control | Value | Notes |
|---------|-------|-------|
| Hue Select | ~60% | Target color to remove |
| Hue Width | ~60% | Moderately wide window |
| Edge Soft | ~60% | Smooth edge blend |
| Sat Boost | Any | Reserved — no effect |
| Desat Level | Any | Reserved — no effect |
| Brightness | Any | Reserved — no effect |
| Invert Sel | On | Inverted — desaturate target |
| Show Mask | Off | View final result |
| Sat Gate | Off | Allow all saturations |
| Luma Invert | On | Inverted brightness |
| Bypass | Off | Processing active |
| Mix | ~60% | Partial blend |

---
## Glossary

- **Chroma**: The color information in a video signal, encoded as U and V components relative to a neutral midpoint.

- **CORDIC**: Coordinate Rotation Digital Computer; an iterative algorithm for trigonometric calculations. Chroma Hold avoids it in favor of a quadrant-based approximation.

- **Desaturation**: Reducing the color intensity of a pixel toward neutral grey by collapsing U and V toward 512.

- **Feathering**: A gradual transition at the boundary of a selection rather than a hard edge; controlled by Edge Soft.

- **Hold Factor**: An internal per-pixel value (0–1023) that determines how much chroma is preserved. Full hold retains the original color; zero hold desaturates completely.

- **Hue**: The perceived color of a pixel, determined by the angle of its U/V values relative to the neutral axis.

- **Manhattan Distance**: An approximation of geometric distance using axis-aligned sums (|ΔU| + |ΔV|) instead of the Euclidean square root.

- **Quadrant Lookup**: A method for approximating hue angle by determining which of four UV quadrants a pixel occupies and computing a dominant-axis ratio.

- **Saturation**: The intensity or vividness of a color; high saturation means vivid color, low saturation means near-grey.

- **Saturation Gate**: A threshold that rejects pixels with very low saturation, preventing noisy hue angles from contaminating the selection.

- **YUV 4:4:4**: A video format with full-resolution luminance (Y) and chrominance (U, V) channels (every pixel carries both brightness and color data.)

---
