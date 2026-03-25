---
draft: true
sidebar_position: 169
slug: /instruments/videomancer/lenticular
title: "Lenticular"
image: /img/instruments/videomancer/lenticular/lenticular_hero_s1.png
description: "Lenticular prints are those plastic-ridged cards that seem to shift or animate when you tilt them."
---

![Lenticular hero image](/img/instruments/videomancer/lenticular/lenticular_hero_s1.png)
*Lenticular splitting live video into interlaced vertical stripes that alternate between shifted and unshifted views, producing a shimmering pseudo-3D parallax effect.*

---

## Overview

Lenticular is a video processing program that divides the screen into alternating vertical (or horizontal) stripes. Every other stripe shows a horizontally shifted copy of the image, while the remaining stripes pass the original pixels through. The result is an interleaved parallax effect that recalls the shimmer of a ***lenticular print***: those ridged plastic cards that change images as you tilt them. At small stripe widths and moderate shift distances, the image appears to split into two slightly offset layers, creating an uncanny illusion of depth on a flat screen.

The program's second personality is ***wiggle mode***, where the alternation happens across time instead of space. Rather than interleaving two views side by side, Lenticular flips the entire frame between the original and shifted image on every other video frame, producing a rapid back-and-forth animation. This is the digital equivalent of physically tilting a lenticular card to make it "wiggle."

:::tip
Try feeding Lenticular a high-contrast source and setting **Stripe W** to a narrow width. The fine interleaving creates a moiré shimmer that looks different from every viewing angle (just like a holographic sticker.)
:::

### What's In a Name?

A ***lenticular lens*** is an array of tiny cylindrical magnifying lenses molded into a sheet of plastic. When an image is printed in interlaced strips behind the lens, each strip is magnified to fill the field of view: but only from a specific angle. Tilt the card, and a different set of strips snaps into focus, revealing a different image. Novelty postcards, flip-sticker baseball cards, and early "3D" magazine covers all use lenticular printing. Lenticular recreates this optical trick electronically, splitting video into alternating stripe views and animating between them.

---

## Quick Start

1. Load **Lenticular** and feed it a camera or any video source. Set **Stripe W** (Knob 1) to about 40%. You'll see the image divided into vertical stripes of alternating content.
2. Slowly increase **Shift** (Knob 2). Alternate stripes now show pixels from earlier in the scan line (the image appears to peel apart into two offset layers.)
3. Flip the **Direction** toggle (Switch 8) from **Vert** to **Radial**. Instead of spatial stripes, the entire image now flickers between the two views on alternating frames (a rapid wiggle animation.)
4. Flip **Direction** back to **Vert** and narrow the **Stripe W** to about 15%. The fine interleaving produces a dense, shimmering parallax texture.

---

## Parameters

![Videomancer front panel with Lenticular loaded](/img/instruments/videomancer/lenticular/lenticular_control_panel.png)
*Videomancer's front panel with Lenticular active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Stripe W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Stripe W** controls the width of each alternating stripe. The stripe period is quantized into five discrete levels: at the lowest knob positions the stripes are 4 pixels wide, stepping through 8, 16, and 32 pixels, up to 64 pixels wide at the highest setting. This control determines how finely the image is sliced. Very narrow stripes (4 px) produce a dense, almost holographic shimmer where the two views blend perceptually. Wide stripes (64 px) create broad, clearly separated bands (the shifted and unshifted regions are individually legible.)

:::note
Because the stripe width is quantized, turning the knob does not produce a smooth sweep. Instead, the pattern snaps between five discrete widths. Listen for the moment each step clicks into place.
:::

---

### Knob 2 — Shift

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Shift** sets the horizontal pixel offset between the two interleaved views. Internally, a 64-sample ***shift register*** delays the incoming pixels. This knob selects the tap point, from 0 (no delay: both stripe views are identical) up to 63 pixels of horizontal displacement. At low values, the two views are nearly the same and the stripes are subtle. At high values, the alternate stripes show content that appeared many pixels earlier on the scan line, creating a strong parallax displacement. Edges and high-contrast boundaries become the most visually dramatic areas, because the horizontal offset makes them visibly double.

:::tip
Combine a moderate **Shift** with a narrow **Stripe W** for a "lenticular postcard" look. Widen the stripes and push Shift to maximum for an aggressive image-doubling glitch.
:::

---

### Knob 3 — Views

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Views** is reserved for a future firmware update. Adjusting this knob has no visible effect on the output image in the current version.

---

### Knob 4 — Angle

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Angle** enables a vertical softening effect on the alternate stripes. When the knob is set above its minimum position, the Y (luminance) channel on every alternate stripe is averaged with the luminance of the previous scan line, read from a ***line buffer***. This creates a subtle vertical smear on the shifted stripes while leaving the primary stripes sharp, adding an additional dimension of visual separation between the two interleaved views.

:::note
The blending engages as a threshold: any position above minimum activates the vertical averaging at full strength. The knob does not provide a graduated blend: it functions as an enable switch with a small dead zone at the bottom of its travel.
:::

---

### Knob 5 — Sharp

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Sharp** controls the luminance intensity of the processed output. Below the midpoint (50%), the processed image is attenuated: darkened proportionally as you turn the knob counterclockwise. At the lowest setting, the processed stripes are fully black. Above 50%, the luminance passes through at full strength with no attenuation. Use lower **Sharp** values to reduce the visual impact of the interleaving effect, fading the striped image toward darkness while the **Mix** fader blends toward the dry signal.

---

### Knob 6 — Depth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Depth** is reserved for a future firmware update. Adjusting this knob has no visible effect on the output image in the current version.

---

### Switch 7 — Mode

| Property | Value |
|----------|-------|
| Off | Flip |
| On | Anim |
| Default | Flip |

**Mode** selects the stripe orientation. In the **Flip** position, stripes run vertically: alternating columns of pixels. In the **Anim** position, stripes run horizontally: alternating rows of pixels. Vertical stripes produce the classic lenticular interleave along the horizontal axis. Horizontal stripes create a different visual character: the parallax displacement shifts content between adjacent scan lines rather than adjacent columns, producing a layered, venetian-blind effect.

---

### Switch 8 — Direction

| Property | Value |
|----------|-------|
| Off | Vert |
| On | Radial |
| Default | Vert |

**Direction** selects between spatial interleaving and temporal wiggle. In the **Vert** position, alternation is spatial: even-numbered stripes show the original pixels, odd-numbered stripes show the shifted view, and both are visible simultaneously on every frame. In the **Radial** position, alternation is temporal: the entire frame flips between the original view and the shifted view on every other video frame, producing a rapid wiggle animation. This is the "flip card" mode (the image appears to jitter back and forth.)

:::warning
At standard frame rates, the temporal wiggle can produce a rapid flicker. Viewers sensitive to flashing images should approach this mode with care.
:::

---

### Switch 9 — Source

| Property | Value |
|----------|-------|
| Off | Luma |
| On | Edge |
| Default | Luma |

**Source** flips the assignment of which stripes show the original view and which show the shifted view. In the **Luma** position, the default assignment applies. In the **Edge** position, the assignment is inverted: stripes that previously showed the original now show the shifted view, and vice versa. This effectively mirrors the parallax direction, swapping left-eye and right-eye perspectives.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** is reserved for a future firmware update. Toggling this switch has no visible effect on the output image in the current version.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Lenticular processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the striped result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (processed) output. At 0%, only the original signal passes through. At 100%, only the processed lenticular output is visible. Intermediate values blend the two together smoothly. Because Lenticular defaults to 100% mix, you hear the full effect immediately on load. Pull the fader down to soften the stripe interleaving into a subtle shimmer.

---

## Background

### Lenticular printing

***Lenticular printing*** is a technique developed in the early twentieth century that uses an array of tiny cylindrical lenses: called ***lenticules***: bonded to the surface of a printed sheet. The image beneath the lens array is printed as a series of interlaced vertical strips, each strip visible only from a narrow range of viewing angles. As the viewer tilts the print, different strips snap into focus, creating the illusion of motion, depth, or image transformation. The technique reached mass popularity in the 1960s through novelty postcards, cereal-box prizes, and magazine covers. Today it's used in commercial packaging, security labels, and art prints.

Lenticular exploits the same underlying principle digitally. Instead of physical lenses selecting which strips you see, the program selects which pixels belong to the "original" view and which belong to the "shifted" view, interleaving them across the screen in alternating stripes.

### Shift registers and parallax

In hardware, a ***shift register*** is a chain of memory cells arranged so that data moves from one cell to the next on every clock pulse. Lenticular uses a 64-stage shift register to store the most recent 64 pixels of Y, U, and V video data as they stream across each scan line. By reading from a selectable tap along this chain, the program retrieves a pixel that appeared some number of clock cycles earlier: effectively a horizontally displaced copy of the image. The **Shift** knob selects which tap to read.

This horizontal displacement is what creates the illusion of depth. In real stereoscopic vision, each eye sees the world from a slightly different horizontal position. Lenticular approximates this by presenting two horizontally offset views of the same scene, interleaved through the stripe pattern.

### Wiggle stereoscopy

***Wiggle stereoscopy*** is a technique where a camera captures two photographs of the same scene from slightly different positions, and the two images are played back in rapid alternation. The brain interprets the oscillating horizontal shift as depth: objects closer to the camera appear to move more than distant objects. Animated GIF "wigglegrams" are a popular modern incarnation of this century-old technique. Lenticular's temporal wiggle mode (the **Radial** position of the **Direction** toggle) implements this principle in real time, flipping the entire frame between the original and shifted view on alternating video frames.


---

## Signal Flow

### Signal Flow Notes

Two primary signal paths run in parallel through the pipeline:

1. **Shift register path**: Every incoming pixel is written into a 64-deep FIFO. On alternate stripes, the program reads a tap from this register: effectively looking "backward" along the scan line by 0 to 63 pixels. This creates the horizontal parallax displacement. On primary stripes, the current pixel passes through unchanged.

2. **Line buffer path**: The Y channel is also written into a one-line-deep buffer. When **Angle** is enabled, alternate stripes blend the shift-register Y with the previous line's Y, softening the shifted view vertically.

:::tip
**Stripe selection is the heart of the effect.** The bit tested in `h_count` (or `v_count` in horizontal mode) determines whether each pixel falls on a primary or alternate stripe. The **Stripe W** knob selects which bit to test, quantizing the stripe period to powers of two.
:::


---

## Exercises

These exercises progress from basic stripe interleaving to animated wiggle effects, building familiarity with Lenticular's spatial and temporal modes.
### Exercise 1: Classic Lenticular Card

![Classic Lenticular Card result](/img/instruments/videomancer/lenticular/lenticular_ex1_s1.png)
*Classic Lenticular Card — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic lenticular postcard effect: the image appears to shimmer with depth as if viewed through a ridged plastic overlay.

#### Key Concepts

- Stripe interleaving creates two parallel views of the same scene
- The shift register provides horizontal displacement
- Narrow stripes merge perceptually; wide stripes remain distinct

#### Video Source

A live camera feed pointed at a scene with objects at different distances, or any video with recognizable subjects and moderate contrast.

#### Steps

1. Set **Stripe W** (Knob 1) to about 25%. The image is divided into narrow vertical stripes.
2. Slowly increase **Shift** (Knob 2) from 0% to about 40%. You'll see the alternate stripes slide sideways: the image splits into two offset copies interleaved together.
3. Step through the five stripe widths by sweeping **Stripe W** slowly from minimum to maximum. Notice each discrete jump. Settle on a narrow width (around 15–25%) for the finest lenticular shimmer.
4. Enable **Angle** (Knob 4) by turning it above minimum. The alternate stripes soften vertically, adding a subtle blur that distinguishes them from the sharp primary stripes.
5. Toggle **Source** (Switch 9) to **Edge**. The parallax direction reverses (the "near" and "far" layers swap.)

#### Settings

| Control | Value |
|---------|-------|
| Stripe W | ~20% |
| Shift | ~40% |
| Views | 50% |
| Angle | ~60% |
| Sharp | 75% |
| Depth | 50% |
| Mode | Flip |
| Direction | Vert |
| Source | Luma |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Wiggle Stereoscopy

![Wiggle Stereoscopy result](/img/instruments/videomancer/lenticular/lenticular_ex2_s1.png)
*Wiggle Stereoscopy — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A rapid-fire wiggle animation where the image jitters back and forth between two horizontally offset views, creating an impression of depth.

#### Key Concepts

- Temporal alternation creates wiggle stereoscopy
- Frame-rate flickering simulates depth perception
- Shift distance controls the strength of the 3D illusion

#### Video Source

A static camera shot of a scene with clear foreground and background elements: a tabletop with objects, a hallway, or any scene with depth.

#### Steps

1. Set **Direction** (Switch 8) to **Radial** to engage temporal wiggle mode.
2. Set **Shift** (Knob 2) to about 20%. The entire frame alternates between the original and shifted view. You should see a gentle oscillation.
3. Increase **Shift** gradually. The oscillation grows more dramatic. Find the sweet spot where the depth illusion is strongest without becoming disorienting.
4. Try **Mode** (Switch 7) in both **Flip** and **Anim** positions. In wiggle mode, the orientation toggle has no visible effect because the alternation is temporal, not spatial (the entire frame switches.)
5. Pull **Mix** (Fader 12) down to about 60%. The wiggle effect softens as the dry signal bleeds through, creating a ghostly double-exposure oscillation.

#### Settings

| Control | Value |
|---------|-------|
| Stripe W | 50% |
| Shift | ~20% |
| Views | 50% |
| Angle | 0% |
| Sharp | 75% |
| Depth | 50% |
| Mode | Flip |
| Direction | Radial |
| Source | Luma |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Venetian Blind Layers

![Venetian Blind Layers result](/img/instruments/videomancer/lenticular/lenticular_ex3_s1.png)
*Venetian Blind Layers — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dramatic venetian-blind effect where the image is sliced into wide horizontal bands, alternating between the original and a shifted copy.

#### Key Concepts

- Horizontal stripes create a venetian-blind interleave
- Wide stripes reveal the two views as distinct layers
- Combining orientation and shift produces a layered composite

#### Video Source

Video footage with strong horizontal lines or layered compositions: cityscapes, bookshelves, a window with blinds, or any subject with interesting horizontal structure.

#### Steps

1. Set **Mode** (Switch 7) to **Anim** for horizontal stripes.
2. Set **Stripe W** (Knob 1) between 60–80% for wide, clearly visible horizontal bands.
3. Increase **Shift** (Knob 2) to about 50%. The alternate bands now show a noticeably displaced copy of the image. The result resembles looking through venetian blinds at a scene that has shifted sideways.
4. Enable **Angle** (Knob 4) to add the vertical line-buffer softening. On horizontal stripes, this blurs the alternate bands slightly, making them look like they belong to a different focal plane.
5. Lower **Sharp** (Knob 5) below 50%. The processed output darkens: the interleaved bands fade toward black while the primary bands remain at full brightness, creating a dramatic contrast between the two views.
6. Toggle **Source** (Switch 9) to **Edge** and compare. The assignment of which bands are "primary" and "shifted" swaps.

#### Settings

| Control | Value |
|---------|-------|
| Stripe W | ~70% |
| Shift | ~50% |
| Views | 50% |
| Angle | ~60% |
| Sharp | ~35% |
| Depth | 50% |
| Mode | Anim |
| Direction | Vert |
| Source | Luma |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Interleaving**: Arranging two or more signals in alternating segments so they occupy the same physical space; in Lenticular, alternating stripes carry different views of the same image.

- **Lenticular Lens**: An array of tiny cylindrical lenses that direct light from interlaced image strips to different viewing angles, creating the illusion of motion or depth.

- **Line Buffer**: A block RAM that stores one full scan line of pixel data, allowing the program to read the previous line's luminance for vertical blending.

- **Parallax**: The apparent displacement of an object caused by a change in the observer's point of view; used in stereoscopy to create depth perception from flat images.

- **Shift Register**: A chain of memory cells where data advances one position per clock cycle, providing a tapped delay line for horizontal pixel displacement.

- **Stereoscopy**: Any technique that creates the illusion of three-dimensional depth from two-dimensional images, typically by presenting slightly different views to each eye.

- **Stripe Period**: The number of pixels (or lines) in one full cycle of the alternating pattern (one primary stripe plus one alternate stripe.)

- **Wiggle Stereoscopy**: A depth illusion technique where two horizontally offset images are displayed in rapid alternation, causing the brain to interpret the oscillation as depth.

---
