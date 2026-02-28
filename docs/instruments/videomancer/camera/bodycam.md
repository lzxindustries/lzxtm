---
draft: true
sidebar_position: 25
slug: /instruments/videomancer/bodycam
title: "Bodycam"
image: /img/instruments/videomancer/bodycam/bodycam_hero.png
description: "Bodycam simulates the look of footage from a low-quality body-worn camera."
---

import bodycam_hero from '/img/instruments/videomancer/bodycam/bodycam_hero.png';
import bodycam_before_after from '/img/instruments/videomancer/bodycam/bodycam_before_after.png';
import bodycam_control_panel from '/img/instruments/videomancer/bodycam/bodycam_control_panel.png';
import bodycam_exercise1_result from '/img/instruments/videomancer/bodycam/bodycam_exercise1_result.png';
import bodycam_exercise2_result from '/img/instruments/videomancer/bodycam/bodycam_exercise2_result.png';
import bodycam_exercise3_result from '/img/instruments/videomancer/bodycam/bodycam_exercise3_result.png';

# Bodycam

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={bodycam_hero} alt="Bodycam hero image"/>
*Jittery horizontal lines, dropped frames, edge vignetting, and a scrolling timestamp bar transform clean footage into convincing body-camera surveillance.*
<img src={bodycam_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Bodycam applied.*

---

## Overview

Bodycam simulates the look of footage from a low-quality body-worn camera. It combines several degradation artefacts: horizontal line jitter (random per-line horizontal displacement sampled from an LFSR), periodic frame drops that briefly replace the image with near-black, edge vignetting that darkens the horizontal borders, additive noise, a scrolling timestamp bar overlay, vertical bounce from a triangle-wave oscillator, and an optional night-vision mode that desaturates and tints the image green.

The pipeline is entirely register-based — no BRAM is used. All effects are composited in four stages plus a four-clock interpolator, producing a total latency of eight clocks. The LFSR provides a continuously-cycling pseudo-random sequence used for both per-line jitter offsets and noise injection.

The name directly references the body-worn video cameras used by law enforcement and security personnel. These cameras typically produce lower-quality footage characterised by motion artefacts, lens vignetting, compression glitches, and timestamp overlays — exactly the artefact vocabulary that Bodycam puts under real-time control.

---

## Background

### Body-Worn Camera Artefacts

Real body camera footage suffers from several characteristic degradations. The camera is mounted on a person's body and subject to constant motion, producing horizontal displacement and vertical bounce. Low-end sensors and codecs drop frames under rapid motion or low light. Wide-angle lenses create peripheral darkening (vignetting). Automatic gain control boosts noise in dim environments. Firmware-embedded timestamps scroll across the frame. Bodycam distills these artefacts into individual controllable parameters.

### LFSR Noise and Jitter

A 16-bit linear feedback shift register (Galois LFSR, seed 0xD4C7) generates a continuously-cycling pseudo-random sequence. At the start of each active video line, a 6-bit sample is latched from the LFSR output — this becomes the line's horizontal jitter offset. The same LFSR output is also masked and scaled to inject random noise into the luma channel. Because a single LFSR drives both jitter and noise, the two artefacts are correlated — a property that adds realism, since real camera artefacts tend to be correlated across failure modes.

### Vignette via Shift-Select

Real body camera vignetting is radial, darkening the entire periphery. Bodycam approximates this with horizontal-only edge darkening. The vignette factor is computed from the pixel's horizontal position: within 128 pixels of the left or right edge, a brightness factor ramps from near-zero to full. The factor is then applied to luma using a 3-bit shift selector — an approximation of multiplication that avoids hardware multipliers. The result is a smooth-looking edge fade using only shifts and adds.

### Frame Drop Simulation

Body cameras frequently drop frames when the recording buffer overflows or the codec can't keep up with motion. Bodycam simulates this by periodically replacing the entire output with near-black (Y=16, neutral chroma) for one frame. The drop frequency is controlled by masking the frame counter with a threshold derived from the Drop Frq pot — higher values create more frequent drops.

### Night Vision Mode

Night-vision cameras typically use IR illumination with a monochrome sensor, producing a characteristic green-tinted monochrome image. Bodycam's night mode desaturates the image by pulling U and V toward a value offset from neutral (512 − Y>>3), creating a green bias, and boosts luma by 12.5% (Y + Y>>3) for the amplified-gain look.


---

## Signal Flow

```
                              ┌────────────────────┐
data_in ─────────────────────►│ Input Register      │
                              │ + LFSR sample latch │
                              └──────┬─────────────┘
                                     │ Stage 1
                                     ▼
                              ┌────────────────────┐
                              │ Jitter Offset       │
                              │ + Frame Drop Detect │
                              │ + Vignette Compute  │
                              │ + Noise Add         │
                              └──────┬─────────────┘
                                     │ Stage 2
                                     ▼
                              ┌────────────────────┐
                              │ Timestamp Bar       │
                              │ + Bounce Compose    │
                              └──────┬─────────────┘
                                     │ Stage 3
                                     ▼
                              ┌────────────────────┐
                              │ Final Compose       │
                              │ (drop + stamp +     │
                              │  night mode)        │
                              └──────┬─────────────┘
                                     │ Stage 4
                                     ▼
data_in ──► [sync delay] ──► dry ──► Interpolator ◄── wet
                                       (4 clk)
                                          │
                                          ▼
                                      data_out
```

All effects are layered in a fixed priority order in the final compose stage. Frame drops have the highest priority — when active, the output is forced to near-black regardless of other effects. The timestamp bar takes next priority, overwriting video with its scrolling bright/dim pattern. Night mode applies last, tinting the entire result (including any timestamp bar) green. The vignette and noise are applied earlier in Stage 2 to the luma channel before any overlay compositing.

The bounce effect modulates the vertical line counter with a triangle wave, but in the current pipeline this offset is computed and available for position-dependent processing — the primary visible effect is a slow vertical oscillation of position-dependent features like the timestamp bar.

---

## Parameter Reference

<img src={bodycam_control_panel} alt="Videomancer front panel with Bodycam loaded"/>
*Videomancer's front panel with Bodycam active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Distort
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the amplitude of horizontal line jitter. A 6-bit LFSR sample is latched at the start of each active line; the jitter amount pot masks this sample to control the maximum displacement. At 0%, no jitter is applied. At low values (10–30%), a subtle horizontal wobble appears — individual lines shift by 1–4 pixels. At high values (70–100%), lines displace by up to 63 pixels, creating severe horizontal shearing that mimics a physically jarred camera or corrupted video data.

---

#### Knob 2 — Drop Frq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the frame drop frequency. Higher values create more frequent drops. The pot value is quartered as a mask against the 10-bit frame counter — when the masked counter equals zero, the current frame is replaced with near-black. At low values, drops are rare (every 256+ frames). At moderate values, drops occur every few seconds. At high values, drops become frequent enough to make the video barely watchable, simulating a severely overloaded recording system.

---

#### Knob 3 — Bar Pos
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the vertical position of the timestamp bar on screen. The pot value maps directly to a line number, placing the 8-pixel-tall bar at that scanline. At 0%, the bar is at the top of the frame. At 100%, it's near the bottom. The bar is only visible when Stamp (Toggle 9) is enabled.

---

#### Knob 4 — Bounce
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the amplitude of vertical bounce. A triangle-wave oscillator increments once per frame, with the top bit selecting direction (up/down). The pot value scales the bounce offset: below ~12%, no bounce; 12–25%, a gentle ±4-pixel sway; 25–50%, a moderate ±16-pixel bounce; above 50%, the full ±32-pixel range. This models the vertical bobbing of a camera mounted on a walking or running person.

---

#### Knob 5 — Noise
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the noise injection level. The LFSR output is masked and scaled by this pot's value, then added to luma as a signed noise offset. At 0%, no noise is visible. At moderate values (30–50%), a subtle grain appears — consistent with a camera sensor at moderate ISO. At high values (70–100%), aggressive noise dominates the image, simulating a camera operating well beyond its light sensitivity range.

---

#### Knob 6 — Vignette
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls vignette intensity. When Vignette (Toggle 8) is enabled, this pot's value indirectly scales the edge darkening effect. In the VHDL, vignette is independently computed from horizontal position, but this pot can be used in conjunction with vignette enable to control the effect depth. The vignette ramps from near-black at the edge to full brightness 128 pixels inward.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Quality** | 720p | 480p |
| **8 — Codec** | Clean | MPEG |
| **9 — Stamp** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control night vision mode, vignette enable, timestamp enable, an unused toggle, and bypass. Toggle 7 selects normal or night-vision processing. Toggle 8 enables/disables the horizontal edge vignette. Toggle 9 enables/disables the timestamp bar overlay. Toggle 10 is reserved. Toggle 11 bypasses all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) and wet (processed) signal using three parallel interpolators. At 0% the output is the unmodified input; at 100% the output is the full body camera effect. Intermediate values blend the degraded look with the original, useful for subtle surveillance-aesthetic applications.

---

## Guided Exercises

These exercises progress from individual artefacts through combined degradations to the full body camera look.

### Exercise 1: Line Jitter and Noise

<img src={bodycam_exercise1_result} alt="Line Jitter and Noise result"/>
*Line Jitter and Noise — simulated result across source images.*
**Source**: Any moving footage — faces, walking, street scenes.

**Objective**: Understand the LFSR-driven jitter and noise injection.

1. **Add jitter**: Set Distort to about 30%. Subtle horizontal line displacement appears.
2. **Increase jitter**: Push to 70%. Lines shift dramatically — severe shearing visible.
3. **Add noise**: Set Noise to about 40%. A grainy texture appears over the image.
4. **Maximum noise**: Push Noise to 80%. The image becomes heavily degraded.
5. **Correlation**: Note that jitter and noise have a correlated character — they share the same LFSR source.
6. **A/B**: Toggle Bypass to compare clean and degraded versions.

**Key concepts**: LFSR provides correlated noise and jitter, jitter amplitude proportional to pot masking, noise is additive signed offset on luma

---

### Exercise 2: Frame Drops and Timestamp

<img src={bodycam_exercise2_result} alt="Frame Drops and Timestamp result"/>
*Frame Drops and Timestamp — simulated result across source images.*
**Source**: Any footage with continuous motion.

**Objective**: Explore frame drop simulation and timestamp overlay.

1. **Enable timestamp**: Set Stamp to On. A bright bar appears.
2. **Position the bar**: Adjust Bar Pos to place the timestamp at the bottom of frame (~80%).
3. **Observe scrolling**: Watch the alternating bright/dim pattern scroll slowly across the bar.
4. **Add frame drops**: Increase Drop Frq to about 40%. Occasional frames flash to black.
5. **More drops**: Push to 70%. Drops become frequent — the video stutters dramatically.
6. **Drop + timestamp**: Note that during dropped frames, the timestamp bar also disappears (drops have priority).

**Key concepts**: Frame drops replace entire frame with near-black, drop frequency scales with pot masking of frame counter, timestamp has scrolling XOR pattern, drops override timestamp

---

### Exercise 3: Full Body Camera

<img src={bodycam_exercise3_result} alt="Full Body Camera result"/>
*Full Body Camera — simulated result across source images.*
**Source**: Any handheld or moving footage.

**Objective**: Create a complete body camera surveillance aesthetic.

1. **Base degradation**: Distort ~35%, Noise ~30%, Drop Frq ~20%.
2. **Enable vignette**: Set Codec to MPEG (Toggle 8 = vignette on). Edge darkening appears.
3. **Add timestamp**: Enable Stamp. Place at bottom (~85%).
4. **Add bounce**: Set Bounce to about 25%. A gentle vertical sway appears.
5. **Night mode**: Toggle Quality to Night. The image shifts to green monochrome with boosted gain.
6. **Mix for subtlety**: Reduce Mix to about 75% for a more restrained look.

**Key concepts**: All artefacts stack: jitter + noise + drops + vignette + timestamp + bounce + night mode, night mode applies after all other effects, mix allows subtle blending

---


## Tips

- **Jitter + Noise = instant surveillance**: A moderate amount of both (25–40%) immediately sells the body camera look without needing other effects.
- **Night mode last**: Night mode tints everything green — apply it after setting up the other artefacts, as it changes the visual weight of noise and vignette.
- **Subtle drops are most convincing**: Drop Frq at 10–20% creates occasional, unexpected blackouts that feel authentic. Higher rates look more like a broken signal.
- **Timestamp at the bottom**: Real body cameras universally place their timestamps at the bottom of frame. Set Bar Pos to 80–90% for realism.
- **Vignette for framing**: Even without other artefacts, vignette adds a cinematic edge-darkening effect useful for directing attention to the frame centre.
- **Mix for documentary look**: Mix at 50–60% blends the degradation subtly with the original, creating a "reconstructed footage" aesthetic popular in documentaries.
- **Combine with external distortion**: Feed Bodycam after another effect (e.g., Cascade for delay, or Bleach for desaturation) for a layered found-footage aesthetic.

---

## Glossary

| Term | Definition |
|------|------------|
| **AGC (Automatic Gain Control)** | A circuit that automatically adjusts signal amplification to maintain a consistent output level, commonly used in cameras to compensate for changing light conditions. |
| **Chroma** | The color-difference components (U and V) of a YUV video signal, representing hue and saturation independently of brightness. |
| **Codec** | A compression/decompression algorithm used to encode and decode digital video; common examples include MPEG and H.264. |
| **Frame counter** | A hardware register that increments once per video frame, used here to determine frame drop timing. |
| **Galois LFSR** | A variant of the linear feedback shift register where feedback taps are applied via XOR at multiple internal bit positions, producing an efficient pseudo-random bit sequence. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **LFSR (Linear Feedback Shift Register)** | A shift register whose input bit is a linear function of its previous state, producing a deterministic but pseudo-random bit sequence. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived luminance. |
| **Shift-select** | A hardware technique that approximates multiplication by selecting among bit-shifted versions of a value, avoiding the cost of a dedicated multiplier. |
| **Triangle wave** | A periodic waveform that rises and falls linearly, producing a smooth back-and-forth oscillation used here for the vertical bounce effect. |
| **Vignetting** | Darkening of the image periphery relative to the center, typically caused by lens geometry or sensor limitations in real cameras. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
