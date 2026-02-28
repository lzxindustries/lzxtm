---
draft: true
sidebar_position: 56
slug: /instruments/videomancer/coral
title: "Coral"
image: /img/instruments/videomancer/coral/coral_hero.png
description: "Program guide for Coral, a Videomancer organic program for the LZX video synthesizer."
---

import coral_hero from '/img/instruments/videomancer/coral/coral_hero.png';
import coral_animation from '/img/instruments/videomancer/coral/coral_animation.gif';
import coral_control_panel from '/img/instruments/videomancer/coral/coral_control_panel.png';
import coral_exercise1_result from '/img/instruments/videomancer/coral/coral_exercise1_result.gif';
import coral_exercise2_result from '/img/instruments/videomancer/coral/coral_exercise2_result.gif';
import coral_exercise3_result from '/img/instruments/videomancer/coral/coral_exercise3_result.gif';

# Coral

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={coral_hero} alt="Coral hero image"/>
*Eight branching coral columns growing upward from the screen floor, their LFSR-driven splits propagating organic structure through a depth-shaded reef rendered in warm living color.*
<img src={coral_animation} alt="Coral animated output"/>
*Coral output evolving over multiple frames â€” synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Coral simulates the vertical growth of a reef structure from the edge of the frame. Eight branch columns emerge from the bottom of the screen and climb upward at a configurable speed. An LFSR pseudo-random generator triggers probabilistic splits that transfer growth energy to neighboring columns, producing the branching, fractal-like silhouettes characteristic of real coral formations. The result is a slowly materializing reef that fills the frame from the ground up â€” a living architecture generated entirely from arithmetic.

The name refers directly to the marine invertebrates of order Scleractinia that build calcium carbonate skeletons over decades, creating the largest biological structures on Earth. In the program's domain, each of the eight columns is a discrete growth front whose height accumulates frame by frame. When the LFSR fires a split event, a quarter of a source column's height is donated to an adjacent column, simulating the lateral branching that gives real coral its characteristic tree-like morphology. A depth-based color gradient darkens the base of each column relative to its tip, mimicking the natural light attenuation that occurs as sunlight penetrates water â€” branches near the surface are bright, while the reef's foundation fades into shadow.

Growth speed, branch thickness, column spacing, split probability, overlay intensity, and gradient strength are all continuously adjustable. At low growth speeds the reef builds slowly and deliberately; at maximum speed the columns race to fill the screen within seconds. The direction toggle flips the growth origin from bottom to top, and the color mode switches between warm coral hues and cool deep-water blues.

---

## Background

### Coral Biology and Reef Formation

Coral reefs are built by colonies of tiny polyps â€” soft-bodied organisms related to jellyfish â€” that secrete calcium carbonate exoskeletons. Over centuries, successive generations of polyps build upon the skeletons of their predecessors, creating massive three-dimensional structures. The branching pattern of species like *Acropora* (staghorn coral) is governed by a combination of genetic body plan, water flow direction, light availability, and nutrient gradients. Coral's eight-column growth model abstracts this process: each column represents a vertical growth axis, and the LFSR-driven splits simulate the stochastic branching events that occur when a polyp colony reaches a critical mass and bifurcates into adjacent territory.

### L-Systems and Formal Grammars for Growth

Aristid Lindenmayer introduced L-systems in 1968 to model the branching patterns of plants and algae. An L-system is a parallel rewriting grammar: a set of production rules that replace symbols with strings of symbols, generating increasingly complex structures through repeated application. The classic example replaces `F` (draw forward) with `F[+F]F[-F]F`, producing branching tree-like figures. Coral's growth model is a hardware-friendly simplification of this concept â€” instead of symbolic rewriting, it uses a fixed array of height accumulators with probabilistic neighbor transfers, achieving a similar visual result (vertical structures that branch laterally) without the memory overhead of storing a parse tree.

### Branching Growth Algorithms in Computer Graphics

Procedural generation of branching structures is a foundational technique in computer graphics, from the space-colonization algorithms used for tree modeling to the diffusion-limited aggregation (DLA) processes used for lightning, rivers, and mineral dendrites. Coral's approach falls into the category of *agent-based growth models*: each of the eight columns is an autonomous agent that accumulates height independently, with the LFSR providing a shared random oracle that occasionally triggers inter-agent communication (the split event). The simplicity of the model â€” eight 12-bit accumulators, one LFSR comparison per frame, no BRAMs â€” makes it feasible in the constrained LUT budget of an iCE40 FPGA while still producing visually rich branching behavior.

### Depth Cues and Underwater Light Attenuation

In natural underwater environments, light intensity decreases exponentially with depth due to absorption and scattering by water molecules. This creates a characteristic gradient: objects near the surface are brightly illuminated, while those at depth are darker and shift toward blue-green hues. Coral's depth gradient stage models this phenomenon by computing a vertical position-dependent darkening factor and subtracting it from the base coral luminance. The Color Gradient parameter controls the strength of this attenuation â€” at maximum, branches near their root are deeply shadowed; at minimum, the entire column is uniformly bright. The gradient gives the flat, column-based structure a sense of three-dimensional depth, implying that the base of the reef is further from the viewer than the growing tips.

### LFSR-Driven Stochastic Branching

The 16-bit maximal-length LFSR (taps at bits 16, 15, 13, 4) provides the randomness that drives branch splitting. On each vertical sync pulse, the low 10 bits of the LFSR output are compared against the Split Rate threshold. When the LFSR value falls below the threshold, a split event occurs: the source column is selected by LFSR bits 15â€“13 (3 bits â†’ 0â€“7), the neighbor direction by bit 12 (left or right), and a quarter of the source column's accumulated height is transferred to the destination column as bonus growth. This mechanism ensures that splits are temporally and spatially unpredictable while remaining deterministic for a given LFSR seed â€” the same growth sequence will replay identically if the program is reset.


---

## Signal Flow

```
Video Input (YUV 4:4:4)
â”‚
â”œâ”€â”€ Register Decode â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ growth_speed = registers_in(0) â†’ s_grow_inc (1..8 px/frame)
â”‚   â”œâ”€ thickness    = registers_in(1) â†’ s_thick_val (2..33 px)
â”‚   â”œâ”€ density      = registers_in(2) â†’ s_spacing_val (60..571 px)
â”‚   â”œâ”€ color_grad   = registers_in(3) â†’ 4-level gradient strength
â”‚   â”œâ”€ split_rate   = registers_in(4) â†’ LFSR split threshold
â”‚   â”œâ”€ intensity    = registers_in(5) â†’ 4-level overlay opacity
â”‚   â””â”€ toggles: direction, color_mode, reset, bypass
â”‚       mix_amount  = registers_in(7)
â”‚
â”œâ”€â”€ Timing Generator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ video_timing_generator â†’ s_h_count, s_v_count
â”‚
â”œâ”€â”€ LFSR Noise â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ lfsr16 (seed 0xC0A1) â†’ s_lfsr_q (16 bits)
â”‚
â”œâ”€â”€ Branch Growth + Split (per vsync) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ 8 branches: height += grow_inc (clamped at 1079)
â”‚   â”œâ”€ Split: if LFSR(9:0) < split_rate then
â”‚   â”‚     src = LFSR(15:13), dir = LFSR(12)
â”‚   â”‚     dst.height += src.height >> 2 + grow_inc
â”‚   â”œâ”€ X positions: 120 + i Ã— spacing_val
â”‚   â””â”€ Tip: bottom âˆ’ height (up) or height (down)
â”‚
â”œâ”€â”€ Clock 1: Input Register â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ Latch Y, U, V from data_in
â”‚
â”œâ”€â”€ Clock 2: 8-Branch Parallel Hit Detection â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ For each branch i:
â”‚       |h_count âˆ’ xpos(i)| < thick_val AND v_count in range
â”‚       â†’ s_coral_hit OR of all 8
â”‚
â”œâ”€â”€ Clock 3: Coral Color Compose â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ Depth gradient: v_gradient = v_count >> 1 (or inverted)
â”‚   â”œâ”€ Scale gradient by color_grad (4 thresholds)
â”‚   â”œâ”€ Color mode 0: warm coral (Y=700, U=400, V=650)
â”‚   â”‚   Color mode 1: cool blue  (Y=600, U=650, V=350)
â”‚   â””â”€ Coral Y = base_y âˆ’ gradient_dim (clamped â‰¥ 64)
â”‚
â”œâ”€â”€ Clock 4: Composite Output â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ Hit + intensity > 768: 100% coral
â”‚   â”œâ”€ Hit + intensity > 512:  75% coral + 25% source
â”‚   â”œâ”€ Hit + intensity > 256:  50% coral + 50% source
â”‚   â”œâ”€ Hit + intensity â‰¤ 256:  25% coral + 75% source
â”‚   â””â”€ No hit: pass source through
â”‚
â”œâ”€â”€ Clocks 5â€“8: Interpolator (wet/dry Mix) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ lerp(dry, wet, mix_amount) Ã—3 channels (4 clocks)
â”‚
â”œâ”€â”€ Sync Delay Pipeline (8 clocks) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ hsync, vsync, field, Y, U, V delayed to match
â”‚
â””â”€â”€ Bypass Mux â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    â””â”€ Select delayed source or processed signal
```

The computational heart of Coral is the frame-level growth-and-split update that executes once per vertical sync. All eight branch heights are incremented by the same growth constant, but the LFSR-driven split creates asymmetry: when a split fires, the destination column receives both the normal growth increment and a quarter of the source column's accumulated height, causing it to surge ahead. This positive-feedback mechanism means that once a column receives a split, it becomes taller and therefore a more attractive source for future splits â€” a rich-get-richer dynamic that produces the characteristic uneven canopy of a natural reef. The per-pixel rendering in Clocks 1â€“4 is purely combinational: each of the eight branches is tested in parallel for horizontal and vertical containment, requiring no BRAMs and keeping the pipeline at a compact 8 clocks total including the interpolator mix stage.

---

## Parameter Reference

<img src={coral_control_panel} alt="Videomancer front panel with Coral loaded"/>
*Videomancer's front panel with Coral active. Knobs 1â€“6 (top two rows of left cluster), Toggle switches 7â€“11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1â€“6)

#### Knob 1 â€” Grow Spd
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

Sets the vertical growth increment applied to all eight branch columns on each frame. At the low end, each column gains a single pixel of height per frame â€” the reef builds over hundreds of frames, allowing you to observe the branching dynamics in slow motion. At the high end, columns gain eight pixels per frame and race toward the opposite edge of the screen within seconds. The growth increment is uniform across all columns; differentiation arises entirely from the LFSR split events that boost selected columns above their peers.

---

#### Knob 2 â€” Branch D
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

Controls the horizontal thickness of each branch column in pixels, determining how wide the coral bands appear on screen. At the minimum setting, branches are thin two-pixel lines â€” skeletal scaffolding that emphasizes the vertical growth structure. At maximum, each branch widens to over thirty pixels, producing fat pillar-like columns that overlap and merge into a solid reef wall when spacing is tight. The thickness value is computed as a fixed base plus a scaled portion of the register value, ensuring that branches never collapse to sub-pixel invisibility.

---

#### Knob 3 â€” Branch Th
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

Determines the horizontal spacing between adjacent branch columns, controlling how densely packed the reef appears. At the minimum setting, columns are separated by only sixty pixels and their broad strokes overlap into a continuous mass. At maximum spacing, columns spread across the full width of the frame with wide gaps between them, creating an open lattice structure. The eight column X positions are computed sequentially starting from a fixed offset of 120 pixels, so the rightmost columns may extend off-screen at high spacing values â€” a deliberate design that prevents the reef from appearing artificially centered.

---

#### Knob 4 â€” Color Grd
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

Controls the strength of the depth-based luminance gradient that darkens branches near their root. At the maximum setting, the gradient subtracts significant luminance from pixels near the growth origin (the bottom of the screen when growing upward), creating a dramatic light-to-dark transition from tip to base. At the minimum, the gradient is barely perceptible and all parts of each column share roughly the same brightness. The gradient operates through a four-level threshold system â€” the register value selects between full, half, quarter, or eighth strength attenuation â€” producing distinct visual steps rather than a smooth continuum.

---

#### Knob 5 â€” Max Hght
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

Sets the LFSR split probability threshold, governing how frequently branch columns donate growth to their neighbors. The low 10 bits of the LFSR output are compared against this value on each frame: higher values increase the probability that any given frame triggers a split event. At zero, no splits occur and all columns grow uniformly as independent parallel lines. At moderate values, occasional splits create gentle asymmetries â€” some columns grow taller than others, and the canopy develops natural variation. At maximum, splits fire almost every frame, rapidly transferring height between neighbors and producing a chaotic, turbulent growth pattern where individual columns surge and plateau unpredictably.

---

#### Knob 6 â€” Angle Sp
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

Controls the opacity of the coral overlay relative to the incoming source video, using a four-level blending scheme. At the highest setting, coral pixels completely replace the source with the synthesized coral color. At three-quarter intensity, the coral dominates but a ghost of the source bleeds through. At half, coral and source contribute equally. At the lowest setting, the coral is a subtle tint over the source. This parameter is distinct from the Mix fader â€” it controls the blending *within* hit pixels, while Mix crossfades the entire processed output against the unprocessed delayed source.

---

### Toggle Switches (Switches 7â€“11)

| Switch | Off | On |
|--------|-----|-----|
| **7 â€” Species** | Staghorn | Brain |
| **8 â€” Palette** | Reef | Deep |
| **9 â€” Current** | Off | On |
| **10 â€” Animate** | Off | On |
| **11 â€” Bypass** | Off | On |

The five toggles configure independent aspects of the coral rendering. Species (7) selects the growth direction â€” whether the reef builds upward from the bottom edge or downward from the top. Palette (8) switches the coral's chromatic identity between warm and cool palettes. Current (9) provides a reset function that clears all branch heights on activation. Animate (10) is reserved for future use and has no visible effect in the current implementation. Bypass (11) is the standard signal bypass. Each toggle operates independently; combining an upward warm reef with periodically triggered resets produces a rhythmic growth animation cycle.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 â€” Mix
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade at the final stage of the pipeline. At maximum (default), the output is the fully processed coral composite. At minimum, the output is the unprocessed input video delayed by the 8-clock pipeline. Intermediate values produce a smooth blend via the three-channel interpolator. Use moderate mix levels to overlay the coral structure as a translucent texture on live video, or pull to minimum for a clean pass-through that preserves the coral growth state for later recall.

---

## Guided Exercises

These exercises explore Coral's synthesis capabilities from basic reef construction through dynamic splitting to layered compositions. Each builds on the previous, revealing how growth speed, split probability, and column spacing interact to shape the emergent branching structure.

### Exercise 1: Static Reef Foundation

<img src={coral_exercise1_result} alt="Static Reef Foundation result"/>
*Static Reef Foundation â€” simulated result across source images.*
**Objective**: Build a basic coral reef from the bottom of the screen and observe how thickness and spacing control the visual density of the structure.

1. Set Growth Speed to about 40% and wait for columns to grow halfway up the screen.
2. Sweep Branch Thickness from minimum to maximum â€” watch columns expand from hairlines to fat pillars.
3. Sweep Branch Spacing from minimum to maximum â€” watch columns spread apart or compress into a wall.
4. Set Color Gradient to about 70% and observe the tip-to-root darkening.
5. Set Growth Speed to 0% to freeze the reef and examine the static structure.
6. Try the cool blue palette â€” toggle Palette to the third or fourth position.

**Key concepts**: Growth speed is uniform across all columns without splits, thickness and spacing define the reef's visual density, the depth gradient creates a natural light attenuation effect, freezing growth allows static analysis of the structure.

---

### Exercise 2: LFSR-Driven Branching

<img src={coral_exercise2_result} alt="LFSR-Driven Branching result"/>
*LFSR-Driven Branching â€” simulated result across source images.*
**Objective**: Enable split events and observe how the LFSR creates organic asymmetry in the coral canopy.

1. Toggle Current On then Off to reset all branch heights.
2. Set Growth Speed to about 30% for slow, visible growth.
3. Gradually increase Split Rate from 0% to about 60%. Watch for sudden height jumps in individual columns as split events fire.
4. Notice how some columns surge ahead of their neighbors â€” this is the rich-get-richer feedback where taller columns donate more height via splits.
5. Increase Split Rate to maximum and observe the chaotic, turbulent canopy.
6. Reset again and try with very wide spacing to see the split dynamics between isolated columns.

**Key concepts**: The LFSR provides deterministic pseudo-randomness for split events, split probability controls branching frequency, the quarter-height transfer creates positive feedback, column spacing affects the visual impact of neighbor-to-neighbor transfers.

---

### Exercise 3: Inverted Stalactite Formation

<img src={coral_exercise3_result} alt="Inverted Stalactite Formation result"/>
*Inverted Stalactite Formation â€” simulated result across source images.*
**Objective**: Create a downward-growing cave formation using reversed direction, cool blue palette, and high-intensity overlay.

1. Toggle Species to the third or fourth position (Fan or Pillar) to reverse growth direction.
2. Switch Palette to the third or fourth position (Blchd or Neon) for cool blue rendering.
3. Set Growth Speed to about 50% and Split Rate to about 40%.
4. Set Color Gradient to maximum â€” the gradient now darkens the top (root) and brightens the tips hanging downward.
5. Set Branch Thickness to about 60% for substantial stalactite columns.
6. Set Intensity to maximum for full coral-colored replacement of the source.

**Key concepts**: Direction reversal inverts both the growth origin and the gradient orientation, cool palette evokes deep cave or underwater environments, the same growth and split algorithms produce visually distinct results when the frame of reference is inverted.

---


## Tips

- **Reset for synchronized starts**: Toggle Current before a performance segment to guarantee all branches begin growing from zero simultaneously. This produces a clean, repeatable growth animation.
- **Low Split Rate for architectural regularity**: With Split Rate near zero, all eight columns grow uniformly, creating a symmetric colonnade. This clean geometry works well as a compositional grid element.
- **High Split Rate for organic chaos**: At maximum split probability, the canopy becomes wildly uneven â€” some columns saturate at full screen height while others remain stunted. This turbulent growth pattern most closely resembles real coral reef morphology.
- **Thickness and spacing interact**: Wide branches at tight spacing merge into a solid wall; narrow branches at wide spacing create an open lattice. Find the balance point where individual columns are distinct but the overall reef reads as a connected structure.
- **Gradient at maximum for depth**: Strong color gradient makes the flat column rendering feel three-dimensional. The darkened roots imply distance and underwater light absorption.
- **Mix for overlay compositing**: Pull Mix to 40â€“60% to overlay the coral structure transparently onto live video, creating a reef that appears to grow through the video content.
- **Direction reversal for variety**: Switching from upward to downward growth produces stalactite formations that feel fundamentally different from the default reef, despite using identical algorithms.
- **Periodic resets for animation loops**: Toggle Current on and off rhythmically to create repeating growth cycles â€” the reef builds, resets, and builds again, producing a looping animation suitable for installations.

---

## Glossary

| Term | Definition |
|------|------------|
| **Accumulator** | A register that sums an increment on each clock cycle; used here for branch height growth, adding a fixed value per frame until clamped at the screen edge. |
| **BRAM** | Block RAM; dedicated FPGA memory. Coral uses zero BRAMs â€” all state is held in distributed register logic. |
| **Branch column** | One of eight vertical growth fronts, each defined by an X position, a height accumulator, and a computed tip position. |
| **Depth gradient** | A vertical luminance attenuation that darkens pixels near the branch root, simulating underwater light absorption with increasing depth. |
| **Hit detection** | The per-pixel comparison that determines whether a pixel falls within any branch's horizontal thickness and vertical extent. |
| **L-system** | Lindenmayer system; a formal grammar for modeling branching growth, the theoretical ancestor of Coral's column-based branching model. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used to trigger stochastic split events between adjacent branches. |
| **Scleractinia** | The order of hard corals that build calcium carbonate skeletons, forming the biological reef structures that the program simulates. |
| **Split event** | A frame-level transfer of growth energy from one branch column to a neighbor, triggered when the LFSR output falls below the Split Rate threshold. |
| **Tip** | The growing end of a branch column; computed as the screen bottom minus accumulated height (for upward growth) or the accumulated height itself (for downward growth). |
| **YUV** | A color space separating luminance (Y) from chrominance (U, V); the native pixel format of the Videomancer processing pipeline. |

---
