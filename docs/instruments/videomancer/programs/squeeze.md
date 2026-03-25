---
draft: true
sidebar_position: 282
slug: /instruments/videomancer/squeeze
title: "Squeeze"
image: /img/instruments/videomancer/squeeze/squeeze_hero_s1.png
description: "In the era of analogue broadcast television, a dedicated hardware box called a DVE — Digital Video Effects unit — sat between the camera switcher and the transmitter."
---

![Squeeze hero image](/img/instruments/videomancer/squeeze/squeeze_hero_s1.png)
*Squeeze confining a live video feed into a bright-bordered inset rectangle with a dimmed background, creating a classic picture-in-picture composition.*

---

## Overview

**Squeeze** is a DVE-style ***squeeze-back*** effect that confines your video inside a smaller inset rectangle. You control the size, position, border, and background fill: everything you need for picture-in-picture compositions, framed insets, or dramatic reveals. The area outside the inset can be solid black, a user-controlled gray level, or a dimmed version of the incoming video, giving you flexible background options.

The effect works by classifying every pixel as belonging to one of four regions: the ***inset*** (where the video plays), the ***border*** (a bright neutral frame), the ***drop shadow*** (a dark offset duplicate of the border for a three-dimensional look), or the ***background*** (everything else). Because the iCE40 FPGA has no line buffer, Squeeze doesn't resample or interpolate: it crops the visible video to the inset window, which gives the effect a hard-edged, direct character reminiscent of vintage broadcast DVE units.

:::note
Because Squeeze windows rather than rescales, what you see inside the inset is the original video at those pixel positions: not a miniaturized copy of the full frame. Shrinking the inset reveals less of the image, like a closing aperture.
:::

### What's In a Name?

In broadcast television, a ***squeeze-back*** is the technique of compressing on-screen content into a smaller rectangle to make room for lower thirds, credits, or a second video feed. Videomancer's **Squeeze** captures that production aesthetic: the tight frame, the clean border, and the empty surround: and puts it under knob control for live performance.

---

## Quick Start

1. Feed a video source into Videomancer and load **Squeeze**. With default settings, you'll see most of the frame visible inside a bordered inset with a dark background beneath it.
2. Turn **Scale** (Knob 1) counter-clockwise. The inset rectangle shrinks, revealing more background. The video inside it becomes a smaller cropped window.
3. Sweep **Pos X** (Knob 2) left and right. The inset slides horizontally across the frame. Then sweep **Pos Y** (Knob 3) to move it vertically. You can park the inset in any corner, edge, or center position.
4. Toggle **Bg Mode** (Switch 8) to **Dim Vid**. The background changes from solid black to a dimmed version of the input: the inset now floats over a ghostly copy of the original footage.

---

## Parameters

![Videomancer front panel with Squeeze loaded](/img/instruments/videomancer/squeeze/squeeze_control_panel.png)
*Videomancer's front panel with Squeeze active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Scale

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Scale** sets the size of the inset rectangle as a proportion of the full frame. Fully clockwise, the inset fills the entire screen and the border sits at the edges: the effect is invisible. As you turn Scale counter-clockwise, the inset shrinks and more background is revealed. At the minimum, the inset disappears entirely, leaving only background, border, and shadow.

Scale affects both width and height simultaneously. At moderate settings, Squeeze creates a classic picture-in-picture window. At very low settings, the inset becomes a thin sliver or vanishes altogether.

---

### Knob 2 — Pos X

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Pos X** controls the horizontal position of the inset within the frame. At the center detent, the inset is centered horizontally. Turning counter-clockwise pushes the inset toward the left edge; clockwise pushes it toward the right. The available travel range depends on the current Scale: a small inset can be positioned anywhere across the frame, while a large inset has less room to move.

---

### Knob 3 — Pos Y

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Pos Y** controls the vertical position of the inset within the frame. Behavior mirrors Pos X along the vertical axis. Counter-clockwise parks the inset near the top of the frame; clockwise pushes it toward the bottom. Combined with **Pos X**, you can place the inset in any of the standard broadcast positions: upper-left, lower-right, dead center, or anywhere in between.

---

### Knob 4 — Border W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |

**Border W** sets the width of the border frame that surrounds the inset rectangle. At zero, no border is visible even if the Border toggle is enabled: the inset edge cuts directly to the background. As you increase Border W, a neutral-colored frame grows outward from the inset boundary. The border extends up to about 32 pixels wide at maximum, creating a thick picture frame.

:::tip
Even at maximum width, the border is drawn in pixels rather than percentage of screen, so it looks proportionally thinner around a large inset and thicker around a small one.
:::

---

### Knob 5 — Border Br

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Border Br** controls the brightness of the border ring. At zero, the border is black: invisible against a black background, but visible as a dark frame against dimmed video. At maximum, the border is peak white. Intermediate values produce gray borders. The border is always achromatic (neutral U and V), so it appears as a clean, colorless frame regardless of the brightness setting.

---

### Knob 6 — Bg Level

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 6% |

**Bg Level** controls the brightness of the background region outside the inset and border. When **Bg Mode** is set to **Black**, it directly sets the background luminance: zero is true black, maximum is peak white. When Bg Mode is set to **Dim Vid**, Bg Level acts as a multiplier on the incoming video: zero produces black, maximum passes the background video at full brightness, and intermediate values create a dimmed ghost of the original footage.

:::note
Setting Bg Level to maximum with Bg Mode on Dim Vid effectively passes the full video behind the inset, turning Squeeze into a border-overlay tool rather than a picture-in-picture effect.
:::

---

### Switch 7 — Aspect

| Property | Value |
|----------|-------|
| Off | Free |
| On | Lock |
| Default | Lock |

**Aspect** selects between free and locked aspect ratios for the inset rectangle. In the current implementation, this toggle is mapped but reserved for future use: both positions produce identical behavior. The inset always maintains the frame's native proportions.

---

### Switch 8 — Bg Mode

| Property | Value |
|----------|-------|
| Off | Black |
| On | Dim Vid |
| Default | Black |

**Bg Mode** selects the background fill behind the inset. In the **Black** position, the background is a solid neutral tone controlled by **Bg Level**: pure black at zero, gray or white at higher values. In the **Dim Vid** position, the background shows the original video multiplied by Bg Level, creating a dimmed or ghosted version of the input behind the inset window.

:::tip
Dim Vid mode is powerful for live performance. At low Bg Level values, the audience sees a faint image in the surround that contextualizes the cropped inset. At high values, the border and shadow become the primary visual elements floating over a nearly full-brightness background.
:::

---

### Switch 9 — Border

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Border** enables or disables the bright frame around the inset rectangle. When set to **Off**, the inset edge cuts directly to the background (or shadow, if enabled) with no visible frame: the transition from video to background is a hard pixel boundary. When set to **On**, the border ring appears at the width and brightness set by **Border W** and **Border Br**.

---

### Switch 10 — Shadow

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Shadow** enables or disables the drop shadow behind the inset. The shadow is a dark rectangle offset a few pixels down and to the right of the border, giving the inset a three-dimensional floating appearance. Shadow renders at a fixed low brightness (approximately 3% of full scale) with neutral color. When the border is also enabled, the shadow appears behind it, creating a layered look: inset → border → shadow → background.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Squeeze processing. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the composed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry input signal and the processed Squeeze output. At zero, only the original unprocessed video is visible. At maximum, the full Squeeze composition is shown. Intermediate positions blend the two using a linear interpolator applied independently to Y, U, and V channels.

:::tip
Mix is useful for subtle compositing. At around 50%, the inset border and background become translucent, creating a ghostly overlay effect where the original video bleeds through the composition.
:::

---

## Background

### Picture-in-Picture and the DVE

The ***digital video effects*** (DVE) unit is a piece of broadcast equipment that became iconic in the 1980s and 1990s. DVEs could shrink, position, rotate, and transition live video in real time: capabilities that were revolutionary when television was transitioning from analog switches to digital compositing. The ***squeeze-back*** was one of the most frequently used DVE moves: shrinking the outgoing shot into a corner while the incoming shot fills the frame. News broadcasts still use this framing today to show a reporter and a remote subject simultaneously.

Squeeze brings this production technique to Videomancer's analog-digital hybrid world. Rather than full-resolution resampling, it uses boundary comparison to window the input video, producing the hard-edged crop and neutral border that defined early DVE aesthetics.

### Region Classification

At the heart of Squeeze is a ***region classifier***: a pixel-by-pixel comparator that checks every incoming pixel's position against four nested rectangles. The innermost rectangle is the inset itself. Around it sits the border ring (if enabled). Behind the border sits the shadow (if enabled). Everything else is background. This classification happens in a single clock cycle, with priority given to the innermost region: a pixel that falls inside the inset is always shown as video, even if it also falls within the border or shadow boundaries.

### Drop Shadow Geometry

The drop shadow is a copy of the border rectangle offset down and to the right by a fixed number of pixels. Only the portions of the shadow that are ***not*** covered by the inset or border are visible: so the shadow appears as an L-shaped sliver on the bottom and right edges of the frame. The offset is built into the hardware at 4 pixels, and the shadow brightness is fixed near black. This simple geometry creates a convincing illusion of depth, making the inset appear to float above the background.


---

## Signal Flow

### Signal Flow Notes

The critical interaction in Squeeze is between the ***inset rectangle calculation*** and the ***region classifier***. Scale, Pos X, and Pos Y are combined to produce four boundary coordinates that define the inset rectangle in pixel space. Every pixel is then checked against those boundaries in priority order: inset first, then border, then shadow, then background. This priority means the inset always wins (a pixel can never be covered by a border or shadow.)

The background compositing path branches on the **Bg Mode** toggle. In Dim Vid mode, the background passes through the input video's U and V channels unchanged while scaling only the luminance by Bg Level. This preserves color in the dimmed background, preventing it from collapsing to monochrome at low brightness. In Black mode, both chroma channels are forced to neutral (512), producing a purely achromatic background.


---

## Exercises

These exercises explore Squeeze's framing and compositing capabilities, progressing from basic picture-in-picture to layered compositions.
### Exercise 1: Classic PiP Window

![Classic PiP Window result](/img/instruments/videomancer/squeeze/squeeze_ex1_s1.png)
*Classic PiP Window — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A traditional picture-in-picture composition with a bright-bordered inset floating in the lower-right corner over a dark background.

#### Key Concepts

- Scale and position define a cropped viewing window
- The border creates a visual frame that separates content from background
- Background mode changes the surround from solid to video-derived

#### Video Source

A camera feed or recorded footage with recognizable subjects: talking heads, landscapes, or anything with clear spatial composition.

#### Steps

1. Load **Squeeze** and set **Scale** (Knob 1) to roughly 50%. The image contracts to a rectangle about half the frame size.
2. Turn **Pos X** (Knob 2) clockwise to push the inset toward the right edge. Turn **Pos Y** (Knob 3) clockwise to push it toward the bottom. You now have a lower-right PiP window.
3. Confirm **Border** (Switch 9) is set to **On**. Adjust **Border W** (Knob 4) until you see a visible frame (a moderate setting works well.)
4. Set **Border Br** (Knob 5) to maximum for a bright white frame.
5. Ensure **Bg Mode** (Switch 8) is set to **Black** and **Bg Level** (Knob 6) is low. The surround is dark, making the bordered inset pop.

#### Settings

| Control | Value |
|---------|-------|
| Scale | ~50% |
| Pos X | ~80% |
| Pos Y | ~80% |
| Border W | ~30% |
| Border Br | 100% |
| Bg Level | ~5% |
| Aspect | Lock |
| Bg Mode | Black |
| Border | On |
| Shadow | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Floating Window with Drop Shadow

![Floating Window with Drop Shadow result](/img/instruments/videomancer/squeeze/squeeze_ex2_s1.png)
*Floating Window with Drop Shadow — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A medium-sized inset that appears to float above a ghostly copy of the original footage, with a drop shadow adding depth.

#### Key Concepts

- The drop shadow creates an illusion of depth
- Dimmed video backgrounds contextualize the inset
- Border brightness and shadow interact to define the visual hierarchy

#### Video Source

Footage with moderate contrast and varied spatial content: street scenes, architecture, or nature footage work well for showing the background relationship.

#### Steps

1. Set **Scale** (Knob 1) to roughly 60%. Center the inset using **Pos X** (Knob 2) and **Pos Y** (Knob 3) at their midpoints.
2. Enable **Shadow** (Switch 10). A dark L-shaped shadow appears below and to the right of the inset, giving it a floating appearance.
3. Switch **Bg Mode** (Switch 8) to **Dim Vid**. The background changes from solid black to a faded version of the input.
4. Adjust **Bg Level** (Knob 6) until the background is visible but clearly subordinate to the inset (roughly 20–30%.)
5. Set **Border Br** (Knob 5) to about 70% for a soft gray frame that complements the dimmed background.
6. Slowly sweep **Pos X** and **Pos Y** to slide the floating window around. The shadow follows, and the dimmed background shifts behind it.

#### Settings

| Control | Value |
|---------|-------|
| Scale | ~60% |
| Pos X | 50% |
| Pos Y | 50% |
| Border W | ~25% |
| Border Br | ~70% |
| Bg Level | ~25% |
| Aspect | Lock |
| Bg Mode | Dim Vid |
| Border | On |
| Shadow | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Animated Reveal

![Animated Reveal result](/img/instruments/videomancer/squeeze/squeeze_ex3_s1.png)
*Animated Reveal — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dynamic transition where the video starts full-frame and squeezes down into a corner, revealing the background fill beneath it (a classic broadcast squeeze-back move.)

#### Key Concepts

- Scale can be swept in real time for dramatic reveal transitions
- Mix creates translucent overlay effects
- Position and scale interact to produce broadcast-style squeeze-back moves

#### Video Source

Any visually interesting footage. High-contrast or colorful material makes the squeeze-back transition more dramatic.

#### Steps

1. Start with **Scale** (Knob 1) at maximum (fully clockwise). The image fills the entire frame: Squeeze is invisible.
2. Set **Pos X** (Knob 2) and **Pos Y** (Knob 3) to park the inset in the upper-left corner (both fully counter-clockwise).
3. Enable **Border** (Switch 9) and **Shadow** (Switch 10). Set **Border Br** (Knob 5) to maximum and **Border W** (Knob 4) to a moderate width.
4. Switch **Bg Mode** (Switch 8) to **Dim Vid** and set **Bg Level** (Knob 6) to about 15%.
5. Now slowly turn **Scale** counter-clockwise. The image squeezes down into the upper-left corner, the border appears, shadow emerges, and the dimmed background fills the surround (a live squeeze-back.)
6. Bring **Mix** (Fader 12) to about 60%. The composition becomes translucent, blending the squeeze-back with the original full-frame video.
7. Sweep **Scale** back to maximum for the reverse reveal.

#### Settings

| Control | Value |
|---------|-------|
| Scale | ~30% (end position) |
| Pos X | ~10% |
| Pos Y | ~10% |
| Border W | ~30% |
| Border Br | 100% |
| Bg Level | ~15% |
| Aspect | Lock |
| Bg Mode | Dim Vid |
| Border | On |
| Shadow | On |
| Bypass | Off |
| Mix | ~60% |

---
## Glossary

- **Crop**: Removing the outer portions of an image, reducing the visible area without changing pixel scale.

- **Drop Shadow**: A dark offset duplicate of a shape, creating an illusion of depth by simulating a cast shadow.

- **DVE**: Digital Video Effects; a class of broadcast equipment that manipulates live video in real time (scaling, positioning, rotating, and transitioning.)

- **Inset**: A smaller rectangle within the full frame that displays video content, surrounded by background or border.

- **Interpolator**: A circuit that blends between two values based on a mixing coefficient, used here for wet/dry crossfading.

- **Picture-in-Picture (PiP)**: A display mode where a secondary video feed appears in a small window overlaid on a primary feed.

- **Region Classification**: The process of determining which visual zone each pixel belongs to, based on its position relative to defined boundaries.

- **Squeeze-Back**: A broadcast transition where on-screen content shrinks into a smaller rectangle, typically to reveal a second feed or background.

---
