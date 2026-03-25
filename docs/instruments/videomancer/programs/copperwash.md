---
draft: true
sidebar_position: 66
slug: /instruments/videomancer/copperwash
title: "Copperwash"
image: /img/instruments/videomancer/copperwash/copperwash_hero.png
description: "Copper Wash generates per-scanline colour gradients that scroll vertically through the video frame, blending continuous rainbow bands with the input signal."
---

![Copperwash hero image](/img/instruments/videomancer/copperwash/copperwash_hero_s1.png)
*Copperwash painting a scrolling rainbow gradient across live video, tinting each scanline with a unique hue drawn from a sine-based color wheel.*

---

## Overview

Copperwash is a per-scanline color gradient synthesizer inspired by the legendary ***copper coprocessor*** of the Commodore Amiga. Every horizontal line receives a unique hue from a smooth, continuous rainbow that scrolls vertically over time. The gradient is computed using a sine-based hue-to-YUV conversion, producing bands of color that flow, shift, and morph in real time. The effect is blended with the input video via multiply or additive modes, transforming ordinary footage into a wash of animated color.

At gentle settings, Copperwash applies a subtle tint that shifts gradually from top to bottom, like a warm-toned photographic filter that changes mood with every frame. At extreme settings, the screen becomes a liquid cascade of scrolling rainbow bars: a real-time recreation of the copper-list color tricks that elevated Amiga demoscene productions into art.

:::tip
Copperwash excels as a ***color grading layer***. Use it in Multiply mode with low saturation to add time-varying warmth or coolness to any source. Stack it with other Videomancer programs for animated tinting that would be impossible to achieve with static filters.
:::

### What's In a Name?

The name ***Copperwash*** fuses the Amiga's ***copper*** coprocessor: a hardware unit that could change palette registers on every scanline: with the idea of a ***color wash***, a gradual tonal gradient laid over an image. In demoscene jargon, "copper bars" are horizontal bands of color produced by rapidly reprogramming the display palette mid-frame. Copperwash turns that classic trick into a continuous, infinitely smooth gradient that flows like liquid metal.

---

## Quick Start

1. With **Gradient Freq** (Knob 2) at about 40% and **Saturation** (Knob 4) and **Brightness** (Knob 6) both above 75%, you should see rainbow bars flowing down the screen. The smoothly shifting hues are a hallmark of the copper effect.
2. Turn **Scroll Speed** (Knob 1) slowly in either direction from center. The rainbow bands scroll upward or downward. At center, the gradient is stationary.
3. Increase **Wobble** (Knob 5). The straight horizontal color bars begin to ripple and undulate: each line's hue is nudged by a slow sinusoidal wave, creating a liquid, organic feel.
4. Flip **H Spread** (Switch 9) to On. The gradient now extends diagonally across the screen, adding a horizontal component to the vertical wash.

---

## Parameters

![Videomancer front panel with Copperwash loaded](/img/instruments/videomancer/copperwash/copperwash_control_panel.png)
*Videomancer's front panel with Copperwash active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Scroll Speed

| Property | Value |
|----------|-------|
| Range | -90deg – 90deg |
| Default | 12deg |

**Scroll Speed** controls the rate and direction at which the color gradient scrolls vertically. The control is ***bipolar***: at the 12 o'clock center position, the gradient is stationary. Turning clockwise increases the upward scroll speed; turning counterclockwise scrolls the gradient downward. Faster scroll speeds produce a continuously flowing waterfall of color, while values near center allow you to freeze the gradient in place and fine-tune its position.

:::note
Scroll Speed accumulates a phase offset on each vertical sync pulse. Even a tiny offset from center produces a slow drift over time. Set it exactly to center (0 deg) to lock the gradient in place.
:::

---

### Knob 2 — Gradient Freq

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Gradient Freq** sets how many color bands appear on screen at once. At low values, the gradient stretches across the full height of the display with gentle transitions between hues. As you increase Gradient Freq, the color cycle repeats more often, packing more bands into the frame. At maximum, the screen fills with rapid, fine-grained stripes of color. The frequency control scales the per-scanline phase increment: each additional unit of frequency multiplies how fast the hue rotates as the raster descends.

---

### Knob 3 — Hue Offset

| Property | Value |
|----------|-------|
| Range | -180deg – 180deg |
| Default | 0deg |

**Hue Offset** rotates the starting point of the gradient around the color wheel. This control is ***bipolar*** and wraps around 360 degrees. Fully counterclockwise shifts the starting hue 180 degrees in one direction; fully clockwise shifts it 180 degrees the other way. At center, the gradient begins at the default hue. Use Hue Offset to dial in the exact palette you want: shift the wash toward blue, red, green, or any point in between without changing the shape or speed of the gradient.

---

### Knob 4 — Saturation

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Saturation** controls the intensity of the gradient's color. At 0%, fully counterclockwise, the gradient produces no chrominance: only luminance variation appears, producing a monochrome wash. As Saturation increases, the colors become vivid and deeply saturated. At 100%, the chroma channels carry the full output of the sine-based hue converter. Saturation scales both the U and V components symmetrically, so the overall hue angle is preserved while the vividness changes.

:::tip
Pair low **Saturation** with the Multiply blend mode for a subtle, film-like tonal grade. Only a whisper of color appears, shifting gently from frame to frame.
:::

---

### Knob 5 — Wobble

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Wobble** adds a sinusoidal per-scanline phase modulation to the gradient. At 0%, the gradient follows perfectly straight horizontal lines. As Wobble increases, each scanline's hue is nudged by a slow sine wave, causing the color bands to ripple and undulate. The wobble animation is driven by its own independent time accumulator, so the ripple pattern drifts continuously even when Scroll Speed is at center. Higher Wobble values create a more dramatic liquid shimmer.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Brightness** scales the luminance of the generated gradient before it is blended with the input video. At 0%, the gradient produces no light: in Multiply mode this drives the output toward black; in Add mode it adds nothing. At 100%, the gradient's luminance is at full strength. In Multiply mode, Brightness effectively controls the depth of the tint: lower values darken the image more aggressively. In Add mode, Brightness controls how much luminance is added to the source.

---

### Switch 7 — Gradient

| Property | Value |
|----------|-------|
| Off | Rainbow |
| On | Mono |
| Default | Rainbow |

**Gradient** selects between rainbow and monochrome gradient modes. With the switch set to **Rainbow**, the hue sweeps continuously through the color wheel, producing full-spectrum bands of color. Each scanline receives a unique hue based on its vertical position, the current frequency, and scroll phase. With the switch set to **Mono**, the chroma channels are zeroed out and the gradient becomes a luminance-only wave (a rippling pattern of light and dark bands with no color.)

:::note
**Gradient** and **Blend** (Switch 8) together form a four-state gradient palette selector in the VHDL. When both are at their defaults (Rainbow + Multiply), you get the classic full-spectrum copper wash. See the Toggle Group Notes below for the complete interaction.
:::

---

### Switch 8 — Blend

| Property | Value |
|----------|-------|
| Off | Multiply |
| On | Add |
| Default | Multiply |

**Blend** selects how the generated gradient is combined with the input video. In **Multiply** mode, each pixel's luminance is scaled by the gradient's brightness: the gradient acts as a tint, coloring and darkening the source image. The chroma is averaged between the source and gradient. In **Add** mode, the gradient's luminance is added to the source with saturation clamping at maximum white, and the gradient's chroma completely replaces the source chroma.

:::tip
Multiply mode preserves the source image's structure while washing it with color: ideal for tinting and grading. Add mode creates a more aggressive overlay where the gradient glows on top of the source.
:::

---

### Switch 9 — H Spread

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**H Spread** adds a horizontal component to the gradient. With the switch **Off**, the gradient varies only in the vertical direction: every pixel on the same scanline shares the same hue. With the switch **On**, the horizontal pixel position also contributes to the gradient phase, creating a diagonal wash that sweeps across the screen at an angle. The slope of the diagonal is determined by **Gradient Freq**: higher frequencies produce steeper angles.

---

### Switch 10 — Smooth

| Property | Value |
|----------|-------|
| Off | Steps |
| On | Smooth |
| Default | Smooth |

**Smooth** controls the resolution of the gradient phase. With the switch set to **Smooth**, the gradient uses the full 10-bit phase, producing silky transitions between hues. With the switch set to **Steps**, the phase is quantized to 64 discrete levels, creating visible bands with hard edges between each color. The stepped look recalls the discrete palette entries of classic copper-list effects, while smooth mode takes advantage of the full analog range.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Copperwash processing and blending stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant before-and-after comparison between the raw input and the gradient-washed result.

---

:::note Toggle Group Notes

**Gradient** (Switch 7) and **Blend** (Switch 8) together form a combined four-mode gradient palette selector in the VHDL. The two toggle bits are packed into a 2-bit field (`s_gradient`) that selects the hue-to-YUV conversion algorithm. Simultaneously, the **Blend** toggle independently controls the blending mode (Multiply vs. Add). The four combined states are:

| Switch 7 (Gradient) | Switch 8 (Blend) | Gradient Mode | Blend Mode | Description |
|---|---|---|---|---|
| Rainbow | Multiply | **Rainbow** | Multiply | Full-spectrum hue sweep; Y = bright white. Classic copper bars |
| Mono | Multiply | **Warm** | Multiply | Blue attenuated, red boosted; Y = medium-high. Sunset palette |
| Rainbow | Add | **Cool** | Add | Red attenuated, blue boosted; Y = medium. Ocean palette |
| Mono | Add | **Mono** | Add | No chroma; Y = sine-modulated mid-gray. Luminance waves only |

:::warning
The display labels ("Rainbow" and "Mono" for Switch 7) simplify the four actual VHDL modes. The intermediate states (Warm and Cool) are accessed by combining both switches. Experiment with all four combinations to discover the full palette range.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry input signal and the wet gradient-blended output. At 0%, the output is entirely the unprocessed input. At 100%, the output is the full Copperwash effect. Intermediate values blend between the two using a per-channel ***linear interpolation***, allowing you to dial in exactly how much of the gradient wash is applied. The interpolator operates independently on Y, U, and V channels.

---

## Background

### The Amiga copper coprocessor

The Commodore Amiga's custom chipset included a remarkable piece of hardware called the ***copper***: a coprocessor that could reprogram the display hardware in sync with the raster beam. By waiting for specific scanlines and then jamming new color values into the palette registers, programmers could display far more colors on screen than the hardware's palette would normally allow. The signature visual result was horizontal bands of color: ***copper bars***: flowing smoothly down the screen. This technique became a defining aesthetic of the Amiga ***demoscene***, where programmers competed to push the hardware to its visual limits.

Copperwash translates this concept into a continuous analog domain. Instead of discrete palette entries switched at scanline boundaries, it computes a smooth sine-based gradient that produces infinitely variable hue transitions. The result is the same aesthetic: horizontal bands of color that flow and scroll: but with the richness of a 30-bit YUV color space.

### Sine-based hue conversion

The gradient's color is generated by evaluating sine and cosine functions of the gradient phase. In YUV color space, the U and V channels represent the chrominance, and a point on the color wheel can be described as U = sin(θ) and V = cos(θ), where θ is the hue angle. As the phase sweeps from 0 to 360 degrees, the color traces a full circle through the hue spectrum: red, yellow, green, cyan, blue, magenta, and back to red.

Copperwash implements this using a 256-entry quarter-wave ***lookup table*** (LUT) that stores one quadrant of the sine function. The other three quadrants are reconstructed by mirroring and negating, producing a complete 10-bit sine evaluation with no block RAM (only combinatorial logic.)

### Blend modes

The program offers two ways to combine the generated gradient with the input video:

- **Multiply** scales each input pixel's luminance by the gradient's brightness. Dark regions of the gradient suppress the source; bright regions let it through. The effect is like looking at the video through a tinted window that changes color on every scanline. Chroma is averaged between source and gradient.
- **Additive** adds the gradient's luminance to the source (with clamping at maximum white). The gradient glows on top of the image, and the gradient's chroma replaces the source chroma entirely. This mode produces vivid, fluorescent results.


---

## Signal Flow

### Signal Flow Notes

The gradient is computed entirely from the vertical scanline counter, timing accumulators, and control parameters: no block RAM is consumed. The sine LUT is synthesized as combinatorial logic, keeping the resource footprint small (approximately 500 LUTs, 0 BRAMs).

Two animation accumulators drive the time-varying behavior. The ***scroll accumulator*** is bipolar: at center (raw value 512), it adds zero per frame, freezing the gradient. Values above or below center scroll the gradient up or down. The ***wobble accumulator*** advances at a fixed rate of 3 per vsync, independent of any control: it provides a slow, continuous ripple animation that shapes the gradient when Wobble is non-zero.

:::tip
Because the wobble accumulator runs independently, even a frozen gradient (Scroll Speed at center) will show gentle undulation if **Wobble** is raised. The two animations are layered on top of each other.
:::


---

## Exercises

These exercises progress from a simple static gradient to an animated liquid copper wash, exploring blend modes, wobble, and horizontal spread along the way.
### Exercise 1: Classic Copper Bars

![Classic Copper Bars result](/img/instruments/videomancer/copperwash/copperwash_ex1_s1.png)
*Classic Copper Bars — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A flowing vertical rainbow: the classic Amiga copper bar effect, scrolling smoothly down the screen.

#### Key Concepts

- Per-scanline gradient synthesis
- Scroll speed as a bipolar control
- Smooth vs. stepped quantization

#### Steps

1. Set **Gradient Freq** (Knob 2) to about 50%. You should see several rainbow bands stacked vertically.
2. Turn **Scroll Speed** (Knob 1) slightly clockwise from center. The bands begin to scroll downward. Increase the offset for faster scrolling.
3. Flip **Smooth** (Switch 10) to **Steps**. The silky gradient snaps into hard-edged color bands, each a solid block of color (this is closer to the original Amiga aesthetic.)
4. Flip Smooth back to **Smooth** and adjust **Hue Offset** (Knob 3). The entire palette rotates around the color wheel, shifting which hue appears at the top of the screen.
5. Use **Bypass** (Switch 11) to toggle back and forth, comparing the gradient-washed output with the raw input.

#### Settings

| Control | Value |
|---------|-------|
| Scroll Speed | ~55 deg |
| Gradient Freq | 50% |
| Hue Offset | 0 deg |
| Saturation | 75% |
| Wobble | 0% |
| Brightness | 75% |
| Gradient | Rainbow |
| Blend | Multiply |
| H Spread | Off |
| Smooth | Smooth |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Liquid Wobble Wash

![Liquid Wobble Wash result](/img/instruments/videomancer/copperwash/copperwash_ex2_s1.png)
*Liquid Wobble Wash — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An undulating, diagonal wash of color (liquid copper flowing across the screen like a lava lamp.)

#### Key Concepts

- Wobble as sinusoidal phase modulation
- H Spread adds a diagonal component
- Blend mode changes the character of the wash

#### Steps

1. Start with the settings from Exercise 1, but increase **Wobble** (Knob 5) to about 60%. The straight color bars begin to ripple and wave.
2. Flip **H Spread** (Switch 9) to **On**. The gradient tilts diagonally, and the wobble creates swirling interference patterns.
3. Switch **Blend** (Switch 8) to **Add**. The gradient now glows brightly on top of the input video. Notice the gradient also shifts to the **Cool** palette (blue/cyan bias) due to the toggle interaction.
4. Reduce **Saturation** (Knob 4) to about 30%. The vivid colors fade to a gentle pastel wash (subtle but alive.)
5. Slowly sweep **Gradient Freq** (Knob 2) from low to high. Watch the diagonal bands multiply and compress, creating complex moiré-like patterns with the wobble.

#### Settings

| Control | Value |
|---------|-------|
| Scroll Speed | ~30 deg |
| Gradient Freq | 40% |
| Hue Offset | 0 deg |
| Saturation | 30% |
| Wobble | 60% |
| Brightness | 75% |
| Gradient | Rainbow |
| Blend | Add |
| H Spread | On |
| Smooth | Smooth |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Warm Sunset Tint

![Warm Sunset Tint result](/img/instruments/videomancer/copperwash/copperwash_ex3_s1.png)
*Warm Sunset Tint — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A warm, sunset-toned color grade that shifts gently over time (like golden-hour light that never ends.)

#### Key Concepts

- Combined toggle states access the Warm and Cool palettes
- Multiply blend as a cinematic tinting tool
- Mix fader for dialing in subtle grades

#### Steps

1. Set **Gradient** (Switch 7) to **Mono** and **Blend** (Switch 8) to **Multiply**. This activates the **Warm** palette, biasing the gradient toward red and orange tones.
2. Set **Gradient Freq** (Knob 2) low: about 15%. Only one or two broad color bands span the screen, producing a slow vertical gradient from warm tones to neutral.
3. Reduce **Scroll Speed** (Knob 1) to a very gentle offset: just a degree or two from center. The warm wash drifts almost imperceptibly.
4. Set **Hue Offset** (Knob 3) to about 40 deg. This rotates the warm palette toward golden amber.
5. Pull **Mix** (Fader 12) down to about 40%. The tint becomes subtle: the source image dominates, but the warm wash shimmers gently underneath.
6. Add a touch of **Wobble** (Knob 5) at about 15% for gentle undulation in the tint.

#### Settings

| Control | Value |
|---------|-------|
| Scroll Speed | ~3 deg |
| Gradient Freq | 15% |
| Hue Offset | 40 deg |
| Saturation | 75% |
| Wobble | 15% |
| Brightness | 80% |
| Gradient | Mono |
| Blend | Multiply |
| H Spread | Off |
| Smooth | Smooth |
| Bypass | Off |
| Mix | 40% |

---
## Glossary

- **Bipolar**: A control centered at zero that ranges equally into positive and negative values; turning clockwise from center produces positive offsets, counterclockwise produces negative.

- **Copper**: The coprocessor in the Commodore Amiga's custom chipset that could reprogram display registers in sync with the raster beam, enabling per-scanline palette changes.

- **Demoscene**: A computer art subculture focused on producing real-time audiovisual presentations (demos) that push hardware to its limits.

- **Gradient**: A smooth transition between colors or brightness levels, typically spanning a spatial region of the image.

- **Hue**: The attribute of a color that places it on the color wheel: red, orange, yellow, green, blue, violet: independent of brightness or saturation.

- **Interpolation**: Computing intermediate values between two known points; used here to crossfade between dry and wet signals.

- **Lookup Table (LUT)**: A precomputed table of values used to replace runtime calculation with a fast table read; Copperwash uses a quarter-wave sine LUT.

- **Phase**: The current position within a repeating cycle, measured in degrees or radians; determines which point in the color wheel is being evaluated.

- **Raster**: The process of drawing an image line by line from top to bottom; the raster beam position determines which scanline is currently being generated.

- **Saturation**: The intensity or purity of a color; zero saturation produces gray, full saturation produces vivid color.

- **Scanline**: A single horizontal row of pixels in a video frame, drawn left to right by the raster beam.

- **YUV**: A color encoding that separates brightness (Y) from color information (U and V), used in analog and digital video systems.

---
