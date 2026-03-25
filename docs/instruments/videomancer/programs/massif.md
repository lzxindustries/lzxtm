---
draft: true
sidebar_position: 188
slug: /instruments/videomancer/massif
title: "Massif"
image: /img/instruments/videomancer/massif/massif_hero_s1.png
description: "In 1973, Steve Rutt and Bill Etra built a video instrument that did something no other machine could do: it took a standard television signal and deflected each scan line vertically by an amount proportional to its brightness."
---

![Massif hero image](/img/instruments/videomancer/massif/massif_hero_s1.png)
*Massif transforming a live camera feed into a luminance-displaced scanline terrain with amber phosphor glow and perspective foreshortening.*

---

## Overview

Massif is a scanline terrain synthesizer that converts video into three-dimensional landscapes made of light. Each horizontal scanline is vertically displaced by an amount proportional to its brightness, turning flat pictures into undulating topographic surfaces. Bright regions push scanlines upward (or downward), creating peaks and ridges. Dark regions sink into valleys. The result looks like a wire-frame mountain range rendered on a vector display, with the video content itself sculpting the terrain.

Between frames, the column buffer ***decays*** rather than clearing: each pixel fades gradually, leaving ghostly trails when the terrain shifts. This simulates the phosphor persistence of a cathode-ray tube, where bright areas linger for a moment after they've moved. Combined with edge enhancement that brightens contour lines and a tint control that colors the monochrome output, Massif produces imagery that evokes the analog video synthesis experiments of the 1970s.

:::tip
Massif is a ***processing*** program. It needs a video input to generate terrain: the input image *is* the landscape. Try a camera pointed at your hands, a face, or any high-contrast subject.
:::

### What's In a Name?

A ***massif*** is a compact group of mountain peaks formed from a single geological structure: a distinct, self-contained block of elevated terrain. The name suits this program perfectly: the displaced scanlines form ridgelines and valleys that resemble a mountain range viewed from a distance, and the column buffer architecture literally builds the terrain column by column, like the geological forces that raise a massif from the earth's crust. The word also carries the connotation of something massive and imposing, which describes the visual presence of a full-screen scanline displacement effect.

---

## Quick Start

1. Feed a live camera or recorded footage into Videomancer. Turn **Deflection** (Knob 1) clockwise to about 40%. The image tears apart vertically: bright areas push scanlines upward, forming peaks above the dark areas that remain flat.
2. Toggle **Direction** (Switch 8) to **Down**. The displacement reverses: bright regions now push downward, and the terrain flips. Switch back to **Up** for a classic Rutt/Etra look where brightness rises.
3. Increase **Decay** (Knob 3) past 75%. The terrain develops glowing trails: scanlines linger as phosphor ghosts, blurring motion into luminous streaks. Move your hand in front of the camera and watch the afterglow.
4. Enable **Perspective** (Switch 9, set to **On**) and turn **Perspective** (Knob 2) clockwise. Lines near the bottom of the screen displace more than lines near the top, simulating depth foreshortening. The flat terrain suddenly looks three-dimensional.

---

## Parameters

![Videomancer front panel with Massif loaded](/img/instruments/videomancer/massif/massif_control_panel.png)
*Videomancer's front panel with Massif active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Deflection

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |

**Deflection** controls how much each scanline is vertically displaced by its brightness. At 0%, fully counterclockwise, scanlines remain in their original positions and the image passes through with no terrain effect. As the value increases, brighter pixels push scanlines farther from their home position. At 100%, fully clockwise, the displacement reaches its maximum range of approximately 128 lines: bright regions are flung far from their origin, creating dramatic peaks and deep canyons in the terrain.

:::note
High Deflection values cause scanlines from different parts of the image to overlap and interleave. The column buffer overwrites each target position, so the last scanline to land at a given line wins. This creates a natural occlusion effect where foreground terrain hides background terrain.
:::

---

### Knob 2 — Perspective

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Perspective** controls the amount of depth foreshortening applied to the displacement. When **Perspective** (Switch 9) is enabled, scanlines near the bottom of the frame receive more displacement than scanlines near the top, simulating a camera looking across a landscape toward the horizon. At 0%, the bottom scanlines receive minimal foreshortening. At 100%, the perspective gradient is at maximum strength, creating a dramatic sense of depth where foreground terrain looms large and distant terrain flattens toward the horizon.

:::tip
Perspective works by scaling the displacement by the current scanline's vertical position. Disable Perspective (Switch 9 to **Off**) for a flat, orthographic view where all scanlines displace equally regardless of vertical position.
:::

---

### Knob 3 — Decay

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Decay** controls inter-frame phosphor persistence: how much of the previous frame's terrain survives into the next frame. At 0%, fully counterclockwise, the column buffer clears completely between frames, producing a sharp, flicker-free terrain with no trails. As the value increases, previous frames fade more slowly, creating ghostly afterimages that blur motion into luminous streaks. At 100%, the buffer barely decays at all, and the terrain accumulates into a dense, glowing mass where everything that has ever been bright leaves a permanent mark.

---

### Knob 4 — Edge Enh

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |

**Edge Enh** (Edge Enhancement) brightens pixels where the luminance changes rapidly from one pixel to the next. This highlights contour lines and edges in the displaced terrain, making the ridgeline profiles sharper and more visible. At 0%, no edge enhancement is applied. As the value increases, the brightness boost at contour boundaries intensifies. At 100%, edges glow brightly against the surrounding terrain, giving the output a neon wireframe quality.

---

### Knob 5 — Tint Hue

| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 123deg |

**Tint Hue** selects the phosphor color used in monochrome mode. The control sweeps through a circular color map: starting from green at the far left, passing through yellow and red at the midpoint, continuing to blue, and returning through magenta toward green at the far right. Classic phosphor tones include green (far left), amber (roughly 33%), and cool blue (roughly 70%). This control has no effect when the **Color** toggle (Switch 7) is set to **Source**.

---

### Knob 6 — Line Gap

| Property | Value |
|----------|-------|
| Range | 0ln – 16ln |
| Default | 4ln |

**Line Gap** controls the spacing between drawn scanlines. At 0%, every scanline is drawn, producing a solid terrain surface. As the value increases, scanlines are drawn less frequently: only every second, third, or fourth line: creating visible horizontal gaps between the terrain strokes. At 100%, only every sixteenth line is drawn, producing a sparse wireframe of widely spaced scanlines. The gaps between drawn lines are filled according to the **Fill Mode** toggle (Switch 10).

---

### Switch 7 — Color

| Property | Value |
|----------|-------|
| Off | Mono |
| On | Source |
| Default | Mono |

**Color** selects between monochrome and source color modes. In **Mono** mode, the terrain is rendered in a single hue controlled by **Tint Hue** (Knob 5), with brightness determined by the displaced luminance. In **Source** mode, the original color information from the input video is preserved: each displaced scanline carries its original chrominance values, producing a full-color terrain.

---

### Switch 8 — Direction

| Property | Value |
|----------|-------|
| Off | Up |
| On | Down |
| Default | Up |

**Direction** controls whether bright pixels push scanlines upward or downward. In **Up** mode, bright areas rise above dark areas, creating the classic Rutt/Etra look where a face or hand appears as a luminous mountain range. In **Down** mode, the displacement is inverted: bright areas push downward, creating an inverted terrain where highlights sink into valleys.

---

### Switch 9 — Perspect

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Perspect** (Perspective) enables or disables the perspective foreshortening effect controlled by the **Perspective** knob (Knob 2). When set to **Off**, all scanlines displace by the same amount regardless of their vertical position, producing a flat orthographic view. When set to **On**, displacement is scaled by vertical position so that lines near the bottom of the frame displace more than lines near the top, simulating depth.

---

### Switch 10 — Fill Mode

| Property | Value |
|----------|-------|
| Off | Black |
| On | Hold |
| Default | Black |

**Fill Mode** determines what appears in the gaps between displaced scanlines. In **Black** mode, gaps are filled with black (Y=0, neutral chroma), creating dark valleys between the bright terrain strokes. In **Hold** mode, the last non-zero pixel value is held through the gap, filling empty regions with a repeating copy of the nearest terrain stroke above. Hold mode creates a solid, painted look; Black mode creates a more traditional wireframe.

---

### Switch 11 — Invert

| Property | Value |
|----------|-------|
| Off | Normal |
| On | Invert |
| Default | Normal |

**Invert** reverses the luminance of the input before displacement is calculated. In **Normal** mode, bright pixels receive the most displacement. In **Invert** mode, dark areas receive the most displacement and bright areas remain flat. This flips the terrain: valleys become peaks and peaks become valleys. Inversion occurs at the very first pipeline stage, so it affects displacement, edge enhancement, and all downstream processing.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (original) and wet (terrain) signals. At 0%, fully down, only the original video is visible. At 100%, fully up, only the terrain output is visible. Intermediate positions blend the two, superimposing the displaced terrain over the source image. This is useful for creating transparent terrain overlays or for quickly comparing the processed and unprocessed signals.

---

## Background

### The Rutt/Etra Video Synthesizer

In 1973, Steve Rutt and Bill Etra built one of the most iconic instruments in the history of video art. The ***Rutt/Etra Video Synthesizer*** displayed video as a grid of deflected scanlines on a vector display, where the vertical position of each line was controlled by the brightness of the corresponding pixel. Faces became landscapes. Hands became mountains. The machine turned the flat television image into a sculptural, three-dimensional form rendered entirely in light.

The visual language of the Rutt/Etra: glowing scanline ridges against a black void: became synonymous with electronic art and science-fiction graphics throughout the 1970s and 1980s. Massif recreates this aesthetic digitally, using a column buffer in FPGA block RAM to simulate the vector display's ability to place scanlines at arbitrary vertical positions.

### Column buffer architecture

Massif's displacement engine works fundamentally differently from a pixel-by-pixel filter. Instead of transforming each pixel in place, it writes each input scanline into a ***column buffer*** at a displaced vertical address. The column buffer is a 1024-line memory that represents a single column of the output frame. For every input pixel, the algorithm calculates a target line number based on that pixel's brightness and writes the result into the buffer at that address. When it's time to output the frame, the buffer is read line by line from top to bottom.

This architecture means that multiple input scanlines can land on the same output line: the last one written wins, creating a natural front-to-back ***occlusion*** effect. It also means that some output lines may never be written at all, creating the characteristic gaps between terrain strokes.

### Phosphor persistence and decay

Real cathode-ray tubes don't go dark instantly when the electron beam moves on. The phosphor coating continues to glow for a brief period, creating a fading afterimage. Massif simulates this behavior by ***decaying*** the column buffer between frames rather than clearing it. During vertical blanking, every value in the buffer is multiplied by the decay factor, shrinking it toward zero. A high decay value means the buffer retains most of its previous content, and moving objects leave luminous trails. A low decay value means the buffer clears almost completely, and each frame is drawn fresh.

The decay process operates in a two-phase cycle: on the first clock, the current value is read from BRAM; on the second clock, the decayed value is written back. This two-phase approach ensures clean BRAM inference on the iCE40 FPGA.


---

## Signal Flow

### Signal Flow Notes

Two architectural features define Massif's character:

1. **Column buffer compositing.** Unlike pixel-in/pixel-out effects, Massif writes input scanlines to *displaced* addresses in a 1024-line column buffer. The write-port overwrites any previous contents at the target address, creating natural front-to-back occlusion: when two scanlines map to the same output line, the one processed last wins. Gaps appear wherever no input scanline was displaced to a given output line.

2. **Decay as persistence.** The column buffer is not cleared between frames. Instead, during vertical blanking, a two-phase sweep reads each address, multiplies the luminance by the decay factor, and writes the result back. This creates phosphor-like persistence: terrain from previous frames fades gradually, and moving subjects leave glowing trails. Chrominance values are preserved through the decay sweep (only luminance fades.)

:::tip
**Edge enhancement and displacement interact.** The edge gradient is computed *before* displacement, from the horizontal difference between adjacent input pixels. This means edge brightening follows the contours of the original image, not the displaced terrain. Steep luminance transitions in the source create bright ridgelines in the output.
:::


---

## Exercises

These exercises progress from basic terrain displacement to full Rutt/Etra landscapes with phosphor persistence and perspective depth.
### Exercise 1: First Terrain

![First Terrain result](/img/instruments/videomancer/massif/massif_ex1_s1.png)
*First Terrain — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A simple scanline terrain from a live camera feed, with glowing contour edges.

#### Key Concepts

- Luminance displacement converts brightness to vertical position
- Direction toggle flips the terrain
- Edge enhancement highlights contour ridges

#### Video Source

A live camera feed pointed at a face or hand, or recorded footage with strong contrast.

#### Steps

1. **Displace**: Turn **Deflection** (Knob 1) slowly clockwise to about 40%. The image breaks apart vertically (bright areas rise (or fall) from dark areas.)
2. **Flip direction**: Toggle **Direction** (Switch 8) between **Up** and **Down**. Watch the terrain invert (peaks become valleys. Set it to **Up** for a classic look.)
3. **Sharpen edges**: Increase **Edge Enh** (Knob 4) to about 30%. Contour lines brighten, giving the terrain a glowing wireframe quality.
4. **Tint the phosphor**: With **Color** (Switch 7) set to **Mono**, sweep **Tint Hue** (Knob 5) to find an amber tone (about 33%). The terrain glows like a 1970s vector display.
5. **Add gaps**: Increase **Line Gap** (Knob 6) slightly. Visible horizontal gaps appear between scanlines, reinforcing the wireframe aesthetic.

#### Settings

| Control | Value |
|---------|-------|
| Deflection | ~40% |
| Perspective | 50% |
| Decay | 0% |
| Edge Enh | ~30% |
| Tint Hue | ~120 deg |
| Line Gap | ~4 ln |
| Color | Mono |
| Direction | Up |
| Perspect | Off |
| Fill Mode | Black |
| Invert | Normal |
| Mix | 100% |

---

### Exercise 2: Phosphor Persistence

![Phosphor Persistence result](/img/instruments/videomancer/massif/massif_ex2_s1.png)
*Phosphor Persistence — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A glowing, persistent terrain with luminous motion trails.

#### Key Concepts

- Decay creates inter-frame persistence (phosphor glow)
- High decay values accumulate terrain across multiple frames
- Hold fill mode creates solid surfaces instead of gaps

#### Video Source

A live camera feed with slow hand or body movement, or footage with gradual motion.

#### Steps

1. **Start with terrain**: Set **Deflection** to ~50%, **Edge Enh** to ~40%, **Color** to **Mono**, **Tint Hue** to amber (~33%).
2. **Add persistence**: Increase **Decay** (Knob 3) slowly from 0% toward 75%. The terrain begins to leave afterimages. Move your hand slowly and watch the trails linger.
3. **High persistence**: Push Decay above 85%. The terrain accumulates into a dense, glowing mass. Fast movement creates long streaks; slow movement builds up bright ridges.
4. **Solid fill**: Toggle **Fill Mode** (Switch 10) to **Hold**. The gaps between scanlines fill with the nearest terrain value, creating a solid painted surface instead of a wireframe.
5. **Source color**: Toggle **Color** (Switch 7) to **Source**. The terrain now carries the original video's color, creating a chromatic landscape with persistent color trails.

#### Settings

| Control | Value |
|---------|-------|
| Deflection | ~50% |
| Perspective | 50% |
| Decay | ~85% |
| Edge Enh | ~40% |
| Tint Hue | ~120 deg |
| Line Gap | ~4 ln |
| Color | Mono |
| Direction | Up |
| Perspect | Off |
| Fill Mode | Hold |
| Invert | Normal |
| Mix | 100% |

---

### Exercise 3: Perspective Landscape

![Perspective Landscape result](/img/instruments/videomancer/massif/massif_ex3_s1.png)
*Perspective Landscape — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A three-dimensional terrain landscape with depth foreshortening, phosphor trails, and visible scanline gaps.

#### Key Concepts

- Perspective foreshortening creates depth by scaling displacement with vertical position
- Combining perspective, decay, and line gaps produces immersive 3D terrain
- The Mix fader blends terrain with the dry source

#### Video Source

Footage of clouds, water, or landscape scenery. Alternatively, any footage with gradual brightness transitions.

#### Steps

1. **Enable perspective**: Set **Perspect** (Switch 9) to **On**. Turn **Perspective** (Knob 2) to about 70%. Lines near the bottom of the screen now displace more than lines near the top, creating a strong sense of depth.
2. **Set terrain**: **Deflection** to ~70%, **Decay** to ~70%, **Edge Enh** to ~60%.
3. **Widen gaps**: Increase **Line Gap** (Knob 6) to about 6 ln. The terrain resolves into widely spaced, glowing scanlines (a convincing wireframe landscape.)
4. **Color landscape**: Set **Color** (Switch 7) to **Source** for color terrain, or keep **Mono** and set **Tint Hue** to a cool blue (~250 deg) for an icy mountain range.
5. **Invert the terrain**: Toggle **Invert** (Switch 11) to **Invert**. The terrain flips: dark areas now rise and bright areas sink. Experiment with switching Direction as well for different orientations.
6. **Overlay**: Lower **Mix** (Fader 12) to about 60%. The terrain superimposes over the source image, creating a translucent holographic landscape floating over the original footage.

#### Settings

| Control | Value |
|---------|-------|
| Deflection | ~70% |
| Perspective | ~70% |
| Decay | ~70% |
| Edge Enh | ~60% |
| Tint Hue | ~250 deg |
| Line Gap | ~6 ln |
| Color | Source |
| Direction | Up |
| Perspect | On |
| Fill Mode | Black |
| Invert | Normal |
| Mix | ~60% |

---
## Glossary

- **Column Buffer**: A per-column memory storing one vertical slice of the output frame; scanlines are written at displaced addresses and read back sequentially for display.

- **Decay**: The gradual fading of stored pixel values between frames, simulating cathode-ray phosphor persistence.

- **Displacement**: The vertical shifting of a scanline from its original position, proportional to its brightness value.

- **Edge Enhancement**: Brightening of pixels where luminance changes rapidly between adjacent horizontal pixels, emphasizing contour ridgelines.

- **Foreshortening**: A perspective technique that makes distant objects appear smaller; in Massif, lines near the top of the frame displace less than lines near the bottom.

- **Occlusion**: The hiding of background geometry behind foreground geometry; when two displaced scanlines land on the same output line, the last one written prevails.

- **Phosphor**: The luminescent coating inside a cathode-ray tube that glows when struck by an electron beam and fades gradually afterward.

- **Rutt/Etra**: A pioneering analog video synthesizer (1973) by Steve Rutt and Bill Etra that displayed video as vertically deflected scanlines on a vector display.

- **Scanline**: A single horizontal row of pixels in a video frame, traced left to right by the electron beam (or pixel clock).

- **Terrain**: The visual result of scanline displacement (an undulating surface where brightness maps to height.)

- **Tint**: A uniform chrominance applied to the monochrome terrain output, simulating the color of a CRT phosphor.

- **Vector Display**: A display that draws arbitrary lines by steering an electron beam to specific coordinates, rather than scanning a fixed raster grid.

---
