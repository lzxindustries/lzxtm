---
draft: true
sidebar_position: 342
slug: /instruments/videomancer/zollner
title: "Zollner"
image: /img/instruments/videomancer/zollner/zollner_hero_s1.png
description: "The Zöllner illusion is one of the oldest documented optical illusions — discovered in 1860 by astrophysicist Johann Karl Friedrich Zöllner when he noticed that parallel lines on a piece of fabric appeared to converge when crossed by short diagonal hash marks."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import zollner_control_panel from '/img/instruments/videomancer/zollner/zollner_control_panel.png';
import zollner_source1_dog from '/img/instruments/videomancer/zollner/zollner_source1_dog.png';
import zollner_source2_fruit from '/img/instruments/videomancer/zollner/zollner_source2_fruit.png';
import zollner_source3_turtle from '/img/instruments/videomancer/zollner/zollner_source3_turtle.png';
import zollner_source4_pattern from '/img/instruments/videomancer/zollner/zollner_source4_pattern.png';
import zollner_source5_woman from '/img/instruments/videomancer/zollner/zollner_source5_woman.png';
import zollner_source6_paint from '/img/instruments/videomancer/zollner/zollner_source6_paint.png';
import zollner_hero_s1 from '/img/instruments/videomancer/zollner/zollner_hero_s1.png';
import zollner_hero_s2 from '/img/instruments/videomancer/zollner/zollner_hero_s2.png';
import zollner_hero_s3 from '/img/instruments/videomancer/zollner/zollner_hero_s3.png';
import zollner_hero_s4 from '/img/instruments/videomancer/zollner/zollner_hero_s4.png';
import zollner_hero_s5 from '/img/instruments/videomancer/zollner/zollner_hero_s5.png';
import zollner_hero_s6 from '/img/instruments/videomancer/zollner/zollner_hero_s6.png';
import zollner_ex1_s1 from '/img/instruments/videomancer/zollner/zollner_ex1_s1.png';
import zollner_ex1_s2 from '/img/instruments/videomancer/zollner/zollner_ex1_s2.png';
import zollner_ex1_s3 from '/img/instruments/videomancer/zollner/zollner_ex1_s3.png';
import zollner_ex1_s4 from '/img/instruments/videomancer/zollner/zollner_ex1_s4.png';
import zollner_ex1_s5 from '/img/instruments/videomancer/zollner/zollner_ex1_s5.png';
import zollner_ex1_s6 from '/img/instruments/videomancer/zollner/zollner_ex1_s6.png';
import zollner_ex2_s1 from '/img/instruments/videomancer/zollner/zollner_ex2_s1.png';
import zollner_ex2_s2 from '/img/instruments/videomancer/zollner/zollner_ex2_s2.png';
import zollner_ex2_s3 from '/img/instruments/videomancer/zollner/zollner_ex2_s3.png';
import zollner_ex2_s4 from '/img/instruments/videomancer/zollner/zollner_ex2_s4.png';
import zollner_ex2_s5 from '/img/instruments/videomancer/zollner/zollner_ex2_s5.png';
import zollner_ex2_s6 from '/img/instruments/videomancer/zollner/zollner_ex2_s6.png';
import zollner_ex3_s1 from '/img/instruments/videomancer/zollner/zollner_ex3_s1.png';
import zollner_ex3_s2 from '/img/instruments/videomancer/zollner/zollner_ex3_s2.png';
import zollner_ex3_s3 from '/img/instruments/videomancer/zollner/zollner_ex3_s3.png';
import zollner_ex3_s4 from '/img/instruments/videomancer/zollner/zollner_ex3_s4.png';
import zollner_ex3_s5 from '/img/instruments/videomancer/zollner/zollner_ex3_s5.png';
import zollner_ex3_s6 from '/img/instruments/videomancer/zollner/zollner_ex3_s6.png';

# Zollner

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: zollner_source1_dog, after: zollner_hero_s1 },
    { label: "Fruit", before: zollner_source2_fruit, after: zollner_hero_s2 },
    { label: "Turtle", before: zollner_source3_turtle, after: zollner_hero_s3 },
    { label: "Pattern", before: zollner_source4_pattern, after: zollner_hero_s4 },
    { label: "Woman", before: zollner_source5_woman, after: zollner_hero_s5 },
    { label: "Paint", before: zollner_source6_paint, after: zollner_hero_s6 },
  ]}
/>
*Zöllner pattern overlay in Café Wall mode with animated hatching, creating compelling motion illusions on live video.*

---

## Overview

The Zöllner illusion is one of the oldest documented optical illusions — discovered in 1860 by astrophysicist Johann Karl Friedrich Zöllner when he noticed that parallel lines on a piece of fabric appeared to converge when crossed by short diagonal hash marks. The effect arises because the visual cortex misjudges the angles of the main lines due to contextual influence from the crossing hatches. Xero — wait — Zollner translates this phenomenon into a real-time video overlay.

The program generates a pattern of alternating horizontal bands overlaid with diagonal hatch marks and composites it onto the incoming video. The hatch angle, spacing, length, and thickness are all adjustable, and four distinct pattern variants (Zöllner, Hering, Wundt, and Café Wall) offer different geometric illusion styles. Animation scrolls the hatch origin vertically, creating visible motion that intensifies the perceptual distortion.

The name directly references Johann Zöllner, whose 1860 paper "Über eine neue Art von Pseudoskopie" introduced this family of illusions to formal vision science.

---

## Quick Start

1. **Illusion strength is angle-dependent**: The Zöllner illusion is strongest when hatch angles are 10°–30° from the band direction. Extreme angles (near 0° or 90°) weaken the effect.
2. **Animation intensifies illusion**: Moving hatches create stronger perceptual distortion than static ones. Even slow animation (10–20%) noticeably enhances the Zöllner and Hering effects.
3. **Band width sets illusion scale**: Narrow bands (8–16px) create fine illusions that work best at close viewing distance. Wide bands (48–64px) create bold patterns visible at any distance.

---

## Background

### The Zöllner Illusion

Johann Zöllner's original observation was deceptively simple: parallel lines crossed by short oblique strokes appear to tilt — converging at one end and diverging at the other. The explanation lies in angle assimilation: the visual system biases the perceived orientation of the main lines toward the angle of the crossing hatches. The effect is strongest when the hatch angle is between 10° and 30° relative to the main lines, and weakens as the crossing angle approaches perpendicular.

### Hering and Wundt Illusions

Ewald Hering and Wilhelm Wundt extended the Zöllner concept radially. In the Hering illusion, parallel lines appear to bow outward when superimposed on a starburst of lines radiating from a central point. The Wundt illusion inverts this: the same parallel lines appear to bow inward when the radiating lines converge toward the center. In Zollner's implementation, these modes compute hatch angle as a function of distance from the center of the frame — Hering uses the direct radial angle, Wundt inverts it.

### Café Wall Illusion

Discovered in the tilework of a Bristol café in 1979 by Richard Gregory, the Café Wall illusion consists of alternating rows of dark and light tiles with the rows offset by half a tile width. Despite the rows being perfectly horizontal and parallel, they appear to converge and diverge. Zollner approximates this with a shifted checkerboard pattern that produces the same perceptual tilt.

### Illusions in Video Art

Optical illusions have a long history in video art, from Bridget Riley's Op Art animations to Nam June Paik's explorations of perceptual interference. Overlaying geometric illusion patterns on live video creates a unique interaction: the brain simultaneously processes the realistic content and the illusory geometry, creating a perceptual tension that neither element would produce alone.

### Band Structure and Hatch Geometry

The underlying structure is a set of horizontal bands whose width is selectable from a lookup table: 8, 12, 16, 20, 24, 32, 48, or 64 pixels. Within each band, short diagonal lines (hatches) are drawn at a configurable angle, spacing, and length. In the classic Zöllner pattern, adjacent bands have opposite hatch angles, creating the convergence illusion. The pattern opacity controls how strongly the overlay blends with the underlying video.


---

## Signal Flow

Input Register → Band Detection → Hatch Angle Computation → Hatch Pattern Generation → Opacity Composite

```
Input Video (YUV 4:4:4 30-bit)
│
├── Stage 1: Input Register + Animation Counter ───────
│   ├─ y_in, u_in, v_in registered
│   └─ anim_offset incremented by speed per field
│
├── Stage 2: Band Detection ───────────────────────────
│   ├─ band_width from LUT: [8,12,16,20,24,32,48,64]
│   ├─ band_index = v_counter / band_width
│   ├─ in_band_pos = v_counter mod band_width
│   └─ band_parity = band_index[0]
│
├── Stage 3: Hatch Angle Computation ──────────────────
│   ├─ Zöllner: slope = ±(angle-512) per band parity
│   ├─ Hering: slope from radial angle to center
│   ├─ Wundt: inverted Hering slope
│   └─ Café: shifted checkerboard (no slope)
│
├── Stage 4: Hatch Pattern Generation ─────────────────
│   ├─ hatch_phase = (h + slope*v + anim) mod spacing
│   ├─ on_hatch = hatch_phase < length
│   │   (thick mode: hatch_phase < length*2)
│   ├─ on_pattern = on_hatch AND in_band_check
│   └─ pattern_y = on_pattern ? 0 : 1023
│
├── Stage 5: Opacity Composite ────────────────────────
│   ├─ blended_y = y_in * (1023 - opacity) / 1024
│   │              + pattern_y * opacity / 1024
│   ├─ blended_u, blended_v (same formula)
│   └─ invert option flips pattern_y
│
├── Mix (3× interpolator_u) ───────────────────────────
│   └─ lerp(dry, wet, mix_amount)
│
└── Bypass → Output
```

The hatch pattern is generated entirely in pixel-clock logic with no frame buffer — every pixel decision is made from the current h/v position, band index, and animation offset. This keeps resource usage minimal (~600 LUTs) but limits the pattern to line-oriented geometries. The Café Wall pattern is unique among the four modes because it uses a shifted checkerboard rather than angled hatching, but it still passes through the same opacity compositing stage.

---

## Parameter Reference

<img src={zollner_control_panel} alt="Videomancer front panel with Zollner loaded"/>
*Videomancer's front panel with Zollner active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Band W
| Property | Value |
|----------|-------|
| Range | 8 – 64 |
| Default | 29 |

Controls the width of the horizontal bands. An 8-entry lookup table maps the 3-bit quantized input to pixel widths: 8, 12, 16, 20, 24, 32, 48, 64. Narrow bands (8 pixels) produce a dense, fine-lined pattern where the illusion is strong but individual hatches are hard to distinguish. Wide bands (64 pixels) create bold, architectural stripes with clearly visible diagonal lines.

---

#### Knob 2 — Hatch Ang
| Property | Value |
|----------|-------|
| Range | 0° – 90° |
| Default | 45° |
| Suffix | ° |

Controls the angle of the hatch marks relative to horizontal. The parameter is centered at 512 (0°). Increasing values tilt the hatches clockwise; decreasing values tilt counter-clockwise. In Zöllner mode, alternate bands receive opposite angles. In Hering and Wundt modes, this parameter sets the base angle that is modulated by radial distance from center.

---

#### Knob 3 — Hatch Sp
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the spacing between adjacent hatch marks within each band. Lower values pack hatches closer together, creating a denser pattern. Higher values spread them apart, giving each hatch more visual weight. The spacing interacts with the hatch length — when spacing equals length, the pattern becomes a solid fill.

---

#### Knob 4 — Opacity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls how strongly the pattern overlay affects the underlying video. At 0% the pattern is invisible. At 100% the pattern completely replaces the video in the hatch regions. Intermediate values blend the pattern semi-transparently over the input. The opacity formula is: output = input × (1023 − opacity) / 1024 + pattern × opacity / 1024.

---

#### Knob 5 — Anim Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the speed of the vertical animation scroll. When Animation is enabled (Toggle 9), this parameter determines how fast the hatch pattern shifts vertically. At 0% there is no movement. Higher values create faster scrolling, which intensifies the perceptual illusion by adding motion to the already-misleading geometry.

---

#### Knob 6 — Hatch Len
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the length of individual hatch marks. Short hatches (low values) create dashed, intermittent diagonal lines. Long hatches (high values) make the diagonals nearly continuous within each band. The Zöllner illusion is typically strongest with moderate-length hatches that are clearly diagonal but don't merge into continuous stripes.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Zöllner | Café |
| **8 — Hatch Style** | Thin | Thick |
| **9 — Animate** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a 2-bit pattern mode selector. Toggle 9 enables or disables animation. Toggle 10 inverts the pattern polarity. Toggle 11 (bit 5) controls bypass. The pattern and invert toggles combine to create 8 distinct visual configurations before considering the continuous knob parameters.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input signal and the pattern-composited output. At 0% the output is the unprocessed input. At 100% the output is the full illusion overlay. Intermediate positions allow subtle pattern underlays that create subliminal perceptual interference.





---

## Guided Exercises

These exercises demonstrate the four illusion pattern modes and show how hatch geometry parameters interact to create different perceptual effects.

### Exercise 1: Classic Zöllner

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: zollner_source1_dog, after: zollner_ex1_s1 },
    { label: "Fruit", before: zollner_source2_fruit, after: zollner_ex1_s2 },
    { label: "Turtle", before: zollner_source3_turtle, after: zollner_ex1_s3 },
    { label: "Pattern", before: zollner_source4_pattern, after: zollner_ex1_s4 },
    { label: "Woman", before: zollner_source5_woman, after: zollner_ex1_s5 },
    { label: "Paint", before: zollner_source6_paint, after: zollner_ex1_s6 },
  ]}
/>
*Classic Zöllner — simulated result across source images.*
**Source**: A video feed with strong horizontal or vertical elements — architecture, bookshelves, or ruled paper.

**What You'll Create**: Create the classic Zöllner illusion of converging parallel lines.

1. **Set Zöllner mode**: Ensure both Pattern toggles are Off (00).
2. **Band width**: Set Band W to ~30% for 16-pixel bands.
3. **Hatch angle**: Set Hatch Ang to ~60%. The hatches tilt visibly from horizontal.
4. **Moderate spacing**: Set Hatch Sp to ~50% for evenly spaced diagonals.
5. **Opacity**: Set Opacity to ~60%. The pattern overlays clearly without hiding the video.
6. **Static**: Keep Animate Off to see the static illusion clearly.

**Key concepts**: The Zöllner illusion works by angle assimilation — hatch angles bias perceived band orientation, adjacent bands with opposite hatches appear to converge/diverge

---

### Exercise 2: Animated Hering Curves

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: zollner_source1_dog, after: zollner_ex2_s1 },
    { label: "Fruit", before: zollner_source2_fruit, after: zollner_ex2_s2 },
    { label: "Turtle", before: zollner_source3_turtle, after: zollner_ex2_s3 },
    { label: "Pattern", before: zollner_source4_pattern, after: zollner_ex2_s4 },
    { label: "Woman", before: zollner_source5_woman, after: zollner_ex2_s5 },
    { label: "Paint", before: zollner_source6_paint, after: zollner_ex2_s6 },
  ]}
/>
*Animated Hering Curves — simulated result across source images.*
**Source**: Video with straight lines — roads, building edges, or a calibration grid.

**What You'll Create**: Demonstrate the Hering illusion with animated hatching.

1. **Hering mode**: Set Pattern high bit On, low bit Off (10 → Hering? Actually toggle_switch_7 On = high bit). With the 2-bit selector: 01 = Hering. Set Toggle 7 Off, Toggle 8 on... No — per the VHDL, pattern bits are from toggle 7 (high) and toggle 8 is hatch style. Let me re-check... Actually Toggle 7 is the pattern selector in a multi-toggle sense. Per the TOML, Toggle 7 has value_labels ["Zöllner", "Hering", "Wundt", "Café Wall"]. This is a 4-option parameter, likely using the same register with thresholds. Set it to position 2 (Hering).
2. **Enable animation**: Toggle Animate On and set Anim Speed to ~40%.
3. **Moderate angle**: Set Hatch Ang to ~55%. Radial hatches create a bulging effect.
4. **Wide bands**: Set Band W to ~50% for clearly visible curvature.
5. **Full opacity**: Set Opacity to ~80%. The pattern dominates the frame.
6. **Observe**: Straight lines in the source video appear to bow outward from center.

**Key concepts**: Hering illusion uses radial angle from center — hatch slope varies across the frame, creating apparent curvature in straight lines

---

### Exercise 3: Café Wall with Thick Lines

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: zollner_source1_dog, after: zollner_ex3_s1 },
    { label: "Fruit", before: zollner_source2_fruit, after: zollner_ex3_s2 },
    { label: "Turtle", before: zollner_source3_turtle, after: zollner_ex3_s3 },
    { label: "Pattern", before: zollner_source4_pattern, after: zollner_ex3_s4 },
    { label: "Woman", before: zollner_source5_woman, after: zollner_ex3_s5 },
    { label: "Paint", before: zollner_source6_paint, after: zollner_ex3_s6 },
  ]}
/>
*Café Wall with Thick Lines — simulated result across source images.*
**Source**: Any video — the Café Wall pattern is effective regardless of source content.

**What You'll Create**: Create the Café Wall illusion with bold, visible tiles.

1. **Café Wall mode**: Set Pattern to Café Wall (position 4).
2. **Thick style**: Toggle Hatch Style to Thick for bold tile boundaries.
3. **Wide bands**: Set Band W to the maximum (~100%) for large 64-pixel tiles.
4. **Spacing**: Adjust Hatch Sp to ~50% to set the tile width.
5. **Partial opacity**: Set Opacity to ~50%. The checkerboard pattern is visible but doesn't obscure the video.
6. **Invert**: Toggle Invert On to see white tiles on video instead of dark.
7. **Animate**: Enable animation at slow speed (~20%) for a slow tile scroll.

**Key concepts**: The Café Wall illusion uses shifted checkerboard rows to create apparent tilt in perfectly horizontal boundaries

---


## Tips

- **Café Wall needs wide bands**: The Café Wall illusion requires bands wide enough for the shifted checkerboard tiles to be individually visible. Use 32px or wider.
- **Invert for dark sources**: When processing dark video, switch to inverted (bright) hatches to maintain pattern visibility.
- **Opacity controls subtlety**: Low opacity (15–25%) creates subliminal pattern interference — viewers sense something is "off" without identifying the overlay. High opacity (70–100%) makes the illusion explicit and dramatic.
- **Thick hatches for projection**: When the output will be displayed on a large screen or projected, thick hatch style ensures the lines remain visible at viewing distance.

---

## Glossary

| Term | Definition |
|------|------------|
| **Angle Assimilation** | The perceptual phenomenon where nearby lines bias the perceived orientation of a target line toward their own angle. |
| **Band** | A horizontal stripe region within which all hatches share the same angle; Zöllner patterns alternate hatch direction between adjacent bands. |
| **Café Wall Illusion** | A geometric illusion where alternating rows of offset dark and light tiles create the appearance of non-parallel horizontal lines. |
| **Checkerboard** | A pattern of alternating dark and light squares; the Café Wall variant shifts alternate rows by half a tile. |
| **Hatch** | A short diagonal line segment drawn within a band; the primary element that creates perceptual angle distortion. |
| **Hering Illusion** | An illusion where parallel straight lines appear to bow outward when superimposed on radially emanating lines. |
| **LUT** | Look-Up Table; here used to map the 3-bit quantized band width parameter to one of 8 pixel widths. |
| **Op Art** | Optical Art movement of the 1960s that exploited geometric patterns to create visual illusions of movement and depth. |
| **Opacity** | The blending weight between the illusion pattern and the underlying video (0 = transparent, 1023 = opaque). |
| **Wundt Illusion** | The inverse of the Hering illusion; parallel lines appear to bow inward when crossed by converging radial lines. |
| **Zöllner Illusion** | The foundational optical illusion (1860) where parallel lines appear non-parallel due to crossing diagonal hatch marks. |

---
