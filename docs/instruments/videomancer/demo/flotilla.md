---
draft: true
sidebar_position: 102
slug: /instruments/videomancer/flotilla
title: "Flotilla"
image: /img/instruments/videomancer/flotilla/flotilla_hero.png
description: "Program guide for Flotilla, a Videomancer demo program for the LZX video synthesizer."
---

import flotilla_hero from '/img/instruments/videomancer/flotilla/flotilla_hero.png';
import flotilla_animation from '/img/instruments/videomancer/flotilla/flotilla_animation.gif';
import flotilla_control_panel from '/img/instruments/videomancer/flotilla/flotilla_control_panel.png';
import flotilla_exercise1_result from '/img/instruments/videomancer/flotilla/flotilla_exercise1_result.gif';
import flotilla_exercise2_result from '/img/instruments/videomancer/flotilla/flotilla_exercise2_result.gif';
import flotilla_exercise3_result from '/img/instruments/videomancer/flotilla/flotilla_exercise3_result.gif';

# Flotilla

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={flotilla_hero} alt="Flotilla hero image"/>
*Eight arrow sprites in tight formation across a black void â€” staggered vertically in a wave pattern, each one a bright pixel cluster marching rightward in lock-step, trailing nothing but geometry.*
<img src={flotilla_animation} alt="Flotilla animated output"/>
*Flotilla output evolving over multiple frames â€” synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In the early days of home computing, sprites were not abstract concepts â€” they were hardware resources, tiny bitmaps that the display controller could place at arbitrary screen positions without the CPU redrawing the background. A typical system offered between four and eight of them, each a few pixels square, each independently positioned, each composited over the playfield by dedicated silicon. Flotilla recreates this paradigm in FPGA logic: eight independent 8Ã—8 bitmap sprites, positioned by direct digital synthesis accumulators, arranged in configurable wave formations, and composited over either a black field or a video passthrough â€” all in approximately 1300 LUTs and zero BRAM.

The sprites move along a single axis (horizontal or vertical) at a rate controlled by the Speed knob, with per-sprite phase offsets that spread them into a formation. The Wave Amp knob controls how far the formation spreads perpendicular to the direction of travel, and Wave Freq modulates that spread sinusoidally over time, creating the rippling motion that gives the program its name. Two selectable shapes â€” arrow and diamond â€” are stored as 64-bit constants, requiring no block RAM. Magnification from 1Ã— to 4Ã— doubles pixel size at each step, scaling the tiny 8Ã—8 glyphs up to 64Ã—64 screen pixels. A priority compositor checks all active sprites in parallel and selects the first hit, mirroring the classic hardware sprite priority chain.

The name *Flotilla* evokes a small fleet of vessels moving in formation across open water â€” a fitting image for a squadron of pixel sprites traversing the screen in coordinated waves.

---

## Background

### Demoscene Sprite Programming

The demoscene inherited sprite hardware from the game consoles and home computers of the 1980s. The Commodore 64's VIC-II chip offered eight hardware sprites, each 24Ã—21 pixels in a single colour or 12Ã—21 in multicolour mode. The Amiga's custom chipset provided eight 16-pixel-wide sprites with independent vertical and horizontal positioning. Demo coders pushed these systems far beyond their intended limits â€” multiplexing sprites mid-scanline, reusing them at different vertical positions, chaining them into larger composite objects. The technical constraint of a fixed number of small bitmaps became a creative medium: sprite choreography, formation flying, and wave effects were standard fare in demo intros and cracktros. Flotilla distills this tradition to its essentials: eight 8Ã—8 bitmaps, independently positioned, composited in real time.

### 8Ã—8 Bitmap Sprites and ROM Storage

An 8Ã—8 monochrome bitmap requires exactly 64 bits of storage â€” one bit per pixel. At this scale, every pixel matters: an arrow can be recognisable in a 5-pixel-wide silhouette, and a diamond is simply a rotated square with its corners trimmed. Storing these as 64-bit constants in FPGA fabric costs zero BRAM â€” the values are encoded directly into the lookup logic, consuming only a handful of LUTs. This is the same approach used by early arcade hardware, where character ROMs held 8Ã—8 tiles as fixed bit patterns. The Flotilla VHDL stores two shapes â€” arrow and diamond â€” as compile-time constants, selecting between them with a single multiplexer controlled by Toggle 7.

### Direct Digital Synthesis for Animation

Direct Digital Synthesis is a technique borrowed from signal generation, where a fixed-width accumulator is incremented by a tuning word on each clock (or frame). The upper bits of the accumulator directly represent the output phase or position. Because the accumulator wraps naturally at its bit width, DDS produces seamless cyclical motion without explicit bounds checking. In Flotilla, each sprite carries a 16-bit DDS accumulator for its movement axis. The upper 12 bits of the accumulator become the screen coordinate, giving smooth sub-pixel positioning and automatic screen-edge wrapping when the accumulator overflows. The Speed knob controls the tuning word â€” larger values produce faster motion â€” and each sprite adds a small per-index offset (iÃ—7 for horizontal, iÃ—5 for vertical) to stagger their phases, preventing the fleet from collapsing into a single point.

### Wave Formations

Military flight formations (echelon, V-formation, line abreast) are designed so that each member maintains a fixed offset from the leader while the group moves as a unit. Flotilla extends this concept with a wave modulation: the perpendicular offset of each sprite oscillates sinusoidally over time, controlled by Wave Amp (amplitude) and Wave Freq (oscillation rate). At zero amplitude, the sprites travel in a straight line with fixed vertical or horizontal staggering defined by the Y-offset constants. As amplitude increases, the formation spreads and contracts rhythmically, creating undulating wave patterns reminiscent of fish schools, bird flocks, or the classic side-scrolling shoot-'em-up enemy waves. The fixed offset constants place sprites at positions 0, Â±90, Â±180, Â±270, and +45 pixels, producing an asymmetric spread that avoids perfect symmetry.

### Sprite Priority Compositing

When multiple sprites overlap on the same pixel, classic hardware used a priority chain: sprite 0 wins over sprite 1, which wins over sprite 2, and so on. This is computationally trivial â€” a first-match scan â€” and produces deterministic layering without the complexity of z-buffering or alpha blending. Flotilla implements the same scheme: all active sprites are tested in parallel against the current pixel coordinate, and the lowest-numbered sprite that registers a hit determines the output colour. In mono mode, all sprites share the same hue; in multi mode, each sprite receives a distinct palette colour from an eight-entry fixed table, making the priority order visible when sprites cross paths.


---

## Signal Flow

```
[Per-Frame (vsync_start)]
â”œâ”€ Wave Phase Accumulator     (wave_phase += wave_freq, 16-bit)
â”œâ”€ LFSR Update                (16-bit feedback shift register)
â””â”€ DDS Position Update Ã— 8
    â”œâ”€ Direction = Right:  dds_x(i) += speed + iÃ—7
    â””â”€ Direction = Down:   dds_y(i) += speed + iÃ—5

[Per-Pixel Pipeline]
â”‚
â”œâ”€ Stage 1: Sprite Coordinate Setup
â”‚   â”œâ”€ For each sprite i (0..num_active-1):
â”‚   â”‚   â”œâ”€ Direction Right:
â”‚   â”‚   â”‚   â”œâ”€ sp_x = dds_x(i)[15:4]
â”‚   â”‚   â”‚   â””â”€ sp_y = 360 + Y_OFFSET(i) + (wave_amp>>3) Ã— i
â”‚   â”‚   â””â”€ Direction Down:
â”‚   â”‚       â”œâ”€ sp_y = dds_y(i)[15:4]
â”‚   â”‚       â””â”€ sp_x = 640 + Y_OFFSET(i) + (wave_amp>>3) Ã— i
â”‚   â”‚   â—„â”€â”€ Speed (pot 1), Wave Amp (pot 2), Direction (tog 8)
â”‚   â””â”€ Screen wrapping: sp_x mod 1920, sp_y mod 1080
â”‚
â”œâ”€ Stage 2: Hit Detection (all 8 sprites in parallel)
â”‚   â”œâ”€ rel = pixel_pos âˆ’ sprite_pos
â”‚   â”œâ”€ in_bounds = (0 â‰¤ rel_x < sprite_w) âˆ§ (0 â‰¤ rel_y < sprite_w)
â”‚   â”œâ”€ bitmap_col = rel_x >> size_shift, bitmap_row = rel_y >> size_shift
â”‚   â”œâ”€ pixel_on = bitmap[(7âˆ’row)Ã—8 + (7âˆ’col)]
â”‚   â””â”€ First-hit priority scan â†’ hit_sprite_idx
â”‚       â—„â”€â”€ Sprite Size (pot 4), Shape (tog 7), Count (pot 6)
â”‚
â”œâ”€ Stage 3: Color Mapping
â”‚   â”œâ”€ Hit pixel:
â”‚   â”‚   â”œâ”€ Y = 1023 (full bright)
â”‚   â”‚   â”œâ”€ Mono:  U = 512 + hue/4 âˆ’ 128,  V = 512 âˆ’ hue/8 + 64
â”‚   â”‚   â””â”€ Multi: U = PAL_U[idx],  V = PAL_V[idx]
â”‚   â””â”€ No hit:
â”‚       â”œâ”€ Black bg:  Y=0, U=V=512
â”‚       â””â”€ Video bg:  Y/U/V = input passthrough
â”‚       â—„â”€â”€ Hue (pot 5), Color (tog 9), Background (tog 10)
â”‚
â”œâ”€ Stages 4â€“8: Interpolator Mix (Ã—3 channels, 4 clk)
â”‚   â””â”€ mix = lerp(delayed_input, generated, mix_amount)
â”‚       â—„â”€â”€ Mix (fader 12)
â”‚
â”œâ”€ Sync Delay Pipeline         (5-clock shift register)
â”‚
â””â”€ Output Mux
    â”œâ”€ Bypass off â†’ mixed Y/U/V + aligned sync
    â””â”€ Bypass on  â†’ delayed input Y/U/V + aligned sync
        â—„â”€â”€ Bypass (tog 11)
```

The per-frame DDS update runs once during vertical blanking, incrementing each sprite's position accumulator by the Speed value plus a per-sprite offset. This staggered increment ensures sprites do not all move at exactly the same rate â€” sprite 0 is slowest, sprite 7 is fastest â€” which naturally spreads the formation over time even without wave modulation. The upper 12 bits of the 16-bit accumulator serve as the screen coordinate, providing smooth sub-pixel positioning at the cost of limiting the effective resolution to 4096 positions per axis, well beyond the 1920Ã—1080 screen.

Hit detection operates in a single clock cycle despite checking all eight sprites. Each sprite's bounds test and bitmap lookup is fully combinational, with the loop unrolled into parallel hardware. The first-match priority scan uses a cascaded conditional: if sprite 0 hits, its colour is selected regardless of whether sprites 1â€“7 also overlap. This mirrors the priority chain of classic sprite hardware and ensures deterministic rendering order without z-buffer overhead.

---

## Parameter Reference

<img src={flotilla_control_panel} alt="Videomancer front panel with Flotilla loaded"/>
*Videomancer's front panel with Flotilla active. Knobs 1â€“6 (top two rows of left cluster), Toggle switches 7â€“11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1â€“6)

#### Knob 1 â€” Speed
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 29% |
| Suffix | % |

Controls the base increment added to each sprite's DDS position accumulator per frame. At minimum, the sprites are nearly stationary â€” their only motion comes from the small per-index offset (iÃ—7 or iÃ—5), which slowly spreads the formation across the screen. At maximum, sprites race across the frame, wrapping around screen edges in rapid succession. The relationship between the knob and apparent velocity is linear: doubling the register value doubles the screen-space speed. Because each sprite adds a unique per-index contribution on top of the base speed, increasing Speed also increases the rate at which the formation stretches â€” at very high speeds, the fleet fans out across the full screen width before the slowest sprite completes a single traversal.

---

#### Knob 2 â€” Wave Amp
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 39% |
| Suffix | % |

Sets the amplitude of the wave formation spread. At zero, the formation spacing comes only from the fixed Y-offset constants, producing a static staggered arrangement. As Wave Amp increases, the perpendicular offset for each sprite grows proportionally to its index â€” sprite 0 stays centred while sprite 7 swings the widest. The effective offset is computed as the register value right-shifted by 3 bits and multiplied by the sprite index, yielding a maximum spread of approximately Â±896 pixels for the outermost sprite. Moderate values create a gentle undulation visible as a wave pattern; extreme values scatter the formation across the full screen height or width.

---

#### Knob 3 â€” Wave Freq
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 29% |
| Suffix | % |

Controls the rate at which the wave formation evolves over time. This parameter drives a 16-bit phase accumulator that modulates the formation shape frame by frame. At zero, the formation is static regardless of Wave Amp. At moderate values, the wave pattern ripples slowly â€” sprites drift in and out of tight formation over several seconds. At maximum, the wave oscillates rapidly, creating a shimmering, restless quality to the sprite arrangement. The visual effect is most dramatic when Wave Amp is set to a moderate value and Count is high, producing a visible sine wave of sprites that breathes and flexes as the phase accumulator cycles.

---

#### Knob 4 â€” Sprite Size
| Property | Value |
|----------|-------|
| Range | 1x â€“ 4x |
| Default | 2x |
| Suffix | x |

Selects the sprite magnification factor across four discrete steps. At step 1, each sprite occupies its native 8Ã—8 pixel footprint â€” tiny points on the HD canvas. Step 2 doubles each pixel to 16Ã—16, making the shape clearly identifiable. Step 3 expands to 32Ã—32, and step 4 fills a 64Ã—64 pixel region, rendering each bitmap detail as an 8Ã—8 block of solid colour. Magnification is achieved by right-shifting the pixel-relative coordinates before bitmap lookup, effectively repeating each texel across a square block. The sprite bounding box scales accordingly, so larger sprites are easier to see but more likely to overlap â€” particularly at high sprite counts with tight formation spacing.

---

#### Knob 5 â€” Hue
| Property | Value |
|----------|-------|
| Range | 0d â€“ 360d |
| Default | 0d |
| Suffix | d |

Sets the hue for monochrome colour mode. The 10-bit register value is converted to chroma offsets: U receives a quarter of the hue value minus 128, and V receives the complement. At register zero, the sprites are pure white (Y=1023, U=V=512). As the knob sweeps through its range, the sprites cycle through warm and cool tints â€” the mapping is not a true HSV rainbow but a simple linear ramp through the YUV chroma plane, producing distinctive colour shifts at each position. This parameter has no effect when Color is set to Multi, since each sprite draws from the fixed eight-entry palette instead.

---

#### Knob 6 â€” Count
| Property | Value |
|----------|-------|
| Range | 1 â€“ 8 |
| Default | 7 |

Selects how many sprites are active, from 1 to 8 in discrete steps. Inactive sprites are excluded from the hit detection loop â€” they are not rendered and cannot occlude active sprites. At 1, a single sprite traverses the screen alone. At 8, the full flotilla is deployed, and the formation pattern becomes visible. The default value of 7 (register 896) activates all eight sprites. Reducing the count simplifies the visual field and can clarify the motion of individual sprites when exploring speed and wave interactions. The active set always starts from sprite 0 â€” it is not possible to activate sprite 5 without also activating sprites 0â€“4.

---

### Toggle Switches (Switches 7â€“11)

| Switch | Off | On |
|--------|-----|-----|
| **7 â€” Shape** | Arrow | Diamond |
| **8 â€” Direction** | Right | Down |
| **9 â€” Color** | Mono | Multi |
| **10 â€” Background** | Black | Video |
| **11 â€” Bypass** | Off | On |

The five toggles divide into three functional clusters. Shape (7) and Direction (8) define the sprite geometry and motion axis â€” these are the structural controls that set up the visual character of the flotilla. Color (9) and Background (10) affect rendering appearance â€” mono versus palette colouring and whether non-sprite pixels show black or video passthrough. Bypass (11) overrides everything, routing the delayed input directly to output. All toggles operate independently and can be combined freely: a diamond fleet moving downward over video in multi-colour mode is as valid as an arrow fleet moving rightward over black in mono.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 â€” Mix
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the delayed input video and the composed sprite output. At 0% (fader down), the output is pure dry input â€” no sprites are visible. At 100% (fader up), the output is the fully composed sprite scene (either over black or over video, depending on Background). Intermediate positions blend the two, allowing the sprites to appear as semi-transparent overlays. In Black background mode at 50% mix, the sprites ghost over the input as luminous phantoms; in Video background mode, the mix blends two copies of the input â€” one with sprites, one without.

---

## Guided Exercises

These exercises progress from a single sprite through full-fleet formation flying. Because Flotilla is a synthesis program, output is generated from internal state â€” allow a few seconds for the DDS accumulators to spread the formation before evaluating the visual pattern.

### Exercise 1: Single Arrow Traversal

<img src={flotilla_exercise1_result} alt="Single Arrow Traversal result"/>
*Single Arrow Traversal â€” simulated result across source images.*
**Objective**: Observe a single sprite moving across the screen to understand DDS animation, screen wrapping, and magnification.

1. **Solo sprite**: Set Count to 1. Only sprite 0 is active.
2. **Moderate speed**: Set Speed to ~30%. The arrow moves rightward at a steady pace.
3. **Maximum size**: Set Sprite Size to 4Ã— (fully clockwise). The 8Ã—8 arrow is magnified to a clearly visible 64Ã—64 block.
4. **Watch wrapping**: Observe the sprite reach the right edge of the screen. It wraps seamlessly to the left side â€” the DDS accumulator overflow handles edge wrapping automatically.
5. **Change direction**: Flip Direction to Down. The arrow now descends vertically. Notice it starts at Y position derived from the DDS accumulator â€” there is no reset.
6. **Try 1Ã— size**: Set Sprite Size to 1Ã—. The sprite shrinks to a tiny 8Ã—8 dot â€” barely visible at 1080p but still moving smoothly.

**Key concepts**: DDS accumulators produce smooth linear motion, screen wrapping is automatic via accumulator overflow, magnification scales the bounding box and repeats bitmap texels, direction toggle swaps the movement axis without resetting position

---

### Exercise 2: Wave Formation

<img src={flotilla_exercise2_result} alt="Wave Formation result"/>
*Wave Formation â€” simulated result across source images.*
**Objective**: Deploy the full fleet and explore wave formation parameters to create undulating sprite patterns.

1. **Full fleet**: Set Count to 8. All sprites are active.
2. **Moderate speed**: Set Speed to ~30%. The fleet moves rightward, staggered by the per-index speed offsets.
3. **Add wave spread**: Increase Wave Amp to ~50%. The sprites spread vertically into a wave pattern â€” sprite 0 stays near centre while outer sprites swing wide.
4. **Animate the wave**: Increase Wave Freq to ~40%. The formation begins to ripple â€” sprites drift in and out of alignment as the wave phase advances.
5. **Multi colour**: Switch Color to Multi. Each sprite now shows a different hue from the palette, making individual sprites easy to track as they weave through the formation.
6. **Observe overlap**: Increase Sprite Size to 3Ã— or 4Ã—. At large sizes, sprites overlap â€” notice that sprite 0 (the first colour) always appears on top at intersections due to priority compositing.
7. **Vary amplitude**: Sweep Wave Amp from 0% to 100%. At zero, the fleet is a horizontal line; at maximum, sprites scatter across the full screen height.

**Key concepts**: Wave Amp controls formation spread, Wave Freq animates the spread over time, multi-colour mode makes individual sprites distinguishable, priority compositing determines overlap order, per-index speed offsets create natural formation staggering

---

### Exercise 3: Fleet Over Video

<img src={flotilla_exercise3_result} alt="Fleet Over Video result"/>
*Fleet Over Video â€” simulated result across source images.*
**Objective**: Composite the sprite flotilla over a live video input using Video background mode and the Mix fader to create a layered composition.

1. **Enable video background**: Set Background to Video. Ensure a video source is connected.
2. **Full fleet, diamond shape**: Set Count to 8, Shape to Diamond. The diamond shape is more symmetric and reads well as an overlay.
3. **Vertical motion**: Switch Direction to Down. The diamonds descend over the video like falling gems.
4. **Slow speed**: Set Speed to ~20%. A gentle descent allows individual sprites to be observed against the video content.
5. **Subtle wave**: Set Wave Amp to ~30%, Wave Freq to ~25%. The formation sways gently, creating organic motion.
6. **Mono colour**: Set Color to Mono, Hue to ~180Â°. All sprites share a single tint that contrasts with the video.
7. **Blend with Mix**: Pull Mix fader to ~60%. The sprites become semi-transparent, ghosting over the video as luminous shapes.
8. **Experiment with Hue**: Sweep the Hue knob to find a colour that complements the video content.

**Key concepts**: Video background passes input through non-sprite pixels, Mix fader controls sprite opacity over video, mono mode with Hue allows colour matching to video content, vertical motion creates a "falling" effect, diamond shape provides compact symmetric overlay

---


## Tips

- **Start with one sprite**: Set Count to 1 to understand DDS motion and wrapping before adding formation complexity. A single sprite at 4Ã— magnification is easy to track.
- **Wave Amp before Wave Freq**: Set a non-zero Wave Amp first â€” Wave Freq has no visible effect when Wave Amp is zero, since it modulates the amplitude of the formation spread.
- **Multi-colour for debugging**: Switch to Multi colour mode to distinguish individual sprites by index. This is invaluable when studying priority compositing at overlap points.
- **Video background for compositing**: Video mode layers the sprites over live input, turning Flotilla into a sprite overlay program. Combine with low Mix for subtle animated decorations.
- **Large sprites overlap more**: At 4Ã— magnification and high Count, sprites frequently overlap. Use this to study the priority chain â€” sprite 0 always wins.
- **Direction changes are non-destructive**: Toggling Direction swaps the axis but does not reset the DDS accumulators. The formation reorganises smoothly from whatever state it was in.
- **Speed zero freezes the fleet**: Setting Speed to 0% nearly stops all motion. The small per-index offsets (iÃ—7 or iÃ—5) still produce very slow relative drift, gradually spreading the formation.
- **Mix fader for transparency**: In Video background mode, pulling Mix to 50â€“70% creates semi-transparent sprites that ghost over the video â€” effective for atmospheric layering.

---

## Glossary

| Term | Definition |
|------|------------|
| **Accumulator** | A register that sums an increment value on each frame or clock cycle, producing a linearly increasing value that wraps at the register width. |
| **Bitmap** | A pixel grid where each element stores a fixed number of bits; in Flotilla, 1-bit per pixel (on or off) in an 8Ã—8 arrangement. |
| **Compositing** | The process of combining multiple visual layers into a single output image, here performed by overlaying sprite pixels over a background. |
| **DDS (Direct Digital Synthesis)** | A technique for generating smooth cyclical motion or waveforms using a fixed-width accumulator incremented by a tuning word; the upper bits represent the output value. |
| **Demoscene** | A computer art subculture focused on producing real-time audio-visual demonstrations that push hardware capabilities, originating on 1980s home computers. |
| **Formation** | A spatial arrangement of multiple elements (sprites) maintaining defined relative positions while moving as a group. |
| **LFSR (Linear Feedback Shift Register)** | A shift register whose input bit is a linear function of its previous state, used for pseudorandom sequence generation. |
| **LUT (Look-Up Table)** | The basic logic element in an FPGA, used here to measure resource consumption (~1300 LUTs for Flotilla). |
| **Magnification** | Scaling a bitmap by repeating each pixel across a larger block; 2Ã— doubles each dimension, 4Ã— quadruples it. |
| **Priority chain** | A compositing rule where the lowest-numbered overlapping element wins, common in hardware sprite systems. |
| **Screen wrapping** | When an object exits one edge of the screen it re-enters from the opposite edge, implemented here via modular arithmetic on position coordinates. |
| **Tuning word** | The increment value added to a DDS accumulator each cycle; larger values produce faster motion or higher frequency. |
| **YUV** | A colour model separating luminance (Y) from two chrominance components (U and V), used throughout Videomancer's video pipeline. |

---
