---
draft: true
sidebar_position: 112
slug: /instruments/videomancer/firefly
title: "Firefly"
image: /img/instruments/videomancer/firefly/firefly_hero.png
description: "Firefly simulates a swarm of drifting luminous particles governed by Brownian motion."
---

import firefly_hero from '/img/instruments/videomancer/firefly/firefly_hero.png';
import firefly_animation from '/img/instruments/videomancer/firefly/firefly_animation.gif';
import firefly_control_panel from '/img/instruments/videomancer/firefly/firefly_control_panel.png';
import firefly_exercise1_result from '/img/instruments/videomancer/firefly/firefly_exercise1_result.gif';
import firefly_exercise2_result from '/img/instruments/videomancer/firefly/firefly_exercise2_result.gif';
import firefly_exercise3_result from '/img/instruments/videomancer/firefly/firefly_exercise3_result.gif';

# Firefly

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={firefly_hero} alt="Firefly hero image"/>
*Eight luminous particles drifting across a dark void — soft warm glows tracing Brownian paths through the silence of the screen.*
<img src={firefly_animation} alt="Firefly animated output"/>
*Firefly output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Firefly simulates a swarm of drifting luminous particles governed by Brownian motion. Eight simultaneous point sources occupy the 1280×720 coordinate space, each carrying a position that is nudged by a pseudo-random offset on every vertical blanking interval. The rendering pipeline scans every pixel of the output frame, computing the Manhattan distance from the pixel to each particle center, generating a brightness value that falls off linearly from the core, and accumulating the glow contributions of all eight particles into a single clamped luminance value. The result is a sparse field of soft, overlapping light sources that wander unpredictably across the screen.

The name evokes the bioluminescent beetles of the family Lampyridae, whose intermittent flashes appear to drift through warm summer air with no discernible trajectory. In the digital domain, this apparent randomness is produced by a 16-bit linear feedback shift register (LFSR) that generates two bits of directional offset per particle per frame — a minimal but effective model of Brownian drift. The combination of gentle random motion, pulsating brightness modulation, and warm or cool chrominance produces a contemplative, ambient visual instrument that ranges from a barely perceptible constellation of glowing motes to a dense, overlapping field of radiant color.

Two color palettes offer distinct aesthetic starting points. Warm mode tints all particles with reduced U and elevated V, producing amber-gold tones reminiscent of candlelight or firefly bioluminescence. Cool mode inverts this relationship with elevated U and reduced V, evoking moonlit phosphorescence or deep-sea luminescence. The Pulse toggle adds a temporal dimension by halving brightness every eight frames, creating a rhythmic on-off flicker that reinforces the biological metaphor.

---

## Quick Start

1. **Start with Pulse On for the firefly effect**: The rhythmic brightness modulation is what gives Firefly its biological character. Without pulse, the particles are steady glowing dots — pleasant, but less evocative of their namesake.
2. **Size and Brightness together control visual weight**: Large size with low brightness produces soft, barely-there halos. Small size with high brightness produces intense, crisp points. Matching both to moderate levels gives the most naturalistic glow.
3. **Manhattan distance means diamonds, not circles**: The diamond-shaped glow is a feature, not a limitation. At small sizes it is barely noticeable; at large sizes it becomes a distinctive geometric signature that recalls pixel-art traditions.

---

## Background

### Bioluminescence

Bioluminescence — the production of light by living organisms — is among the most widespread and ancient biochemical capabilities on Earth. From deep-sea jellyfish and anglerfish to terrestrial fireflies and glowworms, organisms across dozens of phyla produce light through the oxidation of luciferin substrates catalyzed by luciferase enzymes. The firefly's flash is particularly iconic: it is a precisely timed pulse controlled by nitric oxide signaling in specialized photocytes, used for species recognition and mate selection. Firefly's warm color palette and pulse modulation directly echo this biological rhythm — the intermittent amber glow of *Photinus pyralis* drifting through a summer meadow.

### Brownian Motion

In 1827, botanist Robert Brown observed pollen grains suspended in water executing an erratic, jittering dance with no apparent cause. Einstein's 1905 theoretical explanation — that the visible motion results from the cumulative impact of invisible molecular collisions — established Brownian motion as a foundational concept in statistical mechanics. The key insight is that a random walk composed of many small, independent steps produces smooth-looking drift over long timescales despite being fundamentally stochastic at short timescales. Firefly implements a discrete Brownian walk: each particle receives a ±1 pixel offset per axis per frame, derived from the LFSR. Over hundreds of frames, this produces the characteristic meandering trajectories that inspired Brown's original observations.

### Particle Systems in Computer Graphics

Particle systems, formalized by William Reeves at Lucasfilm in 1983, represent amorphous phenomena as collections of independent point masses. Traditional implementations use frame buffers to accumulate per-particle contributions, but Firefly takes the streaming approach dictated by the FPGA video pipeline: rather than plotting particles into memory, it evaluates all eight distance tests for every output pixel in real time. This scanline-distance-field technique eliminates the need for any pixel memory — the entire rendering computation is purely register-based, evaluated fresh for each pixel at wire speed. The result is a zero-BRAM particle renderer that trades mathematical sophistication for hardware simplicity.

### Screensaver Art

The screensaver emerged in the late 1980s as a practical utility — preventing phosphor burn-in on CRT monitors by ensuring continuous pixel movement. Programs like *Starfield Simulation*, *Flying Toasters*, and the Windows *Mystify Your Mind* quickly transcended their utilitarian purpose, becoming a distinct art form: autonomous, generative, and designed for sustained ambient viewing. Firefly belongs to this lineage of contemplative screen art, producing slowly evolving compositions that reward peripheral attention rather than focused scrutiny. The drifting particles serve the same dual purpose as their CRT-era ancestors: perpetual motion across the display surface, wrapped in an aesthetic that transforms utility into beauty.

### Manhattan Distance Approximation

True Euclidean distance — $\sqrt{dx^2 + dy^2}$ — requires multiplication and square root operations that are expensive in combinatorial FPGA logic. The Manhattan distance — $|dx| + |dy|$ — provides a computationally cheap approximation that requires only absolute value and addition. The resulting iso-distance contours are diamond-shaped rather than circular, giving each particle a characteristic rhombus glow pattern. This diamond geometry is a deliberate aesthetic choice as much as a hardware optimization: it recalls pixel-art traditions and early computer graphics where computational constraints shaped visual language, producing geometric forms that are unmistakably digital.


---

## Signal Flow

Clock 0: Register Decode → Internal LFSR16 → 8 Particle Position → ... → Sync Pipeline → Bypass Mux

```
Synthesis Engine (no input video required)
│
├── Clock 0: Register Decode ──────────────────────────────────
│   ├─ speed      = registers_in(0)     [10-bit, unused in VHDL]
│   ├─ size       = registers_in(1)     [10-bit] → particle_r [8-bit]
│   ├─ brightness = registers_in(2)     [10-bit]
│   ├─ count      = registers_in(3)     [10-bit, unused in VHDL]
│   ├─ flicker    = registers_in(4)     [10-bit, unused in VHDL]
│   ├─ trail      = registers_in(5)     [10-bit, unused in VHDL]
│   ├─ mix_amount = registers_in(7)     [10-bit]
│   └─ toggles from registers_in(6):
│       ├─ bit 0: color_mode (0=warm, 1=cool)
│       ├─ bit 1: pulse      (0=off, 1=on)
│       ├─ bit 2: drift      (0=off, 1=on) [unused in VHDL]
│       ├─ bit 3: swarm      (0=off, 1=on) [unused in VHDL]
│       └─ bit 4: bypass
│
├── Internal LFSR16 (seed=0xB5A7) ────────────────────────────
│   └─ taps 15,13,12,10 → 16-bit pseudo-random stream
│
├── 8 Particle Position Registers ────────────────────────────
│   ├─ s_px[0..7]: 12-bit unsigned X positions
│   ├─ s_py[0..7]: 12-bit unsigned Y positions
│   └─ Initial positions:
│       X = [200, 400, 600, 800, 300, 500, 700, 900]
│       Y = [100, 200, 300, 400, 150, 250, 350, 450]
│
├── Position Counters ────────────────────────────────────────
│   ├─ s_x_counter: 12-bit horizontal pixel counter
│   └─ s_y_counter: 12-bit vertical line counter
│
├── Brownian Drift Update (per vsync) ────────────────────────
│   ├─ LFSR step: shift left, feedback = bit15⊕bit13⊕bit12⊕bit10
│   ├─ Frame counter increment
│   └─ For each particle i = 0..7:
│       ├─ s_px(i) += lfsr(1:0) − 1    [range −1..+2]
│       ├─ s_py(i) += lfsr(3:2) − 1    [range −1..+2]
│       ├─ Wrap: if s_px(i) > 1280 → 0
│       └─ Wrap: if s_py(i) > 720  → 0
│
├── Per-Pixel Manhattan Distance Rendering ───────────────────
│   For each particle i = 0..7:
│   ├─ dx = |x_counter − s_px(i)|
│   ├─ dy = |y_counter − s_py(i)|
│   ├─ dist = dx + dy  (Manhattan)
│   ├─ if dist < particle_r:
│   │   └─ glow = brightness − dist  (linear falloff)
│   └─ total_glow += glow  (accumulate all particles)
│
├── Clamp ────────────────────────────────────────────────────
│   └─ if total_glow > 1023 → 1023
│
├── Color Assignment ─────────────────────────────────────────
│   ├─ proc_y = clamped total_glow
│   ├─ Warm: proc_u = 448, proc_v = 640
│   └─ Cool: proc_u = 640, proc_v = 384
│
├── Pulse Modulation ─────────────────────────────────────────
│   └─ if pulse=1 AND frame_counter(3)=1:
│       └─ proc_y >>= 1  (halve brightness)
│
├── Interpolator Stage — wet/dry mix (4 clocks each) ─────────
│   ├─ mix_y = lerp(input_y, proc_y, mix_amount)
│   ├─ mix_u = lerp(input_u, proc_u, mix_amount)
│   └─ mix_v = lerp(input_v, proc_v, mix_amount)
│
├── Sync Pipeline (8-stage delay) ────────────────────────────
│   └─ hsync_n, vsync_n, field_n, Y, U, V delayed 8 clocks
│
└── Bypass Mux ──────────────────────────────────────────────
    └─ bypass ? delayed_input : mixed_output
```

The architecture splits cleanly into two temporal domains. The drift engine runs exclusively during the vertical blanking interval: a single LFSR step provides the random bits that offset all eight particle positions simultaneously using the same two-bit field (bits 1:0 for X, bits 3:2 for Y). Because the LFSR advances only once per vsync, all eight particles receive the same directional bias on any given frame — a subtle correlation that occasionally produces coordinated drifts before the LFSR state diverges their paths on subsequent frames. The rendering pipeline operates during active video, evaluating eight Manhattan distance tests per pixel purely in combinatorial logic, accumulating glow additively, and passing the result through the interpolator mix stage in a fixed 8-clock pipeline.

The pulse modulation operates on the already-rendered luminance by examining bit 3 of the frame counter — effectively dividing the 60 Hz frame rate into 8-frame groups and halving brightness during every other group. This produces a slow, rhythmic fade at approximately 3.75 Hz (on for 8 frames, dim for 8 frames), a cadence that closely matches the flash interval of many *Photinus* firefly species. The modulation applies after glow accumulation but before the wet/dry mix, so the pulse affects only the synthesized particle field and not the passthrough input video.

---

## Parameter Reference

<img src={firefly_control_panel} alt="Videomancer front panel with Firefly loaded"/>
*Videomancer's front panel with Firefly active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the notional speed of particle drift. Although this parameter is mapped to a register in the TOML interface, the current VHDL implementation does not use it — particle drift rate is fixed at ±1 pixel per frame per axis. Future firmware revisions may scale the LFSR-derived offset by this value. At default, the control has no visible effect; it exists as a reserved interface point for extended drift behavior.

---

#### Knob 2 — Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

At minimum, particles render as tiny points with almost no visible extent — single-pixel diamonds barely distinguishable from noise. At maximum, each particle projects a large diamond-shaped glow field where brightness falls off linearly from center to edge via Manhattan distance. Larger radii dramatically increase the chance of particle overlap, causing additive brightness accumulation that can saturate to full white where multiple glow fields intersect. The interaction between Size and Brightness determines the visual weight of each particle: large size with moderate brightness produces soft, diffuse halos, while small size with high brightness produces intense pinpoints. Internally, sets the rendering radius of each particle by extracting the upper 8 bits of the 10-bit register value.

---

#### Knob 3 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Sets the peak luminance of each particle's glow field. The brightness value serves as the ceiling from which Manhattan distance is subtracted: a pixel at distance *d* from a particle center receives a glow contribution of *brightness − d*, clamped to zero when distance exceeds brightness. At maximum, particles render as intensely bright cores with wide falloff tails. At minimum, particles are barely visible — their glow contribution drops below the perceptible threshold within a few pixels of center. Brightness interacts multiplicatively with particle overlap: where two particles' glow fields intersect, their contributions add, so high brightness with multiple overlapping particles quickly saturates to the 1023 clamp ceiling.

---

#### Knob 4 — Count
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 4 |

Controls the intended particle count. Although this parameter is mapped to a register, the current VHDL implementation always renders all 8 particles regardless of this setting. The count value is reserved for future firmware revisions that may selectively disable particle slots based on this control. At any setting, all eight particles drift and render identically.

---

#### Knob 5 — Flicker
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls a notional flicker intensity that would modulate per-particle brightness with random variation. This parameter is reserved in the TOML interface but not implemented in the current VHDL — particle brightness is determined solely by the Brightness knob and the Pulse toggle. Future firmware may use this register to scale a per-frame random brightness offset applied to individual particles, creating an organic, candle-like shimmer independent of the global Pulse modulation.

---

#### Knob 6 — Trail
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls a notional persistence trail that would blend previous frame positions into the current output. This parameter is reserved but not implemented in the current VHDL, which has no frame buffer and therefore no temporal persistence. Each frame is rendered independently with no memory of prior particle positions. Future revisions using BRAM-based frame storage could implement exponential decay trails that trace each particle's Brownian path across the screen.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color** | Warm | Cool |
| **8 — Pulse** | Off | On |
| **9 — Drift** | Off | On |
| **10 — Swarm** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–11 configure five independent binary aspects of the particle system. Color (7) selects between warm amber and cool blue chrominance. Pulse (8) enables rhythmic brightness modulation at a ~3.75 Hz cadence. Drift (9) and Swarm (10) are reserved for future firmware extensions — Drift is wired to the drift-enable signal but the VHDL always applies drift regardless, while Swarm has no behavioral effect. Bypass (11) routes the delayed input directly to the output. The two active toggles (Color and Pulse) and the Bypass toggle provide six distinct combinatorial modes; the reserved toggles expand the interface for future development.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix ratio between the delayed input video and the synthesized particle field. At maximum (1023), the output is fully wet — the synthesized particles at full intensity mixed over the input. At minimum (0), the output is fully dry — only the delayed input passes through with no particle contribution. Intermediate values create a translucent overlay where particles appear as soft ghosts superimposed on the source. For pure synthesis without any input signal, set Mix to maximum to display only the particle field. When using Firefly as an overlay effect on external video, reduce Mix to blend particles at lower opacity for a subtle ambient glow layer.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore Firefly's ambient synthesis capabilities, progressing from a basic warm constellation through pulse-modulated bioluminescence to cool-toned spatial density experiments.

### Exercise 1: Warm Drift

<img src={firefly_exercise1_result} alt="Warm Drift result"/>
*Warm Drift — simulated result across source images.*
**What You'll Create**: Create a gentle field of warm amber fireflies drifting across a dark background, observing the Brownian path characteristics and Manhattan distance glow geometry.

1. **Verify synthesis mode**: Ensure no external video is connected, or set Mix to maximum for pure synthesis output.
2. **Set warm tones**: Color toggle to Warm. Eight amber particles should be visible.
3. **Moderate brightness**: Set Brightness to ~75%. Particles glow visibly but do not oversaturate at overlap zones.
4. **Medium size**: Set Size to ~40%. Each particle projects a noticeable diamond-shaped glow field.
5. **Disable pulse**: Set Pulse to Off. Brightness should be constant — observe the steady drift.
6. **Watch Brownian paths**: Over 30–60 seconds, note how particles wander unpredictably. Some cluster close together while others drift apart. Occasional coordinated movements occur when the LFSR produces similar offsets for consecutive frames.
7. **Increase size**: Sweep Size toward maximum and observe overlapping glow fields creating brighter additive zones where particles converge.

**Key concepts**: Brownian drift produces meandering paths, Manhattan distance creates diamond-shaped glow, additive accumulation brightens at overlap

---

### Exercise 2: Bioluminescent Pulse

<img src={firefly_exercise2_result} alt="Bioluminescent Pulse result"/>
*Bioluminescent Pulse — simulated result across source images.*
**What You'll Create**: Add rhythmic pulse modulation to the particle field, creating a breathing, organic bioluminescent display that alternates between bright and dim states.

1. **Start from Exercise 1 settings**: Warm color, moderate size and brightness.
2. **Enable pulse**: Toggle Pulse to On. The entire field should begin a slow ~3.75 Hz blink.
3. **Increase brightness**: Raise Brightness to ~90%. During the bright phase, particles glow intensely. During the dim phase, they fade to half intensity — the contrast makes the pulse clearly visible.
4. **Increase size**: Set Size to ~60%. The larger glow fields make the pulsation more dramatic as substantial screen area alternates between bright and dim.
5. **Try cool palette**: Switch Color to Cool. The same pulse cadence now produces blue-cyan flashes reminiscent of deep-sea organisms.
6. **Reduce brightness**: Pull Brightness to ~50% and observe how the dim phase becomes nearly invisible while the bright phase remains present — more firefly-like, with distinct on/off character.

**Key concepts**: Pulse modulation creates rhythmic breathing, brightness controls on/off contrast ratio, color palette shapes emotional tone

---

### Exercise 3: Dense Cool Constellation

<img src={firefly_exercise3_result} alt="Dense Cool Constellation result"/>
*Dense Cool Constellation — simulated result across source images.*
**What You'll Create**: Maximize particle visibility by pushing size and brightness to their extremes, creating a dense field of overlapping cool-toned glows that fill the screen with luminous geometry.

1. **Switch to cool palette**: Set Color to Cool for blue-cyan tones.
2. **Maximize size**: Set Size to ~100%. Each particle now projects a very large diamond glow covering substantial screen area.
3. **High brightness**: Set Brightness to ~95%. Glow fields extend far from particle centers.
4. **Disable pulse**: Set Pulse to Off. Steady brightness allows observation of spatial structure.
5. **Observe saturation**: Where multiple large glow fields overlap, the additive accumulation clamps to 1023 — these zones appear as pure white against the cool-tinted surrounds. The number and location of white zones shifts as particles drift.
6. **Reduce size gradually**: Sweep Size down from maximum and watch the overlap zones shrink. At middle values, individual diamond shapes become clearly distinguishable. At minimum, only sparse bright points remain.
7. **Enable pulse**: Toggle Pulse On at maximum size. The alternating bright/dim phases cause the white saturation zones to appear and vanish rhythmically.

**Key concepts**: Additive accumulation creates saturation zones at overlap, Manhattan distance produces diamond geometry, size controls spatial density

---


## Tips

- **Use Cool palette for underwater scenes**: The blue-cyan tones combine beautifully with dark or blue-tinted input video to evoke deep-sea bioluminescence — anglerfish lures, jellyfish bells, dinoflagellate blooms.
- **Mix fader enables overlay compositing**: feeding a video source and reducing Mix to 30–50% creates a delicate particle overlay that adds depth and atmosphere without overwhelming the source content.
- **Extended observation reveals Brownian character**: The true beauty of Brownian motion emerges over minutes, not seconds. Let the program run and watch particles gradually explore the full screen area — occasionally clustering, occasionally dispersing, always drifting.
- **Bypass for A/B comparison**: When evaluating the particle overlay against source video, toggle Bypass On for an instant clean reference, then Off to see the composited result.
- **All particles drift together**: Because the LFSR provides a single offset for all particles per frame, the swarm moves in loose coordination. This produces a shoal-of-fish quality at short timescales that dissolves into independent randomness over longer periods.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bioluminescence** | The production and emission of light by living organisms, typically through the enzymatic oxidation of a luciferin substrate. Fireflies (family Lampyridae) are the most familiar terrestrial example. |
| **Brownian motion** | Random motion of particles resulting from collisions with surrounding molecules, first systematically observed by Robert Brown in 1827 and theoretically explained by Einstein in 1905. Characterized by a random walk where displacement grows as the square root of time. |
| **Clamping** | Restricting a computed value to a fixed range (here 0–1023) by replacing out-of-range results with the nearest boundary value. Prevents arithmetic overflow from producing visual artifacts. |
| **LFSR** | Linear Feedback Shift Register; a hardware-efficient pseudo-random number generator that produces a deterministic but statistically uniform bit sequence through XOR feedback taps. Firefly uses a 16-bit LFSR with taps at positions 15, 13, 12, and 10. |
| **Manhattan distance** | A distance metric defined as the sum of the absolute differences along each axis: $|dx| + |dy|$. Named after the grid-like street layout of Manhattan, where travel distance between two points is measured along right-angle paths. Produces diamond-shaped iso-distance contours. |
| **Particle system** | A computer graphics technique representing phenomena as collections of independent point masses, each with position and visual attributes. Firefly maintains 8 particles in register fabric with no frame buffer. |
| **Pulse modulation** | Periodic variation of signal amplitude. Firefly's pulse halves brightness every 8 frames at 60 Hz, producing a ~3.75 Hz on/off rhythm that mimics natural firefly flash patterns. |
| **Wrap-around** | Position arithmetic where values exceeding the screen boundary (1280×720) are reset to zero, causing particles to reappear at the opposite edge. A simple form of periodic boundary condition. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
