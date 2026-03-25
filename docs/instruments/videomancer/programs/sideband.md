---
draft: true
sidebar_position: 266
slug: /instruments/videomancer/sideband
title: "Sideband"
image: /img/instruments/videomancer/sideband/sideband_hero_s1.png
description: "Before cable and digital broadcasting, television reception was an analog adventure."
---

![Sideband hero image](/img/instruments/videomancer/sideband/sideband_hero_s1.png)
*Sideband degrading a clean video signal into the ghosted, snowy, interference-laced texture of 1970s off-air television reception.*

---

## Overview

Sideband is an analog broadcast reception artifact simulator. It recreates the specific imperfections of watching television through an imperfect antenna system: the kind of picture quality that was simply a fact of life before cable and digital broadcasting. Ghost images, herringbone interference bars, rolling hum bands, and snow noise are layered together to transform clean video into something that looks like it traveled through miles of atmosphere, bounced off a few buildings, and arrived at a set of rabbit-ear antennas on top of a portable television.

Each artifact is independently controllable. You can dial in a subtle single ghost for a wistful, nostalgic haze, or stack all four degradation layers at once to bury your signal in a blizzard of analog chaos. The six knobs and five toggles give you fine control over each phenomenon, and the final Mix fader lets you blend the degraded signal with the clean original at any ratio.

:::tip
Sideband is a ***processing*** program. It transforms an incoming video signal rather than generating imagery from scratch. Feed it a camera, a pattern generator, or the output of another Videomancer program.
:::

### What's In a Name?

In radio engineering, a ***sideband*** is a band of frequencies adjacent to the main carrier that contains the actual signal information. Analog television transmits video as amplitude-modulated sidebands flanking a carrier frequency. When reception is poor: when the antenna is misaligned, when buildings create reflections, when a neighboring station's carrier bleeds through: it's the sidebands that suffer. The name captures the essence of the program: it simulates what happens when sidebands are corrupted on the journey from transmitter to screen.

---

## Quick Start

1. Turn **Ghost Gain** (Knob 2) to about 50%. A faint, displaced copy of the image appears, offset to the right. Adjust **Ghost Delay** (Knob 1) to slide the ghost closer to or farther from the original.
2. Increase **Interference** (Knob 3). Fine diagonal bars appear across the luminance channel: the telltale herringbone pattern of adjacent-channel interference.
3. Add **Hum Level** (Knob 4). Soft horizontal brightness bands roll slowly up or down the screen. Adjust **Hum Roll** (Knob 6) to change how fast the bands drift.
4. Lower **Signal Str** (Knob 5) from its default maximum. Snow noise creeps into the picture, replacing signal with static. The lower the signal strength, the more noise dominates.

---

## Parameters

![Videomancer front panel with Sideband loaded](/img/instruments/videomancer/sideband/sideband_control_panel.png)
*Videomancer's front panel with Sideband active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Ghost Delay

| Property | Value |
|----------|-------|
| Range | 0px – 256px |
| Default | 32px |

**Ghost Delay** sets the horizontal displacement of the ghost image, measured in pixels. At 0 px, the ghost sits directly on top of the original and is invisible (the two copies overlap perfectly). As the value increases, the ghost slides further to the right, creating a wider gap between the original image and its echo. At the maximum of 256 px, the ghost is displaced by a quarter of the visible line width.

In real-world analog reception, ghost delay depends on the path-length difference between the direct signal and its reflection off a building or hillside. Short delays produce a subtle thickening of edges; long delays create an obvious double image.

---

### Knob 2 — Ghost Gain

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Ghost Gain** controls the brightness of the ghost image relative to the original. At 0.0%, the ghost is invisible: no echo is mixed in. Increasing the value makes the ghost progressively brighter and more visible. At 100.0%, the ghost is at full strength, as bright as the direct signal itself.

:::note
When **Dual Ghost** (Switch 8) is set to **Dual**, a second ghost appears at double the delay and half the gain of the first. This second reflection is automatically derived from the Ghost Delay and Ghost Gain settings (no separate controls are needed.)
:::

---

### Knob 3 — Interference

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Interference** controls the amplitude of the ***herringbone*** interference pattern overlaid on the luminance channel. At 0.0%, no interference is present. As the value increases, fine bars appear across the image: bright and dark stripes that alternate in a rapid pattern. Higher values also increase the spatial frequency of the pattern, making the bars finer and more numerous. At 100.0%, the interference dominates the luminance channel with aggressive banding.

Herringbone interference is generated by a ***direct digital synthesis*** (DDS) phase accumulator producing a square-ish waveform. The Interference knob simultaneously controls both the amplitude and the frequency of the pattern.

---

### Knob 4 — Hum Level

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Hum Level** controls the strength of ***mains hum*** bars: the slowly rolling horizontal brightness bands caused by power-line interference coupling into the signal path. At 0.0%, no hum bars are visible. As the value increases, broad bands of brighter and darker luminance appear, spanning the full width of the screen. At 100.0%, the hum modulation is at full depth.

The hum bars are generated by a triangle wave whose vertical phase is derived from the scanline counter. Roughly five bars appear per frame, replicating the look of 50 Hz mains pickup in a PAL-region signal chain.

:::tip
Hum bars affect all three channels (Y, U, V) equally. They modulate overall brightness, not color, which matches the behavior of real power-line hum in an analog receiver's IF amplifier.
:::

---

### Knob 5 — Signal Str

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Signal Str** (Signal Strength) sets the overall quality of the received signal. At 100.0% (fully clockwise, the default), the signal is clean and noise-free. As the value decreases, ***snow noise***: the familiar analog TV static: progressively replaces the video signal. The crossfade is a linear interpolation: `output = video × strength + noise × (1 − strength)`. At 0.0% (fully counterclockwise), the picture is entirely replaced by noise.

Signal Strength is the "dramatic" control. Everything else adds minor artifacts to a recognizable image; this one can dissolve the picture into nothing.

---

### Knob 6 — Hum Roll

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Hum Roll** controls the vertical scrolling speed of the hum bars. At 0.0%, the bars are stationary: locked in place on the screen. As the value increases, the bars drift upward (or downward, depending on the phase relationship) at an increasing rate. At 100.0%, the bars roll rapidly. The roll speed is accumulated frame by frame, so the bars move smoothly rather than jumping.

:::note
If **Hum Level** (Knob 4) is set to 0.0%, adjusting Hum Roll has no visible effect, because there are no bars to scroll.
:::

---

### Switch 7 — Ghost Pol

| Property | Value |
|----------|-------|
| Off | Pos |
| On | Neg |
| Default | Pos |

**Ghost Pol** (Ghost Polarity) switches the ghost echo between positive and negative polarity. With the switch set to **Pos**, the ghost is additive: it brightens the image where it overlaps. With the switch set to **Neg**, the ghost is subtractive: it darkens the image where it overlaps, creating a dark echo.

In real-world reception, the polarity of a ghost depends on the number of reflections in the signal path. An odd number of reflections inverts the signal, producing a negative ghost. Even reflections (or direct-path reflections from a flat surface) produce positive ghosts. Negative ghosts are often more visually distinctive because they create dark outlines around bright objects.

---

### Switch 8 — Dual Ghost

| Property | Value |
|----------|-------|
| Off | Single |
| On | Dual |
| Default | Single |

**Dual Ghost** adds a second ghost image when set to **Dual**. The second ghost is automatically placed at double the delay and half the gain of the first, simulating a weaker secondary reflection that has traveled a longer path. When set to **Single**, only the primary ghost is active.

The polarity of the second ghost matches the first (both are controlled by **Ghost Pol**). In a real antenna system, multiple reflections at different delays are the norm rather than the exception (a single, clean ghost is actually the unusual case.)

---

### Switch 9 — Color Loss

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color Loss** simulates the way chrominance information is lost before luminance as signal strength degrades. When set to **On**, the noise level applied to the U and V chroma channels is doubled relative to the Y luminance channel (clamped to the maximum). This means color disappears into static before brightness does: exactly what happens in real analog reception, because the color subcarrier is more fragile than the baseband luminance signal.

When set to **Off**, all three channels receive the same noise level from the **Signal Str** control.

:::tip
***Color Loss is historically accurate.*** On a real television, a weak signal first turns to black-and-white static before the picture itself disappears. Sideband replicates this behavior.
:::

---

### Switch 10 — Interf Tilt

| Property | Value |
|----------|-------|
| Off | Horiz |
| On | Diag |
| Default | Diag |

**Interf Tilt** (Interference Tilt) switches the herringbone interference pattern between horizontal and diagonal orientations. When set to **Horiz**, the interference bars run straight across the screen. When set to **Diag**, the bars tilt diagonally: each new scanline introduces a fixed phase offset, creating the characteristic slanted pattern of adjacent-channel interference.

The diagonal mode is the more realistic of the two. In real reception, the beat frequency between the desired carrier and an interfering carrier drifts in phase from line to line, creating a slowly rotating diagonal pattern.

---

### Switch 11 — Noise Type

| Property | Value |
|----------|-------|
| Off | Fine |
| On | Coarse |
| Default | Fine |

**Noise Type** selects between fine and coarse snow noise textures. When set to **Fine**, the LFSR noise updates every pixel, producing the characteristic fine-grained static of a detuned television. When set to **Coarse**, the noise uses a sample-and-hold that updates every eight pixels, producing a chunkier, blockier static pattern.

Fine noise is more realistic for standard analog snow. Coarse noise has a grittier, more stylized look that can be useful for artistic effect or for simulating the appearance of a very low-bandwidth signal path.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) and wet (fully processed) signal. At 0.0%, the output is the original input with no artifacts. At 100.0% (the default), the output is the fully degraded signal. Intermediate values blend the two, which is useful for dialing in subtle amounts of analog texture without committing to full degradation.

The Mix control uses a hardware interpolator for smooth, artifact-free blending across all three YUV channels simultaneously.

---

## Background

### Analog broadcast television

Before cable and satellite delivery became universal, most television viewers received their signal through an antenna. The broadcast signal: a radio-frequency carrier modulated with video information in its ***sidebands***: traveled from a transmitter tower to a receiving antenna through open air. Every obstacle between transmitter and receiver introduced degradation.

The artifacts Sideband recreates are specific to this ***over-the-air*** (OTA) reception path. They are distinct from the encoding artifacts of a particular color system (NTSC, PAL, SECAM) and distinct from camera or recording artifacts. These are the artifacts of ***propagation*** and ***reception***.

### Multipath and ghosts

When a broadcast signal bounces off a building, hillside, or aircraft, the reflected copy arrives at the antenna slightly later than the direct signal. Because the reflected path is longer, the delay manifests as a horizontal displacement on screen: the ghost image is shifted to the right by an amount proportional to the extra path length. The brightness of the ghost depends on the reflectivity of the surface and the signal loss along the extra path.

In cities, multiple reflections were common. A viewer might see two, three, or even four ghost images stacked to the right of the original, each progressively fainter and more delayed. Sideband's **Dual Ghost** mode recreates this layered effect with a primary and secondary reflection.

### Herringbone interference

When two broadcast stations operate on adjacent channels, the carrier frequency of the unwanted station creates a ***beat frequency*** with the desired signal. This beat manifests as a fine pattern of alternating bright and dark bars across the screen: the herringbone pattern. The bars typically tilt diagonally because the beat frequency drifts slightly in phase from one scanline to the next.

Sideband implements this with a DDS phase accumulator that generates a square-ish waveform at a frequency controlled by the **Interference** knob. The diagonal tilt is created by adding a fixed phase offset at each horizontal sync pulse.

### Mains hum bars

Power-line hum at 50 Hz (in PAL regions) or 60 Hz (in NTSC regions) was a persistent nuisance in analog television. When mains frequency couples into the signal chain: through a ground loop, a poorly shielded cable, or a failing power supply capacitor: it creates a slow brightness modulation at the mains frequency. Because the mains frequency is close to but not exactly equal to the field rate, the resulting bars drift slowly up or down the screen.

Sideband generates hum bars using a triangle wave whose vertical period creates roughly five bars per frame. The **Hum Roll** control advances the phase of this wave frame by frame, simulating the characteristic slow drift.

### Snow noise

When signal strength drops, the receiver's automatic gain control amplifies everything: including thermal noise from the antenna and the receiver's own front-end circuits. This noise appears on screen as the familiar analog ***snow***: random bright and dark pixels that increasingly obscure the picture.

Sideband models this with two LFSR-based pseudo-random noise generators. One drives the luminance noise; the other drives the chroma noise. The **Signal Str** control crossfades linearly between the clean video and the noise floor. With **Color Loss** enabled, the chroma channels are driven to noise faster than the luminance channel, replicating the real-world behavior where color disappears before the picture does.


---

## Signal Flow

### Signal Flow Notes

Two critical interactions define Sideband's behavior:

1. **Herringbone and hum are luminance-only.** The interference pattern and hum bars are added exclusively to the Y channel. The U and V chroma channels pass through these stages unmodified. This matches real analog behavior: herringbone is a baseband luminance artifact, and mains hum modulates the overall brightness of the picture.

2. **Snow noise affects all channels, with optional chroma acceleration.** The noise mix stage operates on all three channels, but when **Color Loss** is enabled, the chroma channels receive double the noise level. This creates the characteristic progression of signal degradation: color fades to gray first, then the luminance picture dissolves into snow.

:::tip
**Ghost images include chroma.** Unlike herringbone and hum (which are Y-only), the ghost delay operates on all three YUV channels. The ghost carries a full-color copy of the displaced image, which is correct: multipath reflections duplicate the entire signal, not just the luminance component.
:::


---

## Exercises

These exercises progress from isolated artifacts to a fully layered analog reception simulation. Each one adds a new type of degradation to the signal chain.
### Exercise 1: Ghost Image Control

![Ghost Image Control result](/img/instruments/videomancer/sideband/sideband_ex1_s1.png)
*Ghost Image Control — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A convincing multipath ghost effect ranging from subtle edge doubling to an obvious hall-of-mirrors displacement.

#### Key Concepts

- Multipath ghosts are horizontally displaced copies of the image
- Ghost delay controls the displacement; ghost gain controls the echo brightness
- Polarity and dual-ghost mode add realism

#### Video Source

A high-contrast still image or title card with sharp edges and readable text (these make ghost displacement easy to see.)

#### Steps

1. Set **Ghost Gain** (Knob 2) to about 40%. A faint copy of the image appears, offset to the right.
2. Sweep **Ghost Delay** (Knob 1) slowly from 0 to 256 px. Watch the ghost slide away from the original.
3. Increase **Ghost Gain** to 80%. The ghost is now nearly as bright as the original (a strong multipath reflection.)
4. Toggle **Ghost Pol** (Switch 7) to **Neg**. The ghost becomes a dark shadow instead of a bright echo. Toggle back and forth to compare.
5. Set **Dual Ghost** (Switch 8) to **Dual**. A second, fainter ghost appears at double the delay. This is the "city reception" look (multiple reflections from different buildings.)

#### Settings

| Control | Value |
|---------|-------|
| Ghost Delay | ~128 px |
| Ghost Gain | 40.0% |
| Interference | 0.0% |
| Hum Level | 0.0% |
| Signal Str | 100.0% |
| Hum Roll | 0.0% |
| Ghost Pol | Neg |
| Dual Ghost | Dual |
| Color Loss | Off |
| Interf Tilt | Diag |
| Noise Type | Fine |
| Mix | 100.0% |

---

### Exercise 2: Interference and Hum

![Interference and Hum result](/img/instruments/videomancer/sideband/sideband_ex2_s1.png)
*Interference and Hum — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A layered interference and hum bar effect that transforms clean video into the look of a poorly tuned broadcast receiver.

#### Key Concepts

- Herringbone interference is a luminance-only artifact with controllable tilt
- Hum bars are broad brightness bands that roll vertically
- Layering both creates a convincing "bad reception" baseline

#### Video Source

Footage with a mix of flat areas and detail: a talking-head interview or a still life works well, because the flat areas make hum bars visible while the detailed areas show herringbone texture.

#### Steps

1. With Ghost Gain at 0.0% (ghosts off), increase **Interference** (Knob 3) to about 40%. Fine bars appear across the image.
2. Toggle **Interf Tilt** (Switch 10) between **Horiz** and **Diag**. Diagonal is the more realistic orientation for adjacent-channel interference.
3. Add **Hum Level** (Knob 4) at about 40%. Broad brightness bands appear, rolling slowly.
4. Adjust **Hum Roll** (Knob 6). At 0.0%, the bars are frozen. Increase the value and they begin to drift. Find a slow, gentle roll speed that looks natural.
5. Now add a mild ghost: set **Ghost Gain** to about 25% and **Ghost Delay** to about 64 px. The three artifacts: ghost, herringbone, and hum: combine into a convincing "bad reception" look.

#### Settings

| Control | Value |
|---------|-------|
| Ghost Delay | ~64 px |
| Ghost Gain | 25.0% |
| Interference | 40.0% |
| Hum Level | 40.0% |
| Signal Str | 100.0% |
| Hum Roll | 50.0% |
| Ghost Pol | Pos |
| Dual Ghost | Single |
| Color Loss | Off |
| Interf Tilt | Diag |
| Noise Type | Fine |
| Mix | 100.0% |

---

### Exercise 3: Weak Signal Simulation

![Weak Signal Simulation result](/img/instruments/videomancer/sideband/sideband_ex3_s1.png)
*Weak Signal Simulation — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A full analog reception degradation, progressing from a slightly noisy picture to near-total signal loss.

#### Key Concepts

- Signal Strength crossfades between video and noise
- Color Loss makes chroma degrade faster than luminance
- Combining all four artifact layers creates a complete reception simulation

#### Video Source

Any footage with recognizable content: faces, text, or familiar objects help the viewer appreciate the degradation as signal strength drops.

#### Steps

1. Start with the Exercise 2 settings (mild ghost, interference, and hum). The picture should look like mediocre but watchable reception.
2. Slowly lower **Signal Str** (Knob 5) from 100% toward 50%. Snow noise creeps into the picture, softening detail and adding grain.
3. Enable **Color Loss** (Switch 9). The chroma channels dissolve into static faster than luminance: the picture fades to a noisy black-and-white image before the luminance itself is lost.
4. Toggle **Noise Type** (Switch 11) to **Coarse**. The snow becomes blockier and chunkier. Compare with **Fine** to decide which texture you prefer.
5. Continue lowering **Signal Str** toward 10%. The picture is barely visible through the static. This is the "distant transmitter in a thunderstorm" look.
6. Use **Mix** (Fader 12) to blend the degraded signal with the clean original. A Mix value around 60–70% preserves the artifacts while keeping the image readable.

#### Settings

| Control | Value |
|---------|-------|
| Ghost Delay | ~64 px |
| Ghost Gain | 30.0% |
| Interference | 20.0% |
| Hum Level | 20.0% |
| Signal Str | 40.0% |
| Hum Roll | 50.0% |
| Ghost Pol | Pos |
| Dual Ghost | Dual |
| Color Loss | On |
| Interf Tilt | Diag |
| Noise Type | Coarse |
| Mix | 100.0% |

---
## Glossary

- **Beat Frequency**: The difference frequency produced when two signals of slightly different frequencies combine; responsible for herringbone interference patterns.

- **DDS (Direct Digital Synthesis)**: A technique for generating waveforms using a phase accumulator and lookup table, used here to create the herringbone interference pattern.

- **Ghost Image**: A displaced, attenuated copy of the picture caused by a reflected signal arriving at the antenna after the direct signal.

- **Herringbone**: A fine diagonal or horizontal bar pattern caused by interference from an adjacent broadcast channel's carrier frequency.

- **LFSR (Linear Feedback Shift Register)**: A digital circuit that generates pseudo-random bit sequences, used to produce snow noise.

- **Mains Hum**: A low-frequency brightness modulation caused by power-line frequency (50 or 60 Hz) coupling into the signal chain.

- **Multipath**: The phenomenon where a broadcast signal reaches the antenna via multiple paths (direct + reflected), causing ghost images.

- **Sideband**: A band of frequencies adjacent to a carrier that contains the modulated signal information in analog broadcasting.

- **Signal-to-Noise Ratio (SNR)**: The ratio of desired signal power to noise power; lower SNR produces more visible snow.

- **Snow**: Random bright and dark pixels caused by thermal noise in the receiver when signal strength is low.

---
