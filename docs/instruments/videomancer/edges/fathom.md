---
draft: true
sidebar_position: 92
slug: /instruments/videomancer/fathom
title: "Fathom"
image: /img/instruments/videomancer/fathom/fathom_hero.png
description: "Every topographic map you have ever seen uses the same trick: draw lines where the ground crosses a constant altitude, then fill the zones between those..."
---

import fathom_hero from '/img/instruments/videomancer/fathom/fathom_hero.png';
import fathom_before_after from '/img/instruments/videomancer/fathom/fathom_before_after.png';
import fathom_control_panel from '/img/instruments/videomancer/fathom/fathom_control_panel.png';
import fathom_exercise1_result from '/img/instruments/videomancer/fathom/fathom_exercise1_result.png';
import fathom_exercise2_result from '/img/instruments/videomancer/fathom/fathom_exercise2_result.png';
import fathom_exercise3_result from '/img/instruments/videomancer/fathom/fathom_exercise3_result.png';

# Fathom

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={fathom_hero} alt="Fathom hero image"/>
*Fathom rendering luminance contour lines with hypsometric terrain tinting across a landscape feed, mapping brightness to elevation like a topographic survey.*
<img src={fathom_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Fathom applied.*

---

## Overview

Every topographic map you have ever seen uses the same trick: draw lines where the ground crosses a constant altitude, then fill the zones between those lines with colors that suggest the terrain — green lowlands, brown mountains, white glacial peaks. Fathom applies that cartographic technique to live video. It treats the luminance of each pixel as an elevation value, draws contour isolines wherever brightness crosses a threshold between adjacent pixels, and fills the zones between contours with colors from a selectable palette.

The name evokes depth measurement — to *fathom* is to sound the depth of water, and the program's bathymetric palette directly references nautical charts that color the seabed from shallow white through progressively deeper blues. At moderate settings, Fathom produces imagery that looks strikingly like a relief map rendered in real time from a camera feed. At extreme settings — wide contour intervals, bold line weights, high saturation — it becomes a vivid color-field abstraction where the original video is barely recognizable beneath the cartographic overlay.

A single BRAM line buffer stores the previous scanline's luminance, enabling vertical contour detection. The pipeline tests up to fifteen threshold levels against both horizontal and vertical pixel neighbours in parallel, classifies every fifth contour level as "major" for optional bold styling, and composites the result through a zone saturation and opacity stage before a final wet/dry mix.

---

## Background

### Contour Lines and Isolines

A contour line — or *isoline* — connects all points that share the same value of a measured quantity. On a topographic map, contour lines connect points of equal elevation. On a weather map, isobars connect points of equal atmospheric pressure. The fundamental detection algorithm is the same in all cases: compare adjacent samples, and if the measured value crosses a threshold between them, a contour passes through that point. Fathom implements exactly this comparison in hardware, testing the luminance of each pixel against its left and upper neighbours.

### Hypsometric Tinting

Hypsometric tinting is the cartographic practice of color-coding elevation zones on a map. The word comes from the Greek *hypsos* (height) and *metron* (measure). A standard hypsometric color scheme progresses from dark green at sea level, through yellows and ochres for foothills and plateaus, to brown and gray for high mountains, and finally white for snowcapped peaks. Fathom's terrain palette follows this tradition, mapping the eight luminance zones from low-brightness greens through mid-brightness browns to high-brightness whites.

### Bathymetric Charts

Bathymetry is the underwater equivalent of topography — the measurement of ocean depth. Bathymetric charts use a blue color ramp that intensifies with depth: shallow waters appear light cyan or white, while the deepest trenches are rendered in dark navy or indigo. Fathom's bathymetric palette inverts the brightness-to-depth relationship, assigning deep saturated blues to low-luminance zones and near-white to the brightest zones, producing imagery reminiscent of seafloor surveys.

### Major and Minor Contour Lines

On printed topographic maps, every fifth contour line is drawn heavier and labelled with the elevation value — these are called *index contours* or major contours. The lighter intermediate lines are *supplementary* or minor contours. This visual hierarchy helps the eye parse the terrain at a glance. Fathom replicates this convention: contour levels 5, 10, and 15 are flagged as major, and the Major/Minor toggle enables distinct styling so that the map-like periodicity is visually apparent.

### Terrain Color Palettes in Digital Cartography

Modern GIS software renders elevation data using color ramps defined in lookup tables. The choice of palette is not arbitrary — it follows perceptual research into which color progressions most naturally suggest rising terrain, receding depth, or temperature change. Fathom's two built-in palettes are deliberately designed for immediate readability: the terrain palette uses warm earth tones that viewers instinctively associate with landscape, while the bathymetric palette uses cool blues that suggest water and depth.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Elevation Offset       (add offset, clamp 0–1023)
│   ├─ 2. Line Buffer Write      (store current luma for next line)
│   ├─ 3. Contour Detection      (15 thresholds × H/V crossing)
│   │      ├─ H crossing          (current vs left pixel)
│   │      ├─ Extended H crossing (current vs 2-pixels-left, weight>1)
│   │      └─ V crossing          (current vs above pixel from BRAM)
│   ├─ 4. Zone Index              (top 3 bits of offset luma → 0…7)
│   ├─ 5. Major/Minor Class.     (levels 5, 10, 15 → major)
│   ├─ 6. Color Composite       (contour line color or zone fill)
│   │      ├─ On contour → contour color (8-hue selector)
│   │      └─ Off contour → palette zone or video passthrough
│   ├─ 7. Saturation Scale        (chroma around 512 × zone_sat)
│   ├─ 8. Opacity Blend           (zone color vs original, zone only)
│   └─ 9. Wet/Dry Mix             (3× interpolator_u, 4 clocks)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ Palette lookup / video passthrough (same path as Y)
│   ├─ Saturation scaling (around 512 neutral)
│   └─ Wet/Dry Mix (interpolator_u)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-stage delay pipeline (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original (delayed) or processed signal
```

The critical interaction is between contour detection and zone coloring. Contour detection operates on the *offset* luma — after the elevation offset has been applied — so the Elev Offset knob shifts the entire contour map up or down through the brightness range, like adjusting sea level on a relief map. Zone coloring uses the same offset luma, so the palette assignment stays consistent with the contour boundaries. The opacity blend is applied *only* to non-contour zone fills when in HypsoFill mode, meaning contour lines always render at full opacity regardless of the Zone Opac setting; this ensures that the map grid remains legible even when the fill is dialled back to a subtle tint.

---

## Parameter Reference

<img src={fathom_control_panel} alt="Videomancer front panel with Fathom loaded"/>
*Videomancer's front panel with Fathom active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Contour Int
| Property | Value |
|----------|-------|
| Range | 16 – 256 |
| Default | 106 |

Selects the spacing between contour lines from a lookup table of eight values: 16, 32, 48, 64, 96, 128, 192, and 256 luminance levels. At the narrowest interval (16), the image is densely crosshatched with contour lines — up to fifteen visible levels spanning the 10-bit range. At the widest interval (256), only three or four contours appear, dividing the image into broad elevation bands. The choice of interval determines how much topographic detail is visible: narrow intervals reveal subtle gradients; wide intervals emphasize major tonal transitions.

---

#### Knob 2 — Line Weight
| Property | Value |
|----------|-------|
| Range | 1px – 4px |
| Default | 2px |
| Suffix | px |

Sets the thickness of contour lines from 1 to 4 pixels. At the minimum weight, contours are single-pixel hairlines. The hardware implements thicker lines by extending the horizontal crossing detection to include a second pixel neighbour — effectively widening the zone in which a crossing is detected. Higher weights make the contour grid bolder and more dominant in the image, which works well with wide contour intervals where the sparse lines benefit from extra visual presence.

---

#### Knob 3 — Contour Clr
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 45° |
| Suffix | ° |

Selects the color of contour lines from an eight-hue palette: brown, black, white, blue, red, green, yellow, and purple. The top three bits of the register value select the hue, producing clean eight-step switching. Brown is the cartographic default for land contours, blue is traditional for bathymetric lines, and white or black provide maximum contrast against any palette. The color applies equally to major and minor contours when Major/Minor is set to Equal; when set to Styled, major contours render at full intensity while minor contours use the same hue.

---

#### Knob 4 — Zone Opac
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls how strongly the hypsometric zone color replaces the original video in non-contour areas when Fill Mode is set to HypsoFill. At zero, the zones are invisible and only contour lines are drawn over the original video. At full, the zones completely replace the original luminance with the palette color. Intermediate values produce a translucent overlay where the palette tint is visible but the underlying video texture shows through. This control has no effect when Fill Mode is set to VideoFill, since the original video is passed through between contours without palette coloring.

---

#### Knob 5 — Elev Offset
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Adds a constant offset to the input luminance before contour detection and zone assignment. This shifts the entire contour map through the brightness range — like raising or lowering the datum elevation on a topographic survey. With a high offset, contour lines cluster in the bright regions of the image while dark areas appear as a single low-elevation zone. With zero offset, the contour map is anchored to the source signal's native brightness.

---

#### Knob 6 — Zone Sat
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Scales the chroma saturation of the composite output. The saturation is applied symmetrically around the 512 neutral axis — at full, zone and contour colors are vivid; at zero, the output is monochrome regardless of palette selection. Intermediate values produce pastel or muted versions of the terrain or bathymetric palette. This interacts with the Palette B toggle: setting Palette B to Mono and Zone Sat to zero both desaturate, but through different mechanisms — Mono forces chroma to neutral before the saturation stage, while Zone Sat scales it afterwards.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette A** | Terrain | Bathy |
| **8 — Palette B** | Tinted | Mono |
| **9 — Major/Minor** | Equal | Styled |
| **10 — Fill Mode** | HypsoFill | VideoFill |
| **11 — Bypass** | Off | On |

Toggles 7 through 10 configure the programme's visual character in four independent binary dimensions: palette origin (land or sea), chromaticity (color or monochrome), contour hierarchy (uniform or weighted), and fill source (synthetic palette or original video). Toggle 11 is the standard bypass. The five switches can be combined freely, producing 16 distinct rendering modes before any continuous parameter is adjusted.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the delayed original signal (dry) and the fully processed contour-mapped signal (wet) using three parallel interpolator instances — one per YUV channel. At full, the output is entirely the processed contour map. At zero, the original video passes through unchanged. Intermediate values blend the contour overlay with the source, producing a transparent map effect where contour lines and zone tinting are visible but the underlying video remains clearly readable.

---

## Guided Exercises

These exercises progress from basic contour rendering through palette exploration to full cartographic compositing, demonstrating how Fathom transforms video into topographic imagery.

### Exercise 1: First Survey — Basic Contour Mapping

<img src={fathom_exercise1_result} alt="First Survey — Basic Contour Mapping result"/>
*First Survey — Basic Contour Mapping — simulated result across source images.*
**Source**: A slowly panning landscape or face with smooth tonal gradients.

**Objective**: Learn how contour interval and elevation offset work together to reveal tonal structure in the source.

1. **Narrow contours**: Set Contour Int to its lowest step (16). Dense contour lines appear wherever luminance changes, creating a fine topographic mesh.
2. **Widen intervals**: Sweep Contour Int upward through the eight steps. Watch contour lines thin out and the elevation zones grow wider with each step.
3. **Shift the datum**: Slowly increase Elev Offset from zero. The contour grid slides upward through the brightness range — dark areas lose their contours first, while bright areas gain new ones.
4. **Bold lines**: Increase Line Weight to 3–4 px. The contour grid becomes a dominant structural overlay.
5. **Choose a color**: Rotate Contour Clr through the eight hues. Note how brown and blue feel cartographic while white and red feel analytical.

**Key concepts**: Contour detection compares adjacent pixels on horizontal and vertical axes, interval selects the spacing between contour levels, elevation offset shifts the entire contour map

---

### Exercise 2: Seafloor to Summit — Palette Exploration

<img src={fathom_exercise2_result} alt="Seafloor to Summit — Palette Exploration result"/>
*Seafloor to Summit — Palette Exploration — simulated result across source images.*
**Source**: Footage with wide tonal range — skylines, underwater scenes, or gradient test patterns.

**Objective**: Explore both palettes and the interaction between saturation, opacity, and fill mode.

1. **Terrain survey**: Start with Palette A = Terrain, Palette B = Tinted, Fill Mode = HypsoFill. The image appears as a color relief map with green lowlands and white peaks.
2. **Dive deep**: Switch Palette A to Bathy. The same footage now reads as an ocean depth chart — deep blues in the shadows, white in the highlights.
3. **Desaturate**: Switch Palette B to Mono. The palette becomes greyscale — relief shading without color.
4. **Reduce opacity**: Lower Zone Opac to ~30%. The palette becomes a translucent tint over the original video.
5. **Video fill**: Switch Fill Mode to VideoFill. Only contour lines remain; the zones show the original video.
6. **Saturation sweep**: Return to HypsoFill and sweep Zone Sat from 0% to 100%. Watch the palette colors go from greyscale to fully saturated.

**Key concepts**: Two complementary palettes for land and sea, monochrome mode isolates luminance structure, zone opacity controls palette transparency, video fill preserves source imagery between contours

---

### Exercise 3: Cartographic Composite — Full Map Rendering

<img src={fathom_exercise3_result} alt="Cartographic Composite — Full Map Rendering result"/>
*Cartographic Composite — Full Map Rendering — simulated result across source images.*
**Source**: A live camera feed of a face, hand, or textured object with clear tonal variation.

**Objective**: Combine all parameters to produce a full-featured topographic map overlay.

1. **Base map**: Set Contour Int to step 5 (96), Line Weight to 2 px, Contour Clr to brown, Palette A to Terrain.
2. **Major contours**: Set Major/Minor to Styled. Every fifth contour level receives the major classification.
3. **Tune elevation**: Adjust Elev Offset so contour lines are well-distributed across the subject.
4. **Opacity layer**: Set Zone Opac to ~60% for a translucent palette overlay.
5. **Saturation color**: Set Zone Sat to ~80% for vivid terrain colors.
6. **Mix blend**: Pull Mix to ~70% to let some original video texture through the composited result.
7. **Compare**: Toggle Bypass on and off to compare the raw feed with the fully mapped output.

**Key concepts**: Layered compositing — contour lines over palette zones over original video, major/minor hierarchy adds cartographic authenticity, mix control blends processed and original for subtle overlay effects

---


## Tips

- **Brown contours on terrain palette**: The default contour color (brown) with the terrain palette produces the most naturalistic topographic map effect. This is the cartographic standard.
- **Blue contours on bathymetric palette**: Switch to blue contour color when using the bathymetric palette for an authentic nautical chart appearance.
- **Elevation offset as animation**: Slowly sweeping the Elev Offset control creates a rising-water or shifting-terrain animation as contour lines migrate across the image.
- **Video fill for analysis**: Use VideoFill mode with high-contrast contour colors (white or black) to overlay a luminance contour grid on the original video — useful for technical monitoring or as a visual effect that preserves the source.
- **Opacity for layering**: Zone Opac at 20–40% produces a subtle tinted overlay that adds color depth without obscuring the original video texture.
- **Feedback loops**: Routing the output back to the input creates recursive contour mapping — contour lines themselves become elevation features, generating secondary contours at their edges.
- **Narrow intervals reveal texture**: Contour Int at 16 with thin lines reveals micro-gradients in the source — skin texture, fabric weave, and atmospheric haze all produce distinct contour patterns.
- **Wide intervals for bold graphics**: Contour Int at 192 or 256 with 4 px line weight produces a bold graphic poster effect with only a few strong contour bands.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bathymetric** | Relating to the measurement and mapping of underwater depth; bathymetric charts use blue color ramps to represent ocean floor elevation. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **Contour Line** | A curve connecting all points of equal value (here, equal luminance), also called an isoline. |
| **Hypsometric Tinting** | The cartographic technique of coloring elevation zones on a map using a graduated color palette. |
| **Index Contour** | A major contour line (every 5th level) drawn heavier for visual hierarchy, matching the convention on printed topographic maps. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **Isoline** | A line of constant value on a map or image; synonym for contour line. |
| **Line Buffer** | A BRAM-based single-scanline delay that stores the previous line's luminance for vertical neighbour comparison. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **Proc amp** | Processing amplifier; a gain-and-offset stage that applies contrast (multiplication) and brightness (addition) to a signal. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
| **Zone** | One of eight elevation bands defined by the top 3 bits of the offset luminance, each assigned a color from the selected palette. |

---
