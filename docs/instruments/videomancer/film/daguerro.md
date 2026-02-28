---
draft: true
sidebar_position: 62
slug: /instruments/videomancer/daguerro
title: "Daguerro"
image: /img/instruments/videomancer/daguerro/daguerro_hero.png
description: "Program guide for Daguerro, a Videomancer film program for the LZX video synthesizer."
---

import daguerro_hero from '/img/instruments/videomancer/daguerro/daguerro_hero.png';
import daguerro_before_after from '/img/instruments/videomancer/daguerro/daguerro_before_after.png';
import daguerro_control_panel from '/img/instruments/videomancer/daguerro/daguerro_control_panel.png';
import daguerro_exercise1_result from '/img/instruments/videomancer/daguerro/daguerro_exercise1_result.png';
import daguerro_exercise2_result from '/img/instruments/videomancer/daguerro/daguerro_exercise2_result.png';
import daguerro_exercise3_result from '/img/instruments/videomancer/daguerro/daguerro_exercise3_result.png';

# Daguerro

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={daguerro_hero} alt="Daguerro hero image"/>
*Daguerro transforming video into a silver-mirror daguerreotype with compressed tonal range, cold plate tinting, and iridescent tarnish patina.*
<img src={daguerro_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Daguerro applied.*

---

## Overview

Before film, before paper prints, the first photographs were made on polished silver plates. Louis Daguerre announced his process in 1839 — a copper sheet coated in silver iodide, exposed in a camera, and developed over heated mercury to reveal a unique, unreproducible image. Every daguerreotype is a mirror and a photograph at once: tilt the plate one way and you see the image, tilt it another and you see your own reflection in the silver surface.

Daguerro recreates the optical qualities of this process as a real-time video effect. The pipeline begins with an exposure stage that shifts overall brightness, followed by tonal compression that narrows the dynamic range to match the limited latitude of a sensitized silver plate. A silver-mirror stage adds the characteristic brightness boost of a mercury-developed plate, or the gentler partial solarization of the later Becquerel sunlight process. Color tinting applies the cold silver-blue or warm gold-amber tonality of period plate finishes, while a tarnish overlay introduces the iridescent blue-green patina that develops on aged silver surfaces. Finally, an LFSR-driven plate texture adds the surface grain of polished or rough metal.

At conservative settings Daguerro produces a restrained monochrome-tinted image with compressed highlights and a metallic sheen. At extreme settings the tarnish patina dominates, the plate texture becomes coarse, and the tonal compression crushes the image into narrow bands of silver and shadow — an abstraction of early photographic chemistry rendered in real-time video.

---

## Background

### Daguerre and Niépce

The daguerreotype emerged from a collaboration between Louis-Jacques-Mandé Daguerre and Nicéphore Niépce. Niépce had produced the first permanent photograph — a view from his workshop window — using bitumen of Judea on a pewter plate as early as 1826. After Niépce's death in 1833, Daguerre continued experimenting and discovered that a silver-iodide-coated plate, after brief exposure in a camera, could be developed by mercury vapor to produce a startlingly detailed image. The French government purchased the rights to the process in 1839 and released it to the world as a gift — with the notable exception of England, where Daguerre held a patent.

### The Silver Iodide Plate

A daguerreotype plate starts as a sheet of copper electroplated with pure silver. The silver surface is polished to a mirror finish, then sensitized by exposure to iodine vapor (and later bromine or chlorine) to form a thin layer of light-sensitive silver halide crystals. This sensitized surface has extremely limited dynamic range — perhaps five stops of exposure latitude compared to the fourteen or more stops of a modern digital sensor. Shadows and highlights compete for a narrow tonal band, which is why daguerreotypes have their characteristic compressed, almost bas-relief quality.

### Mercury vs Becquerel Development

The original mercury process creates the image by amalgamating mercury vapor with the exposed silver halide. Mercury droplets condense preferentially on the most exposed areas, forming a white amalgam that appears as highlights when the plate is viewed against a dark background. The mercury process produces bright, punchy highlights with strong contrast — but requires toxic mercury fumes. The Becquerel process, introduced in 1840 by Edmond Becquerel, replaces mercury with extended exposure to diffuse sunlight. This gentler process produces a subtler tonal scale with softer highlights and a partial solarization effect where the very brightest areas curve back toward mid-tones. In the VHDL pipeline, the Mercury path adds a brightness boost proportional to luminance (the brighter the pixel, the more it is boosted), while the Becquerel path attenuates values above a threshold — faithfully reproducing the solarization shoulder of the sunlight process.

### Tarnish and Patina

Silver is reactive. Over the decades, atmospheric sulfur compounds react with the plate surface to form silver sulfide — a dark, iridescent film that collectors call tarnish. On well-preserved plates, the tarnish appears as blue, green, or violet halos around the edges and across shadow areas, leaving highlight zones relatively clear. This tarnish is spatially irregular because it depends on surface chemistry, humidity, and the presence of volatile organic compounds from the plate's housing. Daguerro simulates this with an LFSR-modulated chrominance offset that pushes selected pixel zones toward blue-green, creating the random-seeming iridescent patina of an aged plate.

### Plate Finish and Clarity

The reflective quality of a daguerreotype depends on how thoroughly the silver was polished before sensitization. A well-polished plate produces a smooth, mirror-like image; a hastily prepared plate shows fine scratches and surface irregularities that scatter light and reduce contrast. The Plate toggle switches between a polished surface (minimal LFSR texture) and a rough surface (stronger LFSR texture applied to the luminance channel). The Clarity control enhances mid-tone separation — pushing brighter-than-mid values up and darker-than-mid values down — emulating the optical effect of a well-prepared plate that resolves fine tonal distinctions.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Exposure Adjustment    (brightness offset from Exposure pot)
│   ├─ 2. Tonal Compression      (narrow dynamic range via Compress pot)
│   ├─ 3. Silver Mirror          (Mercury boost or Becquerel solarization)
│   ├─ 4. Y Pass-through         (Y forwarded to stage 5)
│   ├─ 5a. Plate Texture         (LFSR-based surface grain: polished/rough)
│   ├─ 5b. Clarity               (mid-tone contrast enhancement)
│   └─ 5c. Invert                (optional luminance inversion)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1–3. Latch + pipeline     (U/V held through stages 1–3)
│   └─ 4. Tint + Tarnish         (cold/warm monochrome tint + LFSR tarnish)
│
├── Mix Stage ──────────────────────────────────────────────────
│   └─ Interpolator × 3          (wet/dry crossfade per Y, U, V)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delayed pass-through      (9-clock shift register)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The Y and U/V channels follow different paths through the pipeline. Luminance passes through all five stages — exposure, compression, silver mirror, plate texture, and clarity — while chrominance is discarded and replaced in stage 4 with a synthesized tint based on the Tone toggle and Tint pot. The tarnish overlay modulates chrominance on a per-pixel basis using the LFSR output bit, creating spatially random zones of iridescent color shift. Because the LFSR runs continuously at clock rate, the tarnish pattern is fixed for a given seed and does not change frame-to-frame — just like real silver sulfide tarnish, which is a permanent surface feature.

---

## Parameter Reference

<img src={daguerro_control_panel} alt="Videomancer front panel with Daguerro loaded"/>
*Videomancer's front panel with Daguerro active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Silver
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 68% |
| Suffix | % |

Silver controls the intensity of the silver-mirror reflectivity effect in the Mercury development path. At zero the luminance passes through unchanged. As Silver increases, the brightness boost applied to highlight pixels grows — first by one-eighth, then one-quarter, then one-half of the current luminance value. This simulates the way mercury amalgam preferentially condenses on heavily exposed areas, making highlights bloom with a metallic sheen. In Becquerel mode (Toggle 7), Silver has no effect because the sunlight process does not use mercury vapor.

---

#### Knob 2 — Tarnish
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Tarnish controls the intensity of the iridescent patina overlay applied to the chrominance channels. At zero the chrominance carries only the base tint from Toggle 9 and Pot 4. As Tarnish increases, pixel zones flagged by the LFSR receive a progressively stronger push toward blue-green, simulating the silver sulfide film that forms on aged daguerreotype plates. The spatial distribution of tarnish is pseudo-random and repeatable — the same LFSR seed produces the same tarnish pattern every frame.

---

#### Knob 3 — Compress
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |
| Suffix | % |

Compress controls the tonal range compression applied to the luminance channel. At zero the full 10-bit range is preserved. As Compress increases, the floor rises and the ceiling drops, squeezing the image into an ever-narrower band of mid-tones. Above three-quarters, heavy compression applies — the floor is raised by one-quarter of the Compress value and luminance is reduced to one-quarter of its original excursion. This models the limited dynamic range of the silver iodide plate, where only a few stops of exposure latitude separate pure black from saturated white.

---

#### Knob 4 — Tint
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 49% |
| Suffix | % |

Tint controls the intensity of the monochrome color tint applied to the U and V channels. At zero the output is purely achromatic (neutral gray at U=512, V=512). As Tint increases, the chrominance offset grows — cold blue-silver or warm gold-amber depending on Toggle 9. At maximum the tint is vivid, pushing the image strongly into the selected color temperature. Historical daguerreotypes were sometimes gold-toned by immersing the plate in gold chloride solution, producing a warm amber cast that also improved contrast and permanence.

---

#### Knob 5 — Clarity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Clarity enhances the separation between tones above and below the mid-point. Values above center push highlights brighter and shadows darker, increasing the perceived sharpness and tonal resolution of the plate. Values below center reduce this separation, producing a flatter, more muted result. This emulates the optical qualities of a well-polished vs. poorly polished plate — a pristine surface resolves finer tonal steps, while a degraded surface compresses everything toward the middle.

---

#### Knob 6 — Exposure
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Exposure shifts the overall brightness of the input signal before any other processing. At center (512) the image passes unaltered. Below center the image darkens, simulating an underexposed plate with detail receding into shadow. Above center the image brightens, simulating overexposure where highlight detail washes into featureless silver. Because exposure is the first stage, it affects everything downstream — compression floor/ceiling placement, silver boost intensity, and the input to the clarity stage.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Process** | Mercury | Becquer |
| **8 — Plate** | Polishd | Rough |
| **9 — Tone** | Cold | Warm |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the photographic process and plate characteristics. Process (Toggle 7) selects the development method — Mercury produces punchy highlights with brightness boost, while Becquerel produces a softer, partially solarized tonal curve. Plate (Toggle 8) selects the surface finish — Polished adds only subtle LFSR texture, Rough adds stronger surface grain. Tone (Toggle 9) selects the plate color temperature — Cold produces a blue-silver cast typical of unfinished plates, Warm produces the gold-amber cast of gold-toned plates. Invert (Toggle 10) reverses the luminance at the output stage, producing a negative image reminiscent of the ambrotype (which is a daguerreotype on glass, often appearing as a negative without a dark backing). Bypass (Toggle 11) passes the unprocessed signal for direct comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the original (dry) input and the fully processed (wet) daguerreotype signal. At zero the output is entirely dry — the original video passes through. At maximum the output is entirely wet — the full daguerreotype simulation. Intermediate values blend the two, which is useful for producing a partially processed look where the original color and dynamic range show through the silver-mirror overlay. The interpolator operates independently on Y, U, and V channels with 10-bit fractional precision.

---

## Guided Exercises

These exercises explore the daguerreotype simulation from basic silver plate reproduction through tarnish aging and into abstract tonal manipulation.

### Exercise 1: Classic Mercury Daguerreotype

<img src={daguerro_exercise1_result} alt="Classic Mercury Daguerreotype result"/>
*Classic Mercury Daguerreotype — simulated result across source images.*
**Source**: Portrait footage or a detailed still image with a wide tonal range — faces, fabric folds, or architectural detail work well.

**Objective**: Reproduce the look of a well-preserved mercury-process daguerreotype with compressed tonal range and cold silver tinting.

1. **Initial setup**: Set all pots to center, Process to Mercury, Plate to Polished, Tone to Cold, Invert off, Bypass off, Mix to 100%.
2. **Exposure**: Adjust Exposure slightly above center to brighten the image — daguerreotypes are characteristically luminous.
3. **Compression**: Increase Compress to about 60% to narrow the tonal range. Notice how shadows lift and highlights clip earlier.
4. **Silver boost**: Increase Silver to about 70%. Watch the highlights bloom with a metallic sheen.
5. **Tint**: Increase Tint to about 50% to add the cool blue-silver tone of bare silver.
6. **Fine-tune**: Use Clarity to separate mid-tone detail, then back off Mix slightly to let some original color bleed through.

**Key concepts**: Mercury development adds brightness proportional to luminance, tonal compression narrows dynamic range, cold tinting reproduces the silver surface color

---

### Exercise 2: Aged and Tarnished Plate

<img src={daguerro_exercise2_result} alt="Aged and Tarnished Plate result"/>
*Aged and Tarnished Plate — simulated result across source images.*
**Source**: Landscape or still-life footage with mid-tone detail — foliage, textiles, or tabletop subjects that show tarnish patterns clearly.

**Objective**: Create the appearance of a daguerreotype that has aged for over a century, developing iridescent tarnish and surface degradation.

1. **Start from Exercise 1**: Use the classic mercury settings as a baseline.
2. **Add tarnish**: Increase Tarnish to about 40%. Watch iridescent blue-green patches appear in spatially random zones.
3. **Rough surface**: Switch Plate to Rough. The luminance channel acquires visible grain — scratches and surface irregularities.
4. **Warm aging**: Switch Tone to Warm. The plate shifts from cold silver to aged gold-amber, consistent with gold-toned plates in museum collections.
5. **Increase compression**: Push Compress to about 75% for the heavily degraded tonal range of an old plate.
6. **Reduce clarity**: Lower Clarity below center to soften the tonal transitions, simulating surface haze.

**Key concepts**: Tarnish is LFSR-modulated chrominance shift, plate texture is LFSR-modulated luminance noise, gold toning produces warm amber cast

---

### Exercise 3: Becquerel Negative

<img src={daguerro_exercise3_result} alt="Becquerel Negative result"/>
*Becquerel Negative — simulated result across source images.*
**Source**: High-contrast footage — architecture, silhouettes, or video with strong backlighting.

**Objective**: Use the Becquerel solarization curve and luminance inversion to produce an abstract photographic negative with tarnish overlay.

1. **Switch to Becquerel**: Set Process to Becquerel. The highlight boost disappears, replaced by a solarization shoulder.
2. **Moderate compression**: Set Compress to about 50% to preserve some tonal range for the solarization to work with.
3. **Strong tarnish**: Increase Tarnish to about 60% for heavy iridescent patina.
4. **Cold tone**: Set Tone to Cold for the stark blue-silver look of an untreated plate.
5. **Invert**: Enable Invert. The image flips to negative — highlights become shadows, and the blue tarnish becomes orange-amber in the inverted chrominance.
6. **High clarity**: Increase Clarity to enhance the tonal separation in the inverted result.
7. **Texture**: Try Plate on Rough for maximum surface degradation.

**Key concepts**: Becquerel solarization attenuates highlight peaks, inversion reverses luminance and chrominance perception, tarnish chrominance inverts to complementary colors

---


## Tips

- **Exposure is your starting point**: Daguerreotypes have a narrow latitude. Start by setting Exposure to place your subject in the sweet spot of the compression curve before adjusting other controls.
- **Silver only works in Mercury mode**: The Silver knob has no effect when Process is set to Becquerel. Switch to Mercury to use it.
- **Tarnish needs Tint to show**: The tarnish overlay modulates the chrominance tint. If Tint is at zero, tarnish has nothing to modulate and will not be visible.
- **Gold toning for warm aging**: Switch Tone to Warm and increase Tint for the gold-chloride-toned look found in well-preserved museum daguerreotypes.
- **Rough plate for texture**: The Polished setting is very subtle. Switch to Rough for visible surface grain — useful for compositing with other effects.
- **Mix for blending**: Use the Mix fader at 50–70% to let original color bleed through the monochrome daguerreotype — a hybrid look that preserves some source identity.
- **Becquerel for subtle work**: The Becquerel process produces a gentler tonal curve than Mercury. Use it for portraiture or subjects where highlight bloom would be distracting.
- **Invert for ambrotype look**: Combine Invert with low Compress and cold Tone for the appearance of an ambrotype — a glass-plate photograph that appears as a negative without a dark backing.

---

## Glossary

| Term | Definition |
|------|------------|
| **Amalgam** | An alloy of mercury with another metal; in daguerreotype processing, mercury vapor forms an amalgam with exposed silver to create visible highlights. |
| **Becquerel Process** | A daguerreotype development method using extended sunlight exposure instead of mercury vapor, producing a softer tonal curve with partial solarization. |
| **Daguerreotype** | The first commercially practical photographic process (1839), producing a unique image on a polished silver-plated copper sheet. |
| **Dynamic Range** | The ratio between the brightest and darkest values a system can capture; daguerreotype plates have very limited dynamic range. |
| **Gold Toning** | A chemical treatment using gold chloride that shifts a daguerreotype's color temperature from cold silver to warm amber while improving permanence. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used here to create plate texture and tarnish zone patterns. |
| **Mercury Process** | The original daguerreotype development method using heated mercury vapor to form a bright amalgam on exposed silver halide. |
| **Patina** | A surface coating that develops through age and exposure; on daguerreotypes, tarnish patina appears as iridescent blue-green halos. |
| **Silver Halide** | Light-sensitive silver compounds (silver iodide, silver bromide) that form the photosensitive layer on a daguerreotype plate. |
| **Silver Sulfide** | The dark, iridescent compound formed when atmospheric sulfur reacts with silver; the primary component of daguerreotype tarnish. |
| **Solarization** | A tonal reversal in overexposed highlights where the image curve bends back toward mid-tones, characteristic of the Becquerel process. |
| **Tonal Compression** | Narrowing the range of brightness values in an image by raising the floor and lowering the ceiling of the output range. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
