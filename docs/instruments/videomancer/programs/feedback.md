---
draft: true
sidebar_position: 109
slug: /instruments/videomancer/feedback
title: "Feedback"
image: /img/instruments/videomancer/feedback/feedback_hero_s1.png
description: "Feedback is one of the most powerful techniques in analog video synthesis — point a camera at its own monitor, and the image folds into itself endlessly, creating spiraling tunnels, ghost trails, and self-similar fractal structures."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import feedback_control_panel from '/img/instruments/videomancer/feedback/feedback_control_panel.png';
import feedback_source1_skull from '/img/instruments/videomancer/feedback/feedback_source1_skull.png';
import feedback_source2_runner from '/img/instruments/videomancer/feedback/feedback_source2_runner.png';
import feedback_source3_clouds from '/img/instruments/videomancer/feedback/feedback_source3_clouds.png';
import feedback_source4_pattern from '/img/instruments/videomancer/feedback/feedback_source4_pattern.png';
import feedback_source5_girl from '/img/instruments/videomancer/feedback/feedback_source5_girl.png';
import feedback_source6_knit from '/img/instruments/videomancer/feedback/feedback_source6_knit.png';
import feedback_hero_s1 from '/img/instruments/videomancer/feedback/feedback_hero_s1.png';
import feedback_hero_s2 from '/img/instruments/videomancer/feedback/feedback_hero_s2.png';
import feedback_hero_s3 from '/img/instruments/videomancer/feedback/feedback_hero_s3.png';
import feedback_hero_s4 from '/img/instruments/videomancer/feedback/feedback_hero_s4.png';
import feedback_hero_s5 from '/img/instruments/videomancer/feedback/feedback_hero_s5.png';
import feedback_hero_s6 from '/img/instruments/videomancer/feedback/feedback_hero_s6.png';
import feedback_ex1_s1 from '/img/instruments/videomancer/feedback/feedback_ex1_s1.png';
import feedback_ex1_s2 from '/img/instruments/videomancer/feedback/feedback_ex1_s2.png';
import feedback_ex1_s3 from '/img/instruments/videomancer/feedback/feedback_ex1_s3.png';
import feedback_ex1_s4 from '/img/instruments/videomancer/feedback/feedback_ex1_s4.png';
import feedback_ex1_s5 from '/img/instruments/videomancer/feedback/feedback_ex1_s5.png';
import feedback_ex1_s6 from '/img/instruments/videomancer/feedback/feedback_ex1_s6.png';
import feedback_ex2_s1 from '/img/instruments/videomancer/feedback/feedback_ex2_s1.png';
import feedback_ex2_s2 from '/img/instruments/videomancer/feedback/feedback_ex2_s2.png';
import feedback_ex2_s3 from '/img/instruments/videomancer/feedback/feedback_ex2_s3.png';
import feedback_ex2_s4 from '/img/instruments/videomancer/feedback/feedback_ex2_s4.png';
import feedback_ex2_s5 from '/img/instruments/videomancer/feedback/feedback_ex2_s5.png';
import feedback_ex2_s6 from '/img/instruments/videomancer/feedback/feedback_ex2_s6.png';
import feedback_ex3_s1 from '/img/instruments/videomancer/feedback/feedback_ex3_s1.png';
import feedback_ex3_s2 from '/img/instruments/videomancer/feedback/feedback_ex3_s2.png';
import feedback_ex3_s3 from '/img/instruments/videomancer/feedback/feedback_ex3_s3.png';
import feedback_ex3_s4 from '/img/instruments/videomancer/feedback/feedback_ex3_s4.png';
import feedback_ex3_s5 from '/img/instruments/videomancer/feedback/feedback_ex3_s5.png';
import feedback_ex3_s6 from '/img/instruments/videomancer/feedback/feedback_ex3_s6.png';

# Feedback

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: feedback_source1_skull, after: feedback_hero_s1 },
    { label: "Runner", before: feedback_source2_runner, after: feedback_hero_s2 },
    { label: "Clouds", before: feedback_source3_clouds, after: feedback_hero_s3 },
    { label: "Pattern", before: feedback_source4_pattern, after: feedback_hero_s4 },
    { label: "Girl", before: feedback_source5_girl, after: feedback_hero_s5 },
    { label: "Knit", before: feedback_source6_knit, after: feedback_hero_s6 },
  ]}
/>
*Feedback applying recursive pixel-buffer accumulation with zoom, color rotation, and decay to produce self-referencing tunnel and trail effects.*

---

## Overview

Feedback is one of the most powerful techniques in analog video synthesis — point a camera at its own monitor, and the image folds into itself endlessly, creating spiraling tunnels, ghost trails, and self-similar fractal structures. This recursive loop, where the output becomes the input, generates visual complexity far beyond what any single-pass effect can produce.

Feedback implements a digital approximation of this analog process using circular pixel buffers. Each channel (Y, U, V) writes incoming pixels into a 512-sample ring buffer and simultaneously reads from an offset position, creating a spatial displacement. The read offset grows linearly across the scanline, producing a perspective-like zoom effect where the displaced image converges toward or diverges from a vanishing point. The read-back value is mixed with the current input, and the result is written back into the buffer — creating the essential recursive loop that accumulates information over time.

Color Shift rotates the chroma toward its complement during each feedback pass, causing successive iterations to cycle through hues. Gain amplifies the luminance of the feedback signal, intensifying bright elements with each pass. Decay controls how quickly old information fades, setting the trail length of the recursive accumulation. The result spans a wide range — from subtle ghosting trails to deep recursive tunnels with rainbow color evolution.

---

## Quick Start

1. **Decay is the memory knob**: Think of Decay as how long the system "remembers." Low decay = short memory (quick trails). High decay = long memory (deep tunnels).
2. **Gain excites the system**: Gain above center causes self-amplification. Start with moderate gain and increase slowly — the system can quickly bloom into saturation.
3. **Color Shift for psychedelia**: Even small amounts of Color Shift create rainbow trails. Maximum shift produces a full spectrum cycle every ~8 feedback generations.

---

## Background

### What Is Video Feedback?

**Video feedback** occurs when a video camera's output is routed back to its own input — either optically (pointing a camera at its monitor) or electronically (routing the output signal back to the input). Each frame contains the previous frame, which contains the frame before that, ad infinitum. With each pass through the system, the image is slightly transformed by the camera's and monitor's imperfections — zoom, pan, brightness shifts, color drift. This recursive process generates self-similar structures reminiscent of fractals, and it became a foundational technique in video art during the 1960s and 1970s, pioneered by artists like Nam June Paik and the Vasulkas.

### What Is a Circular Buffer?

A **circular buffer** (or ring buffer) is a fixed-size memory that wraps around — when the write pointer reaches the end, it returns to the beginning, overwriting the oldest data. Feedback uses three 512-sample circular buffers (one per YUV channel). Each pixel is written at the current write address and read from an offset address behind the write pointer. Because the buffer wraps, the read address can lag the write address by any amount up to the buffer's full length, accessing pixels from earlier on the current scanline. The offset determines the spatial displacement — how far "back" in the scanline the feedback reaches.

### What Is Recursive Accumulation?

In Feedback's architecture, the value written to the buffer is not simply the current input — it is a weighted mixture of the current input and the value read from the buffer. This creates a **recursive accumulation**: each buffer cell contains a blend of the new pixel and whatever was there before from previous scanlines and frames. Over time, with decay less than 100%, old information gradually fades while new information accumulates. The decay rate determines the "trail length" — how many iterations of feedback are visible before they fade to invisibility.


---

## Signal Flow

Y/U/V Channels → Y Post-Processing → Control → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y/U/V Channels ─────────────────────────────────────────────
│   │
│   ├─ 1. Write to Buffer       (circular 512×10 BRAM, write at wr_addr)
│   ├─ 2. Read from Buffer      (offset = grows across scanline for zoom)
│   ├─ 3. Gain (Y only)         (amplify feedback luminance)
│   ├─ 4. Color Shift (UV only) (rotate toward complement: blend UV ↔ neg-UV)
│   ├─ 5. Decay Mix             (blend: input × (1−decay) + feedback × decay)
│   └─ 6. Write-Back            (mixed result → buffer for next iteration)
│
├── Y Post-Processing ──────────────────────────────────────────
│   │
│   └─ 7. Brightness Offset     (DC shift)
│
├── Control ────────────────────────────────────────────────────
│   │
│   ├─ X Offset                 (shifts read-address origin left/right)
│   └─ Freeze                   (holds frame counter and buffer content)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The recursive loop is the defining feature: each pixel written into the buffer is already a mixture of the current input and the previous buffer contents. This means every pixel in the buffer contains echoes of all previous inputs, decaying geometrically over time. The zoom effect arises because the read offset increases linearly across the scanline — at the left edge, the offset is small (reading nearby pixels), and at the right edge, the offset is large (reading pixels from much earlier in the line). This creates a perspective convergence effect. The Direction toggle flips the direction of the offset growth, changing whether the zoom converges to the left or right side of the screen.

---

## Parameter Reference

<img src={feedback_control_panel} alt="Videomancer front panel with Feedback loaded"/>
*Videomancer's front panel with Feedback active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Zoom
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

At 0%, no offset growth occurs and the feedback reads from the same relative position at every pixel (no spatial zoom). As Zoom increases, the offset grows faster, creating a stronger perspective convergence. At high values, the image is dramatically pulled toward the vanishing point, with each recursive pass producing increasingly compressed copies of the original. Internally, controls the zoom factor — how quickly the read offset grows across the scanline.

---

#### Knob 2 — Gain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Amplifies the luminance of the feedback signal before it is mixed back into the buffer. At center, the feedback Y passes at unity. Above center, bright elements get amplified with each recursive pass, causing them to intensify and eventually saturate. Below center, the feedback luminance is attenuated, producing dimmer trails. High Gain combined with high Decay creates self-exciting bright regions that persist and grow across frames.

---

#### Knob 3 — Color Shift
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

Rotates the chrominance of the feedback signal toward its complement. At 0%, the UV channels are unchanged during each feedback pass — colors remain stable across iterations. As Color Shift increases, the UV values are progressively blended toward their negatives (inverted U and V), causing the color to drift toward the complementary hue with each recursive pass. Multiple iterations create a rainbow cycling effect as the feedback color rotates through the spectrum.

---

#### Knob 4 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 68% |
| Suffix | % |

At 0%, the output is entirely the live input — no feedback accumulation occurs. At 100%, the output is dominated by the buffer contents — new input barely registers, and old information persists indefinitely. Moderate values create a balance where new input gradually replaces old information, producing ghostly trails of adjustable length. Decay is the primary control for the visual "memory" of the feedback system. Internally, controls the mixing ratio between the current input and the feedback buffer.

---

#### Knob 5 — X Offset
| Property | Value |
|----------|-------|
| Range | -100% – 100% |
| Default | 0% |
| Suffix | % |

Shifts the starting read-address offset horizontally. The read address begins at `wr_addr − x_offset` and increases from there. This moves the zoom vanishing point left or right across the screen. At center, the zoom is roughly centered. At extreme values, the convergence point shifts to the edges, creating asymmetric tunnel effects.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a DC offset to the output luminance channel. Use this to lift or lower the overall brightness of the feedback-processed image. Particularly useful when high Gain settings have created overly bright self-exciting regions or when Decay settings have darkened the overall output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Direction** | Right | Left |
| **8 — Mirror** | Off | On |
| **9 — Freeze** | Off | On |
| **10 — Invert Y** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent parameters. Direction sets the zoom convergence direction. Mirror reflects the read addressing. Freeze holds the buffer state. Invert Y provides luminance polarity reversal. Bypass enables instant comparison.

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

Routes the unprocessed input signal directly to the output, bypassing all Feedback processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Feedback-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from basic spatial displacement to full recursive feedback with color evolution and zoom tunneling.

### Exercise 1: Ghost Trails

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: feedback_source1_skull, after: feedback_ex1_s1 },
    { label: "Runner", before: feedback_source2_runner, after: feedback_ex1_s2 },
    { label: "Clouds", before: feedback_source3_clouds, after: feedback_ex1_s3 },
    { label: "Pattern", before: feedback_source4_pattern, after: feedback_ex1_s4 },
    { label: "Girl", before: feedback_source5_girl, after: feedback_ex1_s5 },
    { label: "Knit", before: feedback_source6_knit, after: feedback_ex1_s6 },
  ]}
/>
*Ghost Trails — simulated result across source images.*
**Source**: A slowly moving subject — a hand, a swinging pendulum, or slowly panning footage.

**What You'll Create**: Learn how Decay creates persistence trails from moving objects.

1. **Basic trails**: Set Zoom to 0% (no zoom), Gain to center, Color Shift to 0%, Decay to ~70%. Moving elements leave ghostly trails that fade over ~1 second.
2. **Trail length**: Increase Decay toward 100%. Trails persist longer. Decrease Decay toward 0%. Trails shorten until they disappear entirely.
3. **Bright trails**: Increase Gain above center. The trails become brighter with each iteration, creating intensifying echoes.
4. **Color evolution**: Slowly increase Color Shift. Each trail generation shifts in hue, creating a rainbow gradient across the trail history.
5. **Freeze capture**: Enable Freeze (Switch 9) during an interesting trail pattern. The trails persist indefinitely, creating a time-exposure composite.

**Key concepts**: Decay sets trail persistence, gain controls trail intensity, color shift creates spectral evolution across iterations

---

### Exercise 2: Zoom Tunnel

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: feedback_source1_skull, after: feedback_ex2_s1 },
    { label: "Runner", before: feedback_source2_runner, after: feedback_ex2_s2 },
    { label: "Clouds", before: feedback_source3_clouds, after: feedback_ex2_s3 },
    { label: "Pattern", before: feedback_source4_pattern, after: feedback_ex2_s4 },
    { label: "Girl", before: feedback_source5_girl, after: feedback_ex2_s5 },
    { label: "Knit", before: feedback_source6_knit, after: feedback_ex2_s6 },
  ]}
/>
*Zoom Tunnel — simulated result across source images.*
**Source**: Any footage with clear visual elements — faces, geometric shapes, or high-contrast scenes.

**What You'll Create**: Create the classic video feedback zoom tunnel effect.

1. **Enable zoom**: Set Zoom to ~40%, Decay to ~80%, Gain to ~55%. A converging zoom effect appears as the feedback recursion creates smaller copies of the image nested inside each other.
2. **Direction**: Toggle Direction (Switch 7) to switch which side of the screen the tunnel converges toward.
3. **Mirror symmetry**: Enable Mirror (Switch 8). The tunnel becomes symmetric around the center, creating a kaleidoscope-like convergence.
4. **Color cycling**: Increase Color Shift to ~60%. Each nested copy cycles further through the spectrum, creating a rainbow tunnel.
5. **Adjust vanishing point**: Sweep X Offset to move the convergence point across the frame.

**Key concepts**: Zoom creates perspective convergence through linearly growing read offsets, mirror produces bilateral symmetry, each recursive iteration applies all transformations cumulatively

---

### Exercise 3: Self-Exciting Feedback

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: feedback_source1_skull, after: feedback_ex3_s1 },
    { label: "Runner", before: feedback_source2_runner, after: feedback_ex3_s2 },
    { label: "Clouds", before: feedback_source3_clouds, after: feedback_ex3_s3 },
    { label: "Pattern", before: feedback_source4_pattern, after: feedback_ex3_s4 },
    { label: "Girl", before: feedback_source5_girl, after: feedback_ex3_s5 },
    { label: "Knit", before: feedback_source6_knit, after: feedback_ex3_s6 },
  ]}
/>
*Self-Exciting Feedback — simulated result across source images.*
**Source**: High-contrast footage or even a blank/black input — the feedback system can generate its own content.

**What You'll Create**: Push the feedback system into self-exciting oscillation where internal noise and gain produce emergent visual structures.

1. **High gain**: Set Gain to ~80%. Set Decay to ~90%. Set Zoom to ~30%.
2. **Seed it**: Feed a brief flash of bright input (or move a light across the camera). The bright pixels amplify through the recursive loop.
3. **Watch the build**: Over several seconds, the recursive amplification produces structures that grow, bloom, and evolve on their own.
4. **Color evolution**: Set Color Shift to ~70%. The self-exciting structures cycle through colors as they evolve.
5. **Freeze snapshot**: Enable Freeze during a peak moment. The frozen pattern continues to be transformed by the read-offset zoom.
6. **Remove input**: Lower Mix to see how the feedback system sustains itself even with minimal external input.

**Key concepts**: High gain creates positive feedback loops where noise amplifies, self-exciting systems generate emergent structure, freeze captures transient patterns

---


## Tips

- **Mirror for symmetry**: Mirror mode turns asymmetric footage into kaleidoscopic patterns, doubling the visual complexity of the feedback structure.
- **Freeze for composition**: Use Freeze to capture a moment, then unfreeze to let new content interact with the frozen pattern.
- **X Offset as composition tool**: Moving the vanishing point creates dramatic asymmetric compositions — the tunnel doesn't have to be centered.
- **Feed it nothing**: Try feeding black or near-black input with high Gain. Internal noise seeds the feedback, and emergent structures appear from nothing — the system creates its own content.

---

## Glossary

| Term | Definition |
|------|------------|
| **Circular Buffer** | A fixed-size memory that wraps around: when the write pointer reaches the end, it returns to the beginning. |
| **Decay** | The rate at which old information fades in a recursive system; governs trail length and feedback depth. |
| **Feedback** | A signal processing configuration where the output is routed back to the input, creating recursive self-referencing. |
| **Gain** | Amplification of the feedback signal's luminance; values above unity cause self-excitation. |
| **Recursive Accumulation** | A process where each new value is mixed with the result of previous iterations, building up information over time. |
| **Ring Buffer** | Another name for a circular buffer. |

---
