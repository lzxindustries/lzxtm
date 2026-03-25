---
draft: true
sidebar_position: 236
slug: /instruments/videomancer/psychedelia
title: "Psychedelia"
image: /img/instruments/videomancer/psychedelia/psychedelia_hero.png
description: "Psychedelia recreates Jeff Minter's 1984 light synthesiser of the same name, originally released for the Commodore 64."
---

![Psychedelia hero image](/img/instruments/videomancer/psychedelia/psychedelia_hero_s1.png)
*Psychedelia painting expanding mandala-like color pulses across a persistent framebuffer grid, with palette-cycled trails fading into the darkness.*

---

## Overview

**Psychedelia** is a self-contained ***light synthesizer***: a program that generates its own visual output rather than processing an incoming video signal. It maintains a low-resolution grid of color cells that persist across frames. Each frame, every cell decays one step toward black while the cursor emits a new burst of color. The pulse expands symmetrically from the cursor position, and overlapping pulses create layered, mandala-like patterns that bloom and fade in real time.

The effect is organic and mesmerizing. Colors cycle through a sixteen-step palette inspired by the Commodore 64: deep purples and blues at the bottom of the ramp, climbing through teals and greens, peaking at hot oranges and whites at the top. Because cells decay one level per frame, each pulse leaves a rainbow trail as it fades. The interplay between pulse rate, cursor speed, and pattern shape produces an almost infinite variety of kaleidoscopic imagery, from slow, meditative spirals to frenetic bursts of neon confetti.

:::tip
Psychedelia is a ***synthesis*** program. It does not require any video input to produce output: plug in a display and start turning knobs. However, enabling **Mod Vid** allows an external video signal to modulate the brightness of the generated patterns, blending the two worlds together.
:::

### What's In a Name?

**Psychedelia** is named after Jeff Minter's 1984 ***light synthesizer*** for the Commodore 64, considered one of the earliest real-time interactive visual instruments for home computers. The original Psychedelia was not a game: it was a tool for creating abstract, colorful displays synchronized to music, designed to be performed live. Minter called it a "light synthesizer" to draw a direct parallel with audio synthesizers: an instrument you play, not a program you run. This recreation translates that concept to modern FPGA hardware while preserving the spirit of the original: persistent color cells, symmetric pulse patterns, and palette-cycling decay.

---

## Quick Start

1. With all controls at their defaults, **Psychedelia** starts generating patterns immediately. The cursor traces a Lissajous path across the grid, leaving trails of color that fade behind it.
2. Turn **Pattern** (Knob 4) to step through eight different pulse shapes: diamond, cross, star, X, box, ring, double-cross, and burst. Watch how each shape produces a different character of mandala.
3. Adjust **Speed** (Knob 1) to change how quickly the cursor moves. Slower speeds produce tight, overlapping spirals. Faster speeds scatter pulses across the entire grid.
4. Flip **Symmetry** (Switch 8) to **8-Way**. The pattern reflections double, creating denser, more intricate mandalas with octagonal symmetry.

---

## Parameters

![Videomancer front panel with Psychedelia loaded](/img/instruments/videomancer/psychedelia/psychedelia_control_panel.png)
*Videomancer's front panel with Psychedelia active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Speed** controls the rate at which the cursor moves along its Lissajous path when in Auto mode. At the lowest setting, the cursor barely drifts, and successive pulses stack almost on top of each other, building up intense color concentrations in a small area. As you increase Speed, the cursor sweeps wider arcs across the grid, scattering pulses and producing broad, open mandala shapes.

In Manual mode, Speed has no visible effect since the cursor position is controlled directly by knobs.

---

### Knob 2 — Cursor X

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Cursor X** sets the horizontal position of the cursor when the **Cursor** switch is set to Manual. At 0%, the cursor sits at the left edge of the grid. At 100%, it sits at the right edge. In Auto mode, this parameter is ignored (the cursor follows its Lissajous trajectory instead.)

:::tip
In Manual mode, try turning **Cursor X** and **Cursor Y** simultaneously with both hands. The cursor becomes a direct extension of your gestures, painting color pulses wherever you point (just like Minter's original joystick interface.)
:::

---

### Knob 3 — Cursor Y

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Cursor Y** sets the vertical position of the cursor when the **Cursor** switch is set to Manual. At 0%, the cursor sits at the top of the grid. At 100%, it sits at the bottom. Like Cursor X, this parameter is ignored in Auto mode.

---

### Knob 4 — Pattern

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

**Pattern** selects one of eight geometric pulse shapes that the cursor stamps onto the grid. The shapes are:

- **0**: Diamond: a compact rhombus shape (Manhattan distance ≤ 3)
- **1**: Cross: a plus-sign extending four cells in each cardinal direction
- **2**: Star: a diamond core with cross arms, combining shapes 0 and 1
- **3**: X: diagonal lines radiating outward
- **4**: Box: a hollow square outline
- **5**: Ring: a hollow diamond shape (distance 2–4)
- **6**: Double Cross: both cardinal and diagonal axes in a snowflake-like pattern
- **7**: Burst: a large, solid filled diamond covering the maximum area

Compact shapes like Diamond and Cross create clean, well-separated mandala arms. Larger shapes like Burst flood the grid with color and produce denser, more saturated patterns.

---

### Knob 5 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Bright** scales the overall luminance of the color palette. At 0%, the output is completely dark regardless of cell values. At 100%, the palette displays at its full designed brightness. This control acts as a master intensity, useful for balancing Psychedelia's output level against other signals in a video chain.

---

### Knob 6 — Pulse Rate

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Pulse Rate** controls how many frames pass between each pulse emission. At the lowest setting, pulses fire very frequently: nearly every frame: producing dense overlapping trails. At higher settings, the cursor travels a longer distance between pulses, resulting in more widely spaced shapes with visible gaps between them.

:::note
Pulse Rate and **Speed** interact closely. High Speed with low Pulse Rate scatters rapid-fire pulses across the entire grid. Low Speed with high Pulse Rate produces slow, deliberate stamps that barely overlap.
:::

---

### Switch 7 — Cursor

| Property | Value |
|----------|-------|
| Off | Manual |
| On | Auto |
| Default | Auto |

**Cursor** selects between Manual and Auto cursor modes. In **Auto** mode (the default), the cursor traces a ***Lissajous curve***: a figure-eight-like path created by two sine waves at slightly different frequencies. The X and Y phases advance at different rates derived from the **Speed** parameter, so the cursor never quite traces the same path twice.

In **Manual** mode, the cursor position is controlled directly by **Cursor X** and **Cursor Y**. Auto mode parameters (Speed) are ignored.

---

### Switch 8 — Symmetry

| Property | Value |
|----------|-------|
| Off | 4-Way |
| On | 8-Way |
| Default | 4-Way |

**Symmetry** selects between 4-way and 8-way reflection symmetry for the pulse pattern. In **4-Way** mode, each stamp is reflected horizontally and vertically, producing patterns with quadrilateral symmetry. In **8-Way** mode, diagonal reflections are added, creating patterns with octagonal symmetry (denser and more intricate mandalas.)

:::note
In the current VHDL implementation, only the primary stamp position is written to the framebuffer; full symmetry reflections are a planned enhancement. The toggle sets the flag but the reflection writes are not yet active. Patterns still exhibit natural symmetry from the Lissajous cursor path and shape geometry.
:::

---

### Switch 9 — Reset

| Property | Value |
|----------|-------|
| Off | Off |
| On | Reset |
| Default | Off |

**Reset** clears the entire framebuffer to black when toggled from Off to Reset. All accumulated pulse trails are erased and the pattern begins building from scratch. This is an edge-triggered action: flip it once to clear, then flip it back. Useful for starting fresh after experimenting with different pattern and speed combinations.

---

### Switch 10 — Mod Vid

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mod Vid** enables video modulation of the synthesized pattern. When set to **On**, the brightness of each synthesized pixel is multiplied by the incoming video signal's luminance. Bright areas of the input video allow the pattern through; dark areas suppress it. This creates a masking effect where the generated mandala shapes are sculpted by an external image.

:::tip
Feed a high-contrast black-and-white source into the video input and enable **Mod Vid**. The mandala patterns appear only where the video is bright, creating a stencil-like interplay between the synthesized graphics and the live image.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Psychedelia synthesis. The sync delay pipeline still aligns timing, so there is no glitch when switching. In bypass mode, Psychedelia becomes transparent: useful for quick A/B comparison or for chaining in a larger video system.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the wet/dry blend between the synthesized output and the input video signal. At 0%, only the dry input signal passes through. At 100%, only the Psychedelia synthesis is visible. Intermediate values produce a crossfade between the two. The interpolation is applied independently to the Y, U, and V channels.

---

## Background

### Light synthesizers and the demoscene

Jeff Minter created the original Psychedelia in 1984, releasing it for the Commodore 64, Atari 8-bit, and Spectrum. It was a radical departure from typical software of the era: not a game, not a utility, but something he called a ***light synthesizer***. You plugged in a joystick, turned on music, and created abstract color displays in real time. The program laid the philosophical groundwork for an entire genre of interactive visual instruments, from Minter's own Neon (1986) and Virtual Light Machine (1994, for the Atari Jaguar) to modern tools like this Videomancer recreation.

The ***demoscene***: the underground culture of programmers creating real-time audiovisual demonstrations on limited hardware: drew heavily on these ideas. Psychedelia's technique of persistent framebuffer accumulation with decay is a staple of demoscene effects: plasma routines, fire effects, and starfield simulations all use variations of the same concept. Write a bright value, let it fade, and new patterns emerge from the interaction of fresh marks and decaying trails.

### Framebuffer persistence and decay

Psychedelia's visual engine is built on a simple but powerful concept: a ***persistent framebuffer***. The grid is a 48×27 array of 4-bit cells, each storing a value from 0 to 15. Every frame, the entire grid decays: every non-zero cell is decremented by one. Then the cursor stamps a fresh pattern at maximum brightness (15). Because the palette maps these 16 levels to a smooth color ramp from black through purples, blues, greens, yellows, and whites, the decay creates a rainbow trail effect. Newer pulses shine white-hot while older ones cool through the spectrum toward darkness.

This approach is computationally minimal: just a decrement and a compare: but produces visually rich results. The 48×27 grid resolution is deliberately low, matching the blocky aesthetic of 1980s home computers while keeping the BRAM footprint within the iCE40 HX4K's 32-block budget.

### Lissajous curves

In Auto mode, the cursor traces a ***Lissajous curve***: the same family of figures you see on an oscilloscope when two sine waves are fed to the X and Y deflection plates. The X and Y sine phases advance at different rates (the X phase increments faster than the Y phase by a ratio derived from the Speed parameter), so the cursor path never quite repeats. The resulting trajectory produces naturally symmetric patterns even without explicit symmetry reflections, because the sinusoidal motion creates balanced, mirrored arcs.


---

## Signal Flow

### Signal Flow Notes

The engine operates in two phases during the vertical blanking interval. First, a ***decay pass*** iterates through all 1,296 cells of the framebuffer, reading each value and writing back a decremented copy (or leaving zeros unchanged). Second, if the pulse timer has expired, a ***stamp pass*** writes the selected pattern shape at maximum brightness (15) around the current cursor position. Both passes share the framebuffer's read and write ports via an address multiplexer, so the engine temporarily takes priority over the rendering pipeline during blanking.

During active video, the rendering pipeline takes over. It maps each output pixel to its corresponding grid cell (40×40 pixels per cell at 1920×1080), reads the cell's 4-bit value from the framebuffer, looks up Y, U, and V values from the sixteen-entry C64-inspired palette, scales luminance by the Brightness parameter, and optionally multiplies by the input video's luminance when Mod Vid is enabled. Three parallel `interpolator_u` instances then blend the synthesized YUV with the delayed input signal according to the Mix fader.


---

## Exercises

The exercises progress from passive observation of the synthesizer in its default state through manual cursor control and finally to video-modulated hybrid imagery.
### Exercise 1: Automatic Mandalas

![Automatic Mandalas result](/img/instruments/videomancer/psychedelia/psychedelia_ex1_s1.png)
*Automatic Mandalas — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A flowing, self-animating mandala of overlapping color pulses traced by the automatic cursor.

#### Key Concepts

- Persistent framebuffer decay creates rainbow trails
- Lissajous cursor motion generates naturally symmetric patterns
- Pattern shape and pulse rate control the character of the mandala

#### Steps

1. Begin with defaults. **Psychedelia** is already generating patterns. Watch the cursor trace its Lissajous path and observe the rainbow trails left behind.
2. Turn **Speed** (Knob 1) counterclockwise toward 0%. The cursor slows to a near-standstill, stacking pulses atop each other (colors concentrate intensely at the center.)
3. Increase **Speed** back to about 75%. The cursor sweeps wider arcs, and the pattern opens up into broad, flowing shapes.
4. Step through **Pattern** (Knob 4) from Diamond through Burst. Notice how each shape creates a fundamentally different mandala character.
5. Lower **Pulse Rate** (Knob 6) to its minimum. Pulses fire rapidly, filling the grid quickly with overlapping shapes.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~75% |
| Cursor X | 50% |
| Cursor Y | 50% |
| Pattern | Star (2) |
| Bright | ~75% |
| Pulse Rate | 0% |
| Cursor | Auto |
| Symmetry | 4-Way |
| Reset | Off |
| Mod Vid | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Manual Painting

![Manual Painting result](/img/instruments/videomancer/psychedelia/psychedelia_ex2_s1.png)
*Manual Painting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Deliberate, hand-painted mandala compositions by manually positioning the cursor and controlling the pulse rate.

#### Key Concepts

- Manual mode gives direct positional control of the cursor
- Slow pulse rates produce deliberate, separated stamps
- Reset clears the canvas for a fresh start

#### Steps

1. Switch **Cursor** (Switch 7) to **Manual**. The automatic Lissajous path stops; the cursor now responds to your knobs.
2. Set **Pulse Rate** (Knob 6) to about 50%. This spaces pulses apart so you can see each one appear individually.
3. Slowly turn **Cursor X** (Knob 2) and **Cursor Y** (Knob 3) to move the cursor around the grid. Watch color pulses appear at each position, decaying behind you as you go.
4. Select the **Box** pattern (Knob 4, position 4). The hollow square stamps create a distinct tessellated look.
5. Toggle **Reset** (Switch 9) to clear the canvas, then start painting again from a blank grid.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 0% |
| Cursor X | ~50% |
| Cursor Y | ~50% |
| Pattern | Box (4) |
| Bright | 100% |
| Pulse Rate | ~50% |
| Cursor | Manual |
| Symmetry | 4-Way |
| Reset | Off |
| Mod Vid | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Video-Modulated Synthesis

![Video-Modulated Synthesis result](/img/instruments/videomancer/psychedelia/psychedelia_ex3_s1.png)
*Video-Modulated Synthesis — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A hybrid composition where the synthesized mandala patterns are masked and sculpted by an incoming video signal.

#### Key Concepts

- Mod Vid multiplies synthesized brightness by input video luminance
- Mix blends synthesized output with the input signal
- The combination creates hybrid imagery (generated patterns shaped by real-world content)

#### Steps

1. Connect a video source to Videomancer's input. Set **Mix** (Fader 12) to about 50% to blend the input with the synthesis.
2. Enable **Mod Vid** (Switch 10). The generated patterns now appear only where the input video is bright.
3. Set **Cursor** (Switch 7) back to **Auto** and increase **Speed** (Knob 1) to about 60%. The cursor traces its path, but the color pulses are masked by the video content.
4. Adjust **Bright** (Knob 5) upward to compensate for the modulation reducing overall brightness.
5. Sweep **Mix** (Fader 12) from 0% to 100% and back. At low Mix values, the source dominates with faint pattern overlays. At high Mix values, the mandala dominates with video-shaped holes. Find the blend you prefer.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~60% |
| Cursor X | 50% |
| Cursor Y | 50% |
| Pattern | Double Cross (6) |
| Bright | 100% |
| Pulse Rate | ~30% |
| Cursor | Auto |
| Symmetry | 4-Way |
| Reset | Off |
| Mod Vid | On |
| Bypass | Off |
| Mix | ~50% |

---
## Glossary

- **Decay**: The per-frame process of decrementing all non-zero framebuffer cells by one, causing older pulse marks to fade toward black through a palette gradient.

- **Framebuffer**: A persistent memory grid (48×27 cells, 4 bits per cell) that retains pixel data across frames, enabling accumulation and gradual decay of visual content.

- **Light Synthesizer**: An interactive visual instrument designed for real-time performance, generating abstract graphics in response to user input (coined by Jeff Minter in 1984.)

- **Lissajous Curve**: A figure traced by a point whose X and Y coordinates follow sine functions at different frequencies, producing looping, figure-eight-like paths.

- **Mandala**: A symmetrical geometric pattern radiating from a center point; here, the emergent result of overlapping symmetric pulse stamps.

- **Palette Cycling**: A technique where a fixed set of colors (a palette) is mapped to numeric cell values, so that as values change (via decay), colors appear to shift through the spectrum.

- **Persistent Framebuffer**: A display buffer that retains its contents between frames rather than being cleared, allowing accumulation of successive drawing operations.

- **Pulse**: A single stamp of the selected pattern shape at maximum color value (15) onto the framebuffer grid, originating from the cursor position.

- **Stamp**: The act of writing a geometric pattern into the framebuffer at the cursor location; the pattern shape is determined by the Pattern parameter.

- **Synthesis Program**: A Videomancer program type that generates its own video output from internal logic rather than transforming an incoming signal.

---
