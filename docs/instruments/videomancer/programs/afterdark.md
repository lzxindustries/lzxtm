---
draft: true
sidebar_position: 1
slug: /instruments/videomancer/afterdark
title: "Afterdark"
image: /img/instruments/videomancer/afterdark/afterdark_hero.png
description: "Before screensavers were quaint nostalgia, they were engineering necessities."
---

![Afterdark hero image](/img/instruments/videomancer/afterdark/afterdark_hero_s1.png)
*A luminous rectangle drifts across a black void, bouncing off invisible walls and leaving color-cycling trails in its wake.*

---

## Overview

**Afterdark** is a synthesis program that conjures a solitary, bouncing rectangular sprite on a black canvas. The shape drifts across the screen at a steady pace, reflecting off the edges of the frame when bounce is enabled. Its color can be fixed or continuously cycling through shifting hues driven by an internal frame counter. The result is a living, geometric animation: part nostalgia, part hypnotic screensaver, part building block for layered video compositions.

Because Afterdark is a ***synthesis*** program, it generates imagery from scratch rather than processing an external video input. The interpolator mix stage blends the synthesized shape against whatever signal arrives on the input: typically black: so the **Brightness** fader effectively controls the overall opacity of the generated output. At full brightness, the bouncing rectangle stands alone; at lower values, it fades toward transparency, useful when Afterdark feeds downstream processing programs.

:::note
Several parameters: **Speed**, **Shape**, **Trail**, **Rotate**, and the **Gravity** switch: are mapped to hardware controls but are reserved for a future firmware update. In the current version, the shape is always a rectangle, moves at a fixed velocity, and does not rotate or leave persistent trails. These controls are documented below so you know what each knob and switch is named on your panel.
:::

### What's In a Name?

The name ***Afterdark*** is an homage to ***After Dark***, the iconic screensaver software released in 1989 by Berkeley Systems. After Dark shipped dozens of animated modules: flying toasters, starfields, bouncing shapes: that danced across CRT monitors to prevent ***phosphor burn-in***. Afterdark channels that same spirit: a simple geometric shape bouncing endlessly inside a frame, a miniature universe governed by nothing but velocity and reflection. The lowercase, single-word spelling is a nod to the program naming convention, but the cultural reference is unmistakable.

---

## Quick Start

1. Push the **Brightness** fader (Fader 12) to about 75%. A bright rectangle appears against a black background, drifting across the screen.
2. Confirm **Bounce** (Switch 7) is set to **On**. The rectangle reflects off the edges of the frame, reversing direction each time it hits a wall.
3. Confirm **Color Cycle** (Switch 8) is set to **On**. The rectangle's hue shifts continuously: blues sliding into greens sliding into magentas: driven by an internal frame counter.
4. Turn **Size** (Knob 2) clockwise to enlarge the rectangle, or counterclockwise to shrink it down to a small, darting square.

---

## Parameters

![Videomancer front panel with Afterdark loaded](/img/instruments/videomancer/afterdark/afterdark_control_panel.png)
*Videomancer's front panel with Afterdark active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Speed** is reserved for a future update. In the current firmware, the shape moves at a fixed velocity of two pixels per frame horizontally and one pixel per frame vertically. Turning this knob has no visible effect.

---

### Knob 2 — Size

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Size** controls the dimensions of the rectangular sprite. The shape is always square: width and height are equal. At minimum, the rectangle shrinks to a tiny dot. As you turn the knob clockwise, the shape grows. Internally, the half-width is derived from the upper eight bits of the parameter value, yielding a range of roughly 0 to 255 pixels per side.

:::tip
Very small sizes create a fast-moving pixel that's easy to lose on a large display. Very large sizes fill most of the frame, turning Afterdark into a pulsing, full-screen color field.
:::

---

### Knob 3 — Color

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Color** sets the hue of the rectangle when **Color Cycle** (Switch 8) is turned off. Internally, the U chrominance channel is set directly to the Color value while the V channel is set to the complement (maximum minus Color). Sweeping the knob rotates through a spectrum of hues: from cool blue-cyans at low values through warm reds and magentas at high values. At mid-position, the U and V channels are roughly balanced, producing a neutral or desaturated tone.

:::note
When **Color Cycle** is enabled, this knob has no effect (the cycling animation overrides the static color.)
:::

---

### Knob 4 — Shape

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 2 |

**Shape** is reserved for a future update. The control uses an eight-step mode suggesting eight planned shape variants, but in the current firmware only a rectangle is generated. Turning this knob has no visible effect.

---

### Knob 5 — Trail

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Trail** is reserved for a future update. In the current firmware, no persistence or decay trail is applied: the rectangle appears cleanly against the background with no ghosting or afterimage. Turning this knob has no visible effect.

---

### Knob 6 — Gravity

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Gravity** controls the luminance (brightness) of the rectangular sprite's fill. At 0%, the shape is near-black: almost invisible against the black background. As you increase the value, the shape brightens. At 100%, it reaches maximum luminance. Despite its name, this parameter does not apply gravitational physics to the shape's motion; it functions purely as a fill brightness control.

:::tip
At its default value of 0%, the rectangle is nearly invisible unless **Color Cycle** is enabled, which still tints the dark shape with shifting chrominance. Push the knob up to see the shape clearly.
:::

---

### Switch 7 — Bounce

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Bounce** enables edge reflection. When set to **On**, the rectangle reverses its horizontal or vertical velocity each time its center crosses predefined screen boundaries (approximately 80–1200 pixels horizontally, 70–650 pixels vertically). The shape ping-pongs endlessly within the frame. When set to **Off**, the rectangle drifts past the edges and eventually wraps around, re-entering from the opposite side after traversing offscreen coordinates.

---

### Switch 8 — Color Cycle

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Color Cycle** switches between static and animated coloring. When **On**, the U and V chrominance channels are derived from the internal frame counter, producing a continuously shifting hue that cycles through the color spectrum as frames advance. The cycling speed is tied to the frame rate: it progresses by one step per frame and repeats after 256 frames. When **Off**, the shape uses the static hue set by the **Color** knob (Knob 3).

---

### Switch 9 — Rotate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Rotate** is reserved for a future update. In the current firmware, the rectangle does not rotate. Toggling this switch has no visible effect.

---

### Switch 10 — Gravity

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Gravity** (the switch, distinct from the knob) is reserved for a future update. It is intended to enable gravitational acceleration on the shape's vertical motion, but in the current firmware toggling this switch has no visible effect.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the delayed input signal directly to the output, bypassing all synthesis and mixing stages. The sync delay pipeline still aligns timing, so switching between bypass and active modes produces no glitch. Use Bypass for instant comparison between the raw input and the synthesized output.

---

### Fader 12 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Brightness** controls the wet/dry mix between the input video signal and the synthesized shape. At 0%, the output is the unaltered input: no synthesized content is visible. As the fader is pushed upward, the bouncing rectangle fades in over the input. At 100%, the output is entirely the synthesized shape: rectangle against black. For typical use as a standalone synthesizer, keep this fader high.

:::tip
When chaining Afterdark into another program, **Brightness** becomes an opacity control. Lower values produce a subtle, ghostly overlay of the bouncing rectangle on top of whatever the next program generates.
:::

---

## Background

### Screensavers and CRT phosphor burn-in

Before LCD panels replaced cathode-ray tubes, static images posed a real threat to display hardware. A CRT works by firing an electron beam at a phosphor-coated glass surface. Regions struck repeatedly with high-intensity content would permanently degrade: the phosphor would lose its ability to glow, leaving a faint ghost of the burned-in image visible forever. This phenomenon is called ***phosphor burn-in***.

***Screensavers*** emerged in the 1980s as a software solution: when a computer sat idle, an animated pattern would take over the display, continuously moving bright areas around the screen to distribute phosphor wear evenly. Berkeley Systems' ***After Dark*** (1989) turned this utilitarian concept into entertainment, shipping dozens of whimsical animation modules: flying toasters being the most famous. Afterdark channels the simplest and most archetypal screensaver: a colored shape bouncing endlessly inside a rectangular boundary.

### Velocity, reflection, and the laws of the frame

Afterdark's motion model is intentionally primitive. The shape has a fixed velocity vector: two pixels per frame rightward, one pixel per frame downward. When **Bounce** is enabled, the shape reflects off invisible walls: its horizontal velocity reverses when it crosses the left or right boundary, and its vertical velocity reverses at the top or bottom boundary. This produces the classic billiard-ball trajectory, tracing a repeating diagonal path that eventually visits every region of the screen.

Because the velocity is fixed and the boundary checks happen once per frame (at the vertical sync pulse), the trajectory is ***deterministic***: it follows the same path every time Afterdark starts. The shape always begins at position (200, 150) and always moves in the same direction. This predictability is a feature: the animation is a reliable, repeatable signal that can be synchronized or layered with other programs.

### Color cycling and the frame counter

When **Color Cycle** is enabled, the rectangle's hue is derived from an internal 16-bit frame counter that increments once per vertical sync. The U channel receives the upper bits of the counter while the V channel receives the lower bits, creating a continuously shifting two-axis color trajectory through the YUV color space. Because U and V advance at different rates (the U cycle is four times slower than V), the resulting color sequence is not a simple rainbow: it traces a more complex Lissajous-like path through the chroma plane, producing unexpected hue combinations.


---

## Signal Flow

### Signal Flow Notes

The pipeline begins with ***timing detection***: edges of hsync and vsync are detected and used to drive XY pixel counters. At the start of each new frame (vsync falling edge), the shape's position is updated by adding the fixed velocity vector. If **Bounce** is enabled, the velocity components are negated when the position crosses the screen boundaries.

The ***shape hit test*** runs every pixel clock, computing the signed distance from the current pixel to the shape's center and comparing against the half-size derived from the **Size** knob. Pixels inside the rectangle receive the synthesized color; pixels outside receive near-black with neutral chroma. This synthesized frame is then blended with the delayed input video through three parallel ***interpolator*** instances: one per YUV channel: controlled by the **Brightness** fader. The final output passes through a bypass mux for A/B comparison.

:::note
The input video is delayed by 8 clocks through a shift-register pipeline to align with the processing latency. This ensures the interpolator receives time-aligned data from both the input and the synthesizer.
:::


---

## Exercises

These exercises explore the working controls of Afterdark, progressing from a basic bouncing rectangle to creative compositions using color cycling and mix blending.
### Exercise 1: The Classic Bounce

![The Classic Bounce result](/img/instruments/videomancer/afterdark/afterdark_ex1_s1.png)
*The Classic Bounce — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A single, bright rectangle bouncing endlessly inside the frame (the archetypal screensaver animation.)

#### Key Concepts

- Afterdark is a synthesis program (it generates imagery, not processes it)
- Bounce reflection creates a deterministic billiard-ball trajectory
- Size controls the sprite dimensions

#### Steps

1. Push the **Brightness** fader (Fader 12) to maximum. A rectangle appears against black.
2. Turn **Gravity** (Knob 6): the shape brightness control: to about 75%. The rectangle is now clearly visible.
3. Set **Bounce** (Switch 7) to **On**. Watch the rectangle drift and reflect off the screen edges.
4. Sweep **Size** (Knob 2) from minimum to maximum and back. At small sizes, the rectangle is a darting square. At large sizes, it fills most of the frame.
5. Set **Color Cycle** (Switch 8) to **Off**, then sweep **Color** (Knob 3) slowly. The rectangle's hue shifts across the spectrum.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 50% |
| Size | ~40% |
| Color | 50% |
| Shape | 0 |
| Trail | 0% |
| Gravity | 75% |
| Bounce | On |
| Color Cycle | Off |
| Rotate | Off |
| Gravity (Switch) | Off |
| Bypass | Off |
| Brightness | 100% |

---

### Exercise 2: Color Cycling Light Show

![Color Cycling Light Show result](/img/instruments/videomancer/afterdark/afterdark_ex2_s1.png)
*Color Cycling Light Show — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A bouncing rectangle with continuously shifting, psychedelic colors.

#### Key Concepts

- Color cycling derives hue from the frame counter
- U and V channels cycle at different rates, creating complex color paths
- Brightness fader controls opacity when layered

#### Steps

1. Start from the Exercise 1 settings.
2. Enable **Color Cycle** (Switch 8). The rectangle's hue begins shifting automatically: notice how the color doesn't simply loop through a rainbow but traces a more complex path through blues, greens, magentas, and yellows.
3. Increase **Size** (Knob 2) to about 60%. The larger shape makes the color shifts more dramatic and easier to observe.
4. Increase **Gravity** (Knob 6) to maximum. The shape is now at full brightness, making the color cycling vivid.
5. Lower **Brightness** (Fader 12) to about 40%. The rectangle becomes a translucent, glowing overlay (useful when this output feeds into another program.)

#### Settings

| Control | Value |
|---------|-------|
| Speed | 50% |
| Size | ~60% |
| Color | 50% |
| Shape | 0 |
| Trail | 0% |
| Gravity | 100% |
| Bounce | On |
| Color Cycle | On |
| Rotate | Off |
| Gravity (Switch) | Off |
| Bypass | Off |
| Brightness | 40% |

---

### Exercise 3: Abstract Geometry

![Abstract Geometry result](/img/instruments/videomancer/afterdark/afterdark_ex3_s1.png)
*Abstract Geometry — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An abstract, slow-morphing color field that oscillates across the frame.

#### Key Concepts

- Very large shapes approach full-screen color fields
- Bounce off creates wrap-around drift
- Mixing with input creates layered compositions

#### Steps

1. Turn **Size** (Knob 2) to maximum. The rectangle fills nearly the entire screen. It's no longer a small bouncing sprite (it's a massive color plane that slides in and out of view.)
2. Set **Bounce** (Switch 7) to **Off**. The shape no longer reflects: it drifts off one edge and re-enters from the opposite side, creating a wipe-like transition each time it crosses a boundary.
3. Enable **Color Cycle** (Switch 8) for continuously shifting hues.
4. Set **Gravity** (Knob 6) to about 50% for a medium-brightness fill.
5. Set **Brightness** (Fader 12) to about 60%. The shape is semi-transparent, blending with any signal arriving on the input.
6. If you have a second program feeding into Afterdark's input, the color field overlays the incoming image. Sweep **Brightness** to find the balance point between the two layers.

#### Settings

| Control | Value |
|---------|-------|
| Speed | 50% |
| Size | 100% |
| Color | 50% |
| Shape | 0 |
| Trail | 0% |
| Gravity | 50% |
| Bounce | Off |
| Color Cycle | On |
| Rotate | Off |
| Gravity (Switch) | Off |
| Bypass | Off |
| Brightness | 60% |

---
## Glossary

- **Bounce**: Edge reflection: the shape reverses direction when it reaches a screen boundary, producing a billiard-ball trajectory.

- **Chrominance**: The color component of a video signal, encoded as U and V channels in YUV color space. Neutral chrominance (U=V=512) produces a grayscale image.

- **Color Cycling**: Automatically animating the color of a graphic element over time, typically by incrementing an index through a color palette or color space.

- **Frame Counter**: An internal register that increments once per video frame (vertical sync), used to drive time-varying animations like color cycling.

- **Interpolator**: A hardware mixing stage that blends two input values according to a parameter. At t=0, output equals input A; at t=maximum, output equals input B; between, a weighted average.

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Phosphor Burn-in**: Permanent degradation of a CRT display's phosphor coating caused by prolonged display of a static, high-intensity image.

- **Screensaver**: An animated program that activates during idle periods to prevent phosphor burn-in on CRT displays, later becoming a form of digital decoration.

- **Sprite**: A small, independently movable graphic element composited over a background (borrowed from the vocabulary of 2D game hardware.)

- **Synthesis**: Generation of video imagery from scratch, as opposed to processing an existing video signal.

- **Velocity Vector**: A pair of values (horizontal, vertical) describing the speed and direction of motion per frame.

- **YUV**: A color encoding system that separates luminance (Y) from chrominance (U, V), used in video signal processing.

---
