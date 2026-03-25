---
draft: true
sidebar_position: 319
slug: /instruments/videomancer/vectorscope
title: "Vectorscope"
image: /img/instruments/videomancer/vectorscope/vectorscope_hero_s1.png
description: "Vectorscope implements a real-time chrominance analysis display, plotting each pixel's U and V color coordinates as a dot on a two-dimensional grid."
---

![Vectorscope hero image](/img/instruments/videomancer/vectorscope/vectorscope_hero_s1.png)
*A broadcast vectorscope glowing to life in phosphor green, painting the chrominance anatomy of every frame as a constellation of luminous dots.*

---

## Overview

Vectorscope is a real-time chrominance analysis display that transforms Videomancer into a piece of broadcast test equipment. It plots the color content of every incoming video frame as a scatter of luminous dots on a two-dimensional grid, where horizontal position represents the blue-difference axis and vertical position represents the red-difference axis. Areas of the image that share similar hues cluster together on the display; saturated colors push dots outward from the center, while neutral tones converge at the crosshair. The result is a living, breathing map of color activity, rendered in glowing phosphor tones.

At its heart, Vectorscope maintains a 64×64 accumulation grid stored in block RAM. Each incoming pixel's chrominance values select a cell in the grid, and that cell's brightness is incremented: the more pixels that share the same color, the brighter the dot glows. Between frames, every cell decays according to the **Persist** parameter, creating the warm, fading afterglow of a phosphor display. The scope occupies a 64-pixel square region centered on screen, with an optional crosshair ***graticule*** and a choice of four phosphor colors.

:::tip
Vectorscope can serve double duty. Use it as a diagnostic tool to monitor color balance and saturation in a live signal chain, or crank up the persistence and intensity to create an abstract light painting from your video's color content.
:::

### What's In a Name?

A ***vectorscope*** is a standard piece of broadcast test equipment dating to the early days of color television. The name comes from the fact that a color signal can be represented as a two-dimensional ***vector***: its angle indicates hue and its length indicates saturation. The word ***scope***, from the Greek *skopein* (to look at), ties it to the family of oscilloscopes, waveform monitors, and other instruments that make invisible electrical signals visible. Videomancer's Vectorscope brings this broadcast engineering heritage onto the hardware as both a faithful analysis tool and a creative phosphor display.

---

## Quick Start

1. Connect a color video source: color bars, a camera feed, or any material with visible hue variation. The small scope display appears in the center of the screen, showing a scatter plot of colored dots.
2. Increase **Persist** (Knob 2) to about 75%. Watch how the dots leave glowing trails as colors shift, mimicking the warm decay of a CRT phosphor.
3. Increase **Intensity** (Knob 1) to brighten the dots. The scatter plot becomes more vivid, and even faint chrominance activity becomes visible.
4. Set **I/Q Mode** (Switch 10) to **On** to overlay the scope on top of the source video. The scope sits in the center, and the original footage fills the rest of the screen.

---

## Parameters

![Videomancer front panel with Vectorscope loaded](/img/instruments/videomancer/vectorscope/vectorscope_control_panel.png)
*Videomancer's front panel with Vectorscope active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Intensity

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Intensity** scales the brightness of each dot in the scatter plot. At low values, only the most frequently-hit cells glow visibly: rare colors vanish into darkness. As Intensity is increased, even single-pixel color events become luminous. At maximum, the entire accumulation grid burns hot and the display blooms with light. This parameter multiplies the raw accumulator value before it reaches the screen, acting as a brightness gain for the scope display alone.

---

### Knob 2 — Persist

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Persist** controls the temporal decay rate of the phosphor simulation. At minimum, dots vanish almost instantly: each cell drains to black within one or two frames, and the display shows only the current frame's color content. As you increase Persist, cells decay more slowly, leaving luminous trails that linger across many frames. At maximum, the display approaches infinite persistence: once a cell is lit, it stays lit until new data replaces it. Long persistence transforms the scatter plot into a cumulative light painting of all the chrominance that has passed through the signal.

:::tip
High persistence is the key to the "phosphor art" look. Set Persist above 90% and slowly pan a camera across colorful objects: the scope accumulates a luminous record of every hue that appeared.
:::

---

### Knob 3 — Gain

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Gain** is reserved for future use and has no visible effect in the current firmware version.

---

### Knob 4 — Grat Opac

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Grat Opac** sets the brightness of the ***graticule*** crosshair overlay. At zero, the crosshair lines are invisible even when the graticule is enabled. Increasing this control makes the horizontal and vertical reference lines progressively brighter, helping you gauge where colors fall relative to the center of the chrominance space. The crosshair marks the neutral point: the position where U and V are both at their midpoint, corresponding to pure gray with no color.

:::note
The graticule must be enabled using **Over Video** (Switch 9) to be visible. Grat Opac controls brightness only; it does not toggle the crosshair on or off.
:::

---

### Knob 5 — Hue Shift

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Hue Shift** is reserved for future use and has no visible effect in the current firmware version.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** is reserved for future use and has no visible effect in the current firmware version.

---

### Switch 7 — Phosphor

| Property | Value |
|----------|-------|
| Off | Green |
| On | White |
| Default | Green |

**Phosphor** selects the phosphor color for the vectorscope display. This control works together with **Graticule** (Switch 8) to form a four-color selection system. See the Toggle Group Notes below for the complete color table. With both switches in their default positions, the display glows classic green: the color most associated with broadcast oscilloscopes and CRT phosphor screens.

---

### Switch 8 — Graticule

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Graticule** combines with **Phosphor** (Switch 7) to select the phosphor color. Despite its label, this toggle does not independently control the graticule overlay. See the Toggle Group Notes below for the complete color table. In its default position (**On**), Switch 8 contributes the high bit of the two-bit phosphor selector.

---

### Switch 9 — Over Video

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Over Video** enables or disables the crosshair ***graticule*** overlay on the vectorscope display. When set to **On**, a horizontal and vertical reference line intersect at the center of the scope, marking the neutral chrominance point. When set to **Off**, the crosshair is hidden and only the scatter dots appear. Despite its label, this toggle controls the graticule visibility, not the video overlay.

---

### Switch 10 — I/Q Mode

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**I/Q Mode** controls whether the source video is visible in the area surrounding the scope. When set to **On**, the original video signal fills the region outside the 64-pixel scope window, letting you see the analyzed image alongside its chrominance map. When set to **Off**, the area outside the scope is black. Despite its label, this toggle controls the video overlay feature.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all vectorscope rendering. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the scope display and the raw input.

---

:::note Toggle Group Notes

**Phosphor** (Switch 7) and **Graticule** (Switch 8) combine to form a two-bit phosphor color selector. Their on-screen labels do not fully describe this combined behavior. The four color options are:

| Phosphor (Sw 7) | Graticule (Sw 8) | Display Color |
|:---:|:---:|:---:|
| Green | Off | Green |
| White | Off | Amber |
| Green | On | Blue |
| White | On | White |

- **Green** is the classic oscilloscope phosphor (the most recognizable scope aesthetic.)
- **Amber** evokes the warm glow of vintage CRT terminals.
- **Blue** recalls cool-toned laboratory displays and modern digital instruments.
- **White** provides a neutral, monochrome scope display.

The phosphor color affects only the scope dots and graticule crosshair. It does not alter the source video visible through the **I/Q Mode** overlay.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the original input video and the vectorscope output. At 0%, the output is the unprocessed source video: the scope is not visible. At 100%, the output is the full vectorscope render (scope region plus the surrounding area, which is either black or the source video depending on **I/Q Mode**). Intermediate values blend the scope and source smoothly, creating a translucent vectorscope overlay.

---

## Background

### The broadcast vectorscope

The vectorscope has been an essential piece of broadcast engineering equipment since the adoption of color television in the 1950s. In the analog world, a vectorscope modulates a CRT electron beam so that the X and Y deflection plates are driven by the two ***chrominance*** components of the video signal. The resulting display is a circular scatter plot where the angle of each dot from the center encodes its hue and the distance from the center encodes its saturation. Engineers use the vectorscope to verify that skin tones fall along the correct line, that color bars hit their target positions, and that a signal's chrominance is properly balanced before transmission.

Videomancer's Vectorscope recreates this instrument digitally, replacing the CRT's analog deflection with a dual-port BRAM accumulation grid and replacing the phosphor's physical afterglow with an IIR decay algorithm. The result is functionally identical to a hardware vectorscope, rendered in real time alongside the video signal.

### UV color space

The vectorscope plots color in ***UV space***, the two chrominance components of the YUV color model. U encodes the blue-difference axis: ranging from orange on the left to blue on the right: while V encodes the red-difference axis: ranging from cyan at the bottom to red at the top. The center of the plot represents zero chrominance: pure gray, with neither warm nor cool tint.

On a standard broadcast vectorscope, reference marks at specific angles correspond to the six primary and secondary bars of a color bar pattern: red, magenta, blue, cyan, green, and yellow. Though Videomancer's Vectorscope renders a simplified crosshair rather than full burst-phase target marks, the spatial distribution of dots follows the same UV geometry. Feeding color bars into the program produces six distinct clusters arranged around the neutral center (the classic vectorscope fingerprint.)

### Phosphor persistence and IIR decay

The warm, fading glow of an oscilloscope display is called ***phosphor persistence***. On a real CRT, a thin layer of phosphorescent material on the screen continues to emit light for a brief period after the electron beam moves on. Videomancer's Vectorscope simulates this effect with an ***infinite impulse response*** (IIR) decay filter applied to every cell of the accumulation grid during each vertical blanking interval.

Each frame, the engine scans all 4,096 cells of the 64×64 grid and subtracts a small amount from each cell's stored value. The subtraction amount is derived from the **Persist** parameter: high persistence means a tiny subtraction per frame (slow fade), while low persistence means a large subtraction (fast fade). If the subtracted result would go below zero, the cell is clamped to zero. New pixel hits increment the cell, while the decay simultaneously drains it: the balance between accumulation and decay creates the characteristic phosphor trail.


---

## Signal Flow

### Signal Flow Notes

Two parallel data paths drive the vectorscope:

1. **Accumulation engine** (Port A of dual-port BRAM): During active video, each pixel's U and V chrominance values are quantized to 6-bit indices (bits 9 down to 4) and used to address a cell in the 64×64 grid. The cell value is incremented, saturating at 255. During vertical blanking, the engine scans all 4,096 cells and subtracts a decay amount derived from **Persist**. This read-modify-write pipeline runs with 1-clock latency: the read result is available one cycle after the address is presented, and the incremented value is written back in the following cycle.

2. **Scope renderer** (Port B of dual-port BRAM): A position tracker counts X and Y coordinates from sync edges. When the current pixel falls within the 64-pixel scope region, the renderer reads the corresponding accumulator cell, scales it by **Intensity**, optionally overwrites it with the **Grat Opac** value for crosshair pixels, and assigns a phosphor tint color to the UV channels. Outside the scope region, the renderer either passes the source video (if **I/Q Mode** is on) or outputs black.

:::note
The accumulation engine and renderer share the BRAM through a true dual-port architecture: Port A writes and reads for accumulation and decay, while Port B reads independently for display. This allows both operations to proceed simultaneously without contention.
:::


---

## Exercises

These exercises progress from basic scope reading to creative phosphor effects. Each exercise uses the vectorscope both as an analysis tool and a visual instrument.
### Exercise 1: Reading Color Bars

![Reading Color Bars result](/img/instruments/videomancer/vectorscope/vectorscope_ex1_s1.png)
*Reading Color Bars — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Learn to read a vectorscope display by analyzing a standard color bar test pattern.

#### Key Concepts

- UV scatter plots map chrominance to spatial position
- Saturated colors push dots outward from center
- The graticule crosshair marks the neutral point

#### Video Source

SMPTE color bars or any color bar generator signal.

#### Steps

1. **Start clean**: Ensure **Bypass** (Switch 11) is **Off** and **Mix** (Fader 12) is at 100%. The scope display should be visible in the center of the screen.
2. **Enable graticule**: Set **Over Video** (Switch 9) to **On** to show the crosshair. Increase **Grat Opac** (Knob 4) until the crosshair is clearly visible.
3. **Observe the pattern**: With color bars feeding in, you should see six distinct clusters of dots arranged around the center: one for each bar color (red, green, blue, cyan, magenta, yellow). White and black bars produce dots at or near the center crosshair.
4. **Adjust persistence**: Sweep **Persist** (Knob 2) from low to high. At low persistence, the dots are crisp but flickery. At high persistence, the dots blur into soft halos.
5. **Change phosphor color**: Flip **Phosphor** (Switch 7) and **Graticule** (Switch 8) to cycle through Green, Amber, Blue, and White phosphor tints. Notice how each tint changes the character of the display without altering the dot positions.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | 50% |
| Persist | 50% |
| Gain | 0% |
| Grat Opac | 50% |
| Hue Shift | 0° |
| Brightness | 0% |
| Phosphor | Green |
| Graticule | Off |
| Over Video | On |
| I/Q Mode | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Phosphor Light Painting

![Phosphor Light Painting result](/img/instruments/videomancer/vectorscope/vectorscope_ex2_s1.png)
*Phosphor Light Painting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Use high persistence to create abstract phosphor light paintings from moving footage.

#### Key Concepts

- High persistence accumulates chrominance history across many frames
- Intensity controls how visible rare color events are
- The scope becomes a time-lapse of color activity

#### Video Source

A live camera feed pointed at colorful subjects: paint swatches, fabric, holiday lights, or slowly moving objects with varied hues.

#### Steps

1. **Set high persistence**: Turn **Persist** (Knob 2) to about 90%. Dots will linger for many seconds after appearing, building on each other.
2. **Boost intensity**: Set **Intensity** (Knob 1) to about 80%. Even brief color events leave visible traces in the accumulation grid.
3. **Overlay on video**: Set **I/Q Mode** (Switch 10) to **On** to see the source video surrounding the scope. This helps you understand what real-world color is producing each cluster of dots.
4. **Sweep the camera**: Slowly pan across your colorful subjects. Watch the scope accumulate a luminous map of every hue that enters the frame. Saturated objects leave bright trails extending from the center; muted tones cluster tightly around the crosshair.
5. **White phosphor**: Set **Phosphor** (Switch 7) to **White** and **Graticule** (Switch 8) to **On** for a clean, monochrome display that emphasizes the dot pattern over the tint.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~80% |
| Persist | ~90% |
| Gain | 0% |
| Grat Opac | 25% |
| Hue Shift | 0° |
| Brightness | 0% |
| Phosphor | White |
| Graticule | On |
| Over Video | On |
| I/Q Mode | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Scope as Broadcast Monitor

![Scope as Broadcast Monitor result](/img/instruments/videomancer/vectorscope/vectorscope_ex3_s1.png)
*Scope as Broadcast Monitor — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Combine the vectorscope overlay with the source video to create a broadcast-style monitoring view.

#### Key Concepts

- Mix blends the scope output with the source at any ratio
- I/Q Mode places the source behind the scope region
- The scope becomes a picture-in-picture chrominance monitor

#### Video Source

Any live video feed: camera, media player, or a video synthesizer upstream in the chain.

#### Steps

1. **Enable overlay**: Set **I/Q Mode** (Switch 10) to **On** so the source video surrounds the scope window.
2. **Enable graticule**: Set **Over Video** (Switch 9) to **On** and **Grat Opac** (Knob 4) to about 30%. A faint crosshair marks the neutral point.
3. **Moderate persistence**: Set **Persist** (Knob 2) to about 60% for a responsive but smooth display.
4. **Reduce mix**: Pull **Mix** (Fader 12) down to about 70%. The scope region becomes slightly translucent, and you can see the source video ghosting through the scatter plot.
5. **Amber phosphor**: Set **Phosphor** (Switch 7) to **White** and **Graticule** (Switch 8) to **Off** for warm amber tones that contrast nicely with most video content.
6. **Observe**: As your source material changes, the vectorscope responds in real time. Watch how saturated scenes push dots outward and low-saturation scenes keep dots clustered at the center.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | 60% |
| Persist | ~60% |
| Gain | 0% |
| Grat Opac | ~30% |
| Hue Shift | 0° |
| Brightness | 0% |
| Phosphor | White |
| Graticule | Off |
| Over Video | On |
| I/Q Mode | On |
| Bypass | Off |
| Mix | ~70% |

---
## Glossary

- **Accumulator**: A memory cell that sums pixel hits over time, producing a brightness count proportional to how many pixels share the same chrominance coordinates.

- **Chrominance**: The color portion of a video signal, separate from brightness. In YUV encoding, chrominance is carried by the U and V components.

- **Dual-Port BRAM**: Block RAM configured with two independent access ports, allowing simultaneous read and write operations from different parts of the circuit.

- **Graticule**: A reference grid or crosshair overlaid on a test instrument display, used for alignment and measurement.

- **IIR (Infinite Impulse Response)**: A type of digital filter whose output depends on both current input and previous output values. Here it models the gradual decay of phosphor glow.

- **Phosphor**: A substance that emits light after being excited by an electron beam. On CRT displays, different phosphor compounds produce green, amber, blue, or white glows.

- **Saturation**: The intensity or purity of a color. High saturation means vivid color; low saturation means washed-out or gray.

- **Scatter Plot**: A two-dimensional chart where each data point is placed according to two independent values (here, U and V chrominance.)

- **UV Space**: The two-dimensional chrominance plane of the YUV color model, where U encodes the blue-difference axis and V encodes the red-difference axis.

- **Vectorscope**: A broadcast test instrument that displays the chrominance content of a video signal as a polar or Cartesian scatter plot.

- **Vertical Blanking**: The interval between video fields when no active picture content is transmitted; used here to perform the phosphor decay pass across all 4,096 accumulator cells.

---
