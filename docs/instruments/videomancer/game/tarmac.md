---
draft: true
sidebar_position: 254
slug: /instruments/videomancer/tarmac
title: "Tarmac"
image: /img/instruments/videomancer/tarmac/tarmac_hero.png
description: "The Super Nintendo's Mode 7 background layer was a hardware trick that changed everything."
---

import tarmac_before_after from '/img/instruments/videomancer/tarmac/tarmac_before_after.png';
import tarmac_control_panel from '/img/instruments/videomancer/tarmac/tarmac_control_panel.png';
import tarmac_exercise1_result from '/img/instruments/videomancer/tarmac/tarmac_exercise1_result.png';
import tarmac_exercise2_result from '/img/instruments/videomancer/tarmac/tarmac_exercise2_result.png';
import tarmac_exercise3_result from '/img/instruments/videomancer/tarmac/tarmac_exercise3_result.png';
import tarmac_hero from '/img/instruments/videomancer/tarmac/tarmac_hero.png';
import tarmac_source1_kodim15 from '/img/instruments/videomancer/tarmac/tarmac_source1_kodim15.png';
import tarmac_source2_kodim03 from '/img/instruments/videomancer/tarmac/tarmac_source2_kodim03.png';
import tarmac_source3_kodim15_bw from '/img/instruments/videomancer/tarmac/tarmac_source3_kodim15_bw.png';

# Tarmac

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={tarmac_hero} alt="Tarmac hero image"/>
*Tarmac applying SNES Mode 7 affine transformation with per-scanline perspective to create a pseudo-3D ground plane from a tiled video texture.*
<img src={tarmac_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Tarmac applied.*

---

## Overview

The Super Nintendo's Mode 7 background layer was a hardware trick that changed everything. By applying a per-scanline affine transformation — rotation, scaling, and translation — to a flat texture map, it simulated a 3D ground plane stretching toward a vanishing point on the horizon. F-Zero, Mario Kart, Pilotwings — an entire generation of games was built on this single technique. Tarmac brings that same transformation to live video.

Tarmac captures a 64×64 downsampled tile from the input video and replays it through an affine matrix with per-scanline perspective scaling. Below the horizon line, the tile stretches toward the viewer with foreshortening that increases with distance. Above the horizon, an optional sky gradient fills the frame. The name evokes both the road surface seen in racing games and the tarmac runway stretching to the vanishing point — the quintessential Mode 7 image.

At conservative settings, Tarmac creates gentle perspective warps and subtle texture scrolling. At extreme settings, the ground plane spins, zooms, and scrolls simultaneously while the tile repeats in a dizzying infinite floor. Combining rotation with scroll offset and scale produces hypnotic, ever-changing geometric kaleidoscopes that transform any source material into a retro-futuristic landscape.

---

## Background

### The SNES Mode 7 Hardware

The Super Nintendo's Picture Processing Unit (PPU) included a special background mode called Mode 7 that could apply a 2×2 affine transformation matrix to an entire background layer. The matrix supported rotation, scaling, and shearing — everything needed to simulate a textured ground plane receding into the distance. The trick was computing different matrix coefficients for each scanline: near the bottom of the screen (close to the viewer), the texture was large and detailed; near the horizon, it compressed to a vanishing point. This per-scanline variation created convincing pseudo-3D perspective from a purely 2D texture lookup.

### Affine Transformation Matrices

An affine transformation maps source coordinates (u, v) to screen coordinates (x, y) through a 2×2 matrix plus translation:

    u = A · (x − cx) + B · (y − cy) + sx
    v = C · (x − cx) + D · (y − cy) + sy

For pure rotation by angle θ with uniform scale s: A = cos(θ)·s, B = sin(θ)·s, C = −sin(θ)·s, D = cos(θ)·s. For Mode 7 perspective, s varies per scanline — small near the horizon (distant), large at the bottom of the screen (close). This progressive scaling is what creates the illusion of depth.

### Tile Buffering and Texture Mapping

Tarmac captures the input video into a 64×64×30-bit tile buffer stored in FPGA block RAM. The downsampling takes every ~30th pixel horizontally (~1920/64) and every ~16th line vertically (~1080/64) to fill the tile. This captured tile becomes the "texture" that the Mode 7 transform maps onto the ground plane. Because the tile is small (64×64) relative to the output (1920×1080), the affine transform magnifies it substantially, creating the characteristic blocky, pixel-art aesthetic of the SNES era. In repeat mode, the tile seamlessly tiles across the infinite ground plane.

### Quarter-Wave Sine LUT

Rotation requires sine and cosine values. Rather than implementing CORDIC or polynomial approximation, Tarmac stores a 64-entry quarter-wave sine lookup table. Full 360° coverage is achieved through quadrant mirroring and sign flipping — the same technique used in the original SNES PPU. This approach trades 64 words of storage for a rotation computation that completes in a single clock cycle.

### Per-Pixel Incremental Walk

After computing the starting texture coordinates for the left edge of each scanline using the full affine equation, Tarmac advances across the row by simply adding the matrix column coefficients (A and C) to the accumulators for each new pixel. This reduces the per-pixel cost from four multiplications to two additions — the same optimization that made Mode 7 feasible in 1990s hardware running at 3.58 MHz. The per-pixel walk adds M7A to the horizontal accumulator and M7C to the vertical accumulator, producing correct affine mapping for the entire row from a single row-init multiplication.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Tile Capture ─────────────────────────────────────────────
│   │
│   └─ Downsample input to 64×64×30-bit BRAM tile buffer
│      (horizontal skip ≈ 30, vertical skip ≈ 16)
│
├── Mode 7 Render Engine ─────────────────────────────────────
│   │
│   ├─ 1. DDS Phase Accumulators (rotation angle, scale oscillation)
│   ├─ 2. Sine/Cosine LUT Lookup (64-entry quarter-wave)
│   ├─ 3. Matrix Coefficient Compute (A=cos·s, B=sin·s, C=−sin·s, D=cos·s)
│   ├─ 4. Per-Scanline Row Init (starting tx, ty from center offset)
│   ├─ 5. Per-Pixel Accumulator Walk (tx += A, ty += C)
│   ├─ 6. Tile Address Compute (wrap mod 64 or clamp 0–63)
│   ├─ 7. Tile Buffer Read (30-bit packed YUV from BRAM)
│   │
│   ├─ Sky Gradient (optional: above horizon line)
│   └─ Grid Overlay (optional: XOR at tile boundaries)
│
├── Invert (optional) ────────────────────────────────────────
│
├── Mix ──────────────────────────────────────────────────────
│   └─ Interpolator: dry (original) ↔ wet (Mode 7 render)
│
├── Sync Signals ─────────────────────────────────────────────
│   └─ 8-clock delay shift registers (hsync, vsync, field)
│
└── Bypass ───────────────────────────────────────────────────
    └─ Select original or processed signal
```

Two important interactions define Tarmac's character. First, the **tile capture and render phases overlap**: the tile buffer stores data from the current frame while simultaneously being read by the affine engine. Since the FPGA runs at pixel clock speed, reads and writes interleave naturally — write during the active video region of the captured tile area, read during the render pass for the output. Second, the **per-scanline perspective variation** is what separates Tarmac from a simple 2D rotation: by scaling the matrix coefficients differently for each horizontal line, distant parts of the ground plane compress toward the horizon while near parts expand, creating the iconic Mode 7 depth illusion.

---

## Parameter Reference

<img src={tarmac_control_panel} alt="Videomancer front panel with Tarmac loaded"/>
*Videomancer's front panel with Tarmac active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Rot Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the vertical position of the horizon line. At 0%, the horizon sits at the top of the frame and the entire output is ground plane. As the control increases, the horizon drops, allocating more of the upper frame to sky (if enabled) and compressing the ground plane into fewer scanlines at the bottom. The horizon position also defines the vanishing point where the converging perspective lines meet.

---

#### Knob 2 — Zoom Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of the perspective foreshortening. At low values, the ground plane appears relatively flat with minimal depth illusion — the tile texture maintains roughly uniform scale across the frame. As you increase tilt, the scale differential between near and far scanlines increases dramatically, creating steeper perspective. At maximum, the ground rushes from near at the bottom of the frame to a tight vanishing point at the horizon.

---

#### Knob 3 — Perspective
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Horizontal scroll offset for the ground plane texture. At 50%, the texture is centered. Sweeping this control slides the texture left and right across the ground plane. Combined with rotation, scroll creates the illusion of driving or flying over the texture surface — the same effect as directional movement in F-Zero or lateral turning in Mario Kart.

---

#### Knob 4 — Base Scale
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Vertical scroll offset for the ground plane texture. Works identically to Scroll X but in the forward and backward direction of the ground plane. Increasing Scroll Y appears to move the viewpoint forward over the texture surface. Combined with Scroll X, you can navigate freely across the tiled pattern in two dimensions.

---

#### Knob 5 — Zoom Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Overall zoom level of the ground plane texture. At 50%, the texture displays at 1:1 relative to the tile capture resolution. Turning counter-clockwise zooms in, magnifying the 64×64 tile and revealing individual pixel blocks as large colored rectangles. Turning clockwise zooms out, showing more repetitions of the tile (in repeat mode) or more of the clamped edge (in clamp mode). Scale interacts multiplicatively with perspective — at high zoom combined with high tilt, the near-to-far transition is extreme.

---

#### Knob 6 — Center Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Rotation angle of the ground plane, mapped through a 64-entry sine lookup table to produce continuous 360° rotation. At 0°, the tile aligns with the screen axes. The rotation pivots around the center point defined by the horizon position and screen center. Combined with perspective, rotation creates the distinctive Mode 7 spinning ground plane familiar from SNES games.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Rot Dir** | CW | CCW |
| **8 — Shear** | Off | On |
| **9 — Wrap Mode** | Wrap | Clamp |
| **10 — Persp Hold** | Center | Bottom |
| **11 — Bypass** | Off | On |

The five toggle switches control rendering modes that change the visual character of the output. Tile mode determines whether the 64×64 texture wraps infinitely or stops at its edges. Grid adds structural reference lines at tile boundaries. Sky fills the area above the horizon with a synthetic gradient. Invert reverses the luminance of the entire rendered output. Bypass provides instant A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 100 |

Crossfade between the dry (original) and wet (Mode 7 rendered) signals. At 0%, the output is pure input video. At 100%, the output is pure Mode 7 ground plane with optional sky. Intermediate values blend the two proportionally, which can create ghostly overlay effects where the original video shows through the perspective-transformed texture.

---

## Guided Exercises

These exercises build from basic perspective rendering to complex animated ground plane compositions, progressively engaging more of Tarmac's Mode 7 controls.

### Exercise 1: First Ground Plane

<img src={tarmac_exercise1_result} alt="First Ground Plane result"/>
*First Ground Plane — simulated result across source images.*
**Source**: A still image or camera feed with strong texture — brickwork, fabric pattern, tile floor, or printed text.

**Objective**: Create the basic Mode 7 perspective ground plane and understand the horizon, tilt, and scale interaction.

1. **Set the horizon**: Turn Horizon to ~25%. The ground plane fills the lower three-quarters of the frame.
2. **Add perspective**: Increase Tilt to ~60%. Watch the perspective deepen — the texture now recedes convincingly from near to far.
3. **Enable tiling**: Set Tile to Repeat so the texture tiles across the infinite floor.
4. **Adjust zoom**: Slowly sweep Scale. Note how higher scale reveals more tile repetitions while lower scale magnifies the pixel structure of the 64×64 capture.
5. **Enable Grid**: Turn Grid On to visualize how the grid lines converge toward the horizon — a structural reference for the perspective mapping.

**Key concepts**: Horizon position sets the vanishing point, tilt controls perspective depth, scale controls magnification, repeat mode enables infinite floor, grid overlay reveals the transform geometry

---

### Exercise 2: Spinning Floor

<img src={tarmac_exercise2_result} alt="Spinning Floor result"/>
*Spinning Floor — simulated result across source images.*
**Source**: A colorful pattern, logo, or high-contrast graphic with recognizable orientation.

**Objective**: Add rotation to the ground plane for the classic Mode 7 spinning effect.

1. **Start with the ground plane** from Exercise 1 (Horizon ~25%, Tilt ~60%, Repeat mode).
2. **Engage rotation**: Slowly sweep Rotation through its full range. Watch the ground plane rotate around the center point.
3. **Observe at 45°**: Stop at 45° and observe how the grid lines now run diagonally across the perspective plane.
4. **Try different scales**: Adjust Scale while rotated — small scale creates a zoomed view of a single tile; large scale shows many repeating tiles spiraling away toward the horizon.
5. **Complete the scene**: Enable Sky to see the full ground-plus-sky composition while rotating.

**Key concepts**: Rotation pivots around the center point defined by the horizon, affine transforms preserve straight lines and parallel relationships, rotation combined with perspective creates the F-Zero racing effect

---

### Exercise 3: Racing Game Composite

<img src={tarmac_exercise3_result} alt="Racing Game Composite result"/>
*Racing Game Composite — simulated result across source images.*
**Source**: A camera feed of a road, floor tiles, or any directional texture.

**Objective**: Combine scrolling and rotation to simulate forward movement across the ground plane, then overlay it on the original video.

1. **Set up the ground plane**: Horizon ~30%, Tilt ~70%, Repeat, Sky On.
2. **Scroll forward**: Slowly increase Scroll Y while Rotation is at 0°. The texture appears to scroll toward you — forward movement over the ground.
3. **Add steering**: While Scroll Y is advancing, add slight Rotation. The floor pivots as if cornering on a racetrack.
4. **Lateral movement**: Adjust Scroll X simultaneously to create turning combined with forward motion.
5. **Try Clamp mode**: Switch Tile to Clamp to see how the edge stretching looks for a single-texture flyover without tiling.
6. **Transparent overlay**: Lower Mix to ~50% to overlay the Mode 7 ground on top of the original video as a semi-transparent layer.

**Key concepts**: Combining scroll axes simulates free navigation over the texture, clamp mode creates single-texture flyovers, mix enables transparent overlay compositing of the ground plane onto the source video

---


## Tips

- **Start with Repeat mode**: Infinite tiling is the classic Mode 7 look and reveals the affine transform's full character. Switch to Clamp only when you want the single-tile flyover aesthetic with stretched borders.
- **Use Grid for calibration**: The grid overlay shows exactly how the affine transform distorts space. It is invaluable for setting up perspective depth and understanding how rotation warps the coordinate system before committing to a final texture.
- **Combine Scroll X and Scroll Y for navigation**: Sweeping both scroll controls simultaneously simulates flying over the ground plane. Add slight rotation for cornering and you have the basic F-Zero control scheme.
- **Low tilt for planimetric views**: Near-zero tilt produces a flat top-down view of the tile, similar to a 2D rotation without perspective. This is useful for kaleidoscope-like effects with repeated tiles.
- **High tilt + low horizon for drama**: Pushing tilt toward maximum while setting the horizon low creates extreme foreshortening — the texture rushes from the bottom of the frame to a tight vanishing point.
- **Mix for overlay compositing**: Setting Mix to 50% blends the Mode 7 ground plane transparently over the original video, creating surreal double-exposure effects where the source shows through the perspective-mapped floor.
- **Scale and tile capture interact**: The tile is captured at 64×64 regardless of scale. Zooming out reveals the blocky pixel structure of the low-resolution tile, which is part of the retro aesthetic and a feature, not a bug.
- **Feedback loops**: Routing the output back to the input creates recursive tile captures — each frame's ground plane becomes the next frame's tile texture, producing self-referencing fractal floor patterns that evolve over time.

---

## Glossary

| Term | Definition |
|------|------------|
| **Affine Transform** | A geometric transformation preserving parallel lines, defined by a 2×2 matrix plus translation; encompasses rotation, scaling, shearing, and translation. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator and using the result to index a lookup table. |
| **Foreshortening** | Perspective compression where objects farther from the viewer appear shorter, narrower, and closer together. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Mode 7** | A background rendering mode in the Super Nintendo PPU that applies per-scanline affine transformations to a tiled texture for pseudo-3D ground plane effects. |
| **Per-Scanline Perspective** | Varying the affine matrix scaling coefficient for each horizontal line to simulate depth — the central technique behind Mode 7's 3D illusion. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **Quarter-Wave Sine LUT** | A lookup table storing one quarter of a sine wave; full 360° sine and cosine coverage is achieved through quadrant mirroring and sign flipping. |
| **Tile Buffer** | A small (64×64 pixels, 30-bit packed YUV) memory region storing a downsampled snapshot of the input video, used as the texture source for Mode 7 rendering. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
