---
draft: true
sidebar_position: 226
slug: /instruments/videomancer/phosphor
title: "Phosphor"
image: /img/instruments/videomancer/phosphor/phosphor_hero_s1.png
description: "Phosphor recreates the look of analogue CRT monitors — the faint glow bleeding rightward from bright edges, the dark scanline gaps between rows, and the characteristic colour of a phosphor screen."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import phosphor_control_panel from '/img/instruments/videomancer/phosphor/phosphor_control_panel.png';
import phosphor_source1_runner from '/img/instruments/videomancer/phosphor/phosphor_source1_runner.png';
import phosphor_source2_car from '/img/instruments/videomancer/phosphor/phosphor_source2_car.png';
import phosphor_source3_turtle from '/img/instruments/videomancer/phosphor/phosphor_source3_turtle.png';
import phosphor_source4_pattern from '/img/instruments/videomancer/phosphor/phosphor_source4_pattern.png';
import phosphor_source5_woman from '/img/instruments/videomancer/phosphor/phosphor_source5_woman.png';
import phosphor_source6_berries from '/img/instruments/videomancer/phosphor/phosphor_source6_berries.png';
import phosphor_hero_s1 from '/img/instruments/videomancer/phosphor/phosphor_hero_s1.png';
import phosphor_hero_s2 from '/img/instruments/videomancer/phosphor/phosphor_hero_s2.png';
import phosphor_hero_s3 from '/img/instruments/videomancer/phosphor/phosphor_hero_s3.png';
import phosphor_hero_s4 from '/img/instruments/videomancer/phosphor/phosphor_hero_s4.png';
import phosphor_hero_s5 from '/img/instruments/videomancer/phosphor/phosphor_hero_s5.png';
import phosphor_hero_s6 from '/img/instruments/videomancer/phosphor/phosphor_hero_s6.png';
import phosphor_ex1_s1 from '/img/instruments/videomancer/phosphor/phosphor_ex1_s1.png';
import phosphor_ex1_s2 from '/img/instruments/videomancer/phosphor/phosphor_ex1_s2.png';
import phosphor_ex1_s3 from '/img/instruments/videomancer/phosphor/phosphor_ex1_s3.png';
import phosphor_ex1_s4 from '/img/instruments/videomancer/phosphor/phosphor_ex1_s4.png';
import phosphor_ex1_s5 from '/img/instruments/videomancer/phosphor/phosphor_ex1_s5.png';
import phosphor_ex1_s6 from '/img/instruments/videomancer/phosphor/phosphor_ex1_s6.png';
import phosphor_ex2_s1 from '/img/instruments/videomancer/phosphor/phosphor_ex2_s1.png';
import phosphor_ex2_s2 from '/img/instruments/videomancer/phosphor/phosphor_ex2_s2.png';
import phosphor_ex2_s3 from '/img/instruments/videomancer/phosphor/phosphor_ex2_s3.png';
import phosphor_ex2_s4 from '/img/instruments/videomancer/phosphor/phosphor_ex2_s4.png';
import phosphor_ex2_s5 from '/img/instruments/videomancer/phosphor/phosphor_ex2_s5.png';
import phosphor_ex2_s6 from '/img/instruments/videomancer/phosphor/phosphor_ex2_s6.png';
import phosphor_ex3_s1 from '/img/instruments/videomancer/phosphor/phosphor_ex3_s1.png';
import phosphor_ex3_s2 from '/img/instruments/videomancer/phosphor/phosphor_ex3_s2.png';
import phosphor_ex3_s3 from '/img/instruments/videomancer/phosphor/phosphor_ex3_s3.png';
import phosphor_ex3_s4 from '/img/instruments/videomancer/phosphor/phosphor_ex3_s4.png';
import phosphor_ex3_s5 from '/img/instruments/videomancer/phosphor/phosphor_ex3_s5.png';
import phosphor_ex3_s6 from '/img/instruments/videomancer/phosphor/phosphor_ex3_s6.png';

# Phosphor

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: phosphor_source1_runner, after: phosphor_hero_s1 },
    { label: "Car", before: phosphor_source2_car, after: phosphor_hero_s2 },
    { label: "Turtle", before: phosphor_source3_turtle, after: phosphor_hero_s3 },
    { label: "Pattern", before: phosphor_source4_pattern, after: phosphor_hero_s4 },
    { label: "Woman", before: phosphor_source5_woman, after: phosphor_hero_s5 },
    { label: "Berries", before: phosphor_source6_berries, after: phosphor_hero_s6 },
  ]}
/>
*Phosphor simulating a P1 green CRT monitor with visible scanlines, horizontal bloom, and edge vignette applied to a live video input.*

---

## Overview

Phosphor recreates the look of analogue CRT monitors — the faint glow bleeding rightward from bright edges, the dark scanline gaps between rows, and the characteristic colour of a phosphor screen. It is a processing program: it takes an incoming video signal and reshapes it to look as though it is being displayed on a vintage monitor.

The name refers to the phosphor coating on the inside of a cathode-ray tube. When an electron beam strikes the phosphor, it glows briefly in a colour determined by the chemical compound: P1 (zinc silicate) glows green, P4 (white) is the standard television phosphor, P7 (yellow–green) has a long-persistence afterglow used in radar displays, and P31 (zinc sulfide) is the bluish short-persistence type preferred for oscilloscopes. Phosphor provides eight phosphor presets covering these classic compounds, plus a Custom mode that lets you dial in any hue.

At subtle settings Phosphor adds a gentle CRT warmth — faint scanlines, a touch of green tint. Pushed hard, it becomes a full-on retro monitor: thick scanline bars, heavy rightward bloom glow, deep vignette shadows, and binary-clipped vector-display graphics. The Hi Contrast mode clamps the signal to 1-bit, recreating the look of a vector arcade game or oscilloscope trace.

---

## Quick Start

1. **Contrast is the master control**: At 0% everything is black regardless of other settings. Start with Contrast around 50% and adjust from there.
2. **Bloom is directional**: The glow only spreads rightward because the IIR processes pixels left to right. Bright features on the left edge of the screen create long tails; features on the right have nowhere to bloom.
3. **Scanlines need sufficient contrast**: If the image is too dim (low Contrast × low Brightness), the scanline darkening is not visible because the dark and light lines are both near black.

---

## Background

### CRT Phosphor Persistence

When energised by an electron beam, phosphor crystals emit light for a brief period after the beam moves on. Different compounds have different decay times: P4 (standard TV) decays in microseconds, while P7 (radar) can persist for seconds, leaving ghostly afterimages. Phosphor's simulation does not model temporal decay (that would require frame-to-frame memory), but the bloom effect approximates the spatial glow that results from persistence — bright pixels bleed into their neighbours, mimicking the halo seen on high-brightness CRT displays.

### Scanline Structure

An analogue CRT paints the image one line at a time. Between each active scanline, the beam retraces, leaving a thin dark gap. On low-resolution monitors, these gaps are clearly visible — they are the "scanlines" that define the CRT aesthetic. Phosphor simulates this by darkening alternate scanlines (or every third, in Triple mode). The darkening amount is adjustable: at 0% all lines are equally bright, at 100% the dark lines are completely black.

### Bloom and Halation

When very bright areas of a CRT screen excite the phosphor beyond its linear range, the glow spreads outward — a phenomenon called **bloom** or **halation**. On a real tube, this is an optical effect: the glass faceplate scatters light from overdriven phosphor elements. Phosphor simulates bloom using a horizontal IIR (infinite impulse response) filter: each pixel's brightness is mixed with the accumulated brightness of all preceding pixels on the same line. The IIR coefficient is controlled by the Bloom knob, producing four levels of spread from none to a heavy rightward glow trail.

### Vignette

CRT displays are naturally dimmer at the edges than the centre — the electron beam arrives at oblique angles and the phosphor coating thins near the glass corners. Phosphor models this with a simple edge-darkening vignette: pixels within the first and last 80 columns are progressively dimmed in three steps (25%, 50%, and 87.5% of full brightness). This creates a soft light falloff at the horizontal edges.

### Vector Display Mode

Early arcade games and oscilloscope displays used CRT tubes driven in "vector" mode — the beam traces lines rather than raster-scanning. The visual result is pure black-and-white with no grey tones. Phosphor's Hi Contrast toggle replicates this by clamping the signal to 1-bit: any pixel brighter than mid-grey becomes full white, everything else becomes black. Combined with a green or amber phosphor tint and heavy bloom, this creates an authentic vector-game look.


---

## Signal Flow

Y Channel → U/V Channels → Sync Signals

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ Stage 1a: Contrast Scaling
│   │   └── y ≈ input_Y × contrast / 512
│   │       (shift-add approximation using top 3 bits)
│   │
│   ├─ Stage 1b: Brightness Offset + Hi-Contrast
│   │   ├── y += (brightness - 512), clamped [0, 1023]
│   │   └── If Hi Contrast: y = (y ≥ 512) ? 1023 : 0
│   │
│   ├─ Stage 2: Scanline Darkening
│   │   ├── Alternate mode: darken every-other line
│   │   ├── Triple mode: darken every-3rd line
│   │   └── y_dark ≈ y × (1023 - scanline_amount) / 1024
│   │
│   ├─ Stage 3: Bloom (Horizontal IIR)
│   │   ├── Level 0: no bloom (pass-through)
│   │   ├── Level 1: 50% prev + 50% current
│   │   ├── Level 2: 75% prev + 25% current
│   │   ├── Level 3: ~94% prev + ~6% current
│   │   └── H+V mode: seed bloom from previous line's residual
│   │
│   ├─ Stage 4: Vignette (optional)
│   │   ├── x < 16:  25% brightness
│   │   ├── x < 48:  50% brightness
│   │   ├── x < 80:  87.5% brightness
│   │   ├── x > 1856: 25% brightness
│   │   ├── x > 1824: 50% brightness
│   │   └── x > 1792: 87.5% brightness
│   │
├── U/V Channels ───────────────────────────────────────────────
│   │
│   └─ Stage 3: Phosphor Tint
│       ├── Presets 0–6: fixed U/V from lookup table
│       └── Preset 7 (Custom): 4-quadrant hue from Custom Hue knob
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline (9 clocks) → pass-through
│
└── Interpolator Mix (4 clk) → Bypass Mux → Output
```

Contrast and brightness are applied in sequence: contrast scales the dynamic range, then brightness shifts the result vertically. This means a contrast of 0% crushes the signal to black regardless of brightness. The bloom IIR is unidirectional — it only smears rightward along each scanline. At level 3 (heavy bloom), approximately 94% of the accumulated value persists from pixel to pixel, creating a long bright tail that extends far to the right of any bright feature. When Bloom Axis is set to H+V, the bloom state is seeded at the start of each line from the previous line's final value, adding a subtle vertical glow component.

---

## Parameter Reference

<img src={phosphor_control_panel} alt="Videomancer front panel with Phosphor loaded"/>
*Videomancer's front panel with Phosphor active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Brightness adds a DC offset to every pixel after contrast scaling. At 50% the offset is zero (unity). Below 50% the image darkens overall; above 50% it lifts toward white. The offset is computed as $\text{brightness} - 512$ in 10-bit domain (range −512 to +511). When Hi Contrast is active, brightness shifts the threshold point — a brighter offset means more pixels cross the 512 midpoint and appear as full white in the binary output.

---

#### Knob 2 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Contrast scales the input luminance before the brightness offset is applied. The VHDL uses a shift-add approximation: the top 3 bits of the register select whether to add the input shifted by 0, 1, or 2 positions. At 0% the output is black. At 50% (~512) the gain is approximately unity. At 100% (~1023) the gain is approximately 1.75× — just under 2×. This approximation introduces slight gain quantisation (8 effective steps), but in practice the steps are not visible.

---

#### Knob 3 — Bloom
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Bloom controls the horizontal IIR glow intensity. The top 2 bits of the register select four discrete levels: no bloom, light (50/50 mix), medium (75% carry / 25% current), and heavy (~94% carry / ~6% current). At the heavy setting, a single bright pixel creates a visible glow trail extending hundreds of pixels to its right. The bloom state resets at the start of each scanline (in H-only mode) or carries a residual from the previous line (in H+V mode).

---

#### Knob 4 — Scanlines
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scanlines controls the depth of scanline darkening. At 0% all lines are equally bright — no visible scanlines. At 100% the dark lines are completely black. The attenuation uses a shift-add multiplication: $y_{\text{dark}} \approx y \times (1023 - \text{scanlines}) / 1024$. The pattern of which lines are darkened depends on the Scan Mode toggle: every-other or every-third.

---

#### Knob 5 — Phosphor
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Phosphor selects the tint applied to the output — a monochrome colourisation that simulates the phosphor coating of a historical CRT type. The 3 most significant bits of the register select one of 8 presets: P1 green (0), P4 white (1), P7 amber (2), P31 blue-white (3), P22 green (4), P33 orange (5), P43 cyan (6), or Custom (7). Each preset defines fixed U and V values; the luminance channel carries the image detail.

---

#### Knob 6 — Custom Hue
| Property | Value |
|----------|-------|
| Range | -180° – 180° |
| Default | -120° |
| Suffix | ° |

Custom Hue sets the chrominance when Phosphor is in Custom mode (preset 7). The 10-bit register is divided into four quadrants: 0–255 sweeps from red toward yellow (V rises), 256–511 from yellow toward green (U drops), 512–767 from green toward cyan (V drops), 768–1023 from cyan back toward red (U rises). This gives full 360° hue coverage. When any other phosphor preset is selected, this knob has no effect.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Scan Mode** | Alternate | Triple |
| **8 — Bloom Axis** | H Only | H+V |
| **9 — Vignette** | Off | On |
| **10 — Hi Contrast** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary features. Scan Mode and Bloom Axis affect the geometry of existing effects. Vignette adds spatial dimming. Hi Contrast enables vector-display mode. Together they can transform a subtle CRT tint into an aggressive retro-arcade look. All toggles are latched at the register level — switching does not cause transients or glitches.

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

Routes the unprocessed input signal directly to the output, bypassing all Phosphor processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Phosphor-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.





---

## Guided Exercises

These exercises progress from basic gain adjustment through CRT scanline structure to full retro monitor simulation, building up the processing chain layer by layer.

### Exercise 1: Contrast and Brightness Calibration

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: phosphor_source1_runner, after: phosphor_ex1_s1 },
    { label: "Car", before: phosphor_source2_car, after: phosphor_ex1_s2 },
    { label: "Turtle", before: phosphor_source3_turtle, after: phosphor_ex1_s3 },
    { label: "Pattern", before: phosphor_source4_pattern, after: phosphor_ex1_s4 },
    { label: "Woman", before: phosphor_source5_woman, after: phosphor_ex1_s5 },
    { label: "Berries", before: phosphor_source6_berries, after: phosphor_ex1_s6 },
  ]}
/>
*Contrast and Brightness Calibration — simulated result across source images.*
**Source**: A greyscale gradient or colour bar test pattern.

**What You'll Create**: Learn how contrast and brightness interact as a gain-and-offset pair, and observe the shift-add contrast approximation.

1. **Unity setup**: Set Contrast to ~50% and Brightness to ~50%. The test pattern should pass through with minimal change — this is the unity gain/offset point.
2. **Swept contrast**: Slowly reduce Contrast to 0%. The image fades to black as gain drops. Now sweep from 0% to 100% and watch the signal expand. Notice that the gain does not increase perfectly smoothly — the shift-add approximation produces 8 discrete steps.
3. **Brightness offset**: Return Contrast to ~50%. Sweep Brightness below 50% (image darkens globally) and above 50% (image lifts). At 0% the offset is −512, crushing all but the brightest pixels to black.
4. **Combine**: Set Contrast to ~75% and Brightness to ~60%. The image is brighter than unity with expanded contrast. This is the basic "proc amp" adjusts that every CRT monitor has.
5. **Hi Contrast**: Enable Hi Contrast (Toggle 10). The smooth gradient collapses to pure black and white. Sweep Brightness to move the threshold — the line between black and white shifts across the gradient.

**Key concepts**: Contrast is multiplicative gain, brightness is additive offset, gain × offset = proc amp, Hi Contrast is 1-bit quantisation at the 512 threshold

---

### Exercise 2: Scanline and Phosphor CRT Look

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: phosphor_source1_runner, after: phosphor_ex2_s1 },
    { label: "Car", before: phosphor_source2_car, after: phosphor_ex2_s2 },
    { label: "Turtle", before: phosphor_source3_turtle, after: phosphor_ex2_s3 },
    { label: "Pattern", before: phosphor_source4_pattern, after: phosphor_ex2_s4 },
    { label: "Woman", before: phosphor_source5_woman, after: phosphor_ex2_s5 },
    { label: "Berries", before: phosphor_source6_berries, after: phosphor_ex2_s6 },
  ]}
/>
*Scanline and Phosphor CRT Look — simulated result across source images.*
**Source**: Live camera footage or full-colour video content.

**What You'll Create**: Build the classic CRT monitor aesthetic by combining scanlines and phosphor tinting.

1. **Green terminal**: Set Phosphor to 0 (P1 green). The image turns monochrome green. This is the look of a 1970s terminal or early Apple II monitor.
2. **Add scanlines**: Increase Scanlines to ~50%. Dark gaps appear between alternate lines — the characteristic CRT raster. At ~80% the effect becomes quite pronounced.
3. **Triple mode**: Switch Scan Mode (Toggle 7) to Triple. Now every third line is darkened instead of every second. The image retains more brightness but the scanline texture is subtler.
4. **Amber monitor**: Set Phosphor to 2 (P7 amber). Combined with scanlines, this creates the warm amber look of an IBM PC monochrome display.
5. **Custom colour**: Set Phosphor to 7 (Custom) and sweep Custom Hue from 0° to 360°. Watch the tint cycle through red, yellow, green, cyan. Find a colour that matches a specific monitor you remember.
6. **White phosphor**: Set Phosphor to 1 (P4 white). The tint is neutral — scanlines are visible but colour is preserved from the input. This is the standard television phosphor look.

**Key concepts**: Phosphor presets are fixed UV pairs, scanline darkening is multiplicative, alternate vs triple scanline spacing, custom hue uses 4-quadrant UV mapping

---

### Exercise 3: Full Retro CRT Simulation

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: phosphor_source1_runner, after: phosphor_ex3_s1 },
    { label: "Car", before: phosphor_source2_car, after: phosphor_ex3_s2 },
    { label: "Turtle", before: phosphor_source3_turtle, after: phosphor_ex3_s3 },
    { label: "Pattern", before: phosphor_source4_pattern, after: phosphor_ex3_s4 },
    { label: "Woman", before: phosphor_source5_woman, after: phosphor_ex3_s5 },
    { label: "Berries", before: phosphor_source6_berries, after: phosphor_ex3_s6 },
  ]}
/>
*Full Retro CRT Simulation — simulated result across source images.*
**Source**: High-contrast video — text on a dark background, arcade game footage, or bold graphic content.

**What You'll Create**: Combine all processing stages for a full retro CRT simulation: gain, scanlines, bloom, vignette, and phosphor tint.

1. **Start from Exercise 2**: Begin with P1 green and moderate scanlines.
2. **Add bloom**: Increase Bloom to ~60%. Bright areas develop a rightward glow trail — this is the IIR horizontal bloom. Notice the glow only spreads to the right, not evenly in both directions.
3. **Heavy bloom**: Push Bloom to ~100%. The glow now extends far to the right, creating dramatic light trails behind bright features. This is the level 3 (~94% carry) IIR.
4. **Vertical bloom**: Switch Bloom Axis to H+V. The glow now has a subtle vertical component — bright areas bleed downward as well. This creates a warmer, more diffuse halo.
5. **Vignette**: Enable Vignette (Toggle 9). The left and right 80 pixels darken, creating a tunnel-vision effect that suggests the curvature of a CRT faceplate.
6. **Vector arcade**: Enable Hi Contrast. The image collapses to 1-bit black and green. With heavy bloom, the bright lines develop the characteristic vector-game glow. Adjust Brightness to control how much of the image is "on".
7. **Mix for subtlety**: Lower the Mix fader to ~50%. The CRT effect blends with the original signal, creating a half-strength retro look.

**Key concepts**: Bloom IIR is unidirectional (rightward), H+V adds vertical seeding, vignette is 3-step edge darkening, Hi Contrast + bloom = vector display, mix controls effect intensity

---


## Tips

- **Hi Contrast transforms the signal**: It is not a post-process — it replaces the analogue signal with a 1-bit digital version. Use it deliberately, not as a subtle effect.
- **Vignette frames the image**: Enable Vignette as the final touch to complete the CRT illusion. It works best with green or amber phosphor tint.
- **Custom presets via MIDI**: Automate the Phosphor selector via MIDI CC to cycle through CRT types in a performance.
- **Feedback creates persistence**: Routing Phosphor's output back into its input creates a temporal feedback loop — the bloom accumulates over frames, simulating the phosphor persistence that the spatial IIR cannot capture.
- **Bloom level 3 is extreme**: The ~94% carry means a single bright pixel's glow extends for approximately 16 pixels at half-brightness. Use levels 1 or 2 for subtlety.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bloom** | Spatial glow around bright features, modelled here as a horizontal IIR low-pass filter. |
| **CRT** | Cathode-Ray Tube; a vacuum tube display that fires an electron beam at a phosphor-coated screen to produce light. |
| **Hi Contrast** | 1-bit quantisation that clamps the signal to black (0) or white (1023) at the 512 threshold. |
| **IIR** | Infinite Impulse Response; a filter type where the output feeds back into the computation, creating sustained response. |
| **Phosphor** | A chemical compound coating the inside of a CRT that emits light when struck by electrons. |
| **Proc Amp** | Processing Amplifier; the gain-and-offset stage that implements brightness/contrast adjustment. |
| **Raster** | The pattern of horizontal scanlines that compose a CRT image, painted sequentially from top to bottom. |
| **Scanline** | A single horizontal line of the raster; in CRT simulation, alternating bright and dark lines create the visible line structure. |
| **Shift-Add** | A multiplication approximation technique that replaces hardware multipliers with combinations of bit-shifts and additions. |
| **Vector Display** | A CRT display mode where the electron beam traces lines directly rather than raster-scanning, producing bright lines on a dark background. |
| **Vignette** | Darkening at the edges of the frame, simulating the optical falloff of CRT displays. |

---
