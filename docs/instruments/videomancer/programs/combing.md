---
draft: true
sidebar_position: 61
slug: /instruments/videomancer/combing
title: "Combing"
image: /img/instruments/videomancer/combing/combing_hero_s1.png
description: "Before the world went progressive, all television was interlaced."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import combing_control_panel from '/img/instruments/videomancer/combing/combing_control_panel.png';
import combing_source1_fruit from '/img/instruments/videomancer/combing/combing_source1_fruit.png';
import combing_source2_field from '/img/instruments/videomancer/combing/combing_source2_field.png';
import combing_source3_clouds from '/img/instruments/videomancer/combing/combing_source3_clouds.png';
import combing_source4_pattern from '/img/instruments/videomancer/combing/combing_source4_pattern.png';
import combing_source5_boy from '/img/instruments/videomancer/combing/combing_source5_boy.png';
import combing_source6_berries from '/img/instruments/videomancer/combing/combing_source6_berries.png';
import combing_hero_s1 from '/img/instruments/videomancer/combing/combing_hero_s1.png';
import combing_hero_s2 from '/img/instruments/videomancer/combing/combing_hero_s2.png';
import combing_hero_s3 from '/img/instruments/videomancer/combing/combing_hero_s3.png';
import combing_hero_s4 from '/img/instruments/videomancer/combing/combing_hero_s4.png';
import combing_hero_s5 from '/img/instruments/videomancer/combing/combing_hero_s5.png';
import combing_hero_s6 from '/img/instruments/videomancer/combing/combing_hero_s6.png';
import combing_ex1_s1 from '/img/instruments/videomancer/combing/combing_ex1_s1.png';
import combing_ex1_s2 from '/img/instruments/videomancer/combing/combing_ex1_s2.png';
import combing_ex1_s3 from '/img/instruments/videomancer/combing/combing_ex1_s3.png';
import combing_ex1_s4 from '/img/instruments/videomancer/combing/combing_ex1_s4.png';
import combing_ex1_s5 from '/img/instruments/videomancer/combing/combing_ex1_s5.png';
import combing_ex1_s6 from '/img/instruments/videomancer/combing/combing_ex1_s6.png';
import combing_ex2_s1 from '/img/instruments/videomancer/combing/combing_ex2_s1.png';
import combing_ex2_s2 from '/img/instruments/videomancer/combing/combing_ex2_s2.png';
import combing_ex2_s3 from '/img/instruments/videomancer/combing/combing_ex2_s3.png';
import combing_ex2_s4 from '/img/instruments/videomancer/combing/combing_ex2_s4.png';
import combing_ex2_s5 from '/img/instruments/videomancer/combing/combing_ex2_s5.png';
import combing_ex2_s6 from '/img/instruments/videomancer/combing/combing_ex2_s6.png';
import combing_ex3_s1 from '/img/instruments/videomancer/combing/combing_ex3_s1.png';
import combing_ex3_s2 from '/img/instruments/videomancer/combing/combing_ex3_s2.png';
import combing_ex3_s3 from '/img/instruments/videomancer/combing/combing_ex3_s3.png';
import combing_ex3_s4 from '/img/instruments/videomancer/combing/combing_ex3_s4.png';
import combing_ex3_s5 from '/img/instruments/videomancer/combing/combing_ex3_s5.png';
import combing_ex3_s6 from '/img/instruments/videomancer/combing/combing_ex3_s6.png';

# Combing

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: combing_source1_fruit, after: combing_hero_s1 },
    { label: "Field", before: combing_source2_field, after: combing_hero_s2 },
    { label: "Clouds", before: combing_source3_clouds, after: combing_hero_s3 },
    { label: "Pattern", before: combing_source4_pattern, after: combing_hero_s4 },
    { label: "Boy", before: combing_source5_boy, after: combing_hero_s5 },
    { label: "Berries", before: combing_source6_berries, after: combing_hero_s6 },
  ]}
/>
*Combing applying alternating-scanline interlace artifacts and checkerboard patterning to create structured temporal interference in the video signal.*

---

## Overview

Before the world went progressive, all television was *interlaced*. Each frame was split into two fields — one containing the odd-numbered scanlines, the other the even — transmitted in alternation at 50 or 60 fields per second. When an interlaced signal is displayed on a progressive monitor without proper deinterlacing, the two fields become visible simultaneously, creating a characteristic **comb** pattern along the edges of moving objects. Horizontal lines of the current field alternate with lines from the previous field, producing a set of teeth along every motion boundary.

Combing recreates this artifact synthetically. It operates three line-delay buffers (one per Y, U, V channel), each storing a full 1024-pixel scanline. The program alternates between the live input and the delayed scanline on consecutive lines, creating a one-line temporal offset that mimics comb artifacts. The alternation pattern can be driven by a configurable line offset, animated over time, or switched to a two-dimensional checkerboard mode that creates a grid-like interference pattern across both axes.

The Blend control crossfades between the live and delayed signals, allowing the comb teeth to range from hard binary alternation to soft, ghostly interlace shimmer. Combined with contrast and brightness processing, Combing can simulate everything from subtle broadcast interlace artifacts to aggressive pattern-based video decomposition.

---

## Quick Start

1. **Subtle shimmer**: Low Comb Depth (~20%) with Blend at ~50% creates a barely perceptible interlace shimmer that adds analog broadcast character without obvious artifacts.
2. **Checkerboard for texture**: Checkerboard mode at moderate depth creates a fine mesh overlay that interacts beautifully with source detail.
3. **Animation for life**: Enable Animate to prevent the comb pattern from looking static and digital. The continuous drift adds natural temporal variation.

---

## Background

### What Is Interlace Combing?

Interlace was the dominant television scanning format for over 60 years. Each frame was split into two **fields** — odd lines first, even lines next — each captured at a slightly different moment in time. When a scene contains motion, the two fields show the moving object at different positions. Displaying both fields simultaneously (progressive playback) produces a characteristic **comb** artifact: along the edges of moving objects, alternating scanlines show different positions, creating a tooth-like pattern. Combing simulates this artifact by alternating between the current input and a one-line-delayed version, reproducing the temporal displacement of interlaced fields.

### What Is Checkerboard Patterning?

While interlace combing creates horizontal line-by-line alternation, **checkerboard** patterning extends the alternation to both dimensions — every other pixel on every other line comes from the delayed signal. The result is a fine grid where live and delayed pixels alternate in both the horizontal and vertical directions. This pattern appears in various digital video pathologies, including certain types of chroma subsampling artifacts and dithered rendering. Combing implements this by XORing the line-parity signal with a per-pixel toggle, creating the characteristic two-dimensional alternation.

### What Is a Line Buffer?

A **line buffer** is a block of memory that stores one complete scanline of video data. By writing pixels into the buffer as they arrive and reading them out one line later, the buffer creates a one-scanline delay — the fundamental building block of vertical filtering and interlace simulation. Combing uses three 1024×10-bit line buffers (one per YUV channel), implemented in FPGA block RAM, providing exactly one scanline of delay for each color component independently.


---

## Signal Flow

Y/U/V Channels → Y Post-Processing → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y/U/V Channels ─────────────────────────────────────────────
│   │
│   ├─ 1. Line Buffer Write     (store current pixel to BRAM)
│   ├─ 2. Line Buffer Read      (retrieve previous-line pixel)
│   ├─ 3. Phase Computation     (line_count + offset + animation)
│   ├─ 4. Pattern Selection     (Lines: line parity; Checker: XOR pixel parity)
│   ├─ 5. Mux: Live / Delayed   (select based on pattern phase)
│   └─ 6. Blend                 (crossfade between live and muxed)
│
├── Y Post-Processing ──────────────────────────────────────────
│   │
│   ├─ 7. Contrast             (gain around midpoint)
│   ├─ 8. Brightness           (DC offset)
│   └─ 9. Fade                 (final output level)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The key interaction is between the phase computation and the pattern mode. In Lines mode, the alternation pattern depends only on the vertical scanline count plus an offset — creating purely horizontal comb artifacts. In Checkerboard mode, the pixel position is XORed with the line parity, creating a two-dimensional grid. The Blend control then determines how strongly the delayed signal replaces the live signal: at 0%, the output is entirely live (no combing visible); at 100%, the alternation is a hard binary switch between live and delayed pixels. Animation adds a time-varying offset to the phase, causing the comb pattern to drift vertically over time.

---

## Parameter Reference

<img src={combing_control_panel} alt="Videomancer front panel with Combing loaded"/>
*Videomancer's front panel with Combing active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Comb Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

At 0%, the live and delayed signals contribute equally to every pixel — no visible combing. As Comb Depth increases, the alternation between live and delayed becomes more pronounced. At 100%, the full delayed signal replaces the live signal on alternate lines (or pixels in checkerboard mode), creating the maximum comb artifact. This control determines the visibility and intensity of the interlace simulation. Internally, controls the strength of the comb pattern.

---

#### Knob 2 — Blend
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Crossfades between the combed output and the original live input. At 0%, the output is entirely the original signal regardless of Comb Depth. At 100%, the full combed signal passes through. Intermediate values create a ghost-like blend where the comb pattern is visible but semi-transparent. This control is useful for dialing in subtle interlace shimmer without committing to full binary alternation.

---

#### Knob 3 — Line Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Shifts the phase of the comb pattern vertically. Increasing the Line Offset moves the alternation boundary — lines that were showing live signal switch to delayed, and vice versa. At 0%, even lines show live and odd lines show delayed. Sweeping this control provides continuous vertical scrolling of the comb pattern. In checkerboard mode, the offset shifts the grid pattern vertically.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies gain around the midpoint (512) to the luminance channel after combing. Values above center increase contrast, pushing bright pixels brighter and dark pixels darker. Values below center reduce contrast, compressing the tonal range toward mid-gray. The contrast is applied after the comb processing, so it affects the already-combed signal.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC offset to the luminance channel after contrast processing. Controls the overall brightness of the output. At center position, no offset is applied. Above center brightens, below center darkens.

---

#### Knob 6 — Fade
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

At 100%, the processed signal passes at full level. At 0%, the output fades to black. Acts as a master output level control applied after all comb processing, contrast, and brightness adjustments. Internally, controls the final output amplitude.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Field** | Odd | Even |
| **8 — Pattern** | Lines | Checker |
| **9 — Animate** | Off | On |
| **10 — Invert Y** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent parameters. Field selects the starting field polarity. Pattern chooses between line-based and checkerboard alternation. Animate adds temporal evolution to the comb pattern. Invert Y provides a luminance polarity reversal. Bypass enables instant comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Combing processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Combing-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from basic interlace simulation to creative pattern-based video decomposition using the comb filter and its modifiers.

### Exercise 1: Broadcast Interlace Simulation

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: combing_source1_fruit, after: combing_ex1_s1 },
    { label: "Field", before: combing_source2_field, after: combing_ex1_s2 },
    { label: "Clouds", before: combing_source3_clouds, after: combing_ex1_s3 },
    { label: "Pattern", before: combing_source4_pattern, after: combing_ex1_s4 },
    { label: "Boy", before: combing_source5_boy, after: combing_ex1_s5 },
    { label: "Berries", before: combing_source6_berries, after: combing_ex1_s6 },
  ]}
/>
*Broadcast Interlace Simulation — simulated result across source images.*
**Source**: Video footage with moderate motion — a person walking, traffic, or a slowly panning camera.

**What You'll Create**: Recreate the characteristic comb artifacts of improperly deinterlaced broadcast video.

1. **Basic combing**: Set Comb Depth to ~80% and Blend to ~100%. The output shows alternating scanlines from the current and previous field — the classic comb pattern is visible along motion boundaries.
2. **Field polarity**: Toggle the Field switch. Notice the comb pattern shifts by one line — odd vs. even field dominance.
3. **Reduce blend**: Lower Blend to ~50%. The comb teeth become ghostly and semi-transparent rather than hard binary alternation.
4. **Line offset sweep**: Slowly sweep Line Offset. The comb pattern scrolls vertically, simulating field-alignment drift.
5. **Natural combing**: Set Comb Depth ~40%, Blend ~60% for a subtle interlace shimmer like a poorly calibrated TV monitor.

**Key concepts**: Interlace combing is caused by temporal offset between odd and even fields, comb depth controls the field separation, blend controls the mixing ratio

---

### Exercise 2: Checkerboard Decomposition

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: combing_source1_fruit, after: combing_ex2_s1 },
    { label: "Field", before: combing_source2_field, after: combing_ex2_s2 },
    { label: "Clouds", before: combing_source3_clouds, after: combing_ex2_s3 },
    { label: "Pattern", before: combing_source4_pattern, after: combing_ex2_s4 },
    { label: "Boy", before: combing_source5_boy, after: combing_ex2_s5 },
    { label: "Berries", before: combing_source6_berries, after: combing_ex2_s6 },
  ]}
/>
*Checkerboard Decomposition — simulated result across source images.*
**Source**: A still image or slow-moving footage with fine detail — text, geometric patterns, or fabric textures.

**What You'll Create**: Explore the two-dimensional checkerboard pattern and its visual effects.

1. **Switch to checkerboard**: Enable Checkerboard mode (Switch 8). The alternation pattern changes from horizontal stripes to a fine grid.
2. **Full depth**: Set Comb Depth to 100%. Every other pixel on every other line shows the delayed signal, creating a checkerboard mosaic.
3. **Contrast enhancement**: Increase Contrast to ~70%. The checkerboard pattern becomes more defined as the tonal difference between live and delayed pixels is amplified.
4. **Animate**: Enable Animate (Switch 9). The checkerboard pattern begins to crawl, creating a shimmering mesh effect.
5. **Fade sculpting**: Lower Fade to ~60% and observe how the pattern darkens into a structured vignette.

**Key concepts**: Checkerboard extends alternation to both axes, animation creates temporal shimmer, contrast amplifies the pattern visibility

---

### Exercise 3: Animated Drift and Pattern Blending

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: combing_source1_fruit, after: combing_ex3_s1 },
    { label: "Field", before: combing_source2_field, after: combing_ex3_s2 },
    { label: "Clouds", before: combing_source3_clouds, after: combing_ex3_s3 },
    { label: "Pattern", before: combing_source4_pattern, after: combing_ex3_s4 },
    { label: "Boy", before: combing_source5_boy, after: combing_ex3_s5 },
    { label: "Berries", before: combing_source6_berries, after: combing_ex3_s6 },
  ]}
/>
*Animated Drift and Pattern Blending — simulated result across source images.*
**Source**: Any footage — the effect is primarily pattern-driven rather than content-dependent.

**What You'll Create**: Combine animation, blending, and contrast for evolving pattern-based video textures.

1. **Moderate combing**: Set Comb Depth ~60%, Blend ~70%.
2. **Animate**: Enable Animation (Switch 9). The comb pattern scrolls vertically, creating a rolling shutter-like drift.
3. **Line offset**: Set Line Offset to ~40%. This adds a static offset to the animated pattern, shifting the starting position of the drift.
4. **Contrast and brightness**: Increase Contrast to ~75%, set Brightness to ~40% for a darker, more contrasty look.
5. **Invert Y**: Toggle Invert Y (Switch 10). The negative image reveals the comb pattern structure differently — dark teeth become bright.
6. **Pattern comparison**: Quickly switch between Lines and Checkerboard modes to compare the two-pattern character in motion.

**Key concepts**: Animation adds temporal evolution to static patterns, contrast shapes the visual weight of the comb teeth, inversion reveals complementary pattern structure

---


## Tips

- **Contrast shapes teeth**: Increasing contrast after combing amplifies the tonal difference between live and delayed lines, making the comb teeth sharper and more visible.
- **Fade for vignette**: Use the Fade control to darken the combed output, creating a processed-looking signal that sits well in a mix.
- **Feedback loops**: Route the output back to the input. The one-line delay creates recursive vertical shifting that builds complex stripe patterns over successive passes.

---

## Glossary

| Term | Definition |
|------|------------|
| **Comb Artifact** | A visual defect in interlaced video where alternating scanlines show temporal offset, creating tooth-like edges along motion boundaries. |
| **Field** | One half of an interlaced video frame, containing either all odd-numbered or all even-numbered scanlines. |
| **Interlace** | A scanning method where each frame is divided into two fields (odd and even lines), transmitted in alternation. |
| **Line Buffer** | A memory block storing one complete scanline, creating a one-line delay for vertical filtering operations. |
| **Progressive** | A scanning method where all lines of a frame are captured and displayed in sequential order, without field splitting. |

---
