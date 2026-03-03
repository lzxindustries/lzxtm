---
draft: true
sidebar_position: 246
slug: /instruments/videomancer/rime
title: "Rime"
image: /img/instruments/videomancer/rime/rime_hero_s1.png
description: "In 1885, a Vermont farmer named Wilson Bentley attached a bellows camera to a compound microscope and captured the first photomicrograph of a snowflake."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import rime_source1_skull from '/img/instruments/videomancer/rime/rime_source1_skull.png';
import rime_source2_boat from '/img/instruments/videomancer/rime/rime_source2_boat.png';
import rime_source3_clouds from '/img/instruments/videomancer/rime/rime_source3_clouds.png';
import rime_source4_pattern from '/img/instruments/videomancer/rime/rime_source4_pattern.png';
import rime_source5_man from '/img/instruments/videomancer/rime/rime_source5_man.png';
import rime_source6_knit from '/img/instruments/videomancer/rime/rime_source6_knit.png';
import rime_hero_s1 from '/img/instruments/videomancer/rime/rime_hero_s1.png';
import rime_hero_s2 from '/img/instruments/videomancer/rime/rime_hero_s2.png';
import rime_hero_s3 from '/img/instruments/videomancer/rime/rime_hero_s3.png';
import rime_hero_s4 from '/img/instruments/videomancer/rime/rime_hero_s4.png';
import rime_hero_s5 from '/img/instruments/videomancer/rime/rime_hero_s5.png';
import rime_hero_s6 from '/img/instruments/videomancer/rime/rime_hero_s6.png';
import rime_ex1_s1 from '/img/instruments/videomancer/rime/rime_ex1_s1.png';
import rime_ex1_s2 from '/img/instruments/videomancer/rime/rime_ex1_s2.png';
import rime_ex1_s3 from '/img/instruments/videomancer/rime/rime_ex1_s3.png';
import rime_ex1_s4 from '/img/instruments/videomancer/rime/rime_ex1_s4.png';
import rime_ex1_s5 from '/img/instruments/videomancer/rime/rime_ex1_s5.png';
import rime_ex1_s6 from '/img/instruments/videomancer/rime/rime_ex1_s6.png';
import rime_ex2_s1 from '/img/instruments/videomancer/rime/rime_ex2_s1.png';
import rime_ex2_s2 from '/img/instruments/videomancer/rime/rime_ex2_s2.png';
import rime_ex2_s3 from '/img/instruments/videomancer/rime/rime_ex2_s3.png';
import rime_ex2_s4 from '/img/instruments/videomancer/rime/rime_ex2_s4.png';
import rime_ex2_s5 from '/img/instruments/videomancer/rime/rime_ex2_s5.png';
import rime_ex2_s6 from '/img/instruments/videomancer/rime/rime_ex2_s6.png';
import rime_ex3_s1 from '/img/instruments/videomancer/rime/rime_ex3_s1.png';
import rime_ex3_s2 from '/img/instruments/videomancer/rime/rime_ex3_s2.png';
import rime_ex3_s3 from '/img/instruments/videomancer/rime/rime_ex3_s3.png';
import rime_ex3_s4 from '/img/instruments/videomancer/rime/rime_ex3_s4.png';
import rime_ex3_s5 from '/img/instruments/videomancer/rime/rime_ex3_s5.png';
import rime_ex3_s6 from '/img/instruments/videomancer/rime/rime_ex3_s6.png';

# Rime

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: rime_source1_skull, after: rime_hero_s1 },
    { label: "Boat", before: rime_source2_boat, after: rime_hero_s2 },
    { label: "Clouds", before: rime_source3_clouds, after: rime_hero_s3 },
    { label: "Pattern", before: rime_source4_pattern, after: rime_hero_s4 },
    { label: "Man", before: rime_source5_man, after: rime_hero_s5 },
    { label: "Knit", before: rime_source6_knit, after: rime_hero_s6 },
  ]}
/>
*Rime compositing six-fold symmetric ice crystal dendrites over input video, with DLA-grown branching patterns and glacial blue tint.*

---

## Overview

In 1885, a Vermont farmer named Wilson Bentley attached a bellows camera to a compound microscope and captured the first photomicrograph of a snowflake. What he revealed — that every crystal was a unique six-fold symmetric structure of branching ice needles — launched a century of fascination with the geometry of frozen water. Rime brings that geometry into the video domain: a procedural crystal growth engine generates dendritic ice patterns in real time and composites them over the input video as a semi-transparent frost overlay.

The program implements diffusion-limited aggregation (DLA) in a reduced-resolution binary field stored in BRAM (120×90 cells, 10,800 bits). Growth proceeds by scanning the field during vertical blanking: empty cells adjacent to frozen neighbors are candidates for freezing, with the probability controlled by a branch-density threshold and LFSR-seeded stochasticity. Six-fold crystallographic symmetry is enforced by folding all display coordinates into a single 60-degree wedge before looking up the crystal field, then replicating the result across six sectors. An optional 4-fold mode switches to simple quadrant mirroring.

At subtle settings — low growth rate, moderate opacity, gentle ice tint — Rime adds a delicate frost tracery to the video, like breath condensing on a cold window. At extreme settings — maximum growth, high opacity, full tint — the crystal field can consume the entire frame, transforming the input into an abstract frozen landscape of branching white structures.

---

## Background

### Diffusion-Limited Aggregation

DLA is a growth model proposed by Witten and Sander in 1981 to explain the branching, dendritic structures found in nature — from frost crystals to mineral deposits to lightning. In the classical model, particles undergo random walks and aggregate upon contact with an existing cluster, producing tree-like structures with fractal dimension around 1.7. Rime implements a simplified grid-based DLA: during each vblank scan, an empty cell freezes if it has enough frozen cardinal neighbors (meeting the branch-density threshold) or with LFSR-gated probability if it has at least one. This produces the characteristic branching patterns without requiring particle random walks.

### Six-Fold Crystallographic Symmetry

The hexagonal symmetry of ice crystals arises from the molecular geometry of water: hydrogen bonds lock each water molecule to four neighbors in a tetrahedral arrangement that, in the basal plane, produces a hexagonal lattice. Rime enforces this symmetry computationally by mapping all screen coordinates into a single canonical 60-degree wedge through a coordinate fold. The fold uses the approximation: if `|Δy| > |Δx| + |Δx|/2 + |Δx|/4` (approximately `|Δy| > 1.75|Δx|`), the axes are swapped and Y is halved. The result is that one sector of the crystal field appears replicated six times around the center of the screen.

### Frost Opacity and Ice Tint

Where the crystal field is frozen, Rime blends a configurable ice color over the input video using alpha compositing. In additive mode, the ice color (bright, slightly blue-shifted) is blended additively, brightening the image where crystals appear. In subtractive mode, the video is darkened proportionally, creating shadowed frost regions. The Ice Color pot controls the hue of the frost overlay through a simple UV offset derived from the 10-bit register: U shifts positive and V shifts negative with increasing register value, producing blue-cyan tones at the default center position.

### Melt Dynamics

The Melt Rate control enables a background erosion process: during the growth scan, the LFSR occasionally selects random field addresses and clears them, removing frozen cells. This creates a dynamic equilibrium where growth at the crystal front competes with random melt behind it. At high melt rates the crystal never fills the field, producing a perpetually evolving frontier. The auto-reset toggle provides an alternative cycle: when the frozen count exceeds 75% of the field, the entire BRAM is cleared and growth restarts from the seed points.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Display Pipeline ───────────────────────────────────────────
│   │
│   ├─ 1. Sector Mapping         (screen → canonical wedge via 6/4-fold)
│   ├─ 2. BRAM Lookup             (read crystal bit from packed field)
│   ├─ 3. Crystal Compositor      (frozen: alpha blend ice color over video
│   │                               unfrozen: pass through input)
│   └─ 4. Output Register         (valid signal staging)
│
├── Growth Engine (vblank-only) ────────────────────────────────
│   │
│   ├─ A. Seed Placement          (center of field, 1–6 points)
│   ├─ B. Scan + Neighbor Count   (4 cardinal neighbors per cell)
│   ├─ C. Freeze Decision         (threshold ≥ or LFSR-gated)
│   ├─ D. Melt Erosion            (LFSR random cell clear)
│   └─ E. Auto-Reset              (clear BRAM at 75% fill)
│
├── Mix Stage ──────────────────────────────────────────────────
│   └─ 5. Interpolator Mix        (3× interpolator_u wet/dry)
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock pipeline delay
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select processed or input signal
```

The display pipeline and growth engine operate in different time domains. The growth engine runs only during vertical blanking: it scans the entire 120×90 field up to `growth_max` times per vblank, checking each cell's four cardinal neighbors. The freeze decision uses a two-tier test — cells with neighbors meeting the branch-density threshold freeze unconditionally, while cells with at least one neighbor freeze only if two specific LFSR bits are both high (25% probability). The display pipeline runs at full pixel rate: it maps each screen pixel into the canonical wedge, looks up the corresponding crystal bit from the packed BRAM, and composites the ice color over the input video at the configured opacity. Three `interpolator_u` instances handle the final wet/dry mix.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Growth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls the DLA growth rate by setting the maximum number of full-field scan iterations performed per vertical blanking interval. The 10-bit register is divided by 64 to give 0–15 iterations per frame. At low values, crystals grow slowly — you can watch individual branches extend over seconds. At maximum, the crystal fills rapidly, often reaching the auto-reset threshold within a few seconds. Zero growth freezes the crystal at its current state.

---

#### Knob 2 — Seeds
| Property | Value |
|----------|-------|
| Range | 1 – 6 |
| Default | 1 |

Sets the number of seed points planted at the center of the crystal field. Steps_4 quantization divides the register into 4 zones: 1, 2, 3, or 6 seeds. More seeds produce denser initial nucleation and faster field coverage. With 6 seeds, the six-fold symmetry creates a hexagonal rosette of branches; with 1 seed, growth is more asymmetric and exploratory.

---

#### Knob 3 — Branch
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the neighbor threshold for the DLA freeze decision. Higher branch density (higher register values) lowers the threshold, making it easier for empty cells to freeze — producing denser, more filled-in crystal structures rather than sparse tendrils. At low density, only cells with multiple frozen neighbors freeze deterministically, creating thin, spidery branches. At high density, single-neighbor freezing dominates, producing solid masses.

---

#### Knob 4 — Opacity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 68.4% |
| Suffix | % |

Sets the alpha opacity of the crystal overlay when compositing over the input video. At zero opacity, crystals are invisible. At maximum, frozen regions completely replace the input with the ice color. The Growth Vis toggle overrides this to full opacity, highlighting the active growth front for diagnostic observation.

---

#### Knob 5 — Ice Color
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |
| Suffix | ° |

Controls the hue of the ice crystal overlay through UV offset. The 10-bit register is centered at 512 (neutral). Values above 512 shift U positively and V negatively, producing blue-cyan tones. Values below 512 shift in the opposite direction, producing warm tints. The Y component of the ice color is fixed at 900 (bright), so the overlay always appears luminant. This control lets you choose between the naturalistic icy-blue default and creative tint alternatives.

---

#### Knob 6 — Melt Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the melt erosion rate. When non-zero, the growth engine uses its LFSR to randomly select cells and clear them during each scan step — but only when the upper 4 LFSR bits match a specific pattern (1/16 probability per step). Higher melt rates increase the frequency of these erasure events. At zero, no melting occurs and crystals grow monotonically until auto-reset or manual clearing. At high values, the crystal is in constant flux — growing at the front, melting behind.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Frost** | Add | Sub |
| **8 — AutoReset** | Off | On |
| **9 — GrowthVis** | Off | On |
| **10 — Symmetry** | 6-fold | 4-fold |
| **11 — Bypass** | Off | On |

The five toggles control independent aspects of the crystal rendering. Frost Mode selects additive or subtractive compositing. Auto Reset enables automatic BRAM clearing at 75% fill. Growth Vis forces full opacity to show the crystal front. Symmetry switches between 6-fold (hexagonal) and 4-fold (quadrant) mirroring. Bypass routes the input past all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix crossfade between the unprocessed input video and the crystal-composited output. Three parallel `interpolator_u` instances blend Y, U, and V channels independently using 10-bit fractional precision. At 0% the output is pure dry (original input); at 100% the output is the fully frosted composite.

---

## Guided Exercises

These exercises explore the crystal growth dynamics, opacity compositing, and symmetry modes that define Rime's glacial aesthetic.

### Exercise 1: Gentle Frost Overlay

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: rime_source1_skull, after: rime_ex1_s1 },
    { label: "Boat", before: rime_source2_boat, after: rime_ex1_s2 },
    { label: "Clouds", before: rime_source3_clouds, after: rime_ex1_s3 },
    { label: "Pattern", before: rime_source4_pattern, after: rime_ex1_s4 },
    { label: "Man", before: rime_source5_man, after: rime_ex1_s5 },
    { label: "Knit", before: rime_source6_knit, after: rime_ex1_s6 },
  ]}
/>
*Gentle Frost Overlay — simulated result across source images.*
**Source**: A live camera feed or recorded footage with warm colors and mid-range tonal variation.

**Objective**: Create a subtle frost effect that adds delicate ice tracery over the input video.

1. Set Growth to about 30% for slow crystal expansion.
2. Set Seeds to 1 for a single point of origin.
3. Set Branch to about 30% for thin, spidery dendrites.
4. Set Opacity to about 40% for translucent overlay.
5. Set Ice Color to center (512) for default blue-cyan tint.
6. Set Melt Rate to 0% to let the crystal build undisturbed.
7. Watch dendrites slowly extend from the center across the video.

**Key concepts**: Low growth rate allows observation of individual branch extension, single seed creates asymmetric growth, low opacity preserves video visibility beneath the frost

---

### Exercise 2: Dynamic Equilibrium

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: rime_source1_skull, after: rime_ex2_s1 },
    { label: "Boat", before: rime_source2_boat, after: rime_ex2_s2 },
    { label: "Clouds", before: rime_source3_clouds, after: rime_ex2_s3 },
    { label: "Pattern", before: rime_source4_pattern, after: rime_ex2_s4 },
    { label: "Man", before: rime_source5_man, after: rime_ex2_s5 },
    { label: "Knit", before: rime_source6_knit, after: rime_ex2_s6 },
  ]}
/>
*Dynamic Equilibrium — simulated result across source images.*
**Source**: High-contrast footage — strong text, graphics, or architectural video.

**Objective**: Establish a perpetual growth-melt cycle where the crystal front continuously evolves.

1. Set Growth to about 60% for rapid expansion.
2. Set Seeds to 6 for full hexagonal nucleation.
3. Set Branch to about 50% for moderate density.
4. Set Opacity to about 70% for clearly visible frost.
5. Set Melt Rate to about 40% to compete with growth.
6. Enable AutoReset in case growth outpaces melt.
7. Observe the crystal front advancing and retreating in perpetual flux.

**Key concepts**: Melt erasure competes with DLA growth at the crystal boundary, auto-reset provides a safety net if growth dominates, 6 seeds with high growth rate fill the frame quickly

---

### Exercise 3: Subtractive Shadow Crystal

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: rime_source1_skull, after: rime_ex3_s1 },
    { label: "Boat", before: rime_source2_boat, after: rime_ex3_s2 },
    { label: "Clouds", before: rime_source3_clouds, after: rime_ex3_s3 },
    { label: "Pattern", before: rime_source4_pattern, after: rime_ex3_s4 },
    { label: "Man", before: rime_source5_man, after: rime_ex3_s5 },
    { label: "Knit", before: rime_source6_knit, after: rime_ex3_s6 },
  ]}
/>
*Subtractive Shadow Crystal — simulated result across source images.*
**Source**: Bright, well-lit footage — outdoor scenes, stage lighting, or white backgrounds.

**Objective**: Use subtractive frost mode to create shadowed crystal patterns that darken the input.

1. Set Growth to about 50%.
2. Set Seeds to 3 for moderate nucleation.
3. Set Branch to about 70% for dense, filled-in crystal regions.
4. Set Opacity to about 80% for deep shadows.
5. Switch Frost toggle to Sub (subtractive mode).
6. Set Ice Color to about 30% for warm shadow tones.
7. Switch Symmetry to 4-fold to observe square mirroring.
8. Watch frozen regions darken the video, creating frost-shadow compositions.

**Key concepts**: Subtractive mode darkens instead of brightening, high branch density creates solid crystal masses rather than filigree, 4-fold symmetry produces rectilinear patterns

---


## Tips

- **Growth Rate is temporal resolution**: Low growth lets you watch individual branches form. High growth fills the frame between vblanks.
- **Melt creates living crystals**: Non-zero melt rate produces perpetually evolving patterns. Pair with auto-reset for guaranteed cyclical behavior.
- **Subtractive mode for dark scenes**: Sub mode creates frost shadows on bright sources — useful when you want darkening rather than brightening.
- **6-fold symmetry is natural ice**: Real ice crystals have hexagonal symmetry. Use 4-fold for unnatural, geometric compositions.
- **Growth Vis is diagnostic**: Toggle it on briefly to see exactly what the crystal field holds, then turn it off for the compositional result.
- **Seeds control early density**: More seeds mean faster initial coverage but also mean the crystal reaches auto-reset sooner.
- **Ice Color at extremes creates warm frost**: Moving Ice Color away from center shifts the tint warm, producing golden or amber frost rather than the default blue-cyan.
- **Feedback routing**: Send Rime's output through a second processing program and back for recursive crystal textures.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha Compositing** | Blending two image layers using a transparency value (alpha) to control the contribution of each layer. |
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for the crystal field storage. |
| **Dendrite** | A branching, tree-like crystal growth pattern produced by diffusion-limited aggregation. |
| **DLA** | Diffusion-Limited Aggregation; a growth model where particles aggregate on contact with an existing cluster, producing branching dendritic structures. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function of its previous state, producing pseudo-random sequences. |
| **Nucleation** | The initial formation of a crystal seed point from which further growth propagates. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Sector Mapping** | Folding screen coordinates into a canonical wedge region to enforce rotational symmetry in the rendered pattern. |
| **Six-Fold Symmetry** | The rotational symmetry of ice crystals, where the pattern repeats every 60 degrees around the central axis. |
| **Vblank** | Vertical blanking interval; the period between video frames when no active pixels are displayed, used here for the growth engine scan. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
