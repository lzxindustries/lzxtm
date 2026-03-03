---
draft: true
sidebar_position: 92
slug: /instruments/videomancer/dropout
title: "Dropout"
image: /img/instruments/videomancer/dropout/dropout_hero_s1.png
description: "Every VHS cassette is a battlefield between the recording and time itself."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import dropout_source1_runner from '/img/instruments/videomancer/dropout/dropout_source1_runner.png';
import dropout_source2_boat from '/img/instruments/videomancer/dropout/dropout_source2_boat.png';
import dropout_source3_elephant from '/img/instruments/videomancer/dropout/dropout_source3_elephant.png';
import dropout_source4_pattern from '/img/instruments/videomancer/dropout/dropout_source4_pattern.png';
import dropout_source5_girl from '/img/instruments/videomancer/dropout/dropout_source5_girl.png';
import dropout_source6_wood from '/img/instruments/videomancer/dropout/dropout_source6_wood.png';
import dropout_hero_s1 from '/img/instruments/videomancer/dropout/dropout_hero_s1.png';
import dropout_hero_s2 from '/img/instruments/videomancer/dropout/dropout_hero_s2.png';
import dropout_hero_s3 from '/img/instruments/videomancer/dropout/dropout_hero_s3.png';
import dropout_hero_s4 from '/img/instruments/videomancer/dropout/dropout_hero_s4.png';
import dropout_hero_s5 from '/img/instruments/videomancer/dropout/dropout_hero_s5.png';
import dropout_hero_s6 from '/img/instruments/videomancer/dropout/dropout_hero_s6.png';
import dropout_ex1_s1 from '/img/instruments/videomancer/dropout/dropout_ex1_s1.png';
import dropout_ex1_s2 from '/img/instruments/videomancer/dropout/dropout_ex1_s2.png';
import dropout_ex1_s3 from '/img/instruments/videomancer/dropout/dropout_ex1_s3.png';
import dropout_ex1_s4 from '/img/instruments/videomancer/dropout/dropout_ex1_s4.png';
import dropout_ex1_s5 from '/img/instruments/videomancer/dropout/dropout_ex1_s5.png';
import dropout_ex1_s6 from '/img/instruments/videomancer/dropout/dropout_ex1_s6.png';
import dropout_ex2_s1 from '/img/instruments/videomancer/dropout/dropout_ex2_s1.png';
import dropout_ex2_s2 from '/img/instruments/videomancer/dropout/dropout_ex2_s2.png';
import dropout_ex2_s3 from '/img/instruments/videomancer/dropout/dropout_ex2_s3.png';
import dropout_ex2_s4 from '/img/instruments/videomancer/dropout/dropout_ex2_s4.png';
import dropout_ex2_s5 from '/img/instruments/videomancer/dropout/dropout_ex2_s5.png';
import dropout_ex2_s6 from '/img/instruments/videomancer/dropout/dropout_ex2_s6.png';
import dropout_ex3_s1 from '/img/instruments/videomancer/dropout/dropout_ex3_s1.png';
import dropout_ex3_s2 from '/img/instruments/videomancer/dropout/dropout_ex3_s2.png';
import dropout_ex3_s3 from '/img/instruments/videomancer/dropout/dropout_ex3_s3.png';
import dropout_ex3_s4 from '/img/instruments/videomancer/dropout/dropout_ex3_s4.png';
import dropout_ex3_s5 from '/img/instruments/videomancer/dropout/dropout_ex3_s5.png';
import dropout_ex3_s6 from '/img/instruments/videomancer/dropout/dropout_ex3_s6.png';

# Dropout

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: dropout_source1_runner, after: dropout_hero_s1 },
    { label: "Boat", before: dropout_source2_boat, after: dropout_hero_s2 },
    { label: "Elephant", before: dropout_source3_elephant, after: dropout_hero_s3 },
    { label: "Pattern", before: dropout_source4_pattern, after: dropout_hero_s4 },
    { label: "Girl", before: dropout_source5_girl, after: dropout_hero_s5 },
    { label: "Wood", before: dropout_source6_wood, after: dropout_hero_s6 },
  ]}
/>
*Dropout simulating VHS tape degradation with tracking error bands, dropout streaks, time-base jitter, and chroma-under color bleed.*

---

## Overview

Every VHS cassette is a battlefield between the recording and time itself. Oxide flakes off the tape. The rubber pinch roller wears unevenly. The spinning head drum drifts a fraction of a degree from where it was when the recording was made. Dropout recreates these analog indignities with obsessive fidelity — not as a filter preset but as a collection of independent degradation mechanisms that interact exactly the way they do on real tape.

The program chains six artifact generators together — horizontal time-base jitter from capstan wobble, a rolling tracking-error noise band, head-switching noise at the bottom of each field, random dropout streaks from tape coating damage, IIR chroma blur simulating color-under bandwidth limitation, and chroma phase noise from azimuth error. Each mechanism operates on its own LFSR-driven noise source and has its own amplitude control. At conservative settings, Dropout adds subtle analog warmth — a gentle horizontal shimmer, faint color softening, occasional dropout flickers. At extreme settings, the image tears apart into the unmistakable chaos of a played-to-death rental tape.

The name is borrowed directly from the language of magnetic recording engineers, where a "dropout" is a momentary loss of signal caused by a physical defect in the tape's magnetic coating — a scratch, a crease, a speck of dust trapped between the oxide layer and the spinning head.

---

## Background

### Helical Scan and the VHS Format

VHS records video using a helical-scan head drum — a metal cylinder roughly 62 mm in diameter that spins at 1,800 RPM (NTSC) or 1,500 RPM (PAL). The tape wraps around the drum at a slight angle, so each revolution of the drum traces a diagonal stripe across the tape. Each stripe holds one field of video (half a frame). The heads must make contact with the tape at exactly the right angle and exactly the right speed to read back the signal. Any deviation — from wear, misalignment, or tape stretch — produces artifacts.

### Tracking Errors

"Tracking" refers to the alignment between the spinning head's path and the diagonal stripes on the tape. When the tracking is off, the head partially reads one stripe and partially reads the adjacent stripe, producing a horizontal band of noise that sweeps vertically through the image. On a real VCR, the tracking control adjusts a delay that shifts the head's timing. Dropout's Tracking knob controls the scroll speed of this noise band, and the Track Band toggle enables or disables it entirely.

### Time-Base Correctors and TBC Error

The tape transport pulls tape past the head drum at approximately 2.339 cm/s (SP mode). "Approximately" is the key word — the rubber capstan that drives the tape stretches, slips, and wobbles. These speed variations cause each scan line to arrive slightly early or late, which appears as horizontal jitter. Professional facilities used time-base correctors (TBCs) to lock each line to a stable reference. Consumer decks had no TBC, so the jitter was always present. Dropout's TBC Error control simulates capstan wobble by reading each line from a BRAM line buffer at a jitter-offset address computed from a smoothed LFSR.

### Chroma-Under Encoding

VHS uses a technique called "color-under" recording. The color information is downconverted to a low carrier frequency (~629 kHz) and recorded beneath the luminance signal. This carrier has extremely limited bandwidth compared to the luma — roughly 400 kHz of chroma bandwidth versus 3 MHz of luma bandwidth. The result is soft, smeared color with reduced saturation. Dropout's Chroma BW control simulates this by applying a single-pole IIR low-pass filter to the U and V channels, with the filter's alpha (cutoff) controlled by the knob.

### Head Switching Noise

At the bottom of each video field, the active head finishes its diagonal pass across the tape and the next head takes over. This handoff — the "head switch" — produces a brief burst of noise at the very bottom of the frame, typically visible as a bright, jittery bar. Most monitors overscan to hide this region, but on some displays and capture setups, the head-switch noise is clearly visible. Dropout places LFSR-generated noise in a configurable band at the bottom of the active picture.

### Tape Wear and Dropout Streaks

Physical damage to the tape's magnetic oxide coating causes momentary signal loss — a "dropout." On playback, a dropout appears as a brief horizontal streak of white noise or, on more sophisticated decks, a held-previous-line replacement where the deck substitutes the last good line. Dropout models both behaviors: the Drop Mode toggle selects between white streaks and hold-previous, while the Wear knob controls how frequently dropouts trigger. Internally, a 16-bit Galois LFSR fires a dropout burst when its upper bits fall below the Wear threshold, with the burst length randomized from the LFSR's lower bits.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y/U/V Write ────────────────────────────────────────────────
│   └─ 1. Line Buffer Write   (3× BRAM, write at h_count)
│
├── Jitter Compute ─────────────────────────────────────────────
│   ├─ 2. LFSR Jitter         (16-bit Galois LFSR, per-line step)
│   ├─ 3. IIR Smooth          (7/8 feedback → slow capstan wobble)
│   └─ 4. Read Offset         (h_count + jitter × TBC Error → BRAM addr)
│
├── Chroma Processing ──────────────────────────────────────────
│   ├─ 5. Chroma IIR Blur     (single-pole LP on U/V, alpha=Chroma BW)
│   └─ 6. Phase Noise         (LFSR × Phase Noise → U/V cross-offset)
│
├── Artifact Overlay ───────────────────────────────────────────
│   ├─ 7. Luma Noise          (LFSR low 4 bits added to Y, optional)
│   ├─ 8. Chroma Kill         (force U/V = 512, optional)
│   ├─ 9. Head Switch Bar     (LFSR noise replaces Y at bottom of frame)
│   ├─ 10. Tracking Band      (LFSR noise added to Y in rolling band)
│   └─ 11. Dropout Streaks    (white or hold-previous, LFSR-triggered)
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock shift register (hsync, vsync, field, Y/U/V)
│
└── Mix ────────────────────────────────────────────────────────
    └─ 12. Interpolator (3×)   (dry/wet crossfade, Mix fader)
```

The pipeline has two critical ordering constraints. First, the line buffer write and jitter-offset read must occur on consecutive clocks so the read address reflects the current line's jitter — this is what creates the per-line horizontal displacement that simulates capstan wobble. Second, the artifact overlays (head switch, tracking band, dropout) are applied *after* chroma processing, so a dropout streak replaces the already-blurred chroma with either white or held-previous values, matching real tape behavior where a dropout obliterates the entire recovered signal, not just the raw recording.

The chroma IIR filter resets its state to mid-scale (512) at each line start. This prevents inter-line accumulation that would cause color smearing across scan lines — matching the behavior of a real VHS chroma demodulator that locks to the color-under carrier independently on each line.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Tracking
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the scroll speed of the tracking error noise band. At minimum, the band is nearly stationary — a fixed horizontal stripe of noise parked at one vertical position. As you increase the control, the band sweeps faster through the frame, producing the classic "rolling bar" of a misaligned VCR. The tracking value also feeds the speed-error accumulator when Speed Error is enabled, coupling the tracking scroll rate to a slow vertical roll of the entire image.

---

#### Knob 2 — Wear
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls dropout density — how frequently the LFSR triggers a new dropout burst. At minimum, dropouts are rare, appearing as occasional single-pixel flickers. At maximum, the image is riddled with horizontal streaks, approaching the look of a severely damaged tape where large sections of oxide have separated from the base film. The burst length of each dropout is randomized independently from the LFSR's lower 8 bits, so even at moderate density settings, you get a natural mix of short flickers and longer streaks.

---

#### Knob 3 — TBC Error
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the amplitude of horizontal time-base jitter. The jitter source is a 16-bit LFSR smoothed through a 7/8 IIR filter to produce the slow, undulating wobble characteristic of capstan instability (rather than the per-pixel randomness of white noise). At minimum, lines are rock-solid. At moderate values, edges shimmer with a gentle horizontal displacement that varies slowly from line to line. At maximum, the image tears horizontally with each scan line shifted significantly from its neighbors.

---

#### Knob 4 — Chroma BW
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the chroma bandwidth — the cutoff frequency of the IIR low-pass filter applied to U and V channels. At maximum (fully clockwise), the filter alpha is high and the chroma passes through with minimal blurring. As you decrease the control, the alpha drops and colors smear horizontally, replicating the ~400 kHz bandwidth limitation of VHS color-under recording. At minimum, the chroma is so heavily filtered that only the broadest color regions survive, with fine color detail replaced by a uniform average.

---

#### Knob 5 — Phase Noise
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the amplitude of per-line chroma phase noise. On real VHS, the azimuth angle of the spinning head varies slightly from line to line, causing the recovered chroma carrier to shift in phase. This appears as a subtle, line-by-line color wobble — hues shift randomly on each scan line. At minimum, the chroma phase is stable. At moderate values, you see the characteristic VHS "rainbow shimmer" on saturated edges. At maximum, the U and V channels are heavily displaced, producing psychedelic color fringing.

---

#### Knob 6 — Head Switch
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the height of the head-switching noise bar at the bottom of the active picture. At minimum, the bar is absent (zero lines). As you increase the control, the noise bar extends upward from the bottom of the frame, filling the head-switch region with LFSR-generated noise. The noise replaces the Y channel entirely (with U/V forced to mid-scale), replicating the achromatic, high-amplitude noise burst that appears during the head transition.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Track Band** | Off | On |
| **8 — Drop Mode** | White | Hold |
| **9 — Chroma Kill** | Off | On |
| **10 — Speed Error** | Off | On |
| **11 — Luma Noise** | Off | On |

The five toggles control independent artifact mechanisms. Track Band enables the rolling noise bar. Drop Mode selects between white streaks (simulating a basic deck with no dropout compensation) and hold-previous (simulating a deck with dropout compensator that repeats the last good line). Chroma Kill forces monochrome output. Speed Error introduces a slow vertical roll from capstan speed drift. Luma Noise adds a fine grain overlay. None of the toggles interact with each other — each enables or disables its respective processing stage independently.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the processed (degraded) signal and the original clean input. At 100%, the output is fully degraded. At 0%, the output is the clean input with no artifacts. Intermediate positions blend the two, which can be used to dial in a subtle tape coloration without committing to full degradation. Because there is no bypass toggle on this program, the Mix fader is the only way to reduce the effect to zero.

---

## Guided Exercises

These exercises progress from individual artifact mechanisms to full tape degradation composites. Each isolates a specific VHS failure mode before combining them into a convincing analog decay aesthetic.

### Exercise 1: Capstan Wobble and Time-Base Jitter

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: dropout_source1_runner, after: dropout_ex1_s1 },
    { label: "Boat", before: dropout_source2_boat, after: dropout_ex1_s2 },
    { label: "Elephant", before: dropout_source3_elephant, after: dropout_ex1_s3 },
    { label: "Pattern", before: dropout_source4_pattern, after: dropout_ex1_s4 },
    { label: "Girl", before: dropout_source5_girl, after: dropout_ex1_s5 },
    { label: "Wood", before: dropout_source6_wood, after: dropout_ex1_s6 },
  ]}
/>
*Capstan Wobble and Time-Base Jitter — simulated result across source images.*
**Source**: Footage with strong vertical lines — architecture, text overlays, or a vertical stripe test pattern.

**Objective**: Understand how the TBC Error control creates horizontal jitter that simulates capstan instability.

1. **Isolate jitter**: Set TBC Error to ~40%. Leave all other knobs at minimum and all toggles off.
2. **Observe edges**: Watch vertical lines in the source shimmer horizontally. The displacement changes slowly from line to line because of the IIR smoothing.
3. **Increase amplitude**: Sweep TBC Error to ~80%. The shimmer becomes a pronounced tear — each scan line visibly displaced from its neighbors.
4. **Add chroma blur**: Now bring Chroma BW down to ~30%. The color softens and smears behind the jittered luma edges, recreating the dual-bandwidth look of real VHS.
5. **Add grain**: Enable Luma Noise (Toggle 11). A fine grain appears over the jittered image.
6. **Mix down**: Use the Mix fader to find a level where the jitter is present but not overwhelming.

**Key concepts**: Time-base jitter is per-line horizontal displacement from LFSR noise smoothed through an IIR filter, the smoothing creates slow wobble rather than per-pixel randomness, chroma blur and jitter together recreate the dual-bandwidth signature of VHS

---

### Exercise 2: Dropout Streaks and Tracking Bands

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: dropout_source1_runner, after: dropout_ex2_s1 },
    { label: "Boat", before: dropout_source2_boat, after: dropout_ex2_s2 },
    { label: "Elephant", before: dropout_source3_elephant, after: dropout_ex2_s3 },
    { label: "Pattern", before: dropout_source4_pattern, after: dropout_ex2_s4 },
    { label: "Girl", before: dropout_source5_girl, after: dropout_ex2_s5 },
    { label: "Wood", before: dropout_source6_wood, after: dropout_ex2_s6 },
  ]}
/>
*Dropout Streaks and Tracking Bands — simulated result across source images.*
**Source**: A slowly moving camera shot or static scene with moderate detail.

**Objective**: Explore the two horizontal-bar artifacts — random dropout streaks and the periodic tracking error band.

1. **Dropout streaks**: Set Wear to ~30%. Set Drop Mode to White. Watch brief white streaks flash across random horizontal positions. Note how burst lengths vary.
2. **Hold mode**: Switch Drop Mode to Hold. The streaks now show frozen copies of earlier pixel values — less visually aggressive but still clearly damaged.
3. **High wear**: Increase Wear to ~70%. The streaks become dense and frequent, approaching the look of severely damaged tape.
4. **Tracking band**: Enable Track Band (Toggle 7). Set Tracking to ~30%. A horizontal noise band begins sweeping vertically through the image.
5. **Speed sweep**: Increase Tracking to ~80%. The band scrolls faster. Within the band, color is killed and luma is replaced with additive LFSR noise.
6. **Combine**: Leave both dropouts and tracking band active. Add moderate TBC Error (~25%) and reduce Chroma BW to ~50%.

**Key concepts**: Dropout streaks are LFSR-triggered bursts with random length, the tracking band is a fixed-width noise zone that scrolls vertically, white-streak and hold-previous are two distinct dropout compensation strategies from real VCR hardware

---

### Exercise 3: Full Tape Degradation

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: dropout_source1_runner, after: dropout_ex3_s1 },
    { label: "Boat", before: dropout_source2_boat, after: dropout_ex3_s2 },
    { label: "Elephant", before: dropout_source3_elephant, after: dropout_ex3_s3 },
    { label: "Pattern", before: dropout_source4_pattern, after: dropout_ex3_s4 },
    { label: "Girl", before: dropout_source5_girl, after: dropout_ex3_s5 },
    { label: "Wood", before: dropout_source6_wood, after: dropout_ex3_s6 },
  ]}
/>
*Full Tape Degradation — simulated result across source images.*
**Source**: Any video footage — the more recognizable the subject, the more dramatic the degradation.

**Objective**: Combine all degradation mechanisms into a convincing worn-tape composite.

1. **Base degradation**: Set TBC Error ~30%, Chroma BW ~40%, Phase Noise ~20%. This establishes the fundamental VHS character — jittery, soft color, slight hue wobble.
2. **Tracking**: Enable Track Band, set Tracking to ~15%. A slow-rolling noise bar sweeps through the image.
3. **Dropouts**: Set Wear ~25%, Drop Mode to Hold. Occasional held-line streaks appear.
4. **Head switch**: Set Head Switch to ~40%. A noise bar appears at the bottom of the frame.
5. **Speed error**: Enable Speed Error (Toggle 10). The image begins to roll slowly vertically.
6. **Luma noise**: Ensure Luma Noise is on. The fine grain completes the analog noise floor.
7. **Final mix**: Adjust Mix to taste — try ~85% for a tape that's been played many times, or ~50% for a subtle vintage overlay.

**Key concepts**: VHS degradation is the sum of many independent failure modes — capstan wobble, head alignment, tape damage, bandwidth limitation, phase instability, and amplifier noise, each degradation mechanism operates on a different axis (horizontal jitter, vertical band, random burst, frequency response, phase rotation, additive noise)

---


## Tips

- **Start with TBC Error and Chroma BW**: These two controls establish the fundamental VHS character — horizontal wobble and soft color. Everything else is secondary damage on top of this base.
- **Hold mode is more subtle than White**: Hold-previous dropout streaks blend into the image and can be almost invisible on static scenes. White streaks are more dramatic and visible.
- **Low Tracking = slow roll**: The tracking-band scroll speed and speed-error roll rate are both proportional to the Tracking knob. Very low values create an almost-imperceptible creep that builds atmosphere without obvious motion.
- **Head Switch is overscan**: Most displays overscan the bottom few lines, so the head-switch bar may not be visible at low settings. Increase the control to push the noise into the visible area.
- **Chroma BW at maximum is nearly transparent**: At full clockwise, the IIR alpha is high enough that chroma passes through with minimal filtering. This is useful for isolating other artifacts without the color softening.
- **Mix is your only bypass**: Unlike most programs, Dropout has no bypass toggle. The Mix fader at 0% gives you clean output; at 100%, full degradation. Use intermediate positions for subtle vintage warmth.
- **Feedback loops**: Routing Dropout's output back to its input accumulates degradation — jitter stacks on jitter, dropouts hit already-damaged regions, and chroma blur compounds. This quickly produces an extreme multi-generation-dub aesthetic.
- **Combine with Cascade**: Dropout into Cascade creates the look of a VHS tape played through a feedback monitor — tracking errors and dropout streaks echo and trail across the screen.

---

## Glossary

| Term | Definition |
|------|------------|
| **Azimuth** | The angle between the recording head gap and the tape track. Misalignment causes phase errors in the recovered chroma signal. |
| **BRAM** | Block RAM; dedicated memory within the FPGA used here for line buffers that enable per-line horizontal displacement. |
| **Capstan** | The motorized spindle that pulls tape past the head drum at a controlled speed. Wobble or slip produces time-base jitter. |
| **Chroma-Under** | VHS color recording technique that downconverts chrominance to a low carrier frequency (~629 kHz), severely limiting color bandwidth. |
| **Dropout** | A momentary loss of signal caused by a physical defect (scratch, oxide flake, debris) on the tape's magnetic coating. |
| **Galois LFSR** | A linear feedback shift register using XOR taps at the output, providing a maximal-length pseudo-random sequence for noise generation. |
| **Head Drum** | The spinning cylinder containing the video read/write heads in a helical-scan VCR. Rotation at 1800 RPM (NTSC) or 1500 RPM (PAL). |
| **Head Switch** | The point at the bottom of each field where the active head finishes its diagonal pass and the next head takes over, producing a noise burst. |
| **Helical Scan** | Recording technique where the tape wraps around a tilted spinning drum, tracing diagonal stripes across the tape. |
| **IIR** | Infinite Impulse Response; a recursive filter structure where the output feeds back into the computation. Used here for chroma low-pass and jitter smoothing. |
| **LFSR** | Linear Feedback Shift Register; a shift register with XOR feedback that generates a deterministic pseudo-random bit sequence. |
| **TBC** | Time-Base Corrector; a device that locks each scan line to a stable reference clock, removing horizontal jitter from tape playback. |
| **Tracking** | The alignment between the playback head's scanning path and the recorded diagonal stripes on the tape. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
