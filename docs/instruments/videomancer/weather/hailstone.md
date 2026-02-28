---
draft: true
sidebar_position: 117
slug: /instruments/videomancer/hailstone
title: "Hailstone"
image: /img/instruments/videomancer/hailstone/hailstone_hero.png
description: "Hailstone is a particle physics simulation that overlays bright, bouncing shapes onto the input video signal."
---

import hailstone_hero from '/img/instruments/videomancer/hailstone/hailstone_hero.png';
import hailstone_before_after from '/img/instruments/videomancer/hailstone/hailstone_before_after.png';
import hailstone_control_panel from '/img/instruments/videomancer/hailstone/hailstone_control_panel.png';
import hailstone_exercise1_result from '/img/instruments/videomancer/hailstone/hailstone_exercise1_result.png';
import hailstone_exercise2_result from '/img/instruments/videomancer/hailstone/hailstone_exercise2_result.png';
import hailstone_exercise3_result from '/img/instruments/videomancer/hailstone/hailstone_exercise3_result.png';

# Hailstone

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={hailstone_hero} alt="Hailstone hero image"/>
*Hailstone overlaying bright bouncing diamond-shaped particles with splash bars onto a live video source.*
<img src={hailstone_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Hailstone applied.*

---

## Overview

Hailstone is a particle physics simulation that overlays bright, bouncing shapes onto the input video signal. Up to four particles are tracked using 12-bit position accumulators with signed velocities. Each particle falls under simulated gravity, accelerating downward frame by frame until it strikes the bottom of the screen, at which point its vertical velocity inverts and decays — a bounce. On impact, a horizontal bright bar flashes near the ground for several frames, simulating a splash. The particles themselves are rendered as diamond shapes using **Manhattan distance** — a pixel lights up when the sum of its horizontal and vertical distances from the particle center is below a threshold.

The name *hailstone* comes from the colloquial term for frozen precipitation that bounces on impact — an apt description of the on-screen behaviour. It also echoes the *hailstone sequence* in mathematics (the Collatz conjecture), where numbers rise and fall unpredictably before eventually settling, much like the particles' trajectories across the screen.

At conservative settings — small radius, low gravity, two particles — Hailstone produces gentle bright dots drifting across the live video. At extreme settings — four large particles, high gravity, wide splashes, blue tint — the screen fills with diamond flashes and bright impact bars that dramatically transform the source.

> **TOML vs. VHDL discrepancies**: The TOML parameter names and descriptions were written to describe an aspirational feature set. The VHDL implementation is simpler. This supplement documents what the VHDL *actually does*. See individual parameter descriptions for specific discrepancies.

---

## Background

### What Is Manhattan Distance?

In Euclidean geometry, the distance between two points is the straight-line length of the segment connecting them. **Manhattan distance** (also called taxicab distance or L1 norm) measures distance along axis-aligned paths instead: |Δx| + |Δy|. The name comes from the grid layout of Manhattan streets — to get from one intersection to another, you walk along blocks, never diagonally. In Hailstone, pixels are tested against each particle center using Manhattan distance, which produces a diamond (rotated-square) shape rather than a circle. Manhattan distance is computationally cheap — two subtractions and an addition, no multiplication — making it ideal for FPGA implementations where LUT resources are constrained.

### What Is Gravity in a Particle System?

In physics, gravity is a constant downward acceleration. In a discrete-time simulation like Hailstone, this is modelled as a per-frame increment to the vertical velocity: each frame, `vy += gravity_increment`. The velocity accumulates over time, causing the particle to fall faster and faster — the characteristic parabolic arc of a thrown object. When the particle strikes the bottom boundary (Y ≥ 1000), the velocity is inverted and set to a fixed negative (upward) value, causing the bounce. The bounce velocity is less than the impact velocity, so the particle rises to a lower peak each time, eventually settling at the bottom.

### What Is an LFSR?

A **Linear Feedback Shift Register** (LFSR) is a hardware-efficient pseudo-random number generator. It produces a deterministic sequence of bit patterns that has statistical properties similar to true randomness. Hailstone uses a 16-bit LFSR (seeded at 0x7A3C) for two purposes: initial position jitter and horizontal re-randomisation on each bounce. When a particle hits the bottom boundary, a few LFSR bits are added to its X position, so successive bounces wander across the screen rather than repeating the same trajectory.

### What Is an Additive Overlay?

In video compositing, an **additive overlay** adds the brightness of a foreground element to the existing background pixel. If the sum exceeds the maximum (1023 in 10-bit), it is clamped. The result is that bright foreground elements appear to glow — they never darken the background, only brighten it. Hailstone uses additive overlay for both particle rendering and splash bars: particle pixels add a fixed brightness (768 or 1023) to the source luma, and splash bars add 512.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Particle Physics (per-frame at vsync) ──────────────────────
│   └─ 4 particles: gravity → position update → bounce detect
│      → velocity invert + decay → LFSR x-jitter → splash timer
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register           (capture Y + Manhattan distance setup)
│   ├─ 2. Distance Test            (min Manhattan dist < radius → hit)
│   ├─ 3. Brightness Overlay       (additive: particle +768/+1023, splash +512)
│   │      └─ Trail Mode           (if enabled: glow halo at 2× radius)
│   └─ 4. Output Compose           (→ interpolator_u mix)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1–3. Pass-through           (unchanged unless blue tint active)
│   └─ 4. Color Tint               (if blue + hit/splash: U=512+Y/4, V=512)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay pipeline (matched to processing + interpolator)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The particle physics runs in a separate process triggered once per frame at the vsync falling edge. The rendering pipeline (Stages 1–4) runs every pixel clock and tests each pixel against all active particle positions. The minimum Manhattan distance across all particles determines the hit — this means overlapping particles merge into a single bright region rather than drawing separately. Splash bars are composited only near the bottom boundary (within 4 lines of Y=1000) and only while a particle's splash timer is non-zero (8 frames after impact). The blue tint in Stage 4 only applies to pixels that are already hit or splashed — background pixels retain their original chroma.

---

## Parameter Reference

<img src={hailstone_control_panel} alt="Videomancer front panel with Hailstone loaded"/>
*Videomancer's front panel with Hailstone active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Count
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**TOML says "Count" but VHDL controls particle radius.** The register value is right-shifted by 4, the lower 6 bits are taken, and 4 is added, producing a radius in the range 4–67 pixels. Larger values create bigger diamond shapes — at maximum, each particle covers a substantial area. The radius also affects the trail-mode glow halo, which extends to twice the displayed radius. At minimum, particles are small bright dots; at maximum, they are large diamond overlays that dominate the frame.

---

#### Knob 2 — Fall Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**TOML says "Fall Spd" — VHDL uses this as gravity acceleration.** The register value is right-shifted by 6 to produce a small per-frame velocity increment (0–15). At zero, particles float weightlessly with no downward acceleration. At maximum, particles accelerate rapidly and hit the bottom boundary within a few frames, producing frequent fast bounces. Moderate values (~50%) give a natural falling-hailstone feel with visible parabolic arcs.

---

#### Knob 3 — Bounce H
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the upward velocity applied on each bounce (bounce restitution). The register value is right-shifted by 2, negated, and offset by −4 to produce a negative (upward) signed velocity. Higher pot values produce stronger bounces — particles leap higher after impact. At minimum, bounces barely lift the particle off the bottom boundary. This control determines how long particles remain visible in the upper portion of the screen between impacts.

---

#### Knob 4 — Splash Sz
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the horizontal radius of the splash bars that appear when a particle bounces. The register value is right-shifted by 3 and 2 is added, producing a radius of 2–129 pixels. The splash bar appears as a bright horizontal stripe near the bottom boundary, extending this radius in each direction from the particle's X position. At minimum, splashes are narrow flashes; at maximum, they span a large portion of the screen width.

---

#### Knob 5 — Part Sz
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**TOML says "Part Sz" but VHDL uses this as horizontal velocity scale.** The register value is right-shifted by 6 to produce a small signed value used as the base horizontal speed for particle drift. Higher values cause particles to traverse the screen more quickly. Particles wrap horizontally — exiting the right edge reappears at the left, and vice versa.

---

#### Knob 6 — Impact Br
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

**TOML says "Impact Br" but this register is unused in the VHDL.** The signal is mapped from `registers_in(5)` but not referenced in any processing stage. Sweeping this pot has no visible effect. It is reserved for a future firmware revision.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Size** | Small | Medium |
| **8 — Surface** | Bounce | Shatter |
| **9 — Wind** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 are independent binary options, though their TOML descriptions substantially overstate the implemented functionality. Switch 7 toggles between 2 and 4 active particles. Switch 8 enables a glow trail mode. Switch 9 enables a blue color tint on particle and splash pixels. Switch 10 is mapped but unused in the VHDL. Switch 11 bypasses all processing. The TOML describes Switches 7 and 8 as multi-state selectors (steps_4), but the VHDL reads only a single bit from each, so they function as simple on/off toggles despite the TOML listing four value labels.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade via three interpolator_u instances (one per YUV channel). At maximum (default), the output is the full particle composite over the source. At minimum, the output is the unprocessed input (delayed by 8 clocks). Intermediate values blend the particle overlay proportionally — useful for making the particles more subtle or ghostly against the source video.

---

## Guided Exercises

These exercises progress from simple falling particles through splash effects to the full particle system with color tinting and trail mode.

### Exercise 1: Falling Diamonds

<img src={hailstone_exercise1_result} alt="Falling Diamonds result"/>
*Falling Diamonds — simulated result across source images.*
**Source**: Any video source with moderate brightness — a camera feed of a scene with visible midtones works well.

**Objective**: Learn how particle radius, gravity, and bounce interact to create the basic hailstone animation.

1. **Two particles**: Ensure Switch 7 is in its first position (two particles active).
2. **Set moderate radius**: Turn Pot 1 to about 40%. Watch two bright diamond shapes fall across the screen.
3. **Adjust gravity**: Sweep Pot 2 from low to high. At low values, particles drift slowly downward. At high values, they accelerate rapidly and bounce frequently.
4. **Control bouncing**: Turn Pot 3 to about 60%. Observe the upward rebound after each impact. Higher values produce higher bounces.
5. **Enable four particles**: Switch Toggle 7 to its second position. Two more diamonds appear on screen.
6. **A/B compare**: Toggle Bypass (Switch 11) to see the raw source without particles.

**Key concepts**: Manhattan distance creates diamond shapes, gravity is a per-frame velocity increment, bounce inverts and decays vertical velocity, particle count is 2 or 4

---

### Exercise 2: Splash and Trail

<img src={hailstone_exercise2_result} alt="Splash and Trail result"/>
*Splash and Trail — simulated result across source images.*
**Source**: A dark or low-contrast source that lets bright overlays stand out clearly.

**Objective**: Explore splash bar compositing and the trail mode glow effect.

1. **Prepare particles**: Set moderate radius (~30%), moderate gravity (~40%), strong bounce (~70%).
2. **Increase splash width**: Turn Pot 4 to about 70%. When particles hit the bottom, bright horizontal bars flash across the lower portion of the screen.
3. **Observe splash timing**: The splash bar lasts for 8 frames (about 130 ms at 60 fps) after each impact — watch for the brief flash.
4. **Enable trail mode**: Toggle Switch 8 to its second position. A soft glow halo appears around each particle, extending to twice the diamond radius.
5. **Increase radius**: With trail mode on, increase Pot 1 to ~70%. The halos grow proportionally, creating large soft glow regions.
6. **Compare**: Toggle trail mode off and on to see the difference between crisp diamonds and glowing halos.

**Key concepts**: Splash bars are additive composites near the bottom boundary, splash timer runs for 8 frames, trail mode creates a glow halo at 2× radius, all overlays are additive (never darken the source)

---

### Exercise 3: Blue Ice Storm

<img src={hailstone_exercise3_result} alt="Blue Ice Storm result"/>
*Blue Ice Storm — simulated result across source images.*
**Source**: Any source — the blue tint and large particles will dominate the image.

**Objective**: Combine all active features for the most dramatic hailstone effect.

1. **Four particles**: Set Switch 7 to its second position.
2. **Large particles**: Turn Pot 1 to about 80%.
3. **Fast gravity with strong bounce**: Set Pot 2 to ~60% and Pot 3 to ~70%.
4. **Wide splashes**: Set Pot 4 to ~80%.
5. **Enable blue tint**: Toggle Switch 9 on. Particle and splash pixels shift to a cool blue hue against the warm source video.
6. **Enable trail mode**: Toggle Switch 8 on. The glow halos now appear blue as well.
7. **Horizontal drift**: Increase Pot 5 to ~50%. Particles traverse the screen more quickly, covering more ground between bounces.
8. **Reduce mix**: Pull the Mix fader to ~60%. The particles become semi-transparent, blending with the source rather than overpowering it.

**Key concepts**: Blue tint applies only to hit/splash pixels, trail mode and tint combine, mix fader can create semi-transparent particle overlays, horizontal velocity adds lateral motion

---


## Tips

- **Diamond shapes, not circles**: Hailstone uses Manhattan distance for efficiency — this produces diamond (rotated-square) particles. If you want rounder shapes, other Videomancer programs use Euclidean distance masks.
- **TOML names are aspirational**: The TOML labels (Count, Part Sz, Wind, Animate, etc.) describe a planned feature set. The VHDL implements a simpler system. Trust the knob labels on the panel but understand that some controls do not match their descriptions.
- **Pot 6 and Toggle 10 are inert**: Impact Brightness (Pot 6) and Animate (Toggle 10) are mapped to registers but unused in the VHDL. Turning them has no visible effect.
- **Splash bars are brief**: Each splash lasts only 8 frames (~130 ms). With low gravity, bounces are infrequent and splashes rare. Increase gravity for more frequent impacts and more visible splash activity.
- **Trail mode is not persistence**: Trail mode does not accumulate across frames — it is a per-pixel-clock computation that draws a glow halo around each particle's current position. The halo disappears instantly when the particle moves to a new position.
- **Blue tint is selective**: The color tint only applies to pixels that pass the hit or splash test. Background pixels are completely unaffected, so the tint acts as a color key for the particle overlay.
- **Feedback loops**: Routing the output back to the input creates additive particle trails that accumulate frame over frame — particles leave bright streaks across the image.
- **Bypass for A/B comparison**: Switch 11 removes all particle overlays instantly.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Overlay** | A compositing method that adds foreground brightness to the background, never darkening it; values exceeding the maximum (1023) are clamped. |
| **Bounce Restitution** | The proportion of velocity retained after a bounce; in Hailstone, the bounce velocity is a fixed value rather than a proportion of impact velocity. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Gravity** | In a discrete-time particle system, a constant per-frame increment to vertical velocity that simulates downward acceleration. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **LUT** | Look-Up Table; a fundamental FPGA logic resource used to implement combinational functions. |
| **Manhattan Distance** | The sum of absolute differences along each axis: |Δx| + |Δy|. Produces diamond-shaped distance contours rather than circular ones. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **Splash Bar** | A bright horizontal stripe composited near the bottom boundary when a particle bounces, simulating the visual effect of impact. |
| **SPSC Queue** | Single-Producer Single-Consumer lock-free queue used for cross-core communication in the Videomancer kernel. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
