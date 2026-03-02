---
draft: true
sidebar_position: 94
slug: /instruments/videomancer/emboss
title: "Emboss"
image: /img/instruments/videomancer/emboss/emboss_hero.png
description: "Every surface tells a story through the way it catches light."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import emboss_hero from '/img/instruments/videomancer/emboss/emboss_hero.png';
import emboss_control_panel from '/img/instruments/videomancer/emboss/emboss_control_panel.png';
import emboss_exercise1_result from '/img/instruments/videomancer/emboss/emboss_exercise1_result.png';
import emboss_exercise2_result from '/img/instruments/videomancer/emboss/emboss_exercise2_result.png';
import emboss_exercise3_result from '/img/instruments/videomancer/emboss/emboss_exercise3_result.png';
import emboss_source1_kodim02 from '/img/instruments/videomancer/emboss/emboss_source1_kodim02.png';
import emboss_source2_kodim07 from '/img/instruments/videomancer/emboss/emboss_source2_kodim07.png';
import emboss_source3_kodim01_bw from '/img/instruments/videomancer/emboss/emboss_source3_kodim01_bw.png';

# Emboss

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: emboss_source1_kodim02, after: emboss_hero },
    { label: "Kodim07", before: emboss_source2_kodim07, after: emboss_hero },
    { label: "Kodim01 B&W", before: emboss_source3_kodim01_bw, after: emboss_hero },
  ]}
/>
*Emboss rendering directional bas-relief lighting across luminance gradients, carving depth from flat video.*

---

## Overview

Every surface tells a story through the way it catches light. A coin pressed into clay, a name stamped into leather, a fossil embedded in stone — these are all forms of relief, where three-dimensional structure is revealed by the interplay of highlights and shadows across a surface. Emboss brings this principle to video, computing spatial gradients in both horizontal and vertical directions and combining them under a virtual light source to create the illusion of a raised or carved surface.

The program works by measuring how brightness changes from pixel to pixel (horizontally) and from line to line (vertically). These two gradients — essentially the slope of the image in two perpendicular directions — are combined according to a selectable light angle that determines which edges appear illuminated and which fall into shadow. The result is added to a bias level (typically mid-gray) to produce a bas-relief effect where bright edges on one side of an object are matched by dark edges on the opposite side. The name comes directly from the metalworking and printing term for raising a design above a surface.

At moderate depth settings, Emboss creates convincing three-dimensional textures from flat video — text appears stamped into metal, faces gain sculptural weight, and architectural details develop tactile presence. At extreme settings, the effect becomes a high-contrast edge map where only the steepest gradients survive, useful as a key source or for generating abstract line-art textures from photographic material.

---

## Background

### Bas-Relief Sculpture

The technique that Emboss emulates has roots stretching back thousands of years. **Bas-relief** (from the Italian *basso-rilievo*, "low relief") is a sculptural method where figures project slightly from a flat background. Unlike freestanding sculpture, bas-relief relies entirely on the way a single light source rakes across the surface to reveal form. The shadows cast by the raised portions create the perception of depth. Ancient Egyptian temple walls, Greek friezes, and Renaissance architectural ornament all exploit this principle. Emboss translates the same idea into the pixel domain: spatial gradients become the raised surface, and the light angle control determines where the virtual illumination falls.

### Embossing in Printing and Manufacturing

In commercial printing and packaging, **embossing** is the process of creating a raised image on paper or card stock using matched male and female dies. A related technique, **debossing**, pushes the image *into* the surface rather than raising it. The Style toggle (Raised/Carved) in Emboss mirrors this distinction exactly — the Carved position negates the gradient combination, reversing which edges receive highlights versus shadows. Blind embossing (without ink) relies entirely on the play of ambient light across the raised surface, just as the Gray color mode strips chroma and presents the relief as pure luminance.

### Sobel and Prewitt Edge Detection

Emboss's gradient computation is closely related to classical edge detection kernels used in image processing. The **Sobel operator** convolves a 3×3 kernel with the image to estimate horizontal and vertical derivatives, weighting the center row/column more heavily. The **Prewitt operator** uses equal weights. Emboss simplifies this to a minimal 1×2 kernel in each direction: the horizontal gradient is simply *current pixel minus previous pixel*, and the vertical gradient is *current pixel minus previous line*. This minimal kernel is computationally cheap (a single subtraction per axis) and fits naturally into the FPGA's scanline-sequential processing model, where a one-pixel register delay and a one-line BRAM buffer are all that are needed. The resulting gradients capture the same directional edge information as larger kernels, with slightly more sensitivity to noise.

### Directional Lighting in 3D Graphics

In real-time 3D rendering, the appearance of a surface under illumination is computed from the **dot product** of the surface normal and the light direction vector. For a heightfield (a 2D surface where each pixel represents a height), the surface normal at any point can be approximated from the horizontal and vertical gradients of the height values. Emboss uses exactly this principle: the Y channel acts as a heightfield, the two gradients approximate the surface normal, and the light angle control rotates the virtual light source around the compass. The eight selectable directions (E, SE, S, SW, W, NW, N, NE) correspond to the eight combinations of positive, negative, and zero contributions from each gradient axis — a discrete approximation of a continuously rotating dot product.

### Metallic Surface Rendering

The Metal Tint control adds a luminance-dependent color shift to the source chroma, mimicking the way metallic surfaces reflect colored light. In physical metallurgy, the color of a metal surface depends on which wavelengths its free electrons absorb and re-emit. Gold absorbs blue, copper absorbs green and blue, and steel reflects nearly equally. The Metal Tint effect approximates this by using the embossed luminance to modulate the U and V channels in opposite directions — brighter areas shift toward one hue while darker areas shift toward the complementary hue, creating the iridescent color variation seen on brushed or anodized metal surfaces.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register         (latch current Y, U, V)
│   ├─ 2. Horizontal Gradient    (current Y − previous pixel Y)
│   ├─ 3. Vertical Gradient      (current Y − previous line Y via BRAM)
│   ├─ 4. Direction Select       (8-way mux: pot upper 3 bits → sign combo of H/V)
│   ├─ 5. Style Negate           (carved: negate combined gradient)
│   ├─ 6. Depth Multiply         (combined × depth pot, scaled)
│   ├─ 7. Sharpen Add            (add edge-boost: combined × sharpen pot)
│   ├─ 8. Bias Add               (DC offset: emboss + bias pot)
│   ├─ 9. Contrast Expand        (stretch around mid-gray: (val−512) × k + 512)
│   ├─ 10. Invert                (optional: 1023 − result)
│   └─ 11. Clamp                 (0–1023)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ A. Gray Mode              (U=512, V=512 — neutral gray)
│   └─ B. Source Color Mode
│       ├─ Metal Tint             (luminance-dependent U/V shift)
│       └─ Clamp                  (0–1023)
│
├── Wet/Dry Mix ────────────────────────────────────────────────
│   └─ 3× interpolator_u         (mix fader crossfades Y, U, V)
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock pipeline delay    (hsync, vsync, field, data)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical architectural detail is that gradients are computed only on the Y (luminance) channel. The horizontal gradient uses a single register delay — one clock cycle stores the previous pixel, and the subtraction yields the horizontal slope. The vertical gradient uses a BRAM-based line buffer that stores the entire previous scanline's Y values, allowing a per-pixel subtraction between the current and previous lines. These two gradients are combined through an 8-way multiplexer controlled by the upper three bits of the Light Angle pot, which selects cardinal and diagonal compass directions by choosing sign combinations and half-amplitude scaling of the H and V gradients.

After direction selection, the combined gradient passes through depth scaling (multiplication by the Depth pot), optional sharpening (additive edge boost), bias offset (DC level shift to make the emboss visible against a neutral background), and contrast expansion (gain around mid-gray). The U/V path is separate and simpler — in Gray mode, chroma is replaced with neutral 512; in Source Color mode, the original chroma is preserved with an optional metallic tint that shifts U and V in opposite directions proportional to the source luminance.

---

## Parameter Reference

<img src={emboss_control_panel} alt="Videomancer front panel with Emboss loaded"/>
*Videomancer's front panel with Emboss active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the amplitude of the emboss effect by scaling the combined directional gradient before it is added to the bias level. At 0%, the gradient is fully attenuated and the output is determined entirely by the bias and contrast settings — effectively a flat gray field. As Depth increases, edges in the source image produce progressively stronger highlights and shadows in the output. At maximum, even subtle gradients in the source are amplified into strong relief, and the effect transitions from a gentle surface texture to a high-contrast edge detector.

---

#### Knob 2 — Light Ang
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 90deg |
| Suffix | deg |

Selects the virtual light source direction from eight compass points. The pot's upper three bits map to East (0), Southeast (1), South (2), Southwest (3), West (4), Northwest (5), North (6), and Northeast (7). Each direction determines the sign combination of the horizontal and vertical gradients: East uses only the horizontal gradient with positive sign, South uses only the vertical gradient, and diagonal directions average both gradients with appropriate signs. Rotating through the eight positions changes which side of each edge receives the highlight and which receives the shadow, creating the appearance of the light source orbiting the embossed surface.

---

#### Knob 3 — Bias
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the DC offset added to the emboss gradient before output. At 0%, the bias is zero and the emboss output is centered around black — only positive gradients are visible. At the default 50% (register value 512), the bias places the neutral surface at mid-gray, allowing both highlights (above mid-gray) and shadows (below mid-gray) to be visible. At 100%, the neutral surface is near white and only negative gradients (shadows) appear as darker-than-white regions. The bias acts as a virtual surface color for the embossed relief.

---

#### Knob 4 — Sharpen
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Adds an edge-sharpening component to the emboss output by mixing a portion of the raw gradient magnitude back into the depth-scaled signal. At 0%, no sharpening is applied and the relief is smooth. As Sharpen increases, edges become more pronounced and the transition between highlight and shadow grows steeper. At high values, Sharpen effectively doubles the edge response, making fine details in the source more visible in the embossed output. This interacts with Depth — both amplify edges, but Depth scales the directional gradient while Sharpen adds an omnidirectional edge boost.

---

#### Knob 5 — Metal Tnt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls a luminance-dependent color shift applied when the Color toggle is set to Source. The Metal Tint value is divided by four to produce a tinting coefficient, which is then multiplied by the source luminance value. The resulting product is added to the U channel and subtracted from the V channel, creating complementary hue shifts in bright versus dark areas. At 0%, source chroma passes through unmodified. At higher values, the embossed surface develops an iridescent, anodized-metal quality where highlights and shadows take on different hues. Metal Tint has no effect in Gray mode because the chroma channels are replaced with neutral 512.

---

#### Knob 6 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies a gain around middle gray to the embossed output. The contrast coefficient is computed as half the pot value plus 256 (giving a range of 256 to 767 from a neutral multiplier of 512). The embossed signal is offset to center it around zero, multiplied by this coefficient, then shifted back. At the default 50% (register 512), contrast is unity and the emboss appears as computed. Below 50%, the relief is softened — highlights and shadows compress toward mid-gray. Above 50%, the relief is exaggerated — subtle emboss textures are stretched into starker highlight/shadow pairs. Extreme settings clip the output, producing binary black-and-white edge maps.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Raised | Carved |
| **8 — Color** | Gray | Source |
| **9 — Channel** | Y Only | YUV |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 configure independent qualitative aspects of the emboss effect. Style (Raised/Carved) reverses the gradient polarity, flipping the apparent direction of the relief. Color (Gray/Source) determines whether the output is monochrome relief or carries the original video's chroma information. Channel (Y Only/YUV) controls whether the emboss processing extends to chroma channels. Invert reverses the final luminance polarity. Bypass routes the input directly to the output for A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the original (dry) signal and the embossed (wet) signal using three parallel interpolators — one each for Y, U, and V. At 0% (register 0), the output is entirely the original input. At 100% (register 1023, the default), the output is entirely the embossed result. Intermediate values produce a blend where the emboss texture is partially visible over the original image. This is particularly useful for subtle surface texturing: a low mix value overlays a gentle relief onto the source video without losing the original detail.

---

## Guided Exercises

These exercises progress from basic directional emboss to complex metallic surface textures. Each builds familiarity with a different part of the processing chain.

### Exercise 1: Sculptural Relief

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: emboss_source1_kodim02, after: emboss_exercise1_result },
    { label: "Kodim07", before: emboss_source2_kodim07, after: emboss_exercise1_result },
    { label: "Kodim01 B&W", before: emboss_source3_kodim01_bw, after: emboss_exercise1_result },
  ]}
/>
*Sculptural Relief — simulated result across source images.*
**Source**: A portrait or face with strong contours and varied skin tones.

**Objective**: Learn how Depth, Light Angle, and Bias interact to create a convincing bas-relief.

1. **Basic relief**: Set Depth to ~50%. A subtle emboss appears — edges gain highlight/shadow pairs.
2. **Rotate the light**: Slowly sweep Light Angle through all eight positions. Watch how the virtual illumination orbits the subject, revealing different contours at each angle.
3. **Adjust bias**: Sweep Bias from 0% to 100%. At low bias, only highlights are visible against black. At 50% (default), the relief sits on mid-gray. At high bias, only shadows are visible against white.
4. **Raised vs Carved**: Toggle Style. The face alternates between appearing to project outward (Raised) and being pressed into the surface (Carved).
5. **Contrast sculpt**: Increase Contrast above 50% to exaggerate the relief. The subject should look like a coin or medallion.

**Key concepts**: Emboss computes directional gradients, Light Angle selects which edges receive highlights, Bias sets the neutral surface level, Style reverses the relief polarity

---

### Exercise 2: Metallic Color Emboss

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: emboss_source1_kodim02, after: emboss_exercise2_result },
    { label: "Kodim07", before: emboss_source2_kodim07, after: emboss_exercise2_result },
    { label: "Kodim01 B&W", before: emboss_source3_kodim01_bw, after: emboss_exercise2_result },
  ]}
/>
*Metallic Color Emboss — simulated result across source images.*
**Source**: A brightly colored scene — flowers, painted surfaces, or color bars.

**Objective**: Explore Source color mode and Metallic Tint for iridescent surfaces.

1. **Color relief**: Set Color to Source. The embossed relief now carries the original video's hue and saturation — edges are colored rather than monochrome.
2. **Metal surface**: Increase Metal Tint from 0% toward ~60%. Watch the color shift — bright areas and dark areas take on complementary hues, mimicking anodized metal.
3. **Light direction**: Set Light Angle to a diagonal (SE or NW) for the strongest sense of three-dimensionality with colored edges.
4. **Sharpen detail**: Add ~30% Sharpen. Fine textures in the source become more visible in the relief.
5. **Partial mix**: Lower Mix to ~40%. The metallic emboss blends with the original color image, creating a subtle hammered-metal overlay.

**Key concepts**: Source color mode preserves original chroma, Metal Tint creates luminance-dependent hue shifts, partial mix blends emboss with original

---

### Exercise 3: Edge Map Key Source

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: emboss_source1_kodim02, after: emboss_exercise3_result },
    { label: "Kodim07", before: emboss_source2_kodim07, after: emboss_exercise3_result },
    { label: "Kodim01 B&W", before: emboss_source3_kodim01_bw, after: emboss_exercise3_result },
  ]}
/>
*Edge Map Key Source — simulated result across source images.*
**Source**: High-contrast footage — silhouettes, text overlays, or architectural elements with strong edges.

**Objective**: Push Emboss into a high-contrast edge detector suitable as a key or mask source.

1. **Maximum depth**: Set Depth to 100%. Only the strongest gradients in the source should produce visible output.
2. **Maximum contrast**: Set Contrast to 100%. The mid-range values collapse, leaving predominantly black and white.
3. **Set bias to center**: Keep Bias at ~50% to center the edge map around mid-gray before the contrast expansion clips it.
4. **Sharpen for detail**: Add ~60% Sharpen to bring up fine lines.
5. **Invert for polarity**: Toggle Invert to choose whether edges appear as white-on-black or black-on-white.
6. **Gray mode**: Keep Color on Gray for a clean monochrome edge map without chroma artifacts.
7. **Compare directions**: Step through Light Angle positions. Each direction emphasizes different edge orientations — East/West highlight vertical edges, North/South highlight horizontal edges.

**Key concepts**: High Depth + high Contrast converts Emboss into an edge detector, Light Angle selects edge orientation sensitivity, Invert controls edge polarity

---


## Tips

- **Light Angle is the key creative control**: Rotating through the eight positions transforms the character of the emboss. Diagonal angles (SE, NW) produce the strongest sense of three-dimensionality. Cardinal angles (E, S, W, N) emphasize edges aligned perpendicular to the light.
- **Bias sets the canvas**: Think of Bias as the color of the surface the emboss is stamped into. Mid-gray is the classic emboss look. Black bias creates a lithographic plate effect. White bias creates a watermark appearance.
- **Subtle mix for texture overlay**: Setting Mix to 10–30% overlays a gentle relief texture onto the original video without overwhelming the source content — excellent for adding tactile "weight" to flat graphics.
- **Sharpen fills in fine detail**: The base emboss can miss fine textures because the 1-pixel and 1-line gradient kernels are small. Sharpen boosts these fine edges back into visibility within the relief.
- **Contrast as a threshold**: At extreme Contrast settings, the emboss becomes a binary edge map. Route this to another module as a key source for selective processing.
- **Metal Tint for warmth**: Even a small Metal Tint value (10–20%) adds warmth and visual interest to Source color mode, breaking the monotony of a uniform emboss tint.
- **Carved + dark bias = intaglio print**: Setting Style to Carved with Bias below 50% produces the look of a copperplate intaglio engraving — dark lines etched into a dark surface with only the deepest cuts catching light.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bas-Relief** | A sculptural technique where figures project slightly from a flat background, creating the illusion of depth through light and shadow. |
| **Bias** | A DC offset added to a signal to shift its operating point; in Emboss, the neutral surface brightness level. |
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for line delay storage. |
| **Deboss** | The opposite of emboss; pressing a design into a surface rather than raising it above the surface. |
| **Dot Product** | A mathematical operation that projects one vector onto another; used in lighting calculations to determine surface brightness. |
| **Gradient** | The rate of change of a value across space; in image processing, the difference between adjacent pixel values. |
| **Heightfield** | A 2D representation of a 3D surface where pixel brightness represents height above a base plane. |
| **Intaglio** | A printmaking technique where the image is incised into a surface and ink is held in the grooves. |
| **Interpolator** | An FPGA IP block that computes weighted average (crossfade) between two input values based on a control parameter. |
| **Line Buffer** | A BRAM-based memory storing one complete scanline of pixel data, enabling vertical comparisons between adjacent lines. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **Sobel Operator** | A 3×3 convolution kernel used in image processing to compute horizontal and vertical gradient approximations for edge detection. |
| **Surface Normal** | A vector perpendicular to a surface at a given point, used in lighting calculations to determine the angle of incidence. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
