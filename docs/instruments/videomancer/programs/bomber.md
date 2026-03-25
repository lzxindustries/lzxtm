---
draft: true
sidebar_position: 27
slug: /instruments/videomancer/bomber
title: "Bomber"
image: /img/instruments/videomancer/bomber/bomber_hero_s1.png
description: "Every arcade game has its moment of spectacle — the bomb detonation, the boss defeat, the screen-clearing super move."
---

![Bomber hero image](/img/instruments/videomancer/bomber/bomber_hero_s1.png)
*Bomber detonating an expanding shockwave ring over a live video feed, the wavefront carrying a white flash that sweeps outward from the blast center.*

---

## Overview

Bomber is a radial shockwave wipe processor that detonates concentric ring blasts across the video frame. An expanding wavefront emanates from a triggerable center point, carrying one of eight visual effects: white flash, color inversion, dissolve, color blast, and more: as it sweeps across each pixel. Once the wave passes, the aftermath can either revert to the clean input or leave a dimmed, latched impression behind.

At its simplest, Bomber produces dramatic circular wipes: a bright ring expands outward from the center of the screen, swallowing the image. At its most complex, overlapping waves detonate from drifting Lissajous positions, each carrying a different visual payload, layering concentric halos of processed video over the source. The effect is visceral and immediate (a detonation you can see.)

:::tip
Bomber is at its most spectacular when auto-triggering with **Center Drift** engaged. Successive blasts fire from shifting positions, creating overlapping interference patterns that evolve continuously.
:::

### What's In a Name?

The name ***Bomber*** is a direct reference to the arcade game ***Bomberman*** (Hudson Soft, 1983) and the visual language of classic arcade explosions. From Bomberman's grid-filling chain blasts to the screen-clearing detonations of ***R-Type*** (Irem, 1987) and ***Metal Slug*** (Nazca, 1996), the expanding radial shockwave is gaming's most universal moment of spectacle. Bomber distills that explosive energy into a real-time video processing tool: every trigger is a detonation, and every pixel is in the blast radius.

---

## Quick Start

1. Make sure **Trigger** (Switch 9) is set to **Auto** and **Mix** (Fader 12) is at maximum. You should see periodic shockwave rings expanding outward from the center of the screen.
2. Adjust **Speed** (Knob 1) to control how quickly the ring expands. Slower speeds let you see the wave's structure; faster speeds create sudden flashes.
3. Turn **Ring Width** (Knob 2) clockwise to widen the active blast zone. A narrow ring produces a sharp edge; a wide ring creates a soft, gradual transition.
4. Increase **Center Dft** (Knob 4) to engage the ***Lissajous drift***: successive blasts will detonate from different positions, creating overlapping interference patterns.

---

## Parameters

![Videomancer front panel with Bomber loaded](/img/instruments/videomancer/bomber/bomber_control_panel.png)
*Videomancer's front panel with Bomber active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Speed** controls how quickly the shockwave ring expands outward from its detonation point. Each video frame, the ring radius grows by an amount proportional to this value. At 0%, the wave barely moves, crawling outward pixel by pixel. At 100%, the blast tears across the entire screen in just a few frames.

:::note
The ring radius increases by approximately one quarter of the raw Speed value per frame. At high speeds, the ring may expand so fast that the wavefront effect is visible for only a single frame (a dramatic flash rather than a rolling wave.)
:::

---

### Knob 2 — Ring Width

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Ring Width** sets the thickness of the active wavefront zone. The blast ring has an inner and outer boundary, and every pixel whose distance from the center falls between those boundaries receives the selected effect. At 0%, the ring is razor-thin: a single-pixel line of fire sweeping outward. At 100%, the ring is extremely wide, turning the blast into a broad wash that covers most of the screen simultaneously.

Wider rings reveal more of the wavefront effect at any given moment, while narrower rings create sharper, more dramatic transitions.

---

### Knob 3 — Auto Rate

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Auto Rate** controls the interval between automatically triggered waves when **Trigger** (Switch 9) is set to **Auto**. At 0%, waves fire every frame, creating continuous concentric ripples. At 100%, the interval between detonations is long, allowing each wave to fully expand and expire before the next one fires.

:::tip
Very low Auto Rate values with **Multi Wave** (Switch 10) set to **Multi** produce dense concentric ring patterns (like ripples spreading from a stone dropped in water.)
:::

---

### Knob 4 — Center Dft

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Center Dft** (Center Drift) controls the amplitude of a ***Lissajous drift*** applied to the blast center point. At 0%, all waves detonate from dead center. As the value increases, the center traces a smooth, looping figure-eight path driven by two sine oscillators running at different frequencies (a 3:5 ratio). Each successive auto-triggered wave fires from a different position along this path.

The drift is computed from a 32-entry sine lookup table. The horizontal and vertical phase accumulators advance by 3 and 5 steps respectively on each trigger, producing a pattern that repeats every 256 triggers.

---

### Knob 5 — Post Intns

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Post Intns** (Post Intensity) controls the brightness of the aftermath zone when **Post Mode** (Switch 8) is set to **Latch**. In latch mode, pixels behind the wavefront are dimmed proportionally to this value. At 0%, the latch has no dimming effect: the post-wave region looks identical to the input. At 100%, the post-wave region is aggressively darkened. In **Pass** mode, this parameter has no visible effect.

The dimming formula subtracts a fraction of each pixel's own luminance, preserving relative brightness relationships while pulling the entire post-wave region toward black.

---

### Knob 6 — Flash Brt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Flash Brt** (Flash Brightness) controls the luminance level used by wavefront effects that generate their own light: specifically the **White Flash** (mode 0), **Color Blast** (mode 4), and **Freeze/Reveal** (mode 5) effects. At 0%, the flash is black (invisible). At 100%, the flash is maximum white. This parameter has no effect on modes that transform the input signal rather than replacing it (Invert, Displacement, Dissolve, Posterize, Ripple).

---

### Switch 7 — Effect

| Property | Value |
|----------|-------|
| Off | Flash |
| On | Ripple |
| Default | Flash |

**Effect** selects between two families of wavefront effects. In the **Flash** position, the wavefront carries even-numbered effects (White Flash, Radial Displacement, Color Blast, or Posterize). In the **Ripple** position, the wavefront carries odd-numbered effects (Invert, Dissolve, Freeze/Reveal, or Ripple). The specific effect within each family depends on the positions of **Post Mode** (Switch 8) and **Trigger** (Switch 9), which together with Effect form a 3-bit mode selector. See the Toggle Group Notes below for the full 8-mode table.

---

### Switch 8 — Post Mode

| Property | Value |
|----------|-------|
| Off | Pass |
| On | Latch |
| Default | Pass |

**Post Mode** controls what happens to pixels *after* the wavefront has passed over them. In the **Pass** position, once the blast ring moves beyond a pixel, it reverts to the clean input: the wave passes through and leaves no trace. In the **Latch** position, the post-wave region retains a dimmed version of the input, controlled by **Post Intns** (Knob 5). Latch mode creates the visual impression of scorched earth left behind by the blast.

:::note
Post Mode also contributes to the 3-bit wavefront effect selector. Changing it will alter the wavefront effect as well as the post-wave behavior.
:::

---

### Switch 9 — Trigger

| Property | Value |
|----------|-------|
| Off | Manual |
| On | Auto |
| Default | Auto |

**Trigger** selects between manual and automatic wave triggering. In the **Manual** position, a wave fires on the rising edge when you toggle this switch from Auto back to Manual (edge-detected). In the **Auto** position, waves fire periodically at the interval set by **Auto Rate** (Knob 3). Auto mode is the primary way to generate continuous wave patterns.

:::note
Trigger also contributes to the 3-bit wavefront effect selector. Changing from Manual to Auto will switch to a different wavefront effect (see Toggle Group Notes).
:::

---

### Switch 10 — Multi Wave

| Property | Value |
|----------|-------|
| Off | Single |
| On | Multi |
| Default | Single |

**Multi Wave** controls whether new waves can fire while a previous wave is still active. In the **Single** position, a new wave cannot start until the current one has fully expanded past the maximum screen distance and deactivated. In the **Multi** position, waves can be triggered at any time, even while a prior wave is still expanding. Multi mode enables overlapping concentric rings.

:::tip
With Multi Wave on and a fast Auto Rate, you can create dense fields of concentric rings that interfere and overlap: Bomber's most visually complex mode.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all blast processing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

:::note Toggle Group Notes

Switches 7, 8, and 9 form a combined 3-bit wavefront effect selector. Each toggle has its own independent function (effect family selection, post-wave behavior, and trigger mode), but their combined bit pattern also determines which of eight wavefront effects is applied at the blast ring. The full mode table:

| Effect (Sw 7) | Post Mode (Sw 8) | Trigger (Sw 9) | Wavefront Effect |
|---------------|-------------------|-----------------|------------------|
| Flash | Pass | Manual | **White Flash** — pixels driven to Flash Brt luminance, neutral chroma |
| Ripple | Pass | Manual | **Invert** — bitwise complement of all three YUV channels |
| Flash | Latch | Manual | **Radial Displacement** — luminance shifted by distance fraction |
| Ripple | Latch | Manual | **Dissolve** — pixels replaced by LFSR pseudo-random noise |
| Flash | Pass | Auto | **Color Blast** — Flash Brt luminance with quadrant-based saturated hue |
| Ripple | Pass | Auto | **Freeze/Reveal** — grey flash at half Flash Brt |
| Flash | Latch | Auto | **Posterize** — extreme 2-bit quantization of all channels |
| Ripple | Latch | Auto | **Ripple** — LFSR-modulated luminance perturbation |

Because Post Mode and Trigger each serve dual roles, changing either one alters *both* the wavefront effect and the corresponding behavior (post-wave handling or trigger mechanism).

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (blast-processed) output using a per-channel ***interpolator***. At 0%, only the dry signal passes through: no blast effect is visible. At 100%, the full blast-processed output is shown. Intermediate values blend the two, which can soften the visual impact of the wavefront.

---

## Background

### Radial distance and the shockwave metaphor

Every pixel on screen has a distance from the blast center. Bomber computes this distance every clock cycle using the ***alpha-max-plus-beta-min*** approximation: a fast, hardware-friendly alternative to the Pythagorean formula that avoids square roots entirely. The approximation computes:

$$\text{dist} \approx \max(|dx|, |dy|) + \frac{3}{8} \cdot \min(|dx|, |dy|)$$

This produces a distance estimate with roughly 3.5% maximum error. The result is slightly octagonal rather than perfectly circular, but at video rates the difference is imperceptible. The ring appears round.

The expanding ring divides every pixel into one of three zones: ***pre-wave*** (untouched, ahead of the blast), ***wavefront*** (inside the ring, receiving the active effect), and ***post-wave*** (behind the ring, showing the aftermath). This three-zone spatial classification is the core of Bomber's architecture.

### Lissajous center drift

When Center Drift is nonzero, the blast center traces a ***Lissajous figure***: a smooth, looping curve produced by combining two sinusoidal oscillators at different frequencies. Bomber's horizontal oscillator advances 3 steps per trigger while the vertical oscillator advances 5 steps, drawing a 3:5 Lissajous figure that creates complex, non-repeating drift paths. The sine values come from a 32-entry lookup table embedded in the FPGA fabric.

### LFSR noise generation

Several wavefront effects rely on a 16-bit ***linear feedback shift register*** (LFSR) for pseudo-random values. The LFSR advances every pixel clock, generating noise for the Dissolve and Ripple modes. The feedback polynomial taps bits 15, 13, 12, and 10, producing a maximal-length sequence of 65,535 values before repeating.


---

## Signal Flow

### Signal Flow Notes

The processing has two timescales. Per-frame logic (at vsync) manages the wave lifecycle: expanding the ring radius, checking auto-trigger timing, updating the Lissajous center, and detecting manual trigger edges. Per-pixel logic (every clock) computes the distance from the current pixel to the blast center, classifies the pixel into a zone, and applies the appropriate effect.

The wavefront effect engine is a single large case statement that selects among eight processing modes based on the combined toggle state. Some modes generate new pixel data (White Flash, Color Blast, Dissolve), while others transform the input (Invert, Posterize, Ripple, Displacement). The post-wave zone either passes the input unchanged or applies a luminance dimming proportional to Post Intensity.

:::tip
Because the distance calculation and zone classification happen pixel-by-pixel, the ring boundary is truly per-pixel: it follows the octagonal distance contour precisely, with no blockiness or quantization artifacts.
:::


---

## Exercises

These exercises progress from a single dramatic blast to complex layered detonation patterns. Each exercise builds on the previous, introducing more of Bomber's wavefront and triggering capabilities.
### Exercise 1: The First Blast

![The First Blast result](/img/instruments/videomancer/bomber/bomber_ex1_s1.png)
*The First Blast — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A single, dramatic white-flash shockwave expanding from the center of the screen.

#### Key Concepts

- The expanding radial wipe is Bomber's core visual gesture
- Speed and Ring Width define the blast's character
- Flash Brightness controls the intensity of flash-based effects

#### Video Source

A live camera feed or recorded footage with visible detail across the frame.

#### Steps

1. Set **Trigger** (Switch 9) to **Manual** and **Effect** (Switch 7) to **Flash**. The screen shows undisturbed input.
2. Set **Speed** (Knob 1) to about 30% and **Ring Width** (Knob 2) to about 25%.
3. Set **Flash Brt** (Knob 6) to maximum and **Mix** (Fader 12) to maximum.
4. Toggle **Trigger** to **Auto** and back to **Manual** to fire a single wave. A white ring expands from the center, sweeping across the entire frame.
5. Adjust **Speed** and **Ring Width** to shape the blast. Slower speed with narrow ring creates a precise, surgical wipe. Faster speed with wide ring creates an explosive flash.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~30% |
| Ring Width | ~25% |
| Auto Rate | 25% |
| Center Dft | 0% |
| Post Intns | 50% |
| Flash Brt | 100% |
| Effect | Flash |
| Post Mode | Pass |
| Trigger | Manual |
| Multi Wave | Single |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Concentric Ripples

![Concentric Ripples result](/img/instruments/videomancer/bomber/bomber_ex2_s1.png)
*Concentric Ripples — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A continuous field of expanding concentric rings drifting across the screen, creating interference patterns.

#### Key Concepts

- Auto-trigger creates periodic waves
- Multi Wave enables overlapping ring patterns
- Center Drift moves the detonation point along a Lissajous path

#### Video Source

Footage with mid-range brightness and some texture (a landscape, a face, or abstract patterns.)

#### Steps

1. Set **Trigger** (Switch 9) to **Auto** and **Multi Wave** (Switch 10) to **Multi**.
2. Set **Speed** (Knob 1) to about 40% and **Auto Rate** (Knob 3) to about 20%. Rings should fire frequently and expand at a moderate pace.
3. Increase **Ring Width** (Knob 2) to about 40%. The overlapping rings create bands of processed and unprocessed video.
4. Turn **Center Dft** (Knob 4) to about 50%. The blast center begins tracing a smooth figure-eight path, so rings emerge from different positions on each trigger.
5. Try different effects: toggle **Effect** (Switch 7) to **Ripple** to switch from White Flash to Invert mode. The concentric rings now carry inverted video instead of white flash.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~40% |
| Ring Width | ~40% |
| Auto Rate | ~20% |
| Center Dft | ~50% |
| Post Intns | 50% |
| Flash Brt | 100% |
| Effect | Ripple |
| Post Mode | Pass |
| Trigger | Auto |
| Multi Wave | Multi |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Scorched Earth

![Scorched Earth result](/img/instruments/videomancer/bomber/bomber_ex3_s1.png)
*Scorched Earth — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An aftermath landscape where each blast leaves a darkened scar on the image, building up layers of destruction.

#### Key Concepts

- Latch mode creates persistent aftermath zones
- Post Intensity controls the severity of the aftermath dimming
- Toggle combinations select different wavefront effects

#### Video Source

High-contrast footage or a colorful still image: the darkening effect is most visible against bright content.

#### Steps

1. Set **Post Mode** (Switch 8) to **Latch** and **Trigger** (Switch 9) to **Auto**. This selects the Posterize wavefront effect (mode 110).
2. Set **Speed** (Knob 1) to about 25% and **Auto Rate** (Knob 3) to about 60% (moderate interval between detonations).
3. Set **Post Intns** (Knob 5) to about 70%. The aftermath zone behind each passing ring is noticeably darkened.
4. Watch as successive waves sweep across the frame. Each pass leaves a dimmer post-wave zone. The cumulative effect builds up, darkening the image with each detonation.
5. Toggle **Effect** (Switch 7) to **Ripple** to switch the wavefront from Posterize to Ripple effect (mode 111). The wavefront now carries a noisy luminance perturbation, with the same darkened latch behind it.
6. Adjust **Mix** (Fader 12) to about 60% to blend the scorched result with the clean input, softening the destruction.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~25% |
| Ring Width | ~30% |
| Auto Rate | ~60% |
| Center Dft | ~40% |
| Post Intns | ~70% |
| Flash Brt | 100% |
| Effect | Ripple |
| Post Mode | Latch |
| Trigger | Auto |
| Multi Wave | Single |
| Bypass | Off |
| Mix | ~60% |

---
## Glossary

- **Alpha-Max-Plus-Beta-Min**: A fast distance approximation that avoids square roots by combining the larger and smaller coordinate differences with fixed coefficients; produces slightly octagonal distance contours.

- **Blast Radius**: The distance from the detonation center to the outer edge of the expanding wavefront ring.

- **Interpolator**: A crossfade circuit that blends two signals by a fractional amount; used here for the wet/dry mix between processed and clean video.

- **LFSR**: Linear Feedback Shift Register; a shift register with XOR feedback taps that generates a deterministic pseudo-random sequence. Used for Dissolve and Ripple effects.

- **Lissajous Figure**: A smooth, looping curve produced by combining two sinusoidal oscillators at different frequencies; used to drift the blast center.

- **Posterization**: Reducing pixel values to a very small number of discrete levels, creating hard-edged flat color regions.

- **Radial Wipe**: A transition effect where content is revealed or concealed by an expanding circle or ring.

- **Shockwave**: The expanding ring wavefront that carries visual effects as it sweeps across the frame.

- **Wavefront**: The active effect zone within the expanding ring, bounded by the inner and outer ring radii.

- **Zone Classification**: The per-pixel determination of whether a pixel is in the pre-wave, wavefront, or post-wave region relative to the current ring position.

---
