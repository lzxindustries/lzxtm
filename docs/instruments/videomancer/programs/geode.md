---
draft: true
sidebar_position: 128
slug: /instruments/videomancer/geode
title: "Geode"
image: /img/instruments/videomancer/geode/geode_hero.png
description: "Geode draws regular polygons on screen — triangles, squares, pentagons, hexagons, heptagons, and octagons — using a real-time half-plane rasterizer built entirely in FPGA logic."
---

![Geode hero image](/img/instruments/videomancer/geode/geode_hero_s1.png)
*Geode rendering a luminous rotating hexagon with radial vertex morph animation against a black void.*

---

## Overview

**Geode** is a polygon shape synthesizer that draws glowing geometric figures directly on the video output. It renders convex polygons with three to six sides: triangles, squares, pentagons, and hexagons: centered on screen and rotating continuously. Vertices are placed on a circle using a sine/cosine lookup table, and the polygon's shape can be animated with a radial morph oscillation that pushes vertices in and out, creating a pulsing, organic quality.

The program computes everything from scratch. No input video is required, though input video can be used as a fill texture inside the polygon or as a visible background behind it. Geode belongs to the ***synthesis*** family of programs: it generates its own imagery rather than transforming an existing signal.

At its simplest, Geode draws a still white polygon on black. At its most complex, it produces slowly morphing kaleidoscopic crystal shapes filled with live video, hovering over a secondary video background (a clean geometric window into another world.)

:::tip
Because Geode is a synthesizer, it produces output even with no video input connected. Patch it at the end of your signal chain to composite polygon shapes over other effects, or use it standalone for pure geometric animation.
:::

### What's In a Name?

A ***geode*** is a hollow rock whose rough, unremarkable exterior conceals a cavity lined with crystals. The name reflects the program's nature: simple polygon geometry on the outside, but with faceted complexity revealed through morph animation and hue shifting. Like cracking open a stone to find amethyst formations inside, turning Geode's controls reveals hidden geometries within basic shapes.

---

## Quick Start

1. Turn **Sides** (Knob 1) fully clockwise to select a hexagon. A bright white hexagonal shape appears centered on a black background.
2. Increase **Size** (Knob 2) to fill more of the screen. The polygon expands outward from the center.
3. Turn **Rotation** (Knob 3) clockwise. The hexagon begins to spin, its speed increasing with the knob position.
4. Increase **Morph** (Knob 4). The vertices begin pulsing inward and outward at different rates, turning the rigid hexagon into a breathing, organic crystal shape.

---

## Parameters

![Videomancer front panel with Geode loaded](/img/instruments/videomancer/geode/geode_control_panel.png)
*Videomancer's front panel with Geode active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Sides

| Property | Value |
|----------|-------|
| Range | 3 – 8 |
| Default | 6 |

**Sides** selects the number of vertices in the polygon. The knob sweeps across four discrete positions, producing a triangle (three sides), a square (four sides), a pentagon (five sides), and a hexagon (six sides). Turning the knob counterclockwise selects fewer sides; turning it clockwise selects more. The default position (center) produces a pentagon.

The number of sides determines the overall character of the shape. Triangles have an aggressive, angular quality. Squares feel stable and architectural. Pentagons and hexagons become more circular and crystalline, especially when morph animation is active.

:::note
The hardware display shows a range of 3 to 8, but the FPGA architecture implements four distinct polygon types (3, 4, 5, and 6 sides). Display values above 6 produce a hexagon.
:::

---

### Knob 2 — Size

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Size** controls the radius of the polygon, determining how large the shape appears on screen. At 0%, the polygon collapses to a point at the center. At the default (50%), a medium-sized polygon is drawn. At 100%, the polygon extends to fill most of the frame.

:::note
At large sizes, the polygon's edges may extend beyond the visible frame. This is normal: the polygon is mathematically clipped to the active video area by the scanline span computation.
:::

---

### Knob 3 — Rotation

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Rotation** sets the speed of continuous rotation animation. At 0% (fully counterclockwise and the default), the polygon is stationary. Increasing the value causes the polygon to spin faster. The rotation is driven by a ***direct digital synthesis*** accumulator that adds the knob value to a phase register on each frame, so the motion is smooth and continuous regardless of video format.

Even a small amount of rotation brings the shape to life, especially when combined with **Morph** animation.

---

### Knob 4 — Morph

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Morph** controls the amplitude of a radial oscillation applied independently to each vertex. At 0% (the default), all vertices sit at the same distance from the center, and the polygon is perfectly regular. As the value increases, vertices begin pulsing inward and outward at different phases, distorting the polygon into star-like, flower-like, or amoebic forms.

The morph animation uses a ***triangle wave*** at a fixed internal rate. Each vertex oscillates at a different phase offset (evenly spaced around the polygon), creating a mesmerizing ripple effect around the perimeter. Higher **Morph** values produce more dramatic deformation, while lower values create subtle breathing.

:::tip
Combine high **Morph** with a triangle (**Sides** fully counterclockwise) for a three-pointed star effect. With a hexagon and moderate morph, the shape resembles a rotating crystal or snowflake.
:::

---

### Knob 5 — Edge Glow

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Edge Glow** controls the width of a luminance highlight along the polygon's edges. At 0%, no edge highlight is drawn: the shape has hard boundaries. Increasing the value widens the glow band around the perimeter, creating a soft neon-like outline effect. The default is approximately 25%.

:::note
This parameter is mapped to the FPGA registers but is reserved for a future implementation of edge proximity distance computation. In the current version, the polygon renders with hard edges regardless of this control's position.
:::

---

### Knob 6 — Hue

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Hue** selects the color of the polygon's solid fill. The control sweeps through four color zones. In the first quarter (0 to 25%), the polygon is filled with pure white: no chroma. In the second quarter (25 to 50%), a warm tint is applied: blue-difference increases and red-difference decreases. In the third quarter (50 to 75%), a cool tint is applied: blue-difference decreases and red-difference increases. In the final quarter (75 to 100%), a golden amber tone is produced by boosting both chroma components. The default is center (50%).

**Hue** has no effect when **Fill Src** (Switch 7) is set to **Video**, because the fill color is taken directly from the input video stream in that mode.

---

### Switch 7 — Fill Src

| Property | Value |
|----------|-------|
| Off | Color |
| On | Video |
| Default | Color |

**Fill Src** selects the source for the polygon's interior color. When set to **Color** (the default), the polygon is filled with a solid color determined by the **Hue** knob. When set to **Video**, the polygon is filled with the input video signal, creating a shaped window through which the video is visible.

---

### Switch 8 — Draw Mode

| Property | Value |
|----------|-------|
| Off | Filled |
| On | Edge |
| Default | Filled |

**Draw Mode** selects how the polygon is rendered. When set to **Filled** (the default), the entire interior of the polygon is drawn. When set to **Edge**, only the outline of the polygon is visible.

:::note
This parameter is mapped to the FPGA registers but is reserved for a future implementation of edge-only rendering. In the current version, the polygon is always rendered as a filled shape regardless of this switch position.
:::

---

### Switch 9 — Double

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Double** enables a second polygon that rotates in the opposite direction from the primary shape. When set to **Off** (the default), only one polygon is drawn. When set to **On**, a second counter-rotating polygon of the same size and vertex count overlaps the first, creating interference patterns and symmetrical compositions.

:::note
This parameter is mapped to the FPGA registers but is reserved for a future implementation of dual-polygon rendering. In the current version, only a single polygon is drawn regardless of this switch position.
:::

---

### Switch 10 — Background

| Property | Value |
|----------|-------|
| Off | Black |
| On | Video |
| Default | Black |

**Background** selects what is drawn behind the polygon. When set to **Black** (the default), the area outside the polygon is filled with black (Y=0, U=512, V=512). When set to **Video**, the input video signal is displayed behind the polygon, allowing the geometric shape to be composited over live footage.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the input signal directly to the output, bypassing all Geode rendering. The sync delay pipeline still aligns timing signals, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the generated polygon output.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the unprocessed input (dry) and the Geode output (wet). At 0%, the output is entirely the dry input signal. At 100% (the default), the output is entirely the generated polygon image. Intermediate positions blend the two together, useful for ghostly overlay effects where the polygon fades in and out of the source material.

---

## Background

### Polygon rasterization on a scanline renderer

Traditional computer graphics draws polygons by filling triangles with a ***rasterizer*** that works in two-dimensional framebuffer space. Geode takes a different approach suited to real-time video hardware: it evaluates polygon containment per scanline, computing the left and right boundaries of the polygon on each horizontal line and filling the span in between. This technique is called ***scanline rendering*** and was one of the earliest practical methods for drawing filled shapes in computer graphics.

For each scanline, Geode clips the polygon to a horizontal slice at that line's Y coordinate. It walks each edge of the polygon, finds where the edge crosses the current scanline using iterative binary division, and narrows a span window from both sides. During active video, each pixel is tested against this span: a simple range check that determines whether the pixel falls inside or outside the polygon.

### Sin/cos lookup and DDS animation

Geode places polygon vertices on a circle using a 1024-entry ***sine/cosine lookup table*** stored in FPGA logic fabric as combinational ROM. The table accepts a 10-bit angle (0 to 1023, representing 0° to 360°) and returns both sine and cosine as signed 10-bit values. Vertex positions are computed by multiplying the cosine and sine of each vertex's angle by the polygon radius, then adding the screen center offset.

The rotation animation uses a ***direct digital synthesis*** (DDS) accumulator: a 20-bit register that adds the **Rotation** knob value on every vertical sync pulse. The accumulator's upper 10 bits become the base angle for vertex placement. Because the accumulator wraps naturally at its word width, rotation is seamless and continuous. The speed is proportional to the knob value, and at zero the polygon is stationary.

### Morph animation

The morph effect applies a per-vertex radial oscillation. Each vertex has a different phase offset (spaced evenly by 171 angle units, approximately 60° per vertex), and the oscillation is driven by a separate 20-bit accumulator that increments by 37 counts per frame. This slow, fixed-rate accumulator means the morph animation runs at a constant speed regardless of the **Morph** knob: the knob controls only the *amplitude* of the oscillation, not the speed.

Within the vertex computation pipeline, the morph offset is computed as a triangle wave from the morph accumulator, then multiplied by the **Morph** amplitude and added to the base polygon radius. Any negative result is clamped to zero. The result is that each vertex independently breathes in and out, distorting the regular polygon into fluid, organic forms.

### Vertex computation pipeline

Vertex positions are recomputed once per frame during the vertical blanking interval. The computation runs as a five-phase state machine, processing one vertex every five clock cycles:

1. **Phase 0**: Compute the vertex's angle (base rotation + index × angular step) and the morph triangle wave offset. Set the sin/cos LUT address.
2. **Phase 1**: Multiply the morph offset by the morph amplitude (registered product).
3. **Phase 2**: Compute the effective radius (base size + scaled morph product, clamped to non-negative). Register the sin/cos LUT outputs.
4. **Phase 3**: Multiply cosine and sine by the effective radius (two parallel multiplications).
5. **Phase 4**: Shift and add the products to the screen center coordinates. Store the vertex position and advance to the next vertex.


---

## Signal Flow

### Signal Flow Notes

The rendering pipeline splits into two independent computation phases that run at different times. During the ***vertical blanking interval***, the vertex computation state machine processes all polygon vertices (three to six, depending on **Sides**), computing each vertex's screen position from the rotation angle, morph offset, and radius. This happens once per frame. At the start of each ***active scanline***, the span computation state machine processes each polygon edge serially, using iterative binary division to find where edges cross the current line. This narrows a span window to produce the final pixel range for the per-pixel inside/outside test.

The color generation stage downstream of the per-pixel test selects fill and background independently. When both **Fill Src** and **Background** are set to Video, the polygon acts as a luminance mask: the polygon's interior shows video at full brightness while the background also shows video, creating a geometric highlight or stencil effect rather than a cutout.

:::note
The vertex computation pipeline takes five clock cycles per vertex, so a hexagon requires thirty clocks. At 74.25 MHz, this completes well within the vertical blanking interval. The span computation processes edges serially during horizontal blanking: approximately fourteen clocks per edge: and a hexagon's six edges are fully evaluated before the first active pixel arrives.
:::


---

## Exercises

These exercises explore Geode's core shape-synthesis capabilities, from static geometric forms to animated crystal shapes composited with live video.
### Exercise 1: Crystal Formation

![Crystal Formation result](/img/instruments/videomancer/geode/geode_ex1_s1.png)
*Crystal Formation — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A stationary series of geometric shapes of increasing complexity, learning how **Sides**, **Size**, and **Hue** interact.

#### Key Concepts

- Polygon vertex count changes the fundamental character of the shape
- Size scales the shape from a point to full-frame
- Hue sweeps through four discrete color zones

#### Steps

1. Set **Sides** (Knob 1) fully counterclockwise to select a triangle. A bright white triangle appears centered on a black background.
2. Slowly increase **Size** (Knob 2) from zero to full. Watch the triangle expand from a point to fill the frame.
3. Step through the **Sides** control, pausing at each position: triangle, square, pentagon, hexagon. Notice how higher vertex counts make the shape approach a circle.
4. Set **Hue** (Knob 6) to about 50%. The fill changes from white to a cool-tinted color. Sweep the knob slowly from 0% to 100% to see all four hue zones: neutral white, warm cyan, cool magenta, and golden amber.

#### Settings

| Control | Value |
|---------|-------|
| Sides | Vary (3 to 6) |
| Size | 75% |
| Rotation | 0% |
| Morph | 0% |
| Edge Glow | 0% |
| Hue | 50% |
| Fill Src | Color |
| Draw Mode | Filled |
| Double | Off |
| Background | Black |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Living Geometry

![Living Geometry result](/img/instruments/videomancer/geode/geode_ex2_s1.png)
*Living Geometry — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated morphing polygon that breathes and rotates, exploring the interplay between uniform rotation and per-vertex distortion.

#### Key Concepts

- Rotation uses DDS accumulation for smooth, continuous animation
- Morph applies per-vertex radial oscillation at independent phases
- The combination of rotation and morph creates organic, crystal-like motion

#### Steps

1. Start with a hexagon at moderate size (**Sides** fully clockwise, **Size** ~60%).
2. Slowly turn **Rotation** (Knob 3) clockwise. The hexagon begins to spin. Find a slow, hypnotic speed around 20–30%.
3. Now increase **Morph** (Knob 4) from zero. The vertices start pulsing independently. At low values, the hexagon wobbles gently. At high values, vertices extend far beyond the base radius, creating a star or flower shape.
4. Try different **Sides** settings with active morph. A morphing triangle creates a three-pointed star. A morphing square creates a pinwheel. A morphing hexagon resembles a sea anemone.
5. Set **Hue** (Knob 6) to sweep through the four color zones while the shape animates. The color shifts give each frame of the animation a different character.

#### Settings

| Control | Value |
|---------|-------|
| Sides | 6 (fully CW) |
| Size | 60% |
| Rotation | 25% |
| Morph | 60% |
| Edge Glow | 25% |
| Hue | 75% |
| Fill Src | Color |
| Draw Mode | Filled |
| Double | Off |
| Background | Black |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Video Stencil

![Video Stencil result](/img/instruments/videomancer/geode/geode_ex3_s1.png)
*Video Stencil — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A rotating polygon window that reveals the input video inside its boundaries, composited over either a black void or the same video as background (a geometric stencil effect.)

#### Key Concepts

- The polygon can act as a shaped window into the input video
- Background and fill source can both use video independently
- Mix blends the synthesized output with the dry input signal

#### Steps

1. Connect a video input with recognizable content (a camera feed, pattern, or video loop.)
2. Set **Fill Src** (Switch 7) to **Video**. The polygon is now filled with the input video instead of a solid color.
3. Leave **Background** (Switch 10) on **Black**. The polygon acts as a window: the video image is visible only within the polygon's boundaries, floating on a black void.
4. Now set **Background** to **Video**. Both inside and outside the polygon show video. The polygon becomes a stencil (a subtle geometric highlight on the full-frame video.)
5. Lower the **Mix** fader (Fader 12) to about 50%. The polygon blends with the raw input, creating a ghostly overlay effect.
6. Enable rotation (~15%) and morph (~30%). The spinning, breathing polygon sweeps across the video content like a living magnifying lens.

#### Settings

| Control | Value |
|---------|-------|
| Sides | 5 |
| Size | 50% |
| Rotation | 15% |
| Morph | 30% |
| Edge Glow | 0% |
| Hue | 50% |
| Fill Src | Video |
| Draw Mode | Filled |
| Double | Off |
| Background | Video |
| Bypass | Off |
| Mix | 75% |

---
## Glossary

- **Convex Polygon**: A polygon where all interior angles are less than 180°; any line segment between two interior points stays inside the shape.

- **DDS (Direct Digital Synthesis)**: A technique for generating periodic waveforms by incrementing a phase accumulator at a fixed rate and using the accumulated value to index a lookup table or drive an output.

- **Morph**: In Geode, a radial oscillation applied independently to each vertex, creating organic deformations of the polygon shape.

- **Rasterization**: The process of converting vector geometry (points, lines, polygons) into discrete pixel values for display.

- **Scanline Rendering**: A rendering technique that processes an image one horizontal line at a time, computing which shapes are visible on each line.

- **Sin/Cos LUT**: A lookup table storing precomputed sine and cosine values, allowing the FPGA to compute positions on a circle without trigonometric hardware.

- **Span**: In scanline rendering, the horizontal range of pixels on a given line that fall inside a polygon.

- **Synthesis Program**: A Videomancer program that generates imagery from scratch rather than processing an input video signal.

- **Triangle Wave**: A periodic waveform that rises and falls linearly, used in Geode for the vertex morph oscillation.

- **Vertex**: A corner point of a polygon; Geode computes vertex positions from angle and radius using a sin/cos lookup table.

---
