---
draft: true
sidebar_position: 215
slug: /instruments/videomancer/parade
title: "Parade"
image: /img/instruments/videomancer/parade/parade_hero_s1.png
description: "Before digital scopes and vectorscopes, broadcast engineers relied on cathode-ray tube waveform monitors to see inside the video signal."
---

![Parade hero image](/img/instruments/videomancer/parade/parade_hero_s1.png)
*Parade rendering three side-by-side waveform columns from a color video signal, tracing Y, U, and V channel amplitudes as glowing green phosphor traces against a dark background.*

---

## Overview

Parade turns your Videomancer into a broadcast-grade waveform monitor. It captures each line of incoming video and redraws it as a luminous dot graph: the brightness and color values of every pixel become vertical positions on screen, rendered as glowing traces that rise and fall like a city skyline viewed through an oscilloscope. Three columns march side by side: luminance on the left, blue-difference chrominance in the center, red-difference chrominance on the right: giving you a complete X-ray of the signal's anatomy.

But Parade is more than a measurement tool. With adjustable phosphor persistence, selectable trace colors, and a wet/dry mix fader, the waveform display itself becomes a visual instrument. Overlay the traces on top of the source video for heads-up monitoring, or push intensity and persistence to extremes and let the glowing dot-graphs become abstract neon landscapes. Parade bridges the gap between cold analysis and warm aesthetics (a spell that reveals the hidden skeleton of light.)

:::tip
Parade is equally at home in a technical calibration session and in a live visual performance. Use it to check levels, then leave it running as a visual element in its own right.
:::

### What's In a Name?

In broadcast engineering, a ***parade display*** is a standard waveform monitor layout that arranges color channels side by side in a marching formation: like soldiers on parade, lined up for inspection. Each column shows one component of the video signal, allowing the engineer to compare their amplitudes at a glance. The name captures both the orderly arrangement and the sense of presentation: the signal's inner structure, put on display for all to see.

---

## Quick Start

1. Feed a video signal into Videomancer and select **Parade**. You'll see three vertical columns of glowing dots: these trace the Y, U, and V values of each pixel along the scan line.
2. Turn **Intensity** (Knob 1) clockwise to brighten the dot traces. The waveform becomes vivid and easy to read.
3. Increase **Persist** (Knob 2) to thicken the traces vertically. The dots spread into fat bands, creating a phosphor-glow look reminiscent of a vintage CRT oscilloscope.
4. Flip the **Graticule** switch (Switch 9) to **On**. Three faint horizontal reference lines appear at 10%, 50%, and 90% of the signal range, helping you gauge levels at a glance.

---

## Parameters

![Videomancer front panel with Parade loaded](/img/instruments/videomancer/parade/parade_control_panel.png)
*Videomancer's front panel with Parade active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Intensity

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Intensity** controls the brightness of the waveform dots. At 0%, the trace dots are dark and nearly invisible against the background. As you turn the knob clockwise, the dots grow brighter, making the waveform easier to read. At 100%, the dots are at full brightness (a vivid, saturated trace that leaps off the screen.)

Intensity does not change the shape or position of the waveform. It only controls how bright the dot pixels are rendered, similar to the beam intensity knob on a traditional oscilloscope.

---

### Knob 2 — Persist

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Persist** controls the vertical thickness of each waveform dot, simulating the phosphor persistence of an analog CRT display. At 0%, each dot is a single pixel tall: a thin, precise trace. As you increase Persist, each dot spreads vertically, producing thicker bands of light. At 100%, the spread reaches its maximum, and the trace becomes a wide, glowing ribbon.

:::tip
Higher persistence values create a softer, more organic look that's useful as a visual effect. Lower values give a sharp, technical trace ideal for accurate signal reading.
:::

---

### Knob 3 — Gain

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Gain** controls the vertical scaling of the waveform, similar to the volts-per-division setting on an oscilloscope. At 0%, the waveform is compressed to a narrow band around the center line: signal variations are barely visible. At moderate settings, the waveform fills the vertical space naturally. At 100%, the waveform is magnified to four times its natural height, stretching peaks and valleys far beyond the screen edges.

The gain scaling uses eight discrete steps (0.125×, 0.25×, 0.5×, 1×, 1.5×, 2×, 3×, 4×) selected by the top three bits of the knob position. This gives you oscilloscope-style zoom levels rather than a smooth linear sweep.

:::note
At high gain settings, signal peaks that exceed the screen boundaries are clipped. This is normal: it's how real oscilloscopes behave when the V/div is set too high.
:::

---

### Knob 4 — Grat Opac

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Grat Opac** controls the brightness of the ***graticule***, the set of horizontal reference lines overlaid on the waveform display. At 0%, the graticule lines are invisible even when enabled. As you increase the value, the lines brighten, becoming thin gray markers at 10%, 50%, and 90% of the signal range. At 100%, the graticule lines are at their brightest.

This control has no effect unless the **Graticule** switch (Switch 9) is set to **On**.

---

### Knob 5 — Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Hue** is intended to rotate the color of the phosphor trace through 360 degrees of hue. In the current firmware, the phosphor color is selected by the **Phosphor** toggle (Switch 8) rather than this continuous knob. Adjusting Hue has no visible effect in this version.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** controls the luminance of the background behind the waveform traces. At 0%, the background is completely black, giving maximum contrast against the glowing dots. As you increase Brightness, the background lightens to a dim gray. At 100%, the background reaches its brightest level, reducing the contrast between the trace and the background.

When **Over Video** (Switch 10) is enabled, the source video replaces the flat background, and Brightness has no visible effect.

---

### Switch 7 — Mode

| Property | Value |
|----------|-------|
| Off | Parade |
| On | Luma |
| Default | Parade |

**Mode** selects the display layout. In the **Parade** position, the screen is divided into three equal columns, each rendering one video component: Y (luminance) on the left, U (blue-difference chrominance) in the center, and V (red-difference chrominance) on the right. The **Luma** position is intended for a single full-width luminance display.

---

### Switch 8 — Phosphor

| Property | Value |
|----------|-------|
| Off | Green |
| On | White |
| Default | Green |

**Phosphor** selects the color of the waveform trace, named after the phosphor coatings used in cathode ray tubes. In the **Green** position, the dots glow green with suppressed chroma: the classic oscilloscope look. In the **White** position, the dots are rendered as neutral white with no color tint, resembling a modern digital waveform monitor.

---

### Switch 9 — Graticule

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Graticule** enables or disables the horizontal reference lines overlaid on the waveform. When set to **On**, three thin lines appear at the 10%, 50%, and 90% levels of the signal range. These ***graticule*** lines serve as visual rulers, helping you judge whether a signal is clipping, centered, or within legal broadcast limits. When set to **Off**, the lines are hidden. Graticule brightness is controlled separately by **Grat Opac** (Knob 4).

---

### Switch 10 — Over Video

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Over Video** controls whether the original video signal is visible behind the waveform traces. When set to **Off**, the background is a flat dark field (controlled by **Brightness**, Knob 6). When set to **On**, the source video is rendered behind the waveform dots, creating a heads-up overlay where you can see both the image content and its signal analysis simultaneously.

:::tip
Over Video is especially useful during live performance: the audience sees the source material with luminous waveform traces dancing on top of it.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all waveform rendering. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the waveform display and the clean source.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input signal and the wet (waveform display) output. At 0%, only the original video is visible: the waveform display is completely hidden. At 100%, only the waveform display is visible. Intermediate positions blend the two, allowing you to ghost the waveform over the source at any desired opacity.

:::tip
Mix provides a smoother alternative to the **Over Video** toggle. With Over Video off, sliding Mix to a midpoint lets the source video bleed through the dark waveform background as a subtle ghost image.
:::

---

## Background

### Waveform monitors

A ***waveform monitor*** is one of the most fundamental tools in video engineering. It plots the amplitude of a video signal as a vertical trace against horizontal time, producing a graph where height represents brightness. Every broadcast studio, post-production suite, and color grading room relies on waveform monitors to ensure video signals stay within legal levels and to diagnose problems invisible to the naked eye.

The earliest waveform monitors were oscilloscopes repurposed for video work, displaying one scan line of analog voltage on a CRT screen. The phosphor coating of the CRT would glow briefly where the electron beam struck, producing a fading trace: the characteristic green glow that Parade recreates digitally.

### The parade display

The ***parade display*** is a specific waveform layout that separates a composite or component video signal into its individual channels, displaying them side by side. For a YUV signal, this means three columns: Y (luminance), U (Cb, blue-difference chrominance), and V (Cr, red-difference chrominance). This arrangement makes it easy to compare channel amplitudes and spot imbalances.

In a parade display, each column resamples the full scan line. Every horizontal pixel position within a column maps back to a corresponding position in the original line, so the three waveforms are spatially aligned. You can look straight across the three columns to compare how a single feature in the image contributes to each channel.

### Phosphor persistence

On a real CRT waveform monitor, the electron beam traces the waveform once per field. The ***phosphor*** coating on the screen face glows at the point of impact and then fades over a few milliseconds. This natural decay creates a soft, slightly blurred trace. Engineers chose phosphor compounds with different persistence characteristics depending on whether they needed a crisp single-trace readout or a longer-lasting afterglow for spotting intermittent events.

Parade simulates this with the **Persist** control. Increasing persistence widens the vertical spread of each dot, mimicking the glow of a slow-decay phosphor. The result is a thicker, fuzzier trace: aesthetically warmer and more organic, at the cost of reduced precision.

### Graticule

On a physical waveform monitor, the ***graticule*** is a set of calibrated lines etched or printed on a transparent overlay in front of the CRT screen. These lines mark key reference levels: typically 0%, 50%, and 100% of the signal range, plus markers for broadcast-legal limits. The graticule never changes; the trace moves behind it.

Parade renders its graticule as thin horizontal lines at the 10%, 50%, and 90% levels. These serve as visual rulers for gauging signal amplitude: a well-exposed image should have its Y waveform spanning from near the bottom graticule to near the top, with peaks and valleys distributed across the range.


---

## Signal Flow

### Signal Flow Notes

The pipeline has two conceptually distinct paths that share the same line buffer memory. The ***write path*** captures incoming pixel values continuously during the active video period, storing one full scan line of Y, U, and V data into three dual-port BRAMs. The ***read path*** runs simultaneously, reading back stored values for each horizontal position and comparing them against the current vertical position to determine whether a dot should be drawn.

The critical interaction is in the gain scaling stage: channel values are offset from the midpoint (512), scaled using shift-based discrete gain levels, and then mapped to vertical screen coordinates. The comparison stage checks whether the current scanline (`v_count`) falls within the persistence threshold of the mapped position: if so, a dot is lit. Graticule hits are evaluated in parallel: thin horizontal lines at pre-computed 10%, 50%, and 90% positions override the background but are themselves overridden by active dots. The composition priority is dot > graticule > over-video > dark background.

:::note
The 12-clock processing delay is matched by a sync delay pipeline that shifts hsync, vsync, field, and raw video data by the same number of clocks. This ensures the mixed output stays in perfect alignment with the video timing.
:::


---

## Exercises

These exercises progress from basic waveform reading to creative use of the parade display as a visual effect. Each builds on the previous, gradually exploring the aesthetic potential of what is traditionally a measurement tool.
### Exercise 1: Reading the Waveform

![Reading the Waveform result](/img/instruments/videomancer/parade/parade_ex1_s1.png)
*Reading the Waveform — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Learn to read the parade display as a diagnostic tool, identifying signal levels and color channel balance.

#### Key Concepts

- The waveform display plots signal amplitude vertically against horizontal position
- Three columns show Y, U, and V channels independently
- Graticule lines provide reference levels for signal amplitude

#### Video Source

A live camera feed or recorded footage with a mix of bright highlights, mid-tones, and dark shadows (a face lit from one side works well.)

#### Steps

1. **Default parade**: With the program loaded and a video signal connected, observe the three columns of dots. The left column (Y) shows brightness: bright areas push dots toward the top, dark areas toward the bottom.
2. **Enable graticule**: Flip **Graticule** (Switch 9) to **On** and increase **Grat Opac** (Knob 4) to about 60%. Three reference lines appear (these mark 10%, 50%, and 90% of the signal range.)
3. **Adjust gain**: Turn **Gain** (Knob 3) slowly clockwise. The waveform stretches vertically, magnifying small differences and making subtle details visible. Find a gain level where the trace fills most of the screen without clipping at the edges.
4. **Sharpen the trace**: Set **Persist** (Knob 2) to a low value, around 10%. The trace narrows to a thin, precise line. This is the sharpest reading.
5. **Compare channels**: Look across the three columns at the same horizontal position. A white object will show high Y, mid U, and mid V. A saturated color will show strong offsets from center in the U and V columns.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~70% |
| Persist | ~10% |
| Gain | ~50% |
| Grat Opac | ~60% |
| Hue | 0° |
| Brightness | ~0% |
| Mode | Parade |
| Phosphor | Green |
| Graticule | On |
| Over Video | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Phosphor Portrait

![Phosphor Portrait result](/img/instruments/videomancer/parade/parade_ex2_s1.png)
*Phosphor Portrait — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Transform the parade display into a glowing phosphor portrait overlaid on the source video.

#### Key Concepts

- Persistence and intensity transform the waveform from a measurement into a visual texture
- Phosphor color selection changes the aesthetic character of the display
- Over Video composites the waveform on top of the source image

#### Video Source

A high-contrast portrait or figure against a dark background (something with strong silhouette edges.)

#### Steps

1. **Thicken the trace**: Increase **Persist** (Knob 2) to about 80%. The thin dots become wide bands of light, creating soft vertical columns of glow.
2. **Boost intensity**: Turn **Intensity** (Knob 1) to about 90%. The thick traces become vivid and luminous.
3. **Switch to white**: Flip **Phosphor** (Switch 8) to **White**. The green CRT look is replaced by a clean white trace, giving a more modern, ethereal quality.
4. **Overlay on video**: Flip **Over Video** (Switch 10) to **On**. The source video appears behind the glowing waveform traces, creating a composite where the subject is visible through the luminous bars.
5. **Add graticule**: Turn on **Graticule** (Switch 9) and set **Grat Opac** (Knob 4) to about 40%. The thin reference lines add a subtle grid structure to the composition.
6. **Blend with mix**: Pull **Mix** (Fader 12) to about 60%. The waveform overlay softens, blending with the dry source for a ghostly, translucent effect.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~90% |
| Persist | ~80% |
| Gain | ~40% |
| Grat Opac | ~40% |
| Hue | 0° |
| Brightness | 0% |
| Mode | Parade |
| Phosphor | White |
| Graticule | On |
| Over Video | On |
| Bypass | Off |
| Mix | ~60% |

---

### Exercise 3: Neon Landscape

![Neon Landscape result](/img/instruments/videomancer/parade/parade_ex3_s1.png)
*Neon Landscape — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Push the parade display to its visual extremes, turning the waveform into an abstract neon landscape.

#### Key Concepts

- High gain magnifies small signal differences into dramatic vertical sweeps
- Combining high persistence with high intensity creates painterly, abstract visuals
- The waveform display can be used purely as a generative visual element

#### Video Source

Any video with motion: a panning camera, moving figures, or animated graphics. The motion creates evolving waveform shapes.

#### Steps

1. **Maximum gain**: Turn **Gain** (Knob 3) fully clockwise. The waveform explodes vertically: peaks shoot past the screen edges, and even subtle signal variations become towering columns of light.
2. **Maximum persistence**: Set **Persist** (Knob 2) fully clockwise. Each dot becomes a wide vertical band. The three columns merge into broad, overlapping ribbons of glow.
3. **Full intensity**: Set **Intensity** (Knob 1) to about 95%. The traces are blazing bright against the dark background.
4. **Dark background**: Set **Brightness** (Knob 6) to about 10%. A faint gray background adds a trace of depth without competing with the vivid traces.
5. **Green phosphor**: Ensure **Phosphor** (Switch 8) is set to **Green**. The classic oscilloscope green pops against the near-black background.
6. **Disable graticule**: Set **Graticule** (Switch 9) to **Off**. Without reference lines, the display becomes pure abstract pattern.
7. **Watch the motion**: As the video source changes, the waveform sweeps and pulses in real time, creating an evolving neon terrain.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~95% |
| Persist | 100% |
| Gain | 100% |
| Grat Opac | 0% |
| Hue | 0° |
| Brightness | ~10% |
| Mode | Parade |
| Phosphor | Green |
| Graticule | Off |
| Over Video | Off |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Chrominance**: The color information in a video signal, encoded as U (blue-difference) and V (red-difference) components that describe hue and saturation independently of brightness

- **Graticule**: A set of calibrated reference lines on a waveform monitor screen, used to measure signal amplitude against known levels

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness on a scale from black to white

- **Parade Display**: A waveform monitor layout that arranges video signal components (Y, U, V or R, G, B) side by side in separate columns for simultaneous comparison

- **Persistence**: On a CRT display, the duration a phosphor dot continues to glow after the electron beam has moved on; simulated here as vertical dot thickness

- **Phosphor**: A chemical coating on the face of a cathode ray tube that glows when struck by an electron beam; different phosphor compounds produce different colors and decay rates

- **Waveform Monitor**: A specialized oscilloscope used in video engineering to display the amplitude of a video signal as a vertical trace against horizontal time, revealing brightness and color levels

---
