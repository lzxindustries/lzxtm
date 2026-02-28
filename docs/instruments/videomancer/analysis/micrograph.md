---
draft: true
sidebar_position: 166
slug: /instruments/videomancer/micrograph
title: "Micrograph"
image: /img/instruments/videomancer/micrograph/micrograph_hero.png
description: "Program guide for Micrograph, a Videomancer analysis program for the LZX video synthesizer."
---

import micrograph_before_after from '/img/instruments/videomancer/micrograph/micrograph_before_after.png';
import micrograph_control_panel from '/img/instruments/videomancer/micrograph/micrograph_control_panel.png';
import micrograph_exercise1_result from '/img/instruments/videomancer/micrograph/micrograph_exercise1_result.png';
import micrograph_exercise2_result from '/img/instruments/videomancer/micrograph/micrograph_exercise2_result.png';
import micrograph_exercise3_result from '/img/instruments/videomancer/micrograph/micrograph_exercise3_result.png';
import micrograph_hero from '/img/instruments/videomancer/micrograph/micrograph_hero.png';
import micrograph_source1_grayscale_ramp_h_1920x1080 from '/img/instruments/videomancer/micrograph/micrograph_source1_grayscale_ramp_h_1920x1080.png';
import micrograph_source2_grayscale_ramp_v_1920x1080 from '/img/instruments/videomancer/micrograph/micrograph_source2_grayscale_ramp_v_1920x1080.png';
import micrograph_source3_step_wedge_21level_512 from '/img/instruments/videomancer/micrograph/micrograph_source3_step_wedge_21level_512.png';

# Micrograph

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={micrograph_hero} alt="Micrograph hero image"/>
*Micrograph applying histological staining and reticle overlay to transform video into a calibrated microscope specimen view.*
<img src={micrograph_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Micrograph applied.*

---

## Overview

Every laboratory microscope presents the world through a particular frame — a circular viewport, a calibrated grid, a stained slice of tissue lit from below. Micrograph brings that frame to video. It treats the incoming signal as a specimen on a glass slide and wraps it in the visual language of optical microscopy: measurement reticles, false-color staining, contrast enhancement, circular vignette, and dark-field illumination.

The name comes from the scientific photograph taken through a microscope eyepiece. The program's controls correspond to real laboratory operations — selecting a stain chemistry, choosing a reticle pattern, switching between bright-field and dark-field illumination, adjusting the condenser aperture (vignette), and tuning the substage lamp (brightness). The result is a convincing scientific-instrument aesthetic that can range from subtle grid overlay to full histological false-color rendering.

At conservative settings Micrograph simply overlays a fine measurement grid on the video. At extreme settings it transforms footage into alien tissue cultures — purple-stained cellular landscapes viewed through a dark-field eyepiece with heavy contrast and deep vignetting.

---

## Background

### What Is a Reticle?

A reticle is a pattern of lines inscribed on a glass disc placed at the focal plane of a microscope eyepiece. It provides a fixed reference for measurement and spatial orientation. Micrograph implements four reticle modes: a grid of evenly spaced horizontal and vertical lines, a crosshair centered on the frame, a scale bar with tick marks at grid intervals along the crosshair, and a blank mode with no overlay. The grid spacing is continuously variable from 8 to 64 pixels per cell, simulating different objective magnifications.

### What Is Histological Staining?

In histology, thin tissue sections are chemically treated with dyes that bind selectively to different cellular components. **Hematoxylin and Eosin (H&E)** is the most widely used combination — hematoxylin stains cell nuclei blue-purple while eosin stains cytoplasm and connective tissue pink. **Periodic Acid–Schiff (PAS)** produces a magenta color in carbohydrate-rich structures. **Gram staining** differentiates bacteria by cell wall composition, producing violet or red-pink results. Micrograph maps these color palettes onto the video's chrominance channels, with the Stain knob controlling dye concentration.

### What Is Dark-Field Microscopy?

In bright-field microscopy the specimen is illuminated from below and appears dark against a bright background. Dark-field microscopy reverses this: the illumination is angled so that only light scattered by the specimen reaches the objective. Unstained transparent structures that are invisible in bright field become brilliantly lit against a black background. Micrograph simulates this by inverting the luminance channel so that bright areas become dark and vice versa.

### What Is Vignetting in an Eyepiece?

When you look through a microscope eyepiece, the circular aperture of the optical system naturally darkens the edges of the field of view. This vignette is an inherent property of the cylindrical optical path. Micrograph recreates this effect using Manhattan distance from the frame center — pixels beyond the threshold distance are progressively darkened by right-shifting, creating a soft circular falloff that frames the specimen.

### What Is Contrast Enhancement?

Microscope substage condensers and illumination adjustments are used to enhance visibility of fine specimen structures. Micrograph implements digital contrast enhancement by shifting pixel values away from mid-gray (512) using bit-shift multiplication — 1×, 2×, 4×, or 8× gain. This emphasizes subtle tonal differences in the specimen, making faint structures visible at the cost of compressing the dynamic range.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   └─ video_timing_generator → h_count, v_count
│
├── Stage 1: Input + Position ──────────────────────────────────
│   ├─ Register Y, U, V
│   ├─ Grid spacing selection (8/16/32/64 from pot)
│   ├─ Grid cell position (x, y modulo grid size)
│   └─ Manhattan distance from center (for vignette)
│
├── Stage 2: Grid + Reticle ────────────────────────────────────
│   ├─ Grid line detection (cell boundary = 0)
│   ├─ Crosshair detection (center ±2 pixels)
│   ├─ Scale bar detection (crosshair + grid ticks)
│   └─ Reticle mode mux (Grid / Cross / Scale / Off)
│
├── Stage 3: Stain + Contrast ─────────────────────────────────
│   ├─ Contrast: Y centered at 512, shift by 0..3 bits
│   ├─ Stain color: U/V offset by stain type × strength
│   ├─ Dark field: Y inversion (1023 − Y)
│   └─ Reticle overlay: force Y to 100/900, U/V to 512
│
├── Stage 4: Vignette + Output ─────────────────────────────────
│   ├─ Vignette: Manhattan dist > threshold → darken
│   ├─ Brightness offset (centered at 512)
│   ├─ Invert toggle (1023 − Y)
│   └─ Output Y, U, V
│
├── Interpolator (4 clocks) ────────────────────────────────────
│   └─ wet/dry mix per channel (Y, U, V)
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ hsync, vsync, field delayed to match pipeline
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed or delayed original
```

The program's spatial awareness comes from the video_timing_generator, which supplies pixel and line counters. These counters drive two parallel calculations: the grid cell position (for reticle rendering) and the distance from frame center (for vignette). The reticle rendering in Stage 2 determines *where* to draw overlay lines but does not modify pixel data — that happens in Stage 3 where reticle pixels force Y to a contrasting value and chrominance to neutral gray. Dark-field inversion also occurs in Stage 3, before the reticle overlay, so reticle lines always appear bright on a dark-field background and dark on a bright-field background.

---

## Parameter Reference

<img src={micrograph_control_panel} alt="Videomancer front panel with Micrograph loaded"/>
*Videomancer's front panel with Micrograph active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Grid Sz
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spacing of the measurement grid. The pot value is divided into four discrete zones: below 25% selects 8-pixel cells (fine grid), 25–50% selects 16-pixel cells, 50–75% selects 32-pixel cells, and above 75% selects 64-pixel cells (coarse grid). Smaller cells simulate higher magnification objectives where more measurement divisions are visible. The grid spacing also affects the scale bar tick marks in Scale reticle mode.

---

#### Knob 2 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the contrast enhancement applied to the specimen image. The top two bits of the register select the gain factor: 1× (unity), 2×, 4×, or 8× multiplication of the deviation from mid-gray. At low settings the image retains its natural tonal range. At high settings fine details are amplified but highlights and shadows clip aggressively. This mirrors the real microscopy practice of adjusting condenser aperture and lamp intensity to reveal faint structures.

---

#### Knob 3 — Stain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the intensity of the histological stain applied to the chrominance channels. The register value is right-shifted by 2 to produce a 0–255 strength value that offsets U and V according to the selected stain type. At zero the original color is preserved. As the knob increases, the false-color stain progressively overwhelms the native chrominance. The effect is only visible when a stain type other than None is selected via the toggle.

---

#### Knob 4 — Focus
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

This control is labeled Focus in the TOML but is not referenced by the VHDL processing pipeline. The register is read but never used in any computation. Adjusting this knob has no effect on the output. It is reserved for a future edge-sharpening stage that has not yet been implemented.

---

#### Knob 5 — Vignette
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the radius of the circular vignette that simulates the microscope eyepiece aperture. The register value sets a Manhattan distance threshold from the frame center (pixel 640, line 360). Pixels within the threshold are unaffected. Pixels beyond it are progressively darkened by right-shifting — the further past the threshold, the more the brightness is reduced. Low values create a tight circular viewport; high values open the aperture to nearly full frame. At maximum the vignette disappears entirely.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls a brightness offset applied after vignetting. The register is centered at 512 — values below 512 darken the image, values above brighten it. This simulates the substage lamp intensity on a real microscope. The offset is additive and applied uniformly across the frame, including both specimen and reticle areas.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Stain** | None | H&E |
| **8 — Reticle** | Grid | Cross |
| **9 — Field** | Bright | Dark |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches use a non-standard packing arrangement in register 6. Stain Type and Reticle Mode each consume two bits, pushing the remaining three boolean toggles (Field, Invert, Bypass) to bits 4, 5, and 6 respectively. The Bypass toggle occupies bit 6, outside the standard 5-bit range. Stain Type and Reticle Mode together define the visual presentation of the microscope simulation — the chemical treatment and measurement overlay.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed microscope output and the original delayed input. At 100% the full microscope effect is applied. At 0% the original signal passes through unchanged. Intermediate values blend the two, which can create a ghostly overlay where the reticle grid and stain color are partially visible over the original image — useful for subtle scientific annotation without overwhelming the source material.

---

## Guided Exercises

These three exercises explore Micrograph's capabilities from basic grid overlay through full histological simulation. Each builds on the previous, progressively engaging more of the microscope's optical systems.

### Exercise 1: Measurement Grid Overlay

<img src={micrograph_exercise1_result} alt="Measurement Grid Overlay result"/>
*Measurement Grid Overlay — simulated result across source images.*
**Source**: A camera feed of detailed subject matter — macro photography of textures, circuits, or natural patterns.

**Objective**: Learn how the reticle modes and grid spacing interact to create calibrated overlays.

1. **Basic grid**: Set Grid Sz to 50% (32-pixel cells). Select Grid reticle. A regular measurement grid appears over the video.
2. **Fine grid**: Lower Grid Sz below 25%. The grid becomes very fine — 8-pixel cells create a dense mesh like a hemocytometer counting chamber.
3. **Crosshair**: Switch Reticle to Cross. The grid disappears, replaced by centered crosshairs.
4. **Scale bar**: Switch to Scale. The crosshair gains tick marks at grid intervals — a calibrated ruler overlay.
5. **Grid spacing interaction**: Sweep Grid Sz while in Scale mode. Watch the tick spacing change from fine to coarse, simulating different objective magnifications.

**Key concepts**: Reticle modes are mutually exclusive overlay patterns, grid spacing is discretized to 8/16/32/64 pixels, scale ticks follow grid spacing

---

### Exercise 2: Histological Staining

<img src={micrograph_exercise2_result} alt="Histological Staining result"/>
*Histological Staining — simulated result across source images.*
**Source**: Footage of organic textures — leaves, skin, food surfaces, or any material with fine tonal detail.

**Objective**: Explore the false-color staining modes and their interaction with contrast enhancement.

1. **Prepare**: Set Vignette to ~50% for a classic circular viewport. Select Grid reticle with 32-pixel spacing.
2. **H&E stain**: Switch Stain type to H&E. Slowly increase the Stain knob. Watch the image take on a pink-purple histological tint.
3. **Contrast boost**: Increase Contrast to ~60%. Fine structures in the specimen become more visible as mid-tones are pushed apart.
4. **PAS stain**: Switch to PAS. The tint shifts to a deeper magenta — notice U remains neutral while V carries the color.
5. **Gram stain**: Switch to Gram. The tint shifts to blue-violet. Compare the three stain chemistries at the same intensity.
6. **Dark field**: Toggle Field to Dark. The specimen inverts dramatically — bright structures glow against black. Reticle lines automatically become bright.

**Key concepts**: Each stain type maps to specific U/V offsets matching real histological dye chemistry, contrast enhancement is multiplicative bit-shift gain, dark field inverts before stain application

---

### Exercise 3: Full Microscope Simulation

<img src={micrograph_exercise3_result} alt="Full Microscope Simulation result"/>
*Full Microscope Simulation — simulated result across source images.*
**Source**: Any footage — abstract patterns, camera input, or feedback loops.

**Objective**: Combine all optical systems for a complete microscope aesthetic.

1. **Tight vignette**: Set Vignette to ~25% for a narrow circular viewport.
2. **Dense grid**: Set Grid Sz below 25% for fine 8-pixel cells. Select Scale reticle.
3. **Heavy stain**: Choose Gram stain at ~80% intensity. The image takes on a deep blue-violet cast.
4. **Strong contrast**: Set Contrast above 75% for 4× or 8× gain. Fine detail is amplified dramatically.
5. **Dark field**: Toggle to dark field. The stained, contrast-enhanced image inverts — glowing structures on black with blue-violet coloring and a tight vignette.
6. **Brightness**: Adjust Bright to fine-tune the overall illumination level.
7. **Blend**: Lower Mix to ~60% to let the original image ghost through the microscope overlay — the reticle grid appears as a subtle transparent annotation.

**Key concepts**: Vignette simulates the circular eyepiece aperture, all optical systems compound in the pipeline, Mix blending creates transparent annotation overlays

---


## Tips

- **Grid size is discrete**: Unlike most knobs, Grid Sz selects between four fixed spacings (8/16/32/64 pixels). There are no intermediate values — the transitions are abrupt.
- **Focus does nothing**: Pot 4 is reserved for a future feature. Do not expect any visible change when adjusting it.
- **Dark field + stain is the signature look**: Combining dark-field illumination with a stain type produces the most dramatic microscope aesthetic — glowing colored structures on black.
- **Vignette creates the eyepiece**: Even a mild vignette adds significant realism to the microscope simulation. It frames the specimen and draws attention to the center.
- **Reticle adapts to field mode**: Grid lines are automatically dark on bright field and bright on dark field, maintaining visibility in both illumination modes.
- **Mix for annotation**: Use partial Mix values to overlay the reticle grid transparently on the original image — useful for measurement without altering the base footage.
- **Stain type matters more than stain intensity**: The toggle selects fundamentally different color mappings. Start by choosing the stain chemistry, then adjust intensity with the knob.
- **Bypass is at bit 6**: Due to the two-bit toggle encodings for Stain Type and Reticle, the Bypass toggle is at a non-standard bit position. Functionally it works identically to standard bypass.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bright Field** | Standard microscopy illumination where the specimen is lit from below, appearing dark against a bright background. |
| **BT.601** | ITU-R Recommendation BT.601; the color encoding standard used throughout the Videomancer video pipeline for YUV conversion. |
| **Contrast Enhancement** | Amplification of tonal differences by multiplying deviations from mid-gray, making faint structures more visible. |
| **Dark Field** | Microscopy illumination technique where only scattered light reaches the objective, causing structures to glow against a black background. |
| **Gram Stain** | A differential staining technique that classifies bacteria by cell wall composition, producing violet or red-pink coloration. |
| **H&E** | Hematoxylin and Eosin; the most common histological stain combination, producing blue-purple nuclei and pink cytoplasm. |
| **Histology** | The study of the microscopic structure of tissues, typically involving thin-sectioned and chemically stained specimens. |
| **Manhattan Distance** | The sum of absolute horizontal and vertical distances; used here as a computationally efficient approximation of radial distance for vignette calculation. |
| **PAS** | Periodic Acid–Schiff stain; produces magenta coloration in carbohydrate-rich tissue structures. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Reticle** | A pattern of lines inscribed in a microscope eyepiece used for measurement and spatial reference. |
| **Vignette** | Darkening of the image periphery, here simulating the circular aperture of a microscope optical system. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
