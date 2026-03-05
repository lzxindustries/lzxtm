---
draft: true
sidebar_position: 209
slug: /instruments/videomancer/oilslick
title: "Oilslick"
image: /img/instruments/videomancer/oilslick/oilslick_hero_s1.png
description: "Oil on water shimmers because the film is thin enough that light reflecting off its top and bottom surfaces interferes constructively at different wavelengths depending on the film thickness."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import oilslick_control_panel from '/img/instruments/videomancer/oilslick/oilslick_control_panel.png';
import oilslick_source1_field from '/img/instruments/videomancer/oilslick/oilslick_source1_field.png';
import oilslick_source2_house from '/img/instruments/videomancer/oilslick/oilslick_source2_house.png';
import oilslick_source3_collage from '/img/instruments/videomancer/oilslick/oilslick_source3_collage.png';
import oilslick_source4_pattern from '/img/instruments/videomancer/oilslick/oilslick_source4_pattern.png';
import oilslick_source5_man from '/img/instruments/videomancer/oilslick/oilslick_source5_man.png';
import oilslick_source6_berries from '/img/instruments/videomancer/oilslick/oilslick_source6_berries.png';
import oilslick_hero_s1 from '/img/instruments/videomancer/oilslick/oilslick_hero_s1.png';
import oilslick_hero_s2 from '/img/instruments/videomancer/oilslick/oilslick_hero_s2.png';
import oilslick_hero_s3 from '/img/instruments/videomancer/oilslick/oilslick_hero_s3.png';
import oilslick_hero_s4 from '/img/instruments/videomancer/oilslick/oilslick_hero_s4.png';
import oilslick_hero_s5 from '/img/instruments/videomancer/oilslick/oilslick_hero_s5.png';
import oilslick_hero_s6 from '/img/instruments/videomancer/oilslick/oilslick_hero_s6.png';
import oilslick_ex1_s1 from '/img/instruments/videomancer/oilslick/oilslick_ex1_s1.png';
import oilslick_ex1_s2 from '/img/instruments/videomancer/oilslick/oilslick_ex1_s2.png';
import oilslick_ex1_s3 from '/img/instruments/videomancer/oilslick/oilslick_ex1_s3.png';
import oilslick_ex1_s4 from '/img/instruments/videomancer/oilslick/oilslick_ex1_s4.png';
import oilslick_ex1_s5 from '/img/instruments/videomancer/oilslick/oilslick_ex1_s5.png';
import oilslick_ex1_s6 from '/img/instruments/videomancer/oilslick/oilslick_ex1_s6.png';
import oilslick_ex2_s1 from '/img/instruments/videomancer/oilslick/oilslick_ex2_s1.png';
import oilslick_ex2_s2 from '/img/instruments/videomancer/oilslick/oilslick_ex2_s2.png';
import oilslick_ex2_s3 from '/img/instruments/videomancer/oilslick/oilslick_ex2_s3.png';
import oilslick_ex2_s4 from '/img/instruments/videomancer/oilslick/oilslick_ex2_s4.png';
import oilslick_ex2_s5 from '/img/instruments/videomancer/oilslick/oilslick_ex2_s5.png';
import oilslick_ex2_s6 from '/img/instruments/videomancer/oilslick/oilslick_ex2_s6.png';
import oilslick_ex3_s1 from '/img/instruments/videomancer/oilslick/oilslick_ex3_s1.png';
import oilslick_ex3_s2 from '/img/instruments/videomancer/oilslick/oilslick_ex3_s2.png';
import oilslick_ex3_s3 from '/img/instruments/videomancer/oilslick/oilslick_ex3_s3.png';
import oilslick_ex3_s4 from '/img/instruments/videomancer/oilslick/oilslick_ex3_s4.png';
import oilslick_ex3_s5 from '/img/instruments/videomancer/oilslick/oilslick_ex3_s5.png';
import oilslick_ex3_s6 from '/img/instruments/videomancer/oilslick/oilslick_ex3_s6.png';

# Oilslick

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: oilslick_source1_field, after: oilslick_hero_s1 },
    { label: "House", before: oilslick_source2_house, after: oilslick_hero_s2 },
    { label: "Collage", before: oilslick_source3_collage, after: oilslick_hero_s3 },
    { label: "Pattern", before: oilslick_source4_pattern, after: oilslick_hero_s4 },
    { label: "Man", before: oilslick_source5_man, after: oilslick_hero_s5 },
    { label: "Berries", before: oilslick_source6_berries, after: oilslick_hero_s6 },
  ]}
/>
*Oilslick generating vivid position-dependent rainbow iridescence patterns over a live video source through DDS-based thin-film interference simulation.*

---

## Overview

Oil on water shimmers because the film is thin enough that light reflecting off its top and bottom surfaces interferes constructively at different wavelengths depending on the film thickness. Thicker regions reflect longer wavelengths; thinner regions reflect shorter ones. The result is a continuously varying rainbow that shifts as the viewing angle changes.

Oilslick recreates this phenomenon digitally. It computes a per-pixel "thickness" value from horizontal and vertical position counters, sums them with an animation phase accumulator, and extracts triangle-wave UV modulations at two different phase offsets. The two offset channels produce the U and V chrominance deviations that create the characteristic oil-on-water rainbow. The source luminance passes through unchanged — only the color is replaced or modulated.

The spatial frequency of the color pattern is independently controllable for horizontal and vertical axes, producing everything from fine ripples to broad washes. An animation accumulator sweeps the pattern smoothly over time. A phase separation control determines how different the U and V extractions are — at zero offset they track identically and produce monochrome tinting; at high offset they diverge into full spectral iridescence.

---

## Quick Start

1. **Pot 6 is the mix**: The wet/dry crossfade is on Pot 6 (not the fader). The fader has no effect in this program.
2. **Toggles 10 and 11 are unused**: Only three toggles (7–9) are connected in the VHDL. The remaining two toggle positions and the fader have no function.
3. **Phase separation is the color key**: At Thickness Var = 0, the effect produces single-hue tinting. Increase it to unlock the full spectral rainbow.

---

## Background

### Thin-Film Interference

When white light hits a thin transparent layer (oil, soap bubble, anti-reflective coating), part reflects off the top surface and part off the bottom. The two reflected waves travel different distances — equal to twice the film thickness — and may constructively or destructively interfere depending on the wavelength. For a given thickness, some wavelengths add (producing vivid color) while others cancel. Varying the thickness across the surface produces the rainbow banding characteristic of oil slicks.

### Direct Digital Synthesis

DDS generates a smoothly varying periodic waveform by accumulating a phase value on every clock cycle and mapping the accumulated phase to an output waveform. In Oilslick's case, the "clock" is horizontal or vertical pixel position rather than time, and the output waveform is a triangle wave rather than a sine. The phase increment per pixel is controlled by the spatial frequency parameters, and an additional animation phase accumulates once per video frame to create temporal motion.

### Triangle Wave Extraction

A triangle wave is the simplest periodic waveform that can be extracted from a binary counter: if the MSB is zero, the remaining bits form an ascending ramp; if the MSB is one, the remaining bits are inverted to create a descending ramp. The result is a symmetric triangular waveform that spans half the counter range. Oilslick extracts two such triangle waves from different bit windows of the same thickness value, producing phase-offset UV modulations.

### UV Color Space and Interference Hue

In YUV, neutral gray sits at U = 512, V = 512 (10-bit midpoint). Deviations from center encode color: positive U is blue-ish, negative U is yellow-ish; positive V is red-ish, negative V is cyan-ish. By applying triangle-wave deviations at different phases to U and V simultaneously, Oilslick traces a path through color space that sweeps through the visible spectrum — mimicking the spectral sequence produced by real thin-film interference.

### XOR Pattern Modulation

The optional XOR pattern mode takes the computed thickness value and XOR-combines it with a shifted version of the horizontal position counter. XOR creates a fractal-like diagonal interference pattern that breaks the otherwise smooth linear gradients into complex cellular structures, similar to the moire patterns visible on real oil films when surface tension creates irregular thickness boundaries.


---

## Signal Flow

Y Channel → UV Channels → Animation → Wet/Dry Mix → Sync

```
Input Video (YUV 4:4:4, 10-bit)
│
├── Y Channel ─────────────────────────────────────────────────
│   └─ Pass-through (unchanged)
│
├── UV Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Position Counters     (h_count, v_count per pixel/line)
│   ├─ 2. Frequency Scaling     (shift h/v counts by pot-controlled amount)
│   ├─ 3. Thickness Sum         (h_scaled + v_scaled + phase_accum)
│   ├─     └─ XOR modulation    (optional: XOR with shifted h_count)
│   ├─ 4. Triangle Extraction   (fold 10-bit windows → 9-bit triangles)
│   │      ├─ U window: thickness[9:0]
│   │      └─ V window: thickness[9+offset : offset]  (phase separated)
│   ├─ 5. Center + Scale        (wave − 256, then right-shift by intensity)
│   ├─ 6. Color Mode            (optional: swap U ↔ V deltas)
│   ├─ 7. Compose               (add deltas to 512 center or to source UV)
│   └─ 8. Clamp                 (0..1023)
│
├── Animation ─────────────────────────────────────────────────
│   └─ Phase accumulator        (+anim_speed per frame, wraps at 16 bits)
│
├── Wet/Dry Mix ───────────────────────────────────────────────
│   └─ 3× interpolator_u       (source ↔ processed, controlled by Mix pot)
│
└── Sync ──────────────────────────────────────────────────────
    └─ Delayed pass-through     (hsync, vsync, field, 8-clock pipeline)
```

The pipeline separates spatial computation from color composition. Stages 1–3 compute a single 16-bit "thickness" value per pixel using only position and animation state — this value is independent of the input video content. Stages 4–8 then extract color modulations from that thickness and compose them with (or replace) the source chrominance. Source luminance passes through unchanged, so the interference effect is purely chromatic — it tints the image with position-dependent rainbow colors while preserving all brightness detail.

The phase separation mechanism is the key to spectral variety. When the V-channel window offset (controlled by Thickness Var) matches the U-channel window, both channels receive the same triangle wave and the output is a single hue that varies with position. As the offset increases, U and V receive progressively different phases of the thickness waveform, sweeping through the full gamut of YUV chrominance combinations and producing multicolored interference fringes.

---

## Parameter Reference

<img src={oilslick_control_panel} alt="Videomancer front panel with Oilslick loaded"/>
*Videomancer's front panel with Oilslick active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Wave Frq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the horizontal spatial frequency of the interference pattern. The 10-bit register value is quantized to one of eight shift amounts (0 through 7) applied to the horizontal position counter before it enters the thickness sum. At shift 0 the pattern changes very slowly across the screen — broad, gentle color washes. At shift 7 every pixel accumulates 128× faster, producing tight vertical color fringes. The quantized step behavior means the frequency jumps between octaves rather than sweeping continuously, producing distinct pattern modes at each pot position.

---

#### Knob 2 — Shift Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At low values, color bands are tall horizontal stripes spanning many scan lines. At high values, the bands compress to single-line fringes. Combined with Wave Freq H, the two axes define the angle and density of the interference pattern: equal settings produce diagonal bands; unequal settings produce horizontal or vertical dominance. Internally, controls the vertical spatial frequency using the same shift-amount quantization as Wave Freq H, but applied to the vertical position counter.

---

#### Knob 3 — Saturate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the intensity of the UV color modulation. The 10-bit register is mapped to an attenuation shift of 0 to 3 bits applied to the triangle-wave delta before composition. At minimum (shift 3), the UV deviation is divided by 8, producing very subtle pastel tinting barely visible over the source. At maximum (shift 0), the full triangle-wave amplitude drives the UV channels, producing vivid saturated rainbows. The four-level quantization creates distinct saturation bands rather than a smooth ramp.

---

#### Knob 4 — Pattern
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the DDS animation rate. The register value is added to a 16-bit phase accumulator once per video frame. At zero the pattern is static. At low values the rainbow drifts slowly across the image like oil on gently flowing water. At maximum the pattern races through complete color cycles in a few frames. Because the accumulator wraps at 16 bits, the animation is seamlessly periodic — the pattern always returns to its starting state after a fixed number of frames determined by the speed setting.

---

#### Knob 5 — Film Thk
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the phase separation between the U and V triangle-wave extractions. The top three bits of the register select which 10-bit window of the 16-bit thickness value feeds the V channel (the U channel always reads bits 9:0). At offset 0, both channels extract the same window and produce identical modulation — the result is a single varying hue (monochromatic tint that shifts with position). As the offset increases, the V channel reads progressively higher bit windows of the thickness, creating a growing phase difference that sweeps U and V through different parts of their respective triangle waves simultaneously. This is what produces the spectral rainbow — the wider the separation, the more distinct colors appear between adjacent pixels.

---

#### Knob 6 — Blend
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Wet/dry crossfade amount. This register directly drives the interpolation parameter of all three interpolator_u instances. At 0 the output is pure dry (original input). At 1023 the output is pure wet (interference-colored). Intermediate values blend between the two, allowing subtle chromatic overlay at low mix or full replacement at high mix. Note that this control is on Pot 6 (not the fader), so the primary effect intensity is adjusted by knob rather than slider.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Shape** | Radial | Random |
| **8 — Palette** | Rainbow | Subtle |
| **9 — React** | Off | Luma |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Three toggle bits (7–9) control independent aspects of the color composition: spatial pattern type, UV channel routing, and source blending. Toggles 10 and 11 are declared in the TOML parameter set but are not connected to any processing logic in the VHDL — they have no effect on the output. The fader (register 7) is likewise not connected. All mix control is through Pot 6.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Not connected in the current VHDL implementation. The fader register (register 7) is not read by the processing pipeline. All wet/dry mix control is through Pot 6. Moving the fader has no effect on the output.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore Oilslick's spatial interference patterns from simple color washes through animated spectral effects to complex textured overlays. Each builds on the previous, gradually revealing the interactions between frequency, phase separation, pattern mode, and blending.

### Exercise 1: Static Rainbow Wash

<BeforeAfterSlider
  sources={[
    { label: "Field", before: oilslick_source1_field, after: oilslick_ex1_s1 },
    { label: "House", before: oilslick_source2_house, after: oilslick_ex1_s2 },
    { label: "Collage", before: oilslick_source3_collage, after: oilslick_ex1_s3 },
    { label: "Pattern", before: oilslick_source4_pattern, after: oilslick_ex1_s4 },
    { label: "Man", before: oilslick_source5_man, after: oilslick_ex1_s5 },
    { label: "Berries", before: oilslick_source6_berries, after: oilslick_ex1_s6 },
  ]}
/>
*Static Rainbow Wash — simulated result across source images.*
**Source**: A grayscale gradient ramp or neutral gray card — any low-chroma source that lets the interference colors stand out clearly.

**What You'll Create**: Understand how horizontal and vertical frequencies define the interference band geometry, and how phase separation creates spectral color.

1. **Single axis**: Set Wave Freq H to ~60% (shift 4). Leave Wave Freq V at 0. A series of vertical color bands appears — the color changes with horizontal position.
2. **Add vertical**: Increase Wave Freq V to ~60%. The bands tilt diagonally as both axes contribute to the thickness sum.
3. **Phase separation**: Start with Thickness Var at 0 — the image shows a single shifting hue. Slowly increase it. At moderate values, two or three distinct colors appear in the pattern. At high values, a full spectral rainbow emerges.
4. **Intensity**: Sweep Color Intensity from minimum to maximum. Watch the pattern go from barely-visible tinting to vivid saturated rainbows.

**Key concepts**: Spatial frequency controls band spacing, phase separation creates spectral variety, color intensity scales UV amplitude

---

### Exercise 2: Animated Oil Shimmer

<BeforeAfterSlider
  sources={[
    { label: "Field", before: oilslick_source1_field, after: oilslick_ex2_s1 },
    { label: "House", before: oilslick_source2_house, after: oilslick_ex2_s2 },
    { label: "Collage", before: oilslick_source3_collage, after: oilslick_ex2_s3 },
    { label: "Pattern", before: oilslick_source4_pattern, after: oilslick_ex2_s4 },
    { label: "Man", before: oilslick_source5_man, after: oilslick_ex2_s5 },
    { label: "Berries", before: oilslick_source6_berries, after: oilslick_ex2_s6 },
  ]}
/>
*Animated Oil Shimmer — simulated result across source images.*
**Source**: A live camera feed or recorded footage with varied brightness — faces, landscapes, or abstract shapes work well.

**What You'll Create**: Explore animation, source blending, and color swap to create evolving chromatic overlays over live video.

1. **Animate**: From the Exercise 1 pattern, increase Anim Speed to ~30%. The rainbow drifts gently across the image.
2. **Source blend**: Enable Source Blend (Toggle 9). The interference colors now tint the source rather than replacing its chroma. The original colors show through beneath the rainbow.
3. **Color swap**: Toggle Color Mode (Toggle 8). The palette rotates — warm-dominated hues become cool-dominated and vice versa. Toggle it back and forth to compare.
4. **Speed sweep**: Increase Anim Speed toward 100%. The pattern races through color cycles. Find a speed that creates a gentle, organic shimmer.

**Key concepts**: DDS animation creates seamless periodic motion, Source Blend preserves original chroma, Color Mode rotates the interference palette

---

### Exercise 3: Crystalline XOR Textures

<BeforeAfterSlider
  sources={[
    { label: "Field", before: oilslick_source1_field, after: oilslick_ex3_s1 },
    { label: "House", before: oilslick_source2_house, after: oilslick_ex3_s2 },
    { label: "Collage", before: oilslick_source3_collage, after: oilslick_ex3_s3 },
    { label: "Pattern", before: oilslick_source4_pattern, after: oilslick_ex3_s4 },
    { label: "Man", before: oilslick_source5_man, after: oilslick_ex3_s5 },
    { label: "Berries", before: oilslick_source6_berries, after: oilslick_ex3_s6 },
  ]}
/>
*Crystalline XOR Textures — simulated result across source images.*
**Source**: High-contrast footage — sharp edges, text, or geometric patterns that interact visually with the XOR lattice.

**What You'll Create**: Combine XOR pattern mode with high frequencies to create stained-glass and crystalline interference patterns.

1. **XOR mode**: Enable Pattern Mode (Toggle 7). The smooth gradient bands shatter into angular, cellular structures.
2. **High frequency**: Increase Wave Freq H to maximum (~100%). The XOR pattern becomes a fine mosaic of colored cells.
3. **Slow animation**: Set Anim Speed to ~15%. The cellular pattern crawls and morphs, creating the appearance of a stained-glass window drifting over the source.
4. **Blend balance**: Reduce Mix (Pot 6) to ~50%. The original image shows through at half intensity beneath the crystalline texture.
5. **Phase extremes**: Sweep Thickness Var from 0 to 100%. At zero, the XOR pattern is monochromatic; at maximum, each cell contains a different spectral color.

**Key concepts**: XOR creates fractal-like spatial patterns, high frequency + XOR = stained-glass mosaic, Mix pot controls overlay strength

---


## Tips

- **Frequency is octave-quantized**: The spatial frequency controls jump between 8 discrete octave levels rather than sweeping smoothly. Use this to dial in specific pattern densities.
- **Source Blend for subtle chromatic overlay**: Enable Source Blend (Toggle 9) to add iridescent color on top of existing video chroma rather than replacing it.
- **XOR for texture**: Pattern Mode transforms smooth washes into crystalline cellular patterns. Combine with high frequency for fine stained-glass effects.
- **Color Mode doubles your palette**: Swapping U and V rotates the entire color scheme by ~90°, giving two palettes per spatial configuration.
- **Feedback loops**: Routing output back to input stacks interference patterns, creating increasingly saturated and complex color structures with each pass.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation BT.601; the color space standard used by Videomancer's YUV pipeline, defining the matrix for converting between RGB and YUV. |
| **Chrominance** | The color-difference components (U and V) of a YUV signal, encoding hue and saturation relative to the neutral axis. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms by incrementing a phase accumulator and mapping the result to an output function. |
| **Iridescence** | The phenomenon where apparent color changes with viewing angle or surface geometry, caused by thin-film interference or diffraction. |
| **LUT** | Look-Up Table; a pre-computed array that maps input values to output values, used in FPGA for function evaluation. |
| **Phase Accumulator** | A register that increments by a configurable step on each cycle, wrapping at its maximum value to create a repeating ramp. |
| **Thin-Film Interference** | Constructive and destructive interference of light waves reflecting off the top and bottom surfaces of a thin transparent layer. |
| **Triangle Wave** | A periodic waveform with linear ascending and descending ramps, produced by folding a sawtooth ramp at its midpoint. |
| **XOR** | Exclusive OR; a bitwise operation that outputs 1 when inputs differ, used here to create fractal-like spatial modulation patterns. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
