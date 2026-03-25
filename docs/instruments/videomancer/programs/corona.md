---
draft: true
sidebar_position: 69
slug: /instruments/videomancer/corona
title: "Corona"
image: /img/instruments/videomancer/corona/corona_hero_s1.png
description: "Corona synthesizes the radial streamer field of a total solar eclipse — the ethereal halo of plasma that becomes visible only when the Moon's disk occults the Sun's photosphere."
---

![Corona hero image](/img/instruments/videomancer/corona/corona_hero_s1.png)
*A radiant solar corona erupts from a dark lunar disk, its asymmetric streamers drifting and evolving across the screen like a total eclipse that never ends.*

---

## Overview

Corona transforms your video into the backdrop for a simulated total solar eclipse. Radial streamers emanate from a configurable center point, fall off with distance, and glow additively over the input image. Three harmonically related sine functions shape the angular structure of the corona, producing anything from a simple two-pointed star to a complex, asymmetric halo with a dozen or more lobes. A dark occluding disk at the center represents the Moon's silhouette during totality.

What makes Corona special is its sense of life. Three ***direct digital synthesis*** phase accumulators drift at different rates, causing the streamer pattern to continuously evolve: lobes swell, merge, split, and reform in an organic rhythm. The **Rotation** knob controls the drift speed, and the entire corona center can wander across the frame on a slow ***Lissajous*** path. The result is a luminous, breathing structure that feels astronomical rather than mechanical.

The program operates additively: the corona brightens the scene beneath it without erasing it. Dark areas of the corona leave the source image untouched, while bright streamers bloom over whatever is underneath. A **Butler** color mode recreates the pearl-white inner corona and blue-green outer corona observed by the painter Howard Russell Butler during total eclipses in the early twentieth century.

### What's In a Name?

A ***corona*** is the outermost layer of the Sun's atmosphere: a halo of superheated plasma normally invisible behind the Sun's overwhelming glare. It becomes visible only during a total solar eclipse, when the Moon blocks the solar disk and reveals the corona's delicate, structured streamers extending outward into space. The word comes from the Latin *corōna*, meaning "crown" or "garland." This program generates that crown of light.

---

## Quick Start

1. With **Eclipse** (Switch 7) set to **Disk** and all other controls at their defaults, you'll see a dark central disk surrounded by a faint ring of streamer lobes glowing over your input video.
2. Turn **Brightness** (Knob 5) clockwise past the halfway point. The corona blooms: streamers become vivid and bright, washing out the source image where they overlap.
3. Sweep **Streamers** (Knob 2) slowly through its range. Watch the corona change from two broad lobes to a dense starburst with twelve points. Then increase **Asymmetry** (Knob 3) to break the symmetry, making some lobes longer than others.
4. Turn **Rotation** (Knob 1) to a moderate value. The corona comes alive: its streamers drift and morph continuously. Flip **CtrLock** (Switch 9) to **Drift** and watch the entire corona wander across the frame.

---

## Parameters

![Videomancer front panel with Corona loaded](/img/instruments/videomancer/corona/corona_control_panel.png)
*Videomancer's front panel with Corona active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Rotation

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Rotation** controls the drift speed of the corona's streamer pattern. At zero, the corona is frozen. As you turn the knob clockwise, three internal phase accumulators advance faster with each video frame, causing the streamer lobes to rotate, merge, and separate at increasing speeds. At low values the drift is glacial and meditative; at high values the corona swirls rapidly, its structure evolving in frantic, kaleidoscopic motion. The three accumulators run at different rates (the second at roughly five-eighths, the third at roughly five-sixteenths of the primary), so the resulting drift is never a simple rotation (it's a complex, quasi-periodic evolution.)

---

### Knob 2 — Streamers

| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 9 |

**Streamers** sets the angular complexity of the corona by selecting the fundamental frequency of the lobe function. At the minimum setting, only two broad, opposing lobes appear: a simple bipolar glow. Turning the knob clockwise steps through eight discrete values: 2, 3, 4, 5, 6, 8, 10, and 12 streamers. Higher streamer counts produce denser, more intricate patterns. Because two additional harmonics (offset by +3 and +6 from the fundamental) always contribute to the pattern, even the simplest settings have subtle complexity.

---

### Knob 3 — Asymmetry

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Asymmetry** controls the amplitude of the third harmonic in the lobe function. At zero, the third harmonic is silent and the corona is determined only by the fundamental and second harmonic, producing a more regular, balanced pattern. Turning **Asymmetry** clockwise introduces increasing amounts of the third harmonic, which breaks the angular symmetry of the corona. Some lobes grow longer while others shrink, creating an uneven, organic look. At full strength, the third harmonic contributes as much energy as the fundamental, producing highly asymmetric streamer fields.

---

### Knob 4 — Disk Size

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |

**Disk Size** sets the radius of the central occluding disk: the Moon's silhouette. At zero, the disk is tiny and the corona extends nearly to the center. Increasing the value widens the dark circle, pushing the visible corona further from center and revealing only the outer streamer tips. This control has no effect when **Eclipse** (Switch 7) is set to **NoDisk**.

:::tip
Increasing **Disk Size** while **Prominences** (Switch 8) is **On** makes the bright prominence ring more visible, because more of the corona behind the disk is hidden while the ring at the disk edge stays.
:::

---

### Knob 5 — Brightness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 68.4% |

**Brightness** scales the overall intensity of the corona. At zero, the corona is invisible: no light is added to the scene. As you turn the knob clockwise, the streamers grow brighter, eventually washing out the source image beneath them. The scaling applies after the radial falloff and lobe function, so it uniformly controls the "exposure" of the entire corona.

---

### Knob 6 — Color

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 106° |

**Color** sweeps the hue of the corona in monochrome mode. The control maps across 360 degrees of color space. The tint is applied as a UV offset from neutral gray, so different positions on the knob produce different colored coronas: warm ambers, cool blues, vivid greens. This control has no visible effect when **ColorMode** (Switch 10) is set to **Butler**, because the Butler palette overrides the manual color selection with its own distance-based color mapping.

---

### Switch 7 — Eclipse

| Property | Value |
|----------|-------|
| Off | Disk |
| On | NoDisk |
| Default | Disk |

**Eclipse** selects between two rendering modes. In the **Disk** position, a dark occluding disk is drawn at the center: the Moon blocking the Sun. The corona is masked to zero inside the disk radius, creating the classic total eclipse silhouette. In the **NoDisk** position, the disk is removed entirely, and the corona extends all the way to the center, forming a bright starburst with no dark core. The NoDisk mode is useful when you want a pure radial glow effect without the eclipse metaphor.

---

### Switch 8 — Promin.

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Prominences** adds a bright ring at the edge of the occluding disk, simulating the solar prominences visible during totality. When **On**, an intense band of light appears precisely at the disk boundary, like the chromosphere peeking around the Moon's limb. This ring is only visible when **Eclipse** (Switch 7) is set to **Disk**: without the disk, there is no edge to illuminate. The prominence ring has a fixed brightness of approximately 78% of maximum and spans about 8 pixels in width.

:::note
Real solar prominences are eruptions of plasma visible as bright pink or red arcs during totality. Corona's prominences are a simplified luminance ring rather than colored arcs, but they serve the same compositional purpose (a bright accent framing the dark disk.)
:::

---

### Switch 9 — CtrLock

| Property | Value |
|----------|-------|
| Off | Center |
| On | Drift |
| Default | Center |

**CtrLock** chooses whether the corona center is fixed or drifting. In the **Center** position, the corona is locked to the center of the frame. In the **Drift** position, the center follows a slow ***Lissajous curve***: two independent sine oscillators at prime-number rates (73 and 97 per frame) move the center horizontally and vertically. The resulting path never exactly repeats, producing a gentle, wandering motion. The drift range is modest, roughly ±128 pixels from center, keeping the corona within the frame.

---

### Switch 10 — ColorMode

| Property | Value |
|----------|-------|
| Off | Mono |
| On | Butler |
| Default | Mono |

**ColorMode** selects between two color palettes. In the **Mono** position, the corona is tinted with a single color controlled by the **Color** knob (Knob 6). In the **Butler** position, the program applies a distance-based color gradient inspired by the eclipse paintings of ***Howard Russell Butler***: an American painter who documented total solar eclipses for the American Museum of Natural History between 1918 and 1932. The Butler palette renders the inner corona as warm pearl-white with a slight amber shift, transitioning to cooler blue-green tones in the outer corona. The transition occurs across three distance zones.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping the corona synthesis and compositing. The sync delay pipeline still aligns timing, so there is no glitch on toggle. Use Bypass for instant A/B comparison between the processed and unprocessed signal.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** controls the wet/dry blend between the corona-composited result and the delayed original signal. At zero, you hear only the dry signal: no corona is visible. At full, you see the fully composited result with the corona glowing over the input. Intermediate positions create a partial overlay, useful for subtly suggesting a corona glow without overwhelming the source image. The mix is applied via three interpolators (one per YUV channel) after the compositing stage.

---

## Background

### Total solar eclipses in art and science

A total solar eclipse is one of the most dramatic events in the natural world. For a few minutes, the Moon's shadow races across the Earth's surface, day turns to twilight, and the Sun's corona: invisible at all other times: blazes into view. Before photography could reliably capture the corona's faint, extended structure, painters and illustrators were dispatched to eclipse sites to make rapid observational sketches during the precious minutes of totality. Howard Russell Butler, a Princeton-trained lawyer turned artist, made some of the most scientifically rigorous eclipse paintings between 1918 and 1932. His canvases, displayed at the American Museum of Natural History in New York, remain among the finest visual records of coronal structure from the pre-photographic era. Corona's Butler color mode is a tribute to his palette: warm pearl tones close to the disk edge, transitioning to a blue-green glow in the outer corona.

### Direct digital synthesis and drifting phases

Corona's evolving streamer pattern is generated by ***direct digital synthesis*** (DDS). Three phase accumulators increment by a fixed amount on each video frame (at the vertical sync rate). The accumulated phase values index into a 32-entry sine lookup table to produce time-varying angular offsets for the lobe function. Because the three accumulators advance at different rates (the ratios are approximately 1 : 0.625 : 0.3125), their combined effect is a slow, quasi-periodic modulation. The corona never loops back to the same exact pattern: it continuously evolves, producing an organic quality that simple rotation cannot achieve.

### Radial geometry and the octant trick

Computing per-pixel angle and distance from a center point in real time on an FPGA is a geometric challenge. Corona uses a classic ***octant decomposition*** technique: the pixel's displacement from center is classified into one of eight angular sectors, and a fractional position within that sector becomes the fine angle. This produces an 11-bit angle (3 bits of octant + 8 bits of fraction) without any division or trigonometric function: just comparisons and bit shifts. The distance is approximated with the ***octagon norm***: $\text{max}(|dx|, |dy|) + 0.375 \cdot \text{min}(|dx|, |dy|)$, which approximates Euclidean distance to within about 4% error using only addition and shifts.


---

## Signal Flow

### Signal Flow Notes

The corona synthesis engine is a purely generative pipeline: it computes a radial glow pattern from screen coordinates and phase accumulators, independent of the input video content. The input video only enters the picture at Stage 4 (additive compositing), where the corona is layered *on top* of the source.

Two interactions are worth noting. First, the compositing is ***additive*** for luminance: the corona's Y value is simply added to the input Y value, clamped at 1023. This means bright source areas plus a bright corona can clip to pure white. Second, the chrominance blending is ***proportional***: the UV channels are pulled toward the corona's color in proportion to the corona's intensity at that pixel. Dark corona regions leave the source color untouched; bright corona regions tint the source toward the corona's hue.

:::tip
Because the compositing is additive, Corona works beautifully with dark source material. Feed in a black signal and the corona stands alone. Feed in a dim, moody scene and the corona illuminates it like a distant light source.
:::


---

## Exercises

These exercises progress from a simple static corona to a fully animated, color-mapped eclipse composition. Each builds on the previous, engaging more of the parameter space.
### Exercise 1: First Eclipse

![First Eclipse result](/img/instruments/videomancer/corona/corona_ex1_s1.png)
*First Eclipse — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A static eclipse with a visible disk and a shaped corona.

#### Key Concepts

- Streamer count and asymmetry shape the corona's angular structure
- The disk creates the eclipse silhouette
- Brightness controls overall corona intensity

#### Video Source

A dark or dimly lit video source: a night scene, dark fabric, or a color bar pattern with low overall brightness.

#### Steps

1. Start with all defaults. You should see a faint corona around a dark center disk.
2. Turn **Brightness** (Knob 5) to about 70%. The corona becomes clearly visible (radial streaks glowing over your source.)
3. Sweep **Streamers** (Knob 2) through its range. Count the lobes as they change: 2 broad petals at minimum, then 3, 4, 5, 6, 8, 10, 12 at maximum. Settle on 6 streamers for a classic look.
4. Increase **Asymmetry** (Knob 3) to about 50%. Some lobes grow while others shrink, breaking the perfect symmetry.
5. Adjust **Disk Size** (Knob 4) until the dark circle feels balanced against the streamer length.
6. Toggle **Prominences** (Switch 8) to **On**. A narrow bright ring lights up at the disk edge.

#### Settings

| Control | Value |
|---------|-------|
| Rotation | 0% |
| Streamers | 6 (mid-range) |
| Asymmetry | 50% |
| Disk Size | ~30% |
| Brightness | 70% |
| Color | 0° |
| Eclipse | Disk |
| Promin. | On |
| CtrLock | Center |
| ColorMode | Mono |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Living Corona

![Living Corona result](/img/instruments/videomancer/corona/corona_ex2_s1.png)
*Living Corona — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated, color-mapped eclipse with drifting center and evolving streamers.

#### Key Concepts

- Phase drift produces evolving, non-repeating streamer motion
- Lissajous center drift adds spatial animation
- The Butler palette applies distance-based color

#### Video Source

A slowly moving camera feed or abstract video with gentle color gradients.

#### Steps

1. Begin with the settings from Exercise 1.
2. Turn **Rotation** (Knob 1) to about 25%. The streamer pattern begins to drift (lobes swell, merge, and reform in slow motion.)
3. Flip **CtrLock** (Switch 9) to **Drift**. The corona center begins a slow, wandering path across the frame. The streamer field slides over the source video.
4. Switch **ColorMode** (Switch 10) to **Butler**. The inner corona turns warm pearl-white, and the outer corona shifts to a cool blue-green (the classic eclipse palette.)
5. Increase **Streamers** to about 10 and **Asymmetry** to about 60%. The corona becomes complex and irregular (more like a real solar corona.)
6. Experiment with **Brightness** to find the balance between visible structure and source bleed-through.

#### Settings

| Control | Value |
|---------|-------|
| Rotation | 25% |
| Streamers | 10 |
| Asymmetry | 60% |
| Disk Size | ~30% |
| Brightness | 60% |
| Color | 0° |
| Eclipse | Disk |
| Promin. | On |
| CtrLock | Drift |
| ColorMode | Butler |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Chromatic Starburst

![Chromatic Starburst result](/img/instruments/videomancer/corona/corona_ex3_s1.png)
*Chromatic Starburst — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A vivid, full-frame starburst with user-controlled color, blended subtly over the source.

#### Key Concepts

- Without the disk, corona becomes a pure radial glow
- Monochrome color mode allows manual hue selection
- Mix controls intensity layering over the source

#### Video Source

Footage with strong visual structure (architecture, geometric patterns, or a live performance.)

#### Steps

1. Set **Eclipse** (Switch 7) to **NoDisk**. The dark disk vanishes, and the corona extends all the way to the center as a bright starburst.
2. Ensure **ColorMode** (Switch 10) is set to **Mono**. Now sweep the **Color** knob (Knob 6) through the full 360° range. The starburst shifts through warm golds, vivid cyans, deep purples (choose a color that complements your source material.)
3. Set **Streamers** to 4 for bold, wide lobes, and **Asymmetry** to about 40%.
4. Turn **Rotation** to about 15% for gentle animation.
5. Pull the **Mix** fader (Fader 12) down to about 50%. The starburst becomes a translucent overlay, adding a luminous texture to the source without overwhelming it.
6. Adjust **Brightness** to taste: lower values for a subtle glow, higher values for a dramatic burst.

#### Settings

| Control | Value |
|---------|-------|
| Rotation | 15% |
| Streamers | 4 |
| Asymmetry | 40% |
| Disk Size | 0% |
| Brightness | 55% |
| Color | 80° |
| Eclipse | NoDisk |
| Promin. | Off |
| CtrLock | Center |
| ColorMode | Mono |
| Bypass | Off |
| Mix | 50% |

---
## Glossary

- **Additive Compositing**: A blending method where the generated image is added to the source; bright regions glow over the scene while dark regions leave it untouched.

- **Butler Palette**: A distance-based color gradient inspired by Howard Russell Butler's eclipse paintings: warm pearl-white near the disk, transitioning to blue-green in the outer corona.

- **Corona**: The outermost region of the Sun's atmosphere, visible as a structured halo of plasma during a total solar eclipse.

- **Direct Digital Synthesis (DDS)**: A technique for generating time-varying waveforms by incrementing a phase accumulator at a fixed rate and using its value to index a lookup table.

- **Lissajous Curve**: A path traced by two perpendicular sinusoidal oscillations at different frequencies, producing a wandering, non-repeating figure.

- **Lobe**: One of the angular peaks in the corona's radial streamer pattern, formed by the summation of harmonically related sine functions.

- **Octant Decomposition**: A geometric technique that classifies a 2D vector into one of eight angular sectors to simplify angle computation without division or trigonometry.

- **Prominence**: A bright, localized feature at the edge of the solar disk, here simulated as a narrow luminance ring at the boundary of the occluding disk.

- **Radial Falloff**: The decrease in corona intensity with increasing distance from center, approximating an inverse-distance relationship.

- **Streamer**: An elongated ray of coronal plasma extending outward from the Sun, here generated by a multi-frequency angular function applied to radial geometry.

---
