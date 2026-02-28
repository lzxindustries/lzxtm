---
draft: true
sidebar_position: 78
slug: /instruments/videomancer/downpour
title: "Downpour"
image: /img/instruments/videomancer/downpour/downpour_hero.png
description: "Program guide for Downpour, a Videomancer weather program for the LZX video synthesizer."
---

import downpour_hero from '/img/instruments/videomancer/downpour/downpour_hero.png';
import downpour_before_after from '/img/instruments/videomancer/downpour/downpour_before_after.png';
import downpour_control_panel from '/img/instruments/videomancer/downpour/downpour_control_panel.png';
import downpour_exercise1_result from '/img/instruments/videomancer/downpour/downpour_exercise1_result.png';
import downpour_exercise2_result from '/img/instruments/videomancer/downpour/downpour_exercise2_result.png';
import downpour_exercise3_result from '/img/instruments/videomancer/downpour/downpour_exercise3_result.png';

# Downpour

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={downpour_hero} alt="Downpour hero image"/>
*Downpour compositing LFSR-seeded diagonal rain streaks with splash highlights and fog overlay onto live video.*
<img src={downpour_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Downpour applied.*

---

## Overview

Rain is one of those visual phenomena that sits right at the boundary between order and chaos. Each drop follows a deterministic path — gravity pulls it straight down, wind pushes it sideways — but millions of drops falling simultaneously create a texture that reads as random noise. Downpour reproduces this duality by using two LFSR pseudo-random generators to seed drop positions across the frame, then rendering each drop as a bright additive streak on the Y channel with wind-angled displacement per scanline.

The program layers five compositing stages on top of the source video: deterministic rain particle placement, configurable vertical streak rendering with brightness falloff, horizontal edge detection for splash highlights, optional fog darkening with a cool blue tint, and a final wet/dry crossfade mix. The name references the heaviest category of rainfall — a deluge where individual drops blur together into sheets of falling water. At low density with long streaks, Downpour renders gentle drizzle. At high density with heavy mode engaged, it produces a torrential curtain of light across the entire frame.

Every rain drop exists only in register fabric — zero BRAM is consumed. The LFSR pair cycles freely, combining with the horizontal pixel counter via XOR to produce a per-pixel hash that determines which columns contain drops. A frame counter, advanced on each vsync edge, shifts the vertical start position of drops downward, creating the illusion of continuous falling motion.

---

## Background

### Rain Simulation in Computer Graphics

Simulating rain convincingly requires solving two problems simultaneously: where do the drops appear, and how do they move? Early broadcast weather overlays used simple vertical lines drawn at random x-positions, but these looked artificial because real rain is affected by wind, turbulence, and perspective foreshortening. Modern particle systems track individual drop positions with velocity vectors, but this is computationally expensive. Downpour takes a middle path: it uses pseudo-random hash functions to determine *which pixel columns* contain drops, then computes vertical position from a global frame counter plus per-column offsets. The result looks like a particle system but requires no per-particle state memory.

### Pseudo-Random Number Generation with LFSRs

A Linear Feedback Shift Register (LFSR) is the simplest hardware-friendly pseudo-random number generator. It consists of a shift register whose input bit is computed as an XOR of selected tap positions. A 16-bit LFSR with correctly chosen taps cycles through all 65,535 non-zero states before repeating. Downpour instantiates two independent LFSR16 generators — seeded with 0xCAFE and 0xBEEF — and XORs their outputs together to produce a 12-bit combined noise value. This combined value is further XORed with the horizontal pixel counter to produce a per-pixel hash that determines drop column placement.

### Streak Rendering and Brightness Falloff

Real raindrops are nearly invisible in still air — they are small, transparent, and fast-moving. What we *see* as a "raindrop" on camera is actually a motion-blurred streak: the camera's shutter stays open long enough that the drop traces a bright line across the sensor. Downpour renders these streaks by checking whether the current scanline falls within a drop's vertical extent. The streak brightness tapers toward the tail — the bottom half of each streak is rendered at half brightness — simulating the way motion blur fades at the trailing edge of a moving object.

### Edge Detection and Splash Highlights

When a raindrop hits a surface, it produces a small burst of scattered light — the splash. Downpour simulates this by running a simple horizontal edge detector on the source luma channel. Where the absolute difference between adjacent Y samples exceeds a threshold of 128 (on the 10-bit scale), and a rain drop is active at that position, a splash is triggered. The splash renders as a short horizontal burst of bright pixels that decays exponentially — each clock cycle, the splash brightness halves and the splash counter decrements. The result is a bright flash at sharp horizontal edges in the source, creating the illusion that rain is landing on surfaces visible in the video.

### Weather Overlays in Broadcast Video

Television weather graphics have used synthetic rain and snow overlays since the early days of chroma-key compositing. The classic approach superimposes a semi-transparent particle layer over live or recorded footage. Downpour extends this tradition with its fog mode, which darkens the background by reducing Y by 25% and shifts the chrominance toward blue (U+24, V−16) to simulate the desaturated, cool-toned look of an overcast sky. Combined with the rain streaks, fog mode transforms bright daylight footage into a convincing rainy-day atmosphere.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ h_count: horizontal pixel position (reset on hsync)
│   ├─ v_count: vertical scanline position (reset on vsync)
│   └─ frame_count: frame index (incremented on vsync)
│
├── LFSR Noise ─────────────────────────────────────────────────
│   ├─ LFSR1 (seed 0xCAFE) ──┐
│   └─ LFSR2 (seed 0xBEEF) ──┴── XOR → combined noise
│
├── Rain Pipeline (6 stages) ───────────────────────────────────
│   │
│   ├─ Stage 1: Drop Position Compute
│   │   ├─ hash = h_count XOR combined_noise
│   │   ├─ drop_length = drop_len_param >> 4 (2–64 px)
│   │   └─ drop_y_base = frame_count × speed + hash(7:0)
│   │
│   ├─ Stage 2: Hit Test
│   │   ├─ density_threshold (doubled in heavy mode)
│   │   ├─ column is drop? hash(11:4) < threshold(11:4)
│   │   ├─ wind_offset = v_count × wind_angle (±direction)
│   │   ├─ in vertical range? v_count ∈ [y_start, y_end)
│   │   └─ brightness with tail falloff (half in lower half)
│   │
│   ├─ Stage 3: Edge Detection + Splash
│   │   ├─ edge = |current_Y − previous_Y|
│   │   ├─ splash trigger: edge>128 AND rain_hit AND splash_en
│   │   └─ splash decay: brightness halves, counter decrements
│   │
│   ├─ Stage 4: Fog Overlay + Composite
│   │   ├─ fog: Y -= Y>>2, U += 24, V -= 16
│   │   ├─ add rain brightness to Y (saturating)
│   │   ├─ add splash brightness to Y (saturating)
│   │   └─ rain tint on hit pixels: U += 8, V -= 8
│   │
│   └─ Stage 5: Output Register
│
├── Sync Delay Pipeline (10 clocks) ────────────────────────────
│   └─ Delayed dry Y/U/V + sync signals
│
├── Interpolator (4 clocks) ────────────────────────────────────
│   ├─ Y: lerp(dry_Y, wet_Y, mix)
│   ├─ U: lerp(dry_U, wet_U, mix)
│   └─ V: lerp(dry_V, wet_V, mix)
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed or delayed original
```

The key architectural choice is that rain drops have no persistent per-particle state. Instead, the LFSR pair runs freely and the per-pixel hash (h_count XOR combined LFSR) deterministically assigns each pixel column a "drop or no-drop" status based on the density threshold. Vertical animation comes from the frame counter multiplied by the speed parameter, which shifts every drop's vertical position downward each frame. This means all drops fall at the same speed — there is no per-drop velocity variation — but the per-column hash offset staggers their vertical positions, creating visual diversity. The splash system is the only stateful element: once triggered by a strong horizontal edge coinciding with a rain hit, the splash counter and brightness decay independently across subsequent pixels.

---

## Parameter Reference

<img src={downpour_control_panel} alt="Videomancer front panel with Downpour loaded"/>
*Videomancer's front panel with Downpour active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the number of rain drops per scanline. The density value sets a threshold: pixel columns whose hash value falls below this threshold produce visible drops. At 0%, no columns pass the threshold and the frame is clear. At 100%, the maximum number of columns produce drops. When heavy mode is active (Toggle 8), the effective threshold is doubled, filling the frame with twice as many drops — simulating the difference between a light shower and a cloudburst.

---

#### Knob 2 — Wind Ang
| Property | Value |
|----------|-------|
| Range | 0° – 180° |
| Default | 90° |
| Suffix | ° |

Controls the vertical length of each rain streak in pixels. The register value is right-shifted by 4 bits and clamped to a minimum of 2, yielding streak lengths from 2 to 64 pixels. Short streaks create a fine drizzle appearance — small bright dots scattered across the frame. Long streaks produce dramatic diagonal lines that sweep across the image. The lower half of each streak is rendered at half brightness, simulating the tapered motion blur of a real raindrop photographed with a slow shutter.

---

#### Knob 3 — Streak Len
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the vertical speed of rain drop animation. Higher values make drops traverse the frame more quickly by increasing the per-frame vertical offset applied to all drop positions. At 0%, drops are frozen in place. At 100%, drops race through the frame at maximum velocity. Because all drops share the same speed multiplier, the entire rain field moves as a coherent sheet — identical to how real rain looks when driven by a steady wind.

---

#### Knob 4 — Splash Int
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Sets the wind-driven horizontal displacement of rain streaks. Each scanline's drop positions are offset horizontally by an amount proportional to this value multiplied by the scanline number. Higher values create more extreme diagonal angles — the rain appears to blow sideways rather than fall vertically. The offset direction is controlled by Toggle 7 (Type). At 0°, rain falls perfectly vertical. At maximum, streaks become nearly horizontal slashes across the frame.

---

#### Knob 5 — Fall Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the luminance added to pixels where rain drops are active. This is the peak brightness at the top of each streak — the tail fades to half this value. At low settings, rain appears as subtle translucent streaks barely visible against the source. At high settings, drops become brilliant white slashes that overpower the underlying video. Because the addition is saturating (clamped to 1023), bright source areas will clip before dark areas, making rain most visible against dark backgrounds.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the horizontal extent of splash highlights. When a splash is triggered by a strong luma edge coinciding with a rain hit, this parameter sets the initial splash counter value (register >> 4, yielding 0–63 pixel spread). The splash brightness starts at half the rain brightness and halves again on each subsequent pixel, creating an exponentially decaying burst. Larger values produce wider, more dramatic splashes; smaller values create tight, subtle flashes.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Type** | Rain | Snow |
| **8 — Splash** | Off | On |
| **9 — Tint** | Off | On |
| **10 — Accumulate** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–11 control five independent binary options. Toggle 7 sets the wind direction for diagonal rain displacement. Toggle 8 enables heavy mode, which doubles the effective density threshold. Toggle 9 enables the splash highlight system. Toggle 10 enables fog overlay compositing. Toggle 11 is the global bypass switch. These toggles do not interact with each other — each enables or disables a specific aspect of the rain simulation independently.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original (delayed) source and the rain-composited result. At 0%, only the unmodified source is output. At 100%, the full rain effect is applied. Intermediate values produce a proportional blend. This uses the same interpolator_u hardware as other Videomancer programs — a linear interpolation across all three YUV channels simultaneously. The mix operates on the final composited signal (including fog, rain, and splash).

---

## Guided Exercises

These exercises progress from a simple rain overlay to complex weather scene construction. Each introduces additional layers of the rain simulation.

### Exercise 1: Gentle Drizzle

<img src={downpour_exercise1_result} alt="Gentle Drizzle result"/>
*Gentle Drizzle — simulated result across source images.*
**Source**: A recorded outdoor scene — a park, street, or garden — with moderate contrast and varied textures.

**Objective**: Learn how density, streak length, and brightness interact to create a convincing light rain effect.

1. **Sparse drops**: Set Density to about 20%. A few scattered bright streaks appear over the source.
2. **Streak length**: Increase Wind Ang (streak length control) to about 40%. Drops stretch into short vertical lines.
3. **Brightness balance**: Adjust Fall Speed (brightness control) until the streaks are visible but not overwhelming — around 50%.
4. **Add wind**: Slowly increase Splash Int (wind angle) to introduce a slight diagonal tilt. Try about 20%.
5. **Direction**: Toggle Type to flip the wind direction. Notice how the rain angle mirrors.
6. **Mix subtlety**: Lower Mix to about 70% for a more transparent, atmospheric look.

**Key concepts**: Density sets the number of drops, streak length and brightness control their appearance, wind angle creates diagonal rain, and the mix fader controls overall transparency

---

### Exercise 2: Thunderstorm

<img src={downpour_exercise2_result} alt="Thunderstorm result"/>
*Thunderstorm — simulated result across source images.*
**Source**: Dark, moody footage with strong contrast — night scenes, dramatic lighting, or high-contrast architecture.

**Objective**: Build a heavy rain scene with splash highlights and fog overlay.

1. **Heavy density**: Set Density to about 60% and enable Splash (heavy mode) for dense rain.
2. **Long streaks**: Set Wind Ang to about 70% for dramatic long streaks.
3. **Strong wind**: Set Splash Int (wind angle) to about 50% and toggle Type to choose a direction.
4. **Bright rain**: Increase Fall Speed (brightness) to about 80% so drops stand out against the dark source.
5. **Enable splashes**: Turn on Tint (splash enable). Watch for bright horizontal bursts where rain hits high-contrast edges.
6. **Splash spread**: Increase Brightness (splash size) to about 40% for visible splash highlights.
7. **Fog atmosphere**: Enable Accumulate (fog overlay). The background darkens and shifts blue.
8. **Full immersion**: Set Mix to 100% for the complete thunderstorm effect.

**Key concepts**: Heavy mode doubles drop density, splash highlights appear at luma edges, fog darkens and blue-shifts the background, all layers combine for atmospheric weather simulation

---

### Exercise 3: Abstract Rain Texture

<img src={downpour_exercise3_result} alt="Abstract Rain Texture result"/>
*Abstract Rain Texture — simulated result across source images.*
**Source**: Any high-contrast video — graphics, text overlays, or footage with strong edges.

**Objective**: Use the rain engine as an abstract texture generator rather than a realistic weather effect.

1. **Maximum density**: Set Density to 100% and enable Splash (heavy mode) for near-total coverage.
2. **Short streaks**: Set Wind Ang to about 15% for dot-like drops instead of streaks.
3. **Extreme wind**: Set Splash Int (wind angle) to about 90% for heavily diagonal rain.
4. **Bright splashes**: Enable Tint (splash enable) and set Brightness (splash size) to about 60%.
5. **Low brightness**: Set Fall Speed (brightness) to about 30% so the rain is subtle but splashes are prominent.
6. **Speed variation**: Sweep Streak Len (fall speed) slowly and observe how the rain pattern crawls and jumps.
7. **Mix modulation**: Sweep Mix between 30% and 80% to blend the abstract texture with the source.

**Key concepts**: High density with short streaks creates noise textures, diagonal wind turns vertical rain into diagonal hatching, splash highlights respond to source content creating edge-aware texturing

---


## Tips

- **Dark backgrounds reveal rain best**: Rain brightness is additive, so drops are most visible against dark source material. Combine with fog overlay to darken bright footage.
- **Heavy mode for drama**: The heavy/light toggle (Splash) doubles the effective density, transforming a gentle drizzle into a torrential curtain. This stacks with the Density knob for extreme coverage.
- **Wind angle creates drama**: Even a small wind angle transforms monotonous vertical rain into dynamic diagonal streaks. Match the angle to the scene's implied wind direction for realism.
- **Splash needs edges**: The splash system responds to horizontal luma edges in the source — it is content-aware. High-contrast footage with sharp details produces the most dramatic splash effects.
- **Fog sets the mood**: Enabling fog (Accumulate) darkens the background by 25% and shifts chrominance toward blue. This single toggle changes the entire atmosphere from "rain on a sunny day" to "overcast downpour."
- **Short streaks for snow/mist**: Setting streak length very low (Wind Ang ~10%) creates dot-like particles that read as snowflakes or mist droplets rather than rain streaks.
- **Speed zero for freeze**: Setting fall speed (Streak Len) to 0% freezes all drops in place, creating a static noise texture overlay. Useful for abstract compositing.
- **Feedback layering**: Route the output back to the input for recursive rain — drops accumulate and interact with their own splash highlights across multiple generations.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Compositing** | A blending operation that adds pixel values together, clamping at maximum (1023). Rain brightness is composited additively onto the source luma. |
| **Edge Detection** | Measuring the difference between adjacent pixel values to identify sharp transitions. Downpour uses horizontal luma edge detection to trigger splash highlights. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Frame Counter** | A register that increments once per vertical sync, used to animate the vertical position of rain drops across successive frames. |
| **LFSR** | Linear Feedback Shift Register; a simple pseudo-random number generator that cycles through a sequence of states determined by its tap configuration and seed value. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Saturating Arithmetic** | Addition or subtraction that clamps the result to the valid range (0–1023) instead of wrapping around on overflow or underflow. |
| **Splash** | A short horizontal burst of bright pixels triggered at luma edges coinciding with rain drops, simulating the visual effect of a raindrop striking a surface. |
| **Streak** | A vertical run of bright pixels representing a single rain drop's motion-blurred trail across the camera sensor. |
| **XOR Hash** | A bitwise exclusive-OR operation used to combine the horizontal pixel counter with LFSR noise, producing a deterministic but pseudo-random per-pixel value. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
