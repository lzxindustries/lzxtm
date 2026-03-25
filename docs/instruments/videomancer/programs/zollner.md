---
draft: true
sidebar_position: 342
slug: /instruments/videomancer/zollner
title: "Zollner"
image: /img/instruments/videomancer/zollner/zollner_hero_s1.png
description: "The Zöllner illusion is one of the oldest documented optical illusions — discovered in 1860 by astrophysicist Johann Karl Friedrich Zöllner when he noticed that parallel lines on a piece of fabric appeared to converge when crossed by short diagonal hash marks."
---

![Zollner hero image](/img/instruments/videomancer/zollner/zollner_hero_s1.png)
*Zollner overlaying alternating hatch-mark bands onto a video signal, bending straight lines into curves through the power of optical illusion.*

---

## Overview

Zollner is a real-time optical illusion generator that overlays geometric patterns onto live video. Its core trick is deceptively simple: draw parallel bands across the screen and fill them with short, angled hatch marks that alternate direction from band to band. The result is the classic Zöllner illusion: objectively parallel lines that appear to converge, diverge, or wobble depending on the hatch angle. The effect is immediate and visceral, turning any video source into a perceptual puzzle.

Beyond the classic Zöllner pattern, the program offers three additional illusion variants. The Hering illusion bends parallel lines outward from a central vanishing point, the Wundt illusion curves them inward, and the Café Wall illusion uses offset checkerboard tiles to make horizontal mortar lines appear sloped. Each variant exploits a different flaw in human spatial perception, and all four run in real time at video rate.

The overlay composites onto the input by darkening the video wherever the pattern is drawn. At low opacity the pattern is a subtle texture; at high opacity it dominates the frame. An optional animation mode scrolls the band structure vertically, creating a hypnotic rolling-shutter effect that continuously refreshes the illusion.

:::tip
Zollner is a ***processing*** program: it transforms an incoming video signal. Feed it something with strong horizontal or vertical lines and watch those lines appear to bend and twist under the illusion overlay.
:::

### What's In a Name?

The ***Zöllner illusion*** was discovered in 1860 by the German astrophysicist Johann Karl Friedrich Zöllner. While examining a piece of fabric with an oblique line pattern, he noticed that parallel lines appeared to converge and diverge. He published his observation, and it became one of the most studied geometric optical illusions in perceptual psychology. The name ***Zollner*** (without the umlaut) is the program's nod to that original discovery: a fitting title for a tool that weaponizes human perception against itself.

---

## Quick Start

1. Send a video signal into Videomancer and load the **Zollner** program. You'll see evenly spaced horizontal bands overlaid on your video, with short diagonal hatch marks inside each band.
2. Turn **Hatch Ang** (Knob 2) slowly clockwise. Watch the hatch marks tilt to steeper angles: and notice how the horizontal band edges seem to tilt along with them, even though they haven't moved at all.
3. Adjust **Band W** (Knob 1) to change the spacing between bands. Wider bands make the illusion more dramatic; narrower bands create a denser, more textured overlay.
4. Increase **Opacity** (Knob 4) until the pattern is prominently visible against your video. Now flip the **Pattern** toggle (Switch 7) to **Café** to see the Café Wall illusion: the straight mortar lines between tiles appear to slope in alternating directions.

---

## Parameters

![Videomancer front panel with Zollner loaded](/img/instruments/videomancer/zollner/zollner_control_panel.png)
*Videomancer's front panel with Zollner active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Band W

| Property | Value |
|----------|-------|
| Range | 8 – 64 |
| Default | 29 |

**Band W** sets the width of each repeating band in the overlay pattern. The control steps through eight discrete sizes: 8, 12, 16, 20, 24, 32, 48, and 64 pixels. At the smallest setting the screen fills with many thin bands, producing a dense, fine-grained illusion. At the largest setting, a handful of wide bands stretch across the frame, giving the hatch marks more room to develop their diagonal sweep. Wider bands generally produce a stronger illusion because the eye has more space to misjudge the angle of the band edges.

:::note
Because **Band W** uses discrete steps rather than a smooth sweep, you'll hear (and see) the pattern jump between sizes as you turn the knob. This is by design: each step maps to a specific pixel count optimized for clean modular arithmetic in the FPGA.
:::

---

### Knob 2 — Hatch Ang

| Property | Value |
|----------|-------|
| Range | 0° – 90° |
| Default | 45° |

**Hatch Ang** controls the diagonal angle of the hatch marks within each band. At the center position (45°), the marks are tilted at a moderate angle. Turning fully counterclockwise flattens them to nearly horizontal; turning fully clockwise steepens them toward vertical. The illusion's strength depends heavily on this angle: moderate angles (around 20° to 40°) tend to produce the most convincing perceptual distortion, while very shallow or very steep angles weaken the effect.

In the Zöllner and Café Wall modes, the hatch angle alternates direction between adjacent bands, which is the mechanism that creates the illusion of convergence and divergence. In the Hering and Wundt modes, the angle parameter instead controls how strongly the radial fan lines curve outward or inward from the screen center.

---

### Knob 3 — Hatch Sp

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Hatch Sp** controls the spacing between individual hatch marks along each band. At 0%, the marks are packed tightly together, creating a nearly solid diagonal fill. As the value increases, gaps open up between the marks, producing a dotted or dashed appearance. At 100%, the marks are widely separated. Tighter spacing creates a stronger illusion because the eye perceives a continuous diagonal line rather than individual marks.

---

### Knob 4 — Opacity

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Opacity** sets the strength of the overlay composite. The pattern darkens the video wherever a hatch mark or band edge is drawn. At 0%, no darkening occurs and the pattern is invisible. At 100%, the pattern area is driven to full black. Moderate values (around 50% to 75%) let the pattern sit visibly on top of the video while preserving the underlying image content.

:::tip
For a subtle, almost subliminal effect, keep **Opacity** low (around 20% to 30%). The illusion still works: parallel lines in the source video will appear to bend: but the overlay itself fades into the background.
:::

---

### Knob 5 — Anim Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Anim Speed** controls the rate of the vertical scroll animation when animation is enabled via the **Animate** toggle (Switch 9). At 0% the pattern is stationary. As the value increases, the entire band structure scrolls upward at increasing speed, continuously refreshing the illusion across the frame. The scroll advances once per video field, so the motion is inherently synchronized to the video refresh rate.

When **Animate** is set to **Off**, this control has no effect.

---

### Knob 6 — Hatch Len

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Hatch Len** sets the ***duty cycle*** of each hatch mark: the proportion of each hatch period that is filled versus empty. At 0%, the marks are as short as possible (just a single pixel wide). At 100%, each mark fills its entire period, creating a continuous solid line with no gaps. This parameter interacts closely with **Hatch Sp** (Knob 3): spacing sets the period between marks, while length sets how much of that period is drawn.

---

### Switch 7 — Pattern

| Property | Value |
|----------|-------|
| Off | Zöllner |
| On | Café |
| Default | Zöllner |

**Pattern** selects the primary illusion variant. In the **Zöllner** position, the overlay draws parallel horizontal bands with alternating-angle hatch marks: the classic Zöllner illusion. Straight band edges appear to tilt and converge. In the **Café** position, the program switches to a different geometric arrangement.

:::note
The **Pattern** and **Hatch Style** toggles work together as a combined mode selector. See the Toggle Group Notes section below for the full four-mode breakdown.
:::

---

### Switch 8 — Hatch Style

| Property | Value |
|----------|-------|
| Off | Thin |
| On | Thick |
| Default | Thin |

**Hatch Style** selects the secondary illusion variant. In the **Thin** position, the hatch geometry uses its default line weight. In the **Thick** position, the pattern changes to a different geometric variant.

Because **Hatch Style** interacts with **Pattern** (Switch 7) to select among four illusion modes, its visual effect depends on the position of both toggles. See Toggle Group Notes below.

---

### Switch 9 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Animate** enables or disables the vertical scroll animation. When set to **On**, the band structure scrolls upward at the rate set by **Anim Speed** (Knob 5), creating a continuously rolling illusion. When set to **Off**, the pattern is locked to screen coordinates and remains stationary.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** reverses the overlay polarity. When set to **Off**, the hatch marks and band edges darken the video (the pattern is drawn as dark lines on lighter video). When set to **On**, the logic inverts: everything *outside* the pattern is darkened, leaving the hatch marks and band edges as bright windows into the original video. This effectively swaps figure and ground, creating a photographic-negative version of the illusion.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the input signal directly to the output, skipping all Zollner processing. The sync delay pipeline still maintains timing alignment, so toggling bypass produces no glitch. Use this for instant A/B comparison between the raw input and the processed result.

---

:::note Toggle Group Notes

The **Pattern** (Switch 7) and **Hatch Style** (Switch 8) toggles form a combined two-bit mode selector, giving access to four distinct optical illusion variants:

| Pattern | Hatch Style | Illusion Mode | Description |
|---------|-------------|---------------|-------------|
| Zöllner | Thin | **Zöllner** | Parallel horizontal bands with alternating-angle hatch marks. Band edges appear to converge and diverge. |
| Café | Thin | **Hering** | Radial fan lines extending outward from the screen center. Parallel lines appear to bow outward. |
| Zöllner | Thick | **Wundt** | Inverse radial fan lines curving inward toward the screen center. Parallel lines appear to bow inward. |
| Café | Thick | **Café Wall** | Offset checkerboard tiles with thin mortar lines between them. The horizontal mortar lines appear to slope in alternating directions. |

:::tip
The Hering and Wundt illusions use a ***radial coordinate system*** centered at the middle of the screen. **Hatch Ang** controls the curvature of the fan lines rather than a simple diagonal slope. The Café Wall mode ignores hatch marks entirely and instead shifts alternating tile rows by half a band width to produce the characteristic staggered-brick pattern.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (Zollner-processed) output. At 0%, only the dry signal passes through, equivalent to a full bypass. At 100%, the fully processed output is heard. Intermediate values blend the two, softening the overlay effect. The crossfade uses three interpolator instances (one each for Y, U, and V) to produce a smooth, artifact-free transition.

---

## Background

### Geometric optical illusions

Geometric optical illusions exploit the way the human visual system interprets angles, lines, and spatial relationships. When short oblique lines cross longer parallel lines, the brain misjudges the orientation of the parallels: this is the Zöllner effect. The distortion arises not in the eye itself, but in the neural processing that estimates line orientation. Lateral inhibition between orientation-selective neurons in the visual cortex causes neighboring angles to repel each other perceptually, making parallel lines appear to tilt away from the crossing hatch marks.

The four illusions in this program: Zöllner, Hering, Wundt, and Café Wall: are all variations on this basic mechanism. They differ in geometry (parallel bands vs. radial fans vs. offset tiles) but share the same perceptual root: local angular context distorts the perceived orientation of longer structures.

### Real-time overlay compositing

Unlike synthesis programs that generate imagery from scratch, Zollner overlays a computed pattern onto an existing video signal. The overlay uses a simple multiplicative composite: where the pattern is "on," the video luminance is scaled down by an amount set by the **Opacity** control. Chrominance (U and V) passes through unchanged in the affected regions, so the overlay darkens without desaturating. This produces a shadow-like effect where the pattern appears stamped onto the video.

### Animation and temporal illusions

The scroll animation adds a temporal dimension to the illusion. As the band structure moves vertically across the frame, stationary features in the source video interact with the moving pattern to create ***moiré*** effects and apparent motion. Diagonal elements in the video appear to bend and flex as the hatch marks sweep past them. The animation rate is frame-locked (advancing once per vsync), ensuring smooth, jitter-free scrolling regardless of the video format.


---

## Signal Flow

### Signal Flow Notes

The pipeline is eight clocks deep: four stages of pattern generation and compositing, followed by four clocks for the interpolator mix. The sync and data delay pipeline shifts the original input through an eight-stage register so that the dry signal arrives at the mix stage in perfect alignment with the processed signal.

Two key interactions dominate the signal flow. First, the band parity signal from Stage 1 controls whether the hatch slope is added or subtracted in Stage 2 (for Zöllner mode), or whether the radial coordinate sign flips (for Hering/Wundt modes). This alternation is the entire mechanism of the illusion: without it, all bands would have identical hatching and no perceptual distortion would occur. Second, the opacity composite in Stage 3 is purely multiplicative on the Y channel; U and V pass through unmodified. This means the overlay darkens without shifting color, producing clean shadow-like marks rather than colored tints.

:::note
The Café Wall mode bypasses the hatch-angle machinery entirely. Instead of computing diagonal slopes, it shifts the horizontal coordinate by half a band width on alternate bands, creating the offset-tile geometry characteristic of the Café Wall illusion.
:::


---

## Exercises

These exercises progress from the classic Zöllner illusion through the four pattern modes, building up to animated compositions.
### Exercise 1: The Classic Zöllner

![The Classic Zöllner result](/img/instruments/videomancer/zollner/zollner_ex1_s1.png)
*The Classic Zöllner — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic Zöllner illusion overlay where parallel horizontal bands appear to converge and diverge across your video.

#### Key Concepts

- Alternating hatch angles create the perception of non-parallel lines
- Hatch angle and band width control the illusion strength
- Opacity controls how visibly the pattern sits on the video

#### Video Source

A live camera feed or footage with strong horizontal lines: bookshelves, window blinds, or brick walls work especially well because the illusion bends them visually.

#### Steps

1. Load the **Zollner** program with all settings at default. You should see horizontal bands with angled hatch marks overlaid on the video.
2. Turn **Hatch Ang** (Knob 2) until the hatch marks are at roughly a 30° angle. Look at the band edges: they should appear to tilt even though they're perfectly horizontal.
3. Adjust **Band W** (Knob 1) to find the most convincing illusion. Wider bands (32 or 48 pixels) often produce the strongest effect.
4. Increase **Opacity** (Knob 4) to about 75% so the pattern is clearly visible against the source video.
5. Try different **Hatch Sp** (Knob 3) settings. Tighter spacing strengthens the illusion; wider spacing creates a more open, dotted pattern.

#### Settings

| Control | Value |
|---------|-------|
| Band W | 32 px |
| Hatch Ang | ~30° |
| Hatch Sp | 50.0% |
| Opacity | 75.0% |
| Anim Speed | 0.0% |
| Hatch Len | 50.0% |
| Pattern | Zöllner |
| Hatch Style | Thin |
| Animate | Off |
| Invert | Off |
| Bypass | Off |
| Mix | 100.0% |

---

### Exercise 2: Four Illusions Tour

![Four Illusions Tour result](/img/instruments/videomancer/zollner/zollner_ex2_s1.png)
*Four Illusions Tour — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A guided tour through all four illusion modes: Zöllner, Hering, Wundt, and Café Wall: using the same source video for comparison.

#### Key Concepts

- Two toggles combine to select four illusion variants
- Each variant exploits a different spatial-perception mechanism
- The same hatch angle parameter has different visual meaning in each mode

#### Video Source

Footage with a grid pattern or geometric composition: tiled floors, graph paper, or a test pattern with parallel lines in both axes.

#### Steps

1. Start with **Pattern** = **Zöllner** and **Hatch Style** = **Thin** (both switches in their default position). This is the classic Zöllner mode. Set **Hatch Ang** to about 45° and **Opacity** to about 60%. Note how the horizontal band edges appear to tilt.
2. Flip **Pattern** to **Café** while leaving **Hatch Style** on **Thin**. The pattern changes to the Hering illusion: radial fan lines curve outward from the center of the screen. Horizontal lines in the video appear to bow outward.
3. Now flip **Hatch Style** to **Thick** while keeping **Pattern** on **Café**. This activates the Café Wall illusion: offset checkerboard tiles with mortar lines that appear to slope. Adjust **Band W** to a larger width (48 or 64) for the best effect.
4. Finally, set **Pattern** back to **Zöllner** while leaving **Hatch Style** on **Thick**. This activates the Wundt illusion: the inverse of Hering, with fan lines curving inward. Horizontal lines bow inward rather than outward.
5. Toggle **Invert** (Switch 10) in each mode. Notice how inverting swaps figure and ground, changing the character of each illusion.

#### Settings

| Control | Value |
|---------|-------|
| Band W | 48 px |
| Hatch Ang | 45° |
| Hatch Sp | 50.0% |
| Opacity | 60.0% |
| Anim Speed | 0.0% |
| Hatch Len | 50.0% |
| Pattern | (varies) |
| Hatch Style | (varies) |
| Animate | Off |
| Invert | Off |
| Bypass | Off |
| Mix | 100.0% |

---

### Exercise 3: Animated Scroll

![Animated Scroll result](/img/instruments/videomancer/zollner/zollner_ex3_s1.png)
*Animated Scroll — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A continuously scrolling illusion overlay that creates hypnotic moiré interactions with the source video.

#### Key Concepts

- Animation adds temporal interaction between the pattern and the video content
- Scrolling hatch bands create moiré effects with stationary video features
- Invert mode and animation combine for a stroboscopic quality

#### Video Source

High-contrast footage with repeating structures: fences, venetian blinds, striped fabric, or architectural patterns with strong vertical or horizontal lines.

#### Steps

1. Set **Pattern** to **Zöllner**, **Hatch Style** to **Thin**, and **Band W** to 24 pixels for a moderately dense pattern.
2. Flip **Animate** (Switch 9) to **On**. Nothing moves yet because **Anim Speed** is at its default value.
3. Increase **Anim Speed** (Knob 5) slowly. The band structure begins to scroll upward. As it moves, watch for ***moiré*** interference patterns where the scrolling hatch marks interact with stationary lines in the video.
4. Set **Opacity** high (around 80%) and **Hatch Ang** to a moderate angle (30° to 40°). The scrolling diagonal marks should create strong visual beats against the source.
5. Toggle **Invert** (Switch 10) to **On**. The moving pattern becomes a set of bright slits through a darkened frame, producing a stroboscopic scanning effect.
6. Experiment with **Mix** (Fader 12) to blend the animated overlay with the dry signal at various strengths.

#### Settings

| Control | Value |
|---------|-------|
| Band W | 24 px |
| Hatch Ang | ~35° |
| Hatch Sp | 40.0% |
| Opacity | 80.0% |
| Anim Speed | 40.0% |
| Hatch Len | 50.0% |
| Pattern | Zöllner |
| Hatch Style | Thin |
| Animate | On |
| Invert | On |
| Bypass | Off |
| Mix | 100.0% |

---
## Glossary

- **Café Wall Illusion**: An optical illusion in which alternating rows of dark and light tiles, offset by half a tile width, make the horizontal mortar lines between rows appear to slope.

- **Composite**: The process of combining two image layers: here, an overlay pattern and the input video: into a single output by multiplicative blending.

- **Duty Cycle**: The fraction of a repeating period that is "on" versus "off"; in Zollner, it controls how much of each hatch period is filled by a visible mark.

- **Hatch Mark**: A short diagonal line drawn within a band; the alternating direction of hatch marks across adjacent bands is the mechanism behind the Zöllner illusion.

- **Hering Illusion**: An optical illusion in which two parallel straight lines appear to bow outward when overlaid with a pattern of radial lines emanating from a central point.

- **Interpolator**: A hardware module that computes a weighted blend between two values; used here for the wet/dry mix crossfade.

- **Moiré**: An interference pattern created when two regular patterns (such as scrolling hatch marks and stationary video lines) overlap at slightly different frequencies or angles.

- **Opacity**: The strength of the overlay effect; higher opacity produces stronger darkening where the pattern is drawn.

- **Wundt Illusion**: The inverse of the Hering illusion: parallel lines appear to bow inward when crossed by inward-curving radial lines.

- **Zöllner Illusion**: A geometric optical illusion in which parallel lines appear tilted due to the influence of short crossing lines at alternating angles.

---
