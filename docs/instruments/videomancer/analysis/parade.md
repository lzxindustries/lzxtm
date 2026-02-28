---
draft: true
sidebar_position: 188
slug: /instruments/videomancer/parade
title: "Parade"
image: /img/instruments/videomancer/parade/parade_hero.png
description: "Program guide for Parade, a Videomancer analysis program for the LZX video synthesizer."
---

import parade_before_after from '/img/instruments/videomancer/parade/parade_before_after.png';
import parade_control_panel from '/img/instruments/videomancer/parade/parade_control_panel.png';
import parade_exercise1_result from '/img/instruments/videomancer/parade/parade_exercise1_result.png';
import parade_exercise2_result from '/img/instruments/videomancer/parade/parade_exercise2_result.png';
import parade_exercise3_result from '/img/instruments/videomancer/parade/parade_exercise3_result.png';
import parade_hero from '/img/instruments/videomancer/parade/parade_hero.png';
import parade_source1_grayscale_ramp_h_1920x1080 from '/img/instruments/videomancer/parade/parade_source1_grayscale_ramp_h_1920x1080.png';
import parade_source2_grayscale_ramp_v_1920x1080 from '/img/instruments/videomancer/parade/parade_source2_grayscale_ramp_v_1920x1080.png';
import parade_source3_step_wedge_21level_512 from '/img/instruments/videomancer/parade/parade_source3_step_wedge_21level_512.png';

# Parade

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={parade_hero} alt="Parade hero image"/>
*Parade rendering a three-column waveform monitor over live video, with green phosphor traces mapping the Y, U, and V channel levels across every scanline.*
<img src={parade_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Parade applied.*

---

## Overview

Before digital scopes and vectorscopes, broadcast engineers relied on cathode-ray tube waveform monitors to see inside the video signal. A phosphor trace painted the instantaneous voltage of each scanline as a vertical dot — low values near the bottom of the screen, high values near the top — producing a luminous curtain of dots whose shape revealed the tonal and color structure of the picture at a glance. Parade brings that tradition into the Videomancer processing pipeline.

The program captures one full scanline of Y, U, and V channel values into three BRAM line buffers. On the next frame, for each horizontal position in each column, the stored channel value is mapped to a vertical screen position and compared against the current vertical scan coordinate. Where the two match within a configurable persistence threshold, a bright dot is drawn in the selected phosphor color. The result is three side-by-side waveform traces — the classic parade display — that update every scanline. Four display modes (Parade, Overlay, RGB, Luma), four phosphor colors (Green, Amber, Blue, White), optional graticule grid lines at 10% / 50% / 90% levels, and a gain control with eight discrete magnification steps give the user a full-featured monitoring tool that can overlay the source video or replace it entirely.

The name *Parade* references the broadcast engineering term for the side-by-side arrangement of channel waveforms. In a standard parade display, each component of the color space gets its own column so that levels, clipping, and color balance can be evaluated independently — exactly what this program provides.

---

## Background

### Waveform Monitors in Broadcast Engineering

The waveform monitor is the oscilloscope of the video world. It displays the voltage of a video signal as a function of horizontal position within each scanline. Engineers use it to verify that peak white does not exceed the legal limit, that black level is properly set, and that the pedestal (setup level) is correct. In a parade configuration, the Y, U, and V components are shown side by side in three equal columns, making it easy to see whether the color components are balanced. Clipping in any channel is immediately visible as a trace that flattens against the top or bottom of the display.

### Phosphor Persistence and CRT Aesthetics

Early waveform monitors used long-persistence phosphors — P31 green for general monitoring, P7 amber for low-light broadcast trucks, P11 blue for photographic recording. The persistence allowed the trace to remain visible between sweeps, creating the characteristic glowing curtain effect. Parade simulates this by widening the dot-match threshold: higher persistence means each dot is drawn not as a single-pixel line but as a vertical smear, mimicking the slow decay of a long-persistence phosphor.

### Gain and Vertical Scale

Professional waveform monitors offer selectable V/div settings that magnify the displayed waveform vertically. At unity gain (1×), a full-range signal fills the display. At 2× gain, the display zooms in on the center of the range, revealing fine detail in mid-tone transitions while clipping the extremes off-screen. Parade implements eight discrete gain levels using shift-based scaling — 0.125×, 0.25×, 0.5×, 1×, 1.5×, 2×, 3×, and 4× — allowing the user to examine narrow signal excursions at high magnification.

### Graticule Overlays

A graticule is the calibrated grid overlay on an oscilloscope or waveform monitor. In Parade, thin horizontal lines are drawn at the 10%, 50%, and 90% positions (lines 108, 540, and 972 of 1080) to provide reference markers. The graticule opacity is independently controllable, allowing it to be subtle or prominent.

### Line Buffers and Dot Rendering

The core of the display engine is a set of three dual-port BRAM line buffers (Y, U, V), each storing 2048 pixel values from the most recent scanline. During the subsequent frame, the stored value at each horizontal position is read, scaled by the gain setting, and mapped to a vertical screen coordinate. The current v_count is compared to the mapped coordinate; if the absolute distance is less than the persistence threshold, a dot is drawn at the phosphor color. This comparison runs for every pixel in every frame, producing the characteristic waveform curtain.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Clock 1: Input Register + Counter Logic ─────────────────────
│   ├─ h_count, v_count ← sync edge detection
│   ├─ line_buffer_y.write(h_count, Y_in)
│   ├─ line_buffer_u.write(h_count, U_in)
│   └─ line_buffer_v.write(h_count, V_in)
│
├── Clock 2: Address Compute ────────────────────────────────────
│   └─ rd_addr = remap h_count within column (×3 for parade)
│
├── Clocks 3–4: BRAM Read Latency (2 clocks) ───────────────────
│   └─ stored_y, stored_u, stored_v ← line buffer read
│
├── Clock 5: Register BRAM Output ───────────────────────────────
│   └─ Break critical path for next-stage multiply
│
├── Clock 6: Gain Scaling ───────────────────────────────────────
│   ├─ abs_offset = |stored_ch - 512|
│   ├─ scaled = abs_offset × gain_factor (shift-based, 8 levels)
│   └─ mapped_pos = 540 ± scaled
│
├── Clock 7: Compare + Graticule ────────────────────────────────
│   ├─ dot_hit = |v_count - mapped_pos| ≤ (1 + persist/32)
│   ├─ col_sel = h_count column selection (Y/U/V)
│   └─ grat_hit = graticule_en AND v_count ∈ {108, 540, 972}
│
├── Clock 8: Output Compose ─────────────────────────────────────
│   ├─ dot_active → phosphor color (Green/Amber/Blue/White)
│   ├─ grat_hit → graticule line (half grat_opacity, achromatic)
│   ├─ over_video → pass-through source Y/U/V
│   └─ else → dark background (brightness/4, achromatic)
│
├── Clocks 9–12: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(dry, composed, mix_amount) per Y, U, V
│
├── Sync Signals ────────────────────────────────────────────────
│   └─ 12-stage delay pipeline (hsync_n, vsync_n, field_n, YUV)
│
└── Output Mux ──────────────────────────────────────────────────
    └─ bypass ? delayed_input : mix_result
```

The critical interaction is between the line buffer write path and the display render path. During each scanline, the current pixel values are written into the BRAM line buffers at the h_count address. Simultaneously, the read path fetches the *previously stored* line's values at a remapped address — in parade mode, each of the three 640-pixel columns maps its local position back to the full 1920-pixel line range via a ×3 multiplication. The gain stage then converts the 10-bit channel value to a 12-bit vertical screen position using shift-based discrete magnification levels, avoiding any hardware multiplier. The persistence threshold widens the dot match from a single-pixel hair to a configurable vertical smear, recreating the phosphor bloom of an analog CRT waveform monitor.

---

## Parameter Reference

<img src={parade_control_panel} alt="Videomancer front panel with Parade loaded"/>
*Videomancer's front panel with Parade active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Intensity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness of the phosphor trace dots. At 0%, the dots are invisible — the display shows only the background and graticule. At 100%, the dots are drawn at maximum luminance in the selected phosphor color. This directly sets the Y value of dot pixels; the U and V components are determined by the phosphor color selection toggle.

---

#### Knob 2 — Persist
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the vertical thickness of each waveform dot, simulating the persistence of a CRT phosphor. At 0%, each dot is a single-pixel-high hairline. As you increase the control, the match threshold widens and each dot becomes a vertical smear — the trace thickens into a luminous band. At maximum, the smear reaches ±31 pixels, creating a soft, glowing curtain. This is the primary control for achieving the classic CRT waveform monitor aesthetic.

---

#### Knob 3 — Gain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Vertical gain control with eight discrete magnification levels selected by the top 3 bits of the register value: 0.125×, 0.25×, 0.5×, 1×, 1.5×, 2×, 3×, 4×. At unity (1×), a full-range 0–1023 signal maps to the full 1080-line display height. At 4×, the display zooms into the center quarter of the signal range, revealing fine-grained structure in mid-tone transitions while clipping the extremes off-screen. Lower gain values compress the trace into a narrow band in the center of the display.

---

#### Knob 4 — Grat Opac
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the brightness of the graticule reference lines. These are thin horizontal lines drawn at the 10%, 50%, and 90% vertical positions (lines 108, 540, and 972). The graticule is achromatic (U=V=512) and drawn at half of this control's value. At 0%, the graticule is invisible even when enabled by Toggle 9. At 100%, the reference lines are prominent calibration markers.

---

#### Knob 5 — Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Rotates the hue of the phosphor trace. This control shifts the chrominance of all dot pixels around the color wheel. At 0°, the color is determined solely by the Phosphor toggle (Green/Amber/Blue/White). As you rotate the hue, the phosphor color shifts — green becomes cyan, amber becomes red, and so on. This allows fine-tuning the aesthetic of the waveform display beyond the four preset phosphor colors.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the background brightness behind the waveform traces. The background Y value is this control divided by 4. At 0%, the background is pure black — the classic waveform monitor look. Increasing the value reveals the background as a dim gray field, which can help distinguish the waveform area from the surrounding blanking region when Over Video is off.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Parade | Overlay |
| **8 — Phosphor** | Green | Amber |
| **9 — Graticule** | Off | On |
| **10 — Over Video** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 form two related 2-bit selectors controlling display mode and phosphor color. Toggle 9 enables the graticule overlay. Toggle 10 selects whether the scope renders on a dark background or composites over the source video. Toggle 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) input signal and the wet (waveform monitor) output. At 0%, the output is pure source video. At 100%, the output is the full waveform display. Intermediate values blend the two, which can create a semi-transparent scope overlay effect useful for monitoring during live performance.

---

## Guided Exercises

These exercises progress from basic waveform reading to advanced monitoring techniques, building familiarity with Parade's scope display in the context of live video analysis.

### Exercise 1: Reading a Parade Display

<img src={parade_exercise1_result} alt="Reading a Parade Display result"/>
*Reading a Parade Display — simulated result across source images.*
**Source**: A color bar test pattern or footage with known brightness levels (skin tones, pure white, pure black regions).

**Objective**: Learn to read the three-column parade display and identify signal levels by their vertical position.

1. **Default parade view**: Ensure Mode is set to Parade. Feed color bars or a known-level source.
2. **Read the Y column**: The left column shows luminance. White bars should trace near the top of the display; black bars trace near the bottom. Mid-gray sits at the 50% graticule line.
3. **Read U and V columns**: The center (U) and right (V) columns show chrominance. For achromatic signals (gray, white, black), both traces sit at the center line (512 = no color). Saturated colors push the traces above or below center.
4. **Enable Graticule**: Toggle Graticule On and increase Grat Opac to ~60%. Use the 10%/50%/90% lines as reference markers.
5. **Adjust Gain**: Sweep the Gain control through its eight magnification levels. Watch the waveform expand and contract vertically. At 2× or 4×, fine-grained tonal transitions that were invisible at 1× become clearly resolved.

**Key concepts**: Parade separates Y/U/V into three columns for independent monitoring, vertical position maps to signal level, graticule lines provide calibrated references, gain magnifies the vertical scale

---

### Exercise 2: Phosphor Aesthetics

<img src={parade_exercise2_result} alt="Phosphor Aesthetics result"/>
*Phosphor Aesthetics — simulated result across source images.*
**Source**: Any dynamic footage — camera feed, music video, or abstract patterns.

**Objective**: Explore the CRT aesthetic controls — phosphor color, persistence, and intensity — to create visually evocative waveform displays.

1. **Set high persistence**: Turn Persist to ~80%. The waveform traces become thick, glowing bands — the signature CRT look.
2. **Cycle phosphors**: Switch through Green, Amber, Blue, and White. Each gives a distinctly different mood — clinical green, warm amber, cold blue, stark white.
3. **Adjust intensity**: Push Intensity to ~90% for bright, saturated traces. Pull it back to ~30% for a dim, subtle glow.
4. **Rotate hue**: Sweep the Hue pot through 360° to shift the phosphor color continuously. Find a custom color that complements your source material.
5. **Enable Over Video**: Toggle Over Video On. The waveform traces now overlay the source picture — a live heads-up display of signal levels on the image itself.
6. **Background brightness**: With Over Video Off, increase Brightness to ~40% to see the display area as a gray field, separating it from the blanking surround.

**Key concepts**: Persistence thickens traces for CRT emulation, phosphor color sets the mood, hue provides continuous fine-tuning, Over Video composites scope onto the picture

---

### Exercise 3: Gain Zoom and Detail Analysis

<img src={parade_exercise3_result} alt="Gain Zoom and Detail Analysis result"/>
*Gain Zoom and Detail Analysis — simulated result across source images.*
**Source**: Footage with subtle tonal detail — skin tones, fabric textures, or gradient test patterns.

**Objective**: Use high gain magnification to examine fine signal structure that is invisible at unity scale.

1. **Feed subtle content**: Use a camera aimed at skin or fabric — signals with narrow dynamic range.
2. **Set gain to 1×**: The waveform occupies only a narrow band in the center of the display. Fine tonal gradations are invisible at this scale.
3. **Increase gain to 4×**: Turn Gain fully clockwise. The display zooms into the center quarter of the signal range. Fine texture and noise that were invisible at 1× are now clearly resolved as separated trace lines.
4. **Lower persistence**: Set Persist to ~10% for thin, precise traces. Each individual value is visible as a distinct dot rather than a blurred band.
5. **Sweep source content**: Slowly change the camera angle or lighting. Watch the magnified trace respond to subtle brightness shifts that are invisible in the picture itself.
6. **Compare with overlay**: Enable Over Video and reduce Mix to ~60% for a semi-transparent high-magnification scope overlaid on the picture.

**Key concepts**: Gain magnifies the vertical scale to reveal fine detail, low persistence provides maximum precision, high gain clips extreme values off-screen, overlaid scope enables simultaneous image and signal analysis

---


## Tips

- **Green phosphor for authenticity**: The P31 green preset matches the classic Tektronix waveform monitor look. Combine with high persistence for maximum CRT nostalgia.
- **Low persistence for precision**: When reading exact signal levels, reduce Persist to near-zero for thin, precise traces. Each pixel corresponds to a single signal value.
- **Gain zoom for noise analysis**: At 4× gain, sensor noise and quantization artifacts in the source become clearly visible as jittering dot clusters — useful for evaluating camera quality.
- **Over Video for live monitoring**: Toggle Over Video On during live performance to get a heads-up signal level display without leaving the picture view.
- **Graticule for quick level checks**: Enable the graticule and look for Y traces touching the 10% or 90% lines — this indicates the signal is approaching the legal limits for broadcast.
- **Mix for overlay compositing**: At 30–50% Mix with Over Video Off, the waveform display becomes a semi-transparent overlay that can be composited into the final output for video art applications.
- **Hue rotation for creative use**: Although Parade is primarily a monitoring tool, rotating the phosphor hue creates colorful oscilloscope aesthetics suitable for VJ performance or music visualization.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for the three channel line buffers. |
| **DDS** | Direct Digital Synthesis; a digital technique for generating periodic waveforms using a phase accumulator. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Gain** | Vertical magnification of the waveform display, analogous to V/div on an oscilloscope. |
| **Graticule** | Calibrated reference grid lines overlaid on the waveform display at known signal levels. |
| **Line Buffer** | A BRAM-based memory that stores one complete scanline of pixel values for subsequent readout and display. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Parade** | A waveform display layout where Y, U, and V channels are shown in three side-by-side columns. |
| **Persistence** | The duration a CRT phosphor dot remains visible after excitation; simulated by widening the vertical dot match threshold. |
| **Phosphor** | The luminescent coating inside a CRT that glows when struck by an electron beam; different phosphor types emit different colors. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
