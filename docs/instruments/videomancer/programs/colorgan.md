---
draft: true
sidebar_position: 58
slug: /instruments/videomancer/colorgan
title: "Colorgan"
image: /img/instruments/videomancer/colorgan/colorgan_hero.png
description: "Colorgan transforms incoming video luminance into a three-band colour organ display reminiscent of 1970s CEL Chromascope disco lighting units."
---

![Colorgan hero image](/img/instruments/videomancer/colorgan/colorgan_hero_s1.png)
*Colorgan projecting warm concentric zones of bass red, mid green, and treble blue that pulse and bloom in response to input video luminance.*

---

## Overview

Colorgan is a three-band color organ synthesizer that transforms input video luminance into pulsing, colored zones. It works like a disco light show for video: the overall brightness of the incoming picture is analyzed frame by frame, split into slow-moving "bass," medium-moving "mid," and fast-changing "treble" frequency bands, and each band drives a colored region of the screen. Where the bass is strong, warm reds bloom; where the mid band rises, greens glow; where high-frequency changes spike, cool blues flash.

The program offers two spatial layouts. In ***concentric*** mode, the zones radiate outward from the center of the screen like a target, with treble at the core and bass at the rim. In ***layered*** mode, the screen is divided into three horizontal bands: treble at the top, mid in the middle, bass at the bottom: like stacked light panels. A palette switch flips between warm and cool color schemes, and a dry/wet mix fader lets you blend the synthesized light show with the original input video.

:::tip
Colorgan responds to ***changes*** in brightness, not absolute brightness levels. A static image produces a fixed color field. Feed it footage with motion, flashing lights, or rhythmic edits, and the zones come alive.
:::

### What's In a Name?

The name ***Colorgan*** is a portmanteau of ***color*** and ***organ***, paying homage to the ***color organ***: an instrument that translates sound into light. The earliest color organs date to the eighteenth century, but the concept reached its peak in the 1970s disco era with devices like the CEL Chromascope, which split audio into frequency bands and drove colored light bulbs accordingly. Colorgan applies the same principle to video: instead of bass guitar driving a red floodlight, it's the slow-moving average brightness of the video frame that makes the red zone glow.

---

## Quick Start

1. Connect a video source with visible motion: a camera feed, music video, or footage with rhythmic brightness changes works best.
2. Turn **Bass Zone** (Knob 1), **Mid Zone** (Knob 2), and **Treble Zone** (Knob 3) to their midpoints. You should see colored zones appear: reds and blues pulsing gently with the video's brightness changes.
3. Flip the **Layout** switch (Switch 7) to compare **Concentric** (rings radiating from center) and **Layered** (horizontal stripes). Concentric places treble at the center; Layered stacks bass at the bottom and treble at the top.
4. Adjust the **Mix** fader (Fader 12) to blend the color organ output with your original video. At 100%, only the synthesized light show is visible. Pull it back toward 0% to overlay the color organ onto your source footage.

---

## Parameters

![Videomancer front panel with Colorgan loaded](/img/instruments/videomancer/colorgan/colorgan_control_panel.png)
*Videomancer's front panel with Colorgan active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Bass Zone

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bass Zone** controls the sensitivity of the lowest frequency band: the slow-moving luminance envelope. This band tracks the overall average brightness of the video frame through a slow ***IIR filter*** with a time constant of roughly sixteen frames. When the input video makes gradual brightness shifts, the bass level rises and falls in a slow, breathing rhythm. Turning Bass Zone clockwise increases the gain applied to this slow envelope, making the bass-colored region brighter and more dominant. At 0%, the bass band contributes nothing. At 100%, even subtle shifts in average brightness produce vivid color.

:::note
Because the bass filter is so slow, it responds to sustained brightness changes rather than quick flashes. Pan across a bright scene and the bass zone will swell; cut rapidly between shots and it barely flinches.
:::

---

### Knob 2 — Mid Zone

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Mid Zone** controls the sensitivity of the middle frequency band. This band uses a faster IIR filter with a time constant of roughly four frames, making it responsive to moderate-speed brightness changes: scene cuts, camera moves, and lighting transitions. Turning Mid Zone clockwise increases the gain, causing the mid-colored region (green in the warm palette, cyan-shifted in the cool palette) to glow more intensely. At 0%, the mid band is silent. At high values, even moderate brightness fluctuations produce strong color.

---

### Knob 3 — Treble Zone

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Treble Zone** controls the sensitivity of the highest frequency band. The treble signal is derived from the instantaneous difference between the current frame's average brightness and the fast IIR filter: it spikes when the video makes sudden brightness jumps (flash cuts, strobe effects, rapid motion). Turning Treble Zone clockwise amplifies these spikes, producing sharp, brief flashes of treble color. At 0%, fast changes are ignored. At 100%, every brightness transient fires the treble zone.

:::tip
Feed Colorgan a video with rhythmic edits or strobe effects and crank **Treble Zone** to maximum. The center of the screen (in concentric mode) or the top band (in layered mode) will flash in sync with each cut.
:::

---

### Knob 4 — Zone Width

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Zone Width** controls the spatial extent of the colored zones on screen. In concentric mode, this sets the radius of the concentric rings: small values compress the zones into a tight cluster at the center, while large values spread them across the full screen. In layered mode, the zones occupy fixed horizontal bands regardless of this setting, so Zone Width has its most dramatic effect in concentric layout. The minimum effective width is clamped to prevent the zones from collapsing to zero.

---

### Knob 5 — Hue Offset

| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |

**Hue Offset** is intended to rotate the base hue of the color palette, shifting the color assignments of all three bands simultaneously around the color wheel. This parameter is reserved for a future update and does not currently affect the output.

---

### Knob 6 — Decay

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |

**Decay** is intended to control the temporal smoothing rate of the envelope followers, adjusting how quickly the band levels rise and fall in response to brightness changes. This parameter is reserved for a future update. The built-in IIR filter time constants provide the temporal smoothing: the bass band decays over approximately sixteen frames, and the mid band over approximately four frames.

---

### Switch 7 — Layout

| Property | Value |
|----------|-------|
| Off | Concentric |
| On | Layered |
| Default | Concentric |

**Layout** selects the spatial arrangement of the three frequency zones. Set to **Concentric**, the zones radiate outward from the center of the screen: the treble zone occupies the innermost area, the mid zone forms a ring around it, and the bass zone fills the outer ring. The distance metric is ***Manhattan distance*** (sum of horizontal and vertical offsets from center), which gives the concentric zones a diamond-like shape rather than perfect circles. Set to **Layered**, the screen is divided into three equal horizontal bands: treble at the top, mid in the middle, bass at the bottom.

:::note
In concentric mode the zones are defined by the **Zone Width** parameter. In layered mode the band boundaries are fixed at one-third intervals of the screen height.
:::

---

### Switch 8 — Palette

| Property | Value |
|----------|-------|
| Off | Warm |
| On | Cool |
| Default | Warm |

**Palette** switches between two color schemes. Set to **Warm**, the bass zone glows red (positive V chroma), the mid zone glows green (negative U chroma), and the treble zone glows blue-magenta (positive U chroma). Set to **Cool**, the color assignments shift: bass becomes blue (positive U), mid becomes cyan (negative V), and treble shifts toward a red-violet blend (negative U, positive V). The warm palette produces fire-like washes; the cool palette produces underwater or neon tones.

---

### Switch 9 — React

| Property | Value |
|----------|-------|
| Off | Smooth |
| On | Sharp |
| Default | Smooth |

**React** is intended to switch between smooth and sharp envelope response curves. This parameter is reserved for a future update. The current IIR filter time constants are fixed regardless of this switch position.

---

### Switch 10 — Video Mod

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Video Mod** is intended to enable input-video modulation of the generated zones, allowing the source video to influence the spatial pattern of the color organ beyond its role as a luminance envelope source. This parameter is reserved for a future update.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** is intended to route the unprocessed input directly to the output, skipping the color organ rendering entirely. This parameter is reserved for a future update. To achieve bypass behavior, set the **Mix** fader (Fader 12) to 0%, which crossfades fully to the dry input.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the dry/wet crossfade between the original input video and the synthesized color organ output. At 0%, the output is a clean pass-through of the input: no color organ is visible. At 100%, the output is entirely the synthesized light show. Intermediate values overlay the pulsing color zones onto the source footage, creating a tinted, modulated composite.

:::tip
At low Mix values (10–30%), Colorgan acts as a subtle color wash that tints your footage in time with brightness changes: a gentle, ambient effect. At high Mix values (70–100%), the color organ dominates and the source becomes a ghost beneath the pulsing zones.
:::

---

## Background

### Color organs

A ***color organ*** is an instrument that translates a signal into colored light. The concept dates back to Louis Bertrand Castel's *ocular harpsichord* in the 1720s, which mapped musical notes to colored panels. By the 1960s and 1970s, electronic color organs had become staples of the disco and psychedelic music scenes. Devices like the CEL Chromascope split an audio signal into frequency bands: bass, mid, and treble: and drove colored light bulbs or projectors proportionally. A thumping bass line would make a red floodlight swell; a guitar solo would pulse a green spotlight; a cymbal crash would flash a blue strobe.

Colorgan applies this principle to video instead of audio. The "signal" is the average luminance of each video frame, and the "lights" are colored zones rendered directly onto the screen. The metaphor is the same: slow-moving energy drives warm colors, fast transients drive cool flashes.

### IIR envelope followers

The bass and mid bands are extracted using ***infinite impulse response*** (IIR) filters: a common technique in digital signal processing for smoothing a signal over time. An IIR filter computes its output as a weighted sum of the current input and its own previous output:

$$y[n] = (1 - \alpha) \cdot y[n-1] + \alpha \cdot x[n]$$

A small $\alpha$ (like 1/16 for the bass filter) means the output changes very slowly: it "remembers" past values for many frames. A larger $\alpha$ (like 1/4 for the mid filter) lets the output track the input more quickly. The treble band bypasses filtering entirely and uses the instantaneous difference between the frame average and the fast filter output, capturing only rapid changes.

### Additive color mixing

Colorgan uses ***additive color mixing*** in the YUV color space. Each frequency band contributes independently to the U and V chroma channels. Where two or more bands overlap spatially, their color contributions sum, producing blended hues. Bass red plus mid green yields yellow; bass red plus treble blue yields magenta. The warm palette is arranged so that bass occupies the warm end of the spectrum (red/orange), while the cool palette shifts the mapping toward blues and cyans. The luminance channel (Y) receives the sum of all band contributions, so brighter zones correspond to areas where more bands are active simultaneously.


---

## Signal Flow

### Signal Flow Notes

The signal path splits into two timescales. The ***luminance analysis*** stage runs once per frame at the vertical sync boundary: it computes the average brightness of the entire frame, feeds it through two IIR filters with different time constants, and derives three band levels (bass, mid, treble). These levels persist for the duration of the next frame.

The ***zone rendering*** stage runs every pixel clock. It computes each pixel's Manhattan distance from the center of the screen, determines which spatial zone the pixel falls within (based on the Layout toggle and Zone Width parameter), and multiplies the appropriate band level by the corresponding sensitivity knob. The three band contributions are summed into luminance and mapped to chroma using the selected palette. Finally, the rendered zones are crossfaded with the delayed input video via the Mix fader.

:::tip
Because the band levels update only once per frame (at vsync), the color zones hold steady within each frame and transition smoothly from frame to frame. This gives Colorgan its characteristic slow, breathing quality rather than pixel-level jitter.
:::


---

## Exercises

These exercises progress from a simple color pulse to a full three-band light show. Each one adds layers of interaction between the frequency bands, spatial layout, and color palette.
### Exercise 1: Single-Band Pulse

![Single-Band Pulse result](/img/instruments/videomancer/colorgan/colorgan_ex1_s1.png)
*Single-Band Pulse — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A single pulsing red zone that breathes with the video's overall brightness (the simplest possible color organ configuration.)

#### Key Concepts

- The bass band tracks slow brightness changes via IIR filtering
- Zone Width controls the spatial footprint
- The warm palette maps bass to red

#### Steps

1. Connect a video source with gradual brightness changes (a camera panning across a room, or footage of clouds).
2. Turn **Bass Zone** (Knob 1) fully clockwise to maximum sensitivity.
3. Set **Mid Zone** (Knob 2) and **Treble Zone** (Knob 3) to 0% (fully counterclockwise. Only the bass band is active now.)
4. Set **Zone Width** (Knob 4) to about 75% so the bass zone fills most of the screen.
5. Make sure **Layout** (Switch 7) is set to **Concentric** and **Palette** (Switch 8) is set to **Warm**.
6. Set **Mix** (Fader 12) to 100%. You should see a red glow that slowly swells and fades as the video's average brightness changes.
7. Switch **Palette** (Switch 8) to **Cool**. The red glow becomes blue.

#### Settings

| Control | Value |
|---------|-------|
| Bass Zone | 100% |
| Mid Zone | 0% |
| Treble Zone | 0% |
| Zone Width | 75% |
| Hue Offset | 0d |
| Decay | 0% |
| Layout | Concentric |
| Palette | Warm |
| React | Smooth |
| Video Mod | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Three-Band Light Show

![Three-Band Light Show result](/img/instruments/videomancer/colorgan/colorgan_ex2_s1.png)
*Three-Band Light Show — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A full three-band color organ with all zones visible, using both layout modes.

#### Key Concepts

- Three frequency bands occupy different spatial zones
- Concentric mode places treble at center, bass at rim
- Layered mode stacks bands as horizontal stripes
- Additive mixing creates blended hues where zones overlap

#### Steps

1. Set **Bass Zone** (Knob 1), **Mid Zone** (Knob 2), and **Treble Zone** (Knob 3) all to about 80%.
2. Set **Zone Width** (Knob 4) to about 50% and **Mix** (Fader 12) to 100%.
3. Feed the program a video with mixed content: scene cuts, camera motion, and brightness variation. You should see three colored zones pulsing at different rates: bass (red) breathes slowly at the edges, mid (green) flickers in the middle ring, and treble (blue) flashes at the center with each cut or sudden brightness change.
4. Flip **Layout** (Switch 7) to **Layered**. The concentric target becomes three horizontal stripes: treble at top, mid in the middle, bass at bottom.
5. Switch **Palette** (Switch 8) to **Cool**. The color mapping shifts (bass becomes blue, treble shifts toward violet.)
6. Adjust **Zone Width** (Knob 4) while watching the concentric mode. Smaller values compress the rings; larger values spread them across the screen.

#### Settings

| Control | Value |
|---------|-------|
| Bass Zone | 80% |
| Mid Zone | 80% |
| Treble Zone | 80% |
| Zone Width | 50% |
| Hue Offset | 0d |
| Decay | 59% |
| Layout | Concentric |
| Palette | Warm |
| React | Sharp |
| Video Mod | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Color Wash Overlay

![Color Wash Overlay result](/img/instruments/videomancer/colorgan/colorgan_ex3_s1.png)
*Color Wash Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A gentle color wash overlay on top of your source footage, using the color organ as a tinting layer rather than a standalone pattern.

#### Key Concepts

- Low Mix values blend the color organ subtly over input video
- Different sensitivity ratios emphasize different bands
- The combined effect creates a tinted, rhythmic overlay

#### Steps

1. Set **Mix** (Fader 12) to about 70%: enough to see the color organ clearly while the source video remains visible underneath.
2. Set **Bass Zone** (Knob 1) to about 50%, **Mid Zone** (Knob 2) to about 40%, and **Treble Zone** (Knob 3) to about 30%. This creates a bass-dominant wash that tints the video warmly during sustained brightness.
3. Set **Zone Width** (Knob 4) to about 80% so the zones spread broadly, creating an even wash rather than a tight spotlight.
4. Set **Layout** (Switch 7) to **Concentric** and **Palette** (Switch 8) to **Warm**. The video now has a warm, pulsing color cast that responds to its own brightness.
5. Try pulling **Mix** down to 20%. The effect becomes very subtle: a barely perceptible warm tint that shifts with scene changes.
6. Push **Treble Zone** (Knob 3) to 100% while leaving **Mix** at 20%. Even with the subtle mix, sharp cuts in the video now produce brief flashes of blue at the center of the screen.
7. Flip **Palette** (Switch 8) to **Cool**. The warm wash becomes an icy blue-cyan tint.

#### Settings

| Control | Value |
|---------|-------|
| Bass Zone | 50% |
| Mid Zone | 40% |
| Treble Zone | 30% |
| Zone Width | 80% |
| Hue Offset | 33d |
| Decay | 70% |
| Layout | Concentric |
| Palette | Warm |
| React | Smooth |
| Video Mod | Off |
| Bypass | Off |
| Mix | 70% |

---
## Glossary

- **Additive Mixing**: Combining color contributions by summing their values; overlapping zones produce brighter, blended hues.

- **Chroma**: The color information in a video signal, encoded as U and V components in YUV color space.

- **Color Organ**: An instrument that translates a signal (originally audio, here video) into colored light by splitting it into frequency bands.

- **Envelope Follower**: A circuit or algorithm that tracks the amplitude of a signal over time, producing a smooth curve that rises and falls with the signal's energy.

- **IIR Filter**: Infinite impulse response filter; a digital filter whose output depends on both the current input and its own previous output, producing exponential smoothing.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness.

- **Manhattan Distance**: The sum of horizontal and vertical offsets between two points, producing diamond-shaped contours rather than circles.

- **Time Constant**: The duration over which an IIR filter's impulse response decays to approximately 37% of its initial value; longer time constants mean slower, smoother tracking.

---
