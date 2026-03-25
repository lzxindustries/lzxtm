---
draft: true
sidebar_position: 19
slug: /instruments/videomancer/birefring
title: "Birefring"
image: /img/instruments/videomancer/birefring/birefring_hero_s1.png
description: "When light passes through a crystalline material like calcite or quartz, something unusual happens — the crystal splits the light into two rays that travel at different speeds."
---

![Birefring hero image](/img/instruments/videomancer/birefring/birefring_hero_s1.png)
*Birefring mapping input luminance through a Michel-Lévy interference color spectrum, transforming grayscale video into the iridescent palette of stressed crystal viewed between crossed polarizers.*

---

## Overview

Birefring is an optical simulation program that maps video luminance to interference colors: the vivid rainbow palette that appears when a transparent material is placed between two polarizing filters. Its core technique is ***color lookup***: every pixel's brightness selects a color from a sixty-four-entry spectrum table, producing the same kind of iridescent banding you see in a soap bubble, a stressed plastic ruler, or a thin mineral slice under a geology microscope.

At gentle settings, Birefring tints the image with subtle pastel washes that follow the contours of brightness. At extreme settings, the entire picture dissolves into ribbons of spectral color, cycling through three full orders of interference from deep violet through brilliant green and back to pale rose. The **Thickness** and **Stress** controls decide how much of the spectrum is traversed, while the **Polarizer** knob darkens the image according to a realistic cos² extinction curve (just like rotating a real polarizing filter.)

Two spectrum tables are included. The default ***Michel-Lévy*** chart reproduces the standard mineralogical reference used in geology labs, where colors desaturate in higher orders. The alternate ***Newton's rings*** palette is more saturated and wraps its hues in a tighter loop, inspired by the concentric color fringes seen when a curved lens rests on flat glass.

:::tip
Birefring works best with source material that has a wide range of brightness. Gradients, faces, and backlit subjects all produce dramatic spectral ribbons.
:::

### What's In a Name?

The name ***Birefring*** is a contraction of ***birefringence***, the optical property of certain crystals and stressed polymers that splits light into two rays traveling at different speeds. When that material is sandwiched between crossed polarizers, the speed difference converts into vivid interference colors. The particular hue depends on the material's thickness and internal stress: which is exactly what the program's two primary controls model.

---

## Quick Start

1. Feed a source with visible tonal contrast into Videomancer and load **Birefring**. The image immediately takes on a rainbow-tinted appearance as the default **Thickness** and **Stress** settings map brightness through the interference spectrum.
2. Sweep **Thickness** (Knob 1) slowly from left to right. The color bands shift across the image like rotating a polarizer over a mineral slide (dark areas cycle through different hues than bright areas.)
3. Increase **Stress** (Knob 2) past the halfway mark. The spectrum stretches so that even small brightness differences produce dramatic color changes, revealing fine tonal detail as vivid spectral contours.
4. Rotate **Polarizer** (Knob 3) to see the image darken and brighten according to a cos² curve. At certain angles the picture nearly vanishes: this is the simulated ***extinction*** position of a real crossed-polarizer setup.

---

## Parameters

![Videomancer front panel with Birefring loaded](/img/instruments/videomancer/birefring/birefring_control_panel.png)
*Videomancer's front panel with Birefring active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Thickness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Thickness** sets the base offset into the interference color spectrum. Think of it as choosing the starting point on a Michel-Lévy chart: at 0%, the lookup begins at the bottom of the chart (black, through gray, into white), while increasing the value scrolls upward through yellows, reds, violets, blues, greens, and eventually into the pale, desaturated higher orders. With **Stress** at zero, Thickness alone determines which single color tints the entire image. With Stress active, Thickness shifts the whole mapping so that the same brightness values land on different spectral colors.

:::note
Because the lookup table has sixty-four entries and wraps around, sweeping Thickness through its full range cycles through the spectrum roughly four times. This makes it easy to dial in a specific hue by ear (just keep turning until the color you want appears.)
:::

---

### Knob 2 — Stress

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Stress** controls how much the input luminance contributes to the spectrum index. At 0%, the input brightness has no influence: every pixel maps to the same point in the lookup table (set by **Thickness** alone), and the image appears as a flat color wash. As Stress increases, bright and dark pixels diverge along the spectrum, producing visible color contours that follow the tonal structure of the source. At 100%, the full luma range spans a wide swath of the sixty-four-entry table, and fine brightness gradients explode into dense spectral ribbons.

Stress and **Thickness** work together: Thickness picks the center of the spectral window, while Stress sets its width.

---

### Knob 3 — Polarizer

| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |

**Polarizer** simulates the angular rotation of a crossed-polarizer pair. The output brightness is multiplied by a ***cos² attenuation curve***: the same law that governs real polarized light. At 0 degrees the signal passes at full brightness. At 90 degrees (a quarter turn) the signal is fully extinguished, producing a dark image. Continuing past 90 degrees brightens it again, completing the cos² cycle at 360 degrees.

:::tip
The Polarizer control is especially dramatic when combined with high **Stress**. Because it attenuates the overall brightness, it changes which parts of the spectrum the eye can still see, effectively shifting the apparent color balance without touching Thickness.
:::

---

### Knob 4 — Dispersion

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Dispersion** introduces ***chromatic dispersion***: a spatial offset between the color channels' lookup indices. At 0%, the Y, U, and V channels all use the same spectrum index, producing clean spectral hues. As Dispersion increases, the U-channel index is shifted forward and the V-channel index is shifted backward (or vice versa), so each channel reads a different point on the spectrum. The result is a prismatic splitting of hue: edges and contours develop color fringes reminiscent of light passing through a dispersive prism.

At high values, the three channels diverge enough to produce tricolor separation effects where distinct red, blue, and green bands appear along brightness contours.

---

### Knob 5 — Saturation

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Saturation** scales the intensity of the interference colors. At 0%, the color components are zeroed out and only the luminance information remains, producing a monochrome image tinted by the spectrum's brightness profile. At the default position (about 75%), the colors reproduce at approximately their natural intensity. Turning past 75% toward 100% boosts saturation beyond the reference level, exaggerating the spectral hues to vivid, almost fluorescent intensity.

The scaling is applied symmetrically around the neutral chroma axis (U = 512, V = 512), so increasing saturation pushes colors outward from gray in all directions equally.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** adds a fixed offset to the luminance channel after all other processing. At the center position (50%), no offset is applied. Turning counterclockwise darkens the image; turning clockwise brightens it. This is a simple DC shift: it does not affect the spectral color mapping, only the final luminance level.

:::note
Because Brightness is applied after the cos² Polarizer attenuation, you can use it to recover visibility at extinction angles. Turn the Polarizer to near-extinction, then push Brightness up to reveal a dim, deeply colored image.
:::

---

### Switch 7 — Spectrum

| Property | Value |
|----------|-------|
| Off | Michel-Levy |
| On | Newton |
| Default | Michel-Levy |

**Spectrum** selects between two built-in interference color palettes. In the **Michel-Lévy** position (default), the lookup table reproduces the classic mineralogical interference chart: three orders of color that gradually desaturate at higher orders, ending in pale pastels. In the **Newton** position, the palette uses a more saturated, tightly wrapped sequence inspired by ***Newton's rings***: the concentric color fringes seen when a convex lens touches a flat glass surface. The Newton palette cycles through vivid hues more aggressively and maintains its saturation into the higher orders.

---

### Switch 8 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Animate** enables automatic cycling through the spectrum over time. When set to **On**, an internal counter increments once per video frame, and its upper bits add a slowly increasing offset to the spectrum index. The result is a continuous, gentle rotation of colors across the image: as though the mineral sample were being slowly heated and its internal stress were changing. The animation speed is fixed and produces a complete spectral sweep over several seconds.

:::tip
Animate is beautiful on static or slowly moving sources. The interference colors drift and shimmer across the image like oil on water.
:::

---

### Switch 9 — Invert Map

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert Map** reverses the direction of the spectrum lookup. When set to **On**, the table index is mirrored: what was entry 0 becomes entry 63, and vice versa. This swaps which brightness values map to which colors. Dark areas that previously appeared violet might now appear green, and bright areas shift in the opposite direction. Invert Map is a quick way to explore alternate colorizations without changing **Thickness** or **Stress**.

---

### Switch 10 — Y Couple

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Y Couple** controls whether the output luminance tracks the input brightness or follows the spectrum's own brightness profile. In the default **On** position, the lookup table's Y value is multiplied by the input luma, so dark input pixels produce dark output and bright input pixels produce bright output: the tonal structure of the source is preserved, with spectral colors overlaid on top. In the **Off** position, the output luminance comes entirely from the lookup table, so the image's brightness is replaced by the spectrum's own lightness curve regardless of the input.

:::note
With Y Couple off, the output brightness depends entirely on the spectrum position. Dark inputs might produce bright spectral colors and vice versa. This creates an unusual, poster-like look where the original tonal hierarchy is discarded.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Birefring processing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the processed spectrum mapping and the raw input.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** blends between the dry (original) and wet (processed) signal. At 0%, fully down, the output is the unprocessed input. At 100%, fully up (the default), the output is the full Birefring spectrum mapping. Intermediate positions create a translucent overlay where the spectral colors are blended on top of the original image, producing a subtle tinted look.

---

## Background

### Birefringence and Interference Colors

When certain transparent materials: quartz, calcite, cellophane, stressed acrylic: are placed between two polarizing filters arranged at right angles, they produce vivid colors even though the material itself is colorless. The phenomenon occurs because the material splits incoming light into two polarized rays that travel at different speeds. When those rays recombine at the second polarizer, they interfere: some wavelengths cancel and others reinforce, depending on the material's thickness and the amount of mechanical stress applied to it. The surviving wavelengths form the ***interference colors*** that geologists, materials scientists, and artists have used for centuries.

### The Michel-Lévy Chart

In 1888, the French geologist Auguste Michel-Lévy published a color chart that systematized these interference colors. The chart plots material thickness against ***birefringence*** (the difference in speed between the two rays) and shows which color appears at each combination. The chart is divided into ***orders***: the first order runs from black through gray, white, yellow, orange, red, and indigo; the second order sweeps from blue through green, yellow, and rose; higher orders repeat with progressively paler, more pastel hues. Birefring's sixty-four-entry lookup table encodes an approximation of the first three and a half orders of this chart.

### Newton's Rings

Isaac Newton described a related phenomenon in 1704: when a convex lens is placed on a flat glass plate, a thin film of air forms between them. The film's thickness varies from zero at the contact point outward, producing concentric rings of interference color. Newton's rings are more saturated than Michel-Lévy colors because the air film is perfectly uniform: there is no scattering or crystal irregularity to wash out the hues. Birefring's alternate Newton palette captures this vivid, tightly wrapped quality.

### Malus's Law and Polarizer Extinction

The **Polarizer** control implements ***Malus's law***: the intensity of light passing through two polarizers is proportional to cos²(θ), where θ is the angle between their transmission axes. At 0° the polarizers are aligned and all light passes. At 90° they are crossed and no light passes: this is called ***extinction***. Birefring uses a sixteen-entry cos² lookup table with quarter-wave symmetry to reproduce this behavior.


---

## Signal Flow

### Signal Flow Notes

The most important interaction in Birefring is between **Thickness**, **Stress**, and the input luminance. Thickness sets the base offset into the sixty-four-entry spectrum table, and Stress determines how much the input brightness shifts that offset. Because the table wraps around (it is indexed by a six-bit value), pushing the combined offset past entry 63 cycles back to entry 0, producing natural spectral repetition.

**Dispersion** introduces a deliberate mismatch between the Y, U, and V channel indices. The Y channel determines the luma output, but the U and V channels look up their colors at slightly different points on the spectrum. This is analogous to chromatic aberration in a real lens: different wavelengths refract by different amounts, producing color fringes at brightness transitions. Because the offset is applied symmetrically (U adds, V subtracts), the fringing appears as complementary-color halos rather than a uniform shift.

:::tip
The six-clock pipeline means that the spectrum mapping, polarizer extinction, saturation scaling, brightness offset, and wet/dry mix all happen in sequence. Because the sync delay pipeline keeps the original data aligned, the **Mix** fader blends the dry and wet signals at pixel-perfect registration.
:::


---

## Exercises

These exercises progress from basic spectrum exploration to complex animated optical simulations. Each builds on the last, introducing more controls and interactions.
### Exercise 1: Mineral Slide

![Mineral Slide result](/img/instruments/videomancer/birefring/birefring_ex1_s1.png)
*Mineral Slide — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A still image transformed into a simulated thin-section mineral slide: the kind of view you would see through a geology microscope with crossed polarizers.

#### Key Concepts

- Luminance-to-color mapping via a lookup table
- Thickness and Stress as the primary spectral controls
- Y Couple preserves the source's tonal hierarchy

#### Video Source

A portrait or landscape with smooth gradients and a full range of brightness.

#### Steps

1. Load **Birefring** and observe the default output. The source image is already tinted with interference colors from the Michel-Lévy spectrum.
2. Turn **Stress** (Knob 2) down to about 20%. The spectral mapping narrows: most of the image falls within a small slice of the chart, producing a subtle warm tint.
3. Sweep **Thickness** (Knob 1) slowly across its range. Watch the tint shift through the spectrum: from near-black, through first-order yellows and reds, into second-order blues and greens, and finally into pale third-order pastels.
4. Increase **Stress** back to 70%. Now the brightness contours of the image explode into dense spectral ribbons. Edges and gradients reveal themselves as vivid color bands.
5. Adjust **Saturation** (Knob 5) to taste. Lower values produce a watercolor wash; higher values push the hues toward neon intensity.

#### Settings

| Control | Value |
|---------|-------|
| Thickness | ~25% |
| Stress | 70% |
| Polarizer | 0 deg |
| Dispersion | 0% |
| Saturation | ~75% |
| Brightness | 50% |
| Spectrum | Michel-Lévy |
| Animate | Off |
| Invert Map | Off |
| Y Couple | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Rotating Polarizer

![Rotating Polarizer result](/img/instruments/videomancer/birefring/birefring_ex2_s1.png)
*Rotating Polarizer — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated polarizer rotation effect, as though a polarizing filter is being slowly turned in front of the camera, revealing and hiding spectral colors.

#### Key Concepts

- Malus's law cos² extinction curve
- Polarizer interaction with Brightness offset
- Dispersion creates chromatic fringing

#### Video Source

High-contrast footage: a backlit subject or a scene with strong shadows works well.

#### Steps

1. Set **Thickness** (Knob 1) to about 50% and **Stress** (Knob 2) to about 50% for a moderate spectral spread.
2. Enable **Animate** (Switch 8). The interference colors begin to drift slowly across the image.
3. Slowly rotate **Polarizer** (Knob 3). At certain angles the image dims dramatically: this is the simulated ***extinction*** position. At other angles it brightens back to full intensity.
4. While near extinction, push **Brightness** (Knob 6) past center. The image recovers with deeply saturated, almost gem-like colors visible against a dark background.
5. Add **Dispersion** (Knob 4) at about 40%. Color fringes appear along brightness contours, splitting the hues into prismatic bands.
6. Toggle **Spectrum** (Switch 7) to **Newton** and compare the more saturated, tightly wrapped ring palette.

#### Settings

| Control | Value |
|---------|-------|
| Thickness | 50% |
| Stress | 50% |
| Polarizer | ~135 deg |
| Dispersion | 40% |
| Saturation | ~75% |
| Brightness | ~70% |
| Spectrum | Newton |
| Animate | On |
| Invert Map | Off |
| Y Couple | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Prismatic Dispersion

![Prismatic Dispersion result](/img/instruments/videomancer/birefring/birefring_ex3_s1.png)
*Prismatic Dispersion — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A heavily dispersed, prismatic image where color channels separate into distinct spectral bands, resembling light refracted through a glass prism.

#### Key Concepts

- Chromatic dispersion splits the U and V look-up indices
- Invert Map reverses the spectrum direction
- Y Couple off decouples brightness from input

#### Video Source

Geometric patterns, lines, or text (anything with hard edges to reveal the chromatic splitting.)

#### Steps

1. Set **Thickness** (Knob 1) to about 40% and **Stress** (Knob 2) to about 60%.
2. Push **Dispersion** (Knob 4) to a high value, around 80%. The edges of brightness transitions develop vivid tricolor fringes as the U and V channels diverge widely on the spectrum.
3. Toggle **Y Couple** (Switch 10) to **Off**. The output brightness now follows the spectrum's own profile rather than the source's tonal structure. Dark input areas may suddenly become bright, and vice versa.
4. Toggle **Invert Map** (Switch 9) to **On**. The spectrum reverses: colors that appeared in shadows now appear in highlights.
5. Increase **Saturation** (Knob 5) to maximum. The dispersed fringes become intensely vivid.
6. Lower **Mix** (Fader 12) to about 60%. The prismatic dispersion blends with the original image, producing a translucent, stained-glass overlay.

#### Settings

| Control | Value |
|---------|-------|
| Thickness | 40% |
| Stress | 60% |
| Polarizer | 0 deg |
| Dispersion | 80% |
| Saturation | 100% |
| Brightness | 50% |
| Spectrum | Michel-Lévy |
| Animate | Off |
| Invert Map | On |
| Y Couple | Off |
| Bypass | Off |
| Mix | 60% |

---
## Glossary

- **Birefringence**: An optical property of certain crystals and stressed polymers that splits light into two polarized rays traveling at different speeds, producing interference colors when viewed between crossed polarizers.

- **Chromatic Dispersion**: The separation of light into its component colors due to wavelength-dependent refraction; in Birefring, simulated by offsetting the U and V channel lookup indices.

- **Cos² Law (Malus's Law)**: The mathematical relationship governing the intensity of polarized light passing through two polarizers: intensity is proportional to the square of the cosine of the angle between them.

- **Extinction**: The condition where two crossed polarizers block all transmitted light, occurring at 90° relative alignment; simulated by the Polarizer control's attenuation minimum.

- **Interference Colors**: The vivid hues produced when two light waves combine constructively or destructively after traveling different paths through a birefringent material.

- **Lookup Table (LUT)**: A pre-computed array of values used to transform input data; Birefring uses a sixty-four-entry YUV lookup table to map luminance to spectral color.

- **Michel-Lévy Chart**: A standard reference chart used in geological microscopy that maps material thickness and birefringence to the resulting interference color, divided into numbered orders.

- **Newton's Rings**: Concentric interference color fringes formed in the thin air film between a curved lens surface and a flat glass plate; Birefring's alternate, more saturated spectrum palette is inspired by this phenomenon.

- **Polariscopy**: The technique of examining materials between crossed polarizers to reveal internal stress and structure through interference colors.

- **Spectrum Order**: A complete cycle through the interference color sequence; higher orders repeat the hue cycle with progressively lower saturation.

---
