---
draft: true
sidebar_position: 183
slug: /instruments/videomancer/macrobloc
title: "Macrobloc"
image: /img/instruments/videomancer/macrobloc/macrobloc_hero_s1.png
description: "Digital video compression divides every frame into small rectangular blocks and encodes each one independently."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import macrobloc_source1_skull from '/img/instruments/videomancer/macrobloc/macrobloc_source1_skull.png';
import macrobloc_source2_sunset from '/img/instruments/videomancer/macrobloc/macrobloc_source2_sunset.png';
import macrobloc_source3_collage from '/img/instruments/videomancer/macrobloc/macrobloc_source3_collage.png';
import macrobloc_source4_pattern from '/img/instruments/videomancer/macrobloc/macrobloc_source4_pattern.png';
import macrobloc_source5_woman from '/img/instruments/videomancer/macrobloc/macrobloc_source5_woman.png';
import macrobloc_source6_wood from '/img/instruments/videomancer/macrobloc/macrobloc_source6_wood.png';
import macrobloc_hero_s1 from '/img/instruments/videomancer/macrobloc/macrobloc_hero_s1.png';
import macrobloc_hero_s2 from '/img/instruments/videomancer/macrobloc/macrobloc_hero_s2.png';
import macrobloc_hero_s3 from '/img/instruments/videomancer/macrobloc/macrobloc_hero_s3.png';
import macrobloc_hero_s4 from '/img/instruments/videomancer/macrobloc/macrobloc_hero_s4.png';
import macrobloc_hero_s5 from '/img/instruments/videomancer/macrobloc/macrobloc_hero_s5.png';
import macrobloc_hero_s6 from '/img/instruments/videomancer/macrobloc/macrobloc_hero_s6.png';
import macrobloc_ex1_s1 from '/img/instruments/videomancer/macrobloc/macrobloc_ex1_s1.png';
import macrobloc_ex1_s2 from '/img/instruments/videomancer/macrobloc/macrobloc_ex1_s2.png';
import macrobloc_ex1_s3 from '/img/instruments/videomancer/macrobloc/macrobloc_ex1_s3.png';
import macrobloc_ex1_s4 from '/img/instruments/videomancer/macrobloc/macrobloc_ex1_s4.png';
import macrobloc_ex1_s5 from '/img/instruments/videomancer/macrobloc/macrobloc_ex1_s5.png';
import macrobloc_ex1_s6 from '/img/instruments/videomancer/macrobloc/macrobloc_ex1_s6.png';
import macrobloc_ex2_s1 from '/img/instruments/videomancer/macrobloc/macrobloc_ex2_s1.png';
import macrobloc_ex2_s2 from '/img/instruments/videomancer/macrobloc/macrobloc_ex2_s2.png';
import macrobloc_ex2_s3 from '/img/instruments/videomancer/macrobloc/macrobloc_ex2_s3.png';
import macrobloc_ex2_s4 from '/img/instruments/videomancer/macrobloc/macrobloc_ex2_s4.png';
import macrobloc_ex2_s5 from '/img/instruments/videomancer/macrobloc/macrobloc_ex2_s5.png';
import macrobloc_ex2_s6 from '/img/instruments/videomancer/macrobloc/macrobloc_ex2_s6.png';
import macrobloc_ex3_s1 from '/img/instruments/videomancer/macrobloc/macrobloc_ex3_s1.png';
import macrobloc_ex3_s2 from '/img/instruments/videomancer/macrobloc/macrobloc_ex3_s2.png';
import macrobloc_ex3_s3 from '/img/instruments/videomancer/macrobloc/macrobloc_ex3_s3.png';
import macrobloc_ex3_s4 from '/img/instruments/videomancer/macrobloc/macrobloc_ex3_s4.png';
import macrobloc_ex3_s5 from '/img/instruments/videomancer/macrobloc/macrobloc_ex3_s5.png';
import macrobloc_ex3_s6 from '/img/instruments/videomancer/macrobloc/macrobloc_ex3_s6.png';

# Macrobloc

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: macrobloc_source1_skull, after: macrobloc_hero_s1 },
    { label: "Sunset", before: macrobloc_source2_sunset, after: macrobloc_hero_s2 },
    { label: "Collage", before: macrobloc_source3_collage, after: macrobloc_hero_s3 },
    { label: "Pattern", before: macrobloc_source4_pattern, after: macrobloc_hero_s4 },
    { label: "Woman", before: macrobloc_source5_woman, after: macrobloc_hero_s5 },
    { label: "Wood", before: macrobloc_source6_wood, after: macrobloc_hero_s6 },
  ]}
/>
*Macrobloc corrupting a video source with block displacement, DC fill, freeze artifacts, and chroma separation errors.*

---

## Overview

Digital video compression divides every frame into small rectangular blocks and encodes each one independently. When the data stream is damaged — a dropped packet, a bit error, a lost reference frame — the decoder cannot reconstruct the affected blocks. The result is the distinctive breakup everyone has seen on satellite TV, streaming video, or video calls over bad connections: rectangular patches of wrong color, frozen content, shifted pixels, and green-magenta chroma smears. Macrobloc recreates those failure modes deliberately.

The program divides the screen into either 8×8 or 16×16 pixel blocks (the two standard macroblock sizes from MPEG and H.264) and randomly selects which blocks to corrupt each frame. Four corruption types are available: DC fill (a flat gray rectangle), displacement (content shifted from a wrong position), freeze (the block holds its previous value instead of updating), and chroma shift (luminance and chrominance read from different spatial positions, creating color separation artifacts). The density of corruption is continuously variable from pristine to total destruction.

The name is a deliberate misspelling of *macroblock*, the standard term in video compression for the fundamental coding unit. By removing a letter, it becomes its own thing — not a decoder bug, but a creative tool that happens to look exactly like one.

---

## Background

### Macroblocking in Video Compression

Every modern video codec — MPEG-2, H.264, HEVC — divides each frame into a grid of square blocks. In MPEG-2 these are 16×16 pixel macroblocks; H.264 can use 4×4, 8×8, or 16×16. Each block is transformed, quantized, and entropy-coded independently. When any part of that data chain is corrupted, the decoder produces a visually wrong block while surrounding blocks remain correct. The sharp rectangular boundary between correct and incorrect content is the signature of digital compression failure — fundamentally different from the smooth, gradual degradation of analog video noise.

### Motion Vector Errors and Displacement

In inter-frame prediction, the encoder stores a *motion vector* for each block — a pointer to a region in a reference frame that looks similar. The decoder uses this vector to copy pixels from the reference and then adds a small correction. If the motion vector itself is corrupted, the decoder copies pixels from the wrong location. The result is a block of content that is internally coherent (it looks like real video) but spatially displaced from where it should be. Macrobloc's displacement mode simulates this by reading pixel data from an offset position in the line buffer.

### I-Frame Loss and Freeze

Video codecs maintain reference frames that subsequent frames depend on. When a reference frame is lost or corrupted, the decoder can only display the last successfully decoded content for the affected blocks. These blocks "freeze" — they stop updating while the rest of the image continues to move. Macrobloc simulates this with a per-block freeze flag that, when set, causes the block to output its held previous values instead of the current input. The freeze map is re-rolled each frame based on the Freeze Rate parameter.

### Chroma Subsampling Errors

In YUV 4:2:0 (the most common broadcast format), chroma is sampled at half the resolution of luma in both axes. If the chroma and luma data become misaligned during decoding — a common failure mode when packet boundaries are lost — the color information ends up spatially shifted relative to the brightness. This creates the characteristic green and magenta fringing seen in heavily corrupted MPEG streams. Macrobloc simulates this by reading U and V channel data from a different line buffer address than Y.

### LFSR-Driven Block Selection

The corruption pattern is generated by a 16-bit linear feedback shift register. At the start of each block, the LFSR is advanced and its output compared against the Corruption threshold. If the LFSR value falls below the threshold, the block is marked corrupt. The corruption type is determined by the low 2 bits of the same LFSR state. In animated mode, the LFSR seed evolves frame to frame, producing dynamic corruption. In static mode, the same seed is loaded every frame, producing a fixed corruption pattern.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Line Buffer Write
│   └─ ram_y/ram_u/ram_v[wr_addr] ← Y/U/V input (continuous)
│
├── Stage 1: Block Address Generation + LFSR Sample
│   ├─ h_count, v_count (pixel counters)
│   ├─ block_x, block_y (block grid coordinates)
│   ├─ pixel_x, pixel_y (position within block)
│   ├─ block_start flag (top-left pixel of each block)
│   ├─ at_edge flag (first row or column of block)
│   ├─ LFSR advance at block_start
│   ├─ Luma Mod: threshold += (1023 − Y) >> 4 if enabled
│   └─ block_corrupt = LFSR < threshold; corrupt_type = LFSR[1:0]
│
├── Stage 2: Source Selection + Line Buffer Read
│   ├─ Write address: h_count (current pixel)
│   ├─ Y read address: h_count + displacement_offset (if corrupt type 01/11)
│   ├─ UV read address: Y_addr + chroma_offset (independent shift)
│   └─ Freeze map update at frame boundary (per-block toggle)
│
├── Stage 3: Corruption Application
│   ├─ Type 00 (DC fill): Y = dc_fill_level, U = V = 512
│   ├─ Type 01 (Displacement): Y from displaced addr, UV from chroma-shifted addr
│   ├─ Type 10 (Freeze): Y/U/V from held previous values (if freeze flag set)
│   ├─ Type 11 (Chroma shift): Y from normal addr, UV from chroma-shifted addr
│   └─ Store held values for freeze (update when not frozen)
│
├── Stage 4: Block Edge + Compose
│   ├─ If Block Edge On and at_edge: Y = 0, UV = 512 (black border)
│   └─ Output proc_y/proc_u/proc_v
│
├── Interpolator (4 clocks)
│   └─ Mix: lerp(dry, wet, mix_amount) per Y/U/V
│
└── Output
    └─ No bypass toggle — use Mix = 0% for dry signal
```

The line buffers are critical to the displacement and freeze modes. Each pixel is written to the buffer at its natural horizontal address as it arrives. Displaced blocks read from a different address in the same line buffer, effectively pulling content from elsewhere in the current scan line. The chroma shift adds a second independent offset to the U/V read address, so luma and chroma can come from entirely different horizontal positions. The freeze mode bypasses the line buffer entirely, outputting held registers that were captured during a previous non-frozen pass.

The LFSR drives all randomness: which blocks are corrupt, what type of corruption they get, the magnitude of displacement offsets, and the freeze map evolution. The Seed control sets the starting state for static mode, making the corruption pattern fully reproducible. In animated mode, the LFSR evolves across frames, producing temporally varying corruption that more closely matches the look of real-time codec failure.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Corruption
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the percentage of blocks that are corrupted. The 10-bit register value is compared against each block's LFSR sample — higher values mean more blocks pass the corruption threshold. At 0%, no blocks are corrupted and the output is clean. At 100%, every block is corrupted. The relationship is roughly linear, though the LFSR's pseudo-random distribution means the actual percentage varies slightly from the nominal value.

---

#### Knob 2 — Displacement
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets the magnitude of spatial displacement for blocks that receive displacement corruption (types 01 and 11). The displacement offset is computed by multiplying a portion of the LFSR state by this register value and scaling down. At zero, displaced blocks read from their correct position (no visible displacement). At maximum, content can shift by up to half a scan line, pulling in pixels from distant parts of the image.

---

#### Knob 3 — Freeze Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the probability that each block's freeze flag is toggled at the start of each frame. A higher value means more blocks get frozen more often. The freeze state is persistent — once a block is frozen, it stays frozen until the flag is toggled back. This creates a stochastic pattern where some blocks hold stale content for many frames while others update normally, closely matching the visual behavior of I-frame loss in real codecs.

---

#### Knob 4 — Chroma Shift
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets the magnitude of the independent chroma displacement. When a block is corrupted, the U and V channels are read from a different line buffer address than Y. This register controls how far apart those addresses are. At zero, chroma and luma are aligned (no visible color shift). At high values, the color information is pulled from a completely different part of the scan line, creating strong green-magenta fringing at block boundaries.

---

#### Knob 5 — Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 512 |

Sets the LFSR seed for static corruption mode. In static mode (Animate = Static), the LFSR is reset to this value at the start of every frame, producing a repeatable corruption pattern. Different seed values produce different spatial distributions of corrupted blocks. In animated mode, this parameter has reduced effect because the LFSR evolves freely across frames.

---

#### Knob 6 — DC Fill
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the luminance level for DC-fill corruption blocks. When a block receives DC fill corruption (type 00), Y is replaced with this register value and U/V are set to neutral (512). At zero, DC blocks appear black. At mid-scale, they are mid-gray. At maximum, they are near-white. This directly controls the visual intensity of the flat rectangular patches.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Block Size** | 8x8 | 16x16 |
| **8 — Corr Type** | Random | DC Fill |
| **9 — Block Edge** | Off | On |
| **10 — Animate** | Static | Animate |
| **11 — Luma Mod** | Off | On |

Five toggles configure the corruption behavior. There is no bypass toggle — toggle 11 is used for Luma Modulation instead. To bypass all processing, set the Mix fader to 0% (fully dry).

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade. At 0% the output is the unprocessed source (dry). At 100% the output is the fully corrupted signal (wet). Because there is no bypass toggle, the Mix fader is the only way to preview the clean source — set it to 0% for a completely unprocessed pass-through.

---

## Guided Exercises

These exercises progress from basic block corruption to complex multi-mode degradation. Each demonstrates a different aspect of digital codec failure and its creative potential.

### Exercise 1: Basic Block Corruption

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: macrobloc_source1_skull, after: macrobloc_ex1_s1 },
    { label: "Sunset", before: macrobloc_source2_sunset, after: macrobloc_ex1_s2 },
    { label: "Collage", before: macrobloc_source3_collage, after: macrobloc_ex1_s3 },
    { label: "Pattern", before: macrobloc_source4_pattern, after: macrobloc_ex1_s4 },
    { label: "Woman", before: macrobloc_source5_woman, after: macrobloc_ex1_s5 },
    { label: "Wood", before: macrobloc_source6_wood, after: macrobloc_ex1_s6 },
  ]}
/>
*Basic Block Corruption — simulated result across source images.*
**Source**: A camera feed or recorded footage with moderate motion and recognizable content.

**Objective**: Understand how corruption density and block size interact to create the fundamental macroblocking effect.

1. **Start clean**: Set Corruption to 0%. Output should be pristine.
2. **Introduce corruption**: Slowly increase Corruption. Gray rectangles (DC fill) and displaced blocks begin appearing.
3. **Block size comparison**: Switch Block Size between 8×8 and 16×16. Observe how larger blocks create chunkier breakup.
4. **DC only**: Switch Corruption Type to DC Fill. All corrupted blocks become uniform gray rectangles.
5. **Adjust DC level**: Sweep DC Fill from 0% to 100%. The rectangles change from black to white.
6. **Block edges**: Enable Block Edge to see the grid structure underlying the corruption.

**Key concepts**: Corruption threshold sets block density, DC fill produces uniform rectangles, block size changes the granularity of the grid

---

### Exercise 2: Motion Vector Failure

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: macrobloc_source1_skull, after: macrobloc_ex2_s1 },
    { label: "Sunset", before: macrobloc_source2_sunset, after: macrobloc_ex2_s2 },
    { label: "Collage", before: macrobloc_source3_collage, after: macrobloc_ex2_s3 },
    { label: "Pattern", before: macrobloc_source4_pattern, after: macrobloc_ex2_s4 },
    { label: "Woman", before: macrobloc_source5_woman, after: macrobloc_ex2_s5 },
    { label: "Wood", before: macrobloc_source6_wood, after: macrobloc_ex2_s6 },
  ]}
/>
*Motion Vector Failure — simulated result across source images.*
**Source**: Footage with lateral motion — panning shots, moving subjects, or scrolling graphics.

**Objective**: Explore displacement and chroma shift to simulate motion vector and chroma subsampling errors.

1. **Set moderate corruption**: Corruption ~50%, Corruption Type set to Random.
2. **Add displacement**: Increase Displacement to about 60%. Corrupted blocks now show content from wrong positions rather than flat gray.
3. **Add chroma shift**: Increase Chroma Shift to about 50%. Green and magenta fringing appears at block edges.
4. **Maximum displacement**: Push Displacement to 100%. Blocks pull content from far across the scan line.
5. **Animate**: Set Animate to Animated. Watch the corruption pattern shift frame to frame.
6. **Luma modulation**: Enable Luma Mod. Dark regions become more corrupted while bright areas stay cleaner.

**Key concepts**: Displacement reads from wrong line buffer positions, chroma shift separates Y from UV address, luma modulation creates content-aware corruption

---

### Exercise 3: Frozen Reference Frame

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: macrobloc_source1_skull, after: macrobloc_ex3_s1 },
    { label: "Sunset", before: macrobloc_source2_sunset, after: macrobloc_ex3_s2 },
    { label: "Collage", before: macrobloc_source3_collage, after: macrobloc_ex3_s3 },
    { label: "Pattern", before: macrobloc_source4_pattern, after: macrobloc_ex3_s4 },
    { label: "Woman", before: macrobloc_source5_woman, after: macrobloc_ex3_s5 },
    { label: "Wood", before: macrobloc_source6_wood, after: macrobloc_ex3_s6 },
  ]}
/>
*Frozen Reference Frame — simulated result across source images.*
**Source**: Active footage with continuous motion — handheld camera, dance performance, or sports.

**Objective**: Combine freeze mode with other corruption types for full codec failure simulation.

1. **Moderate corruption**: Corruption ~40%, Random mode.
2. **Enable freeze**: Set Freeze Rate to about 40%. Some blocks hold their previous values.
3. **Add displacement**: Set Displacement ~30% and Chroma Shift ~30%.
4. **Observe persistence**: Watch frozen blocks — they hold stale content for multiple frames while the source continues to move.
5. **16×16 blocks**: Switch to 16×16 for dramatic, chunky freeze artifacts.
6. **Static pattern**: Switch Animate to Static and adjust Seed to find an interesting fixed corruption pattern.
7. **Subtle blend**: Lower Mix to about 60% to blend the corrupted signal with the clean source, creating a ghostly double-exposure with block artifacts.

**Key concepts**: Freeze flags persist across frames (stochastic toggling), displacement + freeze + chroma shift compound for realistic codec failure, static mode produces repeatable patterns

---


## Tips

- **No bypass toggle**: Use Mix at 0% for clean pass-through. This is the only way to preview the unprocessed source.
- **Start with DC Fill**: DC-only mode produces the clearest macroblocking effect. Add displacement and chroma shift later for more complex failure modes.
- **16×16 for drama**: Larger blocks create more visually impactful corruption. 8×8 blocks produce subtler, higher-frequency breakup that reads better at a distance.
- **Seed for composition**: In static mode, sweep the Seed knob to audition different corruption patterns. Each seed produces a unique spatial distribution.
- **Luma Mod for narrative**: Enabling luma modulation makes shadows corrupt first, creating a natural-looking degradation where darkness hides information loss.
- **Chroma Shift is the codec signature**: Real MPEG failures almost always show chroma misalignment. A small amount of Chroma Shift (20–30%) makes the effect read as authentically digital.
- **Freeze needs motion**: Freeze corruption is invisible on static sources. Use moving footage to see the held-block persistence effect.
- **Mix for compositing**: Partial mix values create a ghostly overlay of corrupted and clean content — useful for subtle datamosh aesthetics.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory in the FPGA fabric. Macrobloc uses 3 BRAMs for Y/U/V line buffers. |
| **Chroma** | Color information in a video signal, encoded as U and V offsets from neutral gray. |
| **Chroma Subsampling** | Encoding technique that stores color at lower resolution than brightness (e.g., 4:2:0). |
| **DC Fill** | Replacing a block with a flat solid color, simulating total data loss for that macroblock. |
| **Displacement** | Spatial offset applied to a block's read address, simulating a corrupted motion vector. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip executing the processing pipeline. |
| **Freeze** | Holding a block's previous pixel values instead of reading new ones, simulating reference frame loss. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator that drives corruption decisions. |
| **Luma** | Brightness component (Y) of a YUV video signal. |
| **Macroblock** | The fundamental rectangular coding unit in MPEG/H.264 compression, typically 8×8 or 16×16 pixels. |
| **Motion Vector** | A pointer stored per macroblock indicating where to find similar content in a reference frame. |
| **Pipeline** | A chain of sequential processing stages, eight clocks total in this program. |
| **YUV** | Color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
