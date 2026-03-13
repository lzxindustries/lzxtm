---
draft: true
sidebar_position: 84
slug: /instruments/videomancer/diorama
title: "Diorama"
image: /img/instruments/videomancer/diorama/diorama_hero_s1.png
description: "A Victorian diorama is a miniature theater — layers of painted scenery stacked at different distances from the viewer, lit from behind so that near layers appear sharp and vivid while far layers recede into haze."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import diorama_control_panel from '/img/instruments/videomancer/diorama/diorama_control_panel.png';
import diorama_source1_castle from '/img/instruments/videomancer/diorama/diorama_source1_castle.png';
import diorama_source2_parrot from '/img/instruments/videomancer/diorama/diorama_source2_parrot.png';
import diorama_source3_collage from '/img/instruments/videomancer/diorama/diorama_source3_collage.png';
import diorama_source4_pattern from '/img/instruments/videomancer/diorama/diorama_source4_pattern.png';
import diorama_source5_man from '/img/instruments/videomancer/diorama/diorama_source5_man.png';
import diorama_source6_berries from '/img/instruments/videomancer/diorama/diorama_source6_berries.png';
import diorama_hero_s1 from '/img/instruments/videomancer/diorama/diorama_hero_s1.png';
import diorama_hero_s2 from '/img/instruments/videomancer/diorama/diorama_hero_s2.png';
import diorama_hero_s3 from '/img/instruments/videomancer/diorama/diorama_hero_s3.png';
import diorama_hero_s4 from '/img/instruments/videomancer/diorama/diorama_hero_s4.png';
import diorama_hero_s5 from '/img/instruments/videomancer/diorama/diorama_hero_s5.png';
import diorama_hero_s6 from '/img/instruments/videomancer/diorama/diorama_hero_s6.png';
import diorama_ex1_s1 from '/img/instruments/videomancer/diorama/diorama_ex1_s1.png';
import diorama_ex1_s2 from '/img/instruments/videomancer/diorama/diorama_ex1_s2.png';
import diorama_ex1_s3 from '/img/instruments/videomancer/diorama/diorama_ex1_s3.png';
import diorama_ex1_s4 from '/img/instruments/videomancer/diorama/diorama_ex1_s4.png';
import diorama_ex1_s5 from '/img/instruments/videomancer/diorama/diorama_ex1_s5.png';
import diorama_ex1_s6 from '/img/instruments/videomancer/diorama/diorama_ex1_s6.png';
import diorama_ex2_s1 from '/img/instruments/videomancer/diorama/diorama_ex2_s1.png';
import diorama_ex2_s2 from '/img/instruments/videomancer/diorama/diorama_ex2_s2.png';
import diorama_ex2_s3 from '/img/instruments/videomancer/diorama/diorama_ex2_s3.png';
import diorama_ex2_s4 from '/img/instruments/videomancer/diorama/diorama_ex2_s4.png';
import diorama_ex2_s5 from '/img/instruments/videomancer/diorama/diorama_ex2_s5.png';
import diorama_ex2_s6 from '/img/instruments/videomancer/diorama/diorama_ex2_s6.png';
import diorama_ex3_s1 from '/img/instruments/videomancer/diorama/diorama_ex3_s1.png';
import diorama_ex3_s2 from '/img/instruments/videomancer/diorama/diorama_ex3_s2.png';
import diorama_ex3_s3 from '/img/instruments/videomancer/diorama/diorama_ex3_s3.png';
import diorama_ex3_s4 from '/img/instruments/videomancer/diorama/diorama_ex3_s4.png';
import diorama_ex3_s5 from '/img/instruments/videomancer/diorama/diorama_ex3_s5.png';
import diorama_ex3_s6 from '/img/instruments/videomancer/diorama/diorama_ex3_s6.png';

# Diorama

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: diorama_source1_castle, after: diorama_hero_s1 },
    { label: "Parrot", before: diorama_source2_parrot, after: diorama_hero_s2 },
    { label: "Collage", before: diorama_source3_collage, after: diorama_hero_s3 },
    { label: "Pattern", before: diorama_source4_pattern, after: diorama_hero_s4 },
    { label: "Man", before: diorama_source5_man, after: diorama_hero_s5 },
    { label: "Berries", before: diorama_source6_berries, after: diorama_hero_s6 },
  ]}
/>
*Diorama layering luminance-stratified depth zones with atmospheric fog and chroma desaturation to create a theatrical parallax illusion.*

---

## Overview

A Victorian diorama is a miniature theater — layers of painted scenery stacked at different distances from the viewer, lit from behind so that near layers appear sharp and vivid while far layers recede into haze. The effect is convincing not because the individual layers are realistic, but because the *relationships between them* follow rules the eye already expects: close things are bright and colorful, distant things are pale and gray.

Diorama applies those rules to live video. It analyzes the luminance of each pixel, assigns it to one of three depth zones (near, mid, far), and then applies zone-dependent processing: fog blending, chroma desaturation, and contrast scaling. The result is a synthetic depth field derived entirely from brightness — bright regions appear to push forward, dark regions recede into atmospheric haze. A DDS-based oscillator can animate a slow lateral drift, adding a parallax wobble that reinforces the layered illusion.

At subtle settings, Diorama adds a gentle atmospheric perspective — distant objects fade into a blue-gray haze while foreground subjects retain full color and contrast. At extreme settings, the image separates into hard-edged tonal planes with heavy fog tinting, resembling a hand-painted theatrical backdrop or a color-separated film composite.

---

## Quick Start

1. **Use zone visualization for setup**: Enable Show Zones (Toggle 9) to see exactly how pixels are being classified before dialing in fog and contrast. This saves time when fine-tuning the Parallax threshold.
2. **Start with Fog Depth, then add contrast**: Set your fog blend level first with contrast at unity (50%). Then sweep contrast to amplify or soften the depth separation. Working in this order avoids confusion about which parameter is doing what.
3. **Invert Depth for dark-subject footage**: If your subject is darker than the background, enable Invert Depth so the subject is classified as near (foreground) and retains full color and contrast.

---

## Background

### Atmospheric Perspective in Painting

Renaissance painters discovered that distant objects appear bluer, lighter, and less saturated than near objects. Leonardo da Vinci formalized this as *sfumato* and *atmospheric perspective* — the understanding that air itself has color, and that layers of atmosphere between the viewer and a distant object progressively scatter short-wavelength light. Every landscape painting since has used this principle: warm, saturated foregrounds and cool, desaturated backgrounds. Diorama applies the same logic to video, using brightness as a proxy for distance.

### The Victorian Diorama

The original diorama was a theatrical entertainment invented by Louis Daguerre in 1822 — before he invented photography. Audiences sat in a rotating auditorium while enormous translucent paintings were illuminated from the front and back to create illusions of depth, time of day, and weather. The key technique was *layering*: near elements were painted on opaque panels, mid-ground on semi-transparent scrims, and far elements on backlit translucent screens. Each layer received different lighting, creating parallax as the viewer's angle shifted. Diorama's zone classification and per-zone processing replicate this layered approach digitally.

### Depth from Luminance

In the absence of stereoscopic information, the human visual system uses many monocular cues to infer depth. One of the strongest is *luminance contrast*: bright objects against a dark background appear closer, and objects with lower contrast appear farther away. Photographers call this "tonal separation." Diorama exploits this cue directly — it maps pixel brightness to a depth factor and then applies depth-dependent effects. This is a simplification compared to true depth estimation (which would require stereo cameras or time-of-flight sensors), but it is remarkably effective for creating the *impression* of depth from a flat video signal.

### Fog in Film and Games

Fog is a fundamental rendering primitive in 3D computer graphics. OpenGL and Direct3D both provide built-in fog equations — linear and exponential — that blend distant geometry toward a fog color based on depth. Film colorists use a similar technique called *atmospheric grading*: pulling shadows toward a cool color and highlights toward a warm color to create the illusion of aerial perspective. Diorama implements the same linear fog model used in classic 3D graphics: blend amount increases linearly with depth factor, mixing the pixel color toward a configurable fog color.

### Zone Quantization and Posterized Depth

Rather than treating depth as a continuous gradient, Diorama can quantize the luminance into discrete steps — like the distinct planes of a paper theater. This quantization is controlled by the Layers parameter, which determines how many discrete depth levels exist between the near and far thresholds. With few layers, the image separates into bold, flat tonal planes; with many layers, the transitions become smoother. This is related to the concept of *posterization* from print media, but applied to the depth dimension rather than the color dimension.


---

## Signal Flow

Input Registration → Zone Classification → Fog Blending → Contrast → Output Saturation Clamp → Output Register

```
Input Video (YUV 4:4:4)
│
├── Stage 0: Input Registration + Parameter Latch (1 clk) ─────
│   ├─ Register Y, U, V inputs
│   ├─ Compute near/far thresholds from Parallax parameter
│   │   near_thresh = 512 + parallax / 4
│   │   far_thresh  = 512 - parallax / 4
│   └─ DDS drift animation (16-bit phase accumulator)
│
├── Stage 1: Zone Classification + Depth Factor (1 clk) ───────
│   ├─ Optional depth inversion (Invert Depth toggle)
│   ├─ Classify: near (Y ≥ near_thresh), far (Y ≤ far_thresh), mid
│   ├─ Depth factor: 0 (near) → linear interpolation → 1023 (far)
│   └─ Luma quantization for layer stepping (Layers parameter)
│
├── Stage 2: Fog Blending + Desaturation (1 clk) ──────────────
│   ├─ Fog blend amount = depth_factor × fog_depth / 1024
│   ├─ Fog color: default blue/gray (Y=400, U=600, V=450)
│   │             or custom hue from Fog Color parameter
│   ├─ Y blending: y_out = y × (1 - blend) + fog_y × blend
│   └─ Chroma desaturation: U,V → midpoint proportional to blend
│
├── Stage 3: Contrast + Zone Visualization (1 clk) ────────────
│   ├─ Show Zones mode: false color (near=green, mid=yellow, far=blue)
│   └─ Contrast: proc_amp (512 = unity, 0 = flat, 1023 = 2×)
│
├── Stage 4: Output Saturation Clamp (1 clk) ──────────────────
│
├── Stage 5: Output Register (1 clk) ──────────────────────────
│
├── Interpolator: Wet/Dry Mix (4 clk, 3× interpolator_u) ─────
│   └─ Crossfade original → processed via Mix fader
│
├── Sync Delay Pipeline (10 clk shift register) ───────────────
│   └─ hsync, vsync, field, Y, U, V delayed to match processing
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select original (delayed) or mixed output
```

The central interaction is between the zone classifier and the fog blender. The Parallax parameter controls how *wide* the separation is between the near and far thresholds — at zero, all pixels cluster around the midpoint with a narrow mid zone; at maximum, the thresholds spread to 768 (near) and 256 (far), creating broad, well-separated depth zones. The depth factor then drives two downstream effects simultaneously: fog blending (Y toward fog color) and chroma desaturation (U, V toward midpoint 512). These two effects compound — far-zone pixels lose both brightness contrast and color saturation, exactly mimicking atmospheric perspective.

The contrast stage sits *after* fog blending, meaning it amplifies or compresses the already-fogged signal. At low contrast, the depth zones flatten into a uniform haze; at high contrast, the zone boundaries become dramatic and theatrical.

---

## Parameter Reference

<img src={diorama_control_panel} alt="Videomancer front panel with Diorama loaded"/>
*Videomancer's front panel with Diorama active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Parallax
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At minimum, the near and far thresholds collapse to the midpoint — nearly all pixels fall into the mid zone, receiving moderate fog treatment. As you increase Parallax, the thresholds spread apart: bright pixels are classified as near (receiving no fog), dark pixels as far (receiving maximum fog), and the mid zone widens. At maximum, the full brightness range is divided into clearly separated zones with distinct visual treatment. Internally, controls the sensitivity of the depth zone classifier.

---

#### Knob 2 — Fog Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

At zero, no fog is applied regardless of depth classification — the depth zones are computed but have no visible effect. As you increase Fog Depth, far-zone pixels are progressively blended toward the fog color while their chroma is desaturated. At maximum, far-zone pixels are nearly replaced by the fog color. The mid zone always receives a proportionally reduced fog treatment. Internally, sets the maximum fog intensity applied to the far zone.

---

#### Knob 3 — Layers
| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 5 |

Determines the number of discrete depth steps between near and far. With fewer layers, the image separates into bold, flat tonal planes with visible boundaries — like a paper theater with distinct cutout panels. With more layers, the depth gradient becomes smoother and more continuous. The quantization is applied to the working luminance value before zone classification, so it affects both the fog intensity and the visual appearance of the depth planes.

---

#### Knob 4 — Drift Spd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

At zero, the fog is static. As you increase Drift Speed, a slow animation modulates the fog brightness via a 16-bit phase accumulator that advances on each vertical sync. The effect is a subtle pulsing or breathing of the fog layer. At high speeds, the modulation becomes a rapid shimmer. The drift animation is only active when the Animate Fog toggle is enabled. Internally, controls the speed of the DDS-based lateral drift oscillator.

---

#### Knob 5 — Fog Color
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 60° |
| Suffix | ° |

Selects the hue of the custom fog color when the Fog Custom toggle is active. The parameter maps a full 360° hue rotation, allowing you to tint the fog any color — warm amber for a sunset atmosphere, cool cyan for an underwater feel, or deep red for an infernal mood. When Fog Custom is off, the program uses a default blue-gray fog that mimics natural atmospheric haze.

---

#### Knob 6 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Adjusts the contrast of the fogged image. At the midpoint (50%), contrast is unity — the fog blend is preserved as computed. Below the midpoint, contrast is reduced, flattening the image toward mid-gray and softening the zone boundaries. Above the midpoint, contrast is amplified, making zone transitions more dramatic and increasing the visual separation between near and far regions. The contrast operates in proc_amp style: deviation from midpoint (512) is scaled by the parameter, then re-centered.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Layer Mode** | Luma | Zone |
| **8 — Fog Type** | Linear | Exp |
| **9 — Drift Dir** | Left | Right |
| **10 — Freeze** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options that modify different stages of the processing pipeline. Fog Custom (Toggle 7) selects the fog color source. Invert Depth (Toggle 8) flips the luminance-to-depth mapping. Show Zones (Toggle 9) replaces the output with a false-color diagnostic visualization. Animate Fog (Toggle 10) enables the DDS drift oscillator. Bypass (Toggle 11) routes the input directly to the output. These toggles do not interact with each other except through the sequential pipeline — for example, Invert Depth reverses which pixels are classified as near vs. far, which changes where fog is applied, which in turn changes what the zone visualization shows.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Diorama processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Diorama-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from basic depth classification through atmospheric fog to animated theatrical layering. Each builds on the previous, gradually engaging more of the processing chain.

### Exercise 1: Depth Zone Mapping

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: diorama_source1_castle, after: diorama_ex1_s1 },
    { label: "Parrot", before: diorama_source2_parrot, after: diorama_ex1_s2 },
    { label: "Collage", before: diorama_source3_collage, after: diorama_ex1_s3 },
    { label: "Pattern", before: diorama_source4_pattern, after: diorama_ex1_s4 },
    { label: "Man", before: diorama_source5_man, after: diorama_ex1_s5 },
    { label: "Berries", before: diorama_source6_berries, after: diorama_ex1_s6 },
  ]}
/>
*Depth Zone Mapping — simulated result across source images.*
**Source**: A live camera feed or recorded footage with clear tonal separation — bright foreground subjects against a dark background, or a landscape with distinct highlights and shadows.

**What You'll Create**: Learn how the zone classifier divides the image by luminance and how the Parallax parameter controls zone boundaries.

1. **Enable zone visualization**: Turn on Show Zones (Toggle 9). The image becomes a false-color map: green (near), yellow (mid), blue (far).
2. **Sweep Parallax**: Slowly increase from 0% to 100%. At low values, most pixels are mid-zone (yellow). As you increase, green and blue regions grow as near and far thresholds separate.
3. **Invert depth**: Enable Invert Depth (Toggle 8). The zone colors swap — what was near becomes far and vice versa. Toggle back and forth to see the reversal.
4. **Adjust Layers**: Sweep the Layers knob. With fewer layers, the zone map becomes blocky and posterized. With more layers, the transitions soften.
5. **Disable visualization**: Turn off Show Zones to see the actual processed output with fog and contrast applied to the zones you just mapped.

**Key concepts**: Luminance drives zone classification, Parallax sets the threshold spread, Invert Depth reverses the depth mapping, zone visualization is a diagnostic tool for setup

---

### Exercise 2: Atmospheric Fog Grading

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: diorama_source1_castle, after: diorama_ex2_s1 },
    { label: "Parrot", before: diorama_source2_parrot, after: diorama_ex2_s2 },
    { label: "Collage", before: diorama_source3_collage, after: diorama_ex2_s3 },
    { label: "Pattern", before: diorama_source4_pattern, after: diorama_ex2_s4 },
    { label: "Man", before: diorama_source5_man, after: diorama_ex2_s5 },
    { label: "Berries", before: diorama_source6_berries, after: diorama_ex2_s6 },
  ]}
/>
*Atmospheric Fog Grading — simulated result across source images.*
**Source**: Landscape footage, cityscape, or any scene with natural depth variation — a park with trees at different distances works well.

**What You'll Create**: Explore fog blending and chroma desaturation to create atmospheric perspective.

1. **Set moderate Parallax**: About 50% to establish clear zone separation.
2. **Sweep Fog Depth**: Slowly increase from 0% to 100%. Watch far-zone areas progressively fade into blue-gray haze while near-zone areas remain vivid.
3. **Compare fog colors**: Toggle Fog Custom (Toggle 7) on. Sweep the Fog Color knob through warm and cool hues. Notice how the fog tint changes the mood — warm amber feels like golden hour, cool cyan feels underwater.
4. **Adjust contrast**: Sweep Contrast from 0% to 100%. At low values, the entire image flattens into fog. At high values, the zone boundaries become dramatic and theatrical.
5. **Subtle blend**: Lower Mix to about 40–60%. The fog effect becomes a gentle atmospheric overlay rather than a complete transformation.

**Key concepts**: Fog blending interpolates between the pixel color and the fog color proportional to depth, chroma desaturation accompanies fog for realistic atmospheric perspective, contrast amplifies or softens the depth-dependent treatment

---

### Exercise 3: Animated Paper Theater

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: diorama_source1_castle, after: diorama_ex3_s1 },
    { label: "Parrot", before: diorama_source2_parrot, after: diorama_ex3_s2 },
    { label: "Collage", before: diorama_source3_collage, after: diorama_ex3_s3 },
    { label: "Pattern", before: diorama_source4_pattern, after: diorama_ex3_s4 },
    { label: "Man", before: diorama_source5_man, after: diorama_ex3_s5 },
    { label: "Berries", before: diorama_source6_berries, after: diorama_ex3_s6 },
  ]}
/>
*Animated Paper Theater — simulated result across source images.*
**Source**: High-contrast footage with moving subjects — dancers, performers, or any scene with figure-ground separation.

**What You'll Create**: Combine depth layering with animated fog drift and reduced layers for a theatrical paper-cutout aesthetic.

1. **Bold zones**: Set Parallax to about 70% for wide zone separation.
2. **Heavy fog**: Increase Fog Depth to about 80%.
3. **Few layers**: Reduce Layers to minimum for bold posterized depth planes.
4. **Custom fog color**: Enable Fog Custom and set Fog Color to a warm amber (~60°) for a stage-lighting feel.
5. **Enable animation**: Turn on Animate Fog (Toggle 10). Set Drift Speed to about 30% for a slow, gentle breathing effect.
6. **Maximize contrast**: Push Contrast toward 80%. The depth planes become dramatically separated — near elements pop, far elements dissolve into colored haze.
7. **Full mix**: Set Mix to 100% and observe the complete animated theatrical depth effect.

**Key concepts**: Reduced Layers creates discrete tonal planes like paper theater cutouts, DDS drift animation adds organic breathing to the fog layer, high contrast emphasizes the theatrical separation between near and far

---


## Tips

- **Subtle mix for grading**: Set Mix to 30–50% for a gentle atmospheric grading effect that adds depth cues without overwhelming the source material.
- **Custom fog for mood**: Use the Fog Color knob with Fog Custom enabled to dramatically shift the emotional tone — warm amber for nostalgia, deep blue for cold solitude, green for an eerie underwater feeling.
- **Animate for organic feel**: Enable Animate Fog at low Drift Speed (10–20%) for a subtle fog breathing effect that prevents the depth layering from looking static and artificial.
- **Feedback routing**: Routing the output back to the input creates recursive fog layering — each pass pushes far-zone pixels further into the fog color, eventually dissolving them entirely while near-zone pixels remain.
- **Few layers for theatrical look**: Set Layers to minimum for bold, poster-like depth planes that resemble actual theatrical scenery cutouts.

---

## Glossary

| Term | Definition |
|------|------------|
| **Atmospheric Perspective** | The visual phenomenon where distant objects appear lighter, bluer, and less saturated due to light scattering through intervening air. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space; distinct from luminance. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator and lookup table. |
| **Depth Factor** | A per-pixel value (0–1023) computed from luminance, representing relative distance from the viewer; 0 = near, 1023 = far. |
| **Desaturation** | Reducing the intensity of color components toward the neutral midpoint, making the image appear more gray. |
| **Fog Blending** | Linear interpolation between the pixel color and a fog color, controlled by a depth-dependent blend factor. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Phase Accumulator** | A register that increments by a fixed step each clock cycle, wrapping around to create a periodic ramp; the core of DDS. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **Quantization** | Mapping a continuous range of values to a smaller set of discrete levels, producing visible steps in gradients. |
| **Zone Classification** | The process of assigning each pixel to a depth zone (near, mid, or far) based on its luminance value relative to threshold parameters. |

---
