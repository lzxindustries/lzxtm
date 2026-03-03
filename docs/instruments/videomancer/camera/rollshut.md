---
draft: true
sidebar_position: 253
slug: /instruments/videomancer/rollshut
title: "Roll Shutter"
image: /img/instruments/videomancer/rollshut/rollshut_hero_s1.png
description: "Rollshut simulates the rolling-shutter artifact common to CMOS image sensors, where each scanline is captured at a slightly different moment in time."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import rollshut_control_panel from '/img/instruments/videomancer/rollshut/rollshut_control_panel.png';
import rollshut_source1_house from '/img/instruments/videomancer/rollshut/rollshut_source1_house.png';
import rollshut_source2_boat from '/img/instruments/videomancer/rollshut/rollshut_source2_boat.png';
import rollshut_source3_clouds from '/img/instruments/videomancer/rollshut/rollshut_source3_clouds.png';
import rollshut_source4_pattern from '/img/instruments/videomancer/rollshut/rollshut_source4_pattern.png';
import rollshut_source5_woman from '/img/instruments/videomancer/rollshut/rollshut_source5_woman.png';
import rollshut_source6_knit from '/img/instruments/videomancer/rollshut/rollshut_source6_knit.png';
import rollshut_hero_s1 from '/img/instruments/videomancer/rollshut/rollshut_hero_s1.png';
import rollshut_hero_s2 from '/img/instruments/videomancer/rollshut/rollshut_hero_s2.png';
import rollshut_hero_s3 from '/img/instruments/videomancer/rollshut/rollshut_hero_s3.png';
import rollshut_hero_s4 from '/img/instruments/videomancer/rollshut/rollshut_hero_s4.png';
import rollshut_hero_s5 from '/img/instruments/videomancer/rollshut/rollshut_hero_s5.png';
import rollshut_hero_s6 from '/img/instruments/videomancer/rollshut/rollshut_hero_s6.png';
import rollshut_ex1_s1 from '/img/instruments/videomancer/rollshut/rollshut_ex1_s1.png';
import rollshut_ex1_s2 from '/img/instruments/videomancer/rollshut/rollshut_ex1_s2.png';
import rollshut_ex1_s3 from '/img/instruments/videomancer/rollshut/rollshut_ex1_s3.png';
import rollshut_ex1_s4 from '/img/instruments/videomancer/rollshut/rollshut_ex1_s4.png';
import rollshut_ex1_s5 from '/img/instruments/videomancer/rollshut/rollshut_ex1_s5.png';
import rollshut_ex1_s6 from '/img/instruments/videomancer/rollshut/rollshut_ex1_s6.png';
import rollshut_ex2_s1 from '/img/instruments/videomancer/rollshut/rollshut_ex2_s1.png';
import rollshut_ex2_s2 from '/img/instruments/videomancer/rollshut/rollshut_ex2_s2.png';
import rollshut_ex2_s3 from '/img/instruments/videomancer/rollshut/rollshut_ex2_s3.png';
import rollshut_ex2_s4 from '/img/instruments/videomancer/rollshut/rollshut_ex2_s4.png';
import rollshut_ex2_s5 from '/img/instruments/videomancer/rollshut/rollshut_ex2_s5.png';
import rollshut_ex2_s6 from '/img/instruments/videomancer/rollshut/rollshut_ex2_s6.png';
import rollshut_ex3_s1 from '/img/instruments/videomancer/rollshut/rollshut_ex3_s1.png';
import rollshut_ex3_s2 from '/img/instruments/videomancer/rollshut/rollshut_ex3_s2.png';
import rollshut_ex3_s3 from '/img/instruments/videomancer/rollshut/rollshut_ex3_s3.png';
import rollshut_ex3_s4 from '/img/instruments/videomancer/rollshut/rollshut_ex3_s4.png';
import rollshut_ex3_s5 from '/img/instruments/videomancer/rollshut/rollshut_ex3_s5.png';
import rollshut_ex3_s6 from '/img/instruments/videomancer/rollshut/rollshut_ex3_s6.png';

# Roll Shutter

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "House", before: rollshut_source1_house, after: rollshut_hero_s1 },
    { label: "Boat", before: rollshut_source2_boat, after: rollshut_hero_s2 },
    { label: "Clouds", before: rollshut_source3_clouds, after: rollshut_hero_s3 },
    { label: "Pattern", before: rollshut_source4_pattern, after: rollshut_hero_s4 },
    { label: "Woman", before: rollshut_source5_woman, after: rollshut_hero_s5 },
    { label: "Knit", before: rollshut_source6_knit, after: rollshut_hero_s6 },
  ]}
/>
*Rolling-shutter simulation distorting a video frame with per-scanline horizontal displacement, recreating the wobbling, skewed look of CMOS sensor readout on fast-moving subjects.*

---

## Overview

**Rollshut** simulates the **rolling-shutter** artifact common to CMOS image sensors, where each scanline is captured at a slightly different moment in time. When the camera or subject moves during readout, the frame becomes horizontally skewed — vertical lines lean into diagonals, and sudden movements produce the characteristic "jello" wobble. This artifact is familiar from smartphone and drone footage, where rapid panning or vibration causes straight edges to bend and warp.

The implementation stores a 64-pixel-wide circular buffer per channel (Y, U, V) using distributed RAM. Each scanline is read from a different position within the buffer, determined by a skew rate that increases with vertical position. A 16-entry signed sine table modulates the per-scanline offset with frame-rate wobble, producing the organic, trembling distortion seen in real rolling shutters. The Direction toggle flips the skew gradient, and the optional Blur mode averages the displaced pixel with the current position for a motion-blur effect.

Rollshut is in the **Camera** category — a family of effects that recreate lens, sensor, and capture artifacts from physical cameras.

---

## Background

### What Is Rolling Shutter?

A **rolling shutter** reads the image sensor one row at a time, from top to bottom (or vice versa). Each row is exposed at a slightly different instant. If the scene changes during readout — due to camera pan, subject motion, or vibration — the recorded frame contains a mixture of time-shifted slices. Vertical lines appear tilted, fast horizontal motion causes skewing, and vibration produces a distinctive "jellyfish" wobble. Global-shutter sensors capture all rows simultaneously, eliminating this artifact.

### What Is Scanline Displacement?

Rollshut recreates rolling-shutter distortion by **displacing each scanline horizontally** by an amount proportional to its vertical position. The bottom of the frame is displaced more than the top (or the reverse, depending on direction). This per-line offset simulates the time delay between readout of the first and last row. The offset is clamped to the 64-pixel buffer depth, limiting maximum displacement while keeping the computation simple.

### What Is Wobble Modulation?

Real rolling-shutter artifacts are rarely a clean linear skew — vibration and hand tremor add an oscillatory component. Rollshut adds a **sine-wave wobble** derived from the frame counter, so the skew rate oscillates over time. A 16-entry signed sine table provides the modulation waveform. The wobble amplitude is separately controllable, allowing anything from a steady lean to violent camera-shake distortion.

### What Is Motion Blur via Averaging?

When Blur mode is enabled, each output pixel is the average of the current (undisplaced) pixel and the displaced pixel. This simulates the motion blur inherent in a real rolling shutter, where each row integrates light during its exposure window. The averaging softens the displacement boundary and produces a more photorealistic smear.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ X counter (per-pixel, reset on hsync)
│   ├─ Y counter (per-line, reset on vsync)
│   └─ Frame counter (wobble timebase)
│
├── Offset Computation ─────────────────────────────────────────
│   ├─ 1. Y normalization    (vertical position → 0-1 range)
│   ├─ 2. Direction flip     (top-to-bottom or reversed)
│   ├─ 3. Base skew          (y_normalized × skew_rate)
│   ├─ 4. Sine wobble        (sin(frame) × wobble_amount)
│   ├─ 5. Combined offset    (base skew + wobble)
│   ├─ 6. Roll depth scale   (× roll_depth knob)
│   └─ 7. Clamp to 0–63     (buffer depth limit)
│
├── Line Buffer (per Y/U/V) ───────────────────────────────────
│   ├─ 64-entry circular buffer (distributed RAM)
│   ├─ Write: current pixel at write pointer
│   ├─ Read: pixel at (write_ptr - offset)
│   └─ Blur: average of current + displaced pixels
│
├── Post-Processing ────────────────────────────────────────────
│   ├─ Contrast      (expand/compress around 512)
│   ├─ Brightness    (DC offset)
│   ├─ Fade          (interpolator mix with input)
│   └─ Invert Y      (optional complement)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through with 6-clock delay
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The offset computation is the heart of the effect. The vertical position is normalized and optionally flipped (Direction toggle), then multiplied by the skew rate to produce a linear displacement gradient. The sine wobble adds an oscillatory perturbation that varies with frame number. The combined offset is scaled by Roll Depth and clamped to the 64-pixel buffer range. The circular buffer write pointer advances each pixel clock, and reading from `write_ptr - offset` yields a horizontally displaced version of the signal. The Blur option averages displaced and current samples for motion-blur softening.

---

## Parameter Reference

<img src={rollshut_control_panel} alt="Videomancer front panel with Roll Shutter loaded"/>
*Videomancer's front panel with Roll Shutter active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Roll Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the maximum displacement depth across the frame. At minimum, no scanlines are displaced — the image appears normal. At maximum, the bottom (or top) of the frame is displaced by 63 pixels horizontally, producing extreme skewing. This is the primary "intensity" control for the rolling-shutter effect. Moderate settings (25–50%) produce the natural-looking wobble typical of smartphone video.

---

#### Knob 2 — Skew Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the skew rate — the slope of the displacement gradient from top to bottom (or bottom to top). At minimum, all scanlines share the same offset (uniform horizontal shift). At maximum, the displacement changes steeply with vertical position, producing extreme diagonal lean. Combined with the Direction toggle, this shapes whether the skew appears as a forward or backward lean.

---

#### Knob 3 — Wobble
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the amplitude of the sinusoidal wobble modulation. At zero, the skew is steady (no temporal variation). Increasing Wobble adds progressively more frame-to-frame oscillation to the offset, producing the trembling, vibrating quality of real handheld rolling-shutter footage. At maximum, the wobble can swing the displacement through its full range.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adjusts the output contrast — the expansion or compression of luminance around the midpoint (512). At 50%, contrast is unity (no change). Above 50%, the tonal range is expanded; below 50%, it compresses toward gray. This is applied after displacement and blur.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC brightness offset to the output signal. At 50%, no shift. Above center brightens, below center darkens. Useful for compensating brightness changes from the contrast control or matching levels with other effects in a chain.

---

#### Knob 6 — Fade
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the fade amount — an interpolator blend between the displaced (processed) signal and the original input. At maximum, the full displaced signal is output. At minimum, the original input is output unmodified. This functions as a wet/dry mix applied via the hardware interpolator.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Direction** | Down | Up |
| **8 — Blur** | Off | On |
| **9 — Freeze** | Off | On |
| **10 — Invert Y** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control skew direction, motion blur, frame freeze, luminance inversion, and bypass. Direction and Blur have the most impact on the visual character of the effect — Direction determines whether the skew leans forward or backward, and Blur softens the displacement for a more photorealistic look.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

The fader serves as the primary wet/dry mix. At 100%, the full rolling-shutter processed output is delivered. Lowering the fader smoothly blends back toward the unprocessed input via the hardware interpolator.

---

## Guided Exercises

These exercises explore linear skew, wobble animation, and the blur setting for natural rolling-shutter looks.

### Exercise 1: Linear Skew (Static)

<BeforeAfterSlider
  sources={[
    { label: "House", before: rollshut_source1_house, after: rollshut_ex1_s1 },
    { label: "Boat", before: rollshut_source2_boat, after: rollshut_ex1_s2 },
    { label: "Clouds", before: rollshut_source3_clouds, after: rollshut_ex1_s3 },
    { label: "Pattern", before: rollshut_source4_pattern, after: rollshut_ex1_s4 },
    { label: "Woman", before: rollshut_source5_woman, after: rollshut_ex1_s5 },
    { label: "Knit", before: rollshut_source6_knit, after: rollshut_ex1_s6 },
  ]}
/>
*Linear Skew (Static) — simulated result across source images.*
**Source**: Camera input with strong vertical lines (window blinds, columns, bookshelves) — verticals make skew clearly visible.

**Objective**: Produce a clean, static rolling-shutter lean without wobble.

1. **No wobble**: Set Wobble to 0%. The displacement will be purely linear.
2. **Roll Depth**: Increase Roll Depth to ~50%. Vertical edges begin to lean diagonally.
3. **Skew Rate**: Increase Skew Rate. The lean angle steepens.
4. **Direction**: Flip Direction between Down and Up. The lean reverses.
5. **Observe displacement**: Note how the bottom (or top) of the frame is displaced horizontally relative to the center.
6. **Fade blend**: Use Fade to blend the skewed image with the original for a subtle double-exposure look.

**Key concepts**: Scanline displacement creates a linear skew, Roll Depth controls maximum offset, Skew Rate controls steepness, Direction flips the gradient

---

### Exercise 2: Jello Wobble

<BeforeAfterSlider
  sources={[
    { label: "House", before: rollshut_source1_house, after: rollshut_ex2_s1 },
    { label: "Boat", before: rollshut_source2_boat, after: rollshut_ex2_s2 },
    { label: "Clouds", before: rollshut_source3_clouds, after: rollshut_ex2_s3 },
    { label: "Pattern", before: rollshut_source4_pattern, after: rollshut_ex2_s4 },
    { label: "Woman", before: rollshut_source5_woman, after: rollshut_ex2_s5 },
    { label: "Knit", before: rollshut_source6_knit, after: rollshut_ex2_s6 },
  ]}
/>
*Jello Wobble — simulated result across source images.*
**Source**: Handheld or slightly shaky camera feed — imperfect motion enhances the realism.

**Objective**: Recreate the characteristic "jello" wobble of handheld CMOS footage.

1. **Enable wobble**: Set Wobble to ~40%. The frame begins to oscillate.
2. **Roll Depth**: Set Roll Depth to ~35%. Moderate displacement keeps the effect believable.
3. **Skew Rate**: Set Skew Rate to ~40%. Enough gradient to see the wobble propagate spatially.
4. **Observe jello**: Vertical edges should appear to wobble back and forth, mimicking CMOS readout during vibration.
5. **Increase wobble**: Push Wobble to ~70%. The effect becomes more extreme — like aggressive handheld DSLR footage.
6. **Blur**: Enable Blur (Switch 8). The displacement edges soften, more closely resembling real motion blur.

**Key concepts**: Sine wobble modulates the displacement over time, blur softens displacement for photorealism, moderate settings produce natural handheld look

---

### Exercise 3: Extreme Distortion

<BeforeAfterSlider
  sources={[
    { label: "House", before: rollshut_source1_house, after: rollshut_ex3_s1 },
    { label: "Boat", before: rollshut_source2_boat, after: rollshut_ex3_s2 },
    { label: "Clouds", before: rollshut_source3_clouds, after: rollshut_ex3_s3 },
    { label: "Pattern", before: rollshut_source4_pattern, after: rollshut_ex3_s4 },
    { label: "Woman", before: rollshut_source5_woman, after: rollshut_ex3_s5 },
    { label: "Knit", before: rollshut_source6_knit, after: rollshut_ex3_s6 },
  ]}
/>
*Extreme Distortion — simulated result across source images.*
**Source**: High-contrast graphic content or text — makes distortion clearly visible.

**Objective**: Push the rolling-shutter simulation to its limits for creative distortion effects.

1. **Maximum depth**: Set Roll Depth to 100%. Scanlines at the edge of the frame are displaced by the full 63-pixel buffer depth.
2. **Maximum skew**: Set Skew Rate to 100%. The displacement gradient is at its steepest.
3. **High wobble**: Set Wobble to ~80%. Violent oscillation tears the image apart.
4. **Toggle direction**: Rapidly toggle Direction to observe the skew flipping.
5. **Contrast push**: Increase Contrast to ~70%. Enhances the visual punch of the displaced content.
6. **Blur comparison**: Toggle Blur on and off. Without blur, the displacement produces hard-edged horizontal slicing. With blur, it softens into smeared bands.

**Key concepts**: Extreme settings break the photorealistic simulation into creative distortion territory, blur vs sharp displacement produces different characters

---


## Tips

- **Subtle is realistic**: Roll Depth 20–35% with moderate Wobble produces convincingly natural CMOS rolling-shutter artifacts.
- **Vertical lines reveal skew**: Feed content with strong verticals to make the effect clearly visible.
- **Blur for realism**: Enable Blur to soften displacement edges — real rolling shutters produce motion blur, not hard cuts.
- **Freeze for static composition**: Freeze locks the wobble phase, allowing you to dial in a specific tilt angle.
- **Chain with kinescope**: Rollshut followed by Kinescope creates a convincing lo-fi camera simulation.
- **Direction matters**: Down mode simulates top-to-bottom readout (most common in real cameras); Up mode simulates bottom-to-top.
- **Wobble as LFO**: At high wobble with moderate depth, the effect acts as a rhythmic horizontal oscillator.

---

## Glossary

| Term | Definition |
|------|------------|
| **Circular Buffer** | A fixed-size memory region where the write pointer wraps around to the beginning when it reaches the end, providing a sliding window of recent samples. |
| **CMOS** | Complementary Metal-Oxide-Semiconductor; the sensor technology that produces rolling-shutter artifacts through row-sequential readout. |
| **Distributed RAM** | Small RAM blocks implemented using FPGA logic cells rather than dedicated Block RAM, efficient for shallow buffers like the 64-entry line store. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Global Shutter** | A sensor readout mode where all rows are captured simultaneously, eliminating rolling-shutter skew and wobble. |
| **Manhattan Distance** | Absolute-difference distance metric; not used in Rollshut but related to the general family of scanline-offset techniques. |
| **Rolling Shutter** | A sensor readout mode where each row is captured at a slightly different time, causing motion-dependent skew and wobble. |
| **Scanline Displacement** | Shifting a horizontal row of pixels left or right by a computed offset, the core mechanism of the rolling-shutter simulation. |
| **Sine Wobble** | A sinusoidal modulation applied to the displacement offset over time, simulating camera vibration. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
