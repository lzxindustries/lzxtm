---
draft: true
sidebar_position: 274
slug: /instruments/videomancer/slitscan
title: "Slit Scan"
image: /img/instruments/videomancer/slitscan/slitscan_hero_s1.png
description: "Slit Scan captures a narrow vertical strip of the input image each frame and writes it into a scrolling BRAM framebuffer."
---

![Slit Scan hero image](/img/instruments/videomancer/slitscan/slitscan_hero_s1.png)
*Slit Scan unfolding a live video input into a luminous temporal ribbon, each column a frozen instant scrolling across the screen.*

---

## Overview

**Slit Scan** is a real-time spatio-temporal streak processor that turns time into space. It captures a narrow vertical strip of the input frame and writes it into a scrolling ***framebuffer***: a small block of memory inside the FPGA that holds an entire low-resolution image. Each column of the output represents a different moment in time, so the result is a continuously scrolling panorama of sampled instants. Move your hand in front of the camera and watch it stretch into a luminous ribbon that trails across the screen.

The framebuffer stores only luminance at reduced resolution (160 × 68 pixels, roughly one-eighth the horizontal and one-sixteenth the vertical size of the input). Old columns gradually fade away at a rate controlled by the **Decay** parameter, and a **Hue Shift** knob tints the monochrome luminance data with color. The **Mix** fader crossfades between the dry input and the wet streak image, letting you layer the temporal panorama over the original video.

:::tip
Because the framebuffer is downsampled, Slit Scan has a characteristically soft, low-resolution look: more like a glowing memory than a sharp recording. Lean into it. The warmth is part of the charm.
:::

### What's In a Name?

The name ***Slit Scan*** comes directly from the optical photographic technique pioneered by special effects artist Douglas Trumbull for the Star Gate sequence in *2001: A Space Odyssey* (1968). In the original technique, a camera moves slowly past a narrow slit cut in a mask, exposing the film to a long, thin stripe of artwork at each moment. The result is an image where the horizontal axis represents time rather than space: a streak photograph. Videomancer's Slit Scan recreates this process digitally, sampling a thin vertical strip of live video and scrolling it into a memory buffer so that each column of the output is a snapshot from a different moment.

---

## Quick Start

1. Feed a live camera signal into Videomancer and load **Slit Scan**. You should see a scrolling panorama of luminance strips (the program is already capturing and scrolling by default.)
2. Turn **Strip Pos** (Knob 1) slowly. The vertical sample line moves across the input frame, picking up different parts of the image. Try waving your hand in front of the camera to see the streak respond.
3. Increase **Decay** (Knob 4) clockwise. Old strips fade out more quickly, leaving a shorter visible trail. Decrease it to let strips linger and accumulate.
4. Rotate **Hue Shift** (Knob 6) to tint the monochrome streak with color (reds, greens, blues, or back to pure white.)

---

## Parameters

![Videomancer front panel with Slit Scan loaded](/img/instruments/videomancer/slitscan/slitscan_control_panel.png)
*Videomancer's front panel with Slit Scan active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Strip Pos

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Strip Pos** selects where on the input frame the capture strip is located. At 0%, the strip sits at the left edge of the frame. At 100%, it sits at the right edge. Every frame, the luminance values along this thin vertical column are sampled and written into the framebuffer at the current scroll position. Moving the strip across a moving subject changes which part of the action gets recorded into the streak panorama.

:::note
Because the framebuffer is downsampled to one-sixteenth vertical resolution, fine vertical detail in the source is averaged into broader bands. The strip captures the coarse luminance structure of the input.
:::

---

### Knob 2 — Scroll Spd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Scroll Spd** controls how quickly the write position advances through the framebuffer. At low values the panorama scrolls slowly: each captured strip lingers in place for many frames before the next column overwrites the adjacent position. At high values the write position races across the buffer, producing a fast-moving streak. The speed is driven by an ***accumulator***: the scroll speed value is added to an internal counter every frame, and the write column advances by one pixel each time the counter overflows. This means very low speed settings produce a stepped, intermittent scroll rather than continuous motion.

---

### Knob 3 — Strip Width

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 6% |

**Strip Width** adjusts the width of the capture strip: the horizontal span of input pixels that are sampled on each frame. At narrow settings, a single thin slice of the input is captured, producing clean, well-defined streaks. At wider settings, a broader swath of input is sampled, blending more of the horizontal scene into each captured column.

---

### Knob 4 — Decay

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Decay** controls the fade rate for old columns in the framebuffer. Every frame, during the ***vertical blanking interval***, the FPGA walks through every pixel in the framebuffer and subtracts a small value determined by this knob. At 0%, no decay occurs and old strips persist indefinitely, gradually building up a dense layered history. As Decay increases, old columns fade to black more quickly, shortening the visible trail. At very high settings, only the most recent few columns remain visible and the panorama becomes a narrow bright band racing across a dark field.

:::tip
***Decay is subtractive, not multiplicative.*** Each pixel loses the same fixed amount per frame regardless of its brightness. This means bright strips survive longer than dim ones (a natural, visually appealing fade characteristic.)
:::

---

### Knob 5 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** scales the output luminance of the framebuffer readout. At 50%, the stored luminance passes through at unity gain. Below 50%, the streak image dims. Above 50%, it brightens: values near 100% can push peaks into clipping, producing a hot, blown-out look. Because the framebuffer stores only 8-bit luminance, Brightness is applied during the read pipeline *after* the stored data is retrieved, giving you final control over the visible intensity of the streak.

---

### Knob 6 — Hue Shift

| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |

**Hue Shift** tints the monochrome streak with color. The framebuffer stores luminance only: no color information. Hue Shift generates synthetic chrominance from the stored luma, painting the streak in one of four broad color families as the knob sweeps through its full rotation. Turning the knob from its minimum, the streak passes through warm reds, then greens, then cool blues, before returning to pure monochrome white at the far end of the range.

The color mapping is intentionally coarse: four broad zones rather than a smooth rainbow: giving each zone a distinct, saturated character. The brighter the stored luminance, the more vivid the tint.

---

### Switch 7 — Axis

| Property | Value |
|----------|-------|
| Off | Vertical |
| On | Horizontal |
| Default | Vertical |

**Axis** selects whether the capture strip and scroll direction are oriented vertically or horizontally. In **Vertical** mode (default), a vertical strip of input is captured and the panorama scrolls horizontally. In **Horizontal** mode, a horizontal strip is captured and the panorama scrolls vertically, creating top-to-bottom or bottom-to-top streaks.

---

### Switch 8 — Direction

| Property | Value |
|----------|-------|
| Off | Right |
| On | Left |
| Default | Right |

**Direction** controls which way the scroll moves. In **Right** mode (default), the write position advances from left to right: new strips appear on the left and old ones exit on the right. In **Left** mode, the direction reverses: new strips appear on the right and scroll leftward. Flipping direction mid-performance reverses the flow of time in the panorama.

---

### Switch 9 — Trail

| Property | Value |
|----------|-------|
| Off | Streak |
| On | Mirror |
| Default | Streak |

**Trail** selects between two scroll behaviors. In **Streak** mode (default), the write position wraps around when it reaches the edge of the framebuffer, creating a continuous loop: old strips silently vanish behind the advancing write head. In **Mirror** mode, the scroll direction bounces at the edges of the buffer, like a ball reflecting off a wall. This creates a back-and-forth oscillation that keeps the entire history visible as it alternately advances and retreats.

---

### Switch 10 — Freeze

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Freeze** halts both capture and scroll when set to **On**. The framebuffer stops updating: no new strips are captured and no decay is applied. The output holds a frozen snapshot of the streak panorama as it existed at the moment Freeze was engaged. Toggle it off to resume live capture. Use Freeze to hold an interesting composition while adjusting other parameters, or to create a static backdrop that you can then crossfade against the live input with the **Mix** fader.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input video directly to the output, skipping all Slit Scan processing. The sync delay pipeline still maintains timing alignment, so switching between processed and bypassed output is glitch-free. Use Bypass for instant A/B comparison.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry input video and the wet slit-scan output. At 0%, only the original input is visible. At 100%, only the streak panorama is visible. Intermediate values blend the two, layering the low-resolution temporal ribbon over the full-resolution source. This is useful for creating ghostly overlay effects where the streak trails behind or beneath the live image.

:::tip
Try setting Mix to around 50% while waving an object in front of the camera. The object appears in sharp focus *and* as a stretched, softly glowing trail (like a time-lapse double exposure.)
:::

---

## Background

### Slit-scan photography

The slit-scan technique predates both video and cinema. In its simplest form, a camera exposes film through a narrow slit while either the slit or the subject moves. Because each horizontal strip of the resulting image is exposed at a different moment, the photograph encodes time along one spatial axis. Sports photographers used slit-scan (sometimes called ***strip photography***) to capture photo finishes at racetracks: the position on the film corresponds directly to the moment each runner crossed the finish line.

Douglas Trumbull's landmark use of the technique in *2001: A Space Odyssey* brought slit-scan into the world of cinematic special effects. Trumbull's rig moved a camera slowly toward a narrow slit, behind which a piece of backlit art was being pulled. The resulting footage is the psychedelic Star Gate sequence: a tunnel of endlessly streaking colors. Videomancer's Slit Scan captures the essence of this process in real time: a thin slice of live video is sampled each frame and scrolled into a digital framebuffer.

### Framebuffer and downsampling

The iCE40 FPGA has limited block RAM: 32 tiles of 4 Kbit each. Slit Scan uses 3 of those tiles to store a 160 × 68 pixel luminance framebuffer (10,880 bytes). The input video is downsampled by a factor of 8 horizontally and 16 vertically to fit into this memory budget. This aggressive downsampling is what gives Slit Scan its characteristic soft, blocky, lo-fi texture.

The framebuffer stores only the Y (luminance) component. No color information is recorded. Color is synthesized at the output stage from the stored luminance and the **Hue Shift** parameter, which tints the monochrome data across four broad color zones.

### Decay and persistence

Each frame, during the ***vertical blanking interval*** (the brief pause while the video beam retraces from bottom to top), the FPGA iterates through every pixel in the framebuffer and subtracts a fixed amount determined by the **Decay** knob. This is a simple linear fade: bright pixels lose the same absolute value per frame as dim ones, so bright strips persist longer. The decay pass is a ***read-modify-write*** loop: each pixel is read, reduced, and written back: cycling through all 10,880 addresses at FPGA clock speed. The entire pass completes well within the blanking interval.


---

## Signal Flow

### Signal Flow Notes

The architecture splits into two time domains. During ***active video*** (when pixels are being drawn), the capture path samples input luminance at the strip position and writes it into the framebuffer, while the read pipeline simultaneously reads the framebuffer at a different address to produce output. During ***vertical blanking***, the decay pass sweeps through the entire framebuffer, fading every stored pixel.

The read pipeline adds an offset equal to the current write column so that the most recently captured strip always appears at the left edge of the output (or right edge, depending on direction). This gives the panorama its characteristic "scrolling across the screen" appearance: the write head stays anchored in screen space while history fills in behind it.

:::note
Because the framebuffer stores only luminance, the chroma channels in the output are entirely synthetic. The Hue Shift parameter selects one of four color zones (red, green, blue, or neutral) and derives U and V values proportional to the stored luma. This means brighter regions receive more saturated tints while dark regions remain nearly neutral.
:::


---

## Exercises

These exercises progress from observing the raw streak effect to building layered compositions that use Slit Scan as a time-based painting tool.
### Exercise 1: Temporal Ribbon

![Temporal Ribbon result](/img/instruments/videomancer/slitscan/slitscan_ex1_s1.png)
*Temporal Ribbon — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A basic scrolling streak panorama that turns motion into a luminous ribbon.

#### Key Concepts

- The framebuffer captures a thin slice of each frame and scrolls it
- Decay controls how long old strips persist
- Strip Pos selects *what* is captured

#### Video Source

A live camera feed pointed at a scene with slow, continuous movement (a lava lamp, flowing water, or your own hand waving.)

#### Steps

1. Load **Slit Scan** with default settings. You should see a scrolling panorama of luminance strips.
2. Wave your hand slowly in front of the camera. Watch the hand stretch into a horizontal ribbon as each frame's strip captures a thin slice of the motion.
3. Turn **Strip Pos** (Knob 1) to move the capture line across the frame. Different parts of the scene produce different streak textures.
4. Lower **Scroll Spd** (Knob 2) until the scroll slows to a crawl. Each captured strip persists for many frames before advancing. Raise it back up for a fast-moving streak.
5. Increase **Decay** (Knob 4) to shorten the visible trail. Decrease it to zero and watch the framebuffer fill up with a dense, layered history that never fades.

#### Settings

| Control | Value |
|---------|-------|
| Strip Pos | 50% |
| Scroll Spd | ~25% |
| Strip Width | 6% |
| Decay | ~40% |
| Brightness | 50% |
| Hue Shift | 0d |
| Axis | Vertical |
| Direction | Right |
| Trail | Streak |
| Freeze | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Color Painted Streaks

![Color Painted Streaks result](/img/instruments/videomancer/slitscan/slitscan_ex2_s1.png)
*Color Painted Streaks — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A vivid, color-tinted temporal panorama layered over the live input.

#### Key Concepts

- The framebuffer is monochrome; color is synthesized from luminance
- Hue Shift selects one of four broad color families
- Brightness scales the final output intensity

#### Video Source

A camera feed with varied brightness (faces, hands, or objects under directional lighting.)

#### Steps

1. Set **Mix** (Fader 12) to about 50%. The streak panorama now overlays the live camera input: you can see both the sharp original and the soft, downsampled trail.
2. Rotate **Hue Shift** (Knob 6) slowly through its range. Watch the streak move through warm reds, greens, and cool blues before returning to monochrome at the far end.
3. Stop at a color you like. Now increase **Brightness** (Knob 5) until the streak glows vividly against the dimmer dry input.
4. Increase **Decay** (Knob 4) to a moderate value so the trail is clearly visible but not overwhelming. The streak should glow and fade like a comet tail.
5. Flip **Direction** (Switch 8) to **Left**. The panorama reverses (new strips appear on the right and scroll leftward.)

#### Settings

| Control | Value |
|---------|-------|
| Strip Pos | 50% |
| Scroll Spd | ~30% |
| Strip Width | 6% |
| Decay | ~50% |
| Brightness | ~65% |
| Hue Shift | ~90d |
| Axis | Vertical |
| Direction | Left |
| Trail | Streak |
| Freeze | Off |
| Bypass | Off |
| Mix | 50% |

---

### Exercise 3: Frozen Time Collage

![Frozen Time Collage result](/img/instruments/videomancer/slitscan/slitscan_ex3_s1.png)
*Frozen Time Collage — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A time-collage effect: freeze a streak panorama, then layer live video over it.

#### Key Concepts

- Freeze halts capture and decay, locking the framebuffer state
- The frozen panorama becomes a static texture for compositing
- Mix blends the frozen texture with live video

#### Video Source

A camera feed with varied, interesting movement (dancers, traffic, or light patterns.)

#### Steps

1. Start with moderate **Scroll Spd** (~30%) and **Decay** (~40%). Let the streak panorama build for a few seconds with lively input.
2. When you see a composition you like, flip **Freeze** (Switch 10) to **On**. The panorama locks in place (a frozen snapshot of accumulated time.)
3. Set **Mix** (Fader 12) to about 40%. The frozen streak becomes a glowing backdrop behind the live camera feed.
4. Move the camera or change the scene. The live input moves freely while the frozen streaks remain static underneath.
5. Adjust **Brightness** (Knob 5) and **Hue Shift** (Knob 6) to change the color and intensity of the frozen backdrop without unfreezing it.
6. Flip **Freeze** off to resume live capture. The panorama immediately begins scrolling and updating again with fresh input over the old frozen data.

#### Settings

| Control | Value |
|---------|-------|
| Strip Pos | 50% |
| Scroll Spd | ~30% |
| Strip Width | 6% |
| Decay | ~40% |
| Brightness | 50% |
| Hue Shift | ~180d |
| Axis | Vertical |
| Direction | Right |
| Trail | Streak |
| Freeze | On |
| Bypass | Off |
| Mix | 40% |

---
## Glossary

- **Accumulator**: A counter that adds a fixed value each frame; when it overflows a threshold, it triggers an event (here, advancing the scroll position by one column).

- **Blanking Interval**: The portion of each video frame during which no visible pixels are drawn: used by Slit Scan to perform framebuffer maintenance (decay) without interfering with the output image.

- **Decay**: The per-frame subtraction applied to every pixel in the framebuffer, causing old data to fade toward black over time.

- **Downsampling**: Reducing the resolution of an image by discarding or averaging pixels, here from full-resolution video to 160 × 68 pixels.

- **Framebuffer**: A region of memory (BRAM) that stores an image. Slit Scan's framebuffer holds a 160 × 68 pixel luminance snapshot, allowing it to accumulate and display a history of captured strips.

- **Interpolator**: A hardware crossfade module that blends between two input values according to a mix parameter, used here for wet/dry blending.

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Read-Modify-Write**: A three-step memory operation: read a value, transform it, and write it back to the same address (used during the decay pass.)

- **Slit Scan**: A photographic and cinematographic technique where an image is built by exposing a narrow slit of the scene at successive moments, encoding time along one spatial axis.

- **Streak**: A visual trail produced by accumulating successive strip captures into a scrolling framebuffer.

---
