---
draft: true
sidebar_position: 82
slug: /instruments/videomancer/dolly
title: "Dolly"
image: /img/instruments/videomancer/dolly/dolly_hero.png
description: "Every broadcast control room has a button that shrinks the on-screen talent into a box and slides that box to any corner of the frame — usually to make room for a map, a graphic, or a second camera feed."
---

import dolly_hero from '/img/instruments/videomancer/dolly/dolly_hero.png';
import dolly_before_after from '/img/instruments/videomancer/dolly/dolly_before_after.png';
import dolly_control_panel from '/img/instruments/videomancer/dolly/dolly_control_panel.png';
import dolly_exercise1_result from '/img/instruments/videomancer/dolly/dolly_exercise1_result.png';
import dolly_exercise2_result from '/img/instruments/videomancer/dolly/dolly_exercise2_result.png';
import dolly_exercise3_result from '/img/instruments/videomancer/dolly/dolly_exercise3_result.png';

# Dolly

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={dolly_hero} alt="Dolly hero image"/>
*Dolly repositioning and scaling a live camera feed within a colored background frame, demonstrating picture-in-picture composition.*
<img src={dolly_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Dolly applied.*

---

## Overview

Every broadcast control room has a button that shrinks the on-screen talent into a box and slides that box to any corner of the frame — usually to make room for a map, a graphic, or a second camera feed. In the television industry, this operation is called a DVE: a Digital Video Effect. Dolly distills the DVE to its essential geometry: position, size, and aspect ratio, wrapped in a configurable border and background.

The name comes from the camera dolly — the wheeled platform that moves a camera through space. A physical dolly changes the camera's relationship to the scene; Dolly changes the image's relationship to the frame. Where a camera dolly moves through three-dimensional space, the program moves the picture across a two-dimensional output raster, scaling it along the way.

At default settings (Size at 0%, Position X and Y centered, Aspect centered), the image fills the entire frame with no border or background visible. As you increase Size, the image shrinks toward a point. Position X and Y slide the shrunken image anywhere within the output raster. Aspect stretches or compresses the image horizontally. Border Width frames the image rectangle in white or black. The background behind everything is a solid color whose hue you can sweep through the full spectrum.

---

## Background

### Digital Video Effects and the DVE

The term DVE originally referred to dedicated hardware units — room-filling machines that could resize, reposition, rotate, and perspective-warp a live video signal in real time. The first commercial DVE was the Quantel DPE 5000, introduced in 1977, which could squeeze, zoom, and slide a picture within the broadcast frame. By the early 1980s, every major broadcast facility owned at least one DVE unit, and the picture-in-picture insert became a visual signature of news and sports television. Dolly implements the core geometric operation that made all of those effects possible: raster-domain scaling and repositioning using a per-pixel address generator.

### Picture-in-Picture Composition

The simplest DVE application is picture-in-picture (PiP): one image shown inside another. The technique requires three simultaneous decisions for every output pixel: Is this pixel part of the inset image? Is it part of the border frame? Or is it part of the background? Dolly answers that question with a region classifier that evaluates the current pixel coordinates against the computed image rectangle and border rectangle every clock cycle. This three-way classification — image, border, background — is the foundation of all broadcast graphics compositing.

### The Digital Differential Analyzer

Horizontal scaling in hardware requires generating a fractional read address for every output pixel. Dolly uses a DDA — a Digital Differential Analyzer — to solve this. The DDA maintains a fixed-point accumulator that advances by a computed step value for each pixel within the image region. The integer part of the accumulator becomes the read address into the line buffer. When the step is less than unity (image wider than source), source pixels repeat. When the step is greater than unity (image narrower than source), source pixels are skipped. The result is arbitrary horizontal scaling without multiplication per pixel — just one addition per clock cycle.

### Line Buffer Architecture

Scaling requires random access to the current scanline's pixel data. Dolly stores each incoming line in a dual-port BRAM (Block RAM) line buffer — one buffer each for Y, U, and V. The write side records pixels linearly as they arrive from the input stream. The read side retrieves pixels at whatever address the DDA computes. A ping-pong mechanism (the AB flag) alternates between two buffer halves so that one line is being written while the previous line is being read. This is the same architecture used in professional video scalers and frame synchronizers.

### Hue Generation via Quadrature LUTs

The background color is specified by a single hue angle. Converting a hue angle to YUV chrominance requires sine and cosine functions, which are expensive in gate logic. Dolly uses a pair of 64-entry lookup tables — one storing a quarter-cosine wave, the other a quarter-sine wave — indexed by the upper 6 bits of the hue register. The cosine table drives the U channel and the sine table drives the V channel. The luminance channel is set to one of two fixed levels (dark or bright) by a toggle switch. This is the same quadrature technique used in analog NTSC color burst generation, implemented digitally.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Write Path ─────────────────────────────────────────────────
│   └─ Linear write into 3× video_line_buffer (Y, U, V)
│      using pixel counter as write address
│
├── Geometry Engine (per frame at vsync) ───────────────────────
│   ├─ image_width  = active_width × (1023−size) / 1024 × aspect / 512
│   ├─ image_height = active_height × (1023−size) / 1024
│   ├─ center_x = pos_x × active_width / 1024
│   ├─ center_y = pos_y × active_height / 1024
│   ├─ image bounds = center ± half_dimensions
│   ├─ border bounds = image bounds ± border_pix
│   └─ DDA step = (active_width << 10) / image_width
│
├── Region Classifier (per pixel) ──────────────────────────────
│   ├─ Image:      inside image bounds (H and V)
│   ├─ Border:     inside border bounds but outside image bounds
│   └─ Background: everything else
│
├── DDA Read Address (per pixel in image region) ───────────────
│   ├─ accumulator += step
│   ├─ read_addr = accumulator >> 10  (integer part)
│   └─ Mirror: read_addr = active_width − 1 − read_addr
│
├── Read Path ──────────────────────────────────────────────────
│   └─ 3× video_line_buffer read at DDA address → image pixels
│
├── Output Compositor (3-way region mux) ───────────────────────
│   ├─ Image region  → line buffer output (or black if edge clamp)
│   ├─ Border region → border color (White or Black)
│   └─ Background    → hue LUT color (Dark or Bright luminance)
│
├── Wet/Dry Mix ────────────────────────────────────────────────
│   └─ 3× interpolator_u: crossfade compositor ↔ delayed input
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 10-clock shift register aligns hsync/vsync/field/data
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed or delayed original signal
```

The critical path runs vertically through time: geometry is computed once per frame (at vsync), then the region classifier and DDA run per pixel for the duration of that frame. The line buffers bridge between the input's linear pixel order and the DDA's potentially non-linear read order. Because the DDA accumulator resets at the left edge of the image region and advances by a fixed step, the horizontal scaling is uniform across the line — there is no per-pixel multiplication, just one addition. The region classifier's output is delayed by two pipeline stages to align with the line buffer's two-clock read latency before reaching the compositor.

---

## Parameter Reference

<img src={dolly_control_panel} alt="Videomancer front panel with Dolly loaded"/>
*Videomancer's front panel with Dolly active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the image scale factor. At minimum, the image fills the entire output raster — no border or background is visible. As you increase the control, the image shrinks symmetrically toward a point defined by Position X and Y. The scaling is applied to both horizontal and vertical dimensions simultaneously, maintaining the image's proportions (before Aspect modification). At maximum, the image is reduced to a sliver. The relationship between the control position and the scale factor is linear: the image area decreases proportionally with the control value.

---

#### Knob 2 — BKG Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |
| Suffix | ° |

Sets the background hue angle. The control sweeps through the full color wheel: reds, oranges, yellows, greens, cyans, blues, and violets. The hue is generated by a pair of cosine/sine lookup tables that produce the U and V chrominance values. The resulting background color is always fully saturated; luminance is controlled separately by the BKG Lum toggle. At the default center position, the hue is approximately cyan. Sweeping the control produces smooth, continuous color rotation behind the image.

---

#### Knob 3 — Position X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the image horizontally within the output frame. At the minimum position, the image is flush against the left edge. At center, the image is centered horizontally. At maximum, the image is flush against the right edge. When the image is smaller than the frame (Size above minimum), adjusting Position X slides the inset image left and right, revealing more or less background on each side. Combined with Position Y, this control places the image at any point within the broadcast canvas.

---

#### Knob 4 — Position Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the image vertically within the output frame. At minimum, the image sits at the top of the frame. At center, the image is vertically centered. At maximum, the image is at the bottom. This control and Position X together define the image's anchor point — the center of the scaled rectangle. For picture-in-picture layouts, you typically push the inset to a corner by setting both position controls near their extremes.

---

#### Knob 5 — Aspect
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Adjusts the horizontal aspect ratio of the scaled image. At center, the image maintains its original proportions. Turning below center compresses the image horizontally (tall and narrow). Turning above center stretches the image horizontally (short and wide). The vertical dimension is unaffected — only the horizontal scale is multiplied by the aspect factor. This is useful for creating anamorphic squeeze effects or compensating for non-square pixel sources.

---

#### Knob 6 — Border Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the width of the border frame drawn around the image rectangle. At minimum, no border is visible. As you increase the control, a solid-color border grows outward from the image edges. The border color is selected by the Border Color toggle (white or black). The border pixels are always achromatic (U=V=512). Maximum border width is 64 pixels, which creates a bold frame around even small inset images. Border width is independent of image size — a thin border stays thin regardless of how large or small the image is.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Border Color** | White | Black |
| **8 — BKG Lum** | Dark | Bright |
| **9 — Edge Clamp** | Clamp | Black |
| **10 — Mirror** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7 through 11 control five independent binary options. Border Color and BKG Lum affect the appearance of non-image regions. Edge Clamp determines what happens when the DDA reads beyond the source line's extent. Mirror flips the image horizontally. Bypass routes the input directly to the output. These switches do not interact with each other — each controls a single, independent aspect of the DVE.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the DVE compositor output and the original input signal. At maximum (default), only the processed DVE output is visible. At minimum, only the original input is visible. Intermediate positions create a dissolve blend between the two. This is implemented by three `interpolator_u` instances (one per YUV channel) that linearly interpolate between the delayed input and the compositor output. The mix operates on every pixel, including border and background regions — so at partial mix, the border and background partially overlay the original image.

---

## Guided Exercises

These exercises progress from basic picture-in-picture setups through broadcast composition techniques, building familiarity with the geometry, border, and background controls.

### Exercise 1: Classic Picture-in-Picture

<img src={dolly_exercise1_result} alt="Classic Picture-in-Picture result"/>
*Classic Picture-in-Picture — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects.

**Objective**: Create a standard broadcast picture-in-picture insert positioned in a corner of the frame.

1. **Shrink the image**: Slowly increase Size from 0%. Watch the image shrink toward the center of the frame, revealing the background color behind it.
2. **Position the inset**: Set Position X to about 80% and Position Y to about 20%. The image slides to the upper-right corner.
3. **Add a border**: Increase Border Width to about 15%. A white frame appears around the inset image.
4. **Choose a background**: Sweep BKG Hue to find a background color. Try toggling BKG Lum between Dark and Bright to see how it affects the background saturation.
5. **Fine-tune**: Adjust Size and Position until the inset looks like a classic news-style PiP insert.

**Key concepts**: Size controls scale factor, Position X/Y control placement, Border Width adds a visible frame, background color fills the remaining area

---

### Exercise 2: Anamorphic Squeeze and Stretch

<img src={dolly_exercise2_result} alt="Anamorphic Squeeze and Stretch result"/>
*Anamorphic Squeeze and Stretch — simulated result across source images.*
**Source**: Footage with strong geometric features — architecture, grids, or text.

**Objective**: Explore horizontal aspect distortion for creative anamorphic effects.

1. **Start centered**: Set Size to about 30% so the image is clearly smaller than the frame.
2. **Squeeze narrow**: Turn Aspect below center. The image compresses horizontally into a tall, narrow column.
3. **Stretch wide**: Turn Aspect above center. The image stretches into a short, wide strip.
4. **Edge behavior**: With the image stretched wide, toggle Edge Clamp between Clamp and Black. Notice how the edges of the stretched image either smear (Clamp) or cut to black (Black).
5. **Mirror and stretch**: Enable Mirror while the image is stretched. The flipped, distorted image creates a kaleidoscope-like symmetry.
6. **Add a bold border**: Set Border Width to about 40% with Border Color on Black. The black border frames the distorted image like a letterbox.

**Key concepts**: Aspect modifies only horizontal scale, edge clamp controls out-of-bounds behavior, mirror reverses read direction, border is independent of image geometry

---

### Exercise 3: Animated DVE Dissolve

<img src={dolly_exercise3_result} alt="Animated DVE Dissolve result"/>
*Animated DVE Dissolve — simulated result across source images.*
**Source**: Any footage, especially high-contrast material with bold colors.

**Objective**: Use the Mix fader and background hue together to create layered dissolve compositions.

1. **Set up the inset**: Size at about 50%, centered position, moderate border (about 10% width, white).
2. **Background color**: Sweep BKG Hue slowly while watching the background color change. Choose a complementary color to the source material.
3. **Partial mix**: Lower Mix to about 50%. The DVE output blends with the original full-frame image. The border and background become semi-transparent overlays.
4. **Sweep size during mix**: While Mix is at 50%, slowly increase Size. The shrinking inset dissolves against the full-frame original, creating a ghostly double-exposure effect.
5. **Full cross-dissolve**: Sweep Mix from 100% (full DVE) down to 0% (full original). This is the classic broadcast cross-dissolve, but with the DVE geometry visible during the transition.
6. **Toggle BKG Lum**: At partial mix, toggle between Dark and Bright backgrounds. The dissolve character changes dramatically — dark backgrounds create shadows, bright backgrounds create glows.

**Key concepts**: Mix crossfades processed and original signals, partial mix creates overlay compositions, background luminance affects dissolve character, geometry changes during dissolve create motion effects

---


## Tips

- **Corner inserts**: For a standard broadcast PiP, set Size to about 40%, then push Position X and Y toward a corner (e.g., 80%/20% for upper-right). Add a thin white border for separation.
- **Aspect for anamorphic looks**: Aspect values below center create a pillarbox-style vertical squeeze; values above center create a letterbox-style horizontal stretch. Use with edge clamp set to Black for clean cutoffs.
- **Background as a canvas**: The background is visible everywhere the image and border are not. With a large Size value (small image), the background becomes the dominant visual element. Sweep BKG Hue for animated color fields.
- **Border as a graphic element**: At large Border Width values, the border becomes a substantial graphic frame. Black borders disappear into dark backgrounds; white borders pop against any hue.
- **Mix for transitions**: The Mix fader is not just for A/B comparison — at intermediate positions, the DVE output overlays the original signal, creating double-exposure compositions where the inset and the full-frame image coexist.
- **Mirror for symmetry**: Enable Mirror to create left-right reflected versions of the source. Combined with a centered position, this creates a bilateral symmetry effect.
- **Edge clamp for smear effects**: When the DDA reads beyond the source line, Clamp mode smears the edge pixel outward. This can be a deliberate effect — pushing Aspect to extremes with Clamp creates colored streaks at the image margins.
- **Geometry is per-frame**: Size, Position, Aspect, and Border Width are recomputed at each vsync. Rapid parameter changes produce immediate, glitch-free geometric updates.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for line buffer storage. |
| **Compositor** | The output stage that selects between image, border, and background pixels based on region classification. |
| **DDA** | Digital Differential Analyzer; a fixed-point accumulator-based technique for computing evenly spaced sample addresses, used here for horizontal scaling. |
| **DVE** | Digital Video Effect; a broadcast industry term for real-time geometric manipulation (scale, position, rotation) of a video signal. |
| **Hue** | The attribute of a color that distinguishes it from other colors on the color wheel (red, green, blue, etc.), independent of brightness or saturation. |
| **Interpolator** | A component that computes weighted averages between two values; used here for the wet/dry mix crossfade. |
| **Line Buffer** | A dual-port BRAM that stores one scanline of pixel data, allowing linear write and random-access read for scaling operations. |
| **Ping-Pong** | A double-buffering technique where two memory regions alternate roles (read/write) to allow simultaneous input capture and output generation. |
| **PiP** | Picture-in-Picture; a composition technique where a smaller image is displayed within a larger frame. |
| **Region Classifier** | Logic that determines whether each output pixel belongs to the image, border, or background region based on coordinate comparisons. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
