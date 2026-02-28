---
draft: true
sidebar_position: 178
slug: /instruments/videomancer/neon
title: "Neon"
image: /img/instruments/videomancer/neon/neon_hero.png
description: "Program guide for Neon, a Videomancer edges program for the LZX video synthesizer."
---

import neon_before_after from '/img/instruments/videomancer/neon/neon_before_after.png';
import neon_control_panel from '/img/instruments/videomancer/neon/neon_control_panel.png';
import neon_exercise1_result from '/img/instruments/videomancer/neon/neon_exercise1_result.png';
import neon_exercise2_result from '/img/instruments/videomancer/neon/neon_exercise2_result.png';
import neon_exercise3_result from '/img/instruments/videomancer/neon/neon_exercise3_result.png';
import neon_hero from '/img/instruments/videomancer/neon/neon_hero.png';
import neon_source1_kodim02 from '/img/instruments/videomancer/neon/neon_source1_kodim02.png';
import neon_source2_kodim07 from '/img/instruments/videomancer/neon/neon_source2_kodim07.png';
import neon_source3_kodim01_bw from '/img/instruments/videomancer/neon/neon_source3_kodim01_bw.png';

# Neon

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={neon_hero} alt="Neon hero image"/>
*Neon rendering luminous colored edge halos over a darkened background, transforming video contours into glowing tube outlines.*
<img src={neon_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Neon applied.*

---

## Overview

Every city at dusk has them — glass tubes bent into letters and shapes, filled with ionized gas, glowing with saturated color against dark storefronts. Neon recreates this aesthetic electronically. It detects horizontal luminance edges in the incoming video, gates them through a configurable threshold, spreads the detected edges into soft glowing halos via a horizontal IIR low-pass filter, and tints the halos with a selectable hue from a 6-sector piecewise color wheel. The original video can serve as a dimmed background behind the glow, or the background can be dropped to near-black for a pure neon-on-dark look.

The name is literal — the program turns video contours into neon tubes. The edge detector is a first-order horizontal difference (|current pixel − previous pixel|), not a full Sobel kernel, so it responds primarily to vertical structures in the image where horizontal brightness transitions are sharpest. The IIR glow filter operates entirely within each scan line, producing a rightward bloom that decays exponentially from each detected edge. Where edges are dense, the glow fields overlap additively and the composite can saturate to full brightness.

The hue wheel divides the 360° color circle into six piecewise sectors, each mapping a portion of the Hue pot range to specific U and V offsets around the 512 midpoint. At maximum saturation, these offsets reach ±256 counts, producing vivid spectral colors. A Color toggle switches between this fixed hue and the source video's own chrominance, letting the glow inherit the color of the edge that produced it.

---

## Background

### First-Order Horizontal Gradient

The simplest edge detector computes the absolute difference between adjacent pixels. In Neon, this is the horizontal gradient: |Y[x] − Y[x−1]|. Unlike a Sobel kernel that needs line buffers and 3×3 convolution, the first-order difference requires only a single register to hold the previous pixel value, making it extremely resource-efficient. The tradeoff is that it only detects horizontal transitions — vertical edges in the image. This directional bias is part of the neon aesthetic: horizontal structures in the source produce no glow, while vertical contours light up brightly.

### IIR Glow Spread

An Infinite Impulse Response filter with a single feedback tap creates the glow halo. Each clock cycle, the accumulator decays toward zero by subtracting a right-shifted copy of itself, then adds a right-shifted copy of the thresholded edge signal. The shift amount controls the time constant: shift 1 produces wide, slowly decaying glow (the accumulator retains 50% per sample); shift 4 produces narrow, rapidly decaying glow (retains 93.75% subtracted). Because the filter runs left-to-right along each scan line, the glow always extends to the right of each detected edge, creating the asymmetric bloom characteristic of real CRT phosphor persistence.

### Piecewise Hue Mapping

Rather than storing a full sine/cosine table, Neon divides the hue circle into 6 sectors using the top 3 bits of the Hue pot value (clamped to 0–5). Each sector assigns fixed U and V offset polarities from the saturation control: sector 0 is pure red (V+), sector 1 is yellow-magenta (U−, V+ half), sector 2 is cyan-blue (U− half, V−), and so on around the wheel. The result is a coarse but effective color selector that covers the primary and secondary hues with zero multiplier usage.

### Additive Compositing

The final image is formed by adding the glow luminance to the background luminance, with saturation clamping at 1023. This additive model means glow always brightens the output — it never subtracts from the background. Where multiple edge halos overlap, their luminances sum, creating bright hotspots at edge intersections. The chrominance channel switches abruptly between tube color and background color based on a glow threshold of 64 counts, producing a hard color boundary around each glow halo.

### Background Dimming

The background path offers two modes. In black mode, the background is simply the Bg Level pot value divided by 8, producing a near-black floor with neutral chrominance (U=V=512). In dim video mode, the source luminance is multiplied by the Bg Level pot and divided by 1024, producing a darkened but recognizable version of the input video with its original color intact. The dim video mode is particularly effective for the neon aesthetic — glowing edges floating over a barely visible scene.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ─────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register         (latch Y, U, V; store Y_prev)
│   │     Horizontal gradient:  |Y[x] − Y[x−1]|
│   ├─ 2. Threshold Gate         (soft: max(0, mag−thresh); hard: mag>thresh ? 1023 : 0)
│   │     IIR Glow:  acc = acc − (acc >> shift) + (edge >> shift)
│   ├─ 3. Glow Brightness        (glow_y = glow_val × bright >> 10, clamp 1023)
│   │     Hue Decode:  6-sector hue pot → (U_off, V_off)
│   ├─ 4. Color Select           (fixed hue UV or source UV)
│   │     Background Prepare     (black: bg_level/8; dim: Y × bg_level >> 10)
│   ├─ 5. Composite              (bg_y + tube_y, clamp 1023)
│   │     Invert:  1023 − result
│   │     UV Select:  glow > 64 → tube UV, else bg UV
│   └─ 6–9. Interpolator Mix     (4 clocks, dry/wet crossfade)
│
├── Sync Signals ──────────────────────────────────────────────
│   └─ 9-stage delay pipeline (hsync, vsync, field, Y/U/V for bypass)
│
└── Bypass ────────────────────────────────────────────────────
    └─ Select delayed original or mixed signal via bypass toggle
```

The entire glow effect is produced within a single scan line — there are no line buffers or vertical processing. This means the gradient detector only responds to horizontal brightness transitions (producing glow on vertical image structures). The IIR filter's rightward-only decay creates an asymmetric halo: the left edge of a bright object gets a clean onset while the right side trails off exponentially. The decay rate, controlled by the Glow Size shift amount, determines how far the glow extends before it falls below the visibility threshold.

The chrominance crossover at glow level 64 is an important design detail. Rather than smoothly blending tube and background colors (which would require additional multipliers), the VHDL uses a hard threshold: pixels with glow above 64 receive the tube's hue; pixels below receive the background's color. This creates a visible color boundary that reinforces the neon-tube illusion — real neon tubes have a sharp color edge where the glow fades to darkness.

---

## Parameter Reference

<img src={neon_control_panel} alt="Videomancer front panel with Neon loaded"/>
*Videomancer's front panel with Neon active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Threshold sets the minimum horizontal gradient magnitude required to trigger glow. In soft mode, the threshold is subtracted from the edge magnitude (clamping at zero), so edges just above threshold produce faint glow and strong edges produce bright glow. In hard mode, any edge above threshold produces maximum glow (1023) while edges below produce nothing. Low threshold values make the detector sensitive to subtle textures and noise; high values restrict glow to only the strongest contours in the image.

---

#### Knob 2 — Glow Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Glow Size controls the horizontal spread of the IIR glow filter by selecting the right-shift amount applied to both the decay and input terms. High pot values select shift 1 (wide glow extending many pixels right of each edge); low pot values select shift 4 (narrow glow that decays within a few pixels). The mapping uses four threshold bands at 256-count intervals. Because the IIR operates per-scanline, this parameter only affects horizontal spread — vertical extent is always a single pixel.

---

#### Knob 3 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Bright scales the glow luminance via a 10-bit multiply: glow_y = glow_val × bright >> 10. At zero, the glow is invisible regardless of edge detection. At maximum (1023), the glow reaches nearly the full detected magnitude. This control sets the peak intensity of the neon tubes — how bright they appear above the background. Because the composite is additive, high brightness values can push areas with overlapping glow to full white (1023).

---

#### Knob 4 — Hue
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 120deg |
| Suffix | deg |

Hue selects the glow color from the 6-sector piecewise hue wheel. The top 3 bits of the pot value (clamped to 0–5) index a case statement that generates U and V offsets from the Saturate pot value. Sector 0 produces red-orange, sector 1 yellow-magenta, sector 2 cyan, sector 3 blue-green, sector 4 magenta-pink, and sector 5 warm red. Sweeping the pot traverses the full color circle in six discrete steps.

---

#### Knob 5 — Saturate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Saturate controls the amplitude of the hue-derived U and V chrominance offsets. The 10-bit pot value is right-shifted by 1 to produce a half-range scaling factor. Each hue sector applies this factor as positive or negative offsets to the U=512 and V=512 midpoints. At zero, both offsets are zero and the glow is achromatic (white). At maximum, the offsets reach ±512 counts (clamped), producing fully saturated spectral color. This lets you create either white neon tubes or richly colored ones.

---

#### Knob 6 — Bg Level
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 6% |
| Suffix | % |

Bg Level controls the background brightness in both modes. In black background mode, the pot value is right-shifted by 3, producing a dim floor between 0 and 127 counts with neutral (gray) chrominance. In dim video mode, the pot value multiplies the source luminance (Y × bg_level >> 10), scaling the background from completely black (pot at 0) to nearly full brightness (pot at 1023). This controls how visible the source scene is behind the neon glow.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color** | Fixed | Source |
| **8 — Bg Style** | Black | Dim Vid |
| **9 — Edge** | Soft | Hard |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent aspects of the neon rendering. Color selects between the hue-pot-driven tube color and the source video's own chrominance. Bg Style chooses the background treatment. Edge switches the threshold gate between soft (proportional) and hard (binary) response. Invert flips the final luminance. Bypass routes the delayed original signal directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix controls the interpolator crossfade between the dry (original) and wet (processed) signals. At 0, the output is entirely the original video. At 1023, the output is entirely the neon-processed signal. The interpolator operates independently on all three YUV channels with 4-clock latency.

---

## Guided Exercises

These exercises build from basic edge glow through color and background styling to full neon-sign compositions, progressively engaging the IIR spread, hue mapping, and composite controls.

### Exercise 1: Basic Neon Tubes

<img src={neon_exercise1_result} alt="Basic Neon Tubes result"/>
*Basic Neon Tubes — simulated result across source images.*
**Source**: A high-contrast graphic or text overlay — sharp black-on-white lettering, geometric shapes, or a title card with clean vertical edges.

**Objective**: Produce clean, bright neon tube outlines from hard-edged source material, learning how Threshold and Glow Size interact to shape the halo.

1. Start with default settings. Observe faint glow on edges of the source.
2. Lower Threshold to ~20% to detect more edges. Glow becomes more pervasive.
3. Set Edge to Hard. Observe how all edges become uniform-intensity tubes.
4. Increase Glow Size to ~75%. The halos spread further right from each edge.
5. Increase Bright to full. The tubes become intensely luminous.
6. Sweep Hue slowly through its range. Watch the tube color cycle through six sectors.

**Key concepts**: First-order horizontal gradient detects vertical structures, hard threshold creates uniform tubes, IIR shift controls bloom width, 6-sector hue wheel

---

### Exercise 2: Neon Sign on a Dark Scene

<img src={neon_exercise2_result} alt="Neon Sign on a Dark Scene result"/>
*Neon Sign on a Dark Scene — simulated result across source images.*
**Source**: A moderately detailed camera feed — a face, a room interior, or an outdoor scene with varied luminance.

**Objective**: Create the classic neon-sign-over-dark-wall look by combining dim video background with colored edge glow.

1. Set Bg Style to Dim Vid. The source video appears behind the glow.
2. Lower Bg Level to ~10%. The background dims to barely visible.
3. Set Threshold to ~40% to limit glow to the strongest contours.
4. Use soft Edge mode — edges glow proportionally to their strength.
5. Set Hue to a warm color (sector 0 or 5) and Saturate to ~75%.
6. Adjust Glow Size to taste. Wider glow creates a more atmospheric haze.

**Key concepts**: Dim video background preserves scene context, soft threshold reveals edge hierarchy, additive composite brightens over the dimmed background

---

### Exercise 3: Source-Colored Glow with Invert

<img src={neon_exercise3_result} alt="Source-Colored Glow with Invert result"/>
*Source-Colored Glow with Invert — simulated result across source images.*
**Source**: A colorful, high-contrast feed — flowers, graffiti, a colorful textile, or a saturated video clip.

**Objective**: Use source-colored glow and invert to create an x-ray or blueprint negative of the scene's color edges.

1. Set Color to Source. The glow now inherits the chrominance of the source pixel at each edge.
2. Set Threshold low (~15%) and Edge to Soft for maximum edge detail.
3. Enable Invert. The bright glow inverts to dark lines on a bright background.
4. Set Bg Style to Dim Vid and Bg Level to ~80%. The inverted result shows bright background with dark edge traces.
5. Lower Mix to ~60% to blend with the original, creating a partially processed look.
6. Compare with Invert off — observe the complementary color relationships.

**Key concepts**: Source color mode preserves original chrominance in glow, invert flips luminance polarity, mix blending creates partial effect

---


## Tips

- **Start with high-contrast sources**: The first-order gradient detector responds to horizontal brightness transitions. Sharp vertical edges in the source produce the brightest glow; soft gradients and horizontal structures produce little or nothing.
- **Use Hard edge mode for the classic neon look**: Hard threshold creates uniform-intensity tubes that closely mimic real neon signage. Soft mode is better for revealing textural detail.
- **Glow Size shift is coarse**: There are only 4 settings (shift 1–4), each doubling or halving the bloom width. Fine-tune the apparent glow width by adjusting Bright and Threshold instead.
- **Bg Level in black mode stays dim**: The pot value is divided by 8 in black mode, so even at full the background only reaches ~127 counts. For a brighter background, switch to Dim Vid mode.
- **Source color mode ignores Hue and Saturate**: When Color is set to Source, the tube U/V come directly from the input — the Hue and Saturate pots do nothing. Adjust them only in Fixed mode.
- **IIR glow resets at line boundaries**: The glow accumulator is per-scan-line with no vertical carry, so the glow effect is purely horizontal. This creates scan-line-independent results with no frame-to-frame memory.
- **Invert creates blueprint effects**: Combining invert with dim video background and source color produces dark edge traces on a bright field — an aesthetic closer to architectural blueprints than neon signs.
- **Layer after threshold programs**: Running Neon after a hard-keyer or posterizer program produces exceptionally clean neon tubes because the input already has strong, well-defined edges.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Composite** | Pixel combination by summing luminance values, with clamping at maximum (1023) to prevent overflow. |
| **BT.601** | ITU-R BT.601 standard defining the YUV color encoding used in the Videomancer video pipeline. |
| **Chrominance** | The color difference components (U and V) of a YUV signal, encoding hue and saturation around the (512, 512) neutral midpoint. |
| **First-Order Difference** | Edge detection by computing |pixel[x] − pixel[x−1]|, the simplest discrete derivative. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip executing the video processing pipeline at 74.25 MHz. |
| **IIR** | Infinite Impulse Response; a feedback filter whose output depends on both the current input and its own previous output, creating exponentially decaying response. |
| **Interpolator** | A linear crossfade module that blends two 10-bit values based on a mix parameter over 4 clock cycles. |
| **Luminance** | The brightness component (Y) of a YUV signal, range 0–1023 in 10-bit representation. |
| **Piecewise Hue Mapping** | Dividing the 360° color circle into discrete sectors, each with fixed U/V offset directions, rather than computing continuous trigonometric functions. |
| **Pipeline** | Sequential processing stages where each stage's output feeds the next on every clock cycle. |
| **YUV** | Color encoding separating luminance (Y) from chrominance (U, V), the native format of the Videomancer video pipeline. |
