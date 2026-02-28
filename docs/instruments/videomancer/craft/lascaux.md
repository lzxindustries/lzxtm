---
draft: true
sidebar_position: 142
slug: /instruments/videomancer/lascaux
title: "Lascaux"
image: /img/instruments/videomancer/lascaux/lascaux_hero.png
---

import lascaux_before_after from '/img/instruments/videomancer/lascaux/lascaux_before_after.png';
import lascaux_control_panel from '/img/instruments/videomancer/lascaux/lascaux_control_panel.png';
import lascaux_exercise1_result from '/img/instruments/videomancer/lascaux/lascaux_exercise1_result.png';
import lascaux_exercise2_result from '/img/instruments/videomancer/lascaux/lascaux_exercise2_result.png';
import lascaux_exercise3_result from '/img/instruments/videomancer/lascaux/lascaux_exercise3_result.png';
import lascaux_hero from '/img/instruments/videomancer/lascaux/lascaux_hero.png';
import lascaux_source1_kodim03 from '/img/instruments/videomancer/lascaux/lascaux_source1_kodim03.png';
import lascaux_source2_kodim13 from '/img/instruments/videomancer/lascaux/lascaux_source2_kodim13.png';
import lascaux_source3_kodim13_bw from '/img/instruments/videomancer/lascaux/lascaux_source3_kodim13_bw.png';

# Lascaux

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={lascaux_hero} alt="Lascaux hero image"/>
*Lascaux transforming a video portrait into earth-tone cave pigments illuminated by a flickering torch drifting across rough stone.*
<img src={lascaux_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Lascaux applied.*

---

## Overview

Thirty-two thousand years ago, artists crouched in the darkness of limestone caves and painted animals, handprints, and abstract symbols onto rough stone walls using nothing but mineral pigments and firelight. The results — preserved at Lascaux, Altamira, and Chauvet — remain among the most powerful images ever created. Lascaux recreates this primal visual world by processing modern video through a four-stage pipeline that mimics the materials and conditions of Paleolithic cave art.

First, the input video is reduced to a palette of two, three, or four earth-tone pigments — charcoal black, yellow ochre, red ochre, and raw sienna — derived from spectroscopic analysis of actual Lascaux paint samples. Second, charcoal contour lines are extracted from the edges of the palettized image using horizontal and vertical gradient detection, darkening the boundaries between color regions the way a cave artist would outline a figure with a charcoal stick. Third, stone surface grain is applied via LFSR noise, adding the rough texture of limestone or basalt walls. Finally, a virtual torch illuminates a circular region of the frame with radial falloff, leaving the rest of the image in cave darkness. The torch drifts slowly across the frame on a Lissajous-like path, its brightness flickering with the organic randomness of a fat lamp or pine resin flame.

The program is named after the Lascaux cave complex in the Dordogne region of southwestern France, discovered in 1940 by four teenagers and their dog. The cave contains over 600 paintings and 1,500 engravings dating to approximately 17,000 BCE, including the famous Hall of the Bulls — one of the most celebrated works of prehistoric art.

---

## Background

### Paleolithic Pigments and Color Science

The cave painters of Lascaux had access to a remarkably limited palette: manganese dioxide and lamp black for dark tones, iron oxide minerals (goethite, haematite, limonite) for yellows, reds, and browns, and occasionally kaolin clay for white. Spectroscopic analysis of paint samples from Lascaux has identified these as the primary constituents. Lascaux's four-entry palette is modeled directly on these minerals: charcoal (Y=80, neutral chroma) represents manganese dioxide, yellow ochre (Y=620, warm amber) represents goethite, red ochre (Y=380, red-orange) represents haematite, and raw sienna (Y=520, earth brown) represents mixed iron oxides. The palette quantizer uses Manhattan distance in YUV space to classify each input pixel to the nearest pigment.

### Contour Extraction and Charcoal Outlines

The cave artists at Lascaux frequently outlined their figures with charcoal sticks before filling areas with pigment — a technique visible in the engraved and drawn outlines that underlie many of the painted animals. Lascaux simulates this by computing the gradient magnitude at each pixel: the absolute difference between adjacent pixels horizontally (from a one-pixel delay) and vertically (from a one-line BRAM delay buffer). The sum of these gradients, scaled by the Contour Weight parameter, is subtracted from the palettized luminance to darken edge regions. In Edges Only mode, the program shows just the contour lines against a plain stone-colored background — a pure charcoal drawing without pigment fill.

### LFSR Noise and Stone Texture

Real cave walls are not smooth — they are rough, pitted, and irregularly textured. Lascaux adds stone surface grain using a 16-bit linear feedback shift register (LFSR) as a pseudorandom noise source. The LFSR output is converted to a signed offset and scaled by the Stone Grain parameter before being added to the luminance channel. Because the LFSR runs freely at pixel rate (one shift per clock), the noise pattern is different on every pixel and every frame, simulating the granular irregularity of natural stone. The noise interacts with the palette quantization: since the palette has already reduced the image to a few discrete colors, the grain appears as a speckled texture within each pigment region rather than as smooth film grain.

### Torch Lighting and Firelight Physics

Before electric lights, the only way to see cave paintings was by the light of animal-fat lamps or pine resin torches — small, flickering point sources that illuminated a limited area while leaving the rest of the cave in total darkness. Lascaux simulates this with a radial falloff function centered on a moving torch position. The torch brightness decreases linearly with Manhattan distance from the center, reaching a minimum ambient level (Y≈30) at the torch radius boundary. The torch position drifts on a Lissajous-like path using cosine and sine lookup tables driven by DDS phase accumulators, creating smooth organic wandering. Flicker is applied per-frame using the LFSR to modulate the overall torch intensity, simulating the guttering of a real flame. The torch also desaturates the chroma channels in shadow — colors fade to neutral in the darkness, matching how firelight suppresses color perception at low intensities.

### Cave Wall Materials

Lascaux offers two cave wall types: Limestone (warm yellowish, matching the Dordogne cave walls where the real Lascaux is located) and Basalt (cool gray, matching volcanic cave systems like those in the Auvergne region or Iceland). The selection affects the chroma tint applied in the stone grain stage — the U/V channels are blended toward the wall color constants, shifting the overall color temperature of the scene. Limestone mode produces the warm, amber-lit atmosphere of the real Lascaux cave; Basalt mode produces a cooler, more austere environment.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Clock 1: Palette Quantization ──────────────────────────────
│   ├─ Manhattan distance in YUV space to each pigment
│   ├─ Select nearest of 2/3/4 pigments (controlled by Pigments)
│   ├─ Output: palettized Y, U, V
│   └─ Store original Y for edge detection
│
├── Clock 2: Contour Extraction ────────────────────────────────
│   ├─ Horizontal gradient: |Y(x) − Y(x−1)|
│   ├─ Vertical gradient:   |Y(x,line) − Y(x,line−1)|  (BRAM)
│   ├─ Edge magnitude = (gx + gy) × Contour Wt >> 10
│   ├─ Normal mode: palette_Y − edge_scaled  (darken edges)
│   └─ Edges Only:  edge > 40 → charcoal, else → stone color
│
├── Clock 3: Stone Surface Grain ───────────────────────────────
│   ├─ LFSR noise → signed offset (−128 .. +127)
│   ├─ noise × Stone Grain >> 8  → scaled grain
│   ├─ Y += grain  (clamp 0–1023)
│   └─ U/V blended 75/25 toward cave wall color
│
├── Clock 4: Torch Lighting ────────────────────────────────────
│   ├─ Manhattan distance from torch center
│   ├─ Radial falloff: light = (radius − dist) × 1023 >> 10
│   ├─ Below threshold: ambient darkness (Y≈30)
│   ├─ Apply flicker: light × flicker_val >> 8
│   ├─ Y = grain_Y × light >> 10
│   └─ U/V desaturated toward 512 by light level
│
├── Clocks 5–8: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(dry, wet, Mix)  ×3 channels  (4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-stage delay pipeline (hsync, vsync, field)
│
├── Torch Position (per-frame update at vsync) ─────────────────
│   ├─ DDS phase accumulators × Torch Speed
│   ├─ Cosine/Sine LUT → X/Y position
│   ├─ Torch Lock: override to center (960, 540)
│   └─ Flicker: LFSR × Flicker Depth → per-frame intensity
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The four processing stages (palette → contour → grain → torch) execute sequentially in a single monolithic process, each stage reading the previous stage's registered outputs. The line buffer for vertical edge detection is a 2048×10-bit BRAM tile — the only memory resource the program consumes. The torch position and flicker updates happen once per frame at vsync, so the torch motion is smooth at the video frame rate but does not vary within a single frame. The LFSR that drives both stone grain and torch flicker is a single 16-bit register running at pixel rate, meaning the grain pattern changes every pixel while the flicker value is sampled once per frame from whatever LFSR state happens to coincide with the vsync edge.

---

## Parameter Reference

<img src={lascaux_control_panel} alt="Videomancer front panel with Lascaux loaded"/>
*Videomancer's front panel with Lascaux active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Torch Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the speed of the torch drift when Torch Lock is set to Drift mode. The register value feeds the DDS phase accumulator increment — higher values make the torch traverse its Lissajous path more quickly, while lower values produce a slow, contemplative wander. At zero, the torch position freezes at its current location in the drift cycle. The X and Y phase accumulators use different multipliers (full speed and half speed), so the torch traces an asymmetric figure-eight-like path rather than a simple circle. This control has no effect when Torch Lock is set to Center.

---

#### Knob 2 — Pigments
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 2 |

Selects how many pigments are available to the palette quantizer. The steps_4 control mode divides the 10-bit range into three zones: below 256 selects 2 pigments (charcoal and yellow ochre), 256–511 selects 3 pigments (adding red ochre), and 512 and above selects all 4 pigments (adding raw sienna). Fewer pigments create a more austere, charcoal-and-ochre palette reminiscent of older cave art; more pigments produce a richer, polychrome result like the painted ceilings of Altamira. At 2 pigments, the image reduces to a stark binary of dark and light earth tones.

---

#### Knob 3 — Contour Wt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the darkness of the charcoal contour outlines. The edge magnitude (sum of horizontal and vertical gradients) is multiplied by this value and shifted right by 10, then subtracted from the palettized luminance. At zero, no contour darkening is applied — the palette output passes through cleanly. At maximum, even gentle gradients produce strong dark outlines, and the image takes on a heavily drawn, engraved quality. In Edges Only mode, this control scales the threshold sensitivity for what qualifies as an edge — higher values cause more of the image to register as contour.

---

#### Knob 4 — Torch Radius
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the radius of the torch illumination circle. The register value is scaled to a pixel range of 64 to 960 — from a tight spotlight that reveals only a small patch of cave wall to a wide flood that illuminates most of the frame. The falloff within the illuminated circle is linear with Manhattan distance from the torch center, so the light is brightest at the center and fades steadily toward the edge. Beyond the radius, only a minimal ambient glow (Y≈30) remains, simulating the deep darkness of an unlit cave.

---

#### Knob 5 — Stone Grain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the intensity of the stone surface grain noise. The LFSR noise output (signed, ±128) is multiplied by this value and divided by 256, then added to the luminance. At zero, the stone surface is smooth — only the palette colors and contour lines are visible. At moderate values, a subtle speckled texture appears within each pigment region, imitating the natural roughness of limestone. At high values, the noise becomes aggressive and begins to break up the palette colors themselves, producing a heavily weathered, eroded appearance.

---

#### Knob 6 — Flicker
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the depth of the torch flicker effect. The LFSR provides a random 8-bit value each frame, which is scaled by this parameter and added to a base intensity of 192. At zero, the torch burns with a steady, unwavering brightness — useful for analytical viewing. At moderate values, a gentle organic flicker animates the torch, simulating the natural guttering of a fat lamp. At maximum, the flicker is dramatic and intense — the torch seems to be buffeted by cave drafts, rapidly alternating between bright flare-ups and near-darkness.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Cave Type** | Limestone | Basalt |
| **8 — Torch Color** | Fat Lamp | Pine Resin |
| **9 — Edges Only** | Off | On |
| **10 — Torch Lock** | Drift | Center |
| **11 — Bypass** | Off | On |

Five toggles provide binary mode selections. Cave Type selects the wall material (warm limestone vs. cool basalt). Torch Color is wired to a register but not referenced in the pipeline — it has no visible effect. Edges Only replaces the full painted output with a pure contour-line drawing. Torch Lock pins the torch to center or allows free drift. Bypass routes the input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Standard wet/dry crossfade between the delayed input (dry) and the processed cave-painting output (wet). At 0%, the output is pure passthrough of the original video. At 100%, the output is the fully processed cave painting with torch lighting. Intermediate values blend the two, which can produce an ethereal effect of cave pigments ghosting over modern video — as if the ancient paintings were emerging from the surface of the footage.

---

## Guided Exercises

These exercises progress from minimal palette restriction through full cave-painting immersion, exploring how the four pipeline stages interact to evoke Paleolithic art.

### Exercise 1: Earth-Tone Palette

<img src={lascaux_exercise1_result} alt="Earth-Tone Palette result"/>
*Earth-Tone Palette — simulated result across source images.*
**Source**: A portrait or landscape with a range of skin tones, foliage, and sky — material with varied hue and luminance.

**Objective**: Explore how the palette quantizer reduces modern video to Paleolithic pigments, and how the pigment count changes the character of the image.

1. **Disable torch and grain**: Set Torch Radius to 100% and Flicker to 0% for uniform lighting. Set Stone Grain to 0%, Contour Wt to 0%.
2. **Full palette**: Set Pigments to maximum (~100%, all 4 pigments). The image reduces to four earth tones. Notice how faces become patches of ochre and sienna.
3. **Reduce pigments**: Sweep Pigments downward. At 3 pigments, sienna disappears. At 2 pigments, the image reduces to a stark charcoal-and-ochre duotone.
4. **Add contour**: Slowly increase Contour Wt. Charcoal outlines emerge at the boundaries between pigment regions, giving the image a drawn quality.
5. **Edges Only**: Toggle Edges Only On. The pigment fill vanishes — only the charcoal contour lines remain on a stone-colored background. Compare Limestone vs. Basalt cave types.

**Key concepts**: Manhattan distance palette quantization in YUV, fewer pigments create starker images, contour extraction darkens palette edges, Edges Only isolates the line drawing

---

### Exercise 2: Stone Surface and Torch

<img src={lascaux_exercise2_result} alt="Stone Surface and Torch result"/>
*Stone Surface and Torch — simulated result across source images.*
**Source**: Same portrait or landscape from Exercise 1.

**Objective**: Add stone texture and torch lighting to complete the cave-painting simulation.

1. **Start from Exercise 1**: Pigments ~100%, Contour Wt ~40%, uniform lighting.
2. **Stone Grain**: Increase Stone Grain to ~40%. A speckled texture appears within each pigment region, breaking the flat color into rough stone.
3. **Torch Radius**: Set Torch Radius to ~50%. A circular illumination pool appears, with the surrounding area falling to near-black.
4. **Torch Lock**: Set Torch Lock to Drift and increase Torch Speed to ~30%. The torch begins wandering across the frame, sequentially illuminating different parts of the painting.
5. **Flicker**: Increase Flicker to ~40%. The torch brightness begins to pulse and gutter organically, simulating a real flame in a cave draft.
6. **Cave Type**: Toggle between Limestone and Basalt. Notice how the color temperature of the entire scene shifts — warm amber vs. cool gray.

**Key concepts**: LFSR grain adds per-pixel noise within pigment regions, torch uses radial Manhattan-distance falloff, flicker is per-frame LFSR-driven, cave type shifts the chroma blend target

---

### Exercise 3: Charcoal Study

<img src={lascaux_exercise3_result} alt="Charcoal Study result"/>
*Charcoal Study — simulated result across source images.*
**Source**: High-contrast footage — strong directional lighting, clear silhouettes, or figure-ground separation.

**Objective**: Use Edges Only mode with stone grain and torch lighting to create an animated charcoal drawing on stone.

1. **Edges Only**: Toggle Edges Only On. The image reduces to charcoal contour lines on stone.
2. **Contour Wt**: Sweep Contour Wt through its range. Low values produce only the strongest edges. High values fill in finer detail, producing a denser drawing.
3. **Stone Grain**: Increase Stone Grain to ~50%. The background stone acquires a gritty, pitted texture.
4. **Torch**: Set Torch Radius ~40%, Torch Lock to Drift, Torch Speed ~25%. The charcoal drawing is revealed section by section as the torch wanders past.
5. **Flicker**: Add Flicker at ~50%. The flickering torchlight makes the charcoal lines seem to dance and shift — exactly the experience of viewing a Chauvet cave engraving by firelight.
6. **Cave Type**: Switch to Basalt for a cooler, more austere background. Notice how the contour lines stand out more sharply against the neutral gray.

**Key concepts**: Edges Only isolates contour extraction as a standalone effect, high-contrast source material produces the strongest edges, torch + flicker animate the line drawing like real firelight

---


## Tips

- **Torch Color is a stub**: The Fat Lamp / Pine Resin toggle is wired but unused. Don't waste time tweaking it — it has no visible effect.
- **Start with uniform lighting**: Set Torch Radius to 100%, Flicker to 0%, Torch Lock to Center to see the palette and contour stages clearly before adding torch effects.
- **2-pigment mode for maximum drama**: Reducing to 2 pigments (charcoal + ochre) creates the most prehistoric-looking result — stark, high-contrast, and unmistakably ancient.
- **Stone Grain interacts with palette quantization**: Since the palette has already reduced colors to a few discrete values, grain appears as speckle *within* each color region rather than as smooth noise — this is what makes it look like stone texture rather than film grain.
- **Torch drift speed vs. radius**: Large radius + slow speed = gentle, contemplative exploration. Small radius + fast speed = dramatic, flickering searchlight effect. Match the drift speed to the content's emotional tone.
- **Edges Only for overlay compositing**: Use Edges Only mode with the Mix fader at 50–70% to overlay charcoal contours on the original video — a subtle "pencil sketch" effect without the full cave-painting treatment.
- **Feedback creates cave echo**: Routing Lascaux's output back to its input compounds the palette quantization and contour extraction, progressively reducing the image to fewer, bolder strokes — like successive generations of cave artists painting over each other's work.
- **Basalt for monochrome subjects**: Cool gray basalt walls look best with already-desaturated source material. Limestone's warm amber enhances the earth-tone pigments when working with colorful sources.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory within the FPGA fabric, used here for the one-scanline vertical edge detection buffer. |
| **Contour extraction** | Detection of edges in an image by computing gradient magnitudes between adjacent pixels, used to simulate charcoal outlines. |
| **DDS** | Direct Digital Synthesis; a technique using phase accumulators to generate periodic waveforms, used here to animate the torch position along a Lissajous path. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that implements the video processing pipeline in hardware. |
| **Goethite** | An iron oxyhydroxide mineral (FeOOH) that produces yellow-ochre pigment, one of the primary colorants used at Lascaux. |
| **Haematite** | An iron oxide mineral (Fe₂O₃) that produces red-ochre pigment, widely used in Paleolithic cave art. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used here for both stone surface grain and torch flicker. |
| **Lissajous figure** | A parametric curve traced when two perpendicular sinusoidal oscillations are combined, used to describe the torch drift path. |
| **Manhattan distance** | The sum of absolute differences along each axis, used as a computationally cheap alternative to Euclidean distance for palette matching and torch falloff. |
| **Palette quantization** | Reducing a continuous-color image to a limited set of discrete colors by mapping each pixel to the nearest palette entry. |
| **Proc amp** | Processing amplifier; a gain-and-offset stage for video signals. |
| **YUV** | A color space separating luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |
