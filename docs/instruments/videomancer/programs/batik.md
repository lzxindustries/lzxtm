---
draft: true
sidebar_position: 15
slug: /instruments/videomancer/batik
title: "Batik"
image: /img/instruments/videomancer/batik/batik_hero_s1.png
description: "Batik simulates the centuries-old Indonesian wax-resist textile dyeing technique in the video domain."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import batik_control_panel from '/img/instruments/videomancer/batik/batik_control_panel.png';
import batik_source1_house from '/img/instruments/videomancer/batik/batik_source1_house.png';
import batik_source2_parrot from '/img/instruments/videomancer/batik/batik_source2_parrot.png';
import batik_source3_clouds from '/img/instruments/videomancer/batik/batik_source3_clouds.png';
import batik_source4_pattern from '/img/instruments/videomancer/batik/batik_source4_pattern.png';
import batik_source5_man from '/img/instruments/videomancer/batik/batik_source5_man.png';
import batik_source6_berries from '/img/instruments/videomancer/batik/batik_source6_berries.png';
import batik_hero_s1 from '/img/instruments/videomancer/batik/batik_hero_s1.png';
import batik_hero_s2 from '/img/instruments/videomancer/batik/batik_hero_s2.png';
import batik_hero_s3 from '/img/instruments/videomancer/batik/batik_hero_s3.png';
import batik_hero_s4 from '/img/instruments/videomancer/batik/batik_hero_s4.png';
import batik_hero_s5 from '/img/instruments/videomancer/batik/batik_hero_s5.png';
import batik_hero_s6 from '/img/instruments/videomancer/batik/batik_hero_s6.png';
import batik_ex1_s1 from '/img/instruments/videomancer/batik/batik_ex1_s1.png';
import batik_ex1_s2 from '/img/instruments/videomancer/batik/batik_ex1_s2.png';
import batik_ex1_s3 from '/img/instruments/videomancer/batik/batik_ex1_s3.png';
import batik_ex1_s4 from '/img/instruments/videomancer/batik/batik_ex1_s4.png';
import batik_ex1_s5 from '/img/instruments/videomancer/batik/batik_ex1_s5.png';
import batik_ex1_s6 from '/img/instruments/videomancer/batik/batik_ex1_s6.png';
import batik_ex2_s1 from '/img/instruments/videomancer/batik/batik_ex2_s1.png';
import batik_ex2_s2 from '/img/instruments/videomancer/batik/batik_ex2_s2.png';
import batik_ex2_s3 from '/img/instruments/videomancer/batik/batik_ex2_s3.png';
import batik_ex2_s4 from '/img/instruments/videomancer/batik/batik_ex2_s4.png';
import batik_ex2_s5 from '/img/instruments/videomancer/batik/batik_ex2_s5.png';
import batik_ex2_s6 from '/img/instruments/videomancer/batik/batik_ex2_s6.png';
import batik_ex3_s1 from '/img/instruments/videomancer/batik/batik_ex3_s1.png';
import batik_ex3_s2 from '/img/instruments/videomancer/batik/batik_ex3_s2.png';
import batik_ex3_s3 from '/img/instruments/videomancer/batik/batik_ex3_s3.png';
import batik_ex3_s4 from '/img/instruments/videomancer/batik/batik_ex3_s4.png';
import batik_ex3_s5 from '/img/instruments/videomancer/batik/batik_ex3_s5.png';
import batik_ex3_s6 from '/img/instruments/videomancer/batik/batik_ex3_s6.png';

# Batik

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "House", before: batik_source1_house, after: batik_hero_s1 },
    { label: "Parrot", before: batik_source2_parrot, after: batik_hero_s2 },
    { label: "Clouds", before: batik_source3_clouds, after: batik_hero_s3 },
    { label: "Pattern", before: batik_source4_pattern, after: batik_hero_s4 },
    { label: "Man", before: batik_source5_man, after: batik_hero_s5 },
    { label: "Berries", before: batik_source6_berries, after: batik_hero_s6 },
  ]}
/>
*Wax-resist crackle veins fracture a portrait into dye-limited Voronoi cells, echoing the layered resist-and-dye process of Javanese batik cloth.*

---

## Overview

Batik simulates the centuries-old Indonesian wax-resist textile dyeing technique in the video domain. The program generates a crackle vein network — dark boundary lines that recall the characteristic cracks formed when molten wax dries and fractures on cloth — and overlays it on a palette-quantised version of the input video. The result resembles hand-dyed fabric where each region between wax cracks holds a limited range of dye colours.

The crackle pattern is produced by a pseudo-Voronoi cell algorithm seeded from a free-running LFSR. For every pixel, the hardware divides the frame into coarse rectangular regions and hashes the region coordinates to create a pseudo-random cell centre. Chebyshev distance to the nearest cell boundary determines whether a pixel falls on a dark vein or inside a cell body. Cell bodies receive palette-quantised luma (reducing brightness to 2–64 discrete levels like limited dye baths) and hue-rotated chroma to simulate indigo, ochre, or earth-tone palettes.

The name references *batik tulis*, the hand-drawn Javanese method where artisans apply hot wax with a copper stylus called a *canting*, dip the cloth in dye, then crack and re-wax in successive layers. Batik's digital version compresses this multi-step resist-dye-crack cycle into a single real-time video pass.

---

## Quick Start

1. **Dense for close-ups, Sparse for wide shots**: Fine crackle works best when the subject fills the frame; large cells suit wide compositions where the vein pattern reads as architectural structure.
2. **Dye Depth and Palette together set the aesthetic**: Low Dye Depth with a warm Palette creates a two-tone sepia batik; high Dye Depth with a cool Palette gives detailed indigo cloth.
3. **Use Crackle as a presence control**: Set Wax Amt for the desired vein darkness, then use Crackle to fade the overlay in and out without changing the vein geometry.

---

## Background

### What Is Batik?

Batik is a textile dyeing technique originating in Java, Indonesia, where hot wax is applied to fabric as a resist before immersion in dye. Areas covered by wax remain undyed. The wax inevitably cracks, allowing thin lines of dye to seep through — these "crackle" veins are the hallmark of authentic batik. The process is repeated with different wax patterns and dye colours to build up complex multi-layered designs. UNESCO recognised Indonesian batik as an Intangible Cultural Heritage of Humanity in 2009.

### Voronoi Cells and Distance Fields

A Voronoi diagram partitions a plane into regions based on proximity to a set of seed points — every point in a region is closer to its seed than to any other. The boundaries between regions form a network of edges. Batik approximates this by dividing the frame into coarse grid regions, hashing the coordinates to generate a pseudo-random "seed" position within each cell, then computing the Chebyshev distance (maximum of horizontal and vertical displacement) from each pixel to its cell boundary. Pixels near a boundary fall on a vein; pixels deep inside a cell receive the dyed colour.

### Palette Quantisation

Traditional batik fabric typically uses only a few dye colours per layer — sometimes as few as two (indigo and white) in the simplest *batik cap* stamps. The program mimics this constraint by reducing the 10-bit luma channel to a small number of discrete levels via bit-shifting. At the lowest setting, only 2 brightness levels survive; at the highest, 64 levels preserve most of the original tonal detail. This staircase effect creates the flat colour fields characteristic of dyed cloth.

### Hue Rotation as Dye Palette

Rather than replacing colours entirely, the hue rotation stage shifts the U and V chroma channels by an offset derived from the Palette knob. This rotates the original image's colour wheel, transforming naturalistic colours into the earthy indigos, ochres, and greens typical of traditional batik cloth. The rotation is additive on U and subtractive on V (or vice versa), maintaining colour saturation while changing hue.

### LFSR-Based Procedural Noise

The crackle pattern's randomness comes from a 16-bit linear feedback shift register (LFSR) running continuously at the pixel clock. The LFSR's current state is XORed with the current grid region's coordinates to produce a unique hash per cell. When animation is enabled, the frame counter is mixed into the hash as well, causing the cell pattern to evolve every frame. The result is a deterministic but visually random texture that tiles seamlessly across the frame.


---

## Signal Flow

```
                                  ┌──────────────┐
data_in ─────────────────────────►│ Input Reg     │
                                  │ + Position    │
                                  │   Counters    │
                                  └──────┬────────┘
                                         │ Stage 1
                                         ▼
                               ┌─────────────────────┐
                               │ Cell Hash (LFSR XOR  │
                               │  region coords) +    │
                               │  Chebyshev Distance  │
                               │  → Vein Test         │
                               └──────────┬──────────┘
                                          │ Stage 2
                                          ▼
                               ┌─────────────────────┐
                               │ Luma Quantise        │
                               │ (shift-reduce 2–64   │
                               │  levels) + Vein Dark │
                               └──────────┬──────────┘
                                          │ Stage 3
                                          ▼
                               ┌─────────────────────┐
                               │ Hue Rotation (U/V    │
                               │ offset by Palette)   │
                               │ + Vein Diff          │
                               └──────────┬──────────┘
                                          │ Stage 4
                                          ▼
                               ┌─────────────────────┐
                               │ Opacity Multiply     │
                               │ (Wax Amt × vein      │
                               │  difference)         │
                               └──────────┬──────────┘
                                          │ Stage 5
                                          ▼
                               ┌─────────────────────┐
                               │ Vein Subtract +      │
                               │ Clamp + Mono Mode    │
                               └──────────┬──────────┘
                                          │ Stage 6
                                          ▼
data_in ──► [sync delay] ──► dry ──► Interpolator ◄── wet
                                       (4 clk)
                                          │
                                          ▼
                                      data_out
```

The pipeline splits into two parallel paths after input: the processing path computes the crackle overlay and palette quantisation, while the sync delay path preserves the original data for the final wet/dry mix. The cell hash in Stage 2 is the critical creative step — it converts deterministic pixel coordinates into a pseudo-random cell boundary distance that drives the entire vein pattern. Stages 3 through 6 progressively shape how those veins appear: quantized colour in the cell bodies, hue-shifted chroma for dye palette simulation, and opacity-controlled darkening along the crack boundaries.

The Mono mode switch bypasses hue rotation entirely, forcing U and V to neutral 512 — this produces the monochrome indigo-and-white look of traditional *batik tulis* in its simplest form.

---

## Parameter Reference

<img src={batik_control_panel} alt="Videomancer front panel with Batik loaded"/>
*Videomancer's front panel with Batik active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 4 – 64 |
| Default | 27 |

Controls the spatial scale of the Voronoi cell grid. The pot value is mapped through a threshold decoder that selects one of three cell sizes, with the Dense/Sparse toggle determining the range. In Dense mode, cells range from 8 to 32 pixels; in Sparse mode, from 32 to 128 pixels. Smaller cells create a fine, intricate crackle network reminiscent of aged wax; larger cells produce bold, architectural vein patterns. At the smallest sizes the pattern becomes a dense mesh of dark lines with tiny colour patches between them.

---

#### Knob 2 — Vein Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Sets the width of the dark crackle veins. The pot value is scaled to an 8-bit threshold that determines how close to a cell boundary a pixel must be before it is classified as a vein pixel. At minimum, only the thinnest hairline cracks appear — a subtle texture overlay. At maximum, veins grow wide enough to dominate the image, leaving only small islands of dyed colour. Mid-range settings around 40% produce the most natural-looking crackle patterns reminiscent of actual wax fractures.

---

#### Knob 3 — Dye Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the luma quantisation depth, simulating the limited number of dye colours available in a traditional batik process. The pot maps to six discrete quantisation levels: 2, 4, 8, 16, 32, or 64 brightness steps. At the lowest setting (2 levels), the image becomes a stark two-tone design; at the highest (64 levels), colour transitions remain fairly smooth. The quantisation is applied via shift-right then shift-left, which truncates the least-significant bits and creates the characteristic flat colour banding of dyed fabric.

---

#### Knob 4 — Palette
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 1 |

Rotates the chroma hue by adding a signed offset to U and subtracting it from V. At the center position (512), no rotation occurs and original colours are preserved. Turning counter-clockwise shifts toward cool indigo and blue tones; turning clockwise shifts toward warm ochre and brown tones. The eight steps on this knob give you eight distinct dye palettes, each evoking a different regional batik tradition — Javanese indigo, Balinese earth tones, or Pekalongan coastal colours.

---

#### Knob 5 — Wax Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the darkness of the crackle veins. The hardware computes a brightness target by multiplying the source luma by `(1023 - darkness) / 1024`. At minimum (0%), veins are jet black regardless of the underlying image. At maximum, veins are barely darker than the surrounding dyed area. This parameter interacts with Crackle (Pot 6): Wax Amt sets the *difference* between vein and non-vein pixels, while Crackle controls how much of that difference actually appears in the final composite via opacity multiplication.

---

#### Knob 6 — Crackle
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scales the vein darkening effect via an opacity multiplication stage. The computed vein brightness reduction is multiplied by this value before being subtracted from the quantised luma. At 0%, even pixels classified as veins receive no darkening — the crackle pattern is invisible. At 100%, the full computed reduction is applied. This works as a "presence" control for the crackle texture, letting you dial in anything from a barely-visible surface grain to bold, high-contrast fracture lines.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Dye Mode** | Natural | Dark |
| **8 — Wax Show** | Off | On |
| **9 — Video Dye** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent aspects of the batik simulation. Toggle 7 selects Dense or Sparse cell grids, fundamentally changing the crackle scale. Toggle 8 switches between full-colour and monochrome (desaturated) output. Toggle 9 enables frame-by-frame animation of the crackle pattern. Toggle 10 inverts the vein/cell classification so that cell interiors become dark and vein boundaries become bright. Toggle 11 bypasses all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) and wet (processed) signal at the output stage using three parallel interpolators. At 0% the output is the unmodified input; at 100% the output is fully processed batik. Intermediate values blend the crackle overlay with the source, useful for creating subtle textile texture overlays on live video.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Batik processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises progress from basic crackle generation to full batik simulation with palette control and animation.

### Exercise 1: Simple Crackle Overlay

<BeforeAfterSlider
  sources={[
    { label: "House", before: batik_source1_house, after: batik_ex1_s1 },
    { label: "Parrot", before: batik_source2_parrot, after: batik_ex1_s2 },
    { label: "Clouds", before: batik_source3_clouds, after: batik_ex1_s3 },
    { label: "Pattern", before: batik_source4_pattern, after: batik_ex1_s4 },
    { label: "Man", before: batik_source5_man, after: batik_ex1_s5 },
    { label: "Berries", before: batik_source6_berries, after: batik_ex1_s6 },
  ]}
/>
*Simple Crackle Overlay — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects.

**What You'll Create**: Understand how Voronoi cell geometry creates a crackle vein pattern and how vein parameters control its appearance.

1. **Base crackle**: Set Cell Size to the middle position, Vein Width to about 40%, and Crackle to 80%. A visible crackle network should appear over the source video.
2. **Cell size**: Sweep Cell Size from minimum to maximum. Watch the veins go from a dense mesh to a wide geometric grid.
3. **Vein width**: With Cell Size at a moderate setting, increase Vein Width. The dark lines grow thicker until they dominate most of the frame.
4. **Darkness**: Reduce Wax Amt to 30%. The veins become faint, barely-visible hairlines. Return to 80% for bold cracks.
5. **Opacity**: Now sweep Crackle. At 0% the veins vanish entirely even though they're being computed; at 100% the full darkening is applied.
6. **Invert**: Toggle Animate off, then enable Invert. The crackle network becomes a bright wireframe on a darkened field.

**Key concepts**: Cell size sets the grid scale, Vein Width sets the boundary thickness, Wax Amt and Crackle together control vein visibility, Invert flips the vein/cell relationship

---

### Exercise 2: Dye Palette Exploration

<BeforeAfterSlider
  sources={[
    { label: "House", before: batik_source1_house, after: batik_ex2_s1 },
    { label: "Parrot", before: batik_source2_parrot, after: batik_ex2_s2 },
    { label: "Clouds", before: batik_source3_clouds, after: batik_ex2_s3 },
    { label: "Pattern", before: batik_source4_pattern, after: batik_ex2_s4 },
    { label: "Man", before: batik_source5_man, after: batik_ex2_s5 },
    { label: "Berries", before: batik_source6_berries, after: batik_ex2_s6 },
  ]}
/>
*Dye Palette Exploration — simulated result across source images.*
**Source**: Footage with varied colours — flowers, fabrics, or colourful scenery.

**What You'll Create**: Explore palette quantisation and hue rotation for traditional dye effects.

1. **Reduce dye levels**: Set Dye Depth low (around 20%). Watch the image snap to just a few brightness levels, like a two-colour dye bath.
2. **Increase gradually**: Sweep Dye Depth upward. More tonal steps appear, from stark two-tone through 4, 8, 16, 32, to nearly full-range at 64 levels.
3. **Rotate palette**: With Dye Depth at about 40% (8 levels), sweep the Palette knob. Watch the colours shift through indigo, ochre, green, and magenta ranges.
4. **Monochrome**: Enable Wax Show (Toggle 8). All colour drops out, leaving only quantised luminance — a monochrome batik.
5. **Combine with crackle**: Return to colour mode and set moderate crackle (Vein Width ~35%, Crackle ~70%). The crackle veins now overlay the dye-limited palette.

**Key concepts**: Dye Depth controls quantisation levels, Palette rotates the colour wheel to simulate different dye traditions, monochrome mode removes chroma for single-dye effects

---

### Exercise 3: Animated Textile

<BeforeAfterSlider
  sources={[
    { label: "House", before: batik_source1_house, after: batik_ex3_s1 },
    { label: "Parrot", before: batik_source2_parrot, after: batik_ex3_s2 },
    { label: "Clouds", before: batik_source3_clouds, after: batik_ex3_s3 },
    { label: "Pattern", before: batik_source4_pattern, after: batik_ex3_s4 },
    { label: "Man", before: batik_source5_man, after: batik_ex3_s5 },
    { label: "Berries", before: batik_source6_berries, after: batik_ex3_s6 },
  ]}
/>
*Animated Textile — simulated result across source images.*
**Source**: Slow-moving footage or a static scene.

**What You'll Create**: Create a living textile effect using crackle animation and full batik processing.

1. **Set base look**: Cell Size ~50%, Vein Width ~30%, Dye Depth ~50%, Palette ~25%, Wax Amt ~70%, Crackle ~80%.
2. **Enable animation**: Toggle Animate on. The crackle pattern shifts every frame, creating a shimmering organic texture.
3. **Dense mode**: Switch to Dense crackle via Dye Mode toggle. The fine mesh shimmer creates a living-fabric aesthetic.
4. **Mix for subtlety**: Reduce Mix to about 60%. The batik texture now blends gently with the source, creating a translucent textile overlay.
5. **Invert for glow**: Enable Invert. The animated crackle becomes a pulsing neon wireframe over the darkened source.
6. **Explore density**: Toggle Dense/Sparse while animation runs. Dense creates rapid, fine-grained shimmer; Sparse creates slow, architectural movement.

**Key concepts**: Animation XORs the frame counter into the hash seed, producing per-frame variation, Mix blending creates textile overlay effects, Dense vs Sparse changes the temporal character of animation

---


## Tips

- **Animation + feedback loops**: Route the output back to the input while Animate is on for evolving, self-referencing batik patterns.
- **Monochrome + low Dye Depth = woodblock print**: Enabling Mono with only 2–4 quantisation levels produces a stark black-and-white graphic reminiscent of Japanese woodblock prints.
- **Mix for overlay compositing**: Set Mix to 30–50% to blend the batik texture gently over source video, creating a translucent textile filter effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chebyshev distance** | A distance metric where the distance between two points is the greater of their horizontal and vertical separations; used here for cell boundary detection. |
| **Chrominance** | The color-difference components (U and V) of a YUV video signal, separate from luminance. |
| **Crackle** | The network of fine lines in traditional batik cloth caused by dye seeping through cracks in the wax resist layer. |
| **Hue rotation** | Shifting U and V chroma values by a signed offset to change perceived color without altering brightness or saturation. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input is a linear function of its previous state, producing a deterministic pseudo-random bit sequence. |
| **Luminance** | The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color. |
| **Palette quantisation** | Reducing a full-range luminance signal to a small number of discrete levels, simulating the limited dye colours of textile printing. |
| **Voronoi diagram** | A spatial partition where each region contains all points closer to one seed than to any other, producing a network of cell boundaries. |
| **Wax resist** | A dyeing technique where areas coated with wax repel dye, preserving the original fabric colour beneath. |
| **XOR** | Exclusive OR; a bitwise logic operation that outputs 1 when its two inputs differ, used here to mix the frame counter into the hash seed. |

---
