---
draft: true
sidebar_position: 121
slug: /instruments/videomancer/folio
title: "Folio"
image: /img/instruments/videomancer/folio/folio_hero_s1.png
description: "Folio simulates the page turn transition familiar from presentation software and e-book readers, implemented entirely in scanline-rate FPGA logic."
---

![Folio hero image](/img/instruments/videomancer/folio/folio_hero_s1.png)
*Folio simulating a 3D page turn, compressing live video into a narrowing strip while revealing a colored background beneath.*

---

## Overview

Folio is a real-time page turn transition for live video. It simulates a flat page anchored at one edge: the ***hinge***: that folds away from the viewer like a turning book page. As the page turns, the visible portion of the video compresses horizontally and darkens with perspective shading, revealing a solid-colored background behind it. The result is a convincing 3D page turn effect built entirely from 2D scanline manipulation.

The compression is driven by a ***cosine function***: at zero degrees the page faces the viewer straight-on and occupies the full screen width. As the turn angle increases toward ninety degrees, the page narrows according to the cosine curve, eventually collapsing to a thin vertical line. This geometry matches how a flat surface would appear when rotated in perspective: the projected width of a tilted rectangle is proportional to the cosine of its tilt angle.

Folio can operate manually, where the turn position is set by a knob, or automatically via an internal oscillator that sweeps the page open and closed in a continuous loop. A configurable background color and fold shadow complete the illusion.

:::tip
Folio excels as a ***transition effect***. Place it in your signal chain and use the **Turn Pos** knob or auto-animation to wipe between your live video and a colored backdrop. The **Mix** fader lets you blend between the processed and unprocessed signal for subtler reveals.
:::

### What's In a Name?

A ***folio*** is a large sheet of paper folded once to form two leaves: the basic unit of a bound book. The name evokes the physical act of turning a page: grabbing a corner and swinging it around the spine. In traditional bookbinding, the folio is the grandest format, and the page turn is the most fundamental interaction. Videomancer's Folio translates that gesture into real-time video, folding your signal like a leaf of parchment.

---

## Quick Start

1. Feed a recognizable video signal into Videomancer with Folio loaded. The image appears normal (the page is fully open at 0°.)
2. Slowly turn **Turn Pos** (Knob 1) clockwise. The video compresses horizontally from one side, revealing a colored background. You are watching the page fold away.
3. Toggle **Hinge** (Switch 7) between **Left** and **Right** to change which edge the page is anchored to. The fold reverses direction.
4. Flip **Animate** (Switch 10) to **Auto** and increase **Anim Spd** (Knob 3). The page begins to oscillate on its own, sweeping open and closed in a continuous loop.

---

## Parameters

![Videomancer front panel with Folio loaded](/img/instruments/videomancer/folio/folio_control_panel.png)
*Videomancer's front panel with Folio active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Turn Pos

| Property | Value |
|----------|-------|
| Range | 0° – 90° |
| Default | 0° |

**Turn Pos** sets the manual turn angle of the page. At 0°, fully counterclockwise, the page faces the viewer head-on and the full input image is visible at its native resolution. As you turn the knob clockwise, the page rotates away from the viewer: the visible width shrinks according to a cosine curve, and the input video is horizontally compressed into the narrowing strip. Around two-thirds of the knob travel, the page reaches its edge-on position: nearly invisible: with the background fully revealed. Continuing past that point, the page begins to reopen as though viewed from behind.

:::note
**Turn Pos** has no effect when **Animate** (Switch 10) is set to **Auto**. In Auto mode, the internal oscillator controls the turn angle and the knob is ignored.
:::

---

### Knob 2 — BKG Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |

**BKG Hue** selects the hue of the background color revealed behind the turning page. The knob sweeps through a full 360° color circle, cycling through reds, yellows, greens, cyans, blues, and magentas. The background is a flat, uniform color: no texture, no gradient. Its brightness is set independently by **BKG Lum** (Knob 6). Together, Hue and Luminance let you dial in any solid color backdrop.

---

### Knob 3 — Anim Spd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Anim Spd** controls the speed of automatic page turn animation. This parameter only has an effect when **Animate** (Switch 10) is set to **Auto**. At 0%, the page is stationary. As the value increases, the page oscillates faster, sweeping from fully open to edge-on and back in a continuous cycle. At high speeds the motion becomes a rapid flutter; at low speeds it produces a slow, dramatic page turn.

The oscillation is driven by a ***direct digital synthesis*** (DDS) phase accumulator: the same technique used in audio synthesizers to generate precise waveforms. Each frame, the speed value is added to a running phase counter, and the accumulated phase selects a position on the cosine curve.

---

### Knob 4 — Curvatur

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Curvatur** is labeled on the panel but is reserved for a future update. In the current version, adjusting this knob has no visible effect on the output. It is intended to add a bowing or warping curvature to the fold geometry.

---

### Knob 5 — Shadow

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Shadow** controls the intensity of perspective shading applied to the turning page. Shading simulates the way a real page darkens as it angles away from a light source. At 0%, the shading effect is at full strength: a page turned to 90° goes completely black. At the default midpoint of 50%, the page retains about half its brightness when edge-on. At 100%, shading is disabled entirely and the page luminance is unaffected by the turn angle.

The shading formula blends between a brightness floor (set by this knob) and full cosine-driven attenuation. Shading affects only the luminance channel: chrominance passes through unaltered, so colors remain vivid even as the page darkens.

:::tip
Set **Shadow** low for dramatic, cinematic page turns where the folding edge disappears into darkness. Set it high if you want the compressed video content to remain fully visible regardless of turn angle.
:::

---

### Knob 6 — BKG Lum

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**BKG Lum** sets the brightness of the background color. At 0%, the background is black regardless of the hue setting. At 100%, the background is at maximum brightness. Combined with **BKG Hue** (Knob 2), this lets you create any solid color from deep dark tones to vivid saturated fields to bright pastels.

---

### Switch 7 — Hinge

| Property | Value |
|----------|-------|
| Off | Left |
| On | Right |
| Default | Left |

**Hinge** selects which edge of the frame the page is anchored to. When set to **Left**, the page is hinged at the left edge: turning the page reveals the background from the right side, and the compressed video remains anchored to the left. When set to **Right**, the anchor flips: the page folds from the left, revealing background on the left side, with video anchored to the right.

---

### Switch 8 — Axis

| Property | Value |
|----------|-------|
| Off | Horiz |
| On | Vert |
| Default | Vert |

**Axis** is labeled as **Horiz** / **Vert** on the panel but is reserved for a future update. In the current version, the page turn always operates along the horizontal axis (compressing scanlines horizontally). Toggling this switch has no visible effect. It is intended to add a vertical turn mode that would compress the image vertically instead.

---

### Switch 9 — Fold Shd

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Fold Shd** enables or disables the fold shadow: a darkened crease that appears at the bending edge of the turning page. When set to **On** (the default), an 8-pixel strip along the fold edge receives an additional 50% luminance reduction on top of the normal perspective shading, creating a visible crease line. When set to **Off**, the fold edge blends smoothly with the rest of the page surface.

:::tip
The fold shadow is a small but important detail for realism. It simulates the way a physical page casts a shadow on itself at the fold. Enable it for convincing page turns; disable it for a cleaner, more abstract compression effect.
:::

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Manual |
| On | Auto |
| Default | Manual |

**Animate** selects between manual and automatic page turn control. In **Manual** mode (default), the turn angle is controlled entirely by **Turn Pos** (Knob 1). In **Auto** mode, an internal oscillator drives the turn angle and the Turn Pos knob is ignored. The oscillation speed is set by **Anim Spd** (Knob 3). Auto mode produces a continuous, hands-free page turn loop: useful for installations, performances, or any situation where you want the effect to run unattended.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Folio processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the page turn effect.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (unprocessed) input and the wet (page turn) output. At 0%, the output is entirely dry: you see the original video with no page turn effect. At 100% (the default), the output is entirely wet: the full page turn is visible. Intermediate positions blend the two, creating a ghostly overlay where the turning page and the unprocessed image coexist.

---

## Background

### The geometry of a turning page

When a flat sheet of paper rotates around a vertical hinge, its apparent width changes. Viewed head-on, the page occupies its full width. As it turns, the visible width narrows. At 90°: perfectly edge-on: the page is just a thin line. The relationship between the turn angle and the visible width is the ***cosine function***: $W = W_0 \cdot \cos(\theta)$, where $W_0$ is the full width and $\theta$ is the turn angle.

This is the same projection that makes a coin look like an ellipse when tilted, or a door appear to shrink as it swings open. Folio uses a 128-entry cosine lookup table to compute this projection for every frame. The result is a convincing 3D perspective illusion built from simple 1D horizontal compression.

### Horizontal compression via DDA

Once Folio knows how many pixels wide the visible page should be, it needs to compress the full-resolution input scanline into that narrower strip. It does this using a ***Digital Differential Analyzer*** (DDA): a classic algorithm from computer graphics that maps coordinates from one space to another. The DDA maintains a running accumulator that steps through source pixel addresses at a fractional rate, reading from the line buffer at non-integer positions. The step size is computed once per frame via a hardware divider: $\text{step} = W_0 / W_{\text{visible}}$.

When the page is fully open, the step size is 1:1: each output pixel reads one input pixel. As the page narrows, the step size increases, skipping source pixels to compress the image. The result is a rescaled version of the input squeezed into the visible region, with the background color filling the remainder of the scanline.

### Fold shading and depth cues

A real turning page darkens as it angles away from a light source. Folio simulates this with two layers of shading. The first layer is ***perspective shading***: the luminance of every "page" pixel is multiplied by a factor derived from the cosine value and the Shadow knob, so the page gradually darkens as it turns. The second layer is the ***fold shadow***: an 8-pixel strip at the bending edge receives an additional 50% luminance reduction, creating a visible crease. Together, these two shading layers give the flat 2D effect a convincing sense of depth.


---

## Signal Flow

### Signal Flow Notes

The key architectural decision in Folio is the separation of write and read paths through the line buffers. Input pixels are written sequentially at native resolution, one per clock. Output pixels are read at DDA-compressed addresses, so the line buffer acts as a random-access scanline resampler. This allows horizontal compression without a dedicated scaler: the DDA accumulator simply skips ahead through the stored scanline data at the appropriate rate.

The DDA step divider uses a restoring binary division algorithm that runs during vertical blanking, completing in 24 clock cycles: well within the available blanking time. This avoids any combinational divider on the pixel processing path, keeping the pipeline deterministic and timing-clean.

:::note
Shading is applied only to the luminance channel. Chrominance (U, V) passes through unmodified from the line buffer. This means colors remain fully saturated even as the page darkens: a deliberate design choice that preserves color vibrancy during the turn.
:::


---

## Exercises

These exercises explore Folio's page turn from basic manual control through animated transitions to creative signal chain techniques.
### Exercise 1: Manual Page Turn

![Manual Page Turn result](/img/instruments/videomancer/folio/folio_ex1_s1.png)
*Manual Page Turn — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A controlled, cinematic page turn that reveals a colored background behind a live video feed.

#### Key Concepts

- Cosine-based horizontal compression
- Hinge side selection
- Perspective shading and fold shadow

#### Video Source

A live camera feed or recorded footage with recognizable subjects and moderate contrast.

#### Steps

1. **Full page**: With **Turn Pos** (Knob 1) fully counterclockwise, the input image fills the screen at native resolution. This is the page at 0°.
2. **Begin the turn**: Slowly rotate Turn Pos clockwise. The image compresses horizontally from the right side: the page is folding away. A colored background appears where the page retreats.
3. **Observe shading**: As the page narrows, it darkens. This is perspective shading. Look for the darker crease at the fold edge (the fold shadow.)
4. **Flip the hinge**: Toggle **Hinge** (Switch 7) to **Right**. The page now folds from the left instead. Try the same slow turn and notice the mirror-image behavior.
5. **Set the backdrop**: Adjust **BKG Hue** (Knob 2) and **BKG Lum** (Knob 6) to choose the revealed background color.

#### Settings

| Control | Value |
|---------|-------|
| Turn Pos | ~45° |
| BKG Hue | 180° |
| Anim Spd | 0% |
| Curvatur | 0% |
| Shadow | 50% |
| BKG Lum | 60% |
| Hinge | Left |
| Axis | Vert |
| Fold Shd | On |
| Animate | Manual |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Automated Page Loop

![Automated Page Loop result](/img/instruments/videomancer/folio/folio_ex2_s1.png)
*Automated Page Loop — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A hands-free, continuously looping page turn animation with dramatic shading and a vivid colored background.

#### Key Concepts

- DDS-driven auto-animation
- Speed control and oscillation behavior
- Shadow depth tuning for dramatic effect

#### Video Source

Footage with bold colors and clear shapes: geometric patterns, architecture, or abstract video synthesis output.

#### Steps

1. **Enable auto-animation**: Set **Animate** (Switch 10) to **Auto**. The page is stationary because **Anim Spd** is at 0%.
2. **Start the oscillation**: Slowly increase **Anim Spd** (Knob 3). The page begins to swing open and closed in a continuous loop, like a door in a breeze.
3. **Tune the speed**: Find a tempo that suits your material. Slow speeds produce stately, cinematic turns. Fast speeds create a rapid flutter.
4. **Deepen the shadows**: Lower **Shadow** (Knob 5) toward 0%. The page now darkens dramatically as it folds, disappearing into near-black at the edge-on position.
5. **Color the backdrop**: Set **BKG Hue** (Knob 2) to a warm tone (around 30°) and increase **BKG Lum** (Knob 6) to 80%. The oscillating page now reveals a glowing amber field with each turn.
6. **Disable fold shadow**: Toggle **Fold Shd** (Switch 9) to **Off**. The crease line vanishes, giving a smoother, more abstract compression effect.

#### Settings

| Control | Value |
|---------|-------|
| Turn Pos | 0° |
| BKG Hue | 30° |
| Anim Spd | ~25% |
| Curvatur | 0% |
| Shadow | 15% |
| BKG Lum | 80% |
| Hinge | Left |
| Axis | Vert |
| Fold Shd | Off |
| Animate | Auto |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Partial Mix Reveal

![Partial Mix Reveal result](/img/instruments/videomancer/folio/folio_ex3_s1.png)
*Partial Mix Reveal — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A partially transparent page turn where the compressed video and the full-frame input coexist as overlapping layers.

#### Key Concepts

- Wet/dry Mix as a compositional tool
- Page turn as a masking / layering technique
- Background color as a design element

#### Video Source

Two contrasting video sources if available (swap during the exercise), or a single source with strong visual structure (text, grids, or graphic overlays.)

#### Steps

1. **Set a half turn**: Place **Turn Pos** (Knob 1) at roughly the midpoint: the page should be visibly compressed, with about half the screen showing background.
2. **Lower the Mix**: Pull **Mix** (Fader 12) down to around 50%. The page turn effect becomes semi-transparent: you see both the compressed page and the full-resolution dry signal simultaneously.
3. **Adjust the background**: Set **BKG Hue** to a contrasting color and **BKG Lum** to a moderate level. The background now tints the overlay, creating a colored split-screen with a ghostly double exposure.
4. **Switch hinge and compare**: Toggle **Hinge** to each side and observe how the layered composition changes. Each hinge position creates a different visual balance.
5. **Try extreme shadow**: Set **Shadow** to 0%. The dark page pixels in the mix create areas of near-transparency where only the dry signal shows through, while the background color bleeds through the open region.
6. **Enable auto-animation at a slow speed**: Set **Animate** to **Auto** and **Anim Spd** to about 10%. The mixed layers shift continuously as the page oscillates.

#### Settings

| Control | Value |
|---------|-------|
| Turn Pos | ~45° |
| BKG Hue | 240° |
| Anim Spd | ~10% |
| Curvatur | 0% |
| Shadow | 0% |
| BKG Lum | 50% |
| Hinge | Right |
| Axis | Vert |
| Fold Shd | On |
| Animate | Auto |
| Bypass | Off |
| Mix | 50% |

---
## Glossary

- **Cosine Function**: A trigonometric function that maps an angle to a ratio between −1 and 1; used here to compute the projected width of a tilted surface.

- **DDA (Digital Differential Analyzer)**: An algorithm that steps through coordinates at a fractional rate, used to resample a scanline into a different number of output pixels.

- **DDS (Direct Digital Synthesis)**: A technique for generating waveforms by accumulating a phase value each cycle and looking up the corresponding amplitude in a table.

- **Fold Shadow**: An additional darkening applied to pixels near the bending edge of the turning page, simulating the crease where a page casts a shadow on itself.

- **Hinge**: The fixed edge around which the page rotates; determines which side of the frame the video remains anchored to during a turn.

- **Interpolator**: A hardware module that performs linear crossfading between two values, used here for the wet/dry mix.

- **Line Buffer**: A block RAM that stores one complete scanline of video data, enabling random-access reads for horizontal resampling.

- **Perspective Shading**: Luminance attenuation proportional to the turn angle, simulating how a surface darkens as it angles away from a light source.

- **Restoring Division**: A binary division algorithm that produces one quotient bit per clock cycle, used here to compute the DDA step size without a combinational divider.

- **Turn Angle**: The rotation of the virtual page, measured in degrees from 0° (fully open) to 90° (edge-on).

---
