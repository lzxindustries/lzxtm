---
draft: true
sidebar_position: 152
slug: /instruments/videomancer/kintsugi
title: "Kintsugi"
image: /img/instruments/videomancer/kintsugi/kintsugi_hero.png
description: "In the Japanese art of kintsugi (金継ぎ), broken pottery is repaired with gold-dusted lacquer, transforming fractures into luminous features rather than hiding them."
---

import kintsugi_hero from '/img/instruments/videomancer/kintsugi/kintsugi_hero.png';
import kintsugi_before_after from '/img/instruments/videomancer/kintsugi/kintsugi_before_after.png';
import kintsugi_control_panel from '/img/instruments/videomancer/kintsugi/kintsugi_control_panel.png';
import kintsugi_exercise1_result from '/img/instruments/videomancer/kintsugi/kintsugi_exercise1_result.png';
import kintsugi_exercise2_result from '/img/instruments/videomancer/kintsugi/kintsugi_exercise2_result.png';
import kintsugi_exercise3_result from '/img/instruments/videomancer/kintsugi/kintsugi_exercise3_result.png';

# Kintsugi

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={kintsugi_hero} alt="Kintsugi hero image"/>
*Kintsugi tracing luminance edges in gold lacquer lines across a video source, transforming discontinuities into radiant metallic seams.*
<img src={kintsugi_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Kintsugi applied.*

---

## Overview

In the Japanese art of kintsugi (金継ぎ), broken pottery is repaired with gold-dusted lacquer, transforming fractures into luminous features rather than hiding them. This program applies the same philosophy to video: it detects edges and discontinuities in the source image and fills them with bright metallic color — gold or silver — so that the boundaries between tonal regions become the most prominent visual element.

The detection engine runs two parallel comparisons on the luminance channel. A horizontal detector compares each pixel to its immediate predecessor; a lookback detector compares each pixel to one eight clocks earlier in the scan line. Where either comparison exceeds a configurable threshold, a metallic line is drawn. The brightness, width, warmth, and color family of that line are all adjustable in real time. A fill mode extends the metallic color beyond the initial detection point, widening cracks into bands. The result is a dry/wet mix between the original source and the gold-traced version, controlled by the Mix fader.

At conservative settings — high threshold, thin lines, moderate brightness — Kintsugi adds a subtle golden edge highlight that enhances the structure of the source material. At aggressive settings — low threshold, wide fill, full brightness — the entire image becomes a web of luminous metallic veins with the original content visible only in the gaps between detected edges.

---

## Background

### The Art of Kintsugi

Kintsugi (金継ぎ, literally "gold joining") is a Japanese repair technique dating to the fifteenth century. When a ceramic vessel breaks, it is reassembled using lacquer mixed with powdered gold, silver, or platinum. The visible repair lines become a celebrated part of the object's history rather than a flaw to be concealed. The philosophy extends beyond craft into wabi-sabi aesthetics — the appreciation of imperfection, impermanence, and the beauty of things that bear the marks of use and time. Applied to video, the concept transforms every luminance discontinuity — every edge, contour, and texture boundary — into a glowing metallic trace.

### Edge Detection by Finite Differences

The simplest way to find an edge in a digital signal is to subtract adjacent samples and compare the absolute difference against a threshold. If the difference exceeds the threshold, the samples straddle a boundary. This is a one-dimensional finite-difference operator — the discrete equivalent of a first derivative. Kintsugi applies this operator in two directions simultaneously: a **horizontal** detector compares pixel N to pixel N−1 (one clock delay), and a **lookback** detector compares pixel N to pixel N−8 (eight-clock shift register). The horizontal detector catches sharp vertical edges; the lookback detector catches gradual transitions and diagonal edges that span multiple pixels. Combining both detectors produces a richer crack map than either alone.

### Metallic Color in YUV Space

Gold, silver, and copper are not spectral colors — they are perceptual phenomena arising from specific combinations of brightness, saturation, and hue. In the YUV color space, a convincing gold is achieved by setting high luminance (Y ≈ 900/1023), pulling U below neutral (reducing blue), and pushing V above neutral (adding red-amber warmth). Silver is simply high luminance with neutral chroma (U = V = 512). Kintsugi computes these colors per-pixel, blending them with the source based on edge strength. The Warmth parameter controls how far U and V deviate from neutral, sweeping the metallic line color from cool silver through warm gold to deep amber.

### Fill and Line Width

A raw edge detector produces single-pixel-wide detections — thin hairlines wherever the threshold is crossed. Kintsugi's fill mode extends each detection by holding the "edge active" flag for a configurable number of pixels after the initial trigger. This is implemented as a countdown counter that reloads on each new detection and decrements otherwise. The result is that closely-spaced edge pixels merge into broader metallic bands, while isolated edge pixels become short dashes. The Line Thickness parameter controls the reload value of this counter, producing lines from 1 to 16 pixels wide.

### Edge Strength and Brightness Modulation

Rather than treating all edges equally, Kintsugi computes an **edge strength** — the maximum of the horizontal and lookback deltas, scaled and clamped to the full 10-bit range. Stronger edges (larger luminance discontinuities) receive more of the metallic color; weaker edges receive a blend closer to the source. This creates a natural hierarchy of crack visibility: major contours glow brightly while subtle textures receive only a faint metallic shimmer. The Gold Brightness parameter sets the peak brightness of the metallic overlay, which is then modulated by this per-pixel edge strength.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Edge Detection Delay Line ──────────────────────────────────
│   ├─ 1-clock delay register (s_y_prev)
│   └─ 8-clock shift register (s_y_lookback[0..7])
│
├── Stage 1: Input Register + Delay Tap Latch ──────────────────
│   ├─ Latch current Y, U, V
│   ├─ Latch previous Y (1-clock delay)
│   └─ Latch lookback Y (8-clock delay)
│
├── Stage 2: Delta Compute ─────────────────────────────────────
│   ├─ Horizontal delta: abs(current_Y − previous_Y)
│   └─ Lookback delta: abs(current_Y − lookback_Y)
│
├── Stage 3: Threshold Compare + Edge Strength ─────────────────
│   ├─ Horizontal edge: h_delta > h_thresh
│   ├─ Lookback edge: lb_delta > lb_thresh (if edge_mode = 1)
│   ├─ Fill counter: countdown extends edge detection
│   ├─ Final edge decision: edge OR (fill_style AND counter > 0)
│   └─ Edge strength: max(h_delta, lb_delta) × 2, clamped to 1023
│
├── Stage 4: Gold/Silver Color Compose ─────────────────────────
│   ├─ Edge pixel:
│   │   ├─ Y: blend source toward Gold Brightness via edge strength
│   │   ├─ U: 512 − warmth_offset (gold) or 512 + warmth/8 (silver)
│   │   └─ V: 512 + warmth_offset (gold) or 512 − warmth/8 (silver)
│   └─ Non-edge pixel: pass-through source Y, U, V
│
├── Interpolator Mix (4 clocks) ────────────────────────────────
│   └─ 3× interpolator_u: crossfade delayed input ↔ composed output
│
├── Sync / Data Delay (8 clocks) ───────────────────────────────
│   └─ Shift registers for hsync, vsync, field, Y, U, V
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed (mix output) or delayed input
```

The two edge detection paths operate in parallel on the same input luma. The horizontal detector uses a single flip-flop delay, catching sharp vertical edges in the image. The lookback detector uses an 8-deep shift register, catching broader transitions and diagonal structures. When Edge Mode is set to horizontal-only (toggle bit 0 = 0), the lookback comparison is suppressed — only horizontal deltas matter. When Edge Mode enables both (toggle bit 0 = 1), the two detections are OR'd together, producing a denser edge map. The fill counter bridges short gaps between detected edges, creating continuous metallic lines rather than scattered dots. Gold and silver differ only in their chroma: gold shifts U below and V above neutral by the warmth offset, while silver applies a much smaller opposite shift (warmth/8) for a very faint cool tint.

---

## Parameter Reference

<img src={kintsugi_control_panel} alt="Videomancer front panel with Kintsugi loaded"/>
*Videomancer's front panel with Kintsugi active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sensitiv
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the sensitivity of horizontal edge detection. The register value is inverted and scaled to produce a threshold: high knob values yield a low threshold, meaning more edges are detected and more gold lines appear. At minimum, only the strongest transitions in the source trigger a metallic trace. At maximum, even subtle gradients become visible as fine golden seams. This is the primary sensitivity control — start here when calibrating Kintsugi to a new source.

---

#### Knob 2 — Gold Br
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the peak brightness of the metallic line color. At full, edges glow with near-white gold or silver. At zero, the metallic overlay is dark and subtle — edges are tinted but not luminous. This control interacts with edge strength: the VHDL blends the source pixel toward the brightness value based on how large the detected delta was, so stronger edges always appear brighter than weaker ones even at moderate brightness settings.

---

#### Knob 3 — Line Thk
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the width of the metallic fill that extends beyond each detected edge pixel. The register value is scaled to a 4-bit reload value (1–16 pixels). At minimum, each detection produces a single-pixel metallic dot. As the value increases, the fill counter holds the edge flag active for more pixels after each trigger, merging closely-spaced detections into broad metallic bands. This transforms Kintsugi from a thin-line edge tracer into a wide-band luminance contour renderer.

---

#### Knob 4 — Warmth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the warmth (hue shift) of the metallic color in the chroma channels. The register value is right-shifted by 3 bits to produce an offset. In gold mode, this offset pulls U below neutral (reducing blue) and pushes V above neutral (adding amber). Higher values produce a deeper golden-orange tint; lower values approach neutral, making the gold appear cooler and more platinum-like. In silver mode, the same offset is divided by 8 again and applied in the opposite direction, producing a very faint cool-blue tint rather than warm amber.

---

#### Knob 5 — Crack Den
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the lookback edge detection sensitivity, independent of the horizontal threshold. The mapping is the same inverted scaling as Sensitivity (Knob 1), but applied to the 8-clock lookback comparison. Higher values make the lookback detector more responsive to gradual transitions, adding more edge detections from diagonal and textural features. This control only has visible effect when Edge Mode (Toggle 7) enables the lookback path.

---

#### Knob 6 — Fill Ctr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Labeled "Fill Ctr" in the TOML configuration. This register is latched from `registers_in(5)` but the signal is not connected to any processing logic in the current VHDL implementation. Adjusting this knob produces no visible change. It may be reserved for a future fill contrast or fill color control feature.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Metal** | Gold | Silver |
| **8 — Cracks** | Fine | Bold |
| **9 — Glow** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle bits are decoded independently from `registers_in(6)`. Two control the edge detection behavior (edge mode, fill style), one selects the metallic color family (gold vs. silver), one is unconnected (Animate), and one is the standard bypass. The TOML presents Toggle 7 with four value labels (Gold/Silver/Copper/Platinum) and Toggle 8 with four labels (Fine/Bold/Web/Shatter), but the VHDL decodes only the least significant bit of each toggle position, making them effectively binary switches rather than four-way selectors.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the delayed original signal and the gold-traced output via three `interpolator_u` instances (one per Y/U/V channel). At 0% (register 0), the output is the delayed input — no metallic traces visible. At 100% (register 1023), the output is fully the composed gold/silver signal. Intermediate values create a semi-transparent metallic overlay where the gold lines are partially blended with the original source, useful for subtle edge enhancement without overwhelming the image.

---

## Guided Exercises

These exercises progress from basic edge tracing to complex metallic texturing, exploring the interaction between detection sensitivity, line width, color warmth, and fill mode.

### Exercise 1: Thin Gold Traces

<img src={kintsugi_exercise1_result} alt="Thin Gold Traces result"/>
*Thin Gold Traces — simulated result across source images.*
**Source**: A live camera feed or recorded footage with clear subjects and moderate contrast — faces, architecture, or natural scenes with defined contours.

**Objective**: Learn how edge threshold and brightness create subtle metallic edge highlights.

1. **Start clean**: Set Sensitivity to ~40%. Only the strongest edges in the source are detected — major contours and object boundaries.
2. **Add gold**: Increase Gold Brightness to ~70%. The detected edges glow with a golden hue.
3. **Warmth**: Turn Warmth to ~60% for a rich amber tone. Note how the gold color deepens.
4. **Silver comparison**: Toggle Glow (Toggle 9) to On. The metallic lines shift from warm gold to cool silver. Toggle back to compare.
5. **Increase sensitivity**: Slowly turn Sensitivity toward 100%. More and more edges appear — textures, gradients, and fine details become traced in gold.

**Key concepts**: Edge threshold as sensitivity control, inverted mapping (high knob = low threshold = more edges), gold vs. silver as chroma selection, warmth as UV offset

---

### Exercise 2: Wide Metallic Bands

<img src={kintsugi_exercise2_result} alt="Wide Metallic Bands result"/>
*Wide Metallic Bands — simulated result across source images.*
**Source**: Footage with strong tonal regions — high-contrast scenes, silhouettes, or graphic patterns.

**Objective**: Explore fill mode and line width to create broad metallic contours.

1. **Enable fill mode**: Set Cracks (Toggle 8) beyond the first position to activate gap filling. The metallic traces immediately widen.
2. **Line width**: Increase Line Thickness to ~80%. Each detected edge now extends for many pixels, creating broad metallic bands.
3. **Combined detection**: Set Metal (Toggle 7) to enable lookback detection. The edge map becomes denser — diagonal and textural edges join the horizontal detections.
4. **Crack density**: Increase Crack Density to ~80%. The lookback threshold drops, adding more secondary edge detections that merge with the widened lines.
5. **Extreme fill**: Push Line Thickness to 100%. The metallic color floods across large areas, leaving only the most uniform regions of the source untouched. The source becomes visible only through gaps in the golden web.

**Key concepts**: Fill counter extends edges, line width controls counter reload value, combined edge mode adds lookback detections, fill mode merges closely-spaced detections into bands

---

### Exercise 3: Golden Web Overlay

<img src={kintsugi_exercise3_result} alt="Golden Web Overlay result"/>
*Golden Web Overlay — simulated result across source images.*
**Source**: Any footage, especially material with varied textures and tonal ranges.

**Objective**: Combine all active parameters to create a dense golden web overlay, then use Mix for partial transparency.

1. **Maximum detection**: Set Sensitivity and Crack Density both to ~90%. Both horizontal and lookback detectors fire on subtle transitions.
2. **Enable both modes**: Set Metal toggle to combined detection, Cracks toggle to fill mode.
3. **Moderate width**: Set Line Thickness to ~50% for medium-width bands that follow the source structure.
4. **Full warmth**: Warmth at 100% for deep amber-gold.
5. **Lower Mix**: Reduce the Mix fader to ~60%. The golden web becomes semi-transparent, allowing the source to show through the metallic overlay.
6. **Silver web**: Toggle Glow to On. The warm golden web shifts to a cool silver mesh. Compare the aesthetic difference at partial mix.
7. **Bypass check**: Toggle Bypass for A/B comparison to see how much of the original image structure is preserved vs. overwhelmed.

**Key concepts**: Detection sensitivity compounds with fill width, mix as transparency control, gold-to-silver toggle changes mood without affecting detection, bypass for A/B comparison

---


## Tips

- **Start with Sensitivity**: This is the master density control. Begin at a moderate setting and listen to the source — high-contrast footage needs less sensitivity than flat, low-contrast material.
- **Gold vs. silver sets the mood**: Gold creates warmth and a sense of precious repair. Silver creates a cooler, more clinical or futuristic feeling. Toggle between them to find the right aesthetic.
- **Fill mode transforms the effect**: Without fill, Kintsugi produces delicate hairline traces. With fill, it produces broad metallic bands. The character of the effect changes dramatically.
- **Warmth at zero = platinum**: With the Warmth knob fully counter-clockwise, gold mode produces near-neutral chroma — effectively a bright platinum rather than warm gold.
- **Mix for subtlety**: At 100% mix, the metallic lines dominate. Drop to 40–60% for a subtle golden edge enhancement that preserves the source material's character.
- **Combined detection for texture**: Enable the lookback path (Metal toggle) to catch diagonal and textural edges that horizontal-only detection misses. This is especially effective on organic material like foliage, fabric, and skin.
- **Feedback loops**: Routing Kintsugi's output back to its input creates recursive edge detection — gold lines spawn new edges that spawn more gold, building into dense luminous webs.
- **Two controls are non-functional**: Fill Ctr (Knob 6) and Animate (Toggle 10) are registered but unconnected. Don't waste time calibrating them.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation BT.601; the standard color matrix used for converting between RGB and YUV in standard-definition video. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Edge detection** | The process of identifying pixel locations where luminance changes abruptly, indicating boundaries between distinct regions. |
| **Fill counter** | A countdown register that holds the edge-active flag for a configurable number of pixels after an edge trigger, widening detected edges into bands. |
| **Finite difference** | A discrete approximation of a derivative, computed as the difference between adjacent sample values. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interpolator** | A linear crossfade module (`interpolator_u`) that blends two signals based on a mix parameter. |
| **Kintsugi** | Japanese art of repairing broken pottery with gold-dusted lacquer, celebrating the repair as part of the object's history. |
| **Lookback** | A delayed comparison where the current pixel is compared to a pixel several clocks earlier in the scan line, catching broader transitions. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages on each clock cycle; Kintsugi uses an 8-clock pipeline. |
| **Wabi-sabi** | Japanese aesthetic rooted in the acceptance of transience and imperfection. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
