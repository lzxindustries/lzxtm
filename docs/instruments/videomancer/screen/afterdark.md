---
draft: true
sidebar_position: 1
slug: /instruments/videomancer/afterdark
title: "Afterdark"
image: /img/instruments/videomancer/afterdark/afterdark_hero.png
description: "Before screensavers were quaint nostalgia, they were engineering necessities."
---

import afterdark_hero from '/img/instruments/videomancer/afterdark/afterdark_hero.png';
import afterdark_animation from '/img/instruments/videomancer/afterdark/afterdark_animation.gif';
import afterdark_control_panel from '/img/instruments/videomancer/afterdark/afterdark_control_panel.png';
import afterdark_exercise1_result from '/img/instruments/videomancer/afterdark/afterdark_exercise1_result.gif';
import afterdark_exercise2_result from '/img/instruments/videomancer/afterdark/afterdark_exercise2_result.gif';
import afterdark_exercise3_result from '/img/instruments/videomancer/afterdark/afterdark_exercise3_result.gif';

# Afterdark

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={afterdark_hero} alt="Afterdark hero image"/>
*Afterdark generating bouncing rectangular sprites with color cycling trails across a black field.*
<img src={afterdark_animation} alt="Afterdark animated output"/>
*Afterdark output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Before screensavers were quaint nostalgia, they were engineering necessities. CRT monitors would burn permanent ghost images into their phosphor coatings if a static picture sat too long. The solution was motion — geometric shapes drifting endlessly across the screen, touching every phosphor in turn. Afterdark is a love letter to that era, recreating the bouncing-shape screensaver aesthetic inside the Videomancer's FPGA pipeline.

The program synthesizes rectangular sprites that move across the frame, bouncing off edges with configurable reflection. Shape position is updated per vertical sync interval using velocity accumulators, and color cycling driven by a frame counter creates the rainbow trail effects that defined the genre. The name references the iconic After Dark screensaver software of the late 1980s and early 1990s.

At subtle settings, Afterdark produces clean geometric shapes drifting smoothly across the display. At extreme settings — high trail persistence, rapid color cycling, gravity enabled — it generates dense, layered compositions of overlapping colored rectangles that accumulate into abstract expressionist canvases.

---

## Quick Start

1. **Trail is the composition tool**: Low trail values give clean geometric motion; high values build dense layered paintings over time.
2. **Speed and Size trade off**: Fast small sprites create fine-grained trail textures; slow large sprites create bold overlapping blocks.
3. **Gravity creates natural arcs**: Even subtle gravity values add organic curvature to otherwise linear bounce paths.

---

## Background

### The Screensaver Era

The screensaver emerged in the early 1980s as a practical tool: CRT monitors suffered phosphor burn-in when displaying static images for extended periods. The solution was software that activated during idle periods, replacing the static display with moving graphics. What began as a utilitarian measure quickly became a canvas for generative art. Programs like After Dark (Berkeley Systems, 1989) and its famous "Flying Toasters" module elevated the screensaver from utility to cultural phenomenon.

### Sprite Motion and Edge Reflection

Afterdark's sprite movement uses the simplest possible physics model: constant velocity with perfect elastic reflection at screen boundaries. Each frame, the sprite position increments by a velocity vector. When the sprite reaches a screen edge, the corresponding velocity component reverses sign. This produces the characteristic diagonal bouncing path that eventually visits every region of the screen — a property related to the ergodicity of billiard dynamics in rectangular domains.

### Color Cycling

Color cycling — smoothly rotating through the color spectrum over time — was a signature visual technique of early computer graphics. It exploits the periodic nature of hue in the HSV color model: incrementing the hue angle at a constant rate produces a seamless rainbow progression. In Afterdark, the frame counter drives this rotation, so each new sprite position gets a slightly different color, creating rainbow trails when persistence is active.


---

## Signal Flow

Position Engine → Shape Rasterizer → Trail Compositor → Output Stage → Bypass

```
Synthesis Generator
│
├── Position Engine ────────────────────────────────────────────
│   ├─ 1. Velocity Accumulator   (per-vsync position update)
│   ├─ 2. Edge Detection         (boundary collision test)
│   └─ 3. Reflection             (velocity sign reversal on bounce)
│
├── Shape Rasterizer ───────────────────────────────────────────
│   ├─ 4. Rectangle Hit Test     (|dx| < half_size AND |dy| < half_size)
│   ├─ 5. Shape Select           (rectangle variant from Shape knob)
│   └─ 6. Color Assignment       (frame counter → hue, plus brightness)
│
├── Trail Compositor ───────────────────────────────────────────
│   ├─ 7. Trail Persistence      (fade factor on previous frame)
│   └─ 8. Additive Blend         (new sprite over faded trail)
│
├── Output Stage ───────────────────────────────────────────────
│   ├─ 9. Brightness Scale       (master brightness control)
│   └─ 10. Interpolator Mix      (3× interpolator_u wet/dry)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select generated or bypass signal
```

The position engine operates at frame rate (once per vsync), while the rasterizer runs at pixel rate. The velocity accumulator step size maps directly to the Speed control — higher values produce faster sprite movement. The rectangle hit test compares absolute horizontal and vertical distances from the sprite center against the Size parameter, producing a simple inside/outside determination per pixel. Color cycling applies the frame counter as a hue offset, so trails left behind by previous positions naturally form a rainbow gradient.

---

## Parameter Reference

<img src={afterdark_control_panel} alt="Videomancer front panel with Afterdark loaded"/>
*Videomancer's front panel with Afterdark active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls sprite movement speed by scaling the velocity accumulator step. At minimum, the sprite barely creeps across the screen, leaving dense overlapping trails. At maximum, it zips rapidly from edge to edge, creating widely-spaced trail patterns. Mid-range values produce the classic leisurely drift of vintage screensavers.

---

#### Knob 2 — Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Sets the half-width of the rectangular sprite. Small values produce compact square dots; large values create broad rectangular blocks that dominate the frame. The size also affects how quickly the sprite covers the screen — larger sprites overlap more of the field with each bounce, filling the canvas faster.

---

#### Knob 3 — Color
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the color hue of the sprite. When Color Cycle is enabled, this acts as a hue offset applied to the cycling base color. When Color Cycle is disabled, it sets a fixed hue for the sprite. The full range sweeps through the complete color wheel.

---

#### Knob 4 — Shape
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 2 |

Selects from eight shape variants that modify the basic rectangle. Different step positions produce variations in the rectangular fill pattern — from solid blocks to outlined rectangles to patterned fills. This control uses stepped quantization, snapping to discrete shape indices.

---

#### Knob 5 — Trail
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

At zero, no trail is left — only the current sprite position is visible. As the control increases, previous positions fade more slowly, building up layered compositions of overlapping colored shapes. At maximum, trails persist almost indefinitely, eventually filling the entire frame with accumulated color. Internally, controls the persistence of sprite trails.

---

#### Knob 6 — Gravity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

At zero, there is no gravity even when the toggle is on. As the value increases the sprite arcs in parabolic trajectories, bouncing with increasing energy at the bottom of the screen. High gravity values produce rapid oscillatory bouncing. Internally, sets the gravitational acceleration applied to the vertical velocity component when the Gravity toggle is enabled.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Bounce** | Off | On |
| **8 — Color Cycle** | Off | On |
| **9 — Rotate** | Off | On |
| **10 — Gravity** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent behavioral modes. Bounce enables edge reflection (without it the sprite wraps around). Color Cycle enables frame-counter hue rotation. Rotate applies angular rotation to the sprite shape. Gravity enables vertical acceleration. Bypass routes the signal past all generation.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Master brightness control for the entire synthesized output. Scales the final Y channel value before output. At minimum the output is black; at maximum the sprites and trails are at full brightness. This does not affect the color saturation, only the luminance level.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore the range of Afterdark's generative capabilities, from classic screensaver aesthetics to dense abstract compositions.

### Exercise 1: Classic Bouncing Square

<img src={afterdark_exercise1_result} alt="Classic Bouncing Square result"/>
*Classic Bouncing Square — simulated result across source images.*
**What You'll Create**: Recreate the iconic bouncing-square screensaver with rainbow trails.

1. Set Speed to about 40% for a leisurely drift.
2. Set Size to about 30% for a medium square.
3. Enable Bounce (Switch 7) and Color Cycle (Switch 8).
4. Set Trail to about 50% for moderate persistence.
5. Set Brightness to about 75%.
6. Watch the sprite bounce corner to corner, leaving a rainbow trail.

**Key concepts**: Edge reflection produces zigzag paths, color cycling creates hue variation along the trail, trail persistence controls visual density

---

### Exercise 2: Gravitational Bounce

<img src={afterdark_exercise2_result} alt="Gravitational Bounce result"/>
*Gravitational Bounce — simulated result across source images.*
**What You'll Create**: Add gravity for parabolic sprite trajectories.

1. Start from Exercise 1 settings.
2. Enable Gravity toggle (Switch 10).
3. Set Gravity knob to about 40%.
4. Watch the sprite arc in parabolas, bouncing at the bottom.
5. Increase Trail to 80% to build up dense arc patterns.
6. Try increasing Gravity knob to see faster oscillation.

**Key concepts**: Gravity adds vertical acceleration creating parabolic arcs, higher gravity values produce faster oscillation, trail persistence captures the arc trajectories

---

### Exercise 3: Abstract Composition

<img src={afterdark_exercise3_result} alt="Abstract Composition result"/>
*Abstract Composition — simulated result across source images.*
**What You'll Create**: Use all features simultaneously to generate dense abstract textures.

1. Set Speed to about 70% for rapid movement.
2. Set Size to about 20% for compact shapes.
3. Enable all toggles: Bounce, Color Cycle, Rotate, Gravity.
4. Set Trail to about 90% for maximum persistence.
5. Set Gravity to about 60%.
6. Set Shape to position 4 for a patterned fill variant.
7. Let the composition build for 30–60 seconds.

**Key concepts**: All features combine to create complex layered compositions, rotation adds angular variety, high trail persistence accumulates shapes into dense fields

---


## Tips

- **Color Cycle off for monochrome**: Disable cycling and set Color to your desired hue for single-color compositions.
- **Rotate adds tumble**: The rotation toggle makes the rectangle spin as it moves, creating diamond and angled patterns in the trail.
- **Feedback routing**: Send Afterdark's output through another Videomancer program and back for recursive generative compositions.

---

## Glossary

| Term | Definition |
|------|------------|
| **Color Cycling** | Continuously incrementing a hue angle to produce a smooth rainbow progression over time. |
| **DDS** | Direct Digital Synthesis; an accumulator-based technique for generating waveforms at precise frequencies. |
| **Edge Reflection** | Reversing a velocity component when a moving object reaches a boundary, simulating an elastic collision. |
| **Hue** | The attribute of color perception described as red, green, blue, etc.; the angular position on the color wheel. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function of its previous state. |
| **Screensaver** | Software that displays moving graphics to prevent CRT phosphor burn-in during idle periods. |
| **Sprite** | A two-dimensional graphical object that can be moved independently across a display. |
| **Velocity Accumulator** | A register that adds a step value each frame to compute position, implementing constant-velocity motion. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
