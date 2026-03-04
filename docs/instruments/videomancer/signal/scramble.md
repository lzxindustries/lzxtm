---
draft: false
sidebar_position: 262
slug: /instruments/videomancer/scramble
title: "Scramble"
image: /img/instruments/videomancer/scramble/scramble_hero_s1.png
description: "Analog pay-TV systems of the late 1980s and early 1990s scrambled their signals to prevent unauthorized viewing."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import scramble_control_panel from '/img/instruments/videomancer/scramble/scramble_control_panel.png';
import scramble_source1_fruit from '/img/instruments/videomancer/scramble/scramble_source1_fruit.png';
import scramble_source2_skull from '/img/instruments/videomancer/scramble/scramble_source2_skull.png';
import scramble_source3_turtle from '/img/instruments/videomancer/scramble/scramble_source3_turtle.png';
import scramble_source4_pattern from '/img/instruments/videomancer/scramble/scramble_source4_pattern.png';
import scramble_source5_boy from '/img/instruments/videomancer/scramble/scramble_source5_boy.png';
import scramble_source6_berries from '/img/instruments/videomancer/scramble/scramble_source6_berries.png';
import scramble_hero_s1 from '/img/instruments/videomancer/scramble/scramble_hero_s1.png';
import scramble_hero_s2 from '/img/instruments/videomancer/scramble/scramble_hero_s2.png';
import scramble_hero_s3 from '/img/instruments/videomancer/scramble/scramble_hero_s3.png';
import scramble_hero_s4 from '/img/instruments/videomancer/scramble/scramble_hero_s4.png';
import scramble_hero_s5 from '/img/instruments/videomancer/scramble/scramble_hero_s5.png';
import scramble_hero_s6 from '/img/instruments/videomancer/scramble/scramble_hero_s6.png';
import scramble_ex1_s1 from '/img/instruments/videomancer/scramble/scramble_ex1_s1.png';
import scramble_ex1_s2 from '/img/instruments/videomancer/scramble/scramble_ex1_s2.png';
import scramble_ex1_s3 from '/img/instruments/videomancer/scramble/scramble_ex1_s3.png';
import scramble_ex1_s4 from '/img/instruments/videomancer/scramble/scramble_ex1_s4.png';
import scramble_ex1_s5 from '/img/instruments/videomancer/scramble/scramble_ex1_s5.png';
import scramble_ex1_s6 from '/img/instruments/videomancer/scramble/scramble_ex1_s6.png';
import scramble_ex2_s1 from '/img/instruments/videomancer/scramble/scramble_ex2_s1.png';
import scramble_ex2_s2 from '/img/instruments/videomancer/scramble/scramble_ex2_s2.png';
import scramble_ex2_s3 from '/img/instruments/videomancer/scramble/scramble_ex2_s3.png';
import scramble_ex2_s4 from '/img/instruments/videomancer/scramble/scramble_ex2_s4.png';
import scramble_ex2_s5 from '/img/instruments/videomancer/scramble/scramble_ex2_s5.png';
import scramble_ex2_s6 from '/img/instruments/videomancer/scramble/scramble_ex2_s6.png';
import scramble_ex3_s1 from '/img/instruments/videomancer/scramble/scramble_ex3_s1.png';
import scramble_ex3_s2 from '/img/instruments/videomancer/scramble/scramble_ex3_s2.png';
import scramble_ex3_s3 from '/img/instruments/videomancer/scramble/scramble_ex3_s3.png';
import scramble_ex3_s4 from '/img/instruments/videomancer/scramble/scramble_ex3_s4.png';
import scramble_ex3_s5 from '/img/instruments/videomancer/scramble/scramble_ex3_s5.png';
import scramble_ex3_s6 from '/img/instruments/videomancer/scramble/scramble_ex3_s6.png';

# Scramble

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: scramble_source1_fruit, after: scramble_hero_s1 },
    { label: "Skull", before: scramble_source2_skull, after: scramble_hero_s2 },
    { label: "Turtle", before: scramble_source3_turtle, after: scramble_hero_s3 },
    { label: "Pattern", before: scramble_source4_pattern, after: scramble_hero_s4 },
    { label: "Boy", before: scramble_source5_boy, after: scramble_hero_s5 },
    { label: "Berries", before: scramble_source6_berries, after: scramble_hero_s6 },
  ]}
/>
*Scramble applying per-line cut-and-rotate shuffling with jitter and inversion zones to a portrait, recreating the look of a failing analog TV descrambler.*

---

## Overview

Analog pay-TV systems of the late 1980s and early 1990s scrambled their signals to prevent unauthorized viewing. The most common technique was **per-line cut-and-rotate**: each scanline was split at a secret cut point and the two halves were swapped. Without the matching decoder key, the viewer saw a picture sliced into horizontal strips, each shifted to a different horizontal position — recognizable in outline but impossible to watch. Scramble recreates this effect digitally, simulating not just the scrambling itself but the full spectrum of decoder failure artifacts: sync suppression jitter, video inversion zones, and the mesmerizing drift of a descrambler that almost — but never quite — locks on.

The program chains four processing stages: a line buffer with per-line cut-and-rotate addressing, video inversion zones that negate alternating groups of lines, horizontal jitter simulating sync suppression, and a wet/dry crossfade mix. The name comes directly from the broadcast industry term — a "scrambled" signal is one whose line order or line content has been deliberately disrupted to deny intelligibility. The "Decode" control sweeps the descrambler alignment, and when it cancels the LFSR sequence the image momentarily snaps into clarity like adjusting a pirate decoder box.

At conservative settings, Scramble produces a mild horizontal displacement that gently slides portions of the image apart. At extreme settings with all features enabled — double scramble, luma modulation, heavy jitter, and fast drift — the image dissolves into an aggressively disrupted field of shuffled, inverted, trembling video fragments that evokes the experience of trying to watch a premium cable channel through a malfunctioning black-market decoder.

---

## Background

### Per-Line Cut-and-Rotate Scrambling

The **VideoCrypt** system, deployed by British Sky Broadcasting in 1989, scrambled each scanline by splitting it at a pseudo-random cut point and swapping the two halves. The cut point changed every line according to a sequence stored on a smart card. Without the card, the viewer saw a picture in which every line was horizontally displaced by a different amount — the classic "shuffled blinds" look. **Nagravision** and other European pay-TV systems used similar line-delay techniques. Scramble implements this by writing each scanline into a 1024-pixel line buffer and reading it back with a per-line offset derived from a 16-bit LFSR, producing a new pseudo-random displacement for every line.

### Sync Suppression and Horizontal Jitter

Pay-TV systems like **SSAVI** (Sync Suppression And Video Inversion) went further than line shuffling: they attenuated or replaced the horizontal sync pulses in the analog signal. A TV receiver that lost horizontal sync would display lines that drifted and wobbled horizontally — the picture "swam" left and right. Scramble simulates this with a second LFSR that generates a per-line horizontal displacement scaled by the Jitter control. The result is the characteristic trembling instability of a signal whose sync has been partially suppressed.

### Video Inversion Scrambling

**ON TV** and **SelecTV**, two over-the-air pay-TV services in the United States during the early 1980s, scrambled their signals by inverting the video — replacing each brightness value with its complement so that bright became dark and dark became bright. More sophisticated systems inverted only portions of each frame, creating alternating bands of normal and inverted video. Scramble implements this by selecting a bit of the line counter as an inversion toggle, producing groups of 2, 4, 8, 16, 32, 64, or 128 consecutive lines that alternate between normal and inverted. In "Full YUV" mode, the chroma channels are also inverted, producing complementary-color zebra stripes.

### LFSR Pseudo-Random Sequences

A **Linear Feedback Shift Register** (LFSR) generates a sequence of pseudo-random numbers by shifting a register and feeding back the XOR of specific bit positions (called taps). The sequence is deterministic — given the same seed, the same sequence always results. Scramble uses a 16-bit LFSR (taps 16, 15, 13, 4 for maximal length) to generate the per-line cut point, and a 10-bit LFSR (taps 10, 7) for the jitter displacement. The cut LFSR is reseeded every frame from the Seed control plus the current drift offset, ensuring repeatable scramble patterns that evolve predictably when drift is active.

### Descrambler Lock and Drift

Real descramblers worked by applying the inverse of the scrambling sequence — subtracting the same cut-point offset that was added. When the decoder key matched, the offsets cancelled and the picture snapped into clarity. When the key was wrong or the decoder was drifting, the picture would partially lock — some lines clear, others still scrambled — creating a hypnotic cycling between clarity and chaos. Scramble's Decode control provides this manual alignment, while the Drift mode automatically sweeps the decode offset, producing the periodic lock-unlock cycling that defined the experience of watching a pirate decoder slowly lose sync.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── All Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Line Buffer Write      (write Y/U/V at linear address)
│   ├─ 2. Cut-Point Generation    (16-bit LFSR or sawtooth per line)
│   ├─ 3. Cut-Point Scaling       (scale by Cut Depth, add Decode + drift)
│   ├─ 4. Luma Modulation         (optional: add input Y to read offset)
│   ├─ 5. Double Scramble         (optional: add second LFSR-derived offset)
│   ├─ 6. H-Jitter                (add 10-bit LFSR × Jitter amount)
│   ├─ 7. Line Buffer Read        (read Y/U/V at computed offset address)
│   └─ 8. Video Inversion         (conditional Y/UV negate per line group)
│
├── Mix Stage ──────────────────────────────────────────────────
│   └─ 9. Interpolator            (wet/dry crossfade, 4-clock pipeline)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delayed pass-through (8-clock shift register)
│
└── Output ─────────────────────────────────────────────────────
    └─ Mixed result with aligned sync
```

The cut-and-rotate mechanism is the core of the pipeline: all three channels (Y, U, V) share the same line buffer write and offset-read addresses, so the scrambling is always spatially coherent. The read address is the sum of the horizontal position, the scaled cut point (LFSR or sawtooth × Cut Depth), the negated decode offset (including any drift), optional luma-reactive offset, optional double-scramble offset, and jitter. All address arithmetic wraps naturally at 1024 pixels due to the 10-bit address width.

Video inversion is applied *after* the line buffer read, meaning the inversion zones operate on the already-scrambled image. The inversion period is controlled by selecting which bit of the vertical line counter acts as the toggle — bit 1 gives 2-line groups, bit 7 gives 128-line groups. The 8-clock processing delay is compensated by a matching shift register on the sync and dry-path data signals, ensuring the interpolator mix stage receives properly aligned wet and dry signals.

---

## Parameter Reference

<img src={scramble_control_panel} alt="Videomancer front panel with Scramble loaded"/>
*Videomancer's front panel with Scramble active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Cut Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the maximum horizontal displacement of the cut-and-rotate scrambling. At the minimum setting the cut point is always zero regardless of the LFSR sequence, producing no visible scrambling. As the control increases, each line's cut point is scaled proportionally — low values create subtle horizontal shifts that are barely perceptible; high values produce full-line displacements where each scanline wraps around the entire 1024-pixel buffer. This is the primary intensity control for the scrambling effect and should be the first knob adjusted when exploring the program.

---

#### Knob 2 — Decode
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Applies a constant horizontal offset that is subtracted from the LFSR-generated cut point on every line. When this offset exactly matches the LFSR sequence for a given line, that line appears unscrambled. Sweeping this control slowly across its range produces the signature descrambler effect: the image periodically snaps into partial or full clarity as the offset cancels more of the LFSR values, then slides back into scrambled chaos. With Drift enabled, this control sets the center point around which the auto-drift wanders.

---

#### Knob 3 — Seed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the seed value for the 16-bit LFSR that generates per-line cut points. Different seed values produce entirely different scramble patterns — the same input frame looks completely different with different seeds. The LFSR is reseeded at the start of every video frame, so the scramble pattern repeats identically from frame to frame for a given seed. When Drift is enabled, the drift offset is XORed with the seed, causing the pattern to evolve gradually over time.

---

#### Knob 4 — Invert Period
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Selects the size of the line groups used for video inversion zones. At step 0, inversion is disabled entirely. Steps 1 through 7 select progressively larger line groups (2, 4, 8, 16, 32, 64, 128 lines) that alternate between normal and inverted video. Small group sizes produce fine zebra-stripe banding; large group sizes produce broad alternating bands. The inversion interacts visually with the scrambling — because the lines are already horizontally shuffled, the inversion zones create a complex interleaving of normal and negative imagery.

---

#### Knob 5 — Jitter
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the amplitude of the horizontal sync-suppression jitter. A second 10-bit LFSR generates a per-line pseudo-random displacement that is scaled by this control and added to the read address. At zero, lines are horizontally stable. As the control increases, lines begin to tremble and swim horizontally, simulating the effect of a TV receiver losing horizontal sync lock due to suppressed or corrupted sync pulses. Heavy jitter combined with full scrambling produces an aggressively disrupted image.

---

#### Knob 6 — Drift Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the speed of the automatic decode offset drift. When Drift mode is enabled (Toggle 9), a frame-rate accumulator adds this value every frame, causing the effective decode offset to slowly wander. At zero drift rate, the offset is stationary. At maximum, the offset sweeps rapidly, producing fast cycling between locked and unlocked states. The drift is deterministic — the same rate always produces the same lock/unlock timing pattern for a given seed.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Scramble Mode** | LFSR | Sawtooth |
| **8 — Invert Mode** | Luma | Full YUV |
| **9 — Drift** | Off | On |
| **10 — Luma Mod** | Off | On |
| **11 — Double** | Off | On |

The five toggles control independent binary options that can be combined freely. Scramble Mode (Toggle 7) selects the fundamental scramble pattern generator. Invert Mode (Toggle 8) extends inversion from luma-only to full YUV. Drift (Toggle 9) enables automatic decode offset wandering. Luma Mod (Toggle 10) makes the scramble pattern content-dependent. Double (Toggle 11) adds a second layer of scrambling for more aggressive disruption. Any combination of these toggles is valid and produces distinct visual results.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed (scrambled) signal and the original unprocessed input. At 0% (fully counterclockwise), the output is the clean, unscrambled input signal. At 100% (fully clockwise), the output is the fully processed scrambled signal. Intermediate positions blend the two, which can produce a ghostly overlay of the scrambled and unscrambled images — useful for subtle displacement effects or for monitoring the degree of scrambling while adjusting other controls.

---

## Guided Exercises

These exercises progress from basic cut-and-rotate scrambling to full descrambler failure simulation. Each builds on the previous, gradually engaging more of the scrambling and artifact pipeline.

### Exercise 1: Basic Cut-and-Rotate

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: scramble_source1_fruit, after: scramble_ex1_s1 },
    { label: "Skull", before: scramble_source2_skull, after: scramble_ex1_s2 },
    { label: "Turtle", before: scramble_source3_turtle, after: scramble_ex1_s3 },
    { label: "Pattern", before: scramble_source4_pattern, after: scramble_ex1_s4 },
    { label: "Boy", before: scramble_source5_boy, after: scramble_ex1_s5 },
    { label: "Berries", before: scramble_source6_berries, after: scramble_ex1_s6 },
  ]}
/>
*Basic Cut-and-Rotate — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects — faces, text, or geometric patterns work well because the scrambling effect is most obvious when you can tell the image *should* be coherent.

**Objective**: Learn how the cut-and-rotate mechanism works and how the Decode control interacts with the LFSR sequence to produce momentary locks.

1. **Set Mix to full wet**: Push the Mix fader to 100% so you see only the scrambled output.
2. **Engage scrambling**: Slowly increase Cut Depth from zero. Watch as horizontal slices of the image begin to shift apart — the classic "shuffled blinds" effect appears.
3. **Full displacement**: Set Cut Depth to about 75%. Each scanline is now displaced by up to three-quarters of the line width.
4. **Sweep the decoder**: Slowly turn the Decode knob across its full range. Watch for moments where groups of lines suddenly snap into alignment — this is the descrambler locking onto portions of the LFSR sequence.
5. **Change the pattern**: Adjust the Seed knob. The scramble pattern changes entirely — different lines shift to different positions, and the Decode lock point moves.
6. **Sawtooth mode**: Flip Scramble Mode to Sawtooth (Toggle 7). The random per-line displacement is replaced by a smooth diagonal shear. Sweep Decode again — the lock behavior is different because the pattern is linear rather than pseudo-random.

**Key concepts**: Cut-and-rotate splits and swaps each scanline at a variable cut point, LFSR generates pseudo-random per-line offsets, Decode cancels the offset to produce momentary clarity, Seed determines the scramble pattern

---

### Exercise 2: Jitter and Inversion Artifacts

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: scramble_source1_fruit, after: scramble_ex2_s1 },
    { label: "Skull", before: scramble_source2_skull, after: scramble_ex2_s2 },
    { label: "Turtle", before: scramble_source3_turtle, after: scramble_ex2_s3 },
    { label: "Pattern", before: scramble_source4_pattern, after: scramble_ex2_s4 },
    { label: "Boy", before: scramble_source5_boy, after: scramble_ex2_s5 },
    { label: "Berries", before: scramble_source6_berries, after: scramble_ex2_s6 },
  ]}
/>
*Jitter and Inversion Artifacts — simulated result across source images.*
**Source**: Any footage, preferably with a mix of bright and dark regions to make inversion zones clearly visible.

**Objective**: Layer sync-suppression jitter and video inversion onto the basic scrambling to create a more complete descrambler failure simulation.

1. **Prepare base scramble**: Set Cut Depth to ~60%, Decode to ~30%, Seed to ~25%.
2. **Add jitter**: Slowly increase the Jitter knob. Watch as lines begin to tremble horizontally — this is the simulated sync suppression. At moderate levels the image swims gently; at high levels it shakes violently.
3. **Enable inversion zones**: Turn the Invert Period knob from 0 to step 3 (8-line groups). Alternating bands of the image flip to negative. The scrambling makes these bands interleave in complex ways.
4. **Full YUV inversion**: Flip Invert Mode (Toggle 8) to Full YUV. The inverted zones now show complementary colors as well as inverted brightness — a much more dramatic effect.
5. **Reduce group size**: Turn Invert Period back to step 1 (2-line groups). The inversion becomes a fine-grained zebra stripe that interleaves with the scrambled lines.
6. **Increase group size**: Try step 6 (64-line groups). Broad alternating bands of normal and inverted scrambled video appear.

**Key concepts**: Jitter simulates horizontal sync suppression, inversion zones negate brightness and optionally color, group size controls the visual density of the inversion pattern, all artifacts compound on each other

---

### Exercise 3: Full Descrambler Failure

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: scramble_source1_fruit, after: scramble_ex3_s1 },
    { label: "Skull", before: scramble_source2_skull, after: scramble_ex3_s2 },
    { label: "Turtle", before: scramble_source3_turtle, after: scramble_ex3_s3 },
    { label: "Pattern", before: scramble_source4_pattern, after: scramble_ex3_s4 },
    { label: "Boy", before: scramble_source5_boy, after: scramble_ex3_s5 },
    { label: "Berries", before: scramble_source6_berries, after: scramble_ex3_s6 },
  ]}
/>
*Full Descrambler Failure — simulated result across source images.*
**Source**: Any dynamic video source — movement helps reveal the drift and luma modulation effects.

**Objective**: Combine all features to create the complete descrambler failure experience with auto-drifting lock, content-responsive scrambling, and maximum disruption.

1. **Full scramble**: Set Cut Depth to ~80%, Jitter to ~40%, Invert Period to step 4 (16-line groups), Invert Mode to Full YUV.
2. **Enable drift**: Flip Drift (Toggle 9) to On. Set Drift Rate to ~30%. Watch as the image begins to cycle between clarity and chaos — the decode offset is wandering automatically.
3. **Adjust drift speed**: Increase Drift Rate to ~60%. The lock/unlock cycling accelerates. Decrease it to ~10% for slow, meditative transitions.
4. **Add luma modulation**: Enable Luma Mod (Toggle 10). Bright regions of the source now scramble differently than dark regions — the displacement pattern follows the image content.
5. **Double scramble**: Enable Double (Toggle 11). The disruption intensifies dramatically as two independent LFSR-derived offsets are applied simultaneously. The Decode lock becomes much harder to achieve.
6. **Partial mix**: Pull the Mix fader down to ~60%. The scrambled and unscrambled images overlay each other, creating a ghostly double-exposure effect.
7. **Animate**: Let the drift run while slowly adjusting Cut Depth and Seed. Watch the descrambler cycle through lock states with evolving patterns.

**Key concepts**: Drift creates periodic lock/unlock cycling, luma modulation makes scrambling content-dependent, double scramble compounds two LFSR offsets, partial mix creates overlay effects, all features interact to produce rich temporal variation

---


## Tips

- **Decode is the signature control**: Sweeping Decode while scrambling is active produces the quintessential descrambler effect — the image snapping in and out of clarity. Start every session with Cut Depth up and Decode sweeping.
- **Seed controls the vocabulary**: Different seeds produce completely different scramble patterns. If you find a particularly interesting partial-lock position, that specific seed/decode combination defines it — try several seeds to find the pattern you want.
- **Drift creates temporal evolution**: Enable Drift and set a low Drift Rate for slow, meditative cycling between locked and scrambled states. Higher rates produce rapid strobing between clarity and chaos.
- **Jitter adds realism**: Real descrambler failures always included horizontal instability. Even a small amount of Jitter (10–20%) adds convincing sync-suppression wobble to the scrambled image.
- **Inversion deepens the disruption**: The inversion zones are most dramatic at medium group sizes (steps 3–5) where you get visible bands without the effect becoming too fine or too coarse. Full YUV inversion is more visually striking than luma-only.
- **Feedback loops**: Routing Scramble's output back to its input creates recursive scrambling — each feedback pass applies a new layer of cut-and-rotate, rapidly dissolving the image into horizontal noise.
- **Partial mix for overlay effects**: Setting Mix to 40–60% creates a double-exposure look where the scrambled and original images coexist, useful for subtle glitch effects or artistic displacement.
- **Bypass for A/B comparison**: The Mix fader at 0% instantly shows the unprocessed signal for before/after comparison without changing any other settings.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chroma** | The color-carrying component of a video signal, as distinct from luminance (brightness). |
| **Crossfade** | A gradual blend between two signals, here used to mix between the processed (wet) and unprocessed (dry) video paths. |
| **Cut-and-rotate** | A scrambling technique that splits each scanline at a variable cut point and swaps the two halves, wrapping around the line boundary. |
| **LFSR** | Linear Feedback Shift Register; a hardware circuit that generates a deterministic pseudo-random bit sequence by feeding back the XOR of selected register tap positions. |
| **Line buffer** | A block of memory sized to store one complete horizontal scanline of pixel data, enabling per-line read and write at independent addresses. |
| **Luma** | The luminance (brightness) component of a video signal, represented by the Y channel in YUV encoding. |
| **Sawtooth** | A waveform that rises linearly from minimum to maximum and then resets, used here as an alternative to LFSR for generating progressive per-line displacement offsets. |
| **Seed** | An initial value loaded into a pseudo-random generator that determines the entire subsequent output sequence. |
| **Sync suppression** | Deliberate removal or attenuation of horizontal synchronization pulses in an analog video signal, causing the receiving display to lose horizontal timing. |
| **Wet/dry** | Audio and video processing convention where "wet" refers to the fully processed signal and "dry" refers to the original unprocessed signal. |
| **XOR** | Exclusive OR; a binary logic operation that outputs 1 when its two inputs differ, used in LFSR feedback paths and bit-level manipulation. |
| **YUV** | A color encoding scheme that separates luminance (Y) from two chrominance difference signals (U and V), standard in broadcast and digital video processing. |

---
