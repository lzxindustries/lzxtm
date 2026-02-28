---
draft: true
sidebar_position: 167
slug: /instruments/videomancer/mimeo
title: "Mimeo"
image: /img/instruments/videomancer/mimeo/mimeo_hero.png
---

import mimeo_before_after from '/img/instruments/videomancer/mimeo/mimeo_before_after.png';
import mimeo_control_panel from '/img/instruments/videomancer/mimeo/mimeo_control_panel.png';
import mimeo_exercise1_result from '/img/instruments/videomancer/mimeo/mimeo_exercise1_result.png';
import mimeo_exercise2_result from '/img/instruments/videomancer/mimeo/mimeo_exercise2_result.png';
import mimeo_exercise3_result from '/img/instruments/videomancer/mimeo/mimeo_exercise3_result.png';
import mimeo_hero from '/img/instruments/videomancer/mimeo/mimeo_hero.png';
import mimeo_source1_kodim02 from '/img/instruments/videomancer/mimeo/mimeo_source1_kodim02.png';
import mimeo_source2_kodim07 from '/img/instruments/videomancer/mimeo/mimeo_source2_kodim07.png';
import mimeo_source3_kodim01_bw from '/img/instruments/videomancer/mimeo/mimeo_source3_kodim01_bw.png';

# Mimeo

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={mimeo_hero} alt="Mimeo hero image"/>
*Mimeo rendering a spirit duplicator print with purple ink on cream paper stock, showing letterform fill-in and progressive copy fade.*
<img src={mimeo_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Mimeo applied.*

---

## Overview

Before photocopiers, before laser printers, there was the mimeograph. Schools, churches, and small offices produced their printed material on stencil duplicators and spirit duplicators — machines that pressed ink through a perforated stencil or transferred dye from a master sheet onto paper. Each copy was slightly different from the last. The ink bled a little at the edges. The density varied across the page. By the fiftieth copy, the text was fading to a ghost. Mimeo recreates that entire experience in the video domain.

The program reduces the input image to a small number of discrete tonal levels — like the limited ink density a stencil can produce — and then applies the characteristic artifacts of mechanical duplication: letterform fill-in (where thin white gaps between dark areas flood with ink), horizontal edge bleed (from the rotating print drum), ink density noise, progressive copy fade, and paper fiber grain texture. Four ink colors correspond to real duplicator technologies: purple for spirit duplicators, black for stencil mimeographs, blue for hectographs, and red for carbon copies.

The name is the informal term for a mimeographed copy. At gentle settings Mimeo produces a clean posterized print with subtle paper texture. At extreme settings it creates a barely legible, heavily degraded nth-generation duplicate — the kind of hand-cranked copy that smelled like solvent and smudged when you touched it.

---

## Background

### What Is a Mimeograph?

A mimeograph (also called a stencil duplicator) works by forcing ink through a perforated wax stencil onto paper. The operator types or draws onto the stencil, cutting tiny holes that allow ink to pass through when pressed against paper by a rotating drum. Each revolution of the drum produces one copy. The technology was dominant from the 1880s through the 1970s. Mimeo's Tone Levels control simulates the limited tonal range of stencil printing — most stencils could only produce a few discrete density levels, not smooth gradients.

### What Is a Spirit Duplicator?

The spirit duplicator (often called a Ditto machine after the dominant brand) used a different process. A wax master sheet coated with a dye (typically purple aniline) was placed on a rotating drum. Each sheet of paper was moistened with a volatile solvent that dissolved a thin layer of dye from the master, transferring it to the paper. Each copy removed some dye from the master, so prints progressively faded across a run — the first copy was dark and saturated, the fiftieth was pale and washed out. Mimeo's Copy Fade control directly simulates this progressive degradation.

### What Is Letterform Fill-In?

In stencil printing, thin white spaces between dark strokes can flood with ink — the gaps are too narrow for the paper to remain clean. The letter "e" loses its counter (the enclosed white space), thin serifs merge together, and fine detail disappears into solid ink. Mimeo implements this as a horizontal minimum filter: if the brightness gap between the current pixel and its neighbor is less than the Fill-In threshold, the darker value wins. This causes dark areas to expand into adjacent lighter areas, exactly as ink fills into narrow gaps on a stencil.

### What Is Edge Bleed?

The rotating drum of a duplicator applies ink with a slight directional bias. As the drum rolls across the page, wet ink smears horizontally in the direction of rotation. Mimeo simulates this with a one-directional horizontal IIR (Infinite Impulse Response) low-pass filter. Each pixel's darkness is blended with its left neighbor's darkness — the feedback coefficient is controlled by the Edge Bleed knob. Higher values create more smearing, as if the drum is rotating faster or the ink is wetter.

### What Is Paper Grain?

Real paper has a visible fiber texture — a random micro-pattern of lighter and darker spots caused by variations in pulp density. This grain is especially visible on the cheap, absorbent paper stocks used in mimeograph machines. Mimeo adds paper grain as LFSR-generated noise at a lower amplitude than the ink noise, creating a subtle textural background that distinguishes the paper from digital flatness.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register ────────────────────────────────────
│   └─ Register Y channel
│
├── Stage 2: Posterization + Fill-In ───────────────────────────
│   ├─ Quantize Y to N levels (2/3/4/5/6, or 2 if Stencil)
│   └─ Horizontal minimum filter (fill-in threshold)
│
├── Stage 3: Ink Tint + Copy Fade ──────────────────────────────
│   ├─ Ink density = 1023 − quantized Y
│   ├─ Copy fade: density × (1023 − copy_fade) / 1024
│   ├─ Y = paper_y − range_y × density / 1024
│   ├─ U = paper_u + delta_u × density / 1024
│   └─ V = paper_v + delta_v × density / 1024
│
├── Stage 4: Edge Bleed + Noise + Grain ────────────────────────
│   ├─ Horizontal IIR low-pass on Y (alpha from top 4 bits)
│   ├─ IIR only darkens (ink spreads into paper, not reverse)
│   ├─ LFSR ink noise (6-bit centered, scaled by Noise knob)
│   └─ LFSR paper grain (6-bit centered, lower amplitude)
│
├── Interpolator (4 clocks) ────────────────────────────────────
│   └─ wet/dry mix per channel (Y, U, V)
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ hsync, vsync, field delayed to match pipeline
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed or delayed original
```

The processing chain is strictly luminance-driven. Chrominance is generated entirely from the ink/paper palette lookup in Stage 3 — the original U and V channels are discarded. The ink density value (inverted quantized Y) drives all three output channels simultaneously, producing a monochromatic tinted result. The edge bleed IIR in Stage 4 is asymmetric: it only applies when the blended value is *darker* than the tinted value, ensuring ink spreads into paper but paper never bleaches into ink. The LFSR noise source runs continuously and provides both ink noise (upper 6 bits) and paper grain (lower 6 bits) from the same 16-bit register.

---

## Parameter Reference

<img src={mimeo_control_panel} alt="Videomancer front panel with Mimeo loaded"/>
*Videomancer's front panel with Mimeo active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Tone Levels
| Property | Value |
|----------|-------|
| Range | 2 – 6 |
| Default | 3 |

Controls the number of discrete tonal levels in the printed output. The pot value maps to five quantization depths: 2, 3, 4, 5, or 6 levels. At 2 levels the output is pure binary — ink or paper, with no intermediate tones. At 6 levels the output has smooth tonal gradation approaching a continuous-tone print. The quantization thresholds are evenly distributed across the input luminance range, and output levels are mapped to evenly spaced values across the full 10-bit range.

---

#### Knob 2 — Fill-In
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the letterform fill-in threshold. This is a horizontal minimum filter that expands dark areas into adjacent lighter areas. When the brightness gap between the current quantized pixel and the previous pixel is less than the Fill-In threshold, the darker value replaces the lighter one. At zero there is no fill-in. At high values, thin white gaps between dark regions are completely flooded — small text features merge, fine lines thicken, and counters in letterforms close up.

---

#### Knob 3 — Edge Bleed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls horizontal edge bleed — the directional ink smear from the print drum. The top 4 bits of the register set the IIR feedback coefficient (alpha = 0..15/16). At zero there is no bleed. At maximum the IIR has very high feedback, causing dark edges to trail significantly to the right. The filter is asymmetric — it only darkens, never lightens — so ink can spread into paper but paper never intrudes into inked areas.

---

#### Knob 4 — Noise
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the amplitude of LFSR-generated ink density noise. This simulates the random variation in ink transfer that occurs with each revolution of the duplicator drum — some areas receive slightly more or less ink than intended. The noise is added to the luminance channel after edge bleed. At zero the print is perfectly clean. At high values the tonal levels become rough and gritty, with visible random variation in ink coverage.

---

#### Knob 5 — Copy Fade
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Simulates progressive copy fade across a print run. The register value attenuates ink density: density is multiplied by (1023 − copy_fade) / 1024. At zero (first copy), full ink density is applied. As the value increases, the ink becomes progressively lighter — simulating the 10th, 20th, or 50th copy from a spirit duplicator where each print removes dye from the master. At maximum the print is almost entirely paper with barely visible ink traces.

---

#### Knob 6 — Paper Grain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls paper fiber grain texture amplitude. A separate LFSR noise source (lower 6 bits of the same 16-bit register) is scaled by this control and added to the luminance channel. The amplitude is half that of the ink noise at the same register value, producing a subtler texture that suggests the fibrous surface of cheap duplicator paper stock. At zero the paper is perfectly smooth. At moderate values a realistic paper texture emerges.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Ink Color A** | Off | On |
| **8 — Ink Color B** | Off | On |
| **9 — Paper Tint** | Warm | Cool |
| **10 — Stencil** | Tonal | Binary |
| **11 — Bypass** | Off | On |

Toggles 7–10 configure the duplicator technology simulation: ink color, paper stock, and print mode. Ink Color A and B form a 2-bit selector that chooses between four historically accurate ink palettes. Paper Tint selects warm cream or cool white stock. Stencil mode overrides Tone Levels and forces binary (2-level) output regardless of the knob setting — simulating a basic stencil cut where ink either passes through or doesn't.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed duplicator output and the original delayed input. At 100% the full print simulation is applied. At 0% the original signal passes through unchanged. Intermediate values overlay the print effect onto the original — useful for a translucent print-over-video look where the ink tint and posterization are partially visible over the source.

---

## Guided Exercises

These exercises progress from basic posterized prints through fully degraded multi-generation duplicates. Each exercise engages more of the duplicator's artifact chain.

### Exercise 1: Spirit Duplicator Print

<img src={mimeo_exercise1_result} alt="Spirit Duplicator Print result"/>
*Spirit Duplicator Print — simulated result across source images.*
**Source**: A camera feed of text, signage, or high-contrast graphic material.

**Objective**: Create a classic spirit duplicator output — purple ink on cream paper with gentle copy fade.

1. **Purple ink**: Set Ink Color A and B both to Off (00 = purple). Set Paper Tint to Warm for cream paper.
2. **Moderate tone levels**: Set Tone Levels to ~50% (4 levels). The image posterizes into four discrete ink densities.
3. **Gentle fill-in**: Increase Fill-In to ~30%. Watch thin white gaps between dark areas begin to close up.
4. **Light edge bleed**: Set Edge Bleed to ~25%. Dark edges develop a subtle rightward ink smear.
5. **Copy fade**: Slowly increase Copy Fade from 0%. Watch the print progressively lighten as if you are pulling the 10th, 20th, 50th copy from the machine.
6. **Paper texture**: Add Paper Grain at ~30% for realistic paper fiber texture.

**Key concepts**: Spirit duplicator uses purple aniline dye, copy fade simulates progressive dye depletion from the master, letterform fill-in floods narrow white gaps

---

### Exercise 2: Stencil Mimeograph

<img src={mimeo_exercise2_result} alt="Stencil Mimeograph result"/>
*Stencil Mimeograph — simulated result across source images.*
**Source**: High-contrast footage — text overlays, sharp graphic patterns, or architectural details.

**Objective**: Create a binary stencil mimeograph print with heavy ink artifacts.

1. **Black ink**: Set Ink Color A to On, B to Off (01 = black). Paper Tint to Cool.
2. **Stencil mode**: Enable the Stencil toggle. Output is forced to binary (2-level) regardless of Tone Levels.
3. **Heavy fill-in**: Increase Fill-In to ~60%. Fine detail floods with ink — thin lines merge, text becomes bold.
4. **Strong bleed**: Set Edge Bleed to ~50%. The horizontal IIR smears dark edges significantly to the right.
5. **Ink noise**: Increase Noise to ~40%. The previously clean ink areas develop visible random density variation.
6. **Compare**: Toggle Stencil off. The image jumps to multi-tone output while all artifacts remain. Toggle back — binary mode snaps everything to pure ink-or-paper.

**Key concepts**: Stencil mode forces binary output, black ink is chromatically neutral, IIR bleed is asymmetric (darkening only)

---

### Exercise 3: Degraded Multi-Generation Copy

<img src={mimeo_exercise3_result} alt="Degraded Multi-Generation Copy result"/>
*Degraded Multi-Generation Copy — simulated result across source images.*
**Source**: Any footage — the more detailed the source, the more dramatic the degradation.

**Objective**: Simulate a severely degraded nth-generation duplicate at the end of a long print run.

1. **Red ink on cream**: Set Ink Color A and B both to On (11 = red). Paper Tint to Warm.
2. **Few levels**: Set Tone Levels to ~25% (3 levels). The image simplifies to ink, midtone, and paper.
3. **Maximum fill-in**: Set Fill-In to ~80%. Nearly every white gap floods with ink.
4. **Heavy bleed**: Set Edge Bleed to ~70%. The horizontal smear is dramatic.
5. **Strong noise**: Set Noise to ~60%. Ink coverage becomes rough and uneven.
6. **Heavy fade**: Set Copy Fade to ~70%. The ink becomes pale and washed out — a 50th-generation copy.
7. **Paper grain**: Set Paper Grain to ~50%. The paper fiber texture competes with the fading ink.
8. **A/B compare**: Use Mix to blend at ~50%, seeing the degraded print ghosted over the original input.

**Key concepts**: All artifact stages compound — fill-in + bleed + noise + fade + grain create authentic multi-generational print degradation, copy fade is multiplicative so it scales all ink uniformly

---


## Tips

- **Purple is the classic look**: Spirit duplicator purple (Ink Color 00) is the most iconic and recognizable mimeograph aesthetic. Start there for authentic results.
- **Stencil mode is dramatic**: Binary mode produces the starkest print look — pure ink or pure paper. Combine with fill-in for bold, heavy stencil prints.
- **Copy Fade tells a story**: Animate Copy Fade from 0% to maximum over time to simulate watching an entire print run degrade copy by copy.
- **Fill-in eats fine detail**: High fill-in values destroy small features. This is historically accurate — real stencils lose fine detail as ink fills narrow gaps.
- **Edge Bleed is directional**: The IIR smear runs left to right, simulating a clockwise print drum. Dark edges trail to the right.
- **Noise + Grain layer naturally**: Ink noise affects the inked areas most visibly while paper grain affects the background. Together they create a realistic paper-and-ink texture stack.
- **Feedback loops**: Route the output back to the input to simulate physically re-copying a mimeograph — each pass adds more fill-in, bleed, and noise degradation.
- **Black ink for text**: When processing text or high-contrast graphic material, black ink (01) with Stencil mode produces the most legible result.

---

## Glossary

| Term | Definition |
|------|------------|
| **Copy Fade** | Progressive reduction in ink density across a print run, caused by dye depletion from the spirit duplicator master sheet. |
| **Edge Bleed** | Horizontal ink smearing caused by the rotating drum of a duplicator, simulated as a one-directional IIR low-pass filter. |
| **Hectograph** | A duplicating process using a gelatin pad to transfer dye to paper, typically producing blue prints. |
| **IIR** | Infinite Impulse Response; a filter type where the output feeds back into the input, creating persistent temporal or spatial effects. |
| **Letterform Fill-In** | The flooding of narrow white spaces between dark ink areas, caused by capillary action and ink pressure in stencil printing. |
| **LFSR** | Linear Feedback Shift Register; a digital circuit that generates pseudo-random binary sequences, used here for ink noise and paper grain. |
| **Mimeograph** | A stencil duplicator that forces ink through a perforated wax stencil onto paper, widely used from the 1880s through the 1970s. |
| **Paper Grain** | The visible fiber texture of paper caused by variations in pulp density, especially noticeable on cheap duplicator stock. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Posterization** | Reducing the number of distinct tonal levels in an image, creating flat areas of uniform brightness. |
| **Spirit Duplicator** | A duplicating machine (e.g., Ditto machine) that transfers aniline dye from a wax master to paper using a volatile solvent. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
