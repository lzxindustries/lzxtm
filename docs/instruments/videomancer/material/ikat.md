---
draft: true
sidebar_position: 141
slug: /instruments/videomancer/ikat
title: "Ikat"
image: /img/instruments/videomancer/ikat/ikat_hero_s1.png
description: "Ikat simulates the ancient resist-dyeing technique of the same name by dividing the video frame into vertical (or horizontal) stripe columns and processing each column as if it were a bundle of warp threads dipped into a dye bath."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import ikat_control_panel from '/img/instruments/videomancer/ikat/ikat_control_panel.png';
import ikat_source1_boat from '/img/instruments/videomancer/ikat/ikat_source1_boat.png';
import ikat_source2_castle from '/img/instruments/videomancer/ikat/ikat_source2_castle.png';
import ikat_source3_turtle from '/img/instruments/videomancer/ikat/ikat_source3_turtle.png';
import ikat_source4_pattern from '/img/instruments/videomancer/ikat/ikat_source4_pattern.png';
import ikat_source5_boy from '/img/instruments/videomancer/ikat/ikat_source5_boy.png';
import ikat_source6_knit from '/img/instruments/videomancer/ikat/ikat_source6_knit.png';
import ikat_hero_s1 from '/img/instruments/videomancer/ikat/ikat_hero_s1.png';
import ikat_hero_s2 from '/img/instruments/videomancer/ikat/ikat_hero_s2.png';
import ikat_hero_s3 from '/img/instruments/videomancer/ikat/ikat_hero_s3.png';
import ikat_hero_s4 from '/img/instruments/videomancer/ikat/ikat_hero_s4.png';
import ikat_hero_s5 from '/img/instruments/videomancer/ikat/ikat_hero_s5.png';
import ikat_hero_s6 from '/img/instruments/videomancer/ikat/ikat_hero_s6.png';
import ikat_ex1_s1 from '/img/instruments/videomancer/ikat/ikat_ex1_s1.png';
import ikat_ex1_s2 from '/img/instruments/videomancer/ikat/ikat_ex1_s2.png';
import ikat_ex1_s3 from '/img/instruments/videomancer/ikat/ikat_ex1_s3.png';
import ikat_ex1_s4 from '/img/instruments/videomancer/ikat/ikat_ex1_s4.png';
import ikat_ex1_s5 from '/img/instruments/videomancer/ikat/ikat_ex1_s5.png';
import ikat_ex1_s6 from '/img/instruments/videomancer/ikat/ikat_ex1_s6.png';
import ikat_ex2_s1 from '/img/instruments/videomancer/ikat/ikat_ex2_s1.png';
import ikat_ex2_s2 from '/img/instruments/videomancer/ikat/ikat_ex2_s2.png';
import ikat_ex2_s3 from '/img/instruments/videomancer/ikat/ikat_ex2_s3.png';
import ikat_ex2_s4 from '/img/instruments/videomancer/ikat/ikat_ex2_s4.png';
import ikat_ex2_s5 from '/img/instruments/videomancer/ikat/ikat_ex2_s5.png';
import ikat_ex2_s6 from '/img/instruments/videomancer/ikat/ikat_ex2_s6.png';
import ikat_ex3_s1 from '/img/instruments/videomancer/ikat/ikat_ex3_s1.png';
import ikat_ex3_s2 from '/img/instruments/videomancer/ikat/ikat_ex3_s2.png';
import ikat_ex3_s3 from '/img/instruments/videomancer/ikat/ikat_ex3_s3.png';
import ikat_ex3_s4 from '/img/instruments/videomancer/ikat/ikat_ex3_s4.png';
import ikat_ex3_s5 from '/img/instruments/videomancer/ikat/ikat_ex3_s5.png';
import ikat_ex3_s6 from '/img/instruments/videomancer/ikat/ikat_ex3_s6.png';

# Ikat

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: ikat_source1_boat, after: ikat_hero_s1 },
    { label: "Castle", before: ikat_source2_castle, after: ikat_hero_s2 },
    { label: "Turtle", before: ikat_source3_turtle, after: ikat_hero_s3 },
    { label: "Pattern", before: ikat_source4_pattern, after: ikat_hero_s4 },
    { label: "Boy", before: ikat_source5_boy, after: ikat_hero_s5 },
    { label: "Knit", before: ikat_source6_knit, after: ikat_hero_s6 },
  ]}
/>
*Ikat applying column-quantized dye simulation and LFSR-driven bleed to create warp-resist textile textures from live video.*

---

## Overview

Ikat simulates the ancient resist-dyeing technique of the same name by dividing the video frame into vertical (or horizontal) stripe columns and processing each column as if it were a bundle of warp threads dipped into a dye bath. Within each column, the luminance channel is quantized to a reduced set of levels — mimicking the way hand-dyed threads hold only a few distinct color values across a skein. At column boundaries, an LFSR-driven jitter displacement bleeds color from one stripe into the next, replicating the soft, irregular edges that occur when wax or string resist barriers fail to contain the dye perfectly.

The name comes from the Malay-Indonesian word *ikat*, meaning "to tie" or "to bind" — referring to the bundles of yarn that are tightly bound before immersion in dye vats. In the physical process, the resist ties create sharp but imperfect color boundaries; the tighter the tie, the crisper the edge. Ikat reproduces this dynamic digitally: the Column Width control sets the stripe spacing (the width of each yarn bundle), the Palette control sets the quantization coarseness (how many dye levels each bundle can hold), and the Bleed control governs the feathering at column edges (how much dye leaks across the resist barrier).

At conservative settings — wide columns, moderate quantization, low bleed — Ikat adds a subtle woven-fabric texture to any video source, compressing tonal detail into flat, dye-lot bands while preserving the overall composition. At extreme settings — narrow columns, coarse quantization, maximum bleed and jitter — the image dissolves into a buzzing, thread-like interference pattern where the original subject is barely recognizable through the textile simulation.

---

## Quick Start

1. **Unused controls**: Pot 6 (Warmth) and Toggle 8 (Palette Src) are registered but have no effect in the current VHDL. Don't spend time searching for their influence.
2. **Column width sets the fundamental scale**: Everything else — bleed, quantization, jitter — operates within the column structure defined by Pot 1. Start by choosing a column width that matches the visual density you want, then tune the other controls.
3. **Bleed is chroma-only**: The edge bleed feathers color (U/V) at column boundaries but does not affect luminance. This means the brightness structure remains column-quantized even at maximum bleed.

---

## Background

### What Is Ikat Dyeing?

**Ikat** is a dyeing technique practiced across South-East Asia, Central Asia, Japan (*kasuri*), and parts of Central and South America. Unlike printing, where patterns are applied to finished cloth, ikat creates patterns by selectively dyeing the *yarn* before weaving. Bundles of threads are wrapped tightly with wax, string, or rubber at intervals that correspond to the desired pattern, then submerged in dye. The bound sections resist the dye; the exposed sections absorb it. After dyeing, the bindings are removed and the threads are woven into fabric. Because the resist boundaries are never perfectly sharp, ikat textiles have a characteristic soft, feathered edge between color regions — a visual signature that distinguishes them from printed fabric.

### Column Quantization as Warp Simulation

In the physical process, each warp thread holds a single color value at any given point along its length — it was either exposed to the dye or it was not. Ikat simulates this by dividing the video frame into columns of a programmable width and quantizing the luminance within each column to a reduced number of levels. The quantization is implemented as a bit mask on the 10-bit Y channel: the upper bits of the Palette register control how many low-order bits are zeroed. At minimum quantization, the signal passes with full 10-bit resolution. At maximum, only the top two or three bits survive, collapsing the image into a few stark tonal bands — like yarn that has been dipped in only two or three dye baths.

### LFSR Jitter as Resist Bleed

Real ikat textiles never have perfectly straight color boundaries. The dye seeps under the resist ties, creating a soft, irregular edge. Ikat simulates this imperfection using a 16-bit **linear-feedback shift register** (LFSR) seeded with the value 0xACE1. The LFSR produces a pseudo-random displacement that shifts each pixel's luminance by a variable amount controlled by the Dye Depth knob. The jitter is added directly to the quantized Y channel, creating the fuzzy, hand-dyed look at stripe edges.

### Double Ikat and Saturation Boost

Traditional *double ikat* — where both warp and weft threads are pre-dyed — is among the most difficult textile techniques in the world. Toggle 9 enables this mode: the quantization mask is applied a second time on the perpendicular axis, creating a cross-hatched pattern instead of simple stripes. Meanwhile, the Saturate knob boosts the U and V chroma channels when set above 50%, simulating the vivid, over-saturated colors produced by repeated dye immersion.


---

## Signal Flow

Y Channel → U/V Channels → Sync Signals → Interpolator → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Column Quantization    (divide position by col_width → column index)
│   │      + LFSR Jitter Offset  (s_jitter_amount × LFSR → signed displacement)
│   ├─ 2. Palette Quantization   (bit-mask Y by palette_depth(9:7))
│   ├─ 3. Jitter Composite       (add jitter_offset to quantized Y, clamp)
│   │      + Double Ikat          (re-apply quant mask on perpendicular axis)
│   └─ 4. Output Registration
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Pass-through (latched)
│   ├─ 2. Saturation Boost       (if sat_boost > 512: U,V × sat_boost >> 9)
│   ├─ 3. Edge Bleed             (U,V × edge_blend factor at column boundaries)
│   └─ 4. Output Registration
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay pipeline (hsync, vsync, field)
│
├── Interpolator (4 clocks) ────────────────────────────────────
│   └─ Crossfade dry (delayed input) ↔ wet (processed) by Mix fader
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The key interaction in the pipeline is between column quantization and edge bleed. Stage 1 computes which column a pixel belongs to and its fractional position within that column. Stage 2 quantizes Y and boosts chroma. Stage 3 applies the LFSR jitter to Y and fades chroma toward neutral at column edges using the fractional position — pixels near the center of a column retain full chroma, while pixels near the boundary are attenuated proportionally to the Bleed Amount. Double Ikat re-applies the quantization mask in Stage 3, effectively quantizing on both axes. Note that Pot 6 (Warmth / `s_color_shift`) and Toggle 8 (Palette Src / `s_palette_mode`) are mapped to registers but are not connected to any processing stage in the current VHDL — they are reserved for future use and have no effect on the output.

---

## Parameter Reference

<img src={ikat_control_panel} alt="Videomancer front panel with Ikat loaded"/>
*Videomancer's front panel with Ikat active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Col Width
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 7 |

Controls the width of each simulated warp stripe in pixels. The pot value is divided by 16 and offset by 4, giving an effective column width range of 4 to 68 pixels. Narrow columns create a fine, thread-like vertical pattern where individual stripes are barely wider than a pixel. Wide columns create bold, flat bands of color. The column width interacts with Bleed Amount — narrower columns leave less room for edge feathering, so the bleed zone can span the entire stripe at high bleed settings.

---

#### Knob 2 — Bleed Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls how much color feathers at the boundaries between adjacent columns. At 0%, column edges are hard — each stripe has a sharp transition to its neighbor. As the value increases, the chroma channels are progressively attenuated near column edges, creating a soft gradient that simulates dye seeping under the resist tie. The bleed zone is symmetric: it fades from both the left and right edges of each column toward the center.

---

#### Knob 3 — Palette
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 1 |

Controls the number of quantization levels applied to the luminance channel. Despite its TOML label of "Palette," in the VHDL this control operates as a bit-mask depth selector: the upper three bits of the register (`palette_depth(9:7)`) determine how many low-order bits of the 10-bit Y channel are zeroed. At the minimum setting, Y passes through with full resolution. At the maximum, only two or three MSBs remain, collapsing the image into stark tonal bands. This simulates having fewer dye baths — fewer quantization levels mean fewer distinct thread colors.

---

#### Knob 4 — Saturate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls a multiplicative boost applied to the U and V chroma channels when the register value exceeds 512 (50%). Below 50%, chroma passes through unmodified. Above 50%, each chroma sample is multiplied by the register value and right-shifted by 9 bits, progressively over-saturating colors. This simulates the vivid, concentrated dye hues of deeply-immersed textile fibers. At maximum, colors become intensely saturated, often clipping to primary values.

---

#### Knob 5 — Dye Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the magnitude of LFSR-driven luminance displacement. Despite its TOML label of "Dye Depth," in the VHDL this register scales the raw LFSR output to produce a signed jitter offset that is added to the quantized Y channel. At 0%, no jitter is applied and quantized columns have perfectly uniform luminance. As the value increases, each pixel's brightness is perturbed by a pseudo-random amount, creating the characteristic irregular, hand-dyed look of ikat textiles. The jitter interacts with palette quantization: heavy quantization with moderate jitter produces pixels that occasionally jump between adjacent dye levels.

---

#### Knob 6 — Warmth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Mapped to the VHDL signal `s_color_shift` but not connected to any processing stage in the current implementation. Adjusting this control has no visible effect on the output. It is reserved for future functionality.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Axis** | Vert | Horiz |
| **8 — Palette Src** | Fixed | Video |
| **9 — Double Ikat** | Off | On |
| **10 — Noise** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control a mix of independent binary options and reserved controls. Toggle 7 (Axis) swaps the stripe direction between vertical and horizontal. Toggle 8 (Palette Src) is registered but unused in the current VHDL — it has no effect. Toggle 9 (Double Ikat) applies quantization on both axes simultaneously. Toggle 10 (Noise) animates the jitter pattern by advancing an accumulator on each vertical sync. Toggle 11 (Bypass) routes input directly to output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Ikat processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Ikat-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from simple column striping to full textile simulation, each building on the previous to engage more of the processing chain.

### Exercise 1: Basic Warp Stripes

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: ikat_source1_boat, after: ikat_ex1_s1 },
    { label: "Castle", before: ikat_source2_castle, after: ikat_ex1_s2 },
    { label: "Turtle", before: ikat_source3_turtle, after: ikat_ex1_s3 },
    { label: "Pattern", before: ikat_source4_pattern, after: ikat_ex1_s4 },
    { label: "Boy", before: ikat_source5_boy, after: ikat_ex1_s5 },
    { label: "Knit", before: ikat_source6_knit, after: ikat_ex1_s6 },
  ]}
/>
*Basic Warp Stripes — simulated result across source images.*
**Source**: A live camera feed or recorded footage with clearly defined subjects and moderate contrast.

**What You'll Create**: Learn how column width and palette quantization create the fundamental ikat stripe pattern.

1. **Set column width**: Turn Col Width to about 40%. Watch as the image divides into vertical stripes of uniform width.
2. **Quantize luminance**: Slowly increase Palette from minimum. Watch smooth gradients within each stripe collapse into flat tonal bands — like threads dipped in progressively fewer dye colors.
3. **Narrow the stripes**: Reduce Col Width toward 20%. The stripes become finer, more thread-like. Notice how the image's structure is still visible through the stripe pattern.
4. **Switch axis**: Flip the Axis toggle to Horiz. The stripes rotate 90 degrees, creating horizontal bands instead of vertical columns.
5. **Return to vertical**: Flip Axis back to Vert for the exercises that follow.

**Key concepts**: Column quantization divides the frame into stripes, palette quantization reduces tonal levels within stripes, independent axis control rotates the stripe pattern

---

### Exercise 2: Dye Bleed and Jitter

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: ikat_source1_boat, after: ikat_ex2_s1 },
    { label: "Castle", before: ikat_source2_castle, after: ikat_ex2_s2 },
    { label: "Turtle", before: ikat_source3_turtle, after: ikat_ex2_s3 },
    { label: "Pattern", before: ikat_source4_pattern, after: ikat_ex2_s4 },
    { label: "Boy", before: ikat_source5_boy, after: ikat_ex2_s5 },
    { label: "Knit", before: ikat_source6_knit, after: ikat_ex2_s6 },
  ]}
/>
*Dye Bleed and Jitter — simulated result across source images.*
**Source**: Footage with broad tonal gradients — skies, skin tones, or slowly-moving abstract video.

**What You'll Create**: Explore how edge bleed and LFSR jitter create the characteristic soft, hand-dyed ikat look.

1. **Establish stripes**: Set Col Width ~40%, Palette ~40% for visible column quantization.
2. **Add bleed**: Slowly increase Bleed Amt. Watch the hard edges between columns soften — chroma fades toward neutral at stripe boundaries, simulating dye seeping under the resist ties.
3. **Add jitter**: Increase Dye Depth from 0% to ~60%. Each pixel's brightness is now displaced by a pseudo-random amount, creating the fuzzy, uneven look of hand-dyed threads.
4. **Animate jitter**: Toggle Noise to On. The jitter pattern now shifts frame-by-frame, creating a shimmering, living textile effect.
5. **Boost saturation**: Increase Saturate above 50%. Watch colors intensify as if the virtual threads have been dipped in concentrated dye.

**Key concepts**: Bleed feathers chroma at column edges, LFSR jitter creates pseudo-random luminance displacement, noise animation adds temporal shimmer, saturation boost simulates concentrated dye

---

### Exercise 3: Double Ikat Textile

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: ikat_source1_boat, after: ikat_ex3_s1 },
    { label: "Castle", before: ikat_source2_castle, after: ikat_ex3_s2 },
    { label: "Turtle", before: ikat_source3_turtle, after: ikat_ex3_s3 },
    { label: "Pattern", before: ikat_source4_pattern, after: ikat_ex3_s4 },
    { label: "Boy", before: ikat_source5_boy, after: ikat_ex3_s5 },
    { label: "Knit", before: ikat_source6_knit, after: ikat_ex3_s6 },
  ]}
/>
*Double Ikat Textile — simulated result across source images.*
**Source**: High-contrast footage with strong geometric content — architecture, text, or patterned surfaces.

**What You'll Create**: Combine all processing stages to create a full double-ikat textile simulation.

1. **Start with fine stripes**: Set Col Width ~25%, Palette ~60% for a dense vertical stripe pattern.
2. **Heavy bleed and jitter**: Set Bleed Amt ~70%, Dye Depth ~80%. The stripe edges are now thoroughly feathered.
3. **Enable double ikat**: Toggle Double Ikat to On. Immediately, the vertical stripes gain a horizontal cross-quantization, creating a woven grid pattern.
4. **Maximum saturation**: Push Saturate to ~90%. Colors become vivid and over-dyed.
5. **Animate**: Enable Noise. The cross-hatched pattern shimmers and shifts per frame.
6. **Blend back**: Lower Mix to ~70% to let some of the original image show through the textile overlay, creating a fabric-over-video composite.

**Key concepts**: Double ikat applies quantization on both axes creating cross-hatched patterns, all processing stages compound to create full textile simulation, mix control layers texture over source

---


## Tips

- **Jitter creates the hand-dyed look**: The LFSR displacement is Ikat's signature effect. Without jitter, the quantized columns look mechanical and digital. With moderate jitter, they look like hand-dyed yarn.
- **Double ikat is computationally cheap but visually dramatic**: Enabling the double ikat toggle re-applies the same quantization mask on the perpendicular axis, creating a woven grid from what was previously a simple stripe pattern.
- **Feedback loops**: Routing the output back to the input creates recursive column quantization — each pass further reduces the tonal palette, simulating the visual effect of over-dyeing on already-dyed fabric.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed signal. Use it to judge how much textile texture has been added.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bit Mask** | A binary pattern used to selectively zero specific bits of a value, implementing quantization by preserving only the most significant bits. |
| **Bleed** | The soft transition zone at column boundaries where chroma fades toward neutral, simulating dye seeping under resist ties. |
| **Column Quantization** | Dividing the video frame into fixed-width vertical or horizontal stripes, within which pixel values are processed as a group. |
| **Double Ikat** | A textile technique (and this program's mode) where both warp and weft threads are pre-dyed, creating patterns on two axes simultaneously. |
| **Ikat** | A Malay-Indonesian dyeing technique where yarn is bound with resist material before dyeing, creating patterns with characteristically soft edges. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input is a linear function of its previous state, producing a pseudo-random sequence used for jitter generation. |
| **LUT** | Look-Up Table; FPGA logic resources used for combinational logic. Ikat uses approximately 700 LUTs. |
| **Resist** | A material (wax, string, rubber) that prevents dye from reaching covered portions of yarn, creating the pattern boundaries in ikat textiles. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
