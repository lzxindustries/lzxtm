---
draft: true
sidebar_position: 79
slug: /instruments/videomancer/degauss
title: "Degauss"
image: /img/instruments/videomancer/degauss/degauss_hero_s1.png
description: "Every cathode-ray tube shipped from the factory with its electron beams converged — red, green, and blue landing precisely on their respective phosphor dots."
---

![Degauss hero image](/img/instruments/videomancer/degauss/degauss_hero_s1.png)
*Degauss applying animated color fringing and rainbow warp to a live camera feed, simulating the chromatic distortion of a degaussing CRT monitor.*

---

## Overview

Degauss recreates the mesmerizing color distortion that occurs when a CRT monitor is degaussed: the process of demagnetizing the shadow mask by passing a strong alternating magnetic field across the tube face. On a real CRT, this causes the red, green, and blue electron beams to momentarily misalign, producing vivid rainbow fringes that ripple across the screen. Degauss simulates this by applying opposite chroma offsets to the U and V channels that vary sinusoidally with vertical position and, optionally, animate over time.

At low settings, Degauss adds gentle color fringing along horizontal gradients: a subtle rainbow shimmer. At extreme settings, the entire image warps into bands of vivid false color that ripple vertically across the frame. The animation can be frozen for a static rainbow warp, or set in continuous motion to recreate the signature CRT degaussing spectacle.

### What's In a Name?

To ***degauss*** is to remove unwanted magnetism from a device, named after the ***gauss***, the CGS unit of magnetic flux density and its originator, mathematician Carl Friedrich Gauss. Color CRT monitors contained an internal degaussing coil that fired automatically at power-on, producing a brief flash of rainbow distortion as the shadow mask demagnetized. Pressing the degauss button on a studio monitor was a small ritual: a moment of chromatic chaos before the picture snapped back to normal.

---

## Quick Start

1. Turn **Intensity** (Knob 1) to about 60%. Rainbow color fringes appear across the image, varying from top to bottom.
2. Enable **Animate** (Switch 7) if it isn't already on. The color bands begin to ripple vertically, recreating the CRT degauss waveform in motion.
3. Adjust **Frequency** (Knob 2) to change how many color bands appear vertically. Lower values produce broad, sweeping bands; higher values create denser ripples.
4. Use **Speed** (Knob 3) to control how fast the animation scrolls.

---

## Parameters

![Videomancer front panel with Degauss loaded](/img/instruments/videomancer/degauss/degauss_control_panel.png)
*Videomancer's front panel with Degauss active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Intensity

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Intensity** controls the strength of the chroma offset applied to each pixel. At 0%, no offset is applied and the image passes through with its original color. As the value increases, the U and V channels are pushed further from their original values, creating more vivid and saturated color fringing. At 100%, the offset is at maximum strength, producing bold rainbow bands.

---

### Knob 2 — Frequency

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Frequency** controls the spatial frequency of the sinusoidal warp pattern. At low values, the color bands are broad and span many scanlines, producing gentle, sweeping color shifts across the frame. At high values, the bands become narrow and numerous, creating a dense vertical striping of color. The waveform is a triangle wave derived from the vertical pixel counter, so the pattern repeats at regular intervals down the screen.

---

### Knob 3 — Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Speed** controls the rate of the animation when **Animate** is enabled. At 0%, the pattern is frozen in place: a static rainbow warp. As the value increases, the color bands scroll vertically at increasing rates. The animation is driven by a frame counter that advances the vertical phase offset each frame.

:::tip
Setting Speed to 0% with Animate enabled still freezes the pattern, but the pattern position depends on which frame the Speed was set to zero. Toggle **Animate** off for a guaranteed static pattern locked to the vertical position.
:::

---

### Knob 4 — Spread

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Spread** controls the spatial spread of the color distortion. At low values the color shifts are tightly concentrated. At higher values the offset pattern is distributed more broadly across the image, creating a wider zone of chromatic aberration.

---

### Knob 5 — Convergence

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Convergence** adjusts the relative alignment of the color channels. At 50%, the U and V channels receive perfectly opposite offsets, producing symmetrical rainbow fringing. Reducing convergence brings the channels closer together, while increasing it pushes them further apart. This mimics the convergence adjustment on a real CRT, where misaligned electron beams produce colored halos around edges.

---

### Knob 6 — Saturation

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Saturation** controls the overall chroma saturation of the output. At 50%, saturation passes through at unity. Reducing the value desaturates the color fringing toward gray. Increasing it intensifies the colors beyond their natural levels, producing hyper-vivid rainbow bands.

---

### Switch 7 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** enables or disables the frame-by-frame animation of the color warp pattern. With the switch **On**, the frame counter advances each vertical sync, causing the rainbow bands to scroll vertically. With the switch **Off**, the frame counter freezes and the pattern remains static.

---

### Switch 8 — Radial

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Radial** changes the geometry of the warp pattern. With the switch **Off**, the color offset varies only with vertical position, producing horizontal bands of color. With the switch **On**, the offset also varies with horizontal position, creating a radial or circular fringing pattern that emanates from the center of the screen (closer to the way a real degaussing coil affects a CRT.)

---

### Switch 9 — Horizontal

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Horizontal** controls whether the color offset is applied along the horizontal axis. With the switch **On**, per-pixel chroma offsets create visible color fringing that varies across each scanline. With the switch **Off**, the offset pattern depends only on the vertical position and remains constant along each line.

---

### Switch 10 — Persistent

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Persistent** changes how the color offset behaves over time. With the switch **Off**, the animation resets cleanly each frame. With the switch **On**, the offset accumulates frame-over-frame, creating a slowly building, more chaotic color distortion that evolves gradually rather than cycling in a clean loop.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Degauss processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (unprocessed) signal and the wet (Degauss-processed) signal. At 0%, only the dry signal passes through. At 100%, only the processed signal is output. Intermediate values blend the original and degaussed versions, useful for adding a subtle color shimmer without full-strength rainbow distortion.

---

## Background

### CRT degaussing

Every color CRT contains a ***shadow mask***: a thin metal screen perforated with hundreds of thousands of tiny holes, precisely aligned so that each of the three electron beams (red, green, blue) strikes only its corresponding phosphor dot. Over time, external magnetic fields from speakers, power supplies, or even the Earth's magnetic field can magnetize the shadow mask, causing the beams to bend slightly and strike the wrong phosphor dots. The result is patches of false color, especially noticeable in white or neutral areas. ***Degaussing*** removes this unwanted magnetism by applying a strong alternating magnetic field that decays to zero, randomizing the magnetic domains back to a neutral state.

### Color fringing

During the degaussing process, the rapidly alternating magnetic field temporarily throws all three electron beams off course simultaneously, producing dramatic rainbow ***fringing*** across the screen. The colors appear in roughly sinusoidal bands because the magnetic field strength varies smoothly with distance from the degaussing coil. As the field decays, the bands narrow and fade until the picture snaps back to normal. This transient moment of chromatic chaos is the visual spectacle that Degauss recreates.

### Chroma offset in YUV

Degauss achieves its color fringing by applying opposite offsets to the U and V chroma channels. In the ***YUV*** color model, U and V represent the color difference signals: U encodes the blue-yellow axis, and V encodes the red-cyan axis. By pushing U in one direction and V in the opposite direction, Degauss rotates the perceived hue of each pixel. The magnitude of the offset varies sinusoidally with vertical position, creating the characteristic banded rainbow pattern.


---

## Signal Flow

### Signal Flow Notes

The key interaction is that U and V receive ***opposite*** offsets from the same modulation source. When U is pushed positive (toward blue), V is pushed negative (toward green/cyan), and vice versa. This opposite-sign modulation produces a hue rotation that sweeps through the color wheel as the offset magnitude varies with vertical position.

The Y channel passes through completely unmodified: Degauss does not alter brightness or contrast. All visible changes are purely chromatic, which is faithful to the real degaussing phenomenon where luminance remains stable while color goes haywire.

:::tip
Because only chroma is modified, Degauss pairs well with programs that process luminance. Chain Degauss before a luma-based effect (like Bitcullis or Contour) to add color dimension to a brightness-driven process.
:::


---

## Exercises

These exercises progress from a static color warp to animated chromatic chaos. Each builds on the previous, engaging more of the modulation pipeline.
### Exercise 1: Static Rainbow

![Static Rainbow result](/img/instruments/videomancer/degauss/degauss_ex1_s1.png)
*Static Rainbow — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A frozen rainbow color warp across the frame, like a CRT with a permanently magnetized shadow mask.

#### Key Concepts

- Chroma offsets create color fringing without altering brightness
- Vertical position drives the sinusoidal color pattern
- Intensity controls the strength of the color shift

#### Video Source

A camera feed with neutral tones: faces, gray objects, or white walls show the color shift most clearly.

#### Steps

1. **Disable animation**: Turn **Animate** (Switch 7) off. The pattern is now static.
2. **Set intensity**: Increase **Intensity** (Knob 1) to about 60%. Rainbow bands appear across the image.
3. **Adjust frequency**: Turn **Frequency** (Knob 2) to about 40%. Broad bands of color sweep from top to bottom.
4. **Observe**: The image retains its original brightness, but the colors ripple in horizontal bands. White areas show the fringing most clearly.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~60% |
| Frequency | ~40% |
| Speed | ~0% |
| Spread | ~50% |
| Convergence | ~50% |
| Saturation | ~50% |
| Animate | Off |
| Radial | Off |
| Horizontal | On |
| Persistent | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 2: CRT Degauss Animation

![CRT Degauss Animation result](/img/instruments/videomancer/degauss/degauss_ex2_s1.png)
*CRT Degauss Animation — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An animated ripple of rainbow bands scrolling down the screen, recreating the CRT degauss experience.

#### Key Concepts

- The frame counter drives vertical scrolling of the color pattern
- Speed controls the animation rate
- The effect simulates real-time CRT degaussing

#### Video Source

Any live camera feed or recorded footage with recognizable content.

#### Steps

1. **Enable animation**: Turn **Animate** (Switch 7) on.
2. **Set speed**: Increase **Speed** (Knob 3) to about 30%. The rainbow bands begin scrolling downward.
3. **Increase intensity**: Set **Intensity** (Knob 1) to about 70% for vivid color.
4. **Tune frequency**: Adjust **Frequency** (Knob 2) to ~50% for a moderate density of color bands.
5. **Observe the ripple**: Watch as rainbow bands cascade down the frame in smooth vertical motion.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~70% |
| Frequency | ~50% |
| Speed | ~30% |
| Spread | ~50% |
| Convergence | ~50% |
| Saturation | ~50% |
| Animate | On |
| Radial | Off |
| Horizontal | On |
| Persistent | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 3: Radial Color Chaos

![Radial Color Chaos result](/img/instruments/videomancer/degauss/degauss_ex3_s1.png)
*Radial Color Chaos — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An evolving, radial color distortion that builds in intensity over time, producing a psychedelic, unstable CRT look.

#### Key Concepts

- Radial mode creates circular fringing patterns
- Persistent mode accumulates offsets over time
- Combining all modulation modes produces the most extreme color distortion

#### Video Source

High-contrast footage with strong edges (text, graphics, or geometric patterns.)

#### Steps

1. **Full settings**: Set **Intensity** to ~80%, **Frequency** to ~60%, **Speed** to ~25%.
2. **Enable radial**: Turn **Radial** (Switch 8) on. The color pattern gains a circular component.
3. **Enable persistence**: Turn **Persistent** (Switch 10) on. The color distortion begins accumulating frame over frame.
4. **Watch the buildup**: Over several seconds, the color warp grows more extreme and chaotic.
5. **Adjust mix**: Use **Mix** (Fader 12) at ~70% to blend some original color through the chaos.
6. **Disable horizontal**: Turn **Horizontal** (Switch 9) off to isolate just the vertical and radial components.

#### Settings

| Control | Value |
|---------|-------|
| Intensity | ~80% |
| Frequency | ~60% |
| Speed | ~25% |
| Spread | ~70% |
| Convergence | ~70% |
| Saturation | ~70% |
| Animate | On |
| Radial | On |
| Horizontal | Off |
| Persistent | On |
| Bypass | Off |
| Mix | ~70% |

---
## Glossary

- **Chroma**: The color difference components (U and V) of a YUV video signal, representing hue and saturation independently of brightness.

- **Convergence**: The alignment of the three electron beams (red, green, blue) in a color CRT so they strike the correct phosphor dots through the shadow mask.

- **CRT**: Cathode Ray Tube; a display technology using electron beams to excite phosphor coatings on a glass screen.

- **Degaussing**: The process of demagnetizing a CRT's shadow mask by applying a decaying alternating magnetic field, temporarily producing rainbow color distortion.

- **Fringing**: Colored halos or bands that appear when the color channels of a display are misaligned, either deliberately or due to magnetic interference.

- **Shadow Mask**: A thin perforated metal sheet inside a color CRT that ensures each electron beam strikes only its corresponding phosphor color.

- **YUV**: A color encoding system that separates brightness (Y) from color information (U = blue-yellow axis, V = red-cyan axis).

---
