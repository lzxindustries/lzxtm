---
draft: true
sidebar_position: 78
slug: /instruments/videomancer/defocus
title: "Defocus"
image: /img/instruments/videomancer/defocus/defocus_hero_s1.png
description: "Every camera lens has a focal plane — a thin slice of space where objects are rendered sharp."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import defocus_control_panel from '/img/instruments/videomancer/defocus/defocus_control_panel.png';
import defocus_source1_dog from '/img/instruments/videomancer/defocus/defocus_source1_dog.png';
import defocus_source2_cat from '/img/instruments/videomancer/defocus/defocus_source2_cat.png';
import defocus_source3_elephant from '/img/instruments/videomancer/defocus/defocus_source3_elephant.png';
import defocus_source4_pattern from '/img/instruments/videomancer/defocus/defocus_source4_pattern.png';
import defocus_source5_man from '/img/instruments/videomancer/defocus/defocus_source5_man.png';
import defocus_source6_knit from '/img/instruments/videomancer/defocus/defocus_source6_knit.png';
import defocus_hero_s1 from '/img/instruments/videomancer/defocus/defocus_hero_s1.png';
import defocus_hero_s2 from '/img/instruments/videomancer/defocus/defocus_hero_s2.png';
import defocus_hero_s3 from '/img/instruments/videomancer/defocus/defocus_hero_s3.png';
import defocus_hero_s4 from '/img/instruments/videomancer/defocus/defocus_hero_s4.png';
import defocus_hero_s5 from '/img/instruments/videomancer/defocus/defocus_hero_s5.png';
import defocus_hero_s6 from '/img/instruments/videomancer/defocus/defocus_hero_s6.png';
import defocus_ex1_s1 from '/img/instruments/videomancer/defocus/defocus_ex1_s1.png';
import defocus_ex1_s2 from '/img/instruments/videomancer/defocus/defocus_ex1_s2.png';
import defocus_ex1_s3 from '/img/instruments/videomancer/defocus/defocus_ex1_s3.png';
import defocus_ex1_s4 from '/img/instruments/videomancer/defocus/defocus_ex1_s4.png';
import defocus_ex1_s5 from '/img/instruments/videomancer/defocus/defocus_ex1_s5.png';
import defocus_ex1_s6 from '/img/instruments/videomancer/defocus/defocus_ex1_s6.png';
import defocus_ex2_s1 from '/img/instruments/videomancer/defocus/defocus_ex2_s1.png';
import defocus_ex2_s2 from '/img/instruments/videomancer/defocus/defocus_ex2_s2.png';
import defocus_ex2_s3 from '/img/instruments/videomancer/defocus/defocus_ex2_s3.png';
import defocus_ex2_s4 from '/img/instruments/videomancer/defocus/defocus_ex2_s4.png';
import defocus_ex2_s5 from '/img/instruments/videomancer/defocus/defocus_ex2_s5.png';
import defocus_ex2_s6 from '/img/instruments/videomancer/defocus/defocus_ex2_s6.png';
import defocus_ex3_s1 from '/img/instruments/videomancer/defocus/defocus_ex3_s1.png';
import defocus_ex3_s2 from '/img/instruments/videomancer/defocus/defocus_ex3_s2.png';
import defocus_ex3_s3 from '/img/instruments/videomancer/defocus/defocus_ex3_s3.png';
import defocus_ex3_s4 from '/img/instruments/videomancer/defocus/defocus_ex3_s4.png';
import defocus_ex3_s5 from '/img/instruments/videomancer/defocus/defocus_ex3_s5.png';
import defocus_ex3_s6 from '/img/instruments/videomancer/defocus/defocus_ex3_s6.png';

# Defocus

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: defocus_source1_dog, after: defocus_hero_s1 },
    { label: "Cat", before: defocus_source2_cat, after: defocus_hero_s2 },
    { label: "Elephant", before: defocus_source3_elephant, after: defocus_hero_s3 },
    { label: "Pattern", before: defocus_source4_pattern, after: defocus_hero_s4 },
    { label: "Man", before: defocus_source5_man, after: defocus_hero_s5 },
    { label: "Knit", before: defocus_source6_knit, after: defocus_hero_s6 },
  ]}
/>
*Defocus dissolving a busy scene into soft luminous pools of color with glow highlights bleeding across the frame.*

---

## Overview

Every camera lens has a focal plane — a thin slice of space where objects are rendered sharp. Move outside that plane and the image softens, edges dissolve, and point light sources bloom into discs. This is defocus, and it is one of the most fundamental optical phenomena in image-making. Videomancer's Defocus program brings this behavior into the electronic domain with a 32-step blur engine, six line buffers for vertical averaging, a glow extraction stage, and an auto-animation oscillator that racks focus without touching a knob.

The name is deliberately clinical. Where "blur" suggests an accident, "defocus" implies intent — a deliberate withdrawal of sharpness to reshape the image. At low settings, Defocus produces the gentle softening of a diffusion filter stretched across a lens. At moderate settings, it creates the dreamy haze of a pulled-focus transition. At high settings with glow enabled, it transforms video into luminous abstract fields where bright areas bleed outward and consume the frame.

The engine operates in YUV space, treating luminance and chrominance independently. Horizontal blur uses a sliding-window running-sum box filter with power-of-two window widths up to 64 pixels. Vertical blur averages consecutive scanlines through dual-bank line buffers. The H/V Balance control crossfades between horizontal-only and combined blur, letting you create directional softening — horizontal streaks, vertical smears, or uniform fields.

---

## Quick Start

1. **Diffusion filter trick**: Set a high Blur Amt (step 20+) and pull Mix back to 30–40%. The sharp original shows through a soft overlay — exactly how a physical diffusion filter works on a camera lens.
2. **Anamorphic streaks**: Turn V-Blur Off and set H/V Bal to 0% for pure horizontal smearing. Combined with moderate Glow, this produces the characteristic streak flares of anamorphic cinema lenses.
3. **Glow threshold is key**: The difference between subtle highlight bloom and a washed-out white image is entirely in GlowThr. Start high (60%+) and lower cautiously.

---

## Background

### Optical Defocus vs. Digital Blur

In an optical system, defocus occurs when light rays from a point in the scene converge before or after the sensor plane, creating a circle of confusion. The shape and size of this circle are determined by the aperture geometry — circular apertures produce round bokeh, hexagonal apertures produce hexagonal highlights. The result is inherently two-dimensional: every point spreads into a disc whose diameter depends on its distance from the focal plane.

Digital blur operates differently. Rather than simulating the physics of light convergence, it applies a mathematical kernel to the pixel grid. Box filters average rectangular neighborhoods. Gaussian filters weight the neighborhood with a bell curve. Triangle filters apply a linearly decaying weight. Defocus implements a box filter with an optional triangle morph, applied separately in the horizontal and vertical directions. This separable approach is computationally efficient — a 2D blur of radius R costs O(R²) per pixel, but two 1D passes cost O(2R). The visual result closely approximates a true 2D filter for most video content.

### Box, Gaussian, and Triangle Kernels

A **box kernel** assigns equal weight to every pixel within the window. The result is a flat average — efficient to compute but prone to ringing artifacts on high-contrast edges, because the transition from "included" to "excluded" pixels is abrupt. A **Gaussian kernel** weights pixels with a bell curve centered on the target pixel, producing smoother results but requiring more multiplications. A **triangle kernel** falls halfway between: weights decrease linearly from the center to the edges. Mathematically, a triangle kernel equals a box kernel convolved with itself — so applying a box filter twice produces a triangle response.

Defocus's Blur Shape control (BlrShpe) crossfades between the single-pass box filter and a double-pass triangle approximation. At 0% the filter is pure box; at 100% it is fully triangular. Intermediate positions blend the two, letting you dial in the exact softness character you want.

### Line-Buffer Vertical Blur

Horizontal blur is straightforward — the shift register holds 64 pixels of the current scanline, and a running sum yields the average. Vertical blur is harder because it requires data from adjacent scanlines, which arrive one at a time in a raster-scanned signal. The solution is **line buffers**: dedicated memory blocks that store entire scanlines so they can be recalled when the next line arrives.

Defocus uses six line buffers arranged in two banks (A and B) of three channels each. Bank A stores the previous line; Bank B stores the line before that. When a new pixel arrives, the vertical blur engine reads the corresponding pixel from Banks A and B, sums all three lines, and divides by three (via the integer approximation ×341 >> 10). The result is a 3-line running average. With the V Cascade toggle set to Double, the 3-line average is fed through a second set of buffers in the same ping-pong fashion, extending the effective window and producing a softer vertical blur.

### Glow and Bloom

In film and television, bloom occurs when bright areas overwhelm the sensor or film emulsion, causing light to spread into surrounding regions. The effect is physically caused by internal reflections in the lens assembly and scattering in the sensor. Digitally, glow is simulated by extracting the bright portions of an already-blurred image and additively blending them back.

Defocus's glow engine compares each pixel's blurred luminance against a threshold (GlowThr). Pixels below the threshold pass through unchanged. Pixels above the threshold receive an additive boost proportional to both their luminance and the Glow Level (Glow Lv) parameter. The result is clamped to the 10-bit maximum (1023). Because the glow operates on the *blurred* signal, highlights spread as soft halos rather than hard-edged overlays — and higher blur settings produce wider, more diffuse glow.

### Auto-Animation and Focus Racking

A rack focus is a cinematographic technique where the camera operator smoothly shifts the focal plane from one subject to another within a single shot. The viewer's attention follows the sharpness. Defocus's Auto-Animation mode replicates this effect electronically by oscillating the blur amount with a triangle-wave LFO synchronized to the vertical sync signal.

The animation counter increments once per field. At the Slow speed, the phase advances by 128 per field; at Fast, it advances by 512. The upper bit of the 16-bit phase register selects the ramp direction: when low, the blur amount ramps up; when high, it ramps back down. The resulting triangle wave sweeps the effective blur step between 0 and 31, producing a continuous rack-focus cycle. The base Blur Amount knob has no effect while Auto-Animation is active — the oscillator takes full control.


---

## Signal Flow

Y / U / V Channels → Sync Signals → Animation Oscillator → Bypass

```
Input Video (YUV 4:4:4 30-bit)
│
├── Y / U / V Channels ────────────────────────────────────────
│   │
│   ├─ 1. Blur Step Selector       (pot 1 quantized to 32 steps, or auto-anim)
│   ├─ 2. Horizontal Box Filter    (64-deep shift register, running sum,
│   │                                power-of-2 window: 1/2/4/8/16/32/64 px)
│   ├─ 3. Blur Shape Morph         (crossfade box → triangle via 2nd pass)
│   ├─ 4. Line Buffers             (6× video_line_buffer: bank A + bank B)
│   ├─ 5. Vertical Blur            (3-line average × 341 >> 10, optional cascade)
│   ├─ 6. H/V Balance              (crossfade H-only ↔ H+V combined)
│   ├─ 7. Chroma Blur              (additional U/V filtering, independent)
│   ├─ 8. Glow Engine              (threshold + additive gain on Y, clamp 1023)
│   └─ 9. Wet/Dry Mix              (interpolator_u: original ↔ processed)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delayed pipeline (10 clocks): hsync_n, vsync_n, field_n
│
├── Animation Oscillator ──────────────────────────────────────
│   └─ Triangle LFO on vsync: phase +128 (slow) or +512 (fast)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Toggle 11: route delayed original directly to output
```

The horizontal filter is the heart of the engine. A 64-deep shift register per channel implements a sliding-window running sum: each clock, the entering pixel is added and the exiting pixel (determined by the window width) is subtracted. Division is a right-shift by the base-2 logarithm of the window width, making the entire filter zero-multiplier. The vertical blur stage is architecturally separate — it reads from line buffers written by the horizontal stage, so horizontal and vertical processing are not interchangeable in order.

Glow operates exclusively on the Y channel and only on the already-blurred signal, which means higher blur settings produce wider, more diffuse glow haloes. The glow threshold sets a hard floor below which no brightening occurs. The wet/dry mix is the final stage before the bypass mux, applied equally to Y, U, and V via three independent interpolator_u instances.

---

## Parameter Reference

<img src={defocus_control_panel} alt="Videomancer front panel with Defocus loaded"/>
*Videomancer's front panel with Defocus active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Blur Amt
| Property | Value |
|----------|-------|
| Range | 0 – 31 |
| Default | 0 |

Selects the blur radius in 32 discrete steps. Steps 0–3 map to a window width of 1 pixel (no blur). Steps 4–7 map to 2 pixels, 8–11 to 4, 12–15 to 8, 16–19 to 16, 20–23 to 32, and 24–31 to the maximum of 64 pixels. Because the window widths are powers of two, the division stage is a simple binary right-shift — no multiplier needed. At step 0 the image passes through sharp; at step 31 each pixel is the average of 64 horizontal neighbors, producing a heavy motion-blur-like smear. This control has no effect when Auto-Animation is active.

---

#### Knob 2 — BlrShpe
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Morphs the filter kernel between a box shape and a triangle shape. At 0% the filter is a single-pass box average — every pixel within the window contributes equally. At 100% a second box pass is applied to the already-filtered signal, yielding a triangle (tent) response that weights center pixels more heavily than edge pixels. Intermediate positions crossfade between the two, letting you tune the softness character from flat and mechanical to smooth and organic. The difference is most visible at moderate blur amounts where individual kernel artifacts are perceptible.

---

#### Knob 3 — H/V Bal
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Crossfades between horizontal-only blur and combined horizontal-plus-vertical blur. At 0% only the horizontal box filter contributes to the output; the vertical line-buffer stage is ignored. At 50% (center detent) horizontal and vertical contributions are equal, producing a symmetrical soft focus. At 100% the output is purely the vertical-blur path. This control lets you create directional effects — anamorphic streak-style softening at the horizontal extreme, scan-line smearing at the vertical extreme, or uniform defocus at center.

---

#### Knob 4 — ChrBlur
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Applies additional blur exclusively to the U and V chrominance channels, leaving Y untouched. This produces a chroma-only softening where luminance detail remains intact but colors bleed and merge. At low values, chroma blur subtly desaturates fine color detail — similar to what happens in broadcast chroma subsampling. At high values, large color fields wash across the frame while edges defined by brightness remain sharp, creating a painterly separation of form and color.

---

#### Knob 5 — Glow Lv
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

At 0% the glow stage is disabled and the blurred signal passes through unchanged. As you increase the level, pixels whose blurred luminance exceeds the Glow Threshold receive an additive brightness boost proportional to both their luminance and this control's value. At high settings, bright highlights bloom dramatically — white areas clamp to maximum and expand into surrounding mid-tones. The glow operates on the already-blurred signal, so higher Blur Amount settings produce wider and softer halos. Internally, controls the intensity of the glow engine's additive overlay.

---

#### Knob 6 — GlowThr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the luminance floor for glow extraction. Pixels whose blurred Y value is below this threshold receive no glow boost and pass through unchanged. Pixels above the threshold enter the glow computation. At high threshold values (toward 100%), only the brightest highlights receive glow — specular reflections, light sources, bright text. At low threshold values, nearly the entire image receives glow boost, producing a flat wash of brightness. The default position (approximately 60%) catches most highlights while leaving mid-tones and shadows untouched.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — V-Blur** | Off | On |
| **8 — V Cascde** | Single | Double |
| **9 — AutoAnim** | Off | On |
| **10 — AnimSpd** | Slow | Fast |
| **11 — Bypass** | Off | On |

The five toggles control three independent subsystems: vertical blur configuration (Switches 7–8), animation (Switches 9–10), and bypass (Switch 11). V-Blur and V Cascade work together — V-Blur must be On for V Cascade to have any effect. Similarly, AnimSpd only matters when AutoAnim is On. Bypass overrides everything downstream of the sync delay, routing the time-aligned original signal directly to output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade at the output. At 0% (fader fully down), the output is entirely the original dry signal — equivalent to bypass but via the interpolator rather than the mux. At 100% (fader fully up, default), the output is entirely the processed wet signal including all blur and glow. Intermediate positions blend the two, which is useful for dialing in subtle diffusion: you can set a strong blur amount and then pull the fader back to mix in just a hint of softness over the sharp original.





---

## Guided Exercises

These three exercises progress from basic soft focus through vertical blur and glow, culminating in animated focus racking. Each builds on the previous, gradually engaging more of the processing chain.

### Exercise 1: Soft Focus Diffusion

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: defocus_source1_dog, after: defocus_ex1_s1 },
    { label: "Cat", before: defocus_source2_cat, after: defocus_ex1_s2 },
    { label: "Elephant", before: defocus_source3_elephant, after: defocus_ex1_s3 },
    { label: "Pattern", before: defocus_source4_pattern, after: defocus_ex1_s4 },
    { label: "Man", before: defocus_source5_man, after: defocus_ex1_s5 },
    { label: "Knit", before: defocus_source6_knit, after: defocus_ex1_s6 },
  ]}
/>
*Soft Focus Diffusion — simulated result across source images.*
**Source**: A live camera feed with a well-lit subject — portraits or detailed textures work best.

**What You'll Create**: Learn how horizontal blur amount and blur shape interact to create classic diffusion-filter effects.

1. **Minimal softening**: Set Blur Amt to step 4 (first detectable blur — window width 2). The image softens almost imperceptibly.
2. **Moderate diffusion**: Increase to step 12 (window width 8). Fine detail dissolves while large shapes remain recognizable.
3. **Heavy blur**: Push to step 24 (window width 64). The image becomes broad fields of color.
4. **Shape comparison**: With Blur Amt at step 12, sweep BlrShpe from 0% to 100%. Watch the softness character change from flat and mechanical (box) to rounded and organic (triangle).
5. **Mix back**: Reduce Mix to approximately 50%. The sharp original bleeds through the blur, creating the classic "diffusion filter" look where detail is present but wrapped in softness.

**Key concepts**: Power-of-two window widths create discrete blur jumps, box vs triangle kernels produce different softness characters, wet/dry mix allows partial diffusion

---

### Exercise 2: Directional Blur with Glow

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: defocus_source1_dog, after: defocus_ex2_s1 },
    { label: "Cat", before: defocus_source2_cat, after: defocus_ex2_s2 },
    { label: "Elephant", before: defocus_source3_elephant, after: defocus_ex2_s3 },
    { label: "Pattern", before: defocus_source4_pattern, after: defocus_ex2_s4 },
    { label: "Man", before: defocus_source5_man, after: defocus_ex2_s5 },
    { label: "Knit", before: defocus_source6_knit, after: defocus_ex2_s6 },
  ]}
/>
*Directional Blur with Glow — simulated result across source images.*
**Source**: Footage with bright highlights against a darker background — candles, stage lighting, or reflections on water.

**What You'll Create**: Explore vertical blur, H/V balance for directional effects, and glow extraction from highlights.

1. **Prepare**: Set Blur Amt to step 16 (window width 16) with BlrShpe at 0%.
2. **Enable vertical**: Turn V-Blur On. The image softens vertically as well as horizontally.
3. **Horizontal streak**: Set H/V Bal to about 20%. The blur is mostly horizontal — highlights smear into anamorphic streaks.
4. **Vertical smear**: Set H/V Bal to about 80%. Now the softening is predominantly vertical — scan-line averaging dominates.
5. **Add glow**: Increase Glow Lv to about 60% while keeping GlowThr at the default 60%. Bright highlights bloom outward, adding luminous halos.
6. **Lower threshold**: Pull GlowThr down to about 30%. Mid-tones now receive glow, and the entire image takes on a dreamy bright cast.
7. **Cascade**: Toggle V Cascde to Double. The vertical blur deepens, and glow haloes extend further vertically.

**Key concepts**: H/V balance creates directional softening, glow threshold selects which brightness range blooms, cascade doubles vertical blur depth

---

### Exercise 3: Animated Focus Rack

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: defocus_source1_dog, after: defocus_ex3_s1 },
    { label: "Cat", before: defocus_source2_cat, after: defocus_ex3_s2 },
    { label: "Elephant", before: defocus_source3_elephant, after: defocus_ex3_s3 },
    { label: "Pattern", before: defocus_source4_pattern, after: defocus_ex3_s4 },
    { label: "Man", before: defocus_source5_man, after: defocus_ex3_s5 },
    { label: "Knit", before: defocus_source6_knit, after: defocus_ex3_s6 },
  ]}
/>
*Animated Focus Rack — simulated result across source images.*
**Source**: A scene with multiple subjects at different visual distances — a foreground object and a background environment.

**What You'll Create**: Use auto-animation to create a continuous rack-focus effect and combine it with glow for cinematic atmosphere.

1. **Prepare**: Set Blur Amt to any position (it will be overridden). Enable V-Blur On, V Cascde Single. Set H/V Bal to 50% for uniform defocus.
2. **Engage animation**: Turn AutoAnim On. The blur amount begins sweeping from sharp to maximum and back.
3. **Speed comparison**: Toggle AnimSpd between Slow and Fast. Slow creates a languid, meditative focus pull; Fast creates an urgent, rhythmic pulsation.
4. **Add glow**: Set Glow Lv to about 40% and GlowThr to about 50%. As the blur sweeps through its cycle, glow appears during the blurred phases and recedes during the sharp phases.
5. **Triangle shape**: Set BlrShpe to 100%. The softening becomes rounder during the blur peaks.
6. **Chroma separation**: Increase ChrBlur to about 60%. Colors lag behind luminance during the focus rack, creating a subtle chromatic aberration effect.
7. **Partial mix**: Pull Mix to about 70%. The sharp original anchors the detail while the animated blur washes over it.

**Key concepts**: Triangle-wave LFO drives blur amount synchronized to vertical sync, glow intensity varies with blur depth, chroma blur adds chromatic aberration character

---


## Tips

- **Cascade for depth**: Double cascade nearly doubles the vertical blur radius. Use it when vertical softening looks too subtle in single mode.
- **Chroma blur for vintage look**: Increasing ChrBlur while leaving Y blur moderate simulates the behavior of older lens systems where color registration was less precise than luminance resolution.
- **Animation as performance tool**: AutoAnim creates a rhythmic focus cycle that can be synchronized to music or other visual rhythms. Slow mode suits ambient material; Fast mode suits percussive content.
- **Bypass for comparison**: Toggle Switch 11 for instant A/B. The sync delay pipeline ensures no horizontal shift between bypassed and processed output.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bokeh** | The aesthetic quality of the blur produced by a lens in out-of-focus areas, often characterized by the shape of highlights. |
| **Box Filter** | A spatial averaging kernel where every pixel within the window contributes equally; also called a moving-average filter. |
| **Cascade** | Applying the same filter operation multiple times in series to increase its effective width or order. |
| **Circle of Confusion** | The disc-shaped blur pattern produced by a single point of light when a lens is defocused. |
| **Glow** | An additive brightness effect applied to pixels above a luminance threshold, simulating optical bloom. |
| **LFO** | Low-Frequency Oscillator; a periodic signal used for animation or modulation, here a triangle wave driving blur amount. |
| **Line Buffer** | A scanline-length memory that stores pixel data from a previous line for vertical processing. |
| **Rack Focus** | A cinematographic technique of smoothly shifting the focal plane during a shot to redirect viewer attention. |
| **Running Sum** | An accumulator that adds entering pixels and subtracts exiting pixels to maintain a sliding-window total. |
| **Shift Register** | A chain of flip-flops that delays a signal by a fixed number of clock cycles; here used as a 64-deep pixel delay. |
| **Triangle Filter** | A spatial kernel with linearly decaying weights; equivalent to two successive box filter passes. |

---
