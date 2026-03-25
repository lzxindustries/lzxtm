---
draft: true
sidebar_position: 258
slug: /instruments/videomancer/schufftan
title: "Schufftan"
image: /img/instruments/videomancer/schufftan/schufftan_hero_s1.png
description: "The Schüfftan process was a visual effects technique invented in 1920s German cinema."
---

![Schufftan hero image](/img/instruments/videomancer/schufftan/schufftan_hero_s1.png)
*Schufftan applying luminance-keyed mirror compositing to split a video frame into reflected miniature and live plate zones.*

---

## Overview

Schufftan is a video compositing program inspired by one of cinema's most ingenious practical effects. It divides your image into two worlds using luminance as a self-matte: bright areas are treated as a reflected miniature: reduced in contrast, softened, and tinted: while dark areas pass through as the live scene viewed through scraped-clear glass. The result is an uncanny split-reality effect where the same video appears to contain both a model and the real world.

The program recreates three signature artifacts of the original mirror technique. A per-scanline ***wobble*** simulates the physical vibration of a large mirror on set, breathing life into the boundary between reflection and reality. An ***edge double-image*** adds a ghosted overlap zone where matte and clear glass meet. And a ***mirror tint*** shifts the reflected region's color temperature, simulating the warm silver or cool blue cast of a real reflective surface.

At subtle settings, Schufftan can add an ethereal, otherworldly split to naturalistic footage. At extreme settings, it transforms the image into a fractured composite of contrasting textures (one side smooth and tinted, the other sharp and raw.)

:::tip
***The self-matte is the magic.*** Unlike a traditional key, Schufftan derives its matte directly from the video's own brightness: bright areas become the mirror, dark areas become the glass. This recreates the real technique where the mirror *itself* formed the matte.
:::

### What's In a Name?

The name ***Schufftan*** comes from Eugen Schüfftan, a German cinematographer who patented the mirror shot technique in 1923. The technique was most famously used by Fritz Lang in *Metropolis* (1927) to composite live actors into miniature cityscapes. A large mirror was placed at 45° to the camera. A miniature set was reflected in the mirror's intact surface, while the silver coating was scraped away in precise areas to reveal the live-action scene behind the glass. Hitchcock used the same technique in *Blackmail* (1929), and Marcel Carné employed it in *Les Enfants du Paradis* (1945). The method was eventually superseded by optical printing, but its distinctive visual character: the slightly unreal quality of the reflected plate, the soft boundary where two realities meet: remains evocative.

---

## Quick Start

1. Feed a video source with a range of bright and dark areas. Set **Key Thresh** (Knob 1) to about 50%. Bright areas shift in contrast and color: they've become the "reflected miniature." Dark areas pass through unchanged: they're the live scene behind the glass.
2. Increase **Key Soft** (Knob 2) to see the transition between the two zones widen into a soft gradient. The matte boundary dissolves.
3. Sweep **Mirror Tint** (Knob 3) through its range. Watch the reflected zone shift from warm amber to cool blue to cyan. The live zone remains untouched.
4. Turn up **Wobble Amt** (Knob 5) and adjust **Wobble Spd** (Knob 6). The matte boundary ripples per scanline, as though the mirror is vibrating on set.

---

## Parameters

![Videomancer front panel with Schufftan loaded](/img/instruments/videomancer/schufftan/schufftan_control_panel.png)
*Videomancer's front panel with Schufftan active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Key Thresh

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Key Thresh**, the luminance key threshold, sets the brightness level that divides the image into two zones. Pixels brighter than the threshold are treated as the "reflected miniature" and receive contrast reduction, tinting, and softening. Pixels dimmer than the threshold pass through as the "live plate."

At 0%, fully counterclockwise, the threshold is at black: nearly the entire image becomes the reflected zone. At 100%, fully clockwise, the threshold is at peak white: nearly the entire image passes through as the live plate. At the default of 50%, the image splits roughly at mid-gray.

:::note
The threshold is modulated by the **Wobble Amt** and **Wobble Spd** controls. When wobble is active, the effective threshold shifts per scanline, creating a rippling matte boundary.
:::

---

### Knob 2 — Key Soft

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Key Soft**, the key softness, controls the width of the gradient transition between the live plate and the reflected miniature. At 0%, the boundary is a hard edge: pixels snap instantly between the two zones. As Key Soft increases, the transition widens into a smooth ramp where both zones blend together.

At the default of about 25%, a moderate gradient produces a natural-looking boundary. High values create a broad, atmospheric crossfade between the two worlds. The softness range is symmetric around the threshold (it extends equally above and below the threshold level.)

---

### Knob 3 — Mirror Tint

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Mirror Tint** shifts the color temperature of the reflected zone, simulating the spectral characteristics of different mirror surfaces. The tint sweeps through four color regions as the knob rotates:

- **0 to 25%**: Warm silver (a slight amber cast, like aged glass.)
- **25 to 50%**: Neutral to cool blue: transitioning from clear reflection to the blue-shifted appearance of aluminum mirrors.
- **50 to 75%**: Cool blue to cyan (a deep, cold reflection.)
- **75 to 100%**: Cyan wrapping back to warm (completing the cycle.)

The tint offsets the U and V chrominance channels of the reflected zone only. The live plate is unaffected.

:::tip
For a subtle, cinematic look, keep Mirror Tint in the warm silver range (below 25%). For a science-fiction aesthetic, push it into the cool blue or cyan range.
:::

---

### Knob 4 — Contrast

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Contrast**, the contrast reduction control, compresses the tonal range of the reflected zone toward a slightly below-mid-gray anchor point. This simulates the reduced contrast inherent in mirror reflections, where scattered light fills in shadows and clips highlights.

At 0%, the reflected zone is fully compressed: all pixels collapse to a flat, uniform mid-tone. At 100%, no compression is applied and the reflected zone retains its original contrast. At the default of 50%, the reflected zone has noticeably less punch than the live plate, creating a clear visual distinction between the two worlds.

A subtle brightness boost of about 3% is applied to the reflected zone after contrast reduction, simulating the additional exposure from a reflective surface.

---

### Knob 5 — Wobble Amt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Wobble Amt**, the wobble amount, controls the depth of per-scanline matte displacement. A ***direct digital synthesis*** (DDS) oscillator shifts the effective key threshold up and down for each scanline, creating a rippling, organic matte boundary that simulates mirror vibration.

At 0%, the matte boundary is perfectly still. At low values, a gentle undulation gives the boundary a living, breathing quality. At high values, the threshold swings dramatically from line to line, shattering the matte into horizontal bands of alternating reflection and transparency.

---

### Knob 6 — Wobble Spd

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Wobble Spd**, the wobble speed, controls the frequency of the DDS oscillator that drives the scanline wobble. At low values, the wobble pattern drifts slowly, producing broad, gentle waves along the matte boundary. At high values, the oscillator cycles rapidly, producing fine, closely spaced ripples.

The wobble phase accumulates continuously across scanlines and wraps around, creating a repeating sinusoidal pattern. When **Wobble Amt** is at 0%, this control has no visible effect.

:::tip
For a realistic mirror vibration, keep both Wobble Amt and Wobble Spd at low values. The boundary should shimmer, not shatter.
:::

---

### Switch 7 — Invert Key

| Property | Value |
|----------|-------|
| Off | Normal |
| On | Invert |
| Default | Normal |

**Invert Key** reverses the matte polarity. In the **Normal** position, bright areas are treated as the reflected miniature and dark areas as the live plate: matching the original Schüfftan process where scraped-away silver revealed the live scene. In the **Invert** position, dark areas become the reflected zone and bright areas pass through.

Inverting the key does not change the matte shape: only which side receives the mirror processing. The key alpha is subtracted from 1023, so a pixel that was 70% reflected becomes 70% live.

---

### Switch 8 — Edge Dbl

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Edge Dbl**, the edge double-image toggle, enables a ghosted overlap artifact in the matte boundary zone. In the original Schüfftan process, partially scraped glass produced a region where both the reflected miniature and the live scene were faintly visible simultaneously (a characteristic double-image.)

When set to **On** (the default), pixels in the matte transition zone receive a dimmed copy of the live video added on top of the blend. The ghost is about 25% brightness of the live signal. When set to **Off**, the blend is clean with no ghosts. The edge zone is defined as the region where the key alpha falls between approximately 5% and 95%.

---

### Switch 9 — Detail Loss

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Detail Loss** enables a horizontal low-pass filter on the reflected zone's luminance, simulating the reduced sharpness of a mirror reflection. Reflected images are never quite as sharp as direct views: the glass surface introduces scatter, and the reflected subject is at a greater optical distance.

When set to **On** (the default), a two-tap horizontal average blurs the reflected luminance slightly. When set to **Off**, the reflected zone retains full horizontal detail.

---

### Switch 10 — Key Source

| Property | Value |
|----------|-------|
| Off | Y Only |
| On | Y+Edge |
| Default | Y Only |

**Key Source** determines what signal feeds the luminance key. In the **Y Only** position, only the input luminance determines the matte: a straightforward brightness split. In the **Y+Edge** position, the magnitude of horizontal luminance edges is added to the key distance, causing high-contrast edges to push toward the reflected zone.

The edge magnitude is the absolute horizontal difference between adjacent pixels, scaled by half before being added. This creates a more complex matte where edges and contours become part of the reflected world.

:::note
The Y+Edge mode makes the matte edge-aware, tending to place sharp boundaries in the reflected zone. This can produce an outline-like effect around subjects.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Schufftan processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the mirror-composited result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix**, the wet/dry crossfade, blends between the original unprocessed video and the full Schufftan composite. At 0%, the output is entirely the dry (unprocessed) input. At 100% (the default), the output is the full wet (processed) composite. Intermediate values produce a proportional blend using three parallel interpolators (one for each YUV channel.)

Mix is useful for dialing in subtle mirror effects without committing to the full composite. A setting around 50 to 75% produces a ghostly, translucent overlay where the mirror processing is present but the original image shows through.

---

## Background

### The Schüfftan Process

The Schüfftan process was born from a practical problem: how to place live actors into sets too expensive or impossible to build at full scale. Eugen Schüfftan's solution was elegant. A mirror was placed at 45° to the camera. A miniature set: a cityscape, a cathedral interior, a palace hallway: was positioned to the side, reflected into the mirror so it filled the camera's field of view. Then, with extraordinary precision, the silver coating was scraped from the mirror in the exact regions where live actors needed to appear. Through the cleared glass, the camera saw the real actors on a partial set behind the mirror. Through the intact silver, it saw the reflected miniature.

The result was a seamless in-camera composite. No post-production, no optical printing, no separate matte pass. The mirror was the matte.

This program recreates that technique digitally. Instead of a physical mirror, the input video's own luminance serves as the matte. Instead of scraping silver, you set a threshold.

### Mirror reflections in the real world

Real mirror reflections differ from direct observation in several measurable ways. The reflected image has lower contrast: scattered light within the glass fills in shadows and softens highlights. Color temperature shifts because glass and metallic coatings selectively absorb and reflect different wavelengths. Silver mirrors tend warm; aluminum mirrors lean cool. Fine detail is slightly softened by surface imperfections and the additional optical path length. And reflections from large, unsupported mirrors exhibit a subtle oscillation: thermal currents and mechanical vibrations cause the image to shimmer.

Schufftan models each of these characteristics: contrast reduction, color tint, detail loss, and wobble.


---

## Signal Flow

### Signal Flow Notes

Two key interactions define the Schufftan signal path:

1. **The self-matte feedback loop.** The input luminance simultaneously *is* the video content and *determines* how that content is processed. Bright pixels generate high key alpha, routing themselves into the reflected plate path. Dark pixels generate low key alpha, routing themselves into the live plate path. This creates a recursive aesthetic relationship: the image's own tonal structure defines the boundary between its two processed versions.

2. **Wobble modulates the matte, not the image.** The DDS oscillator offsets the key threshold per scanline, not the pixel data. This means the image content itself doesn't move: only the dividing line between reflection and reality shifts. The visual result is a boundary that ripples like heat shimmer or a vibrating mirror, while both the reflected and live zones remain stable.

:::tip
**Contrast sets the distinction.** The contrast reduction control is the most powerful visual separator between the two zones. At 50%, the reflected zone is visibly flatter and softer than the live zone. This contrast difference: more than the tint or detail loss: is what sells the illusion of a mirror.
:::


---

## Exercises

These exercises progress from basic matte splitting to full cinematic mirror compositing. Each builds on the previous, gradually engaging more of the Schufftan effect chain.
### Exercise 1: The Mirror Split

![The Mirror Split result](/img/instruments/videomancer/schufftan/schufftan_ex1_s1.png)
*The Mirror Split — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean two-zone composite where bright areas appear as a contrast-reduced, tinted reflection and dark areas pass through as the live scene.

#### Key Concepts

- Luminance self-matte divides the image by brightness
- Key threshold sets the dividing line
- Key softness controls the transition width

#### Video Source

Footage with strong tonal contrast: a face lit from one side, architecture with bright sky and dark interiors, or a subject against a bright background.

#### Steps

1. **Set the threshold**: Turn **Key Thresh** (Knob 1) to about 50%. The image splits: bright areas lose contrast and shift color, dark areas look normal.
2. **Soften the edge**: Increase **Key Soft** (Knob 2) from 0% to about 40%. The hard boundary dissolves into a smooth gradient. Watch the transition zone widen.
3. **Tint the reflection**: Sweep **Mirror Tint** (Knob 3) slowly from left to right. The reflected zone shifts from warm amber through neutral to cool blue. Find a tint that makes the reflected zone feel like a different material.
4. **Reduce contrast**: Lower **Contrast** (Knob 4) to about 40%. The reflected zone flattens: shadows fill in, highlights dim. It starts to look like a reflection rather than the real thing.
5. **Compare**: Toggle **Bypass** (Switch 11) to see the unprocessed source. Note how the Schufftan composite creates a tangible sense of two overlapping realities.

#### Settings

| Control | Value |
|---------|-------|
| Key Thresh | 50% |
| Key Soft | 40% |
| Mirror Tint | ~15% |
| Contrast | 40% |
| Wobble Amt | 0% |
| Wobble Spd | 0% |
| Invert Key | Normal |
| Edge Dbl | On |
| Detail Loss | On |
| Key Source | Y Only |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: The Vibrating Mirror

![The Vibrating Mirror result](/img/instruments/videomancer/schufftan/schufftan_ex2_s1.png)
*The Vibrating Mirror — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated mirror composite with a living, breathing boundary that shimmers like a physical mirror vibrating on set.

#### Key Concepts

- DDS wobble shifts the matte boundary per scanline
- Wobble amount and speed create organic rippling
- Edge double adds a ghosted overlap at the boundary

#### Video Source

A static camera shot with a clear split between bright and dark regions (a window against a dark wall, or a silhouette.)

#### Steps

1. **Establish the split**: Set **Key Thresh** to 45% and **Key Soft** to 30% to create a soft matte boundary.
2. **Add wobble**: Increase **Wobble Amt** (Knob 5) to about 25%. The matte boundary begins to ripple horizontally. Each scanline's threshold shifts slightly.
3. **Set wobble speed**: Adjust **Wobble Spd** (Knob 6) to about 20%. The ripple pattern should drift slowly (a gentle shimmer, not a strobe.)
4. **Check the edge**: With **Edge Dbl** (Switch 8) set to **On**, look closely at the boundary zone. A faint ghost of the live image bleeds through the reflected zone. Toggle it off to compare (the ghosted version has more depth.)
5. **Invert**: Flip **Invert Key** (Switch 7) to **Invert**. The reflected and live zones swap. Dark areas now receive the mirror treatment while bright areas pass through naturally.
6. **Push it**: Increase Wobble Amt to 80% or higher. The matte fractures into horizontal bands of alternating reflection and transparency (an extreme, abstract effect.)

#### Settings

| Control | Value |
|---------|-------|
| Key Thresh | 45% |
| Key Soft | 30% |
| Mirror Tint | ~35% |
| Contrast | 50% |
| Wobble Amt | 25% |
| Wobble Spd | 20% |
| Invert Key | Normal |
| Edge Dbl | On |
| Detail Loss | On |
| Key Source | Y Only |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Edge-Keyed Dreamscape

![Edge-Keyed Dreamscape result](/img/instruments/videomancer/schufftan/schufftan_ex3_s1.png)
*Edge-Keyed Dreamscape — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dreamlike composite where sharp edges in the image trigger the reflected zone, creating a halo of tinted, softened mirror-world around contours and details.

#### Key Concepts

- Y+Edge key source adds contour information to the matte
- Mix control blends between dry and wet for translucent effects
- All parameters interact to create complex composites

#### Video Source

Footage with fine detail and well-defined edges: foliage, fabric textures, text, or a face with sharp features.

#### Steps

1. **Engage edge keying**: Set **Key Source** (Switch 10) to **Y+Edge**. Set **Key Thresh** to about 35% and **Key Soft** to 50%.
2. **Observe the contours**: The reflected zone now wraps around edges and high-contrast boundaries. Flat areas tend toward the live plate; textured areas shift toward the reflected zone.
3. **Style the reflection**: Set **Mirror Tint** to about 60% for a cool blue cast. Lower **Contrast** to 30% for a heavily compressed, dreamy reflected zone.
4. **Add detail loss**: Confirm **Detail Loss** (Switch 9) is **On**. The reflected zone blurs slightly, enhancing the distinction between the sharp live plate and the soft reflection.
5. **Gentle wobble**: Set **Wobble Amt** to about 15% and **Wobble Spd** to 10%. The contour halos shimmer subtly.
6. **Blend back**: Lower **Mix** (Fader 12) to about 75%. The unprocessed image bleeds through, creating a translucent, ghostly overlay.

#### Settings

| Control | Value |
|---------|-------|
| Key Thresh | 35% |
| Key Soft | 50% |
| Mirror Tint | ~60% |
| Contrast | 30% |
| Wobble Amt | 15% |
| Wobble Spd | 10% |
| Invert Key | Normal |
| Edge Dbl | On |
| Detail Loss | On |
| Key Source | Y+Edge |
| Bypass | Off |
| Mix | 75% |

---
## Glossary

- **Alpha Blend**: A compositing operation that mixes two images proportionally using a per-pixel opacity value (alpha). Alpha of 0 shows only the first image; alpha of 1 shows only the second.

- **Contrast Reduction**: Compressing the tonal range of an image toward a central gray point, reducing the difference between the brightest and darkest values.

- **DDS (Direct Digital Synthesis)**: A technique for generating waveforms by incrementing a phase accumulator at a programmable rate. Used here to create the per-scanline wobble oscillation.

- **Edge Zone**: The transition region where the key alpha is neither fully live nor fully reflected: between approximately 5% and 95% opacity. This is where the edge double artifact appears.

- **Key Threshold**: The luminance level that divides the image into two zones. Pixels above the threshold are assigned to one composite layer; pixels below are assigned to the other.

- **Live Plate**: In the Schüfftan process, the real scene viewed through the scraped-clear regions of the mirror. In this program, the portion of the image below the key threshold that passes through without mirror processing.

- **Matte**: A mask that defines which parts of an image are visible or transparent. In self-matting, the matte is derived from the image's own content rather than from a separate source.

- **Reflected Plate**: The miniature or painting reflected in the mirror's intact silver surface. In this program, the portion of the image above the key threshold that receives contrast reduction, tinting, detail loss, and brightness boost.

- **Self-Matte**: A compositing technique where the matte mask is derived from the image being composited, rather than from a separate matte source. The Schüfftan process is a physical self-matte (the mirror's silver coating is the mask.)

- **Wobble**: Per-scanline oscillation of the key threshold, simulating the physical vibration of a mirror. The threshold shifts up and down for each horizontal line, creating a rippling matte boundary.

---
