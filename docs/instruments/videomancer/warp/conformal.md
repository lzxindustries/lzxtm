---
draft: true
sidebar_position: 54
slug: /instruments/videomancer/conformal
title: "Conformal"
image: /img/instruments/videomancer/conformal/conformal_hero.png
description: "Mathematics is full of functions that preserve angles — and in the complex plane, those functions transform images in ways that are surprising, beautifu..."
---

import conformal_hero from '/img/instruments/videomancer/conformal/conformal_hero.png';
import conformal_before_after from '/img/instruments/videomancer/conformal/conformal_before_after.png';
import conformal_control_panel from '/img/instruments/videomancer/conformal/conformal_control_panel.png';
import conformal_exercise1_result from '/img/instruments/videomancer/conformal/conformal_exercise1_result.png';
import conformal_exercise2_result from '/img/instruments/videomancer/conformal/conformal_exercise2_result.png';
import conformal_exercise3_result from '/img/instruments/videomancer/conformal/conformal_exercise3_result.png';

# Conformal

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={conformal_hero} alt="Conformal hero image"/>
*Conformal applying complex-plane inversion mapping to warp portrait geometry into spherical distortion patterns with grid overlay.*
<img src={conformal_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Conformal applied.*

---

## Overview

Mathematics is full of functions that preserve angles — and in the complex plane, those functions transform images in ways that are surprising, beautiful, and deeply connected to physics and engineering. Conformal takes the screen and treats every pixel as a complex number z = x + iy, applies one of four holomorphic functions, and reads the source video at the transformed coordinate. The result is a smooth, angle-preserving geometric distortion that turns straight lines into curves, circles into circles, and familiar images into something that feels like looking through strange glass.

The name comes directly from the mathematical term **conformal mapping** — a transformation that preserves local angles between curves. Four selectable maps are available: Inversion (1/z), which turns the plane inside-out through a circle; Joukowski (z + 1/z), the classic airfoil transform from fluid dynamics; Exponential, which converts Cartesian coordinates into a polar-like radial displacement; and Power (z²), which doubles angles and creates kaleidoscopic n-fold symmetry. A 256-entry reciprocal lookup table provides the division needed for the inversion-based maps, and a 2048-sample scanline buffer allows displaced horizontal reads.

At conservative Strength settings, Conformal produces gentle lens-like warps — a subtle fisheye or barrel distortion. At full strength with the grid overlay enabled, the underlying coordinate transformation becomes visible as a mesh of curved lines, revealing the mathematical structure directly.

---

## Background

### Complex Plane Mapping

Every pixel on the screen can be described by two numbers — its horizontal position x and its vertical position y. In complex analysis, those two numbers combine into a single complex number z = x + iy, and functions of z describe transformations of the entire plane. A **conformal map** is a function f(z) that is holomorphic (complex-differentiable) and whose derivative is nonzero — which guarantees that local angles are preserved. This is a powerful constraint: only a narrow family of functions qualify, and each one produces a geometrically elegant distortion.

Conformal maps appear throughout physics: electrostatic potential fields, fluid flow around obstacles, heat conduction in shaped regions, and the geometry of special relativity. In video synthesis, they give you access to an entire branch of mathematics through a pair of toggle switches.

### The Inversion Map (1/z)

The simplest nontrivial conformal map is the **Möbius inversion** w = 1/z. In Cartesian terms, if z = x + iy, then the real and imaginary parts of 1/z are Re(1/z) = x/(x² + y²) and Im(1/z) = −y/(x² + y²). The denominator x² + y² is the squared distance from the origin, so the map sends points near the origin to infinity and vice versa — the plane is turned inside-out through a circle. Circles and lines in the original image remain circles and lines (considered as circles through infinity). This is why inversion produces dramatic radial stretching centered on the mapping origin.

### The Joukowski Transform

The **Joukowski map** w = z + 1/z was developed in the early 20th century to study airfoil lift. It maps circles passing near the origin into shapes with a sharp trailing cusp — the profile of a wing cross-section. Applied to video, it creates a combined stretching and compression: regions near the mapping center are pushed outward (the 1/z term dominates), while distant regions are displaced roughly linearly (the z term dominates). The result is a distinctive "pinch and stretch" distortion.

### Reciprocal Lookup Tables

Computing 1/r² (where r² = x² + y²) in real-time FPGA logic without a hardware divider requires a lookup table. Conformal uses a 256-entry BRAM-based table where entry i holds round(2^18 / (i + 1)), clamped to 10 bits. The magnitude-squared value is reduced to an 8-bit index by selecting the most significant nonzero byte, giving a coarse but fast approximation. This is the same trade-off that early 3D graphics chips made — precision for speed, with visually acceptable results because small errors in a coordinate lookup just produce a slightly different warp.

### Power Maps and Angular Magnification

The **power map** w = z^n multiplies all angles around the origin by n. For n = 2, every 180° sector is compressed into 360°, creating a twofold reflection symmetry. For n = 3, a 120° sector fills the plane. Higher powers create kaleidoscope-like radial symmetries. The VHDL implements z² directly using Re(z²) = x² − y² and Im(z²) = 2xy, which requires only two multiplications and a subtraction — no lookup table.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Coordinate Pipeline ─────────────────────────────────────────
│   │
│   ├─ 1. Position Counters    (h_count, v_count from timing gen)
│   ├─ 2. Center & Scale       (v_dx = h - CenterX, v_dy = v - CenterY)
│   ├─ 3. Magnitude Squared    (v_dx² + v_dy² → reciprocal LUT index)
│   ├─ 4. Reciprocal Lookup    (256-entry BRAM → 10-bit 1/r²)
│   ├─ 5. Function Eval        (00: 1/z, 01: z+1/z, 10: exp, 11: z²)
│   ├─ 6. Strength Blend       (lerp identity ↔ warped coordinate)
│   ├─ 7. Abs Coords + Clamp/Tile (re-add center, boundary handling)
│   └─ 8. Grid Detect          (low bits of warped coords → grid lines)
│
├── Scanline Buffer ─────────────────────────────────────────────
│   │
│   ├─ Write: current pixel at h_count
│   └─ Read:  displaced pixel at out_x
│
├── Compose ─────────────────────────────────────────────────────
│   │
│   ├─ Grid overlay (white on chroma-neutral) if Grid=On & grid line
│   └─ Displaced pixel from scanline buffer otherwise
│
├── Mix (Interpolator ×3) ───────────────────────────────────────
│   │
│   └─ Crossfade: delayed dry ↔ composed wet per Y, U, V
│
├── Sync Delay ──────────────────────────────────────────────────
│   └─ 8-clock pipeline delay for hsync, vsync, field, Y, U, V
│
└── Bypass Mux ──────────────────────────────────────────────────
    └─ Select delayed original or mixed output
```

The heart of Conformal is the four-clock coordinate pipeline that transforms pixel positions into displaced read addresses. Stage 1 centers the coordinates around the user-defined origin; stage 2 computes the squared magnitude and looks up the reciprocal in BRAM; stage 3 evaluates one of four conformal functions using the reciprocal and centered coordinates; stage 4 blends the warped result with the identity mapping according to the Strength parameter, then clamps or tiles the output address. The scanline buffer stores the current input line and provides displaced horizontal reads — vertical displacement is limited to the current line because only a single-scanline buffer is used, so the v_out_y coordinate affects grid detection but the actual pixel read comes from the current row's displaced x position.

---

## Parameter Reference

<img src={conformal_control_panel} alt="Videomancer front panel with Conformal loaded"/>
*Videomancer's front panel with Conformal active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — CenterX
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the horizontal position of the mapping center — the complex-plane origin. At 0% the origin is at the left edge of the frame; at 50% it is centered; at 100% it is at the right edge. Moving the center shifts the entire distortion pattern, because all four conformal functions are defined relative to this point. For inversion (1/z), the center becomes the singularity where the image collapses to a point.

---

#### Knob 2 — CenterY
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the vertical position of the mapping center. Together with CenterX, this places the complex-plane origin anywhere on screen. The VHDL scales the pot value by half (shift_right by 1) to account for the 2:1 horizontal-to-vertical pixel ratio in HD video. Placing the center near an edge pushes the singularity partially off-screen, which can produce dramatic sweeping curves that arc across the frame.

---

#### Knob 3 — Scale
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the scale (magnification) of the coordinate system before the conformal function is evaluated. At low values the effective zoom is tight, concentrating the entire warp into a small region around the center. At high values the zoom is wide, spreading the transformation across the full frame. Scale interacts strongly with each mapping function: in inversion mode, low scale creates a tight vortex; in Joukowski mode, it controls how far the airfoil stretching extends.

---

#### Knob 4 — Power N
| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 2 |

Selects the exponent for the Power map (mode 11). The steps_8 control mode quantizes the knob into eight discrete positions corresponding to exponents 2 through 8. Higher exponents create more angular repetitions — n = 2 gives twofold symmetry, n = 4 gives fourfold, and so on. Note that in the current VHDL implementation the power map always computes z² regardless of this register; the parameter is reserved for future extension to higher exponents via iterated squaring.

---

#### Knob 5 — Rotate
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |
| Suffix | deg |

Applies a pre-rotation to the centered coordinates before the conformal function is evaluated. The polar_degs_360 control mode maps the full knob range to 0–360°. Rotation before a conformal map rotates the output pattern; for inversion, it has no visible effect (1/z is rotationally symmetric), but for Joukowski and Power maps it rotates the axis of symmetry, changing which part of the image receives the strongest distortion.

---

#### Knob 6 — Strengt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Blends between the identity mapping (0%) and the fully warped coordinate (100%). The VHDL computes a linear interpolation: output = identity + (warped − identity) × Strength / 1024. At 0% the image is untransformed; at intermediate values you get a partial warp that can look like a gentle lens distortion; at 100% the full conformal function is applied. This is useful for dialing in subtle effects or animating the warp intensity via external CV.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — MapSelA** | 0 | 1 |
| **8 — MapSelB** | 0 | 1 |
| **9 — Tile** | Clamp | Tile |
| **10 — Grid** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a 2-bit map selector: MapSelA is bit 0, MapSelB is bit 1. The four combinations select the conformal function: **00** = Inversion (1/z), **01** = Joukowski (z + 1/z), **10** = Exponential (radial displacement), **11** = Power (z²). Toggle 9 switches the boundary handling between Clamp (out-of-bounds coordinates are clamped to the nearest edge pixel) and Tile (coordinates wrap modularly, creating repeating tiled copies of the warped image). Toggle 10 enables a white grid overlay on the warped coordinate mesh, making the structure of the mapping visible. Toggle 11 bypasses all processing and passes the input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Dry/wet crossfade between the original input video and the conformally warped output. At 0% the output is entirely the original (dry) signal. At 100% the output is entirely the warped (wet) signal. Intermediate positions blend the two, which creates a ghostly double-exposure effect where the warped image is superimposed on the original — useful for subtle distortion effects or for previewing the warp intensity before committing to full wet.

---

## Guided Exercises

These exercises explore the four conformal mapping functions and their interactions with the Strength, Tile, and Grid controls.

### Exercise 1: Inversion Through Center

<img src={conformal_exercise1_result} alt="Inversion Through Center result"/>
*Inversion Through Center — simulated result across source images.*
**Source**: Feed a high-contrast graphic or text source — white text on a black background works well because straight edges make the inversion visible.

**Objective**: Demonstrate the 1/z inversion map, which turns the plane inside-out through the center point.

1. Set both map toggles to 0 (MapSelA = 0, MapSelB = 0) to select Inversion mode.
2. Set CenterX and CenterY to 50% to place the singularity at the center of the frame.
3. Bring Strength to 100% for full warp.
4. Enable Grid overlay to see how straight lines become circles and circles pass through the origin.
5. Slowly sweep CenterX left and right — watch the inversion singularity move across the frame.
6. Toggle Tile on to see the inside-out image tile at the boundaries.

**Key concepts**: Inversion sends points near the origin to infinity and vice versa. Text or lines that cross the center appear to flip radially. The grid overlay shows that the rectilinear grid maps to a family of circles passing through the origin.

---

### Exercise 2: Joukowski Airfoil Stretch

<img src={conformal_exercise2_result} alt="Joukowski Airfoil Stretch result"/>
*Joukowski Airfoil Stretch — simulated result across source images.*
**Source**: Feed a live camera or a colorful, organic video source with curves and gradients.

**Objective**: Explore the Joukowski map, which creates a distinctive pinch-and-stretch distortion resembling fluid dynamics.

1. Set MapSelA = 1, MapSelB = 0 (toggle 7 On, toggle 8 Off) for Joukowski mode.
2. Center the origin (CenterX = 50%, CenterY = 50%).
3. Set Strength to 75% and observe the combined z + 1/z distortion.
4. Sweep Scale from low to high — at low scale the airfoil cusp is tight; at high scale it stretches across the frame.
5. Rotate using Pot 5 to change the axis of the Joukowski distortion. At 0° the cusp points rightward; at 90° it points upward.
6. Reduce Mix to 50% to blend the warped result with the original, creating a lens-flare-like overlay.

**Key concepts**: Joukowski combines the identity (z) with the inversion (1/z). Close to the origin, the 1/z term dominates and creates strong stretching. Far from the origin, the z term dominates and the image is nearly undistorted. The transition region creates the airfoil-like cusp.

---

### Exercise 3: Power Map Kaleidoscope with Tiling

<img src={conformal_exercise3_result} alt="Power Map Kaleidoscope with Tiling result"/>
*Power Map Kaleidoscope with Tiling — simulated result across source images.*
**Source**: Feed a symmetrical pattern or mandala-like video source — or any video with strong central features.

**Objective**: Use the Power map (z²) with Tile mode to create a kaleidoscopic, fractal-like tiling pattern.

1. Set both map toggles to 1 (MapSelA = 1, MapSelB = 1) for Power mode.
2. Center the origin.
3. Set Strength to 100%.
4. Enable Tile (toggle 9) to wrap out-of-bounds coordinates, creating repeating tiles.
5. Enable Grid (toggle 10) to see the angular doubling — the grid lines radiate from the origin with doubled angular spacing.
6. Slowly sweep CenterX and CenterY off-center — the tiling pattern shifts and creates new symmetries.
7. Try reducing Strength to 50% to blend partial angular doubling with the original, creating a mild kaleidoscopic shimmer.

**Key concepts**: The z² power map doubles all angles around the origin: a 180° sector fills the full 360° plane. With tiling enabled, coordinates that leave the frame wrap back, creating a repeating tile field. The grid overlay shows the doubled angular periodicity clearly.

---


## Tips

- **Start centered:** Place CenterX and CenterY at 50% when exploring a new map function, so the distortion is symmetrical and predictable. Move the center off-screen only after you understand the map's behavior.
- **Use Grid to learn:** Enable the Grid overlay when switching between map functions. The grid reveals the mathematical structure of each mapping far more clearly than processed video alone.
- **Tile for recursion:** Enable Tile mode with Inversion or Power maps to create fractal-like repeating patterns. The wrapping fills the entire frame with transformed copies of the source.
- **Strength for subtlety:** Low Strength values (10–30%) applied to the Joukowski map produce gentle lens-like barrel distortions that can simulate curved glass or underwater refraction.
- **Animate CenterX/CenterY:** Patching slow LFOs to Center X and Center Y with the Inversion map creates a wandering singularity that sweeps across the frame, pulling the image into continuously shifting vortex patterns.
- **Combine with feedback:** Routing the output of Conformal back into its own input (via an external mixer or feedback loop) amplifies the nonlinear distortion, creating increasingly complex and chaotic warp patterns with each pass.
- **Joukowski for flow:** The Joukowski map naturally evokes fluid dynamics. Try it on smoke, water, or abstract flowing video to reinforce the aesthetic connection to aerodynamic streamlines.
- **Mix for double exposure:** Setting Mix to 50% creates a transparent overlay of the warped image on the original — useful as a creative double-exposure technique rather than just a utility fade.

---
