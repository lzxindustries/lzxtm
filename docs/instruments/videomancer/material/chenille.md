---
draft: true
sidebar_position: 45
slug: /instruments/videomancer/chenille
title: "Chenille"
image: /img/instruments/videomancer/chenille/chenille_hero.png
description: "Chenille is named for the French word meaning \"caterpillar\" — the same word that gives its name to the soft, tufted fabric whose surface is made of tiny cut threads standing upright in a dense grid."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import chenille_hero from '/img/instruments/videomancer/chenille/chenille_hero.png';
import chenille_control_panel from '/img/instruments/videomancer/chenille/chenille_control_panel.png';
import chenille_exercise1_result from '/img/instruments/videomancer/chenille/chenille_exercise1_result.png';
import chenille_exercise2_result from '/img/instruments/videomancer/chenille/chenille_exercise2_result.png';
import chenille_exercise3_result from '/img/instruments/videomancer/chenille/chenille_exercise3_result.png';
import chenille_source1_kodim15 from '/img/instruments/videomancer/chenille/chenille_source1_kodim15.png';
import chenille_source2_kodim03 from '/img/instruments/videomancer/chenille/chenille_source2_kodim03.png';
import chenille_source3_kodim13_bw from '/img/instruments/videomancer/chenille/chenille_source3_kodim13_bw.png';

# Chenille

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: chenille_source1_kodim15, after: chenille_hero },
    { label: "Kodim03", before: chenille_source2_kodim03, after: chenille_hero },
    { label: "Kodim13 B&W", before: chenille_source3_kodim13_bw, after: chenille_hero },
  ]}
/>
*Chenille transforming a still life into a field of luminous tufted dots, each pile cluster carrying the color memory of the pixel it replaced.*

---

## Overview

Chenille is named for the French word meaning "caterpillar" — the same word that gives its name to the soft, tufted fabric whose surface is made of tiny cut threads standing upright in a dense grid. The program recreates that tactile quality in the video domain, replacing the continuous pixel field with a structured grid of raised dots whose size, spacing, shading, and color palette are all under direct control.

The processing chain is compact — eight clock cycles from input to output, consuming roughly 600 LUTs and zero BRAMs. At its heart is a coordinate-space decomposition: horizontal and vertical pixel counters are masked to power-of-two cell boundaries, producing a regular grid of square cells. Within each cell, the fractional position relative to the center is computed as a Manhattan distance. Pixels closer than a threshold radius are designated as tuft pixels; those beyond it become the backing fabric. Tuft pixels receive a brightness boost, directional shading, and optional color tinting. Non-tuft pixels are slightly dimmed, creating the illusion of depth between pile and substrate.

At low density with large tuft sizes, Chenille produces bold polka-dot fields that pulse with the source video's color. At high density with small tufts, the image dissolves into a shimmering textile whose individual dots are barely distinguishable — a woven screen through which the original content is still legible. The interplay of pile height, softness, and directional lighting creates the impression of a physical surface catching light at an angle.

---

## Background

### Chenille Fabric and Pile Texture

True chenille fabric is constructed by inserting short lengths of yarn between two core threads, then cutting the pile to create a dense field of soft tufts standing perpendicular to the backing. The result is a surface with a distinctive directional sheen — run your hand one way and the pile lays flat and dark; run it the other way and the tufts stand up, catching light. This directional quality is what Chenille's shading model approximates: a signed dot product between the tuft's position offset and a configurable light-direction vector creates brighter highlights on one side of each dot and darker shadows on the other.

### Grid Quantization and Spatial Tiling

The fundamental operation behind Chenille is **spatial quantization** — dividing the continuous pixel coordinate space into discrete cells. This is the same operation used in mosaic effects, Voronoi tessellation, and halftone screening, but here the cells serve as containers for individual tuft elements rather than uniform color blocks. The program supports four tiling patterns: regular square grid, hexagonal offset (odd rows shifted by half a cell width), pseudo-random jitter, and diagonal offset. Each pattern produces a different visual rhythm — grids feel mechanical, hex feels organic, random feels chaotic, and offset feels woven.

### Manhattan Distance and Circular Approximation

Within each cell, Chenille computes the **Manhattan distance** (|dx| + |dy|) from the pixel to the cell center rather than the true Euclidean distance (√(dx² + dy²)). Manhattan distance is far cheaper in hardware — no multiplier, no square root — and produces diamond-shaped contours rather than circular ones. At small tuft sizes the diamonds read as circles to the eye; at larger sizes the faceted shape becomes part of the aesthetic, giving each tuft a gem-cut quality that reinforces the textile metaphor.

### Directional Shading and the Dot Product

The directional shading model uses a simplified **dot product** between the pixel's offset vector (dx, dy) within the cell and a global light-direction vector controlled by the Direction knob. The dot product yields a signed value: positive on the lit side, negative on the shadow side. This value is scaled by the Pile Height parameter and added to the tuft's base brightness, creating a hemisphere-like shading gradient across each dot. The effect is subtle at low pile heights and dramatic at high values, where each tuft appears to cast its own shadow.

### Halftone Screening and Dot-Matrix Printing

Chenille's dot grid has a visual kinship with **halftone screening**, the technique used in offset printing to simulate continuous tone with a pattern of variably-sized ink dots. In traditional halftoning, dot size encodes brightness; in Chenille, dot brightness and color encode the source video's pixel values. The hex pattern mode is particularly reminiscent of rotated halftone screens, which use staggered dot rows to minimize moire interference. Where halftoning reduces information to binary ink-on-paper, Chenille preserves the full tonal range within each tuft, creating a richer, more luminous result.


---

## Signal Flow

```
Input Video (YUV 4:4:4 30-bit)
│
├─ Clock 1: Input Capture + Grid Coordinate Generation ─────────
│   ├─ Latch Y, U, V, sync signals
│   ├─ Mask h_count / v_count to power-of-2 cell size
│   ├─ Compute cell-local dx, dy (fractional position)
│   └─ Apply pattern mode (grid / hex / random / offset)
│
├─ Clock 2: Distance Computation ───────────────────────────────
│   ├─ Manhattan distance = |dx| + |dy|
│   └─ Tuft test: distance < radius_thresh
│
├─ Clock 3: Tuft Color + Shading ──────────────────────────────
│   ├─ Directional shade = dot_product(dx, dy, light_dir)
│   ├─ Tuft Y = source_Y + pile_boost - (distance << soft_shift) + shade_offset
│   ├─ Tuft U/V = source_U/V + color_tint (warm / cool / source / mono)
│   └─ Non-tuft Y = source_Y - dim_offset
│
├─ Clock 4: Composite Mux ─────────────────────────────────────
│   ├─ Select tuft or non-tuft based on distance test
│   └─ Apply Color Variance modulation to chroma
│
├─ Clocks 5–8: Interpolation + Mix + Bypass ────────────────────
│   ├─ 4-stage linear interpolation (wet/dry mix via fader)
│   └─ Bypass mux (toggle_switch_11)
│
└─ Output Video (YUV 4:4:4 30-bit)
```

The pipeline's key decision happens at clock 2: the Manhattan distance test cleanly partitions every pixel into "tuft" or "backing fabric." Everything downstream — shading, color tinting, dimming — branches on that single boolean. The directional shading at clock 3 adds spatial variation *within* each tuft, giving the illusion of three-dimensional pile catching angled light. Because the grid coordinates are generated from masked pixel counters, the tiling is perfectly regular and deterministic — no frame-to-frame noise or drift unless the Animate toggle is enabled, which offsets the grid origin by a frame counter to create a gentle crawling motion.

---

## Parameter Reference

<img src={chenille_control_panel} alt="Videomancer front panel with Chenille loaded"/>
*Videomancer's front panel with Chenille active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Tuft Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the radius threshold that determines how large each tuft dot appears within its grid cell. At minimum, tufts shrink to single-pixel points barely visible against the dimmed backing. At maximum, tufts expand to fill nearly the entire cell, leaving only thin dark seams between adjacent dots. The sweet spot for a convincing chenille texture is around 40–60%, where the tufts are large enough to carry shading detail but small enough to show the grid structure.

---

#### Knob 2 — Density
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the grid cell size by selecting which power-of-two mask is applied to the pixel counters — effectively choosing between 8, 16, 32, 64, and 128-pixel cell widths. Lower values pack more tufts into the frame, creating a fine-grained textile; higher values produce large, bold dots that dominate the composition. At very high density the individual tufts blur into a shimmering screen, and at very low density each dot becomes an isolated island of color.

---

#### Knob 3 — Pile Hght
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Governs the brightness boost applied to tuft pixels relative to the backing fabric, simulating the way raised pile catches more ambient light than the flat substrate. At zero, tufts and backing have equal brightness and the texture is nearly invisible. As Pile Height increases, tufts glow brighter while the surrounding fabric recedes, creating a pronounced embossed quality. This parameter also scales the directional shading amplitude — higher pile means more dramatic light-to-shadow contrast across each dot.

---

#### Knob 4 — Direction
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Rotates the virtual light source around each tuft by setting the angle of the (dx, dy) dot-product vector. At the leftmost position, light arrives from the left; at center, from above; at the rightmost position, from the right. The shading effect is most visible when Pile Height is moderate to high and Shading is set to Lit mode. Sweeping Direction while watching a field of tufts creates a convincing illusion of a light source orbiting the fabric surface.

---

#### Knob 5 — Color Var
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds chroma modulation to the tuft color, introducing slight hue and saturation variation between adjacent tufts. At zero, all tufts carry the exact color of their source pixel. As Color Variance increases, a position-dependent offset is added to U and V, creating the subtle color irregularity found in real dyed textiles where adjacent yarn bundles absorb dye slightly differently.

---

#### Knob 6 — Softness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how sharply the tuft brightness falls off toward its edges. At minimum softness, tufts have hard, crisp boundaries — each dot is a uniform disc of color with an abrupt edge. As Softness increases, the brightness rolls off gradually from center to perimeter, creating a pillowed, rounded appearance. The underlying mechanism is a left-shift applied to the distance value before subtracting it from the pile boost — more shift means faster falloff per pixel of distance.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Grid | Hex |
| **8 — Color** | Mono | Warm |
| **9 — Shading** | Flat | Lit |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into three functional groups: visual style (Pattern and Color select the tiling geometry and color palette), rendering mode (Shading and Animate control lighting model and motion), and signal routing (Bypass). Pattern and Color are four-position selectors decoded from two bits each; Shading, Animate, and Bypass are simple on/off switches.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the processed chenille texture and the original video signal. At 100%, the output is fully processed — tufts, shading, and color tinting are all visible. As the fader descends toward 0%, the original video increasingly shows through, blending with the textured version. Intermediate positions create a ghostly overlay effect where the grid of tufts is visible but the original image detail is still readable beneath.

---

## Guided Exercises

These three exercises move from basic grid exploration through directional shading to full textile synthesis, building familiarity with each control layer before combining them.

### Exercise 1: Dot Grid Fundamentals

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: chenille_source1_kodim15, after: chenille_exercise1_result },
    { label: "Kodim03", before: chenille_source2_kodim03, after: chenille_exercise1_result },
    { label: "Kodim13 B&W", before: chenille_source3_kodim13_bw, after: chenille_exercise1_result },
  ]}
/>
*Dot Grid Fundamentals — simulated result across source images.*
**Source**: A live camera feed or any footage with recognizable mid-tone content — avoid very dark or very bright material.

**Objective**: Understand how Tuft Size, Density, and Softness interact to define the basic chenille texture grid.

1. **Reveal the grid**: Set Density to ~40% and Tuft Size to ~50%. A regular grid of dots should appear over the source video.
2. **Size vs. density**: Sweep Tuft Size from minimum to maximum while watching how the dots grow and shrink within their cells. Then sweep Density to change the cell size itself.
3. **Edge softness**: With tufts at a medium size, sweep Softness from 0% to 100%. Observe the dots transition from hard-edged discs to soft, pillowed circles.
4. **Pattern modes**: Cycle through Grid, Hex, Random, and Offset on the Pattern toggle. Note how the tiling structure changes the overall rhythm.
5. **Mix**: Use the fader to blend the textured output with the original. Find a point where the grid is clearly visible but the source content remains legible.

**Key concepts**: Manhattan distance defines tuft shape, power-of-two cell masking creates the grid, softness shift controls edge falloff rate

---

### Exercise 2: Directional Shading and Pile Height

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: chenille_source1_kodim15, after: chenille_exercise2_result },
    { label: "Kodim03", before: chenille_source2_kodim03, after: chenille_exercise2_result },
    { label: "Kodim13 B&W", before: chenille_source3_kodim13_bw, after: chenille_exercise2_result },
  ]}
/>
*Directional Shading and Pile Height — simulated result across source images.*
**Source**: Portrait or still life with smooth tonal gradients and soft lighting.

**Objective**: Explore the directional shading model and how Pile Height controls the three-dimensional illusion.

1. **Enable lighting**: Set Shading to Lit. With Pile Height low, the effect is subtle.
2. **Raise the pile**: Slowly increase Pile Hght from 0% to ~70%. Watch each dot develop a highlight-to-shadow gradient.
3. **Rotate the light**: Sweep Direction from left to right. The bright side of each tuft migrates around the dot, creating the impression of a moving light source.
4. **High pile drama**: Push Pile Hght to ~90% and observe the extreme contrast between lit and shadowed halves of each tuft.
5. **Hex + lit**: Switch Pattern to Hex. The staggered honeycomb layout makes the directional shading feel more organic and less mechanical.
6. **Flat vs. lit**: Toggle Shading between Flat and Lit to compare the uniform dot field against the three-dimensional version.

**Key concepts**: Dot product encodes light direction, pile height scales shading amplitude, hex tiling softens geometric rigidity

---

### Exercise 3: Animated Textile Synthesis

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: chenille_source1_kodim15, after: chenille_exercise3_result },
    { label: "Kodim03", before: chenille_source2_kodim03, after: chenille_exercise3_result },
    { label: "Kodim13 B&W", before: chenille_source3_kodim13_bw, after: chenille_exercise3_result },
  ]}
/>
*Animated Textile Synthesis — simulated result across source images.*
**Source**: Saturated, high-contrast footage — color bars, graphics, or the macaw image.

**Objective**: Combine color tinting, animation, and all shading parameters to create a living textile surface.

1. **Warm palette**: Set Color to Warm and observe how tufts take on an amber glow regardless of source color.
2. **Cool contrast**: Switch to Cool for a cyan-blue tint. Compare the emotional quality of warm vs. cool.
3. **Color variance**: Increase Color Var to ~60%. Adjacent tufts now shimmer with slightly different hues, like hand-dyed yarn.
4. **Start animation**: Toggle Animate to On. The grid begins to drift, creating a crawling textile motion.
5. **Full composition**: Set Pattern to Hex, Shading to Lit, Pile Hght to ~50%, Direction to ~40%. Let the animation run and observe how the moving lit tufts create a shimmering, fabric-like surface.
6. **Mix down**: Lower the fader to ~60% to blend the animated textile with the original video.

**Key concepts**: Color toggle selects chroma bias, color variance adds per-tuft dye variation, animation offsets grid origin per frame, mix blends processed and original

---


## Tips

- **Hex for realism**: The hexagonal tiling mode produces the most fabric-like result because it eliminates the rigid horizontal and vertical seams of the square grid. Use it as the default starting point.
- **Softness shapes the character**: Even small adjustments to Softness dramatically change the feel — hard edges read as mechanical dots, soft edges read as plush pile. Start around 40% and adjust to taste.
- **Pile Height and Shading are partners**: Pile Height has minimal visual impact in Flat mode. Switch to Lit mode before adjusting it, so the brightness boost is shaped into a convincing directional gradient.
- **Color Variance for textile realism**: Real dyed fabrics never have perfectly uniform color. Even a small amount of Color Variance (10–20%) adds the subtle dye-lot variation that makes the texture feel handmade.
- **Low density for bold dots**: Setting Density below 30% creates large, isolated dots that work well as a graphic overlay — almost like a Ben-Day dot screen from comic book printing.
- **Animate for living fabric**: The animation drift is subtle by design. It works best in combination with Lit shading, where the moving grid creates shimmering highlight patterns as tufts pass under the virtual light source.
- **Mix for compositing**: Rather than using Chenille as a full replacement, try mixing at 50–70% to create a translucent textile layer over the source video — the original content shows through the gaps in the tuft grid.
- **Bypass is your friend**: Use the Bypass toggle frequently to compare the textured output against the original. The eye adapts quickly to the dot grid, and periodic A/B checks keep your adjustments honest.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory blocks within an FPGA used for look-up tables, line buffers, and data storage. |
| **Dot product** | A mathematical operation that multiplies corresponding components of two vectors and sums the results, used here to compute directional shading across each tuft. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that implements the video processing pipeline in hardware. |
| **Halftone** | A printing technique that simulates continuous tone using a grid of variably-sized dots, visually related to Chenille's dot-grid texture. |
| **LUT** | Look-Up Table; a pre-computed array that maps input values to output values, enabling fast function evaluation in hardware. |
| **Manhattan distance** | A distance metric computed as |dx| + |dy|, producing diamond-shaped contours rather than circles; used to determine tuft boundaries. |
| **Moire** | An interference pattern produced when two regular grids overlap at slightly different scales or angles. |
| **Pile** | In textiles, the raised surface of cut or looped fibers standing upright from a backing fabric; the physical phenomenon Chenille's shading model simulates. |
| **Spatial quantization** | The process of dividing a continuous coordinate space into discrete cells, each treated as an independent unit for processing. |
| **Voronoi tessellation** | A partition of a plane into regions based on proximity to a set of seed points, related to Chenille's cell-based grid decomposition. |
| **YUV** | A color space that separates luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |

---
