---
draft: true
sidebar_position: 287
slug: /instruments/videomancer/xero
title: "Xero"
image: /img/instruments/videomancer/xero/xero_hero.png
description: "Before digital networking, the photocopier was the medium of underground publishing."
---

import xero_before_after from '/img/instruments/videomancer/xero/xero_before_after.png';
import xero_control_panel from '/img/instruments/videomancer/xero/xero_control_panel.png';
import xero_exercise1_result from '/img/instruments/videomancer/xero/xero_exercise1_result.png';
import xero_exercise2_result from '/img/instruments/videomancer/xero/xero_exercise2_result.png';
import xero_exercise3_result from '/img/instruments/videomancer/xero/xero_exercise3_result.png';
import xero_hero from '/img/instruments/videomancer/xero/xero_hero.png';
import xero_source1_kodim02 from '/img/instruments/videomancer/xero/xero_source1_kodim02.png';
import xero_source2_kodim07 from '/img/instruments/videomancer/xero/xero_source2_kodim07.png';
import xero_source3_kodim01_bw from '/img/instruments/videomancer/xero/xero_source3_kodim01_bw.png';

# Xero

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={xero_hero} alt="Xero hero image"/>
*Xero applying multi-generational copy degradation with blue toner and warm recycled paper, transforming video into a faded office photocopy.*
<img src={xero_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Xero applied.*

---

## Overview

Before digital networking, the photocopier was the medium of underground publishing. Zines, protest flyers, fan art, and anonymous manifestos all passed through xerographic machines that left their own distinctive mark on every copy — edge-enhanced contours, grainy toner spatter, periodic density bands from uneven drum rotation, and wandering vertical streaks from fuser roller defects. Xero recreates this entire artifact vocabulary as a real-time video effect.

The program implements a six-stage processing chain that models the physics of electrostatic copying. Edge enhancement simulates the charge differential at sharp boundaries on the photoconductor drum. Generation loss applies an S-curve contrast function that mimics the tonal compression that occurs when a copy is copied — each generation losing shadow detail and blowing out highlights. Toner grain adds density-dependent noise that mirrors the random distribution of toner particles. Drum banding introduces periodic horizontal density variation from drum eccentricity. Fuser streaking creates a wandering vertical bright line where the fuser roller has a defect.

The name is a play on "Xerox" — the company whose machines defined the xerographic process — with the "x" reduced to its phonetic essence, also evoking "zero" to suggest the generational degradation toward nothing.

---

## Background

### Xerographic Edge Enhancement

In electrostatic photocopying, the photoconductor drum is charged uniformly, then selectively discharged by reflected light from the document. At sharp brightness transitions, lateral charge diffusion creates an overshoot — a narrow bright fringe on the dark side of an edge and a dark fringe on the bright side. This is the xerographic equivalent of photographic unsharp masking. Xero models this as a horizontal Laplacian: enhanced = Y[x-1] + (2·Y[x-1] − Y[x-2] − Y[x]) × edge_enhance.

### Generation Loss

Copying a copy of a copy — a process familiar to anyone who grew up with office machines — progressively destroys tonal nuance. Each pass through the xerographic process clips shadows and highlights while steepening the midtone contrast. After several generations, a photograph becomes a stark, high-contrast graphic. Xero simulates this by applying a contrast S-curve whose steepness increases with the Generations parameter: result = 512 + (input − 512) × gain / 1024, where gain scales from 1024 to 3072 in Copy Art mode.

### Toner Grain and Drum Banding

Real toner is not a continuous ink — it consists of microscopic polymer particles that fuse to paper under heat. The random distribution of these particles creates a characteristic graininess, most visible in midtones where coverage is neither full nor empty. Drum banding is a separate mechanical artifact: eccentricity in the rotating photoconductor drum causes periodic density variation aligned with scan lines, visible as faint horizontal stripes.

### Copy Art

The "Copy Art" movement of the 1970s–80s embraced the photocopier as an artistic tool. Artists like Sonia Landy Sheridan and Pati Hill deliberately exploited xerographic artifacts, pushing machines to their limits to create images that were as much about the copying process as the original subject. Xero's Copy Art mode doubles the edge enhancement and contrast curve steepness, leaning into the aesthetic of deliberate degradation.

### Toner Colors and Paper Tint

While most office copiers used black toner on white paper, specialized machines and custom toner cartridges offered colored output. Xero provides four toner colors: Black (neutral), Blue (cold corporate), Brown (sepia/archival), and Red (emergency/protest). Paper can be neutral white or warm recycled (yellowish), completing the vintage copier palette.


---

## Signal Flow

```
Input Video (YUV 4:4:4 30-bit)
│
├── Stage 1: Input Register + 2-Pixel Delay Line ──────
│   ├─ y_in = current pixel
│   ├─ y_d1 = 1-pixel delayed (center of kernel)
│   └─ y_d2 = 2-pixel delayed
│
├── Stage 2: Laplacian Edge Enhancement + Brightness ──
│   ├─ laplacian = y_d2 − 2·y_d1 + y_in
│   ├─ edge_scaled = laplacian × edge_enhance / 1024
│   │   (or / 512 in Copy Art mode)
│   ├─ bright_off = brightness − 512 (signed offset)
│   └─ enhanced = y_d1 + edge_scaled + bright_off
│
├── Stage 3: Generation Loss + Toner Grain ─────────────
│   ├─ centered = enhanced − 512
│   ├─ gain = 1024 + generations (×2 in Copy Art)
│   ├─ curved = 512 + centered × gain / 1024
│   ├─ noise = LFSR[5:0] − 32 (±32 range)
│   ├─ grain = noise × toner_grain / 64
│   └─ grained = curved + grain
│
├── Stage 4: Drum Banding + Fuser Streak + Toner Color ─
│   ├─ band_mod = triangle_wave(line_counter) × banding
│   ├─ streak_mod = proximity(h_counter, streak_pos) × fuser
│   ├─ final_y = grained + band_mod + streak_mod
│   ├─ density = 1023 − final_y
│   ├─ u = paper_u + toner_delta_u × density / 1024
│   └─ v = paper_v + toner_delta_v × density / 1024
│
├── Mix (3× interpolator_u) ────────────────────────────
│   └─ lerp(dry, wet, mix_amount)
│
└── Bypass → Output
```

The processing chain is intentionally ordered to match the physics of xerographic copying. Edge enhancement comes first because it models a phenomenon at the photoconductor surface, before toner is applied. Generation loss (contrast curve) follows because it represents the cumulative effect of multiple copy passes. Grain is added after the contrast curve because toner particles are distributed on the already-thresholded image. Drum banding and fuser streak are mechanical artifacts that modulate the final density. Toner colorization is applied last, proportional to darkness — darker areas receive more toner color, while paper shows through in bright areas.

---

## Parameter Reference

<img src={xero_control_panel} alt="Videomancer front panel with Xero loaded"/>
*Videomancer's front panel with Xero active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Edge Enhance
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the intensity of the horizontal Laplacian edge enhancement. At 0% there is no edge effect. Increasing the control amplifies the overshoot at brightness transitions, creating the characteristic bright-fringe / dark-fringe halos around edges. In Copy Art mode, the effective gain is doubled — strong settings produce extreme high-frequency ringing.

---

#### Knob 2 — Generations
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the steepness of the generation-loss contrast S-curve. At 0% the curve is linear (no tonal compression). Increasing the control steepens the midtone slope, progressively crushing shadows and clipping highlights. This simulates the cumulative degradation of copying a copy repeatedly. Maximum settings produce a near-binary, soot-and-flash graphic.

---

#### Knob 3 — Toner Grain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of toner grain noise. An LFSR noise source generates a ±32 count random offset that is scaled by this parameter and added to the post-curve luminance. The grain is most visible in midtones where the contrast curve hasn't already pushed values to the clipping rails. Higher settings create a rough, sandpaper-like texture.

---

#### Knob 4 — Drum Banding
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the intensity of drum banding — periodic horizontal density stripes caused by drum eccentricity. A triangle wave with a 16-line period modulates the luminance. At 0% there is no banding. Higher settings make the horizontal stripes more visible, adding a rhythmic mechanical texture.

---

#### Knob 5 — Fuser Streak
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the intensity of the fuser streak — a wandering vertical bright line that simulates a defective fuser roller. The streak position drifts randomly by ±1 pixel per frame using an LFSR bit, creating a slow horizontal wander. The streak brightness falls off within 3 pixels of center, creating a soft vertical highlight.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | -50% – 50% |
| Default | 0% |
| Suffix | % |

Controls the overall exposure offset. The parameter is centered at 512 (mid-range), producing zero offset. Values above 512 brighten the image; values below darken it. This simulates adjusting the copier's exposure control — the dial that every office worker has turned to lighten or darken their copies.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Toner Hi** | Off | On |
| **8 — Toner Lo** | Off | On |
| **9 — Paper Tint** | Neutral | Warm |
| **10 — Mode** | Standard | Copy Art |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a 2-bit toner color selector (Hi and Lo bits). Toggle 9 selects between neutral white and warm recycled paper. Toggle 10 selects between Standard and Copy Art modes. Toggle 11 bypasses all processing. The toner system uses a "density-proportional" model — darker areas receive more toner color while light areas show paper color.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input signal and the processed xerographic output. At 0% the output is the unprocessed input. At 100% the output is the full copy simulation. Intermediate positions blend the effect at varying intensity, useful for subtle vintage texture overlays.

---

## Guided Exercises

These exercises progress from basic copy simulation to extreme copy-art deconstruction, layering artifacts one at a time to understand how each stage contributes to the overall xerographic aesthetic.

### Exercise 1: First-Generation Copy

<img src={xero_exercise1_result} alt="First-Generation Copy result"/>
*First-Generation Copy — simulated result across source images.*
**Source**: A photograph or video feed with smooth gradients and fine detail — a portrait or landscape works well.

**Objective**: Create a clean, first-generation photocopy look using edge enhancement and minimal generation loss.

1. **Edge enhancement**: Set Edge Enhance to ~50%. Observe the bright/dark halos appearing around edges.
2. **Gentle generation loss**: Set Generations to ~25%. Smooth gradients begin to flatten slightly.
3. **Add grain**: Increase Toner Grain to ~20%. A subtle texture appears, especially in midtones.
4. **Paper choice**: Toggle Paper Tint to Warm for a recycled paper look.
5. **Black toner**: Keep both Toner Hi and Toner Lo off for classic black-and-white copying.

**Key concepts**: Edge enhancement is a Laplacian operator, generation loss is a contrast S-curve, grain is LFSR noise scaled by toner amount

---

### Exercise 2: Fifth-Generation Degradation

<img src={xero_exercise2_result} alt="Fifth-Generation Degradation result"/>
*Fifth-Generation Degradation — simulated result across source images.*
**Source**: Same source as Exercise 1, to compare degradation against the cleaner version.

**Objective**: Simulate extreme multi-generational copying with mechanical artifacts.

1. **Heavy generation loss**: Set Generations to ~80%. The image becomes stark and high-contrast.
2. **Strong edges**: Increase Edge Enhance to ~80%. Edge halos become prominent.
3. **Drum banding**: Set Drum Banding to ~50%. Horizontal stripes appear across the image.
4. **Fuser streak**: Set Fuser Streak to ~40%. A vertical bright line wanders slowly across the frame.
5. **Heavy grain**: Increase Toner Grain to ~60%. The surface becomes rough and grainy.
6. **Blue toner**: Set Toner Lo On, Toner Hi Off. The image shifts to cold corporate blue.

**Key concepts**: Multiple generation loss creates high-contrast graphics, drum banding is periodic, fuser streak wanders per frame via LFSR random walk

---

### Exercise 3: Copy Art Extreme

<img src={xero_exercise3_result} alt="Copy Art Extreme result"/>
*Copy Art Extreme — simulated result across source images.*
**Source**: High-contrast footage — faces, hands on a copier glass, text pages, or object silhouettes.

**Objective**: Push the Copy Art mode to maximum for zine-aesthetic abstract graphics.

1. **Copy Art mode**: Toggle Mode to Copy Art. Edge and contrast effects are immediately doubled.
2. **Maximum edges**: Set Edge Enhance to ~90%. Extreme ringing creates graphic outlines.
3. **Maximum generations**: Set Generations to ~90%. Image collapses to near-binary.
4. **Red toner**: Set both Toner Hi and Toner Lo On. Output shifts to urgent red.
5. **Darken exposure**: Reduce Brightness to ~30%. Shadows deepen, creating heavy, inky areas.
6. **All artifacts**: Enable Drum Banding (~40%) and Fuser Streak (~50%) for full mechanical degradation.

**Key concepts**: Copy Art mode doubles both edge enhancement and contrast gain, producing the exaggerated aesthetics of deliberate copier abuse

---


## Tips

- **Layer artifacts gradually**: Start with just Edge Enhance, then add Generations, then Grain. Each layer adds character — the effect is most convincing when artifacts are balanced rather than all at maximum.
- **Brightness compensates generation loss**: Heavy generation loss clips highlights. Reducing Brightness shifts the tonal center downward, preserving more detail in the compressed range.
- **Copy Art for graphics**: Copy Art mode is most effective with high-contrast source material. Portraits become stark graphic prints; text becomes bold woodcut-style lettering.
- **Grain reveals midtones**: Toner grain is most visible in the 30–70% gray range, where it mimics the sparse, uneven toner coverage of a running-low cartridge.
- **Warm paper + brown toner = archive look**: This combination produces the appearance of an aged document found in a storage box — yellowish paper with sepia-toned text.
- **Fuser streak for authenticity**: A tiny amount of Fuser Streak (10–15%) adds a subtle mechanical imperfection that makes the simulation more convincing than a clean copy effect.
- **Red toner for urgency**: Red toner on white paper evokes emergency notices, protest flyers, and confidential stamps — a powerful visual shorthand.

---

## Glossary

| Term | Definition |
|------|------------|
| **Copy Art** | An artistic movement using photocopiers as creative tools, deliberately exploiting machine artifacts for aesthetic effect. |
| **Drum Banding** | Periodic horizontal density variation caused by eccentricity in the photocopier's rotating photoconductor drum. |
| **Edge Enhancement** | Amplification of brightness transitions using a spatial derivative (Laplacian), creating overshoot halos at edges. |
| **Fuser** | The heated roller in a photocopier that melts toner particles onto paper; defects cause vertical streak artifacts. |
| **Generation Loss** | Progressive degradation of image quality when a copy is made from a copy, modeled as an S-curve contrast function. |
| **Laplacian** | A spatial second-derivative operator that detects edges; here implemented as a 3-pixel horizontal kernel. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **Photoconductor** | The light-sensitive drum in a xerographic copier that holds the electrostatic image pattern. |
| **S-Curve** | A sigmoidal contrast function that compresses shadows and highlights while steepening midtone contrast. |
| **Toner** | Dry powder (polymer particles with carbon black) fused to paper by heat in xerographic copying. |
| **Xerography** | The dry electrostatic copying process invented by Chester Carlson in 1938, commercialized by Haloid/Xerox. |
