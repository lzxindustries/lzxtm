---
draft: true
sidebar_position: 156
slug: /instruments/videomancer/kaleidoscope
title: "Kaleidoscope"
image: /img/instruments/videomancer/kaleidoscope/kaleidoscope_hero.png
description: "Kaleidoscope is a faithful recreation of Li-Chen Wang's legendary 1976 demo for the Cromemco Dazzler — one of the earliest consumer video graphics boards."
---

![Kaleidoscope hero image](/img/instruments/videomancer/kaleidoscope/kaleidoscope_hero_s1.png)
*Kaleidoscope generating a four-way symmetric pattern from Li-Chen Wang's 1976 Cromemco Dazzler algorithm, rendered across a 64×64 grid in full-color YUV.*

---

## Overview

**Kaleidoscope** is a synthesis program that recreates one of the earliest real-time computer graphics demos ever written. In 1976, Li-Chen Wang wrote a tiny program for the ***Cromemco Dazzler***: a 64×64-pixel color graphics board for the Altair 8800: that produced endlessly evolving symmetric patterns from a simple pair of feedback equations. Videomancer's Kaleidoscope faithfully implements Wang's algorithm in hardware, running the original iteration engine inside the FPGA at video rate and rendering the results as a full-screen synthesis.

The core loop is deceptively simple. Two coordinates, X and Y, are updated each iteration by shifting and masking each other. The result is plotted with ***four-way mirror symmetry*** across the grid, and the process repeats through a cycle of fifteen colors. When all colors have been visited, the mask value increments, producing an entirely new family of shapes. The algorithm never truly repeats: it wanders through an enormous space of geometric patterns, from tight spirals to crystalline lattices to chaotic scatters.

:::tip
Kaleidoscope is a ***synthesis*** program: it generates imagery from scratch, no input video required. However, the **Mix** fader lets you blend the generated pattern over any video source passing through the chain, creating hybrid compositions.
:::

### What's In a Name?

The name references both the physical optical toy: a tube of mirrors that produces symmetric patterns from tumbling beads: and the program's algorithmic heritage. Wang's original listing was titled "KALEIDOSCOPE" in the Cromemco Dazzler software manual. We've kept the name as a tribute to that pioneering moment in real-time computer graphics, when a few dozen bytes of 8080 assembly could fill a screen with living geometry.

---

## Quick Start

1. Confirm **Run** (Switch 7) is set to **Run** and **Auto Mask** (Switch 8) is set to **Auto**. A pattern should already be evolving on-screen: symmetric shapes in bright Dazzler colors cycling across the grid.
2. Turn **Speed** (Knob 1) clockwise. The pattern updates faster, shapes shifting and mutating more rapidly. Turn it counterclockwise for slow, meditative evolution.
3. Flip **Reset** (Switch 9) to **Reset**, then back to **Off**. The pattern clears and begins a fresh sequence from the current **Seed X** and **Seed Y** values. Try different seed positions to launch new pattern families.
4. Turn **Hue Shift** (Knob 5) to rotate the color palette. The geometry stays the same, but the mood changes entirely (cool blues shift to warm reds and back again.)

---

## Parameters

![Videomancer front panel with Kaleidoscope loaded](/img/instruments/videomancer/kaleidoscope/kaleidoscope_control_panel.png)
*Videomancer's front panel with Kaleidoscope active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Speed** controls how many iterations of Wang's algorithm execute per video frame. At low values, the pattern evolves slowly: you can watch individual plots appear across the grid. At high values the pattern mutates rapidly, with up to 128 iterations landing per frame. The visual effect ranges from a patient, crystalline unfolding to a flickering cascade of shapes. Because the algorithm is deterministic, the same seed and mask values always produce the same sequence, just at different rates.

:::note
At very low Speed settings with a static mask and seeds, you can observe the algorithm plotting individual cells one at a time with four-way symmetry (a direct window into Wang's original step-by-step logic.)
:::

---

### Knob 2 — Seed X

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Seed X** sets the initial X coordinate for the iteration engine. This value is loaded when you trigger a **Reset**. Different seeds launch the algorithm from different starting points in its coordinate space, producing entirely different pattern families from the same mask value. Small changes in the seed can lead to dramatically different visual outcomes thanks to the feedback nature of the iteration.

---

### Knob 3 — Seed Y

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Seed Y** sets the initial Y coordinate, complementing **Seed X**. Together, the two seeds define the starting position in a two-dimensional coordinate space. Because the algorithm feeds X and Y back into each other through shifting and masking, even tiny differences between seeds can produce wildly divergent trajectories.

:::tip
Try setting **Seed X** and **Seed Y** to matching values for symmetric initial conditions, or to opposite extremes for asymmetric launches. Reset after each change to see the effect.
:::

---

### Knob 4 — Mask

| Property | Value |
|----------|-------|
| Range | 0 – 255 |
| Default | 0 |

**Mask** directly sets the AND mask applied to the coordinate feedback terms when **Auto Mask** is disabled. The mask determines which bits of the shifted coordinate survive into the feedback equation, and this single value is the primary source of pattern variety. Low mask values (few bits set) produce sparse, geometric patterns with long, sweeping curves. High mask values (many bits set) produce dense, intricate textures. The mask effectively controls the ***complexity*** of the generated shapes.

When **Auto Mask** is active, this knob has no effect: the mask increments automatically after each full color cycle.

---

### Knob 5 — Hue Shift

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Hue Shift** rotates the sixteen-entry color palette by an offset derived from the knob position. At the default midpoint, the original Dazzler palette is used unmodified. Turning the knob shifts all non-black color indices forward through the palette, wrapping around at the top. This changes the color assignment of every plotted cell without altering the underlying geometry. Fully counterclockwise and fully clockwise produce different rotations of the same palette.

:::tip
Because the palette wraps, certain Hue Shift positions map geometrically distinct color indices onto the same palette entry, creating the illusion of fewer colors. Other positions spread the palette wide. Experiment to find color distributions you like.
:::

---

### Knob 6 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Bright** scales the luminance of every rendered pixel. At the default position (roughly 75%), the Dazzler palette renders at close to its natural brightness. Turning the knob counterclockwise dims the entire pattern toward black. Turning it clockwise pushes brightness higher, with the palette's whites approaching full scale. Brightness scaling is multiplicative: it compresses or expands the tonal range of the sixteen palette colors proportionally.

---

### Switch 7 — Run

| Property | Value |
|----------|-------|
| Off | Pause |
| On | Run |
| Default | Run |

**Run** starts and stops the iteration engine. When set to **Run**, the algorithm advances on every video frame, plotting new cells and cycling colors. When set to **Pause**, the engine halts and the framebuffer holds its current state: the last pattern remains frozen on-screen. This is useful for examining a single frame of the pattern in detail, or for "catching" a particular shape before it mutates away.

---

### Switch 8 — Auto Mask

| Property | Value |
|----------|-------|
| Off | Manual |
| On | Auto |
| Default | Auto |

**Auto Mask** selects between automatic and manual mask progression. In **Auto** mode, the mask increments by one each time the algorithm completes a full pass through all fifteen color levels: this is Wang's original behavior, producing an endless, non-repeating sequence of patterns. In **Manual** mode, the mask is set directly by the **Mask** knob, giving you precise control over which pattern family is displayed. Manual mode is ideal for exploring one mask value in depth or for performances where you want deterministic shapes.

---

### Switch 9 — Reset

| Property | Value |
|----------|-------|
| Off | Off |
| On | Reset |
| Default | Off |

**Reset** clears the framebuffer and re-seeds the iteration engine with the current **Seed X** and **Seed Y** values. Flip the switch to **Reset** and then back to **Off** to trigger a fresh start. The color counter resets to its maximum, the iteration counter clears, and in Auto Mask mode, the mask resets to its starting value. This gives you a clean slate to begin a new pattern sequence.

:::note
Reset is edge-triggered: the engine re-seeds on the transition from Off to Reset. Holding the switch in the Reset position doesn't continuously reset; only the initial flip matters.
:::

---

### Switch 10 — Grid

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Grid** overlays thin lines at cell boundaries, drawing a 64×64 grid across the entire output. The grid lines are rendered as dim, desaturated marks at the first pixel of each cell row and column. This is useful for visualizing the discrete structure of the framebuffer and understanding exactly how the 64×64 grid maps to the full video frame. Each cell occupies 30 pixels wide by 16 pixels tall.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the input video directly to the output, bypassing all Kaleidoscope synthesis and mixing. The sync delay pipeline still operates, so switching produces no glitch. Use Bypass for instant A/B comparison between the synthesis output and the raw input signal.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the wet/dry blend between the Kaleidoscope synthesis and the input video. At 100% (fully clockwise, the default), only the synthesized pattern is visible. At 0%, only the incoming video passes through. Intermediate positions blend the two, allowing you to overlay geometric patterns on live footage. The mix operates independently on Y, U, and V channels via three parallel ***interpolators***.

:::tip
With Mix at an intermediate setting, the synthesized pattern becomes a colorful geometric texture overlaid on your video source. Try combining this with a slow Speed for a gentle, evolving overlay effect.
:::

---

## Background

### The Cromemco Dazzler

In January 1976, the Cromemco Dazzler appeared as a kit in *Popular Electronics* magazine. It was one of the first color graphics boards for personal computers: a plug-in card for the Altair 8800 that could display a 64×64 grid of pixels in sixteen colors. The Dazzler used ***direct memory mapping***: each pixel in the grid corresponded to a nibble (four bits) in a block of system RAM. Write a value to memory, and a colored dot would appear on the TV screen.

Li-Chen Wang, a programmer at Cromemco, wrote several demonstration programs for the Dazzler. His "Kaleidoscope" was the most famous: a tiny routine that generated endlessly changing symmetric patterns using nothing but integer shifts, additions, and bitwise AND operations. The entire program fit in a handful of 8080 instructions.

### Wang's Algorithm

The core of Wang's Kaleidoscope is a pair of coupled feedback equations operating on two 8-bit coordinates:

```
y = y + ((x >> 2) AND mask)
x = x - ((y >> 2) AND mask)
```

Each iteration, the current X coordinate is shifted right by two bits, masked, and added to Y. Then the *new* Y is shifted, masked, and *subtracted* from X. This asymmetric feedback (addition in one axis, subtraction in the other) produces the characteristic rotational quality (patterns tend to spiral rather than simply grow or shrink.)

The mask value is the key parameter. It determines which bits of the shifted coordinate survive into the feedback term. Different masks produce fundamentally different pattern families: some produce tight spirals, others produce crystalline lattices, others produce scattered dots. Wang's original program auto-incremented the mask after completing a full color cycle, creating a continuous slideshow of visual themes.

### Four-Way Symmetry

Each computed coordinate is plotted four times, mirrored across both the horizontal and vertical center lines of the 64×64 grid. The four ***quadrants*** reflect each other:

- **Lower-right**: the raw computed position
- **Lower-left**: X coordinate mirrored
- **Upper-left**: both X and Y mirrored
- **Upper-right**: Y coordinate mirrored

This produces the kaleidoscopic quality: every mark generates three reflections simultaneously. Even random-looking coordinate sequences become structured patterns when reflected across two axes.

### Color Cycling

Wang's algorithm cycles through colors in a deliberate pattern. A counter runs from 31 down to 1. On odd counts, the plotted color is black; on even counts, it's the current palette color (the counter's upper bits index the palette). This creates a strobing effect where patterns are alternately drawn and erased, building up layered imagery as different colors overwrite each other. After completing the full count, all fifteen non-black palette entries have been used once, and the mask increments.


---

## Signal Flow

### Signal Flow Notes

The architecture splits into two concurrent domains: a ***rendering*** path that reads the framebuffer and converts cell colors to YUV output, and an ***iteration*** path that writes new cells into the framebuffer during vertical blanking.

The rendering path runs continuously. Position counters track which cell is currently being displayed (using modular counters to avoid division: each cell is 30 pixels wide by 16 tall). The cell's row and column form a 12-bit address into the framebuffer. The 4-bit color index read from the framebuffer enters a 16-entry palette lookup table that outputs 10-bit Y, U, and V values. Brightness scaling multiplies the palette Y value by the Bright knob and shifts right by 10 bits. If the grid overlay is enabled, cell boundary pixels are replaced with dim neutral gray.

The iteration engine runs only during vsync blanking. On each vsync, it executes a batch of iterations (controlled by Speed). Each iteration computes new X and Y coordinates, then writes the color to four framebuffer addresses in sequence: one per quadrant of the mirror symmetry. This four-clock write cycle means each iteration takes five clocks total (one compute + four writes). After 64 iterations at one color level, the coordinates are bumped and the color counter decrements. After all fifteen colors, the mask auto-increments (in Auto mode).


---

## Exercises

These exercises explore the Kaleidoscope's pattern generation from simple observation through deliberate control of seeds, masks, and color. Since Kaleidoscope is a synthesis program, no input source is needed.
### Exercise 1: Watching the Machine

![Watching the Machine result](/img/instruments/videomancer/kaleidoscope/kaleidoscope_ex1_s1.png)
*Watching the Machine — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Observe the algorithm's natural behavior (an endlessly evolving slideshow of symmetric patterns.)

#### Key Concepts

- The iteration engine runs Wang's feedback algorithm at video rate
- Speed controls the rate of pattern evolution
- Auto Mask produces continuous, non-repeating variation

#### Steps

1. **Default state**: Leave all controls at their defaults. The pattern should already be evolving (symmetric shapes in Dazzler palette colors.)
2. **Slow down**: Turn **Speed** (Knob 1) fully counterclockwise. Watch individual cells appear in symmetric groups of four. This is Wang's algorithm running one iteration at a time.
3. **Speed up**: Turn Speed fully clockwise. The pattern mutates rapidly, shapes flickering and reforming as up to 128 iterations land per frame.
4. **Pause and study**: Flip **Run** (Switch 7) to **Pause**. The current pattern freezes. Examine the four-way symmetry: every shape in the lower-right quadrant has three reflections.
5. **Resume**: Set Run back to **Run** and let the pattern continue evolving. Notice how the character of the shapes changes periodically (that's the mask auto-incrementing after each color cycle.)

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~50% |
| Seed X | 50% |
| Seed Y | 50% |
| Mask | 0 |
| Hue Shift | 50% |
| Bright | ~75% |
| Run | Run |
| Auto Mask | Auto |
| Reset | Off |
| Grid | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Seeds and Masks

![Seeds and Masks result](/img/instruments/videomancer/kaleidoscope/kaleidoscope_ex2_s1.png)
*Seeds and Masks — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Learn to control which pattern family appears by manipulating seeds and masks manually.

#### Key Concepts

- Seed X and Seed Y define the starting coordinates
- The Mask knob directly controls pattern complexity in Manual mode
- Reset triggers a fresh start from the current seeds

#### Steps

1. **Enter manual mode**: Flip **Auto Mask** (Switch 8) to **Manual**. The mask is now under your direct control.
2. **Set a low mask**: Turn **Mask** (Knob 4) fully counterclockwise. The pattern becomes sparse (long curves and sweeping arcs with lots of empty space.)
3. **Increase the mask**: Slowly turn Mask clockwise. The patterns grow denser and more intricate. Notice how certain mask values produce tight, ordered lattices while others produce scattered, chaotic textures.
4. **Change seeds**: Adjust **Seed X** (Knob 2) and **Seed Y** (Knob 3) to new positions. Flip **Reset** (Switch 9) to **Reset** and back to **Off** to launch from the new starting point. The same mask value now produces a different trajectory.
5. **Find a favorite**: Experiment with different seed and mask combinations. When you find a pattern you like, flip Run to **Pause** to freeze it.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~40% |
| Seed X | 25% |
| Seed Y | 75% |
| Mask | ~50 |
| Hue Shift | 50% |
| Bright | ~75% |
| Run | Run |
| Auto Mask | Manual |
| Reset | Off |
| Grid | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Color and Overlay

![Color and Overlay result](/img/instruments/videomancer/kaleidoscope/kaleidoscope_ex3_s1.png)
*Color and Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Use palette rotation, grid visualization, and wet/dry mixing to create layered compositions.

#### Key Concepts

- Hue Shift rotates the palette without changing geometry
- Grid reveals the discrete 64×64 structure
- Mix blends synthesis with input video

#### Steps

1. **Palette exploration**: With a pattern running, slowly sweep **Hue Shift** (Knob 5) through its full range. Watch how the same geometric shapes take on completely different moods as colors rotate through the Dazzler palette (from cool blues and cyans to warm reds and yellows.)
2. **Brightness control**: Turn **Bright** (Knob 6) down to dim the pattern to a subtle glow, then up toward full brightness. At low brightness, only the brightest palette entries remain visible; at high brightness, the full sixteen-color palette is vivid on screen.
3. **Grid overlay**: Flip **Grid** (Switch 10) to **On**. A 64×64 grid of thin lines appears, revealing the discrete cell structure underlying the pattern. Each cell is 30 pixels wide by 16 pixels tall.
4. **Mix with video**: If a video source is connected, pull the **Mix** fader (Fader 12) down from 100%. The synthesized pattern blends with the input, creating a geometric overlay on live footage.
5. **Composite**: Set Mix to about 40% so the Kaleidoscope pattern is visible but translucent. Adjust Bright to balance the synthesis against the source material.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~50% |
| Seed X | 50% |
| Seed Y | 50% |
| Mask | 0 |
| Hue Shift | ~80% |
| Bright | ~60% |
| Run | Run |
| Auto Mask | Auto |
| Reset | Off |
| Grid | On |
| Bypass | Off |
| Mix | ~40% |

---
## Glossary

- **BRAM**: Block RAM: dedicated memory blocks inside the FPGA, used here to store the 64×64 framebuffer.

- **Cromemco Dazzler**: A 1976 color graphics board for the Altair 8800, displaying a 64×64-pixel grid in sixteen colors via direct memory mapping.

- **Feedback Equation**: A mathematical formula where the output of one iteration becomes the input to the next, producing evolving, self-referential patterns.

- **Four-Way Symmetry**: Mirroring a computed point across both the horizontal and vertical center axes, producing four reflected copies.

- **Framebuffer**: A block of memory holding the color value of every pixel in the grid, read continuously for display and written by the iteration engine.

- **Interpolator**: A DSP module that linearly blends between two input values based on a mixing coefficient (used here for wet/dry control.)

- **Iteration Engine**: The hardware state machine that executes Wang's coordinate feedback algorithm and writes results to the framebuffer.

- **Mask**: A bitwise AND filter applied to the shifted coordinate in Wang's feedback equations, determining which bits participate and thus controlling pattern complexity.

- **Palette**: A lookup table mapping 4-bit color indices (0–15) to 10-bit YUV values, based on the Cromemco Dazzler's RGBI color set.

- **Synthesis Program**: A Videomancer program that generates imagery from internal algorithms rather than processing an external video input.

---
