---
draft: true
sidebar_position: 39
slug: /instruments/videomancer/cascade
title: "Cascade"
image: /img/instruments/videomancer/cascade/cascade_hero_s1.png
description: "A CRT phosphor does not turn off instantly."
---

![Cascade hero image](/img/instruments/videomancer/cascade/cascade_hero_s1.png)
*Cascade painting luminance-tinted scanline echoes across the frame, each trail displaced and colored like light refracting through a prism of time.*

---

## Overview

Cascade is a scanline echo and trail generator. It stores each line of incoming video in a dual-bank memory buffer and reads it back at a configurable offset, producing horizontal displacement echoes that streak across the image like afterimages burned into a phosphor screen. Two independent echo taps alternate line by line, creating layered, interleaved trails at different displacements. The echoed signal can be tinted per channel: adjusting brightness, shifting hue: so that each trail carries its own color signature.

The program's personality emerges from three interlocking features. First, ***feedback*** routes the mixed output back into the delay buffer, causing echoes to accumulate and evolve over time. Second, ***mirror read*** reverses the direction the buffer is read, folding the echo into a palindrome pattern. Third, ***luma modulation*** bends the echo displacement based on the brightness of the source image, so that bright regions echo at a different offset than dark regions.

At gentle settings, Cascade adds subtle trailing afterimages and phosphor-like persistence. At extreme settings, it tears the image apart into interlocking ribbons of displaced color, stuttering and smearing across the frame in rhythmic waves.

:::tip
***Feedback is the key to Cascade's deepest textures.*** Without it, you get clean displaced echoes. With it, echoes accumulate into dense, evolving textures that respond to every control change.
:::

### What's In a Name?

The name ***Cascade*** refers to a waterfall of repeating echoes, each one displaced further from the original and tinted with its own color: like water spilling over ledges in a terraced falls. It also references the engineering concept of ***cascaded stages***, where the output of one process feeds the input of the next, which is exactly what feedback mode does.

---

## Quick Start

1. Push **Echo Mix** (Fader 12) to about 75%. Turn **Echo Delay** (Knob 1) clockwise to about 40%. You'll see a displaced copy of the image overlaid on the original, shifted horizontally.
2. Turn **Echo Y Tint** (Knob 4) counter-clockwise. The echo copy darkens, creating a shadow trail. Turn it clockwise past center and the echo brightens.
3. Turn up **Echo U Tint** (Knob 5) and **Echo V Tint** (Knob 6) to shift the echo's color. The original image retains its true colors while the echo takes on a tinted hue.
4. Flip **Feedback** (Switch 7) to **On**. The echo feeds back into itself, building up iterative trails that compound and evolve. Adjust **Echo Delay** to change the spacing of the cascading trails.

---

## Parameters

![Videomancer front panel with Cascade loaded](/img/instruments/videomancer/cascade/cascade_control_panel.png)
*Videomancer's front panel with Cascade active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Echo Delay

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Echo Delay** sets the horizontal displacement of the first echo tap. At 0%, the echo reads from nearly the same position as the write head, producing minimal visible displacement. As the value increases, the echo reads further behind the current pixel, stretching the trail across the scan line. At 100%, the offset spans close to the full width of the line buffer. This control defines the basic spacing of the echo effect. Because the two echo taps alternate on successive scan lines, this parameter defines the displacement on every other line.

:::note
The delay is measured in pixels along a scan line, not in time. Even lines use this tap; odd lines use **Echo 2 Delay**. The interleaving creates a woven pattern when the two taps are set to different values.
:::

---

### Knob 2 — Echo 2 Delay

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Echo 2 Delay** sets the horizontal displacement of the second echo tap. It functions identically to **Echo Delay** but operates on alternating scan lines. When both taps are set to the same value, the echo appears uniform across the frame. When set to different values, the two taps create a scanline-interleaved pattern: each line echoes at a different offset, producing a combed or woven texture. Setting one tap to zero and the other to a high value creates a dramatic alternation between untouched and heavily displaced lines.

---

### Knob 3 — Luma Mod

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Luma Mod** modulates both echo tap offsets based on the brightness of the input image. At 0%, both taps read at their fixed offsets. As the value increases, bright pixels push the read offset further while dark pixels keep it closer to zero, bending the echo displacement across the image. At 100%, the modulation is at full strength and the echo trails visibly follow the luminance contours of the source. The result is an ***adaptive displacement*** (bright areas stretch further than dark areas.)

:::tip
Luma Mod interacts with **Luma Invert** (Switch 9). Inverting luminance swaps which regions receive more displacement. Together, they let you sculpt which parts of the image "cascade" and which remain anchored.
:::

---

### Knob 4 — Echo Y Tint

| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |

**Echo Y Tint** controls the brightness gain of the echoed signal. At center (0%), the echo's luminance passes through unchanged: unity gain. Turning counter-clockwise darkens the echo toward black. Turning clockwise brightens the echo, doubling its luminance at the maximum. This control affects only the echo; the dry signal retains its original brightness. Use it to create shadow trails (darkened echo) or glowing afterimages (brightened echo).

---

### Knob 5 — Echo U Tint

| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |

**Echo U Tint** shifts the blue-difference chrominance of the echo signal. At center (0%), no shift is applied. Turning counter-clockwise shifts U toward its negative extreme; turning clockwise shifts it toward its positive extreme. Combined with **Echo V Tint**, this control lets you apply an arbitrary color cast to the echoed image while leaving the dry signal untouched. Small offsets create subtle warm or cool tints; large offsets push the echo into vivid, saturated hues.

---

### Knob 6 — Echo V Tint

| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |

**Echo V Tint** shifts the red-difference chrominance of the echo signal. It operates identically to **Echo U Tint** but on the V axis. Together, the U and V tint controls form a two-dimensional color offset. For example, boosting V while reducing U tints the echo toward magenta; the opposite combination tints toward green. At center, both tints are neutral and the echo carries the same color as the source.

:::tip
Setting **Echo Y Tint** below center while shifting **Echo U Tint** and **Echo V Tint** off-center creates deeply tinted shadow trails (like colored ghosts following the image.)
:::

---

### Switch 7 — Feedback

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Feedback** routes the mixed output back into the delay line input, replacing the live video feed. When set to **Off**, the delay line stores the incoming video directly, producing clean single-generation echoes. When set to **On**, each echo pass feeds back into the buffer, causing trails to accumulate iteratively. The echo compounds on itself, growing denser and more saturated with each cycle. Tint controls are applied on every feedback pass, so even small tint offsets accumulate into vivid color shifts over successive generations.

:::warning
Feedback with high **Echo Mix** and bright **Echo Y Tint** can saturate the image to white. Pull **Echo Y Tint** slightly below center to create decaying trails that fade over time rather than building up.
:::

---

### Switch 8 — Mirror Read

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mirror Read** reverses the read direction of echo tap A in the delay line buffer. When set to **Off**, the buffer is read in the same direction it was written: left to right. When set to **On**, the buffer is read in reverse: right to left. This flips the echo horizontally, creating a palindrome or kaleidoscopic effect where the echo is a mirror image of the source. Combined with feedback, mirror read produces symmetrical textures that fold and unfold across the center of the frame.

---

### Switch 9 — Luma Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Luma Invert** flips the brightness of the input signal before it enters the processing chain. When set to **Off**, luminance passes through normally. When set to **On**, luminance is bitwise-complemented: bright becomes dark and dark becomes bright. Because this happens at the very first stage, it affects everything downstream: the image stored in the delay line is inverted, the luma modulation offset is computed from inverted brightness, and the feedback loop accumulates inverted data.

---

### Switch 10 — Freeze

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Freeze** holds the current contents of the delay line buffer, preventing new data from being written. When set to **Off**, the buffer updates continuously with incoming video (or feedback output). When set to **On**, the buffer stops accepting new data and replays its stored contents indefinitely. The echoed output becomes a static, looping pattern frozen at the moment the switch was engaged. Combined with **Echo Mix** and the tint controls, Freeze turns the buffer into a fixed texture source that can be blended and colored independently of the live input.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Cascade processing stages. The internal sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the echoed result.

---

### Fader 12 — Echo Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Echo Mix** crossfades between the dry (unprocessed) input and the wet (tinted echo) signal. At 0%, the output is purely dry: the echo is inaudible. At 100%, the output is purely the tinted echo, with no dry signal present. At 50%, equal parts dry and wet are blended. This is the master intensity control for the entire echo effect. With feedback active, even moderate Mix values produce strong trails because the feedback loop compounds the echo internally.

---

## Background

### Scanline delay and displacement

Cascade's core mechanism is a ***scanline delay line***: a block of memory (BRAM) that stores one line of video and reads it back at a configurable offset. As each pixel arrives, it's written into the buffer at the current position. Simultaneously, the buffer is read at a position offset by the Echo Delay parameter. The result is a horizontally displaced copy of the scan line, shifted to the left or right depending on the offset value.

The delay line uses a ***dual-bank ping-pong*** architecture. Two memory banks alternate roles: while one bank is being written with the current line, the other is being read to produce the echo. At the start of each new line, the roles swap. This ensures that the echo always reads from a complete, stable line rather than from partially written data.

### Interleaved echo taps

Cascade provides two independent echo taps, each with its own delay offset. Rather than mixing both taps simultaneously, the program interleaves them: even scan lines use **Echo Delay** (tap A), and odd scan lines use **Echo 2 Delay** (tap B). This alternation is driven by a vertical accumulator that toggles a bank-select signal once per scan line.

When both taps are set to the same offset, the interleaving is invisible: every line echoes identically. When the taps differ, the image develops a fine-grained, line-by-line texture. One line might echo 20% across the frame while the next echoes 60%, creating a combed or interlaced displacement pattern.

### Tinting and color trails

After the echo is read from the delay line, it passes through a two-stage ***tint pipeline***. The Y (luma) channel is multiplied by the **Echo Y Tint** value, functioning as a gain control: values below center attenuate, center is unity pass-through, and above center amplifies up to approximately double brightness. The U and V (chroma) channels are shifted by additive offsets derived from **Echo U Tint** and **Echo V Tint**: the center position (512) is neutral, and deviations add or subtract color.

All three tint results are saturated to the valid 10-bit range (0 to 1023) before proceeding to the mix stage. This prevents overflow from creating wrap-around artifacts.

### Feedback accumulation

When **Feedback** is engaged, the mixed output of the previous pixel clock is routed back into the delay line input instead of the live video signal. Each successive echo generation is tinted again, so color offsets and brightness changes compound. A small Y tint reduction below unity causes each echo generation to decay, creating a fading trail. Equal tint values create a steady-state loop. Y tint above unity causes exponential brightening that saturates to white.

The feedback path introduces a one-cycle latency because the previous mix result must be registered before it can be written back. This means the feedback signal is always one pixel behind the current input, adding a subtle diagonal slant to feedback trails.


---

## Signal Flow

### Signal Flow Notes

Two key architectural features define Cascade's behavior:

1. **Feedback before tinting**: The feedback mux sits at the input to the delay line, before tinting is applied. This means each feedback generation is stored as a pre-tint signal. The tint is then applied fresh on every readout. The consequence is that tint changes affect all accumulated feedback generations simultaneously: adjusting the tint knobs "recolors" the entire trail history in real time.

2. **Interleaved tap selection**: The two echo taps share a single delay line output, selected per scan line by the vertical accumulator. This is not a blend: it's a hard switch. Each line sees exactly one tap. This creates the characteristic combed texture when the taps are set to different offsets, and it means that feedback on even lines accumulates through tap A while feedback on odd lines accumulates through tap B.

:::tip
**The mix interpolator determines what "dry" means.** At full dry (Echo Mix = 0%), you see the input delayed by the sync pipeline. At full wet (100%), you see only the tinted echo. At intermediate values, the dry input anchors the echo in place, providing spatial reference. With feedback, moderate mix values produce cleaner trails because the dry signal "refreshes" the image each frame.
:::


---

## Exercises

These exercises progress from clean displacement echoes through tinted afterimages to dense feedback textures. Each one builds on the interactions explored in the previous exercise.
### Exercise 1: Displacement Echo

![Displacement Echo result](/img/instruments/videomancer/cascade/cascade_ex1_s1.png)
*Displacement Echo — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean, split-echo displacement effect with visible line-by-line interleaving and brightness-adaptive offset.

#### Key Concepts

- The delay line produces horizontal displacement
- Two taps interleave on alternating scan lines
- Luma modulation bends the displacement

#### Video Source

A live camera feed or recorded footage with strong vertical edges and varied brightness (a backlit subject works well.)

#### Steps

1. **Single echo**: Set **Echo Mix** (Fader 12) to about 75%. Turn **Echo Delay** (Knob 1) clockwise to about 40%. A displaced copy of the image appears, shifted horizontally.
2. **Second tap**: Turn **Echo 2 Delay** (Knob 2) to a different value: try about 15%. Notice how alternating scan lines now show different displacements, creating a fine-combed texture.
3. **Matched taps**: Set both Echo Delay and Echo 2 Delay to the same value. The combing disappears and the echo is uniform across all lines.
4. **Luma modulation**: Turn up **Luma Mod** (Knob 3). Bright areas displace further than dark areas. The echo bends around brightness contours in the source.
5. **Inversion**: Flip **Luma Invert** (Switch 9) to **On**. Dark areas now displace further and bright areas stay anchored. Flip it back.

#### Settings

| Control | Value |
|---------|-------|
| Echo Delay | ~40% |
| Echo 2 Delay | ~15% |
| Luma Mod | ~60% |
| Echo Y Tint | 0% |
| Echo U Tint | 0% |
| Echo V Tint | 0% |
| Feedback | Off |
| Mirror Read | Off |
| Luma Invert | Off |
| Freeze | Off |
| Bypass | Off |
| Echo Mix | ~75% |

---

### Exercise 2: Phosphor Afterimage

![Phosphor Afterimage result](/img/instruments/videomancer/cascade/cascade_ex2_s1.png)
*Phosphor Afterimage — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A CRT-style phosphor persistence effect with colored afterimage trails that decay behind moving objects.

#### Key Concepts

- Y tint controls echo brightness (multiply)
- U/V tint controls shift echo color (additive offset)
- Tint affects only the echo, not the dry signal

#### Video Source

Footage with slow or moderate motion (a hand waving, a pendulum, or scrolling text.)

#### Steps

1. **Dim echo**: Set **Echo Delay** (Knob 1) to about 30% and **Echo Mix** (Fader 12) to about 50%. Turn **Echo Y Tint** (Knob 4) counter-clockwise to about −50%. The echo darkens into a shadow trail.
2. **Color the ghost**: Turn **Echo U Tint** (Knob 5) clockwise to about 30% and **Echo V Tint** (Knob 6) counter-clockwise to about −30%. The shadow trail takes on a cool blue-green tint, like a decaying CRT phosphor.
3. **Warm trail**: Now reverse: turn Echo U Tint counter-clockwise and Echo V Tint clockwise. The trail shifts to warm amber-orange.
4. **Mirror the echo**: Flip **Mirror Read** (Switch 8) to **On**. The echo reverses direction, creating a mirrored afterimage that extends in the opposite direction from the source motion.
5. **Match taps**: Set **Echo 2 Delay** (Knob 2) to a similar value as Echo Delay. The trail smooths out across all scan lines.

#### Settings

| Control | Value |
|---------|-------|
| Echo Delay | ~30% |
| Echo 2 Delay | ~30% |
| Luma Mod | 0% |
| Echo Y Tint | ~−50% |
| Echo U Tint | ~30% |
| Echo V Tint | ~−30% |
| Feedback | Off |
| Mirror Read | On |
| Luma Invert | Off |
| Freeze | Off |
| Bypass | Off |
| Echo Mix | ~50% |

---

### Exercise 3: Feedback Cascade

![Feedback Cascade result](/img/instruments/videomancer/cascade/cascade_ex3_s1.png)
*Feedback Cascade — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dense, evolving feedback texture with compounding color shifts and a frozen snapshot captured mid-cascade.

#### Key Concepts

- Feedback routes mixed output back into the delay line
- Tint values compound across feedback generations
- Freeze captures a moment and holds it indefinitely

#### Video Source

Any footage with motion: geometric patterns, rotating shapes, or hand gestures produce striking results.

#### Steps

1. **Enable feedback**: Set **Echo Delay** (Knob 1) to about 50%, **Echo Mix** (Fader 12) to about 70%, and flip **Feedback** (Switch 7) to **On**. Trails begin compounding, building up into dense streaks.
2. **Decaying tint**: Pull **Echo Y Tint** (Knob 4) slightly below center to about −10%. Each feedback generation dims slightly, creating a natural decay curve.
3. **Color accumulation**: Push **Echo U Tint** (Knob 5) and **Echo V Tint** (Knob 6) off-center by small amounts. Even small shifts accumulate rapidly through feedback (after a few generations, the trails carry vivid color.)
4. **Offset the second tap**: Set **Echo 2 Delay** (Knob 2) to a distinctly different value, about 80%. The interleaved taps create two competing feedback streams at different spacings.
5. **Luma-modulated feedback**: Turn up **Luma Mod** (Knob 3) to about 40%. The feedback trails bend according to image brightness, creating curved, flowing echo patterns.
6. **Freeze the moment**: When the feedback texture reaches an interesting state, flip **Freeze** (Switch 10) to **On**. The buffer holds its contents. Adjust the tint knobs to recolor the frozen pattern in real time (the tint pipeline still processes the stored data.)
7. **Release**: Flip Freeze back to **Off** and watch the feedback cascade resume from the frozen state.

#### Settings

| Control | Value |
|---------|-------|
| Echo Delay | ~50% |
| Echo 2 Delay | ~80% |
| Luma Mod | ~40% |
| Echo Y Tint | ~−10% |
| Echo U Tint | ~15% |
| Echo V Tint | ~−15% |
| Feedback | On |
| Mirror Read | Off |
| Luma Invert | Off |
| Freeze | Off |
| Bypass | Off |
| Echo Mix | ~70% |

---
## Glossary

- **BRAM**: Block RAM; dedicated memory blocks within the FPGA used to store scan line data for delay and echo effects.

- **Delay Line**: A memory buffer that stores incoming data and reads it back at a later position, producing a time- or position-shifted copy of the signal.

- **Displacement**: Shifting an image horizontally by reading scan line data at an offset from where it was written.

- **Feedback**: Routing the processed output back into the input, causing effects to compound and accumulate across successive passes.

- **Interpolation**: Blending between two values using a mix parameter; Cascade uses this for the dry/wet crossfade.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness.

- **Mirror Read**: Reversing the read direction of a delay line buffer, producing a horizontally flipped copy of the stored data.

- **Ping-Pong Buffer**: A dual-bank memory architecture where two buffers alternate between reading and writing roles, ensuring stable readout.

- **Saturation (signal)**: Clamping a computed value to a valid range (0 to 1023) to prevent overflow or underflow artifacts.

- **Scan Line**: A single horizontal row of pixels in a video frame, traced left to right by the display beam.

- **Tint**: A per-channel brightness or color offset applied to the echo signal, coloring the displaced copy independently of the source.

---
