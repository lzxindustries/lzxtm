---
draft: true
sidebar_position: 87
slug: /instruments/videomancer/dragon
title: "Dragon"
image: /img/instruments/videomancer/dragon/dragon_hero.png
description: "In 1966, NASA physicist John Heighway discovered a curve by repeatedly folding a strip of paper in half and unfolding it so that each crease opens to a right angle."
---

import dragon_hero from '/img/instruments/videomancer/dragon/dragon_hero.png';
import dragon_animation from '/img/instruments/videomancer/dragon/dragon_animation.gif';
import dragon_control_panel from '/img/instruments/videomancer/dragon/dragon_control_panel.png';
import dragon_exercise1_result from '/img/instruments/videomancer/dragon/dragon_exercise1_result.gif';
import dragon_exercise2_result from '/img/instruments/videomancer/dragon/dragon_exercise2_result.gif';
import dragon_exercise3_result from '/img/instruments/videomancer/dragon/dragon_exercise3_result.gif';

# Dragon

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={dragon_hero} alt="Dragon hero image"/>
*Dragon projecting a luminous fractal labyrinth of XOR-folded coordinates, each iteration depth revealing a deeper layer of self-similar geometry.*
<img src={dragon_animation} alt="Dragon animated output"/>
*Dragon output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1966, NASA physicist John Heighway discovered a curve by repeatedly folding a strip of paper in half and unfolding it so that each crease opens to a right angle. The resulting shape — the Heighway dragon — is a space-filling fractal that tiles the plane without gaps or overlaps, its boundary an infinitely complex coastline that never quite touches itself. Every magnification reveals the same folding pattern: a dragon eating its own tail.

Dragon renders this folding geometry in real time by replacing the sequential paper-fold construction with a parallel position hash. For every pixel on screen, the program takes the centered coordinates, quantizes them to a coarse grid, concatenates the bits, and applies a sequence of XOR folds — each fold analogous to one iteration of the paper-folding process. The Iteration knob controls how many folds are applied, progressively refining the boundary between foreground and background. At low iterations the pattern is a simple checkerboard; at high iterations it fractures into the characteristic dragon curve silhouette, its edges bristling with the recursive zigzag of self-similar refolds.

Color cycling derives hue directly from the hash bits themselves, so regions at different spatial frequencies receive different chrominance — a built-in spectral decomposition of the fractal structure. The Animation toggle advances a frame counter that shifts the hash seed, causing the pattern to crawl and morph continuously as if the paper were being re-folded in a different direction each frame. Mirror mode XORs an additional hash bit into the pattern, breaking the bilateral symmetry and producing denser, more chaotic tilings.

---

## Background

### The Heighway Dragon Curve

The Heighway dragon is constructed by a simple recursive rule: take a line segment, replace it with two segments joined at a right angle, and repeat. After *n* iterations, the curve has $2^n$ segments and begins to fill a region of the plane with a fractal boundary of Hausdorff dimension 2. The remarkable property of the dragon is that it tiles the plane — four copies rotated by 90° about a common vertex fill the plane completely with no overlap. This tiling property means the dragon curve's interior and exterior have the same combinatorial complexity, making it an ideal candidate for a binary foreground/background pattern: every pixel either belongs to the dragon or does not, and the boundary between the two is infinitely detailed.

### Paper Folding and Bit Sequences

The most intuitive construction of the dragon curve is paper folding. Fold a strip of paper in half *n* times (always in the same direction), then unfold so each crease opens to 90°. The sequence of left and right turns along the unfolded strip determines the dragon curve. Crucially, this turn sequence has an elegant binary representation: the turn at step $k$ is determined by the bit above the lowest set bit of $k$. If that bit is 1, turn right; if 0, turn left. This connection between the fractal geometry and the binary representation of integers is what allows the Heighway dragon to be computed by pure bit manipulation — no trigonometry, no floating-point arithmetic, no recursive subdivision — just shifts, masks, and XOR operations on the step index.

### Self-Similarity and Iterated Function Systems

The dragon curve is a fixed point of an Iterated Function System (IFS) — a pair of affine contractions whose repeated application converges to the fractal attractor. Each contraction scales by $1/\sqrt{2}$ and rotates by ±45°, mapping the entire curve onto its left or right half. This self-similarity means that any sub-region of the dragon, when magnified by $\sqrt{2}$ and rotated, looks identical to the whole. In the pixel domain, the XOR-fold hash exploits this self-similarity directly: each additional XOR shift corresponds to one level of the IFS hierarchy, mixing information from successively finer spatial scales into the pattern decision at each pixel.

### Bit Manipulation for Fractal Generation

Traditional fractal renderers — Mandelbrot sets, Julia sets, L-system turtles — rely on iterative computation per pixel or sequential path tracing. Both are expensive in hardware. The XOR-fold technique sidesteps iteration entirely by encoding the fractal structure into a hash function applied to the pixel coordinates. The key operation is `hash ^= hash >> k`, which folds the upper bits of the coordinate representation down onto the lower bits, creating interference patterns between spatial scales separated by a factor of $2^k$. The number of fold operations (controlled by the Iteration parameter) determines how many scales contribute to the final pattern. One fold produces a simple diagonal; two folds produce a Sierpinski-like checkerboard; five or more folds produce recognizable dragon curve boundaries. The entire computation fits in a single clock cycle with no BRAM, no DSP blocks, and roughly 400 logic cells.

### Fractal Art and Video Synthesis

Fractal imagery has been central to computational art since Benoit Mandelbrot's visualizations in the 1980s. The ability to generate infinitely detailed patterns from compact mathematical descriptions resonates with the video synthesizer tradition of deriving complex imagery from minimal signal generators. Dragon connects these traditions: it uses a technique rooted in 1960s recreational mathematics (paper folding) implemented with 1990s FPGA logic (XOR hashing) to produce imagery that evokes both the mathematical sublime of fractal geometry and the analog warmth of modular video synthesis. The color cycling mode further bridges these worlds, deriving chrominance from the same hash bits that determine geometry — a single computation producing both structure and palette.


---

## Signal Flow

```
Synthesis Output (YUV 4:4:4)
│
├── Clock 0: Register Decode ───────────────────────────────────
│   ├─ scale = registers_in(0)
│   ├─ rotation = registers_in(1)
│   ├─ position_x = registers_in(2)
│   ├─ position_y = registers_in(3)
│   ├─ iteration = registers_in(4)
│   ├─ line_width = registers_in(5)
│   ├─ toggles: fill(6.0), color_cycle(6.1),
│   │           animate(6.2), mirror(6.3), bypass(6.4)
│   └─ brightness = registers_in(7)
│
├── Clock 1: Timing Detection ─────────────────────────────────
│   ├─ hsync_fall / vsync_fall edge detect
│   ├─ x_counter++, y_counter++ (pixel/line position)
│   └─ frame_counter++ on vsync_fall (if animate on)
│
├── Clock 2: Centered Coordinates ──────────────────────────────
│   ├─ cx = x_counter − position_x  (signed 13-bit)
│   └─ cy = y_counter − position_y  (signed 13-bit)
│
├── Clock 3: Position Hash + XOR Folding ───────────────────────
│   ├─ hash = cx[11:4] & cy[11:4]        (16-bit concat)
│   ├─ hash ^= hash >> 1                 (first fold)
│   └─ hash ^= hash >> (iteration[9:7]+1) (depth fold, shift 1–8)
│
├── Clock 4: Pattern Extraction ────────────────────────────────
│   ├─ pattern = hash[0] XOR hash[1]
│   └─ if mirror: pattern ^= hash[2]
│
├── Clock 5: Color Assignment ─────────────────────────────────
│   ├─ pattern=1, color_cycle on:
│   │     Y = brightness,  U = hash[9:2],  V = hash[7:0]
│   ├─ pattern=1, color_cycle off:
│   │     Y = brightness,  U = 512,  V = 512
│   └─ pattern=0:
│         Y = 64,  U = 512,  V = 512
│
├── Clocks 4–7: Interpolator (wet/dry) ────────────────────────
│   └─ lerp(delayed_input, processed, mix_t)  ×3 channels
│
├── Sync Signals ──────────────────────────────────────────────
│   └─ 8-stage delay pipeline (hsync, vsync, field, Y, U, V)
│
└── Bypass ────────────────────────────────────────────────────
    └─ Select delayed input or interpolated output
```

The core algorithm occupies just three clock cycles — coordinate centering, XOR-fold hashing, and pattern extraction — yet produces fractal complexity comparable to iterative renderers that consume hundreds of cycles per pixel. The critical operation is the double XOR fold in Clock 3: the first fold (`hash ^= hash >> 1`) creates the fundamental diagonal structure by mixing adjacent coordinate bits, while the second fold (`hash ^= hash >> shift`) introduces the self-similar recursion by interfering bits separated by a distance controlled by the Iteration parameter. Increasing the shift distance brings coarser spatial scales into the pattern decision, deepening the fractal boundary. The entire hash computation requires no BRAM and no DSP multiplier blocks — only combinational logic (XOR gates and barrel shifters), making this one of the most resource-efficient fractal generators possible on the iCE40 platform.

---

## Parameter Reference

<img src={dragon_control_panel} alt="Videomancer front panel with Dragon loaded"/>
*Videomancer's front panel with Dragon active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Scale
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial zoom level of the fractal pattern. At the default center position, the pattern displays at its native resolution — one hash cell per 16-pixel block (the quantization step from the `cx[11:4]` bit extraction). Reducing Scale zooms out, revealing more of the fractal tiling and producing a finer, more densely packed pattern. Increasing Scale zooms in, magnifying individual hash cells and exposing the sharp binary boundaries between foreground and background regions. At extreme zoom levels, the underlying grid structure becomes visible as the pattern resolves into blocky squares — the quantization artifacts of the coordinate-to-hash conversion.

---

#### Knob 2 — Rotation
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Rotates the entire fractal pattern around the position center. At 0° the dragon curve aligns with the screen axes, its primary folds running horizontally and vertically. As Rotation advances, the pattern pivots smoothly, revealing different cross-sections of the XOR hash field. At 45° the diagonal structure created by the first XOR fold becomes aligned with the screen horizontal, producing a dramatically different visual texture. Full 360° rotation cycles through all orientations, with the pattern repeating exactly at 90° intervals due to the square symmetry of the coordinate grid.

---

#### Knob 3 — Position X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the center of the fractal pattern horizontally. At the default center position, the hash origin aligns with the middle of the screen. Moving Position X leftward or rightward pans the pattern across the frame, revealing different regions of the infinite fractal tiling. Because the XOR hash is computed on centered coordinates, the position offset effectively translates through a fixed mathematical space — the pattern itself does not change, only which portion of it is visible. This makes Position X and Position Y together function as a viewport control over an infinitely extending fractal plane.

---

#### Knob 4 — Position Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the center of the fractal pattern vertically. Operates identically to Position X but along the vertical axis. Combined with Position X, these two knobs allow navigation through the full 2D fractal field. At default center values, the pattern is symmetric about the screen center. Detuning both positions from center reveals asymmetric regions of the tiling where the dragon curve boundary passes through different phases of its self-similar structure.

---

#### Knob 5 — Iteration
| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 9 |

Controls the depth of XOR folding in the hash computation. The Iteration register's upper three bits select a shift distance from 1 to 8, determining how many spatial octaves contribute to the fractal pattern. At the minimum setting (shift=1), the pattern is a simple diagonal checkerboard — only adjacent bits interfere. Each additional iteration brings a coarser spatial scale into the fold, deepening the boundary complexity. By shift 4–5, the characteristic dragon curve silhouette emerges clearly, with recursive zigzag edges separating foreground from background. At maximum depth (shift=8), the pattern incorporates the broadest spatial structure, producing the finest fractal detail at the cost of visual density — the foreground/background ratio approaches 50/50 as more scales contribute equally to the pattern decision.

---

#### Knob 6 — Line Width
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

Adjusts the apparent thickness of the fractal boundary by controlling how many hash-derived bits participate in the pattern test. At the narrowest setting, only the basic two-bit XOR pattern determines foreground membership, producing thin, sharply defined fractal edges. Increasing Line Width progressively includes adjacent hash bits in the pattern decision, broadening the transition zone between foreground and background regions. At wide settings, the fractal boundary thickens into bold graphic strokes, and the self-similar detail is smoothed into broader regions of solid color. This control interacts with Iteration — high iteration with narrow width produces the finest filigree, while low iteration with wide width produces bold geometric blocks.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Fill** | Off | On |
| **8 — Color Cycle** | Off | On |
| **9 — Animate** | Off | On |
| **10 — Mirror** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure distinct aspects of the fractal engine's output. Fill (7) controls whether the interior of the fractal regions is rendered as solid or hollow. Color Cycle (8) determines whether the UV chrominance channels derive from the hash bits — producing a spatially-varying color field — or remain at neutral gray for monochrome output. Animate (9) advances the frame counter on each vertical sync, causing the hash seed to shift and the pattern to evolve over time. Mirror (10) XORs an additional hash bit into the pattern decision, breaking the bilateral symmetry of the standard dragon fold and producing denser, more chaotic tilings. Bypass (11) routes the input signal directly to the output, skipping all fractal generation. These toggles interact multiplicatively — enabling all four active modes simultaneously produces animated, colored, asymmetric, filled fractal fields with maximum visual complexity.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls the luminance intensity of foreground (pattern=1) pixels. At 100%, foreground pixels are rendered at full white (Y=1023); at 0%, they dim to black, effectively erasing the pattern. The background (pattern=0) is always rendered at a fixed dark level (Y=64). At the default 75% setting, the contrast between foreground and background is strong but not clipped — suitable for both standalone display and downstream processing. Reducing Brightness below 50% produces a subtler pattern that can be overlaid on other video signals without overwhelming them. When Color Cycle is active, Brightness affects only the Y channel — the chromatic content from the hash bits is independent, so reducing Brightness desaturates the pattern toward dark color rather than gray.

---

## Guided Exercises

These exercises explore the dragon fractal from simple static geometry through chromatic animation to complex mirrored compositions, progressively engaging more of the parameter space.

### Exercise 1: Fractal Depth Discovery

<img src={dragon_exercise1_result} alt="Fractal Depth Discovery result"/>
*Fractal Depth Discovery — simulated result across source images.*
**Objective**: Explore how the Iteration parameter transforms a simple checkerboard into the classic dragon curve silhouette, understanding the relationship between XOR fold depth and fractal complexity.

1. **Start minimal**: Set Iteration to its lowest step (1). The screen shows a simple diagonal checkerboard — the result of a single-bit XOR fold with minimal spatial mixing.
2. **Increase iteration depth**: Slowly advance Iteration through each step. Watch the checkerboard edges begin to fracture and fold — the diagonal lines develop recursive zigzag indentations at each new depth level.
3. **Reach the dragon**: By step 8–10, the characteristic dragon curve boundary is clearly visible — a densely folded coastline separating foreground from background regions.
4. **Adjust Scale**: Zoom in to examine the fractal boundary at high magnification, then zoom out to see the overall tiling structure.
5. **Center the view**: Use Position X and Position Y to navigate to a region where the dragon curve boundary passes through the center of the screen.
6. **Compare with Fill**: Toggle Fill On and Off to see how the interior solid fill changes the visual character at different iteration depths.

**Key concepts**: XOR fold depth controls fractal complexity, each iteration brings a coarser spatial scale into the pattern, the dragon curve boundary emerges at moderate iteration counts, Scale reveals different structural levels of the hash

---

### Exercise 2: Chromatic Dragon Flight

<img src={dragon_exercise2_result} alt="Chromatic Dragon Flight result"/>
*Chromatic Dragon Flight — simulated result across source images.*
**Objective**: Combine color cycling with animation to produce a continuously evolving, spectrally rich fractal landscape that reveals the spatial structure of the hash function through color.

1. **Enable color**: Toggle Color Cycle On. The monochrome dragon pattern blooms into bands of hue — each region of the fractal field receives its color from the local hash bits.
2. **Start animation**: Toggle Animate On. The pattern begins crawling and morphing, the colors shifting as the frame counter modifies the hash seed.
3. **Set moderate iteration**: Set Iteration to step 6–8 for a pattern with clear fractal structure but enough spatial variation to show the color banding.
4. **Rotate slowly**: Sweep Rotation from 0° to 180°. The color bands rotate with the pattern, but because they derive from the hash bits (which depend on the absolute coordinate grid), the color distribution shifts relative to the fractal boundary as the pattern rotates.
5. **Adjust Brightness**: Pull Brightness to ~60% for a rich, saturated color field where the pattern is visible without being blindingly bright.
6. **Zoom to color detail**: Increase Scale to zoom into a region where the color transitions between hash cells are visible — the color changes abruptly at each 16-pixel block boundary, creating a stained-glass effect.

**Key concepts**: Hash-derived chrominance creates spatially varying color, animation shifts the hash seed over time producing morphing patterns, rotation reveals different cross-sections of the color field, Brightness controls intensity without affecting chrominance

---

### Exercise 3: Mirrored Kaleidoscope

<img src={dragon_exercise3_result} alt="Mirrored Kaleidoscope result"/>
*Mirrored Kaleidoscope — simulated result across source images.*
**Objective**: Use Mirror mode with animation and color cycling to produce a densely textured, asymmetric fractal field that evokes kaleidoscopic glass patterns.

1. **Enable Mirror**: Toggle Mirror On. The pattern immediately becomes denser and more chaotic as the third hash bit disrupts the bilateral symmetry of the standard dragon fold.
2. **Maximum iteration**: Set Iteration to step 14–16. At this depth, the mirrored pattern is extremely fine-grained, approaching a noise-like texture with fractal micro-structure.
3. **Enable everything**: Ensure Color Cycle, Animate, and Fill are all On. The screen becomes a churning field of colored fractal noise, continuously morphing.
4. **Navigate the field**: Use Position X and Position Y to pan through the infinite fractal plane. Different regions have subtly different local structure due to the coordinate-dependent hash.
5. **Reduce Brightness for ambience**: Pull Brightness to ~40% for a dark, gem-like appearance where colors glow against a near-black background.
6. **Zoom out**: Reduce Scale to see the large-scale tiling structure emerge from the noise — at sufficient zoom, the self-similar repetition of the hash pattern becomes visible as a meta-grid overlaying the fractal texture.

**Key concepts**: Mirror mode breaks symmetry via additional hash bit, high iteration + mirror produces noise-like fractal texture, Fill mode solidifies the interior regions, full parameter engagement creates maximum visual complexity

---


## Tips

- **Start with low iteration, then climb**: Begin at Iteration step 1 to understand the base diagonal grid, then increase one step at a time. Each step adds one level of fractal folding — watching the progression builds intuition for how XOR hashing generates self-similar structure.
- **Color Cycle reveals spatial structure**: The hash-derived chrominance is not decorative — it encodes the spatial position within the fractal tiling. Regions with similar color share similar hash-bit configurations, making Color Cycle a diagnostic tool for understanding the pattern's topology.
- **Rotation at 45° is a sweet spot**: Because the XOR fold creates primary structure along the diagonal, rotating by 45° aligns this structure with the horizontal, producing a dramatically different visual texture from the same parameters. Try comparing 0° and 45° at each iteration depth.
- **Mirror mode for density**: When the basic dragon pattern feels too sparse or regular, engage Mirror to add a third spatial frequency. The resulting pattern is always denser and more turbulent than the non-mirrored version, useful for textured backgrounds or noise-like overlays.
- **Brightness controls contrast ratio**: The foreground-to-background contrast is determined by the ratio between Brightness (foreground Y) and the fixed background level (Y=64). At Brightness=75%, the ratio is about 12:1. Reducing Brightness to 25% drops the ratio to about 4:1, producing a subtler pattern suitable for layering.
- **Animate + slow parameter sweeps**: With Animate On, slowly sweeping Iteration or Scale produces compound motion — the pattern morphs due to animation while simultaneously reconfiguring due to the parameter change. This creates organic, unpredictable visual evolution.
- **Use as a modulation source**: Dragon's high-contrast binary output makes it an excellent modulation source for downstream video effects. Route it into a keyer, multiplier, or feedback loop to impose fractal geometry onto any video signal.
- **Position for asymmetric compositions**: The default centered position produces a symmetric pattern. Offsetting Position X and Y breaks this symmetry, placing the densest fractal boundary off-center for more dynamic compositions.

---

## Glossary

| Term | Definition |
|------|------------|
| **Affine contraction** | A geometric transformation that combines scaling, rotation, and translation, used to define the self-similar pieces of an IFS fractal. |
| **BRAM** | Block RAM; dedicated memory within an FPGA. Dragon uses zero BRAMs — its entire fractal computation is combinational. |
| **DDS** | Direct Digital Synthesis; the technique of generating periodic signals using a phase accumulator, used here to advance the animation frame counter. |
| **Dragon curve** | A space-filling fractal discovered by John Heighway, constructed by repeated paper folding or equivalently by bit manipulation of integer step indices. |
| **Fractal dimension** | A measure of geometric complexity; the Heighway dragon has a boundary dimension of 2, meaning its edge is as complex as a filled region. |
| **Hash function** | A deterministic mapping from input values to pseudo-random output values; the XOR-fold position hash maps (x,y) coordinates to a binary pattern. |
| **Hausdorff dimension** | The mathematical formalization of fractal dimension, measuring how a set's detail scales with magnification. |
| **IFS** | Iterated Function System; a collection of contraction mappings whose repeated application converges to a fractal attractor. |
| **Self-similarity** | The property of looking identical at every scale of magnification, the defining characteristic of fractal geometry. |
| **Space-filling curve** | A continuous curve that passes through every point in a 2D region; the Heighway dragon fills a compact region of the plane. |
| **XOR fold** | The operation `hash ^= hash >> k`, which mixes bits separated by k positions to create self-similar interference patterns in the hash output. |
| **YUV** | A color space separating luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |

---
