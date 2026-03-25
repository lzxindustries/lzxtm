---
draft: true
sidebar_position: 166
slug: /instruments/videomancer/lattice
title: "Lattice"
image: /img/instruments/videomancer/lattice/lattice_hero.png
description: "Lattice is a geometric pattern synthesizer that generates two-dimensional grid structures from a pair of orthogonal frequency accumulators."
---

![Lattice hero image](/img/instruments/videomancer/lattice/lattice_hero_s1.png)
*Lattice projecting a scrolling grid of luminous colored bars over a video input, boolean-combined into shifting geometric tile patterns.*

---

## Overview

Lattice is a geometric grid synthesizer that builds two-dimensional bar patterns from horizontal and vertical ***phase accumulators***. Each axis generates a repeating ramp waveform whose frequency you control independently. The ramps can be folded into triangle waves for symmetric bars, then combined with a selectable boolean operation: AND for intersection grids, XOR for alternating checkerboard tiles. The resulting mask keys between a configurable fill color and the input video, with an animation accumulator adding continuous horizontal scrolling.

At low frequencies, Lattice produces bold stripes and wide tiles. At higher frequencies, the bars multiply into dense lattice structures that shimmer and alias as the accumulators wrap. Adding animation transforms static geometry into scrolling pattern fields: and switching the boolean combine mode from AND to XOR flips the entire visual character from rigid grids to interlocking mosaics.

:::tip
***The fader brings the grid to life.*** At startup the output is pure input video. Increase **Anim Rate** (Fader 12) to crossfade toward the grid composite (this is your master wet/dry control.)
:::

### What's In a Name?

A ***lattice*** is a framework of regularly spaced, intersecting bars: the criss-crossed wood of a garden trellis, the atomic scaffolding of a crystal, or the repeating tile of a mathematical point grid. The program earns its name by generating exactly that: a two-dimensional array of evenly spaced lines whose intersections form the nodes of a geometric lattice. Flip the boolean combine to XOR and the lattice dissolves into a ***tessellation*** of alternating tiles, like a chessboard built from waveforms.

---

## Quick Start

1. Push **Anim Rate** (Fader 12) to about 75%. The grid pattern fades in over the input video.
2. Turn **Fill Y** (Knob 4) counter-clockwise to roughly 50%. Thick grid bars appear (this control sets the bar thickness threshold.)
3. Sweep **H Freq** (Knob 1) and **V Freq** (Knob 2) to change the number of horizontal and vertical bars. More bars appear as you turn clockwise.
4. Flip **H Shape** (Switch 7) to its second position. The grid switches from an AND intersection pattern to an XOR checkerboard (a completely different geometry from the same waveforms.)

---

## Parameters

![Videomancer front panel with Lattice loaded](/img/instruments/videomancer/lattice/lattice_control_panel.png)
*Videomancer's front panel with Lattice active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — H Freq

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**H Freq** controls the spatial frequency of the horizontal grid pattern. The underlying mechanism is a ***phase accumulator*** that steps through a 16-bit counter once per pixel. Higher values advance the accumulator faster, producing more cycles: and therefore more vertical bar stripes: across the width of the screen. At 0%, fully counter-clockwise, the accumulator barely advances and the pattern shows at most a single broad stripe. At 100%, fully clockwise, the bars multiply into a dense curtain of fine lines. The initial value sits at 25.0%, producing a modest number of evenly spaced bars.

:::note
The accumulator resets at the start of each active video line, so the horizontal pattern is locked to the screen and does not drift vertically.
:::

---

### Knob 2 — V Freq

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**V Freq** controls the spatial frequency of the vertical grid pattern. A second phase accumulator steps once per line (rather than per pixel), producing horizontal bar stripes that tile down the screen. At 0%, you see a single broad horizontal band. Increasing the value adds more horizontal stripes. The initial value is 25.0%.

Together, **H Freq** and **V Freq** define the density and proportions of the lattice. Equal values create roughly square cells; unequal values produce rectangular tiles.

---

### Knob 3 — Bar Width

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Bar Width** controls the speed of a free-running animation accumulator. This accumulator increments once per video field and its output is added to the horizontal grid waveform, causing the entire horizontal pattern to scroll continuously. At 0%, the pattern is perfectly static: no scrolling occurs. As the value increases, the grid scrolls faster. At 100%, the scroll completes a full cycle in just a few frames, producing rapid horizontal motion. The initial value is 50.0%, yielding a moderate, visible scroll.

:::tip
Because animation offsets only the horizontal axis, **V Freq** bars remain stationary while **H Freq** bars slide across them. This creates mesmerizing moiré interference when both axes have similar frequencies.
:::

---

### Knob 4 — Fill Y

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Fill Y** sets the bar thickness threshold. Each grid waveform (horizontal and vertical) is compared against this value: wherever the waveform exceeds the threshold, the grid line is "on." At 0%, fully counter-clockwise, the threshold is minimal and nearly the entire waveform exceeds it: the grid fills the screen with solid color. As the value increases, the threshold rises and only the peaks of the waveform pass, producing thinner and thinner bars. At 100%, the threshold is at maximum and the bars vanish almost entirely. The initial value is 100.0%, meaning the grid starts fully transparent.

:::warning
At default settings the grid bars are invisible because the threshold is at maximum. Turn **Fill Y** counter-clockwise to reveal the pattern.
:::

---

### Knob 5 — Fill U

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Fill U** controls the luminance (brightness) of the fill color applied to grid bar regions. At 0%, the fill is black. At 100%, the fill is peak white. The initial value is 50.0%, producing a mid-gray fill. Non-grid regions display the delayed input video, so this control determines the brightness contrast between the grid and the underlying image.

---

### Knob 6 — Fill V

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Fill V** controls the hue of the fill color. Internally, the single value derives both chroma channels: U receives the raw value while V receives its complement (1023 minus the value). At 50.0% (the initial value), both channels are near neutral: the fill is achromatic gray, tinted only by the **Fill U** luminance. Turning counter-clockwise shifts the fill toward one color extreme; turning clockwise shifts it toward the complementary hue. At either extreme the fill is strongly saturated.

:::tip
For a pure white or black grid with no color tint, leave **Fill V** at center (50%). To create colored lattice overlays, push **Fill V** toward either end while adjusting **Fill U** for brightness.
:::

---

### Switch 7 — H Shape

| Property | Value |
|----------|-------|
| Off | Ramp |
| On | Triangle |
| Default | Ramp |

**H Shape** selects the boolean operation used to combine the horizontal and vertical grid masks into a single two-dimensional pattern. In its default position (labeled **Ramp**), the combination is AND: a pixel is part of the grid only where *both* the horizontal and vertical bars overlap, producing a classic lattice of intersecting lines. In the second position (labeled **Triangle**), the combination switches to XOR: a pixel belongs to the grid when it falls on *either* axis but not both, generating an alternating checkerboard of rectangular tiles.

AND grids emphasize the crossing points of bars. XOR grids fill the spaces between crossings, producing a complementary pattern that looks like a woven or tiled surface.

---

### Switch 8 — V Shape

| Property | Value |
|----------|-------|
| Off | Ramp |
| On | Triangle |
| Default | Ramp |

**V Shape** controls the waveform shape of the *horizontal* grid axis. In its default position (labeled **Ramp**), the horizontal frequency doubler is active. The doubler folds the sawtooth ramp at its midpoint, converting it into a symmetric ***triangle wave*** that produces evenly balanced bars. In the second position (labeled **Triangle**), the doubler is bypassed and the raw sawtooth ramp passes through, producing asymmetric bars (a sharp leading edge and a gradual trailing edge.)

:::note
Despite its label, this switch affects the *horizontal* waveform shape. The label/function mismatch is a known firmware display artifact.
:::

---

### Switch 9 — Combine

| Property | Value |
|----------|-------|
| Off | AND |
| On | XOR |
| Default | AND |

**Combine** controls the waveform shape of the *vertical* grid axis. In its default position (labeled **AND**), the vertical frequency doubler is active, producing symmetric triangle-wave bars. In the second position (labeled **XOR**), the doubler is bypassed and the raw sawtooth ramp produces asymmetric vertical bars.

:::note
Despite its label, this switch affects the *vertical* waveform shape rather than the combine mode. The boolean combine mode is selected by **H Shape** (Switch 7).
:::

---

### Switch 10 — Soft Edge

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Soft Edge** inverts the polarity of the grid key. In its default position (**Off**), grid bar regions display the fill color and non-bar regions display the input video. When set to **On**, the assignment flips: bars show the input video and the gaps between bars receive the fill color. This effectively swaps foreground and background without changing the grid geometry.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Lattice processing stages. The sync delay pipeline still runs, so there is no glitch or timing jump when toggling. Use Bypass for instant A/B comparison between the raw input and the grid composite.

---

### Fader 12 — Anim Rate

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Anim Rate** is the master wet/dry crossfade between the unprocessed input video and the grid-keyed composite. At 0%, the output is pure input video: the grid is computed but not visible. At 100%, the output is the full grid composite with fill colors keyed over the input. Intermediate values blend the two, producing a semi-transparent overlay. The initial value is 0.0%, so no grid is visible at startup.

:::tip
Think of **Anim Rate** as your master "grid intensity" control. Start at 0% and slowly increase to bring the lattice into view.
:::

---

## Background

### Phase Accumulators and Ramp Generation

At the heart of Lattice are three ***phase accumulators***: 16-bit counters that add a fixed step value on every tick. A horizontal accumulator advances once per pixel and resets at the start of each active video line, sweeping a sawtooth ramp from left to right. A vertical accumulator advances once per line and resets at the start of each frame, sweeping a ramp from top to bottom. A third accumulator runs freely, advancing once per field without resetting, producing a continuously rolling ramp whose position shifts from frame to frame.

The step size: the value added on each tick: determines how fast the accumulator wraps. Larger steps mean the counter overflows more often within a single line or frame, producing more cycles and denser patterns. Smaller steps produce fewer cycles and wider bars. This is the same principle behind a ***numerically controlled oscillator*** (NCO): the output frequency is proportional to the step size.

### Frequency Folding

A raw phase accumulator produces a ***sawtooth*** (ramp) waveform: a linear sweep from zero to maximum, followed by an abrupt wraparound. The ***frequency doubler*** folds this ramp at its midpoint, reflecting values above the halfway mark back down. The result is a ***triangle wave*** at twice the original spatial frequency, with symmetric rise and fall. Triangle-wave grid bars have equal-width light and dark regions. Raw sawtooth bars are asymmetric, with a gradual ramp on one side and a hard edge on the other.

Lattice provides independent fold bypass switches for the horizontal and vertical axes, so you can mix symmetric and asymmetric bar shapes across the two dimensions.

### Boolean Mask Operations

Once the horizontal and vertical waveforms are thresholded into binary masks (bar or gap), they are combined with a selectable boolean operation:

- **AND**: a pixel is "on" only where both horizontal *and* vertical bars overlap. The result is a grid of small rectangular patches at the intersections (a classic lattice.)
- **XOR**: a pixel is "on" where *either* bar is active but not both. The result is an alternating tile pattern: bars without their crossing points, like a woven fabric or chessboard.

AND grids emphasize structure; XOR grids emphasize rhythm. The choice profoundly changes the visual character of the output even though the underlying waveforms are identical.

### Video Keying

The boolean grid mask is used as a hard ***key*** signal. Where the mask is active, the output shows a configurable fill color (luminance and hue). Where the mask is inactive, the delayed input video passes through. A key inversion switch swaps these roles. Finally, an ***interpolator*** crossfades between the fully keyed composite and the original dry input, providing a smooth wet/dry mix.

Because the key is binary (hard-edged), the grid bars have crisp pixel boundaries. There is no anti-aliasing or feathering (the bars are pure digital geometry.)


---

## Signal Flow

### Signal Flow Notes

Two key interactions define the Lattice pipeline:

1. **Animation is horizontal only.** The animation accumulator's ramp is added to the folded horizontal waveform *before* the threshold comparison. The vertical waveform receives no animation offset. This means horizontal bars scroll while vertical bars remain stationary, creating sliding interference patterns when both axes are active.

2. **A single threshold controls both axes.** The same **Fill Y** (Pot 4) value sets the bar/gap boundary for both horizontal and vertical waveforms. Changing it uniformly affects bar thickness on both axes simultaneously: you cannot set independent widths for horizontal and vertical bars.

:::tip
**Order matters.** The pipeline flows: accumulator → frequency doubler → animation offset (H only) → threshold → boolean combine → key invert → key compose → mix → bypass. Each stage feeds the next, so changes early in the chain (like waveform shape) cascade through all downstream stages.
:::


---

## Exercises

These exercises progress from a static monochrome grid to animated, colored lattice compositions. Each builds on the controls introduced in the previous exercise.
### Exercise 1: Static Monochrome Grid

![Static Monochrome Grid result](/img/instruments/videomancer/lattice/lattice_ex1_s1.png)
*Static Monochrome Grid — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean, static black-and-white grid (the fundamental lattice structure.)

#### Key Concepts

- Phase accumulators generate repeating ramp patterns
- The threshold determines bar thickness
- AND combining creates a classic lattice at intersections

#### Steps

1. Push **Anim Rate** (Fader 12) to maximum. This fully engages the grid composite.
2. Turn **Fill Y** (Knob 4) to about 30%. Thick grid bars appear as the threshold lowers.
3. Increase **H Freq** (Knob 1) to about 40%. Several vertical bar stripes appear.
4. Increase **V Freq** (Knob 2) to about 40%. Horizontal bars join the vertical ones, forming a two-dimensional grid.
5. Slowly sweep **Fill Y** (Knob 4) from 0% to 100%. Watch the bars go from screen-filling solid to razor-thin lines and finally vanish.

#### Settings

| Control | Value |
|---------|-------|
| H Freq | 40% |
| V Freq | 40% |
| Bar Width | 0% |
| Fill Y | 30% |
| Fill U | 100% |
| Fill V | 50% |
| H Shape | Ramp |
| V Shape | Ramp |
| Combine | AND |
| Soft Edge | Off |
| Bypass | Off |
| Anim Rate | 100% |

---

### Exercise 2: Colored XOR Tiles

![Colored XOR Tiles result](/img/instruments/videomancer/lattice/lattice_ex2_s1.png)
*Colored XOR Tiles — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A saturated, tiled mosaic with complementary colors and inverted key regions.

#### Key Concepts

- XOR combining transforms intersection grids into alternating tile patterns
- The fill hue control creates colored lattice overlays
- Key inversion swaps grid and background roles

#### Steps

1. Start from the grid in Exercise 1 (or load those settings).
2. Flip **H Shape** (Switch 7) to **Triangle**. The AND grid transforms into an XOR checkerboard (alternating filled and empty tiles.)
3. Turn **Fill V** (Knob 6) to about 20%. The fill shifts from neutral gray to a saturated color.
4. Adjust **Fill U** (Knob 5) to set the brightness of the colored fill. Try about 70% for a vivid result.
5. Flip **Soft Edge** (Switch 10) to **On**. The key inverts: the tiles that were filled are now transparent, and vice versa. The complementary mosaic appears.
6. Experiment with different **H Freq** and **V Freq** ratios. Unequal values create rectangular tiles instead of squares.

#### Settings

| Control | Value |
|---------|-------|
| H Freq | 35% |
| V Freq | 50% |
| Bar Width | 0% |
| Fill Y | 40% |
| Fill U | 70% |
| Fill V | 20% |
| H Shape | Triangle |
| V Shape | Ramp |
| Combine | AND |
| Soft Edge | On |
| Bypass | Off |
| Anim Rate | 100% |

---

### Exercise 3: Animated Moiré Weave

![Animated Moiré Weave result](/img/instruments/videomancer/lattice/lattice_ex3_s1.png)
*Animated Moiré Weave — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A continuously scrolling lattice with moiré beating, colored fills, and mixed waveform shapes (a hypnotic woven-light texture.)

#### Key Concepts

- Animation scrolls the horizontal axis continuously
- Mixing ramp and triangle waveform shapes creates asymmetric patterns
- Near-equal H and V frequencies produce moiré interference

#### Steps

1. Set **H Freq** (Knob 1) to about 35% and **V Freq** (Knob 2) to about 37%. The slight mismatch creates subtle moiré interference in the grid.
2. Turn **Bar Width** (Knob 3) to about 40%. The horizontal grid begins scrolling at moderate speed.
3. Set **Fill Y** (Knob 4) to about 45% for visible bars.
4. Push **Fill V** (Knob 6) to about 80% for a strongly colored fill, and **Fill U** (Knob 5) to about 60% for brightness.
5. Flip **V Shape** (Switch 8) to **Triangle**. The horizontal bars become raw sawtooth ramps (asymmetric and edgier.)
6. Flip **Combine** (Switch 9) to **XOR**. The vertical bars also switch to raw ramps. Now both axes have asymmetric shapes, creating a woven, directional texture.
7. Slowly sweep **Fill Y** (Knob 4) while the pattern scrolls. The moiré interference shifts as bar thickness changes.

#### Settings

| Control | Value |
|---------|-------|
| H Freq | 35% |
| V Freq | 37% |
| Bar Width | 40% |
| Fill Y | 45% |
| Fill U | 60% |
| Fill V | 80% |
| H Shape | Ramp |
| V Shape | Triangle |
| Combine | XOR |
| Soft Edge | Off |
| Bypass | Off |
| Anim Rate | 100% |

---
## Glossary

- **Boolean Operation**: A logical combination of two binary values; AND produces output only when both inputs are true, XOR produces output when exactly one input is true.

- **Frequency Doubler**: A circuit that folds a sawtooth ramp at its midpoint, converting it into a triangle wave at twice the spatial frequency.

- **Interpolator**: A crossfade circuit that blends between two signals based on a mix parameter, providing smooth wet/dry control.

- **Key (Video)**: A technique that uses a mask signal to select between two video sources on a per-pixel basis: grid regions show one source, non-grid regions show another.

- **Lattice**: A regular, repeating arrangement of intersecting elements; in this program, a two-dimensional grid of bars generated by phase accumulators.

- **Moiré**: An interference pattern that appears when two similar periodic structures overlap with a slight frequency or phase difference.

- **Phase Accumulator**: A counter that adds a fixed step value on each clock tick, producing a repeating ramp (sawtooth) waveform whose frequency is proportional to the step size.

- **Sawtooth (Ramp)**: A waveform that rises linearly from minimum to maximum and then wraps abruptly back to minimum, producing an asymmetric repeating pattern.

- **Threshold**: A comparison value that divides a continuous waveform into binary regions (above the threshold is "on," below is "off.")

- **Triangle Wave**: A symmetric waveform that rises linearly to a peak and then falls linearly back to the minimum, producing evenly balanced high and low regions.

- **XOR Tessellation**: A tiled pattern created by exclusive-OR combination of two grid masks, producing alternating filled and empty cells like a chessboard.

---
