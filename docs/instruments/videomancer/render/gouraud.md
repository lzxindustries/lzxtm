---
draft: true
sidebar_position: 129
slug: /instruments/videomancer/gouraud
title: "Gouraud"
image: /img/instruments/videomancer/gouraud/gouraud_hero.png
description: "Every era of computer graphics has a defining look, and for the early 3D hardware generation — PlayStation, Saturn, N64 — that look was Gouraud shading."
---

import gouraud_hero from '/img/instruments/videomancer/gouraud/gouraud_hero.png';
import gouraud_animation from '/img/instruments/videomancer/gouraud/gouraud_animation.gif';
import gouraud_control_panel from '/img/instruments/videomancer/gouraud/gouraud_control_panel.png';
import gouraud_exercise1_result from '/img/instruments/videomancer/gouraud/gouraud_exercise1_result.gif';
import gouraud_exercise2_result from '/img/instruments/videomancer/gouraud/gouraud_exercise2_result.gif';
import gouraud_exercise3_result from '/img/instruments/videomancer/gouraud/gouraud_exercise3_result.gif';

# Gouraud

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={gouraud_hero} alt="Gouraud hero image"/>
*Gouraud rendering smooth-shaded morphing triangles with DDS-animated vertex color cycling across a fan of rasterized faces.*
<img src={gouraud_animation} alt="Gouraud animated output"/>
*Gouraud output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Every era of computer graphics has a defining look, and for the early 3D hardware generation — PlayStation, Saturn, N64 — that look was Gouraud shading. Flat polygons with colors that bled smoothly from vertex to vertex, moving through space with a fluidity that suggested depth even when triangle counts were low. Gouraud recreates that aesthetic as a real-time video synthesis program, rendering an animated field of morphing triangles with per-vertex color interpolation directly in the FPGA fabric.

The program maintains eight vertices animated by **DDS (Direct Digital Synthesis)** oscillators tracing Lissajous orbits around screen center. Pairs of adjacent vertices form triangles in a fan arrangement, and for each pixel the engine evaluates edge functions to determine which triangle (if any) covers it. Vertex colors are then interpolated across the face — smooth gradients in Gouraud mode, solid fills in flat mode. The name honors Henri Gouraud, whose 1971 paper introduced continuous shading to computer graphics. The program is both a homage and a practical synthesis tool: the animated triangles produce endlessly evolving color fields suitable for layering, keying, and modulation.

At conservative settings — two triangles, slow morph, moderate spread — Gouraud produces gentle gradient washes that drift across the screen like stained glass panels. At extreme settings — four triangles, high spread, maximum color speed, wireframe enabled — it generates a hyperkinetic mesh of overlapping geometric forms with rapidly cycling hues, recalling the polygon-shattered aesthetic of early 3D demos.

---

## Quick Start

1. **Bit overlap matters**: Switching to flat shading also changes the triangle count to 4. This is a hardware design choice, not a bug — plan compositions knowing that flat mode always uses 4 triangles.
2. **Prime offsets create uniqueness**: Each vertex's DDS uses a different prime-number frequency offset, so even at uniform morph speed, no two vertices trace the same path. This is why the patterns never exactly repeat.
3. **Wireframe as overlay**: Combining wireframe mode with video modulation turns Gouraud into a geometric overlay generator — thin colored lines that track and deform over the video signal.

---

## Background

### What Is Gouraud Shading?

In 1971, Henri Gouraud published a method for making faceted 3D surfaces appear smooth. Instead of filling each polygon with a single flat color, his algorithm computes a color at each vertex and **linearly interpolates** across the face. The result is a continuous gradient that disguises the polygon boundaries. This technique became the default shading model for an entire generation of 3D hardware because it requires only simple arithmetic per pixel — no per-pixel lighting, no texture lookups, just weighted averages of vertex colors. Gouraud implements this interpolation directly: when smooth shading is selected, each pixel's color is the average of the three vertex colors of the triangle that covers it.

### What Is Edge-Function Rasterization?

Determining whether a pixel lies inside a triangle is the core problem of rasterization. The **edge function** method — attributed to Juan Pineda (1988) — evaluates a signed area for each edge. For a triangle with vertices A, B, C, the edge function for edge AB at point P is: $e_{AB}(P) = (B_x - A_x)(P_y - A_y) - (B_y - A_y)(P_x - A_x)$. If all three edge functions share the same sign, point P is inside the triangle. Gouraud evaluates this test for up to four triangles per pixel, accepting the first hit. The same edge function values also detect pixels near triangle edges (within a threshold of 4096), enabling the wireframe overlay.

### What Is Direct Digital Synthesis?

**DDS** is a technique for generating periodic waveforms using a phase accumulator and a lookup table. A fixed increment is added to a phase register each clock cycle (or each frame, in Gouraud's case). The accumulated phase indexes a waveform function — here a piecewise triangle wave approximating a sine — to produce smooth, continuous motion. By assigning each vertex a unique prime-number frequency offset, the eight vertices trace independent Lissajous figures that never exactly repeat, producing the constantly evolving geometric compositions that characterize the program.

### Fan Arrangement and Triangle Topology

Gouraud arranges its triangles in a **fan** topology. Vertex 0 sits at screen center (960, 540) and serves as the anchor for every triangle. Triangle 0 connects center → vertex 1 → vertex 2; triangle 1 connects center → vertex 3 → vertex 4; and so on. This means the triangles always radiate outward from the middle of the screen, creating compositions reminiscent of pinwheel patterns or kaleidoscopic symmetry. Because the outer vertices orbit independently, the triangles stretch, overlap, and fold through each other in complex patterns.


---

## Signal Flow

Per-Frame → Per-Pixel Pipeline → Sync Signals → Bypass

```
Synthesis Engine (no video input required)
│
├── Per-Frame (VBlank) ─────────────────────────────────────────
│   │
│   ├─ 1. DDS Phase Accumulate    (8 vertex X/Y phases + 8 color phases)
│   ├─ 2. Triangle Wave Lookup    (phase → amplitude via piecewise function)
│   └─ 3. Vertex Position/Color   (spread-scaled Lissajous orbit + color cycle)
│
├── Per-Pixel Pipeline ─────────────────────────────────────────
│   │
│   ├─ 1. Edge Function Setup     (triangle fan: center + vert[2i+1] + vert[2i+2])
│   ├─ 2. Edge Evaluation         (hit test for up to 4 triangles, first hit wins)
│   ├─ 3. Color Interpolation     (Gouraud: 3-vertex average / Flat: vertex 1 color)
│   ├─ 4. Output Compose          (brightness scale, chroma scale, video mod, wireframe)
│   └─ 5. Mix                     (3× interpolator_u, wet/dry crossfade)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay alignment (pass-through)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select processed or delayed input signal
```

Two distinct timing domains operate here. The vertex animation runs once per frame at vsync — all eight vertex positions and colors are updated simultaneously before the next frame scan begins. The pixel pipeline runs continuously at pixel rate, evaluating edge functions and interpolating colors for every pixel in every active line. The vertex positions are effectively frozen during each frame scan, so the triangles appear as crisp, static shapes within any single frame and move smoothly between frames.

A notable hardware detail: the VHDL `s_tri_count` and `s_flat_mode` signals both read from `registers_in(6)` with overlapping bit positions. Bit 1 controls both the upper bit of the triangle count selector and the flat shading flag simultaneously. In practice, this means the triangle count is either 2 (both bits "00") or 4 (any other combination), and flat mode activates whenever bit 1 is set — which also forces the triangle count to 4.

---

## Parameter Reference

<img src={gouraud_control_panel} alt="Videomancer front panel with Gouraud loaded"/>
*Videomancer's front panel with Gouraud active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Morph Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the rate at which vertex positions evolve. The morph speed value is added to each vertex's X and Y phase accumulators every frame, on top of the per-vertex prime frequency offsets. At zero, the vertices freeze in place and the triangle pattern becomes static. As the control increases, the Lissajous orbits speed up and the geometric composition transforms more rapidly. Because each vertex has a unique prime offset, even small changes in morph speed produce complex phase relationships between vertices.

---

#### Knob 2 — Color Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the rate at which vertex colors cycle. Each vertex's color phase accumulator advances by this value plus a per-vertex offset (multiples of 8192) every frame. The color phases drive a triangle wave function that produces smoothly cycling luminance and chrominance. At zero, vertex colors are frozen. At maximum, colors cycle rapidly, producing a strobing kaleidoscopic effect across the triangle faces.

---

#### Knob 3 — Spread
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

At zero, all vertices collapse to the center point and the triangles degenerate. As spread increases, the vertices swing farther from center, creating larger triangles that can extend beyond the screen edges. The X and Y axes are scaled differently — X spread is divided by 1024, Y spread by 2048 — producing slightly wider-than-tall orbits that compensate for the 16:9 aspect ratio. Internally, controls the radius of the Lissajous orbits that the eight outer vertices trace around screen center.

---

#### Knob 4 — Scale
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scales the overall size of the triangle geometry. This register is latched at vsync but the VHDL does not directly use a separate scale multiplier on vertex positions — the spread control primarily determines triangle size. The scale register is available in the architecture for future extensions or firmware-level tuning.

---

#### Knob 5 — Chroma
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the amplitude of the chrominance components. Vertex U and V colors are offset from neutral (512) by the triangle wave function, and this control scales how far the chrominance values deviate from neutral. At zero, all triangle fills are grayscale regardless of vertex color phase. At maximum, the full color range of the cycling vertices is visible — deep blues, warm oranges, vivid greens sweeping across the triangle faces.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the luminance of the rendered triangles. After color interpolation (or flat-color assignment), the per-pixel luminance is multiplied by this value. At zero, all triangles render as black regardless of vertex colors. At maximum, the full brightness range of the vertex color cycle is expressed. The multiplication is a 10×10 bit product shifted right by 9, so the effective range is 0× to approximately 2× gain.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Triangles** | 2 | 8 |
| **8 — Shading** | Smooth | Flat |
| **9 — Wireframe** | Off | On |
| **10 — Video Mod** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7 through 11 control a mixture of independent options and one notable hardware quirk. Switch 7 selects triangle count, but its encoding overlaps with Switch 8's flat shading bit — bit 1 of `registers_in(6)` is read as both `s_tri_count(1)` and `s_flat_mode`. This means enabling flat shading also forces the triangle count to 4. Switches 9 through 11 are fully independent binary options controlling wireframe overlay, video modulation, and bypass respectively.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the synthesized triangle output and the delayed input video. Three interpolator instances crossfade Y, U, and V independently. At zero, only the delayed input passes through. At maximum, only the synthesized output is visible. Intermediate positions blend the two, useful for layering the triangle geometry over an existing video signal at reduced opacity.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore Gouraud's synthesis capabilities from simple static geometry to fully animated, modulated compositions.

### Exercise 1: Static Triangle Fan

<img src={gouraud_exercise1_result} alt="Static Triangle Fan result"/>
*Static Triangle Fan — simulated result across source images.*
**What You'll Create**: Understand the basic triangle fan topology and Gouraud smooth shading.

1. **Freeze motion**: Set Morph Speed and Color Speed to 0%. The triangle field should be completely static.
2. **Observe the fan**: With Spread at ~75%, you should see two large triangles radiating from screen center, filled with smooth color gradients.
3. **Increase triangle count**: Move the Triangles switch to 4. Two additional triangles appear, filling more of the screen.
4. **Compare shading modes**: Toggle Shading between Smooth and Flat. In smooth mode, colors blend across each face. In flat mode, each triangle is a uniform solid color.
5. **Adjust chroma**: Sweep Chroma from 0% to 100%. At zero, the triangles are grayscale. At full, the vertex colors produce vivid hues.
6. **Brightness range**: Sweep Brightness from 0% to 100%. The triangles fade from black to full intensity.

**Key concepts**: Fan topology from screen center, Gouraud vs flat shading, vertex color interpolation produces continuous gradients, chroma and brightness as independent output controls

---

### Exercise 2: Animated Wireframe

<img src={gouraud_exercise2_result} alt="Animated Wireframe result"/>
*Animated Wireframe — simulated result across source images.*
**What You'll Create**: Explore vertex animation dynamics and the wireframe rendering mode.

1. **Start motion**: Set Morph Speed to ~30%. The triangles begin to drift and deform as vertices trace their Lissajous orbits.
2. **Enable wireframe**: Turn Wireframe on. The solid fills disappear, leaving only thin colored lines at the triangle edges.
3. **Speed up**: Increase Morph Speed to ~60%. The wireframe mesh morphs more rapidly, creating an animated geometric lattice.
4. **Add color cycling**: Set Color Speed to ~40%. The wireframe lines shift through the color spectrum.
5. **Widen the spread**: Increase Spread to ~90%. The wireframe extends to the screen edges, creating wide sweeping arcs.
6. **Observe edge detection**: Watch how the wireframe thickness remains constant (approximately 1 pixel) regardless of triangle size — the edge threshold is fixed in hardware.

**Key concepts**: DDS phase accumulation drives smooth vertex animation, wireframe renders only edge-proximate pixels, prime frequency offsets prevent vertices from synchronizing, Lissajous patterns from independent X/Y oscillators

---

### Exercise 3: Video-Modulated Kaleidoscope

<img src={gouraud_exercise3_result} alt="Video-Modulated Kaleidoscope result"/>
*Video-Modulated Kaleidoscope — simulated result across source images.*
**What You'll Create**: Combine all synthesis features with video modulation for a fully layered composition.

1. **Feed video**: Connect a video source. Enable Video Mod. The triangles now act as colored windows into the video — inside each triangle, the video is tinted by the interpolated vertex color.
2. **Fast animation**: Set Morph Speed to ~70% and Color Speed to ~60%. The geometric windows morph and recolor rapidly.
3. **Full chroma**: Set Chroma to ~100% and Brightness to ~100%. The video-modulated triangles display vivid, saturated hues.
4. **Partial mix**: Lower Mix to ~60%. The raw video blends through behind the modulated triangles, creating a layered composite.
5. **Toggle wireframe**: Turn Wireframe on while Video Mod remains active. The triangles collapse to colored outlines overlaying the full video image — a dynamic geometric overlay.
6. **Switch to flat shading**: Enable Flat mode. Each triangle window becomes a uniform color mask, creating bold stained-glass panels over the video.

**Key concepts**: Video modulation multiplies triangle luma by input luma, wireframe + video mod creates geometric overlays, flat shading produces uniform color masks, mix fader controls composite opacity

---


## Tips

- **Grayscale geometry**: Setting Chroma to 0% produces grayscale triangle fills that work well as luminance masks for downstream keying programs.
- **Feedback loops**: Routing Gouraud's output back to its own input (via Video Mod) creates recursive self-modulated geometry — triangles that texture themselves with their own rendered output.
- **Bypass for level check**: Switch 11 instantly shows the unprocessed input for verifying signal levels and sync integrity.
- **Slow morph for ambient visuals**: Morph Speed at 5–10% with high Spread produces slowly drifting stained-glass compositions ideal for ambient video installations.

---

## Glossary

| Term | Definition |
|------|------------|
| **Barycentric Coordinates** | A coordinate system for points inside a triangle, expressed as weighted averages of the three vertices; used in Gouraud interpolation. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator incremented by a fixed value each cycle. |
| **Edge Function** | A signed area computation that determines whether a point lies on the inside or outside of a triangle edge; all three must agree for the point to be inside. |
| **Fan Topology** | A triangle arrangement where all triangles share a common vertex (here, screen center), radiating outward like blades of a fan. |
| **Gouraud Shading** | A shading technique that interpolates vertex colors across a polygon face, producing smooth gradients; introduced by Henri Gouraud in 1971. |
| **Lissajous Figure** | A parametric curve traced by combining two sinusoidal oscillations along perpendicular axes; each vertex follows a unique Lissajous path. |
| **LUT** | Lookup Table; a pre-computed array of values indexed by an input, used here implicitly by the triangle wave function. |
| **Rasterization** | The process of determining which pixels are covered by a geometric primitive (triangle) and computing their colors. |
| **Triangle Wave** | A piecewise linear waveform that approximates a sine wave using four linear ramp segments; used for vertex position and color oscillation. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
