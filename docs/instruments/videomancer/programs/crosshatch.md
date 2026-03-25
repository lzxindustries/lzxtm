---
draft: true
sidebar_position: 70
slug: /instruments/videomancer/crosshatch
title: "Crosshatch"
image: /img/instruments/videomancer/crosshatch/crosshatch_hero_s1.png
description: "Every illustrator and printmaker who has worked without continuous tone knows the challenge: reproduce the full range of light and shadow using only marks and blank surface."
---

![Crosshatch hero image](/img/instruments/videomancer/crosshatch/crosshatch_hero_s1.png)
*Crosshatch overlaying intersecting diagonal and perpendicular stroke layers on a tinted wash, blended with the input video for a hand-drawn ink-on-paper effect.*

---

## Overview

**Crosshatch** turns your video into an ink drawing. It renders a pattern of evenly spaced lines: diagonal, horizontal, and vertical: over a colored background, then blends the result with your original video signal. The line spacing, thickness, brightness, and direction are all independently adjustable, giving you full control over every aspect of the hatching pattern. Think of it as a digital engraving press running in real time on live video.

At subtle settings, Crosshatch adds a delicate web of fine lines over the image, like a pencil sketch drawn on translucent vellum laid over the screen. At extreme settings, it replaces the video entirely with a bold geometric grid of stark lines on a colored field: pure constructivist graphics generated from nothing but pixel-position arithmetic. Between these extremes lies a rich territory of pen-and-ink illustration, copperplate engraving, and technical drawing aesthetics. Use the **Mix** fader to dial in exactly how much of the original video shows through the hatch.

:::tip
The classic cross-hatch look comes from combining the **Style** and **Cross** switches together. Set both to their active positions and the diamond grid appears (then use **Mix** to overlay it on your source video.)
:::

### What's In a Name?

***Cross-hatching*** is one of the oldest shading techniques in drawing and printmaking. An artist lays down a first set of parallel lines and then draws a second set crossing at an angle. Where the lines overlap, tonality deepens. Closely spaced strokes appear dark; widely spaced strokes appear light. Renaissance engravers like Albrecht Dürer mastered this technique to render astonishing depth and detail using nothing but intersecting lines on metal plates. Videomancer's **Crosshatch** brings the technique into the electronic domain, generating its line patterns in real time from bitwise arithmetic on pixel counters.

---

## Quick Start

1. Set **Style** (Switch 7) to **Etch** and **Cross** (Switch 8) to **Cross**. A diamond grid of intersecting diagonal lines fills the screen instantly.
2. Turn **Stroke W** (Knob 1) counterclockwise to tighten the spacing. The diamond pattern becomes finer and denser as the hatching period shrinks.
3. Lower **Mix** (Fader 12) to about halfway. The original video reappears through the gaps in the hatch lines, giving your image a hand-sketched quality (ink strokes laid over living video.)

---

## Parameters

![Videomancer front panel with Crosshatch loaded](/img/instruments/videomancer/crosshatch/crosshatch_control_panel.png)
*Videomancer's front panel with Crosshatch active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Stroke W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Stroke W** controls the spacing period of the hatch lines. At minimum, lines are packed tightly together with a period of just eight pixels, creating a dense weave of fine strokes. As you turn the knob clockwise, the period doubles in discrete steps: 16, 32, 64, 128, and finally 256 pixels: spreading the lines farther apart. At maximum, the hatch pattern becomes a sparse grid of widely separated strokes with large open areas between them.

:::note
The spacing steps in powers of two, so the visual jumps between levels become more dramatic as the knob increases. Fine control over line density is concentrated in the lower range of the knob.
:::

---

### Knob 2 — Density

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Density** controls the brightness of the hatch lines themselves. At minimum, the lines are black: dense, dark ink strokes that stand out sharply against a lighter background. At maximum, the lines are white, reading as bright marks or highlights. At the midpoint, the lines are neutral gray. The hatch lines are always achromatic regardless of the background color settings, so this control adjusts only their luminance.

---

### Knob 3 — Angle

| Property | Value |
|----------|-------|
| Range | 0° – 90° |
| Default | 45° |

**Angle** controls the brightness of the background fill: the "paper" behind the hatch lines. At minimum, the background is black, and the lines float on darkness. At maximum, the background is fully bright. Combined with the line brightness set by **Density** (Knob 2), you can create dark lines on a bright field (the classic ink-on-paper look), bright lines on a dark field (a chalkboard sketch), or any combination. This control works together with **Levels** (Knob 4) and **Ink Tint** (Knob 5) to define the full color of the background.

---

### Knob 4 — Levels

| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 5 |

**Levels** adjusts the blue-difference chroma axis of the background color. At one extreme, the background shifts toward blue. At the other, it shifts toward yellow. At the middle step, the background chroma is roughly neutral on this axis. This control combines with **Ink Tint** (Knob 5) to set the overall hue and saturation of the paper behind the hatch lines.

---

### Knob 5 — Ink Tint

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Ink Tint** adjusts the red-difference chroma axis of the background color. Combined with **Levels** (Knob 4), these two controls together set the hue and saturation of the paper. **Angle** (Knob 3) sets the paper brightness, while Levels and Ink Tint define its two chroma components. For a neutral gray background, set both chroma controls near their center positions.

:::tip
To create a warm parchment background, set **Angle** to a medium-high value, then nudge **Levels** and **Ink Tint** slightly off center. Small deviations from neutral produce convincing tinted paper. Large offsets produce vivid, poster-like color fields.
:::

---

### Knob 6 — Paper Tint

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Paper Tint** controls the thickness of the hatch lines. At minimum, each hatch line is a crisp single-pixel stroke: the thinnest possible mark. As you increase this control, the lines become progressively thicker in discrete steps: first two pixels wide, then four, then eight. Thicker lines fill more of the frame, creating a heavier, bolder hatching pattern. At maximum, the thick bands can dominate the visual field, leaving only narrow slivers of background color visible.

---

### Switch 7 — Style

| Property | Value |
|----------|-------|
| Off | Pen |
| On | Etch |
| Default | Pen |

**Style** selects between two stroke modes. In the **Pen** position, 45° diagonal lines are disabled, producing a cleaner composition limited to horizontal and vertical strokes (if those directions are enabled by other switches). In the **Etch** position, 45° diagonal lines are activated, adding the characteristic angled scratches of an etching or engraving. Combining Etch with the **Cross** switch (Switch 8) creates classical cross-hatching with two intersecting diagonal directions.

---

### Switch 8 — Cross

| Property | Value |
|----------|-------|
| Off | Single |
| On | Cross |
| Default | Single |

**Cross** controls whether a second set of diagonal lines crosses the first. In the **Single** position, only the primary 45° direction is available (when **Style** is set to Etch). In the **Cross** position, a second set of 135° diagonal lines is added perpendicular to the first, forming an intersecting diamond pattern. This is the core of the cross-hatching effect (a single set of parallels becomes a woven lattice.)

---

### Switch 9 — Color Ink

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color Ink** enables horizontal lines in the hatch pattern. When set to **Off**, no horizontal strokes appear. When set to **On**, horizontal lines are rendered at the same spacing and thickness as all other active line directions. Adding horizontal strokes increases the density and visual weight of the overall pattern. Combined with vertical lines (via **Invert**, Switch 10), you get a rectilinear grid on top of any active diagonal hatching.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** enables vertical lines in the hatch pattern. When set to **Off**, no vertical strokes appear. When set to **On**, vertical lines are rendered alongside any other active directions. Combining vertical with horizontal lines creates a rectangular grid. Adding diagonals on top of that produces a dense multi-directional mesh where lines cross at four different angles.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all hatch rendering and mixing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw video and the hatched result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original video and the hatch composite. At minimum, the output is the unaltered source video: no hatching is visible. At maximum, the output is entirely the hatch pattern on its tinted background, with no source video showing through. At intermediate values, the hatch lines overlay the video with varying degrees of transparency, creating the effect of a drawing on translucent paper laid over a moving image.

:::tip
Try setting **Mix** to roughly 50% with dark hatch lines and a transparent background (**Angle** at minimum). The dark strokes appear to be drawn directly onto the video, with no visible "paper" between them.
:::

---

## Background

### Cross-hatching in art

Cross-hatching has been a fundamental drawing and printmaking technique since the Renaissance. Engravers like Albrecht Dürer and Rembrandt incised parallel lines into metal plates with a ***burin***, a sharp cutting tool. Ink settles into the grooves during printing: a first layer of lines provides a base tone, and a second layer drawn at an angle deepens the shadows. Additional layers at different angles create progressively darker areas. The result is shading built entirely from line work, with no continuous tones or washes.

In traditional hatching, the artist controls perceived brightness by varying line spacing and thickness: closely packed, thick lines appear dark, while widely spaced, thin lines appear light. Crosshatch brings this principle into the electronic video domain, generating its intersecting line patterns in real time on every frame.

### Power-of-two bitmask detection

Crosshatch generates its line patterns without any division or modulus operations: an important consideration on the iCE40 FPGA, which has no hardware divider. Instead, it uses ***bitmask AND*** operations on pixel-position counters.

Each pixel position is tracked by a binary counter. To place lines at regular intervals, the program applies a bit mask and checks whether the result is zero. A mask of 7 (binary 00000111) catches every eighth pixel: any position whose lowest three bits are all zero falls on a line. A mask of 15 catches every sixteenth position, 31 catches every thirty-second, and so on doubling up to 255 for every 256th pixel. This power-of-two trick replaces a costly modulus operator with a single AND gate (a fraction of the logic.)

Line thickness is controlled by a second mask that ignores additional low bits. With the thickness mask set to 254 (binary 11111110), the lowest bit is disregarded, so both even and odd pixel positions near a line boundary match: effectively doubling the line width. Each additional ignored bit doubles the width again.

### Diagonal lines on a pixel grid

Detecting diagonal lines on a rectangular pixel grid requires an elegant mathematical trick. A 45° diagonal connects all pixels where the horizontal position plus the vertical position equals a constant: if you step one pixel right and one pixel down, the sum stays the same. By applying the spacing bitmask to the sum (h_count + v_count), the program detects pixels lying along 45° stripes without calculating a slope or running a line-drawing algorithm.

For 135° lines, the program uses the difference (h_count − v_count) instead of the sum. Horizontal lines test the vertical counter alone, and vertical lines test the horizontal counter alone. All four directions share the same spacing and thickness masks, so the entire multi-directional pattern stays uniform.

### Interpolation and wet/dry mixing

The final stage of the Crosshatch pipeline blends the hatch composite with the original video using three ***interpolator*** modules: one for each of the Y, U, and V channels. Each interpolator performs a linear crossfade: output = A + (B − A) × t, where A is the delayed original pixel, B is the hatch composite pixel, and t is the **Mix** fader value. At t = 0, the output equals the original video. At t = maximum, the output equals the hatch composite. Values in between produce a proportional blend, letting the artist lay the hatch pattern over the source at any opacity.


---

## Signal Flow

### Signal Flow Notes

The pipeline runs in four processing stages plus four interpolator clocks, totaling eight cycles of latency. All sync signals and the original YUV data are delayed through a matching eight-stage shift register to maintain alignment at the output.

The hatch detection is entirely ***position-based***: it depends only on pixel coordinates, not on the input video content. The input video enters the pipeline solely through the interpolator mix stage, where it is crossfaded with the hatch composite. This means the hatch pattern is geometrically identical regardless of the source video; only the degree of overlay changes with the **Mix** fader.

:::note
Hatch lines always use neutral chroma (U = 512, V = 512), so the lines themselves are always achromatic: gray, black, or white depending on the **Density** setting, but never colored. Color appears only in the background fill, controlled by **Levels** and **Ink Tint**. The **Color Ink** switch adds horizontal lines to the pattern; it does not add color to the lines.
:::


---

## Exercises

These exercises progress from a simple diagonal pattern to a full multi-directional overlay, building your understanding of how line directions, spacing, thickness, and background color interact with one another and with the source video.
### Exercise 1: Diamond Grid

![Diamond Grid result](/img/instruments/videomancer/crosshatch/crosshatch_ex1_s1.png)
*Diamond Grid — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic diamond cross-hatch overlay with dark strokes on a bright field, blended at half intensity over a live video source.

#### Key Concepts

- Two diagonal directions combine to form a diamond cross-hatch pattern
- Stroke spacing controls overall pattern density
- The Mix fader blends the hatch overlay with live video

#### Video Source

A camera feed or recorded footage with recognizable subjects and a range of tones (faces, architecture, or natural scenes work well.)

#### Steps

1. **Enable diagonals**: Set **Style** (Switch 7) to **Etch** and **Cross** (Switch 8) to **Cross**. A diamond grid of intersecting diagonal lines fills the screen.
2. **Darken the strokes**: Turn **Density** (Knob 2) fully counterclockwise. The lines become black, reading as ink strokes.
3. **Brighten the paper**: Turn **Angle** (Knob 3) clockwise to about 70°. The background lightens, producing dark lines on a bright field (a classic pen-on-paper look.)
4. **Tighten the spacing**: Turn **Stroke W** (Knob 1) counterclockwise to roughly 25%. The diamond pattern becomes finer as the line period decreases.
5. **Blend with video**: Lower **Mix** (Fader 12) to about 50%. The original video shows through the hatch pattern. The image looks as though a crosshatch drawing has been laid over the screen on translucent paper.

#### Settings

| Control | Value |
|---------|-------|
| Stroke W | ~25% |
| Density | 0% |
| Angle | ~70° |
| Levels | 4 |
| Ink Tint | ~180° |
| Paper Tint | 0° |
| Style | Etch |
| Cross | Cross |
| Color Ink | Off |
| Invert | Off |
| Bypass | Off |
| Mix | ~50% |

---

### Exercise 2: Copperplate Engraving

![Copperplate Engraving result](/img/instruments/videomancer/crosshatch/crosshatch_ex2_s1.png)
*Copperplate Engraving — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dense copperplate-style engraving with slightly thickened strokes on warm-tinted paper, overlaying the source video.

#### Key Concepts

- Adding horizontal and vertical lines increases pattern density
- Line thickness controls the visual weight of the hatching
- Tinted backgrounds create the illusion of aged paper or hand-toned prints

#### Video Source

Footage with strong contrast and clear outlines. Portraits and architectural subjects produce especially convincing engraving-style results.

#### Steps

1. **Full hatching**: Enable all four line directions: **Style** to **Etch**, **Cross** to **Cross**, **Color Ink** (Switch 9) to **On**, and **Invert** (Switch 10) to **On**. The screen fills with a tight mesh of diagonal, horizontal, and vertical lines.
2. **Fine spacing, heavier stroke**: Set **Stroke W** (Knob 1) low for close spacing. Increase **Paper Tint** (Knob 6) to about 100° to thicken the lines slightly. The mesh becomes visually heavier.
3. **Dark ink**: Turn **Density** (Knob 2) low for dark strokes against the background.
4. **Warm paper**: Set **Angle** (Knob 3) to about 55° for a medium background brightness. Nudge **Levels** (Knob 4) and **Ink Tint** (Knob 5) slightly off center to tint the background a warm tone (aim for a soft parchment color.)
5. **Dominant overlay**: Set **Mix** (Fader 12) to about 70%. The hatch dominates, but the video content is still visible beneath, showing through the gaps in the mesh.

#### Settings

| Control | Value |
|---------|-------|
| Stroke W | ~15% |
| Density | ~10% |
| Angle | ~55° |
| Levels | 6 |
| Ink Tint | ~200° |
| Paper Tint | ~100° |
| Style | Etch |
| Cross | Cross |
| Color Ink | On |
| Invert | On |
| Bypass | Off |
| Mix | ~70% |

---

### Exercise 3: Bold Constructivist Grid

![Bold Constructivist Grid result](/img/instruments/videomancer/crosshatch/crosshatch_ex3_s1.png)
*Bold Constructivist Grid — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A bold, heavy grid of thick perpendicular bars on a vivid colored background: pure geometric abstraction that reveals the source video when you lower the fader.

#### Key Concepts

- Horizontal and vertical lines without diagonals create a rectilinear grid
- Thick lines and wide spacing form bold geometric blocks
- At full Mix, the hatch pattern replaces the video entirely (then lower Mix to frame the source inside the grid)

#### Video Source

Any video input. At full Mix the source is not visible; it appears only when you lower the fader in the final step.

#### Steps

1. **Perpendicular grid**: Set **Style** (Switch 7) to **Pen** and **Cross** (Switch 8) to **Single** to disable diagonals. Enable **Color Ink** (Switch 9) and **Invert** (Switch 10) for horizontal and vertical lines only.
2. **Maximum thickness**: Turn **Paper Tint** (Knob 6) fully clockwise. The lines become thick bars that dominate the frame.
3. **Wide spacing**: Set **Stroke W** (Knob 1) to about 60%. The thick bars separate into a visible grid with colored background rectangles between them.
4. **Bright lines, colored ground**: Turn **Density** (Knob 2) to maximum for white lines. Set **Angle** (Knob 3) low for a dark background. Push **Levels** (Knob 4) and **Ink Tint** (Knob 5) to strong off-center positions for a vivid background color.
5. **Full replacement**: Set **Mix** (Fader 12) to 100%. The output is entirely the generated grid pattern (no source video.)
6. **Reveal the source**: Slowly lower **Mix**. The video reappears inside the colored rectangles, framed by the white grid lines like a stained-glass window.

#### Settings

| Control | Value |
|---------|-------|
| Stroke W | ~60% |
| Density | 100% |
| Angle | ~10° |
| Levels | 2 |
| Ink Tint | ~270° |
| Paper Tint | ~350° |
| Style | Pen |
| Cross | Single |
| Color Ink | On |
| Invert | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Bitmask**: A binary number used to select or ignore specific bits in another number; Crosshatch uses bitmasks to detect line positions without division

- **Chroma**: The color information in a video signal, encoded as U and V components in YUV color space

- **Cross-hatching**: A drawing and printmaking technique where intersecting sets of parallel lines create the illusion of shading and tone

- **Interpolator**: A module that blends two values by a fractional amount, used here for the wet/dry mix between the hatch pattern and the original video

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness

- **Pipeline**: A chain of processing stages where data moves forward one stage per clock cycle; Crosshatch has an eight-stage pipeline

- **Power of two**: A number produced by multiplying 2 by itself repeatedly (2, 4, 8, 16, 32...); used for efficient bitmask-based line spacing

---
