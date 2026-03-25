---
draft: true
sidebar_position: 126
slug: /instruments/videomancer/gazette
title: "Gazette"
image: /img/instruments/videomancer/gazette/gazette_hero_s1.png
description: "Every home computer of the early 1980s faced the same engineering constraint: memory was expensive, and storing a unique color for every pixel on screen was a luxury none of them could afford."
---

![Gazette hero image](/img/instruments/videomancer/gazette/gazette_hero_s1.png)
*Gazette restricting a live video feed to the two-color-per-cell palette of a ZX Spectrum, producing characteristic attribute clash across the entire frame.*

---

## Overview

Gazette is a retro computing color restriction effect that divides the screen into character cells and forces each cell to display only two colors: an ***ink*** color and a ***paper*** color: drawn from one of four classic 8-bit computer palettes. The result is an authentic simulation of the display limitations that defined the visual identity of machines like the ZX Spectrum, the IBM CGA adapter, the Commodore 64, and the MSX standard.

The magic of Gazette lies in its per-cell color assignment. Each cell samples the luminance of the incoming video at its center point. Bright pixels adopt the ink color, while dark pixels adopt the paper color. The ink color itself is chosen from the palette based on that cell's brightness, so adjacent cells end up displaying different color pairs. This produces ***attribute clash***: the phenomenon where sharp color boundaries appear at cell edges because each cell is locked to its own two-color subset of the full palette.

Gazette goes beyond strict emulation by offering creative controls that the original hardware never had. **Color Bleed** simulates the horizontal chroma smear of composite video cables. **Flash** periodically swaps ink and paper, recreating the blinking text attribute found on many of these platforms. And **Cell Size** scales the character grid from tiny 4-pixel cells up to chunky 32-pixel blocks, letting you dial in the level of restriction from subtle to dramatic.

:::tip
Gazette is at its most visually striking with high-contrast source material. Faces, text, and geometric patterns all produce vivid attribute clash patterns.
:::

### What's In a Name?

A ***gazette*** is a newspaper or official journal: columns of ink on paper. The name plays on Gazette's core metaphor: every character cell is defined by exactly two values, ***ink*** and ***paper***, just as a printed gazette renders its text with dark ink pressed onto light paper. The name also nods to the Sinclair ZX Spectrum, whose BASIC language used the commands `INK` and `PAPER` to set character cell colors: a direct inspiration for this program's architecture.

---

## Quick Start

1. Feed a video signal into Videomancer and load **Gazette**. The image immediately snaps to the ZX Spectrum palette with visible character cell boundaries.
2. Turn **Palette** (Knob 5) to cycle through the four platform palettes: ZX Spectrum, CGA, C64, and MSX. Each has a different personality.
3. Adjust **Ink Bias** (Knob 2) clockwise while watching the image. The ink color brightens and shifts across the palette for each cell, changing the overall color palette of the image.
4. Toggle **Bright** (Switch 7) to **Bright** to switch from the dim, muted normal palette half to the vivid bright palette half.

---

## Parameters

![Videomancer front panel with Gazette loaded](/img/instruments/videomancer/gazette/gazette_control_panel.png)
*Videomancer's front panel with Gazette active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Cell Size

| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 2 |

**Cell Size** selects the width of each character cell in pixels. The four positions are 4, 8, 16, and 32 pixels wide. Smaller cells preserve more spatial detail from the source but create more frequent attribute boundaries. Larger cells produce a chunkier, more abstract look with fewer color transitions.

At the smallest setting (4 pixels), the image retains a surprising amount of recognizable detail despite the two-color restriction. At the largest setting (32 pixels), the screen becomes a coarse grid of bold color blocks (each one a miniature flag of ink and paper.)

:::note
The original ZX Spectrum used 8×8 pixel character cells. Set **Cell Size** to position 1 and **Cell Shape** to **Square** for the most authentic Spectrum look.
:::

---

### Knob 2 — Ink Bias

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Ink Bias** shifts the palette index used for the ink color in every cell. At its default position, the ink color is determined purely by the cell's sampled luminance: dark cells pick dark ink colors, bright cells pick bright ink colors. Increasing Ink Bias pushes all ink selections toward brighter palette entries, while decreasing it pulls them toward darker entries. This acts as a global tint control over the ink layer without affecting which pixels are classified as ink or paper.

The bias is added to the cell's luma value before the palette lookup, so the effect is most visible in mid-tone cells where a small push can jump to an entirely different color.

---

### Knob 3 — Paper Bias

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Paper Bias** selects the palette entry used for the paper (background) color across all cells. Unlike Ink Bias, this control is not modulated by cell luminance: every cell on screen shares the same paper color. At low values, paper is a dark color from the palette. As you increase Paper Bias, the paper color walks through the palette toward brighter entries.

The interaction between Ink Bias and Paper Bias defines the overall color scheme of the image. Pushing them apart creates high-contrast two-tone graphics; bringing them closer together produces subtle, low-contrast results where ink and paper nearly merge.

:::tip
Try setting Paper Bias to a mid-range value and slowly sweeping Ink Bias. The image cycles through dramatically different color schemes as the ink color walks through the palette entries.
:::

---

### Knob 4 — Threshold

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Threshold** biases the cutoff point that decides whether each pixel becomes ink or paper. At the center position (50%), the decision is based purely on the cell's sampled brightness: pixels brighter than the cell average become ink, and darker pixels become paper. Turning the knob clockwise raises the cutoff, meaning more of each cell becomes paper. Turning it counterclockwise lowers the cutoff, meaning more of each cell becomes ink.

At extreme settings, entire cells can flip to all-ink or all-paper, eliminating the two-tone texture within cells and reducing the image to blocks of solid color.

---

### Knob 5 — Palette

| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

**Palette** selects one of four classic 8-bit computer color palettes. Each palette contains 16 colors organized into two halves: 8 normal-intensity colors and 8 bright-intensity colors: sorted by luminance.

- **Position 0: ZX Spectrum**: The iconic 15-color palette (black appears in both halves) of the Sinclair ZX Spectrum. Bold primaries with no intermediate shades.
- **Position 1: CGA**: The 16-color palette of the IBM Color Graphics Adapter. Includes brown and two grays, giving it a warmer, more utilitarian feel.
- **Position 2: C64**: The Commodore 64's 16-color palette. Subtler than the Spectrum, with multiple grays and muted earth tones.
- **Position 3: MSX**: The MSX standard's TMS9918-derived palette. Warm reds and greens with a distinctive retro Japanese computer aesthetic.

---

### Knob 6 — Color Bleed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Color Bleed** simulates the horizontal chroma smearing that occurred when 8-bit computers connected to televisions via composite video cables. At zero, colors transition crisply at cell and pixel boundaries. As you increase Color Bleed, an ***IIR*** (infinite impulse response) low-pass filter smears the chroma channels horizontally, causing each pixel's color to bleed into its neighbors.

The filter operates at four discrete intensity levels: no bleed, 50% carry, 75% carry, and approximately 94% carry. At the highest setting, colors trail dramatically to the right, producing rainbow streaks reminiscent of a CRT television receiving a weak composite signal.

:::note
Color Bleed affects only the chroma (U and V) channels. Luminance transitions remain sharp regardless of the bleed setting, just as they did on real composite video hardware.
:::

---

### Switch 7 — Bright

| Property | Value |
|----------|-------|
| Off | Normal |
| On | Bright |
| Default | Normal |

**Bright** selects between the normal-intensity and bright-intensity halves of the current palette. In the **Normal** position, ink and paper colors are drawn from the first 8 entries of the palette: the dim, muted set. In the **Bright** position, colors are drawn from entries 8–15: the vivid, saturated set.

On the original ZX Spectrum, the BRIGHT attribute was a per-cell flag that doubled the intensity of both ink and paper. Gazette applies it globally, affecting all cells simultaneously.

---

### Switch 8 — Cell Shape

| Property | Value |
|----------|-------|
| Off | 8x1 Row |
| On | Square |
| Default | 8x1 Row |

**Cell Shape** determines the vertical extent of each character cell. In the **8×1 Row** position, each scan line independently samples and assigns cell colors, creating tall, narrow character cells that are one pixel high. In the **Square** position, cells extend vertically to match their horizontal width (4×4, 8×8, 16×16, or 32×32 pixels), and the cell color is sampled once at the center of the square.

The **Square** setting produces the most authentic retro computer look, since real hardware character cells were square or nearly square. The **8×1 Row** setting creates a finer vertical structure with line-by-line color variation, producing a distinctive moiré-like texture.

---

### Switch 9 — Black Paper

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Black Paper** forces the paper color to black (palette entry 0) regardless of the Paper Bias setting. This emulates the classic "bright text on a black background" appearance of most 8-bit computer displays. With Black Paper enabled, only the ink color varies per cell, producing a cleaner, higher-contrast result.

:::tip
Enable **Black Paper** and set **Bright** to **Bright** for the quintessential ZX Spectrum loading screen look (vivid colors floating on a jet-black background.)
:::

---

### Switch 10 — Flash

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Flash** periodically swaps the ink and paper colors in every cell. The swap occurs on a roughly half-second cycle (every 16 frames), recreating the blinking text attribute found on many 8-bit platforms. When Flash is **Off**, colors are stable. When Flash is **On**, the image alternates between normal and inverted color assignments, producing a rhythmic pulsing effect.

On the ZX Spectrum, FLASH was a per-character attribute for drawing attention to specific screen elements. Gazette applies it globally, affecting all cells at once.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the original input video directly to the output, bypassing all Gazette processing. Sync timing is still aligned through the delay pipeline, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the palette-restricted result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original input video and the Gazette-processed result. At 0% (fully down), the output is pure dry input. At 100% (fully up), the output is pure Gazette effect. Intermediate positions blend the two, allowing subtle color restriction overlays or gentle retro tinting.

The mix operates per-channel on Y, U, and V independently, so partial mix values produce a ghostly overlay of the palette-restricted image on top of the clean source.

---

## Background

### Attribute clash

The display hardware of 1980s home computers worked under severe memory constraints. A machine like the ZX Spectrum had only 6,912 bytes of video memory for a 256×192 pixel display: not nearly enough to store an independent color for every pixel. The solution was ***attribute-based color***: the screen was divided into 8×8 pixel character cells, and each cell stored a single byte specifying one ink color and one paper color. Every pixel within that cell could only be one of those two colors.

This memory-efficient scheme came with a famous trade-off. When a graphical element crossed a cell boundary, its colors would abruptly change at the cell edge, producing harsh color fringing that became known as ***attribute clash*** or ***color clash***. Artists and programmers spent enormous effort designing graphics that hid or worked around this limitation. Gazette embraces it as an aesthetic, applying the restriction to live video where the clash becomes part of the visual texture.

### Palette archaeology

Each of Gazette's four palettes reflects the design philosophy and hardware constraints of its era. The ZX Spectrum's palette is pure and mathematical: three bits of RGB plus one brightness bit, yielding 15 unique colors (black is duplicated across both halves). CGA introduced browns and grays, reflecting IBM's pragmatic office-computing roots. The C64's palette was hand-tuned by engineers for pleasing skin tones and natural colors on NTSC televisions, resulting in a distinctively warm, earthy set. The MSX palette derives from Texas Instruments' TMS9918 video chip, with its characteristic warm reds and cool greens.

All four palettes are stored in the FPGA as constant ROM arrays, pre-converted from RGB to YUV at ***elaboration time***: the moment when the FPGA design is compiled. This means the color conversion math runs on the synthesis computer, not in the FPGA hardware, keeping the runtime logic simple and fast.

### Composite video bleed

When 8-bit computers connected to televisions through composite video cables, the chroma (color) information was encoded as a high-frequency modulated signal riding on top of the luminance (brightness) signal. Television decoders separated these imperfectly, causing the color of each pixel to bleed horizontally into its neighbors. Sharp color transitions smeared into rainbow fringes, and adjacent colors would contaminate each other.

Gazette's **Color Bleed** control simulates this artifact using an ***IIR filter***: a feedback filter where each pixel's chroma output is a weighted mix of the current palette color and the previous pixel's output. At the strongest setting, the filter retains 94% of the previous value and adds only 6% of the new color, producing long, dramatic chroma trails that cascade across the screen.


---

## Signal Flow

### Signal Flow Notes

The pipeline's key interaction is between the BRAM column buffer and the palette index computation. At the center of each cell, the input luma is written into a 256-entry BRAM. On every subsequent pixel in that cell, the stored luma is read back and used to compute both the ink palette index and the threshold cutoff. This means the ink color and the ink-vs-paper decision are both driven by a single sample taken at the cell's center (not by the current pixel's brightness.)

The threshold mechanism deserves special attention. The cutoff is not a fixed value but an ***adaptive threshold***: `cell_luma + (threshold - 512)`. When Threshold is centered, the cutoff equals the cell's own brightness, so pixels brighter than average become ink and darker pixels become paper. Turning Threshold clockwise raises the bar, pushing more pixels into paper territory. This interaction between per-cell luma sampling and global threshold bias is what gives Gazette its characteristic texture.

:::tip
**Color Bleed resets at every line start.** The IIR filter state is cleared to neutral (512) at each horizontal sync, so bleed trails never wrap from the end of one line to the beginning of the next. This matches the behavior of real composite video decoders.
:::


---

## Exercises

These exercises progress from basic palette exploration to creative composite video simulation. Each one builds on the previous, gradually engaging more of Gazette's control surface.
### Exercise 1: ZX Spectrum Loading Screen

![ZX Spectrum Loading Screen result](/img/instruments/videomancer/gazette/gazette_ex1_s1.png)
*ZX Spectrum Loading Screen — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Recreate the look of a ZX Spectrum loading screen: vivid primary colors on a black background with visible 8×8 character cells.

#### Key Concepts

- Attribute clash creates color boundaries at cell edges
- Ink and paper combine to define the two-color character cell
- The Bright toggle switches between palette intensity halves

#### Video Source

A portrait or still image with clear tonal contrast (a face, a logo, or bold graphic shapes.)

#### Steps

1. **Set the platform**: Turn **Palette** (Knob 5) fully counterclockwise to select the ZX Spectrum palette (position 0).
2. **Set authentic cell size**: Set **Cell Size** (Knob 1) to position 1 (8-pixel cells) and toggle **Cell Shape** (Switch 8) to **Square** for authentic 8×8 cells.
3. **Black background**: Enable **Black Paper** (Switch 9). The paper layer snaps to black.
4. **Go bright**: Toggle **Bright** (Switch 7) to **Bright**. Colors jump from muted to vivid (classic Spectrum loading screen intensity.)
5. **Tune the ink**: Sweep **Ink Bias** (Knob 2) slowly. Watch how the ink color cycles through the Spectrum colors: blue, red, magenta, green, cyan, yellow, white: as the bias walks through the palette.
6. **Adjust the threshold**: Center **Threshold** (Knob 4) and then nudge it to control how much ink vs. paper appears in each cell.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | 1 (8px) |
| Ink Bias | 75% |
| Paper Bias | 0% |
| Threshold | 50% |
| Palette | 0 (ZX Spectrum) |
| Color Bleed | 0% |
| Bright | Bright |
| Cell Shape | Square |
| Black Paper | On |
| Flash | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Composite Video Nostalgia

![Composite Video Nostalgia result](/img/instruments/videomancer/gazette/gazette_ex2_s1.png)
*Composite Video Nostalgia — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Simulate what a Commodore 64 game looked like on a consumer television connected via composite cable (smeared colors, chunky cells, and warm earth tones.)

#### Key Concepts

- Color Bleed simulates composite video chroma smearing
- Different palettes evoke different hardware platforms
- Cell Shape affects how attribute clash manifests vertically

#### Video Source

Footage with colorful, high-contrast content (animation, bold graphics, or colorful objects.)

#### Steps

1. **Select the C64 palette**: Turn **Palette** (Knob 5) to position 2 for the Commodore 64 color set.
2. **Set large cells**: Turn **Cell Size** (Knob 1) to position 2 (16-pixel cells) and set **Cell Shape** to **Square** for chunky 16×16 blocks.
3. **Add color bleed**: Turn **Color Bleed** (Knob 6) to about 70%. The palette colors begin to smear horizontally, producing rainbow trails.
4. **Warm up the paper**: Increase **Paper Bias** (Knob 3) to about 50% to select a warm mid-tone as the paper color.
5. **Partial mix**: Lower **Mix** (Fader 12) to about 60%. The palette-restricted image blends with the clean source, producing a ghostly overlay effect.
6. **Compare palettes**: Cycle through the four palettes with Knob 5. Notice how each platform's color personality transforms the mood of the image.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | 2 (16px) |
| Ink Bias | 75% |
| Paper Bias | 50% |
| Threshold | 50% |
| Palette | 2 (C64) |
| Color Bleed | 70% |
| Bright | Normal |
| Cell Shape | Square |
| Black Paper | Off |
| Flash | Off |
| Bypass | Off |
| Mix | 60% |

---

### Exercise 3: Blinking Bulletin Board

![Blinking Bulletin Board result](/img/instruments/videomancer/gazette/gazette_ex3_s1.png)
*Blinking Bulletin Board — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Produce an animated display reminiscent of a BBS (bulletin board system) terminal with blinking text attributes and fine character cells.

#### Key Concepts

- Flash creates rhythmic ink/paper color swaps
- Small cells and row mode create a text-like line structure
- Ink Bias and Paper Bias together define the color scheme

#### Video Source

Any moving video. Scrolling text, a slow camera pan, or a talking head all work well (motion makes the flash effect more dynamic.)

#### Steps

1. **Tiny cells in row mode**: Set **Cell Size** (Knob 1) to position 0 (4-pixel cells) and **Cell Shape** (Switch 8) to **8×1 Row**. This creates a fine horizontal texture (every scan line has independent color assignments.)
2. **Choose CGA**: Set **Palette** (Knob 5) to position 1 for the CGA palette, with its distinctive browns and grays.
3. **Enable Flash**: Toggle **Flash** (Switch 10) to **On**. The image begins pulsing as ink and paper swap every half second.
4. **Set contrasting ink and paper**: Push **Ink Bias** (Knob 2) high (~80%) and **Paper Bias** (Knob 3) low (~20%). This creates a strong two-tone contrast that makes the flash swap dramatic.
5. **Add a touch of bleed**: Set **Color Bleed** (Knob 6) to about 30%. The colors smear subtly, softening the cell boundaries.
6. **Lower the threshold**: Pull **Threshold** (Knob 4) below center (~35%) so more of the image renders as ink, creating denser "text" coverage.
7. **Observe the flash rhythm**: Watch how the periodic swap creates a systematic pulsing. Cells that were mostly ink become mostly paper, and vice versa.

#### Settings

| Control | Value |
|---------|-------|
| Cell Size | 0 (4px) |
| Ink Bias | 80% |
| Paper Bias | 20% |
| Threshold | 35% |
| Palette | 1 (CGA) |
| Color Bleed | 30% |
| Bright | Normal |
| Cell Shape | 8×1 Row |
| Black Paper | Off |
| Flash | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Attribute Clash**: The visual artifact produced when adjacent character cells display different ink/paper color pairs, creating harsh color boundaries at cell edges.

- **BRAM**: Block RAM; dedicated memory blocks inside the FPGA used here to store per-column luminance samples for the cell color assignment.

- **Character Cell**: A rectangular region of pixels that shares a single pair of colors (ink and paper), inherited from the memory-saving display architecture of 1980s home computers.

- **Composite Video**: An analog video signal format that combines luminance and chrominance into a single wire, causing imperfect separation and characteristic color smearing artifacts.

- **Elaboration Time**: The moment when the FPGA design is compiled by synthesis tools, before it runs on hardware; constant computations like palette color conversion happen here.

- **IIR Filter**: Infinite Impulse Response filter; a feedback-based filter where the output depends on both the current input and the filter's own previous output, producing exponential decay trails.

- **Ink**: The foreground color assigned to bright pixels within each character cell, selected from the active palette based on cell luminance.

- **Palette**: A fixed set of colors available to the display hardware; Gazette offers four historically accurate palettes with 16 entries each.

- **Paper**: The background color assigned to dark pixels within each character cell, selected uniformly across the screen via the Paper Bias control.

- **YUV**: A color encoding that separates brightness (Y) from color (U and V), used internally by Videomancer's video processing pipeline.

---
