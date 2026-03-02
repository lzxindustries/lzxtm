---
draft: true
sidebar_position: 26
slug: /instruments/videomancer/bomber
title: "Bomber"
image: /img/instruments/videomancer/bomber/bomber_hero.png
description: "Every arcade game has its moment of spectacle — the bomb detonation, the boss defeat, the screen-clearing super move."
---

import bomber_hero from '/img/instruments/videomancer/bomber/bomber_hero.png';
import bomber_before_after from '/img/instruments/videomancer/bomber/bomber_before_after.png';
import bomber_control_panel from '/img/instruments/videomancer/bomber/bomber_control_panel.png';
import bomber_exercise1_result from '/img/instruments/videomancer/bomber/bomber_exercise1_result.png';
import bomber_exercise2_result from '/img/instruments/videomancer/bomber/bomber_exercise2_result.png';
import bomber_exercise3_result from '/img/instruments/videomancer/bomber/bomber_exercise3_result.png';

# Bomber

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={bomber_hero} alt="Bomber hero image"/>
*Bomber launching an expanding concentric shockwave with white flash effect, the ring sweeping outward from center and leaving a dimmed aftermath in its wake.*
<img src={bomber_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Bomber applied.*

---

## Overview

Every arcade game has its moment of spectacle — the bomb detonation, the boss defeat, the screen-clearing super move. What they share is the **radial shockwave**: an expanding ring of visual energy that transforms everything it touches. Bomber recreates this mechanic as a video processing effect. An expanding concentric ring emanates from a triggerable center point, carrying one of eight selectable visual effects — white flash, inversion, dissolve, color blast, displacement, posterization, ripple, or reveal — as it sweeps across the image. Behind the ring, the video either returns to normal or remains transformed, depending on the post-wave mode.

The program chains four processing stages: input registration with per-pixel distance calculation, zone classification based on ring geometry, effect application within the wavefront zone, and composite output through a wet/dry mix. A separate per-frame engine expands the ring radius, handles auto-triggering at configurable intervals, and drifts the center point along a two-dimensional Lissajous path for non-repeating blast positions. The name references both the explosive mechanic and Hudson Soft's 1983 arcade classic *Bomber* (later *Bomberman*), where grid-based chain detonations defined a genre.

At conservative settings — slow speed, narrow ring, flash effect — Bomber produces clean geometric halos that sweep gracefully across the image. At extreme settings — rapid auto-trigger, wide ring, multi-wave stacking, dissolve or ripple effect — it generates overlapping shockwaves of noise and distortion that consume the input signal in a cascade of visual chaos.

---

## Background

### Arcade Explosions and the Radial Shockwave

The explosion is gaming's most universal moment of visual impact. Defender (Williams, 1981) scattered pixel particles across its bitmap display. Bomber (Hudson Soft, 1983) filled grid cells in expanding cross patterns. R-Type (Irem, 1987) detonated bosses in expanding circles of white flash. Metal Slug (Nazca, 1996) delivered hand-animated pyrotechnics that remain the gold standard of two-dimensional explosions. Each hardware generation had its own explosion language, shaped by the capabilities and constraints of the display technology.

But the most hardware-characteristic explosion pattern is the **radial shockwave wipe** — where a detonation point produces an expanding ring of visual transformation. This pattern appears in boss-defeat sequences (the screen goes white in an expanding circle), stage transitions (the next level is revealed behind an expanding ring), and power-up effects (a blast wave distorts everything in its path). The ring itself carries the visual energy: brightness flash, color inversion, displacement, or dissolve. What makes it different from a simple circular wipe is the active zone — the ring is not a boundary but a region, with distinct behavior inside, on, and outside the wavefront.

### Radial Wipes in Broadcast Video

Television production has used circular and radial wipes since the earliest days of electronic switching. The standard SMPTE wipe set (Society of Motion Picture and Television Engineers) includes circle reveal, iris open/close, and expanding ring transitions. These are clean geometric boundaries that separate two video sources — one inside the wipe, one outside.

Bomber extends this broadcast concept by adding an **active effect zone** within the wipe boundary. Instead of simply revealing a second source behind an expanding circle, Bomber transforms the single input signal differently at each radial zone. The wavefront ring is not just a transition edge but a carrier of visual effects — a moving processing region that applies flash, inversion, noise, or displacement to every pixel it passes over. The result is closer to a cinematic shockwave than a clean broadcast transition.

### The Alpha-Max-Beta-Min Distance Approximation

Computing the Euclidean distance from each pixel to the blast center requires a square root — an expensive operation on FPGA hardware without dedicated DSP multipliers. The **alpha-max-plus-beta-min** approximation replaces the square root with a weighted sum of the absolute coordinate differences. Given horizontal offset dx and vertical offset dy from the center point:

$$\text{dist} \approx \max(|dx|, |dy|) + \tfrac{5}{8} \times \min(|dx|, |dy|)$$

Implemented in hardware as three shifts and an add: $\max + \min \gg 1 + \min \gg 3$. The approximation produces an octagonal iso-distance contour rather than a true circle — the ring's shape is slightly faceted at the diagonals. At video resolution, this faceting is invisible. The approximation runs in a single clock cycle with zero BRAM and minimal LUT usage, enabling real-time per-pixel distance classification at 74.25 MHz.

### Lissajous Figures and Center Drift

When auto-triggering successive blasts, a fixed center point produces concentric rings centered on the same spot — visually repetitive. Bomber optionally drifts the center point along a **Lissajous curve**, a two-dimensional parametric path defined by sinusoidal oscillations on independent axes with different frequencies.

The Lissajous path is generated from a 32-entry sine lookup table with coprime phase increments — 3 per frame for the horizontal axis and 5 per frame for the vertical axis. Because 3 and 5 share no common factors, the path does not repeat until both phases simultaneously return to their starting positions ($3 \times 5 \times 32 = 480$ frames at minimum). The result is a wandering, non-repeating trajectory that scatters successive blast centers across the image. The drift amplitude is controllable from zero (fixed center) to full-range (center can reach beyond the image edges).


---

## Signal Flow

```
Wave Generator (per frame, at vsync)
├── Radius += Speed >> 2
├── Auto-trigger: counter vs Auto Rate threshold
├── Lissajous center: sine LUT with coprime phase increments (3, 5)
└── Deactivate when radius > 1600
         │
         │  ring_radius, wave_active, center_x, center_y
         ▼
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register (1 clk) ────────────────────────────
│   ├── Register Y, U, V inputs
│   ├── dx = hcount − center_x
│   └── dy = vcount − center_y
│
├── Stage 2: Distance Calculation (1 clk) ──────────────────────
│   ├── abs_dx, abs_dy
│   └── dist = max(abs_dx, abs_dy) + min/2 + min/8
│
├── Stage 3: Zone Classification + Effect (1 clk) ──────────────
│   ├── ring_inner = radius − ring_width (clamped ≥ 0)
│   ├── ring_outer = radius + ring_width
│   │
│   ├── Zone "00" — No wave (wave_active = 0): passthrough
│   ├── Zone "01" — Pre-wave (dist > ring_outer): passthrough
│   ├── Zone "10" — Wavefront (ring_inner ≤ dist ≤ ring_outer):
│   │   ├── Flash:     Y = Flash Brt, U/V = 512
│   │   ├── Invert:    Y/U/V = NOT(input)
│   │   ├── Displace:  Y = Y/2 + dist/4
│   │   ├── Dissolve:  Y/U/V = LFSR noise
│   │   ├── Color:     Y = Flash Brt, U/V = quadrant hue
│   │   ├── Reveal:    Y = Flash Brt / 2, U/V = 512
│   │   ├── Posterize: Y/U/V = top 2 bits, zero lower 8
│   │   └── Ripple:    Y += (LFSR − 512) >> 2
│   │
│   └── Zone "11" — Post-wave (dist < ring_inner):
│       ├── Pass mode: passthrough
│       └── Latch mode: Y = Y − (Y × Post Intns) >> 10
│
├── Stage 4: Composite Output (1 clk) ──────────────────────────
│   └── Register effect output
│
├── Interpolator Mix (4 clks) ──────────────────────────────────
│   └── result = lerp(dry, wet, Mix)    ×3 (Y, U, V)
│
├── Sync Delay Pipeline (8 clks) ───────────────────────────────
│   └── Aligned hsync, vsync, field, dry Y/U/V
│
└── Bypass Mux ─────────────────────────────────────────────────
    └── Output = bypass ? delayed_input : mixed_output
```

Two key architectural features define Bomber's character. First, the **zone classification** is purely radial — every pixel is classified solely by its distance from the current center point, creating perfect concentric ring geometry (octagonal due to the alpha-max-beta-min approximation). There is no angular variation in the zone boundaries, though some effects (Color Blast) introduce angular variation within the wavefront zone itself. Second, the **wave generator operates at frame rate** — the ring radius expands once per vsync, not per pixel. This means the ring geometry is constant within a single frame; the effect is a spatial pattern that changes from frame to frame, not a per-pixel temporal effect.

The LFSR (Linear Feedback Shift Register) is a 16-bit pseudo-random generator seeded at `0xDEAD` with polynomial feedback (taps at bits 15, 13, 12, 10). It advances once per pixel clock, producing a different noise value for every pixel in the frame. The Dissolve and Ripple effects sample this running noise, creating spatially varied patterns within the wavefront ring.

---

## Parameter Reference

<img src={bomber_control_panel} alt="Videomancer front panel with Bomber loaded"/>
*Videomancer's front panel with Bomber active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the wave expansion rate — how many pixels the ring radius grows per video frame. At 0%, the ring is frozen in place. At higher values, the ring expands faster, sweeping across the image in fewer frames. The expansion rate is the register value right-shifted by 2 (divided by 4), so at maximum setting the ring advances approximately 255 pixels per frame — fast enough to clear a 1080p screen in about six frames. At very low settings (under 5%), the expansion is slow enough to study the ring structure in detail.

---

#### Knob 2 — Ring Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the thickness of the active wavefront ring — the radial distance over which the selected effect is applied. The ring width is added to and subtracted from the current radius to define the outer and inner boundaries of the effect zone. At 0%, the wavefront is a single-pixel-thin line (nearly invisible). At higher values, the ring broadens into a wide band of effect. A wide ring combined with a slow speed creates a gradual, sweeping transformation; a narrow ring with high speed creates a sharp, fast-moving edge of visual impact.

---

#### Knob 3 — Auto Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the interval between auto-triggered waves when Trigger mode is set to Auto. The auto-trigger counter increments once per frame and fires a new wave when it reaches the threshold set by this control. Lower values fire waves more frequently (rapid bombardment); higher values space them out. At 0%, waves fire every frame — continuous shockwave generation. Combined with Multi Wave mode, rapid auto-triggering creates dense overlapping ring patterns.

---

#### Knob 4 — Center Dft
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the amplitude of the Lissajous center drift — how far the blast center wanders from the default screen center between successive auto-triggered waves. At 0% (default), all waves originate from the exact center of the image. As you increase this control, the center follows a two-dimensional Lissajous path with coprime frequency ratios (3:5), creating a smoothly wandering, non-repeating trajectory. At maximum, the center can drift well beyond the visible image area, producing off-center blasts whose rings enter from the edges.

---

#### Knob 5 — Post Intns
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the intensity of the post-wave dimming when Post Mode is set to Latch. In latch mode, pixels behind the expanding ring (the post-wave zone) are darkened by subtracting a fraction of their luminance: the fraction equals this control's register value divided by 1024. At 0%, no dimming occurs — the post-wave area looks identical to the input. At 50%, luminance is halved. At 100%, the post-wave area is driven to black. In Pass mode, this control has no visible effect since the post-wave zone simply passes the input unchanged.

---

#### Knob 6 — Flash Brt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Sets the brightness level used by the Flash, Color, and Reveal wavefront effects. Flash drives the wavefront luminance to this value with neutral chroma (white flash). Color uses this value as the wavefront luminance while deriving chroma from the pixel's angular position relative to the center. Reveal uses half this value for a dimmer neutral flash. At maximum (default), Flash produces a full white ring. Reducing this control dims the flash to gray, creating a subtler wavefront. Has no effect on Invert, Displace, Dissolve, Posterize, or Ripple modes.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Effect** | Flash | Invert |
| **8 — Post Mode** | Pass | Latch |
| **9 — Trigger** | Manual | Auto |
| **10 — Multi Wave** | Single | Multi |
| **11 — Bypass** | Off | On |

Toggle 7 is a 3-bit selector (steps_8 mode) choosing one of eight wavefront effects — this is the primary creative control determining what the expanding ring does to the image. Toggles 8–10 control wave behavior: post-wave treatment (pass or latch), trigger mode (manual or auto), and wave stacking (single or multi). Toggle 11 is the standard bypass. The effect selection and behavior toggles are independent — any effect can be combined with any post-wave mode and trigger configuration.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the processed and unprocessed signal via the interpolator. At 0%, the output is the original input regardless of effect settings. At 100% (default), the full processed signal is output. Intermediate values blend the effect with the clean signal, useful for softening aggressive effects like Dissolve or reducing the visual impact of the wavefront flash.

---

## Guided Exercises

These exercises progress from a single clean shockwave to overlapping multi-wave chaos. Each introduces new controls while building on the previous configuration.

### Exercise 1: The Expanding Ring

<img src={bomber_exercise1_result} alt="The Expanding Ring result"/>
*The Expanding Ring — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and saturated color.

**Objective**: Observe the basic shockwave mechanic — an expanding ring of white flash sweeping outward from the image center.

1. **Set a slow speed**: Turn Speed to approximately 5%. The ring should expand slowly enough to study its geometry.
2. **Widen the ring**: Set Ring Width to approximately 15%. A wider ring makes the wavefront clearly visible.
3. **Trigger a wave**: With Trigger in Auto mode and Auto Rate at approximately 25%, waves fire periodically. Watch the expanding white circle sweep across the image.
4. **Compare effects**: Cycle through the Effect toggle: Flash produces a clean white ring, Invert creates a photographic-negative ring, Dissolve replaces the ring with noise. Each effect changes only the wavefront zone — the surrounding image is untouched.
5. **Adjust brightness**: With Flash selected, sweep the Flash Brt control. At maximum, the ring is pure white. Reducing it dims the flash to progressively darker gray.

**Key concepts**: The blast center is fixed at the image center, the ring expands at a constant rate per frame, the wavefront zone applies the selected effect while pre-wave and post-wave zones pass the input unchanged

---

### Exercise 2: Aftermath and Latch

<img src={bomber_exercise2_result} alt="Aftermath and Latch result"/>
*Aftermath and Latch — simulated result across source images.*
**Source**: High-contrast footage with a mix of bright and dark regions — shows dimming effect clearly.

**Objective**: Explore post-wave latch mode, where the expanding ring leaves a darkened aftermath across the image.

1. **Enable latch**: Set Post Mode to Latch and Post Intns to approximately 50%. Now the area behind the ring will be visibly darkened.
2. **Slow expansion**: Keep Speed at approximately 5% to watch the aftermath grow behind the ring.
3. **Trigger a wave**: With auto-trigger enabled, observe how the expanding ring leaves a dimmed region behind it. The dimming amount matches the Post Intns setting.
4. **Increase post intensity**: Sweep Post Intns from 0% to 100%. At 0%, no dimming (same as Pass mode). At 50%, half brightness. At 100%, the post-wave area goes to black — the ring erases the image as it passes.
5. **Try Invert + Latch**: Switch the Effect to Invert. Now the ring inverts the image, and the post-wave latch dims the inverted result. The combination creates a dramatic before/after split as the ring expands.

**Key concepts**: Post-wave latch transforms the aftermath, Post Intns controls dimming depth, latch mode combined with different effects creates layered visual transformations

---

### Exercise 3: Bombardment

<img src={bomber_exercise3_result} alt="Bombardment result"/>
*Bombardment — simulated result across source images.*
**Source**: Any footage — the source will be largely consumed by overlapping shockwaves.

**Objective**: Combine auto-trigger, multi-wave, Lissajous center drift, and the Dissolve effect for maximal visual chaos.

1. **Enable multi-wave**: Set Multi Wave to Multi. New triggers no longer reset the existing wave — rings accumulate.
2. **Enable auto-trigger with rapid rate**: Set Trigger to Auto and Auto Rate to approximately 15%. Waves fire frequently.
3. **Enable center drift**: Set Center Dft to approximately 40%. Successive blasts now originate from different positions along the Lissajous path.
4. **Select Dissolve**: Set Effect to Dissolve. Each wavefront ring replaces pixels with LFSR noise — a fizzing disintegration.
5. **Enable latch**: Set Post Mode to Latch and Post Intns to approximately 30%. Each wave leaves a dimmed aftermath, and overlapping post-wave zones compound the darkening.
6. **Increase speed**: Gradually raise Speed to approximately 20%. Faster expansion means each ring covers the screen quickly, and new rings pile up before the old ones finish. The result is a churning field of overlapping noise shockwaves consuming the image.
7. **Reduce mix**: Lower the Mix fader to approximately 60% to blend the chaos with the original signal, softening the effect into a shimmering distortion overlay.

**Key concepts**: Multi-wave allows overlapping concurrent rings, Lissajous drift scatters blast centers across the image, rapid auto-trigger creates dense ring patterns, post-wave latch compounds across overlapping waves

---


## Tips

- **Speed and frame count**: At maximum speed, a wave crosses a 1080p screen in about 6 frames — blink and you miss it. Start below 10% to see the ring structure clearly, then increase for dramatic fast-wipes.
- **Ring width sets the mood**: A narrow ring (under 10%) creates a sharp, precise shockwave edge. A wide ring (over 40%) creates a gradual, sweeping transformation zone. Match ring width to the effect — Flash looks best narrow, Dissolve and Ripple look best wide.
- **Latch mode for reveals**: Set Post Intns to 100% (black aftermath) with a slow Flash ring. As the ring expands, it erases the image to black behind a wall of white light — a dramatic reveal-to-black transition.
- **Color Blast for prismatic rings**: The Color effect divides the wavefront into four angular quadrants, each with a different saturated hue. Combined with a narrow ring and slow speed, this creates a rainbow halo that sweeps outward — delicate and geometric.
- **Feedback loops**: Route the output back to the input with Latch enabled. Each wave compounds the dimming of the previous wave's aftermath, progressively darkening the image with each blast. After several cycles, only the wavefront rings remain visible against black.
- **Mix for subtlety**: Reduce Mix to 30–50% to blend the shockwave with the clean signal. The wavefront becomes a translucent overlay rather than a hard replacement — useful for layering Bomber's effect over other video without fully obscuring the source.
- **Dissolve for disintegration**: The Dissolve effect fills the wavefront with LFSR pseudo-random noise, different for every pixel. Combined with latch mode and rapid auto-trigger, it simulates the image being eaten alive by expanding circles of static.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha-max-beta-min** | A fast approximation of Euclidean distance using weighted sums of absolute coordinate differences, avoiding the need for a square root operation. |
| **Coprime** | Two integers that share no common factor other than 1; coprime frequency ratios prevent Lissajous paths from repeating quickly. |
| **DDS (Direct Digital Synthesis)** | A technique for generating waveforms using a phase accumulator that increments at a controlled rate, producing precise frequency output from a lookup table. |
| **LFSR (Linear Feedback Shift Register)** | A shift register whose input bit is a linear function of its previous state, producing a deterministic pseudo-random bit sequence used here for Dissolve and Ripple effects. |
| **Lissajous curve** | A two-dimensional parametric path traced by sinusoidal oscillations on independent axes with different frequencies, producing non-repeating wandering trajectories. |
| **LUT (Look-Up Table)** | A pre-computed array of values stored in FPGA logic that replaces real-time calculation with a simple memory read. |
| **Posterize** | Reducing the number of discrete tonal levels in an image, creating harsh banding between adjacent brightness or color regions. |
| **Radial wipe** | A video transition where a boundary expands outward from a center point in a circular or ring pattern. |
| **SMPTE** | Society of Motion Picture and Television Engineers, the standards body that defines broadcast video wipe patterns and transition types. |
| **Vsync (Vertical Sync)** | A timing pulse that marks the beginning of each new video frame, used here to trigger per-frame wave expansion. |
| **Wavefront zone** | The annular region between the inner and outer ring boundaries where the active visual effect is applied to each pixel. |
| **YUV** | A color encoding scheme that separates luminance (Y) from chrominance (U, V), widely used in video systems. |

---
