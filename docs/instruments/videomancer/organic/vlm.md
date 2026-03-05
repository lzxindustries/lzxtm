---
draft: true
sidebar_position: 329
slug: /instruments/videomancer/vlm
title: "VLM"
image: /img/instruments/videomancer/vlm/vlm_hero.png
description: "VLM is a multi-attractor particle light machine inspired by Jeff Minter's Virtual Light Machine (VLM), the legendary music visualiser originally developed for the Atari Jaguar in 1994."
---

import vlm_hero from '/img/instruments/videomancer/vlm/vlm_hero.png';
import vlm_animation from '/img/instruments/videomancer/vlm/vlm_animation.gif';
import vlm_control_panel from '/img/instruments/videomancer/vlm/vlm_control_panel.png';
import vlm_exercise1_result from '/img/instruments/videomancer/vlm/vlm_exercise1_result.gif';
import vlm_exercise2_result from '/img/instruments/videomancer/vlm/vlm_exercise2_result.gif';
import vlm_exercise3_result from '/img/instruments/videomancer/vlm/vlm_exercise3_result.gif';

# VLM

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={vlm_hero} alt="VLM hero image"/>
*Luminous points orbit multiple invisible attractors, painting persistent colour trails across the screen in a recreation of Jeff Minter's Virtual Light Machine concept — pure light motion driven by gravitational choreography.*
<img src={vlm_animation} alt="VLM animated output"/>
*VLM output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

VLM is a multi-attractor particle light machine inspired by Jeff Minter's Virtual Light Machine (VLM), the legendary music visualiser originally developed for the Atari Jaguar in 1994. The program renders emitter particles that orbit invisible gravitational attractors on a persistent framebuffer. As particles move, they leave trails of colour that fade through a 16-entry palette, creating evolving luminous ribbons that trace the gravitational dynamics.

The name is an abbreviation of "Virtual Light Machine" — Minter's self-coined term for his real-time music visualisation system. The VLM was arguably the first console-based music visualiser, predating WinAmp's visual plugins by several years. Minter's design fused gravitational simulation with palette cycling and framebuffer persistence, exactly the technique Videomancer's implementation reproduces.

The FPGA implementation renders 1 to 4 independent attractors on a 64×64 framebuffer with 4-bit indexed colour. Each attractor has an orbiting emitter particle whose position is computed from a simplified gravitational model. The Orbit toggle switches between simple circular orbits and complex, chaotic figure-eight trajectories. The Waveform toggle modulates the stamp intensity between smooth and pulsed modes, adding rhythmic visual emphasis.

---

## Quick Start

1. **Start with one attractor**: Understanding a single orbit's character makes it easier to interpret the multi-attractor composite. Add attractors incrementally.
2. **Complex mode for organic motion**: Complex orbits create non-repeating, chaotic trajectories that look more natural and less mechanical than Simple circular orbits.
3. **Pulsed waveform for rhythm**: Use Pulsed mode to add visual rhythm to the orbital trails. The strobed effect works especially well when synchronised with musical tempo.

---

## Background

### The Virtual Light Machine Legacy

Jeff Minter developed the VLM for the Atari Jaguar's CD add-on in 1994, creating a system that responded to audio input with real-time abstract visuals. The VLM was the culmination of Minter's light synthesiser series, incorporating lessons from Psychedelia (1984), Colourspace (1985), and Trip-a-Tron (1987). Unlike its predecessors, the VLM introduced gravitational dynamics — particles didn't simply follow Lissajous paths but orbited attractors with pseudo-physical motion, creating more organic, unpredictable visual trajectories.

### Gravitational Attractor Dynamics

Each attractor acts as an invisible gravitational centre. An emitter particle orbits this centre with velocity and position updated per frame. In Simple orbit mode, the particle follows a nearly circular or elliptical path. In Complex mode, a perturbation is added that creates figure-eight loops and chaotic divergence, where the particle's trajectory never exactly repeats. The interplay between multiple attractors creates compound gravitational fields where particles' paths are influenced by all attractors simultaneously.

### Framebuffer Persistence and Decay

Like Videomancer's other light synthesiser programs, VLM uses a 64×64 persistent framebuffer where emitter stamps accumulate additively and gradually decay toward black. The Decay knob controls the decay rate — slow decay creates long, flowing trails while fast decay produces short, bright flashes at the particle's current position. The Intensity knob scales the stamp brightness, controlling how quickly cells saturate.

### Pulsed Waveform Mode

The Waveform toggle switches between Smooth and Pulsed stamp intensity. In Smooth mode the stamp always writes at full Intensity. In Pulsed mode the stamp brightness is modulated by a periodic function synchronised to the animation clock, creating rhythmic flashes that give the particle trail a beaded or strobed appearance — as if the emitter pulses on and off during its orbit.


---

## Signal Flow

```
 registers_in(0) ── Speed ─────────────────────────────────────────────────┐
 registers_in(1) ── Attractors (4 steps) ──────────────────────────────────┤
 registers_in(2) ── Decay ─────────────────────────────────────────────────┤
 registers_in(3) ── Hue Speed ─────────────────────────────────────────────┤
 registers_in(4) ── Brightness ────────────────────────────────────────────┤
 registers_in(5) ── Intensity ─────────────────────────────────────────────┤
 registers_in(6) ── Toggles [Orbit Simp/Cmplx|Waveform Smooth/Pulsed|Reset|ModVid|Bypass]
 registers_in(7) ── Mix Fader ─────────────────────────────────────────────┤
                                                                            │
 ┌─────────────────────────────────────────────────────────────────────────┘
 │
 │    ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
 ├───►│  ATTRACTOR SETUP │────►│  ORBIT COMPUTE   │────►│  STAMP WRITE     │
 │    │  1–4 centres     │     │  per emitter:    │     │  additive blend  │
 │    │  screen-space    │     │  position update │     │  × intensity     │
 │    │  positions       │     │  simple/complex  │     │  × waveform      │
 │    └──────────────────┘     └──────────────────┘     └───────┬──────────┘
 │                                                              │
 │    ┌──────────────────┐     ┌──────────────────┐             │ additive FB
 │    │  PALETTE LOOKUP  │◄────│  DECAY ENGINE    │◄────────────┘
 │    │  16-colour table │     │  global per-frame│
 │    │  + hue offset    │     │  decrement       │
 │    │  → YUV 10-bit   │     └──────────────────┘
 │    └───────┬──────────┘
 │            │
 │    ┌───────┴──────────┐
 │    │  BRIGHTNESS      │
 │    │  × bright knob   │
 │    └───────┬──────────┘
 │            │
 │    ┌───────┴──────────┐
 └───►│  INTERPOLATOR    │
      │  dry/wet mix     │
      └──────────────────┘
               │
               ▼
          data_out (YUV)
```

Each frame, the 1–4 active emitter particles have their orbital positions updated based on the current orbit mode. In Simple mode each emitter follows a fixed-radius elliptical path around its attractor. In Complex mode a phase perturbation creates chaotic looping trajectories. After position updates, each emitter's stamp is additively written to the framebuffer at the new position, scaled by the Intensity knob and optionally modulated by the Pulsed waveform.

The global decay pass then decrements all cells by the Decay amount. The resulting 4-bit indices are looked up in the colour palette with a Hue Speed-driven offset, so trail colours cycle through the spectrum over time. Brightness applies a final luminance scaling to the entire output.

---

## Parameter Reference

<img src={vlm_control_panel} alt="Videomancer front panel with VLM loaded"/>
*Videomancer's front panel with VLM active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 34% |
| Suffix | % |

Speed controls how quickly the emitter particles orbit their attractors. At zero all particles are frozen. At moderate values they trace smooth orbital curves. At maximum the orbital frequency is so high that trails overlap continuously, filling the framebuffer with dense colour fields.

---

#### Knob 2 — Attractors
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Attractors selects the number of active gravitational centres from 1 to 4. A single attractor produces one orbital trail. Two attractors create a binary system with interleaving trails. At four, the screen fills with four independent particle streams, creating a complex multi-body visual.

---

#### Knob 3 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

Decay controls the per-frame brightness decrement applied to all framebuffer cells. At zero the framebuffer accumulates indefinitely. At moderate values a balanced trail length is maintained. At maximum, stamps vanish almost immediately, showing only the particle's current position.

---

#### Knob 4 — Hue Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Hue Speed sets the rate at which the palette index offset advances per frame. At zero the colour mapping is static. At moderate values the trail colours slowly shift through the spectrum. At maximum the colours cycle rapidly, creating rainbow shimmer across all trails.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 78% |
| Suffix | % |

Brightness is a global luminance multiplier applied after palette lookup. At zero the output is black. At full value the palette colours reach their maximum intensity. This scales the final rendered output uniformly.

---

#### Knob 6 — Intensity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 68% |
| Suffix | % |

Intensity controls the stamp brightness written to the framebuffer during each emitter write. Low intensity produces faint stamps that require multiple overlapping passes to reach high palette indices. High intensity saturates cells quickly, creating bright, punchy trails. This interacts with Decay — high intensity with fast decay creates bright but short trails.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Orbit** | Simple | Complex |
| **8 — Waveform** | Smooth | Pulsed |
| **9 — Reset** | Off | On |
| **10 — Mod Video** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the orbital dynamics and rendering. Orbit selects simple or complex trajectory modes. Waveform controls stamp brightness modulation. Reset clears the framebuffer. Mod Video and Bypass handle video compositing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the synthesised VLM output. At minimum the output is entirely dry. At maximum the output is entirely wet. Intermediate values blend the orbital trails over the source material.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from understanding single-attractor dynamics to creating complex multi-attractor compositions, exploring how orbit mode and waveform interact to shape the visual output.

### Exercise 1: Single Smooth Orbit

<img src={vlm_exercise1_result} alt="Single Smooth Orbit result"/>
*Single Smooth Orbit — simulated result across source images.*
**What You'll Create**: Study the fundamental orbital mechanics and trail persistence with a single attractor.

1. Set Attractors to 1.
2. Set Orbit to Simple.
3. Set Waveform to Smooth.
4. Set Speed to approximately 25%.
5. Set Decay to approximately 30%.
6. Set Intensity to approximately 60%.
7. Set Hue Speed to approximately 15%.
8. Set Brightness to approximately 80%.
9. Set Mix to 100%.
10. Observe the single particle tracing an elliptical orbit with a fading colour trail.

**Key concepts**: Orbital dynamics, trail persistence, decay rate vs speed relationship.

---

### Exercise 2: Multi-Attractor Chaos

<img src={vlm_exercise2_result} alt="Multi-Attractor Chaos result"/>
*Multi-Attractor Chaos — simulated result across source images.*
**What You'll Create**: Create a complex chaotic light pattern using multiple attractors in Complex orbit mode.

1. Set Attractors to 4.
2. Set Orbit to Complex.
3. Set Waveform to Pulsed.
4. Set Speed to approximately 35%.
5. Set Decay to approximately 25%.
6. Set Intensity to approximately 70%.
7. Set Hue Speed to approximately 40%.
8. Set Brightness to full.
9. Set Mix to 100%.
10. Observe four particles tracing chaotic figure-eight trajectories with pulsed brightness.

**Key concepts**: Multi-attractor dynamics, chaotic trajectories, pulsed waveform modulation.

---

### Exercise 3: Orbital Video Overlay

<img src={vlm_exercise3_result} alt="Orbital Video Overlay result"/>
*Orbital Video Overlay — simulated result across source images.*
**What You'll Create**: Layer the multi-attractor orbital animation over live video for a performance-ready composition.

1. Continue from Exercise 2 with 4 attractors.
2. Enable Mod Video.
3. Set Mix to approximately 65%.
4. Feed a video source with flowing motion (water, smoke, fabric).
5. Switch Orbit between Simple and Complex to compare visual styles.
6. Adjust Decay to balance trail length with video clarity.
7. Try Waveform Smooth vs Pulsed for different rhythmic qualities.
8. Use Reset to clear and restart compositions dynamically.

**Key concepts**: Video modulation, overlay compositing, orbit mode comparison, dynamic reset.

---


## Tips

- **Balance Intensity and Decay**: High intensity with low decay creates saturated, persistent trails. Low intensity with fast decay creates brief, subtle impressions. Find the sweet spot for your composition.
- **Hue Speed for colour evolution**: Animate the palette slowly for gradual colour drift, or quickly for psychedelic rainbow cycling along the trails.
- **Reset for performance**: During live performance, Reset provides a clean canvas on demand — use it between musical sections or for dramatic visual cuts.
- **Mod Video with movement**: Video modulation works best with moving video sources that reveal different parts of the orbital pattern over time.

---
