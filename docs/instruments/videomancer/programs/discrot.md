---
draft: true
sidebar_position: 86
slug: /instruments/videomancer/discrot
title: "Discrot"
image: /img/instruments/videomancer/discrot/discrot_hero_s1.png
description: "Every technology carries the seeds of its own decay."
---

![Discrot hero image](/img/instruments/videomancer/discrot/discrot_hero_s1.png)
*Discrot simulating progressive LaserDisc oxidation with concentric ring dropouts, specular speckle noise, and chroma desaturation across a degrading video signal.*

---

## Overview

Discrot is a real-time disc rot simulator that recreates the progressive physical degradation of optical and capacitance-based video disc formats. It models the specific failure modes of LaserDisc oxidation and CED stylus wear: concentric ring dropouts that trace the disc's spiral track structure, specular speckle noise from laser read errors, chroma desaturation as the FM color carrier deteriorates ahead of the luminance signal, and random analog snow in the most damaged regions. The damage pattern can optionally rotate across the frame, mimicking the disc spinning under the laser pickup.

At low settings, Discrot adds subtle, localized corruption: a faint ring of missing pixels here, a scatter of bright speckle dots there. At high settings, entire concentric bands of the image collapse into black or noise, color bleeds away from damaged zones, and frame skipping produces the jarring temporal discontinuities of a disc that can no longer be tracked. The result is an uncanny reproduction of a format dying on screen.

:::note
Discrot is a ***processing*** program. It transforms an input video signal. Without a source connected, there is nothing to degrade.
:::

### What's In a Name?

***Disc rot*** is the colloquial term for the physical deterioration of optical disc media: most famously LaserDiscs, but also some early CDs and DVDs. The aluminum reflective layer oxidizes through pinholes in the protective lacquer, creating translucent spots the laser cannot read. The name **Discrot** compresses that phenomenon into a single word: a disc that has rotted, a signal that is rotting before your eyes.

---

## Quick Start

1. Connect a video source and set **Mix** (Fader 12) fully clockwise. Turn **Damage** (Knob 1) clockwise to about 25%. Concentric rings of black dropout appear across the image, radiating outward from the center of the frame.
2. Increase **Speckle** (Knob 2) to about 25%. Bright white dots scatter across the damaged regions (specular noise from simulated laser read errors.)
3. Set **Animate** (Switch 9) to **Rotate**. The damage pattern slowly drifts across the frame as the virtual disc spins. Adjust **Rotation** (Knob 4) to control the speed.
4. Increase **Desat** (Knob 5) clockwise. Color drains from the damaged bands first, leaving monochrome ghosts where the chroma carrier has failed.

---

## Parameters

![Videomancer front panel with Discrot loaded](/img/instruments/videomancer/discrot/discrot_control_panel.png)
*Videomancer's front panel with Discrot active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Damage

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Damage** controls the probability that any pixel inside a damage band will drop out. At 0%, fully counterclockwise, no pixels are affected: the image passes through clean. As the value increases, more pixels within each concentric ring fail the LFSR threshold test and are replaced by dropout fill. At 100%, fully clockwise, every pixel inside a damage band is corrupted.

The damage decision is per-pixel and pseudo-random: each pixel's fate is determined by comparing a 16-bit ***linear feedback shift register*** noise value against the Damage threshold. This produces an organic, varying edge to each damaged region rather than a hard geometric boundary.

:::tip
Start with Damage around 25% for a realistic, mild disc rot look. Values above 50% produce catastrophic damage more typical of a disc that has been stored improperly for decades.
:::

---

### Knob 2 — Speckle

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Speckle** controls the intensity of bright specular noise dots within damaged regions. At 0%, no speckle is added: dropouts are silent. As the value increases, more pixels in damaged areas are replaced with full-brightness white. At 100%, damaged areas become dense fields of white specular points.

Speckle only appears where the damage decision has already flagged a pixel: it layers on top of the dropout fill. This reproduces the bright "sparkle" artifacts seen on real rotted LaserDiscs, where the laser encounters pitted aluminum and returns a maximum-intensity reflection instead of meaningful data.

---

### Knob 3 — Ring Width

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Ring Width** controls the width of each concentric damage band. At 0%, damage bands are at their narrowest. At 50%, bands occupy roughly half the period of each ring. At 100%, the bands cover the full ring period, meaning every radial position is potentially damaged. The interaction between Ring Width and **Damage** (Knob 1) determines the overall visual density of corruption: narrow bands with high damage create thin arcs of severe dropout, while wide bands with low damage produce broad regions of sparse speckle.

---

### Knob 4 — Rotation

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Rotation** sets the animation speed of the damage pattern when **Animate** (Switch 9) is set to **Rotate**. At 0%, the pattern rotates very slowly. At 100%, the pattern sweeps rapidly across the frame. When Animate is set to **Static**, the Rotation knob has no visible effect.

The rotation is implemented as a 16-bit accumulator that adds the Rotation parameter value on each frame. The accumulated offset shifts the ring index computation, causing the concentric damage bands to drift across the image.

---

### Knob 5 — Desat

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Desat** controls the amount of color desaturation applied inside damaged regions. At 0%, chroma passes through unchanged even in damaged areas. As the value increases, the U and V chrominance channels are attenuated toward their neutral midpoint. At 100%, damaged areas are fully desaturated (monochrome.)

This models the real-world behavior of disc rot: the FM chroma subcarrier is more fragile than the baseband luminance signal, so color information deteriorates first. A disc in the early stages of rot often plays back with washed-out or absent color before the picture itself breaks up.

:::note
Desat affects only pixels that are inside a damage band. Undamaged regions retain full color regardless of this setting.
:::

---

### Knob 6 — Snow

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Snow** controls how much random analog static is blended into severely damaged areas. At 0%, no snow is added. As the value increases, the LFSR output is summed with the luma channel in regions where the damage level exceeds a threshold derived from this control. At 100%, heavily damaged areas fill with full-amplitude white noise.

Snow layers on top of all other damage effects. In real disc rot, the worst areas degenerate from structured dropout into pure analog noise: the player's error correction has given up entirely and the output falls back to random RF hash.

---

### Switch 7 — Rot Pattern

| Property | Value |
|----------|-------|
| Off | Rings |
| On | Streaks |
| Default | Rings |

**Rot Pattern** selects the spatial structure of the damage. With the switch set to **Rings**, damage follows concentric circular bands radiating from the center of the frame: matching how oxidation spreads from the disc edge or inner hub along the spiral track. With the switch set to **Streaks**, damage follows radial angular sectors instead, creating spoke-like patterns that shoot outward from the center.

Rings mode uses the computed radial distance modulo <b>Ring Width</b> to determine per-pixel band membership. Streaks mode uses a pseudo-angular approximation (the XOR of the absolute horizontal and vertical displacements from center) as the band index instead.

---

### Switch 8 — Drop Mode

| Property | Value |
|----------|-------|
| Off | Black |
| On | Hold |
| Default | Black |

**Drop Mode** selects the fill behavior for dropped-out pixels. With the switch set to **Black**, damaged pixels are replaced with black (Y = 0, U = 512, V = 512): a clean, hard dropout. With the switch set to **Hold**, damaged pixels are replaced with the most recent undamaged pixel values: a ***sample-and-hold*** fill that smears the last good data across the gap.

:::tip
**Hold** mode produces a more analog, "sticky" look reminiscent of a real player struggling to maintain sync. **Black** mode creates a cleaner, more digital blackout look.
:::

---

### Switch 9 — Animate

| Property | Value |
|----------|-------|
| Off | Static |
| On | Rotate |
| Default | Rotate |

**Animate** controls whether the damage pattern is stationary or rotating. With the switch set to **Static**, the concentric ring or streak pattern remains fixed on screen, frame after frame. With the switch set to **Rotate**, the pattern slowly drifts, controlled by the **Rotation** knob (Knob 4). In Rotate mode, the rotation offset accumulates smoothly across frames, creating the impression of a disc spinning beneath the laser pickup.

---

### Switch 10 — Frame Skip

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Frame Skip** enables a pseudo-random temporal glitch that freezes the output on occasional frames. With the switch set to **Off**, every frame processes live. With the switch set to **On**, a random LFSR sample is checked at each vertical sync; roughly one in four frames may toggle the freeze state, causing the output to hold the last non-skipped result. This reproduces the temporal stutter of a disc player whose tracking servo is intermittently losing lock.

---

### Switch 11 — Heavy Rot

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Heavy Rot** doubles the effective Damage threshold, dramatically increasing the density and severity of dropout. With the switch set to **Off**, the Damage knob operates at its normal range. With the switch set to **On**, the threshold is left-shifted by one bit (doubled), clamped to the 10-bit maximum of 1023. A Damage setting of 50% with Heavy Rot On behaves like 100% Damage with Heavy Rot Off.

:::warning
Heavy Rot can obliterate the image rapidly. Use it when you want to simulate catastrophic, terminal-stage disc rot: the kind where the disc is probably destined for the landfill.
:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (damaged) output. At 0%, the output is the clean input: no damage is visible. At 100%, the output is fully processed. Intermediate values blend the two, allowing subtle layering of disc rot over a clean signal.

The mix is implemented via three `interpolator_u` instances (one per YUV channel), each requiring 4 clock cycles. The dry input path is delay-matched through an 8-stage shift register so that the clean and processed signals arrive at the interpolator inputs in phase.

---

## Background

### LaserDiscs and disc rot

The LaserDisc format, introduced in 1978, recorded analog video as a frequency-modulated signal encoded in microscopic pits on an aluminum-coated plastic disc. A laser read the pattern of reflections to reconstruct the video signal. The format offered a picture quality far superior to VHS tape, but it came with a specific vulnerability: the aluminum reflective layer could oxidize if the protective lacquer coating developed pinholes. Oxygen and moisture penetrated through these defects, slowly eating away at the reflective surface.

The resulting damage: ***disc rot***: appeared as translucent or opaque spots that the laser could no longer read. Because the damage followed the disc's spiral track structure, it manifested on screen as concentric arcs or rings of corrupted video. A mildly rotted disc might show occasional sparkle or brief color dropout during playback. A severely rotted disc could produce whole seconds of unwatchable noise.

### CED VideoDisc

The ***Capacitance Electronic Disc*** (CED), marketed as SelectaVision by RCA, was a different format entirely. Rather than a laser, it used a diamond stylus that rode in grooves on the disc surface, reading capacitance variations to decode the video signal. CED discs suffered from groove wear and conductive-coating breakdown, producing damage patterns that were more radial (following the stylus path) than concentric. Discrot's **Streaks** mode recreates this radial damage pattern.

### Piecewise-linear radial distance

Computing the true distance from each pixel to the center of the frame would require a square root or CORDIC algorithm: expensive in FPGA logic. Discrot uses a ***piecewise-linear approximation*** instead: $r \approx \max(|dx|, |dy|) + \frac{\min(|dx|, |dy|)}{4}$. This octagonal approximation is within a few percent of the true Euclidean distance for most of the frame and costs only a comparator, a subtractor, and a shift: no multipliers, no lookup tables.


---

## Signal Flow

### Signal Flow Notes

Three key interactions define Discrot's behavior:

1. **Spatial damage structure**: The radial distance computation establishes each pixel's position relative to the frame center. In Rings mode, the ring index (radius plus rotation offset, modulo ring width) determines whether a pixel falls inside a damage band. In Streaks mode, a pseudo-angular value replaces the ring index. The LFSR then probabilities the damage within those bands, so not every pixel in a band drops out (just those that fail the threshold test.)

2. **Layered damage effects**: Within damaged regions, effects are applied in a specific order. First, dropout fill replaces the pixel value (black or hold-previous). Then speckle may override the fill with full white. Then snow adds LFSR noise to the luma in severely damaged pixels. Finally, desaturation scales the chroma channels toward neutral. This layering produces the same progression seen in real disc rot: color loss, then dropout, then complete noise.

3. **Temporal instability**: The rotation accumulator and frame skip features add time-domain artifacts. Rotation causes the spatial damage pattern to drift smoothly. Frame skip causes random temporal freeze-frames. Together, they simulate a disc player that is both physically degraded and mechanically unstable.

:::tip
The LFSR seed is `0xD15C`: hex for "DISC." It advances on every pixel (main process), every line start, and twice per frame (vsync), ensuring a rich, non-repeating noise texture across the entire image.
:::


---

## Exercises

These exercises progress from subtle disc degradation to catastrophic format failure, demonstrating the layered interactions of Discrot's damage model.
### Exercise 1: Gentle Decay

![Gentle Decay result](/img/instruments/videomancer/discrot/discrot_ex1_s1.png)
*Gentle Decay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A subtle, realistic disc rot effect: the kind of damage that makes you wonder if the disc is starting to go bad, or if you're just imagining things.

#### Key Concepts

- Ring-shaped dropout follows radial distance from center
- Speckle adds specular noise on top of dropout
- Desaturation models chroma carrier failure before luma loss

#### Video Source

A live camera feed or recorded footage with areas of both high and low contrast. Skin tones and saturated colors show the desaturation effect clearly.

#### Steps

1. Set **Damage** (Knob 1) to about 25%. Faint concentric rings of black dropout appear across the frame.
2. Add a small amount of **Speckle** (Knob 2), around 15%. Scattered bright dots appear within the damaged rings.
3. Widen the affected area by setting **Ring Width** (Knob 3) to about 40%.
4. Set **Animate** (Switch 9) to **Rotate** and adjust **Rotation** (Knob 4) to about 20%. The damage drifts slowly, as though a disc is spinning under the laser.
5. Increase **Desat** (Knob 5) to about 50%. Color bleeds out of the damaged bands while undamaged areas retain full saturation. This is the most visually distinctive symptom of real disc rot.

#### Settings

| Control | Value |
|---------|-------|
| Damage | 25.0% |
| Speckle | 15.0% |
| Ring Width | 40.0% |
| Rotation | 20.0% |
| Desat | 50.0% |
| Snow | 0.0% |
| Rot Pattern | Rings |
| Drop Mode | Black |
| Animate | Rotate |
| Frame Skip | Off |
| Heavy Rot | Off |
| Mix | 100.0% |

---

### Exercise 2: CED Stylus Wear

![CED Stylus Wear result](/img/instruments/videomancer/discrot/discrot_ex2_s1.png)
*CED Stylus Wear — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A simulation of CED SelectaVision playback failure: radial streaks of damaged video with analog snow and sample-and-hold fill, as though a worn diamond stylus is skipping across groove walls.

#### Key Concepts

- Streaks mode simulates radial groove damage instead of concentric oxidation
- Hold mode smears undamaged data across gaps, mimicking analog tracking errors
- Snow fills the worst damage with analog static

#### Video Source

High-contrast footage with geometric patterns or strong vertical lines. The radial streaks interact visually with vertical elements in the source.

#### Steps

1. Switch **Rot Pattern** (Switch 7) to **Streaks**. Damage now radiates outward from the center in angular sectors instead of concentric rings.
2. Set **Damage** (Knob 1) to about 40% and **Ring Width** (Knob 3) to about 50%. Broad radial spoke patterns of dropout appear.
3. Switch **Drop Mode** (Switch 8) to **Hold**. Dropout areas now smear the last good pixel across the gap instead of going black (a sticky, analog feel.)
4. Add **Snow** (Knob 6) at about 40%. The most damaged areas fill with random analog noise on top of the hold-previous fill.
5. Enable **Frame Skip** (Switch 10). Occasional frames freeze, producing a temporal stutter as the virtual stylus loses tracking.

#### Settings

| Control | Value |
|---------|-------|
| Damage | 40.0% |
| Speckle | 25.0% |
| Ring Width | 50.0% |
| Rotation | 25.0% |
| Desat | 37.5% |
| Snow | 40.0% |
| Rot Pattern | Streaks |
| Drop Mode | Hold |
| Animate | Rotate |
| Frame Skip | On |
| Heavy Rot | Off |
| Mix | 100.0% |

---

### Exercise 3: Terminal Rot

![Terminal Rot result](/img/instruments/videomancer/discrot/discrot_ex3_s1.png)
*Terminal Rot — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A catastrophic disc rot simulation: the last playback before the disc is unplayable. The image is barely recognizable through layers of dropout, noise, and color failure.

#### Key Concepts

- Heavy Rot doubles the damage threshold, modeling catastrophic degradation
- All damage layers stack: dropout + speckle + snow + desaturation
- Mix allows blending catastrophic damage with the clean source

#### Video Source

Any footage: recognizable subjects let you appreciate how much of the image is destroyed.

#### Steps

1. Enable **Heavy Rot** (Switch 11). The damage threshold doubles instantly.
2. Set **Damage** (Knob 1) to about 80%. With Heavy Rot, this produces near-total coverage (most pixels in every damage band are corrupted.)
3. Narrow the damage bands by setting **Ring Width** (Knob 3) to about 20%. This concentrates the destruction into dense, thin arcs.
4. Max out **Speckle** (Knob 2) to 70% and **Snow** (Knob 6) to about 80%. Damaged areas alternate between bright specular hits and dense analog static.
5. Set **Desat** (Knob 5) to 100%. All color is stripped from damaged regions.
6. Set **Rotation** (Knob 4) to about 80% with **Animate** on **Rotate**. The damage sweeps rapidly, creating a violent, churning destruction pattern.
7. Pull **Mix** (Fader 12) back to about 60%. The clean source ghosts through the devastation, creating an eerie double-exposure of the intact and destroyed signal.

#### Settings

| Control | Value |
|---------|-------|
| Damage | 80.0% |
| Speckle | 70.0% |
| Ring Width | 20.0% |
| Rotation | 80.0% |
| Desat | 100.0% |
| Snow | 80.0% |
| Rot Pattern | Rings |
| Drop Mode | Black |
| Animate | Rotate |
| Frame Skip | Off |
| Heavy Rot | On |
| Mix | 60.0% |

---
## Glossary

- **CED (Capacitance Electronic Disc)**: A grooved-disc video format by RCA that used a diamond stylus to read capacitance variations; prone to groove wear and conductive-coating failure.

- **Chroma Subcarrier**: The modulated signal carrying color information in analog video; more fragile than the luminance baseband and typically deteriorates first during disc rot.

- **Desaturation**: The reduction of color intensity toward monochrome, modeled here as scaling the U and V channels toward their neutral midpoint.

- **Disc Rot**: Physical degradation of optical disc media caused by oxidation of the aluminum reflective layer through pinholes in the protective lacquer.

- **Dropout**: A momentary loss of signal where pixel data is replaced with a substitute value (typically black or the last good sample).

- **Interpolator**: A hardware blending unit that crossfades between two values based on a parameter; used here for the wet/dry mix.

- **LaserDisc**: An analog optical disc format (1978–2001) that encoded video as frequency-modulated pits in an aluminum-coated disc, read by a laser.

- **LFSR (Linear Feedback Shift Register)**: A shift register whose input bit is a linear function of its previous state; produces a deterministic pseudo-random sequence.

- **Piecewise-Linear Approximation**: A method of estimating a complex function (such as Euclidean distance) using simple linear operations; avoids expensive square root computation.

- **Sample and Hold**: A signal processing technique that captures a value and holds it constant until the next valid sample arrives; used here in Hold dropout mode.

- **Snow**: Random analog noise (static) produced when a video player's error correction fails completely and outputs unfiltered RF hash.

- **Speckle**: Bright specular noise dots caused by laser read errors on pitted or oxidized disc surfaces.

---
