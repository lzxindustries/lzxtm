---
draft: true
sidebar_position: 277
slug: /instruments/videomancer/vigil
title: "Vigil"
image: /img/instruments/videomancer/vigil/vigil_hero.png
description: "Program guide for Vigil, a Videomancer camera program for the LZX video synthesizer."
---

import vigil_before_after from '/img/instruments/videomancer/vigil/vigil_before_after.png';
import vigil_control_panel from '/img/instruments/videomancer/vigil/vigil_control_panel.png';
import vigil_exercise1_result from '/img/instruments/videomancer/vigil/vigil_exercise1_result.png';
import vigil_exercise2_result from '/img/instruments/videomancer/vigil/vigil_exercise2_result.png';
import vigil_exercise3_result from '/img/instruments/videomancer/vigil/vigil_exercise3_result.png';
import vigil_hero from '/img/instruments/videomancer/vigil/vigil_hero.png';
import vigil_source1_kodim05 from '/img/instruments/videomancer/vigil/vigil_source1_kodim05.png';
import vigil_source2_kodim15 from '/img/instruments/videomancer/vigil/vigil_source2_kodim15.png';
import vigil_source3_kodim15_bw from '/img/instruments/videomancer/vigil/vigil_source3_kodim15_bw.png';

# Vigil

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={vigil_hero} alt="Vigil hero image"/>
*Vigil degrading a live camera feed into a grainy, desaturated CCTV surveillance image with scanline noise bands, horizontal tearing, line dropouts, and a timestamp bar overlay.*
<img src={vigil_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Vigil applied.*

---

## Overview

Security cameras do not produce beautiful images. They produce images that are good enough — captured by cheap CMOS sensors behind plastic lenses, compressed by decade-old codecs, transmitted over degraded coaxial cable, and displayed on monitors that have been running 24 hours a day for years. The result is a distinctive visual language: low contrast, heavy desaturation, visible scanline noise, horizontal tearing, and the ever-present timestamp burned into the bottom of the frame. Vigil recreates this entire degradation chain as a real-time video effect.

The program chains ten processing stages together — vertical rolling, horizontal tearing, scanline noise injection, line dropout, desaturation, vignette darkening, luma inversion, timestamp overlay, glitch mix crossfade, and frame freeze. Two independent 16-bit LFSRs (Linear Feedback Shift Registers) provide decorrelated pseudo-random noise sources for the horizontal displacement and amplitude domains. The name *Vigil* refers to the act of keeping watch — the tireless, unblinking observation that defines surveillance camera footage.

At subtle settings Vigil adds a gentle surveillance-camera patina to any footage. At extreme settings it creates heavily corrupted, nearly unwatchable glitch video that evokes the worst moments of found-footage horror films and leaked security tapes.

---

## Background

### CCTV Image Degradation

Closed-circuit television systems prioritize reliability and uptime over image quality. A typical CCTV installation uses cameras with 1/3-inch sensors producing 480 or 576 interlaced lines, connected via RG-59 coaxial cable to a multiplexer or DVR. Signal degradation accumulates at every stage: sensor noise in low light, impedance mismatches causing reflections, ground loops introducing hum bars, and lossy compression in the recorder. The resulting images exhibit characteristic artifacts — scanline noise bands that drift vertically, occasional horizontal displacement of entire lines, and random line dropouts where the signal briefly fails.

### Horizontal Tearing and Sync Errors

When the horizontal sync timing of a video signal is disrupted, individual scanlines shift left or right relative to their neighbors. This creates the characteristic *horizontal tearing* seen in improperly terminated or damaged analog video connections. In CCTV systems, this often occurs when multiple cameras share a single coaxial cable via a multiplexer — switching between cameras can introduce brief sync disturbances. Vigil simulates this by applying a random horizontal offset to the pixel position counter on selected lines, displacing the pixel data without altering the actual sync signals.

### Rolling Shutter and Vertical Roll

When a monitor loses vertical sync lock with the incoming video signal, the image appears to *roll* — the frame boundary scrolls continuously up or down the screen. This was a common fault in aging CRT monitors connected to CCTV systems. Vigil simulates this by accumulating a per-frame offset to the vertical position counter, causing all processing that depends on vertical position (noise bands, vignette, timestamp) to shift smoothly through the frame. The roll speed is continuously variable from stationary to rapid scrolling.

### LFSR Noise Generation

Linear Feedback Shift Registers produce deterministic pseudo-random sequences that repeat after $2^n - 1$ cycles. A 16-bit maximal-length LFSR produces 65,535 unique values before repeating — long enough that the pattern is visually indistinguishable from true randomness at video frame rates. Vigil uses two decorrelated LFSRs (seeded with different initial values, 0xDEAD and 0xBEEF) to generate independent noise streams for the horizontal and amplitude domains, preventing correlated artifacts.

### Vignette and Corner Darkening

Security cameras with wide-angle lenses exhibit significant light falloff at the edges of the frame — a phenomenon called *vignetting*. The effect is stronger with cheaper lenses and smaller sensors. Vigil computes vignetting using the Chebyshev (maximum of horizontal and vertical) distance from the frame center, which is cheaper than true radial distance and produces a slightly rectangular falloff pattern that matches the look of rectangular sensor vignetting.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├─ 1. Roll Offset ─────────── vertical position accumulator (shifts band positions)
├─ 2. Horizontal Tear ─────── LFSR-driven random line displacement (implicit in h_count)
├─ 3. Scanline Noise ──────── LFSR noise added to luma in rolling noise bands
├─ 4. Line Dropout ─────────── random whole-line blanking to black
├─ 5. Desaturation ─────────── UV blend toward neutral (512)
├─ 6. Vignette ────────────── Chebyshev distance darkening from edges
├─ 7. Luma Invert ─────────── optional Y-channel complement
├─ 8. Timestamp Bar ───────── white rectangle overlay on lower portion of frame
├─ 9. Glitch Mix ──────────── crossfade between clean input and glitched output
├─ 10. Freeze ─────────────── hold last output (stops counter updates)
│
└── Output Video (YUV 4:4:4)
```

The roll offset is accumulated per-field based on the Roll Speed parameter, affecting the apparent vertical position of noise bands and other position-dependent effects. Scanline noise uses LFSR A to generate noise bands that drift vertically via the roll accumulator — the noise_mode toggle selects between pseudo-random LFSR-driven bands and a deterministic periodic stripe pattern. The Glitch Mix fader crossfades between the original clean input and the fully processed glitch output, allowing partial glitch blending rather than a binary on/off. The Freeze toggle stops updating the output registers, holding the last processed frame indefinitely — it does not stop the LFSRs, so unfreezing reveals a new noise state.

---

## Parameter Reference

<img src={vigil_control_panel} alt="Videomancer front panel with Vigil loaded"/>
*Videomancer's front panel with Vigil active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Scan Noise
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity and probability of scanline noise bands. At zero, no noise is added. As the value increases, broader and stronger noise bands appear across the image, drifting vertically when Roll Speed is active. The noise hits hardest on luma, creating horizontal brightness streaks that are characteristic of analog signal degradation. The Noise Mode toggle (Toggle 10) selects between LFSR-driven random flickering bands and a fixed periodic stripe pattern.

---

#### Knob 2 — H-Tear
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls horizontal line displacement — random per-frame offsets that shift entire scanlines left or right. At zero the image is stable. As you increase the value, lines begin to jitter horizontally, creating the characteristic *tearing* of a poorly terminated analog video connection. Higher values produce more dramatic displacement, breaking the vertical alignment of the image.

---

#### Knob 3 — Roll Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 6.3% |
| Suffix | % |

Controls the speed of vertical rolling. At zero the image is stationary. As the value increases, the frame boundary scrolls upward through the image at increasing speed, simulating loss of vertical sync. The roll affects the position of noise bands, vignette, and the timestamp overlay — everything that depends on the vertical position counter.

---

#### Knob 4 — Dropout
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 6.3% |
| Suffix | % |

Controls the probability of line dropout — complete blanking of random scanlines to black. At zero no lines drop out. As you increase the value, more lines per frame are replaced with black, creating horizontal black streaks that flash randomly across the image. The dropout decision is made per-line at the start of each line using LFSR B, so dropout patterns change every frame.

---

#### Knob 5 — Desaturate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Blends the chrominance channels toward neutral (U=512, V=512), progressively removing color. At zero the image retains full color; at maximum it is pure monochrome. Most CCTV cameras produce relatively desaturated images even when shooting in color, so moderate desaturation (50–80%) creates the most realistic surveillance look.

---

#### Knob 6 — Vignette
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of radial darkening from the frame edges. At zero there is no vignette. As the value increases, the edges and corners of the frame darken progressively, concentrating visual attention on the center. The vignette is computed using Chebyshev distance (max of horizontal and vertical distance from center), producing a slightly rectangular falloff pattern.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Luma Invert** | Off | On |
| **8 — Timestamp** | Off | On |
| **9 — Intlc Jitter** | Off | On |
| **10 — Noise Mode** | LFSR | Pattern |
| **11 — Freeze** | Off | On |

The five toggles control independent processing features. Toggles 7–10 enable specific signal degradation modes. Toggle 11 is the Freeze function, not a bypass — use the Glitch Mix fader at 0% for a clean signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Glitch Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the original clean input and the fully processed surveillance-degraded output. At 0% the output is the unmodified source; at 100% the full glitch processing is applied. This fader is labeled "Glitch Mix" rather than "Mix" to emphasize that it controls the balance between clean and degraded signal paths.

---

## Guided Exercises

These exercises progress from subtle surveillance aesthetic to full analog signal destruction. Each builds on the previous, layering degradation effects.

### Exercise 1: Basic Surveillance Look

<img src={vigil_exercise1_result} alt="Basic Surveillance Look result"/>
*Basic Surveillance Look — simulated result across source images.*
**Source**: Indoor footage with mixed lighting — office scenes, hallways, or room interiors work well.

**Objective**: Create a convincing CCTV surveillance camera aesthetic with desaturation, vignette, and timestamp.

1. Set Desaturate to about 80% to wash out most of the color.
2. Set Vignette to about 40% for subtle corner darkening.
3. Enable the Timestamp toggle. Observe the white bar at the bottom of the frame.
4. Set Scan Noise to about 15% for just a hint of noise band activity.
5. Set Glitch Mix to 100% to see the full effect.
6. Toggle Desaturate between different values to find the sweet spot between "cheap color camera" and "full monochrome."

**Key concepts**: Desaturation and vignette create the base surveillance look, the timestamp bar is the universal CCTV identifier, subtle noise sells the effect without overwhelming it

---

### Exercise 2: Signal Degradation

<img src={vigil_exercise2_result} alt="Signal Degradation result"/>
*Signal Degradation — simulated result across source images.*
**Source**: Outdoor footage with movement — traffic, pedestrians, or nature scenes with motion.

**Objective**: Add horizontal tearing and line dropout to simulate a failing analog video connection.

1. Start from the Exercise 1 surveillance base (Desaturate ~80%, Vignette ~40%, Timestamp on).
2. Increase H-Tear to about 15%. Watch lines begin to shift horizontally.
3. Add Dropout at about 10%. Random black lines flash across the image.
4. Increase Scan Noise to about 30%. Noise bands become clearly visible.
5. Set Roll Speed to about 10%. The frame begins to scroll slowly upward.
6. Enable Intlc Jitter for an additional layer of field-bounce artifacts.
7. Pull Glitch Mix back to about 70% to let some clean image show through.

**Key concepts**: H-Tear, dropout, and noise stack as independent degradation layers, Roll Speed shifts the vertical position of noise bands, Glitch Mix controls the degradation intensity more precisely than individual controls

---

### Exercise 3: Total Signal Destruction

<img src={vigil_exercise3_result} alt="Total Signal Destruction result"/>
*Total Signal Destruction — simulated result across source images.*
**Source**: Any footage — the heavy processing will obscure most content.

**Objective**: Push all degradation controls to their extremes for abstract glitch video.

1. Set Scan Noise to about 70% for heavy noise band coverage.
2. Set H-Tear to about 50% for dramatic horizontal displacement.
3. Set Roll Speed to about 40% for rapid vertical scrolling.
4. Set Dropout to about 30% for frequent line blanking.
5. Desaturate to 100% for full monochrome.
6. Vignette to about 60% for strong edge darkening.
7. Enable Luma Invert for a negative-image surveillance look.
8. Switch Noise Mode to Pattern for structured stripes instead of random bands.
9. Use Freeze to capture a single frame of the destruction, then unfreeze to see the noise jump.
10. Sweep Glitch Mix to find the balance between recognizable and abstract.

**Key concepts**: All degradation stages compound, LFSR vs Pattern noise creates different visual textures, Freeze captures a single moment of the evolving noise state, Luma Invert changes the entire tonal character

---


## Tips

- **No bypass toggle**: Vigil uses all five toggles for features. Use the Glitch Mix fader at 0% for a clean passthrough.
- **Subtle sells it**: The most convincing surveillance look uses low values — 15% noise, 5% H-tear, 80% desaturate. Heavy settings look like glitch art rather than CCTV.
- **Pattern mode for texture**: Switch Noise Mode to Pattern for structured horizontal bands that resemble analog interference rather than random digital noise.
- **Roll Speed for unease**: Even a tiny amount of Roll Speed (5%) creates a subtle drift that signals "something is wrong with this signal" without being overtly glitchy.
- **Freeze for stills**: Use Freeze to capture a single degraded frame, creating a "surveillance still capture" look for compositions or overlays.
- **Luma Invert surprise**: Inverting luma on top of a desaturated, vignetted image creates a distinctive negative-CCTV look that reads as "infrared camera" to most viewers.
- **Layer with Viewfinder**: Feed Vigil's output into Viewfinder for a surveillance camera being monitored through a camcorder viewfinder — double-degradation aesthetic.

---

## Glossary

| Term | Definition |
|------|------------|
| **CCTV** | Closed-Circuit Television; a video surveillance system where cameras feed directly to monitors or recorders without broadcast transmission. |
| **Chebyshev Distance** | Maximum of horizontal and vertical distances; produces a rectangular distance field rather than circular. |
| **DVR** | Digital Video Recorder; the recording device in modern CCTV installations that stores compressed camera feeds. |
| **Ground Loop** | An electrical interference condition caused by multiple grounding points creating a current loop, producing horizontal noise bars in video signals. |
| **Interlace** | A scanning method where odd and even lines are drawn in alternating fields, used by analog video standards (NTSC, PAL). |
| **LFSR** | Linear Feedback Shift Register; a shift register whose input bit is a linear function of its previous state, generating pseudo-random sequences. |
| **Multiplexer** | A device that switches between multiple camera inputs on a single monitor or recording channel. |
| **Pipeline** | Sequential processing stages where each stage's output feeds the next on each clock cycle. |
| **Scanline** | A single horizontal line of video; analog video is transmitted and displayed one scanline at a time. |
| **Sync** | Synchronization signals (horizontal and vertical) that tell the display where each line and frame begins. |
| **Tearing** | Horizontal displacement of scanlines caused by sync timing errors, creating a jagged vertical edge in the image. |
| **Vignette** | Gradual darkening at the edges and corners of an image, caused by lens light falloff or sensor geometry. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |
