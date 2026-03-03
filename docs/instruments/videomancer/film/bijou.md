---
draft: true
sidebar_position: 18
slug: /instruments/videomancer/bijou
title: "Bijou"
image: /img/instruments/videomancer/bijou/bijou_hero_s1.png
description: "Bijou recreates two foundational visual techniques of silent cinema: the iris mask and the title card frame."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import bijou_control_panel from '/img/instruments/videomancer/bijou/bijou_control_panel.png';
import bijou_source1_parrot from '/img/instruments/videomancer/bijou/bijou_source1_parrot.png';
import bijou_source2_car from '/img/instruments/videomancer/bijou/bijou_source2_car.png';
import bijou_source3_clouds from '/img/instruments/videomancer/bijou/bijou_source3_clouds.png';
import bijou_source4_pattern from '/img/instruments/videomancer/bijou/bijou_source4_pattern.png';
import bijou_source5_girl from '/img/instruments/videomancer/bijou/bijou_source5_girl.png';
import bijou_source6_berries from '/img/instruments/videomancer/bijou/bijou_source6_berries.png';
import bijou_hero_s1 from '/img/instruments/videomancer/bijou/bijou_hero_s1.png';
import bijou_hero_s2 from '/img/instruments/videomancer/bijou/bijou_hero_s2.png';
import bijou_hero_s3 from '/img/instruments/videomancer/bijou/bijou_hero_s3.png';
import bijou_hero_s4 from '/img/instruments/videomancer/bijou/bijou_hero_s4.png';
import bijou_hero_s5 from '/img/instruments/videomancer/bijou/bijou_hero_s5.png';
import bijou_hero_s6 from '/img/instruments/videomancer/bijou/bijou_hero_s6.png';
import bijou_ex1_s1 from '/img/instruments/videomancer/bijou/bijou_ex1_s1.png';
import bijou_ex1_s2 from '/img/instruments/videomancer/bijou/bijou_ex1_s2.png';
import bijou_ex1_s3 from '/img/instruments/videomancer/bijou/bijou_ex1_s3.png';
import bijou_ex1_s4 from '/img/instruments/videomancer/bijou/bijou_ex1_s4.png';
import bijou_ex1_s5 from '/img/instruments/videomancer/bijou/bijou_ex1_s5.png';
import bijou_ex1_s6 from '/img/instruments/videomancer/bijou/bijou_ex1_s6.png';
import bijou_ex2_s1 from '/img/instruments/videomancer/bijou/bijou_ex2_s1.png';
import bijou_ex2_s2 from '/img/instruments/videomancer/bijou/bijou_ex2_s2.png';
import bijou_ex2_s3 from '/img/instruments/videomancer/bijou/bijou_ex2_s3.png';
import bijou_ex2_s4 from '/img/instruments/videomancer/bijou/bijou_ex2_s4.png';
import bijou_ex2_s5 from '/img/instruments/videomancer/bijou/bijou_ex2_s5.png';
import bijou_ex2_s6 from '/img/instruments/videomancer/bijou/bijou_ex2_s6.png';
import bijou_ex3_s1 from '/img/instruments/videomancer/bijou/bijou_ex3_s1.png';
import bijou_ex3_s2 from '/img/instruments/videomancer/bijou/bijou_ex3_s2.png';
import bijou_ex3_s3 from '/img/instruments/videomancer/bijou/bijou_ex3_s3.png';
import bijou_ex3_s4 from '/img/instruments/videomancer/bijou/bijou_ex3_s4.png';
import bijou_ex3_s5 from '/img/instruments/videomancer/bijou/bijou_ex3_s5.png';
import bijou_ex3_s6 from '/img/instruments/videomancer/bijou/bijou_ex3_s6.png';

# Bijou

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: bijou_source1_parrot, after: bijou_hero_s1 },
    { label: "Car", before: bijou_source2_car, after: bijou_hero_s2 },
    { label: "Clouds", before: bijou_source3_clouds, after: bijou_hero_s3 },
    { label: "Pattern", before: bijou_source4_pattern, after: bijou_hero_s4 },
    { label: "Girl", before: bijou_source5_girl, after: bijou_hero_s5 },
    { label: "Berries", before: bijou_source6_berries, after: bijou_hero_s6 },
  ]}
/>
*A feathered circular iris carves a silent-cinema spotlight from a portrait, its sepia-tinted surround fading to black at the edges of the frame.*

---

## Overview

Bijou recreates two foundational visual techniques of silent cinema: the **iris mask** and the **title card frame**. In iris mode, a geometric aperture — circle, diamond, rectangle, or keyhole — reveals a portion of the input video while the surrounding area fills with dimmed, tinted imagery. In title card mode, a decorative double-rectangle border overlays the video, recreating the ornamental frames that surrounded intertitle text cards in silent films from 1895 to 1930.

The iris is computed as a real-time signed distance field (SDF). Each pixel's distance from the shape boundary determines whether it lies inside the reveal zone, in the feathered transition band, or in the masked fill region. The edge softness control scales this transition from the hard mechanical edge of a brass iris diaphragm to the gentle falloff of a photographic vignette.

The name *bijou* refers to the ornate neighborhood cinemas of the silent era — small, jewel-like theaters where audiences first experienced iris transitions, keyhole point-of-view shots, and Art Deco title cards. The program distills these essential visual elements into a single real-time video processor.

---

## Background

### The Iris in Early Cinema

The iris-in/iris-out transition was pioneered by cinematographer Billy Bitzer working with director D.W. Griffith on *The Birth of a Nation* (1915) and *Intolerance* (1916). A mechanical iris diaphragm attached to the camera lens could be opened or closed during filming to reveal or conceal the frame. The iris served as a narrative punctuation mark — iris-in to open a scene, iris-out to close it — and as a dramatic spotlight, narrowing the frame to a single character's face. Georges Méliès used vignette masks and multiple exposures as early as *A Trip to the Moon* (1902), and keyhole-shaped masks became standard shorthand for point-of-view shots.

### Signed Distance Fields

A signed distance field assigns each pixel a value representing its distance from a shape boundary. Negative values are inside the shape, positive values are outside, and zero is exactly on the edge. By comparing this distance against a softness threshold, the hardware generates a smooth alpha gradient in the feather zone — a linear ramp from fully revealed to fully masked. This approach computes four different shapes (circle, diamond, rectangle, keyhole) using only basic arithmetic: absolute values, additions, and comparisons.

### Shape Approximations

The circle SDF uses an alpha-max-beta-min approximation — `max(|dx|,|dy|) + min(|dx|,|dy|)/2` — rather than a true Euclidean distance requiring a square root. The diamond is an L1 (Manhattan) norm, the rectangle is a Chebyshev (L∞) norm, and the keyhole is the union of two offset circles, taking the minimum distance. Each requires only adders and comparators, fitting easily into the iCE40 FPGA.

### Silent Film Title Cards

Before synchronised sound, dialogue and narrative exposition were conveyed through intertitle cards — typeset text photographed and spliced between live-action shots. These cards were framed by decorative borders that evolved from simple rules to elaborate Art Deco compositions. Fritz Lang's *Metropolis* (1927) featured particularly ornate geometric borders. Bijou's title card mode generates the border geometry — double rectangles with optional 8×8 corner ornaments — providing the visual frame that the artist can compose with external text or graphics.

### Tint and Fill Processing

Silent films were often tinted by hand or chemically: amber for daytime scenes, blue for night, green for exteriors. Bijou's tint system divides the Tint Color pot into four quadrants — sepia, green, blue, and magenta — applied as additive U/V offsets to the fill region's chroma. Combined with the Fill Brightness control that scales the fill luma, this recreates the coloured fills seen in tinted silent film prints.


---

## Signal Flow

```
                              ┌────────────────────┐
data_in ─────────────────────►│ Pos Counters +     │
                              │ Register Map       │
                              └──────┬─────────────┘
                                     │ Stage 1
                                     ▼
                              ┌────────────────────┐
                              │ SDF Shape Distance  │
                              │ (circle/diamond/    │
                              │  rect/keyhole)      │
                              │ — or —              │
                              │ Title Card Border   │
                              │ Hit-Test            │
                              └──────┬─────────────┘
                                     │ Stage 2
                                     ▼
                              ┌────────────────────┐
                              │ Edge Alpha Ramp     │
                              │ + Invert            │
                              │ + Fill Processing   │
                              │ (dim + tint)        │
                              └──────┬─────────────┘
                                     │ Stage 3
                                     ▼
                              ┌────────────────────┐
                              │ Composite           │
                              │ (inside × (1-α) +   │
                              │  fill × α)          │
                              │ + Border Overlay    │
                              └──────┬─────────────┘
                                     │ Stage 4
                                     ▼
data_in ──► [sync delay] ──► dry ──► Interpolator ◄── wet
                                       (4 clk)
                                          │
                                          ▼
                                      data_out
```

The pipeline branches at Stage 2 based on the Mode toggle. In iris mode, the shape generator computes an SDF distance that becomes an alpha ramp for soft-edged masking. In title card mode, the hit-test checks whether the pixel falls on the outer border, inner border, corner ornament, or fill zone. Both paths converge at Stage 4 where compositing blends inside video, filled region, and border elements. The fill processing in Stage 3 simultaneously prepares dimmed/tinted video for the masked area regardless of which mode produces the alpha values.

The 4-clock interpolator at the output provides a final wet/dry crossfade between the processed iris composite and the original delayed input. This allows the iris effect to be dialed in from subtle vignette overlay to full silent-cinema mask.

---

## Parameter Reference

<img src={bijou_control_panel} alt="Videomancer front panel with Bijou loaded"/>
*Videomancer's front panel with Bijou active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the iris aperture size or, in title card mode, the border margin. The pot value is scaled to approximately 0–640 pixels by adding `pot + pot/4`. At minimum, the iris closes to a tiny pinpoint; at maximum, the iris opens wide enough to reveal nearly the entire frame. In title card mode, larger values push the border frame closer to the centre of the image. At about 75% the iris reveals most of the frame with a comfortable border margin — the classic "full shot" iris size.

---

#### Knob 2 — Center X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the iris centre horizontally. The pot value is scaled to pixel coordinates using the same `pot + pot/4` formula. At the centre position (512), the iris is centred on the frame. Turning counter-clockwise moves the iris left; turning clockwise moves it right. This is essential for the off-centre iris-down technique used by Griffith to spotlight a character who isn't at frame centre.

---

#### Knob 3 — Center Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the iris centre vertically. Identical scaling to Center X. At the centre position, the iris sits at mid-frame. Adjusting this along with Center X lets you place the iris spotlight anywhere in the frame. In title card mode, Center X and Y have no effect since the border is always frame-centred.

---

#### Knob 4 — Softness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the feather width of the iris edge. At 0%, the edge is a hard binary mask — inside or outside with no transition, matching the sharp mechanical edge of a real brass camera iris. As the value increases, the transition zone widens into a smooth gradient, eventually producing the gradual darkening of a photographic vignette. The softness is implemented as a linear ramp across the SDF distance band `[-softness, +softness]`, so larger values create wider transition zones.

---

#### Knob 5 — Fill Brt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the brightness of the fill region — the area outside the iris (or between the borders in title card mode). At 0%, the fill is completely black, matching the traditional silent-cinema iris look. At 100%, the fill region shows the original video at full brightness. Intermediate values create a dimmed surround, useful for spotlight effects where the context remains visible but de-emphasised. The brightness is applied as a multiplication: `fill_y = source_y × fill_bright / 1024`.

---

#### Knob 6 — Tint Color
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Selects the colour tint applied to the fill region and title card borders. The pot's top two bits select one of four colour quadrants: sepia/amber (U−30, V+50), green (U−40, V−30), blue (U+60, V−20), or magenta (U+30, V+40). These offsets are added to the fill region's chroma channels, tinting the dimmed surround. In title card mode, the same tint colour is used for the border lines themselves, drawn at a fixed brightness of 800.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Iris | Title |
| **8 — Shape** | Circle | Diamond |
| **9 — Shape Alt** | Rect | Keyhole |
| **10 — Invert** | Normal | Invert |
| **11 — Bypass** | Off | On |

The five toggles configure the iris geometry and mode. Toggle 7 selects between iris mask and title card border — two mutually exclusive visual techniques. Toggles 8 and 9 work together to select one of four iris shapes. Toggle 10 inverts the alpha mask, swapping the reveal and fill regions. Toggle 11 bypasses all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) and wet (processed) signal at the output stage using three parallel interpolators. At 0% the output is the unmodified input; at 100% the output is fully processed with iris or title card overlay. Intermediate values blend the effect, useful for creating subtle vignette overlays.

---

## Guided Exercises

These exercises progress from simple iris masks through shape exploration to title card framing, demonstrating the full range of silent cinema visual techniques.

### Exercise 1: Classic Iris Spotlight

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: bijou_source1_parrot, after: bijou_ex1_s1 },
    { label: "Car", before: bijou_source2_car, after: bijou_ex1_s2 },
    { label: "Clouds", before: bijou_source3_clouds, after: bijou_ex1_s3 },
    { label: "Pattern", before: bijou_source4_pattern, after: bijou_ex1_s4 },
    { label: "Girl", before: bijou_source5_girl, after: bijou_ex1_s5 },
    { label: "Berries", before: bijou_source6_berries, after: bijou_ex1_s6 },
  ]}
/>
*Classic Iris Spotlight — simulated result across source images.*
**Source**: A portrait or scene with a clear subject.

**Objective**: Create the classic silent-cinema iris-out spotlight effect.

1. **Open iris**: Set Size to about 50%, Centre X and Y both at 50%. A circular iris reveals the centre of the frame.
2. **Hard edge**: Set Softness to 0%. The edge is sharp — a mechanical iris diaphragm.
3. **Black surround**: Set Fill Brt to 0%. The fill region goes to black, the classic look.
4. **Soften gradually**: Increase Softness. The hard edge melts into a vignette.
5. **Move spotlight**: Adjust Centre X and Y to place the iris over a specific subject.
6. **Close iris**: Slowly reduce Size toward 0%. Watch the iris close down to a pinpoint.

**Key concepts**: SDF distance produces the alpha mask, Softness scales the feather width, Fill Brightness darkens the surround, centre controls position the spotlight

---

### Exercise 2: Shape Exploration

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: bijou_source1_parrot, after: bijou_ex2_s1 },
    { label: "Car", before: bijou_source2_car, after: bijou_ex2_s2 },
    { label: "Clouds", before: bijou_source3_clouds, after: bijou_ex2_s3 },
    { label: "Pattern", before: bijou_source4_pattern, after: bijou_ex2_s4 },
    { label: "Girl", before: bijou_source5_girl, after: bijou_ex2_s5 },
    { label: "Berries", before: bijou_source6_berries, after: bijou_ex2_s6 },
  ]}
/>
*Shape Exploration — simulated result across source images.*
**Source**: A colourful scene with strong composition.

**Objective**: Compare the four iris shapes and understand their geometric properties.

1. **Circle**: Start with default Circle shape. Note the rounded aperture.
2. **Diamond**: Toggle Shape to Diamond. The aperture becomes a 45-degree rotated square.
3. **Rectangle**: Toggle Shape back to Circle, set Shape Alt to Rect. A 4:3 aspect rectangle appears.
4. **Keyhole**: Toggle Shape Alt to Keyhole. Two overlapping circles create a figure-eight.
5. **Invert each**: For each shape, toggle Invert to see the negative — the shape becomes a void.
6. **Soft diamond**: On Diamond shape, increase Softness to 60%. The angular edges become a soft diamond vignette.

**Key concepts**: Four shapes from four distance metrics (Euclidean approx, L1, Chebyshev, union), Shape and Shape Alt toggles combine to select between them, Invert flips the mask

---

### Exercise 3: Title Card Frame

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: bijou_source1_parrot, after: bijou_ex3_s1 },
    { label: "Car", before: bijou_source2_car, after: bijou_ex3_s2 },
    { label: "Clouds", before: bijou_source3_clouds, after: bijou_ex3_s3 },
    { label: "Pattern", before: bijou_source4_pattern, after: bijou_ex3_s4 },
    { label: "Girl", before: bijou_source5_girl, after: bijou_ex3_s5 },
    { label: "Berries", before: bijou_source6_berries, after: bijou_ex3_s6 },
  ]}
/>
*Title Card Frame — simulated result across source images.*
**Source**: Any video — the border frame works as an overlay on any content.

**Objective**: Create a decorative silent-film intertitle frame with tinted fill.

1. **Switch to Title Card**: Toggle Mode to Title. The iris disappears, replaced by a double-rectangle border.
2. **Set margin**: Adjust Size to about 60%. The border moves inward, creating a wide decorative frame.
3. **Add tint**: Set Tint Color to the sepia quadrant (around 10%). The border lines and fill region take on a warm amber tone.
4. **Dim fill**: Set Fill Brt to about 30%. The video between the borders is dimmed but visible.
5. **Add ornaments**: Toggle Shape Alt to Keyhole. Small 8×8 corner ornament blocks appear at the inner rectangle's corners.
6. **Try blue tint**: Move Tint Color to the blue quadrant (around 60%). The frame takes on a cool blue tone — the nighttime tint of silent cinema.

**Key concepts**: Title card mode generates geometric border frames, Size controls margin width, Tint Color sets border and fill colour, Shape Alt enables corner ornaments

---


## Tips

- **Iris for transitions**: Animate the Size pot from 100% to 0% for a classic iris-out. The reverse creates an iris-in reveal.
- **Off-centre for drama**: Move Centre X/Y away from 50% to spotlight a specific subject — the D.W. Griffith technique.
- **Soft vignette for portraits**: Circle shape at large size with high Softness creates a subtle portrait vignette that darkens the frame edges.
- **Keyhole for POV shots**: The keyhole shape at small size with hard edges creates the classic "looking through a keyhole" point-of-view effect.
- **Fill Brightness for context**: Instead of pure black surround, set Fill Brt to 20–30% so the audience can see the broader scene context while attention is drawn to the spotlight.
- **Title card + external text**: Use Title Card mode as a border frame, then composite text from another source into the revealed centre area.
- **Invert for negative space**: An inverted small circle creates a dramatic void — a dark spot that draws the eye by its absence.
- **Tint for period authenticity**: Sepia tint + dimmed fill = authentic silent-film amber tone. Blue + low brightness = classic "night" tinting.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha ramp** | A gradual transition from fully transparent to fully opaque, computed from the signed distance field to produce feathered mask edges. |
| **Art Deco** | An early 20th-century decorative style characterized by bold geometric forms, influencing the ornamental borders of silent-film title cards. |
| **Chebyshev distance** | A distance metric returning the greater of the horizontal and vertical separations between two points; used here for the rectangle iris shape. |
| **Chrominance** | The color-difference components (U and V) of a YUV video signal, separate from luminance. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline in hardware. |
| **Interpolator** | A hardware module that performs linear crossfading between two signals (wet and dry) based on a mix parameter. |
| **Iris diaphragm** | A mechanical aperture in a camera lens made of overlapping blades that can be opened or closed to control the exposed area of the frame. |
| **Luminance** | The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color. |
| **Manhattan distance** | The sum of absolute horizontal and vertical differences between two points (L1 norm); used here for the diamond iris shape. |
| **SDF** | Signed Distance Field; a representation where each pixel stores its signed distance from a shape boundary, enabling smooth feathered-edge rendering. |
| **Vignette** | A gradual darkening or fading toward the edges of an image, often used to draw attention to the centre of the frame. |
| **YUV** | A color encoding that separates luminance (Y) from two chrominance components (U and V), used in broadcast video. |

---
