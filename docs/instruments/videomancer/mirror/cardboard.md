---
draft: true
sidebar_position: 35
slug: /instruments/videomancer/cardboard
title: "Cardboard"
image: /img/instruments/videomancer/cardboard/cardboard_hero.png
description: "Before cinema, before animation, there was the paper theater — a miniature stage built from flat cardboard cutouts arranged in parallel planes."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import cardboard_hero from '/img/instruments/videomancer/cardboard/cardboard_hero.png';
import cardboard_control_panel from '/img/instruments/videomancer/cardboard/cardboard_control_panel.png';
import cardboard_exercise1_result from '/img/instruments/videomancer/cardboard/cardboard_exercise1_result.png';
import cardboard_exercise2_result from '/img/instruments/videomancer/cardboard/cardboard_exercise2_result.png';
import cardboard_exercise3_result from '/img/instruments/videomancer/cardboard/cardboard_exercise3_result.png';
import cardboard_source1_kodim01 from '/img/instruments/videomancer/cardboard/cardboard_source1_kodim01.png';
import cardboard_source2_kodim02 from '/img/instruments/videomancer/cardboard/cardboard_source2_kodim02.png';
import cardboard_source3_kodim01_bw from '/img/instruments/videomancer/cardboard/cardboard_source3_kodim01_bw.png';

# Cardboard

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: cardboard_source1_kodim01, after: cardboard_hero },
    { label: "Kodim02", before: cardboard_source2_kodim02, after: cardboard_hero },
    { label: "Kodim01 B&W", before: cardboard_source3_kodim01_bw, after: cardboard_hero },
  ]}
/>
*Cardboard splitting a portrait into four luma-driven depth planes with staggered horizontal parallax, revealing paper theater cutout layers in a single video frame.*

---

## Overview

Before cinema, before animation, there was the paper theater — a miniature stage built from flat cardboard cutouts arranged in parallel planes. Actors, scenery, and sky were each painted onto separate sheets, then stacked behind a proscenium arch. Slide the sheets sideways at different speeds and a convincing illusion of depth appears, even though every element is perfectly flat. Cardboard recreates this illusion in the electronic domain.

The program segments every frame into four depth layers based on luminance thresholds. Dark pixels become the background; bright pixels become the foreground. Each layer is assigned a different horizontal offset via a 32-sample shift register, so the background shifts by a different amount than the foreground — producing the parallax effect of a paper theater viewed from a moving vantage point. The offsets are fixed within a frame, creating a hard-edged, flat-plane look rather than a smooth depth gradient.

At conservative settings, the effect is subtle — a gentle separation of tonal planes with a slight horizontal stagger. At extreme settings, the image fractures into bold cutout silhouettes with visible seams between layers, exaggerated parallax, and optional monochrome desaturation that reinforces the paper-and-cardboard aesthetic. Edge detection between layers adds dark contour lines at the boundaries, completing the illusion of stacked flat sheets with slight shadows between them.

---

## Background

### What Is a Paper Theater?

The paper theater (also called toy theater or juvenile drama) originated in early 19th-century England. Publishers printed scenery and character figures onto sheets of cardboard. The sheets were cut out and mounted in grooved tracks inside a miniature proscenium stage. By sliding the scenery sheets at different speeds, operators created parallax — the same depth cue the human visual system uses when looking out a train window. Nearby objects move fast; distant objects move slowly. Cardboard applies this same principle to video, using luminance as a proxy for depth.

### Luma-Driven Depth Segmentation

Cardboard divides the 10-bit luminance range (0–1023) into four zones using three adjustable thresholds. Pixels darker than the first threshold become Layer 0 (background). Pixels between the first and second thresholds become Layer 1, and so on up to Layer 3 (foreground, the brightest pixels). The threshold spacing is controlled by a single knob that scales all three boundaries together, keeping their relative proportions fixed. This is a simple form of depth-from-luminance — an assumption that brighter objects are closer to the viewer. While not physically accurate for arbitrary scenes, it works well with many video compositions, especially high-contrast sources or images lit with a key/fill separation.

### Parallax via Horizontal Delay

The horizontal offset for each layer comes from a 32-sample shift register. Every pixel clock, the current input pixel is pushed into position 0 and all previous samples shift up. To read a pixel with a horizontal offset of N, the program taps position N in the shift register — which holds the pixel from N columns earlier on the same scan line. Layer 0 reads from tap 0 (no delay, no parallax). Layer 1 reads from half the base offset. Layer 2 reads from the full base offset. Layer 3 reads from 1.5× the base offset, clamped to 31 samples. The direction toggle inverts the tap index (31 minus the computed tap), reversing which side of the frame the parallax shifts toward.

### Edge Detection Between Layers

Where two layers meet, the luminance changes abruptly — just as a real paper cutout creates a visible edge against the layer behind it. Cardboard detects these edges by comparing each pixel's luminance to the previous scan line's luminance (stored in a video line buffer). When the absolute difference exceeds the edge threshold, the output pixel is darkened to half its luminance, creating a visible contour line at layer boundaries. This contour mimics the shadow cast by a physical cardboard edge onto the layer behind it.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y/U/V Channels ─────────────────────────────────────────────
│   │
│   ├─ 1. Input Register          (capture + push to 32-sample shift reg)
│   │                              (write current Y to line buffer)
│   │
│   ├─ 2. Layer Classification    (luma thresholds → layer 0/1/2/3)
│   │                              (compute shift-reg tap per layer)
│   │                              (direction toggle: invert tap index)
│   │
│   ├─ 3. Shift Register Read     (read Y/U/V from computed tap)
│   │                              (flat mode: bypass shift, use source pixel)
│   │                              (line buffer data arrives)
│   │
│   ├─ 4. Edge Detection          (|current line Y − prev line Y| > threshold)
│   │                              (shifted Y/U/V passed through)
│   │
│   ├─ 5. Layer Contrast + Edge   (per-layer brightness: avg(Y, layer_scale))
│   │      Highlight               (edge pixels: Y ← Y >> 1)
│   │                              (mono mode: U/V ← 512)
│   │
│   └─ 6. Output Compose          (final clamped Y/U/V)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 10-stage delay pipeline (hsync, vsync, field)
│
├── Interpolator (4 clks) ─────────────────────────────────────
│   └─ 3× interpolator_u wet/dry mix (Y, U, V)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original (delayed) or processed signal
```

The critical data path splits early: the original input luminance feeds both the layer classifier (stage 2) and the line buffer write (stage 1), while the shift register stores the full YUV pixel for later parallax readout. Layer assignment is based on the *original* pixel luminance, but the output pixel data comes from the *shifted* tap position. This means a pixel classified as Layer 2 at column 400 may actually display the YUV data from column 380 (or wherever the shift register tap points), creating the parallax displacement.

Edge detection also operates on the original (unshifted) luminance, comparing the current scan line against the previous line stored in the video line buffer. This ensures that layer boundaries are detected based on the true image content rather than on the shifted parallax result. The edge darkening, however, is applied to the shifted pixel — so contour lines appear at the correct spatial position in the parallax-displaced output.

---

## Parameter Reference

<img src={cardboard_control_panel} alt="Videomancer front panel with Cardboard loaded"/>
*Videomancer's front panel with Cardboard active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Layers
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spacing between the three luma thresholds that divide the image into four depth layers. At 0%, the thresholds are tightly clustered near the low end of the luminance range, pushing most pixels into Layer 3 (foreground) and collapsing the parallax separation. As the control increases, the thresholds spread apart across the full 10-bit range, producing a more even distribution of pixels across all four layers. The three thresholds are computed as 128 + spacing/4, 256 + spacing/2, and 384 + spacing/2 (clamped to 1023). At maximum, the layers carve the luminance range into well-separated zones with distinct parallax offsets.

---

#### Knob 2 — Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the base horizontal parallax offset. The 10-bit register value is divided by 32 to produce a 0–31 sample offset. Layer 0 receives zero offset (stationary background). Layer 1 receives half the base offset. Layer 2 receives the full base offset. Layer 3 receives 1.5× the base offset, clamped to 31 samples. At 0%, all layers share the same position and no parallax is visible. At maximum, the foreground layer is displaced by up to 31 pixels from the background, creating a dramatic paper-cutout separation. The direction of displacement is controlled by the Mode toggle.

---

#### Knob 3 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Mapped to the layer contrast register in the VHDL parameter header, but this register is not read by the current processing pipeline. Adjusting this control has no visible effect on the output. The per-layer brightness adjustment is instead governed entirely by the Shadow control (Pot 5) and the hard-coded layer scale formula. This discrepancy between the TOML label ("Threshold") and the VHDL behavior should be noted when designing patches — the knob is physically present but electrically unused.

---

#### Knob 4 — Edge Ctr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the luminance difference threshold for edge detection between layers. The absolute difference between the current scan line's luminance and the previous scan line's luminance is compared against this value. When the difference exceeds the threshold, the pixel is classified as an edge and its luminance is halved, creating a dark contour line. At 0%, even tiny luminance variations trigger edge darkening, producing dense contour lines throughout the image. At maximum, only the most extreme luminance transitions (hard layer boundaries) produce visible edges. This control lets you tune the contour density from fine cross-hatching to bold silhouette outlines.

---

#### Knob 5 — Shadow
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness floor applied to the darkest layer (Layer 0, background). The per-layer brightness formula averages each pixel's shifted luminance with a layer-dependent scale value: Layer 0 uses the Shadow register directly, Layer 1 uses 512 + Shadow/2, Layer 2 uses 768 + Shadow/4, and Layer 3 always uses 1023 (full brightness). At 0%, the background layer is averaged with zero, darkening it to roughly half its original brightness and creating a strong depth-from-brightness cue. At maximum (1023), all layers receive nearly equal brightness and the depth illusion comes only from the horizontal parallax offset.

---

#### Knob 6 — Depth Rng
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Mapped in the TOML configuration as "Depth Rng" but the corresponding register (registers_in(5)) is not read by the VHDL processing pipeline. Adjusting this control has no visible effect on the output. It is reserved for a potential future enhancement — for example, scaling the per-layer offset multipliers or modulating the threshold spacing dynamically.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Theater | Popup |
| **8 — Edges** | Hard | Torn |
| **9 — Palette** | Paper | Color |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 each contribute a single bit to the packed toggle register (registers_in(6)). The TOML configuration presents multi-label selectors for Switches 7 and 8, but the VHDL extracts only individual bits, reducing them to binary toggles. Switch 7's four labels (Theater/Popup vs. Diorama/Relief) map to bit 0 (parallax direction). Switch 8's four labels (Hard/Torn vs. Cut/Fold) map to bit 1 (parallax vs. flat cutout mode). Switch 10's bit (bit 3) is declared but not used in the processing pipeline.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade controlling the blend between the original (delayed) input and the fully processed output. At 0%, the output is the unmodified input signal. At 100%, the output is the fully processed parallax-layered result. Intermediate positions produce a transparent overlay where the depth layers ghost over the original image. This control uses three interpolator_u instances (one per Y/U/V channel) with 4-clock latency for smooth, alias-free blending.

---

## Guided Exercises

These exercises progress from basic layer separation to full paper theater parallax, building familiarity with threshold tuning, parallax depth, and edge contouring.

### Exercise 1: Layer Separation

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: cardboard_source1_kodim01, after: cardboard_exercise1_result },
    { label: "Kodim02", before: cardboard_source2_kodim02, after: cardboard_exercise1_result },
    { label: "Kodim01 B&W", before: cardboard_source3_kodim01_bw, after: cardboard_exercise1_result },
  ]}
/>
*Layer Separation — simulated result across source images.*
**Source**: A portrait or landscape with a clear foreground subject and a darker background — strong tonal separation between near and far elements.

**Objective**: Learn how the luma thresholds divide the image into four flat depth planes, and how the Shadow control creates brightness-based depth cues.

1. **Default state**: Set all controls to 50%. The image should show four tonal bands with moderate parallax.
2. **Threshold spread**: Slowly increase Layers from 0% to 100%. Watch the threshold boundaries migrate across the luminance range, redistributing pixels among the four layers.
3. **Background darkness**: Lower Shadow to 0%. The darkest layer dims to roughly half brightness, creating a strong depth cue.
4. **Full brightness**: Raise Shadow to 100%. All layers converge to similar brightness, eliminating the depth-from-brightness effect.
5. **Edge contours**: Lower Edge Ctr to ~20%. Dark contour lines appear at layer boundaries where luminance changes sharply between scan lines.
6. **Flat mode**: Switch Edges to "Cut" or "Fold" to disable parallax. The layer brightness and contours remain but all horizontal displacement stops.

**Key concepts**: Luma thresholds segment the image into four flat depth planes, the Shadow control darkens the background layer to reinforce depth, edge detection adds contour lines at layer boundaries

---

### Exercise 2: Parallax Depth

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: cardboard_source1_kodim01, after: cardboard_exercise2_result },
    { label: "Kodim02", before: cardboard_source2_kodim02, after: cardboard_exercise2_result },
    { label: "Kodim01 B&W", before: cardboard_source3_kodim01_bw, after: cardboard_exercise2_result },
  ]}
/>
*Parallax Depth — simulated result across source images.*
**Source**: High-contrast material with distinct bright and dark regions — a lit face against a dark background, or neon signage against a night sky.

**Objective**: Explore horizontal parallax displacement and direction reversal.

1. **Start flat**: Set Offset to 0% and Layers to ~50%. Four tonal layers are visible but share the same horizontal position.
2. **Add parallax**: Slowly increase Offset. The foreground layer slides sideways relative to the background. Note the hard edges where layers meet — the paper cutout effect.
3. **Full offset**: Push Offset to 100%. The foreground is displaced by up to 31 pixels from the background. The layer seams are dramatic.
4. **Reverse direction**: Switch Mode from "Theater" to "Diorama." The parallax reverses — the layer that was stationary now moves, and vice versa.
5. **Edge enhancement**: Lower Edge Ctr to add dark contour lines at the parallax seams. These mimic the shadows between stacked cardboard sheets.
6. **Monochrome**: Switch Palette to "Color" (mono mode). The desaturated output emphasizes the structural parallax over color information.

**Key concepts**: The shift register creates per-layer horizontal displacement, direction inversion reverses which layer is stationary, edge contours mark layer boundaries like physical cutout shadows

---

### Exercise 3: Cardboard Diorama

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: cardboard_source1_kodim01, after: cardboard_exercise3_result },
    { label: "Kodim02", before: cardboard_source2_kodim02, after: cardboard_exercise3_result },
    { label: "Kodim01 B&W", before: cardboard_source3_kodim01_bw, after: cardboard_exercise3_result },
  ]}
/>
*Cardboard Diorama — simulated result across source images.*
**Source**: Any footage with a range of tonal values — landscapes, cityscapes, or abstract video synthesis patches.

**Objective**: Combine all parameters to create a full paper theater diorama look with parallax, contours, layer contrast, and optional monochrome.

1. **Layer spread**: Set Layers to ~70% for well-separated depth zones.
2. **Strong parallax**: Set Offset to ~60% for visible but not extreme displacement.
3. **Deep shadows**: Set Shadow to ~15% for a dramatic falloff in the background layer.
4. **Tight edges**: Set Edge Ctr to ~15% for pronounced contour lines between all layers.
5. **Paper mode**: Switch Palette to "Color" for monochrome. The image now looks like a hand-cut shadow box.
6. **Direction sweep**: Toggle Mode between positions while observing how the parallax shifts across the frame.
7. **Mix blend**: Pull Mix down to ~60% to ghost the processed layers over the original image, creating a translucent overlay effect.

**Key concepts**: All parameters interact — threshold spacing determines which pixels fall into which layer, parallax offset determines how far layers separate, shadow and edge controls add sculptural depth cues, monochrome mode strips the image to pure form

---


## Tips

- **Luma is depth**: Cardboard treats bright pixels as foreground and dark pixels as background. Light your scene with this assumption in mind — key light on the subject, dark background — for the most convincing parallax.
- **Edge Ctr acts as a contour pen**: Low values produce dense, fine contour lines across the entire image. High values limit contours to only the boldest layer boundaries. Start high and reduce gradually.
- **Shadow creates atmosphere**: Darkening the background layer (low Shadow values) dramatically increases the perceived depth. The effect is reminiscent of theatrical lighting that dims the upstage flats.
- **Flat mode for tonal posters**: Switching Edges to "Cut" or "Fold" disables parallax but keeps the four-layer contrast separation, producing a flat posterized look with edge contours — useful as a standalone effect.
- **Feedback loops**: Routing the processed output back to the input creates recursive layer separation — the parallax shifts compound across iterations, producing increasingly abstract stacked-plane landscapes.
- **Pot 3 and Pot 6 are inactive**: The Threshold and Depth Rng knobs are physically present but not read by the current VHDL pipeline. Leave them at default or use them as scratch controls in your patch without affecting the image.
- **Mix for ghosting**: Pulling the Mix fader to an intermediate position blends the parallax layers with the original image, creating a translucent overlay where the depth planes ghost over the unshifted source.
- **Direction for animation**: If your source is scrolling or panning, switching between Theater and Diorama modes changes whether the parallax reinforces or counteracts the pan direction.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chrominance** | The color information (U and V channels) in a video signal, independent of brightness. |
| **Depth segmentation** | The process of classifying pixels into discrete layers based on a visual property (here, luminance) as a proxy for distance from the viewer. |
| **Interpolator** | A hardware module that computes weighted blends between two values, used here for wet/dry crossfading of Y, U, and V channels. |
| **Line buffer** | A memory element storing one complete scan line of video data, enabling vertical comparisons between adjacent lines for edge detection. |
| **Luminance** | The brightness component (Y channel) of a YUV video signal, measured on a 0–1023 scale in 10-bit video. |
| **Parallax** | The apparent displacement of objects at different distances when the viewpoint shifts, simulated here by applying different horizontal offsets to each depth layer. |
| **Proscenium** | The architectural frame surrounding the front of a stage, through which the audience views the performance; used here by analogy for the video frame edge. |
| **Scan line** | A single horizontal row of pixels in a video frame, traced left to right during display. |
| **Shift register** | A chain of storage elements that passes data forward one position per clock cycle, used here to provide variable horizontal pixel delay for parallax offsets. |
| **YUV** | A color encoding system separating luminance (Y) from two chrominance components (U, V), the native format for video processing. |

---
