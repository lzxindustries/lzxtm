---
draft: true
sidebar_position: 231
slug: /instruments/videomancer/sfumato
title: "Sfumato"
image: /img/instruments/videomancer/sfumato/sfumato_hero.png
description: "Leonardo da Vinci described sfumato as painting 'in the manner of smoke, beyond the plane of focus' — the technique of eliminating hard outlines between..."
---

import sfumato_before_after from '/img/instruments/videomancer/sfumato/sfumato_before_after.png';
import sfumato_control_panel from '/img/instruments/videomancer/sfumato/sfumato_control_panel.png';
import sfumato_exercise1_result from '/img/instruments/videomancer/sfumato/sfumato_exercise1_result.png';
import sfumato_exercise2_result from '/img/instruments/videomancer/sfumato/sfumato_exercise2_result.png';
import sfumato_exercise3_result from '/img/instruments/videomancer/sfumato/sfumato_exercise3_result.png';
import sfumato_hero from '/img/instruments/videomancer/sfumato/sfumato_hero.png';
import sfumato_source1_kodim03 from '/img/instruments/videomancer/sfumato/sfumato_source1_kodim03.png';
import sfumato_source2_kodim13 from '/img/instruments/videomancer/sfumato/sfumato_source2_kodim13.png';
import sfumato_source3_kodim13_bw from '/img/instruments/videomancer/sfumato/sfumato_source3_kodim13_bw.png';

# Sfumato

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={sfumato_hero} alt="Sfumato hero image"/>
*Sfumato dissolving tonal boundaries with edge-adaptive IIR blur, depth-dependent shadow diffusion, and atmospheric haze reminiscent of Leonardo's prospettiva aerea.*
<img src={sfumato_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Sfumato applied.*

---

## Overview

Leonardo da Vinci described *sfumato* as painting "in the manner of smoke, beyond the plane of focus" — the technique of eliminating hard outlines between tones and colors so that forms appear to emerge from the air itself. The Mona Lisa's face is the canonical example: no visible brush boundary separates one shade of skin from the next. This program applies the same principle to live video.

Sfumato runs an IIR (infinite impulse response) low-pass filter along each scanline, but instead of uniform blurring it adapts the filter strength to the local luminance gradient. Where the image has a strong tonal edge, the filter applies heavily, softening the transition. Where the image is already smooth, the filter relaxes and leaves the signal nearly untouched. The result is selective softening of tonal boundaries while preserving gross spatial structure — exactly Leonardo's technique, executed at 74.25 million pixels per second.

Three additional layers deepen the atmospheric effect: *depth modulation* applies stronger blur to shadows (prospettiva aerea — distant objects appear softer and lighter), *chrominance diffusion* dissolves color boundaries more aggressively than luminance edges, and *ambient haze* lifts shadows and desaturates the entire image to simulate the scattering of light through atmosphere. An optional warm varnish mode tints the output with an amber color shift, evoking the aged appearance of an Old Master oil painting.

---

## Background

### Leonardo's Sfumato Technique

The term *sfumato* comes from the Italian *sfumare*, "to evaporate" or "to vanish like smoke." Leonardo achieved the effect by applying dozens of translucent oil glazes over a dark underpainting, each layer so thin that individual brushstrokes are invisible. The result is a continuous tonal gradient with no discernible color boundary — what modern image processing would call a *low-pass filtered* signal. This program automates the principle: the IIR filter acts as the digital equivalent of an oil glaze, and the edge-adaptive coefficient determines where the glaze is applied most heavily.

### Edge-Adaptive IIR Filtering

A standard IIR low-pass filter applied uniformly across a scanline would simply blur the entire image by a fixed amount. Sfumato modifies the filter coefficient *alpha* based on the local luminance gradient — the absolute difference between adjacent pixels. High gradient (a sharp tonal edge) produces a high alpha, meaning the filter weights the previous output heavily and smooths the transition. Low gradient (a flat area) produces a low alpha, leaving the signal nearly unchanged. This is an edge-*preserving* technique in the Anisotropic Diffusion family, but implemented as a causal 1D IIR rather than a 2D iterative PDE.

### Prospettiva Aerea — Depth-Dependent Diffusion

In atmospheric perspective, distant objects appear softer, lighter, and less saturated because light scatters through more air. Sfumato approximates this by using luminance as a proxy for depth: darker pixels are assumed to be "further away" (or in shadow), so they receive stronger blur. The depth modulation formula is `alpha × (1023 - Y × depth / 1024)`, ensuring that bright (foreground) regions are barely affected while shadows dissolve. Quadratic mode squares the depth factor for a steeper falloff.

### Chrominance Diffusion

Human vision is less sensitive to color boundaries than to luminance boundaries (this is why chroma subsampling works). Sfumato exploits this by offering extra chrominance diffusion independent of the luminance blur. When Chroma Lock is disengaged, the UV channels receive an additional half of the Chroma Diffusion parameter added to their filter alpha, causing color boundaries to dissolve further than luminance edges — exactly the way Leonardo's glazes affected pigment hue more than tonal value.

### Atmospheric Haze

The haze stage lifts shadow luminance toward mid-gray and desaturates the entire signal proportionally. The Y channel receives a lift of `haze_amount / 2`, and each chroma channel is multiplied by `(1023 - haze_amount) / 1024`. At full haze the image approaches a uniform flat gray — total atmospheric whiteout. At subtle levels it creates the silvery, slightly washed-out quality of overcast daylight seen through a veil of humidity.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Gradient Compute
│   ├─ Latch Y, U, V
│   └─ gradient = |Y_current − Y_previous|   (horizontal pixel-to-pixel)
│
├── Stage 2: Alpha Modulation
│   ├─ Edge alpha = base_alpha × gradient / threshold  (clamped at base_alpha)
│   ├─ Depth mod = 1023 − (Y × depth_amount) / 1024   [optionally squared]
│   ├─ Effective Y alpha = edge_alpha × depth_mod / 1024
│   └─ Effective UV alpha = Y alpha [+ chroma_diff/2 if unlocked]
│
├── Stage 3: IIR Filter + Haze
│   ├─ Y_out = alpha × Y_prev_out + (1−alpha) × Y_in  (resets to 512 per line)
│   ├─ U_out = alpha_uv × U_prev + (1−alpha_uv) × U_in
│   ├─ V_out = alpha_uv × V_prev + (1−alpha_uv) × V_in
│   ├─ Bidirectional: average forward with reverse-read from line buffer
│   ├─ Haze lift: Y += haze_amount / 2
│   └─ Haze desat: UV = 512 + (UV−512) × (1023−haze) / 1024
│
├── Stage 4: Varnish Warmth + Output Composite
│   ├─ If varnish: U −= warmth >> 2,  V += warmth >> 2
│   └─ Else: passthrough
│
├── Stages 5–8: interpolator_u ×3 Wet/Dry Mix
│   └─ a=delayed dry, b=composite, t=mix_amount
│
└── Output (bypass mux)
```

The IIR filter state resets to 512 (mid-gray) at every horizontal sync start, making the process purely per-scanline with no vertical memory dependency in unidirectional mode. In bidirectional mode, the forward pass result is written into a line buffer and a second pass reads the buffer in reverse, averaging the two. This creates symmetrical smoothing that doesn't favour left-over-right, at the cost of one BRAM tile. The gradient computation uses the *raw input* pixel (before filtering), so the edge-adaptive coefficient responds to the original image structure rather than to previously-smoothed data.

---

## Parameter Reference

<img src={sfumato_control_panel} alt="Videomancer front panel with Sfumato loaded"/>
*Videomancer's front panel with Sfumato active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Diffusion
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Maps to `registers_in(0)`, the base IIR blur strength. At 0% the filter coefficient is zero and the output equals the input — no diffusion. As the value increases, the IIR weights its own previous output more heavily, creating progressively stronger horizontal blur on tonal transitions. At 100% the filter is maximally sticky, smearing nearly all tonal variation into a uniform wash. The edge-adaptive gradient and depth modulation scale *down* from this base value, so it sets the ceiling of how much smoothing is possible.

---

#### Knob 2 — Edge Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Maps to `registers_in(1)`, the edge detection gradient threshold. When the luminance gradient between adjacent pixels is below this value, the blur alpha is proportionally reduced; when it equals or exceeds the threshold, the full base alpha is applied. Low thresholds mean even gentle gradients trigger full diffusion. High thresholds restrict heavy smoothing to only the sharpest tonal edges, leaving soft gradients nearly untouched. This is the primary tool for controlling *where* in the image sfumato is applied.

---

#### Knob 3 — Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Maps to `registers_in(2)`, the luminance-adaptive depth modulation amount. Darker pixels receive stronger blur when this control is raised, simulating atmospheric perspective. The formula is `1023 - (Y × depth / 1024)`, so at full depth a pixel at Y=0 (black) gets the maximum coefficient while Y=1023 (white) gets nearly zero. Toggle 8 selects between linear and quadratic depth curves — quadratic concentrates the effect more tightly into the deepest shadows.

---

#### Knob 4 — Chroma Diffusion
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 58.7% |
| Suffix | % |

Maps to `registers_in(3)`, extra chrominance diffusion. When Chroma Lock (Toggle 9) is disengaged, half of this value is added to the effective UV alpha, causing color boundaries to dissolve more than luminance edges. Setting this high while keeping Diffusion moderate creates an effect where forms maintain their tonal shape but colors bleed into one another — a watercolor-like dissolution of hue.

---

#### Knob 5 — Haze
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 19.6% |
| Suffix | % |

Maps to `registers_in(4)`, the atmospheric haze amount. Haze lifts shadow luminance by `haze / 2` counts and desaturates chrominance proportionally by multiplying the centred UV signal by `(1023 - haze) / 1024`. At subtle levels it adds a delicate silver-gray veil; at high levels the image washes out into near-uniform fog. Haze is applied after the IIR filter but before the varnish stage, so the warm tint (if active) is applied to the already-hazed signal.

---

#### Knob 6 — Warmth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Maps to `registers_in(5)`, the warm varnish color temperature shift amount. When the Varnish toggle (Toggle 10) is active, this value (right-shifted by 2) is subtracted from U and added to V, pushing the color balance toward amber. The right-shift limits the maximum shift to about 256 counts, preventing extreme color distortion. At subtle levels it produces the golden warmth of aged varnish on a Renaissance panel painting; at high levels the entire image takes on a deep amber tone.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Direction** | Uni | Bidi |
| **8 — Depth Mode** | Linear | Quad |
| **9 — Chroma Lock** | Indep | Lock |
| **10 — Varnish** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–10 control four independent modal options. Toggle 7 selects unidirectional or bidirectional IIR filtering. Toggle 8 chooses linear or quadratic depth modulation. Toggle 9 locks or unlocks chrominance diffusion from luminance. Toggle 10 enables the warm varnish color shift. Each toggle operates independently — all sixteen combinations are valid.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original delayed signal and the processed output. At 100% the full sfumato effect is applied. At 0% the original signal passes through. Intermediate values blend the two — useful for dialling in a subtle atmospheric enhancement without fully committing to the softened look.

---

## Guided Exercises

These exercises progress from basic edge-adaptive diffusion through depth modulation and atmospheric haze to the full Venetian varnish treatment.

### Exercise 1: Edge-Adaptive Softening

<img src={sfumato_exercise1_result} alt="Edge-Adaptive Softening result"/>
*Edge-Adaptive Softening — simulated result across source images.*
**Source**: Portrait footage or any source with a mix of sharp edges and smooth gradients — faces, still-life objects, or architectural details.

**Objective**: Learn how the base diffusion and edge threshold interact to create selective tonal smoothing.

1. Start with all pots at defaults and all toggles off (unidirectional, linear depth, independent chroma, no varnish).
2. Slowly raise Diffusion (Pot 1) from 0%. Watch as horizontal tonal edges soften while flat regions remain crisp.
3. Lower Edge Threshold (Pot 2) toward 20%. Now even gentle gradients trigger full diffusion — the entire image softens.
4. Raise Edge Threshold to 80%. Only the sharpest edges are smoothed; subtle gradients pass through untouched.
5. Toggle Direction (Switch 7) to Bidi. The rightward smear disappears and edges soften symmetrically.

**Key concepts**: Higher base alpha = more maximum blur; higher threshold = more selective (only strong edges); bidirectional evens out the directionality of unidirectional IIR

---

### Exercise 2: Atmospheric Perspective

<img src={sfumato_exercise2_result} alt="Atmospheric Perspective result"/>
*Atmospheric Perspective — simulated result across source images.*
**Source**: Landscape footage or any image with a bright foreground and dark background — a window looking out, a lit figure against shadows, or a sunset sky.

**Objective**: Use depth modulation and haze to simulate the effect of viewing a scene through atmosphere.

1. Use settings from Exercise 1 as a starting point, with Diffusion ~50% and Edge Threshold ~40%.
2. Raise Depth (Pot 3) to ~60%. Shadows soften dramatically while highlights remain crisp — the dark background dissolves.
3. Switch Depth Mode (Toggle 8) to Quad. The effect concentrates in the deepest shadows; mid-tones sharpen back up.
4. Add Haze (Pot 5) at ~30%. Shadows lift toward gray and colors desaturate slightly — a silvery atmospheric veil.
5. Toggle back to Linear depth and compare the more gradual falloff.

**Key concepts**: Darker pixels get more blur (atmospheric perspective simulation), quadratic depth steepens the shadow bias, haze lifts shadows and desaturates independently of the IIR filter

---

### Exercise 3: Venetian Varnish

<img src={sfumato_exercise3_result} alt="Venetian Varnish result"/>
*Venetian Varnish — simulated result across source images.*
**Source**: Portrait or still-life footage in warm lighting — ideal for simulating an Old Master painting.

**Objective**: Combine all four layers (diffusion, depth, haze, varnish) for a full Renaissance-painting treatment.

1. Set Diffusion ~60%, Edge Threshold ~50%, Depth ~40%.
2. Add Chroma Diffusion ~70% and unlock Chroma Lock (Switch 9 = Indep). Color boundaries dissolve more than luminance — a watercolor softness.
3. Add Haze ~20% for a delicate atmospheric lift.
4. Enable Varnish (Toggle 10) and raise Warmth (Pot 6) to ~50%. The output takes on a golden amber tone.
5. Lower Mix to ~70% to blend the varnished result with the original, retaining some of the source's crispness.
6. Toggle Direction to Bidi for symmetrical softening that better simulates the omni-directional diffusion of oil glazes.

**Key concepts**: Chroma diffusion + independent mode dissolves color beyond luminance, haze and varnish stack to create layered atmospheric effects, wet/dry mix controls the commitment level

---


## Tips

- **Edge Threshold is the selectivity control**: Low threshold = everything softens. High threshold = only the hardest tonal edges are treated. Start high and lower until you find the boundary between "selective sfumato" and "uniform blur."
- **Depth creates foreground/background separation**: Raising Depth makes shadows dissolve while highlights stay sharp. This is the core of atmospheric perspective — use it to push dark regions into the background.
- **Chroma Diffusion unlocked is the watercolor mode**: When Chroma Lock is set to Indep with high Chroma Diffusion, colors bleed beyond their luminance boundaries like wet pigment.
- **Haze and Varnish stack**: Haze lifts and desaturates; Varnish warms. Together they create the complete Old Master palette: soft edges, atmospheric lift, amber warmth.
- **Bidirectional mode costs one BRAM but eliminates directionality**: Uni mode is lighter on resources but produces a characteristic rightward smear. Switch to Bidi for symmetrical diffusion.
- **Mix for subtlety**: The full sfumato treatment can overwhelm detail. Blend at 60–80% to retain some of the source's crispness while still softening tonal boundaries.
- **IIR resets each line**: There is no vertical blurring — all diffusion is strictly horizontal. Pair Sfumato with a vertical blur program in the chain for omni-directional softening.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha** | The IIR filter coefficient (0–1023); higher alpha weights the previous output more heavily, creating stronger blur. |
| **Atmospheric Perspective** | The visual phenomenon where distant objects appear softer, lighter, and less colorful due to intervening atmosphere. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **Chrominance** | The color components (U, V) of a YUV signal. |
| **Depth Modulation** | Varying the blur strength based on pixel luminance to simulate distance-dependent softening. |
| **Edge-Adaptive** | A filtering strategy that changes its strength based on the local image gradient, preserving structure while smoothing transitions. |
| **Gradient** | The absolute difference between adjacent pixel luminance values, used to detect tonal edges. |
| **Haze** | A post-filter stage that lifts shadow luminance and desaturates chrominance, simulating atmospheric scattering. |
| **IIR** | Infinite Impulse Response; a recursive filter whose output depends on its own previous values. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived luminance. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **Sfumato** | Italian for "vanished like smoke"; Leonardo da Vinci's painting technique of eliminating visible tonal boundaries. |
| **Varnish** | A color temperature shift toward amber, simulating the aged appearance of oil painting varnish. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
