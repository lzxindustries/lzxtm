---
draft: true
sidebar_position: 67
slug: /instruments/videomancer/coral
title: "Coral"
image: /img/instruments/videomancer/coral/coral_hero.png
description: "Coral simulates the vertical growth of a reef structure from the edge of the frame."
---

![Coral hero image](/img/instruments/videomancer/coral/coral_hero_s1.png)
*Glowing coral colonies rising from the screen edge, branching and splitting as LFSR-driven growth fills the frame with organic structure.*

---

## Overview

**Coral** is a generative program that grows branching reef structures from the edge of the screen. Four vertical columns extend frame by frame toward the opposite edge, and a pseudorandom number generator triggers ***splits*** that transfer growth energy between neighboring branches. The result is an ever-expanding network of coral-like bands whose shape is governed by chance and a handful of controls.

Because Coral overlays its synthesized structures on whatever video signal is passing through the chain, feeding it interesting source material creates layered composites. At low growth speeds, the reef emerges slowly: a single branch creeping upward one pixel at a time. At high speeds, the entire screen can fill with coral in seconds, completely overtaking the source image.

:::tip
Coral is classified as a ***synthesis*** program: the reef structures are generated entirely inside the FPGA, not derived from the input video. The input signal is still visible wherever coral hasn't grown.
:::

### What's In a Name?

***Coral*** takes its name directly from the marine organism. Coral reefs grow by depositing hard mineral structure over time, branching outward and splitting into new colonies when conditions are right. This program models that behavior: vertical branches extend from an origin edge, an LFSR decides when and where to split, and a depth-based color gradient darkens the roots (just as living coral darkens in deeper water.)

---

## Quick Start

1. With all controls at their defaults, watch the four coral branches grow upward from the bottom of the screen. Growth is continuous and automatic (the reef is already alive.)
2. Turn **Branch D** (Knob 2) counterclockwise and then clockwise. The branches become thinner or wider, changing the weight of each column.
3. Sweep **Color Grd** (Knob 4) from minimum to maximum. The roots of each branch darken progressively, adding depth to the structure.
4. Flip **Palette** (Toggle 8) to **Neon**. The warm orange-pink coral shifts to a cool blue. Flip **Species** (Toggle 7) to **Pillar** and the reef inverts, growing downward from the top of the screen.

---

## Parameters

![Videomancer front panel with Coral loaded](/img/instruments/videomancer/coral/coral_control_panel.png)
*Videomancer's front panel with Coral active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Grow Spd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Grow Spd** sets the vertical growth rate: how many pixels each branch extends per video frame. At the lowest setting the reef creeps upward one pixel at a time, giving you a long, contemplative growth sequence. As you turn the knob clockwise, branches accelerate, and the screen fills with coral much more quickly.

Because growth is clamped to the visible height of the screen, even the fastest setting cannot cause branches to overshoot. Once a branch reaches the opposite edge it simply stops elongating, and the reef holds its shape until you trigger a reset.

---

### Knob 2 — Branch D

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Branch D** controls the horizontal diameter of each coral column. At minimum, branches are thin two-pixel lines. Turning the knob clockwise widens them into broad bands up to about thirty pixels across. Wider branches overlap sooner when spacing is tight, merging into a solid curtain of color.

:::note
Branch diameter is uniform across all four columns. There is no per-branch width control (the entire reef shares one thickness setting.)
:::

---

### Knob 3 — Branch Th

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Branch Th** governs the horizontal spacing between coral columns. At low values the four branches cluster tightly together at the left side of the screen. As you increase the knob, the columns spread apart, pushing the rightmost branches further across the frame. At extreme settings only one or two branches remain visible on screen while the rest drift off the right edge.

Think of this as a ***thinning*** control: higher values thin out the visible reef by spreading branches apart, while lower values pack them densely together.

---

### Knob 4 — Color Grd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Color Grd** adjusts the strength of the depth-based color gradient that darkens branches near their root. At the lowest setting, the gradient is very subtle: branches appear nearly uniform in brightness from root to tip. As you increase the knob, the darkening near the origin edge becomes more pronounced, creating a sense of depth: roots recede into shadow while tips glow brightly.

The gradient operates in four discrete strength levels, so you will notice distinct steps as you sweep the knob rather than a perfectly smooth transition.

:::tip
Combine a strong gradient with low **Grow Spd** to watch the shading develop slowly as each branch extends. The tip stays bright while the root behind it gradually falls into shadow.
:::

---

### Knob 5 — Max Hght

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Max Hght** controls how frequently branches split and transfer growth energy to their neighbors. At minimum, splits are extremely rare and each branch grows independently in a straight column. As you increase the knob, the LFSR-based split mechanism fires more often: a randomly chosen branch donates a quarter of its accumulated height to an adjacent column, accelerating that neighbor's growth.

At high settings, splits happen nearly every frame, creating a cascade of shared growth that fills the screen rapidly. The visual result is that branches appear to race each other: one surges ahead, splits its energy sideways, and the neighbor catches up.

---

### Knob 6 — Angle Sp

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Angle Sp** determines the opacity of the coral overlay where it covers the source video. Below the halfway point, coral pixels are blended fifty-fifty with the underlying source, producing a translucent reef through which the input image remains clearly visible. Above the halfway point, coral pixels completely replace the source, producing fully opaque branches.

:::note
This control behaves as a binary threshold, not a smooth crossfade. You will see a distinct shift at the midpoint rather than a gradual change in transparency.
:::

---

### Switch 7 — Species

| Property | Value |
|----------|-------|
| Off | Staghorn |
| On | Pillar |
| Default | Staghorn |

**Species** sets the growth direction. In the **Staghorn** position, branches grow upward from the bottom of the screen: like the upward-reaching arms of ***staghorn coral***. In the **Pillar** position, branches grow downward from the top, resembling stalactites or inverted pillar formations. The depth gradient adjusts automatically: roots are always at the origin edge and tips always at the growing end.

---

### Switch 8 — Palette

| Property | Value |
|----------|-------|
| Off | Reef |
| On | Neon |
| Default | Reef |

**Palette** selects between two color schemes. **Reef** renders branches in warm coral tones: a bright orange-pink luma with reddish chroma: reminiscent of shallow tropical reefs. **Neon** switches to cool blue tones, evoking deep-water bioluminescence. Both palettes are affected by the **Color Grd** depth gradient.

---

### Switch 9 — Current

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Current** triggers a branch reset. When you flip this toggle from Off to On, all four branches are cleared to zero height and the reef begins growing again from scratch. This is an ***edge-triggered*** action: only the transition from Off to On causes a reset. Leaving the toggle in the On position does not continuously reset.

:::warning
Resetting during a performance erases the entire reef instantly. There is no undo (growth must start over from the origin edge.)
:::

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** is reserved for future use. In the current implementation, growth is always active regardless of this toggle's position. The reef grows continuously each frame whether Animate is set to Off or On.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all coral rendering. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the coral-composited result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (original input) and wet (coral-composited) signal. At minimum, only the original input passes through: no coral is visible. At maximum, the full coral composite is shown. Intermediate positions blend the two proportionally.

This is the final stage in the processing chain and operates independently of the **Angle Sp** opacity control. Even if coral branches are fully opaque, the Mix fader can dissolve them into the source signal.

---

## Background

### Procedural growth simulation

Coral models a simplified version of ***L-system*** growth: the mathematical framework biologists use to describe branching patterns in plants, corals, and other organisms. In a full L-system, a set of rewriting rules generates arbitrarily complex branching structures. Coral distills this idea to its essence: four columns grow at a fixed rate, and a random process decides when to share growth with a neighbor. The result captures the visual character of branching growth without the computational cost of a full recursive system.

### LFSR-based randomness

The splitting decision relies on a 16-bit ***linear feedback shift register*** (LFSR), a classic hardware random number generator. Each clock cycle the LFSR shifts its bits and feeds back a combination through XOR gates, producing a pseudorandom sequence that repeats only after 65,535 steps. The program compares the low ten bits of the LFSR output against the split-rate threshold: if the random value falls below the threshold, a split occurs. Higher thresholds mean more frequent splits, and therefore faster, more chaotic growth.

The LFSR also selects ***which*** branch splits (bits 14–13 choose the source column) and ***which direction*** the split transfers (bit 12 picks left or right neighbor). This ensures that splits are distributed across all branches rather than favoring one column.

### Depth gradient shading

Living coral colonies darken with depth: sunlight attenuates as it passes through water, so deeper structures receive less illumination. Coral's depth gradient models this effect digitally. The program computes a vertical ramp from the growing tip (bright) to the root (dark) and subtracts it from the base luma value. The gradient strength is quantized to four levels controlled by the top two bits of the **Color Grd** parameter, keeping the logic simple and avoiding a full multiplier.


---

## Signal Flow

### Signal Flow Notes

The most important architectural feature is the ***separation between frame-level and pixel-level processing***. All growth, splitting, and position computations happen once per frame at the vsync trigger. The per-pixel pipeline then simply tests whether each pixel falls within any branch's pre-computed bounds: a fast parallel range check with no per-pixel arithmetic beyond comparison.

The hit detection tests all four branches simultaneously in a single clock cycle. Pre-computed horizontal bounds (xleft and xright) eliminate the need for per-pixel subtraction, keeping the critical path short. The vertical test checks whether the pixel's line number is within the branch's extent, accounting for growth direction.

:::note
Because branch positions and bounds are updated only at vsync, the reef structure is rock-stable within each frame. There is no mid-frame tearing or partial update (every pixel sees the same branch geometry.)
:::


---

## Exercises

These exercises explore Coral's growth dynamics, from slow single-column emergence to rapid screen-filling reef cascades. Because Coral is a synthesis program, no specific source material is required (any input signal (or none) works.)
### Exercise 1: Slow Growth Study

![Slow Growth Study result](/img/instruments/videomancer/coral/coral_ex1_s1.png)
*Slow Growth Study — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A slow, meditative growth sequence where four thin branches emerge from the bottom edge over thirty seconds, shaded from dark roots to bright tips.

#### Key Concepts

- Growth rate and branch width define the visual weight
- The depth gradient adds three-dimensional shading
- Resetting clears all branches for a fresh start

#### Steps

1. Flip **Current** (Toggle 9) to On, then back to Off (this resets all branches to zero.)
2. Set **Grow Spd** (Knob 1) fully counterclockwise for the slowest growth rate.
3. Set **Branch D** (Knob 2) to about 20% for narrow columns.
4. Turn **Color Grd** (Knob 4) fully clockwise for maximum depth shading.
5. Set **Max Hght** (Knob 5) fully counterclockwise to suppress splits (each branch grows independently.)
6. Watch the four columns creep upward. Notice how the roots darken while the tips stay bright.
7. After about thirty seconds, flip **Species** (Toggle 7) to **Pillar** and reset with **Current**. Now growth descends from the top.

#### Settings

| Control | Value |
|---------|-------|
| Grow Spd | 0% |
| Branch D | 20% |
| Branch Th | 50% |
| Color Grd | 100% |
| Max Hght | 0% |
| Angle Sp | 100% |
| Species | Staghorn |
| Palette | Reef |
| Current | Off |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Split Cascade

![Split Cascade result](/img/instruments/videomancer/coral/coral_ex2_s1.png)
*Split Cascade — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A fast-growing reef where frequent splits cause branches to race each other across the screen, creating an unpredictable cascade pattern.

#### Key Concepts

- Split rate controls how often growth transfers between branches
- Spacing affects how many branches are visible on screen
- The LFSR makes every growth sequence unique

#### Steps

1. Reset branches via **Current** (Toggle 9).
2. Set **Grow Spd** (Knob 1) to about 40% for moderate growth.
3. Turn **Max Hght** (Knob 5) to about 80%. Splits will fire frequently, transferring growth energy between neighbors.
4. Set **Branch Th** (Knob 3) to about 30% so all four branches cluster together on screen.
5. Watch the branches compete: one surges ahead, donates growth sideways, and its neighbor catches up. The pattern is different every time because the LFSR sequence determines split timing and direction.
6. Now widen **Branch D** (Knob 2) to about 60%. The thick columns overlap, merging into a solid curtain where branches are close together.
7. Switch **Palette** (Toggle 8) to **Neon** and reset. Observe the same cascade in cool blue tones.

#### Settings

| Control | Value |
|---------|-------|
| Grow Spd | 40% |
| Branch D | 60% |
| Branch Th | 30% |
| Color Grd | 50% |
| Max Hght | 80% |
| Angle Sp | 50% |
| Species | Staghorn |
| Palette | Neon |
| Current | Off |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Translucent Reef Overlay

![Translucent Reef Overlay result](/img/instruments/videomancer/coral/coral_ex3_s1.png)
*Translucent Reef Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A layered composition where translucent coral branches float over the input video, visible but not obscuring the source entirely.

#### Key Concepts

- Coral composites on top of the input signal
- The Angle Sp and Mix controls work together to set final opacity
- Wide spacing reveals the source between branches

#### Steps

1. Feed an interesting video source into the chain: a camera feed, a pattern generator, or another Videomancer program upstream.
2. Reset branches via **Current** (Toggle 9).
3. Set **Angle Sp** (Knob 6) below 50% so coral pixels blend fifty-fifty with the source.
4. Set **Mix** (Fader 12) to about 70%. The crossfade further reduces coral opacity, making the reef ghostly and translucent.
5. Increase **Branch Th** (Knob 3) to spread branches apart, leaving gaps where the source video shows through clearly.
6. Set **Color Grd** (Knob 4) to about 60% so the roots fade into the source image while the tips remain distinct.
7. Slowly sweep **Grow Spd** (Knob 1) from low to moderate. The reef unfurls over the source, creating a layered double-exposure effect.

#### Settings

| Control | Value |
|---------|-------|
| Grow Spd | 30% |
| Branch D | 40% |
| Branch Th | 70% |
| Color Grd | 60% |
| Max Hght | 50% |
| Angle Sp | 30% |
| Species | Staghorn |
| Palette | Reef |
| Current | Off |
| Animate | On |
| Bypass | Off |
| Mix | 70% |

---
## Glossary

- **Clamping**: Limiting a computed value to a fixed range so it cannot overflow or underflow, ensuring stable behavior at parameter extremes.

- **Depth Gradient**: A vertical brightness ramp that darkens coral branches near their origin edge, simulating the way sunlight attenuates with depth in water.

- **Hit Detection**: The per-pixel test that determines whether a given screen coordinate falls within any coral branch's horizontal and vertical bounds.

- **Interpolator**: A hardware crossfade block that smoothly blends between two input values based on a fractional mix parameter.

- **L-System**: A formal grammar for modeling branching growth in biological organisms, simplified here to fixed-rate vertical extension with random splits.

- **LFSR**: Linear Feedback Shift Register: a hardware circuit that generates pseudorandom bit sequences by shifting and XOR-feeding back selected taps.

- **Pseudorandom**: A deterministic sequence that appears random but repeats after a fixed period; the LFSR16 used here cycles every 65,535 steps.

- **Split**: The transfer of growth energy from one coral branch to an adjacent neighbor, triggered by the LFSR when its output falls below the split-rate threshold.

- **Vsync**: The vertical synchronization pulse marking the start of each video frame, used here as the trigger for all frame-level growth and split computations.

- **YUV**: A color encoding that separates brightness (Y) from color information (U and V), used throughout the Videomancer video pipeline.

---
