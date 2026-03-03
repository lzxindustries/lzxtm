---
draft: true
sidebar_position: 194
slug: /instruments/videomancer/mitosis
title: "Mitosis"
image: /img/instruments/videomancer/mitosis/mitosis_hero.png
description: "Mitosis is a 2D cellular automaton engine that evolves a pixel grid through discrete generations according to configurable birth and survival rules."
---

import mitosis_hero from '/img/instruments/videomancer/mitosis/mitosis_hero.png';
import mitosis_animation from '/img/instruments/videomancer/mitosis/mitosis_animation.gif';
import mitosis_control_panel from '/img/instruments/videomancer/mitosis/mitosis_control_panel.png';
import mitosis_exercise1_result from '/img/instruments/videomancer/mitosis/mitosis_exercise1_result.gif';
import mitosis_exercise2_result from '/img/instruments/videomancer/mitosis/mitosis_exercise2_result.gif';
import mitosis_exercise3_result from '/img/instruments/videomancer/mitosis/mitosis_exercise3_result.gif';

# Mitosis

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={mitosis_hero} alt="Mitosis hero image"/>
*Mitosis rendering cascading cellular automaton generations in Growth rule mode — alive cells glow cyan while decaying cells fade through magenta tiers against a deep black field.*
<img src={mitosis_animation} alt="Mitosis animated output"/>
*Mitosis output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Mitosis is a 2D cellular automaton engine that evolves a pixel grid through discrete generations according to configurable birth and survival rules. The automaton state lives in two ping-pong BRAM banks — one holds the current generation while the other is being written with the next. Each cell exists in one of four states: dead, alive, dying-1, and dying-2. The alive/dead transition is governed by one of four selectable rule sets (Growth, Seeds, Brain, Cascade), each producing radically different emergent behavior from the same neighbor-counting infrastructure.

The name *Mitosis* refers to cell division — the biological process by which a single cell splits into two daughter cells. The program's cellular automaton exhibits analogous behavior: living cells spawn new cells in adjacent positions according to local rules, populations expand and contract, and complex macro-structures emerge from purely local interactions. At conservative settings a sparse field of slowly blinking points drifts across the screen. At extreme settings the entire frame writhes with rapidly evolving fractal-like structures — branching dendrites, oscillating gliders, and self-replicating patterns that fill every pixel.

Video input serves as a seed source: the input luminance is thresholded against Birth Thresh to inject alive cells into the automaton grid. In Continuous seed mode, the video constantly seeds new cells every frame; in Evolve-Only mode, seeding happens once and the automaton runs autonomously. The four decay tiers map to a chroma color palette — alive cells carry one hue, dying-1 a second, dying-2 a third, and dead cells a fourth. The Color Map knob rotates through these palettes while Invert flips the mapping.

---

## Background

### What Is a Cellular Automaton?

A **cellular automaton** (CA) is a grid of cells, each in one of a finite number of states, that evolves in discrete time steps according to a fixed local rule. At each generation, every cell examines its neighborhood — typically the eight surrounding cells in a 2D grid (the Moore neighborhood) — and transitions to a new state based on how many neighbors are alive. The most famous example is John Conway's Game of Life, where a dead cell with exactly three live neighbors is born, and a live cell with two or three live neighbors survives; all other cells die.

Despite the simplicity of local rules, cellular automata produce extraordinary emergent complexity. Stable structures, oscillators, gliders, and self-replicating patterns arise spontaneously from random initial conditions. Different rule sets produce qualitatively different universes — some are chaotic, some settle into static patterns, some support long-range information transport.

### What Are Birth/Survival Rules?

CA rules are commonly expressed in **B/S notation**: B*n*/S*m* means a dead cell is born if it has exactly *n* live neighbors, and a live cell survives if it has exactly *m* live neighbors. Conway's Life is B3/S23. Mitosis implements four distinct rule sets selected by two toggle bits:

| Rule | Name | Character |
|------|------|-----------|
| 00 | Growth | Aggressive expansion — cells born easily, creating dense branching structures |
| 01 | Seeds | Cells born but never survive — every alive cell dies next generation, producing sparkling ephemeral patterns |
| 10 | Brain | Two-state decay — alive cells become "dying" before fully dead, creating trails behind moving structures |
| 11 | Cascade | Asymmetric rules favoring directional flow patterns |

### What Is Ping-Pong Buffering?

The automaton requires reading the current generation while simultaneously writing the next one. **Ping-pong buffering** uses two identical memory banks: on even frames, bank A is the read source and bank B is the write destination; on odd frames, the roles swap. This eliminates read-write conflicts without requiring double the bandwidth — each bank is accessed by only one operation (read or write) per frame. The two BRAM blocks in Mitosis serve exactly this purpose.

### What Is Multi-State Decay?

In simple binary CAs, cells are either alive or dead. Mitosis extends this to four states: alive → dying-1 → dying-2 → dead. When a cell fails the survival test, it does not immediately become dead — it transitions through two intermediate "dying" states at a rate controlled by the Decay Rate parameter. This creates visual trails behind moving structures: alive cells are brightest, dying-1 cells are dimmer, dying-2 cells are dimmest, and dead cells are black. The decay rate determines how long these trails persist.

### What Is Frame-Rate Throttling?

Evolving the automaton every video frame (60 Hz) can be too fast to observe individual generations. The Evolve Rate parameter implements a **frame skip counter** — the automaton only advances one generation every N frames, where N is derived from the register value. At low Evolve Rate, the automaton evolves at full speed; at high values, generations are separated by many frames, allowing the viewer to see each state transition clearly.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Seed Extraction ────────────────────────────────────────────
│   │
│   ├─ 1. Threshold Y against Birth Thresh (reg 0)
│   └─ 2. Inject seed cells into write bank (continuous or once)
│            ◄── Seed Mode (toggle bit 2)
│
├── Cellular Automaton Engine ──────────────────────────────────
│   │
│   ├─ 3. Read current generation from bank A/B (ping-pong)
│   ├─ 4. Count neighbors (3×3 window, cardinal/diagonal weight)
│   │        ◄── Neighborhood (reg 4)
│   ├─ 5. Apply birth/survival rule
│   │        ◄── Rule Bit 0, Rule Bit 1 (toggle bits 0–1)
│   ├─ 6. Decay state transition (alive → dying1 → dying2 → dead)
│   │        ◄── Decay Rate (reg 5)
│   ├─ 7. Frame-skip throttle
│   │        ◄── Evolve Rate (reg 1)
│   └─ 8. Write next generation to bank B/A
│
├── Color Mapping ──────────────────────────────────────────────
│   │
│   ├─ 9. Map 4-tier state to YUV palette
│   │        ◄── Color Map (reg 2), Invert (toggle bit 3)
│   └─ 10. Dead cell transparency blend
│            ◄── Dead Opacity (reg 3)
│
├── Output Mixing ──────────────────────────────────────────────
│   └─ 11. Interpolator wet/dry mix
│            ◄── Mix (reg 7)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
         ◄── Bypass (toggle bit 4)
```

The critical interaction is between the seed path and the evolution engine. In Continuous mode, the input video constantly injects new alive cells, fighting against the automaton's natural tendency toward equilibrium — the resulting pattern is a dynamic hybrid of the video structure and the CA rule's emergent behavior. In Evolve-Only mode, the initial seed determines everything and the automaton runs free, producing pure emergent structure independent of the ongoing input. The Evolve Rate throttle is essential for observation — at full speed, most rules produce patterns that change too rapidly to follow.

---

## Parameter Reference

<img src={mitosis_control_panel} alt="Videomancer front panel with Mitosis loaded"/>
*Videomancer's front panel with Mitosis active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Birth Thresh
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the luminance threshold applied to the input video for cell seeding. At low values, only the brightest input pixels inject alive cells — the automaton seeds from highlights. At high values, most of the input frame qualifies as a seed source, flooding the grid with alive cells. The optimal setting depends on the input material: high-contrast sources work well at moderate threshold; low-contrast sources need the threshold lowered to generate any seeds.

---

#### Knob 2 — Evolve Rate
| Property | Value |
|----------|-------|
| Range | 1 – 60 |
| Default | 31 |

Controls the evolution frame-skip count. At minimum, the automaton advances one generation every video frame (60 generations per second). As the value increases, more frames are skipped between generations, slowing evolution. At maximum, the automaton may advance only once every several seconds, allowing individual generation transitions to be observed clearly. This is the primary control for matching the CA's temporal behavior to the viewer's perceptual speed.

---

#### Knob 3 — Color Map
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Selects which chroma palette is applied to the four cell states. The Color Map register indexes through preset hue assignments for alive, dying-1, dying-2, and dead cells. At one extreme, alive cells are cyan and dying cells shift through blue to magenta. At the other, alive cells are warm yellow and dying cells shift through orange to red. The transitions between palette entries are smooth, allowing fine-tuning of the color scheme.

---

#### Knob 4 — Dead Opacity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the transparency of dead cells. At minimum, dead cells are fully opaque black — the automaton pattern sits on a solid black background. As the value increases, dead cell regions become increasingly transparent, allowing the input video to show through the gaps in the CA pattern. At maximum, the automaton overlays the input with alive and dying cells while the background is fully transparent.

---

#### Knob 5 — Neighborhood
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Weights the influence of diagonal versus cardinal neighbors in the 3×3 counting window. At minimum, only the four cardinal neighbors (up/down/left/right) participate in the birth/survival calculation. At maximum, all eight Moore neighborhood cells contribute equally. Intermediate values blend between these extremes, changing the directional character of emergent structures — cardinal-only rules tend to produce axis-aligned grid patterns, while full Moore neighborhoods produce isotropic organic shapes.

---

#### Knob 6 — Decay Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls how many frames a dying cell persists before transitioning to the next decay tier. At minimum, dying cells transition immediately — alive → dead in one generation, producing crisp patterns with no trailing. At maximum, dying cells persist for many frames, creating long luminous trails behind moving structures that reveal the automaton's recent history as a fading afterimage.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Rule Bit 0** | Off | On |
| **8 — Rule Bit 1** | Off | On |
| **9 — Seed Mode** | Cont. | Evolve |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a 2-bit rule selector (4 combinations), while toggles 9–11 independently control seed behavior, color polarity, and bypass. The rule selection has the most dramatic effect — switching rules transforms the entire character of the automaton's emergent behavior.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the processed automaton output and the original input signal. At 100%, the full automaton output is visible. At 0%, the original input passes through unmodified. Intermediate positions blend the two, allowing the automaton pattern to be superimposed on the source at reduced intensity — useful for creating subtle texture overlays rather than full replacement.

---

## Guided Exercises

These exercises explore the four rule sets and their interactions with seeding, decay, and color mapping. Each builds familiarity with a different aspect of cellular automaton behavior.

### Exercise 1: Growth Rule — Dendrite Forests

<img src={mitosis_exercise1_result} alt="Growth Rule — Dendrite Forests result"/>
*Growth Rule — Dendrite Forests — simulated result across source images.*
**Objective**: Observe how the Growth rule produces aggressive branching structures that fill available space, and how the seed threshold controls initial density.

1. **Start sparse**: Set Birth Thresh to ~80% so only the brightest input pixels seed cells. Set Evolve Rate to ~40% for moderate speed. Enable Continuous seeding (Seed Mode off).
2. **Watch expansion**: Bright regions of the input generate seed clusters that rapidly branch outward, forming dendrite-like trees.
3. **Increase density**: Lower Birth Thresh to ~30%. More seeds appear — the dendrites collide and merge into dense cellular tissue.
4. **Slow down**: Increase Evolve Rate to ~70%. Individual generations become visible — watch each branch extend by one cell per step.
5. **Add color**: Sweep Color Map to find a palette where the alive/dying tiers are clearly distinct. The dendrite tips (alive) should be a different hue from the trailing regions (dying).
6. **Enable decay trails**: Increase Decay Rate to ~60%. The dendrite branches leave persistent trails, revealing growth direction and history.

**Key concepts**: Growth rule produces aggressive space-filling expansion, birth threshold controls seed density, decay trails reveal growth history, evolve rate makes individual generations observable

---

### Exercise 2: Seeds Rule — Ephemeral Sparkle

<img src={mitosis_exercise2_result} alt="Seeds Rule — Ephemeral Sparkle result"/>
*Seeds Rule — Ephemeral Sparkle — simulated result across source images.*
**Objective**: Experience the Seeds rule where alive cells always die the next generation, producing sparkling, firework-like patterns that never settle into stable structures.

1. **Select Seeds rule**: Toggle Rule Bit 0 on, Rule Bit 1 off (rule 01).
2. **Continuous seeding**: Keep Seed Mode off (continuous). Set Birth Thresh to ~50%.
3. **Observe sparkle**: Each seed cell flashes alive for exactly one generation, then dies. New cells are born from the dying cell's neighbors, creating expanding rings of single-frame flashes.
4. **Reduce evolve rate**: Slow to ~60% Evolve Rate. Watch individual flash events — each alive cell exists for only one frame before vanishing.
5. **Decay trails**: Increase Decay Rate to ~70%. The single-frame alive cells leave two-tier dying trails, transforming point flashes into comet-like streaks.
6. **Invert color**: Toggle Invert on. The brief alive flashes become dark points against a bright dying-cell field — a photographic negative of the sparkle pattern.

**Key concepts**: Seeds rule: alive cells never survive, creating ephemeral single-generation flashes; decay trails transform point events into visible streaks; invert reverses figure/ground relationship

---

### Exercise 3: Brain Rule — Autonomous Evolution

<img src={mitosis_exercise3_result} alt="Brain Rule — Autonomous Evolution result"/>
*Brain Rule — Autonomous Evolution — simulated result across source images.*
**Objective**: Use the Brain rule in Evolve-Only mode to create self-sustaining automaton patterns that are completely independent of the input video after the initial seeding.

1. **Select Brain rule**: Toggle Rule Bit 0 off, Rule Bit 1 on (rule 10).
2. **Evolve-Only mode**: Toggle Seed Mode on. The automaton will seed once from the current video frame and then run autonomously.
3. **Moderate threshold**: Set Birth Thresh to ~45% for a balanced initial density.
4. **Slow evolution**: Set Evolve Rate to ~50% so patterns develop at a watchable pace.
5. **Observe self-organization**: After the initial seeding, watch the Brain rule produce traveling wave patterns and oscillators. The two-stage decay creates visible wave fronts with bright leading edges and dim trailing edges.
6. **Full neighborhood**: Set Neighborhood to maximum (~100%). The waves become isotropic — circular expanding rings rather than diamond-shaped cardinal patterns.
7. **Color mapping**: Sweep Color Map slowly. The three visible tiers (alive, dying-1, dying-2) shift through palette combinations — find a combination where the wave front hierarchy is clearest.

**Key concepts**: Brain rule produces traveling waves via mandatory decay, evolve-only creates input-independent patterns, neighborhood weighting controls wave isotropy, self-sustaining structures emerge from random initial conditions

---


## Tips

- **Rule selection is the most powerful control**: The four rules produce completely different visual worlds from the same seed. Cycle through them first to find the character you want, then refine with the other parameters.
- **Evolve Rate is essential for observation**: At full speed, most rules produce patterns that change faster than the eye can follow. Slow the rate to study individual generation transitions.
- **Continuous seeding links to video content**: Keep Seed Mode off to anchor the automaton pattern to the input video structure — the CA becomes a living texture overlay that follows the source.
- **Evolve-Only creates autonomous life**: Toggle Seed Mode on to let the automaton run free. The initial video frame determines the starting conditions, but all subsequent behavior is purely emergent.
- **Decay Rate reveals motion history**: High decay rates create trailing afterimages behind moving CA structures — useful for showing directionality and flow in the pattern.
- **Dead Opacity for compositing**: At high Dead Opacity, the CA pattern floats over the input video. At zero, it sits on solid black. Use this to control whether the program produces standalone visuals or textured overlays.
- **Neighborhood shapes the geometry**: Cardinal-only neighbors produce grid-aligned, crystalline structures. Full Moore neighborhoods produce organic, rounded forms.
- **Feedback loops create recursive CAs**: Route the output back to the input. The automaton's own pattern becomes the seed source, creating a feedback loop where the CA evolves from its own output.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA used for the ping-pong cell state buffers. |
| **Cardinal Neighbors** | The four cells directly up, down, left, and right of a given cell. |
| **Cellular Automaton (CA)** | A grid of cells evolving in discrete steps according to local rules examining neighbor states. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **DDS** | Direct Digital Synthesis; a technique using a phase accumulator to generate periodic waveforms. |
| **Decay** | The gradual transition from alive through intermediate dying states to dead, creating visual trails. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit executing the video pipeline. |
| **Frame Skip** | Holding the automaton state unchanged for multiple video frames to slow visible evolution rate. |
| **Generation** | One complete update cycle of the cellular automaton, where every cell evaluates its neighborhood and transitions. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Moore Neighborhood** | The eight cells surrounding a given cell in a 2D grid (four cardinal + four diagonal). |
| **Ping-Pong Buffer** | Two memory banks alternating between read and write roles each frame to avoid conflicts. |
| **Pipeline** | A chain of processing stages executing one operation per clock cycle with fixed total latency. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V); used throughout the Videomancer pipeline. |

---
