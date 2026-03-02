---
draft: true
sidebar_position: 8
slug: /instruments/videomancer/antic
title: "Antic"
image: /img/instruments/videomancer/antic/antic_hero.png
description: "Antic recreates the distinctive display modes of the Atari 8-bit computer's GTIA (George's Television Interface Adapter) graphics chip."
---

import antic_hero from '/img/instruments/videomancer/antic/antic_hero.png';
import antic_before_after from '/img/instruments/videomancer/antic/antic_before_after.png';
import antic_control_panel from '/img/instruments/videomancer/antic/antic_control_panel.png';
import antic_exercise1_result from '/img/instruments/videomancer/antic/antic_exercise1_result.png';
import antic_exercise2_result from '/img/instruments/videomancer/antic/antic_exercise2_result.png';
import antic_exercise3_result from '/img/instruments/videomancer/antic/antic_exercise3_result.png';

# Antic

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={antic_hero} alt="Antic hero image"/>
*Antic rendering a DLI rainbow gradient in Mode 9 over a portrait source — the per-scanline hue cycling produces the signature Atari raster-bar effect with 16-level luminance quantization.*
<img src={antic_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Antic applied.*

---

## Overview

Antic recreates the distinctive display modes of the Atari 8-bit computer's GTIA (George's Television Interface Adapter) graphics chip. The program processes input video through three selectable colour constraint modes — Mode 9 (single hue, 16 luminance levels), Mode 10 (9-colour palette nearest-match), and Mode 11 (16 hues at a single luminance) — that defined the visual identity of the Atari 400/800 and XL/XE computers. Each mode imposes a specific relationship between hue and luminance that produces results impossible to replicate with generic posterization or palette reduction.

The name *Antic* references the ANTIC (Alpha-Numeric Television Interface Controller) chip designed by Jay Miner for the Atari 8-bit family. The ANTIC chip worked in tandem with the GTIA to produce the Atari's unique graphics capabilities. The most famous technique enabled by this hardware was the **Display List Interrupt** (DLI) — a per-scanline interrupt that allowed programmers to change the background colour register on every scanline, creating the rainbow gradient backgrounds and "raster bar" effects that became the visual signature of Atari demos and games like *Rescue on Fractalus*, *Star Raiders*, *Alternate Reality*, and *M.U.L.E.*

At conservative settings — Mode 9 with DLI disabled and moderate saturation — the program produces clean monochromatic images tinted in any of 16 authentic Atari hues. At extreme settings — Mode 10 with DLI cycling and artifact fringing — the image transforms into a vivid, illustrated mosaic of shifting colour bands that captures the raw, unmistakable energy of 1980s Atari home computer graphics.

---

## Background

### What Is the Atari GTIA?

The **GTIA** (George's Television Interface Adapter) was a custom graphics chip designed by George McLeod for Atari's 8-bit home computers, first shipping in the Atari 400 and 800 in 1979. While most home computers of that era offered simple bitmap modes with fixed colour capabilities, the GTIA provided three unique high-resolution modes that each imposed a different constraint on the relationship between hue and luminance. These constraints were not limitations — they were a deliberate design choice that gave programmers fine control over either colour or luminance, trading one for the other in ways that produced visually distinctive results. No other computer of the era offered this particular combination of modes.

The GTIA operated alongside the ANTIC chip, which handled display list processing (the Atari's equivalent of a display mode table). Together, ANTIC and GTIA allowed programmers to mix different graphics modes on the same screen, change colour registers per scanline, and produce visual effects that were architecturally unique to the Atari platform.

### What Are GTIA Modes 9, 10, and 11?

**GTIA Mode 9** provides 16 luminance levels at a single hue. Every pixel shares the same colour (set by the background register COLBK), but each pixel can independently display one of 16 brightness levels. The result is a monochromatic image — think of a photograph printed in sepia, amber, or any chosen tint — with smooth tonal gradation. This mode was used extensively for title screens, loading screens, and atmospheric scenes like the eerie green landscapes of *Rescue on Fractalus*.

**GTIA Mode 10** maps each pixel to the nearest colour in a 9-colour palette loaded from the Atari's hardware colour registers (COLPM0–COLPM3, COLPF0–COLPF3, plus COLBK). This produces an illustrated, paint-by-numbers look — the image is reduced to just 9 distinct colours, each independently chosen. The nearest-match algorithm uses Manhattan distance in YUV space to find the closest palette entry for each pixel.

**GTIA Mode 11** provides 16 hues at a single luminance level. This is the inverse of Mode 9: every pixel shares the same brightness, but each pixel can display one of 16 hues from the Atari colour wheel. The result is a flat hue-map where colour variation is preserved but tonal range is eliminated — like a false-colour thermal image.

### What Is a Display List Interrupt (DLI)?

A **Display List Interrupt** (DLI) is a technique where the CPU is interrupted on specific scanlines during video output, allowing it to modify colour registers between scanlines. On the Atari, this was used primarily to create effects that required more colours than a single mode could display. The most iconic use was cycling the hue register every scanline to create a rainbow gradient background — a smooth vertical spectrum of colours that became the visual calling card of the Atari demoscene.

In this program, the DLI is simulated by a phase accumulator that increments on every horizontal sync pulse. The phase determines an offset added to the base hue register, causing the active hue to change smoothly from top to bottom of the frame. The DLI Rate controls how quickly the hue cycles, and the DLI Offset controls where in the colour wheel the gradient starts.

### What Are NTSC and PAL Colour Differences?

The Atari 8-bit computers used different colour encoding depending on the television standard. **NTSC** (North America, Japan) Atari systems produced 16 hues with specific colour points derived from the NTSC colour subcarrier phase. **PAL** (Europe, Australia) systems produced 16 hues at slightly different colour points, due to the different colour encoding of the PAL standard. Programmers and artists learned to account for these differences — artwork that looked correct on an NTSC system could appear with shifted hues on PAL, and vice versa. This program includes both authentic hue tables so users can switch between the two colour systems.

### What Are Artifact Colours?

**Artifact colours** were unintentional but exploitable colour effects caused by the interaction between the Atari's high-resolution pixel clock and the NTSC colour subcarrier frequency. When adjacent pixels had different hue values, the colour transition produced a brief fringe of intermediate colour — an electromagnetic artefact of the analog encoding. Demo programmers deliberately exploited these fringes to create apparent colour detail beyond what the hardware officially supported. In this program, artifact mode simulates this fringing by blending intermediate UV values at hue transitions.


---

## Signal Flow

```
Input Video (YUV 4:4:4 30-bit)
│
├── Y Channel ──────────────────────────────────────────────────────
│   │
│   ├─ 1a. Gain partial products     (10×5 split multiply by Luma Gain)
│   ├─ 1b. Gain combine + Brightness (combine PP + offset by Brightness pot)
│   ├─ 2.  DLI phase + hue select    (phase accum per scanline → hue LUT)
│   ├─ 3.  GTIA mode switch          (Mode 9: quantize Y to 16 levels)
│   │                                 (Mode 10: pass Y to palette matcher)
│   │                                 (Mode 11: pass Y, extract hue from UV)
│   │                                 (Mode "11": Mode 9+DLI forced)
│   ├─ 3a–3d. Mode 10 pipeline       (9-entry Manhattan distance matcher,
│   │         (8 clocks)               pipelined 3-at-a-time reduce tree)
│   ├─ 3d. Merge mux                 (select Mode 10 result or immediate)
│   ├─ 4a. Saturation: center+mag    (U/V − 512, take absolute value)
│   ├─ 4b. Saturation: partial prods (10×5 split multiply by Saturation)
│   ├─ 4c. Saturation: combine+clamp (reconstruct U/V around midpoint)
│   ├─ 5.  Artifact fringe           (blend intermediate UV at hue changes)
│   └─ 6.  Output register
│
├── U/V Channels ───────────────────────────────────────────────────
│   │
│   ├─ 2.  Hue LUT lookup            (NTSC or PAL table, 16 entries)
│   ├─ 3.  Mode-dependent UV         (Mode 9: from hue LUT)
│   │                                 (Mode 10: from 9-colour palette)
│   │                                 (Mode 11: from hue extraction → LUT)
│   ├─ 4a–c. Saturation scaling      (scale UV offset from midpoint)
│   └─ 5.  Artifact fringe           (conditional UV blending)
│
├── Sync Signals ───────────────────────────────────────────────────
│   └─ 22-clock delay pipeline        (align with processing depth)
│
├── Interpolator (4 clocks per channel) ────────────────────────────
│   └─ Mix = lerp(input_delayed, processed, mix_amount)
│
└── Output ─────────────────────────────────────────────────────────
    └─ Y/U/V from interpolator mix
```

The processing chain has two main paths that must be delay-aligned. The "immediate" GTIA path (Modes 9, 11, and the mode "11" variant) produces output in a single clock after the gain/brightness stage but must wait 8 additional clocks in a delay pipeline to align with the Mode 10 palette matcher, which requires 8 pipeline stages to compute Manhattan distances against all 9 palette entries using a pipelined 3-at-a-time reduction tree. A mode select signal is also delayed 8 clocks so the merge mux at stage 3d can choose the correct result.

The saturation stage operates on UV channels after the GTIA mode processing. It centers U and V around the midpoint (512), takes the magnitude, multiplies by the Saturation pot using split partial products (to fit iCE40 multiplier resources), then reconstructs the offset with the original sign. This means saturation scales the chroma intensity of the GTIA-processed colour, not the original input colour. The artifact fringe stage sits between saturation and the output register, conditionally blending UV values at hue transitions when artifact mode is enabled.

---

## Parameter Reference

<img src={antic_control_panel} alt="Videomancer front panel with Antic loaded"/>
*Videomancer's front panel with Antic active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Base Hue
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Selects the base hue from the Atari colour wheel. The 16 hue positions match the authentic Atari GTIA hue register values: Gray, Gold, Orange, Red-Orange, Pink, Purple, Violet-Blue, Blue, Medium Blue, Light Blue, Turquoise, Green-Blue, Green, Yellow-Green, Orange-Green, and Light Orange. In Mode 9, this hue is applied to every pixel in the image. In Mode 11, this selects the starting point for hue quantization. When DLI is enabled, this sets the base hue from which the per-scanline rainbow effect begins cycling. The stepped control gives 16 discrete positions, each mapping to a specific entry in either the NTSC or PAL hue lookup table.

---

#### Knob 2 — DLI Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the speed of the per-scanline DLI hue cycling effect. At 0%, the hue does not change between scanlines — the base hue applies uniformly across the entire frame. As the rate increases, the hue register advances faster per scanline, compressing more of the colour wheel into the vertical height of the frame. At moderate values, a gentle rainbow gradient appears from top to bottom. At maximum, the hue cycles through the entire colour wheel multiple times per frame, producing dense horizontal colour banding. This control only has a visible effect when DLI Enable (Toggle 9) is on. The DLI phase accumulator uses a 32-bit register, so the rate-to-visual-speed mapping is extremely smooth.

---

#### Knob 3 — Luma Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the pre-processing luminance gain applied to the input video before GTIA mode processing. This scales the input Y channel before quantization or palette matching, effectively controlling how the input video's tonal range maps into the GTIA mode's available levels. At low values, the input is darkened and more luminance levels cluster near black. At 50%, gain is approximately unity. At maximum, the input is brightened and highlights are pushed toward saturation. In Mode 9, where Y is quantized to 16 levels, the gain control determines which part of the tonal range receives the most distinct quantization steps.

---

#### Knob 4 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the chroma intensity of the processed output. The saturation stage scales the distance of U and V values from the chroma midpoint (512). At 0%, the output is fully desaturated — all chroma information is removed regardless of GTIA mode. At the default (approximately 75%), colours appear vivid and match the standard Atari palette intensity. At maximum, colours are pushed towards the gamut boundary, producing hyper-saturated results. This control interacts with all three GTIA modes: in Mode 9, it intensifies or desaturates the single hue applied to the image; in Mode 10, it adjusts the saturation of the 9-colour palette; in Mode 11, it controls the vividness of the per-pixel hue map.

---

#### Knob 5 — DLI Offset
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the starting phase of the DLI rainbow gradient. At 0%, the rainbow begins at the base hue (Knob 1) and cycles upward through the colour wheel. Increasing the offset rotates the starting point of the gradient, shifting which colour appears at the top of the frame. This allows the user to position specific colours at specific vertical positions on screen. The offset and rate together define the complete gradient: the rate sets how many cycles per frame, and the offset sets where each cycle begins. Like DLI Rate, this control only has a visible effect when DLI Enable (Toggle 9) is on.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Adds a constant brightness offset to the gain-scaled luminance. At 50%, brightness is neutral — no offset is applied. Below 50%, the entire image is darkened by subtracting from the luma channel. Above 50%, the image is brightened. The brightness offset is applied after the gain stage but before GTIA mode processing, so it shifts the input's tonal range within the GTIA quantization space. Combined with Luma Gain, this provides full control over how the input video maps into the GTIA mode's available luminance levels.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — GTIA Sel A** | Off | On |
| **8 — GTIA Sel B** | Off | On |
| **9 — DLI Enable** | Off | On |
| **10 — Pal/NTSC** | NTSC | PAL |
| **11 — Artifacts** | Clean | Artifact |

Switches 7 and 8 form a **combined 2-bit mode selector** controlling which GTIA display mode is active. The four combinations map to: 00 = Mode 9 (single hue, 16 luminance), 01 = Mode 10 (9-colour palette), 10 = Mode 11 (16 hues, single luminance), 11 = Mode 9 with DLI forced on. Switches 9–11 are **independent binary controls**: DLI Enable turns the per-scanline rainbow cycling on or off, PAL/NTSC selects the colour palette, and Artifacts enables the colour fringing simulation.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 100 |

Wet/dry crossfade between the original input video (delayed to match the 22-clock processing pipeline) and the GTIA-processed output. At 0%, the output is pure unprocessed input. At 100%, the output is fully processed through the selected GTIA mode. Intermediate positions blend the two, allowing the Atari colour constraints to be superimposed over the original footage at any opacity.

---

## Guided Exercises

These exercises progress from basic single-mode rendering to full DLI rainbow compositions, each building on familiarity with the GTIA mode constraints.

### Exercise 1: Mode 9 Monochrome Tinting

<img src={antic_exercise1_result} alt="Mode 9 Monochrome Tinting result"/>
*Mode 9 Monochrome Tinting — simulated result across source images.*
**Source**: Camera feed or recorded footage with varied brightness — portraits work well to show luminance quantization.

**Objective**: Understand how Mode 9 reduces the image to a single hue with 16 luminance levels and how the Base Hue selector changes the colour character.

1. **Set Mode 9**: Ensure both GTIA Sel A (Toggle 7) and GTIA Sel B (Toggle 8) are off. DLI Enable (Toggle 9) off.
2. **Unity settings**: Set Luma Gain and Brightness to ~50%, Saturation to ~75%, Mix to 100%.
3. **Gray wash**: Set Base Hue (Knob 1) to step 1 (Gray). The image appears as a 16-level grayscale — no colour, just luminance quantization with visible banding.
4. **Amber tint**: Rotate Base Hue to step 2 (Gold). The same luminance structure now glows in warm amber. Notice how tonal gradation is preserved while all chroma information becomes monochromatic.
5. **Cool blue**: Continue to step 8 (Blue). The image shifts to cold blue. Shadows become deep navy, highlights become pale sky blue.
6. **Adjust gain**: Turn Luma Gain (Knob 3) down to ~25%. The quantization bands compress into the dark end — the image becomes a dark, moody rendering with most levels concentrated in the shadows.
7. **Boost brightness**: Raise Brightness (Knob 6) to ~70%. The compressed levels shift upward, producing a blown-out, high-key monochrome image.

**Key concepts**: GTIA Mode 9 luminance quantization, single-hue constraint, Atari hue wheel, gain and brightness mapping into quantized tonal space

---

### Exercise 2: DLI Rainbow Gradient

<img src={antic_exercise2_result} alt="DLI Rainbow Gradient result"/>
*DLI Rainbow Gradient — simulated result across source images.*
**Source**: Any video source — the DLI rainbow is most visible on dark or moderately exposed content.

**Objective**: Learn how the DLI per-scanline hue cycling creates a rainbow gradient and how Rate and Offset control its appearance.

1. **Start from Mode 9**: Both mode toggles off, Mix at 100%, moderate Saturation (~75%).
2. **Enable DLI**: Switch DLI Enable (Toggle 9) to On. A rainbow gradient appears from top to bottom.
3. **Slow rate**: Set DLI Rate (Knob 2) to ~15%. The gradient is gentle — one partial cycle of the colour wheel spans the full frame height.
4. **Increase rate**: Turn DLI Rate to ~60%. Multiple rainbow cycles compress into the frame, producing the dense horizontal banding characteristic of Atari demo raster bars.
5. **Shift offset**: Sweep DLI Offset (Knob 5). The rainbow slides vertically — different hues anchor at the top of the frame as the offset rotates the starting phase.
6. **Maximum saturation**: Push Saturation (Knob 4) to 100%. The rainbow bands become hyper-vivid.
7. **Try PAL**: Switch PAL/NTSC (Toggle 10) to PAL. The same gradient now uses slightly shifted hue points — notice the differences in blue and green tones.

**Key concepts**: Display List Interrupt simulation, per-scanline hue cycling, phase accumulator, DLI rate and offset interaction, NTSC vs PAL palette differences

---

### Exercise 3: Mode 10 Illustrated Palette with Artifact Fringe

<img src={antic_exercise3_result} alt="Mode 10 Illustrated Palette with Artifact Fringe result"/>
*Mode 10 Illustrated Palette with Artifact Fringe — simulated result across source images.*
**Source**: Camera feed or recorded footage with saturated colours — subjects wearing colourful clothing or outdoor scenes with sky and vegetation.

**Objective**: Explore Mode 10 nearest-match palette mapping and combine it with DLI cycling and artifact colour fringing for the most complex Atari emulation.

1. **Select Mode 10**: Set GTIA Sel A (Toggle 7) to On, GTIA Sel B (Toggle 8) to Off. The image snaps into a 9-colour illustrated look — each pixel mapped to the nearest palette colour.
2. **Observe palette**: The 9 fixed colours (black, orange, blue, green, pink, turquoise, gold, yellow-green, white) create a distinctive paint-by-numbers appearance.
3. **Adjust gain**: Vary Luma Gain (Knob 3). The gain shifts which palette entries dominate — low gain emphasises dark colours (black, orange, blue), high gain pushes toward light colours (gold, yellow-green, white).
4. **Enable DLI**: Switch DLI Enable (Toggle 9) on. The rainbow cycling overlays the palette-matched image, creating horizontal colour banding.
5. **Enable artifacts**: Switch Artifacts (Toggle 11) to Artifact. At hue transitions in the DLI gradient, colour fringing appears — brief intermediate hues at the boundary between rainbow bands.
6. **Increase DLI rate**: Push DLI Rate to ~80%. Dense rainbow bands with artifact fringing at each boundary — this is the maximally complex Atari look.
7. **Desaturate**: Pull Saturation (Knob 4) to ~30%. The palette colours become pastel, softening the illustrated appearance.

**Key concepts**: Mode 10 nearest-match palette mapping, Manhattan distance in YUV, DLI + Mode 10 combination, artifact colour fringing at hue transitions, saturation control over palette vividness

---


## Tips

- **Processing order matters**: Input gain and brightness are applied *before* GTIA mode processing. Adjust gain and brightness to control how the input maps into the GTIA quantization — this is the primary creative control for shaping the final look.
- **Mode 9 is the signature Atari effect**: The 16-level monochrome tint is the most instantly recognizable Atari visual. Use Gold (step 2) or Green (step 13) for the most nostalgic Atari feel.
- **DLI Rate and Offset are the rainbow controls**: Rate compresses or expands the rainbow gradient. Offset slides it. Together they position any colour at any vertical position on screen.
- **Mode 10 is computationally expensive**: The 9-colour palette matcher uses an 8-stage pipelined reduction tree. Mode 9 and 11 produce results faster but are delay-aligned. There is no visual difference in output timing — the alignment is handled internally.
- **Saturation scales the GTIA output**: The saturation control operates after GTIA mode processing, not on the original input. Desaturating to 0% makes all modes monochrome. Boosting saturation intensifies the palette colours.
- **Artifact mode needs DLI**: Artifact fringing simulates NTSC colour encoding artefacts at hue transitions. Without DLI or rapid hue changes, there are no transitions to fringe. Enable DLI for the most visible artifact effect.
- **Feedback loops create recursive posterization**: Routing the output back to the input causes GTIA processing to be applied iteratively. Mode 9 feedback quickly converges to a few luminance levels. Mode 10 feedback locks the image to the 9-colour palette in one or two passes.
- **Bypass for A/B comparison**: Use the Mix fader (Fader 12) to blend between original and processed, or toggle Bypass for an instant comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **ANTIC** | Alpha-Numeric Television Interface Controller; the Atari 8-bit display list processor chip that worked alongside the GTIA to produce the Atari's unique graphics modes. |
| **Artifact colours** | Unintentional colour fringes produced by the interaction between pixel hue transitions and the NTSC colour subcarrier frequency, deliberately exploited by demo programmers for additional colour detail. |
| **Chroma** | The colour information in a video signal, represented by the U and V channels in YUV encoding. |
| **DLI** | Display List Interrupt; a per-scanline CPU interrupt on the Atari that allows colour register changes between scan lines to create rainbow gradient effects. |
| **GTIA** | George's Television Interface Adapter; the Atari 8-bit graphics chip providing Modes 9, 10, and 11, each imposing a different constraint on the relationship between hue and luminance. |
| **iCE40** | The Lattice Semiconductor FPGA family used in Videomancer's hardware. |
| **LUT** | Lookup Table; a stored array mapping input values to output values, used here for hue-to-UV conversion. |
| **Manhattan distance** | The sum of absolute differences between corresponding coordinates; used in Mode 10 to find the nearest palette colour in YUV space. |
| **NTSC** | National Television System Committee; the analog colour television standard used in North America and Japan, with 16 hue points specific to the Atari colour subcarrier. |
| **PAL** | Phase Alternating Line; the analog colour television standard used in Europe and Australia, with slightly shifted hue points compared to NTSC. |
| **Phase accumulator** | A digital counter that increments by a fixed step each cycle and wraps at overflow, generating a repeating ramp waveform used for DLI hue cycling. |
| **Quantization** | The process of mapping a continuous range of values to a finite set of discrete levels; in Mode 9, input luminance is quantized to 16 levels. |
| **YUV** | A colour model separating luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
