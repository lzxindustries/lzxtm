---
draft: true
sidebar_position: 47
slug: /instruments/videomancer/chrome
title: "Chrome"
image: /img/instruments/videomancer/chrome/chrome_hero.png
description: "Program guide for Chrome, a Videomancer color program for the LZX video synthesizer."
---

import chrome_hero from '/img/instruments/videomancer/chrome/chrome_hero.png';
import chrome_before_after from '/img/instruments/videomancer/chrome/chrome_before_after.png';
import chrome_control_panel from '/img/instruments/videomancer/chrome/chrome_control_panel.png';
import chrome_exercise1_result from '/img/instruments/videomancer/chrome/chrome_exercise1_result.png';
import chrome_exercise2_result from '/img/instruments/videomancer/chrome/chrome_exercise2_result.png';
import chrome_exercise3_result from '/img/instruments/videomancer/chrome/chrome_exercise3_result.png';

# Chrome

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={chrome_hero} alt="Chrome hero image"/>
*Chrome transforming a still life into a liquid-metal relief, sigmoid luminance remapping compressing midtones into mirror-bright highlights and deep shadow pools while a faint gold tint warms the reflected surface.*
<img src={chrome_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Chrome applied.*

---

## Overview

There is a particular quality to chrome — the way it swallows the world around it and hands it back distorted, compressed, impossibly bright. Every highlight is a small sun; every shadow is an abyss. The midtones barely exist. Chrome is a program that chases that quality: it takes ordinary video and remaps its luminance through a sigmoid S-curve that stretches highlights and shadows apart while crushing everything in between. The result is a signal that behaves like a polished reflective surface — hard, glossy, and unforgiving.

The processing chain reinforces the metallurgical metaphor at every stage. After the S-curve compresses the tonal range, a desaturation stage drains colour toward monochrome — because real chrome reflects the world in silver, not in Technicolor. A spatial blur softens fine detail into the kind of broad, flowing gradients you see on the curved surface of a bumper or a trumpet bell. An additive bloom stage lifts the brightest regions into a white glow that spills across adjacent pixels, simulating the overexposure halation that cameras produce when pointed at specular highlights. Finally, a tint stage re-introduces colour — not the source colour, but a uniform metallic hue selected by the operator or by one of four preset metals: chrome silver, gold, copper, or steel blue.

At conservative settings — gentle curve, moderate desaturation, a whisper of bloom — Chrome is a subtle grading tool that gives footage a polished, editorial sheen. At extremes — hard sigmoid, full desaturation, heavy bloom, deep gold tint — it transforms any input into the liquid-metal title cards and chrome logos that defined the visual language of 1980s broadcast graphics. The name is literal: this program makes video look like chrome.

---

## Background

### Chrome and Metallic Surfaces in Video Art

The fascination with metallic surfaces in moving-image art predates digital video. Robert Rauschenberg's *Revolver* series (1967) used revolving plexiglass discs with silkscreened images, and his later collaborations with engineers explored reflective and transmissive surfaces as image carriers. By the 1980s, chrome had become the signature material of broadcast design — extruded chrome logos spinning against starfields were the universal language of network identity packages, from HBO's chrome cityscape to MTV's liquid-metal moon man. The aesthetic depended on a specific tonal signature: extreme contrast, compressed midtones, specular highlights blown to pure white, and shadows driven to black. Chrome replicates that tonal signature in real time, applied not to 3D-rendered geometry but to live video.

### Sigmoid and S-Curve Transfer Functions

The mathematical heart of Chrome is the sigmoid function — a smooth, S-shaped curve that maps input values to output values with steep transitions at the extremes and a compressed plateau in the middle. In photography, S-curves have been used since the earliest days of the Zone System to control tonal contrast: a gentle S-curve adds "punch" to flat scans; an aggressive one creates the hard, glossy look of fashion photography. The sigmoid is defined by its midpoint and its steepness. Chrome's S-curve LUT stores 1024 pre-computed entries in BRAM, mapping each possible 10-bit luminance value to its remapped output. The Curve knob controls the steepness: at 0%, the LUT is a straight diagonal (identity), and at 100%, the sigmoid approaches a step function where everything below mid-gray is driven to black and everything above is driven to white.

### Spatial Blur and Bloom in Compositing

In film compositing and visual effects, "bloom" refers to the optical phenomenon where bright regions of an image bleed light into adjacent areas. It occurs naturally in cameras with flared lenses or overexposed film, and it is deliberately added in post-production to simulate the look of intense specular highlights. The technique decomposes into two steps: threshold the image to isolate only the brightest pixels, then blur the thresholded result and add it back to the original. The blur spreads the bright regions outward; the addition lifts the surrounding pixels. Chrome implements both a general spatial blur (a box filter over a line buffer) and a bloom path (threshold → blur → additive combine). The Blur knob controls the general softening — how much fine detail is dissolved into the metallic surface — while the Bloom knob controls the intensity of the bright-pixel glow.

### Chroma Tinting for Metal Simulation

Real metals have characteristic colours. Silver and chrome are achromatic — they reflect the spectral content of the illuminant without tinting it. Gold shifts reflected light toward warm yellow (lower U, higher V in the YUV domain). Copper is warmer still, pushing toward red-orange. Steel introduces a cool blue bias. Chrome's tint stage adds signed offsets to the U and V chroma channels after the luminance processing is complete. The Tint U and Tint V knobs allow free-form colour placement anywhere on the UV plane, while the Metal and Preset toggles override the manual tint with four calibrated presets matching the spectral characteristics of these four metals. The combination of desaturation (removing original colour) and re-tinting (adding metallic colour) is the same workflow used in colour grading suites to create "bleach bypass" and "teal-and-orange" looks.

### Real-Time Reflective Surface Processing

Simulating reflective surfaces in real-time video is a problem that sits at the intersection of image processing and material science. Chrome's approach is deliberately approximate — it does not ray-trace reflections or model surface geometry. Instead, it exploits the fact that the human visual system interprets certain tonal and spatial cues as "metallic": extreme contrast, compressed midtones, spatial coherence (blur), specular bloom, and achromatic or single-hue colouring. By chaining these cues together in a single pipeline, Chrome creates a convincing metallic impression from any video source. The technique is related to the "matcap" (material capture) approach used in real-time 3D rendering, where a pre-photographed sphere of a material is used to shade arbitrary geometry — here, the "material" is applied not to geometry but to the luminance structure of the video signal itself.


---

## Signal Flow

```
Input Video (YUV 4:4:4, 30-bit)
│
├─── Stage 1: Input Register ──────────────────────────────────
│    └─ Latch Y, U, V, sync signals
│
├─── Stage 2: Luminance Invert (optional) ─────────────────────
│    └─ If Invert toggle On: Y ← 1023 − Y
│
├─── Stage 3: S-Curve LUT ─────────────────────────────────────
│    └─ 1024-entry BRAM sigmoid lookup, steepness set by Curve
│
├─── Stage 4: Desaturation ────────────────────────────────────
│    └─ U,V ← lerp(U,V → 512) by Desat amount
│
├─── Stage 5: Spatial Blur ────────────────────────────────────
│    └─ Box filter via line buffer BRAM, kernel width set by Blur
│
├─── Stage 6: Bloom ───────────────────────────────────────────
│    ├─ Threshold bright pixels (Y > ~768)
│    ├─ Blur thresholded result via line buffer BRAM
│    └─ Add blurred highlights back to main signal, scaled by Bloom
│
├─── Stage 7: Chroma Tint ────────────────────────────────────
│    ├─ If Metal/Preset active: override Tint U, Tint V with preset
│    └─ U ← U + (Tint_U − 512), V ← V + (Tint_V − 512)
│
├─── Stage 8: Smooth (optional) ──────────────────────────────
│    └─ Additional low-pass filter if Smooth toggle On
│
├─── Stages 9–12: Interpolator (wet/dry mix) ─────────────────
│    └─ 4-clock crossfade between delayed original and processed
│
├─── Sync Delay ───────────────────────────────────────────────
│    └─ Delay chain matching pipeline depth (hsync, vsync, field)
│
└─── Output ───────────────────────────────────────────────────
     └─ Bypass mux: processed or delayed original
```

The processing chain is strictly serial: every pixel passes through every stage in order, with the optional stages (Invert, Smooth) gated by their respective toggle switches. The S-curve LUT is the tonal engine — it defines the "chrome" character by compressing midtones and expanding the extremes. Everything downstream refines the illusion: desaturation removes the source's original colour identity, blur dissolves fine detail into flowing metallic gradients, bloom adds specular glow, and tint re-introduces colour in the narrow, uniform-hue palette that the eye reads as "metal." The Metal and Preset toggles interact as a 2-bit selector across four calibrated metal types, but they can be overridden at any time by manual Tint U/V adjustment.

---

## Parameter Reference

<img src={chrome_control_panel} alt="Videomancer front panel with Chrome loaded"/>
*Videomancer's front panel with Chrome active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

The Curve knob controls the steepness of the sigmoid S-curve stored in BRAM. At minimum, the LUT is a linear ramp — the identity function — and the luminance passes through unmodified. As you increase the knob, the sigmoid steepens: shadows are pushed darker, highlights are pushed brighter, and the midtone range compresses into a narrow band of rapid transition. At maximum, the curve approaches a hard step function and the image collapses into near-binary contrast — the extreme chrome look where almost every pixel is either mirror-bright or shadow-black. The sweet spot for liquid-chrome aesthetics is typically 60–80%, where the curve is steep enough to create the characteristic reflective contrast but soft enough to retain some midtone modelling.

---

#### Knob 2 — Desat
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

The Desat knob controls the desaturation amount — a linear interpolation between the original U and V chroma values and the neutral midpoint (512). At 0%, the source colour is fully preserved; the chrome effect is applied to luminance only, producing a high-contrast but still colourful image. At 100%, all chroma is removed and the image is pure monochrome before the tint stage. For convincing metallic looks, desaturation should be set high (75%+), because real polished metal surfaces reflect light without adding colour of their own. Partial desaturation (30–50%) creates an interesting hybrid where vestiges of the original colour bleed through the metallic sheen.

---

#### Knob 3 — Blur Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

The Blur knob controls the kernel width of the spatial box filter implemented via line buffer BRAM. At 0%, no blur is applied and fine detail is preserved — the chrome effect is crisp and hard-edged. As you increase the knob, the filter averages across a wider neighbourhood, dissolving texture and fine detail into smooth gradients. This is the control that transforms a high-contrast image into a *surface* — the softened luminance gradients read as reflections flowing across a curved metallic body rather than as a flat contrasty photograph. Heavy blur (70%+) combined with strong S-curve creates the liquid-mercury look; light blur (10–30%) retains enough detail for a brushed-metal or satin-finish appearance.

---

#### Knob 4 — Bloom
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

The Bloom knob scales the intensity of the additive highlight glow. The bloom path thresholds the luminance to isolate bright pixels, blurs the result through a second line buffer, and adds the blurred highlights back to the main signal. At 0%, no bloom — highlights remain sharp and contained. As you increase the knob, bright regions begin to glow, spilling light into neighboring pixels. At high values, the bloom dominates and the image acquires the dreamy, overexposed quality of a camera pointed at specular chrome. Bloom interacts strongly with the S-curve: a steeper curve pushes more pixels above the bloom threshold, so increasing Curve also increases the visible bloom even if the Bloom knob is unchanged.

---

#### Knob 5 — Reflect
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

The Tint U knob adds a signed offset to the U chroma channel after all luminance processing is complete. At the centre position (512), no tint is applied. Below 512, U shifts negative (toward blue-cyan); above 512, U shifts positive (toward red-yellow). This control is overridden when the Metal or Preset toggles select a calibrated preset, but returns to manual operation when the toggles are in a state that does not define a preset value for U. Combined with Tint V, this provides full free-form placement of the metallic hue anywhere on the UV colour plane.

---

#### Knob 6 — Tint Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

The Tint V knob adds a signed offset to the V chroma channel. At centre (512), no tint. Below 512, V shifts negative (toward green); above 512, V shifts positive (toward magenta-red). For gold, you want low U and high V (warm yellow). For copper, push V even higher and U slightly lower (warm red-orange). For steel blue, raise U and lower V (cool blue). The Metal and Preset toggles provide calibrated starting points for each of these metals, but the Tint U/V knobs allow infinite fine-tuning — or completely novel metallic colours that don't correspond to any real-world alloy.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Metal** | Chrome | Gold |
| **8 — Curve** | S-Curve | Hard |
| **9 — Tint** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 (Metal, Preset) form a 2-bit selector across four metallic tint presets. Metal selects between cool and warm base tones; Preset selects between two variants within each temperature. The four combinations are: Metal=Chrome + Preset=Copper → Chrome silver (U=512, V=512, neutral); Metal=Chrome + Preset=Steel → Steel blue (U≈540, V≈480, cool); Metal=Gold + Preset=Copper → Copper (U≈440, V≈580, warm orange); Metal=Gold + Preset=Steel → Gold (U≈460, V≈560, warm yellow). The presets override the manual Tint U/V knob positions, providing instant recall of calibrated metal colours. The manual knobs can still be used as a starting point if you disengage the presets by experiment.

Toggle 9 (Smooth) adds a secondary low-pass filter after the main processing chain, further softening the output. This is useful when the S-curve has introduced harsh tonal transitions that the primary Blur stage didn't fully dissolve. Toggle 10 (Invert) flips the luminance before the S-curve, producing a negative-chrome look where shadows become highlights and vice versa — the metallic aesthetic is preserved but the tonal polarity is reversed, creating dark chrome or shadow-metal effects. Toggle 11 (Bypass) routes the delayed original signal directly to the output, bypassing all processing and the wet/dry mix.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

The Mix fader controls the wet/dry crossfade via a 4-clock interpolator. At 100% (fader fully up), the output is entirely the processed chrome signal. At 0%, the output is the unprocessed original. Intermediate positions blend the two, which is particularly effective for subtle metallic grading — a 20–30% mix of chrome over the original adds a high-gloss editorial sheen without obliterating the source detail. The crossfade operates on all three channels simultaneously, so the desaturation and tint effects are also blended proportionally.

---

## Guided Exercises

These exercises progress from basic S-curve contrast shaping to full liquid-chrome transformations with metallic tinting. Each builds familiarity with a different stage of the processing chain and how the stages compound into the final metallic impression.

### Exercise 1: Sculpting the S-Curve

<img src={chrome_exercise1_result} alt="Sculpting the S-Curve result"/>
*Sculpting the S-Curve — simulated result across source images.*
**Source**: Footage or stills with a wide tonal range — landscapes, portraits, or gradient test patterns.

**Objective**: Understand how the sigmoid S-curve remaps luminance to create the fundamental chrome contrast signature.

1. **Isolate the curve**: Set Desat, Blur, Bloom, and Tint U/V to neutral (50% / centre). Set Metal to Chrome, Preset to Copper (neutral silver). Smooth and Invert off.
2. **Identity baseline**: Set Curve to 0%. The output matches the input — the LUT is a straight ramp.
3. **Gentle enhancement**: Increase Curve to ~30%. Highlights brighten, shadows deepen, but midtones remain. This is a classic contrast boost.
4. **Chrome territory**: Push Curve to ~70%. Midtones compress dramatically — the image begins to look glossy and hard, with distinct highlight and shadow separation.
5. **Hard step**: Push Curve to 100%. The image approaches binary contrast — almost everything is either white or black. This is the extreme chrome look.
6. **Mix it back**: Lower the Mix fader to ~60% to blend the hard curve with the original, creating a punchy but recoverable contrast.

**Key concepts**: The sigmoid S-curve is the tonal foundation of the chrome effect. Steeper curves = more metallic contrast. The Mix fader recovers midtone detail by blending with the original.

---

### Exercise 2: Gold Plate and Bloom

<img src={chrome_exercise2_result} alt="Gold Plate and Bloom result"/>
*Gold Plate and Bloom — simulated result across source images.*
**Source**: Close-up footage of objects with specular highlights — glass, water, metallic surfaces, or well-lit portraits.

**Objective**: Combine desaturation, gold tinting, and bloom to create a convincing liquid-gold surface treatment.

1. **Chrome base**: Set Curve ~65%, Desat ~85%, Blur ~25%. The image should look like polished silver — high contrast, mostly monochrome, slightly soft.
2. **Gold tint**: Set Metal to Gold, Preset to Steel. The output shifts to a warm yellow-gold. Compare with Preset=Copper for a warmer orange-gold.
3. **Add bloom**: Increase Bloom from 0% to ~50%. Watch specular highlights begin to glow and spill outward. The bloom adds the "liquid" quality — highlights feel like they're overflowing.
4. **Bloom interaction**: Now increase Curve slightly. Notice how a steeper curve pushes more pixels above the bloom threshold, increasing the glow even without touching the Bloom knob.
5. **Smooth finish**: Toggle Smooth on. The hard sigmoid transitions soften into flowing curves — the difference between hammered gold and liquid gold.

**Key concepts**: Desaturation removes source colour so the tint defines the metal. Bloom creates specular glow. The S-curve and bloom interact — steeper curves increase visible bloom. Smooth softens hard tonal edges.

---

### Exercise 3: Dark Chrome and Mixed Metals

<img src={chrome_exercise3_result} alt="Dark Chrome and Mixed Metals result"/>
*Dark Chrome and Mixed Metals — simulated result across source images.*
**Source**: High-contrast footage with strong silhouettes — architecture against sky, backlit figures, or stark graphic patterns.

**Objective**: Use the Invert toggle and manual tinting to create negative-chrome and custom metallic colour effects.

1. **Standard chrome**: Set Curve ~70%, Desat ~90%, Blur ~20%, Bloom ~30%. Metal=Chrome, Preset=Copper (neutral silver). Confirm a solid chrome look.
2. **Invert for dark chrome**: Toggle Invert on. The tonal polarity reverses — dark areas become bright chrome, bright areas become shadow. The metallic character is preserved but the mood changes completely.
3. **Steel blue**: With Invert still on, switch Metal to Chrome, Preset to Steel. The dark-chrome look acquires a cool blue tint — like brushed stainless steel in shadow.
4. **Custom alloy**: Disable both Metal/Preset presets by setting Metal=Chrome, Preset=Copper (neutral), then manually adjust Tint U and Tint V to create a custom metallic colour — try pushing Tint V high and Tint U low for a magenta-bronze.
5. **Blend**: Lower Mix to ~40% to let the original source texture show through the metallic overlay.

**Key concepts**: Invert reverses tonal polarity before the S-curve, creating dark-chrome/black-mirror effects. Manual Tint U/V allows custom metallic colours beyond the four presets. Low Mix values create metallic overlays rather than full replacements.

---


## Tips

- **Start with the curve**: The S-curve is the foundation of every chrome look. Dial it in first, then add desaturation, blur, bloom, and tint as refinements. A good curve makes the rest of the chain sing.
- **Desaturation before tinting**: For convincing metallics, desaturate heavily (80%+) before applying tint. Residual source colour fights with the metallic hue and breaks the illusion.
- **Bloom follows Curve**: The bloom intensity is coupled to the S-curve steepness because a steeper curve pushes more pixels above the bloom threshold. Use them as a pair — if you want more bloom, sometimes increasing Curve is more natural than increasing Bloom directly.
- **Smooth for liquid, off for brushed**: The Smooth toggle is the difference between liquid mercury and brushed aluminium. Engage it for flowing, organic chrome; leave it off for harder, more industrial textures.
- **Invert for dark chrome**: The Invert toggle before the S-curve creates an entirely different mood — dark regions become mirror-bright, producing black-mirror and shadow-chrome effects that pair well with Steel or custom cool tints.
- **Custom metals via Tint U/V**: The four Metal/Preset combinations cover the most common metals, but the Tint U and Tint V knobs unlock any colour on the UV plane. Try turquoise chrome (high U, low V) or rose gold (moderate U decrease, high V) for metallic colours that don't exist in nature.
- **Mix as a grading tool**: Rather than committing to full chrome at 100% Mix, blend at 20–40% to add a metallic sheen to the original footage. This is the editorial-chrome look — polished and glossy without losing the source entirely.
- **Feedback loops**: Route Chrome's output back to its input through an external feedback path. The S-curve re-applies to the already-curved signal, compounding the contrast until the image is pure black-and-white metallic relief — endlessly polished.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bloom** | An optical phenomenon where bright regions of an image bleed light into adjacent pixels, simulating camera halation from specular highlights. |
| **Box filter** | A spatial averaging filter that replaces each pixel with the mean of its neighbors within a rectangular kernel, used for Chrome's blur stage. |
| **BRAM** | Block RAM; dedicated memory blocks within an FPGA used for look-up tables, line buffers, and data storage. |
| **Desaturation** | Reduction of color intensity by interpolating chroma values toward the neutral midpoint, removing the source's original color identity. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that implements the video processing pipeline in hardware. |
| **Halation** | The spreading of light beyond its proper boundary in a camera or film, producing a soft glow around bright highlights. |
| **Interpolator** | A hardware module that performs linear blending between two signals, used for wet/dry mix crossfading. |
| **LUT** | Look-Up Table; a pre-computed array stored in BRAM that maps each 10-bit input luminance value to its sigmoid-remapped output. |
| **Matcap** | Material capture; a real-time rendering technique that applies a pre-photographed material appearance to arbitrary geometry, conceptually related to Chrome's approach of applying metallic tonal characteristics to video. |
| **Sigmoid** | An S-shaped mathematical curve that maps input values through steep transitions at the extremes and a compressed plateau in the middle, the core transfer function of the chrome effect. |
| **Specular highlight** | A bright, mirror-like reflection from a smooth surface, the dominant visual cue that Chrome's pipeline reproduces. |
| **UV plane** | The two-dimensional chroma space defined by the U and V components of the YUV color model, where hue and saturation are represented as angular position and radial distance. |
| **YUV** | A color space that separates luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |

---
