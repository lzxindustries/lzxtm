---
draft: true
sidebar_position: 78
slug: /instruments/videomancer/delirium
title: "Delirium"
image: /img/instruments/videomancer/delirium/delirium_hero_s1.png
description: "Every line of a video image is a row of numbers — brightness and color values marching left to right across the screen."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import delirium_source1_fruit from '/img/instruments/videomancer/delirium/delirium_source1_fruit.png';
import delirium_source2_field from '/img/instruments/videomancer/delirium/delirium_source2_field.png';
import delirium_source3_collage from '/img/instruments/videomancer/delirium/delirium_source3_collage.png';
import delirium_source4_pattern from '/img/instruments/videomancer/delirium/delirium_source4_pattern.png';
import delirium_source5_girl from '/img/instruments/videomancer/delirium/delirium_source5_girl.png';
import delirium_source6_wood from '/img/instruments/videomancer/delirium/delirium_source6_wood.png';
import delirium_hero_s1 from '/img/instruments/videomancer/delirium/delirium_hero_s1.png';
import delirium_hero_s2 from '/img/instruments/videomancer/delirium/delirium_hero_s2.png';
import delirium_hero_s3 from '/img/instruments/videomancer/delirium/delirium_hero_s3.png';
import delirium_hero_s4 from '/img/instruments/videomancer/delirium/delirium_hero_s4.png';
import delirium_hero_s5 from '/img/instruments/videomancer/delirium/delirium_hero_s5.png';
import delirium_hero_s6 from '/img/instruments/videomancer/delirium/delirium_hero_s6.png';
import delirium_ex1_s1 from '/img/instruments/videomancer/delirium/delirium_ex1_s1.png';
import delirium_ex1_s2 from '/img/instruments/videomancer/delirium/delirium_ex1_s2.png';
import delirium_ex1_s3 from '/img/instruments/videomancer/delirium/delirium_ex1_s3.png';
import delirium_ex1_s4 from '/img/instruments/videomancer/delirium/delirium_ex1_s4.png';
import delirium_ex1_s5 from '/img/instruments/videomancer/delirium/delirium_ex1_s5.png';
import delirium_ex1_s6 from '/img/instruments/videomancer/delirium/delirium_ex1_s6.png';
import delirium_ex2_s1 from '/img/instruments/videomancer/delirium/delirium_ex2_s1.png';
import delirium_ex2_s2 from '/img/instruments/videomancer/delirium/delirium_ex2_s2.png';
import delirium_ex2_s3 from '/img/instruments/videomancer/delirium/delirium_ex2_s3.png';
import delirium_ex2_s4 from '/img/instruments/videomancer/delirium/delirium_ex2_s4.png';
import delirium_ex2_s5 from '/img/instruments/videomancer/delirium/delirium_ex2_s5.png';
import delirium_ex2_s6 from '/img/instruments/videomancer/delirium/delirium_ex2_s6.png';
import delirium_ex3_s1 from '/img/instruments/videomancer/delirium/delirium_ex3_s1.png';
import delirium_ex3_s2 from '/img/instruments/videomancer/delirium/delirium_ex3_s2.png';
import delirium_ex3_s3 from '/img/instruments/videomancer/delirium/delirium_ex3_s3.png';
import delirium_ex3_s4 from '/img/instruments/videomancer/delirium/delirium_ex3_s4.png';
import delirium_ex3_s5 from '/img/instruments/videomancer/delirium/delirium_ex3_s5.png';
import delirium_ex3_s6 from '/img/instruments/videomancer/delirium/delirium_ex3_s6.png';

# Delirium

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: delirium_source1_fruit, after: delirium_hero_s1 },
    { label: "Field", before: delirium_source2_field, after: delirium_hero_s2 },
    { label: "Collage", before: delirium_source3_collage, after: delirium_hero_s3 },
    { label: "Pattern", before: delirium_source4_pattern, after: delirium_hero_s4 },
    { label: "Girl", before: delirium_source5_girl, after: delirium_hero_s5 },
    { label: "Wood", before: delirium_source6_wood, after: delirium_hero_s6 },
  ]}
/>
*Delirium applying cascaded sinusoidal distortion to produce psychedelic scanline warping reminiscent of classic 16-bit battle screen effects.*

---

## Overview

Every line of a video image is a row of numbers — brightness and color values marching left to right across the screen. What happens when you slide each row sideways by a different amount, and the amount follows a sine wave? The image bends. Curves ripple through it like heat shimmer off asphalt, or like the surface of a pool viewed from below. Delirium does exactly this, with two independent distortion layers that can cascade into each other.

The name captures the visual experience: at high amplitudes and mismatched frequencies, the image dissolves into a churning, hallucinatory warp field where subject and background lose all spatial coherence. The program is a direct descendant of the battle background distortion system from *EarthBound* (Mother 2, 1994), which applied per-scanline sinusoidal offsets to create its iconic psychedelic combat screens. Delirium extends the concept with independent dual-layer distortion, three displacement modes per layer, variable-speed animation, and a cascade architecture that lets one warp field feed into another.

At gentle settings — low amplitude, moderate frequency — Delirium produces subtle undulating waves suitable for underwater or dream sequences. At extreme settings — high amplitude on both layers with mismatched frequencies — the image becomes an abstract, constantly shifting topology where recognizable content appears only in momentary glimpses between wave peaks.

---

## Background

### EarthBound Battle Backgrounds

The Super Nintendo game *EarthBound* (Mother 2, HAL Laboratory, 1994) is famous for its psychedelic battle backgrounds — swirling, rippling, color-cycling fields that played behind every enemy encounter. The technical secret was a per-scanline horizontal offset register in the SNES PPU (Picture Processing Unit), known as Mode 7 HDMA. By programming a DMA channel to write a different horizontal scroll value to each scanline during the vertical blank, the hardware could warp a flat tile map into undulating waves, spirals, and tunnel effects — all without any CPU intervention during the active frame.

The key insight was that a simple sine function applied to horizontal scroll per scanline produces compelling organic distortion. Two sine functions with different frequencies and phase velocities create interference patterns that appear to ripple and breathe. EarthBound's effect designers composed dozens of distinct battle backgrounds by varying amplitude, frequency, speed, and palette cycling parameters. Delirium brings this technique to analog and HDMI video in real time, applying the same per-scanline sinusoidal offset to live camera feeds rather than tile maps.

### Scanimate and Analog Warp Heritage

Long before the SNES, analog video synthesizers achieved similar effects through entirely different means. The Scanimate system (Computer Image Corporation, 1969) used analog deflection circuits to warp raster scan trajectories in real time. By modulating the horizontal deflection with a sine wave synchronized to the vertical scan rate, Scanimate could produce undulating text and logos for television broadcast — the same mathematical operation that Delirium performs digitally.

The Rutt/Etra Video Synthesizer (1973) took the concept further, using video luminance to modulate both horizontal and vertical deflection, turning flat images into three-dimensional wireframe landscapes. Delirium's vertical displacement mode (Mode 3) echoes this lineage, though simplified to a half-amplitude horizontal offset that creates a compression effect rather than true raster bending.

### Sinusoidal Distortion Mathematics

Each layer in Delirium computes a displacement offset for every scanline using the formula:

**Offset(y, t) = A × sin(F × y + S × t)**

where *A* is amplitude (pixels of displacement), *F* is spatial frequency (how quickly the wave oscillates across scanlines), *y* is the vertical line number, *S* is temporal speed, and *t* is the frame count. The sine function is computed via a quarter-wave lookup table with 64 entries, extended to the full cycle through quadrant folding and sign negation — a classic FPGA technique that uses one quarter the memory of a full-cycle table while producing identical results.

The product *F × y* determines the spatial pattern: low frequency creates broad, gentle curves; high frequency creates tight, rapid oscillations. The phase term *S × t* advances per frame, causing the wave pattern to scroll vertically through the image over time. Because both layers have independent frequency and speed controls, their interference pattern evolves continuously, never exactly repeating.

### Interlaced Displacement

Mode 2 (Interlaced) applies the sinusoidal offset normally on even scanlines but *negates* it on odd scanlines. The visual result is a zigzag pattern where adjacent lines are displaced in opposite directions. At low amplitudes, this produces a subtle interline shimmer similar to interlace artifacts on CRT displays. At high amplitudes, the image splits into alternating horizontal bands that slide in opposite directions, creating a venetian-blind tearing effect. The interlaced mode is particularly effective for simulating analog video distortion and tracking errors.

### Cascaded Warp Layers

Single-layer sinusoidal distortion produces smooth, predictable waves. Delirium's two-layer cascade architecture creates far more complex topologies. When Layer 2 distorts the output of Layer 1, the second sine wave operates on already-warped pixel data. The result is not a simple sum of two sine waves — it is a *composition* of nonlinear spatial transformations. Regions that Layer 1 has compressed get stretched differently by Layer 2 than regions Layer 1 has expanded. The compound distortion field contains spatial frequencies and structures that neither layer could produce alone, generating the organic, almost liquid quality that gives the program its name.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Parameter Latch ─────────────────────────────────────────────
│   ├─ registers_in(0..5) → Amp1, Freq1, Speed1, Amp2, Freq2, Speed2
│   ├─ registers_in(6)    → Layer modes [1:0][3:2], cascade [4]
│   └─ registers_in(7)    → Mix amount
│
├── Timing / Position Counters ──────────────────────────────────
│   ├─ h_count : horizontal pixel position (per scanline)
│   └─ v_count : vertical line number (per frame)
│
├── Phase Accumulators (advance per vsync) ──────────────────────
│   ├─ phase1 += speed1
│   └─ phase2 += speed2
│
├── Sine Argument (per scanline) ────────────────────────────────
│   ├─ arg1 = (freq1 × v_count)[19:10] + phase1[15:6]
│   └─ arg2 = (freq2 × v_count)[19:10] + phase2[15:6]
│
├── Quarter-Wave Sine LUT ───────────────────────────────────────
│   ├─ sine1 = sine_lookup(arg1)    (signed, ±492 max)
│   └─ sine2 = sine_lookup(arg2)
│
├── Amplitude Scaling ───────────────────────────────────────────
│   ├─ offset1 = (sine1 × amp1) >> 9     (signed pixel offset)
│   └─ offset2 = (sine2 × amp2) >> 9
│
├── Line Buffer A (2048 × 30-bit) ──────────────────────────────
│   ├─ Write: input YUV packed at h_count
│   └─ Read:  displaced address per layer 1 mode
│
├── Layer 1 Distortion ──────────────────────────────────────────
│   ├─ Mode 00: Off        → read at h_count (passthrough)
│   ├─ Mode 01: Horizontal → read at h_count + offset1
│   ├─ Mode 10: Interlace  → even: +offset1, odd: −offset1
│   └─ Mode 11: Vertical   → read at h_count + offset1/2
│
├── Line Buffer B (2048 × 30-bit) ──────────────────────────────
│   ├─ Write: layer 1 output packed YUV
│   └─ Read:  displaced address per layer 2 mode
│
├── Layer 2 Distortion ──────────────────────────────────────────
│   ├─ Mode 00: Off        → read at h_count (passthrough)
│   ├─ Mode 01: Horizontal → read at h_count + offset2
│   ├─ Mode 10: Interlace  → even: +offset2, odd: −offset2
│   └─ Mode 11: Vertical   → read at h_count + offset2/2
│
├── Wet/Dry Mix (3× interpolator_u) ────────────────────────────
│   ├─ Y: lerp(dry_y, wet_y, mix)
│   ├─ U: lerp(dry_u, wet_u, mix)
│   └─ V: lerp(dry_v, wet_v, mix)
│
├── Sync Delay Pipeline (10 clk) ───────────────────────────────
│   └─ Delayed hsync_n, vsync_n, field_n, dry Y/U/V
│
└── Output Video (YUV 4:4:4)
```

The critical architectural choice is the *serial cascade*: Layer 1 writes its distorted output into Line Buffer B, and Layer 2 reads from Buffer B with its own displacement. This means Layer 2 distorts already-warped pixels — the two sine functions compose rather than add. The result is spatial interference patterns that cannot be achieved with parallel mixing. The Cascade toggle reverses which layer processes first, fundamentally changing the compound distortion character even when both layers use identical parameters.

The phase accumulators advance once per frame (at vsync), not per scanline. This means the wave pattern animates smoothly from frame to frame but remains spatially fixed within a single frame. Speed controls the rate of this per-frame phase advance — at Speed 0%, the pattern is static; at Speed 100%, it scrolls rapidly through the image.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Amplitude 1
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the peak pixel displacement of Layer 1's sinusoidal warp. At 0%, Layer 1 produces no distortion regardless of its mode setting. As Amplitude 1 increases, each scanline shifts further from its original position, creating deeper and more pronounced wave curves. At maximum, individual scanlines can shift by nearly the full frame width, wrapping around to the opposite edge of the image. The visual effect progresses from gentle ripples to violent tearing as the amplitude increases. Because Layer 2 operates on Layer 1's output, increasing Amplitude 1 feeds more pre-distorted material into the second warp stage, amplifying the cascaded complexity.

---

#### Knob 2 — Frequency 1
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Sets the spatial frequency of Layer 1's sine wave — how many complete wave cycles fit within the visible frame height. At low values, the sine wave completes fewer cycles across the image, creating broad, sweeping curves. At high values, the wave oscillates rapidly from scanline to scanline, producing tight, closely-spaced ripples. The spatial frequency interacts with amplitude to determine the wave's visual character: low frequency with high amplitude creates large rolling undulations, while high frequency with high amplitude creates a dense, shredded texture.

---

#### Knob 3 — Speed 1
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the animation speed of Layer 1's phase accumulator. At 0%, the distortion pattern is frozen — the wave shape is fixed in position from frame to frame. As Speed 1 increases, the sine wave pattern scrolls vertically through the image, creating the illusion of flowing liquid or moving heat shimmer. Higher speeds produce faster scrolling. The speed value is added to a 16-bit phase accumulator once per frame, so the animation rate is linear with the control setting.

---

#### Knob 4 — Amplitude 2
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the peak pixel displacement of Layer 2, independent of Layer 1. At default (0%), Layer 2 is effectively inactive regardless of its mode setting. Increasing Amplitude 2 activates the second distortion layer, which operates on Layer 1's output when Layer 2 Mode is enabled. Because the two layers cascade, even small Amplitude 2 values create noticeable compound distortion when Layer 1 is already active. For maximum psychedelic intensity, set both amplitudes high with different frequency values.

---

#### Knob 5 — Frequency 2
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Sets the spatial frequency of Layer 2's sine wave, independent of Layer 1. The most interesting compound distortion patterns emerge when the two layers use *different* frequency values — the interference between mismatched spatial frequencies creates complex, evolving topologies. When both frequencies match, the cascade produces a regular pattern. When they differ by a small amount, slow spatial beating patterns appear. When they differ significantly, the image dissolves into chaotic warp fields.

---

#### Knob 6 — Speed 2
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls Layer 2's animation speed, independent of Speed 1. When both layers animate at different speeds, the compound distortion pattern shifts and breathes as the two sine waves drift in and out of phase with each other. Setting Speed 2 to a value close to but not equal to Speed 1 creates a slow beating effect where the compound distortion periodically simplifies and complexifies. Setting them to very different values creates rapid, unpredictable visual evolution.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Layer 1 Mode** | Off | On |
| **8 — Layer 2 Mode** | Off | On |
| **9 — Cascade** | L1>L2 | L2>L1 |
| **10 — Phase Link** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 activate their respective distortion layers. When a layer's toggle is Off, that layer passes its input unchanged regardless of amplitude and frequency settings. The front panel provides Off and Horizontal displacement modes; the VHDL internally supports four modes per layer (Off, Horizontal, Interlaced, Vertical) accessible via MIDI or external control. Toggle 9 reverses which layer processes the input first. Toggle 10 links both phase accumulators so both layers animate in lock-step. Toggle 11 bypasses all processing for instant A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 100 |

Crossfades between the dry (unprocessed) and wet (distorted) signal. At 0%, the output is the original input regardless of distortion settings. At 100% (default), the output is fully distorted. Intermediate values blend the two, creating a ghostly overlay where the undistorted image shows through the warped version. This is particularly effective at 30–60% with high-amplitude distortion — the stable reference image anchors perception while the warp field ripples around it.

---

## Guided Exercises

These exercises build from single-layer displacement to full dual-layer cascaded distortion. Each reveals a different aspect of how sinusoidal warp fields interact.

### Exercise 1: Single-Layer Waves

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: delirium_source1_fruit, after: delirium_ex1_s1 },
    { label: "Field", before: delirium_source2_field, after: delirium_ex1_s2 },
    { label: "Collage", before: delirium_source3_collage, after: delirium_ex1_s3 },
    { label: "Pattern", before: delirium_source4_pattern, after: delirium_ex1_s4 },
    { label: "Girl", before: delirium_source5_girl, after: delirium_ex1_s5 },
    { label: "Wood", before: delirium_source6_wood, after: delirium_ex1_s6 },
  ]}
/>
*Single-Layer Waves — simulated result across source images.*
**Source**: A live camera feed or recorded footage with strong vertical lines, architectural elements, or text — content where horizontal displacement is immediately visible.

**Objective**: Understand the relationship between amplitude, frequency, and the resulting warp pattern using a single distortion layer.

1. **Gentle curves**: With Amplitude 1 at 25% and Frequency 1 at 12%, observe the broad, sweeping curves that ripple through the image. Vertical lines bend into smooth S-shapes.
2. **Tight ripples**: Increase Frequency 1 to 80%. The same amplitude now produces dense, closely-spaced oscillations — the image appears to shimmer rather than wave.
3. **Deep warp**: Lower Frequency 1 back to 25% and increase Amplitude 1 to 75%. The broad curves now displace scanlines far enough to wrap around the frame edges.
4. **Animation**: Increase Speed 1 from 0% to 50%. The wave pattern scrolls vertically through the image, creating a flowing liquid effect.
5. **A/B compare**: Toggle Bypass on and off to compare the warped and original signals.

**Key concepts**: Amplitude controls displacement depth, frequency controls spatial density of the sine wave, speed animates the wave pattern vertically through the frame

---

### Exercise 2: Cascaded Distortion

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: delirium_source1_fruit, after: delirium_ex2_s1 },
    { label: "Field", before: delirium_source2_field, after: delirium_ex2_s2 },
    { label: "Collage", before: delirium_source3_collage, after: delirium_ex2_s3 },
    { label: "Pattern", before: delirium_source4_pattern, after: delirium_ex2_s4 },
    { label: "Girl", before: delirium_source5_girl, after: delirium_ex2_s5 },
    { label: "Wood", before: delirium_source6_wood, after: delirium_ex2_s6 },
  ]}
/>
*Cascaded Distortion — simulated result across source images.*
**Source**: Abstract or colorful footage — kaleidoscopic patterns, color bars, or footage with saturated colors and varied spatial content.

**Objective**: Explore how two distortion layers cascade to produce compound warp fields.

1. **Prepare Layer 1**: Set Amplitude 1 to 30%, Frequency 1 to 20%, Speed 1 to 15%.
2. **Activate Layer 2**: Turn Layer 2 Mode On. Increase Amplitude 2 from 0% to 30%.
3. **Matched frequencies**: Set Frequency 2 to match Frequency 1 (~20%). Observe the regular compound pattern.
4. **Detune frequencies**: Slowly increase Frequency 2 to 60%. Watch the interference pattern emerge as the two sine waves interact with different spatial rates.
5. **Animate both**: Set Speed 2 to 20% (different from Speed 1). The compound pattern now evolves continuously as the two phases drift.
6. **Reverse cascade**: Toggle Cascade to L2>L1. Note how the visual character changes — the higher-frequency layer now distorts the input first.

**Key concepts**: Cascaded distortion is composition not addition, mismatched frequencies create complex interference, cascade order affects which warp dominates

---

### Exercise 3: Psychedelic Meltdown

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: delirium_source1_fruit, after: delirium_ex3_s1 },
    { label: "Field", before: delirium_source2_field, after: delirium_ex3_s2 },
    { label: "Collage", before: delirium_source3_collage, after: delirium_ex3_s3 },
    { label: "Pattern", before: delirium_source4_pattern, after: delirium_ex3_s4 },
    { label: "Girl", before: delirium_source5_girl, after: delirium_ex3_s5 },
    { label: "Wood", before: delirium_source6_wood, after: delirium_ex3_s6 },
  ]}
/>
*Psychedelic Meltdown — simulated result across source images.*
**Source**: Any visually rich footage — faces, landscapes, or music videos work well. Content with recognizable subjects makes the distortion more dramatic.

**Objective**: Push both layers to extreme settings for full psychedelic distortion, then use Mix to dial back the intensity.

1. **Maximum chaos**: Set both amplitudes to 80%, Frequency 1 to 15%, Frequency 2 to 45%, both speeds to 25–30%.
2. **Observe**: The image should be almost unrecognizable — a churning, liquid warp field. Glimpses of the source appear between wave peaks.
3. **Phase link**: Toggle Phase Link On. The two layers now animate in lock-step, producing a more regular (but still complex) compound pattern.
4. **Ghost mix**: Lower Mix to ~40%. The original image appears as a stable ghost behind the warped version, anchoring perception.
5. **Freeze**: Set both speeds to 0%. The distortion freezes in place, revealing the static compound wave topology. Sweep Frequency 2 slowly to watch the topology reshape.
6. **Cascade comparison**: Toggle Cascade back and forth between L1>L2 and L2>L1. Notice how the same parameters produce different distortion textures.

**Key concepts**: Extreme amplitudes with mismatched frequencies create liquid distortion fields, Mix provides intensity control, Phase Link synchronizes animation

---


## Tips

- **Start with one layer**: Delirium defaults to single-layer operation (Layer 2 amplitude at zero). Master the amplitude/frequency/speed relationship on Layer 1 before engaging Layer 2.
- **Detune for complexity**: The most visually interesting compound distortion comes from mismatched frequencies between the two layers. Try ratios like 1:3 or 2:5 for complex interference without total chaos.
- **Mix as intensity control**: Rather than reducing amplitude, use the Mix fader to dial back intensity. This preserves the distortion character while blending in the stable reference image.
- **Phase Link for regularity**: When the dual-layer animation is too chaotic, Phase Link forces both layers to animate together, creating a more predictable compound pattern.
- **Speed zero for stills**: Setting both speeds to 0% freezes the distortion pattern, turning Delirium into a static spatial transform useful for graphic design and fixed-frame compositions.
- **Feedback loops**: Routing the output back to the input creates recursive sinusoidal distortion that evolves over time, producing organic spiral and tunnel effects.
- **Cascade order matters**: Even with identical parameters on both layers, L1>L2 and L2>L1 produce different results because the composition order of nonlinear transforms is not commutative.
- **Frequency as texture control**: Low frequency values (~5–15%) create smooth, rolling waves. High values (~70–90%) create dense, shredded textures. The visual transition is continuous.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for line buffer storage. |
| **Cascade** | Serial composition of two distortion layers where the output of one feeds the input of the other, producing compound effects. |
| **Displacement** | Shifting a pixel's read position by an offset, causing the image to appear moved at that location. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interlaced Displacement** | A distortion mode where even and odd scanlines receive opposite horizontal offsets, creating a zigzag tearing effect. |
| **Interpolator** | A hardware module that computes weighted averages between two values, used here for wet/dry crossfading. |
| **Line Buffer** | A memory buffer storing one full scanline of video data, enabling displaced reads at arbitrary horizontal positions. |
| **LUT** | Lookup Table; a memory array storing precomputed function values, used here for the quarter-wave sine function. |
| **Phase Accumulator** | A counter that advances by a speed value each frame, providing the time-varying phase offset for wave animation. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Quadrant Folding** | A technique for computing a full-cycle sine function from a quarter-wave lookup table by mirroring and negating values based on the phase quadrant. |
| **Scanline** | A single horizontal line of video data; Delirium computes one displacement offset per scanline. |
| **Sinusoidal Distortion** | Applying a sine-wave-shaped offset to pixel positions, creating smooth, periodic undulation. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
