---
draft: true
sidebar_position: 307
slug: /instruments/videomancer/vitrage
title: "Vitrage"
image: /img/instruments/videomancer/vitrage/vitrage_hero.png
description: "Stained glass is an exercise in constraint — lead strips force the artist to work in discrete regions of flat color, while the glass itself filters and saturates light passing through it."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import vitrage_hero from '/img/instruments/videomancer/vitrage/vitrage_hero.png';
import vitrage_control_panel from '/img/instruments/videomancer/vitrage/vitrage_control_panel.png';
import vitrage_exercise1_result from '/img/instruments/videomancer/vitrage/vitrage_exercise1_result.png';
import vitrage_exercise2_result from '/img/instruments/videomancer/vitrage/vitrage_exercise2_result.png';
import vitrage_exercise3_result from '/img/instruments/videomancer/vitrage/vitrage_exercise3_result.png';
import vitrage_source1_kodim02 from '/img/instruments/videomancer/vitrage/vitrage_source1_kodim02.png';
import vitrage_source2_kodim07 from '/img/instruments/videomancer/vitrage/vitrage_source2_kodim07.png';
import vitrage_source3_kodim01_bw from '/img/instruments/videomancer/vitrage/vitrage_source3_kodim01_bw.png';

# Vitrage

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: vitrage_source1_kodim02, after: vitrage_hero },
    { label: "Kodim07", before: vitrage_source2_kodim07, after: vitrage_hero },
    { label: "Kodim01 B&W", before: vitrage_source3_kodim01_bw, after: vitrage_hero },
  ]}
/>
*Vitrage transforming video into luminous stained glass panels with dark lead came borders, color-flattened panes, and simulated sunlight transmission.*

---

## Overview

Stained glass is an exercise in constraint — lead strips force the artist to work in discrete regions of flat color, while the glass itself filters and saturates light passing through it. Vitrage applies this principle to moving video, dividing the image into cell-shaped panes bounded by visible dark "came" borders, flattening and saturating the color within each pane, and adding a brightness gradient that simulates light transmission through glass.

The name *vitrage* comes from the French *vitrail* / *vitrage*, meaning stained glass or glazing. In practice the program chains six processing stages: edge detection on the luma channel identifies cell boundaries, intra-cell color is quantized and flattened, saturation is boosted to emulate vivid glass pigments, dark came borders are composited over boundary pixels, and a radial brightness gradient simulates sunlight illuminating the pane centres. Four glass-type presets — Clear, Tint, Opal, and Antique — modify the color treatment within each cell to approximate different historical glass-making techniques.

At subtle settings Vitrage adds a gentle faceted quality to the image, like looking through a beveled window. At extreme settings the video collapses into bold stained-glass panels — flat blocks of vivid colour separated by prominent dark leading, with a warm glow at each cell centre.

---

## Background

### The Art of Stained Glass

Stained glass windows have been used in architecture since at least the 7th century, reaching their artistic peak in the Gothic cathedrals of the 12th and 13th centuries. The technique involves cutting pieces of colored glass to shape and joining them with strips of lead called *came* (from the Latin *calamus*, meaning reed). The lead strips serve both structural and aesthetic purposes: they hold the glass in place while also providing the dark outlines that define each region of color. Vitrage replicates this structure digitally — the edge detector finds natural contours in the image and draws came lines along them, while the intra-cell processor flattens color to simulate the uniform tint of a single piece of glass.

### Edge Detection and Cell Boundaries

Vitrage uses a horizontal gradient detector to identify edges in the luma channel. The program reads the current pixel's Y value and compares it against a delayed version from a video line buffer, computing the absolute difference. When this difference exceeds the Edge Threshold, the pixel is classified as a cell boundary. The line buffer provides a one-line-delayed copy of the luma signal, so the comparison is effectively between pixels separated by one or more scan lines — the exact cell spacing depends on the Came Width parameter. This approach creates rectangular or quasi-hexagonal cell boundaries that follow the natural contours of the source image rather than imposing a rigid grid.

### Color Quantization and Flattening

Real stained glass panes contain a single uniform color — the glass is either red or blue or amber, not a gradient. Vitrage emulates this by quantizing the Y channel within each cell region. The Flat Amount control determines how aggressively the color is flattened: at low settings, intra-cell gradients are preserved; at high settings the luma is posterized into a small number of discrete levels, creating the flat, uniform look of real glass. The quantization uses bit-shift truncation for efficiency, producing 2 to 64 discrete luma levels depending on the control position.

### Saturation and Light Transmission

Colored glass saturates light passing through it — removing certain wavelengths and intensifying others. Vitrage emulates this by stretching the U and V chroma channels away from the neutral midpoint, boosting saturation proportionally to the Saturate control. The Sunlight control adds a brightness gradient that peaks at each cell centre and falls off toward the edges, simulating the way a backlit window appears brightest in the middle of each pane. Together, these two effects create the luminous, jewel-like quality associated with cathedral windows.

### Historical Glass Types

The Glass Type toggle selects one of four color-treatment presets inspired by glass-making traditions. **Clear** glass applies minimal color modification — the source palette is preserved with only the structural effects (came, flattening, light gradient). **Tint** glass shifts the intra-cell color toward the Came Tint hue, emulating sheets of uniformly tinted glass. **Opal** glass reduces contrast and pushes colors toward white, simulating the milky translucence of opalescent art glass. **Antique** glass adds per-pixel noise and slight irregularity, replicating the bubbles and striations found in mouth-blown antique glass.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Line Buffer Read      (sample-hold Y for cell reference)
│   ├─ 2. Edge Detection         (horizontal gradient → boundary flag)
│   ├─ 3. Flatten / Quantize     (reduce Y to discrete levels)
│   ├─ 4. Sunlight Gradient      (brighten toward cell centre)
│   ├─ 5. Came Overlay           (darken boundary pixels)
│   └─ 6. Invert                 (optional luminance inversion)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Saturation Boost       (stretch from midpoint)
│   ├─ 2. Glass Type Modifier    (Clear / Tint / Opal / Antiq)
│   └─ 3. Came Overlay           (desaturate at boundaries if opaque)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ Interpolator × 3          (wet/dry crossfade per channel)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 10-clock delay pipeline   (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline's most critical interaction is between the edge detector and the flattening stage. The line buffer captures the Y value at the start of each cell region; the flattening quantizer then reduces all pixels within that cell to a small set of levels derived from that captured reference. This means the flattening follows the same cell boundaries defined by the edge detector — the two stages are tightly coupled through the line buffer addressing.

The sunlight gradient computation runs in parallel with quantization. A Manhattan distance metric measures each pixel's distance from the cell centre, and the Sunlight pot controls the gradient's intensity. The gradient is added to the quantized Y value, so flattened cells still show the characteristic central brightness peak of backlit glass. The came overlay happens last in the Y path, darkening boundary pixels by a factor controlled by the Edge Threshold pot — this ensures that came lines are always drawn on top of the fully processed cell interior.

---

## Parameter Reference

<img src={vitrage_control_panel} alt="Videomancer front panel with Vitrage loaded"/>
*Videomancer's front panel with Vitrage active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Came Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the width of the lead came strips between glass panes. At low settings the came lines are thin hairlines that merely outline the cell boundaries. As the control increases, the dark lead borders grow wider, consuming more of the image and leaving smaller visible glass regions. Very wide came settings create a bold graphic look where the dark grid dominates and only narrow slivers of color show through. The effective cell size is determined jointly by this control and the Edge Threshold — wider came combined with a sensitive threshold produces dense, small cells.

---

#### Knob 2 — Flat Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how aggressively the source color is flattened within each glass pane. At 0% the intra-cell gradient is fully preserved — you see the source image through a tinted overlay. At 100% the Y channel is quantized to just a few discrete levels, producing the flat, uniform color fields characteristic of real stained glass. Intermediate settings create a painterly effect where large-scale tonal structure is visible but fine detail is suppressed. This control interacts strongly with the Sunlight gradient: even at full flattening, the light gradient re-introduces a smooth brightness variation within each cell.

---

#### Knob 3 — Saturate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Boosts the saturation of the U and V chroma channels by stretching them away from the neutral midpoint (512 in 10-bit). At 0% the image retains its original saturation. At moderate settings, colors become more vivid — greens deepen, reds intensify, blues become richer. At extreme settings, saturation blows out into full-intensity color blocks. The saturation boost operates on the chroma channels independently of the Y-channel flattening, so you can have flat luma with vivid chroma (classic stained glass) or smooth luma with extreme chroma (psychedelic glass).

---

#### Knob 4 — Sunlight
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the intensity of the simulated sunlight gradient within each glass pane. At 0% the cell interior has uniform brightness (after quantization). As you increase the control, pixels near the centre of each cell are brightened while pixels near the edges remain at their quantized level. This creates the illusion of light streaming through the glass — each pane appears to glow from within. At extreme settings the gradient dominates and each cell becomes a bright disc surrounded by a dim border, regardless of the source content.

---

#### Knob 5 — Edge Thr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the sensitivity of the edge detector that identifies cell boundaries. At low settings, only the strongest edges in the source image trigger came lines — large, well-defined contours in the video. At high settings, even subtle gradients and textures are classified as boundaries, producing a dense mesh of small cells. This control determines the overall "granularity" of the stained glass pattern: low threshold creates large, open panes; high threshold creates intricate, finely divided panels. The threshold interacts with Came Width — a high threshold with wide came can fill the entire image with dark leading.

---

#### Knob 6 — Came Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the hue angle of the lead came strips. In Lead came mode (default), this shifts the came color from neutral gray toward a tinted hue — blue-tinted leading, copper-tinted leading, etc. In Gold came mode, the base came color is a warm golden tone and this control rotates it further around the color wheel. The came tint is purely cosmetic and does not affect the glass pane colors. At 0° the came is neutral; as you rotate through 360° the came passes through the full spectrum.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Glass Type** | Clear | Tint |
| **8 — Came Color** | Lead | Gold |
| **9 — Sun Anim** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 control the visual character of the glass and came respectively — Glass Type selects one of four presets that modify the intra-cell color treatment, while Came Color switches between Lead (dark neutral) and Gold (warm metallic) came appearances. Toggle 9 enables animation of the sunlight pattern. Toggle 10 inverts the output luminance. Toggle 11 bypasses all processing for A/B comparison. The Glass Type is a four-position selector, while all other toggles are simple on/off switches.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed stained glass output and the original unprocessed input. At 100% (fully clockwise, default) the effect is at full intensity. At 0% (fully counter-clockwise) the original signal passes through unaffected. Intermediate positions blend between the two — useful for dialing in a subtle hint of the stained glass effect without committing to the full transformation. The crossfade operates per-channel through three interpolator instances (Y, U, V).

---

## Guided Exercises

These exercises progress from simple edge highlighting through full stained glass simulation. Each builds on the previous, gradually engaging more processing stages and demonstrating the interactions between controls.

### Exercise 1: Lead Came Skeleton

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: vitrage_source1_kodim02, after: vitrage_exercise1_result },
    { label: "Kodim07", before: vitrage_source2_kodim07, after: vitrage_exercise1_result },
    { label: "Kodim01 B&W", before: vitrage_source3_kodim01_bw, after: vitrage_exercise1_result },
  ]}
/>
*Lead Came Skeleton — simulated result across source images.*
**Source**: A live camera feed or recorded footage with strong geometric content — architecture, window frames, or objects with clear edges.

**Objective**: Understand how the edge detector and Came Width interact to create the structural skeleton of a stained glass window.

1. **Reveal the came**: Start with Came Width at about 30% and Edge Threshold at 50%. Dark lines appear at the strongest edges in the source image.
2. **Widen the lead**: Slowly increase Came Width. The dark borders grow thicker, progressively consuming the image. Notice how wide came with few cells creates bold, graphic outlines.
3. **Increase sensitivity**: Raise Edge Threshold to 80%. More edges are detected and the cell mesh becomes denser — the glass panes shrink.
4. **Reduce sensitivity**: Lower Edge Threshold to 20%. Only the most prominent contours survive as came lines. Large, open panes dominate.
5. **Gold came**: Toggle Came Color to Gold. The dark came lines take on a warm golden hue.

**Key concepts**: Edge detection identifies cell boundaries, Came Width controls border thickness, Edge Threshold controls detection sensitivity, denser detection creates smaller cells

---

### Exercise 2: Colored Glass Panels

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: vitrage_source1_kodim02, after: vitrage_exercise2_result },
    { label: "Kodim07", before: vitrage_source2_kodim07, after: vitrage_exercise2_result },
    { label: "Kodim01 B&W", before: vitrage_source3_kodim01_bw, after: vitrage_exercise2_result },
  ]}
/>
*Colored Glass Panels — simulated result across source images.*
**Source**: Footage with varied, saturated colors — flowers, street art, colorful textiles, or a test pattern with gradients.

**Objective**: Explore how flattening and saturation boost transform the source into vivid stained glass panes.

1. **Prepare skeleton**: Set Came Width ~25%, Edge Threshold ~50% to establish a visible cell grid.
2. **Flatten the color**: Increase Flat Amt from 0% to about 70%. Watch intra-cell gradients collapse into flat uniform regions — each pane becomes a single color.
3. **Boost saturation**: Raise Saturate to about 60%. Colors within each pane intensify dramatically, emulating the vivid hues of stained glass.
4. **Add sunlight**: Bring Sunlight up to about 40%. Each pane now glows from within — brighter at the centre, dimmer at the edges.
5. **Try Glass Types**: Cycle through the four Glass Type modes. Notice how Tint shifts all pane colors toward one hue, Opal washes them out to milky pastels, and Antique adds textural variation.

**Key concepts**: Flattening quantizes luma within cells to simulate uniform glass color, saturation boost emulates the color-filtering properties of glass, sunlight gradient creates the backlit glow, glass types modify the color treatment

---

### Exercise 3: Animated Cathedral Window

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: vitrage_source1_kodim02, after: vitrage_exercise3_result },
    { label: "Kodim07", before: vitrage_source2_kodim07, after: vitrage_exercise3_result },
    { label: "Kodim01 B&W", before: vitrage_source3_kodim01_bw, after: vitrage_exercise3_result },
  ]}
/>
*Animated Cathedral Window — simulated result across source images.*
**Source**: Slowly moving footage — clouds, water reflections, or a slow camera pan across a landscape.

**Objective**: Combine all processing stages to create a fully realized animated stained glass window effect.

1. **Full setup**: Came Width ~30%, Flat Amt ~80%, Saturate ~70%, Sunlight ~50%, Edge Thr ~60%.
2. **Gold leading**: Toggle Came Color to Gold. Tint the came to a warm amber at about 30° on the Came Tint knob.
3. **Enable animation**: Toggle Sun Anim to On. Watch the sunlight pattern drift slowly across the window, illuminating different panes in sequence.
4. **Antique glass**: Set Glass Type to Antique. The panes develop a subtle texture with slight color irregularities.
5. **Mix down**: Reduce Mix to about 70% to let some of the original image show through, creating a translucent stained-glass overlay.
6. **Inversion negative**: Toggle Invert to see the luminance-negative version — dark glass with bright came lines, like a photographic negative of a window.

**Key concepts**: All stages interact — flattening defines the pane color, saturation intensifies it, sunlight illuminates it, came overlays the boundaries, animation makes it breathe, and mix controls the intensity

---


## Tips

- **Edge Threshold is the most important control**: It determines the number and size of glass panes. Start here when dialing in a look — find the right cell density first, then adjust came width and color processing.
- **Flat Amt and Sunlight work together**: Flattening removes intra-cell variation; Sunlight adds it back as a controlled gradient. Use both to shape the lighting within each pane.
- **Glass Type presets are starting points**: Clear preserves source colors, Tint shifts everything toward one hue, Opal washes out to pastels, Antique adds organic texture. Layer these with Saturate and Sunlight for nuanced results.
- **Came Tint is subtle by default**: The effect is most visible with Came Color set to Gold, which provides a warmer base for the hue shift.
- **Animation is gentle**: Sun Anim creates a slow shimmer, not dramatic motion. It works best with moderate Sunlight and a slowly changing source.
- **Mix for overlay effects**: At 50% Mix, the stained glass effect becomes a semi-transparent overlay on the source — useful for creating a window-like compositing effect.
- **Invert for negative windows**: The Invert toggle creates a striking negative-image version where came lines become bright rails against dark glass. Combine with Gold came and high Saturate for a neon-stained-glass look.
- **Feedback loops**: Routing the output back to the input creates recursive cell subdivision as each generation's edges spawn new came boundaries.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated FPGA memory used for the video line buffer that sample-holds Y values at cell boundaries. |
| **Came** | The lead or zinc strips that hold glass pieces together in a stained glass window; rendered as dark borders at cell boundaries. |
| **Cell** | A rectangular or hexagonal region in the image bounded by came lines; each cell represents one pane of stained glass. |
| **Chroma** | The color information in YUV video, represented by U and V channels centered at midpoint (512 in 10-bit). |
| **Edge Detection** | Comparing adjacent pixel values to identify sharp transitions; used to determine where came boundaries are drawn. |
| **Flattening** | Quantizing the Y channel to a small number of discrete levels, producing uniform color within each glass pane. |
| **Interpolator** | A hardware crossfade unit that blends between two signals by a fractional amount; used for the wet/dry Mix control. |
| **Line Buffer** | A one-line BRAM delay used to compare pixels across scan lines for cell boundary detection. |
| **Opal** | A glass type characterized by milky translucence and pastel colors, simulated by reducing contrast and desaturating. |
| **Pipeline** | The sequence of processing stages from input to output; Vitrage uses a 10-clock pipeline. |
| **Quantization** | Reducing the number of discrete levels in a signal; creates the flat, uniform color regions within glass panes. |
| **Saturate** | Boosting chroma by stretching U/V values away from the neutral midpoint, intensifying colors. |
| **Vitrage** | French term for stained glass or glazing; the art of creating pictures and patterns from pieces of colored glass joined by lead strips. |
| **YUV** | Color encoding separating luminance (Y) from chrominance (U, V); the native format of the Videomancer video pipeline. |

---
