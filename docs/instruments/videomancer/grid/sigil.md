---
draft: true
sidebar_position: 235
slug: /instruments/videomancer/sigil
title: "Sigil"
image: /img/instruments/videomancer/sigil/sigil_hero.png
---

import sigil_animation from '/img/instruments/videomancer/sigil/sigil_animation.gif';
import sigil_control_panel from '/img/instruments/videomancer/sigil/sigil_control_panel.png';
import sigil_exercise1_result from '/img/instruments/videomancer/sigil/sigil_exercise1_result.gif';
import sigil_exercise2_result from '/img/instruments/videomancer/sigil/sigil_exercise2_result.gif';
import sigil_exercise3_result from '/img/instruments/videomancer/sigil/sigil_exercise3_result.gif';
import sigil_hero from '/img/instruments/videomancer/sigil/sigil_hero.png';

# Sigil

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={sigil_hero} alt="Sigil hero image"/>
*Sigil passing video through unchanged — a placeholder program reserving a slot for future grid-based processing.*
<img src={sigil_animation} alt="Sigil animated output"/>
*Sigil output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Sigil is a placeholder program currently in development. In its present firmware, it performs a single-clock passthrough — every YUV sample, sync pulse, and timing flag passes from input to output without modification. The program slot is reserved for a future grid-based visual processing module.

Because no processing is active, Sigil functions as a transparent wire. Any video signal routed through it emerges pixel-identical on the other side (delayed by one clock cycle). This makes it useful as a no-op reference point for signal chain verification and latency measurement.

The name *sigil* — a symbol believed to carry inherent meaning or power — reflects the intent that this program slot will eventually contain a fully realized processing architecture. For now, it stands as a named placeholder within the program registry.

---

## Background

### What Is a Passthrough Program?

A passthrough program copies its input directly to its output with no modification. In FPGA terms, this is implemented as a single clocked register stage: on every rising clock edge, all input port values are latched into their corresponding output ports. This adds exactly one clock cycle of latency (approximately 13.5 ns at 74.25 MHz) and consumes minimal resources — roughly 7 flip-flops for the 30-bit YUV data plus sync signals.

### Why Use a Placeholder?

The Videomancer program registry allocates fixed slots for each named program. Reserving a slot with a passthrough implementation ensures that the program ID, name, and category are established in the build system and firmware before the actual processing logic is written. This avoids program ID conflicts and allows the documentation, TOML metadata, and test infrastructure to be created incrementally.

### Grid Category Programs

Programs in the Grid category typically generate or manipulate geometric grid patterns — lines, meshes, coordinate overlays, and spatial subdivision structures. Sigil's eventual implementation will join this family. The passthrough behavior is temporary and will be replaced when the program's processing architecture is finalized.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
└── Single Clock Register ──────────────────────────────────────
    │
    ├─ Y  → Y  (unchanged)
    ├─ U  → U  (unchanged)
    ├─ V  → V  (unchanged)
    ├─ hsync_n → hsync_n (unchanged)
    ├─ vsync_n → vsync_n (unchanged)
    ├─ avid → avid (unchanged)
    └─ field_n → field_n (unchanged)
```

The entire architecture is a single synchronous process. All seven port signals (Y, U, V, hsync_n, vsync_n, avid, field_n) are registered on the rising edge of the clock with no conditional logic, no multiplexing, and no parameter-dependent behavior. The one-clock delay aligns all signals identically — there is no differential latency between video data and sync timing.

---

## Parameter Reference

<img src={sigil_control_panel} alt="Videomancer front panel with Sigil loaded"/>
*Videomancer's front panel with Sigil active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

### Toggle Switches (Switches 7–11)


---

### Linear Potentiometer (Fader 12)


---

## Guided Exercises

Because Sigil is a passthrough program, these exercises focus on verifying transparent signal transfer and comparing Sigil's output against the unprocessed input to confirm pixel-identical fidelity.

### Exercise 1: Passthrough Verification

<img src={sigil_exercise1_result} alt="Passthrough Verification result"/>
*Passthrough Verification — simulated result across source images.*
**Objective**: Confirm that Sigil passes the input signal through without any modification to luminance, chrominance, or sync timing.

1. **Load Sigil**: Select the Sigil program on the Videomancer.
2. **Feed reference**: Route a color bar test pattern to the input.
3. **Compare output**: Observe the output on a waveform monitor or vectorscope. Verify that Y, U, and V levels match the input exactly.
4. **Check sync**: Confirm that hsync, vsync, and field timing are preserved without jitter or offset beyond the single-clock pipeline delay.
5. **Sweep controls**: Turn all six knobs and toggle all five switches. Confirm that no control produces any visible change.

**Key concepts**: Passthrough programs add one clock of latency, all controls are inactive in placeholder firmware, output should be pixel-identical to input

---

### Exercise 2: Latency Measurement

<img src={sigil_exercise2_result} alt="Latency Measurement result"/>
*Latency Measurement — simulated result across source images.*
**Objective**: Measure the single-clock pipeline delay introduced by Sigil's register stage.

1. **Split input**: Route the same source to both the Videomancer input and a reference monitor.
2. **Load Sigil**: Select the Sigil program.
3. **Compare timing**: Using a dual-input oscilloscope or frame-accurate comparison, verify that the output is delayed by exactly one clock cycle relative to the input.
4. **Document**: Record the measured delay for comparison against programs with longer pipelines.

**Key concepts**: Single-register passthrough adds minimal latency, useful as a baseline for measuring other programs' pipeline depths

---

### Exercise 3: Control Inactivity Sweep

<img src={sigil_exercise3_result} alt="Control Inactivity Sweep result"/>
*Control Inactivity Sweep — simulated result across source images.*
**Objective**: Systematically verify that every control is inactive in the current firmware.

1. **Load Sigil**: Select the Sigil program with a known video input.
2. **Knob sweep**: One at a time, sweep each of the six rotary potentiometers through their full range. Confirm no change in the output.
3. **Toggle sweep**: Flip each of the five toggle switches. Confirm no change.
4. **Fader sweep**: Move the linear potentiometer through its full range. Confirm no change.
5. **Rapid parameter changes**: Move multiple controls simultaneously. Confirm the output remains stable and identical to the input.

**Key concepts**: Placeholder programs must not respond to any control input, confirming parameter isolation before active processing is implemented

---


## Tips

- **Use as a reference**: Sigil is useful as a "wire" program for measuring latency introduced by other programs in the chain — compare their output timing against Sigil's single-clock delay.
- **Verify signal integrity**: Route through Sigil to confirm that the Videomancer I/O path is clean before loading a complex processing program.
- **No controls are active**: All knobs, toggles, and faders are reserved for the future implementation. Do not expect any parameter to produce a visible effect.
- **Minimal resource usage**: Sigil consumes approximately 7 flip-flops and zero BRAMs, making it the lightest program in the library.
- **Placeholder status**: This program is in active development. Future firmware updates will replace the passthrough with grid-based processing.
- **Category intent**: Sigil is categorized as Grid, indicating that its eventual implementation will involve geometric grid patterns, spatial subdivision, or coordinate-based visual structures.

---

## Glossary

| Term | Definition |
|------|------------|
| **Clock Cycle** | One period of the FPGA master clock (approximately 13.5 ns at 74.25 MHz). Sigil's single-register pipeline adds exactly one clock cycle of latency. |
| **Flip-Flop** | A basic FPGA storage element that captures and holds a single bit of data on each clock edge. |
| **Passthrough** | A program that copies input to output without modification, adding only pipeline delay. |
| **Placeholder** | A program slot reserved in the registry with minimal or no processing, to be replaced by a full implementation in a future firmware release. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
