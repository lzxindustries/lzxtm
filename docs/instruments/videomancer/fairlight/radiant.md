---
draft: true
sidebar_position: 211
slug: /instruments/videomancer/radiant
title: "Radiant"
image: /img/instruments/videomancer/radiant/radiant_hero.png
description: "Radiant generates concentric colored rings that radiate outward from an adjustable center point, creating a tunnel-like wash of color that composites wi..."
---

import radiant_before_after from '/img/instruments/videomancer/radiant/radiant_before_after.png';
import radiant_control_panel from '/img/instruments/videomancer/radiant/radiant_control_panel.png';
import radiant_exercise1_result from '/img/instruments/videomancer/radiant/radiant_exercise1_result.png';
import radiant_exercise2_result from '/img/instruments/videomancer/radiant/radiant_exercise2_result.png';
import radiant_exercise3_result from '/img/instruments/videomancer/radiant/radiant_exercise3_result.png';
import radiant_hero from '/img/instruments/videomancer/radiant/radiant_hero.png';
import radiant_source1_kodim15 from '/img/instruments/videomancer/radiant/radiant_source1_kodim15.png';
import radiant_source2_kodim01 from '/img/instruments/videomancer/radiant/radiant_source2_kodim01.png';
import radiant_source3_kodim01_bw from '/img/instruments/videomancer/radiant/radiant_source3_kodim01_bw.png';

# Radiant

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={radiant_hero} alt="Radiant hero image"/>
*Radiant projecting concentric expanding color rings from a movable center point, composited over live video via additive blending.*
<img src={radiant_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Radiant applied.*

---

## Overview

Radiant generates concentric colored rings that radiate outward from an adjustable center point, creating a tunnel-like wash of color that composites with the incoming video signal. The effect is inspired by the Fairlight CVI's color wash modes — procedural gradient generation that interacts with live imagery to produce color fields, spotlight effects, and pulsing radial animations.

The program computes an octagonal distance approximation from each pixel to the center point, then maps that distance through a scrolling color palette to determine ring hue and brightness. The distance-to-color mapping wraps cyclically, producing repeating bands of color that appear to expand or contract when the frame scroll DDS advances. Three `interpolator_u` instances handle the wet/dry crossfade. The entire pipeline uses zero BRAM — all color generation is procedural, computed per-pixel from distance, hue wheel position, and saturation scaling.

At default settings Radiant produces gently colored concentric rings centered on the frame. Orbit mode animates the center in a quasi-Lissajous triangular-wave pattern. Auto Hue mode slowly rotates the palette over time. The Multiply toggle switches between additive compositing (rings add brightness to the source) and gated multiplication (rings modulate the source brightness), producing either luminous overlays or shadow-like vignettes.

---

## Background

### Octagonal Distance Approximation

Computing true Euclidean distance ($\sqrt{dx^2 + dy^2}$) requires a multiplier and square root — expensive on an iCE40. Radiant uses an octagonal approximation: $d \approx \max(|dx|, |dy|) + \frac{3}{8} \min(|dx|, |dy|)$. Specifically, the VHDL computes `max + min/4 + min/8`, which equals `max + 3*min/8`. This produces an octagon-shaped equidistant contour rather than a circle, but the visual difference is subtle, especially when the rings are scrolling. The approximation requires only addition and bit-shifting.

### Hue Wheel Color Generation

The ring color is generated from a hue index that wraps cyclically through the 10-bit range. The ring hue value is split into U and V components with a 90-degree (256-count) phase offset: U derives from `hue - 512` and V from `(hue + 256) - 512`. This produces a simple two-channel color wheel where the hue rotates through complementary color pairs. Saturation is applied by shifting U and V offsets toward zero via a variable right-shift (0–3 positions), controlled by the upper 2 bits of the Saturation register. The Value pot sets ring luma brightness directly.

### DDS Frame Scrolling

A 16-bit Direct Digital Synthesis accumulator advances by `speed << 4` each frame at vertical sync. The upper 10 bits of this accumulator become the frame scroll offset added to the ring index. Faster speed values cause the rings to expand more rapidly. Because the accumulator wraps at 16 bits, the scroll is periodic — after enough frames, the pattern repeats. The expansion rate is proportional to the Speed pot value.

### Triangular-Wave Orbit

When Orbit mode is active, two independent 16-bit DDS accumulators advance at slightly different rates each frame (speed + 32 for X, speed + 48 for Y), creating a quasi-Lissajous pattern. Each accumulator is converted to a triangular wave by inverting its lower bits when the MSB is set. The resulting 10-bit offsets are added to the Center X and Center Y pot values, causing the ring center to meander across the frame in a smooth, non-repeating figure.

### Composite Modes

Radiant offers two compositing strategies. **Additive** mode adds the ring Y to the input Y with clamping, and adds ring U/V to input U/V with a midpoint offset (ring chroma is centered at 512, so the operation is `input + ring - 512` clamped to [0, 1023]). **Multiply** mode uses the ring Y value to gate the input brightness via a variable right-shift (0–7 positions derived from the ring brightness), and averages ring and input chroma. Additive produces luminous overlays; multiply produces vignette and shadow effects.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Sync + Counters + DDS ────────────
│   ├─ Capture Y, U, V
│   ├─ Sync edge detection (hsync_fall, vsync_fall)
│   ├─ Pixel/line counters → pixel_x [10-bit], pixel_y [10-bit]
│   ├─ Frame scroll DDS: acc += speed << 4 at vsync
│   ├─ Orbit DDS: x_acc += speed + 32, y_acc += speed + 48
│   │   └─ Triangular wave → orbit offsets
│   ├─ Hue auto-rotation DDS: hue_acc += 2 at vsync
│   └─ Effective center = pot + orbit_offset (wrapping add)
│
├── Stage 2: Distance Computation ──────────────────────────────
│   ├─ abs_dx = |pixel_x - eff_center_x|
│   ├─ abs_dy = |pixel_y - eff_center_y|
│   ├─ max_d, min_d = sort(abs_dx, abs_dy)
│   └─ radial_dist = max_d + min_d/4 + min_d/8  (octagonal)
│
├── Stage 3: Ring Color Generation ─────────────────────────────
│   ├─ ring_index = dist[wide?>>1:full] + frame_scroll + eff_hue
│   ├─ ring_y = Value pot (direct)
│   ├─ sat_shift = 3 - saturation[9:8]
│   ├─ U_offset = (ring_hue - 512) >> sat_shift + 512
│   └─ V_offset = ((ring_hue + 256) - 512) >> sat_shift + 512
│
├── Stage 4: Composite ─────────────────────────────────────────
│   ├─ Additive mode:
│   │   ├─ comp_y = clamp(y_in + ring_y)
│   │   ├─ comp_u = clamp(u_in + ring_u - 512)
│   │   └─ comp_v = clamp(v_in + ring_v - 512)
│   └─ Multiply mode:
│       ├─ atten = 7 - ring_y[9:7]
│       ├─ comp_y = y_in >> atten
│       ├─ comp_u = (u_in + ring_u) / 2
│       └─ comp_v = (v_in + ring_v) / 2
│
├── Mix (3× interpolator_u, 4 clocks) ─────────────────────────
│   └─ lerp(dry, wet, mix_amount) per channel
│
└── Output ─────────────────────────────────────────────────────
    └─ bypass ? delayed_input : mixed_output
```

The key interaction is the additive ring index construction: `distance + frame_scroll + effective_hue`. Distance provides the spatial structure (concentric rings), frame scroll provides temporal animation (expanding/contracting), and hue provides the color starting point. Because all three are added modulo 1024, the rings seamlessly wrap in all three domains — spatially at the frame edges, temporally over the DDS period, and chromatically through the full color wheel. The Wide Ring toggle halves the distance contribution by right-shifting it one bit, which doubles the apparent ring width.

---

## Parameter Reference

<img src={radiant_control_panel} alt="Videomancer front panel with Radiant loaded"/>
*Videomancer's front panel with Radiant active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the ring expansion speed — how fast the concentric rings appear to move outward or inward. The 10-bit register value is left-shifted by 4 bits and added to a 16-bit DDS accumulator once per frame at vsync. At zero, the rings are static. At maximum, they scroll rapidly. The same speed value also influences the orbit rate when Orbit mode is enabled, as it is added to fixed offsets for the X and Y orbit accumulators.

---

#### Knob 2 — Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the base hue of the ring color palette. The 10-bit value rotates the starting position on the color wheel. At 0 the rings begin from one end of the hue cycle; sweeping to 1023 rotates through the full spectrum. When Auto Hue is enabled, this value is summed with a slowly incrementing DDS accumulator, so the pot sets the starting point of an automatically rotating palette.

---

#### Knob 3 — Saturaton
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the color saturation of the generated rings. The upper two bits of the 10-bit register select a right-shift amount (0–3) applied to the U and V chroma offsets. At maximum saturation (shift = 0), ring colors are vivid. At minimum (shift = 3), U and V offsets are divided by 8, producing near-neutral rings that appear as luminance-only bands. Intermediate positions provide increasingly pastel coloring.

---

#### Knob 4 — Value
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Sets the brightness (Y value) of the ring signal. This value is used directly as the ring luma in additive mode and as the attenuation selector in multiply mode. In additive mode, higher values produce brighter rings that wash out the source. In multiply mode, the value controls how much the ring darkens the source — at maximum the ring passes the source through nearly unattenuated; at minimum it crushes the signal to black.

---

#### Knob 5 — Center X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the horizontal position of the ring center. At 512 (midpoint) the center is approximately at the middle of the frame. Lower values move it left; higher values move it right. The 10-bit value maps to the same coordinate space as the pixel counter (roughly 0–1023 across the active picture width). When Orbit mode is active, a triangular-wave DDS offset is added to this value, so the pot sets the center of the orbit path.

---

#### Knob 6 — Center Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the vertical position of the ring center. At 512 the center is approximately mid-frame. Lower values move it upward; higher values move it downward. Combined with Center X, this positions the origin point from which all rings radiate. Like Center X, the orbit DDS adds a triangular-wave offset when Orbit mode is enabled.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Orbit** | Off | On |
| **8 — Auto Hue** | Off | On |
| **9 — Multiply** | Add | Mult |
| **10 — Wide Ring** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control animation, color behavior, compositing style, and ring geometry. Orbit and Auto Hue enable two independent DDS-driven animations (center position and palette rotation). Multiply switches the compositing math. Wide Ring doubles the ring width by halving the distance contribution. Bypass passes the input through unprocessed.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the composited ring signal and the original input. At 0 the output is entirely dry (original video); at 1023 it is entirely wet (full ring overlay). Three parallel `interpolator_u` instances handle the crossfade on Y, U, and V independently. Intermediate positions create semi-transparent ring overlays.

---

## Guided Exercises

These exercises explore Radiant's core capabilities — from static centered gradients to animated orbiting rings to multiplicative video gating.

### Exercise 1: Centered Rainbow Spotlight

<img src={radiant_exercise1_result} alt="Centered Rainbow Spotlight result"/>
*Centered Rainbow Spotlight — simulated result across source images.*
**Source**: A moderately bright video source with recognizable content — a face, an object, or a graphic with visible structure.

**Objective**: Create a static bulls-eye of concentric rainbow rings centered on the frame, additively overlaid on the source video.

1. Set Speed to 0% for static rings
2. Set Hue to 0° for default palette starting point
3. Set Saturaton to 75% for vivid ring colors
4. Set Value to 60% for moderate ring brightness
5. Set Center X to 50% to center horizontally
6. Set Center Y to 50% to center vertically
7. Switch Orbit to Off for static center
8. Switch Auto Hue to Off for fixed palette
9. Switch Multiply to Add for additive compositing
10. Switch Wide Ring to Off for tight rings
11. Confirm Bypass is Off
12. Set Mix to 100% for full effect

**Key concepts**: With Speed at zero the rings are frozen in place, revealing the octagonal distance approximation as a subtle octagonal faceting of the ring contours. The additive composite brightens the source wherever ring luma is nonzero.

---

### Exercise 2: Orbiting Color Tunnel

<img src={radiant_exercise2_result} alt="Orbiting Color Tunnel result"/>
*Orbiting Color Tunnel — simulated result across source images.*
**Source**: A dark or low-contrast video source — a dimly lit scene or abstract dark texture that will serve as a backdrop for the vivid ring overlay.

**Objective**: Create an animated color tunnel with the ring center orbiting across the frame and the palette slowly rotating through the spectrum.

1. Set Speed to 40% for moderate expansion rate
2. Set Hue to 180° for starting midway through palette
3. Set Saturaton to 100% for maximum color intensity
4. Set Value to 80% for bright luminous rings
5. Set Center X to 50% as orbit center
6. Set Center Y to 50% as orbit center
7. Switch Orbit to On for animated center
8. Switch Auto Hue to On for palette rotation
9. Switch Multiply to Add for additive blending
10. Switch Wide Ring to On for broad ring bands
11. Confirm Bypass is Off
12. Set Mix to 85% for slight source visibility

**Key concepts**: The quasi-Lissajous orbit creates asymmetric ring patterns as the center moves — rings bunch up on one side of the frame and spread out on the other. Auto Hue ensures the color palette evolves continuously. Wide Ring mode makes the bands broad enough to see the hue gradient within each ring.

---

### Exercise 3: Vignette Gating

<img src={radiant_exercise3_result} alt="Vignette Gating result"/>
*Vignette Gating — simulated result across source images.*
**Source**: A well-lit, colorful video source with good dynamic range — the multiply mode will selectively darken regions, so the source needs visible brightness variation.

**Objective**: Use multiply compositing mode to create a spotlight/vignette effect where the ring pattern selectively attenuates the source video.

1. Set Speed to 10% for slow, subtle ring expansion
2. Set Hue to 90° for a warm color bias
3. Set Saturaton to 30% for subdued, near-neutral ring tint
4. Set Value to 70% for moderate gating depth
5. Set Center X to 50% to center the spotlight
6. Set Center Y to 40% to position slightly above center
7. Switch Orbit to Off for stable center position
8. Switch Auto Hue to Off for consistent coloring
9. Switch Multiply to Mult for gated multiplication
10. Switch Wide Ring to On for broad attenuation bands
11. Confirm Bypass is Off
12. Set Mix to 100% for full gating effect

**Key concepts**: In multiply mode, the ring Y value controls brightness attenuation via right-shift — bright ring regions pass the source through, dark ring regions crush it toward black. With low saturation, the ring's chroma influence is subtle, producing a nearly monochrome vignette that gradually reveals and conceals the source.

---


## Tips

- **Octagonal, not circular**: The rings are slightly octagonal due to the `max + 3*min/8` distance approximation — look for the faceting when rings are large and static.
- **Speed drives orbit too**: The orbit rate is linked to the Speed pot, so faster expansion also means faster center movement when Orbit is enabled.
- **Saturation has four levels**: The sat_shift is derived from 2 bits, so saturation changes in discrete steps rather than continuously — there are effectively four saturation positions.
- **Multiply darkens**: In multiply mode, the ring attenuates the source rather than adding to it — low Value settings crush the image to black at the ring center.
- **Auto Hue is slow**: The fixed increment of 2 per frame means full palette rotation takes many seconds — be patient when evaluating color cycling.
- **Orbit is quasi-random**: The X and Y orbit rates differ by design (offsets of 32 vs 48), so the center path never repeats exactly within a typical viewing session.
- **Wide Ring halves density**: Enabling Wide Ring right-shifts the distance, doubling apparent ring width — useful for broad color washes rather than tight interference patterns.
- **Additive clips to white**: In additive mode with high Value, source highlights will clip to peak white — reduce Value or Mix to preserve source dynamic range.
