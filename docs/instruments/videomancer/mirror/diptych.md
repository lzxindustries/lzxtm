---
draft: true
sidebar_position: 80
slug: /instruments/videomancer/diptych
title: "Diptych"
image: /img/instruments/videomancer/diptych/diptych_hero.png
description: "A diptych is a two-panel artwork — two images joined along a central hinge."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import diptych_hero from '/img/instruments/videomancer/diptych/diptych_hero.png';
import diptych_control_panel from '/img/instruments/videomancer/diptych/diptych_control_panel.png';
import diptych_exercise1_result from '/img/instruments/videomancer/diptych/diptych_exercise1_result.png';
import diptych_exercise2_result from '/img/instruments/videomancer/diptych/diptych_exercise2_result.png';
import diptych_exercise3_result from '/img/instruments/videomancer/diptych/diptych_exercise3_result.png';
import diptych_source1_kodim01 from '/img/instruments/videomancer/diptych/diptych_source1_kodim01.png';
import diptych_source2_kodim02 from '/img/instruments/videomancer/diptych/diptych_source2_kodim02.png';
import diptych_source3_kodim01_bw from '/img/instruments/videomancer/diptych/diptych_source3_kodim01_bw.png';

# Diptych

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: diptych_source1_kodim01, after: diptych_hero },
    { label: "Kodim02", before: diptych_source2_kodim02, after: diptych_hero },
    { label: "Kodim01 B&W", before: diptych_source3_kodim01_bw, after: diptych_hero },
  ]}
/>
*Diptych splitting a live camera feed at mid-frame with complementary color inversion on the mirrored half and a narrow black gap at the fold line.*

---

## Overview

A diptych is a two-panel artwork — two images joined along a central hinge. Diptych applies the same idea to live video: it splits the frame at an adjustable point and applies complementary color inversion to one half, creating a bilateral fold where left and right are chromatic opposites. The name comes directly from the Greek *diptykhos* ("folded in two"), acknowledging both the art form and the literal folding of the color space around the split line.

The program does not spatially mirror pixels — it has no line buffer for address remapping. Instead, it achieves the visual impression of a mirror by inverting the U and V chroma channels on one side of the split. Because YUV chroma inversion maps every color to its complement (red ↔ cyan, blue ↔ yellow, green ↔ magenta), the two halves of the frame appear as chromatic reflections of each other. The Vertical toggle extends the inversion to the Y (luminance) channel, producing a full negative image on the mirrored side.

At default settings (split at center, no gap), Diptych produces a clean bilateral split with complementary color halves. Sweeping the Split Point slider shifts the fold line across the frame. Adding gap width inserts a black divider at the fold, and the Mix fader controls the blend between processed and dry signal.

---

## Background

### The Diptych Art Form

The diptych — two panels hinged together — is one of the oldest formats in Western art. Roman writing tablets, Byzantine ivory carvings, and medieval altarpieces all used the paired-panel structure. The format implies dialogue: left panel and right panel comment on each other through juxtaposition. In video art, the diptych structure appears whenever the frame is split into two related but distinct fields — a compositional device that Diptych makes available as a real-time processing tool.

### Bilateral Symmetry in Nature and Design

Bilateral symmetry — mirror-image correspondence across a central axis — is one of the most fundamental organizational patterns in biology. Nearly all animals exhibit it. Human perception is tuned to detect bilateral symmetry rapidly and automatically, which is why mirror effects in video feel immediately striking. Diptych's chroma inversion creates a *chromatic* bilateral symmetry: the spatial content remains continuous, but the color field reflects across the split line.

### Mirror Effects in Analog Video Art

Hardware video mirrors have a long history in the video art tradition. Early analog mirror effects required frame stores or delay lines to read pixel addresses in reverse order. Diptych takes a computationally simpler approach — rather than spatially reversing pixels, it inverts the color channels. The visual result suggests a mirror because complementary colors create a strong sense of opposition and reflection, even without spatial reversal.

### Rorschach Symmetry

The Rorschach inkblot test relies on bilateral symmetry to create ambiguous, projective images. When Diptych is applied to organic or abstract source material, the complementary color split creates a similar effect — the viewer perceives meaningful patterns in the symmetric opposition between the two color fields. This is especially pronounced when the split point is centered and the source contains complex textures.

### Nam June Paik and the Video Mirror

Nam June Paik's early video sculptures frequently employed electronic mirrors — circuits that processed the video signal to create reflections, inversions, and chromatic transformations. Paik understood that the mirror is not merely a spatial operation but a *transformation* of the image's identity. Diptych follows this lineage: the "mirror" is a color-space transformation rather than a geometric one, altering what the image *means* rather than where its pixels *are*.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Timing Detection ───────────────────────────────────────────
│   ├─ hsync/vsync edge detection
│   ├─ x_counter (pixel position within scanline)
│   └─ y_counter (line number within field)
│
├── Split Computation ──────────────────────────────────────────
│   ├─ v_split = split_point + 128
│   ├─ v_gap_half = gap_width >> 3
│   └─ v_in_gap = (x in [split-gap .. split+gap]) and gap > 0
│
├── Channel Processing ─────────────────────────────────────────
│   ├─ Gap region (v_in_gap = 1):
│   │   Y = 0 (black), U = 512 (neutral), V = 512 (neutral)
│   ├─ Right of split (x > v_split, normal mode):
│   │   U = NOT(U), V = NOT(V)  ← chroma complement
│   │   Y = NOT(Y) if Vertical toggle on, else passthrough
│   └─ Left of split:
│   │   Y, U, V passthrough
│   (Reverse toggle: flips which side receives inversion)
│
├── Wet/Dry Mix ────────────────────────────────────────────────
│   ├─ interpolator_u × 3 (Y, U, V)
│   └─ Mix fader blends processed ↔ delayed dry signal
│
├── Sync Delay Pipeline ────────────────────────────────────────
│   └─ 8-clock shift register for hsync, vsync, field, Y, U, V
│
└── Output Assignment ──────────────────────────────────────────
    ├─ Bypass off: mix result → output
    └─ Bypass on: delayed dry signal → output
```

The core of Diptych is a spatial threshold: every pixel's horizontal position is compared against the split point, and pixels on one side receive a bitwise complement on their chroma channels. This is a per-pixel, per-clock operation with no memory — each pixel is processed independently based on its x-coordinate alone. The gap region overrides both sides, inserting black at the fold line. The 8-clock delay pipeline aligns the dry signal with the interpolator latency so that the wet/dry mix blends correctly time-aligned signals.

The Offset, Zoom, Tilt, Tint, Double, and Color Tint controls are declared as register-mapped signals in the VHDL but are not connected to the current processing pipeline. They are reserved for future expansion of the mirror geometry.

---

## Parameter Reference

<img src={diptych_control_panel} alt="Videomancer front panel with Diptych loaded"/>
*Videomancer's front panel with Diptych active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Split Point
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the horizontal position of the fold line. At 0% the split sits near the left edge of the active picture; at 100% it sits near the right edge. The VHDL maps the 10-bit register to screen coordinates as `split = register + 128`, placing the default 50% (register 512) at pixel 640 — approximately mid-frame in a 1280-pixel HD line. Sweeping this control slides the boundary between the normal and color-inverted halves of the image.

---

#### Knob 2 — Gap Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the width of the black gap inserted at the fold line. At 0% (register 0) there is no gap — the normal and inverted halves meet directly. As the value increases, a symmetrical band of black pixels appears centered on the split point. The gap half-width is computed as `register >> 3`, giving a maximum gap of approximately 128 pixels on each side of the split. The gap region outputs Y = 0 with neutral chroma (U = V = 512).

---

#### Knob 3 — Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Offset control. This parameter is mapped to a register and declared in the VHDL signal list, but it is not connected to any processing stage in the current pipeline. It is reserved for future use — potentially shifting the read address on the mirrored side to create a spatial offset from the fold line. Adjusting this control has no visible effect on the output.

---

#### Knob 4 — Zoom
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Zoom control. Like Offset, this parameter is declared but not active in the current VHDL implementation. It is reserved for future magnification or scaling of the mirrored region. Adjusting this control has no visible effect on the output.

---

#### Knob 5 — Tilt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Tilt control. Declared but inactive. Reserved for future angular rotation of the fold axis — potentially allowing diagonal or angled mirror lines. Adjusting this control has no visible effect on the output.

---

#### Knob 6 — Tint
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Tint control. Declared but inactive. Reserved for future colorization of the mirrored region — potentially applying a hue offset to the inverted chroma. Adjusting this control has no visible effect on the output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Vertical** | Off | On |
| **8 — Double** | Off | On |
| **9 — Reverse** | Off | On |
| **10 — Color Tint** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–11 control five binary options. Vertical extends the mirror inversion to the luminance channel. Double and Color Tint are declared but inactive in the current pipeline. Reverse flips which side receives the inversion. Bypass routes the dry signal directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry mix between the processed and original signal. At 100% (register 1023), the output is fully processed — the split, gap, and inversion are fully visible. At 0% (register 0), the output is the original unprocessed signal. Intermediate values blend between the two, creating a ghost-like overlay of the inverted half over the original. This is implemented by three parallel interpolator instances (one per YUV channel) that linearly crossfade between the delayed dry input and the processed output.

---

## Guided Exercises

These exercises explore split positioning, gap insertion, and chroma/luma inversion — progressing from a simple bilateral color fold to a full negative mirror with gap framing.

### Exercise 1: Bilateral Color Fold

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: diptych_source1_kodim01, after: diptych_exercise1_result },
    { label: "Kodim02", before: diptych_source2_kodim02, after: diptych_exercise1_result },
    { label: "Kodim01 B&W", before: diptych_source3_kodim01_bw, after: diptych_exercise1_result },
  ]}
/>
*Bilateral Color Fold — simulated result across source images.*
**Source**: A live camera feed or recorded footage with strong, varied colors — flowers, painted surfaces, or colorful clothing work well.

**Objective**: Understand how the split point divides the frame and how UV inversion creates complementary color opposition.

1. **Center split**: Confirm Split Point is at 50% (default). The frame divides into two halves — left with original colors, right with complementary colors.
2. **Sweep the split**: Slowly rotate Split Point from 0% to 100%. Watch the fold line slide across the frame. Notice how the inverted region grows or shrinks.
3. **Observe color opposition**: Red objects on the left appear cyan on the right. Blue becomes yellow. Green becomes magenta. The luminance remains identical on both sides.
4. **Add a gap**: Increase Gap Width to ~30%. A black stripe appears at the fold line, visually separating the two color fields like a hinge in a physical diptych.
5. **Compare with bypass**: Toggle Bypass to see the original image, then back to see the split.

**Key concepts**: UV inversion maps every color to its complement, split point controls the fold position, gap inserts a visual separator at the fold

---

### Exercise 2: Full Negative Mirror

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: diptych_source1_kodim01, after: diptych_exercise2_result },
    { label: "Kodim02", before: diptych_source2_kodim02, after: diptych_exercise2_result },
    { label: "Kodim01 B&W", before: diptych_source3_kodim01_bw, after: diptych_exercise2_result },
  ]}
/>
*Full Negative Mirror — simulated result across source images.*
**Source**: High-contrast footage with clear tonal structure — backlit subjects, architecture, or black-and-white patterns.

**Objective**: Explore the Vertical toggle to create a full negative on the mirrored side, and use Reverse to choose which half retains the original image.

1. **Set center split**: Split Point at 50%, Gap Width at 0%.
2. **Enable vertical**: Toggle Vertical on. Now the right half shows a full photographic negative — both brightness and color are inverted.
3. **Observe tonal reversal**: Black areas on the left become white on the right. Bright highlights become deep shadows. The inversion is total.
4. **Flip with reverse**: Toggle Reverse on. Now the *left* side is the negative and the right side is the original. This is useful for choosing which half of the composition retains natural appearance.
5. **Partial mix**: Lower Mix to ~50%. The negative and original blend together, creating a washed-out, low-contrast ghost image where dark and light regions cancel.

**Key concepts**: Y inversion creates a full photographic negative, reverse flips which side gets the inversion, partial mix blends the two halves

---

### Exercise 3: Framed Diptych Composition

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: diptych_source1_kodim01, after: diptych_exercise3_result },
    { label: "Kodim02", before: diptych_source2_kodim02, after: diptych_exercise3_result },
    { label: "Kodim01 B&W", before: diptych_source3_kodim01_bw, after: diptych_exercise3_result },
  ]}
/>
*Framed Diptych Composition — simulated result across source images.*
**Source**: A slowly panning camera or a static scene with a clear subject in the center.

**Objective**: Combine split positioning, gap width, and mix to create a composed diptych with a visible frame between the panels.

1. **Off-center split**: Set Split Point to ~35% so the original panel is narrower than the inverted panel, creating an asymmetric composition.
2. **Wide gap**: Increase Gap Width to ~50%. The black gap becomes a prominent visual frame between the two panels.
3. **Chroma only**: Leave Vertical off so the mirror is chromatic — both panels have the same luminance structure, differing only in color.
4. **Partial mix**: Set Mix to ~80% to let a hint of the original signal bleed through the inverted side, softening the color opposition.
5. **Slow sweep**: Slowly rotate Split Point while watching the composition shift. The gap tracks the split point, maintaining the frame.
6. **Reverse**: Toggle Reverse to see the composition with the inverted panel on the opposite side.

**Key concepts**: Asymmetric split creates unequal panel sizes, wide gap functions as a visual frame, partial mix softens the contrast between panels

---


## Tips

- **Color complements are automatic**: The UV inversion produces mathematically exact color complements — every hue maps to its opposite on the color wheel. No parameter tuning needed.
- **Gap as framing device**: A wide gap turns the effect from a split-screen into a framed diptych. Use it to create deliberate two-panel compositions.
- **Vertical for maximum contrast**: The Vertical toggle extends inversion to luminance, producing a full negative. This is the most dramatic setting — use it for high-impact visual contrast.
- **Reverse for composition control**: Reverse lets you choose which side of the frame retains the original image. Useful when the subject is not centered.
- **Mix for blending**: Partial mix values (40–60%) create ghostly overlays where complementary colors partially cancel, producing desaturated, low-contrast textures.
- **Neutral gray is invariant**: Mid-gray (Y=512, U=512, V=512) is unchanged by the inversion — the complement of neutral is neutral. Use this as a visual anchor.
- **Feedback creates kaleidoscope patterns**: Routing the output back to the input produces recursive complementary inversions that build complex color patterns over time.
- **Chain with other programs**: Diptych pairs well with spatial effects — follow it with a rotation or zoom program to create symmetrical mandala-like compositions.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bilateral Symmetry** | Mirror-image correspondence across a central axis; Diptych creates chromatic bilateral symmetry by inverting color channels on one side. |
| **Bitwise Complement** | The NOT operation: each bit in a binary value is flipped (0→1, 1→0). Applied to 10-bit video, value N becomes 1023−N. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Complementary Colors** | Color pairs that sit opposite each other on the color wheel; in YUV, swapping a chroma channel via NOT maps every hue to its complement. |
| **Diptych** | A two-panel artwork, historically hinged along a central fold; the namesake of this program. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interpolator** | A hardware module that linearly blends between two values based on a mix parameter; used here for wet/dry crossfading. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Split Point** | The horizontal pixel position at which the frame is divided into normal and inverted halves. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
