---
draft: true
sidebar_position: 102
slug: /instruments/videomancer/enhance
title: "Enhance"
image: /img/instruments/videomancer/enhance/enhance_hero_s1.png
description: "Every crime drama fan knows the scene: a detective peers at a grainy security camera still and commands the lab technician to \"enhance.\" The image zooms impossibly close, pixelated detail sharpens into clarity, and the killer's face appears in a reflection on a doorknob."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import enhance_source1_fruit from '/img/instruments/videomancer/enhance/enhance_source1_fruit.png';
import enhance_source2_runner from '/img/instruments/videomancer/enhance/enhance_source2_runner.png';
import enhance_source3_elephant from '/img/instruments/videomancer/enhance/enhance_source3_elephant.png';
import enhance_source4_pattern from '/img/instruments/videomancer/enhance/enhance_source4_pattern.png';
import enhance_source5_woman from '/img/instruments/videomancer/enhance/enhance_source5_woman.png';
import enhance_source6_paint from '/img/instruments/videomancer/enhance/enhance_source6_paint.png';
import enhance_hero_s1 from '/img/instruments/videomancer/enhance/enhance_hero_s1.png';
import enhance_hero_s2 from '/img/instruments/videomancer/enhance/enhance_hero_s2.png';
import enhance_hero_s3 from '/img/instruments/videomancer/enhance/enhance_hero_s3.png';
import enhance_hero_s4 from '/img/instruments/videomancer/enhance/enhance_hero_s4.png';
import enhance_hero_s5 from '/img/instruments/videomancer/enhance/enhance_hero_s5.png';
import enhance_hero_s6 from '/img/instruments/videomancer/enhance/enhance_hero_s6.png';
import enhance_ex1_s1 from '/img/instruments/videomancer/enhance/enhance_ex1_s1.png';
import enhance_ex1_s2 from '/img/instruments/videomancer/enhance/enhance_ex1_s2.png';
import enhance_ex1_s3 from '/img/instruments/videomancer/enhance/enhance_ex1_s3.png';
import enhance_ex1_s4 from '/img/instruments/videomancer/enhance/enhance_ex1_s4.png';
import enhance_ex1_s5 from '/img/instruments/videomancer/enhance/enhance_ex1_s5.png';
import enhance_ex1_s6 from '/img/instruments/videomancer/enhance/enhance_ex1_s6.png';
import enhance_ex2_s1 from '/img/instruments/videomancer/enhance/enhance_ex2_s1.png';
import enhance_ex2_s2 from '/img/instruments/videomancer/enhance/enhance_ex2_s2.png';
import enhance_ex2_s3 from '/img/instruments/videomancer/enhance/enhance_ex2_s3.png';
import enhance_ex2_s4 from '/img/instruments/videomancer/enhance/enhance_ex2_s4.png';
import enhance_ex2_s5 from '/img/instruments/videomancer/enhance/enhance_ex2_s5.png';
import enhance_ex2_s6 from '/img/instruments/videomancer/enhance/enhance_ex2_s6.png';
import enhance_ex3_s1 from '/img/instruments/videomancer/enhance/enhance_ex3_s1.png';
import enhance_ex3_s2 from '/img/instruments/videomancer/enhance/enhance_ex3_s2.png';
import enhance_ex3_s3 from '/img/instruments/videomancer/enhance/enhance_ex3_s3.png';
import enhance_ex3_s4 from '/img/instruments/videomancer/enhance/enhance_ex3_s4.png';
import enhance_ex3_s5 from '/img/instruments/videomancer/enhance/enhance_ex3_s5.png';
import enhance_ex3_s6 from '/img/instruments/videomancer/enhance/enhance_ex3_s6.png';

# Enhance

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: enhance_source1_fruit, after: enhance_hero_s1 },
    { label: "Runner", before: enhance_source2_runner, after: enhance_hero_s2 },
    { label: "Elephant", before: enhance_source3_elephant, after: enhance_hero_s3 },
    { label: "Pattern", before: enhance_source4_pattern, after: enhance_hero_s4 },
    { label: "Woman", before: enhance_source5_woman, after: enhance_hero_s5 },
    { label: "Paint", before: enhance_source6_paint, after: enhance_hero_s6 },
  ]}
/>
*Enhance applying 4× pixel replication zoom and false-color thermal palette to a surveillance-style Region of Interest.*

---

## Overview

Every crime drama fan knows the scene: a detective peers at a grainy security camera still and commands the lab technician to "enhance." The image zooms impossibly close, pixelated detail sharpens into clarity, and the killer's face appears in a reflection on a doorknob. Enhance is Videomancer's tribute to that beloved fiction — and a genuinely useful forensic magnification tool.

The program defines a rectangular Region of Interest (ROI) on the incoming video and applies pixel-level magnification within that window. Inside the ROI, the luma channel is read from a line buffer at a divided address rate, producing blocky pixel replication at 2× or 4× magnification. A histogram contrast stretch expands the luma range by shifting pixel values away from a center point and clamping the result. An optional false-color thermal palette remaps the stretched luminance to a four-zone surveillance colormap — blue for dark, green for low, yellow for mid, red for hot. A bright 2-pixel border outlines the ROI, and an animated scan line sweeps vertically through the region, completing the forensic-display aesthetic.

Outside the ROI, the original video passes through unmodified. The result is a picture-in-picture magnification window that selectively enlarges and recolors part of the frame while preserving the full context around it.

---

## Background

### The CSI "Enhance" Trope

The fictional "enhance" command has appeared in crime procedurals since the 1980s, from *Blade Runner*'s Esper machine to *CSI*'s omniscient lab computers. In reality, digital zoom cannot create detail that was never captured — magnifying a low-resolution image merely makes the pixels bigger. Enhance leans into this truth: its pixel replication zoom makes the blocky, discrete nature of the magnification explicitly visible, turning the gap between fiction and physics into a visual feature. The name is a direct, playful homage to the trope.

### Pixel Replication Zoom

Pixel replication is the simplest form of image magnification. Each source pixel is duplicated two or four times in the output, producing uniform blocks of color. Unlike interpolation-based upscaling (bilinear, bicubic), pixel replication introduces no new values and no blurring — the zoomed image is a faithful, if blocky, representation of the original sample grid. In hardware, this is implemented by dividing the line-buffer read address by the zoom factor: reading address N/2 instead of N makes each stored pixel appear twice on the output scanline.

### Histographic Contrast Stretch

Real forensic analysts use contrast stretching to reveal faint detail in under-exposed surveillance footage. The technique remaps a narrow band of input values to the full output range, expanding tonal differences. Enhance implements a simplified version: the luma value is offset from a center point (256 in 10-bit space), multiplied by a power-of-two gain (1×, 2×, 4×, or 8×), and then re-centered and clamped. Values near the center expand outward; values at the extremes clip to black or white. At high stretch settings, the image becomes a stark, high-contrast rendering that exaggerates tonal differences in the zoomed region.

### False-Color Thermography

Thermal cameras map invisible infrared radiation to visible color palettes so that temperature differences become immediately apparent. Enhance borrows this visualization technique, mapping the four quarters of the 10-bit luma range to distinct hues: dark values turn blue, low values turn green, mid values turn yellow, and bright values turn red. The result resembles a thermal or night-vision overlay, transforming ordinary video into a surveillance-aesthetic display that makes tonal structure instantly readable.

### Region of Interest Processing

ROI-based processing is fundamental to machine vision, medical imaging, and video surveillance. Rather than processing the entire frame, the system selects a rectangular sub-region and applies enhanced analysis only within that window. Enhance computes ROI boundaries from three parameters — horizontal position, vertical position, and size — and evaluates every pixel against those boundaries on every clock cycle. Inside the region, the full processing chain (zoom, stretch, false color) applies. Outside the region, the signal passes through unchanged, providing context for the magnified detail.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ Horizontal pixel counter (hsync reset)
│   ├─ Vertical line counter (vsync reset, hsync increment)
│   └─ Animated scan line position (vsync increment, wraps at ROI bottom)
│
├── ROI Boundary Computation ───────────────────────────────────
│   ├─ width      = (roi_size >> 1) + 64
│   ├─ roi_left   = roi_x_pos + 32
│   ├─ roi_right  = roi_left + width
│   ├─ roi_top    = (roi_y_pos >> 1) + 16
│   └─ roi_bottom = roi_top + (width >> 1)
│
├── Stage 1: Input Register + ROI Detection ────────────────────
│   ├─ Register Y, U, V
│   ├─ in_roi_h  = h_count in [roi_left, roi_right)
│   ├─ in_roi_v  = v_count in [roi_top, roi_bottom)
│   ├─ in_roi    = in_roi_h AND in_roi_v
│   └─ on_border = 2-pixel edge detection on ROI perimeter
│
├── Line Buffer Write ──────────────────────────────────────────
│   └─ Write input Y to buffer at h_count every active pixel
│
├── Stage 2: Zoom Address Compute ──────────────────────────────
│   ├─ offset = h_count − roi_left
│   ├─ 2× mode: rd_addr = roi_left + (offset >> 1)
│   └─ 4× mode: rd_addr = roi_left + (offset >> 2)
│
├── Stages 3–4: BRAM Read Latency ─────────────────────────────
│   └─ 2 pipeline register stages (BRAM output delay)
│
├── Stage 5: Contrast Stretch + False Color ────────────────────
│   ├─ Zoomed Y from line buffer readback
│   ├─ Contrast: (Y − 256) << shift + 256, clamp [0, 1023]
│   ├─ False Color zone (by raw zoomed Y[9:8]):
│   │   00 dark  → (Y/2, U=700, V=350) blue
│   │   01 low   → (Y,   U=350, V=350) green
│   │   10 mid   → (Y,   U=400, V=600) yellow
│   │   11 hot   → (Y,   U=512, V=800) red
│   └─ Scan line detect: v_count == scan_line AND in_roi
│
├── Stage 6: Composite ────────────────────────────────────────
│   ├─ Border active   → (border_brt, 512, 512) achromatic
│   ├─ Scan line active → (border_brt, 512, 600) slight warm tint
│   ├─ Inside ROI      → (fc_y, fc_u, fc_v) processed
│   └─ Outside ROI     → (original Y, U, V) pass-through
│
├── Interpolator Mix (4 clocks) ────────────────────────────────
│   └─ lerp(delayed_dry, wet, mix_amount) × 3 channels
│
└── Output ─────────────────────────────────────────────────────
    └─ Bypass mux: if bypass then delayed-original else mixed
```

Two important characteristics define the processing path. First, only the Y (luma) channel passes through the line buffer for zoom — the U and V (chroma) channels pipeline through without replication. When false color is off, the zoomed ROI shows magnified brightness at original chroma resolution, creating a subtle luma-chroma resolution split. When false color is on, the chroma channels are replaced entirely by the thermal palette constants, so this split disappears. Second, the false-color zone assignment uses the *raw* zoomed Y value (bits [9:8] of the line buffer output), while the *intensity* within each zone uses the contrast-stretched Y. This means contrast stretching affects how bright each zone appears but does not change which zone a pixel belongs to — zone boundaries remain fixed at Y=256, 512, and 768 regardless of the stretch setting.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Zoom
| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 5 |

Controls the horizontal position of the ROI rectangle. At the fully counter-clockwise position, the magnification window sits near the left edge of the frame. Turning clockwise sweeps the ROI rightward across the video. In the VHDL, this register value plus a 32-pixel margin sets the left boundary, keeping the window within the active picture area. Combined with the vertical position control, this knob navigates the zoom window to any region of the input frame.

---

#### Knob 2 — ROI X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the vertical position of the ROI rectangle. The register value is halved before mapping to line coordinates, so the vertical sweep range is inherently finer than the horizontal — the vertical position moves at a more controlled rate. At the counter-clockwise extreme, the ROI sits near the top of the frame; turning clockwise moves it downward. A 16-pixel offset keeps the window within the active picture.

---

#### Knob 3 — ROI Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the size of the ROI rectangle. The register value maps to a width ranging from about 64 pixels (fully counter-clockwise) to several hundred pixels (fully clockwise). The ROI height is always half the width, creating a landscape-oriented window. At small sizes with 4× zoom, the magnification window shows a very tight crop of the source with highly visible pixel blocks. At large sizes, the ROI covers a significant portion of the frame and the zoomed blocks are less dramatic.

---

#### Knob 4 — Stretch
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for zoom level fine-tuning. In the current hardware implementation, the zoom magnification is set discretely by the Mode toggle (2× or 4×), and this register is declared but not referenced by the processing pipeline. Future firmware revisions may use this parameter to provide continuously variable zoom between the discrete detents.

---

#### Knob 5 — Sharpen
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the histogram contrast stretch intensity. The 10-bit register value maps to four discrete shift levels: 0–255 produces no stretch (1×), 256–511 produces 2× expansion, 512–767 produces 4× expansion, and 768–1023 produces 8× expansion. The stretch formula subtracts a center offset of 256 from the zoomed luma, applies the power-of-two multiplication, re-centers, and clamps to the 0–1023 range. Higher settings push subtle tonal differences into dramatic high-contrast imagery, simulating the histogram equalization tools used in forensic video analysis.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness of the ROI border and the animated scan line. Both overlay elements use this register value directly as their Y (luma) component, with chroma set to neutral. At 0, the border and scan line are invisible (black); at 1023, they are full-intensity bright white. The scan line shares this brightness but receives a slight warm tint from a chroma V offset of 600 (above the 512 neutral point), distinguishing it visually from the achromatic border.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Zoom | Stretch |
| **8 — Palette** | Normal | Thermal |
| **9 — Grid** | Off | On |
| **10 — PIP** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options in the processing pipeline. Mode selects between 2× and 4× pixel replication zoom. Palette enables or disables false-color thermographic rendering within the ROI. Grid switches the bright ROI border rectangle on and off. PIP activates the animated vertical scan line that sweeps through the ROI once per field. Bypass routes the original signal directly to the output. Each toggle acts independently — none are mutually exclusive, and any combination is valid.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed output (zoomed, stretched, false-colored) and the delayed original signal. At 0%, only the unprocessed original is visible — the ROI, border, and all effects are suppressed. At 100%, the full processing chain output is displayed. Intermediate settings blend the two, creating a translucent overlay effect where the ROI zoom appears semi-transparent against the source. The crossfade operates per-channel on all three YUV components simultaneously via three parallel interpolator instances.

---

## Guided Exercises

Three exercises build from basic ROI navigation through contrast stretching to the full forensic display with false color and animated scanning.

### Exercise 1: ROI Navigation and Pixel Zoom

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: enhance_source1_fruit, after: enhance_ex1_s1 },
    { label: "Runner", before: enhance_source2_runner, after: enhance_ex1_s2 },
    { label: "Elephant", before: enhance_source3_elephant, after: enhance_ex1_s3 },
    { label: "Pattern", before: enhance_source4_pattern, after: enhance_ex1_s4 },
    { label: "Woman", before: enhance_source5_woman, after: enhance_ex1_s5 },
    { label: "Paint", before: enhance_source6_paint, after: enhance_ex1_s6 },
  ]}
/>
*ROI Navigation and Pixel Zoom — simulated result across source images.*
**Source**: A live camera feed or recorded footage with readable text and fine details — signs, printed pages, circuit boards, or textured fabrics.

**Objective**: Learn how the ROI window navigates the frame and how pixel replication zoom produces blocky magnification.

1. **Find the ROI**: With default settings and Grid enabled, locate the bordered rectangle in the frame.
2. **Move horizontally**: Sweep the Zoom knob left and right to slide the ROI across the frame.
3. **Move vertically**: Sweep the ROI X knob to move the ROI up and down.
4. **Resize**: Turn ROI Y counter-clockwise for a tiny window, then clockwise for a large one. Notice how the height is always half the width.
5. **Compare zoom levels**: Toggle Mode to switch between 2× and 4×. At 4×, each pixel becomes a clearly visible square block and the source crop is tighter.
6. **Border visibility**: Adjust Brightness to control border intensity — dim for subtle framing, bright for maximum visibility.

**Key concepts**: ROI position is controlled by two independent knobs, ROI height is half its width, pixel replication creates blocky magnification without interpolation, 4× shows fewer source pixels than 2×

---

### Exercise 2: Contrast Stretch and Detail Enhancement

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: enhance_source1_fruit, after: enhance_ex2_s1 },
    { label: "Runner", before: enhance_source2_runner, after: enhance_ex2_s2 },
    { label: "Elephant", before: enhance_source3_elephant, after: enhance_ex2_s3 },
    { label: "Pattern", before: enhance_source4_pattern, after: enhance_ex2_s4 },
    { label: "Woman", before: enhance_source5_woman, after: enhance_ex2_s5 },
    { label: "Paint", before: enhance_source6_paint, after: enhance_ex2_s6 },
  ]}
/>
*Contrast Stretch and Detail Enhancement — simulated result across source images.*
**Source**: Under-exposed or low-contrast footage — dimly lit interiors, foggy scenes, or washed-out exteriors with subtle tonal variation.

**Objective**: Explore how histogram stretching brings out hidden tonal detail within the zoomed ROI.

1. **Position the ROI** over an area with subtle tonal variation (shadows, fabric texture, foliage).
2. **Enable 2× zoom** (Mode in first position) for moderate magnification.
3. **Sweep contrast**: Slowly turn Sharpen clockwise. In the first quarter, no stretch — the zoom is clean. In the second quarter, 2× stretch makes shadows slightly darker and highlights brighter. Past the midpoint, 4× stretch produces a dramatic contrasty image. In the last quarter, 8× stretch pushes most values to pure black or white.
4. **Before/after**: Toggle Bypass to compare the stretched ROI against the raw footage. Note tonal details that were invisible before stretching.
5. **Mix overlay**: Set Mix to ~50% to superimpose the stretched ROI semi-transparently over the original, creating a ghostly forensic overlay that reveals enhanced detail in context.

**Key concepts**: Contrast stretch multiplies tonal deviation from a center point by a power of two, higher stretch creates harder contrast, the stretch operates on the zoomed (pixel-replicated) Y so each block stretches uniformly

---

### Exercise 3: Full Forensic Display

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: enhance_source1_fruit, after: enhance_ex3_s1 },
    { label: "Runner", before: enhance_source2_runner, after: enhance_ex3_s2 },
    { label: "Elephant", before: enhance_source3_elephant, after: enhance_ex3_s3 },
    { label: "Pattern", before: enhance_source4_pattern, after: enhance_ex3_s4 },
    { label: "Woman", before: enhance_source5_woman, after: enhance_ex3_s5 },
    { label: "Paint", before: enhance_source6_paint, after: enhance_ex3_s6 },
  ]}
/>
*Full Forensic Display — simulated result across source images.*
**Source**: Any video content — the more mundane the better, as the forensic aesthetic transforms ordinary footage into dramatic surveillance-style analysis imagery.

**Objective**: Combine all features for the complete CSI "enhance" experience: zoom, stretch, false color, border, and animated scan line.

1. **Position and size the ROI** over a region of interest in the incoming video.
2. **Set 4× zoom**: Toggle Mode to the second position for maximum blockiness.
3. **Moderate contrast**: Set Sharpen to ~50% for visible contrast expansion without total clipping.
4. **Enable false color**: Toggle Palette on. The ROI transforms into a thermal-style display — darks turn blue, mids turn green or yellow, brights turn red.
5. **Frame it**: Enable Grid and set Brightness to ~80% for a bright white border outline.
6. **Start scanning**: Enable PIP. A bright horizontal stripe slowly descends through the ROI, one line per field.
7. **Full display**: Observe the complete effect — a blocky, false-colored, contrast-stretched surveillance window bordered by a bright outline with a scanning highlight.
8. **Context blend**: Lower Mix to ~70% to see the original video ghosting through behind the forensic overlay, creating a layered, translucent analysis display.

**Key concepts**: False color replaces chroma with zone-based thermal palette mapped from luma, border and scan line share the Brightness control, scan line tint is slightly warm compared to the achromatic border, mix crossfade blends all processed elements simultaneously

---


## Tips

- **Y-only zoom**: Pixel replication applies to the Y channel only. Without false color, the zoomed ROI shows magnified brightness at original chroma resolution — a deliberately forensic look that emphasizes tonal structure over color.
- **Mix as overlay**: At 50% mix, the ROI effect becomes a translucent overlay. This is useful for seeing both the enhanced detail and the original context simultaneously, similar to heads-up display compositing.
- **Stretch as edge finder**: At 8× contrast shift, only the strongest tonal transitions survive the clipping. The ROI becomes a crude edge detector, highlighting boundaries while crushing everything else to black or white.
- **False color for exposure checking**: The four-zone thermal palette instantly reveals the tonal distribution of the source — if the ROI is mostly blue, the area is underexposed; if mostly red, it is clipping.
- **Border before navigating**: Enable Grid before moving the ROI so you can see exactly where the magnification window sits against the full frame.
- **Scan speed varies with ROI height**: The animation advances one line per video field, so it sweeps a small ROI in under a second but takes several seconds for a large one.
- **Bypass for A/B**: Use Bypass rather than sweeping Mix for instant before/after comparison with no crossfade transition period.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory inside the FPGA used for the video line buffer that stores luma for zoom readback. |
| **Chroma** | The color information (U and V components) in a YUV video signal, encoding hue and saturation. |
| **Contrast Stretch** | Expanding a narrow range of pixel values to the full output range by multiplying deviation from a center point, increasing tonal separation. |
| **False Color** | Mapping monochrome intensity values to a multi-hue palette for visual analysis, borrowed from thermal imaging. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline in dedicated hardware. |
| **Histogram** | A distribution showing how many pixels occupy each brightness level; contrast stretching reshapes this distribution. |
| **Line Buffer** | A BRAM-based memory that stores one horizontal line of pixel data for delayed readback at modified addresses. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | Sequential processing stages where each stage's output feeds the next on every clock cycle. |
| **Pixel Replication** | Duplicating each source pixel multiple times to create blocky magnification without interpolation or blurring. |
| **ROI** | Region of Interest; a user-defined rectangular sub-area of the frame where enhanced processing is applied. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
