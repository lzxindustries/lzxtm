---
draft: true
sidebar_position: 3
slug: /instruments/videomancer/alcove
title: "Alcove"
image: /img/instruments/videomancer/alcove/alcove_hero_s1.png
description: "Alcove is a broadcast-style DVE (Digital Video Effects) priority compositor that places a positioned, scaled foreground window showing clean unprocessed video over a processed background."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import alcove_control_panel from '/img/instruments/videomancer/alcove/alcove_control_panel.png';
import alcove_source1_dog from '/img/instruments/videomancer/alcove/alcove_source1_dog.png';
import alcove_source2_car from '/img/instruments/videomancer/alcove/alcove_source2_car.png';
import alcove_source3_clouds from '/img/instruments/videomancer/alcove/alcove_source3_clouds.png';
import alcove_source4_pattern from '/img/instruments/videomancer/alcove/alcove_source4_pattern.png';
import alcove_source5_boy from '/img/instruments/videomancer/alcove/alcove_source5_boy.png';
import alcove_source6_berries from '/img/instruments/videomancer/alcove/alcove_source6_berries.png';
import alcove_hero_s1 from '/img/instruments/videomancer/alcove/alcove_hero_s1.png';
import alcove_hero_s2 from '/img/instruments/videomancer/alcove/alcove_hero_s2.png';
import alcove_hero_s3 from '/img/instruments/videomancer/alcove/alcove_hero_s3.png';
import alcove_hero_s4 from '/img/instruments/videomancer/alcove/alcove_hero_s4.png';
import alcove_hero_s5 from '/img/instruments/videomancer/alcove/alcove_hero_s5.png';
import alcove_hero_s6 from '/img/instruments/videomancer/alcove/alcove_hero_s6.png';
import alcove_ex1_s1 from '/img/instruments/videomancer/alcove/alcove_ex1_s1.png';
import alcove_ex1_s2 from '/img/instruments/videomancer/alcove/alcove_ex1_s2.png';
import alcove_ex1_s3 from '/img/instruments/videomancer/alcove/alcove_ex1_s3.png';
import alcove_ex1_s4 from '/img/instruments/videomancer/alcove/alcove_ex1_s4.png';
import alcove_ex1_s5 from '/img/instruments/videomancer/alcove/alcove_ex1_s5.png';
import alcove_ex1_s6 from '/img/instruments/videomancer/alcove/alcove_ex1_s6.png';
import alcove_ex2_s1 from '/img/instruments/videomancer/alcove/alcove_ex2_s1.png';
import alcove_ex2_s2 from '/img/instruments/videomancer/alcove/alcove_ex2_s2.png';
import alcove_ex2_s3 from '/img/instruments/videomancer/alcove/alcove_ex2_s3.png';
import alcove_ex2_s4 from '/img/instruments/videomancer/alcove/alcove_ex2_s4.png';
import alcove_ex2_s5 from '/img/instruments/videomancer/alcove/alcove_ex2_s5.png';
import alcove_ex2_s6 from '/img/instruments/videomancer/alcove/alcove_ex2_s6.png';
import alcove_ex3_s1 from '/img/instruments/videomancer/alcove/alcove_ex3_s1.png';
import alcove_ex3_s2 from '/img/instruments/videomancer/alcove/alcove_ex3_s2.png';
import alcove_ex3_s3 from '/img/instruments/videomancer/alcove/alcove_ex3_s3.png';
import alcove_ex3_s4 from '/img/instruments/videomancer/alcove/alcove_ex3_s4.png';
import alcove_ex3_s5 from '/img/instruments/videomancer/alcove/alcove_ex3_s5.png';
import alcove_ex3_s6 from '/img/instruments/videomancer/alcove/alcove_ex3_s6.png';

# Alcove

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: alcove_source1_dog, after: alcove_hero_s1 },
    { label: "Car", before: alcove_source2_car, after: alcove_hero_s2 },
    { label: "Clouds", before: alcove_source3_clouds, after: alcove_hero_s3 },
    { label: "Pattern", before: alcove_source4_pattern, after: alcove_hero_s4 },
    { label: "Boy", before: alcove_source5_boy, after: alcove_hero_s5 },
    { label: "Berries", before: alcove_source6_berries, after: alcove_hero_s6 },
  ]}
/>
*Alcove compositing a clean foreground window over a mosaicked background — the DVE priority compositor places an unprocessed video inset with coloured border over a sample-and-hold posterized background scene.*

---

## Overview

Alcove is a broadcast-style DVE (Digital Video Effects) priority compositor that places a positioned, scaled foreground window showing clean unprocessed video over a processed background. The background can be treated with one of four processing modes — Defocus (8-pixel box blur), Mosaic (sample-and-hold block quantization), Posterize (bit truncation), and Dim (luminance attenuation) — while the foreground window displays the original input via a DDA-scaled line buffer readback. A configurable border in either a selectable hue or white frames the foreground window.

The name *Alcove* references the architectural element — a recessed area within a wall — evoking the idea of a framed opening that reveals one view nested within another. In broadcast production, this type of effect is ubiquitous: picture-in-picture, over-the-shoulder graphics boxes, and split-screen interview layouts all use the same fundamental principle of region-based compositing with foreground priority.

At conservative settings — large window with defocused background and thin white border — the program produces a clean broadcast picture-in-picture. At extreme settings — small window, maximally mosaicked background, thick coloured border in a contrasting hue — the output becomes an abstract graphic composition where the clean video inset floats as a jewel within a deconstructed, block-quantized field.

---

## Quick Start

1. **Window size drives the DDA**: The foreground scaling quality depends on the ratio between the input resolution and the window pixel width. Larger windows produce near-unity scaling (minimal resampling). Very small windows produce heavy downsampling with nearest-neighbour stairstepping.
2. **Mosaic is the most graphic mode**: High BG Inten in Mosaic mode produces large blocks that turn the background into an abstract colour field. Combined with a coloured border, this creates a graphic design aesthetic.
3. **Defocus suggests depth**: Low-to-moderate Defocus with a thin white border creates the most naturalistic picture-in-picture, suggesting physical depth separation between foreground and background.

---

## Background

### What Is a DVE Compositor?

A **DVE (Digital Video Effects)** compositor is a real-time video processing system that manipulates the spatial placement and scaling of video sources within a frame. The simplest DVE operation is picture-in-picture (PiP), where a secondary video source is scaled down and positioned within the frame of a primary source. More complex DVE operations include flying, rotating, and perspective-warping video planes.

Alcove implements the core PiP function with a twist: rather than compositing two independent sources, it composites two *views* of the same source — the foreground window shows the clean input while the background shows a processed version of the same input. This self-referential structure means the effect is always coherent: the foreground and background show the same content at the same moment, just with different processing applied.

### What Is DDA Scaling?

**DDA (Digital Differential Analyzer)** scaling is a technique for resampling a line of pixels to a different resolution using integer-only arithmetic. The DDA maintains an accumulator that adds a fixed step value for each output pixel; when the accumulator overflows, an extra source pixel is consumed. This produces nearest-neighbour scaling without requiring multiplication or division during the scanline.

In Alcove, three line buffers store one full scanline of Y, U, and V data from the input. During the foreground window region, the line buffer is read back using a DDA that maps the full scanline into the window width. A 21-clock multi-cycle restoring divider computes the DDA step during vertical blanking, ensuring the arithmetic is ready before the first active line.

### What Are the Background Processing Modes?

The four background modes each produce a different degradation of the source video:

- **Defocus**: An 8-pixel horizontal box blur implemented as a shift register. The output at each pixel is the average of the surrounding 8 pixels, producing a soft-focus effect that suggests depth-of-field separation between the background and foreground.
- **Mosaic**: Sample-and-hold block quantization. The input is sampled once per block and the sampled value is held for the entire block width. Block size is controlled by the BG Inten pot. This produces the classic pixelated mosaic used in broadcast to obscure faces or license plates.
- **Posterize**: Bit truncation reduces the precision of each colour channel by masking lower bits. This produces flat-shaded colour banding that simplifies the background into broad tonal regions.
- **Dim**: Luminance attenuation reduces the background brightness using a pre-registered multiplication factor derived from the BG Inten pot. This fades the background while keeping the foreground at full brightness.


---

## Signal Flow

Line Buffer Write → Background Processing → Foreground Scaling → ... → Interpolator → Output

```
Input Video (YUV 4:4:4 30-bit)
│
├── Line Buffer Write ──────────────────────────────────────────────
│   └─ Store Y/U/V scanline for FG readback (3x video_line_buffer)
│
├── Background Processing ──────────────────────────────────────────
│   ├─ BG Mode 00: Defocus  (8-pixel box blur via shift register)
│   ├─ BG Mode 01: Mosaic   (sample-and-hold, block size from pot)
│   ├─ BG Mode 10: Posterize (bit truncation)
│   └─ BG Mode 11: Dim      (luma attenuation, pre-registered factor)
│
├── Foreground Scaling ─────────────────────────────────────────────
│   ├─ DDA step computation  (21-clock restoring divider at vblank)
│   └─ Line buffer readback  (DDA-walked read address within window)
│
├── Window Geometry ────────────────────────────────────────────────
│   ├─ Size/position from pots (Win Size, Win X, Win Y)
│   ├─ Optional square aspect  (FG Aspc toggle)
│   └─ Bounds computed per frame at vsync
│
├── Region Classifier ──────────────────────────────────────────────
│   ├─ Foreground region → line buffer Y/U/V (scaled)
│   ├─ Border region → hue colour or white
│   └─ Background region → processed BG video
│
├── Border Generation ──────────────────────────────────────────────
│   ├─ 64-entry hue U/V LUTs (sine/cosine approximation)
│   └─ White mode override → Y=1023, U=V=512
│
├── Sync Delay Pipeline ────────────────────────────────────────────
│   └─ 10-clock delay for sync alignment
│
├── Interpolator (4 clocks per channel) ────────────────────────────
│   └─ Mix = lerp(input_delayed, composited, mix_amount)
│
└── Output ─────────────────────────────────────────────────────────
    └─ Y/U/V from interpolator mix
```

The DDA step computation uses a multi-cycle restoring divider that runs during vertical blanking (21 clock cycles). It divides the active line width by the window pixel width to produce the fixed-point step value used during active video. The line buffers are dual-port BRAMs that are written sequentially during the input scanline and read with the DDA-generated address during the foreground window region.

The region classifier evaluates each pixel's position against the pre-computed window bounds (left, right, top, bottom) plus the border width to determine whether the pixel belongs to the foreground, border, or background region. The foreground has highest priority — if a pixel is within the window bounds (excluding border), it shows line buffer data. If it's within the border region, it shows the border colour. Otherwise, it shows the background-processed video.

---

## Parameter Reference

<img src={alcove_control_panel} alt="Videomancer front panel with Alcove loaded"/>
*Videomancer's front panel with Alcove active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Win Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At minimum, the window is very small — a tiny inset in the background. At maximum, the window fills nearly the entire frame, leaving only a thin border of processed background visible around the edges. The window dimensions are recomputed at each vsync from this pot value combined with the aspect ratio toggle. Internally, controls the size of the foreground window as a proportion of the full frame.

---

#### Knob 2 — Win X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, the window is positioned at the left edge. At 50%, it is centred horizontally. At 100%, it is positioned at the right edge. The position is computed relative to the window size, so the window always remains within the frame bounds. The position is recomputed per frame at vsync. Internally, controls the horizontal position of the foreground window within the frame.

---

#### Knob 3 — Win Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, the window is at the top. At 50%, centred vertically. At 100%, at the bottom. Like horizontal position, the vertical position keeps the window within frame bounds and is updated per frame. Internally, controls the vertical position of the foreground window within the frame.

---

#### Knob 4 — Border W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

At minimum, there is no visible border — the foreground window transitions directly into the background. At maximum, a wide coloured or white frame surrounds the window. The border is rendered inside the region between the window edge and the background, consuming background space as it widens. Internally, controls the width of the border around the foreground window in pixels.

---

#### Knob 5 — BG Inten
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the intensity of the background processing effect. The specific meaning depends on the active background mode: in Defocus mode, higher values increase the blur radius. In Mosaic mode, higher values increase the block size (more aggressive quantization). In Posterize mode, higher values increase the bit truncation. In Dim mode, higher values darken the background more.

---

#### Knob 6 — BrdrHue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |
| Suffix | ° |

Selects the hue of the border around the foreground window using a 64-entry colour LUT. The LUT provides sine/cosine-approximated UV values that sweep through the full colour wheel over 360°. At 0°, the border is orange/red. At 90°, green. At 180°, cyan/blue. At 270°, magenta. When BrdrClr toggle is set to White, this pot is ignored and the border is always white.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — BG Md A** | Off | On |
| **8 — BG Md B** | Off | On |
| **9 — BrdrClr** | Color | White |
| **10 — FG Aspc** | Square | Free |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a **combined 2-bit background mode selector**: 00 = Defocus (box blur), 01 = Mosaic (sample-hold), 10 = Posterize (bit truncation), 11 = Dim (luminance attenuation). Toggle 9 selects **border colour mode** (hue LUT vs white). Toggle 10 selects **foreground aspect ratio** (square vs free). Toggle 11 is bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original input video (delayed to match the 10-clock processing pipeline plus 4-clock interpolator) and the composited output. At 0%, the output is pure unprocessed input. At 100%, the output is the full DVE composite. Intermediate positions blend between the two.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from basic picture-in-picture to complex multi-mode compositions, building familiarity with window geometry, background processing, and border styling.

### Exercise 1: Classic Picture-in-Picture

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: alcove_source1_dog, after: alcove_ex1_s1 },
    { label: "Car", before: alcove_source2_car, after: alcove_ex1_s2 },
    { label: "Clouds", before: alcove_source3_clouds, after: alcove_ex1_s3 },
    { label: "Pattern", before: alcove_source4_pattern, after: alcove_ex1_s4 },
    { label: "Boy", before: alcove_source5_boy, after: alcove_ex1_s5 },
    { label: "Berries", before: alcove_source6_berries, after: alcove_ex1_s6 },
  ]}
/>
*Classic Picture-in-Picture — simulated result across source images.*
**Source**: Any video source — a camera feed or pre-recorded footage with visible subject matter.

**What You'll Create**: Create a standard broadcast picture-in-picture layout with a clean foreground inset over a defocused background.

1. **Set Defocus background**: BG Md A and BG Md B both off (mode 00).
2. **Size the window**: Set Win Size to ~40%. A medium-sized window appears.
3. **Position**: Set Win X to ~75%, Win Y to ~75%. The window moves to the lower-right quadrant.
4. **Add white border**: Set Border W to ~15%, toggle BrdrClr to White.
5. **Adjust background**: Increase BG Inten to ~50%. The background outside the window becomes softly blurred.
6. **Mix full**: Set Mix to 100%. The composite is clearly visible.
7. **Try repositioning**: Sweep Win X and Win Y to move the window around the frame.

**Key concepts**: DVE picture-in-picture, window geometry, defocus background, border width and colour mode

---

### Exercise 2: Mosaic Background with Coloured Border

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: alcove_source1_dog, after: alcove_ex2_s1 },
    { label: "Car", before: alcove_source2_car, after: alcove_ex2_s2 },
    { label: "Clouds", before: alcove_source3_clouds, after: alcove_ex2_s3 },
    { label: "Pattern", before: alcove_source4_pattern, after: alcove_ex2_s4 },
    { label: "Boy", before: alcove_source5_boy, after: alcove_ex2_s5 },
    { label: "Berries", before: alcove_source6_berries, after: alcove_ex2_s6 },
  ]}
/>
*Mosaic Background with Coloured Border — simulated result across source images.*
**Source**: Footage with saturated colours and visible detail.

**What You'll Create**: Combine the mosaic background mode with a hue-selected coloured border to create an abstract graphic composition.

1. **Set Mosaic mode**: Toggle BG Md A to On, BG Md B off (mode 01).
2. **Large blocks**: Set BG Inten to ~80%. The background becomes a coarse mosaic of large colour blocks.
3. **Centre window**: Win X ~50%, Win Y ~50%, Win Size ~30%.
4. **Square aspect**: Toggle FG Aspc to Square. The window becomes a perfect square.
5. **Coloured border**: Toggle BrdrClr to Color. Set BrdrHue to ~120° (green region). A vivid green border frames the square window.
6. **Wide border**: Increase Border W to ~25%. The border becomes a prominent graphic element.
7. **Sweep hue**: Slowly rotate BrdrHue through 360°. The border colour cycles through the entire spectrum.

**Key concepts**: Mosaic sample-and-hold, block size control, hue LUT border, square aspect constraint, border as graphic element

---

### Exercise 3: Dim Background Interview Layout

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: alcove_source1_dog, after: alcove_ex3_s1 },
    { label: "Car", before: alcove_source2_car, after: alcove_ex3_s2 },
    { label: "Clouds", before: alcove_source3_clouds, after: alcove_ex3_s3 },
    { label: "Pattern", before: alcove_source4_pattern, after: alcove_ex3_s4 },
    { label: "Boy", before: alcove_source5_boy, after: alcove_ex3_s5 },
    { label: "Berries", before: alcove_source6_berries, after: alcove_ex3_s6 },
  ]}
/>
*Dim Background Interview Layout — simulated result across source images.*
**Source**: Camera feed of a person speaking — ideal for demonstrating broadcast interview framing.

**What You'll Create**: Create a professional-looking interview overlay where the background is dimmed to draw focus to the foreground subject.

1. **Set Dim mode**: Toggle BG Md A to On, BG Md B to On (mode 11).
2. **Strong dimming**: Set BG Inten to ~70%. The background darkens significantly while the foreground window remains at full brightness.
3. **Large window**: Win Size ~60%, positioned centre-left (Win X ~35%, Win Y ~45%).
4. **Thin white border**: Border W ~5%, BrdrClr set to White. A subtle white outline separates the foreground.
5. **Free aspect**: FG Aspc to Free. The window takes a 16:9-proportional shape.
6. **Fade in**: Slowly increase Mix from 0% to 100%. The dim background effect fades in smoothly over the original.

**Key concepts**: Dim background mode, luminance attenuation, interview framing, thin border styling, aspect ratio choice

---


## Tips

- **Border hue as accent colour**: Use BrdrHue to match or contrast the predominant colour in the video. A complementary-colour border (opposite on the wheel) draws maximum attention to the window.
- **Square windows for social media**: The Square aspect toggle produces 1:1 frames suitable for social media crop ratios. Position the window in a lower-third or corner for a professional overlay look.
- **Dim mode for focus**: Dim is the subtlest background mode — it reduces background brightness without altering colour or spatial detail. Best for drawing the viewer's eye to the foreground window.
- **Posterize for stylization**: Posterize mode reduces colour precision in the background, creating flat-shaded regions. Combined with a wide border, this produces a graphic novel or comic book aesthetic.
- **Feedback routing creates recursive PiP**: Routing the output back to the input creates a picture-in-picture within a picture-in-picture, producing an infinite tunnel of nested windows.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bit Truncation** | Reducing colour precision by masking lower-order bits, producing flat-shaded banding; used in Posterize background mode. |
| **Box Blur** | A spatial filter that replaces each pixel with the arithmetic mean of its neighbours; Alcove's Defocus mode uses an 8-pixel horizontal box blur. |
| **BRAM (Block RAM)** | Dedicated memory blocks within the FPGA used for line buffers and lookup tables; Alcove uses dual-port BRAMs for simultaneous scanline read and write. |
| **DDA (Digital Differential Analyzer)** | An integer-only resampling algorithm that maps source pixels to a different resolution using an accumulator and fixed step value, avoiding division during the scanline. |
| **DVE (Digital Video Effects)** | A class of real-time video processing that manipulates spatial placement, scaling, and compositing of video sources within a frame. |
| **LUT (Lookup Table)** | A precomputed array mapping input values to output values; Alcove uses a 64-entry hue LUT for border colour generation. |
| **Nearest-Neighbour Scaling** | A resampling method that selects the closest source pixel for each output pixel without interpolation, producing sharp edges but visible stairstepping. |
| **PiP (Picture-in-Picture)** | A compositing technique where a scaled secondary video is overlaid within the frame of a primary video. |
| **Restoring Divider** | A multi-cycle binary division circuit that computes one quotient bit per clock cycle; Alcove uses a 21-clock restoring divider for DDA step calculation. |
| **Sample-and-Hold** | A technique that captures a signal value at one moment and holds it constant until the next sample; used in Mosaic mode to produce block quantization. |
| **Scanline** | A single horizontal row of pixels in a video frame, scanned left-to-right by the raster. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
