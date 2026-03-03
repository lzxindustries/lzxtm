---
draft: true
sidebar_position: 141
slug: /instruments/videomancer/imprint
title: "Imprint"
image: /img/instruments/videomancer/imprint/imprint_hero_s1.png
description: "Every printed photograph in a newspaper, magazine, or book is an illusion."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import imprint_source1_ballerina from '/img/instruments/videomancer/imprint/imprint_source1_ballerina.png';
import imprint_source2_runner from '/img/instruments/videomancer/imprint/imprint_source2_runner.png';
import imprint_source3_elephant from '/img/instruments/videomancer/imprint/imprint_source3_elephant.png';
import imprint_source4_pattern from '/img/instruments/videomancer/imprint/imprint_source4_pattern.png';
import imprint_source5_girl from '/img/instruments/videomancer/imprint/imprint_source5_girl.png';
import imprint_source6_wood from '/img/instruments/videomancer/imprint/imprint_source6_wood.png';
import imprint_hero_s1 from '/img/instruments/videomancer/imprint/imprint_hero_s1.png';
import imprint_hero_s2 from '/img/instruments/videomancer/imprint/imprint_hero_s2.png';
import imprint_hero_s3 from '/img/instruments/videomancer/imprint/imprint_hero_s3.png';
import imprint_hero_s4 from '/img/instruments/videomancer/imprint/imprint_hero_s4.png';
import imprint_hero_s5 from '/img/instruments/videomancer/imprint/imprint_hero_s5.png';
import imprint_hero_s6 from '/img/instruments/videomancer/imprint/imprint_hero_s6.png';
import imprint_ex1_s1 from '/img/instruments/videomancer/imprint/imprint_ex1_s1.png';
import imprint_ex1_s2 from '/img/instruments/videomancer/imprint/imprint_ex1_s2.png';
import imprint_ex1_s3 from '/img/instruments/videomancer/imprint/imprint_ex1_s3.png';
import imprint_ex1_s4 from '/img/instruments/videomancer/imprint/imprint_ex1_s4.png';
import imprint_ex1_s5 from '/img/instruments/videomancer/imprint/imprint_ex1_s5.png';
import imprint_ex1_s6 from '/img/instruments/videomancer/imprint/imprint_ex1_s6.png';
import imprint_ex2_s1 from '/img/instruments/videomancer/imprint/imprint_ex2_s1.png';
import imprint_ex2_s2 from '/img/instruments/videomancer/imprint/imprint_ex2_s2.png';
import imprint_ex2_s3 from '/img/instruments/videomancer/imprint/imprint_ex2_s3.png';
import imprint_ex2_s4 from '/img/instruments/videomancer/imprint/imprint_ex2_s4.png';
import imprint_ex2_s5 from '/img/instruments/videomancer/imprint/imprint_ex2_s5.png';
import imprint_ex2_s6 from '/img/instruments/videomancer/imprint/imprint_ex2_s6.png';
import imprint_ex3_s1 from '/img/instruments/videomancer/imprint/imprint_ex3_s1.png';
import imprint_ex3_s2 from '/img/instruments/videomancer/imprint/imprint_ex3_s2.png';
import imprint_ex3_s3 from '/img/instruments/videomancer/imprint/imprint_ex3_s3.png';
import imprint_ex3_s4 from '/img/instruments/videomancer/imprint/imprint_ex3_s4.png';
import imprint_ex3_s5 from '/img/instruments/videomancer/imprint/imprint_ex3_s5.png';
import imprint_ex3_s6 from '/img/instruments/videomancer/imprint/imprint_ex3_s6.png';

# Imprint

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: imprint_source1_ballerina, after: imprint_hero_s1 },
    { label: "Runner", before: imprint_source2_runner, after: imprint_hero_s2 },
    { label: "Elephant", before: imprint_source3_elephant, after: imprint_hero_s3 },
    { label: "Pattern", before: imprint_source4_pattern, after: imprint_hero_s4 },
    { label: "Girl", before: imprint_source5_girl, after: imprint_hero_s5 },
    { label: "Wood", before: imprint_source6_wood, after: imprint_hero_s6 },
  ]}
/>
*Imprint rendering CMYK halftone dot screens with rotated color separations and subtractive ink composite over a warm paper background.*

---

## Overview

Every printed photograph in a newspaper, magazine, or book is an illusion. What appears to be continuous tone is actually a pattern of tiny ink dots laid down at specific angles — one screen for each ink color. Imprint recreates this illusion in reverse: it takes a continuous-tone video signal and converts it into a halftone print simulation, complete with rotated dot screens for cyan, magenta, and yellow separations, a configurable paper background color, and a subtractive ink compositing model.

The program splits the input video into three ink channels (C, M, Y), rotates each channel's dot grid by a different angle using a 32-entry sin/cos lookup table, evaluates a distance function within each grid cell to determine whether a dot is present, and composites the results subtractively onto a paper color. The name *Imprint* refers to the physical act of pressing an inked plate onto paper — the moment when the halftone screen transfers to the page.

At conservative settings — large dot pitch, moderate ink density, separated CMY screens — Imprint produces a convincing newspaper or poster print effect. At extreme settings — small pitch, maximum density, unusual screen angles — the dot patterns become moire-like interference textures where the three ink layers visually interact in complex ways. Switching to monochrome mode, line screen mode, or diamond dots produces entirely different families of print effects.

---

## Background

### What Is Halftone Printing?

**Halftone** is a reprographic technique that simulates continuous tone using dots of varying size or spacing. In conventional offset printing, each ink color can only be applied at full strength or not at all — there are no partial ink densities on a press. To create the illusion of lighter tones, the printer breaks the image into a grid of dots: large dots in dark areas, small dots in light areas. From a distance, the eye averages the dots with the surrounding white paper to perceive intermediate tones. This technique was invented in the 1880s and remains the foundation of all CMYK color printing.

### Color Separation and Screen Angles

A full-color halftone print requires at least three ink layers: **cyan** (absorbs red light), **magenta** (absorbs green light), and **yellow** (absorbs blue light). Each ink layer is screened independently, and critically, each screen is rotated to a different angle. If all three screens were at the same angle, their dots would overlap perfectly, producing either full-ink or no-ink with no intermediate blending. By rotating the screens — traditionally cyan at 15°, magenta at 75°, yellow at 0° — the dots interleave, creating the characteristic **rosette pattern** visible under magnification. Imprint uses a configurable base angle plus a spread parameter that offsets the magenta and yellow screens from the cyan screen by one and two spread increments respectively.

### Distance Functions and Dot Shapes

Within each grid cell, Imprint evaluates how far a pixel is from the cell center to determine whether it falls inside or outside the dot. Three distance functions are available. **Circle mode** uses an approximation: `max(|dx|, |dy|) + min(|dx|, |dy|) / 2`, which produces roughly circular dots without requiring a multiply or square root. **Diamond mode** uses **Manhattan distance**: `|dx| + |dy|`, producing diamond-shaped dots — the classic pattern seen in comic book printing. **Line screen mode** evaluates only the horizontal distance `|dx|`, producing parallel lines instead of dots — the technique used in engraved banknote printing.

### Subtractive Color Mixing

Printed ink works by **subtraction**: each ink layer absorbs (subtracts) a portion of the light spectrum reflected from the paper. Cyan ink absorbs red, so where a cyan dot is present, the Cr (red-difference) channel is reduced. Magenta absorbs green, reducing luminance. Yellow absorbs blue, reducing the Cb (blue-difference) channel. Imprint implements a simplified subtractive model: starting from the paper color, each active dot subtracts fixed amounts from the Y, Cb, and Cr channels. Where all three dots overlap, the result approaches black (or very dark paper color).

### Paper and Ink Tinting

Commercial printing rarely uses pure white paper or pure black ink. Newsprint has a yellowish cast; art paper ranges from warm cream to cool blue-white; specialty inks include sepia, navy, and metallic tones. Imprint provides two 8-entry color lookup tables — one for paper, one for ink — selectable via the Paper Tint and Ink Tint knobs. The paper colors range from white through cream, warm, mint, sky, lavender, pink, and newsprint. The ink colors range from black through sepia, navy, crimson, forest, indigo, maroon, and brown.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Channel Separation ───────────────
│   │
│   ├─ Y → Cyan Value     (C = 1023 - Y, brightness → ink density)
│   ├─ V → Magenta Value  (M = Cr, red content → magenta ink)
│   └─ U → Yellow Value   (Y = 1023 - Cb, blue absence → yellow ink)
│
├── Stage 2: Rotated Grid Coordinates ──────────────────────────
│   │
│   ├─ 3× rotation:  rx = h·cos(θ) + v·sin(θ)
│   │                 ry = v·cos(θ) - h·sin(θ)
│   ├─ Cell-local position: (rx AND pitch_mask, ry AND pitch_mask)
│   └─ Angles: C = base, M = base + spread, Y = base + 2×spread
│
├── Stage 3: Distance + Threshold ──────────────────────────────
│   │
│   ├─ dx, dy = cell_position - half_pitch (distance from centre)
│   ├─ Distance mode:
│   │   ├─ Line:    dist = |dx|
│   │   ├─ Diamond: dist = |dx| + |dy|
│   │   └─ Circle:  dist = max(|dx|,|dy|) + min(|dx|,|dy|)/2
│   ├─ Threshold = channel_value × ink_density >> 15 + half_pitch
│   └─ dot_active = (dist ≤ threshold)
│
├── Stage 4: Subtractive Ink Composite ─────────────────────────
│   │
│   ├─ CMY Mode:
│   │   ├─ Start from paper colour (Y, Cb, Cr)
│   │   ├─ Cyan dot:    Y -= 200, Cr -= 180
│   │   ├─ Magenta dot: Y -= 200, Cb -= 100, Cr += 140
│   │   ├─ Yellow dot:  Y -= 80, Cb -= 180
│   │   └─ Clamp [0, 1023]
│   ├─ Mono Mode: ink colour where dot_c active, paper colour otherwise
│   └─ Invert: complement all channels (1023 - value)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay pipeline (hsync, vsync, field)
│
├── Interpolator (4 clocks) ────────────────────────────────────
│   └─ Crossfade dry (delayed input) ↔ wet (halftone) by Mix fader
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline's most critical interaction is between the rotated grid coordinates (Stage 2) and the distance threshold (Stage 3). The rotation uses a 32-entry sin/cos LUT with 8-bit signed values scaled by 128, giving approximately 11.25° per LUT step. The cell-local position is extracted by masking the rotated coordinates with `pitch_mask` (a power-of-two bitmask), which limits valid pitches to 4, 8, 16, and 32 pixels. The threshold comparison is channel-dependent: brighter source areas produce larger dots (higher threshold), while darker areas produce smaller dots or no dot at all. The subtractive composite model is simplified — fixed subtraction amounts per ink rather than proportional mixing — which creates the characteristic hard-edged, graphic quality of a coarsely-screened print.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Dot Pitch
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Selects the halftone dot pitch — the spacing of the screen grid in pixels. The four available pitches are 4, 8, 16, and 32 pixels, selected as discrete steps. Smaller pitches create finer dot patterns that resolve more detail but can produce dense moire when combined with screen rotation. Larger pitches create coarse, poster-like dots that are individually visible. The pitch also determines the maximum dot size, since dots cannot exceed the cell boundary.

---

#### Knob 2 — Ink Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the ink density — how large the halftone dots grow within each grid cell. At 0%, dots are at their minimum size relative to the channel intensity, producing a very light print. At 100%, dots are at their maximum, filling more of each cell and producing denser, darker areas. Ink Density interacts with the source brightness: a bright area of the source creates high channel values, which combined with high ink density produce large dots. Dark areas always produce small dots regardless of density. This mirrors the physical relationship between tonal value and dot size in real halftone printing.

---

#### Knob 3 — Screen Angle
| Property | Value |
|----------|-------|
| Range | 0° – 90° |
| Default | 0° |
| Suffix | ° |

Sets the base rotation angle for the halftone screen grid. At 0°, the dot pattern is axis-aligned with the video raster. As the angle increases, the entire grid rotates. In CMY mode, this angle applies to the cyan screen; the magenta and yellow screens are offset from it by the Angle Spread value. Rotation is essential for avoiding moire between the dot pattern and the video raster, and for creating the traditional rosette pattern between color separations.

---

#### Knob 4 — Angle Spread
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the angular separation between the three CMY screen layers. The cyan screen uses the base angle; the magenta screen is offset by one spread increment; the yellow screen by two spread increments. At 0%, all three screens are at the same angle — their dots overlap perfectly, producing a monochromatic pattern. As spread increases, the screens separate and their dots interleave, creating the color rosette pattern characteristic of commercial printing. At maximum spread, the three screens are widely separated, producing vivid moire interference between the ink layers.

---

#### Knob 5 — Paper Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Selects the paper background color from an 8-entry lookup table using the upper 3 bits of the register. The available paper colors are: white, cream, warm, mint, sky, lavender, pink, and newsprint. The paper color is visible wherever no ink dots are present — it fills the space between dots and determines the overall background tone of the halftone image. Warm paper tints (cream, newsprint) simulate aged or recycled paper stock; cool tints (sky, lavender) create a more contemporary look.

---

#### Knob 6 — Ink Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Selects the ink color from a second 8-entry lookup table, again using the upper 3 bits. The available ink colors are: black, sepia, navy, crimson, forest, indigo, maroon, and brown. In mono mode, this color is used directly wherever a dot is active. In CMY mode, the ink tint is not applied — the subtractive CMY model uses fixed ink subtraction values instead. Sepia ink on cream paper produces a convincing antique print effect; navy ink on white paper resembles a blueprint or architectural drawing.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color Mode** | CMY | Mono |
| **8 — Dot Shape** | Circle | Diamond |
| **9 — Line Screen** | Dots | Lines |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent binary processing options. Toggle 7 (Color Mode) selects between full CMY color separation and single-channel monochrome. Toggle 8 (Dot Shape) switches the distance function between circular and diamond dots. Toggle 9 (Line Screen) overrides the dot shape entirely, producing parallel lines instead of dots. Toggle 10 (Invert) complements the composited output. Toggle 11 (Bypass) routes input directly to output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet crossfade between the original input (delayed to match the 8-clock processing pipeline) and the halftone output. At 100%, the output is fully halftone-rendered. At 0%, the output is the unmodified input. Intermediate values blend the two, allowing the halftone dot texture to be layered over the source video at any strength.

---

## Guided Exercises

These exercises progress from a simple monochrome halftone to full CMYK color separation, each introducing new screen parameters and compositing options.

### Exercise 1: Newspaper Halftone

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: imprint_source1_ballerina, after: imprint_ex1_s1 },
    { label: "Runner", before: imprint_source2_runner, after: imprint_ex1_s2 },
    { label: "Elephant", before: imprint_source3_elephant, after: imprint_ex1_s3 },
    { label: "Pattern", before: imprint_source4_pattern, after: imprint_ex1_s4 },
    { label: "Girl", before: imprint_source5_girl, after: imprint_ex1_s5 },
    { label: "Wood", before: imprint_source6_wood, after: imprint_ex1_s6 },
  ]}
/>
*Newspaper Halftone — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable faces and moderate contrast.

**Objective**: Learn how dot pitch and ink density control the fundamental halftone pattern, using mono mode for simplicity.

1. **Enable mono mode**: Set Color Mode to Mono. The output is now a single-screen halftone.
2. **Set coarse pitch**: Set Dot Pitch to step 3 (16-pixel dots). Large, individually visible dots appear.
3. **Adjust density**: Sweep Ink Density from 0% to 100%. Watch dots grow from tiny points to solid fields. Find a setting (~50%) where faces are clearly recognizable through the dot pattern.
4. **Rotate the screen**: Increase Screen Angle. The dot grid rotates — notice how the moire pattern with the video raster changes at different angles.
5. **Try diamond dots**: Flip Dot Shape to Diamond. The round dots become square diamonds, giving a comic-book print quality.
6. **Paper and ink**: Set Paper Tint to select newsprint (yellowish). Set Ink Tint to black. The result should resemble a newspaper photograph.

**Key concepts**: Halftone dots create continuous tone illusion, dot size is proportional to source brightness, screen rotation reduces moire with raster, mono mode uses a single ink channel

---

### Exercise 2: Color Separation Rosettes

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: imprint_source1_ballerina, after: imprint_ex2_s1 },
    { label: "Runner", before: imprint_source2_runner, after: imprint_ex2_s2 },
    { label: "Elephant", before: imprint_source3_elephant, after: imprint_ex2_s3 },
    { label: "Pattern", before: imprint_source4_pattern, after: imprint_ex2_s4 },
    { label: "Girl", before: imprint_source5_girl, after: imprint_ex2_s5 },
    { label: "Wood", before: imprint_source6_wood, after: imprint_ex2_s6 },
  ]}
/>
*Color Separation Rosettes — simulated result across source images.*
**Source**: Colorful footage — flowers, fruit, painted surfaces, or color bars.

**Objective**: Explore how CMY color separations interact through screen angle spread to create rosette patterns.

1. **Enable CMY**: Set Color Mode to CMY. Three ink screens are now active.
2. **Zero spread**: Set Angle Spread to 0%. All three screens are at the same angle — the output looks like a mono print because the dots overlap perfectly.
3. **Increase spread**: Slowly increase Angle Spread. Watch the three screen layers separate and interleave, creating the colored rosette pattern visible between dots.
4. **Large pitch for clarity**: Set Dot Pitch to step 4 (32-pixel dots) so individual dots and rosettes are large enough to examine.
5. **Screen rotation**: Sweep Screen Angle while watching the rosette pattern rotate and reconfigure.
6. **Compare shapes**: Toggle Dot Shape between Circle and Diamond. Notice how the rosette geometry changes — diamond dots create a tighter, more angular interleave.

**Key concepts**: CMY color separation requires three independently-rotated screens, angle spread creates the inter-screen rosette pattern, separation angle determines color mixing quality

---

### Exercise 3: Engraved Line Print

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: imprint_source1_ballerina, after: imprint_ex3_s1 },
    { label: "Runner", before: imprint_source2_runner, after: imprint_ex3_s2 },
    { label: "Elephant", before: imprint_source3_elephant, after: imprint_ex3_s3 },
    { label: "Pattern", before: imprint_source4_pattern, after: imprint_ex3_s4 },
    { label: "Girl", before: imprint_source5_girl, after: imprint_ex3_s5 },
    { label: "Wood", before: imprint_source6_wood, after: imprint_ex3_s6 },
  ]}
/>
*Engraved Line Print — simulated result across source images.*
**Source**: High-contrast footage — architectural details, text overlays, or strong geometric content.

**Objective**: Combine line screen mode with colored ink and paper for an engraved illustration effect.

1. **Enable line screen**: Set Line Screen to Lines. The dots are replaced by parallel ruled lines.
2. **Fine pitch**: Set Dot Pitch to step 1 (4-pixel lines) for dense, engraved-looking lines.
3. **Mono mode**: Set Color Mode to Mono for a single-ink engraving.
4. **Rotate**: Set Screen Angle to about 45° for diagonal ruling.
5. **Sepia on cream**: Set Ink Tint to ~45° (sepia). Set Paper Tint to ~45° (cream). The result resembles an antique copper-plate engraving.
6. **Invert for negativity**: Toggle Invert On. The bright/dark relationship reverses — lines appear as scratches of light against a dark ground.
7. **Full CMY lines**: Switch Color Mode back to CMY and increase Angle Spread to ~60%. Three sets of differently-angled ruled lines create a cross-hatched color engraving.

**Key concepts**: Line screen evaluates only the horizontal distance, creating ruled lines instead of dots, line width increases with source brightness, line crosshatching emerges from CMY angle spread

---


## Tips

- **Screen angle prevents moire**: Without rotation, the dot grid aligns with the video raster and produces distracting interference. Even a small rotation angle (5–15°) eliminates raster moire.
- **Angle spread creates color**: In CMY mode, the spread between screen angles is what makes the print colorful. At zero spread, the output is nearly monochrome. The traditional print industry uses carefully chosen angles to minimize moire between the color screens.
- **Large pitch for clarity, small pitch for detail**: The four pitch options (4/8/16/32 pixels) span from fine photographic halftone to coarse poster-print scale. Start with pitch 4 (32px) to understand the dot mechanics, then reduce pitch for production results.
- **Line screen for engravings**: Switching to line mode and rotating the screen creates ruled-line patterns that mimic copper-plate or steel-plate engraving — a highly distinctive look, especially in mono mode with sepia ink.
- **Paper and ink tints set the mood**: The 8×8 combination of paper and ink colors covers classic (sepia on cream), modern (black on white), and experimental (crimson on sky) print aesthetics without touching the halftone geometry itself.
- **Feedback loops**: Routing the output back to the input creates progressive halftone re-screening — the dot pattern is itself halftoned, producing a decreasing-scale fractal dot structure.
- **Bypass for A/B comparison**: Switch 11 instantly shows the original video for before/after comparison against the halftone output.
- **Mix for overlay effects**: Blending the halftone with the source at 30–50% mix creates a "printed overlay" effect where the dot texture is visible but the source video shows through.

---

## Glossary

| Term | Definition |
|------|------------|
| **CMYK** | Cyan, Magenta, Yellow, and Key (black); the four inks used in process color printing. Imprint implements CMY without explicit black (K). |
| **Distance Function** | A mathematical formula that computes the distance from a point to a reference location; used here to determine whether a pixel falls inside or outside a halftone dot. |
| **Dot Pitch** | The spacing between adjacent dot centres in the halftone grid, measured in pixels. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Halftone** | A reprographic technique that simulates continuous tones using dots of varying size, spacing, or density. |
| **Interpolator** | A linear crossfade module that blends between the dry (unprocessed) and wet (processed) signal paths based on the Mix fader position. |
| **LUT** | Look-Up Table; used here for both the sin/cos rotation coefficients and the paper/ink color palettes. |
| **Manhattan Distance** | The sum of absolute differences along each axis: |dx| + |dy|. Produces diamond-shaped equidistant contours. |
| **Moire** | An interference pattern that appears when two regular grids are overlaid at slightly different angles or frequencies. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Rosette Pattern** | The characteristic flower-like pattern visible under magnification in color halftone prints, created by the interaction of differently-angled dot screens. |
| **Screen Angle** | The rotation angle of a halftone dot grid relative to the horizontal axis, measured in degrees. |
| **Subtractive Color** | A color model where pigments or inks absorb (subtract) portions of the light spectrum; mixing C, M, and Y inks produces darker colors. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
