---
draft: true
sidebar_position: 260
slug: /instruments/videomancer/scriptorium
title: "Scriptorium"
image: /img/instruments/videomancer/scriptorium/scriptorium_hero_s1.png
description: "Before the printing press and before movable type, every book in Europe was made by hand."
---

![Scriptorium hero image](/img/instruments/videomancer/scriptorium/scriptorium_hero_s1.png)
*Scriptorium rendering a live video feed as an illuminated manuscript page with knotwork borders, mineral palette quantization, and gold leaf highlights.*

---

## Overview

Scriptorium transforms your video into a page from a medieval illuminated manuscript. The incoming image is framed within a procedurally generated ornamental border, its colors reduced to a palette of eight historical mineral pigments, and its brightest areas optionally replaced with shimmering gold leaf. A subtle parchment grain texture blankets the entire composition, as though the image were painted onto vellum.

The program divides the screen into three zones: the border ornament, a narrow frame line separating border from image, and the central ***miniature***: the manuscript term for the pictorial field where your video appears. Four border ornament styles are available, drawn from the traditions of Insular, Classical, and Islamic manuscript decoration. Inside the miniature, palette quantization maps every pixel to its nearest match in an eight-color set inspired by the actual mineral pigments used by medieval scribes.

At gentle settings, Scriptorium adds a warm, hand-painted quality to any video source. At extreme settings, it reduces the image to flat blocks of ultramarine, vermillion, malachite, ochre, ivory, gold, lamp black, and lead white: surrounded by ornate geometric borders: creating a striking fusion of ancient craft and electronic signal.

:::tip
Scriptorium uses ***zero block RAM***. Every pattern: knotwork, scrollwork, fret, and diaper tiling: is generated procedurally from coordinate arithmetic, so the entire FPGA memory budget remains free for other programs in the signal chain.
:::

### What's In a Name?

A ***scriptorium*** was the dedicated writing room in a medieval monastery where monks copied and illustrated manuscripts by hand. Every page was a collaboration: scribes lettered the text, and ***illuminators*** painted the decorative borders and miniature illustrations using pigments ground from minerals, plants, and precious metals. The name places you in that quiet workshop, transforming your video signal the way an illuminator transforms a blank page (one brushstroke of color at a time.)

---

## Quick Start

1. Turn **Border Width** (Knob 1) clockwise to about 40%. A colored ornamental border appears around the edges of the screen, framing your video in a rectangular margin filled with interlaced knotwork.
2. Slowly turn **Color Depth** (Knob 3) counterclockwise. The colors in your video snap to a smaller and smaller set of flat mineral tones: you are watching the palette shrink from eight pigments down to four.
3. Turn **Gold Threshold** (Knob 4) counterclockwise until bright areas of the image flash to a rich gold. You have just applied gold leaf to the highlights of your miniature.

---

## Parameters

![Videomancer front panel with Scriptorium loaded](/img/instruments/videomancer/scriptorium/scriptorium_control_panel.png)
*Videomancer's front panel with Scriptorium active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Border Width

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |

**Border Width** controls the size of the ornamental margin surrounding the central miniature. At 0%, the border vanishes and the miniature fills the entire screen. As you turn the knob clockwise, the border grows inward from all four edges, steadily shrinking the pictorial field. At 100%, the border is at its widest, leaving a small window of processed video in the center.

The border zone is filled with one of four procedural ornament patterns (selected by toggles 7 and 8). A narrow frame line: two pixels wide: separates the ornament from the miniature, drawn in gold when **Gold Leaf** is enabled or tinted by the **Frame Color** hue when gold is disabled.

:::note
Border Width is resolution-adaptive. The same knob position produces a visually proportional margin at both SD and HD resolutions.
:::

---

### Knob 2 — Ornament Scale

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Ornament Scale** controls the repetition frequency of the border ornament pattern. At low values, the pattern tiles are large and the ornament appears coarse. Increasing the knob clockwise makes the tiles smaller and more numerous, producing denser, more intricate decoration. The underlying tile period ranges from about 8 pixels to 48 pixels.

This control also influences the band width within each tile: the visible thickness of the interlaced strands in knotwork mode, the vine width in scroll mode, and the line weight in geometric fret mode.

---

### Knob 3 — Color Depth

| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

**Color Depth** selects how many entries from the medieval mineral palette are used to quantize the miniature. The knob sweeps through four stepped values. At step 1, only four pigments are available: ultramarine, vermillion, malachite, and ochre. At step 2, ivory is added. At step 3, gold joins the set. At step 4, all eight pigments are active: including lamp black and lead white: giving the widest tonal range.

Each pixel in the miniature is matched to the nearest palette entry by ***Manhattan distance*** in YUV color space. Reducing the palette produces flat, poster-like areas of color reminiscent of actual manuscript painting, where the illuminator had only a handful of pigments on the palette.

:::tip
Dropping **Color Depth** to step 1 while feeding a colorful source creates bold, graphic results: every pixel is forced to one of four mineral tones.
:::

---

### Knob 4 — Gold Threshold

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 68.4% |

**Gold Threshold** determines the luminance level above which pixels in the miniature are replaced with gold leaf. At 0%, even moderately bright pixels receive gold treatment. At 100%, only the absolute brightest peaks are gilded. The default position sits high, applying gold sparingly to specular highlights and white regions.

When **Gold Leaf** (Toggle 9) is set to Off, this control has no visible effect (the gold substitution stage is bypassed entirely.)

---

### Knob 5 — Vellum

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |

**Vellum** controls the intensity of a parchment grain texture applied to the entire output: border, frame, and miniature alike. The texture is generated by a 16-bit ***linear feedback shift register*** (LFSR) producing pseudo-random noise, which modulates the luminance channel with a warm, organic randomness.

At 0%, the texture is imperceptible. Increasing the knob introduces subtle brightness variations that simulate the irregular surface of animal-skin parchment. At high values, the grain becomes coarse and visible as splotchy, sandy noise.

:::note
Vellum also applies a gentle warm tint to the chrominance channels, shifting the entire image slightly toward the creamy tone of aged parchment (even at low settings.)
:::

---

### Knob 6 — Frame Color

| Property | Value |
|----------|-------|
| Range | 0 – 360 |
| Default | 60 |

**Frame Color** sets the accent hue of the narrow frame line that separates the border ornament from the miniature. This control is active only when **Gold Leaf** (Toggle 9) is set to Off; when gold is enabled, the frame line is drawn in gold regardless of this knob's position.

The hue sweeps through 360° of color. The frame line itself is drawn at a fixed low luminance (dark), so the result is a deeply saturated accent line: think of the thin colored rules that separate text columns and illustrations in medieval manuscripts.

---

### Switch 7 — Pattern A

| Property | Value |
|----------|-------|
| Off | Knot |
| On | Scroll |
| Default | Knot |

**Pattern A** selects between two ornament families for the border region. Set to **Knot**, the border displays an Insular-style ***knotwork*** pattern: horizontal and vertical bands interlace in a woven grid, with an over-under crossing effect created by toggling color between warm and cool bands at each cell parity. Set to **Scroll**, the border displays an ***acanthus scroll***: an undulating vine that snakes vertically through the margin, created by a piecewise-linear sine approximation.

Pattern A combines with **Pattern B** (Toggle 8) to select one of four ornament modes.

---

### Switch 8 — Pattern B

| Property | Value |
|----------|-------|
| Off | Geo |
| On | Diaper |
| Default | Geo |

**Pattern B** selects the second ornament family pair. Set to **Geo**, the border displays a ***geometric fret***: a stepped, angular meander inspired by Greek key patterns. Set to **Diaper**, the border fills with a ***diaper pattern***: a repeating lattice of diamond lozenges in alternating colors, common in Gothic manuscript backgrounds.

---

### Switch 9 — Gold Leaf

| Property | Value |
|----------|-------|
| Off | On |
| On | Off |
| Default | On |

**Gold Leaf** enables or disables the gold leaf substitution stage. When set to **On**, two things happen: bright pixels in the miniature that exceed the **Gold Threshold** are replaced with a rich gold color, and the frame line surrounding the miniature is drawn in gold. When set to **Off**, the miniature passes through ungilded, and the frame line color is determined by the **Frame Color** knob instead.

Gold leaf was the single most expensive material in a medieval scriptorium. Sheets of real gold were hammered impossibly thin and applied to the page with gum arabic before the surrounding pigments were painted. Scriptorium's digital gold leaf captures that sense of precious, luminous accent.

---

### Switch 10 — Aging

| Property | Value |
|----------|-------|
| Off | New |
| On | Aged |
| Default | New |

**Aging** simulates the visual deterioration of an ancient manuscript. When set to **New**, the output retains its full brightness and saturation. When set to **Aged**, luminance is reduced to 75% of its original value and chrominance is pushed halfway toward neutral, producing the faded, desaturated appearance of a page that has spent centuries in a monastery library.

The aging effect also introduces a subtle warm bias to the chrominance, shifting the overall color cast toward the yellowed tone of oxidized vellum.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Scriptorium processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant comparison between the raw source and the illuminated result.

---

:::note Toggle Group Notes

Toggles 7 and 8 combine as a two-bit binary selector to choose one of four ornament modes:

| Pattern A | Pattern B | Ornament |
|-----------|-----------|----------|
| Knot | Geo | Insular knotwork (interlaced horizontal and vertical bands) |
| Scroll | Geo | Acanthus scroll (sinusoidal vine) |
| Knot | Diaper | Geometric fret (Greek key meander) |
| Scroll | Diaper | Diaper pattern (repeating diamond tiling) |

:::tip
Each ornament mode has its own color identity: knotwork alternates warm and cool bands, scroll uses malachite green, fret uses ochre, and diaper alternates purple and vermillion. Try each one to find the palette that best complements your source material.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) and wet (fully processed) signals. At 0%, the output is the original input: identical to Bypass. At 100%, the output is fully illuminated. Intermediate positions blend the two, creating a ghostly overlay of the manuscript page on the original footage.

:::tip
Setting **Mix** around 50% lets the original video show through the manuscript treatment like a translucent palimpsest (a ghostly double-exposure of the modern and the medieval.)
:::

---

## Background

### Medieval manuscript illumination

***Illuminated manuscripts*** are handwritten books decorated with gold, silver, and vivid mineral pigments. Produced primarily between the 5th and 16th centuries in Europe and the Islamic world, they represent some of the most labor-intensive artworks ever created. A single decorated page could take weeks. The illuminator's toolkit was modest: a few brushes, a grinding stone, and a palette of natural pigments extracted from minerals, plants, and insects.

Scriptorium's eight-color palette draws from historically documented pigments: ***ultramarine*** (ground lapis lazuli, the most expensive pigment in the world), ***vermillion*** (mercuric sulfide), ***malachite*** (copper carbonate), ***ochre*** (iron oxide), ***ivory*** (bone ash), ***gold*** (hammered leaf), ***lamp black*** (carbon soot), and ***lead white*** (basic lead carbonate). Each pigment had its own preparation, cost, and cultural significance.

### Ornamental traditions

The four border ornament modes correspond to real decorative traditions:

- **Knotwork**: From the Insular tradition (Irish and Anglo-Saxon art, 6th–9th century). Interlaced bands weave over and under one another in an endless pattern with no beginning and no end (symbolizing eternity.)
- **Acanthus scroll**: From Classical and Romanesque traditions. A sinuous vine bearing stylized leaves, representing natural growth and abundance.
- **Geometric fret**: Inspired by the Greek key or meander pattern, one of the oldest ornamental motifs in the world, symbolizing infinity and the eternal flow of life.
- **Diaper pattern**: Common in Gothic manuscripts (13th–15th century). A repeating diamond lattice filled with alternating colors, used as a background behind figures and text.

### Palette quantization

Scriptorium's color reduction works by ***nearest-neighbor quantization*** in YUV color space. For each pixel in the miniature, the program computes the Manhattan distance to every active palette entry and selects the closest match. The computation is split across two pipeline stages: entries 0–3 in one clock, entries 4–7 in the next: to meet timing on the iCE40 FPGA.

The result is a hard-edged, posterized color field that mirrors the flat, unmixed quality of real tempera painting on vellum. Medieval illuminators did not blend colors on the page; each pigment was applied in discrete, opaque strokes.


---

## Signal Flow

### Signal Flow Notes

The program's architecture is built around the zone classification in Stage 1. Every pixel is sorted into one of three zones: border ornament, frame line, or miniature: and that zone tag follows the pixel through the entire pipeline. The ornament generator and palette quantizer run in parallel on their respective data, and the results are merged in the gold/composite stage according to each pixel's zone.

Two cross-domain interactions are especially worth noting. First, the **Gold Leaf** toggle simultaneously controls both the miniature (bright pixels replaced by gold) and the frame line (rendered in gold vs. the Frame Color hue). This makes the gold effect feel holistic, as though an illuminator applied gold leaf to both the border and the highlights in one pass. Second, the **Vellum** texture is applied after zone compositing, so it unifies the entire composition under a single parchment grain: ornament and miniature share the same surface texture, reinforcing the illusion that everything was painted on the same physical page.


---

## Exercises

These exercises progress from simple framing to full manuscript illumination. Each builds on the previous, engaging more of the processing chain.
### Exercise 1: Bordered Miniature

![Bordered Miniature result](/img/instruments/videomancer/scriptorium/scriptorium_ex1_s1.png)
*Bordered Miniature — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Frame a video source inside a knotwork border, creating a simple illuminated manuscript page.

#### Key Concepts

- Zone classification divides the screen into ornament, frame, and miniature
- Border Width and Ornament Scale control the ornamental margin
- Pattern toggles select one of four ornament traditions

#### Video Source

A live camera feed or recorded footage with a clearly visible subject in the center of the frame.

#### Steps

1. **Create the border**: Turn **Border Width** (Knob 1) to about 40%. A knotwork border appears around the video.
2. **Adjust ornament density**: Sweep **Ornament Scale** (Knob 2) from low to high. Watch the knotwork tiles become smaller and more intricate.
3. **Try each ornament**: Flip **Pattern A** (Toggle 7) to **Scroll**: the knotwork becomes a sinuous vine. Flip **Pattern B** (Toggle 8) to **Diaper**: now you see a diamond lattice. Try all four combinations.
4. **Adjust the frame width**: Return to knotwork (both toggles in their first position) and sweep Border Width slowly to find a proportional frame for your subject.

#### Settings

| Control | Value |
|---------|-------|
| Border Width | ~40% |
| Ornament Scale | ~50% |
| Color Depth | 4 (all 8 pigments) |
| Gold Threshold | ~70% |
| Vellum | ~30% |
| Frame Color | ~170° |
| Pattern A | Knot |
| Pattern B | Geo |
| Gold Leaf | On |
| Aging | New |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Gilded Palette

![Gilded Palette result](/img/instruments/videomancer/scriptorium/scriptorium_ex2_s1.png)
*Gilded Palette — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Reduce your video to a handful of medieval pigments with gold leaf highlights, creating a richly colored manuscript illumination.

#### Key Concepts

- Palette quantization maps video to mineral pigments
- Gold Threshold controls which brightness levels receive gold leaf
- Color Depth limits the pigment count

#### Video Source

Footage with a range of brightness levels: faces, landscapes, or still life with specular highlights work well.

#### Steps

1. **Start from Exercise 1 settings** with a knotwork border.
2. **Reduce the palette**: Turn **Color Depth** (Knob 3) counterclockwise to step 1 (4 pigments). The video snaps to bold blocks of ultramarine, vermillion, malachite, and ochre.
3. **Apply gold**: Turn **Gold Threshold** (Knob 4) counterclockwise until bright areas: specular highlights, white clothing, sky: turn to gold. Notice how the frame line is also gold.
4. **Disable gold**: Flip **Gold Leaf** (Toggle 9) to **Off**. The gold vanishes from both the miniature and the frame line. Sweep **Frame Color** (Knob 6) to choose an accent hue for the frame.
5. **Increase palette**: Slowly step Color Depth back up to step 4. Watch the palette expand: ivory appears, then gold, then black and white. The image gains tonal depth.

#### Settings

| Control | Value |
|---------|-------|
| Border Width | ~30% |
| Ornament Scale | ~50% |
| Color Depth | 1 (4 pigments) |
| Gold Threshold | ~50% |
| Vellum | ~30% |
| Frame Color | ~170° |
| Pattern A | Knot |
| Pattern B | Geo |
| Gold Leaf | On |
| Aging | New |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Aged Manuscript

![Aged Manuscript result](/img/instruments/videomancer/scriptorium/scriptorium_ex3_s1.png)
*Aged Manuscript — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Combine all Scriptorium features to produce a weathered, centuries-old manuscript page with visible parchment grain and faded pigments.

#### Key Concepts

- Vellum texture unifies border and miniature under a single grain
- Aging desaturates and dims the output
- Mix blends the manuscript with the original source

#### Video Source

Any footage with moderate color and contrast: portraits or interior scenes create an intimate, personal manuscript page.

#### Steps

1. **Set a wide border**: **Border Width** ~50%, **Ornament Scale** ~40%. Choose the diaper ornament (**Pattern A** to Scroll, **Pattern B** to Diaper).
2. **Reduce the palette**: Set **Color Depth** to step 2 (5 pigments).
3. **Add parchment**: Turn **Vellum** (Knob 5) to about 60%. A grainy, sandy texture appears across the entire image.
4. **Age the page**: Flip **Aging** (Toggle 10) to **Aged**. The brightness drops and the colors fade, as though the page had been locked in a vault for centuries.
5. **Gold highlights**: Enable **Gold Leaf** (Toggle 9) and set **Gold Threshold** (Knob 4) to about 60%. Only the brightest highlights receive gold (like the restrained gilding on a monastic psalter.)
6. **Palimpsest blend**: Pull **Mix** (Fader 12) down to about 40%. The original video shows through the manuscript treatment like a ghostly underpainting.

#### Settings

| Control | Value |
|---------|-------|
| Border Width | ~50% |
| Ornament Scale | ~40% |
| Color Depth | 2 (5 pigments) |
| Gold Threshold | ~60% |
| Vellum | ~60% |
| Frame Color | ~90° |
| Pattern A | Scroll |
| Pattern B | Diaper |
| Gold Leaf | On |
| Aging | Aged |
| Bypass | Off |
| Mix | ~40% |

---
## Glossary

- **Diaper Pattern**: A repeating lattice of diamond or lozenge shapes, common in Gothic manuscript backgrounds.

- **Geometric Fret**: A stepped, angular ornamental border also known as the Greek key or meander pattern.

- **Gold Leaf**: Extremely thin sheets of hammered gold applied to manuscript pages with an adhesive; the most prestigious decorative material in medieval book arts.

- **Illuminated Manuscript**: A handwritten book decorated with gold, silver, and vivid pigments; produced primarily in medieval Europe.

- **Knotwork**: Interlaced band patterns with no beginning or end, characteristic of Insular (Celtic and Anglo-Saxon) art.

- **LFSR**: Linear Feedback Shift Register; a digital circuit that produces a repeating pseudo-random bit sequence, used here for vellum grain.

- **Manhattan Distance**: The sum of absolute differences along each axis; used here as a fast color-distance metric for palette quantization.

- **Miniature**: In manuscript terminology, the pictorial illustration within a decorated page (not a reference to size.)

- **Palette Quantization**: Reducing the colors in an image to a fixed set of entries by mapping each pixel to its nearest palette match.

- **Scriptorium**: The writing room in a medieval monastery where manuscripts were copied and illuminated by hand.

- **Vellum**: Prepared animal skin (usually calf) used as a writing and painting surface for manuscripts.

---
