---
draft: true
sidebar_position: 95
slug: /instruments/videomancer/duotone
title: "Duotone"
image: /img/instruments/videomancer/duotone/duotone_hero_s1.png
description: "Most color video processors adjust the colors that already exist in the source signal."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import duotone_control_panel from '/img/instruments/videomancer/duotone/duotone_control_panel.png';
import duotone_source1_car from '/img/instruments/videomancer/duotone/duotone_source1_car.png';
import duotone_source2_parrot from '/img/instruments/videomancer/duotone/duotone_source2_parrot.png';
import duotone_source3_clouds from '/img/instruments/videomancer/duotone/duotone_source3_clouds.png';
import duotone_source4_pattern from '/img/instruments/videomancer/duotone/duotone_source4_pattern.png';
import duotone_source5_woman from '/img/instruments/videomancer/duotone/duotone_source5_woman.png';
import duotone_source6_paint from '/img/instruments/videomancer/duotone/duotone_source6_paint.png';
import duotone_hero_s1 from '/img/instruments/videomancer/duotone/duotone_hero_s1.png';
import duotone_hero_s2 from '/img/instruments/videomancer/duotone/duotone_hero_s2.png';
import duotone_hero_s3 from '/img/instruments/videomancer/duotone/duotone_hero_s3.png';
import duotone_hero_s4 from '/img/instruments/videomancer/duotone/duotone_hero_s4.png';
import duotone_hero_s5 from '/img/instruments/videomancer/duotone/duotone_hero_s5.png';
import duotone_hero_s6 from '/img/instruments/videomancer/duotone/duotone_hero_s6.png';
import duotone_ex1_s1 from '/img/instruments/videomancer/duotone/duotone_ex1_s1.png';
import duotone_ex1_s2 from '/img/instruments/videomancer/duotone/duotone_ex1_s2.png';
import duotone_ex1_s3 from '/img/instruments/videomancer/duotone/duotone_ex1_s3.png';
import duotone_ex1_s4 from '/img/instruments/videomancer/duotone/duotone_ex1_s4.png';
import duotone_ex1_s5 from '/img/instruments/videomancer/duotone/duotone_ex1_s5.png';
import duotone_ex1_s6 from '/img/instruments/videomancer/duotone/duotone_ex1_s6.png';
import duotone_ex2_s1 from '/img/instruments/videomancer/duotone/duotone_ex2_s1.png';
import duotone_ex2_s2 from '/img/instruments/videomancer/duotone/duotone_ex2_s2.png';
import duotone_ex2_s3 from '/img/instruments/videomancer/duotone/duotone_ex2_s3.png';
import duotone_ex2_s4 from '/img/instruments/videomancer/duotone/duotone_ex2_s4.png';
import duotone_ex2_s5 from '/img/instruments/videomancer/duotone/duotone_ex2_s5.png';
import duotone_ex2_s6 from '/img/instruments/videomancer/duotone/duotone_ex2_s6.png';
import duotone_ex3_s1 from '/img/instruments/videomancer/duotone/duotone_ex3_s1.png';
import duotone_ex3_s2 from '/img/instruments/videomancer/duotone/duotone_ex3_s2.png';
import duotone_ex3_s3 from '/img/instruments/videomancer/duotone/duotone_ex3_s3.png';
import duotone_ex3_s4 from '/img/instruments/videomancer/duotone/duotone_ex3_s4.png';
import duotone_ex3_s5 from '/img/instruments/videomancer/duotone/duotone_ex3_s5.png';
import duotone_ex3_s6 from '/img/instruments/videomancer/duotone/duotone_ex3_s6.png';

# Duotone

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Car", before: duotone_source1_car, after: duotone_hero_s1 },
    { label: "Parrot", before: duotone_source2_parrot, after: duotone_hero_s2 },
    { label: "Clouds", before: duotone_source3_clouds, after: duotone_hero_s3 },
    { label: "Pattern", before: duotone_source4_pattern, after: duotone_hero_s4 },
    { label: "Woman", before: duotone_source5_woman, after: duotone_hero_s5 },
    { label: "Paint", before: duotone_source6_paint, after: duotone_hero_s6 },
  ]}
/>
*Duotone applying luma-driven dual-hue colorization to remap source brightness into cool shadow and warm highlight tones with adjustable threshold and blend.*

---

## Overview

Most color video processors adjust the colors that already exist in the source signal. Duotone discards the original chrominance entirely and rebuilds it from scratch, using only the brightness of each pixel to decide what color it should become. The program assigns one hue to the shadow range and a second hue to the highlight range, then blends between them based on where each pixel falls on the brightness scale.

The name comes directly from the printing technique: a *duotone* print uses two ink colors — typically black plus one spot color — to reproduce a photographic image with richer tonal depth than a single-ink halftone. Duotone extends the concept by allowing independent hue control for both the shadow and highlight ends of the tonal range, creating the video equivalent of split-tone darkroom printing.

At subtle settings the program produces the warm-shadow, cool-highlight aesthetic of traditional photographic toning baths. At extreme settings — maximum hue offsets with hard-edge thresholding — it reduces the image to a stark two-color graphic reminiscent of pop art screen printing or propaganda poster design.

---

## Quick Start

1. **Soft edge for photography, hard edge for graphics**: Soft-edge mode creates the continuous gradient blend of darkroom split toning. Hard-edge mode creates the flat color zones of screen printing and pop art.
2. **Hues are complementary**: Shadow and highlight tints sit on opposing UV axes (blue-cyan vs. red-amber). This guarantees a pleasing complementary palette regardless of pot positions.
3. **Invert flips everything**: Because inversion happens before the blend calculation, it reverses the color assignment *and* the brightness in one toggle — useful for quickly exploring the opposite palette.

---

## Background

### Duotone Printing

In commercial printing, a standard halftone uses a single ink (usually black) to reproduce a photograph. The limitation is obvious: a single ink can only express tonal range, not color richness. Duotone printing solves this by running the paper through the press twice with two different inks — often black for the shadows and a second color (sepia, Pantone blue, warm gray) for the midtones and highlights. The result is a monochromatic image with far greater tonal depth than a single-pass halftone. Tritone and quadtone extend the idea to three and four inks. The Videomancer Duotone program implements the two-color version digitally, replacing the shadow and highlight inks with selectable UV offsets in the YUV color space.

### Split Toning in Photography

Darkroom photographers discovered that chemical toning baths — selenium, sepia, gold, copper — could selectively color different tonal ranges of a silver gelatin print. A selenium-toned print might have cool blue-purple shadows while the highlights remain neutral, or a sepia-toned print might warm only the midtones and highlights while the deepest blacks stay cold. The technique depends on the fact that different tonal densities of silver respond differently to chemical toners. Duotone's soft-edge mode replicates this behavior: the blend between shadow and highlight hues follows the natural brightness gradient of the source, creating the same selective coloring without chemistry.

### Pop Art and Two-Color Graphics

Andy Warhol's screen prints — Marilyn, Mao, Campbell's Soup — are perhaps the most recognizable application of reduced-color image processing. Warhol photographed his subjects, then used high-contrast lithographic film to separate the image into starkly simplified tonal zones, each printed in a flat ink color. The result strips away photographic subtlety and replaces it with graphic boldness. Duotone's hard-edge mode produces the same effect: a binary threshold divides the image into two zones, each filled with a solid hue. The threshold control sets the cutoff point, determining how much of the image falls into each color zone.

### Hue Mapping in the YUV Domain

In BT.601 YUV encoding, color is represented by two chroma components — U (blue-difference) and V (red-difference) — centered at a midpoint of 512 in the 10-bit domain. A pixel with U=512 and V=512 is achromatic (gray). Duotone generates its hues by offsetting U and V from this midpoint in opposite directions: shadow hue pushes U positive and V negative (toward the blue-cyan axis), while highlight hue pushes U negative and V positive (toward the red-amber axis). The two controls determine the *strength* of offset along these complementary axes rather than selecting arbitrary hue angles — this constraint ensures the shadow and highlight tints are always complementary.

### Colorization in Early Cinema and Video Art

Before the invention of color film, filmmakers applied tints and tones to black-and-white footage. Tinting dyed the entire film base (coloring highlights and midtones), while toning chemically replaced the silver image with a colored compound (coloring shadows and blacks). The combination of tinting and toning produced a two-color effect strikingly similar to modern split toning. Video artists adopted analogous techniques in the analog domain — colorizing monochrome signals by injecting subcarrier reference tones keyed to luminance levels. Duotone is the digital descendant of these practices, applying luma-keyed colorization at 74.25 million pixels per second.


---

## Signal Flow

Optional Inversion → Brightness Scale → Shadow Hue → UV → Highlight Hue → UV → Blend Factor from Luma → UV Crossfade

```
Input Video (YUV 4:4:4)
│
├─ Luma Path ──────────────────────────────────────────────
│   ├─ 1. Optional Inversion     (bitwise NOT of Y)
│   └─ 2. Brightness Scale       (luma × Brightness >> 10)
│         └──→ Processed Y
│
├─ Chroma Generation ──────────────────────────────────────
│   ├─ 1. Shadow Hue → UV        (U = 512 + hue/4, V = 512 − hue/4)
│   ├─ 2. Highlight Hue → UV     (U = 512 − hue/4, V = 512 + hue/4)
│   ├─ 3. Blend Factor from Luma
│   │      ├─ Hard Edge: binary   (luma ≥ threshold → 1023, else 0)
│   │      └─ Soft Edge: blend = luma value
│   └─ 4. UV Crossfade
│          (blend × highlight_UV + (1023 − blend) × shadow_UV) >> 10
│          └──→ Processed U, V
│
├─ Mix (3× interpolator_u) ───────────────────────────────
│   └─ Dry/wet blend per channel  (original ←→ processed)
│
├─ Sync Delay ─────────────────────────────────────────────
│   └─ 8-clock pipeline           (hsync_n, vsync_n, field_n, Y, U, V)
│
└─ Bypass Mux ─────────────────────────────────────────────
    └─ Select delayed original or mixed output
```

Two structural details are important. First, the Invert toggle sits at the very beginning of the pipeline — before both the blend factor calculation and the brightness scaler. Inversion does not simply flip the output brightness; it also reverses the shadow/highlight color assignment in soft-edge mode, because the blend is driven by the inverted luma. Dark areas of the source receive the highlight hue and bright areas receive the shadow hue, flipping the entire color map.

Second, the hue controls map to fixed complementary UV axes rather than arbitrary hue angles. Shadow Hue pushes U positive and V negative (blue-cyan direction) while Highlight Hue pushes U negative and V positive (red-amber direction). The two pots control the *strength* of tinting along these opposing axes. This means the shadow and highlight colors are always perceptual complements, which is consistent with traditional split-tone aesthetics.

---

## Parameter Reference

<img src={duotone_control_panel} alt="Videomancer front panel with Duotone loaded"/>
*Videomancer's front panel with Duotone active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Shadow Hue
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

At 0%, the shadow tint is neutral gray — no color is added to dark areas. As the pot increases, the shadow color shifts along the blue-cyan axis (U increases, V decreases relative to mid). At maximum, dark areas of the image carry a strong cool tint. The offset is computed as the pot value divided by four, giving a maximum chroma displacement of 255 out of 512 from the center — enough for vivid color without wrapping. Internally, controls the chrominance offset applied to the shadow (dark) regions of the image.

---

#### Knob 2 — Highlight Hue
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls the chrominance offset applied to the highlight (bright) regions. The offset axis is complementary to Shadow Hue: U decreases and V increases relative to mid, producing a warm red-amber tint. At 0%, highlights remain neutral. At maximum, bright areas carry a strong warm tint. With both Shadow Hue and Highlight Hue at maximum, the image splits into a dramatic cool-shadow, warm-highlight duotone — the classic split-tone look.

---

#### Knob 3 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the luma cutoff point for hard-edge mode. When Hard Edge (Toggle 9) is active, pixels with brightness at or above this threshold receive the highlight hue and pixels below receive the shadow hue, with no gradual blend between them. This control has no effect in soft-edge mode, where the blend follows the luma gradient directly. At 50% threshold with hard edge, the image splits roughly in half tonally; lower values assign more of the image to the highlight zone, higher values assign more to the shadow zone.

---

#### Knob 4 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

This parameter is declared in the TOML configuration and mapped to a register but is not connected to the processing pipeline in the current firmware. The label suggests it was intended to control the width of the transition zone between shadow and highlight hues. Adjusting this control has no effect on the output.

---

#### Knob 5 — Intensity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

This parameter is declared in the TOML configuration and mapped to a register but is not connected to the processing pipeline in the current firmware. The label suggests it was intended to control the saturation intensity of the applied hue tints. Adjusting this control has no effect on the output.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scales the output luminance via a fixed-point multiply. The processing luma (after optional inversion) is multiplied by this register value and the upper 10 bits of the 20-bit product are taken as the result. At maximum (100%), the output brightness roughly matches the input. At 50%, brightness is halved. At 0%, the output goes black. This scaling applies only to the processed luma — the original signal available through the Mix fader is unaffected.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Swap** | Off | On |
| **8 — Mono Input** | Off | On |
| **9 — Hard Edge** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control three active features and two reserved parameters. Hard Edge (Toggle 9) selects between soft gradient blending and binary threshold mode. Invert (Toggle 10) applies a bitwise complement to the input luma before all downstream processing. Bypass (Toggle 11) routes the original delayed signal directly to the output. Swap (Toggle 7) and Mono Input (Toggle 8) are declared in the configuration but not connected in the current VHDL pipeline — they have no effect on the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original input and the fully processed output, implemented by three parallel interpolator instances (one per YUV channel). At 100% (fully clockwise), the output is entirely the colorized duotone signal. At 0%, the output is the unmodified original. Intermediate positions blend the two, allowing subtle tinting effects where the original color partially shows through the duotone colorization.





---

## Guided Exercises

These exercises progress from gentle split toning to aggressive two-color graphics, demonstrating the full range of Duotone's colorization capabilities.

### Exercise 1: Classic Split Tone

<BeforeAfterSlider
  sources={[
    { label: "Car", before: duotone_source1_car, after: duotone_ex1_s1 },
    { label: "Parrot", before: duotone_source2_parrot, after: duotone_ex1_s2 },
    { label: "Clouds", before: duotone_source3_clouds, after: duotone_ex1_s3 },
    { label: "Pattern", before: duotone_source4_pattern, after: duotone_ex1_s4 },
    { label: "Woman", before: duotone_source5_woman, after: duotone_ex1_s5 },
    { label: "Paint", before: duotone_source6_paint, after: duotone_ex1_s6 },
  ]}
/>
*Classic Split Tone — simulated result across source images.*
**Source**: A portrait or landscape with a wide tonal range — skin tones, sky, and shadow detail.

**What You'll Create**: Create a warm-highlight, cool-shadow split-tone look matching traditional photographic toning.

1. **Neutral start**: Set Shadow Hue and Highlight Hue to 0%. Observe that the image retains its original colors through the mix.
2. **Add shadow tint**: Slowly increase Shadow Hue to ~25%. Dark areas take on a subtle blue-cyan cast.
3. **Add highlight tint**: Increase Highlight Hue to ~50%. Bright areas warm toward amber.
4. **Adjust brightness**: Sweep Brightness from 50% upward to find a pleasing overall exposure.
5. **Blend**: Lower the Mix fader to ~70% to let some original color show through the duotone tint.

**Key concepts**: Split toning is a continuous gradient blend driven by luma, shadow and highlight hues are always complementary, the Mix fader controls the intensity of the effect

---

### Exercise 2: Hard-Edge Two-Color Poster

<BeforeAfterSlider
  sources={[
    { label: "Car", before: duotone_source1_car, after: duotone_ex2_s1 },
    { label: "Parrot", before: duotone_source2_parrot, after: duotone_ex2_s2 },
    { label: "Clouds", before: duotone_source3_clouds, after: duotone_ex2_s3 },
    { label: "Pattern", before: duotone_source4_pattern, after: duotone_ex2_s4 },
    { label: "Woman", before: duotone_source5_woman, after: duotone_ex2_s5 },
    { label: "Paint", before: duotone_source6_paint, after: duotone_ex2_s6 },
  ]}
/>
*Hard-Edge Two-Color Poster — simulated result across source images.*
**Source**: High-contrast footage — strong backlit silhouettes or graphic shapes against a bright background.

**What You'll Create**: Create a stark two-color graphic using hard-edge threshold mode.

1. **Enable hard edge**: Turn on Hard Edge (Toggle 9). The blend snaps to binary.
2. **Set threshold**: Adjust Threshold to ~50%. The image splits into two flat color zones.
3. **Maximize hues**: Push Shadow Hue to ~75% and Highlight Hue to ~75% for vivid complementary colors.
4. **Set brightness**: Set Brightness to ~100% so the light zone is fully bright.
5. **Sweep the threshold**: Move Threshold slowly from 0% to 100%. Watch the boundary between the two color zones sweep through the tonal range of the source.
6. **Invert**: Toggle Invert (Toggle 10) to reverse which color goes to shadows and which to highlights.

**Key concepts**: Hard-edge mode uses a binary threshold to split the image into exactly two color zones, threshold position determines the tonal cutoff, inversion reverses the entire color assignment

---

### Exercise 3: Inverted Duotone with Partial Mix

<BeforeAfterSlider
  sources={[
    { label: "Car", before: duotone_source1_car, after: duotone_ex3_s1 },
    { label: "Parrot", before: duotone_source2_parrot, after: duotone_ex3_s2 },
    { label: "Clouds", before: duotone_source3_clouds, after: duotone_ex3_s3 },
    { label: "Pattern", before: duotone_source4_pattern, after: duotone_ex3_s4 },
    { label: "Woman", before: duotone_source5_woman, after: duotone_ex3_s5 },
    { label: "Paint", before: duotone_source6_paint, after: duotone_ex3_s6 },
  ]}
/>
*Inverted Duotone with Partial Mix — simulated result across source images.*
**Source**: Any footage with moderate contrast and visible color detail.

**What You'll Create**: Combine luma inversion with partial wet/dry mix to create an unusual tinted negative effect.

1. **Enable invert**: Turn on Invert (Toggle 10). The image brightness reverses.
2. **Set moderate hues**: Shadow Hue ~40%, Highlight Hue ~60%. The inverted tonal map now assigns warm tones to originally dark areas and cool tones to originally bright areas.
3. **Reduce brightness**: Lower Brightness to ~40%. The inverted image darkens, creating a moody palette.
4. **Partial mix**: Set Mix to ~50%. The original colors blend with the inverted duotone, producing a surreal double-exposure effect.
5. **Compare**: Toggle Bypass on and off to compare the composite with the original source.

**Key concepts**: Inversion reverses the luma before all processing including the blend factor, partial mix creates composites of original and processed signal, brightness scaling operates on the inverted luma

---


## Tips

- **Brightness controls exposure**: The brightness scaler is a simple multiply, not a proc amp. At 50% (default), output brightness is halved. Push toward 100% for full-level output.
- **Mix for subtlety**: Reducing the Mix fader lets original chrominance bleed through the duotone tint, creating a less aggressive effect than full wet.
- **Feedback loops**: Routing the output back to the input creates recursive colorization — the duotone effect deepens with each pass, converging toward the two endpoint hues.
- **Unused controls**: Spread (Pot 4), Intensity (Pot 5), Swap (Toggle 7), and Mono Input (Toggle 8) are declared but not connected in the current pipeline. They are reserved for future firmware updates.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation BT.601; the color encoding standard used by Videomancer, defining how RGB maps to YUV. |
| **Chroma** | The color information in a video signal, encoded as U and V components offset from a midpoint of 512 in the 10-bit domain. |
| **Colorization** | The process of adding color to a monochrome or desaturated signal based on a mapping rule (here, luma-to-hue). |
| **Duotone** | A printing technique using two ink colors to reproduce a photographic image; by extension, any two-color tonal mapping. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Split Toning** | A photographic technique that applies different color tints to the shadow and highlight regions of an image. |
| **Threshold** | A brightness cutoff value that divides the image into two tonal zones in hard-edge mode. |

---
