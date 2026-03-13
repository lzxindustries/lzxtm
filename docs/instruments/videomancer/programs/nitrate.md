---
draft: true
sidebar_position: 207
slug: /instruments/videomancer/nitrate
title: "Nitrate"
image: /img/instruments/videomancer/nitrate/nitrate_hero_s1.png
description: "Before Technicolor, cinema was colored by hand."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import nitrate_control_panel from '/img/instruments/videomancer/nitrate/nitrate_control_panel.png';
import nitrate_source1_parrot from '/img/instruments/videomancer/nitrate/nitrate_source1_parrot.png';
import nitrate_source2_field from '/img/instruments/videomancer/nitrate/nitrate_source2_field.png';
import nitrate_source3_turtle from '/img/instruments/videomancer/nitrate/nitrate_source3_turtle.png';
import nitrate_source4_pattern from '/img/instruments/videomancer/nitrate/nitrate_source4_pattern.png';
import nitrate_source5_man from '/img/instruments/videomancer/nitrate/nitrate_source5_man.png';
import nitrate_source6_berries from '/img/instruments/videomancer/nitrate/nitrate_source6_berries.png';
import nitrate_hero_s1 from '/img/instruments/videomancer/nitrate/nitrate_hero_s1.png';
import nitrate_hero_s2 from '/img/instruments/videomancer/nitrate/nitrate_hero_s2.png';
import nitrate_hero_s3 from '/img/instruments/videomancer/nitrate/nitrate_hero_s3.png';
import nitrate_hero_s4 from '/img/instruments/videomancer/nitrate/nitrate_hero_s4.png';
import nitrate_hero_s5 from '/img/instruments/videomancer/nitrate/nitrate_hero_s5.png';
import nitrate_hero_s6 from '/img/instruments/videomancer/nitrate/nitrate_hero_s6.png';
import nitrate_ex1_s1 from '/img/instruments/videomancer/nitrate/nitrate_ex1_s1.png';
import nitrate_ex1_s2 from '/img/instruments/videomancer/nitrate/nitrate_ex1_s2.png';
import nitrate_ex1_s3 from '/img/instruments/videomancer/nitrate/nitrate_ex1_s3.png';
import nitrate_ex1_s4 from '/img/instruments/videomancer/nitrate/nitrate_ex1_s4.png';
import nitrate_ex1_s5 from '/img/instruments/videomancer/nitrate/nitrate_ex1_s5.png';
import nitrate_ex1_s6 from '/img/instruments/videomancer/nitrate/nitrate_ex1_s6.png';
import nitrate_ex2_s1 from '/img/instruments/videomancer/nitrate/nitrate_ex2_s1.png';
import nitrate_ex2_s2 from '/img/instruments/videomancer/nitrate/nitrate_ex2_s2.png';
import nitrate_ex2_s3 from '/img/instruments/videomancer/nitrate/nitrate_ex2_s3.png';
import nitrate_ex2_s4 from '/img/instruments/videomancer/nitrate/nitrate_ex2_s4.png';
import nitrate_ex2_s5 from '/img/instruments/videomancer/nitrate/nitrate_ex2_s5.png';
import nitrate_ex2_s6 from '/img/instruments/videomancer/nitrate/nitrate_ex2_s6.png';
import nitrate_ex3_s1 from '/img/instruments/videomancer/nitrate/nitrate_ex3_s1.png';
import nitrate_ex3_s2 from '/img/instruments/videomancer/nitrate/nitrate_ex3_s2.png';
import nitrate_ex3_s3 from '/img/instruments/videomancer/nitrate/nitrate_ex3_s3.png';
import nitrate_ex3_s4 from '/img/instruments/videomancer/nitrate/nitrate_ex3_s4.png';
import nitrate_ex3_s5 from '/img/instruments/videomancer/nitrate/nitrate_ex3_s5.png';
import nitrate_ex3_s6 from '/img/instruments/videomancer/nitrate/nitrate_ex3_s6.png';

# Nitrate

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: nitrate_source1_parrot, after: nitrate_hero_s1 },
    { label: "Field", before: nitrate_source2_field, after: nitrate_hero_s2 },
    { label: "Turtle", before: nitrate_source3_turtle, after: nitrate_hero_s3 },
    { label: "Pattern", before: nitrate_source4_pattern, after: nitrate_hero_s4 },
    { label: "Man", before: nitrate_source5_man, after: nitrate_hero_s5 },
    { label: "Berries", before: nitrate_source6_berries, after: nitrate_hero_s6 },
  ]}
/>
*Nitrate applying sepia-toned tinting and blue-toned toning to create a hand-painted silent cinema colorization effect.*

---

## Overview

Before Technicolor, cinema was colored by hand. From the 1890s through the late 1920s, film laboratories applied chemical dyes to black-and-white nitrate prints using two principal techniques: *tinting* (soaking the film base in a dye bath so that highlights take on color while shadows remain dark) and *toning* (replacing the silver particles in the emulsion with a metallic salt so that shadows take on color while highlights remain white). A single print could combine both processes — warm sepia tinting in daytime scenes, cold blue toning for night — or use the Pathé stencil process to apply multiple colors to different luminance zones within a single frame.

Nitrate recreates these photochemical coloring processes in real-time video. Two independent hue wheels (Tint Hue and Tone Hue) select colors from an eight-segment piecewise UV mapping. The tint process applies color proportional to luminance (brighter pixels get more color); the tone process applies color proportional to inverse luminance (darker pixels get more color). Four blending modes — combined tint+tone, tone-only, and stencil multi-zone — determine how the two colors interact. A per-frame LFSR flicker gate simulates the brightness variations of nitrate prints projected on carbon arc equipment.

The name refers to cellulose nitrate, the highly flammable film stock used in the silent era. Most surviving tinted and toned prints are nitrate originals, and their characteristic warm amber patina and occasional frame-by-frame brightness flutter are the visual signatures that Nitrate reproduces.



---

## Quick Start

1. **Set Desat In to Mono for authentic results**: Real film tinting and toning worked on black-and-white prints. Desaturating the input first gives the most historically accurate colorization.
2. **Use Tone Amt at 0% for isolated tinting**: Since Mode A "Tint" actually yields the combined blend, zero out the tone intensity to hear only the tint color.
3. **Flicker at low values for subtlety**: Even 10–15% flicker adds barely-perceptible frame-to-frame brightness variation that reads as "aged" without being distracting.

---

## Background

### Film Tinting

Tinting was the simplest and most widespread colorization technique. The developed print was immersed in a dye bath — typically aniline dyes dissolved in water — that stained the gelatin base. Because the dye absorbed into the clear (bright) areas of the film, tinted scenes show color in the highlights while dark areas remain black. Amber and sepia were the most common tint colors, used for interior and daytime scenes. Nitrate's Tint Hue control selects the dye color, and Tint Amt controls the immersion depth (intensity).

### Film Toning

Toning was chemically more complex. The metallic silver in the emulsion was replaced with a colored salt — iron for blue, copper for red, uranium for brown. Because the conversion only affects areas with silver (the exposed, dark parts of the image), toned scenes show color in the shadows while highlights remain white. Blue toning was universally used for night scenes and moonlit exteriors. Nitrate's Tone Hue and Tone Amt controls replicate this luminance-inverse colorization.

### Duotone and Combined Processing

Many prints combined both processes. A typical dramatic sequence might be tinted amber (warm highlights) and toned blue (cool shadows), creating a duotone where the midtones smoothly transition between the two dye colors. Nitrate's combined mode weights the tint result by luminance and the tone result by inverse luminance, then blends them. The crossover point is at mid-gray (Y=512).

### Pathé Stencil Coloring

The Pathé Frères stencil process (1906–1930) was the most labor-intensive colorization technique. Skilled workers cut stencils from spare prints, one for each color zone, and then ran the exhibition print through a series of dye baths using each stencil as a mask. The result was multi-zone coloring within a single frame — different luminance bands received different colors. Nitrate's stencil mode divides the luminance range into four zones using the Stencil Spread control, assigning tone color to deep shadows, blended tone to shadows, blended tint to midtones, and full tint to highlights.

### Carbon Arc Flicker

Early projection equipment used carbon arc lamps that produced slightly different brightness from frame to frame as the carbon electrodes burned down. Combined with the variable density of hand-applied dyes, nitrate prints exhibited a characteristic per-frame brightness flutter. Nitrate simulates this with a per-frame LFSR noise source that modulates luminance. The smooth mode adds a scaled random offset; the harsh mode gates brightness on or off per frame.


---

## Signal Flow

Desaturation → Tint + Tone Colorize → Mode Blend → Flicker Gate

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Desaturation + Hue Mapping ────────────────────────
│   ├─ Desat In toggle: keep UV or force UV = 512 (mono)
│   ├─ Tint Hue pot → 8-segment piecewise → (s_tint_u, s_tint_v)
│   └─ Tone Hue pot → 8-segment piecewise → (s_tone_u, s_tone_v)
│
├── Stage 2: Tint + Tone Colorize ──────────────────────────────
│   ├─ Tint: U = 512 + (tint_uv × Y × tint_intensity) >> 20
│   │        V = 512 + (tint_uv × Y × tint_intensity) >> 20
│   │        Y unchanged
│   ├─ Tone: U = 512 + (tone_uv × (1023-Y) × tone_intensity) >> 20
│   │        V = 512 + (tone_uv × (1023-Y) × tone_intensity) >> 20
│   │        Y = 512 + Y/2  (compressed, lifted)
│   └─ Both clamped [0, 1023]
│
├── Stage 3: Mode Blend ────────────────────────────────────────
│   ├─ Mode B=Stencil: 4 luminance zones →
│   │     deep shadow (tone), shadow (attenuated tone),
│   │     midtone (attenuated tint), highlight (tint)
│   ├─ Mode A=0, Mode B=0: Combined duotone
│   │     weighted blend: tint×Y + tone×(1023-Y)
│   └─ Mode A=1, Mode B=0: Tone only
│       (Note: Tint-only is unreachable — Mode A=0 yields combined)
│
├── Stage 4: Flicker Gate ──────────────────────────────────────
│   ├─ Smooth: Y += LFSR_scaled × flicker_amt (random offset)
│   └─ Harsh:  Y × (1 - flicker_amt) when LFSR(0)=1
│   UV passes through unchanged
│
├── Interpolator (4 clocks) ────────────────────────────────────
│   └─ lerp(dry, wet, mix_amount) per Y, U, V
│
└── Output ─────────────────────────────────────────────────────
    └─ Always interpolator result (bypass signal is dead)
```

The most important architectural detail is the mode selection logic. When Mode B is set to Stencil, Mode A is ignored — the stencil classifier takes priority. When Mode B is set to Combined, Mode A selects between combined duotone (Mode A = Tint) and tone-only (Mode A = Tone). There is no way to isolate tint-only processing through the mode toggles; the "Tint" position of Mode A actually yields the combined tint+tone blend. For tint-only coloring, set Tone Amt to 0%.

The flicker gate operates only on luminance — chrominance UV passes through unchanged from the mode blend stage. This matches the behavior of real nitrate prints, where arc lamp variations affected brightness uniformly without shifting hue.

---

## Parameter Reference

<img src={nitrate_control_panel} alt="Videomancer front panel with Nitrate loaded"/>
*Videomancer's front panel with Nitrate active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Tint Hue
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Selects the tint color (highlight dye) from an eight-segment piecewise hue wheel. The 10-bit pot value is divided into eight sectors: sepia/amber (0), yellow-green (128), green (256), blue (384), cyan (512), magenta (640), red (768), warm/sepia wrap (896). Each sector maps to a fixed (U, V) offset pair that determines the chrominance added to bright pixels. The mapping is discontinuous between sectors — there is no interpolation at segment boundaries.

---

#### Knob 2 — Tone Hue
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 33.3% |
| Suffix | % |

Selects the tone color (shadow replacement dye) from the same eight-segment hue wheel as Tint Hue. In traditional film processing, tone hues were limited by available metallic salts — iron blue, copper red, uranium brown. Nitrate provides the full wheel for both tint and tone, allowing historically impossible combinations like green shadows with magenta highlights.

---

#### Knob 3 — Tint Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the tint intensity — how strongly the tint color appears in highlights. The UV offsets from the hue wheel are multiplied by both the input luminance and this intensity value. At 0%, no tint is applied regardless of the hue setting. At 100%, the full chrominance offset is added to bright pixels. The multiplication is: `UV_out = 512 + (hue_uv × Y × intensity) >> 20`.

---

#### Knob 4 — Tone Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the tone intensity — how strongly the tone color appears in shadows. The operating principle mirrors Tint Amt but uses inverse luminance (1023 − Y) as the scaling factor. At 0%, shadows are neutral. At 100%, dark pixels receive the full tone hue chrominance. Additionally, the tone process compresses and lifts the luminance range: `Y_toned = 512 + Y/2`, simulating the reduced dynamic range of chemically-toned silver prints.

---

#### Knob 5 — Stencil
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the zone boundary width in stencil mode. The pot value is right-shifted by 2 to produce an 8-bit zone width. Four zones are defined at luminance thresholds: zone_width, 2×zone_width, and 3×zone_width. Pixels below the first threshold get full tone color; pixels above the third get full tint color. The two middle zones receive attenuated versions (75% color, 25% neutral). When Mode B is set to Combined, this control has no effect.

---

#### Knob 6 — Flicker
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the per-frame brightness variation amplitude. A 16-bit LFSR advances once per frame (on vsync edge), producing a new random value. In smooth mode, 8 bits of the LFSR are scaled by this pot and added as a signed offset to luminance. In harsh mode, the LFSR's LSB gates a multiplicative dimming: odd frames are darkened by `Y × (1 - flicker_amt/1023)`. At 0%, no flicker occurs.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode A** | Tint | Tone |
| **8 — Mode B** | Combined | Stencil |
| **9 — Desat In** | Color | Mono |
| **10 — Flk Style** | Smooth | Harsh |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form a mode selector with three reachable states: combined duotone, tone-only, and stencil. Toggle 9 controls input desaturation. Toggle 10 selects flicker character. Toggle 11 is mapped but non-functional — the bypass signal is never read in the output assignment, so it has no effect on the output. Wet/dry blending is controlled exclusively by the Mix fader.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input (delayed to match the 8-clock pipeline latency) and the colorized output. At 0% (value 0), the output is the dry, unprocessed signal. At 100% (value 1023), the output is fully colorized. This is the only means of bypassing the effect, since the Bypass toggle is non-functional.





---

## Guided Exercises

These exercises progress from basic single-color tinting through duotone processing to full multi-zone stencil coloring, exploring the interaction between tint, tone, and flicker stages.

### Exercise 1: Sepia Tinting

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: nitrate_source1_parrot, after: nitrate_ex1_s1 },
    { label: "Field", before: nitrate_source2_field, after: nitrate_ex1_s2 },
    { label: "Turtle", before: nitrate_source3_turtle, after: nitrate_ex1_s3 },
    { label: "Pattern", before: nitrate_source4_pattern, after: nitrate_ex1_s4 },
    { label: "Man", before: nitrate_source5_man, after: nitrate_ex1_s5 },
    { label: "Berries", before: nitrate_source6_berries, after: nitrate_ex1_s6 },
  ]}
/>
*Sepia Tinting — simulated result across source images.*
**Source**: A black-and-white or desaturated video source — monochrome camera feed, or any footage with the Desat In toggle set to Mono.

**What You'll Create**: Learn how tinting adds color proportional to luminance, coloring highlights while leaving shadows dark.

1. Set Desat In to Mono to work with a black-and-white base. Set Mode A to Tint, Mode B to Combined.
2. Set Tint Hue to 0% (sepia/amber sector). Set Tint Amt to ~75%.
3. Observe: bright areas take on warm sepia color. Dark areas remain black or near-black.
4. Slowly sweep Tint Hue through the full range. Watch the highlight color cycle through amber, green, blue, cyan, magenta, red, and back to warm.
5. Set Tone Amt to 0% to isolate the tint effect. Note that Mode A in "Tint" position actually gives the combined blend — but with tone at zero, only tint is visible.

**Key concepts**: Tinting colors highlights proportional to luminance, shadows stay dark, hue wheel has 8 discrete sectors, combined mode with zero tone intensity effectively isolates tint

---

### Exercise 2: Duotone Tint and Tone

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: nitrate_source1_parrot, after: nitrate_ex2_s1 },
    { label: "Field", before: nitrate_source2_field, after: nitrate_ex2_s2 },
    { label: "Turtle", before: nitrate_source3_turtle, after: nitrate_ex2_s3 },
    { label: "Pattern", before: nitrate_source4_pattern, after: nitrate_ex2_s4 },
    { label: "Man", before: nitrate_source5_man, after: nitrate_ex2_s5 },
    { label: "Berries", before: nitrate_source6_berries, after: nitrate_ex2_s6 },
  ]}
/>
*Duotone Tint and Tone — simulated result across source images.*
**Source**: Video with a full tonal range — portraits, architectural interiors, or dramatic lighting.

**What You'll Create**: Combine tint (highlight color) and tone (shadow color) to create a duotone colorization.

1. Set Desat In to Mono. Mode A to Tint, Mode B to Combined.
2. Set Tint Hue to ~0% (sepia) and Tone Hue to ~33% (blue sector). Set both Tint Amt and Tone Amt to ~75%.
3. Observe: highlights are warm amber, shadows are blue, midtones transition between the two. This is the classic warm-day/cool-shadow duotone.
4. Swap the hues — blue tint, sepia tone. The emotional quality reverses.
5. Toggle Desat In to Color. The original source chrominance shows through under the tint/tone colorization, creating a partially-colored effect.

**Key concepts**: Duotone blends tint and tone weighted by luminance and inverse luminance, crossover occurs at mid-gray (Y=512), desaturation controls whether original color shows through

---

### Exercise 3: Stencil Coloring with Flicker

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: nitrate_source1_parrot, after: nitrate_ex3_s1 },
    { label: "Field", before: nitrate_source2_field, after: nitrate_ex3_s2 },
    { label: "Turtle", before: nitrate_source3_turtle, after: nitrate_ex3_s3 },
    { label: "Pattern", before: nitrate_source4_pattern, after: nitrate_ex3_s4 },
    { label: "Man", before: nitrate_source5_man, after: nitrate_ex3_s5 },
    { label: "Berries", before: nitrate_source6_berries, after: nitrate_ex3_s6 },
  ]}
/>
*Stencil Coloring with Flicker — simulated result across source images.*
**Source**: High-contrast footage with distinct shadow and highlight regions — stage lighting, candle-lit scenes, or strong backlight.

**What You'll Create**: Use stencil mode to assign different colors to luminance zones, then add per-frame flicker for a vintage projection effect.

1. Set Mode B to Stencil. Set Tint Hue to ~0% (sepia) and Tone Hue to ~50% (cyan). Both amounts to ~75%.
2. Adjust Stencil to ~50%. Observe four distinct color zones: deep shadows (cyan tone), lighter shadows (attenuated cyan), midtones (attenuated sepia), highlights (sepia).
3. Sweep Stencil from low to high. The zone boundaries move — low values compress zones into the shadows, high values spread them across the full range.
4. Now increase Flicker to ~40%. The image begins to flutter in brightness — smooth random offsets per frame.
5. Toggle Flk Style to Harsh. The flicker becomes binary — frames randomly dim sharply, simulating a failing projector.
6. Lower Mix to ~70% to blend the aged colorization with the original signal.

**Key concepts**: Stencil mode divides luminance into four zones with distinct colorization, flicker gate adds per-frame brightness variation, harsh vs. smooth flicker models different projector conditions, mix fader is the only bypass mechanism

---


## Tips

- **Stencil mode for multi-zone coloring**: The stencil classifier divides luminance into four zones. Pair contrasting tint and tone hues for the most dramatic zone separation.
- **Bypass is non-functional**: Use the Mix fader (set to 0%) to bypass the effect. The Bypass toggle does nothing.
- **Hue sectors are hard-edged**: There is no interpolation between the eight hue sectors. If you need a smooth color sweep, animate the pot value and accept the sector snaps.
- **Tone lifts shadows**: The tone process compresses luminance to [512, 1023]. Images with tone-only processing will have elevated black levels. This is by design — it simulates the metallic-salt replacement that lightens shadows.
- **Feedback loops**: Routing the tinted/toned output back to the input creates cumulative dye layering — each pass intensifies the colorization and further separates the tint and tone zones.

---

## Glossary

| Term | Definition |
|------|------------|
| **Carbon Arc** | A type of electric lamp used in early film projection, producing light by passing current through carbon electrodes. Known for frame-to-frame brightness variation. |
| **Duotone** | A colorization technique combining two colors, typically one for highlights and one for shadows. |
| **LFSR** | Linear Feedback Shift Register; a hardware-efficient pseudo-random number generator. Nitrate uses one to produce per-frame flicker noise. |
| **Luminance** | The brightness component (Y) of a YUV video signal. |
| **Nitrate** | Cellulose nitrate; the flammable film stock used in cinema from the 1890s through the 1950s. |
| **Pathé Stencil** | A hand-cut stencil process developed by Pathé Frères for applying multiple colors to different zones within a single film frame. |
| **Tinting** | Coloring the bright areas of a film print by dyeing the film base. Color is proportional to luminance. |
| **Toning** | Coloring the dark areas of a film print by replacing silver with a metallic salt. Color is proportional to inverse luminance. |

---
