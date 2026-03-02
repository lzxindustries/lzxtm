---
draft: true
sidebar_position: 226
slug: /instruments/videomancer/quilt
title: "Quilt"
image: /img/instruments/videomancer/quilt/quilt_hero.png
description: "Every image carries a grid — the rows and columns of pixels that compose it."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import quilt_hero from '/img/instruments/videomancer/quilt/quilt_hero.png';
import quilt_control_panel from '/img/instruments/videomancer/quilt/quilt_control_panel.png';
import quilt_exercise1_result from '/img/instruments/videomancer/quilt/quilt_exercise1_result.png';
import quilt_exercise2_result from '/img/instruments/videomancer/quilt/quilt_exercise2_result.png';
import quilt_exercise3_result from '/img/instruments/videomancer/quilt/quilt_exercise3_result.png';
import quilt_source1_kodim15 from '/img/instruments/videomancer/quilt/quilt_source1_kodim15.png';
import quilt_source2_kodim03 from '/img/instruments/videomancer/quilt/quilt_source2_kodim03.png';
import quilt_source3_kodim13_bw from '/img/instruments/videomancer/quilt/quilt_source3_kodim13_bw.png';

# Quilt

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: quilt_source1_kodim15, after: quilt_hero },
    { label: "Kodim03", before: quilt_source2_kodim03, after: quilt_hero },
    { label: "Kodim13 B&W", before: quilt_source3_kodim13_bw, after: quilt_hero },
  ]}
/>
*Quilt dividing a video field into patchwork blocks with per-block pattern overlays, LFSR color jitter, and configurable stitch borders.*

---

## Overview

Every image carries a grid — the rows and columns of pixels that compose it. Quilt makes that grid visible and decorative, dividing the video frame into square blocks and stamping each one with a pattern selected by hashing its grid position. The result looks like a digital patchwork: some tiles are solid tints, some carry horizontal stripes, some are checkerboards, and some bear diagonal lines. Thin "stitch" lines mark the block boundaries like thread running between fabric patches.

The name comes straight from the visual effect — the output looks like a quilt assembled from swatches of the source image, each one slightly recolored and decorated with a repeating motif. The program operates entirely in the spatial domain with no BRAM: a position counter, modular arithmetic for intra-block coordinates, an XOR hash for pattern assignment, an LFSR for color jitter, and a border threshold comparator. Three `interpolator_u` instances handle the wet/dry crossfade.

At low Block Size values the patches are large (64 pixels), giving each tile visible internal detail from the source. As Block Size increases the patches shrink to 32 and then 16 pixels, abstracting the image into a dense mosaic. Pattern Intensity controls how strongly the overlaid motifs brighten or darken the source, while Color Scatter injects per-block chroma variation drawn from a 16-bit LFSR noise source. The stitch borders can be turned off entirely or dialed from gossamer-thin to boldly visible.

---

## Background

### Sample-and-Hold Grid Division

Quilt divides the frame using power-of-two block sizes selected by the Block Size potentiometer. The three available sizes — 16, 32, and 64 pixels — are chosen via simple threshold comparisons on the 10-bit register value. Intra-block coordinates are computed by masking the pixel counter with the block mask (0x00F, 0x01F, or 0x03F), producing a repeating local position that resets at each block boundary. Grid column and row indices are obtained by right-shifting the pixel counter by the corresponding block shift (4, 5, or 6 bits).

### Position Hashing and Pattern Selection

Each block receives a pattern via a hash of its grid coordinates. The hash XORs the column index with the row index and then with a nibble-swapped version of those indices, producing an 8-bit value whose lower bits select among four patterns: solid tint, horizontal stripe, checker, or diagonal stripe. In 2-pattern mode (Pattern Mode toggle) only the lowest hash bit is used, reducing selection to two patterns. This creates a deterministic but visually complex mosaic — the same grid position always gets the same pattern, but the pattern distribution appears pseudo-random.

### Border Stitching

Block boundaries are rendered as thin lines whose width is controlled by the Border Width potentiometer (mapped to a 1–4 pixel threshold). A pixel is "on border" when either its local X or local Y coordinate within the block falls below the threshold. Border pixels receive a flat luma value set by the Stitch Brightness control, with chroma forced to the neutral midpoint (512), producing a monochrome stitch line regardless of the source content beneath.

### LFSR Color Jitter

A 16-bit LFSR runs continuously, generating a pseudo-random bit stream. For each pixel outside a border, the lower 8 bits of the LFSR output are AND-masked with a scatter amount derived from the Color Scatter potentiometer (scaled 0–63). The resulting signed jitter is added to U and subtracted from V, producing complementary chroma shifts. Additionally, hash bit 3 selects whether a per-block tint offset is applied to U or V, creating warm/cool block-to-block variation.

### Animation Mode

When the Animate toggle is active, the LFSR seed is reloaded at each vertical sync from the current LFSR state XORed with a fixed constant. This causes the color jitter pattern to evolve frame-to-frame, producing a subtle shimmer across the patchwork. With Animate off, the LFSR still runs but its seed is never reloaded, so the jitter pattern is static and repeatable.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Timing Generator ──────────────────────────────────────────
│   └─ video_timing_generator → h_count, v_count, avid
│
├── LFSR16 ─────────────────────────────────────────────────────
│   └─ 16-bit linear feedback shift register (color jitter)
│       └─ seed reload on vsync (if Animate enabled)
│
├── Parameter Pre-Registration ─────────────────────────────────
│   ├─ block_size → block_mask (0x00F/0x01F/0x03F), block_shift (4/5/6)
│   ├─ pattern_int → intensity (>>3, range 0–127)
│   ├─ border_width → border_thresh (1/2/3/4)
│   ├─ stitch_bright → stitch_val (direct passthrough)
│   └─ color_scatter → scatter_amt (>>4, range 0–63)
│
├── Stage 1: Grid Position Compute ─────────────────────────────
│   ├─ Register Y, U, V
│   ├─ h_offset = h_count (+ half-block if grid_style=offset & odd row)
│   ├─ local_x = h_offset AND block_mask
│   ├─ local_y = v_count AND block_mask
│   ├─ grid_col = h_offset >> block_shift
│   └─ grid_row = v_count >> block_shift
│
├── Stage 2: Pattern Select ────────────────────────────────────
│   ├─ hash = (col XOR row) XOR (row[3:0] & col[7:4])
│   ├─ pattern_sel = hash[1:0] (or hash[0] in 2-pattern mode)
│   └─ Pipeline Y, U, V, local coords
│
├── Stage 3: Pattern Apply + Border Detect ─────────────────────
│   ├─ Pattern value from selection:
│   │   ├─ 00: solid tint (hash bit 2)
│   │   ├─ 01: horizontal stripe (local_x bit 2)
│   │   ├─ 10: checker (local_x[3] XOR local_y[3])
│   │   └─ 11: diagonal (double-XOR of bits 3 and 2)
│   └─ Border = (local_x < thresh) OR (local_y < thresh)
│
├── Stage 4: Compose + Color Jitter ────────────────────────────
│   ├─ If border: Y=stitch_val, U=V=512
│   ├─ If pattern ON: Y += intensity; if OFF: Y -= intensity
│   ├─ LFSR jitter: U += jitter, V -= jitter
│   ├─ Hash tint: hash[3] ? U+=intensity/4 : V+=intensity/4
│   └─ Clamp all channels [0, 1023]
│
├── Mix (3× interpolator_u, 4 clocks) ─────────────────────────
│   └─ lerp(dry, wet, mix_amount) per channel
│
└── Output ─────────────────────────────────────────────────────
    └─ bypass ? delayed_input : mixed_output
```

The critical interaction is between the position hash and the LFSR jitter. The hash deterministically assigns each block its pattern type and its warm/cool tint direction (via bit 3), while the LFSR adds stochastic variation within the scatter range. Together they create a patchwork that is structurally ordered — the same block always gets the same pattern — but chromatically varied in a way that depends on the noise state. The offset-row grid style shifts odd rows by half a block width, breaking the vertical alignment and producing a brick-like layout.

---

## Parameter Reference

<img src={quilt_control_panel} alt="Videomancer front panel with Quilt loaded"/>
*Videomancer's front panel with Quilt active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Block Sz
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the patchwork block size. The 10-bit register value is divided into three bands: values above 682 select 16-pixel blocks (fine mosaic), values 342–682 select 32-pixel blocks (medium), and values 0–341 select 64-pixel blocks (coarse). This is a discrete three-way switch, not a continuous control. Smaller blocks abstract the source image more aggressively, while larger blocks preserve more internal detail within each tile.

---

#### Knob 2 — Variety
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the pattern overlay intensity — how strongly each block's assigned motif brightens or darkens the source luma. The raw 10-bit value is right-shifted by 3 to produce a working range of 0–127. At zero, blocks carry no visible pattern and only the color jitter distinguishes them. At maximum, the stripe/checker/diagonal patterns create high-contrast overlays that dominate the source image content.

---

#### Knob 3 — Border Th
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the stitch border width between blocks. The register value maps to a 1–4 pixel threshold: values 0–256 give a 1-pixel hairline, 257–512 give 2 pixels, 513–768 give 3, and above 768 give 4 pixels. These thin lines are drawn wherever the pixel's local position within its block falls below the threshold on either axis, producing a grid of horizontal and vertical stitch marks.

---

#### Knob 4 — Stitch Vs
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the brightness of the stitch border lines. The 10-bit register value passes directly to the border compositor as the luma value for stitch pixels. At 0 the borders are black; at 1023 they are peak white. Stitch pixels always have neutral chroma (U = V = 512), so this control determines only their luminance. Combine with border width to create anything from faint dividing lines to bold white grids.

---

#### Knob 5 — Color Rch
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls per-block color scatter — the amount of LFSR-driven chroma variation applied to non-border pixels. The raw value is right-shifted by 4 to produce a 0–63 scatter amplitude. At zero, blocks retain the source chrominance unmodified (aside from pattern luma changes). As scatter increases, each pixel's U and V channels receive complementary random offsets, and an additional hash-based tint pushes alternating blocks toward warm or cool hues.

---

#### Knob 6 — Padding
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

This control is declared in the TOML configuration as "Padding" but is not connected to any signal in the VHDL processing pipeline. Adjusting it has no effect on the output image. It is reserved for possible future expansion.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Log Cab | Star |
| **8 — Palette** | Warm | Cool |
| **9 — Stitch** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control structural and behavioral options. Grid Style selects between aligned square blocks and offset (brick-pattern) rows. Pattern Mode switches between a four-pattern or two-pattern repertoire. Animate enables per-frame LFSR seed reloading for evolving jitter. Toggle 10 is reserved and has no effect. Bypass passes the input through unprocessed.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed and original signals. At 0 the output is entirely dry (original input); at 1023 it is entirely wet (full quilt effect). The crossfade is handled by three parallel `interpolator_u` instances operating on Y, U, and V independently, each taking 4 clock cycles. Intermediate positions create a transparent overlay where the patchwork pattern is blended over the source.

---

## Guided Exercises

These exercises explore three distinct aspects of the Quilt effect — from coarse structural tiling to fine-grained color scatter and animated texture evolution.

### Exercise 1: Bold Patchwork Grid

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: quilt_source1_kodim15, after: quilt_exercise1_result },
    { label: "Kodim03", before: quilt_source2_kodim03, after: quilt_exercise1_result },
    { label: "Kodim13 B&W", before: quilt_source3_kodim13_bw, after: quilt_exercise1_result },
  ]}
/>
*Bold Patchwork Grid — simulated result across source images.*
**Source**: A scene with large areas of varied brightness and moderate color — a landscape or portrait with distinct light and dark regions works well.

**Objective**: Create a coarse patchwork with clearly visible block patterns, bold stitch lines, and minimal color variation — a digital quilt with strong graphic structure.

1. Set Block Sz to 0% for 64-pixel blocks
2. Turn Variety to 50% for moderate pattern contrast
3. Set Border Th to 75% for 3-pixel stitch lines
4. Set Stitch Vs to 100% for bright white stitches
5. Set Color Rch to 0% for no color scatter
6. Leave Padding at 50% (no effect)
7. Switch Pattern to "Log Cab" for aligned square grid
8. Switch Palette to "Warm" for 4-pattern mode
9. Switch Stitch to "Off" for static jitter
10. Leave Animate at default
11. Confirm Bypass is Off
12. Set Mix to 100% for full effect

**Key concepts**: Large blocks preserve source detail within each tile while the four pattern types create visible textural variation. The bold stitch lines reinforce the patchwork metaphor.

---

### Exercise 2: Fine Mosaic with Color Scatter

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: quilt_source1_kodim15, after: quilt_exercise2_result },
    { label: "Kodim03", before: quilt_source2_kodim03, after: quilt_exercise2_result },
    { label: "Kodim13 B&W", before: quilt_source3_kodim13_bw, after: quilt_exercise2_result },
  ]}
/>
*Fine Mosaic with Color Scatter — simulated result across source images.*
**Source**: A colorful, high-contrast image — abstract graphics, multicolored patterns, or a brightly lit scene with saturated objects.

**Objective**: Create a dense, jewel-like mosaic with small blocks and strong per-block color variation. Each tile should appear as a distinct hue swatch.

1. Set Block Sz to 100% for 16-pixel blocks
2. Turn Variety to 30% for subtle pattern overlays
3. Set Border Th to 25% for thin 1-pixel stitch lines
4. Set Stitch Vs to 60% for mid-gray stitches
5. Set Color Rch to 85% for strong color scatter
6. Leave Padding at 50% (no effect)
7. Switch Pattern to "Star" for offset brick-pattern grid
8. Switch Palette to "Cool" for 2-pattern mode
9. Switch Stitch to "Off" for static color distribution
10. Leave Animate at default
11. Confirm Bypass is Off
12. Set Mix to 80% for slight source bleed-through

**Key concepts**: Small blocks with high color scatter produce a stained-glass mosaic. The 2-pattern mode (via Palette toggle) creates a calmer distribution, letting the LFSR chroma jitter provide the visual complexity.

---

### Exercise 3: Animated Shimmer Quilt

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: quilt_source1_kodim15, after: quilt_exercise3_result },
    { label: "Kodim03", before: quilt_source2_kodim03, after: quilt_exercise3_result },
    { label: "Kodim13 B&W", before: quilt_source3_kodim13_bw, after: quilt_exercise3_result },
  ]}
/>
*Animated Shimmer Quilt — simulated result across source images.*
**Source**: A slowly moving video source — a gently shifting abstract pattern, a slow camera pan, or a face with subtle expression changes.

**Objective**: Combine coarse patchwork structure with the Animate mode to create a quilt whose per-block coloring shifts and shimmers over time.

1. Set Block Sz to 40% for 32-pixel blocks
2. Turn Variety to 60% for visible but not dominant patterns
3. Set Border Th to 50% for 2-pixel stitch borders
4. Set Stitch Vs to 80% for bright stitches
5. Set Color Rch to 50% for moderate color scatter
6. Leave Padding at 50% (no effect)
7. Switch Pattern to "Log Cab" for aligned grid
8. Switch Palette to "Warm" for 4-pattern mode
9. Switch Stitch to "On" to enable animation
10. Leave Animate at default
11. Confirm Bypass is Off
12. Set Mix to 100% for full effect

**Key concepts**: The Animate toggle (Stitch in TOML) reloads the LFSR seed each frame, causing the color scatter pattern to evolve. Against the structurally stable grid, this creates a quilt that "breathes" — the block boundaries and patterns remain fixed while the per-tile coloring drifts.

---


## Tips

- **Block size is discrete**: Unlike most controls, Block Sz jumps between three sizes (16/32/64) at fixed thresholds rather than sweeping continuously.
- **Pot 6 does nothing**: The Padding knob is wired in the TOML but unconnected in hardware. Save it for live-performance misdirection.
- **Toggle labels differ from VHDL**: Pattern (Tog 7) controls grid style, Palette (Tog 8) controls pattern count, and Stitch (Tog 9) controls animation — not what the labels suggest.
- **Color scatter is complementary**: The LFSR jitter is added to U and subtracted from V simultaneously, so blocks shift along the blue-yellow/red-cyan axis rather than becoming arbitrarily colored.
- **Hash tinting is per-block**: The warm/cool offset is determined by hash bit 3, so it's consistent within each block — neighboring blocks may have opposite tint directions.
- **Borders override everything**: A pixel on a stitch border loses all source content and pattern overlay — it becomes a flat monochrome line at the stitch brightness value.
- **2-pattern mode calms the grid**: Switching Palette to offset (2-pattern mode) removes the checker and diagonal types, producing a more textile-like result.

---
