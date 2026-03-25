---
draft: true
sidebar_position: 246
slug: /instruments/videomancer/ricochet
title: "Ricochet"
image: /img/instruments/videomancer/ricochet/ricochet_hero.png
description: "Every office worker of the 1990s had the same secret hope — that the DVD logo bouncing endlessly in the corner would finally hit the exact corner of the screen."
---

![Ricochet hero image](/img/instruments/videomancer/ricochet/ricochet_hero_s1.png)
*A luminous rectangle bouncing across the screen, revealing processed video inside its borders while the outside world dims to shadow.*

---

## Overview

**Ricochet** is a real-time motion synthesis program that places a bouncing shape on screen: a rectangle or circle that drifts, collides with edges, and reverses direction. Inside the shape, your input video is processed through one of eight selectable effects: pass-through, brighten, invert, colorize, solarize, posterize, threshold, or high contrast. Outside the shape, video is dimmed toward darkness. The result is a wandering spotlight that reveals a processed version of whatever you feed it.

The magic happens at the corners. When the shape strikes two edges simultaneously: a ***corner hit***: it cycles through an eight-color palette, tinting the border and optionally flooding the entire screen with a momentary color flash. Enable **Trail** mode, and the shape paints a persistent map of everywhere it has been, leaving a mosaic of processed tiles across the frame that accumulates and then resets itself.

If you grew up staring at a DVD player's idle screen, willing that little logo to hit the corner, Ricochet is the video synthesizer version of that dopamine hit (and it brings real video processing along for the ride.)

### What's In a Name?

A ***ricochet*** is a rebound: a projectile bouncing off a surface and continuing in a new direction. The name captures the program's core behavior: a shape that bounces endlessly off the edges of the screen, changing color each time it strikes a corner. Like a billiard ball careening around a table, the shape's trajectory is simple but its path is endlessly varied.

---

## Quick Start

1. With any video source connected, you'll see a bright rectangular shape drifting across a dimmed background. The shape reveals your input video inside its borders (that's Ricochet at its default settings.)
2. Turn **Speed** (Knob 1) clockwise to accelerate the shape. Watch it ping off the edges faster and faster. When it hits a corner, the screen flashes with a new color.
3. Try the **In FX** knob (Knob 4): rotate it through its eight positions. Each click selects a different effect applied to the video inside the shape (from color inversion to solarization to hard threshold.)
4. Flip the **Trail** switch (Switch 8) to On. Now every region the shape crosses stays revealed, building up a patchwork mosaic of processed tiles. When roughly three-quarters of the screen is painted, the trail resets and begins again.

---

## Parameters

![Videomancer front panel with Ricochet loaded](/img/instruments/videomancer/ricochet/ricochet_control_panel.png)
*Videomancer's front panel with Ricochet active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Speed** controls how fast the shape moves across the screen. At the lowest setting, the shape creeps at one pixel per frame: a slow, meditative drift. As you turn the knob clockwise, velocity increases up to eight pixels per frame, and collisions with the edges come fast. The velocity is constant between bounces; the shape doesn't accelerate or decelerate. At high speeds, corner hits happen more frequently, cycling through the color palette quickly.

:::tip
At very high speeds with **Crn Flash** enabled, the rapid succession of corner hits creates a strobing color effect. We recommend starting at low-to-moderate speed while learning the other controls.
:::

---

### Knob 2 — Width

| Property | Value |
|----------|-------|
| Range | 32px – 960px |
| Default | 380px |

**Width** sets the horizontal size of the bouncing shape. At minimum, we get a narrow sliver. At maximum, the shape stretches nearly edge to edge, leaving almost no dimmed region visible. In **Circle** mode, the width also defines the circle's diameter, so the height parameter is overridden. Combined with **Height**, this lets you sculpt the shape from a thin vertical bar to a wide letterbox to a rough square.

---

### Knob 3 — Height

| Property | Value |
|----------|-------|
| Range | 32px – 540px |
| Default | 223px |

**Height** sets the vertical size of the bouncing shape. A small height creates a horizontal band that scans up and down across the frame. A large height reveals most of the screen at once. When using **Circle** mode, height has no effect: the circle's size is determined entirely by the Width parameter.

---

### Knob 4 — In FX

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

**In FX** selects which processing effect is applied to the input video ***inside*** the shape. The knob steps through eight discrete effects:

- **0: Pass-through**: Video appears unchanged inside the shape.
- **1: Brighten**: Luminance is boosted by a fixed offset, pushing mid-tones toward white. Already-bright areas clip to peak white.
- **2: Invert**: All three channels (Y, U, V) are inverted: darks become lights, and colors flip to their complements.
- **3: Colorize**: Luminance is preserved from the input, but chrominance is replaced with the current palette color. The result is a monochrome tint that shifts each time the shape hits a corner.
- **4: Solarize**: Luminance values above midpoint fold back downward, creating a ***Sabattier***-like partial reversal. Shadows remain dark, highlights darken, and mid-tones become the brightest areas.
- **5: Posterize**: Each channel is quantized to three bits, reducing the image to eight levels per channel: flat, hard-edged color bands with no gradients.
- **6: Threshold**: A hard binary key at midpoint. Pixels brighter than 50% become peak white; all others become black. Chrominance goes neutral, producing a stark monochrome silhouette.
- **7: High Contrast**: The lower eight bits of luminance are amplified, expanding subtle detail while clipping bright areas. The effect is a punchy, contrasty look that pulls texture out of darker regions.

:::note
Effect 3 (Colorize) is the only inside effect that uses the corner-hit color palette. The tint ***changes automatically*** each time the shape bounces off two edges simultaneously.
:::

---

### Knob 5 — Out Dim

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Out Dim** controls how much the video outside the shape is darkened. At minimum, the outside video passes through at full brightness: there's no visible distinction between inside and outside. As you increase the value, the outside dims progressively toward black. At high settings (above roughly 88%), the outside region also loses its color, fading to neutral gray then to black. This creates the classic spotlight effect: a bright reveal surrounded by darkness.

---

### Knob 6 — Aspect

| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

**Aspect** is a four-position selector intended for aspect ratio presets. In the current firmware version, this parameter is reserved and has no visible effect on the output. The shape's proportions are controlled independently by **Width** (Knob 2) and **Height** (Knob 3).

---

### Switch 7 — Shape

| Property | Value |
|----------|-------|
| Off | Rect |
| On | Circle |
| Default | Rect |

**Shape** selects between a rectangular and a circular bouncing region. When set to **Rect**, the shape is an axis-aligned rectangle whose size is defined by Width and Height. When set to **Circle**, the shape becomes a roughly circular region using an ***octagonal approximation***: a computationally efficient method that calculates distance as `max(|dx|, |dy|) + min(|dx|, |dy|) / 2`. The result is a shape that looks circular at large sizes but reveals eight-sided geometry at smaller scales. In Circle mode, the circle's radius is derived from the Width parameter; Height has no effect.

---

### Switch 8 — Trail

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Trail** enables persistent painting mode. When active, the shape marks a grid of cells as it passes over them. Each cell covers a 64×64 pixel region of the screen. Once a cell is marked, it stays revealed: showing the inside effect: even after the shape has moved on. The trail accumulates over time, building a patchwork mosaic of processed tiles. When approximately 75% of the grid is painted, the trail auto-resets and begins accumulating from scratch. When Trail is disabled, only the current shape position is revealed.

:::tip
Trail mode transforms Ricochet from a moving spotlight into a ***generative painting tool***. The bouncing shape acts as a brush, gradually filling the canvas with processed video tiles. Each reset creates a fresh start with a new trajectory.
:::

---

### Switch 9 — Crn Flash

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Crn Flash** enables a full-screen color flash whenever the shape hits a corner: that is, when it bounces off both a horizontal and a vertical edge in the same frame. The flash lasts eight frames and uses the current palette color. With each corner hit, the palette advances to the next of eight colors, so consecutive flashes cycle through the entire palette. When this switch is Off, corner hits still cycle the border color, but the full-screen flash effect is suppressed.

---

### Switch 10 — Border

| Property | Value |
|----------|-------|
| Off | Off |
| On | Glow |
| Default | Off |

**Border** enables a colored glow ring around the edge of the bouncing shape. The ring is three pixels wide and drawn inside the shape boundary. Its color comes from the eight-entry palette, which cycles on corner hits. When set to **Glow**, the border is visible; when **Off**, the shape has no visible edge (the transition between inside and outside is abrupt.)

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the input video directly to the output, bypassing all Ricochet processing. The sync pipeline still runs, so there is no timing glitch on transition. Use Bypass for instant A/B comparison between the bouncing spotlight and the raw input.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the unprocessed input video and the Ricochet output. At minimum, you see only the original input: no spotlight, no dimming. At maximum, you see the full Ricochet effect. Intermediate values blend the two, creating a translucent overlay where the bouncing shape is ghosted over the full-brightness input. This is handled by three parallel ***interpolator*** instances (one per YUV channel) that perform a linear crossfade.

---

## Background

### The DVD Bounce

In the early 2000s, DVD players and media consoles displayed an idle screen: a small logo drifting across the display, bouncing off edges, changing direction at each wall. It became an internet meme: millions of people watched and waited for the logo to land perfectly in a corner. The geometry of the bounce meant corner hits were rare, roughly once every few minutes depending on screen proportions and logo size. The anticipation became the entertainment.

Ricochet recreates this behavior as a video processing tool. The bouncing shape isn't decorative: it's functional. It defines a region of the frame where one of eight processing effects is applied, while the surrounding area is dimmed or blacked out. Corner hits aren't just satisfying to watch; they trigger a color palette change that affects the border glow and the colorize effect.

### Inside Effects

The **In FX** parameter selects from eight signal-processing modes applied to Video inside the bouncing shape. These effects range from subtle (pass-through, brighten) to dramatic (invert, threshold) to deliberately crude (posterize at 3-bit, high contrast). The effects operate directly on the raw YUV video data:

- **Brighten** adds a fixed offset of 256 to the 10-bit luminance, clamping at 1023. This is roughly a 25% brightness boost.
- **Invert** subtracts each channel from 1023, providing true YUV inversion (not just luma negation).
- **Solarize** folds luminance at the midpoint: values below 512 pass through; values above 512 are mirrored downward. The result resembles an analog ***Sabattier effect***.
- **Posterize** truncates each channel to its top three bits, yielding 8 × 8 × 8 = 512 possible YUV combinations.
- **Threshold** applies a hard binary key at midpoint (512), producing a black-and-white silhouette with neutral chrominance.

### Trail Painting

Trail mode adds persistent memory to the bouncing shape. The FPGA maintains a grid of 30 columns by 17 rows: one bit per cell, each representing a 64×64-pixel region of the active picture. As the shape moves, it marks the cell beneath its center. Once marked, that cell is treated as "inside" for rendering purposes, showing the current inside effect even after the shape has moved on.

The trail accumulates until roughly 75% of the 510-cell grid is filled, at which point the entire grid auto-clears and the painting begins again. This creates a cyclical rhythm: slow accumulation → near-complete coverage → sudden reset → fresh start. The rate of accumulation depends on shape size and speed: larger shapes at higher speeds cover more cells per frame and fill the grid faster.

:::note
Because the trail grid maps 64×64-pixel cells, the painted regions have a blocky, tiled appearance. This is intentional: the coarse grid keeps FPGA resource usage minimal (510 bits of storage) while creating an interesting mosaic aesthetic.
:::


---

## Signal Flow

### Signal Flow Notes

The rendering priority chain is the key to understanding Ricochet's compositing behavior. When the corner flash is active and enabled, it ***overrides everything***: the entire screen is flooded with the current palette color at peak luminance for eight frames. When the flash is inactive, the border glow takes priority if the current pixel is within three pixels of the shape edge. Below that, the inside effect is applied to any pixel inside the shape boundary or inside a trail-marked cell. Everything else gets the dimmed outside treatment.

The outside dimming multiplies input luminance by `(1023 - out_dim) / 1024`, a simple fractional attenuation. At very high dim settings (above approximately 900 out of 1023), chrominance is also forced to neutral: the outside region loses all color and fades to monochrome darkness. This two-stage behavior prevents muddy, desaturated color from appearing in deeply dimmed regions.

:::warning
The **Aspect** parameter (Knob 6) is mapped to a VHDL signal but is not connected to any rendering logic in the current firmware. Adjusting it has no visible effect. Shape proportions are set independently using Width and Height.
:::


---

## Exercises

These exercises explore Ricochet's layers of behavior: from simple bouncing spotlight to generative trail painting to full-screen color composition.
### Exercise 1: The Classic Bounce

![The Classic Bounce result](/img/instruments/videomancer/ricochet/ricochet_ex1_s1.png)
*The Classic Bounce — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean, moving spotlight that reveals your input video against a dark backdrop, celebrating corner hits with color flashes (the essential Ricochet experience.)

#### Key Concepts

- Bouncing geometry and edge collision
- Inside vs. outside rendering regions
- Corner-hit color cycling

#### Steps

1. Set **Speed** (Knob 1) to a moderate value, roughly 25%. The shape should drift smoothly across the screen.
2. Set **Width** (Knob 2) and **Height** (Knob 3) to small values, creating a compact shape.
3. Increase **Out Dim** (Knob 5) to about 75% so the outside is noticeably dark but not black.
4. Make sure **In FX** (Knob 4) is at position 0 (pass-through). The video inside the shape should look unchanged.
5. Confirm **Crn Flash** (Switch 9) is On and **Border** (Switch 10) is set to Glow.
6. Watch the shape bounce. When it hits a corner: both edges at once: the border color changes and the screen flashes. Count the hits and watch all eight palette colors cycle.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~25% |
| Width | ~200 px |
| Height | ~150 px |
| In FX | 0 |
| Out Dim | ~75% |
| Aspect | 0 |
| Shape | Rect |
| Trail | Off |
| Crn Flash | On |
| Border | Glow |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Trail Painting

![Trail Painting result](/img/instruments/videomancer/ricochet/ricochet_ex2_s1.png)
*Trail Painting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A generative composition where the bouncing shape gradually paints the screen with processed video tiles, creating an accumulating mosaic that periodically resets.

#### Key Concepts

- Persistent trail memory and auto-reset behavior
- 64×64-pixel cell grid creates mosaic tiling
- Shape size and speed control coverage rate

#### Steps

1. Start from Exercise 1's settings. Flip **Trail** (Switch 8) to On.
2. Set **In FX** (Knob 4) to position 3 (Colorize). The inside of the shape: and every cell it has visited: shows your video tinted with the current palette color.
3. Increase **Speed** (Knob 1) to accelerate coverage. Watch the 64×64-pixel tiles fill in, creating a patchwork grid.
4. When roughly three-quarters of the screen is painted, the trail auto-clears. The mosaic vanishes and begins accumulating again from the shape's current position.
5. Now switch **Shape** (Switch 7) to Circle. The painting brush becomes circular, producing slightly different coverage patterns along diagonal trajectories.
6. Try **In FX** position 2 (Invert) for a trail of inverted-video tiles, or position 5 (Posterize) for a trail of flat, hard-edged color blocks.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~50% |
| Width | ~400 px |
| Height | ~300 px |
| In FX | 3 |
| Out Dim | ~90% |
| Aspect | 0 |
| Shape | Circle |
| Trail | On |
| Crn Flash | On |
| Border | Glow |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Strobe Composition

![Strobe Composition result](/img/instruments/videomancer/ricochet/ricochet_ex3_s1.png)
*Strobe Composition — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A high-energy composition that uses rapid corner flashes as bursts of color overlaid on processed video, blended with the raw input for a layered result.

#### Key Concepts

- Corner flash as a rhythmic compositional element
- Combining inside effects with rapid palette cycling
- Mix crossfade for layering

#### Steps

1. Set **Speed** (Knob 1) high: around 80%. The shape will bounce rapidly, hitting corners frequently.
2. Make the shape small: **Width** ~100 px, **Height** ~80 px. A small, fast-moving shape maximizes the number of edge collisions.
3. Set **In FX** (Knob 4) to position 6 (Threshold). The shape shows a stark black-and-white silhouette of your input.
4. Turn **Out Dim** (Knob 5) to maximum (the outside goes completely black.)
5. Confirm **Crn Flash** (Switch 9) is On and **Border** (Switch 10) is Glow. Corner hits produce full-screen color bursts cycling rapidly through the palette.
6. Now pull **Mix** (Fader 12) down to about 50%. The strobing color washes blend with the unprocessed input, creating a ghostly double-exposure with rhythmic color pulses.
7. Slowly increase the shape size while watching how the corner-hit frequency changes (larger shapes cover more area but hit corners less often.)

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~80% |
| Width | ~100 px |
| Height | ~80 px |
| In FX | 6 |
| Out Dim | 100% |
| Aspect | 0 |
| Shape | Rect |
| Trail | Off |
| Crn Flash | On |
| Border | Glow |
| Bypass | Off |
| Mix | ~50% |

---
## Glossary

- **Corner Hit**: A simultaneous bounce off both a horizontal and vertical edge in the same frame, triggering a palette color change and optional flash.

- **Interpolator**: A hardware module that performs linear blending between two values; Ricochet uses three interpolators (Y, U, V) for wet/dry mix.

- **Octagonal Approximation**: A distance formula (`max(|dx|, |dy|) + min(|dx|, |dy|) / 2`) that approximates a circle with an eight-sided polygon, efficient for FPGA implementation.

- **Palette**: A fixed set of eight YUV colors that Ricochet cycles through on corner hits, used for border glow, corner flash, and the Colorize effect.

- **Posterization**: Quantizing pixel values to fewer discrete levels, producing flat regions separated by hard tonal edges.

- **Sabattier Effect**: A photographic technique where tonal values partially reverse around the midpoint, creating a combined positive-negative image. Ricochet's Solarize mode emulates this digitally.

- **Sample and Hold**: Capturing a signal value and holding it constant until the next sample point, used in the trail grid to "freeze" processed video in visited cells.

- **Solarization**: Folding luminance values at a midpoint so that bright areas darken while shadows remain dark, producing surreal tonal curves.

- **Trail Grid**: A 30×17 array of single-bit cells (one per 64×64-pixel region) stored in BRAM, tracking which areas of the screen the bouncing shape has visited.

- **Velocity**: The number of pixels the shape moves per frame; derived from the Speed parameter as `(pot >> 7) + 1`, yielding a range of 1 to 8 pixels per frame.

- **Wet/Dry Mix**: A crossfade between the processed (wet) and unprocessed (dry) signals, controlled by the Mix fader.

- **YUV**: A color space separating luminance (Y) from chrominance (U, V), used natively by the Videomancer video pipeline.

---
