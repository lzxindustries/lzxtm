---
draft: true
sidebar_position: 260
slug: /instruments/videomancer/slitscan
title: "Slit Scan"
image: /img/instruments/videomancer/slitscan/slitscan_hero.png
description: "Slit Scan captures a narrow vertical strip of the input image each frame and writes it into a scrolling BRAM framebuffer."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import slitscan_hero from '/img/instruments/videomancer/slitscan/slitscan_hero.png';
import slitscan_control_panel from '/img/instruments/videomancer/slitscan/slitscan_control_panel.png';
import slitscan_exercise1_result from '/img/instruments/videomancer/slitscan/slitscan_exercise1_result.png';
import slitscan_exercise2_result from '/img/instruments/videomancer/slitscan/slitscan_exercise2_result.png';
import slitscan_exercise3_result from '/img/instruments/videomancer/slitscan/slitscan_exercise3_result.png';
import slitscan_source1_kodim02 from '/img/instruments/videomancer/slitscan/slitscan_source1_kodim02.png';
import slitscan_source2_kodim07 from '/img/instruments/videomancer/slitscan/slitscan_source2_kodim07.png';
import slitscan_source3_kodim01_bw from '/img/instruments/videomancer/slitscan/slitscan_source3_kodim01_bw.png';

# Slit Scan

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: slitscan_source1_kodim02, after: slitscan_hero },
    { label: "Kodim07", before: slitscan_source2_kodim07, after: slitscan_hero },
    { label: "Kodim01 B&W", before: slitscan_source3_kodim01_bw, after: slitscan_hero },
  ]}
/>
*Time made visible — each column captures a different moment, scrolling a slit of live video into an ever-shifting streak panorama.*

---

## Overview

Slit Scan captures a narrow vertical strip of the input image each frame and writes it into a scrolling BRAM framebuffer. As new strips arrive, older ones shift sideways, building a panoramic streak image where every column represents a different instant in time. The result is a spatio-temporal map: the horizontal axis becomes a timeline, and movement through the scene draws ribbon-like trails across the display.

The name references the photographic slit-scan technique pioneered by Douglas Trumbull for the Star Gate corridor in *2001: A Space Odyssey* (1968). Traditional slit-scan uses a mechanical slit moving across film stock to streak light sources into abstract trails. Videomancer implements this digitally, replacing the mechanical slit with a pixel-column sampler and the film strip with a 160×68-pixel BRAM framebuffer that scrolls at a controllable rate.

At full scroll speed with moderate decay, a busy scene produces dense psychedelic ribbons of color. At slow speed with minimal decay, the result is closer to a long-exposure photograph with temporal smearing. Combined with the hue-shift control, the streaks can be tinted through the full rainbow spectrum while the brightness control adjusts the overall luminance of the buffer readout.

---

## Background

### The Slit-Scan Camera

Douglas Trumbull's original slit-scan rig exposed each frame of film through a narrow slit while backlit artwork moved past on a glass platen. The camera shutter remained open for the full length of the artwork pass, producing a single-frame image in which every horizontal stripe came from a different moment of the artwork's motion. The technique creates flowing, taffy-like distortions that are impossible to achieve through conventional lens or filter methods.

### Time as Space

Slit-scan is a member of a broader class of spatio-temporal manipulations in which time is encoded as a spatial axis. Related devices include the streak camera (used in ballistics and laser diagnostics to record nanosecond events), the keyed optical printer, and various real-time video slit-scan implementations developed by John Whitney Sr. and others in the 1960s–70s. The core idea is that collapsing one spatial dimension and replacing it with time allows a two-dimensional display to encode three dimensions of information.

### Framebuffer Scrolling

The FPGA implementation stores the streak image in a 160×68-pixel BRAM framebuffer (10,880 bytes, 3 BRAM tiles). Each frame, the write column advances and the captured strip overwrites the oldest data. A separate decay pass during vertical blanking fades all existing pixels, creating a natural temporal decay that darkens old streaks. The read pipeline maps the current screen position to the circular framebuffer, offsetting by the write column so that the most recent capture always appears at the same screen position.

### Decay and Persistence

The decay mechanism subtracts a configurable amount from every pixel in the framebuffer once per frame during the vertical blanking interval. This approximates the phosphor persistence of a long-persistence CRT or the bleaching of photographic emulsion. At maximum decay, old data vanishes almost instantly, leaving only a narrow recent strip. At zero decay, data persists indefinitely, and the buffer fills with an additive collage of every frame sampled since reset.

### Hue Tinting

The color mapping is simplified from a full look-up table into four quadrant zones based on the hue-shift register: red-warm (V+), green-cool (U−, V−), blue-cold (U+, V−), and neutral monochrome. The chroma offset is proportional to the luminance of the framebuffer pixel, so bright streaks carry more color saturation while dark areas remain near grey. This produces the classic tinted-oscilloscope look associated with early video art.


---

## Signal Flow

```
Input Y ──→ [Strip Sample] ──→ [FB Write] ──→ [BRAM 160×68]
                                                     │
                         [Decay Pass (vblank)] ◄─────┘
                                                     │
 Screen Pos ──→ [Addr Gen] ──→ [FB Read] ──→ [Brightness] ──→ [Hue Tint]
                                                                    │
                                                              ┌─────┘
 Input Y/U/V ──→ [Delay SR] ──→ [Interpolator Mix] ◄─ wet ──┘
                                        │
                                   Output Y/U/V
```

The framebuffer operates as a circular buffer with a single write column per frame. The decay pass runs during vertical blanking, sweeping through all 10,880 bytes in a three-phase read-modify-write cycle. The read pipeline maps screen coordinates to buffer coordinates by offsetting by the current write column, so the newest data always appears at the left edge of the display. The interpolator mix provides the dry/wet crossfade, blending the raw input with the streak output.

Strip sampling happens during active video: when the horizontal pixel counter matches the Strip Pos register, the current input luminance is grabbed and written to the current write column in the framebuffer. The vertical position is decimated by 1/16 to fit within the 68-row buffer.

---

## Parameter Reference

<img src={slitscan_control_panel} alt="Videomancer front panel with Slit Scan loaded"/>
*Videomancer's front panel with Slit Scan active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Strip Pos
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the horizontal pixel position of the capture slit. Sweeping this control across the frame selects which vertical strip of the input is sampled each frame. At the centre position, the slit captures the middle column of the image. Moving it left or right samples the corresponding edge region. When combined with camera movement, the slit position determines which part of the scene contributes to the streak trail.

---

#### Knob 2 — Scroll Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the rate at which the write column advances frame-by-frame. At zero, the write position is frozen and the same column is continuously overwritten. At maximum, the write column advances every frame, scrolling rapidly. Intermediate values use a fractional accumulator so the scroll rate can be sub-frame — advancing one column every several frames for slow, smooth scrolling.

---

#### Knob 3 — Strip Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 6% |
| Suffix | % |

Adjusts the width of the capture strip in pixels. At the minimum setting, only a single pixel column is sampled. At wider settings, multiple adjacent columns within the strip are grabbed, averaging them into the write column and producing a smoother, less aliased streak. Very wide strips capture a broader swath of the input, approaching a temporal blur rather than a slit-scan effect.

---

#### Knob 4 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Sets the per-frame decay rate applied to all pixels in the framebuffer during vertical blanking. At zero, old data never fades and the buffer fills with an additive collage. At maximum, old data fades almost instantly, showing only the most recent few strips. Moderate values create a phosphor-persistence effect where trails gradually dim over several frames.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Multiplies the luminance of the framebuffer readout. At centre (512), the brightness is approximately unity — what was captured is what is displayed. Below centre, the streaks are dimmed. Above centre, the streaks are amplified, potentially clipping bright areas. This control is applied after the decay pass, so it does not affect how fast old data fades — only how bright the streaks appear at output.

---

#### Knob 6 — Hue Shift
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

Rotates the hue tint applied to the streak output. The control sweeps through four quadrant zones: warm red-orange (0°–90°), cool green (90°–180°), cold blue-purple (180°–270°), and neutral monochrome (270°–360°). The chroma intensity is proportional to the luminance of each pixel, so only bright streaks carry visible color while dark areas remain desaturated.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Axis** | Vertical | Horizontal |
| **8 — Direction** | Right | Left |
| **9 — Trail** | Streak | Mirror |
| **10 — Freeze** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control orientation, scroll direction, trail mode, freeze, and bypass. Axis and Direction together determine which axis the slit-scan operates along and which way the timestamp columns advance. Trail mode switches between a continuously scrolling streak and a mirror-bounce mode that reverses at buffer edges. Freeze halts all buffer updates while the read pipeline continues to display the last captured state. Bypass passes the dry input through unchanged.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the dry input signal and the processed slit-scan output. At 0% (fader down), the output is pure dry — the original video passes through unchanged. At 100% (fader up), the output is the full slit-scan streak image. Intermediate positions blend the two, allowing the live input to be ghosted behind or in front of the streak layer.

---

## Guided Exercises

These exercises progress from a simple temporal streak through colored time-lapse trails to frozen panoramic snapshots. Each exercise introduces new controls while reinforcing the core slit-scan concept.

### Exercise 1: Basic Time Streak

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: slitscan_source1_kodim02, after: slitscan_exercise1_result },
    { label: "Kodim07", before: slitscan_source2_kodim07, after: slitscan_exercise1_result },
    { label: "Kodim01 B&W", before: slitscan_source3_kodim01_bw, after: slitscan_exercise1_result },
  ]}
/>
*Basic Time Streak — simulated result across source images.*
**Source**: A live camera feed with a slowly moving subject — a walking person, swaying plant, or rotating object works well.

**Objective**: Understand how the capture slit samples a column of the input each frame and scrolls it into a temporal panorama.

1. **Single-strip streak**: Set Strip Pos to ~50%, Scroll Spd to ~30%, Strip Width to minimum. Push Mix fader to 100%. A thin vertical slice of the scene is captured and scrolled across the display, building a ribbon of time.
2. **Observe motion encoding**: Move the camera slowly. Notice how horizontal motion in the scene appears as diagonal streaks in the output — faster motion creates steeper diagonals.
3. **Adjust speed**: Increase Scroll Spd to ~60%. The streaks compress temporally — more frames fit on screen, but each strip is thinner and the image scrolls faster.
4. **Apply decay**: Set Decay to ~40%. Old columns now fade gradually, creating a ghostly phosphor trail effect. Only the most recent several columns remain bright.
5. **Reverse direction**: Toggle Direction to Left. The streak now scrolls in the opposite direction.

**Key concepts**: Time-to-space mapping via column sampling, scroll rate controls temporal resolution, decay creates persistence effects, direction reverses the temporal axis

---

### Exercise 2: Hue-Tinted Temporal Ribbons

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: slitscan_source1_kodim02, after: slitscan_exercise2_result },
    { label: "Kodim07", before: slitscan_source2_kodim07, after: slitscan_exercise2_result },
    { label: "Kodim01 B&W", before: slitscan_source3_kodim01_bw, after: slitscan_exercise2_result },
  ]}
/>
*Hue-Tinted Temporal Ribbons — simulated result across source images.*
**Source**: A source with varied brightness — a lit candle, neon sign, or high-contrast scene with both bright and dark areas.

**Objective**: Apply hue tinting and brightness to create colored temporal ribbons that shift with the luminance of the captured content.

1. **Prepare streak**: Set Strip Pos ~50%, Scroll Spd ~25%, Strip Width ~10%, Mix 100%.
2. **Set warm hue**: Turn Hue Shift to ~45° (warm red-orange). Bright streaks glow with an amber tint while dark areas stay neutral grey.
3. **Increase brightness**: Push Brightness above 50% to amplify the tinted streaks. Watch how the color saturation increases with luminance.
4. **Sweep hue**: Slowly rotate Hue Shift through the full 360°. Notice the four quadrant zones — warm, cool, cold, and monochrome.
5. **Add decay**: Set Decay to ~50%. The tinted trails now fade over time, creating a rainbow afterglow effect as different frames carry different hue densities.
6. **Mirror bounce**: Toggle Trail to Mirror. The streak now bounces back and forth, creating a symmetric bilateral pattern of colored ribbons.

**Key concepts**: Hue tinting maps luminance to chroma proportionally, brightness amplifies both luma and chroma, mirror mode creates palindromic time-symmetric patterns

---

### Exercise 3: Frozen Panoramic Snapshot

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: slitscan_source1_kodim02, after: slitscan_exercise3_result },
    { label: "Kodim07", before: slitscan_source2_kodim07, after: slitscan_exercise3_result },
    { label: "Kodim01 B&W", before: slitscan_source3_kodim01_bw, after: slitscan_exercise3_result },
  ]}
/>
*Frozen Panoramic Snapshot — simulated result across source images.*
**Source**: A slowly rotating scene or panning camera — a turntable with an object or a long slow pan across a landscape.

**Objective**: Use the freeze function to capture a complete slit-scan panorama and hold it as a static image for compositing.

1. **Prepare slow scan**: Set Strip Pos to ~50%, Scroll Spd to ~15%, Decay to 0% (no fade), Mix 100%.
2. **Observe accumulation**: With Decay at zero, every captured strip persists indefinitely. Watch as the buffer fills with a complete panoramic record of the rotating subject.
3. **Wait for full fill**: Allow the buffer to fill completely (takes several seconds at low scroll speed). The display is now a complete temporal panorama — every column is a different moment.
4. **Freeze**: Toggle Freeze to On. The panorama locks in place as a static image.
5. **Composite**: Pull Mix fader to ~50%. The frozen panorama overlays the live input, creating a ghostly double-exposure effect.
6. **Capture different moment**: Toggle Freeze off, let the buffer update for a few seconds, then Freeze again to capture a new panorama.

**Key concepts**: Zero decay preserves all data for long-term accumulation, freeze halts all updates for static capture, mix enables live compositing over the frozen panorama

---


## Tips

- **Start with no decay**: Set Decay to 0% when learning the controls. This lets you see the full accumulated buffer without fading, making it easier to understand the relationship between slit position and streak output.
- **Slow scroll for detail**: Low Scroll Spd values produce higher temporal resolution — each strip occupies the buffer for many frames, capturing fine motion details.
- **Hue follows brightness**: The hue tinting is proportional to luminance, so dark areas stay neutral. Feed bright, high-contrast content for the most vivid color trails.
- **Freeze for compositing**: Use Freeze to capture a panoramic snapshot, then adjust Mix to overlay it against live video for double-exposure effects.
- **Mirror for symmetry**: Mirror mode creates bilateral time-symmetric patterns that are particularly effective with rhythmic or periodic source motion.
- **Wide strips smooth aliasing**: Increase Strip Width to average multiple adjacent pixel columns into each captured strip, reducing aliasing in the temporal direction.
- **Axis swap for vertical time**: Switch Axis to Horizontal for a vertical timeline — useful for scrolling time upward or downward through the frame.
- **Bypass for comparison**: Use Toggle 11 for instant A/B comparison without changing any other settings.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM (Block RAM)** | Dedicated memory blocks in the FPGA fabric, used here for the 160×68 pixel framebuffer that stores the streak image. |
| **Decay** | A per-frame subtraction applied to every pixel in the framebuffer during vertical blanking, simulating phosphor persistence by gradually fading old data. |
| **Framebuffer** | A two-dimensional pixel array stored in BRAM that holds the accumulated streak image and is read out each frame for display. |
| **Interpolator** | A hardware crossfade unit that blends two signals by a configurable ratio, used here for the wet/dry mix between the slit-scan output and the dry input. |
| **Slit-scan** | A photographic/video technique in which a narrow aperture (slit) exposes successive strips of an image over time, converting temporal change into spatial displacement. |
| **Spatio-temporal** | Relating to both space and time; in slit-scan, one spatial axis is replaced by a time axis, creating a hybrid space-time image. |
| **Streak** | The continuous trail left by the slit-scan process as the captured strip scrolls across the framebuffer, encoding temporal movement as horizontal displacement. |
| **Vertical blanking** | The interval between video frames when no active pixels are displayed, used by the program to perform framebuffer maintenance (decay pass, scroll advancement). |

---
