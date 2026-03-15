---
draft: true
sidebar_position: 154
slug: /instruments/videomancer/kaledos
title: "Kaledos"
image: /img/instruments/videomancer/kaledos/kaledos_hero_s1.png
description: "In 1816, the Scottish physicist Sir David Brewster patented the kaleidoscope — a tube of mirrors that transforms a handful of colored fragments into an infinite tiling of perfect symmetry."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import kaledos_control_panel from '/img/instruments/videomancer/kaledos/kaledos_control_panel.png';
import kaledos_source1_ballerina from '/img/instruments/videomancer/kaledos/kaledos_source1_ballerina.png';
import kaledos_source2_field from '/img/instruments/videomancer/kaledos/kaledos_source2_field.png';
import kaledos_source3_collage from '/img/instruments/videomancer/kaledos/kaledos_source3_collage.png';
import kaledos_source4_pattern from '/img/instruments/videomancer/kaledos/kaledos_source4_pattern.png';
import kaledos_source5_boy from '/img/instruments/videomancer/kaledos/kaledos_source5_boy.png';
import kaledos_source6_wood from '/img/instruments/videomancer/kaledos/kaledos_source6_wood.png';
import kaledos_hero_s1 from '/img/instruments/videomancer/kaledos/kaledos_hero_s1.png';
import kaledos_hero_s2 from '/img/instruments/videomancer/kaledos/kaledos_hero_s2.png';
import kaledos_hero_s3 from '/img/instruments/videomancer/kaledos/kaledos_hero_s3.png';
import kaledos_hero_s4 from '/img/instruments/videomancer/kaledos/kaledos_hero_s4.png';
import kaledos_hero_s5 from '/img/instruments/videomancer/kaledos/kaledos_hero_s5.png';
import kaledos_hero_s6 from '/img/instruments/videomancer/kaledos/kaledos_hero_s6.png';
import kaledos_ex1_s1 from '/img/instruments/videomancer/kaledos/kaledos_ex1_s1.png';
import kaledos_ex1_s2 from '/img/instruments/videomancer/kaledos/kaledos_ex1_s2.png';
import kaledos_ex1_s3 from '/img/instruments/videomancer/kaledos/kaledos_ex1_s3.png';
import kaledos_ex1_s4 from '/img/instruments/videomancer/kaledos/kaledos_ex1_s4.png';
import kaledos_ex1_s5 from '/img/instruments/videomancer/kaledos/kaledos_ex1_s5.png';
import kaledos_ex1_s6 from '/img/instruments/videomancer/kaledos/kaledos_ex1_s6.png';
import kaledos_ex2_s1 from '/img/instruments/videomancer/kaledos/kaledos_ex2_s1.png';
import kaledos_ex2_s2 from '/img/instruments/videomancer/kaledos/kaledos_ex2_s2.png';
import kaledos_ex2_s3 from '/img/instruments/videomancer/kaledos/kaledos_ex2_s3.png';
import kaledos_ex2_s4 from '/img/instruments/videomancer/kaledos/kaledos_ex2_s4.png';
import kaledos_ex2_s5 from '/img/instruments/videomancer/kaledos/kaledos_ex2_s5.png';
import kaledos_ex2_s6 from '/img/instruments/videomancer/kaledos/kaledos_ex2_s6.png';
import kaledos_ex3_s1 from '/img/instruments/videomancer/kaledos/kaledos_ex3_s1.png';
import kaledos_ex3_s2 from '/img/instruments/videomancer/kaledos/kaledos_ex3_s2.png';
import kaledos_ex3_s3 from '/img/instruments/videomancer/kaledos/kaledos_ex3_s3.png';
import kaledos_ex3_s4 from '/img/instruments/videomancer/kaledos/kaledos_ex3_s4.png';
import kaledos_ex3_s5 from '/img/instruments/videomancer/kaledos/kaledos_ex3_s5.png';
import kaledos_ex3_s6 from '/img/instruments/videomancer/kaledos/kaledos_ex3_s6.png';

# Kaledos

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: kaledos_source1_ballerina, after: kaledos_hero_s1 },
    { label: "Field", before: kaledos_source2_field, after: kaledos_hero_s2 },
    { label: "Collage", before: kaledos_source3_collage, after: kaledos_hero_s3 },
    { label: "Pattern", before: kaledos_source4_pattern, after: kaledos_hero_s4 },
    { label: "Boy", before: kaledos_source5_boy, after: kaledos_hero_s5 },
    { label: "Wood", before: kaledos_source6_wood, after: kaledos_hero_s6 },
  ]}
/>
*Kaledos splitting a cathedral window into twelve-fold crystalline symmetry, each sector tinted by per-sector hue rotation through the full color wheel.*

---

## Overview

In 1816, the Scottish physicist Sir David Brewster patented the kaleidoscope — a tube of mirrors that transforms a handful of colored fragments into an infinite tiling of perfect symmetry. The principle is simple: place two or more mirrors at an angle, and the reflections multiply whatever lies between them into a radially symmetric pattern. The number of reflections depends on the angle; narrower angles produce higher-fold symmetry.

Kaledos applies this principle to live video. It captures a narrow sector of the input image into a line buffer RAM, then tiles the screen by reading that buffer forward and backward across alternating strips. The result is a real-time kaleidoscope that transforms any video source into crystalline symmetry patterns. The fold count — selectable from 2 to 24 via an 8-preset lookup table — determines how many virtual mirrors divide the frame. A rotation DDS continuously advances the sector offset, spinning the kaleidoscopic pattern. Center X and Y position both the source capture region and the vignette center, linking the geometric origin of the pattern to the visual focus of the mask.

Three decorative features extend the basic mirror. Per-sector hue rotation shifts the UV channels by 90° per sector, creating rainbow-tinted reflections that recall the colored glass fragments in Brewster's original instrument. A vignette darkens the image edges using Manhattan-distance falloff from the center point. A circular mask cuts the output to a disc, recreating the experience of peering through the eyepiece of a physical kaleidoscope tube.

---

## Quick Start

1. **Low folds for recognition**: At 2- or 3-fold symmetry, the source video is still recognizable — faces become Rorschach-like symmetric masks. Use this for portraiture effects.
2. **High folds for abstraction**: At 16 or 24 folds, even simple source material becomes an abstract geometric lattice. Feed in slow-moving footage for hypnotic textures.
3. **Hue Rotate needs color input**: Hue rotation permutes the UV channels, so it only produces visible results with saturated source material. Monochrome or desaturated input shows no change when Hue Rotate is toggled.

---

## Background

### The Kaleidoscope

David Brewster's 1816 patent described an optical instrument using two or more inclined mirrors inside a tube. Objects placed at one end are reflected back and forth between the mirrors, producing a symmetric pattern visible through the eyepiece at the other end. The key insight is that the symmetry order depends on the angle between the mirrors: two mirrors at 60° produce six-fold symmetry, at 45° produce eight-fold, and so on. Brewster explored both "polycentral" configurations (multiple mirror pairs creating infinite tiling) and "annular" configurations (concentric ring patterns). Kaledos implements the polycentral variant, where repeated horizontal strips tile the screen in a grid pattern with diamond-offset rows.

### Reflective Symmetry and Strip Mirroring

True angular kaleidoscope symmetry requires polar-to-Cartesian coordinate transformation — computationally expensive in FPGA. Kaledos approximates this with a simpler technique: it divides the horizontal and vertical screen dimensions into strips of equal width, then mirrors alternate strips. The horizontal mirroring creates bilateral symmetry along each vertical strip boundary; the vertical strip counter creates a second axis of symmetry. The diamond-pattern half-strip offset on alternate rows breaks the rectangular grid alignment, creating a more organic tiling that approximates the hexagonal geometry of a real kaleidoscope. The approximation works well because the visual coherence of natural video fills the gaps — the brain perceives radial symmetry even though the underlying geometry is rectilinear.

### Line-Buffer Architecture

Kaledos captures one horizontal sector of the input video into three 1024-entry Block RAMs (one each for Y, U, and V channels). The capture region is centered on the Center X position and spans one strip width. During readout, the buffer address either counts forward (for even-numbered strips) or backward (for odd-numbered strips in mirror mode), producing the mirrored reflection. The zoom control applies power-of-two address scaling — shifting the read address right by 0, 1, 2, or 3 bits, effectively magnifying the captured sector by 1×, 2×, 4×, or 8×. Because the buffer is re-read every line, the kaleidoscope pattern repeats identically on every scanline within a vertical strip.

### Hue Rotation as Colored Glass

In a physical kaleidoscope, colored glass or crystal fragments give each sector a different tint. Kaledos creates this effect digitally by rotating the UV chroma channels by 90° per sector. The rotation is implemented as a simple permutation of the U and V values based on the sector index modulo 4: sector 0 passes U and V unchanged, sector 1 swaps them with a V inversion, sector 2 inverts both, and sector 3 swaps with a U inversion. This four-step cycle covers the full 360° of the UV color wheel, so a four-fold or higher kaleidoscope displays the complete hue spectrum across its sectors.

### Vignette and Circular Mask

Two masking features recreate the physical experience of viewing through a kaleidoscope tube. The vignette computes a Manhattan-distance metric from each pixel to the center point: |Δx| + |Δy|. This distance is subtracted from a maximum value and used to scale the Y channel, creating a smooth brightness falloff from center to edge. The circular mask uses an octagonal distance approximation — max(|Δx|, |Δy|) + min(|Δx|, |Δy|)/2 — which closely approximates Euclidean distance using only integer addition and shifting. Pixels beyond the mask radius are replaced with black. The two features can be combined: vignette provides gradual darkening, and the circular mask provides a hard cutoff, mimicking the aperture of an eyepiece.


---

## Signal Flow

Configuration → Strip Counters → BRAM Write → ... → Pipeline Stage 4: → Interpolator

```
Input Video (YUV 4:4:4)
│
├── Configuration (per-frame) ──────────────────────────────────
│   ├─ Fold index → strip width/height from LUT
│   ├─ Center X/Y → pixel coordinates
│   ├─ Source start = Center X − strip_width/2
│   └─ Rotation DDS → start_offset (mod strip_width)
│
├── Strip Counters ─────────────────────────────────────────────
│   ├─ h_local: pixel within horizontal strip (wraps at strip_w)
│   ├─ h_strip: which horizontal strip (increments at wrap)
│   ├─ v_local: scanline within vertical strip (wraps at strip_h)
│   ├─ v_strip: which vertical strip
│   └─ Diamond offset: odd v_strips shift h_local by strip_w/2
│
├── BRAM Write ─────────────────────────────────────────────────
│   └─ Capture source sector [src_start..src_start+strip_w]
│       into Y/U/V line RAMs
│
├── Pipeline Stage 1: Mirror + Zoom → Read Address ─────────────
│   ├─ Mirror: odd h_strips read address = strip_w − 1 − h_local
│   ├─ Zoom: shift right by 0/1/2/3 (1×/2×/4×/8×)
│   └─ Sector index = h_strip + v_strip
│
├── Pipeline Stage 2: BRAM Read ────────────────────────────────
│   └─ Read Y/U/V from line RAM at computed address
│
├── Pipeline Stage 3: Hue Rotation + Vignette Distance ─────────
│   ├─ Per-sector 90° UV permutation (sector mod 4)
│   ├─ Manhattan vignette distance = |Δx| + |Δy|
│   └─ Octagonal mask distance = max(|Δx|,|Δy|) + min/2
│
├── Pipeline Stage 4: Vignette + Circle Mask → Output ──────────
│   ├─ Y × vignette_factor (linear falloff from 1023)
│   └─ If mask_dist ≥ 360: output = black
│
├── Interpolator (4 clk) ──────────────────────────────────────
│   └─ Wet/dry mix per Y, U, V channel
│
└── Output: bypass mux → data_out
```

The BRAM write and display readout operate on the same scanline — the line buffer captures the source sector during the current line, and the pipeline reads back from the same buffer with potentially different addresses. Because the read address is computed from the strip counter (not the raw pixel position), every strip reads the same captured sector, producing the tiled pattern. The zoom control scales the read address by powers of two, magnifying the captured content. The rotation DDS increments the start offset each frame, causing the strip counters to begin at a progressively shifted position and making the whole kaleidoscope pattern rotate.

---

## Parameter Reference

<img src={kaledos_control_panel} alt="Videomancer front panel with Kaledos loaded"/>
*Videomancer's front panel with Kaledos active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Fold Count
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 2 |

Selects the number of symmetry folds from an 8-preset lookup table: 2, 3, 4, 6, 8, 12, 16, or 24. Each preset determines the strip width and height that divide the 1280×720 active area. Low fold counts produce large, bold reflections with easily recognizable source content. High fold counts create dense lattice patterns where the source material fragments into abstract crystalline textures. The transition between presets is instantaneous — each fold count completely reconfigures the strip geometry.

---

#### Knob 2 — Sector Ofs
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Rotates which angular sector of the source image is captured into the line buffer. The offset is added to the rotation DDS accumulator, so it acts as a phase shift on the kaleidoscope pattern. Sweeping this control manually rotates the pattern in discrete steps. Combined with Rot Speed (knob 4), the sector offset sets the starting phase of the continuous rotation animation.

---

#### Knob 3 — Zoom
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the zoom magnification of the captured sector. The zoom is implemented as power-of-two address scaling — the pot value selects between 1×, 2×, 4×, and 8× magnification in four discrete steps. At 1× the full captured strip width is visible; at 8× only the central eighth is magnified to fill each strip, creating a highly zoomed, abstract pattern. Because the scaling is by bit-shifting, the zoom steps are coarse and distinct rather than continuously variable.

---

#### Knob 4 — Rot Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the speed of the continuous rotation animation. A DDS phase accumulator increments by a scaled value derived from this pot on each vsync pulse. At 0% the pattern is static (manual control only via Sector Ofs). Increasing the value makes the kaleidoscope spin faster. The rotation speed interacts with the fold count — higher fold counts produce visually faster rotation because each strip is narrower and traverses its content sooner.

---

#### Knob 5 — Center X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the horizontal center of the source capture region and the vignette/mask center point. At 50% the capture and vignette are centered on the screen. Moving left or right shifts which part of the input video is captured into the kaleidoscope, changing the source material that gets reflected. The same value determines the vignette center, so the brightness falloff and circular mask track the capture region.

---

#### Knob 6 — Center Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the vertical center for the vignette and circular mask. Unlike Center X, this control does not affect which scanline is captured (the line buffer always reads the current scanline). Instead, it moves the origin point for the vignette distance calculation and circular mask, shifting the brightness falloff pattern up or down on the screen.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Hue Rotate** | Off | On |
| **8 — Vignette** | Off | On |
| **9 — Circle Mask** | Off | On |
| **10 — Mirror/Rot** | Mirror | Rotate |
| **11 — Bypass** | Off | On |

The five toggles control decorative features and mode selection. Hue Rotate, Vignette, and Circle Mask are independent additive effects that can be combined freely. Mirror/Rot selects the fundamental reflection behavior — mirroring creates bilateral symmetry (the classic kaleidoscope look), while rotation repeats the sector without flipping, creating a pinwheel pattern. Bypass routes the input directly to the output for A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Kaledos processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Kaledos-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from simple mirroring through decorative features to complex animated kaleidoscope compositions. Each builds on the previous, gradually engaging more of the effect's capabilities.

### Exercise 1: Basic Mirror Symmetry

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: kaledos_source1_ballerina, after: kaledos_ex1_s1 },
    { label: "Field", before: kaledos_source2_field, after: kaledos_ex1_s2 },
    { label: "Collage", before: kaledos_source3_collage, after: kaledos_ex1_s3 },
    { label: "Pattern", before: kaledos_source4_pattern, after: kaledos_ex1_s4 },
    { label: "Boy", before: kaledos_source5_boy, after: kaledos_ex1_s5 },
    { label: "Wood", before: kaledos_source6_wood, after: kaledos_ex1_s6 },
  ]}
/>
*Basic Mirror Symmetry — simulated result across source images.*
**Source**: A live camera pointed at a face, hand, or detailed object. High-contrast subjects work best.

**What You'll Create**: Explore how fold count and mirror mode transform a video source into symmetric patterns.

1. **Two-fold mirror**: Set Fold Count to the first step (2-fold). The screen splits into two halves — the right half is a mirror image of the left. Recognize the source content flipped along the center line.
2. **Increase folds**: Step through fold presets: 4, 6, 8. Watch the source fragment into progressively more reflections. At 8-fold, the original content becomes abstract.
3. **High folds**: Jump to 16 or 24. The pattern becomes a dense lattice of tiny repeated tiles. Source detail is barely recognizable.
4. **Sector offset**: Sweep knob 2 to rotate which part of the source feeds the kaleidoscope. The pattern shifts as different parts of the image enter the capture sector.
5. **Center X**: Move knob 5 to shift the capture region left and right. Different source content enters the reflections.
6. **Try Rotate mode**: Toggle Mirror/Rot to Rotate. The bilateral symmetry disappears, replaced by a pinwheel of repeated (non-mirrored) sectors.

**Key concepts**: Fold count determines the number of virtual mirrors, mirror mode creates bilateral symmetry at strip boundaries, sector offset selects which source region is captured

---

### Exercise 2: Colored Glass Kaleidoscope

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: kaledos_source1_ballerina, after: kaledos_ex2_s1 },
    { label: "Field", before: kaledos_source2_field, after: kaledos_ex2_s2 },
    { label: "Collage", before: kaledos_source3_collage, after: kaledos_ex2_s3 },
    { label: "Pattern", before: kaledos_source4_pattern, after: kaledos_ex2_s4 },
    { label: "Boy", before: kaledos_source5_boy, after: kaledos_ex2_s5 },
    { label: "Wood", before: kaledos_source6_wood, after: kaledos_ex2_s6 },
  ]}
/>
*Colored Glass Kaleidoscope — simulated result across source images.*
**Source**: Footage with moderate color saturation — flowers, stained glass, or colored fabric. Color variety in the source makes the hue rotation more dramatic.

**What You'll Create**: Combine hue rotation, vignette, and circular mask to recreate the full kaleidoscope-tube experience.

1. **Set 6- or 8-fold symmetry**: Choose a fold count that creates a clear, recognizable pattern.
2. **Enable Hue Rotate**: Toggle Hue Rotate On. Each sector takes on a different color cast — the kaleidoscope now shows rainbow-tinted reflections.
3. **Enable Vignette**: Toggle Vignette On. The edges darken, drawing the eye to the center of the pattern.
4. **Enable Circle Mask**: Toggle Circle Mask On. The rectangular frame cuts to a disc. The combination of vignette + circle mask closely resembles peering through a real kaleidoscope tube.
5. **Adjust Center Y**: Move knob 6 to shift the vignette and mask center. Notice how the circular aperture moves vertically while the kaleidoscope pattern stays anchored to the horizontal center.
6. **Zoom in**: Step the Zoom control to 2× or 4×. The captured sector magnifies, filling each strip with a zoomed detail of the source.

**Key concepts**: Hue rotation permutes UV channels per sector creating rainbow tinting, vignette provides gradual edge darkening, circular mask provides hard disc cutoff, all three features are independent and composable

---

### Exercise 3: Spinning Kaleidoscope

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: kaledos_source1_ballerina, after: kaledos_ex3_s1 },
    { label: "Field", before: kaledos_source2_field, after: kaledos_ex3_s2 },
    { label: "Collage", before: kaledos_source3_collage, after: kaledos_ex3_s3 },
    { label: "Pattern", before: kaledos_source4_pattern, after: kaledos_ex3_s4 },
    { label: "Boy", before: kaledos_source5_boy, after: kaledos_ex3_s5 },
    { label: "Wood", before: kaledos_source6_wood, after: kaledos_ex3_s6 },
  ]}
/>
*Spinning Kaleidoscope — simulated result across source images.*
**Source**: Any dynamic video — camera footage, animation, or generative video from another Videomancer program chained upstream.

**What You'll Create**: Engage continuous rotation to create a spinning kaleidoscope effect, then combine with all decorative features for a complete kinetic composition.

1. **Start rotation**: Increase Rot Speed from 0%. The kaleidoscope pattern begins to spin slowly as the sector offset auto-advances.
2. **Find a pleasing speed**: Adjust Rot Speed until the rotation is smooth and hypnotic — not so fast that the pattern blurs, not so slow that it appears static.
3. **Add hue rotation**: Enable Hue Rotate. The rainbow colors now rotate with the pattern, creating a spinning stained-glass window effect.
4. **Add mask**: Enable both Vignette and Circle Mask. The spinning pattern is framed within a dark-edged disc.
5. **Zoom and fold**: Try changing fold count while the pattern spins. Higher folds spin visually faster because each strip is narrower.
6. **Mix blend**: Pull the Mix fader to about 60%. The spinning kaleidoscope overlays the source video as a translucent mandala.

**Key concepts**: Rotation DDS advances the sector offset each frame, rotation speed interacts with fold count (higher folds = visually faster spin), all decorative features combine with rotation for layered compositions

---


## Tips

- **Zoom magnifies noise**: At 4× or 8× zoom, small details and noise in the source become large, prominent features in the kaleidoscope. Use clean, high-quality source material for high zoom levels.
- **Combine vignette and mask**: Vignette alone provides gentle darkening. Circle Mask alone provides a hard disc cutoff. Together they create the most convincing kaleidoscope-tube look — gradual falloff into a defined circular aperture.
- **Rotation speed and fold count interact**: Higher fold counts make the same DDS speed produce visually faster rotation because each strip is narrower. Reduce Rot Speed when increasing fold count to maintain the same apparent rotation rate.
- **Feedback for infinite depth**: Route the output back to the input. The kaleidoscope reflects its own reflections, creating recursive symmetry patterns — an electronic Droste effect that evolves over time.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bilateral Symmetry** | Mirror symmetry across an axis; each side is a reversed copy of the other. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms by incrementing a phase accumulator, here used to drive continuous rotation. |
| **Fold Count** | The number of symmetry axes in the kaleidoscope pattern; higher counts produce denser, more abstract reflections. |
| **Hue Rotation** | Shifting color angle by permuting the U and V chroma channels; 90° rotation cycles through complementary colors. |
| **Manhattan Distance** | The sum of absolute horizontal and vertical differences: |Δx| + |Δy|. Cheaper to compute than Euclidean distance; used for the vignette falloff. |
| **Octagonal Distance** | An approximation to Euclidean distance using max(|Δx|, |Δy|) + min(|Δx|, |Δy|)/2; used for the circular mask. |
| **Strip** | A rectangular subdivision of the screen; the fundamental repeating unit of the kaleidoscope tiling pattern. |
| **Vignette** | Gradual brightness reduction from center to edges, simulating the peripheral light falloff of an optical system. |

---
