---
draft: true
sidebar_position: 136
slug: /instruments/videomancer/inertia
title: "Inertia"
image: /img/instruments/videomancer/inertia/inertia_hero.png
description: "Most Videomancer programs give you direct control — turn a knob, the image changes proportionally."
---

import inertia_hero from '/img/instruments/videomancer/inertia/inertia_hero.png';
import inertia_before_after from '/img/instruments/videomancer/inertia/inertia_before_after.png';
import inertia_control_panel from '/img/instruments/videomancer/inertia/inertia_control_panel.png';
import inertia_exercise1_result from '/img/instruments/videomancer/inertia/inertia_exercise1_result.png';
import inertia_exercise2_result from '/img/instruments/videomancer/inertia/inertia_exercise2_result.png';
import inertia_exercise3_result from '/img/instruments/videomancer/inertia/inertia_exercise3_result.png';

# Inertia

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={inertia_hero} alt="Inertia hero image"/>
*Inertia applying momentum-driven pixelation drift to a colorful video source, with blocks sliding and zooming under accumulated velocity.*
<img src={inertia_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Inertia applied.*

---

## Overview

Most Videomancer programs give you direct control — turn a knob, the image changes proportionally. Inertia inverts that paradigm. Its six continuous controls set *forces* rather than positions. Turning the H Force knob does not move the image sideways; it applies a horizontal push that accelerates the internal state over time. Release the knob back to center and the drift continues, decaying gradually under friction. The program chains a Newtonian physics engine with a sample-and-hold pixelation grid: force integration into velocity, velocity integration into position, and position driving the phase and block size of a spatial mosaic. The result is a mosaic whose blocks slide, zoom, and bounce with tangible physical weight.

The name *Inertia* refers to Newton's first law of motion — an object in motion stays in motion unless acted upon by an external force. Here, the "object" is the sampling grid's phase and scale. Once set in motion, the grid continues drifting until friction bleeds the velocity away or a boundary reflects it. The program draws direct inspiration from the Fairlight CVI's *glide* and *slide* modes, which applied similar momentum-based control to early digital video effects in the 1980s.

At conservative settings — low force, moderate friction — the mosaic shifts gently, blocks drifting a pixel or two per frame. Increasing force and reducing friction produces wild, accelerating scrolls where the sampling grid whips across the image. Zoom momentum adds a third axis, scaling the block size up and down with the same physical inertia. Trail mode introduces 50% motion blur by holding every other frame, softening fast transitions. At extreme settings with bounce enabled, the grid ricochets off invisible walls in an unpredictable, pinball-like trajectory.

---

## Background

### What Is Momentum-Based Control?

Traditional video effects map a control input directly to a parameter: knob at 50% means the parameter is at 50%. **Momentum-based control** adds a layer of physics simulation between the input and the output. The knob sets a *force*, which is integrated over time into *velocity*, which is then integrated into *position*. The position is what actually controls the visual effect. This two-stage integration gives the control a sense of physical mass — it takes time to accelerate, it overshoots when you release, and it gradually comes to rest under friction. The Fairlight CVI (Computer Video Instrument), introduced in 1984, was one of the first commercial video processors to offer this kind of inertial control for image translation and rotation.

### What Is Sample-and-Hold Decimation?

**Sample-and-hold decimation** is a spatial resolution reduction technique. At a horizontal boundary, the current pixel value is captured and then *held* (repeated) for a number of subsequent pixels, creating a block of uniform color. At the next boundary, a new value is captured. The result is the familiar mosaic or pixelation effect — the image appears to be made of rectangular blocks. By varying when the hold boundaries occur (the block size and starting phase), the appearance of the mosaic changes. Inertia uses the physics engine's position to shift the phase of these boundaries, making the mosaic grid slide across the image.

### What Is a Dead Zone?

Analog potentiometers have mechanical tolerances — when centered, the actual voltage may not be exactly at the midpoint. A **dead zone** is a range of input values around the center that the program treats as exactly zero. Inertia uses a ±32 dead zone (out of the 10-bit 0–1023 range) around the 512 center point. Any force input within this band produces zero force, preventing the physics engine from drifting due to pot noise or imprecise centering.

### What Is Bounce vs. Wrap?

When the internal position accumulator reaches a boundary, two behaviors are possible. In **wrap mode**, the position wraps around to the opposite extreme — the effect is continuous scrolling, as if the image were tiled on a cylinder. In **bounce mode**, the velocity is negated and the position clamped at the boundary — the effect reverses direction instantly, like a ball hitting a wall. Bounce mode produces oscillatory motion within fixed limits; wrap mode produces unbounded traversal.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── All Channels (Y, U, V) ─────────────────────────────────────
│   │
│   ├─ 1. Input Register          (latch input + sync edge detect)
│   ├─ 2. Force → Velocity → Position
│   │      (per-frame: force with dead zone, accel shift,
│   │       friction decay, position integration, bounce/wrap)
│   ├─ 3. Block Size Computation  (zoom position magnitude →
│   │      powers of 2: 1–128 horizontal, 1–1024 vertical)
│   ├─ 4. Phase + Counter Setup   (h_pos/v_pos → block phase offset)
│   ├─ 5. Sample-and-Hold         (capture pixel at block boundary,
│   │      hold for block duration; trail skips alternate frames)
│   └─ 6. Output Register         (composite held Y, U, V)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delayed 8 clocks to match processing pipeline
│
├── Interpolator (wet/dry mix) ─────────────────────────────────
│   └─ 4 clocks per channel: crossfade between dry and processed
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical interaction is between the physics engine and the sample-and-hold grid. Velocity and position are updated once per frame (on vsync falling edge), but the block counters run continuously on every active pixel. The position's upper bytes set the *phase* of the block grid — where the block boundaries start — while the zoom position's magnitude determines the *size* of the blocks. This means the mosaic grid slides and scales simultaneously, driven by three independent momentum axes (horizontal, vertical, zoom). The V Stretch control adds additional shift to the vertical block size independently of the horizontal, allowing non-square blocks even at matched zoom levels.

---

## Parameter Reference

<img src={inertia_control_panel} alt="Videomancer front panel with Inertia loaded"/>
*Videomancer's front panel with Inertia active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — H Force
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Applies horizontal force to the physics engine. At center (zero), no force is applied and the horizontal velocity decays under friction. Pushing right of center accelerates the sampling grid's horizontal phase to the right; pushing left accelerates it left. The force passes through a ±32 dead zone around center, so gentle movements near the midpoint produce no drift. The actual acceleration depends on the Accel control (Knob 5), which scales the force before it is added to velocity.

---

#### Knob 2 — V Force
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Applies vertical force. Identical in behavior to H Force, but drives the vertical axis. Combined with H Force, these two controls create 2D inertial motion of the sampling grid — diagonal trajectories when both are non-zero, straight horizontal or vertical when only one is active. The resulting vertical position shifts the phase of the line-based sample-and-hold, making block rows slide up or down across the image.

---

#### Knob 3 — Zoom
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Applies zoom force — momentum that changes the block size over time. At center, no zoom force is applied. Pushing away from center in either direction accelerates block size growth. The zoom position's magnitude is converted to a block shift via the upper 3 bits, giving power-of-2 block sizes from 1 (no pixelation) to 128 (extreme mosaic). Because zoom uses the same momentum physics, it overshoots and oscillates just like the spatial axes.

---

#### Knob 4 — Friction
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the rate at which velocity decays toward zero. At low values, friction is minimal — once the grid is set in motion, it drifts for a long time before stopping. At high values, velocity is aggressively damped, making the grid respond more directly to force inputs and stop quickly when force is removed. The friction is implemented as a right-shift subtraction of the current velocity: higher pot values reduce the shift amount, producing stronger decay.

---

#### Knob 5 — Accel
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Scales the force before it is added to velocity. At low values, the same knob movement produces a gentle push; at high values, a small force input creates rapid acceleration. The acceleration is implemented as a left-shift of the force value, with the upper 3 bits of the pot selecting the shift amount (0–7). Combined with Friction, this control determines the overall responsiveness: high acceleration with low friction creates wild, fast-moving drift; low acceleration with high friction creates sluggish, controlled movement.

---

#### Knob 6 — V Stretch
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Adds additional vertical block size beyond what the zoom axis provides. The upper 2 bits of this control add 0–3 extra shift levels to the vertical block size lookup. At minimum, vertical and horizontal blocks are the same size (square mosaic). As V Stretch increases, the vertical blocks become taller relative to the horizontal — creating wide, banner-like rectangular blocks. This is independent of zoom momentum; it is a static offset.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Bounce** | Wrap | Bounce |
| **8 — ZoomLink** | Off | On |
| **9 — Trail** | Off | On |
| **10 — Reset** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent binary options. Bounce and ZoomLink alter the physics engine's behavior. Trail modifies the sample-and-hold refresh rate. Reset provides a momentary return to initial conditions. These are not combined into a mode selector — each independently modifies one aspect of the system.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfade between the dry (unprocessed) signal and the wet (momentum-pixelated) signal. At 0% the output is entirely dry. At 100% the output is entirely the processed mosaic. Intermediate values blend the two, which can create a translucent overlay of the blocky mosaic over the clean source.

---

## Guided Exercises

These exercises progress from simple directional drift to full multi-axis momentum control with collisions and motion blur.

### Exercise 1: Horizontal Drift

<img src={inertia_exercise1_result} alt="Horizontal Drift result"/>
*Horizontal Drift — simulated result across source images.*
**Source**: A camera feed with strong vertical features — columns, doorways, or vertical stripes.

**Objective**: Learn how force, velocity, and friction interact to create inertial image movement.

1. **Initial push**: Gently turn H Force clockwise past center. Watch the mosaic grid begin to drift rightward — slowly at first, then accelerating.
2. **Release to center**: Return H Force to center. The grid continues drifting, gradually slowing under friction.
3. **Reverse**: Push H Force counter-clockwise. The grid decelerates, stops, then begins moving left.
4. **Friction comparison**: Set Friction to minimum (~0%). Give a brief push with H Force, then release. The grid drifts for a very long time. Now set Friction to ~75%. Repeat the push — the grid stops almost immediately.
5. **Acceleration scaling**: With moderate Friction (~50%), compare Accel at ~25% vs. ~75%. At high acceleration, the same H Force input produces much faster drift.

**Key concepts**: Force integrates into velocity, velocity integrates into position, friction decays velocity, acceleration scales force sensitivity

---

### Exercise 2: Bounce and Zoom

<img src={inertia_exercise2_result} alt="Bounce and Zoom result"/>
*Bounce and Zoom — simulated result across source images.*
**Source**: A static test pattern or graphic with both fine and coarse detail.

**Objective**: Explore zoom momentum and bounce behavior.

1. **Zoom up**: With Friction at ~50%, push Zoom away from center. Watch the block size grow as the position accumulator builds up. The image pixelates into larger and larger blocks.
2. **Release**: Return Zoom to center. The block size continues growing (momentum), then gradually shrinks back as friction pulls the position toward zero.
3. **Bounce mode**: Enable Bounce (Switch 7). Push Zoom hard. When the position hits the boundary, the velocity reverses — blocks grow to maximum, then shrink, then grow again in a bouncing oscillation.
4. **ZoomLink**: Enable ZoomLink (Switch 8). Give a strong H Force push. As horizontal velocity increases, blocks automatically grow even without touching the Zoom knob.
5. **V Stretch**: Turn V Stretch to ~75%. Observe that vertical blocks are now much taller than horizontal blocks — the mosaic becomes rectangular.

**Key concepts**: Zoom is a momentum axis like H/V, bounce reflects velocity at boundaries, ZoomLink couples horizontal speed to block size, V Stretch creates non-square blocks

---

### Exercise 3: Full Momentum Chaos

<img src={inertia_exercise3_result} alt="Full Momentum Chaos result"/>
*Full Momentum Chaos — simulated result across source images.*
**Source**: Any dynamic video footage, especially with movement and color variation.

**Objective**: Combine all axes, trail mode, and bounce for maximum inertial complexity.

1. **Multi-axis push**: Set H Force and V Force both off-center. The grid drifts diagonally across the image, mosaic blocks sliding in two dimensions simultaneously.
2. **Add zoom**: Push Zoom away from center. Now the mosaic is simultaneously sliding and scaling — blocks grow as they drift.
3. **Enable bounce**: Toggle Bounce on. All three axes now reflect at their boundaries, creating a complex, unpredictable trajectory.
4. **Trail mode**: Enable Trail (Switch 9). Motion blur appears — each frame's mosaic partially overlaps the previous, creating a ghostly doubled effect during fast drift.
5. **Friction sweep**: Slowly increase Friction. The chaotic motion dampens, settling into a gentle oscillation. Reduce Friction to near-zero for wild, sustained drift.
6. **Reset recovery**: Toggle Reset (Switch 10) on, then off. All motion stops instantly, the grid returns to default. Resume by applying new forces.
7. **Wet/dry blend**: Pull Mix to ~50%. The blocky mosaic is now overlaid transparently on the clean source — a ghostly, sliding pixelation.

**Key concepts**: Three independent momentum axes compose into complex trajectories, bounce creates bounded oscillation, trail adds temporal blur, reset is an emergency stop, mix blends clean and processed signals

---


## Tips

- **Forces, not positions**: The fundamental paradigm shift. If you turn a force knob and nothing seems to happen, wait — momentum is building. Release and watch the drift continue.
- **Friction is your brake**: At low friction, every input accumulates indefinitely. Start with moderate friction (~50%) until you develop an intuition for the momentum dynamics.
- **Dead zone prevents noise drift**: The ±32 dead zone ensures that centered knobs produce true zero force. If your grid is drifting with all knobs centered, one knob may be slightly miscalibrated — use Reset to clear accumulated state.
- **Bounce vs. Wrap controls containment**: Bounce keeps the effect within bounds, creating oscillatory patterns. Wrap creates unbounded scrolling — useful for continuously drifting mosaics over backgrounds.
- **ZoomLink ties speed to scale**: When enabled, fast horizontal motion automatically increases block size, mimicking the visual effect of motion blur at high speed.
- **Reset is your safety net**: When the accumulated state becomes too chaotic, a quick toggle of Reset (Switch 10) zeros everything instantly. New forces applied afterward start from a clean slate.
- **Feedback loops**: Routing Inertia's output back to its input creates recursive pixelation — the mosaic of a mosaic, drifting within itself. The momentum dynamics make the feedback evolution feel organic rather than mechanical.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed signal for before/after comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **Accumulator** | A register that sums values over time; used here for velocity and position integration. |
| **Bounce** | Boundary behavior where velocity is negated at the position limit, causing reflection. |
| **Dead Zone** | A range of input values around center that the program treats as exactly zero, preventing noise-induced drift. |
| **Fairlight CVI** | Computer Video Instrument (1984); an early digital video processor that pioneered inertial control for image effects. |
| **Fixed-Point** | A number representation using a fixed number of integer and fractional bits (here, 16.8 signed: 16 integer bits, 8 fractional). |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip executing the video processing pipeline. |
| **Friction** | A velocity decay mechanism that subtracts a fraction of the current velocity each frame, simulating physical drag. |
| **Interpolator** | A crossfade module that linearly blends between two signals based on a mix coefficient. |
| **Momentum** | The tendency of the internal state to continue moving after force is removed, arising from velocity integration. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next on each clock cycle. |
| **Sample-and-Hold** | A technique that captures a signal value at one instant and holds it constant until the next capture, creating uniform blocks. |
| **Wrap** | Boundary behavior where position overflows continuously to the opposite extreme, creating seamless scrolling. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
