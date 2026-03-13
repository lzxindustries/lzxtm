---
draft: true
sidebar_position: 66
slug: /instruments/videomancer/copperwash
title: "Copperwash"
image: /img/instruments/videomancer/copperwash/copperwash_hero.png
description: "Copper Wash generates per-scanline colour gradients that scroll vertically through the video frame, blending continuous rainbow bands with the input signal."
---

import copperwash_hero from '/img/instruments/videomancer/copperwash/copperwash_hero.png';
import copperwash_animation from '/img/instruments/videomancer/copperwash/copperwash_animation.gif';
import copperwash_control_panel from '/img/instruments/videomancer/copperwash/copperwash_control_panel.png';
import copperwash_exercise1_result from '/img/instruments/videomancer/copperwash/copperwash_exercise1_result.gif';
import copperwash_exercise2_result from '/img/instruments/videomancer/copperwash/copperwash_exercise2_result.gif';
import copperwash_exercise3_result from '/img/instruments/videomancer/copperwash/copperwash_exercise3_result.gif';

# Copperwash

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<img src={copperwash_hero} alt="Copperwash hero image"/>
*Smooth rainbow bands cascade down the frame, tinting live video with the liquid colour gradients of the Amiga copper coprocessor.*
<img src={copperwash_animation} alt="Copperwash animated output"/>
*Copperwash output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Copper Wash generates per-scanline colour gradients that scroll vertically through the video frame, blending continuous rainbow bands with the input signal. The effect replicates the Amiga's copper coprocessor, which could change palette registers on every scanline to produce smooth colour gradients otherwise impossible on indexed-colour hardware. Here, a sine-based hue-to-YUV conversion produces an infinitely smooth continuous spectrum rather than stepping through palette entries.

The name references the Commodore Amiga's "copper" — a coprocessor that executed display lists synchronised to the raster beam. Copper bars, copper gradients, and copper rainbows were among the most recognised visual signatures of the Amiga demo scene from 1986 onward.

Four gradient modes are available — Rainbow, Warm, Cool, and Mono — each biasing the hue space toward different colour temperatures. Wobble adds sinusoidal per-scanline phase modulation that warps the straight gradient bands into undulating liquid waves. The gradient can be blended with the input video via multiply (tinting) or additive (glowing overlay) modes.

---

## Quick Start

1. **Scroll Speed exactly at centre** (512) stops all motion, useful for static colour grading effects.
2. **Low frequency + Warm/Cool mode** produces subtle colour temperature grading across the frame, ideal for tinting landscape footage.
3. **Wobble + H Spread** together create the most complex plasma-like patterns as bands wave both horizontally and vertically.

---

## Background

### The Amiga Copper Coprocessor

The copper was a custom DMA controller that could wait for specific beam positions and then write to hardware registers — typically colour palette entries. By loading new colour values on each scanline, programmers created smooth vertical gradients on hardware that normally supported only 32 or 64 simultaneous colours. This per-line colour manipulation became the defining visual technique of the Amiga demo scene.

### Per-Scanline Colour Gradients

Unlike pixel-by-pixel colouring, per-scanline gradients apply uniform colour to each horizontal line. The human eye perceives this as a smooth wash because the vertical resolution of colour is limited to one value per line. This matches how CRT displays render — one line at a time — and creates the characteristic banded look of copper effects.

### Hue-to-YUV via Sine

The program converts hue angle to YUV colour space using paired sine and cosine evaluations: U = sin(phase), V = sin(phase + 90°). This traces a circle through the UV chrominance plane, producing all spectrum hues at constant saturation. Different gradient modes compress or bias this circle to favour certain colour temperatures — warm (red/yellow), cool (blue/cyan), or mono (luminance only).

### Wobble Modulation

The per-line phase wobble is itself sinusoidal, producing S-shaped undulations in the gradient bands. The wobble frequency changes slowly over time via its own phase accumulator, creating an organic, liquid appearance as bands weave back and forth. This mimics the "plasma" effects that extended basic copper gradients in many Amiga demos.


---

## Signal Flow

```
registers_in ──→ [Register Map] ──→ scroll speed, freq, hue offset,
                                    saturation, wobble, brightness
                                    toggles: gradient, blend, spread, smooth, bypass

                ┌─────────────────────────────────────┐
                │          VBLANK ANIMATION            │
                │  scroll_phase += speed − 512         │
                │  wobble_phase += 3                   │
                └─────────────────────────────────────┘

data_in ──→ [Stage 1: Gradient Phase]
              phase = v_count × freq + scroll + hue_offset
              + h_count × freq (if spread)
              + sine(wobble) × wobble_amount
              stepped or smooth quantization
                        │
                   s_grad_phase
                        │
                        ▼
            [Stage 2: Hue-to-YUV]
              U = sine(phase), V = sine(phase + 256)
              gradient mode selects bias:
                Rainbow / Warm / Cool / Mono
                        │
                  s_grad_y/u/v
                        │
                        ▼
            [Stage 3: Saturation + Brightness]
              chroma × saturation / 1024
              luma × brightness / 1024
                        │
                 s_scaled_y/u/v
                        │
                        ▼
            [Stage 4: Blend with Input]
              Multiply: out_y = input_y × grad_y / 1024
              or Add: out_y = input_y + grad_y (clamped)
                        │
                   s_gen_y/u/v
                        │
                        ▼
            [interpolator_u × 3]
              wet/dry crossfade
                        │
                        ▼
                   data_out
```

The gradient phase computation in stage 1 is the heart of the program. The scanline number multiplied by the frequency control determines how many colour bands span the screen height. Adding the scroll phase creates the scrolling animation, while the hue offset rotates the starting colour. Wobble adds a per-line sinusoidal offset that makes the bands undulate. The smooth/stepped toggle determines whether the gradient phase is quantized to 64 discrete steps (stepped) or uses the full 10-bit resolution (smooth), creating either visible colour bands or a seamless wash.

---

## Parameter Reference

<img src={copperwash_control_panel} alt="Videomancer front panel with Copperwash loaded"/>
*Videomancer's front panel with Copperwash active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Scroll Speed
| Property | Value |
|----------|-------|
| Range | -90deg – 90deg |
| Default | 12deg |
| Suffix | deg |

Scroll Speed controls the vertical scrolling velocity of the gradient. At centre (512) the gradient is stationary. Clockwise speeds scroll the bands downward; counter-clockwise reverses direction. The bipolar implementation uses a DDS accumulator, meaning even small offsets from centre produce slow, steady drift. At extreme speeds the colours cascade rapidly through the spectrum.

---

#### Knob 2 — Gradient Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Gradient Freq sets the number of colour cycles visible across the screen height. At minimum the entire screen shows a single colour transition. At maximum, dense rainbow bands stripe the frame. The frequency multiplies the scanline number, so increasing this control compresses the colour wavelength. Moderate values (30–60%) produce the most visually pleasing gradient spacing.

---

#### Knob 3 — Hue Offset
| Property | Value |
|----------|-------|
| Range | -180deg – 180deg |
| Default | 0deg |
| Suffix | deg |

Hue Offset rotates the starting hue of the gradient around the colour wheel. At 0° the gradient starts at a reference hue; sweeping through 360° cycles through all starting colours. When Scroll Speed is zero, Hue Offset allows manual colour selection. When scrolling, it shifts the entire animation phase.

---

#### Knob 4 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Saturation scales the chroma intensity of the gradient from zero (grey) to full colour. At zero, only the luminance component of the gradient remains, producing a monochrome wash. At full saturation, the hues are vivid. The scaling is applied around the 512 chroma midpoint to preserve colour balance.

---

#### Knob 5 — Wobble
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Wobble adds sinusoidal per-scanline phase modulation to the gradient. At zero the bands are perfectly straight horizontal lines. Increasing wobble creates increasingly pronounced S-shaped undulations in the colour bands, producing a liquid or plasma-like appearance. The wobble frequency evolves slowly over time, creating organic movement patterns.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Brightness scales the luminance of the generated gradient from black to full intensity. In multiply blend mode, this controls how much of the input video's brightness is preserved. In additive mode, it controls how much additional brightness the gradient contributes.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Gradient** | Rainbow | Mono |
| **8 — Blend** | Multiply | Add |
| **9 — H Spread** | Off | On |
| **10 — Smooth** | Steps | Smooth |
| **11 — Bypass** | Off | On |

The five toggles configure gradient colour mode, blend behaviour, spatial spread, quantization, and bypass. Gradient mode selects the colour temperature bias. Blend mode determines how the gradient combines with the input video. H Spread adds a horizontal component to the gradient for diagonal washes. Smooth toggles between quantized colour steps and continuous interpolation.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the dry (unprocessed) input and the wet (gradient-blended) output. At 0% the output matches the input. At 100% the full gradient effect is visible.





---

## Guided Exercises

These exercises demonstrate copper wash effects from classic rainbow scrolling to warm tinting to liquid plasma.

### Exercise 1: Classic Copper Rainbow Scroll

<img src={copperwash_exercise1_result} alt="Classic Copper Rainbow Scroll result"/>
*Classic Copper Rainbow Scroll — simulated result across source images.*
**What You'll Create**: Achieve the classic Amiga copper rainbow gradient scrolling over video.

1. Set Gradient to Rainbow and Blend to Multiply.
2. Scroll Speed to a gentle forward pace (~580).
3. Gradient Freq to 30% for 3–4 visible colour bands.
4. Saturation at 75%, Brightness at 80%.
5. Wobble at 0 for straight bands, Smooth enabled.
6. Observe the smooth rainbow tinting the input video as it scrolls down.
7. Increase Freq to see more colour bands compress.

**Key concepts**: - Multiply blend tints the input proportionally to gradient brightness
- Smooth mode creates seamless colour transitions
- Scroll speed is bipolar — centre is stationary

---

### Exercise 2: Warm Sunset Tint

<img src={copperwash_exercise2_result} alt="Warm Sunset Tint result"/>
*Warm Sunset Tint — simulated result across source images.*
**What You'll Create**: Apply a warm sunset colour wash using the warm gradient mode.

1. Set Gradient to Warm, Blend to Multiply.
2. Scroll Speed to 0 (stationary gradient).
3. Gradient Freq to 15% — broad colour bands.
4. Hue Offset to 70% to select an orange/gold starting hue.
5. Saturation at 60%, Brightness at 85%.
6. Enable Smooth, disable H Spread.
7. The landscape should appear tinted in warm sunset tones.

**Key concepts**: - Warm mode attenuates blue, biasing toward red and yellow hues
- Stationary gradient with hue offset allows manual colour selection
- Low frequency creates broad, gentle colour zones

---

### Exercise 3: Liquid Plasma Wash

<img src={copperwash_exercise3_result} alt="Liquid Plasma Wash result"/>
*Liquid Plasma Wash — simulated result across source images.*
**What You'll Create**: Create a psychedelic liquid plasma effect using wobble and additive blending.

1. Set Gradient to Rainbow, Blend to Add.
2. Scroll Speed to 560 (gentle scroll).
3. Gradient Freq to 50% for medium band density.
4. Wobble to 75% for pronounced undulation.
5. Enable H Spread for diagonal wave movement.
6. Saturation at 90%, Brightness at 50%.
7. Set Smooth to Steps for visible colour banding.
8. The result should resemble a classic demoscene plasma.

**Key concepts**: - Wobble creates sinusoidal band warping for organic movement
- H Spread makes bands diagonal, adding spatial complexity
- Stepped mode creates visible colour bands typical of retro plasma
- Additive blend makes the gradient glow over dark backgrounds

---


## Tips

- **Stepped mode** at low frequency gives a classic Amiga copper bar look with clearly defined colour regions.
- **Multiply blend** preserves input video contrast and detail better than additive, making it the preferred mode for subtle tinting.
- **High frequency + smooth** produces a dense, seamless rainbow that blends into a soft pastel wash when viewed at normal distance.

---
