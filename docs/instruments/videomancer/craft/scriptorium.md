---
draft: true
sidebar_position: 263
slug: /instruments/videomancer/scriptorium
title: "Scriptorium"
image: /img/instruments/videomancer/scriptorium/scriptorium_hero_s1.png
description: "Before the printing press and before movable type, every book in Europe was made by hand."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import scriptorium_control_panel from '/img/instruments/videomancer/scriptorium/scriptorium_control_panel.png';
import scriptorium_source1_house from '/img/instruments/videomancer/scriptorium/scriptorium_source1_house.png';
import scriptorium_source2_fruit from '/img/instruments/videomancer/scriptorium/scriptorium_source2_fruit.png';
import scriptorium_source3_elephant from '/img/instruments/videomancer/scriptorium/scriptorium_source3_elephant.png';
import scriptorium_source4_pattern from '/img/instruments/videomancer/scriptorium/scriptorium_source4_pattern.png';
import scriptorium_source5_boy from '/img/instruments/videomancer/scriptorium/scriptorium_source5_boy.png';
import scriptorium_source6_knit from '/img/instruments/videomancer/scriptorium/scriptorium_source6_knit.png';
import scriptorium_hero_s1 from '/img/instruments/videomancer/scriptorium/scriptorium_hero_s1.png';
import scriptorium_hero_s2 from '/img/instruments/videomancer/scriptorium/scriptorium_hero_s2.png';
import scriptorium_hero_s3 from '/img/instruments/videomancer/scriptorium/scriptorium_hero_s3.png';
import scriptorium_hero_s4 from '/img/instruments/videomancer/scriptorium/scriptorium_hero_s4.png';
import scriptorium_hero_s5 from '/img/instruments/videomancer/scriptorium/scriptorium_hero_s5.png';
import scriptorium_hero_s6 from '/img/instruments/videomancer/scriptorium/scriptorium_hero_s6.png';
import scriptorium_ex1_s1 from '/img/instruments/videomancer/scriptorium/scriptorium_ex1_s1.png';
import scriptorium_ex1_s2 from '/img/instruments/videomancer/scriptorium/scriptorium_ex1_s2.png';
import scriptorium_ex1_s3 from '/img/instruments/videomancer/scriptorium/scriptorium_ex1_s3.png';
import scriptorium_ex1_s4 from '/img/instruments/videomancer/scriptorium/scriptorium_ex1_s4.png';
import scriptorium_ex1_s5 from '/img/instruments/videomancer/scriptorium/scriptorium_ex1_s5.png';
import scriptorium_ex1_s6 from '/img/instruments/videomancer/scriptorium/scriptorium_ex1_s6.png';
import scriptorium_ex2_s1 from '/img/instruments/videomancer/scriptorium/scriptorium_ex2_s1.png';
import scriptorium_ex2_s2 from '/img/instruments/videomancer/scriptorium/scriptorium_ex2_s2.png';
import scriptorium_ex2_s3 from '/img/instruments/videomancer/scriptorium/scriptorium_ex2_s3.png';
import scriptorium_ex2_s4 from '/img/instruments/videomancer/scriptorium/scriptorium_ex2_s4.png';
import scriptorium_ex2_s5 from '/img/instruments/videomancer/scriptorium/scriptorium_ex2_s5.png';
import scriptorium_ex2_s6 from '/img/instruments/videomancer/scriptorium/scriptorium_ex2_s6.png';
import scriptorium_ex3_s1 from '/img/instruments/videomancer/scriptorium/scriptorium_ex3_s1.png';
import scriptorium_ex3_s2 from '/img/instruments/videomancer/scriptorium/scriptorium_ex3_s2.png';
import scriptorium_ex3_s3 from '/img/instruments/videomancer/scriptorium/scriptorium_ex3_s3.png';
import scriptorium_ex3_s4 from '/img/instruments/videomancer/scriptorium/scriptorium_ex3_s4.png';
import scriptorium_ex3_s5 from '/img/instruments/videomancer/scriptorium/scriptorium_ex3_s5.png';
import scriptorium_ex3_s6 from '/img/instruments/videomancer/scriptorium/scriptorium_ex3_s6.png';

# Scriptorium

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "House", before: scriptorium_source1_house, after: scriptorium_hero_s1 },
    { label: "Fruit", before: scriptorium_source2_fruit, after: scriptorium_hero_s2 },
    { label: "Elephant", before: scriptorium_source3_elephant, after: scriptorium_hero_s3 },
    { label: "Pattern", before: scriptorium_source4_pattern, after: scriptorium_hero_s4 },
    { label: "Boy", before: scriptorium_source5_boy, after: scriptorium_hero_s5 },
    { label: "Knit", before: scriptorium_source6_knit, after: scriptorium_hero_s6 },
  ]}
/>
*Scriptorium compositing live video into the pictorial field of a procedurally generated illuminated manuscript with knotwork borders and mineral pigment quantization.*

---

## Overview

Before the printing press and before movable type, every book in Europe was made by hand. Monks and scribes working in the *scriptorium* — the writing room of a monastery — copied texts letter by letter onto prepared animal skins, embellishing important pages with ornamental borders, decorated initial capitals, and miniature paintings set into frames of gold leaf and mineral pigments. Scriptorium recreates this visual world inside the Videomancer pipeline.

The program divides the output frame into three concentric zones: an outer ornamental border filled with procedurally generated patterns, a thin frame line (optionally gilded), and a central pictorial field — the *miniature* — where the input video appears. The video in the miniature zone is quantized to a palette of eight medieval mineral pigments, collapsing continuous color into the flat, jewel-toned hues of a hand-painted manuscript. Bright areas can be replaced with gold leaf, and the entire output receives a subtle LFSR-driven parchment texture.

Four ornament algorithms are available — Insular knotwork, acanthus scroll, geometric fret, and diaper tiling — each generated procedurally from pixel-coordinate modular arithmetic. No BRAM is used; every visual element is computed from position and parameter values alone. The name references both the medieval writing room and the Latin *scriptor* — one who writes — placing the video artist in the role of illuminator.

---

## Background

### The Illuminated Manuscript Tradition

From roughly the 6th through the 15th century, the most elaborate books produced in Europe were *illuminated manuscripts* — texts decorated with gold leaf, painted borders, and miniature illustrations. The word "illuminate" comes from the Latin *illuminare*, meaning "to light up," referring to the way gold leaf catches and reflects light. Major centers of production included Insular monasteries (Ireland and Northumbria), Carolingian scriptoria, and later the courts of Burgundy and France. The Book of Kells, the Lindisfarne Gospels, and the Très Riches Heures du Duc de Berry represent pinnacles of the tradition.

### Mineral Pigment Palettes

Medieval painters worked with pigments ground from minerals, plants, and animal products. Ultramarine blue was made from lapis lazuli imported from Afghanistan — more expensive than gold. Vermillion came from cinnabar (mercury sulfide). Malachite provided green, yellow ochre came from iron-rich clay, and verdigris was derived from copper acetate. Lead white and lamp black completed the standard palette. These pigments produce saturated, opaque colors with a distinctive matte quality quite unlike modern synthetic paints. Scriptorium's palette quantization maps continuous video color to the nearest of these historical pigments.

### Interlace Knotwork

The Insular art tradition — centered in Ireland, Scotland, and Anglo-Saxon England — developed a distinctive vocabulary of interlaced ribbon patterns, spirals, and zoomorphic forms. Knotwork consists of bands that weave over and under one another in continuous loops with no beginning or end. Geometrically, these patterns arise from a grid of crossing points where each intersection alternates between over and under — precisely the XOR parity logic that Scriptorium implements in hardware.

### Gold Leaf Application

In manuscript illumination, gold leaf is applied before pigments in a process called *gilding*. A sticky ground (gesso or gum) is laid down, the gold is pressed onto it, and then burnished with an agate tool to achieve a mirror-like shine. *Flat gilding* produces a uniform matte gold surface, while *burnished gilding* creates a polished reflective surface that varies in brightness with viewing angle. Scriptorium's gold leaf substitution replaces pixels above a brightness threshold with a gold color, and the gilding toggle adds position-based brightness variation to simulate the burnished effect.

### Zone-Based Page Layout

Medieval manuscripts follow strict page layout conventions. The *mise en page* divides the folio into zones: margins (often decorated), a text block, and sometimes a separate pictorial field for the miniature painting. Scriptorium uses a simplified version of this hierarchy — border, frame line, and central miniature — controlled by a single width parameter. This three-zone approach captures the essential structure while remaining computationally tractable in a single-pass pipeline.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Zone Classification ───────────────────────────────
│   ├─ Compare h_count/v_count vs border_width thresholds
│   ├─ Zone 0 = border ornament (outside frame line)
│   ├─ Zone 1 = frame line (2-pixel border at edge of miniature)
│   └─ Zone 2 = miniature (central pictorial field)
│
├── Stage 2: Ornament + Palette ────────────────────────────────
│   ├─ Border ornament generation (4 algorithms via toggles):
│   │   ├─ Knotwork: modular position → horizontal/vertical band → XOR parity weave
│   │   ├─ Acanthus: piecewise-linear sine approximation → vine + leaf lobes
│   │   ├─ Fret: stepped Greek key from modular position bits
│   │   └─ Diaper: diagonal sum → repeating diamond/lozenge tiling
│   └─ Miniature zone: nearest-pigment quantization (Manhattan distance, up to 8 entries)
│
├── Stage 3: Gold Leaf + Zone Composite ────────────────────────
│   ├─ Border → ornament color
│   ├─ Frame line → gold (if enabled) or hue-tinted accent
│   └─ Miniature → gold substitution if luma > threshold, else quantized pigment
│
├── Stage 4: Vellum + Aging ────────────────────────────────────
│   ├─ LFSR grain overlay on Y, scaled by vellum amount
│   ├─ Warm parchment tint blend on U/V
│   └─ Aging toggle: darken Y by 25%, desaturate UV toward warm neutral
│
├── Interpolator: Wet/Dry Mix ──────────────────────────────────
│   └─ 3× interpolator_u: crossfade original ↔ processed (4 clocks)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline is purely feedforward with no feedback paths. Two key design decisions shape the output: (1) **Zone classification happens first**, so every subsequent stage knows whether it is rendering border, frame, or miniature content. The ornament generator and palette quantizer run in parallel during stage 2, each producing a candidate color for its respective zone. (2) **Vellum texture is applied globally** after zone compositing, so the parchment grain unifies all three zones with a consistent material quality. The aging toggle compounds with vellum — when active, the overall brightness drops by approximately 25% and chrominance is pulled toward a warm neutral, simulating centuries of oxidation and light exposure.

---

## Parameter Reference

<img src={scriptorium_control_panel} alt="Videomancer front panel with Scriptorium loaded"/>
*Videomancer's front panel with Scriptorium active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Border Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls the width of the ornamental border in pixels, mapped from the 10-bit register to a 0–128 pixel range. At zero, the entire frame is miniature — no border or frame line is visible. As the border widens, the central pictorial field shrinks and the ornamental margin grows. The frame line always sits at the inner edge of the border, so widening the border pushes the gold or tinted frame line inward as well.

---

#### Knob 2 — Ornament Scale
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the spatial frequency of the ornament pattern by controlling the modular tile period. Lower values produce finer, more densely packed ornament — tighter knotwork crossings, smaller acanthus lobes, narrower fret steps. Higher values produce larger, more open patterns. The ornament scale also determines the band width used in knotwork and the leaf lobe size in acanthus scroll mode.

---

#### Knob 3 — Color Depth
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

Controls how many entries from the medieval mineral palette are used for miniature zone quantization. At the lowest setting, only four pigments are available — ultramarine, vermillion, malachite, and ochre — producing bold, high-contrast posterization. At the highest setting, all eight pigments (including ivory, gold, lamp black, and lead white) are active, giving a subtler quantization with more tonal range.

---

#### Knob 4 — Gold Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 68.4% |
| Suffix | % |

Sets the luminance threshold above which pixels in the miniature zone are replaced with gold leaf color. At low values, only the very brightest highlights receive gold treatment. At high values, mid-tones and even darker regions are gilded, pushing more of the miniature toward a golden monochrome. When gold leaf is disabled (toggle 9), this parameter has no visible effect.

---

#### Knob 5 — Vellum
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Controls the intensity of the LFSR-driven parchment grain texture overlaid on the Y channel. At zero, the output is perfectly smooth. As vellum increases, a subtle noise modulates brightness across the entire frame — border, frame line, and miniature alike — simulating the fibrous surface texture of prepared calfskin or goatskin. The noise is broadband and uniform, unlike the structured patterns of the ornament zone.

---

#### Knob 6 — Frame Color
| Property | Value |
|----------|-------|
| Range | 0 – 360 |
| Default | 60 |

When gold leaf is disabled, this parameter controls the hue of the frame line accent by modulating the U and V channels of the frame line color. Sweeping the control rotates the accent through warm and cool tones. When gold leaf is enabled, the frame line uses gold instead and this parameter has no visible effect on the frame line. The underlying mechanism is a simple bipolar U/V shift derived from the pot position.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern A** | Knot | Scroll |
| **8 — Pattern B** | Geo | Diaper |
| **9 — Gold Leaf** | On | Off |
| **10 — Aging** | New | Aged |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 combine as a 2-bit selector to choose one of four ornament algorithms (Knotwork, Acanthus Scroll, Geometric Fret, Diaper). Toggle 9 enables or disables gold leaf substitution globally — affecting both the frame line and the miniature zone. Toggle 10 activates the aging effect, and toggle 11 provides bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) and wet (processed) signal via three interpolator_u instances. At 100% the full manuscript effect is visible. At 0% the original video passes through unaltered. Intermediate values blend the two, which can produce a ghostly overlay of the manuscript structure on top of recognizable video content.

---

## Guided Exercises

These exercises progress from basic page layout to full illuminated manuscript compositions. Each builds on the previous, gradually engaging more ornament modes, palette settings, and surface treatments.

### Exercise 1: Knotwork Page

<BeforeAfterSlider
  sources={[
    { label: "House", before: scriptorium_source1_house, after: scriptorium_ex1_s1 },
    { label: "Fruit", before: scriptorium_source2_fruit, after: scriptorium_ex1_s2 },
    { label: "Elephant", before: scriptorium_source3_elephant, after: scriptorium_ex1_s3 },
    { label: "Pattern", before: scriptorium_source4_pattern, after: scriptorium_ex1_s4 },
    { label: "Boy", before: scriptorium_source5_boy, after: scriptorium_ex1_s5 },
    { label: "Knit", before: scriptorium_source6_knit, after: scriptorium_ex1_s6 },
  ]}
/>
*Knotwork Page — simulated result across source images.*
**Source**: A slowly moving camera feed with moderate contrast — portraits or architectural subjects work well.

**Objective**: Learn how border width, ornament scale, and basic palette quantization interact to create a framed manuscript page.

1. **Set the border**: Turn Border Width to about 40%. A wide ornamental margin appears around the central video.
2. **Select knotwork**: Ensure Pattern A is set to Knot and Pattern B to Geo. The border fills with interlaced ribbon bands.
3. **Adjust scale**: Sweep Ornament Scale slowly. Watch the knotwork tile period change — small values produce dense weaving, large values produce open lattice.
4. **Reduce palette**: Set Color Depth to its lowest step. The miniature collapses to four pigments — bold, poster-like medieval colors.
5. **Add vellum**: Increase Vellum to about 30%. A subtle grain appears across the entire page, unifying border and miniature.

**Key concepts**: Zone classification divides the frame into border/frame/miniature, knotwork uses XOR parity for over-under weave, palette quantization maps continuous color to discrete mineral pigments

---

### Exercise 2: Gilded Miniature

<BeforeAfterSlider
  sources={[
    { label: "House", before: scriptorium_source1_house, after: scriptorium_ex2_s1 },
    { label: "Fruit", before: scriptorium_source2_fruit, after: scriptorium_ex2_s2 },
    { label: "Elephant", before: scriptorium_source3_elephant, after: scriptorium_ex2_s3 },
    { label: "Pattern", before: scriptorium_source4_pattern, after: scriptorium_ex2_s4 },
    { label: "Boy", before: scriptorium_source5_boy, after: scriptorium_ex2_s5 },
    { label: "Knit", before: scriptorium_source6_knit, after: scriptorium_ex2_s6 },
  ]}
/>
*Gilded Miniature — simulated result across source images.*
**Source**: High-contrast footage with bright highlights — candle flames, sunlit surfaces, or specular reflections.

**Objective**: Explore gold leaf substitution and how the threshold control sculpts which parts of the image become gold.

1. **Start with a knotwork border**: Keep Border Width at ~30% with Knotwork pattern.
2. **Enable gold leaf**: Confirm Gold Leaf toggle is On. Notice the frame line is now gold.
3. **Sweep Gold Threshold**: Start high (~90%) — only the brightest specular highlights become gold. Slowly lower the threshold. More and more of the miniature turns gold as mid-tones cross the threshold.
4. **Full palette**: Set Color Depth to its highest step. The non-gilded pigment areas now show the full eight-color palette.
5. **Add aging**: Toggle Aging to Aged. The entire page darkens and desaturates, giving the gold areas more visual prominence against the muted background.
6. **Compare toggles**: Switch Gold Leaf off. The frame line changes from gold to the hue accent, and the miniature shows only pigments — no gold anywhere.

**Key concepts**: Gold leaf substitution is threshold-based, the frame line responds to the gold toggle independently, aging compounds with gold to enhance contrast between gilded and painted areas

---

### Exercise 3: Four Ornament Comparison

<BeforeAfterSlider
  sources={[
    { label: "House", before: scriptorium_source1_house, after: scriptorium_ex3_s1 },
    { label: "Fruit", before: scriptorium_source2_fruit, after: scriptorium_ex3_s2 },
    { label: "Elephant", before: scriptorium_source3_elephant, after: scriptorium_ex3_s3 },
    { label: "Pattern", before: scriptorium_source4_pattern, after: scriptorium_ex3_s4 },
    { label: "Boy", before: scriptorium_source5_boy, after: scriptorium_ex3_s5 },
    { label: "Knit", before: scriptorium_source6_knit, after: scriptorium_ex3_s6 },
  ]}
/>
*Four Ornament Comparison — simulated result across source images.*
**Source**: Any slowly changing video — abstract patterns, landscapes, or color bars.

**Objective**: Compare all four ornament algorithms and understand how their visual character changes with scale.

1. **Wide border**: Set Border Width to ~60% so the ornament dominates the frame.
2. **Knotwork** (Knot + Geo): Observe the over-under interlaced bands. Note the two alternating colors at crossings.
3. **Acanthus Scroll** (Scroll + Geo): Toggle Pattern A to Scroll. The border changes to an undulating vine pattern with piecewise-linear sine approximation.
4. **Fret** (Knot + Diaper): Toggle Pattern A back to Knot, then set Pattern B to Diaper. A stepped Greek key meander appears in ochre tones.
5. **Diaper** (Scroll + Diaper): Toggle Pattern A to Scroll. The border fills with repeating diamond lozenges in purple and vermillion.
6. **Scale sweep**: For each pattern, sweep Ornament Scale through its full range. Each algorithm responds differently — knotwork changes crossing density, acanthus changes lobe width, fret changes step size, diaper changes diamond scale.
7. **Gold frame**: Toggle Gold Leaf on and off to see how the frame line interacts with each ornament style.

**Key concepts**: All four ornaments are procedural from coordinate modular arithmetic, pattern toggle bits form a 2-bit selector, ornament scale affects tile period uniformly across all four modes

---


## Tips

- **Border Width is your page layout**: Small borders create a picture-frame effect; large borders fill the screen with ornament and reduce the miniature to a small window.
- **Gold Threshold shapes the gilding**: Use high thresholds for subtle highlight-only gilding; use low thresholds for lavish all-over gold leafing.
- **Ornament Scale interacts with Border Width**: Narrow borders may not have enough pixels to show the ornament pattern clearly — use smaller ornament scales with narrow borders.
- **Color Depth controls the historical period**: Fewer pigments evoke early medieval manuscripts (6th–9th century); more pigments suggest the later Gothic and Renaissance styles.
- **Aging works best with gold**: The desaturation of aging makes gold areas stand out dramatically against muted pigment backgrounds, just as real gold on aged parchment catches the eye.
- **Vellum unifies the composition**: Even a small amount of vellum texture ties the procedural border ornaments to the quantized miniature, making the whole frame feel like a single material surface.
- **Mix for overlay effects**: Setting Mix to intermediate values blends the manuscript rendering over the original video, creating a translucent illumination overlay.
- **Feedback routing**: Sending the output back to the input creates recursive palette quantization — the color palette narrows further with each pass, eventually collapsing to the dominant pigment.

---

## Glossary

| Term | Definition |
|------|------------|
| **Acanthus** | A thorny Mediterranean plant whose scrolling leaf forms became a dominant ornamental motif in classical and medieval decorative arts. |
| **Burnished Gilding** | Gold leaf polished with an agate tool to achieve a mirror-like reflective surface, as opposed to flat (matte) gilding. |
| **Diaper Pattern** | A repeating geometric surface pattern of small diamond or lozenge shapes, common in medieval textiles and architectural decoration. |
| **Fret** | A continuous geometric border pattern of interlocking right-angle turns; also called Greek key or meander. |
| **Gilding** | The application of gold leaf or gold paint to a surface, used in manuscripts to highlight important text and borders. |
| **Insular Art** | The distinctive artistic tradition of early medieval Ireland and Britain, characterized by intricate interlace knotwork, spirals, and carpet pages. |
| **Knotwork** | Interlaced ribbon patterns that weave over and under in continuous loops, a hallmark of Insular and Celtic art. |
| **LFSR** | Linear Feedback Shift Register; a hardware-efficient pseudo-random number generator used here for vellum grain texture. |
| **Manhattan Distance** | The sum of absolute differences along each axis (|ΔY| + |ΔU| + |ΔV|); used for nearest-pigment color matching. |
| **Miniature** | In manuscript terminology, a small painting within the text, derived from the Latin *miniare* (to color with red lead), not from "small." |
| **Mise en Page** | French term for page layout — the arrangement of text, decoration, and illustration within the margins of a manuscript folio. |
| **Parchment** | Writing surface prepared from animal skin (calfskin = vellum, sheepskin = parchment proper), with a characteristic fibrous texture. |
| **Pigment** | A colored powder ground from minerals, plants, or animals, mixed with a binder to make paint. |
| **Scriptorium** | The writing room of a medieval monastery where manuscripts were copied and illuminated. |
| **Ultramarine** | A deep blue pigment historically made from ground lapis lazuli; the most expensive pigment in the medieval palette. |
| **Vellum** | Fine-quality parchment made from calfskin, valued for its smooth writing surface and durability. |
| **Vermillion** | A brilliant red pigment made from ground cinnabar (mercury sulfide), widely used in medieval illumination. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
