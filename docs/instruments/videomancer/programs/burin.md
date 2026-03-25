---
draft: true
sidebar_position: 33
slug: /instruments/videomancer/burin
title: "Burin"
image: /img/instruments/videomancer/burin/burin_hero_s1.png
description: "Every photograph contains continuous tonal gradations — smooth transitions from light to shadow."
---

![Burin hero image](/img/instruments/videomancer/burin/burin_hero_s1.png)
*Burin rendering luminance-zone crosshatch engraving with four angle-selectable line sets, transforming video into copperplate intaglio artwork.*

---

## Overview

**Burin** is a real-time engraving renderer that transforms live video into the look of a hand-cut copperplate print. It reads the brightness of every pixel and assigns it to one of five ***luminance zones***, from paper white through progressively denser hatching to a tight lozenge mesh in the deepest shadows. Four independent sets of parallel lines, each at a different angle, are drawn across the screen using modular coordinate arithmetic. The zone determines which line sets are active: bright areas remain blank paper, light shadows receive a single hatching direction, deeper shadows add a crossing direction, and the darkest regions activate all four directions, producing the dense diamond pattern that master engravers use to render rich blacks.

The result is a living copperplate print. Portraits resolve into delicate webs of ink. Landscapes acquire the texture of a Renaissance illustration. Because the hatching responds to the source video in real time, the engraving breathes with motion (lines appear and vanish as light moves across the scene.)

:::tip
Burin is purely combinational: ***zero BRAM tiles*** are used. All of that intricate crosshatching is computed from scratch every pixel clock using modular arithmetic on the pixel coordinates.
:::

### What's In a Name?

A ***burin*** is the steel cutting tool used by engravers to incise lines into a copper printing plate. The tool's V-shaped tip is pushed across the metal, raising a thin curl of copper and leaving a groove that will hold ink. The name places this program squarely in the tradition of ***intaglio*** printmaking: the family of techniques where ink sits in grooves cut below the plate surface, the opposite of relief printing. Masters like Albrecht Dürer and Marcantonio Raimondi used burins to create prints of extraordinary tonal range, building up shadow and form entirely from networks of crossed lines.

---

## Quick Start

1. Feed a source with clear tonal range: a face, a landscape, anything with distinct lights and darks. You should see the image rendered as a pattern of fine lines on a bright paper background. Light areas are blank; dark areas are densely hatched.
2. Turn **Spacing** (Knob 1) to increase the gap between lines. The engraving becomes coarser and more graphic. Turn it back for fine, tightly spaced hatching.
3. Rotate **Primary Angle** (Knob 3) to swing the hatching direction. Watch the line orientation shift across eight angles, from horizontal through 45° diagonals to near-vertical.
4. Push **Mix** (Fader 12) toward the dry end. The original video blends back in beneath the engraving, like a print laid over a photograph.

---

## Parameters

![Videomancer front panel with Burin loaded](/img/instruments/videomancer/burin/burin_control_panel.png)
*Videomancer's front panel with Burin active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Spacing

| Property | Value |
|----------|-------|
| Range | 2 – 24 |
| Default | 13 |

**Spacing** controls the distance between parallel lines in all four hatching directions. At the lowest setting, lines are packed tightly: just three pixels apart: producing fine, closely woven textures that look almost like pencil shading. As you increase Spacing, the gaps between lines widen and the engraving becomes bolder and more graphic. At the highest setting, lines are twenty-four pixels apart and the image takes on the feel of a rough woodcut.

Spacing is quantized into eight discrete steps (3, 4, 6, 8, 10, 12, 16, and 24 pixels), so the control clicks between distinct visual densities rather than sweeping smoothly. This mirrors the way a real engraver commits to a line spacing for each tonal region of a plate.

:::note
**Line Width** (Knob 2) is constrained to half the current Spacing value. When you increase Spacing, the maximum possible line width also increases (wider grooves become available to cut.)
:::

---

### Knob 2 — Line Width

| Property | Value |
|----------|-------|
| Range | 1px – 12px |
| Default | 4px |

**Line Width** sets the thickness of each hatching stroke, measured in pixels. At minimum, every line is a single pixel wide: a hairline cut. As you turn the knob clockwise, the strokes thicken and ink coverage increases, making shadows darker and the overall print heavier. The maximum width is always half the current spacing, so lines can never merge into a solid fill.

When Line Width is narrow, the engraving has an airy, delicate quality. When it approaches its maximum, each line set covers nearly half the available space and the crosshatch pattern becomes a dense, authoritative mesh.

---

### Knob 3 — Primary Angle

| Property | Value |
|----------|-------|
| Range | 0° – 157° |
| Default | 39° |

**Primary Angle** selects the orientation of the first hatching direction: the one that appears first in light shadows. Eight discrete angles are available, stepping from horizontal lines (0°) through diagonal (45°) to near-vertical (157°). This is the dominant visual angle of the engraving; it establishes the "grain" of the print.

Traditional engravers chose their primary hatching direction based on the subject. Portraits often use gently angled lines that follow the contour of a face. Landscapes favor horizontal strokes. Experiment with Primary Angle to find the orientation that best suits your source material.

:::tip
Combine a ***horizontal*** Primary Angle with a high **Cross Angle** to emulate classic line engraving. Use a ***diagonal*** Primary Angle for a more dynamic, Baroque feel.
:::

---

### Knob 4 — Cross Angle

| Property | Value |
|----------|-------|
| Range | 30° – 90° |
| Default | 60° |

**Cross Angle** sets the angular separation between the crossing line sets. At the lowest setting (30°), the crossing lines are nearly parallel to the primary set, producing a tight, shimmering moiré. At the highest setting (90°), the crossings are perpendicular, creating a clean grid. Four discrete steps are available.

The cross angle has a dramatic effect on the lozenge pattern that appears in the darkest zones. A 90° cross produces square diamonds; a 45° cross produces elongated rhombuses. Historical engravers carefully chose their crossing angles to control the "tooth" of their hatching.

---

### Knob 5 — Paper Tint

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 45° |

**Paper Tint** shifts the hue of the paper background. At default, the paper is a bright, neutral off-white (Y = 940). Rotating this knob warms or cools the paper tone by introducing a subtle chroma offset. Think of it as choosing between cream laid paper, cool blue-white stock, or warm parchment.

The tint is gentle: the paper never becomes saturated or brightly colored. We're simulating the understated warmth of aged cotton rag, not construction paper.

---

### Knob 6 — Ink Tint

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Ink Tint** shifts the hue of the ink used to render hatching lines. At default, the ink is a near-black neutral (Y = 40). Rotating this knob introduces a subtle color cast: sepia for warm-toned prints, blue-black for cooler steel engravings, or a hint of green for the patina of oxidized copper.

:::tip
Set **Paper Tint** to warm and **Ink Tint** to cool (or vice versa) for a ***split-toned*** print that evokes hand-tinted historical engravings.
:::

---

### Switch 7 — Line Style

| Property | Value |
|----------|-------|
| Off | Sharp |
| On | Feathered |
| Default | Sharp |

**Line Style** selects between hard-edged and soft-edged hatching strokes. In **Sharp** mode, each line is rendered at full ink density with crisp pixel boundaries: clean, mechanical, like a freshly printed plate. In **Feathered** mode, line edges are softened by blending ink toward the paper color, producing a gentler, slightly diffused appearance. Feathered lines suggest the spread of ink on dampened paper or the subtle burr left by a freshly cut groove.

---

### Switch 8 — Plate Wear

| Property | Value |
|----------|-------|
| Off | Clean |
| On | Worn |
| Default | Clean |

**Plate Wear** simulates the degradation of a copper plate after many impressions. In **Clean** mode, every hatching line prints perfectly. In **Worn** mode, a pseudo-random noise source (a 16-bit LFSR) randomly breaks individual line pixels, creating small skips and dropouts across the engraving. The result looks like a plate that has been through the press hundreds of times: the shallow grooves have worn down and no longer hold ink consistently.

:::note
Plate Wear affects all four line sets equally. The randomness changes every pixel, so the wear pattern shimmers with subtle motion (a living patina rather than a static texture.)
:::

---

### Switch 9 — Color

| Property | Value |
|----------|-------|
| Off | Single Ink |
| On | Duotone |
| Default | Single Ink |

**Color** selects between monochrome and duotone rendering. In **Single Ink** mode, hatched areas receive the pure ink color set by **Ink Tint** (Knob 6). In **Duotone** mode, the chroma of the original video source is blended into the hatched areas: ink lines carry a tint derived from the source image's color at each pixel. Bright paper areas remain unaffected.

Duotone mode is the key to color engravings. A face rendered in Single Ink is a pure etching; in Duotone, the skin picks up warm tones, lips carry a blush, and eyes darken with their own color.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Normal |
| On | Invert |
| Default | Normal |

**Invert** reverses the tonal mapping of the output. In **Normal** mode, paper is bright and ink is dark: a traditional print on white stock. In **Invert** mode, the luminance channel is complemented, swapping lights and darks. The result resembles a ***mezzotint*** or a photographic negative of an engraving: bright lines on a dark ground.

Invert does not change the zone classification or the hatching pattern: only the final output brightness is flipped. The same crosshatch structure is preserved, but rendered as light strokes on a dark field.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all engraving stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw video and the engraved result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (original) and wet (engraved) signals. At 100%, fully clockwise, only the engraved output is visible. As you pull the fader toward 0%, the original video blends back in. At 50%, the engraving overlays the source as a translucent texture (like seeing a print superimposed on a photograph.)

Mix uses three parallel interpolators (one per YUV channel) for a smooth, artifact-free crossfade at any position.

---

## Background

### Intaglio Engraving

***Intaglio*** is the family of printmaking techniques where the image is incised into a surface. Ink is pressed into the grooves, the surface is wiped clean, and damp paper is pressed against the plate under enormous pressure, pulling ink from the grooves onto the page. ***Line engraving***: the specific technique Burin emulates: uses a burin tool to cut V-shaped grooves directly into a polished copper plate. Unlike etching, which uses acid to bite into the metal, engraving is a purely mechanical process: the artist's hand pushes the tool through copper.

Because the burin can only cut lines, not continuous tones, engravers developed an elaborate visual language of hatching. Parallel lines suggest light tone; crossed lines build darker shadow; and dense networks of four or more crossing directions create the deepest blacks. This system maps naturally to Burin's five luminance zones.

### Zone-Based Hatching

Burin classifies every pixel into one of five ***luminance zones*** based on its brightness:

- **Zone 0** (brightest): Paper white (no lines at all.)
- **Zone 1**: First lines (only the primary hatching direction is drawn.)
- **Zone 2**: Crosshatch (two line directions are active.)
- **Zone 3**: Triple cross (three directions produce a complex mesh.)
- **Zone 4** (darkest): Lozenge fill (all four directions create a tight diamond pattern.)

This mirrors the way a master engraver builds tonal range on a plate. Albrecht Dürer's famous engravings demonstrate the technique: a cheek lit by sunlight shows only faint parallel lines, the shadow under a chin adds a crossing direction, and deep folds of drapery receive three or four sets of lines that lock together into a dark, woven texture. The viewer perceives continuous tone, but every mark is a discrete line.

### Modular Line Generation

Each line set is computed from the pixel's screen coordinates using a simple ***distance projection***. For a given angle, the distance is a linear combination of the horizontal and vertical counters: for example, a 45° line set uses `d = x + y`. The pixel is "on a line" if `d mod spacing < line_width`. This modular arithmetic repeats the line pattern across the entire screen at perfect regularity, like the ruled grooves on a physical plate.

The eight Primary Angle settings correspond to eight projection formulas, stepping from pure horizontal (`d = y`) through eight intermediates to near-vertical (`d = x/2 − y`). The Cross Angle parameter selects which combination of projection formulas the second, third, and fourth line sets use.


---

## Signal Flow

### Signal Flow Notes

Two key interactions define Burin's character:

1. **Luminance drives hatching density.** The input Y value determines the zone, and the zone determines how many of the four line sets are active. This is the core of the engraving illusion: ***tone is encoded as line density***, exactly as it is on a real copperplate.

2. **Cross-channel color injection.** In Duotone mode, the input U and V values are averaged with the ink's U and V, so hatched areas carry a tint derived from the source video's color. This crosses the Y→UV boundary: luminance decides where ink goes, but chrominance decides what color it carries.

:::note
The LFSR for Plate Wear runs continuously and produces a different random pattern every pixel clock. Because it is not synchronized to any video structure, the wear pattern drifts freely, producing a shimmering texture that never repeats in a visually obvious way.
:::


---

## Exercises

These exercises progress from simple hatching to full copperplate compositions. Each exercise builds on the previous one, gradually engaging more of Burin's controls.
### Exercise 1: First Impressions

![First Impressions result](/img/instruments/videomancer/burin/burin_ex1_s1.png)
*First Impressions — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic line engraving from a portrait or still life, exploring the relationship between spacing, width, and angle.

#### Key Concepts

- Zone-based hatching maps brightness to line density
- Spacing and line width control the texture of the print
- Primary Angle sets the dominant visual grain

#### Video Source

A portrait or still life with clear tonal range (distinct highlights, midtones, and shadows.)

#### Steps

1. **Default print**: Feed your source and observe the engraving at default settings. Bright areas are blank paper; dark areas show crosshatched lines.
2. **Coarsen the plate**: Turn **Spacing** (Knob 1) clockwise to widen the gaps between lines. The engraving becomes bolder, more like a woodcut. Return to a medium setting.
3. **Thicken the lines**: Increase **Line Width** (Knob 2). The strokes fatten and shadows darken as more ink coverage fills each zone.
4. **Rotate the grain**: Step through **Primary Angle** (Knob 3). Watch the hatching swing from horizontal bands to diagonal webs to near-vertical stripes. Choose the angle that best follows the contours of your subject.
5. **Adjust the cross**: Change **Cross Angle** (Knob 4) to see how the crossing pattern shifts. A 90° cross produces square diamonds in the darkest areas; a 30° cross produces elongated rhombuses.

#### Settings

| Control | Value |
|---------|-------|
| Spacing | ~8 px (step 4) |
| Line Width | ~4 px |
| Primary Angle | 45° |
| Cross Angle | 90° |
| Paper Tint | default |
| Ink Tint | default |
| Line Style | Sharp |
| Plate Wear | Clean |
| Color | Single Ink |
| Invert | Normal |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Aged Plate

![Aged Plate result](/img/instruments/videomancer/burin/burin_ex2_s1.png)
*Aged Plate — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An aged, hand-tinted engraving with worn lines on warm parchment (the look of a print pulled from a well-used plate.)

#### Key Concepts

- Plate Wear simulates physical degradation of the printing plate
- Feathered lines soften the mechanical precision of the engraving
- Paper and Ink Tint create period-appropriate color palettes

#### Video Source

A landscape or architectural subject with large tonal areas.

#### Steps

1. **Set the base**: Start with medium Spacing (~8 px) and moderate Line Width.
2. **Warm the paper**: Rotate **Paper Tint** (Knob 5) toward a warm tone. The background shifts from cool white to cream or parchment.
3. **Tint the ink**: Rotate **Ink Tint** (Knob 6) toward a warm sepia tone. The lines shift from neutral black toward brown.
4. **Soften the edges**: Set **Line Style** (Switch 7) to **Feathered**. The crisp pixel edges blur slightly, as if ink bled into dampened paper.
5. **Wear the plate**: Set **Plate Wear** (Switch 8) to **Worn**. Random dropouts appear in the hatching: shallow grooves that no longer hold ink. The print looks like it was pulled from a plate with hundreds of impressions behind it.
6. **Blend the eras**: Pull **Mix** (Fader 12) to about 70%. The source video shows through the engraving like a ghostly underpainting.

#### Settings

| Control | Value |
|---------|-------|
| Spacing | ~8 px (step 4) |
| Line Width | ~5 px |
| Primary Angle | 22° |
| Cross Angle | 60° |
| Paper Tint | ~45° (warm) |
| Ink Tint | ~30° (sepia) |
| Line Style | Feathered |
| Plate Wear | Worn |
| Color | Single Ink |
| Invert | Normal |
| Bypass | Off |
| Mix | ~70% |

---

### Exercise 3: Duotone Mezzotint

![Duotone Mezzotint result](/img/instruments/videomancer/burin/burin_ex3_s1.png)
*Duotone Mezzotint — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An inverted color engraving: bright hatching lines on a dark ground, tinted by the source video's own colors. The effect resembles a ***mezzotint*** or a photographic negative of a hand-colored print.

#### Key Concepts

- Duotone mode injects source color into ink areas
- Invert creates a mezzotint-style bright-on-dark rendering
- Combining Duotone and Invert produces rich color negative effects

#### Video Source

Colorful footage: flowers, neon, painted surfaces: anything with vivid saturation.

#### Steps

1. **Enable Duotone**: Set **Color** (Switch 9) to **Duotone**. Hatched areas now carry the color of the source video at each pixel. A red flower produces red-tinted hatching; a blue sky produces blue ink.
2. **Invert the ground**: Set **Invert** (Switch 10) to **Invert**. The luminance flips: paper becomes dark, ink becomes light. Bright hatching lines now glow on a dark field.
3. **Tighten the mesh**: Reduce **Spacing** (Knob 1) to a fine setting (3–4 px) and increase **Line Width** (Knob 2) to fill most of the spacing. The dense hatching produces a richly textured color field.
4. **Rotate for drama**: Set **Primary Angle** (Knob 3) to a diagonal (45°) and **Cross Angle** (Knob 4) to 90° for a strong diamond pattern in the highlights (which are now the densely hatched areas).
5. **Add wear**: Enable **Plate Wear** (Switch 8) for sparkle: bright dropouts in the dark ground add a stippled, starry quality.

#### Settings

| Control | Value |
|---------|-------|
| Spacing | ~4 px (step 2) |
| Line Width | ~3 px |
| Primary Angle | 45° |
| Cross Angle | 90° |
| Paper Tint | default |
| Ink Tint | default |
| Line Style | Sharp |
| Plate Wear | Worn |
| Color | Duotone |
| Invert | Invert |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Burin**: A steel engraving tool with a V-shaped tip, pushed by hand across a copper plate to cut grooves that hold ink.

- **Crosshatch**: A shading technique using two or more sets of intersecting parallel lines to build tonal density.

- **Duotone**: A printing or rendering mode using two ink colors (or an ink plus a tinted substrate) to expand tonal range beyond pure monochrome.

- **Feathering**: Softening the edges of lines or shapes by blending them gradually into the surrounding area, simulating ink spread.

- **Hatching**: Drawing tone with parallel lines; closer lines or thicker lines suggest darker values.

- **Intaglio**: A family of printmaking techniques where ink is held in grooves cut or etched below the plate surface, including engraving, etching, drypoint, and mezzotint.

- **LFSR**: Linear Feedback Shift Register; a simple digital circuit that generates a pseudo-random binary sequence, used here for plate wear noise.

- **Lozenge**: A diamond-shaped pattern formed where four sets of crossing lines intersect; the densest hatching zone.

- **Luminance Zone**: A brightness range that determines which hatching line sets are active at a given pixel.

- **Mezzotint**: An intaglio technique that works from dark to light by selectively smoothing a roughened plate surface; Burin's Invert mode evokes this look.

- **Modular Arithmetic**: The `mod` (remainder) operation that creates repeating line patterns from pixel coordinates.

---
