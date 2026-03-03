---
draft: true
sidebar_position: 187
slug: /instruments/videomancer/massif
title: "Massif"
image: /img/instruments/videomancer/massif/massif_hero_s1.png
description: "In 1973, Steve Rutt and Bill Etra built a video instrument that did something no other machine could do: it took a standard television signal and deflected each scan line vertically by an amount proportional to its brightness."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import massif_source1_fruit from '/img/instruments/videomancer/massif/massif_source1_fruit.png';
import massif_source2_runner from '/img/instruments/videomancer/massif/massif_source2_runner.png';
import massif_source3_clouds from '/img/instruments/videomancer/massif/massif_source3_clouds.png';
import massif_source4_pattern from '/img/instruments/videomancer/massif/massif_source4_pattern.png';
import massif_source5_man from '/img/instruments/videomancer/massif/massif_source5_man.png';
import massif_source6_knit from '/img/instruments/videomancer/massif/massif_source6_knit.png';
import massif_hero_s1 from '/img/instruments/videomancer/massif/massif_hero_s1.png';
import massif_hero_s2 from '/img/instruments/videomancer/massif/massif_hero_s2.png';
import massif_hero_s3 from '/img/instruments/videomancer/massif/massif_hero_s3.png';
import massif_hero_s4 from '/img/instruments/videomancer/massif/massif_hero_s4.png';
import massif_hero_s5 from '/img/instruments/videomancer/massif/massif_hero_s5.png';
import massif_hero_s6 from '/img/instruments/videomancer/massif/massif_hero_s6.png';
import massif_ex1_s1 from '/img/instruments/videomancer/massif/massif_ex1_s1.png';
import massif_ex1_s2 from '/img/instruments/videomancer/massif/massif_ex1_s2.png';
import massif_ex1_s3 from '/img/instruments/videomancer/massif/massif_ex1_s3.png';
import massif_ex1_s4 from '/img/instruments/videomancer/massif/massif_ex1_s4.png';
import massif_ex1_s5 from '/img/instruments/videomancer/massif/massif_ex1_s5.png';
import massif_ex1_s6 from '/img/instruments/videomancer/massif/massif_ex1_s6.png';
import massif_ex2_s1 from '/img/instruments/videomancer/massif/massif_ex2_s1.png';
import massif_ex2_s2 from '/img/instruments/videomancer/massif/massif_ex2_s2.png';
import massif_ex2_s3 from '/img/instruments/videomancer/massif/massif_ex2_s3.png';
import massif_ex2_s4 from '/img/instruments/videomancer/massif/massif_ex2_s4.png';
import massif_ex2_s5 from '/img/instruments/videomancer/massif/massif_ex2_s5.png';
import massif_ex2_s6 from '/img/instruments/videomancer/massif/massif_ex2_s6.png';
import massif_ex3_s1 from '/img/instruments/videomancer/massif/massif_ex3_s1.png';
import massif_ex3_s2 from '/img/instruments/videomancer/massif/massif_ex3_s2.png';
import massif_ex3_s3 from '/img/instruments/videomancer/massif/massif_ex3_s3.png';
import massif_ex3_s4 from '/img/instruments/videomancer/massif/massif_ex3_s4.png';
import massif_ex3_s5 from '/img/instruments/videomancer/massif/massif_ex3_s5.png';
import massif_ex3_s6 from '/img/instruments/videomancer/massif/massif_ex3_s6.png';

# Massif

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: massif_source1_fruit, after: massif_hero_s1 },
    { label: "Runner", before: massif_source2_runner, after: massif_hero_s2 },
    { label: "Clouds", before: massif_source3_clouds, after: massif_hero_s3 },
    { label: "Pattern", before: massif_source4_pattern, after: massif_hero_s4 },
    { label: "Man", before: massif_source5_man, after: massif_hero_s5 },
    { label: "Knit", before: massif_source6_knit, after: massif_hero_s6 },
  ]}
/>
*Massif displacing video scanlines by luminance to sculpt a phosphor-glow terrain landscape from a camera image, evoking the Rutt/Etra Video Synthesizer.*

---

## Overview

In 1973, Steve Rutt and Bill Etra built a video instrument that did something no other machine could do: it took a standard television signal and deflected each scan line vertically by an amount proportional to its brightness. A face became a mountain range. A hand became a landscape. The flat raster of broadcast television was transformed into a undulating three-dimensional terrain, drawn in glowing phosphor lines on a CRT monitor. The Rutt/Etra Video Synthesizer became one of the most iconic instruments in the history of video art.

Massif is an FPGA reimagining of that concept. It samples the luminance of each input pixel, calculates a vertical displacement proportional to brightness, and writes the pixel data into a column buffer at the displaced position using max-brightness compositing. The column buffer accumulates a vertical slice of the terrain, and inter-frame decay creates phosphor persistence — bright lines glow and slowly fade like a long-persistence CRT. Perspective foreshortening makes mountains appear to recede toward the horizon. Scanline spacing creates the characteristic raster-line gaps of a CRT display. Edge enhancement brightens contour lines where luminance changes rapidly.

The name *Massif* refers to a compact group of mountains — a geological term for the terrain formations that this program sculpts from video signals. At moderate settings, it produces recognizable luminance-displaced portraits. At extreme settings, it generates abstract phosphor landscapes, oscilloscope-like waveform displays, and neon terrain visualizations.

---

## Background

### The Rutt/Etra Video Synthesizer

The original Rutt/Etra (1973) was an analog instrument that manipulated the horizontal and vertical deflection signals of a CRT monitor. By mixing video luminance into the vertical deflection path, each scan line was physically displaced on the monitor — bright areas pushed the electron beam upward, creating peaks, while dark areas left the beam at its resting position, creating valleys. The result was captured by pointing a camera at the monitor, creating a feedback loop between the input video and the terrain display. Massif reproduces the luminance-to-vertical-displacement core of this instrument digitally, using BRAM column buffers instead of analog deflection circuits.

### Column Buffer Architecture

Unlike a frame buffer (which stores every pixel of every line), Massif uses a **column buffer** — a 1024-entry vertical memory that stores one pixel-column of the terrain. During each pixel clock, the displaced target address is written (if the new pixel is brighter than what's already stored, using max-brightness compositing) and the current output line is read simultaneously. This dual-port BRAM architecture allows the terrain to accumulate with each new input scan line. Three separate column buffers store Y, U, and V independently.

### Phosphor Decay

Real CRT phosphors have a characteristic persistence — after the electron beam excites them, they glow brightly and then gradually fade. Massif simulates this with an inter-frame decay sweep: during vertical blanking, the entire column buffer is traversed and each stored luminance value is multiplied by the Decay parameter, attenuating it toward black. High decay values produce long glowing trails; low decay values make the terrain refresh quickly with each new frame.

### Perspective Foreshortening

In a real three-dimensional landscape, objects closer to the viewer appear larger and more displaced, while distant objects appear compressed. Massif's Perspective control scales the vertical displacement by the current scan line position — lines near the bottom of the frame (closer to the "viewer") get more displacement than lines near the top (further away). This creates a convincing illusion of depth as the terrain recedes toward a vanishing point.

### Max-Brightness Compositing

When multiple input scan lines displace to the same target position in the column buffer, Massif uses **max-brightness compositing** — only the brightest value is retained. This prevents darker scan lines from overwriting bright peaks, preserving the mountain silhouette. The result is that the terrain accumulates the brightest features of each input frame, creating a luminous relief map of the video content.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Luma Invert ──────────────────────
│   └─ input_y = invert ? (1023 - Y) : Y
│
├── Stage 2: Displacement Calculation ──────────────────────────
│   ├─ disp_raw = input_y × deflection
│   ├─ disp_signed = disp_raw[19:13]  (max ±128 lines)
│   ├─ direction: bright-up = −disp, bright-down = +disp
│   └─ luma_gradient = |input_y − prev_pixel_y|
│
├── Stage 3: Perspective + Target Line ─────────────────────────
│   ├─ persp_factor = (v_count × perspective) >> 10
│   ├─ scaled_disp = displacement × persp_factor
│   ├─ target_line = v_count + scaled_disp
│   ├─ target_valid = (target_line ≥ 0 AND < 1024)
│   └─ edge_boost = gradient × edge_enhance, clamped
│
├── Stage 4: Column Buffer (Dual-Port BRAM) ────────────────────
│   ├─ Write port: col[target_addr] = max(existing, brightness)
│   │   └─ Writes Y + (mono ? tint_UV : source_UV)
│   ├─ Read port: col[v_count] → col_rd_y/u/v
│   └─ Decay sweep (vblank): col[addr] *= decay >> 10
│
├── Stage 5: Output Mux ───────────────────────────────────────
│   ├─ col_rd_y > 0 → show terrain pixel (update hold state)
│   └─ col_rd_y = 0 → fill_mode ? hold : black
│
├── Interpolator (4 clk) ──────────────────────────────────────
│   └─ Mix: lerp(dry_input, wet_terrain, mix_amount)
│
└── Output ─────────────────────────────────────────────────────
    └─ data_out.y / u / v + delayed sync
```

The column buffer is the heart of the program. It operates as a dual-port BRAM: each pixel clock simultaneously writes at the displaced target address and reads at the current output address. The max-brightness write policy means the terrain accumulates the brightest features — multiple input scan lines can "paint" into the same column position, but only the brightest pixel survives. The decay sweep runs during vertical blanking, gradually attenuating the entire buffer so that the terrain refreshes with each new frame rather than building up indefinitely. The line gap mask operates upstream of the column write, skipping lines to create the CRT raster-line spacing effect.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Deflection
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Controls the vertical displacement gain — how far each scan line is pushed by its luminance value. The displacement is calculated as `input_y × deflection / 1024`, yielding a maximum of approximately 128 lines of displacement at full gain with a white input signal. At zero, all scan lines remain at their original positions and the terrain is flat. At moderate values, the video resolves into gentle rolling hills. At maximum, the terrain becomes extreme — bright areas push far from their original positions, creating dramatic mountain peaks and deep valleys.

---

#### Knob 2 — Perspective
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the perspective foreshortening amount. When Perspective is enabled (Toggle 9), this scales the displacement by scan line position: lines near the bottom of the frame get more displacement than lines near the top. At 50%, the scaling is moderate — a gentle sense of depth. At 100%, the foreshortening is extreme — the bottom of the frame shows towering peaks while the top is nearly flat, creating a strong vanishing-point perspective. When Perspective is disabled, this control has no effect.

---

#### Knob 3 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls the phosphor decay rate — how quickly the column buffer attenuates between frames. At 0%, the buffer clears completely every frame, showing only the current frame's terrain with no persistence. At 100%, the buffer barely decays, creating long glowing trails where bright features persist across many frames. At moderate values (50–70%), the terrain shows smooth phosphor-like persistence where peaks glow brightly and fade gradually, closely matching the look of a long-persistence CRT phosphor.

---

#### Knob 4 — Edge Enh
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

Controls the edge enhancement intensity. The edge detector computes the absolute difference between adjacent horizontal pixels, and this gradient is multiplied by the Edge Enhancement parameter to boost contour brightness. At zero, no enhancement — the terrain brightness matches the raw input luminance. At moderate values, contour edges glow more brightly than flat areas, creating a wire-frame-like outline effect over the terrain. At maximum, the enhancement can dominate, producing a purely contour-driven terrain where only edges are visible.

---

#### Knob 5 — Tint Hue
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 123deg |
| Suffix | deg |

Selects the phosphor tint color for monochrome mode. The pot maps through a piecewise hue circle: green (0°) → yellow → red → blue → magenta → green (360°). Classic CRT phosphor colors include green (~0°) for P1 phosphor, amber (~90°) for P3, and blue-white (~200°) for P4. In Source color mode, this control has no effect — the original video chroma is preserved.

---

#### Knob 6 — Line Gap
| Property | Value |
|----------|-------|
| Range | 0ln – 16ln |
| Default | 4ln |
| Suffix | ln |

Controls the scanline spacing — how many lines apart the terrain raster is drawn. The top 4 bits of the register select a gap divisor from 1 (every line drawn) to 16 (every 16th line drawn). At 1, the terrain is a dense continuous surface. At moderate values (4–8), the classic CRT raster-line look appears with visible gaps between scan lines. At 16, the terrain becomes very sparse — widely spaced horizontal lines floating in black space, evoking an oscilloscope trace rather than a filled surface.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color** | Mono | Source |
| **8 — Direction** | Up | Down |
| **9 — Perspect** | Off | On |
| **10 — Fill Mode** | Black | Hold |
| **11 — Invert** | Normal | Invert |

The five toggles control fundamental display characteristics rather than compositing layers. Color selects between monochrome tinted output and full-color source passthrough. Direction flips the displacement polarity, completely changing the terrain character. Perspective enables the depth foreshortening effect. Fill Mode controls what appears in the gaps between terrain lines — black space or held values. Invert flips the luminance before displacement, swapping peaks and valleys. Note that there is no bypass toggle — set Mix to 0% to pass the original signal through unchanged.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the original dry input and the wet terrain output. At 0%, the output is 100% dry — effectively bypassing all processing. At 100%, the output is fully wet — the complete terrain visualization. Intermediate values blend the flat video with the displaced terrain, creating a ghostly overlay where the original image is visible beneath the terrain peaks. Since there is no dedicated bypass toggle, this fader is the primary bypass control.

---

## Guided Exercises

These exercises progress from basic luminance displacement to full terrain visualization with phosphor persistence and perspective depth.

### Exercise 1: Basic Terrain Displacement

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: massif_source1_fruit, after: massif_ex1_s1 },
    { label: "Runner", before: massif_source2_runner, after: massif_ex1_s2 },
    { label: "Clouds", before: massif_source3_clouds, after: massif_ex1_s3 },
    { label: "Pattern", before: massif_source4_pattern, after: massif_ex1_s4 },
    { label: "Man", before: massif_source5_man, after: massif_ex1_s5 },
    { label: "Knit", before: massif_source6_knit, after: massif_ex1_s6 },
  ]}
/>
*Basic Terrain Displacement — simulated result across source images.*
**Source**: A portrait or face — any image with clear luminance structure and recognizable features.

**Objective**: Learn how luminance displacement transforms flat video into a terrain surface.

1. **Initial setup**: Set Deflection to about 40%. The face should visibly distort — bright areas push upward.
2. **Observe displacement**: Bright cheeks, forehead, and highlights become peaks. Dark eye sockets and shadows become valleys.
3. **Increase deflection**: Push Deflection to 80%. The terrain becomes more extreme — features stretch and overlap.
4. **Flip direction**: Toggle Direction from Up to Down. The entire terrain inverts — peaks become valleys and vice versa.
5. **Invert luminance**: Toggle Invert. Now dark features produce the peaks. Compare the four combinations of Direction × Invert.

**Key concepts**: Luminance maps to vertical displacement, displacement gain controls terrain height, direction flips the polarity, invert swaps which features drive the displacement

---

### Exercise 2: Phosphor Persistence Display

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: massif_source1_fruit, after: massif_ex2_s1 },
    { label: "Runner", before: massif_source2_runner, after: massif_ex2_s2 },
    { label: "Clouds", before: massif_source3_clouds, after: massif_ex2_s3 },
    { label: "Pattern", before: massif_source4_pattern, after: massif_ex2_s4 },
    { label: "Man", before: massif_source5_man, after: massif_ex2_s5 },
    { label: "Knit", before: massif_source6_knit, after: massif_ex2_s6 },
  ]}
/>
*Phosphor Persistence Display — simulated result across source images.*
**Source**: Slow-moving or static footage — a slowly rotating object, a dimly lit scene, or a slow pan across a landscape.

**Objective**: Explore the decay and persistence behavior of the column buffer, creating CRT phosphor glow effects.

1. **Set moderate deflection**: Deflection ~50% to create a clear terrain.
2. **Enable phosphor tint**: Set Color to Mono. Choose a green tint (~0°) for classic P1 phosphor or amber (~90°) for P3.
3. **Increase decay**: Set Decay to ~80%. Previously bright terrain peaks now persist across frames, creating glowing trails.
4. **Add line gaps**: Set Line Gap to ~6 lines. The raster-line spacing creates the characteristic CRT scan-line look.
5. **Add edge enhancement**: Increase Edge Enh to ~40%. Contour edges glow more brightly, creating a wireframe overlay on the terrain.
6. **Maximum persistence**: Push Decay to ~95%. The terrain accumulates bright features over many frames, building up a luminous relief map.

**Key concepts**: Decay controls phosphor persistence via per-frame buffer attenuation, max-brightness compositing accumulates the brightest features, line gaps create CRT raster-line spacing, tint hue simulates phosphor color

---

### Exercise 3: Perspective Landscape

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: massif_source1_fruit, after: massif_ex3_s1 },
    { label: "Runner", before: massif_source2_runner, after: massif_ex3_s2 },
    { label: "Clouds", before: massif_source3_clouds, after: massif_ex3_s3 },
    { label: "Pattern", before: massif_source4_pattern, after: massif_ex3_s4 },
    { label: "Man", before: massif_source5_man, after: massif_ex3_s5 },
    { label: "Knit", before: massif_source6_knit, after: massif_ex3_s6 },
  ]}
/>
*Perspective Landscape — simulated result across source images.*
**Source**: Wide-angle footage — a cityscape, landscape, or any image with content distributed across the full frame height.

**Objective**: Build a full perspective terrain with foreshortening, creating a vanishing-point 3D landscape from flat video.

1. **Start with Exercise 2 settings**: Moderate deflection, green phosphor tint, some decay.
2. **Enable perspective**: Toggle Perspect to On. Immediately the bottom of the frame shows more displacement than the top.
3. **Increase perspective amount**: Push the Perspective knob to ~70%. The foreshortening becomes dramatic — towering peaks at the bottom, compressed ridges at the top.
4. **Enable fill hold**: Toggle Fill Mode to Hold. The gaps between terrain lines fill with the held value, creating a solid surface instead of a raster-line display.
5. **Try source color**: Switch Color to Source. The terrain retains the original video colors, creating a colorful 3D landscape.
6. **Combine with edge enhancement**: Add Edge Enh ~50% to highlight the contour ridges in the perspective terrain.

**Key concepts**: Perspective scales displacement by vertical position for vanishing-point depth, hold fill mode creates solid terrain surfaces, source color preserves original chrominance through the column buffer

---


## Tips

- **No bypass toggle**: Like Marquee, Massif uses Toggle 11 for Invert rather than bypass. Set the Mix fader to 0% for instant A/B comparison.
- **Start with moderate deflection**: High deflection values create extreme terrain that can be hard to read. Start at 30–50% and increase gradually.
- **Green phosphor for authenticity**: Set Tint Hue to ~0° and Color to Mono for a classic P1 CRT phosphor look. Amber (~90°) evokes warm vintage monitors.
- **Decay shapes the persistence**: Low decay clears the buffer quickly, showing each frame in isolation. High decay builds up cumulative terrain over many frames — ideal for slow-moving material.
- **Perspective needs Perspect toggle**: The Perspective knob only takes effect when the Perspect toggle is On. Without the toggle, displacement is uniform across all scan lines.
- **Fill Hold for solid surfaces**: Toggle Fill Mode to Hold to eliminate the raster-line gaps, creating a solid terrain surface instead of individual scan lines floating in black space.
- **Four displacement polarities**: Combine Direction (Up/Down) × Invert (Normal/Invert) for four distinct terrain characters from the same source material.
- **Feedback creates layered terrain**: Route the output back to the input for recursive displacement — each pass deepens the terrain, creating multi-layered mountain formations.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated FPGA memory used for the 1024-entry column buffers that store the terrain data. |
| **Column Buffer** | A vertical memory array (1024 × 10-bit) storing one pixel-column of the displaced terrain. Three buffers store Y, U, and V independently. |
| **CRT** | Cathode Ray Tube; the display technology whose electron-beam deflection and phosphor persistence Massif emulates digitally. |
| **Decay** | Inter-frame attenuation of the column buffer, simulating the gradual fading of CRT phosphor after excitation. |
| **Deflection** | Vertical displacement of a scan line based on its luminance value, the core operation of the Rutt/Etra technique. |
| **Foreshortening** | Perspective scaling where objects closer to the viewer appear larger and more displaced, creating depth illusion. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Luminance** | The brightness component (Y) of a YUV video signal; in Massif, the primary driver of vertical displacement. |
| **Max-Brightness Compositing** | A write policy where only the brightest pixel value is retained when multiple sources target the same buffer address. |
| **Persistence** | The visual afterglow of CRT phosphor, simulated by high Decay values that slow the buffer attenuation. |
| **Pipeline** | Sequential processing stages where each stage's output feeds the next on every clock cycle. |
| **Raster** | The pattern of horizontal scan lines that compose a video frame; Line Gap controls the spacing of these lines in the terrain display. |
| **Rutt/Etra** | A 1973 analog video synthesizer by Steve Rutt and Bill Etra that deflected CRT scan lines by luminance, creating terrain-like video displays. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
