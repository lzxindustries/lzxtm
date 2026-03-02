---
draft: true
sidebar_position: 232
slug: /instruments/videomancer/redacted
title: "Redacted"
image: /img/instruments/videomancer/redacted/redacted_hero.png
description: "Broadcast television and government documents share a common visual vocabulary: the black bar."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import redacted_hero from '/img/instruments/videomancer/redacted/redacted_hero.png';
import redacted_control_panel from '/img/instruments/videomancer/redacted/redacted_control_panel.png';
import redacted_exercise1_result from '/img/instruments/videomancer/redacted/redacted_exercise1_result.png';
import redacted_exercise2_result from '/img/instruments/videomancer/redacted/redacted_exercise2_result.png';
import redacted_exercise3_result from '/img/instruments/videomancer/redacted/redacted_exercise3_result.png';
import redacted_source1_kodim15 from '/img/instruments/videomancer/redacted/redacted_source1_kodim15.png';
import redacted_source2_kodim15_bw from '/img/instruments/videomancer/redacted/redacted_source2_kodim15_bw.png';
import redacted_source3_male_1024 from '/img/instruments/videomancer/redacted/redacted_source3_male_1024.png';

# Redacted

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: redacted_source1_kodim15, after: redacted_hero },
    { label: "Kodim15 B&W", before: redacted_source2_kodim15_bw, after: redacted_hero },
    { label: "Male", before: redacted_source3_male_1024, after: redacted_hero },
  ]}
/>
*Redacted applying luma-threshold censorship bars to bright regions of a video stream, with configurable bar orientation and white border trim.*

---

## Overview

Broadcast television and government documents share a common visual vocabulary: the black bar. Whether obscuring a face, a license plate, or a classified paragraph, the solid black rectangle is the universal sign that something has been deliberately hidden. Redacted brings that vocabulary into the video synthesis domain, detecting bright (or dark) regions of the input signal and covering them with solid censorship bars in real time.

The detection engine works by accumulating luma values along each scan line. When a sustained run of pixels exceeds a configurable brightness threshold, the region is flagged and covered with a near-black bar. A margin control extends the bar beyond the detected boundaries. In vertical mode, the accumulator works across lines instead — when an entire scan line is bright enough, subsequent lines within a configurable height window are blacked out. The result is an adaptive, content-responsive censorship overlay that follows the video signal's tonal structure.

The name is a direct reference to redacted documents — classified text covered by black bars, where the shape of the redaction itself becomes a visual element that hints at what lies beneath.

---

## Background

### What Is Luma Thresholding?

At the core of Redacted is a simple brightness test: is this pixel above or below a threshold? The Threshold pot sets the luma cutoff, and the Sensitivity pot adds an additional offset that fine-tunes the detection boundary. Together they define a luma gate — pixels above the combined threshold are flagged for redaction. The Invert toggle reverses the sense of the test, flagging dark regions instead of bright ones. This is the same principle used in broadcast luminance keyers, but applied here to drive a censorship overlay rather than a compositing mask.

### What Is Run-Length Detection?

A single bright pixel should not trigger a full censorship bar. Redacted requires a sustained *run* of above-threshold pixels before activating redaction. The Bar Width pot controls how many consecutive bright pixels are needed — mapped from the 0–1023 register value to a run threshold of 4–63 pixels. This prevents noise and isolated bright specks from triggering false bars. Once a run is detected, the bar stays active for an additional margin (controlled by the Margin pot), extending coverage past the end of the detected region.

### What Are Horizontal vs Vertical Bars?

In horizontal mode, the detection and bar drawing operate pixel-by-pixel within each scan line. Bright horizontal runs trigger horizontal bars — the classic censorship stripe across a face or word. In vertical mode, the accumulator tracks total line brightness across the entire scan line. When a line's accumulated brightness exceeds the threshold, subsequent scan lines within the Bar Height window are blacked out. This produces vertical censorship columns — useful for obscuring full-height regions of the frame like doorways, windows, or monitor screens.

### What Is Bar Border?

The Border toggle adds a thin bright-white edge (Y=940) at the transitions of bar regions. This mimics the visual convention of document redaction stamps, where the censorship bar has a visible border or box outline. The border is one pixel wide at the start and end of each bar region, creating a crisp visual separation between the redacted and unredacted content.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register ────────────────────────────────────
│   └─ Latch Y, U, V input values
│
├── Stage 2: Luma Accumulator + Threshold ──────────────────────
│   ├─ Threshold compare: Y vs (threshold + sensitivity/4)
│   ├─ Invert toggle: dark-detect or bright-detect
│   ├─ Run counter: consecutive above-threshold pixels
│   ├─ Run active: triggered when run_count ≥ run_thresh
│   └─ Line brightness: IIR accumulator for vertical mode
│
├── Stage 3: Bar Region Detect + Margin ────────────────────────
│   ├─ Horizontal bar: active when run detected + trailing margin
│   ├─ Vertical bar: triggered by line brightness, persists for
│   │                bar_height lines
│   └─ Border detect: transition pixels at bar edges
│
├── Stage 4: Bar Draw + Output Compose ─────────────────────────
│   ├─ H/V mode select: horizontal or vertical bars
│   ├─ Bar interior: near-black (Y=64, U=512, V=512)
│   ├─ Border pixel: bright white (Y=940, U=512, V=512)
│   └─ No bar: pass through original Y, U, V
│
├── Mix Stage (4 clk) ──────────────────────────────────────────
│   └─ 3× interpolator_u: crossfade dry ↔ wet per Mix fader
│
├── Bypass Mux ─────────────────────────────────────────────────
│   └─ Toggle 11: select mixed output or delayed dry signal
│
└── Sync Delay Pipeline ────────────────────────────────────────
    └─ 8-clock shift register for hsync, vsync, field, Y, U, V
```

The detection pipeline is purely one-dimensional — horizontal bars track pixel runs within a single line, while vertical bars track accumulated line brightness across successive lines. There is no 2D spatial detection or frame buffering (zero BRAM design). The Threshold and Sensitivity pots combine additively with saturation clamping to set the effective detection boundary. The run threshold derived from Bar Width ranges from 4 to 63 consecutive pixels, preventing noise triggers while keeping detection responsive.

---

## Parameter Reference

<img src={redacted_control_panel} alt="Videomancer front panel with Redacted loaded"/>
*Videomancer's front panel with Redacted active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Bar W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the luma threshold for detection. At low values, only very bright pixels trigger redaction. At high values, even moderate brightness is flagged. The threshold combines additively with the Sensitivity offset (Pot 4) — the effective detection boundary is `threshold + sensitivity/4`, clamped to 1023. With the Invert toggle active, the sense reverses: the threshold defines the darkness level below which pixels are flagged.

---

#### Knob 2 — Sensitiv
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the horizontal bar extension width by setting the run-length threshold. The 10-bit register maps to a required run of 4–63 consecutive above-threshold pixels. Low values mean even short bright stretches trigger a bar. High values require sustained bright regions — a wide, continuous bright area — before redaction activates. This prevents isolated bright pixels or noise from triggering false censorship bars.

---

#### Knob 3 — Bar Dens
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the vertical bar height in lines when vertical mode is active. After a bright scan line is detected, subsequent lines within this height window are also blacked out. The register value maps to 2–256 lines of vertical extension. At low values, vertical bars are thin stripes. At high values, vertical bars can cover large swaths of the frame. Has no visible effect in horizontal mode.

---

#### Knob 4 — Opacity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adjusts detection sensitivity by adding an offset to the base threshold. The sensitivity register value is right-shifted by 2 bits (divided by 4) and added to the Threshold pot value. This provides fine-tuning of the detection boundary — you can set a coarse threshold with Pot 1 and refine it with Pot 4. The combined value is clamped to 1023.

---

#### Knob 5 — Pattern
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the trailing margin that extends bars beyond the detected region. After a run ends (above-threshold pixels stop), the bar stays active for an additional number of pixels determined by this control. The register value maps to 0–255 extra margin pixels. Higher values create wider bars that extend well past the actual bright region, producing a conservative censorship that hides context around the detected area.

---

#### Knob 6 — Border
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved — not connected to any signal in the current VHDL implementation. Turning this pot has no effect on the output. Future firmware revisions may assign functionality to this control.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Bars | Blocks |
| **8 — Class** | Secret | Top Sec |
| **9 — Color** | Black | White |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Three of the five toggles are active in the current implementation. Toggle 7 selects horizontal or vertical bar orientation. Toggle 8 enables the white border trim on bars. Toggle 9 inverts the detection sense. Toggle 10 is reserved (not connected). Toggle 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input and the processed (censored) output. At 0, the original signal passes through unmodified. At 1023, the full censorship effect is applied. Intermediate values blend proportionally via the interpolator. The bypass toggle (Toggle 11) overrides this fader when active.

---

## Guided Exercises

These exercises demonstrate the detection engine, bar styling, and creative applications of the censorship overlay from practical obscuring to abstract pattern generation.

### Exercise 1: Classic Censorship Bars

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: redacted_source1_kodim15, after: redacted_exercise1_result },
    { label: "Kodim15 B&W", before: redacted_source2_kodim15_bw, after: redacted_exercise1_result },
    { label: "Male", before: redacted_source3_male_1024, after: redacted_exercise1_result },
  ]}
/>
*Classic Censorship Bars — simulated result across source images.*
**Source**: A live camera feed of a person's face or a document with text, ensuring strong brightness contrast.

**Objective**: Set up basic horizontal censorship bars that track bright regions of the source.

1. **Set threshold**: Start Threshold at about 50%. Bright areas of the face or text should start triggering bars.
2. **Adjust bar width**: Set Bar Width to about 40% so that short bright stretches are enough to trigger.
3. **Add margin**: Increase Margin to about 30% to extend bars past the detected region edges.
4. **Enable border**: Turn Border on (Toggle 8). White outlines appear at bar edges.
5. **Fine-tune sensitivity**: Sweep Sensitivity to narrow or widen the detection gate.
6. **Invert test**: Toggle Invert (Toggle 9) to see bars on dark regions instead.

**Key concepts**: Luma thresholding detects bright regions, run-length detection prevents noise triggers, margin extends bars past detected boundaries, border adds visual framing

---

### Exercise 2: Vertical Redaction Columns

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: redacted_source1_kodim15, after: redacted_exercise2_result },
    { label: "Kodim15 B&W", before: redacted_source2_kodim15_bw, after: redacted_exercise2_result },
    { label: "Male", before: redacted_source3_male_1024, after: redacted_exercise2_result },
  ]}
/>
*Vertical Redaction Columns — simulated result across source images.*
**Source**: Footage with vertical bright regions — windows, doorways, monitors, or vertical stripes.

**Objective**: Use vertical bar mode to create full-height censorship columns that track line brightness.

1. **Switch to vertical**: Set H/V Bars to Vertical (Toggle 7).
2. **Set threshold**: Threshold at about 40% to detect moderately bright lines.
3. **Set bar height**: Increase Bar Height to about 60%. After a bright line, subsequent lines are also blacked out.
4. **Observe accumulation**: The vertical bars persist across multiple lines, creating column-like censorship blocks.
5. **Add border**: Enable Border for visible column edges.
6. **Compare modes**: Toggle between Horizontal and Vertical to see how the same source triggers different bar patterns.

**Key concepts**: Vertical mode accumulates line brightness across scan lines, bar height controls persistence in lines, horizontal and vertical modes use different detection algorithms

---

### Exercise 3: Abstract Threshold Patterns

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: redacted_source1_kodim15, after: redacted_exercise3_result },
    { label: "Kodim15 B&W", before: redacted_source2_kodim15_bw, after: redacted_exercise3_result },
    { label: "Male", before: redacted_source3_male_1024, after: redacted_exercise3_result },
  ]}
/>
*Abstract Threshold Patterns — simulated result across source images.*
**Source**: High-contrast footage, pattern generators, or feedback loops.

**Objective**: Push the detection engine to extremes for abstract pattern generation rather than practical censorship.

1. **Low threshold**: Set Threshold to about 20% so nearly everything triggers detection.
2. **Minimum bar width**: Set Bar Width low so even brief bright flashes produce bars.
3. **Zero margin**: Set Margin to 0 for tight, precisely timed bars.
4. **No border**: Turn Border off for solid black bars without white framing.
5. **Half mix**: Set Mix to about 50% for a ghostly overlay that shows bars semi-transparently.
6. **Invert rapidly**: Toggle Invert on and off to flip the pattern — the bars and the gaps swap.
7. **Feedback**: Route the output back to the input. The bars themselves become the content, creating recursive censorship patterns.

**Key concepts**: At extreme settings the detection becomes a full-frame pattern generator, mix fader creates semi-transparent overlay effects, feedback loops create recursive censorship structures

---


## Tips

- **Threshold and Sensitivity together**: Use Threshold for coarse detection range and Sensitivity for fine adjustment. Together they define the exact luma gate boundary.
- **Bar Width prevents false triggers**: If you see bars flickering on noise, increase Bar Width to require longer runs before detection activates.
- **Margin is conservative**: Add margin to ensure bars cover a bit beyond the bright region — this mirrors real broadcast censorship practice where bars intentionally overshoot.
- **Vertical mode is line-based**: Vertical bars don't detect vertical edges — they detect bright *scan lines*. A horizontal bright stripe triggers vertical bars; a vertical bright stripe triggers horizontal bars.
- **Border adds legibility**: The white border makes bars visible against dark backgrounds where a plain black bar would be invisible.
- **Feedback for recursion**: Routing the output back to the input creates recursive censorship — bars cover bars, producing evolving stripe patterns.
- **Reserved controls are safe**: Pot 6 and Toggle 10 do nothing in the current version. Leave them at any position.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bar** | A solid rectangular region drawn over detected content, typically near-black (Y=64), simulating broadcast censorship or document redaction. |
| **BRAM** | Block RAM; dedicated FPGA memory, not used by this program (zero BRAM, register-based design). |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip executing the video processing pipeline. |
| **IIR** | Infinite Impulse Response; a digital filter whose output depends on both current input and previous output, used here for line brightness accumulation. |
| **Interpolator** | A hardware multiply-accumulate unit for linear crossfading between two signals. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Margin** | Extra pixels of bar coverage extending past the end of a detected bright run, preventing partial exposure. |
| **Run-Length** | The number of consecutive pixels meeting a condition; used here to require sustained brightness before triggering redaction. |
| **Threshold** | A brightness cutoff value; pixels above (or below, when inverted) this level are flagged for redaction. |
| **YUV** | Color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
