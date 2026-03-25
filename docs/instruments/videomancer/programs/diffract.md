---
draft: true
sidebar_position: 83
slug: /instruments/videomancer/diffract
title: "Diffract"
image: /img/instruments/videomancer/diffract/diffract_hero_s1.png
description: "When white light passes through a diffraction grating — a surface scored with thousands of parallel slits — each wavelength bends at a slightly different angle."
---

![Diffract hero image](/img/instruments/videomancer/diffract/diffract_hero_s1.png)
*Diffract splitting edge transitions into prismatic chromatic fringes that shimmer across the U and V color channels.*

---

## Overview

Diffract simulates the behavior of a ***diffraction grating***: an optical element that splits light into its component colors based on wavelength. When light passes through a real grating, it fans out into a rainbow of colored copies, each offset by a slightly different angle. Diffract applies this principle to video: it reads brightness differences at nearby pixel positions and converts those differences into chromatic offsets in the U and V color channels. The result is vivid spectral fringes that appear along edges, transitions, and contours in the source image.

The effect draws its color energy from the luminance structure of the input. Flat, uniform areas produce no fringe: there's nothing to split. High-contrast edges and sharp transitions produce the strongest chromatic halos. Soft gradients produce gentle, painterly color washes. This makes Diffract inherently content-responsive: the fringes live where the action is.

Two dispersion modes are available. Horizontal mode uses a 32-entry ***shift register*** to create pixel-delay taps, producing left-right chromatic spreading. Vertical mode uses a ***line buffer*** to compare the current scan line with the previous one, producing top-bottom fringe. Three toggles control the color geometry of the fringe, giving eight distinct spectral configurations from a single processing chain.

:::tip
Diffract works best with high-contrast source material. Feed it graphics, text, silhouettes, or anything with strong edges, and watch the prismatic colors bloom.
:::

### What's In a Name?

***Diffraction*** is the bending of waves around obstacles or through narrow openings. When white light hits a diffraction grating: a surface scored with thousands of fine parallel grooves: each wavelength bends by a different amount, fanning the light out into a spectrum. The word comes from the Latin *diffringere*, meaning "to break apart." Diffract breaks the luminance signal apart into chromatic copies, just as a grating breaks white light into its constituent colors.

---

## Quick Start

1. Feed a high-contrast source into Videomancer and load **Diffract**. Turn **Grating** (Knob 1) to about 50%. You should see colored halos appearing along the edges of bright objects: blues and oranges hugging opposite sides of every transition.
2. Sweep **Orders** (Knob 2) from low to high. The fringes grow from barely visible whispers to vivid chromatic bands. This controls how strongly the edge differences translate into color.
3. Flip **Mode** (Switch 7) from **Split** to **Cross**. The fringe orientation shifts from horizontal to vertical: now the colors stack above and below edges instead of left and right.
4. Bring **Angle** (Knob 6) down toward 0%. The processed effect fades and the original image returns. This is your wet/dry blend: use it to dial in the perfect balance between source and spectral color.

---

## Parameters

![Videomancer front panel with Diffract loaded](/img/instruments/videomancer/diffract/diffract_control_panel.png)
*Videomancer's front panel with Diffract active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Grating

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Grating** controls the spacing between delay taps in the horizontal shift register, setting how far apart the chromatic copies are. Internally, the 10-bit pot value is quantized into eight discrete spacing levels, from closely packed taps at 0% to maximally separated taps at 100%. Wider spacing means the fringe samples brightness from pixels that are further apart, producing broader, more dramatic color spreads. Narrower spacing produces tight, fine-featured fringes that hug edges closely.

At 0%, the taps are only 4 pixels apart and the spectral splitting is subtle and compact. At 100%, the taps span the full 31-entry depth of the shift register, and the chromatic copies are pulled wide apart. In vertical mode (**Mode** set to **Cross**), Grating has no direct effect because the line buffer provides a fixed one-line delay.

:::note
Because the spacing is quantized to eight levels, you'll notice the fringe width changing in discrete steps as you sweep the knob. This is by design: it keeps the tap positions aligned to integer pixel offsets for clean, alias-free results.
:::

---

### Knob 2 — Orders

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Orders** controls the intensity of the chromatic fringe: how strongly edge differences are converted into color. The pot value is mapped to four attenuation levels. At 0%, the fringe signal is divided by eight, producing very faint pastel halos. At 25%, it's divided by four. At 50%, divided by two. At 100%, the full, unattenuated fringe is applied.

Think of Orders as the "gain" of the diffraction process. Low values produce delicate, translucent color washes. High values produce bold, saturated spectral bands. Orders combines multiplicatively with **Falloff** (Knob 5), so the total attenuation is the product of both controls.

---

### Knob 3 — Disperse

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Disperse** shifts the position of the entire tap group within the horizontal shift register. The top three bits of the pot value are used, giving eight discrete offset positions. At 0%, the taps start near the beginning of the delay line (the most recent pixels). As Disperse increases, the taps shift deeper into the register, sampling older pixels.

Shifting the tap group changes the character of the fringe. Near the start of the register, the fringe responds to immediate pixel-to-pixel transitions. Deeper in the register, it responds to broader structures: the fringe "looks further back" in time and space. Combined with **Grating** (Knob 1), Disperse lets you position the spectral window precisely within the 32-pixel delay line.

---

### Knob 4 — Spread

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Spread** controls the polarity of the chromatic fringe. Only the top bit of the pot value is used, making this a binary control disguised as a knob. Below 50%, the fringe polarity is normal: one color appears on the leading edge of a transition and the complementary color appears on the trailing edge. Above 50%, the polarity inverts: the colors swap sides.

This is equivalent to flipping a prism upside down: the rainbow reverses. It's a creative tool for matching the color orientation of the fringe to the aesthetic you want.

:::tip
Because only the MSB matters, you can think of **Spread** as a toggle with a dead zone. Any position from 0% to just under 50% produces the same normal polarity. Anything from 50% to 100% produces inverted polarity.
:::

---

### Knob 5 — Falloff

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Falloff** applies additional attenuation to the chromatic fringe, stacking on top of the **Orders** control. The pot value is mapped to four levels of attenuation. At 0%, no additional reduction is applied: the fringe intensity is governed solely by Orders. At 25%, the fringe is halved. At 50%, quartered. At 100%, the fringe is divided by eight.

Falloff and Orders work together to provide a wide range of intensity control. With Orders at full and Falloff at zero, the fringe is at maximum strength. With both at their most attenuating positions, the fringe is divided by 64: effectively invisible. Use Falloff to tame an otherwise aggressive fringe without changing the tap geometry.

---

### Knob 6 — Angle

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Angle** controls the wet/dry crossfade between the original input signal and the processed output. At 0%, fully counterclockwise, the output is entirely dry: the unprocessed source passes through unchanged. At 100%, fully clockwise, the output is entirely wet: only the diffracted result is heard. Intermediate positions blend the two proportionally.

This is Diffract's master mix control. Use it to fold the chromatic fringe gently into the source at low values, or to commit fully to the spectral effect at high values.

---

### Switch 7 — Mode

| Property | Value |
|----------|-------|
| Off | Split |
| On | Cross |
| Default | Split |

**Mode** selects the orientation of the dispersion source. In the **Split** position, Diffract uses the horizontal shift register: three taps at configurable positions sample the luminance of recent pixels, and the differences between those taps generate the chromatic fringe. This produces left-right color spreading along horizontal edges and transitions.

In the **Cross** position, Diffract uses a ***line buffer*** that stores the previous scan line. The difference between the current pixel's luminance and the luminance of the same pixel on the previous line generates the fringe. This produces top-bottom color splitting along vertical edges and transitions.

:::note
In Cross mode, the **Grating** and **Disperse** controls have no effect because the line buffer uses a fixed one-line delay. **Orders** and **Falloff** still control fringe intensity in both modes.
:::

---

### Switch 8 — Spectrum

| Property | Value |
|----------|-------|
| Off | Full |
| On | Custom |
| Default | Full |

**Spectrum** selects between two fringe-channel configurations. In the **Full** position, the U and V color channels receive independent, complementary fringes. The primary difference (near-tap minus far-tap) drives one channel while the secondary difference (mid-tap minus near-tap) drives the other. This produces the classic diffraction look: complementary colors flanking each edge, like magenta and green, or blue and orange.

In the **Custom** position, the same fringe signal is applied to both U and V channels identically. This collapses the complementary-color effect into a monochromatic fringe: both channels shift together, producing a single-hue tint at edges rather than a rainbow split.

---

### Switch 9 — Blend

| Property | Value |
|----------|-------|
| Off | Add |
| On | Screen |
| Default | Add |

**Blend** controls the color-channel assignment of the fringe. In the **Add** position, the primary fringe drives U and the secondary fringe drives V, producing the default color mapping. In the **Screen** position, the assignments are swapped: the primary fringe drives V and the secondary drives U. This rotates the hue of the spectral fringes, shifting blues toward reds and vice versa.

Combined with **Spectrum** (Switch 8), Blend provides four distinct color configurations. With Spectrum set to Full, you get two complementary-color modes (one the hue-rotation of the other). With Spectrum set to Custom, you get two monochromatic modes with different base hues.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** enables or disables animation of the chromatic dispersion effect. With Animate set to **On** (the default), the fringe pattern evolves dynamically in response to moving video. Set to **Off**, the effect applies to each frame independently with no temporal variation.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Diffract processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the diffracted result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** provides an overall wet/dry blend control via the fader. At 0%, the output is entirely dry. At 100%, the output is entirely wet. This works alongside **Angle** (Knob 6) to control the balance between processed and unprocessed signal. With both at maximum, the full diffraction effect is applied.

---

## Background

### Diffraction gratings

A ***diffraction grating*** is an optical component made of a flat surface etched with hundreds or thousands of evenly spaced grooves. When light strikes the grating, each groove acts as a tiny source of waves. These waves interfere with one another: where wave peaks align, they reinforce (***constructive interference***); where peaks meet troughs, they cancel (***destructive interference***). Because different wavelengths of light bend at different angles, white light fans out into a spectrum: just like a prism, but using wave interference rather than refraction.

The number and spacing of the grooves determines how far the colors spread. Finer gratings produce wider spectral fans. This is analogous to Diffract's **Grating** control: wider tap spacing in the shift register means the program samples brightness differences across a larger pixel span, producing broader chromatic fringes.

### Chromatic aberration

In real cameras and lenses, ***chromatic aberration*** is usually considered a flaw: an unwanted colored fringe that appears because the lens bends different wavelengths by slightly different amounts. The edges of objects pick up colored halos, typically magenta on one side and green on the other. Diffract deliberately recreates this artifact as a creative tool. By computing luminance differences at nearby pixel positions and injecting them into the U and V color channels, it synthesizes the characteristic complementary-color halos of chromatic aberration on demand.

### Shift registers and line buffers

Diffract uses two different delay structures to generate its dispersion. The ***shift register*** is a chain of 32 flip-flops that passes each pixel's luminance value from one stage to the next on every clock cycle. Reading from different positions in the chain gives access to the luminance of pixels that arrived 1, 2, 4, 8, or more clocks ago: which, at video rate, corresponds to pixels at different horizontal positions. Three taps (near, mid, and far) sample this chain, and the differences between their values create the fringe signal.

The ***line buffer*** uses a block of RAM to store an entire scan line. As each pixel of the current line is processed, the corresponding pixel from the previous line is read from RAM. The difference between current and previous-line luminance drives the vertical fringe. Together, these two structures give Diffract both horizontal and vertical dispersion capability.


---

## Signal Flow

### Signal Flow Notes

The critical insight is that Diffract derives all its color from the ***luminance*** channel. The input U and V values pass through to the output with fringe offsets added: but the fringe itself is computed entirely from Y-channel differences. A monochrome input with no chroma information will still produce vivid colored fringes, because the edge structure in the Y channel is what generates the U/V offsets.

The intensity pipeline has two independent attenuation stages: **Orders** and **Falloff**, each providing a right-shift of 0 to 3 bits. These are applied sequentially, so the total attenuation ranges from ÷1 (both at zero shift) to ÷64 (both at maximum shift). This wide dynamic range allows the fringe to be dialed from invisible to overwhelming.

:::tip
**Order of operations matters.** Polarity inversion (**Spread**) is applied after intensity scaling but before the color swap (**Blend**) and double-mode (**Spectrum**) stages. This means inverting polarity affects the raw fringe, while the UV routing decisions are applied to the already-scaled, already-inverted signal.
:::


---

## Exercises

These exercises explore Diffract's spectral fringe capabilities, from subtle chromatic halos to full prismatic textures. Each exercise builds on the previous, engaging more of the processing chain.
### Exercise 1: Prismatic Edge Halos

![Prismatic Edge Halos result](/img/instruments/videomancer/diffract/diffract_ex1_s1.png)
*Prismatic Edge Halos — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Subtle, camera-lens-like chromatic aberration halos hugging the edges of objects in your source video.

#### Key Concepts

- Luminance differences at edges generate chromatic fringe
- Grating controls the horizontal span of the spectral splitting
- Orders and Falloff jointly control fringe intensity

#### Video Source

High-contrast footage with clear edges: text overlays, silhouettes, or architectural footage with strong lines.

#### Steps

1. Load **Diffract** and set **Grating** (Knob 1) to about 30%. A moderate tap spacing produces compact, realistic-looking fringes.
2. Set **Orders** (Knob 2) to about 75% and **Falloff** (Knob 5) to about 25%. This gives a strong but not overwhelming fringe intensity.
3. Set **Angle** (Knob 6) to 100% for the full wet signal.
4. Confirm **Mode** (Switch 7) is set to **Split** for horizontal dispersion. You should see complementary-colored halos along vertical edges (a warm color on one side, a cool color on the other.)
5. Now slowly reduce **Angle** (Knob 6) toward 50%. The prismatic halos blend with the clean source, creating a naturalistic chromatic aberration look (as though your camera lens has a beautiful flaw.)

#### Settings

| Control | Value |
|---------|-------|
| Grating | 30% |
| Orders | 75% |
| Disperse | 50% |
| Spread | 0% |
| Falloff | 25% |
| Angle | 50% |
| Mode | Split |
| Spectrum | Full |
| Blend | Add |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Vertical Rainbow Contours

![Vertical Rainbow Contours result](/img/instruments/videomancer/diffract/diffract_ex2_s1.png)
*Vertical Rainbow Contours — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Vivid vertical chromatic contours that trace horizontal edges and gradients in the source, producing a neon-outlined look.

#### Key Concepts

- Cross mode uses the line buffer for vertical fringe
- Spectrum and Blend toggles reshape the color palette
- Polarity inversion via Spread reverses the rainbow

#### Video Source

Footage with strong horizontal features: landscapes with horizons, stacked objects, or text with horizontal strokes.

#### Steps

1. Flip **Mode** (Switch 7) to **Cross** for vertical dispersion. The fringe now runs top-to-bottom, coloring horizontal edges.
2. Set **Orders** (Knob 2) to 100% for full intensity and **Falloff** (Knob 5) to 0% for no additional attenuation. The fringes should be bold and vivid.
3. Set **Angle** (Knob 6) to 100% for fully wet output.
4. Toggle **Spectrum** (Switch 8) to **Custom**. The complementary-color split collapses into a monochromatic hue (edges are now tinted a single color instead of rainbowed.)
5. Toggle **Blend** (Switch 9) to **Screen** to rotate the hue of the monochromatic fringe.
6. Flip **Spread** (Knob 4) above 50% to invert the fringe polarity. The color shifts to the opposite side of each edge.

#### Settings

| Control | Value |
|---------|-------|
| Grating | 50% |
| Orders | 100% |
| Disperse | 50% |
| Spread | 75% |
| Falloff | 0% |
| Angle | 100% |
| Mode | Cross |
| Spectrum | Custom |
| Blend | Screen |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Full-Spectrum Texture Wash

![Full-Spectrum Texture Wash result](/img/instruments/videomancer/diffract/diffract_ex3_s1.png)
*Full-Spectrum Texture Wash — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An abstract, heavily processed spectral texture where the source is barely recognizable: a wash of prismatic color driven by the original image's edge structure.

#### Key Concepts

- Maximum tap spacing and intensity create extreme spectral effects
- Toggle combinations produce eight distinct color configurations
- Disperse shifts the chromatic window through the delay line

#### Video Source

Any high-contrast footage. Geometric patterns, digital graphics, or video feedback loops work especially well.

#### Steps

1. Set **Grating** (Knob 1) to 100% for maximum tap spacing. The chromatic copies are pulled as far apart as the shift register allows.
2. Set **Orders** (Knob 2) to 100% and **Falloff** (Knob 5) to 0% for full, unattenuated fringe intensity.
3. Set **Disperse** (Knob 3) to about 75%. The tap group shifts deep into the shift register, sampling older pixel data for broader spatial fringe structures.
4. Set **Spread** (Knob 4) below 50% for normal polarity.
5. Set **Angle** (Knob 6) to 100%.
6. Confirm **Mode** (Switch 7) is **Split**, **Spectrum** (Switch 8) is **Full**, and **Blend** (Switch 9) is **Add**.
7. Now begin cycling through the eight toggle combinations. Flip each switch in turn: Mode, Spectrum, Blend. Each combination reshapes the color geometry of the fringe. Find the one that best complements your source.
8. While holding your favorite toggle combination, slowly sweep **Disperse** (Knob 3) from 0% to 100%. The fringe window slides through the delay line, shifting the spatial character of the color wash.

#### Settings

| Control | Value |
|---------|-------|
| Grating | 100% |
| Orders | 100% |
| Disperse | 75% |
| Spread | 0% |
| Falloff | 0% |
| Angle | 100% |
| Mode | Split |
| Spectrum | Full |
| Blend | Add |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Chromatic Aberration**: A lens artifact where different wavelengths of light focus at slightly different points, producing colored fringes at edges.

- **Clamp**: Constraining a computed value to a legal range (0 to 1023 for 10-bit video) to prevent overflow or underflow artifacts.

- **Diffraction**: The bending and spreading of waves as they pass through an opening or around an obstacle, causing interference patterns.

- **Diffraction Grating**: An optical element with many fine parallel grooves that splits white light into a spectrum via constructive and destructive interference.

- **Fringe**: A band of color appearing at the boundary between light and dark areas, caused by chromatic dispersion or interference.

- **Interpolator**: A hardware unit that computes a weighted blend between two values; used here for wet/dry crossfade.

- **Line Buffer**: A block RAM that stores one full scan line of video data, allowing comparison between consecutive lines.

- **Polarity**: The sign (positive or negative) of the fringe offset; inverting polarity swaps which color appears on which side of an edge.

- **Shift Register**: A chain of storage elements where data moves one position forward on each clock cycle, providing multi-tap pixel delay.

- **Tap**: A read point in a delay line; multiple taps at different positions provide access to pixel values at different spatial offsets.

---
