---
draft: true
sidebar_position: 47
slug: /instruments/videomancer/chinook
title: "Chinook"
image: /img/instruments/videomancer/chinook/chinook_hero_s1.png
description: "There is a luminous trembling in the late paintings of J.M.W."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import chinook_control_panel from '/img/instruments/videomancer/chinook/chinook_control_panel.png';
import chinook_source1_castle from '/img/instruments/videomancer/chinook/chinook_source1_castle.png';
import chinook_source2_fruit from '/img/instruments/videomancer/chinook/chinook_source2_fruit.png';
import chinook_source3_collage from '/img/instruments/videomancer/chinook/chinook_source3_collage.png';
import chinook_source4_pattern from '/img/instruments/videomancer/chinook/chinook_source4_pattern.png';
import chinook_source5_boy from '/img/instruments/videomancer/chinook/chinook_source5_boy.png';
import chinook_source6_berries from '/img/instruments/videomancer/chinook/chinook_source6_berries.png';
import chinook_hero_s1 from '/img/instruments/videomancer/chinook/chinook_hero_s1.png';
import chinook_hero_s2 from '/img/instruments/videomancer/chinook/chinook_hero_s2.png';
import chinook_hero_s3 from '/img/instruments/videomancer/chinook/chinook_hero_s3.png';
import chinook_hero_s4 from '/img/instruments/videomancer/chinook/chinook_hero_s4.png';
import chinook_hero_s5 from '/img/instruments/videomancer/chinook/chinook_hero_s5.png';
import chinook_hero_s6 from '/img/instruments/videomancer/chinook/chinook_hero_s6.png';
import chinook_ex1_s1 from '/img/instruments/videomancer/chinook/chinook_ex1_s1.png';
import chinook_ex1_s2 from '/img/instruments/videomancer/chinook/chinook_ex1_s2.png';
import chinook_ex1_s3 from '/img/instruments/videomancer/chinook/chinook_ex1_s3.png';
import chinook_ex1_s4 from '/img/instruments/videomancer/chinook/chinook_ex1_s4.png';
import chinook_ex1_s5 from '/img/instruments/videomancer/chinook/chinook_ex1_s5.png';
import chinook_ex1_s6 from '/img/instruments/videomancer/chinook/chinook_ex1_s6.png';
import chinook_ex2_s1 from '/img/instruments/videomancer/chinook/chinook_ex2_s1.png';
import chinook_ex2_s2 from '/img/instruments/videomancer/chinook/chinook_ex2_s2.png';
import chinook_ex2_s3 from '/img/instruments/videomancer/chinook/chinook_ex2_s3.png';
import chinook_ex2_s4 from '/img/instruments/videomancer/chinook/chinook_ex2_s4.png';
import chinook_ex2_s5 from '/img/instruments/videomancer/chinook/chinook_ex2_s5.png';
import chinook_ex2_s6 from '/img/instruments/videomancer/chinook/chinook_ex2_s6.png';
import chinook_ex3_s1 from '/img/instruments/videomancer/chinook/chinook_ex3_s1.png';
import chinook_ex3_s2 from '/img/instruments/videomancer/chinook/chinook_ex3_s2.png';
import chinook_ex3_s3 from '/img/instruments/videomancer/chinook/chinook_ex3_s3.png';
import chinook_ex3_s4 from '/img/instruments/videomancer/chinook/chinook_ex3_s4.png';
import chinook_ex3_s5 from '/img/instruments/videomancer/chinook/chinook_ex3_s5.png';
import chinook_ex3_s6 from '/img/instruments/videomancer/chinook/chinook_ex3_s6.png';

# Chinook

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: chinook_source1_castle, after: chinook_hero_s1 },
    { label: "Fruit", before: chinook_source2_fruit, after: chinook_hero_s2 },
    { label: "Collage", before: chinook_source3_collage, after: chinook_hero_s3 },
    { label: "Pattern", before: chinook_source4_pattern, after: chinook_hero_s4 },
    { label: "Boy", before: chinook_source5_boy, after: chinook_hero_s5 },
    { label: "Berries", before: chinook_source6_berries, after: chinook_hero_s6 },
  ]}
/>
*Chinook applying hash-driven thermal displacement with bottom-up gradient envelope and atmospheric haze to create Turner-esque heat shimmer.*

---

## Overview

There is a luminous trembling in the late paintings of J.M.W. Turner — a refusal to let form be still. Buildings dissolve, ships blur, the horizon itself becomes a suggestion rather than a fact. The air between the viewer and the subject is not empty but *active*, bending light through invisible gradients of heat and moisture. Chinook is an attempt to make video behave this way.

The program generates a 2D turbulence field from a Jenkins-style hash function, evaluated at block coordinates that tile the frame. Each block receives a pseudo-random signed displacement value. A configurable thermal envelope — bottom-up gradient (as heat rising from the ground), horizontal band (a concentrated thermal layer), or radial point source (outward from frame center) — modulates the displacement spatially, confining the distortion to a region of the image. The envelope-masked displacement drives luminance shimmer and subtle chromatic shifts. An atmospheric haze stage then compresses the processed signal toward mid-gray and desaturates the chrominance, simulating the way distant objects lose contrast and color through intervening atmosphere.

At gentle settings, Chinook adds the barely perceptible wavering of a hot road surface or a summer meadow. At extreme settings, the entire image fractures into blocky turbulence cells, each vibrating at its own amplitude — a digital hallucination of thermal convection.

---

## Background

### The Atmospheric Paintings of Turner

Joseph Mallord William Turner (1775–1851) spent his final decades pursuing something no painter before him had seriously attempted: depicting the *medium* through which we see, rather than the objects we see through it. Works like "Snow Storm: Steam-Boat off a Harbour's Mouth" (1842) and "Rain, Steam, and Speed — The Great Western Railway" (1844) dissolve solid matter into gradients of light, moisture, and heat. Critics of the time called them "pictures of nothing." Turner understood that atmosphere is not nothing — it is the thing that *makes* vision possible, and it has its own structure.

### What Is Thermal Refraction?

When air is heated unevenly — by sun-baked asphalt, an exhaust vent, or a campfire — layers of different temperature develop different refractive indices. Light passing through these boundaries bends, creating spatially irregular displacement of the image behind the heated zone. This is what produces the shimmering mirage above a desert road or the wavering column of air above a barbecue grill. The displacement is chaotic but spatially coherent: nearby rays bend by similar amounts. Chinook approximates this by quantizing the frame into blocks and assigning each block a pseudo-random displacement, creating spatial coherence at the block scale while remaining irregular at the frame scale.

### Hash-Based Turbulence Fields

True turbulence simulation requires solving Navier–Stokes equations at prohibitive computational cost. A common approximation in real-time graphics is the hash-based noise field: evaluate a deterministic hash function at integer lattice points, producing pseudo-random values that are repeatable for a given coordinate but appear random across space. Chinook uses a Jenkins-style mixing function that XORs and shifts the block coordinates with a per-frame seed. The result is a displacement field that tiles the screen in blocks, evolves coherently from frame to frame (via the DDS seed accumulator), and costs zero BRAM — all computation is combinatorial.

### Thermal Envelopes

Real atmospheric distortion is not uniformly distributed. Heat rises, creating a vertical gradient of turbulence intensity that peaks near the ground and fades with altitude. Chinook offers three envelope shapes to model different thermal geometries: a bottom-up gradient (the default, simulating ground-level heat haze), a horizontal band (simulating a concentrated thermal layer at a specific height), and a radial point source (simulating a plume emanating from the center of the frame). The envelope multiplies the raw hash displacement, so regions outside the envelope pass through undisturbed.

### Atmospheric Haze and Desaturation

Distant objects appear lighter, lower in contrast, and less saturated than near objects — an effect painters call *aerial perspective*. The physical cause is scattering: light passing through particulate-laden atmosphere loses directional information and gains a bias toward the ambient sky color. Chinook's haze stage approximates this by compressing each channel toward its midpoint (512 in the 10-bit domain). Luminance flattens toward mid-gray; chrominance shrinks toward neutral. The effect is proportional to the Haze parameter, allowing smooth progression from crystal-clear to deeply veiled.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ h_count (pixel), v_count (line)
│   └─ frame_seed DDS (incremented by Speed at vsync)
│
├── Stage 0: Block Coordinate Quantization ─────────────────────
│   ├─ block_x = h_count >> block_shift
│   ├─ block_y = v_count >> block_shift
│   └─ frac_x = sub-block horizontal fraction
│
├── Stage 1: Hash Mixing Function (Jenkins-style) ──────────────
│   ├─ h0 = block_x XOR (block_y << 5) XOR (block_y >> 3)
│   ├─ h1 = h0 XOR frame_seed → shift/XOR cascade
│   ├─ raw_disp = h1[9:0] - 512  (signed, centered)
│   └─ raw_disp_next = hash(block_x+1, block_y)  (for interpolation)
│
├── Stage 2: Thermal Envelope ──────────────────────────────────
│   ├─ Radial mode: Manhattan distance from center → falloff
│   ├─ Gradient mode: bottom-up ramp from env_row over env_extent
│   └─ Band mode: symmetric falloff around env_row
│
├── Stage 3: Displacement × Envelope × Depth ──────────────────
│   ├─ Optional smooth inter-block interpolation (frac_x blend)
│   └─ masked_disp = disp × envelope × depth  (scaled product)
│
├── Stage 4: Horizontal Shift + Luminance Shimmer ──────────────
│   ├─ Y: ± shimmer perturbation (masked_disp >> 2)  [if Shimmer On]
│   ├─ U: + chromatic shift (masked_disp >> 4)
│   └─ V: − chromatic shift (masked_disp >> 4)
│
├── Stage 5: Atmospheric Haze ──────────────────────────────────
│   ├─ Y: compress toward mid-gray (512)
│   ├─ U: desaturate toward neutral (512)
│   └─ V: desaturate toward neutral (512)
│
├── Stages 6–9: Interpolator (wet/dry mix per channel) ─────────
│   └─ lerp(dry, wet, Mix)  ×3 channels  (4 clocks each)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 10-stage delay pipeline (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline is purely combinatorial per pixel — zero BRAM — which means every pixel is computed independently from its hash coordinates, not read from a buffer. Because there is no line buffer, Chinook cannot perform true spatial displacement (reading a different pixel). Instead, the displacement value modulates the *current* pixel's luminance and chrominance in a way that produces a visual effect resembling spatial refraction. The shimmer perturbation is four times stronger on the Y channel (right-shifted by 2) than on U/V (right-shifted by 4), preserving the impression that luminance bends more violently than color — consistent with how thermal distortion appears in nature. The smooth inter-block interpolation mode linearly blends the hash values of adjacent horizontal blocks using the sub-block fractional position, softening the hard block boundaries into a continuous gradient of displacement.

---

## Parameter Reference

<img src={chinook_control_panel} alt="Videomancer front panel with Chinook loaded"/>
*Videomancer's front panel with Chinook active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Controls the temporal evolution rate of the turbulence field. At zero, the displacement pattern is frozen — a static texture of thermal warping. As Speed increases, the frame seed DDS accumulator advances more rapidly at each vertical sync, causing the hash field to evolve. Low values produce a slow, drifting shimmer like heat rising from warm stone; high values create a rapid, flickering distortion like the air above an open flame.

---

#### Knob 2 — Scale
| Property | Value |
|----------|-------|
| Range | 4px – 64px |
| Default | 27px |
| Suffix | px |

Selects the spatial block size from 4 to 64 pixels in 8 steps. Small blocks (4–8 px) produce fine-grained turbulence with rapid spatial variation — sharp and insect-like, reminiscent of heat shimmer seen very close to its source. Large blocks (32–64 px) produce broad, sweeping displacement zones where large regions of the image move together — slower, more monumental distortion like the wavering of a distant building seen through a column of hot exhaust.

---

#### Knob 3 — Env Pos
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 68.4% |
| Suffix | % |

Positions the thermal envelope vertically across the frame. At 0%, the envelope starts at the top of the frame. At 100%, it starts at the bottom. The meaning changes depending on the envelope shape: in Gradient mode, this sets the row where heat begins to rise upward; in Band mode, this centers the thermal band at the specified height; in Radial mode, this parameter still shifts the vertical origin, though the effect is centered around frame center by default.

---

#### Knob 4 — Env Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the vertical extent of the thermal envelope. Small values confine distortion to a narrow strip — a thin shimmer line where the thermal gradient is concentrated. Large values spread the envelope across a wide portion of the frame, allowing a broad, gradual transition between undisturbed and fully displaced regions. In Band mode, this determines the band's total width. In Radial mode, it sets the radius within which the point source has influence.

---

#### Knob 5 — Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Sets the maximum displacement amplitude. This is the master intensity control for Chinook's distortion effect. At zero, the hash field exists but produces no visible displacement — the image passes through with only haze applied. As Depth increases, the multiplicative product of hash × envelope × depth grows, producing increasingly violent spatial perturbation. At maximum, the displacement can push luminance through nearly its full range, creating aggressive thermal fracturing.

---

#### Knob 6 — Haze
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 19.6% |
| Suffix | % |

Controls the atmospheric haze intensity. At zero, the processed signal retains its full contrast and saturation — only the shimmer displacement is active. As Haze increases, luminance compresses toward mid-gray and chrominance desaturates toward neutral, simulating the scattered-light wash of aerial perspective. At maximum, the output approaches a uniform gray fog punctuated only by the strongest displacement perturbations. Haze operates *after* shimmer and displacement, so it softens the shimmer artifacts as well as the source material.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Env Shape** | Gradient | Band |
| **8 — Env Type** | Normal | Radial |
| **9 — Shimmer** | Off | On |
| **10 — BlkInterp** | Hard | Smooth |
| **11 — Bypass** | Off | On |

Switches 7–10 configure four independent aspects of the turbulence engine. Switches 7 and 8 together define the thermal envelope geometry (four combinations: gradient/normal, gradient/radial, band/normal, band/radial). Switch 9 enables or disables luminance shimmer independently of the chromatic displacement, which is always active. Switch 10 selects between hard block boundaries and smooth inter-block interpolation. Switch 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix at the end of the processing chain. At 100%, the output is fully processed — shimmer, chromatic displacement, and haze are at their set intensities. At 0%, the output is the unprocessed input. Intermediate values blend between the two. Because the mix operates on all three channels simultaneously via three parallel interpolator instances, the crossfade is perceptually smooth with no color artifacts.

---

## Guided Exercises

These exercises progress from gentle atmospheric haze through targeted thermal shimmer to full turbulent refraction. Each explores a different interaction between the envelope geometry, displacement engine, and haze.

### Exercise 1: Ground-Level Heat Haze

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: chinook_source1_castle, after: chinook_ex1_s1 },
    { label: "Fruit", before: chinook_source2_fruit, after: chinook_ex1_s2 },
    { label: "Collage", before: chinook_source3_collage, after: chinook_ex1_s3 },
    { label: "Pattern", before: chinook_source4_pattern, after: chinook_ex1_s4 },
    { label: "Boy", before: chinook_source5_boy, after: chinook_ex1_s5 },
    { label: "Berries", before: chinook_source6_berries, after: chinook_ex1_s6 },
  ]}
/>
*Ground-Level Heat Haze — simulated result across source images.*
**Source**: Footage with a visible horizon or ground plane — outdoor landscapes, cityscapes, or a static camera pointed down a road.

**Objective**: Create a naturalistic bottom-up heat shimmer that affects the lower portion of the frame while leaving the sky undisturbed.

1. **Set the envelope**: Leave Env Shape on Gradient (default). Adjust Env Pos to place the onset of shimmer near the bottom third of the frame. Set Env Size to about 50% so the distortion fades gradually upward.
2. **Introduce turbulence**: Slowly increase Depth from zero. Watch the lower portion of the image begin to waver while the upper sky remains stable.
3. **Set block scale**: Try Scale at 8 px (second step) for fine heat shimmer, then 16 px (fourth step) for broader wavering.
4. **Animate**: Increase Speed until the shimmer drifts at a natural pace — roughly 25–35%.
5. **Add haze**: Bring Haze up to 15–25% to soften the shimmer zone with a subtle desaturation, simulating aerial perspective near the ground.

**Key concepts**: Bottom-up gradient envelope models rising heat, small block sizes produce fine-grained shimmer, haze adds aerial perspective

---

### Exercise 2: Thermal Band with Radial Focus

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: chinook_source1_castle, after: chinook_ex2_s1 },
    { label: "Fruit", before: chinook_source2_fruit, after: chinook_ex2_s2 },
    { label: "Collage", before: chinook_source3_collage, after: chinook_ex2_s3 },
    { label: "Pattern", before: chinook_source4_pattern, after: chinook_ex2_s4 },
    { label: "Boy", before: chinook_source5_boy, after: chinook_ex2_s5 },
    { label: "Berries", before: chinook_source6_berries, after: chinook_ex2_s6 },
  ]}
/>
*Thermal Band with Radial Focus — simulated result across source images.*
**Source**: Footage with a central subject and visible background — a portrait, a performer on stage, or an object against a landscape.

**Objective**: Create a concentrated thermal distortion band that radiates from the center, leaving the subject partially visible through the turbulence.

1. **Switch to Band + Radial**: Set Env Shape to Band and Env Type to Radial. This creates a diamond-shaped distortion zone at frame center.
2. **Position and size**: Set Env Pos to ~50% (center) and Env Size to ~40%. The distortion should form a focused zone around the subject.
3. **Depth and scale**: Set Depth to ~50% and Scale to 16 px for medium-scale turbulence cells.
4. **Compare Hard vs Smooth**: Toggle BlkInterp between Hard and Smooth. Notice how Hard creates a tiled mosaic of displacement, while Smooth produces flowing gradients.
5. **Isolate shimmer**: Toggle Shimmer Off to see only the chromatic shift and haze. Toggle it On again to observe how luminance perturbation dominates the visual effect.

**Key concepts**: Radial mode creates point-source distortion, Band envelope confines effect to a strip, BlkInterp dramatically changes character

---

### Exercise 3: Full Atmospheric Dissolution

<BeforeAfterSlider
  sources={[
    { label: "Castle", before: chinook_source1_castle, after: chinook_ex3_s1 },
    { label: "Fruit", before: chinook_source2_fruit, after: chinook_ex3_s2 },
    { label: "Collage", before: chinook_source3_collage, after: chinook_ex3_s3 },
    { label: "Pattern", before: chinook_source4_pattern, after: chinook_ex3_s4 },
    { label: "Boy", before: chinook_source5_boy, after: chinook_ex3_s5 },
    { label: "Berries", before: chinook_source6_berries, after: chinook_ex3_s6 },
  ]}
/>
*Full Atmospheric Dissolution — simulated result across source images.*
**Source**: Any footage — especially high-contrast or richly colored material where the loss of structure is most dramatic.

**Objective**: Push Chinook to its extreme: full-frame turbulence with maximum haze, dissolving the image into a Turner-esque atmospheric abstraction.

1. **Maximum envelope**: Set Env Shape to Gradient, Env Pos to 100% (bottom), Env Size to 100% so the entire frame is in the thermal zone.
2. **Maximum displacement**: Set Depth to ~80%. The image should fracture into visibly blocky perturbation cells.
3. **Large blocks**: Set Scale to 64 px (maximum). Each distortion cell now covers a significant area of the frame.
4. **Hard edges**: Set BlkInterp to Hard for the most aggressive, tiled distortion.
5. **Full haze**: Increase Haze to ~70%. Watch the contrast and saturation drain away, leaving ghostly shapes wavering in fog.
6. **Speed sweep**: Slowly increase Speed to animate the dissolution, then freeze it at zero to examine the static turbulence pattern.
7. **Mix fade**: Use the Mix fader to bring the processed signal in and out, revealing how much information each percentage of mix recovers.

**Key concepts**: Large blocks with hard interpolation produce dramatic tiled distortion, haze compresses dynamic range toward mid-gray, combining shimmer + haze + depth creates complete atmospheric dissolution

---


## Tips

- **Turner's secret was restraint**: The most convincing heat shimmer uses low Depth (15–35%), small Scale (4–12 px), and Smooth interpolation. Real thermal distortion is subtle — only a pixel or two of apparent displacement at human viewing distances.
- **Speed controls perceived temperature**: Slow animation (~10–20%) feels like warm stone or a sun-heated highway. Fast animation (~60–80%) feels like an open flame or industrial exhaust vent.
- **Gradient is the most naturalistic mode**: Real heat shimmer rises from below. The bottom-up gradient envelope is physically correct for ground-plane heat haze. Use Band or Radial for more stylized or fantastical effects.
- **Haze and Depth are complementary**: Depth controls the violence of displacement; Haze controls how much of the resulting image you can see. Maximum Depth with maximum Haze produces ghostly abstraction — violent movement barely visible through fog.
- **Bypass + Mix for A/B evaluation**: Toggle Bypass for an instant comparison, or use the Mix fader for a progressive crossfade that reveals exactly how much each percentage of processing adds.
- **Smooth mode at large Scale values**: With 32–64 px blocks, Smooth interpolation is essential to avoid obvious grid artifacts. At small block sizes (4–8 px), Hard mode is acceptable because the blocks are already near pixel scale.
- **Shimmer Off for pure haze**: Disabling Shimmer while leaving Haze active produces a flat desaturation/contrast reduction without any spatial distortion — a simple aerial perspective filter useful for simulating fog or distance.
- **Feedback creates recursive refraction**: Routing Chinook's output back to its input produces compound distortion — each pass through the turbulence field adds another layer of displacement, building up a densely layered atmospheric texture.

---

## Glossary

| Term | Definition |
|------|------------|
| **Aerial perspective** | The visual phenomenon where distant objects appear lighter, less saturated, and lower in contrast due to atmospheric light scattering. |
| **BRAM** | Block RAM; dedicated memory blocks within an FPGA used for look-up tables, line buffers, and data storage. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator that increments by a fixed frequency word each clock cycle. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that implements the video processing pipeline in hardware. |
| **Hash function** | A deterministic function that maps input data to a fixed-size pseudo-random output, used here to generate a turbulence displacement field from block coordinates. |
| **Jenkins hash** | A family of non-cryptographic hash functions using XOR and bit-shift cascades, employed by Chinook for fast pseudo-random displacement generation. |
| **Manhattan distance** | A distance metric computed as |dx| + |dy|, used in the radial envelope mode to create diamond-shaped falloff from the frame center. |
| **Navier–Stokes equations** | The fundamental partial differential equations governing fluid dynamics, whose full solution is computationally prohibitive for real-time processing. |
| **Refractive index** | A measure of how much a medium bends light passing through it; variations in air temperature create the refractive-index gradients that produce thermal shimmer. |
| **Thermal envelope** | A spatial mask that modulates displacement strength across the frame, confining turbulence to a specific region such as a ground-level gradient or radial plume. |
| **YUV** | A color space that separates luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |

---
