---
draft: true
sidebar_position: 264
slug: /instruments/videomancer/sideband
title: "Sideband"
image: /img/instruments/videomancer/sideband/sideband_hero.png
description: "Before cable and digital broadcasting, television reception was an analog adventure."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import sideband_hero from '/img/instruments/videomancer/sideband/sideband_hero.png';
import sideband_control_panel from '/img/instruments/videomancer/sideband/sideband_control_panel.png';
import sideband_exercise1_result from '/img/instruments/videomancer/sideband/sideband_exercise1_result.png';
import sideband_exercise2_result from '/img/instruments/videomancer/sideband/sideband_exercise2_result.png';
import sideband_exercise3_result from '/img/instruments/videomancer/sideband/sideband_exercise3_result.png';
import sideband_source1_kodim15 from '/img/instruments/videomancer/sideband/sideband_source1_kodim15.png';
import sideband_source2_kodim01 from '/img/instruments/videomancer/sideband/sideband_source2_kodim01.png';
import sideband_source3_stream_bridge_512 from '/img/instruments/videomancer/sideband/sideband_source3_stream_bridge_512.png';

# Sideband

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: sideband_source1_kodim15, after: sideband_hero },
    { label: "Kodim01", before: sideband_source2_kodim01, after: sideband_hero },
    { label: "Stream Bridge", before: sideband_source3_stream_bridge_512, after: sideband_hero },
  ]}
/>
*Sideband degrading a clean video signal with multipath ghost echoes, herringbone interference, rolling hum bars, and snow noise.*

---

## Overview

Before cable and digital broadcasting, television reception was an analog adventure. The signal traveled through the air as an RF carrier, arriving at the antenna along multiple paths — direct, reflected off buildings, scattered by terrain. Each path introduced its own delay, creating faint displaced copies of the image called *ghosts*. Adjacent-channel transmitters leaked energy into the tuned channel as herringbone interference patterns. Mains hum from the power supply crept into the signal chain as slowly rolling brightness bars. And when the signal was too weak, random noise replaced the picture as static snow. Sideband recreates all four of these degradation artifacts simultaneously, turning any clean digital video into a convincing simulation of marginal analog reception.

The program chains five processing stages in series: a BRAM-based ghost delay line produces displaced echo images, a DDS oscillator generates herringbone interference, a triangle-wave modulator adds hum bars, and an LFSR noise generator crossfades between signal and snow. The name *Sideband* refers to the frequency sidebands of a modulated RF carrier — the mechanism by which adjacent-channel interference occurs in analog broadcasting. Every artifact in this program has a direct physical analog in the RF reception chain.

At subtle settings — a faint ghost, a hint of hum, high signal strength — Sideband adds a warm analog patina to clean digital video. At extreme settings — deep ghosts, heavy interference, low signal strength — it reduces the signal to near-unintelligible static, evoking late-night UHF reception on a portable television with rabbit-ear antennas.

---

## Background

### Multipath Ghost Images

When a television signal bounces off a building or hillside before reaching the antenna, it arrives slightly later than the direct signal. The receiver adds the delayed copy to the primary image, creating a *ghost* — a faint, horizontally displaced duplicate. The displacement distance depends on the extra path length (approximately 1 microsecond per 300 meters of additional travel). In severe multipath environments, multiple ghosts can appear at different offsets and intensities. Sideband simulates this using a 1024-pixel BRAM delay line for each of the Y, U, and V channels, with controllable delay offset and echo amplitude.

### Herringbone Interference

Analog television channels are spaced at fixed frequency intervals (6 MHz in NTSC, 7 or 8 MHz in PAL). When a receiver's selectivity is insufficient to fully reject the adjacent channel, the beat frequency between the two carriers produces a fine diagonal or horizontal stripe pattern across the screen called *herringbone* interference. Sideband generates this using a DDS (direct digital synthesis) phase accumulator that advances per pixel, with an optional per-line offset that tilts the pattern diagonally. The resulting square wave is scaled by the Interference control and added to the luminance channel.

### Mains Hum Bars

Power supply filtering in consumer television receivers was often imperfect. The 50 Hz or 60 Hz AC mains frequency would leak into the video signal path, producing slowly rolling horizontal bars of brightness variation called *hum bars*. A receiver with severe hum might show 2–5 bars drifting vertically through the picture. Sideband simulates this with a triangle wave whose phase is derived from the vertical line position within each frame, plus a frame-to-frame phase accumulator that controls the scroll speed.

### Snow Noise

When the received signal strength drops below the receiver's noise floor, the automatic gain control amplifies both signal and noise equally. At very low signal levels, the random thermal and shot noise in the tuner's front end dominates the picture, producing the characteristic *snow* or *static* — random white and black dots covering the screen. Sideband models this as a crossfade between the processed signal and LFSR pseudo-random noise, controlled by the Signal Strength parameter. The noise can be fine (per-pixel) or coarse (sample-and-hold over several pixels for a blockier, more "analog" texture).

### Color Loss in Weak Signals

In analog NTSC and PAL broadcasting, the chrominance subcarrier sits on top of the luminance signal at a higher frequency. Because higher frequencies attenuate faster in a noisy channel, color information degrades before brightness information as signal strength drops. This is why a weak analog TV signal would often show a recognizable but desaturated or monochrome image before dissolving completely into snow. Sideband's Color Loss toggle doubles the effective noise level for the U/V channels, causing chroma to disappear at higher signal strengths than luminance.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input + BRAM Write ────────────────────────────────
│   ├─ Current pixel → BRAM write (Y, U, V)
│   ├─ Ghost 1 read at h_count − ghost_delay/4
│   └─ Ghost 2 read at h_count − ghost_delay/2
│
├── Stage 2: Ghost Summation ───────────────────────────────────
│   ├─ Ghost 1: scale by ghost_gain
│   ├─ Ghost 2: scale by ghost_gain / 2 (dual mode only)
│   ├─ Polarity: add or subtract based on Ghost Pol
│   └─ Clamp Y/U/V to 0..1023
│
├── Stage 3: Herringbone Interference ──────────────────────────
│   ├─ DDS phase accumulator (per pixel)
│   ├─ Diagonal tilt: +4096/line when enabled
│   ├─ Square wave: ±256 from MSB of phase
│   ├─ Scale by interference × interference / 1024
│   └─ Add to Y only
│
├── Stage 4: Hum Bar ───────────────────────────────────────────
│   ├─ Phase = frame_phase + v_count × 32
│   ├─ Triangle wave centered at 0
│   ├─ Scale by hum_level
│   └─ Add to Y only
│
├── Stage 5: Snow Noise Mix ────────────────────────────────────
│   ├─ noise_level = 1023 − signal_strength
│   ├─ Y = signal × strength + noise × noise_level
│   ├─ Color Loss: double chroma noise level
│   └─ Coarse mode: sample-and-hold noise every N pixels
│
├── Interpolator: Wet/Dry Mix (4 clocks) ──────────────────────
│   └─ Crossfade between delayed dry input and processed output
│
└── Output ─────────────────────────────────────────────────────
    └─ Always through interpolator (no bypass toggle)
```

The five degradation stages are chained in the order they would occur in a real analog receiver: the ghost arrives first (it is a property of the RF propagation path), then adjacent-channel interference adds its pattern, then power supply hum modulates the brightness, and finally noise is mixed in based on overall signal quality. Each stage feeds the next, so a ghosted signal also gets hum bars applied to it, and the combined result gets noise mixed in. Herringbone and hum affect luminance only (matching the real-world behavior where these artifacts primarily disturb the baseband video), while snow noise affects all three channels. Note that there is no bypass toggle — toggle_switch_11 controls the noise texture type (fine vs. coarse), and the Mix fader controls the wet/dry blend via the interpolator.

---

## Parameter Reference

<img src={sideband_control_panel} alt="Videomancer front panel with Sideband loaded"/>
*Videomancer's front panel with Sideband active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Ghost Delay
| Property | Value |
|----------|-------|
| Range | 0px – 256px |
| Default | 32px |
| Suffix | px |

Controls the horizontal displacement of the ghost image in pixels. The top 8 bits of the 10-bit register select a delay from 0 to 255 pixels. At 0, no ghost is visible (the delayed copy overlaps the original exactly). As you increase the delay, a displaced copy of the image appears shifted to the right. In Dual Ghost mode, a second ghost appears at double the delay distance. Large delay values push the ghost far enough that it becomes a clearly separate image rather than a subtle edge echo.

---

#### Knob 2 — Ghost Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Sets the amplitude of the ghost echo. At 0%, the ghost is invisible regardless of delay. At moderate values, the ghost appears as a faint overlay — a semi-transparent displaced copy typical of mild multipath interference. At high values, the ghost becomes as bright as the original signal, creating a strong double-image effect. In Dual Ghost mode, the second ghost receives half this gain, producing a realistic cascading reflection pattern where each successive reflection is weaker than the previous one.

---

#### Knob 3 — Interference
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the amplitude of the herringbone interference pattern. At 0%, no interference is visible. As you increase the control, a fine stripe pattern appears across the image. The pattern frequency is determined by the DDS accumulator's increment rate (which is also scaled by this parameter), so higher Interference values produce both a stronger and finer pattern. With Interference Tilt set to Diagonal, the stripes angle across the screen, closely matching real adjacent-channel interference.

---

#### Knob 4 — Hum Level
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the depth of the hum bar brightness modulation. At 0%, no hum bars are visible. Increasing the control makes slowly rolling horizontal bands of brighter and darker video appear across the frame. The bars come from a triangle wave with approximately 5 cycles per frame (from the v_count × 32 term), creating the characteristic wide horizontal bands of a badly filtered power supply. The hum affects all channels equally through the luminance path.

---

#### Knob 5 — Signal Str
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls overall signal quality — the balance between clean video and noise. At 100%, the signal is fully clean with no snow noise. As you decrease the control, random noise begins mixing into the signal. At very low values, the picture dissolves almost entirely into static. This parameter works as an inverse noise level: noise_level = 1023 − signal_strength. When Color Loss is enabled, the chroma channels degrade at twice the rate of luminance, producing a desaturated image before total signal loss.

---

#### Knob 6 — Hum Roll
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the vertical scroll speed of the hum bars. The register value is added to a 16-bit frame phase accumulator on each vertical sync pulse. At 0%, the hum bars are stationary (frozen in place). As you increase the roll speed, the bars begin drifting vertically through the frame. Higher values create faster rolling, simulating a receiver with increasingly poor power supply regulation. The scroll is continuous and wraps smoothly.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Ghost Pol** | Pos | Neg |
| **8 — Dual Ghost** | Single | Dual |
| **9 — Color Loss** | Off | On |
| **10 — Interf Tilt** | Horiz | Diag |
| **11 — Noise Type** | Fine | Coarse |

The five toggles modify different aspects of the degradation chain. Ghost Pol (toggle 7) and Dual Ghost (toggle 8) affect the ghost summation stage. Color Loss (toggle 9) modifies the snow noise mix for chroma channels. Interf Tilt (toggle 10) adds diagonal drift to the herringbone pattern. Noise Type (toggle 11) selects between fine per-pixel noise and coarse blocked noise. Unlike many Videomancer programs, there is no bypass toggle — the Mix fader serves as the wet/dry control, and toggle 11 is repurposed for noise texture selection.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade via the output interpolator. At 0%, the output is the original clean signal with no degradation artifacts. At 100%, the output is the fully processed signal with all active artifacts. This serves as both a mix control and an effective bypass — setting Mix to 0% completely removes all artifacts. Intermediate values create a partial blend that can suggest a signal that is degraded but not fully compromised.

---

## Guided Exercises

These exercises progress from individual artifact exploration through combined degradation to full weak-signal simulation. Each exercise isolates one aspect of the program before combining them.

### Exercise 1: Ghost Delay and Polarity

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: sideband_source1_kodim15, after: sideband_exercise1_result },
    { label: "Kodim01", before: sideband_source2_kodim01, after: sideband_exercise1_result },
    { label: "Stream Bridge", before: sideband_source3_stream_bridge_512, after: sideband_exercise1_result },
  ]}
/>
*Ghost Delay and Polarity — simulated result across source images.*
**Source**: A high-contrast test pattern or graphics-heavy footage with sharp vertical edges — text, geometric shapes, or architectural details.

**Objective**: Understand how ghost delay, gain, polarity, and dual mode interact to create multipath echo effects.

1. Set all controls to neutral: Interference 0%, Hum Level 0%, Signal Strength 100%. This isolates the ghost stage.
2. Set Ghost Gain to ~50% and slowly increase Ghost Delay from 0. A faint displaced copy of the image appears, shifting rightward.
3. Increase Ghost Gain to see the echo strengthen. At 100% the ghost is as bright as the original.
4. Toggle Ghost Pol to Negative. The ghost becomes a dark shadow instead of a bright overlay.
5. Enable Dual Ghost. A second, weaker ghost appears further displaced. Note the cascading echo pattern.
6. Sweep Ghost Delay through its full range with Dual Ghost enabled to see both echoes shift in tandem.

**Key concepts**: Ghost delay is a BRAM line buffer read at an offset, gain scales the echo amplitude, negative ghosts subtract from the signal, dual ghost adds a second reflection at 2× delay and 0.5× gain

---

### Exercise 2: Interference and Hum Bars

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: sideband_source1_kodim15, after: sideband_exercise2_result },
    { label: "Kodim01", before: sideband_source2_kodim01, after: sideband_exercise2_result },
    { label: "Stream Bridge", before: sideband_source3_stream_bridge_512, after: sideband_exercise2_result },
  ]}
/>
*Interference and Hum Bars — simulated result across source images.*
**Source**: A flat or slowly varying image — a solid color field, a gentle gradient, or a static scene with minimal detail to make the interference pattern clearly visible.

**Objective**: Explore herringbone interference patterns and hum bar modulation as independent artifacts.

1. Set Ghost Gain to 0% and Signal Strength to 100% to isolate the interference and hum stages.
2. Slowly increase Interference from 0%. A fine horizontal stripe pattern appears on the image.
3. Toggle Interf Tilt to Diagonal. The stripes tilt into a classic herringbone weave pattern.
4. Return Interference to 0% and increase Hum Level. Broad horizontal brightness bands appear across the frame.
5. Increase Hum Roll to set the bars in motion — they scroll vertically through the frame.
6. Combine both: set moderate Interference (~40%) and moderate Hum Level (~40%). The fine herringbone pattern is superimposed on the broader hum bands, creating a layered degradation.

**Key concepts**: Herringbone is a DDS-generated square wave added to Y, diagonal tilt adds phase offset per line, hum bars are a triangle wave modulated by vertical position

---

### Exercise 3: Weak Signal Simulation

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: sideband_source1_kodim15, after: sideband_exercise3_result },
    { label: "Kodim01", before: sideband_source2_kodim01, after: sideband_exercise3_result },
    { label: "Stream Bridge", before: sideband_source3_stream_bridge_512, after: sideband_exercise3_result },
  ]}
/>
*Weak Signal Simulation — simulated result across source images.*
**Source**: Any video — this exercise works best with recognizable content so you can judge the degradation level.

**Objective**: Simulate the progressive degradation of a weak analog TV signal, from mild noise through color loss to total snow.

1. Set moderate ghost (Delay ~64 px, Gain ~30%), light interference (~20%), light hum (~20%). This creates a baseline of mild reception artifacts.
2. Slowly lower Signal Strength from 100% toward 0%. Snow noise begins mixing into the picture.
3. At ~60% signal strength, the image is still recognizable but noticeably noisy. Enable Color Loss — the image desaturates as chroma noise increases at double rate.
4. Switch Noise Type from Fine to Coarse. The noise becomes blockier and more "analog" in character.
5. Continue lowering Signal Strength. At ~20%, the image is barely visible through the snow.
6. At ~5%, the picture is almost entirely static with only occasional hints of the original content visible through the noise.
7. Toggle Color Loss off and on at ~40% signal strength to see the dramatic difference in chroma noise.

**Key concepts**: Signal strength inversely controls noise mix ratio, color loss doubles chroma noise rate, coarse mode samples-and-holds noise for blockier texture, all artifacts compound in series

---


## Tips

- **Isolate each artifact separately first**: Set Ghost Gain to 0, Interference to 0, Hum Level to 0, and Signal Strength to 100 to create a clean baseline. Then introduce one artifact at a time to understand its contribution.
- **Negative ghosts for edge enhancement**: A subtle negative ghost at small delay creates a dark outline along vertical edges, similar to a sharpening effect. This can add visual detail rather than degradation.
- **Dual ghost for depth**: The cascading echo pattern of dual ghost mode creates a sense of spatial depth — the image appears to recede into layered reflections.
- **Color Loss sells the illusion**: Enabling Color Loss makes weak signal simulation dramatically more convincing. Real analog TV always lost color before luminance, and viewers instinctively recognize this degradation pattern.
- **Coarse noise for vintage character**: Fine noise looks like modern digital sensor noise. Coarse noise, with its blocked sample-and-hold texture, more closely resembles the bandwidth-limited noise of a real analog tuner.
- **Hum Roll for animation**: Even a static image comes alive when hum bars are rolling. The slow vertical drift creates constant motion that suggests a live, unstable signal.
- **Combine with feedback for progressive degradation**: Route the output back to the input. Each pass through the ghost delay, interference, and noise stages compounds the degradation, creating a signal that deteriorates over time — like a VHS tape being copied repeatedly.
- **Mix as a performance control**: Use the Mix fader to cross-fade between clean and degraded signal in real time. This creates a dramatic reveal effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used here for the ghost delay line (1024×10-bit per channel). |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator, used here for herringbone interference generation. |
| **Ghost** | A displaced, attenuated copy of the video image caused by multipath signal propagation, where the RF signal arrives via both direct and reflected paths. |
| **Herringbone** | A fine diagonal or horizontal stripe pattern caused by adjacent-channel interference beating against the desired signal's carrier frequency. |
| **Hum Bar** | A slowly rolling horizontal band of brightness variation caused by AC mains frequency leaking into the video signal path. |
| **LFSR** | Linear Feedback Shift Register; a hardware pseudo-random number generator that produces noise sequences for the snow effect. |
| **Multipath** | The simultaneous reception of a signal via multiple propagation paths (direct, reflected, diffracted), causing ghost images. |
| **Noise Floor** | The level of background noise in a receiver; signals below the noise floor are unrecoverable. |
| **Sample-and-Hold** | A circuit technique that captures a value and holds it for multiple clock cycles, used in coarse noise mode. |
| **Sideband** | The frequency components above and below a modulated carrier that contain the signal information; the source of adjacent-channel interference. |
| **Snow** | Random white-and-black noise visible on an analog TV screen when signal strength is insufficient, caused by thermal noise in the receiver. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
