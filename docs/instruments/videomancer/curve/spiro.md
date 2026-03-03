---
draft: true
sidebar_position: 283
slug: /instruments/videomancer/spiro
title: "Spiro"
image: /img/instruments/videomancer/spiro/spiro_hero.png
description: "The Spirograph — that beloved plastic drawing toy invented by Denys Fisher in 1965 — works by rolling a toothed wheel inside (or around) a larger toothed ring."
---

import spiro_hero from '/img/instruments/videomancer/spiro/spiro_hero.png';
import spiro_animation from '/img/instruments/videomancer/spiro/spiro_animation.gif';
import spiro_control_panel from '/img/instruments/videomancer/spiro/spiro_control_panel.png';
import spiro_exercise1_result from '/img/instruments/videomancer/spiro/spiro_exercise1_result.gif';
import spiro_exercise2_result from '/img/instruments/videomancer/spiro/spiro_exercise2_result.gif';
import spiro_exercise3_result from '/img/instruments/videomancer/spiro/spiro_exercise3_result.gif';

# Spiro

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={spiro_hero} alt="Spiro hero image"/>
*Spiro tracing rainbow-hued hypotrochoid curves onto a persistent canvas, each gear ratio preset producing a distinct geometric rosette.*
<img src={spiro_animation} alt="Spiro animated output"/>
*Spiro output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

The Spirograph — that beloved plastic drawing toy invented by Denys Fisher in 1965 — works by rolling a toothed wheel inside (or around) a larger toothed ring. A pen inserted through one of the wheel's holes traces a mathematical curve called a hypotrochoid (inside) or epitrochoid (outside). Depending on the ratio of teeth between the two gears and the pen's distance from the center of the rolling wheel, the resulting curves range from simple circles and ellipses to complex, multi-petalled rosettes that close only after many revolutions.

Spiro recreates this mechanical drawing process in the FPGA pixel domain. Two DDS phase accumulators drive the outer and inner rotation angles of a parametric equation, evaluated once per frame using a 256-entry quarter-wave sine lookup table. The computed pen position is stamped onto a persistent 128×96 one-bit BRAM canvas, building up intricate geometric figures point by point over hundreds of frames. A separate morph oscillator slowly sweeps the pen position parameter, causing the curve to evolve continuously through shapes that no fixed Spirograph could produce. Eight preset gear ratios — from the classic 3/8 five-petal flower to the complex 11/16 figure — provide a curated palette of mathematical starting points.

The canvas read-out maps each lit cell to a color from a 16-entry hue palette that cycles over time, producing rainbow trails that reveal the drawing history. A configurable trail decay gradually erases older marks, balancing persistence against freshness. Optional input video luma modulation distorts the pen position in real time, injecting organic wobble into the otherwise perfect mathematical curves.

---

## Background

### The Mathematics of Roulette Curves

A hypotrochoid is the curve traced by a point attached to a circle of radius *r* rolling inside a fixed circle of radius *R*. The parametric equations are:

    x(t) = (R − r)·cos(t) + d·cos((R − r)/r · t)
    y(t) = (R − r)·sin(t) − d·sin((R − r)/r · t)

where *d* is the distance from the pen to the center of the rolling wheel and *t* is the rotation angle. When the small wheel rolls outside the large one, the sign changes produce an epitrochoid. The number of "petals" or lobes in the resulting figure depends on the ratio *r/R* reduced to lowest terms: if *r/R = p/q*, the curve closes after *p* revolutions of the inner wheel, producing a figure with *q − p* cusps (hypotrochoid) or *q + p* lobes (epitrochoid). Spiro's eight gear ratio presets select specific *p/q* pairs chosen for their visual variety.

### Direct Digital Synthesis for Curve Tracing

In the physical Spirograph, the drawing speed is set by how fast you push the pen around the ring. In Spiro, a DDS phase accumulator replaces the mechanical rotation. The accumulator adds a fixed increment each frame, and its upper bits serve as the angle argument *t* fed into the parametric equations. Higher increments trace the curve faster, placing fewer points between successive frames — at very high speeds the curve becomes a connect-the-dots approximation, while at low speeds each revolution is densely sampled. The draw speed control also determines how many trail points are stamped per frame (up to 16), ensuring smooth curves even at moderate rotation rates.

### Quarter-Wave Sine Lookup

Computing sine and cosine in hardware typically uses a lookup table. Spiro stores only the first quarter of the sine wave — 256 entries covering 0 to π/2 — and reconstructs the remaining three quarters via symmetry. This halves the memory requirement compared to a half-wave table and quarters it compared to a full-wave table. The 9-bit unsigned output (0–511) is mapped to signed values (−511 to +511) based on the quadrant bits. The same table serves both sin and cos by adding a 90° phase offset (256 entries) to the lookup argument.

### Persistent BRAM Canvas

Unlike frame-buffer-based drawing, where old content is erased each frame, Spiro accumulates marks on a 128×96 one-bit canvas stored in block RAM. Each pixel in the canvas is a single bit: 1 = drawn, 0 = empty. The canvas is read out during the active video period by mapping screen coordinates to canvas cells (dividing by 16 in each axis), producing a blocky, retro aesthetic reminiscent of early home computers. The trail decay mechanism periodically clears canvas bytes, with the decay rate inversely proportional to the Trail Decay pot — high values create long-lasting trails, low values make marks vanish almost immediately.

### Morph Oscillator and Video Modulation

The morph oscillator is a second, much slower DDS accumulator whose sine output is added to the pen position parameter. This creates a continuous sweep through pen distance values, making the curve evolve through families of related shapes without any knob movement. When Video Modulation is enabled, the input video's luminance value at the current pen position is multiplied into the pen distance, causing bright areas of the incoming video to stretch the curve outward and dark areas to compress it. This bridges the gap between pure mathematical synthesis and responsive video processing.


---

## Signal Flow

```
Per-Frame (during vertical blanking):
│
├── 1. DDS Phase Accumulators ──────────────────────────────────
│   ├─ s_draw_phase += draw_speed (rotation angle)
│   ├─ s_morph_phase += morph_rate (pen position sweep)
│   └─ s_hue_phase += 1 (color cycling)
│
├── 2. Curve Equation Evaluation ───────────────────────────────
│   ├─ Select gear ratio preset (3 bits of Pot 1)
│   ├─ Compute pen_l = pen_position + morph_sin [+ video_mod]
│   ├─ outer_arg = draw_phase upper bits
│   ├─ inner_arg = draw_phase × (den±num)/num (hypo/epi)
│   ├─ cos/sin lookups via quarter-wave LUT
│   └─ x,y = parametric equation → canvas coordinates
│
├── 3. Canvas Stamp (per point, up to 16/frame) ────────────────
│   └─ canvas[y][x] = 1 (set bit in BRAM)
│
├── 4. Trail Decay (periodic byte clear) ───────────────────────
│   └─ Erase one canvas byte per fade cycle
│
Per-Pixel (during active video):
│
├── 5. Canvas Readout ──────────────────────────────────────────
│   └─ Map screen (hcount>>4, vcount>>4) → canvas bit
│
├── 6. Color Mapping ───────────────────────────────────────────
│   ├─ bit=1, mono: Y=800, U=440, V=440 (green phosphor)
│   ├─ bit=1, rainbow: hue_palette[hue_phase + hue_offset]
│   └─ bit=0: Y=0, U=512, V=512 (black)
│
├── 7. Interpolator (wet/dry mix, 4 clocks) ────────────────────
│   └─ lerp(input_delayed, generated, mix_amount)
│
└── 8. Bypass Mux ──────────────────────────────────────────────
    └─ bypass=1 → pass input; bypass=0 → mix output
```

The critical distinction in Spiro's architecture is the separation between per-frame computation and per-pixel readout. The DDS accumulators and curve equation are evaluated during vertical blanking — computing and stamping up to 16 trail points per frame — while the canvas readout and color mapping run at pixel rate during active video. This means the curve builds up gradually over many frames, and the visual output at any moment reflects the accumulated history of all previous stamps minus any faded-out regions. The morph oscillator operates on a much longer timescale than the draw phase, creating slow evolutionary change in the curve shape that unfolds over tens of seconds.

---

## Parameter Reference

<img src={spiro_control_panel} alt="Videomancer front panel with Spiro loaded"/>
*Videomancer's front panel with Spiro active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Gear Ratio
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Selects one of eight gear ratio presets that define the mathematical relationship between the inner and outer wheels. The upper 3 bits of the 10-bit register index into a table of numerator/denominator pairs: 3/8 (five petals), 5/12 (seven petals), 1/4 (three petals), 7/16 (nine petals), 2/7 (five petals, different symmetry), 3/11 (eight petals), 5/8 (three lobes, suited for epitrochoid mode), and 11/16 (five complex lobes). Each ratio produces a distinctly different closed figure, and switching between them mid-drawing creates overlay compositions where multiple curve families coexist on the same canvas.

---

#### Knob 2 — Pen Pos
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the pen position — the distance *d* from the rolling wheel's center to the pen point. At 0% the pen sits at the center, producing a simple circle (the wheel's center traces a circle regardless of gear ratio). As the pen moves outward, the curve develops pronounced cusps or loops. At 100% the pen extends to the rim, producing the maximum cusp depth. The morph oscillator adds a sinusoidal sweep to this value, so the actual pen position is always the sum of the knob setting and the morph signal. This parameter defines the baseline around which the morph oscillates.

---

#### Knob 3 — Draw Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the DDS draw speed — the angular velocity of the virtual Spirograph wheel. Higher values trace the curve faster, stamping more points per second and completing full figures more quickly. The upper bits also determine how many discrete points are stamped per frame (0–15), so very high speeds produce dense, smooth curves while low speeds show individual dots progressing around the path. At the lowest settings, each frame adds a single point, making the drawing process visible as a slow dot-by-dot construction.

---

#### Knob 4 — Morph Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the morph rate — how quickly the pen position sweeps up and down via the morph DDS oscillator. At 0% the morph is frozen and the curve shape is determined solely by the Pen Position knob. As the morph rate increases, the pen distance sweeps through its range faster, causing the curve to cycle through families of related shapes. Very high morph rates create rapidly morphing, pulsating figures where the curve visibly breathes between tight and loose forms.

---

#### Knob 5 — Trail Decay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the trail decay rate — how quickly older canvas marks are erased. The VHDL implementation uses a fade counter that periodically clears one canvas byte, with the period inversely proportional to this parameter. At 100% the trail persists almost indefinitely, building up dense, overlapping curve layers. At 0% marks vanish almost immediately, showing only the most recent few points. Mid-range values create a ghostly trail where the newest portion of the curve is crisp and older sections fade through decreasing brightness (via the binary nature of the canvas, fading appears as random pixel dropout rather than smooth dimming).

---

#### Knob 6 — Hue Offset
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the starting hue offset for the rainbow color mode. The 16-entry hue palette cycles automatically via the hue phase accumulator; this knob shifts the starting point of that cycle. Rotating through 360° moves through red, orange, yellow, green, cyan, blue, violet, magenta, and back to red. In mono mode, this control has no visible effect since the output is always green phosphor.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Epitrochoid** | Hypo | Epi |
| **8 — Color Mode** | Rainbow | Mono |
| **9 — Video Mod** | Off | On |
| **10 — Clear** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles select mutually independent modes: curve type (hypotrochoid vs epitrochoid), color mode, video modulation, canvas clearing, and bypass. Epitrochoid mode changes the sign in the parametric equations, producing lobed figures instead of cusped ones. Color Mode selects between rainbow hue cycling and monochrome green phosphor. Video Mod enables real-time pen position modulation from the input video luminance. Clear forces the canvas to all zeros every frame, preventing trail accumulation.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the Spiro synthesis output and the delayed input signal. At 100% the synthesized curve completely replaces the input. At 0% the input passes through unaltered. Intermediate values create a translucent overlay where the geometric curve floats above the source video, combining mathematical precision with the texture and color of the input material.

---

## Guided Exercises

These exercises progress from simple static figures through evolving morphing curves to complex compositions that exploit the persistent canvas as a layered drawing surface.

### Exercise 1: Classic Spirograph Rosette

<img src={spiro_exercise1_result} alt="Classic Spirograph Rosette result"/>
*Classic Spirograph Rosette — simulated result across source images.*
**Objective**: Draw a clean, closed Spirograph figure and understand how gear ratio and pen position determine the shape.

1. **Clear the canvas**: Toggle Clear On momentarily, then back to Off to start with a blank canvas.
2. **Set 3/8 ratio**: Turn Gear Ratio to the first preset position (~0%). This selects the 3/8 ratio, which produces a classic five-petal flower.
3. **Mid pen position**: Set Pen Pos to ~50%. The curve should have moderate cusp depth.
4. **Moderate speed**: Set Draw Speed to ~40% so you can watch the curve being traced point by point.
5. **Full trail**: Set Trail Decay to 100% so nothing fades.
6. **Watch the figure close**: Over several seconds, the five-petal rosette builds up and eventually closes on itself.
7. **Try other ratios**: Sweep Gear Ratio through all 8 presets, clearing between each, to catalogue the available figures.

**Key concepts**: Gear ratio determines petal count and symmetry, pen position controls cusp depth, speed controls drawing density, trail persistence accumulates the complete figure

---

### Exercise 2: Morphing Impossible Curves

<img src={spiro_exercise2_result} alt="Morphing Impossible Curves result"/>
*Morphing Impossible Curves — simulated result across source images.*
**Objective**: Engage the morph oscillator to create continuously evolving curves that pass through shapes no fixed-ratio Spirograph can produce.

1. **Start with a clean canvas**: Clear, then disable Clear.
2. **Select a complex ratio**: Set Gear Ratio to preset 7 (~100%, the 11/16 complex figure).
3. **Enable morph**: Slowly increase Morph Rate from 0% to ~30%. The pen position begins sweeping, and the curve shape evolves continuously.
4. **Moderate trail decay**: Set Trail Decay to ~60% so older curve iterations slowly fade, preventing the canvas from becoming a solid mass.
5. **Watch the evolution**: Over 30–60 seconds, the curve wanders through a family of related shapes, creating overlapping traces that form intricate moire-like interference patterns.
6. **Switch to epitrochoid**: Toggle Epitrochoid to Epi. The curve family changes character from cusped stars to rounded lobes. The morph continues sweeping through the new family.

**Key concepts**: Morph oscillator sweeps pen position continuously, trail decay creates layered ghost traces, switching epitrochoid/hypotrochoid mid-morph creates hybrid compositions

---

### Exercise 3: Video-Modulated Organic Curves

<img src={spiro_exercise3_result} alt="Video-Modulated Organic Curves result"/>
*Video-Modulated Organic Curves — simulated result across source images.*
**Objective**: Enable video modulation to inject organic distortion into the mathematical curves, producing unique content-responsive forms.

1. **Feed an input signal**: Connect a camera or video source with dynamic brightness variation.
2. **Set a steady curve**: Gear Ratio preset 2 (~25%, the 1/4 three-petal figure), medium pen position, moderate speed.
3. **Enable Video Mod**: Toggle Video Mod On. The curve immediately responds to the input video brightness, warping outward in bright frames and contracting in dark frames.
4. **Enable morph**: Set Morph Rate to ~20% for gentle shape evolution combined with the video-driven distortion.
5. **Mono mode for clarity**: Switch Color Mode to Mono to see the distorted curves as clean green traces against black.
6. **Overlay on source**: Reduce Mix to ~70% so the source video shows through behind the curves, revealing the relationship between the input content and the curve distortion.

**Key concepts**: Video modulation multiplies input luma into pen position, bright input stretches curves outward, morph and video mod compound for complex organic motion, mix reveals the modulation source

---


## Tips

- **Clear for fresh starts**: Momentarily toggle Clear On/Off to wipe the canvas and begin a new composition from scratch. The DDS phase continues uninterrupted, so the new drawing picks up where the old phase left off.
- **Gear ratio exploration**: Each of the 8 presets produces a distinct figure. Try drawing one ratio, clearing, and switching to another to compare the petal counts and symmetries side by side (or layer them without clearing).
- **Morph for evolution**: Even a small Morph Rate creates subtle, beautiful variations over time. Set Trail Decay to ~60–70% to see the morphing history as ghostly overlapping traces.
- **Speed affects density**: Low Draw Speed values stamp fewer points per frame, making the curve appear as a dotted line. High values provide smooth, dense curves but trace the full figure faster.
- **Epitrochoid for lobes**: Epitrochoid mode tends to produce outward-looping, flower-like curves compared to the inward-cusping stars of hypotrochoid mode. The visual difference is most dramatic with gear ratios where the numerator and denominator are close in value.
- **Video Mod for organic flavour**: Even subtle video modulation — especially from slowly moving footage — adds a gentle wobble that makes the mathematical curves feel alive and hand-drawn.
- **Rainbow hue cycling**: The hue palette cycles automatically. Adjust Hue Offset to start the cycle at a preferred colour range (warm reds, cool blues, etc.).
- **Mix for overlay**: At 50–70% Mix, the curve floats translucently over the input video, creating a distinctive layered aesthetic suitable for live performance.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used here for the persistent 128×96 one-bit canvas. |
| **Canvas** | The 128×96 one-bit bitmap stored in BRAM where trail points are accumulated. |
| **Cusp** | A pointed feature on a hypotrochoid curve where the pen direction reverses sharply. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms by incrementing a phase accumulator at a fixed rate. |
| **Epitrochoid** | The curve traced by a point on a circle rolling outside a fixed circle. |
| **Gear Ratio** | The ratio r/R of the rolling wheel radius to the fixed ring radius, determining the number of lobes or cusps in the figure. |
| **Hypotrochoid** | The curve traced by a point on a circle rolling inside a fixed circle. |
| **Lobe** | A rounded outward protrusion on an epitrochoid curve. |
| **Morph Oscillator** | A slow DDS sine wave that sweeps the pen position, causing the curve to evolve continuously. |
| **Pen Position** | The distance *d* from the rolling wheel's center to the pen point, controlling cusp/lobe depth. |
| **Quarter-Wave LUT** | A 256-entry lookup table storing the first quarter of a sine wave; the remaining three quarters are reconstructed by symmetry. |
| **Roulette** | The general mathematical term for curves traced by a point on a circle rolling along another circle. |
| **Trail Decay** | The rate at which the canvas fade mechanism erases older marks. |

---
