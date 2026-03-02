---
draft: true
sidebar_position: 317
slug: /instruments/videomancer/xorwire
title: "Xorwire"
image: /img/instruments/videomancer/xorwire/xorwire_hero.png
description: "XOR Wire renders a rotating three-dimensional polyhedron directly in the video stream using per-pixel edge distance testing."
---

import xorwire_hero from '/img/instruments/videomancer/xorwire/xorwire_hero.png';
import xorwire_animation from '/img/instruments/videomancer/xorwire/xorwire_animation.gif';
import xorwire_control_panel from '/img/instruments/videomancer/xorwire/xorwire_control_panel.png';
import xorwire_exercise1_result from '/img/instruments/videomancer/xorwire/xorwire_exercise1_result.gif';
import xorwire_exercise2_result from '/img/instruments/videomancer/xorwire/xorwire_exercise2_result.gif';
import xorwire_exercise3_result from '/img/instruments/videomancer/xorwire/xorwire_exercise3_result.gif';

# Xorwire

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={xorwire_hero} alt="Xorwire hero image"/>
*A luminous wireframe cube rotates through live video, its edges etched in XOR interference patterns that invert the underlying image.*
<img src={xorwire_animation} alt="Xorwire animated output"/>
*Xorwire output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

XOR Wire renders a rotating three-dimensional polyhedron directly in the video stream using per-pixel edge distance testing. Rather than frame-buffer rendering, the FPGA evaluates all twelve edges of the shape simultaneously for every pixel in real time, drawing lines where the Manhattan distance falls within the thickness threshold. This massively parallel approach trades LUT resources for deterministic single-frame latency with zero BRAM.

The name references the XOR compositing mode central to ZX Spectrum vector demos of the late 1980s. XOR blending creates ghostly interference patterns where wireframe edges cross bright regions of the input, producing the characteristic "negative" look of classic 8-bit 3D. An additive mode is also available for a more contemporary glow aesthetic.

Four polyhedra are available — Cube, Pyramid, Octahedron, and Diamond — each defined by vertex tables rotated through all three axes using quarter-wave sine and cosine lookups. The rotation speeds are bipolar, allowing forward, reverse, or frozen axes in any combination.

---

## Background

### Vector Graphics on 8-Bit Hardware

The ZX Spectrum lacked hardware sprites or blitters, so 3D graphics required software line drawing into a 256×192 pixel framebuffer. Elite (1984) and Starion (1985) demonstrated wireframe rendering within severe CPU constraints. The XOR draw mode was essential: it allowed lines to be erased by drawing them a second time without needing to store background pixels.

### Real-Time Rasterization Without a Framebuffer

XOR Wire takes a fundamentally different approach from software line drawing. Instead of tracing pixels along each edge sequentially, the FPGA tests every screen pixel against all edges simultaneously. This per-pixel distance field approach is related to signed distance function rendering used in modern shader art, but implemented here in fixed-point VHDL for single-cycle throughput.

### Orthographic Projection

The program uses orthographic (parallel) projection rather than perspective. Vertex X and Y coordinates are scaled and translated to screen space while the Z axis only participates in rotation. This preserves the flat, graphic quality of early 8-bit 3D where objects appear as rigid wireframes rather than perspectively distorted solids.

### XOR Compositing

Bitwise XOR between the wireframe luminance and input video creates a unique visual interaction: bright regions invert to dark where edges cross them, while dark regions gain brightness. The result is a holographic interference pattern that depends equally on wireframe geometry and input content. In the additive mode, wireframe luminance is simply added to the input, producing a glowing overlay.


---

## Signal Flow

```
registers_in ──→ [Register Map] ──→ rotation speeds, scale, line width, brightness
                                    toggles: shape, fill, composite, color, bypass

                ┌─────────────────────────────────────────┐
                │           VBLANK VERTEX UPDATE           │
                │  angle accumulators += speed − 512       │
                │  for each vertex:                        │
                │    rotate X → rotate Y → rotate Z       │
                │    orthographic project → screen coords  │
                └─────────────────────────────────────────┘
                                    │
                              s_proj(0..7)
                                    │
                                    ▼
data_in ──→ [h/v counters] ──→ [Per-Pixel Edge Test]
                                12 edges parallel:
                                cross product distance
                                segment t clamping
                                min distance select
                                    │
                            s_edge_hit, s_edge_idx
                                    │
                                    ▼
                              [Composite]
                         XOR or Add with input
                         white or rainbow hue
                                    │
                               s_gen_y/u/v
                                    │
                                    ▼
                         [interpolator_u × 3]
                           wet/dry crossfade
                                    │
                                    ▼
                               data_out
```

The vertex rotation and projection runs entirely during the vertical blanking interval, computing all eight screen-space vertex positions once per frame. During active video, the rasterizer tests the current pixel's Manhattan distance against all twelve edge segments in parallel, selecting the nearest edge and comparing against the line width threshold. This two-phase architecture avoids any per-pixel vertex computation and keeps the active-line pipeline at a constant depth of five processing clocks plus four interpolator clocks.

---

## Parameter Reference

<img src={xorwire_control_panel} alt="Videomancer front panel with Xorwire loaded"/>
*Videomancer's front panel with Xorwire active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — X Rotate
| Property | Value |
|----------|-------|
| Range | -180deg – 180deg |
| Default | 31deg |
| Suffix | deg |

X Rotate controls the angular velocity around the horizontal axis. At centre (512) the axis is frozen. Turning clockwise increases forward rotation speed; turning counter-clockwise reverses it. Combined with Y and Z rotation, complex tumbling orbits emerge. Setting all three axes to slightly different speeds produces the classic "tumbling cube" of 1980s vector demos.

---

#### Knob 2 — Y Rotate
| Property | Value |
|----------|-------|
| Range | -180deg – 180deg |
| Default | 24deg |
| Suffix | deg |

Y Rotate controls rotation speed around the vertical axis. This is the most visually prominent axis for a cube, swinging faces in and out of view. At extreme speeds the shape blurs into a cylindrical shell of overlapping edges, creating dense moire patterns with the XOR composite mode.

---

#### Knob 3 — Z Rotate
| Property | Value |
|----------|-------|
| Range | -180deg – 180deg |
| Default | 0deg |
| Suffix | deg |

Z Rotate controls rotation speed around the depth axis (perpendicular to screen). This produces a pinwheel-like spinning motion. When the other axes are frozen, Z rotation alone creates a flat 2D rotation effect. Combined with X and Y, it adds a rolling component to the tumble.

---

#### Knob 4 — Scale
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scale adjusts the orthographic projection size. At minimum the shape collapses to a point at screen centre. At maximum it fills the entire frame, with edges extending well beyond the visible area. Mid-range values (40–60%) produce the most legible wireframe geometry. The scale control has a minimum clamp at approximately 6% to prevent degenerate zero-size projections.

---

#### Knob 5 — Line Width
| Property | Value |
|----------|-------|
| Range | 1px – 4px |
| Default | 2px |
| Suffix | px |

Line Width sets the edge rendering thickness in four discrete steps (1–4 pixels). At its narrowest the wireframe appears as a fine hairline mesh. At maximum width, edges become bold strokes that overlap at vertices, creating filled junction regions even in wireframe mode. Thicker lines interact more dramatically with the XOR composite, producing wider interference bands.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Brightness scales the luminance of the wireframe lines from black to full white. At zero the wireframe is invisible; at maximum the XOR interaction is strongest. In additive mode, brightness controls how much energy the wireframe adds to the input signal. Mid-range brightness in XOR mode produces the subtlest interference effects.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Shape** | Cube | Pyramid |
| **8 — Fill** | Wire | Solid |
| **9 — Composite** | XOR | Add |
| **10 — Color** | White | Rainbow |
| **11 — Bypass** | Off | On |

The five toggles configure shape geometry, rendering style, compositing mode, colouring, and bypass. Shape selects between four polyhedra with different vertex and edge counts. Fill switches between wireframe (edges only) and solid rendering. Composite chooses XOR interference or additive glow blending. Color provides monochrome white or per-edge rainbow hue assignment. Bypass passes the input through unprocessed.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the dry (unprocessed) input and the wet (wireframe-composited) output. At 0% the output matches the input. At 100% the full wireframe composite is visible. Intermediate positions blend the two, useful for ghosting the wireframe subtly over live video.

---

## Guided Exercises

These three exercises demonstrate the core wireframe interactions, from classic XOR tumble to rainbow overlay to creating dense geometric textures.

### Exercise 1: Classic Tumbling Cube

<img src={xorwire_exercise1_result} alt="Classic Tumbling Cube result"/>
*Classic Tumbling Cube — simulated result across source images.*
**Objective**: Achieve the classic ZX Spectrum wireframe cube tumbling over live video with XOR interference.

1. Set all three rotation axes to gentle forward speeds (X=580, Y=600, Z=540).
2. Scale to 50% so the cube is well-framed within the image.
3. Set Line Width to the finest setting (step 1).
4. Raise Brightness to 80%.
5. Ensure Shape=Cube, Composite=XOR, Color=White, Fill=Wire.
6. Observe how the wireframe edges invert bright regions of the face.
7. Reduce Brightness to 40% for a subtler interference pattern.

**Key concepts**: - XOR compositing creates interference that depends on input brightness
- Bipolar rotation allows each axis to spin independently
- Fine line width gives the cleanest classic vector demo aesthetic

---

### Exercise 2: Rainbow Octahedron Overlay

<img src={xorwire_exercise2_result} alt="Rainbow Octahedron Overlay result"/>
*Rainbow Octahedron Overlay — simulated result across source images.*
**Objective**: Create a rainbow-coloured wireframe floating over saturated video using additive blending.

1. Switch Shape to Octahedron and Color to Rainbow.
2. Set Composite to Add for a glowing overlay.
3. Set rotation to a slow tumble (X=530, Y=520, Z=510).
4. Increase Scale to 70% and Line Width to step 3.
5. Adjust Brightness to 60% so the wireframe glows without washing out.
6. Watch how rainbow edges interact with the coloured input.

**Key concepts**: - Rainbow mode assigns unique hues per edge using the sine LUT
- Additive compositing adds energy rather than inverting
- The Octahedron's symmetric edge layout creates kaleidoscopic patterns

---

### Exercise 3: Dense Geometric Texture

<img src={xorwire_exercise3_result} alt="Dense Geometric Texture result"/>
*Dense Geometric Texture — simulated result across source images.*
**Objective**: Create a dense, overlapping wireframe texture by maximising line width and rotation speed.

1. Set all rotation speeds to maximum in different directions (X=1023, Y=0, Z=1023).
2. Scale to 90% to fill the screen.
3. Line Width to maximum (step 4).
4. Shape=Cube, Composite=XOR, Color=White.
5. Brightness to 100%.
6. The rapidly overlapping thick edges create a complex XOR texture.
7. Reduce Mix to 60% to blend with the dark background.

**Key concepts**: - Maximum rotation and line width creates dense moire interference
- XOR of overlapping edges produces unpredictable evolving patterns
- Mix control allows the texture to be subtly layered

---


## Tips

- **Slow single-axis rotation** reveals the geometric structure of each polyhedron most clearly. Freeze two axes and rotate one at a time to understand each shape.
- **XOR on grey** produces the most visible interference because the midpoint luminance has maximum dynamic range for both brightening and darkening.
- **Rainbow + slow rotation** creates the most visually striking colour display as individual edge hues become distinguishable.
- **Additive on dark backgrounds** makes the wireframe glow like a neon sign, which pairs well with dark or high-contrast source video.
- **Maximum line width** at high rotation speed creates dense moire textures that evolve continuously, useful as abstract background overlays.
- **Mix at 30–50%** produces a ghostly wireframe suggestion that works well as a subtle geometric overlay on narrative video content.

---
