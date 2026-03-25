---
draft: true
sidebar_position: 110
slug: /instruments/videomancer/ferro
title: "Ferro"
image: /img/instruments/videomancer/ferro/ferro_hero_s1.png
description: "The cyanotype is one of the oldest photographic processes — a UV-sensitive emulsion of ferric ammonium citrate and potassium ferricyanide, coated onto paper, exposed through a negative, and developed in running water."
---

![Ferro hero image](/img/instruments/videomancer/ferro/ferro_hero_s1.png)
*Ferro transforming a live video feed into a luminous Prussian blue cyanotype contact print, complete with paper fiber texture and edge diffusion.*

---

## Overview

Ferro is a cyanotype contact print simulator. It converts any video input into a continuous reproduction of the historic photographic process invented by Sir John Herschel in 1842: the same process that gave us the word "blueprint." The program inverts the luminance of the input signal (as a contact print inverts a negative), applies a nonlinear contrast curve modeled on the ***Hurter–Driffield sensitometric response*** of ferric salt emulsion, maps the resulting print density to a Prussian blue color axis, and overlays paper fiber texture and edge diffusion artifacts to complete the illusion.

What makes Ferro special is the fidelity of its emulation. The contrast curve isn't a simple gamma: it uses a piecewise reciprocal approximation that compresses deep shadows (where the Prussian blue pigment saturates) while retaining highlight separation (where thin emulsion shows the paper base through the blue). Four selectable tone presets let you move beyond classic Prussian blue into sepia, violet, and a deeper blue based on Mike Ware's 1994 reformulated cyanotype chemistry. At low intensity, Ferro produces a subtle vintage wash. At full strength, it is a convincing digital darkroom.

:::note
Ferro uses zero block RAMs. The entire tone curve is computed arithmetically using a reciprocal lookup table of only eight entries, making it one of the most resource-efficient programs in the Videomancer library.
:::

### What's In a Name?

The name ***Ferro*** comes from the Latin word *ferrum*, meaning iron. The cyanotype process depends on light-sensitive ***ferric*** (iron-based) salts: ferric ammonium citrate and potassium ferricyanide. When exposed to ultraviolet light, these iron compounds undergo a chemical reduction to form ***ferric ferrocyanide***: the deep blue pigment known as Prussian blue. The entire family of iron-based photographic processes is called ***siderotype***, but cyanotype artists and chemists most often use the prefix "ferro" when referring to the chemistry. It's fitting: this program is built on iron.

---

## Quick Start

1. Send a video signal into Videomancer with **Ferro** loaded. You should immediately see a deep blue-on-white image: the default Prussian blue preset with negative polarity, simulating a contact print from a photographic negative.
2. Turn **Contrast** (Knob 1) slowly clockwise past the midpoint. The tonal separation increases: shadows deepen to near-indigo, and highlights brighten toward the paper white. Back it off to around 50% for a natural-looking print.
3. Turn **Paper Grain** (Knob 2) up to about 40%. A subtle fibrous texture appears across the image, as if the emulsion were coated onto watercolor paper. The texture is most visible in midtones.
4. Toggle **Tone A** (Switch 7) to **On** while leaving **Tone B** (Switch 8) at **Off**. The color axis shifts from classic Prussian blue to a richer, deeper blue: the Ware formula cyanotype. Now set both **Tone A** and **Tone B** to **On** to hear the color turn to a warm wine-violet. Explore all four combinations.

---

## Parameters

![Videomancer front panel with Ferro loaded](/img/instruments/videomancer/ferro/ferro_control_panel.png)
*Videomancer's front panel with Ferro active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Contrast

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Contrast** controls the steepness of the sensitometric response curve: the relationship between input luminance and print density. At 0%, fully counterclockwise, the curve is nearly flat and the image appears low-contrast and foggy, as if the emulsion were underexposed. At 50%, the curve produces a natural tonal range with smooth highlight-to-shadow transitions. As the value increases beyond 50%, the curve steepens, compressing midtones and pushing the image toward stark white paper and saturated blue. At 100%, the curve is at maximum steepness, producing hard-edged, high-contrast prints reminiscent of overexposed contact prints where only the densest negative areas register.

:::tip
The contrast curve is ***not*** a simple brightness-contrast adjustment. It models the nonlinear response of light-sensitive ferric salts, so the compression happens asymmetrically: shadows saturate faster than highlights brighten. Listen to the midtones: they tell you where the curve is working.
:::

---

### Knob 2 — Paper Grain

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Paper Grain** controls the amplitude of the simulated paper fiber texture. At 0%, the paper surface is perfectly smooth: a glass plate print. As the value increases, a fine noise pattern modulates the luminance, simulating the visible fibers of watercolor or rag paper as they show through the semi-transparent emulsion. The texture is generated by a ***linear feedback shift register*** (LFSR), producing a pseudo-random pattern that repeats on a very long cycle. At 100%, the paper grain is very pronounced, as if the emulsion were coated onto rough handmade paper.

The texture is added to the luminance channel only, after colorization. This matches the physical reality: in a real cyanotype, the paper texture affects how much pigment sits on any given fiber, modulating brightness but not the hue of the blue.

---

### Knob 3 — Diffusion

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Diffusion** controls the edge diffusion amount, simulating imperfect contact between the photographic negative and the sensitized paper during UV exposure. At 0%, edges are perfectly sharp: the negative was pressed flat under heavy glass. As the value increases, density transitions soften, simulating the optical spread caused by a gap between the negative and the paper surface. At high values, the entire image takes on a dreamy, soft-focus quality, as if printed from a negative that was loosely laid on the paper.

The diffusion is implemented as a single-pole ***IIR*** (infinite impulse response) lowpass filter applied horizontally to the luminance channel. The top four bits of the Diffusion parameter set the filter coefficient, producing 16 discrete levels of blur from crisp to heavily smoothed.

:::note
Diffusion is applied only to the luminance channel. The chrominance values (U and V) pass through the colorization stage without horizontal blur, which is physically accurate: in a real cyanotype, the blue hue doesn't spread laterally; only the density does.
:::

---

### Knob 4 — Vignette

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Vignette** is reserved for a future update. The control is read by the program but does not currently affect the output. Adjusting this knob has no visible effect.

---

### Knob 5 — Bleach

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Bleach** controls the overall density fade, simulating the natural bleaching that occurs when a finished cyanotype is exposed to bright light. At 0%, fully counterclockwise, no bleaching is applied and the print retains its full density range. As the value increases, the entire image fades toward the paper base color, as if left in direct sunlight. At 100%, the blue is almost entirely bleached away, leaving a faint ghost image on the paper.

Bleach operates by scaling the computed density value toward zero before colorization. This means it uniformly reduces the strength of both the luminance depression and the chrominance shift: the image fades evenly toward paper white, not toward some other color.

:::tip
***Bleaching is reversible in a real cyanotype.*** Place a bleached print in a dark drawer for a few hours and the blue regenerates. In Ferro, you can simulate this by sweeping Bleach back to zero and watching the full density return.
:::

---

### Knob 6 — Exposure

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Exposure** controls the pre-inversion brightness offset, simulating the overall UV exposure time of the contact print. At 50% (the default midpoint), no offset is applied. Turning below 50% darkens the exposure: less UV light reached the paper, producing a lighter, more delicate print with reduced density. Turning above 50% brightens the exposure: more UV light reached the paper, producing a denser, more saturated print where even subtle negative areas register as blue.

Exposure is applied after the polarity inversion but before the contrast curve. This means it shifts the entire tonal range up or down the curve, changing which portion of the sensitometric response is engaged. A small Exposure adjustment can dramatically change the character of the print.

---

### Switch 7 — Tone A

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Tone A** is the first bit of the two-bit tone preset selector. Combined with **Tone B** (Switch 8), it selects one of four cyanotype toning presets. See the Toggle Group Notes section below for the full preset table.

---

### Switch 8 — Tone B

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Tone B** is the second bit of the two-bit tone preset selector. Combined with **Tone A** (Switch 7), it selects one of four cyanotype toning presets. See the Toggle Group Notes section below for the full preset table.

---

### Switch 9 — Polarity

| Property | Value |
|----------|-------|
| Off | Negative |
| On | Positive |
| Default | Negative |

**Polarity** selects whether the luminance channel is inverted before processing. In the **Negative** position (default), luminance is inverted: bright areas in the input become the darkest blue on the print, and dark areas become paper white. This is how a real cyanotype contact print works: you place a photographic negative on the sensitized paper, and the transparent areas of the negative allow UV light through to form blue pigment. In the **Positive** position, luminance is not inverted: bright areas remain bright (paper white) and dark areas become blue. This simulates printing from a positive transparency, or making a direct-positive cyanotype.

---

### Switch 10 — Paper Color

| Property | Value |
|----------|-------|
| Off | Warm |
| On | Cool |
| Default | Warm |

**Paper Color** selects between two paper base tones. In the **Warm** position (default), the paper has a slight cream tint (Y=960, U=506, V=516), simulating aged or off-white watercolor paper. In the **Cool** position, the paper is a cleaner, more neutral white (Y=970, U=510, V=510), simulating modern bright-white paper stock.

The paper color is most visible in highlight areas where density is low and the paper base shows through the emulsion. It also subtly affects the perceived warmth of the overall print.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Ferro processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the original video and the cyanotype effect.

---

:::note Toggle Group Notes

**Tone A** and **Tone B** together form a two-bit binary selector that chooses from four cyanotype toning presets. Each preset defines the color axis from the paper base to maximum print density:

| Tone B | Tone A | Preset | Description |
|--------|--------|--------|-------------|
| Off | Off | Classic Prussian Blue | The standard cyanotype blue. Deep navy-indigo at maximum density, paper white at minimum. |
| Off | On | Deep Blue (Ware) | A richer, more saturated blue based on Mike Ware's 1994 reformulated cyanotype chemistry using ammonium iron(III) oxalate. Slightly higher density range. |
| On | Off | Tea-Toned Sepia | Warm sepia-brown tones, simulating the effect of soaking a finished cyanotype in tannic acid (black tea or coffee). The blue is chemically converted to a warm brown-black. |
| On | On | Wine-Toned Violet | Purple-violet tones, simulating toning with anthocyanin-rich wine or grape juice. The result is a moody, reddish-purple print. |

:::tip
In a real darkroom, toning a cyanotype is irreversible: you can't un-tone a tea-stained print. In Ferro, you can switch between presets instantly. Try toggling between Classic Prussian Blue and Tea-Toned Sepia while watching how the color axis rotates through color space.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** controls the wet/dry crossfade between the original input signal and the processed cyanotype output. At 0%, only the original (dry) signal passes through. At 100% (the default), only the processed (wet) cyanotype signal is output. Intermediate values blend between the two, allowing you to dial in a partial cyanotype wash that retains some of the original color and luminance of the input.

The mix is applied independently to each channel (Y, U, and V) using three parallel interpolators. This means color blending is smooth and continuous across the entire range.

---

## Background

### The Cyanotype Process

The cyanotype is one of the oldest photographic printing processes, invented by Sir John Herschel in 1842. It uses two iron-based chemicals: ***ferric ammonium citrate*** and ***potassium ferricyanide***: coated onto paper and dried in the dark. When the coated paper is exposed to ultraviolet light through a photographic negative, the iron salts undergo a chemical reduction to form ***ferric ferrocyanide***, the insoluble pigment known as ***Prussian blue***. The unexposed areas are washed away in water, leaving a white-on-blue negative image.

The process was adopted commercially by Marion and Company of Paris in 1872 for reproducing architectural and engineering drawings: the original "blueprints." It remained the standard reprographic technology through the 1940s. As a fine-art medium, the cyanotype was pioneered by Anna Atkins (who used it to catalog botanical specimens in 1843) and later embraced by pictorialist photographers including Edward Steichen and Clarence White.

### Sensitometric Response

Real photographic emulsions don't respond linearly to light. The relationship between exposure and density follows a characteristic ***S-curve*** described by Hurter and Driffield in 1890. The toe of the curve (low exposure) rises slowly: the emulsion needs a threshold of UV energy before pigment begins to form. The straight-line section (mid-exposure) is roughly linear. The shoulder (high exposure) saturates: beyond a certain point, adding more light produces no additional density.

Ferro models this response with a piecewise reciprocal approximation. The contrast parameter shifts the curve's steepness, changing where the toe and shoulder fall relative to the input signal. This is more physically accurate than a simple gamma curve or a linear contrast control, and it explains why Ferro's contrast feels different from the contrast control on other programs.

### Toning Chemistry

A finished cyanotype can be ***toned*** by soaking it in various chemical solutions that react with the Prussian blue pigment. Tannic acid (found in black tea and coffee) converts the blue to warm sepia-brown through a chemical substitution reaction. Anthocyanins (found in red wine and grape juice) shift the blue toward violet-purple. Mike Ware's 1994 reformulated "new cyanotype" chemistry uses ammonium iron(III) oxalate instead of ferric ammonium citrate, producing a deeper, richer blue with higher maximum density and better archival stability.

Ferro's four tone presets model these real chemical variations by defining different color axes (different YUV deltas from the paper base to maximum density) for each toning bath.


---

## Signal Flow

### Signal Flow Notes

The processing chain has two key interactions to understand:

1. **Exposure before contrast**: The exposure offset is applied to the (possibly inverted) luminance ***before*** the reciprocal contrast curve. This means exposure doesn't simply brighten or darken the result: it shifts the signal's position on the S-curve, changing which part of the sensitometric response is engaged. A small exposure change can have a large effect when the signal sits near the toe or shoulder of the curve.

2. **Bleach after contrast, before color**: Bleach is applied to the density value after the contrast curve computes it but before the density is mapped to the Prussian blue color axis. This ensures the fade is physically consistent: bleaching reduces Prussian blue pigment uniformly, not selectively by tone.

:::tip
**Diffusion is Y-only.** The IIR lowpass filter that simulates contact edge diffusion operates exclusively on the luminance channel. The U and V chrominance channels receive their colorized values directly from the density-to-color mapping without any horizontal blur. This is physically accurate: in a real cyanotype, the pigment density blurs at imperfect contact boundaries, but the hue of Prussian blue doesn't change just because the edge is soft.
:::


---

## Exercises

These exercises progress from a simple contact print to advanced toning and texture techniques, building familiarity with every control on the panel.
### Exercise 1: Classic Blueprint

![Classic Blueprint result](/img/instruments/videomancer/ferro/ferro_ex1_s1.png)
*Classic Blueprint — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A convincing Prussian blue cyanotype print: the classic blueprint look: with subtle paper texture.

#### Key Concepts

- Negative polarity inverts luminance to simulate contact printing
- The contrast curve models the nonlinear response of ferric salt emulsion
- Paper grain adds physical texture to the digital print

#### Video Source

A live camera feed or recorded footage with clear subject-background separation and a range of tonal values.

#### Steps

1. **Default print**: With Ferro loaded at default settings, observe the deep blue-on-white image. The input luminance is inverted (negative polarity), so bright areas in the source become the darkest blue.
2. **Adjust exposure**: Turn **Exposure** (Knob 6) slowly clockwise. The overall print darkens: more of the paper is exposed to UV. Back it off until highlight details just begin to emerge from the paper white.
3. **Set contrast**: Increase **Contrast** (Knob 1) until the tonal range feels natural: shadows are deep indigo, highlights are clean paper, and midtones have smooth gradation.
4. **Add paper grain**: Turn **Paper Grain** (Knob 2) up to about 30%. A fibrous texture appears in the midtones, as if the emulsion is showing the paper surface beneath.
5. **Add edge diffusion**: Turn **Diffusion** (Knob 3) to around 25%. Density transitions soften slightly, as if the negative wasn't pressed perfectly flat against the paper.

#### Settings

| Control | Value |
|---------|-------|
| Contrast | ~60% |
| Paper Grain | ~30% |
| Diffusion | ~25% |
| Vignette | 0% |
| Bleach | 0% |
| Exposure | ~55% |
| Tone A | Off |
| Tone B | Off |
| Polarity | Negative |
| Paper Color | Warm |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Tea-Toned Sepia Print

![Tea-Toned Sepia Print result](/img/instruments/videomancer/ferro/ferro_ex2_s1.png)
*Tea-Toned Sepia Print — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A warm sepia-toned cyanotype print that looks as if it was soaked in a bath of strong black tea, with gentle bleaching to simulate age.

#### Key Concepts

- Tone presets change the color axis from paper base to maximum density
- Bleach fades density toward the paper base regardless of the tone preset
- Paper Color subtly affects the highlight warmth

#### Video Source

Portrait footage or still-life scenes with rich midtone detail.

#### Steps

1. **Start from classic**: Begin with the settings from Exercise 1.
2. **Enable tea toning**: Set **Tone B** (Switch 8) to **On** and leave **Tone A** (Switch 7) at **Off**. The Prussian blue transforms to warm sepia-brown.
3. **Warm the paper**: Ensure **Paper Color** (Switch 10) is set to **Warm**. The paper has a cream tint that complements the sepia tone.
4. **Add light bleaching**: Turn **Bleach** (Knob 5) to about 30%. The overall density fades, as if the print has been sitting near a sunny window for a few weeks. The deepest shadows lighten to a warm brown, and the highlights become almost pure paper.
5. **Increase paper grain**: Raise **Paper Grain** (Knob 2) to about 50%. The rougher texture emphasizes the handmade quality.
6. **Compare**: Toggle **Bypass** (Switch 11) to compare the sepia print with the original video. Toggle it back off and adjust **Mix** (Fader 12) to about 70% to blend some of the original color back through the sepia wash.

#### Settings

| Control | Value |
|---------|-------|
| Contrast | ~40% |
| Paper Grain | ~50% |
| Diffusion | ~20% |
| Vignette | 0% |
| Bleach | ~30% |
| Exposure | ~50% |
| Tone A | Off |
| Tone B | On |
| Polarity | Negative |
| Paper Color | Warm |
| Bypass | Off |
| Mix | ~70% |

---

### Exercise 3: Extreme Texture Positive

![Extreme Texture Positive result](/img/instruments/videomancer/ferro/ferro_ex3_s1.png)
*Extreme Texture Positive — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An abstract, heavily textured image using positive polarity and wine-toned violet, maximizing the physical artifacts for an expressive, painterly result.

#### Key Concepts

- Positive polarity bypasses the luminance inversion for a direct-print look
- High paper grain and diffusion combine for heavily textured results
- Cool paper with wine-violet toning creates an unusual color palette

#### Video Source

High-contrast footage with strong geometric shapes (architecture, silhouettes, or abstract patterns.)

#### Steps

1. **Switch to positive**: Set **Polarity** (Switch 9) to **Positive**. Bright areas remain bright and dark areas become the densest color. The image no longer looks like a contact print negative.
2. **Set wine-violet tone**: Enable both **Tone A** (Switch 7) and **Tone B** (Switch 8) to select the wine-toned violet preset. The color axis shifts to a moody purple.
3. **Cool paper**: Set **Paper Color** (Switch 10) to **Cool**. The neutral white paper creates a starker contrast against the violet tones.
4. **Crank the contrast**: Push **Contrast** (Knob 1) to about 80%. The sensitometric curve steepens, producing hard transitions between paper white and saturated violet.
5. **Heavy texture**: Set **Paper Grain** (Knob 2) to about 75% and **Diffusion** (Knob 3) to about 80%. The image becomes dreamy and rough, as if printed on coarse handmade paper from a negative held several inches away.
6. **Half mix**: Set **Mix** (Fader 12) to about 50%. The heavily textured violet print blends with the original video, creating a ghostly overlay where the source content shows through the paper texture.
7. **Animate exposure**: Slowly sweep **Exposure** (Knob 6) from 0% to 100% while watching how the tonal range slides along the contrast curve.

#### Settings

| Control | Value |
|---------|-------|
| Contrast | ~80% |
| Paper Grain | ~75% |
| Diffusion | ~80% |
| Vignette | 0% |
| Bleach | 0% |
| Exposure | ~50% |
| Tone A | On |
| Tone B | On |
| Polarity | Positive |
| Paper Color | Cool |
| Bypass | Off |
| Mix | ~50% |

---
## Glossary

- **Bleaching**: The fading of Prussian blue pigment when exposed to strong visible light; in a real cyanotype, the effect is partially reversible with dark storage.

- **Contact Print**: A photographic print made by placing a negative directly against sensitized paper and exposing it to light, producing a 1:1 scale print without an enlarger.

- **Cyanotype**: An iron-based photographic printing process that produces images in Prussian blue, invented by Sir John Herschel in 1842.

- **Diffusion**: The optical spreading of light at the boundary between a negative and the sensitized paper surface; imperfect contact causes soft, blurred edges.

- **Hurter–Driffield Curve**: The characteristic S-shaped curve describing the relationship between exposure and density in a photographic emulsion; also called the H&D curve or D-log E curve.

- **IIR Filter**: An infinite impulse response filter, a type of digital filter where the output depends on both current input and previous output values, creating a feedback-based smoothing effect.

- **LFSR**: A linear feedback shift register, a shift register that generates a long cycle of pseudo-random bits by feeding back selected tap XOR combinations.

- **Prussian Blue**: The pigment ferric ferrocyanide (Fe₄[Fe(CN)₆]₃), the insoluble blue compound formed by the cyanotype chemical reaction.

- **Sensitometric Response**: The measured relationship between the amount of light energy applied to a photographic emulsion and the resulting optical density.

- **Toning**: A post-processing step where a finished cyanotype is soaked in a chemical bath (tea, wine, etc.) to alter the color of the Prussian blue pigment through chemical substitution.

---
