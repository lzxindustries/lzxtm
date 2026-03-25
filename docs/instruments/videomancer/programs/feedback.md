---
draft: true
sidebar_position: 109
slug: /instruments/videomancer/feedback
title: "Feedback"
image: /img/instruments/videomancer/feedback/feedback_hero_s1.png
description: "Feedback is one of the most powerful techniques in analog video synthesis — point a camera at its own monitor, and the image folds into itself endlessly, creating spiraling tunnels, ghost trails, and self-similar fractal structures."
---

![Feedback hero image](/img/instruments/videomancer/feedback/feedback_hero_s1.png)
*Feedback simulating an infinite camera-monitor tunnel with color-shifted recursion and kaleidoscopic mirroring.*

---

## Overview

**Feedback** recreates the mesmerizing visual phenomenon that occurs when a camera points at its own monitor: an infinite tunnel of self-similar images stretching into the distance. Rather than requiring physical equipment, Feedback achieves this digitally by writing each scanline into a circular line buffer and simultaneously reading from a spatially displaced position. The read data is blended with the incoming video and written back, creating ***iterative recursion*** where each pixel carries traces of its own past.

The result is a living, breathing tunnel of imagery that zooms, rotates in color, and decays over time. At subtle settings, Feedback produces gentle echo trails and ghostly afterimages. At extreme settings, it generates swirling psychedelic tunnels, kaleidoscopic symmetry patterns, and self-exciting color explosions that bear little resemblance to the original source.

:::tip
Feedback is one of the few programs where ***the output feeds back into itself***. Small changes in Gain or Decay can push the system from gentle trails into runaway self-excitation. That instability is a feature (lean into it.)
:::

### What's In a Name?

The name ***Feedback*** refers directly to the optical phenomenon of ***video feedback***: an early staple of video art pioneered in the 1960s and '70s. Artists like Nam June Paik and the Vasulkas discovered that pointing a camera at its own monitor creates recursive, fractal-like imagery. The signal feeds back into itself, each pass amplifying, rotating, and distorting the image. Videomancer's Feedback program captures this spirit in a single scanline-based FPGA effect, giving you all the expressiveness of a camera-monitor loop without the physical setup.

---

## Quick Start

1. Feed a video source into Videomancer. Turn **Decay** (Knob 4) clockwise to about 70%. You should see a ghostly trail following any motion (the signal is now feeding back into itself.)
2. Slowly increase **Zoom** (Knob 1). The echo shifts spatially, and the image begins to develop a tunnel-like streak. Move the source and watch the streaks follow.
3. Turn up **Color Shift** (Knob 3) to about 40%. The feedback trail rotates through hues with each pass, creating rainbow echoes trailing behind every moving element.
4. Flip **Mirror** (Switch 8) to **On**. The tunnel becomes bilateral: a symmetrical kaleidoscope that mirrors the feedback pattern across the horizontal axis.

---

## Parameters

![Videomancer front panel with Feedback loaded](/img/instruments/videomancer/feedback/feedback_control_panel.png)
*Videomancer's front panel with Feedback active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Zoom

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |

**Zoom** controls the spatial offset between the current pixel and its feedback read position. Think of it as how far the "camera" is zoomed into the "monitor." At 0%, the offset is minimal: feedback reads from nearly the same pixel, producing subtle ghosting. As Zoom increases, the displacement grows, and the image develops pronounced streaks and tunnel perspective. At 100%, the offset is at its maximum, creating wide spatial displacement between iterations.

Zoom interacts with **X Offset** (Knob 5) to define the overall horizontal displacement. Zoom contributes the upper bits of the offset (coarser steps), while X Offset contributes finer positioning.

---

### Knob 2 — Gain

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |

**Gain** controls the brightness amplification applied to the feedback signal before it is blended with the incoming video. At 0%, the feedback data receives minimal amplification: trails fade rapidly. As Gain increases, each pass through the buffer gets brighter, causing trails to persist longer and glow more intensely. At high values, the system enters ***self-excitation***: the feedback amplifies itself faster than it decays, and the image floods with saturated light.

:::warning
High Gain combined with high Decay can cause the image to blow out to pure white. This is the intended behavior: the system is self-exciting. Reduce Gain or Decay to bring it back under control.
:::

---

### Knob 3 — Color Shift

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |

**Color Shift** rotates the U and V chrominance channels of the feedback signal with each pass through the buffer. At 0%, no color rotation occurs: trails maintain the original hue. As Color Shift increases, each feedback iteration rotates the color further, producing rainbow-hued trails that cycle through the spectrum. At 100%, the rotation is at full strength, and feedback trails shift aggressively through complementary colors.

The rotation is implemented as a weighted crossfade between the U and V channels: U picks up some of V's energy, while V picks up the inverse of U, creating a smooth hue rotation rather than a hard swap.

---

### Knob 4 — Decay

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 68% |

**Decay** controls the blend ratio between the feedback buffer and the incoming video. At 0%, the output is entirely new input: no feedback is visible, and the buffer receives only fresh pixels. As Decay increases, the feedback signal dominates: more of the old buffer content persists, and less of the new input breaks through. At 100%, the output is nearly pure feedback with almost no new input entering the system.

:::note
Decay is the master control for feedback intensity. It determines how many "generations" of the image remain visible. Low Decay creates a single faint echo. High Decay creates deep, persistent tunnels where dozens of iterations stack on top of each other.
:::

---

### Knob 5 — X Offset

| Property | Value |
|----------|-------|
| Range | -100% – 100% |
| Default | 0% |

**X Offset** sets a base horizontal displacement added to the read address computation. At the center position (displayed as 0%), there is no additional offset: the feedback reads from the position determined solely by Zoom. Turning counterclockwise shifts the read position in one direction; turning clockwise shifts it the other way. Together with Zoom, X Offset defines where on the scanline the feedback buffer looks to read its recursive data.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** applies an overall brightness offset to the processed output after the feedback blend. At center (displayed as 50%), no adjustment is applied. Turning counterclockwise darkens the output; turning clockwise brightens it. This is a simple additive offset: it shifts the entire luminance range up or down without affecting chroma.

---

### Switch 7 — Direction

| Property | Value |
|----------|-------|
| Off | Right |
| On | Left |
| Default | Right |

**Direction** selects whether the spatial offset is subtracted from or added to the write pointer when computing the feedback read address. Set to **Right**, the feedback reads from pixels behind the current write position, creating trails that flow rightward. Set to **Left**, it reads from pixels ahead of the write position, reversing the tunnel direction. Direction fundamentally changes the character of the feedback pattern: the same Zoom and X Offset settings produce mirrored spatial behavior depending on this toggle.

---

### Switch 8 — Mirror

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mirror** enables horizontal bilateral symmetry in the feedback path. When set to **Off**, the feedback read address is used directly. When set to **On**, the read address is averaged with its horizontal complement, causing the left and right halves of the feedback pattern to reflect each other. The result is a ***kaleidoscope*** effect where the recursive tunnel develops symmetrical structure.

:::tip
Mirror combined with high Color Shift creates spectacular symmetrical color wheels. The bilateral symmetry organizes the color rotation into structured, mandala-like patterns.
:::

---

### Switch 9 — Freeze

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Freeze** holds the contents of the line buffers, preventing new input from being written. When set to **Off**, each pixel's blended result is written back to the buffer normally, and the feedback evolves continuously. When set to **On**, the write enable is suppressed: the buffer retains its last written state, and the feedback reads stale data. The output still processes and displays the frozen buffer contents blended with the current input, but the buffer itself no longer updates.

---

### Switch 10 — Invert Y

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert Y** applies a bitwise complement to the luminance channel of the incoming video before it enters the feedback pipeline. This inverts the brightness of the input signal on its way into the buffer. Because the inversion occurs before the feedback blend, it affects the data that gets recursively fed back (dark regions become bright in the buffer, and vice versa.)

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Feedback processing. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the feedback-processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the wet/dry blend between the processed feedback output and the original input signal. At 0% (fader fully down), only the delayed dry signal passes through: no feedback is audible. At 100% (fader fully up), only the processed feedback signal appears in the output. Intermediate positions blend the two, allowing you to layer the feedback effect over the clean source at any desired intensity.

---

## Background

### Video feedback as art

Video feedback: the phenomenon of pointing a camera at its own monitor: has been a cornerstone of video art since the medium's earliest days. In the late 1960s, artists discovered that the recursive loop between camera and screen could generate complex, organic patterns without any external input. The image feeds into itself, and each pass through the loop transforms the signal: zooming, rotating, shifting colors, and accumulating distortion.

The results are strikingly similar to fractal geometry, though they predate the widespread use of that term in art. ***Mandelbrot sets***, Julia sets, and other iteratively defined mathematical shapes share the same fundamental principle: a function is applied to its own output, over and over, and the resulting patterns exhibit ***self-similarity*** at multiple scales.

### Line-buffer recursion

Feedback implements iterative self-reference using three horizontal ***line buffers***: one each for the Y, U, and V channels. Each buffer is a 512-entry circular memory (BRAM). As pixels arrive on a scanline, they are written into the buffer at the current write pointer. Simultaneously, pixels are read from a different position in the same buffer, determined by the Zoom and X Offset controls.

The read data: which contains the accumulated result of all previous feedback passes on this scanline: is then blended with the fresh input according to the Decay ratio. The blended result is written back into the buffer, completing the feedback loop. On the next frame, the buffer already contains traces of previous iterations, so those traces are read, amplified, rotated, and blended again.

:::note
Because the feedback operates within a single scanline buffer, the recursion is ***horizontal only***. There is no vertical feedback: each line is processed independently. This is what gives Feedback its characteristic horizontal streak/tunnel appearance rather than the full two-dimensional zoom seen in optical camera-monitor feedback.
:::

### Gain and self-excitation

The Gain parameter amplifies the feedback signal before it enters the blend. At moderate levels, this compensates for the natural decay and keeps trails visible longer. But above a certain threshold: when Gain × Decay exceeds unity: the system becomes ***self-exciting***. Each pass through the loop adds more energy than was lost, and the image rapidly saturates to white.

Self-excitation is not a failure mode; it's a creative tool. The boundary between stable feedback and runaway saturation is a narrow, dynamic region where the image is maximally responsive to parameter changes. Small adjustments to Gain, Decay, or Color Shift can push the system in and out of self-excitation, producing dramatic visual transitions.

### Color rotation

The Color Shift parameter implements a weighted crossfade between the U and V chroma channels on each feedback pass. This is a simplified form of ***hue rotation*** in YUV space. Rather than performing a true trigonometric rotation (which would require sine/cosine tables), Feedback uses a linear cross-mix: U picks up a portion of V's energy proportional to the Color Shift setting, and V picks up the complement of U. The result approximates a smooth color wheel rotation that accumulates with each recursive pass through the buffer.


---

## Signal Flow

### Signal Flow Notes

The critical interaction is the ***feedback loop***: step 5 reads from the buffers, processes the data, and writes the result *back* to the same buffers. This creates iterative recursion: each frame's output becomes the next frame's feedback input. The loop gain is controlled by two parameters: Gain amplifies the feedback signal, and Decay determines how much of it persists versus being replaced by fresh input. When their product exceeds unity, the system self-excites.

Color Shift operates exclusively on the feedback path: it rotates only the U/V data read from the buffer, not the incoming signal. This means color rotation accumulates: the first pass shifts slightly, the second pass shifts further, and so on. Deep tunnels cycle through the entire color wheel.

:::tip
**Freeze captures the feedback state.** When you flip Freeze on, the buffer stops updating but the output still blends the frozen buffer with the live input. This lets you "snapshot" a complex tunnel pattern and overlay it on new source material.
:::


---

## Exercises

These exercises progress from gentle trails to full self-exciting feedback tunnels. Each one engages more of the feedback loop's parameters.
### Exercise 1: Ghost Trails

![Ghost Trails result](/img/instruments/videomancer/feedback/feedback_ex1_s1.png)
*Ghost Trails — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Soft, ghostly echo trails that follow motion in the source video.

#### Key Concepts

- Decay controls how many feedback iterations remain visible
- Zoom creates spatial displacement between iterations
- Direction reverses the displacement polarity

#### Video Source

A live camera feed with a moving subject (a waving hand or slowly panning shot works well.)

#### Steps

1. Set **Decay** (Knob 4) to about 50%. Motion in the source leaves a faint afterimage (you're seeing one or two generations of feedback.)
2. Increase **Zoom** (Knob 1) slightly. The afterimage shifts horizontally, creating a spatial offset between the original and its echo.
3. Increase Decay to 70%. More generations of the echo become visible, and the trail extends further.
4. Flip **Direction** (Switch 7) from **Right** to **Left**. The trail reverses (it now extends in the opposite direction.)
5. Adjust **Brightness** (Knob 6) to compensate if the image is too dark or bright.

#### Settings

| Control | Value |
|---------|-------|
| Zoom | ~20% |
| Gain | ~40% |
| Color Shift | 0% |
| Decay | ~70% |
| X Offset | 0% |
| Brightness | 50% |
| Direction | Right |
| Mirror | Off |
| Freeze | Off |
| Invert Y | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Color Tunnel

![Color Tunnel result](/img/instruments/videomancer/feedback/feedback_ex2_s1.png)
*Color Tunnel — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A symmetrical, color-cycling tunnel with rainbow trails streaming from the source.

#### Key Concepts

- Color Shift rotates hue between feedback iterations
- Mirror creates bilateral kaleidoscope symmetry
- Gain controls trail persistence and self-excitation threshold

#### Video Source

A static image or slow-moving footage with strong shapes and moderate contrast.

#### Steps

1. Start from the Exercise 1 settings, then increase **Zoom** (Knob 1) to about 40%.
2. Turn **Color Shift** (Knob 3) to about 60%. The feedback trail now cycles through hues (each echo is a different color.)
3. Enable **Mirror** (Switch 8). The tunnel becomes symmetrical, folding the feedback pattern across the horizontal center.
4. Increase **Gain** (Knob 2) to about 55%. The trails brighten and persist longer. If the image starts to blow out, back off Gain slightly.
5. Sweep **X Offset** (Knob 5) slowly. The tunnel's center of symmetry shifts left and right.
6. Toggle **Invert Y** (Switch 10). The brightness relationship reverses: dark areas of the source now drive the bright parts of the tunnel.

#### Settings

| Control | Value |
|---------|-------|
| Zoom | ~40% |
| Gain | ~55% |
| Color Shift | ~60% |
| Decay | ~80% |
| X Offset | ~75% |
| Brightness | 50% |
| Direction | Right |
| Mirror | On |
| Freeze | Off |
| Invert Y | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Self-Exciting Explosion

![Self-Exciting Explosion result](/img/instruments/videomancer/feedback/feedback_ex3_s1.png)
*Self-Exciting Explosion — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Push the feedback loop into self-excitation, then freeze the result and overlay it on live video.

#### Key Concepts

- Self-excitation occurs when gain × decay exceeds unity
- Freeze captures the feedback state for overlay
- The boundary between stability and runaway saturation is the most expressive region

#### Video Source

Any video source. High-contrast material with strong edges works best for dramatic tunnel structures before self-excitation.

#### Steps

1. Set **Decay** (Knob 4) to about 60% and **Gain** (Knob 2) to about 80%. The system should be on the edge of self-excitation: trails are bright and persistent but the image hasn't blown out yet.
2. Turn **Color Shift** (Knob 3) to about 40%. Rainbow cycling adds visual interest to the tunnel.
3. Slowly increase Gain until the image begins to saturate and blow out in places. You've crossed the self-excitation threshold.
4. Quickly flip **Freeze** (Switch 9) to **On**. The buffer holds the explosive pattern.
5. Reduce **Decay** to about 30%. The frozen tunnel pattern now overlays the live input at reduced intensity: you can see the source video showing through the frozen feedback.
6. Adjust **Mix** (Fader 12) to find the blend between the frozen feedback texture and the clean source.
7. Flip Freeze **Off** to release the buffer and let the feedback evolve again.

#### Settings

| Control | Value |
|---------|-------|
| Zoom | ~60% |
| Gain | ~80% |
| Color Shift | ~40% |
| Decay | ~60% |
| X Offset | ~55% |
| Brightness | ~45% |
| Direction | Right |
| Mirror | Off |
| Freeze | Off |
| Invert Y | Off |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **BRAM**: Block RAM; dedicated memory blocks embedded in the FPGA fabric, used here as scanline-wide circular buffers for the Y, U, and V channels.

- **Circular Buffer**: A fixed-size memory where the write pointer wraps around to the beginning when it reaches the end, creating a continuously overwritten loop.

- **Decay**: The blend ratio between the feedback buffer contents and the incoming video; higher decay means more of the old signal persists.

- **Feedback Loop**: A system where the output is routed back to the input, creating iterative self-reference and accumulation of successive transformations.

- **Hue Rotation**: Shifting the color of a signal around the color wheel by cross-mixing the U and V chrominance components.

- **Line Buffer**: A memory that stores one horizontal scanline of video data, enabling pixel-by-pixel read/write operations within the same line.

- **Self-Excitation**: A condition where the feedback loop's gain exceeds its losses, causing the signal to grow without bound until it saturates.

- **Self-Similarity**: A property of patterns that look similar at different scales, characteristic of fractals and iterative feedback systems.

- **Video Feedback**: The optical phenomenon created by pointing a camera at a monitor displaying the camera's own output, producing recursive, fractal-like imagery.

---
