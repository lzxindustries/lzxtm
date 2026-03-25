---
draft: true
sidebar_position: 285
slug: /instruments/videomancer/stereogram
title: "Stereogram"
image: /img/instruments/videomancer/stereogram/stereogram_hero_s1.png
description: "Stereogram generates a Single Image Random Dot Stereogram (SIRDS) from the input video's luminance channel."
---

![Stereogram hero image](/img/instruments/videomancer/stereogram/stereogram_hero_s1.png)
*Stereogram transforming source video into a random-dot autostereogram pattern where hidden 3D depth emerges from the luma of the original image.*

---

## Overview

Stereogram is a real-time autostereogram generator: the same class of images made famous by the ***Magic Eye*** book series of the 1990s. It converts ordinary video into a field of random dots that conceals a hidden three-dimensional shape. The depth illusion is encoded entirely in the horizontal repeat period of the dot pattern: brighter regions of the source image produce a shorter repeat stride, making those areas appear to float closer to the viewer when the image is viewed with ***divergent*** or ***parallel*** gaze.

Unlike printed autostereograms, Stereogram operates on live video. The hidden depth map changes continuously with the source signal, creating moving three-dimensional shapes embedded inside the noise. At subtle settings, Stereogram adds a shimmering, speckled texture over the source. At extreme settings, the source image vanishes entirely into a field of animated dots that only reveals its secret to viewers who can relax their focus.

:::note
Viewing a stereogram requires a specific technique. Relax your eyes and look "through" the screen as if focusing on something far behind it. The repeating dot pattern will split into overlapping layers, and the hidden depth shape will emerge. It takes practice!
:::

### What's In a Name?

The name ***Stereogram*** is a direct reference to the ***autostereogram***, an image that encodes binocular depth without requiring special glasses. The prefix ***stereo-*** means "solid" or "three-dimensional" in Greek, and ***-gram*** means "something drawn or written." A stereogram is, literally, a drawing of solidity (a flat image that tricks the brain into perceiving depth.)

---

## Quick Start

1. Turn **Depth Rng** (Knob 2) to about 75%. This controls how strongly the source image's brightness drives the hidden depth. You should see random dots overlaid on the image, with their spacing subtly varying across bright and dark areas.
2. Turn **Dot Dens** (Knob 1) to about 50%. The dot pattern's tile width narrows, creating a tighter repeating pattern. Try relaxing your eyes to see the hidden 3D shape emerge.
3. Increase **Noise** (Knob 5) clockwise. The dots become higher contrast: brighter whites and deeper blacks: making the pattern more visible and easier to fuse stereoscopically.
4. Flip **Depth** (Switch 8) to **Flat**. The dots burst into color, with random hues driven by the noise generator. The depth illusion still works, but now the texture is a colorful mosaic instead of monochrome static.

---

## Parameters

![Videomancer front panel with Stereogram loaded](/img/instruments/videomancer/stereogram/stereogram_control_panel.png)
*Videomancer's front panel with Stereogram active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Dot Dens

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Dot Dens** controls the base repeat stride of the random-dot pattern: the horizontal distance, in pixels, before the pattern tiles and repeats. At 0%, fully counterclockwise, the stride is at its minimum (16 pixels), creating a tightly packed pattern with many narrow repetitions across the screen. As you turn the knob clockwise, the stride widens. At 100%, the stride reaches its maximum (128 pixels), producing broader tiles with fewer repetitions per line.

Narrower strides make the stereoscopic depth easier to fuse because your eyes don't need to diverge as far, but the depth resolution is lower. Wider strides encode finer depth detail but require more eye divergence to perceive.

:::tip
Start with **Dot Dens** around 30–50% for the easiest stereoscopic viewing experience. Very narrow or very wide strides make the 3D illusion harder to see.
:::

---

### Knob 2 — Depth Rng

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Depth Rng** controls how strongly the source image's luminance modulates the repeat stride. At 0%, the depth modulation is at its weakest: the repeat stride is nearly uniform across the image, and the hidden shape is barely perceptible. As **Depth Rng** increases, brighter areas of the source produce progressively shorter repeat strides (in SIRDS mode), exaggerating the apparent distance between foreground and background layers.

At 100%, the modulation is at full strength and the depth effect is dramatic. Very high values can cause the pattern to break apart in high-contrast regions where the stride changes abruptly from one pixel to the next.

---

### Knob 3 — Repeat W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Repeat W** controls the density of visible dots in the pattern: the fraction of the random texture that appears as bright dots versus dark background. At 0%, almost no dots pass the threshold and the output is mostly dark. As **Repeat W** increases, more and more of the random noise crosses the visibility threshold, filling the screen with dots. At 100%, nearly every pixel is a visible dot.

For the clearest stereoscopic illusion, a moderate dot density (around 50%) works best. Too sparse, and the brain lacks enough texture to fuse. Too dense, and the pattern becomes a uniform wash.

---

### Knob 4 — Dot Size

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Dot Size** controls the vertical coarseness of the dot pattern by grouping adjacent scanlines together. At low values, every scanline generates a unique random pattern, producing fine, pixel-scale dots. As **Dot Size** increases, lines are grouped in pairs, then quads, then octets: each group shares the same random seed, producing vertically elongated rectangular dots.

This parameter operates in four discrete steps despite being a continuous knob. Turning it gradually, you'll notice the dots jump from single-pixel height to two, four, and finally eight pixels tall. The coarser settings create a blockier, more textile-like texture.

:::note
Because only the top two bits of the knob's range select the grouping factor, the transition between steps happens at roughly 25%, 50%, and 75% of the knob's travel.
:::

---

### Knob 5 — Noise

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Noise** controls the brightness range of the random dots: the contrast between the lightest and darkest values in the pattern. At 0%, all dots converge toward a flat mid-gray, producing a nearly invisible pattern. As **Noise** increases, the bright dots grow brighter and the dark dots grow darker, expanding symmetrically around the midpoint.

At 100%, the full 10-bit range is used: bright dots hit peak white and dark regions fall to black. Higher contrast makes the stereoscopic pattern easier to perceive but also makes the effect more visually aggressive.

---

### Knob 6 — Contrast

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Contrast** is reserved for future use. In the current version, this knob has no effect on the output signal.

---

### Switch 7 — Pattern

| Property | Value |
|----------|-------|
| Off | Dots |
| On | Lines |
| Default | Dots |

**Pattern** selects between two depth-encoding methods. With the switch set to **Dots**, Stereogram operates in ***SIRDS*** (Single Image Random Dot Stereogram) mode: brighter source regions produce a shorter repeat stride, making those areas appear to float closer to the viewer. This is the classic autostereogram encoding used in Magic Eye images.

With the switch set to **Lines**, the program enters ***wallpaper*** mode: brighter regions produce a longer stride, expanding the tile size rather than compressing it. Wallpaper mode creates a subtler, less distinctly three-dimensional effect: the pattern stretches and compresses like a rubber sheet rather than popping out in discrete depth layers.

---

### Switch 8 — Depth

| Property | Value |
|----------|-------|
| Off | Source |
| On | Flat |
| Default | Source |

**Depth** toggles the color mode of the dot pattern. With the switch set to **Source**, the dots are monochrome: only the Y (luma) channel carries the random pattern, while U and V are held at neutral gray. The result is a black-and-white noise texture, like television static.

With the switch set to **Flat**, the dots become colorful. The LFSR's bit pattern drives the U and V chroma channels in addition to Y, generating randomly colored dots. The stereoscopic depth illusion still works in color mode: the repeat structure is unchanged: but the visual texture becomes a vibrant confetti of random hues.

:::tip
Color dots make the stereogram more visually interesting but can make the 3D illusion slightly harder to perceive, because the eye is more easily distracted by the chromatic variation.
:::

---

### Switch 9 — Color

| Property | Value |
|----------|-------|
| Off | Mono |
| On | Color |
| Default | Mono |

**Color** toggles the animation of the dot pattern. With the switch set to **Mono**, the random seed is fixed: the same dot pattern repeats identically frame after frame, producing a static texture that holds still while the depth map moves with the source video.

With the switch set to **Color**, the LFSR seed is varied every frame by XORing the frame counter into the line seed. The dot pattern shimmers and crawls, creating a boiling, animated noise texture. The depth illusion remains but the surface texture is in constant motion.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** is reserved for future use. In the current version, this toggle has no effect on the output signal.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Stereogram processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the stereogram pattern.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (original) and wet (stereogram) signals. At 0%, the output is the unprocessed source video. At 100% (the default), the output is the full stereogram pattern. Intermediate values blend the two, progressively hiding the source image inside the dot texture.

:::tip
A **Mix** value around 60–80% lets the source image ghost through the dot pattern, giving viewers a visual hint of the hidden depth shape without needing to fuse the stereogram. This is useful for demonstration or performance settings where not everyone in the audience can see autostereograms.
:::

---

## Background

### Autostereograms

An ***autostereogram*** is a single flat image that produces a perception of three-dimensional depth without glasses, mirrors, or any other optical aid. The technique exploits ***binocular disparity***: the slight difference between the views from each eye: by hiding repeating patterns at varying intervals across the image. When the viewer relaxes their eyes so that each eye locks onto a different repetition of the pattern, the brain interprets the offset as depth.

The most common form is the ***single image random dot stereogram*** (SIRDS), popularized by the Magic Eye franchise in the 1990s. In a SIRDS, the entire image is covered in seemingly random noise that tiles horizontally at a varying repeat period. Objects "closer" to the viewer have a shorter repeat period; objects "farther" have a longer one. The brain fuses the overlapping noise columns and perceives a sculpted surface floating in front of or behind the image plane.

### Random dot generation

Stereogram uses a 16-bit ***linear feedback shift register*** (LFSR) to generate its pseudo-random dot pattern. An LFSR is a shift register whose input bit is a linear function (XOR) of selected output bits. It cycles through a long sequence of seemingly random states before repeating. The lfsr16 module produces a 16-bit output on every clock cycle, providing both the dot brightness (upper 8 bits) and the density test value (lower 8 bits) simultaneously.

The key to the stereogram illusion is that the LFSR is ***re-seeded*** at regular horizontal intervals. Each time the repeat counter wraps to zero, the LFSR is loaded with a seed derived from the current scanline number. Because the same seed always produces the same output sequence, the random pattern tiles perfectly. The depth illusion comes from varying the wrap point: brighter pixels shorten the interval between re-seeds, compressing the tile and shifting the binocular correspondence.

### Repeat stride and depth encoding

The repeat stride is the core mechanism of the stereogram illusion. It is computed per pixel as:

- **SIRDS mode**: stride = base_stride − depth_adjustment
- **Wallpaper mode**: stride = base_stride + depth_adjustment

The depth_adjustment is derived from the source luma, scaled by the **Depth Rng** parameter. In SIRDS mode, brighter values shorten the stride, making those regions appear closer. The minimum stride is clamped to 8 pixels to prevent the pattern from collapsing. In wallpaper mode, brightness increases the stride, creating a stretching effect rather than a depth pop.


---

## Signal Flow

### Signal Flow Notes

Two mechanisms work together to create the stereogram illusion:

1. **Horizontal tiling via LFSR re-seeding.** The repeat counter wraps at the current stride value and re-seeds the LFSR with a line-dependent seed on every wrap. Because the same seed always produces the same pseudo-random sequence, the dot pattern tiles seamlessly across the scanline. The tiling is what allows the brain to fuse adjacent repetitions into a depth percept.

2. **Luma-driven stride modulation.** The source image's brightness shifts the wrap point of the repeat counter, varying the tile width pixel by pixel. In SIRDS mode, brighter pixels compress the tile (shorter stride), and darker pixels expand it (longer stride). The result is that each scanline contains the same random data repeated at varying intervals that encode a depth profile derived from the source video's luminance.

:::tip
The vertical pattern scale (**Dot Size**) groups adjacent lines to share the same seed, creating vertically elongated dots. This is important for stereo fusion: very fine single-pixel dots are harder for the brain to match between left and right eye views.
:::


---

## Exercises

These exercises progress from a simple static stereogram to animated color patterns, building familiarity with the depth encoding and visual texture parameters.
### Exercise 1: Your First Magic Eye

![Your First Magic Eye result](/img/instruments/videomancer/stereogram/stereogram_ex1_s1.png)
*Your First Magic Eye — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic black-and-white random-dot stereogram with a visible hidden depth shape, using a high-contrast source as the depth map.

#### Key Concepts

- SIRDS depth encoding hides a 3D shape inside random noise
- The repeat stride is the key to the illusion
- Source luminance drives the depth map

#### Video Source

A still image or slow-moving footage with strong bright-dark contrast: a white shape on a black background works best (geometric shapes, text, or a spotlight on a dark stage).

#### Steps

1. **Set the base pattern**: Turn **Dot Dens** (Knob 1) to about 40%. The repeat stride is now moderate (wide enough to encode depth, narrow enough to fuse easily.)
2. **Maximize depth**: Turn **Depth Rng** (Knob 2) to about 75%. The source brightness now strongly modulates the repeat stride.
3. **Fill in the dots**: Set **Repeat W** (Knob 3) to about 50% for a balanced mix of bright and dark dots.
4. **Enlarge the dots**: Turn **Dot Size** (Knob 4) to about 60% so the dots are two or four pixels tall (easier for your eyes to lock onto.)
5. **Crank the contrast**: Turn **Noise** (Knob 5) to about 80%. The dots should be clearly visible as black-and-white speckle.
6. **Try to see it**: Relax your eyes and look through the screen. The white regions of your source should appear to float forward out of the noise field.

#### Settings

| Control | Value |
|---------|-------|
| Dot Dens | 40% |
| Depth Rng | 75% |
| Repeat W | 50% |
| Dot Size | 60% |
| Noise | 80% |
| Contrast | 50% |
| Pattern | Dots |
| Depth | Source |
| Color | Mono |
| Animate | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Animated Color Stereogram

![Animated Color Stereogram result](/img/instruments/videomancer/stereogram/stereogram_ex2_s1.png)
*Animated Color Stereogram — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A colorful, animated stereogram with the source image faintly visible beneath the dot pattern.

#### Key Concepts

- Color dots add chromatic texture without destroying the depth illusion
- Animation makes the surface shimmer while the depth shape remains stable
- Mix blending reveals the source as a ghost image

#### Video Source

A slowly moving video source: a face, a hand, or drifting abstract shapes. Moderate contrast is sufficient.

#### Steps

1. **Start from Exercise 1 settings** and verify the depth illusion is working.
2. **Enable color**: Flip **Depth** (Switch 8) to **Flat**. The monochrome dots explode into random color. Try to fuse the stereogram again: the 3D shape should still be visible, now rendered in a confetti texture.
3. **Enable animation**: Flip **Color** (Switch 9) to **Color**. The dots begin to shimmer and crawl. The depth shape remains stable because it's encoded in the repeat stride, not the dot values.
4. **Blend in the source**: Lower **Mix** (Fader 12) to about 70%. The original video ghosts through the dot texture, giving viewers a hint of what the hidden shape is.
5. **Adjust density**: Sweep **Repeat W** (Knob 3) slowly. Notice how the visual weight of the dot field changes from sparse snow to dense confetti.

#### Settings

| Control | Value |
|---------|-------|
| Dot Dens | 40% |
| Depth Rng | 75% |
| Repeat W | 50% |
| Dot Size | 60% |
| Noise | 80% |
| Contrast | 50% |
| Pattern | Dots |
| Depth | Flat |
| Color | Color |
| Animate | Off |
| Bypass | Off |
| Mix | 70% |

---

### Exercise 3: Wallpaper Mode Textures

![Wallpaper Mode Textures result](/img/instruments/videomancer/stereogram/stereogram_ex3_s1.png)
*Wallpaper Mode Textures — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An abstract, pulsating wallpaper texture that stretches and compresses with the source brightness—more of a decorative pattern generator than a hidden-depth illusion.

#### Key Concepts

- Wallpaper mode encodes depth as tile expansion rather than compression
- Extreme settings create abstract, non-stereoscopic textures
- Combining narrow stride with high depth yields visual breakup

#### Video Source

High-contrast footage with motion: a dancer, flickering candle, or oscilloscope pattern. The movement will animate the tile stretching in real time.

#### Steps

1. **Switch to wallpaper mode**: Flip **Pattern** (Switch 7) to **Lines**. The depth encoding reverses: bright areas now produce wider tiles instead of narrower ones.
2. **Narrow the base stride**: Turn **Dot Dens** (Knob 1) to about 20%. The tiles become very narrow at baseline.
3. **Full depth**: Turn **Depth Rng** (Knob 2) to 100%. Bright regions stretch the pattern dramatically while dark regions stay tightly packed.
4. **Coarsen vertically**: Turn **Dot Size** (Knob 4) to about 80% for wide, blocky dots that emphasize the stretching effect.
5. **Enable color and animation**: Flip **Depth** (Switch 8) to **Flat** and **Color** (Switch 9) to **Color**. The wallpaper becomes a shimmering, colorful mosaic that breathes with the source video.
6. **Sweep density**: Turn **Repeat W** (Knob 3) from 0% to 100%. Watch the wallpaper transition from sparse highlights to a saturated textile.

#### Settings

| Control | Value |
|---------|-------|
| Dot Dens | 20% |
| Depth Rng | 100% |
| Repeat W | 65% |
| Dot Size | 80% |
| Noise | 70% |
| Contrast | 50% |
| Pattern | Lines |
| Depth | Flat |
| Color | Color |
| Animate | Off |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Autostereogram**: A single flat image that produces the illusion of three-dimensional depth when viewed with a specific eye convergence technique, without requiring glasses or other aids.

- **Binocular Disparity**: The slight difference between the images seen by the left and right eyes, which the brain uses to perceive depth.

- **Divergent Gaze**: A viewing technique where the eyes focus on a point behind the image plane, causing each eye to fixate on a different repetition of the pattern; the primary method for viewing autostereograms.

- **LFSR**: Linear Feedback Shift Register: a shift register that generates a deterministic but seemingly random sequence of bits, used here to create the pseudo-random dot texture.

- **Luma**: The brightness component (Y) of a YUV video signal, used by Stereogram as the depth map that modulates the repeat stride.

- **Repeat Stride**: The horizontal distance, in pixels, between re-seeds of the random number generator; the fundamental parameter that encodes stereoscopic depth.

- **SIRDS**: Single Image Random Dot Stereogram: the classic autostereogram format where depth is encoded as variations in the horizontal repeat period of a random dot pattern.

- **Wallpaper Stereogram**: A variant where the repeating pattern is a recognizable motif rather than random dots; in Stereogram's wallpaper mode, the tile size varies with brightness rather than encoding pop-out depth.

---
