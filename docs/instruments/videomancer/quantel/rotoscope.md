---
draft: true
sidebar_position: 220
slug: /instruments/videomancer/rotoscope
title: "Rotoscope"
image: /img/instruments/videomancer/rotoscope/rotoscope_hero.png
description: "Program guide for Rotoscope, a Videomancer quantel program for the LZX video synthesizer."
---

import rotoscope_before_after from '/img/instruments/videomancer/rotoscope/rotoscope_before_after.png';
import rotoscope_control_panel from '/img/instruments/videomancer/rotoscope/rotoscope_control_panel.png';
import rotoscope_exercise1_result from '/img/instruments/videomancer/rotoscope/rotoscope_exercise1_result.png';
import rotoscope_exercise2_result from '/img/instruments/videomancer/rotoscope/rotoscope_exercise2_result.png';
import rotoscope_exercise3_result from '/img/instruments/videomancer/rotoscope/rotoscope_exercise3_result.png';
import rotoscope_hero from '/img/instruments/videomancer/rotoscope/rotoscope_hero.png';
import rotoscope_source1_kodim15 from '/img/instruments/videomancer/rotoscope/rotoscope_source1_kodim15.png';
import rotoscope_source2_kodim01 from '/img/instruments/videomancer/rotoscope/rotoscope_source2_kodim01.png';
import rotoscope_source3_kodim01_bw from '/img/instruments/videomancer/rotoscope/rotoscope_source3_kodim01_bw.png';

# Rotoscope

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={rotoscope_hero} alt="Rotoscope hero image"/>
*Rotoscope compositing four temporally displaced trail layers with tinted treatment and screen blending to produce the characteristic Quantel-era trailing echo effect.*
<img src={rotoscope_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Rotoscope applied.*

---

## Overview

In the 1980s and 1990s, Quantel's Harry, Harriet, and Henry systems defined a generation of broadcast visual effects. One of their signature techniques was the "video sandwich" — multiple time-delayed copies of the same video source layered on top of each other, each copy processed differently and blended together. A dancer's arm trails through four echoes: each echo dimmer, tinted toward a different hue, dissolving into the one behind it. The result is a painterly, temporal smear that turns motion into visible form.

Rotoscope recreates this technique in the FPGA domain. It reads the incoming video into three BRAM scanline delay buffers and produces up to four time-delayed copies of each pixel. Each copy — each "layer" — can be independently treated: left clean, tinted toward a configurable hue, reduced to a binary silhouette, or converted to an edge-trace contour. The layers are then composited back-to-front using either Porter-Duff alpha blending or additive screen blending. An opacity curve controls how quickly the trail layers fade, and a horizontal spatial offset can separate them visually. The name recalls both the traditional animation technique of tracing over live-action footage and the idea of viewing motion as a sequence of overlapping outlines.

At conservative settings, Rotoscope adds a subtle motion echo — a ghost of movement that follows the live image by a few scanlines. At extreme settings, it produces dense, kaleidoscopic trail compositions where the original subject is buried under layers of tinted, posterized, edge-detected copies of itself.

---

## Background

### The Quantel Legacy

Quantel (an acronym for *Quantised Television*) was a British company that produced the first practical real-time digital video effects systems. Their Harry (1985) and Henry (1992) compositors were among the first to treat video as a stack of independently manipulable layers — each with its own timing, position, and processing. The "trail" or "echo" effect was a natural consequence of this architecture: if you can delay one layer relative to another, you can create temporal trails simply by stacking delayed copies with decreasing opacity. Rotoscope distills this concept to its essence: a single input, multiple time-delayed layers, and flexible per-layer treatment.

### BRAM Delay Buffers

Each of Rotoscope's three delay buffers is a 512×10-bit BRAM tile storing one channel (Y, U, or V) of video data. The write address advances by one at each scanline start, while four read addresses tap the buffer at progressively earlier positions. The delay spread parameter controls the distance between taps: at low values, all four layers read from nearly the same position (minimal trail); at high values, each layer is separated by many scanlines (long trail). Because the BRAM stores 512 scanlines and the buffer wraps, the maximum trail length covers the full vertical extent of the frame.

### Layer Treatment Modes

Each of the four layers receives the same treatment processing, selected by a two-bit toggle pair:

- **Clean** (00): The delayed video passes through unchanged — a pure temporal echo.
- **Tinted** (01): The delayed luminance is preserved, but the chrominance is blended 50/50 with a configurable tint hue from an 8-entry palette. This produces a color-washed echo.
- **Silhouette** (10): The delayed luminance is compared against an edge threshold. Pixels above the threshold become a solid-colored shape (using the tint hue); pixels below become transparent. This produces a flat, cut-out silhouette of the subject.
- **Edge Trace** (11): The horizontal gradient magnitude — the absolute difference between adjacent pixels — is computed. Gradients above the edge threshold produce bright contour lines; everything else is transparent. This produces the outline-trace aesthetic of hand-drawn animation cels.

### Alpha Compositing

The four layers are composited back-to-front (layer 3 first, layer 0 last) against a black background. In **Porter-Duff over** mode, each layer blends with the accumulator using its per-layer alpha: `result = layer × α + background × (1 − α)`. In **screen** mode, layers are additively combined: `result = A + B × α`, clamped to 1023. The opacity curve parameter controls how quickly alpha decreases per layer — layer 0 always has full opacity, while deeper layers fade according to the curve setting.

### Horizontal Spatial Offset

In addition to the temporal delay between layers, Rotoscope can apply a horizontal spatial offset to each successive layer. In "Right" mode, each layer shifts progressively to the right. In "Alternating" mode, even layers shift right and odd layers shift left, creating a spread or fan effect. This spatial separation makes the individual trail layers independently visible even when the subject is stationary.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── BRAM Write ─────────────────────────────────────────────────
│   │
│   ├─ 1. Write Y/U/V to BRAM at wr_addr
│   │      Compute 4 read addresses (delay spread × layer index)
│   │      Horizontal offset per layer (right or alternating)
│   │
│   ├─ 2. BRAM Read — 4 delayed taps
│   │      layer_y/u/v[0..3] from delay buffers
│   │      Save y_prev for edge detection
│   │
│   ├─ 3. Per-Layer Treatment
│   │      Clean:      pass through delayed Y/U/V
│   │      Tinted:     Y unchanged, U/V blended 50% with tint hue
│   │      Silhouette: Y > edge_thresh → solid tint color, else transparent
│   │      Edges:      |Y[x] - Y[x-1]| > edge_thresh → contour, else transparent
│   │      Alpha: 1023 for layer 0, decreasing per opacity_curve
│   │
│   ├─ 4. Back-to-Front 4-Layer Composite
│   │      Over mode:   layer × α + accum × (1 - α)
│   │      Screen mode: accum + layer × α (clamped)
│   │
│   └─ 5-8. Interpolator (wet/dry mix, 4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (delayed to match processing latency)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The BRAM delay buffers are the architectural core of Rotoscope. Unlike purely spatial effects that process each pixel independently, Rotoscope requires memory — it must store previous scanlines in order to produce time-delayed copies. The three BRAM tiles (one per YUV channel) each hold 512 entries, and the write pointer advances once per scanline. The four read addresses are spaced by a configurable delay spread, so the trail length is continuously variable. A crucial subtlety: the treatment mode (clean, tinted, silhouette, edges) is applied *per layer after* the BRAM read, meaning all four layers in a given frame use the same treatment. The treatment affects appearance, not the stored data.

---

## Parameter Reference

<img src={rotoscope_control_panel} alt="Videomancer front panel with Rotoscope loaded"/>
*Videomancer's front panel with Rotoscope active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Layer Cnt
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Selects the number of active trail layers from 1 to 4. The register is divided into four zones: values below 256 activate only layer 0 (no trail), 256–511 activate layers 0–1 (one echo), 512–767 activate three layers, and 768+ activate all four. More layers produce a denser, more complex trail composition. With only one layer active, Rotoscope shows the delayed video with the selected treatment but no trailing echo.

---

#### Knob 2 — Delay Sprd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Controls the temporal offset between successive trail layers by setting the address spacing between BRAM read taps. At low values, all layers read from nearly the same buffer position — the trail is short and the echoes are closely stacked. At high values, each layer is separated by many scanlines, producing a long, drawn-out temporal smear. The delay spread is proportional to the register value's upper bits divided across the buffer depth.

---

#### Knob 3 — Opacity Cv
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the alpha falloff between layers. Layer 0 always has full opacity (1023). Each subsequent layer's alpha is reduced by `opacity_curve × layer_index / 1024`. At 0%, all layers have equal opacity — a uniform stack. At high values, the trail layers fade rapidly, producing a quickly diminishing echo. The opacity curve interacts strongly with the blend mode: in Over mode, each layer's contribution is attenuated by both its own alpha and the already-accumulated background; in Screen mode, opacity directly controls the additive brightness of each layer.

---

#### Knob 4 — Tint Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 60° |
| Suffix | ° |

Selects the tint hue from an 8-entry color palette, used by the Tinted and Silhouette treatment modes. The top 3 bits of the register value map to 8 hue positions: neutral gray, warm red, green, cyan, blue, magenta, pink-orange, and neutral again. The selected hue's U and V values replace (Tinted: blend 50/50) or fill (Silhouette: solid) the layer's chrominance. The tint hue has no effect in Clean or Edge Trace modes.

---

#### Knob 5 — H Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies a horizontal spatial offset to each successive layer. Each layer is shifted by `layer_index × offset_amount` pixels horizontally. In Right mode (Offset Dir = Right), all layers shift progressively to the right. In Alternating mode, even layers shift right and odd layers shift left, creating a symmetric fan or spread pattern. Horizontal offset makes the trail layers spatially separated and individually visible even when the source is static.

---

#### Knob 6 — Edge Thr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

Sets the luminance threshold for the Silhouette and Edge Trace treatment modes. In Silhouette mode, pixels with Y above the threshold are replaced with a solid tint color; pixels below become transparent. In Edge Trace mode, the horizontal gradient (absolute difference between adjacent pixels) must exceed this threshold to produce a visible contour line. Higher values produce fewer, more prominent features; lower values produce dense, detailed silhouettes or edge maps. Has no effect in Clean or Tinted modes.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Treat A** | Off | On |
| **8 — Treat B** | Off | On |
| **9 — Blend** | Over | Screen |
| **10 — Offset Dir** | Right | Altern |
| **11 — Bypass** | Off | On |

Toggles 7–8 form a 2-bit treatment mode selector. Toggle 9 selects the alpha compositing blend mode. Toggle 10 controls horizontal offset direction. Toggle 11 is the standard bypass switch. The treatment selector is the most impactful pair — it completely changes the character of the trail layers from transparent echoes (Clean) through color-washed ghosts (Tinted) to graphic silhouettes and contour drawings (Silhouette, Edge Trace).

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Wet/dry mix crossfade between the original input video and the processed trail composite. At 0%, the output is the unprocessed input. At 100%, the output is the fully composited trail. Intermediate values blend the trail over the original, which can produce a ghostly overlay effect where the live image remains visible beneath the trailing echoes.

---

## Guided Exercises

These exercises progress from simple motion trails to complex multi-treatment compositions, building familiarity with Rotoscope's BRAM-based trail system.

### Exercise 1: Simple Motion Echo

<img src={rotoscope_exercise1_result} alt="Simple Motion Echo result"/>
*Simple Motion Echo — simulated result across source images.*
**Source**: A slowly moving subject — a hand waving, a pendulum, or a dancer — against a contrasting background.

**Objective**: Learn how layer count and delay spread create temporal trails.

1. **Two layers**: Set Layer Cnt to 2. A single echo appears behind the moving subject.
2. **Increase delay**: Sweep Delay Sprd from low to high. Watch the echo separate from the live image — at low values it's a tight shadow, at high values it's a long trailing ghost.
3. **Four layers**: Increase Layer Cnt to 4. Three echoes now follow the subject, each progressively further behind.
4. **Opacity fade**: Increase Opacity Cv. The deeper echoes fade faster, producing a natural diminishing trail.
5. **Compare**: Toggle Bypass to compare the live signal with the processed result.

**Key concepts**: Layer count controls the number of temporal echoes, delay spread controls the time offset between echoes, opacity curve controls how quickly echoes fade

---

### Exercise 2: Tinted Trail Composition

<img src={rotoscope_exercise2_result} alt="Tinted Trail Composition result"/>
*Tinted Trail Composition — simulated result across source images.*
**Source**: A live camera feed with moderate to high motion — a performer, moving traffic, or abstract gestures.

**Objective**: Explore tinted treatment and screen blending for colorized trail effects.

1. **Enable tinting**: Set treatment to Tinted (Treat A = On, Treat B = Off). The trail layers gain a color wash.
2. **Select tint hue**: Sweep Tint Hue through the 8 palette positions. Watch the trail change from neutral to warm to cool hues.
3. **Screen blend**: Switch Blend to Screen. The tinted trails now glow additively — brighter and more luminous.
4. **Add spatial offset**: Increase H Offset. The trail layers separate horizontally, creating a colored fan effect.
5. **Alternate direction**: Switch Offset Dir to Alternating. The layers spread symmetrically left and right.

**Key concepts**: Tinted mode preserves luminance while shifting chrominance, screen blending creates additive glow effects, horizontal offset separates layers spatially

---

### Exercise 3: Edge Trace Contours

<img src={rotoscope_exercise3_result} alt="Edge Trace Contours result"/>
*Edge Trace Contours — simulated result across source images.*
**Source**: High-contrast footage with strong edges — silhouetted figures, architectural features, or text overlays.

**Objective**: Use edge trace treatment to create animated contour drawings from the trail layers.

1. **Set edge trace mode**: Treat A = On, Treat B = On (treatment = 11 = Edge Trace).
2. **Adjust edge threshold**: Sweep Edge Thr from low to high. At low values, dense contour lines appear everywhere. At high values, only the strongest edges survive.
3. **Add tint**: Select a bright tint hue — the edges will be drawn in this color.
4. **Screen blend**: Switch to Screen blending so the edge contours glow against black.
5. **Time spread**: Increase Delay Sprd so each layer's contour represents a different moment in time. Moving edges fan out into a temporal contour animation.
6. **Compare with silhouette**: Switch to Silhouette mode (Treat A = Off, Treat B = On) to see the same subject as solid colored cutouts instead of outlines.

**Key concepts**: Edge trace computes horizontal gradient magnitude, edge threshold controls sensitivity, silhouette mode fills regions above threshold with solid color

---


## Tips

- **Start with Clean treatment**: Before exploring tinted or edge modes, get comfortable with the basic trail behavior — layer count, delay spread, and opacity curve. These three controls define the temporal structure.
- **Screen blend for glow**: When using Tinted treatment, Screen blend mode produces luminous, glowing trails that pop against dark backgrounds. Over mode is more natural but less dramatic.
- **Edge Trace needs contrast**: The horizontal gradient detector works best with high-contrast edges. Low-contrast footage produces sparse, weak contour lines. Feed strong edges for the best results.
- **Silhouette for graphic art**: Silhouette mode reduces video to flat colored cutouts — use it with high layer count and wide delay spread for an animated paper-doll effect reminiscent of early digital compositing.
- **Horizontal offset reveals layers**: When layers are temporally coincident (low Delay Sprd), increasing H Offset makes each copy visible as a spatially displaced echo. Alternating direction creates symmetry.
- **Tint Hue is modal**: The tint color only affects Tinted and Silhouette treatment modes. In Clean and Edge Trace modes, the hue selector has no visible effect.
- **Mix for ghosting**: At 50% Mix, the trailing echoes appear as faint overlays on the live image — a subtle motion ghost that adds depth without overwhelming the source.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha Compositing** | A technique for combining images using per-pixel opacity (alpha) values, where each pixel's contribution is weighted by its transparency. |
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for scanline delay storage. |
| **Delay Buffer** | A FIFO memory that stores video data for later retrieval, enabling temporal displacement between layers. |
| **Edge Trace** | A treatment mode that converts video to contour lines by computing the horizontal gradient magnitude between adjacent pixels. |
| **Layer** | One of up to four time-delayed copies of the input video, each with independent alpha and processing treatment. |
| **Opacity Curve** | A per-layer alpha attenuation that controls how quickly trail echoes fade. |
| **Porter-Duff** | A formal model for alpha compositing operations, named after Tom Porter and Tom Duff (Lucasfilm, 1984). The "over" operator is the most common. |
| **Quantel** | A British company that produced pioneering real-time digital video effects systems (Harry, Henry, Harriet) from the 1980s–2000s. |
| **Screen Blend** | An additive compositing mode where brightness values add together, producing a luminous, glowing result. |
| **Silhouette** | A treatment mode that converts video to binary threshold shapes — pixels above threshold become solid color, below become transparent. |
| **Tint** | A chrominance shift applied to trail layers, blending the original U/V toward a selected palette hue. |
| **Trail** | A series of temporally delayed copies of the input video composited to create a motion echo effect. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
