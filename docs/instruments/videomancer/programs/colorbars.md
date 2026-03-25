---
draft: true
sidebar_position: 57
slug: /instruments/videomancer/colorbars
title: "Colorbars"
image: /img/instruments/videomancer/colorbars/colorbars_hero_s1.png
description: "Every video engineer's first instinct when commissioning a new system is to call up color bars."
---

![Colorbars hero image](/img/instruments/videomancer/colorbars/colorbars_hero_s1.png)
*Seven perfectly rendered SMPTE color bars spanning the full frame, their luminance and chroma independently scaled to reveal the underlying YUV structure of broadcast video.*

---

## Overview

**Colorbars** is a ***synthesis*** program that generates SMPTE-style color bar test patterns from scratch, without requiring any video input. It produces seven vertical bars: White, Yellow, Cyan, Green, Magenta, Red, and Blue: at selectable 75% or 100% amplitude, the two standard levels used in broadcast engineering. Independent brightness and saturation controls let you reshape the bars for creative use beyond simple calibration.

Because Colorbars is a synthesis program, it creates its own imagery rather than processing an incoming signal. The **Mix** fader blends between the generated bars and whatever video is passing through the input, enabling smooth crossfades between test patterns and live material. A **Mono** toggle strips the chroma channels, producing a pure grayscale staircase (useful for isolating luminance behavior in a signal chain.)

:::note
Colorbars auto-measures the active video resolution from the input timing signals, so its bars are correctly proportioned at any supported video standard: SD, HD, or anything in between.
:::

### What's In a Name?

The name ***Colorbars*** is literal. These are the same color bars that have been the universal language of video engineering since the 1970s. Every television station, every broadcast truck, every post-production facility speaks this language. When you see color bars, you know the signal chain is alive and calibrated. Videomancer's Colorbars puts this essential tool directly inside the video synthesis signal path.

---

## Quick Start

1. With all controls at their defaults, Colorbars displays a full-brightness set of seven vertical bars at **75%** amplitude. The bars fill the screen from left to right: white, yellow, cyan, green, magenta, red, blue.
2. Flip the **Level** toggle (Switch 7) to **100%**. The bars punch up to full saturation: yellows become more vivid, blues deepen. This is the difference between SMPTE 75% and 100% amplitude bars.
3. Slowly turn **Y Level** (Knob 1) counterclockwise. The entire pattern dims evenly, as if a master brightness control were being lowered. The bars fade toward black.
4. Now turn **C Level** (Knob 2) counterclockwise. The colors desaturate toward neutral gray while brightness stays unchanged. When C Level reaches zero, the bars become a pure grayscale staircase.

---

## Parameters

![Videomancer front panel with Colorbars loaded](/img/instruments/videomancer/colorbars/colorbars_control_panel.png)
*Videomancer's front panel with Colorbars active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Y Level

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Y Level** controls the overall brightness gain of the generated color bars. At 100%, fully clockwise (the default), the luminance values match the standard SMPTE specification. As you turn the knob counterclockwise, all bars dim proportionally: white becomes gray, yellow becomes olive, and so on. At 0%, the entire pattern goes to black.

Y Level scales the raw luminance by multiplying each bar's Y value by the knob position and dividing by 1024, so the control is perfectly linear from full black to full brightness.

---

### Knob 2 — C Level

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**C Level** controls the chroma saturation gain of the generated bars, independently of brightness. At 100% (the default), the U and V channels carry their full SMPTE-specified deviation from the neutral midpoint. As you decrease C Level, colors desaturate toward gray while their brightness remains unchanged. At 0%, all chroma is removed and the bars become a grayscale luminance staircase.

:::tip
Setting **Y Level** to maximum and **C Level** to zero produces a perfect grayscale step wedge: seven bars of descending brightness with no color. This is a classic tool for checking monitor brightness and contrast calibration.
:::

---

### Knob 3 — —

| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 50 |

This control is reserved for future use. Adjusting Knob 3 has no effect on the output.

---

### Knob 4 — —

| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 50 |

This control is reserved for future use. Adjusting Knob 4 has no effect on the output.

---

### Knob 5 — —

| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 50 |

This control is reserved for future use. Adjusting Knob 5 has no effect on the output.

---

### Knob 6 — —

| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 50 |

This control is reserved for future use. Adjusting Knob 6 has no effect on the output.

---

### Switch 7 — Level

| Property | Value |
|----------|-------|
| Off | 75% |
| On | 100% |
| Default | 75% |

**Level** selects between the two standard color bar amplitudes. In the **75%** position (the default), the bars conform to the SMPTE 75% amplitude specification: colors are muted to the levels traditionally used for routine signal alignment. In the **100%** position, the bars use full-amplitude YUV values, producing the most saturated colors the standard permits.

:::note
The 75% and 100% labels refer to the ***chroma amplitude relative to full scale***, not to the brightness of the white bar. At 75%, the white bar's Y value is 767 (out of 1023). At 100%, the white bar reaches 1023.
:::

---

### Switch 8 — Order

| Property | Value |
|----------|-------|
| Off | Normal |
| On | Reverse |
| Default | Normal |

**Order** controls the horizontal sequence of the seven bars. In the **Normal** position (the default), bars appear left to right in descending luminance order: White, Yellow, Cyan, Green, Magenta, Red, Blue. In the **Reverse** position, the order flips: Blue, Red, Magenta, Green, Cyan, Yellow, White.

Reversing the order can be useful for creative compositions or for checking that downstream processing treats both halves of the chroma spectrum symmetrically.

---

### Switch 9 — —

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

This toggle is reserved for future use. Changing Switch 9 has no effect on the output.

---

### Switch 10 — —

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

This toggle is reserved for future use. Changing Switch 10 has no effect on the output.

---

### Switch 11 — Mono

| Property | Value |
|----------|-------|
| Off | Color |
| On | Mono |
| Default | Color |

**Mono** strips the chroma channels from the generated bars, forcing U and V to their neutral midpoint (512). In the **Color** position (the default), bars display their full YUV color. In the **Mono** position, bars become a grayscale staircase showing only the luminance component of each bar.

:::tip
**Mono** differs from setting **C Level** to zero in a subtle way. Mono forces U and V to exactly 512 in hardware, while C Level at zero *scales* the chroma deviation to zero through multiplication. The visual result is identical, but Mono is a clean digital switch while C Level is a continuous gain.
:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the input video signal and the generated color bars. At 100% (the default), only the synthesized bars appear. At 0%, the input video passes through unchanged. Intermediate positions blend the two signals together, allowing color bars to be overlaid at partial opacity on live video.

The Mix fader uses a four-stage interpolator for smooth, glitch-free crossfading.

:::warning
At 0% Mix, Colorbars acts as a simple passthrough. The bars are still being generated internally, but they are not visible in the output.
:::

---

## Background

### Color Bars and Broadcast History

Color bars are the oldest and most universal test pattern in television. The ***SMPTE color bar*** pattern was standardized by the Society of Motion Picture and Television Engineers and has been used since the early days of color broadcasting. Its seven bars: white, yellow, cyan, green, magenta, red, and blue: are arranged in descending luminance order, creating a staircase that exercises every combination of the three primary color components.

In broadcast facilities, color bars are transmitted before a program to allow engineers at the receiving end to calibrate their equipment. The pattern exercises the full gamut of the color system: the white bar tests peak luminance, the saturated colors test chroma accuracy, and the descending brightness staircase tests the linearity of the luminance path. The 75% amplitude variant is the everyday workhorse; the 100% variant pushes the system to its limits.

### YUV Color Representation

Colorbars generates its output in ***YUV 4:4:4*** color space, the native format of Videomancer's video pipeline. Each pixel has three 10-bit components: ***Y*** (luminance, or brightness), ***U*** (blue-difference chroma), and ***V*** (red-difference chroma). The luminance channel ranges from 0 (black) to 1023 (peak white). The chroma channels are centered at 512 (neutral gray), with deviations above and below representing color in opposite directions.

This separation of brightness from color is what makes the **Y Level** and **C Level** controls possible. Because luminance and chrominance are independent channels, Colorbars can scale them separately without artifacts: something that would require complex matrix math in an RGB color space.

### Resolution-Independent Rendering

Colorbars uses a ***digital differential analyzer*** (DDA) to divide the active video line into seven equal bars without hardware division. An accumulator adds seven to its value at each pixel clock. When the accumulator reaches or exceeds the measured line width, it wraps around and advances to the next bar index. This technique adapts automatically to any resolution: the bars are always evenly spaced regardless of whether the video format is 720×480, 1280×720, or 1920×1080.

The active line width is auto-measured by counting pixels between horizontal sync edges. This measurement updates every line, so the bars remain correctly proportioned even if the video format changes dynamically.


---

## Signal Flow

### Signal Flow Notes

The Colorbars pipeline separates timing analysis from color generation. The video timing generator extracts edge-detected sync signals from the input, and the resolution measurement counts active pixels per line. These two systems feed the DDA bar index calculator, which determines which of the seven bars corresponds to the current pixel position.

The bar generation pipeline is a two-stage process: first, the appropriate YUV triple is read from a lookup table (selected by the 75/100% toggle and the optional reverse), and then gain scaling is applied independently to luminance and chroma. The chroma gain preserves the neutral midpoint: it scales the *deviation* from 512, not the raw value: so reducing C Level always converges toward neutral gray rather than toward zero.

:::tip
The total pipeline delay is 16 clock cycles (10 processing + 4 interpolator + 2 IO alignment), chosen to be divisible by 4 for compatibility with the video core's clock division architecture.
:::


---

## Exercises

These exercises explore Colorbars as both a calibration tool and a creative element in a video synthesis signal chain.
### Exercise 1: Grayscale Staircase

![Grayscale Staircase result](/img/instruments/videomancer/colorbars/colorbars_ex1_s1.png)
*Grayscale Staircase — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Use Colorbars to generate a pure grayscale luminance staircase for monitor calibration.

#### Key Concepts

- Separating luminance from chroma reveals the brightness structure of the color bar pattern
- The seven bars form a descending staircase of brightness levels
- Grayscale bars are the foundation of contrast and brightness calibration

#### Steps

1. **Default color bars**: Start with all controls at their defaults. The screen displays seven colored bars at 75% amplitude.
2. **Strip the color**: Toggle **Mono** (Switch 11) to the **Mono** position. The bars become seven shades of gray, from bright white on the left to near-black on the right.
3. **Full amplitude**: Switch **Level** (Switch 7) to **100%**. The white bar reaches peak brightness and the steps between bars become more pronounced.
4. **Dim the staircase**: Slowly turn **Y Level** (Knob 1) counterclockwise. The entire staircase dims evenly. Find the point where the darkest bar just disappears into black (this reveals the monitor's black level.)
5. **Check separation**: Return **Y Level** to maximum. Observe that all seven steps are clearly distinguishable. If any adjacent bars merge, the monitor's contrast or gamma needs adjustment.

#### Settings

| Control | Value |
|---------|-------|
| Y Level | 100% |
| C Level | 100% |
| — | 50% |
| — | 50% |
| — | 50% |
| — | 50% |
| Level | 100% |
| Order | Normal |
| — | Off |
| — | Off |
| Mono | Mono |
| Mix | 100% |

---

### Exercise 2: Chroma vs. Luminance Isolation

![Chroma vs. Luminance Isolation result](/img/instruments/videomancer/colorbars/colorbars_ex2_s1.png)
*Chroma vs. Luminance Isolation — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Explore how independent Y and C controls separate brightness from color in the bar pattern.

#### Key Concepts

- YUV separates brightness (Y) from color (U, V)
- Chroma gain scales deviation from the neutral midpoint, not the raw value
- Independent control reveals the hidden structure of composite color

#### Steps

1. **Vivid starting point**: Start at defaults with **Level** set to **100%** for maximum color saturation. Seven vivid bars fill the screen.
2. **Drain the color**: Turn **C Level** (Knob 2) slowly to zero. The colors drain away, leaving a grayscale staircase. The brightness of each bar is unchanged (only the color disappears.)
3. **Remove all brightness**: Return **C Level** to 100%. Now turn **Y Level** (Knob 1) to zero. The entire screen goes black, because all luminance has been removed.
4. **Dim glow**: Set **Y Level** to about 50%. The bars are dim but still colored. Notice that the color saturation appears more vivid at low brightness (this is a perceptual effect.)
5. **Vivid on dark**: Slowly increase **C Level** while keeping **Y Level** at 50%. The bar colors become increasingly vivid against the dim background, demonstrating how chroma and luminance interact perceptually.

#### Settings

| Control | Value |
|---------|-------|
| Y Level | 50% |
| C Level | 100% |
| — | 50% |
| — | 50% |
| — | 50% |
| — | 50% |
| Level | 100% |
| Order | Normal |
| — | Off |
| — | Off |
| Mono | Color |
| Mix | 100% |

---

### Exercise 3: Bars as Creative Overlay

![Bars as Creative Overlay result](/img/instruments/videomancer/colorbars/colorbars_ex3_s1.png)
*Bars as Creative Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Use the Mix fader to blend color bars with an input video signal for creative compositing effects.

#### Key Concepts

- The Mix fader crossfades between input video and generated bars
- Partial mix creates a color-tinted overlay effect
- Reverse bar order changes the spatial distribution of color in the overlay

#### Steps

1. **Input passthrough**: Connect a video source to the input. Set **Mix** (Fader 12) to 0%. The input video passes through unchanged.
2. **Fade in the bars**: Slowly increase **Mix** toward 50%. The color bars fade in as a translucent overlay on top of the input video, tinting each vertical region of the frame with the corresponding bar color.
3. **Reverse the palette**: Toggle **Order** (Switch 8) to **Reverse**. The color distribution across the frame flips. Compare how different regions of the input interact with different bar colors.
4. **Soften the tint**: Reduce **C Level** (Knob 2) to about 30%. The overlay becomes more subtle (a gentle color wash rather than a saturated tint.)
5. **Shadow stripes**: Experiment with **Y Level** (Knob 1) at low values. The overlay darkens the input in the bar pattern, creating a venetian-blind shadow effect.

#### Settings

| Control | Value |
|---------|-------|
| Y Level | 100% |
| C Level | 30% |
| — | 50% |
| — | 50% |
| — | 50% |
| — | 50% |
| Level | 75% |
| Order | Reverse |
| — | Off |
| — | Off |
| Mono | Color |
| Mix | 50% |

---
## Glossary

- **Amplitude**: The peak level of a signal; 75% and 100% amplitude color bars differ in how far their chroma values deviate from neutral.

- **BT.601**: The ITU-R standard defining the YUV color encoding used for standard-definition video, specifying how RGB primaries map to luminance and chrominance.

- **Chroma**: The color information in a video signal, encoded as U (blue-difference) and V (red-difference) components centered at a neutral midpoint.

- **DDA**: Digital Differential Analyzer; an algorithm that divides a line into equal segments using only addition and comparison, avoiding hardware division.

- **Interpolator**: A circuit that smoothly blends between two values based on a fractional control input; used here for the wet/dry mix.

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **SMPTE**: Society of Motion Picture and Television Engineers; the standards body that defined the color bar test pattern and many other broadcast specifications.

- **Synthesis**: A program type that generates imagery from the program's own internal logic rather than processing an input video signal.

- **YUV**: A color space that separates brightness (Y) from color (U, V), allowing independent manipulation of luminance and chrominance.

---
