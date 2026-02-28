---
draft: true
sidebar_position: 249
slug: /instruments/videomancer/stratum
title: "Stratum"
image: /img/instruments/videomancer/stratum/stratum_hero.png
---

import stratum_before_after from '/img/instruments/videomancer/stratum/stratum_before_after.png';
import stratum_control_panel from '/img/instruments/videomancer/stratum/stratum_control_panel.png';
import stratum_exercise1_result from '/img/instruments/videomancer/stratum/stratum_exercise1_result.png';
import stratum_exercise2_result from '/img/instruments/videomancer/stratum/stratum_exercise2_result.png';
import stratum_exercise3_result from '/img/instruments/videomancer/stratum/stratum_exercise3_result.png';
import stratum_hero from '/img/instruments/videomancer/stratum/stratum_hero.png';
import stratum_source1_kodim15 from '/img/instruments/videomancer/stratum/stratum_source1_kodim15.png';
import stratum_source2_kodim01 from '/img/instruments/videomancer/stratum/stratum_source2_kodim01.png';
import stratum_source3_stream_bridge_512 from '/img/instruments/videomancer/stratum/stratum_source3_stream_bridge_512.png';

# Stratum

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={stratum_hero} alt="Stratum hero image"/>
*Stratum applying bit-plane barrel rotation and cross-channel XOR to decompose and recombine video into glitched digital strata.*
<img src={stratum_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Stratum applied.*

---

## Overview

Every pixel of video is a column of thirty binary digits — ten bits each for Y, U, and V, stacked from least significant to most significant. Stratum treats this column not as three separate numbers but as a single thirty-layer geological formation. It can rotate these layers, mirror them, swap them between channels, XOR them against each other, and crush the lowest layers to zero. The result is a family of digital artefacts that range from subtle colour shifts to total signal deconstruction.

The name *Stratum* refers to a horizontal layer of material — in geology, a bed of rock; here, a bit plane of video data. The program's barrel rotator shifts bit planes between significance levels and between colour channels. A plane that carried the most significant bit of luminance can end up as the least significant bit of chrominance, or vice versa. Cross-channel XOR operations fold the channel contents into each other, and a frame counter can be XOR'd into the planes for temporal animation.

At zero rotation and no XOR, the output is identical to the input. Small rotations introduce subtle colour bleeding as lower-significance bits from one channel appear in another. Large rotations and active XOR produce hard-edged digital glitch textures — the kind of artefacts that would occur if a video memory chip had its address lines scrambled.

---

## Background

### Bit-Plane Decomposition

Every 10-bit pixel value can be thought of as ten independent binary images stacked on top of each other. The most significant bit (MSB) carries half the signal's dynamic range — it divides the image into two halves, above and below mid-grey. The next bit divides each half again, and so on down to the least significant bit (LSB), which carries only ±1 count of variation. Decomposing a video frame into these ten planes reveals a hierarchy: the MSB plane looks like a high-contrast silhouette, while the LSB plane looks like noise. Stratum extends this concept to all thirty planes across Y, U, and V, treating the entire pixel as one composite bit vector.

### Barrel Rotation

A barrel rotator is a combinational circuit that shifts all bits in a register by an arbitrary number of positions in a single clock cycle. Unlike a serial shift register (which moves one bit per clock), a barrel rotator uses a network of multiplexers to achieve any shift amount instantly. Stratum implements a two-stage barrel rotator: a coarse stage that rotates by multiples of ten (0, 10, or 20 positions) and a fine stage that rotates by 0–9 positions. Combined, they can place any of the thirty planes in any position.

### XOR in Signal Processing

The exclusive-OR (XOR) operation outputs 1 when its two inputs differ and 0 when they match. In image processing, XORing two signals creates a *difference mask* that highlights changes between them. Stratum applies XOR in two modes: *self* XOR (each bit is XOR'd with its adjacent neighbour, creating an edge-detection-like effect within each channel) and *cross-channel* XOR (Y bits are XOR'd with U bits, U with V, V with Y — folding the three channels into each other). Self XOR tends to produce fine textural detail; cross-channel XOR creates colour artefacts.

### Temporal Animation via Frame Counter

Stratum maintains a 10-bit frame counter that increments on each vertical sync pulse. When the Animate toggle is active, this counter is XOR'd into all thirty bit planes — the same ten counter bits are replicated across Y, U, and V. Because the counter changes every frame, the XOR mask evolves over time, creating cyclic visual animation with a 1024-frame period. The Time XOR control gates this: when below a minimum threshold, the temporal injection is suppressed even with Animate enabled.

### Bit Crush

Zeroing the lowest bit planes of each channel is equivalent to reducing the bit depth — a 10-bit signal with its two LSBs crushed becomes an 8-bit signal. This is digital posterisation: smooth gradients collapse into visible steps. Stratum's Crush Floor parameter selects how many LSBs to zero out (0–9), providing continuous control from full 10-bit resolution down to a single binary bit.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Decompose to 30-bit Plane Vector ────────────────
│   └─ Concatenate: [Y9..Y0 | U9..U0 | V9..V0]
│
├── Stage 2a: Coarse Barrel Rotation (by 10s) ────────────────
│   ├─ Left rotate: shift by 0, 10, or 20 positions
│   └─ Mirror mode: reverse entire 30-bit order
│
├── Stage 2b: Fine Barrel Rotation (by units 0–9) ───────────
│   └─ Left rotate by 0–9 single-bit positions
│       (skipped in Mirror mode)
│
├── Stage 3: XOR Operations + Channel Swap + Temporal Inject ─
│   ├─ Self XOR: bit(i) ⊕ bit(i−1) within each channel
│   │   — or —
│   ├─ Cross-channel XOR: Y⊕U, U⊕V, V⊕Y
│   ├─ Channel swap: swap N MSBs between Y and U
│   └─ Temporal XOR: frame_count bits into all 30 planes
│
├── Stage 4: Bit Crush + Recompose ───────────────────────────
│   ├─ Zero all planes below crush floor bit
│   ├─ Split 30-bit vector back to Y[9:0], U[9:0], V[9:0]
│   └─ Optional invert (bitwise complement)
│
├── Mix (4 clk interpolator) ─────────────────────────────────
│   └─ Wet/dry crossfade: dry × (1 − mix) + wet × mix
│
└── Bypass Mux ───────────────────────────────────────────────
    └─ Select original or processed signal
```

The key to understanding Stratum is that *all operations happen on the concatenated 30-bit vector*, not on individual channels. When you rotate by 5 positions, for example, the 5 MSBs of the Y channel move to the 5 LSBs of the V channel, the entire U channel shifts into the Y position, and so on. This inter-channel leakage is what creates Stratum's distinctive colour artefacts — it is not a colour-space transformation but a raw bit-level permutation. The XOR stage then folds these rearranged planes against each other, and bit crush removes the lowest layers after rearrangement.

---

## Parameter Reference

<img src={stratum_control_panel} alt="Videomancer front panel with Stratum loaded"/>
*Videomancer's front panel with Stratum active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Bit Rotate
| Property | Value |
|----------|-------|
| Range | 0 – 29 |
| Default | 0 |

Controls the total barrel rotation amount across the 30-bit plane vector. The 10-bit register is decomposed into a coarse component (0, 10, or 20 positions) and a fine component (0–9 positions), giving a total shift of 0–29 positions. At 0 rotation, the output matches the input. At 10, the entire U channel occupies the Y position, Y moves to V, and V moves to U — a pure channel rotation. Intermediate values create inter-channel bit leakage with unpredictable colour and brightness artefacts.

---

#### Knob 2 — XOR Mask
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the XOR mask intensity. Below a minimum threshold (~6% of range), XOR processing is bypassed entirely. Above threshold, the selected XOR mode is applied to the rotated plane vector. In Self mode, adjacent bits within each channel are XOR'd — this highlights edges and transitions. In Cross-Channel mode, Y, U, and V bit planes are folded into each other — this creates saturated colour artefacts and channel-crossing interference patterns.

---

#### Knob 3 — Swap Depth
| Property | Value |
|----------|-------|
| Range | 0 – 10 |
| Default | 0 |

Controls the MSB swap depth between the Y and U channels. At 0, no swap occurs. At maximum (10), all 10 bits of Y and U are exchanged — luminance and blue-difference chrominance switch places entirely. Intermediate values swap only the most significant *N* bits, creating partial channel blending where the coarse structure of Y appears in U and vice versa, while the fine detail remains in its original channel.

---

#### Knob 4 — Time XOR
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the temporal animation depth. When the Animate toggle is active and this control exceeds the minimum threshold, a 10-bit frame counter is XOR'd into all 30 bit planes. The counter increments every frame, creating a 1024-frame animation cycle. Higher Time XOR values enable the injection; the visual effect is a rapid, structured flickering that cycles through XOR patterns over roughly 17 seconds at 60 fps.

---

#### Knob 5 — Crush Floor
| Property | Value |
|----------|-------|
| Range | 0 – 9 |
| Default | 0 |

Sets the crush floor — the bit position below which all planes in every channel are zeroed. At 0, all 10 bits are preserved (full resolution). At 9, only the MSB survives (the image is reduced to a binary silhouette). Intermediate values produce posterisation: the fewer the surviving bits, the coarser the quantisation steps. Because crush operates *after* rotation and XOR, it quantises the already-rearranged bit planes, creating banded versions of the digital artefacts.

---

#### Knob 6 — Output Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the output gain via the interpolator. At 50%, the output is unity gain. Below 50%, the processed signal is attenuated — useful for taming extreme bit-manipulation artefacts. Above 50%, the signal is boosted, which can drive the bit-manipulated output into saturation for high-contrast graphic results.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Rotate Dir** | Left | Mirror |
| **8 — XOR Mode** | Self | Cross-Ch |
| **9 — Animate** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control the rotation direction, XOR algorithm, temporal animation enable, output inversion, and bypass. The Rotate Dir toggle has a dual function — in Mirror mode, it replaces the barrel rotation with a full bit-order reversal, fundamentally changing the character of the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original input signal and the processed output. At 0%, only the original signal is present. At 100%, only the processed signal is output. Intermediate values blend the two, allowing subtle bit-plane artefacts to be layered over the original image.

---

## Guided Exercises

These exercises progress from simple channel rotation to full bit-plane deconstruction, building familiarity with how rotation, XOR, swap, and crush interact on the 30-bit plane vector.

### Exercise 1: Channel Rotation

<img src={stratum_exercise1_result} alt="Channel Rotation result"/>
*Channel Rotation — simulated result across source images.*
**Source**: A colourful live camera feed or recorded footage with distinct red, green, and blue elements.

**Objective**: Understand how barrel rotation moves bit planes between colour channels.

1. **Identity**: Confirm the output matches the input with all controls at zero.
2. **Rotate by 10**: Turn Bit Rotate to approximately one-third of its range. The entire U channel now occupies the Y position — the image takes on a bluish monochrome cast with the original Y appearing in UV positions.
3. **Rotate by 20**: Turn Bit Rotate to approximately two-thirds. Now V occupies Y — the image gains a reddish-magenta cast.
4. **Fine rotation**: Set Bit Rotate to a value between 0 and 10 (roughly 10–30% of range). Individual bits leak between channels, creating partial colour shifts and banding artefacts.
5. **Mirror mode**: Toggle Rotate Dir (Switch 7). The bit-order reversal creates a dramatically different effect — brightness values undergo a nonlinear permutation similar to bit-reversal in the Bitcullis program.

**Key concepts**: Rotation by multiples of 10 produces clean channel swaps, non-multiple rotations create inter-channel bit leakage, mirror reverses the entire significance hierarchy

---

### Exercise 2: XOR Texture Generation

<img src={stratum_exercise2_result} alt="XOR Texture Generation result"/>
*XOR Texture Generation — simulated result across source images.*
**Source**: High-contrast footage with strong edges — text on screen, silhouettes, or geometric patterns.

**Objective**: Explore the two XOR modes and how they interact with barrel rotation.

1. **Self XOR without rotation**: Set XOR Mask above 10%, Bit Rotate at 0. The self-XOR highlights transitions between adjacent bits — the output shows fine edge detail, like a spatial derivative applied per-bit.
2. **Cross-channel XOR**: Toggle XOR Mode (Switch 8). The channels fold into each other — strong colour artefacts appear as Y information leaks into UV.
3. **XOR + rotation**: Set Bit Rotate to ~15 (roughly 50%). The barrel rotation rearranges the planes *before* XOR, so the XOR now operates on a scrambled bit-field. The combined effect is more chaotic than either alone.
4. **Channel swap**: Increase Swap Depth to 5. The top 5 bits of Y and U are exchanged before XOR, creating a luminance/chrominance hybrid.
5. **Bit crush**: Increase Crush Floor to 3. The three LSBs of each channel are zeroed — the XOR texture is posterised into coarser steps.

**Key concepts**: Self XOR acts as a bitwise edge detector, cross-channel XOR creates colour interference, the order is rotation → XOR → crush, so each stage transforms the result of the previous

---

### Exercise 3: Temporal Bit-Plane Animation

<img src={stratum_exercise3_result} alt="Temporal Bit-Plane Animation result"/>
*Temporal Bit-Plane Animation — simulated result across source images.*
**Source**: Any footage — the temporal animation creates its own visual rhythm regardless of source content.

**Objective**: Combine all processing stages with temporal animation for evolving digital textures.

1. **Base effect**: Set Bit Rotate ~10, XOR Mask ~20%, Cross-Channel mode, Crush Floor 2.
2. **Enable animation**: Toggle Animate (Switch 9) to On. Increase Time XOR above ~10%. The frame counter XOR'd into the planes creates a rhythmic visual pulse.
3. **Observe the cycle**: Watch for approximately 17 seconds (1024 frames at 60 fps). The animation cycles — some frames produce clean channel swaps, others full-spectrum glitch.
4. **Sweep Time XOR**: Increase Time XOR toward 100%. More counter bits are injected, creating a more chaotic animation cycle.
5. **Add mirror**: Toggle Rotate Dir to Mirror. The bit reversal combined with temporal XOR creates a completely different animation character — the counter bits interact with the reversed plane order.
6. **Mix down**: Lower Mix to ~50% to layer the animated texture over the original signal as a translucent digital overlay.

**Key concepts**: The frame counter cycles every 1024 frames, temporal XOR creates structured animation, combining rotation + XOR + temporal produces complex evolving textures

---


## Tips

- **Multiples of 10 for clean swaps**: Rotating by exactly 0, 10, or 20 positions produces clean channel rotations with no inter-channel bit leakage. Use these as starting points, then add fine rotation for controlled artefacts.
- **Self XOR for edges**: Self-XOR mode acts as a bitwise edge detector — it highlights transitions between adjacent bit planes. Useful for extracting textural detail from the bit-manipulated signal.
- **Crush after rotation**: Because bit crush operates after rotation, it posterises the *rearranged* planes. Crushing after a 15-position rotation quantises a hybrid of Y and UV data, creating colour-banded posterisation that no standard posteriser can produce.
- **Temporal animation is cyclic**: The 1024-frame cycle means the animation repeats every ~17 seconds at 60 fps. Use Time XOR to control the density of the temporal pattern.
- **Mirror for nonlinear distortion**: Mirror mode reverses the significance hierarchy — the MSB becomes the LSB. This is a nonlinear permutation that produces chaotic brightness and colour mappings, similar to bit-order reversal in Bitcullis.
- **Swap for partial blending**: The Swap Depth control provides a gradual way to blend Y and U content. Low swap depths create subtle colour tinting; high swap depths produce full channel exchange.
- **Mix for layering**: Use the Mix fader at 30–50% to layer the bit-manipulation artefacts as a translucent texture over the original image.
- **Bypass for A/B**: Switch 11 instantly compares the processed and unprocessed signal.

---

## Glossary

| Term | Definition |
|------|------------|
| **Barrel Rotator** | A combinational circuit that shifts all bits in a register by an arbitrary number of positions in a single clock cycle using a multiplexer network. |
| **Bit Crush** | Zeroing the least significant bit planes of a signal, reducing its effective bit depth and creating visible quantisation steps. |
| **Bit Plane** | A single binary layer within a multi-bit pixel value; the MSB plane carries half the dynamic range, the LSB plane carries ±1 count. |
| **DDS** | Direct Digital Synthesis; a technique for generating time-varying signals using a phase accumulator and lookup table. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Frame Counter** | A register that increments on each vertical sync pulse, providing a temporal index for animation effects. |
| **LSB** | Least Significant Bit; the binary digit with the smallest weight in a multi-bit number. |
| **MSB** | Most Significant Bit; the binary digit with the largest weight in a multi-bit number. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **XOR** | Exclusive OR; a logic operation that outputs 1 when its inputs differ and 0 when they match. |
| **YUV** | A colour encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
