---
draft: true
sidebar_position: 74
slug: /instruments/videomancer/daguerro
title: "Daguerro"
image: /img/instruments/videomancer/daguerro/daguerro_hero_s1.png
description: "Before film, before paper prints, the first photographs were made on polished silver plates."
---

![Daguerro hero image](/img/instruments/videomancer/daguerro/daguerro_hero_s1.png)
*Daguerro transforming a portrait into a silvery daguerreotype: compressed tonal range, metallic sheen, and iridescent tarnish patina on a polished plate surface.*

---

## Overview

Daguerro simulates the ***daguerreotype***, the first commercially successful photographic process, invented by Louis Daguerre in 1839. Unlike later photographic processes that produce images on paper or flexible film, daguerreotypes are unique objects: silver-coated copper plates where the image is formed directly in the polished metal surface. The result is a mirror-like image with a compressed tonal range, delicate detail, and a distinctive metallic quality that shifts appearance depending on the viewing angle.

The program reproduces the key visual characteristics of daguerreotypes: a silver-mirror luminance boost that gives highlights their characteristic metallic sheen, tonal compression that limits the dynamic range to the narrow band a polished plate can represent, and an optional tarnish patina: the iridescent blue-green oxidation that appears on aged plates. Two development processes are available: Mercury (the original 1839 method) and Becquerel (a later light-based variant that produces partial solarization in highlights).

### What's In a Name?

The name is a compressed form of ***daguerreotype***, the photographic process named after ***Louis-Jacques-Mandé Daguerre***, the French artist and inventor who publicly announced it in 1839. The word has been shortened to fit the Videomancer display with a phonetic spelling that nods to both the inventor and the Italian word ***guerro*** (warrior) (fitting for the enduring first process of photography.)

---

## Quick Start

1. Feed any video source into Videomancer with Daguerro loaded. The image takes on a compressed, metallic appearance with muted color.
2. Increase **Silver** (Knob 1) to about 70%. Highlights gain a bright, mirror-like metallic quality.
3. Turn **Compress** (Knob 3) to about 60%. The tonal range narrows: the darkest blacks lift and the brightest whites are brought down, creating the limited dynamic range characteristic of a silver plate.
4. Adjust **Tarnish** (Knob 2) to about 40%. An iridescent blue-green patina appears in random patches across the image, simulating the oxidation of aged silver.

---

## Parameters

![Videomancer front panel with Daguerro loaded](/img/instruments/videomancer/daguerro/daguerro_control_panel.png)
*Videomancer's front panel with Daguerro active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Silver

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 68% |

**Silver** controls the metallic reflectivity of the simulated silver plate. At low values, the plate is dull with minimal brightness boost. As Silver increases, highlights gain progressively more luminance, creating the bright, mirror-like sheen of a freshly polished silver plate. In Mercury mode, the boost is proportional to input brightness (bright areas get brighter). In Becquerel mode, the silver also introduces partial solarization: very bright areas are pulled back, mimicking the light-based development process.

---

### Knob 2 — Tarnish

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |

**Tarnish** adds an LFSR-driven oxidation patina to the chroma channels. At 0%, the plate is clean. As Tarnish increases, random pixel positions receive a blue-green tint (U pushed positive, V pushed negative), simulating the ***iridescent tarnish*** that forms on silver daguerreotype plates exposed to air and humidity over decades. The tarnish is spatially random: some pixels get the patina and others don't, creating an organic, mottled appearance.

:::note
Real daguerreotype tarnish is iridescent, shifting through blue, green, gold, and purple depending on the thickness of the oxide layer. Daguerro simplifies this to a blue-green push on randomly selected pixels, which captures the dominant color cast of tarnish without modeling the full iridescence.
:::

---

### Knob 3 — Compress

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |

**Compress** narrows the tonal range of the image, simulating the limited dynamic range of a polished plate. At 0%, the full brightness range (0–1023) is preserved. As Compress increases, the floor lifts and the ceiling drops: at low-mid values, the range narrows to about 75%; at mid, to 50%; at high values, to about 25% of the original range. This compression is the most distinctive visual characteristic of daguerreotypes: the image exists in a narrow band of tonality between bright silver and dark silver, never reaching true black or brilliant white.

---

### Knob 4 — Tint

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 49% |

**Tint** controls the intensity of the color cast applied to the monochrome plate. At 0%, the image is nearly achromatic. As Tint increases, the Cold or Warm tone becomes more pronounced in the U and V channels. The tint is a fixed shift, not proportional to brightness (it applies uniformly to the entire image.)

---

### Knob 5 — Clarity

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Clarity** provides a mid-tone contrast enhancement. At 50% (center), no adjustment is applied. Below center, mid-tone contrast is reduced, softening detail. Above center, mid-tone contrast is increased: pixels above 512 are pushed brighter and pixels below 512 are pushed darker, enhancing local detail. This simulates the sharpness variation in daguerreotypes caused by plate polishing quality and exposure focus.

---

### Knob 6 — Exposure

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Exposure** applies a brightness offset to the input signal before processing. At 50%, no offset is applied. Below 50%, the image is darkened; above 50%, it's brightened. The offset is additive (not multiplicative), shifting the entire tonal curve up or down. This is applied before tonal compression and silver processing, so it changes which parts of the original brightness range fall within the compressed output window.

:::tip
Adjusting Exposure is the most intuitive way to control which tonal zone is "captured" by the daguerreotype simulation. Think of it as controlling the exposure time in the camera: more exposure (higher values) brings out shadow detail at the cost of highlight clipping.
:::

---

### Switch 7 — Process

| Property | Value |
|----------|-------|
| Off | Mercury |
| On | Becquer |
| Default | Mercury |

**Process** selects between two historical development methods. **Mercury** simulates the original 1839 daguerreotype process, where mercury vapor develops the exposed silver iodide into a visible image. This produces a proportional brightness boost: brighter areas get brighter, creating a natural highlight sheen. **Becqueel** (Becquerel process) simulates the later light-based development method, which adds partial ***solarization*** in very bright areas (above 768): highlights are partially pulled back toward mid-gray, creating the subtle tonal reversal that Becquerel-developed plates sometimes exhibit.

---

### Switch 8 — Plate

| Property | Value |
|----------|-------|
| Off | Polishd |
| On | Rough |
| Default | Polishd |

**Plate** selects between a polished and rough plate surface texture. **Polishd** (Polished) uses a minimal LFSR-based texture with small, subtle noise. **Rough** uses a coarser texture with larger noise values, simulating a plate that was not fully polished before sensitization: common in early daguerreotype practice and in plates that have been handled or damaged.

---

### Switch 9 — Tone

| Property | Value |
|----------|-------|
| Off | Cold |
| On | Warm |
| Default | Cold |

**Tone** selects the overall color temperature of the plate. **Cold** applies a silvery-blue tint (U + shift, V − shift/2), simulating a freshly made daguerreotype under daylight. **Warm** applies a gold-amber tint (U − shift, V + shift), simulating gold-toned plates (a common preservation technique from the 1840s onward) or plates viewed under warm artificial light.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** flips the processed luminance. With Invert **On**, the daguerreotype becomes a negative: light areas go dark and dark areas go light. This exploits a unique property of real daguerreotypes: they are simultaneously a positive and a negative, depending on the viewing angle and backing. Tilting a daguerreotype against a dark background reveals the positive image; against a light background, the negative appears.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Daguerro processing stages. Use for instant A/B comparison.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (unprocessed) signal and the wet (Daguerro-processed) signal. At partial values, the compressed, tinted daguerreotype aesthetic blends with the original color and tonal range, which can produce a stylized vintage color effect.

---

## Background

### The daguerreotype process

The daguerreotype was announced to the world on August 19, 1839, causing an immediate sensation. The process begins with a highly polished copper plate coated with a thin layer of silver. The silver surface is sensitized by exposure to iodine (and later bromine) fumes, forming light-sensitive silver halide crystals. After exposure in a camera, the latent image is developed by suspending the plate over heated mercury, which amalgamates with the exposed silver to form a visible image. The plate is then fixed in sodium thiosulfate (hypo) to remove remaining light-sensitive compounds, and optionally toned with gold chloride for preservation and color shift.

### Mercury vs. Becquerel development

The ***Mercury process*** is the original 1839 method. Mercury vapor condenses on areas of the plate that received the most light during exposure, creating an amalgam that scatters light and appears bright. Unexposed areas remain as dark polished silver that acts as a mirror. The ***Becquerel process***, discovered in 1840, uses red light (rather than mercury vapor) to complete the development. This produces a different tonal character: highlights can exhibit a subtle ***solarization*** effect where over-development by light causes a partial tonal reversal, pulling very bright areas back toward mid-tones.

### Tarnish and aging

Daguerreotype plates are inherently fragile. The silver surface tarnishes when exposed to sulfur compounds in the air, forming silver sulfide films of varying thickness. Thin layers appear iridescent blue; thicker layers progress through gold, purple, and eventually opaque dark brown. This tarnish typically begins at the edges (where seals fail in the plate's protective case) and works inward, creating the characteristic ring-shaped tarnish patterns seen on antique daguerreotypes. Daguerro simulates this patina with spatially random blue-green tinting controlled by the Tarnish parameter.


---

## Signal Flow

### Signal Flow Notes

The pipeline is designed to mirror the historical process: exposure happens first (light hits the plate), then tonal compression limits the plate's dynamic range, then the silver development process reveals the image, and finally the plate ages with tint and tarnish. The clarity stage is last because it represents the viewer's experience of examining the plate: sharper examination reveals more or less detail depending on the plate's polish.

The tarnish patina uses a single bit from the LFSR to determine whether each pixel receives the blue-green push or not. This creates a 50/50 random spatial distribution, which at the 10-bit output resolution produces a mottled, organic appearance that's visually convincing as surface oxidation. The tarnish intensity is uniform across the plate: real daguerreotypes have edge-heavy tarnish patterns, but modeling spatial tarnish distribution would require frame-level memory that exceeds the available BRAM budget.


---

## Exercises

These exercises progress from a clean daguerreotype simulation to an aged, tarnished artifact.
### Exercise 1: Classic Mercury Daguerreotype

![Classic Mercury Daguerreotype result](/img/instruments/videomancer/daguerro/daguerro_ex1_s1.png)
*Classic Mercury Daguerreotype — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean, silvery daguerreotype with compressed tonality and metallic highlights (as if freshly made in 1845.)

#### Key Concepts

- Tonal compression limits the image to the narrow range of a silver plate
- Mercury development boosts brightness proportionally
- Cold tone creates the silvery-blue appearance of a fresh plate

#### Video Source

A portrait or still life with a range of tones. Daguerreotypes were primarily used for portraiture.

#### Steps

1. Set **Process** (Switch 7) to Mercury and **Tone** (Switch 9) to Cold.
2. Set **Silver** (Knob 1) to ~70% for bright metallic highlights.
3. Set **Compress** (Knob 3) to ~60% for noticeably limited dynamic range.
4. Set **Tarnish** (Knob 2) to 0% for a clean plate.
5. Adjust **Exposure** (Knob 6) until the subject's face is well-rendered within the compressed range.
6. Set **Clarity** (Knob 5) to ~55% for slightly enhanced detail.

#### Settings

| Control | Value |
|---------|-------|
| Silver | ~70% |
| Tarnish | ~0% |
| Compress | ~60% |
| Tint | ~50% |
| Clarity | ~55% |
| Exposure | ~55% |
| Process | Mercury |
| Plate | Polishd |
| Tone | Cold |
| Invert | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 2: Aged and Tarnished

![Aged and Tarnished result](/img/instruments/videomancer/daguerro/daguerro_ex2_s1.png)
*Aged and Tarnished — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An aged daguerreotype with tarnish patina, gold toning, and rough plate texture (a found artifact from a museum collection.)

#### Key Concepts

- Tarnish adds iridescent blue-green patina to the silver surface
- Warm tone simulates gold-toned preservation
- Rough plate adds visible surface texture

#### Video Source

Any subject works, but architectural details or landscapes (uncommon for real daguerreotypes due to long exposures) create an interesting anachronism.

#### Steps

1. Start from the Exercise 1 settings.
2. Switch **Tone** to Warm. The plate shifts from silver to gold.
3. Switch **Plate** (Switch 8) to Rough. Visible surface texture appears.
4. Increase **Tarnish** to ~50%. Blue-green patches appear across the image.
5. Increase **Tint** (Knob 4) to ~65% for a strong gold cast.
6. Reduce **Clarity** to ~40% to soften detail as if the plate's surface is degraded.

#### Settings

| Control | Value |
|---------|-------|
| Silver | ~70% |
| Tarnish | ~50% |
| Compress | ~60% |
| Tint | ~65% |
| Clarity | ~40% |
| Exposure | ~55% |
| Process | Mercury |
| Plate | Rough |
| Tone | Warm |
| Invert | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 3: Becquerel Solarization

![Becquerel Solarization result](/img/instruments/videomancer/daguerro/daguerro_ex3_s1.png)
*Becquerel Solarization — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A Becquerel-developed daguerreotype with partially solarized highlights, demonstrating the tonal reversal that occurs with light-based development.

#### Key Concepts

- Becquerel development introduces partial solarization in highlights
- The combination of solarization and compression creates an otherworldly tonal curve
- Invert reveals the daguerreotype's dual positive/negative nature

#### Video Source

A high-key subject: bright scenes, backlighting, or subjects with extensive highlight areas to show the solarization effect.

#### Steps

1. Set **Process** to Becquerel.
2. Set **Silver** to ~50% and **Compress** to ~50%.
3. Observe the highlights: areas above 768 in the compressed output begin to pull back toward mid-gray rather than continuing to brighten.
4. Set **Tarnish** to ~60% and **Tone** to Cold for a silvery, tarnished look.
5. Enable **Invert** (Switch 10). The daguerreotype flips to its negative presentation (as if tilted against a light background.)
6. Toggle Invert on and off to see the positive/negative duality.

#### Settings

| Control | Value |
|---------|-------|
| Silver | ~50% |
| Tarnish | ~60% |
| Compress | ~50% |
| Tint | ~40% |
| Clarity | ~50% |
| Exposure | ~50% |
| Process | Becquerl |
| Plate | Polishd |
| Tone | Cold |
| Invert | On |
| Bypass | Off |
| Mix | ~100% |

---
## Glossary

- **Becquerel Process**: A daguerreotype development method using red light instead of mercury vapor, discovered by Edmond Becquerel in 1840.

- **Daguerreotype**: The first practical photographic process, producing a unique image on a silver-coated copper plate.

- **Gold Toning**: A preservation technique where the daguerreotype is treated with gold chloride solution, shifting the tone from silver to warm gold and improving longevity.

- **Mercury Development**: The original daguerreotype development method where the exposed plate is suspended over heated mercury, creating a silver-mercury amalgam.

- **Silver Halide**: The light-sensitive crystals (silver iodide, silver bromide) formed on the daguerreotype plate's surface during sensitization.

- **Solarization**: A photographic phenomenon where overexposure causes a partial reversal of tones (very bright areas become darker rather than brighter.)

- **Tarnish**: Silver sulfide film that forms on exposed silver surfaces, creating iridescent blue, gold, and purple colors depending on thickness.

- **Tonal Compression**: The narrowing of an image's brightness range, limiting both the darkest and lightest possible output values.

---
