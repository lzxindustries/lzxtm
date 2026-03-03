---
draft: true
sidebar_position: 198
slug: /instruments/videomancer/mycelium
title: "Mycelium"
image: /img/instruments/videomancer/mycelium/mycelium_hero.png
description: "In 1984, John Pearson numerically investigated a class of reaction-diffusion systems first described by Gray and Scott in the context of isothermal chemical reactions."
---

import mycelium_hero from '/img/instruments/videomancer/mycelium/mycelium_hero.png';
import mycelium_animation from '/img/instruments/videomancer/mycelium/mycelium_animation.gif';
import mycelium_control_panel from '/img/instruments/videomancer/mycelium/mycelium_control_panel.png';
import mycelium_exercise1_result from '/img/instruments/videomancer/mycelium/mycelium_exercise1_result.gif';
import mycelium_exercise2_result from '/img/instruments/videomancer/mycelium/mycelium_exercise2_result.gif';
import mycelium_exercise3_result from '/img/instruments/videomancer/mycelium/mycelium_exercise3_result.gif';

# Mycelium

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={mycelium_hero} alt="Mycelium hero image"/>
*Mycelium rendering a field of reaction-diffusion patterns — branching coral-like structures emerging from input video luminance, mapped through a warm color palette.*
<img src={mycelium_animation} alt="Mycelium animated output"/>
*Mycelium output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1984, John Pearson numerically investigated a class of reaction-diffusion systems first described by Gray and Scott in the context of isothermal chemical reactions. The system models two virtual chemical species — an activator (U) and an inhibitor (V) — that diffuse through space while undergoing nonlinear reactions. Depending on the feed and kill rates, the system spontaneously generates a remarkable variety of self-organizing patterns: spots, stripes, labyrinthine curves, pulsating blobs, and self-replicating dots. These patterns emerge from nothing but the interaction of diffusion and reaction — no explicit shape definition, no boundary conditions, no templates.

Mycelium implements a simplified Gray-Scott reaction-diffusion system in real-time hardware. Two chemical species evolve per-pixel at video rate, with horizontal diffusion computed from left-neighbor registers and vertical diffusion approximated using single-line BRAM buffers storing concentrations from the previous scanline. The reaction terms — the nonlinear products u·v² that drive pattern formation — are computed using shift-and-add approximations with no hardware multipliers. Input video luminance seeds the system by injecting inhibitor concentration wherever brightness exceeds a configurable threshold, causing organic patterns to grow from the video's bright features. The inhibitor concentration is then mapped to YUV output through a three-tier color palette.

The name references mycelium, the branching underground network of fungal threads that grows through soil in patterns strikingly similar to reaction-diffusion simulations. Like its biological namesake, the program's patterns spread, branch, and fill space with organic complexity emerging from simple local rules.

---

## Background

### Gray-Scott Reaction-Diffusion

The Gray-Scott system models two species reacting in a continuously stirred reactor. The activator U is fed into the system at a constant rate and consumed by the reaction U + 2V → 3V. The inhibitor V is produced by this reaction and simultaneously decays at a rate proportional to a kill constant. The continuous equations are:

$$\frac{\partial u}{\partial t} = D_u \nabla^2 u - uv^2 + f(1-u)$$
$$\frac{\partial v}{\partial t} = D_v \nabla^2 v + uv^2 - (f+k)v$$

where $f$ is the feed rate, $k$ is the kill rate, $D_u$ and $D_v$ are diffusion constants, and $\nabla^2$ is the Laplacian (spatial second derivative). The nonlinear term $uv^2$ is the autocatalytic reaction that creates structure. Mycelium's VHDL implements these equations with fixed diffusion ratios (hard-coded bit shifts instead of using the Diffusion pot) and shift-and-add approximations for the cubic reaction term.

### The Laplacian and Neighbor Stencils

The Laplacian $\nabla^2 u$ measures how much a pixel's value differs from its neighbors. A standard 2D discrete Laplacian uses a 5-point stencil (up, down, left, right, center). Due to the streaming architecture of FPGA video processing — pixels arrive left to right, top to bottom — only the left neighbor and the north neighbor (via BRAM line buffer) are available at computation time. Mycelium therefore uses a reduced 2-neighbor stencil: $\nabla^2 u \approx u_{left} + u_{north} - 2u_{center}$. This approximation is asymmetric (biased toward upper-left diffusion), which slightly favors diagonal pattern growth — a characteristic visual fingerprint of the hardware implementation.

### Shift-and-Add Multiplication

The Gray-Scott reaction requires computing $u \cdot v^2$ — a cubic product. On the iCE40 FPGA with no hardware multipliers, Mycelium approximates these products using shift-and-add: the top two bits of the multiplicand select which shifted copies of the multiplier to sum. For a 10-bit value, this computes $x \cdot y \approx y \cdot (x_9 \cdot 2^{-1} + x_8 \cdot 2^{-2})$, capturing roughly 75% of the full product's precision. The error manifests as slight variation in reaction rates across the concentration range, adding organic irregularity to the patterns.

### Video-Seeded Pattern Growth

Classical reaction-diffusion simulations are typically seeded with random initial perturbations. Mycelium instead injects inhibitor concentration from the input video's luminance channel wherever it exceeds a configurable threshold. Bright regions of the video become nucleation sites where patterns begin to grow. In continuous mode, the video continuously feeds the system, maintaining an ongoing relationship between the input image and the evolving patterns. In one-shot mode, seeding occurs only on the first frame — after that, the system evolves autonomously, and the initial video imprint gradually dissolves into the reaction-diffusion dynamics.

### Color Mapping

After the reaction-diffusion computation, the inhibitor concentration (0–1023) is mapped to YUV output. The Color Map parameter selects among three palettes: monochrome (no chroma — pure luminance), warm (negative U shift + positive V shift, producing amber/orange tones), and cool (positive U shift + negative V shift, producing cyan/blue tones). The chroma offset scales linearly with concentration, so brighter regions receive more saturated color. The Invert toggle flips the concentration before color mapping, swapping which regions are bright and dark.


---

## Signal Flow

```
INPUT VIDEO
│
├── Stage 1: Input Registration + Seed Detection ──────────────
│   ├─ s_y_in = data_in.y
│   ├─ seed_active = (y_in >= seed_thresh) AND (seed_mode OR NOT seeded)
│   └─ s_act_left, s_inh_left = previous pixel state
│
├── Stage 2: BRAM Read + Laplacian ────────────────────────────
│   ├─ act_north, inh_north = BRAM[pixel_count] (ping-pong bank)
│   ├─ lap_act = act_left + act_north − 2·act_cur
│   └─ lap_inh = inh_left + inh_north − 2·inh_cur
│
├── Stage 3a: v² + Feed/Kill Pre-computation ──────────────────
│   ├─ v_sq = inh · inh  (shift-add, top 2 bits)
│   ├─ feed_r = feed_rate/4 − (feed_rate · act_cur)/4
│   └─ kill_r = (feed_rate + kill_rate) >> 3
│
├── Stage 3b: Reaction (u · v²) ───────────────────────────────
│   └─ reaction_r = act_cur · v_sq  (shift-add, top 2 bits)
│
├── Stage 3c: State Update Assembly + Seed Injection ──────────
│   ├─ act_next = act_cur + lap_act/8 + feed_r − reaction_r
│   ├─ inh_next = inh_cur + lap_inh/16 + reaction_r/2 − kill_r
│   ├─ Clamp both to [0, 1023]
│   ├─ If seed_active → inh_next = y_in (override)
│   └─ Write act_next, inh_next to BRAM[wr_addr]
│
├── Stage 4: Color Mapping ────────────────────────────────────
│   ├─ color_val = invert ? (1023 − inh_next) : inh_next
│   ├─ Y = color_val
│   ├─ color_map < 341 → mono (U=512, V=512)
│   ├─ color_map < 682 → warm (U=512−val/4, V=512+val/4)
│   └─ color_map ≥ 682 → cool (U=512+val/4, V=512−val/4)
│
├── Clocks 9–12: Interpolator (wet/dry Mix) ───────────────────
│   └─ lerp(delayed_input, color_mapped, mix_amount) per Y/U/V
│
└── Output Mux ────────────────────────────────────────────────
    ├─ Bypass off → mixed output + delayed sync
    └─ Bypass on  → delayed input
```

The pipeline's most critical detail is the asymmetric diffusion stencil. Because pixels stream left-to-right, the right neighbor is not available during computation — only the left neighbor (from a register) and the north neighbor (from the BRAM line buffer) contribute to the Laplacian. This means diffusion is biased toward the upper-left quadrant, causing patterns to drift subtly in that direction over time. The BRAM uses a ping-pong banking scheme: on even scan lines, bank A is read and bank B is written; on odd lines, the roles reverse. This ensures the north-neighbor data is always one complete line behind. The Freeze toggle gates the speed check, halting the reaction computation while continuing to pass through the color-mapped output — the pattern freezes in place but remains visible.

---

## Parameter Reference

<img src={mycelium_control_panel} alt="Videomancer front panel with Mycelium loaded"/>
*Videomancer's front panel with Mycelium active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Feed Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Feed Rate controls the rate at which activator species is injected into the system. In the Gray-Scott model, this corresponds to the parameter $f$ — the concentration of activator entering the reactor per unit time. The VHDL computes the feed contribution as $f(1-u)/4$, approximated with shift-and-add. Low feed rates starve the system, causing patterns to shrink and die. High feed rates flood the system with activator, overwhelming the reaction and producing a uniform bright field. The sweet spot — typically 30–50% — produces the most complex branching and self-organizing behavior. This parameter interacts strongly with Kill Rate; together they define the region of parameter space where interesting patterns form.

---

#### Knob 2 — Kill Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 54.7% |
| Suffix | % |

Kill Rate controls the decay speed of the inhibitor species. In the Gray-Scott model, this is the combined $(f+k)$ death rate, but the VHDL computes it as $(feed + kill) \gg 3$, linking the two parameters. High kill rates cause the inhibitor to decay faster than it can be produced by the reaction, collapsing the patterns. Low kill rates allow the inhibitor to accumulate, producing dense, filled-in regions. The balance between Feed Rate and Kill Rate determines the pattern type: for spots, kill should be slightly higher than feed; for labyrinthine patterns, they should be nearly equal; for stripes, kill should be slightly lower.

---

#### Knob 3 — Diffusion
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Diffusion is declared as a register mapping in the VHDL but is not actually used in the computation. The Laplacian contributions use fixed bit-shift values (activator diffusion is shifted right by 3 bits, inhibitor by 4 bits), giving a fixed diffusion ratio of approximately 2:1 between species. Turning this knob has no effect on the output. The fixed ratio was chosen to match the classical Gray-Scott regime where $D_u = 2D_v$.

---

#### Knob 4 — Seed Thresh
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Seed Threshold sets the luminance level above which input video pixels inject inhibitor into the reaction-diffusion system. At minimum (0), every pixel seeds the system — the entire input image drives pattern formation. At maximum (1023), essentially no seeding occurs unless the input contains pure white. Intermediate values (40–60%) provide the most interesting results: bright features of the video become nucleation sites where patterns originate and grow outward, while dark areas remain inert until reached by diffusion from nearby seeds.

---

#### Knob 5 — Color Map
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Color Map selects the chromatic palette for the output. The register is divided into three equal zones: below 341 produces monochrome output (pure luminance, no chroma), 341–681 produces warm tones (amber/orange, achieved by shifting U negative and V positive proportionally to concentration), and 682–1023 produces cool tones (cyan/blue, U positive and V negative). The chroma shift scales linearly with inhibitor concentration, so the most active regions of the pattern receive the most saturated color. At palette boundaries the color changes abruptly — there is no smooth cross-fade between palettes.

---

#### Knob 6 — Sim Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sim Speed is declared in the register mapping but is not used to modulate the simulation rate. The only speed control is the Freeze toggle, which halts evolution entirely. When Freeze is off, the system evolves at the full per-pixel video rate regardless of this knob position. The naming suggests an intended feature (frame-skipping or sub-sampling) that was not implemented in the final VHDL.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Freeze** | Off | On |
| **8 — Seed Mode** | Cont. | One-Shot |
| **9 — Pattern** | Spots | Stripes |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure independent aspects of the simulation. Freeze halts evolution while preserving the current pattern. Seed Mode selects between continuous video seeding and one-shot (first frame only). Pattern is mapped to a register but has no effect on the output — the spots/stripes distinction is controlled entirely by the Feed Rate and Kill Rate balance, not by a toggle. Invert flips the luminance mapping. Bypass routes the delayed input to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix crossfade. At 0% (register = 0), the output is the unprocessed delayed input video. At 100% (register = 1023), the output is the fully color-mapped reaction-diffusion rendering. Intermediate values blend the two proportionally via the three interpolator_u instances. This allows subtle integration of the reaction-diffusion texture with the input video.

---

## Guided Exercises

These exercises explore the Gray-Scott reaction-diffusion system as implemented in hardware — starting with autonomous pattern growth, then adding video seeding, and finally experimenting with one-shot evolution.

### Exercise 1: Autonomous Coral Growth

<img src={mycelium_exercise1_result} alt="Autonomous Coral Growth result"/>
*Autonomous Coral Growth — simulated result across source images.*
**Objective**: Observe self-organizing reaction-diffusion patterns emerging from minimal seeding.

1. **Set feed and kill rates for spots**: Feed Rate ~40%, Kill Rate ~55%. This puts the system in the spot-formation regime.
2. **Low seed threshold**: Set Seed Thresh to ~20%. Even dim video features will seed the system.
3. **Warm palette**: Set Color Map to ~50% for amber tones.
4. **Continuous seeding**: Seed Mode set to Continuous.
5. **Full wet**: Mix at 100%.
6. **Observe**: Bright areas of the input video become nucleation sites. Watch spots form and slowly spread outward through diffusion.
7. **Adjust feed/kill**: Sweep Feed Rate and Kill Rate to find the boundary between spots and labyrinthine patterns.

**Key concepts**: The feed/kill rate ratio determines pattern morphology, spots form when kill slightly exceeds feed, seeding provides nucleation sites for pattern growth

---

### Exercise 2: Video Imprint with Freeze

<img src={mycelium_exercise2_result} alt="Video Imprint with Freeze result"/>
*Video Imprint with Freeze — simulated result across source images.*
**Objective**: Capture a moment of the reaction-diffusion system interacting with video, then freeze it.

1. **Feed a detailed video source**: Camera feed with faces or text works well.
2. **High seed threshold**: Set Seed Thresh to ~60%. Only the brightest features seed the pattern.
3. **Moderate kill**: Kill Rate ~50%. Patterns grow but don't fill everything.
4. **Let it evolve**: Watch patterns grow from bright features for 5–10 seconds.
5. **Freeze**: Engage the Freeze toggle. The pattern locks in place.
6. **Sweep Color Map**: Rotate through mono/warm/cool palettes while frozen. The pattern remains but the colorization changes.
7. **Unfreeze and compare**: Toggle Freeze off. The pattern resumes evolving from exactly where it stopped.

**Key concepts**: Freeze halts the reaction-diffusion update while preserving state, color mapping operates independently of simulation, seed threshold controls which video features drive pattern formation

---

### Exercise 3: One-Shot Dissolution

<img src={mycelium_exercise3_result} alt="One-Shot Dissolution result"/>
*One-Shot Dissolution — simulated result across source images.*
**Objective**: Observe how a video-seeded pattern evolves autonomously after seeding stops.

1. **Set one-shot mode**: Toggle Seed Mode to One-Shot.
2. **Strong feed**: Feed Rate ~45%. Patterns grow aggressively.
3. **Moderate kill**: Kill Rate ~50%.
4. **Low threshold**: Seed Thresh ~30%. Captures lots of video detail in the initial seed.
5. **Cool palette**: Color Map ~80% for cyan/blue tones.
6. **Observe over 30 seconds**: The initial video imprint slowly dissolves as the reaction-diffusion dynamics reshape the concentrations. Familiar shapes erode into organic abstractions.
7. **Invert**: Toggle Invert to see the negative — dark veins where bright patterns were.

**Key concepts**: One-shot seeding provides initial conditions from video then evolves autonomously, the system gradually loses the video imprint as diffusion homogenizes concentrations, invert reverses figure-ground relationship

---


## Tips

- **Feed and Kill are everything**: The Diffusion, Sim Speed, and Pattern controls have no effect in the current VHDL. Focus on Feed Rate and Kill Rate — they define the pattern morphology entirely.
- **The sweet spot is narrow**: Interesting Gray-Scott patterns occupy a small region of feed/kill parameter space. Start with Feed ~40%, Kill ~55% and make small adjustments. Large changes tend to produce either uniform fields or total decay.
- **One-shot for generative art**: Set Seed Mode to One-Shot, feed an interesting image, and watch it dissolve into pure reaction-diffusion patterns over time. The transition from recognizable image to organic abstraction is the most compelling visual evolution.
- **Asymmetric diffusion is a feature**: The 2-neighbor Laplacian produces patterns that drift slightly upper-left. This hardware artifact gives Mycelium a distinctive look compared to standard Gray-Scott simulations.
- **Freeze for color exploration**: Use Freeze to lock a complex pattern, then sweep Color Map through mono/warm/cool to find the best palette. Unfreeze to continue.
- **Invert for negative prints**: The Invert toggle produces striking results when the color map is in warm or cool mode — dark organic veins against a tinted bright field.
- **Low seed threshold floods the system**: Setting Seed Thresh below ~20% lets nearly every pixel inject inhibitor, which can overwhelm the reaction dynamics. Use 40–60% for structured growth from high-contrast features.

---

## Glossary

| Term | Definition |
|------|------------|
| **Activator** | The chemical species U in the Gray-Scott model, which is consumed by the autocatalytic reaction and replenished by the feed term. |
| **BRAM** | Block RAM; dedicated memory within the FPGA fabric. Mycelium uses 4 BRAM tiles for activator and inhibitor line buffers (2 banks each for ping-pong access). |
| **Diffusion** | The spatial spreading of chemical species through the Laplacian operator; drives pattern formation by creating local concentration gradients. |
| **Feed rate** | The parameter $f$ controlling how fast activator species is injected into the reactor. Higher values replenish activator faster. |
| **Gray-Scott** | A two-species reaction-diffusion model producing self-organizing patterns through the autocatalytic reaction U + 2V → 3V. |
| **Inhibitor** | The chemical species V in the Gray-Scott model, produced by the autocatalytic reaction and removed by the kill term. |
| **Kill rate** | The parameter $k$ controlling how fast inhibitor species decays. Combined with feed rate as $(f+k)$ in the VHDL implementation. |
| **Laplacian** | The spatial second derivative operator $\nabla^2$ measuring how much a value differs from its neighbors; approximated here with a 2-neighbor stencil. |
| **Ping-pong** | A double-buffering technique where two BRAM banks alternate between read and write roles on successive scan lines. |
| **Reaction-diffusion** | A class of partial differential equations where local nonlinear reactions interact with spatial diffusion to produce emergent patterns. |
| **Shift-and-add** | A multiplication approximation using bit shifts and additions instead of hardware multipliers; captures the top 2 bits of precision. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
