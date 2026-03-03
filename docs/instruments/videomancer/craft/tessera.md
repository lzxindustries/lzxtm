---
draft: true
sidebar_position: 301
slug: /instruments/videomancer/tessera
title: "Tessera"
image: /img/instruments/videomancer/tessera/tessera_hero.png
description: "Byzantine mosaics are among the most enduring art forms in human history."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import tessera_hero from '/img/instruments/videomancer/tessera/tessera_hero.png';
import tessera_control_panel from '/img/instruments/videomancer/tessera/tessera_control_panel.png';
import tessera_exercise1_result from '/img/instruments/videomancer/tessera/tessera_exercise1_result.png';
import tessera_exercise2_result from '/img/instruments/videomancer/tessera/tessera_exercise2_result.png';
import tessera_exercise3_result from '/img/instruments/videomancer/tessera/tessera_exercise3_result.png';
import tessera_source1_kodim03 from '/img/instruments/videomancer/tessera/tessera_source1_kodim03.png';
import tessera_source2_kodim13 from '/img/instruments/videomancer/tessera/tessera_source2_kodim13.png';
import tessera_source3_kodim13_bw from '/img/instruments/videomancer/tessera/tessera_source3_kodim13_bw.png';

# Tessera

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: tessera_source1_kodim03, after: tessera_hero },
    { label: "Kodim13", before: tessera_source2_kodim13, after: tessera_hero },
    { label: "Kodim13 B&W", before: tessera_source3_kodim13_bw, after: tessera_hero },
  ]}
/>
*Tessera quantizing a video frame into Byzantine smalti mosaic with gold-leaf highlights, visible grout lines, and per-tessera scintillation jitter.*

---

## Overview

Byzantine mosaics are among the most enduring art forms in human history. Assembled from thousands of small glass or stone cubes called tesserae, they transform continuous imagery into a discretized field of color that shimmers under changing light. The technique reached its apex in the churches of Ravenna, where gold-leaf glass tesserae were deliberately set at irregular angles so that candlelight would catch each cube differently, producing the characteristic scintillation that makes mosaic walls appear to glow.

Tessera applies this ancient craft to live video. The input frame is divided into a grid of square cells — from 4×4 to 16×16 pixels — and each cell is sample-and-held to a single color value taken from the cell center. That held color is then quantized to the nearest match in a 12-color smalti palette derived from surviving Byzantine churches. Pixels whose luminance exceeds a configurable threshold are replaced with gold tessera, simulating the gold-leaf ground that defines Byzantine sacred art. Visible grout lines are rendered at cell boundaries, and per-tessera luminance jitter — computed by XOR-hashing the cell coordinates — simulates the irregular setting angles that produce real mosaic scintillation.

Four historically inspired palettes are available: Ravenna (golds, blues, vermillion), Hagia Sophia (ultramarines, teals, ambers), Palermo (Sicilian Norman-Byzantine brights), and a Monochrome palette of twelve grays for achromatic compositions. Each palette contains twelve colors tuned in the YUV domain for accurate video reproduction.

---

## Background

### What Are Tesserae?

A tessera (plural: tesserae) is a single cube of material — glass, stone, ceramic, or gold-leaf glass — used to build a mosaic. In Byzantine mosaic work, tesserae are typically 5–15mm per side, set into wet plaster (the *settingbed*) at deliberate angles. The Latin word *tessera* derives from the Greek *τέσσερα* (four), referring to the four sides of the cube. Tessera uses square pixel cells as digital tesserae: each cell holds a single color, just as each physical cube holds a single hue.

### Gold Ground and Sacred Light

The defining feature of Byzantine mosaic is the gold ground — vast expanses of gold-leaf glass tesserae that form the background of sacred figures. These gold cubes were made by sandwiching thin gold foil between layers of glass, then cutting the resulting sheet into small squares. In Tessera, any cell whose sampled luminance exceeds the Gold Threshold is replaced with a fixed gold color (Y=920, U=490, V=550). This creates a luminance-dependent key: bright areas of the source become golden, while darker areas are quantized to the smalti palette.

### Smalti Palette Quantization

Smalti are handmade Venetian glass tesserae, prized for their rich, saturated colors and irregular surfaces. Tessera approximates this by quantizing the sampled cell color to the nearest entry in a 12-color palette using minimum Manhattan distance in YUV space: $d = |Y_\text{cell} - Y_\text{palette}| + |U_\text{cell} - U_\text{palette}| + |V_\text{cell} - V_\text{palette}|$. The palette with the smallest total distance wins. This YUV distance metric weights luminance and chrominance equally, producing a visually balanced quantization.

### Scintillation and Angle Jitter

Real mosaic walls scintillate — individual tesserae catch light differently as the viewer moves or the light source shifts. This effect arises because craftsmen set each cube at a slightly different angle in the plaster bed. Tessera simulates this with a deterministic XOR hash of the cell coordinates that produces a per-tessera signed luminance offset, scaled by the Scintillation knob. The Raking Light toggle doubles the jitter amplitude, simulating the dramatic side-lighting used in conservation photography to reveal the surface texture of ancient mosaics.

### Weathering and Patina

Over centuries, exposed mosaics lose brightness and saturation as grout absorbs moisture, tesserae surfaces dull, and gold leaf oxidizes. Tessera's Age toggle simulates this weathering by reducing luminance to 75% and halving the saturation. The result is a muted, patinated appearance that suggests a mosaic that has survived a thousand years of candle smoke and Mediterranean humidity.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Cell Grid + Sample-and-Hold ───────────────────
│   ├─ Divide frame into cell grid (cell_size: 4/8/12/16 px)
│   ├─ Compute cell_x, cell_y, in_cell_x, in_cell_y
│   ├─ Sample-and-hold: latch input YUV at cell center
│   └─ Grout detect: pixel at cell edge < grout_width
│
├── Stage 2: Gold Ground + Palette Quantization ────────────
│   ├─ If gold enabled AND held_Y > gold_threshold → gold
│   └─ Else: nearest-match in 12-entry smalti palette
│       └─ Distance: |ΔY| + |ΔU| + |ΔV| (Manhattan)
│
├── Stage 3: Scintillation Jitter + Grout Overlay ──────────
│   ├─ XOR hash cell coordinates → 8-bit per-tessera key
│   ├─ Extract signed jitter, scale by Scintillation pot
│   ├─ Raking Light: double jitter amplitude
│   ├─ Apply jitter to Y channel
│   └─ Grout overlay: if is_grout → grout color (Y=180)
│
├── Stage 4: Saturation + Weathering + Border ──────────────
│   ├─ Saturation: scale U,V around midpoint (512)
│   ├─ Weathered: Y × 0.75, saturation × 0.5
│   └─ Border: darken outer 16px to gold-colored frame
│
├── Mix (interpolator_u × 3) ──────────────────────────────
│   └─ Wet/dry crossfade: lerp(dry, wet, mix_amount)
│
└── Bypass Mux ─────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical design choice is that sample-and-hold occurs at stage 1, before palette quantization. Each cell is reduced to a single YUV value sampled at the cell center, and all subsequent stages — gold test, palette matching, jitter, saturation — operate on that single held value. This means the palette quantization only runs once per cell transition rather than per pixel, matching the behavior of a real mosaic where each tessera is a single color. The grout flag is carried through stages 2–3 as a pipeline signal and applied at stage 3, overriding the palette color with the fixed grout constant.

---

## Parameter Reference

<img src={tessera_control_panel} alt="Videomancer front panel with Tessera loaded"/>
*Videomancer's front panel with Tessera active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cell Size
| Property | Value |
|----------|-------|
| Range | 4px – 16px |
| Default | 10px |
| Suffix | px |

Controls the tessera cell dimensions using a steps_4 decode: the pot maps to cell sizes of 4, 8, 12, or 16 pixels per side. At 4 pixels, the mosaic is extremely fine — over 100,000 cells on a 1920×1080 frame — and retains considerable detail. At 16 pixels, the mosaic is coarse with clearly visible individual tesserae, and the image is heavily abstracted to the 12-color palette. Larger cells make the grout lines, scintillation jitter, and gold ground more visually prominent because each tessera occupies more screen area.

---

#### Knob 2 — Gold Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Sets the luminance threshold above which cells are assigned the gold tessera color instead of being palette-quantized. At 0%, essentially no pixels are bright enough to trigger gold — the entire image is quantized to smalti colors. At 100%, only the very brightest highlights become gold. A mid-range setting (around 75%) creates the classic Byzantine composition where gold fills the background sky and haloes while figures and architecture remain in colored smalti. This threshold operates on the sample-and-held cell luminance, so each cell is either entirely gold or entirely smalti.

---

#### Knob 3 — Palette
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 1 |

Selects one of four smalti palettes, each derived from a different Byzantine monument. Ravenna (position 1): rich golds, deep blues, vermillion — the palette of San Vitale. Hagia Sophia (position 2): ultramarines, teals, amber — Istanbul's great dome. Palermo (position 3): bright golds, royal blues, emerald — the Cappella Palatina. Monochrome (position 4): twelve grades of neutral gray for achromatic compositions. The palette affects only the non-gold tesserae; gold color is fixed across all palettes.

---

#### Knob 4 — Grout Width
| Property | Value |
|----------|-------|
| Range | 0px – 3px |
| Default | 1px |
| Suffix | px |

Controls the grout line width between cells using a steps_4 decode: 0, 1, 2, or 3 pixel widths. At 0, tesserae abut seamlessly. At 1 pixel, thin grout lines define the grid without dominating. At 2–3 pixels, the grout becomes a prominent visual element — the warm gray color (Y=180, U=505, V=530) creates a visible lattice that structures the mosaic composition. Grout is rendered by detecting pixels within the grout width of the cell boundary and overriding their color with the grout constant.

---

#### Knob 5 — Scintillation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the amplitude of per-tessera luminance jitter that simulates the scintillation of irregularly set glass cubes. At 0%, all tesserae of the same palette color appear identical. As you increase Scintillation, individual tesserae brighten or darken relative to their neighbors based on their XOR-hashed coordinate signature. The effect simulates candlelight catching each cube at a different angle. At high values, the jitter becomes dramatic — some tesserae appear nearly washed out while adjacent ones are deeply shaded.

---

#### Knob 6 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Scales the saturation of the palette colors around the neutral chroma midpoint (U=512, V=512). At 0%, all tesserae become grayscale — the mosaic loses its color. At 50% (midpoint), the palette colors display at their designed saturation. At 100%, colors are pushed toward full saturation, creating the vivid, almost gaudy chromatic intensity of freshly made smalti before centuries of weathering. This control interacts with the Weathered toggle, which further halves saturation when enabled.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Gold Ground** | On | Off |
| **8 — Raking Light** | Even | Raking |
| **9 — Age** | New | Weathered |
| **10 — Border** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control distinct aspects of the mosaic rendering. Gold Ground is the most visually impactful — it enables or disables the luminance-keyed gold background that defines Byzantine style. Raking Light doubles the scintillation amplitude for dramatic texture. Age simulates centuries of patina. Border adds a decorative frame. Each toggle operates independently, and all combinations are valid.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) signal and the wet (mosaic) signal using three parallel interpolator instances. At 0%, the output is the unprocessed source. At 100%, the output is the fully rendered mosaic. Intermediate values create a translucent overlay where the mosaic pattern ghosts over the source video — an effect that recalls the practice of laying out tesserae on a preparatory cartoon drawing before setting them in plaster.

---

## Guided Exercises

These exercises progress from simple palette quantization to full Byzantine mosaic composition, introducing gold ground, scintillation, and weathering in sequence.

### Exercise 1: Smalti Quantization

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: tessera_source1_kodim03, after: tessera_exercise1_result },
    { label: "Kodim13", before: tessera_source2_kodim13, after: tessera_exercise1_result },
    { label: "Kodim13 B&W", before: tessera_source3_kodim13_bw, after: tessera_exercise1_result },
  ]}
/>
*Smalti Quantization — simulated result across source images.*
**Source**: A camera feed or footage with a range of colors and good tonal variety — faces, flowers, or painted surfaces work well.

**Objective**: Learn how palette quantization reduces continuous video to discrete smalti colors, and how cell size affects detail retention.

1. **Coarse cells**: Set Cell Size to its maximum (16 px). The image breaks into large mosaic tiles, each a single palette color. Watch how the source content is abstracted.
2. **Fine cells**: Reduce Cell Size to minimum (4 px). The mosaic becomes much finer — you can still recognize subjects, but they're composed entirely from 12 colors.
3. **Palette comparison**: Sweep through the four palettes. Note how Ravenna renders warm, Sophia cooler, Palermo brighter, and Monochrome achromatic.
4. **Add grout**: Set Grout Width to 1 pixel. Thin gray lines appear between tesserae, defining the grid structure.
5. **Saturation**: Sweep the Saturation knob. At low values, the palette becomes desaturated; at high values, smalti colors become vivid.

**Key concepts**: Palette quantization maps continuous color to 12 discrete entries by minimum YUV distance, cell size controls detail retention, grout lines define the mosaic grid

---

### Exercise 2: Gold Ground Composition

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: tessera_source1_kodim03, after: tessera_exercise2_result },
    { label: "Kodim13", before: tessera_source2_kodim13, after: tessera_exercise2_result },
    { label: "Kodim13 B&W", before: tessera_source3_kodim13_bw, after: tessera_exercise2_result },
  ]}
/>
*Gold Ground Composition — simulated result across source images.*
**Source**: Footage with strong luminance contrast — a figure against a bright sky, a candle flame, or a spotlight on a dark background.

**Objective**: Explore the gold ground feature and learn how the luminance threshold creates a Byzantine figure-ground separation.

1. **Enable gold**: Toggle Gold Ground to On. Set Gold Threshold to about 75%. Bright areas of the source become gold tesserae; darker areas are quantized to the smalti palette.
2. **Threshold sweep**: Slowly lower the Gold Threshold from 100% toward 0%. Watch as more of the image converts to gold: first just highlights, then mid-tones, then nearly everything.
3. **Find the sweet spot**: Around 60–70%, many sources produce a composition where the background is gold and the foreground subject is rendered in smalti — the classic Byzantine figure-ground arrangement.
4. **Add scintillation**: Increase Scintillation to about 50%. The gold and smalti tesserae begin to shimmer individually.
5. **Add border**: Toggle Border On. A dark gold frame surrounds the mosaic.

**Key concepts**: Gold ground is a luminance key — bright cells become gold, dark cells keep palette colors, threshold position controls the figure-ground boundary

---

### Exercise 3: Ancient Mosaic Restoration

<BeforeAfterSlider
  sources={[
    { label: "Kodim03", before: tessera_source1_kodim03, after: tessera_exercise3_result },
    { label: "Kodim13", before: tessera_source2_kodim13, after: tessera_exercise3_result },
    { label: "Kodim13 B&W", before: tessera_source3_kodim13_bw, after: tessera_exercise3_result },
  ]}
/>
*Ancient Mosaic Restoration — simulated result across source images.*
**Source**: Any footage — architectural details, portraits, or abstract textures.

**Objective**: Combine all features to produce the appearance of a weathered Byzantine mosaic under raking conservation light.

1. **Set the mosaic**: Cell Size 12 px, Grout Width 2 px, Palette Ravenna, Gold Ground On, Gold Threshold ~60%.
2. **Scintillation**: Increase Scintillation to about 70%. Each tessera now has a clearly different brightness.
3. **Raking Light**: Toggle Raking Light to Raking. The jitter amplitude doubles — the mosaic surface becomes dramatically textured.
4. **Weathering**: Toggle Age to Weathered. The entire mosaic dims and desaturates, as if photographed in situ after a millennium.
5. **Border**: Enable Border for the ornamental frame.
6. **Partial mix**: Lower Mix to about 60%. The weathered mosaic overlays ghostly on the source, like a conservation transparency sheet.
7. **Palette swap**: Switch to Hagia Sophia and Palermo palettes to see how different color families affect the composition.

**Key concepts**: Raking Light doubles scintillation jitter, Weathering reduces brightness and saturation to simulate patina, combining features creates a historically informed mosaic simulation

---


## Tips

- **Gold Threshold is the composition tool**: Finding the right threshold splits the image into foreground (smalti) and background (gold) — the fundamental Byzantine visual structure.
- **Scintillation makes it alive**: Even modest scintillation (20–30%) adds the characteristic mosaic shimmer. Without it, the result looks like a flat color quantization.
- **Raking Light for conservation aesthetic**: Double jitter creates the dramatic texture seen in museum photography of ancient mosaics under oblique side-lighting.
- **Weathered + Ravenna = Ravenna in situ**: The combination of the Ravenna palette with Weathered mode closely approximates the current appearance of the mosaics of San Vitale.
- **Cell Size 8 is the sweet spot**: Large enough for visible individual tesserae, small enough to retain recognizable subjects — the scale of real Byzantine mosaic work.
- **Feedback creates recursive mosaic**: Route the output back to the input to create tesserae within tesserae — a mosaic of mosaics, each level further quantized.
- **Mix for overlay study**: At 40–60% mix, the mosaic overlays on the source like a conservation transparency, revealing how the quantization maps to the original content.
- **Try Monochrome for ink wash**: The 12-gray palette with fine cells (4 px) creates a stippled halftone effect reminiscent of ink wash or stone lithography.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory within the FPGA used here for the video line buffer that retains held cell colors across scanlines. |
| **Byzantine** | Relating to the Eastern Roman Empire (330–1453 CE) and its distinctive artistic traditions, especially gold-ground mosaic. |
| **Gold Ground** | The background of gold-leaf glass tesserae that defines Byzantine mosaic composition. |
| **Grout** | The morite or cement filling gaps between tesserae, rendered as dark gray lines between cells. |
| **Interpolator** | A linear interpolation module used for wet/dry crossfade mixing. |
| **Manhattan Distance** | The sum of absolute differences across dimensions: $|ΔY| + |ΔU| + |ΔV|$. Used for palette color matching. |
| **Palette** | A fixed set of colors (12 entries) to which continuous input values are quantized. |
| **Pipeline** | Sequential processing stages executing on consecutive clock cycles. |
| **Raking Light** | Oblique side-lighting used in conservation to reveal surface texture of mosaics and reliefs. |
| **Sample-and-Hold** | A circuit that captures an input value at a specific moment and holds it constant until the next sample. |
| **Scintillation** | The shimmering effect produced by mosaic tesserae set at irregular angles, catching light differently. |
| **Smalti** | Handmade Venetian glass tesserae, prized for rich color and irregular surface texture. |
| **Tessera** | A single cube of glass, stone, or ceramic used to construct a mosaic (plural: tesserae). |
| **Weathering** | Simulated aging that reduces brightness and saturation to approximate centuries of patina. |
| **XOR Hash** | A bitwise exclusive-OR function producing a deterministic per-cell variation key from cell coordinates. |
| **YUV** | Color encoding separating luminance (Y) from chrominance (U, V), used throughout Videomancer. |

---
