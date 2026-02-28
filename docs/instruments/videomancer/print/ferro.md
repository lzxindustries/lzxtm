---
draft: true
sidebar_position: 95
slug: /instruments/videomancer/ferro
title: "Ferro"
image: /img/instruments/videomancer/ferro/ferro_hero.png
description: "The cyanotype is one of the oldest photographic processes — a UV-sensitive emulsion of ferric ammonium citrate and potassium ferricyanide, coated onto p..."
---

import ferro_hero from '/img/instruments/videomancer/ferro/ferro_hero.png';
import ferro_before_after from '/img/instruments/videomancer/ferro/ferro_before_after.png';
import ferro_control_panel from '/img/instruments/videomancer/ferro/ferro_control_panel.png';
import ferro_exercise1_result from '/img/instruments/videomancer/ferro/ferro_exercise1_result.png';
import ferro_exercise2_result from '/img/instruments/videomancer/ferro/ferro_exercise2_result.png';
import ferro_exercise3_result from '/img/instruments/videomancer/ferro/ferro_exercise3_result.png';

# Ferro

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={ferro_hero} alt="Ferro hero image"/>
*Ferro rendering a live camera feed as a Prussian blue cyanotype contact print with paper fiber texture and edge diffusion softness.*
<img src={ferro_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Ferro applied.*

---

## Overview

The cyanotype is one of the oldest photographic processes — a UV-sensitive emulsion of ferric ammonium citrate and potassium ferricyanide, coated onto paper, exposed through a negative, and developed in running water. The result is a monochrome image in deep Prussian blue on a warm cream ground. Ferro simulates every stage of this chemistry in real time, processing live video as though it were being contact-printed onto sensitized paper under ultraviolet light.

The program inverts the input luminance (modeling the negative-to-positive contact print), applies an S-shaped contrast curve modeled on the Hurter–Driffield sensitometric response of iron-salt emulsion, maps the resulting density onto one of four toning presets (Classic Prussian Blue, Deep Blue, Tea-Toned Sepia, Wine-Toned Violet), overlays paper fiber texture from a 16-bit LFSR noise generator, and smears detail with an IIR edge diffusion filter simulating imperfect negative-to-paper contact. The name references the Latin *ferrum* (iron), the element at the heart of the cyanotype's chemistry — ferric salts reduced to ferrous Prussian blue.

At default settings, Ferro produces a convincing Prussian blue cyanotype with subtle grain, gentle diffusion, and the characteristic warm cream of cotton rag paper. Pushing the controls reveals more extreme territory — bleached-out washes, dense sepia prints, violet-toned platinum palladium crossovers, and aggressive paper textures that fragment the image into fiber and noise.

---

## Background

### Anna Atkins and the Birth of the Cyanotype

Sir John Herschel invented the cyanotype process in 1842, but it was Anna Atkins who first used it to create an entire illustrated book — *Photographs of British Algae: Cyanotype Impressions* (1843). Atkins placed botanical specimens directly onto sensitized paper and exposed them to sunlight, creating white silhouettes on a deep blue ground. Her work is widely considered the first book illustrated with photographic images. The cyanotype's simplicity — two chemicals, sunlight, and water — made it the first photographic process accessible outside a laboratory.

### Prussian Blue Chemistry

The distinctive color of a cyanotype comes from Prussian blue (iron(III) hexacyanoferrate(II)), one of the first synthetic pigments, accidentally discovered in Berlin around 1706. During UV exposure, ferric ammonium citrate is photo-reduced from Fe³⁺ to Fe²⁺. The ferrous ions react with potassium ferricyanide to precipitate insoluble Prussian blue directly within the paper fibers. Unexposed areas wash away in water, leaving the cream-white paper base. This is why a cyanotype is always a negative process — where light strikes, blue forms; where a negative blocks light, paper remains white. Ferro models this by inverting input luminance before applying the tone curve.

### Hurter–Driffield Sensitometry

Ferdinand Hurter and Vero Charles Driffield published their landmark paper on photographic sensitometry in 1890, establishing the characteristic S-shaped curve that describes how photographic emulsions respond to light. The curve has three regions: a *toe* (shadow compression where exposure barely registers), a *straight-line* section (proportional density increase in the midtones), and a *shoulder* (highlight saturation where increased exposure produces diminishing density gains). Ferro models this response with a piecewise soft-clip function — `512 + (centered × (contrast_k + 512)) / (|centered| + 512)` — that compresses shadows and highlights while separating midtones. The Contrast control adjusts the steepness of this curve, corresponding to the *gamma* (slope of the straight-line section) of the emulsion.

### Contact Printing and Edge Diffusion

In contact printing, the negative is placed directly against the sensitized paper and pressed flat in a printing frame. Any gap between negative and paper causes UV light to scatter laterally, creating soft, diffused edges — an effect distinctive to contact prints versus enlarger-projected prints. The diffusion is most visible around high-contrast edges: fine lines blur, text softens, and hard boundaries acquire a gentle halo. Ferro simulates this with a first-order IIR lowpass filter on the luminance channel, where the filter coefficient is controlled by the Diffusion knob. At zero the image is pixel-sharp; at full the image smears horizontally like a slightly out-of-contact print.

### Paper Fiber Texture in Printmaking

Fine-art photographic prints are made on paper with visible fiber texture — cotton rag, kozo, or gampi. The paper surface is not perfectly flat; its woven or felted structure modulates the density of the printed image at a fine scale. In cyanotype printing, the emulsion soaks into the paper fibers, so the image literally *is* the paper — every fiber shows through. Ferro adds this texture with a 16-bit LFSR pseudo-random noise generator, scaled by the Paper Grain control. At low levels it creates a subtle organic texture; at high levels the paper itself becomes the dominant visual element.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Polarity Inversion     (1023 - Y for negative contact print)
│   ├─ 1. Exposure Offset        (± 512 centered shift)
│   ├─ 2. H-D Contrast Curve     (S-curve: shadow compress, midtone sep)
│   ├─ 3. Density-to-Color Y     (paper_y - range_y × density / 1024)
│   ├─ 3. Bleach                  (density × (1023 - bleach) / 1024)
│   ├─ 4. IIR Edge Diffusion     (lowpass: α × prev + (16 - α) × curr)
│   ├─ 4. Paper Fiber Noise      (LFSR bipolar ±32, scaled by grain)
│   └─ 5. Wet/Dry Mix Y          (interpolator_u, 4 clocks)
│
├── U Channel ──────────────────────────────────────────────────
│   │
│   ├─ 3. Density-to-Color U     (paper_u + delta_u × density / 1024)
│   └─ 5. Wet/Dry Mix U          (interpolator_u, 4 clocks)
│
├── V Channel ──────────────────────────────────────────────────
│   │
│   ├─ 3. Density-to-Color V     (paper_v + delta_v × density / 1024)
│   └─ 5. Wet/Dry Mix V          (interpolator_u, 4 clocks)
│
├── Tone Preset (2-bit selector) ───────────────────────────────
│   ├─ 00: Classic Prussian Blue  (range=880, Δu=+125, Δv=−140)
│   ├─ 01: Deep Blue (Ware)       (range=900, Δu=+150, Δv=−155)
│   ├─ 10: Tea-Toned Sepia        (range=850, Δu=−60,  Δv=+80)
│   └─ 11: Wine-Toned Violet      (range=860, Δu=+90,  Δv=+70)
│
├── Paper Base Color ───────────────────────────────────────────
│   ├─ Warm: Y=960, U=506, V=516 (cream cotton rag)
│   └─ Cool: Y=970, U=510, V=510 (bright white)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field — 8-clock delay)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical interaction in Ferro's pipeline is the relationship between density and color. After inversion and contrast shaping, the single-channel density value fans out into all three YUV channels simultaneously — Y decreases from the paper base toward black, while U and V shift from neutral paper tones toward the selected Prussian blue (or toned) target. This means the Contrast control does not just affect brightness — it reshapes the entire color mapping by changing which density values fall in the toe, midtone, and shoulder regions of the H-D curve. The Bleach control acts as a density multiplier applied *before* the color mapping, so it fades the image toward paper white while preserving the tonal character of whatever density remains.

Edge diffusion and paper texture operate only on the Y channel after colorization. This matches the physics of the real process: the emulsion diffusion and paper fiber modulation are spatial phenomena that affect density uniformly, not chromaticity. The U and V channels pass through the colorization stage but are not filtered or textured, preserving clean Prussian blue hue even at high diffusion or grain settings.

---

## Parameter Reference

<img src={ferro_control_panel} alt="Videomancer front panel with Ferro loaded"/>
*Videomancer's front panel with Ferro active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the steepness of the Hurter–Driffield sensitometric contrast curve. At the midpoint, the curve provides moderate separation between shadow and highlight densities with natural-looking midtone gradation. Turning counter-clockwise flattens the curve toward a linear response — shadows and highlights compress less, producing a lower-contrast print with more visible detail in the extremes. Turning clockwise steepens the S-curve, crushing shadows and blowing highlights while increasing midtone separation. At maximum, the response approaches a hard threshold — pixels snap to either paper-white or full-density blue with little midtone.

---

#### Knob 2 — Paper Grain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Scales the amplitude of the LFSR paper fiber noise applied to the luminance channel after colorization and diffusion. At zero the print surface is perfectly smooth. As you increase this control, fine-grained bipolar noise modulates the density, simulating the visible fiber structure of cotton rag paper. At moderate values the texture is subtle and organic, adding the visual warmth of a real handmade print. At high values the noise becomes the dominant signal, breaking the image into a field of luminance speckle that obscures the underlying content.

---

#### Knob 3 — Diffusion
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the IIR lowpass filter coefficient for horizontal edge diffusion, simulating imperfect contact between negative and paper during UV exposure. At zero the filter coefficient (alpha) is zero — no blending with the previous pixel, yielding a sharp image. As you increase the control, alpha grows from 0 toward 15/16, causing each output pixel to blend more heavily with its horizontal predecessor. The effect is a directional smear that softens edges and bleeds detail in the scan direction, closely mimicking the lateral light scatter seen in real contact prints with poor negative-to-paper registration.

---

#### Knob 4 — Vignette
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Labeled Vignette in the control interface, this parameter is reserved in the current VHDL implementation — the register is mapped but not connected to any processing stage. Adjusting this control has no visible effect on the output. It is included for future firmware revisions that may add a UV exposure falloff simulation.

---

#### Knob 5 — Bleach
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Reduces the overall print density by multiplying the post-curve density value with `(1023 - bleach) / 1024`. At zero the full density is preserved. Increasing Bleach fades the entire tonal range toward the paper base color, simulating the chemical bleaching step used in alternative process printing to lighten an overexposed cyanotype. At maximum the density is multiplied by near-zero, producing an almost blank paper-white image with only the faintest trace of blue (or toning color) in the deepest shadows.

---

#### Knob 6 — Exposure
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Applies a brightness offset to the input luminance before contrast shaping. The offset is centered at the register midpoint (512): at midpoint, no offset is applied. Turning counter-clockwise subtracts from the inverted luminance, making the print darker (as though the UV exposure time were reduced). Turning clockwise adds to the luminance, brightening the print (longer exposure). This control interacts strongly with Contrast — shifting the input into the toe or shoulder of the H-D curve before the S-shape is applied changes which parts of the tonal range get compressed.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Tone A** | Off | On |
| **8 — Tone B** | Off | On |
| **9 — Polarity** | Negative | Positive |
| **10 — Paper Color** | Warm | Cool |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a 2-bit tone preset selector (4 combinations), controlling the Prussian blue or alternative toning color applied during the density-to-YUV colorization stage. Toggle 9 selects negative (contact print) or positive (direct print) polarity. Toggle 10 chooses between warm cream and cool white paper base colors. Toggle 11 is the global bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input and the processed cyanotype output. At 100% (default, register 1023), the output is fully processed — the complete cyanotype simulation is visible. At 0%, the output is the original unprocessed input. Intermediate positions blend the two using three parallel instances of the unsigned interpolator (one per YUV channel), allowing you to dial in a subtle cyanotype tint over a mostly-clean signal or fade between the raw feed and the full print simulation.

---

## Guided Exercises

These exercises progress from a basic Prussian blue cyanotype to toned and textured alternative-process prints. Each builds on the previous, gradually engaging more of the processing chain.

### Exercise 1: Classic Prussian Blue Cyanotype

<img src={ferro_exercise1_result} alt="Classic Prussian Blue Cyanotype result"/>
*Classic Prussian Blue Cyanotype — simulated result across source images.*
**Source**: A well-lit portrait or still life with recognizable subjects and a wide tonal range — skin tones, fabric, and shadow areas work well.

**Objective**: Create a convincing traditional cyanotype contact print with natural tonality and subtle paper texture.

1. **Default tone**: With Tone A and Tone B both off, the Classic Prussian Blue preset is active. Observe the Prussian blue rendering of the source.
2. **Exposure**: Sweep Exposure from minimum to maximum. Watch the print darken (under-exposure) and lighten (over-exposure). Return to the midpoint for balanced density.
3. **Contrast**: Increase Contrast to about 60%. Midtones separate more distinctly while shadows and highlights compress — the signature S-curve of a photographic emulsion.
4. **Paper grain**: Increase Paper Grain to about 30%. Subtle fiber texture appears across the image, most visible in midtone areas.
5. **Diffusion**: Increase Diffusion to about 25%. Edges soften slightly, simulating imperfect negative-to-paper contact.
6. **A/B compare**: Toggle Bypass on and off to compare the cyanotype rendering against the original color feed.

**Key concepts**: Negative inversion is the foundation of contact printing, the H-D curve shapes photographic tonality, paper grain adds organic texture to a digital image

---

### Exercise 2: Tea-Toned Sepia Print

<img src={ferro_exercise2_result} alt="Tea-Toned Sepia Print result"/>
*Tea-Toned Sepia Print — simulated result across source images.*
**Source**: Landscape footage with trees, water, or architecture — subjects that suit warm-toned vintage aesthetics.

**Objective**: Explore toning presets and bleach to create a sepia-toned alternative-process print.

1. **Select sepia tone**: Set Tone B on and Tone A off to activate the Tea-Toned Sepia preset. The blue shifts to a warm brown.
2. **Reduce contrast**: Set Contrast to about 40%. Tea-toned prints historically have a softer, lower-contrast look than Prussian blue cyanotypes.
3. **Bleach**: Increase Bleach to about 30%. The density lightens, simulating a tannin-bleached print. Shadows retain some color while highlights push toward paper white.
4. **Warm paper**: Ensure Paper Color is set to Warm. The warm cream base reinforces the vintage sepia aesthetic.
5. **Add grain**: Set Paper Grain to about 40% to simulate rough handmade paper.
6. **Compare blue vs sepia**: Toggle Tone B off and on to compare Prussian blue against sepia side by side.

**Key concepts**: Toning changes the chemical composition of the image deposit, bleach reduces density before colorization, paper color affects the entire tonal range

---

### Exercise 3: Extreme Texture and Diffusion

<img src={ferro_exercise3_result} alt="Extreme Texture and Diffusion result"/>
*Extreme Texture and Diffusion — simulated result across source images.*
**Source**: High-contrast graphic material — text overlays, geometric patterns, or footage with strong edges.

**Objective**: Push the diffusion and grain controls to their limits to deconstruct the image into abstract texture.

1. **Maximum diffusion**: Set Diffusion to about 80%. The image smears heavily in the horizontal direction — fine detail dissolves into broad tonal washes.
2. **Heavy grain**: Set Paper Grain to about 75%. The noise dominates — the image becomes a dense field of fiber-like texture with only broad tonal shapes recognizable from the source.
3. **Deep blue**: Set both Tone A on and Tone B off for the Deep Blue (Ware) preset. The saturated blue works well with extreme textures.
4. **High contrast**: Set Contrast to about 80%. The S-curve clips most of the smeared tonal range into either paper-white or full-density blue, creating a stark graphic effect.
5. **Positive polarity**: Toggle Polarity to Positive. The tonality inverts — areas that were blue become white, and vice versa.
6. **Partial mix**: Set Mix to about 50% to see the original half-ghosted behind the extreme cyanotype texture.

**Key concepts**: IIR diffusion accumulates across the scanline, high grain makes the LFSR noise the primary visual element, positive polarity reverses the contact print metaphor

---


## Tips

- **Exposure before contrast**: Set Exposure first to place the tonal range in the H-D curve's sweet spot, then shape the curve with Contrast. Adjusting them in the opposite order requires re-tuning Exposure every time Contrast changes.
- **Bleach for vintage fading**: A small amount of Bleach (10–20%) simulates the look of an aged cyanotype that has faded over decades of UV exposure — paler overall with warmer shadows.
- **Sepia + warm paper**: The Tea-Toned Sepia preset paired with Warm paper and gentle Bleach produces a convincingly vintage look that resembles a 19th-century albumen print.
- **Grain reveals paper**: Paper Grain is most visible in midtone regions. In deep shadows and pure highlights the noise is clipped, so it disappears at the extremes of the tonal range.
- **Diffusion is directional**: The IIR filter smears left-to-right only (following the scan direction). Vertical detail is not affected. For a more uniform softness, combine Diffusion with moderate Paper Grain.
- **Positive polarity for solarization**: Switching to Positive polarity while keeping all other settings at cyanotype defaults produces a solarized-negative appearance — an eerie reversal where bright sky becomes deep blue and dark shadows become paper-white.
- **Mix for subtle tinting**: Use Mix at 10–30% to add a faint Prussian blue tonality over an otherwise clean video signal — useful as a color grading tool rather than a full-process simulation.
- **Vignette is reserved**: The Vignette knob is mapped but unimplemented in the current firmware. Adjusting it has no effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | The ITU-R standard defining the color matrix used to convert between RGB and YUV in video systems. |
| **Contact Print** | A photographic print made by placing a negative in direct contact with sensitized paper and exposing to light, producing a 1:1 scale positive image. |
| **Cyanotype** | A photographic printing process using iron salts that produces images in Prussian blue; invented by Sir John Herschel in 1842. |
| **Density** | The opacity of a photographic image; higher density means less light transmission (darker print area). |
| **H-D Curve** | Hurter–Driffield characteristic curve; the S-shaped relationship between log exposure and resulting density in a photographic emulsion. |
| **IIR** | Infinite Impulse Response; a filter topology where each output sample depends on previous output samples, creating a recursive feedback loop. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **Prussian Blue** | Iron(III) hexacyanoferrate(II); the deep blue pigment formed during cyanotype development. |
| **Sensitometry** | The science of measuring photographic materials' response to light exposure; the basis of the H-D curve. |
| **Toning** | A post-processing step that chemically alters the color of a photographic print, converting the image substance to a different compound (e.g., sepia, selenium, gold). |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
