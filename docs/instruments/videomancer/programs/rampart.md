---
draft: true
sidebar_position: 240
slug: /instruments/videomancer/rampart
title: "Rampart"
image: /img/instruments/videomancer/rampart/rampart_hero_s1.png
description: "Every castle begins with a wall."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import rampart_control_panel from '/img/instruments/videomancer/rampart/rampart_control_panel.png';
import rampart_source1_field from '/img/instruments/videomancer/rampart/rampart_source1_field.png';
import rampart_source2_runner from '/img/instruments/videomancer/rampart/rampart_source2_runner.png';
import rampart_source3_clouds from '/img/instruments/videomancer/rampart/rampart_source3_clouds.png';
import rampart_source4_pattern from '/img/instruments/videomancer/rampart/rampart_source4_pattern.png';
import rampart_source5_woman from '/img/instruments/videomancer/rampart/rampart_source5_woman.png';
import rampart_source6_wood from '/img/instruments/videomancer/rampart/rampart_source6_wood.png';
import rampart_hero_s1 from '/img/instruments/videomancer/rampart/rampart_hero_s1.png';
import rampart_hero_s2 from '/img/instruments/videomancer/rampart/rampart_hero_s2.png';
import rampart_hero_s3 from '/img/instruments/videomancer/rampart/rampart_hero_s3.png';
import rampart_hero_s4 from '/img/instruments/videomancer/rampart/rampart_hero_s4.png';
import rampart_hero_s5 from '/img/instruments/videomancer/rampart/rampart_hero_s5.png';
import rampart_hero_s6 from '/img/instruments/videomancer/rampart/rampart_hero_s6.png';
import rampart_ex1_s1 from '/img/instruments/videomancer/rampart/rampart_ex1_s1.png';
import rampart_ex1_s2 from '/img/instruments/videomancer/rampart/rampart_ex1_s2.png';
import rampart_ex1_s3 from '/img/instruments/videomancer/rampart/rampart_ex1_s3.png';
import rampart_ex1_s4 from '/img/instruments/videomancer/rampart/rampart_ex1_s4.png';
import rampart_ex1_s5 from '/img/instruments/videomancer/rampart/rampart_ex1_s5.png';
import rampart_ex1_s6 from '/img/instruments/videomancer/rampart/rampart_ex1_s6.png';
import rampart_ex2_s1 from '/img/instruments/videomancer/rampart/rampart_ex2_s1.png';
import rampart_ex2_s2 from '/img/instruments/videomancer/rampart/rampart_ex2_s2.png';
import rampart_ex2_s3 from '/img/instruments/videomancer/rampart/rampart_ex2_s3.png';
import rampart_ex2_s4 from '/img/instruments/videomancer/rampart/rampart_ex2_s4.png';
import rampart_ex2_s5 from '/img/instruments/videomancer/rampart/rampart_ex2_s5.png';
import rampart_ex2_s6 from '/img/instruments/videomancer/rampart/rampart_ex2_s6.png';
import rampart_ex3_s1 from '/img/instruments/videomancer/rampart/rampart_ex3_s1.png';
import rampart_ex3_s2 from '/img/instruments/videomancer/rampart/rampart_ex3_s2.png';
import rampart_ex3_s3 from '/img/instruments/videomancer/rampart/rampart_ex3_s3.png';
import rampart_ex3_s4 from '/img/instruments/videomancer/rampart/rampart_ex3_s4.png';
import rampart_ex3_s5 from '/img/instruments/videomancer/rampart/rampart_ex3_s5.png';
import rampart_ex3_s6 from '/img/instruments/videomancer/rampart/rampart_ex3_s6.png';

# Rampart

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: rampart_source1_field, after: rampart_hero_s1 },
    { label: "Runner", before: rampart_source2_runner, after: rampart_hero_s2 },
    { label: "Clouds", before: rampart_source3_clouds, after: rampart_hero_s3 },
    { label: "Pattern", before: rampart_source4_pattern, after: rampart_hero_s4 },
    { label: "Woman", before: rampart_source5_woman, after: rampart_hero_s5 },
    { label: "Wood", before: rampart_source6_wood, after: rampart_hero_s6 },
  ]}
/>
*Rampart generating a fortress-wall brick lattice with running bond, mortar shadowing, and video-filled crenellations over a live input.*

---

## Overview

Every castle begins with a wall. Rampart builds one from arithmetic — a tiled grid of rectangular bricks, mortared joints, and crenellated parapets, all synthesized entirely from pixel coordinates. The program treats the screen as a masonry surface: each pixel's horizontal and vertical position is reduced modulo the brick dimensions to determine whether it lies on a brick face, a mortar line, or a crenel gap. The result is a dense architectural lattice that can overlay, replace, or modulate the input video.

The name evokes the fortified outer wall of a castle — a rampart — and the program's visual output mirrors that structure. Bricks tile the screen in a periodic grid, optionally staggered in a running-bond pattern. A configurable row of crenellations crowns the top edge with the distinctive tooth-shaped profile of a battlement. Mortar lines between bricks can carry shadow, and each brick's surface can be filled with the live video signal or a flat color.

A critical ABI boundary bug limits the program's hardware interface. The VHDL attempts to read registers 8 through 11, which fall outside the Videomancer's 8-register ABI (indices 0–7). These out-of-bounds reads always return zero. Since all six potentiometers, all five toggles, and the mix fader are correctly mapped within registers 0–7, the bug does not disable any user-facing controls — it only means any features that were intended to use registers 8–11 are inoperative. The core brick, mortar, crenellation, and video-fill functionality works as designed.

---

## Quick Start

1. **Start with mortar**: The mortar lines are the strongest visual element of the grid. Set Mortar width and brightness first, then adjust brick dimensions around it.
2. **Running bond is more natural**: Real walls almost always use running bond. Stack bond creates a rigid, digital-looking grid; running bond adds visual rhythm and authenticity.
3. **Video fill as mosaic**: With video fill active and moderate brick sizes, Rampart acts as a mosaic filter — the source image is visible but fractured into rectangular tiles.

---

## Background

### Brick Bonding in Architecture

Real masonry walls use specific arrangements of bricks called *bonds*. The simplest is the **stack bond**, where every row aligns vertically — each brick sits directly above the one below. This creates clean vertical columns but is structurally weak because the vertical joints form continuous fault lines. The **running bond** (also called stretcher bond) offsets every other row by half a brick width, staggering the joints like a typical house wall. Rampart implements both: the Bond toggle switches between stack alignment and half-width stagger.

### Modular Arithmetic in Pixel Grids

The foundation of Rampart's grid is modular arithmetic. For any pixel at coordinates (h, v), the position within its local brick is `(h mod block_w, v mod block_h)`. When the local position falls near the edge of the brick — within the mortar threshold — the pixel is classified as mortar rather than brick surface. This is the same technique used in shader programming to create tiling patterns: a single brick definition repeats infinitely across the screen through the modulo operation.

### Crenellations and Battlements

The distinctive tooth-shaped top edge of a medieval fortress wall is called a *crenellation* or *battlement*. The raised portions (merlons) alternate with gaps (crenels) along the parapet. Rampart creates this pattern by defining a rectangular cutout region at the top of the screen. Within this region, a secondary horizontal modulo operation alternates between solid (merlon) and empty (crenel) zones, with the height and width of the crenels independently controllable.

### Video Fill and Texture Mapping

Each brick in the grid can be rendered as a flat color or filled with the live video signal. Video fill is a simple form of texture mapping — rather than a flat value, the brick surface takes its color from whatever video content happens to underlie that pixel position. This creates a stained-glass or mosaic effect where recognizable video content is visible within each brick tile, framed by mortar lines.

### Shadow and Depth Cues

Mortar lines in real masonry are typically recessed below the brick face, creating thin shadow lines that give the wall a sense of depth. Rampart simulates this by darkening pixels classified as mortar when the Shadow toggle is active. The darkening is applied as a multiplicative reduction — mortar pixels have their brightness scaled down rather than replaced with black, preserving some of the underlying video or color information.


---

## Signal Flow

Position Analysis → Crenellation → Surface Rendering → Compositing → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Position Analysis ──────────────────────────────────────────
│   ├─ 1. Compute (h mod block_w, v mod block_h)
│   ├─ 2. Running bond offset: odd rows shift by block_w / 2
│   └─ 3. Mortar detection: local_x < mortar OR local_y < mortar
│
├── Crenellation ───────────────────────────────────────────────
│   ├─ 4. Top-row check: v < crenel_h
│   └─ 5. Periodic cutout: (h mod (crenel_w * 2)) >= crenel_w
│
├── Surface Rendering ─────────────────────────────────────────
│   ├─ 6. Brick face: video fill (input YUV) or flat mid-gray
│   ├─ 7. Mortar: mortar brightness value (flat gray)
│   └─ 8. Shadow: darken mortar pixels (multiplicative)
│
├── Compositing ────────────────────────────────────────────────
│   └─ 9. Mix interpolator: wet/dry crossfade (3x interpolator_u)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The grid is computed entirely from pixel coordinates — no BRAMs or line buffers are needed. The modular arithmetic for brick boundaries, the stagger offset for running bond, and the rectangular crenellation test are all combinational logic gated by the pixel clock. The mortar detection is a simple threshold comparison on the local position within each brick tile. When Video Fill is active, brick pixels pass the input video through unchanged; when inactive, they receive a flat mid-gray. The Mix fader crossfades between the grid-composited result and the unmodified input, allowing the wall pattern to be overlaid at any opacity.

---

## Parameter Reference

<img src={rampart_control_panel} alt="Videomancer front panel with Rampart loaded"/>
*Videomancer's front panel with Rampart active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 170 |

At minimum, bricks are very narrow — a dense column of vertical mortar lines. At maximum, each brick spans a significant fraction of the screen width. Combined with Block H, this control defines the brick's aspect ratio. Real masonry bricks are roughly 2:1 width-to-height; Rampart allows any ratio from extreme verticals to extreme horizontals. Internally, sets the horizontal repeat period of the brick grid.

---

#### Knob 2 — U Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 341 |

Sets the vertical repeat period — the course height in masonry terms. Small values create many thin horizontal courses; large values create tall bricks. When Bond is active (running bond), odd-numbered courses shift horizontally by half the Block W value, breaking the vertical alignment. The visual density of the grid is most strongly affected by this control and Block W together.

---

#### Knob 3 — V Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 682 |

At zero, bricks tile edge-to-edge with no visible joint. As the value increases, the gap between bricks widens, and the mortar becomes a prominent visual element. At very high values, the mortar dominates the pattern and the bricks shrink to thin islands. The mortar color is set by Mortar Bright (Pot 4). Internally, controls the mortar line width.

---

#### Knob 4 — Y Polynomial
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 675 |

At zero, mortar is black — creating a dark grid of deep joints. At mid-range, mortar takes on a neutral gray. At maximum, mortar is white, producing a bright grid overlay. When Shadow is active, the mortar brightness value is further multiplied by a darkening factor, simulating recessed joints. Internally, sets the brightness of the mortar lines.

---

#### Knob 5 — U Polynomial
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 675 |

At zero, no crenellations are visible. As the value increases, the battlement row extends further down from the top edge. The crenellation pattern only appears when the Crenel toggle (Toggle 8) is also enabled. Internally, controls the height of the crenellation zone at the top of the screen.

---

#### Knob 6 — V Polynomial
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 675 |

Sets the width of each crenel (gap) and merlon (solid) in the battlement row. The crenellation pattern alternates between solid and gap at this period. Small values create a fine-toothed battlement; large values create wide, blocky teeth. The crenel width is independent of the main brick width — the battlement has its own horizontal rhythm.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Frame Sync** | Free Run | Sync |
| **8 — Chroma** | Off | On |
| **9 — Luma Invert** | Off | On |
| **10 — Half Speed** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent brick-wall rendering options. Bond selects the brick stagger pattern. Crenel enables or disables the battlement row at the top of the screen. Video Fill determines whether bricks show live video or flat color. Shadow adds depth to mortar lines. Bypass passes the input through unchanged — this is a true hardware bypass that skips all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input video (0%) and the fully processed brick-wall composite (100%). At intermediate values, the grid pattern is superimposed as a semi-transparent overlay on the source video, allowing subtle architectural textures without completely obscuring the underlying content.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Rampart processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises explore the LFSR noise generator's parameter space, from simple static noise to structured colour patterns.

### Exercise 1: Basic Noise Pattern

<BeforeAfterSlider
  sources={[
    { label: "Field", before: rampart_source1_field, after: rampart_ex1_s1 },
    { label: "Runner", before: rampart_source2_runner, after: rampart_ex1_s2 },
    { label: "Clouds", before: rampart_source3_clouds, after: rampart_ex1_s3 },
    { label: "Pattern", before: rampart_source4_pattern, after: rampart_ex1_s4 },
    { label: "Woman", before: rampart_source5_woman, after: rampart_ex1_s5 },
    { label: "Wood", before: rampart_source6_wood, after: rampart_ex1_s6 },
  ]}
/>
*Basic Noise Pattern — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and moderate contrast.

**What You'll Create**: Learn how seed values and polynomial feedback taps shape the noise output.

1. **Start with defaults**: With all Polynomials at mid-range and seeds at low values, observe the noise pattern on screen.
2. **Sweep Y Seed**: Slowly turn Y Seed from 0 to 100%. Watch how the luminance noise texture shifts — different seeds initialize the LFSR to different starting states.
3. **Change Y Polynomial**: Sweep Y Polynomial. Different feedback tap configurations produce radically different spatial patterns — some tightly structured, some chaotic.
4. **Add colour**: Toggle Chroma on (Toggle 8). U and V channels now generate independent noise, adding colour to the pattern.
5. **Half speed**: Toggle Half Speed on (Toggle 10). The noise pattern doubles in horizontal pixel width, producing a blockier texture.

**Key concepts**: Seed values set the LFSR starting state, polynomial feedback taps determine the sequence structure, chroma toggle enables colour noise

---

### Exercise 2: Structured Colour Noise

<BeforeAfterSlider
  sources={[
    { label: "Field", before: rampart_source1_field, after: rampart_ex2_s1 },
    { label: "Runner", before: rampart_source2_runner, after: rampart_ex2_s2 },
    { label: "Clouds", before: rampart_source3_clouds, after: rampart_ex2_s3 },
    { label: "Pattern", before: rampart_source4_pattern, after: rampart_ex2_s4 },
    { label: "Woman", before: rampart_source5_woman, after: rampart_ex2_s5 },
    { label: "Wood", before: rampart_source6_wood, after: rampart_ex2_s6 },
  ]}
/>
*Structured Colour Noise — simulated result across source images.*
**Source**: Colorful footage with strong shapes — flowers, faces, or abstract graphics work well.

**What You'll Create**: Explore how different polynomial and seed combinations create distinct colour textures.

1. **Colour separation**: With Chroma on, set different Polynomial values for Y, U, and V — for example Y ~800, U ~400, V ~600. Each channel now cycles through a different LFSR sequence.
2. **Seed offsets**: Adjust U Seed and V Seed independently. The colour palette shifts as each channel's LFSR starts from a different point in its sequence.
3. **Invert luma**: Toggle Luma Invert on (Toggle 9). The luminance channel inverts, creating a photographic-negative noise effect while chroma remains unchanged.
4. **Frame sync**: Toggle Frame Sync between Free Run and Sync (Toggle 7). In Free Run, the noise evolves continuously. In Sync, it locks to the video frame.
5. **Mix overlay**: Lower Mix to about 50%. The noise becomes a semi-transparent overlay on the source video.

**Key concepts**: Independent polynomials per channel create colour separation, luma inversion produces negative noise, frame sync controls temporal behaviour

---

### Exercise 3: Animated Texture Overlay

<BeforeAfterSlider
  sources={[
    { label: "Field", before: rampart_source1_field, after: rampart_ex3_s1 },
    { label: "Runner", before: rampart_source2_runner, after: rampart_ex3_s2 },
    { label: "Clouds", before: rampart_source3_clouds, after: rampart_ex3_s3 },
    { label: "Pattern", before: rampart_source4_pattern, after: rampart_ex3_s4 },
    { label: "Woman", before: rampart_source5_woman, after: rampart_ex3_s5 },
    { label: "Wood", before: rampart_source6_wood, after: rampart_ex3_s6 },
  ]}
/>
*Animated Texture Overlay — simulated result across source images.*
**Source**: Landscape or architectural footage — an outdoor scene with sky at the top works especially well for the noise overlay effect.

**What You'll Create**: Combine noise generation with half-speed mode and mix to create animated texture overlays.

1. **Set up base noise**: Use moderate seed and polynomial values across all channels with Chroma on.
2. **Half speed**: Enable Half Speed (Toggle 10). The noise pattern becomes coarser and more visually distinct.
3. **Free running animation**: Set Frame Sync to Free Run (Toggle 7). The noise now evolves frame-to-frame, creating a shimmering animated texture.
4. **Overlay blend**: Set Mix to about 30%. The noise becomes a subtle animated film-grain effect over the source.
5. **Vary polynomials**: Sweep V Polynomial while watching the output. Some polynomial values produce smooth rolling patterns while others create sharp static.

**Key concepts**: Half-speed mode doubles pixel width for coarser patterns, free-run frame sync enables animation, low mix creates subtle film-grain overlays

---


## Tips

- **Crenellation as a top border**: The battlement row works as a decorative top border. Set a small Crenel H for a subtle effect or a large value for a dramatic battlement silhouette.
- **Shadow needs mortar**: Shadow only affects mortar pixels. If Mortar is set to zero, enabling Shadow has no visible effect.
- **Mix for overlay**: Use Mix at 50–80% to overlay the brick grid on source video — useful for creating architectural textures without losing the underlying image.
- **ABI registers 8–11 are dead**: The VHDL reads four registers beyond the ABI boundary. These reads always return zero. All visible controls work correctly since they map to registers 0–7.

---

## Glossary

| Term | Definition |
|------|------------|
| **ABI** | Application Binary Interface; the fixed register layout through which the Videomancer firmware communicates parameter values to FPGA programs. Limited to 8 registers (indices 0–7). |
| **Bond** | The pattern in which bricks are laid in a wall. Running bond offsets alternating rows; stack bond aligns all rows vertically. |
| **Crenel** | The gap (open section) in a crenellated battlement wall. The raised solid sections between crenels are called merlons. |
| **Crenellation** | The alternating tooth-shaped parapet profile along the top of a fortress wall, consisting of merlons and crenels. |
| **Merlon** | The raised solid portion between two crenels in a battlement wall. |
| **Modular Arithmetic** | Division remainder operation (mod) that creates infinite repetition: `h mod w` produces a periodic pattern with period `w`. |
| **Mortar** | The material (or in Rampart's case, the pixel region) between adjacent bricks, rendered as lines of configurable width and brightness. |
| **Running Bond** | A brick bonding pattern where each course is offset by half a brick width, staggering vertical joints. |
| **Stack Bond** | A brick bonding pattern where all courses align vertically, creating continuous vertical mortar lines. |

---
