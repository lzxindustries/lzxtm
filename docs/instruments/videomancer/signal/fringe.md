---
draft: true
sidebar_position: 122
slug: /instruments/videomancer/fringe
title: "Fringe"
image: /img/instruments/videomancer/fringe/fringe_hero_s1.png
description: "Before the era of component video and digital interfaces, nearly all consumer video passed through a single wire — the composite cable."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import fringe_control_panel from '/img/instruments/videomancer/fringe/fringe_control_panel.png';
import fringe_source1_runner from '/img/instruments/videomancer/fringe/fringe_source1_runner.png';
import fringe_source2_dog from '/img/instruments/videomancer/fringe/fringe_source2_dog.png';
import fringe_source3_collage from '/img/instruments/videomancer/fringe/fringe_source3_collage.png';
import fringe_source4_pattern from '/img/instruments/videomancer/fringe/fringe_source4_pattern.png';
import fringe_source5_woman from '/img/instruments/videomancer/fringe/fringe_source5_woman.png';
import fringe_source6_knit from '/img/instruments/videomancer/fringe/fringe_source6_knit.png';
import fringe_hero_s1 from '/img/instruments/videomancer/fringe/fringe_hero_s1.png';
import fringe_hero_s2 from '/img/instruments/videomancer/fringe/fringe_hero_s2.png';
import fringe_hero_s3 from '/img/instruments/videomancer/fringe/fringe_hero_s3.png';
import fringe_hero_s4 from '/img/instruments/videomancer/fringe/fringe_hero_s4.png';
import fringe_hero_s5 from '/img/instruments/videomancer/fringe/fringe_hero_s5.png';
import fringe_hero_s6 from '/img/instruments/videomancer/fringe/fringe_hero_s6.png';
import fringe_ex1_s1 from '/img/instruments/videomancer/fringe/fringe_ex1_s1.png';
import fringe_ex1_s2 from '/img/instruments/videomancer/fringe/fringe_ex1_s2.png';
import fringe_ex1_s3 from '/img/instruments/videomancer/fringe/fringe_ex1_s3.png';
import fringe_ex1_s4 from '/img/instruments/videomancer/fringe/fringe_ex1_s4.png';
import fringe_ex1_s5 from '/img/instruments/videomancer/fringe/fringe_ex1_s5.png';
import fringe_ex1_s6 from '/img/instruments/videomancer/fringe/fringe_ex1_s6.png';
import fringe_ex2_s1 from '/img/instruments/videomancer/fringe/fringe_ex2_s1.png';
import fringe_ex2_s2 from '/img/instruments/videomancer/fringe/fringe_ex2_s2.png';
import fringe_ex2_s3 from '/img/instruments/videomancer/fringe/fringe_ex2_s3.png';
import fringe_ex2_s4 from '/img/instruments/videomancer/fringe/fringe_ex2_s4.png';
import fringe_ex2_s5 from '/img/instruments/videomancer/fringe/fringe_ex2_s5.png';
import fringe_ex2_s6 from '/img/instruments/videomancer/fringe/fringe_ex2_s6.png';
import fringe_ex3_s1 from '/img/instruments/videomancer/fringe/fringe_ex3_s1.png';
import fringe_ex3_s2 from '/img/instruments/videomancer/fringe/fringe_ex3_s2.png';
import fringe_ex3_s3 from '/img/instruments/videomancer/fringe/fringe_ex3_s3.png';
import fringe_ex3_s4 from '/img/instruments/videomancer/fringe/fringe_ex3_s4.png';
import fringe_ex3_s5 from '/img/instruments/videomancer/fringe/fringe_ex3_s5.png';
import fringe_ex3_s6 from '/img/instruments/videomancer/fringe/fringe_ex3_s6.png';

# Fringe

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: fringe_source1_runner, after: fringe_hero_s1 },
    { label: "Dog", before: fringe_source2_dog, after: fringe_hero_s2 },
    { label: "Collage", before: fringe_source3_collage, after: fringe_hero_s3 },
    { label: "Pattern", before: fringe_source4_pattern, after: fringe_hero_s4 },
    { label: "Woman", before: fringe_source5_woman, after: fringe_hero_s5 },
    { label: "Knit", before: fringe_source6_knit, after: fringe_hero_s6 },
  ]}
/>
*Fringe rendering vivid rainbow moire and chroma smear across a colour-bar test pattern, the simulated NTSC composite artifacts blooming false colour from every vertical transition.*

---

## Overview

Before the era of component video and digital interfaces, nearly all consumer video passed through a single wire — the composite cable. Inside that one signal, luminance and chrominance fought for bandwidth, separated only by the mathematical elegance of quadrature modulation and the practical limitations of inexpensive decoding hardware. The result was a family of visual artifacts that defined the look of an entire generation of video: rainbow fringing on sharp vertical edges, dot crawl along horizontal boundaries, chroma smear trailing saturated objects, and cross-colour rainbows where fine luma detail was misinterpreted as colour. These artifacts were not bugs but the inevitable consequence of encoding three channels into one, then pulling them apart with imperfect filters.

Fringe recreates this process pixel by pixel inside the FPGA pipeline. A DDS-based subcarrier oscillator generates a four-phase quadrature carrier that modulates the input chrominance onto the luma channel, producing a simulated composite waveform. The composite is then separated back into Y and C using either a comb filter (two-sample averaging) or a simple notch filter (adjacent-sample averaging), both intentionally coarse enough to leave residual chroma in the luma and residual luma in the chroma. The extracted chroma is demodulated by reversing the quadrature and passed through a variable-bandwidth IIR lowpass to control how much smearing affects the recovered colour channels. Every stage is tunable: modulation depth, subcarrier rate, filter type, notch blend, cross-colour injection, and chroma bandwidth — giving granular control over which composite artifacts dominate the output.

The name *Fringe* refers both to the colour fringing that appears at luminance transitions in composite video and to the broader concept of signal artifacts lurking at the fringe of a transmission system's capabilities.

---

## Background

### NTSC Composite Video Encoding

The NTSC colour television system, adopted in 1953, solved the problem of backward compatibility by embedding chrominance information within the existing monochrome luminance bandwidth. A colour subcarrier at precisely 3.579545 MHz was quadrature-modulated with the I and Q colour-difference signals and summed with the luminance — the result was a single composite waveform carrying brightness and colour in the same band. Monochrome receivers simply ignored the high-frequency subcarrier as noise, while colour receivers used a reference burst at the start of each line to lock a local oscillator and demodulate the chrominance. The system worked remarkably well, but the shared bandwidth meant that any sharp luminance edge near the subcarrier frequency would appear as false colour, and any saturated colour would interfere with the luminance. Fringe models this fundamental tradeoff by encoding and decoding a simulated composite within the FPGA, using intentionally imperfect filters to expose the artifacts that real NTSC hardware struggled to suppress.

### Colour Subcarrier and Quadrature Modulation

Quadrature modulation encodes two signals on a single carrier by multiplying one signal by the carrier's cosine and the other by its sine — the 90° phase offset means the two signals occupy the same frequency band but remain mathematically separable. In NTSC, the I and Q axes are rotated 33° from U and V, but the underlying technique is the same four-phase pattern: the carrier cycles through +V, +U, −V, −U (or equivalently cos, sin, −cos, −sin) at the subcarrier frequency. Demodulation reverses the process — multiplying the composite by the same phase sequence and lowpass-filtering the result recovers the chroma axes independently. Fringe implements this as a DDS-driven phase accumulator whose top two bits select one of four quadrature phases. The subcarrier rate knob controls the DDS increment, determining how many pixels span one complete cycle and thus how fine or coarse the artifact pattern appears.

### Artifact Colour: From CGA to NES

Some of the most iconic visuals in computing history owe their colour to composite artifacts. The IBM CGA adapter output a monochrome NTSC-compatible signal whose pixel clock happened to land at half the colour subcarrier frequency — meaning adjacent pixels produced a consistent chroma pattern when decoded by a television. Programmers exploited this: by arranging black and white pixels in specific patterns, they could produce sixteen colours on a monitor that technically received only two. The Nintendo Entertainment System used a similar trick in the opposite direction — its PPU generated composite directly, and the characteristic rainbow banding on vertical transitions became a defining element of 8-bit aesthetics. Fringe allows artists to reproduce these effects deliberately by setting the source to monochrome (stripping real chroma) and adjusting the subcarrier rate and artifact depth until false colour emerges from luminance detail alone.

### The Dot Crawl Phenomenon

Dot crawl is the most recognisable artifact of composite video — a shimmering pattern of coloured dots that slowly marches along the boundary between differently coloured regions. It occurs because the colour subcarrier frequency is not an exact multiple of the line rate, causing the subcarrier phase to shift slightly from line to line and frame to frame. The human eye integrates the crawling pattern into a distracting sparkle at colour boundaries. In Fringe, the dot crawl control shifts the DDS accumulator's initial phase on each vertical sync pulse, changing the alignment of the subcarrier pattern relative to the image and simulating the frame-to-frame phase progression. At different dot crawl settings, the pattern locks to different horizontal positions, producing the characteristic crawling appearance when recorded as a video sequence.

### Comb Filtering vs Notch Filtering

The fundamental challenge of composite decoding is separating luminance from chrominance when they occupy the same frequency band. The simplest approach — a notch filter that averages two adjacent samples — attenuates the subcarrier but also removes high-frequency luminance detail, producing a softer Y channel. A comb filter improves on this by averaging samples separated by one subcarrier cycle (two pixels apart), exploiting the fact that the subcarrier inverts phase every half cycle: the average cancels the chroma while preserving luma detail. However, the comb filter only works perfectly when the signal does not change vertically — on horizontal edges, the two-line-apart assumption breaks down and produces hanging dots. Fringe implements both filters as selectable modes: the comb uses a 3-tap structure (comp_r + comp_d2) / 2 for Y and (2 × comp_d1 − comp_r − comp_d2) / 2 for C, while the notch uses a simpler 2-tap (comp_r + comp_d1) / 2 for Y and (comp_d1 − comp_r) / 2 for C. The luma notch blend then controls how much of the filtered Y replaces the original.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├─ DDS Subcarrier Oscillator                  (per pixel)
│   ├─ Accumulator += Subcarrier rate
│   ├─ Reset to 0 on hsync (each line)
│   ├─ Dot crawl offset on vsync (per frame)
│   ├─ Phase = accumulator[9:8]  (4 quadrants)
│   └─ PAL mode: invert V axis on odd lines
│
├─ 1a. Input + Edge Boost + Quad Modulation    (1 clock)
│   ├─ Edge boost: Y + (Y − prev_Y), clamp [0,1023]
│   ├─ Mono source: zero U/V offsets
│   └─ Quadrature: phase 0→+V, 1→+U, 2→−V, 3→−U
│
├─ 1b. Shift-Add Composite Encode             (1 clock)
│   ├─ Approximate (chroma_mod × Artifact / 1024)
│   │   via bit-test of Artifact[9], [8], [7]
│   ├─ composite = Y + scaled_chroma, clamp [0,1023]
│   └─ Delay line: comp_r → comp_d1 → comp_d2
│
├─ 2a. Y Estimation + C Extraction             (1 clock)
│   ├─ Comb ON:  Y_est = (comp_r + comp_d2) / 2
│   │            C_raw = (2×comp_d1 − comp_r − comp_d2) / 2
│   └─ Comb OFF: Y_est = (comp_r + comp_d1) / 2
│                C_raw = (comp_d1 − comp_r) / 2
│
├─ 2b. Luma Notch Blend                        (1 clock)
│   ├─ Level 0: Y = original (no filtering)
│   ├─ Level 1: Y = (original + Y_est) / 2
│   ├─ Level 2: Y = (3×Y_est + original) / 4
│   └─ Level 3: Y = Y_est (fully filtered)
│
├─ 3a. Cross-Colour Boost + Demodulation        (1 clock)
│   ├─ Cross-colour: C × 1.0 / 1.25 / 1.5 / 2.0
│   └─ Reverse quadrature: sign from phase[1], axis from phase[0]
│
├─ 3b. IIR Error Computation                    (1 clock)
│   └─ error = demod_value − filter_state
│
├─ 3c. IIR Step + Filter Update                 (1 clock)
│   ├─ Bandwidth: step = error >> 0 / 1 / 2 / 3
│   ├─ filter_new = filter_state + step
│   └─ Update filt_U or filt_V per axis
│
├─ 4. Output Registration                       (1 clock)
│   └─ Y = notch-blended, U = filt_U + 512, V = filt_V + 512
│
├─ 5–8. Interpolator Mix (×3 channels)          (4 clocks)
│   └─ mix = lerp(dry_input, wet_output, mix_amount)
│
├─ Sync/Data Delay Pipeline                     (12-clock shift register)
│
└─ Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → delayed dry Y/U/V + aligned sync
```

The DDS subcarrier oscillator is the heartbeat of the artifact simulation. Its 10-bit accumulator advances by the Subcarrier rate on every active pixel, cycling the quadrature phase through the four-phase pattern that encodes chroma onto the composite waveform. The two most significant bits of the accumulator select the quadrant — +V, +U, −V, −U — creating a discrete approximation of continuous quadrature modulation. Higher subcarrier rates cycle the phase faster, producing finer fringing patterns; lower rates produce coarser, more exaggerated colour banding. Because the accumulator resets to zero on each horizontal sync, the subcarrier pattern starts fresh on every line, ensuring horizontal consistency within each scanline.

The composite encoding uses a three-bit shift-add approximation rather than a hardware multiplier, testing bits 9, 8, and 7 of the Artifact register to accumulate chroma_mod/2, chroma_mod/4, and chroma_mod/8 respectively. This covers approximately 87.5% of the full modulation range and avoids the latency and resource cost of a true multiplier. The resulting composite waveform captures the essence of NTSC encoding — luminance plus modulated chrominance — while the subsequent Y/C separation and chroma demodulation stages model the decoding imperfections that make composite video visually distinctive. The IIR filters reset at each line boundary alongside the DDS, preventing inter-line state leakage and ensuring each scanline is decoded independently.

---

## Parameter Reference

<img src={fringe_control_panel} alt="Videomancer front panel with Fringe loaded"/>
*Videomancer's front panel with Fringe active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Artifact
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the modulation depth of the simulated composite encoding — how much quadrature-modulated chroma is mixed into the luminance channel. At zero, no chroma modulation is added and the composite signal is pure luma, producing a clean output with no artifacts regardless of other settings. As Artifact increases, the chroma component grows stronger in the composite, producing progressively more visible fringing, rainbow moire, and cross-colour effects in the decoded output. At maximum, the chroma modulation is nearly full-scale, and the imperfect Y/C separation creates dramatic colour artifacts on every luminance transition. This is the master intensity control for the composite simulation — set it low for a subtle vintage wash, or push it high for aggressive CGA-era artifact colour.

---

#### Knob 2 — Subcarrier
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the DDS increment that determines the subcarrier oscillator frequency — the spatial rate at which the quadrature phase cycles across each scanline. Low values produce wide phase regions where the chroma pattern has large spatial periods — the resulting artifacts appear as broad colour bands. High values compress the phase cycling into very few pixels per cycle, creating fine fringing patterns that approach the look of real NTSC subcarrier interference. The default mid-range setting produces approximately four pixels per full quadrature cycle, matching the relationship between pixel clock and subcarrier frequency in early composite systems. The subcarrier rate also affects the alignment between encoding and decoding phases across the pipeline, which changes the character of the cross-colour leakage.

---

#### Knob 3 — Chroma BW
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Governs the bandwidth of the IIR lowpass filter applied to each demodulated chroma axis. The filter controls how quickly the recovered U and V signals respond to incoming data. At minimum (widest bandwidth), the IIR step equals the full error — the filter tracks perfectly, producing sharp chroma transitions with minimal smearing. As the bandwidth narrows through four discrete levels, the step size halves at each stage (error/2, error/4, error/8), causing the filter to lag behind rapid chroma changes and producing the distinctive chroma smear that trails saturated objects in composite video. Maximum bandwidth narrowing creates heavy colour bleeding where each sharp chroma transition produces a long exponential tail of false colour.

---

#### Knob 4 — Dot Crawl
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 2 |

Selects one of eight dot crawl phase offsets applied to the DDS accumulator on each vertical sync pulse. The three-bit value (extracted from register bits [9:7]) is left-shifted by seven positions and loaded into the subcarrier accumulator at the start of each frame. Different settings place the subcarrier pattern at different horizontal starting positions, simulating the frame-to-frame phase shift that causes dot crawl in real composite systems. When the dot crawl value changes between frames — either through manual adjustment or parameter modulation — the coloured fringe pattern shifts horizontally, creating the characteristic crawling-dot animation along colour boundaries. At a static setting, the dot crawl determines a fixed phase alignment that affects which edges show the strongest artifacts.

---

#### Knob 5 — Luma Notch
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls how much of the filtered luma estimate replaces the original input luma, blending between unfiltered Y and the Y extracted by the comb or notch filter. At level zero (minimum), the output uses the original Y with no notch filtering — the full luma bandwidth is preserved, but any chroma residue in the luma path remains visible. At level one, the output is a 50/50 average of original and estimated Y. At level two, the estimated Y dominates at 75%. At maximum (level three), the output uses the fully filtered Y estimate, removing high-frequency chroma interference from the luma but also softening genuine luma detail. This control trades luma sharpness against chroma rejection — the same compromise faced by every real composite decoder.

---

#### Knob 6 — Cross Color
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Amplifies the extracted chroma signal before demodulation, injecting exaggerated false colour into the output. At minimum (×1), the extracted C passes through at natural amplitude. At the second level (×1.25), a quarter of the C signal is added back. At level three (×1.5), half is added. At maximum (×2), the chroma is doubled — every residual luma component in the C extraction path appears as vivid false colour in the output. This control is the key to producing dramatic rainbow moire and cross-colour effects: high Cross Color with a monochrome source creates artifact colour from pure luminance detail, recalling the CGA and NES colour tricks that defined early computer graphics.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Standard** | NTSC | PAL |
| **8 — Comb Filter** | Off | On |
| **9 — Mono Source** | Off | On |
| **10 — Edge Boost** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches split into two functional groups. Standard and Comb Filter control the core composite simulation algorithm — NTSC vs PAL carrier behaviour and the Y/C separation filter topology. Mono Source and Edge Boost are input pre-processing controls that modify the video before it enters the composite encoder. Bypass disables all processing. The most dramatic configurations combine Mono Source (stripping real colour) with high Cross Color and Artifact — producing pure artifact colour from luminance detail — or pair Comb Filter with different Luma Notch levels to compare the two separation strategies. All five toggles are fully independent and can be combined freely.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the unprocessed input and the composite-artefacted output via three parallel interpolator units (one per YUV channel). At 0%, the output is pure dry input — no artifacts visible. At 100%, the output is fully processed through the composite simulation. Intermediate positions blend proportionally, allowing the artifact effect to be dialled in at any strength. The interpolator operates in the unsigned 10-bit domain with 4-clock pipelined multiply-accumulate, producing glitch-free crossfading at any position.

---

## Guided Exercises

These three exercises progressively explore the composite artifact space — from basic fringing through dot crawl mechanics to the full CGA-era artifact colour effect. Each builds on the previous, so work through them in order for the clearest understanding of how the simulation parameters interact.

### Exercise 1: Composite Fringing on Colour Bars

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: fringe_source1_runner, after: fringe_ex1_s1 },
    { label: "Dog", before: fringe_source2_dog, after: fringe_ex1_s2 },
    { label: "Collage", before: fringe_source3_collage, after: fringe_ex1_s3 },
    { label: "Pattern", before: fringe_source4_pattern, after: fringe_ex1_s4 },
    { label: "Woman", before: fringe_source5_woman, after: fringe_ex1_s5 },
    { label: "Knit", before: fringe_source6_knit, after: fringe_ex1_s6 },
  ]}
/>
*Composite Fringing on Colour Bars — simulated result across source images.*
**Source**: Colour bar test pattern or any source with sharp vertical colour transitions — SMPTE bars, vertical stripes, or high-contrast graphics.

**Objective**: Observe how the composite encode/decode cycle produces colour fringing at luminance transitions and understand the relationship between Artifact depth and Subcarrier rate.

1. **Initialise**: Set all controls to default (Artifact 50%, Subcarrier 50%, Chroma BW 50%, Dot Crawl 2, Luma Notch 50%, Cross Color 25%, Standard NTSC, Comb Off, Mono Off, Edge Boost Off, Bypass Off, Mix 100%).
2. **Observe fringing**: Look at sharp colour transitions — vertical edges should show rainbow fringing where the composite encode leaves residual chroma in the luma separation.
3. **Increase Artifact**: Push Artifact to ~80%. The fringing intensifies — more chroma modulation means more residual colour in the decoded output.
4. **Vary Subcarrier**: Sweep Subcarrier from ~20% to ~80%. Lower rates produce wide, coarse colour bands; higher rates produce fine, tight fringing patterns.
5. **Add Cross Color**: Increase Cross Color to ~60%. The extracted chroma signal is amplified, making every residual artifact more vivid.
6. **Compare Comb vs Notch**: Toggle Comb Filter on. Observe how the fringing pattern changes — the comb filter should produce cleaner luma but different artifact textures.
7. **Disengage**: Pull Mix to ~50% to see the artefacted output blended against the clean input, highlighting exactly where the artifacts appear.

**Key concepts**: Composite encoding adds chroma to luma, imperfect separation leaves residual colour as fringing, higher artifact depth increases modulation energy, subcarrier rate controls the spatial frequency of the pattern, cross-colour amplifies false chroma.

---

### Exercise 2: Dot Crawl and Comb Filter Exploration

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: fringe_source1_runner, after: fringe_ex2_s1 },
    { label: "Dog", before: fringe_source2_dog, after: fringe_ex2_s2 },
    { label: "Collage", before: fringe_source3_collage, after: fringe_ex2_s3 },
    { label: "Pattern", before: fringe_source4_pattern, after: fringe_ex2_s4 },
    { label: "Woman", before: fringe_source5_woman, after: fringe_ex2_s5 },
    { label: "Knit", before: fringe_source6_knit, after: fringe_ex2_s6 },
  ]}
/>
*Dot Crawl and Comb Filter Exploration — simulated result across source images.*
**Source**: Graphic with large areas of flat colour separated by clean horizontal or diagonal edges — cartoon or anime footage works well, as does a simple two-colour split-screen.

**Objective**: Understand how dot crawl shifts the fringing pattern and how the comb filter changes the artifact signature on different edge orientations.

1. **From Exercise 1 settings**: Artifact ~60%, Subcarrier ~50%, Mix 100%.
2. **Enable comb filter**: Toggle Comb Filter on. Observe that vertical edges show less fringing (the comb cancels subcarrier well), but horizontal colour boundaries may show hanging-dot artifacts.
3. **Sweep Dot Crawl**: Slowly step through Dot Crawl values 0–7. Watch the fringing pattern shift horizontally at each step — the subcarrier phase offset changes where the colour artifacts land relative to the image content.
4. **Disable comb filter**: Toggle Comb Filter off. Sweep Dot Crawl again — the notch filter's artifact pattern should shift differently, since it uses adjacent rather than 2-apart samples.
5. **Adjust Luma Notch**: With comb off, sweep Luma Notch from 0% to 100%. At 0%, the original luma is used (maximum sharpness, maximum chroma leakage into luma). At 100%, the notch-filtered luma removes most subcarrier residue but softens the image.
6. **Switch to PAL**: Toggle Standard to PAL. Observe how the line-alternating V inversion changes the vertical structure of the fringing — PAL tends to produce a line-paired banding rather than smooth vertical colour bands.

**Key concepts**: Dot crawl shifts subcarrier phase per frame producing crawling-dot animation, comb filter preserves luma detail but creates hanging dots, notch filter softens luma but distributes artifacts more evenly, luma notch blend trades sharpness against chroma rejection, PAL creates line-paired artifact structure.

---

### Exercise 3: CGA Artifact Colour Laboratory

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: fringe_source1_runner, after: fringe_ex3_s1 },
    { label: "Dog", before: fringe_source2_dog, after: fringe_ex3_s2 },
    { label: "Collage", before: fringe_source3_collage, after: fringe_ex3_s3 },
    { label: "Pattern", before: fringe_source4_pattern, after: fringe_ex3_s4 },
    { label: "Woman", before: fringe_source5_woman, after: fringe_ex3_s5 },
    { label: "Knit", before: fringe_source6_knit, after: fringe_ex3_s6 },
  ]}
/>
*CGA Artifact Colour Laboratory — simulated result across source images.*
**Source**: High-contrast monochrome source — black and white text, geometric line patterns, dithered pixel art, or checkerboard test pattern.

**Objective**: Reproduce the CGA/NES artifact colour effect where false colour emerges from pure luminance detail through the composite encode/decode process.

1. **Enable Mono Source**: Toggle Mono Source on. All incoming colour is stripped — the composite encodes only luminance.
2. **Set high Artifact**: Push Artifact to ~90%. Maximum modulation depth creates the strongest composite signal.
3. **Increase Cross Color**: Set Cross Color to ~80% (×2 amplification). The decoder will aggressively interpret luma transitions as chroma.
4. **Adjust Subcarrier**: Sweep Subcarrier slowly. At certain rates, the pixel grid of the source will align with the subcarrier cycle to produce stable, repeatable false colours — just like CGA on a composite monitor.
5. **Enable Edge Boost**: Toggle Edge Boost on. The sharpened luma edges produce stronger high-frequency content, resulting in more vivid artifact colours.
6. **Narrow Chroma BW**: Push Chroma BW to ~80% (narrow filter). The IIR responds slowly, causing each false colour burst to smear horizontally — a characteristic look of cheap composite decoders.
7. **Try PAL mode**: Toggle Standard to PAL. The line-alternating V inversion creates a different false colour palette from the same source pattern — different colours emerge on adjacent lines.
8. **Reduce Artifact for subtlety**: Pull Artifact back to ~40%. The false colours become pastel and translucent — a nostalgic wash rather than aggressive banding.

**Key concepts**: Mono source strips real colour forcing all output chroma to be artifacts, subcarrier rate alignment with source pixel grid creates stable false-colour palettes, edge boost amplifies luma transitions for stronger false chroma, narrow bandwidth smears artifact colours horizontally, PAL produces different false colour patterns than NTSC.

---


## Tips

- **Start with Mono Source for artifact colour**: The most dramatic effect is CGA-style false colour from a monochrome source. Toggle Mono Source on, push Artifact and Cross Color high, and sweep Subcarrier to find the sweet spot where the pixel grid locks to the subcarrier.
- **Subcarrier rate is the key frequency control**: The Subcarrier knob determines the spatial frequency of all fringing patterns. Low rates produce broad colour washes; high rates produce fine moire. At certain rates, the subcarrier aligns with the source pixel grid to create stable false-colour patterns.
- **Narrow Chroma BW for vintage smear**: Push Chroma BW above 75% for the characteristic horizontal colour bleeding of cheap composite decoders. Combined with high Artifact, this produces the heavy chroma smear seen on worn VHS tapes and budget televisions.
- **Cross Color amplifies everything**: Even modest Cross Color settings (×1.25) noticeably boost artifact visibility. At ×2, every luminance transition becomes a vivid colour event. Use with restraint for subtle vintage effects, or push maximum for aggressive false colour.
- **Comb filter for cleaner luma**: When you want composite artifacts on the chroma side but relatively sharp luma, enable the Comb Filter. It preserves luma detail better than the notch filter at the cost of occasional hanging-dot artifacts on horizontal colour boundaries.
- **Edge Boost before Mono Source**: Enable Edge Boost before Mono Source to maximise the high-frequency content entering the composite encoder. The sharpened luma edges produce stronger false-colour patterns than a standard monochrome input.
- **PAL for alternate colour palettes**: Switch to PAL mode to get a different false-colour palette from the same source. The line-alternating V inversion creates complementary colours on adjacent lines, producing a distinct visual texture from NTSC mode.
- **Mix at 50% for compositing**: Use the Mix fader at ~50% to overlay the composite artifacts onto the clean source. This produces a translucent vintage wash that preserves the original image while adding composite character.

---

## Glossary

| Term | Definition |
|------|------------|
| **Artifact colour** | False colour produced when a composite decoder misinterprets high-frequency luminance detail as chrominance, creating hues that do not exist in the original source signal. |
| **CGA (Colour Graphics Adapter)** | IBM's first colour display adapter (1981), whose composite output at half the NTSC subcarrier frequency enabled programmers to exploit artifact colour for an extended palette. |
| **Chroma smear** | Horizontal spreading of colour caused by a narrow-bandwidth lowpass filter in the chroma demodulation chain, producing trailing colour tails behind saturated objects. |
| **Comb filter** | A Y/C separation technique that averages samples separated by one subcarrier cycle, exploiting phase inversion to cancel chroma while preserving luma detail. |
| **Composite video** | A video signal format that combines luminance and modulated chrominance into a single waveform, requiring the receiver to separate them for display. |
| **Cross-colour** | False colour appearing in areas of fine luminance detail when the Y/C separation filter fails to fully extract chroma from the high-frequency luma component. |
| **DDS (Direct Digital Synthesis)** | A frequency generation technique using a fixed-width accumulator incremented by a tuning word, producing seamless cyclical phase progression. |
| **Dot crawl** | A visible pattern of shimmering coloured dots along colour boundaries in composite video, caused by frame-to-frame subcarrier phase shifts. |
| **IIR (Infinite Impulse Response)** | A filter topology where the output depends on both current input and previous filter state, producing exponential convergence with minimal hardware. |
| **Interpolator** | A pipelined hardware crossfade unit that blends two signals by a configurable ratio, used for wet/dry mixing. |
| **Notch filter** | A Y/C separation technique that averages adjacent samples to attenuate the subcarrier, simpler than a comb filter but with greater luma softening. |
| **NTSC (National Television System Committee)** | The analogue colour television standard used in North America and Japan, characterised by a 3.58 MHz colour subcarrier using I/Q quadrature modulation. |
| **PAL (Phase Alternating Line)** | The analogue colour television standard used in Europe and Australasia, characterised by V-axis phase inversion on alternate lines to reduce colour phase errors. |
| **Quadrature modulation** | Encoding two signals on a single carrier by multiplying one by the carrier's cosine and the other by its sine, exploiting the 90° phase orthogonality for independent recovery. |
| **Rainbow moire** | A characteristic diagonal rainbow pattern in composite video caused by interaction between fine horizontal luma detail and the colour subcarrier frequency. |

---
