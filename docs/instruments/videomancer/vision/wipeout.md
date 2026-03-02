---
draft: true
sidebar_position: 313
slug: /instruments/videomancer/wipeout
title: "Wipeout"
image: /img/instruments/videomancer/wipeout/wipeout_hero.png
description: "Every broadcast television viewer has seen a wipe — a geometric edge that sweeps across the screen, replacing one image with another."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import wipeout_hero from '/img/instruments/videomancer/wipeout/wipeout_hero.png';
import wipeout_control_panel from '/img/instruments/videomancer/wipeout/wipeout_control_panel.png';
import wipeout_exercise1_result from '/img/instruments/videomancer/wipeout/wipeout_exercise1_result.png';
import wipeout_exercise2_result from '/img/instruments/videomancer/wipeout/wipeout_exercise2_result.png';
import wipeout_exercise3_result from '/img/instruments/videomancer/wipeout/wipeout_exercise3_result.png';
import wipeout_source1_kodim15 from '/img/instruments/videomancer/wipeout/wipeout_source1_kodim15.png';
import wipeout_source2_kodim15_bw from '/img/instruments/videomancer/wipeout/wipeout_source2_kodim15_bw.png';
import wipeout_source3_male_1024 from '/img/instruments/videomancer/wipeout/wipeout_source3_male_1024.png';

# Wipeout

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: wipeout_source1_kodim15, after: wipeout_hero },
    { label: "Kodim15 B&W", before: wipeout_source2_kodim15_bw, after: wipeout_hero },
    { label: "Male", before: wipeout_source3_male_1024, after: wipeout_hero },
  ]}
/>
*Wipeout performing a clock wipe transition with soft edge and colored border, revealing a luminance matte beneath live video.*

---

## Overview

Every broadcast television viewer has seen a wipe — a geometric edge that sweeps across the screen, replacing one image with another. Before digital effects processors, production switchers in television studios used analog pattern generators to create these transitions, and the vocabulary of wipe shapes became a visual language of its own: barn doors, irises, venetian blinds, clock sweeps. Wipeout recreates eight of these classic transition patterns as a real-time spatial key generator.

The program computes a distance or angular key value for every pixel based on its position relative to screen center, then thresholds that value against the Transition control to determine whether each pixel shows the input video or a selectable matte color. The result is a continuously variable geometric transition with adjustable soft edge, colored border, and an optional luma-modulation mode that makes the wipe boundary reactive to the source content.

Unlike a simple crossfade, a wipe creates spatial structure — the boundary between the two images has a definite geometric shape. Wipeout's eight patterns cover the most recognizable shapes from the broadcast wipe catalog, from the utilitarian barn door to the decorative star iris.

---

## Background

### The Production Switcher Wipe

Wipe patterns trace back to the earliest video production switchers of the 1960s. The Grass Valley Group 1600 series and similar analog switchers offered pattern generators that created geometric key signals from X and Y ramp waveforms synchronized to the scanning beam. By comparing these ramps against a threshold voltage, the switcher produced a hard-edged key that could cut between two video sources. The threshold control became the "T-bar" — the physical handle that operators swept to execute a transition.

### Soft Edge and Border

A hard-edged wipe has an abrupt boundary — pixels are fully source A or fully source B with no blending. Professional switchers added soft edge by replacing the hard threshold with a linear ramp, creating a gradual transition zone where source A fades into source B. Border adds a colored stripe at the transition edge, giving the wipe a visible outline. Wipeout implements both features: Softness widens the alpha ramp, and Border Width inserts a colored band whose hue is set by the Border Color knob.

### Distance Metrics for Pattern Generation

Different wipe patterns correspond to different spatial distance functions. The barn door uses horizontal distance from center. The iris circle uses radial distance (approximated here with the efficient octagonal method: max(|x|,|y|) + 3/8 · min(|x|,|y|)). The diamond uses Manhattan distance (|x|+|y|). The clock wipe uses angular position derived from octant classification. Each metric generates a different spatial key ramp that sweeps across the screen as Transition is varied.

### Luma Modulation

When Luma Mod is enabled, the spatial key is modulated by the input video's luminance. Bright areas advance the wipe position while dark areas retard it, creating a content-reactive boundary that follows the tonal structure of the source image. This is not a standard broadcast wipe feature — it is an artistic extension that bridges geometric transitions and content-keyed compositing.

### Venetian Blinds and Checkerboard

Some patterns subdivide the screen into repeating cells. Venetian blinds create horizontal bands; checkerboard creates alternating cells in both axes. The Band Count control sets the number of repetitions. These patterns use modular arithmetic on the vertical or both position counters, creating periodic wipe structures that reveal the underlying video in multiple strips or blocks simultaneously.


---

## Signal Flow

```
Input Video (YUV 4:4:4 30-bit)
│
├── Position Counters ───────────────────────────────
│   ├─ h_count (horizontal pixel position)
│   ├─ v_count (vertical line position)
│   ├─ Centered: x = h - 640, y = v - 360
│   └─ Absolute: |x|, |y|
│
├── Pattern Generator ───────────────────────────────
│   ├─ 3-bit pattern select (8 patterns)
│   ├─ Barn Door:      |x|
│   ├─ Venetian Blinds: v_count MOD band_width
│   ├─ Clock Wipe:     octant + minor/major ratio
│   ├─ Iris Circle:    max(|x|,|y|) + 3/8 · min
│   ├─ Iris Diamond:   |x| + |y|
│   ├─ Diagonal:       (h + v) / 2
│   ├─ Checkerboard:   cell ramp ⊕ cell parity
│   └─ Star:           radial − angular modulation
│
├── Luma Modulation (optional) ──────────────────────
│   └─ wipe_key = wipe_key × input_Y >> 10
│
├── Invert Key ──────────────────────────────────────
│   └─ wipe_key = NOT wipe_key
│
├── Threshold + Softness ────────────────────────────
│   ├─ offset = wipe_key − transition
│   ├─ alpha = ramp through soft zone
│   └─ border = |offset| < border_width/2
│
├── Compositor ──────────────────────────────────────
│   ├─ Border pixel → border color (hue → YUV)
│   └─ Normal pixel → video × α + matte × (1−α)
│
├── Mix (interpolator_u) ────────────────────────────
│   └─ lerp(dry, wet, mix_amount)
│
└── Output (YUV 4:4:4 30-bit)
```

The critical interaction is between the pattern generator and the threshold stage. The pattern generator produces a 10-bit spatial key that varies smoothly across the screen according to the selected geometric function. The threshold stage converts this key into an alpha value by comparing it to the Transition control with an adjustable soft zone. The softness parameter determines whether the transition is a hard binary edge or a gradual crossfade region. Border detection runs in parallel, flagging pixels whose key value is within half the border width of the transition point.

---

## Parameter Reference

<img src={wipeout_control_panel} alt="Videomancer front panel with Wipeout loaded"/>
*Videomancer's front panel with Wipeout active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Transition
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the wipe transition position. At 0% the key is fully closed — every pixel shows the matte color. At 100% the key is fully open — every pixel shows the input video. This is the primary animation control, equivalent to the T-bar on a production switcher. The midpoint at 50% places the wipe boundary at the geometric center for symmetric patterns.

---

#### Knob 2 — Softness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 6.3% |
| Suffix | % |

Controls the width of the soft transition zone at the wipe boundary. At 0% the edge is a hard binary cut between video and matte. Increasing Softness widens the alpha ramp, creating a gradual blend zone. High softness values produce a wide, dreamy crossfade region that can occupy a significant portion of the screen.

---

#### Knob 3 — Border Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the width of the colored border stripe at the wipe edge. At 0% there is no border — the transition goes directly from video to matte. Increasing Border Width inserts a band of solid color centered on the transition point. The border is visible regardless of the softness setting, providing a distinct visual edge marker.

---

#### Knob 4 — Border Color
| Property | Value |
|----------|-------|
| Range | 0° – 359° |
| Default | 0° |
| Suffix | ° |

Sets the hue of the border stripe. The 0–359 degree range maps to six color sectors via the VHDL hue-to-YUV lookup, cycling through red, yellow, green, cyan, blue, and magenta. The border is always rendered at high luminance (Y=768) for visibility.

---

#### Knob 5 — Matte Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the luminance of the matte background that is revealed where the wipe key is closed. At 0% the matte is black; at 100% it is near-white. The matte chroma is always neutral (U=V=512), producing a grayscale background. This control determines the contrast between the matte and the input video at the wipe boundary.

---

#### Knob 6 — Band Count
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 1 |

Sets the number of repetitions for patterns that tile — specifically Venetian Blinds and Checkerboard. The steps_8 mode selects from 1 to 8 bands. More bands create finer spatial subdivisions of the wipe pattern. For non-tiling patterns (barn door, iris, etc.), this control has no visible effect.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern B0** | 0 | 1 |
| **8 — Pattern B1** | 0 | 1 |
| **9 — Pattern B2** | 0 | 1 |
| **10 — Invert Key** | Off | On |
| **11 — Luma Mod** | Off | On |

Toggles 7–9 form a 3-bit pattern selector choosing among eight wipe geometries. Toggle 10 inverts the key polarity — swapping which side shows video and which shows matte. Toggle 11 enables luma modulation, which multiplies the spatial key by the input luminance to create content-reactive transitions. There is no bypass toggle — the Mix fader at 0% serves as the effective bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input signal and the processed wipe output. At 0% the output is the unprocessed input. At 100% the output is the full wipe composite. Since Wipeout has no dedicated bypass toggle, setting Mix to 0% is the way to hear the original signal unmodified.

---

## Guided Exercises

These exercises progress from basic wipe transitions to complex content-reactive composites, exploring the interplay between pattern geometry, edge treatment, and luma modulation.

### Exercise 1: Classic Barn Door Transition

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: wipeout_source1_kodim15, after: wipeout_exercise1_result },
    { label: "Kodim15 B&W", before: wipeout_source2_kodim15_bw, after: wipeout_exercise1_result },
    { label: "Male", before: wipeout_source3_male_1024, after: wipeout_exercise1_result },
  ]}
/>
*Classic Barn Door Transition — simulated result across source images.*
**Source**: A live camera feed or recorded footage with clear subject and background.

**Objective**: Learn the basic transition controls using the simplest wipe pattern.

1. **Open the barn door**: Slowly sweep Transition from 0% to 100%. Watch the vertical split wipe reveal the video from center outward.
2. **Soften the edge**: Increase Softness to ~50%. The hard edge becomes a smooth gradient blend zone.
3. **Add a border**: Increase Border Width to ~30% and rotate Border Color through the hue range.
4. **Change the matte**: Raise Matte Y from black to mid-gray. The revealed background brightens.
5. **Invert**: Enable Invert Key. The transition direction reverses — now the center shows matte and the edges show video.

**Key concepts**: Transition is the T-bar equivalent, Softness controls the alpha ramp width, Border adds a colored stripe at the transition edge

---

### Exercise 2: Venetian Blinds and Checkerboard

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: wipeout_source1_kodim15, after: wipeout_exercise2_result },
    { label: "Kodim15 B&W", before: wipeout_source2_kodim15_bw, after: wipeout_exercise2_result },
    { label: "Male", before: wipeout_source3_male_1024, after: wipeout_exercise2_result },
  ]}
/>
*Venetian Blinds and Checkerboard — simulated result across source images.*
**Source**: High-contrast footage with strong geometric elements — architecture, signage, or test patterns.

**Objective**: Explore tiling wipe patterns and the Band Count control.

1. **Venetian blinds**: Set pattern to 001 (B0=1, B1=0, B2=0). Sweep Transition to see horizontal bands reveal the video.
2. **Band count**: Rotate Band Count through its 8 steps. Watch the number of visible bands increase.
3. **Checkerboard**: Set pattern to 110 (B0=0, B1=1, B2=1). The screen divides into alternating squares.
4. **Soft checkerboard**: Increase Softness. The sharp squares become rounded, blurred patches.
5. **Bordered tiles**: Add Border Width for a grid-line effect outlining each tile.

**Key concepts**: Band Count controls spatial subdivision frequency, tiling patterns create repeating wipe cells, softness on tiled patterns creates organic rounded shapes

---

### Exercise 3: Luma-Reactive Iris

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: wipeout_source1_kodim15, after: wipeout_exercise3_result },
    { label: "Kodim15 B&W", before: wipeout_source2_kodim15_bw, after: wipeout_exercise3_result },
    { label: "Male", before: wipeout_source3_male_1024, after: wipeout_exercise3_result },
  ]}
/>
*Luma-Reactive Iris — simulated result across source images.*
**Source**: Footage with strong tonal variation — a face against a dark background, or high-contrast still life.

**Objective**: Combine the iris circle pattern with luma modulation for content-reactive compositing.

1. **Iris circle**: Set pattern to 011 (B0=1, B1=1, B2=0). Set Transition to ~50% for a mid-screen iris.
2. **Enable Luma Mod**: Toggle Luma Mod on. The iris boundary now follows the brightness contours of the source image.
3. **Sweep transition**: Slowly sweep Transition while Luma Mod is active. Bright areas open first, dark areas open last.
4. **Add softness**: Increase Softness to blend the luma-modulated boundary.
5. **Star variant**: Switch pattern to 111 (Star). The star pattern combined with luma modulation creates complex organic boundaries.

**Key concepts**: Luma modulation multiplies the spatial key by source brightness, creating content-keyed transitions that follow image structure

---


## Tips

- **T-bar equivalent**: The Transition knob is the primary animation control — sweep it slowly for classic broadcast-style transitions, or modulate it externally for rhythmic wipe effects.
- **Softness transforms the character**: The same pattern can feel industrial (hard edge) or dreamy (maximum softness). Try maximum softness on the clock wipe for a radial gradient spotlight effect.
- **Border as grid lines**: On Checkerboard with high Band Count and moderate Border Width, the borders form a visible grid overlaying the video — useful as a compositional tool.
- **Luma Mod for organic edges**: Enable Luma Mod to break the geometric regularity of wipe patterns, creating transitions that follow the image content rather than pure geometry.
- **Mix as bypass**: Since Wipeout has no dedicated bypass toggle, use the Mix fader at 0% to pass the original signal unmodified.
- **Matte as background**: Set Matte Y to match your composition's background level. Black matte creates silhouette effects; white matte creates high-key reveals.
- **Star pattern detail**: The star pattern uses XOR-based angular modulation of the radial distance — its complexity varies with source content when Luma Mod is active.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha Blend** | Compositing method that mixes two sources using a per-pixel opacity value, producing smooth transitions between images. |
| **Barn Door** | A wipe pattern that splits the screen vertically from center, opening outward like a pair of doors. |
| **Checkerboard** | A wipe pattern dividing the screen into alternating cells that transition independently. |
| **Clock Wipe** | A wipe pattern that sweeps radially around the screen like the hand of a clock. |
| **Iris** | A wipe pattern that expands from a central point outward, masking the screen in a geometric shape. |
| **Luma Modulation** | Using the brightness of the input video to modify a processing parameter, creating content-reactive effects. |
| **Manhattan Distance** | A distance metric computed as |x| + |y|, producing diamond-shaped iso-distance contours. |
| **Matte** | A solid-color background image used as the "reveal" layer in a wipe transition. |
| **Octagonal Approximation** | An efficient method for estimating circular distance using max + 3/8·min, avoiding square root computation. |
| **Production Switcher** | A broadcast video mixing console used for live television production, featuring wipe pattern generators. |
| **Soft Edge** | A gradual transition zone at a wipe boundary, replacing a hard cut with a smooth alpha ramp. |
| **T-Bar** | The physical fader on a production switcher that controls the wipe transition position. |

---
