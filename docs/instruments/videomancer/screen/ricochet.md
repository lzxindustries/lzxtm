---
draft: true
sidebar_position: 235
slug: /instruments/videomancer/ricochet
title: "Ricochet"
image: /img/instruments/videomancer/ricochet/ricochet_hero.png
description: "Every office worker of the 1990s had the same secret hope — that the DVD logo bouncing endlessly in the corner would finally hit the exact corner of the screen."
---

import ricochet_hero from '/img/instruments/videomancer/ricochet/ricochet_hero.png';
import ricochet_animation from '/img/instruments/videomancer/ricochet/ricochet_animation.gif';
import ricochet_control_panel from '/img/instruments/videomancer/ricochet/ricochet_control_panel.png';
import ricochet_exercise1_result from '/img/instruments/videomancer/ricochet/ricochet_exercise1_result.gif';
import ricochet_exercise2_result from '/img/instruments/videomancer/ricochet/ricochet_exercise2_result.gif';
import ricochet_exercise3_result from '/img/instruments/videomancer/ricochet/ricochet_exercise3_result.gif';

# Ricochet

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={ricochet_hero} alt="Ricochet hero image"/>
*Ricochet generating a bouncing spotlight revealing processed video over a dimmed background, with color-cycling border glow and trail persistence.*
<img src={ricochet_animation} alt="Ricochet animated output"/>
*Ricochet output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Every office worker of the 1990s had the same secret hope — that the DVD logo bouncing endlessly in the corner would finally hit the exact corner of the screen. Ricochet turns that shared cultural moment into a video synthesis program. A rectangular or circular spotlight bounces around the frame, elastically reflecting off the screen edges. Inside the spotlight, the input video is processed through one of eight selectable effects. Outside, the video is dimmed to a configurable level. When the spotlight hits a corner — both edges simultaneously — the color palette cycles and an optional full-screen flash fires.

The program implements per-vsync position updating with signed velocity accumulators, octagonal distance approximation for circle mode, a 1-bit-per-16×16-cell trail BRAM that paints visited regions, and eight selectable inside-shape processing effects (pass-through, brighten, invert, colorize, solarize, posterize, threshold, high-contrast). Shape dimensions, movement speed, inside effect, outside dimming level, and an aspect lock mode are all continuously variable. The name evokes the ball's relentless bouncing — a ricochet off every surface.

At low speeds and large shapes, Ricochet works as a gentle spotlight that slowly reveals and conceals portions of the input. At high speeds with trails enabled, it paints an accumulating mosaic of processed video fragments across the frame, building complex layered compositions from the simple act of bouncing.

---

## Background

### The DVD Bounce

The DVD screensaver — a logo drifting diagonally across the screen, changing color each time it strikes an edge — became one of the most widely recognized pieces of generative animation in consumer electronics history. Its appeal lies in its simplicity: constant velocity, perfect reflection, color change on impact. The mathematics guarantee that the logo will eventually visit every region of the screen, but corner hits (where both X and Y edges are struck simultaneously) are rare events whose frequency depends on the aspect ratio and velocity. Ricochet recreates this mechanic, adding a trail BRAM and multiple video processing modes inside the shape.

### Elastic Edge Reflection

When the shape reaches a screen boundary, the corresponding velocity component reverses sign. This is the simplest possible boundary collision model — perfect elastic reflection with zero energy loss. For a rectangle, the bounce condition checks the shape's bounding box against the active video area (1920×1080). For a circle, the octagonal distance approximation `max(|dx|,|dy|) + min(|dx|,|dy|)/2` tests against the half-width radius. The velocity magnitude is derived from the Speed pot by dividing the 10-bit register by 128 and adding 1, giving a range of 1–8 pixels per frame.

### Inside Effects

The In FX knob selects from eight processing effects applied only to pixels inside the bouncing shape. Effect 0 is pass-through (unaltered video). Effect 1 brightens by adding 256 to the Y channel with saturation at 1023. Effect 2 inverts all three channels. Effect 3 colorizes — replacing U and V with the current corner-palette entry while preserving Y. Effect 4 solarizes — folding brightness values above 512 back toward black. Effect 5 posterizes to 3-bit (8 levels). Effect 6 thresholds Y at 512. Effect 7 applies high-contrast bit shifting.

### Trail BRAM

When the Trail toggle is active, a 120×68-cell grid (one bit per 16×16-pixel cell) records which screen regions the spotlight has visited. Trail cells, once marked, render with the inside effect even after the spotlight has moved on. When 75% of cells are marked, the trail auto-clears and accumulation begins again. This creates a slowly building mosaic of processed video patches that periodically resets.


---

## Signal Flow

```
Synthesis Engine
│
├── Position Engine ────────────────────────────────────────────
│   ├─ 1. Input Register          (capture sync edges)
│   ├─ 2. Velocity Accumulator    (per-vsync X/Y position update)
│   └─ 3. Edge Reflection         (velocity sign reversal at boundaries)
│
├── Shape Rasterizer ───────────────────────────────────────────
│   ├─ 4. Hit Test                (rectangle or octagonal circle)
│   ├─ 5. Border Detection        (2–3 pixel ring at shape edge)
│   └─ 6. Trail Lookup            (1-bit BRAM cell for current pixel)
│
├── Video Processor ────────────────────────────────────────────
│   ├─ 7. Inside Effect           (8 selectable modes via In FX knob)
│   ├─ 8. Outside Dimming         (Y × (1023 − Out Dim) / 1023)
│   ├─ 9. Corner Flash            (full-screen palette color on corner hit)
│   └─ 10. Border Glow            (palette color on shape border pixels)
│
├── Output Stage ───────────────────────────────────────────────
│   └─ 11. Interpolator Mix       (3× interpolator_u wet/dry)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select processed or input signal
```

The position engine runs once per vertical sync, updating X and Y positions using signed velocity accumulators. Corner events (both X and Y bounce in the same frame) increment a 3-bit color index into an 8-entry YUV palette and trigger a flash counter that counts down over 8 frames. The hit test runs at pixel rate — every pixel computes its distance from the shape center and determines inside/outside/border status. The trail BRAM is read at pixel rate but written only at vsync (marking the center cell of the current shape position). The outside dimming multiplies the Y channel by `(1023 − Out Dim) / 1023`, and when Out Dim exceeds 900 the chroma is neutralized to mid-gray.

---

## Parameter Reference

<img src={ricochet_control_panel} alt="Videomancer front panel with Ricochet loaded"/>
*Videomancer's front panel with Ricochet active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the sprite movement speed. The 10-bit register is divided by 128 and offset by 1 to produce a velocity magnitude ranging from 1 to 8 pixels per frame. Low values create a leisurely drift reminiscent of classic screensavers. High values produce rapid bouncing that quickly covers the screen, especially useful with Trail enabled to build mosaic compositions rapidly.

---

#### Knob 2 — Width
| Property | Value |
|----------|-------|
| Range | 32px – 960px |
| Default | 380px |
| Suffix | px |

Sets the horizontal width of the bouncing shape. The register is divided by 2 and offset by 32 to give a range of 32 to 543 pixels. In Rectangle mode, this defines the shape's full width. In Circle mode, the half-width sets the octagonal radius. The shape cannot extend beyond the 1920-pixel active area — the bounce engine constrains position to keep the entire shape on-screen.

---

#### Knob 3 — Height
| Property | Value |
|----------|-------|
| Range | 32px – 540px |
| Default | 223px |
| Suffix | px |

Sets the vertical height of the bouncing shape. Same scaling as Width — register / 2 + 32 — giving a range of 32 to 543 pixels. Combined with Width, this defines the aspect ratio of the spotlight window. In Circle mode, Height is ignored and the octagonal radius is derived from Width alone.

---

#### Knob 4 — In FX
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Selects one of eight video processing effects applied inside the bouncing shape, using stepped quantization (steps_8). Effect 0: pass-through. Effect 1: brighten (+256 to Y). Effect 2: invert (complement all channels). Effect 3: colorize (replace chroma with corner palette). Effect 4: solarize (fold above 512). Effect 5: posterize (3-bit quantization). Effect 6: threshold (binary at 512). Effect 7: high-contrast (bit shift).

---

#### Knob 5 — Out Dim
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the dimming level applied to video outside the bouncing shape. At 0%, no dimming — outside video is full brightness. As the control increases, the exterior darkens toward black. Above ~88% (register > 900), the chroma is also neutralized so the exterior becomes monochrome gray fading to black. This creates the classic "spotlight" effect where only the bouncing shape reveals full-color video.

---

#### Knob 6 — Aspect
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

Selects an aspect ratio lock mode via 4-step quantization. Position 0: free aspect (Width and Height independent). Positions 1–3 lock the shape to preset aspect ratios, overriding the Height control. This is useful for maintaining square or cinema-style spotlight proportions regardless of Width setting.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Shape** | Rect | Circle |
| **8 — Trail** | Off | On |
| **9 — Crn Flash** | Off | On |
| **10 — Border** | Off | Glow |
| **11 — Bypass** | Off | On |

The five toggles control independent rendering features. Shape selects between rectangle and circle hit-testing. Trail enables the persistent BRAM mosaic. Corner Flash fires a full-screen flash on corner-hit events. Border Glow renders a colored border ring around the shape edge using the current corner palette entry. Bypass routes the input signal past all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix crossfade between the unprocessed input video and the fully processed bounce output. Three parallel `interpolator_u` instances blend Y, U, and V channels independently using 10-bit fractional precision. At 0% the output is pure dry (original input); at 100% the output is pure wet (bounce-processed).

---

## Guided Exercises

These exercises progress from a simple bouncing spotlight to complex trail-based compositions, gradually engaging more of Ricochet's rendering features.

### Exercise 1: Classic DVD Bounce

<img src={ricochet_exercise1_result} alt="Classic DVD Bounce result"/>
*Classic DVD Bounce — simulated result across source images.*
**Objective**: Recreate the iconic screen-saver bounce with a rectangular spotlight revealing the input video.

1. Set Speed to about 30% for a leisurely diagonal drift.
2. Set Width and Height to about 40% each for a medium rectangle.
3. Set In FX to 0 (pass-through) so the inside simply reveals the input.
4. Set Out Dim to about 80% to darken the exterior significantly.
5. Enable Corner Flash (Switch 9) and Border Glow (Switch 10).
6. Watch the rectangle bounce off edges, flashing on the rare corner hit.

**Key concepts**: Edge reflection produces predictable diagonal paths, corner hits are rare and produce color cycling, the spotlight reveals unaltered video against a dimmed background

---

### Exercise 2: Trail Mosaic

<img src={ricochet_exercise2_result} alt="Trail Mosaic result"/>
*Trail Mosaic — simulated result across source images.*
**Objective**: Use the trail BRAM to progressively reveal processed video across the entire frame.

1. Set Speed to about 50% for moderate coverage rate.
2. Set Width and Height to about 25% for a compact spotlight.
3. Set In FX to 2 (invert) to make the inside effect visually distinct.
4. Set Out Dim to about 95% for near-black exterior.
5. Enable Trail (Switch 8) and Circle mode (Switch 7).
6. Watch as the circle bounces, leaving a growing mosaic of inverted video patches.
7. Observe the auto-clear when 75% of cells are filled.

**Key concepts**: The trail BRAM records visited regions at 16×16 cell resolution, marked cells persist the inside effect, auto-clear at 75% coverage creates a build-reset rhythm

---

### Exercise 3: Effect Showcase

<img src={ricochet_exercise3_result} alt="Effect Showcase result"/>
*Effect Showcase — simulated result across source images.*
**Objective**: Explore the eight inside effects while the spotlight bounces with border glow active.

1. Set Speed to about 20% for slow movement to observe effects clearly.
2. Set Width and Height to about 50% for a large viewing window.
3. Set Out Dim to 100% for a black exterior.
4. Enable Circle mode (Switch 7) and Border Glow (Switch 10).
5. Step through In FX positions 0–7, pausing at each to observe the effect.
6. Note how Effect 3 (colorize) changes tint with each corner hit.
7. Compare Effect 5 (posterize) and Effect 6 (threshold) on the same source material.

**Key concepts**: Eight independent inside effects provide varied processing, colorize effect is linked to the corner-hit palette cycle, posterize and threshold both reduce tonal levels but in different ways

---


## Tips

- **Out Dim is the spotlight control**: High Out Dim values create a classic spotlight-on-dark effect; low values create a subtle inside/outside processing difference.
- **Trail builds compositions**: Enable Trail to progressively reveal processed video across the frame. The auto-clear at 75% creates a recurring build-up rhythm.
- **Corner hits are rare**: With most velocity/size combinations, corner hits occur infrequently. Small shapes and faster speeds make them slightly more common.
- **Effect 3 ties to the palette**: The Colorize effect replaces chroma with the current corner-hit palette entry, so the tint changes each time the spotlight hits a corner.
- **Circle mode simplifies shape**: Circle mode uses only the Width control for radius and an octagonal distance approximation — the result has subtle faceting visible at large radii.
- **Feedback routing**: Send Ricochet's output back into itself for recursive spotlight-within-spotlight compositions.
- **Mix for compositing**: Use the fader at 50% to overlay the spotlight composition semi-transparently on top of the original video.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for trail cell storage. |
| **Color Palette** | An 8-entry table of YUV values indexed by the corner-hit counter, cycling through preset colors. |
| **Corner Hit** | A rare event where the bouncing shape collides with two screen edges simultaneously, triggering a color cycle and optional flash. |
| **Edge Reflection** | Reversing a velocity component when a moving object reaches a boundary, simulating an elastic collision. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Hit Test** | Per-pixel computation determining whether the current screen position is inside, on the border of, or outside the bouncing shape. |
| **Interpolator** | A hardware mixing stage that blends two values by a fractional amount; used for the wet/dry mix fader. |
| **Octagonal Approximation** | A fast distance metric `max(|dx|,|dy|) + min(|dx|,|dy|)/2` that approximates circular distance using only adds and shifts. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Solarize** | A photographic effect that folds brightness values above a threshold back toward black, creating a partial-negative appearance. |
| **Trail BRAM** | A 120×68-cell binary grid recording which screen regions the spotlight has visited. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
