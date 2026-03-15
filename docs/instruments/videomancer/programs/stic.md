---
draft: false
sidebar_position: 286
slug: /instruments/videomancer/stic
title: "STIC"
image: /img/instruments/videomancer/stic/stic_hero_s1.png
description: "STIC transforms incoming video into the restricted visual language of the Mattel Intellivision game console."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import stic_control_panel from '/img/instruments/videomancer/stic/stic_control_panel.png';
import stic_source1_ballerina from '/img/instruments/videomancer/stic/stic_source1_ballerina.png';
import stic_source2_castle from '/img/instruments/videomancer/stic/stic_source2_castle.png';
import stic_source3_elephant from '/img/instruments/videomancer/stic/stic_source3_elephant.png';
import stic_source4_pattern from '/img/instruments/videomancer/stic/stic_source4_pattern.png';
import stic_source5_girl from '/img/instruments/videomancer/stic/stic_source5_girl.png';
import stic_source6_knit from '/img/instruments/videomancer/stic/stic_source6_knit.png';
import stic_hero_s1 from '/img/instruments/videomancer/stic/stic_hero_s1.png';
import stic_hero_s2 from '/img/instruments/videomancer/stic/stic_hero_s2.png';
import stic_hero_s3 from '/img/instruments/videomancer/stic/stic_hero_s3.png';
import stic_hero_s4 from '/img/instruments/videomancer/stic/stic_hero_s4.png';
import stic_hero_s5 from '/img/instruments/videomancer/stic/stic_hero_s5.png';
import stic_hero_s6 from '/img/instruments/videomancer/stic/stic_hero_s6.png';
import stic_ex1_s1 from '/img/instruments/videomancer/stic/stic_ex1_s1.png';
import stic_ex1_s2 from '/img/instruments/videomancer/stic/stic_ex1_s2.png';
import stic_ex1_s3 from '/img/instruments/videomancer/stic/stic_ex1_s3.png';
import stic_ex1_s4 from '/img/instruments/videomancer/stic/stic_ex1_s4.png';
import stic_ex1_s5 from '/img/instruments/videomancer/stic/stic_ex1_s5.png';
import stic_ex1_s6 from '/img/instruments/videomancer/stic/stic_ex1_s6.png';
import stic_ex2_s1 from '/img/instruments/videomancer/stic/stic_ex2_s1.png';
import stic_ex2_s2 from '/img/instruments/videomancer/stic/stic_ex2_s2.png';
import stic_ex2_s3 from '/img/instruments/videomancer/stic/stic_ex2_s3.png';
import stic_ex2_s4 from '/img/instruments/videomancer/stic/stic_ex2_s4.png';
import stic_ex2_s5 from '/img/instruments/videomancer/stic/stic_ex2_s5.png';
import stic_ex2_s6 from '/img/instruments/videomancer/stic/stic_ex2_s6.png';
import stic_ex3_s1 from '/img/instruments/videomancer/stic/stic_ex3_s1.png';
import stic_ex3_s2 from '/img/instruments/videomancer/stic/stic_ex3_s2.png';
import stic_ex3_s3 from '/img/instruments/videomancer/stic/stic_ex3_s3.png';
import stic_ex3_s4 from '/img/instruments/videomancer/stic/stic_ex3_s4.png';
import stic_ex3_s5 from '/img/instruments/videomancer/stic/stic_ex3_s5.png';
import stic_ex3_s6 from '/img/instruments/videomancer/stic/stic_ex3_s6.png';

# STIC

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: stic_source1_ballerina, after: stic_hero_s1 },
    { label: "Castle", before: stic_source2_castle, after: stic_hero_s2 },
    { label: "Elephant", before: stic_source3_elephant, after: stic_hero_s3 },
    { label: "Pattern", before: stic_source4_pattern, after: stic_hero_s4 },
    { label: "Girl", before: stic_source5_girl, after: stic_hero_s5 },
    { label: "Knit", before: stic_source6_knit, after: stic_hero_s6 },
  ]}
/>
*STIC rendering a live camera feed through 16-color Intellivision palette quantization with Color Stack background cycling.*

---

## Overview

STIC transforms incoming video into the restricted visual language of the Mattel Intellivision game console. Every pixel of the input is matched against the console's fixed 16-color palette using Manhattan distance in YUV space, then rendered through one of two authentic display modes: Color Stack, where each tile shows a foreground color on a cycling background, or Colored Squares, where each tile is subdivided into four independently quantized quadrant blocks. The result is a living mosaic of flat, bright colors that looks like a lost Intellivision game running on real hardware.

The name refers to the **Standard Television Interface Chip** (AY-3-8900), the custom IC at the heart of the Intellivision's video display system. The real STIC imposed severe constraints — 16 colors, 8x8 tile cells, a 4-entry rotating Color Stack for backgrounds, and a crude 4x4-block subdivision mode called Colored Squares. This program faithfully recreates those constraints as a video effect, applying them to any live video signal rather than rendering pre-authored game graphics.

At conservative settings — large tile sizes with the Color Stack cycling slowly — the effect is a gentle, painterly quantization that suggests watercolor blocks. At extreme settings — small tiles, fast stack cycling, scanlines and sprite flicker enabled — the result is an aggressive retro simulation, complete with the characteristic visual artifacts of 1980s console hardware.

---

## Background

### The Intellivision Display Architecture

The Mattel Intellivision, released in 1979, used a custom **STIC** (Standard Television Interface Chip, part number AY-3-8900) to generate its video output. Unlike the Atari 2600's scanline-by-scanline rendering, the STIC worked with a tile-based framebuffer: the screen was divided into a grid of 8x8 pixel cells, and each cell referenced a character from a pattern table. The chip supported exactly 16 colors, derived from a fixed analog palette encoded directly in the silicon. This program recreates that palette in YUV space and applies the STIC's two principal rendering modes to arbitrary video input.

### Color Stack Mode

The STIC's **Color Stack** was a memory-saving mechanism for assigning background colors. Instead of storing a separate background color for each tile, the chip maintained a rotating stack of four color entries. As tiles were rendered left-to-right, top-to-bottom, the background color was drawn from the current stack position. A tile could optionally advance the stack pointer, cycling to the next entry. Game designers used this to create color gradients and region changes across the screen with minimal memory. In this program, the Stack Hue control selects the base palette entry, and four colors spaced evenly around the palette (offsets 0, 4, 8, 12 from the base) form the rotating stack.

### Colored Squares Mode

For even coarser graphics, the STIC offered a **Colored Squares** mode where each 8x8 tile was subdivided into four 4x4 quadrant blocks. Each quadrant could independently display one of the STIC foreground colors. Games like *Snafu* and *Checkers* used this mode for their abstract, ultra-blocky graphics. In this program, Colored Squares mode re-samples the input video at each quadrant boundary, independently quantizing each sub-block to the nearest palette entry, producing a mosaic four times finer than the tile grid.

### Palette Quantization via Manhattan Distance

The program maps each input pixel to the nearest color in the Intellivision's 16-color palette. The distance metric is **Manhattan distance** (also called taxicab or L1 distance) computed across the three YUV channels: the sum of the absolute differences in Y, U, and V between the input pixel and each palette entry. Manhattan distance is computationally cheaper than Euclidean distance — it requires only subtractions and additions, no multiplications or square roots — making it well-suited for per-pixel FPGA processing. The matching pipeline processes all 16 entries over five pipeline stages using a pairwise tournament reduction.

### CRT Simulation Effects

Two additional processing stages simulate the look of Intellivision games displayed on 1980s CRT televisions. **Scanline dimming** reduces the luminance of every other display line to 75%, emulating the visible gap between phosphor rows on an interlaced CRT. **Sprite flicker** simulates the characteristic blinking that occurred when the Intellivision's EXEC framework tried to display more sprites than the STIC's hardware limit allowed — the EXEC would alternate which sprites were visible each frame, creating a 20 Hz flicker. The program simulates this by dimming one out of every three frames.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
|
+-- All Channels -----------------------------------------------
|   |
|   +- 1. Input Register          (latch Y/U/V + timing detection)
|   +- 2. Tile Tracking           (cell position, quadrant tracking,
|   |                               Color Stack state)
|   +- 3. Palette Distance A      (Manhattan dist for entries 0-3)
|   +- 4. Reduce A + Distance B   (min of 0-3, dist for entries 4-7)
|   +- 5. Reduce AB + Distance C  (min of 0-7, dist for entries 8-11)
|   +- 6. Reduce ABC + Distance D (min of 0-11, dist for entries 12-15)
|   +- 7. Final Winner            (best match from all 16 entries)
|   +- 8. Mode Mux + Post         (Color Stack / Colored Squares,
|   |                               brightness, saturation, grid,
|   |                               scanline dim, sprite flicker)
|   +- 9. Interpolator Mix        (wet/dry crossfade, 4 clk x3)
|
+-- Sync Signals -----------------------------------------------
|   +-- 12-clock delay pipeline (hsync, vsync, field, data bypass)
|
+-- Bypass -----------------------------------------------------
    +-- Select original or processed signal via Switch 11
```

The palette matching pipeline is the core of STIC. Input pixels are sampled and held at tile boundaries — once per tile in Color Stack mode, or re-sampled at each half-cell boundary in Colored Squares mode for per-quadrant matching. The held sample is then compared against all 16 palette entries over five pipelined clock stages using a tournament reduction: four groups of four entries are computed and reduced in parallel, then merged pairwise to find the overall best match. The foreground/background decision (driven by the Threshold control) and the Color Stack state are pipelined in parallel with the distance computation and merged at the mode mux stage. Brightness and saturation scaling are applied after the mode mux, followed by optional grid overlay, scanline dimming, and sprite flicker — all before the final wet/dry interpolator mix.

---

## Parameter Reference

<img src={stic_control_panel} alt="Videomancer front panel with STIC loaded"/>
*Videomancer's front panel with STIC active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Tile Size
| Property | Value |
|----------|-------|
| Range | 4px – 35px |
| Default | 16px |
| Suffix | px |

Controls the width and height of each tile cell in pixels. At the minimum setting, tiles are tiny (4 pixels wide) and the palette quantization creates a fine mosaic that preserves much of the source image's structure. At maximum, tiles grow to 35 pixels across, reducing the image to a very coarse grid of solid color blocks. Because both horizontal and vertical cell dimensions track this single control, the tiles are always roughly square. The tile size also determines the spacing of the Color Stack's rotation and the grid overlay lines.

---

#### Knob 2 — Stack Hue
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Selects the base hue for the Color Stack background. The 16 Intellivision palette colors are arranged by index, and this control steps through all 16 entries. The Color Stack then uses four colors spaced at intervals of 4 around the palette from this base — for example, selecting Blue (index 1) produces a stack of Blue, Green, Cyan, and Pink. Changing this control shifts the entire background color scheme while leaving foreground matching unchanged.

---

#### Knob 3 — Stack Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls how quickly the Color Stack advances through its four entries. At 0% the stack is nearly static — the same background color persists across many tiles. As the rate increases, the stack cycles faster, advancing more frequently and creating visible color banding across the screen. At maximum, the stack advances on nearly every tile, producing a rapid alternation of the four background colors that creates a shimmering, plaid-like effect behind the foreground content.

---

#### Knob 4 — Saturation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Scales the chrominance intensity of the output. At 0% the image becomes fully achromatic — all 16 palette colors collapse to their grayscale equivalents. At the default (approximately 75%), colors appear at their natural Intellivision saturation. Pushing above default toward 100% exaggerates the chroma differences between palette entries, creating vivid, poster-like color blocks. Internally, the U and V channels are offset from their midpoint (512), scaled by this control, and clamped.

---

#### Knob 5 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 22% |
| Suffix | % |

Sets the luminance threshold that separates foreground from background in Color Stack mode. Pixels whose Y value exceeds this threshold are rendered in the nearest palette match (foreground). Pixels below the threshold receive the current Color Stack background color. At 0%, nearly everything triggers as foreground and the background stack is rarely visible. At higher settings, only the brightest parts of the input qualify as foreground, and more of the image fills with the cycling background colors. In Colored Squares mode, this control has no effect because there is no foreground/background distinction.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scales the overall luminance of the palette-matched output. At 0% the image is completely dark. At the default (approximately 50%), the palette colors appear at their original brightness values. Increasing toward 100% brightens the output beyond the natural palette levels, which can wash out subtle color differences between palette entries. The brightness scaling is applied after the mode mux and before grid overlay and scanline effects, so grid lines maintain their own fixed brightness regardless of this control.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | ColorStk | ClrSqrs |
| **8 — Grid** | Off | On |
| **9 — Scanlines** | Off | On |
| **10 — Sprite Flk** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7-11 control five independent binary options. Mode (Switch 7) selects between the two STIC rendering modes and fundamentally changes the visual character. Grid, Scanlines, and Sprite Flicker (Switches 8-10) layer CRT simulation effects on top of the palette-quantized output. Bypass (Switch 11) is a standard processing bypass. These switches do not interact with each other — each enables or disables its named feature independently.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 100 |

Controls the wet/dry mix between the processed STIC output and the original input signal. At 100% (fully clockwise), only the processed signal is output. As the fader is reduced, the original input is blended in proportionally via a per-channel linear interpolator. At 0%, the output is entirely dry (original signal). Intermediate settings create a ghostly overlay where the palette-quantized image sits on top of the original video, which can be useful for alignment or for a subtle retro tinting effect.





---

## Guided Exercises

These exercises progress from basic palette quantization to full retro console simulation, each building on the previous by engaging more of the STIC rendering pipeline.

### Exercise 1: Palette Quantization

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: stic_source1_ballerina, after: stic_ex1_s1 },
    { label: "Castle", before: stic_source2_castle, after: stic_ex1_s2 },
    { label: "Elephant", before: stic_source3_elephant, after: stic_ex1_s3 },
    { label: "Pattern", before: stic_source4_pattern, after: stic_ex1_s4 },
    { label: "Girl", before: stic_source5_girl, after: stic_ex1_s5 },
    { label: "Knit", before: stic_source6_knit, after: stic_ex1_s6 },
  ]}
/>
*Palette Quantization — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a range of colors — faces, foliage, sky, and saturated objects work well.

1. **Default start**: With all controls at default, observe how the input video is quantized to flat blocks of Intellivision colors. Notice that smooth gradients become abrupt steps between palette entries.
2. **Tile size**: Sweep Tile Size from minimum to maximum. At small sizes, the mosaic is fine and the source is recognizable. At large sizes, the image becomes a coarse grid of solid color blocks.
3. **Threshold sweep**: In Color Stack mode, slowly increase Threshold. Watch as darker parts of the image flip from foreground (palette-matched) to background (stack color), gradually replacing the source with the cycling stack.
4. **Saturation**: Reduce Saturation to 0%. The 16 colors collapse to their grayscale equivalents. Bring it back up to observe how the palette entries separate in chroma space.
5. **Brightness**: Sweep Brightness across its range. Note that very low settings crush all palette colors toward black, while high settings wash them toward white.

**Key concepts**: Manhattan distance palette matching, foreground/background separation via luminance threshold, saturation and brightness as post-quantization processing

---

### Exercise 2: Color Stack and Colored Squares

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: stic_source1_ballerina, after: stic_ex2_s1 },
    { label: "Castle", before: stic_source2_castle, after: stic_ex2_s2 },
    { label: "Elephant", before: stic_source3_elephant, after: stic_ex2_s3 },
    { label: "Pattern", before: stic_source4_pattern, after: stic_ex2_s4 },
    { label: "Girl", before: stic_source5_girl, after: stic_ex2_s5 },
    { label: "Knit", before: stic_source6_knit, after: stic_ex2_s6 },
  ]}
/>
*Color Stack and Colored Squares — simulated result across source images.*
**Source**: High-contrast footage — graphic design elements, text on colored backgrounds, or geometric patterns.

1. **Color Stack mode**: Set Mode to ColorStk. Set Stack Rate to about 50% and observe the background color cycling across the tile grid as a slow color gradient behind the foreground content.
2. **Stack Hue selection**: Step through Stack Hue values. Each base hue produces a different quartet of background colors spaced around the palette.
3. **Fast cycling**: Increase Stack Rate to maximum. The background becomes a rapid plaid-like alternation of four colors.
4. **Switch to Colored Squares**: Toggle Mode to ClrSqrs. The tile structure changes — each tile now shows four independently colored quadrants. The Color Stack background and Threshold controls no longer affect the output.
5. **Grid overlay**: Enable Grid (Switch 8). The tile boundaries become visible as dark lines, revealing the cell structure in both modes.
6. **Compare**: Toggle between ColorStk and ClrSqrs to see how the same source renders differently — Color Stack shows foreground/background separation while Colored Squares shows per-quadrant detail.

**Key concepts**: Color Stack rotating background, Colored Squares quadrant subdivision, mode differences in spatial resolution and color assignment

---

### Exercise 3: Full Retro Console Simulation

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: stic_source1_ballerina, after: stic_ex3_s1 },
    { label: "Castle", before: stic_source2_castle, after: stic_ex3_s2 },
    { label: "Elephant", before: stic_source3_elephant, after: stic_ex3_s3 },
    { label: "Pattern", before: stic_source4_pattern, after: stic_ex3_s4 },
    { label: "Girl", before: stic_source5_girl, after: stic_ex3_s5 },
    { label: "Knit", before: stic_source6_knit, after: stic_ex3_s6 },
  ]}
/>
*Full Retro Console Simulation — simulated result across source images.*
**Source**: Any footage — this exercise is about layering all CRT and console simulation effects together.

1. **Base rendering**: Set Tile Size to about 37% and use Color Stack mode with a moderate Stack Rate. Set Threshold so there is a clear foreground/background split.
2. **Grid**: Enable Grid to make tile boundaries visible. The image now looks like a character display.
3. **Scanlines**: Enable Scanlines. Every other line dims, adding horizontal banding that simulates a CRT raster display.
4. **Sprite flicker**: Enable Sprite Flk. A subtle pulsing appears as every third frame dims, simulating the Intellivision's sprite multiplexing flicker.
5. **Saturation boost**: Increase Saturation above default to make the palette colors pop against the scanline dimming. The CRT simulation effects now work together to create a convincing retro display.
6. **Mix blend**: Pull the Mix fader to about 70% to blend the retro-processed image with the original, creating a ghostly overlay effect.
7. **A/B compare**: Toggle Bypass on and off to compare the full simulation against the raw input.

**Key concepts**: Scanline dimming simulates CRT raster, sprite flicker simulates hardware sprite limits, combining post-processing effects creates convincing retro aesthetics

---


## Tips

- **Tile Size is the master control**: It sets the spatial resolution of the entire pipeline — palette matching, Color Stack cycling, grid spacing, and quadrant subdivision all depend on it. Start here when dialing in a look.
- **Threshold only matters in Color Stack mode**: In Colored Squares mode, every pixel is rendered as foreground. Switch to Color Stack mode to use the foreground/background separation.
- **Stack Hue offsets by 4**: The four Color Stack entries are spaced at palette indices 0, 4, 8, and 12 from the base hue. Choose stack hues whose quartets create pleasing combinations — Blue (1) gives Blue/Green/Cyan/Pink; Red (2) gives Red/Yellow/Orange/Yellow-Green.
- **Scanlines and flicker compound with brightness**: Because scanline dimming and sprite flicker reduce luminance, moderate boosts to Brightness or Saturation can compensate for the overall darkening.
- **Mix for tinting**: At intermediate Mix settings, the palette-quantized output overlays the original video — useful for creating a retro color tint without completely destroying the source.
- **Feedback loops**: Routing the STIC output back to the input creates recursive palette quantization — colors lock harder to the palette with each pass, and the Color Stack pattern becomes self-referencing.
- **Bypass for A/B comparison**: Switch 11 instantly reverts to the original signal, making it easy to evaluate the strength of the retro effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **AY-3-8900** | The part number for the Intellivision's Standard Television Interface Chip, a custom video display IC manufactured by General Instrument. |
| **BRAM** | Block RAM; dedicated memory blocks on an FPGA die, used for delay lines and lookup tables. |
| **Color Stack** | A memory-saving technique used by the Intellivision STIC where background colors are drawn from a rotating 4-entry stack rather than stored per tile. |
| **Colored Squares** | A STIC display mode that subdivides each 8x8 tile into four 4x4 quadrant blocks, each independently colored. |
| **CRT** | Cathode Ray Tube; the display technology used by televisions in the Intellivision era, characterized by visible scanlines and phosphor persistence. |
| **EXEC** | The Intellivision's built-in operating system ROM, responsible for sprite multiplexing and other system services. |
| **FPGA** | Field-Programmable Gate Array; reconfigurable digital logic hardware used to implement the Videomancer's video processing pipeline. |
| **LUT** | Lookup Table; a memory structure used to store pre-computed values, here used for the palette ROM. |
| **Manhattan Distance** | A distance metric computed as the sum of absolute differences along each axis, also called L1 distance or taxicab distance. |
| **Palette Quantization** | The process of mapping each pixel to the nearest entry in a fixed set of colors, reducing the color space. |
| **STIC** | Standard Television Interface Chip; the Intellivision's video display processor that this program emulates. |
| **YUV** | A color encoding system separating luminance (Y) from chrominance (U, V), used by analog and digital video standards. |

---
