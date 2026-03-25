---
draft: true
sidebar_position: 93
slug: /instruments/videomancer/dragon
title: "Dragon"
image: /img/instruments/videomancer/dragon/dragon_hero.png
description: "In 1966, NASA physicist John Heighway discovered a curve by repeatedly folding a strip of paper in half and unfolding it so that each crease opens to a right angle."
---

![Dragon hero image](/img/instruments/videomancer/dragon/dragon_hero_s1.png)
*Dragon conjuring a self-similar fractal mosaic of XOR-folded geometry across the screen in vivid, position-derived color.*

---

## Overview

**Dragon** is a real-time fractal synthesis program that generates intricate, self-similar patterns across the entire video frame. Its core engine hashes each pixel's spatial coordinates through a series of ***XOR folds***: bitwise exclusive-or operations that collapse position data into a fractal tiling. The result is a dense geometric tapestry whose complexity and structure you control with a single knob. At low iteration depths, Dragon produces bold, blocky checker-like regions. At high depths, it reveals delicate, branching filigree reminiscent of the mathematical dragon curve.

Dragon's chromatic mode paints the fractal with hues derived from each pixel's position hash, producing a stained-glass mosaic of shifting color. Mirror mode injects an additional fold that creates bilateral symmetry, doubling the pattern into a kaleidoscopic reflection. Because the entire pattern is generated spatially: no video input required: Dragon excels as a stand-alone visual source for live performance, layering, or keying with other Videomancer programs.

:::tip
Dragon is a ***synthesis*** program. It generates imagery from scratch. No video input is needed, though input video can be blended in using the **Brightness** fader.
:::

### What's In a Name?

The name **Dragon** refers to the ***dragon curve***, a famous fractal discovered by physicist John Heighway in the 1960s. The dragon curve can be produced by repeatedly folding a strip of paper in half and then unfolding it so each fold stands at a right angle. Mathematically, the fold direction at each step is determined by examining specific bits of the step index: precisely the kind of bit-manipulation this program performs. Like the mythological creature, the pattern is elaborate and seemingly chaotic, yet governed by simple, elegant rules.

---

## Quick Start

1. With default settings, you'll see a colorful fractal pattern covering the screen. The colors shift across the surface because **Color Cycle** (Switch 8) is on by default.
2. Turn **Iteration** (Knob 5) slowly. At low values, the pattern is coarse: large regions of solid color. As you increase it, finer and finer fractal detail emerges, as if you're zooming into the dragon's scales.
3. Sweep **Position X** (Knob 3) and **Position Y** (Knob 4) to slide the entire fractal pattern across the screen. The pattern tiles infinitely, so new structure scrolls in from the edges.
4. Flip **Mirror** (Switch 10) on. The pattern doubles into a symmetric reflection (a dragon gazing at its own twin.)

---

## Parameters

![Videomancer front panel with Dragon loaded](/img/instruments/videomancer/dragon/dragon_control_panel.png)
*Videomancer's front panel with Dragon active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Scale

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Scale** is reserved for a future update. In the current version of Dragon, adjusting this knob does not change the output. It is mapped to the hardware register and ready for use when additional scaling logic is added to the fractal engine.

---

### Knob 2 — Rotation

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Rotation** is reserved for a future update. In the current version, adjusting this knob does not change the output. It is mapped to the hardware register and ready for use when angular rotation of the fractal pattern is implemented.

---

### Knob 3 — Position X

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Position X** slides the fractal pattern horizontally across the screen. At the default center position, the hash origin sits near the middle of the frame. Turning the knob counterclockwise shifts the pattern to the right; turning it clockwise shifts the pattern to the left. Because the fractal tiles infinitely in all directions, you never run out of pattern: new structure continuously scrolls into view. Position X pairs naturally with **Position Y** (Knob 4) for two-axis panning.

---

### Knob 4 — Position Y

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Position Y** slides the fractal pattern vertically. At the default center position, the hash origin sits near the vertical midpoint. Turning the knob shifts the pattern up or down. Combined with **Position X** (Knob 3), you can navigate freely through the infinite fractal plane, discovering new regions of the pattern.

---

### Knob 5 — Iteration

| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 9 |

**Iteration** controls the depth of the XOR-fold operation that generates the fractal. This knob selects one of sixteen discrete steps. At low values, only one or two folds are applied, producing large, blocky regions of alternating pattern. As you increase the iteration depth, additional folds subdivide the pattern into progressively finer structure. At maximum, the fractal reveals its full complexity: a dense, branching network of self-similar tiles. This is Dragon's primary creative control.

:::tip
***Iteration is Dragon's signature control.*** It's the difference between a bold geometric grid and an intricate fractal web. Sweep it slowly to watch the pattern unfold level by level.
:::

---

### Knob 6 — Line Width

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

**Line Width** is reserved for a future update. In the current version, adjusting this knob does not change the output. It is mapped to the hardware register and ready for use when variable-width fractal rendering is added.

---

### Switch 7 — Fill

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Fill** is reserved for a future update. In the current version, toggling this switch does not change the output. It is mapped to the hardware register for future use.

---

### Switch 8 — Color Cycle

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Color Cycle** enables position-derived coloring of the fractal pattern. When set to **On** (the default), each lit pixel receives hue values extracted from the position hash. The U and V chrominance channels are set from different bit slices of the hash, producing a mosaic of shifting color that varies across the surface. When set to **Off**, the fractal is rendered in monochrome: lit pixels are a uniform neutral gray at the brightness level set by **Brightness** (Fader 12), and dark pixels remain near-black.

:::note
Because color is derived from the position hash, the hue at any given screen location is deterministic. Moving the pattern with **Position X** or **Position Y** changes which colors are visible, but the color at a given fractal coordinate is always the same.
:::

---

### Switch 9 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** enables a per-frame counter that increments on every vertical sync pulse. In the current version of Dragon, the animation counter is internal and reserved for future use: the visible pattern does not change between frames. The fractal remains static regardless of this toggle's position.

---

### Switch 10 — Mirror

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mirror** introduces an additional XOR fold into the pattern hash, combining a third bit of the hash with the base pattern. The result is a symmetry transformation: regions that were uniform split into mirrored pairs, and the overall pattern takes on bilateral symmetry. Enable Mirror to double the visual complexity and create kaleidoscopic reflections within the fractal.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input video directly to the output, bypassing all Dragon processing. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the fractal output and whatever signal is patched into the input.

---

### Fader 12 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Brightness** controls two things simultaneously. First, it sets the luminance of the lit pixels in the fractal pattern: higher values produce a brighter pattern against the near-black background. Second, it controls the wet/dry mix between the generated fractal and any video present at the input. At 0%, the output is pure input video (if any). At 100%, the output is the full-brightness fractal with no input bleed. At intermediate values, the fractal is superimposed over the input at reduced intensity, creating a translucent overlay.

:::tip
Because Brightness controls both intensity and mix, pulling the fader down doesn't just dim the fractal: it also fades in the input video underneath. This makes it easy to blend Dragon's patterns over a live camera feed or another program's output.
:::

---

## Background

### The dragon curve

The ***dragon curve*** is one of the most elegant fractals in mathematics. It was discovered in the 1960s by NASA physicist John Heighway, who noticed the pattern that emerges when you fold a strip of paper in half repeatedly and then unfold it so each crease stands at a right angle. The resulting shape: also called the ***Heighway dragon***: is a space-filling curve: given enough folds, it tiles the plane completely without gaps or overlaps.

What makes the dragon curve special is how the fold direction at each step is determined. If you number each fold starting from one, you can figure out whether to fold left or right by examining specific bits of that number. This is the connection to digital logic: the dragon curve is, at its heart, a ***bit-manipulation*** problem. Each level of iteration adds one more bit of information, doubling the curve's complexity.

### XOR folding

Dragon's pattern engine uses the ***exclusive-or*** (XOR) operation to create fractal structure from pixel coordinates. XOR is a fundamental digital logic operation: it outputs one when its two inputs differ and zero when they match. When applied to shifted copies of a number, XOR produces self-similar patterns: each level of shifting introduces a new scale of detail that echoes the previous one.

The program constructs a 16-bit hash from each pixel's horizontal and vertical position, then folds that hash against a shifted copy of itself. The **Iteration** knob controls how far the second copy is shifted before the XOR, directly setting the depth of fractal detail. This is a computationally elegant approach: the entire fractal is generated with just a few XOR and shift operations per pixel, requiring no memory buffers, no look-up tables, and no complex arithmetic.

### Self-similarity

***Self-similarity*** is the defining property of fractals. A self-similar object looks the same: or statistically similar: at every scale of magnification. The dragon curve exhibits this property: any section of the curve, when magnified, reveals the same branching structure as the whole.

In Dragon, self-similarity appears as you sweep the **Iteration** knob: each additional fold level adds detail that echoes the coarser pattern already visible. The coarse structure doesn't change: it gains finer ornamentation. This is a hallmark of ***iterated function systems*** (IFS), a class of fractals where the whole is built from smaller copies of itself.


---

## Signal Flow

### Signal Flow Notes

The fractal engine is purely combinational within a single clock cycle: pixel coordinates are centered, hashed, folded, and mapped to color in one pipeline stage. The resulting fractal YUV values are then blended with the ***delayed*** input video through three `interpolator_u` instances, which contribute four additional clock cycles each.

The critical interaction is the dual role of **Brightness** (Fader 12). The same register value simultaneously sets the luminance of lit fractal pixels *and* the interpolation coefficient for the wet/dry mix. When Brightness is high, the fractal is both bright and dominant over the input. When Brightness is low, the fractal dims *and* the input shows through. This coupling is intentional: it provides a single-fader "presence" control for the fractal.

:::note
The input data delay pipeline (8 clocks) aligns the passthrough video with the fractal + interpolator output. This ensures glitch-free bypass switching and clean blending.
:::


---

## Exercises

These exercises explore Dragon's fractal engine from basic pattern generation through chromatic variations to overlay blending. Each exercise builds on the previous one.
### Exercise 1: Fractal Depth

![Fractal Depth result](/img/instruments/videomancer/dragon/dragon_ex1_s1.png)
*Fractal Depth — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Explore the full range of Dragon's fractal complexity by sweeping the Iteration control.

#### Key Concepts

- Iteration depth controls fractal complexity
- Position knobs pan through an infinite fractal plane
- The pattern is generated mathematically (no video input needed)

#### Steps

1. **Start simple**: Turn **Iteration** (Knob 5) to its lowest setting. You see a pattern of large, boldly colored blocks filling the screen.
2. **Build complexity**: Slowly increase Iteration. With each step, finer detail emerges within the existing blocks. The coarse structure persists while new subdivisions appear.
3. **Full depth**: Set Iteration to its maximum. The screen fills with dense, intricate fractal geometry.
4. **Navigate**: Sweep **Position X** (Knob 3) and **Position Y** (Knob 4) to pan across the fractal plane. Note how the pattern tiles seamlessly (new structure scrolls in from every edge.)
5. **Monochrome view**: Flip **Color Cycle** (Switch 8) to **Off**. The same fractal geometry is now rendered in grayscale, making the self-similar structure easier to see.

#### Settings

| Control | Value |
|---------|-------|
| Scale | ~50% |
| Rotation | 0° |
| Position X | ~50% |
| Position Y | ~50% |
| Iteration | 16 |
| Line Width | 1 |
| Fill | Off |
| Color Cycle | Off |
| Animate | Off |
| Mirror | Off |
| Bypass | Off |
| Brightness | ~75% |

---

### Exercise 2: Chromatic Dragon

![Chromatic Dragon result](/img/instruments/videomancer/dragon/dragon_ex2_s1.png)
*Chromatic Dragon — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Build a vivid, symmetrical stained-glass fractal.

#### Key Concepts

- Color Cycle derives hue from the position hash
- Mirror creates bilateral symmetry via an additional XOR fold
- Brightness controls both intensity and presence

#### Steps

1. **Enable color**: Ensure **Color Cycle** (Switch 8) is set to **On**. The fractal fills with shifting hues derived from each pixel's position.
2. **Add symmetry**: Flip **Mirror** (Switch 10) to **On**. The pattern doubles into a symmetric reflection, creating a kaleidoscopic effect.
3. **Set depth**: Adjust **Iteration** (Knob 5) to a moderate value: around step 10–12. This provides enough detail to see the fractal branching without overwhelming density.
4. **Brighten**: Push **Brightness** (Fader 12) to about 60%. The colors pop against the near-black background.
5. **Explore position**: Pan with **Position X** and **Position Y** to find a region where the mirrored pattern forms an interesting composition. Some positions create butterfly-like shapes; others form crystalline lattices.

#### Settings

| Control | Value |
|---------|-------|
| Scale | ~50% |
| Rotation | 0° |
| Position X | ~50% |
| Position Y | ~50% |
| Iteration | 12 |
| Line Width | 1 |
| Fill | Off |
| Color Cycle | On |
| Animate | Off |
| Mirror | On |
| Bypass | Off |
| Brightness | ~60% |

---

### Exercise 3: Fractal Overlay

![Fractal Overlay result](/img/instruments/videomancer/dragon/dragon_ex3_s1.png)
*Fractal Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Blend Dragon's fractal pattern over an input video signal to create a translucent geometric overlay.

#### Key Concepts

- Brightness controls the wet/dry mix between fractal and input video
- The interpolator blends all three channels (Y, U, V) simultaneously
- Dragon works as a texture overlay when blended with another source

#### Steps

1. **Connect input**: Patch a video source into Videomancer's input (a live camera, another program, or recorded footage.)
2. **Full fractal**: Set **Brightness** (Fader 12) to maximum. You see only the fractal pattern.
3. **Fade in the source**: Slowly pull **Brightness** down. As the value decreases, two things happen simultaneously: the fractal dims *and* the input video fades in underneath. At about 40–50%, you get a translucent overlay where both layers are clearly visible.
4. **Tune the pattern**: Adjust **Iteration** (Knob 5) to control how dense the overlay grid is. Lower iterations create bold geometric frames; higher iterations create a fine mesh.
5. **Color blend**: With **Color Cycle** on, the fractal's position-derived hues tint the underlying video. Toggle it off for a monochrome mesh that preserves the source colors.
6. **A/B compare**: Flip **Bypass** (Switch 11) to see the clean input, then back to see the overlay. This confirms the blend level.

#### Settings

| Control | Value |
|---------|-------|
| Scale | ~50% |
| Rotation | 0° |
| Position X | ~50% |
| Position Y | ~50% |
| Iteration | 8 |
| Line Width | 1 |
| Fill | Off |
| Color Cycle | On |
| Animate | Off |
| Mirror | Off |
| Bypass | Off |
| Brightness | ~45% |

---
## Glossary

- **Dragon Curve**: A fractal discovered by John Heighway, produced by repeatedly folding a strip of paper in half and unfolding at right angles; also called the Heighway dragon.

- **Fractal**: A geometric shape exhibiting self-similarity: the same structural pattern appears at every scale of magnification.

- **Hash**: A mathematical function that converts input data (here, pixel coordinates) into a fixed-size numerical fingerprint used to generate patterns.

- **Interpolator**: A hardware module that smoothly blends between two values based on a third control value; used here for wet/dry mixing.

- **Iteration**: One pass of a repeated mathematical operation; each additional iteration adds a finer level of detail to the fractal.

- **Self-Similarity**: The property of looking the same at different scales; the defining characteristic of fractal geometry.

- **Synthesis**: A program type that generates imagery from scratch without requiring a video input signal.

- **XOR (Exclusive-Or)**: A digital logic operation that outputs one when its two inputs differ and zero when they match; the core operation in Dragon's pattern engine.

- **YUV**: A color encoding that separates brightness (Y) from color information (U and V), used in video signal processing.

---
