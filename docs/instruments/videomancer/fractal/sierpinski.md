---
draft: true
sidebar_position: 252
slug: /instruments/videomancer/sierpinski
title: "Sierpinski"
image: /img/instruments/videomancer/sierpinski/sierpinski_hero.png
description: "The Sierpinski triangle is one of the simplest fractals to describe but one of the richest to explore."
---

import sierpinski_hero from '/img/instruments/videomancer/sierpinski/sierpinski_hero.png';
import sierpinski_animation from '/img/instruments/videomancer/sierpinski/sierpinski_animation.gif';
import sierpinski_control_panel from '/img/instruments/videomancer/sierpinski/sierpinski_control_panel.png';
import sierpinski_exercise1_result from '/img/instruments/videomancer/sierpinski/sierpinski_exercise1_result.gif';
import sierpinski_exercise2_result from '/img/instruments/videomancer/sierpinski/sierpinski_exercise2_result.gif';
import sierpinski_exercise3_result from '/img/instruments/videomancer/sierpinski/sierpinski_exercise3_result.gif';

# Sierpinski

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={sierpinski_hero} alt="Sierpinski hero image"/>
*Sierpinski generating nested XOR fractal textures with warm-toned color mapping and video-warped coordinate space.*
<img src={sierpinski_animation} alt="Sierpinski animated output"/>
*Sierpinski output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

The Sierpinski triangle is one of the simplest fractals to describe but one of the richest to explore. Take two numbers — a horizontal coordinate and a vertical coordinate — and XOR their binary representations together. The result is a self-similar pattern of nested triangles that repeats at every power of two. Sierpinski implements this operation in real time across the entire video frame, using direct digital synthesis (DDS) accumulators as the coordinate sources.

Two independent fractal layers run simultaneously at different frequency ratios. They can be combined via AND (intersection — sparse, skeletal patterns) or XOR (symmetric difference — denser, more intricate textures). A bit-slice selector lets you choose which binary digit of the combined result drives the output, effectively zooming into different levels of the fractal hierarchy. Lower bits reveal fine-grained structure; higher bits show broad geometric divisions.

The program bridges generative synthesis and video processing. In Warp mode, the input video's luminance bends the fractal coordinate space, causing the self-similar geometry to flow around the contours of the source image. In Threshold mode, the video acts as a luminance key — revealing the input signal where it falls below the Video Mod level and showing the fractal everywhere else. The Key Mix fader crossfades between the dry input and the wet fractal output across all three YUV channels.

---

## Background

### Sierpinski's Triangle and Binary XOR

Wacław Sierpiński described his triangle in 1915, but the structure appears much earlier — in Pascal's triangle (odd entries form the pattern), in cellular automata (Rule 90), and in the parity function of binary numbers. The XOR operation is the computational key: for any pixel at coordinates (x, y), the bit at position *n* of (x XOR y) is 1 exactly when the *n*-th bits of x and y differ. This binary parity test, repeated across a grid, produces the characteristic nested-triangle fractal.

### Direct Digital Synthesis (DDS)

DDS is a technique borrowed from RF engineering. A phase accumulator adds a fixed increment on every clock cycle. The accumulator wraps around at its maximum value, creating a sawtooth waveform whose frequency is proportional to the increment. In Sierpinski, horizontal and vertical DDS accumulators generate the coordinate values that feed the XOR operation. Changing the frequency increment changes the spatial frequency of the fractal — higher values create finer, more tightly packed triangles; lower values create larger structures.

### Bit Slicing and Fractal Zoom

A 10-bit XOR result encodes ten different scales of fractal structure simultaneously. Bit 0 (the least significant) toggles on every pixel, creating the finest possible pattern. Bit 9 (the most significant) toggles only at the coarsest spatial division. The Bit Slice control selects which single bit drives the output, effectively choosing which fractal "zoom level" to display. Sweeping through bit slices is like looking through a microscope at progressively finer scales of the same self-similar geometry.

### Boolean Layer Composition

Two fractal layers with different DDS frequencies produce two independent Sierpinski patterns. Combining them with AND yields their intersection — only pixels where both layers are active survive, creating sparse, skeletal forms. XOR combination yields the symmetric difference — pixels active in one layer but not both — producing denser, interlocking textures with moire-like interference between the two frequency ratios.

### Video-Fractal Interaction

The relationship between input video and generated fractal is controlled by two modes. In Warp mode, the input luminance adds an offset to the DDS coordinates, bending the fractal geometry around bright regions of the source image. This is a form of spatial modulation — the fractal structure deforms to follow the video content. In Threshold mode, the input luminance acts as a hard key — regions below the threshold show the original video, regions above show the fractal. This creates composites where recognizable imagery coexists with geometric abstraction.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── DDS Accumulators ───────────────────────────────────────────
│   │
│   ├─ Layer 1: h_accum_1 += h_freq per pixel
│   │           v_accum_1 += v_freq per line
│   ├─ Layer 2: h_accum_2 += (h_freq + layer2_ratio) per pixel
│   │           v_accum_2 += (v_freq + layer2_ratio) per line
│   └─ Animation: frame_count added to H accumulators (optional)
│
├── Stage 1: Coordinate XOR + Video Modulation ─────────────────
│   │
│   ├─ Video Mod: warp → add luma·video_mod to layer 1 coords
│   │             threshold → coordinates unmodified
│   ├─ xor_result_1 = h1_mod XOR v1_mod
│   └─ xor_result_2 = h2 XOR v2
│
├── Stage 2: Layer Combination + Bit Slice ─────────────────────
│   │
│   ├─ Combined = xor_1 AND xor_2  (Layer Mode = AND)
│   │           = xor_1 XOR xor_2  (Layer Mode = XOR)
│   └─ fractal_bit = combined(slice_sel)   [bit 0–9]
│
├── Stage 3: Color Mapping ─────────────────────────────────────
│   │
│   ├─ Threshold mode + luma < video_mod → pass input YUV
│   ├─ fractal_bit=1 → Y=combined (inverted if toggle)
│   │   Color Map zones:
│   │   [0–255]   Monochrome (U=V=512)
│   │   [256–511] Warm (V up, U down)
│   │   [512–767] Cool (U up, V down)
│   │   [768–1023] Rainbow (both shift from XOR layers)
│   └─ fractal_bit=0 → black (or white if inverted), U=V=512
│
├── Stage 4: Interpolator Mix ──────────────────────────────────
│   └─ output = lerp(delayed_input, fractal_output, key_mix)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field) delayed 8 clocks
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The core fractal engine is purely combinational — no BRAMs or DSP blocks, just DDS accumulators feeding XOR gates. The two critical interaction paths are: (1) **Video-to-coordinate modulation**, where the input luminance warps the spatial geometry of the fractal in Warp mode, creating organic distortions of the otherwise rigid self-similar structure; and (2) **Dual-layer interference**, where the Layer 2 Ratio offsets the second layer's DDS frequency, creating beating patterns between the two fractal grids. The bit-slice selector then chooses at which magnification level these interactions become visible. The interpolator stage provides a smooth crossfade between the dry input and the fractal output, allowing the fractal to be overlaid at any opacity.

---

## Parameter Reference

<img src={sierpinski_control_panel} alt="Videomancer front panel with Sierpinski loaded"/>
*Videomancer's front panel with Sierpinski active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — H Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the horizontal DDS accumulator increment for layer 1. Higher values increase the horizontal spatial frequency of the fractal — creating finer, more tightly spaced triangle structures across the width of the frame. At 0%, the horizontal accumulator never advances, collapsing the fractal into vertical stripes. At 50%, a balanced scale of nested triangles fills the frame. At 100%, the triangles are so fine they approach single-pixel detail. Layer 2's horizontal frequency is offset from this value by the Layer 2 Ratio.

---

#### Knob 2 — V Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the vertical DDS accumulator increment for layer 1. This sets the vertical spatial frequency of the fractal, determining how many triangle rows appear from top to bottom of the frame. The fractal's aspect ratio is controlled by the relationship between H Freq and V Freq — equal values produce equilateral triangles, while unequal values stretch the geometry horizontally or vertically. Layer 2's vertical frequency is similarly offset by the Layer 2 Ratio.

---

#### Knob 3 — Layer 2 Ratio
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Adds a frequency offset to layer 2's DDS accumulators relative to layer 1. At 0%, both layers run at identical frequencies and produce the same pattern — AND combination yields the original pattern, XOR combination yields black. As Layer 2 Ratio increases, the second layer's fractal shifts in scale, creating interference patterns between the two grids. This is the primary control for the moire-like interactions between layers.

---

#### Knob 4 — Video Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the depth of video luminance modulation. In Warp mode, brighter pixels in the input add larger offsets to the fractal coordinates, bending the geometry. At 0%, no modulation — the fractal is perfectly rigid. At 100%, bright areas of the source image dramatically distort the fractal structure. In Threshold mode, this sets the luminance threshold — pixels below this brightness level show the input video directly while pixels above show the fractal.

---

#### Knob 5 — Bit Slice
| Property | Value |
|----------|-------|
| Range | 0 – 9 |
| Default | 5 |

Selects which bit (0–9) of the combined fractal result drives the output. Bit 0 toggles at the finest spatial scale — every pixel boundary. Bit 9 toggles at the coarsest scale — broad geometric quadrants. Sweeping bit slice from 0 to 9 is equivalent to zooming out through the fractal hierarchy. Intermediate values reveal the characteristic Sierpinski triangle at different magnifications, each self-similar to the others.

---

#### Knob 6 — Color Map
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Maps the fractal output to chrominance values across four zones. The pot sweeps through monochrome (U=V=512, pure luminance), warm tones (V increases, U decreases — reds and oranges), cool tones (U increases, V decreases — blues and cyans), and rainbow mode (both U and V shift independently based on the two XOR layers, creating multicolored interference patterns). The luminance channel always carries the combined fractal value.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Layer Mode** | AND | XOR |
| **8 — Video Mode** | Threshold | Warp |
| **9 — Animate** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent binary options: the boolean operation for layer combination, the video interaction mode, animation on/off, output polarity, and bypass. Layer Mode and Video Mode are the most impactful — they fundamentally change the character of the fractal and how it relates to the input video. Animate adds temporal evolution. Invert swaps the figure/ground relationship of the fractal pattern.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Key Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the delayed input video and the fractal output via three interpolator instances (one each for Y, U, V). At 0%, output is pure input video — the fractal is invisible. At 100%, output is pure fractal. Intermediate values overlay the fractal onto the source at partial opacity. This enables subtle fractal textures to be layered over existing video content rather than replacing it entirely.

---

## Guided Exercises

These exercises progress from basic fractal generation through multi-layer interference to video-interactive compositing. Each introduces a new layer of complexity in the Sierpinski processing chain.

### Exercise 1: Basic Fractal Exploration

<img src={sierpinski_exercise1_result} alt="Basic Fractal Exploration result"/>
*Basic Fractal Exploration — simulated result across source images.*
**Objective**: Learn how H Freq, V Freq, and Bit Slice interact to generate and navigate Sierpinski fractal patterns at different scales.

1. **Default fractal**: With default settings (H Freq 50%, V Freq 50%, Bit Slice ~5), observe the characteristic nested-triangle pattern filling the frame.
2. **Frequency sweep**: Slowly decrease H Freq toward 0%. Watch the triangles stretch horizontally until they collapse into vertical stripes. Return to 50%.
3. **Vertical sweep**: Decrease V Freq similarly. The pattern stretches vertically into horizontal bands.
4. **Aspect ratio**: Set H Freq to ~30% and V Freq to ~70%. Observe the resulting elongated triangles.
5. **Bit slice zoom**: Slowly sweep Bit Slice from 0 to 9. Watch the pattern zoom out through ten levels of self-similar structure — each scale is a magnified copy of the finest details.
6. **Invert**: Toggle Invert to swap figure and ground. Note how the negative space reveals the complementary fractal geometry.

**Key concepts**: XOR between coordinates produces self-similar fractal structure, H/V Freq controls spatial frequency independently per axis, bit slicing reveals different fractal zoom levels, each bit level is self-similar to every other

---

### Exercise 2: Dual-Layer Interference

<img src={sierpinski_exercise2_result} alt="Dual-Layer Interference result"/>
*Dual-Layer Interference — simulated result across source images.*
**Objective**: Explore how Layer 2 Ratio and Layer Mode create interference patterns between two fractal grids.

1. **Single layer**: Set Layer 2 Ratio to 0%. Both layers are identical — AND shows the original pattern, XOR shows black (identical layers cancel).
2. **Small offset**: Slowly increase Layer 2 Ratio from 0% toward ~25%. In XOR mode, watch moire-like interference patterns emerge as the two grids begin to diverge.
3. **AND vs XOR**: Toggle Layer Mode between AND and XOR with Layer 2 Ratio at ~25%. AND creates thin, skeletal intersection lines. XOR creates denser interlocking regions.
4. **Large offset**: Push Layer 2 Ratio to ~75%. The interference becomes coarser and more chaotic.
5. **Warm color**: Set Color Map to ~40% and observe how the warm-tone color mapping colorizes the fractal structure.
6. **Animate**: Enable Animate (Switch 9) to add scrolling motion. The two layers scroll at different rates due to the frequency offset, creating evolving interference.

**Key concepts**: Two fractal layers at different frequencies create moire interference, AND intersects (sparse), XOR differentiates (dense), Layer 2 Ratio controls the frequency offset between layers

---

### Exercise 3: Video-Fractal Compositing

<img src={sierpinski_exercise3_result} alt="Video-Fractal Compositing result"/>
*Video-Fractal Compositing — simulated result across source images.*
**Objective**: Use both Video Mode settings to composite the fractal with the input video signal in different ways.

1. **Threshold mode**: Set Video Mode to Threshold. Set Video Mod to ~40%. Observe how the fractal appears only where the input luminance exceeds the threshold. Dark areas of the image show through directly.
2. **Threshold sweep**: Slowly increase Video Mod. More of the image is revealed through the fractal. At 100%, nearly everything is fractal.
3. **Switch to Warp**: Toggle Video Mode to Warp. With Video Mod at ~40%, the fractal geometry deforms and flows around the bright contours of the source image.
4. **Deep warp**: Increase Video Mod to ~80%. The fractal structure is now heavily distorted by the input luminance — bright areas create large coordinate offsets, producing organic, flowing distortions.
5. **Mix down**: Lower Key Mix to ~50% to blend the warped fractal with the unprocessed input at half opacity. The fractal becomes a textural overlay.
6. **Rainbow color**: Set Color Map to ~90% for rainbow mode. Both XOR layers contribute independently to U and V, creating polychromatic fractal textures over the video.

**Key concepts**: Threshold mode composites by luminance comparison, Warp mode bends fractal coordinates with video content, Key Mix crossfades wet/dry, color mapping adds chrominance to the fractal structure

---


## Tips

- **Start with monochrome**: Set Color Map to 0% when exploring fractal geometry. Color adds visual complexity that can make it harder to understand the underlying structure. Add color after you understand the spatial pattern.
- **Bit Slice is your zoom control**: Sweeping bit slice is the fastest way to explore the fractal. Each level is a magnified copy of the finest structure — a visual demonstration of self-similarity.
- **Layer 2 Ratio at small offsets creates the richest textures**: Large offsets create coarse interference; small offsets (5–15%) produce intricate moire patterns between the two fractal grids.
- **Warp mode with moving video creates organic motion**: Static fractals feel rigid. Route a slowly moving camera through Warp mode to give the self-similar geometry organic, flowing motion.
- **Use Key Mix for subtle textures**: At 100%, the fractal dominates. At 20–40%, it becomes a translucent overlay — a fractal texture laid over the source video, useful for adding geometric structure without obliterating the image.
- **Feedback routing amplifies structure**: Route the output back to the input. The fractal modulates its own coordinate space, creating recursive self-similar patterns that evolve and cascade with each feedback pass.
- **Animate + Layer 2 Ratio = evolving interference**: When both layers run at different frequencies and animation is on, they scroll at different rates. The resulting interference pattern evolves continuously — useful for generative visual backgrounds.

---

## Glossary

| Term | Definition |
|------|------------|
| **AND** | Bitwise logical conjunction; output is 1 only when both inputs are 1. Used as one of two layer combination modes. |
| **Bit Slice** | Selecting a single binary digit from a multi-bit value. Different bit positions correspond to different spatial scales. |
| **DDS** | Direct Digital Synthesis; a technique using a phase accumulator with a fixed increment to generate repeating waveforms at precise frequencies. |
| **Fractal** | A geometric structure that exhibits self-similarity at different scales; smaller portions resemble the whole. |
| **Interpolator** | A hardware module that performs linear interpolation (crossfade) between two values based on a mixing coefficient. |
| **Moire** | An interference pattern created when two similar periodic structures overlap at slightly different scales or orientations. |
| **Phase Accumulator** | A counter that wraps around at its maximum value, producing a sawtooth progression proportional to its increment rate. |
| **Self-Similar** | A property where a structure contains smaller copies of itself at every scale of magnification. |
| **Sierpinski Triangle** | The specific fractal pattern produced by XOR of spatial coordinates, named after mathematician Wacław Sierpiński. |
| **XOR** | Bitwise exclusive-or; output is 1 when inputs differ. The core operation generating Sierpinski fractal patterns. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
