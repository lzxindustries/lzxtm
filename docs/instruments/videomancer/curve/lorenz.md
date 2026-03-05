---
draft: true
sidebar_position: 179
slug: /instruments/videomancer/lorenz
title: "Lorenz"
image: /img/instruments/videomancer/lorenz/lorenz_hero.png
description: "In 1963, meteorologist Edward Lorenz was running a simplified weather simulation on a Royal McBee LGP-30 computer."
---

import lorenz_hero from '/img/instruments/videomancer/lorenz/lorenz_hero.png';
import lorenz_animation from '/img/instruments/videomancer/lorenz/lorenz_animation.gif';
import lorenz_control_panel from '/img/instruments/videomancer/lorenz/lorenz_control_panel.png';
import lorenz_exercise1_result from '/img/instruments/videomancer/lorenz/lorenz_exercise1_result.gif';
import lorenz_exercise2_result from '/img/instruments/videomancer/lorenz/lorenz_exercise2_result.gif';
import lorenz_exercise3_result from '/img/instruments/videomancer/lorenz/lorenz_exercise3_result.gif';

# Lorenz

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lorenz_hero} alt="Lorenz hero image"/>
*Lorenz rendering the iconic butterfly-shaped strange attractor as a persistent phosphor trace on a 64×64 canvas, its trajectory glowing against the void.*
<img src={lorenz_animation} alt="Lorenz animated output"/>
*Lorenz output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1963, meteorologist Edward Lorenz was running a simplified weather simulation on a Royal McBee LGP-30 computer. To save time, he restarted a run from the middle, typing in state values rounded to three decimal places instead of the six stored internally. The result diverged completely from the original — a tiny rounding error, amplified by the system's nonlinear dynamics, produced a totally different trajectory. This discovery became the founding example of deterministic chaos: a system governed by simple, fixed equations whose long-term behavior is nonetheless unpredictable because infinitesimal differences in initial conditions grow exponentially over time.

Lorenz renders this system in real time. Three coupled differential equations — the Lorenz equations — are integrated using a fixed-point Euler method running during the horizontal blanking intervals of the video signal. The trajectory is projected onto a 64×64 canvas stored in BRAM, where each point is plotted at maximum brightness and then slowly fades according to a phosphor decay model. The result is the iconic butterfly-shaped attractor: two lobes connected by a central saddle, the trajectory spiraling around one lobe before unpredictably switching to the other. With the classic parameters (σ=10, ρ=28, β=8/3), the system produces the strange attractor that has become one of the most recognized images in mathematics and physics.

The program offers direct control over all three Lorenz parameters, integration speed, phosphor persistence, and trace brightness. A projection toggle switches between the X-Y and X-Z planes of the three-dimensional phase space. A periodic perturbation mode demonstrates sensitive dependence on initial conditions by kicking the state every 128 frames. Rainbow mode maps the z-coordinate to hue, revealing the vertical structure of the attractor through color.

---

## Quick Start

1. **Start canonical**: Begin with σ=10, ρ=28, β=8/3. These values produce the classic attractor and serve as a known-good baseline for exploration.
2. **Rho is the drama knob**: Sweeping Rho through the bifurcation point (≈24.74) produces the most visually dramatic effect — a transition from convergent order to bounded chaos.
3. **Decay shapes the aesthetic**: Zero decay accumulates everything, eventually saturating to a solid bright blob. Maximum decay shows only the instantaneous trajectory. The sweet spot (rate 1–2) reveals the attractor's shape through persistent trails.

---

## Background

### The Lorenz System

The Lorenz system is a set of three ordinary differential equations:

$$\frac{dx}{dt} = \sigma(y - x)$$
$$\frac{dy}{dt} = x(\rho - z) - y$$
$$\frac{dz}{dt} = xy - \beta z$$

The three parameters — σ (sigma, the Prandtl number), ρ (rho, the Rayleigh number), and β (beta, a geometric factor) — were originally derived from a simplified model of atmospheric convection. At the canonical values σ=10, ρ=28, β=8/3, the system exhibits chaotic behavior: the trajectory never settles into a fixed point or periodic orbit, instead tracing an infinitely long, never-repeating path through a bounded region of phase space. This bounded region — the strange attractor — has a fractal dimension of approximately 2.06, meaning it fills more than a surface but less than a volume.

### Strange Attractors and Phase Portraits

A strange attractor is a set of states toward which a dynamical system evolves over time, characterized by sensitive dependence on initial conditions and a fractal geometric structure. The "phase portrait" is a visualization of the attractor — a plot of the system's trajectory through its state space. For the Lorenz system, the state space is three-dimensional (x, y, z), and the attractor resembles a butterfly or figure-eight, with the trajectory spiraling around two lobes centered at the system's unstable fixed points. Lorenz projects this 3D trajectory onto a 2D canvas by selecting either the X-Y or X-Z plane, producing the characteristic wing pattern.

### Euler Integration in Fixed-Point Arithmetic

The VHDL implementation uses the simplest numerical integration method: the forward Euler method. At each step, the new state is computed as $x_{n+1} = x_n + \Delta t \cdot f(x_n)$, where $f$ is the right-hand side of the differential equations. The state variables are stored as signed 16-bit fixed-point numbers in 6.10 format (6 integer bits, 10 fractional bits), giving a range of approximately ±32 with a resolution of about 0.001. The multiplications required for the Lorenz equations produce 32-bit intermediate products, from which bits 25:10 are extracted as the scaled increment — effectively dividing by 1024, which serves as the integration time step $\Delta t$. Clamping at ±32000 prevents overflow when parameters are pushed to extreme values.

### Phosphor Decay and Persistence

Oscilloscope displays and early vector monitors used phosphor-coated screens where the electron beam excited the phosphor to glow brightly at the point of impact. After the beam moved on, the phosphor decayed exponentially — bright traces faded over time, leaving a ghostly afterimage. Lorenz simulates this with a 4-bit-per-pixel canvas. Each plotted point is set to maximum brightness (15). On every frame, a decay scan subtracts a configurable amount (0–3) from every canvas cell. The result is a persistence effect: recent trajectory points glow brightly, older points are dimmer, and the oldest have faded to black. Higher decay rates produce shorter trails; lower rates produce long, luminous persistence.

### Sensitive Dependence on Initial Conditions

The hallmark of chaos is that two trajectories starting from nearly identical initial conditions will diverge exponentially over time. Lorenz's Perturb toggle demonstrates this directly: every 128 frames, a small kick (adding 0.5 in 6.10 fixed-point, which is 512 raw counts) is applied to the x state variable. This tiny perturbation is rapidly amplified by the chaotic dynamics, causing the trajectory to explore a completely different sequence of lobe switches — even though the underlying equations and parameters are unchanged. The effect is visible as a sudden change in the pattern of the attractor's trace.


---

## Signal Flow

Canvas Address Compute → Canvas Read → Brightness Scaling → Compose

```
HORIZONTAL BLANKING (integration phase)
│
├── Parameter Scaling ──────────────────────────────────────────
│   ├─ sigma = sigma_pot × 40  (6.10 fp)
│   ├─ rho   = rho_pot × 50   (6.10 fp)
│   ├─ beta  = beta_pot × 10  (6.10 fp)
│   ├─ steps_per_line = step_speed >> 4 + 1  (1..64)
│   └─ decay_rate = pot threshold → 0..3
│
├── Lorenz Euler Integration (signed 16-bit, 6.10 fp) ─────────
│   ├─ dx = sigma × (y − x)
│   ├─ dy = x × (rho − z) − y × 1024
│   ├─ dz = x × y − beta × z
│   ├─ x_new = x + dx[25:10]  (clamped ±32000)
│   ├─ y_new = y + dy[25:10]  (clamped ±32000)
│   └─ z_new = z + dz[25:10]  (clamped ±32000)
│
├── Projection to Canvas (64×64) ───────────────────────────────
│   ├─ canvas_x = x >> 10 + 32  (center in 64-wide canvas)
│   ├─ canvas_y = y >> 10 + 32  (X-Y projection)
│   │         or  z >> 10 + 16  (X-Z projection, Z is positive-biased)
│   └─ Plot: canvas[y][x] = 15  (max brightness)
│
├── Perturbation (every 128 frames) ────────────────────────────
│   └─ If Perturb on and frame_count=0 → x += 512
│
FRAME START (vsync rising edge)
│
├── Canvas Decay Scan ──────────────────────────────────────────
│   └─ For each cell: value = max(0, value − decay_rate)
│
ACTIVE VIDEO (display phase, 4 clocks)
│
├── Stage 1: Canvas Address Compute ────────────────────────────
│   ├─ canvas_x = h_count >> 5  (screen ÷ 32)
│   └─ canvas_y = v_count >> 4  (screen ÷ 16)
│
├── Stage 2: Canvas Read ───────────────────────────────────────
│   └─ pixel_val = canvas[canvas_y × 64 + canvas_x]  (4-bit)
│
├── Stage 3: Brightness Scaling ────────────────────────────────
│   └─ trace_bright = pixel_val × bright_pot × 4 >> 4
│
├── Stage 4: Compose ───────────────────────────────────────────
│   ├─ Replace: Y = trace_bright, UV = colored/phosphor
│   ├─ Overlay: Y = input_Y + trace_bright (saturate)
│   └─ Rainbow: UV from pixel_val hue quadrant
│
├── Clocks 5–8: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(delayed_input, composed, mix_amount) per channel
│
└── Output Mux ─────────────────────────────────────────────────
    ├─ Bypass off → mixed output
    └─ Bypass on  → delayed input
```

The pipeline splits into two distinct time domains. During horizontal blanking, the integrator runs up to 64 Euler steps per scan line, advancing the Lorenz trajectory and plotting points to the 64×64 canvas BRAM. At frame boundaries (vsync rising edge), a decay scan decrements every canvas cell. During active video, the display pipeline reads the canvas at a scaled address, maps the 4-bit pixel value to brightness, and composes with the input video. The canvas's low resolution (64×64) means each canvas pixel covers approximately 30×17 screen pixels, producing a blocky, CRT-oscilloscope-like rendering. The rainbow color mode uses a simple 4-quadrant lookup indexed by the upper 2 bits of the pixel value, cycling through four distinct UV pairs — it does not produce a smooth hue gradient but rather four discrete color zones that correlate with trace recency.

---

## Parameter Reference

<img src={lorenz_control_panel} alt="Videomancer front panel with Lorenz loaded"/>
*Videomancer's front panel with Lorenz active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sigma
| Property | Value |
|----------|-------|
| Range | 0 – 40 |
| Default | 10 |

The Lorenz σ (sigma) parameter, scaled from the 10-bit register to a range of 0–40. In the original atmospheric convection model, sigma represents the Prandtl number — the ratio of kinematic viscosity to thermal diffusivity. At the canonical value of 10 (register ≈256), the system produces the classic butterfly attractor. Lower values slow the x-y coupling, causing the trajectory to spiral more tightly around each lobe. Higher values increase the coupling strength, making lobe transitions more frequent and the overall pattern more tightly wound. At extreme values, the attractor may collapse to a fixed point or diverge to the clamp boundaries.

---

#### Knob 2 — Rho
| Property | Value |
|----------|-------|
| Range | 0 – 50 |
| Default | 28 |

The Lorenz ρ (rho) parameter, scaled from 0–50. Rho represents the Rayleigh number — the temperature difference driving convection. The canonical value is 28 (register ≈573). Below ρ≈24.74, the attractor contracts and the system settles into a stable fixed point — the trajectory spirals inward and stops. Above this critical threshold, the system becomes chaotic. Increasing rho beyond 28 expands the attractor vertically and makes the lobe switches more erratic. This is arguably the most dramatic parameter — sweeping it through the bifurcation point produces a visible transition from order to chaos.

---

#### Knob 3 — Beta
| Property | Value |
|----------|-------|
| Range | 0 – 10 |
| Default | 3 |

The Lorenz β (beta) parameter, scaled from 0–10. Beta represents a geometric aspect ratio in the convection model. The canonical value is 8/3 ≈ 2.67 (register ≈273). Beta controls the damping of the z variable. Lower values reduce damping, allowing z to grow larger and stretching the attractor vertically. Higher values increase damping, compressing the attractor into a flatter profile. This parameter has a subtler effect than sigma or rho — it shapes the attractor's proportions without dramatically changing its qualitative behavior.

---

#### Knob 4 — StepSpd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Integration speed. Controls how many Euler steps are computed per horizontal blanking interval. The register is shifted right by 4 bits and incremented by 1, giving a range of 1–64 steps per line. At minimum, the trajectory advances slowly — one step per scan line, requiring many frames to trace the attractor. At maximum, 64 steps are computed per line, and the trajectory races around the attractor, quickly filling the canvas with traces. Higher speeds also increase the numerical error of the Euler method, which can cause the trajectory to deviate slightly from the true mathematical solution — an acceptable trade-off that adds an element of computational imperfection to the visualization.

---

#### Knob 5 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Phosphor decay rate. Controls how quickly plotted points fade from the canvas. The register is threshold-quantized into four levels: 0 (no decay — points persist indefinitely), 1 (slow fade), 2 (moderate fade), and 3 (fast fade). At zero decay, the canvas accumulates all trajectory points and eventually saturates to a solid bright field. At maximum decay, only the most recent points are visible — the trace appears as a short, bright worm crawling along the attractor. Intermediate values produce the characteristic phosphor persistence where the trajectory leaves a glowing trail that fades over several frames.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Trace brightness. Scales the 4-bit canvas pixel value to the 10-bit display domain. The brightness computation multiplies the pixel value by the register value and scales the result, determining how bright the attractor trace appears against the background. At minimum, the trace is barely visible. At maximum, even partially decayed canvas cells produce bright output. This control interacts with the Compose mode: in Overlay mode, high brightness can wash out the underlying video; in Replace mode, it sets the absolute luminance of the attractor rendering.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Proj** | X-Y | X-Z |
| **8 — Color** | Phosphor | Rainbow |
| **9 — Perturb** | Off | On |
| **10 — Compose** | Overlay | Replace |
| **11 — Bypass** | Off | On |

Switches 7–10 configure four independent aspects of the visualization: projection plane, color mode, perturbation, and composition method. None interact combinatorially — each switch independently modifies one dimension of the display. Switch 11 is the standard bypass.

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

Wet/dry crossfade between the original (dry) signal and the Lorenz-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore the Lorenz system from first principles — starting with the canonical chaotic attractor, then varying parameters to observe bifurcations, and finally experimenting with visualization modes.

### Exercise 1: The Canonical Butterfly

<img src={lorenz_exercise1_result} alt="The Canonical Butterfly result"/>
*The Canonical Butterfly — simulated result across source images.*
**What You'll Create**: Observe the classic Lorenz strange attractor at its canonical parameter values.

1. **Set canonical parameters**: Sigma ≈ 10 (register ~256), Rho ≈ 28 (register ~573), Beta ≈ 2.67 (register ~273).
2. **Moderate speed**: Set StepSpd to ~50%. The trajectory traces the attractor at a visible pace.
3. **Phosphor trail**: Set Decay to ~25%. Long persistence lets the butterfly shape accumulate.
4. **Brightness**: Set Bright to ~75% for clear visibility.
5. **Replace mode**: Set Compose to Replace (Switch 10 On). The attractor renders against black.
6. **Observe**: Watch the trajectory spiral around one lobe, then unpredictably switch to the other. The two wings of the butterfly gradually fill in.
7. **Projection**: Toggle Proj (Switch 7) to see the X-Z view. The butterfly appears from above, with the trajectory arcing between stacked lobes.

**Key concepts**: The Lorenz attractor has two lobes connected by a saddle point, the trajectory never repeats, canonical values σ=10 ρ=28 β=8/3 produce the classic butterfly shape

---

### Exercise 2: Edge of Chaos

<img src={lorenz_exercise2_result} alt="Edge of Chaos result"/>
*Edge of Chaos — simulated result across source images.*
**What You'll Create**: Sweep the Rho parameter through the bifurcation point to observe the transition from order to chaos.

1. **Start below critical threshold**: Set Rho to ~20 (register ~410). The trajectory spirals inward and settles to a fixed point.
2. **Increase Decay**: Set Decay to ~50% so old traces fade quickly, showing current behavior clearly.
3. **Sweep Rho upward**: Slowly increase Rho. Watch for the moment when the trajectory stops converging — it begins to oscillate, then suddenly breaks into chaotic switching between lobes.
4. **The critical point**: At ρ≈24.74 (register ~506), the bifurcation occurs. Below it: stable spiral. Above it: chaos.
5. **Push higher**: Continue increasing Rho toward 40–50. The attractor expands and the lobe switches become more erratic.
6. **Sigma variation**: Return to canonical Rho. Now sweep Sigma from low to high. Observe how it changes the tightness of the spirals without eliminating chaos.

**Key concepts**: The Lorenz system undergoes a Hopf bifurcation at a critical Rho value, below which the trajectory converges, parameter sweeping reveals the boundary between order and chaos

---

### Exercise 3: Chaos in Color

<img src={lorenz_exercise3_result} alt="Chaos in Color result"/>
*Chaos in Color — simulated result across source images.*
**What You'll Create**: Combine perturbation, rainbow color, and video overlay for a dynamic composite visualization.

1. **Canonical parameters**: Sigma ≈ 10, Rho ≈ 28, Beta ≈ 2.67.
2. **Enable Perturb**: Turn on Switch 9. Every 128 frames (~2 seconds), the trajectory receives a kick.
3. **Rainbow mode**: Turn on Switch 8. The trace colors shift with pixel brightness, revealing decay layers.
4. **Overlay mode**: Set Compose to Overlay (Switch 10 Off). The attractor is added to the input video.
5. **Reduce brightness**: Set Bright to ~40% to prevent washing out the video source.
6. **Moderate decay**: Set Decay to ~30%. Trails persist long enough to show the attractor shape but clear fast enough to see perturbation effects.
7. **Speed up**: Increase StepSpd to ~70%. The trajectory moves fast, rapidly filling the attractor region.
8. **Mix**: Set Mix to ~80% for a subtle blend of attractor over video.

**Key concepts**: Perturbation demonstrates sensitive dependence on initial conditions, rainbow mode reveals temporal structure through color, overlay mode composites the mathematical visualization with live video

---


## Tips

- **Replace for math, Overlay for art**: Replace mode isolates the attractor for pure mathematical visualization. Overlay mode integrates it with video, creating a composite where chaos theory meets lived imagery.
- **Perturb reveals chaos**: The perturbation toggle is the clearest demonstration of sensitive dependence. Enable it and watch the trajectory change unpredictably after each kick — same equations, same parameters, different evolution.
- **Low resolution is the point**: The 64×64 canvas intentionally produces a low-resolution, blocky rendering. This is not a limitation — it evokes the resolution constraints of early computer graphics and vector oscilloscopes, where scientists first visualized dynamical systems.
- **Extreme parameters break beautifully**: Pushing Sigma, Rho, and Beta to extreme values causes the integrator to hit its clamp boundaries, producing geometric patterns at the canvas edges that are visually interesting in their own right.

---

## Glossary

| Term | Definition |
|------|------------|
| **Attractor** | A set of states toward which a dynamical system evolves over time; the Lorenz attractor is "strange" because it has fractal structure and supports chaotic trajectories. |
| **Bifurcation** | A qualitative change in a system's behavior as a parameter crosses a critical threshold; the Lorenz system bifurcates from stable to chaotic near ρ≈24.74. |
| **Canvas** | The 64×64 pixel buffer stored in BRAM that accumulates trajectory points and is read out during active video. |
| **Chaos** | Deterministic but unpredictable behavior arising from nonlinear dynamics and sensitive dependence on initial conditions. |
| **Euler method** | The simplest numerical integration technique: $x_{n+1} = x_n + \Delta t \cdot f(x_n)$. Fast but accumulates error, especially at large time steps. |
| **Fixed-point** | A representation of fractional numbers using integer arithmetic with a fixed binary point; the Lorenz integrator uses 6.10 format (6 integer bits, 10 fractional bits). |
| **Lorenz equations** | Three coupled ODEs ($\dot{x}=\sigma(y-x)$, $\dot{y}=x(\rho-z)-y$, $\dot{z}=xy-\beta z$) that model simplified atmospheric convection and exhibit deterministic chaos. |
| **Phase portrait** | A visualization of a dynamical system's trajectory through its state space. |
| **Phosphor decay** | The gradual fading of a display phosphor after excitation, simulated by decrementing canvas pixel values each frame. |
| **Strange attractor** | An attractor with fractal dimension, supporting chaotic trajectories that never repeat. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
