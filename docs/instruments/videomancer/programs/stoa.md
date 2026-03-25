---
draft: true
sidebar_position: 288
slug: /instruments/videomancer/stoa
title: "Stoa"
image: /img/instruments/videomancer/stoa/stoa_hero_s1.png
description: "The stoa was the defining architectural form of ancient Greece — a long covered walkway fronted by a row of columns."
---

![Stoa hero image](/img/instruments/videomancer/stoa/stoa_hero_s1.png)
*Stoa transforming a video source into a fluted colonnade of light and shadow, as if the image were carved into a Greek temple facade.*

---

## Overview

Stoa is a video processing program that carves the image into vertical strips resembling the fluted columns of a Greek Doric temple. Each strip is shaded with a cosine curve that darkens the edges and brightens the center, producing the concave cross-section of a classical column flute. Dark ***arris*** lines appear at the boundaries between flutes, and a controllable light angle shifts the cosine highlight across the surface, simulating sunlight raking across stone. The result is a striking three-dimensional illusion: the flat video appears to be projected onto the surface of a corrugated colonnade.

Beyond mere shading, Stoa can render an ***entablature***: a horizontal band of alternating triglyphs and metopes: across the top of the frame, capping the colonnade with architectural detail. A capital highlight zone can soften the transition between columns and entablature. Depth fading darkens columns toward the edges of the frame, suggesting a receding perspective. An optional stone color tint shifts the hue of the rendered surface from cool to warm, evoking different kinds of marble or limestone.

:::tip
Start with the preset **Columnar Lgt** for a wide-column, high-contrast introduction to the effect. Then try **Architectural** for a fuller facade with entablature and capitals.
:::

### What's In a Name?

A ***stoa*** was a covered walkway in ancient Greek architecture, defined by a long row of columns on one side. The most famous example is the Stoa of Attalos in the Athenian Agora (c. 150 BC), reconstructed in the 1950s. Looking through a colonnade of fluted Doric columns: each shaft carved with twenty shallow channels that catch the light differently as the sun moves: was one of the foundational visual experiences of the classical world. The Stoic school of philosophy takes its name from the Stoa Poikile ("Painted Porch") in Athens, where Zeno of Citium taught. Column fluting was not merely decorative; Vitruvius noted that the channels corrected the optical flattening of smooth cylinders in direct sunlight.

---

## Quick Start

1. Set **Column W** (Knob 1) to a middle position. The video splits into several wide vertical strips, each shaded from bright center to dark edges (you can already see the fluting.)
2. Turn **Flute Depth** (Knob 2) clockwise past the halfway mark. The contrast between the bright flute centers and dark troughs deepens dramatically, and the image takes on a corrugated, carved look.
3. Slowly sweep **Light Angle** (Knob 3) through a full rotation. Watch the highlight shift across each flute, as if you were moving a spotlight around the colonnade.
4. Raise **Entablatur** (Knob 5) from zero. A patterned horizontal band appears at the top of the frame, alternating between darker triglyphs and lighter metopes, completing the architectural illusion.

---

## Parameters

![Videomancer front panel with Stoa loaded](/img/instruments/videomancer/stoa/stoa_control_panel.png)
*Videomancer's front panel with Stoa active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Column W

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 3 |

**Column W** selects the pixel width of each column strip. The eight available settings range from narrow (40 pixels) to wide (240 pixels). At the narrowest setting the frame divides into many thin columns, producing a tight vertical rhythm like a dense colonnade. At the widest setting, each column occupies a large fraction of the screen and the concave shading becomes a broad, gentle curve.

The column width also determines the scale of the entablature pattern and the capital zones (everything in the architecture scales together.)

---

### Knob 2 — Flute Depth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Flute Depth** controls the amplitude of the cosine shading applied across each column strip. At 0%, all flutes are flat: the image passes through with no visible concavity. As you increase this control, the difference between the bright flute center and the dark flute edges grows. At 100%, the shading spans the full dynamic range: flute centers are nearly at full brightness and flute edges approach black. The cosine shape ensures the transition is always smooth, never harsh.

:::note
Because the fluting is applied as a brightness modulation on the input video, the actual contrast depends on the source material. A bright source produces vivid fluting; a dark source produces subtler grooves.
:::

---

### Knob 3 — Light Angle

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Light Angle** shifts the phase of the cosine shading function, moving the highlight position within each flute. At 0°, the highlight sits at the center of each flute, as if light were falling straight on. As you rotate the control, the highlight slides to one side, simulating raking light from the left or right. A full 360° sweep moves the highlight all the way across the flute and back to center.

This control brings the colonnade to life. Sweeping it slowly mimics the passage of the sun across a temple facade over the course of a day.

---

### Knob 4 — Arris W

| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 1 |

**Arris W** sets the width of the dark arris lines at the boundaries between flutes. An ***arris*** is the sharp ridge where two adjacent concave channels meet on a column. In the Doric order, arrises are not rounded: they form crisp edges that cast thin shadow lines. The four available settings range from a single-pixel hairline to a four-pixel-wide shadow band. Wider arrises make the column divisions more prominent and graphic.

---

### Knob 5 — Entablatur

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Entablatur** controls the height of the entablature region at the top of the frame. At 0%, no entablature is drawn and the columns fill the entire frame. As you increase this control, a horizontal band of alternating triglyph and metope panels appears at the top. The triglyphs are rendered in a darker stone tone, and the metopes remain in the lighter column surface color. The pattern repeats at the same period as the column width, so the entablature aligns with the colonnade below it.

:::tip
In classical architecture, a ***triglyph*** is a rectangular panel with three vertical grooves, and a ***metope*** is the plain panel between two triglyphs. Together they form the frieze of the Doric order, sitting atop the columns.
:::

---

### Knob 6 — Stone Color

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Stone Color** shifts the hue of the rendered stone surface. At the center position, the surface is a warm neutral: a pale sandstone. Rotating counterclockwise pulls the color cooler (bluish-grey, like Pentelic marble), while rotating clockwise pushes it warmer (golden, like Naxian marble). This control offsets the U and V chroma channels of the stone in opposite directions, creating natural hue shifts without introducing artificial saturation.

---

### Switch 7 — Flute Count

| Property | Value |
|----------|-------|
| Off | 20 Doric |
| On | Fit Frame |
| Default | Fit Frame |

**Flute Count** selects between two fluting densities. When set to **20 Doric**, Stoa calculates flutes at the classical Doric standard of twenty channels per column: the count prescribed by Vitruvius. When set to **Fit Frame**, the count increases to twenty-four, which produces narrower, more closely spaced flutes within each column.

:::note
If your column width is narrow, the difference between 20-flute and 24-flute modes may be subtle, because individual flute widths become very small in both cases.
:::

---

### Switch 8 — Light Anim

| Property | Value |
|----------|-------|
| Off | Static |
| On | Animated |
| Default | Static |

**Light Anim** enables an automated slow sweep of the light angle. When set to **Static**, the light position is controlled solely by the **Light Angle** knob. When set to **Animated**, a ***direct digital synthesizer*** (DDS) accumulator adds a small increment to the light phase on every video frame. The highlight drifts steadily across the flutes, creating the appearance of a moving sun. The **Light Angle** knob becomes a starting offset for the animation.

---

### Switch 9 — Capitals

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Capitals** enables a highlight zone between the entablature and the column shafts properly. When turned **On**, a 40-scanline band of brighter stone color appears just below the entablature region, representing the ***echinus*** and ***abacus*** of a Doric capital. This band is drawn in a lighter shade than the column body, providing a visual transition between the horizontal entablature and the vertical fluting.

:::note
Capitals are only visible when **Entablatur** (Knob 5) is set above zero, because they appear directly below the entablature zone. With the entablature at zero, the capital zone is pushed off the top of the frame.
:::

---

### Switch 10 — Depth Fade

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Depth Fade** darkens columns closer to the left and right edges of the frame, suggesting a receding colonnade stretching into perspective. When set to **On**, luminance is reduced proportionally to the pixel's horizontal distance from the frame center. Columns at the center remain at full brightness while columns at the edges dim, as though the flanking columns are in shadow or receding into space.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input video directly to the output, skipping all Stoa processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw source and the colonnade effect.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (original) video and the wet (processed) video at the output stage. At 0%, the output is entirely the unprocessed source. At 100%, the output is entirely the Stoa-processed colonnade. Intermediate values produce a transparent overlay, blending the architectural shading with the underlying image. Three independent interpolators handle Y, U, and V channels to maintain correct color balance at all mix positions.

:::tip
At moderate Mix values (30–60%), the fluting appears as a subtle texture overlaid on the source, like a column-shaped vignette. This is an excellent way to add depth and structure to live camera footage without obscuring the content.
:::

---

## Background

### Doric fluting and the cosine profile

The concave cross-section of a Doric column flute is remarkably close to a cosine curve. Each of the twenty channels is a segment of a cylinder, so when lit from one side, the reflected brightness varies as a cosine function of the angle from the surface normal to the light direction. This relationship: brightness proportional to the cosine of the incidence angle: is known as ***Lambert's cosine law*** and applies to any ideal diffuse surface. Stoa exploits this physical fact directly: a 32-entry cosine lookup table, stored entirely in FPGA registers (no block RAM needed), provides the shading value for each horizontal pixel position within a flute.

### Directional lighting in video synthesis

By shifting the phase of the cosine function, Stoa simulates the visual effect of moving a light source around a three-dimensional surface. In physical columns, as the sun moves across the sky, the highlight on each flute sweeps from one edge to the other. The columns appear to subtly change shape as different portions of each channel catch the light. Stoa's **Light Angle** control and **Light Anim** toggle recreate this phenomenon digitally. The animated mode uses a frame-rate DDS accumulator: a counter that advances by a fixed step each frame: to produce smooth, continuous motion.

### Architectural synthesis as video processing

Stoa belongs to a tradition of using geometric patterns as video processing masks. Rather than generating imagery from scratch (synthesis) or simply adjusting brightness and contrast (color correction), it imposes an architectural structure: repeating columns, entablature patterns, arris lines: onto the input video. The video becomes the surface of the building. This is related to ***spatial modulation***, where a pattern is multiplied with the image to selectively reveal or suppress different regions.


---

## Signal Flow

### Signal Flow Notes

The shading function in Stage 3 is not a simple multiply: it takes the input luminance, subtracts the inverse of the flute shade (creating the concave darkening), and then adds a stone-base brightness offset. This means that even without any input video, the colonnade has its own inherent brightness. The arris override replaces the entire pixel with a fixed dark stone color, functioning as a hard mask rather than a modulation.

The entablature and capital zones are layered on top of the shading result in Stage 3 with priority: capitals override shading, and the entablature (triglyph/metope) overrides both. This means the triglyph pattern sits atop whatever columns are below it, which matches real architecture: the entablature is a horizontal band that bridges between columns.

:::tip
**Depth fade and Mix interact.** Because depth fade darkens edge columns before the wet/dry mix, a moderate Mix setting can restore brightness to the edges while keeping the center fully fluted. This creates a vignette-like focus effect.
:::


---

## Exercises

These exercises explore Stoa from simple column shading to full architectural facade composition. Each builds on the previous, adding more architectural elements.
### Exercise 1: Sunlit Colonnade

![Sunlit Colonnade result](/img/instruments/videomancer/stoa/stoa_ex1_s1.png)
*Sunlit Colonnade — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A simple row of fluted columns with a sweeping spotlight, transforming the video source into a sunlit ancient colonnade.

#### Key Concepts

- Cosine shading creates the illusion of carved stone
- Light angle shifts the highlight within each flute
- Arris lines divide flutes with sharp shadow edges

#### Video Source

A live camera feed or recorded footage with moderate contrast and recognizable subjects.

#### Steps

1. Set **Column W** (Knob 1) to step 5 (about 120-pixel-wide columns). The video divides into broad vertical strips.
2. Turn **Flute Depth** (Knob 2) to about 70%. Deep concave shadows appear within each strip.
3. Slowly sweep **Light Angle** (Knob 3) through 360°. The bright highlight slides across each flute, and the shadows shift in response.
4. Increase **Arris W** (Knob 4) to step 3. Bold arris lines appear at flute boundaries, making the column structure more graphic.
5. Toggle **Light Anim** (Switch 8) to **Animated**. The highlight now drifts continuously (the sun is moving.)

#### Settings

| Control | Value |
|---------|-------|
| Column W | 4 (120 px) |
| Flute Depth | 70% |
| Light Angle | 90° |
| Arris W | 2 (3 px) |
| Entablatur | 0% |
| Stone Color | 0° |
| Flute Count | 20 Doric |
| Light Anim | Animated |
| Capitals | Off |
| Depth Fade | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Temple Facade

![Temple Facade result](/img/instruments/videomancer/stoa/stoa_ex2_s1.png)
*Temple Facade — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A complete Doric temple facade with columns, capitals, and entablature.

#### Key Concepts

- Entablature adds horizontal architectural structure
- Capitals provide a transitional highlight zone
- Stone color tinting evokes different types of marble

#### Video Source

Static or slow-moving footage with a dominant vertical composition, such as trees, buildings, or curtains.

#### Steps

1. Set **Column W** (Knob 1) to step 3 (about 80-pixel columns) for a proportioned colonnade.
2. Set **Flute Depth** (Knob 2) to about 60%. The fluting is visible but not overpowering.
3. Raise **Entablatur** (Knob 5) to about 25%. A horizontal band with alternating dark and light panels appears at the top of the frame.
4. Toggle **Capitals** (Switch 9) to **On**. A bright highlight band appears just below the entablature (the column capitals.)
5. Rotate **Stone Color** (Knob 6) to about 45°. The stone surface warms to a golden hue.
6. Toggle **Depth Fade** (Switch 10) to **On**. The columns at the edges darken, giving the facade a sense of depth.

#### Settings

| Control | Value |
|---------|-------|
| Column W | 2 (80 px) |
| Flute Depth | 60% |
| Light Angle | 45° |
| Arris W | 1 (2 px) |
| Entablatur | 25% |
| Stone Color | 45° |
| Flute Count | 20 Doric |
| Light Anim | Static |
| Capitals | On |
| Depth Fade | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Ghostly Ruins

![Ghostly Ruins result](/img/instruments/videomancer/stoa/stoa_ex3_s1.png)
*Ghostly Ruins — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A translucent colonnade overlay that turns the source footage into a spectral view through ancient ruins.

#### Key Concepts

- Low Mix values blend the colonnade as a translucent overlay
- Narrow columns create a dense, screen-like texture
- Animated light on a transparent colonnade creates dreamy motion

#### Video Source

Footage of landscapes, clouds, or ocean waves: subjects that evoke open sky visible through broken architecture.

#### Steps

1. Set **Column W** (Knob 1) to step 2 (about 60-pixel columns) for a dense colonnade.
2. Set **Flute Depth** (Knob 2) to about 40%. Moderate fluting (enough to see the carved shape but not black shadows.)
3. Toggle **Flute Count** (Switch 7) to **Fit Frame** (24 flutes). The denser fluting creates a finer texture.
4. Toggle **Light Anim** (Switch 8) to **Animated**. The highlight drifts across the ruins.
5. Lower **Mix** (Fader 12) to about 40%. The colonnade becomes a translucent overlay (the source shows through the stone.)
6. Raise **Entablatur** (Knob 5) to about 15%. A faint architectural cap appears at the top.
7. Rotate **Stone Color** (Knob 6) to about 270° for a cool, bluish marble tone.

#### Settings

| Control | Value |
|---------|-------|
| Column W | 1 (60 px) |
| Flute Depth | 40% |
| Light Angle | 0° |
| Arris W | 0 (1 px) |
| Entablatur | 15% |
| Stone Color | 270° |
| Flute Count | Fit Frame |
| Light Anim | Animated |
| Capitals | Off |
| Depth Fade | Off |
| Bypass | Off |
| Mix | 40% |

---
## Glossary

- **Arris**: The sharp ridge formed where two adjacent concave flutes meet on a column; rendered as a dark line at flute boundaries.

- **Capital**: The topmost element of a column, sitting between the shaft and the entablature; Stoa renders it as a bright highlight band.

- **Cosine Shading**: A brightness modulation technique using a cosine function to simulate the light falloff across a curved surface.

- **DDS (Direct Digital Synthesis)**: A technique for generating a waveform by accumulating a phase value at a fixed rate; used here for smooth light animation.

- **Doric Order**: The oldest and most austere of the Greek architectural orders, characterized by columns with twenty shallow flutes and no base.

- **Entablature**: The horizontal structure resting atop columns, divided into architrave, frieze (with triglyphs and metopes), and cornice.

- **Fluting**: The shallow concave channels carved vertically into the shaft of a column, creating a play of light and shadow.

- **Interpolator**: A hardware module that performs linear interpolation between two values; used here for the wet/dry crossfade.

- **Lambert's Cosine Law**: The physical principle that brightness of a diffuse surface is proportional to the cosine of the angle between the surface normal and the light direction.

- **Metope**: The plain panel between two triglyphs in a Doric frieze.

- **Stoa**: A covered walkway with a colonnade on one side, the archetypal public space of ancient Greek cities.

- **Triglyph**: A rectangular element of the Doric frieze with three vertical grooves, placed above each column and between metopes.

---
