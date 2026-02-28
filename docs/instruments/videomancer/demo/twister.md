---
draft: true
sidebar_position: 269
slug: /instruments/videomancer/twister
title: "Twister"
image: /img/instruments/videomancer/twister/twister_hero.png
description: "Program guide for Twister, a Videomancer demo program for the LZX video synthesizer."
---

import twister_animation from '/img/instruments/videomancer/twister/twister_animation.gif';
import twister_control_panel from '/img/instruments/videomancer/twister/twister_control_panel.png';
import twister_exercise1_result from '/img/instruments/videomancer/twister/twister_exercise1_result.gif';
import twister_exercise2_result from '/img/instruments/videomancer/twister/twister_exercise2_result.gif';
import twister_exercise3_result from '/img/instruments/videomancer/twister/twister_exercise3_result.gif';
import twister_hero from '/img/instruments/videomancer/twister/twister_hero.png';

# Twister

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={twister_hero} alt="Twister hero image"/>
*Twister rendering a helically twisted vertical bar with four-face shading, evoking the classic Amiga demoscene rotating column effect.*
<img src={twister_animation} alt="Twister animated output"/>
*Twister output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Twister is a pure synthesis program — it generates imagery from scratch, producing the iconic rotating bar effect that was a staple of Amiga and Atari ST demoscene productions in the late 1980s and early 1990s. A virtual vertical bar rotates around its central axis, with a helical per-scanline twist that makes the bar appear to writhe and coil. The rotation angle varies linearly down the screen, creating the illusion of a three-dimensional column being viewed through a perspective window.

The program uses a 256-entry quarter-wave sine lookup table to compute cosine and sine values for each scanline's rotation angle. These trigonometric values determine the apparent widths of the bar's front and side faces, and provide Lambert shading for a convincing cylindrical illusion. Four faces with distinct colors create the impression of a rotating square bar, and optional stripe patterns on the faces add visual complexity.

At conservative settings, Twister produces a gently undulating bar with smooth color transitions. At extreme twist and speed settings, the bar disintegrates into a frenzy of rapidly spinning, tightly coiled helical strips — a visual hallmark of the demoscene era.

---

## Background

### The Demoscene Twister

The twister effect was one of the defining visual tricks of the demoscene — a subculture of programmers who competed to create the most impressive real-time graphics within severe hardware constraints. On the Amiga 500, with its 7 MHz 68000 processor and limited blitter, rendering a convincing 3D rotating bar required creative use of precomputed lookup tables: a sine table for the rotation math, and a palette table for face colors. The vertical bar was chosen specifically because it could be rendered scanline-by-scanline — each horizontal line simply needed to know where the bar's edges fell and which face was visible, making it inherently compatible with raster-line rendering.

### Quarter-Wave Sine LUT

The VHDL implementation uses a 256-entry quarter-wave sine table to reconstruct full sine and cosine values for any 10-bit phase angle. A quarter-wave table exploits the symmetry of the sine function: the values for 0°–90° can generate all four quadrants by mirroring and negating. This reduces ROM usage to one-quarter of a full table while maintaining 9-bit amplitude resolution (0–511). Cosine is obtained by adding a 256-entry phase offset before lookup. The approach matches historical demoscene practice, where memory was precious and mathematical identities were exploited ruthlessly.

### Lambert Shading and Face Visibility

The bar's faces are shaded using a simplified Lambert model: the brightness of each face is proportional to the cosine of the angle between the face normal and the viewing direction. The front face receives brightness proportional to `|cos(θ)|`, giving it maximum brightness when facing the viewer. The side faces receive brightness proportional to `|sin(θ)|/2`, making them dimmer. This creates a convincing 3D cylindrical illusion despite the effect being rendered entirely in 2D — no z-buffer, no polygons, no rotation matrices.

### Helical Twist

The twist parameter adds a per-scanline phase increment to the base rotation angle. Each scanline sees a slightly different rotation, so the bar's orientation varies continuously from top to bottom of the screen. Small twist values create a gentle helical curve; large values create a tightly wound coil. The visual effect is that of a rigid bar being twisted like taffy — the front face transitions smoothly into the side face as the eye travels down the screen.

### Multi-Bar Arrangements

In dual-bar mode, a second bar is rendered at a fixed horizontal offset (400 pixels from center). The second bar shares the same rotation parameters but provides its own column classification and face determination. The two bars rotate in concert, creating a symmetrical composition reminiscent of columns flanking a doorway.


---

## Signal Flow

```
Per-Frame State ──────────────────────────────────────
│ global_angle += rot_speed >> 2
│ scroll_offset += y_scroll >> 2
│
Per-Scanline State ───────────────────────────────────
│ line_angle = global_angle + vcount * twist_rate >> 8
│ cos_val = cosine_lookup(line_angle)
│ sin_val = sine_lookup(line_angle)
│ abs_cos, abs_sin = |cos_val|, |sin_val|
│ front_half = bar_width * abs_cos >> 9
│ side_half = bar_width * abs_sin >> 9
│
├── Stage 1: Column Classification ───────────────────
│   ├─ dx = pixel_x - screen_center
│   ├─ Front face: dx in [-front_half, +front_half)
│   ├─ Left side:  dx in [-front_half-side_half, -front_half)
│   ├─ Right side: dx in [+front_half, +front_half+side_half)
│   ├─ 4-face mode: right side = face 3
│   └─ Double bar: repeat classification at center+400
│
├── Stage 2: Face Pattern + Shading ──────────────────
│   ├─ Palette lookup → face color (Y, U, V)
│   ├─ Stripe: if scroll_line bit 3 = 1, dim Y by half
│   ├─ Video face: front face uses input video YUV
│   └─ Lambert shading: face_y = face_y * shade >> 9
│
├── Stage 3: Brightness + Composite ──────────────────
│   ├─ On bar: pixel_y = pixel_y * brightness >> 10
│   └─ Off bar: black background (Y=0, U=512, V=512)
│
├── Mix Stage (4 clk interpolator_u × 3 channels) ───
│   └─ Crossfade between dry input and wet synthesis
│
├── Sync Delay Pipeline ──────────────────────────────
│   └─ 9-clock delay for sync alignment
│
└── Bypass Mux ───────────────────────────────────────
    └─ Select original input or synthesized output
```

The critical interaction is between the per-scanline angle computation and the column classification. The `line_angle` changes every scanline by `twist_rate`, so the cosine and sine values — and therefore the front and side face widths — vary continuously down the screen. This is what creates the twisting illusion: the bar appears to rotate as the eye moves vertically. The column classifier then uses these varying widths to determine which pixels belong to which face, and the Lambert shading provides depth cues by dimming side faces relative to the front.

The face color lookup uses a hardcoded 4-entry palette with fixed YUV values. The `face_hue` parameter is defined in the TOML but the VHDL palette is static — the hue control is reserved for future palette rotation. The stripe pattern operates on the vertical scrolling line counter, creating horizontal bands that dim every 8th line for visual texture.

---

## Parameter Reference

<img src={twister_control_panel} alt="Videomancer front panel with Twister loaded"/>
*Videomancer's front panel with Twister active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Rot Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the rotation speed — the angular velocity increment applied to the global phase accumulator each frame. At 0%, the bar is stationary. As the value increases, the bar rotates faster. The speed register's top 8 bits are used as the DDS increment, so the rotation rate is approximately proportional to the pot position. Very high speeds create a spinning blur effect where individual faces are no longer distinguishable.

---

#### Knob 2 — Twist Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the twist rate — the per-scanline phase increment that creates the helical deformation. At 0%, every scanline sees the same rotation angle and the bar appears as a straight vertical column. As twist increases, the angular difference between the top and bottom of the screen grows. High twist values create a tightly wound helix where the bar completes multiple full rotations across the screen height. The twist increment is scaled by `vcount * twist_rate >> 8`.

---

#### Knob 3 — Bar Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the bar width — the half-width of the virtual bar in pixels before foreshortening. The actual visible width of any face depends on the cosine or sine of the rotation angle multiplied by this value. Narrow bars create a thin column effect; wide bars fill more of the screen. The front face half-width is `bar_width * |cos|` and the side face half-width is `bar_width * |sin|`, both divided by 512.

---

#### Knob 4 — Y Scroll
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Sets the vertical scroll speed for the stripe pattern. When the Striped toggle is active, horizontal bands alternate between full and half brightness across the face. The Y Scroll parameter controls how fast these bands move vertically, creating a barber-pole or candy-cane scrolling texture on the bar's surface. The scroll offset accumulates the top 8 bits of this register each frame.

---

#### Knob 5 — Face Hue
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |
| Suffix | deg |

Face hue control — a polar parameter mapped from 0° to 360°. In the current VHDL implementation the face palette is hardcoded (four fixed face colors), so this parameter is reserved for future palette rotation or hue-shifting functionality. Adjusting it has no visible effect in the current hardware version.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Global brightness multiplier applied to all bar pixels in the composite stage. The product `pixel_y * brightness` is right-shifted by 10, so brightness register 1023 produces approximately full brightness and 0 produces black. Off-bar background pixels are always black (Y=0, U=512, V=512) regardless of this setting.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Faces** | 2 Face | 4 Face |
| **8 — Pattern** | Solid | Striped |
| **9 — Video Face** | Off | On |
| **10 — Double** | Single | Dual |
| **11 — Bypass** | Off | On |

Toggles 7–10 each control a single rendering option that changes the visual character of the twister. They are independent — each addresses a different aspect of the bar's appearance. Toggle 11 is the standard bypass switch.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade mix. At 100%, the output is the fully synthesized twister bar. At 0%, the output is the unprocessed input video. Intermediate values blend the bar over the source via three parallel interpolator_u instances. This allows the twister to be composited as a semi-transparent overlay on existing video content.

---

## Guided Exercises

These exercises explore the twister from simple rotation through helical twist to multi-bar compositions. Each builds on the previous, gradually engaging more visual parameters.

### Exercise 1: Basic Rotation

<img src={twister_exercise1_result} alt="Basic Rotation result"/>
*Basic Rotation — simulated result across source images.*
**Objective**: Observe a single vertical bar rotating smoothly with no twist, understanding how face widths change with the cosine/sine of the rotation angle.

1. **Single wide bar**: Set Bar Width to ~60%, Twist Rate to 0%, Rot Speed to ~30%.
2. **Observe face transitions**: Watch the front face expand and contract as the bar rotates. The side face width changes inversely.
3. **Speed up**: Increase Rot Speed to ~70%. The rotation becomes faster but the geometry remains the same.
4. **Four-face mode**: Toggle Faces to 4 Face. Four distinct colors now cycle through as the bar rotates. Notice how the right side gets its own color.
5. **Reduce width**: Set Bar Width to ~20%. The bar becomes a thin column. Observe how the side face nearly vanishes when it faces the viewer.

**Key concepts**: Cosine determines front face width, sine determines side face width, 4-face mode assigns distinct colors to all four quadrants, bar width scales the overall column size

---

### Exercise 2: Helical Twist

<img src={twister_exercise2_result} alt="Helical Twist result"/>
*Helical Twist — simulated result across source images.*
**Objective**: Add per-scanline twist to create the classic helical deformation and explore how twist rate affects the visual complexity.

1. **Start with basic rotation**: Rot Speed ~30%, Bar Width ~50%.
2. **Add gentle twist**: Set Twist Rate to ~20%. The bar begins to curve — the top and bottom face different directions.
3. **Increase twist**: Push Twist Rate to ~60%. The bar now completes nearly a full rotation across the screen height. The helical coil is clearly visible.
4. **Maximum twist**: Set Twist Rate to ~90%. Multiple rotations visible simultaneously — the bar disintegrates into rapidly alternating color bands.
5. **Add stripes**: Toggle Pattern to Striped. Horizontal bands scroll across the twisted surface, creating a barber-pole effect.
6. **Scroll speed**: Increase Y Scroll to ~50%. The stripes scroll faster, emphasizing the helical wrap.

**Key concepts**: Twist rate adds a per-scanline phase increment, higher twist creates tighter helical coils, stripe pattern interacts with twist to create barber-pole texture, scroll speed animates the stripe position

---

### Exercise 3: Dual Bar Composition

<img src={twister_exercise3_result} alt="Dual Bar Composition result"/>
*Dual Bar Composition — simulated result across source images.*
**Objective**: Create a multi-bar arrangement with video compositing, exploring the overlay and transparency capabilities.

1. **Enable dual bars**: Toggle Double to Dual. A second bar appears 400 pixels from center.
2. **Set moderate parameters**: Rot Speed ~25%, Twist Rate ~40%, Bar Width ~40%.
3. **Four faces**: Set Faces to 4 Face for maximum color variety across both bars.
4. **Enable video face**: Toggle Video Face On. The front faces now show the input video signal, while side faces show palette colors.
5. **Reduce brightness**: Set Brightness to ~60%. The Lambert shading becomes more dramatic as overall brightness decreases.
6. **Partial mix**: Pull Mix to ~70%. The bars become semi-transparent, blending with the source video behind them.

**Key concepts**: Dual mode renders a second bar at fixed offset, video face maps input to the front face only, brightness modulates after shading, mix controls overlay transparency

---


## Tips

- **Slow rotation reveals geometry**: Start with Rot Speed ~10–20% to clearly see the face transitions and understand the column classification before increasing speed.
- **Twist Rate is the signature control**: The twist is what distinguishes this from a simple rotating bar. Start gentle (~20%) and increase to discover the sweet spot where the helix is visible but not overwhelming.
- **Four faces for maximum drama**: 2-face mode is simpler, but 4-face mode produces a more dynamic color sequence during rotation — four distinct phases per revolution instead of two.
- **Video face for compositing**: Enable Video Face to use the twister bar as a shaped viewport into the source video. The rotating bar reveals and conceals the video in a rhythmic pattern.
- **Stripe + twist = barber pole**: The combination of horizontal stripes and helical twist creates a classic barber-pole illusion, especially effective with moderate twist rates around 30–40%.
- **Dual bars for symmetry**: The second bar at +400 pixels creates a symmetrical frame-like composition. Use with reduced bar width to avoid overlap.
- **Mix for overlay**: Use Mix at ~50–70% to blend the twister over source video, creating a semi-transparent 3D overlay effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R BT.601, the standard defining the YUV color encoding used throughout the Videomancer video pipeline. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by accumulating a phase increment per sample and using it to index a lookup table. |
| **Demoscene** | A computer art subculture focused on creating real-time audiovisual demonstrations within hardware constraints; originated in the 1980s on Amiga and Atari ST platforms. |
| **Face ID** | An integer (0–3) identifying which of the four faces of the virtual square bar is visible at a given pixel; determines color from the palette. |
| **Helical Twist** | A deformation that rotates a shape progressively along its vertical axis, creating a coiling or corkscrew appearance. |
| **Interpolator** | A linear crossfade unit that blends between two values based on a mix parameter, used for wet/dry blending. |
| **Lambert Shading** | A lighting model where surface brightness is proportional to the cosine of the angle between the surface normal and the light direction; produces convincing matte surface illumination. |
| **LUT** | Lookup Table; a precomputed array of values used to replace runtime computation, here a quarter-wave sine table with 256 entries. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Quarter-Wave** | A sine table optimization that stores only 0°–90° and reconstructs the remaining three quadrants using symmetry (mirror and negate). |
