---
draft: true
sidebar_position: 132
slug: /instruments/videomancer/grisaille
title: "Grisaille"
image: /img/instruments/videomancer/grisaille/grisaille_hero_s1.png
description: "Oil painters of the Renaissance did not paint colour directly onto canvas."
---

![Grisaille hero image](/img/instruments/videomancer/grisaille/grisaille_hero_s1.png)
*Grisaille transforming a color video source into a luminance-mapped oil painting with translucent chroma glazes, aged patina, and procedural crack patterns.*

---

## Overview

**Grisaille** simulates a classical oil painting technique in real time. In the Renaissance, painters built images in layers: first a monochrome underpainting called a ***grisaille***, then thin translucent color glazes on top, and finally highlights and varnish. Grisaille recreates this layered workflow digitally. Your input video becomes the canvas, its luminance remapped through a tone curve that lifts shadows and compresses highlights: just as an artist would sketch light and dark masses before adding color. Chroma information is then reintroduced as a luminance-dependent glaze: shadows lose their color first, exactly as translucent pigment over a gray ground would behave.

Beyond the painting itself, Grisaille offers the passage of time. The **Patina** control simulates the yellowing of aged linseed oil, shifting the color palette toward warm amber. The **Craquelure** control overlays a procedural crack grid that darkens pixels on a modular-arithmetic lattice, as centuries of thermal cycling would fracture dried paint. Together, these controls let you age a painting from freshly varnished to museum antique in one smooth gesture.

:::note
Grisaille uses zero Block RAM tiles. All processing is purely combinational and registered: tone curves, glaze multiplies, hue shifts, and crack overlays are computed on the fly with no frame storage.
:::

### What's In a Name?

***Grisaille*** (pronounced "griz-EYE") is a French painting term derived from *gris*, meaning "gray." In the visual arts, a grisaille is a monochrome painting executed entirely in shades of gray, used either as a finished work or: more commonly: as the underpainting layer beneath translucent oil glazes. Artists like Jan van Eyck and Caravaggio used grisaille underpaintings to establish tonal structure before building color in successive layers of thin, transparent pigment. The technique is also known as ***chiaroscuro*** (Italian for "light-dark") when emphasizing dramatic contrasts between illuminated and shadowed forms.

---

## Quick Start

1. Turn **Glaze Opacity** (Knob 2) fully counterclockwise. The image collapses to monochrome: you're looking at the grisaille underpainting. Raise **Shadow Lift** (Knob 1) to brighten the darkest tones, as though sketching on tinted paper.
2. Slowly turn **Glaze Opacity** clockwise. Color seeps back in, starting with the brightest areas first. Dark regions stay gray longest, like translucent pigment pooling over a gray ground.
3. Sweep **Glaze Curve** (Knob 3) through its four positions. Each setting changes how aggressively shadows desaturate: from gentle roll-off to a dramatic van Eyck look where only highlights carry color.
4. Increase **Craquelure** (Knob 5) to overlay a procedural crack pattern. Toggle **Crack Scale** (Switch 8) between fine and coarse to change the density of the fracture grid.

---

## Parameters

![Videomancer front panel with Grisaille loaded](/img/instruments/videomancer/grisaille/grisaille_control_panel.png)
*Videomancer's front panel with Grisaille active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Shadow Lift

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Shadow Lift** sets the floor of the grisaille tone curve. At minimum, the darkest input pixels remain fully black. As you turn the knob clockwise, shadows are lifted toward a mid-gray floor, compressing the tonal range from below. This emulates painting on a toned ground: the darker the ground, the more dramatic the contrast; the lighter the ground, the more the painting floats above its surface.

The tone curve is piecewise linear with three segments: a shadow region below quarter scale, a midtone region in the center, and a highlight region above three-quarter scale. Shadow Lift controls the starting point of all three segments, so increasing it brightens the entire image while compressing the dynamic range.

---

### Knob 2 — Glaze Opacity

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Glaze Opacity** controls the base amount of chrominance that passes through the luminance-dependent glaze. At minimum, effective chroma opacity is zero regardless of luminance: the output is pure monochrome grisaille. As you increase Glaze Opacity, color returns, with the exact distribution controlled by **Glaze Curve** (Knob 3). At maximum, the glaze layer transmits nearly all of the original chroma in bright areas.

:::tip
For the classic grisaille-to-color transition, start with Glaze Opacity at zero, then sweep it slowly clockwise while feeding a richly colored source. You'll see the image bloom from gray into full color, with shadows lagging behind: exactly as a Renaissance painter would add successive glaze layers.
:::

---

### Knob 3 — Glaze Curve

| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 3 |

**Glaze Curve** selects one of four gamma exponents that shape how luminance maps to chroma opacity. The four steps approximate different historical glazing techniques:

- **Step 1** (gamma ~0.5): More color survives in shadows. A forgiving, even glaze.
- **Step 2** (gamma 1.0): Linear falloff (chroma tracks luminance directly.)
- **Step 3** (gamma ~1.5): Moderate shadow desaturation. Shadows are noticeably grayer than highlights.
- **Step 4** (gamma 2.0): The "van Eyck" setting: strong quadratic desaturation pushes shadows toward monochrome while highlights retain vivid color.

:::note
Because the glaze function multiplies ***base opacity × f(luminance)***, the effect of Glaze Curve is only visible when Glaze Opacity is above zero and Color Mode is set to Full.
:::

---

### Knob 4 — Patina

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Patina** simulates the yellowing of aged linseed oil. It shifts the U channel downward (toward yellow-amber) and nudges the V channel slightly upward. The effect intensifies as you turn the knob clockwise. At zero, the painted image retains its original hue balance. At maximum, the palette is dragged heavily into warm amber territory, as though the canvas has been hanging in a dimly lit gallery for three hundred years.

---

### Knob 5 — Craquelure

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Craquelure** controls the intensity of a procedural crack pattern overlaid on the image. The crack grid is generated by modular arithmetic on the horizontal and vertical pixel counters: wherever a pixel falls on a crack line, its luminance is darkened. At zero, no cracks appear. As you increase the value, cracks darken more aggressively. At maximum, crack-line pixels are driven close to black, simulating deep fractures in dried oil paint.

:::warning
Craquelure darkens only the Y channel at crack positions. U and V are ***not*** affected on crack lines, so hairline color streaks may be visible at very high settings on saturated sources. This is by design: real craquelure fractures the paint film, exposing the underpainting, not the chroma layer.
:::

---

### Knob 6 — Ground Tint

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Ground Tint** controls the hue of the ***imprimatura***: the tinted ground applied to the canvas before painting. This knob sweeps through 360 degrees of hue angle, shifting the palette of the underpainting. The effect is most visible when **Ground Type** (Switch 7) is set to Warm, which applies an initial U/V offset before the ground tint rotation. At minimum and maximum the hue wraps around, so the control behaves like a continuous rotation.

---

### Switch 7 — Ground Type

| Property | Value |
|----------|-------|
| Off | Warm |
| On | Cool |
| Default | Warm |

**Ground Type** selects between two imprimatura base tones. When set to **Warm**, the pipeline applies a subtle earth-tone bias: U is shifted down (toward amber) and V is nudged up, producing a warm yellowish ground reminiscent of raw sienna or burnt umber gesso. When set to **Cool**, no tonal bias is applied: the ground is a neutral gray. The warm ground interacts with **Patina** (Knob 4), amplifying the yellowing effect when both are active.

---

### Switch 8 — Crack Scale

| Property | Value |
|----------|-------|
| Off | Fine |
| On | Coarse |
| Default | Fine |

**Crack Scale** selects between two craquelure grid densities. **Fine** uses a tighter grid with a period of 24 pixels and single-pixel-wide crack lines, producing a delicate web of hairline fractures. **Coarse** uses a wider grid with a period of 48 pixels and two-pixel-wide crack lines, creating bold, widely spaced cracks that suggest deep structural fractures in thick paint. The visual weight of the cracks is then controlled by the **Craquelure** (Knob 5) intensity knob.

---

### Switch 9 — Color Mode

| Property | Value |
|----------|-------|
| Off | Full |
| On | Grisaille |
| Default | Full |

**Color Mode** switches between full-color output and pure grisaille. When set to **Full**, the luminance-dependent glaze is active and chroma passes through according to the Glaze Opacity and Glaze Curve settings. When set to **Grisaille**, the glaze opacity is forced to zero: all chroma is stripped and the output is monochrome regardless of other settings. This is useful for isolating the tonal structure of the underpainting without distraction from color.

---

### Switch 10 — Impasto

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Impasto** enables a hard highlight clip in the grisaille tone curve. With Impasto **Off**, highlights compress softly toward maximum. With Impasto **On**, any pixel in the highlight region is hard-clipped to full white, simulating the thick, opaque brushstrokes that painters use to build up bright highlights: the ***impasto*** technique. This creates stark, flat highlight planes that contrast with the softer tonal gradations in the shadows and midtones.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed, delay-matched input signal directly to the output, skipping all painting stages. The sync delay pipeline still aligns timing, so toggling Bypass produces a clean A/B comparison between the raw input and the painted result with no glitch on transition.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) and wet (painted) signals. At minimum, the output is the original input video. At maximum, the output is entirely the grisaille-painted result. Intermediate positions blend the two, which can produce a partially painted look: as though the artist has only begun to lay down the underpainting and portions of the original canvas still show through.

---

## Background

### The Grisaille Technique

The grisaille underpainting method dominated European oil painting from the fifteenth through the eighteenth centuries. Painters like Jan van Eyck, Rogier van der Weyden, and later Caravaggio established tonal values first by working entirely in shades of gray (or gray-green, called ***verdaccio***). Once the monochrome image was complete and dry, the artist applied thin layers of transparent colored pigment: ***glazes***: over the gray base. Because the glazes were translucent, the underlying tonal structure showed through, giving the painting a luminous depth that opaque paint mixing cannot achieve. Each glaze layer could emphasize a different color or temperature, and multiple glazes built up rich, complex hues.

### Chroma Glaze Modeling

Grisaille models the translucent glaze mathematically. The effective chroma opacity at each pixel is `base_opacity × f(Y)`, where `f(Y)` is a luminance-dependent function shaped by one of four gamma exponents. At gamma 2.0 (the van Eyck setting), the function is quadratic: chroma opacity falls off as the square of luminance, so only the brightest areas carry significant color. At gamma 0.5, a square-root-like approximation keeps more color in mid-shadows. The chroma channels (U and V) are scaled toward neutral (the value 512 in 10-bit space) by the complement of the effective opacity: fully opaque = original chroma, fully transparent = gray.

### Aging and Patina

Real oil paintings change over time. Linseed oil: the most common binder in oil paint: oxidizes and turns yellow-brown over decades. Dust and varnish layers accumulate. The Patina control simulates this by shifting the U channel downward (toward yellow) and the V channel slightly upward, producing a warm amber cast. Combined with the Warm ground type, which pre-biases the underpainting toward earth tones, the patina effect can push the image into the territory of heavily aged Old Master paintings.


---

## Signal Flow

### Signal Flow Notes

The pipeline is a straightforward four-stage chain: input curve, glaze, aging effects, and output mix: with no feedback loops. Two important interactions shape the result:

1. **Luminance drives chroma.** The grisaille tone curve in Stage 1 reshapes the Y channel, and the ***remapped*** Y (not the original input Y) feeds the glaze opacity function in Stage 2. This means Shadow Lift indirectly affects color distribution: lifting shadows gives them higher luminance, which in turn allows more chroma to pass through the glaze. Lowering Shadow Lift darkens shadows further, pushing them deeper into the monochrome zone.

2. **Ground tint stacks with patina.** The Stage 1 ground-type offset and the Stage 3 patina shift both modify U and V, but they act at different pipeline stages. Setting Ground Type to Warm applies a constant shift (U −20, V +15) before the glaze, while Patina applies a second shift after the glaze. When both are active, the two shifts compound, producing a very heavy amber bias. To get patina yellowing without doubling the warmth, set Ground Type to Cool.


---

## Exercises

These exercises progress from monochrome underpainting to full aged-painting simulation. Each one introduces additional pipeline stages so you can hear how the layers interact.
### Exercise 1: The Gray Underpainting

![The Gray Underpainting result](/img/instruments/videomancer/grisaille/grisaille_ex1_s1.png)
*The Gray Underpainting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dramatic monochrome underpainting with lifted shadows and impasto highlights (the first step of any Classical painting.)

#### Key Concepts

- Grisaille tone curves remap luminance to emulate painted tonal structure
- Shadow Lift controls the darkness floor
- Impasto creates hard highlight planes

#### Video Source

Portrait or still life footage with a wide tonal range (faces, draped fabric, and candlelit scenes work well.)

#### Steps

1. Set **Color Mode** (Switch 9) to **Grisaille** to strip all color.
2. Start with **Shadow Lift** (Knob 1) at about 25%. Dark areas lift off the floor, as if sketching on warm-toned paper.
3. Toggle **Impasto** (Switch 10) **On**. Bright highlights snap to full white, creating thick, flat highlight planes.
4. Sweep Shadow Lift from minimum to maximum and observe how the tonal range compresses. Find the setting that best balances drama and legibility.
5. Toggle Impasto back **Off** and notice how highlights return to a gentler compression.

#### Settings

| Control | Value |
|---------|-------|
| Shadow Lift | ~25% |
| Glaze Opacity | 0% |
| Glaze Curve | 1 |
| Patina | 0% |
| Craquelure | 0% |
| Ground Tint | 0° |
| Ground Type | Cool |
| Crack Scale | Fine |
| Color Mode | Grisaille |
| Impasto | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Glazing Color Over Gray

![Glazing Color Over Gray result](/img/instruments/videomancer/grisaille/grisaille_ex2_s1.png)
*Glazing Color Over Gray — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A richly colored image where shadows remain gray while highlights bloom with full chroma (the classic Old Master glazing effect.)

#### Key Concepts

- Chroma glaze is luminance-dependent (shadows desaturate first)
- Glaze Curve selects the opacity falloff shape
- Ground Type introduces tonal warmth before the glaze

#### Video Source

Footage featuring saturated colors and mixed lighting: botanical scenes, market stalls, stained glass, or a color bar test pattern.

#### Steps

1. Switch **Color Mode** back to **Full**. Set **Glaze Opacity** (Knob 2) fully counterclockwise (the image stays monochrome.)
2. Slowly turn Glaze Opacity clockwise. Color appears in the brightest areas first and gradually fills in toward the shadows.
3. Step through all four positions of **Glaze Curve** (Knob 3). At Step 1, even moderate shadows retain color. At Step 4, only the brightest highlights carry chroma (the dramatic van Eyck look.)
4. Set **Ground Type** (Switch 7) to **Warm**. The monochrome base shifts to an amber earth tone. Now the interplay between warm ground and colored glaze adds depth.
5. Set Glaze Curve to Step 3 and Glaze Opacity to about 75%. This balance gives rich highlights with moody, desaturated shadows.

#### Settings

| Control | Value |
|---------|-------|
| Shadow Lift | ~25% |
| Glaze Opacity | ~75% |
| Glaze Curve | 3 |
| Patina | 0% |
| Craquelure | 0% |
| Ground Tint | 0° |
| Ground Type | Warm |
| Crack Scale | Fine |
| Color Mode | Full |
| Impasto | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: The Aged Painting

![The Aged Painting result](/img/instruments/videomancer/grisaille/grisaille_ex3_s1.png)
*The Aged Painting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A complete aged painting simulation: grisaille underpainting, colored glaze, oil yellowing, and cracking: as though you're looking at a canvas that has hung in a gallery for centuries.

#### Key Concepts

- Patina yellows the image to simulate oxidized linseed oil
- Craquelure overlays a procedural crack grid
- All layers combine for a museum-aged painting effect

#### Video Source

Portraiture or landscape footage (subjects that evoke classical painting compositions.)

#### Steps

1. Load the settings from Exercise 2 as your starting point (Glaze Opacity ~75%, Glaze Curve Step 3, Ground Type Warm).
2. Increase **Patina** (Knob 4) to about 50%. The image acquires a warm amber cast, simulating centuries of linseed oil oxidation.
3. Increase **Craquelure** (Knob 5) to about 60%. A grid of dark crack lines appears across the image.
4. Toggle **Crack Scale** (Switch 8) between Fine and Coarse. Fine produces delicate hairline fractures; Coarse produces bold, wide cracks.
5. Push Shadow Lift higher (~40%) so the cracks don't vanish into black shadows.
6. Finally, pull **Mix** (Fader 12) to about 70% to let some of the original video bleed through, as though the painting is displayed over a rear-lit screen.

#### Settings

| Control | Value |
|---------|-------|
| Shadow Lift | ~40% |
| Glaze Opacity | ~60% |
| Glaze Curve | 3 |
| Patina | ~50% |
| Craquelure | ~60% |
| Ground Tint | 0° |
| Ground Type | Warm |
| Crack Scale | Coarse |
| Color Mode | Full |
| Impasto | On |
| Bypass | Off |
| Mix | ~70% |

---
## Glossary

- **Chiaroscuro**: Italian for "light-dark"; a painting technique that uses strong contrasts between illuminated and shadowed areas to model three-dimensional form.

- **Craquelure**: The network of fine cracks that develops in the surface of an oil painting as layers of paint and varnish dry, shrink, and age over time.

- **Gamma**: A nonlinear function that describes how input values map to output intensity; higher gamma darkens midtones and compresses shadows.

- **Glaze**: A thin, transparent layer of pigment applied over a dried underpainting; the underlying tonal values show through the glaze, creating luminous depth.

- **Grisaille**: A monochrome painting executed in shades of gray, often used as an underpainting layer beneath translucent oil glazes.

- **Impasto**: A painting technique in which thick strokes of opaque paint are applied so that they stand above the surface, creating visible texture and flat highlight planes.

- **Imprimatura**: A toned ground: a thin wash of color applied to the canvas before painting: that unifies the palette and eliminates the stark white of raw gesso.

- **Interpolator**: A hardware module that linearly crossfades between two input values based on a fractional blend parameter; used here for dry/wet mixing.

- **Patina**: The surface appearance of an object that has changed through age or exposure; in painting, often refers to the yellow-brown tone that develops in aged linseed oil.

- **Tone Curve**: A function that remaps input brightness values to output brightness values, reshaping the tonal distribution of an image.

- **Underpainting**: The initial layer of paint applied to a canvas, establishing the composition and tonal values before subsequent layers of color.

- **Verdaccio**: A variant of grisaille underpainting using gray-green tones, common in Italian fresco and tempera painting traditions.

---
