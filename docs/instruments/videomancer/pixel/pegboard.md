---
draft: true
sidebar_position: 221
slug: /instruments/videomancer/pegboard
title: "Pegboard"
image: /img/instruments/videomancer/pegboard/pegboard_hero_s1.png
description: "Before LCD panels and OLED screens, there was Lite-Brite — a toy that turned translucent colored pegs into glowing pictures when backlit."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import pegboard_control_panel from '/img/instruments/videomancer/pegboard/pegboard_control_panel.png';
import pegboard_source1_boat from '/img/instruments/videomancer/pegboard/pegboard_source1_boat.png';
import pegboard_source2_runner from '/img/instruments/videomancer/pegboard/pegboard_source2_runner.png';
import pegboard_source3_elephant from '/img/instruments/videomancer/pegboard/pegboard_source3_elephant.png';
import pegboard_source4_pattern from '/img/instruments/videomancer/pegboard/pegboard_source4_pattern.png';
import pegboard_source5_woman from '/img/instruments/videomancer/pegboard/pegboard_source5_woman.png';
import pegboard_source6_knit from '/img/instruments/videomancer/pegboard/pegboard_source6_knit.png';
import pegboard_hero_s1 from '/img/instruments/videomancer/pegboard/pegboard_hero_s1.png';
import pegboard_hero_s2 from '/img/instruments/videomancer/pegboard/pegboard_hero_s2.png';
import pegboard_hero_s3 from '/img/instruments/videomancer/pegboard/pegboard_hero_s3.png';
import pegboard_hero_s4 from '/img/instruments/videomancer/pegboard/pegboard_hero_s4.png';
import pegboard_hero_s5 from '/img/instruments/videomancer/pegboard/pegboard_hero_s5.png';
import pegboard_hero_s6 from '/img/instruments/videomancer/pegboard/pegboard_hero_s6.png';
import pegboard_ex1_s1 from '/img/instruments/videomancer/pegboard/pegboard_ex1_s1.png';
import pegboard_ex1_s2 from '/img/instruments/videomancer/pegboard/pegboard_ex1_s2.png';
import pegboard_ex1_s3 from '/img/instruments/videomancer/pegboard/pegboard_ex1_s3.png';
import pegboard_ex1_s4 from '/img/instruments/videomancer/pegboard/pegboard_ex1_s4.png';
import pegboard_ex1_s5 from '/img/instruments/videomancer/pegboard/pegboard_ex1_s5.png';
import pegboard_ex1_s6 from '/img/instruments/videomancer/pegboard/pegboard_ex1_s6.png';
import pegboard_ex2_s1 from '/img/instruments/videomancer/pegboard/pegboard_ex2_s1.png';
import pegboard_ex2_s2 from '/img/instruments/videomancer/pegboard/pegboard_ex2_s2.png';
import pegboard_ex2_s3 from '/img/instruments/videomancer/pegboard/pegboard_ex2_s3.png';
import pegboard_ex2_s4 from '/img/instruments/videomancer/pegboard/pegboard_ex2_s4.png';
import pegboard_ex2_s5 from '/img/instruments/videomancer/pegboard/pegboard_ex2_s5.png';
import pegboard_ex2_s6 from '/img/instruments/videomancer/pegboard/pegboard_ex2_s6.png';
import pegboard_ex3_s1 from '/img/instruments/videomancer/pegboard/pegboard_ex3_s1.png';
import pegboard_ex3_s2 from '/img/instruments/videomancer/pegboard/pegboard_ex3_s2.png';
import pegboard_ex3_s3 from '/img/instruments/videomancer/pegboard/pegboard_ex3_s3.png';
import pegboard_ex3_s4 from '/img/instruments/videomancer/pegboard/pegboard_ex3_s4.png';
import pegboard_ex3_s5 from '/img/instruments/videomancer/pegboard/pegboard_ex3_s5.png';
import pegboard_ex3_s6 from '/img/instruments/videomancer/pegboard/pegboard_ex3_s6.png';

# Pegboard

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: pegboard_source1_boat, after: pegboard_hero_s1 },
    { label: "Runner", before: pegboard_source2_runner, after: pegboard_hero_s2 },
    { label: "Elephant", before: pegboard_source3_elephant, after: pegboard_hero_s3 },
    { label: "Pattern", before: pegboard_source4_pattern, after: pegboard_hero_s4 },
    { label: "Woman", before: pegboard_source5_woman, after: pegboard_hero_s5 },
    { label: "Knit", before: pegboard_source6_knit, after: pegboard_hero_s6 },
  ]}
/>
*Pegboard rendering a live camera feed as glowing Lite-Brite pegs snapped to an eight-color palette on a dark field.*

---

## Overview

Before LCD panels and OLED screens, there was Lite-Brite — a toy that turned translucent colored pegs into glowing pictures when backlit. You placed plastic pegs into a perforated black board, and the light shining through each peg created a mosaic of bright dots against a dark field. Pegboard recreates this aesthetic in the video domain: it divides each frame into a grid of cells, samples the input color at each cell center, snaps that color to an eight-entry palette, and renders each cell as a glowing circular peg on a black background.

The result is a striking transformation that reduces continuous video to a constellation of colored dots. Complex images simplify into patterns of pure, saturated color. The peg grid is adjustable from dense (4-pixel cells) to coarse (32-pixel cells), and each peg's radius, glow softness, and brightness are continuously variable. A "Full Color" mode bypasses the palette snap to preserve the input's full color range while maintaining the peg rendering geometry.

At its simplest, Pegboard is a spatial quantizer with artistic output — it reduces spatial resolution while adding shape, glow, and optional color reduction. At its most expressive, it transforms live video into animated light-peg art with bloom halos and invertible contrast.

---

## Background

### Lite-Brite and Peg Art Tradition

Lite-Brite, introduced by Hasbro in 1967, was one of the first commercial products to combine geometry and light for consumer art-making. The user placed colored translucent pegs into a black backing board, and a light bulb behind the board made each peg glow. The aesthetic — bright saturated dots on a dark field, arranged in a regular grid — became iconic. Pegboard digitizes this concept, treating each video frame as a backing board and each grid cell as a peg slot.

### Color Palette Quantization

The Lite-Brite set shipped with pegs in a limited number of colors: red, blue, green, yellow, orange, pink, violet, and white. Pegboard encodes these eight colors as fixed YUV values in an FPGA lookup table. For each grid cell, the sampled input color is compared against all eight palette entries using Manhattan distance in YUV space (|ΔY| + |ΔU| + |ΔV|), and the nearest match wins. This is a form of nearest-neighbor color quantization — the continuous color space of the input is collapsed to eight distinct hues.

The Manhattan distance metric is computationally lighter than Euclidean distance (no square root needed) while still producing perceptually reasonable results. Because the comparison is parallel across all eight entries, the palette snap completes in a single clock cycle.

### Radial Glow and Falloff

Real Lite-Brite pegs glow brightest at the center and fade at the edges because light scatters through the translucent plastic. Pegboard simulates this with a radial falloff function: within each peg, the brightness decreases with distance squared from the cell center. The Glow Softness control adjusts how rapidly the falloff occurs — low values produce a sharp-edged dot, high values produce a soft halo that blends into the background. An optional bloom zone extends slightly beyond the peg radius, rendering a dim halo of the peg's color to simulate light bleeding.

### Cell-Based Rendering

The frame is divided into a regular square grid. Cell size is selectable from eight presets: 4, 6, 8, 12, 16, 20, 24, or 32 pixels. Within each cell, a modular counter tracks the position relative to the cell origin. At the cell center, the input video's YUV values are sampled and held for the entire cell — this is the "sample and hold" operation that determines each peg's color. The pixel's distance from the cell center then determines whether it falls inside the peg, inside the bloom zone, or in the background gap.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Timing + Counters ──────────────────────────────────────────
│   ├─ Video Timing Generator (sync edge detection)
│   ├─ Pixel Counters (hcount, vcount)
│   ├─ Cell Position (cell_x, cell_y mod cell_size)
│   ├─ Cell Size Selection (top 3 bits of Pot 1 → 8 presets)
│   └─ Cell Center Detection (at_center flag)
│
├── Sample + Hold (1 clk) ─────────────────────────────────────
│   └─ Latch input YUV at cell center, hold for entire cell
│
├── Stage 1: Palette Snap (1 clk) ─────────────────────────────
│   ├─ Full Color off: Manhattan distance to 8 palette entries
│   │   → nearest palette color (Y, U, V)
│   └─ Full Color on: bypass palette, apply saturation scaling
│
├── Stage 2: Circle/Square Test + Distance (1 clk) ────────────
│   ├─ |dx|, |dy| from cell center
│   ├─ dist_sq = dx² + dy²
│   ├─ radius = peg_radius × cell_half / 1024
│   ├─ Circle: inside = (dist_sq ≤ radius²)
│   ├─ Square: inside = (|dx| ≤ radius AND |dy| ≤ radius)
│   └─ Bloom zone = slightly larger radius test
│
├── Stage 3: Color Compose (1 clk) ────────────────────────────
│   ├─ Inside peg: radial falloff × brightness × peg color
│   ├─ Bloom zone: dimmed peg color (÷8)
│   ├─ Background: background brightness (neutral chroma)
│   └─ Invert: dark pegs on light (900 - peg_Y) background
│
├── Stage 4: Output Register (1 clk) ──────────────────────────
│
├── Mix (4 clk × 3 channels via interpolator_u) ───────────────
│   └─ Wet/dry blend: a=delayed_input, b=processed, t=Mix
│
├── Bypass ─────────────────────────────────────────────────────
│   └─ Select delayed input or mixed signal
│
└── Sync ───────────────────────────────────────────────────────
    └─ Delayed sync (hsync, vsync, field, avid)
```

The sample-and-hold is the critical stage: each cell's color is determined by a single pixel at the cell center, then held constant for the entire cell. This means the spatial sampling is aliased by design — small features that don't fall on cell centers are missed entirely. The grid alignment is fixed (no sub-pixel offset), so the spatial relationship between the source content and the peg grid creates moire and aliasing patterns that shift as the source moves.

The palette snap and the circle/square rendering are independent operations. Palette snap determines *what color* the peg is; the distance test determines *where* the peg appears. This separation means you can change peg shape and size without affecting color, and vice versa.

---

## Parameter Reference

<img src={pegboard_control_panel} alt="Videomancer front panel with Pegboard loaded"/>
*Videomancer's front panel with Pegboard active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Peg Size
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 2 |

Selects the peg grid cell size from eight presets: 4, 6, 8, 12, 16, 20, 24, or 32 pixels per cell. The top three bits of the register value select the preset. Smaller cells produce denser grids with more pegs and finer spatial resolution. Larger cells produce fewer, bigger pegs with coarser spatial sampling. At the smallest setting (4 pixels), the pegs are barely visible as individual dots. At the largest (32 pixels), each peg is a prominent circle that can span significant frame area.

---

#### Knob 2 — Peg Radius
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 62.6% |
| Suffix | % |

Controls the peg radius within each cell, expressed as a fraction of the cell half-size. At 0%, the peg shrinks to a single pixel at the center. At 100%, the peg extends to the cell boundary, filling the entire cell with no gap between adjacent pegs. The radius is clamped to a minimum of 1 pixel. For circle mode, the test is Euclidean (dx² + dy² ≤ r²); for square mode, it checks each axis independently (|dx| ≤ r AND |dy| ≤ r).

---

#### Knob 3 — Glow Soft
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Adjusts the radial glow falloff within each peg. The falloff is computed from the difference between the radius squared and the distance squared, then shifted right by a glow-dependent amount. Low softness values produce sharp-edged pegs with uniform brightness. Higher values produce a gentler falloff where the peg brightness fades gradually from center to edge, simulating the translucent glow of a real Lite-Brite peg.

---

#### Knob 4 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the overall peg brightness. The peg's palette color (or input color in Full Color mode) is multiplied by this value. At 0%, the pegs are black. At 100%, the peg renders at full palette brightness. Values in between produce dimmer pegs. This interacts with the radial falloff — the falloff attenuates from this brightness level, so lower brightness produces subtler glow gradients.

---

#### Knob 5 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls chroma intensity in Full Color mode. When Full Color is active, the input U and V channels are centered, scaled by this value, then re-centered. At 0%, the pegs become monochrome (neutral chroma). At 100%, the input saturation is preserved. This control has no effect in palette mode — palette colors are fixed and unaffected by saturation scaling.

---

#### Knob 6 — Background
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the brightness of the background gaps between pegs. At 0%, the background is fully black — the classic Lite-Brite look. Increasing this value raises the background luma, reducing contrast between pegs and gaps. Background chroma is always neutral (U = V = 512). In invert mode, the background becomes bright (fixed at 900) regardless of this setting.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Full Color** | Palette | Full |
| **8 — Peg Shape** | Circle | Square |
| **9 — Bloom** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control independent rendering options. Full Color and Peg Shape affect the peg content and geometry respectively. Bloom adds a halo effect. Invert reverses the brightness relationship between pegs and background. Bypass passes the original video through unchanged.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix between the original input video and the peg-rendered output. At 0%, the output is the unprocessed input. At 100%, the output is fully processed. Intermediate values blend the two via linear interpolation across all three YUV channels. This allows subtle integration of the peg effect into the source image.

---

## Guided Exercises

These exercises progress from basic peg rendering through color manipulation to advanced bloom and inversion effects. Each engages different aspects of the Lite-Brite simulation.

### Exercise 1: Classic Lite-Brite

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: pegboard_source1_boat, after: pegboard_ex1_s1 },
    { label: "Runner", before: pegboard_source2_runner, after: pegboard_ex1_s2 },
    { label: "Elephant", before: pegboard_source3_elephant, after: pegboard_ex1_s3 },
    { label: "Pattern", before: pegboard_source4_pattern, after: pegboard_ex1_s4 },
    { label: "Woman", before: pegboard_source5_woman, after: pegboard_ex1_s5 },
    { label: "Knit", before: pegboard_source6_knit, after: pegboard_ex1_s6 },
  ]}
/>
*Classic Lite-Brite — simulated result across source images.*
**Source**: A live camera feed or recorded footage with strong, varied colors — fruit bowls, flower arrangements, or color bar patterns work well.

**Objective**: Create the classic Lite-Brite look: bright colored pegs on a black background with palette-quantized color.

1. **Set grid size**: Start with Peg Size at step 4 (16-pixel cells) for clearly visible individual pegs.
2. **Adjust radius**: Set Peg Radius to about 60%. The pegs should have visible black gaps between them.
3. **Observe palette snap**: With Full Color off (Palette mode), watch how the input colors quantize to the eight Lite-Brite colors. Move the camera slowly to see different regions snap between palette entries.
4. **Adjust glow**: Increase Glow Soft to add a soft falloff within each peg. Compare sharp pegs (low softness) with glowing pegs (high softness).
5. **Brightness**: Set Brightness to about 75% for a natural peg glow level.
6. **Black background**: Keep Background at 0% for the classic dark-field look.

**Key concepts**: Cell-based sample-and-hold spatial quantization, Manhattan distance palette matching, radial glow falloff as a function of distance squared

---

### Exercise 2: Full Color Mosaic with Saturation

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: pegboard_source1_boat, after: pegboard_ex2_s1 },
    { label: "Runner", before: pegboard_source2_runner, after: pegboard_ex2_s2 },
    { label: "Elephant", before: pegboard_source3_elephant, after: pegboard_ex2_s3 },
    { label: "Pattern", before: pegboard_source4_pattern, after: pegboard_ex2_s4 },
    { label: "Woman", before: pegboard_source5_woman, after: pegboard_ex2_s5 },
    { label: "Knit", before: pegboard_source6_knit, after: pegboard_ex2_s6 },
  ]}
/>
*Full Color Mosaic with Saturation — simulated result across source images.*
**Source**: Footage with subtle color variation — landscapes, skin tones, or gradients.

**Objective**: Explore Full Color mode and saturation control for a photographic peg mosaic.

1. **Enable Full Color**: Toggle Full Color to "Full". The pegs now show the actual sampled input color instead of snapping to the eight-color palette.
2. **Reduce saturation**: Lower Saturation to about 50%. The pegs desaturate, retaining tonal variation but losing color intensity.
3. **Increase saturation**: Push Saturation to 100%. Colors become vivid.
4. **Zero saturation**: Set Saturation to 0%. The pegs become a monochrome mosaic — brightness-only peg art.
5. **Switch to square pegs**: Toggle Peg Shape to "Square". With full radius, the squares tile seamlessly — a pure color mosaic without gaps.
6. **Vary cell size**: Step through Peg Size presets. Watch the mosaic resolution change from fine photographic pixels to coarse color blocks.

**Key concepts**: Full Color bypasses palette quantization, saturation scales centered chroma channels, square pegs at full radius produce gap-free mosaic tiling

---

### Exercise 3: Blooming Inverted Pegs

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: pegboard_source1_boat, after: pegboard_ex3_s1 },
    { label: "Runner", before: pegboard_source2_runner, after: pegboard_ex3_s2 },
    { label: "Elephant", before: pegboard_source3_elephant, after: pegboard_ex3_s3 },
    { label: "Pattern", before: pegboard_source4_pattern, after: pegboard_ex3_s4 },
    { label: "Woman", before: pegboard_source5_woman, after: pegboard_ex3_s5 },
    { label: "Knit", before: pegboard_source6_knit, after: pegboard_ex3_s6 },
  ]}
/>
*Blooming Inverted Pegs — simulated result across source images.*
**Source**: High-contrast material — spotlit subjects, neon signs, or black-and-white graphics.

**Objective**: Combine bloom and invert modes for stylized negative-space peg effects.

1. **Set up basic pegs**: Medium grid (Peg Size step 5, 20px), moderate radius (~50%), Palette mode.
2. **Enable Bloom**: Toggle Bloom on. Observe the dim halo around each peg — a colored fringe extending just past the peg edge.
3. **Enable Invert**: Toggle Invert on. The pegs become dark cutouts in a bright field. The bloom halo also inverts.
4. **Adjust brightness**: Lower Brightness. In invert mode, this makes the dark pegs lighter (closer to background), reducing contrast.
5. **Raise background**: Increase Background. In normal mode this lightens the gaps. In invert mode, the background is fixed at 900.
6. **Mix blend**: Reduce the Mix fader to ~50%. The inverted peg pattern ghosts over the original image.

**Key concepts**: Bloom extends the peg boundary with a dimmed color halo, invert reverses the brightness relationship (900 - peg_Y), Mix fader allows partial overlay of the effect on the source

---


## Tips

- **Cell size is the master control**: Peg Size determines the spatial resolution of the entire effect. Start here, then adjust radius and glow to taste.
- **Full radius square pegs = mosaic**: Square pegs at 100% radius fill their cells completely, producing a gap-free color mosaic. This is useful as a spatial quantizer without the peg aesthetic.
- **Palette mode for graphic impact**: The eight-color palette creates bold, poster-like imagery. Full Color mode is subtler and more photographic. Switch between them for dramatically different results from the same source.
- **Bloom adds depth**: The bloom halo is subtle (÷8 brightness) but adds a sense of light emission around each peg. Most visible with dark backgrounds and moderate peg radius.
- **Invert for negative space**: Inverted pegs create dark holes in a bright field — the opposite of Lite-Brite. This looks especially striking with Bloom, where the halo becomes a dark fringe around each hole.
- **Mix for ghost overlay**: Partial mix values overlay the peg pattern on the source video, creating a grid texture over the original image. This is useful for subtle spatial quantization effects.
- **Feedback amplifies quantization**: Route the output back to the input. The palette snap becomes recursive — already-quantized colors snap more cleanly to palette entries, and the peg grid creates increasingly geometric patterns.
- **Background brightens the gaps**: Increasing Background from zero reduces the "dark field" contrast. At high values, the pegs barely stand out. At zero, the pegs glow against pure black.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bloom** | A rendered halo just outside the peg radius, simulating light bleeding from a translucent peg into the surrounding dark field. |
| **Cell** | A square grid region of fixed pixel size. Each cell renders one peg at its center. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Euclidean Distance** | Distance measured as the square root of dx² + dy²; Pegboard uses distance-squared to avoid the square root. |
| **Falloff** | The radial decrease in brightness from the peg center to its edge, simulating translucent glow. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Lite-Brite** | A 1967 Hasbro toy that creates glowing images by placing translucent colored pegs into a backlit perforated board. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Manhattan Distance** | The sum of absolute differences along each axis (|ΔY| + |ΔU| + |ΔV|); used for palette color matching. |
| **Mosaic** | A visual pattern composed of small uniform-color blocks arranged in a grid. |
| **Palette Quantization** | Reducing a continuous color space to a fixed set of representative colors by nearest-neighbor matching. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Sample and Hold** | Capturing a signal value at one instant (the cell center) and maintaining it for a duration (the entire cell). |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
