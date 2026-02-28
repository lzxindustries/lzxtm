---
draft: true
sidebar_position: 112
slug: /instruments/videomancer/geode
title: "Geode"
image: /img/instruments/videomancer/geode/geode_hero.png
---

import geode_hero from '/img/instruments/videomancer/geode/geode_hero.png';
import geode_animation from '/img/instruments/videomancer/geode/geode_animation.gif';
import geode_control_panel from '/img/instruments/videomancer/geode/geode_control_panel.png';
import geode_exercise1_result from '/img/instruments/videomancer/geode/geode_exercise1_result.png';
import geode_exercise2_result from '/img/instruments/videomancer/geode/geode_exercise2_result.png';
import geode_exercise3_result from '/img/instruments/videomancer/geode/geode_exercise3_result.png';

# Geode

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={geode_hero} alt="Geode hero image"/>
*Geode rendering a morphing hexagonal polygon with edge glow and dual counter-rotating interference.*
<img src={geode_animation} alt="Geode animated output"/>
*Geode output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Geode draws regular polygons on screen — triangles, squares, pentagons, hexagons, heptagons, and octagons — using a real-time half-plane rasterizer built entirely in FPGA logic. Each polygon is defined by its vertex positions, computed from a sin/cos lookup table, and tested pixel by pixel using incremental edge functions. The result is a geometrically precise shape that can rotate continuously, morph its vertices with a radial wobble, glow at its edges, and fill with either a solid hue-cycled color or the live video input.

The name *Geode* comes from the geological formation — a hollow rock whose interior is lined with crystal facets. Like a geode cracked open to reveal its geometry, this program exposes the pure polygonal scaffolding that underlies so much of computer graphics. The vertex count control selects how many facets the crystal has.

At conservative settings — a static hexagon with subtle edge glow on a black background — Geode produces clean geometric overlays suitable for titling or framing. At extreme settings — a dual morphing triangle with video fill, rotating at full speed over a video background — it becomes a kaleidoscopic compositing engine where the polygon acts as an animated shaped window into the source material.

---

## Background

### What Is Half-Plane Rasterization?

Determining whether a pixel lies inside a convex polygon is one of the fundamental problems in computer graphics. The **half-plane method** solves it by treating each edge of the polygon as a dividing line that splits the plane into two halves. A pixel is inside the polygon if and only if it lies on the correct side of *every* edge simultaneously. For each edge, the test reduces to evaluating a linear function $e = \Delta x \cdot (P_y - A_y) - \Delta y \cdot (P_x - A_x)$, where $A$ is a vertex and $(\Delta x, \Delta y)$ is the edge direction. If $e \geq 0$ for all edges (assuming consistent winding), the pixel is inside. Geode evaluates up to eight edge functions in parallel, one per polygon side.

### Why Incremental Evaluation?

Evaluating the edge function from scratch for every pixel would require a multiply per edge per pixel — far too expensive at video rates. Instead, Geode exploits the fact that along a horizontal scanline, only the $x$-coordinate changes. The edge function increment per pixel is simply $-\Delta y$, a constant for each edge. At the start of each scanline, the edge function is initialized with one multiply per edge (during horizontal blanking), and then each pixel requires only an addition per edge. This **incremental evaluation** reduces the per-pixel cost from a multiply to an add, enabling real-time rasterization of complex polygons at 74.25 MHz.

### Sin/Cos Lookup for Vertex Positioning

Geode places its polygon vertices on a circle centered on screen. The position of each vertex is determined by a **sin/cos lookup table** (`sin_cos_full_lut_10x10`) that maps a 10-bit angle (0–1023, representing 0°–360°) to signed 10-bit sine and cosine values. The angle for each vertex is the base rotation angle plus the vertex index times the angle step (1024 divided by the number of sides). This lookup is purely combinational — no BRAM, just fabric LUTs configured as ROM — keeping resource usage minimal.

### Radial Morph and DDS Animation

The polygon's rotation is driven by a **direct digital synthesis (DDS)** phase accumulator. Each frame, the accumulator adds the Rotation register value. The upper 10 bits of the 20-bit accumulator become the base rotation angle, so higher register values produce faster rotation. The morph effect adds a per-vertex radial oscillation: each vertex's radius is modulated by a triangle wave whose phase depends on both a global morph accumulator and the vertex index. This creates a pulsing, breathing deformation where vertices move inward and outward at slightly different rates.

### Edge Glow and Distance Fields

The minimum value among all edge functions at any pixel is a measure of that pixel's distance from the nearest polygon edge (in the edge-function metric, not Euclidean distance). Geode uses this minimum distance to generate an **edge glow** — a brightness falloff that is brightest right at the edge and fades to zero at a user-controlled width. In edge-only draw mode, the polygon interior is invisible and only the glowing outline remains, producing neon-like wireframe graphics.


---

## Signal Flow

```
Parameter Registers
│
├── VBlank: Vertex Computation ──────────────────────────────────
│   │
│   ├─ 1. Angle Calculation       (base rotation + vertex_index × step)
│   ├─ 2. Sin/Cos Lookup          (combinational LUT, 10-bit angle → sin/cos)
│   ├─ 3. Vertex Position         (center + radius × sin/cos, with morph wobble)
│   └─ 4. Repeat for N vertices   (sequential state machine, one vertex per cycle)
│
├── Per-Scanline: Edge Setup ────────────────────────────────────
│   │
│   └─ 5. Edge Function Init      (one multiply per edge at scanline start)
│
├── Per-Pixel: Rasterization ────────────────────────────────────
│   │
│   ├─ 6. Edge Increment          (add per-pixel delta to all edge functions)
│   ├─ 7. Inside/Outside Test     (all edges ≥ 0 → inside polygon)
│   ├─ 8. Edge Glow               (min edge distance → brightness falloff)
│   ├─ 9. Color Fill              (solid hue-mapped or video passthrough)
│   └─ 10. Background Compose     (black or video behind polygon)
│
├── Second Polygon (if Double enabled) ──────────────────────────
│   └─ Negated edge functions → counter-winding interference glow
│
├── Mix ─────────────────────────────────────────────────────────
│   └─ 3× interpolator_u          (wet/dry crossfade Y, U, V)
│
├── Sync Signals ────────────────────────────────────────────────
│   └─ Delayed by 8 clocks to match processing pipeline
│
└── Bypass ──────────────────────────────────────────────────────
    └─ Select original or generated signal
```

The critical architectural choice is the split between blanking-time computation and active-video computation. Vertex positions and the initial edge function setup run during horizontal and vertical blanking — the "off-screen" portion of each video line. During active video, each pixel requires only additions (one per edge) and comparisons, keeping the per-pixel logic fast enough for real-time HD. The edge glow is computed from the minimum edge function value across all active edges, which creates a smooth distance-based falloff rather than a binary inside/outside boundary. When the Double toggle is enabled, a second set of edge functions (with inverted winding) adds additional glow lines that interfere with the primary polygon's edges.

---

## Parameter Reference

<img src={geode_control_panel} alt="Videomancer front panel with Geode loaded"/>
*Videomancer's front panel with Geode active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sides
| Property | Value |
|----------|-------|
| Range | 3 – 8 |
| Default | 6 |

Selects the number of polygon sides. The 10-bit register value is mapped to integers 3 through 8 via threshold boundaries at approximately equal spacing. At the lowest setting, Geode draws a triangle — the simplest polygon; at the highest, an octagon that approaches a circle. Because the mapping uses discrete steps, you will feel distinct click-like transitions as you sweep the knob. The vertex computation and edge function evaluation automatically adjust to handle the selected number of sides.

---

#### Knob 2 — Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the polygon's radius — the distance from screen center to each vertex. At zero, the polygon collapses to a point. At maximum, the vertices extend to the edges of the frame. The radius directly scales the sin/cos lookup output, so the polygon maintains perfect geometric proportions at any size. When morph is active, the Size control sets the base radius around which the morph oscillation varies.

---

#### Knob 3 — Rotation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the rotation animation speed. The register value is added to a 20-bit phase accumulator each frame, with the upper 10 bits becoming the base angle. At zero, the polygon is static. At low values, it rotates slowly enough to track individual vertex movements. At high values, the polygon spins rapidly, and the morph wobble creates spirograph-like motion trails when combined with persistence effects downstream.

---

#### Knob 4 — Morph
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the amplitude of the radial morph deformation. At zero, all vertices sit at exactly the same radius, producing a perfect regular polygon. As you increase the control, each vertex oscillates inward and outward along its radial axis. The oscillation phase is offset per vertex (by 171/1024 of a cycle), so adjacent vertices move in opposition, creating a breathing, pulsing deformation. At high values, the polygon can collapse into star-like shapes as some vertices approach the center while others extend outward.

---

#### Knob 5 — Edge Glow
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the width of the edge glow effect. At zero, edges are sharp one-pixel boundaries. As you increase Edge Glow, pixels near the polygon edge receive brightness proportional to their proximity — creating a soft, neon-like halo around the polygon outline. The glow extends both inward and outward from the geometric edge. In edge-only draw mode, this control determines the line thickness of the wireframe rendering.

---

#### Knob 6 — Hue
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the chrominance of the solid fill color. The hue register is divided into four quadrants that map to different color combinations by shifting the U and V chroma channels relative to the neutral midpoint. At the lowest setting the fill is achromatic (white/gray). The remaining quadrants produce warm, cool, and intermediate tint combinations. This control has no effect when Fill Src is set to Video, since the fill color comes from the input signal instead.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Fill Src** | Color | Video |
| **8 — Draw Mode** | Filled | Edge |
| **9 — Double** | Off | On |
| **10 — Background** | Black | Video |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options. Fill Src and Background select video compositing modes. Draw Mode switches between filled polygon and edge-only wireframe. Double enables a second counter-winding polygon for interference patterns. Bypass routes the input signal directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the generated polygon output and the delayed input video. At maximum (default), the output is fully the generated signal. At minimum, the output is the unprocessed input. Intermediate positions blend between the two, allowing subtle geometric overlays. The mix is performed by three interpolator_u instances (one per YUV channel) using 10-bit fractional precision.

---

## Guided Exercises

These exercises progress from a simple static polygon to animated dual-polygon compositing, building familiarity with each control layer.

### Exercise 1: Static Geometric Shapes

<img src={geode_exercise1_result} alt="Static Geometric Shapes result"/>
*Static Geometric Shapes — simulated result across source images.*
**Objective**: Learn how the Sides and Size controls produce different regular polygon shapes.

1. **Triangle**: Set Sides fully counter-clockwise. A triangle appears on screen with sharp edges on a black background.
2. **Square**: Slowly turn Sides clockwise until the shape snaps to four sides. Note the discrete step — the transition is not gradual.
3. **Hexagon**: Continue clockwise to six sides. The shape approaches a circle but retains visible facets.
4. **Scale**: Sweep Size from minimum to maximum. Watch the polygon grow from a point at center to a shape that fills the frame.
5. **Edge glow**: Increase Edge Glow to about 50%. The edges develop a soft luminous halo. Note how the glow extends outward beyond the polygon boundary.
6. **Wireframe**: Switch Draw Mode to Edge. The polygon interior disappears, leaving only the glowing outline.

**Key concepts**: Half-plane rasterization, vertex count selection, edge distance glow, filled vs wireframe rendering

---

### Exercise 2: Animated Morph and Rotation

<img src={geode_exercise2_result} alt="Animated Morph and Rotation result"/>
*Animated Morph and Rotation — simulated result across source images.*
**Objective**: Explore continuous rotation and radial morph deformation as time-varying animation.

1. **Slow rotation**: Start with a pentagon (Sides ~40%). Set Rotation to about 20%. Watch the polygon spin slowly.
2. **Add morph**: Increase Morph to about 50%. The vertices begin pulsing inward and outward, creating a breathing star shape.
3. **Speed up**: Increase Rotation to about 60%. The shape spins faster and the morph creates spiraling vertex trails.
4. **Edge glow trail**: Increase Edge Glow to about 70%. The glow extends the visible area of the spinning edges, creating wider luminous arcs.
5. **Color shift**: Sweep Hue through its full range. Watch the fill color cycle through achromatic, warm, cool, and mixed tints.
6. **Observe morph extremes**: Increase Morph to maximum. Some vertices collapse to the center while others extend outward, creating star-burst formations.

**Key concepts**: DDS phase accumulator rotation, per-vertex radial oscillation, triangle wave morph, hue quadrant mapping

---

### Exercise 3: Dual Polygon Video Composite

<img src={geode_exercise3_result} alt="Dual Polygon Video Composite result"/>
*Dual Polygon Video Composite — simulated result across source images.*
**Objective**: Combine dual polygon mode with video fill and video background for complex compositing.

1. **Video fill**: Feed a camera or recorded source into the input. Set Fill Src to Video. The polygon interior now shows the live input.
2. **Video background**: Set Background to Video. The entire screen shows video, with the polygon edges visible as glowing overlays.
3. **Enable Double**: Turn on the Double toggle. A second set of edge glow lines appears, creating interference patterns where the two polygons' edges cross.
4. **Triangle interference**: Set Sides to minimum (triangle). The dual triangles create six-pointed star-like glow patterns.
5. **Morph animation**: Add Morph at about 60%. The interference patterns shift and breathe as the vertices oscillate.
6. **Mix blend**: Lower the Mix fader to about 60%. The polygon overlay becomes semi-transparent over the video, creating a subtle geometric texture.
7. **Sweep rotation**: Increase Rotation to about 40%. The entire composite animation rotates, with the video windowed through a spinning geometric mask.

**Key concepts**: Video fill compositing, dual polygon interference, edge glow overlay on video, wet/dry mix blending

---


## Tips

- **Sides are discrete steps**: Unlike most Videomancer knobs, the Sides control has only six positions (3–8). You will feel distinct transitions — there are no fractional side counts.
- **Edge Glow is the signature effect**: The luminous edge falloff is what gives Geode its distinctive look. Even at low values it adds depth; at high values it produces neon-wireframe graphics.
- **Video fill creates shaped windows**: Set Fill Src to Video and Background to Black to use the polygon as an animated viewport — a geometric mask that reveals the live input within the polygon and hides it outside.
- **Morph creates star shapes**: At high Morph values, alternating vertices collapse inward while others extend outward, turning regular polygons into star formations. The effect is most dramatic on triangles and squares.
- **Rotation speed is exponential**: Because the rotation register value is added per frame, doubling the knob position doubles the rotation speed. Very high values produce rapid spinning.
- **Feedback loops**: Routing Geode's output back through its own input (via Fill Src = Video or Background = Video in a feedback patch) creates recursive geometric patterns — polygons within polygons.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed signal for before/after comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **Convex Polygon** | A polygon where all interior angles are less than 180°; any line segment between two interior points lies entirely within the polygon. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator at a fixed rate and using its value to index a lookup table. |
| **Edge Function** | A linear equation evaluated per pixel that determines which side of a polygon edge the pixel lies on; the sign of the result indicates inside or outside. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Half-Plane Rasterization** | A method for determining polygon interior by testing whether a pixel lies on the correct side of all edges simultaneously. |
| **Incremental Evaluation** | An optimization where per-pixel computation is reduced to a single addition by exploiting the fact that only one coordinate changes along a scanline. |
| **LUT** | Look-Up Table; in FPGA context, a small memory element used to implement combinational logic or ROM data. |
| **Morph** | Radial deformation of polygon vertices that creates breathing, pulsing shapes by oscillating vertex distance from center. |
| **N-gon** | A polygon with N sides; a regular N-gon has all sides equal and all angles equal. |
| **Phase Accumulator** | A register that increments by a fixed value each cycle; its overflow rate generates a frequency, used here for rotation animation. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Sin/Cos LUT** | A lookup table that maps angle values to sine and cosine outputs, used for positioning vertices on a circle. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
