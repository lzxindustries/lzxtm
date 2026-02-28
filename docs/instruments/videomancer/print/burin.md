---
draft: true
sidebar_position: 30
slug: /instruments/videomancer/burin
title: "Burin"
image: /img/instruments/videomancer/burin/burin_hero.png
description: "Program guide for Burin, a Videomancer print program for the LZX video synthesizer."
---

import burin_hero from '/img/instruments/videomancer/burin/burin_hero.png';
import burin_before_after from '/img/instruments/videomancer/burin/burin_before_after.png';
import burin_control_panel from '/img/instruments/videomancer/burin/burin_control_panel.png';
import burin_exercise1_result from '/img/instruments/videomancer/burin/burin_exercise1_result.png';
import burin_exercise2_result from '/img/instruments/videomancer/burin/burin_exercise2_result.png';
import burin_exercise3_result from '/img/instruments/videomancer/burin/burin_exercise3_result.png';

# Burin

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={burin_hero} alt="Burin hero image"/>
*Burin rendering a video source as copper intaglio crosshatching, with luminance-dependent line density recreating the look of a Dürer engraving.*
<img src={burin_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Burin applied.*

---

## Overview

Every photograph contains continuous tonal gradations — smooth transitions from light to shadow. Before photography existed, engravers had to represent those transitions with nothing but lines cut into copper. The trick was systematic: sparse parallel lines for light areas, denser crosshatching for midtones, and interlocking diamond meshes for the deepest shadows. An entire vocabulary of marks, developed over centuries, could render any subject from a human face to a landscape using only ink and paper.

Burin applies that vocabulary to live video. It classifies each pixel's luminance into one of five tonal zones — paper white, first lines, crosshatch, triple-cross, and lozenge fill — and renders the appropriate hatching pattern at that location. The math is simple modular arithmetic on pixel coordinates: a set of parallel lines at angle θ is just the set of all points where the perpendicular distance to the nearest line is less than the stroke width. By evaluating four such line sets at different angles and combining them according to the luminance zone, the full crosshatching system emerges. The name comes from the *burin*, the V-shaped steel cutting tool used to engrave copper plates since the fifteenth century.

At conservative settings — wide spacing, a single primary angle, clean plate — Burin produces a subtle linear texture over the source. At aggressive settings — tight spacing, multiple crossing angles, worn plate, inverted — the video dissolves into dense networks of broken strokes that recall late impressions pulled from a heavily-used copper plate.

---

## Background

### Intaglio Engraving and the Burin

Intaglio printing was developed in the Rhine Valley around 1430. The technique is the inverse of woodcut: instead of cutting away non-printing areas, the engraver pushes a burin — a small steel rod with a lozenge-shaped cutting tip — directly into a polished copper plate. The incised grooves hold ink when the surface is wiped clean, and under the enormous pressure of a rolling press, the ink transfers from grooves to dampened paper. The word *intaglio* comes from the Italian *intagliare*, to cut in. The depth, width, and spacing of the cuts determine how much ink each groove holds and therefore how dark it prints.

### The Crosshatching Vocabulary

The earliest engravers — the anonymous Master of the Playing Cards and his successor Martin Schongauer — discovered that tonal modelling could be built from systems of parallel lines. A shadow could be suggested by a single set of closely-spaced strokes. A deeper shadow required a second set of lines crossing the first at an angle, creating a grid. The darkest passages demanded three or even four overlapping sets, producing a dense mesh where only tiny diamond-shaped highlights (lozenges) of paper remained visible. This four-level system — first lines, crosshatch, triple-cross, and lozenge fill — became the standard tonal vocabulary of copper engraving for the next four hundred years.

### Dürer and the Systematization of Line

Albrecht Dürer, working in Nuremberg from the 1490s onward, brought mathematical precision to the crosshatching system. His engravings demonstrate a rigorous angular discipline: first lines follow the form of the subject (curving around a cheek or along a fold of drapery), and each successive crossing set is laid at a consistent angular offset. The result is a surface that reads simultaneously as a tonal image and as a woven texture of individually legible strokes. Dürer's *Melencolia I* (1514) is often cited as the summit of the technique — every shadow is built from identifiable line sets whose angle, spacing, and width vary continuously across the plate.

### Marcantonio Raimondi and Reproductive Engraving

While Dürer used engraving as a primary creative medium, Marcantonio Raimondi pioneered its use as a reproductive technology. Working in Rome from about 1510, Raimondi translated paintings by Raphael and others into copper engravings for mass distribution. His crosshatching had to encode not just tone but also the character of painted surfaces — the softness of skin, the hardness of armour, the transparency of drapery. Raimondi's solution was to vary line spacing and crossing angle systematically with luminance, producing prints that conveyed the tonal structure of the original painting with remarkable fidelity.

### From Copper to Computation

Burin's computational approach mirrors the engraver's physical process. The pixel coordinate system replaces the copper plate. Modular arithmetic on coordinates produces parallel line sets at controlled angles, just as the burin produces parallel grooves at controlled spacing. The luminance classifier determines how many line sets to activate at each point, just as the engraver decides how many crossing directions a given shadow requires. The plate wear toggle adds stochastic line breaks via an LFSR noise source, simulating the gradual degradation of a copper plate over hundreds of impressions.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Luminance Zone Classifier
│   │      Zone 0: Y >= 800 → paper white (no lines)
│   │      Zone 1: 600 <= Y < 800 → first lines
│   │      Zone 2: 400 <= Y < 600 → crosshatch
│   │      Zone 3: 200 <= Y < 400 → triple-cross
│   │      Zone 4: Y < 200 → lozenge fill
│   │
│   ├─ 2. Line Set Evaluation (×4)
│   │      d = f(x, y, angle) mod spacing
│   │      is_line = (d < line_width)
│   │      Set 1: primary angle (pot 3)
│   │      Set 2: primary + cross offset (pot 4)
│   │      Set 3: primary + 2× cross offset
│   │      Set 4: primary + 3× cross offset
│   │
│   ├─ 3. Zone Combiner + Plate Wear + Ink/Paper Render
│   │      Zone 0 → hatched = 0
│   │      Zone 1 → line_1
│   │      Zone 2 → line_1 OR line_2
│   │      Zone 3 → line_1 OR line_2 OR line_3
│   │      Zone 4 → line_1 OR line_2 OR line_3 OR line_4
│   │      Plate wear: LFSR AND-gates break lines randomly
│   │      Hatched → ink YUV, else → paper YUV
│   │
│   └─ 4. Output Compose
│          Duotone: blend input chroma into hatched areas
│          Feathered: soften ink toward paper
│          Invert: 1023 - Y
│
├── Mix ────────────────────────────────────────────────────────
│   └─ Interpolate processed ↔ original (fader 12)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline is purely combinational on pixel coordinates — no BRAM or framebuffer is used. The critical interaction is between the luminance zone classifier and the line set combiner: the zone determines *how many* line sets contribute to each pixel, while the line spacing and primary angle controls determine *where* those lines fall. Plate wear acts as a stochastic AND-gate on each line set's output, breaking continuous strokes into fragments. The duotone mode preserves input chrominance in hatched areas, allowing color information from the source to bleed through the engraving texture.

---

## Parameter Reference

<img src={burin_control_panel} alt="Videomancer front panel with Burin loaded"/>
*Videomancer's front panel with Burin active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Spacing
| Property | Value |
|----------|-------|
| Range | 2 – 24 |
| Default | 13 |

Controls the spacing between parallel lines in all four hatching sets simultaneously. The control is quantized to eight steps — the resulting pixel spacings are 3, 4, 6, 8, 10, 12, 16, and 24 pixels. At the tightest spacing, lines are so close together that even single-direction hatching produces a dense, near-solid tone. At the widest spacing, individual strokes are clearly separated and the paper shows through prominently. Spacing interacts directly with line width: a narrow line at wide spacing produces delicate, airy hatching; the same line at tight spacing fills most of the available space.

---

#### Knob 2 — Line Width
| Property | Value |
|----------|-------|
| Range | 1px – 12px |
| Default | 4px |
| Suffix | px |

Sets the width of each engraved stroke. At minimum, lines are a single pixel wide — thin, precise, and reminiscent of fine-point burin work. At maximum, lines swell to fill most of the inter-line gap, producing heavy, saturated strokes. Line width is constant across all four sets and all five luminance zones, mirroring the physical constraint of a burin cut at fixed depth.

---

#### Knob 3 — Primary Angle
| Property | Value |
|----------|-------|
| Range | 0° – 157° |
| Default | 39° |
| Suffix | ° |

Selects the primary hatching angle from eight compass directions: 0° (horizontal), 22.5°, 45°, 67.5°, 90° (vertical), 112.5°, 135°, and 157.5°. This angle defines the orientation of the first line set — the lines that appear in the lightest shadow zone. All other sets derive their angles from this primary direction plus the cross angle offset. Diagonal angles (45° and 135°) produce the most visually familiar engraving textures; horizontal and vertical produce a more mechanical, ruled appearance.

---

#### Knob 4 — Cross Angle
| Property | Value |
|----------|-------|
| Range | 30° – 90° |
| Default | 60° |
| Suffix | ° |

Sets the angular offset between successive line sets, quantized to four steps: 30°, 45°, 60°, and 90°. A 45° cross angle with a 45° primary produces the classic Dürer crosshatch — diagonal strokes crossed by perpendicular strokes. A 30° offset creates tighter crossing angles that fill shadows more gradually. A 90° offset places all sets orthogonal to their neighbours, producing open grid patterns with prominent lozenge shapes in the darkest zones.

---

#### Knob 5 — Paper Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 45° |
| Suffix | ° |

Adds a warm or cool tint to the paper (non-hatched) areas. At zero, the paper is neutral white. Rotating the control shifts the paper hue through a full 360° colour cycle — cream, aged yellow, pink, cool blue, and back. Subtle settings simulate the off-white tone of antique laid paper; extreme settings produce coloured grounds reminiscent of chiaroscuro woodcuts printed on tinted stock.

---

#### Knob 6 — Ink Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Tints the ink (hatched line) colour. At default, ink is near-black. Rotating shifts through warm sepia and bistre tones (historically accurate for iron gall ink), through blues (reminiscent of cyanotype), reds, and greens. Combined with the paper tint, this creates a full two-colour printing effect — ink on coloured paper — using hue alone.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Line Style** | Sharp | Feathered |
| **8 — Plate Wear** | Clean | Worn |
| **9 — Color** | Single Ink | Duotone |
| **10 — Invert** | Normal | Invert |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent binary processing options. Line Style and Plate Wear affect the character of individual strokes; Color and Invert affect the final rendering; Bypass routes signal around all processing. These switches can be combined freely — feathered lines with plate wear and duotone, for example, produce a weathered two-colour print effect.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet mix between the processed engraving output and the original input video, via three parallel interpolators (Y, U, V). At 100%, only the engraved rendering is visible. At 0%, the original signal passes through unchanged. Intermediate values overlay the hatching texture onto the source at reduced opacity, which can produce a subtle sketch-over-video effect.

---

## Guided Exercises

These exercises build from basic line hatching through the full crosshatching vocabulary to coloured plate printing. Each introduces additional controls and reveals how Burin's parameters interact to create the engraving effect.

### Exercise 1: First Lines and Crosshatch

<img src={burin_exercise1_result} alt="First Lines and Crosshatch result"/>
*First Lines and Crosshatch — simulated result across source images.*
**Source**: A portrait or figure with clear tonal transitions — skin highlights through deep shadows.

**Objective**: Learn how the primary angle, spacing, and luminance zones produce the basic hatching vocabulary.

1. **Prepare**: Set Spacing to step 5 (~10px), Line Width to ~25%, Primary Angle to 45°, all toggles off, Mix at 100%.
2. **Observe zones**: Look at the image. The brightest areas should be clean paper (zone 0). Mid-highlights show a single set of diagonal lines (zone 1). Midtones show crosshatching (zone 2). Shadows show dense triple-cross (zone 3) and lozenges (zone 4).
3. **Change angle**: Sweep Primary Angle through all eight steps. Watch how the hatching direction rotates. At 0° you get horizontal lines; at 90°, vertical; at 45° and 135°, classic diagonals.
4. **Adjust spacing**: Move through the eight spacing steps. Tight spacing fills tone densely; wide spacing produces open, airy hatching.
5. **Cross angle**: Switch Cross Angle between 30°, 45°, 60°, and 90°. Notice how the crosshatch diamond shape changes — tighter angles produce elongated diamonds, 90° produces squares.

**Key concepts**: Luminance zones control which line sets are active; primary angle sets the dominant stroke direction; cross angle determines the shape of the crosshatch pattern

---

### Exercise 2: Plate Character and Wear

<img src={burin_exercise2_result} alt="Plate Character and Wear result"/>
*Plate Character and Wear — simulated result across source images.*
**Source**: A scene with a full tonal range — outdoor landscape or still life with highlights and deep shadows.

**Objective**: Explore how line style, plate wear, and paper/ink tint create the character of a printed impression.

1. **Baseline**: Set Spacing to step 4 (~8px), Line Width to ~35%, Primary Angle to 135°, Cross Angle to 45°.
2. **Feathered lines**: Toggle Line Style to Feathered. The strokes soften, becoming lighter and less harsh. Compare against Sharp.
3. **Plate wear**: Toggle Plate Wear to Worn. Individual strokes break into fragments — the engraving looks like a late impression. The effect is most visible in high-density areas (zones 3 and 4).
4. **Paper tint**: Slowly rotate Paper Tint. The background colour shifts from white through cream, yellow, pink. Settle on a warm cream (~30°) to simulate antique paper.
5. **Ink tint**: Rotate Ink Tint to ~180° (the default is near-black at 0°). The ink shifts to warm sepia. Try a deep brown (~40°) for a historically accurate appearance.
6. **Combine**: Feathered + Worn + warm tints produces a weathered, centuries-old print aesthetic.

**Key concepts**: Feathered mode lightens ink to simulate shallow cuts; plate wear breaks lines stochastically via LFSR noise; paper and ink tints create two-colour printing effects

---

### Exercise 3: Duotone and Inversion

<img src={burin_exercise3_result} alt="Duotone and Inversion result"/>
*Duotone and Inversion — simulated result across source images.*
**Source**: High-contrast material — a face lit from one side, or any source with both saturated colour and strong shadows.

**Objective**: Use duotone and invert to push the engraving beyond monochrome reproduction into colour and negative territory.

1. **Prepare**: Set Spacing to step 3 (~6px), Line Width to ~30%, Primary Angle to 45°, Cross Angle to 60°, clean plate, sharp lines.
2. **Enable duotone**: Toggle Color to Duotone. The hatched lines now carry the source video's chrominance — colour bleeds through the engraving texture. Reds, blues, and greens appear within the hatched strokes.
3. **Mix overlay**: Lower the Mix fader to ~60%. The engraving texture overlays the source at partial opacity — a sketch-over-video effect.
4. **Invert**: Toggle Invert to On. The engraving flips — bright lines on a dark ground. With duotone active, the source colour now appears in the light strokes against a dark field, resembling a white-line wood engraving or a mezzotint.
5. **Paper and ink tint in invert mode**: Adjust Paper Tint and Ink Tint. Because luminance is inverted, the visual role of paper and ink reverse — paper tint now colours the dark background, and ink tint colours the bright lines.

**Key concepts**: Duotone blends source chrominance into hatched areas; invert flips the tonal relationship; mix allows partial overlay of engraving on source

---


## Tips

- **Spacing and width are the master controls**: Together they determine the overall density of the engraving. Set these first, then adjust angles and tints to taste.
- **45° primary with 45° cross is the classic look**: This combination produces the most recognizable copperplate crosshatch pattern — the one you see in Dürer prints and on currency.
- **Plate wear adds realism at any spacing**: Even subtle wear — a few broken strokes per line — makes the output look like a physical print rather than a computer rendering.
- **Duotone preserves source identity**: When you want the subject to remain recognizable through the hatching, duotone lets the source colour information survive the engraving process.
- **Invert for mezzotint aesthetics**: Inverting produces bright lines on dark ground — the opposite of normal engraving, closer to mezzotint or white-line woodcut. Especially dramatic with tight spacing and warm ink tint.
- **Mix for sketch overlay**: Pulling the fader back to 50–70% overlays the hatching texture onto the source video, creating a drawing-over-footage effect.
- **Feedback routing**: Sending Burin's output back to its input creates recursive crosshatching — each pass adds another layer of line structure, filling the image with increasingly complex woven textures.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bistre** | A warm brown pigment made from wood soot, historically used as a drawing ink and wash medium. |
| **Burin** | A V-shaped steel cutting tool used to engrave lines directly into a copper plate for intaglio printing. |
| **Chiaroscuro** | An art technique emphasizing strong contrasts between light and dark to model three-dimensional form. |
| **Chrominance** | The color information (U and V channels) in a video signal, independent of brightness. |
| **Crosshatching** | A shading technique using two or more sets of intersecting parallel lines to represent tonal gradations. |
| **Duotone** | A rendering mode that combines two color sources — here, the engraving ink color and the source video's chrominance. |
| **Intaglio** | A family of printmaking techniques where the image is incised into a surface; ink is held in the grooves and transferred under pressure. |
| **LFSR** | Linear Feedback Shift Register; a hardware pseudo-random number generator used here to create stochastic plate wear effects. |
| **Lozenge** | A small diamond-shaped area of unprinted paper visible in the densest crosshatch zones where four line sets overlap. |
| **Luminance** | The brightness component (Y channel) of a YUV video signal, measured on a 0–1023 scale in 10-bit video. |
| **Mezzotint** | An intaglio printmaking technique that produces tonal images by working from dark to light, creating white lines on a dark ground. |
| **YUV** | A color encoding system separating luminance (Y) from two chrominance components (U, V), used as the native format in video processing. |

---
