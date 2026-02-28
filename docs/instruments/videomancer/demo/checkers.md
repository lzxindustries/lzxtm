---
draft: true
sidebar_position: 42
slug: /instruments/videomancer/checkers
title: "Checkers"
image: /img/instruments/videomancer/checkers/checkers_hero.png
description: "Program guide for Checkers, a Videomancer demo program for the LZX video synthesizer."
---

import checkers_hero from '/img/instruments/videomancer/checkers/checkers_hero.png';
import checkers_animation from '/img/instruments/videomancer/checkers/checkers_animation.gif';
import checkers_control_panel from '/img/instruments/videomancer/checkers/checkers_control_panel.png';
import checkers_exercise1_result from '/img/instruments/videomancer/checkers/checkers_exercise1_result.gif';
import checkers_exercise2_result from '/img/instruments/videomancer/checkers/checkers_exercise2_result.gif';
import checkers_exercise3_result from '/img/instruments/videomancer/checkers/checkers_exercise3_result.gif';

# Checkers

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={checkers_hero} alt="Checkers hero image"/>
*Checkers projecting an infinite monochrome floor toward a fog-veiled horizon â€” tiles shrink in strict perspective, Z-scroll frozen mid-stride, the floor receding into gray nothingness.*
<img src={checkers_animation} alt="Checkers animated output"/>
*Checkers output evolving over multiple frames â€” synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Somewhere in the early 1990s, a coder with a 68000 and a framebuffer figured out that you do not need division to draw a checkerboard floor stretching toward infinity. You need a running step that gets smaller as you approach the horizon, a couple of texture coordinates, and a one-bit XOR to decide which tile is black and which is white. The floor appeared in countless Amiga and Atari ST demos â€” a receding plane of alternating squares that conveyed three-dimensional depth with almost no computational cost. Checkers recreates that effect in dedicated FPGA hardware, rendering a perspective-projected infinite floor at 74.25 MHz with zero BRAM and approximately 600 logic cells.

The screen is divided at a configurable horizon line. Below the horizon, a perspective-projected checkerboard extends to infinity, each scanline computed independently with a step size inversely proportional to its distance from the horizon. Above the horizon, the sky region either passes through the input video (overlay mode) or shows a dark blue sky (replace mode). The checkerboard pattern is the simplest possible: a single XOR of the upper bits of the U and V texture coordinates. Distance-based fog blends tiles toward mid-gray as they approach the horizon, providing natural depth cues and hiding the aliasing that would otherwise appear at extreme foreshortening. An animated Z-scroll creates the illusion of forward motion â€” the classic demoscene infinite floor rush.

At conservative settings, Checkers produces a clean geometric pattern suitable for compositing. At extreme settings â€” fast scroll, tiny tiles, high fog â€” it becomes a hypnotic tunnel of receding geometry, tiles flickering past faster than the eye can track. The name *Checkers* is the obvious one: a game board stretching to infinity.

---

## Background

### The Demo Infinite Floor

The infinite checkerboard floor is one of the oldest and most recognized effects in the demoscene. It appeared in demos by groups like Scoopex, Phenomena, and Silents on the Amiga, and was a staple of the Atari ST scene as well. The technique exploits a fundamental property of perspective projection: objects further from the viewer appear smaller. For a flat floor, this means each successive scanline (moving from the bottom of the screen toward the horizon) represents a greater distance from the viewer, and the texture appears correspondingly compressed. Rather than computing a true perspective divide ($1/z$) for every pixel â€” which was prohibitively expensive on 16/32-bit home computers â€” the demos used per-scanline accumulators that approximate the same foreshortening with only shifts and additions.

### Perspective Without Division

True perspective projection of a texel onto the screen requires dividing by the depth $z$. On hardware without a fast divider, coders approximated this by observing that for a flat plane, the pixel-to-texel step size is proportional to $1/d$, where $d$ is the distance (in scanlines) from the horizon. Computing $1/d$ exactly is still a divide, but finding the leading bit of $d$ gives a cheap logarithmic approximation. If $d$ has its highest set bit at position $n$, then $1/d \approx 2^{-n}$. This is what Checkers implements: a priority-encoder-style cascade that determines the leading bit of the distance and shifts a base step value accordingly. The approximation introduces visible "banding" in tile widths near the horizon, but the fog mask hides most of this.

### The XOR Checker Pattern

The checkerboard is perhaps the simplest possible two-dimensional pattern. Given texture coordinates $U$ and $V$, the checker value is the XOR of a single bit from each: $\text{checker} = U[k] \oplus V[k]$. When this bit is 1, the tile is bright; when 0, the tile is dark. The bit chosen determines the tile spatial frequency â€” higher bits produce larger tiles. In Checkers, the XOR operates on bit 15 of the 20-bit texture coordinates, with the Tile Size parameter controlling how rapidly those coordinates accumulate and thus how many tiles are visible across the frame.

### Distance-Based Fog

As tiles approach the horizon, their on-screen size shrinks toward zero, creating extreme aliasing and MoirÃ© patterns. Demo coders solved this visually (if not mathematically) with distance fog: tiles nearest the horizon are blended toward a neutral background colour. In Checkers, the fog is computed as the complement of the distance from the horizon, clamped by the Fog Dist parameter. Tiles close to the bottom of the screen (near the viewer) receive zero fog. Tiles near the horizon receive maximum fog, fading toward mid-gray (YUV value 512). This serves both the aesthetic purpose of depth perception and the practical purpose of masking perspective artifacts where the approximation is coarsest.

### Z-Scroll and the Tunnel Effect

Adding a constant offset to the V texture coordinate each frame creates the illusion of forward motion along the floor. The floor appears to rush toward the viewer, tiles emerging from the fog at the horizon and sweeping downward to pass beneath. In Checkers, the Z-scroll is implemented as a 16-bit accumulator that increments by the Speed parameter value on each vertical sync. The accumulated value is added to the base V texture coordinate at frame start, so the entire texture map slides continuously. Disabling scroll (Toggle 7) freezes the floor in place, useful for static compositions or when the checkerboard is used purely as a spatial pattern.


---

## Signal Flow

```
Video Input (YUV 4:4:4)
â”‚
â”œâ”€ Timing Generator           (extracts hsync/vsync/avid â†’ h_count, v_count)
â”‚
â”œâ”€ Z-Scroll Accumulator        (per-frame: z_scroll += speed, when scroll=on)
â”‚
â”œâ”€ Perspective Engine (per-scanline, at avid_start)
â”‚   â”œâ”€ distance = v_count âˆ’ horizon_line
â”‚   â”œâ”€ persp_step = tile_scale << log2_approx(1/distance)
â”‚   â””â”€ tex_v_accum += persp_step                   (running V coord)
â”‚       â—„â”€â”€ Tile Size (pot 2), Horizon (pot 3)
â”‚
â”œâ”€ Stage 1: Texture U Coordinate (per-pixel)
â”‚   â”œâ”€ tex_u = (h_count âˆ’ 640) Ã— persp_step + pan_offset
â”‚   â”œâ”€ fog_level = fog_dist âˆ’ dist_from_horizon     (clamped â‰¥ 0)
â”‚   â””â”€ pass through: below_horizon flag, input Y/U/V
â”‚       â—„â”€â”€ Pan X (pot 5), Fog Dist (pot 4)
â”‚
â”œâ”€ Stage 2: Checker XOR
â”‚   â””â”€ checker = tex_u(15) XOR tex_v(15)
â”‚
â”œâ”€ Stage 3: Color + Fog
â”‚   â”œâ”€ Below horizon:
â”‚   â”‚   â”œâ”€ tile_y = checker ? bright : bright/4
â”‚   â”‚   â”œâ”€ fogged_y = lerp(tile_y, 512, fog_level)
â”‚   â”‚   â”œâ”€ if invert: fogged_y = 1023 âˆ’ fogged_y
â”‚   â”‚   â”œâ”€ Color mode: mono (U=V=512) or RGB (red/blue alternation)
â”‚   â”‚   â””â”€ â—„â”€â”€ Bright (pot 6), Invert (tog 10), Color (tog 8)
â”‚   â””â”€ Above horizon:
â”‚       â”œâ”€ Replace mode: sky (Y=64, U=600, V=400)
â”‚       â””â”€ Overlay mode: pass input Y/U/V
â”‚           â—„â”€â”€ Render (tog 9)
â”‚
â”œâ”€ Stage 4: Compose
â”‚   â”œâ”€ Replace mode: output tile/sky directly
â”‚   â””â”€ Overlay mode (below horizon): Y = input_Y Ã— tile_Y / 1024
â”‚
â”œâ”€ Stages 5â€“8: Interpolator Mix (Ã—3 channels, 4 clk)
â”‚   â””â”€ mix = lerp(delayed_input, composed, mix_amount)
â”‚       â—„â”€â”€ Mix (fader 12)
â”‚
â”œâ”€ Sync Delay Pipeline          (8-clock shift register)
â”‚
â””â”€ Output Mux
    â”œâ”€ Bypass off â†’ mixed Y/U/V + aligned sync
    â””â”€ Bypass on  â†’ delayed input Y/U/V + aligned sync
        â—„â”€â”€ Bypass (tog 11)
```

The perspective engine operates once per scanline (triggered by `avid_start`) rather than once per pixel. It computes a single step value proportional to $1/\text{distance}$ and accumulates the V texture coordinate, then holds both values constant while the per-pixel pipeline scans horizontally. The U coordinate is recomputed every pixel by multiplying the horizontal position by the same step value, keeping tiles square in both axes. This separation â€” per-scanline V accumulation, per-pixel U computation â€” is the core of the division-free perspective trick: the expensive reciprocal approximation happens only 720 times per frame (once per active line) rather than 921,600 times (once per pixel).

The fog computation is deliberately linear rather than exponential. When the scanline distance from the horizon is less than the Fog Dist parameter, fog increases linearly toward the horizon. This is physically imprecise but computationally trivial â€” a single subtraction â€” and produces a smooth gradient that effectively masks the perspective banding artifacts near the horizon where the log2 approximation is coarsest.

---

## Parameter Reference

<img src={checkers_control_panel} alt="Videomancer front panel with Checkers loaded"/>
*Videomancer's front panel with Checkers active. Knobs 1â€“6 (top two rows of left cluster), Toggle switches 7â€“11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1â€“6)

#### Knob 1 â€” Speed
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 25% |
| Suffix | % |

Controls the rate at which the Z-scroll accumulator advances each frame. At 0%, the accumulator does not increment and the floor is stationary. At 100%, each frame adds the maximum step to the V texture origin, producing fast forward-rushing motion. The speed is linear â€” doubling the knob value doubles the apparent floor velocity. When scroll is disabled via Toggle 7, this parameter has no effect regardless of its value. Intermediate values around 25% produce a gentle drift suitable for ambient backdrops; values above 75% create a rapid tunnel-rush effect where individual tiles are barely visible as they streak past.

---

#### Knob 2 â€” Tile Size
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial frequency of the checkerboard tiles by scaling the base perspective step. The step value is derived from this parameter via a 3-bit shift extracted from the upper bits, yielding tile scales from 1Ã— to 12Ã—. Lower values produce larger, fewer tiles that dominate the frame. Higher values produce smaller, more numerous tiles that create a finer texture receding toward the horizon. Because the same step scales both U and V coordinates, tiles remain square regardless of the setting. The perceptual effect is dramatic: low tile size shows a handful of massive squares, while high tile size fills the floor with a dense mosaic that blurs into fog at the horizon.

---

#### Knob 3 â€” Horizon
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 38% |
| Suffix | % |

Sets the vertical position of the horizon line, mapped from the 10-bit register to the 0â€“719 scanline range. At 0%, the horizon sits at the top of the frame, and the entire screen is filled with checkerboard floor. At 100%, the horizon drops to the bottom of the frame, and the entire screen shows sky or input video. The default position (~38%) places the horizon roughly a third of the way down â€” a natural composition with two-thirds floor and one-third sky, consistent with Renaissance perspective conventions. Extreme positions allow using the checker floor as a narrow strip or filling the entire frame for maximal geometric immersion.

---

#### Knob 4 â€” Fog Dist
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 75% |
| Suffix | % |

Controls how far the fog extends from the horizon. At 0%, there is no fog and tiles remain at full contrast all the way to the horizon â€” revealing the banding artifacts of the log2 perspective approximation. At 100%, the fog region extends far from the horizon, blending a large portion of the visible floor toward mid-gray. The fog is linear: within the fog zone, tile brightness transitions smoothly from full contrast (at the fog boundary) to pure gray (at the horizon). Medium values around 75% maintain visible geometry in the foreground while softening the transition into the deep field, striking a balance between realism and visual clarity.

---

#### Knob 5 â€” Pan X
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

Shifts the horizontal texture origin by adding an offset to the U coordinate. At 50% (centre), the texture is centred on the screen. Turning left shifts the floor pattern to the right; turning right shifts it to the left. This allows repositioning the checkerboard laterally within the composition â€” useful for aligning the vanishing point with other elements in a video chain. The offset is scaled by 8 bits (multiplied by 256) before addition, providing a wide spatial range. When combined with Z-scroll, Pan X creates diagonal apparent motion â€” the floor rushes forward while sliding sideways.

---

#### Knob 6 â€” Bright
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 75% |
| Suffix | % |

Sets the peak brightness of the lighter checker tiles. The bright tiles receive this value directly; the dark tiles receive one-quarter of it (a 2-bit right shift). At 0%, both tiles are black and the floor is invisible. At 100%, bright tiles reach maximum white (1023) and dark tiles reach a quarter-brightness gray (255). The fog blend operates on this brightness â€” tiles near the horizon fade toward mid-gray regardless of this setting. When Invert is active, the brightness mapping reverses after fog is applied, so what was bright becomes dark and vice versa. This parameter essentially controls the contrast ratio of the checkerboard.

---

### Toggle Switches (Switches 7â€“11)

| Switch | Off | On |
|--------|-----|-----|
| **7 â€” Scroll** | Off | On |
| **8 â€” Color** | Mono | RGB |
| **9 â€” Render** | Overlay | Replace |
| **10 â€” Invert** | Off | On |
| **11 â€” Bypass** | Off | On |

The five toggles partition cleanly into three functional groups. Scroll (7) controls animation, enabling or disabling the frame-to-frame Z-scroll accumulator. Color (8) and Invert (10) affect the checker tile appearance â€” Color switches between mono and RGB colorization, while Invert complements the fogged luma. Render (9) determines the compositing strategy â€” Replace generates the entire frame (floor below horizon, dark sky above), while Overlay uses the input video above the horizon and modulates video luma by the checker pattern below. Bypass (11) overrides everything, routing the delayed input directly to the output. All five operate independently and can be combined freely.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 â€” Mix
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the delayed input video and the composed checkerboard output. At 0% (fader down), the output is pure dry input â€” no checkerboard is visible. At 100% (fader up), the output is the fully composed checkerboard (either replaced or overlaid, depending on Render mode). Intermediate positions blend the two, allowing the checkerboard to appear as a semi-transparent overlay. In Replace mode at 50% mix, the checkerboard floor is ghosted over the input video â€” useful for aligning the generated pattern with live elements.

---

## Guided Exercises

These exercises build from a static floor through animated scroll to complex overlay compositions. Because Checkers is a generative synthesis program, each exercise produces output from scratch â€” allow a few seconds for the animation to settle before evaluating the visual result.

### Exercise 1: Static Infinite Floor

<img src={checkers_exercise1_result} alt="Static Infinite Floor result"/>
*Static Infinite Floor â€” simulated result across source images.*
**Objective**: Understand how the perspective projection, horizon position, and tile size interact to form the basic infinite floor.

1. **Disable scroll**: Set Scroll (Toggle 7) to Off. The floor will be static.
2. **Set the horizon**: Turn Horizon to ~38%. The division between floor and sky should sit about one-third down from the top of the frame.
3. **Large tiles**: Set Tile Size to ~25%. The floor shows a few large squares receding into the distance.
4. **Adjust fog**: Set Fog Dist to ~75%. Tiles near the horizon fade smoothly into gray, masking any perspective banding.
5. **Full brightness**: Set Bright to ~75%. The bright tiles should be clearly visible against the dark tiles.
6. **Observe perspective**: Note how tiles near the bottom of the frame (closest to the viewer) are large and high-contrast, while tiles near the horizon are compressed and fogged.
7. **Shrink tiles**: Slowly increase Tile Size toward 80%. The floor fills with a dense grid of smaller squares. Watch how the fog hides the increased aliasing near the horizon.

**Key concepts**: Horizon position divides screen into floor and sky, tile size controls spatial frequency of the checker pattern, fog hides perspective artifacts near the horizon, perspective compression is visible as tiles shrink with distance

---

### Exercise 2: Tunnel Rush with Colour

<img src={checkers_exercise2_result} alt="Tunnel Rush with Colour result"/>
*Tunnel Rush with Colour â€” simulated result across source images.*
**Objective**: Explore Z-scroll animation and RGB colourization to create a dynamic forward-rushing floor.

1. **Enable scroll**: Set Scroll (Toggle 7) to On.
2. **Moderate speed**: Set Speed to ~50%. The floor begins scrolling forward â€” tiles emerge from the horizon fog and rush toward the viewer.
3. **Medium tiles**: Set Tile Size to ~50%. A balanced grid density that shows clear tile edges during motion.
4. **Enable colour**: Switch Color (Toggle 8) to RGB. Alternating tiles now show warm red-orange and cool blue-cyan, creating a vibrant chromatic runway.
5. **Increase speed**: Push Speed toward 80%. The tiles streak past rapidly â€” the tunnel-rush effect becomes hypnotic at high velocities.
6. **Pan sideways**: Slowly turn Pan X away from centre (~70%). The floor appears to drift diagonally, as if the viewer is strafing rather than moving straight ahead.
7. **Lower horizon**: Bring Horizon down to ~60%. The floor occupies less of the frame, and the sky region expands. The rushing tiles are compressed into a narrow band at the bottom.

**Key concepts**: Z-scroll creates forward motion through the tile field, Speed controls scroll rate linearly, RGB mode adds complementary colour to alternate tiles, Pan X introduces lateral drift, lowering the horizon shrinks the floor region

---

### Exercise 3: Overlay Composition

<img src={checkers_exercise3_result} alt="Overlay Composition result"/>
*Overlay Composition â€” simulated result across source images.*
**Objective**: Composite the checkerboard floor over an input video signal using Overlay mode and the Mix fader.

1. **Switch to Overlay**: Set Render (Toggle 9) to Overlay.
2. **Feed video**: Ensure a video source is connected to the input.
3. **Set mix**: Push Mix fader to ~70%. The composed output blends with the input â€” above the horizon, the video passes through cleanly; below, the checker pattern modulates the video luma.
4. **Slow scroll**: Set Speed to ~20%, Scroll On. The floor drifts gently, and the multiplicative overlay creates a slowly shifting grid pattern on the lower portion of the video.
5. **Enable invert**: Toggle Invert (Toggle 10) to On. The bright/dark tile mapping reverses, and the modulation pattern swaps â€” portions of the video that were darkened are now bright and vice versa.
6. **Reduce mix**: Pull Mix to ~40%. The checker overlay becomes subtle, serving as a semi-transparent texture layer over the video.
7. **Pan slowly**: Sweep Pan X back and forth. The floor slides laterally under the video, creating a moving geometric texture.

**Key concepts**: Overlay mode modulates input video by checker brightness, video above the horizon passes through unaffected, Mix fader controls overlay intensity, Invert reverses the modulation pattern, gentle scroll and low mix create subtle animated textures

---


## Tips

- **Start with Replace mode**: Replace mode generates a complete frame, making it easier to understand the perspective engine before adding video overlay complexity.
- **Use fog to taste**: Zero fog reveals the raw perspective approximation and its banding. A moderate fog setting (60â€“80%) smooths the transition while keeping foreground tiles crisp. Very high fog fades most of the floor to gray.
- **Pan X for composition**: Pan X lets you offset the vanishing point laterally. Use it to position the floor pattern relative to other elements in a video chain.
- **Speed zero is valid**: Disabling scroll and setting Speed to 0% creates a perfectly static floor â€” useful as a geometric overlay or key pattern.
- **RGB mode for psychedelia**: RGB colour with high-speed scroll creates a hypnotic rush of alternating red and blue tiles. Add Invert for a negative-image variant.
- **Overlay for texture**: In Overlay mode with low Mix, the checkerboard becomes a subtle geometric texture over the video â€” effective as a compositional grid or spatial reference.
- **Invert changes fog direction**: Because inversion happens after fog, the fog gradient also inverts â€” the horizon region becomes bright instead of gray, which can create an interesting glowing horizon effect.
- **Bypass for glitch-free switching**: Toggle 11 bypasses all processing at the output mux. Use it for instant comparison without affecting the running scroll accumulator.

---

## Glossary

| Term | Definition |
|------|------------|
| **Accumulator** | A register that sums an increment value on each clock or frame, used here for the Z-scroll offset and the per-scanline V texture coordinate. |
| **Demoscene** | A computer art subculture focused on producing real-time audio-visual demonstrations that push hardware capabilities, originating on 1980s home computers. |
| **Foreshortening** | The apparent compression of objects or texture along the depth axis in a perspective view, causing distant tiles to appear smaller and narrower. |
| **FPGA (Field-Programmable Gate Array)** | A reconfigurable integrated circuit whose logic function is defined by a hardware description language rather than fixed at manufacture. |
| **Log2 approximation** | An estimation of the reciprocal 1/d by finding the position of the leading set bit, avoiding a full hardware division. |
| **MoirÃ© pattern** | A visual interference artefact produced when two regular patterns overlap at slightly different scales or angles, visible here when tiles become very small near the horizon. |
| **Perspective projection** | The geometric transformation that maps three-dimensional scene coordinates to two-dimensional screen coordinates, causing distant objects to appear smaller. |
| **Texel** | A single element of a texture map; the texture-space analogue of a pixel in screen space. |
| **XOR (Exclusive-OR)** | A logic operation that returns true when exactly one of two inputs is true, used here to generate the alternating checker pattern from texture coordinate bits. |
| **YUV** | A colour model that separates luminance (Y) from two chrominance components (U and V), widely used in video signal processing. |
| **Z-scroll** | A per-frame offset added to the depth texture coordinate, creating the illusion of forward motion through the tile field. |

---
