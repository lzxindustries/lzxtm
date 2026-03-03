---
draft: true
sidebar_position: 184
slug: /instruments/videomancer/maelstrom
title: "Maelstrom"
image: /img/instruments/videomancer/maelstrom/maelstrom_hero_s1.png
description: "Every pixel in a video frame has a position."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import maelstrom_source1_field from '/img/instruments/videomancer/maelstrom/maelstrom_source1_field.png';
import maelstrom_source2_house from '/img/instruments/videomancer/maelstrom/maelstrom_source2_house.png';
import maelstrom_source3_collage from '/img/instruments/videomancer/maelstrom/maelstrom_source3_collage.png';
import maelstrom_source4_pattern from '/img/instruments/videomancer/maelstrom/maelstrom_source4_pattern.png';
import maelstrom_source5_boy from '/img/instruments/videomancer/maelstrom/maelstrom_source5_boy.png';
import maelstrom_source6_paint from '/img/instruments/videomancer/maelstrom/maelstrom_source6_paint.png';
import maelstrom_hero_s1 from '/img/instruments/videomancer/maelstrom/maelstrom_hero_s1.png';
import maelstrom_hero_s2 from '/img/instruments/videomancer/maelstrom/maelstrom_hero_s2.png';
import maelstrom_hero_s3 from '/img/instruments/videomancer/maelstrom/maelstrom_hero_s3.png';
import maelstrom_hero_s4 from '/img/instruments/videomancer/maelstrom/maelstrom_hero_s4.png';
import maelstrom_hero_s5 from '/img/instruments/videomancer/maelstrom/maelstrom_hero_s5.png';
import maelstrom_hero_s6 from '/img/instruments/videomancer/maelstrom/maelstrom_hero_s6.png';
import maelstrom_ex1_s1 from '/img/instruments/videomancer/maelstrom/maelstrom_ex1_s1.png';
import maelstrom_ex1_s2 from '/img/instruments/videomancer/maelstrom/maelstrom_ex1_s2.png';
import maelstrom_ex1_s3 from '/img/instruments/videomancer/maelstrom/maelstrom_ex1_s3.png';
import maelstrom_ex1_s4 from '/img/instruments/videomancer/maelstrom/maelstrom_ex1_s4.png';
import maelstrom_ex1_s5 from '/img/instruments/videomancer/maelstrom/maelstrom_ex1_s5.png';
import maelstrom_ex1_s6 from '/img/instruments/videomancer/maelstrom/maelstrom_ex1_s6.png';
import maelstrom_ex2_s1 from '/img/instruments/videomancer/maelstrom/maelstrom_ex2_s1.png';
import maelstrom_ex2_s2 from '/img/instruments/videomancer/maelstrom/maelstrom_ex2_s2.png';
import maelstrom_ex2_s3 from '/img/instruments/videomancer/maelstrom/maelstrom_ex2_s3.png';
import maelstrom_ex2_s4 from '/img/instruments/videomancer/maelstrom/maelstrom_ex2_s4.png';
import maelstrom_ex2_s5 from '/img/instruments/videomancer/maelstrom/maelstrom_ex2_s5.png';
import maelstrom_ex2_s6 from '/img/instruments/videomancer/maelstrom/maelstrom_ex2_s6.png';
import maelstrom_ex3_s1 from '/img/instruments/videomancer/maelstrom/maelstrom_ex3_s1.png';
import maelstrom_ex3_s2 from '/img/instruments/videomancer/maelstrom/maelstrom_ex3_s2.png';
import maelstrom_ex3_s3 from '/img/instruments/videomancer/maelstrom/maelstrom_ex3_s3.png';
import maelstrom_ex3_s4 from '/img/instruments/videomancer/maelstrom/maelstrom_ex3_s4.png';
import maelstrom_ex3_s5 from '/img/instruments/videomancer/maelstrom/maelstrom_ex3_s5.png';
import maelstrom_ex3_s6 from '/img/instruments/videomancer/maelstrom/maelstrom_ex3_s6.png';

# Maelstrom

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: maelstrom_source1_field, after: maelstrom_hero_s1 },
    { label: "House", before: maelstrom_source2_house, after: maelstrom_hero_s2 },
    { label: "Collage", before: maelstrom_source3_collage, after: maelstrom_hero_s3 },
    { label: "Pattern", before: maelstrom_source4_pattern, after: maelstrom_hero_s4 },
    { label: "Boy", before: maelstrom_source5_boy, after: maelstrom_hero_s5 },
    { label: "Paint", before: maelstrom_source6_paint, after: maelstrom_hero_s6 },
  ]}
/>
*Maelstrom warping a camera feed into concentric rings of radially displaced, color-inverted imagery radiating from a controllable singularity.*

---

## Overview

Every pixel in a video frame has a position. Maelstrom takes each pixel's distance from a configurable center point and uses that distance to move it — displacing pixels along radial lines according to a sine wave that ripples outward from the center. Close to the center the displacement is intense; farther away it fades. The result is concentric rings of warped imagery, like the visual distortion of looking through a glass sphere or the surface of disturbed water.

Beyond displacement, Maelstrom adds a second layer of visual disruption: alternating radial bands where the luminance and chrominance channels are inverted. At certain radial distances the image appears in negative; at others it appears normal. The band boundaries follow the distorted radius, so the inversion pattern ripples and breathes with the same wave that drives the displacement. The name evokes the Norse legend of the Maelström — a massive whirlpool that pulls everything toward its center.

At conservative settings — low Depth, moderate Frequency — Maelstrom produces gentle concentric ripples reminiscent of heat haze or underwater refraction. At extreme settings, the entire image explodes into a pulsating vortex of displaced, inverted, and twisted video. The Speed and Expand controls add animation, making the rings radiate outward or contract inward in endless cycles.

---

## Background

### Radial Coordinate Transforms

Video effects based on polar coordinates — radius and angle from a center point — produce patterns that radiate symmetrically outward. Converting Cartesian pixel coordinates to polar requires computing the Euclidean distance $r = \sqrt{dx^2 + dy^2}$. On an FPGA without dedicated multiplier/divider units, this is expensive. Maelstrom uses the **alpha-max-plus-beta-min** approximation, a classic embedded-systems technique that estimates radius as $r \approx \max(|dx|, |dy|) + 0.4375 \cdot \min(|dx|, |dy|)$. The error is less than 4% — imperceptible in a real-time video effect. This avoids the square root entirely, requiring only comparisons and shifts.

### Sine-Wave Displacement

Once the radius is known, Maelstrom computes a displacement $\Delta = A \cdot \sin(F \cdot r + \phi)$ where $A$ is the amplitude (Depth), $F$ is the spatial frequency, and $\phi$ is the animation phase that advances each frame. The sine is evaluated from a 64-entry quarter-wave lookup table using quadrant folding — the same technique used in audio DDS (Direct Digital Synthesis) chips. The displacement is applied horizontally: each pixel's read address is shifted left or right along the scanline by the displacement amount. Vertical displacement would require two-dimensional frame buffers; by restricting distortion to the horizontal axis, Maelstrom achieves the effect using only a single-line scanline buffer per channel.

### Scanline Buffer Architecture

Maelstrom writes incoming pixels into 2048-deep scanline buffers (one for Y, one for U, one for V — each 10 bits wide, consuming 4 BRAM tiles). As each pixel is written at the current horizontal position, it is simultaneously read from a *displaced* horizontal address — the current position offset by the radial distortion value. This creates a horizontal warp that varies across the screen based on each pixel's distance from the center. Pixels near the distortion center experience the largest displacement; pixels at the edges of the frame experience little to none.

### Band Inversion

After displacement, Maelstrom optionally divides the radial field into alternating bands of normal and inverted imagery. The band boundaries are determined by inspecting a single bit of the distorted radius value. Which bit is inspected depends on the Band Width control — lower settings select lower bits (narrow bands, closely spaced), while higher settings select higher bits (wide bands, far apart). Because the inversion pattern tracks the distorted radius rather than the original, the band edges ripple with the displacement wave, creating the signature pulsating-ring appearance.

### DDS Animation

All animation in Maelstrom is driven by Direct Digital Synthesis (DDS) phase accumulators — 16-bit counters that increment by a configurable step on each video frame. The Speed control sets the main displacement wave's phase increment. Separate accumulators drive the expand/contract breathing effect and the Lissajous center drift. The DDS approach guarantees smooth, jitter-free animation at any speed, including extremely slow motion where the phase advances by only a few counts per second.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Scanline Buffer Write ──────────────────────────────────────
│   └─ Write Y, U, V to 2048-deep line buffers at h_count
│
├── Position + Center ──────────────────────────────────────────
│   ├─ h_count, v_count from timing generator
│   ├─ Center X/Y from pots (+ optional Lissajous drift)
│   └─ dx = h_count − cx,  dy = v_count − cy
│
├── Stage 1: Radius Approximation ──────────────────────────────
│   └─ r ≈ max(|dx|,|dy|) + 0.4375 · min(|dx|,|dy|)
│       (alpha-max-plus-beta-min, no sqrt)
│
├── Stage 2: Radial Distortion ─────────────────────────────────
│   ├─ arg = (frequency × radius[11:2] >> 8) + anim_phase
│   ├─ Optional: arg −= expand_phase (breathing)
│   ├─ Waveform: sine LUT (64-entry quarter-wave) or square wave
│   ├─ dist_offset = depth × sin_val >> 9
│   ├─ distorted_r = radius + dist_offset (clamped ≥ 0)
│   └─ Band inversion: select bit of distorted_r via band_width
│
├── Stage 3: Displaced Read + Inversion ────────────────────────
│   ├─ Read address = h_count + dist_offset (clamped to buffer)
│   ├─ Fetch Y, U, V from scanline buffer
│   └─ If invert_flag: Y = 1023−Y, U = 1023−U, V = 1023−V
│
├── Sync / Data Delay (8 clocks) ───────────────────────────────
│   └─ Shift registers: hsync, vsync, field, Y, U, V
│
├── Interpolator Mix (4 clocks) ────────────────────────────────
│   └─ 3× interpolator_u: crossfade delayed dry ↔ wet
│
└── Output ─────────────────────────────────────────────────────
    └─ Mixed Y, U, V + delayed sync (no bypass mux)
```

The displacement operates only in the horizontal direction — each pixel's read address is shifted left or right along the same scanline. This is why the effect creates concentric *rings* rather than true radial distortion in all directions: the vertical component of the radius determines the displacement amplitude but does not shift the pixel vertically. The inversion flag is computed from the distorted radius (not the original), so band edges follow the rippling displacement wave. Critically, the Bypass toggle declared in the TOML is never read by the VHDL — `registers_in(6)(4)` is not connected. Output always passes through the wet/dry mix; to hear the dry signal only, set Mix to 0%.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the amplitude of the radial displacement wave. At 0%, no distortion — the scanline buffer read address equals the write address and the image passes through unchanged (before mixing). As Depth increases, pixels are displaced farther from their original positions, creating wider ripples. At maximum, the displacement can exceed hundreds of pixels, producing dramatic warping where features stretch and compress across the frame. Depth scales the sine value linearly: `dist_offset = depth × sin_val >> 9`.

---

#### Knob 2 — Frequency
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Controls the spatial frequency of the displacement sine wave — how many concentric rings appear between the center and the edge of the frame. At low settings, the entire frame may contain only one or two broad undulations. At high settings, many tightly spaced concentric rings pack into the visible area, creating a fine ripple pattern. Frequency multiplies the radius in the sine argument: higher frequency means more cycles per unit of radial distance.

---

#### Knob 3 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the animation rate of the displacement wave. The Speed register value is added to a 16-bit DDS phase accumulator on each video frame (vsync). At 0%, the wave pattern is static. Low values produce slow, meditative outward drift. High values produce rapid pulsation. The phase is continuous and wraps at 16 bits, producing seamless cyclic animation at any speed.

---

#### Knob 4 — Band W
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls the width of the radial inversion bands by selecting which bit of the 12-bit distorted radius determines the inversion flag. Low register values (below 128) select bit 3, creating very narrow bands approximately 8 pixels wide. Higher values progressively select higher bits — bit 4 (16 px), bit 5 (32 px), bit 6 (64 px), bit 7 (128 px), bit 8 (256 px), bit 9 (512 px), and at maximum, bit 10 (1024 px). The transition between band widths is discrete, not continuous, because each threshold selects a different binary bit.

---

#### Knob 5 — Center X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the horizontal center of the distortion field. At 0%, the center is at the left edge of the active video; at 100%, at the right edge. At the midpoint (register 512), the center is roughly in the middle of the 1920-pixel-wide frame. When Drift is enabled, this value serves as the base offset — the Lissajous pattern adds a ±200 pixel oscillation on top of the pot position.

---

#### Knob 6 — Center Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the vertical center of the distortion field. Behaves identically to Center X but for the vertical axis. Combined, Center X and Center Y define the singularity point from which all concentric rings radiate. Moving the center off-screen shifts the ring pattern so that only partial arcs are visible — a useful compositional technique for creating asymmetric warps.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Inv Mode** | Off | On |
| **8 — Wave** | Sine | Square |
| **9 — Drift** | Off | On |
| **10 — Expand** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options. Inv Mode and Wave shape the distortion character, while Drift and Expand add DDS-driven animation. The Bypass toggle is declared in the TOML metadata but is not connected in the VHDL implementation — `registers_in(6)(4)` is never read. The output always passes through the interpolator mix stage.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the delayed original input and the distorted, optionally inverted wet signal. At 0% (register 0), the output is the original delayed input — no visible effect. At 100% (register 1023), the output is fully the processed signal. Because no bypass toggle is implemented, the Mix fader is the only way to control the effect intensity. Intermediate values blend the distorted and undistorted signals, creating a ghost-like overlay where the original image shows through the warped version.

---

## Guided Exercises

These exercises progress from gentle radial ripples to full vortex animation, exploring displacement, inversion bands, and motion controls.

### Exercise 1: Concentric Ripples

<BeforeAfterSlider
  sources={[
    { label: "Field", before: maelstrom_source1_field, after: maelstrom_ex1_s1 },
    { label: "House", before: maelstrom_source2_house, after: maelstrom_ex1_s2 },
    { label: "Collage", before: maelstrom_source3_collage, after: maelstrom_ex1_s3 },
    { label: "Pattern", before: maelstrom_source4_pattern, after: maelstrom_ex1_s4 },
    { label: "Boy", before: maelstrom_source5_boy, after: maelstrom_ex1_s5 },
    { label: "Paint", before: maelstrom_source6_paint, after: maelstrom_ex1_s6 },
  ]}
/>
*Concentric Ripples — simulated result across source images.*
**Source**: A live camera feed or recorded footage with strong horizontal detail — architecture, text, or geometric patterns work well.

**Objective**: Learn how Depth and Frequency interact to create concentric displacement rings.

1. **Gentle ripple**: Starting from defaults, slowly increase Depth. Watch as the image begins to shimmer with faint concentric rings.
2. **Add frequency**: Increase Frequency to pack more rings into the visible area. The ripples become tighter and more densely spaced.
3. **Center position**: Move Center X and Center Y while watching the ring pattern recenter itself in real time. Position the center over a face or prominent feature.
4. **Static vs. animated**: Note that the wave is static until you increase Speed. The rings are frozen in place, allowing careful study of the displacement pattern.
5. **Speed sweep**: Slowly increase Speed. The rings begin to drift outward, creating a living, breathing distortion field.

**Key concepts**: Radial displacement follows a sine wave, Depth is amplitude, Frequency is spatial frequency, displacement operates horizontally only, Speed animates the phase

---

### Exercise 2: Inversion Bands

<BeforeAfterSlider
  sources={[
    { label: "Field", before: maelstrom_source1_field, after: maelstrom_ex2_s1 },
    { label: "House", before: maelstrom_source2_house, after: maelstrom_ex2_s2 },
    { label: "Collage", before: maelstrom_source3_collage, after: maelstrom_ex2_s3 },
    { label: "Pattern", before: maelstrom_source4_pattern, after: maelstrom_ex2_s4 },
    { label: "Boy", before: maelstrom_source5_boy, after: maelstrom_ex2_s5 },
    { label: "Paint", before: maelstrom_source6_paint, after: maelstrom_ex2_s6 },
  ]}
/>
*Inversion Bands — simulated result across source images.*
**Source**: Color bars or footage with a wide range of brightness values and saturated colors — the inversion effect is most visible on varied content.

**Objective**: Explore band inversion and understand how Band Width selects inversion zone spacing.

1. **Enable inversion**: Turn Inv Mode On. Immediately, alternating rings of the image appear in negative.
2. **Band Width sweep**: Slowly turn Band W from minimum to maximum. Watch the inversion bands grow from very narrow stripes to broad zones. Notice the stepped transitions — the band width changes discretely as different bits of the radius are selected.
3. **Frequency interaction**: Increase Frequency. The inversion bands follow the distorted radius, so higher frequency creates more inversion transitions within the same radial distance.
4. **Square wave**: Switch Wave to Square. The displacement becomes hard-edged, and the inversion bands snap to crisp boundaries instead of fading gradually.
5. **Depth at zero**: Set Depth to 0%. The displacement disappears but the inversion bands remain — perfectly concentric zones of normal and inverted imagery with no spatial distortion.

**Key concepts**: Band inversion uses a single bit of the distorted radius, Band Width selects which bit (3 through 10), inversion applies to all three channels (Y, U, V), bands follow distorted not original radius

---

### Exercise 3: Animated Vortex

<BeforeAfterSlider
  sources={[
    { label: "Field", before: maelstrom_source1_field, after: maelstrom_ex3_s1 },
    { label: "House", before: maelstrom_source2_house, after: maelstrom_ex3_s2 },
    { label: "Collage", before: maelstrom_source3_collage, after: maelstrom_ex3_s3 },
    { label: "Pattern", before: maelstrom_source4_pattern, after: maelstrom_ex3_s4 },
    { label: "Boy", before: maelstrom_source5_boy, after: maelstrom_ex3_s5 },
    { label: "Paint", before: maelstrom_source6_paint, after: maelstrom_ex3_s6 },
  ]}
/>
*Animated Vortex — simulated result across source images.*
**Source**: Any active video — faces, nature, or abstract patterns all work well at maximum effect intensity.

**Objective**: Combine all motion controls for a fully animated whirlpool effect.

1. **Full distortion**: Set Depth ~70%, Frequency ~50%. The image should be heavily warped with visible concentric rings.
2. **Animate**: Set Speed to ~40%. The rings begin pulsating outward.
3. **Expand**: Enable Expand. A second breathing motion layer appears — the rings seem to inflate and deflate in addition to their radial drift.
4. **Drift**: Enable Drift. The center of the distortion begins wandering across the frame on a Lissajous path, carrying the entire ring structure with it.
5. **Inversion**: Enable Inv Mode with Band W at ~60%. Alternating positive/negative rings add visual complexity.
6. **Mix blend**: Lower Mix to ~60% and observe the ghostly overlay of the distorted and original images.

**Key concepts**: Three independent DDS accumulators (Speed, Expand, Drift) produce layered animation, Lissajous motion uses coprime increments (47 and 31), all motion is phase-continuous and seamless

---


## Tips

- **Horizontal only**: Displacement moves pixels left and right along the scanline — the vertical structure of the rings comes from the radius computation, not from vertical pixel shift. This keeps BRAM usage to a single scanline buffer.
- **No bypass**: The Bypass toggle in the TOML is not connected in VHDL. Use Mix at 0% for a fully dry signal.
- **Band Width is exponential**: Each step selects the next higher bit of the radius, effectively doubling the band width. The control feels nonlinear because it *is* nonlinear — it's a bit selector, not a continuous width.
- **Depth at zero is useful**: With Depth at 0%, no displacement occurs, but inversion bands still appear as perfectly concentric rings. This is a distinct visual mode — clean radial inversion without any warping.
- **Drift adds life**: Even subtle Drift (center wandering ±100 px) prevents the pattern from looking static and mechanical. The Lissajous path has a long repeat period due to coprime DDS increments.
- **Expand vs. Speed**: Speed animates the wave envelope outward. Expand modulates the wave argument itself, creating a breathing effect where rings appear to grow from the center. Together they create complex layered motion.
- **Feedback potential**: Routing the output back to the input creates recursive displacement — each pass warps the already-warped image, producing increasingly extreme vortex effects that evolve over time.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha-max-plus-beta-min** | A fast approximation for Euclidean distance using only comparisons, additions, and bit shifts. Error is typically under 4%. |
| **BRAM** | Block RAM; dedicated memory tiles on the FPGA used here for 2048×10 scanline buffers. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator and lookup table. |
| **Displacement** | Shifting a pixel's read address relative to its write address, causing spatial warping of the image. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip that executes the video processing pipeline in real time. |
| **Interpolator** | A linear crossfade module (`interpolator_u`) that blends dry and wet signals based on the Mix parameter. |
| **Lissajous** | A family of curves traced by combining sinusoidal motions at different frequencies on perpendicular axes. Used here for center drift. |
| **Pipeline** | A series of sequential processing stages, each completing one clock cycle of work before passing results to the next stage. |
| **Quarter-wave LUT** | A lookup table storing one quarter of a sine wave (0° to 90°); the full waveform is reconstructed by quadrant folding and sign inversion. |
| **Scanline buffer** | A memory that stores one horizontal line of video, enabling displaced horizontal reads for spatial warping. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline at 10-bit precision. |

---
