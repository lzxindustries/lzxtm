---
draft: true
sidebar_position: 24
slug: /instruments/videomancer/bobbin
title: "Bobbin"
image: /img/instruments/videomancer/bobbin/bobbin_hero.png
description: "Program guide for Bobbin, a Videomancer material program for the LZX video synthesizer."
---

import bobbin_hero from '/img/instruments/videomancer/bobbin/bobbin_hero.png';
import bobbin_before_after from '/img/instruments/videomancer/bobbin/bobbin_before_after.png';
import bobbin_control_panel from '/img/instruments/videomancer/bobbin/bobbin_control_panel.png';
import bobbin_exercise1_result from '/img/instruments/videomancer/bobbin/bobbin_exercise1_result.png';
import bobbin_exercise2_result from '/img/instruments/videomancer/bobbin/bobbin_exercise2_result.png';
import bobbin_exercise3_result from '/img/instruments/videomancer/bobbin/bobbin_exercise3_result.png';

# Bobbin

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={bobbin_hero} alt="Bobbin hero image"/>
*Bobbin rendering a diamond-mesh lace overlay with luminance-darkened thread curves composited over a live video source.*
<img src={bobbin_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Bobbin applied.*

---

## Overview

Bobbin draws a mesh of woven threads across the video image, simulating the look of pillow-lace fabric stretched over a monitor. Two families of sinusoidal curves — one oscillating horizontally, the other vertically — intersect to form either a diamond or hexagonal lattice. Where a pixel falls near a curve, Bobbin darkens it by an amount proportional to its proximity, creating the illusion of semi-transparent threads laid across the picture.

The name references the hand-held bobbins used in traditional pillow lace. Lacemakers cross and twist dozens of bobbin-wound threads over a pricked pattern pinned to a stuffed cushion, building fabric from nothing but air and thread. Bobbin does the same thing in the video domain — it constructs a fabric pattern from mathematical curves, then composites it over whatever image passes through.

At gentle settings — wide thread spacing, low opacity, no tint — Bobbin produces a subtle screen-door texture that softens the image without obscuring it. At extreme settings — narrow spacing, full opacity, solid fill, vivid tint — the lace pattern dominates and the source video becomes a background glimpsed through the mesh.

---

## Background

### Pillow Lace and Bobbin Lace

Pillow lace (also called bobbin lace) originated in 16th-century Flanders and Italy. A lacemaker pins a pricked pattern card to a firm cushion, then manipulates dozens of thread-wound bobbins in pairs — crossing and twisting them around pins to form an open-work fabric. The result is a textile whose structure is entirely defined by the paths of its threads: the negative space (the voids between threads) is as much a design element as the thread itself. Bobbin translates this into video: sinusoidal curves are the thread paths, and the areas between them are the voids.

### Sinusoidal Curve Families

The fundamental building block of Bobbin's mesh is the sine curve. Family A oscillates along the horizontal axis (controlled by the vertical pixel counter), producing undulating horizontal threads. Family B oscillates along the vertical axis (controlled by the horizontal pixel counter), producing undulating vertical threads. The sine function itself comes from a hard-coded 32-entry lookup table storing 8-bit signed values (±127), which is compact enough to fit in LUT fabric without consuming any BRAM.

### Diamond vs. Hexagonal Geometry

When both curve families use the same oscillation frequency, their intersections form a regular diamond (rhombic) lattice — the classic ground pattern of torchon lace. Offsetting Family B by a half period shifts every other row of intersections, creating the familiar diamond shape. When Family B uses a slightly different frequency, the intersection points drift into a hexagonal (honeycomb) arrangement reminiscent of Cluny or Bruges lace grounds. The toggle between Diamond and Hex modes selects between these two geometric families.

### Thread Rendering and Proximity Darkening

For each pixel, Bobbin computes the Manhattan distance to the nearest curve in each family. If that distance falls within the configured thread width, the pixel is classified as "on thread." The proximity value — how close the pixel is to the curve center — scales from 1023 (directly on the curve) to 0 (at the thread edge). The output luminance is then darkened proportionally: `output_y = input_y - (opacity × proximity) >> 10`. This creates threads with soft edges that taper from dark centers to transparent margins, closely mimicking the appearance of real thread under magnification.

### Animation and Phase Accumulation

Bobbin can animate the mesh by advancing a DDS (Direct Digital Synthesis) phase accumulator once per vertical sync interval. The accumulator's value is added to each curve family's phase, causing the entire lattice to drift smoothly across the image. Because the phase offset is identical for both families, the mesh translates as a rigid body — threads maintain their intersections and spacing as they move. The speed control sets the accumulator increment, so the drift rate is continuously variable from static to rapid scrolling.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Curve Generation ───────────────────────────────────────────
│   │
│   ├─ 1. Register Decode        (thread_w LUT, freq scale, hue index)
│   ├─ 2. Phase Accumulator      (vsync-advanced DDS for animation)
│   ├─ 3. Sine LUT × 2           (Family A: v_count×freq, Family B: h_count×freq)
│   ├─ 4. Distance Compute       (Manhattan distance to nearest curve)
│   └─ 5. Thread Detect          (distance < thread_width → on_thread, proximity)
│
├── Compositing ────────────────────────────────────────────────
│   │
│   ├─ 6. Thread Darken (Y)      (input_y - opacity×proximity >> 10)
│   ├─ 7. Hue Tint (U/V)         (optional: hue LUT → U/V modulation)
│   └─ 8. Void/Solid Fill        (void=passthrough, solid=input_y >> 1)
│
├── Output Compose ─────────────────────────────────────────────
│   │
│   ├─ 9. Interpolator Mix       (dry/wet crossfade via Mix fader)
│   └─10. Bypass Mux             (select original or processed)
│
└── Sync Signals ───────────────────────────────────────────────
    └─ Pass-through (hsync, vsync, field, avid)
```

The critical path runs through the sine LUT twice — once for each curve family — then feeds the distance comparator and proximity scaler. Because the sine table is only 32 entries deep, both lookups complete in a single clock cycle using replicated LUT logic (no BRAM). The three `interpolator_u` instances handle thread-pixel Y darkening, optional hue-tinted U/V modulation, and the final dry/wet mix — each consuming one pipeline stage. The entire chain completes in 8 clocks, introducing negligible latency relative to the video frame.

---

## Parameter Reference

<img src={bobbin_control_panel} alt="Videomancer front panel with Bobbin loaded"/>
*Videomancer's front panel with Bobbin active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Thread W
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 7 |

Selects the thread width from eight discrete steps: 2, 3, 4, 5, 6, 8, 12, or 16 pixels. Narrower threads produce delicate lacework with large voids; wider threads create a heavier, more opaque mesh that obscures more of the source image. Because the width control is quantized to 8 steps (not continuous), rotating the knob clicks through distinct mesh densities — each step is a noticeably different weave.

---

#### Knob 2 — Void Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the size of the voids — the open spaces between thread curves. At 0% the curves are packed tightly together with minimal gaps. At 100% the curves are widely spaced, leaving large regions of unobstructed source video visible through the mesh. This control interacts strongly with Thread Width: wide threads plus small voids produce an almost opaque fabric, while narrow threads plus large voids produce a sparse, airy lattice.

---

#### Knob 3 — Curve Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the oscillation frequency of both curve families. Low values produce long, gentle undulations — the threads arc slowly across the screen. High values produce rapid, tight oscillations that create a dense, complex interference pattern at the intersection points. Because Family A and Family B use the same base frequency (with an offset in Hex mode), changing this control reshapes the entire lattice geometry simultaneously.

---

#### Knob 4 — Opacity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls thread opacity — how much the thread darkens the underlying video. At 0% the threads are invisible (no darkening applied). At 100% the threads darken to full black regardless of the source brightness. The darkening is proximity-weighted: pixels at the center of a thread are darkened by the full opacity amount, while pixels at the thread edge receive proportionally less darkening. The default is 75%, producing clearly visible threads that still reveal the source content beneath them.

---

#### Knob 5 — Anim Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Sets the animation speed of the mesh drift. At 0% the lattice is static. As the value increases, the mesh translates across the image at an increasing rate, driven by the DDS phase accumulator. The drift direction is diagonal (both families shift simultaneously), so the mesh appears to slide smoothly at roughly 45 degrees. The default is 25%, producing a slow, meditative drift.

---

#### Knob 6 — Tint Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 60° |
| Suffix | ° |

Selects the hue used to tint thread pixels when Thread Tint is enabled. The control maps to an 8-entry hue LUT cycling through red, orange, yellow, green, cyan, blue, magenta, and back toward red — a full 360° hue sweep. At 0° threads are tinted red; at 180° they are tinted cyan. The tint is applied by modulating the U and V channels of thread pixels according to the LUT values, leaving void pixels unaffected.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mesh Type** | Diamond | Hex |
| **8 — Fill Mode** | Void | Solid |
| **9 — Thread Tint** | Off | On |
| **10 — Anim** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 configure the mesh geometry, void rendering, thread coloring, animation, and bypass. Mesh Type and Fill Mode define the structural character of the lace pattern. Thread Tint adds color via the hue LUT. Anim enables or disables the phase accumulator drift. These four switches are independent — any combination is valid.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet crossfade between the unprocessed source and the lace-composited output. At 0% the output is the original source with no mesh visible. At 100% the output is the fully processed lace overlay. Intermediate values blend the two, which can produce a ghostly, semi-transparent mesh effect distinct from simply reducing thread opacity.

---

## Guided Exercises

These exercises build from a basic static overlay to a fully animated, tinted lace pattern. Each one introduces new controls while reinforcing the interactions learned in the previous exercise.

### Exercise 1: Static Diamond Mesh

<img src={bobbin_exercise1_result} alt="Static Diamond Mesh result"/>
*Static Diamond Mesh — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and moderate contrast.

**Objective**: Learn how thread width, void size, and opacity interact to define the basic mesh structure.

1. **Baseline mesh**: Set Thread W to step 4 (width = 5 pixels), Void Size to 50%, Curve Freq to 50%. A diamond lattice should be clearly visible over the source.
2. **Thread weight**: Rotate Thread W through its 8 steps. Watch the mesh transition from delicate hairlines (step 1, width 2) to heavy bands (step 8, width 16).
3. **Void spacing**: Sweep Void Size from 0% to 100%. At low values the threads crowd together into near-opacity; at high values the mesh opens into a sparse grid.
4. **Opacity gradient**: Sweep Opacity from 0% to 100%. At 0% the mesh vanishes. At 100% the threads are solid black. Find the sweet spot (~60–80%) where threads are clearly visible but the source remains legible.
5. **Frequency modulation**: Sweep Curve Freq. Low values create gentle, wide arcs; high values create rapid oscillations with complex intersection patterns.

**Key concepts**: Thread width is quantized to 8 discrete steps, void size and frequency are continuous, opacity is proximity-weighted (soft thread edges)

---

### Exercise 2: Hex Mesh with Solid Fill

<img src={bobbin_exercise2_result} alt="Hex Mesh with Solid Fill result"/>
*Hex Mesh with Solid Fill — simulated result across source images.*
**Source**: Footage with strong horizontal and vertical elements — architecture, window frames, bookshelves.

**Objective**: Explore hexagonal geometry and the Solid fill mode, which adds a dimmed background behind the mesh.

1. **Switch geometry**: Set Mesh Type to Hex. The regular diamond lattice shifts into a honeycomb-like arrangement. Compare by toggling back and forth.
2. **Solid fill**: Switch Fill Mode to Solid. The void regions dim to half brightness, creating the appearance of a dense fabric backing.
3. **Frequency interplay**: Sweep Curve Freq while in Hex mode. Because Family B uses a slightly different frequency, the interference patterns differ from Diamond mode.
4. **Wide threads, small voids**: Set Thread W to step 7 (width 12), Void Size to ~20%. The mesh becomes nearly opaque — the source is barely visible through small hexagonal windows.
5. **Narrow threads, large voids**: Set Thread W to step 2 (width 3), Void Size to ~80%. A delicate hexagonal lattice floats over the dimmed source.

**Key concepts**: Hex mode uses a frequency offset on Family B to create non-rhombic intersections, Solid fill dims void regions to half brightness, thread width and void size together control mesh density

---

### Exercise 3: Animated Colored Lace

<img src={bobbin_exercise3_result} alt="Animated Colored Lace result"/>
*Animated Colored Lace — simulated result across source images.*
**Source**: Slow-moving or static footage — landscapes, still lifes, or a fixed camera shot.

**Objective**: Combine animation and thread tinting for a fully realized lace effect with colored, drifting threads.

1. **Enable tint**: Switch Thread Tint to On. Rotate Tint Hue slowly through 360°. Watch the thread color cycle through red → yellow → green → cyan → blue → magenta.
2. **Pick a hue**: Choose a tint that complements the source content — warm orange (~45°) for cool-toned footage, cyan (~180°) for warm footage.
3. **Enable animation**: Switch Anim to On. Set Anim Speed to ~25%. The mesh drifts diagonally across the image.
4. **Speed sweep**: Increase Anim Speed gradually. At high values the mesh scrolls rapidly, creating a moiré shimmer at certain frequencies.
5. **Mix blend**: Lower the Mix fader to ~60%. The lace becomes ghostly and semi-transparent — a different effect from reducing Opacity (which changes thread darkness but keeps the mesh at full Mix).
6. **Final composition**: Combine Hex mesh, Solid fill, moderate tint, slow animation, and partial Mix for a complex, layered textile effect.

**Key concepts**: Tint Hue maps to an 8-entry hue LUT for UV modulation, animation uses a DDS phase accumulator advanced per vsync, Mix and Opacity produce different types of transparency

---


## Tips

- **Thread W is quantized**: Unlike the other knobs, Thread W clicks through 8 discrete widths (2–16 pixels). Each step produces a distinctly different mesh density. There are no in-between values.
- **Void Size and Curve Freq interact**: Both affect the spacing between threads, but in different ways — Void Size shifts the curves apart, while Curve Freq changes how often they oscillate. Experiment with both to find the exact lattice geometry you want.
- **Solid fill for fabric look**: Switching to Solid fill and increasing Thread W creates the appearance of a woven textile draped over the screen, with the source visible only as a dim pattern through the weave.
- **Mix and Opacity are different**: Opacity controls how dark the threads are. Mix crossfades the entire processed image with the dry source. Use Opacity for thread transparency; use Mix for overall effect intensity.
- **Tint complements the source**: Choose a Tint Hue that contrasts with the dominant colors in the source for maximum visual impact — warm threads on cool footage, cool threads on warm footage.
- **Animation for texture**: Even a very slow Anim Speed (5–10%) adds subtle life to the mesh, preventing it from locking to the display raster and looking static.
- **Feedback loops**: Routing Bobbin's output back to its input creates recursive mesh layering — each pass adds another lace pattern at a different scale, building increasingly complex textile textures.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chroma** | The colour-difference components (U and V) of a YUV video signal, representing hue and saturation independently of brightness. |
| **DDS** | Direct Digital Synthesis; a technique that generates periodic waveforms by advancing a phase accumulator by a fixed increment each cycle, used here to animate mesh drift. |
| **Hue LUT** | A look-up table that maps a control value to U and V chroma offsets corresponding to a specific colour around the colour wheel. |
| **Interpolator** | A hardware mixing block that crossfades between two input signals using a weighted average, used here for thread darkening and dry/wet blending. |
| **Luma** | The brightness component (Y) of a YUV video signal, darkened proportionally at thread pixel locations. |
| **Manhattan distance** | The sum of absolute horizontal and vertical distances between two points, used here to measure pixel proximity to a curve without computing a square root. |
| **Moiré** | An interference pattern produced when two periodic structures (such as the thread mesh and the display pixel grid) overlap at similar spatial frequencies. |
| **Phase accumulator** | A register that increments by a fixed step each vertical sync interval, whose value offsets both curve families to produce smooth mesh animation. |
| **Rhombic lattice** | A repeating grid of diamond-shaped cells formed by the intersection of two sinusoidal curve families oscillating at the same frequency. |
| **Sine LUT** | A look-up table containing 32 pre-computed signed sine values, used to generate smooth wave curves without real-time trigonometric calculation. |
| **Torchon** | A traditional style of bobbin lace characterized by its regular diamond-mesh ground pattern, the real-world counterpart to Bobbin's Diamond mode. |
| **YUV** | A colour encoding system that separates brightness (Y) from two colour-difference components (U and V), used as the native signal format in Videomancer. |

---
