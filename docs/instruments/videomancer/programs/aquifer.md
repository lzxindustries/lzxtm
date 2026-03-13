---
draft: true
sidebar_position: 9
slug: /instruments/videomancer/aquifer
title: "Aquifer"
image: /img/instruments/videomancer/aquifer/aquifer_hero_s1.png
description: "Aquifer simulates the visual distortion of viewing video through a layer of disturbed water."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import aquifer_control_panel from '/img/instruments/videomancer/aquifer/aquifer_control_panel.png';
import aquifer_source1_ballerina from '/img/instruments/videomancer/aquifer/aquifer_source1_ballerina.png';
import aquifer_source2_boat from '/img/instruments/videomancer/aquifer/aquifer_source2_boat.png';
import aquifer_source3_clouds from '/img/instruments/videomancer/aquifer/aquifer_source3_clouds.png';
import aquifer_source4_pattern from '/img/instruments/videomancer/aquifer/aquifer_source4_pattern.png';
import aquifer_source5_man from '/img/instruments/videomancer/aquifer/aquifer_source5_man.png';
import aquifer_source6_wood from '/img/instruments/videomancer/aquifer/aquifer_source6_wood.png';
import aquifer_hero_s1 from '/img/instruments/videomancer/aquifer/aquifer_hero_s1.png';
import aquifer_hero_s2 from '/img/instruments/videomancer/aquifer/aquifer_hero_s2.png';
import aquifer_hero_s3 from '/img/instruments/videomancer/aquifer/aquifer_hero_s3.png';
import aquifer_hero_s4 from '/img/instruments/videomancer/aquifer/aquifer_hero_s4.png';
import aquifer_hero_s5 from '/img/instruments/videomancer/aquifer/aquifer_hero_s5.png';
import aquifer_hero_s6 from '/img/instruments/videomancer/aquifer/aquifer_hero_s6.png';
import aquifer_ex1_s1 from '/img/instruments/videomancer/aquifer/aquifer_ex1_s1.png';
import aquifer_ex1_s2 from '/img/instruments/videomancer/aquifer/aquifer_ex1_s2.png';
import aquifer_ex1_s3 from '/img/instruments/videomancer/aquifer/aquifer_ex1_s3.png';
import aquifer_ex1_s4 from '/img/instruments/videomancer/aquifer/aquifer_ex1_s4.png';
import aquifer_ex1_s5 from '/img/instruments/videomancer/aquifer/aquifer_ex1_s5.png';
import aquifer_ex1_s6 from '/img/instruments/videomancer/aquifer/aquifer_ex1_s6.png';
import aquifer_ex2_s1 from '/img/instruments/videomancer/aquifer/aquifer_ex2_s1.png';
import aquifer_ex2_s2 from '/img/instruments/videomancer/aquifer/aquifer_ex2_s2.png';
import aquifer_ex2_s3 from '/img/instruments/videomancer/aquifer/aquifer_ex2_s3.png';
import aquifer_ex2_s4 from '/img/instruments/videomancer/aquifer/aquifer_ex2_s4.png';
import aquifer_ex2_s5 from '/img/instruments/videomancer/aquifer/aquifer_ex2_s5.png';
import aquifer_ex2_s6 from '/img/instruments/videomancer/aquifer/aquifer_ex2_s6.png';
import aquifer_ex3_s1 from '/img/instruments/videomancer/aquifer/aquifer_ex3_s1.png';
import aquifer_ex3_s2 from '/img/instruments/videomancer/aquifer/aquifer_ex3_s2.png';
import aquifer_ex3_s3 from '/img/instruments/videomancer/aquifer/aquifer_ex3_s3.png';
import aquifer_ex3_s4 from '/img/instruments/videomancer/aquifer/aquifer_ex3_s4.png';
import aquifer_ex3_s5 from '/img/instruments/videomancer/aquifer/aquifer_ex3_s5.png';
import aquifer_ex3_s6 from '/img/instruments/videomancer/aquifer/aquifer_ex3_s6.png';

# Aquifer

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: aquifer_source1_ballerina, after: aquifer_hero_s1 },
    { label: "Boat", before: aquifer_source2_boat, after: aquifer_hero_s2 },
    { label: "Clouds", before: aquifer_source3_clouds, after: aquifer_hero_s3 },
    { label: "Pattern", before: aquifer_source4_pattern, after: aquifer_hero_s4 },
    { label: "Man", before: aquifer_source5_man, after: aquifer_hero_s5 },
    { label: "Wood", before: aquifer_source6_wood, after: aquifer_hero_s6 },
  ]}
/>
*Aquifer refracting a landscape source through concentric water ripples — caustic brightness patterns dance along the wave gradients as dual raindrop sources create interference patterns.*

---

## Overview

Aquifer simulates the visual distortion of viewing video through a layer of disturbed water. A 2D wave equation simulation runs at reduced resolution, propagating circular ripples outward from periodically injected raindrop impulse sources. The height field gradient displaces the video read address horizontally using a BRAM scanline delay buffer, while a caustic brightness boost proportional to gradient magnitude creates the characteristic dancing bright lines that light produces when refracted through a wavy surface.

The name *Aquifer* refers to an underground layer of rock or sediment that holds water — a hidden reservoir. The program reveals the water metaphorically by making the video appear as if viewed through a disturbed pool surface. The caustic refraction patterns — those shimmering bright lines visible on the bottom of a swimming pool — are the visual signature of the effect, instantly recognizable as a natural water phenomenon.

At conservative settings — low drop rate, moderate refraction, no caustic boost — the image gently wobbles as slow ripples pass through. At extreme settings — high drop rate with dual sources, maximum refraction and caustic, reflected edges — the image fragments into a kaleidoscopic shimmer of overlapping interference patterns with brilliant caustic highlights at every wave crest.

---

## Quick Start

1. **Drop Rate controls activity level**: Zero drop rate = calm water. Maximum drop rate = continuous rain. The simulation naturally decays to stillness when no new drops fall.
2. **Damping and Drop Rate are the primary equilibrium controls**: High drop rate with low damping creates a chaotically active surface. Low drop rate with high damping creates brief, isolated disturbances. Find the balance that suits the content.
3. **Refraction and Caustic are independent**: You can have strong displacement with no caustic boost (pure wobble), or strong caustic with no displacement (pure brightness patterns on an undistorted image). The most natural water look uses moderate amounts of both.

---

## Background

### What Is the 2D Wave Equation?

The **2D wave equation** is a mathematical model describing how disturbances propagate through a medium — such as the surface of a body of water. In its discrete form, each point on a grid stores a height value representing the surface elevation at that position. On each time step, the new height at each point is computed as the average of its four neighbors (left, right, above, below) minus the point's previous height value:

$h_{next}(x,y) = \frac{h(x-1,y) + h(x+1,y) + h(x,y-1) + h(x,y+1)}{2} - h_{prev}(x,y)$

This is the simplest discretization of the wave equation and produces physically plausible circular ripple propagation, constructive and destructive interference, and reflection off boundaries. A damping term is applied to prevent energy from accumulating indefinitely — without damping, every ripple would persist forever, and the surface would become chaotic noise.

In this program, the wave simulation runs on a 32×32 grid (one height sample per 64×64 pixel block), using register-array storage for current, previous, and above-row height fields. The simulation updates during vertical blanking, processing one column per clock cycle.

### What Are Caustic Patterns?

**Caustics** are the bright curved lines visible on the bottom of a swimming pool or the surface beneath a glass of water. They form when light rays are refracted (bent) by a curved transparent surface — in this case, the water surface. Where the surface curves inward (convex upward), light rays converge and produce a bright concentration. Where the surface curves outward, rays diverge and the area appears darker. The result is a network of bright filaments that trace the curvature of the water surface.

In this program, caustic brightness is computed from the gradient magnitude of the height field. Where the height field is flat (between ripples), the gradient is zero and no brightness boost is applied. Where the surface is steeply curved (at ripple crests and troughs), the gradient magnitude is large, and a brightness boost proportional to the Caustic pot is added to the Y channel. This creates the characteristic bright dancing lines at wave fronts.

### What Is Refraction Displacement?

**Refraction** is the bending of light as it passes from one medium to another — in this case, from air through the curved water surface to the image beneath. According to Snell's law, the direction of bending depends on the angle of the surface relative to the incoming light. For a wavy water surface viewed from above, this means the apparent position of each point in the submerged image is shifted by an amount proportional to the local slope (gradient) of the surface.

In this program, horizontal displacement is implemented using a BRAM-based scanline delay buffer. The input video is written sequentially into the buffer, and the read address is offset by the scaled horizontal gradient of the height field. Where the surface slopes to the left, the read address shifts left; where it slopes to the right, the read address shifts right. The Refraction pot controls the magnitude of this displacement. Vertical displacement is approximated by a luma perturbation based on the vertical gradient.

### What Is Wave Damping?

In a real body of water, ripples gradually lose energy to viscosity, surface tension, and turbulence. In the discrete wave equation, **damping** is simulated by subtracting a small fraction of the computed next-height value on each update step. Without damping, the system is lossless — every injected impulse ripples outward indefinitely, and the cumulative energy always increases. With heavy damping, ripples decay quickly after a few cycles of propagation. With light damping, ripples persist for many frames, travel farther, and interfere more extensively.

The program implements damping by shifting the next-height value right by a variable number of bits (2–5), controlled by the Damping pot. This provides exponential decay rates from aggressive (25% per frame) to gentle (3% per frame).

### What Is an LFSR?

A **Linear Feedback Shift Register** (LFSR) is a digital circuit that produces a pseudo-random sequence of bits by shifting a register and feeding back a combination of its tapped bits. The sequence is deterministic (given the same seed, it always produces the same output) but statistically well-distributed, making it useful as a lightweight random number source in hardware. In this program, a 16-bit LFSR provides the randomness used to vary raindrop positions and timing, ensuring that ripple patterns evolve unpredictably without requiring a true random number generator.


---

## Signal Flow

```
┌──────────────────────────────────────────────────────────────────┐
│  Vblank Update (wave equation + raindrop injection)              │
│                                                                  │
│  1. Raindrop Injection                                           │
│     ├─ DDS oscillators (LFSR-modulated) compute drop positions   │
│     ├─ Drop timer vs Drop Rate → inject impulse (h = +120)      │
│     ├─ Dual Source: second drop from offset DDS phases           │
│     └─ Drop Spread controls oscillator amplitude                 │
│           ◄── Drop Rate (pot 1), Drop Spread (pot 6),            │
│               Dual Source (toggle 7)                             │
│                                                                  │
│  2. Wave Equation Update (1 column per clock)                    │
│     ├─ For each column: read left, right, above neighbors        │
│     ├─ next = (left + right + above + above) / 2 - prev         │
│     ├─ Damping: subtract v_next >> (2..5)                        │
│     ├─ Boundary: absorb (zero) or reflect (mirror neighbor)      │
│     └─ Saturate to signed 8-bit range                            │
│           ◄── Damping (pot 2), Edge Mode (toggle 8),             │
│               Wave Speed (pot 5), Freeze (toggle 10)             │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Active Video Pipeline (10 clocks total)                         │
│                                                                  │
│  Input Video (YUV 4:4:4 30-bit)                                  │
│  │                                                               │
│  ├── Line Buffer Write (Y/U/V into 2048-deep BRAMs)             │
│  │                                                               │
│  ├─ Stage 1: Height field read                                   │
│  │   └─ Read left, right, center, above from register arrays     │
│  │                                                               │
│  ├─ Stage 1b: Gradient + BRAM address                            │
│  │   ├─ grad_x = right - left                                    │
│  │   ├─ Displacement = grad_x × refraction_scale                 │
│  │   └─ BRAM read_addr = h_count + displacement (clamped)        │
│  │         ◄── Refraction (pot 3)                                │
│  │                                                               │
│  ├─ Stage 2: Gradient magnitude (while BRAM read in flight)      │
│  │   ├─ grad_mag = |right - left| + |center - above|            │
│  │   └─ (Manhattan distance of height field gradient)            │
│  │                                                               │
│  ├─ Stage 2.5: Gradient magnitude delay (align with BRAM)        │
│  │                                                               │
│  ├─ Stage 3: Caustic output                                      │
│  │   ├─ Y = BRAM_Y + grad_mag × caustic_scale                   │
│  │   ├─ Tint Depth: U += grad_mag (blue shift on displacement)  │
│  │   └─ V = BRAM_V (pass-through or tinted)                     │
│  │         ◄── Caustic (pot 4), Tint Depth (toggle 9)            │
│  │                                                               │
│  ├── Interpolator (4 clocks per Y/U/V)                           │
│  │   └─ Mix = lerp(input_delayed, wet, mix_amount)               │
│  │         ◄── Mix (fader 12)                                    │
│  │                                                               │
│  └── Output register                                             │
│                                                                  │
│  Bypass: select delayed input or mix result                      │
│           ◄── Bypass (toggle 11)                                 │
└──────────────────────────────────────────────────────────────────┘
```

The processing chain has two distinct phases: the wave simulation update (during vertical blanking) and the per-pixel displacement pipeline (during active video). The wave update processes one grid column per clock, completing the full 32-column sweep within the blanking interval. During active video, the height field is read but not written — it remains stable across the entire frame.

The horizontal displacement path is the most critical. Input video is written into a 2048-deep BRAM scanline buffer. The height field gradient is computed in Stage 1b, generating a displacement offset that modifies the BRAM read address. The BRAM read has one clock of latency, so the gradient magnitude computation (Stage 2) runs in parallel while the BRAM data is in flight. A one-clock delay register aligns the gradient magnitude with the BRAM output for the caustic brightness application in Stage 3. The Tint Depth toggle adds a blue-shifted chroma tint proportional to the displacement magnitude, giving displaced areas a "underwater" colour cast.

---

## Parameter Reference

<img src={aquifer_control_panel} alt="Videomancer front panel with Aquifer loaded"/>
*Videomancer's front panel with Aquifer active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Drop Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls how frequently new raindrops are injected into the wave simulation. At 0%, no drops fall — the water surface remains still (or decays to stillness if previously disturbed). As the rate increases, drops are injected more frequently, creating overlapping concentric ripple patterns. At maximum, drops fall almost every frame, producing a densely disturbed surface with complex interference patterns. The drop timer compares against this register to determine when to inject the next impulse.

---

#### Knob 2 — Damping
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At 0% (heavy damping), ripples attenuate rapidly — each wave crest loses about 25% of its amplitude per frame, producing short-lived, localized disturbances. At maximum (light damping), ripples persist for many seconds, traveling across the entire grid and creating extensive interference patterns. The damping value selects between four exponential decay rates by controlling the bit-shift amount applied to the wave equation output. Internally, controls the rate at which ripple energy decays.

---

#### Knob 3 — Refraction
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At 0%, no displacement occurs — the video passes through the line buffer undistorted, though caustic brightness may still be applied. As refraction increases, the displacement becomes more dramatic: ripple crests push the image sideways, and the amount of visual distortion grows. At maximum, the displacement is strong enough to create obvious horizontal smearing and fragmentation of the image along wave fronts. The upper 4 bits of the pot register set the displacement multiplier applied to the horizontal gradient. Internally, controls the magnitude of horizontal displacement applied to the video read address.

---

#### Knob 4 — Caustic
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

At 0%, no brightness enhancement occurs — the displaced video passes through at its original luminance. As the caustic amount increases, areas of steep gradient (wave crests and troughs) receive a proportional brightness boost, creating the characteristic bright dancing lines of underwater caustic patterns. At maximum, the boost is strong enough to push gradient areas to peak white, creating vivid white filaments tracing every ripple front. The caustic is applied to the Y channel only by default, with optional chroma tinting via Toggle 9. Internally, controls the intensity of the caustic brightness boost applied at wave gradients.

---

#### Knob 5 — Wave Speed
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Selects the wave propagation speed from four discrete settings. In the VHDL, the Wave Speed pot maps to a shift amount (0–3) that scales how quickly the wave equation update modifies height values. At setting 1, waves propagate slowly — each ripple front advances one grid cell over several frames. At setting 4, propagation is rapid and ripples expand quickly across the grid. Higher speeds also increase the apparent frequency of ripple patterns, since the same drop rate produces faster-moving, more closely spaced wavefronts.

---

#### Knob 6 — Drop Spread
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At 0%, drops always land near the center of the grid, creating concentric ring patterns radiating from a single point. As spread increases, the DDS oscillators move the drop position across a wider area of the grid, producing ripple sources distributed across the surface. At maximum, drops can land anywhere on the grid, creating a spatially varied disturbance pattern. The spread parameter scales the LFSR-modulated phase oscillator amplitude that determines drop position. Internally, controls the spatial range over which raindrop positions vary.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Dual Source** | Single | Dual |
| **8 — Edge Mode** | Absorb | Reflect |
| **9 — Tint Depth** | Off | On |
| **10 — Freeze** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control **independent binary options** with no combined selector. Dual Source adds a second raindrop source with independently animated position. Edge Mode switches between absorbing (energy disappears at boundaries) and reflecting (waves bounce back from edges). Tint Depth adds a blue chroma shift proportional to displacement. Freeze halts the wave simulation update while preserving the current state. Bypass routes the delayed input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Aquifer-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from gentle single-drop ripples to complex multi-source interference patterns with caustic highlights and chroma tinting.

### Exercise 1: Single Raindrop Pool

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: aquifer_source1_ballerina, after: aquifer_ex1_s1 },
    { label: "Boat", before: aquifer_source2_boat, after: aquifer_ex1_s2 },
    { label: "Clouds", before: aquifer_source3_clouds, after: aquifer_ex1_s3 },
    { label: "Pattern", before: aquifer_source4_pattern, after: aquifer_ex1_s4 },
    { label: "Man", before: aquifer_source5_man, after: aquifer_ex1_s5 },
    { label: "Wood", before: aquifer_source6_wood, after: aquifer_ex1_s6 },
  ]}
/>
*Single Raindrop Pool — simulated result across source images.*
**Source**: Camera feed or recorded footage with recognizable subjects — portraits or architectural scenes show displacement clearly.

**What You'll Create**: Observe basic ripple propagation from a single drop source and understand how damping controls ripple persistence.

1. **Clean start**: Set Freeze (Toggle 10) off, Bypass off, Mix at 100%.
2. **Slow drops**: Set Drop Rate (Knob 1) to ~30%. A single raindrop falls every few frames, producing clean concentric rings.
3. **Watch propagation**: With Wave Speed (Knob 5) at step 2, watch a single ripple expand outward from the drop point. The displaced image wobbles concentrically around the impact.
4. **Heavy damping**: Set Damping (Knob 2) to ~15%. Ripples die quickly after a few rings — each drop creates a brief, localized disturbance.
5. **Light damping**: Turn Damping to ~85%. Now ripples persist across the entire grid, reflecting off edges (set Edge Mode to Reflect). Multiple overlapping ring patterns create interference.
6. **Moderate refraction**: Set Refraction (Knob 3) to ~50%. The displacement becomes clearly visible — the image shimmers along ripple fronts.
7. **No caustic**: Keep Caustic (Knob 4) at 0%. Observe pure displacement without brightness enhancement.

**Key concepts**: 2D wave equation propagation, circular ripple expansion, damping controls persistence, refraction displacement without caustic, absorb vs reflect boundary conditions

---

### Exercise 2: Caustic Light Patterns

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: aquifer_source1_ballerina, after: aquifer_ex2_s1 },
    { label: "Boat", before: aquifer_source2_boat, after: aquifer_ex2_s2 },
    { label: "Clouds", before: aquifer_source3_clouds, after: aquifer_ex2_s3 },
    { label: "Pattern", before: aquifer_source4_pattern, after: aquifer_ex2_s4 },
    { label: "Man", before: aquifer_source5_man, after: aquifer_ex2_s5 },
    { label: "Wood", before: aquifer_source6_wood, after: aquifer_ex2_s6 },
  ]}
/>
*Caustic Light Patterns — simulated result across source images.*
**Source**: Moderately bright footage with areas of uniform colour — sky, walls, or fabric show caustic lines most clearly.

**What You'll Create**: Understand how caustic brightness enhancement creates the characteristic underwater light patterns and how it interacts with displacement.

1. **Setup ripples**: Set Drop Rate to ~50%, Damping to ~60%, Refraction to ~40%, Wave Speed to step 2.
2. **Enable caustic**: Turn Caustic (Knob 4) to ~60%. Bright lines appear along every ripple front — the gradient magnitude drives a brightness boost on the Y channel.
3. **Observe caustic character**: Where ripples are strongest (near drop impacts), the caustic lines are brightest. Between ripple rings, the image is undisturbed. At interference points where two ripple fronts cross, the caustic is especially bright.
4. **Maximum caustic**: Push Caustic to 100%. The bright lines become vivid white filaments tracing every wave crest. Areas of high gradient saturate to peak white.
5. **Enable tint**: Switch Tint Depth (Toggle 9) to On. Displaced areas take on a blue-green colour cast, giving the effect a distinctly underwater quality.
6. **Reduce refraction**: Pull Refraction to ~10%. The displacement is minimal but the caustic brightness remains — the image is mostly undistorted but latticed with bright light patterns.

**Key concepts**: Gradient magnitude as caustic driver, caustic brightness boost independent of displacement magnitude, tint depth adds chroma dimension, brightness saturation at high caustic settings

---

### Exercise 3: Rainstorm Interference

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: aquifer_source1_ballerina, after: aquifer_ex3_s1 },
    { label: "Boat", before: aquifer_source2_boat, after: aquifer_ex3_s2 },
    { label: "Clouds", before: aquifer_source3_clouds, after: aquifer_ex3_s3 },
    { label: "Pattern", before: aquifer_source4_pattern, after: aquifer_ex3_s4 },
    { label: "Man", before: aquifer_source5_man, after: aquifer_ex3_s5 },
    { label: "Wood", before: aquifer_source6_wood, after: aquifer_ex3_s6 },
  ]}
/>
*Rainstorm Interference — simulated result across source images.*
**Source**: Any video source — the extreme distortion creates abstract results regardless of content.

**What You'll Create**: Combine dual raindrop sources, maximum rate, and full caustic with reflected edges for the most complex water simulation.

1. **Dual sources**: Switch Dual Source (Toggle 7) to Dual. Two independent drop positions now inject ripples.
2. **Maximum rate**: Set Drop Rate to ~90%. Drops fall almost every frame from both sources.
3. **Fast waves**: Set Wave Speed (Knob 5) to step 4. Ripples expand rapidly, filling the grid with overlapping wavefronts.
4. **Light damping**: Set Damping to ~80%. Ripples persist long enough to create dense interference patterns.
5. **Reflect edges**: Set Edge Mode (Toggle 8) to Reflect. Waves bounce off all four edges, creating standing wave patterns that interact with the primary ripples.
6. **Full refraction + caustic**: Set Refraction to ~80% and Caustic to ~80%. The image fragments into a kaleidoscopic shimmer with brilliant caustic highlights at every interference node.
7. **Add tint**: Enable Tint Depth. Strongly displaced regions take on an underwater blue cast.
8. **Freeze and observe**: Toggle Freeze (Toggle 10) on. The complex pattern freezes in place — a snapshot of the interference field. Resume to watch it evolve again.

**Key concepts**: Dual source interference patterns, constructive/destructive interference, boundary reflection creating standing waves, dense ripple fields, freeze for static pattern analysis

---


## Tips

- **Tint Depth sells the underwater look**: Enabling the blue-shift tint gives displaced areas a convincing aquatic colour cast that significantly enhances the water illusion.
- **Freeze captures a moment**: Use Freeze to lock an interesting ripple pattern in place. The frozen pattern continues to displacement-process every incoming frame, creating a consistent spatial distortion.
- **Reflect mode creates standing waves**: With reflected edges and persistent ripples, energy bounces back and forth across the grid, eventually creating standing wave patterns — stable nodal lines where the surface is permanently still and anti-nodes where it oscillates strongly.
- **Feedback loops create recursive distortion**: Routing the output back to the input causes each frame to be displaced by the ripple pattern and then displaced again, creating accumulating geometric distortion.
- **Bypass for A/B comparison**: Switch 11 or the Mix fader instantly shows the unprocessed input for comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **Caustic** | Bright curved lines formed when light rays converge after refracting through a curved transparent surface such as water. |
| **Damping** | The gradual reduction of wave amplitude over time, simulating energy loss due to viscosity and surface tension in the water model. |
| **DDS** | Direct Digital Synthesis; a technique using phase accumulators and lookup tables to generate periodic waveforms, used here to animate raindrop positions. |
| **Height field** | A 2D grid of elevation values representing the water surface displacement at each spatial sample point. |
| **Interference** | The combination of overlapping wave patterns producing regions where crests reinforce (constructive) or cancel (destructive) each other. |
| **LFSR** | Linear Feedback Shift Register; a digital circuit producing a pseudo-random bit sequence by shifting and feeding back tapped bits, used to randomise raindrop positions. |
| **Refraction** | The bending of light as it passes between media of different optical density, simulated here as horizontal pixel displacement proportional to the water surface gradient. |
| **Snell's law** | The physical law relating the angle of incidence to the angle of refraction when light crosses a boundary between two media of different refractive index. |
| **Standing wave** | A stable wave pattern formed when reflected waves interfere with incoming waves, producing fixed nodes where the surface is still and anti-nodes where it oscillates. |
| **Wave equation** | A partial differential equation describing how disturbances propagate through a medium; discretised here as a 4-neighbour average minus the previous height value. |

---
