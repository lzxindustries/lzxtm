---
draft: true
sidebar_position: 213
slug: /instruments/videomancer/receipt
title: "Receipt"
image: /img/instruments/videomancer/receipt/receipt_hero.png
---

import receipt_before_after from '/img/instruments/videomancer/receipt/receipt_before_after.png';
import receipt_control_panel from '/img/instruments/videomancer/receipt/receipt_control_panel.png';
import receipt_exercise1_result from '/img/instruments/videomancer/receipt/receipt_exercise1_result.png';
import receipt_exercise2_result from '/img/instruments/videomancer/receipt/receipt_exercise2_result.png';
import receipt_exercise3_result from '/img/instruments/videomancer/receipt/receipt_exercise3_result.png';
import receipt_hero from '/img/instruments/videomancer/receipt/receipt_hero.png';
import receipt_source1_kodim02 from '/img/instruments/videomancer/receipt/receipt_source1_kodim02.png';
import receipt_source2_kodim07 from '/img/instruments/videomancer/receipt/receipt_source2_kodim07.png';
import receipt_source3_kodim01_bw from '/img/instruments/videomancer/receipt/receipt_source3_kodim01_bw.png';

# Receipt

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={receipt_hero} alt="Receipt hero image"/>
*Receipt reducing a live video stream to dithered thermal printer output with visible block structure, head banding, and warm paper tint.*
<img src={receipt_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Receipt applied.*

---

## Overview

Before digital snapshots were instant, video printers were the only way to get a physical copy of a single video frame. Devices like the Sony UP-5600MD and Mitsubishi CP-D70DW captured one field, quantized it to a handful of tonal levels, and burned it onto thermal paper line by line — a process that took several seconds and produced images with a distinctive low-resolution, high-contrast, warm-toned appearance. Receipt recreates that entire pipeline in real time.

The program chains six processing stages: spatial decimation (sample-and-hold block quantization), level quantization with selectable dithering, thermal head banding, paper tint blending, ink density control, and a top-to-bottom print reveal animation. The name evokes the ubiquitous thermal receipt — the most common surviving example of thermal printing technology, with its coarse resolution, fading ink, and warm off-white paper stock.

There is no bypass toggle on this program. Toggle 11 selects between Thermal and Dot Matrix print modes. The Mix fader is the only wet/dry control — fully counter-clockwise for dry (original), fully clockwise for wet (full effect).

---

## Background

### What Is Sample-and-Hold Quantization?

Receipt's Resolution control implements **sample-and-hold** spatial decimation. At the top-left pixel of each block, the input YUV values are latched into holding registers. Every subsequent pixel within that block outputs the same held values, creating uniform rectangular blocks of color. Early video printers did this physically — the thermal head had a fixed number of heating elements, each spanning several source pixels. Resolution offers four block sizes: 4×4, 8×8, 16×16, and 32×32 pixels, matching the coarseness of real printer resolution modes.

### What Is Ordered Dithering?

Before quantizing a signal to fewer levels, you can add a small, structured offset to each pixel. If the pattern is carefully chosen, the quantization errors average out over a local neighborhood, creating the illusion of intermediate tones from a distance. Receipt uses a **4×4 Bayer matrix** for ordered dithering — the same algorithm used in early computer printing. The alternative Pattern mode substitutes a simple checkerboard hash, producing a coarser, more artificial stipple. Both methods are applied before level quantization, just as a real printer would dither before committing ink to paper.

### What Is Thermal Head Banding?

Thermal printers drag a row of heating elements across the paper. Mechanical imperfections — uneven pressure, temperature drift, debris on the head — cause periodic brightness variations every few scan lines. Receipt simulates this with a periodic horizontal stripe modulation: every eighth line, brightness is reduced proportionally to the Banding parameter. In Dot Matrix mode, the banding is sharper and more frequent (every fourth line), mimicking the harsher mechanical artifacts of impact dot-matrix printers versus the smoother thermal transfer process.

### What Is Paper Tint?

Thermal paper is not white — it has a warm, cream-to-sepia cast that becomes more visible in lighter areas. Receipt blends a fixed paper color (Y=950, U=480, V=540 — a warm cream) into the processed image, weighted by pixel brightness. Brighter pixels receive more paper tint; darker pixels remain relatively unaffected. This is physically accurate: thermal printing works by darkening the paper, so the lightest areas are the closest to raw paper stock.

### What Is Print Animation?

Real thermal printers reveal the image line by line as the print head traverses the page. Receipt simulates this with a vertical cursor that advances down the frame at a speed controlled by Print Spd. Lines below the cursor display the paper color instead of processed video. The reveal speed is quantized into five tiers: very slow (1 line every 8 frames), slow (1 line every 4 frames), medium (1 line per frame), fast (2 lines per frame), and very fast (4 lines per frame). The animation resets on each field.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 0: Input Register + Sample-and-Hold ──────────────────
│   ├─ Parameter decode (resolution, levels, banding, tint, ink, speed)
│   ├─ Block size select (4×4 / 8×8 / 16×16 / 32×32)
│   ├─ Sample-and-hold: latch YUV at top-left of each block
│   ├─ Grid edge detection (block boundary pixels)
│   └─ Print animation cursor compare (v_count vs print_line)
│
├── Stage 1: Mono + Level Quantization + Dither ────────────────
│   ├─ Mono mode: clamp U,V to 512
│   ├─ Dither threshold (Bayer 4×4 ordered or checkerboard pattern)
│   └─ Level quantize: truncate to 4/8/16/32 levels with dither offset
│
├── Stage 2: Banding + Tint + Density + Grid + Animation ──────
│   ├─ Thermal banding: periodic scanline darkening (every 8th or 4th line)
│   ├─ Ink density: contrast curve around mid-point (512)
│   ├─ Paper tint: blend lighter pixels toward paper color
│   ├─ Dot grid: darken block boundary pixels by 50%
│   └─ Print animation: replace below-cursor pixels with paper color
│
├── Mix Stage (4 clk) ──────────────────────────────────────────
│   └─ 3× interpolator_u: crossfade dry ↔ wet per Mix fader
│
└── Sync Delay Pipeline ────────────────────────────────────────
    └─ 8-clock shift register for hsync, vsync, field, Y, U, V
```

The critical ordering is: decimation happens *before* level quantization, so the quantizer operates on already-uniform block values. Dithering sits between decimation and quantization, adding spatial variation within uniform blocks to create tonal texture at the block level. Banding, paper tint, and ink density are applied *after* quantization, modifying the final printed appearance. The print animation override is last — it simply replaces everything below the cursor with paper color, regardless of processing state.

---

## Parameter Reference

<img src={receipt_control_panel} alt="Videomancer front panel with Receipt loaded"/>
*Videomancer's front panel with Receipt active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Resolution
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 1 |

Selects the spatial block size for sample-and-hold decimation. This is a four-step selector: 4×4, 8×8, 16×16, or 32×32 pixels per block. At 4×4, the image retains reasonable detail with a subtle mosaic quality. At 32×32, the image becomes extremely coarse — just a handful of large colored rectangles. The block boundaries also define the dither matrix tiling and the dot grid overlay positions.

---

#### Knob 2 — Levels
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 2 |

Selects the number of quantization levels per channel. Another four-step selector: 4, 8, 16, or 32 levels. At 4 levels, the image is reduced to stark posterized bands — pure thermal receipt territory. At 32 levels, the tonal staircase is subtle enough to be nearly invisible without dithering. Level quantization is applied equally to Y, U, and V channels (unless Mono mode is active, which fixes U and V to neutral).

---

#### Knob 3 — Banding
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the intensity of periodic horizontal stripe artifacts simulating thermal print head banding. At zero, the image is clean. As Banding increases, every eighth scan line darkens noticeably, creating the characteristic horizontal streaks of a worn print head. In Dot Matrix mode (Thermal toggle off), the banding pattern is sharper and affects every fourth line, mimicking the coarser mechanical artifacts of impact printers. The visual effect is a subtle horizontal texture that adds physical plausibility to the printed look.

---

#### Knob 4 — Paper Tint
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls how strongly the warm paper stock color bleeds into lighter areas of the image. At zero, the processed image retains its original color balance. As Paper Tint increases, bright areas shift toward a warm cream (Y=950, U=480, V=540), simulating aged thermal paper. The blending is luminance-weighted — darker pixels are less affected, just as actual thermal ink coverage masks the underlying paper color. This is one of the most visually distinctive controls for achieving the thermal receipt aesthetic.

---

#### Knob 5 — Ink Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls ink density as a contrast curve centered on mid-point (512). Above 50%, contrast is boosted — bright pixels get brighter and dark pixels get darker, simulating heavily inked thermal transfer. Below 50%, contrast is compressed toward mid-gray, simulating a faded or depleted ink ribbon. The effect interacts with level quantization: high density with few levels produces hard graphic blocks, while low density with many levels produces a washed-out, ghostly print.

---

#### Knob 6 — Print Spd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls how fast the print animation cursor advances down the frame. The speed is quantized into five tiers based on the top three bits: very slow (1 line per 8 frames), slow (1 line per 4 frames), medium (1 line per frame), fast (2 lines per frame), and very fast (4 lines per frame). At the slowest setting, a full HD frame takes about 144 seconds to fully reveal — roughly matching the pace of a real thermal printer on high-quality mode. Only active when Print Anim (Toggle 10) is enabled.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color Mode** | Color | Mono |
| **8 — Dither** | Ordered | Pattern |
| **9 — Dot Grid** | Off | On |
| **10 — Print Anim** | Off | On |
| **11 — Thermal** | Dot Matrix | Thermal |

The five toggles operate independently. Color Mode (Toggle 7) affects the color pipeline. Dither (Toggle 8) selects the dither algorithm. Dot Grid (Toggle 9) enables a visual block boundary overlay. Print Anim (Toggle 10) enables or disables the animation cursor. Thermal (Toggle 11) switches between smooth thermal transfer and hard-edged dot matrix appearance, affecting both the banding pattern and the overall texture quality. There is no bypass toggle — use the Mix fader for wet/dry blending.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input signal and the processed printer output. Fully left (0) passes the original signal unmodified. Fully right (1023) outputs the full printer effect. Intermediate positions blend proportionally via the interpolator. This is the *only* dry/wet control — there is no bypass toggle on this program.

---

## Guided Exercises

These exercises progress from basic resolution reduction to full thermal printer simulation, building up the processing chain layer by layer.

### Exercise 1: Thermal Receipt

<img src={receipt_exercise1_result} alt="Thermal Receipt result"/>
*Thermal Receipt — simulated result across source images.*
**Source**: A live camera feed or recorded footage with varied tonal range — faces, text, everyday objects.

**Objective**: Create a convincing thermal receipt print using resolution reduction, level quantization, and paper tint.

1. **Set block size**: Turn Resolution to 8×8 for a classic thermal printer resolution.
2. **Reduce levels**: Set Levels to 8 for visible posterization without total abstraction.
3. **Add dithering**: Keep Dither on Ordered for clean stipple patterns.
4. **Paper color**: Increase Paper Tint to about 60%. Watch lighter areas warm up toward cream.
5. **Go mono**: Switch Color Mode to Mono. The image becomes a sepia-toned thermal print.
6. **Add banding**: Increase Banding to about 40%. Horizontal streaks appear every few lines.

**Key concepts**: Sample-and-hold decimation creates uniform blocks, level quantization with dithering simulates halftone printing, paper tint adds physical realism to the thermal paper look

---

### Exercise 2: Dot Matrix Banner

<img src={receipt_exercise2_result} alt="Dot Matrix Banner result"/>
*Dot Matrix Banner — simulated result across source images.*
**Source**: High-contrast graphics, text overlays, or pattern generator output.

**Objective**: Create a dot-matrix printer look with visible pixel grid and hard-edged banding.

1. **Coarse resolution**: Set Resolution to 16×16 for large visible blocks.
2. **Few levels**: Set Levels to 4 for stark posterization.
3. **Enable grid**: Turn Dot Grid on. Watch the cell boundaries appear.
4. **Dot matrix mode**: Switch Thermal to Dot Matrix. Banding becomes sharper.
5. **Pattern dither**: Switch Dither to Pattern for checkerboard stipple.
6. **High contrast**: Push Ink Density above 75% for bold, saturated blocks.
7. **Color output**: Keep Color Mode on Color to see the reduced-palette effect.

**Key concepts**: Dot grid overlay adds mechanical structure, dot matrix mode produces sharper banding than thermal, pattern dithering creates binary stipple textures

---

### Exercise 3: Animated Print Reveal

<img src={receipt_exercise3_result} alt="Animated Print Reveal result"/>
*Animated Print Reveal — simulated result across source images.*
**Source**: A static or slowly changing source — a held frame, still image, or slow dissolve.

**Objective**: Use the print animation to create a dramatic top-to-bottom reveal effect.

1. **Set up the print look**: Resolution 8×8, Levels 16, Banding ~30%, Paper Tint ~50%, Ink Density ~70%.
2. **Enable animation**: Switch Print Anim to On. The output shows paper color everywhere.
3. **Slow reveal**: Set Print Spd to minimum. Watch the image slowly appear from the top.
4. **Speed variation**: Sweep Print Spd during the reveal to change the printing pace.
5. **Reset**: Each new field restarts the animation cursor. With a static source, you get a repeated print cycle.
6. **Layer effects**: Try combining the animation with mono mode and strong paper tint for maximum thermal printer realism.

**Key concepts**: Print animation replaces below-cursor pixels with paper color, speed is quantized into five tiers, the cursor resets every field for repeating reveals

---


## Tips

- **No bypass toggle**: Unlike most programs, Receipt has no bypass switch. Use the Mix fader fully counter-clockwise for the original signal, or blend wet/dry at any intermediate position.
- **Resolution sets the foundation**: The block size chosen with Resolution determines the scale of every subsequent effect — dithering, grid overlay, and the overall coarseness of the print.
- **Dither first, then judge levels**: Enable dithering before reducing Levels, because dithering smooths the quantization boundaries and changes the visual character of level reduction significantly.
- **Paper tint needs brightness**: Paper tint only affects lighter areas. If your source is very dark or Ink Density is very high, you may not see much tint effect. Reduce Ink Density or choose a brighter source.
- **Thermal vs Dot Matrix is subtle**: The mode primarily changes banding frequency and edge character. For maximum mode difference, use moderate Banding values where the pattern is visible but not overwhelming.
- **Feedback loops**: Route the output back to the input for recursive printing — each pass further reduces resolution and quantizes levels, producing increasingly abstracted prints.
- **Animate for performance**: The print reveal animation is a powerful live performance tool. Set Print Spd to medium and use a static source for a dramatic, slow reveal.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bayer Matrix** | A fixed threshold pattern used for ordered dithering; distributes quantization error in a regular grid to simulate additional tonal levels. |
| **BRAM** | Block RAM; dedicated memory in the FPGA, not used by this program (zero BRAM design). |
| **Decimation** | Discarding spatial samples to reduce resolution; Receipt uses sample-and-hold, latching one pixel per block. |
| **Dithering** | Adding a structured noise pattern before quantization to break up banding and simulate intermediate tones. |
| **Dot Matrix** | Impact printing technology using pins striking an inked ribbon; characterized by visible dots and coarse mechanical banding. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip executing the video processing pipeline. |
| **Interpolator** | A hardware multiply-accumulate unit used for linear crossfading between two signals (wet/dry mix). |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Posterization** | Reducing the number of discrete tonal levels, collapsing smooth gradients into flat bands. |
| **Sample-and-Hold** | Latching a value and holding it constant for a defined interval; used here to create uniform pixel blocks. |
| **Thermal Printing** | A printing technology that uses heat to darken chemically treated paper; produces smooth transfers with characteristic paper tint and head banding. |
| **YUV** | Color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |
