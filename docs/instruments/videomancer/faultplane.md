---
draft: false
sidebar_position: 5
slug: /instruments/videomancer/faultplane
title: "Faultplane"
image: /img/instruments/videomancer/faultplane/faultplane_hero.png
---

import faultplane_hero from '/img/instruments/videomancer/faultplane/faultplane_hero.png';
import faultplane_before_after from '/img/instruments/videomancer/faultplane/faultplane_before_after.png';
import faultplane_control_panel from '/img/instruments/videomancer/faultplane/faultplane_control_panel.png';
import faultplane_exercise1_result from '/img/instruments/videomancer/faultplane/faultplane_exercise1_result.png';
import faultplane_exercise2_result from '/img/instruments/videomancer/faultplane/faultplane_exercise2_result.png';
import faultplane_exercise3_result from '/img/instruments/videomancer/faultplane/faultplane_exercise3_result.png';

# Faultplane

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={faultplane_hero} alt="Faultplane hero image"/>
*Faultplane fracturing a natural scene into displaced, mirrored zones with selective blanking.*
<img src={faultplane_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Faultplane applied.*

---

## Overview

**Faultplane** is a spatial displacement and zone-blanking program that splits the video frame into alternating regions using two timing accumulators and applies independent horizontal pixel shifts, mirror flips, and color inversions to each region. The name refers to geological fault planes — surfaces where rock masses shift along a boundary. In Faultplane, the video image is fractured along oscillating boundaries and the fragments are displaced, mirrored, and inverted relative to one another.

The program divides the image into spatial zones using two frequency-driven accumulators — one operating at the line rate (creating horizontal bands) and one at the pixel rate (creating vertical columns). The XOR of these two oscillators produces a checkerboard-like pattern of alternating regions. Each region reads from a dual-port line buffer at a different horizontal offset, creating the visual impression of the image being fractured and shifted along fault lines.

Two independent parameter sets — **Top** and **Bottom** — control the displacement, mirroring, and inversion applied to each region. A blanking threshold gates both accumulators, allowing portions of the image to be replaced with black where both oscillator outputs are below a programmable level.

---

## Background

### Delay Lines and Spatial Displacement

At the heart of Faultplane is a **mirror delay line** — a dual-port line buffer that writes incoming pixels into RAM and reads them back at a different address. By varying the read offset, pixels are shifted horizontally within the scan line. Small offsets produce subtle echo effects; large offsets produce dramatic horizontal displacement where distant parts of the line wrap around and replace nearby content.

The delay line uses two independent RAMs (A and B) that alternate every scan line. While one RAM is being written with new data, the other holds the previous line's data and can be read freely. This dual-buffer architecture allows the FPGA to simultaneously write and read without conflicts.

### Timing Accumulators and Spatial Zoning

Faultplane's two **timing accumulators** generate oscillating signals at programmable frequencies:
- **Accumulator A** (Vert Freq) operates at the **line rate** — it increments once per scan line and resets at the start of each frame. Creates **horizontal bands**.
- **Accumulator B** (Horiz Freq) operates at the **pixel rate** — it increments every clock cycle and resets at the start of each line. Creates **vertical columns**.

The MSB of each accumulator acts as a clock divider. The XOR of the two MSBs creates the **zone selection signal** (`ab_sel`), which alternates between selecting the Top and Bottom parameter sets.

### Mirror and Invert

Each zone can independently **mirror** (horizontally flip the write address) and **invert** (apply bitwise NOT to the pixel data). Mirroring causes the pixel data within a zone to be written in reverse order. Inversion negates every bit of the YUV data, producing a color and luminance negative.

### Processing Amplifier (Displacement Control)

Each accumulator's output is fed through a **proc_amp**: **Delay** = brightness (DC offset), **Displace** = contrast (gain). The DC offset sets *where* the displacement is centered. The gain controls *how much* the displacement varies as the accumulator oscillates. Higher Displace values create displacement that sweeps back and forth across the line as the accumulator oscillates.


---

## Signal Flow

```
Input Video (YUV 4:4:4 30-bit)
│
├── Timing ──────────────────────────────────────────────────────
│   ├─ Accumulator A (Vert Freq — line rate, creates horiz bands)
│   │   └── → proc_amp A (Bot Delay = brightness, Bot Displace = contrast)
│   ├─ Accumulator B (Horiz Freq — pixel rate, creates vert columns)
│   │   └── → proc_amp B (Top Delay = brightness, Top Displace = contrast)
│   └─ ab_sel = MSB(acc_a) XOR MSB(acc_b) — zone selection
│
├── Mirror Delay Line (dual-port RAM, 2048 × 30-bit) ──────────
│   ├─ RAM A: writes on even lines (mirrored by Bot Flip, inverted by Bottom Invert)
│   ├─ RAM B: writes on odd lines (mirrored by Top Flip, inverted by Top Invert)
│   └─ Read: ab_sel selects RAM A or B, offset selects position
│
├── Zone Blanking ──────────────────────────────────────────────
│   └─ If both acc_a AND acc_b < Line Blank threshold: blank to black
│      └─ Blank Invert reverses the condition
│
└── Output Video (YUV 4:4:4 30-bit)
```

The architecture splits naturally into two domains: the **timing domain** (accumulators, zone selection, blanking) and the **spatial domain** (delay line, mirror, invert). The timing domain defines *where* the zones are. The spatial domain defines *what happens* inside each zone. This separation means you can change the zone pattern independently of the displacement — and vice versa.

---

## Parameter Reference

<img src={faultplane_control_panel} alt="Videomancer front panel with Faultplane loaded"/>
*Videomancer's front panel with Faultplane active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Top Delay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0 |
| Suffix | % |

DC offset of horizontal displacement for Top zones. Think of this as setting *where* the fracture displacement is centered on the scan line. At 0%, the Top zones read from the leftmost part of the line buffer; at 100%, they read from the rightmost. Setting different Top and Bottom delays creates visible displacement discontinuities at zone boundaries — this is the "fault" in Faultplane.

---

#### Knob 2 — Top Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Gain applied to Accumulator B's output for Top zones. This determines *how much* the displacement varies within a zone — how far the read address sweeps back and forth. Defaults to 0% (bypass) — no oscillation, displacement is static and determined solely by Top Delay. As you increase this control, the displacement oscillates with the accumulator's frequency, creating rhythmic shifting patterns.

---

#### Knob 3 — Vert Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0 |
| Suffix | % |

Frequency of Accumulator A, which operates at the line rate. This determines the number of horizontal bands per frame. Low values create a few wide bands. High values create many narrow bands. Because the accumulator resets every frame, the band pattern is stable — it does not drift or shift between frames.

---

#### Knob 4 — Bot Delay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0 |
| Suffix | % |

DC offset for Bottom zones. Setting different Top and Bottom delays creates the characteristic fault displacement — adjacent zones read from different positions in the line buffer, producing visible horizontal discontinuities at every zone boundary.

---

#### Knob 5 — Bot Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Gain for Bottom zones. Defaults to 0% (bypass) — no oscillation, displacement is static and determined solely by Bot Delay. Independent of Top Displace (Knob 2). When Top Displace is high and Bot Displace is low, Top zones show strong dynamic displacement while Bottom zones remain relatively static. This asymmetry is what creates the fault-like appearance.

---

#### Knob 6 — Horiz Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0 |
| Suffix | % |

Frequency of Accumulator B, which operates at the pixel rate. This determines the number of vertical columns per line. Combined with Vert Freq (Knob 3), this defines the full zone grid. Low Horiz Freq = few wide columns. High Horiz Freq = many narrow columns. When both frequencies are similar, the zones approximate squares. When they differ, the zones become rectangles.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Top Flip** | Off | On |
| **8 — Bot Flip** | Off | On |
| **9 — Top Invert** | Off | On |
| **10 — Bottom Invert** | Off | On |
| **11 — Blank Invert** | Off | On |

The five toggle switches control independent binary options — mirroring, inversion, and blanking reversal. Switches 7/8 and 9/10 form natural pairs: Top and Bottom versions of the same effect. Switch 11 reverses the blanking condition.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Line Blank
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0 |
| Suffix | % |

Threshold for zone blanking. Compared against both accumulator outputs (acc_a AND acc_b). When both values are below the threshold, the output is blanked to black (or visible if Blank Invert is on). At 0%, no blanking occurs. As you raise the fader, periodic regions of black appear, aligned with the zone grid defined by Vert Freq and Horiz Freq. At 100%, most of the output is blanked.

---

## Guided Exercises

These exercises progress from simple displacement bands to complex fracture grids with blanking. Start by isolating one accumulator, then combine both.

### Exercise 1: Horizontal Displacement Bands

<img src={faultplane_exercise1_result} alt="Horizontal Displacement Bands result"/>
*Horizontal Displacement Bands — simulated result across source images.*
**Source**: Camera feed with recognizable horizontal features — architecture, text, or landscapes.

**Objective**: Learn how the vertical accumulator creates horizontal bands of displaced image content.

1. **Isolate vertical bands**: Set Horiz Freq (Knob 6) fully counter-clockwise to eliminate vertical columns.
2. **Set band frequency**: Set Vert Freq (Knob 3) to about 30%. You should see several horizontal bands.
3. **Displace one set**: Set Top Delay fully counter-clockwise, Top Displace to ~70%. Keep Bot Delay at center, Bot Displace at 0%.
4. **Observe**: Top zones show strong horizontal displacement while Bottom zones pass through undisplaced. The boundaries between them are the "fault lines."
5. **Vary delay**: Slowly sweep Top Delay. Watch the displaced bands shift to read from different parts of the line buffer.
6. **Add dynamics**: Increase Top Displace to see displacement oscillate within each band.
7. **Finer banding**: Increase Vert Freq. More, thinner bands appear, each fractured along its boundary.

**Key concepts**: Accumulator A creates horizontal bands, Delay sets the static offset, Displace sets the oscillation amplitude, zone boundaries create the displacement discontinuities

---

### Exercise 2: Mirror and Invert Zones

<img src={faultplane_exercise2_result} alt="Mirror and Invert Zones result"/>
*Mirror and Invert Zones — simulated result across source images.*
**Source**: Camera feed with strong directional features — faces, text, or architecture.

**Objective**: Explore how mirror and invert create visual discontinuities at zone boundaries.

1. **Set up grid**: Set Vert Freq to ~40%, Horiz Freq to ~25%.
2. **Top Flip**: Enable Top Flip (Switch 7). Top zones now show a mirrored reflection of their content. Zone boundaries become axes of symmetry.
3. **Bottom Invert**: Enable Bottom Invert (Switch 10). Bottom zones show color and brightness negative. Adjacent zones alternate between mirrored positive and inverted negative.
4. **Combine**: Enable both Top Flip and Bottom Invert simultaneously. The image becomes a complex alternating pattern.
5. **Add displacement**: Bring up Top Displace and Bot Displace. The displaced, mirrored, inverted zones create increasingly complex fracture patterns.
6. **Add blanking**: Raise Line Blank to ~50%. Periodic black regions appear at grid intersections.

**Key concepts**: Mirror reverses write order within a zone, invert applies bitwise NOT to all 30 YUV bits, zone boundaries create discontinuities between different processing modes

---

### Exercise 3: Checkerboard Grid with Blanking

<img src={faultplane_exercise3_result} alt="Checkerboard Grid with Blanking result"/>
*Checkerboard Grid with Blanking — simulated result across source images.*
**Source**: Any footage, especially geometric or high-contrast material.

**Objective**: Create a fine-grid fracture pattern with selective blanking.

1. **Fine grid**: Set Vert Freq to ~60%, Horiz Freq to ~50%. Many small zones appear.
2. **Differentiate zones**: Set Top Delay ~25%, Bot Delay ~75%. The displacement difference makes zone boundaries clearly visible.
3. **Add processing**: Enable Top Flip and Bottom Invert for maximum visual contrast between zones.
4. **Apply blanking**: Raise Line Blank to ~50%. Periodic regions of the grid go black, creating a rhythmic pattern of visible and blanked zones.
5. **Invert blanking**: Toggle Blank Invert (Switch 11). The visible and blanked regions swap — you now see the "negative space."
6. **Sweep threshold**: Slowly move Line Blank from 0% to 100% to see the blanking pattern evolve.
7. **Animate**: Vary Vert Freq or Horiz Freq slowly. The zone grid pattern shifts, creating animated fracture motion.

**Key concepts**: Both accumulators contribute to zone selection, blanking is independent of displacement/mirror/invert, Blank Invert shows the negative space, frequency ratio determines zone aspect ratio

---


## Tips

- **Start simple**: Set Horiz Freq to 0% to work with horizontal bands only. Master the vertical accumulator before adding the second axis.
- **Displacement is relative**: The visual effect depends on the *difference* between Top and Bottom delays. Equal delays = invisible boundaries. Different delays = fault-like displacement.
- **Mirror creates symmetry**: Enable one flip for asymmetric mirror effects, both for full bilateral symmetry at every zone boundary.
- **Invert is per-channel**: All 30 bits of YUV data are inverted simultaneously — luminance and chrominance together. One inverted zone next to one normal zone creates maximum visual contrast.
- **Blanking tracks the grid**: The blanking pattern inherits the grid geometry defined by Vert Freq and Horiz Freq.
- **Blank Invert for negative space**: The "negative space" of a blanking pattern is often more visually interesting than the pattern itself.
- **Frequency ratio matters**: Similar Vert and Horiz Freq values create roughly square zones. Different values create rectangles — wide bands or tall columns.
- **Feedback loops**: Routing output back to input creates recursive spatial displacement with complex layered fracture patterns that evolve over time.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bitwise NOT** | A logic operation that flips every bit of a value (0→1, 1→0); applied to all 30 bits of YUV data simultaneously when inversion is enabled. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA used here as dual-port line buffers for scanline storage and displaced readback. |
| **Clock divider** | A circuit that reduces a clock frequency by toggling its output every N input cycles; the MSB of each timing accumulator acts as a divide-by-two clock divider. |
| **DC offset** | A constant value added to a signal, shifting it up or down without changing its shape; the Delay controls set the DC offset of the displacement address. |
| **Dual-port RAM** | Memory with independent read and write ports, allowing simultaneous writing of new data and reading of previously stored data on alternating scanlines. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip (Lattice iCE40 HX4K) that executes the video processing pipeline in real time. |
| **Line rate** | The frequency at which horizontal scanlines are produced; Accumulator A increments once per line, creating horizontal band patterns. |
| **MSB (Most Significant Bit)** | The highest-order bit of a binary value; the MSBs of the two timing accumulators are XOR'd to produce the zone selection signal. |
| **Pixel rate** | The frequency at which individual pixels are clocked; Accumulator B increments every pixel clock cycle, creating vertical column patterns. |
| **Proc amp (Processing Amplifier)** | A circuit that adjusts a signal's gain (contrast) and DC offset (brightness); used here to shape the accumulator outputs into displacement addresses. |
| **Scanline** | One horizontal row of pixels in a video frame; Faultplane's delay line operates on a per-scanline basis. |
| **Timing accumulator** | A register that increments by a programmable amount on each clock or line event, producing an oscillating signal whose frequency determines the zone pattern. |
| **XOR (Exclusive-OR)** | A bitwise logic operation that outputs 1 when inputs differ; used here to combine the two accumulator MSBs into the alternating zone selection signal. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); Faultplane processes all three channels as a 30-bit composite. |
