---
draft: true
sidebar_position: 172
slug: /instruments/videomancer/lightshow
title: "Light Show"
image: /img/instruments/videomancer/lightshow/lightshow_hero.png
description: "Light Show generates the undulating, amoeba-like color fields of 1960s liquid light projections."
---

import lightshow_hero from '/img/instruments/videomancer/lightshow/lightshow_hero.png';
import lightshow_animation from '/img/instruments/videomancer/lightshow/lightshow_animation.gif';
import lightshow_control_panel from '/img/instruments/videomancer/lightshow/lightshow_control_panel.png';
import lightshow_exercise1_result from '/img/instruments/videomancer/lightshow/lightshow_exercise1_result.gif';
import lightshow_exercise2_result from '/img/instruments/videomancer/lightshow/lightshow_exercise2_result.gif';
import lightshow_exercise3_result from '/img/instruments/videomancer/lightshow/lightshow_exercise3_result.gif';

# Light Show

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lightshow_hero} alt="Light Show hero image"/>
*Liquid light pools drift and merge — iridescent fringes shimmer at the boundaries where amorphous blobs meet, evoking the psychedelic overhead projector shows of the 1960s.*
<img src={lightshow_animation} alt="Light Show animated output"/>
*Light Show output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Light Show generates the undulating, amoeba-like color fields of 1960s liquid light projections. Four invisible blob centers orbit on Lissajous trajectories, each generating an inverse-distance field. Where two fields overlap, thin-film interference fringes emerge as rainbow or monochrome shimmer lines. The result is an ever-shifting landscape of soft-edged color pools with iridescent boundaries — no two frames are identical.

The program name references the Joshua White Light Show and Brotherhood of Light collectives who projected dyed oils and inks pressed between glass on overhead projectors at rock concerts. The heat from the projector lamp and manual manipulation created slowly evolving, unpredictable organic shapes with brilliant prismatic edge effects. Videomancer recreates this digitally using per-pixel distance field computation against four orbiting points.

The visual palette ranges from warm amber oil tones to full psychedelic rainbow, controllable via the Palette toggle. Blob shapes can be round (circular distance fields) or flat (vertically compressed), and the fringe boundaries can be rendered as spectral rainbow or single-hue monochrome lines. At low speed, the blobs drift glacially like cells under a microscope. At high speed, they whip around their orbits, creating rapid color cycling and stroboscopic fringe patterns.

---

## Quick Start

1. **Start with 2 blobs**: Begin with Blob Count at 2 to clearly see the fringe boundary between a single pair of fields. Add more blobs as you become comfortable.
2. **Oil + Rainbow is the classic look**: The Oil palette with Rainbow fringe mode most closely approximates the liquid light show aesthetic from 1960s concerts.
3. **Spread sets the mood**: Large Spread values fill the screen with colour, creating an immersive environment. Small values create isolated floating shapes in darkness.

---

## Background

### The Liquid Light Show Tradition

The liquid light show emerged in San Francisco in 1966, pioneered by artists such as Bill Ham, Elias Romero, and the Joshua White Light Show. Performers placed clock crystals, Petri dishes, or custom-built cells filled with dyed water and immiscible oils on the glass of overhead projectors. As the heat and manual pressure deformed the oil globules, the projected image showed enormous, slowly morphing color fields with brilliant interference fringes at the boundaries between oil and water. The aesthetic was inseparable from the psychedelic counterculture — formless, unpredictable, and hypnotic.

### Metaballs and Distance Fields

Light Show's rendering algorithm is closely related to the metaball (isosurface) technique developed in computer graphics by Jim Blinn (1982). Each blob contributes an inverse-distance field, and the visible surface is the isoline where the combined field exceeds a threshold. In the FPGA, Manhattan distance (|dx| + |dy|) is used instead of Euclidean to avoid costly square root operations, but the visual result retains the organic blobby quality. The two-nearest sorting step enables fringe detection at the boundary between the closest and second-closest blob regions.

### Lissajous Orbits

Each blob center follows an independent Lissajous path — sinusoidal motion in X and Y at different frequency ratios. The four blobs use fixed frequency multiplier ratios (1:2, 2:3, 3:1, 5:4), producing complex non-repeating trajectories that fill the screen over time. This is the same mathematical framework as the harmonograph, but applied here to position rather than pen-tip drawing. The Speed control scales the DDS phase increment, speeding up or slowing down all four orbits proportionally.

### Thin-Film Interference Fringes

At the boundary between two blob regions — where the nearest and second-nearest blob distances are close — the program generates a fringe pattern that simulates the thin-film interference seen at oil-water boundaries. In Rainbow fringe mode, the fringe distance is mapped through a sinusoidal UV colour space rotation, producing spectral bands. In Mono mode, fringes appear as luminance-only intensity lines without colour shift.

### Quarter-Wave Sine LUT

The sinusoidal functions for both Lissajous orbit computation and fringe colour mapping use a shared 64-entry quarter-wave sine lookup table. Full 360° coverage is achieved through quadrant mirroring and sign inversion. The 10-bit output resolution provides smooth curves without visible stepping at video rates.


---

## Signal Flow

```
DDS Phase Accums (×4) ──→ [Sine LUT] ──→ Blob Positions (cx, cy)
                                                │
Screen (h_count, v_count) ──→ [Manhattan Dist ×4] ──→ [Min1/Min2 Sort]
                                                           │
                                          ┌────────────────┤
                                          ▼                ▼
                                    [Luma from Min1]  [Fringe from Min2-Min1]
                                          │                │
                                          ▼                ▼
                                    [Brightness ×]    [Hue → UV Sine Map]
                                          │                │
                                          └─────┬──────────┘
                                                ▼
Input Y/U/V ──→ [Delay SR] ──→ [Interpolator Mix] ◄── wet Y/U/V
                                        │
                                   Output Y/U/V
```

The core computation happens per-pixel in a single clock cycle: four Manhattan distances are calculated, then a two-pass sort finds the nearest (min1) and second-nearest (min2) blob distances. Luminance is derived from how far inside the nearest blob's field the pixel lies (spread - min1). The fringe effect comes from the gap between min2 and min1 — a small gap means the pixel is at a blob junction where two fields are nearly equal, producing the characteristic boundary shimmer.

Blob animation runs once per frame during vsync, advancing the four DDS phase accumulators and computing new screen-space positions through the shared sine LUT. This keeps the per-pixel pipeline free of temporal state and fully combinational.

---

## Parameter Reference

<img src={lightshow_control_panel} alt="Videomancer front panel with Light Show loaded"/>
*Videomancer's front panel with Light Show active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

Controls the orbital velocity of all four blob centers. The Speed register scales the DDS phase increment — at zero, the blobs are frozen in place. At maximum, they whip through their Lissajous orbits rapidly, creating fast swirling motion and stroboscopic fringe patterns. Moderate values produce the classic slow, hypnotic drift associated with liquid light shows.

---

#### Knob 2 — Blob Count
| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 4 |

Selects the number of active blobs via an 8-step quantised control. Although the FPGA always computes four blob distance fields, the Blob Count register determines how many contribute to the visible output. Fewer blobs create simpler, larger fields with less boundary interaction. More blobs fragment the screen into a dense web of overlapping fringe boundaries.

---

#### Knob 3 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the radial extent of each blob's field. This is the threshold distance below which a pixel is considered "inside" a blob. Larger Spread values create bigger, more diffuse colour pools that fill more of the frame. Smaller values create compact, distinct separate blobs with more dark space between them. The spread also affects fringe visibility — wider spread means fringe boundaries are broader and more visible.

---

#### Knob 4 — Fringe
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the width of the interference fringe zone at blob boundaries. A small Fringe value produces tight, hair-thin spectral lines at the exact junction between two blob regions. A large value expands the fringe zone outward, creating wide bands of rainbow or monochrome shimmer. At zero, fringes are invisible and the output shows only solid blob colours.

---

#### Knob 5 — Hue Offset
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

Rotates the base hue applied to both the fringe colour mapping and the psychedelic palette mode. The UV sine map is offset by this value, effectively spinning the colour wheel. Sweeping this control produces a slow shift through the entire spectrum, useful for matching the colour scheme to other elements in a video mix.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

At centre (512), brightness is approximately unity — the original distance-to-luminance mapping is preserved. Below centre, the blobs are dimmed. Above centre, they are amplified, potentially producing bright white-hot centres with saturated colour fringes. Internally, multiplies the output luminance of the blob fields.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Oil | Psychedelic |
| **8 — Shape** | Round | Flat |
| **9 — Fringe Mode** | Rainbow | Mono |
| **10 — Video Seed** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles shape the palette, geometry, fringe style, video interaction, and bypass. Palette and Fringe Mode together determine the colour character — Oil + Rainbow produces classic warm pools with prismatic edge fringes, while Psychedelic + Mono creates position-dependent colour fields with luminance-only boundaries. Shape changes the blob geometry between circular and vertically compressed ellipses. Video Seed modulates the blob animation from input video luminance for reactive live visuals.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the dry input signal and the synthesised light show output. At 0%, only the input video is visible. At 100%, only the synthesis output is visible. Intermediate positions blend the two, creating a ghostly overlay of drifting colour pools on top of the live video feed.





---

## Guided Exercises

These exercises progress from observing basic blob drift through fringe colour exploration to creating complex multi-blob light show compositions. Each builds on the controls introduced in the previous one.

### Exercise 1: Basic Liquid Drift

<img src={lightshow_exercise1_result} alt="Basic Liquid Drift result"/>
*Basic Liquid Drift — simulated result across source images.*
**What You'll Create**: Understand how the blob centers orbit and create soft-edged colour pools with the default Oil palette.

1. **Start simple**: Set Speed to ~20%, Blob Count to 2, Spread to ~60%, Fringe to ~40%, Mix to 100%.
2. **Watch the drift**: Two warm amber blobs appear and drift slowly across the screen on their Lissajous orbits.
3. **Observe fringe**: Where the two blobs approach each other, a thin rainbow shimmer line appears at the boundary.
4. **Increase speed**: Push Speed to ~50%. The blobs orbit faster, and the fringe line dances between them more rapidly.
5. **Increase blob count**: Turn Blob Count to 4. The screen fills with overlapping fields and multiple fringe boundaries.

**Key concepts**: Inverse-distance fields create soft-edged blobs, blob count controls visual complexity, fringe appears at field junctions

---

### Exercise 2: Psychedelic Fringe Exploration

<img src={lightshow_exercise2_result} alt="Psychedelic Fringe Exploration result"/>
*Psychedelic Fringe Exploration — simulated result across source images.*
**What You'll Create**: Explore the full colour range by switching to the Psychedelic palette and sweeping hue offset through the spectrum.

1. **Switch palette**: Toggle Palette to Psychedelic. The blob interiors now show position-dependent colour swirls.
2. **Widen fringe**: Increase Fringe to ~80%. The interference bands at blob boundaries become wide, colourful ribbons.
3. **Sweep hue**: Slowly rotate Hue Offset through 360°. The entire colour scheme rotates through the spectrum.
4. **Try mono fringe**: Toggle Fringe Mode to Mono. The boundary lines become luminance-only contours — subtler but more precise.
5. **Flatten blobs**: Toggle Shape to Flat. The blobs stretch into horizontal ellipses, creating wider vertical fringe bands.
6. **Boost brightness**: Push Brightness above 75%. The blob centres turn white-hot while the colour fringes remain saturated.

**Key concepts**: Psychedelic palette maps position to hue, fringe width controls boundary band size, mono fringe shows contour lines, flat shape creates elliptical fields

---

### Exercise 3: Reactive Video Light Show

<img src={lightshow_exercise3_result} alt="Reactive Video Light Show result"/>
*Reactive Video Light Show — simulated result across source images.*
**What You'll Create**: Create a live-reactive light show by enabling Video Seed and blending the synthesis with the input signal.

1. **Set base**: Speed ~25%, Blob Count 4, Spread ~50%, Fringe ~50%, Palette Oil, Mix ~70%.
2. **Enable video seed**: Toggle Video Seed to On. The blob fields now react to the brightness of the input video.
3. **Feed live video**: With a camera or video source active, observe how the blob patterns shift and pulse in response to the input luminance.
4. **Adjust mix**: Pull Mix to ~50%. The liquid light overlay blends with the live input, creating a psychedelic double-exposure.
5. **Try rainbow fringe**: Switch Fringe Mode to Rainbow. The boundary fringes add prismatic colour to the overlay, creating a more vivid composite.
6. **Slow down**: Reduce Speed to ~10% for a glacial, meditative drift that responds gently to the video content.

**Key concepts**: Video Seed connects input luminance to blob animation, mix controls blend depth, combining Oil palette with live input creates authentic concert projection feel

---


## Tips

- **Fringe width is subtle**: The Fringe control has a large effect on visual character. Wide fringes create broad spectral bands; narrow fringes produce precise contour lines.
- **Slow speed is mesmerising**: Very low Speed values create glacial, almost imperceptible motion that holds attention over long periods.
- **Flat shape mimics real oil**: Real dyed oil on glass tends to flatten horizontally. Use Flat mode for a more physically authentic look.
- **Bypass for comparison**: Use Toggle 11 for instant A/B comparison without losing your settings.
- **Video Seed adds reactivity**: Enable Video Seed when performing live to create a light show that responds to the camera input.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDS (Direct Digital Synthesis)** | A technique for generating periodic waveforms by incrementing a phase accumulator and looking up the corresponding amplitude, used here to animate blob orbital positions. |
| **Distance field** | A scalar field that assigns to each pixel the distance to the nearest point of interest (blob centre), used for rendering soft-edged shapes without explicit geometry. |
| **Fringe** | An interference pattern at the boundary between two regions, inspired by the thin-film colour bands at oil-water interfaces in real liquid light projections. |
| **Isosurface** | A contour in a scalar field where the value equals a threshold; the visible edge of each blob is an isoline of the combined distance field. |
| **Lissajous** | A family of parametric curves generated by two sinusoidal oscillations at different frequencies, used here for organic, non-repeating blob orbital paths. |
| **Manhattan distance** | The sum of absolute horizontal and vertical offsets (|dx| + |dy|), used as a computationally efficient approximation of Euclidean distance in the FPGA. |
| **Metaball** | A computer graphics technique for rendering organic blobs by summing inverse-distance fields and extracting an isosurface; closely related to Light Show's rendering. |
| **Phase accumulator** | A digital counter that wraps at its maximum value, used in DDS to track the current position within a periodic waveform cycle. |
| **Quarter-wave LUT** | A lookup table storing only the first quadrant (0°–90°) of a sine wave; full 360° coverage is achieved through symmetry (reflection and negation). |

---
