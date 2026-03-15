---
draft: true
sidebar_position: 233
slug: /instruments/videomancer/polaroid
title: "Polaroid"
image: /img/instruments/videomancer/polaroid/polaroid_hero_s1.png
description: "Polaroid places a white border frame around the active video area, mimicking the distinctive look of instant-film prints."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import polaroid_control_panel from '/img/instruments/videomancer/polaroid/polaroid_control_panel.png';
import polaroid_source1_car from '/img/instruments/videomancer/polaroid/polaroid_source1_car.png';
import polaroid_source2_house from '/img/instruments/videomancer/polaroid/polaroid_source2_house.png';
import polaroid_source3_collage from '/img/instruments/videomancer/polaroid/polaroid_source3_collage.png';
import polaroid_source4_pattern from '/img/instruments/videomancer/polaroid/polaroid_source4_pattern.png';
import polaroid_source5_girl from '/img/instruments/videomancer/polaroid/polaroid_source5_girl.png';
import polaroid_source6_paint from '/img/instruments/videomancer/polaroid/polaroid_source6_paint.png';
import polaroid_hero_s1 from '/img/instruments/videomancer/polaroid/polaroid_hero_s1.png';
import polaroid_hero_s2 from '/img/instruments/videomancer/polaroid/polaroid_hero_s2.png';
import polaroid_hero_s3 from '/img/instruments/videomancer/polaroid/polaroid_hero_s3.png';
import polaroid_hero_s4 from '/img/instruments/videomancer/polaroid/polaroid_hero_s4.png';
import polaroid_hero_s5 from '/img/instruments/videomancer/polaroid/polaroid_hero_s5.png';
import polaroid_hero_s6 from '/img/instruments/videomancer/polaroid/polaroid_hero_s6.png';
import polaroid_ex1_s1 from '/img/instruments/videomancer/polaroid/polaroid_ex1_s1.png';
import polaroid_ex1_s2 from '/img/instruments/videomancer/polaroid/polaroid_ex1_s2.png';
import polaroid_ex1_s3 from '/img/instruments/videomancer/polaroid/polaroid_ex1_s3.png';
import polaroid_ex1_s4 from '/img/instruments/videomancer/polaroid/polaroid_ex1_s4.png';
import polaroid_ex1_s5 from '/img/instruments/videomancer/polaroid/polaroid_ex1_s5.png';
import polaroid_ex1_s6 from '/img/instruments/videomancer/polaroid/polaroid_ex1_s6.png';
import polaroid_ex2_s1 from '/img/instruments/videomancer/polaroid/polaroid_ex2_s1.png';
import polaroid_ex2_s2 from '/img/instruments/videomancer/polaroid/polaroid_ex2_s2.png';
import polaroid_ex2_s3 from '/img/instruments/videomancer/polaroid/polaroid_ex2_s3.png';
import polaroid_ex2_s4 from '/img/instruments/videomancer/polaroid/polaroid_ex2_s4.png';
import polaroid_ex2_s5 from '/img/instruments/videomancer/polaroid/polaroid_ex2_s5.png';
import polaroid_ex2_s6 from '/img/instruments/videomancer/polaroid/polaroid_ex2_s6.png';
import polaroid_ex3_s1 from '/img/instruments/videomancer/polaroid/polaroid_ex3_s1.png';
import polaroid_ex3_s2 from '/img/instruments/videomancer/polaroid/polaroid_ex3_s2.png';
import polaroid_ex3_s3 from '/img/instruments/videomancer/polaroid/polaroid_ex3_s3.png';
import polaroid_ex3_s4 from '/img/instruments/videomancer/polaroid/polaroid_ex3_s4.png';
import polaroid_ex3_s5 from '/img/instruments/videomancer/polaroid/polaroid_ex3_s5.png';
import polaroid_ex3_s6 from '/img/instruments/videomancer/polaroid/polaroid_ex3_s6.png';

# Polaroid

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Car", before: polaroid_source1_car, after: polaroid_hero_s1 },
    { label: "House", before: polaroid_source2_house, after: polaroid_hero_s2 },
    { label: "Collage", before: polaroid_source3_collage, after: polaroid_hero_s3 },
    { label: "Pattern", before: polaroid_source4_pattern, after: polaroid_hero_s4 },
    { label: "Girl", before: polaroid_source5_girl, after: polaroid_hero_s5 },
    { label: "Paint", before: polaroid_source6_paint, after: polaroid_hero_s6 },
  ]}
/>
*Polaroid applying instant-film border framing and warm colour shift to transform video into nostalgic snapshots.*

---

## Overview

Polaroid places a white border frame around the active video area, mimicking the distinctive look of instant-film prints. Inside the frame, a brightness scaling control adjusts overall exposure while a warmth offset shifts the chrominance toward yellow-orange, replicating the warm colour cast typical of vintage instant-film stock.

The current implementation focuses on the core visual identity of the Polaroid aesthetic — the white border and warm tint. Several parameters declared in the register map (Fade, Saturation, Overexpose, Color Shift, Grain, Wide Border) are reserved for future expansion and have no effect on the output in this version. The supplement notes each unused parameter explicitly so that patch artists can focus on the controls that actually shape the image.

At moderate settings, its effects are subtle — a cream-toned frame with gentle warmth. Push the Exposure knob past midpoint and the image blooms into overdriven whites; pull Warmth to maximum and the entire colour palette takes on a sepia-amber tone. The Border knob can produce anything from a thin hairline outline to a massive frame that nearly hides the picture.

---

## Quick Start

1. **Only three knobs matter**: In this version, the active controls are Exposure, Warmth, and Border. The remaining pots and toggles are reserved stubs — ignore them for creative work.
2. **Frame width scales with the top 8 bits**: The Border knob uses `register >> 2`, so the first quarter-turn of the knob has the finest resolution for thin frames.
3. **Warm tint is additive**: The Warmth offset affects all pixels equally — it shifts the entire UV gamut, not just specific hues. Strong warmth can push already-warm source material into clipping.

---

## Background

### Instant Film and the Polaroid Aesthetic

Edwin Land's instant-film process, introduced in 1948, became synonymous with a visual style: a white rectangular border (wider at the bottom on SX-70 prints) surrounding a slightly desaturated, warm-toned image. The chemical development process produced colours that drifted toward yellow-green in the shadows and amber in the highlights. This colour signature is so recognisable that "Polaroid look" has become shorthand for warm, slightly faded imagery.

### Border Framing in Video

Adding a geometric border to a raster signal requires comparing each pixel's position against threshold values for all four edges. The FPGA implementation uses horizontal and vertical counters that reset on sync edges, then tests whether the current position falls within a configurable margin. Pixels inside the margin are replaced with a fixed output value — in this case, near-white — creating a clean rectangular frame with no anti-aliasing.

### Warm Tint via Chrominance Offset

In the YUV colour model, shifting the U channel downward and the V channel upward moves the overall hue from neutral toward yellow-orange. This is a constant offset rather than a multiplicative gain, so it affects all pixels equally regardless of their original hue. The technique is computationally inexpensive — a single subtraction on U and addition on V — and produces a convincing approximation of the warm colour drift found in instant-film chemistry.

### Exposure Scaling

Multiplying the luminance channel by a register value implements a brightness gain stage. When the multiplier equals the full-scale register value (1023), the output matches the input. Values below full-scale attenuate brightness; values above the midpoint create a progressively brighter image. Because the multiplication uses the full 10-bit register, the gain curve is linear with 1024 steps from black to unity.


---

## Signal Flow

Timing Detection → Border Region Test → IMAGE AREA → Interpolator → Sync Delay Pipeline → Output Mux

```
Input Video (YUV 4:4:4)
│
├── Timing Detection ──────────────────────────────────
│   ├─ hsync / vsync falling-edge detection
│   └─ x_counter, y_counter (pixel position tracking)
│
├── Border Region Test ────────────────────────────────
│   └─ Compare x/y against border threshold (4 edges)
│       │
│       ├── BORDER → Y=960, U=512, V=512 (near-white)
│       │
│       └── IMAGE AREA ────────────────────────────────
│           ├─ Y: input_Y × Exposure  (10-bit multiply)
│           ├─ U: input_U − Warmth/8  (saturating sub)
│           └─ V: input_V + Warmth/8  (saturating add)
│
├── Interpolator ──────────────────────────────────────
│   └─ Wet/dry crossfade (Mix fader)
│
├── Sync Delay Pipeline (8 clocks) ────────────────────
│   └─ Align sync + dry data to processed path
│
└── Output Mux ────────────────────────────────────────
    └─ Bypass toggle selects processed or dry signal
```

The processing pipeline is dominated by a single synchronous process that handles timing, border detection, and pixel transformation in one block. Border detection is purely positional — it compares x/y counters against a threshold derived from the Border knob. Inside the frame, the Y channel is scaled by the Exposure register (a 10×10-bit multiply taking the upper 10 bits), while U and V are offset by Warmth divided by 8. The vignette distance calculation exists in the VHDL source but its result is never applied to the output, so the Vignette knob has no visible effect in this version.

---

## Parameter Reference

<img src={polaroid_control_panel} alt="Videomancer front panel with Polaroid loaded"/>
*Videomancer's front panel with Polaroid active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Exposure
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Exposure controls overall image brightness by multiplying the input luminance channel against the 10-bit register value. At the default midpoint (512), the image is approximately half brightness. Turning fully clockwise (1023) passes the original brightness through unchanged. Turning counter-clockwise darkens the image toward black. Because the multiply is linear, the attenuation curve is smooth and uniform across the tonal range.

---

#### Knob 2 — Warmth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

Warmth shifts the chrominance toward yellow-orange by subtracting from U and adding to V. The offset magnitude is the register value divided by 8, giving a maximum shift of ±127 counts in the 10-bit chroma domain. At the default of 640, a moderate warm cast is applied. At zero, the chroma is unchanged. At maximum, the entire image takes on a strong amber tone. The shift is constant regardless of source hue — every pixel moves the same amount in UV space.

---

#### Knob 3 — Fade
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Fade is declared in the register map but has no effect on the output in the current VHDL implementation. It is reserved for future development — likely intended for a development-style fade-in exposure simulation. Adjusting this knob produces no visible change.

---

#### Knob 4 — Saturation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Saturation is declared in the register map but has no effect on the output in the current VHDL implementation. It is reserved for a future chroma gain stage. Adjusting this knob produces no visible change.

---

#### Knob 5 — Border
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Border sets the width of the white frame surrounding the image. The VHDL uses the top 8 bits of the 10-bit register (`border(9 downto 2)`) as a pixel threshold, giving a range of 0 to 255 pixels. When any pixel's x or y coordinate falls within this distance of the frame edge, the output is replaced with near-white (Y=960, U=V=512). The frame is uniform on all four sides. At zero, no border is visible. At maximum, the border consumes a significant portion of the 1280×720 frame.

---

#### Knob 6 — Vignette
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Vignette is partially implemented — the VHDL computes a Manhattan distance from the frame centre and derives a darkening factor, but this factor is never applied to the output luminance. Adjusting this knob produces no visible change in the current version. It is reserved for a future edge-darkening effect.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Overexpose** | Off | On |
| **8 — Color Shift** | Off | On |
| **9 — Grain** | Off | On |
| **10 — Wide Border** | Off | On |
| **11 — Bypass** | Off | On |

Of the five toggle switches, only Bypass (Switch 11) produces a visible effect. Overexpose, Color Shift, Grain, and Wide Border are all declared in the toggle register but are never read by any processing logic. They are reserved for future expansion of the instant-film emulation.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry (original) signal and the wet (processed) signal via the interpolator stage. At 100% (default, register 1023), only the processed signal is output. At 0%, the original signal passes through unchanged. Intermediate values create a transparent overlay where the border and warm tint are partially visible — useful for subtle framing effects.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Polaroid processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises explore the three active parameters — Border, Exposure, and Warmth — and demonstrate how they combine to create instant-film aesthetics ranging from subtle vintage toning to dramatic graphic framing.

### Exercise 1: Classic Instant Print

<BeforeAfterSlider
  sources={[
    { label: "Car", before: polaroid_source1_car, after: polaroid_ex1_s1 },
    { label: "House", before: polaroid_source2_house, after: polaroid_ex1_s2 },
    { label: "Collage", before: polaroid_source3_collage, after: polaroid_ex1_s3 },
    { label: "Pattern", before: polaroid_source4_pattern, after: polaroid_ex1_s4 },
    { label: "Girl", before: polaroid_source5_girl, after: polaroid_ex1_s5 },
    { label: "Paint", before: polaroid_source6_paint, after: polaroid_ex1_s6 },
  ]}
/>
*Classic Instant Print — simulated result across source images.*
**Source**: A portrait or still-life shot with warm skin tones and moderate contrast.

**What You'll Create**: Create a convincing Polaroid-style framing with warm tone shift.

1. Set Border to ~60% to create a visible white frame around the image.
2. Increase Warmth to ~70% for a noticeable amber cast.
3. Reduce Exposure to ~45% to slightly darken the image, simulating the softer exposure of instant film.
4. Observe how the white border contrasts with the warm-tinted image area.
5. Adjust Mix to ~80% to let a hint of the original colour through.

**Key concepts**: Border detection replaces edge pixels with white, warmth shifts UV uniformly, exposure scales luminance linearly

---

### Exercise 2: Bold Frame Graphic

<BeforeAfterSlider
  sources={[
    { label: "Car", before: polaroid_source1_car, after: polaroid_ex2_s1 },
    { label: "House", before: polaroid_source2_house, after: polaroid_ex2_s2 },
    { label: "Collage", before: polaroid_source3_collage, after: polaroid_ex2_s3 },
    { label: "Pattern", before: polaroid_source4_pattern, after: polaroid_ex2_s4 },
    { label: "Girl", before: polaroid_source5_girl, after: polaroid_ex2_s5 },
    { label: "Paint", before: polaroid_source6_paint, after: polaroid_ex2_s6 },
  ]}
/>
*Bold Frame Graphic — simulated result across source images.*
**Source**: High-contrast material — geometric patterns, text overlays, or architectural footage.

**What You'll Create**: Use a thick border and extreme warmth to create a graphic poster effect.

1. Push Border to ~90% for a massive frame that nearly envelops the image.
2. Set Warmth to maximum (100%) for deep amber colour.
3. Set Exposure to ~30% to darken the image into a moody vignette-like feel.
4. Compare with Bypass to see the original — toggle Switch 11.
5. Pull Mix down to ~50% to blend the framed look with the raw signal.

**Key concepts**: Large border values consume most of the 1280×720 frame, warmth at maximum shifts colour dramatically, mix blending softens aggressive effects

---

### Exercise 3: Neutral Frame with Full Brightness

<BeforeAfterSlider
  sources={[
    { label: "Car", before: polaroid_source1_car, after: polaroid_ex3_s1 },
    { label: "House", before: polaroid_source2_house, after: polaroid_ex3_s2 },
    { label: "Collage", before: polaroid_source3_collage, after: polaroid_ex3_s3 },
    { label: "Pattern", before: polaroid_source4_pattern, after: polaroid_ex3_s4 },
    { label: "Girl", before: polaroid_source5_girl, after: polaroid_ex3_s5 },
    { label: "Paint", before: polaroid_source6_paint, after: polaroid_ex3_s6 },
  ]}
/>
*Neutral Frame with Full Brightness — simulated result across source images.*
**Source**: Any video source — the focus is on the border framing without colour alteration.

**What You'll Create**: Isolate the border effect from the tinting to understand each component independently.

1. Set Exposure to 100% (fully clockwise) so brightness is unmodified.
2. Set Warmth to 0% for neutral chroma.
3. Set Border to ~40% for a moderate frame width.
4. Observe the clean white frame with untinted image content.
5. Slowly increase Warmth from 0% to 100% and watch the colour shift independently of framing.
6. Reverse: set Warmth to 50%, then sweep Exposure from 0% to 100% to see brightness scaling alone.

**Key concepts**: Exposure and warmth are independent processing stages, border detection is purely positional, white frame value is fixed at Y=960

---


## Tips

- **Exposure is a linear gain**: Unlike a camera exposure which affects noise and dynamic range, this is a simple multiply. Turning Exposure above midpoint recovers full brightness; there is no overexposure bloom.
- **Mix for transparent borders**: Lowering the Mix fader blends the white frame with the original image, creating a semi-transparent border effect.
- **White border value**: The border fill is Y=960, not 1023. This is slightly below full white, matching the off-white appearance of aged instant-film prints.

---

## Glossary

| Term | Definition |
|------|------------|
| **Border Detection** | Comparing pixel coordinates against threshold values to determine whether a pixel falls inside a frame margin. |
| **Chroma** | The colour information in a video signal, encoded as U and V components in YUV colour space. |
| **Chrominance Offset** | Adding or subtracting a constant from the U and V channels to shift the overall hue. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Manhattan Distance** | The sum of absolute differences along each axis; used (but not applied) for the vignette calculation. |
| **Saturating Arithmetic** | Arithmetic that clamps results to a valid range instead of wrapping around on overflow or underflow. |

---
