---
draft: true
sidebar_position: 260
slug: /instruments/videomancer/terminal
title: "Terminal"
image: /img/instruments/videomancer/terminal/terminal_hero.png
description: "Every home computer of the early 1980s presented its output on a CRT monitor with a single-color phosphor — green, amber, or crisp white."
---

import terminal_before_after from '/img/instruments/videomancer/terminal/terminal_before_after.png';
import terminal_control_panel from '/img/instruments/videomancer/terminal/terminal_control_panel.png';
import terminal_exercise1_result from '/img/instruments/videomancer/terminal/terminal_exercise1_result.png';
import terminal_exercise2_result from '/img/instruments/videomancer/terminal/terminal_exercise2_result.png';
import terminal_exercise3_result from '/img/instruments/videomancer/terminal/terminal_exercise3_result.png';
import terminal_hero from '/img/instruments/videomancer/terminal/terminal_hero.png';
import terminal_source1_kodim15 from '/img/instruments/videomancer/terminal/terminal_source1_kodim15.png';
import terminal_source2_kodim03 from '/img/instruments/videomancer/terminal/terminal_source2_kodim03.png';
import terminal_source3_kodim15_bw from '/img/instruments/videomancer/terminal/terminal_source3_kodim15_bw.png';

# Terminal

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={terminal_hero} alt="Terminal hero image"/>
*Terminal applying green phosphor tinting and CRT scanline darkening to transform input video into a vintage computer monitor display.*
<img src={terminal_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Terminal applied.*

---

## Overview

Every home computer of the early 1980s presented its output on a CRT monitor with a single-color phosphor — green, amber, or crisp white. The image was built from horizontal scan lines, and every other line was slightly darker, giving the display its characteristic striped texture. Terminal recreates this aesthetic as a real-time video processor, converting any input signal into a monochrome CRT terminal display with phosphor color tinting, scanline overlay, contrast adjustment, and a bold highlight mode.

The current implementation is deliberately minimal — approximately 150 LUTs of FPGA logic. It focuses on the core visual elements that define the CRT terminal look: luminance contrast scaling, bold highlight clipping, alternating-line scanline darkening, and fixed phosphor color tinting in green or amber. Several TOML-declared parameters (Brightness, Curvature, Scanline amount, Phosphor amount, Glow, and Bloom) are placeholders for future development and do not currently affect the output. The program is honest about this: what you see is contrast, bold, scanlines, color, and mix.

Terminal excels at creating vintage computer aesthetics from any video source. Feed it camera footage and it becomes a surveillance monitor. Feed it text graphics and it becomes a working terminal. Feed it abstract video synthesis and it becomes a retro oscilloscope display. The wet/dry mix fader allows blending the phosphor-tinted result with the original signal for partial colorization effects.

---

## Background

### CRT Phosphor Displays

Cathode ray tube monitors create images by sweeping an electron beam across a phosphor-coated screen. Monochrome CRTs use a single phosphor compound: P1 (green), P3 (amber/orange), or P4 (white). The phosphor's emission spectrum determines the display color. Green phosphor monitors (like the IBM 5151 or Apple II Monitor) became iconic of the early computer era. Amber monitors (like the Hercules-compatible displays) were considered easier on the eyes for extended text work. Terminal recreates these color signatures by replacing the input chrominance with fixed UV values corresponding to green or amber phosphor emission.

### Scanline Structure

An interlaced or progressive CRT display traces horizontal lines across the screen. On a real monitor, the electron beam has a Gaussian profile — brightest at centre, fading at the edges — which means there is a visible gap between adjacent lines. This gap creates the characteristic horizontal stripe pattern known as "scanlines." Terminal simulates this by reducing the brightness of every other horizontal line to 75% of its original value, creating a uniform scanline overlay across the entire image.

### Contrast and Bold Text

On a real VT100 terminal, "bold" text was rendered by increasing the beam current for those characters, making them brighter than normal text. Terminal approximates this with a simple threshold: any pixel with luminance above 384 (approximately 37% of full scale) is clipped to maximum brightness (1023). This creates a hard two-level effect for bright content — anything moderately bright becomes fully bright, simulating the high-contrast look of bold terminal text against a dim background.

### Planned Features

The TOML configuration declares parameters for Brightness offset, barrel Curvature distortion, variable Scanline depth, continuous Phosphor hue rotation, Glow bloom, and cursor overlay. These represent the roadmap for a full VT100 terminal emulation. The current VHDL implements only the core pipeline: contrast multiplication, bold clipping, scanline darkening, phosphor tinting, and wet/dry mixing. Future revisions will activate the remaining parameters as the FPGA logic budget allows.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Contrast          Y × Contrast / 1024
│   │                       (multiplication, NOT proc_amp)
│   │
│   ├─ 2. Bold              if Bold ON and Y > 384 → Y = 1023
│   │                       (hard threshold clip)
│   │
│   ├─ 3. Scanline          if Scanlines ON and odd line →
│   │                       Y = Y/2 + Y/4 = 0.75 × Y
│   │
│   └─ 4. → s_proc_y
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   └─ Phosphor Tint        Green: U=384, V=384
│                            Amber: U=384, V=640
│                            (fixed values, input chroma discarded)
│
├── Delayed Input ──────────────────────────────────────────────
│   │   (8-clock delay pipeline for bypass/mix reference)
│   │
│   └─ Y_d, U_d, V_d
│
├── Mix Stage ──────────────────────────────────────────────────
│   │
│   ├─ Y: interpolator_u(dry=Y_d, wet=proc_y, t=Mix)
│   ├─ U: interpolator_u(dry=U_d, wet=proc_u, t=Mix)
│   └─ V: interpolator_u(dry=V_d, wet=proc_v, t=Mix)
│
├── Bypass Mux ─────────────────────────────────────────────────
│   │
│   └─ Bypass=On → pass delayed input; Off → pass mixed output
│
└── Output YUV
```

The pipeline is linear and minimal. The contrast stage is a simple unsigned multiplication (Y × Contrast, taking bits [19:10] of the 20-bit product), not a standard proc_amp with centred offset. This means Contrast = 512 gives approximately half brightness, and Contrast = 1023 gives approximately unity gain. The bold stage is a hard clip, not a gain boost — any pixel above the threshold jumps to maximum, creating a binary bright/dim separation. The scanline effect is applied uniformly regardless of content, darkening every odd-numbered line to 75% brightness.

Note that Brightness (pot 1), Curvature (pot 3), Scanline amount (pot 4), Phosphor amount (pot 5), Glow (pot 6), and Bloom (toggle 10) are declared in the TOML but their register values are not used in the current VHDL processing pipeline. These parameters exist as placeholders for planned future implementation.

---

## Parameter Reference

<img src={terminal_control_panel} alt="Videomancer front panel with Terminal loaded"/>
*Videomancer's front panel with Terminal active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

Brightness offset. **Not yet implemented in the current VHDL.** The register is read and stored but does not affect the processing pipeline. In the planned implementation, this would add a DC offset to the output luminance after contrast scaling, allowing overall brightness adjustment independent of contrast. Currently has no visible effect on the output.

---

#### Knob 2 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Contrast — the only functional gain control. The input luminance is multiplied by this value: Y_out = (Y_in × Contrast) >> 10. At 0, the output is black regardless of input. At 512, the output is approximately half the input brightness. At 1023, the output is near unity gain. This is a simple multiplication, not a centred proc_amp — there is no midpoint offset, so contrast adjustment also shifts the overall brightness level.

---

#### Knob 3 — Curvature
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Curvature — barrel distortion amount. **Not yet implemented in the current VHDL.** The register is declared but unused. In the planned implementation, this would apply barrel lens distortion to simulate the curved glass of a CRT monitor, with the image bowing outward at the edges. Currently has no visible effect on the output.

---

#### Knob 4 — Scanline
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scanline depth — variable scanline intensity. **Not yet implemented in the current VHDL.** The register is declared but unused. The scanline effect is currently controlled only by the Scanlines toggle (on/off), with a fixed darkening ratio of 75%. In the planned implementation, this control would allow continuous adjustment of the scanline depth from subtle to extreme.

---

#### Knob 5 — Phosphor
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Phosphor — phosphor color intensity or hue angle. **Not yet implemented in the current VHDL.** The register is declared but unused. The phosphor tint is currently controlled only by the Color toggle (Green or Amber), with fixed UV values. In the planned implementation, this would allow continuous hue rotation through the phosphor color space, providing access to white, blue, and intermediate tints.

---

#### Knob 6 — Glow
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Glow — bloom/glow radius or intensity. **Not yet implemented in the current VHDL.** The register is declared but unused. In the planned implementation, this would control a soft glow effect around bright pixels, simulating the phosphor bloom visible on overdriven CRT displays.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color** | Green | Amber |
| **8 — Bold** | Off | On |
| **9 — Scanlines** | Off | On |
| **10 — Bloom** | Off | On |
| **11 — Bypass** | Off | On |

Five binary switches controlling processing stages. Of these, Color, Bold, Scanlines, and Bypass are fully functional in the current VHDL. Bloom is declared but not connected to the processing pipeline. All toggles share register 6 using the standard bit-packing scheme (bit 0 through bit 4).

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix ratio via three parallel interpolator_u instances (one each for Y, U, V). At 0%, the output is the delayed dry input signal (unprocessed). At 100%, the output is the fully processed terminal signal (contrast, bold, scanlines, phosphor tint). Intermediate values blend between the two, allowing partial phosphor colorization — useful for creating tinted overlays where the original color partially shows through the monochrome phosphor.

---

## Guided Exercises

These exercises demonstrate Terminal's current capabilities and work within the constraints of the minimal implementation. Each focuses on the functional parameters, building from basic contrast adjustment through CRT emulation to creative misuse of the processing chain.

### Exercise 1: Classic Green Screen

<img src={terminal_exercise1_result} alt="Classic Green Screen result"/>
*Classic Green Screen — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and moderate contrast.

**Objective**: Create a convincing vintage green phosphor CRT display using contrast, scanlines, and phosphor tinting.

1. **Set the color**: Ensure Color (Switch 7) is set to Green.
2. **Enable scanlines**: Turn on Scanlines (Switch 9). Every other horizontal line should darken visibly.
3. **Adjust contrast**: Set Contrast to ~50% for a balanced green screen look. Higher values create a brighter, more washed-out display; lower values create a dim, atmospheric monitor.
4. **Full mix**: Set Mix to 100% so the phosphor tint fully replaces the original colors.
5. **Compare**: Toggle Bypass to see the original signal for A/B comparison.
6. **Bold option**: Enable Bold (Switch 8) to create a high-contrast binary look where bright subjects snap to full brightness.

**Key concepts**: Phosphor tint replaces chroma with fixed UV values. Scanlines darken every odd line to 75%. Contrast multiplies input luminance. Bold clips highlights above threshold.

---

### Exercise 2: Amber Bold Terminal

<img src={terminal_exercise2_result} alt="Amber Bold Terminal result"/>
*Amber Bold Terminal — simulated result across source images.*
**Source**: Text graphics, title cards, or high-contrast black-and-white footage.

**Objective**: Create a high-contrast amber terminal display with bold highlight clipping for a classic text-mode look.

1. **Switch to amber**: Set Color to Amber. The display should shift from cool green to warm orange.
2. **Enable bold**: Turn on Bold (Switch 8). Bright text elements should snap to maximum brightness.
3. **Increase contrast**: Push Contrast to ~70% to ensure the bold threshold (384) catches most text-brightness pixels.
4. **Scanlines on**: Enable Scanlines for the full CRT effect.
5. **Feed text**: If possible, route text graphics or a title card as input. The bold clipping makes text pop sharply against the dark background.
6. **Lower contrast**: Drop Contrast to ~30% and observe how fewer pixels reach the bold threshold. The binary separation point shifts with contrast.

**Key concepts**: Bold clips all pixels above 384 to maximum brightness. Amber tint uses U=384, V=640. Contrast scaling happens before bold, so it determines which pixels reach the clip threshold.

---

### Exercise 3: Phosphor Tint Overlay

<img src={terminal_exercise3_result} alt="Phosphor Tint Overlay result"/>
*Phosphor Tint Overlay — simulated result across source images.*
**Source**: Colorful footage — landscapes, graphics, or abstract video synthesis.

**Objective**: Use the Mix fader to blend the phosphor-tinted monochrome with the original color signal, creating a vintage color grading effect.

1. **Full process first**: Set Color to Green, Scanlines On, Contrast ~50%, Mix 100%. Observe the fully monochrome green result.
2. **Blend in color**: Slowly lower Mix from 100% toward 50%. The original colors begin to show through the green phosphor tint.
3. **Subtle tint**: At Mix ~30%, the image retains most of its original color but with a green cast and visible scanlines blended in.
4. **Try amber**: Switch Color to Amber and repeat the blend. The warm amber wash creates a sepia-like vintage color grade.
5. **No scanlines**: Disable Scanlines to create a pure phosphor color tint without the CRT stripe texture.
6. **Bold accents**: With Mix at ~50%, enable Bold. Bright areas snap to full monochrome phosphor while dim areas retain partial original color.

**Key concepts**: The interpolator_u mix stage blends processed and dry signals. Partial mix creates a color overlay/tint effect. Scanlines and bold interact with the mix — they only affect the wet signal.

---


## Tips

- **Contrast is the primary brightness control**: Since Brightness (pot 1) is not yet implemented, use Contrast to control overall luminance. Higher contrast = brighter image.
- **Bold creates binary separation**: With bold enabled, the image has only two effective brightness levels — below the threshold (dim) and above (maximum). This is most effective with text or high-contrast graphics.
- **Mix for color grading**: At partial Mix values (30–70%), Terminal functions as a color grading tool, adding a phosphor tint wash over the original colors without going fully monochrome.
- **Scanlines scale with resolution**: At 1080p, scanlines are subtle single-pixel lines. At 480i, they are proportionally much more prominent. The visual impact depends on the output resolution.
- **Non-functional knobs are safe**: Turning the Brightness, Curvature, Scanline, Phosphor, or Glow knobs will not cause glitches or unexpected behaviour — the values are simply read and ignored.
- **Green vs. Amber is the only color choice**: Until the Phosphor continuous control is implemented, the color palette is limited to these two presets. For white phosphor emulation, set Color to Green and increase Contrast past unity.
- **Feedback for retro CRT loops**: Route Terminal's output back to its input for recursive phosphor tinting and scanline accumulation. Each pass deepens the green/amber wash and doubles the scanline density.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bold** | In terminal emulation, a text attribute that increases beam current (brightness) for emphasis; here approximated by a hard luminance threshold clip. |
| **CRT** | Cathode Ray Tube; a display technology that creates images by sweeping an electron beam across a phosphor-coated glass screen. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **LUT** | Look-Up Table; the basic logic element in an FPGA, used here as a measure of implementation complexity (~150 LUTs total). |
| **Mix** | The wet/dry blend ratio controlling how much of the processed (wet) signal versus the original (dry) signal appears in the output. |
| **Phosphor** | A fluorescent coating on the inside of a CRT screen that emits light when struck by the electron beam; the compound determines the display color. |
| **Scanline** | A single horizontal line traced by the electron beam; the visible gap between lines on a CRT creates the characteristic stripe texture. |
| **VT100** | A 1978 DEC video terminal that became the de facto standard for text-mode terminal emulation; target aesthetic for this program. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
