---
draft: true
sidebar_position: 257
slug: /instruments/videomancer/schufftan
title: "Schufftan"
image: /img/instruments/videomancer/schufftan/schufftan_hero_s1.png
description: "The Schüfftan process was a visual effects technique invented in 1920s German cinema."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import schufftan_source1_parrot from '/img/instruments/videomancer/schufftan/schufftan_source1_parrot.png';
import schufftan_source2_dog from '/img/instruments/videomancer/schufftan/schufftan_source2_dog.png';
import schufftan_source3_turtle from '/img/instruments/videomancer/schufftan/schufftan_source3_turtle.png';
import schufftan_source4_pattern from '/img/instruments/videomancer/schufftan/schufftan_source4_pattern.png';
import schufftan_source5_woman from '/img/instruments/videomancer/schufftan/schufftan_source5_woman.png';
import schufftan_source6_berries from '/img/instruments/videomancer/schufftan/schufftan_source6_berries.png';
import schufftan_hero_s1 from '/img/instruments/videomancer/schufftan/schufftan_hero_s1.png';
import schufftan_hero_s2 from '/img/instruments/videomancer/schufftan/schufftan_hero_s2.png';
import schufftan_hero_s3 from '/img/instruments/videomancer/schufftan/schufftan_hero_s3.png';
import schufftan_hero_s4 from '/img/instruments/videomancer/schufftan/schufftan_hero_s4.png';
import schufftan_hero_s5 from '/img/instruments/videomancer/schufftan/schufftan_hero_s5.png';
import schufftan_hero_s6 from '/img/instruments/videomancer/schufftan/schufftan_hero_s6.png';
import schufftan_ex1_s1 from '/img/instruments/videomancer/schufftan/schufftan_ex1_s1.png';
import schufftan_ex1_s2 from '/img/instruments/videomancer/schufftan/schufftan_ex1_s2.png';
import schufftan_ex1_s3 from '/img/instruments/videomancer/schufftan/schufftan_ex1_s3.png';
import schufftan_ex1_s4 from '/img/instruments/videomancer/schufftan/schufftan_ex1_s4.png';
import schufftan_ex1_s5 from '/img/instruments/videomancer/schufftan/schufftan_ex1_s5.png';
import schufftan_ex1_s6 from '/img/instruments/videomancer/schufftan/schufftan_ex1_s6.png';
import schufftan_ex2_s1 from '/img/instruments/videomancer/schufftan/schufftan_ex2_s1.png';
import schufftan_ex2_s2 from '/img/instruments/videomancer/schufftan/schufftan_ex2_s2.png';
import schufftan_ex2_s3 from '/img/instruments/videomancer/schufftan/schufftan_ex2_s3.png';
import schufftan_ex2_s4 from '/img/instruments/videomancer/schufftan/schufftan_ex2_s4.png';
import schufftan_ex2_s5 from '/img/instruments/videomancer/schufftan/schufftan_ex2_s5.png';
import schufftan_ex2_s6 from '/img/instruments/videomancer/schufftan/schufftan_ex2_s6.png';
import schufftan_ex3_s1 from '/img/instruments/videomancer/schufftan/schufftan_ex3_s1.png';
import schufftan_ex3_s2 from '/img/instruments/videomancer/schufftan/schufftan_ex3_s2.png';
import schufftan_ex3_s3 from '/img/instruments/videomancer/schufftan/schufftan_ex3_s3.png';
import schufftan_ex3_s4 from '/img/instruments/videomancer/schufftan/schufftan_ex3_s4.png';
import schufftan_ex3_s5 from '/img/instruments/videomancer/schufftan/schufftan_ex3_s5.png';
import schufftan_ex3_s6 from '/img/instruments/videomancer/schufftan/schufftan_ex3_s6.png';

# Schufftan

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: schufftan_source1_parrot, after: schufftan_hero_s1 },
    { label: "Dog", before: schufftan_source2_dog, after: schufftan_hero_s2 },
    { label: "Turtle", before: schufftan_source3_turtle, after: schufftan_hero_s3 },
    { label: "Pattern", before: schufftan_source4_pattern, after: schufftan_hero_s4 },
    { label: "Woman", before: schufftan_source5_woman, after: schufftan_hero_s5 },
    { label: "Berries", before: schufftan_source6_berries, after: schufftan_hero_s6 },
  ]}
/>
*Schufftan applying luminance-keyed mirror compositing with per-scanline wobble and cool tint to simulate the classic miniature-projection technique.*

---

## Overview

The Schüfftan process was a visual effects technique invented in 1920s German cinema. A partially-scraped mirror was placed between the camera and a miniature set: actors were filmed through the cleared areas of the mirror while the miniature's reflection filled the surrounding frame. The technique created the illusion that actors were standing inside enormous architectural sets that existed only as tabletop models. Fritz Lang's *Metropolis* (1927) is the most famous example.

Schufftan translates this optical concept into the digital video domain. It divides the incoming frame into two regions based on a luminance key — pixels above a threshold and pixels below it. One region (configurable via the Mirror Side toggle) is treated as the "mirror" zone: it receives contrast reduction, horizontal blur, a cool blue-silver colour shift, and optional per-scanline wobble that simulates the imperfect flatness of a physical mirror surface. The other region passes through cleanly, representing the direct camera view through the mirror's cleared areas.

The key softness ramp controls the transition width between mirror and direct regions. A hard key produces a sharp boundary — the digital equivalent of a precisely scraped mirror. A soft key creates a gradual blend, mimicking the optical diffusion at the boundary between clear glass and reflective coating. The wobble parameter adds a sinusoidal per-scanline displacement that gives the mirror region a watery, unstable quality, as if the reflection is about to dissolve.

---

## Background

### The Schüfftan Process in Cinema

Eugen Schüfftan patented his mirror-projection technique in 1923. The principle was simple: mount a mirror at 45° to the camera, place a miniature set where the camera can see its reflection, then carefully scrape away the mirror's reflective coating in the areas where live actors should appear. The camera simultaneously photographs the actors directly through the cleared glass and the miniature as reflected by the remaining mirror surface. The result is a seamless composite — provided the geometry is precisely calibrated and the lighting matches.

The technique was labour-intensive but remarkably effective. It required no optical printing, no matte paintings, and no double exposure. Everything was captured in-camera, in a single take. Fritz Lang used it extensively in *Metropolis* to place actors inside vast Art Deco cityscapes. Alfred Hitchcock employed it in *Blackmail* (1929). The process remained in use through the 1960s before being supplanted by blue-screen compositing and, eventually, digital visual effects.

### Luminance Keying

Schufftan's digital mirror boundary is defined by a **luminance key** — a threshold applied to the Y channel of the incoming video. Pixels brighter than the threshold are assigned to one region; pixels darker are assigned to the other. The Mirror Side toggle determines which side becomes the mirror zone. This is the simplest form of keying, analogous to a high-contrast matte: bright areas are one layer, dark areas are another. The Softness parameter adds a ramp around the threshold, creating a smooth transition zone rather than a hard binary cut.

### Wobble and Imperfect Reflection

Physical mirrors are never perfectly flat. Even high-quality optical mirrors have surface irregularities that distort reflected images, especially when the mirror is large or when it is positioned at an extreme angle. Schufftan simulates this imperfection with a per-scanline sinusoidal displacement — a DDS (Direct Digital Synthesis) oscillator generates a sine wave whose amplitude is controlled by the Wobble parameter. Each scanline in the mirror region is shifted horizontally (or vertically) by this sine value, producing a watery, rippling distortion that evokes an imperfect reflective surface.

### Contrast Reduction and Detail Loss

Reflections are always lower-contrast than direct views. Light bouncing off a mirror passes through the reflective coating twice (in and out), losing energy at each interface. Schufftan models this with two complementary processes: contrast reduction (pushing luminance values toward mid-gray) and detail loss (a horizontal IIR low-pass filter that blurs fine spatial detail). Together, these create the visual signature of a reflected image — slightly washed-out, slightly soft, clearly distinguished from the direct camera view.

### Mirror Tint

Metallic mirrors impart a colour cast to reflected light. Silver mirrors produce a cool blue-grey tint; copper mirrors produce a warm amber. Schufftan simulates this with a UV colour shift applied to the mirror region: U is shifted toward blue, V is shifted toward cool. The Mirror Tint parameter controls the intensity of this shift, from a barely-perceptible coolness to an aggressive blue-silver cast that clearly marks the mirror zone.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 0: Input Register + Horizontal Gradient
│   └─ Y_prev register; gradient = |Y[x] - Y[x-1]|
│
├── Stage 1: Key Computation
│   ├─ Luma mode: key_raw = |Y - key_level|
│   └─ Edge mode: key_raw = gradient magnitude
│
├── Stage 2: Key Softness Ramp
│   └─ alpha = clamp((key_raw - clip) × gain, 0, 1023)
│   └─ Mirror Side inverts alpha
│
├── Stage 3: DDS Wobble
│   └─ wobble_offset = sine_lut[v_count + phase] × wobble_amt >> 10
│   └─ Shift read coordinate (horizontal or vertical)
│
├── Stage 4: Mirror Region — Contrast Reduction
│   └─ Y' = (Y - 512) × (1023 - contrast_reduce) >> 10 + 512
│
├── Stage 5: Mirror Region — Detail Loss
│   └─ IIR: y_iir += (y_in - y_iir) >> detail_shift
│
├── Stage 6: Mirror Tint
│   └─ U' = U + (mirror_tint >> 2)
│   └─ V' = V - (mirror_tint >> 3)
│
├── Stage 7: Double Image (optional)
│   └─ Y' = (Y + delayed_Y) >> 1
│
├── Stage 8: Composite
│   └─ output = lerp(original, mirror_processed, alpha)
│
├── Stage 9: Mix + Output Register
│   └─ Interpolate composited ↔ original by Mix amount
│
├── Sync Signals ─── Pass-through
│
└── Bypass ─── Select original or processed signal
```

The pipeline has two distinct phases: key generation (Stages 0–2) and mirror processing (Stages 3–7). The key alpha signal computed in Stage 2 determines *where* the mirror effect is applied, while Stages 3–7 determine *what* the mirror effect looks like. This separation means you can shape the key boundary independently of the mirror's visual character. The wobble displacement in Stage 3 affects only the mirror region's spatial coordinates, not the key boundary itself — the boundary remains smooth while the content within it ripples. The IIR low-pass in Stage 5 is stateless between frames (no BRAM required), operating on a per-scanline basis with the detail_shift parameter controlling the filter cutoff.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Key Thresh
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the luminance threshold that defines the boundary between mirror and direct regions. At 50%, mid-gray pixels sit exactly on the boundary. Lower values shift the boundary darker — more of the image falls into the mirror region. Higher values shift it brighter — only the brightest areas trigger the mirror effect. In Edge mode (Switch 7), this parameter instead sets the gradient magnitude threshold for edge detection.

---

#### Knob 2 — Key Soft
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the softness of the key transition ramp. At 0%, the boundary between mirror and direct regions is a hard binary cut — pixels are either fully mirrored or fully direct. As you increase the control, the transition zone widens into a smooth gradient blend. High softness values create a dreamy, diffused boundary where the mirror effect fades gradually into the direct image, matching the optical behaviour of a partially-transparent reflective coating.

---

#### Knob 3 — Mirror Tint
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the amplitude of the per-scanline sinusoidal wobble applied to the mirror region. At 0%, the mirror region is spatially undistorted. Increasing the control introduces a sine-wave displacement that shifts each scanline horizontally (or vertically, depending on Switch 9), producing a watery, rippling distortion. High values create dramatic funhouse-mirror warping; low values produce a subtle shimmer that suggests an imperfect reflecting surface.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the contrast reduction applied to the mirror region. The processing pushes luminance values toward mid-gray (512): at 0%, no contrast change; at 100%, all luminance in the mirror region is flattened to mid-gray. Intermediate values produce the washed-out, low-contrast appearance characteristic of reflected images — the visual cue that tells the viewer they are looking at a reflection rather than direct reality.

---

#### Knob 5 — Wobble Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the intensity of the blue-silver colour tint applied to the mirror region. U is shifted toward blue, V is shifted toward cool (desaturated). At 0%, no colour shift. Increasing the control produces a progressively stronger cool metallic cast — the colour signature of a silver mirror surface. The tint helps visually separate the mirror zone from the direct zone even when contrast and detail differences are subtle.

---

#### Knob 6 — Wobble Spd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the detail loss (horizontal blur) applied to the mirror region. The processing uses an IIR (infinite impulse response) low-pass filter that smooths fine horizontal detail. At 100%, full detail is preserved — no blur. At 0%, maximum blur — the mirror region becomes a soft, indistinct wash. The IIR filter operates per-scanline with no BRAM requirement, and its cutoff frequency is set by a right-shift of the detail parameter.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Invert Key** | Normal | Invert |
| **8 — Edge Dbl** | Off | On |
| **9 — Detail Loss** | Off | On |
| **10 — Key Source** | Y Only | Y+Edge |
| **11 — Bypass** | Off | On |

The five toggles configure the keying mode, mirror polarity, wobble direction, double-image effect, and bypass. Key Source and Mirror Side interact to determine which image content ends up in the mirror zone. Wobble Dir selects the displacement axis. Double adds a ghost-image layer to the mirror region.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the original input signal and the fully composited mirror output. At 0%, the output is identical to the input. At 100%, the full mirror composite is applied. Intermediate values produce a weighted blend — useful for subtle mirror-tint washes that suggest a reflective surface without fully committing to the effect.

---

## Guided Exercises

These exercises progress from basic luminance keying to full Schüfftan-style mirror compositing, exploring how key shape, mirror character, and wobble interact.

### Exercise 1: Basic Mirror Split

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: schufftan_source1_parrot, after: schufftan_ex1_s1 },
    { label: "Dog", before: schufftan_source2_dog, after: schufftan_ex1_s2 },
    { label: "Turtle", before: schufftan_source3_turtle, after: schufftan_ex1_s3 },
    { label: "Pattern", before: schufftan_source4_pattern, after: schufftan_ex1_s4 },
    { label: "Woman", before: schufftan_source5_woman, after: schufftan_ex1_s5 },
    { label: "Berries", before: schufftan_source6_berries, after: schufftan_ex1_s6 },
  ]}
/>
*Basic Mirror Split — simulated result across source images.*
**Source**: Footage with a clear tonal separation — a brightly-lit subject against a dark background, or a window with daylight and an interior shadow.

**Objective**: Learn to use the luminance key to split the frame into mirror and direct regions.

1. **Set the threshold**: Adjust Key Level to place the boundary between the bright and dark areas of your source.
2. **Hard key**: Set Softness to 0%. The boundary is a sharp cut between mirror and direct.
3. **Mirror character**: Increase Contrast to ~40% and Mirror Tint to ~50%. The mirror region becomes washed-out with a blue-silver cast.
4. **Swap sides**: Toggle Mirror Side (Switch 8). The mirror effect jumps from bright to dark areas.
5. **Soften the edge**: Increase Softness to ~50%. The hard boundary dissolves into a gradual blend.

**Key concepts**: Luminance keying splits frames by brightness, Key Level positions the boundary, Softness controls the transition width, Mirror Side selects polarity

---

### Exercise 2: Wobble and Distortion

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: schufftan_source1_parrot, after: schufftan_ex2_s1 },
    { label: "Dog", before: schufftan_source2_dog, after: schufftan_ex2_s2 },
    { label: "Turtle", before: schufftan_source3_turtle, after: schufftan_ex2_s3 },
    { label: "Pattern", before: schufftan_source4_pattern, after: schufftan_ex2_s4 },
    { label: "Woman", before: schufftan_source5_woman, after: schufftan_ex2_s5 },
    { label: "Berries", before: schufftan_source6_berries, after: schufftan_ex2_s6 },
  ]}
/>
*Wobble and Distortion — simulated result across source images.*
**Source**: A scene with strong geometric lines — architecture, grids, or tile patterns.

**Objective**: Explore how per-scanline wobble distorts the mirror region while leaving the direct region clean.

1. **Establish key**: Set Key Level to ~50%, Softness to ~30%, Contrast to ~30%.
2. **Introduce wobble**: Slowly increase Wobble from 0% to ~60%. Watch the mirror region begin to ripple.
3. **Direction**: Toggle Wobble Dir (Switch 9). Horizontal wobble bends vertical lines; Vertical wobble bends horizontal lines.
4. **Double image**: Enable Double (Switch 10). The ghost adds a translucent layer to the already-wobbling mirror region.
5. **Detail loss**: Reduce Detail to ~30%. The mirror region softens, making the wobble distortion more pronounced against the sharp direct region.

**Key concepts**: Wobble is a per-scanline sine displacement, Direction selects the displacement axis, wobble only affects the mirror region (not the key boundary), Detail loss compounds with wobble for maximum mirror distinction

---

### Exercise 3: Edge-Keyed Mirror Composite

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: schufftan_source1_parrot, after: schufftan_ex3_s1 },
    { label: "Dog", before: schufftan_source2_dog, after: schufftan_ex3_s2 },
    { label: "Turtle", before: schufftan_source3_turtle, after: schufftan_ex3_s3 },
    { label: "Pattern", before: schufftan_source4_pattern, after: schufftan_ex3_s4 },
    { label: "Woman", before: schufftan_source5_woman, after: schufftan_ex3_s5 },
    { label: "Berries", before: schufftan_source6_berries, after: schufftan_ex3_s6 },
  ]}
/>
*Edge-Keyed Mirror Composite — simulated result across source images.*
**Source**: High-contrast footage with strong edges — text, graphic patterns, or architectural details with sharp lines.

**Objective**: Use Edge key mode to apply mirror processing at transitions rather than brightness levels.

1. **Switch to Edge mode**: Set Key Source (Switch 7) to Edge. The key is now driven by horizontal gradient magnitude, not absolute luminance.
2. **Calibrate threshold**: Adjust Key Level to capture the major edges in your source without flooding the frame.
3. **Mirror treatment**: Set Contrast to ~50%, Mirror Tint to ~60%, Detail to ~40%. The edge regions receive full mirror treatment.
4. **Softness**: Increase Softness to ~40%. The mirror effect feathers outward from each edge, creating halos of reflected-looking imagery around transitions.
5. **Wobble halo**: Add Wobble at ~30%. The edge halos now ripple, giving each contour a shimmering, heat-haze quality.
6. **Mix to taste**: Use Mix to dial back the composite — find the point where edges shimmer but the overall image remains legible.

**Key concepts**: Edge mode keys on spatial transitions rather than brightness, edge keys produce haloed borders around contours, Softness feathers the edge key outward, combining edge key with wobble creates shimmering contour effects

---


## Tips

- **Key Level is scene-dependent**: The optimal threshold depends entirely on the tonal structure of your source material. Start at 50% and sweep until the key boundary lands where you want it.
- **Softness for naturalism**: Hard keys look digital; soft keys look optical. For a convincing Schüfftan look, use Softness of at least 20–30%.
- **Wobble amplitude goes a long way**: Even small Wobble values (10–20%) create a noticeable ripple. Reserve high values for deliberate funhouse-mirror effects.
- **Combine Contrast and Detail for mirror realism**: Real reflections are both lower-contrast and softer than direct views. Use both controls together for the most convincing mirror zone.
- **Mirror Tint as colour grade**: At low Key Level with soft key, the mirror tint becomes a gentle cool colour wash over most of the frame — usable as a cinematic colour grade tool.
- **Edge mode for contour effects**: Edge keying applies the mirror treatment to spatial transitions rather than brightness levels, creating haloed contours with the mirror's soft, tinted character.
- **Feedback loops**: Routing Schufftan's output back to its input creates recursive keying — the mirror region's contrast reduction and tint accumulate, progressively separating the two zones into distinct visual layers.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha** | A per-pixel transparency value (0–1023) controlling the blend between two image layers; here, between mirror and direct regions. |
| **BT.601** | ITU-R Recommendation BT.601; the colour space standard defining YUV encoding used throughout the Videomancer pipeline. |
| **Chroma** | The colour information in a video signal, encoded as U and V components in YUV colour space. |
| **Composite** | The process of combining two or more image layers into a single output using alpha blending or keying. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms (here, a sine wave for wobble) using a phase accumulator and lookup table. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **IIR** | Infinite Impulse Response; a filter whose output depends on both current input and previous output, creating exponential smoothing. |
| **Keying** | Separating an image into foreground and background regions based on a signal characteristic (luminance, colour, or edge). |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage applying brightness and contrast adjustment. |
| **Schüfftan Process** | A 1920s visual effects technique using a partially-scraped mirror to composite live actors with miniature sets. |
| **YUV** | A colour encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
