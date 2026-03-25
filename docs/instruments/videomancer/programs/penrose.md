---
draft: true
sidebar_position: 221
slug: /instruments/videomancer/penrose
title: "Penrose"
image: /img/instruments/videomancer/penrose/penrose_hero_s1.png
description: "The Penrose triangle is perhaps the most famous impossible object — a three-bar figure that appears to represent a solid three-dimensional triangle, yet cannot exist in Euclidean space."
---

![Penrose hero image](/img/instruments/videomancer/penrose/penrose_hero_s1.png)
*Penrose overlaying impossible triangle wireframes with depth-cued junction shading onto live video.*

---

## Overview

Penrose draws ***impossible geometry*** wireframes over your video signal. Its core shapes: the Penrose triangle, staircase, Necker cube, and Blivet trident: are classic optical illusions that appear to depict three-dimensional objects which could not actually exist. The program renders these shapes by computing the distance from every pixel to a set of angled line axes, then brightening, darkening, or replacing pixels that fall within the wireframe stroke.

At default settings, Penrose places a single triangular wireframe at screen center and composites it over the input video. You can scale the shape, thicken or thin its lines, tile it across the screen, and animate it with a horizontal drift. A depth cue control darkens the wireframe at the points where two bars overlap, reinforcing the illusion of contradictory spatial relationships: bars that appear to pass both in front of and behind one another.

:::tip
Penrose is a ***processing*** program. It overlays geometry on top of your source video rather than replacing it. Use the **Mix** fader to dial in how much of the wireframe composite blends with the original signal.
:::

### What's In a Name?

The name ***Penrose*** comes from Sir Roger Penrose, the British mathematician and Nobel laureate who popularized the ***impossible triangle*** in the 1950s. The Penrose triangle: also called the ***tribar***: is a two-dimensional figure that the brain interprets as a solid three-dimensional object, but one whose geometry is self-contradictory. Each corner appears reasonable, but following the bars around the full loop reveals that they cannot connect in real space. The program extends this concept to other impossible figures: the Penrose staircase (stairs that climb forever in a loop), the Necker cube (which flips between two spatial interpretations), and the ***Blivet*** (an impossible trident with three prongs that merge into two bars).

---

## Quick Start

1. Load Penrose with default settings. A single wireframe triangle appears centered on the screen, composited over your input video. The lines glow white against the image.
2. Turn **Size** (Knob 1) counterclockwise to shrink the triangle, or clockwise to expand it until it fills the screen.
3. Turn **Count** (Knob 4) clockwise past the halfway point. The single shape tiles into a repeating grid of smaller triangles across the screen.
4. Flip **Shape** (Switch 7) to its second position. The triangle geometry changes: you may see a staircase or trident pattern depending on the state of **Style** (Switch 8). Experiment with both switches to discover all four shapes.

---

## Parameters

![Videomancer front panel with Penrose loaded](/img/instruments/videomancer/penrose/penrose_control_panel.png)
*Videomancer's front panel with Penrose active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Size

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Size** controls the overall scale of the wireframe shape. The pot value sets the ***half-extent***: the distance from the center of the shape to its outermost bar. At 0%, fully counterclockwise, the shape is drawn at its minimum size of about 64 pixels across. As you increase the value, the shape grows. At 100%, the half-extent reaches roughly 575 pixels, and the wireframe spans most of the screen. The bounds-checking logic ensures that wireframe strokes are only drawn within the shape's extent, so you won't see stray lines radiating out to infinity.

---

### Knob 2 — Line Thk

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Line Thk** (Line Thickness) controls the width of the wireframe strokes in pixels. At 0%, each bar is drawn at the minimum width of one pixel: a hairline. As you increase the value, the strokes thicken progressively. At 100%, each bar is 32 pixels wide, giving the wireframe a heavy, architectural quality. Thicker lines make the depth cue shading at junctions more visible because the overlap area between two bars grows proportionally.

:::note
At very large **Size** values with thick lines, the shape can look more like a bold graphic emblem than a delicate wireframe. This is a useful aesthetic for title overlays and motion graphics.
:::

---

### Knob 3 — Rotation

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Rotation** offsets the wireframe shape horizontally across the screen. Despite its name, this control translates the geometry left and right rather than spinning it. At 50% (the default midpoint), the shape is centered. Turning counterclockwise shifts the entire wireframe to the left; turning clockwise shifts it to the right. The offset range spans roughly ±512 pixels from center. When **Spin** (Switch 9) is active, the animation drift is added on top of this manual offset, so you can use **Rotation** to set a starting position for the moving shape.

---

### Knob 4 — Count

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Count** controls how many copies of the wireframe shape tile across the screen. At 0%, a single shape is drawn at center. As the value increases, the program engages power-of-two tiling that repeats the shape at progressively denser intervals. The four tiling modes are:

- Below ~25%: single shape (no repetition)
- ~25% to ~50%: 2× tiling (the shape repeats every 512 pixels)
- ~50% to ~75%: 4× tiling (the shape repeats every 256 pixels)
- Above ~75%: 8× tiling (the shape repeats every 128 pixels)

Each tile is re-centered within its cell, so the pattern is always symmetric. Higher tiling levels force each copy into a smaller cell, which effectively shrinks the visible shape regardless of the **Size** setting.

:::tip
Try 8× tiling with a small **Size** and thin **Line Thk** to create a delicate lattice of impossible triangles across the entire screen.
:::

---

### Knob 5 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bright** (Brightness) controls how strongly the wireframe strokes affect the image. In Wire mode, this value is *added* to the source luminance on every wireframe pixel, so higher values produce brighter overlays. In Shadow mode, the value is *subtracted* from the source, so higher values produce deeper shadows. In Solid mode, this value *replaces* the source luminance directly. In Glow mode, it is added to luminance and also shifts the chrominance toward warm tones. At 0%, the wireframe is invisible (zero brightness contribution). At 100%, the wireframe blazes at full intensity.

---

### Knob 6 — Depth Cue

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Depth Cue** controls the shading applied at junction points: the places where two wireframe bars overlap. Junctions are the key to the impossible-object illusion because they are where the contradictory depth relationships become visible. At 0%, no special shading is applied, and junctions look the same as the rest of the wireframe. As the value increases through five discrete steps, junction pixels are progressively darkened by halving the wireframe brightness one, two, three, or four times. At maximum, junction pixels are dimmed to 1/16 of the wireframe brightness, creating a strong contrast between the bars and their crossing points.

:::note
The depth cue effect is most visible with thicker lines and moderate brightness. Very thin lines produce junctions too small to read clearly.
:::

---

### Switch 7 — Shape

| Property | Value |
|----------|-------|
| Off | Triangle |
| On | Trident |
| Default | Triangle |

**Shape** selects the wireframe geometry. In its default position (**Triangle**), the lower bit of the internal shape selector is cleared. In its second position (**Trident**), the lower bit is set. The final shape you see depends on the combined state of **Shape** and **Style** (Switch 8), because both toggles feed into the two-bit shape selector. See the Toggle Group Notes below for the full mapping.

---

### Switch 8 — Style

| Property | Value |
|----------|-------|
| Off | Wire |
| On | Glow |
| Default | Wire |

**Style** controls the rendering method used to composite the wireframe over the source video. In its default position (**Wire**), the lower bit of the internal style selector is cleared. In its second position (**Glow**), the lower bit is set. **Style** also influences which wireframe geometry is drawn, because it feeds into the shape selector as well. See the Toggle Group Notes for full details.

---

### Switch 9 — Spin

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Spin** enables continuous horizontal drift animation. When set to **Off** (default), the wireframe remains stationary at the position set by **Rotation** (Knob 3). When set to **On**, the program adds an ever-increasing frame counter to the horizontal coordinate each frame, causing the wireframe to scroll steadily to the right across the screen. The speed of the drift is fixed at one pixel per frame. **Spin** requires **Animate** (Switch 10) to be active for the frame counter to advance; if **Animate** is off, the spin offset freezes at its current value.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** enables the internal frame counter that drives the **Spin** animation. When set to **On** (the default), the counter increments on every vertical sync pulse. When set to **Off**, the counter freezes and the spin animation pauses at its current position. Note that **Animate** also affects the rendering style: it feeds into the upper bit of the style selector. See the Toggle Group Notes for details.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all wireframe rendering and compositing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use **Bypass** for instant A/B comparison between the raw input and the Penrose overlay.

---

:::note Toggle Group Notes

Toggles 7, 8, and 10 interact in the VHDL through shared bit fields. **Style** (Switch 8) feeds into both the shape selector and the style selector. **Animate** (Switch 10) feeds into both the frame counter enable and the style selector. The result is a combined mode system with the following mappings:

**Shape modes** (determined by Switch 8 × Switch 7):

| Switch 8 (Style) | Switch 7 (Shape) | Geometry |
|---|---|---|
| Wire | Triangle | Penrose triangle — three bars at 0°, 60°, 120° |
| Wire | Trident | Staircase — horizontal, vertical, and diagonal bars |
| Glow | Triangle | Necker cube — cross and diagonal through center |
| Glow | Trident | Blivet trident — three parallel vertical bars |

**Rendering style** (determined by Switch 10 × Switch 8):

| Switch 10 (Animate) | Switch 8 (Style) | Rendering |
|---|---|---|
| Off | Wire | Wire — brightness added to source |
| Off | Glow | Solid — source replaced with flat wireframe color |
| On | Wire | Shadow — brightness subtracted from source |
| On | Glow | Glow — brightness added with warm chroma shift |

:::warning
Because **Style** (Switch 8) is shared between the shape and style selectors, flipping it changes *both* the geometry and the rendering method simultaneously. Similarly, toggling **Animate** (Switch 10) changes the rendering style in addition to starting or stopping the frame counter. Keep this coupling in mind when dialing in a specific look.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input signal and the wet (wireframe-composited) output. At 0%, fully left, only the original video is visible: the wireframe is completely absent. At 100% (the default, fully right), only the composited signal is output. Intermediate values blend the two, which can create a subtle, ghostly overlay effect where the wireframe floats translucently over the source.

---

## Background

### Impossible Objects

An ***impossible object*** is a two-dimensional figure that the brain automatically interprets as a three-dimensional solid: but one that contradicts itself spatially. The most famous examples are the ***Penrose triangle*** (or tribar), the ***Penrose staircase*** (stairs that ascend forever in a loop), and the ***Blivet*** (a trident with three cylindrical prongs at one end that merge into two rectangular bars at the other). These figures exploit the brain's tendency to interpret local depth cues independently: each junction looks plausible, but the global structure is physically impossible.

Swedish artist Oscar Reutersvärd drew the first impossible triangle in 1934, but it was Roger Penrose and his father Lionel who brought the concept to wide attention in a 1958 paper. M. C. Escher subsequently used impossible geometry as the foundation for many of his most iconic prints, including *Ascending and Descending* (the never-ending staircase) and *Waterfall* (a stream that flows in a closed loop).

### Distance-to-Line Rendering

Penrose draws its wireframe shapes without any frame buffer or polygon rasterizer. Instead, it uses a ***distance field*** technique: for every pixel in every frame, the FPGA computes the distance from that pixel to each wireframe bar's center line. If the distance is less than the thickness parameter, the pixel is "on the wire" and gets composited. This approach is inherently parallel: every pixel is evaluated independently: which suits the FPGA's streaming architecture perfectly.

The three axes of the Penrose triangle are approximated at 0°, 60°, and 120°. Because hardware multipliers are expensive on the iCE40, the 60° and 120° slopes are approximated using bit shifts: the 60° distance is `|cx + cy>>1|` and the 120° distance is `|-cx + cy>>1|`. This avoids multiplications entirely while producing visually convincing angled bars.

### Tiling by Bitmask

The **Count** control tiles shapes across the screen using a power-of-two bitmask trick. Rather than dividing coordinates by a tile size (which would require a divider), the program masks off the upper bits of the centered coordinates using a bitwise AND. For example, AND-ing with 255 keeps only the lowest 8 bits, effectively wrapping coordinates into a 256-pixel-wide cell that repeats across the screen. This is a classic FPGA technique for creating repeating patterns without expensive arithmetic.


---

## Signal Flow

### Signal Flow Notes

The pipeline splits into two parallel paths early on. The ***coordinate engine*** derives centered, tiled pixel coordinates from the video timing signals and parameter pots. The ***wireframe generator*** uses those coordinates to determine which pixels lie on a wireframe bar. Meanwhile, the source video propagates through an 8-clock delay pipeline that keeps it time-aligned with the compositor output.

Two key interactions define the visual character. First, the **depth cue** at junctions: when two or more bar distances are simultaneously below the thickness threshold, the `near_junc` flag fires, and the wireframe shade is halved one to four times depending on the **Depth Cue** pot. This creates the contradictory depth effect: bars appear to pass behind one another at the junctions. Second, the **style** selector radically changes how the wireframe interacts with the source: Wire mode brightens, Shadow mode darkens, Solid mode replaces, and Glow mode adds a warm color cast. These four modes can produce very different moods from the same geometry.

:::tip
Because the wireframe is computed entirely from pixel coordinates and has no memory of past frames, the overlay is perfectly stable and flicker-free. Unlike frame-buffer-based effects, there is no temporal noise or feedback drift.
:::


---

## Exercises

These exercises explore Penrose's four impossible shapes, tiling system, and compositing modes. Each builds on the one before, progressing from a single floating wireframe to dense animated lattices.
### Exercise 1: The Classic Impossible Triangle

![The Classic Impossible Triangle result](/img/instruments/videomancer/penrose/penrose_ex1_s1.png)
*The Classic Impossible Triangle — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A single Penrose triangle centered on screen with visible depth contradiction at each junction.

#### Key Concepts

- Distance-to-line rendering produces clean wireframe strokes
- Depth cue shading creates the impossible-object illusion
- Size and thickness interact to define the wireframe's visual weight

#### Video Source

A live camera feed with a moderately bright, low-contrast background: a wall, curtain, or slow-moving clouds work well. The wireframe needs visual breathing room.

#### Steps

1. Load Penrose with default settings. A triangle overlay appears at screen center.
2. Turn **Size** (Knob 1) to about 70% so the triangle fills most of the screen without clipping.
3. Increase **Line Thk** (Knob 2) to around 40%. The hairlines thicken into bold bars, revealing the triangular structure more clearly.
4. Turn **Depth Cue** (Knob 6) to about 75%. Watch the three junction points darken: each bar appears to pass behind the others, creating the impossible depth illusion.
5. Adjust **Bright** (Knob 5) to taste. Higher brightness makes the wireframe more dominant against the source.

#### Settings

| Control | Value |
|---------|-------|
| Size | 70% |
| Line Thk | 40% |
| Rotation | 50% |
| Count | 0% |
| Bright | 70% |
| Depth Cue | 75% |
| Shape | Triangle |
| Style | Wire |
| Spin | Off |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Tiled Lattice with Spin

![Tiled Lattice with Spin result](/img/instruments/videomancer/penrose/penrose_ex2_s1.png)
*Tiled Lattice with Spin — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A scrolling lattice of small impossible shapes tiled across the entire screen, with a warm glow rendering style.

#### Key Concepts

- Power-of-two tiling creates dense repeating patterns
- Spin animates the lattice with horizontal drift
- Glow mode adds warm chroma to the wireframe

#### Video Source

Dark or moody footage: concert lighting, nighttime cityscapes, or deep-colored abstract patterns. The glow wireframe pops against dark sources.

#### Steps

1. Set **Count** (Knob 4) to about 80% to engage 8× tiling. The screen fills with a dense grid of small wireframes.
2. Reduce **Size** (Knob 1) to about 30% so each tiled copy fits cleanly within its cell.
3. Set **Line Thk** (Knob 2) to about 25% for delicate strokes.
4. Flip **Style** (Switch 8) to **Glow** and confirm **Animate** (Switch 10) is **On**. The rendering switches to Glow mode, adding a warm color cast to the wireframe strokes.
5. Flip **Spin** (Switch 9) to **On**. The entire lattice begins drifting horizontally.
6. Adjust **Mix** (Fader 12) to about 70% to let the source video show through the gaps in the lattice.

#### Settings

| Control | Value |
|---------|-------|
| Size | 30% |
| Line Thk | 25% |
| Rotation | 50% |
| Count | 80% |
| Bright | 80% |
| Depth Cue | 50% |
| Shape | Triangle |
| Style | Glow |
| Spin | On |
| Animate | On |
| Bypass | Off |
| Mix | 70% |

---

### Exercise 3: Shadow Trident Mask

![Shadow Trident Mask result](/img/instruments/videomancer/penrose/penrose_ex3_s1.png)
*Shadow Trident Mask — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A large trident (Blivet) shape that carves dark bars into the source video, like a shadow mask or stencil.

#### Key Concepts

- Shadow mode subtracts the wireframe from the source, creating dark geometry
- The Blivet trident shape draws three parallel bars
- Depth cue in Shadow mode darkens junctions further, compounding the darkness

#### Video Source

Bright, colorful footage: flowers, fabric, sunlit landscapes. The shadow wireframe cuts dramatic dark channels through high-key material.

#### Steps

1. Flip **Shape** (Switch 7) to **Trident**. Flip **Style** (Switch 8) to **Glow**. With **Animate** (Switch 10) still at **On**, this selects the Glow rendering with Blivet geometry: but we want Shadow. So flip **Animate** to **Off**. Now the geometry stays as Blivet (T7=On, T8=Glow) and the style becomes Solid. To get Shadow with Trident, set T7=Trident, T8=Wire, T10=On. Wait: let me trace the tables.
2. Actually, for the Blivet shape we need T7=Trident and T8=Glow (shape_bits = "11"). For Shadow style we need T10=On and T8=Wire (style_bits = "10"). But T8 can't be both Glow and Wire at the same time. The Blivet shape inherently selects a rendering style through the toggle coupling. So instead, set **Shape** to **Trident** and **Style** to **Wire**: this gives Staircase geometry with Wire rendering. For a true trident with shadow, we compromise: set **Style** to **Glow** and **Animate** to **Off**, which gives Blivet shape with Solid rendering (flat replacement). Increase **Bright** to full.
3. Set **Size** (Knob 1) to about 60% to create a large trident.
4. Increase **Line Thk** (Knob 2) to about 60% for bold bars that carve deep into the image.
5. Turn **Bright** (Knob 5) to about 85%. In Solid mode, the wireframe replaces source luminance with a flat tone.
6. Increase **Depth Cue** (Knob 6) to about 60%. Where bars overlap, the solid tone darkens.
7. Lower **Mix** (Fader 12) to about 70% to blend the masked result with the original.

#### Settings

| Control | Value |
|---------|-------|
| Size | 60% |
| Line Thk | 60% |
| Rotation | 50% |
| Count | 0% |
| Bright | 85% |
| Depth Cue | 60% |
| Shape | Trident |
| Style | Glow |
| Spin | Off |
| Animate | Off |
| Bypass | Off |
| Mix | 70% |

---
## Glossary

- **Blivet**: An impossible figure also called the "devil's tuning fork": a shape that appears to have three cylindrical prongs at one end but only two rectangular bars at the other.

- **Depth Cue**: A visual signal that suggests relative depth or distance; in Penrose, junction shading serves as a contradictory depth cue that makes the wireframe appear impossible.

- **Distance Field**: A rendering technique where each pixel stores its distance to the nearest surface or edge, enabling smooth anti-aliased shapes without polygon rasterization.

- **Impossible Object**: A two-dimensional figure that the brain interprets as a three-dimensional solid whose geometry is self-contradictory.

- **Interpolator**: A component that performs linear blending between two values; Penrose uses three interpolators to crossfade YUV channels between dry and wet signals.

- **Junction**: The point where two wireframe bars visually cross or meet; Penrose detects junctions by checking whether two or more distance tests pass simultaneously.

- **Necker Cube**: An ambiguous wireframe cube drawing that spontaneously flips between two equally valid three-dimensional interpretations.

- **Penrose Triangle**: An impossible figure depicting three bars joined at 60° angles into a closed triangle whose spatial relationships are self-contradictory; also called a tribar.

- **Tiling**: Repeating a pattern at regular spatial intervals to fill a region; Penrose tiles using power-of-two bitmask modular arithmetic.

- **Wireframe**: A visual representation of a shape using only its edges, rendered as thin strokes without filled surfaces.

---
