---
draft: true
sidebar_position: 203
slug: /instruments/videomancer/necker
title: "Necker"
image: /img/instruments/videomancer/necker/necker_hero_s1.png
description: "The Necker cube is one of the most iconic figures in visual perception — a wireframe drawing of a cube that appears to spontaneously flip between two valid three-dimensional interpretations."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import necker_control_panel from '/img/instruments/videomancer/necker/necker_control_panel.png';
import necker_source1_parrot from '/img/instruments/videomancer/necker/necker_source1_parrot.png';
import necker_source2_skull from '/img/instruments/videomancer/necker/necker_source2_skull.png';
import necker_source3_clouds from '/img/instruments/videomancer/necker/necker_source3_clouds.png';
import necker_source4_pattern from '/img/instruments/videomancer/necker/necker_source4_pattern.png';
import necker_source5_man from '/img/instruments/videomancer/necker/necker_source5_man.png';
import necker_source6_berries from '/img/instruments/videomancer/necker/necker_source6_berries.png';
import necker_hero_s1 from '/img/instruments/videomancer/necker/necker_hero_s1.png';
import necker_hero_s2 from '/img/instruments/videomancer/necker/necker_hero_s2.png';
import necker_hero_s3 from '/img/instruments/videomancer/necker/necker_hero_s3.png';
import necker_hero_s4 from '/img/instruments/videomancer/necker/necker_hero_s4.png';
import necker_hero_s5 from '/img/instruments/videomancer/necker/necker_hero_s5.png';
import necker_hero_s6 from '/img/instruments/videomancer/necker/necker_hero_s6.png';
import necker_ex1_s1 from '/img/instruments/videomancer/necker/necker_ex1_s1.png';
import necker_ex1_s2 from '/img/instruments/videomancer/necker/necker_ex1_s2.png';
import necker_ex1_s3 from '/img/instruments/videomancer/necker/necker_ex1_s3.png';
import necker_ex1_s4 from '/img/instruments/videomancer/necker/necker_ex1_s4.png';
import necker_ex1_s5 from '/img/instruments/videomancer/necker/necker_ex1_s5.png';
import necker_ex1_s6 from '/img/instruments/videomancer/necker/necker_ex1_s6.png';
import necker_ex2_s1 from '/img/instruments/videomancer/necker/necker_ex2_s1.png';
import necker_ex2_s2 from '/img/instruments/videomancer/necker/necker_ex2_s2.png';
import necker_ex2_s3 from '/img/instruments/videomancer/necker/necker_ex2_s3.png';
import necker_ex2_s4 from '/img/instruments/videomancer/necker/necker_ex2_s4.png';
import necker_ex2_s5 from '/img/instruments/videomancer/necker/necker_ex2_s5.png';
import necker_ex2_s6 from '/img/instruments/videomancer/necker/necker_ex2_s6.png';
import necker_ex3_s1 from '/img/instruments/videomancer/necker/necker_ex3_s1.png';
import necker_ex3_s2 from '/img/instruments/videomancer/necker/necker_ex3_s2.png';
import necker_ex3_s3 from '/img/instruments/videomancer/necker/necker_ex3_s3.png';
import necker_ex3_s4 from '/img/instruments/videomancer/necker/necker_ex3_s4.png';
import necker_ex3_s5 from '/img/instruments/videomancer/necker/necker_ex3_s5.png';
import necker_ex3_s6 from '/img/instruments/videomancer/necker/necker_ex3_s6.png';

# Necker

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: necker_source1_parrot, after: necker_hero_s1 },
    { label: "Skull", before: necker_source2_skull, after: necker_hero_s2 },
    { label: "Clouds", before: necker_source3_clouds, after: necker_hero_s3 },
    { label: "Pattern", before: necker_source4_pattern, after: necker_hero_s4 },
    { label: "Man", before: necker_source5_man, after: necker_hero_s5 },
    { label: "Berries", before: necker_source6_berries, after: necker_hero_s6 },
  ]}
/>
*Necker rendering a perspective-ambiguous wireframe cube with depth-offset back face and overlay compositing onto the video source.*

---

## Overview

The Necker cube is one of the most iconic figures in visual perception — a wireframe drawing of a cube that appears to spontaneously flip between two valid three-dimensional interpretations. First described by Swiss crystallographer Louis Albert Necker in 1832, the figure demonstrates that visual perception is not a passive readout of retinal data but an active, constructive process where the brain chooses between competing depth hypotheses.

This program renders a Necker-style wireframe directly in the video pipeline. Two axis-aligned squares — a front face and a back face offset diagonally by a depth parameter — are drawn as bright edges over either the incoming video signal or a dark background. The result is a classic ambiguous-depth figure that flickers between "seen from above-left" and "seen from below-right" interpretations. Edge brightness, thickness, and cube size are continuously adjustable.

Note that several controls declared in the parameter interface are reserved for future implementation: Rotation and Perspective are mapped to registers but have no effect on the rendering. The Fill and Color toggles are similarly unused — Color references an undeclared signal in the current VHDL and will not synthesize correctly. The Animate toggle enables a frame counter, but the counter is not yet connected to any transform. These controls are documented here for completeness but produce no visible change.

---

## Quick Start

1. **Depth offset controls the illusion**: The Necker flip is strongest when the depth offset is 20–40% of the face size. Too large and the two squares separate into obviously distinct shapes; too small and they merge.
2. **Dark background for pure geometry**: Disable Overlay for a clean wireframe rendering suitable for title cards, overlays, or abstract composition.
3. **Overlay for augmented reality**: Enable Overlay to composite the wireframe onto live video — the cube becomes a spatial reference frame overlaid on the real world.

---

## Background

### The Necker Cube Illusion

In 1832, Louis Albert Necker published a letter describing an unusual property of a rhomboid crystal drawing: the apparent orientation of the figure would spontaneously reverse as he studied it. This *bistable perception* — the brain alternating between two equally valid depth interpretations of an ambiguous 2D figure — became one of the foundational demonstrations of Gestalt psychology. The Necker cube is now a standard test stimulus in visual neuroscience, used to study the mechanisms of perceptual decision-making, attention, and top-down cognitive influence on vision.

### Wireframe Edge Detection via Absolute Distance

The VHDL implementation draws edges by computing the absolute distance of each pixel from each edge line and comparing against a width threshold. For an axis-aligned square with half-size `h`, the top edge is the set of pixels where `|cy + h| < line_width` and `cx` is within `[-h, +h]`. This is a purely combinational test — no line-drawing algorithm, no Bresenham iteration, no BRAM. Each pixel independently decides whether it lies on an edge, making the approach fully parallel and pipelineable.

### Depth Offset as Perspective Proxy

True perspective projection requires division (screen_x = x / z), which is expensive on the iCE40 FPGA. Instead, Necker approximates the depth effect by simply offsetting the back face by a fixed diagonal displacement — both the X and Y coordinates of the back square are shifted by `depth / 2`. This produces a parallel (axonometric) projection rather than a true perspective, but it is sufficient to create the bistable depth illusion. The depth parameter controls how far apart the two faces appear.

### Overlay Compositing

When the Overlay toggle is enabled, pixels that are not on any edge pass the incoming video signal through unchanged. The wireframe is drawn *on top of* the video content. When Overlay is disabled, non-edge pixels output a dark gray (Y = 64, U = V = 512), creating a classic white-lines-on-dark-background technical illustration look.


---

## Signal Flow

Pixel Position → Front Face Edges → Back Face Edges → ... → Sync Delay → Bypass

```
Input Video (YUV 4:4:4)
│
├── Pixel Position ─────────────────────────────────────────────
│   ├─ X counter (horizontal pixel, reset on hsync)
│   ├─ Y counter (vertical line, reset on vsync)
│   └─ Center offset: cx = x - 640, cy = y - 360
│
├── Front Face Edges ───────────────────────────────────────────
│   ├─ Top:    |cy + half| < line_w  AND  cx ∈ [-half, +half]
│   ├─ Bottom: |cy - half| < line_w  AND  cx ∈ [-half, +half]
│   ├─ Left:   |cx + half| < line_w  AND  cy ∈ [-half, +half]
│   └─ Right:  |cx - half| < line_w  AND  cy ∈ [-half, +half]
│
├── Back Face Edges (offset by depth/2 diagonally) ─────────────
│   ├─ dx = cx - depth_off, dy = cy - depth_off
│   ├─ Top:    |dy + half| < line_w  AND  dx ∈ [-half, +half]
│   ├─ Bottom: |dy - half| < line_w  AND  dx ∈ [-half, +half]
│   ├─ Left:   |dx + half| < line_w  AND  dx ∈ [-half, +half]
│   └─ Right:  |dx - half| < line_w  AND  dy ∈ [-half, +half]
│
├── Output Compose ─────────────────────────────────────────────
│   ├─ On edge: Y = brightness, U = V = 512 (achromatic)
│   └─ Off edge: overlay ? pass input : dark background (Y=64)
│
├── Interpolator Mix ───────────────────────────────────────────
│   └─ 4-clock wet/dry crossfade per channel
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-stage pipeline (hsync, vsync, field, Y/U/V bypass)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select delayed original or mixed signal
```

The wireframe consists of two independent axis-aligned squares sharing the same half-size parameter. The front face is centered at screen coordinates (640, 360) and the back face is centered at (640 + depth_off, 360 + depth_off), where `depth_off = depth_register / 2`. No connecting edges are drawn between the front and back faces — the Necker illusion relies on the overlapping squares alone to create the ambiguous depth cue.

Edge thickness is derived from the top 3 bits of the Line Width register plus 1, giving a range of 1 to 8 pixels. The edge test is purely combinational within the pipeline clock, so all 8 edge segments (4 front + 4 back) are evaluated simultaneously.

---

## Parameter Reference

<img src={necker_control_panel} alt="Videomancer front panel with Necker loaded"/>
*Videomancer's front panel with Necker active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Size sets the half-width of the cube's front and back faces. The full 10-bit register value is used directly as the half-size in pixel coordinates. At 0 the cube collapses to a point; at 1023 the faces extend well beyond the visible frame. Moderate values (300–500) produce a cube that fits comfortably within 1280×720 HD resolution.

---

#### Knob 2 — Line Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Line Width controls the thickness of the wireframe edges. The VHDL extracts the top 3 bits of the register and adds 1, yielding a thickness range of 1 to 8 pixels. Fine variations in the lower register bits have no effect — the control has 8 discrete thickness steps. Thicker edges produce a bolder, more graphic appearance; thin edges create a delicate technical-drawing look.

---

#### Knob 3 — Rotation
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Rotation is declared and mapped to a register but has no effect on the rendering in the current implementation. The control is reserved for future rotation transforms. Turning this knob produces no visible change.

---

#### Knob 4 — Perspective
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Perspective is declared and mapped to a register but is not connected to any processing logic. It is reserved for a future perspective projection feature. Turning this knob produces no visible change.

---

#### Knob 5 — Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Depth controls the diagonal offset between the front and back faces. The register value is divided by 2 (right-shifted by 1) to produce the offset in pixel coordinates. Both the X and Y positions of the back face shift by this amount, creating a diagonal displacement that simulates axonometric depth. At 0, both faces overlap perfectly (no depth cue). At maximum, the back face is offset by ~511 pixels diagonally.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Brightness sets the luminance of the wireframe edges. The full 10-bit register value is used directly as the Y channel output for any pixel on an edge. At 0, edges are black (invisible against a dark background). At 1023, edges are peak white. Intermediate values produce gray wireframes. Chroma for edges is always achromatic (U = V = 512).

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Color** | Mono | RGB |
| **9 — Fill** | Off | On |
| **10 — Overlay** | Off | On |
| **11 — Bypass** | Off | On |

Of the five toggles, only Overlay and Bypass produce visible results. Animate enables a frame counter that increments but is not connected to any rendering parameter. Color attempts to reference an undeclared signal and will cause a synthesis error. Fill is declared but unused. These reserved controls are included in the parameter interface for future expansion.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix controls the interpolator crossfade between the dry (delayed original) and wet (processed) signals. At 0 the output is entirely dry; at 1023 entirely wet. The crossfade operates on all three channels (Y, U, V) with 4-clock interpolator latency.





---

## Guided Exercises

These exercises progress from a simple wireframe to an overlay-composited Necker illusion, exploring how the visual system interprets the ambiguous depth figure.

### Exercise 1: Basic Wireframe

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: necker_source1_parrot, after: necker_ex1_s1 },
    { label: "Skull", before: necker_source2_skull, after: necker_ex1_s2 },
    { label: "Clouds", before: necker_source3_clouds, after: necker_ex1_s3 },
    { label: "Pattern", before: necker_source4_pattern, after: necker_ex1_s4 },
    { label: "Man", before: necker_source5_man, after: necker_ex1_s5 },
    { label: "Berries", before: necker_source6_berries, after: necker_ex1_s6 },
  ]}
/>
*Basic Wireframe — simulated result across source images.*
**Source**: Any stable video source or black/blank input.

**What You'll Create**: Render a visible wireframe cube and learn how Size, Line Width, and Depth interact.

1. Disable Overlay (dark background). Set Brightness to ~75% for visible white edges.
2. Set Size to ~50%. A medium-sized square pair should appear centered on screen.
3. Increase Depth from 0 upward. Watch the back face separate diagonally from the front face, creating the classic Necker figure.
4. Adjust Line Width through its 8 thickness steps — note the discrete jumps.
5. Set Depth to ~50%. Stare at the figure for 10–15 seconds. Notice the perceptual flip between two valid 3D interpretations.

**Key concepts**: Absolute-distance edge test draws axis-aligned wireframes, depth offset creates axonometric projection, bistable perception arises from ambiguous depth cues

---

### Exercise 2: Video Overlay Composition

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: necker_source1_parrot, after: necker_ex2_s1 },
    { label: "Skull", before: necker_source2_skull, after: necker_ex2_s2 },
    { label: "Clouds", before: necker_source3_clouds, after: necker_ex2_s3 },
    { label: "Pattern", before: necker_source4_pattern, after: necker_ex2_s4 },
    { label: "Man", before: necker_source5_man, after: necker_ex2_s5 },
    { label: "Berries", before: necker_source6_berries, after: necker_ex2_s6 },
  ]}
/>
*Video Overlay Composition — simulated result across source images.*
**Source**: A camera feed or recorded footage with recognizable subjects.

**What You'll Create**: Composite the wireframe over live video and observe how the illusion interacts with real-world depth cues.

1. Enable Overlay. The wireframe now overlays the video source.
2. Set Size and Depth so the cube frames the subject.
3. Adjust Brightness to find a balance where the wireframe is visible but not overwhelming.
4. Try Mix at ~50% to blend the wireframe with the source rather than hard-overlaying it.
5. Notice how the video content behind the wireframe can lock the perceived 3D orientation — real-world depth cues compete with the ambiguous figure.

**Key concepts**: Overlay compositing passes non-edge pixels through unchanged, real-world depth cues can disambiguate the bistable illusion, mix blending softens the overlay

---

### Exercise 3: Extreme Geometry

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: necker_source1_parrot, after: necker_ex3_s1 },
    { label: "Skull", before: necker_source2_skull, after: necker_ex3_s2 },
    { label: "Clouds", before: necker_source3_clouds, after: necker_ex3_s3 },
    { label: "Pattern", before: necker_source4_pattern, after: necker_ex3_s4 },
    { label: "Man", before: necker_source5_man, after: necker_ex3_s5 },
    { label: "Berries", before: necker_source6_berries, after: necker_ex3_s6 },
  ]}
/>
*Extreme Geometry — simulated result across source images.*
**Source**: High-contrast footage or a pattern generator with geometric shapes.

**What You'll Create**: Explore the range of cube geometries from paper-thin to frame-filling, and compare overlay vs. isolated wireframe.

1. Set Size to maximum — the cube edges extend beyond the frame. Only partial edges are visible.
2. Reduce Size to minimum (~5%) — a tiny wireframe appears at screen center.
3. Set Depth to maximum — the back face is offset far from the front. The figure no longer reads as a cube.
4. Set Depth to ~10% and Size to ~40% — a compact figure with subtle depth offset. The Necker flip is strongest when the depth offset is small relative to the face size.
5. Toggle Overlay on and off to compare the figure in isolation vs. composited over the video source.
6. Sweep Brightness from low to high — at low values the wireframe disappears into the background.

**Key concepts**: The Necker illusion is strongest when depth offset is small relative to face size, edge visibility depends on brightness-to-background contrast, extreme parameters produce partial or degenerate figures

---


## Tips

- **Brightness as opacity proxy**: Since edges are achromatic, lowering Brightness against a dark background simulates transparency; against a bright video source, raising it ensures visibility.
- **Use Mix for soft overlay**: At 50% Mix with Overlay enabled, the wireframe blends subtly with the video source rather than hard-cutting over it.
- **Unused controls are harmless**: Rotation, Perspective, Fill, and Animate can be set to any value without affecting output. Avoid Color toggle as it references a broken signal path.
- **Feed into downstream programs**: The wireframe output makes an excellent control signal for keying, edge detection, or modulation programs further down the video chain.

---

## Glossary

| Term | Definition |
|------|------------|
| **Axonometric Projection** | A method of representing 3D objects in 2D where parallel lines remain parallel, as opposed to perspective projection where they converge. |
| **Bistable Perception** | A visual phenomenon where a single image supports two mutually exclusive interpretations that alternate spontaneously. |
| **Chrominance** | The color difference components (U and V) of a YUV signal, encoding hue and saturation. |
| **Luminance** | The brightness component (Y) of a YUV signal. |
| **Necker Cube** | A wireframe cube drawing first described by Louis Albert Necker in 1832, exhibiting spontaneous depth reversal. |
| **Wireframe** | A 3D object representation showing only edge lines, with no filled surfaces. |

---
