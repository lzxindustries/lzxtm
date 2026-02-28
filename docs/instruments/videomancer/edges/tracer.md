---
draft: true
sidebar_position: 266
slug: /instruments/videomancer/tracer
title: "Tracer"
image: /img/instruments/videomancer/tracer/tracer_hero.png
description: "Program guide for Tracer, a Videomancer edges program for the LZX video synthesizer."
---

import tracer_before_after from '/img/instruments/videomancer/tracer/tracer_before_after.png';
import tracer_control_panel from '/img/instruments/videomancer/tracer/tracer_control_panel.png';
import tracer_exercise1_result from '/img/instruments/videomancer/tracer/tracer_exercise1_result.png';
import tracer_exercise2_result from '/img/instruments/videomancer/tracer/tracer_exercise2_result.png';
import tracer_exercise3_result from '/img/instruments/videomancer/tracer/tracer_exercise3_result.png';
import tracer_hero from '/img/instruments/videomancer/tracer/tracer_hero.png';
import tracer_source1_kodim02 from '/img/instruments/videomancer/tracer/tracer_source1_kodim02.png';
import tracer_source2_kodim07 from '/img/instruments/videomancer/tracer/tracer_source2_kodim07.png';
import tracer_source3_kodim01_bw from '/img/instruments/videomancer/tracer/tracer_source3_kodim01_bw.png';

# Tracer

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={tracer_hero} alt="Tracer hero image"/>
*Tracer accumulating edge contours onto a persistent canvas, rendering the aluminum-powder texture of a miniature drawing toy.*
<img src={tracer_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Tracer applied.*

---

## Overview

Every child of the 1970s and 1980s remembers the feeling: two white knobs, a silver screen, and a stylus hidden behind a pane of glass, scraping aluminum powder off to reveal dark lines. Tracer recreates that experience in real time using live video as the drawing hand. It performs edge detection on the input luminance — finding the boundaries between bright and dark regions — and stamps those contours onto a persistent 128×96 one-bit BRAM canvas. The canvas accumulates over time, building up a dense line drawing that echoes the source video's structure.

The rendered canvas is not a simple black-and-white overlay. Unscraped areas glow with adjustable silver-gray brightness, textured by an LFSR grain pattern that mimics the particulate shimmer of real aluminum powder. Scraped lines appear dark, with just enough grain to suggest depth. An optional red border with white dial circles completes the toy aesthetic. The Decay Rate control introduces probabilistic erasure — shaking the virtual screen to redistribute the powder — so the drawing evolves rather than simply filling in.

At low edge thresholds, subtle gradients and textures produce dense, painterly contour maps. At high thresholds, only the strongest edges register, yielding spare line drawings. The Continuous toggle bypasses the canvas entirely, showing raw edge detection output as a streaming contour effect with no memory.

---

## Background

### The Etch A Sketch as Signal Processor

The Etch A Sketch — patented by André Cassagnes in 1960 — is, at its heart, an analog plotter. A stylus on an X-Y lead screw assembly scrapes aluminum powder off a glass surface coated with a thin layer of the material. The result is a subtractive drawing process: the default state is bright (powder-covered), and drawing *removes* material to reveal the darker surface beneath. Tracer inverts the creative direction — the video signal drives the stylus — but preserves the subtractive rendering model. The canvas starts bright, and detected edges darken it.

### Edge Detection in One Dimension

Tracer's edge detector is the simplest possible gradient operator: the absolute difference between adjacent samples. Horizontally, it computes |Y(x) − Y(x−1)| for each pixel. Vertically, it uses a one-line delay buffer to compute |Y(x, y) − Y(x, y−1)|. The two gradients are summed using Manhattan distance (|∆H| + |∆V|) and compared against a threshold. This is computationally cheap — no multiplication, no Gaussian smoothing — but effective for contour extraction. The result is similar to the output of a Roberts cross operator.

### Persistent Canvas and BRAM

The 128×96 canvas is stored as a 1-bit-per-pixel bitmap in FPGA block RAM. Each detected edge sets a bit; between frames, the decay process probabilistically clears bits. This creates a drawing that builds up over seconds and fades over seconds — a temporal integration that transforms a jittery edge detector into a stable contour map. The low resolution of the canvas (roughly 10× downsampled from 1280×720) gives the output its chunky, pixel-art character.

### LFSR Grain Texture

A 16-bit linear feedback shift register runs continuously, producing a pseudo-random bit stream. Five bits of the LFSR output are scaled by the Grain Amount control and added to both the powder and scraped-line brightness values. This creates the shimmering, particulate texture that distinguishes Tracer's output from a simple binary overlay. The grain is spatially incoherent — a new random value for every pixel — which mimics the microscopic irregularity of real aluminum powder.

### Decay as Probabilistic Erasure

Rather than fading the canvas smoothly (which would require multi-bit storage per pixel), Tracer uses a binary erasure strategy. At each vertical sync, a frame counter increments. When the counter exceeds a threshold derived from (1023 − Decay Rate), the entire canvas is cleared one byte at a time over subsequent clocks. Higher decay rates lower the threshold, causing more frequent complete clears — a rapid "shake" cycle. Lower rates allow the drawing to persist for many seconds before being wiped.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────
│   │
│   ├─ 1. Line Buffer Write     (store current Y for next line)
│   ├─ 2. Horizontal Gradient   |Y(x) - Y(x-1)|
│   ├─ 3. Vertical Gradient     |Y(x,y) - Y(x,y-1)| via line buffer
│   ├─ 4. Manhattan Sum         s_gradient = |∆H| + |∆V|
│   ├─ 5. Threshold Compare     s_gradient > s_edge_thresh → edge_pixel
│   │
│   ├─ 6. Canvas Stamp          edge_pixel → write 1 to BRAM(cx,cy)
│   │                           cx = hcount/16, cy = vcount/16
│   │                           Line weight expands stamp region
│   │
│   ├─ 7. Canvas Read           read BRAM(cx,cy) → canvas_bit
│   │      └─ Continuous Mode   (bypass canvas, use edge_pixel directly)
│   │
│   ├─ 8. Canvas Decay          periodic full-canvas clear via counter
│   │
│   ├─ 9. Render                canvas_bit=1 → scraped_y (dark + grain)
│   │                           canvas_bit=0 → powder_y (bright + grain)
│   │
│   ├─ 10. Negative             optional invert of render_y
│   ├─ 11. Frame Overlay        optional red border + white knob circles
│   └─ 12. Mix                  interpolator: dry (input) ↔ wet (render)
│
├── U/V Channels ───────────────────────────────────────────
│   │
│   └─ Canvas render is achromatic (U=512, V=512)
│      Frame overlay: red bezel (U=420, V=690), white knobs (U=512, V=512)
│
├── Sync Signals ───────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field) with 9-clock delay
│
└── Bypass ─────────────────────────────────────────────────
    └─ Select original or processed signal
```

The most important interaction is between the edge detector and the persistent canvas. The edge detector operates at full HD resolution (1280×720), but the canvas stores results at 128×96 — a roughly 10:1 spatial compression achieved by dividing pixel coordinates by 16. This means many input pixels map to the same canvas cell, and a single strong edge can stamp a block of neighboring cells via the Line Weight expansion. The decay mechanism operates at the canvas level, clearing entire bytes (8 pixels) at once, which creates the characteristic block-erase pattern visible when decay is active.

---

## Parameter Reference

<img src={tracer_control_panel} alt="Videomancer front panel with Tracer loaded"/>
*Videomancer's front panel with Tracer active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Edge Thresh
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the edge detection sensitivity. The Manhattan gradient magnitude (|∆H| + |∆V|) must exceed this threshold for a pixel to be classified as an edge and written to the canvas. At low values, even subtle luminance transitions produce contours — gradients, skin tones, and soft shadows all leave marks. At high values, only hard edges with strong contrast differences trigger the detector. This is the primary control for the density of the line drawing.

---

#### Knob 2 — Line Weight
| Property | Value |
|----------|-------|
| Range | 1px – 4px |
| Default | 1px |
| Suffix | px |

Selects the pen width for canvas stamping. Four discrete sizes are available (1×1 to 4×4 pixels in canvas space). At the narrowest setting, each detected edge marks a single canvas cell, producing thin, precise contour lines. At wider settings, edge stamps expand to neighboring cells, creating bolder strokes that fill in faster. Because the canvas is 128×96, even a 1-pixel pen produces visibly chunky marks on the HD display.

---

#### Knob 3 — Decay Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls how frequently the entire canvas is erased. At 0%, the canvas never decays — contours accumulate indefinitely until the drawing saturates. As the control increases, the interval between full-canvas clears shortens. At maximum, the canvas clears almost every frame, producing a flickering, ephemeral contour effect. Mid-range values (30–50%) create a dynamic equilibrium where contours build up and fade away over several seconds.

---

#### Knob 4 — Powder Brt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Sets the brightness of the unscraped aluminum powder — the background tone of the canvas. At maximum, the powder regions are near-white, giving the classic silver-screen look. Reducing this control darkens the powder layer, making the overall image dimmer but increasing the relative contrast with the dark scraped lines. The LFSR grain texture is added on top of this base brightness.

---

#### Knob 5 — Grain Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the amplitude of the LFSR-derived grain noise added to both powder and scraped regions. At 0%, the canvas renders with smooth, uniform brightness. As the control increases, the characteristic shimmering aluminum texture becomes visible — a spatially random noise pattern that changes every pixel. High grain amounts create a heavily textured, almost stippled surface that evokes the tactile quality of real aluminum powder.

---

#### Knob 6 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 62.6% |
| Suffix | % |

Adjusts the brightness of the scraped (dark line) regions. At low values, scraped areas are near-black, producing maximum contrast against the bright powder. Higher values brighten the scraped lines, reducing the visual separation between drawn and undrawn areas. A subtle amount of grain texture is also added to the scraped regions (at one-quarter the amplitude of the powder grain) to maintain surface coherence.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Negative** | Normal | Invert |
| **8 — Frame** | Off | On |
| **9 — Continuous** | Accum | Stream |
| **10 — Clear** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control binary rendering options that shape the overall character of the output. Negative inverts the brightness polarity. Frame adds a decorative red border. Continuous bypasses the persistent canvas entirely. Clear forces the canvas to zero. Bypass passes the input straight through.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original input video and the Tracer-rendered output. At 100%, the output is fully Tracer. At 0%, the original video passes through unaffected. Intermediate values blend the two, which can produce an interesting semi-transparent overlay of contour lines on top of the source video — an augmented-reality drawing effect.

---

## Guided Exercises

These exercises progress from simple contour detection to full Etch A Sketch simulation with frame overlay and decay animation.

### Exercise 1: Live Contour Drawing

<img src={tracer_exercise1_result} alt="Live Contour Drawing result"/>
*Live Contour Drawing — simulated result across source images.*
**Source**: A live camera feed pointed at objects with clear edges — books, hands, geometric shapes.

**Objective**: Learn how the edge detector and persistent canvas interact to build up a contour drawing over time.

1. **Set moderate threshold**: Turn Edge Thresh to about 40%. Move objects in front of the camera and watch contour lines appear on the canvas.
2. **Vary sensitivity**: Lower the threshold to 20%. Subtle textures and soft shadows now register as edges, filling the canvas more densely.
3. **Pen width**: Sweep Line Weight through all 4 positions. Notice how thicker pens create bolder, more filled-in drawings.
4. **Decay cycle**: Increase Decay Rate to about 50%. Watch as old contours fade away while new ones are drawn — the canvas breathes.
5. **Freeze and accumulate**: Set Decay Rate to 0%. Hold a high-contrast object still and watch the drawing accumulate to full density.

**Key concepts**: Edge detection sensitivity, persistent canvas accumulation, decay as temporal filtering, pen width as stamp expansion

---

### Exercise 2: Classic Etch A Sketch Aesthetic

<img src={tracer_exercise2_result} alt="Classic Etch A Sketch Aesthetic result"/>
*Classic Etch A Sketch Aesthetic — simulated result across source images.*
**Source**: Footage with strong geometric edges — architecture, signage, or a test pattern.

**Objective**: Recreate the characteristic silver-screen appearance of the iconic drawing toy.

1. **Powder brightness**: Set Powder Brt to about 80% for a silver-white background.
2. **Line darkness**: Set Contrast to about 30% for dark scraped lines.
3. **Add grain**: Increase Grain Amt to about 50% to create the aluminum particle shimmer.
4. **Enable frame**: Toggle Frame on. The red border and white knob circles complete the toy aesthetic.
5. **Adjust threshold**: Set Edge Thresh around 45% so that only medium-to-strong edges are drawn, producing clean line art.
6. **Slow decay**: Set Decay Rate to about 20% for a gradual fade that keeps the drawing visible for several seconds.

**Key concepts**: Powder and scraped brightness create the drawing medium, grain simulates aluminum texture, frame overlay completes the toy aesthetic

---

### Exercise 3: Inverted Trace with Motion Trails

<img src={tracer_exercise3_result} alt="Inverted Trace with Motion Trails result"/>
*Inverted Trace with Motion Trails — simulated result across source images.*
**Source**: Footage with significant motion — dancers, traffic, or hands gesturing.

**Objective**: Use negative mode and moderate decay to create glowing motion trails on a dark background.

1. **Enable negative**: Toggle Negative to Invert. The background becomes dark and scraped lines become bright — like phosphor traces on a CRT.
2. **Low decay**: Set Decay Rate to about 30%. Motion trails persist for a few seconds before fading.
3. **High sensitivity**: Set Edge Thresh to about 25% to capture as many contours as possible.
4. **Thick lines**: Set Line Weight to 3 or 4 px for bold, glowing strokes.
5. **Reduce grain**: Set Grain Amt to about 15% for a cleaner, more luminous appearance.
6. **Try continuous mode**: Toggle Continuous to Stream for real-time edge visualization without accumulation. Compare with Accum mode.
7. **Clear and restart**: Toggle Clear momentarily to wipe the canvas and watch it rebuild from scratch.

**Key concepts**: Negative mode inverts the brightness model, decay rate controls motion trail duration, continuous mode disables temporal memory

---


## Tips

- **Threshold is the primary creative control**: It determines what counts as an "edge." Low thresholds create dense, noisy contour maps; high thresholds produce clean, sparse line drawings.
- **Decay creates animation**: Without decay, the canvas eventually saturates to solid scraped. Use decay to create a living drawing that builds up and fades in real time.
- **Continuous mode for live edge visualization**: Stream mode bypasses the canvas entirely, turning Tracer into a simple real-time edge detector — useful for previewing what the threshold captures before committing to canvas mode.
- **Frame overlay sells the aesthetic**: The red border and white knobs instantly evoke the classic toy. Combine with moderate powder brightness and grain for maximum nostalgia.
- **Negative mode for phosphor traces**: Inverted rendering on a dark background creates a CRT-like oscilloscope trace effect, especially effective with moving subjects and moderate decay.
- **Low-resolution charm**: The 128×96 canvas is intentionally chunky. Embrace the blocky pixel aesthetic rather than fighting it — it is the source of Tracer's unique visual character.
- **Mix for augmented overlay**: At 50% mix, the contour drawing overlays the source video semi-transparently, creating an annotated, X-ray-like view of the scene's edge structure.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory within the FPGA used here to store the persistent 128×96 1-bit canvas. |
| **Canvas** | The 128×96 1-bit bitmap that accumulates detected edge contours over time. |
| **Contour** | A line or curve tracing a boundary of equal luminance in the image, detected by the gradient operator. |
| **Decay** | Probabilistic erasure of the canvas contents over time, simulating the shake-to-erase behavior of the physical toy. |
| **Edge Detection** | The process of identifying pixels where luminance changes sharply, implemented here as a Manhattan gradient with threshold comparison. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable IC executing the real-time video processing pipeline. |
| **Gradient** | The rate of luminance change between adjacent pixels; computed separately for horizontal and vertical axes. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used here for the aluminum grain texture. |
| **Line Buffer** | A one-line RAM delay used to access the previous scanline's Y values for vertical gradient computation. |
| **Manhattan Distance** | The sum of absolute horizontal and vertical differences, |∆H| + |∆V|, used as the gradient magnitude. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage for brightness and contrast adjustment. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |
