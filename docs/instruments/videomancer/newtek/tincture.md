---
draft: true
sidebar_position: 264
slug: /instruments/videomancer/tincture
title: "Tincture"
image: /img/instruments/videomancer/tincture/tincture_hero.png
description: "Program guide for Tincture, a Videomancer newtek program for the LZX video synthesizer."
---

import tincture_before_after from '/img/instruments/videomancer/tincture/tincture_before_after.png';
import tincture_control_panel from '/img/instruments/videomancer/tincture/tincture_control_panel.png';
import tincture_exercise1_result from '/img/instruments/videomancer/tincture/tincture_exercise1_result.png';
import tincture_exercise2_result from '/img/instruments/videomancer/tincture/tincture_exercise2_result.png';
import tincture_exercise3_result from '/img/instruments/videomancer/tincture/tincture_exercise3_result.png';
import tincture_hero from '/img/instruments/videomancer/tincture/tincture_hero.png';
import tincture_source1_kodim15 from '/img/instruments/videomancer/tincture/tincture_source1_kodim15.png';
import tincture_source2_kodim03 from '/img/instruments/videomancer/tincture/tincture_source2_kodim03.png';
import tincture_source3_kodim13_bw from '/img/instruments/videomancer/tincture/tincture_source3_kodim13_bw.png';

# Tincture

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={tincture_hero} alt="Tincture hero image"/>
*Tincture mapping a live camera feed through the Thermal false-color palette with edge detection overlay, revealing luminance contours as glowing topographic lines.*
<img src={tincture_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Tincture applied.*

---

## Overview

Before digital color grading became commonplace, television engineers used false-color generators to visualize exposure levels. A monochrome luminance signal would be mapped through a lookup table of bold colors — blue for shadows, green for midtones, red for highlights — turning the invisible structure of brightness into a vivid, readable map. Scientific instruments, thermal cameras, and medical imaging devices still use the same principle to render single-channel data as rich color images.

Tincture applies this technique to live video. The input luminance is divided into configurable bands, and each band is assigned a color from one of eight palettes inspired by classic video synthesis instruments — the Fairlight CVI, the NewTek Video Toaster's ChromaFX, thermal imaging cameras, and scientific visualization systems. The name refers to the alchemical concept of a *tincture*: a concentrated essence that imparts color to a substance.

The processing chain includes input gain and bias (to stretch and shift the luminance range before lookup), configurable band count, inter-band smoothing (from hard Fairlight CVI steps to soft Video Toaster gradients), a tint mode that preserves original chroma, horizontal edge detection for contour overlay, animated band cycling, and a posterize pre-filter for chunkier quantization.

---

## Background

### False-Color Exposure Mapping

Professional video cameras have long included a false-color display mode for exposure monitoring. Each brightness zone is assigned a distinct hue — typically blue for underexposed shadow detail, green for proper skin-tone exposure, yellow for highlights approaching clipping, and red for fully clipped whites. This one-to-one mapping from luminance to palette color is exactly what Tincture implements, but with full creative control over the palette, the number of bands, and the crossover points between zones.

### The Fairlight CVI and Hard Banding

The Fairlight Computer Video Instrument, an Australian video synthesizer from the 1980s, featured a false-color mode with hard quantized bands — abrupt transitions between flat color regions with no interpolation between adjacent palette entries. The result had a stark, poster-like quality. Tincture's Smoothing control at zero reproduces this aesthetic: each luminance band maps to a single flat color with no gradation between adjacent levels.

### The NewTek Video Toaster and Soft Gradients

NewTek's Video Toaster ChromaFX took a different approach, interpolating smoothly between palette entries to create continuous color gradients across the luminance range. Rather than hard quantized steps, the colors blended into each other like a ramp or spectrogram. Tincture's Smoothing control at maximum reproduces this look, creating flowing rainbow-like gradients that track the original luminance contours of the source image.

### Edge Detection as Contour Overlay

Adding edge detection to a false-color image creates a visualization similar to a topographic map — the flat colored bands represent elevation zones, and the bright edges represent the contour lines between them. Tincture implements a simple horizontal gradient (difference between adjacent pixels) and composites it additively onto the palette-mapped image. This was inspired by the Fairlight CVI's "Sketch" mode, which overlaid edge-detected contours on processed video.

### Palettes as Instruments of Perception

The choice of palette profoundly affects how the viewer reads the image. The Thermal palette (blue-cyan-green-yellow-red-white) follows the conventions of infrared imaging and immediately suggests heat. The X-Ray palette inverts high to low and tints through blue-green, evoking medical radiography. Pop Art uses saturated primaries reminiscent of Warhol screen prints. Night Vision maps through green phosphor tones. Each palette is not just a color scheme but a perceptual lens that reframes the source material.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Gain           (multiply luma by gain/512)
│   ├─ 2. Input Bias           (signed offset, 512 = neutral)
│   ├─ 3. Posterize            (optional 4-bit truncation)
│   ├─ 4. Invert               (optional 1023 - Y)
│   ├─ 5. Band Index           (upper 3 bits → palette band + animation offset)
│   ├─ 6. Palette Lookup       (current band + next band colors)
│   ├─ 7. Smoothing            (interpolate between adjacent band colors)
│   ├─ 8. Saturation Scaling   (UV centered scale by saturation register)
│   ├─ 9. Tint/Replace Mux     (Tint: palette Y + original UV; Replace: palette YUV)
│   ├─ 10. Edge Detection      (|Y[x] - Y[x-1]| << 2, horizontal gradient)
│   └─ 11. Edge Composite      (additive: palette + edge, when enabled)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ Delayed input pipeline  (4-stage delay for tint mode)
│   └─ Saturation / Replace    (see stages 8-9 above)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ interpolator_u × 3      (wet/dry crossfade per channel)
│
└── Sync ───────────────────────────────────────────────────────
    └─ Delayed pass-through    (11-stage shift register)
```

The critical architectural detail is that the palette lookup and the edge detection operate on different stages of the processed luma. Band indexing uses the post-gain, post-bias, post-posterize, post-invert luma, so all four preprocessing steps shape *where* the color boundaries fall. The edge detector, however, operates on the raw difference between the current and previous pixel's processed luma — it measures spatial transitions in the already-remapped signal. This means the edge overlay traces the boundaries between the false-color bands themselves, not the boundaries in the original source.

The Tint versus Replace mode at stage 9 determines whether the palette contributes only luminance (with the original U/V chroma preserved) or full YUV color. In Tint mode the original chrominance shows through the palette's brightness structure, creating a watercolor-like layering effect. In Replace mode the palette completely overrides the source color.

---

## Parameter Reference

<img src={tincture_control_panel} alt="Videomancer front panel with Tincture loaded"/>
*Videomancer's front panel with Tincture active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Palette
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Selects one of eight false-color palettes. Each palette contains eight YUV color entries ordered from shadow to highlight. Thermal follows infrared camera conventions — deep blue shadows through cyan and green midtones to yellow and red highlights with a white peak. Hot Metal burns from black through dark red, red, orange, and yellow to white. X-Ray inverts the mapping, running from white highlights down through blue-green tones to near-black. Pop Art uses saturated primaries in a Warhol-inspired arrangement. Night Vision maps through green phosphor shades. Psychedelic sweeps the full rainbow spectrum. Duotone creates a two-color gradient between blue-teal and orange-red. Ice runs through cold blue-white tones.

---

#### Knob 2 — Band Count
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 2 |

Selects how many distinct color bands divide the luminance range. Four options are available: 4, 5, 6, or 8 bands. Fewer bands create bolder, more graphic results with wider stretches of uniform color. More bands produce finer tonal discrimination, approaching a continuous gradient when combined with high smoothing. The band count interacts directly with the palette: with 4 bands only every other palette entry is used, while 8 bands uses all entries.

---

#### Knob 3 — Input Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Input gain multiplies the luminance signal before palette lookup, with 512 representing unity gain. Below 512, the luma range is compressed — the full palette maps across a narrower portion of the brightness range, and extreme highlights and shadows share the same palette entry. Above 512, the luma range is expanded — the palette spreads across a wider range but the extreme bands may be clipped. This control effectively zooms into or out of the luminance range before color assignment.

---

#### Knob 4 — Input Bias
| Property | Value |
|----------|-------|
| Range | -180.0d – 180.0d |
| Default | 0.2d |
| Suffix | d |

Input bias adds a signed offset to the gained luminance, shifting the entire mapping up or down. At the center position (zero degrees), no offset is applied. Rotating clockwise shifts the mapping so that darker source regions begin to pick up colors normally assigned to brighter zones. Rotating counter-clockwise does the reverse. Combined with input gain, bias lets you precisely target which part of the luminance range receives the most palette variation.

---

#### Knob 5 — Smoothing
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls inter-band smoothing — the interpolation between adjacent palette colors. At 0%, boundaries between color bands are hard and abrupt, producing the flat-banded look of the Fairlight CVI. As you increase smoothing, colors blend gradually across band boundaries. At 100%, the transitions are fully interpolated, creating the flowing gradient look of the NewTek Video Toaster's ChromaFX. The smoothing fraction is derived from the sub-band position of each pixel within its current band.

---

#### Knob 6 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the chrominance intensity of the palette output. At 0%, the palette output is monochrome — only the luminance component of each palette entry is used, regardless of Tint/Replace mode. At the default position the palette colors appear at their designed intensity. Higher values push saturation beyond the palette's natural levels, exaggerating the color differences between bands. This control only affects the U and V channels of the palette lookup output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Tint/Rplc** | Tint | Replace |
| **8 — Invert** | Normal | Invert |
| **9 — Edge Mix** | Off | On |
| **10 — Band Anim** | Off | On |
| **11 — Posterize** | Off | On |

The five toggles control independent binary processing stages. Tint/Replace (Toggle 7) determines how the palette replaces the source video. Invert (Toggle 8) flips the luminance mapping before lookup. Edge Mix (Toggle 9) enables the horizontal edge overlay. Band Anim (Toggle 10) slowly cycles the band offset over time. Posterize (Toggle 11) applies a coarse 4-bit truncation to the luma before band indexing. These can be combined in any configuration — for example, enabling both posterize and invert creates a bold graphic look with reversed tonal order.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 100 |

Controls the wet/dry mix crossfade between the original input signal and the false-color processed output. At 0%, the output is the unprocessed input. At 100%, the output is fully processed. Intermediate positions blend the two signals through the interpolator, allowing subtle palette tinting when blended at low levels.

---

## Guided Exercises

These exercises explore Tincture's palette lookup, smoothing, and edge overlay — from basic false-color mapping to complex multi-stage visual transformations.

### Exercise 1: Thermal Camera Emulation

<img src={tincture_exercise1_result} alt="Thermal Camera Emulation result"/>
*Thermal Camera Emulation — simulated result across source images.*
**Source**: A live camera feed with a person standing in front of a moderately lit background — skin tones and varying brightness areas provide clear palette mapping targets.

**Objective**: Learn how palette selection, band count, and smoothing interact to produce false-color exposure maps.

1. **Default thermal**: With Palette on Thermal and all other controls at default, observe how the source luminance maps to the blue-to-white color spectrum. Shadows appear blue, midtones green-yellow, highlights orange-red-white.
2. **Increase bands**: Sweep Band Count through all four positions. Notice how 4 bands creates bold flat zones while 8 bands reveals finer luminance detail.
3. **Add smoothing**: Increase Smoothing to ~75%. The hard band edges dissolve into flowing color gradients — the Toaster look.
4. **Adjust gain**: Sweep Input Gain above and below center. Above center expands the palette across the luma range; below center compresses it, pushing extremes to the same band.
5. **Shift bias**: Sweep Input Bias to shift which brightness range gets the most palette variation. Target the bias so that skin tones fall in the green-yellow zone.

**Key concepts**: False-color maps luminance to palette color, band count determines tonal resolution, smoothing interpolates between adjacent bands, gain and bias target which luma range gets the most palette variation

---

### Exercise 2: Topographic Contour Map

<img src={tincture_exercise2_result} alt="Topographic Contour Map result"/>
*Topographic Contour Map — simulated result across source images.*
**Source**: Footage with soft gradients — clouds, landscapes, or slowly moving abstract patterns work well to reveal the contour lines.

**Objective**: Combine false-color banding with edge overlay to create topographic map visualizations.

1. **Set up false-color**: Choose the Elevation-like palette (Hot Metal) with 8 bands and Smoothing at 0% for hard band edges.
2. **Enable edge overlay**: Turn on Edge Mix (Toggle 9). Bright contour lines appear at the boundaries between color bands.
3. **Adjust smoothing**: Slowly increase Smoothing. Watch how the contour lines track the blending boundaries — they remain visible but soften.
4. **Try invert**: Toggle Invert to flip the mapping. The contour lines remain at the same spatial positions but the color assignments reverse.
5. **Enable band animation**: Turn on Band Anim. Watch the contour lines shift position as the band boundaries scroll through the luminance range, creating a slowly evolving topographic map.

**Key concepts**: Edge detection traces band boundaries not source edges, contour lines persist through smoothing changes, band animation creates time-varying contour maps

---

### Exercise 3: Psychedelic Poster Art

<img src={tincture_exercise3_result} alt="Psychedelic Poster Art result"/>
*Psychedelic Poster Art — simulated result across source images.*
**Source**: High-contrast footage with bold shapes — silhouettes, architectural subjects, or graphics with strong tonal separation.

**Objective**: Use posterize, invert, and saturated palettes together for bold graphic poster effects.

1. **Enable posterize**: Turn on Posterize (Toggle 11) to coarsen the luminance into 16 hard steps before band indexing.
2. **Select Pop Art palette**: Switch to the Pop Art palette for vivid primary colors.
3. **Reduce bands**: Set Band Count to 4 Bands for the boldest color blocks.
4. **Kill smoothing**: Ensure Smoothing is at 0% for hard flat bands.
5. **Invert**: Toggle Invert on. The color assignment reverses, creating unexpected combinations.
6. **Boost saturation**: Push Saturation above 75% to intensify the palette colors.
7. **Switch to Tint mode**: Flip Tint/Rplc to Tint. The original chroma bleeds through the palette's luminance — the bold luma structure remains but with the source's natural color underneath.

**Key concepts**: Posterize reduces luma to 16 levels before palette lookup creating chunky blocks, Tint mode preserves source chroma while applying palette luminance, fewer bands with zero smoothing produces the boldest graphic separations

---


## Tips

- **Gain and bias are the zoom controls**: Think of Input Gain as a zoom on the luminance range and Input Bias as a pan. Together they let you precisely target which portion of the brightness spectrum gets the most palette variation.
- **Smoothing defines the era**: Zero smoothing = Fairlight CVI's hard 1980s digital look. Full smoothing = NewTek Video Toaster's fluid 1990s ChromaFX aesthetic. The midpoint blends both.
- **Tint mode for subtlety**: When Replace mode feels too aggressive, Tint mode layers the palette's luminance structure over the original chrominance, creating a translucent false-color wash.
- **Edge overlay is additive**: The edge contour lines add brightness to the palette output. On dark palette bands the contours are clearly visible; on bright bands they can push to clipping. Reduce Saturation to make contours more prominent.
- **Posterize amplifies banding**: Enabling Posterize before the palette lookup creates wider flat zones that coarsen the false-color effect. Combined with 4 bands and no smoothing, this produces the boldest possible graphic separations.
- **Feedback loops**: Route the output back into the input to create recursive palette lookups — the false-color mapping is re-applied to its own output, producing layered banding patterns.
- **Animation is slow and subtle**: Band Anim cycles at field rate through 8 offset positions. Use it for gentle evolving color shifts on static or slow-moving sources rather than rapid visual effects.

---

## Glossary

| Term | Definition |
|------|------------|
| **Band** | A contiguous range of luminance values that maps to a single palette color entry. |
| **Bias** | A signed constant added to the luma signal to shift the mapping range up or down before palette lookup. |
| **BT.601** | ITU-R Recommendation BT.601; the color encoding standard used in Videomancer's YUV video pipeline. |
| **ChromaFX** | NewTek Video Toaster's false-color palette mapping effect, known for smooth inter-band gradients. |
| **CVI** | Fairlight Computer Video Instrument; an Australian video synthesizer featuring hard-banded false-color modes. |
| **Edge Detection** | Computing the spatial gradient (difference between adjacent pixel values) to find boundaries. |
| **False-Color** | A visualization technique that maps a single data channel (here, luminance) to a multi-color palette. |
| **Gain** | A multiplicative scaling factor applied to the luminance signal before palette lookup. |
| **Interpolation** | Blending between two values based on a fractional position; used for smooth band transitions. |
| **Palette** | An ordered set of YUV color entries indexed by quantized luminance band. |
| **Posterize** | Reducing the number of distinct levels in a signal by truncating lower bits. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage for contrast and brightness adjustment. |
| **Smoothing** | Interpolation between adjacent palette entries to soften band boundaries. |
| **Tint Mode** | A blending mode where only the palette's luminance component is used, preserving the source's original chrominance. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |
