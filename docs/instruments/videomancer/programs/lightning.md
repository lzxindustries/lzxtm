---
draft: true
sidebar_position: 171
slug: /instruments/videomancer/lightning
title: "Lightning"
image: /img/instruments/videomancer/lightning/lightning_hero_s1.png
description: "Lightning is a processing program that renders one or two bright, jagged bolt paths from the top to the bottom of the frame, overlaid additively onto the input video."
---

![Lightning hero image](/img/instruments/videomancer/lightning/lightning_hero_s1.png)
*A jagged bolt of electric discharge tears down the screen, forking and flashing over the source image like a captured moment of storm.*

---

## Overview

Lightning renders a procedural electrical discharge bolt that strikes vertically down the screen. The bolt's path is a ***random walk***: at each scanline, a pseudo-random offset shifts the bolt's horizontal position left or right, producing the jagged, branching silhouette of a real lightning strike. The bolt glows brightest at its center and fades with distance, creating a soft luminous halo that lights up the source video beneath it.

The bolt can fork partway down the screen, splitting into a primary trunk and a secondary branch that diverges at double the jitter rate. A second bolt can be added in **Arc** mode, mirroring the primary bolt's jitter in the opposite direction. A ***DDS flash accumulator*** drives periodic bright flashes followed by dimmer inter-flash periods, simulating the staccato rhythm of an electrical storm. The flash timing can be made irregular with pseudo-random perturbation.

Lightning is an additive overlay effect: the bolt's brightness is summed onto the source video rather than replacing it. At full mix, the bolt burns over the source image like a bright scar. Pulling the mix fader back blends the effect gently into the scene. The result ranges from subtle flickers of illumination to full-frame electrical chaos.

:::tip
Lightning is at its most dramatic over dark footage. The bolt's additive brightness has room to glow against a dark background, whereas a bright source compresses the effect toward white clipping.
:::

### What's In a Name?

The name ***Lightning*** needs no metaphor. The program generates a procedural lightning bolt: a jagged, branching electrical discharge rendered in real time on every frame. Like its natural counterpart, the bolt follows an unpredictable path from top to bottom, forks into branches, and illuminates its surroundings with sudden, blinding flashes.

---

## Quick Start

1. Send a dark or moderately lit video source into Videomancer and load **Lightning**. A glowing bolt should appear running vertically through the center of the image, flickering over the source.
2. Turn **Bolt W** (Knob 1) clockwise to widen the bolt's glow. The luminous halo around the bolt's center expands, lighting a broader area of the source image.
3. Increase **Branch P** (Knob 2) to add more horizontal jitter per scanline. The bolt's path becomes increasingly jagged and erratic: a gentle zigzag at low values, a violent scribble at high values.
4. Set **Style** (Switch 7) to **Arc**. A second bolt appears, mirroring the first with opposite jitter, as though electricity is arcing between two points.

---

## Parameters

![Videomancer front panel with Lightning loaded](/img/instruments/videomancer/lightning/lightning_control_panel.png)
*Videomancer's front panel with Lightning active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Bolt W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bolt W** controls the width of the bolt's luminous glow. At 0%, the bolt is a thin, tight line just a few pixels wide. As the value increases, the bright core expands outward, illuminating a wider swath of the screen. At 100%, the bolt's halo stretches across a substantial portion of the image, creating a broad wash of additive brightness. The brightness falls off with distance from the bolt's center: pixels near the core are brightest, dimming smoothly toward the edges.

---

### Knob 2 — Branch P

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Branch P** controls the amplitude of horizontal jitter applied to the bolt at each scanline. At 0%, the bolt falls nearly straight down the screen with minimal deviation: a taut wire of light. As the value increases, each scanline's random offset grows larger, making the bolt's path increasingly jagged and erratic. At 100%, the jitter is at maximum amplitude and the bolt whips wildly from side to side across the frame. This jitter is what gives the bolt its characteristic lightning-strike silhouette: the more jitter, the more the bolt resembles a real branching discharge.

:::note
The jitter is also doubled for the branch fork, so increasing **Branch P** causes branches to diverge from the main trunk more aggressively.
:::

---

### Knob 3 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bright** controls the bolt's peak luminance: the maximum brightness added to the source at the bolt's center. At 0%, the bolt is invisible. As the value increases, the bolt's core brightens, and the glow halo intensifies proportionally. At 100%, the bolt burns at full intensity, easily clipping to white when added to anything but the darkest source material. This control sets the ceiling that the flash modulation and distance falloff work within.

---

### Knob 4 — Flash Frq

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Flash Frq** controls the rate of the flash cycle. Lightning's brightness alternates between full intensity during a flash and one-quarter intensity between flashes. At 0%, the flash DDS accumulator advances very slowly, producing long, slow pulses. As the value increases, flashes become more rapid and the bolt strobes with increasing urgency. At 100%, the flash cycle is at maximum speed. When **Flash** (Switch 9) is set to **On**, randomness is added to the flash timing, producing irregular, naturalistic flicker.

---

### Knob 5 — Jitter

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Jitter** controls the bolt's peak brightness scaling factor. At 0%, the bolt is completely dark: no glow is rendered. Increasing the value raises the bolt's brightness ceiling. At 100%, the bolt reaches its maximum radiance. This control works in concert with **Bright** (Knob 3) and the flash modulation stage to determine the final visible intensity of each pixel along the bolt's path.

---

### Knob 6 — Tint

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Tint** is reserved for future use. Adjusting this knob has no effect on the output in the current version of Lightning.

---

### Switch 7 — Style

| Property | Value |
|----------|-------|
| Off | Bolt |
| On | Arc |
| Default | Bolt |

**Style** selects between single-bolt and dual-bolt rendering. With the switch set to **Bolt**, a single lightning bolt descends from the top center of the screen. With the switch set to **Arc**, a second bolt appears, starting from a quarter-screen offset and applying jitter in the opposite direction of the first bolt. The two bolts mirror each other's zigzag motions, creating the visual impression of electricity arcing between two terminals. The closest bolt to any given pixel determines that pixel's brightness contribution.

---

### Switch 8 — Color

| Property | Value |
|----------|-------|
| Off | White |
| On | Gold |
| Default | White |

**Color** selects the bolt's color rendering. With the switch set to **White**, the bolt is rendered as pure additive luminance: a colorless white glow layered over the source video's existing chrominance. With the switch set to **Gold**, the bolt takes on a blue-purple tint. When the bolt is bright enough, its chrominance channels are shifted above neutral, pushing Cb higher than Cr and producing a cool violet-blue cast along the discharge path. The tint strength scales with bolt brightness: brighter regions are more saturated, while dim inter-flash glow remains close to neutral.

:::tip
The **Gold** color mode is most visible against desaturated or dark source material. Over colorful footage, the tint blends into the source chrominance and may be subtle.
:::

---

### Switch 9 — Flash

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Flash** selects between regular and random flash timing. With the switch set to **Off**, the flash DDS accumulator advances by a fixed increment each frame, producing evenly spaced periodic flashes: a steady strobe rhythm. With the switch set to **On**, a pseudo-random value from the LFSR is added to each frame's DDS increment. This breaks the regularity of the flash timing, producing the irregular, unpredictable flicker of a natural electrical storm.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** is reserved for future use. Toggling this switch has no effect on the output in the current version of Lightning.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Lightning processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw source and the lightning-overlaid result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) and wet (bolt-overlaid) signals. At 0%, the output is the original source with no lightning visible. At 100%, the full bolt effect is applied. Intermediate positions blend the bolt into the source at reduced opacity, useful for achieving subtle background flickers or gentle luminous accents rather than a full-intensity discharge.

---

## Background

### Procedural lightning generation

Real lightning follows an unpredictable path dictated by the electrical resistance of the atmosphere. Videomancer's Lightning simulates this with a ***random walk***: a mathematical process where each step's position depends on the previous step plus a random offset. At each scanline, the bolt's horizontal position shifts left or right by a small pseudo-random amount drawn from a 16-bit ***linear feedback shift register*** (LFSR). Over the course of a full frame, these accumulated offsets trace a jagged, branching path from the top of the screen to the bottom.

The bolt resets to the horizontal center at each new frame (on vertical sync), so each frame produces a unique discharge path. The branch fork begins at a vertical position determined by the **Flash Frq** parameter and diverges from the primary bolt with doubled jitter, simulating the way real lightning splits into secondary channels as it propagates.

### Distance falloff and additive compositing

The bolt's visible glow is computed as a ***distance falloff*** function. For every pixel on screen, Lightning calculates the absolute horizontal distance to the nearest bolt segment (primary, secondary, or branch). If the pixel falls within the bolt's width, its brightness is computed as the peak brightness minus a scaled version of its distance from the bolt center. Pixels at the very core of the bolt receive full brightness. Pixels at the edge of the glow halo receive near-zero brightness. Pixels beyond the bolt width receive nothing.

This brightness value is then ***additively composited*** onto the source video: the bolt's glow is summed with the source luminance and clamped so it cannot exceed maximum white. The addition means the bolt always brightens the image: it never darkens or replaces the source. This additive model is why lightning effects look most dramatic over dark footage.

### Flash modulation

Natural lightning doesn't glow continuously: it fires in brief, intense flashes separated by dimmer pauses. Lightning models this with a ***direct digital synthesizer*** (DDS) phase accumulator that advances once per frame. When the accumulator's upper three bits equal `111`, the bolt is at full brightness (a flash). Between flashes, the bolt brightness is reduced to one-quarter intensity, producing a faint residual glow.

The DDS increment maps to the **Flash Frq** parameter, so higher values produce faster flash cycling. Enabling the **Flash** toggle adds a pseudo-random perturbation from the LFSR to each frame's increment, breaking the regularity and producing an organic, unpredictable strobe.


---

## Signal Flow

### Signal Flow Notes

Two key architectural features define Lightning's pipeline:

1. **Additive compositing with no feedback.** The bolt's brightness is computed independently from the source video and then added to the source luminance. The bolt path computation depends only on the LFSR, not on the source image content. This means the bolt always looks the same regardless of source material (only the composite result changes.)

2. **Per-scanline random walk with per-frame reset.** The bolt position accumulator updates once per horizontal sync, accumulating jitter across scanlines. At vertical sync, the accumulator resets to center (or quarter-screen for the secondary bolt). Each frame therefore produces an entirely new bolt shape, creating the flickering, re-striking character of natural lightning.

:::note
The branch fork diverges with *doubled* jitter, so it separates from the primary bolt faster the farther it travels below the fork point. The fork point itself is set by the **Flash Frq** parameter (lower values move the fork higher on screen.)
:::


---

## Exercises

These exercises progress from a simple single bolt to a full electrical storm composition. Each exercise builds on the previous, engaging more of Lightning's parameter space.
### Exercise 1: Single Bolt Study

![Single Bolt Study result](/img/instruments/videomancer/lightning/lightning_ex1_s1.png)
*Single Bolt Study — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A single, controllable lightning bolt over dark source material, exploring how width and jitter shape its appearance.

#### Key Concepts

- Random walk creates jagged bolt paths
- Width controls glow radius, not bolt count
- Jitter amplitude shapes the bolt's character

#### Video Source

Dark or low-key footage (a night sky, a dimly lit room, or black leader.)

#### Steps

1. **Establish the bolt**: With default settings, observe the single bolt flickering down the center of the screen. Notice how its path changes every frame.
2. **Narrow the bolt**: Turn **Bolt W** (Knob 1) fully counterclockwise. The bolt becomes a thin bright line (sharp and clinical.)
3. **Widen the glow**: Now sweep **Bolt W** clockwise. The bolt's core stays fixed but its luminous aura expands outward, illuminating a broader swath of the source.
4. **Add jitter**: Increase **Branch P** (Knob 2) from the default. The bolt's path becomes more erratic, zigzagging aggressively from scanline to scanline.
5. **Reduce jitter**: Pull **Branch P** back toward zero. The bolt straightens into a nearly vertical column of light.
6. **Adjust brightness**: Sweep **Jitter** (Knob 5) to control peak intensity. Find the balance where the bolt glows without clipping the source to solid white.

#### Settings

| Control | Value |
|---------|-------|
| Bolt W | ~50% |
| Branch P | ~60% |
| Bright | 50% |
| Flash Frq | 0% |
| Jitter | ~70% |
| Tint | 50% |
| Style | Bolt |
| Color | White |
| Flash | Off |
| Animate | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Arcing and Branching

![Arcing and Branching result](/img/instruments/videomancer/lightning/lightning_ex2_s1.png)
*Arcing and Branching — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dual-bolt arc with a forking branch and animated flash strobing, resembling an active electrical discharge between two points.

#### Key Concepts

- Arc mode adds a mirrored second bolt with opposite jitter
- The branch fork creates a Y-shaped discharge
- Flash timing animates the bolt's intensity over time

#### Video Source

Medium-brightness footage with visible detail (urban scenery, architectural subjects, or a still life.)

#### Steps

1. **Enable Arc mode**: Set **Style** (Switch 7) to **Arc**. A second bolt appears, offset from center, with jitter mirrored relative to the first.
2. **Increase jitter**: Raise **Branch P** (Knob 2) to about 70%. Both bolts zigzag aggressively, and you can see how their opposite jitter creates a spreading arc pattern.
3. **Activate flash**: Increase **Flash Frq** (Knob 4) to add flash cycling. The bolts strobe between full brightness and a dim afterglow.
4. **Randomize flash**: Set **Flash** (Switch 9) to **On**. The regular strobe breaks into irregular, storm-like flickering.
5. **Add color tint**: Set **Color** (Switch 8) to **Gold**. The bolt takes on a cool tint visible along its brightest regions.
6. **Blend**: Pull **Mix** (Fader 12) back to about 60% to let the source image show through the discharge pattern.

#### Settings

| Control | Value |
|---------|-------|
| Bolt W | ~40% |
| Branch P | ~70% |
| Bright | 50% |
| Flash Frq | ~50% |
| Jitter | ~60% |
| Tint | 50% |
| Style | Arc |
| Color | Gold |
| Flash | On |
| Animate | Off |
| Bypass | Off |
| Mix | ~60% |

---

### Exercise 3: Electric Storm

![Electric Storm result](/img/instruments/videomancer/lightning/lightning_ex3_s1.png)
*Electric Storm — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A full-intensity electrical storm composite: wide, fast, branching, and tinted, layered over dramatic source footage.

#### Key Concepts

- High jitter + wide bolts + fast flash = chaotic storm energy
- Mixing back from 100% softens the effect into the source
- Color tint adds atmospheric mood to the discharge

#### Video Source

High-contrast footage (stormy skies, industrial landscapes, or abstract textures.)

#### Steps

1. **Maximum chaos**: Set **Branch P** (Knob 2) high (~80%), **Bolt W** (Knob 1) to about 70%, and **Jitter** (Knob 5) to about 60%. The bolt becomes a wide, violently jagged discharge.
2. **Fast random flash**: Set **Flash Frq** (Knob 4) to about 60% and enable **Flash** (Switch 9). The bolt strobes rapidly and irregularly.
3. **Enable Arc mode**: Set **Style** (Switch 7) to **Arc**. Two bolts tear across the screen simultaneously.
4. **Color the storm**: Set **Color** (Switch 8) to **Gold** for a tinted discharge.
5. **Set brightness**: Adjust **Bright** (Knob 3) to about 60%. This controls the overall flash rate (find a tempo that feels like rolling thunder.)
6. **Composite**: Use **Mix** (Fader 12) at about 70% to blend the storm into the source, preserving enough of the original image to anchor the composition.
7. **Compare**: Toggle **Bypass** (Switch 11) on and off to feel the difference between the raw source and the storm-overlaid result.

#### Settings

| Control | Value |
|---------|-------|
| Bolt W | ~70% |
| Branch P | ~80% |
| Bright | ~60% |
| Flash Frq | ~60% |
| Jitter | ~60% |
| Tint | 50% |
| Style | Arc |
| Color | Gold |
| Flash | On |
| Animate | Off |
| Bypass | Off |
| Mix | ~70% |

---
## Glossary

- **Additive Compositing**: A blending method where the effect's brightness is summed onto the source, always making the result brighter or equal.

- **DDS (Direct Digital Synthesis)**: A technique for generating periodic waveforms by incrementing a phase accumulator at a fixed rate; used here to time the bolt's flash cycle.

- **Distance Falloff**: A brightness curve that decreases with horizontal distance from the bolt center, creating the glowing halo effect.

- **LFSR (Linear Feedback Shift Register)**: A shift register whose input bit is a function of its previous state, producing a pseudo-random sequence used for jitter and flash randomization.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness.

- **Phase Accumulator**: A counter that wraps around at overflow, used in DDS to generate periodic events at a frequency proportional to the increment value.

- **Random Walk**: A mathematical process where each step's position is the previous position plus a random offset; used to trace the bolt's jagged path.

---
