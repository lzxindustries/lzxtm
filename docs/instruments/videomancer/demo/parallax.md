---
draft: true
sidebar_position: 189
slug: /instruments/videomancer/parallax
title: "Parallax"
image: /img/instruments/videomancer/parallax/parallax_hero.png
---

import parallax_animation from '/img/instruments/videomancer/parallax/parallax_animation.gif';
import parallax_control_panel from '/img/instruments/videomancer/parallax/parallax_control_panel.png';
import parallax_exercise1_result from '/img/instruments/videomancer/parallax/parallax_exercise1_result.gif';
import parallax_exercise2_result from '/img/instruments/videomancer/parallax/parallax_exercise2_result.gif';
import parallax_exercise3_result from '/img/instruments/videomancer/parallax/parallax_exercise3_result.gif';
import parallax_hero from '/img/instruments/videomancer/parallax/parallax_hero.png';

# Parallax

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={parallax_hero} alt="Parallax hero image"/>
*Parallax generating multi-layered horizontal raster bars with depth-based scroll speeds and palette color cycling, evoking classic Amiga demoscene copper effects.*
<img src={parallax_animation} alt="Parallax animated output"/>
*Parallax output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In the 1980s and early 1990s, the Amiga computer's custom Copper coprocessor could change hardware color registers on a per-scanline basis, enabling programmers to produce smooth horizontal color gradients and scrolling raster bar effects that seemed impossible for the era's hardware. Demoscene coders turned these capabilities into an art form — stacking colored bars at different scroll speeds to create an illusion of layered depth, a technique borrowed from parallax scrolling in 2D video games. Parallax brings this aesthetic into the Videomancer pipeline.

A vertical DDS (Direct Digital Synthesis) phase accumulator generates a periodic waveform whose instantaneous value indexes into one of eight curated color palettes per scanline. The V Freq control sets how many bar repetitions fill the screen vertically; the Scroll control sets a signed scroll rate that shifts the entire pattern up or down each frame; and an optional horizontal DDS adds a second oscillation axis, creating 2D plasma-like color variation across the frame. Four waveshaping modes — ramp, triangle, sine approximation, and square — reshape the bar profile from smooth gradients to hard-edged stripes. The input video's luma channel modulates bar brightness through either a multiply (colored glass) or additive (neon glow) blend mode, anchoring the synthesized pattern to the video content.

The name *Parallax* references the apparent displacement of overlapping layers moving at different speeds — the core visual mechanism of demoscene raster bar effects, where stacked color bands scrolling at varied rates create a sense of spatial depth.

---

## Background

### The Amiga Copper and Per-Scanline Color Changes

The Amiga's Copper (co-processor) was a simple DMA-driven state machine that could write to hardware registers at precise horizontal and vertical beam positions. By reprogramming the color palette registers at the start of each scanline, the Copper could produce smooth vertical color gradients — a technique called *copper bars* or *raster bars*. Because the palette change happened in hardware without CPU intervention, the effect was perfectly smooth, even on modest 7 MHz 68000 processors. Demoscene programmers exploited this to create dazzling title screens, loading animations, and music visualizations composed entirely of per-scanline palette manipulation.

### Direct Digital Synthesis for Scrolling

DDS is the standard technique for generating periodic waveforms in digital hardware. A phase accumulator adds a frequency word on each clock cycle; its most significant bits represent the current phase, which can be mapped to any desired waveform shape. In Parallax, the vertical DDS accumulates phase proportional to the current scanline number times the V Freq parameter. A separate scroll offset accumulator increments by a signed speed value each frame, causing the entire bar pattern to slide vertically over time. The result is a smooth, continuous scroll whose speed and direction are controlled by a single knob.

### Palette-Based Color Cycling

Rather than computing RGB values per pixel, Parallax stores eight curated palettes of eight colors each as synthesis-time YUV constants. The top 3 bits of the shaped waveform value index into the selected palette, producing quantized color bands that snap between palette entries. This approach mirrors the Amiga's indexed-color architecture, where the visual richness came not from per-pixel computation but from clever palette selection and per-scanline palette rotation. The eight palettes range from full-spectrum rainbow to monochrome binary alternation, each designed for a specific visual character.

### Video Luma Modulation and Blend Modes

The synthesized bar pattern can interact with the input video through two blend modes. In **multiply** mode, the bar luminance is scaled by the input video's brightness — dark regions of the video suppress the bars, bright regions let them through at full intensity, like looking through tinted glass. In **additive** mode, the bar color is added to the video, producing a neon glow overlay where the synthetic and video signals combine. The Video Depth control sets how strongly the input luma affects the blend, from zero (bars are independent of video) to full (bars are completely modulated by video content).

### Waveshaping and Bar Profiles

Four waveshaping modes transform the DDS phase accumulator output into different bar profiles. **Ramp** (sawtooth) produces asymmetric bars with a gradual rise and sharp drop. **Triangle** folds the phase at the midpoint for symmetric bars. **Sine approximation** smooths the triangle with a bit-shift-based softening algorithm, creating rounder transitions. **Square** hard-clips the phase to produce flat bands with sharp edges — the most graphic, Amiga-authentic look.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── DDS Phase Accumulators ──────────────────────────────────────
│   ├─ v_accum += v_freq per line
│   ├─ h_accum += h_freq per pixel (reset on hsync)
│   ├─ scroll_offset += (scroll - 512) per frame
│   └─ v_accum reset on vsync; scroll_offset held if sync_field
│
├── Clock 1: Phase Computation + Waveshaping ────────────────────
│   ├─ phase_raw = v_accum[MSBs] + scroll_offset[MSBs]
│   ├─ mirror: fold phase at half-frame if enabled
│   ├─ combined = phase_raw + h_phase (if h_enable)
│   ├─ waveshape: ramp / triangle / sine-approx / square
│   └─ register input Y, U, V
│
├── Clock 2: Palette Lookup ─────────────────────────────────────
│   ├─ pal_idx = palette_sel(2:0) & shaped_val[9:7]
│   └─ bar_y, bar_u, bar_v = C_PAL_Y/U/V[pal_idx]
│
├── Clock 3a: Video Modulation (shift-add multiply) ─────────────
│   ├─ video_mod = Y_in × depth[9:7] (3-bit shift-add approx)
│   └─ depth_offset = 1023 - video_depth
│
├── Clock 3b: Blend Output ─────────────────────────────────────
│   ├─ Multiply: blend = video_mod + depth_offset (sat)
│   │            comp_y = bar_y × blend[9:7] (shift-add)
│   │            comp_u = bar_u, comp_v = bar_v
│   └─ Additive: comp_y = bar_y + video_mod (sat)
│                comp_u = (bar_u + U_in) / 2
│                comp_v = (bar_v + V_in) / 2
│
├── Clocks 4–7: Interpolator (wet/dry Mix) ──────────────────────
│   └─ lerp(dry, composed, mix_amount) per Y, U, V
│
├── Sync Signals ────────────────────────────────────────────────
│   └─ 9-stage delay pipeline (hsync_n, vsync_n, field_n, YUV)
│
└── Output Mux ──────────────────────────────────────────────────
    └─ bypass ? delayed_input : mix_result
```

The vertical DDS accumulator is the engine of the effect. It increments by V Freq on every line start, producing a phase ramp that wraps at 16 bits. The scroll offset adds a frame-by-frame displacement to this phase, causing the entire pattern to slide vertically. The waveshaper converts the raw phase into one of four bar profiles before the top 3 bits index into the palette. The video modulation stage uses a 3-bit shift-add approximation of multiplication (checking bits 9, 8, and 7 of the Video Depth register) to scale the input luma, avoiding a hardware multiplier. In multiply mode, the modulated luma and a depth-offset complement are combined and applied as a second shift-add multiply against the bar luminance — a two-stage gain chain that keeps the bars anchored to the video content's brightness structure.

---

## Parameter Reference

<img src={parallax_control_panel} alt="Videomancer front panel with Parallax loaded"/>
*Videomancer's front panel with Parallax active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — V Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the vertical repetition frequency of the bar pattern. At 0%, the accumulator increment is zero and the bars do not repeat — a single color fills the screen. As you increase V Freq, more bar repetitions fit within the frame, progressing from a few wide bands to many thin stripes. The frequency is continuous — every value produces a valid pattern, though fractional periods relative to the frame height create subtle beating aliases.

---

#### Knob 2 — Scroll
| Property | Value |
|----------|-------|
| Range | -180° – 180° |
| Default | 0° |
| Suffix | ° |

Sets the vertical scroll speed and direction. The 10-bit value is converted to a signed offset by subtracting 512: values below center scroll downward, values above center scroll upward, and the center position (512) halts scrolling. The scroll offset accumulates per frame, so the movement is smooth and continuous. Higher values produce faster scroll speeds. When Sync Field is enabled, the scroll offset resets to zero each frame, freezing the pattern in place.

---

#### Knob 3 — H Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the horizontal oscillation frequency for the plasma effect. At 0%, there is no horizontal variation — bars are uniform across the width of the screen. As you increase H Freq, a horizontal DDS accumulator adds a second oscillation axis, creating diagonal or wavy color variation. The horizontal accumulator resets on each hsync, so the pattern repeats identically on every scanline. This control only takes effect when H Enable (Toggle 8) is on.

---

#### Knob 4 — Video Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls how strongly the input video's luma channel modulates the bar brightness. At 0%, the bars are drawn at their full palette brightness regardless of the video content. At 100%, the bars are fully modulated — bright areas of the video show bright bars, dark areas suppress them. The modulation uses a 3-bit shift-add approximation (checking bits 9, 8, 7) for iCE40-compatible computation. In multiply mode, this creates a colored-glass effect; in additive mode, it controls how much video brightness is added to the bar color.

---

#### Knob 5 — Palette
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Selects one of eight color palettes via the top 3 bits of the register. **0: Rainbow** — full spectrum hue cycle. **1: Copper** — warm Amiga copper gradient from dark to bright. **2: Ocean** — deep blues and greens. **3: Neon** — synthwave purples, pinks, and oranges. **4: Phosphor** — terminal green shades. **5: Plasma** — classic demoscene warm-to-cool cycle. **6: Sunset** — warm gradient from dark to bright. **7: Binary** — stark black/white alternation. Each palette contains 8 colors stored as pre-computed YUV constants.

---

#### Knob 6 — Waveshape
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 1 |

Selects the waveshaping mode via the top 2 bits of the register. **0: Ramp** — sawtooth, direct phase output creating asymmetric bars with a gradual rise and sharp drop. **1: Triangle** — phase folded at midpoint for symmetric bars. **2: Sine approx** — smoothed triangle using bit-shift averaging for rounder transitions. **3: Square** — hard-clipped binary output producing flat color bands with sharp edges. Square mode is the most graphic and closest to authentic Amiga copper bar aesthetics.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mirror** | Off | On |
| **8 — H Enable** | Off | On |
| **9 — Blend Mode** | Multiply | Additive |
| **10 — Sync Field** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–11 control five independent processing options. Mirror and H Enable modify the DDS phase geometry, Blend Mode selects between multiply and additive video compositing, Sync Field disables the frame-to-frame scroll accumulation, and Bypass routes the input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) input signal and the wet (raster bar) output. At 0%, the output is pure source video. At 100%, the output is the full raster bar effect. Intermediate values blend the two — useful for subtle overlay effects where the bars add color texture to the source without overwhelming it.

---

## Guided Exercises

These exercises progress from basic raster bars to complex animated colour fields, exploring the interplay between DDS frequency, palette selection, waveshaping, and video modulation.

### Exercise 1: Classic Copper Bars

<img src={parallax_exercise1_result} alt="Classic Copper Bars result"/>
*Classic Copper Bars — simulated result across source images.*
**Objective**: Recreate the iconic Amiga copper bar look — smooth horizontal color bands scrolling vertically on a black background.

1. **Select Copper palette**: Set Palette to position 1 (Copper). The display shows warm amber-to-gold horizontal bands.
2. **Set bar frequency**: Turn V Freq to ~30% for wide, comfortable bars that fill the screen with 4–6 repetitions.
3. **Enable scroll**: Set Scroll to ~60% (above center) for a gentle upward scroll. The bars drift smoothly upward.
4. **Square waveshape**: Set Waveshape to position 3 (Square) for hard-edged flat bands — the most authentic retro look.
5. **Disable video modulation**: Set Video Depth to 0% so the bars are fully independent of the input video.
6. **Observe**: The display should show classic Amiga-style copper bars scrolling vertically — a pure synthesis effect.

**Key concepts**: DDS phase accumulator generates the vertical bar pattern, scroll offset accumulates per frame for smooth motion, square waveshape produces flat bands matching retro aesthetics

---

### Exercise 2: Plasma Color Field

<img src={parallax_exercise2_result} alt="Plasma Color Field result"/>
*Plasma Color Field — simulated result across source images.*
**Objective**: Create a two-dimensional plasma-like color field by combining vertical and horizontal DDS oscillators with a smooth waveshape.

1. **Select Plasma palette**: Set Palette to position 5 (Plasma) for the classic demoscene warm-to-cool cycle.
2. **Set vertical frequency**: V Freq ~40% for moderate vertical repetition.
3. **Enable horizontal oscillator**: Toggle H Enable On and set H Freq to ~35%. Diagonal color bands appear as the horizontal phase combines with the vertical.
4. **Triangle waveshape**: Set Waveshape to position 1 (Triangle) for smooth, symmetric colour transitions.
5. **Enable mirror**: Toggle Mirror On. The pattern reflects from the center, creating a kaleidoscopic symmetry.
6. **Slow scroll**: Set Scroll to ~55% for gentle upward drift. The plasma field undulates slowly.
7. **Observe**: The display shows a 2D color plasma reminiscent of classic demoscene effects, with symmetric reflections and smooth colour cycling.

**Key concepts**: Horizontal DDS adds a second dimension to the bar pattern, mirror creates bilateral symmetry, triangle waveshape produces smooth gradients, palette selection defines the overall colour character

---

### Exercise 3: Neon Video Overlay

<img src={parallax_exercise3_result} alt="Neon Video Overlay result"/>
*Neon Video Overlay — simulated result across source images.*
**Objective**: Use additive blend mode and video modulation to overlay neon-coloured raster bars onto live footage, creating a vivid colour-treated image.

1. **Select Neon palette**: Set Palette to position 3 (Neon) for synthwave purples and pinks.
2. **Set video depth**: Turn Video Depth to ~70%. The bars will be strongly influenced by the video brightness.
3. **Additive blend**: Toggle Blend Mode to Additive. The bar colours add to the video signal, creating glowing highlights.
4. **Moderate frequency**: V Freq ~25% for wide colour bands that wash across the frame.
5. **Ramp waveshape**: Set Waveshape to position 0 (Ramp) for asymmetric colour transitions — gradual on one side, sharp on the other.
6. **Scroll for animation**: Scroll ~45% (gentle downward) for slow colour cycling over the video.
7. **Adjust mix**: Pull Mix to ~70% to let some of the original video show through unaffected.

**Key concepts**: Additive blend mode creates neon glow overlays, video depth modulation anchors bars to video brightness, mix control blends original and processed for subtlety

---


## Tips

- **Square waveshape for retro authenticity**: The square waveshape produces flat colour bands with hard edges — the closest visual match to original Amiga copper bar effects.
- **Ramp for asymmetry**: The ramp (sawtooth) waveshape creates bars that rise gradually and drop sharply, producing a distinctive directional quality that interacts well with vertical scrolling.
- **Palette 7 (Binary) for strobing**: The black/white alternating palette combined with square waveshape creates dramatic high-contrast stripe patterns suitable for projection onto three-dimensional objects.
- **Video Depth at ~50% for glass effects**: With multiply blend, moderate Video Depth creates a coloured-glass overlay where the video content is visible through tinted horizontal bands.
- **H Enable + Mirror for kaleidoscope**: Combining horizontal oscillation with vertical mirroring creates symmetric 2D colour fields reminiscent of kaleidoscope patterns.
- **Sync Field for composition**: Enable Sync Field to freeze the bar pattern while adjusting frequency, palette, and waveshape. Once the composition looks right, disable Sync Field to let it animate.
- **Feedback with raster bars**: Routing Parallax output back to the input with additive blend creates self-reinforcing colour accumulation — the bars compound in brightness with each pass, producing vivid neon streaks.
- **Mix at 30–50% for texture**: Full-strength raster bars can overwhelm video content. Pull Mix to 30–50% for a subtle colour wash that adds retro character without obscuring the picture.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive blend** | A compositing mode where pixel values are summed, producing brighter results where both signals are present; creates a neon glow effect. |
| **Copper** | The Amiga computer's co-processor, capable of changing hardware registers at specific beam positions to create per-scanline colour effects. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator incremented by a frequency word each clock cycle. |
| **Demoscene** | A computer art subculture focused on creating real-time audio-visual productions (demos) that push hardware to its limits. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that implements the video processing pipeline in hardware. |
| **Multiply blend** | A compositing mode where pixel values are multiplied, producing darker results where either signal is dark; creates a coloured-glass effect. |
| **Palette** | An indexed set of predefined colours; in Parallax, 8 palettes of 8 colours each provide the bar colouring. |
| **Phase accumulator** | A digital counter that wraps at its maximum value, producing a periodic ramp used as the basis for DDS waveform generation. |
| **Raster bar** | A horizontal band of colour produced by changing the display palette on a per-scanline basis, a signature effect of 1980s–90s demoscene productions. |
| **Waveshaping** | The process of transforming a raw phase ramp into a specific waveform profile (triangle, sine, square, etc.) for different visual bar profiles. |
| **YUV** | A color space that separates luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |
