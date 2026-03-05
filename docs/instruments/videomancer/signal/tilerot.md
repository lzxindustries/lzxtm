---
draft: true
sidebar_position: 310
slug: /instruments/videomancer/tilerot
title: "Tile Rot"
image: /img/instruments/videomancer/tilerot/tilerot_hero_s1.png
description: "Tilerot recreates the distinctive visual corruption that occurs when data packets are lost during compressed video streaming."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import tilerot_control_panel from '/img/instruments/videomancer/tilerot/tilerot_control_panel.png';
import tilerot_source1_car from '/img/instruments/videomancer/tilerot/tilerot_source1_car.png';
import tilerot_source2_skull from '/img/instruments/videomancer/tilerot/tilerot_source2_skull.png';
import tilerot_source3_collage from '/img/instruments/videomancer/tilerot/tilerot_source3_collage.png';
import tilerot_source4_pattern from '/img/instruments/videomancer/tilerot/tilerot_source4_pattern.png';
import tilerot_source5_girl from '/img/instruments/videomancer/tilerot/tilerot_source5_girl.png';
import tilerot_source6_berries from '/img/instruments/videomancer/tilerot/tilerot_source6_berries.png';
import tilerot_hero_s1 from '/img/instruments/videomancer/tilerot/tilerot_hero_s1.png';
import tilerot_hero_s2 from '/img/instruments/videomancer/tilerot/tilerot_hero_s2.png';
import tilerot_hero_s3 from '/img/instruments/videomancer/tilerot/tilerot_hero_s3.png';
import tilerot_hero_s4 from '/img/instruments/videomancer/tilerot/tilerot_hero_s4.png';
import tilerot_hero_s5 from '/img/instruments/videomancer/tilerot/tilerot_hero_s5.png';
import tilerot_hero_s6 from '/img/instruments/videomancer/tilerot/tilerot_hero_s6.png';
import tilerot_ex1_s1 from '/img/instruments/videomancer/tilerot/tilerot_ex1_s1.png';
import tilerot_ex1_s2 from '/img/instruments/videomancer/tilerot/tilerot_ex1_s2.png';
import tilerot_ex1_s3 from '/img/instruments/videomancer/tilerot/tilerot_ex1_s3.png';
import tilerot_ex1_s4 from '/img/instruments/videomancer/tilerot/tilerot_ex1_s4.png';
import tilerot_ex1_s5 from '/img/instruments/videomancer/tilerot/tilerot_ex1_s5.png';
import tilerot_ex1_s6 from '/img/instruments/videomancer/tilerot/tilerot_ex1_s6.png';
import tilerot_ex2_s1 from '/img/instruments/videomancer/tilerot/tilerot_ex2_s1.png';
import tilerot_ex2_s2 from '/img/instruments/videomancer/tilerot/tilerot_ex2_s2.png';
import tilerot_ex2_s3 from '/img/instruments/videomancer/tilerot/tilerot_ex2_s3.png';
import tilerot_ex2_s4 from '/img/instruments/videomancer/tilerot/tilerot_ex2_s4.png';
import tilerot_ex2_s5 from '/img/instruments/videomancer/tilerot/tilerot_ex2_s5.png';
import tilerot_ex2_s6 from '/img/instruments/videomancer/tilerot/tilerot_ex2_s6.png';
import tilerot_ex3_s1 from '/img/instruments/videomancer/tilerot/tilerot_ex3_s1.png';
import tilerot_ex3_s2 from '/img/instruments/videomancer/tilerot/tilerot_ex3_s2.png';
import tilerot_ex3_s3 from '/img/instruments/videomancer/tilerot/tilerot_ex3_s3.png';
import tilerot_ex3_s4 from '/img/instruments/videomancer/tilerot/tilerot_ex3_s4.png';
import tilerot_ex3_s5 from '/img/instruments/videomancer/tilerot/tilerot_ex3_s5.png';
import tilerot_ex3_s6 from '/img/instruments/videomancer/tilerot/tilerot_ex3_s6.png';

# Tile Rot

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Car", before: tilerot_source1_car, after: tilerot_hero_s1 },
    { label: "Skull", before: tilerot_source2_skull, after: tilerot_hero_s2 },
    { label: "Collage", before: tilerot_source3_collage, after: tilerot_hero_s3 },
    { label: "Pattern", before: tilerot_source4_pattern, after: tilerot_hero_s4 },
    { label: "Girl", before: tilerot_source5_girl, after: tilerot_hero_s5 },
    { label: "Berries", before: tilerot_source6_berries, after: tilerot_hero_s6 },
  ]}
/>
*Tilerot simulating the blocky, frozen-then-corrupted look of H.264 streaming packet loss: color-tinted macro-blocks freeze, fill with noise, and slowly recover like a bad video conference connection.*

---

## Overview

**Tilerot** recreates the distinctive visual corruption that occurs when data packets are lost during compressed video streaming. In codecs like H.264/HEVC, video is divided into rectangular slices and tiles. When a packet carrying a slice is lost, the decoder cannot update that region — it freezes on the last successfully decoded content, fills with error-concealment data, or displays corrupted blocks of noise and solid color. The resulting image is a patchwork of frozen, smeared, and noise-filled rectangles that slowly recover as new key frames arrive.

The implementation divides the screen into horizontal slices (or a grid of tiles) whose height is controlled by the Slice Height knob. At each slice boundary, an LFSR-generated random number is compared against the Error Rate threshold — slices that "fail" this check enter a corrupted state with a persistence counter. Corrupted regions display a blend of frozen (previous-line) content, solid color from an 8-entry hue lookup table, or LFSR-generated noise. The Freeze Blend knob controls the mix between frozen and fill content. Quantization noise is added to corrupted regions only, and a slow-recovery mode decrements persistence counters probabilistically, causing tiles to "heal" gradually.

Tilerot is in the **Signal** category — here simulating a digital signal impairment rather than an analog one.

---

## Quick Start

1. **Low error for ambiance**: Error Rate at 5–10% produces occasional glitches that feel like a slightly unstable stream.
2. **Tile mode for realism**: Real codec artifacts are rectangular — use Tile mode for authentic H.264/HEVC looks.
3. **Freeze Blend for ghosting**: At ~50%, corrupted regions show a ghostly blend of old and fill content — evocative of temporal layering.

---

## Background

### What Is Packet Loss in Video Streaming?

Modern video codecs (H.264, HEVC, VP9, AV1) compress video into a stream of **packets**, each containing one or more coded slices of the frame. If a packet is lost or corrupted during transmission (common over Wi-Fi, cellular, and congested networks), the decoder cannot reconstruct the corresponding region. The visible result depends on the error concealment strategy: some decoders freeze the last good frame for that region, some substitute a solid color, and some display corrupted data (random noise or displaced pixels). The artifacts are distinctly blocky because codecs operate on macro-block grids.

### What Is a Macro-Block?

Video codecs divide each frame into a grid of fixed-size blocks — typically 16×16 (H.264) or up to 64×64 (HEVC) pixels. Each **macro-block** is independently coded and can reference predictions from previous frames. When a macro-block's data is lost, only that block region is affected, producing the characteristic rectangular corruption pattern. Tilerot simulates this with configurable slice heights (4–128 pixels) and optional tile-mode column subdivision.

### What Is Persistence and Recovery?

In real streaming, a corrupted region doesn't recover instantly. The decoder continues displaying the error-concealment substitute until a new **intra-coded** (key) frame arrives that fully refreshes the region. This creates a temporal persistence — tiles stay corrupted for multiple frames before suddenly snapping back to clean. Tilerot models this with per-slice 4-bit persistence counters that start at 15 and decrement over time, with the recovery rate controlled by the Slow/Fast toggle.

### What Is Error Concealment?

When a decoder detects a lost packet, it applies an **error concealment** strategy to minimize visible disruption. Common strategies include: repeating the last good frame (freeze), filling with a nearby average color (solid fill), or extrapolating motion vectors (not applicable here). Tilerot implements freeze and fill modes with a blend control, plus optional quantization noise to simulate the halo of DCT-domain corruption around lost blocks.


---

## Signal Flow

Position Counters → Slice / Tile Division → Error Decision Engine → ... → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ X counter (per-pixel, reset on hsync)
│   ├─ Y counter (per-line, reset on vsync)
│   └─ Frame counter (animation, LFSR seed)
│
├── Slice / Tile Division ──────────────────────────────────────
│   ├─ Slice height (pot → 4..128 pixel bands)
│   ├─ Slice index from v_count upper bits
│   └─ Tile mode: additional per-32-pixel column check
│
├── Error Decision Engine ──────────────────────────────────────
│   ├─ LFSR16 random comparison vs Error Rate
│   ├─ Per-slice boundary: set persistence = 15 on fail
│   ├─ Tile mode: per-column check at 32px intervals
│   └─ 32-slot persistence array (4-bit counters)
│
├── Content Generation ─────────────────────────────────────────
│   ├─ Frozen content: line buffer BRAM (1024×10 Y/U/V)
│   ├─ Fill: Solid (hue LUT) or Noise (LFSR Y + hue UV)
│   ├─ Freeze Blend: weighted avg of frozen + fill
│   └─ Quant Noise: LFSR noise added to corrupted pixels only
│
├── Recovery ───────────────────────────────────────────────────
│   ├─ Fast: decrement persistence each frame
│   └─ Slow: probabilistic decrement (LFSR gate)
│
├── Output Selection ───────────────────────────────────────────
│   ├─ If persistence > 0: output corrupted content
│   └─ If persistence = 0: output clean input
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through with 8-clock delay
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The error decision runs once per slice boundary (when `v_count` crosses a slice edge). At that instant, the LFSR output is compared against the Error Rate threshold — higher Error Rate means more slices fail and become corrupted. In Tile mode, a second check runs every 32 pixels horizontally, allowing individual columns within a slice to corrupt independently. The frozen content comes from three 1024×10-bit BRAM buffers (one per YUV channel) that capture the previous line's data. Fill content is either a solid color from the 8-entry hue LUT (indexed by the Fill Hue knob) or LFSR noise tinted with the selected hue. The Freeze Blend knob cross-fades between frozen and fill for each corrupted pixel.

---

## Parameter Reference

<img src={tilerot_control_panel} alt="Videomancer front panel with Tile Rot loaded"/>
*Videomancer's front panel with Tile Rot active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Error Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

At minimum, no slices fail the LFSR check — the image is clean. As Error Rate increases, more slices per frame enter the corrupted state. At maximum, nearly every slice is corrupted every frame, producing a heavily degraded image. The error decision uses a simple threshold comparison: `LFSR_output < error_rate × scale`. Internally, controls the probability of corruption per slice (or tile).

---

#### Knob 2 — Slice Height
| Property | Value |
|----------|-------|
| Range | 4 – 128 |
| Default | 35 |

Controls the height of each horizontal slice, mapped from 4 pixels (narrow strips) to 128 pixels (tall blocks). Shorter slices produce fine-grained corruption with many small affected regions. Taller slices produce large swaths of corruption — fewer affected blocks but each one covers a larger screen area. The mapping is via the upper bits of the vertical counter.

---

#### Knob 3 — Fill Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 106° |
| Suffix | ° |

Selects the fill color hue from an 8-entry lookup table of UV values. The hue cycles through common error-concealment colors: green, cyan, blue, magenta, red, yellow, and intermediate tones. This colors the solid fill (or tints the noise fill) of corrupted regions. In some codecs, corrupted blocks display a consistent fill color; this knob selects which one.

---

#### Knob 4 — Freeze Blend
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, corrupted pixels show only frozen content — the region appears stuck on an old frame. At 100%, corrupted pixels show only fill (solid color or noise). Intermediate values produce a ghost-like blend of frozen video with colored overlay, closely mimicking the temporal blending of real decoder error concealment. Internally, controls the mix between frozen (previous-line) content and fill content within corrupted regions.

---

#### Knob 5 — Quant Noise
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

At zero, corrupted blocks are clean (frozen or solid fill). Increasing Quant Noise adds random per-pixel perturbation to the corrupted content, simulating the halo of DCT coefficient errors around lost blocks. The noise is only applied where persistence > 0 — clean regions are unaffected. Internally, controls the amplitude of quantization noise added to corrupted regions.

---

#### Knob 6 — Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 512 |

Controls the random seed for the LFSR, affecting which specific slices corrupt on each frame. Different seed values produce different spatial patterns of corruption for the same Error Rate. This allows fine-tuning the "look" of the packet loss by shifting which slices tend to fail.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Tiles | Slices |
| **8 — Fill Type** | Solid | Noise |
| **9 — Recover** | Fast | Slow |
| **10 — Animate** | Static | Animate |
| **11 — Bypass** | Off | On |

Switches 7–11 control the corruption geometry (slices vs tiles), fill type (solid vs noise), recovery speed, animation, and bypass. The Mode switch (7) dramatically changes the corruption pattern — Tiles adds column-level subdivision for a more grid-like appearance matching modern codec macro-block structures.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the corrupted output and the original input via the hardware interpolator. At 100%, the full tilerot processing is applied. Lowering the fader blends clean video back in.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Tile Rot processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore slice-mode corruption, tile-mode macro-block artifacts, and creative use of fill colors and noise for glitch aesthetics.

### Exercise 1: Horizontal Slice Corruption

<BeforeAfterSlider
  sources={[
    { label: "Car", before: tilerot_source1_car, after: tilerot_ex1_s1 },
    { label: "Skull", before: tilerot_source2_skull, after: tilerot_ex1_s2 },
    { label: "Collage", before: tilerot_source3_collage, after: tilerot_ex1_s3 },
    { label: "Pattern", before: tilerot_source4_pattern, after: tilerot_ex1_s4 },
    { label: "Girl", before: tilerot_source5_girl, after: tilerot_ex1_s5 },
    { label: "Berries", before: tilerot_source6_berries, after: tilerot_ex1_s6 },
  ]}
/>
*Horizontal Slice Corruption — simulated result across source images.*
**Source**: Camera feed with recognizable content (faces, text, landmarks) where corruption is easily identified.

**What You'll Create**: Produce classic horizontal-slice dropout artifacts with frozen content.

1. **Enable corruption**: Set Error Rate to ~30%. Several horizontal slices begin to freeze.
2. **Slice height**: Set Slice Height to ~40%. Medium-width bands — clearly visible individual slices.
3. **Freeze mode**: Set Freeze Blend to 0%. Corrupted slices show frozen (previous) content — they appear to "stick" on old video.
4. **Observe persistence**: Slices remain corrupted for multiple frames before snapping back to live content.
5. **Solid fill**: Increase Freeze Blend to ~100% and set Fill Type to Solid (Switch 8). Corrupted slices become solid colored bars.
6. **Fill color**: Sweep Fill Hue to change the corruption color — green blocks, cyan blocks, magenta blocks.

**Key concepts**: Error Rate controls corruption probability, slice height sets band width, Freeze Blend crosses between frozen content and fill, persistence causes temporal sticking

---

### Exercise 2: Macro-Block Tile Grid

<BeforeAfterSlider
  sources={[
    { label: "Car", before: tilerot_source1_car, after: tilerot_ex2_s1 },
    { label: "Skull", before: tilerot_source2_skull, after: tilerot_ex2_s2 },
    { label: "Collage", before: tilerot_source3_collage, after: tilerot_ex2_s3 },
    { label: "Pattern", before: tilerot_source4_pattern, after: tilerot_ex2_s4 },
    { label: "Girl", before: tilerot_source5_girl, after: tilerot_ex2_s5 },
    { label: "Berries", before: tilerot_source6_berries, after: tilerot_ex2_s6 },
  ]}
/>
*Macro-Block Tile Grid — simulated result across source images.*
**Source**: Graphic content or video with clear spatial detail — the tile grid is most visible against structured imagery.

**What You'll Create**: Create the rectangular macro-block corruption pattern characteristic of H.264 streaming dropouts.

1. **Tile mode**: Set Mode to Tiles (Switch 7). Corruption now occurs in a grid pattern.
2. **Error Rate**: Set Error Rate to ~40%. Multiple tiles across the frame become corrupted.
3. **Small blocks**: Set Slice Height to ~20%. The tile grid becomes fine-grained — small rectangles.
4. **Noise fill**: Set Fill Type to Noise (Switch 8). Corrupted tiles show colored static.
5. **Quant noise**: Add Quant Noise at ~30%. A halo of quantization artifacts appears around corrupted tiles.
6. **Slow recover**: Set Recover to Slow (Switch 9). Tiles linger in their corrupted state much longer, creating the "buffering" look of congested streaming.

**Key concepts**: Tile mode adds column subdivision for rectangular blocks, Noise fill simulates data corruption, slow recovery mimics sustained packet loss

---

### Exercise 3: Glitch Art Aesthetic

<BeforeAfterSlider
  sources={[
    { label: "Car", before: tilerot_source1_car, after: tilerot_ex3_s1 },
    { label: "Skull", before: tilerot_source2_skull, after: tilerot_ex3_s2 },
    { label: "Collage", before: tilerot_source3_collage, after: tilerot_ex3_s3 },
    { label: "Pattern", before: tilerot_source4_pattern, after: tilerot_ex3_s4 },
    { label: "Girl", before: tilerot_source5_girl, after: tilerot_ex3_s5 },
    { label: "Berries", before: tilerot_source6_berries, after: tilerot_ex3_s6 },
  ]}
/>
*Glitch Art Aesthetic — simulated result across source images.*
**Source**: Any visually rich source — portraits, landscapes, or graphic patterns work well.

**What You'll Create**: Push Tilerot into extreme territory for intentional glitch art effects.

1. **High error**: Set Error Rate to ~80%. Nearly the entire frame is corrupted.
2. **Large tiles**: Set Slice Height to ~70%. Wide horizontal bands in Slice mode.
3. **Blend ghosting**: Set Freeze Blend to ~50%. Corrupted regions show ghostly blends of frozen video and solid color.
4. **Vivid fill**: Set Fill Hue to a bold color (magenta ~60%). The solid fill creates a strong color wash.
5. **Heavy noise**: Set Quant Noise to ~70%. Aggressive noise halos around every corrupted region.
6. **Switch to tiles**: Toggle Mode to Tiles. The large, vivid, noisy rectangular blocks create an intentional datamosh aesthetic.
7. **Static mode**: Set Animate to Static (Switch 10). The corruption pattern locks — useful for framing a specific glitch composition.

**Key concepts**: High error rates create majority-corrupted frames, Freeze Blend ghosting blends temporal layers, Static mode locks the composition, extreme settings cross into intentional glitch art

---


## Tips

- **Seed for variety**: Changing the Seed knob shifts which spatial pattern of slices corrupts, useful for finding aesthetically pleasing compositions.
- **Chain with Subphase**: Tilerot for digital corruption + Subphase for analog degradation creates a "transcoded" look — digital artifacts on analog signal impairments.
- **Static for composition**: Animate=Static freezes the corruption pattern, allowing careful framing of the glitch aesthetic.
- **Quant Noise for halos**: Real codec errors produce a halo of DCT noise around lost blocks — Quant Noise approximates this effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **DCT** | Discrete Cosine Transform; the basis of JPEG and early H.264 compression. Quantization errors in DCT coefficients produce the characteristic noise halos around corrupted blocks. |
| **Error Concealment** | The strategy a decoder uses to minimize visible artifacts when data is lost: freeze, fill, interpolate, or skip. |
| **H.264/HEVC** | Modern video compression codecs (H.264/AVC and H.265/HEVC) that divide frames into macro-blocks and slices. |
| **LFSR** | Linear Feedback Shift Register; a pseudorandom number generator used for corruption decisions and noise generation. |
| **Macro-Block** | A fixed-size rectangular region (e.g., 16×16 or 64×64 pixels) that is independently coded in block-based video codecs. |
| **Packet Loss** | The failure of one or more data packets to arrive at the destination, causing gaps in the compressed bitstream. |
| **Persistence** | A per-slice/tile counter that tracks how long a corrupted region has been affected, controlling recovery timing. |
| **Quantization Noise** | The noise-like artifacts produced by aggressive quantization of transform coefficients, visible as blocky distortion. |
| **Slice** | A horizontal strip of the video frame that is independently decodable in H.264 and similar codecs. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
