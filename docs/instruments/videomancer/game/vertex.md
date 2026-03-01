---
draft: true
sidebar_position: 275
slug: /instruments/videomancer/vertex
title: "Vertex"
image: /img/instruments/videomancer/vertex/vertex_hero.png
description: "Vertex recreates the unmistakable visual artefacts of early 3D game consoles — specifically the PlayStation 1 and Sega Saturn — whose GPUs operated with..."
---

import vertex_before_after from '/img/instruments/videomancer/vertex/vertex_before_after.png';
import vertex_control_panel from '/img/instruments/videomancer/vertex/vertex_control_panel.png';
import vertex_exercise1_result from '/img/instruments/videomancer/vertex/vertex_exercise1_result.png';
import vertex_exercise2_result from '/img/instruments/videomancer/vertex/vertex_exercise2_result.png';
import vertex_exercise3_result from '/img/instruments/videomancer/vertex/vertex_exercise3_result.png';
import vertex_hero from '/img/instruments/videomancer/vertex/vertex_hero.png';
import vertex_source1_kodim15 from '/img/instruments/videomancer/vertex/vertex_source1_kodim15.png';
import vertex_source2_kodim03 from '/img/instruments/videomancer/vertex/vertex_source2_kodim03.png';
import vertex_source3_kodim15_bw from '/img/instruments/videomancer/vertex/vertex_source3_kodim15_bw.png';

# Vertex

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={vertex_hero} alt="Vertex hero image"/>
*Vertex shattering a live video feed into a jittering polygon mesh with PS1-era vertex wobble, posterised Gouraud banding, wireframe grid overlay, and ordered dithering across a field of flat-shaded quads.*
<img src={vertex_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Vertex applied.*

---

## Overview

Vertex recreates the unmistakable visual artefacts of early 3D game consoles — specifically the PlayStation 1 and Sega Saturn — whose GPUs operated without subpixel vertex precision, perspective-correct texture mapping, or sufficient color gradient resolution. The result was a generation of games where polygon geometry wobbled and danced, color gradients stairstepped into visible bands, and wireframe edges occasionally showed through the mesh. What were once engineering limitations are now a celebrated aesthetic, and Vertex applies this full suite of artefacts to any live video feed.

The name references the mathematical vertices that define polygon corners in 3D rendering pipelines. On the PS1, vertex coordinates were snapped to integer screen positions, causing geometry to jitter by up to a full pixel as the camera moved — a distinctive wobble that became the visual signature of an entire console generation. Vertex simulates this by applying LFSR-derived per-scanline horizontal displacement to the video through line buffer readout address perturbation, creating the characteristic swimming, unstable geometry.

At mild settings, Vertex adds a subtle retro texture to the image — gentle posterisation and faint grid lines that evoke the low-poly era without overwhelming the source. Pushed to extremes, the effect is unmistakable: heavy jitter tears the image apart, aggressive posterisation reduces the palette to a handful of banded colors, thick wireframe grids carve the frame into visible polygons, and per-cell tint simulates the flat-faceted normals of an untextured 3D model.

---

## Background

### Integer Vertex Coordinates and Subpixel Precision

The PlayStation 1's GPU (designed by Toshiba) operated entirely with fixed-point integer arithmetic for vertex positioning. Unlike later GPUs that used sub-pixel precision to smoothly interpolate polygon edges, the PS1 snapped every vertex to the nearest integer pixel coordinate. As a 3D camera moved, vertices quantised to different integer positions frame-to-frame, causing the characteristic jitter where polygon edges and textures appeared to swim and vibrate. This was most visible on large, flat surfaces and distant objects where small camera movements caused disproportionate integer snapping. Vertex simulates this by applying a per-scanline random horizontal offset to the line buffer readout, displacing each row of pixels by a different amount.

### Gouraud Shading and Color Banding

Gouraud shading interpolates vertex colors across polygon faces, producing smooth color gradients. On the PS1, this interpolation was performed with limited precision — typically 5 bits per color channel — producing visible banding where the gradient stairstepped between discrete color levels. This banding was especially prominent on large polygons spanning significant color differences, such as lighting gradients across walls or skin tones. Vertex recreates this effect through bit-depth reduction (posterisation), progressively shifting and masking the color channels to simulate the limited interpolation precision of 1990s consumer GPUs.

### Wireframe Debug Rendering

During game development, artists and programmers frequently toggled wireframe rendering to inspect polygon mesh topology — the structural skeleton of every 3D scene. The wireframe view drew only the polygon edges, revealing the density and arrangement of the mesh. Occasionally, wireframe artefacts leaked into final renders as edge-highlighting glitches. Vertex draws cell boundary edges in a fixed brightness set by the Edge Glow control, overlaying a visible grid structure that suggests the underlying polygon mesh of a 3D scene rendered with insufficient z-buffer precision.

### Ordered Dithering

Ordered dithering is a deterministic technique for reducing color banding when quantising to a lower bit depth. By adding a fixed threshold pattern (a Bayer matrix) to pixel values before quantisation, the resulting banding breaks up into a regular dot pattern that the eye integrates into a smoother apparent gradient. The technique was widely used in 1990s game rendering to mask the visible stairstepping of Gouraud shading. Vertex implements a 2×2 Bayer matrix dither that adds a position-dependent offset before posterisation, producing the distinctive crosshatch pattern visible in many PS1 titles.

### Flat Shading and Per-Face Color

Before Gouraud shading became standard, flat shading assigned a single color to each polygon face based on its surface normal relative to the light source. This produced a faceted, polygonal look where each face was a uniform color with hard edges at polygon boundaries — a look that defined early 3D games like Virtua Fighter and Star Fox. Vertex's Flat Shade mode forces chrominance to neutral and uses only the quantised luminance per cell, creating uniform-color grid cells that simulate the per-face flat shading of untextured polygon models.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Line Buffer Write ───────────────────────────────────────
│   │
│   └─ 1. Store current scanline Y/U/V into 3× BRAM (1024×10)
│
├── Jitter Offset ───────────────────────────────────────────
│   │
│   ├─ 2. Per-scanline LFSR → signed offset
│   └─ 3. Scale offset by Jitter amount → read address displacement
│
├── Jittered Read ───────────────────────────────────────────
│   │
│   └─ 4. Read Y/U/V from line buffer at write_addr + jitter_offset
│
├── Grid Cell Detection ─────────────────────────────────────
│   │
│   ├─ 5. Mask h_count/v_count by cell size → detect H/V edges
│   ├─ 6. Compare h_intra == v_intra → detect diagonal (triangle mode)
│   └─ 7. XOR cell coordinates + LFSR → cell hash for tint
│
├── Posterize + Dither ──────────────────────────────────────
│   │
│   ├─ 8. If Dither: add 2×2 Bayer offset to Y before quantise
│   └─ 9. Shift right then left by Posterize amount → reduce bit depth
│
├── Cell Tint ───────────────────────────────────────────────
│   │
│   └─ 10. Add (cell_hash × Cell Tint) >> 10 to luminance
│
├── Flat Shade ──────────────────────────────────────────────
│   │
│   └─ 11. If Flat: force U/V to 512 (neutral)
│
├── Color Kill ──────────────────────────────────────────────
│   │
│   └─ 12. If Color Kill: force U/V to 512 (monochrome)
│
├── Wireframe Overlay ───────────────────────────────────────
│   │
│   ├─ 13. At H/V cell edges: replace with Edge Glow brightness
│   └─ 14. If Triangle grid + on diagonal: also replace
│
├── Mix ─────────────────────────────────────────────────────
│   └─ Interpolator: dry (original) ↔ wet (PS1 effect)
│
└── Output ──────────────────────────────────────────────────
    └─ Direct output (no bypass toggle in this program)
```

The pipeline order reflects the logical sequence of PS1 rendering artefacts. Vertex jitter occurs first at the geometry stage — displacing pixel positions before any shading computation, just as integer vertex snapping happened before rasterisation in actual hardware. Posterisation follows as the Gouraud shading artefact, reducing color resolution during the interpolation stage. Cell tint adds per-polygon brightness variation simulating flat-shaded face normals. The wireframe overlay is last because it represents the polygon edge structure drawn on top of the filled and shaded faces.

The line buffer is essential for horizontal jitter — the FPGA reads each scanline from BRAM at an offset address, effectively shifting the entire row left or right by the LFSR-derived displacement. The LFSR re-seeds each frame when Animate is enabled, causing the jitter pattern to change every frame (simulating the camera-movement-dependent wobble of real PS1 geometry). In Static mode, the LFSR state is fixed, producing consistent per-line displacement that remains stable frame-to-frame.

---

## Parameter Reference

<img src={vertex_control_panel} alt="Videomancer front panel with Vertex loaded"/>
*Videomancer's front panel with Vertex active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Jitter
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the magnitude of per-scanline horizontal displacement applied to the line buffer readout. At zero, the readout address matches the write address exactly — no jitter is visible. As Jitter increases, each scanline shifts horizontally by a larger random offset, creating the characteristic vertex wobble where straight edges break into jagged, swimming lines. At maximum, the displacement is so large that the image tears apart into horizontal strips, each shifted by up to several dozen pixels.

---

#### Knob 2 — Grid Size
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 1 |

Selects the grid cell size that defines the polygon mesh resolution. The four positions map to 8×8, 16×16, 32×32, and 64×64 pixel cells. Smaller cells create a denser polygon mesh with more wireframe lines and more per-cell tinting variety. Larger cells create bigger polygons with more visible flat shading and more dramatic wireframe structure. The grid size also affects the perceived posterisation, since larger cells contain more color variation within each quantised region.

---

#### Knob 3 — Posterize
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the bit-depth reduction applied to the color channels. At zero, no posterisation occurs — full 10-bit color depth is preserved. As Posterize increases, progressively more least-significant bits are dropped, creating stairstepped color bands. At moderate values, the effect is subtle — gentle banding in gradients resembling Gouraud shading precision limits. At maximum, the image reduces to a handful of discrete brightness levels with dramatic hard-edged color bands.

---

#### Knob 4 — Cell Tint
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the magnitude of per-cell random brightness offset. The offset is computed from a hash of the cell coordinates XORed with the LFSR state, producing a pseudo-random brightness value unique to each cell. At zero, no tint is applied. As Cell Tint increases, each grid cell receives a progressively larger brightness offset, simulating the per-face normal variation of a flat-shaded 3D model where each polygon face reflects light at a different angle.

---

#### Knob 5 — Wobble Spd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the speed of jitter animation. When the Animate toggle is enabled, the LFSR re-seeds each frame with an advanced state, causing the per-scanline displacement pattern to evolve over time. Higher Wobble Spd values advance the LFSR faster between frames, creating more rapid jitter changes. At zero, even with Animate enabled, the jitter pattern changes very slowly. The wobble effect is most visible on large, flat surfaces where the frame-to-frame displacement change creates a characteristic swimming, unstable quality.

---

#### Knob 6 — Edge Glow
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the brightness of the wireframe grid overlay at cell boundaries. At zero, no wireframe is visible — the grid is purely implicit. As Edge Glow increases, the horizontal and vertical cell boundary lines become brighter, drawing a visible grid over the image. At maximum, the wireframe lines are full white, creating a stark mesh overlay. When Triangle grid mode is active, diagonal lines within each cell also render at this brightness, creating a triangulated mesh appearance.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Grid Shape** | Quad | Triangle |
| **8 — Shading** | Input | Flat |
| **9 — Animate** | Static | Animate |
| **10 — Color Kill** | Off | On |
| **11 — Dither** | Off | On |

The five toggles configure the geometric, shading, and color characteristics of the polygon artefact simulation. Grid Shape and Shading define the fundamental polygon rendering mode. Animate controls whether jitter evolves frame-to-frame. Color Kill and Dither modify the color treatment of the posterised output. Note that this program does not include a Bypass toggle — toggle 11 controls the Dither effect instead.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfade between the dry (original) and wet (PS1 artefact) signals. At 0%, the output is pure unprocessed video. At 100%, the output is the full polygon artefact effect with jitter, posterisation, wireframe, and tinting. Intermediate values blend the two, useful for subtly introducing the retro aesthetic without overwhelming the source.

---

## Guided Exercises

These exercises progress from basic jitter and posterisation to a full PS1-era polygon artefact composition, exploring how each rendering limitation contributes to the characteristic early-3D-game aesthetic.

### Exercise 1: Vertex Wobble

<img src={vertex_exercise1_result} alt="Vertex Wobble result"/>
*Vertex Wobble — simulated result across source images.*
**Source**: A static scene with strong straight lines — architecture, a bookshelf, window frames, or geometric patterns.

**Objective**: Introduce PS1-style vertex jitter and observe how straight edges break into swimming, unstable lines.

1. **Enable animation**: Toggle Animate to Animate. Jitter will change every frame.
2. **Set moderate jitter**: Increase Jitter to ~40%. Watch straight lines in the source begin to shimmer and wobble.
3. **Add wireframe**: Set Edge Glow to ~50%. A visible grid overlay appears, its lines also affected by the jitter.
4. **Try different grid sizes**: Rotate Grid Size through all four positions. Observe how smaller cells create denser wobble and larger cells create more dramatic but sparser displacement.
5. **Compare static vs animated**: Toggle Animate between Static and Animate. Static shows fixed displacement; Animate shows the characteristic frame-to-frame swimming.

**Key concepts**: Per-scanline jitter from line buffer offset creates the vertex wobble effect, animate mode recreates the frame-to-frame variation caused by camera movement, grid size defines the polygon mesh density

---

### Exercise 2: Gouraud Banding

<img src={vertex_exercise2_result} alt="Gouraud Banding result"/>
*Gouraud Banding — simulated result across source images.*
**Source**: A smooth gradient scene — a sunset, a softly lit face, a colored backdrop, or any content with continuous tonal transitions.

**Objective**: Recreate the Gouraud shading color banding of PS1 graphics and explore how dithering mitigates it.

1. **No jitter**: Set Jitter to 0% to isolate the color effect.
2. **Posterise**: Increase Posterize to ~60%. Watch smooth gradients break into visible color bands.
3. **Add dithering**: Toggle Dither to On. The hard band edges soften into a crosshatch pattern.
4. **Increase posterisation**: Push Posterize to ~80%. The bands become fewer and wider, with the dither pattern more prominent.
5. **Cell tint**: Add Cell Tint at ~30% with Grid Size 32x32. Each cell gets a slightly different brightness, simulating per-face normal variation.
6. **Flat shade**: Toggle Shading to Flat. Chrominance disappears, leaving only luminance bands — the look of an untextured flat-shaded model.

**Key concepts**: Posterisation simulates limited Gouraud interpolation precision, dithering breaks up banding into tolerable patterns, flat shading removes color to emphasise polygon structure

---

### Exercise 3: Full PS1 Composite

<img src={vertex_exercise3_result} alt="Full PS1 Composite result"/>
*Full PS1 Composite — simulated result across source images.*
**Source**: A moving scene with both detail and broad color areas — gameplay footage, a dancing figure, or a busy street with architectural elements.

**Objective**: Combine all PS1 artefacts into a complete retro-game aesthetic: jittering geometry, color-banded shading, wireframe mesh, and animated wobble.

1. **Jitter + animate**: Jitter ~50%, Animate On, Wobble Spd ~40%.
2. **Posterise with dither**: Posterize ~50%, Dither On.
3. **Cell tint for faceted look**: Cell Tint ~40%, Grid Size 16x16.
4. **Triangle mesh**: Toggle Grid Shape to Triangle. Diagonal wireframe lines appear within each cell.
5. **Wireframe overlay**: Edge Glow ~40%. The full triangulated mesh structure becomes visible.
6. **Color Kill for monochrome**: Toggle Color Kill On for maximum retro impact, then toggle Off to compare the color version.
7. **Mix control**: Reduce Mix to ~70% to blend the PS1 effect with the original, creating a subtle retro filter.

**Key concepts**: Layering all artefacts together produces the authentic early-3D-game look, triangle grid adds mesh complexity, color kill recreates the wireframe debug aesthetic, partial mix creates a subtler retro treatment

---


## Tips

- **Match Grid Size to content scale**: Use 8×8 or 16×16 cells for detailed subjects (faces, text), and 32×32 or 64×64 for broad scenic content (landscapes, architecture). The grid should be small enough to create visible polygon structure but large enough to contain meaningful image content per cell.
- **Jitter + Animate sells the PS1 feel**: The single most recognizable PS1 artefact is the swimming vertex jitter. Even with all other effects disabled, Jitter at 30–40% with Animate On creates an instantly recognizable retro-game look.
- **Dither at moderate posterisation**: Dithering is most effective at moderate posterisation levels (40–60%) where it breaks up visible banding without creating an overwhelming pattern. At very high posterisation, the dither becomes a dominant visual element.
- **Cell Tint for faceted look**: Even small amounts of Cell Tint (15–25%) dramatically change the perceived surface quality, making flat areas appear as individually lit polygon faces.
- **No Bypass — use Mix**: Since this program has no bypass toggle, use the Mix fader to compare the processed output with the source. Mix at 0% gives the original video; mix at 100% gives the full effect.
- **Triangle mode for mesh complexity**: Triangle grid doubles the visual wireframe density without changing the cell size, creating a more intricate polygon mesh appearance.
- **Color Kill for wireframe studies**: Combine Color Kill with high Edge Glow and Flat Shade for a wireframe debug render that reveals the polygon structure with maximum clarity.
- **Wobble Spd at zero with Animate On**: Even with Animate enabled, zero Wobble Spd produces nearly static jitter. Use small Wobble Spd values for a subtle drift rather than aggressive frame-to-frame change.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bayer Matrix** | An ordered threshold array used for dithering; Vertex uses a 2×2 matrix producing a four-level crosshatch pattern. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **Cell Hash** | XOR combination of cell grid coordinates and LFSR state, producing a pseudo-random value unique to each grid cell for tinting. |
| **Flat Shading** | A rendering technique assigning a single color to each polygon face, producing a faceted, low-poly appearance. |
| **Gouraud Shading** | A rendering technique interpolating vertex colors across polygon surfaces, producing smooth but precision-limited gradients. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **Line Buffer** | BRAM-based scanline storage enabling horizontal readout displacement for the jitter effect. |
| **Posterisation** | Reduction of color bit depth by shifting right then left, creating stairstepped color bands from smooth gradients. |
| **Subpixel Precision** | The ability to position vertices at fractional pixel coordinates, absent in PS1 hardware, causing integer-snapping wobble. |
| **Wireframe** | A rendering mode showing only polygon edges, simulated here by drawing grid cell boundary lines at Edge Glow brightness. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
