---
draft: true
sidebar_position: 66
slug: /instruments/videomancer/corollas
title: "Corollas"
image: /img/instruments/videomancer/corollas/corollas_hero_s1.png
description: "Corollas is a frequency-doubling harmonic processor that transforms the luminance channel of an incoming video signal into a series of concentric, petal-like interference patterns distributed across the Y, U, and V output channels."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import corollas_source1_boat from '/img/instruments/videomancer/corollas/corollas_source1_boat.png';
import corollas_source2_dog from '/img/instruments/videomancer/corollas/corollas_source2_dog.png';
import corollas_source3_turtle from '/img/instruments/videomancer/corollas/corollas_source3_turtle.png';
import corollas_source4_pattern from '/img/instruments/videomancer/corollas/corollas_source4_pattern.png';
import corollas_source5_girl from '/img/instruments/videomancer/corollas/corollas_source5_girl.png';
import corollas_source6_wood from '/img/instruments/videomancer/corollas/corollas_source6_wood.png';
import corollas_hero_s1 from '/img/instruments/videomancer/corollas/corollas_hero_s1.png';
import corollas_hero_s2 from '/img/instruments/videomancer/corollas/corollas_hero_s2.png';
import corollas_hero_s3 from '/img/instruments/videomancer/corollas/corollas_hero_s3.png';
import corollas_hero_s4 from '/img/instruments/videomancer/corollas/corollas_hero_s4.png';
import corollas_hero_s5 from '/img/instruments/videomancer/corollas/corollas_hero_s5.png';
import corollas_hero_s6 from '/img/instruments/videomancer/corollas/corollas_hero_s6.png';
import corollas_ex1_s1 from '/img/instruments/videomancer/corollas/corollas_ex1_s1.png';
import corollas_ex1_s2 from '/img/instruments/videomancer/corollas/corollas_ex1_s2.png';
import corollas_ex1_s3 from '/img/instruments/videomancer/corollas/corollas_ex1_s3.png';
import corollas_ex1_s4 from '/img/instruments/videomancer/corollas/corollas_ex1_s4.png';
import corollas_ex1_s5 from '/img/instruments/videomancer/corollas/corollas_ex1_s5.png';
import corollas_ex1_s6 from '/img/instruments/videomancer/corollas/corollas_ex1_s6.png';
import corollas_ex2_s1 from '/img/instruments/videomancer/corollas/corollas_ex2_s1.png';
import corollas_ex2_s2 from '/img/instruments/videomancer/corollas/corollas_ex2_s2.png';
import corollas_ex2_s3 from '/img/instruments/videomancer/corollas/corollas_ex2_s3.png';
import corollas_ex2_s4 from '/img/instruments/videomancer/corollas/corollas_ex2_s4.png';
import corollas_ex2_s5 from '/img/instruments/videomancer/corollas/corollas_ex2_s5.png';
import corollas_ex2_s6 from '/img/instruments/videomancer/corollas/corollas_ex2_s6.png';
import corollas_ex3_s1 from '/img/instruments/videomancer/corollas/corollas_ex3_s1.png';
import corollas_ex3_s2 from '/img/instruments/videomancer/corollas/corollas_ex3_s2.png';
import corollas_ex3_s3 from '/img/instruments/videomancer/corollas/corollas_ex3_s3.png';
import corollas_ex3_s4 from '/img/instruments/videomancer/corollas/corollas_ex3_s4.png';
import corollas_ex3_s5 from '/img/instruments/videomancer/corollas/corollas_ex3_s5.png';
import corollas_ex3_s6 from '/img/instruments/videomancer/corollas/corollas_ex3_s6.png';

# Corollas

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: corollas_source1_boat, after: corollas_hero_s1 },
    { label: "Dog", before: corollas_source2_dog, after: corollas_hero_s2 },
    { label: "Turtle", before: corollas_source3_turtle, after: corollas_hero_s3 },
    { label: "Pattern", before: corollas_source4_pattern, after: corollas_hero_s4 },
    { label: "Girl", before: corollas_source5_girl, after: corollas_hero_s5 },
    { label: "Wood", before: corollas_source6_wood, after: corollas_hero_s6 },
  ]}
/>
*Cascading harmonic petals blooming across luma and chroma channels, four frequency-doubled stages folding a live video signal into layered interference geometry.*

---

## Overview

Corollas is a frequency-doubling harmonic processor that transforms the luminance channel of an incoming video signal into a series of concentric, petal-like interference patterns distributed across the Y, U, and V output channels. The input luma is first conditioned through a proc amp stage — applying contrast (Span) and brightness (Offset) — then cascaded through four frequency doublers in series, producing harmonics at 2×, 4×, 8×, and 16× the original spatial frequency. Each harmonic receives an independent brightness offset and polarity inversion toggle, and the four processed harmonics are mapped to the output color channels: the average of harmonics 1 and 2 drives Y, harmonic 3 drives U, and harmonic 4 drives V. A threshold keyer gates the final output, forcing pixels below the threshold to black with neutral chroma.

The name "corollas" refers to the collective petals of a flower — the corolla is the ring of petals that surrounds the reproductive organs, and the concentric folded waveforms produced by cascaded frequency doubling bear a strong visual resemblance to overlapping petal structures. When the four harmonic stages carry different offsets and inversion states, the resulting Y/U/V pattern creates radially symmetric interference that naturally evokes floral geometry. The program descends from the October 2025 Pinwheel architecture with extended per-harmonic control, adding individual offset and inversion for each doubler stage.

The dynamic range of Corollas spans from near-transparent parametric tinting — when all Hue offsets are at zero and the base signal passes through with minimal folding — to aggressive, high-frequency color fragmentation where the 16× harmonic creates fine spectral banding across the chroma channels. The Span control amplifies or compresses the input luma before the doubler chain, controlling how much of the original tonal range participates in the folding process. At low Span, only the brightest highlight regions fold through all four doublers; at high Span, even midtones undergo full 16× frequency multiplication.

---

## Background

### Signal Harmonics and Overtone Series

In acoustics, a harmonic is an integer multiple of a fundamental frequency: the second harmonic vibrates at twice the fundamental, the third at three times, and so on. The overtone series — the set of all harmonics present in a sound — defines the timbral character of an instrument. A pure sine wave has no harmonics; a sawtooth wave contains all harmonics with amplitudes decreasing as 1/n; a square wave contains only odd harmonics. Corollas applies this concept to the spatial domain of video: the input luma ramp is treated as a fundamental, and each frequency doubler stage generates a successive harmonic. The result is a visual overtone series where each harmonic contributes a distinct spatial frequency to the output pattern, creating complex interference when the harmonics are recombined across Y, U, and V.

### Frequency Doubling by Waveform Folding

The frequency_doubler module implements a simple but powerful operation: values below the midpoint are scaled up by 2, and values above the midpoint are mirrored and scaled. Mathematically, this is equivalent to applying the triangle wave function $f(x) = 2|x - 0.5|$ — the absolute-value fold that converts a ramp into a triangle wave, thereby doubling its spatial frequency. When cascaded, each fold doubles again: a single ramp becomes a triangle (2×), then a quad-peak waveform (4×), then eight peaks (8×), then sixteen (16×). This geometric progression is the same principle used in optical frequency doubling (second-harmonic generation) in nonlinear crystals, though here the folding is purely arithmetic rather than photonic. The wrapping arithmetic in 10-bit unsigned ensures that overflow at the fold boundaries creates sharp cusps — the petals of the corolla.

### Processing Amplifier Conditioning

The proc_amp_u stage at the input of the chain applies the classic video processing amplifier formula: $\text{result} = (\text{input} - 0.5) \times \text{contrast} + \text{brightness}$. The Span parameter acts as contrast (ranging from 0× to 2×), controlling how much the input luma is stretched around its midpoint before entering the doubler chain. The Offset parameter acts as brightness, shifting the entire signal up or down. This conditioning stage is critical because the frequency doublers respond nonlinearly to signal level — a narrow-contrast input that hovers near the midpoint will fold minimally, while a full-range input will exercise every fold boundary across all four stages. Span and Offset together allow precise control over which portion of the input tonal range drives the harmonic generation.

### Per-Harmonic Offset and Inversion

After the doubler chain, each of the four harmonics receives two independent controls: a brightness offset (Hue 1–4) and a polarity inversion toggle (Invert Hue 1–4). Inversion flips the harmonic waveform before the offset is applied — where a peak was, a trough appears, and the petal pattern mirrors around the midpoint. This creates complementary interference when one harmonic is inverted and another is not: the peaks of one align with the troughs of the other, producing alternating color bands across the output. The brightness offset then shifts the entire waveform, effectively rotating the phase of the harmonic in the color domain. Because the offset wraps (10-bit unsigned addition), sweeping a Hue parameter from 0 to 1023 cycles the harmonic through a full rotation of interference alignment.

### Color Channel Mapping and Threshold Keying

The final output stage maps the four harmonic signals to the YUV color channels: Y receives the average of harmonics 1 (2×) and 2 (4×), producing a complex luminance pattern with both coarse and fine structure. U receives harmonic 3 (8×), creating chroma interference at a higher spatial frequency than luma. V receives harmonic 4 (16×), creating the finest spectral banding in the complementary chroma axis. This asymmetric mapping — two harmonics to Y, one each to U and V — ensures that the luminance pattern is always richer than either chroma component, maintaining visual coherence even at extreme settings. The threshold keyer at the output gates the entire signal: when the computed Y value falls below the threshold, the pixel is forced to black (Y=0) with neutral chroma (U=V=midpoint), creating a hard-edged key effect that carves out the darkest portions of the harmonic pattern.


---

## Signal Flow

```
Video Input (YUV 4:4:4)
│
├── Register Decode ────────────────────────────────────────────
│   ├─ s_offset       = registers_in(0) → brightness (Offset)
│   ├─ s_hue_1        = registers_in(1) → harmonic 1 offset
│   ├─ s_hue_2        = registers_in(2) → harmonic 2 offset
│   ├─ s_span         = registers_in(3) → contrast (Span)
│   ├─ s_hue_3        = registers_in(4) → harmonic 3 offset
│   ├─ s_hue_4        = registers_in(5) → harmonic 4 offset
│   ├─ s_invert_span  = registers_in(6)(0) → base inversion
│   ├─ s_invert_hue_1 = registers_in(7)(0) → harmonic 1 invert
│   ├─ s_invert_hue_2 = registers_in(8)(0) → harmonic 2 invert
│   ├─ s_invert_hue_3 = registers_in(9)(0) → harmonic 3 invert
│   ├─ s_invert_hue_4 = registers_in(10)(0) → harmonic 4 invert
│   └─ s_threshold    = registers_in(11) → key threshold
│
├── Stage 1: proc_amp_u ────────────────────────────────────────
│   └─ result = (Y_in - 0.5) × Span + Offset
│      (contrast 0×–2×, brightness -0.5–+0.5, clamped 0–1023)
│
├── Stage 2: Base Inversion ────────────────────────────────────
│   └─ if Invert Span: s_base = NOT(s_contrast_result)
│      else: s_base = s_contrast_result
│
├── Stage 3: Cascaded Frequency Doublers ───────────────────────
│   ├─ doubler_2x:  fold(s_base)           → s_doubler_2x_out
│   ├─ doubler_4x:  fold(s_doubler_2x_out) → s_doubler_4x_out
│   ├─ doubler_8x:  fold(s_doubler_4x_out) → s_doubler_8x_out
│   └─ doubler_16x: fold(s_doubler_8x_out) → s_doubler_16x_out
│   Each: if input < midpoint: out = input × 2
│         else: out = MAX - (input - midpoint) × 2
│         (2 clock latency per stage)
│
├── Stage 4: Per-Harmonic Offset + Inversion ───────────────────
│   ├─ harm_1 = (invert? NOT(2x)  : 2x)  + Hue 1  (wrapping)
│   ├─ harm_2 = (invert? NOT(4x)  : 4x)  + Hue 2  (wrapping)
│   ├─ harm_3 = (invert? NOT(8x)  : 8x)  + Hue 3  (wrapping)
│   └─ harm_4 = (invert? NOT(16x) : 16x) + Hue 4  (wrapping)
│
├── Stage 5: Output Mapping + Threshold Key ────────────────────
│   ├─ Y_out = (harm_1 + harm_2) >> 1  (average)
│   ├─ U_out = harm_3
│   ├─ V_out = harm_4
│   └─ if Y_out < threshold:
│        Y=0, U=512, V=512  (black + neutral chroma)
│
└── Sync Passthrough ───────────────────────────────────────────
    └─ hsync_n, vsync_n, field_n, avid passed through directly
```

The pipeline is notable for its cascaded topology: each frequency doubler feeds directly into the next, so the 16× stage operates on data that has already been folded three times. This means that the 16× harmonic is not simply the original input at sixteen times its frequency — it is the original input folded, then that fold folded again, then folded again, then folded once more. Each successive fold re-creates peak boundaries from the previous stage's output, producing increasingly intricate cusp patterns. The proc_amp conditioning at the input is critical because it determines how many fold boundaries the signal crosses: a signal that spans the full 0–1023 range crosses every fold midpoint, generating maximum harmonic content, while a narrow-range signal near midpoint may not cross a single fold boundary and passes through the entire doubler chain essentially unchanged.

The separation of harmonics across Y, U, and V channels creates the program's characteristic chromatic interference. Because each channel carries a different harmonic frequency, the spatial alignment of peaks and troughs varies across the color channels. Where harmonic 3 (U) peaks while harmonic 4 (V) troughs, the chrominance shifts toward one hue; where they align, it shifts toward another. The Hue offset parameters rotate this alignment, allowing you to sweep through the interference pattern without changing the underlying harmonic structure. The threshold keyer operates only on the averaged Y output, so it carves out darkness-based shapes that respect the luminance pattern while ignoring the chrominance content entirely.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Offset
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Controls the brightness offset applied to the input luma before the frequency doubler chain. At the midpoint (0%), the signal passes through the proc amp unchanged relative to its contrast-adjusted center. Sweeping toward positive values lifts the entire signal upward, pushing more of it above the doubler midpoints and changing which fold boundaries are crossed. Sweeping negative pulls the signal down, creating the complementary set of fold crossings. Small adjustments produce dramatic changes in the harmonic output because the proc amp operates before the cascaded doublers — a shift of even a few percent at the input cascades through four folding stages, rearranging every petal in the interference pattern.

---

#### Knob 2 — Hue 1
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the wrapping brightness offset for harmonic 1, the 2× frequency-doubled signal. At zero, the first doubler's output passes directly to the Y averaging stage without modification. Increasing the offset shifts the entire 2× waveform upward in the unsigned domain, wrapping around at 1023 to create a rotational sweep through the interference pattern. Because harmonic 1 contributes directly to Y output (averaged with harmonic 2), sweeping Hue 1 visibly rotates the coarsest luminance structure of the petal pattern. The offset is applied after the optional inversion toggle, so the combination of inversion plus swept offset produces a continuously evolving mirror-image pattern.

---

#### Knob 3 — Hue 2
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the wrapping brightness offset for harmonic 2, the 4× frequency-doubled signal. This harmonic shares the Y output channel with harmonic 1 via averaging, so its offset interacts directly with Hue 1 to determine the composite luminance pattern. When both offsets are swept simultaneously in opposite directions, the averaging creates a moire-like beat pattern between the 2× and 4× harmonics. When swept together, the luminance pattern shifts uniformly without changing its internal structure. Setting Hue 2 to its midpoint while leaving Hue 1 at zero creates a half-period phase offset between the two Y-channel harmonics, emphasizing even-order peaks.

---

#### Knob 4 — Span
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the contrast applied to the input luma by the proc amp stage. This determines the amplitude of the signal entering the frequency doubler chain. At zero, the input is compressed to a constant near the brightness offset — no folding occurs and the output is a flat field. At the midpoint (100%), the input passes through at unity gain. At maximum (200%), the input is stretched to double its original dynamic range, saturating at 0 and 1023, and every fold boundary in all four doubler stages is fully exercised. Span is the master gain control for the entire harmonic series: increasing it adds energy to all four harmonics simultaneously, producing increasingly dense petal formations. Reducing it strips away the higher harmonics first, leaving only the coarsest folds of the 2× stage.

---

#### Knob 5 — Hue 3
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the wrapping brightness offset for harmonic 3, the 8× frequency-doubled signal. This harmonic is mapped directly to the U chroma channel, so sweeping Hue 3 rotates the chroma interference in the blue-yellow axis. Because the chroma channel operates at a higher harmonic frequency than the Y channel, small offset changes produce rapid spectral banding — fine stripes of color that shift across the image as the knob turns. The visual effect is a hue rotation that operates at a finer spatial grain than the luma pattern, creating the characteristic "petal within petal" structure that gives the program its name.

---

#### Knob 6 — Hue 4
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the wrapping brightness offset for harmonic 4, the 16× frequency-doubled signal. This is the highest-frequency harmonic in the chain, mapped directly to the V chroma channel. Because 16× represents the fourth cascade of folding, even small input features are broken into many fine oscillations. Sweeping Hue 4 shifts these micro-oscillations in the red-cyan chroma axis, producing extremely fine spectral banding that animates rapidly with knob movement. At moderate Span settings, the 16× harmonic may be barely visible as a subtle texture; at high Span, it creates an intense chromatic shimmer across the entire image.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Invert Span** | Off | On |
| **8 — Invert Hue 1** | Off | On |
| **9 — Invert Hue 2** | Off | On |
| **10 — Invert Hue 3** | Off | On |
| **11 — Invert Hue 4** | Off | On |

The five toggles form a binary inversion matrix across the harmonic chain. Toggle 7 inverts the conditioned input before the doubler cascade, while toggles 8 through 11 each invert one of the four harmonics independently. Because harmonics 1 and 2 are averaged to form the Y output, inverting one but not the other creates destructive interference — narrow contour lines where they disagree. Harmonics 3 and 4 map directly to U and V chroma channels, so their inversion flips the blue-yellow and red-cyan axes respectively. The five switches together provide 32 binary combinations, each producing a distinct petal geometry and color mapping from the same input signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the threshold level for the output key effect. At zero, no keying occurs and all computed pixels reach the output regardless of their Y value. As the threshold increases, pixels whose averaged harmonic Y value falls below the threshold are forced to black with neutral chroma (Y=0, U=512, V=512). At moderate thresholds, this carves out the darker valleys of the petal pattern, leaving only the bright ridges as floating color structures against a black background. At maximum threshold, nearly all output is keyed to black except the very brightest harmonic peaks. The key operates purely on the computed Y channel — the chroma values of keyed pixels are neutralized to prevent color fringing at the key edge.

---

## Guided Exercises

These three exercises progress from observing the raw harmonic structure through shaping the chromatic interference to sculpting hard-edged petal geometries using the threshold key. Each builds on the previous, revealing how the cascaded frequency doublers interact with offset, inversion, and keying to produce the corolla patterns.

### Exercise 1: Harmonic Anatomy

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: corollas_source1_boat, after: corollas_ex1_s1 },
    { label: "Dog", before: corollas_source2_dog, after: corollas_ex1_s2 },
    { label: "Turtle", before: corollas_source3_turtle, after: corollas_ex1_s3 },
    { label: "Pattern", before: corollas_source4_pattern, after: corollas_ex1_s4 },
    { label: "Girl", before: corollas_source5_girl, after: corollas_ex1_s5 },
    { label: "Wood", before: corollas_source6_wood, after: corollas_ex1_s6 },
  ]}
/>
*Harmonic Anatomy — simulated result across source images.*
**Source**: A smooth horizontal or diagonal gradient — a ramp test pattern or a gently lit face works well. The smoother the input, the cleaner the individual harmonics will be.

**Objective**: Observe the four frequency-doubled harmonics individually and understand how Span controls harmonic complexity.

1. Set Span to about 50% and Offset to 0%. Observe the basic folded pattern in the output.
2. Set all Hue controls to 0% and all Invert toggles to Off. Set Threshold to 0%.
3. Slowly increase Span from 0% toward 200%. Watch as the petal structure grows from a simple single fold to densely packed multi-fold interference.
4. At moderate Span (~80%), sweep Hue 1 from 0% to 100%. Observe the coarsest luminance structure rotating.
5. Return Hue 1 to 0% and sweep Hue 3. Watch the U chroma channel shift independently of Y.
6. Note how higher harmonics (Hue 3, Hue 4) produce finer spatial banding than lower ones (Hue 1, Hue 2).

**Key concepts**: Span is the master gain for all harmonics, lower harmonics produce coarser patterns, chroma and luma channels carry independent harmonics at different spatial frequencies, the proc amp input stage determines how many fold boundaries are crossed.

---

### Exercise 2: Chromatic Interference

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: corollas_source1_boat, after: corollas_ex2_s1 },
    { label: "Dog", before: corollas_source2_dog, after: corollas_ex2_s2 },
    { label: "Turtle", before: corollas_source3_turtle, after: corollas_ex2_s3 },
    { label: "Pattern", before: corollas_source4_pattern, after: corollas_ex2_s4 },
    { label: "Girl", before: corollas_source5_girl, after: corollas_ex2_s5 },
    { label: "Wood", before: corollas_source6_wood, after: corollas_ex2_s6 },
  ]}
/>
*Chromatic Interference — simulated result across source images.*
**Source**: A portrait or scene with a range of skin tones and midtones — the frequency doublers will fragment these tones into colored petal structures.

**Objective**: Create rich chromatic interference by offsetting and inverting individual harmonics against each other.

1. Set Span to ~120% and Offset to 0% for full harmonic excitation.
2. Sweep Hue 3 to ~60% to shift the U chroma pattern.
3. Sweep Hue 4 to ~30% to offset the V chroma in the opposite direction.
4. Toggle Invert Hue 1 On. Notice how the luminance pattern dramatically restructures as harmonic 1 mirrors against harmonic 2 in the Y average.
5. Toggle Invert Hue 3 On. The U chroma band now complements the V band, producing a full chromatic rotation.
6. Sweep Offset slowly — watch the entire interference pattern shift as the input driving point changes.

**Key concepts**: Per-harmonic inversion creates destructive interference within shared channels, offsetting U and V harmonics in opposite directions produces complementary chroma banding, the Offset parameter shifts the input driving point and cascades through all four doublers.

---

### Exercise 3: Threshold-Keyed Petals

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: corollas_source1_boat, after: corollas_ex3_s1 },
    { label: "Dog", before: corollas_source2_dog, after: corollas_ex3_s2 },
    { label: "Turtle", before: corollas_source3_turtle, after: corollas_ex3_s3 },
    { label: "Pattern", before: corollas_source4_pattern, after: corollas_ex3_s4 },
    { label: "Girl", before: corollas_source5_girl, after: corollas_ex3_s5 },
    { label: "Wood", before: corollas_source6_wood, after: corollas_ex3_s6 },
  ]}
/>
*Threshold-Keyed Petals — simulated result across source images.*
**Source**: A high-contrast image or text card — strong edges will produce well-defined fold boundaries that survive the threshold key.

**Objective**: Use the threshold keyer to sculpt the harmonic output into floating neon-like petal structures on a black background.

1. Set Span to ~150% for aggressive folding and Offset to about 10%.
2. Set Hue 1 to ~20%, Hue 2 to ~40%, Hue 3 to ~50%, Hue 4 to ~70% to distribute offsets across all harmonics.
3. Slowly raise Threshold from 0% to ~50%. Watch as the dark valleys of the petal pattern are keyed to black, leaving bright ridges.
4. Continue raising Threshold to ~75%. Only the brightest harmonic peaks survive — thin, neon-like lines.
5. Toggle Invert Span On. The key pattern inverts dramatically as the folding geometry reverses.
6. Try Threshold at ~90% with various Hue offset combinations to find minimal, abstract petal structures.

**Key concepts**: Threshold keying removes the darkest regions of the harmonic pattern, creating hard-edged structures from soft interference. Pre-inversion via Invert Span completely rearranges which peaks survive the threshold. Hue offsets shift the surviving ridge positions. At high threshold, only the narrowest harmonic peaks persist.

---


## Tips

- **Span is the master control**: Before adjusting any Hue offset or inversion, use Span to set the overall harmonic density. Low Span = gentle folds with coarse petals. High Span = dense, fine-grained interference.
- **Start with Offset at center**: The 0% Offset position centers the proc amp output. Sweep Offset after setting Span to shift the pattern without changing its density — small moves cascade dramatically through four doubler stages.
- **Hue offsets for color animation**: Slowly sweeping a single Hue knob animates the interference pattern. Sweeping Hue 3 or Hue 4 produces the most vivid chromatic animation since they drive chroma channels directly.
- **Inversion pairs for destructive interference**: Inverting one Y-channel harmonic but not the other creates narrow contour lines where the two averaged harmonics cancel. This is especially effective for isolating boundary structures.
- **Threshold as a carving tool**: Use Threshold at 30–50% to remove dark valleys and leave bright harmonic ridges floating on black. This converts the smooth interference pattern into hard-edged abstract geometry.
- **Combine Invert Span with high Threshold**: Toggling Invert Span at moderate-to-high Threshold completely reshapes the surviving petal geometry — a performance technique for instant visual transformation.
- **Low-contrast sources for clean harmonics**: Smooth gradients and soft-lit scenes produce the cleanest petal structures because each tonal region maps to a consistent set of fold crossings. High-contrast sources fragment the pattern into noisy interference.
- **16× harmonic as subtle texture**: At moderate Span, the 16× harmonic (Hue 4 / V channel) produces very fine banding that reads as texture rather than structure. Use it sparingly for chromatic shimmer on top of the coarser harmonic structure.

---

## Glossary

| Term | Definition |
|------|------------|
| **Corolla** | The collective term for the petals of a flower; used here as a metaphor for the concentric folded waveforms produced by cascaded frequency doubling. |
| **Destructive interference** | The cancellation that occurs when two waveforms with opposite polarity are combined, producing near-zero values where one peaks and the other troughs. |
| **Fold boundary** | The midpoint value (512 in 10-bit) where the frequency doubler reverses direction. The number of fold boundaries crossed by the input signal determines the harmonic complexity of the output. |
| **Frequency doubler** | A module that folds a signal at its midpoint, converting a ramp to a triangle wave and doubling the spatial frequency. Cascading four doublers produces 2×, 4×, 8×, and 16× harmonics. |
| **Harmonic** | An integer multiple of a fundamental frequency. In Corollas, the fundamental is the input luma after proc amp conditioning, and the harmonics are successive frequency-doubled versions at 2×, 4×, 8×, and 16×. |
| **Phase offset** | A shift in the alignment of a periodic waveform, controlled here by the Hue brightness offset parameters. Wrapping addition rotates the waveform's phase without changing its frequency. |
| **Proc amp** | Processing amplifier; applies contrast (gain around midpoint) and brightness (DC offset) to condition the input signal before harmonic generation. |
| **Threshold key** | A gating function that forces pixels to black when their luminance falls below a configurable level, creating hard-edged cutouts from the smooth harmonic pattern. |
| **Wrapping offset** | An unsigned addition that overflows at the 10-bit boundary (1024), creating a circular shift rather than a clamped shift. Sweeping a wrapping offset through its full range returns the pattern to its starting position. |
| **YUV** | A color space separating luminance (Y) from chrominance (U, V); the native pixel format of the Videomancer processing pipeline. Corollas maps independent harmonics to each channel. |

---
