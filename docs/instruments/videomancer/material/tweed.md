---
draft: true
sidebar_position: 269
slug: /instruments/videomancer/tweed
title: "Tweed"
image: /img/instruments/videomancer/tweed/tweed_hero.png
description: "Tweed is a textile simulator — it renders the geometric patterns of woven fabric directly onto the video signal."
---

import tweed_before_after from '/img/instruments/videomancer/tweed/tweed_before_after.png';
import tweed_control_panel from '/img/instruments/videomancer/tweed/tweed_control_panel.png';
import tweed_exercise1_result from '/img/instruments/videomancer/tweed/tweed_exercise1_result.png';
import tweed_exercise2_result from '/img/instruments/videomancer/tweed/tweed_exercise2_result.png';
import tweed_exercise3_result from '/img/instruments/videomancer/tweed/tweed_exercise3_result.png';
import tweed_hero from '/img/instruments/videomancer/tweed/tweed_hero.png';
import tweed_source1_kodim15 from '/img/instruments/videomancer/tweed/tweed_source1_kodim15.png';
import tweed_source2_kodim03 from '/img/instruments/videomancer/tweed/tweed_source2_kodim03.png';
import tweed_source3_kodim13_bw from '/img/instruments/videomancer/tweed/tweed_source3_kodim13_bw.png';

# Tweed

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={tweed_hero} alt="Tweed hero image"/>
*Tweed applying herringbone weave pattern with color fleck scattering to simulate traditional woven fabric texture.*
<img src={tweed_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Tweed applied.*

---

## Overview

Tweed is a textile simulator — it renders the geometric patterns of woven fabric directly onto the video signal. The characteristic zigzag of herringbone cloth emerges from alternating diagonal stripe directions in horizontal bands, while an LFSR noise source scatters random color flecks across the weave to simulate the multi-colored fiber inclusions found in natural tweed fabric.

The program chains six processing stages: band and diagonal computation, herringbone stripe classification, weave color composition with palette tinting, color fleck scattering, contrast adjustment, and wet/dry crossfade mixing. The name references the coarse, heavy woolen fabric traditionally produced in Scotland and Ireland — distinguished by its herringbone patterns and flecked, multi-toned appearance.

At conservative settings Tweed adds a subtle woven texture to any video source, like viewing the image through a fabric screen. At extreme settings the herringbone pattern dominates, reducing the video to a rhythmic lattice of interlocking chevrons punctuated by random color speckles.

---

## Background

### Herringbone Geometry

The herringbone pattern is one of the oldest weaving arrangements, named after the resemblance to the skeletal structure of a herring fish. It consists of diagonal stripes — but unlike a simple twill, the diagonal direction reverses at regular intervals along the vertical axis. This reversal creates the characteristic zigzag or chevron appearance. In Tweed, the screen is divided into horizontal bands of configurable height. In even bands, the diagonal is computed as `(h + v)`, running upper-left to lower-right. In odd bands, the diagonal reverses to `(h − v)`, running upper-right to lower-left. The transition between band directions creates the zigzag vertex.

### Warp and Weft

In real weaving, the warp threads run lengthwise on the loom while the weft threads run crosswise, interlacing with the warp. In any given position, either the warp or the weft thread is on top, creating the visible pattern. Tweed classifies each pixel as either warp or weft by comparing the diagonal position within the stripe repeat against a visibility threshold. Warp pixels receive a slight brightness boost; weft pixels are slightly dimmed. This alternation creates the characteristic light-and-dark interleaving of woven cloth.

### Color Flecking in Tweed Cloth

Traditional tweed fabrics — particularly Harris Tweed and Donegal Tweed — are distinguished by their color flecks: small inclusions of contrasting fibers scattered throughout the weave. These flecks arise from the spinning process, where short lengths of colored fiber are blended into the yarn. Tweed simulates this effect using a 16-bit LFSR (linear feedback shift register) that generates pseudo-random noise. When the LFSR output falls below a density threshold, the pixel's chrominance is offset by a random amount, creating scattered spots of shifted color throughout the fabric pattern.

### Contrast Expansion

The contrast stage operates around the midpoint value of 512 in the 10-bit domain. It measures the distance of each pixel's luma from this center and expands that distance by a configurable factor. Pixels brighter than mid-gray become brighter; pixels darker than mid-gray become darker. The effect sharpens the visual distinction between warp and weft threads, making the weave pattern more pronounced.

### Palette Tinting

Tweed offers two palette modes for the weave color. The warm palette applies a brown-toned tint by shifting chrominance — decreasing U and increasing V, simulating the earth tones of traditional tweed. The cool palette desaturates the chroma toward neutral gray by averaging each channel toward the midpoint. This tinting is applied before fleck scattering, so the flecks scatter around the palette's base color.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Band/Diagonal Computation ────────
│   ├─ Animation offset applied to horizontal position
│   ├─ Determine even/odd band from v_count bit
│   ├─ Herringbone: even=(h+v), odd=(h-v)
│   └─ Twill: all bands same direction (h+v)
│
├── Stage 2: Herringbone Stripe Test + Fleck Test ──────────────
│   ├─ Diagonal fraction vs weave threshold → warp/weft
│   ├─ LFSR output vs density threshold → fleck trigger
│   └─ Pre-compute fleck U/V offsets from LFSR bits
│
├── Stage 3: Weave Color Compose + Fleck Scatter ───────────────
│   ├─ Warp: source + (source >> 3)  [brighter]
│   ├─ Weft: source - (source >> 3)  [darker]
│   ├─ Palette tint: warm brown or cool gray
│   └─ If fleck: add random U/V offset + slight Y variation
│
├── Stage 4: Contrast Adjust + Clamp ──────────────────────────
│   ├─ Expand luma around midpoint (512)
│   └─ Clamp to [0, 1023]
│
├── Mix Stage (4 clk interpolator_u × 3 channels) ─────────────
│   └─ Crossfade between dry input and wet processed
│
├── Sync Delay Pipeline ────────────────────────────────────────
│   └─ 8-clock delay for sync alignment
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select original or processed signal
```

The key interaction in Tweed's pipeline is the sequence of warp/weft classification followed by palette tinting followed by fleck scattering. The diagonal computation in Stage 1 determines the weave geometry — herringbone reversal creates the zigzag by flipping the sign of the vertical component in alternating bands. The fleck scatter in Stage 3 then randomizes chroma on top of this structured pattern, so the color noise respects the underlying weave rather than obscuring it.

The contrast stage operates downstream of all weave and fleck processing. This means higher contrast settings amplify both the warp/weft brightness difference and any fleck-induced luma variation, making the textile texture more visually prominent.

---

## Parameter Reference

<img src={tweed_control_panel} alt="Videomancer front panel with Tweed loaded"/>
*Videomancer's front panel with Tweed active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Zigzag W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the zigzag stripe width — the diagonal repeat period of the herringbone pattern. The pot value maps to one of five power-of-two stripe masks: 4, 8, 16, 32, or 64 pixels. Low values create fine, dense herringbone with tightly packed chevrons. High values create bold, wide zigzag stripes. The stripe width determines the fundamental scale of the weave — every other visual element (warp/weft alternation, fleck density, thread structure) operates within this repeating cell.

---

#### Knob 2 — Band Hght
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the horizontal band height — the vertical interval at which the herringbone direction reverses. Mapped to power-of-two band sizes: 8, 16, 32, 64, 128, or 256 pixels. Small bands create rapid zigzag reversals with many chevron vertices visible on screen. Large bands create long diagonal runs before reversing, producing a gentler, more elongated herringbone. The ratio between stripe width and band height defines the visual aspect ratio of the chevron pattern.

---

#### Knob 3 — Fleck Den
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls fleck density — the probability that any given pixel will receive a random color scatter. The pot value is mapped to a 16-bit threshold compared against the LFSR output. At 0%, no flecks appear and the weave has uniform coloring. At 100%, nearly every pixel receives a color offset, creating a heavily speckled, almost noisy appearance. Mid-range settings around 30–50% best simulate the look of traditional flecked tweed fabric.

---

#### Knob 4 — Color Sct
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the color scatter amount — how far the fleck offset shifts the pixel's chrominance from its base value. Higher values produce more vivid, contrasting flecks that stand out strongly against the weave background. Lower values create subtle tonal variations that require close viewing to distinguish. The scatter is applied independently to U and V channels using different LFSR bit ranges, so each fleck has an unpredictable hue shift.

---

#### Knob 5 — Weave Vis
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls weave visibility — the threshold that determines the balance between warp and weft thread visibility within each stripe repeat. At low values, the warp region is narrow and the weft dominates, creating a predominantly dark weave. At high values, the warp dominates, creating a predominantly bright weave. The sweet spot around 50% produces the most balanced herringbone pattern with equal warp and weft coverage.

---

#### Knob 6 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Contrast boost for the final processed output. Expands luma values around the 512 midpoint: higher settings increase the brightness difference between warp and weft threads, making the weave pattern sharper and more defined. The VHDL uses a stepped approach — four contrast levels selected by threshold ranges on the pot value — rather than continuous multiplication.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Weave** | Herring | Twill |
| **8 — Palette** | Harris | Donegal |
| **9 — Flecks** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–10 each control a single bit in the toggle register. Despite the TOML specifying four-option labels for some toggles, the VHDL reads only single bits — all toggles function as two-state switches. Toggle 11 controls the bypass mux, routing the delayed input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade mix. At 100%, the output is the fully processed tweed-textured signal. At 0%, the output is the unprocessed input. Intermediate values blend via three parallel interpolator_u instances (one per YUV channel) running over 4 clock cycles. This allows the tweed texture to be subtly overlaid on the source video rather than replacing it entirely.

---

## Guided Exercises

These exercises progress from basic herringbone geometry through color palette exploration to full textile simulation with fleck scattering. Each reveals a different aspect of the weave pattern generation and its interaction with the source video.

### Exercise 1: Herringbone Geometry

<img src={tweed_exercise1_result} alt="Herringbone Geometry result"/>
*Herringbone Geometry — simulated result across source images.*
**Source**: A live camera feed or recorded footage with moderate brightness variation and recognizable subjects.

**Objective**: Understand how stripe width and band height interact to define the herringbone chevron pattern.

1. **Disable flecks**: Toggle Flecks Off to see the pure weave geometry.
2. **Set mid-range weave visibility**: Weave Vis ~50% for balanced warp/weft.
3. **Wide stripes, short bands**: Set Zigzag W high (~80%), Band Hght low (~20%). Observe broad diagonal stripes with frequent direction reversals.
4. **Narrow stripes, tall bands**: Reverse — Zigzag W low (~20%), Band Hght high (~80%). Observe fine, dense stripes with long diagonal runs.
5. **Toggle pattern**: Switch Weave to Twill. The zigzag disappears, replaced by uniform diagonal stripes. Switch back to Herringbone.
6. **Animate**: Toggle Animate On. Watch the herringbone scroll horizontally. Toggle Off to freeze.

**Key concepts**: Band height controls zigzag frequency, stripe width controls diagonal density, herringbone reverses direction per band while twill does not, animation scrolls the pattern horizontally

---

### Exercise 2: Color Palettes and Tinting

<img src={tweed_exercise2_result} alt="Color Palettes and Tinting result"/>
*Color Palettes and Tinting — simulated result across source images.*
**Source**: Footage with varied color content — nature scenes, graphics, or multi-colored subjects.

**Objective**: Compare warm and cool palette tints and explore how the warp/weft brightness modulation interacts with source video color.

1. **Set moderate weave**: Zigzag W ~50%, Band Hght ~50%, Weave Vis ~60%.
2. **Warm palette**: Set Palette to Harris (warm brown tint). Notice the U/V shift adding earthy warmth.
3. **Cool palette**: Switch Palette to Donegal (cool gray). The weave desaturates toward neutral.
4. **Increase contrast**: Push Contrast to ~75%. The warp/weft brightness difference becomes more pronounced.
5. **Reduce contrast**: Pull Contrast to ~25%. The weave pattern nearly vanishes into uniform tone.
6. **Blend with mix**: Pull Mix to ~60% to overlay the weave as a subtle texture rather than full replacement.

**Key concepts**: Warm palette shifts chroma toward brown, cool palette desaturates toward gray, contrast amplifies the warp/weft brightness difference, mix blends the textured result with the original

---

### Exercise 3: Full Tweed Simulation

<img src={tweed_exercise3_result} alt="Full Tweed Simulation result"/>
*Full Tweed Simulation — simulated result across source images.*
**Source**: Footage with recognizable content — the fleck effect is most visible against identifiable subjects where scattered color spots contrast with the underlying image.

**Objective**: Combine all stages — herringbone geometry, palette tinting, and color fleck scattering — to simulate a full tweed fabric overlay.

1. **Set the weave**: Zigzag W ~40%, Band Hght ~40%, Weave Vis ~50% for a medium-density herringbone.
2. **Enable flecks**: Toggle Flecks On. Set Fleck Den ~40% for moderate density.
3. **Set scatter**: Color Sct ~50% for visible but not overwhelming color offsets.
4. **Warm palette**: Set Palette to Harris for classic tweed tones.
5. **Add contrast**: Contrast ~60% to sharpen the weave.
6. **Animate**: Toggle Animate On. The scrolling weave with scattered flecks simulates fabric being pulled across the screen.
7. **Final mix**: Adjust Mix to taste — 100% for full fabric effect, or ~70% for a textured overlay.

**Key concepts**: Fleck density controls the probability of color scatter per pixel, scatter amount controls the magnitude of the chrominance offset, LFSR noise provides pseudo-random distribution, all stages compound to create a convincing textile simulation

---


## Tips

- **Zigzag W and Band Hght ratio**: The visual proportion of the chevron pattern is determined by the ratio between stripe width and band height. Equal values produce 45-degree chevrons. Increasing band height relative to stripe width flattens the zigzag.
- **Subtle overlay**: Use Mix at ~50–60% to overlay the tweed texture on source video without completely obscuring the content. This creates a convincing "viewed through fabric" effect.
- **Fleck density sweet spot**: Around 30–40% fleck density produces the most realistic tweed simulation. Higher densities overwhelm the weave structure with noise.
- **Contrast for definition**: Moderate contrast (~50–70%) makes the weave visible without crushing the luma range. Lower contrast produces a softer, more muted textile feel.
- **Cool palette for monochrome**: The cool gray palette combined with reduced fleck scatter creates a clean, modern herringbone pattern suitable for graphic compositions.
- **Animation for motion graphics**: Enable Animate to scroll the weave pattern. Combined with a static source, this creates a fabric-pulling effect suitable for transitions or background textures.
- **Feedback routing**: Route the output back to the input to create recursive weave patterns — each pass adds another layer of herringbone geometry.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | The ITU-R standard defining the color matrix used to convert between RGB and YUV in video systems. |
| **Fleck** | A small inclusion of contrasting-colored fiber in tweed fabric; simulated by LFSR-driven random chrominance scatter. |
| **Herringbone** | A zigzag weave pattern created by reversing the diagonal direction in alternating horizontal bands; named after the skeletal structure of herring fish. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **Proc amp** | Processing amplifier; a gain-and-offset stage that applies contrast (multiplication) and brightness (addition) to a signal. |
| **Twill** | A weave pattern with uniform diagonal lines running in one direction without reversal; the non-zigzag counterpart to herringbone. |
| **Warp** | The set of lengthwise threads on a loom; in Tweed, pixels classified as warp receive a slight brightness boost. |
| **Weft** | The crosswise threads that interlace with the warp; in Tweed, weft pixels receive a slight brightness reduction. |
