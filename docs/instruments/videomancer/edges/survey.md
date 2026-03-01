---
draft: true
sidebar_position: 252
slug: /instruments/videomancer/survey
title: "Survey"
image: /img/instruments/videomancer/survey/survey_hero.png
description: "Topographic maps translate three-dimensional terrain into two-dimensional line drawings."
---

import survey_before_after from '/img/instruments/videomancer/survey/survey_before_after.png';
import survey_control_panel from '/img/instruments/videomancer/survey/survey_control_panel.png';
import survey_exercise1_result from '/img/instruments/videomancer/survey/survey_exercise1_result.png';
import survey_exercise2_result from '/img/instruments/videomancer/survey/survey_exercise2_result.png';
import survey_exercise3_result from '/img/instruments/videomancer/survey/survey_exercise3_result.png';
import survey_hero from '/img/instruments/videomancer/survey/survey_hero.png';
import survey_source1_kodim02 from '/img/instruments/videomancer/survey/survey_source1_kodim02.png';
import survey_source2_kodim07 from '/img/instruments/videomancer/survey/survey_source2_kodim07.png';
import survey_source3_kodim01_bw from '/img/instruments/videomancer/survey/survey_source3_kodim01_bw.png';

# Survey

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={survey_hero} alt="Survey hero image"/>
*Survey rendering topographic contour lines from a natural scene, with relief shading and altitude-banded color tinting.*
<img src={survey_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Survey applied.*

---

## Overview

Topographic maps translate three-dimensional terrain into two-dimensional line drawings. Contour lines connect points of equal elevation; where the lines crowd together, the terrain is steep; where they spread apart, it is flat. Survey applies this cartographic principle to the luminance channel of live video. Brightness becomes elevation, and the program draws contour lines wherever the luma value crosses a power-of-two boundary.

The contour detection is entirely bitwise — no division or modulus operators appear anywhere in the design. Instead, the program AND-masks the 10-bit luma value against a power-of-two mask and tests whether the masked result is near zero or near the mask value. This simple bit test detects boundary crossings at geometrically-spaced intervals (every 16, 32, 64, 128, 256, or 512 luma levels). A one-line BRAM delay provides the previous scanline's luma for vertical gradient calculation, enabling relief shading that simulates directional hillside lighting. Between contour lines, the luma is divided into altitude bands that can be color-tinted with a cartographic color ramp.

At subtle settings — wide interval spacing, thin lines, gentle tinting — Survey adds a delicate topographic overlay to any video source. At extreme settings — narrow spacing, thick lines, strong relief — the image transforms into an abstracted terrain map where the original content is barely recognizable beneath its own elevation contours.

---

## Background

### Contour Lines and Isohypses

In cartography, a **contour line** (or isohypse) connects all points at a given elevation. The vertical distance between adjacent contour lines is the **contour interval**. On a real topographic map, the interval is a fixed number of metres (e.g., 10 m). In Survey, the "elevation" is the luma value (0–1023), and the contour interval is a power-of-two bitmask. A mask of 63 means contour lines appear every 64 luma levels; a mask of 255 means every 256 levels. The power-of-two constraint means the interval is always a clean binary boundary, which is what makes pure bitmask detection (no division) possible.

### Power-of-Two Bitmask Detection

Survey avoids all arithmetic division. Instead, it detects contour boundaries by AND-masking the luma value with the contour mask and checking if the result is near zero or near the mask value. If `Y AND mask <= width_threshold` or `Y AND mask >= mask − width_threshold`, the pixel is on a contour line. This is equivalent to checking whether Y is within `width_threshold` of any multiple of `(mask + 1)`. The technique exploits the fact that powers of two in binary representation have a single bit set, making boundary detection reducible to simple bitwise logic.

### Relief Shading and Hillshade

Relief shading simulates the effect of a light source illuminating terrain from one direction. In traditional cartography, the illumination direction is conventionally from the northwest. Survey computes a simplified version: the vertical gradient (current line Y minus previous line Y from the BRAM line buffer) serves as a proxy for slope. Positive gradients (brightening downward) receive a brightness boost; negative gradients (darkening downward) receive a dimming. The relief strength parameter scales this gradient before adding it to the background luma. The result is an embossed, three-dimensional quality that makes the contour map appear to have depth.

### Altitude Color Tinting (Hypsometric Tints)

On printed topographic maps, the regions between contour lines are often filled with **hypsometric tints** — color gradients that encode elevation. Low elevations might be green (vegetation), middle elevations brown (rock), and high elevations white (snow). Survey achieves a simplified version: the upper 4 bits of the luma value define an altitude band (0–15), and this band index is multiplied by the altitude tint parameter to produce U and V offsets from the chroma midpoint. The U offset uses the band value directly; the V offset uses its bitwise complement, creating a complementary color spectrum across the altitude range.

### Line Buffers and Vertical Delay

The BRAM line buffer stores one complete scanline of luma values (up to 2048 pixels at 11-bit address depth). As each pixel arrives, its luma is written to the buffer at the current horizontal position, and the luma from the same position on the *previous* line is read out simultaneously. This one-line delay provides the vertical neighbor needed for relief gradient calculation. The ping-pong addressing (toggled by `s_lb_ab` on each hsync) ensures that reads and writes never collide. This is the only BRAM resource used by the entire program.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Line Buffer I/O ──────────────────
│   ├─ Latch Y, U, V
│   ├─ Write current Y to BRAM line buffer
│   └─ Read previous-line Y from BRAM
│
├── Stage 2: Contour Detection + Relief + Altitude Band ────────
│   ├─ v_masked = Y AND contour_mask
│   ├─ Near edge? (v_masked ≤ width_mask OR ≥ mask−width_mask)
│   │   → s_is_contour (optionally inverted)
│   ├─ Relief gradient: Y_current − Y_previous_line (signed)
│   └─ Altitude band: Y(9 downto 6) → 4-bit index
│
├── Stage 3: Multiply Products (registered) ────────────────────
│   ├─ Relief multiply: gradient × relief_strength → s_relief_add
│   └─ Altitude tint: band × tint_strength → U/V offsets
│
├── Stage 4: Composite Mux ────────────────────────────────────
│   ├─ Contour pixel → Y = contour_luma, U = V = 512
│   └─ Non-contour pixel → Y = bg_y + relief_add (clamped)
│      + altitude color (if enabled): U/V = 512 + tint offsets
│
├── Stage 5: Output Register ──────────────────────────────────
│
├── Mix Stage (interpolator_u × 3) ────────────────────────────
│   └─ Wet/dry crossfade by Mix fader
│
└── Bypass Mux ────────────────────────────────────────────────
    └─ Bypass → pass delayed input directly
```

The contour detection uses pure bitwise logic — AND-masking followed by a threshold comparison — which means the contour intervals are always powers of two. This creates geometrically-spaced elevation bands rather than linearly-spaced ones. The relief shading operates on the *raw* input luma (via BRAM), not on the quantised contour output, so the shading gradient is smooth even when contour lines are coarse. The composite mux makes a hard binary decision: each pixel is either a contour line (rendered at the Contrast brightness) or background fill (rendered at the Smooth brightness plus relief shading). There is no anti-aliasing or feathering at contour edges.

---

## Parameter Reference

<img src={survey_control_panel} alt="Videomancer front panel with Survey loaded"/>
*Videomancer's front panel with Survey active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Interval
| Property | Value |
|----------|-------|
| Range | 4 – 64 |
| Default | 34 |

Controls the contour line spacing by selecting the power-of-two bitmask used for boundary detection. At low values, the mask is small (15 = every 16 luma levels), producing dense, closely-spaced contour lines that reveal fine tonal variations. At high values, the mask is large (511 = every 512 levels), producing widely-separated contour lines that show only major tonal boundaries. The stepped control provides six discrete mask values, each doubling the contour interval. Dense contours turn smooth gradients into richly-layered topographic textures; sparse contours extract only the boldest tonal edges.

---

#### Knob 2 — Line W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the thickness of contour lines by controlling the width threshold for the edge detection comparison. At low values, only pixels very close to the exact bitmask boundary are marked as contour lines, producing hair-thin lines. At higher values, a wider tolerance region is used, and the contour lines become thicker bands. The width mask is derived from the contour mask by right-shifting, so thicker lines scale proportionally with the contour interval. Combined with the Index Bold toggle, this control can produce anything from delicate cartographic linework to bold topographic bands.

---

#### Knob 3 — Index Sp
| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 5 |

Controls the saturation of the altitude color tinting applied between contour lines. At zero, the fill regions are monochrome (controlled only by the Smooth brightness). As the value increases, the altitude bands receive progressively stronger U and V offsets, creating a color spectrum across the elevation range. The U channel offset follows the altitude band index directly; the V channel uses the bitwise complement, so high and low elevations receive complementary colors. At maximum, the color banding is vivid and clearly delineates each altitude zone.

---

#### Knob 4 — Color Ramp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the strength of relief shading — the directional gradient lighting applied to the background fill. At zero, no relief is applied and all non-contour pixels share the same flat brightness. As the value increases, the vertical luma gradient (computed from the BRAM line buffer) is amplified and added to the background luma, creating an embossed, three-dimensional appearance. Positive gradients (brightening downward) are boosted; negative gradients are dimmed. The result simulates a light source above the image illuminating the luminance "terrain" from above.

---

#### Knob 5 — Smooth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the background fill brightness for non-contour pixels. This sets the base luma level for regions between contour lines, before relief shading is added. At low values, the background is dark and only contour lines and relief highlights are visible. At high values, the background is bright and the contour lines appear as darker marks on a light field. This control interacts with relief shading: the relief gradient is *added* to this base value, so a dark background with strong relief creates a dramatic chiaroscuro effect, while a bright background with gentle relief creates a subtle embossed overlay.

---

#### Knob 6 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the brightness of contour line pixels directly. When a pixel is classified as a contour line, its Y value is replaced with this parameter's register value. At zero, contour lines are black — dark ink on whatever background the fill provides. At maximum, contour lines are white. At intermediate values, the lines take on a mid-gray tone. This control is independent of the background fill brightness (Smooth), so you can create dark lines on a bright background, bright lines on a dark background, or any combination.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Terrain | Ocean |
| **8 — Index Bold** | Off | On |
| **9 — Fill Mode** | Color | Flat |
| **10 — Labels** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary features. Palette enables or disables relief shading. Index Bold doubles the contour line thickness. Fill Mode enables or disables altitude color tinting. Labels inverts the contour detection polarity. Bypass routes the input directly to output. These switches operate independently — each affects a single processing decision in the pipeline.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (unprocessed) input and the wet (contour-mapped) output. At 100%, only the processed contour rendering is visible. At 0%, the original input passes through unchanged. Intermediate values create a transparent contour overlay on the source — useful for augmenting footage with topographic annotations while preserving recognisability. The interpolation is linear per-channel.

---

## Guided Exercises

These exercises progress from basic contour extraction through relief shading to full cartographic terrain rendering with color tinting and inversion.

### Exercise 1: Basic Contour Lines

<img src={survey_exercise1_result} alt="Basic Contour Lines result"/>
*Basic Contour Lines — simulated result across source images.*
**Source**: A scene with smooth tonal gradients — a landscape, a face lit from one side, or a gradient test pattern.

**Objective**: Understand how bitmask-based contour detection extracts elevation lines from the luminance channel.

1. **Dense contours**: Set Interval to its lowest setting. Dense contour lines appear, tracing every fine tonal transition in the image.
2. **Sparse contours**: Increase Interval toward maximum. Only the boldest tonal boundaries remain as contour lines.
3. **Line thickness**: Sweep Line W from minimum to maximum. Watch the contour lines grow from hairlines to thick bands.
4. **Background brightness**: Adjust Smooth to set the fill brightness. Try dark background (low) for contour-on-black, then bright background (high) for contour-on-white.
5. **Contour brightness**: Adjust Contrast to set the line brightness independently of the background.
6. **Thick toggle**: Enable Index Bold to double the line thickness at the current Line W setting.

**Key concepts**: Contour detection uses bitmask AND (no division), interval spacing is always a power of two, line width and contour brightness are independent controls

---

### Exercise 2: Relief Shading

<img src={survey_exercise2_result} alt="Relief Shading result"/>
*Relief Shading — simulated result across source images.*
**Source**: A scene with strong vertical brightness variations — a sunset sky, a face with directional lighting, or a landscape with horizon gradient.

**Objective**: Learn how the BRAM line buffer enables vertical gradient-based relief shading.

1. **Enable relief**: Set Palette to Terrain (relief enabled) and increase Color Ramp to ~50%.
2. **Observe shading**: Notice how regions with downward brightness transitions appear lighter, and upward transitions appear darker — simulating top-down lighting.
3. **Strong relief**: Increase Color Ramp to ~80%. The embossed effect becomes dramatic.
4. **Dark background**: Set Smooth to ~20% to let relief highlights and shadows dominate.
5. **Combine with contours**: Set Interval to ~40% and Line W to ~30%. The contour lines now sit on a relief-shaded terrain.
6. **Relief only**: Set Interval to maximum (sparse contours) to isolate the relief shading effect.

**Key concepts**: Relief uses the BRAM line buffer for vertical gradient, the gradient is multiplied by relief strength before adding to background, relief operates on raw input luma independent of contour quantisation

---

### Exercise 3: Full Cartographic Rendering

<img src={survey_exercise3_result} alt="Full Cartographic Rendering result"/>
*Full Cartographic Rendering — simulated result across source images.*
**Source**: Any footage with a range of brightness levels — a landscape, a still life, or abstract video synthesis.

**Objective**: Combine contour lines, relief shading, and altitude color tinting for a complete terrain map aesthetic.

1. **Color tinting**: Set Fill Mode to Color and increase Index Sp (altitude tint) to ~60%. Color bands appear between contour lines.
2. **Relief + color**: Enable Palette (relief) and set Color Ramp to ~50%. The color bands now have three-dimensional shading.
3. **Dense contours**: Set Interval to ~30% for detailed linework over the colored terrain.
4. **Invert**: Enable Labels (invert polarity). The contour bands become solid fills and the boundaries become background gaps — a negative terrain map.
5. **Thick lines**: Enable Index Bold and increase Line W to ~60%. Bold contour bands dominate the image.
6. **Mix overlay**: Reduce Mix to ~60% to overlay the terrain map transparently on the original source.

**Key concepts**: Altitude tinting uses upper bits of source luma to create complementary U/V offsets, relief shading operates independently of color tinting, invert polarity swaps contour and background roles

---


## Tips

- **Interval is geometric, not linear**: Each step doubles the contour spacing because the mask values are powers of two. Moving one step changes the map density dramatically.
- **Line width scales with interval**: The width threshold is derived from the contour mask, so the same Line W setting produces visually different thicknesses at different intervals. Adjust both together.
- **Relief needs Palette enabled**: The Color Ramp knob has no effect unless the Palette toggle is set to Terrain (relief enabled). Check the toggle first if relief isn't visible.
- **Dark background for drama**: Set Smooth low and Contrast high for bright contour lines on a dark relief-shaded terrain — the classic cartographic look.
- **Invert for negative maps**: The Labels toggle creates a negative-image effect that turns contour lines into filled bands. Combined with altitude color, this produces broad elevation color chips.
- **Mix for overlay**: Use the Mix fader at 50–70% to overlay the contour map transparently on the source footage — a topographic annotation layer that preserves the original image.
- **Feedback loops**: Route the output back to the input. The contour detector re-processes its own quantised bands, creating recursive fractal-like contour patterns at each power-of-two boundary.
- **Flat input test**: Feed a uniform color to confirm zero contours — useful for verifying the program is running correctly before applying to complex sources.

---

## Glossary

| Term | Definition |
|------|------------|
| **Altitude Band** | A quantised elevation zone defined by the upper bits of the luma value, used to assign hypsometric color tints. |
| **Bitmask** | A binary pattern used to isolate specific bits of a value; Survey uses bitmask AND for division-free contour detection. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **Contour Interval** | The vertical distance (in luma levels) between adjacent contour lines; always a power of two in Survey. |
| **Contour Line** | A line connecting points of equal luminance, analogous to an isohypse on a topographic map. |
| **Hypsometric Tint** | A color assigned to an elevation band on a topographic map, encoding altitude as hue. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **Line Buffer** | A BRAM-based FIFO that delays one scanline of pixel data, providing vertical neighbor access for gradient calculation. |
| **Relief Shading** | A cartographic technique that simulates directional lighting on terrain to create a three-dimensional appearance. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
