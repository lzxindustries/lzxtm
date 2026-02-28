---
draft: true
sidebar_position: 67
slug: /instruments/videomancer/degauss
title: "Degauss"
image: /img/instruments/videomancer/degauss/degauss_hero.png
description: "Program guide for Degauss, a Videomancer tube program for the LZX video synthesizer."
---

import degauss_hero from '/img/instruments/videomancer/degauss/degauss_hero.png';
import degauss_before_after from '/img/instruments/videomancer/degauss/degauss_before_after.png';
import degauss_control_panel from '/img/instruments/videomancer/degauss/degauss_control_panel.png';
import degauss_exercise1_result from '/img/instruments/videomancer/degauss/degauss_exercise1_result.png';
import degauss_exercise2_result from '/img/instruments/videomancer/degauss/degauss_exercise2_result.png';
import degauss_exercise3_result from '/img/instruments/videomancer/degauss/degauss_exercise3_result.png';

# Degauss

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={degauss_hero} alt="Degauss hero image"/>
*Degauss applying vertical-position-dependent chroma offsets to create rainbow color fringing reminiscent of a CRT degaussing coil sweep.*
<img src={degauss_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Degauss applied.*

---

## Overview

Every cathode-ray tube shipped from the factory with its electron beams converged — red, green, and blue landing precisely on their respective phosphor dots. The earth's magnetic field, nearby speakers, or even the metal chassis of the monitor itself could slowly magnetize the shadow mask, pulling the beams out of alignment. The fix was a degaussing coil — a ring of wire pulsed with alternating current that neutralized the stray magnetism. If you were lucky, the colors snapped back into place. If you triggered the coil at the wrong moment, or the field was particularly strong, you got a spectacular wash of rainbow fringing that rippled across the screen before settling.

Degauss recreates that chromatic misalignment as a deliberate effect. It takes the chroma channels of the input signal — U and V — and offsets them in opposite directions based on a triangle wave derived from vertical screen position. The luminance channel passes through untouched, so the brightness structure of the image remains intact while the color information slides apart, producing bands of saturated hue shift that ripple from top to bottom. The name comes directly from the CRT maintenance procedure that inspired the effect: Karl Friedrich Gauss, whose work on magnetic fields gave us the unit of magnetic flux density, and the prefix *de-* meaning to remove.

At conservative settings, Degauss produces subtle color fringing at the edges of objects — a gentle chromatic aberration that feels like a slightly misaligned monitor. At extreme settings, the chroma offsets become so large that the image dissolves into horizontal rainbows of pure color, with the original content visible only as luminance structure beneath the shifting hues.

---

## Background

### CRT Degaussing and the Degaussing Coil

A cathode-ray tube display uses three electron beams — one for each primary color — aimed through a perforated metal sheet called a **shadow mask** or **aperture grille**. For a sharp, color-neutral image, all three beams must land on their correct phosphor dots simultaneously. External magnetic fields can deflect the beams unevenly, causing one color to shift relative to the others. Most CRT monitors included an internal **degaussing coil** — a loop of wire wrapped around the tube face — that automatically pulsed a decaying alternating current at power-on to neutralize accumulated magnetism. The characteristic *thunk* and brief color ripple when turning on an older monitor was the degaussing circuit at work.

### Convergence and Misconvergence

**Convergence** describes the condition where all three electron beams meet at the same point on the phosphor screen. A perfectly converged display shows white as a single sharp dot of overlapping red, green, and blue. **Misconvergence** occurs when the beams diverge — typically in a position-dependent pattern that varies from the center to the edges of the screen. Horizontal misconvergence shifts red and blue apart along the scan line; vertical misconvergence shifts them apart between scan lines. The resulting color fringing is most visible on high-contrast edges: white text on a black background develops red and cyan halos. Degauss models vertical-position-dependent misconvergence, where the offset amount varies sinusoidally from top to bottom of the raster.

### Color Fringing and Chromatic Aberration

In optics, **chromatic aberration** occurs when a lens fails to focus all wavelengths to the same point. In CRT terminology, the equivalent artifact is **color fringing** — different color channels landing at slightly different spatial positions. The visual effect is similar: high-contrast edges develop rainbow halos. Degauss creates color fringing by offsetting the U and V chroma channels in opposite directions. Because U and V encode color on perpendicular axes in color space (roughly blue-yellow and red-cyan), opposite offsets produce complementary color shifts that create the full-spectrum rainbow characteristic of real CRT misconvergence.

### Shadow Mask and Aperture Grille

The **shadow mask** is a thin metal plate perforated with hundreds of thousands of tiny holes, one for each pixel triad. The **aperture grille** (used in Trinitron-type displays) replaces the holes with vertical wires. Both serve the same purpose: ensuring each electron beam hits only its corresponding phosphor. When the shadow mask becomes magnetized, it acts as a weak lens for the electron beams, bending them differentially by color. The degaussing coil demagnetizes the mask, restoring beam alignment. In severe cases, the residual magnetism creates visible color patches — regions of the screen with a persistent tint — that only a strong external degaussing wand can clear.

### Analog Nostalgia and the Aesthetics of Malfunction

CRT artifacts — misconvergence, color purity errors, phosphor bloom, raster geometry distortion — are increasingly valued as aesthetic elements in video art, music visuals, and retro-styled media. The appeal lies in the tension between order and disorder: the underlying image remains recognizable, but the display's imperfect reproduction adds an organic, unpredictable layer. Degaussing artifacts are particularly photogenic because they produce pure, saturated color in smooth gradients — the rainbow bands have a painterly quality that feels both technical and beautiful. Degauss lets you dial in precisely how much of that beautiful malfunction you want, from barely perceptible to total chromatic dissolution.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Timing Detection ──────────────────────────────────────────
│   ├─ Hsync/Vsync edge detection (falling edge)
│   ├─ X counter (per pixel), Y counter (per line)
│   └─ Frame counter (16-bit, increments on vsync when Animate=On)
│
├── Triangle Wave Generation ──────────────────────────────────
│   ├─ v_y_phase = y_counter + frame_counter(9:0)
│   └─ v_mod = v_y_phase(7:0) XOR replicated v_y_phase(8)
│       (folds ascending ramp into triangle wave, 0–255)
│
├── Chroma Offset Calculation ─────────────────────────────────
│   ├─ v_offset_u = +(v_mod AND Intensity)
│   └─ v_offset_v = -v_offset_u
│
├── Y Channel ─────────────────────────────────────────────────
│   └─ Pass-through (no processing)
│
├── U Channel ─────────────────────────────────────────────────
│   └─ clamp(data_in.u + v_offset_u, 0, 1023)
│
├── V Channel ─────────────────────────────────────────────────
│   └─ clamp(data_in.v + v_offset_v, 0, 1023)
│
├── Wet/Dry Mix (3× interpolator_u, 4 clocks each) ───────────
│   ├─ mix_y: lerp(dry_y, proc_y, Mix)
│   ├─ mix_u: lerp(dry_u, proc_u, Mix)
│   └─ mix_v: lerp(dry_v, proc_v, Mix)
│
├── Sync Delay Pipeline (8 clocks) ────────────────────────────
│   └─ hsync_n, vsync_n, field_n, Y, U, V delayed to match
│
├── Bypass Mux ────────────────────────────────────────────────
│   └─ Bypass=Off → mixed output; Bypass=On → delayed dry
│
└── Output (YUV 4:4:4)
```

The core of Degauss is a single interaction: a triangle wave derived from vertical position modulates the chroma channels in opposite directions. The triangle wave is generated by XOR-folding the lower bits of the Y phase counter — when bit 8 is low, the 8-bit value ramps up; when bit 8 is high, the XOR flips all bits, creating a descending ramp. This produces a smooth, repeating triangle that maps directly to screen position. The Intensity parameter acts as a bitwise AND mask on this triangle wave, which means it does not simply scale the amplitude — it quantizes and clips it in a digital, stepped fashion. At low Intensity values, only the most significant bits of the triangle wave pass through, producing coarse, staircase-like offset patterns. At high values, the full triangle shape appears. The frame counter adds a time-varying phase offset to the Y position, causing the triangle wave pattern to scroll vertically when Animate is enabled. Because the offset is applied equally and oppositely to U and V, the color shift is always complementary — pushing toward blue-yellow on one channel while pushing toward red-cyan on the other, producing the characteristic rainbow bands of CRT misconvergence.

---

## Parameter Reference

<img src={degauss_control_panel} alt="Videomancer front panel with Degauss loaded"/>
*Videomancer's front panel with Degauss active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Intensity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the amplitude of the chroma offset applied to U and V channels. The VHDL implements this as a bitwise AND between the triangle wave modulator and the Intensity register, so the relationship is not a smooth linear scale — it is a digital masking operation that progressively enables more bits of the triangle wave signal. At 0%, the AND mask is zero and no offset is applied; the image passes through with its original color intact. At 100%, the full triangle wave amplitude drives the chroma offset, creating maximum rainbow fringing. Intermediate values produce stepped, quantized versions of the offset pattern.

---

#### Knob 2 — Frequency
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the spatial frequency of the triangle wave pattern along the vertical axis. At low values, the color fringing varies slowly from top to bottom of the screen — broad, gentle bands of hue shift. At high values, the pattern oscillates rapidly, producing many narrow rainbow stripes. This parameter modifies the effective wavelength of the vertical modulation, changing how many complete cycles of the triangle wave fit within the visible raster.

---

#### Knob 3 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the rate at which the animation phase accumulator advances per frame. At 0%, the rainbow pattern is stationary even when Animate is enabled (the accumulator increments by zero). At higher values, the pattern scrolls more rapidly, creating a smooth vertical drift of the color fringing bands. The visual effect resembles a degaussing coil being slowly swept past the screen — the rainbow interference pattern migrates from top to bottom in a hypnotic, continuous motion.

---

#### Knob 4 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial separation between the U and V channel offsets. At 50% (midpoint), the offsets are equal and opposite — symmetric complementary color fringing. Below 50%, the U offset dominates and the fringing shifts toward the blue-yellow axis. Above 50%, the V offset dominates and the fringing shifts toward the red-cyan axis. This parameter adjusts how evenly the chromatic displacement is distributed between the two chroma axes, controlling the overall color temperature of the fringing effect.

---

#### Knob 5 — Convergence
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Convergence adjusts how far the chroma offsets pull the U and V channels away from their neutral midpoint (512 in the 10-bit domain). At 50%, the offset is applied symmetrically around center. At lower values, the offset is biased toward convergence — the chroma channels are pulled back toward neutral, reducing the visible color fringing. At higher values, the offset is biased away from center, producing more extreme chromatic displacement. This mimics the convergence adjustment rings on the neck of a CRT — fine-tuning how well the three electron beams align.

---

#### Knob 6 — Saturation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies a post-offset saturation adjustment to the chroma channels. At 50%, the chroma signal passes through at unity gain after the offset is applied. Below 50%, the chroma channels are attenuated toward neutral gray, softening the rainbow effect into pastel tints. Above 50%, the chroma channels are amplified, intensifying the color fringing into vivid, saturated bands. This is useful for controlling the visual weight of the effect — subtle pastel washes versus aggressive, poster-like color streaks.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Radial** | Off | On |
| **9 — Horizontal** | Off | On |
| **10 — Persistent** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent binary options. Animate (7) enables or disables the frame-based phase scroll. Radial (8), Horizontal (9), and Persistent (10) modify the spatial character of the triangle wave modulation. Bypass (11) is a global output mux. These toggles can be combined freely — for example, enabling both Radial and Horizontal produces a pattern that varies across both screen axes simultaneously.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the processed signal and the unprocessed (delayed) input. Three parallel interpolator_u instances perform the blend — one for Y, one for U, one for V. At 0%, the output is the unprocessed input (no color fringing). At 100%, the output is the fully processed signal. Intermediate values produce a proportional blend, which is useful for dialing in subtle touches of color fringing without committing to the full effect. Because the Y channel passes through unmodified, the mix primarily affects the chroma — blending between original and offset U/V values.

---

## Guided Exercises

These exercises progress from static rainbow fringing to animated chromatic dissolution, exploring the interplay between intensity, spatial frequency, and animation.

### Exercise 1: Static Rainbow Fringing

<img src={degauss_exercise1_result} alt="Static Rainbow Fringing result"/>
*Static Rainbow Fringing — simulated result across source images.*
**Source**: A live camera feed or recorded footage with high-contrast edges — text on a dark background, architectural lines, or faces against a plain backdrop.

**Objective**: Learn how Intensity and Frequency interact to create position-dependent color fringing, and observe the characteristic rainbow banding of CRT misconvergence.

1. **Initial setup**: Set Intensity to about 40%. Observe the subtle color halos appearing on horizontal edges — blue-cyan on one side, red-yellow on the other.
2. **Increase Intensity**: Sweep Intensity from 40% up to 80%. Watch the rainbow bands widen and intensify. Note the stepped, digital quality of the offset at lower values versus the smooth triangle wave at higher values.
3. **Vary Frequency**: Sweep Frequency from low to high. At low values, the color shift varies slowly across the screen — broad washes of tint. At high values, many narrow rainbow stripes appear.
4. **Combine**: Set Intensity around 60% and Frequency around 50%. This produces a classic CRT misconvergence look — recognizable color fringing that varies smoothly from top to bottom.
5. **Check Y passthrough**: Toggle Bypass a few times. Note that brightness structure is identical in both states — only the color shifts.

**Key concepts**: Intensity controls offset amplitude via bitwise AND masking, Frequency controls the triangle wave spatial period, Y channel passes through unmodified, color fringing comes from opposite U/V offsets

---

### Exercise 2: Animated Degauss Sweep

<img src={degauss_exercise2_result} alt="Animated Degauss Sweep result"/>
*Animated Degauss Sweep — simulated result across source images.*
**Source**: Slow-moving or static footage — a still life, a landscape, or a color bar test pattern.

**Objective**: Explore the animation system and observe how the rainbow bands scroll through the image, recreating the visual experience of a degaussing coil sweep.

1. **Enable animation**: Turn Animate On. Set Speed to about 25% for a slow, gentle scroll.
2. **Observe the sweep**: The rainbow bands drift vertically through the image. With a color bar input, you can clearly see each band of color shift as it passes through.
3. **Increase Speed**: Sweep Speed from 25% to 75%. The scrolling accelerates from a stately drift to a rapid flutter.
4. **Add Horizontal**: Turn Horizontal On. The straight bands develop a diagonal or wavy character as X position contributes to the phase.
5. **Add Radial**: Turn Radial On (with or without Horizontal). The bands curve into circular arcs radiating from the screen center — this closely mimics the visual effect of waving a degaussing wand near the screen.
6. **Full sweep**: Set Intensity to about 70%, Speed to about 40%, and watch the complete degauss simulation — bands of saturated color washing smoothly across the image.

**Key concepts**: Frame counter adds time-varying phase, Speed controls accumulator rate, Horizontal adds X-axis variation, Radial produces circular field patterns

---

### Exercise 3: Chromatic Dissolution

<img src={degauss_exercise3_result} alt="Chromatic Dissolution result"/>
*Chromatic Dissolution — simulated result across source images.*
**Source**: Any footage with recognizable content — faces, objects, or scenes with a range of saturated and neutral areas.

**Objective**: Push all controls to extreme settings to dissolve the image into pure chromatic abstraction, then use Mix and Convergence to pull it back toward a usable artistic effect.

1. **Maximum fringing**: Set Intensity to 100%, Frequency to about 60%. The image should show strong, vivid rainbow bands.
2. **Boost Saturation**: Push Saturation above 70%. The rainbow bands intensify into solid, poster-like color stripes.
3. **Adjust Spread**: Sweep Spread from 0% to 100%. Watch the color axis tilt — the balance between blue-yellow and red-cyan fringing shifts.
4. **Convergence extremes**: Sweep Convergence from 0% to 100%. At low values, the fringing collapses back toward neutral; at high values, the offsets become more extreme.
5. **Mix back**: Now use the Mix fader to blend the processed signal with the dry input. At about 30-40%, you get a subtle chromatic haze layered over the original image — very useful for creating a "vintage monitor" aesthetic.
6. **Persistent trailing**: Turn Persistent On. The rainbow bands leave ghostly after-images as they scroll, creating a smeared, fluorescent trail effect.

**Key concepts**: Saturation amplifies chroma post-offset, Spread controls U/V balance, Convergence adjusts offset bias, Mix blends processed with dry, Persistent adds temporal trailing

---


## Tips

- **Intensity is a mask, not a gain**: Because the VHDL uses bitwise AND, low Intensity values produce stepped, quantized offsets rather than smoothly scaled small offsets. This gives the fringing a distinctly digital character at low settings.
- **Y is always clean**: The luminance channel passes through completely unprocessed. You can push Intensity to maximum and the brightness structure of the image remains perfectly intact — only the color shifts.
- **Complementary colors**: The opposite U/V offsets always produce complementary color fringing. You cannot get same-direction shifts on both channels — the rainbow bands always contain the full hue spectrum.
- **Mix for subtlety**: At 100% Mix and high Intensity, the effect is dramatic. Use Mix at 20-40% to layer subtle chromatic aberration over the original image for a "vintage monitor" look.
- **Animate for live performance**: With Speed at moderate values, the scrolling rainbow pattern is mesmerizing for live visuals. The pattern repeats every 1024 frames, but the slow drift makes each cycle feel organic.
- **Feedback loops**: Routing the output back to the input compounds the chroma offset on each pass, producing increasingly extreme rainbow banding that eventually saturates into solid color stripes.
- **Pair with Cascade or Cathode**: Degauss adds the color fringing of a misaligned CRT. Combine it with scanline effects (Cascade) or phosphor simulation (Cathode) for a complete CRT emulation chain.
- **Bypass for A/B**: Use Switch 11 to instantly compare the processed and unprocessed signals. Because Y is unchanged, the comparison highlights the chroma effect in isolation.

---

## Glossary

| Term | Definition |
|------|------------|
| **Aperture Grille** | A type of CRT shadow mask using vertical wires instead of holes, used in Trinitron displays; serves the same beam-selection function as a dot-mask. |
| **BT.601** | ITU-R Recommendation BT.601; the color encoding standard used in standard-definition video, defining the YUV matrix coefficients. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Chromatic Aberration** | An optical artifact where different wavelengths of light focus at different points, causing color fringing at edges. |
| **Clamp** | A limiting operation that constrains a value to a defined range (0–1023 in the 10-bit domain). |
| **Convergence** | The condition where all three electron beams in a CRT meet at the same point on the phosphor screen. |
| **Degaussing** | The process of demagnetizing a CRT shadow mask using an alternating magnetic field to restore color purity. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interpolator** | A hardware module that performs linear interpolation between two input values based on a mix parameter. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Misconvergence** | A CRT defect where the three electron beams fail to meet at the same phosphor dot, causing color fringing. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Shadow Mask** | A perforated metal sheet inside a CRT that ensures each electron beam strikes only its designated phosphor color. |
| **Triangle Wave** | A periodic waveform that ramps linearly up and then linearly down, generated here by XOR-folding a binary counter. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
