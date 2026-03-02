---
draft: true
sidebar_position: 191
slug: /instruments/videomancer/mystify
title: "Mystify"
image: /img/instruments/videomancer/mystify/mystify_hero.png
description: "In 1992, Microsoft shipped Windows 3.1 with a set of screensavers that became cultural artifacts of the early personal computing era."
---

import mystify_hero from '/img/instruments/videomancer/mystify/mystify_hero.png';
import mystify_animation from '/img/instruments/videomancer/mystify/mystify_animation.gif';
import mystify_control_panel from '/img/instruments/videomancer/mystify/mystify_control_panel.png';
import mystify_exercise1_result from '/img/instruments/videomancer/mystify/mystify_exercise1_result.gif';
import mystify_exercise2_result from '/img/instruments/videomancer/mystify/mystify_exercise2_result.gif';
import mystify_exercise3_result from '/img/instruments/videomancer/mystify/mystify_exercise3_result.gif';

# Mystify

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={mystify_hero} alt="Mystify hero image"/>
*Mystify rendering two color-shifting quadrilaterals with trailing ribbons bouncing across a dimmed video background — the iconic screensaver geometry reimagined as live video synthesis.*
<img src={mystify_animation} alt="Mystify animated output"/>
*Mystify output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1992, Microsoft shipped Windows 3.1 with a set of screensavers that became cultural artifacts of the early personal computing era. Among them was "Mystify Your Mind" — a program that drew polygon outlines bouncing around the screen, leaving fading colored trails. The effect was hypnotic in its simplicity: vertices moved at constant velocities, reflected off screen edges, and the connecting line segments created flowing ribbon-like patterns as the trails accumulated. An entire generation of office workers watched these shapes drift across CRT monitors during lunch breaks.

Mystify recreates this effect as a real-time FPGA video synthesis program. Two independent polygons — each with either 2 vertices (line) or 4 vertices (quadrilateral) — bounce around the 1920×1080 active video area. Vertices are initialized from a 16-bit LFSR and move with fixed signed velocities, reflecting off screen edges. Line segments connecting the vertices are rasterized per-pixel using a cross-product distance test — a fully parallel computation that avoids the sequential Bresenham algorithm entirely. A trail buffer stores up to 6 frames of previous vertex positions in registers (no BRAM needed), rendering fading copies of the polygon at each trail position. The hue cycles through a 6-segment color wheel, with trail copies offset in time to create the characteristic color-shifting ribbon effect.

The name is a direct homage to the original screensaver. Unlike its software ancestor, which rendered to a framebuffer, Mystify computes every pixel's proximity to every line segment in real time — a brute-force approach made feasible by the FPGA's massively parallel architecture.

---

## Background

### The Windows Screensaver as Art Form

Screensavers emerged in the 1980s to prevent phosphor burn-in on CRT monitors — static images left displayed for hours would permanently darken the phosphor coating. The solution was simple: keep the display moving. But screensavers quickly transcended their practical purpose, becoming one of the first widespread forms of generative visual art. "Mystify Your Mind," "Flying Windows," "Starfield," and "After Dark"'s "Flying Toasters" became shared cultural reference points. Mystify honors this heritage by implementing the geometry in dedicated video hardware — taking what was originally a CPU-bound Windows GDI application and expressing it as a streaming pixel pipeline.

### Cross-Product Line Distance Test

Traditional line rasterization algorithms like Bresenham's work sequentially, stepping pixel by pixel along the line. This is impossible in a streaming video architecture where every pixel must be evaluated in a single clock cycle. Instead, Mystify uses the cross-product formulation for point-to-line distance. For a line segment from point A to point B, the signed distance of pixel P from the infinite line through A and B is proportional to the cross product $(B-A) \times (P-A)$. The magnitude of this cross product, divided by the segment length, gives the perpendicular distance. Mystify approximates the length normalization by dividing by $\max(|dx|, |dy|)$ instead of $\sqrt{dx^2 + dy^2}$, which avoids any square root computation. If the normalized distance falls below a configurable threshold, the pixel is considered "on" the line.

### LFSR-Based Vertex Initialization

The starting positions and velocities of all vertices are derived from a 16-bit Linear Feedback Shift Register (LFSR). The LFSR is seeded with the fixed value 0xD1CE and free-runs continuously. On the first frame after power-on, the LFSR output is sampled to initialize each vertex's X position (10 bits), Y position (9 bits), X velocity (4 bits sign-extended to 7), and Y velocity (4 bits). Because the LFSR is deterministic with a fixed seed, the initial configuration is always the same — but the visual result varies because the LFSR is sampled at a timing-dependent point that depends on when vsync first arrives.

### Trail Buffer Architecture

The original Windows screensaver stored trails in a framebuffer, decaying old pixels over time. Mystify takes a different approach: it stores the vertex positions of the previous 6 frames in a register-based ring buffer. On each vsync, the current vertex positions are shifted into the trail buffer, and the oldest entry is overwritten. During rendering, each trail entry is rasterized as a complete polygon with brightness that decreases with trail index — the most recent trail is half brightness, the next is quarter, and so on (right-shifted by trail_index + 1). This register-based approach uses zero BRAM but consumes significant LUT resources (~1200 LUTs for the full trail logic).

### Hue Wheel Color Mapping

Color cycling is implemented as a 6-segment hue wheel indexed by a frame counter that increments by `hue_speed >> 4` each vsync. The six segments produce approximate YUV representations of red, yellow, green, cyan, blue, and magenta using only shift-and-add operations (no multipliers). Each color is expressed as Y = brightness (full or 3/4 or 1/2 of the line brightness value) with U and V offsets computed as shifted fractions of the brightness. The transitions between segments are abrupt — there is no interpolation across hue boundaries, producing the characteristic hard color jumps of early computer graphics.


---

## Signal Flow

```
VSYNC (vertex update phase)
│
├── Frame 0 Only: LFSR Vertex Init ─────────────────────────────
│   ├─ For each vertex i (0..7):
│   │   ├─ pos_x = lfsr(9:0), pos_y = lfsr(8:0)
│   │   └─ vel_x = lfsr(3:0) sign-ext, vel_y = lfsr(6:3) sign-ext
│   └─ Ensure non-zero velocity (default ±2)
│
├── Trail Buffer Shift ─────────────────────────────────────────
│   ├─ trail[5..1] = trail[4..0]  (shift older positions)
│   └─ trail[0] = current vertex positions
│
├── Vertex Position Update ─────────────────────────────────────
│   ├─ new_x = vtx_x + vel_x
│   ├─ new_y = vtx_y + vel_y
│   ├─ Bounce: if new_x ≤ 0 or ≥ 1919 → negate vel_x, clamp
│   └─ Bounce: if new_y ≤ 0 or ≥ 1079 → negate vel_y, clamp
│
├── Hue Advance ────────────────────────────────────────────────
│   └─ frame_hue += hue_speed >> 4
│
ACTIVE VIDEO (per-pixel rendering, 7 clocks)
│
├── Stage 1: Position Counters ─────────────────────────────────
│   ├─ px = h_count, py = v_count
│   └─ num_polys = poly2_en ? 2 : 1
│
├── Stage 2: Line Distance Test (all segments, all trails) ─────
│   ├─ For each polygon p (0..num_polys-1):
│   │   ├─ For each edge e (0..active_verts-1):
│   │   │   ├─ dx = Bx − Ax, dy = By − Ay
│   │   │   ├─ cross = dx·(py−Ay) − dy·(px−Ax)
│   │   │   ├─ dist = |cross| / max(|dx|,|dy|)
│   │   │   ├─ on_line = dist < line_thresh
│   │   │   └─ if on_line → best = max(best, 1023)
│   │   └─ For each trail t (0..active_trails-1):
│   │       ├─ Same cross-product test on trail positions
│   │       └─ if on_line → best = max(best, 1023 >> (t+1))
│   └─ s_line_bright = best
│
├── Stage 3: Background Dimming ────────────────────────────────
│   ├─ bg_y = data_in.y × (1023 − bg_dim) >> 10
│   ├─ bg_dim > 900 → bg_u = bg_v = 512 (desaturate)
│   └─ else → bg_u = data_in.u, bg_v = data_in.v
│
├── Stage 4: Hue-to-YUV + Compositing ─────────────────────────
│   ├─ 6-segment hue wheel → line Y/U/V from brightness
│   ├─ Additive: line_y += bg_y (saturate at 1023)
│   └─ Key: line replaces background
│
├── Interpolator (wet/dry Mix) ─────────────────────────────────
│   └─ lerp(delayed_input, composited, mix_amount) per Y/U/V
│
└── Output Mux (NON-STANDARD BYPASS) ──────────────────────────
    ├─ Bypass off → mixed output + delayed sync (7 clocks)
    └─ Bypass on  → data_in.y/u/v DIRECTLY (not delayed!)
```

The most critical architectural detail is the non-standard bypass. When bypass is engaged, Mystify outputs `data_in.y`, `data_in.u`, and `data_in.v` directly — not the delayed versions. Since the sync signals (hsync_n, vsync_n) are always delayed through the 7-clock pipeline, engaging bypass causes a 7-clock misalignment between video data and sync. This manifests as a horizontal pixel shift in the output image. The rendering loop is also notable for its brute-force approach: every pixel tests distance to every line segment of every polygon at every trail position. With 2 polygons × 4 vertices × 7 trail copies, that's up to 56 cross-product evaluations per pixel — all computed combinatorially within a single clock cycle thanks to the FPGA's parallel architecture.

---

## Parameter Reference

<img src={mystify_control_panel} alt="Videomancer front panel with Mystify loaded"/>
*Videomancer's front panel with Mystify active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Speed is declared as a register mapping and assigned to the `s_speed` signal, but this signal is never referenced in the vertex update process. All vertices move at their LFSR-initialized velocities regardless of the Speed knob position. The velocities are 7-bit signed values derived from 4 bits of the LFSR seed, giving a range of approximately ±8 pixels per frame. Turning this knob has no visible effect on vertex movement speed.

---

#### Knob 2 — Trail Len
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 4 |

Trail Length controls the number of trailing polygon copies rendered behind the current frame's geometry. The 10-bit register is threshold-quantized into 7 levels (0–6) at register boundaries 146, 292, 438, 584, 730, and 876. At 0 trails, only the current polygon is drawn. Each additional trail adds a fainter copy of the polygon at progressively older vertex positions, creating the characteristic flowing ribbon effect. Trail brightness decreases exponentially: trail 0 is half brightness, trail 1 is quarter, trail 5 is 1/64th of maximum. More trails create longer, more elaborate ribbon patterns but consume more LUT resources in the rendering loop.

---

#### Knob 3 — Hue Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Hue Speed controls the rate of color cycling through the 6-segment hue wheel. The register value is right-shifted by 4 bits and added to the frame hue counter on each vsync, giving a cycling rate of 0–63 hue units per frame. At minimum, the color holds nearly static. At maximum, the hue cycles rapidly through red, yellow, green, cyan, blue, and magenta over the course of a few seconds. The frame hue counter wraps at 1023, so the color cycle period depends on the speed setting. Each trail copy inherits the same hue as the current frame — there is no per-trail hue offset in the implementation.

---

#### Knob 4 — Thickness
| Property | Value |
|----------|-------|
| Range | 1px – 4px |
| Default | 2px |
| Suffix | px |

Thickness sets the line width threshold for the cross-product distance test. The 10-bit register is quantized into 4 steps at boundaries 256, 512, and 768, producing threshold values of 200, 400, 600, and 800 respectively. These approximate line widths of 1, 2, 3, and 4 pixels. At the thinnest setting, only pixels very close to the mathematical line are illuminated. At maximum thickness, the lines become broad bands, and the polygon fills begin to overlap, creating a more saturated geometric pattern. The threshold comparison uses the raw cross-product magnitude divided by the line length approximation — it is not a precise pixel-width measurement.

---

#### Knob 5 — Bg Dim
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Background Dimming controls how much the input video is attenuated behind the polygon rendering. The VHDL computes `data_in.y × (1023 − bg_dim) >> 10`, so at bg_dim = 0 the background is full brightness, and at bg_dim = 1023 the background is completely black. When bg_dim exceeds 900, the chroma channels are also zeroed (forced to 512), desaturating the background to prevent color artifacts in very dark backgrounds. This creates a clean black canvas for the polygon wireframes at high dimming values, while lower values allow the polygons to overlay live video.

---

#### Knob 6 — Hue Sprd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Hue Spread is declared as a register mapping and assigned to the `s_hue_spread` signal, but this signal is never referenced in any process. The intended function — spreading the hue across trail copies so each trail gets a different color — was not implemented. All trail copies render with the same hue derived from the global frame hue counter. Turning this knob has no visible effect.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Poly 2** | Off | On |
| **8 — Vertices** | 2 Line | 4 Quad |
| **9 — Fill** | Wire | Filled |
| **10 — Blend** | Add | Key |
| **11 — Bypass** | Off | On |

The five toggles configure polygon geometry, rendering mode, and output routing. Poly 2 adds a second bouncing polygon. Vertices switches between 2-point lines and 4-point quadrilaterals. Fill is mapped but not implemented — wireframe rendering is always used. Blend selects between additive compositing and hard-key replacement. Bypass routes input directly to output with a sync alignment caveat.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix crossfade. At 0% (register = 0), the output is the 7-clock-delayed input video. At 100% (register = 1023), the output is the fully composited polygon rendering with dimmed background. Intermediate values blend the two proportionally via three interpolator_u instances.

---

## Guided Exercises

These exercises explore the screensaver geometry from simple lines to complex multi-polygon ribbons, experimenting with color cycling, compositing, and the interplay of digital geometry with live video.

### Exercise 1: Classic Screensaver

<img src={mystify_exercise1_result} alt="Classic Screensaver result"/>
*Classic Screensaver — simulated result across source images.*
**Objective**: Recreate the iconic Windows 3.1 Mystify look with colored quadrilaterals and trailing ribbons.

1. **Full quad mode**: Set Vertices to 4 Quad, enable Poly 2.
2. **3–4 trails**: Set Trail Len to step 3 or 4 for flowing ribbons.
3. **Moderate hue cycling**: Set Hue Speed to ~25% for gentle color shifts.
4. **Thick lines**: Set Thickness to step 3 (~3px).
5. **Full dimming**: Set Bg Dim to 100% for a black background.
6. **Additive blend**: Keep Blend on Add.
7. **Observe**: Two quadrilaterals bounce around the screen with colored trailing copies, creating flowing ribbon patterns reminiscent of the original screensaver.

**Key concepts**: Vertex bounce creates organic-feeling motion from simple reflection rules, trail buffer stores previous positions for ribbon effect, hue cycling adds temporal color variation

---

### Exercise 2: Minimal Geometry over Video

<img src={mystify_exercise2_result} alt="Minimal Geometry over Video result"/>
*Minimal Geometry over Video — simulated result across source images.*
**Objective**: Use thin line segments over live video for a subtle geometric overlay.

1. **Line mode**: Set Vertices to 2 Line. Single polygon only (Poly 2 off).
2. **Thin lines**: Set Thickness to step 1 (~1px).
3. **Short trail**: Trail Len step 1 for a single trailing copy.
4. **Partial dimming**: Set Bg Dim to ~30%. The video is slightly darkened.
5. **Slow hue**: Hue Speed ~10% for barely perceptible color drift.
6. **Mix at 80%**: Blend the geometric overlay subtly with the video.
7. **Feed interesting video**: Camera feeds with motion work well — the bouncing line provides a minimal but dynamic geometric accent.

**Key concepts**: Low dimming preserves video legibility, thin lines provide subtle geometric accent, mix below 100% softens the overlay

---

### Exercise 3: Stroboscopic Key Geometry

<img src={mystify_exercise3_result} alt="Stroboscopic Key Geometry result"/>
*Stroboscopic Key Geometry — simulated result across source images.*
**Objective**: Create hard-edged polygon cutouts with bright color jumps and dense trails.

1. **Dense trails**: Trail Len at maximum (step 6). Six trailing copies.
2. **Fast hue**: Hue Speed at ~80%. Colors shift rapidly.
3. **Thick lines**: Thickness at step 4 (~4px). Maximum line width.
4. **Key blend**: Set Blend to Key. Lines replace the background entirely.
5. **Black background**: Bg Dim at 100%.
6. **Both polygons, quad mode**: Poly 2 on, Vertices at 4 Quad.
7. **Observe**: Dense geometric patterns with hard color transitions and thick interlocking ribbons. The fast hue cycling creates a stroboscopic color effect.

**Key concepts**: Key blend produces hard-edged polygon shapes, maximum trail density creates complex interlocking patterns, fast hue cycling produces stroboscopic color jumps at segment boundaries

---


## Tips

- **Speed and Hue Spread do nothing**: The Speed and Hue Spread knobs are mapped but unused. Focus on Trail Len, Hue Speed, Thickness, and Bg Dim for visual control.
- **Fill is not implemented**: The Fill toggle has no effect. All rendering is wireframe regardless of the switch position.
- **Avoid bypass for clean comparisons**: Due to the non-standard bypass (output uses undelayed data while sync is delayed), use Mix at 0% instead of Bypass for A/B comparison of processed vs. unprocessed video.
- **Thick lines + max trails = visual density**: Combining step 4 thickness with 6 trails and dual polygons produces the densest geometric patterns, approaching solid fills where ribbons overlap.
- **Bg Dim shapes the context**: At 0% dimming, the polygons overlay full-brightness video. At 100%, they render against black. The 900-threshold desaturation prevents color bleed in very dark backgrounds.
- **Key blend for hard geometry**: Additive blend produces glowing luminous lines. Key blend produces opaque geometric shapes that punch through the background. Key is closer to the original screensaver look.
- **Color jumps are intentional**: The abrupt 6-segment hue transitions are a feature of the shift-and-add color implementation, not a bug. They recall the limited color palettes of early PC graphics.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive compositing** | A blending mode where the source and destination pixel values are summed, with saturation clamping at the maximum (1023). Produces a luminous glow effect. |
| **Cross product** | The 2D cross product $(B-A) \times (P-A)$ measures the signed area of the parallelogram formed by two vectors; its magnitude is proportional to the perpendicular distance from point P to line AB. |
| **Hard key** | A compositing mode where the source pixel completely replaces the destination when the source has non-zero brightness. No blending or transparency. |
| **Hue wheel** | A circular color space divided into segments; Mystify uses a 6-segment wheel (red, yellow, green, cyan, blue, magenta) with abrupt transitions. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator using XOR-based feedback. Mystify uses a 16-bit LFSR with seed 0xD1CE for vertex initialization. |
| **Screensaver** | A program originally designed to prevent CRT phosphor burn-in by displaying moving images when the computer was idle; became one of the earliest forms of mainstream generative art. |
| **Trail buffer** | A register-based ring buffer storing previous vertex positions. Unlike framebuffer-based trails, this approach re-rasterizes all trail copies every frame. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
