---
draft: true
sidebar_position: 178
slug: /instruments/videomancer/lorenz
title: "Lorenz"
image: /img/instruments/videomancer/lorenz/lorenz_hero.png
description: "In 1963, meteorologist Edward Lorenz was running a simplified weather simulation on a Royal McBee LGP-30 computer."
---

![Lorenz hero image](/img/instruments/videomancer/lorenz/lorenz_hero_s1.png)
*Lorenz rendering its strange attractor as a glowing phosphor trace, the butterfly-shaped trajectory drifting across a field of decaying light.*

---

## Overview

Lorenz is a real-time chaotic system visualizer that computes the famous Lorenz attractor inside the FPGA and draws its trajectory as a persistent, glowing trace on the screen. The attractor's path is plotted onto a small canvas stored in block RAM, and every frame that canvas fades slightly: producing the look of a phosphor oscilloscope display. The result is a butterfly-wing shape that wanders, stretches, and collapses depending on three mathematical parameters exposed as knobs on the front panel. Lorenz is a ***synthesis*** program: it generates imagery from scratch and can either replace the input video entirely or overlay its glowing trace on top of whatever you feed in.

At its default settings, Lorenz produces a slowly evolving green trace against a dark background. Adjusting the three system parameters: **Sigma**, **Rho**, and **Beta**: reshapes the attractor from tight spirals to wide, chaotic orbits. Push the parameters far enough and the system collapses to a fixed point; pull them back and it blooms into the classic double-lobed butterfly.

:::tip
Lorenz is one of the few Videomancer programs that performs ***numerical simulation*** on the FPGA. The trajectory you see is computed step by step using the actual Lorenz differential equations (it's genuine chaos, not an approximation or a recording.)
:::

### What's In a Name?

The program is named after ***Edward Lorenz***, the American meteorologist who discovered the Lorenz attractor in 1963 while studying simplified models of atmospheric convection. His work revealed that deterministic systems can behave unpredictably: a discovery that helped launch the field of ***chaos theory***. The butterfly-shaped trajectory of the Lorenz system became one of the most recognized images in mathematics and is closely associated with the phrase "the butterfly effect."

---

## Quick Start

1. Turn **Sigma** (Knob 1) and **Rho** (Knob 2) to roughly their midpoints. A glowing butterfly-shaped trace should appear on screen, slowly wandering between its two lobes.
2. Increase **StepSpd** (Knob 4) clockwise. The trace moves faster, drawing more of the attractor each frame and filling in the butterfly shape more densely.
3. Decrease **Decay** (Knob 5) toward its minimum. The phosphor trails linger much longer, building up a bright, persistent image of the full attractor.
4. Toggle **Proj** (Switch 7) from X-Y to X-Z to see the attractor from a different angle (the familiar butterfly rotates into a side view.)

---

## Parameters

![Videomancer front panel with Lorenz loaded](/img/instruments/videomancer/lorenz/lorenz_control_panel.png)
*Videomancer's front panel with Lorenz active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Sigma

| Property | Value |
|----------|-------|
| Range | 0 – 40 |
| Default | 10 |

**Sigma** controls the first parameter of the Lorenz system, traditionally called σ (sigma). This value governs the rate of coupling between the X and Y state variables: in fluid dynamics terms, it represents the ***Prandtl number***. At low values the attractor shrinks and the trajectory may collapse to a single point or a small loop. Near the classic value of about 10 (roughly 25% on the knob), the familiar double-lobed butterfly appears. Higher values stretch the attractor horizontally, making the two wings wider and the transitions between them more abrupt.

---

### Knob 2 — Rho

| Property | Value |
|----------|-------|
| Range | 0 – 50 |
| Default | 28 |

**Rho** controls the second parameter, traditionally called ρ (rho), which represents the ***Rayleigh number***: the driving force of the convective system. This is the most dramatic control. Below a critical threshold (around Rho 24), the system settles into a stable fixed point and the trace stops moving. Above that threshold the trajectory becomes chaotic, looping unpredictably between two attracting regions. Increasing Rho further makes the loops taller and wilder. This knob is essentially the "chaos dial": sweep it slowly and watch the system transition from calm to turbulent.

:::note
The transition from order to chaos happens at a specific critical value of Rho. You can watch this ***bifurcation*** happen live: sweep the knob slowly from low to high and notice the exact moment the trace stops settling and begins to wander.
:::

---

### Knob 3 — Beta

| Property | Value |
|----------|-------|
| Range | 0 – 10 |
| Default | 3 |

**Beta** controls the third Lorenz parameter, traditionally called β (beta), which describes how quickly the rotational energy dissipates in the convective model. Lower values allow the system to sustain larger orbits; higher values compress the attractor vertically. The effect is subtler than Sigma or Rho, but Beta shapes the overall proportions of the butterfly (it controls how "tall" each wing is relative to its width.)

---

### Knob 4 — StepSpd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**StepSpd** (Step Speed) sets how many integration steps the FPGA computes during each horizontal blanking interval. At low values the attractor trace crawls slowly, drawing just a few new points per frame. At higher values the integrator runs many more steps per blanking period, and the trace races along the attractor's path. Because the trajectory is plotted onto a persistent canvas, faster step speeds fill in the attractor shape more quickly, building up a dense, complete portrait.

:::tip
Very high step speeds combined with low decay produce a bright, fully-drawn attractor. Very low step speeds combined with high decay show just a single glowing dot wandering through space: a moving point of light tracing out the chaotic orbit in real time.
:::

---

### Knob 5 — Decay

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Decay** controls how quickly the phosphor trace fades. At minimum (fully counterclockwise), the canvas barely fades at all: old trace points persist almost indefinitely, building up a bright, dense image of the full attractor shape. At maximum (fully clockwise), old points vanish almost immediately, leaving only the most recently plotted portion of the trajectory visible as a short, glowing tail. The decay operates in four discrete steps: each frame, every canvas pixel is reduced by 0, 1, 2, or 3 brightness levels depending on the knob position.

---

### Knob 6 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Bright** (Brightness) scales the intensity of the attractor trace when it is composited onto the output. At low values the trace is dim and ghostly. At high values the trace becomes a bright, vivid overlay that dominates the image. This control does not affect the internal canvas: it only scales the brightness during the final display stage, so changing it does not alter the decay behavior or the attractor's evolution.

---

### Switch 7 — Proj

| Property | Value |
|----------|-------|
| Off | X-Y |
| On | X-Z |
| Default | X-Y |

**Proj** (Projection) selects which two of the three Lorenz state variables map to the screen axes. In the **X-Y** position, the horizontal axis shows the X variable and the vertical axis shows Y. This is the classic butterfly view. In the **X-Z** position, the vertical axis switches to the Z variable, showing the attractor from a different angle: the butterfly appears to rotate, revealing the vertical extent of the orbits. The X-Z projection emphasizes the system's vertical structure and the separation between the two lobes.

---

### Switch 8 — Color

| Property | Value |
|----------|-------|
| Off | Phosphor |
| On | Rainbow |
| Default | Phosphor |

**Color** selects between two colorization modes for the attractor trace. In **Phosphor** mode, the trace is rendered in a cool green tint reminiscent of a classic oscilloscope display: the U and V channels are both set below midpoint, producing a muted green. In **Rainbow** mode, the trace color cycles through four hue phases based on the canvas pixel's brightness level, producing a multicolored trail where recently plotted (bright) points appear in a different hue than decaying (dim) points.

:::tip
Rainbow mode is most visible at moderate decay rates, where you can see the color shift as points fade from bright to dim. With very low decay, most pixels stay at maximum brightness and the rainbow effect is less pronounced.
:::

---

### Switch 9 — Perturb

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Perturb** enables periodic perturbation of the Lorenz system. When set to **On**, every 128 frames the integrator gives the X variable a sudden kick, adding a fixed offset to its value. This nudge pushes the trajectory off its current orbit, causing it to snap to the other lobe or explore a different region of phase space. The effect is intermittent: the system settles into its natural behavior between kicks, then suddenly jumps. When set to **Off**, the attractor evolves purely from its mathematical dynamics with no external disturbance.

---

### Switch 10 — Compose

| Property | Value |
|----------|-------|
| Off | Overlay |
| On | Replace |
| Default | Overlay |

**Compose** selects how the attractor trace is combined with the input video. In **Overlay** mode, the trace brightness is added to the incoming video: the attractor appears as a luminous drawing on top of the source material, and the original image remains visible beneath it. In **Replace** mode, the attractor trace completely replaces the input video: you see only the trace against a black background, like an oscilloscope screen.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Lorenz processing. The sync delay pipeline still aligns timing. Use Bypass for instant A/B comparison between the source and the attractor-composited output.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (attractor-composited) output. At 0% the output is entirely dry: pure input video with no trace. At 100% the output is entirely wet: the full attractor composite. Intermediate positions blend the two, allowing subtle ghost-like traces overlaid on a mostly-clean signal.

---

## Background

### Chaos Theory and the Lorenz System

In 1963, Edward Lorenz was running a simplified weather simulation on a Royal McBee computer when he noticed something strange. Re-entering initial conditions with slightly rounded numbers produced wildly different results. The tiny rounding error: less than one part in a thousand: amplified into a completely different weather pattern. This observation became the foundation of ***chaos theory***: the discovery that deterministic systems can exhibit unpredictable behavior when their evolution is ***sensitive to initial conditions***.

The mathematical system Lorenz studied is a set of three coupled ***ordinary differential equations***:

- dx/dt = σ(y − x)
- dy/dt = x(ρ − z) − y
- dz/dt = xy − βz

These three equations describe a simplified model of atmospheric convection. The variables x, y, and z represent the state of the convection cell, and the parameters σ (sigma), ρ (rho), and β (beta) control how the fluid behaves. For certain parameter values: most famously σ = 10, ρ = 28, β = 8/3: the system never settles into a repeating pattern. Instead, the trajectory wanders endlessly between two regions of phase space, tracing out the double-lobed shape known as the ***strange attractor***.

### Fixed-Point Numerical Integration

The FPGA implements the Lorenz equations using ***Euler integration*** in ***fixed-point arithmetic***. Each state variable (x, y, z) is stored as a signed 16-bit number in 6.10 format: six bits for the integer part, ten bits for the fractional part. This gives a range of roughly −32 to +31 with a precision of about 0.001.

Each integration step computes the three derivatives (dx, dy, dz) using three signed multiplications, then adds a scaled fraction of the derivative to each state variable. The step size is effectively 1/1024, matching the fixed-point scale. Multiple integration steps run during each horizontal blanking interval, when the video signal carries no active picture data: this means the integrator runs "for free" in time that would otherwise be wasted.

### Phosphor Persistence

The canvas uses a 64×64 grid of 4-bit pixels stored in block RAM. Each pixel can hold a brightness value from 0 (off) to 15 (maximum). When the integrator plots a point, it sets the corresponding canvas cell to maximum brightness. Every frame, a ***decay pass*** sweeps through the entire canvas and decreases each cell by a fixed amount: the rate controlled by the **Decay** knob. Points that are not refreshed eventually fade to zero.

This two-pass approach: plotting new points at full brightness, then uniformly decaying the whole canvas: produces the ***phosphor persistence*** effect familiar from cathode-ray oscilloscopes. The most recently visited parts of the attractor glow brightest, while the trajectory's history fades into a dim afterimage.


---

## Signal Flow

### Signal Flow Notes

The integrator and the display pipeline run in different phases of the video signal. During ***horizontal blanking***: the brief interval between each line of active picture: the Lorenz equations are iterated and new points are plotted onto the canvas. During ***active video***, the canvas is read and composited with the input signal. This separation means the two processes never contend for the BRAM simultaneously (except during the decay pass, which runs at the start of each frame using a two-phase read-then-write scan).

The canvas is much smaller than the screen (64×64 versus approximately 1920×1080), so each canvas pixel covers a large block of screen pixels. The trace therefore appears as a coarse, blocky shape: which actually reinforces the lo-fi phosphor aesthetic. The projection step maps the signed, fixed-point attractor coordinates into unsigned canvas coordinates, centering the attractor in the grid.

:::note
Because the integrator uses fixed-point arithmetic with limited precision, the FPGA's Lorenz system is not an exact replica of the continuous equations. The discretization introduces small numerical drift: but for a chaotic system, any tiny perturbation leads to divergent trajectories regardless. The visual result is indistinguishable from a higher-precision simulation.
:::


---

## Exercises

These exercises explore the Lorenz attractor from stable equilibrium through full chaos, then combine it with input video for live performance compositing.
### Exercise 1: Finding the Butterfly

![Finding the Butterfly result](/img/instruments/videomancer/lorenz/lorenz_ex1_s1.png)
*Finding the Butterfly — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Discover the classic butterfly-shaped strange attractor by sweeping the Rho parameter through the critical transition from stability to chaos.

#### Key Concepts

- The Lorenz attractor emerges from specific parameter relationships
- The Rho parameter controls the transition from order to chaos
- Decay rate determines whether you see the trajectory's history or only its present

#### Steps

1. Set **Sigma** (Knob 1) to about 25% and **Beta** (Knob 3) to about 27%. These approximate the classic values σ ≈ 10 and β ≈ 8/3.
2. Set **Rho** (Knob 2) to its minimum. The trace should settle to a fixed point (a single dot or a tiny loop.)
3. Set **Decay** (Knob 5) to about 25% so the trace lingers, and **Bright** (Knob 6) to about 75%.
4. Set **Compose** (Switch 10) to **Replace** so the attractor fills the screen against a black background.
5. Now slowly sweep **Rho** clockwise. Watch the transition: the dot begins to orbit, the orbits grow, and at a critical point the trajectory suddenly begins visiting two separate lobes (the butterfly appears.)
6. Toggle **Proj** (Switch 7) to **X-Z** to see the same attractor from its side profile.

#### Settings

| Control | Value |
|---------|-------|
| Sigma | ~25% |
| Rho | Sweep from 0 to 100 |
| Beta | ~27% |
| StepSpd | ~50% |
| Decay | ~25% |
| Bright | ~75% |
| Proj | X-Y |
| Color | Phosphor |
| Perturb | Off |
| Compose | Replace |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Phosphor Trails in Rainbow

![Phosphor Trails in Rainbow result](/img/instruments/videomancer/lorenz/lorenz_ex2_s1.png)
*Phosphor Trails in Rainbow — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Create a colorful, long-exposure trace of the chaotic orbit with rainbow coloring that reveals the trajectory's age.

#### Key Concepts

- Decay rate shapes the visual density of the trace
- Color mode maps brightness to hue, creating gradient trails
- Step speed controls how quickly the attractor fills in

#### Steps

1. Start from the butterfly discovered in Exercise 1 (Sigma ~25%, Rho ~55%, Beta ~27%).
2. Switch **Color** (Switch 8) to **Rainbow**. The trace shifts from monochrome green to a cycling palette.
3. Lower **Decay** (Knob 5) to near minimum. Old trace points linger and fade through different colors as their brightness decreases.
4. Increase **StepSpd** (Knob 4) to about 70%. The attractor fills in more quickly, building a dense multicolored portrait.
5. Now slowly adjust **Sigma** (Knob 1) and **Beta** (Knob 3) while watching the rainbow trails reshape. The attractor's proportions change (wider wings, tighter spirals, or collapse.)
6. Enable **Perturb** (Switch 9). Every few seconds the trace receives a sudden kick, causing it to jump between lobes unexpectedly, leaving colorful arcs across the canvas.

#### Settings

| Control | Value |
|---------|-------|
| Sigma | ~25% |
| Rho | ~55% |
| Beta | ~27% |
| StepSpd | ~70% |
| Decay | ~5% |
| Bright | ~75% |
| Proj | X-Y |
| Color | Rainbow |
| Perturb | On |
| Compose | Replace |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Chaos Over Video

![Chaos Over Video result](/img/instruments/videomancer/lorenz/lorenz_ex3_s1.png)
*Chaos Over Video — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Layer the Lorenz attractor on top of a live video source as a glowing animated overlay, blending mathematics and imagery.

#### Key Concepts

- Overlay mode adds the attractor trace to live video
- Mix crossfades between the clean source and the composited output
- The attractor can serve as a live animated overlay element

#### Video Source

A live camera feed or recorded footage: darker scenes work best, as the additive overlay shows most clearly against low-luminance backgrounds.

#### Steps

1. Connect a video source to Videomancer's input.
2. Set **Compose** (Switch 10) to **Overlay**. The trace now adds to the incoming video rather than replacing it.
3. Set **Bright** (Knob 6) to about 60% so the trace is visible but not overwhelming.
4. Set **Mix** (Fader 12) to about 70%. The source image is partially visible beneath the attractor.
5. Set the system parameters for a lively attractor: **Sigma** ~25%, **Rho** ~55%, **Beta** ~27%, **StepSpd** ~50%.
6. Set **Decay** (Knob 5) to about 50%: a moderate trail length that shows motion without obscuring the video.
7. Switch **Color** (Switch 8) between **Phosphor** and **Rainbow** to see which colorization suits your source material.
8. Slowly sweep **Rho** (Knob 2) to animate the attractor's behavior over the video (from calm orbits to wild chaos.)

#### Settings

| Control | Value |
|---------|-------|
| Sigma | ~25% |
| Rho | ~55% |
| Beta | ~27% |
| StepSpd | ~50% |
| Decay | ~50% |
| Bright | ~60% |
| Proj | X-Y |
| Color | Phosphor |
| Perturb | Off |
| Compose | Overlay |
| Bypass | Off |
| Mix | ~70% |

---
## Glossary

- **Attractor**: A set of states toward which a dynamical system tends to evolve; the Lorenz attractor is a "strange" attractor because it never repeats.

- **Bifurcation**: A qualitative change in a system's behavior as a parameter crosses a critical threshold: such as the transition from a stable fixed point to chaotic orbiting.

- **BRAM**: Block RAM; dedicated memory tiles built into the FPGA fabric, used here to store the 64×64 canvas.

- **Chaos**: Deterministic behavior that appears random because infinitesimally small differences in initial conditions lead to vastly different outcomes.

- **Euler Integration**: The simplest numerical method for solving differential equations, advancing the solution by adding the derivative scaled by a small time step.

- **Fixed-Point Arithmetic**: A method of representing fractional numbers using integers with an implied binary decimal point, used on hardware that lacks floating-point units.

- **Phase Space**: An abstract space where each axis represents one state variable of a dynamical system; the trajectory through this space shows the system's evolution.

- **Phosphor Persistence**: The tendency of a phosphor-coated screen (as in a CRT or oscilloscope) to continue glowing briefly after the electron beam moves on, leaving a fading trail.

- **Projection**: Selecting which two of three (or more) state variables are mapped to the horizontal and vertical screen axes, choosing the "viewing angle" of the phase portrait.

- **Strange Attractor**: An attractor with a fractal structure that produces chaotic trajectories: the system is drawn toward it but never exactly repeats its path.

---
