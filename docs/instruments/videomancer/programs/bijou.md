---
draft: true
sidebar_position: 18
slug: /instruments/videomancer/bijou
title: "Bijou"
image: /img/instruments/videomancer/bijou/bijou_hero_s1.png
description: "Bijou recreates two foundational visual techniques of silent cinema: the iris mask and the title card frame."
---

![Bijou hero image](/img/instruments/videomancer/bijou/bijou_hero_s1.png)
*Bijou applying a feathered circle iris mask to isolate a performer against a sepia-tinted dimmed background, recreating the silent cinema spotlight effect.*

---

## Overview

Bijou is a silent cinema iris mask and title card generator. It places a geometric aperture: circle, rectangle, diamond, or keyhole: over the video frame, revealing the image inside while dimming and tinting the region outside. The effect recreates the mechanical iris transitions that early filmmakers cranked open and shut to begin and end scenes, spotlight characters, or simulate looking through a keyhole or telescope.

A second mode replaces the iris with a decorative double-rectangle border frame: the ornamental surround that enclosed text on silent film intertitle cards. Corner ornaments and color tinting complete the illusion. Bijou doesn't render text, but it builds the visual container: the gilded frame around the words.

At gentle settings, Bijou produces smooth photographic vignettes. At hard settings, it cuts a crisp geometric window. With the fill brightness and tint color controls, the masked region becomes a toned canvas rather than solid black, evoking the amber and blue-tinted nitrate prints of early twentieth-century cinema.

:::tip
Bijou is a ***processing*** program. It transforms your input video: it doesn't generate images from scratch. Feed it a camera, a pattern generator, or the output of another program.
:::

### What's In a Name?

A ***bijou*** is a small, delicate jewel or ornamental trinket: and by extension, the word became shorthand for the intimate neighborhood cinemas of the early twentieth century. The "Bijou Theatre" was the little gem on the corner, the jewel box where silent films flickered to life. The program's iris masks and decorative title frames are the visual jewelry of that era: small, precise, and ornamental.

---

## Quick Start

1. Feed a video source into Videomancer. Turn **Size** (Knob 1) counterclockwise to shrink the iris. A circular window appears, revealing the image inside while the outside dims to black.
2. Turn **Softness** (Knob 4) clockwise. The hard edge of the iris dissolves into a smooth vignette (the feathered glow of a vintage lens.)
3. Increase **Fill Brt** (Knob 5) to bring the outside region back as a dimmed version of the video. Now increase **Tint Color** (Knob 6) to wash the fill with sepia, green, blue, or magenta tones.
4. Flip **Mode** (Switch 7) to **Title**. The iris vanishes and a decorative double-rectangle border frame appears (the silent film intertitle surround.)

---

## Parameters

![Videomancer front panel with Bijou loaded](/img/instruments/videomancer/bijou/bijou_control_panel.png)
*Videomancer's front panel with Bijou active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Size

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Size** controls the radius of the iris aperture in Iris mode, or the margin width of the border frame in Title mode. At 0%, fully counterclockwise, the iris closes to a tiny point at the center of the frame, masking nearly the entire image. As Size increases, the aperture opens wider, revealing more of the picture. At 100%, the iris extends beyond the edges of the frame, effectively disappearing. In Title mode, a smaller Size pushes the border rectangles closer to the edges of the frame; a larger Size moves them inward, creating wider margins.

:::note
The relationship between the knob position and the visible aperture size is not perfectly linear: the pot value is scaled by approximately 1.25× to cover the full pixel range of the frame. Very small iris sizes may clip to a nearly invisible point.
:::

---

### Knob 2 — Center X

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Center X** sets the horizontal position of the iris center. At 0%, the center sits at the left edge of the frame. At 50%, it sits in the middle. At 100%, it sits at the right edge. In Title mode, Center X has no effect (the border frame is always centered on the screen.)

---

### Knob 3 — Center Y

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Center Y** sets the vertical position of the iris center. At 0%, the center sits at the top of the frame. At 50%, the center sits in the middle. At 100%, it sits at the bottom. Like Center X, this control has no effect in Title mode.

:::tip
Pan the iris across the frame by sweeping **Center X** and **Center Y** together. This recreates the classic "iris-down" technique where the director closes the iris onto a character's face before cutting to the next scene.
:::

---

### Knob 4 — Softness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Softness** controls the width of the feathered transition zone at the iris edge. At 0%, the edge is a hard, clean cut: a sharp boundary between revealed and masked regions. As Softness increases, the transition zone widens, blending the inside and outside regions together in a smooth gradient. At 100%, the feather extends so far that the iris becomes a broad, gentle vignette.

When Softness is zero, the mask behaves like a binary stencil: each pixel is either fully revealed or fully masked. Any nonzero Softness value introduces a linear alpha ramp across the transition zone, proportional to the ***signed distance field*** value at each pixel.

---

### Knob 5 — Fill Brt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Fill Brt** sets the brightness of the video in the masked (outside) region. At 0%, the masked area is solid black: the traditional silent cinema iris look. As Fill Brt increases, the masked region becomes a progressively brighter copy of the input video. At 100%, the fill reaches full brightness, though the tint color still shifts its hue.

The fill brightness is computed as a simple multiplication: the input luminance is scaled by the Fill Brt value. The chrominance channels pass through to the fill region with tinting applied independently.

---

### Knob 6 — Tint Color

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Tint Color** selects the hue applied to the fill region's chrominance. The knob sweeps through four color zones, each occupying one quarter of the rotation:

- **0% to 25%**: Sepia / amber (the warm tone of aged nitrate film)
- **25% to 50%**: Green (the tint of certain hand-colored silent prints)
- **50% to 75%**: Blue (moonlight and night scenes)
- **75% to 100%**: Magenta (a vivid, theatrical wash)

The tint is applied by adding fixed UV offsets to the fill region's chrominance channels. It does not affect the revealed (inside) region of the iris.

:::tip
Combine a low **Fill Brt** with a strong **Tint Color** to create the look of hand-tinted nitrate film prints, where dark scenes were bathed in blue or amber wash to convey mood.
:::

---

### Switch 7 — Mode

| Property | Value |
|----------|-------|
| Off | Iris |
| On | Title |
| Default | Iris |

**Mode** selects between the two operating modes. Set to **Iris**, the program generates a geometric aperture mask with controllable shape, position, and feathered edge. Set to **Title**, the program draws a decorative double-rectangle border frame over the video (the ornamental surround of a silent film intertitle card.)

In Title mode, the **Shape**, **Shape Alt**, **Center X**, and **Center Y** controls change meaning or have no effect. **Size** controls the margin width instead of the iris radius. **Softness** has no visible effect on the hard-edged border lines.

---

### Switch 8 — Shape

| Property | Value |
|----------|-------|
| Off | Circle |
| On | Diamond |
| Default | Circle |

**Shape** selects between two primary iris shapes when in Iris mode. Set to **Circle**, the aperture is a circular (octagonal approximation) shape computed from a fast Euclidean distance estimate. Set to **Diamond**, the aperture is a diamond (rhombus) shape computed from the ***L1 norm***: the sum of horizontal and vertical distances, also called the Manhattan distance.

The Shape and **Shape Alt** toggles combine into a two-bit selector that chooses among four distinct shapes: circle, rectangle, diamond, and keyhole.

---

### Switch 9 — Shape Alt

| Property | Value |
|----------|-------|
| Off | Rect |
| On | Keyhole |
| Default | Rect |

**Shape Alt** selects between two alternate iris shapes when in Iris mode. Set to **Rect**, the aperture is a rectangle with a 4:3-ish aspect ratio (three-quarters the width for the height). Set to **Keyhole**, the aperture is a keyhole figure formed by the union of two overlapping circles offset vertically: one shifted up and one shifted down by one quarter of the iris radius.

In Title mode, Shape Alt controls whether corner ornaments appear on the inner border rectangle. Set to **Rect**, no ornaments are drawn. Set to **Keyhole**, small 8×8 pixel blocks appear at each of the four corners of the inner rectangle, adding a decorative flourish.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Normal |
| On | Invert |
| Default | Normal |

**Invert** reverses the mask polarity. In **Normal** mode, the inside of the iris reveals the source video and the outside is masked. In **Invert** mode, the outside reveals the source and the inside is masked (dimmed and tinted). This effectively turns the iris into a spotlight-negative: the subject is hidden and the surroundings are shown.

Invert is applied after the alpha ramp is computed, so the Softness feather is also reversed (the gradient fades in the opposite direction.)

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input video directly to the output, bypassing all iris and title card processing. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

:::note Toggle Group Notes

The **Shape** and **Shape Alt** toggles form a combined two-bit shape selector. Together they choose one of four iris shapes:

| Shape | Shape Alt | Result |
|-------|-----------|--------|
| Circle | Rect | **Circle** — octagonal approximation of Euclidean distance |
| Circle | Keyhole | **Keyhole** — union of two vertically offset circles |
| Diamond | Rect | **Diamond** — L1 norm rhombus |
| Diamond | Keyhole | **Rectangle** — axis-aligned box with 4:3 aspect |

Note that the rectangle is selected by the seemingly unintuitive combination of Diamond + Keyhole. This is because the VHDL shape selector encodes Circle/Keyhole as shapes "00"/"11" and Diamond/Rectangle as "10"/"01": maximizing visual contrast between adjacent toggle positions.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (processed) output. At 0%, the output is entirely dry: identical to Bypass. At 100%, the output is the full iris or title card effect. Intermediate values blend the two, creating a ghostly overlay of the mask on the source.

The mix is implemented with three parallel ***interpolator*** instances (one each for Y, U, and V), which crossfade between the delayed dry signal and the composited wet signal.

---

## Background

### Silent cinema and the mechanical iris

The iris was one of the first special effects in the history of cinema. Early cameras like the Pathé studio camera (circa 1905) featured a metal iris diaphragm mounted in front of the lens: the same mechanism that controls aperture in a still camera, but operated manually during filming. The cinematographer would slowly crank the iris closed to end a scene (***iris-out***) or open it to begin the next (***iris-in***). D.W. Griffith and his cameraman Billy Bitzer refined the technique into a narrative tool, using partial iris closures to draw the viewer's attention to a single character or detail within a wider scene.

The iris wasn't always circular. Filmmakers experimented with custom masks cut from sheet metal or cardboard: keyholes for eavesdropping shots, telescopes for distant views, binoculars for military scenes. These shaped masks told the audience whose eyes they were looking through.

### Signed distance fields

Bijou computes its iris shapes using ***signed distance fields*** (SDFs). For every pixel on screen, the program calculates that pixel's distance from the nearest point on the shape's boundary. Pixels inside the shape get a negative distance; pixels outside get a positive distance; pixels exactly on the edge get zero. The Softness control then maps this signed distance into an alpha value, creating the feathered transition.

The circle shape uses a fast approximation of Euclidean distance: `max(|dx|, |dy|) + min(|dx|, |dy|) / 2`. This produces an octagonal shape rather than a true circle, but the error is small and the computation requires no multiplier (just comparisons, additions, and shifts.)

The diamond uses the L1 (Manhattan) norm: `|dx| + |dy|`. The rectangle uses the Chebyshev-like `max(|dx| - w, |dy| - h)`. The keyhole takes the minimum distance of two vertically offset circles.

### Intertitle cards and decorative borders

Before the advent of synchronized sound in the late 1920s, dialogue and narration in films were conveyed through ***intertitle cards***: static frames of text inserted between scenes. These were not plain text on black, but ornamental compositions: the text was surrounded by decorative borders, filigree, and themed illustrations that matched the tone of the film.

Fritz Lang's *Metropolis* (1927) featured bold Art Deco borders. Georges Méliès's fantasies used whimsical illustrated frames. Bijou's Title mode generates the geometric essentials of these frames: the nested rectangles and corner blocks: providing the visual container that the artist can fill with externally composited text or imagery.


---

## Signal Flow

### Signal Flow Notes

Two key architectural details stand out in the signal path:

1. **Shape selection is combinatorial.** The Shape and Shape Alt toggles are combined into a two-bit selector *before* the SDF computation, so there is no mode-switch latency: the shape changes instantaneously, within a single clock cycle.

2. **The fill region is computed in parallel with the alpha ramp.** Stage 3 simultaneously computes the mask alpha (from the SDF distance and Softness) and the fill pixel values (brightness-scaled, tint-shifted video). This means the fill is always ready when the compositor needs it in Stage 4: there's no serial dependency between the alpha and fill paths.

:::note
The SDF for the circle shape uses a fast integer approximation (the octagonal norm), not a true Euclidean distance. This avoids the need for a hardware multiplier in the distance computation but produces a slightly faceted edge at very large iris sizes. The Softness control hides the faceting by blurring the transition zone.
:::


---

## Exercises

These exercises progress from a basic iris vignette to a full title card composition. Each one introduces more controls and reveals how the processing stages interact.
### Exercise 1: Classic Iris Transition

![Classic Iris Transition result](/img/instruments/videomancer/bijou/bijou_ex1_s1.png)
*Classic Iris Transition — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic silent cinema iris-in effect: a circular window opens over a dimmed, sepia-toned background.

#### Key Concepts

- The iris is a geometric mask with controllable position and size
- Softness controls the feathered edge width
- Fill Brt and Tint Color dress the masked region

#### Video Source

A live camera feed or recorded footage with a recognizable subject: a face, a performer, or an object on a contrasting background.

#### Steps

1. **Close the iris**: Turn **Size** (Knob 1) counterclockwise until a small circle appears in the center of the frame. Everything outside the circle is black.
2. **Soften the edge**: Turn **Softness** (Knob 4) clockwise to about 30%. The hard circle edge dissolves into a soft vignette glow.
3. **Add fill**: Increase **Fill Brt** (Knob 5) to about 20%. The masked region brightens, revealing a dim ghost of the source image behind the iris.
4. **Tint the fill**: Turn **Tint Color** (Knob 6) to the first quarter (sepia range). The fill takes on a warm amber tone (the look of aged nitrate film.)
5. **Open the iris**: Slowly sweep Size clockwise to simulate a classic iris-in transition. The aperture widens to reveal the full frame.

#### Settings

| Control | Value |
|---------|-------|
| Size | ~30% |
| Center X | 50% |
| Center Y | 50% |
| Softness | ~30% |
| Fill Brt | ~20% |
| Tint Color | ~12% |
| Mode | Iris |
| Shape | Circle |
| Shape Alt | Rect |
| Invert | Normal |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Keyhole Point-of-View

![Keyhole Point-of-View result](/img/instruments/videomancer/bijou/bijou_ex2_s1.png)
*Keyhole Point-of-View — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A keyhole-shaped mask that frames the video as if peering through a lock, with a blue-tinted surround.

#### Key Concepts

- The keyhole shape simulates a point-of-view through a real keyhole
- Invert reverses the mask polarity
- Shape and Shape Alt combine into a four-shape selector

#### Video Source

Footage of an interior scene: a doorway, a room, or a stage. High contrast between subject and background works best.

#### Steps

1. **Select keyhole**: Set **Shape** (Switch 8) to **Circle** and **Shape Alt** (Switch 9) to **Keyhole**. The iris changes from a circle to a vertically elongated figure-eight keyhole shape.
2. **Size the keyhole**: Adjust **Size** (Knob 1) until the keyhole frames your subject comfortably (roughly 60%.)
3. **Position it**: Use **Center X** (Knob 2) and **Center Y** (Knob 3) to move the keyhole over your subject.
4. **Hard edge**: Set **Softness** (Knob 4) to 0%. The keyhole becomes a crisp, mechanical cutout.
5. **Blue surround**: Set **Fill Brt** (Knob 5) to about 10% and **Tint Color** (Knob 6) to the third quarter (blue range, about 65%). The area outside the keyhole takes on a dark blue wash (moonlight through an old door.)
6. **Try inversion**: Flip **Invert** (Switch 10) to see the negative: the keyhole interior dims and the surround reveals the full image.

#### Settings

| Control | Value |
|---------|-------|
| Size | ~60% |
| Center X | 50% |
| Center Y | 50% |
| Softness | 0% |
| Fill Brt | ~10% |
| Tint Color | ~65% |
| Mode | Iris |
| Shape | Circle |
| Shape Alt | Keyhole |
| Invert | Normal |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Silent Film Title Card

![Silent Film Title Card result](/img/instruments/videomancer/bijou/bijou_ex3_s1.png)
*Silent Film Title Card — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A decorative intertitle frame with corner ornaments and sepia-tinted fill (the ornamental surround for a silent film text card.)

#### Key Concepts

- Title mode generates decorative border frames
- Size controls the margin width
- Shape Alt enables corner ornaments
- The fill zone between borders is independently tinted

#### Video Source

A simple, low-contrast image or a solid color field. In a live performance, this could be a blank or static input that serves as the background for externally composited text.

#### Steps

1. **Enter Title mode**: Flip **Mode** (Switch 7) to **Title**. The iris vanishes and a rectangular border frame appears.
2. **Adjust margins**: Turn **Size** (Knob 1) to about 50%. The outer and inner rectangles move inward, creating wider margins between the border and the edge of the frame.
3. **Add corner ornaments**: Set **Shape Alt** (Switch 9) to **Keyhole**. Small 8×8 pixel blocks appear at each corner of the inner rectangle.
4. **Tint the borders**: Set **Tint Color** (Knob 6) to the first quarter (sepia). The border lines adopt a warm amber color. Set **Fill Brt** (Knob 5) to about 30% so the zone between the two rectangles shows dimmed, tinted video.
5. **Experiment with colors**: Sweep Tint Color through the full range to preview green, blue, and magenta border themes. Find the one that best matches the mood of your title.

#### Settings

| Control | Value |
|---------|-------|
| Size | ~50% |
| Center X | 50% |
| Center Y | 50% |
| Softness | ~12% |
| Fill Brt | ~30% |
| Tint Color | ~12% |
| Mode | Title |
| Shape | Circle |
| Shape Alt | Keyhole |
| Invert | Normal |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Alpha Blending**: Combining two images using a per-pixel opacity value (alpha), where 0 means fully transparent and 1023 means fully opaque.

- **Intertitle**: A static text card inserted between scenes in a silent film, used to convey dialogue, narration, or chapter headings.

- **Iris**: A variable-aperture mask that reveals or conceals portions of a film frame; originally a mechanical device mounted on the camera lens.

- **L1 Norm**: The sum of the absolute differences along each axis, also called the Manhattan distance. Produces a diamond-shaped equidistant contour.

- **Nitrate Film**: Early photographic film stock made from cellulose nitrate, known for its luminous image quality and warm amber aging characteristics.

- **Signed Distance Field (SDF)**: A mathematical representation where each point stores the signed distance to the nearest boundary (negative inside, positive outside, zero on the edge.)

- **Vignette**: A gradual darkening or fading at the edges of an image, originally caused by optical limitations in lenses.

---
