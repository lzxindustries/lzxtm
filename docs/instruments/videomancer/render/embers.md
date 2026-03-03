---
draft: true
sidebar_position: 97
slug: /instruments/videomancer/embers
title: "Embers"
image: /img/instruments/videomancer/embers/embers_hero.png
description: "Embers simulates a cascade of glowing sparks governed by Newtonian mechanics."
---

import embers_hero from '/img/instruments/videomancer/embers/embers_hero.png';
import embers_animation from '/img/instruments/videomancer/embers/embers_animation.gif';
import embers_control_panel from '/img/instruments/videomancer/embers/embers_control_panel.png';
import embers_exercise1_result from '/img/instruments/videomancer/embers/embers_exercise1_result.gif';
import embers_exercise2_result from '/img/instruments/videomancer/embers/embers_exercise2_result.gif';
import embers_exercise3_result from '/img/instruments/videomancer/embers/embers_exercise3_result.gif';

# Embers

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={embers_hero} alt="Embers hero image"/>
*Embers drifting upward from a dark field — eight simultaneous particle trajectories tracing arcs of white-hot light against the void.*
<img src={embers_animation} alt="Embers animated output"/>
*Embers output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Embers simulates a cascade of glowing sparks governed by Newtonian mechanics. Eight particles exist simultaneously, each carrying position, velocity, and a finite lifetime. On every vertical blanking interval the physics engine updates all eight particles in sequence — applying gravity, drag, and lifetime decay — then the rendering pipeline scans each pixel of the output frame, testing whether any living particle falls within range, computing brightness from distance and remaining life, mapping the result through a color palette, and compositing the glow additively over the input video.

The name evokes the incandescent fragments that spiral upward from a dying fire, their trajectories shaped by the interplay of buoyancy, gravity, and air resistance. In the digital domain these forces are reduced to their essentials: a signed velocity vector updated by a configurable gravitational constant, an optional 1/8-per-frame drag coefficient, and a monotonically decaying lifetime counter. The result is a sparse, luminous particle field that can range from a lazy upward drift of cooling sparks to a violent spray of white-hot projectiles — entirely determined by the six knobs and five toggles on the front panel.

Two emission modes offer fundamentally different creative starting points. Fountain mode spawns particles from the screen center with LFSR-randomised initial velocities, producing a self-contained pyrotechnic display that requires no input signal. Video mode seeds particles at bright pixels in the incoming video, turning the source image into a luminance-reactive emitter — highlights erupt into showers of sparks, while shadows remain inert. In both cases the particles obey the same physics and render through the same pipeline, blending seamlessly into a single visual vocabulary of light and motion.

---

## Background

### Particle Systems in Computer Graphics

The particle system is one of the foundational techniques of real-time computer graphics, introduced by William Reeves at Lucasfilm in 1983 for the Genesis sequence in *Star Trek II: The Wrath of Khan*. The core idea is to represent complex, amorphous phenomena — fire, smoke, water, sparks — not as geometric surfaces but as large populations of independent point masses, each with its own position, velocity, color, and lifetime. The visual effect emerges from the aggregate behavior of the swarm rather than the shape of any individual element. Embers distills this concept to its hardware-minimal form: eight particles maintained entirely in register fabric, with no frame buffer and no BRAM, making it one of the sparsest particle systems ever implemented in silicon.

### Newtonian Physics Simulation

Isaac Newton's second law — force equals mass times acceleration — is the engine behind every particle's trajectory. In Embers, each particle's velocity is updated once per frame by adding a gravitational acceleration vector (configurable in direction and magnitude) and optionally subtracting a drag term proportional to the current velocity. Position is then updated by adding the new velocity. This Euler integration scheme is the simplest possible discretization of Newton's equations: it accumulates small errors over time, but for short-lived particles in a visual context, the approximation is indistinguishable from exact solutions. The signed 9-bit velocity representation allows particles to travel in any direction, while the saturating 12-bit position arithmetic prevents wrap-around at frame boundaries.

### Scanline Rendering and Distance Fields

Traditional particle renderers use frame buffers and alpha blending to accumulate the visual contribution of each particle. Embers takes a different approach dictated by the streaming nature of the FPGA video pipeline: rather than drawing particles into a buffer, the renderer tests every pixel against all eight particles simultaneously, computing the Chebyshev distance (the maximum of the absolute horizontal and vertical offsets) from the pixel to each particle center. If the distance falls within the particle's radius, a brightness value is generated that falls off with distance and scales with remaining lifetime. The brightest overlapping particle wins. This technique eliminates the need for any pixel memory — the entire rendering computation is purely combinatorial, evaluated fresh for every pixel in real time.

### Fire and Ember Aesthetics

The visual language of fire is deeply embedded in human perception. Psychophysical research has established that the progression from deep red through orange to yellow-white closely tracks the blackbody radiation curve — the same sequence that a heated metal object follows as its temperature rises. Embers exploits this association through its white-hot color palette, which maps high brightness to neutral white (achromatic in YUV), moderate brightness to warm orange (reduced U, elevated V), and low brightness to deep red (strongly elevated V, suppressed U). The result triggers an immediate perceptual association with incandescence, even though the underlying computation is a simple piecewise linear function in the chroma domain.

### Video-Reactive Art and Luminance Thresholding

The Video emission mode bridges the gap between autonomous synthesis and input-dependent processing. By spawning particles only at pixels where the input luma exceeds a fixed threshold (midpoint, Y > 512), Embers converts the brightness contours of the source image into a spatial probability map for particle generation. Bright regions become fountains of sparks; dark regions remain dormant. This technique belongs to a broader tradition of video-reactive art — work in which the source signal actively shapes the generative output rather than merely being overlaid. The effect is bidirectional: the source image determines where sparks appear, and the sparks in turn modify the composite image through additive blending, creating a feedback-friendly loop when the output is routed back to the input.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Clock 0: Register Decode ──────────────────────────────────
│   ├─ emit_rate   = registers_in(0)     [10-bit]
│   ├─ gravity     = registers_in(1)     [10-bit]
│   ├─ velocity    = registers_in(2)     [10-bit]
│   ├─ lifetime    = registers_in(3)     [10-bit]
│   ├─ size        = registers_in(4)     → particle_size [1–8]
│   ├─ spread      = registers_in(5)     [10-bit]
│   ├─ brightness  = registers_in(7)     [10-bit]
│   └─ toggles from registers_in(6):
│       ├─ bit 0: emit_mode (0=fountain, 1=video)
│       ├─ bit 1: grav_dir  (0=down, 1=up)
│       ├─ bit 2: drag_en   (0=off, 1=on)
│       ├─ bit 3: color_mode(0=hot, 1=rainbow)
│       └─ bit 4: bypass
│
├── LFSR16 Instance ──────────────────────────────────────────
│   └─ lfsr16(seed=0xCAFE) → 16-bit pseudo-random stream
│
├── Position Counters ────────────────────────────────────────
│   ├─ h_count: 12-bit horizontal pixel counter
│   └─ v_count: 12-bit vertical line counter
│
├── Physics Update (per vblank, 8 sequential clocks) ─────────
│   For each particle i = 0..7:
│   ├─ Gravity: grav = gravity[9:6] signed; negate if grav_dir
│   ├─ Velocity: vy += grav
│   ├─ Drag (if enabled): vx -= vx>>>3; vy -= vy>>>3
│   ├─ Clamp vx, vy to [-128..+127]
│   ├─ Position: px += vx; py += vy  (saturating 12-bit)
│   └─ Lifetime: life -= 4  (clamp to 0)
│
├── Emission (concurrent with scan) ──────────────────────────
│   If emit_counter < emit_rate AND life[emit_idx] == 0:
│   ├─ Fountain: px=960, py=540 (screen center)
│   ├─ Video: px=h_count, py=v_count (if input Y > 512)
│   ├─ vx = lfsr[7:0] × spread[9:6] >> 3  (signed, spread-scaled)
│   ├─ vy = -velocity[9:3]  (upward initial impulse)
│   └─ life = lifetime parameter
│
├── Rendering Pipeline (per pixel, combinatorial) ────────────
│   For each particle i with life > 0:
│   ├─ dx = h_count − px(i);  dy = v_count − py(i)
│   ├─ abs_dx, abs_dy
│   ├─ Chebyshev: radius = max(abs_dx, abs_dy)
│   ├─ if radius ≤ particle_size:
│   │   ├─ bright = (size − radius) << shift  (distance falloff)
│   │   └─ bright = bright × life >> 10  (lifetime scale)
│   └─ best_bright = max over all particles
│
├── Color Mapping ────────────────────────────────────────────
│   ├─ pixel_bright = best_bright × brightness >> 10
│   ├─ Hot mode:
│   │   ├─ bright > 768: white  (Y=bright, U=512, V=512)
│   │   ├─ bright > 384: orange (Y=bright, U=512−bright>>3, V=512+bright>>2)
│   │   └─ else:         red    (Y=bright, U=512−bright>>2, V=512+bright>>1)
│   └─ Rainbow mode:
│       └─ Y=bright, U=512+bright>>2, V=512−bright>>2
│
├── Additive Composite ──────────────────────────────────────
│   comp_y = lerp10(input_y, color_y, pixel_bright)
│   comp_u = lerp10(input_u, color_u, pixel_bright)
│   comp_v = lerp10(input_v, color_v, pixel_bright)
│
├── Sync Pipeline (8-stage delay) ────────────────────────────
│   └─ hsync_n, vsync_n, avid, field_n delayed 8 clocks
│
└── Bypass Mux ──────────────────────────────────────────────
    └─ bypass ? input : composite
```

The physics engine and rendering pipeline occupy two distinct temporal domains. Physics updates run during the vertical blanking interval — a narrow window of approximately 45 lines at HD rates — processing one particle per clock in a simple sequential loop. This avoids any contention with the rendering pipeline, which runs during the active video region and must evaluate all eight particles in parallel for every pixel. The rendering stage is fully combinatorial within each clock: eight distance comparisons, eight brightness computations, and a maximum-brightness selector all resolve in a single pipeline stage. This dual-domain architecture allows Embers to maintain a consistent 8-clock total latency regardless of particle count, with zero BRAM and minimal DSP usage.

The emission system runs concurrently with the scanning process. A free-running counter compared against the Emit Rate parameter determines how frequently new particles are spawned. When a spawn opportunity arises, the engine checks whether the currently indexed particle slot is dead (lifetime = 0) and, if so, initializes it with position, velocity, and lifetime values. The LFSR provides randomness for horizontal velocity; the Spread parameter scales this random component to control the angular dispersion of the emission cone. In Video mode, the additional requirement that the input luma exceed the midpoint threshold gates emission spatially, coupling the particle density to the brightness structure of the incoming video.

---

## Parameter Reference

<img src={embers_control_panel} alt="Videomancer front panel with Embers loaded"/>
*Videomancer's front panel with Embers active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Emit Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls how frequently new particles are emitted. At minimum, no new particles are spawned and the existing population gradually dies out, leaving a dark screen. At maximum, every available dead particle slot is re-spawned as quickly as possible, producing a dense, continuous stream. The emission rate interacts with the Lifetime parameter to determine the steady-state particle count: high emission with short lifetime produces a rapid turnover of brief sparks, while moderate emission with long lifetime fills the screen with persistent, slowly fading trails. In Video mode, a high emission rate causes rapid response to bright regions in the source — highlights erupt almost instantly into showers of sparks.

---

#### Knob 2 — Gravity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the magnitude of gravitational acceleration applied to each particle's vertical velocity on every frame. At zero, particles drift in straight lines determined solely by their initial velocity and drag. As gravity increases, trajectories curve into parabolic arcs — the classic shape of a projectile under constant acceleration. The gravity direction toggle determines whether particles are pulled downward (simulating falling embers) or upward (simulating rising sparks and hot gas). At maximum gravity, particles accelerate rapidly and exit the frame within a few frames of emission, producing short, sharp streaks rather than graceful arcs.

---

#### Knob 3 — Velocity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Determines the magnitude of the initial upward velocity given to each newly emitted particle. At zero, particles are born stationary and immediately begin falling under gravity (if enabled) — a dripping or pooling effect. At maximum, particles launch with a strong upward impulse, reaching considerable height before gravity curves them back down. The interaction between Velocity and Gravity defines the apex height of the parabolic trajectory: high velocity with low gravity produces tall, lazy arcs, while matched velocity and gravity produces tight, energetic bounces. The initial vertical velocity is always directed upward (negative in screen coordinates); horizontal velocity comes from the LFSR-driven random component scaled by Spread.

---

#### Knob 4 — Lifetime
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Sets the initial lifetime counter for newly spawned particles. Lifetime decrements by 4 units per frame, so the maximum duration at full setting is approximately 256 frames (~4.3 seconds at 60 Hz). At minimum, particles expire almost immediately — they appear as momentary flashes with no visible trajectory. At maximum, particles persist long enough to complete full parabolic arcs and fade gradually from bright white through orange to deep red (in Hot color mode), producing long, graceful trails. Lifetime also scales particle brightness through the rendering pipeline: a particle at half its initial lifetime renders at half brightness, creating a natural fade-out that mimics the cooling of a real ember.

---

#### Knob 5 — Size
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

Controls the rendering radius of each particle in pixels, ranging from 1 (single-pixel points) to 8 (16×16-pixel squares rendered via Chebyshev distance). Small sizes produce a field of precise, star-like points that emphasize the trajectories and physics behavior. Large sizes produce soft, glowing blobs where brightness falls off from center to edge, creating a more diffuse, atmospheric effect. The distance falloff within the particle is inversely proportional to the size — larger particles have gentler gradients, while smaller particles are nearly uniform in brightness across their extent. Size interacts strongly with the visual density: eight particles at Size 1 are sparse pinpoints, but at Size 8 they can overlap to fill significant screen area.

---

#### Knob 6 — Spread
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scales the horizontal component of the random initial velocity assigned to each new particle. At zero, all particles are emitted straight up (or straight down, depending on gravity direction) with no lateral dispersion — a narrow column of sparks. At maximum, the LFSR-derived horizontal velocity is amplified to its full range, producing a wide cone of emission that sprays particles across the full width of the frame. The Spread parameter directly maps to the visual cone angle of the particle fountain: narrow spread mimics a candle flame, while wide spread resembles a Roman candle or burst firework. In Video mode, spread determines how far particles wander from their emission point on the source image.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Emit Mode** | Fountain | Video |
| **8 — Gravity Dir** | Down | Up |
| **9 — Drag** | Off | On |
| **10 — Color** | Hot | Rainbow |
| **11 — Bypass** | Off | On |

Toggles 7–10 configure four independent binary aspects of the particle system. Emit Mode (7) selects between autonomous fountain synthesis and video-reactive emission. Gravity Dir (8) flips the gravitational vector, transforming falling ash into rising sparks. Drag (9) enables atmospheric resistance that curves trajectories and slows particles over time. Color (10) switches between the thermodynamic white-hot palette and a chromatic rainbow mapping. Each toggle affects a distinct stage of the pipeline — emission, physics, rendering, and color respectively — so all sixteen combinations produce meaningfully different visual results. Toggle 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Global brightness multiplier applied to the final particle brightness before color mapping and compositing. At maximum, particles render at full intensity — the brightest cores saturate to white in Hot mode. At zero, all particle contribution is suppressed and only the input video passes through. Intermediate values scale the overall luminosity of the particle field, useful for matching the intensity of the ember overlay to the brightness range of the source video. This control acts as the master intensity for the entire particle system, distinct from the per-particle lifetime-based fade.

---

## Guided Exercises

These exercises progress from a basic centered fountain through physics-driven trajectory sculpting to video-reactive emission. Each reveals a different facet of the particle system and its interaction with Newtonian mechanics.

### Exercise 1: Classic Fountain

<img src={embers_exercise1_result} alt="Classic Fountain result"/>
*Classic Fountain — simulated result across source images.*
**Objective**: Create a steady upward fountain of white-hot sparks from the screen center, exploring how gravity and velocity shape the parabolic trajectory envelope.

1. **Set Fountain mode**: Ensure Emit Mode is Fountain. Particles spawn from screen center.
2. **Establish baseline**: Set Emit Rate to ~50%, Velocity to ~50%, Gravity to ~25%, Lifetime to ~75%. A steady stream of sparks should arc upward and fall back.
3. **Adjust gravity**: Increase Gravity and observe trajectories tighten into sharper arcs. Decrease toward zero and watch particles drift in nearly straight lines.
4. **Flip gravity direction**: Toggle Gravity Dir to Up. The fountain now accelerates upward — particles launch and continue to climb, exiting the top of frame.
5. **Enable drag**: Toggle Drag On. Trajectories curve more tightly, and particles cluster near the center rather than scattering to frame edges.
6. **Adjust spread**: Sweep Spread from 0% (narrow column) to 100% (wide spray) and observe the cone angle of the fountain.

**Key concepts**: Gravity shapes trajectory curvature, Velocity sets launch height, Drag dampens scatter, Spread controls emission cone angle

---

### Exercise 2: Slow Ember Drift

<img src={embers_exercise2_result} alt="Slow Ember Drift result"/>
*Slow Ember Drift — simulated result across source images.*
**Objective**: Create large, slowly fading embers with minimal physics, emphasizing the lifetime-brightness relationship and the white-hot color gradient.

1. **Reduce emission**: Set Emit Rate to ~20% for sparse, well-separated particles.
2. **Maximize lifetime**: Set Lifetime to ~100%. Particles will persist for several seconds.
3. **Minimize velocity and gravity**: Velocity ~15%, Gravity ~5%. Particles barely move after emission.
4. **Increase size**: Set Size to ~7 for large, soft glowing orbs.
5. **Observe color fade**: Watch individual particles transition from white through orange to deep red as their lifetime depletes — the incandescence curve in action.
6. **Try Rainbow**: Toggle Color to Rainbow. The same fade now cycles through chromatic hues instead of the thermal gradient.
7. **Reduce brightness**: Pull Brightness to ~60% to dim the cores and extend the visible color range of the fade.

**Key concepts**: Lifetime drives brightness falloff, white-hot palette mimics blackbody radiation, large Size creates soft glow, low physics emphasizes color evolution

---

### Exercise 3: Video-Reactive Sparks

<img src={embers_exercise3_result} alt="Video-Reactive Sparks result"/>
*Video-Reactive Sparks — simulated result across source images.*
**Objective**: Use Video emission mode to generate sparks at bright regions of the input signal, creating a luminance-reactive particle overlay that responds to the source content.

1. **Switch to Video mode**: Toggle Emit Mode to Video. Particles now spawn at bright pixels in the source.
2. **Feed a high-contrast source**: Use footage with distinct bright highlights — candle flames, spotlights, bright text on dark backgrounds.
3. **High emission rate**: Set Emit Rate to ~80% to ensure rapid response to bright regions.
4. **Configure upward drift**: Gravity ~15% with Gravity Dir Up, Velocity ~40%. Sparks rise from highlights.
5. **Enable drag**: Drag On. Particles cluster near their emission points rather than scattering.
6. **Moderate size**: Size ~4 for visible but not overwhelming particle globs.
7. **Observe interaction**: Bright regions in the video should erupt into fountains of sparks that drift upward and fade. Moving highlights produce trailing particle streams.

**Key concepts**: Video mode couples emission to source luma, particles trace highlight motion, additive compositing creates glow around bright features

---


## Tips

- **Start with drag enabled**: The default drag-on setting keeps particles clustered near the emission source, making the fountain visible and controllable. Disable drag only when you want long-range scatter across the full frame.
- **Gravity direction sets the mood**: Downward gravity produces melancholy, descending ash. Upward gravity produces energetic, ascending sparks. Try zero gravity for drifting, nebula-like particle clouds.
- **Size 1 for precision, Size 8 for atmosphere**: Single-pixel particles reveal the pure physics — every trajectory is a clean arc. Large particles create a soft, glowing haze where individual trajectories blur into a luminous field.
- **Video mode loves high contrast**: For the strongest video-reactive effect, feed Embers a source with distinct bright highlights on a dark background. The luma threshold at Y=512 means mid-gray and darker regions produce no particles.
- **Lifetime and emission rate define density**: Short lifetime with high emission gives rapid sparkle. Long lifetime with low emission gives a sparse, slowly evolving constellation. Balance the two for the desired visual density.
- **Hot palette at low brightness reveals the red end**: Pull the Brightness fader to 50–70% to expose the full orange-to-red gradient of the incandescence curve. At full brightness the white core dominates.
- **Feedback creates particle avalanches**: Route the output back to the input in Video mode. Each frame's bright particles become the next frame's emission triggers, creating cascading chains of sparks that propagate across the frame.
- **Combine with dark sources for pure synthesis**: Feed a black video signal and use Fountain mode to treat Embers as a standalone particle generator. The additive compositing over black produces clean, isolated spark trails ideal for overlay compositing downstream.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive compositing** | A blending technique where particle brightness is added to the source video rather than replacing it, preserving the original image while layering luminous elements on top. |
| **Blackbody radiation** | The spectrum of light emitted by an idealized heated object, progressing from red through orange and yellow to white as temperature increases; the basis for the Hot color palette. |
| **Chebyshev distance** | A distance metric defined as the maximum of the absolute differences along each axis: max(|dx|, |dy|). Produces square-shaped iso-distance contours rather than circular ones. |
| **Drag coefficient** | A damping factor applied to particle velocity on each frame, simulating air resistance. Embers uses a fixed 1/8 reduction per frame when drag is enabled. |
| **Euler integration** | The simplest numerical method for solving differential equations: new_position = position + velocity × dt. Used here with dt = 1 frame. |
| **Lerp** | Linear interpolation between two values: result = a + (b − a) × t. Used in the additive compositing stage to blend particle color with the source video. |
| **LFSR** | Linear Feedback Shift Register; a hardware-efficient pseudo-random number generator using XOR feedback taps. Embers uses a 16-bit maximal-length LFSR seeded at 0xCAFE. |
| **Particle system** | A computer graphics technique representing complex phenomena as collections of independent point masses, each with position, velocity, lifetime, and visual attributes. |
| **Register file** | A set of flip-flop registers (as opposed to BRAM) used to store particle state. Embers maintains all 8 particles in registers, consuming zero block RAM. |
| **Saturating arithmetic** | Integer arithmetic that clamps at the minimum and maximum representable values rather than wrapping around. Used for position updates to prevent particles from teleporting across frame boundaries. |
| **YUV** | A color space separating luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer video processing pipeline. |


---
