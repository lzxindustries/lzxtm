---
draft: true
sidebar_position: 14
slug: /instruments/videomancer/barcode
title: "Barcode"
image: /img/instruments/videomancer/barcode/barcode_hero.png
---

import barcode_hero from '/img/instruments/videomancer/barcode/barcode_hero.png';
import barcode_before_after from '/img/instruments/videomancer/barcode/barcode_before_after.png';
import barcode_control_panel from '/img/instruments/videomancer/barcode/barcode_control_panel.png';
import barcode_exercise1_result from '/img/instruments/videomancer/barcode/barcode_exercise1_result.png';
import barcode_exercise2_result from '/img/instruments/videomancer/barcode/barcode_exercise2_result.png';
import barcode_exercise3_result from '/img/instruments/videomancer/barcode/barcode_exercise3_result.png';

# Barcode

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={barcode_hero} alt="Barcode hero image"/>
*Barcode rendering a portrait as variable-width vertical stripes with luminance-driven bar density and guard bar framing.*
<img src={barcode_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Barcode applied.*

---

## Overview

Barcodes are a visual language designed for machines — parallel lines of varying width that encode numeric data. Barcode takes that idea and runs it in reverse: instead of reading stripes to produce numbers, it reads the luminance values of a video signal and produces stripes. Every pixel's brightness becomes a bar-or-space decision, and the result is an image that looks like a living, moving barcode.

The program chains four processing stages together — luminance quantization (reducing the number of brightness levels), bar/space rendering (converting quantized values into stripe patterns at configurable widths), color assignment, and output composition with brightness offset, guard bars, and invert. Three interpolators handle wet/dry mixing at the end. The name is literal: the output resembles the barcodes printed on commercial packaging, but the "data" being encoded is the video signal itself.

At moderate settings, the source image remains legible through the stripe pattern — faces, shapes, and motion are visible as density variations in the bars. At extreme settings, the image is reduced to abstract stripe fields where only gross brightness differences survive as changes in bar density.

---

## Background

### What Is a Barcode?

A **barcode** is a machine-readable representation of data using parallel lines (bars) and gaps (spaces) of varying width. The Universal Product Code (UPC) printed on grocery items is the most familiar example: a sequence of black bars and white spaces whose widths encode a 12-digit number. The key principle is that information is carried by the *ratio* of bar and space widths, not by absolute dimensions. Barcode applies this principle to video — the ratio of bar to space at each horizontal position is determined by the source luminance at that position.

### Luminance Quantization

Before rendering bars, the program quantizes the input luminance. Quantization reduces a continuous range of values to a discrete set of levels — like rounding every price to the nearest dollar. In FPGA hardware, this is implemented efficiently as a right-shift followed by a left-shift: shifting right by N bits discards the N least significant bits, and shifting back left restores the original scale but with the fine detail lost. The Levels control selects among four shift amounts (2, 3, 4, or 5 bits), yielding 256, 128, 64, or 32 distinct brightness levels. Fewer levels produce a more stylized, poster-like barcode pattern; more levels preserve finer tonal gradations.

### Bar Width and Spatial Encoding

The bar width parameter controls how many pixels wide each stripe region is. The VHDL divides the pot value by 16 and adds 1, giving a range of 1 to 64 pixels. Within each stripe region, the position modulo the bar width determines whether a pixel is a "bar" (dark, carrying the quantized luminance) or a "space" (white). This is the core encoding mechanism: wider bars at a given position mean higher luminance, narrower bars mean lower luminance — exactly the same principle that drives commercial barcode scanners.

### Guard Bars and Quiet Zones

Real barcodes include structural elements beyond the data bars. **Guard bars** are fixed-width bars at the left and right edges that tell a scanner where the code begins and ends. **Quiet zones** are blank margins outside the guard bars that prevent adjacent visual elements from being misread as data. Barcode implements both: the Guard toggle enables 8-pixel-wide black bars at the horizontal edges (positions 0–7 and 1273–1279), and the Quiet Zone control blanks a configurable margin at the left edge of the frame. These elements reinforce the barcode aesthetic and provide visual framing.

### Orientation Modes

While traditional barcodes are one-dimensional (vertical stripes), modern data encoding uses two-dimensional patterns — QR codes, Data Matrix, and PDF417 all arrange data in a grid. Barcode offers four orientation modes: 1D Vertical (standard barcode stripes), 1D Horizontal (rotated 90 degrees, using vertical position instead of horizontal), 2D Grid (combining horizontal and vertical tests with OR logic — bars appear wherever either axis criterion is met), and Matrix (an alternate 2D combination). These modes transform the same quantized luminance data into fundamentally different spatial patterns.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Position Counters ──────────────
│   ├─ Latch Y, U, V
│   ├─ h_count (0–1279) horizontal position
│   └─ v_count (0–719) vertical position
│
├── Stage 2: Luminance Quantization + Bar Width ──────────────
│   ├─ Shift-based quantize (shift 2/3/4/5 based on Levels)
│   ├─ bar_width = pot/16 + 1 (range 1–64)
│   ├─ Position mod bar_width → bar or space
│   └─ Type select: V uses h_count, H uses v_count,
│      Grid = H OR V, Matrix = alternate
│
├── Stage 3: Bar Draw + Color Assignment ─────────────────────
│   ├─ Bar pixel: Y = quantized luma
│   ├─ Space pixel: Y = 1023 (white)
│   ├─ Contrast adjustment (expand/compress around 512)
│   └─ Color tint: B/W=U512/V512, Red=U400/V700,
│      Blue=U700/V400, Green=U400/V400
│
├── Stage 4: Guard Bars + Brightness + Invert ────────────────
│   ├─ Brightness offset (signed, pot − 512)
│   ├─ Guard bars: 8px black at h<8 or h>1272
│   ├─ Invert: 1023 − Y
│   └─ Output compose
│
├── Interpolator Stage (4 clocks) ────────────────────────────
│   └─ 3× interpolator_u: wet/dry mix (Y, U, V)
│
├── Sync Delay Pipeline ──────────────────────────────────────
│   └─ 8+4 clock delay matching processing latency
│
└── Bypass Mux ───────────────────────────────────────────────
    └─ Select processed or delayed original
```

The critical interaction is between the quantization and bar-draw stages. Quantization reduces the number of distinct luminance values in the image, and the bar-draw stage converts each quantized value into a spatial pattern within the stripe region. Fewer quantization levels mean fewer distinct bar widths, producing a coarser, more stylized result. The bar width control sets the spatial frequency of the stripe pattern independently of the quantization depth — wide bars with fine quantization create broad stripes with many possible densities, while narrow bars with coarse quantization create a rapid switching pattern with few density levels.

---

## Parameter Reference

<img src={barcode_control_panel} alt="Videomancer front panel with Barcode loaded"/>
*Videomancer's front panel with Barcode active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Bar W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the width of each bar stripe region in pixels. The VHDL divides the 10-bit pot value by 16 and adds 1, giving a range of 1 to 64 pixels. At minimum (bar width 1), every pixel is an independent bar — the image becomes a simple quantized version of the source. At maximum (bar width 64), broad stripe regions dominate the frame, and the barcode structure becomes the primary visual element. Intermediate values around 8–16 produce the most classically barcode-like appearance.

---

#### Knob 2 — Levels
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 9 |

Controls the number of quantization levels applied to the luminance channel before bar rendering. Four shift amounts are selected by threshold: pot values above 768 give 256 levels (shift 2), above 512 give 128 levels (shift 3), above 256 give 64 levels (shift 4), and below give 32 levels (shift 5). Fewer levels produce more distinct, poster-like bar density steps. At the coarsest setting, only 32 brightness values survive — the barcode becomes a stark graphic with a small vocabulary of bar widths.

---

#### Knob 3 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the contrast of the rendered bars. The VHDL computes a signed offset from the pot value (divided by 4, minus 128) and applies it asymmetrically — values above mid-gray are pushed brighter, values below are pushed darker. This expands the visual difference between bars and spaces. At minimum contrast, bars and spaces have similar brightness and the barcode pattern is subtle. At maximum, bars are deep black and spaces are bright white, producing the sharpest possible stripe pattern.

---

#### Knob 4 — Spacing
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the amount of white space inserted between bar groups. The spacing value adds pixels of white separation, visually thinning the bar pattern and introducing rhythm to the stripe sequence. At zero, bars fill their full width. As spacing increases, the bars become narrower relative to the spaces, creating an airier, more open pattern. This interacts with bar width — narrow bars with high spacing produce a sparse, delicate barcode, while wide bars with low spacing produce a dense, heavy one.

---

#### Knob 5 — Quiet Zn
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the width of the quiet zone — a blank white margin at the left edge of the frame. In real barcodes, quiet zones are mandatory clearance areas that prevent scanners from misreading adjacent elements. Here, the quiet zone provides visual framing and compositional control. At zero, bars extend to the frame edge. As you increase the control, a progressively wider white border appears at the left, pushing the barcode pattern inward.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies a signed brightness offset to the entire processed signal. The offset is computed as the pot value minus 512, giving a range of −512 to +511. At center (pot = 512), no offset is applied. Turning below center darkens the output; turning above center brightens it. This is applied after contrast and before guard bars and invert, so it shifts the entire tonal range of the barcode uniformly. Use it to match the output level to downstream equipment or to create intentionally over- or under-exposed barcode textures.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Type** | 1D Vert | 1D Horiz |
| **8 — Color** | B/W | Red |
| **9 — Guard** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7 and 8 each use two bits to select among four options — they are multi-position toggles, not simple on/off switches. Switch 7 selects the bar orientation mode (1D Vertical, 1D Horizontal, 2D Grid, Matrix). Switch 8 selects the color scheme (B/W, Red, Blue, Green). Switches 9 and 10 are standard on/off toggles for guard bars and invert respectively. Switch 11 is bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the processed barcode signal and the delay-compensated original. Three interpolator_u instances (one each for Y, U, V) crossfade between the two. At 100% (pot = 1023), the output is fully processed barcode. At 0%, the output is the original signal. Intermediate values blend the barcode pattern over the source, creating a ghostly overlay where the stripe structure is visible but the original image shows through.

---

## Guided Exercises

These exercises progress from basic vertical barcode rendering through spatial modes and color options to full compositional control. Each exercise produces a visually distinct result.

### Exercise 1: Classic Barcode

<img src={barcode_exercise1_result} alt="Classic Barcode result"/>
*Classic Barcode — simulated result across source images.*
**Source**: A portrait or image with a broad range of tones — skin, hair, background.

**Objective**: Learn how bar width and quantization interact to produce recognizable vertical barcode patterns.

1. **Start simple**: Set Bar W to ~30%, Levels to mid-position, all toggles off except Guard on. You should see vertical stripes of varying density corresponding to the brightness regions of the source.
2. **Adjust bar width**: Sweep Bar W from minimum to maximum. At minimum, the image is almost its normal self (just quantized). At maximum, thick stripes dominate and fine detail disappears.
3. **Change quantization**: Sweep Levels from maximum to minimum. Watch the number of distinct stripe widths decrease — the barcode vocabulary shrinks from 256 levels to 32.
4. **Add contrast**: Increase Contrast to sharpen the difference between bars and spaces. The barcode becomes more graphic and machine-readable.
5. **Enable guard bars**: Toggle Guard on. Black reference bars frame the left and right edges, completing the barcode format.

**Key concepts**: Bar width sets spatial frequency, quantization sets the vocabulary of bar densities, contrast sharpens the bar/space distinction, guard bars provide structural framing

---

### Exercise 2: Color Grid Pattern

<img src={barcode_exercise2_result} alt="Color Grid Pattern result"/>
*Color Grid Pattern — simulated result across source images.*
**Source**: An image with strong color variation — macaws, fruit, or geometric patterns.

**Objective**: Explore 2D grid mode and color tinting to create crosshatch barcode patterns.

1. **2D Grid mode**: Set Type to 2D Grid. Bars appear on both horizontal and vertical axes, creating a crosshatch pattern.
2. **Color tint**: Switch Color from B/W to Red. The bars take on a warm tint. Try Blue and Green as well — each creates a different mood.
3. **Spacing**: Increase Spacing to open up the grid. The crosshatch pattern becomes more airy, with wider white gaps between bars.
4. **Quiet zone**: Add a quiet zone (~30%) to observe how the left margin blanks to white, framing the active barcode area.
5. **Invert**: Toggle Invert to see the color-negative grid — white bars on a dark, tinted background.

**Key concepts**: 2D Grid combines horizontal and vertical bar tests with OR logic, color tinting applies uniform chrominance to all bars, spacing controls bar-to-space ratio, invert swaps the polarity of the entire pattern

---

### Exercise 3: Barcode Overlay

<img src={barcode_exercise3_result} alt="Barcode Overlay result"/>
*Barcode Overlay — simulated result across source images.*
**Source**: Any footage with movement — performers, nature, or abstract video feedback.

**Objective**: Use the wet/dry mix to blend barcode patterns over the source as a compositional overlay.

1. **Set up barcode**: Configure a strong 1D Vertical barcode with moderate bar width (~20%), high contrast, guard bars on, B/W color.
2. **Reduce mix**: Lower the Mix fader to ~50%. The barcode pattern becomes translucent over the original image. The source subjects are visible beneath the stripe pattern.
3. **Horizontal mode**: Switch Type to 1D Horiz. The overlay changes to horizontal stripes, creating a venetian-blind effect over the source.
4. **Brightness offset**: Adjust Bright to shift the barcode tonal range — darkening the overlay makes it more subtle, brightening makes it more intrusive.
5. **Animate**: Slowly sweep Bar W while the mix is at ~50%. The stripe frequency changes smoothly, creating a scanning or shimmering overlay effect.

**Key concepts**: The wet/dry mix blends processed and original signals via interpolation, mixing below 100% creates transparent overlays, brightness offset shifts the overlay density, sweeping parameters during mix creates animated textures

---


## Tips

- **Bar width sets the character**: Values around 4–12 produce the most recognizable barcode patterns. Wider bars become abstract stripes; width 1 is just luminance quantization.
- **Quantization is the vocabulary**: Fewer levels create a more dramatic, graphic-poster barcode. More levels create subtle density variations that read almost like halftone printing.
- **Guard bars complete the illusion**: Enable Guard to add the start/stop markers that make the output look like a real barcode format. Combined with Quiet Zone, the result is compositionally framed.
- **Color tinting is instant drama**: Switching from B/W to Red or Blue creates an immediate visual transformation with no luminance change — useful for live performance transitions.
- **Mix for layering**: At 40–60% mix, the barcode becomes a transparent texture overlay. This is particularly effective when the source has strong motion — the bars shimmer with the movement.
- **Invert for negative barcodes**: White bars on dark backgrounds have a completely different visual weight. Combined with color tinting, invert produces rich color-negative barcode patterns.
- **Horizontal mode for scanlines**: 1D Horiz creates horizontal stripe patterns that evoke CRT scanlines or venetian blinds. Combined with narrow bar width and low contrast, this produces subtle raster-line textures.
- **Feedback loops**: Route the output back to the input for recursive barcode encoding — the already-barcode signal gets re-encoded, creating fractal-like stripe nesting.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bypass mux** | A multiplexer that routes the original signal past all processing stages for instant A/B comparison. |
| **Chrominance** | The color-difference components (U and V) of a YUV video signal, separate from luminance. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline in hardware. |
| **Guard bar** | A fixed-width reference bar at the edge of a barcode that marks where the data region begins or ends. |
| **Interpolator** | A hardware module that performs linear crossfading between two signals (wet and dry) based on a mix parameter. |
| **Luminance** | The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color. |
| **Quantization** | Reducing a continuous range of values to a finite set of discrete levels, here applied to luminance before bar rendering. |
| **Quiet zone** | A mandatory blank margin adjacent to a barcode that prevents nearby visual elements from being misread as data. |
| **UPC** | Universal Product Code; the most common one-dimensional barcode symbology, printed on retail packaging worldwide. |
| **Wet/dry mix** | A crossfade between the processed (wet) and original (dry) signals, controlling effect intensity. |
| **YUV** | A color encoding that separates luminance (Y) from two chrominance components (U and V), used in broadcast video. |

---
