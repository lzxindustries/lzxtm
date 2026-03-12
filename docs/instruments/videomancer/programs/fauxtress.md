---
draft: false
sidebar_position: 108
slug: /instruments/videomancer/fauxtress
title: "Fauxtress"
image: /img/instruments/videomancer/fauxtress/fauxtress_hero.png
description: "Fauxtress is a faithful reimplementation of the LZX Industries Fortress EuroRack module as a Videomancer FPGA program."
---

import fauxtress_hero from '/img/instruments/videomancer/fauxtress/fauxtress_hero.png';
import fauxtress_animation from '/img/instruments/videomancer/fauxtress/fauxtress_animation.gif';
import fauxtress_control_panel from '/img/instruments/videomancer/fauxtress/fauxtress_control_panel.png';
import fauxtress_exercise1_result from '/img/instruments/videomancer/fauxtress/fauxtress_exercise1_result.gif';
import fauxtress_exercise2_result from '/img/instruments/videomancer/fauxtress/fauxtress_exercise2_result.gif';
import fauxtress_exercise3_result from '/img/instruments/videomancer/fauxtress/fauxtress_exercise3_result.gif';

# Fauxtress

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={fauxtress_hero} alt="Fauxtress hero image"/>
*Fauxtress generating a Neon-palette cellular automata pattern, its diagonal interference bands revealing the cross-modulation between horizontal and animation phase accumulators.*
<img src={fauxtress_animation} alt="Fauxtress animated output"/>
*Fauxtress output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Fauxtress is a faithful reimplementation of the LZX Industries Fortress EuroRack module as a Videomancer FPGA program. Fortress was a standalone geometric pattern synthesizer — a "video oscillator on steroids" — that combined phase-accumulator waveforms, multiple pattern generation algorithms, an arithmetic logic unit (ALU), and a bank of curated color palettes to produce an enormous range of geometric, textural, and noise-based video imagery from scratch. Its signature was the cross-modulation between horizontal and animation accumulators, which produced the sweeping diagonal moire patterns instantly recognizable to LZX modular video users.

Fauxtress reproduces all four of Fortress's pattern generation programs: direct waveform combining, a 16-stage shift register delay, 32-cell 1D cellular automata running classic Wolfram rules, and a configurable linear feedback shift register (LFSR) noise generator. Each program feeds its output through one of eight ALU operations — Add, Subtract, AND, OR, XOR, NAND, NOR, XNOR — and the 3-bit result indexes into one of eight color palettes ported directly from the original hardware. The result is a combinatorial space of thousands of distinct visual textures, from razor-sharp geometric grids to evolving organic cellular structures to pseudo-random noise fields, all rendered in the original Fortress color language.

The name "Fauxtress" — a portmanteau of "faux" and "Fortress" — acknowledges that while the implementation is new (VHDL on iCE40 rather than the original discrete logic), the design intent, palette data, CA rules, and aesthetic fingerprint are drawn directly from the original module.

---

## Quick Start

1. **Start with Direct + XOR for instant patterns**: Program 00 with the XOR operation produces the widest variety of classic Fortress geometric grids. It's the fastest path to a recognizable signal from which to explore other program modes.
2. **Anim Rate is diagonal tilt**: Think of the animation rate as a "tilt" control for the pattern. Zero produces purely orthogonal (horizontal/vertical) structures. Small values tilt the pattern slightly diagonal. Large values produce rapidly sweeping moire interference.
3. **Triangle smooths, Ramp sharpens**: Triangle waveforms produce mirrored, smooth patterns with no wrap-around discontinuity. Ramp waveforms produce sawtooth patterns with a sharp edge at the wrap boundary. Mix and match for asymmetric textures.

---

## Background

### The LZX Fortress Module

Fortress was released by LZX Industries as part of the Visionary series of EuroRack video synthesis modules. It occupied a unique niche in the modular video ecosystem: a self-contained pattern generator that could produce complex geometric imagery without any external video input. Unlike oscillator modules that generated simple waveforms, Fortress included an onboard ALU, multiple pattern algorithms, and a curated palette system — making it a complete visual synthesizer in a single module. Its eight color palettes (NTSC, Torchlight, Neon, CMYK, Pastel, Quadrature, Earth, Rhodamine) were hand-designed to produce aesthetically coherent results across all possible pattern combinations, and became a signature element of the LZX visual language. Fauxtress preserves these palettes exactly, converting the original 9-bit RGB values to BT.601 YUV at elaboration time.

### Phase Accumulator Waveforms

A phase accumulator is the simplest and most resource-efficient technique for generating periodic waveforms in digital hardware. A register of width N increments by a fixed "rate" value on each clock tick. Because the register wraps around at $2^N$, the most significant bits trace a sawtooth (ramp) waveform whose frequency is proportional to the rate value. The ramp can be folded into a triangle by using the MSB as a direction bit: when the MSB is 0, the remaining bits increase; when the MSB is 1, the remaining bits are inverted, producing a symmetric rise-and-fall pattern. Fauxtress uses three 20-bit accumulators — horizontal, vertical, and animation — with the horizontal accumulator *preloaded* from the animation accumulator at each horizontal sync pulse. This preload is the source of the diagonal interference patterns: each scanline starts at a progressively shifted phase, so what would be a purely horizontal pattern rotates into diagonal stripes whose angle depends on the animation rate.

### Cellular Automata and Wolfram Rules

A 1D elementary cellular automaton consists of a row of binary cells, each of which updates its state based on its own value and the values of its two immediate neighbors. The three-cell neighborhood yields $2^3 = 8$ possible configurations, and the rule assigns a new value (0 or 1) to each configuration — giving $2^8 = 256$ possible rules, each identified by its Wolfram number (the decimal encoding of the 8-bit output pattern). Fauxtress implements eight rules drawn from the original Fortress hardware: Rule 110 (Turing-complete, produces complex long-range order), Rule 9 (sparse, crystalline), Rule 107 (dense, fabric-like), Rule 133 (complementary to 107), Rule 13 (sparse diagonal), Rule 57 (striped), Rule 30 (chaotic, used by Mathematica for random number generation), and Rule 45 (chaotic with triangular structures). The 32-cell CA array evolves one generation per scanline, with wraparound boundary conditions, producing a spacetime diagram that unfolds vertically down the screen — each row is one generation of the automaton's evolution. The Seed parameter determines both the initial cell position and the rule selection.

### LFSR Noise Generation

A linear feedback shift register generates pseudo-random binary sequences by XOR-ing selected bit positions (the "polynomial taps") and feeding the result back into the register's input. Different polynomials produce different sequence lengths and spatial textures — maximal-length polynomials cycle through $2^N - 1$ states before repeating, while non-maximal polynomials produce shorter, more structured sequences with visible periodicity. In Fauxtress, the LFSR polynomial is set by the Seed parameter, giving the user direct control over the texture character of the noise. The LFSR resets on each vertical sync, ensuring frame-locked repeatable patterns rather than free-running chaos — the same polynomial always produces the same spatial noise field.

### ALU Operations in Video Synthesis

In conventional computing, the ALU performs arithmetic and logic on data. In video synthesis, these same operations become spatial composition tools. Adding two periodic waveforms produces a sum pattern whose frequency content is the union of both inputs — creating dense moire grids. Subtracting emphasizes differences and produces complementary patterns. The bitwise operations (AND, OR, XOR, NAND, NOR, XNOR) treat the waveform values as 10-bit integers and combine them bit by bit, producing hard-edged quantized patterns that are distinctly digital in character. XOR in particular is a classic video synthesis operation: it produces patterns that are zero wherever the inputs match and maximal wherever they differ, creating a checkerboard-like interference that highlights the spatial frequency structure of both inputs simultaneously.


---

## Signal Flow

Waveform Shaping → Pattern Programs → ALU → ... → Sync Delay Pipeline → Bypass Mux

```
Phase Accumulators
│
├── H Accumulator (20-bit)
│   ├─ Reset to Animation Accumulator value on hsync
│   └─ Increment by H Rate per pixel (during avid)
│
├── V Accumulator (20-bit)
│   ├─ Reset to 0 on vsync
│   └─ Increment by V Rate per scanline (on hsync)
│
├── Animation Accumulator (20-bit)
│   └─ Free-running: increment by Anim Rate per pixel clock
│
├── Waveform Shaping ──────────────────────────────────────────
│   ├─ H Ramp = H Accum[19:10]
│   ├─ H Tri  = fold(H Accum[18:9]) via MSB direction
│   ├─ H Wave = (H Shape) ? H Tri : H Ramp
│   ├─ V Ramp = V Accum[19:10]
│   ├─ V Tri  = fold(V Accum[18:9]) via MSB direction
│   └─ V Wave = (V Shape) ? V Tri : V Ramp
│
├── Pattern Programs ──────────────────────────────────────────
│   ├─ Program 0 (Direct):    ALU_A = H Wave,     ALU_B = V Wave
│   ├─ Program 1 (Shift Reg): ALU_A = Shift[tap], ALU_B = V Wave
│   │   └─ 16-stage × 10-bit delay line fed by H Wave
│   ├─ Program 2 (Cell Auto): ALU_A = CA[cell],   ALU_B = H Wave
│   │   └─ 32-cell 1D CA, evolves per scanline, 8 Wolfram rules
│   └─ Program 3 (LFSR):      ALU_A = LFSR[9:0],  ALU_B = V Wave
│       └─ 10-bit polynomial-configurable LFSR
│
├── ALU (8 operations) ────────────────────────────────────────
│   ├─ 0: A + B    1: A − B    2: A AND B    3: A OR B
│   ├─ 4: A XOR B  5: A NAND B 6: A NOR B    7: A XNOR B
│   └─ Pipeline register (1 clock latency)
│
├── Palette Lookup ────────────────────────────────────────────
│   ├─ Index = Palette Select[2:0] & ALU Result[9:7]
│   ├─ → Y = PAL_Y[index], U = PAL_U[index], V = PAL_V[index]
│   └─ 8 palettes × 8 colors = 64 entries (BT.601 converted)
│
├── Mix Crossfade (interpolator × 3 channels) ─────────────────
│   └─ lerp(Input Video, Generated Pattern, Mix)  (4 clocks)
│
├── Sync Delay Pipeline (4 stages) ────────────────────────────
│   └─ hsync, vsync, field, avid delayed to match interpolator
│
└── Bypass Mux ────────────────────────────────────────────────
    └─ Bypass On → pass input directly; Off → mixed output
```

The cross-modulation between the animation and horizontal accumulators is the most distinctive feature of the signal flow. Because the horizontal accumulator is preloaded from the animation accumulator at each hsync, the starting phase of each scanline shifts progressively — producing diagonal patterns whose angle is determined by the ratio of the animation rate to the horizontal rate. When the animation rate is zero, the horizontal pattern is purely horizontal (identical on every line). As the animation rate increases, the phase offset between successive lines grows, rotating the pattern toward the diagonal. This mechanism is computationally free — it uses no additional logic, only the accumulator preload — yet it produces the rich moire interference patterns that defined the original Fortress aesthetic. The ALU pipeline register between the ALU output and the palette lookup breaks what would otherwise be a long combinational path through waveform generation, program selection, ALU operation, and palette ROM lookup.

---

## Parameter Reference

<img src={fauxtress_control_panel} alt="Videomancer front panel with Fauxtress loaded"/>
*Videomancer's front panel with Fauxtress active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — H Rate
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 256 |

At zero, the horizontal accumulator does not advance — every pixel on each scanline sees the same phase value, producing uniform horizontal bands (or a solid field if V Rate is also zero). As H Rate increases, vertical stripes of increasing spatial frequency appear. The value directly sets the 10-bit increment added to the 20-bit accumulator per pixel, so the spatial frequency scales linearly with the knob position. At maximum, the pattern cycles roughly once per two pixels, producing the highest-frequency spatial grid. The horizontal waveform feeds directly into the Direct and Shift Register programs, and indirectly into the Cellular Automata program as the spatial readout index. Internally, controls the frequency of the horizontal phase accumulator.

---

#### Knob 2 — V Rate
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 256 |

At zero, the vertical accumulator remains at its reset value (zero) on every scanline, producing uniform vertical bars. As V Rate increases, horizontal stripes appear and become more closely spaced. Because the vertical accumulator increments once per scanline (at hsync) rather than once per pixel, a given V Rate value produces a coarser spatial frequency than the same H Rate value — there are only 1080 lines versus 1920 pixels. The vertical waveform serves as ALU operand B in the Direct, Shift Register, and LFSR programs. Internally, controls the frequency of the vertical phase accumulator.

---

#### Knob 3 — Anim Rate
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

Controls the animation accumulator rate. When set to zero, the animation accumulator remains at zero and the horizontal accumulator starts each scanline at the same phase — the pattern is static and purely horizontal/vertical. As Anim Rate increases, the animation accumulator advances by this value on every pixel clock (free-running), and the horizontal accumulator is preloaded from it at each hsync. This creates a per-scanline phase shift that produces diagonal interference patterns and sweeping moire effects. Higher values produce faster diagonal drift and more complex cross-modulation. The animation accumulator never resets, so the pattern continuously evolves over time.

---

#### Knob 4 — Operation
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Selects one of eight ALU operations via the top 3 bits of the register value. The operation determines how the two waveform operands are combined: Add (0) creates sum patterns with rich moire, Subtract (1) emphasizes differences, AND (2) produces sparse intersection patterns, OR (3) creates dense union patterns, XOR (4) generates complementary checkerboard interference, NAND (5) inverts AND's sparse patterns into dense fields, NOR (6) inverts OR's dense patterns into sparse voids, and XNOR (7) produces the complement of XOR. The ALU operates on full 10-bit values with modular arithmetic (wrapping), so sum and difference operations produce wrap-around patterns at the extremes.

---

#### Knob 5 — Palette
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Selects one of eight color palettes via the top 3 bits of the register value. Each palette contains 8 colors, ported directly from the original Fortress hardware's 9-bit RGB values and converted to BT.601 YUV. NTSC (0) uses the classic NTSC color bar palette. Torchlight (1) progresses from dark red through orange to yellow. Neon (2) cycles through saturated rainbow hues. CMYK (3) ranges from black through grays to cyan, magenta, and yellow. Pastel (4) maps to soft, desaturated hues. Quadrature (5) cycles through complementary pairs. Earth (6) uses natural brown and green tones. Rhodamine (7) progresses from black through deep purples and magentas to warm neutrals.

---

#### Knob 6 — Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 512 |

Serves multiple roles depending on the active pattern program. In Direct mode (00), Seed has no effect — the pattern is determined entirely by the waveform rates and ALU operation. In Shift Register mode (01), the top 4 bits of Seed select the delay tap position (0–15), controlling how far back in the horizontal delay line the output is read. In Cellular Automata mode (10), the top 3 bits select the Wolfram rule (0–7 mapping to rules 110, 9, 107, 133, 13, 57, 30, 45) and the bottom 5 bits set the initial seed cell position (0–31). In LFSR mode (11), all 10 bits configure the polynomial tap mask, determining the pseudo-random sequence's character and period.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — H Shape** | Ramp | Triangle |
| **8 — V Shape** | Ramp | Triangle |
| **9 — Shift Reg** | Off | On |
| **10 — CA/LFSR** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 independently select between ramp and triangle waveform shapes for the horizontal and vertical axes, producing four waveform combinations (ramp×ramp, ramp×triangle, triangle×ramp, triangle×triangle) that fundamentally alter the geometry of the pattern. Toggles 9 and 10 form a 2-bit program selector: 00 selects Direct combining, 01 selects the Shift Register, 10 selects the Cellular Automata engine, and 11 selects the LFSR noise generator. Toggle 11 is the standard bypass.

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

Routes the unprocessed input signal directly to the output, bypassing all Fauxtress processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Fauxtress-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises explore the four pattern programs, the ALU's combining operations, and the animation cross-modulation that defines the Fauxtress visual language. Each builds on the previous, progressing from simple geometric grids to evolving cellular structures.

### Exercise 1: Geometric Moire Grid

<img src={fauxtress_exercise1_result} alt="Geometric Moire Grid result"/>
*Geometric Moire Grid — simulated result across source images.*
**What You'll Create**: Generate a classic Fortress-style geometric grid using the Direct program, exploring how waveform shapes, ALU operations, and the animation accumulator produce diagonal interference patterns.

1. **Set Direct mode**: Both Shift Reg and CA/LFSR toggles **Off** (program 00).
2. **Set moderate rates**: H Rate ~256, V Rate ~256 for a medium-density grid.
3. **Select XOR operation**: Set Operation to 4 (XOR). A checkerboard interference pattern appears.
4. **Choose NTSC palette**: Set Palette to 0 for the classic NTSC color bars look.
5. **Compare waveform shapes**: Toggle H Shape and V Shape between Ramp and Triangle. Observe how ramp×ramp produces sharp-edged patterns while triangle×triangle produces smooth, diamond-like structures.
6. **Add animation**: Increase Anim Rate from 0. Watch the pattern rotate into diagonal stripes as the animation accumulator cross-modulates the horizontal phase. Higher values produce faster diagonal sweep.
7. **Try different ALU ops**: Sweep Operation through all 8 values. Each produces a distinctly different spatial composition from the same waveforms.

**Key concepts**: Direct program combines H and V waveforms through the ALU, waveform shape determines edge character, Anim Rate introduces diagonal cross-modulation, ALU operation dramatically changes pattern structure

---

### Exercise 2: Cellular Automata Spacetime

<img src={fauxtress_exercise2_result} alt="Cellular Automata Spacetime result"/>
*Cellular Automata Spacetime — simulated result across source images.*
**What You'll Create**: Activate the cellular automata engine and explore the eight Wolfram rules, observing how rule selection and seed position produce dramatically different spacetime diagrams.

1. **Select CA program**: Toggle Shift Reg **Off**, CA/LFSR **On** (program 10).
2. **Set spatial frequencies**: H Rate ~300 for moderate horizontal resolution of the CA readout, V Rate ~200.
3. **Select Rule 110**: Set Seed to ~0 (bits [9:7] = 000 selects Rule 110). An intricate, non-repeating pattern with long-range structure should appear — Rule 110 is Turing-complete.
4. **Move the seed cell**: Adjust Seed's lower bits (without changing the top 3) to shift the initial cell position within the 32-cell array. The spacetime diagram changes character as the seed interacts differently with the wraparound boundary.
5. **Cycle through rules**: Sweep Seed upward to select different rules. Rule 30 (bits [9:7] = 110) produces chaotic, random-looking patterns. Rule 57 (101) produces regular stripes. Rule 45 (111) creates triangular structures.
6. **Change the ALU operation**: Try AND and OR operations to change how the CA output combines with the horizontal waveform. AND extracts sparse intersections of the cellular structure; OR fills in the gaps.
7. **Apply Neon palette**: Set Palette to 2 for vivid rainbow coloring of the 8 quantized amplitude levels.

**Key concepts**: CA evolves one generation per scanline creating a spacetime diagram, Seed upper bits select rule while lower bits set initial cell, different rules span the spectrum from ordered to chaotic, ALU operation shapes the CA readout

---

### Exercise 3: LFSR Noise Textures

<img src={fauxtress_exercise3_result} alt="LFSR Noise Textures result"/>
*LFSR Noise Textures — simulated result across source images.*
**What You'll Create**: Use the LFSR noise generator to produce a variety of pseudo-random textures, exploring how the polynomial, ALU operation, and palette interact to create structured noise.

1. **Select LFSR program**: Toggle both Shift Reg and CA/LFSR **On** (program 11).
2. **Set baseline rates**: H Rate ~512, V Rate ~256. The noise pattern is combined with the vertical waveform through the ALU.
3. **Start with default polynomial**: Seed at 512. A textured noise field should appear, frame-locked (identical on every frame because the LFSR resets on vsync).
4. **Sweep the polynomial**: Slowly adjust Seed through its range. Different polynomial values produce strikingly different noise textures — some are nearly uniform, others produce visible banding, and maximal-length polynomials yield the most uniform random fields.
5. **Try Subtract (1) and XNOR (7) operations**: These operations interact with the noise in different ways. Subtract creates a structured noise gradient modulated by the V waveform. XNOR produces a complement pattern with visible spatial structure.
6. **Apply Earth palette**: Set Palette to 6 for natural coloring, turning the noise into an organic, terrain-like texture.
7. **Use triangle waveforms**: Toggle both V Shape to Triangle. The smooth V waveform modulated by the noisy LFSR produces cloud-like patterns with less hard-edged structure.
8. **Add animation**: Increase Anim Rate slightly. Because the LFSR is driven by the pixel clock, the animation cross-modulation shifts the noise pattern diagonally, creating animated noise drift.

**Key concepts**: LFSR polynomial controls noise character and period, noise is frame-locked via vsync reset, ALU combines noise with V waveform for structured textures, palette colors transform monochrome noise into rich textural fields

---


## Tips

- **CA rules have distinct personalities**: Rule 110 is complex and non-repeating (Turing-complete). Rule 30 is chaotic. Rule 57 produces clean stripes. Rule 9 is sparse and crystalline. Cycle through rules slowly to find the texture you need.
- **LFSR polynomial shapes the noise**: Not all LFSR polynomials produce long sequences. Some produce very short, highly structured patterns that act more like geometric textures than noise. Sweep Seed slowly in LFSR mode to find the sweet spots.
- **Palette quantization is deliberate**: The 8-color-per-palette quantization is not a limitation — it's the Fortress aesthetic. The hard color boundaries create graphic, poster-like compositions that are distinctly different from smooth gradient video processing.
- **Bitwise operations for digital aesthetics**: AND, OR, XOR and their complements produce hard-edged, aliased patterns that look distinctly "digital." Use these when you want pixel-precise geometric structure rather than smooth analog-style gradients.
- **Mix at 50% for overlay compositing**: When feeding external video through Fauxtress, pull Mix to 50% to blend the generated pattern equally with the input. The palette colors will tint the input video, creating a colored-glass overlay effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **ALU** | Arithmetic Logic Unit; a computational block that performs arithmetic (add, subtract) and bitwise logic (AND, OR, XOR, etc.) operations on two input operands. |
| **Cellular automaton (CA)** | A computational system consisting of a row (1D) or grid (2D) of cells, each updating its state based on the states of its neighbors according to a fixed rule. In Fauxtress, a 32-cell 1D elementary CA evolves one generation per scanline. |
| **Cross-modulation** | The technique of feeding the output of one oscillator into the phase or frequency input of another, producing interference patterns. In Fauxtress, the animation accumulator cross-modulates the horizontal accumulator by preloading its value at hsync. |
| **Elementary CA** | A 1D cellular automaton where each cell has 2 states (0 or 1) and a 3-cell neighborhood (left, center, right). There are exactly 256 possible elementary CA rules, identified by Wolfram numbers. |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function (XOR) of its previous state. Produces pseudo-random binary sequences whose period and character depend on the feedback polynomial. |
| **Moire** | An interference pattern produced when two periodic structures (such as ramp waveforms at different frequencies) overlap, creating visible beat frequencies larger than either original pattern. |
| **Phase accumulator** | A digital counter that increments by a fixed value (the frequency word) on each clock cycle, wrapping at its maximum count. The most significant bits represent the instantaneous phase of a periodic waveform. |
| **Polynomial (LFSR)** | A binary mask that selects which bit positions of the LFSR contribute XOR feedback. Different polynomials produce different pseudo-random sequences with different periods and statistical properties. |
| **Spacetime diagram** | A visualization of a 1D cellular automaton's evolution, where the horizontal axis represents cell position and the vertical axis represents successive generations (time). Each row is one generation of the CA. |
| **Wolfram number** | A decimal integer (0–255) that uniquely identifies an elementary cellular automaton rule by encoding the 8-bit output pattern for all possible 3-cell neighborhoods. |

---
