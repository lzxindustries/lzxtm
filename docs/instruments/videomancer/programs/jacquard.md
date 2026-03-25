---
draft: true
sidebar_position: 150
slug: /instruments/videomancer/jacquard
title: "Jacquard"
image: /img/instruments/videomancer/jacquard/jacquard_hero_s1.png
description: "The Jacquard loom, invented in 1804 by Joseph Marie Jacquard, was the first machine to use punched cards for controlling the pattern of a weave."
---

![Jacquard hero image](/img/instruments/videomancer/jacquard/jacquard_hero_s1.png)
*Jacquard weaving a herringbone textile pattern over a live video feed, with copper warp threads and indigo weft threads casting soft shadows at each crossing.*

---

## Overview

**Jacquard** turns your video into woven cloth. It overlays a programmable textile grid onto the input image, sampling pixels at warp and weft intersection points and tinting each thread with its own hue. The result looks like video has been printed onto fabric: warp threads run vertically, weft threads run horizontally, and the two interlock in one of four classic weave patterns. Threads that pass behind the weave are darkened with a configurable shadow, giving the illusion of three-dimensional depth.

At subtle settings, Jacquard adds a gentle canvas-like texture that makes video look like it was shot through a screen door or projected onto linen. At extreme settings, it transforms the image into bold, colorful plaid and tartan patterns where the original video peeks through as dyed fiber. Because the weave grid is driven by pixel-position counters, the pattern locks perfectly to the raster and never drifts.

:::tip
Try feeding a static image and slowly sweeping **Thread W** through its eight steps. You'll see the weave scale jump between discrete sizes (just like choosing different thread gauges on a real loom.)
:::

### What's In a Name?

The name ***Jacquard*** honors Joseph Marie Jacquard, the French weaver who invented the ***Jacquard loom*** in 1804. His loom used punched cards to control individual warp threads, enabling complex patterns like brocade, damask, and tapestry to be woven automatically. It was one of the earliest examples of a programmable machine: a direct ancestor of the computer. In Videomancer, Jacquard's punched-card logic lives on as 8×8 pattern lookup tables stored in FPGA fabric.

---

## Quick Start

1. Feed a video source with recognizable shapes and colors. Set **Thread W** (Knob 1) to a medium value: around step 4 or 5. A grid of interlocking threads appears over the video.
2. Turn **Warp Hue** (Knob 3) and **Weft Hue** (Knob 4) to contrasting positions. The vertical warp threads take on one color and the horizontal weft threads take on another (the image now looks like a two-tone tartan.)
3. Increase **Shadow** (Knob 6). The threads that pass *beneath* the weave darken, creating the illusion that one set of threads sits on top of the other.
4. Flip the **Pattern** switch (Switch 7) to **Herring**. The interlacing pattern changes from a simple checkerboard to a V-shaped ***herringbone*** (named for the skeleton of a herring fish.)

---

## Parameters

![Videomancer front panel with Jacquard loaded](/img/instruments/videomancer/jacquard/jacquard_control_panel.png)
*Videomancer's front panel with Jacquard active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Thread W

| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 7 |

**Thread W** sets the width of each thread in the weave grid, controlling how many pixels wide each warp or weft band is. This parameter is quantized into eight discrete steps, producing thread widths of 2, 3, 4, 5, 6, 8, 10, or 16 pixels. At the narrowest setting, the weave is a fine mesh: almost like a window screen. At the widest, each thread is a thick ribbon spanning 16 pixels. Because the steps are discrete, turning the knob produces distinct jumps between sizes rather than a smooth sweep.

:::note
Thread width is uniform for both warp and weft (horizontal and vertical threads are always the same gauge.)
:::

---

### Knob 2 — Density

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Density** controls the coverage ratio of the thread grid, adjusting how much of the source image is visible between threads. At low values, the weave is loose and open: more of the original video shows through the gaps. As Density increases, threads become tighter and more opaque, filling more of the frame with the woven pattern. At maximum, the weave covers the entire image.

---

### Knob 3 — Warp Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 60° |

**Warp Hue** selects the color tint applied to warp (vertical) threads. The hue sweeps around the color wheel in eight quantized steps, visiting red, orange, yellow-green, green, cyan, blue, purple, and magenta. Warp threads that are "on top" in the current weave pattern receive this tint, blended with the source video according to the **Tint Amt** control.

---

### Knob 4 — Weft Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 240° |

**Weft Hue** selects the color tint applied to weft (horizontal) threads, independent of **Warp Hue**. The same eight-position color wheel applies. Setting Warp Hue and Weft Hue to contrasting positions: say red and cyan: produces a vivid two-tone tartan. Setting them to the same hue creates a monochrome weave where only the shadow gives depth cues.

:::tip
Complementary hue pairs (0° and 180°, or 90° and 270°) produce the most dramatic tartan effects. Try red warp with cyan weft, or yellow-green warp with purple weft.
:::

---

### Knob 5 — Tint Amt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Tint Amt** controls the strength of the hue tint applied to each thread. At zero, no tint is applied: threads carry the original color of the source video, and Warp Hue and Weft Hue have no visible effect. As Tint Amt increases, threads shift further toward their assigned hue. At maximum, the tint dominates and the original color is largely overridden.

---

### Knob 6 — Shadow

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Shadow** controls how much weft-under (beneath) threads are darkened at each crossing point. At zero, all threads are equally bright: there is no depth illusion. As Shadow increases, the threads that pass beneath the weave grow darker, creating the appearance that warp threads are physically stacked on top of weft threads. At maximum, under-threads are nearly black, producing a dramatic relief.

:::note
Shadow is ***one-sided***: it always darkens weft threads. Warp-over threads remain at full brightness regardless of the Shadow setting.
:::

---

### Switch 7 — Pattern

| Property | Value |
|----------|-------|
| Off | Plain |
| On | Herring |
| Default | Plain |

**Pattern** selects the weave interlacing pattern. In the **Plain** position, the pattern is a simple checkerboard: warp and weft threads alternate over and under at every crossing, like a basic basket weave. In the **Herring** position, the interlacing follows a ***herringbone*** pattern: a V-shaped zigzag where the diagonal direction reverses at the midpoint of the repeat. Herringbone creates a more complex, textured appearance reminiscent of tweed and tailored suiting fabrics.

---

### Switch 8 — Noise

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Noise** injects per-pixel randomness from a ***linear feedback shift register*** (LFSR) into the luminance channel. When set to **Off**, the weave pattern is perfectly clean and uniform. When set to **On**, a small random offset is added to each pixel's brightness, simulating the natural irregularity of hand-woven cloth: slight variations in thread tension, dye absorption, and fiber alignment.

:::tip
Noise is most visible at low Thread W settings where the weave is fine. At wide thread widths, each thread spans so many pixels that the per-pixel noise reads as gentle texture rather than grain.
:::

---

### Switch 9 — Color Src

| Property | Value |
|----------|-------|
| Off | Tint |
| On | Video |
| Default | Tint |

**Color Src** selects the source of thread coloring. In the **Tint** position, threads are colored by blending toward the Warp Hue and Weft Hue values: the weave looks like dyed fabric. In the **Video** position, threads carry the original video's chrominance, and the Warp Hue, Weft Hue, and Tint Amt controls have no effect. Video mode is useful when you want the weave texture and shadow depth without altering the color palette.

---

### Switch 10 — Grid Show

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Grid Show** enables a visible grid overlay at thread boundaries. When set to **Off**, the weave pattern blends smoothly. When set to **On**, dark lines are drawn at the edges of each thread cell, making the grid structure explicitly visible. Grid lines are rendered as darkened, desaturated pixels at the cell boundaries: like the gaps between tiles in a mosaic. This is useful for understanding the grid geometry or for creating a stained-glass window aesthetic.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the original, unprocessed input signal directly to the output. When set to **On**, all Jacquard processing is skipped and the clean video passes through. The sync delay pipeline still aligns timing, so switching Bypass produces no glitch. Use it for instant A/B comparison between the raw input and the woven result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (original) and wet (woven) signals. At 0%, only the original video appears. At 100%, only the fully processed weave is visible. Intermediate positions blend the two: useful for dialing in a subtle fabric texture without overwhelming the source content. Mix operates on all three channels (Y, U, V) simultaneously via matched interpolators.

---

## Background

### Textile weaving

Woven fabric is created by interlacing two perpendicular sets of threads. The ***warp*** threads run vertically on the loom (lengthwise), held taut by the frame. The ***weft*** threads are passed horizontally through the warp (crosswise), going alternately over and under warp threads according to a pattern. The specific sequence of over-and-under crossings defines the weave structure.

Four fundamental weave patterns exist, each producing a distinctive surface texture. ***Plain weave*** (also called tabby) is the simplest: each weft thread goes over one warp thread, then under the next, creating a tight checkerboard. ***Twill weave*** offsets the crossings diagonally, creating a characteristic ribbed texture used in denim and gabardine. ***Satin weave*** spaces the crossings far apart, producing a smooth, lustrous surface with few visible interlacings. ***Herringbone*** is a twill variant where the diagonal direction reverses periodically, creating V-shaped zigzags.

### Jacquard looms and programmability

The Jacquard loom, invented in 1804 Lyon, France, was the first machine to use punched cards for automatic pattern control. Each card encoded one row of the weave pattern: holes allowed specific warp threads to be raised, creating the desired interlacing sequence. Complex patterns like brocade and damask, previously requiring skilled hand labor, could be produced mechanically. Charles Babbage and Ada Lovelace were directly inspired by Jacquard's punched-card mechanism when designing the Analytical Engine: making the Jacquard loom a genuine ancestor of modern computing.

In Videomancer's Jacquard program, the punched cards are replaced by 8×8 lookup tables stored as constants in the FPGA logic. Each table encodes a different weave pattern: plain, twill, satin, or herringbone. The pixel's position on the grid indexes into the table to determine whether the warp or weft thread is on top at that crossing.

### Color and depth in woven media

Real woven fabrics derive their visual richness from two phenomena: thread color and crossing depth. Threads dyed different colors create patterns: tartan, plaid, gingham: while the physical stacking of threads at each crossing creates subtle shadows. Jacquard simulates both: the Warp Hue and Weft Hue controls assign colors to each thread direction, while the Shadow control darkens threads that pass beneath the weave. The combination produces the illusion of three-dimensional textile on a flat video signal.


---

## Signal Flow

### Signal Flow Notes

The pipeline has two key structural features:

1. **Pattern lookup is purely combinational**: The 8×8 weave pattern tables are implemented as constants: no BRAM is consumed. The FPGA evaluates grid position and pattern in a single clock cycle using only LUT logic. This is how Jacquard achieves zero BRAM usage while still providing four weave patterns.

2. **Shadow is asymmetric**: The shadow darkening is applied by multiplying Y by `(1023 − shadow) / 1024`. This multiplication only happens when the weft thread is on top (pattern bit = 0). Warp-over threads always multiply by `1023 / 1024`: effectively full brightness. This asymmetry gives the weave its characteristic depth: one thread direction always appears to sit above the other.

:::tip
**Hue quantization**: Both Warp Hue and Weft Hue are quantized to eight positions around the color wheel (0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°). The knob position is divided by the top 3 bits to select one of eight entries from an approximate UV lookup table. You won't get every possible hue: but the eight available positions are evenly spaced and cover the full spectrum.
:::


---

## Exercises

These exercises progress from basic weave textures through colored tinting to full tartan-style compositions. Each one builds on the previous, adding more of Jacquard's processing chain.
### Exercise 1: Plain Canvas Texture

![Plain Canvas Texture result](/img/instruments/videomancer/jacquard/jacquard_ex1_s1.png)
*Plain Canvas Texture — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A subtle linen-like texture overlaid on video, as if the source were projected onto canvas.

#### Key Concepts

- Thread width controls weave scale
- Shadow creates depth at crossings
- Noise adds organic irregularity

#### Video Source

A portrait or still life with smooth gradients and distinct subjects (skin tones, soft lighting, or a landscape with sky.)

#### Steps

1. Set **Thread W** (Knob 1) to a narrow value: step 2 or 3. A fine grid of tiny threads appears over the video.
2. Set **Color Src** (Switch 9) to **Video** so threads carry the original video color.
3. Set **Tint Amt** (Knob 5) fully counterclockwise (no hue tinting.)
4. Increase **Shadow** (Knob 6) to about 40%. Notice how alternating threads darken slightly at each crossing, creating a visible weave texture.
5. Enable **Noise** (Switch 8). The perfectly clean grid gains a subtle organic irregularity (like unevenly dyed thread.)
6. Adjust **Mix** (Fader 12) to about 40–50%. The canvas texture blends gently with the source image.

#### Settings

| Control | Value |
|---------|-------|
| Thread W | Step 3 (~4 px) |
| Density | 50% |
| Warp Hue | — (ignored) |
| Weft Hue | — (ignored) |
| Tint Amt | 0% |
| Shadow | 40% |
| Pattern | Plain |
| Noise | On |
| Color Src | Video |
| Grid Show | Off |
| Bypass | Off |
| Mix | 40% |

---

### Exercise 2: Two-Tone Tartan

![Two-Tone Tartan result](/img/instruments/videomancer/jacquard/jacquard_ex2_s1.png)
*Two-Tone Tartan — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A vivid tartan-style pattern where warp and weft threads carry contrasting colors over the source video.

#### Key Concepts

- Warp and weft hues tint threads independently
- Tint Amount controls color saturation
- Herringbone pattern adds visual complexity

#### Video Source

High-contrast footage with strong shapes: bold graphics, architectural details, or a dancer silhouette.

#### Steps

1. Set **Thread W** (Knob 1) to a wide value: step 6 or 7 (8–10 px). The threads are thick enough to see color clearly.
2. Set **Color Src** (Switch 9) to **Tint** so thread color comes from the hue controls.
3. Turn **Warp Hue** (Knob 3) to approximately 0° (red). Turn **Weft Hue** (Knob 4) to approximately 180° (cyan). The warp threads glow red and the weft threads glow cyan.
4. Increase **Tint Amt** (Knob 5) to about 70%. The colors intensify.
5. Increase **Shadow** (Knob 6) to 60%. The weft (under) threads darken noticeably, giving the tartan real depth.
6. Switch **Pattern** (Switch 7) from **Plain** to **Herring**. The simple checkerboard becomes a V-shaped zigzag (the tartan now looks like herringbone suiting fabric.)

#### Settings

| Control | Value |
|---------|-------|
| Thread W | Step 7 (~10 px) |
| Density | 50% |
| Warp Hue | 0° (red) |
| Weft Hue | 180° (cyan) |
| Tint Amt | 70% |
| Shadow | 60% |
| Pattern | Herring |
| Noise | Off |
| Color Src | Tint |
| Grid Show | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Stained Glass Grid

![Stained Glass Grid result](/img/instruments/videomancer/jacquard/jacquard_ex3_s1.png)
*Stained Glass Grid — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A stained-glass window effect where dark leading lines separate colored panes of video.

#### Key Concepts

- Grid Show draws visible lines at thread boundaries
- Combining Grid Show with shadow and tinting creates a stained-glass effect
- Mix blends the processed result with the source for compositing

#### Video Source

Footage with vivid, saturated colors: flowers, neon signs, colorful murals, or kaleidoscopic graphics.

#### Steps

1. Set **Thread W** (Knob 1) to the widest setting: step 8 (16 px). Each "pane" of glass is wide enough to see the source content clearly.
2. Enable **Grid Show** (Switch 10). Dark lines appear at every thread boundary, dividing the image into a grid of rectangular cells.
3. Set **Color Src** (Switch 9) to **Tint**. Set **Warp Hue** (Knob 3) to ~90° (yellow-green) and **Weft Hue** (Knob 4) to ~270° (purple).
4. Set **Tint Amt** (Knob 5) to 50%. The "glass panes" take on alternating warm and cool tones.
5. Increase **Shadow** (Knob 6) to about 70%. The panes that sit behind the weave darken dramatically, like tinted glass catching less light.
6. Enable **Noise** (Switch 8). Subtle per-pixel variation makes the color within each pane shimmer, as if light were passing through textured glass.
7. Set **Mix** (Fader 12) to ~80%. The source video remains faintly visible beneath the stained-glass overlay.

#### Settings

| Control | Value |
|---------|-------|
| Thread W | Step 8 (16 px) |
| Density | 50% |
| Warp Hue | 90° (yellow-green) |
| Weft Hue | 270° (purple) |
| Tint Amt | 50% |
| Shadow | 70% |
| Pattern | Plain |
| Noise | On |
| Color Src | Tint |
| Grid Show | On |
| Bypass | Off |
| Mix | 80% |

---
## Glossary

- **Herringbone**: A weave pattern where the diagonal direction of the twill reverses periodically, creating V-shaped zigzags resembling the skeleton of a herring fish.

- **Jacquard Loom**: A mechanical loom invented in 1804 that used punched cards to automate complex weave patterns, a precursor to programmable computing.

- **LFSR**: Linear Feedback Shift Register; a simple digital circuit that generates a repeating sequence of pseudo-random bits, used here for noise texture.

- **Plain Weave**: The simplest weave structure where warp and weft threads alternate over-under at every crossing, creating a checkerboard interlacing.

- **Satin Weave**: A weave structure where crossings are widely spaced, producing a smooth, lustrous surface with minimal visible interlacing.

- **Twill Weave**: A weave structure where the interlacing point shifts diagonally on each successive row, creating a characteristic ribbed texture.

- **Warp**: The set of vertical threads held taut on a loom, through which the weft is woven.

- **Weft**: The horizontal thread that is passed over and under the warp threads to create fabric.

---
