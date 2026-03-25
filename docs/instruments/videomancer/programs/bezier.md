---
draft: true
sidebar_position: 17
slug: /instruments/videomancer/bezier
title: "Bezier"
image: /img/instruments/videomancer/bezier/bezier_hero.png
description: "Most video synthesis programs generate imagery from simple geometric primitives — grids, circles, straight lines."
---

![Bezier hero image](/img/instruments/videomancer/bezier/bezier_hero_s1.png)
*Bezier rendering four animated cubic curves as glowing calligraphic strokes with rainbow color cycling.*

---

## Overview

Bezier is a parametric curve animator that draws glowing cubic Bézier curves on a black canvas. Each curve is defined by four ***control points*** that orbit the screen in looping patterns, producing continuously evolving shapes. The program evaluates the curves mathematically during vertical blanking, then renders them pixel by pixel during active video using distance-based stroke rendering with soft anti-aliasing.

At gentle settings, Bezier draws a single luminous arc that drifts slowly across the frame. Push the controls further and the program weaves up to four simultaneous curves into a tangled, color-cycling tapestry of light. Enable **Calligraphic** mode and the strokes thicken and thin like a nib pen dragged across paper. Turn on **Video Mod** and the curves become an additive overlay on live video, tracing bright paths that follow the animation while the source image shows through beneath.

:::tip
Bezier is a ***synthesis*** program: it generates imagery from scratch. No input video is required for standalone use, but the **Video Mod** toggle lets you composite curves over a live signal.
:::

### What's In a Name?

The name ***Bezier*** honors Pierre Bézier, the French engineer at Renault who published the mathematical framework for parametric curves in 1962. The same curves were independently discovered a few years earlier by Paul de Casteljau at rival automaker Citroën, whose recursive evaluation algorithm: the ***De Casteljau algorithm***: is exactly what this program implements in hardware. Both men were designing tools to describe car body shapes with elegant mathematics. Six decades later, their curves are drawing light on your screen.

---

## Quick Start

1. Connect Videomancer's output to a monitor. With default settings, a single luminous arc glides across a dark background. Watch it for a moment (the shape is continuously evolving.)
2. Turn **Stroke Width** (Knob 2) clockwise. The line thickens into a broad ribbon of light. Turn it counterclockwise and it narrows to a hairline.
3. Flip the **Curves** toggle (Switch 7) to **4**. Three additional curves appear, each tracing its own path. The screen fills with intersecting arcs.
4. Increase **Animation Speed** (Knob 1). The curves move faster, weaving complex, ever-changing patterns.

---

## Parameters

![Videomancer front panel with Bezier loaded](/img/instruments/videomancer/bezier/bezier_control_panel.png)
*Videomancer's front panel with Bezier active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Animation Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Animation Speed** controls how fast the control points orbit, which determines how quickly the curve shapes evolve. At 0%, fully counterclockwise, the curves are frozen in place. As the value increases, the sixteen control points (four per curve) accelerate through their looping paths, and the curves shift and morph more rapidly. At 100%, fully clockwise, the animation runs at maximum speed, producing fast, fluid motion.

Each control point moves along a ***triangle wave*** path with a unique frequency. The frequencies are coprime multiples of the base speed, so the control points never all return to the same position at the same time (the pattern never exactly repeats.)

---

### Knob 2 — Stroke Width

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Stroke Width** sets the thickness of the rendered curves. At 0%, the curves are invisible: the distance threshold is zero and no pixels pass the stroke test. As the value increases, more pixels near each curve qualify as "on the curve," widening the visible stroke. At 100%, the strokes are at their maximum width.

:::note
Stroke Width interacts with **Glow** (Knob 4). When Glow is high, the brightness falloff is gradual, so the effective visual width of the stroke extends beyond the hard threshold set by Stroke Width.
:::

---

### Knob 3 — Amplitude

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Amplitude** controls the radius of the control point orbits, which determines how far the curves spread across the screen. At 0%, all control points cluster at the center, collapsing the curves into a point. As the value increases, the orbits widen and the curves sweep across a larger area of the frame. At 100%, the control points reach their maximum displacement from center.

---

### Knob 4 — Glow

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Glow** adjusts the softness of the distance falloff around each curve. At 0%, the brightness drops sharply at the edge of the stroke, producing hard-edged lines. As the value increases, the falloff becomes more gradual and the curves appear to emit a soft halo of light. The glow effect is computed by subtracting the pixel's distance from the **Brightness** value: a larger glow setting lets more of that gradient show through.

:::tip
For the brightest, sharpest lines, keep Glow low and **Brightness** (Knob 6) high. For soft, neon-like trails, increase both Glow and Brightness together.
:::

---

### Knob 5 — Color Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Color Speed** controls how fast the rainbow gradient cycles along and through the curves. At 0%, the color is static: each point on the curve holds a fixed hue. As the value increases, the color pattern scrolls along each curve and rotates over time, producing a flowing rainbow effect. At 100%, the cycling is at maximum speed. This control has no effect when **Color Mode** (Switch 8) is set to **Mono**.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Brightness** sets the peak luminance of the rendered curves. At 0%, the curves are completely dark. As the value increases, the maximum brightness of pixels on the curve rises. At 100%, curves render at full white. This value also serves as the ceiling for the **Glow** falloff: a pixel's luminance is computed as Brightness minus its distance to the nearest curve point, so higher Brightness means brighter cores and wider visible halos.

---

### Switch 7 — Curves

| Property | Value |
|----------|-------|
| Off | 1 |
| On | 4 |
| Default | 1 |

**Curves** selects the number of independent cubic Bézier curves rendered simultaneously. Set to **1**, a single curve traces a graceful arc across the screen. Set to **4**, all four curves are active, each following its own set of control points and producing a denser, more complex weave.

:::note
The actual number of rendered curves depends on the combination of this toggle and **Color Mode** (Switch 8): see the Toggle Group Notes section below for the full interaction table.
:::

---

### Switch 8 — Color Mode

| Property | Value |
|----------|-------|
| Off | Rainbow |
| On | Mono |
| Default | Rainbow |

**Color Mode** selects between **Rainbow** and **Mono** coloring. In Rainbow mode, each curve is colored with a four-quadrant hue palette that shifts along the curve's length and cycles over time via the **Color Speed** control. Cyan, green, magenta, and orange tones blend as the hue phase rotates. In Mono mode, curves are rendered in pure white (neutral chroma), producing clean monochrome strokes.

---

### Switch 9 — Calligraphic

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Calligraphic** enables stroke width modulation based on position along the curve. When set to **Off**, the stroke width is uniform from end to end. When set to **On**, the stroke thickens by fifty percent near the endpoints of each curve (roughly the first and last eighth of the parameter range), emulating the pressure variation of a calligraphy nib lifting off and pressing down on paper.

:::tip
Calligraphic mode is most visible with moderate **Stroke Width** values. At very thin or very wide settings, the fifty-percent variation is harder to see.
:::

---

### Switch 10 — Video Mod

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Video Mod** switches between standalone synthesis and additive overlay modes. When set to **Off**, the curves are drawn on a solid black background: Bezier produces a self-contained image with no dependence on the input signal. When set to **On**, the curve's luminance is ***added*** to the input video's brightness (clamped to maximum white), and the input's color is preserved. The result is a luminous overlay effect where curves brighten the underlying image without altering its hue.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Bezier rendering. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the synthesized output.

---

:::note Toggle Group Notes

The **Curves** (Switch 7) and **Color Mode** (Switch 8) toggles share a hardware register field that determines the curve count. The combination of both switches selects the actual number of rendered curves:

| Curves (Switch 7) | Color Mode (Switch 8) | Rendered Curves | Color |
|---|---|---|---|
| 1 | Rainbow | 1 | Rainbow |
| 4 | Rainbow | 2 | Rainbow |
| 1 | Mono | 3 | Mono |
| 4 | Mono | 4 | Mono |

In practice, this means switching Color Mode also changes the curve count. To get the maximum four curves with rainbow colors, swap to Mono and back: the curve count and color mode are linked through shared control bits. The labels **1** and **4** on the Curves switch represent the minimum and maximum values across all Color Mode combinations.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** blends between the delayed input video (dry) and the rendered curve output (wet). At 0%, the output is the unprocessed input. At 100%, the output is entirely the Bezier-rendered image. Intermediate values crossfade between the two. When **Video Mod** is off, the dry signal is black, so Mix fades the curves toward darkness. When Video Mod is on, Mix crossfades between the plain input and the curve-overlaid composite.

---

## Background

### Cubic Bézier curves

A cubic ***Bézier curve*** is defined by four points: two endpoints (P0 and P3) and two interior control points (P1 and P2) that pull the curve away from a straight line. As a parameter *t* sweeps from 0 to 1, the curve traces a smooth path from P0 to P3, bending toward P1 and P2 without necessarily passing through them. The control points act like magnets (they attract the curve but don't pin it down.)

Mathematically, the curve is a weighted blend of the four points, with the weights determined by cubic polynomials evaluated at each value of *t*. Move a control point, and the curve reshapes smoothly. This property made Bézier curves the foundation of modern vector graphics, font design, and CAD/CAM tools.

### The De Casteljau algorithm

Rather than evaluating the cubic polynomial directly, this program uses ***De Casteljau's algorithm***: a recursive process that reduces a cubic curve to a sequence of simple linear interpolations (lerps). For each value of *t*:

1. Lerp between adjacent control points: P0↔P1, P1↔P2, P2↔P3 → three intermediate points
2. Lerp between those intermediates → two points
3. Lerp between those two → the final curve point

Three stages, six lerps, one output. The algorithm is numerically stable and maps naturally to FPGA pipeline stages. Bezier evaluates 64 samples per curve during vertical blanking and stores the results in ***block RAM***, then uses those stored points for pixel-by-pixel rendering during active video.

### Distance-based rendering

Unlike a CPU-based vector renderer that rasterizes curve segments into pixel spans, this program takes a brute-force approach suited to parallel hardware. For each pixel on screen, the renderer computes the ***Manhattan distance*** (the sum of horizontal and vertical offsets) to nearby stored curve points. If the distance falls within the stroke threshold, the pixel is lit.

Manhattan distance is cheaper than true Euclidean distance: no square root needed: and produces slightly diamond-shaped strokes instead of perfectly round ones. The visual difference is subtle at typical stroke widths.

### Animation via DDS

The sixteen control points (four per curve, four curves) are animated using ***direct digital synthesis*** (DDS) phase accumulators. Each control point has independent X and Y phase accumulators that increment at coprime rates derived from the **Animation Speed** parameter. The phase drives a triangle wave function that produces smooth, bounded oscillation. Because the frequency ratios are coprime, the combined motion is quasi-periodic (the pattern evolves continuously without exact repetition.)


---

## Signal Flow

### Signal Flow Notes

The program operates in two distinct phases each frame. During ***vertical blanking***, the control point positions are updated via DDS animation and all curve sample points are recalculated using De Casteljau evaluation. The results are written to a 256-entry block RAM (4 curves × 64 samples, with each entry packing a 10-bit X and 10-bit Y coordinate). During ***active video***, the renderer reads from this RAM for each pixel, computing distances to find the closest curve point and determining stroke membership, color, and brightness.

Two key interactions govern the visual output:

1. **Glow and Brightness coupling**: The pixel luminance is computed as Brightness minus distance. A high Brightness value with moderate Glow produces bright cores with soft halos. A low Brightness with high Glow produces dim, diffuse strokes.

2. **Video Mod compositing**: When Video Mod is on, curve luminance is *added* to the input video's Y channel (clamped at maximum), while the input's chroma passes through unchanged. This means curves always brighten: they cannot darken the source. When Video Mod is off, pixels not on a curve render as black with neutral chroma.

:::note
The curve evaluation must complete during vertical blanking before active video begins. With four curves at 64 samples each and three pipeline stages per sample, evaluation takes 4 × 64 × 3 = 768 clock cycles. At 74.25 MHz with roughly 2,000 blanking clocks per field, this fits comfortably.
:::


---

## Exercises

These exercises explore Bezier's curve rendering from a single delicate arc to dense, animated weaves and video overlays.
### Exercise 1: Luminous Arc

![Luminous Arc result](/img/instruments/videomancer/bezier/bezier_ex1_s1.png)
*Luminous Arc — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A single glowing arc that drifts smoothly across a dark background, demonstrating the fundamental curve rendering.

#### Key Concepts

- A single cubic Bézier curve is defined by four animated control points
- Stroke Width and Glow together control the visual thickness and softness
- Brightness sets the peak luminance

#### Steps

1. Start with default settings. A single curve traces a slow arc across the screen.
2. Turn **Stroke Width** (Knob 2) clockwise to about 50%. The line broadens into a visible ribbon.
3. Increase **Glow** (Knob 4) to about 60%. The edges of the stroke soften and the curve appears to emit a dim halo.
4. Set **Brightness** (Knob 6) to about 70%. The arc brightens, and the glow halo extends further.
5. Slowly increase **Amplitude** (Knob 3). The curve's control points sweep wider and the arc stretches across more of the screen.
6. Now increase **Animation Speed** (Knob 1) to about 30%. The arc begins to drift and reshape as its control points orbit.

#### Settings

| Control | Value |
|---------|-------|
| Animation Speed | ~30% |
| Stroke Width | ~50% |
| Amplitude | 50% |
| Glow | ~60% |
| Color Speed | 25% |
| Brightness | ~70% |
| Curves | 1 |
| Color Mode | Rainbow |
| Calligraphic | Off |
| Video Mod | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Calligraphic Weave

![Calligraphic Weave result](/img/instruments/videomancer/bezier/bezier_ex2_s1.png)
*Calligraphic Weave — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dense tapestry of four calligraphic strokes with flowing rainbow colors, continuously weaving and overlapping.

#### Key Concepts

- Multiple curves create layered, intersecting patterns
- Calligraphic mode adds nib-like thickness variation
- Color Speed animates the rainbow hue cycling

#### Steps

1. Set **Curves** (Switch 7) to **4** and **Color Mode** (Switch 8) to **Mono**. Four white curves appear, each following its own animation path.
2. Switch **Color Mode** back to **Rainbow**. The curves reduce to two, now rendered in cycling hues.
3. Return to **Mono** to restore four curves, then enable **Calligraphic** (Switch 9). The strokes develop visible thickness variation (thicker at the ends, thinner in the middle.)
4. Increase **Stroke Width** (Knob 2) to about 40% to make the calligraphic variation more pronounced.
5. Set **Amplitude** (Knob 3) to about 60% so the curves span most of the frame.
6. Increase **Color Speed** (Knob 5) to about 50%. Switch **Color Mode** to **Rainbow** (now 2 curves). Watch the hue pattern scroll along each curve and rotate over time.
7. Increase **Animation Speed** (Knob 1) to about 40%. The curves weave around each other in a continuously evolving pattern.

#### Settings

| Control | Value |
|---------|-------|
| Animation Speed | ~40% |
| Stroke Width | ~40% |
| Amplitude | ~60% |
| Glow | ~25% |
| Color Speed | ~50% |
| Brightness | ~75% |
| Curves | 4 |
| Color Mode | Mono |
| Calligraphic | On |
| Video Mod | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Video Overlay

![Video Overlay result](/img/instruments/videomancer/bezier/bezier_ex3_s1.png)
*Video Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Glowing curves composited over a live video feed, producing a luminous overlay effect.

#### Key Concepts

- Video Mod adds curve luminance to the input signal
- Mix crossfades between input and the curve-overlaid composite
- Curves act as additive light sources on live video

#### Steps

1. Connect a video source to Videomancer's input.
2. Set **Video Mod** (Switch 10) to **On**. The curves now brighten the input image wherever they pass.
3. Reduce **Brightness** (Knob 6) to about 40% so the curves add a subtle glow rather than blowing out the highlights.
4. Set **Curves** (Switch 7) to **4** and **Color Mode** (Switch 8) to **Mono** for four white overlaid curves.
5. Enable **Calligraphic** (Switch 9) for varied stroke weight that gives the overlay organic character.
6. Increase **Stroke Width** (Knob 2) to about 20%. Thin strokes look like light trails over the video.
7. Set **Mix** (Fader 12) to about 75% to blend the overlay with the unprocessed input, softening the effect.
8. Adjust **Animation Speed** (Knob 1) to taste. Slow speeds produce drifting highlights; faster speeds create rapid flickering trails.

#### Settings

| Control | Value |
|---------|-------|
| Animation Speed | ~25% |
| Stroke Width | ~20% |
| Amplitude | 50% |
| Glow | ~70% |
| Color Speed | ~25% |
| Brightness | ~40% |
| Curves | 4 |
| Color Mode | Mono |
| Calligraphic | On |
| Video Mod | On |
| Bypass | Off |
| Mix | ~75% |

---
## Glossary

- **Block RAM (BRAM)**: A dedicated memory block inside the FPGA used to store precomputed curve sample points for pixel-by-pixel rendering.

- **Bézier Curve**: A parametric curve defined by a set of control points, widely used in computer graphics for smooth shape representation.

- **Calligraphic**: A rendering style where stroke width varies along the curve, emulating the natural pressure variation of a pen nib.

- **Control Point**: One of four points that define the shape of a cubic Bézier curve; the curve bends toward its control points without necessarily passing through them.

- **DDS (Direct Digital Synthesis)**: A technique for generating periodic waveforms by incrementing a phase accumulator at a fixed rate; used here to animate control point positions.

- **De Casteljau Algorithm**: A recursive method for evaluating Bézier curves using repeated linear interpolation, noted for numerical stability.

- **Lerp (Linear Interpolation)**: A blend between two values controlled by a parameter *t*, producing the value a + (b − a) × t.

- **Manhattan Distance**: The sum of horizontal and vertical offsets between two points, used as a computationally cheap approximation to Euclidean distance.

- **Synthesis Program**: An FPGA program that generates imagery from scratch, independent of any input video signal.

- **Triangle Wave**: A periodic waveform that ramps linearly up and down, used here as a smooth bounded oscillator for control point animation.

---
