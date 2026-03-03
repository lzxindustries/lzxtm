---
draft: true
sidebar_position: 322
slug: /instruments/videomancer/vermiform
title: "Vermiform"
image: /img/instruments/videomancer/vermiform/vermiform_hero.png
description: "Vermiform recreates the hypnotic crawling-worm screensavers that defined the late 1980s and early 1990s desktop computing era."
---

import vermiform_hero from '/img/instruments/videomancer/vermiform/vermiform_hero.png';
import vermiform_animation from '/img/instruments/videomancer/vermiform/vermiform_animation.gif';
import vermiform_control_panel from '/img/instruments/videomancer/vermiform/vermiform_control_panel.png';
import vermiform_exercise1_result from '/img/instruments/videomancer/vermiform/vermiform_exercise1_result.gif';
import vermiform_exercise2_result from '/img/instruments/videomancer/vermiform/vermiform_exercise2_result.gif';
import vermiform_exercise3_result from '/img/instruments/videomancer/vermiform/vermiform_exercise3_result.gif';

# Vermiform

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={vermiform_hero} alt="Vermiform hero image"/>
*Vermiform transforming a live video feed into a gradually revealed image as four coloured worm agents crawl across a persistent 1-bit canvas, painting sinusoidal trails that expose the source through an After Dark–inspired screensaver mechanic.*
<img src={vermiform_animation} alt="Vermiform animated output"/>
*Vermiform output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Vermiform recreates the hypnotic crawling-worm screensavers that defined the late 1980s and early 1990s desktop computing era. Up to four autonomous worm agents move across the screen in smooth, sinusoidal paths, leaving persistent trails on a 1-bit BRAM canvas. Where a worm has passed, the input video is revealed at full brightness; where no worm has visited, the video is dimmed or blacked out entirely. The result is a living reveal effect — the source image emerges gradually as the worms explore the frame, then the canvas resets and the process begins anew.

The name "vermiform" means "worm-shaped," referring to the tubular, meandering paths the agents trace. Each worm carries an 8-bit heading angle updated every frame by an LFSR-modulated steering signal scaled through a quarter-wave sine lookup table. This produces the characteristic smooth, organic curves — never sharp corners, never straight lines — that made the original After Dark screensaver so mesmerising. The heading perturbation is random but continuous, creating paths that resemble the trails of real organisms navigating by chemotaxis.

At subtle settings with high canvas dim and a single worm, Vermiform produces a slow, meditative reveal where the source video appears through a wandering spotlight. With four worms, high speed, maximum turn rate, and low dim, the effect becomes a chaotic, rapidly-filling canvas where the video is almost immediately visible but perpetually interrupted by coverage resets that wipe the slate and begin again.

---

## Background

### Screensaver Culture and Generative Art

The screensaver emerged in the 1980s as a practical solution to phosphor burn-in on CRT monitors, but quickly evolved into a platform for generative art. Berkeley Systems' After Dark (1989) transformed the genre with modules like "Flying Toasters" and "Worms" — programs that ran autonomously, producing endlessly varying visual output from simple algorithmic rules. The "Worms" module specifically used bounded random walks to paint coloured trails on a black canvas, creating organic patterns that audiences found inexplicably compelling. Vermiform brings this generative tradition into the video synthesis domain, replacing the black background with live video and the coloured trails with a reveal mask.

### Random Walks and Bounded Movement

A random walk is a mathematical formalisation of a path consisting of successive random steps. In its simplest form — a drunkard's walk — each step direction is completely independent. Vermiform uses a more structured variant: a persistent random walk where each step's direction is a small perturbation of the previous heading. This produces correlated motion with smooth curves rather than the jagged zigzag of a pure random walk. The LFSR provides the random perturbation, the Turn Rate control scales its magnitude, and the sine/cosine lookup converts the heading angle to Cartesian displacements. Boundary handling (wrap or bounce) ensures the worms remain within the visible frame.

### LFSR-Driven Pseudo-Randomness

A Linear-Feedback Shift Register generates a deterministic but apparently random sequence of bits by XORing selected taps and feeding the result back into the register. Vermiform's 16-bit LFSR with the polynomial $x^{16} + x^{15} + x^{13} + x^{4} + 1$ produces a maximal-length sequence of 65535 states before repeating. The Seed control loads a different initial state into the LFSR, producing an entirely different sequence of steering perturbations and therefore different worm paths. Because the sequence is deterministic for a given seed, the same seed always produces the same worm trajectories — useful for repeatable visual compositions.

### Quarter-Wave Sine Lookup Tables

Computing sine and cosine on FPGA fabric without a hardware multiplier requires a lookup table. Vermiform stores only 64 entries covering the first quarter-wave (0° to 90°) and derives the remaining three quadrants through index mirroring and sign negation. The cosine function is simply the sine with a 90° phase offset. This quarter-wave technique reduces the table to one-quarter its full size while maintaining 8-bit amplitude resolution — sufficient for smooth worm steering at pixel-level granularity.

### Coverage Tracking and Canvas Reset

The canvas is a 1-bit-per-cell BRAM array, where each bit records whether a worm has visited that cell. A 14-bit coverage counter increments each time a worm paints a previously unvisited cell. When the counter exceeds the reset threshold (set by the Reset % control), the entire canvas is sequentially cleared over approximately 8160 clock cycles and the coverage counter resets to zero. This creates the characteristic screensaver rhythm: gradual reveal → coverage threshold → complete reset → new reveal cycle.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Worm Update (vblank) ────────────────────────────────────
│   │
│   ├─ 1. Steer heading: heading += LFSR × Turn Rate
│   ├─ 2. Move forward: (x,y) += speed × (cos(heading), sin(heading))
│   ├─ 3. Boundary: wrap around edges or bounce off edges
│   └─ 4. Paint trail: canvas[cell_x, cell_y] = 1; coverage++
│
├── Canvas Read ─────────────────────────────────────────────
│   │
│   └─ 5. For current pixel: read canvas[cell] → painted flag
│
├── Invert ──────────────────────────────────────────────────
│   │
│   └─ 6. If Invert enabled: flip painted/unpainted sense
│
├── Region Mux ──────────────────────────────────────────────
│   │
│   ├─ 7a. Worm head hit: output fixed worm colour (3×3 dot)
│   ├─ 7b. Painted cell: pass through input video at full brightness
│   └─ 7c. Unpainted cell: dim video by Cvs Dim amount
│
├── Coverage Reset ──────────────────────────────────────────
│   │
│   └─ 8. If coverage ≥ Reset % threshold: clear entire canvas
│
├── Mix ─────────────────────────────────────────────────────
│   └─ Interpolator: dry (original) ↔ wet (worm reveal)
│
└── Bypass ──────────────────────────────────────────────────
    └─ Select original or processed signal
```

The worm update runs exclusively during the vertical blanking interval, ensuring that all worm movement and canvas painting complete before the active video region begins. This means worms advance once per frame regardless of the pixel clock. The canvas read and rendering pipeline then operate at full pixel rate during active video, looking up each pixel's cell in the canvas BRAM and selecting the appropriate output: worm head colour, revealed video, or dimmed video. The coverage reset is also sequential — rather than clearing the entire BRAM in one cycle, it walks through addresses one per clock during vblank to avoid corrupting in-flight reads.

The cell size toggle directly affects the visual granularity of the reveal. Fine mode (8×8 pixels per cell) produces a sharper, more detailed reveal mask at the cost of requiring more worm travel to achieve full coverage. Coarse mode (16×16 pixels per cell) creates a blockier, more pixelated reveal that fills faster. The canvas BRAM dimensions remain constant; fine mode simply maps to a larger effective grid by shifting fewer address bits.

---

## Parameter Reference

<img src={vermiform_control_panel} alt="Videomancer front panel with Vermiform loaded"/>
*Videomancer's front panel with Vermiform active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the forward movement speed of each worm in pixels per frame. At zero, worms are nearly stationary, creeping forward at one pixel per frame. As Speed increases, worms cover more ground each frame, reaching up to eight pixels per step at maximum. Higher speeds mean the canvas fills more quickly and the reveal cycle is shorter. The visual character changes too — slow worms leave tightly packed, detailed trails with visible curvature, while fast worms create broader, more sweeping arcs that skip over intermediate cells.

---

#### Knob 2 — Turn Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the maximum steering perturbation applied to each worm's heading per frame. At zero, worms travel in nearly straight lines with minimal deviation — the LFSR steering signal is scaled to near-zero amplitude. As Turn Rate increases, the heading change per frame grows, producing tighter curves and more erratic paths. At maximum, worms can reverse direction within a few frames, creating dense, tangled trail patterns. The steering is always smooth because it modifies the heading angle incrementally rather than choosing random directions.

---

#### Knob 3 — Worms
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Selects the number of active worm agents from one to four. With one worm, the reveal is slow and focused — a single trail winds across the frame like a solitary explorer. Two worms create a dialogic composition with interleaving paths. Three and four worms fill the canvas progressively faster, creating denser trail networks that reach coverage threshold sooner. Each worm is initialised at a different position (roughly one per quadrant) with evenly spaced heading angles, ensuring initial coverage is distributed across the frame.

---

#### Knob 4 — Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Loads a different initial state into the 16-bit LFSR, producing an entirely different sequence of steering perturbations. Each seed value generates a unique set of worm trajectories — the same seed always produces the same paths, enabling repeatable compositions. Sweeping Seed during live performance continuously re-seeds the LFSR, causing the worms to abruptly change their steering behaviour. This is most visible at low speed and high turn rate, where the path character is dominated by the LFSR sequence.

---

#### Knob 5 — Cvs Dim
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 92.9% |
| Suffix | % |

Controls the brightness of unpainted canvas areas. At zero, unpainted regions pass the input video at full brightness — there is no dimming distinction between painted and unpainted cells, effectively making the canvas invisible. As Cvs Dim increases, unpainted areas become progressively darker. At maximum, unpainted regions are completely black, creating the classic screensaver look where only worm trails reveal the underlying video. At high dim values, the chroma channels of unpainted regions are also forced to neutral gray, preventing colour bleeding from fully dimmed areas.

---

#### Knob 6 — Reset %
| Property | Value |
|----------|-------|
| Range | 50.0% – 100.0% |
| Default | 94.0% |
| Suffix | % |

Sets the coverage threshold at which the canvas resets. The threshold maps to a percentage of total canvas cells. At low values, the canvas resets when only half the cells have been painted — the reveal cycle is short and the video never fully appears. At high values, the canvas must be nearly fully covered before resetting, allowing the entire frame to be revealed before the cycle restarts. At maximum, the canvas is essentially permanent until nearly every cell has been visited.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Wrap** | Wrap | Bounce |
| **8 — Cell Sz** | Fine | Coarse |
| **9 — Worm Vis** | Hide | Show |
| **10 — Invert** | Normal | Invert |
| **11 — Bypass** | Off | On |

The five toggles configure worm behaviour, visual presentation, and rendering options. Wrap and Cell Sz affect the geometric character of the worm paths and canvas resolution. Worm Vis and Invert alter the visual presentation of the reveal effect. Bypass provides instant comparison with the unprocessed source.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfade between the dry (original) and wet (worm reveal) signals. At 0%, the output is pure unprocessed video. At 100%, the output is the full canvas reveal effect with dimming, worm heads, and inversion. Intermediate values blend the reveal effect over the original video, creating a translucent overlay where dimmed regions are partially visible rather than fully dark.

---

## Guided Exercises

These exercises progress from a single-worm minimal reveal to a complex multi-worm composition, exploring how speed, steering, and canvas parameters interact to create different reveal dynamics.

### Exercise 1: Solitary Explorer

<img src={vermiform_exercise1_result} alt="Solitary Explorer result"/>
*Solitary Explorer — simulated result across source images.*
**Objective**: Create a meditative single-worm reveal that gradually exposes the source image through a wandering trail.

1. **Single slow worm**: Set Worms to 1, Speed to ~25%. A single worm begins its slow crawl across the frame.
2. **Full dimming**: Push Cvs Dim to ~95%. Unpainted areas go nearly black — the video is only visible where the worm has passed.
3. **Gentle curves**: Set Turn Rate to ~40%. The worm traces smooth, sweeping arcs with gentle curvature.
4. **Show the worm**: Toggle Worm Vis to Show. A bright coloured dot marks the worm's current position.
5. **High reset threshold**: Set Reset % to ~95%. The canvas persists until almost every cell is visited, allowing the full image to emerge slowly.

**Key concepts**: Single-worm reveals create a spotlight-like exploration of the source, canvas dim controls the contrast between revealed and hidden areas, high reset threshold allows full coverage before cycling

---

### Exercise 2: Chaotic Swarm

<img src={vermiform_exercise2_result} alt="Chaotic Swarm result"/>
*Chaotic Swarm — simulated result across source images.*
**Objective**: Use four fast worms with high turn rate to create a rapidly cycling reveal with dense, tangled trails.

1. **Maximum worms**: Set Worms to 4. Four worms begin exploring from different quadrants.
2. **High speed and turn**: Speed to ~80%, Turn Rate to ~85%. Worms move quickly with tight, erratic curves.
3. **Moderate dim**: Cvs Dim at ~70%. Unpainted areas are dark but not black, maintaining some background visibility.
4. **Fast cycling**: Set Reset % to ~60%. The canvas resets when 60% covered, creating rapid reveal-reset cycles.
5. **Bounce mode**: Toggle Wrap to Bounce. Worms reflect off edges, concentrating activity toward the centre.
6. **Coarse reveal**: Toggle Cell Sz to Coarse. Larger cells fill faster, creating a blockier but more dynamic pattern.

**Key concepts**: Multiple worms create coverage faster, bounce mode concentrates activity centrally, coarse cells accelerate the reveal cycle, low reset threshold produces rapid cycling

---

### Exercise 3: Negative Reveal

<img src={vermiform_exercise3_result} alt="Negative Reveal result"/>
*Negative Reveal — simulated result across source images.*
**Objective**: Use inverted canvas mode to create a reverse reveal where worm trails darken the image rather than exposing it.

1. **Enable invert**: Toggle Invert to Invert. Now painted cells are dimmed and unpainted cells show the video.
2. **Two worms**: Set Worms to 2 for a balanced composition.
3. **Medium speed**: Speed at ~50%, Turn Rate at ~50%. Moderate worm activity.
4. **Full dim**: Cvs Dim at ~100%. Painted areas go completely black.
5. **High coverage**: Reset % at ~85%. Allow the worms to darken most of the frame before resetting.
6. **Hide worms**: Toggle Worm Vis to Hide. Only the darkening trails are visible, not the agent positions.
7. **Observe the cycle**: As worms trace their paths, the bright source is progressively obscured. At reset, the image snaps back to full visibility.

**Key concepts**: Invert mode reverses the reveal mechanic, creating a darkening effect instead of brightening, high-key sources work best because the darkening trails are most visible against bright backgrounds

---


## Tips

- **Start with one worm**: A single worm reveals the composition of the effect most clearly. Add more worms only after dialling in speed, turn rate, and dim settings.
- **Seed for composition**: Different seeds produce radically different trail patterns. Audition several seeds with low speed and high turn rate to find aesthetically interesting paths before performing live.
- **Reset % shapes the rhythm**: Low reset values create rapid, staccato reveal-reset cycles. High values produce slow, sweeping reveals with dramatic reset moments. Match the cycle length to the tempo of your content.
- **Coarse cells for abstraction**: Coarse cell size turns the reveal into a mosaic-like grid pattern. Combined with moderate dim, this creates a digital tile-reveal aesthetic that works well with geometric source material.
- **Invert for erasure performances**: Use Invert mode with a bright source to create a "drawing with darkness" effect — the worms erase the image rather than revealing it.
- **Turn Rate defines personality**: Low turn rate creates long, sweeping arcs like a gliding bird. High turn rate creates tight, tangled knots like an insect. Mid-range values produce the most organic, lifelike worm trails.
- **Bounce concentrates centre**: When using Bounce mode, worms tend to accumulate near the frame centre. Use this for compositions where the subject is centrally placed.
- **Mix for subtlety**: Partial mix values (40–60%) create a gentle vignetting effect where unpainted areas are slightly dimmed rather than fully dark, useful for atmospheric processing.

---

## Glossary

| Term | Definition |
|------|------------|
| **After Dark** | A popular Macintosh/Windows screensaver program (1989) by Berkeley Systems, featuring modules like "Worms" and "Flying Toasters" that became cultural icons of early personal computing. |
| **BRAM** | Block RAM; dedicated FPGA memory used here as the 1-bit canvas storing trail coverage. |
| **Canvas** | The persistent 1-bit-per-cell array recording which cells have been visited by worm agents. |
| **Coverage Counter** | A 14-bit accumulator tracking the number of painted canvas cells, used to trigger canvas reset. |
| **Heading** | An 8-bit angle (0–255 mapping to 0°–360°) defining each worm's current direction of travel. |
| **LFSR** | Linear-Feedback Shift Register; generates the pseudo-random steering perturbations that create varied worm paths. |
| **Quarter-Wave LUT** | A lookup table storing only 0°–90° of a sine wave, deriving the remaining quadrants through symmetry to save BRAM. |
| **Random Walk** | A mathematical path consisting of successive random steps; Vermiform uses a persistent variant with correlated heading changes. |
| **VBlank** | Vertical blanking interval; the non-visible portion of each video frame during which worm positions are updated. |
| **YUV** | A colour encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
