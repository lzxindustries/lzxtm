---
draft: true
sidebar_position: 305
slug: /instruments/videomancer/vinegar
title: "Vinegar"
image: /img/instruments/videomancer/vinegar/vinegar_hero.png
description: "Film does not last forever."
---

import vinegar_hero from '/img/instruments/videomancer/vinegar/vinegar_hero.png';
import vinegar_before_after from '/img/instruments/videomancer/vinegar/vinegar_before_after.png';
import vinegar_control_panel from '/img/instruments/videomancer/vinegar/vinegar_control_panel.png';
import vinegar_exercise1_result from '/img/instruments/videomancer/vinegar/vinegar_exercise1_result.png';
import vinegar_exercise2_result from '/img/instruments/videomancer/vinegar/vinegar_exercise2_result.png';
import vinegar_exercise3_result from '/img/instruments/videomancer/vinegar/vinegar_exercise3_result.png';

# Vinegar

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={vinegar_hero} alt="Vinegar hero image"/>
*Vinegar simulating years of photochemical film decay — gate weave, dye fading, organic burn blobs, grain, and splice flashes transform a clean digital image into deteriorated celluloid.*
<img src={vinegar_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Vinegar applied.*

---

## Overview

Film does not last forever. Cellulose acetate base stock absorbs moisture and releases acetic acid in a self-accelerating decomposition known as *vinegar syndrome* — named for the sharp acetic smell of degrading film cans. The dyes fade at different rates depending on the film stock and storage conditions, colors shift, the emulsion blisters and stains, and the physical film base warps and shrinks, causing the image to weave unsteadily in the projector gate. Vinegar recreates this entire catalogue of photochemical deterioration as a real-time video processing effect.

The program chains ten processing stages across an 11-clock pipeline — gate weave via line-buffered horizontal displacement, asymmetric dye decay curves, organic burn and stain blobs from crossed LFSR generators, film grain noise, per-frame brightness flicker, splice flash bursts, sprocket slip artifacts, desaturation, and a final wet/dry mix. Three BRAMs provide Y/U/V line buffers for the gate weave displacement, and three LFSRs generate decorrelated pseudo-random sequences for the weave, grain, and blob domains.

The name *Vinegar* is a direct reference to vinegar syndrome, the archival community's term for the chemical decomposition of cellulose acetate motion picture film. At conservative settings the program adds a gentle aged-film patina; at extreme settings it produces the look of a print that has been stored in a hot, humid warehouse for decades.

---

## Background

### Vinegar Syndrome and Cellulose Acetate

Motion picture film stock manufactured from the 1950s onward used cellulose triacetate (CTA) as the base material, replacing the dangerously flammable cellulose nitrate used in earlier decades. CTA is chemically stable under ideal conditions but degrades through *acid hydrolysis* when exposed to heat and humidity. The degradation releases acetic acid — the compound that gives vinegar its smell — which accelerates further decomposition in a positive feedback loop called the *autocatalytic stage*. Archives detect vinegar syndrome by monitoring the pH of air inside sealed film cans using acid-detection strips (A-D strips). Once the process reaches the autocatalytic stage, the film base shrinks, buckles, and eventually becomes too warped to project.

### Dye Fading and Color Shift

Most color motion picture film from the 1950s through 1980s used the Eastmancolor (monopack) process, which layered three dye layers — cyan, magenta, and yellow — onto a single strip of film. These dyes fade at different rates depending on the chemical composition and storage environment. The cyan dye (which controls the red channel) is typically the least stable, fading first and producing the characteristic *magenta/pink shift* seen in aged Eastmancolor prints. Films stored in warmer environments lose cyan faster, while cold-stored prints may lose yellow first, producing a blue shift. Vinegar models this asymmetric decay through its Fade Curve toggle: Warm mode simulates cyan-first fading (progressive red/pink shift), while Cold mode simulates yellow-first fading (progressive blue shift).

### Gate Weave and Film Transport

The *gate* is the mechanical assembly in a film projector that holds each frame in position during exposure. Worn sprocket teeth, stretched sprocket holes, and loose gate pressure all cause the film to shift position slightly from frame to frame — an artifact called *gate weave*. The displacement is primarily horizontal (side-to-side wobble) and follows a smooth, low-frequency path rather than jumping randomly between frames. Vinegar models gate weave using a heavily filtered LFSR: the raw pseudo-random output is smoothed by a single-pole IIR filter ($y[n] = \frac{15 \cdot y[n-1] + x[n]}{16}$) that removes high-frequency jitter, then scaled by the Instability control.

### Film Grain Structure

Photographic film records images by exposing microscopic silver halide crystals in the emulsion layer to light. The random distribution of these crystals creates *film grain* — visible noise that varies in character depending on the film stock, exposure, and development process. High-speed (ASA 400+) stocks have larger, more visible grain than low-speed stocks. Vinegar simulates grain by adding per-pixel LFSR noise to the luma channel, with the Grain control setting the amplitude of the noise.

### Splice Marks and Reel Changes

When film breaks during projection — or when multiple reels are assembled into a single print — the film editor joins the ends with a physical *splice*. The splice itself, and the few frames of clear or fogged leader on either side, appear as bright flashes when projected. In badly maintained prints, splices occur frequently. Vinegar simulates this with periodic full-frame brightness bursts whose frequency is controlled by the Splice Rate parameter.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├─ 1. Line Buffer Write ───── Y/U/V stored to BRAM at h_count address
├─ 2. Gate Weave Read ─────── read from BRAM at offset address (IIR-smoothed LFSR)
├─ 3. Dye Fade ────────────── asymmetric channel gain reduction (warm/cold curve)
├─ 4. Blob Overlay ────────── crossed H/V LFSR → burn marks (bright) or stains (dark)
├─ 5. Grain ───────────────── LFSR per-pixel noise added to luma
├─ 6. Flicker ─────────────── per-frame global brightness variation
├─ 7. Splice Flash ────────── periodic full-frame white burst
├─ 8. Sprocket Slip ───────── vertical position jumps from damaged sprocket holes
├─ 9. Desaturate ──────────── chroma reduction toward neutral
├─ 10. Wet/Dry Mix ─────────── interpolator crossfade with delayed dry signal
│
└── Output Video (YUV 4:4:4)
```

The pipeline is structured to match the physical order of film degradation: mechanical transport artifacts (gate weave) come first because they displace the image before any colour or noise processing occurs. Dye fading then alters the colour balance, followed by additive damage (blobs, grain, splice, flicker) that accumulates on the faded image. The desaturation toggle provides an additional channel gain reduction that stacks with the dye fade curve, allowing aggressive monochrome washout independent of the colour-shift controls. The final mix stage crossfades between the fully degraded wet signal and the delayed original dry signal — at 0% the output is clean, at 100% it is fully deteriorated.

---

## Parameter Reference

<img src={vinegar_control_panel} alt="Videomancer front panel with Vinegar loaded"/>
*Videomancer's front panel with Vinegar active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Instability
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the amplitude of gate weave — smooth horizontal displacement applied per-line via a BRAM line buffer. The raw displacement is generated by a 16-bit LFSR and smoothed through a single-pole IIR low-pass filter, producing slow, organic wobble rather than frame-by-frame jitter. The Instability control scales the smoothed offset through 8 discrete levels using shift operations. At zero the image is perfectly stable; at maximum the horizontal wobble reaches several pixels per line, producing the unsteady projection look of a worn gate mechanism.

---

#### Knob 2 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the severity of dye fading — progressive colour shift caused by asymmetric dye decomposition. The Fade Curve toggle (Toggle 7) selects which dyes degrade first: Warm mode fades cyan (U contracts strongly toward neutral while V contracts weakly), producing a red/pink shift. Cold mode fades yellow (V contracts strongly while U contracts weakly), producing a blue shift. At zero the original colour balance is preserved; at maximum the dye that degrades faster is nearly eliminated, leaving a heavily colour-shifted image. The Y channel also loses brightness at higher Decay values, with Cold mode losing more luma than Warm.

---

#### Knob 3 — Damage
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the probability and intensity of damage blobs — circular or organic regions of chemical staining or heat damage overlaid on the image. The blob pattern is generated from crossed horizontal and vertical LFSRs (12-bit each), creating a 2D pseudo-random field. The Damage knob sets the threshold: lower threshold means more blobs. The Blob Mode toggle (Toggle 8) determines whether blobs are bright (burn marks, white) or dark (stains, near-black with neutral chroma).

---

#### Knob 4 — Blob Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial frequency and extent of damage blobs. At low values blobs are small and sparse; at high values they grow larger, covering more of the frame. This parameter works in conjunction with the Damage control — Damage sets the threshold for blob activation, while Blob Size influences the spatial scale of the blob field (via the damage register's division applied to the blob threshold).

---

#### Knob 5 — Grain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Adds per-pixel luma noise simulating photographic film grain. The noise source is a 16-bit LFSR that advances every pixel clock, producing pseudo-random values. The Grain control scales the noise amplitude through 8 discrete levels using shift operations, from barely perceptible at low settings to heavy, coarse grain at maximum. The noise is bipolar — it can add or subtract from luma — with the polarity determined by a single LFSR bit.

---

#### Knob 6 — Splice Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the frequency of splice flash events — periodic full-frame brightness bursts simulating the clear or fogged leader between spliced film reels. At zero, no flashes occur. As the value increases, flashes become more frequent. Each flash lasts 1–2 frames and adds a large brightness offset to the entire frame, simulating the sudden white flash of a splice passing through the projector gate.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Fade Curve** | Warm | Cold |
| **8 — Blob Mode** | Bright | Dark |
| **9 — Flicker** | Off | On |
| **10 — Sprocket** | Off | On |
| **11 — Desaturate** | Off | On |

The five toggles configure the character of the deterioration rather than enabling/disabling stages. Toggles 7 and 8 select between paired modes (warm/cold fade, bright/dark blobs). Toggles 9 and 10 enable optional overlay effects. Toggle 11 is a desaturation switch, not a bypass — use the Mix fader at 0% for the clean signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the original dry signal and the fully deteriorated wet signal. At 0% the output is the unmodified input; at 100% the full film deterioration processing is applied. This allows precise control over the apparent age of the simulated film stock.

---

## Guided Exercises

These exercises progress from subtle aging to severe deterioration. Each builds on the understanding of how individual decay processes combine to create the complete film degradation aesthetic.

### Exercise 1: Gentle Aging

<img src={vinegar_exercise1_result} alt="Gentle Aging result"/>
*Gentle Aging — simulated result across source images.*
**Source**: Well-exposed footage with natural colour — portraits, landscapes, or documentary material.

**Objective**: Add a subtle aged-film patina with gentle gate weave, mild dye fading, and light grain.

1. Set Instability to about 15% for barely perceptible horizontal wobble.
2. Set Decay to about 25% with Fade Curve on Warm. Observe the slight pink/warm colour shift.
3. Set Grain to about 20% for light film texture.
4. Keep all other effects at zero or off.
5. Set Mix to 100%.
6. Toggle Fade Curve between Warm and Cold to compare the two colour-shift directions.
7. Slowly increase Decay to see how the colour shift progresses.

**Key concepts**: Gate weave is smooth and low-frequency due to IIR filtering, Warm and Cold fading produce opposite colour shifts, grain adds texture without altering colour

---

### Exercise 2: Damaged Print

<img src={vinegar_exercise2_result} alt="Damaged Print result"/>
*Damaged Print — simulated result across source images.*
**Source**: Any footage — the damage effects are content-independent.

**Objective**: Add physical damage artifacts: blobs, flicker, splice flashes, and sprocket slip.

1. Start from Exercise 1 settings (Instability ~15%, Decay ~25%, Grain ~20%).
2. Set Damage to about 20% and Blob Size to about 40%. Watch organic blob shapes appear.
3. Toggle Blob Mode between Bright and Dark to compare burn marks vs. stains.
4. Enable Flicker. Observe per-frame brightness variation.
5. Set Splice Rate to about 15%. Watch for periodic white flash frames.
6. Enable Sprocket. Observe occasional subtle vertical jumps.
7. Increase Instability to about 40% for more dramatic gate weave.

**Key concepts**: Blobs are generated from crossed H/V LFSRs creating 2D patterns, Bright and Dark blob modes simulate different physical damage types, flicker and splice are per-frame effects while blobs are spatial

---

### Exercise 3: Terminal Decay

<img src={vinegar_exercise3_result} alt="Terminal Decay result"/>
*Terminal Decay — simulated result across source images.*
**Source**: Any footage — heavy processing creates abstract results regardless of source.

**Objective**: Simulate film in the final stages of vinegar syndrome — extreme colour shift, heavy grain, frequent damage, and instability.

1. Set Instability to about 70% for heavy gate weave.
2. Set Decay to about 80% with Warm fade. Observe extreme pink/magenta colour shift.
3. Set Damage to about 60% and Blob Size to about 60% for extensive dark stains.
4. Set Grain to about 65% for coarse, visible grain texture.
5. Set Splice Rate to about 30% for frequent flash frames.
6. Enable Flicker and Sprocket for full mechanical degradation.
7. Enable Desaturate for additional colour loss.
8. Pull Mix back to about 75% to retain some recognizable image content.
9. Switch to Cold fade to see the alternative (blue-shifted) decay path.

**Key concepts**: All decay processes compound, Desaturate stacks with dye fade for extreme colour loss, high Instability makes the image float and drift horizontally, the autocatalytic metaphor — each degradation makes the others more visible

---


## Tips

- **Start subtle**: The most convincing film aging uses low values — 15% Instability, 25% Decay, 20% Grain. Heavy settings read as "damaged print" rather than "old film."
- **Warm for Eastmancolor**: Choose Warm fade to recreate the iconic pink shift of 1960s–1980s theatrical prints. Cold is for archival simulation of cold-stored prints with yellow dye loss.
- **Dark blobs for mold**: Set Blob Mode to Dark for the organic staining look of mold and water damage. Bright blobs simulate projector burn marks and chemical bleaching.
- **Layer grain and flicker**: Grain (per-pixel) and Flicker (per-frame) are independent noise sources. Using both creates a more organic look than either alone.
- **Splice Rate for rhythm**: Even at low settings, occasional splice flashes create a rhythmic punctuation that signals "projected film" to the viewer.
- **Sprocket for subtlety**: Enable Sprocket for occasional vertical jumps that most viewers won't consciously notice but that contribute to the overall feeling of mechanical instability.
- **Feedback for accelerated decay**: Route the output back to the input. Each pass adds another layer of dye fade, grain, and blobs — the autocatalytic destruction of vinegar syndrome made visible.
- **Mix for time travel**: Animate the Mix fader slowly from 0% to 100% to simulate the progressive deterioration of a film print over decades.

---

## Glossary

| Term | Definition |
|------|------------|
| **Autocatalytic** | A chemical reaction that accelerates its own rate; in vinegar syndrome the acetic acid released by degradation accelerates further decomposition. |
| **BRAM** | Block RAM; dedicated FPGA memory. Vinegar uses 3 BRAMs for Y/U/V line buffers enabling gate weave. |
| **Cellulose Acetate** | The plastic base material of motion picture film manufactured from the 1950s onward; susceptible to vinegar syndrome. |
| **Cyan Dye** | The dye layer in colour film that controls the red channel; the least stable dye in Eastmancolor stocks. |
| **Eastmancolor** | Kodak's monopack colour film process used for most theatrical motion pictures from 1952 onward. |
| **Gate Weave** | Horizontal displacement of the film image caused by mechanical play in the projector gate mechanism. |
| **IIR Filter** | Infinite Impulse Response filter; a digital filter whose output depends on both current input and previous output, used here to smooth LFSR noise into organic wobble. |
| **LFSR** | Linear Feedback Shift Register; generates maximal-length pseudo-random sequences. Vinegar uses three independent LFSRs. |
| **Pipeline** | Sequential processing stages; Vinegar has an 11-clock pipeline plus 5-clock interpolator mix. |
| **Splice** | A physical join between two pieces of film, visible as a bright flash or frame disruption during projection. |
| **Sprocket** | Tooth on a projector mechanism that engages with holes along the film edge to advance it; worn sprockets cause position errors. |
| **Vinegar Syndrome** | The chemical decomposition of cellulose acetate film base through acid hydrolysis, causing warping, shrinkage, and dye fading. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |

---
