---
draft: true
sidebar_position: 50
slug: /instruments/videomancer/chromasia
title: "Chromasia"
image: /img/instruments/videomancer/chromasia/chromasia_hero_s1.png
description: "Every video effects box from the 1980s and 1990s shipped with a bank of colour transformations — negative, solarise, posterise, sepia — accessible by punching a number on a keypad or scrolling through a menu."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import chromasia_control_panel from '/img/instruments/videomancer/chromasia/chromasia_control_panel.png';
import chromasia_source1_dog from '/img/instruments/videomancer/chromasia/chromasia_source1_dog.png';
import chromasia_source2_field from '/img/instruments/videomancer/chromasia/chromasia_source2_field.png';
import chromasia_source3_elephant from '/img/instruments/videomancer/chromasia/chromasia_source3_elephant.png';
import chromasia_source4_pattern from '/img/instruments/videomancer/chromasia/chromasia_source4_pattern.png';
import chromasia_source5_man from '/img/instruments/videomancer/chromasia/chromasia_source5_man.png';
import chromasia_source6_berries from '/img/instruments/videomancer/chromasia/chromasia_source6_berries.png';
import chromasia_hero_s1 from '/img/instruments/videomancer/chromasia/chromasia_hero_s1.png';
import chromasia_hero_s2 from '/img/instruments/videomancer/chromasia/chromasia_hero_s2.png';
import chromasia_hero_s3 from '/img/instruments/videomancer/chromasia/chromasia_hero_s3.png';
import chromasia_hero_s4 from '/img/instruments/videomancer/chromasia/chromasia_hero_s4.png';
import chromasia_hero_s5 from '/img/instruments/videomancer/chromasia/chromasia_hero_s5.png';
import chromasia_hero_s6 from '/img/instruments/videomancer/chromasia/chromasia_hero_s6.png';
import chromasia_ex1_s1 from '/img/instruments/videomancer/chromasia/chromasia_ex1_s1.png';
import chromasia_ex1_s2 from '/img/instruments/videomancer/chromasia/chromasia_ex1_s2.png';
import chromasia_ex1_s3 from '/img/instruments/videomancer/chromasia/chromasia_ex1_s3.png';
import chromasia_ex1_s4 from '/img/instruments/videomancer/chromasia/chromasia_ex1_s4.png';
import chromasia_ex1_s5 from '/img/instruments/videomancer/chromasia/chromasia_ex1_s5.png';
import chromasia_ex1_s6 from '/img/instruments/videomancer/chromasia/chromasia_ex1_s6.png';
import chromasia_ex2_s1 from '/img/instruments/videomancer/chromasia/chromasia_ex2_s1.png';
import chromasia_ex2_s2 from '/img/instruments/videomancer/chromasia/chromasia_ex2_s2.png';
import chromasia_ex2_s3 from '/img/instruments/videomancer/chromasia/chromasia_ex2_s3.png';
import chromasia_ex2_s4 from '/img/instruments/videomancer/chromasia/chromasia_ex2_s4.png';
import chromasia_ex2_s5 from '/img/instruments/videomancer/chromasia/chromasia_ex2_s5.png';
import chromasia_ex2_s6 from '/img/instruments/videomancer/chromasia/chromasia_ex2_s6.png';
import chromasia_ex3_s1 from '/img/instruments/videomancer/chromasia/chromasia_ex3_s1.png';
import chromasia_ex3_s2 from '/img/instruments/videomancer/chromasia/chromasia_ex3_s2.png';
import chromasia_ex3_s3 from '/img/instruments/videomancer/chromasia/chromasia_ex3_s3.png';
import chromasia_ex3_s4 from '/img/instruments/videomancer/chromasia/chromasia_ex3_s4.png';
import chromasia_ex3_s5 from '/img/instruments/videomancer/chromasia/chromasia_ex3_s5.png';
import chromasia_ex3_s6 from '/img/instruments/videomancer/chromasia/chromasia_ex3_s6.png';

# Chromasia

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: chromasia_source1_dog, after: chromasia_hero_s1 },
    { label: "Field", before: chromasia_source2_field, after: chromasia_hero_s2 },
    { label: "Elephant", before: chromasia_source3_elephant, after: chromasia_hero_s3 },
    { label: "Pattern", before: chromasia_source4_pattern, after: chromasia_hero_s4 },
    { label: "Man", before: chromasia_source5_man, after: chromasia_hero_s5 },
    { label: "Berries", before: chromasia_source6_berries, after: chromasia_hero_s6 },
  ]}
/>
*Chromasia in Colorize mode painting a single cyan hue across a still life, with the wet/dry mix fader blending the tinted image against the original.*

---

## Overview

Every video effects box from the 1980s and 1990s shipped with a bank of colour transformations — negative, solarise, posterise, sepia — accessible by punching a number on a keypad or scrolling through a menu. The NewTek NewTek's ChromaFX bank was the archetype: a numbered list of colour mutations you could hot-switch during a live broadcast. Chromasia distils that tradition into an eight-mode colour effects processor on a single FPGA, addressed not by menu but by the binary state of three toggle switches.

The three mode-select toggles form a 3-bit address — 000 through 111 — mapping to Negative, Solarize, Posterize, Colorize, Sepia, Threshold, Color Swap, and Sketch. Each mode repurposes the six potentiometers in its own way: Intensity and Secondary serve as mode-dependent primary and secondary parameters, while Hue, Saturation, Edge Gain, and Brightness provide dedicated tonal shaping across every mode. The result is a Swiss-army-knife processor where a single toggle flip replaces one colour transformation with another, all in a unified eight-clock pipeline that uses zero BRAM and roughly 600 logic cells.

At conservative settings — a gentle solarise fold or a light sepia wash — Chromasia is a subtle colourist's tool. At extremes — hard binary threshold, aggressive posterisation, or full channel-swap routing — it becomes a graphic design weapon, transforming source video into stark, poster-art abstractions. The name fuses *chroma* (colour) with *fantasia* (imagination): a playground of chromatic reinvention.

---

## Quick Start

1. **Binary mode addressing**: Memorise the three-toggle patterns — 000 Negative, 001 Solarize, 010 Posterize, 011 Colorize, 100 Sepia, 101 Threshold, 110 Color Swap, 111 Sketch. Once internalised, switching modes becomes a physical gesture rather than a menu hunt.
2. **All Channels is the hidden dimension**: Negative, Solarize, and Posterize behave like entirely different effects depending on whether All Channels is set to Y Only or YUV. Explore both states for every mode.
3. **Mix fader as a colourist's tool**: Rather than using modes at full strength, blend them at 20–40% via the Mix fader. A subtle Sepia wash or a faint Solarize shimmer can add warmth or texture without overwhelming the source.

---

## Background

### Analog Video Effects Heritage

The earliest analog video effects processors were simple circuits: an inverting amplifier for negative, a level clamp for threshold, a gain stage for contrast. By the mid-1980s, products like the Fairlight and Videonics TitleMaker bundled dozens of such effects into a single rackmount box. The NewTek NewTek (1990) elevated the concept to a software-switchable bank of one hundred numbered colour effects. Chromasia inherits that philosophy — a curated palette of classic transformations, each a distinct flavour of colour alteration, switchable in real time.

### Solarization and the Sabattier Effect

Solarization — the partial reversal of tones in a photographic image — has roots in darkroom chemistry. The Sabattier effect, discovered in 1862, occurs when a partially developed print is briefly re-exposed to light, causing previously dark tones to lighten while light tones remain. The result is a V-shaped or folded transfer curve where pixel values above a threshold are reflected back toward zero. Chromasia's Solarize mode implements this fold digitally: pixels below the Intensity threshold pass unchanged, while pixels above are reflected around the threshold, creating the characteristic metallic, relief-like appearance. Man Ray and Lee Miller popularised the solarised look in fine art photography during the 1930s.

### Posterization and Quantization

When a continuous-tone image is reduced to a small number of discrete levels, smooth gradients collapse into flat bands separated by hard edges. This is posterization — named after the limited-palette screen-printing technique used to produce large-format posters. In the digital domain, posterization is a form of quantization: the 10-bit pixel values (1024 possible levels) are truncated to fewer bits by right-shifting and then left-shifting, discarding the lower bits. Chromasia's Posterize mode uses this bit-mask approach, with the Intensity knob selecting how many bits to discard. At full intensity a single bit remains — the image collapses to pure black and white with no intermediate tones.

### Edge Detection for Sketch Mode

Sketch mode turns video into a line drawing by detecting horizontal edges. The technique is simple: compare each pixel with its immediate horizontal neighbour (one pixel delay). The absolute difference between adjacent pixels is zero in uniform regions and large at transitions. Multiplying this difference by a gain factor and subtracting from white produces dark lines on a bright background — the visual language of a pencil sketch. This single-pixel horizontal differencing is the simplest possible edge detector, requiring no BRAM or multi-line buffers, yet produces surprisingly convincing line art from high-contrast source material.

### Sine LUT for Hue Rotation in Colorize Mode

Colorize mode replaces the original chroma information with a single hue defined by the Hue knob. The hue is encoded as an angle on the colour wheel, and the FPGA converts that angle to U and V offsets using a 64-entry quarter-wave sine/cosine look-up table. The Hue register's upper six bits index into the LUT, producing signed cosine and sine values that are multiplied by the Saturation parameter to yield the final U and V displacements from the neutral chroma midpoint (512). This approach — angle-to-chroma via trigonometric LUT — is the same technique used in broadcast colour-bar generators and analog vectorscope calibration circuits, here repurposed to paint an entire frame in a single chosen hue.


---

## Signal Flow

```
Input Video (YUV 4:4:4, 30-bit)
│
├─── Stage 1: Input Register ──────────────────────────────────
│    ├─ Latch Y, U, V
│    └─ Store previous Y pixel (for sketch edge detection)
│
├─── Stage 2: Eight Modes in Parallel ─────────────────────────
│    ├─ Mode 0 (000): Negative        — 1023 − channel
│    ├─ Mode 1 (001): Solarize        — V-fold at Intensity threshold
│    ├─ Mode 2 (010): Posterize       — bit-mask quantization
│    ├─ Mode 3 (011): Colorize        — LUT hue + saturation → U,V
│    ├─ Mode 4 (100): Sepia           — warm brown tint via Intensity
│    ├─ Mode 5 (101): Threshold       — binary black/white at Intensity
│    ├─ Mode 6 (110): Color Swap      — channel routing (8 sub-modes)
│    └─ Mode 7 (111): Sketch          — |Y − Y_prev| × Edge Gain
│
├─── Stage 3: Output Mode Mux ─────────────────────────────────
│    └─ 3-bit toggle select → one mode's Y,U,V to pipeline
│
├─── Stage 4: Composite Register ──────────────────────────────
│    └─ Latch selected mode output
│
├─── Stages 5–8: Interpolator (wet/dry mix) ───────────────────
│    └─ 4-clock crossfade between delayed original and processed
│
├─── Sync Delay ────────────────────────────────────────────────
│    └─ 8-clock delay matching pipeline depth (hsync, vsync, field)
│
└─── Output ────────────────────────────────────────────────────
     └─ Bypass mux: processed or delayed original
```

All eight modes are computed in parallel on every clock cycle. The 3-bit toggle state selects which mode's output propagates through the mux into the composite register. This means switching modes is instantaneous — there is no transition delay, no reconfiguration, and no dropped frames. The single-pixel delay register for sketch edge detection is the only state element beyond simple pipeline registers; all other modes are purely combinational functions of the input pixel and the parameter registers.

The All Channels toggle (Switch 10) is a cross-cutting concern that affects how several modes handle chroma. When set to Y Only, modes like Negative, Solarize, and Posterize process only the luminance channel, passing U and V through unchanged. When set to YUV, the same transformation is applied to all three channels, producing dramatically different colour results — a negative that inverts hue and saturation, a solarise that folds chroma as well as luma. Colorize, Sepia, Threshold, and Sketch always replace or neutralise chroma regardless of this toggle.

---

## Parameter Reference

<img src={chromasia_control_panel} alt="Videomancer front panel with Chromasia loaded"/>
*Videomancer's front panel with Chromasia active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Intensity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

The Intensity knob is the primary parameter for most modes. In Solarize, it sets the fold threshold — the luminance value at which the V-curve reflects. In Posterize, it selects the bit-depth reduction level (nine quantization steps from 2 colours to 512 colours). In Sepia, it controls the strength of the warm brown tint. In Threshold, it sets the black/white cutoff level. The dual nature of this control means that a single knob sweep produces a completely different animation depending on the active mode — a gentle fold in Solarize, a staircase collapse in Posterize, a tint deepening in Sepia.

---

#### Knob 2 — Secondary
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

The Secondary knob provides a second dimension of control where the mode requires it. In Color Swap mode, its upper three bits select among eight channel-routing permutations — U↔V swap, Y replacing U or V, cross-channel averages, and full monochrome routing. In other modes the Secondary knob is unused and can be left at any position without effect. This per-mode multiplexing keeps the panel uncluttered: rather than dedicating separate controls to each of eight modes, Chromasia reuses the same physical knobs with different mappings.

---

#### Knob 3 — Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

The Hue knob drives the sine/cosine LUT in Colorize mode. Sweeping it through its full range rotates the tint colour through 360 degrees of the YUV colour wheel — from red through yellow, green, cyan, blue, magenta, and back. The upper six bits of the 10-bit register index the 64-entry quarter-wave tables, so the resolution is approximately 5.6 degrees per step, yielding 64 distinct hue positions. Outside of Colorize mode, the Hue knob has no effect on the output.

---

#### Knob 4 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

The Saturation knob controls the amplitude of the chroma offset applied in Colorize mode. At minimum, the colourised frame is desaturated — luminance is preserved but all colour is removed, producing a monochrome output tinted by whatever tiny residual the LUT yields at low gain. At maximum, the tint is vivid and fully saturated. The multiplication of the LUT output by the Saturation register is a 10×10-bit product, truncated to 10 bits, ensuring the chroma offset scales cleanly from zero to full amplitude.

---

#### Knob 5 — Edge Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Edge Gain controls the sensitivity of the Sketch mode edge detector. After computing the absolute horizontal pixel difference, Chromasia multiplies the result by this gain value. Low gain produces faint, delicate lines — only the strongest edges in the source are visible. High gain amplifies even subtle gradients into bold, dark strokes. The product is clamped to 10 bits, so at very high gain, moderate edges saturate to full black, producing a coarser, more graphic line style.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

The Brightness knob is mapped to the `registers_in(5)` register and is available as a global parameter. In the current pipeline architecture, Brightness is routed to the register bus and available for future contrast/brightness post-processing expansion. Its presence on the panel maintains the classic video-processor control layout — Intensity, Secondary, Hue, Saturation, Edge Gain, Brightness — even when not all knobs are active in every mode.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode A** | Off | On |
| **8 — Mode B** | Off | On |
| **9 — Mode C** | Off | On |
| **10 — All Channels** | Y Only | YUV |
| **11 — Bypass** | Off | On |

Toggles 7, 8, and 9 (Mode A, Mode B, Mode C) form a 3-bit binary selector. Mode A is bit 0 (LSB), Mode B is bit 1, Mode C is bit 2 (MSB). The eight combinations map directly to the eight processing modes: 000 = Negative, 001 = Solarize, 010 = Posterize, 011 = Colorize, 100 = Sepia, 101 = Threshold, 110 = Color Swap, 111 = Sketch. This binary addressing scheme is a deliberate nod to the DIP-switch configurations of early digital video hardware, where modes were selected by hardware switches rather than menus. Flipping a single toggle jumps between two modes that differ by one bit — Negative (000) to Solarize (001), or Posterize (010) to Colorize (011) — encouraging exploratory performance.

Toggle 10 (All Channels) is an orthogonal modifier that does not change which mode is active, but changes *how deeply* that mode processes colour. When set to Y Only, chroma passes through untouched in Negative, Solarize, and Posterize modes. When set to YUV, the same transformation is applied to U and V as well, producing dramatically different results. Modes that inherently replace chroma (Colorize, Sepia, Threshold, Sketch) are unaffected by this toggle.

Toggle 11 (Bypass) routes the delayed original signal directly to the output, bypassing all processing and the wet/dry mix. Use it for instant A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

The Mix fader controls the wet/dry crossfade between the processed signal and the delayed original via a 4-clock interpolator. At 100% (fader fully up), the output is entirely the processed signal. At 0%, the output is entirely the original. Intermediate positions blend the two, which is particularly effective for subtle colour grading — a 30% mix of Sepia over the original adds warmth without obliterating the source colours. The crossfade operates on all three channels simultaneously.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from single-mode exploration to multi-mode comparison and creative blending. Each builds familiarity with a different subset of Chromasia's eight processing modes.

### Exercise 1: Solarize Sweep

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: chromasia_source1_dog, after: chromasia_ex1_s1 },
    { label: "Field", before: chromasia_source2_field, after: chromasia_ex1_s2 },
    { label: "Elephant", before: chromasia_source3_elephant, after: chromasia_ex1_s3 },
    { label: "Pattern", before: chromasia_source4_pattern, after: chromasia_ex1_s4 },
    { label: "Man", before: chromasia_source5_man, after: chromasia_ex1_s5 },
    { label: "Berries", before: chromasia_source6_berries, after: chromasia_ex1_s6 },
  ]}
/>
*Solarize Sweep — simulated result across source images.*
**Source**: Footage or stills with broad tonal range — landscapes, portraits, or gradient test patterns.

**What You'll Create**: Understand the solarize fold curve and the effect of the Intensity threshold on tonal reflection.

1. **Select Solarize**: Set Mode A On, Mode B Off, Mode C Off (toggle pattern 001).
2. **Threshold sweep**: Start with Intensity at 0%. Slowly increase — watch as highlights begin to fold back toward black. At 50%, the fold point is at mid-gray. At 100%, only the brightest pixels are reflected.
3. **All Channels**: Toggle All Channels to YUV. Observe how the fold now affects chroma as well — colour wraps in unexpected ways.
4. **Mix blend**: Lower the Mix fader to ~50% to blend the solarised result with the original, creating a subtle metallic sheen.
5. **Compare**: Flip Mode A off (000 = Negative) to compare solarization with simple inversion.

**Key concepts**: Solarization reflects values above a threshold, creating a V-shaped transfer curve. The Intensity knob sets the fold point. All Channels extends the fold to chroma.

---

### Exercise 2: Colorize a Monochrome Scene

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: chromasia_source1_dog, after: chromasia_ex2_s1 },
    { label: "Field", before: chromasia_source2_field, after: chromasia_ex2_s2 },
    { label: "Elephant", before: chromasia_source3_elephant, after: chromasia_ex2_s3 },
    { label: "Pattern", before: chromasia_source4_pattern, after: chromasia_ex2_s4 },
    { label: "Man", before: chromasia_source5_man, after: chromasia_ex2_s5 },
    { label: "Berries", before: chromasia_source6_berries, after: chromasia_ex2_s6 },
  ]}
/>
*Colorize a Monochrome Scene — simulated result across source images.*
**Source**: Black-and-white footage or a desaturated feed — old film clips, surveillance cameras, or any source with strong tonal contrast.

**What You'll Create**: Learn how the Hue and Saturation knobs paint a single tint across the luminance structure of the image.

1. **Select Colorize**: Set Mode A On, Mode B On, Mode C Off (toggle pattern 011).
2. **Full saturation**: Turn Saturation to maximum. The image is painted in a vivid single hue.
3. **Hue rotation**: Slowly sweep the Hue knob through its full range. Watch the colour cycle through the entire YUV wheel — from warm amber through green, cyan, violet, and back.
4. **Desaturate**: Bring Saturation back to ~30%. The tint becomes a subtle wash — the image is nearly monochrome with just a hint of colour.
5. **Sepia comparison**: Flip Mode C On (100 = Sepia). The warm brown tint is similar but fixed — there is no hue control. Compare the two approaches to colour tinting.

**Key concepts**: Colorize replaces chroma with a single hue defined by a sine/cosine LUT, scaled by Saturation. Sepia is a fixed warm-brown variant. The Hue knob provides full 360° control in Colorize mode.

---

### Exercise 3: Sketch to Threshold Composite

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: chromasia_source1_dog, after: chromasia_ex3_s1 },
    { label: "Field", before: chromasia_source2_field, after: chromasia_ex3_s2 },
    { label: "Elephant", before: chromasia_source3_elephant, after: chromasia_ex3_s3 },
    { label: "Pattern", before: chromasia_source4_pattern, after: chromasia_ex3_s4 },
    { label: "Man", before: chromasia_source5_man, after: chromasia_ex3_s5 },
    { label: "Berries", before: chromasia_source6_berries, after: chromasia_ex3_s6 },
  ]}
/>
*Sketch to Threshold Composite — simulated result across source images.*
**Source**: High-contrast footage with strong edges — architecture, typography, silhouettes, or hand-drawn graphics on camera.

**What You'll Create**: Combine Sketch edge detection with Threshold binary conversion to create bold graphic outputs.

1. **Select Sketch**: Set all three mode toggles On (111).
2. **Edge Gain sweep**: Start with Edge Gain at 0% — the output is nearly white. Slowly increase until strong edges appear as dark strokes on the bright background.
3. **Bold lines**: Set Edge Gain to ~70% for prominent edges.
4. **Switch to Threshold**: Flip Mode A Off (110 = Color Swap). Observe the channel routing. Now flip Mode B Off and Mode C On (100 = Sepia). Finally, set Mode A On, Mode C On (101 = Threshold).
5. **Threshold level**: Sweep Intensity to move the black/white cutoff. Notice the stark, graphic quality of the binary image.
6. **Mix**: Lower the Mix fader to ~40% to blend the threshold result with the original, creating a high-contrast overlay effect.

**Key concepts**: Sketch uses horizontal pixel differencing to extract edges. Threshold converts to binary black/white. Both destroy chroma information. The Mix fader can blend either back against the source for creative compositing.

---


## Tips

- **Color Swap sub-modes**: The Secondary knob in Color Swap mode (110) selects among eight different channel routings. Sweep it to discover unexpected false-colour palettes — some swap U and V, others replace chroma with luminance, creating monochrome variants.
- **Sketch plus feedback**: Route Chromasia's Sketch output back to its input through an external feedback path. The edge detector re-edges its own edges, creating increasingly abstract line patterns that evolve over time.
- **Sepia vs. Colorize**: Sepia is a convenience preset — a fixed warm brown tint scaled by Intensity. Colorize offers full hue control. If you want a custom-coloured tint (cyan, violet, gold), use Colorize mode and set the Hue knob to taste.
- **Threshold for keying**: The binary black/white output of Threshold mode is ideal as a key signal for downstream compositing. Feed a clean silhouette or high-contrast graphic to produce a hard matte.
- **Bypass for A/B**: Toggle Bypass (Switch 11) at any time to compare processed and original. The 8-clock delay is matched, so the transition is seamless — no timing shift when switching.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chroma** | The color information in a video signal, encoded as U and V components in the YUV color space, distinct from luminance. |
| **DIP switch** | Dual In-line Package switch; a miniature toggle switch array on a circuit board used for hardware configuration, referenced as inspiration for Chromasia's binary mode selection. |
| **Edge detection** | A signal processing technique that identifies boundaries between regions of different brightness by computing pixel-to-pixel differences. |
| **Luminance** | The brightness component (Y) of a video signal, independent of color information. |
| **LUT** | Look-Up Table; a pre-computed array mapping input values to output values, used here for sine/cosine hue conversion in Colorize mode. |
| **Posterization** | Reduction of a continuous-tone image to a limited number of discrete brightness levels, producing flat color bands separated by hard edges. |
| **Quantization** | The process of mapping a continuous range of values to a finite set of discrete levels, the mathematical basis of the Posterize mode. |
| **Sabattier effect** | A photographic darkroom technique where partial re-exposure during development causes tonal reversal, producing the characteristic solarized look. |
| **Solarization** | Partial inversion of tones in an image by reflecting values above a threshold, creating a V-shaped transfer curve and metallic appearance. |
| **Transfer curve** | A graph mapping input pixel values to output pixel values, defining how a processing stage remaps brightness or color. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
