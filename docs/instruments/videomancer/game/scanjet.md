---
draft: true
sidebar_position: 259
slug: /instruments/videomancer/scanjet
title: "Scanjet"
image: /img/instruments/videomancer/scanjet/scanjet_hero.png
description: "The arcade boards of the mid-1980s — Sega's Hang-On, Out Run, and After Burner — achieved a convincing illusion of three-dimensional forward motion using a technique that never actually rendered a 3D scene."
---

import scanjet_hero from '/img/instruments/videomancer/scanjet/scanjet_hero.png';
import scanjet_control_panel from '/img/instruments/videomancer/scanjet/scanjet_control_panel.png';
import scanjet_exercise1_result from '/img/instruments/videomancer/scanjet/scanjet_exercise1_result.gif';
import scanjet_exercise2_result from '/img/instruments/videomancer/scanjet/scanjet_exercise2_result.gif';
import scanjet_exercise3_result from '/img/instruments/videomancer/scanjet/scanjet_exercise3_result.gif';

# Scanjet

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={scanjet_hero} alt="Scanjet hero image"/>
*Scanjet transforming live video into a pseudo-3D ground plane with perspective-scaled scanlines, sinusoidal road curvature, and retro sky rendering.*
---

## Overview

The arcade boards of the mid-1980s — Sega's Hang-On, Out Run, and After Burner — achieved a convincing illusion of three-dimensional forward motion using a technique that never actually rendered a 3D scene. Instead, they horizontally scaled each scanline of a flat 2D image by a factor inversely proportional to its distance from a vanishing point on the horizon. Scanlines near the horizon were compressed (zoomed out), and scanlines at the bottom of the screen were expanded (zoomed in), creating the visual impression of a ground plane receding into the distance. A sinusoidal per-scanline horizontal offset added road curvature, and a simple sky treatment filled the region above the horizon.

Scanjet implements this entire Super Scaler pipeline in real-time FPGA hardware. Any input video becomes the texture of a pseudo-3D ground plane, stretched and compressed scanline-by-scanline according to a perspective-correct scaling function. A 64-entry sine lookup table generates smooth road curvature that oscillates with configurable amplitude and frequency. Above the configurable horizon line, four sky rendering modes provide different treatments for the upper portion of the frame. The result transforms any flat video source — camera feeds, color bars, graphic patterns — into a convincing arcade-style ground plane racing toward the viewer.

At subtle settings with the horizon near the top of frame and gentle curvature, Scanjet adds a mild perspective tilt to the source. At extreme settings with a low horizon, heavy depth exaggeration, and strong curvature, it produces the full Out Run driving experience — the ground plane warps and bends beneath a configurable sky.

---

## Background

### Super Scaler Technology

Sega's Super Scaler arcade boards (1985–1992) were purpose-built hardware systems that achieved pseudo-3D graphics without any actual 3D rendering pipeline. The key innovation was per-scanline horizontal scaling: by varying the zoom factor of each horizontal line of pixels, a flat 2D sprite or background tile could be made to appear as a receding ground plane. The technique exploited the projective geometry principle that objects at greater distances subtend a smaller visual angle — closer scanlines should be wider (zoomed in) and distant scanlines should be narrower (zoomed out). Games like Hang-On (1985), Space Harrier (1985), Out Run (1986), and After Burner (1987) used this technique to create some of the most visually impressive arcade experiences of the era.

### DDA Perspective Scaling

Scanjet uses a Digital Differential Analyzer (DDA) to compute the source pixel address for each output pixel on each scanline. The DDA maintains a fixed-point accumulator that advances by a step size determined by the desired zoom ratio. For scanlines close to the horizon (far away), the step size is large — the DDA skips source pixels, compressing the line. For scanlines at the bottom of the screen (nearby), the step size is small — the DDA reads each source pixel multiple times, expanding the line. The step size is computed from the reciprocal of the distance-from-horizon, approximated via shift-based division into three distance zones (close, medium, far).

### Sine LUT Road Curvature

A 64-entry sine lookup table provides smooth S-curve road bending. For each scanline below the horizon, the LUT index is computed from the scanline's distance from the horizon multiplied by the Curve Freq parameter, plus a global phase offset. The sine value is then scaled by the Curve Amp parameter and the distance from horizon to produce a per-scanline horizontal pixel offset. Because the offset is modulated by distance, curves appear tighter near the horizon (where the road recedes) and wider near the bottom (where the road is close), matching the perspective geometry.

### Ping-Pong Line Buffers

The scanline scaling pipeline requires reading source pixels at different rates than they arrive in the input stream. Scanjet stores each incoming scanline in a line buffer (2048 × 30-bit packed YUV) and reads from the *previous* line's buffer while writing the *current* line. Two buffers alternate in a ping-pong arrangement: while buffer A receives the current scanline's input data, the DDA reads from buffer B (which holds the previous line), and vice versa. This double-buffering prevents read-write conflicts and ensures the DDA always has a complete scanline available for arbitrary-address reads.

### Sky Rendering Modes

Above the horizon, Scanjet provides four distinct sky treatments selectable via the Sky Mode control. Pass In mode passes the input video through unchanged — the sky region shows the original source. Solid mode fills the sky with a uniform brightness set by the Sky Bright knob, with neutral chrominance. Mirror mode reads from the line buffer as if the ground were reflected upward, creating a water-like or mirror-sky effect. Fade to Black mode creates a vertical gradient that fades from black at the top of the frame to the Sky Bright value at the horizon, simulating atmospheric perspective.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Line Buffer Write ──────────────────────────────────
│   └─ Pack Y/U/V into 30-bit word, write to current buffer
│      Ping-pong: swap buffer at each hsync
│
├── Stage 2: Perspective + Curve Calculation ────────────────────
│   ├─ dist = vcount − horizon_y  (if below horizon)
│   ├─ Scale zones: far (dist>>7≠0) → compressed
│   │                 mid (dist>>4≠0) → moderate
│   │                 near            → expanded
│   ├─ DDA step = f(depth, distance zone)
│   ├─ Sine LUT index = dist × curve_freq + curve_phase
│   └─ curve_offset = curve_amp × sine_val / distance
│
├── Stage 3: DDA Source Address + Line Buffer Read ──────────────
│   ├─ DDA accumulator: source_x += dda_step per pixel
│   ├─ Read address = source_x >> 10 + curve_offset
│   └─ Read from inactive buffer (previous scanline data)
│
├── Stage 4: Sky/Ground Gate + Ground Stripe ────────────────────
│   ├─ Above horizon: sky mode selection
│   │   ├─ "00" Pass In: output = input video
│   │   ├─ "01" Solid:   Y = sky_bright, U/V = 512
│   │   ├─ "10" Mirror:  output = line buffer read
│   │   └─ "11" Fade:    Y = sky_bright × vcount / 1024
│   ├─ Below horizon: output = scaled line buffer data
│   └─ Ground stripe: if enabled, dim alternating scanlines
│      (Y = Y × 0.75)
│
├── Interpolator (4 clk) ───────────────────────────────────────
│   └─ Mix: lerp(dry, wet, Mix fader)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical aspect of the pipeline is that the DDA operates on the *previous* scanline's data stored in the line buffer, not the current incoming scanline. This means the ground plane texture is always one line behind the live input, which is invisible at video rates but essential for the buffer architecture to avoid read/write conflicts. The perspective calculation, sine LUT lookup, and DDA stepping all happen in a single clock cycle (Stage 2), producing the read address for Stage 3 on the next clock. The curve phase advances once per frame (at vsync), creating the forward-motion illusion when Curve Speed is non-zero — the road appears to scroll toward the viewer as the sine pattern shifts.

---

## Parameter Reference

<img src={scanjet_control_panel} alt="Videomancer front panel with Scanjet loaded"/>
*Videomancer's front panel with Scanjet active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Horizon
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Sets the vertical position of the horizon line. At 0%, the horizon is at the top of the frame and nearly the entire screen is ground plane. At 100%, the horizon is at the bottom and nearly the entire screen is sky. The horizon value maps directly to a scanline number (0–1079 in HD). Below the horizon, perspective scaling is applied; above it, the selected sky mode determines the output. Moving the horizon dramatically changes the composition — a low horizon creates an expansive sky with a thin strip of ground; a high horizon creates a vast ground plane stretching toward a distant vanishing point.

---

#### Knob 2 — Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the perspective depth exaggeration factor. This parameter scales the DDA step size computation, determining how aggressively scanlines zoom as they approach or recede from the horizon. At low values, the perspective effect is gentle — scanline scaling varies gradually. At high values, scanlines near the horizon are extremely compressed while scanlines at the bottom are heavily expanded, creating an exaggerated sense of depth and speed. The depth value feeds into the three-zone shift-based reciprocal calculation that maps distance-from-horizon to zoom factor.

---

#### Knob 3 — Curve Amp
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the amplitude of the sinusoidal road curvature. At 0%, the road is perfectly straight — no horizontal offset is applied. As you increase the amplitude, each scanline below the horizon receives a horizontal pixel shift derived from the sine LUT. The shift is modulated by distance from the horizon, so curves appear tighter in the distance and wider near the viewer, matching perspective geometry. At maximum, the road bends dramatically from side to side.

---

#### Knob 4 — Curve Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the forward-motion scroll speed by setting the phase increment added to the sine oscillator's global phase at each vertical sync pulse. At 0%, the road curvature pattern is static — bends remain frozen in place. As you increase the speed, the sine pattern shifts forward each frame, creating the illusion that the ground is scrolling toward the viewer. Higher values produce faster apparent forward motion. The effect is most convincing when combined with moderate Curve Amp settings.

---

#### Knob 5 — Curve Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the frequency (tightness) of road bends by scaling the sine LUT index per scanline. At low values, bends are gentle and extend across many scanlines — the road curves lazily. At high values, the sine function cycles more rapidly, creating tighter, more frequent bends. The upper 6 bits of the register scale the distance-to-LUT-index mapping, giving a range from very gradual curves to rapid serpentine bends.

---

#### Knob 6 — Sky Bright
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the brightness of the sky region (above the horizon). In Solid sky mode, this sets the uniform Y value of the sky. In Fade to Black mode, this sets the maximum brightness at the horizon from which the fade-to-black gradient begins. In Pass In and Mirror modes, this parameter has no visible effect — those modes use input video or line buffer data respectively. The sky brightness uses neutral chrominance (U=512, V=512), producing a grayscale sky.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Sky Mode** | Pass In | Solid |
| **8 — Scale Mode** | Smooth | Nearest |
| **9 — Stereo** | Off | On |
| **10 — Gnd Stripe** | Off | On |
| **11 — Bypass** | Off | On |

The toggles control sky rendering mode (a 2-bit selector), interpolation quality, stereo pair generation, and ground stripe overlay. Sky Mode selects one of four sky treatments applied above the horizon. Scale Mode selects between interpolated and nearest-neighbor sampling (visible as smoother vs. blockier perspective scaling). Stereo creates a side-by-side view. Ground Stripe adds alternating-scanline dimming below the horizon for a checker-road effect. Bypass routes the input directly to output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet crossfade between the original unprocessed signal and the fully perspective-scaled output. At 0%, the output is entirely dry (original). At 100%, the output is entirely wet (processed). Intermediate values blend the two linearly. Partial mix values can create a translucent overlay effect where the perspective ground plane is partially visible over the source.

---

## Guided Exercises

These exercises progress from basic perspective scaling to full arcade-style forward motion, building familiarity with the DDA pipeline, road curvature, and sky rendering.

### Exercise 1: Static Ground Plane

<img src={scanjet_exercise1_result} alt="Static Ground Plane result"/>
*Static Ground Plane — simulated result across source images.*
**Source**: A repeating geometric pattern — color bars, a grid test pattern, or tiled graphics.

**Objective**: Understand basic perspective scaling and the relationship between horizon position and depth.

1. **Set horizon**: Turn Horizon to about 40% to place the vanishing point in the upper-middle of the frame.
2. **Observe scaling**: The source image stretches below the horizon — scanlines at the bottom are wider (zoomed in), and scanlines near the horizon are compressed (zoomed out).
3. **Adjust depth**: Sweep Depth from low to high. Low values create gentle perspective; high values create extreme foreshortening.
4. **Move horizon**: Sweep Horizon across its full range. Low values fill the screen with ground; high values fill it with sky.
5. **Enable ground stripe**: Toggle Gnd Stripe On. Alternating scanlines dim, creating visible horizontal banding.

**Key concepts**: Perspective scaling compresses distant scanlines and expands near ones, Horizon position divides the frame into sky and ground regions, Depth exaggeration controls how aggressively zoom varies with distance

---

### Exercise 2: Road Curvature

<img src={scanjet_exercise2_result} alt="Road Curvature result"/>
*Road Curvature — simulated result across source images.*
**Source**: A simple repeating pattern such as horizontal stripes or a single-color gradient so the curvature is clearly visible.

**Objective**: Explore the sine LUT road curvature system and forward-motion scrolling.

1. **Start with a straight road**: Set Horizon to about 35%, Depth to about 50%, and Curve Amp to 0%.
2. **Add curvature**: Slowly increase Curve Amp from 0% to about 50%. The road begins to bend left and right with a sinusoidal pattern.
3. **Tighten bends**: Increase Curve Freq from low to moderate. The road develops tighter, more frequent turns.
4. **Animate**: Set Curve Speed to about 25%. The road appears to scroll forward, with bends advancing toward the viewer.
5. **Full speed**: Increase Curve Speed further. The forward-motion illusion intensifies.
6. **Compare ground stripe**: Toggle Gnd Stripe On/Off while animating. The alternating stripe dramatically enhances the sense of speed.

**Key concepts**: Sine LUT provides smooth per-scanline curvature, Curve offset is modulated by distance for perspective-correct bending, Phase advance creates forward-motion illusion, Ground stripe enhances speed perception

---

### Exercise 3: Full Arcade Scene

<img src={scanjet_exercise3_result} alt="Full Arcade Scene result"/>
*Full Arcade Scene — simulated result across source images.*
**Source**: Live camera footage or richly textured video — the more detail, the more convincing the ground plane texture appears.

**Objective**: Combine all parameters to create a complete arcade-style driving scene with sky, ground, and animated curvature.

1. **Set the scene**: Horizon at about 38%, Depth at about 60%.
2. **Select sky**: Set Sky Mode to Fade Blk. Set Sky Bright to about 40%. The sky fades from black at the top to moderate brightness at the horizon.
3. **Add road**: Set Curve Amp to about 40%, Curve Freq to about 40%, Curve Speed to about 30%.
4. **Ground texture**: Enable Gnd Stripe for the classic arcade road look.
5. **Try Mirror sky**: Switch Sky Mode to Mirror. The ground plane appears reflected in the sky, creating a surreal symmetrical composition.
6. **Smooth vs Nearest**: Toggle Scale Mode between Smooth and Nearest. Nearest gives the authentic retro look; Smooth gives a cleaner video-art treatment.

**Key concepts**: Sky modes provide different upper-frame treatments, combining all parameters creates a complete pseudo-3D scene, Scale Mode choice defines the aesthetic style (retro vs. clean)

---


## Tips

- **Start with Curve Amp at 0%**: Learn the perspective scaling behavior with a straight road before adding curvature. This isolates the DDA pipeline.
- **Grid patterns reveal scaling clearly**: Feed a regular grid or stripe pattern to visualize exactly how each scanline is being zoomed. Organic video can obscure the perspective math.
- **Curve Freq × Curve Amp interact**: High frequency with high amplitude creates rapid, dramatic serpentine bends. High frequency with low amplitude creates subtle shimmer. Low frequency with high amplitude creates broad sweeping curves.
- **Ground Stripe enhances speed**: The alternating-scanline dimming dramatically increases the perception of forward motion, even at low Curve Speed settings. Always try toggling it for comparison.
- **Mirror mode creates surreal reflections**: Sky Mode Mirror can produce striking water-reflection effects, especially with live camera footage as the ground texture.
- **Nearest mode for authenticity**: Scale Mode Nearest produces the chunky, aliased look of original arcade hardware. Switch to Smooth for cleaner video art applications.
- **Feedback creates infinite tunnels**: Routing the output back to the input creates recursive perspective scaling — the ground plane appears to contain an infinite receding tunnel of the previous frame's output.
- **Horizon near the bottom for dramatic sky**: Setting Horizon to 80–90% creates a thin strip of ground at the bottom with a vast sky region — useful for sky-focused compositions.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources in the FPGA fabric. Scanjet uses 2 BRAMs for ping-pong line buffers storing packed 30-bit YUV scanline data. |
| **DDA** | Digital Differential Analyzer; an iterative algorithm that computes source pixel addresses by accumulating a step value per output pixel. Used for per-scanline perspective zoom. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware executing the video processing pipeline. |
| **IIR** | Infinite Impulse Response; a filter where output feeds back into input. Not used directly in Scanjet but referenced for comparison with Sabattier's Mackie line spread. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator. Referenced in the VHDL but not actively used in Scanjet's main pipeline. |
| **Line Buffer** | A memory storing one complete scanline of video (2048 × 30-bit words). Scanjet uses two in a ping-pong arrangement. |
| **Ping-Pong** | A double-buffering technique where two buffers alternate roles: one receives new data while the other provides data for reading. |
| **Pipeline** | Sequential processing stages. Scanjet uses 4 processing clocks + 4 interpolator clocks = 8 total. |
| **Sine LUT** | A 64-entry lookup table of signed 8-bit sine values used to generate smooth road curvature offsets. |
| **Super Scaler** | Sega's per-scanline horizontal scaling technology (1985–1992) that simulated 3D perspective using 2D sprite/background hardware. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
