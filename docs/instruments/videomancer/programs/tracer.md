---
draft: true
sidebar_position: 311
slug: /instruments/videomancer/tracer
title: "Tracer"
image: /img/instruments/videomancer/tracer/tracer_hero_s1.png
description: "Every child of the 1970s and 1980s remembers the feeling: two white knobs, a silver screen, and a stylus hidden behind a pane of glass, scraping aluminum powder off to reveal dark lines."
---

![Tracer hero image](/img/instruments/videomancer/tracer/tracer_hero_s1.png)
*Tracer rendering persistent edge contours onto a simulated aluminum-powder canvas, evoking the iconic Etch A Sketch drawing toy.*

---

## Overview

**Tracer** is a real-time contour renderer that reimagines your video signal as an Etch A Sketch drawing. It detects edges in the luminance channel using horizontal and vertical gradient operators, then stamps those edges onto a persistent 128×96 canvas stored in block RAM. The canvas simulates the toy's aluminum powder coating: unscraped areas glow with a bright, grainy silver texture, while detected edges carve dark lines through the powder. The result is a living sketch that builds up over time as your source material moves.

The accumulation behavior is what sets Tracer apart from a simple edge detector. Because the canvas retains its contents between frames, edges traced in earlier frames remain visible, layering new contours on top of old ones. The drawing gradually fills in, much like turning the knobs of a real Etch A Sketch. A decay timer periodically clears the canvas, simulating the shake-to-erase gesture, and a manual clear switch lets you wipe the slate on demand.

:::tip
Switch to **Stream** mode for a conventional real-time edge detector: no canvas, no memory. Switch back to **Accum** to let the drawing build up again.
:::

### What's In a Name?

The name ***Tracer*** has two layers of meaning. The first is the verb "to trace": to follow the outline of something, exactly as a stylus traces contours on an Etch A Sketch screen. The second refers to ***edge tracing***, the signal-processing technique of detecting boundaries between bright and dark regions in an image. Tracer does both: it traces the edges of your video and draws them onto a simulated toy screen.

---

## Quick Start

1. Feed a video source with clear subjects and visible edges: a face, a hand, or high-contrast graphics work well. You'll see the silver-gray aluminum powder canvas with dark edge lines scratched through it.
2. Move your source slowly. Watch the contour lines accumulate on the canvas, building up a drawing over time. Earlier edges linger: Tracer remembers.
3. Toggle **Frame** (Switch 8) to **On**. A red bezel with two white knobs appears around the image, completing the Etch A Sketch illusion.
4. Flip **Clear** (Switch 10) to **On** to wipe the canvas clean, then flip it back to **Off** and watch a fresh drawing begin.

---

## Parameters

![Videomancer front panel with Tracer loaded](/img/instruments/videomancer/tracer/tracer_control_panel.png)
*Videomancer's front panel with Tracer active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Edge Thresh

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Edge Thresh** controls the sensitivity of the edge detector. At low values, near 0%, even the faintest luminance gradients register as edges, filling the canvas with dense, noisy contour lines. As you increase the threshold, only stronger gradients: sharper brightness transitions: are detected. At 100%, only the most dramatic edges in your source produce marks on the canvas.

:::tip
Start with Edge Thresh around 40% for clean, readable contour lines. Lower it toward 0% for a dense, textured sketch with fine detail. Raise it toward 100% for a minimal drawing that captures only the boldest outlines.
:::

---

### Knob 2 — Line Weight

| Property | Value |
|----------|-------|
| Range | 1px – 4px |
| Default | 1px |

**Line Weight** selects from four discrete line widths. In the current implementation, the canvas uses a single-pixel stamp regardless of this setting: the parameter is reserved for a future multi-pixel stamp mode. Rotating the knob cycles through four steps (1 px through 4 px), but the visual output does not change.

:::note
Line Weight is reserved for future use. All edges are currently rendered as single-pixel stamps on the 128×96 canvas grid.
:::

---

### Knob 3 — Decay Rate

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Decay Rate** controls how quickly the canvas erases itself. At 0%, the canvas decays very slowly: a full clear happens roughly once every seventeen seconds. As you increase Decay Rate, the clear cycle shortens. At 100%, the canvas clears every single frame, which looks nearly identical to the live **Stream** mode. A moderate setting around 40% gives you several seconds of accumulated drawing before the slate wipes clean and starts over.

The decay works by counting frames between full sequential clears. Each clear sweeps through all 12,288 canvas cells one by one, taking roughly one-fifth of a frame to complete. During the sweep, new edges continue to stamp, so you may briefly see the drawing being rebuilt from top to bottom.

---

### Knob 4 — Powder Brt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Powder Brt** sets the brightness of the unscraped aluminum powder: the background of the drawing surface. At 0%, the powder is dark, and the canvas appears dim. At 100%, the powder glows bright silver-white. The grain texture rides on top of this base brightness, so the visual character of the powder changes as you adjust this knob.

---

### Knob 5 — Grain Amt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Grain Amt** controls the intensity of the aluminum-grain texture overlaid on the powder surface. At 0%, the powder is perfectly smooth and uniform. As you increase Grain Amt, the ***LFSR***-generated noise becomes visible as a fine, shimmering speckle pattern across the unscraped areas. A small amount of grain also appears in the scraped (line) regions, but at one-quarter the intensity of the powder grain.

:::note
The grain is generated by a 16-bit ***linear feedback shift register*** (LFSR): a simple pseudo-random number generator clocked every pixel. The texture is deterministic but visually random, and it shifts every frame, creating a gentle shimmer.
:::

---

### Knob 6 — Contrast

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 62.6% |

**Contrast** controls the brightness of the scraped line areas: the dark trenches carved through the powder. At 0%, scraped lines are pure black. As you increase Contrast, the scraped areas become brighter and closer in tone to the surrounding powder surface, reducing the visual contrast between lines and background. At 100%, scraped lines are still noticeably darker than the powder (maximum scraped brightness is about one-eighth of full scale), but the difference is gentler.

Think of it as controlling how deeply the stylus digs. Low Contrast = deep scratches exposing the dark glass underneath. High Contrast = light scratches that barely disturb the powder.

---

### Switch 7 — Negative

| Property | Value |
|----------|-------|
| Off | Normal |
| On | Invert |
| Default | Normal |

**Negative** inverts the rendered image after the powder and line brightness are calculated. In **Normal** mode, scraped lines are dark on a bright powder background: the classic Etch A Sketch look. In **Invert** mode, the relationship flips: bright lines glow against a dark background, resembling a neon contour drawing or an X-ray sketch.

Negative applies after all rendering math, so it also inverts the grain texture. The frame overlay (if enabled) is not affected (it still appears as a red bezel with white knobs.)

---

### Switch 8 — Frame

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Frame** enables a decorative border overlay that simulates the red plastic bezel and white turning knobs of a classic Etch A Sketch toy. The border is 40 pixels wide on the left and right edges and 30 pixels tall on the top and bottom. Two circular white knobs sit in the lower corners. When Frame is **Off**, the full drawing area fills the screen.

The frame is rendered in color: a warm red bezel and achromatic white knobs. This is the only part of Tracer's output that carries chrominance (the drawing area is always monochrome.)

---

### Switch 9 — Continuous

| Property | Value |
|----------|-------|
| Off | Accum |
| On | Stream |
| Default | Accum |

**Continuous** selects between two fundamentally different operating modes. In **Accum** mode (the default), detected edges stamp onto the persistent BRAM canvas and remain visible until the canvas is cleared by decay or by the **Clear** switch. The drawing builds up over time. In **Stream** mode, the canvas is bypassed entirely: the output shows only the edges detected in the current frame, with no memory of previous frames. Stream mode turns Tracer into a conventional real-time edge detector.

:::tip
Use **Accum** mode for the signature Etch A Sketch drawing effect. Switch to **Stream** for a live edge-detect overlay that you can blend with the dry signal using the **Mix** fader.
:::

---

### Switch 10 — Clear

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Clear** triggers an immediate full canvas wipe. When you flip the switch to **On**, Tracer begins a sequential clear that sweeps through all 12,288 canvas cells, erasing every mark. The clear completes in a fraction of a frame. Flip the switch back to **Off** afterward (leaving it on will repeatedly trigger clears.)

Clear takes priority over edge stamping. While a clear is in progress, new edges cannot write to the canvas. Once the sweep finishes, normal accumulation resumes.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input video directly to the output, skipping all of Tracer's rendering stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw source and the Etch A Sketch rendering.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** blends between the dry (unprocessed) input signal and the wet (rendered) output using a crossfade interpolator. At 0%, only the dry input is visible and the Etch A Sketch drawing is completely hidden. At 100%, only the rendered canvas output is visible. Intermediate values produce a ghostly overlay of the drawing on top of the source video.

:::tip
Set Mix to around 50% in **Stream** mode for a stylized edge-detection overlay on your live video. In **Accum** mode, a moderate Mix value shows the accumulated drawing faintly superimposed on the source (like tracing paper laid over a photograph.)
:::

---

## Background

### Edge detection

***Edge detection*** is one of the oldest and most fundamental operations in image processing. An edge is a boundary where brightness changes sharply: the outline of an object, a shadow, a printed letter. To find edges, we compute the ***gradient*** of the image: the rate of brightness change from one pixel to the next. If the gradient exceeds a threshold, we declare that pixel an edge.

Tracer uses a simple first-difference gradient operator. It computes horizontal differences (current pixel minus previous pixel) and vertical differences (current pixel minus the same pixel on the previous scan line). The magnitudes of both differences are summed using the ***Manhattan distance*** (absolute values added together, not squared and square-rooted like the Euclidean distance). This sum is compared against the **Edge Thresh** parameter to produce a binary edge-or-not decision per pixel.

### The line buffer

Computing the vertical gradient requires access to the previous scan line's data: which has long since scrolled past. Tracer stores the previous line in a ***line buffer***, a 2048×10-bit block RAM that acts as a one-line delay. As each pixel arrives, the buffer is read at the current horizontal position (returning the previous line's value at that position) and then written with the current line's value. This read-first pattern ensures the gradient has both the current and previous line data it needs.

### The persistent canvas

The heart of Tracer is its 128×96-cell persistent canvas: a 1-bit-per-cell array stored in block RAM. Each canvas cell covers a 16×16 block of video pixels. When an edge is detected, the corresponding canvas cell is set to 1 (scraped). When the canvas is read during rendering, a 0 produces the bright powder color and a 1 produces the dark scraped color.

Because the canvas retains its state between frames, edges accumulate over time. A slow pan across a scene paints its contours onto the canvas in real time. The ***decay timer*** counters this by periodically sweeping through every cell and resetting it to 0, simulating the Etch A Sketch's shake-to-erase action.

### Aluminum powder rendering

The original Etch A Sketch works by scraping aluminum powder off the underside of a glass screen with a pointed stylus. Unscraped areas appear bright silver-gray; scraped areas reveal the dark screen beneath. Tracer simulates this with two brightness levels:

- **Powder** (bright): base brightness from **Powder Brt**, plus a grain texture from the LFSR
- **Scraped** (dark): base brightness from **Contrast** (at 1/8 scale), plus a faint grain at 1/4 the powder grain intensity

The LFSR grain gives the powder surface a subtle sparkling texture reminiscent of aluminum flakes catching light at different angles.


---

## Signal Flow

### Signal Flow Notes

Three key architectural details shape Tracer's behavior:

1. **Edge detection is luminance-only.** Horizontal and vertical gradients are computed from the Y channel. Chrominance plays no role in edge detection: a color boundary with identical brightness on both sides produces no edge mark. The rendered output is achromatic by design (U and V are neutral 512), except for the optional frame overlay.

2. **Canvas resolution is much lower than video resolution.** The 128×96 canvas maps each cell to a 16×16 block of video pixels, giving the output a coarse, blocky character that matches the chunky resolution of a real Etch A Sketch screen. Multiple edge pixels within the same 16×16 block all stamp the same canvas cell (detail below canvas resolution is lost.)

3. **Decay is a full sequential clear, not a per-cell fade.** When the decay timer fires, it doesn't dim individual cells. Instead, it sweeps through the entire canvas from start to end, resetting each cell to 0. This takes about 12,288 clock cycles: a fraction of one frame: during which new edges continue to stamp. The result is a periodic clean-slate reset rather than a gradual fadeout.

:::note
The canvas uses 3 block RAMs (12,288 × 1-bit) and the line buffer uses 5 block RAMs (2,048 × 10-bit), for a total of 8 out of 32 available on the iCE40 HX4K.
:::


---

## Exercises

These exercises progress from basic edge detection through full Etch A Sketch rendering with frame overlay. Each exercise builds on the concepts introduced in the previous one.
### Exercise 1: Live Edge Detection

![Live Edge Detection result](/img/instruments/videomancer/tracer/tracer_ex1_s1.png)
*Live Edge Detection — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean, real-time edge-detection overlay blended with your live source.

#### Key Concepts

- Edge detection via luminance gradients
- Threshold sensitivity
- Stream versus Accumulate modes

#### Video Source

A live camera feed or recorded footage with clear subjects (faces, hands, or high-contrast objects work well.)

#### Steps

1. **Stream mode**: Set **Continuous** (Switch 9) to **Stream**. Tracer now shows only the edges detected in the current frame, with no canvas memory.
2. **Adjust sensitivity**: Turn **Edge Thresh** (Knob 1) to about 40%. You should see clean contour lines around your subject against a bright powder background.
3. **Explore threshold**: Sweep Edge Thresh from 0% to 100%. At low values, the image fills with noisy edge detail. At high values, only the boldest outlines remain.
4. **Blend with source**: Lower **Mix** (Fader 12) to about 50%. The edge contours appear as a translucent overlay on top of your original video (a stylized outline effect.)
5. **Invert**: Toggle **Negative** (Switch 7) to **Invert** for bright neon lines on a dark background. This looks especially striking at 50% Mix.

#### Settings

| Control | Value |
|---------|-------|
| Edge Thresh | 40% |
| Line Weight | 1 px |
| Decay Rate | 40% |
| Powder Brt | 75% |
| Grain Amt | 20% |
| Contrast | 10% |
| Negative | Normal |
| Frame | Off |
| Continuous | Stream |
| Clear | Off |
| Bypass | Off |
| Mix | 50% |

---

### Exercise 2: Classic Etch A Sketch

![Classic Etch A Sketch result](/img/instruments/videomancer/tracer/tracer_ex2_s1.png)
*Classic Etch A Sketch — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A faithful Etch A Sketch simulation with accumulating contour lines, periodic decay, and the iconic red frame.

#### Key Concepts

- Persistent canvas accumulation
- Decay rate and manual clear
- Frame overlay

#### Video Source

Slow-moving footage or a camera pointed at a scene with gentle motion: a person slowly turning their head, or a hand moving across the frame.

#### Steps

1. **Accumulate mode**: Set **Continuous** (Switch 9) to **Accum**. Edges now stamp onto the persistent canvas.
2. **Set the look**: Turn **Powder Brt** (Knob 4) to about 75% for a bright silver background. Set **Contrast** (Knob 6) to about 30% for clear dark lines. Add a touch of **Grain Amt** (Knob 5) at about 50%.
3. **Enable the frame**: Flip **Frame** (Switch 8) to **On**. The red bezel and white knobs appear. Now it looks like a real Etch A Sketch.
4. **Watch it draw**: Let your slow-moving source trace lines onto the canvas over several seconds. The drawing builds up, capturing the edges from each frame.
5. **Clear and restart**: Flip **Clear** (Switch 10) to **On**, then immediately back to **Off**. The canvas wipes clean and the drawing starts fresh.
6. **Decay**: Set **Decay Rate** (Knob 3) to about 20%. The canvas now periodically erases itself, creating a cycle of drawing and erasing.
7. **Full mix**: Set **Mix** (Fader 12) to 100% to see only the Etch A Sketch rendering (no source video peeking through.)

#### Settings

| Control | Value |
|---------|-------|
| Edge Thresh | 45% |
| Line Weight | 1 px |
| Decay Rate | 20% |
| Powder Brt | 75% |
| Grain Amt | 50% |
| Contrast | 30% |
| Negative | Normal |
| Frame | On |
| Continuous | Accum |
| Clear | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Inverted Neon Persistence

![Inverted Neon Persistence result](/img/instruments/videomancer/tracer/tracer_ex3_s1.png)
*Inverted Neon Persistence — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A glowing neon contour map that accumulates over time, with bright lines on a dark background and shimmering grain.

#### Key Concepts

- Negative mode creates bright-on-dark rendering
- Grain texture and powder brightness interact
- Accumulated edges produce complex layered patterns

#### Video Source

High-contrast footage with strong edges: geometric objects, architecture, or graphic patterns. Moving source material creates the most interesting accumulation patterns.

#### Steps

1. **Invert the palette**: Set **Negative** (Switch 7) to **Invert**. The powder becomes dark and the lines become bright.
2. **High sensitivity**: Set **Edge Thresh** (Knob 1) to about 25% to capture fine detail.
3. **Dim the powder**: Set **Powder Brt** (Knob 4) to about 25%. Since Negative is on, this becomes the brightness of the dark background.
4. **Heavy grain**: Increase **Grain Amt** (Knob 5) to about 80%. The background now shimmers with a dense speckle texture (like static on a dark CRT.)
5. **Bright lines**: Lower **Contrast** (Knob 6) to about 10%. In Negative mode, low Contrast produces the brightest lines (the inversion of a very dark scraped value).
6. **Slow decay**: Set **Decay Rate** (Knob 3) to about 10%. The accumulated drawing persists for a long time, building up a complex web of neon contours.
7. **Watch**: Let the source move slowly. Bright contour lines accumulate like light trails in a long-exposure photograph, gradually revealing the motion history of your source.

#### Settings

| Control | Value |
|---------|-------|
| Edge Thresh | 25% |
| Line Weight | 1 px |
| Decay Rate | 10% |
| Powder Brt | 25% |
| Grain Amt | 80% |
| Contrast | 10% |
| Negative | Invert |
| Frame | Off |
| Continuous | Accum |
| Clear | Off |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Block RAM (BRAM)**: Dedicated memory blocks on an FPGA, used here for the line buffer and persistent canvas.

- **Canvas**: The 128×96-cell persistent memory that stores traced edge marks, simulating the aluminum-powder screen of an Etch A Sketch.

- **Decay**: The periodic canvas-clearing mechanism that simulates the "shake to erase" gesture, controlled by the Decay Rate parameter.

- **Edge Detection**: The process of identifying boundaries in an image where brightness changes sharply, by computing the gradient of the luminance signal.

- **Gradient**: The rate of change of brightness between adjacent pixels; used to measure edge strength.

- **LFSR**: Linear Feedback Shift Register: a simple pseudo-random number generator used here to produce the aluminum grain texture.

- **Line Buffer**: A single-scanline delay stored in BRAM, providing access to the previous line's luminance data for vertical gradient computation.

- **Manhattan Distance**: A distance metric that sums absolute differences along each axis, used here to combine horizontal and vertical gradients without a square root.

- **Stamp**: The act of writing a 1 to a canvas cell when an edge is detected at that location, permanently marking it until the canvas is cleared.

---
