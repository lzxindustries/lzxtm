---
draft: true
sidebar_position: 86
slug: /instruments/videomancer/discrot
title: "Discrot"
image: /img/instruments/videomancer/discrot/discrot_hero_s1.png
description: "Every technology carries the seeds of its own decay."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import discrot_control_panel from '/img/instruments/videomancer/discrot/discrot_control_panel.png';
import discrot_source1_skull from '/img/instruments/videomancer/discrot/discrot_source1_skull.png';
import discrot_source2_car from '/img/instruments/videomancer/discrot/discrot_source2_car.png';
import discrot_source3_turtle from '/img/instruments/videomancer/discrot/discrot_source3_turtle.png';
import discrot_source4_pattern from '/img/instruments/videomancer/discrot/discrot_source4_pattern.png';
import discrot_source5_woman from '/img/instruments/videomancer/discrot/discrot_source5_woman.png';
import discrot_source6_paint from '/img/instruments/videomancer/discrot/discrot_source6_paint.png';
import discrot_hero_s1 from '/img/instruments/videomancer/discrot/discrot_hero_s1.png';
import discrot_hero_s2 from '/img/instruments/videomancer/discrot/discrot_hero_s2.png';
import discrot_hero_s3 from '/img/instruments/videomancer/discrot/discrot_hero_s3.png';
import discrot_hero_s4 from '/img/instruments/videomancer/discrot/discrot_hero_s4.png';
import discrot_hero_s5 from '/img/instruments/videomancer/discrot/discrot_hero_s5.png';
import discrot_hero_s6 from '/img/instruments/videomancer/discrot/discrot_hero_s6.png';
import discrot_ex1_s1 from '/img/instruments/videomancer/discrot/discrot_ex1_s1.png';
import discrot_ex1_s2 from '/img/instruments/videomancer/discrot/discrot_ex1_s2.png';
import discrot_ex1_s3 from '/img/instruments/videomancer/discrot/discrot_ex1_s3.png';
import discrot_ex1_s4 from '/img/instruments/videomancer/discrot/discrot_ex1_s4.png';
import discrot_ex1_s5 from '/img/instruments/videomancer/discrot/discrot_ex1_s5.png';
import discrot_ex1_s6 from '/img/instruments/videomancer/discrot/discrot_ex1_s6.png';
import discrot_ex2_s1 from '/img/instruments/videomancer/discrot/discrot_ex2_s1.png';
import discrot_ex2_s2 from '/img/instruments/videomancer/discrot/discrot_ex2_s2.png';
import discrot_ex2_s3 from '/img/instruments/videomancer/discrot/discrot_ex2_s3.png';
import discrot_ex2_s4 from '/img/instruments/videomancer/discrot/discrot_ex2_s4.png';
import discrot_ex2_s5 from '/img/instruments/videomancer/discrot/discrot_ex2_s5.png';
import discrot_ex2_s6 from '/img/instruments/videomancer/discrot/discrot_ex2_s6.png';
import discrot_ex3_s1 from '/img/instruments/videomancer/discrot/discrot_ex3_s1.png';
import discrot_ex3_s2 from '/img/instruments/videomancer/discrot/discrot_ex3_s2.png';
import discrot_ex3_s3 from '/img/instruments/videomancer/discrot/discrot_ex3_s3.png';
import discrot_ex3_s4 from '/img/instruments/videomancer/discrot/discrot_ex3_s4.png';
import discrot_ex3_s5 from '/img/instruments/videomancer/discrot/discrot_ex3_s5.png';
import discrot_ex3_s6 from '/img/instruments/videomancer/discrot/discrot_ex3_s6.png';

# Discrot

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: discrot_source1_skull, after: discrot_hero_s1 },
    { label: "Car", before: discrot_source2_car, after: discrot_hero_s2 },
    { label: "Turtle", before: discrot_source3_turtle, after: discrot_hero_s3 },
    { label: "Pattern", before: discrot_source4_pattern, after: discrot_hero_s4 },
    { label: "Woman", before: discrot_source5_woman, after: discrot_hero_s5 },
    { label: "Paint", before: discrot_source6_paint, after: discrot_hero_s6 },
  ]}
/>
*Discrot applying concentric ring dropouts and speckle noise to simulate LaserDisc oxidation damage on a live video signal.*

---

## Overview

Every technology carries the seeds of its own decay. LaserDiscs and CED videodiscs encoded analog video into physical structures — pits pressed into aluminum, grooves cut into carbon — that a beam of light or a stylus tip could read back as a moving image. When those physical structures corrode, the video degrades in ways that are unique to the medium: concentric bands of missing picture, bright speckle from misread pits, snow filling the gaps where signal used to be, and color draining away before brightness does.

Discrot recreates that decay as a real-time video effect. It computes a radial distance from screen center for every pixel — approximating the concentric groove structure of a spinning disc — and applies probabilistic damage based on ring position and an LFSR noise source. Damaged pixels either drop to black or freeze at their last good value. Specular speckle and additive snow fill the corrupted regions. Chroma desaturates independently of luma, mimicking how FM color carriers fail before brightness carriers in analog disc formats. The name is a portmanteau of *disc* (the optical or capacitance medium) and *rot* (the oxidation process that destroys it).

At low Damage settings, Discrot adds subtle ring-shaped interference that suggests a slightly worn disc. At high settings with Heavy Rot engaged, the image disintegrates into concentric bands of snow, speckle, and black — a faithful recreation of a disc that has been sitting in a humid garage for thirty years. Because there is no bypass toggle, the only way to reduce the effect to zero is the Mix fader.

---

## Quick Start

1. **Mix is your bypass**: Since there is no bypass toggle, use the Mix fader (Pot 12) for A/B comparison. Full counter-clockwise = clean signal; full clockwise = full effect.
2. **Color dies first**: Increase Desat before cranking Damage for the most realistic disc rot look — real oxidation degrades the chroma FM carrier before the luma carrier.
3. **Hold mode for subtlety**: Hold dropout (Toggle 8) produces more naturalistic artifacts than black dropout because real disc players attempted to conceal errors by repeating previous samples.

---

## Background

### LaserDisc Technology

The LaserDisc (LD), introduced by Philips and MCA in 1978, was the first commercial optical disc format for video. A 30 cm (12-inch) disc encoded analog composite video as a frequency-modulated carrier, physically represented by a spiral track of microscopic pits stamped into an aluminum reflective layer sandwiched between two acrylic substrates. A helium-neon (later semiconductor) laser read the pit pattern through the transparent substrate. Because the video signal was analog FM rather than digital, there was no error correction in the traditional sense — any physical damage to the reflective layer translated directly into visible artifacts in the reconstructed picture.

### CED Videodiscs

RCA's Capacitance Electronic Disc (CED), marketed as SelectaVision from 1981 to 1986, took a different approach. A diamond stylus rode in a physical groove pressed into a carbon-loaded PVC disc, reading capacitance variations between the stylus electrode and a conductive layer beneath the groove floor. CED discs were vulnerable to groove wear, static charge, and dust contamination. Damaged areas produced streaks and dropouts that followed the disc's radial structure — similar in appearance to disc rot but caused by mechanical wear rather than chemical oxidation.

### What Is Disc Rot?

Disc rot is the progressive degradation of the aluminum reflective layer inside a LaserDisc. Moisture penetrates through imperfections in the acrylic substrate or the bonding adhesive at the disc's edge, oxidizing the aluminum into transparent aluminum oxide. The laser, unable to read the corroded areas, produces read errors that appear as:

1. **Concentric ring dropouts** — bands of corrupted or missing video tracing circular arcs across the frame, following the spiral track structure
2. **Specular speckle** — bright white noise dots from laser scattering off partially corroded pits
3. **Color loss before luma loss** — the FM chroma subcarrier, modulated at higher frequencies, is more sensitive to pit geometry degradation than the lower-frequency luma carrier
4. **Snow fill** — in severely rotted regions, the signal degrades to full random noise

The damage typically spreads inward from the disc edge or outward from the center hub, producing characteristic ring-shaped zones of increasing degradation.

### Analog Video Artifacts vs. Digital Errors

Digital media either reads correctly or fails completely — there is no graceful degradation. Analog disc formats occupy a middle ground: the signal degrades gradually, producing a rich vocabulary of visual artifacts that depend on the specific failure mechanism. A slightly warped disc produces subtle wobble; a mildly oxidized region loses color before losing brightness; a severely corroded section dissolves into snow. Discrot models these failure modes as independent, stackable layers, each with its own control.

### Media Preservation and Aesthetic Value

The disc rot aesthetic has become a visual shorthand for technological obsolescence and analog nostalgia. Archivists document the specific damage patterns of deteriorating collections; video artists deliberately seek out rotted discs for their unique visual textures. Discrot makes these textures available as a controllable effect — no decaying disc required.


---

## Signal Flow

Position Counters → Radial Distance → Rotation Accumulator → ... → Sync Delay Pipeline → Wet/Dry Mix

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ H counter (pixel position within line)
│   ├─ V counter (line number within frame)
│   ├─ Frame counter (frame number)
│   └─ LFSR update (per-pixel, per-line, per-frame taps)
│
├── Radial Distance ────────────────────────────────────────────
│   ├─ dx = |h_count - 960|
│   ├─ dy = |v_count - 540|
│   └─ radius ≈ max(dx, dy) + min(dx, dy) / 4
│
├── Rotation Accumulator ───────────────────────────────────────
│   └─ rot_offset += rotation_speed  (per frame, if Animate on)
│
├── Ring Index + Damage Decision ───────────────────────────────
│   ├─ ring_pos = (radius + rot_offset) mod ring_width
│   ├─ threshold = damage × (2 if Heavy Rot)
│   ├─ Rings mode:  damaged = ring_pos < ring_width AND lfsr < threshold
│   └─ Streaks mode: damaged = angle_approx < ring_width AND lfsr < threshold
│
├── Damage Application ────────────────────────────────────────
│   ├─ Dropout:
│   │   ├─ Black mode  → Y=0, U=512, V=512
│   │   └─ Hold mode   → Y=held_y, U=held_u, V=held_v
│   ├─ Speckle: if lfsr < speckle → Y=1023, U=512, V=512
│   ├─ Snow: if damage_level > snow/2 → Y += lfsr noise
│   └─ Desaturation: U,V → (val-512)*(1023-desat)/1024+512
│
├── Hold-Previous Update ───────────────────────────────────────
│   └─ When not damaged: held_y/u/v ← current input
│
├── Frame Skip ─────────────────────────────────────────────────
│   └─ Random freeze: if skip_active → use frozen_y/u/v
│
├── Sync Delay Pipeline (8 clocks) ─────────────────────────────
│   └─ hsync_n, vsync_n, field_n, Y, U, V delayed
│
└── Wet/Dry Mix (3× interpolator_u, 4 clocks) ─────────────────
    └─ output = lerp(delayed_dry, processed_wet, mix_amount)
```

The processing chain applies damage effects only to pixels that fall within the current damage zone — a probabilistic combination of radial position and LFSR noise. Outside the damage zone, pixels pass through unchanged (and update the hold-previous registers). The radial distance computation uses a piecewise-linear approximation that avoids square roots: $r \approx \max(|dx|, |dy|) + \frac{\min(|dx|, |dy|)}{4}$, which produces slightly squarish rings rather than perfect circles — an acceptable approximation that adds character. The rotation accumulator shifts the ring pattern each frame, simulating the disc spinning beneath the laser pickup. Because there is no bypass toggle, the Mix fader at position 12 is the only way to crossfade between dry and wet signals.

---

## Parameter Reference

<img src={discrot_control_panel} alt="Videomancer front panel with Discrot loaded"/>
*Videomancer's front panel with Discrot active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Damage
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

At zero, no damage occurs regardless of ring position. As Damage increases, the LFSR comparison threshold rises and more pixels within each ring band fail the noise check, producing denser dropout patterns. With Heavy Rot enabled (Toggle 11), the effective threshold is doubled, making even moderate Damage settings produce severe corruption. This is the primary intensity control for the entire effect. Internally, controls the probability that any pixel within a damage ring is actually corrupted.

---

#### Knob 2 — Speckle
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the density of bright specular speckle noise within damaged regions. Speckle simulates laser scattering off partially corroded pits — the dots are always maximum white (Y=1023) with neutral chroma, cutting through even heavily desaturated or snow-filled areas. At low values, only occasional bright dots appear; at high values, damaged regions fill with dense white speckling that can overpower the dropout and snow effects.

---

#### Knob 3 — Ring Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the width of the concentric damage rings (or radial streaks in Streaks mode). Narrow rings create fine, closely-spaced bands of damage separated by clean video — resembling early-stage disc rot where oxidation follows individual track grooves. Wide rings create broad swaths of corrupted image, more like late-stage damage where entire regions of the reflective layer have failed. The ring width also determines the modular arithmetic period for the ring position calculation.

---

#### Knob 4 — Rotation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the speed of the rotation animation when Animate is enabled (Toggle 9). The rotation accumulator adds this value to a 16-bit offset each frame, shifting the ring pattern across the image. Low values produce a slow, subtle drift; high values spin the damage pattern rapidly. At zero, the pattern is static even when Animate is on. This simulates the disc spinning beneath the laser pickup — faster rotation means more of the disc surface sweeps past the read head per frame.

---

#### Knob 5 — Desat
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls chroma desaturation within damaged regions. Damaged pixels have their U and V channels pulled toward neutral (512) by an amount proportional to this control. This models how the FM chroma subcarrier, modulated at higher frequencies than luma, is more vulnerable to pit geometry degradation. At moderate settings, damaged areas appear washed out — color drains away while brightness (or its absence) remains. At maximum, damaged regions are fully monochrome. Undamaged pixels are not affected.

---

#### Knob 6 — Snow
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the intensity of additive snow noise in severely damaged areas. Snow is mixed into the luma channel only when the per-pixel damage level exceeds half the Snow threshold, creating a graduated effect where lightly damaged pixels show dropout or speckle while heavily damaged pixels dissolve into static. The snow noise comes from the LFSR, producing the characteristic analog noise grain of a completely lost signal. Higher values lower the damage threshold at which snow appears, spreading the static effect into less damaged regions.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Rot Pattern** | Rings | Streaks |
| **8 — Drop Mode** | Black | Hold |
| **9 — Animate** | Static | Rotate |
| **10 — Frame Skip** | Off | On |
| **11 — Heavy Rot** | Off | On |

Toggles 7–11 select between paired damage modes and enable secondary effects. There is no bypass toggle — the only way to reduce the effect to zero is the Mix fader (Pot 12). Toggle 7 selects between concentric rings and radial streaks. Toggle 8 selects the dropout behavior (black vs. hold-previous). Toggle 9 enables or disables rotation animation. Toggle 10 enables random frame-skip freezing. Toggle 11 doubles the damage threshold for catastrophic disc rot simulation.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input signal and the processed (damaged) output. At 100% (fully clockwise, default), the full disc rot effect is applied. At 0%, the original signal passes through untouched. Because Discrot has no bypass toggle, the Mix fader is the only way to reduce the effect to zero. Intermediate positions blend the damaged and clean signals, which can produce a translucent overlay effect where damage regions appear as semi-transparent disturbance over the original image.





---

## Guided Exercises

These exercises progress from mild disc wear to catastrophic media failure, exploring how the damage modes and secondary effects interact.

### Exercise 1: Gentle Disc Wear

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: discrot_source1_skull, after: discrot_ex1_s1 },
    { label: "Car", before: discrot_source2_car, after: discrot_ex1_s2 },
    { label: "Turtle", before: discrot_source3_turtle, after: discrot_ex1_s3 },
    { label: "Pattern", before: discrot_source4_pattern, after: discrot_ex1_s4 },
    { label: "Woman", before: discrot_source5_woman, after: discrot_ex1_s5 },
    { label: "Paint", before: discrot_source6_paint, after: discrot_ex1_s6 },
  ]}
/>
*Gentle Disc Wear — simulated result across source images.*
**Source**: Footage with smooth tonal gradients — sky, water, or skin tones work well.

**What You'll Create**: Learn how ring width, damage density, and desaturation interact to produce subtle disc rot artifacts.

1. **First damage**: Set Damage to about 25%. Faint concentric rings of black dropout appear over the image.
2. **Ring width**: Sweep Ring Width from narrow to wide. Narrow settings produce many thin bands; wide settings produce fewer, broader damaged zones.
3. **Color loss**: Increase Desat to about 50%. Damaged regions lose color while retaining their dropout pattern — the classic early-stage disc rot look.
4. **Rotation**: Enable Animate (Toggle 9) and set Rotation to about 20%. The ring pattern slowly drifts, simulating a spinning disc.
5. **Hold mode**: Switch Drop Mode to Hold (Toggle 8). Damaged pixels now smear horizontally instead of going black — a subtler, more realistic artifact.

**Key concepts**: Ring width controls damage band spacing, desaturation mimics chroma carrier failure, hold mode simulates dropout concealment, rotation animates the disc spin

---

### Exercise 2: Specular Speckle and Snow

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: discrot_source1_skull, after: discrot_ex2_s1 },
    { label: "Car", before: discrot_source2_car, after: discrot_ex2_s2 },
    { label: "Turtle", before: discrot_source3_turtle, after: discrot_ex2_s3 },
    { label: "Pattern", before: discrot_source4_pattern, after: discrot_ex2_s4 },
    { label: "Woman", before: discrot_source5_woman, after: discrot_ex2_s5 },
    { label: "Paint", before: discrot_source6_paint, after: discrot_ex2_s6 },
  ]}
/>
*Specular Speckle and Snow — simulated result across source images.*
**Source**: High-contrast footage — black and white graphics, text, or high-contrast live video.

**What You'll Create**: Explore the speckle and snow effects that fill damaged regions with noise artifacts.

1. **Base damage**: Set Damage to about 40% with moderate Ring Width (about 50%).
2. **Speckle injection**: Slowly increase Speckle. Bright white dots begin appearing within the damaged rings — laser read errors scattering off corroded pits.
3. **Snow fill**: Increase Snow to about 50%. Heavily damaged areas now fill with additive LFSR noise, blending with the speckle.
4. **Heavy Rot**: Enable Heavy Rot (Toggle 11). The damage density doubles — nearly the entire image is now affected.
5. **Radial streaks**: Switch Rot Pattern to Streaks (Toggle 7). The damage pattern changes from concentric rings to radial spokes, creating a different failure aesthetic.
6. **Mix blend**: Pull Mix down to about 60% to partially reveal the clean image beneath the damage.

**Key concepts**: Speckle produces bright white dots from laser scatter simulation, snow fills severely damaged areas with static noise, Heavy Rot doubles the effective damage threshold, Mix fader is the only bypass mechanism

---

### Exercise 3: Catastrophic Media Failure

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: discrot_source1_skull, after: discrot_ex3_s1 },
    { label: "Car", before: discrot_source2_car, after: discrot_ex3_s2 },
    { label: "Turtle", before: discrot_source3_turtle, after: discrot_ex3_s3 },
    { label: "Pattern", before: discrot_source4_pattern, after: discrot_ex3_s4 },
    { label: "Woman", before: discrot_source5_woman, after: discrot_ex3_s5 },
    { label: "Paint", before: discrot_source6_paint, after: discrot_ex3_s6 },
  ]}
/>
*Catastrophic Media Failure — simulated result across source images.*
**Source**: Any footage — the source will be largely destroyed.

**What You'll Create**: Combine all effects at extreme settings to simulate unrecoverable disc rot.

1. **Maximum damage**: Set Damage to about 80% with Heavy Rot enabled.
2. **All noise**: Speckle to about 70%, Snow to about 80%.
3. **Full desaturation**: Desat to 100%. All damaged areas are monochrome.
4. **Frame skip**: Enable Frame Skip (Toggle 10). Random frame freezes add stuttering to the corruption.
5. **Fast rotation**: Set Rotation to about 80% with Animate on. The damage pattern spins rapidly.
6. **Narrow rings**: Set Ring Width to about 20% for dense, closely-spaced damage bands.
7. **Observe**: The image is barely recognizable — fragments of the source peek through between damage bands, surrounded by snow, speckle, and frozen frames.

**Key concepts**: Heavy Rot plus high Damage creates near-total corruption, frame skip simulates tracking servo failure, narrow ring width with fast rotation creates strobing interference, desaturation models chroma carrier destruction

---


## Tips

- **Ring Width shapes the character**: Narrow rings = many fine bands (early-stage rot along individual grooves). Wide rings = broad damaged zones (late-stage delamination).
- **Heavy Rot is exponential**: Because Heavy Rot doubles the threshold, combining it with even moderate Damage settings produces catastrophic corruption. Use it as a late-stage intensifier, not a starting point.
- **Rotation completes the illusion**: Enable Animate with low Rotation speed for the most convincing physical disc simulation — the damage pattern should drift, not spin.
- **Frame Skip adds temporal damage**: Real disc rot causes tracking servo instability. Frame Skip simulates this with random freezes that complement the spatial damage.
- **Snow builds on damage**: Snow only appears in pixels with high damage levels, so it naturally concentrates in the most corrupted areas. It cannot be seen without sufficient Damage.

---

## Glossary

| Term | Definition |
|------|------------|
| **CED** | Capacitance Electronic Disc; RCA's grooved capacitance-based videodisc format (1981–1986). |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Desaturation** | Reducing the intensity of color toward neutral gray by pulling U and V values toward 512. |
| **Disc Rot** | Progressive oxidation of the aluminum reflective layer in LaserDiscs, causing read errors and visible video artifacts. |
| **Dropout** | A region of missing or corrupted video caused by physical damage to the storage medium. |
| **FM Carrier** | Frequency-modulated radio signal used to encode analog video on optical disc formats. |
| **Hold-Previous** | Dropout concealment technique where the last good sample is repeated through the damaged region. |
| **LaserDisc** | Optical disc format (1978–2001) encoding analog video as frequency-modulated pit patterns read by laser. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used for noise generation in FPGA designs. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Snow** | Random noise pattern resembling television static, characteristic of a completely lost analog signal. |
| **Speckle** | Bright noise dots caused by laser scattering off partially corroded or irregularly shaped pits. |

---
