---
draft: true
sidebar_position: 11
slug: /instruments/videomancer/attrcycle
title: "Attrcycle"
image: /img/instruments/videomancer/attrcycle/attrcycle_hero.png
description: "Attr Cycle recreates the ZX Spectrum's distinctive attribute colour system, where the screen is divided into character-sized cells and each cell holds a foreground (ink) and background (paper) colour from a limited 8-colour palette."
---

import attrcycle_hero from '/img/instruments/videomancer/attrcycle/attrcycle_hero.png';
import attrcycle_animation from '/img/instruments/videomancer/attrcycle/attrcycle_animation.gif';
import attrcycle_control_panel from '/img/instruments/videomancer/attrcycle/attrcycle_control_panel.png';
import attrcycle_exercise1_result from '/img/instruments/videomancer/attrcycle/attrcycle_exercise1_result.gif';
import attrcycle_exercise2_result from '/img/instruments/videomancer/attrcycle/attrcycle_exercise2_result.gif';
import attrcycle_exercise3_result from '/img/instruments/videomancer/attrcycle/attrcycle_exercise3_result.gif';

# Attrcycle

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={attrcycle_hero} alt="Attrcycle hero image"/>
*A photographic image shattered into coarse 8-bit colour blocks where bright regions reveal cycling ZX Spectrum ink colours and shadows show paper — a living attribute clash.*
<img src={attrcycle_animation} alt="Attrcycle animated output"/>
*Attrcycle output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Attr Cycle recreates the ZX Spectrum's distinctive attribute colour system, where the screen is divided into character-sized cells and each cell holds a foreground (ink) and background (paper) colour from a limited 8-colour palette. The input video's luminance drives the ink/paper selection: pixels brighter than the Density threshold take the cell's ink colour, while darker pixels receive the paper colour. The result is a continuously cycling, coarsely quantised colour map that reinterprets any video source through the lens of 1982 home computing.

The name comes from the Spectrum's "attribute" memory — a separate byte per 8×8 cell that sets ink, paper, brightness, and flash. Classic demos like "Shock Megademo" exploited rapid attribute cycling to create rainbow scrollers and colour animation effects impossible in the bitmap layer alone.

Block sizes are configurable from 8×8 up to 64×64 pixels, covering the range from authentic Spectrum resolution down to extreme mosaic scales. A per-frame phase accumulator sweeps ink and paper assignments through the palette, and an optional FLASH toggle emulates the Spectrum's periodic ink/paper swap.

---

## Quick Start

1. **8×8 blocks with Grid Lines** produces the most authentic Spectrum screenshot look, especially with a pixelated or low-resolution source.
2. **Speed at zero with Palette Offset** allows manual colour theme selection — sweep the offset to find pleasing ink/paper combinations.
3. **Density is the content control** — it determines how much of the source's tonal structure is preserved in the ink/paper separation.

---

## Background

### The ZX Spectrum Colour Model

The Spectrum's display was 256×192 pixels with 1-bit depth per pixel, but colour came from a 32×24 attribute grid. Each attribute byte encoded 3 bits of ink colour, 3 bits of paper colour, a brightness bit, and a flash bit. Only 8 colours were available (with bright variants doubling the palette to 15 plus black). This architecture meant two different-coloured objects sharing the same 8×8 cell would "clash" — one would take the other's attributes, hence the infamous "attribute clash".

### Palette Cycling as Animation

Because the attribute layer was tiny (768 bytes), it could be reprogrammed far faster than the bitmap. Demo coders exploited this by cycling palette indices through the attribute grid each frame, creating cascading rainbow effects across the screen. "Attribute cycling" became a signature Spectrum demo effect, producing smooth colour animation without touching the bitmap.

### Ink, Paper, and Flash

In Spectrum terminology, "ink" is the foreground colour drawn where the bitmap is set (1), and "paper" is the background where it's clear (0). The FLASH bit automatically swaps ink and paper at a fixed interval, creating blinking text and borders. Attr Cycle extends this to a video threshold rather than a bitmap, using input luminance as the 1/0 selector.

### Block Coordinate Hashing

The program uses XOR or row-only hashing of block coordinates to determine palette index. The checker pattern (col XOR row) produces a tessellated colour arrangement like a quilt, while the stripe pattern (row only) creates horizontal colour bands resembling loading screen borders.


---

## Signal Flow

```
registers_in ──→ [Register Map] ──→ speed, block size, palette offset,
                                    saturation, density, brightness
                                    toggles: palette, pattern, flash, grid, bypass

                ┌──────────────────────────────────────┐
                │        VBLANK ANIMATION              │
                │  phase += speed                      │
                │  flash_ctr++; toggle every 16 frames │
                └──────────────────────────────────────┘

data_in ──→ [Stage 1: Block Coords]
              h_count >> blk_shift → block_col
              v_count >> blk_shift → block_row
              sub-pixel mask → grid line detect
                        │
                        ▼
            [Stage 2: Palette Index]
              hash = col XOR row (checker) or row (stripe)
              ink_idx = hash + phase + offset
              paper_idx = ink_idx + 4
              flash swap if active
                        │
                        ▼
            [Stage 3: Colour Lookup]
              ink  = spectrum_palette[ink_idx]
              paper = spectrum_palette[paper_idx]
              saturation scaling of U,V
                        │
                        ▼
            [Stage 4: Luma Threshold]
              data_in.y > density? → ink else paper
                        │
                        ▼
            [Stage 5: Grid + Brightness]
              grid line overlay (dark borders)
              brightness scaling
                        │
                        ▼
            [interpolator_u × 3]
              wet/dry crossfade
                        │
                        ▼
                   data_out
```

The pipeline transforms continuous video into a coarse colour grid in five stages. Block coordinates are computed in the first clock by shifting pixel coordinates right by the block size exponent. The palette index is derived from a hash of these coordinates combined with the animation phase, meaning the same block position traces a repeating path through the eight Spectrum colours over time. The luminance threshold in stage 4 is critical: it uses the raw input video brightness to decide whether each pixel shows as ink or paper, preserving contour information from the source even as colours are replaced.

---

## Parameter Reference

<img src={attrcycle_control_panel} alt="Videomancer front panel with Attrcycle loaded"/>
*Videomancer's front panel with Attrcycle active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Speed controls how fast the colour palette cycles per frame. At zero the colours are static. As speed increases, ink and paper assignments sweep through the eight-colour palette creating a rainbow cascade effect. High speeds produce a rapid strobe that blends neighbouring colours perceptually. The speed is added to a 20-bit phase accumulator, with the top 3 bits selecting the palette index, so colours change smoothly and continuously.

---

#### Knob 2 — Block Size
| Property | Value |
|----------|-------|
| Range | 1x – 8x |
| Default | 4x |
| Suffix | x |

Block Size sets the attribute cell dimensions in four discrete steps: 8×8, 16×16, 32×32, or 64×64 pixels. At 8×8 the result closely matches original Spectrum resolution, with fine detail preserved in the ink/paper boundary. At 64×64 the image becomes an extreme mosaic where each block spans a large area, emphasising coarse shapes and eliminating fine texture.

---

#### Knob 3 — Palette Offset
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Palette Offset shifts the starting point of the cycling palette. This effectively rotates which of the eight colours appears first in the sequence, allowing the user to lock in a preferred colour combination. When Speed is zero, Palette Offset selects the static colour scheme directly. When cycling, it shifts the entire phase of the animation.

---

#### Knob 4 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Saturation scales the chroma components of the palette colours. At zero, all colours collapse to their luminance-only equivalents (shades of grey). At maximum, the full ZX Spectrum colour palette is expressed. Mid-range values produce desaturated pastels. The scaling is applied as a signed multiplication around the 512 chroma midpoint.

---

#### Knob 5 — Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 62.6% |
| Suffix | % |

Density sets the luminance threshold that determines which pixels display as ink versus paper. At minimum, nearly everything is ink (foreground colour). At maximum, nearly everything is paper (background colour). At the midpoint, the boundary follows the 50% grey level of the input, producing the most balanced and detailed ink/paper separation. This control is the primary way video content structure is preserved.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Brightness scales the output luminance from black to full intensity. At zero the output is dark regardless of palette. At maximum, white blocks reach near-peak level. Brightness is applied as a multiplication after palette lookup and ink/paper selection, affecting both colours equally.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Spectrum | Mono |
| **8 — Pattern** | Checker | Stripe |
| **9 — Flash** | Off | On |
| **10 — Grid Lines** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control palette variant, block pattern, flash emulation, grid visibility, and bypass. Palette selects between four colour palettes — only the Spectrum palette is detailed in the VHDL, with the others as variants. Pattern changes how block coordinates map to palette indices. Flash emulates the Spectrum's periodic ink/paper swap. Grid Lines overlay dark borders at block boundaries for a retro grid aesthetic.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the dry (unprocessed) input and the wet (attribute-coloured) output. At 0% the output is the original video. At 100% the full block-colour effect is visible. Intermediate positions blend smoothly, overlaying the attribute grid semi-transparently over the source.





---

## Guided Exercises

These exercises demonstrate the classic Spectrum attribute aesthetic, from faithful 8×8 recreation to extreme mosaic abstraction with colour cycling.

### Exercise 1: Authentic Spectrum Attribute Clash

<img src={attrcycle_exercise1_result} alt="Authentic Spectrum Attribute Clash result"/>
*Authentic Spectrum Attribute Clash — simulated result across source images.*
**What You'll Create**: Recreate the authentic ZX Spectrum attribute clash look with 8×8 blocks and static colours.

1. Set Block Size to step 1 (8×8 — smallest blocks).
2. Set Speed to 0 (no cycling) and Palette Offset to 50%.
3. Set Density to 50% to split foreground and background evenly.
4. Saturation to 80%, Brightness to 70%.
5. Pattern=Checker, Flash=Off, Grid Lines=Off.
6. Observe how facial features are preserved in the ink/paper separation.
7. Sweep Density to see how the threshold shifts the boundary.

**Key concepts**: - 8×8 blocks match the original Spectrum resolution
- Density threshold converts continuous luminance to binary ink/paper
- Static palette offset selects the initial colour pairing

---

### Exercise 2: Rainbow Cascade with Grid

<img src={attrcycle_exercise2_result} alt="Rainbow Cascade with Grid result"/>
*Rainbow Cascade with Grid — simulated result across source images.*
**What You'll Create**: Create a rainbow cycling effect with visible grid lines, similar to Spectrum demo loading screens.

1. Set Block Size to step 2 (16×16) for visible mosaic.
2. Set Speed to 75% for smooth cycling.
3. Saturation to maximum (100%), Brightness to 80%.
4. Enable Grid Lines for the retro mosaic look.
5. Pattern=Stripe for horizontal colour bands.
6. Observe the cascading rainbow effect as colours cycle through rows.

**Key concepts**: - Stripe pattern creates horizontal colour bands mimicking loading screens
- Grid lines add structure and retro authenticity
- Speed controls the cascade rate through the 8-colour palette

---

### Exercise 3: Flash and Mosaic Abstraction

<img src={attrcycle_exercise3_result} alt="Flash and Mosaic Abstraction result"/>
*Flash and Mosaic Abstraction — simulated result across source images.*
**What You'll Create**: Create an abstract blinking mosaic using large blocks, fast cycling, and flash.

1. Set Block Size to step 4 (64×64) for extreme mosaic.
2. Set Speed to 50% for moderate cycling.
3. Enable Flash for periodic ink/paper swap.
4. Set Density to 60% to favour ink colours.
5. Saturation to 60%, Brightness to 90%.
6. Pattern=Checker for maximum spatial variation.
7. Observe how the flash creates a blinking, breathing pattern.

**Key concepts**: - Large blocks create extreme abstraction where only broad shapes remain
- Flash adds rhythmic blinking that echoes the Spectrum's cursor effect
- Checker pattern maximises colour variation between adjacent blocks

---


## Tips

- **Checker vs Stripe** produces dramatically different spatial feel: checker creates quilt-like tessellation, stripe creates horizontal bands.
- **Flash at slow speed** creates a hypnotic breathing effect where the entire screen periodically shifts between complementary colour schemes.
- **Large blocks with high saturation** turn any video into an abstract colour field painting, retaining only the coarsest compositional structure.

---
