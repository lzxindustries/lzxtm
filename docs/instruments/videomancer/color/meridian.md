---
draft: true
sidebar_position: 191
slug: /instruments/videomancer/meridian
title: "Meridian"
image: /img/instruments/videomancer/meridian/meridian_hero_s1.png
description: "Meridian is a per-channel colour processor that applies independent gain, offset, and wavefold operations to the Y, U, and V channels of the input video."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import meridian_control_panel from '/img/instruments/videomancer/meridian/meridian_control_panel.png';
import meridian_source1_ballerina from '/img/instruments/videomancer/meridian/meridian_source1_ballerina.png';
import meridian_source2_fruit from '/img/instruments/videomancer/meridian/meridian_source2_fruit.png';
import meridian_source3_turtle from '/img/instruments/videomancer/meridian/meridian_source3_turtle.png';
import meridian_source4_pattern from '/img/instruments/videomancer/meridian/meridian_source4_pattern.png';
import meridian_source5_girl from '/img/instruments/videomancer/meridian/meridian_source5_girl.png';
import meridian_source6_berries from '/img/instruments/videomancer/meridian/meridian_source6_berries.png';
import meridian_hero_s1 from '/img/instruments/videomancer/meridian/meridian_hero_s1.png';
import meridian_hero_s2 from '/img/instruments/videomancer/meridian/meridian_hero_s2.png';
import meridian_hero_s3 from '/img/instruments/videomancer/meridian/meridian_hero_s3.png';
import meridian_hero_s4 from '/img/instruments/videomancer/meridian/meridian_hero_s4.png';
import meridian_hero_s5 from '/img/instruments/videomancer/meridian/meridian_hero_s5.png';
import meridian_hero_s6 from '/img/instruments/videomancer/meridian/meridian_hero_s6.png';
import meridian_ex1_s1 from '/img/instruments/videomancer/meridian/meridian_ex1_s1.png';
import meridian_ex1_s2 from '/img/instruments/videomancer/meridian/meridian_ex1_s2.png';
import meridian_ex1_s3 from '/img/instruments/videomancer/meridian/meridian_ex1_s3.png';
import meridian_ex1_s4 from '/img/instruments/videomancer/meridian/meridian_ex1_s4.png';
import meridian_ex1_s5 from '/img/instruments/videomancer/meridian/meridian_ex1_s5.png';
import meridian_ex1_s6 from '/img/instruments/videomancer/meridian/meridian_ex1_s6.png';
import meridian_ex2_s1 from '/img/instruments/videomancer/meridian/meridian_ex2_s1.png';
import meridian_ex2_s2 from '/img/instruments/videomancer/meridian/meridian_ex2_s2.png';
import meridian_ex2_s3 from '/img/instruments/videomancer/meridian/meridian_ex2_s3.png';
import meridian_ex2_s4 from '/img/instruments/videomancer/meridian/meridian_ex2_s4.png';
import meridian_ex2_s5 from '/img/instruments/videomancer/meridian/meridian_ex2_s5.png';
import meridian_ex2_s6 from '/img/instruments/videomancer/meridian/meridian_ex2_s6.png';
import meridian_ex3_s1 from '/img/instruments/videomancer/meridian/meridian_ex3_s1.png';
import meridian_ex3_s2 from '/img/instruments/videomancer/meridian/meridian_ex3_s2.png';
import meridian_ex3_s3 from '/img/instruments/videomancer/meridian/meridian_ex3_s3.png';
import meridian_ex3_s4 from '/img/instruments/videomancer/meridian/meridian_ex3_s4.png';
import meridian_ex3_s5 from '/img/instruments/videomancer/meridian/meridian_ex3_s5.png';
import meridian_ex3_s6 from '/img/instruments/videomancer/meridian/meridian_ex3_s6.png';

# Meridian

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: meridian_source1_ballerina, after: meridian_hero_s1 },
    { label: "Fruit", before: meridian_source2_fruit, after: meridian_hero_s2 },
    { label: "Turtle", before: meridian_source3_turtle, after: meridian_hero_s3 },
    { label: "Pattern", before: meridian_source4_pattern, after: meridian_hero_s4 },
    { label: "Girl", before: meridian_source5_girl, after: meridian_hero_s5 },
    { label: "Berries", before: meridian_source6_berries, after: meridian_hero_s6 },
  ]}
/>
*A saturated colour field folds back on itself in mirrored symmetry, each channel's frequency doubled into harmonic overtones that solarize the image into stained glass.*

---

## Overview

Meridian is a per-channel colour processor that applies independent gain, offset, and wavefold operations to the Y, U, and V channels of the input video. The name evokes lines of longitude — the meridians that divide the globe into sectors — because the program divides the colour space into independent parallel processing lanes, each with its own contrast, brightness, and fold controls.

The processing chain follows a classic signal-conditioning architecture: first a proc_amp stage scales and shifts each channel (contrast × input + brightness), then an optional frequency doubler folds the signal at its midpoint, creating a triangle-wave transfer function that mirrors values above 512 back down. This fold effectively doubles the spatial frequency of ramp-like patterns in the image — smooth gradients become V-shaped symmetrical waves, and tonal curves develop harmonic overtones. The result ranges from subtle colour correction (with folds bypassed) to aggressive solarization effects (with high gain and active folds) that recall the Sabattier effect in darkroom photography.

The panel labels are severely mismatched with the VHDL implementation. Pots 1–3 are labelled "Fold" but actually control contrast (proc_amp gain). Pots 4–6 are labelled "Gain" but actually control brightness (proc_amp offset). Toggle 10 is labelled "Link UV" but actually controls luma inversion. Understanding these mismatches is essential for achieving the intended results.

---

## Background

### The Sabattier Effect and Solarization

In traditional photography, solarization (more precisely, the Sabattier effect) occurs when a partially developed print is briefly re-exposed to light during development. The already-developed dark areas resist further development, while the lighter areas darken — causing a partial tonal inversion with characteristic bright edge lines (Mackie lines) where light and dark regions meet. The visual effect is a folded tonal curve: highlights and shadows both push toward a common middle value, while mid-tones swing to extremes. Meridian's frequency doubler produces a mathematically precise version of this effect — values below midpoint scale upward, values above midpoint are reflected downward — creating the same kind of harmonic doubling and tonal mirroring that Sabattier achieved chemically.

### Proc Amp Architecture

The processing amplifier (proc amp) is one of the most fundamental circuits in video engineering. It adjusts two parameters: **contrast** (gain) and **brightness** (offset). In Meridian's VHDL implementation, the proc_amp_u module computes: $(input - 512) \times contrast / 512 + brightness$. The input is first centred around the midpoint (512 in 10-bit), then scaled by the contrast control (0 = zero gain, 512 = unity, 1023 = approximately 2× gain), then offset by brightness (512 = no shift, below = darker, above = brighter). This architecture ensures that contrast adjustments expand or compress the signal symmetrically around the midpoint, rather than simply scaling from zero.

### Triangle-Wave Frequency Doubling

The frequency doubler implements a simple but powerful nonlinear transfer function: values below the midpoint are scaled up by 2×, and values above the midpoint are mirrored and scaled by 2×. Algebraically: $f(x) = 2x$ for $x < 512$, and $f(x) = 2 \times (1023 - x)$ for $x \geq 512$. The result is a triangle wave that passes through zero at both ends and peaks at the midpoint. Applied to a linear ramp, this doubles the spatial frequency — a single ramp becomes a V-shape. Applied to a photographic image, it creates the solarization effect: highlights fold back down, shadows push up, and the overall tonal range compresses while developing harmonic complexity.

### Per-Channel Colour Sculpting

By providing independent proc_amp and fold controls for each of the three YUV channels, Meridian enables what might be called colour sculpting — the ability to reshape each channel's tonal response independently. Folding the Y (luma) channel creates brightness solarization; folding U or V creates chrominance solarization, where hues shift and wrap in ways that have no natural photographic analog. The interaction between channels is what produces the stained-glass-like colour effects: when Y, U, and V are all folded with different gain and offset settings, the resulting colour combinations traverse paths through the YUV colour space that would be impossible to achieve with simple gain, saturation, or hue controls.

### Luma Inversion

The luma inversion stage (mislabelled "Link UV" on the panel) performs a bitwise NOT on the Y channel before all other processing — flipping 0 to 1023, 256 to 767, 512 to 511, and so on. This inverts the brightness of the image at the very start of the pipeline. When combined with the proc_amp and fold stages, luma inversion creates a different family of solarization effects: the fold now operates on the inverted tonal range, producing complementary harmonic patterns. Because only Y is inverted (not U or V), the colour relationships shift — dark areas that were warm become bright and cool, and vice versa.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Clock 0: Luma Inversion ────────────────────────────────────
│   ├─ If s_luma_invert: Y = NOT(Y_in)
│   └─ U, V pass through unchanged
│
├── Clocks 1–9: Proc Amp (×3 parallel) ────────────────────────
│   ├─ Y: proc_amp_u(Y, s_y_contrast, s_y_brightness)
│   ├─ U: proc_amp_u(U, s_u_contrast, s_u_brightness)
│   └─ V: proc_amp_u(V, s_v_contrast, s_v_brightness)
│   │   Each: (input − 512) × contrast / 512 + brightness
│   │   9 clocks: 1 center + 8 multiply+add
│
├── Clocks 10–11: Frequency Doubler (×3 parallel) ─────────────
│   ├─ Y: fold or bypass (s_y_fold_bypass)
│   ├─ U: fold or bypass (s_u_fold_bypass)
│   └─ V: fold or bypass (s_v_fold_bypass)
│   │   Fold: x<512 → 2x, x≥512 → 2×(1023−x)
│   │   2 clocks: 1 input register + 1 compute
│
├── Clocks 12–15: Interpolator (×3 parallel) ──────────────────
│   ├─ Y: lerp(dry_Y, wet_Y, mix_amount)
│   ├─ U: lerp(dry_U, wet_U, mix_amount)
│   └─ V: lerp(dry_V, wet_V, mix_amount)
│   │   4 clocks per channel
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 16-stage delay pipeline (hsync, vsync, field, Y, U, V)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select delayed original or processed signal
```

The pipeline's key architectural feature is the three-way parallelism: proc_amp, frequency doubler, and interpolator all run independently for Y, U, and V channels. The total latency is 16 clocks (1 inversion + 9 proc_amp + 2 frequency doubler + 4 interpolator), and the sync delay pipeline matches this exactly to keep the bypass path time-aligned with the processed path.

The proc_amp stage uses a signed multiplier internally (multiplier_s), which is the most resource-expensive component. The frequency doubler is pure combinatorial logic — a single conditional that either doubles the value or mirrors it around the midpoint. The interpolator provides the wet/dry crossfade, blending between the delayed original (dry) and the fully processed signal (wet) based on the Mix fader. Note that the dry path for the interpolator comes from the sync delay pipeline (the original input delayed by 16 clocks), not from any intermediate processing stage.

---

## Parameter Reference

<img src={meridian_control_panel} alt="Videomancer front panel with Meridian loaded"/>
*Videomancer's front panel with Meridian active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Fold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the Y channel contrast despite being labelled "Y Fold" on the panel. In the VHDL, this register is mapped to `s_y_contrast`, which feeds the contrast port of the Y proc_amp. At 0%, contrast is zero — the Y channel is crushed to the brightness offset value regardless of input. At ~50% (register 512), contrast is approximately unity — the Y channel passes through with its original dynamic range. At 100%, contrast is roughly 2× — the Y channel's deviation from the midpoint is doubled, dramatically expanding highlights and crushing shadows. This control is the primary tool for adjusting the luminance response before the fold stage, and it interacts powerfully with the fold: high contrast pushes more of the signal above the fold midpoint, increasing the proportion of folded pixels.

---

#### Knob 2 — U Fold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the U channel contrast despite being labelled "U Fold" on the panel. Operates identically to the Y contrast control but acts on the blue-difference chrominance channel. At unity (~50%), U chrominance maintains its original saturation. Below unity, blue-yellow colour differences compress toward neutral. Above unity, they expand — blues become more intensely blue, yellows more intensely yellow. When the U fold is active (Toggle 8), this contrast scaling determines how much of the U signal exceeds the midpoint and gets folded back, directly controlling the intensity of chrominance solarization in the blue-yellow axis.

---

#### Knob 3 — V Fold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the V channel contrast despite being labelled "V Fold" on the panel. Operates on the red-difference chrominance channel. The interaction between U and V contrast controls determines the overall hue shift character of the solarization: boosting V contrast while keeping U at unity shifts the solarization axis toward red-cyan, while the reverse shifts it toward blue-yellow. Setting both to high values produces complex colour rotations as the fold creates harmonic interactions between the two chrominance axes.

---

#### Knob 4 — Y Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the Y channel brightness despite being labelled "Y Gain" on the panel. In the VHDL, this register is mapped to `s_y_brightness`, which feeds the brightness port of the Y proc_amp. At ~50% (register 512), no brightness offset is applied. Below 50%, the entire luminance range shifts darker — useful for sinking shadows to black after contrast expansion. Above 50%, the range shifts brighter — useful for lifting the image when contrast has crushed the mid-tones. This offset is applied after the contrast multiplication, so it shifts the entire scaled signal uniformly. The interaction with the fold is significant: brightness shifts the signal up or down relative to the fold midpoint, changing which pixels cross the 512 threshold and get folded.

---

#### Knob 5 — U Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the U channel brightness despite being labelled "U Gain" on the panel. Adds a DC offset to the blue-difference chrominance after contrast scaling. At ~50%, no shift. Below 50%, the U channel shifts toward yellow; above 50%, toward blue. This allows precise colour temperature adjustment before the fold — warming or cooling the image in the blue-yellow axis. When the fold is active, this offset determines the starting position of the chrominance signal relative to the fold midpoint, which can dramatically change which hues survive the fold and which get reflected.

---

#### Knob 6 — V Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the V channel brightness despite being labelled "V Gain" on the panel. Adds a DC offset to the red-difference chrominance after contrast scaling. At ~50%, no shift. Below 50%, the V channel shifts toward cyan; above 50%, toward red/magenta. Combined with U brightness, this provides full two-axis control over the chrominance offset. Setting both U and V brightness to off-center values creates a global colour cast that is then processed through the fold — producing solarization effects with a specific colour character.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Y Folds** | 1x | 2x |
| **8 — U Folds** | 1x | 2x |
| **9 — V Folds** | 1x | 2x |
| **10 — Link UV** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–9 independently bypass the frequency doubler for each channel, providing eight combinations of fold on/off across Y, U, and V. This enables targeted solarization: folding only luma (Y fold on, U/V off) produces a brightness solarization with normal colour; folding only chroma (Y off, U/V on) preserves brightness but creates exotic hue shifts; folding all three channels produces the most extreme effect. Toggle 10 is labelled "Link UV" but actually controls luma inversion — a completely different function that flips Y before all processing. Toggle 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix at the end of the processing chain. At 100%, the output is the fully processed signal (proc_amp + fold). At 0%, the output is the unprocessed input. The interpolator operates on all three channels in parallel using 4-clock pipelines. The dry reference for the mix is the original input delayed by 16 clocks to match the processing latency — so the mix blends between the delayed original and the processed version at the same temporal position. This control is essential for dialing in subtle fold effects: at 30–50%, the solarization becomes a translucent colour overlay rather than a total replacement of the image's tonal structure.

---

## Guided Exercises

These exercises progress from basic colour correction through targeted channel folding to full solarization with luma inversion. Each reveals how Meridian's mismatched panel labels map to the actual signal processing chain.

### Exercise 1: Per-Channel Contrast and Brightness

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: meridian_source1_ballerina, after: meridian_ex1_s1 },
    { label: "Fruit", before: meridian_source2_fruit, after: meridian_ex1_s2 },
    { label: "Turtle", before: meridian_source3_turtle, after: meridian_ex1_s3 },
    { label: "Pattern", before: meridian_source4_pattern, after: meridian_ex1_s4 },
    { label: "Girl", before: meridian_source5_girl, after: meridian_ex1_s5 },
    { label: "Berries", before: meridian_source6_berries, after: meridian_ex1_s6 },
  ]}
/>
*Per-Channel Contrast and Brightness — simulated result across source images.*
**Source**: Colourful, high-saturation footage — flowers, painted surfaces, or colour bars.

**Objective**: Understand that "Y Fold" / "U Fold" / "V Fold" actually control contrast, and "Y Gain" / "U Gain" / "V Gain" actually control brightness, by adjusting each channel independently with folds bypassed.

1. **Bypass all folds**: Set Y Folds, U Folds, and V Folds to 2x (bypass position). This leaves only the proc_amp stages active.
2. **Unity settings**: Set all six pots to ~50%. The image passes through unchanged.
3. **Y contrast**: Sweep Y Fold (pot 1) from 0% to 100%. Despite the label, the image contrast changes — at 0% the image goes flat grey, at 100% it becomes high contrast.
4. **Y brightness**: Sweep Y Gain (pot 4) from 0% to 100%. Despite the label, the image gets darker (below 50%) or brighter (above 50%).
5. **U contrast**: Sweep U Fold (pot 2). Blue/yellow saturation changes.
6. **V contrast**: Sweep V Fold (pot 3). Red/cyan saturation changes.

**Key concepts**: Pots 1–3 are contrast (proc_amp gain) despite "Fold" labels, Pots 4–6 are brightness (proc_amp offset) despite "Gain" labels, with folds bypassed Meridian is a pure proc_amp colour corrector

---

### Exercise 2: Luma Solarization

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: meridian_source1_ballerina, after: meridian_ex2_s1 },
    { label: "Fruit", before: meridian_source2_fruit, after: meridian_ex2_s2 },
    { label: "Turtle", before: meridian_source3_turtle, after: meridian_ex2_s3 },
    { label: "Pattern", before: meridian_source4_pattern, after: meridian_ex2_s4 },
    { label: "Girl", before: meridian_source5_girl, after: meridian_ex2_s5 },
    { label: "Berries", before: meridian_source6_berries, after: meridian_ex2_s6 },
  ]}
/>
*Luma Solarization — simulated result across source images.*
**Source**: A portrait or landscape with smooth tonal gradients and visible highlights.

**Objective**: Enable the Y fold to produce brightness solarization — the Sabattier effect — while keeping chrominance folds bypassed for clean colour.

1. **Enable Y fold**: Set Y Folds to 1x (fold active). The luminance immediately develops the characteristic solarized look — highlights fold back down, creating double-exposure-like tonal mirroring.
2. **Increase Y contrast**: Push Y Fold (pot 1) above ~60%. More of the Y signal exceeds the midpoint, increasing the proportion of folded pixels. The highlights reflect more aggressively.
3. **Adjust Y brightness**: Shift Y Gain (pot 4) below 50% to darken the image before folding, or above 50% to brighten it. Notice how the fold point shifts — the boundary between normal and folded pixels moves through the tonal range.
4. **Keep chroma clean**: Leave U Folds and V Folds at 2x (bypass). The colours remain natural even as the brightness solarizes.
5. **Mix to taste**: Pull Mix to ~70% for a partial solarization that preserves some of the original tonal structure.

**Key concepts**: Y fold creates the classic solarization / Sabattier effect, contrast controls how much signal crosses the fold threshold, brightness shifts the fold point through the tonal range, chrominance folds can be left bypassed for clean colour

---

### Exercise 3: Full Chromatic Solarization with Inversion

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: meridian_source1_ballerina, after: meridian_ex3_s1 },
    { label: "Fruit", before: meridian_source2_fruit, after: meridian_ex3_s2 },
    { label: "Turtle", before: meridian_source3_turtle, after: meridian_ex3_s3 },
    { label: "Pattern", before: meridian_source4_pattern, after: meridian_ex3_s4 },
    { label: "Girl", before: meridian_source5_girl, after: meridian_ex3_s5 },
    { label: "Berries", before: meridian_source6_berries, after: meridian_ex3_s6 },
  ]}
/>
*Full Chromatic Solarization with Inversion — simulated result across source images.*
**Source**: Any footage — abstract or representational. Bold, saturated footage produces the most dramatic results.

**Objective**: Activate all three folds with luma inversion to produce the most extreme Meridian effect — a fully solarized, inverted, stained-glass colour transformation.

1. **Enable all folds**: Set Y Folds, U Folds, and V Folds to 1x (fold active).
2. **Enable luma inversion**: Set Link UV to On (which actually activates luma inversion despite the label).
3. **Boost all contrast**: Push Y Fold, U Fold, V Fold (pots 1–3) to ~70%. This drives all three channels hard into the fold.
4. **Offset brightness**: Set Y Gain to ~40%, U Gain to ~55%, V Gain to ~45%. Asymmetric offsets create more complex colour paths through the fold.
5. **Observe the result**: The image should be dramatically transformed — inverted tones with harmonic colour reflections, producing stained-glass-like false colour from ordinary footage.
6. **Compare with Mix**: Sweep Mix from 100% down to 50%. The effect softens into a ghostly colour overlay.

**Key concepts**: All three folds active creates maximum harmonic complexity, luma inversion reverses the tonal starting point before fold, asymmetric brightness offsets create non-uniform colour paths, Mix blends extreme effects to taste

---


## Tips

- **"Fold" pots are contrast, "Gain" pots are brightness**: The panel labels are swapped. Pots 1–3 control proc_amp gain (contrast), and pots 4–6 control proc_amp offset (brightness). Mental model: "Fold" → scale, "Gain" → shift.
- **"Link UV" is luma invert**: Toggle 10 does not link the chrominance channels. It inverts the Y channel at the very start of the pipeline, before contrast and brightness are applied.
- **Start with folds bypassed**: Set all three fold toggles to 2x (bypass) and use Meridian as a pure proc_amp colour corrector. This is the easiest way to learn what each pot actually does.
- **Fold one channel at a time**: Enable folds individually to isolate their effect. Y fold alone creates brightness solarization; U or V fold alone creates single-axis chrominance solarization; all three together creates maximum complexity.
- **Contrast drives fold intensity**: Higher contrast pushes more of the signal past the fold midpoint. At low contrast, very little of the signal crosses 512, so the fold has minimal visible effect. At high contrast, most of the signal folds, creating dramatic tonal inversion.
- **Brightness shifts the fold boundary**: Think of brightness as sliding the image up and down relative to a fixed fold point at 512. Low brightness = mostly unfolded; high brightness = mostly folded.
- **Mix at 40–60% for subtlety**: Full-strength solarization can be overwhelming. Pull the Mix fader to mid-range for a ghostly colour overlay that preserves the source image's structure while adding harmonic complexity.
- **Luma inversion + fold = complementary solarization**: With inversion on, the fold operates on the inverse tonal range, producing a complementary set of colours and tones. Compare On and Off to find the version that best suits the source material.

---

## Glossary

| Term | Definition |
|------|------------|
| **Brightness** | In a proc_amp, the DC offset added after contrast scaling. Shifts the entire signal lighter or darker. |
| **BT.601** | The ITU-R standard defining the colour matrix used to convert between RGB and YUV in standard-definition video. Used throughout the Videomancer pipeline. |
| **Contrast** | In a proc_amp, the scaling factor applied to the input deviation from midpoint. Controls dynamic range expansion or compression. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip that implements Meridian's pixel pipeline in parallel hardware. |
| **Frequency doubler** | A nonlinear transfer function that folds a signal at its midpoint, effectively doubling its spatial frequency. Values below midpoint are scaled by 2×; values above are reflected and scaled by 2×. |
| **Luma** | The luminance (brightness) component of a YUV video signal, carrying the greyscale information. |
| **Proc amp** | Processing amplifier; a standard video circuit that adjusts contrast and brightness via scaling and offset: $(input - 512) \times contrast / 512 + brightness$. |
| **Sabattier effect** | A darkroom phenomenon where brief re-exposure during development creates partial tonal inversion. The inspiration for Meridian's wavefold solarization. |
| **Solarization** | The visual effect of tonal folding — highlights inverting toward shadows, or the reverse — producing false-colour or negative-like imagery. Technically a misnomer (true solarization requires extreme overexposure), but the term is widely used for the Sabattier effect. |
| **Triangle wave** | A periodic waveform that rises and falls linearly. The frequency doubler's output is a triangle-shaped transfer function that peaks at the midpoint. |
| **Wavefold** | A signal processing technique where a signal that exceeds a threshold is reflected back, rather than clipping. Creates harmonic overtones analogous to wavefolding in analogue synthesizers. |
| **YUV** | A colour space separating luminance (Y) from chrominance (U = blue-difference, V = red-difference). The native pixel format of the Videomancer pipeline. |

---
