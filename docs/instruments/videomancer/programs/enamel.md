---
draft: true
sidebar_position: 101
slug: /instruments/videomancer/enamel
title: "Enamel"
image: /img/instruments/videomancer/enamel/enamel_hero_s1.png
description: "Enamel transforms live video into a digital simulation of cloisonné enamelwork — the ancient decorative art in which thin metal wires are soldered onto a surface to form cells, each filled with vitreous glass paste and fired to a glossy finish."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import enamel_control_panel from '/img/instruments/videomancer/enamel/enamel_control_panel.png';
import enamel_source1_parrot from '/img/instruments/videomancer/enamel/enamel_source1_parrot.png';
import enamel_source2_cat from '/img/instruments/videomancer/enamel/enamel_source2_cat.png';
import enamel_source3_collage from '/img/instruments/videomancer/enamel/enamel_source3_collage.png';
import enamel_source4_pattern from '/img/instruments/videomancer/enamel/enamel_source4_pattern.png';
import enamel_source5_woman from '/img/instruments/videomancer/enamel/enamel_source5_woman.png';
import enamel_source6_paint from '/img/instruments/videomancer/enamel/enamel_source6_paint.png';
import enamel_hero_s1 from '/img/instruments/videomancer/enamel/enamel_hero_s1.png';
import enamel_hero_s2 from '/img/instruments/videomancer/enamel/enamel_hero_s2.png';
import enamel_hero_s3 from '/img/instruments/videomancer/enamel/enamel_hero_s3.png';
import enamel_hero_s4 from '/img/instruments/videomancer/enamel/enamel_hero_s4.png';
import enamel_hero_s5 from '/img/instruments/videomancer/enamel/enamel_hero_s5.png';
import enamel_hero_s6 from '/img/instruments/videomancer/enamel/enamel_hero_s6.png';
import enamel_ex1_s1 from '/img/instruments/videomancer/enamel/enamel_ex1_s1.png';
import enamel_ex1_s2 from '/img/instruments/videomancer/enamel/enamel_ex1_s2.png';
import enamel_ex1_s3 from '/img/instruments/videomancer/enamel/enamel_ex1_s3.png';
import enamel_ex1_s4 from '/img/instruments/videomancer/enamel/enamel_ex1_s4.png';
import enamel_ex1_s5 from '/img/instruments/videomancer/enamel/enamel_ex1_s5.png';
import enamel_ex1_s6 from '/img/instruments/videomancer/enamel/enamel_ex1_s6.png';
import enamel_ex2_s1 from '/img/instruments/videomancer/enamel/enamel_ex2_s1.png';
import enamel_ex2_s2 from '/img/instruments/videomancer/enamel/enamel_ex2_s2.png';
import enamel_ex2_s3 from '/img/instruments/videomancer/enamel/enamel_ex2_s3.png';
import enamel_ex2_s4 from '/img/instruments/videomancer/enamel/enamel_ex2_s4.png';
import enamel_ex2_s5 from '/img/instruments/videomancer/enamel/enamel_ex2_s5.png';
import enamel_ex2_s6 from '/img/instruments/videomancer/enamel/enamel_ex2_s6.png';
import enamel_ex3_s1 from '/img/instruments/videomancer/enamel/enamel_ex3_s1.png';
import enamel_ex3_s2 from '/img/instruments/videomancer/enamel/enamel_ex3_s2.png';
import enamel_ex3_s3 from '/img/instruments/videomancer/enamel/enamel_ex3_s3.png';
import enamel_ex3_s4 from '/img/instruments/videomancer/enamel/enamel_ex3_s4.png';
import enamel_ex3_s5 from '/img/instruments/videomancer/enamel/enamel_ex3_s5.png';
import enamel_ex3_s6 from '/img/instruments/videomancer/enamel/enamel_ex3_s6.png';

# Enamel

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: enamel_source1_parrot, after: enamel_hero_s1 },
    { label: "Cat", before: enamel_source2_cat, after: enamel_hero_s2 },
    { label: "Collage", before: enamel_source3_collage, after: enamel_hero_s3 },
    { label: "Pattern", before: enamel_source4_pattern, after: enamel_hero_s4 },
    { label: "Woman", before: enamel_source5_woman, after: enamel_hero_s5 },
    { label: "Paint", before: enamel_source6_paint, after: enamel_hero_s6 },
  ]}
/>
*Enamel partitioning a portrait into cloisonné cells — gold wire outlines tracing every contour, vivid quantized fill glowing between the boundaries.*

---

## Overview

Enamel transforms live video into a digital simulation of cloisonné enamelwork — the ancient decorative art in which thin metal wires are soldered onto a surface to form cells, each filled with vitreous glass paste and fired to a glossy finish. The program detects edges in the luminance channel to generate wire boundaries, quantizes the brightness within those cells to produce flat, poster-like fill regions, boosts chroma saturation for vivid color, and optionally overlays a position-based gloss shimmer to simulate the curved, reflective surface of real enamel.

The name references both the material (enamel — a glassy coating fused to metal) and the visual character of the output. At moderate settings, Enamel produces a stylized, illustrative look that preserves recognizable imagery while reducing it to bold outlines and flat color. At extreme settings, the image collapses into large uniform cells separated by dense wire networks, resembling stained glass or abstract mosaic. The four style presets — Cloisonné, Champlevé, Plique-à-jour, and Basse-taille — switch between gold and dark wire and between cool and warm palette temperatures, covering the major visual traditions of historical enamelwork.

The signal path is compact: a single video line buffer stores the previous line of Y data for vertical edge detection, horizontal gradient comes from a one-pixel delay, and the combined edge strength determines whether each pixel becomes wire or fill. Three interpolators handle the wet/dry mix. Total pipeline latency is ten clock cycles, with no frame-buffer dependency.

---

## Quick Start

1. **Wire before fill**: Edge detection operates on the raw input luminance, so wire boundaries always trace the source image's natural contours regardless of how aggressively the fill is posterized. Adjust wire first, then tune the palette.
2. **Two-knob threshold**: Wire W and Edge Thr combine to set the effective detection threshold. Think of Wire W as the coarse control and Edge Thr as the fine-tune — together they give more range than either alone.
3. **Coarse palette for authenticity**: Real cloisonné cells contain a single opaque color. Palette steps 1–3 produce the most convincing enamel look; higher steps add tonal nuance at the cost of realism.

---

## Background

### The Art of Cloisonné

Cloisonné (from the French *cloison*, partition) is the oldest and most widely recognized enamel technique. Thin strips of metal wire — traditionally gold, silver, or copper — are bent into shapes and soldered onto a metal base to form enclosed cells. Each cell is filled with powdered glass mixed with metallic oxide pigments, then fired in a kiln at roughly 800 °C until the glass melts and fuses to the metal. After cooling, the surface is ground flat and polished to a high gloss. The result is a mosaic of vivid, opaque color fields separated by gleaming metallic lines that follow the contours of the design.

Cloisonné originated in the ancient Near East around the 12th century BCE and reached its artistic peak in Byzantine, Chinese, and Japanese workshops. The technique demands precision — each wire must be shaped by hand, and the enamel paste must be applied in thin layers to avoid cracking during firing. Videomancer's Enamel program digitizes this craft: edge detection generates the wire network, luminance quantization produces the flat opaque fill, and saturation boost creates the jewel-toned color characteristic of fired vitreous enamel.

### Champlevé, Plique-à-jour, and Basse-taille

Cloisonné is only one member of a family of historical enamel techniques that differ in how the cells are formed and how light interacts with the surface. **Champlevé** (raised field) carves or etches troughs into a thick metal plate rather than building cells from wire; the recessed areas are filled with enamel while the raised metal surface remains visible. The effect is bolder and more architectural than cloisonné because the wire boundaries are the full thickness of the plate.

**Plique-à-jour** (open to daylight) removes the metal backing entirely, leaving translucent enamel suspended in a wire framework like miniature stained glass. Light passes through the enamel, producing luminous, saturated color. **Basse-taille** (low cutting) engraves the metal base with a relief pattern before applying translucent enamel; the underlying texture shows through the glass layer, creating depth and tonal variation. Enamel's four Style toggle positions are named after these techniques, cycling through gold/dark wire and warm/cool palette combinations that approximate each tradition's characteristic visual temperature.

### Edge Detection in Image Processing

Edge detection identifies locations in an image where brightness changes sharply — the boundaries between objects, shadows, and textures. The simplest approach computes the **gradient**: the rate of change of pixel intensity from one sample to the next. A large gradient means a sharp transition; a small gradient means a smooth region.

Enamel computes two gradients per pixel. The **horizontal gradient** is the absolute difference between the current pixel's luminance and the previous pixel's luminance (a one-sample delay). The **vertical gradient** is the absolute difference between the current pixel and the corresponding pixel on the previous scan line (read from a line buffer stored in one BRAM). The two gradients are combined using an approximation of the Euclidean magnitude: the larger of the two is taken at full strength, and half the smaller is added. This produces a rotationally reasonable edge estimate without requiring a multiplication or square root — critical at 74.25 MHz on iCE40 fabric.

### Color Quantization and Posterization

Quantization reduces a continuous range of values to a smaller set of discrete levels. When applied to pixel brightness, it creates **posterization** — named after the flat-toned look of screen-printed posters. Smooth gradients collapse into staircase transitions between uniform tonal bands, each spanning a range of input values that all map to the same output level.

Enamel quantizes the Y channel by masking the lower bits of the 10-bit luminance value. The Palette control selects one of seven shift amounts, producing between 8 levels (shift 7 — very coarse, dramatic flat cells) and 512 levels (shift 1 — nearly imperceptible steps). In the context of enamelwork simulation, heavy quantization is desirable: real enamel cells are filled with a single opaque color, so the flat tonal bands mimic the uniform appearance of fired glass paste within each wire-bounded region.

### Metallic Surface Rendering

Real enamel objects have a polished, curved surface that reflects light in complex ways. The glossy finish produces specular highlights — bright spots that shift position as the viewing angle changes. Enamel simulates this with a position-dependent luminance modulation derived from XOR-ing horizontal and vertical pixel coordinates. The resulting pattern is a quasi-periodic grid of bright and dark patches that mimics the alternating highlight and shadow across a curved reflective surface.

The gloss intensity is controlled by AND-ing the coordinate-derived pattern with a parameter value, then shifting right by three bits. This scales the modulation from invisible (parameter = 0) to a noticeable luminance ripple (parameter = 1023). Wire pixels can also receive a separate shimmer animation derived from XOR-ing the frame counter with the horizontal position, producing a subtle per-frame sparkle that simulates the play of light across metal.


---

## Signal Flow

Y Channel → U/V Channels → Mix → Bypass → Sync

```
Input Video (YUV 4:4:4)
│
├── Y Channel ─────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register + 1-Pixel Delay (horiz prev)
│   ├─ 2. Pipeline Delay (VLB address register)
│   ├─ 3. Line Buffer Read (prev line Y for vertical edge)
│   ├─ 4. Edge Gradient Compute
│   │       H = |Y_curr − Y_prev_pixel|
│   │       V = |Y_curr − Y_prev_line|
│   │       Combined = max(H,V) + min(H,V)/2  (clamp 1023)
│   ├─ 5. Wire / Fill Decision
│   │       eff_thresh = edge_threshold − wire_width/2
│   │       is_wire = (combined > eff_thresh)
│   │   ┌── Wire Path ──────────────────────────
│   │   │   Gold:  Y = wire_bright, UV = warm tint
│   │   │   Dark:  Y = wire_bright/4, UV = neutral
│   │   │   Animate: Y += (frame XOR h_pos) shimmer
│   │   │
│   │   └── Fill Path ──────────────────────────
│   │       Y = quantize(Y_source, palette_shift)
│   │       Gloss: Y += (h_pos XOR v_pos) × gloss_amt >> 3
│   │
│   └─ 6. Composite Y
│
├── U/V Channels ──────────────────────────────────────────────
│   │
│   ├─ Pipeline Delay (stages 1-5)
│   ├─ 5. Wire / Fill Decision
│   │   ├── Wire → UV tint (gold warm / dark neutral)
│   │   └── Fill → Saturation Boost (push UV from 512)
│   │              + Warm/Cool palette shift (V += 32)
│   └─ 6. Composite U/V
│
├── Mix ───────────────────────────────────────────────────────
│   └─ 3× interpolator_u (dry/wet crossfade per channel)
│
├── Bypass ────────────────────────────────────────────────────
│   └─ Select original (delayed) or processed signal
│
└── Sync ──────────────────────────────────────────────────────
    └─ 10-clock shift register pass-through
```

The critical interaction is between edge detection and quantization. Edge detection operates on the *original* unquantized luminance, so the wire boundaries track the source image's natural contours regardless of how aggressively the fill is posterized. This mirrors the cloisonné workflow where wires are shaped first, then cells are filled. The effective threshold combines two knobs — Wire W sets the baseline sensitivity, and Edge Thr lowers it further, giving independent control over detection range and wire coverage. The combined edge formula (max plus half min) provides a reasonable 2D gradient magnitude without needing multiplication, and its output feeds a single comparator that classifies every pixel as wire or fill in one clock cycle.

---

## Parameter Reference

<img src={enamel_control_panel} alt="Videomancer front panel with Enamel loaded"/>
*Videomancer's front panel with Enamel active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Wire W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At low values, even gentle gradients in the source are classified as wire, producing dense, wide-coverage boundary networks that can dominate the image. At high values, only the sharpest transitions — strong object edges and high-contrast boundaries — generate wire, leaving most of the image as smooth enamel fill. The default midpoint provides a balanced coverage suitable for most video sources. Use this as the primary control for overall wire density before fine-tuning with Edge Thr. Internally, sets the baseline threshold for edge detection.

---

#### Knob 2 — Edge Thr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Lowers the effective edge threshold, pulling more gradients above the wire detection point. This control complements Wire W: while Wire W sets the base sensitivity, Edge Thr subtracts from it, widening the wire network. At zero, it has no effect. At maximum, it halves the effective threshold, dramatically increasing wire coverage. Think of it as a secondary width control — increasing Edge Thr makes existing wires thicker and reveals wire at softer transitions that Wire W alone would miss.

---

#### Knob 3 — Palette
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

Selects the luminance quantization level for fill cells, stepping through eight palette sizes from coarse to fine. At step 1, the Y channel is reduced to just eight brightness levels — large, flat-colored cells that closely resemble traditional enamelwork. Each successive step doubles the number of levels (16, 32, 64, 128, 256, 512), progressively restoring smooth gradation. At step 8, quantization is nearly invisible, and the fill regions retain most of the source's tonal detail. For the most authentic cloisonné look, use steps 1–3.

---

#### Knob 4 — Gloss
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Boosts chroma saturation in fill cells by pushing U and V channels away from neutral (midpoint 512). Higher values produce more vivid, jewel-toned color that evokes the intense hues of fired vitreous enamel — cobalt blues, emerald greens, ruby reds. At zero, fill color matches the source chrominance exactly. This control has no effect on wire pixels, which receive their own fixed chroma tint based on the Style toggle. The saturation enhancement is symmetric: both warm and cool chrominance components are amplified equally.

---

#### Knob 5 — Flat Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness of wire pixels. Gold wire uses this value directly as the Y level, so a high setting produces bright, gleaming metallic outlines while a low setting subdues them. Dark wire divides this value by four, so even at maximum the dark wire remains understated. This control determines the visual weight of the wire network in the composition — set it high for prominent, decorative boundaries or low for subtle contour lines that let the fill dominate.

---

#### Knob 6 — Wire Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Scales the intensity of the gloss overlay applied to fill cells when gloss is enabled. The gloss pattern is derived from XOR-ing horizontal and vertical pixel coordinates, producing a quasi-periodic brightness ripple across the enamel surface. At zero, the pattern is fully masked and gloss has no visible effect. At higher values, the shimmer becomes increasingly pronounced, adding a luminance modulation that simulates light reflecting off a polished curved surface. The effect is most visible on large, uniform fill cells created by coarse Palette settings.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Cloisnne | Basel |
| **8 — Wire Color** | Gold | Black |
| **9 — Gloss** | Off | On |
| **10 — Video Pal** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into two groups. Toggles 7 and 8 are four-position switches that combine binary options into named presets: Style pairs wire type with palette temperature, and Wire Color pairs gloss enable with wire animation. Toggles 9–11 are independent two-position switches controlling gloss, the video palette flag, and bypass. The Style toggle has the most dramatic visual impact — switching between gold and dark wire and between warm and cool fill completely changes the character of the output, cycling through the four historical enamel traditions.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Cross-fades between the dry (original) and wet (processed) signal for each of the three YUV channels independently through matched interpolators. At 0%, the output is pure dry — identical to the source. At 100%, the output is fully processed enamel. Intermediate positions produce a transparency blend where the wire and fill are layered over the original image at reduced opacity, which can create a subtle illustrative overlay effect.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Enamel processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises progress from basic edge detection to full cloisonné simulation, gradually introducing quantization, coloring, and surface effects.

### Exercise 1: Wire Network Discovery

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: enamel_source1_parrot, after: enamel_ex1_s1 },
    { label: "Cat", before: enamel_source2_cat, after: enamel_ex1_s2 },
    { label: "Collage", before: enamel_source3_collage, after: enamel_ex1_s3 },
    { label: "Pattern", before: enamel_source4_pattern, after: enamel_ex1_s4 },
    { label: "Woman", before: enamel_source5_woman, after: enamel_ex1_s5 },
    { label: "Paint", before: enamel_source6_paint, after: enamel_ex1_s6 },
  ]}
/>
*Wire Network Discovery — simulated result across source images.*
**Source**: A portrait or face close-up with clear contours — eyes, nose, mouth, hairline — and a range of soft and hard edges.

**What You'll Create**: Learn how Wire W and Edge Thr interact to control wire density and coverage.

1. **Set baseline**: Turn Wire W to ~50% and Edge Thr to 0%. Observe the wire boundaries tracing only the strongest edges in the source.
2. **Lower threshold**: Slowly reduce Wire W toward 0%. Watch as progressively softer transitions become wire — texture, shadows, gradual shading all sprout outlines.
3. **Edge Thr interaction**: Return Wire W to ~50%. Now increase Edge Thr from 0% toward 100%. The wire network expands similarly — Edge Thr achieves the same visual effect as lowering Wire W, but through a different parameter path.
4. **Combine**: Set Wire W to ~60% and Edge Thr to ~40%. Find the sweet spot where the wire traces recognizable contours without filling the entire image.
5. **Flat Amt**: Adjust the Flat Amt knob to change wire brightness. Notice how brighter wire makes the boundaries more prominent and how dim wire lets them recede.

**Key concepts**: Edge detection threshold, gradient magnitude, wire coverage, combined threshold = Wire W − Edge Thr / 2

---

### Exercise 2: Palette and Saturation

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: enamel_source1_parrot, after: enamel_ex2_s1 },
    { label: "Cat", before: enamel_source2_cat, after: enamel_ex2_s2 },
    { label: "Collage", before: enamel_source3_collage, after: enamel_ex2_s3 },
    { label: "Pattern", before: enamel_source4_pattern, after: enamel_ex2_s4 },
    { label: "Woman", before: enamel_source5_woman, after: enamel_ex2_s5 },
    { label: "Paint", before: enamel_source6_paint, after: enamel_ex2_s6 },
  ]}
/>
*Palette and Saturation — simulated result across source images.*
**Source**: A colorful still life — fruit, flowers, or painted objects — with a wide range of hues and smooth tonal gradients.

**What You'll Create**: Explore luminance quantization and chroma saturation boost to achieve the flat, vivid look of fired enamel.

1. **Coarse palette**: Set Palette to step 1 (8 levels). The image collapses into broad flat regions — each cell is a single uniform tone.
2. **Fine palette**: Step through positions 2–8 and observe how the tonal staircase becomes finer. At step 4 (64 levels), the quantization is subtle but still visible in smooth gradients.
3. **Saturation boost**: Increase Gloss (pot 4) from 0% to 100%. Watch the colors intensify — reds become richer, blues deeper, greens more vivid. This is the vitreous enamel character.
4. **Warm palette**: Switch Style from Cloisonné to Basse-taille (gold wire, warm fill). The overall palette shifts toward amber and orange.
5. **Cool palette**: Switch Style to Champlevé (gold wire, cool fill). The same image takes on a cooler, bluer quality.
6. **Compare**: Toggle Bypass rapidly to compare the processed image to the original.

**Key concepts**: Bit-mask quantization, posterization levels, chroma push from midpoint, warm/cool palette temperature shift

---

### Exercise 3: Gloss and Animation

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: enamel_source1_parrot, after: enamel_ex3_s1 },
    { label: "Cat", before: enamel_source2_cat, after: enamel_ex3_s2 },
    { label: "Collage", before: enamel_source3_collage, after: enamel_ex3_s3 },
    { label: "Pattern", before: enamel_source4_pattern, after: enamel_ex3_s4 },
    { label: "Woman", before: enamel_source5_woman, after: enamel_ex3_s5 },
    { label: "Paint", before: enamel_source6_paint, after: enamel_ex3_s6 },
  ]}
/>
*Gloss and Animation — simulated result across source images.*
**Source**: High-contrast footage with large uniform areas — architecture, signage, or geometric patterns — where surface effects will be clearly visible.

**What You'll Create**: Enable gloss and animation to simulate the reflective surface of polished enamelwork.

1. **Prepare**: Set a moderate wire network (Wire W ~50%, Edge Thr ~30%) and coarse palette (step 2, 16 levels).
2. **Enable gloss**: Switch the Gloss toggle (toggle 9) to On. Observe the subtle brightness ripple across fill regions.
3. **Increase gloss intensity**: Slowly increase Wire Hue from 0° toward 360°. The shimmer pattern becomes more pronounced — bright highlights and darker patches alternate across the enamel surface.
4. **Wire animation**: Switch Video Pal to On. Watch the wire boundaries begin to sparkle — the shimmer travels along the wires frame by frame.
5. **Combined effect**: Enable both gloss and animation via the Wire Color toggle (Black position). The entire surface comes alive with shifting highlights.
6. **Gold vs. dark wire**: Toggle between Style positions. Gold wire with animation produces a rich, gilded look; dark wire with animation creates a more subtle, engraved effect.
7. **Mix down**: Slowly reduce the Mix fader to ~50%. The enamel effect becomes a semi-transparent overlay on the original image.

**Key concepts**: Position-based XOR gloss pattern, frame-counter wire shimmer, gloss amount scaling, dry/wet interpolation

---


## Tips

- **Saturation is your glaze**: The Gloss knob (pot 4) boosts chroma saturation, not surface gloss. Increasing it mimics the vivid color of fired vitreous enamel — the higher the boost, the more jewel-toned the fill.
- **Style presets are combinatorial**: The four Style positions permute two independent binary choices (gold/dark wire × warm/cool palette). Experiment with all four to find the aesthetic temperature that suits your source material.
- **Gloss needs coarse fill**: The position-based gloss shimmer is most visible on large, uniform fill regions created by low Palette steps. With fine quantization (step 7–8), the gloss pattern is masked by the surviving tonal detail.
- **Mix for overlay effects**: At 40–60% mix, the enamel effect becomes a semi-transparent layer over the original video, creating a subtle illustrative treatment that preserves depth and detail.
- **Feedback loops**: Route the output back to the input to create recursive enamel — wire boundaries compound and fill regions re-quantize, producing increasingly abstract mosaic structures over successive passes.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chroma** | The color information in a video signal, encoded as U and V components centered on midpoint 512 in 10-bit YUV color space. |
| **Cloisonné** | A decorative enamel technique using thin metal wire to form enclosed cells (cloisons) filled with vitreous glass paste. |
| **Edge Detection** | Identification of sharp luminance transitions in an image by computing the gradient (rate of change) between neighboring pixels. |
| **Gradient** | The magnitude of brightness change between adjacent pixels; the basis for wire/fill classification in Enamel's processing pipeline. |
| **Line Buffer** | A single-line delay implemented in BRAM that stores one horizontal line of video data, enabling vertical pixel comparisons. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color. |
| **Posterization** | Reducing the number of distinct tonal levels in an image by masking lower bits, creating flat bands of uniform brightness. |
| **Quantization** | Mapping a continuous range of values to a smaller set of discrete levels; Enamel quantizes Y via bit-shift masking. |
| **Saturation** | The intensity or purity of a color; Enamel boosts saturation by pushing U and V values away from neutral midpoint. |
| **Vitreous Enamel** | A glassy coating made from powdered glass fused to a metal surface by firing; characterized by vivid, opaque color and a glossy finish. |
| **XOR** | Exclusive OR; a bitwise operation used in Enamel to generate quasi-periodic patterns for gloss shimmer and wire animation. |

---
