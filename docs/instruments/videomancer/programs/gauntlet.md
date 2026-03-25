---
draft: true
sidebar_position: 124
slug: /instruments/videomancer/gauntlet
title: "Gauntlet"
image: /img/instruments/videomancer/gauntlet/gauntlet_hero_s1.png
description: "Every pixel of a video signal carries brightness and color — smooth gradients, soft shadows, gentle transitions."
---

![Gauntlet hero image](/img/instruments/videomancer/gauntlet/gauntlet_hero_s1.png)
*Gauntlet rendering a live camera feed as luminous green vector beam traces with phosphor persistence, evoking a 1980s arcade vector display.*

---

## Overview

Gauntlet transforms conventional raster video into a glowing vector display: a CRT beam trace rendering where only edges and transitions are visible, drawn with luminous beams that fade slowly over time. The effect recreates the look of classic vector arcade monitors like those in ***Asteroids***, ***Tempest***, and ***Battlezone***, where electron beams drew bright lines directly onto the phosphor screen rather than scanning in horizontal raster lines.

The pipeline detects horizontal edges in the incoming video, renders each edge as a bright beam with an exponential glow falloff, applies vertical phosphor persistence through a BRAM-based IIR line buffer, and colorizes the result using one of eight selectable phosphor modes. The result can either replace the input video entirely for a pure vector look, or be additively composited over the dimmed original for a mixed vector-raster display.

### What's In a Name?

A ***gauntlet*** is an armored glove, a challenge, and the name of an iconic dungeon-crawling arcade game. Here it refers to the ordeal every video frame endures: stripped to its edges, redrawn as pure light, and left to fade on the screen. The name captures the adversarial nature of the processing: the image is broken apart, and only its strongest features survive as vector traces.

---

## Quick Start

1. Feed any video source into Videomancer with Gauntlet loaded. Glowing green lines appear wherever the image has strong horizontal edges.
2. Turn **Sensitivity** (Knob 1) down to about 30% to reveal finer edges. Higher sensitivity means fewer edges (only the strongest transitions survive.)
3. Increase **Persistence** (Knob 3) to about 70%. The beam traces now linger on screen, building up a persistent afterimage that fades slowly.
4. Switch **Phosphor** (Switch 7) to Rainbow to see the beam traces rendered in scanline-varying color instead of monochrome green.

---

## Parameters

![Videomancer front panel with Gauntlet loaded](/img/instruments/videomancer/gauntlet/gauntlet_control_panel.png)
*Videomancer's front panel with Gauntlet active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Sensitivity

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Sensitivity** controls the edge detection threshold. At low values, even subtle gradients in the source video produce visible beam traces, creating a dense field of glowing lines. As the value increases, only strong high-contrast transitions survive the threshold, resulting in fewer but more prominent traces. At 100%, only the most extreme brightness jumps produce any output.

:::note
Sensitivity works inversely to how you might expect: ***lower*** values reveal ***more*** edges. Think of it as a minimum contrast requirement: a low requirement means nearly everything qualifies.
:::

---

### Knob 2 — Beam Width

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Beam Width** selects one of three glow falloff curves that determine how the beam light spreads horizontally from each detected edge. At low values (0–33%), the beam uses a ***narrow*** exponential decay that drops to zero within a few pixels: producing sharp, fine lines. At mid-range (34–66%), a ***medium*** curve creates broader, softer glows. At high values (67–100%), the ***wide*** curve spreads light across many pixels, producing large luminous halos around each edge.

---

### Knob 3 — Persistence

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Persistence** controls the vertical phosphor decay rate. At low values, the beam traces vanish within a single frame: each scanline sees only the current frame's edges. As persistence increases, the previous frame's beam intensity is decayed less aggressively before being compared against the new glow: at 25% the decay rate is 50% per frame; at 50% it drops to 25%; at 75%, only 12.5%; and at high persistence, just 6.25% per frame. This creates the slow, additive phosphor afterglow characteristic of long-persistence CRT phosphors.

:::tip
At very high persistence, moving subjects leave ghostly trails that build up over time. Try slowly panning a camera across a static scene for a "light painting" effect.
:::

---

### Knob 4 — Intensity

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Intensity** scales the overall brightness of the beam output after persistence processing. At 0%, the beam is black regardless of edge detection. At full intensity, the brightest edges produce fully saturated phosphor color. The scaling is multiplicative: it amplifies or attenuates the entire beam signal before colorization.

---

### Knob 5 — Hue Offset

| Property | Value |
|----------|-------|
| Range | 0.0d – 360.0d |
| Default | 0.0d |

**Hue Offset** rotates the phosphor color around the color wheel. The effect varies depending on the selected phosphor mode. In monochrome modes (Green, Amber, White, etc.), this shifts the base hue. In Rainbow mode, it rotates the starting point of the scanline-varying hue cycle. The range covers a full 360° rotation.

---

### Knob 6 — Focus

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Focus** adjusts the edge detection signal processing. This parameter modifies the sensitivity threshold scaling, sharpening or softening the boundary between detected and undetected edges. Lower values produce a crisper, more binary distinction. Higher values allow more gradual transitions to pass through.

---

### Switch 7 — Phosphor

| Property | Value |
|----------|-------|
| Off | Green |
| On | Rainbow |
| Default | Green |

**Phosphor** selects the color palette for the beam rendering. The toggle cycles through eight modes encoded as a 3-bit value:

- **Green** (000): Classic P1 phosphor, as seen on ***Battlezone*** and early vector monitors. Deep green with reduced chroma.
- **Blue-Green** (001): P31 phosphor, the color of ***Tempest*** and ***Star Castle***. Cool cyan-green.
- **Amber** (010): P22 amber phosphor, warm and vintage.
- **RGB** (011): Derives color from the input video's chroma. The beam brightness comes from edge detection, but the hue is inherited from the original image.
- **Cyan** (100): The blue-white of Cinematronics vector displays.
- **White** (101): Pure achromatic beam, like a monochrome oscilloscope.
- **Red** (110): Bright red beam on a dark background.
- **Rainbow** (111): Hue varies with scanline position, creating a rainbow-striped vector display.

---

### Switch 8 — Edge Mode

| Property | Value |
|----------|-------|
| Off | Binary |
| On | Gradient |
| Default | Binary |

**Edge Mode** switches between two edge rendering styles. In **Binary** mode, edges are either fully on or fully off: any gradient above the sensitivity threshold produces a full-brightness beam trace. In **Gradient** mode, the beam brightness is proportional to the gradient magnitude, so subtle edges produce dim traces and strong edges produce bright ones. Gradient mode creates a more nuanced, photographic rendering where the beam varies in intensity across the image.

---

### Switch 9 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** flips the input luminance before edge detection. With inversion **Off**, the video is processed as-is. With inversion **On**, the Y channel is bitwise inverted before processing, which swaps which edges are detected: dark-to-light transitions become light-to-dark and vice versa. On most source material this produces a similar but subtly different edge map.

---

### Switch 10 — Over Video

| Property | Value |
|----------|-------|
| Off | Replace |
| On | Overlay |
| Default | Replace |

**Over Video** controls how the beam traces composite against the background. In **Replace** mode, the output is purely the vector beam rendering: the original video is discarded. In **Overlay** mode, the beam traces are additively composited over the original video, which is dimmed to 25% brightness. This lets the source content show through behind the glowing vector lines.

:::tip
Overlay mode works well for live performance where the audience needs to see both the subject and the vector interpretation. The dimmed background provides context while the bright beams draw the eye.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Gauntlet processing. The sync delay pipeline still aligns timing. Use Bypass for instant A/B comparison.

---

:::note Toggle Group Notes

When using the TOML's `steps_8` control mode, all three low bits of the toggle register are used together as a single 3-bit selector. The `control_mode = "steps_8"` is misleading in the TOML: the hardware presents this as a two-position toggle (Green/Rainbow) but the VHDL reads a 3-bit value. On hardware, Switch 7 selects between the first (Green, 000) and last (Rainbow, 111) phosphor modes; intermediate modes are accessible via MIDI or preset recall.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) signal and the wet (Gauntlet-processed) signal. At 0%, only the original video is output. At 100%, only the vector beam rendering passes through. Intermediate values blend the two, which can create a subtle edge-enhancement effect at low mix percentages.

---

## Background

### Vector CRT displays

Early video arcade games used ***vector displays***, sometimes called XY monitors, where the electron beam was steered to draw lines directly on the phosphor screen rather than scanning in horizontal raster lines. This produced sharp, bright lines with smooth geometry, but no filled areas or photographic images. Games like ***Asteroids*** (1979), ***Tempest*** (1981), and ***Star Wars*** (1983) used vector monitors for their visually distinctive wireframe graphics. The bright, persistent glow of phosphor traces against a dark background became an iconic visual style.

### Edge detection and beam rendering

Gauntlet performs horizontal edge detection by computing the absolute difference between adjacent pixels: `|Y(x) - Y(x-1)| × 2 + |U(x) - U(x-1)| + |V(x) - V(x-1)|`. The Y (luminance) channel is weighted double relative to the chroma channels, reflecting the human eye's greater sensitivity to brightness changes. Pixels where this weighted gradient exceeds the sensitivity threshold are flagged as edges and entered into a 16-tap shift register, which tracks the positions of the nearest recent edges for the glow falloff computation.

### Phosphor persistence

Real vector CRT monitors use long-persistence phosphors: chemical coatings that continue to glow for hundreds of milliseconds after the electron beam has moved on. This persistence is what makes vector graphics visible: the beam draws each frame in sequence, and the phosphor afterglow bridges the gap until the beam returns. Gauntlet simulates this with a BRAM-based ***IIR line buffer*** that stores the previous frame's beam intensity for each horizontal pixel position. Each new frame, the stored value is decayed by a configurable amount and compared against the new beam glow: the brighter of the two survives. This "max of new and decayed" approach mimics the way phosphor brightness builds up when the beam revisits the same position.


---

## Signal Flow

### Signal Flow Notes

The gradient calculation weights luminance double relative to chroma (`|ΔY|×2 + |ΔU| + |ΔV|`), which means the edge detector is primarily driven by brightness transitions. Color-only edges (same brightness, different hue) produce a weaker gradient signal and need lower sensitivity thresholds to trigger.

The 16-tap edge shift register is the core of the beam glow system. As each new pixel is processed, the shift register records whether an edge was detected at that position. The nearest-edge priority encoder scans the register to find the closest edge, and the glow LUT translates that distance into a brightness value. This creates a horizontal "halo" of light spreading outward from each edge, with brightness falling off exponentially: exactly how a defocused electron beam spreads on a phosphor screen.

:::warning
The persistence line buffer stores values per horizontal pixel position, not per 2D screen position. This means vertical movement creates trails, but horizontal movement does not persist: the persistence operates vertically across successive scanlines at the same X position.
:::


---

## Exercises

These exercises progress from basic edge detection through to a full vector CRT simulation with persistence and color.
### Exercise 1: Basic Edge Detection

![Basic Edge Detection result](/img/instruments/videomancer/gauntlet/gauntlet_ex1_s1.png)
*Basic Edge Detection — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean vector-line rendering of a live camera feed, showing bright white edges on a black background.

#### Key Concepts

- Horizontal gradient detection reveals edges as bright lines
- Sensitivity controls which edges are visible
- Binary vs. Gradient mode changes the rendering character

#### Video Source

A scene with strong geometric features: architectural elements, text, or household objects with clear edges.

#### Steps

1. Set **Phosphor** (Switch 7) to Green and **Edge Mode** (Switch 8) to Binary.
2. Set **Sensitivity** (Knob 1) to ~40%. Strong edges appear as bright green lines.
3. Set **Intensity** (Knob 4) to ~80% and **Persistence** (Knob 3) to 0%.
4. Switch **Edge Mode** to Gradient. Notice how the beam brightness now varies with edge strength (subtle gradients produce dim traces.)
5. Lower **Sensitivity** to ~20% to reveal more detail.

#### Settings

| Control | Value |
|---------|-------|
| Sensitivity | ~40% (step 2) / ~20% (step 5) |
| Beam Width | ~50% |
| Persistence | ~0% |
| Intensity | ~80% |
| Hue Offset | 0° |
| Focus | ~50% |
| Phosphor | Green |
| Edge Mode | Binary (step 2) / Gradient (step 4) |
| Invert | Off |
| Over Video | Replace |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 2: Phosphor Persistence CRT

![Phosphor Persistence CRT result](/img/instruments/videomancer/gauntlet/gauntlet_ex2_s1.png)
*Phosphor Persistence CRT — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A glowing vector display with phosphor trails, where moving objects leave persistent afterimages (as if drawn on a long-persistence oscilloscope.)

#### Key Concepts

- Persistence creates temporal afterglow across frames
- Decay rate determines how long traces linger
- The IIR line buffer accumulates brightness over time

#### Video Source

A slowly moving subject: a hand, a pendulum, or a face turning slowly: for visible phosphor trails.

#### Steps

1. From the Exercise 1 setup, increase **Persistence** (Knob 3) to ~70%.
2. Move your subject slowly. Bright trails follow the edges, fading gradually.
3. Increase **Beam Width** (Knob 2) to ~80% for wider, softer glow halos.
4. Set **Intensity** (Knob 4) to ~90%. The beam traces become brilliant against the persistence tail.
5. Try **Over Video** (Switch 10) on Overlay to see the ghostly original image behind the vector traces.

#### Settings

| Control | Value |
|---------|-------|
| Sensitivity | ~30% |
| Beam Width | ~80% |
| Persistence | ~70% |
| Intensity | ~90% |
| Hue Offset | 0° |
| Focus | ~50% |
| Phosphor | Green |
| Edge Mode | Gradient |
| Invert | Off |
| Over Video | Replace (step 1) / Overlay (step 5) |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 3: Rainbow Arcade Machine

![Rainbow Arcade Machine result](/img/instruments/videomancer/gauntlet/gauntlet_ex3_s1.png)
*Rainbow Arcade Machine — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A polychromatic vector CRT display where beam traces shift through rainbow colors, composited over the dimmed original video (a psychedelic arcade monitor from an alternate timeline.)

#### Key Concepts

- Rainbow mode varies hue with scanline position
- Overlay compositing layers beam traces over dimmed video
- Combining all processing stages creates a complete CRT simulation

#### Video Source

High-contrast footage with mixed motion and static elements: a performer against a patterned background, or geometric video art.

#### Steps

1. Set **Phosphor** (Switch 7) to Rainbow. The beam traces now cycle through the color wheel.
2. Enable **Over Video** (Switch 10) for Overlay. The original video shows through at 25% behind the vector beams.
3. Set **Persistence** to ~80%, **Beam Width** to ~60%, **Intensity** to ~85%.
4. Set **Edge Mode** to Gradient for variable-brightness beams.
5. Turn **Hue Offset** (Knob 5) to rotate the starting hue of the rainbow pattern.
6. Enable **Invert** (Switch 9). The edge map flips, revealing a different set of beam traces from the same source.

#### Settings

| Control | Value |
|---------|-------|
| Sensitivity | ~35% |
| Beam Width | ~60% |
| Persistence | ~80% |
| Intensity | ~85% |
| Hue Offset | ~120° |
| Focus | ~50% |
| Phosphor | Rainbow |
| Edge Mode | Gradient |
| Invert | On |
| Over Video | Overlay |
| Bypass | Off |
| Mix | ~100% |

---
## Glossary

- **BRAM**: Block RAM; dedicated memory blocks within the iCE40 FPGA, used here for the persistence line buffer.

- **Edge Detection**: The process of identifying pixels where brightness or color changes abruptly, indicating a boundary between regions.

- **Glow Falloff**: The exponential decay of beam brightness with distance from a detected edge, simulating the spread of light from a defocused electron beam.

- **IIR**: Infinite Impulse Response; a feedback filter where the output depends on both current input and previous output, used here for phosphor persistence.

- **Persistence**: The tendency of CRT phosphors to continue glowing after the electron beam has moved on, creating a temporal afterimage.

- **Phosphor**: A chemical coating on the inside of a CRT screen that glows when struck by an electron beam. Different phosphor compounds produce different colors and decay rates.

- **Priority Encoder**: A combinational logic circuit that finds the position of the first active bit in a binary vector (used here to find the nearest detected edge.)

- **Raster Display**: A CRT that scans the electron beam in horizontal lines from top to bottom, filling the screen with a grid of pixels. Contrasted with vector displays.

- **Shift Register**: A chain of flip-flops that passes data from one to the next on each clock cycle, creating a sliding window of historical values.

- **Vector Display**: A CRT display where the electron beam is steered to draw lines directly, rather than scanning in raster lines.

---
