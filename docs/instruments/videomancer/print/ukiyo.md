---
draft: true
sidebar_position: 312
slug: /instruments/videomancer/ukiyo
title: "Ukiyo"
image: /img/instruments/videomancer/ukiyo/ukiyo_hero.png
description: "Ukiyo-e — \"pictures of the floating world\" — was the dominant art form of Japan's Edo period (1603–1868)."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import ukiyo_hero from '/img/instruments/videomancer/ukiyo/ukiyo_hero.png';
import ukiyo_control_panel from '/img/instruments/videomancer/ukiyo/ukiyo_control_panel.png';
import ukiyo_exercise1_result from '/img/instruments/videomancer/ukiyo/ukiyo_exercise1_result.png';
import ukiyo_exercise2_result from '/img/instruments/videomancer/ukiyo/ukiyo_exercise2_result.png';
import ukiyo_exercise3_result from '/img/instruments/videomancer/ukiyo/ukiyo_exercise3_result.png';
import ukiyo_source1_kodim02 from '/img/instruments/videomancer/ukiyo/ukiyo_source1_kodim02.png';
import ukiyo_source2_kodim07 from '/img/instruments/videomancer/ukiyo/ukiyo_source2_kodim07.png';
import ukiyo_source3_kodim01_bw from '/img/instruments/videomancer/ukiyo/ukiyo_source3_kodim01_bw.png';

# Ukiyo

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: ukiyo_source1_kodim02, after: ukiyo_hero },
    { label: "Kodim07", before: ukiyo_source2_kodim07, after: ukiyo_hero },
    { label: "Kodim01 B&W", before: ukiyo_source3_kodim01_bw, after: ukiyo_hero },
  ]}
/>
*Ukiyo transforming a live video feed into a woodblock-printed landscape with Edo-period palette mapping, Sobel edge outlines, bokashi gradients, and washi paper grain texture.*

---

## Overview

Ukiyo-e — "pictures of the floating world" — was the dominant art form of Japan's Edo period (1603–1868). Artists like Hokusai and Hiroshige carved intricate relief blocks, inked them with limited palettes of hand-mixed pigments, and pressed them onto handmade washi paper. Each print layered multiple carved blocks in precise registration, building colour through overprinting. Ukiyo takes this centuries-old process and applies it to live video in real time, transforming any camera feed into a moving woodblock print.

The program works by first flattening the input to a limited palette through nearest-colour matching in YUV space, then extracting edges with a 2D Sobel-style detector to create carved outlines. Bokashi — the characteristic ink gradient seen at the edges of Edo prints where colour bleeds softly into the paper — is simulated by blending a positional gradient across the frame. Deliberate chroma mis-registration shifts the U and V channels by different pixel offsets, recreating the imperfect alignment of multiple carved blocks on a hand press. Finally, an LFSR-driven noise field adds the visible fibre texture of washi paper to the luminance channel.

At subtle settings, Ukiyo applies a gentle posterisation with faint outlines that gives video the quality of a hand-tinted photograph. Pushed further, the palette snaps to bold primary colours, thick black outlines dominate, grain roughens the surface, and bokashi gradients sweep colour across the frame — producing imagery that could step directly out of a Meiji-era print shop.

---

## Background

### Woodblock Printing and Colour Separation

Traditional ukiyo-e prints were produced through a multi-block process called nishiki-e ("brocade printing"). The artist first drew a master line drawing (hanshita-e), which a carver transferred to a cherry-wood block and cut in relief. This key block printed the black outlines. Additional blocks were carved for each colour area, typically four to twelve separate blocks per print. The printer inked each block by hand with water-based pigments, laid dampened washi paper over it, and rubbed the back with a flat disc called a baren. Precise registration marks (kento) cut into each block ensured the colours aligned — though slight misregistration was common and is now considered part of the aesthetic charm. Ukiyo's pipeline mirrors this decomposition: edge detection produces the key block, palette matching selects the colour blocks, and the misalignment control deliberately shifts the colour channels as if the carver's kento marks were slightly off.

### Nearest-Colour Matching in YUV Space

Ukiyo maps every pixel to one of eight palette entries using Manhattan distance in YUV space. For each pixel, the program computes the sum of absolute differences |Y − palY| + |U − palU| + |V − palV| against all eight palette entries and selects the entry with the smallest total distance. Manhattan distance is computationally cheaper than Euclidean distance on FPGA fabric — no multiplier or square root is needed, only subtractors and an adder tree — while still producing perceptually reasonable colour matches. The eight-entry palette is sufficient to capture the limited gamut of traditional ukiyo-e pigments: indigo, vermilion, yellow ochre, sumi ink black, and the bare washi paper white.

### Sobel Edge Detection

The Sobel operator estimates the gradient of image intensity at each pixel by convolving the luminance channel with two 3×3 kernels — one for horizontal changes and one for vertical. The result highlights edges where brightness changes rapidly: the boundaries of objects, the contours of shapes, the lines of text. Ukiyo uses a single BRAM line buffer to hold the previous scanline, allowing the vertical gradient to be computed by comparing the current pixel with the pixel directly above. The horizontal gradient comes from comparing adjacent pixels on the current line. These two components are combined into a single edge magnitude that, when thresholded, produces the sharp outlines characteristic of woodblock key blocks.

### Bokashi Ink Gradients

Bokashi is a printing technique where the printer applies ink in a gradient across the block surface, creating a smooth transition from full colour to bare paper within a single impression. In Hokusai's "The Great Wave off Kanagawa," the sky transitions from deep Prussian blue at the top to pale pink near the horizon — this is bokashi. Ukiyo simulates this effect by generating a spatial ramp tied to either the horizontal or vertical position, then blending it with the palette-mapped image. The direction toggle switches between horizontal bokashi (common in landscape prints) and vertical bokashi (used for atmospheric perspective in tall-format prints).

### Washi Paper Texture

Handmade washi paper has a distinctly visible fibre structure — long mulberry fibres create a soft, irregular texture that absorbs ink unevenly. This texture is part of what distinguishes a woodblock print from a machine reproduction. Ukiyo adds a pseudo-random noise field to the luminance channel using a linear-feedback shift register (LFSR), a simple digital circuit that generates a repeating but apparently random sequence of bits. The grain mode toggle switches between fine grain (single-pixel noise) and coarse grain (2×2 pixel blocks), simulating the difference between tightly pressed kozo-fibre washi and rough-textured gampi-fibre paper.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Edge Detection ───────────────────────────────────────────
│   │
│   ├─ 1. Store current scanline in BRAM line buffer
│   ├─ 2. Compute horizontal gradient (pixel[x] − pixel[x−1])
│   ├─ 3. Compute vertical gradient (pixel[x,y] − pixel[x,y−1])
│   └─ 4. Combine |h_grad| + |v_grad| → edge magnitude
│
├── Palette Match ────────────────────────────────────────────
│   │
│   ├─ 5. For each pixel: compute Manhattan distance to all 8 palette entries
│   └─ 6. Select palette entry with minimum distance → flat Y, U, V
│
├── Bokashi Gradient ─────────────────────────────────────────
│   │
│   └─ 7. Blend spatial gradient (horiz or vert) with palette output
│
├── Outline Composite ────────────────────────────────────────
│   │
│   └─ 8. Where edge magnitude > threshold: replace with black
│          (Thin = 1px, Thick = 2px outline width)
│
├── Misalign ─────────────────────────────────────────────────
│   │
│   └─ 9. Shift U and V channels by different pixel offsets
│
├── Paper Grain ──────────────────────────────────────────────
│   │
│   └─ 10. Add LFSR noise to Y channel (Fine = 1px, Coarse = 2×2)
│
├── Mix ──────────────────────────────────────────────────────
│   └─ Interpolator: dry (original) ↔ wet (print effect)
│
└── Bypass ───────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline order matters for Ukiyo's visual authenticity. Edge detection operates on the original unquantised luminance, ensuring smooth gradient boundaries are captured before the palette flattening removes them. The palette match then snaps colours to the limited gamut. Bokashi blends after palette mapping so the gradient interacts with the flat colour fields rather than the original continuous-tone image. Outlines composite on top of the coloured and gradient-blended result, exactly as a key block prints last over the colour impressions. Misalignment shifts the chroma channels after all colour processing, simulating multi-block registration error. Grain is the final texture layer, applied to luminance only, matching how washi fibre texture appears over the top of all ink layers in a physical print.

---

## Parameter Reference

<img src={ukiyo_control_panel} alt="Videomancer front panel with Ukiyo loaded"/>
*Videomancer's front panel with Ukiyo active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Edge Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the sensitivity of the edge detector. At zero, no outlines are produced and the output consists only of flat palette colours. As Edge Detect increases, progressively finer edges emerge — first major object boundaries, then secondary contours, and finally subtle texture variations. At maximum, even gentle gradients produce visible outlines, creating a dense network of carved lines reminiscent of the most detailed ukiyo-e key blocks. The threshold is applied after the Sobel gradient computation, so this control effectively sets the minimum contrast that produces a visible line.

---

#### Knob 2 — Palette Size
| Property | Value |
|----------|-------|
| Range | 4 – 8 |
| Default | 7 |

Selects one of eight colour palettes inspired by historical ukiyo-e pigment combinations. Classic Edo provides sumi black, vermilion, indigo, and ochre — the workhorse colours of Hiroshige's landscapes. Prussian is dominated by the deep synthetic blue imported from Europe that defined Hokusai's late work. Sunset uses warm oranges and pinks evoking twilight over Edo Bay. Jade emphasises greens and teals found in nature prints. Indigo restricts the palette to shades of indigo and white, mimicking early aizuri-e prints. Autumn brings russets, golds, and deep reds. Monochrome reduces to pure black-and-white sumi ink. Sepia warms the monochrome tones with the brown patina of aged prints.

---

#### Knob 3 — Bokashi Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of colour flattening. At low values, the palette matching is gentle — colours remain close to their original hue with subtle quantisation. As Flat Amount increases, the colour snapping becomes more aggressive, producing the bold, uniform colour fields characteristic of multi-block printing. At maximum, every pixel is mapped firmly to its nearest palette entry with no residual original colour, creating large regions of absolutely flat colour separated only by the edge outlines.

---

#### Knob 4 — Misregister
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of the bokashi gradient overlay. At zero, no gradient is applied and the palette colours remain uniform across the frame. As Bokashi increases, a smooth positional ramp blends across the image, modulating the luminance of the palette-matched output. This simulates the inking gradient where the printer varies pressure or ink density across the block surface. At high values, one side of the frame brightens toward bare paper white while the other side deepens toward full ink saturation.

---

#### Knob 5 — Paper Show
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the magnitude of chroma channel misalignment. At zero, U and V channels are perfectly aligned — the colour blocks register precisely. As Misalign increases, U and V shift by progressively larger and different pixel offsets, producing the colour fringing seen in hand-printed woodblocks where each colour block was positioned by eye against the kento registration marks. The effect is most visible at sharp colour boundaries, where a thin fringe of incorrect colour appears at the edge.

---

#### Knob 6 — Outline Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the amount of LFSR noise added to the luminance channel. At zero, the surface is perfectly smooth. As Paper Grain increases, pseudo-random brightness variations appear across the image, simulating the irregular fibre texture of handmade washi paper. The grain is multiplicative against the ink layers, meaning darker areas show less visible grain than lighter areas — matching how ink saturation masks paper texture in real printing.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Classic | Prussian |
| **8 — Bokashi** | Off | On |
| **9 — Edges** | Outline+Fill | Fill Only |
| **10 — Paper Grain** | Smooth | Textured |
| **11 — Bypass** | Off | On |

The five toggles fine-tune the visual texture and registration of the woodblock print effect. Outline Mode and Grain Mode adjust the coarseness of two different texture layers. Bokashi Dir selects the gradient orientation. Registration deliberately introduces the multi-block misalignment that is a hallmark of genuine hand printing. Bypass provides instant A/B comparison with the unprocessed source.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfade between the dry (original) and wet (woodblock print) signals. At 0%, the output is pure unprocessed video. At 100%, the output is the full ukiyo-e effect with edge outlines, palette mapping, bokashi, grain, and misalignment. Intermediate values create a translucent overlay where the original video shows through the printed effect, evoking a partially inked impression where the paper is not fully covered.

---

## Guided Exercises

These exercises progress from basic palette mapping to complex multi-layer print compositions, exploring how each woodblock printing technique contributes to the ukiyo-e aesthetic.

### Exercise 1: First Impression

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: ukiyo_source1_kodim02, after: ukiyo_exercise1_result },
    { label: "Kodim07", before: ukiyo_source2_kodim07, after: ukiyo_exercise1_result },
    { label: "Kodim01 B&W", before: ukiyo_source3_kodim01_bw, after: ukiyo_exercise1_result },
  ]}
/>
*First Impression — simulated result across source images.*
**Source**: A landscape photograph or camera feed with clear foreground and background separation — trees against sky, buildings against horizon, or similar.

**Objective**: Create a basic ukiyo-e colour print with palette mapping and edge outlines, understanding how the key block and colour blocks work together.

1. **Select a palette**: Turn Palette Sel to Classic Edo. The image immediately snaps to the four-colour Edo palette.
2. **Flatten the colours**: Increase Flat Amount to ~75%. Watch the continuous tones resolve into bold, uniform colour fields.
3. **Add the key block**: Increase Edge Detect to ~50%. Black outlines appear at object boundaries, defining the carved lines of the key block.
4. **Adjust outline weight**: Toggle Outline Mode between Thin and Thick. Observe how Thick outlines create a bolder, more graphic look.
5. **Compare palettes**: Slowly rotate Palette Sel through all eight palettes. Each dramatically changes the mood of the same scene.

**Key concepts**: Palette mapping produces flat colour fields, edge detection creates the key block outlines, outline weight changes the line quality, palette choice defines the emotional tone

---

### Exercise 2: Weathered Print

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: ukiyo_source1_kodim02, after: ukiyo_exercise2_result },
    { label: "Kodim07", before: ukiyo_source2_kodim07, after: ukiyo_exercise2_result },
    { label: "Kodim01 B&W", before: ukiyo_source3_kodim01_bw, after: ukiyo_exercise2_result },
  ]}
/>
*Weathered Print — simulated result across source images.*
**Source**: A portrait or figure study with skin tones and clothing detail.

**Objective**: Layer bokashi gradient, paper grain, and registration error to create a print that looks aged and hand-produced.

1. **Start with the base print**: Edge Detect ~40%, Palette Sel Sepia, Flat Amount ~80%.
2. **Add bokashi**: Increase Bokashi to ~50%. Switch Bokashi Dir to Vert — watch how a top-to-bottom luminance gradient sweeps across the flat colours.
3. **Introduce paper texture**: Turn Paper Grain to ~40% with Fine grain mode. The surface acquires a subtle washi fibre texture.
4. **Switch to Coarse grain**: Toggle Grain Mode to Coarse. The texture becomes rougher and more pronounced — an older, cheaper paper stock.
5. **Misalign the blocks**: Enable Registration toggle, then increase Misalign to ~30%. Watch the chroma channels shift — colour fringing appears at edges where the carved blocks did not quite line up.

**Key concepts**: Bokashi controls ink gradient direction and intensity, paper grain simulates washi texture, registration error adds authenticity through deliberate imperfection

---

### Exercise 3: Prussian Wave

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: ukiyo_source1_kodim02, after: ukiyo_exercise3_result },
    { label: "Kodim07", before: ukiyo_source2_kodim07, after: ukiyo_exercise3_result },
    { label: "Kodim01 B&W", before: ukiyo_source3_kodim01_bw, after: ukiyo_exercise3_result },
  ]}
/>
*Prussian Wave — simulated result across source images.*
**Source**: A high-contrast scene with strong lines — ocean waves, mountain ridges, architectural details, or flowing fabric.

**Objective**: Create a bold, Hokusai-inspired composition emphasising the dramatic interplay of Prussian blue palette, heavy outlines, and bokashi atmospheric gradients.

1. **Set the palette**: Select Prussian. The frame floods with deep indigo and complementary tones.
2. **Maximise flattening**: Push Flat Amount to ~90%. Colours snap to bold, poster-like fields.
3. **Heavy key block**: Edge Detect at ~70%, Outline Mode to Thick. Dense black outlines carve through the composition.
4. **Atmospheric bokashi**: Set Bokashi to ~60%, direction Vert. The upper frame lightens toward a pale sky while the lower deepens.
5. **Subtle misalignment**: Registration On, Misalign at ~15%. Just enough to suggest hand printing.
6. **Light grain**: Paper Grain at ~20%, Fine mode. A gentle washi texture unifies the surface.
7. **Final mix**: With Mix at 100%, toggle Bypass to compare the original source against the full woodblock composition.

**Key concepts**: Prussian blue defines the Hokusai era, heavy edge detect with thick outlines creates bold graphic structure, vertical bokashi simulates atmospheric perspective, subtle misalignment adds credibility

---


## Tips

- **Start with Monochrome palette**: Removing colour lets you focus on the edge detect and grain interaction. Once the line quality is right, switch palettes to add colour.
- **Registration error sells the effect**: Even a small Misalign value (10–20%) adds immense authenticity. Real woodblock prints almost always have slight registration errors — perfect alignment looks artificial.
- **Bokashi direction follows composition**: Use Vert for landscapes (sky-to-ground gradation) and Horiz for portraits or architectural shots (side lighting).
- **Thick outlines at low resolution**: If your source is low-resolution or the output will be viewed at a distance, use Thick outlines — they read better than thin lines at small sizes.
- **Layer grain last mentally**: Paper grain sits on top of everything visually. When designing your print, set grain to zero first, dial in palette and edges, then add grain as the final textural polish.
- **Feedback loops create moire prints**: Routing the output back through Ukiyo creates recursive quantisation — the palette snaps to itself through successive passes, eventually converging to a fixed-point image with increasingly graphic edge patterns.
- **Flat Amount is your tonal control**: Beyond palette selection, Flat Amount is the most important control. Low values create watercolour-like soft prints; high values produce bold graphic posters.
- **Combine with external processing**: Ukiyo pairs beautifully with upstream blur or defocus effects — pre-softening the input reduces spurious edge detection and produces cleaner, more intentional outlines.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bokashi** | A Japanese printing technique where ink is applied in a gradient across the block surface, creating smooth transitions from full colour to bare paper. |
| **BRAM** | Block RAM; dedicated FPGA memory used for the scanline buffer enabling 2D edge detection. |
| **Kento** | Registration marks carved into each woodblock to ensure precise alignment when printing multiple colour layers. |
| **LFSR** | Linear-Feedback Shift Register; a simple digital circuit generating pseudo-random bit sequences, used here for paper grain texture. |
| **Manhattan Distance** | The sum of absolute differences across dimensions (|Y₁ − Y₂| + |U₁ − U₂| + |V₁ − V₂|), cheaper than Euclidean distance on FPGA fabric. |
| **Nishiki-e** | "Brocade printing"; the multi-block colour woodblock technique that defined ukiyo-e's visual richness. |
| **Palette Quantisation** | The process of mapping continuous-tone colour values to a fixed set of discrete colours. |
| **Sobel Operator** | A discrete differentiation operator computing horizontal and vertical intensity gradients from a 3×3 pixel neighbourhood. |
| **Ukiyo-e** | "Pictures of the floating world"; Japanese woodblock prints and paintings produced between the 17th and 19th centuries. |
| **Washi** | Traditional Japanese paper made from plant fibres (kozo, gampi, mitsumata), characterised by visible fibre texture and high durability. |
| **YUV** | A colour encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
