---
draft: true
sidebar_position: 116
slug: /instruments/videomancer/flock
title: "Flock"
image: /img/instruments/videomancer/flock/flock_hero.png
description: "Birds don't follow a conductor."
---

import flock_hero from '/img/instruments/videomancer/flock/flock_hero.png';
import flock_animation from '/img/instruments/videomancer/flock/flock_animation.gif';
import flock_control_panel from '/img/instruments/videomancer/flock/flock_control_panel.png';
import flock_exercise1_result from '/img/instruments/videomancer/flock/flock_exercise1_result.gif';
import flock_exercise2_result from '/img/instruments/videomancer/flock/flock_exercise2_result.gif';
import flock_exercise3_result from '/img/instruments/videomancer/flock/flock_exercise3_result.gif';

# Flock

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={flock_hero} alt="Flock hero image"/>
*Flock scattering eight luminous Lissajous-orbit particles across a video landscape, coupling their paths into coordinated swarm motion.*
<img src={flock_animation} alt="Flock animated output"/>
*Flock output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Birds don't follow a conductor. Each bird in a flock adjusts its trajectory relative to its nearest neighbors — accelerating, banking, drifting — and from these purely local interactions an astonishing collective order emerges. Flock takes this principle and encodes it into eight particle agents orbiting on Lissajous curves.

Each particle carries an independent pair of phase accumulators — one for its horizontal position, one for its vertical — running at coprime frequencies chosen so that no two agents trace the same path. The Speed control scales all eight oscillators simultaneously, and the Coupling control lets each particle borrow a fraction of its predecessor's phase, pulling trajectories toward coordination or letting them disperse. The result is a luminous swarm that can range from eight isolated fireflies tracing their own figure-eight orbits to a tight murmuration where every particle shadows the one ahead of it.

At the rendering stage, every pixel in the frame computes its Manhattan distance to all active particles. The nearest particle within a size threshold gets drawn — as a filled dot or a hollow ring — with brightness that falls off with distance, producing a soft glow around each agent. These rendered particles are composited onto the input video via additive overlay or full replacement, with optional per-particle color and a global invert for negative-image effects.

---

## Quick Start

1. **Start with one particle**: Understanding a single Lissajous orbit makes the full swarm intuitive. Add particles incrementally to see how each agent's unique frequencies create distinct paths.
2. **Coupling is the signature control**: Small amounts of coupling produce the most visually interesting intermediate states — particles loosely coordinating without fully synchronizing.
3. **Size and Scatter interact**: Wide scatter with small size creates sparse firefly pinpoints. Wide scatter with large size creates overlapping luminous clouds. Match them to your desired density.

---

## Background

### Flocking Algorithms and Boids

In 1986, Craig Reynolds introduced *Boids*, a computational model showing that three simple rules — separation, alignment, and cohesion — are sufficient to generate realistic flock, herd, and school behavior from individual agents. Every modern particle-swarm simulation descends from this insight. Flock distills the idea to its minimum: eight agents with a single coupling term that blends neighbor phase into each particle's oscillator. There is no explicit separation or alignment rule — the coupling strength alone controls whether the group scatters or coheres.

### Lissajous Figures

When two sinusoidal signals of different frequency drive the X and Y axes of a display, the resulting trace is a Lissajous figure — the family of curves first studied by Jules-Antoine Lissajous in 1857 using tuning forks and mirrors. Each particle in Flock follows such a curve. Because the X and Y frequencies are coprime (sharing no common factor), the orbit fills a rectangular region over time rather than closing into a simple loop. At low speed the curves are smooth and predictable; at high speed they appear chaotic and fill the screen.

### Phase Coupling and Synchronization

The coupling mechanism in Flock is a form of *phase perturbation*: each particle's phase accumulator is shifted toward its neighbor's phase by an amount proportional to the Coupling control. This is related to the Kuramoto model of coupled oscillators, which describes how a population of oscillators with different natural frequencies can spontaneously synchronize when the coupling exceeds a critical threshold. In Flock, low coupling produces independent orbits; high coupling pulls all eight particles into a synchronized cluster that moves as a single body.

### Particle Rendering and Distance Fields

Rather than plotting individual dots, Flock evaluates every pixel as a point in a *distance field* relative to all active particles. Manhattan distance (|Δx| + |Δy|) is used instead of Euclidean distance because it requires only addition and absolute value — no multiplication or square root — making it efficient in FPGA register logic. The resulting diamond-shaped falloff gives the particles a distinctive angular glow that distinguishes them from the soft circles of Euclidean rendering.

### Emergent Behavior in Simple Systems

Flock's visual richness comes not from complex rules but from the interaction of simple ones. Eight oscillators, one coupling term, and a nearest-particle renderer produce swarm dynamics that look organic and intentional. This is a hallmark of emergent systems: the global behavior cannot be predicted from any single agent's rule, only from the ensemble. Adjusting Speed, Scatter, and Coupling together creates a three-dimensional parameter space where subtle changes can produce dramatic shifts in collective motion.


---

## Signal Flow

Particle Engine → Rendering Pipeline → Wet/Dry Mix → Sync Delay Pipeline → Bypass

```
Input Video (YUV 4:4:4)
│
├── Particle Engine (runs once per frame at vsync) ──────────────
│   │
│   ├─ 1. DDS Phase Accumulate   (8× X + 8× Y accumulators)
│   ├─ 2. Coupling Perturbation  (phase shift from neighbor i−1)
│   └─ 3. Triangle Wave → Screen (phase → position via tri_wave)
│
├── Rendering Pipeline (per pixel, 5 stages) ────────────────────
│   │
│   ├─ Stage 1  Manhattan distance for particles 0–3
│   ├─ Stage 2  Manhattan distance for particles 4–7
│   ├─ Stage 3  Find nearest active particle, apply size threshold
│   ├─ Stage 4  Glow falloff + ring mode + color assign + invert
│   └─ Stage 5  Compose (overlay additive / replace)
│
├── Wet/Dry Mix (3× interpolator_u, 4 clk) ─────────────────────
│   │
│   └─ Interpolate Y, U, V between delayed input and composed output
│
├── Sync Delay Pipeline (9 clk) ────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, Y, U, V)
│
└── Bypass ──────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The particle engine updates all eight agents once per frame on the rising edge of vsync, so particle positions are constant within a single video field. The rendering pipeline then evaluates every active pixel against the frozen positions. The two-stage distance computation (0–3, then 4–7) is a throughput optimization — it splits the eight comparisons across two clock cycles while keeping the pipeline running at full pixel rate. Coupling only flows forward (particle *i* is influenced by particle *i*−1), creating a leader-follower chain where particle 0 is always the independent leader.

---

## Parameter Reference

<img src={flock_control_panel} alt="Videomancer front panel with Flock loaded"/>
*Videomancer's front panel with Flock active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls how fast all eight particle orbits evolve. At zero, the particles freeze in place — their phase accumulators stop advancing. As you increase Speed, the Lissajous trajectories animate more rapidly. Because each particle has unique coprime X and Y frequencies, they all accelerate together but their relative paths diverge. Very high speed causes the orbits to fill the screen quickly, creating a flickering, firefly-like appearance as particles sweep past each pixel in rapid succession.

---

#### Knob 2 — Scatter
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At zero, all particles collapse to the screen center (640, 360). As Scatter increases, the triangle-wave position mapping scales outward, spreading orbits across more of the frame. At maximum, particle paths can extend to the edges and beyond the visible area. Scatter interacts directly with Size — wider scatter means particles spend less time near any given pixel, so you may need to increase Size to maintain visible contact with the swarm. Internally, controls the spatial extent of the particle orbits.

---

#### Knob 3 — Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the distance threshold for particle rendering. A pixel within this threshold of the nearest particle gets illuminated; beyond it, the pixel receives no particle contribution. Small values produce tight pinpoint dots (or thin rings). Large values create broad, overlapping halos where multiple particles blend into luminous clouds. The glow falls off linearly with distance from the particle center, so the visual radius always has a soft gradient edge rather than a hard boundary.

---

#### Knob 4 — Particles
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 8 |

Selects how many of the eight particles are active, from 1 to 8. At minimum, only particle 0 orbits alone — a single Lissajous tracer. Each step adds another agent with its own unique frequency pair.  Fewer particles give cleaner, more geometric patterns; more particles create denser, more complex swarm structures. Because particle 0 is the coupling leader, adding particles 1–7 progressively extends the leader-follower chain.

---

#### Knob 5 — Coupling
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At zero, all eight particles orbit independently on their Lissajous curves, ignoring each other. As Coupling increases, each particle's phase accumulator is pulled toward its predecessor's phase, causing trajectories to converge and the swarm to tighten. At maximum coupling, the particles cluster into a dense group that moves as a near-singular body. The transition from scattered to cohesive motion is gradual and can produce chaotic intermediate states where particles oscillate between following and breaking free. Internally, controls the strength of inter-particle phase perturbation.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Sets the peak brightness of the rendered particles. Glow intensity at each pixel is the product of the distance-based falloff and this Bright control. At low values, particles are dim wisps barely visible over the source video. At high values, they burn bright white (or saturated color in Hue mode). In Overlay mode, particle brightness adds to the input video, so a high Bright setting can push highlights past full scale and clip to maximum. In Replace mode, Bright directly determines the luminance of the particle-only image.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Shape** | Dot | Ring |
| **8 — Color** | White | Hue |
| **9 — Render** | Overlay | Replace |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the rendering character of the particle overlay. Shape and Color control what the particles look like. Render controls how they combine with the input video. Invert flips the brightness polarity of the particle layer before compositing. Bypass routes the input directly to the output, disabling all processing. These toggles are independent — any combination is valid.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Flock processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Flock-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from a single orbiting dot to a full eight-particle coupled swarm, exploring how speed, scatter, coupling, and rendering modes interact to create emergent visual behavior.

### Exercise 1: Single Lissajous Tracer

<img src={flock_exercise1_result} alt="Single Lissajous Tracer result"/>
*Single Lissajous Tracer — simulated result across source images.*
**What You'll Create**: Understand the basic Lissajous orbit, speed, and scatter relationship with a single particle.

1. **One particle**: Set Particles to minimum (1). A single bright dot appears.
2. **Observe the orbit**: With Speed at ~25% and Scatter at ~50%, watch the particle trace a figure-eight or elliptical path.
3. **Speed up**: Increase Speed gradually. The particle moves faster along the same path.
4. **Spread out**: Increase Scatter. The orbit expands toward the screen edges.
5. **Tighten**: Decrease Scatter to near zero. The particle oscillates near the center.
6. **Ring mode**: Toggle Shape to Ring. The filled dot becomes a hollow ring tracing the same orbit.

**Key concepts**: DDS phase accumulation drives smooth orbital motion at coprime X/Y frequencies, Scatter scales the triangle-wave amplitude to control orbit radius, Ring mode subtracts the inner region to show only the perimeter

---

### Exercise 2: Coupled Flock

<img src={flock_exercise2_result} alt="Coupled Flock result"/>
*Coupled Flock — simulated result across source images.*
**What You'll Create**: Explore how coupling strength transforms independent particles into a coordinated swarm.

1. **Add particles**: Set Particles to 8. Eight independent dots orbit across the video.
2. **Introduce coupling**: Slowly increase Coupling from 0%. Watch the particles begin to influence each other's trajectories. Around 30%, they start forming loose groupings.
3. **Strong coupling**: Increase to ~70%. The swarm tightens — particles cluster and move as a group, occasionally a straggler breaks free and snaps back.
4. **Maximum coupling**: At 100%, all particles converge to nearly the same position, orbiting as a single bright cluster.
5. **Color identification**: Toggle Color to Hue. Each particle gets a unique color, making it easy to see which agents are following which paths even when clustered.
6. **Reduce coupling**: Back off Coupling to ~40%. The colored particles spread out but remain loosely coordinated — the characteristic "flocking" behavior.

**Key concepts**: Coupling introduces phase perturbation from neighbor i−1, creating a leader-follower chain. Increasing coupling beyond a threshold causes spontaneous synchronization. Per-particle hue makes individual agents visually trackable within the swarm.

---

### Exercise 3: Luminous Swarm Overlay

<img src={flock_exercise3_result} alt="Luminous Swarm Overlay result"/>
*Luminous Swarm Overlay — simulated result across source images.*
**What You'll Create**: Combine all controls for a rich particle-over-video composite with depth and color.

1. **Set the swarm**: 6 particles, Speed ~35%, Scatter ~60%, Coupling ~50%.
2. **Large halos**: Increase Size to ~60%. Particles become broad glowing clouds that overlap and blend.
3. **Ring wireframes**: Toggle Shape to Ring. The halos become skeletal rings — the intersecting arcs trace visible orbital geometry.
4. **Colored rings**: Toggle Color to Hue. Each ring has a distinct color — overlapping regions create additive color mixing.
5. **Invert**: Toggle Invert. The luminous rings become dark voids cut into the video — the swarm carves negative space from the source.
6. **Replace mode**: Toggle Render to Replace. The input video disappears; only the ring swarm remains — a stand-alone generative pattern.
7. **Blend back**: Use the Mix fader to bring the source video back to ~40%. The rings float over a ghostly, dimmed version of the source.

**Key concepts**: Large Size creates overlapping halos for additive color mixing, Ring mode reveals orbital geometry, Invert flips particle brightness to carve voids, Replace isolates the particle layer, Mix blends the particle and source layers

---


## Tips

- **Ring mode reveals geometry**: Dots show glow; rings show structure. Switch to Ring mode to see the orbital paths traced out as skeletal arcs.
- **Hue mode for tracking**: Per-particle color makes it possible to follow individual agents through the swarm. Essential when experimenting with coupling strength.
- **Invert for voids**: Invert flips the particle layer before compositing. In Overlay mode, particles become dimming regions instead of brightening ones — a useful effect for cutting dark windows into bright source material.
- **Replace mode as a generator**: With Render set to Replace, Flock becomes a stand-alone pattern generator. Use Mix to blend the generated swarm over the source at any ratio.
- **Feedback loops**: Routing the output back into the input creates particle trails — previous-frame positions persist as part of the source, and new particles add on top.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R BT.601 color space standard used for SD video, defining the conversion matrix between RGB and YUV used throughout the Videomancer pipeline. |
| **Coprime** | Two integers sharing no common factor other than 1; coprime frequency pairs ensure Lissajous orbits do not close into simple loops. |
| **Coupling** | Phase perturbation where one oscillator's phase is shifted toward a neighbor's, creating coordinated motion between agents. |
| **DDS** | Direct Digital Synthesis; a method of generating waveforms by accumulating a phase value and mapping it through a wave function (here, triangle wave). |
| **Flocking** | Collective motion of autonomous agents governed by local interaction rules; coined by Craig Reynolds in the Boids model. |
| **Glow Falloff** | Linear decrease in brightness with distance from a particle center, producing a soft gradient halo. |
| **Lissajous Figure** | The curve traced by a point whose X and Y coordinates are independent sinusoidal (or triangular) functions of time at different frequencies. |
| **Manhattan Distance** | The sum of absolute differences in X and Y coordinates (|Δx|+|Δy|), producing diamond-shaped equidistant contours. |
| **Phase Accumulator** | A register that increments by a frequency word each clock cycle, whose overflow produces periodic waveforms. |
| **Triangle Wave** | A periodic waveform that ramps linearly up and down, used here to convert phase to position. |

---
