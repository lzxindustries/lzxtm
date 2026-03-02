---
draft: true
sidebar_position: 16
slug: /instruments/videomancer/benham
title: "Benham"
image: /img/instruments/videomancer/benham/benham_hero.png
description: "In 1895, the English toymaker Charles Benham marketed a painted spinning top that seemed to do the impossible — produce vivid color sensations from nothing but black and white."
---

import benham_hero from '/img/instruments/videomancer/benham/benham_hero.png';
import benham_before_after from '/img/instruments/videomancer/benham/benham_before_after.png';
import benham_control_panel from '/img/instruments/videomancer/benham/benham_control_panel.png';
import benham_exercise1_result from '/img/instruments/videomancer/benham/benham_exercise1_result.png';
import benham_exercise2_result from '/img/instruments/videomancer/benham/benham_exercise2_result.png';
import benham_exercise3_result from '/img/instruments/videomancer/benham/benham_exercise3_result.png';

# Benham

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={benham_hero} alt="Benham hero image"/>
*Benham disc generating field-alternating monochrome arc sectors that induce subjective color perception through temporal flicker.*
<img src={benham_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Benham applied.*

---

## Overview

In 1895, the English toymaker Charles Benham marketed a painted spinning top that seemed to do the impossible — produce vivid color sensations from nothing but black and white. The disc printed on the top contained carefully arranged arcs: concentric rings of short black lines at different radii. When spun, viewers saw red, green, and blue bands appear where only monochrome paint existed. The phenomenon — known as Fechner colors or subjective colors — exploits timing differences in the human visual system's color channels.

Benham recreates this optical illusion in the digital video domain. Instead of a physically spinning disc, the program generates a radial pattern of black and white sectors centered on the screen, then shifts the pattern's angular position between interlaced fields. The rapid alternation between fields — odd and even — means different arcs occupy different screen positions at 30 Hz, producing the same temporal flicker that makes Benham's original top work. The result is a pure monochrome signal that the viewer's eye interprets as colored.

The entire pattern is computed per-pixel using only shifts, compares, and a small sector-count lookup table — no BRAMs, no multipliers on the angle path. A DDS phase accumulator driven by vsync provides smooth continuous rotation. Six potentiometers control speed, sector count, arc duty cycle, contrast, manual rotation offset, and video-luminance modulation of the angle. Four pattern modes — Arcs, Rings, Spiral, and Radial — reshape the geometry, while a field-mode toggle selects between the alternating half-sector offset that produces the classic Benham illusion and a full-inversion strobe mode.

---

## Background

### Benham's Top and the Discovery of Subjective Colors

Charles Edwin Benham was a journalist and amateur scientist who noticed that certain black-and-white patterns, when rotated at moderate speed (5–10 Hz), produced vivid but unstable color sensations. He was not the first to observe the effect — Gustav Fechner had documented similar phenomena with flickering discs in the 1830s — but Benham popularized it by selling the pattern as a children's toy called "Benham's Artificial Spectrum Top." The effect became one of the most studied illusions in visual psychophysics, precisely because it seemed to violate the basic principle that color perception requires colored light.

### Fechner Colors and Temporal Processing

The standard explanation for subjective color involves the different temporal response curves of the three cone types in the human retina. The short-wavelength (blue) cones respond more slowly than the medium (green) and long (red) cones. When a black-and-white pattern flickers at a rate near the cones' integration time, the three cone channels integrate different amounts of the on/off cycle, producing different effective brightness signals. The visual cortex interprets these unequal signals as color. The perceived hue depends on the flicker rate, the duty cycle of the black-and-white transitions, and the angular position of the arcs relative to the direction of rotation.

### Interlaced Fields as Temporal Flicker

Traditional Benham tops require physical rotation to produce the temporal alternation. In interlaced video, the same effect arises naturally: odd and even fields are displayed 1/60th of a second apart (for NTSC) or 1/50th of a second apart (for PAL). By shifting the pattern's angular position between fields — adding a half-sector offset on one field — each arc alternates between black and white at the field rate. This is precisely the frequency range where Fechner colors are strongest. The program's Alt field mode implements this classic half-sector alternation, while Strobe mode adds a full 180° rotation, creating a more aggressive flicker that emphasizes different color effects.

### Radial Pattern Geometry

The pattern is generated by computing each pixel's angle from the screen center using an octant-based approximation. The full 360° circle is divided into 64 coarse angular steps (6 bits). Within each octant (45° slice), three sub-divisions provide finer resolution using only shift-and-compare operations on the ratio of minor to major displacement — no trigonometric functions, no lookup tables, no division. The radius is approximated with the alpha-max-beta-min formula (major + minor×3/8), which gives an octagonal distance contour that closely approximates a true circle for the purpose of disc clipping. This all-combinational approach keeps LUT usage under 800.

### Pattern Modes and Visual Geometry

The four pattern modes create fundamentally different spatial structures from the same angle and radius signals. **Arcs** uses the lowest bit of the sector index, creating the classic Benham top pattern of alternating black-and-white pie slices. **Rings** ignores the angle entirely, using bit 5 of the radius to create concentric circular bands — a Fresnel-zone-like pattern. **Spiral** XORs the sector parity with the radius bit, producing interlocking spiral arms that wind outward from the center. **Radial** uses bit 1 of the raw angle, creating a dense fan of radial lines. Each mode interacts differently with the field alternation, producing distinct families of subjective color.


---

## Signal Flow

```
Screen Coordinates (h_count, v_count)
│
├── Stage 1: Delta from Center ─────────────────────────────────
│   dx = h_count − 640,  dy = v_count − 360
│   abs_dx, abs_dy, sign bits for octant
│   Latch input Y for video modulation
│
├── Stage 2: Angle + Radius Approximation ──────────────────────
│   Octant (3 bits) from sign(dx), sign(dy), |dy|>|dx|
│   Sub-octant (3 bits) from minor/major ratio [0.25, 0.50, 0.75]
│   coarse_angle = octant(3) & sub(3) → 6-bit (0..63)
│   radius = major + minor>>2 + minor>>3  (≈ max + min×3/8)
│
├── Stage 3: Sector Test + Pattern + Compose ───────────────────
│   rot_angle = coarse_angle + rotation(5:0) + phase_accum(15:10)
│   Video mod: rot_angle += (Y × video_mod) >> 14
│   Field offset: Alt → +half-sector, Strobe → +32
│   sector = (rot_angle × num_sectors) >> 6
│   Pattern select: Arcs=sector(0), Rings=radius(5),
│                   Spiral=sector(0)⊕radius(5), Radial=angle(1)
│   Invert, radius gating (>400 → off)
│   gen_y = on ? 1023 : 0
│
├── Stage 4: Contrast + Output Register ────────────────────────
│   comp_y = gen_y × contrast >> 10
│   Over Video: comp_u/v = input U/V  or  512 (neutral)
│
├── Mix: 3× interpolator_u (4 clocks) ─────────────────────────
│   Y mix = lerp(delayed_input_y, comp_y, mix)
│   U mix = lerp(delayed_input_u, comp_u, mix)
│   V mix = lerp(delayed_input_v, comp_v, mix)
│
├── Sync Delay Pipeline (8 clocks) ─────────────────────────────
│   hsync_n, vsync_n, field_n, Y, U, V delayed to match
│
└── Bypass Mux ─────────────────────────────────────────────────
    Output = bypass ? delayed_input : mixed_output
```

The critical path for the Benham illusion is the field-mode offset in Stage 3. In Alt mode, the angular offset added on field_n='0' equals half of one sector's angular span, which means each arc alternates position between fields — the essential mechanism for producing Fechner colors. The DDS phase accumulator advances once per vsync edge, providing continuous rotation independent of pixel rate. Video modulation shifts the angle on a per-pixel basis using the input luminance, which warps the radial pattern according to the source image's brightness structure — bright areas rotate the pattern more than dark areas, breaking the geometric regularity.

---

## Parameter Reference

<img src={benham_control_panel} alt="Videomancer front panel with Benham loaded"/>
*Videomancer's front panel with Benham active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the rotation animation speed. The value is added to a 16-bit DDS phase accumulator on each vsync rising edge, so the rotation rate is proportional to the register value. At 0% the disc is static; increasing the control smoothly accelerates the spin. Moderate speeds (20–40%) produce the strongest Fechner color effects because the resulting flicker rate falls within the temporal integration window of the cone response curves. Very high speeds blur the sectors into a uniform gray.

---

#### Knob 2 — Sectors
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 7 |

Selects the number of radial sectors from a lookup table of eight values: 2, 3, 4, 6, 8, 10, 12, and 16. Fewer sectors produce wider angular arcs with stronger, more saturated subjective colors. More sectors create finer radial divisions with subtler, pastel-like color effects. The classic Benham top uses around 4–8 sectors. The sector count also affects the field-alternation offset — with fewer sectors, the half-sector shift is a larger angular displacement, producing a more dramatic flicker.

---

#### Knob 3 — Arc Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the angular duty cycle of the white arcs within each sector. At 50%, the pattern is an even alternation of equal-width black and white slices. Reducing the value narrows the white arcs into thin radial lines separated by wide black gaps. Increasing it widens the white regions until the pattern becomes mostly white with thin black dividers. The duty cycle interacts with the field alternation — asymmetric duty cycles produce different temporal profiles on each field, which changes the perceived hue and saturation of the Fechner colors.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the generated luminance pattern before the mix stage. At 100% the pattern swings between full black (0) and full white (1023). Reducing contrast compresses the luminance range — the bright arcs become gray rather than white while black remains black, since the scaling is a simple multiply. This attenuates the subjective color effect because weaker flicker produces weaker cone response differences. Use moderate contrast (60–80%) for subtle pastel illusions.

---

#### Knob 5 — Rotation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Adds a manual angular offset to the pattern, rotating the entire disc without affecting the animation speed. The top 6 bits of the 10-bit register are used, giving 64 discrete rotation positions that cover a full 360° turn. Useful for positioning specific arcs at the screen edge or aligning the pattern with features in the source video when video modulation is active.

---

#### Knob 6 — Video Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Modulates the computed angle by the input video's luminance on a per-pixel basis. At 0%, the pattern is geometrically perfect. As Video Mod increases, bright areas of the source image shift the angle more than dark areas, warping the radial pattern into content-dependent distortions. The modulation uses a 16-bit multiply of the input Y value with the register, shifted right by 14 to fit the 6-bit angle domain. This turns the pure geometric disc into a hybrid effect where the pattern follows the input image's brightness contours.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Arcs | Rings |
| **8 — Field Mode** | Alt | Strobe |
| **9 — Invert** | Off | On |
| **10 — Over Video** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–10 configure the pattern geometry and compositing. Switch 7 (two bits) selects among four fundamentally different spatial patterns — all derived from the same angle and radius computation. Switch 8 selects the field-alternation mode. Switches 9 and 10 control polarity inversion and video overlay compositing. Switch 11 is the standard bypass. The most important interaction is between Pattern (Switch 7) and Field Mode (Switch 8): each pattern mode produces a different family of subjective colors under field alternation because the spatial structure determines which areas of the screen flicker and which remain static.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the delayed input signal and the generated pattern via three interpolator instances (Y, U, V). At 0% the output is pure input video. At 100% the output is the full generated pattern (or pattern overlaid on video color, if Over Video is active). Intermediate values produce a transparent overlay where the pattern floats over a dimmed version of the source.

---

## Guided Exercises

These exercises progress from static pattern observation to animated field-alternating illusions. Subjective color perception varies between individuals and display types — CRT monitors produce the strongest effect due to true interlaced scanning.

### Exercise 1: Static Disc Observation

<img src={benham_exercise1_result} alt="Static Disc Observation result"/>
*Static Disc Observation — simulated result across source images.*
**Source**: Any stable video source (color bars, camera feed, or test pattern).

**Objective**: Understand the basic radial pattern geometry and how sector count and arc width shape the disc.

1. **Static disc**: Set Speed to 0%. Observe the black-and-white pattern centered on screen.
2. **Sector count**: Slowly turn Sectors through its 8 positions. Watch the disc change from 2 wide sectors to 16 narrow ones.
3. **Arc width**: With Sectors at 6 (middle position), sweep Arc Width from 0% to 100%. Observe the duty cycle changing from thin white radial lines to mostly white with thin black dividers.
4. **Pattern modes**: Cycle through all four Pattern positions. Compare Arcs (pie slices), Rings (concentric circles), Spiral (winding arms), and Radial (dense fan).
5. **Radius clipping**: Note how the pattern is confined to a disc of radius 400 pixels — outside this boundary, the output is black.

**Key concepts**: Octant-based angle approximation, sector count lookup table, duty cycle controls arc width, radius gating clips to a disc

---

### Exercise 2: Fechner Color Illusion

<img src={benham_exercise2_result} alt="Fechner Color Illusion result"/>
*Fechner Color Illusion — simulated result across source images.*
**Source**: Black video input (or any — the pattern is self-generated).

**Objective**: Experience the subjective color illusion produced by field-alternating sectors.

1. **Start spinning**: Set Speed to about 30%. The disc begins rotating smoothly.
2. **Field alternation**: Ensure Field Mode is set to Alt. On an interlaced display, you should begin to perceive faint colors — typically amber, green, or blue bands — even though the signal is pure monochrome.
3. **Sector tuning**: Try 4, 6, and 8 sectors. Fewer sectors tend to produce more vivid subjective colors because the angular displacement between fields is larger.
4. **Invert phase**: Toggle Invert. The perceived hues should shift to complementary colors.
5. **Strobe comparison**: Switch Field Mode to Strobe. The flicker becomes more aggressive — full pattern inversion between fields. Compare the perceptual quality with Alt mode.
6. **Contrast variation**: Reduce Contrast to ~60%. The subtler luminance swing often produces more delicate pastel-like color sensations.

**Key concepts**: Fechner colors arise from temporal cone response differences, field alternation provides the flicker, half-sector offset is the classic Benham mechanism, contrast affects flicker strength

---

### Exercise 3: Video-Modulated Pattern

<img src={benham_exercise3_result} alt="Video-Modulated Pattern result"/>
*Video-Modulated Pattern — simulated result across source images.*
**Source**: A camera feed or recorded footage with varied luminance — faces, landscapes, or architectural subjects work well.

**Objective**: Explore how the input video's luminance warps the geometric pattern through Video Mod.

1. **Baseline pattern**: Set Speed ~20%, Sectors at 8, Arc Width ~50%, Contrast 100%. Observe the clean geometric disc.
2. **Enable Video Mod**: Slowly increase Video Mod from 0% to ~60%. Watch the radial pattern warp — bright areas of the source shift the pattern's angle, creating content-dependent distortion.
3. **Over Video**: Enable Over Video (Switch 10). The source video's color now fills the pattern. The disc becomes a luminance mask with the source's chrominance visible through it.
4. **Mix blend**: Reduce Mix to ~60%. The pattern becomes a translucent overlay on the full source video.
5. **Spiral + modulation**: Switch Pattern to Spiral. The video modulation creates organic, plant-like spiral distortions that follow the image's brightness contours.
6. **Animate**: With all controls active, let the animation run. The spinning, video-modulated spiral overlaid on the source creates a complex psychedelic composite.

**Key concepts**: Video modulation warps angle per-pixel based on input luma, Over Video passes source chrominance through the pattern, Mix controls overlay transparency, different pattern modes respond differently to modulation

---


## Tips

- **Interlaced displays are essential for the color illusion**: The Fechner color effect depends on field-rate flicker. On progressive scan monitors that de-interlace or double the frame rate, the alternation may be too fast or too well-blended to produce visible subjective colors. CRT displays or professional monitors with true interlaced output give the strongest effect.
- **Fewer sectors = stronger colors**: With 2 or 3 sectors, the half-sector field offset is a large angular displacement, creating bold flicker. With 12 or 16 sectors, the offset is small, and the effect becomes subtle.
- **Speed matters**: The subjective color effect peaks at moderate rotation speeds — roughly 5–10 full rotations per second. Too slow and the eye adapts; too fast and the sectors blur into gray.
- **Video Mod creates hybrid patterns**: Even a small amount of video modulation (10–20%) breaks the geometric perfection of the disc, creating subtle organic distortions that follow the source image.
- **Spiral mode with Video Mod**: This combination produces the most complex visual effects, as the spiral arms warp along luminance contours in the source.
- **Contrast controls illusion strength**: Lower contrast produces subtler, more pastel Fechner colors. Maximum contrast gives the strongest flicker but can also cause visual fatigue.
- **Feedback loops**: Routing the output back to the input while Video Mod is active creates a self-referencing system where the pattern modulates itself, producing evolving geometric structures.
- **Over Video for compositing**: Enable Over Video and reduce Mix to ~40–50% to layer the Benham disc transparently over a video source — useful for live performance or as a visual texture overlay.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha-max-beta-min** | A fast approximation of Euclidean distance using weighted sums of absolute coordinate differences, avoiding square-root computation. |
| **Chrominance** | The color-difference components (U and V) of a YUV video signal, separate from luminance. |
| **DDS** | Direct Digital Synthesis; a technique that generates a waveform by incrementing a phase accumulator at a fixed rate, here used for continuous rotation. |
| **Duty cycle** | The fraction of one period during which a signal is in the active (white) state; controls the width of white arcs relative to black gaps. |
| **Fechner colors** | Subjective color sensations perceived when viewing flickering black-and-white patterns, caused by differing temporal responses of the retinal cone types. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline in hardware. |
| **Interlaced fields** | A video scanning method where each frame is split into two fields (odd and even lines) displayed sequentially, producing temporal flicker at the field rate. |
| **Interpolator** | A hardware module that performs linear crossfading between two signals (wet and dry) based on a mix parameter. |
| **Luminance** | The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color. |
| **LUT** | Look-Up Table; a small ROM that maps an input index to a pre-computed output value, here used for the sector count table. |
| **Octant** | One of eight 45-degree sectors dividing a full circle, used to simplify angle computation with shift-and-compare logic. |
| **Phase accumulator** | A register that increments by a fixed step each cycle, wrapping at overflow to produce a sawtooth ramp representing angular position. |
| **YUV** | A color encoding that separates luminance (Y) from two chrominance components (U and V), used in broadcast video. |


---
