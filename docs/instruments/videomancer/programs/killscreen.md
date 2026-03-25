---
draft: true
sidebar_position: 159
slug: /instruments/videomancer/killscreen
title: "Killscreen"
image: /img/instruments/videomancer/killscreen/killscreen_hero.png
description: "On September 21, 1982, Billy Mitchell became the first person to reach screen 256 of Pac-Man — and discovered that the game's level counter overflowed its 8-bit storage."
---

![Killscreen hero image](/img/instruments/videomancer/killscreen/killscreen_hero_s1.png)
*Arcade corruption creeping across a tiled video grid as six glitch modes scramble color, brightness, and position one tile at a time.*

---

## Overview

**Killscreen** breaks your video into a grid of tiles and unleashes a wave of digital corruption that sweeps from one side of the screen to the other. The result is a split-screen effect straight out of golden-age arcade hardware: one half of the image remains recognizable while the other dissolves into a patchwork of scrambled tiles, wrong colors, inverted brightness, and solid-fill blanks.

Six corruption modes attack each tile differently. Some tiles display shifted pixel data borrowed from their neighbors. Others have their color channels shuffled or inverted. Still others have their brightness data bit-shifted into smeared streaks, or are replaced entirely with a colored fill. Which mode strikes which tile is determined by a ***linear feedback shift register*** (LFSR) hash seeded by the tile's screen position, producing a deterministic but unpredictable pattern of visual chaos that evolves over time.

The corruption zone's extent, the rate at which the pattern evolves, and the direction of the corruption wave are all adjustable. Grid line overlays reveal the tile boundaries, and a wet/dry **Mix** fader lets you blend the corrupted image with the clean original.

:::tip
Killscreen is at its most magical when the **Corrupt Amt** knob is set to a middle value, creating a clear split between a clean half and a corrupted half (just like the original Pac-Man kill screen.)
:::

### What's In a Name?

A ***kill screen*** is the moment an arcade game hits a hardware limitation or software bug that renders it unplayable. The most famous kill screen in gaming history occurs at level 256 of ***Pac-Man***. Namco's 8-bit level counter overflows from 255 to 0, triggering a ***buffer overrun*** in the fruit display routine that corrupts the right half of the screen with scrambled tile data, garbage palette assignments, and misread character ROM graphics. The left half remains eerily functional: you can still play, if you know where the dots are. This program recreates that aesthetic in real time, turning any video source into a canvas of tile-level glitch art.

---

## Quick Start

1. Feed a video signal into Videomancer and turn **Corrupt Amt** (Knob 1) clockwise to about 50%. The right half of the screen fractures into a mosaic of corrupted tiles while the left half stays clean.
2. Slowly turn **Speed** (Knob 2) clockwise. The corruption pattern churns and shifts as the internal pseudorandom generator evolves faster between frames.
3. Flip **Grid Lines** (Switch 10) to **On**. Thin neutral-colored lines appear at tile boundaries, revealing the grid that organizes the corruption.
4. Adjust **Mix** (Fader 12) to blend the corrupted image with the clean original. At the center position, you see a ghostly overlay of both worlds.

---

## Parameters

![Videomancer front panel with Killscreen loaded](/img/instruments/videomancer/killscreen/killscreen_control_panel.png)
*Videomancer's front panel with Killscreen active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Corrupt Amt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Corrupt Amt** controls how far the corruption zone extends across the screen. At 0%, fully counterclockwise, the entire image passes through uncorrupted. As you turn the knob clockwise, corruption creeps inward from the right edge (or left edge, depending on the **Direction** toggle). At 100%, every tile on the screen is subject to corruption. A value around 50% produces the classic split-screen look (a clean half and a corrupted half side by side.)

The corruption threshold is compared against each tile's horizontal position. Tiles beyond the threshold enter the corruption zone, where the LFSR hash determines which of six corruption modes is applied.

---

### Knob 2 — Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Speed** controls how rapidly the master LFSR evolves between video frames. At 0%, the LFSR barely advances: the corruption pattern is nearly frozen, producing a static glitch tableau. As the value increases, the LFSR steps through its sequence more quickly, causing the corruption pattern to churn and shift from frame to frame. At 100%, the pattern changes rapidly, creating a jittering, restless field of visual noise.

:::note
Speed affects only *which* corruption mode appears in each tile, not the visual character of the modes themselves. A frozen pattern at low Speed can be just as visually complex as a fast one (it simply holds still.)
:::

---

### Knob 3 — Offset Range

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Offset Range** is labeled for controlling the displacement range of tile address corruption. This parameter is mapped to the hardware but is reserved for a future firmware update. Turning the knob has no visible effect in the current version.

---

### Knob 4 — Color Intns

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Color Intns** is labeled for controlling the severity of palette corruption effects. This parameter is mapped to the hardware but is reserved for a future firmware update. Turning the knob has no visible effect in the current version.

---

### Knob 5 — Border Brt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Border Brt** sets the brightness of the tile grid lines when **Grid Lines** (Switch 10) is enabled. At 0%, fully counterclockwise, tile borders are dark: they appear as dim seams between tiles. As the value increases, the grid lines become brighter and more prominent. At 100%, the borders are bright white lines overlaid on the image.

Grid lines are drawn at tile boundaries by halving the corrupted pixel's brightness and adding half the Border Brt value. Chroma is set to neutral on border pixels, so grid lines always appear as grayscale regardless of the underlying tile content.

:::tip
Even subtle grid lines can dramatically change the feel of the image. Low **Border Brt** values create an understated tiled-mosaic look, while high values evoke a wireframe overlay on top of the glitch art.
:::

---

### Knob 6 — Fill Color

| Property | Value |
|----------|-------|
| Range | 0.0d – 360.0d |
| Default | 0.0d |

**Fill Color** selects the hue used by the solid-fill corruption mode (Mode 5). This control sweeps through a range of colors by offsetting the U and V chroma channels away from neutral. At 0 degrees, the fill is a dim, nearly achromatic tone. As you rotate the knob, the fill shifts through warm and cool hues. The brightness of the fill tile is derived from half the Fill Color value.

Fill Color only affects tiles that happen to land on Mode 5 during the LFSR hash: not every corrupted tile will show this color. With **Mode Bias** set to **Pac-Man**, Mode 5 tiles appear less frequently.

---

### Switch 7 — Tile Size

| Property | Value |
|----------|-------|
| Off | 8x8 |
| On | 32x32 |
| Default | 8x8 |

**Tile Size** is labeled for selecting between an 8×8 pixel tile grid and a 32×32 pixel tile grid. This toggle is mapped to the hardware but its effect on the internal tile coordinate calculation is reserved for a future firmware update. The visible tile grid size remains constant regardless of this switch position.

---

### Switch 8 — Mode Bias

| Property | Value |
|----------|-------|
| Off | All Equal |
| On | Pac-Man |
| Default | All Equal |

**Mode Bias** shifts the statistical distribution of corruption modes. With the switch set to **All Equal**, all six corruption modes have roughly equal probability of appearing in any given corrupted tile. With the switch set to **Pac-Man**, the address-offset mode (Mode 1) is heavily favored, appearing in roughly half of all corrupted tiles. This recreates the Pac-Man kill screen's signature look, where most of the corruption manifests as displaced tile data rather than palette swaps or solid fills.

:::tip
Try freezing the corruption with **Speed** at 0% and toggling **Mode Bias** back and forth. You can clearly see Mode 1 tiles replace other corruption types as the bias shifts.
:::

---

### Switch 9 — Direction

| Property | Value |
|----------|-------|
| Off | L-to-R |
| On | R-to-L |
| Default | L-to-R |

**Direction** controls which side of the screen corruption originates from. With the switch set to **L-to-R**, corruption creeps in from the right edge as **Corrupt Amt** increases: matching the original Pac-Man kill screen, where the left half stays functional. With the switch set to **R-to-L**, the corruption sweeps in from the left edge instead.

---

### Switch 10 — Grid Lines

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Grid Lines** enables a visible tile boundary overlay. With the switch set to **Off**, tiles blend seamlessly at their edges. With the switch set to **On**, thin neutral lines are drawn at tile boundaries, revealing the grid structure. The brightness of these lines is controlled by **Border Brt** (Knob 5).

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the original input signal directly to the output, bypassing all corruption processing. The internal sync delay pipeline still aligns timing, so there is no glitch or timing disruption when toggling Bypass. Use this for instant A/B comparison between the raw input and the corrupted result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original (dry) input video and the corrupted (wet) output. At 0%, fully down, only the clean input is visible. At 100%, fully up, only the corrupted output is visible. Intermediate values produce a blended overlay where the corruption appears as a ghostly layer on top of the clean image.

The crossfade is a per-pixel linear interpolation across all three YUV channels, implemented by three parallel interpolator stages.

---

## Background

### Arcade tile graphics

The golden age of arcade games (roughly 1978–1985) was defined by ***tile-based graphics***. Hardware such as the Namco Galaxian/Pac-Man platform and the Nintendo VS. System rendered screens by assembling small, fixed-size bitmap tiles: typically 8×8 pixels: from a read-only character ROM. A ***tile map***, which is a grid of index numbers stored in video RAM, told the hardware which tile image to draw at each grid position. A separate ***palette RAM*** held color lookup tables, and a ***sprite engine*** overlaid player and enemy graphics on top of the tiled background.

This architecture was efficient and elegant, but it was also brittle. Buffer overflows, counter rollovers, and address line corruption could redirect tile lookups to wrong ROM addresses, apply wrong palettes, flip tile orientations, or smear data across tile boundaries. The visual results were strikingly abstract: identifiable game art fractured into wrong arrangements, with fragments of recognizable characters appearing in impossible combinations.

### The Pac-Man level 256 kill screen

The most famous instance of tile corruption is the Pac-Man level 256 kill screen. Pac-Man stores its level counter as an unsigned 8-bit integer, which holds values from 0 to 255. When a player clears level 255, the counter increments to 256: but an 8-bit register can only hold values up to 255, so it overflows to 0. The fruit display subroutine uses this counter to determine how many fruit icons to render at the bottom of the screen. It attempts to draw 256 fruits, but the 8-bit loop counter wraps around, causing the routine to overwrite tile map RAM far beyond its allocated region. The result is a cascade of wrong tile indices, misread palette assignments, and visual chaos that renders the right half of the screen as abstract garbage: while the left half, untouched by the overflow, remains fully playable.

Killscreen recreates this aesthetic electronically: a position-dependent corruption wave that produces deterministic but visually unpredictable tile-level corruption of the incoming video signal.

### Linear feedback shift registers

A ***linear feedback shift register*** (LFSR) is a shift register whose input bit is computed from a linear function: typically XOR: of selected register bits called ***taps***. LFSRs cycle through a sequence of states that appears random but is entirely deterministic and periodic. With properly chosen taps, a 16-bit LFSR cycles through all 65,535 nonzero states before repeating.

Killscreen uses a single 16-bit Galois LFSR with taps at positions 16, 14, 13, and 11 as a master pseudorandom source. Rather than maintaining independent per-tile state (which would require a full frame buffer), the master LFSR value is XOR-combined with each tile's screen coordinates to produce a unique ***position-seeded hash*** per tile per frame. This is the key architectural trick: it gives every tile a distinct corruption state without storing any per-tile data, using only a handful of combinational logic gates.


---

## Signal Flow

### Signal Flow Notes

The master LFSR advances once per vertical sync pulse, and its evolution rate is governed by the **Speed** control. A speed counter increments at each vsync; only when the counter exceeds the speed threshold (derived from the upper 8 bits of the Speed pot) does the LFSR actually shift to a new state. At low Speed settings, the corruption pattern holds steady for many frames before changing (this is how you get a frozen glitch tableau.)

The corruption threshold comparison is the heart of the split-screen effect. Each tile's horizontal coordinate is compared against a threshold derived from **Corrupt Amt**. In L-to-R mode, tiles whose x-position exceeds `(255 - threshold)` are corrupted: so increasing Corrupt Amt lowers the ceiling and corrupts more columns from the right. In R-to-L mode, tiles whose x-position is below the threshold are corrupted, sweeping from the left instead.

:::note
Mode 0 (clean passthrough) is one of eight possible hash outcomes even within the corruption zone. This means roughly one in eight tiles will survive uncorrupted: exactly as on the original Pac-Man kill screen, where recognizable tile fragments peek through the chaos.
:::


---

## Exercises

These exercises explore Killscreen's corruption engine from basic split-screen effects to animated glitch art. Each builds on the previous, engaging more controls as you go.
### Exercise 1: The Classic Split Screen

![The Classic Split Screen result](/img/instruments/videomancer/killscreen/killscreen_ex1_s1.png)
*The Classic Split Screen — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Recreate the iconic Pac-Man level 256 split-screen: one half clean, one half corrupted, with visible tile grid lines.

#### Key Concepts

- The corruption zone sweeps across the screen based on tile position
- Mode Bias changes which corruption types dominate
- Grid lines reveal the tile structure underneath the chaos

#### Video Source

A live camera feed or recorded footage with recognizable subjects: faces, text, or geometric patterns work well because the contrast between clean and corrupted halves is most striking.

#### Steps

1. **Set the split**: Turn **Corrupt Amt** (Knob 1) to about 50%. The right half of the image fills with corrupted tiles.
2. **Freeze the pattern**: Turn **Speed** (Knob 2) fully counterclockwise. The corruption pattern holds still, producing a frozen glitch tableau you can study.
3. **Reveal the grid**: Flip **Grid Lines** (Switch 10) to **On** and turn **Border Brt** (Knob 5) to about 40%. Thin lines reveal the tile boundaries.
4. **Pac-Man bias**: Flip **Mode Bias** (Switch 8) to **Pac-Man**. Notice how the corruption becomes dominated by displaced tile data, with fewer color swaps and fills.
5. **Compare**: Toggle **Bypass** (Switch 11) to see the clean original, then toggle back.

#### Settings

| Control | Value |
|---------|-------|
| Corrupt Amt | 50.0% |
| Speed | 0.0% |
| Offset Range | 50.0% |
| Color Intns | 50.0% |
| Border Brt | 40.0% |
| Fill Color | 0.0d |
| Tile Size | 8x8 |
| Mode Bias | Pac-Man |
| Direction | L-to-R |
| Grid Lines | On |
| Bypass | Off |
| Mix | 100.0% |

---

### Exercise 2: Animated Corruption Wave

![Animated Corruption Wave result](/img/instruments/videomancer/killscreen/killscreen_ex2_s1.png)
*Animated Corruption Wave — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated corruption pattern that shifts and churns across the screen, with a sweeping corruption wave you can push back and forth.

#### Key Concepts

- Speed controls how rapidly the LFSR evolves the corruption pattern
- Direction reverses which side of the screen the corruption wave originates from
- Fill Color tints solid-fill tiles with a chosen hue

#### Video Source

Footage with slow movement or a static scene: the motion of the corruption pattern itself becomes the primary visual subject.

#### Steps

1. **Set moderate corruption**: Turn **Corrupt Amt** (Knob 1) to about 60%.
2. **Speed up the LFSR**: Turn **Speed** (Knob 2) to about 50%. The corruption pattern begins to change from frame to frame, producing a jittering, animated glitch texture.
3. **Add fill color**: Turn **Fill Color** (Knob 6) to about 120 degrees. Any tile that lands on Mode 5 fills with a colored tint.
4. **Reverse direction**: Flip **Direction** (Switch 9) to **R-to-L**. The corruption wave now sweeps in from the left.
5. **Sweep the threshold**: Slowly turn **Corrupt Amt** from 0% to 100% and back. Watch the corruption wave advance and retreat across the screen in real time.

#### Settings

| Control | Value |
|---------|-------|
| Corrupt Amt | 60.0% |
| Speed | 50.0% |
| Offset Range | 50.0% |
| Color Intns | 50.0% |
| Border Brt | 0.0% |
| Fill Color | 120.0d |
| Tile Size | 8x8 |
| Mode Bias | All Equal |
| Direction | R-to-L |
| Grid Lines | Off |
| Bypass | Off |
| Mix | 100.0% |

---

### Exercise 3: Glitch Art Composition

![Glitch Art Composition result](/img/instruments/videomancer/killscreen/killscreen_ex3_s1.png)
*Glitch Art Composition — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A composited glitch artwork blending corruption effects with the clean source through the Mix fader, framed by visible tile grid lines (a piece you could photograph or capture as a still.)

#### Key Concepts

- The Mix fader creates ghostly overlay blends of corrupted and clean imagery
- Grid lines and border brightness add graphic structure to the composition
- Freezing Speed produces a static glitch composition you can study and frame

#### Video Source

High-contrast footage or bold graphic patterns: shapes with strong edges and saturated colors show the variety of corruption modes most clearly.

#### Steps

1. **Full corruption**: Turn **Corrupt Amt** (Knob 1) to 100%. The entire screen is corrupted.
2. **Moderate speed**: Set **Speed** (Knob 2) to about 25% for a slowly evolving pattern.
3. **Partial mix**: Pull **Mix** (Fader 12) to about 60%. The corruption appears as a translucent overlay on the clean source (a ghostly double image.)
4. **Strong grid**: Flip **Grid Lines** (Switch 10) to **On** and turn **Border Brt** (Knob 5) to about 70%. The grid becomes a prominent graphic element.
5. **Choose a fill hue**: Turn **Fill Color** (Knob 6) to about 200 degrees for cool-toned fill tiles.
6. **All-equal modes**: Set **Mode Bias** (Switch 8) to **All Equal** for maximum variety in corruption types across the grid.
7. **Freeze and study**: Turn **Speed** fully counterclockwise to freeze the composition. Examine the different corruption modes visible across the tiles.

#### Settings

| Control | Value |
|---------|-------|
| Corrupt Amt | 100.0% |
| Speed | 25.0% |
| Offset Range | 50.0% |
| Color Intns | 50.0% |
| Border Brt | 70.0% |
| Fill Color | 200.0d |
| Tile Size | 32x32 |
| Mode Bias | All Equal |
| Direction | L-to-R |
| Grid Lines | On |
| Bypass | Off |
| Mix | 60.0% |

---
## Glossary

- **Buffer Overflow**: A condition where a program writes data past the end of an allocated memory region, corrupting adjacent data (the root cause of the Pac-Man kill screen.)

- **Galois LFSR**: A variant of linear feedback shift register where XOR taps are applied during each shift operation, producing a pseudorandom sequence with maximal period.

- **Hash**: A function that maps an input (here, tile coordinates combined with an LFSR state) to a fixed-size output in a way that appears random but is entirely deterministic.

- **Kill Screen**: The point in an arcade game where a hardware or software limitation renders the game unplayable, often producing abstract visual corruption as a side effect.

- **LFSR**: Linear Feedback Shift Register: a shift register whose input bit is derived from XOR of selected tap positions, producing a repeating pseudorandom bit sequence.

- **Palette**: A lookup table mapping index values to display colors; in tile-based arcade graphics, each tile references a palette entry for its color scheme.

- **Tile**: A small, fixed-size rectangular block of pixels used as the fundamental drawing unit in tile-based video game graphics hardware.

- **Tile Map**: A grid of index values stored in video RAM that tells the graphics hardware which tile image to display at each position on screen.

---
