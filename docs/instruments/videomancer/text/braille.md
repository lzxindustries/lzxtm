---
draft: true
sidebar_position: 28
slug: /instruments/videomancer/braille
title: "Braille"
image: /img/instruments/videomancer/braille/braille_hero.png
---

import braille_hero from '/img/instruments/videomancer/braille/braille_hero.png';
import braille_before_after from '/img/instruments/videomancer/braille/braille_before_after.png';
import braille_control_panel from '/img/instruments/videomancer/braille/braille_control_panel.png';
import braille_exercise1_result from '/img/instruments/videomancer/braille/braille_exercise1_result.png';
import braille_exercise2_result from '/img/instruments/videomancer/braille/braille_exercise2_result.png';
import braille_exercise3_result from '/img/instruments/videomancer/braille/braille_exercise3_result.png';

# Braille

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={braille_hero} alt="Braille hero image"/>
*Braille converting a photographic image into an array of tactile-style embossed dots on a paper-textured surface.*
<img src={braille_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Braille applied.*

---

## Overview

The Braille cell — six or eight raised dots arranged in a 2×3 or 2×4 matrix — is one of the most elegant encodings ever devised. Each cell maps a binary pattern to a tactile letter, turning the fingertip into a reader. Braille takes this idea and applies it to video: the luminance of each region of the image determines whether a dot is raised or flat, converting continuous tone into a field of embossed points on a simulated paper surface.

The program divides the frame into a grid of rectangular cells, tests each cell's luminance against an adjustable threshold, and renders a dot at the center of every cell that passes the test. Four rendering styles — raised, pressed, outline, and filled — control how the dots interact with the paper surface. Emboss shading adds a pseudo-3D illusion of depth: raised dots appear to protrude from the page, pressed dots appear to sink into it. The name references both the Braille writing system and the broader concept of *bump mapping* — using light and shadow cues to suggest texture on a flat surface.

At gentle settings with large cells and moderate threshold, Braille produces a clean halftone pattern reminiscent of newspaper printing or perforated metal. At extreme settings with small cells, high emboss depth, and tinted color mode, the output becomes a dense tactile mosaic where the original image is encoded entirely in the pattern of raised and lowered points.

---

## Background

### Louis Braille and Tactile Encoding

In 1824, a fifteen-year-old French student named Louis Braille adapted Charles Barbier's military night-writing system into a compact six-dot cell that could represent any letter, number, or punctuation mark. The brilliance of the system lies in its geometry: six dots arranged in a 2×3 matrix yield 64 possible combinations (2⁶), enough for an entire alphabet with room for contractions and formatting. Later extensions to an eight-dot cell (2×4) expanded the space to 256 combinations (2⁸) — a full byte. This program uses the 2×4 cell proportion at its default size, a direct nod to the extended Braille cell.

### Threshold-Based Halftoning

The simplest halftoning algorithm compares each pixel's brightness to a fixed threshold: above the threshold, print a dot; below it, leave the surface blank. This binary decision — dot or no dot — is the foundation of all halftone printing, from newspaper photographs to laser printer output. The result depends critically on the threshold level and the cell size. A low threshold produces sparse dots (only the brightest areas trigger); a high threshold produces dense dot fields (only the darkest areas are blank). Braille's Thresh knob gives continuous control over this decision boundary.

### Cell Geometry and Dot Proportion

Traditional halftone screens use square or hexagonal cells. Braille uses rectangular cells with a 1:2 width-to-height ratio — matching the proportions of an actual Braille cell. The cell size selector offers four scales from 2×4 pixels (almost invisible in HD) up to 16×32 pixels (clearly visible block structure). Within each cell, the dot sits at the center. The Dot Size control adjusts the radius of the dot shape relative to the cell boundary. Small dots create sparse, airy patterns; large dots fill the cell almost completely, approaching a solid halftone.

### Emboss Rendering and Tactile Illusion

A flat circle on a flat background is just a dot. But add a brightness offset that varies with position — brighter on the top-left edge, darker on the bottom-right — and the circle suddenly appears to protrude from the surface. This is the principle behind *emboss* or *bump mapping* rendering. Braille uses a simplified version: rather than computing per-pixel normals, it applies a uniform brightness boost to raised dots and a uniform darkening to pressed dots. The four style modes give different tactile illusions: Raised dots catch light and stand proud of the surface. Pressed dots sit in shadow below the paper plane. Outline dots show only the ring edge. Filled dots are flat solid circles with no depth shading.

### From Dots to Image

The connection between dot patterns and image perception is a matter of spatial frequency. At sufficient distance — or at sufficiently small cell size — the eye integrates the individual dots into a continuous tone. This is the same principle that makes newspaper halftones, pointillist paintings, and LED billboard displays work. Braille sits at the boundary: at small cell sizes, the dot pattern merges into a recognizable image; at large cell sizes, the individual dots dominate and the image becomes an abstract texture of raised points.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Cell Position Calculation ──────────────────────────
│   ├─ cell_row = v_count / cell_height  (bit shift)
│   ├─ cell_col = h_count / cell_width   (bit shift)
│   ├─ local_x = h_count mod cell_width  (bit mask)
│   └─ local_y = v_count mod cell_height (bit mask)
│
├── Stage 2: Threshold Test & Dot Shape ─────────────────────────
│   ├─ Threshold: input Y > thresh_reg → dot raised
│   ├─ Dot radius = dot_sz_reg >> 7 + 1  (range 1–8 px)
│   ├─ Box test: |local_x - center_x| < radius
│   │            AND |local_y - center_y| < radius
│   └─ Grid detect: local_x == 0 OR local_y == 0
│
├── Stage 3: Emboss Shading & Paper ─────────────────────────────
│   ├─ Paper brightness = paper_reg >> 1 + 256  (range 256–767)
│   ├─ Emboss offset = emboss_reg >> 2
│   ├─ Style select (toggle_switch_7, 2-bit):
│   │   ├─ 00 Raised:  dot_bright + emboss_offset
│   │   ├─ 01 Pressed: paper - emboss_offset
│   │   ├─ 10 Outline: dot_bright (flat)
│   │   └─ 11 Filled:  dot_bright (flat)
│   └─ Grid overlay: -64 luma at cell boundaries
│
├── Stage 4: Color Mode, Invert, Mix ───────────────────────────
│   ├─ Invert toggle (negate output Y)
│   ├─ Color mode:
│   │   ├─ Mono:   U=512, V=512
│   │   └─ Tinted: raised dots retain source U/V
│   └─ Mix: interpolate processed ↔ source (3× interpolator_u)
│
├── Sync Signals ────────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ──────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline uses exclusively bit-shift and bit-mask operations for cell division, making it free of any division hardware. Cell widths and heights are always powers of two (2, 4, 8, 16 wide × 4, 8, 16, 32 tall), so modular arithmetic reduces to simple masking. The emboss shading is computed *after* the dot shape test, meaning the style toggle affects only how the dot pixel is shaded — the dot's presence or absence is determined solely by the threshold comparison in Stage 2. The tinted color mode feeds source chroma through only where dots are raised, creating a pointillist color effect where the original hues appear as discrete colored dots on a neutral paper surface.

---

## Parameter Reference

<img src={braille_control_panel} alt="Videomancer front panel with Braille loaded"/>
*Videomancer's front panel with Braille active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Thresh
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

The luminance decision boundary. Every cell in the grid gets a single binary verdict: is the average brightness of the source region above or below this threshold? Below the threshold, the cell shows only paper. Above it, a dot appears. At 0% the threshold is so low that nearly every cell triggers a dot, producing a dense field. At 100% only the very brightest highlights produce dots, yielding a sparse, high-contrast pattern. This is the most immediate control — sweep it slowly across a photographic source and watch the image emerge from and dissolve into the dot field.

---

#### Knob 2 — Cell Sz
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

Selects one of eight cell size steps. The cell always maintains a 1:2 width-to-height ratio matching Braille proportions. Step 1 (2×4 pixels) produces an extremely fine dot grid that reads almost as continuous tone at normal viewing distance. Step 4 (16×32 pixels) creates large, clearly visible cells where each dot is an obvious graphical element. Larger cells mean fewer dots, so the image becomes more abstract. The upper four steps repeat the largest sizes. The relationship between cell size and Dot Size is important: a given dot radius looks proportionally different inside a small cell versus a large one.

---

#### Knob 3 — Dot Sz
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the radius of each dot shape within its cell. The dot is rendered as a box (axis-aligned square) centered in the cell. At minimum, each dot is a single pixel — a sparse pinpoint pattern. At maximum, dots nearly fill their cells, and the output approaches a blocky halftone where dots merge into solid regions. The box shape was chosen over a circular shape to reduce FPGA resource usage (no square root needed) while producing visually clean results at all scales. The dot size interacts with emboss depth: larger dots have more visible emboss shading because there is more surface area for the brightness offset to act on.

---

#### Knob 4 — Emboss
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

The depth of the emboss illusion. At 0%, dots are flat — no brightness difference between the center and edge of a dot. As you increase this control, the brightness offset grows: raised dots become brighter, pressed dots become darker. At maximum emboss with the Raised style, dots appear to pop dramatically off the paper surface. The emboss effect is most visible at larger cell sizes and moderate Paper brightness, where there is room in the luminance range for the offset to be clearly visible without clipping.

---

#### Knob 5 — Paper
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the base brightness of the paper surface — the background behind and between dots. The range spans from dim (roughly quarter-brightness) to bright (roughly three-quarter brightness). Dark paper with bright raised dots creates a "white on black" Braille aesthetic. Bright paper with pressed dots creates the classic embossed-paper look. The paper brightness also determines the contrast ratio between dot and background, which is critical for the emboss illusion: too little contrast and the dots disappear; too much and the emboss shading clips.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a brightness boost to dots beyond the base emboss level. This is additive with the emboss offset — it lifts the overall luminance of raised dots regardless of style. At 0%, dot brightness comes purely from the style and emboss settings. At maximum, dots are pushed toward peak white. Use this to recover dot visibility when working with dark paper settings, or to push raised dots into intentional clipping for a hard, overexposed dot texture.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Raised | Pressed |
| **8 — Grid** | Off | On |
| **9 — Color** | Mono | Tinted |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Toggle switches 7–11 control five independent aspects of the rendering. Switch 7 is unusual in that it encodes a 2-bit value across its two states combined with an internal second bit, selecting among four rendering styles. Switches 8–11 are simple on/off controls. The Grid toggle (Switch 8) adds visible cell boundaries regardless of whether a cell contains a dot, providing a structural overlay. Color mode (Switch 9) determines whether dot color is monotone neutral or derived from the source chroma. Invert (Switch 10) flips the entire output. Bypass (Switch 11) routes the source directly to output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the processed Braille output and the original source signal. At 100% (fully up), the output is entirely processed. At 0% (fully down), the output is the unmodified source. Intermediate positions blend the two, creating a semi-transparent overlay where the dot pattern is visible over the original image. The mix uses three parallel interpolators — one each for Y, U, and V — maintaining correct color handling throughout the blend.

---

## Guided Exercises

These exercises build from basic threshold halftoning through emboss rendering to full tactile-style color output. Each exercise introduces new controls while reinforcing the ones already explored.

### Exercise 1: Basic Threshold Halftone

<img src={braille_exercise1_result} alt="Basic Threshold Halftone result"/>
*Basic Threshold Halftone — simulated result across source images.*
**Source**: A portrait or landscape with a wide tonal range — faces, sky, foliage.

**Objective**: Learn how the threshold and cell size controls convert continuous tone into a binary dot pattern.

1. **Default view**: With all controls at initial values, observe the dot pattern. The image should be recognizable as a field of dots on a mid-brightness paper.
2. **Sweep threshold**: Slowly turn Thresh from 0% to 100%. Watch dots appear and disappear in order of brightness — highlights first, then midtones, then shadows.
3. **Change cell size**: Step through Cell Sz from 1 to 8. At small sizes the image is detailed but dots are tiny. At large sizes the image becomes an abstract grid of widely-spaced dots.
4. **Dot size**: At Cell Sz = 4 (8×16 cells), sweep Dot Sz from minimum to maximum. Small dots create an airy perforation pattern; large dots create a chunky block halftone.
5. **Grid overlay**: Toggle Grid on. The cell boundaries appear as a fine lattice. Note how the grid reinforces the cellular structure at all dot sizes.

**Key concepts**: Threshold halftoning is binary per cell, cell size sets spatial resolution, dot size controls fill factor within each cell, grid overlay reveals cell boundaries

---

### Exercise 2: Emboss and Style Exploration

<img src={braille_exercise2_result} alt="Emboss and Style Exploration result"/>
*Emboss and Style Exploration — simulated result across source images.*
**Source**: A high-contrast black-and-white image or graphic with strong shapes.

**Objective**: Explore the four rendering styles and the emboss depth control.

1. **Raised dots**: Set Emboss to ~60%, Cell Sz to 5 (16×32), Dot Sz to ~50%. The dots appear to protrude from the paper surface.
2. **Pressed dots**: Switch Style to Pressed. The dots now appear as concave depressions — dark wells in the paper. Increase Paper brightness to see the effect more clearly.
3. **Outline dots**: Switch Style to Outline. Dots become flat bright rings with no depth illusion. Note that Emboss has no visible effect in this mode.
4. **Filled dots**: Switch Style to Filled. Solid flat dots — the cleanest, most graphic result.
5. **Emboss depth**: Return to Raised style. Sweep Emboss from 0% to 100%. At maximum, dots are bright white against the paper surface. Reduce Paper brightness and observe how the emboss interacts with available contrast range.
6. **Bright boost**: Increase Bright to push dot luminance further. Note the additive relationship with emboss.

**Key concepts**: Emboss creates depth illusion via brightness offset, four styles offer different tactile and graphic aesthetics, paper brightness sets the contrast baseline for emboss visibility

---

### Exercise 3: Tinted Pointillist Color

<img src={braille_exercise3_result} alt="Tinted Pointillist Color result"/>
*Tinted Pointillist Color — simulated result across source images.*
**Source**: Saturated, multicolored footage — flowers, costumes, painted surfaces, or the macaw image.

**Objective**: Combine tinted color mode with emboss rendering for a pointillist effect.

1. **Enable tinted mode**: Switch Color to Tinted. Dots now carry the source chrominance — each dot is colored according to the original image hue at that cell position.
2. **Adjust threshold**: Set Thresh to ~45% so most midtone and highlight cells produce dots. The image should be recognizable through the colored dots alone.
3. **Cell size for pointillism**: Use Cell Sz 3 (4×8 cells) for a fine pointillist grid, or Cell Sz 5 (16×32) for bold, clearly-visible colored dots.
4. **Emboss on color**: With Raised style and Emboss at ~40%, the colored dots appear to pop up from the neutral paper. The luminance boost from emboss combines with the source color to create bright, saturated dot highlights.
5. **Invert**: Toggle Invert on. The paper becomes dark, neutral-colored dots become bright colored points on a dark field — a very different mood.
6. **Partial mix**: Lower Mix to ~60%. The source image bleeds through behind the dot pattern, creating a textured overlay.

**Key concepts**: Tinted mode passes source chroma through dot positions only, monochrome paper behind dots creates pointillist color separation, invert reverses the tactile metaphor, mix creates overlay blends

---


## Tips

- **Threshold is the primary image control**: Sweep it slowly across a photographic source. The image emerges gradually from the dot field as you find the sweet spot where midtone detail resolves.
- **Cell size and dot size are a pair**: Large cells with small dots create airy, open patterns. Small cells with large dots create dense, block-like halftones. Experiment with the ratio, not just the absolute values.
- **Emboss needs headroom**: The emboss effect adds or subtracts brightness from the paper level. Set Paper to a moderate value (60–80%) so there is room in both directions for the offset to be visible without clipping.
- **Tinted mode is pointillism**: Colored dots on a neutral background is the literal technique of Seurat and Signac. Use moderate cell sizes (steps 3–5) for the most painterly results.
- **Grid reveals structure**: The grid overlay is subtle but useful for understanding cell boundaries, especially when troubleshooting threshold or dot size interactions.
- **Invert for dark-field**: Toggle Invert for a "bright dots on dark background" aesthetic, which reads very differently from the default "dots on paper" look.
- **Mix for texture blending**: Partial mix values overlay the dot pattern on the source, creating a textured, screen-printed look that retains source detail.
- **Feedback loops**: Route the output back to the input to create recursive dot patterns — dots within dots, with each generation responding to the embossed texture of the previous one.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bit mask** | A binary pattern used to extract or isolate specific bits from a value, employed here for modular arithmetic on cell coordinates without division hardware. |
| **Bump mapping** | A rendering technique that uses brightness offsets to simulate the appearance of surface texture and depth on a flat image. |
| **Chrominance** | The color-difference components (U and V) of a YUV signal, representing hue and saturation independently of luminance. |
| **Emboss** | A shading technique that applies directional brightness offsets to simulate raised or depressed surfaces, creating a pseudo-three-dimensional appearance. |
| **Fill factor** | The ratio of dot area to total cell area; higher fill factors produce denser patterns where dots approach the boundaries of their cells. |
| **Halftone** | A reprographic technique that simulates continuous tonal gradation using discrete dots of varying size or spacing. |
| **Interpolator** | A hardware block that linearly blends between two input values based on a mix coefficient, used here for dry/wet crossfading of Y, U, and V channels. |
| **Luma** | The luminance (Y) component of a YUV video signal, representing perceived brightness. |
| **Pointillism** | A painting technique using small, distinct dots of color that blend optically at viewing distance; Braille's tinted mode produces a digital analogue of this technique. |
| **Spatial frequency** | The rate of brightness or pattern variation per unit distance in an image; at sufficiently high spatial frequency, discrete dots merge into perceived continuous tone. |
| **Threshold** | A fixed decision boundary against which each cell's luminance is compared to determine whether a dot is rendered (above) or omitted (below). |
| **YUV** | A color encoding scheme that separates luminance (Y) from chrominance (U, V), widely used in video systems to exploit the eye's greater sensitivity to brightness than to color. |

---
