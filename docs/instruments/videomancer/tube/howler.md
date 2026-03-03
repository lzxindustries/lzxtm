---
draft: true
sidebar_position: 139
slug: /instruments/videomancer/howler
title: "Howler"
image: /img/instruments/videomancer/howler/howler_hero_s1.png
description: "Howler implements a video feedback loop entirely within the FPGA — no external routing required."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import howler_source1_skull from '/img/instruments/videomancer/howler/howler_source1_skull.png';
import howler_source2_fruit from '/img/instruments/videomancer/howler/howler_source2_fruit.png';
import howler_source3_clouds from '/img/instruments/videomancer/howler/howler_source3_clouds.png';
import howler_source4_pattern from '/img/instruments/videomancer/howler/howler_source4_pattern.png';
import howler_source5_man from '/img/instruments/videomancer/howler/howler_source5_man.png';
import howler_source6_knit from '/img/instruments/videomancer/howler/howler_source6_knit.png';
import howler_hero_s1 from '/img/instruments/videomancer/howler/howler_hero_s1.png';
import howler_hero_s2 from '/img/instruments/videomancer/howler/howler_hero_s2.png';
import howler_hero_s3 from '/img/instruments/videomancer/howler/howler_hero_s3.png';
import howler_hero_s4 from '/img/instruments/videomancer/howler/howler_hero_s4.png';
import howler_hero_s5 from '/img/instruments/videomancer/howler/howler_hero_s5.png';
import howler_hero_s6 from '/img/instruments/videomancer/howler/howler_hero_s6.png';
import howler_ex1_s1 from '/img/instruments/videomancer/howler/howler_ex1_s1.png';
import howler_ex1_s2 from '/img/instruments/videomancer/howler/howler_ex1_s2.png';
import howler_ex1_s3 from '/img/instruments/videomancer/howler/howler_ex1_s3.png';
import howler_ex1_s4 from '/img/instruments/videomancer/howler/howler_ex1_s4.png';
import howler_ex1_s5 from '/img/instruments/videomancer/howler/howler_ex1_s5.png';
import howler_ex1_s6 from '/img/instruments/videomancer/howler/howler_ex1_s6.png';
import howler_ex2_s1 from '/img/instruments/videomancer/howler/howler_ex2_s1.png';
import howler_ex2_s2 from '/img/instruments/videomancer/howler/howler_ex2_s2.png';
import howler_ex2_s3 from '/img/instruments/videomancer/howler/howler_ex2_s3.png';
import howler_ex2_s4 from '/img/instruments/videomancer/howler/howler_ex2_s4.png';
import howler_ex2_s5 from '/img/instruments/videomancer/howler/howler_ex2_s5.png';
import howler_ex2_s6 from '/img/instruments/videomancer/howler/howler_ex2_s6.png';
import howler_ex3_s1 from '/img/instruments/videomancer/howler/howler_ex3_s1.png';
import howler_ex3_s2 from '/img/instruments/videomancer/howler/howler_ex3_s2.png';
import howler_ex3_s3 from '/img/instruments/videomancer/howler/howler_ex3_s3.png';
import howler_ex3_s4 from '/img/instruments/videomancer/howler/howler_ex3_s4.png';
import howler_ex3_s5 from '/img/instruments/videomancer/howler/howler_ex3_s5.png';
import howler_ex3_s6 from '/img/instruments/videomancer/howler/howler_ex3_s6.png';

# Howler

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: howler_source1_skull, after: howler_hero_s1 },
    { label: "Fruit", before: howler_source2_fruit, after: howler_hero_s2 },
    { label: "Clouds", before: howler_source3_clouds, after: howler_hero_s3 },
    { label: "Pattern", before: howler_source4_pattern, after: howler_hero_s4 },
    { label: "Man", before: howler_source5_man, after: howler_hero_s5 },
    { label: "Knit", before: howler_source6_knit, after: howler_hero_s6 },
  ]}
/>
*Howler generating recursive tunnel patterns by feeding zoomed, decayed, and hue-rotated video back through its scanline buffer.*

---

## Overview

Howler implements a video feedback loop entirely within the FPGA — no external routing required. Each scanline is read back from a persistent BRAM buffer at a zoomed address, blended with the incoming video, hue-rotated in the UV color plane, and written back. Over successive frames, this creates self-similar recursive structures that bloom outward or tunnel inward, shift in hue, and evolve organically. The program chains six processing stages in a single-clock pipeline: input capture, BRAM read at a zoomed address, decay multiplication, signal accumulation, Givens-approximation hue rotation, and brightness scaling with soft clipping.

The name references the **howl-round** — a technique pioneered by the BBC Radiophonic Workshop in which a television camera was pointed at its own monitor, creating recursive visual feedback. The original *Doctor Who* title sequence (1963) was produced this way: a camera filmed its own output, zoomed slightly, with the resulting fractal tunnel emerging from pure optical feedback. Howler digitizes this process. Instead of a camera and a monitor, three BRAMs serve as the persistent canvas, and the zoom knob replaces the camera's physical distance from the screen.

At conservative settings — low zoom offset, moderate decay, gentle hue drift — Howler adds a soft trailing echo to the input. At extreme settings — high zoom, near-unity decay, strong color drift — it overwhelms the source entirely, producing churning psychedelic tunnels, kaleidoscopic color fields, and self-exciting patterns that emerge from nothing but LFSR noise.

---

## Background

### The Howl-Round Technique

In the 1960s, BBC engineers discovered that pointing a studio camera at its own monitor produced complex, self-organizing visual patterns. The image fed back through the system with a one-frame delay, and any zoom, rotation, or brightness change in the camera path would compound across iterations. The effect was called a **howl-round** — by analogy with audio feedback (the howl of a microphone pointed at its speaker). Delia Derbyshire and the Radiophonic Workshop used howl-round to create the original *Doctor Who* opening titles: a camera zooming into its own monitor output produced the iconic spiraling tunnel. Howler recreates this process digitally, using BRAM storage in place of the camera-monitor loop and register-controlled parameters in place of physical camera adjustments.

### IIR Feedback and Decay

Howler's feedback loop is an **Infinite Impulse Response (IIR)** system. Each output pixel is a weighted sum of the current input and the previous output read from memory. The Decay control sets the feedback coefficient: how much of the old signal is retained. When decay is low, the image fades quickly — only a few frames of history are visible. When decay is near maximum (near 1.0×), the image persists almost indefinitely, and new input barely overwrites the accumulated pattern. This is the digital equivalent of adjusting the monitor persistence or phosphor decay in the original howl-round setup. The system is inherently nonlinear because of the clipping applied at each iteration — accumulated values are clamped to the 10-bit range, preventing overflow but creating soft saturation boundaries.

### Zoom as Spatial Feedback Transform

In the original howl-round, the zoom effect came from the camera's physical proximity to the monitor — moving closer magnified the feedback, creating an expanding tunnel. Howler replaces this with an address transform on the BRAM read. Instead of reading pixel N from position N, it reads from a position offset from the horizontal center and scaled by a zoom factor. The zoom factor is a 1.10 fixed-point number ranging from 0.5× to 1.5×, computed from the Zoom knob and polarity toggle. Zoom factors less than 1.0× compress the feedback toward the center (inward tunnel), while factors greater than 1.0× expand it outward (blooming). This address transform is applied on every read, so the spatial distortion compounds across frames.

### Givens Rotation for Hue Drift

Howler shifts the hue of the feedback signal using a **Givens rotation** — a small-angle approximation of a 2D rotation matrix applied to the U and V chrominance components. The rotation formula is: U' = U − V × k/512, V' = V + U × k/512, where k is derived from the Color Drift knob. This approximation is valid for small angles and avoids the need for sine/cosine lookup tables. Over many feedback iterations, the small rotation compounds into large hue shifts, causing the color of the feedback pattern to cycle continuously through the color wheel. The Drift Direction toggle reverses the sign of k, switching between clockwise and counterclockwise rotation. The Channel Lock toggle controls whether U and V rotate together (locked) or with opposite signs on V (independent), producing different color evolution patterns.

### LFSR Self-Excitation

When the Self-Excite toggle is enabled, the input injection source switches from the incoming video to pseudo-random noise generated by two 16-bit **Linear Feedback Shift Registers (LFSRs)**, seeded with 0xCAFE and 0xFADE. This creates feedback patterns that emerge from noise alone — no external signal required. The LFSR outputs provide three noise channels (Y from LFSR-A bits 9:0, U from LFSR-B bits 9:0, V from LFSR-A bits 15:6) that evolve at clock rate. Combined with the zoom and hue rotation, self-excitation produces continuously evolving abstract patterns reminiscent of cellular automata or reaction-diffusion systems.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Input Selection ────────────────────────────────────────────
│   ├─ Self-Excite Off → use input Y/U/V
│   └─ Self-Excite On  → use LFSR noise (seeds 0xCAFE, 0xFADE)
│
├── BRAM Feedback Loop (3× 10-bit × 1024, Y/U/V) ─────────────
│   │
│   ├─ 1. Input capture + parameter latch
│   ├─ 2. BRAM read at zoomed address:
│   │      addr = (h_count − 512) × zoom_factor / 1024 + 512 + h_shift
│   │      zoom_factor = 0.5× to 1.5× (1.10 fixed-point)
│   ├─ 3. Decay multiply: feedback × decay_factor >> 10
│   ├─ 4. Accumulate: saturating add (decayed feedback + scaled input)
│   ├─ 5. Color drift: Givens rotation on U/V
│   │      U' = U − V×k/512,  V' = V + U×k/512
│   │      Channel Lock → both same direction
│   │      Independent → V gets inverse rotation
│   ├─ 6. Brightness: (Y × brightness_reg) >> 9, soft clip
│   │      Write-back to BRAM uses pre-brightness accumulated data
│   └─ 7. BRAM write (disabled when Freeze is On)
│
├── Interpolator Mix ───────────────────────────────────────────
│   └─ 3× interpolator_u: crossfade between delayed input and pipeline output
│
├── Sync / Data Delay (7 clocks) ───────────────────────────────
│   └─ Shift registers for hsync, vsync, field, Y, U, V
│
└── Output Assignment ──────────────────────────────────────────
    └─ Always outputs mix result (no bypass mux)
```

The critical detail is what gets written back to BRAM. The write-back data is the post-drift, pre-brightness accumulated signal — not the final output. This means the feedback loop operates on the raw accumulation with hue rotation, and brightness is purely a display scaling applied after the loop. This prevents the brightness control from compounding across iterations. The zoom address computation centers on pixel 512 (horizontal midpoint), so expansion and contraction radiate from the center of the scanline. The H Shift accumulator adds a per-frame horizontal drift that wraps the read address, creating a scrolling effect in the feedback pattern. Notably, there is no bypass mux — the output always passes through the interpolator. Toggle 11 (Freeze) disables BRAM writes, holding the current buffer contents static, but the output continues to be processed.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Zoom
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 12.6% |
| Suffix | % |

Controls the spatial scaling of the feedback read address. The register value maps to a 1.10 fixed-point zoom factor ranging from 0.5× (register 0) to 1.5× (register 1023), centered on horizontal pixel 512. At 0.5× the feedback is compressed toward the center, creating an inward-tunneling effect. At 1.5× the feedback expands outward from the center in a blooming pattern. The Zoom Polarity toggle (Toggle 7) inverts the mapping, swapping expand and contract behavior. The default register value of 576 places the zoom slightly above unity, producing a gentle outward expansion.

---

#### Knob 2 — Decay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the persistence of the feedback loop — how much of the previous frame's buffer content is retained. The decay register scales the BRAM readback by `feedback × decay / 1024`. At 0%, feedback is completely suppressed and the output follows the input with no trailing. At 100%, decay is near-unity and the feedback persists almost indefinitely. High decay values are essential for building up the recursive structures that define Howler's visual character. The interaction with Inject (Knob 3) determines the balance between old and new — high decay with low inject creates slow-evolving, deeply layered patterns.

---

#### Knob 3 — Inject
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls how strongly the input signal (or LFSR noise in Self-Excite mode) is injected into the feedback accumulator. The input is scaled by `input × inject / 1024` before being added to the decayed feedback. At 0%, no new signal enters the loop and the feedback decays to black (or freezes if Decay is high). At 100%, the input dominates and feedback patterns are quickly overwritten. The sweet spot for visible feedback effects is typically 30–60%, where the input is strong enough to seed patterns but the feedback accumulation remains visible.

---

#### Knob 4 — Color Drift
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the rate of hue rotation applied to the feedback signal at each iteration. The Color Drift register is centered at 512 (no rotation) and produces a signed rotation coefficient `k = register − 512` applied as a Givens approximation in the UV plane. Small values near center produce gentle, slow-cycling color shifts over many frames. Values near the extremes (0 or 1023) produce rapid hue cycling where colors change noticeably on every frame. The Drift Direction toggle (Toggle 8) reverses the sign of k, switching between clockwise and counterclockwise rotation through the color wheel.

---

#### Knob 5 — H Shift
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls a per-frame horizontal drift in the feedback read address. The H Shift register is accumulated into a 16-bit counter on each vsync, and the upper 10 bits of the accumulator are added to the read address. At 0% the feedback reads back from the same horizontal position each frame. As the value increases, the feedback pattern scrolls horizontally — new feedback is read from a shifted position, creating a lateral motion in the tunnel or bloom structure. High values produce rapid horizontal scrolling that can tear the feedback pattern apart into flowing streams.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the output gain applied to the luminance channel after the feedback loop. The brightness register scales the accumulated Y value by `Y × brightness / 512`. At register 512 (default, ~50%), the gain is unity. Below 512 the output is dimmed; above 512 it is brightened with soft clipping at 1023. Crucially, brightness is applied *after* the BRAM write-back — the feedback loop operates on the raw accumulated signal, not the brightness-scaled output. This prevents gain from compounding across iterations.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Zoom Polar** | Expand | Contract |
| **8 — Drift Dir** | CW | CCW |
| **9 — Self-Excite** | Off | On |
| **10 — Channel Lock** | Indep | Locked |
| **11 — Freeze** | Off | On |

The five toggles control independent binary options with no combined mode selection. Zoom Polarity (Toggle 7) and Drift Direction (Toggle 8) are directional modifiers for their respective knobs. Self-Excite (Toggle 9) fundamentally changes the input source. Channel Lock (Toggle 10) alters the hue rotation behavior. Freeze (Toggle 11) is *not* a bypass — it holds the BRAM contents static but continues to output the processed signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the delayed input signal and the feedback pipeline output via three `interpolator_u` instances (one per Y/U/V channel). At 0% the output matches the delayed input and no feedback is visible. At 100% the output is fully the feedback pipeline signal. Note that there is no bypass mux in Howler — even when Mix is at 0%, the feedback loop continues running internally; only the output blend changes.

---

## Guided Exercises

These exercises progress from gentle trailing effects to full self-exciting feedback tunnels, building understanding of how zoom, decay, injection, and hue drift interact to create recursive visual structures.

### Exercise 1: Basic Feedback Echo

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: howler_source1_skull, after: howler_ex1_s1 },
    { label: "Fruit", before: howler_source2_fruit, after: howler_ex1_s2 },
    { label: "Clouds", before: howler_source3_clouds, after: howler_ex1_s3 },
    { label: "Pattern", before: howler_source4_pattern, after: howler_ex1_s4 },
    { label: "Man", before: howler_source5_man, after: howler_ex1_s5 },
    { label: "Knit", before: howler_source6_knit, after: howler_ex1_s6 },
  ]}
/>
*Basic Feedback Echo — simulated result across source images.*
**Source**: A live camera feed or recorded footage with slow, deliberate motion — a hand moving across frame, or a slowly rotating object.

**Objective**: Understand the basic feedback loop: how decay and inject control the persistence and intensity of the trailing echo.

1. **Visible trail**: With default settings, observe the subtle trailing behind moving objects. The feedback creates a fading echo of the input.
2. **Increase decay**: Slowly turn Decay from 75% toward 100%. The trailing becomes longer and more persistent — old frames linger visibly behind the current input.
3. **Reduce inject**: Lower Inject to ~30%. The current input becomes weaker relative to the accumulated feedback. Old patterns persist longer.
4. **Balance point**: Find the point where Decay and Inject create a stable, visible trail without overwhelming the input. This is Howler's basic echo mode.
5. **Decay at zero**: Turn Decay to 0%. The feedback vanishes entirely and the output follows the input clean. This confirms that the feedback loop is driven purely by the decay multiplier.

**Key concepts**: IIR feedback loop, decay as persistence control, inject as input strength, feedback-to-input ratio determines visual character

---

### Exercise 2: Tunnel and Bloom

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: howler_source1_skull, after: howler_ex2_s1 },
    { label: "Fruit", before: howler_source2_fruit, after: howler_ex2_s2 },
    { label: "Clouds", before: howler_source3_clouds, after: howler_ex2_s3 },
    { label: "Pattern", before: howler_source4_pattern, after: howler_ex2_s4 },
    { label: "Man", before: howler_source5_man, after: howler_ex2_s5 },
    { label: "Knit", before: howler_source6_knit, after: howler_ex2_s6 },
  ]}
/>
*Tunnel and Bloom — simulated result across source images.*
**Source**: High-contrast footage — bright shapes on a dark background, or a graphic pattern from another Videomancer program (e.g., Honeycomb or Checkers).

**Objective**: Explore how zoom polarity creates tunneling and blooming effects, and how hue drift adds color evolution to the recursive structure.

1. **Tunnel inward**: Set Zoom Polarity to Contract and Zoom to ~40%. With high Decay (~90%), the feedback pulls inward from the edges, creating a tunneling spiral that converges at the center of the screen.
2. **Bloom outward**: Switch Zoom Polarity to Expand. The same settings now push the feedback outward — the image blooms from the center toward the edges.
3. **Add hue drift**: Increase Color Drift to ~30%. Watch the colors shift with each feedback iteration — the tunnel or bloom develops a rainbow spiral as hue rotates through the color wheel.
4. **Drift direction**: Toggle Drift Direction between CW and CCW. The color rotation reverses — warm colors become cool and vice versa.
5. **Channel Lock**: Switch Channel Lock to Independent (Indep). The UV rotation changes character — instead of a smooth hue wheel, complementary color pairs emerge in the feedback pattern.

**Key concepts**: Zoom-centered address transform, expand vs. contract polarity, Givens hue rotation, compound hue shift across iterations, channel lock vs. independent UV rotation

---

### Exercise 3: Self-Exciting Psychedelia

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: howler_source1_skull, after: howler_ex3_s1 },
    { label: "Fruit", before: howler_source2_fruit, after: howler_ex3_s2 },
    { label: "Clouds", before: howler_source3_clouds, after: howler_ex3_s3 },
    { label: "Pattern", before: howler_source4_pattern, after: howler_ex3_s4 },
    { label: "Man", before: howler_source5_man, after: howler_ex3_s5 },
    { label: "Knit", before: howler_source6_knit, after: howler_ex3_s6 },
  ]}
/>
*Self-Exciting Psychedelia — simulated result across source images.*
**Source**: No external source needed — Self-Excite provides the input.

**Objective**: Generate fully autonomous feedback patterns using LFSR noise as the injection source, combining all parameters for maximum visual complexity.

1. **Enable Self-Excite**: Toggle Self-Excite On. The input switches from video to LFSR noise. With high Decay and moderate Inject, noise seeds begin accumulating into structured patterns.
2. **Strong zoom**: Set Zoom to ~70% in Expand mode. The noise structures bloom outward, creating radial patterns that emerge from the center.
3. **Maximum hue drift**: Set Color Drift to ~80%. Colors cycle rapidly through the feedback, producing a psychedelic rainbow spiral.
4. **H Shift motion**: Increase H Shift to ~30%. The feedback pattern begins scrolling horizontally, adding lateral motion to the radial zoom structure.
5. **Freeze capture**: Toggle Freeze On to capture a particularly interesting moment. Observe how the frozen pattern continues to decay and hue-shift (since reads continue) but no new data is written. Toggle Freeze Off to resume.
6. **Brightness boost**: Increase Brightness above 50% to drive the soft clipper. The increased gain creates saturated, high-contrast feedback structures.

**Key concepts**: LFSR noise as autonomous seed, self-organizing feedback structures, horizontal drift accumulator, freeze as buffer hold (not bypass), brightness as post-loop gain

---


## Tips

- **Decay is the master control**: Decay determines whether Howler adds a subtle trail or becomes a full recursive feedback engine. Start with Decay and adjust everything else relative to it.
- **Brightness is display-only**: Because brightness is applied after the BRAM write-back, it does not affect feedback behavior. You can push brightness to maximum for vivid output without changing the feedback loop dynamics.
- **Freeze is not bypass**: Toggle 11 stops BRAM writes but the read path and entire processing pipeline remain active. The frozen pattern continues to decay and hue-shift. There is no bypass mux in Howler.
- **Self-Excite for autonomous patterns**: LFSR noise with high decay creates self-organizing structures without any external input. Pair with strong zoom and hue drift for maximum visual complexity.
- **H Shift adds lateral motion**: Even modest H Shift values create continuous horizontal scrolling in the feedback. Combined with zoom, this produces spiral or helical motion paths.
- **Feedback routing**: Connect Howler's output back to its own input externally for a double feedback loop. The internal loop provides spatial zoom; the external loop adds frame-scale recursion.
- **Channel Lock for color control**: Locked mode produces smooth rainbow cycling. Independent mode produces chromatic contrast with complementary pairs. Try both with the same Color Drift value and compare.
- **Start from the original**: The BBC howl-round technique gives the clearest results with high-contrast graphic input — color bars, text generators, or other Videomancer programs work better than camera feeds for initial exploration.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory within the FPGA fabric. Howler uses three BRAMs (one per Y/U/V) as the persistent feedback canvas. |
| **BT.601** | ITU-R Recommendation BT.601; the standard color matrix for YUV-to-RGB conversion in standard-definition video. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Decay** | The feedback persistence coefficient. Multiplies the BRAM readback by a factor between 0 (no persistence) and ~1.0 (indefinite persistence). |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable chip that executes the feedback pipeline. |
| **Givens rotation** | A 2D rotation applied to two components (here U and V) by a small-angle approximation: U' = U − Vk/512, V' = V + Uk/512. |
| **Howl-round** | A visual feedback technique where a camera films its own output, first used by the BBC Radiophonic Workshop. |
| **IIR** | Infinite Impulse Response; a feedback system where each output depends on both current input and previous outputs. |
| **Interpolator** | A linear crossfade module (`interpolator_u`) used for the wet/dry output mix. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used here to seed the feedback loop in Self-Excite mode. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next on each clock cycle. Howler has a 7-clock pipeline plus 4-clock interpolators. |
| **Soft clip** | Saturating arithmetic that clamps values to the valid range (0–1023) rather than wrapping on overflow. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
