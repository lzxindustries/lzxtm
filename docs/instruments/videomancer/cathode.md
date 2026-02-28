---
draft: true
sidebar_position: 37
slug: /instruments/videomancer/cathode
title: "Cathode"
image: /img/instruments/videomancer/cathode/cathode_hero.png
---

import cathode_hero from '/img/instruments/videomancer/cathode/cathode_hero.png';
import cathode_before_after from '/img/instruments/videomancer/cathode/cathode_before_after.png';
import cathode_control_panel from '/img/instruments/videomancer/cathode/cathode_control_panel.png';
import cathode_exercise1_result from '/img/instruments/videomancer/cathode/cathode_exercise1_result.png';
import cathode_exercise2_result from '/img/instruments/videomancer/cathode/cathode_exercise2_result.png';
import cathode_exercise3_result from '/img/instruments/videomancer/cathode/cathode_exercise3_result.png';

# Cathode

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={cathode_hero} alt="Cathode hero image"/>
*Cathode striking a procedural lightning bolt across a nighttime cityscape, the electric-blue glow bleeding into the surrounding video.*
<img src={cathode_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Cathode applied.*

---

## Overview

Lightning is nature's most dramatic display of electrical energy — a branching, jagged path of ionized air that exists for less than a millisecond but burns into visual memory. Cathode recreates this phenomenon as a real-time procedural effect, generating bolt paths via random-walk displacement and compositing them over live video with Gaussian glow profiles and palette-selectable color tinting.

The name references the *cathode* — the electrode from which electrons depart in a discharge tube. It is also a nod to the cathode ray tube, the display technology that defined analog video. The program draws a direct line to the NewTek NewTek's Forked Lightning and Jagged Lightning effects from the Organic Effects bank — staples of early 1990s church broadcasts, wedding videos, and sci-fi television. Where the Toaster played back pre-rendered frame sequences, Cathode synthesizes bolts procedurally every frame using a 16-bit Galois LFSR, midpoint displacement, and hardware-accelerated glow computation.

At moderate settings, Cathode produces convincing electrical arcs that track across the frame. At extreme roughness and fork values, bolts shatter into fractal discharge trees. The four selectable color palettes — electric blue, purple, warm white, and green — cover the most common cinematic lightning styles, from realistic storm footage to sci-fi energy weapons.

---

## Background

### What Is Midpoint Displacement?

Midpoint displacement is a fractal subdivision technique for generating irregular paths. Start with a straight line between two endpoints. Find the midpoint and displace it perpendicular to the line by a random amount. Repeat for each new sub-segment, reducing the displacement range at each level. The result is a jagged, natural-looking path — exactly the visual character of a lightning bolt. Cathode implements a simplified one-dimensional version: it walks sequentially from top to bottom (or bottom to top), accumulating random horizontal displacements at each entry. The Roughness control scales the magnitude of each displacement step, controlling how far the bolt wanders from a straight vertical line.

### What Is a Galois LFSR?

A **Linear Feedback Shift Register** (LFSR) is a shift register whose input bit is a function of its previous state. A Galois LFSR applies XOR taps at specific bit positions during the shift operation, producing a pseudo-random sequence that cycles through every non-zero state before repeating. Cathode uses a 16-bit Galois LFSR with tap mask `0xB400` and seed `0xACE1`. This generates the random displacement values that drive the bolt's random walk and the fork probability decisions. Because the LFSR is deterministic, the same seed always produces the same bolt — but the seed advances with every frame, so successive bolts trace different paths.

### What Is Gaussian Glow?

A real lightning bolt is not a single-pixel-wide line. The ionized plasma channel emits light in all directions, and the surrounding air scatters it further. The result is a bright core that falls off smoothly with distance. Cathode models this with a **Gaussian glow profile** — a lookup table of 64 entries computed from the function $\text{gauss}(i) = 1023 \times e^{-(i/16)^2}$. For each pixel, the horizontal distance to the bolt path is computed, scaled by the Glow Width control, and used to index into this table. The result is a smooth, bell-curve-shaped brightness falloff that gives the bolt its characteristic soft halo.

### What Is Additive Compositing?

Standard video compositing replaces pixels — the effect covers the background. **Additive compositing** adds the effect's pixel values to the background's pixel values, clamping at maximum brightness. This means the bolt can only make the image brighter, never darker. Dark areas of the source receive the full glow; bright areas saturate toward white. This is physically accurate for light-emitting phenomena like lightning, fire, and lens flares — they add luminance to whatever is behind them. Cathode applies additive compositing to the Y (luminance) channel and applies palette-dependent signed shifts to U and V (chrominance).

### What Is Flash-Hold-Fade?

Real lightning appears as a sudden flash that lingers briefly then decays. Cathode's Animate mode reproduces this temporal envelope with a three-phase cycle: **flash** (instant full brightness when a new bolt is generated), **hold** (3 frames at full brightness to simulate the persistence of the main stroke), and **fade** (exponential decay via right-shift, halving brightness each frame until the bolt disappears). The Flash Rate control sets how quickly a new bolt is generated to restart the cycle. In static mode (Animate off), the bolt regenerates every frame at full brightness — useful for still-image captures and sustained glow effects.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Bolt Path Generation (vblank) ──────────────────────────────
│   │
│   ├─ 1. GEN_INIT       Target X → scale to [0,1279] → write entry 0
│   ├─ 2. GEN_WALK        LFSR random walk (128 entries)
│   │     └─ Roughness × signed(LFSR) → displacement
│   │     └─ Fork kink:   if LFSR(15:6) < fork_chance → displacement ×2
│   └─ 3. Store           128 × 11-bit X positions → BRAM
│
├── Flash Timer ────────────────────────────────────────────────
│   └─ Animate mode: flash → hold(3) → exponential fade
│   └─ Static mode:  regen every frame, full brightness
│
├── Pipeline Stage 1: Input Capture ────────────────────────────
│   └─ Latch Y, U, V, sync
│
├── Pipeline Stage 2: Distance Calculation ─────────────────────
│   └─ bolt_rd_addr = scanline(9:3) [Direction: normal or flipped]
│   └─ pixel_dist = |h_count − bolt_x|
│
├── Pipeline Stage 3: Glow + Brightness + Fade ─────────────────
│   └─ Glow Width → scale pixel_dist → index 64-entry Gaussian LUT
│   └─ glow_raw × Brightness → bright_prod
│   └─ bright_prod × bolt_fade → glow_val
│
├── Pipeline Stage 4: Palette Tint + Additive Composite ────────
│   ├─ Y: add_y = in_y + glow_val (saturate at 1023)
│   ├─ U: in_u + palette_u_shift(glow_val)
│   └─ V: in_v + palette_v_shift(glow_val)
│
├── Output: Interpolator (wet/dry mix) ─────────────────────────
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The bolt path is generated entirely during the vertical blanking interval, filling a 128-entry BRAM with horizontal positions. During active video, the pipeline reads from this BRAM — each entry covers approximately 5.6 scan lines (720 ÷ 128 ≈ 5.6), so the bolt has a blocky, segmented quality at the vertical scale that reinforces the electrical discharge aesthetic. The glow computation uses a two-stage multiplication chain (glow × brightness, then × fade), which compresses the dynamic range through 10-bit truncation at each stage — this is why the fade appears to accelerate as it decays, mimicking the nonlinear cooling of a plasma channel.

---

## Parameter Reference

<img src={cathode_control_panel} alt="Videomancer front panel with Cathode loaded"/>
*Videomancer's front panel with Cathode active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Roughness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the magnitude of the random displacement applied at each step of the bolt path walk. At zero, the bolt traces a perfectly straight vertical line from its starting position. As Roughness increases, each step adds a larger horizontal displacement scaled by the LFSR's random output, producing increasingly jagged, erratic paths. Very high values cause the bolt to wander wildly across the full frame width.

---

#### Knob 2 — Fork
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the probability of a "fork kink" at each step of the bolt walk. When the LFSR's upper bits fall below the Fork threshold, the displacement for that step is doubled, creating a sharp directional change that visually suggests a branching fork. At zero, the bolt follows a smooth random walk. At high values, frequent kinks produce a shattered, branching discharge pattern. Note that this control modifies the *main* bolt path — there is no separate branch rendering, but the visual effect convincingly suggests forking due to the sudden directional changes.

---

#### Knob 3 — Glow Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls the spatial extent of the Gaussian glow halo around the bolt core. The width register's upper bits select a scaling shift applied to the pixel distance before indexing the 64-entry glow lookup table: larger widths map the same physical distance to a smaller LUT index, extending the glow further from the bolt center. At low values, the bolt appears as a thin, sharp line. At high values, the glow spreads across a significant portion of the frame, creating a soft atmospheric discharge.

---

#### Knob 4 — Flash Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Sets the bolt regeneration speed in Animate mode. The flash timer counts down from a value derived from this register — lower values produce very slow regeneration with long fade tails, higher values produce rapid-fire flashing. In static mode (Animate toggle off), this control has no effect because the bolt regenerates every frame. The interaction between Flash Rate and the exponential fade creates the program's characteristic temporal rhythm.

---

#### Knob 5 — Target X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the bolt's horizontal strike point. The register value is scaled from the 10-bit control domain to the 1280-pixel display domain (target + target>>2). This sets the starting X position written to BRAM entry 0 — the bolt's origin point. All subsequent random walk steps displace relative to this anchor. Centering the control places the bolt in the middle of the frame; sweeping it left and right moves the discharge across the image.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the overall intensity of the bolt glow after the Gaussian lookup. This multiplier is applied before the fade stage, so it sets the peak brightness of the flash. At zero, the bolt is invisible. At maximum, even the outermost glow fringes are bright enough to saturate the additive composite. This control interacts directly with Glow Width — a narrow bolt with high brightness produces a hot, laser-like line, while a wide bolt with moderate brightness produces a diffuse atmospheric discharge.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette A** | Off | On |
| **8 — Palette B** | Off | On |
| **9 — Animate** | Off | On |
| **10 — Direction** | Down | Up |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a 2-bit color palette selector (00 = Electric Blue, 01 = Purple, 10 = Warm White, 11 = Green). Toggle 9 selects between static mode (regenerate every frame at full brightness) and animated flash-hold-fade mode. Toggle 10 flips the bolt's vertical orientation between top-to-bottom and bottom-to-top. Toggle 11 is a hard bypass. This group divides into three functional clusters: palette selection (7–8), temporal behavior (9), and spatial orientation (10).

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Wet/dry mix between the original input video and the bolt-composited output. At 0%, the output is pure input — no bolt visible. At 100%, the full additive composite is applied. Intermediate values blend linearly via the interpolator, allowing subtle bolt overlays that feel like background atmospheric events rather than dominant foreground effects.

---

## Guided Exercises

These exercises progress from a basic vertical bolt to animated multi-palette discharges, building familiarity with the random walk, glow, and temporal controls.

### Exercise 1: Static Bolt Anatomy

<img src={cathode_exercise1_result} alt="Static Bolt Anatomy result"/>
*Static Bolt Anatomy — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a dark upper region (night sky, dark background).

**Objective**: Understand the bolt path generation, glow profile, and additive compositing fundamentals.

1. **Disable animation**: Set Animate (Toggle 9) to Off so the bolt is continuously visible.
2. **Center the bolt**: Set Target X to 50%. A bolt appears in the center of the frame.
3. **Observe roughness**: Slowly increase Roughness from 0%. At zero, the bolt is a straight vertical line. As roughness increases, the path becomes jagged and wandering.
4. **Glow width**: Sweep Glow Width from minimum to maximum. Watch the bolt expand from a thin line to a broad atmospheric glow.
5. **Brightness**: Increase Brightness to see how the glow saturates the additive composite in bright areas of the source.
6. **Direction**: Toggle Direction (Toggle 10) between Down and Up. The bolt flips vertically.

**Key concepts**: Random walk displacement creates bolt jaggedness, Gaussian glow profile controls spatial falloff, additive compositing only adds luminance, direction flips the BRAM read order

---

### Exercise 2: Flash-Hold-Fade Animation

<img src={cathode_exercise2_result} alt="Flash-Hold-Fade Animation result"/>
*Flash-Hold-Fade Animation — simulated result across source images.*
**Source**: Dark or moderately lit footage where the flash will be clearly visible.

**Objective**: Explore the temporal envelope and how Flash Rate interacts with the fade curve.

1. **Enable animation**: Set Animate (Toggle 9) to On.
2. **Slow flash**: Set Flash Rate low (~15%). Watch the bolt flash, hold briefly, then fade out slowly before the next strike.
3. **Fast flash**: Increase Flash Rate to ~80%. Bolts fire in rapid succession with short fade tails, creating a strobing effect.
4. **Moderate rate**: Settle at ~40%. Each bolt is individually readable — flash, hold, fade.
5. **Fork interaction**: Increase Fork to ~60%. Each regenerated bolt has a different path, so the kink points shift with every strike.
6. **Brightness fade**: Watch how the exponential fade makes the glow shrink inward — the fringes disappear first, then the core.

**Key concepts**: Flash-hold-fade creates a three-phase temporal envelope, exponential decay via bit-shift halving, each regeneration produces a new LFSR-driven path

---

### Exercise 3: Palette Exploration

<img src={cathode_exercise3_result} alt="Palette Exploration result"/>
*Palette Exploration — simulated result across source images.*
**Source**: Footage with visible color — skin tones, foliage, or color bars.

**Objective**: Compare all four color palettes and observe how chroma tinting interacts with saturated source material.

1. **Electric Blue (00)**: Both Palette toggles Off. Note the cool blue-white discharge typical of electrical arcs.
2. **Purple (01)**: Toggle Palette A On. The bolt shifts to a purple/violet tint — both U and V shift positive.
3. **Warm White (10)**: Toggle Palette A Off, Palette B On. Subtle amber warmth — the most naturalistic lightning.
4. **Green (11)**: Both Palette toggles On. The bolt takes on a vivid green tint.
5. **Color interaction**: With each palette, observe how the tint affects the source colors in the glow region — the chroma shifts are proportional to glow intensity, so only areas near the bolt are tinted.
6. **Mix control**: Lower Mix to ~50%. The bolt becomes a subtle atmospheric element rather than a dominant overlay.

**Key concepts**: Palette selection is a 2-bit code from toggles 7+8, chroma shift is proportional to glow intensity, additive luma is independent of palette, mix controls composite strength

---


## Tips

- **Dark backgrounds show bolts best**: Additive compositing means the bolt can only brighten pixels. Dark scenes show the full glow dynamic range; bright scenes compress it.
- **Static mode for still captures**: Turn Animate off to get a persistent bolt that changes path every frame — useful for photographing or freeze-framing a specific bolt shape.
- **Roughness and Fork interact**: Roughness controls the baseline displacement magnitude, Fork controls how often that magnitude is doubled. Use moderate roughness with high fork for realistic branching, or high roughness with low fork for sweeping arcs.
- **Glow Width and Brightness are complementary**: Wide glow with low brightness creates a diffuse atmospheric effect. Narrow glow with high brightness creates a hot, intense discharge. Adjust both together to control the bolt's visual weight.
- **Palette tinting is glow-proportional**: The chroma shift only affects pixels within the glow radius, and it scales with glow intensity. This means the bolt core is heavily tinted while the fringes fade to neutral — a natural-looking color gradient.
- **Feedback routing**: Routing Cathode's output back to its input creates accumulating glow fields — each frame adds to the previous discharge, building up dense lightning networks.
- **Warm White for realism**: The Warm White palette (Palette B On, Palette A Off) produces the most naturalistic lightning because real lightning is approximately 6500K white with slight amber from atmospheric scattering.
- **Mix for layering**: Use Mix at 30–50% to create subtle background electrical activity rather than a dominant foreground effect. This works well when combining with other Videomancer programs in a signal chain.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive compositing** | A blending method that adds the effect's pixel values to the background's values, clamping at maximum brightness so the effect can only brighten the image. |
| **BRAM (Block RAM)** | Dedicated memory blocks embedded in the FPGA fabric, used here to store the 128-entry bolt path lookup table. |
| **Flash-hold-fade** | A three-phase temporal envelope in which a bolt appears at full brightness (flash), persists for several frames (hold), then decays exponentially (fade). |
| **Galois LFSR** | A variant of the Linear Feedback Shift Register that applies XOR taps during the shift operation, producing a deterministic pseudo-random bit sequence. |
| **Gaussian glow** | A brightness falloff profile shaped by the Gaussian (bell curve) function, creating a smooth halo that tapers from a bright core to a dim fringe. |
| **LFSR (Linear Feedback Shift Register)** | A shift register whose input bit is a function of its previous state, generating a pseudo-random sequence that cycles through all non-zero states. |
| **Luminance** | The brightness component of a video signal, represented by the Y channel in YUV colour space. |
| **LUT (Lookup Table)** | A pre-computed array of values indexed by an input, used here for the 64-entry Gaussian glow intensity profile. |
| **Midpoint displacement** | A fractal subdivision technique that recursively displaces the midpoint of a line segment by a random amount, producing jagged natural-looking paths. |
| **Pipeline** | A series of sequential processing stages in hardware, each completing one clock cycle of work and passing results to the next stage. |
| **XOR (Exclusive-OR)** | A logic operation that returns true when exactly one of two inputs is true, used here for LFSR feedback taps and fork probability tests. |
| **YUV** | A colour model that separates luminance (Y) from two chrominance components (U and V), widely used in video signal processing. |

---
