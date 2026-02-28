---
draft: true
sidebar_position: 108
slug: /instruments/videomancer/gauntlet
title: "Gauntlet"
image: /img/instruments/videomancer/gauntlet/gauntlet_hero.png
---

import gauntlet_hero from '/img/instruments/videomancer/gauntlet/gauntlet_hero.png';
import gauntlet_before_after from '/img/instruments/videomancer/gauntlet/gauntlet_before_after.png';
import gauntlet_control_panel from '/img/instruments/videomancer/gauntlet/gauntlet_control_panel.png';
import gauntlet_exercise1_result from '/img/instruments/videomancer/gauntlet/gauntlet_exercise1_result.png';
import gauntlet_exercise2_result from '/img/instruments/videomancer/gauntlet/gauntlet_exercise2_result.png';
import gauntlet_exercise3_result from '/img/instruments/videomancer/gauntlet/gauntlet_exercise3_result.png';

# Gauntlet

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={gauntlet_hero} alt="Gauntlet hero image"/>
*Gauntlet rendering phosphor beam traces from edge-detected video, casting green CRT glow across a high-contrast source image.*
<img src={gauntlet_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Gauntlet applied.*

---

## Overview

Every pixel of a video signal carries brightness and color — smooth gradients, soft shadows, gentle transitions. Gauntlet ignores all of that. It looks only at *edges* — the places where brightness or color changes rapidly from one pixel to the next. It detects those edges, traces them with luminous beams, and lets the beams persist as fading phosphor trails. The result looks like an oscilloscope display or a vector arcade monitor from the early 1980s: bright lines on a dark field, slowly fading as the image moves.

The program chains seven processing stages together: input conditioning (with optional luminance inversion), horizontal gradient calculation across Y, U, and V channels, threshold-based edge detection with a 16-tap sliding window, distance-based glow rendering via exponential decay lookup tables, vertical phosphor persistence through a distributed RAM line buffer, colorization into one of eight phosphor palettes, and overlay compositing. The name *Gauntlet* evokes both the arcade cabinet era (the classic Atari dungeon crawler rendered on custom vector-like hardware) and the idea of "running the gauntlet" — every pixel in the source must pass through a chain of harsh tests before it emerges as a beam trace.

At conservative settings, Gauntlet produces subtle edge highlights that follow the contours of the source material. At extreme settings, it reduces video to pure line graphics — bright phosphor traces on black, with long vertical persistence tails that smear edges across the screen like the afterglow of a radar sweep.

---

## Background

### What Is Edge Detection?

**Edge detection** is the process of identifying pixels where the signal value changes abruptly. In analog video engineering, this was accomplished with differentiation circuits — high-pass filters that responded to rapid transitions and ignored flat regions. Gauntlet implements a discrete horizontal difference: for each pixel it computes the absolute difference between the current and previous pixel values. The Y (luminance) channel is weighted double because brightness edges are perceptually dominant. U and V channel differences are added on top, so color boundaries also trigger detection even when brightness is constant.

### What Is a Sliding Window?

A **sliding window** is a fixed-length view that moves through a data stream one sample at a time. Gauntlet maintains a 16-element shift register that tracks whether each of the last 16 pixels contained an edge. When rendering glow for the current pixel, it scans this window with a **priority encoder** to find the nearest detected edge. The closer the nearest edge, the brighter the glow. This creates the characteristic beam trace appearance — a bright center line with exponentially decaying wings to either side, like the phosphor trail of an electron beam.

### What Is Phosphor Persistence?

In a cathode ray tube, the screen coating (the **phosphor**) continues to glow after the electron beam moves on. Different phosphor compounds have different decay rates and colors — P1 (green, medium persistence), P31 (blue-green, fast), P22 (amber, slow). Gauntlet simulates this by maintaining a 2048-pixel line buffer in distributed RAM. Each scanline, the buffer stores the peak glow value — the maximum of the new beam brightness and the decayed value from the previous scan. The Persistence control selects one of four decay rates, ranging from 50% per frame (fast fade, crisp traces) to 6.25% per frame (slow fade, long trails).

### What Are Phosphor Color Modes?

Real CRT monitors had fixed phosphor colors determined by the chemical coating. Gauntlet provides eight selectable color modes that map beam intensity to YUV color: **Green** (classic Battlezone / artillery simulation), **Blue-Green** (Tempest / P31), **Amber** (terminal / P22), **RGB** (derives color from the original input chroma), **Cyan** (Cinematronics vector games), **White** (monochrome oscilloscope), **Red** (radar display), and **Rainbow** (scanline-dependent hue rotation for a psychedelic multicolor beam). Each mode creates a distinct visual identity and emotional tone.

### What Is Overlay Compositing?

When displaying vector beam traces, you have two choices: **replace** the input entirely (black screen with bright lines) or **overlay** the beams on top of a dimmed version of the original. Gauntlet's overlay mode uses additive compositing — the beam intensity is added to the input (dimmed to 25% brightness). This lets the viewer see the original image content underneath the traced edges, creating a hybrid between the source footage and its edge-detected skeleton.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register           (capture + optional bitwise invert)
│   ├─ 2. Gradient                  (|Y(x)-Y(x-1)|×2 + |U| + |V|, saturated)
│   ├─ 3. Edge Detect              (threshold / gradient mode + 16-tap SR)
│   ├─ 4. Glow Render              (nearest-edge priority encoder + LUT)
│   ├─ 5. Persistence              (IIR line buffer: max(glow, decayed prev))
│   ├─ 6. Colorize                 (intensity × phosphor YUV table)
│   └─ 7. Overlay Composite        (additive over dimmed input, or replace)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Input Register           (capture, no invert)
│   ├─ 2. Gradient Feed            (|U|, |V| contribute to edge gradient)
│   ├─ 6. Colorize                 (phosphor table sets U/V; RGB mode
│   │                               uses original input chroma instead)
│   └─ 7. Overlay Composite        (beam chroma output)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ 8–11. Interpolator ×3       (wet/dry crossfade, 4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 11-clock delay pipeline     (hsync, vsync, field aligned)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The gradient calculation in Stage 2 is a weighted three-channel sum: the Y-channel difference is counted twice, then the U and V differences are added, giving a composite edge strength that fires on both brightness and color transitions. This feeds a single edge detection path — Gauntlet does not detect edges independently per channel.

Two key interactions define the program's character: (1) the 16-tap sliding window in Stage 3–4 creates a *spatial* glow halo around every detected edge, whose width is controlled by the Beam Width parameter selecting between narrow, medium, and wide exponential decay profiles; (2) the persistence IIR in Stage 5 creates *temporal* persistence, smearing beam traces vertically as successive scanlines write into and decay from the line buffer. The combination produces the distinctive CRT vector monitor look — bright traced edges with glowing tails.

**Note on unused parameters**: The current VHDL implementation declares `s_hue_offset` (Knob 5) and `s_focus` (Knob 6) as register-mapped signals, but neither is referenced in the processing pipeline. Hue Offset and Focus are reserved for future firmware revisions. Adjusting these knobs currently has no visible effect.

---

## Parameter Reference

<img src={gauntlet_control_panel} alt="Videomancer front panel with Gauntlet loaded"/>
*Videomancer's front panel with Gauntlet active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sensitivity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the edge detection threshold. At low values, even subtle brightness changes trigger edges — the display fills with traces from noise and gentle gradients. At high values, only sharp, high-contrast boundaries register, producing sparse, clean line graphics. The threshold acts as a gate: in Binary mode, any gradient above it fires at full brightness; in Gradient mode, it sets the floor below which edges are suppressed while passing through the magnitude of stronger edges proportionally.

---

#### Knob 2 — Beam Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Selects the glow falloff curve applied to detected edges. The VHDL provides three hardcoded exponential decay lookup tables — narrow, medium, and wide — selected by threshold divisions of the register value. Narrow glow produces tight, wire-thin beam traces with rapid falloff (full brightness only at the edge pixel itself). Wide glow spreads the beam energy across many pixels, creating broad, soft halos around each edge. The transition between the three LUTs is discrete, not continuous.

---

#### Knob 3 — Persistence
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the vertical phosphor decay rate. The VHDL implements four discrete decay rates selected by register value ranges: 50% decay per frame (fast — crisp traces with no visible trail), 25%, 12.5%, and 6.25% (slow — edges leave long-lasting vertical smears as subsequent scanlines accumulate decayed glow). High persistence values make the display look like a long-persistence CRT where moving edges leave glowing afterimages.

---

#### Knob 4 — Intensity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the overall beam brightness after the persistence stage. The VHDL multiplies the persisted glow value by the Intensity register, saturating at 1023. Low intensity produces dim, barely visible traces; high intensity produces searing bright beams that saturate the phosphor color table. Intensity interacts with persistence — high persistence accumulates glow over many frames, and high intensity amplifies that accumulated brightness.

---

#### Knob 5 — Hue Offset
| Property | Value |
|----------|-------|
| Range | 0.0d – 360.0d |
| Default | 0.0d |
| Suffix | d |

Labeled "Hue Offset" in the TOML metadata, this parameter is mapped to `registers_in(4)` but is not currently referenced in the processing pipeline. The signal `s_hue_offset` is declared and assigned but unused in the colorization stage. This control is reserved for a future firmware revision that may add per-pixel hue rotation to the phosphor color output. Adjusting this knob has no visible effect in the current implementation.

---

#### Knob 6 — Focus
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Labeled "Focus" in the TOML metadata, this parameter is mapped to `registers_in(5)` but is not currently referenced in the edge detection pipeline. The VHDL comment suggests it was intended to scale the sensitivity threshold, but the implementation uses Sensitivity directly (`v_threshold := s_sensitivity`). This control is reserved for a future firmware revision. Adjusting this knob has no visible effect in the current implementation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Phosphor** | Green | Blu-Grn |
| **8 — Edge Mode** | Binary | Gradient |
| **9 — Invert** | Off | On |
| **10 — Over Video** | Replace | Overlay |
| **11 — Bypass** | Off | On |

Switches 7–11 are packed into a single register (`registers_in(6)`) using the standard Videomancer toggle ABI, but with an important overlap. The Phosphor selector (Switch 7) uses bits 2:0 as a 3-bit value selecting one of eight color modes. Edge Mode (Switch 8) reads bit 1, and Invert (Switch 9) reads bit 2 — these *overlap* with the phosphor selection bits. Changing Edge Mode or Invert simultaneously modifies the effective phosphor color. Over Video (Switch 10, bit 3) and Bypass (Switch 11, bit 4) are independent and do not overlap.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the processed beam output and the delayed original input via three `interpolator_u` instances (one per YUV channel). At maximum, the output is fully processed beam traces. As the fader decreases, the original input is progressively blended in, eventually reaching the unprocessed source. This is distinct from Bypass (which is an instant switch) — the Mix fader creates a continuous crossfade between the two signals.

---

## Guided Exercises

These exercises progress from basic edge detection to full CRT vector display emulation. Each builds on the previous, adding more processing stages.

### Exercise 1: Basic Edge Detection

<img src={gauntlet_exercise1_result} alt="Basic Edge Detection result"/>
*Basic Edge Detection — simulated result across source images.*
**Source**: A live camera feed or recorded footage with high-contrast edges — architectural details, text on screen, or a geometric test pattern.

**Objective**: Learn how the edge detector and glow renderer interact to produce beam traces.

1. **See the edges**: With default settings, observe the green beam traces outlining high-contrast boundaries in the source.
2. **Adjust threshold**: Turn Sensitivity counter-clockwise to increase the threshold. Watch as fainter edges disappear, leaving only the strongest boundaries.
3. **Lower threshold**: Turn Sensitivity clockwise to reduce the threshold. The display fills with traces from subtle gradients and noise.
4. **Change glow width**: Sweep Beam Width from minimum to maximum. Watch the beam traces change from tight wireframe lines to broad, soft halos.
5. **Try Gradient mode**: Toggle Edge Mode to Gradient. The beam brightness now tracks edge sharpness — strong edges glow brightly, soft edges are dim.

**Key concepts**: Edge detection as horizontal gradient, threshold gating, binary vs gradient edge modes, glow LUT selection

---

### Exercise 2: Phosphor Persistence and Color

<img src={gauntlet_exercise2_result} alt="Phosphor Persistence and Color result"/>
*Phosphor Persistence and Color — simulated result across source images.*
**Source**: Footage with moderate motion — a slowly panning camera, waving hand, or scrolling graphics.

**Objective**: Explore how vertical persistence and phosphor color create the CRT display aesthetic.

1. **Set up traces**: Establish visible edge traces with Sensitivity ~50%, Beam Width ~50%, Intensity ~75%.
2. **Increase persistence**: Turn Persistence clockwise past the midpoint. Watch edges leave glowing vertical trails as successive scanlines accumulate decayed glow.
3. **Maximum persistence**: Turn Persistence fully clockwise. Edges smear into long, ghostly streaks that fade slowly — the classic long-persistence CRT look.
4. **Cycle phosphor colors**: Step through the eight phosphor modes. Observe how Green, Amber, and Cyan each evoke a different era and type of CRT monitor.
5. **Try RGB mode**: Select the RGB phosphor. The beams now inherit color from the original video — edge traces are colored according to the source material rather than a fixed palette.
6. **Enable overlay**: Toggle Over Video to Overlay. The source image appears dimly beneath the beams, providing context for the traced edges.

**Key concepts**: IIR persistence via line buffer, phosphor decay rates, phosphor color palettes, overlay compositing

---

### Exercise 3: Full Vector Display

<img src={gauntlet_exercise3_result} alt="Full Vector Display result"/>
*Full Vector Display — simulated result across source images.*
**Source**: Any high-contrast footage — music videos, motion graphics, or documentary footage with strong visual compositions.

**Objective**: Combine all processing stages to create a complete CRT vector display emulation.

1. **Low threshold, wide glow**: Set Sensitivity ~30%, Beam Width to maximum. This produces broad, luminous beam traces that capture most edges.
2. **High persistence**: Set Persistence above 75%. Moving edges leave long phosphor trails.
3. **High intensity**: Increase Intensity to ~90%. The beams burn bright, saturating the phosphor color.
4. **Invert the source**: Toggle Invert to On. The underlying tonal relationships change, which affects how overlay compositing looks but not the edges themselves.
5. **Rainbow mode**: Select Rainbow phosphor. The hue shifts per scanline, creating multicolor banded beam traces — a psychedelic CRT effect.
6. **Mix for ghosting**: Lower the Mix fader to ~70%. The original input bleeds through behind the beam display, creating a hybrid double-exposure effect.
7. **Animate**: Move the source material and watch the persistence trails evolve — the display comes alive as traces form, decay, and reform.

**Key concepts**: Full processing chain interaction, persistence trails with moving sources, rainbow scanline colorization, wet/dry mix as creative tool

---


## Tips

- **Processing order**: Input → Invert → Gradient → Edge Detect → Glow → Persistence → Colorize → Overlay → Mix → Bypass. Each stage transforms the signal before the next one sees it. Glow happens *after* edge detection, so Beam Width doesn't affect which edges are found — only how far the glow spreads.
- **Gradient mode is the subtler option**: Binary mode produces uniform wireframe traces. Gradient mode preserves edge strength information, producing traces whose brightness varies with the sharpness of the boundary. For organic-looking CRT emulation, use Gradient mode.
- **Persistence writes to a line buffer, not a frame buffer**: Because the persistence RAM is only 2048 pixels wide (one scanline), the "memory" resets at each line start. Vertical persistence accumulates because successive scanlines write to the same horizontal positions, not because the FPGA stores an entire frame.
- **Toggle bit overlap is by design**: Edge Mode and Invert share register bits with the Phosphor selector. Changing either toggle also changes the effective phosphor color. Treat all three as a combined control — the program has 32 effective color/mode combinations from those three switches.
- **Two unused knobs**: Hue Offset (Knob 5) and Focus (Knob 6) are declared in the VHDL but not referenced in the processing pipeline. They are placeholders for future firmware features.
- **Feedback loops**: Routing Gauntlet's output back to its input creates recursive edge detection — the program detects edges in its own beam traces, producing fractal-like line structures that evolve with each pass.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed signal. Use it to compare the original footage against the vector display rendering.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory blocks in the FPGA fabric. Gauntlet uses zero BRAMs — all storage is distributed RAM and registers. |
| **CRT** | Cathode Ray Tube; a vacuum tube display that produces images by scanning an electron beam across a phosphor-coated screen. |
| **Distributed RAM** | Small RAM blocks synthesized from the FPGA's lookup tables, used here for the 2048×10-bit persistence line buffer. |
| **Edge Detection** | The process of identifying pixels where signal values change abruptly, implemented here as a horizontal absolute difference weighted across Y, U, and V channels. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip executing the video processing pipeline. |
| **Glow LUT** | A lookup table mapping distance-from-edge to brightness using exponential decay curves. Three LUTs provide narrow, medium, and wide beam profiles. |
| **IIR** | Infinite Impulse Response; a filter topology where the output depends on both the current input and previous outputs. Used in the persistence stage as `max(new, decayed_old)`. |
| **Phosphor** | The luminescent coating on a CRT screen that glows when struck by the electron beam. Different phosphor types (P1, P22, P31) have different colors and decay rates. |
| **Pipeline** | Sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. Gauntlet has 11 pipeline stages. |
| **Priority Encoder** | A circuit that scans a set of bits and returns the position of the first (nearest) active bit. Used here to find the closest edge in the 16-tap shift register. |
| **Shift Register** | A chain of flip-flops where data shifts one position per clock cycle. The 16-tap edge shift register provides spatial memory of recent edge positions. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
