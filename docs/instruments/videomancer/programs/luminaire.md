---
draft: true
sidebar_position: 182
slug: /instruments/videomancer/luminaire
title: "Luminaire"
image: /img/instruments/videomancer/luminaire/luminaire_hero_s1.png
description: "Every stage production needs a spotlight."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import luminaire_control_panel from '/img/instruments/videomancer/luminaire/luminaire_control_panel.png';
import luminaire_source1_field from '/img/instruments/videomancer/luminaire/luminaire_source1_field.png';
import luminaire_source2_dog from '/img/instruments/videomancer/luminaire/luminaire_source2_dog.png';
import luminaire_source3_elephant from '/img/instruments/videomancer/luminaire/luminaire_source3_elephant.png';
import luminaire_source4_pattern from '/img/instruments/videomancer/luminaire/luminaire_source4_pattern.png';
import luminaire_source5_girl from '/img/instruments/videomancer/luminaire/luminaire_source5_girl.png';
import luminaire_source6_wood from '/img/instruments/videomancer/luminaire/luminaire_source6_wood.png';
import luminaire_hero_s1 from '/img/instruments/videomancer/luminaire/luminaire_hero_s1.png';
import luminaire_hero_s2 from '/img/instruments/videomancer/luminaire/luminaire_hero_s2.png';
import luminaire_hero_s3 from '/img/instruments/videomancer/luminaire/luminaire_hero_s3.png';
import luminaire_hero_s4 from '/img/instruments/videomancer/luminaire/luminaire_hero_s4.png';
import luminaire_hero_s5 from '/img/instruments/videomancer/luminaire/luminaire_hero_s5.png';
import luminaire_hero_s6 from '/img/instruments/videomancer/luminaire/luminaire_hero_s6.png';
import luminaire_ex1_s1 from '/img/instruments/videomancer/luminaire/luminaire_ex1_s1.png';
import luminaire_ex1_s2 from '/img/instruments/videomancer/luminaire/luminaire_ex1_s2.png';
import luminaire_ex1_s3 from '/img/instruments/videomancer/luminaire/luminaire_ex1_s3.png';
import luminaire_ex1_s4 from '/img/instruments/videomancer/luminaire/luminaire_ex1_s4.png';
import luminaire_ex1_s5 from '/img/instruments/videomancer/luminaire/luminaire_ex1_s5.png';
import luminaire_ex1_s6 from '/img/instruments/videomancer/luminaire/luminaire_ex1_s6.png';
import luminaire_ex2_s1 from '/img/instruments/videomancer/luminaire/luminaire_ex2_s1.png';
import luminaire_ex2_s2 from '/img/instruments/videomancer/luminaire/luminaire_ex2_s2.png';
import luminaire_ex2_s3 from '/img/instruments/videomancer/luminaire/luminaire_ex2_s3.png';
import luminaire_ex2_s4 from '/img/instruments/videomancer/luminaire/luminaire_ex2_s4.png';
import luminaire_ex2_s5 from '/img/instruments/videomancer/luminaire/luminaire_ex2_s5.png';
import luminaire_ex2_s6 from '/img/instruments/videomancer/luminaire/luminaire_ex2_s6.png';
import luminaire_ex3_s1 from '/img/instruments/videomancer/luminaire/luminaire_ex3_s1.png';
import luminaire_ex3_s2 from '/img/instruments/videomancer/luminaire/luminaire_ex3_s2.png';
import luminaire_ex3_s3 from '/img/instruments/videomancer/luminaire/luminaire_ex3_s3.png';
import luminaire_ex3_s4 from '/img/instruments/videomancer/luminaire/luminaire_ex3_s4.png';
import luminaire_ex3_s5 from '/img/instruments/videomancer/luminaire/luminaire_ex3_s5.png';
import luminaire_ex3_s6 from '/img/instruments/videomancer/luminaire/luminaire_ex3_s6.png';

# Luminaire

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Field", before: luminaire_source1_field, after: luminaire_hero_s1 },
    { label: "Dog", before: luminaire_source2_dog, after: luminaire_hero_s2 },
    { label: "Elephant", before: luminaire_source3_elephant, after: luminaire_hero_s3 },
    { label: "Pattern", before: luminaire_source4_pattern, after: luminaire_hero_s4 },
    { label: "Girl", before: luminaire_source5_girl, after: luminaire_hero_s5 },
    { label: "Wood", before: luminaire_source6_wood, after: luminaire_hero_s6 },
  ]}
/>
*Luminaire casting a warm radial glow across the video frame, simulating a stage spotlight with adjustable position and intensity.*

---

## Overview

Every stage production needs a spotlight. Luminaire places a virtual point light source on the video frame and adds a radial glow to everything within its reach. The light has a position, a radius, and an intensity — turn up the brightness, widen the circle, and move it wherever you want in the frame. The glow falls off linearly from the center and is additively blended with the source video, brightening everything it touches without clipping the dark areas.

The name *luminaire* is the technical term for a complete lighting unit — the lamp, the housing, the reflector, and the lens. In stage lighting, a luminaire is the thing that makes the light. Here it is a software luminaire: a point source rendered in real time on the FPGA, positioned by two knobs and shaped by radius and intensity. Flicker mode halves the brightness on alternating 4-frame cycles, producing a candle-like pulsation. Color mode tints the lit area warm (orange) or cool (blue), shifting the chroma within the glow region while leaving the rest of the image untouched.

Two knobs (Color and Falloff) and one toggle (Soft Edge) are registered in the VHDL but never actually referenced in the processing pipeline — they are vestigial parameters from an earlier design revision. The Animation toggle starts a frame counter, but the counter is not used for position modulation — flicker uses it, but the animate toggle itself has no visible effect beyond enabling the counter.

---

## Quick Start

1. **Diamond, not circle**: The glow shape is a diamond due to Manhattan distance. Embrace it — the angular shape is distinctive and gives Luminaire its geometric character.
2. **Intensity vs Radius**: Intensity sets the peak brightness; Radius sets how far the glow extends. Setting Intensity higher than Radius creates a saturated white core. Setting them equal creates a gradient that just reaches zero at the edge.
3. **Position X is offset**: The horizontal position has a +128 pixel offset in hardware. If the light seems shifted rightward from where you expect, this is why.

---

## Background

### Manhattan Distance and Diamond Shapes

Luminaire calculates the distance from each pixel to the light center using **Manhattan distance** (also called taxicab or L₁ distance): $d = |x - x_0| + |y - y_0|$. This is computationally cheap — just two absolute values and an addition, no multiplication or square root needed. The trade-off is that equidistant contours form diamond shapes instead of circles. A pure Manhattan-distance glow at a given radius produces a diamond-shaped bright region rotated 45° relative to the frame. This gives Luminaire its characteristic angular, faceted light shape rather than the smooth circles of Euclidean distance.

### Linear Falloff

The glow brightness is computed as $\text{glow} = \text{intensity} - \text{distance}$, clamped to zero. This is a simple linear falloff — brightness decreases by one unit per pixel of distance. Unlike inverse-square falloff (which is physically accurate for point light sources), linear falloff creates a predictable, even gradient from center to edge. The radius parameter sets the cutoff: pixels beyond the radius receive zero glow. The intensity parameter sets the peak brightness at the center. When intensity exceeds the radius, the glow saturates at the center and creates a flat bright core surrounded by a gradient ring.

### Additive Compositing

The glow is composited additively: $Y_\text{out} = Y_\text{in} + \text{glow}$, clamped to 1023. This means the light always brightens — it never darkens any part of the image. Dark areas of the source receive the glow at full value (since their Y is low), while already-bright areas may clip to maximum white. This is the same compositing model used in real-time graphics for light bloom and lens flare effects. The Mix fader interpolates between the dry (unlit) and wet (lit) signal through the standard 4-clock interpolator pipeline.

### Warm and Cool Color Tints

When the glow exceeds a threshold (128 on the 10-bit scale), Luminaire replaces the source chroma with a fixed tint. Warm mode sets U=448, V=640 — an orange-amber tone reminiscent of incandescent stage lighting. Cool mode sets U=640, V=384 — a blue-white tone suggesting moonlight or LED wash lights. The tint applies only within the visible glow region; outside it, the source chroma passes through unchanged. This creates a natural-looking pool of colored light.

### Frame Counter and Flicker

A 16-bit frame counter increments on each vsync when the Animate toggle is active. The Flicker toggle reads bit 2 of this counter, which toggles every 4 frames. When bit 2 is high, the glow brightness is halved via a right-shift by 1. The result is a regular on-off-on-off modulation at approximately 7.5 Hz (at 60 fps), creating a mechanical flicker effect. At 50 fps the rate shifts to approximately 6.25 Hz. The effect is regular rather than random — more metronome than candle — but at video rates the eye perceives it as a pulsating light.


---

## Signal Flow

Sync Edge Detection → Position Counters → Manhattan Distance → ... → Sync Delay Pipeline → Output Mux

```
Input Video (YUV 4:4:4)
│
├── Sync Edge Detection ────────────────────────────────────────
│   ├─ hsync_n falling edge → reset x_counter, increment y_counter
│   └─ vsync_n falling edge → reset y_counter, increment frame_counter
│
├── Position Counters ──────────────────────────────────────────
│   ├─ x_counter: free-running pixel counter (12-bit)
│   └─ y_counter: line counter (12-bit)
│
├── Manhattan Distance ─────────────────────────────────────────
│   ├─ dx = |x_counter − (Position X + 128)|
│   ├─ dy = |y_counter − Position Y|
│   └─ dist = dx + dy
│
├── Glow Falloff ───────────────────────────────────────────────
│   └─ glow = (dist < Radius) ? (Intensity − dist) : 0
│
├── Flicker Modulation ─────────────────────────────────────────
│   └─ if Flicker && frame_counter[2]: glow >>= 1
│
├── Additive Blend ─────────────────────────────────────────────
│   └─ Y_proc = clamp(Y_in + glow, 0, 1023)
│
├── Warm / Cool Tint ───────────────────────────────────────────
│   └─ if glow > 128:
│       ├─ Warm: U=448, V=640
│       └─ Cool: U=640, V=384
│
├── Interpolator Mix (3× interpolator_u, 4 clocks) ────────────
│   ├─ Y_out = lerp(Y_delayed, Y_proc, Mix)
│   ├─ U_out = lerp(U_delayed, U_proc, Mix)
│   └─ V_out = lerp(V_delayed, V_proc, Mix)
│
├── Sync Delay Pipeline (8 clocks) ─────────────────────────────
│   └─ hsync, vsync, field, Y, U, V delayed to match processing
│
└── Output Mux ─────────────────────────────────────────────────
    ├─ Bypass=0: interpolated mix output
    └─ Bypass=1: delayed input passthrough
```

The core processing is a single synchronous process that runs every pixel clock. Position counters track horizontal and vertical location by detecting sync edges — this is independent of the SDK's video_timing_generator and operates purely on hsync/vsync edge detection. The Manhattan distance computation, glow falloff, flicker, additive blend, and color tint all happen within the same process, producing a result with approximately 4 clocks of processing latency. The 8-clock delay pipeline aligns the dry signal with the interpolator output. The Position X register has a +128 pixel offset hardcoded in the VHDL distance calculation, shifting the light center rightward by 128 pixels relative to the raw register value.

---

## Parameter Reference

<img src={luminaire_control_panel} alt="Videomancer front panel with Luminaire loaded"/>
*Videomancer's front panel with Luminaire active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Position X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Horizontal position of the light center. The register value is scaled to 10-bit pixel coordinates and shifted rightward by 128 pixels in the VHDL. At 0%, the light sits 128 pixels from the left edge. At 100%, the light moves toward the right edge. Because the x_counter is 12-bit (0–4095 range), the light can be positioned anywhere across HD or SD frames. The +128 offset means the light never quite reaches the far left column of the frame.

---

#### Knob 2 — Position Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Vertical position of the light center. The register value maps directly to the line counter — no offset is applied. At 0%, the light sits at the top of the frame. At 100%, the light moves toward the bottom. For HD video at 1080 lines, the 10-bit register covers approximately the upper third of the frame; for SD video at 480/576 lines, the full height is addressable.

---

#### Knob 3 — Radius
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Glow radius — the Manhattan distance cutoff beyond which glow is zero. Larger values create a wider diamond-shaped light pool. The radius is compared against the 13-bit distance sum, so register values up to 1023 can cover a substantial portion of the frame. At zero, no glow is visible regardless of intensity. At maximum, the glow can extend across most of the visible frame from a centered position.

---

#### Knob 4 — Intensity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Peak glow brightness at the light center. The glow value at distance zero equals this register value directly. Higher intensity creates a brighter center and a steeper gradient to the edge. When intensity exceeds the radius, the center is saturated (glow clamps to intensity) and the effective bright core extends outward. When intensity is less than the radius, the glow never reaches full brightness even at the center.

---

#### Knob 5 — Color
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

This knob is labeled "Color" and its register value is captured in the VHDL, but the signal is never referenced in the processing pipeline. Adjusting this control has no effect on the output. It is a vestigial parameter from an earlier design.

---

#### Knob 6 — Falloff
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

This knob is labeled "Falloff" and its register value is captured in the VHDL, but the signal is never referenced in the processing pipeline. Adjusting this control has no effect on the output. A future revision could use this to switch between linear and inverse-square falloff curves.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Flicker** | Off | On |
| **9 — Color** | Warm | Cool |
| **10 — Soft Edge** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles occupy register 6, each reading a single bit. Animate (bit 0) enables the frame counter but has no direct visual effect unless Flicker is also active. Flicker (bit 1) halves glow brightness every 4 frames. Color (bit 2) selects warm or cool tint. Soft Edge (bit 3) is captured but unused in the processing pipeline. Bypass (bit 4) routes input directly to output, skipping all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry mix fader. Controls the interpolation between the delayed dry signal and the processed (lit) signal via three instances of the 4-clock interpolator. At 0%, output equals the dry input — no glow visible. At 100%, output equals the fully processed signal. Intermediate values create a partial glow effect, which is useful for subtly warming a scene without overwhelming the source video.





---

## Guided Exercises

These exercises progress from basic spotlight placement to animated lighting effects, exploring Luminaire's controls and their interactions.

### Exercise 1: Spotlight Placement

<BeforeAfterSlider
  sources={[
    { label: "Field", before: luminaire_source1_field, after: luminaire_ex1_s1 },
    { label: "Dog", before: luminaire_source2_dog, after: luminaire_ex1_s2 },
    { label: "Elephant", before: luminaire_source3_elephant, after: luminaire_ex1_s3 },
    { label: "Pattern", before: luminaire_source4_pattern, after: luminaire_ex1_s4 },
    { label: "Girl", before: luminaire_source5_girl, after: luminaire_ex1_s5 },
    { label: "Wood", before: luminaire_source6_wood, after: luminaire_ex1_s6 },
  ]}
/>
*Spotlight Placement — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a clearly identifiable subject — a person, an object, or a defined scene.

**What You'll Create**: Learn to position the spotlight and control its size and brightness to illuminate a specific area of the frame.

1. **Center the light**: Set Position X and Position Y to approximately 50%. A bright region should appear near the center of the frame.
2. **Adjust radius**: Start with Radius at about 30%. A small diamond-shaped glow appears. Slowly increase to 60% — the glow expands outward.
3. **Adjust intensity**: Start with Intensity at about 50%. The center is moderately bright. Push to 80% — the center saturates to white and the glow ring widens.
4. **Move the light**: Sweep Position X left and right. The spotlight tracks horizontally. Sweep Position Y to move it vertically.
5. **Diamond shape**: Notice that the glow boundary is diamond-shaped, not circular. This is the Manhattan distance characteristic. The diamond is oriented with vertices at top, bottom, left, and right.

**Key concepts**: Manhattan distance creates diamond-shaped equidistant contours, linear falloff produces an even gradient from center to edge, additive blending only brightens — never darkens — the source

---

### Exercise 2: Warm and Cool Stage Lighting

<BeforeAfterSlider
  sources={[
    { label: "Field", before: luminaire_source1_field, after: luminaire_ex2_s1 },
    { label: "Dog", before: luminaire_source2_dog, after: luminaire_ex2_s2 },
    { label: "Elephant", before: luminaire_source3_elephant, after: luminaire_ex2_s3 },
    { label: "Pattern", before: luminaire_source4_pattern, after: luminaire_ex2_s4 },
    { label: "Girl", before: luminaire_source5_girl, after: luminaire_ex2_s5 },
    { label: "Wood", before: luminaire_source6_wood, after: luminaire_ex2_s6 },
  ]}
/>
*Warm and Cool Stage Lighting — simulated result across source images.*
**Source**: A scene with neutral or mixed colors — skin tones, fabric, or architecture work well to show the color tint.

**What You'll Create**: Explore the warm and cool color tinting and how it interacts with the glow region.

1. **Establish spotlight**: Position X ~50%, Position Y ~50%, Radius ~50%, Intensity ~70%, Mix ~100%.
2. **Warm tint**: Set Color toggle to Warm. Observe the amber-orange tint within the glow area. Outside the glow, the source colors remain unchanged.
3. **Cool tint**: Flip Color to Cool. The glow shifts to blue-white. Compare the emotional quality — warm feels like indoor incandescent light, cool feels like moonlight.
4. **Threshold boundary**: Lower Intensity to about 40%. The tint boundary becomes visible as a sharp ring where glow crosses the 128 threshold. Inside: tinted. Outside: original chroma.
5. **Mix for subtlety**: Lower Mix to about 40%. The tint effect becomes more subtle — a gentle wash rather than a saturated overlay.

**Key concepts**: Chroma tinting applies only within the glow threshold region, the 128-level threshold creates a visible boundary between tinted and untinted areas, Mix fader controls the intensity of the entire effect

---

### Exercise 3: Flickering Light Source

<BeforeAfterSlider
  sources={[
    { label: "Field", before: luminaire_source1_field, after: luminaire_ex3_s1 },
    { label: "Dog", before: luminaire_source2_dog, after: luminaire_ex3_s2 },
    { label: "Elephant", before: luminaire_source3_elephant, after: luminaire_ex3_s3 },
    { label: "Pattern", before: luminaire_source4_pattern, after: luminaire_ex3_s4 },
    { label: "Girl", before: luminaire_source5_girl, after: luminaire_ex3_s5 },
    { label: "Wood", before: luminaire_source6_wood, after: luminaire_ex3_s6 },
  ]}
/>
*Flickering Light Source — simulated result across source images.*
**Source**: Dark or moody footage — a dimly lit scene accentuates the flicker effect.

**What You'll Create**: Create a flickering candle or torch-like lighting effect using the frame counter and flicker modulation.

1. **Establish spotlight**: Position the light with moderate radius and intensity (Radius ~40%, Intensity ~60%).
2. **Enable animation**: Turn on Animate (toggle 7) to start the frame counter.
3. **Enable flicker**: Turn on Flicker (toggle 8). The glow now alternates between full brightness and half brightness every 4 frames, creating a visible pulsation.
4. **Warm tint**: Set Color to Warm for a candle-flame aesthetic.
5. **Low mix**: Reduce Mix to about 50% to soften the flicker amplitude. The pulsation becomes a gentle breathing effect rather than a harsh on-off strobe.
6. **Move the light**: Slowly sweep Position X and Y while the flicker runs. The moving, flickering light creates an animated candlelight-on-wall effect.

**Key concepts**: Flicker mode halves brightness by right-shifting the glow value, the 4-frame cycle creates a regular pulsation at approximately 7.5 Hz, combining flicker with warm tint simulates incandescent or flame-based light sources

---


## Tips

- **Unused controls take up slots**: Color (pot 5), Falloff (pot 6), and Soft Edge (toggle 10) are wired but inert. Don't be confused when they do nothing — they are placeholders for a future revision.
- **Flicker needs Animate**: The flicker effect reads the frame counter, which only advances when Animate is on. Enable Animate before Flicker.
- **Warm tint for drama**: Warm mode (U=448, V=640) adds an amber-orange cast reminiscent of theatrical stage lighting. Use it to draw focus to a subject.
- **Low Mix for ambient light**: At Mix ~20–40%, the glow becomes a subtle ambient wash rather than a harsh spotlight — useful for gently warming a corner of the frame.
- **Feedback routing**: Sending Luminaire's output back to its input creates recursive additive brightness that rapidly saturates to white in the glow region, producing a blooming light effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Compositing** | Blending two signals by addition, where the result is always brighter than either input alone. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Falloff** | The rate at which glow brightness decreases with distance from the light center. Luminaire uses linear falloff. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Manhattan Distance** | Distance measured as the sum of absolute differences along each axis: $d = |x_1 - x_2| + |y_1 - y_2|$. Equidistant contours form diamonds. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage for brightness and contrast adjustment. |

---
