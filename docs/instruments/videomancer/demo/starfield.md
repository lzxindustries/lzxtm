---
draft: true
sidebar_position: 243
slug: /instruments/videomancer/starfield
title: "Starfield"
image: /img/instruments/videomancer/starfield/starfield_hero.png
description: "Program guide for Starfield, a Videomancer demo program for the LZX video synthesizer."
---

import starfield_animation from '/img/instruments/videomancer/starfield/starfield_animation.gif';
import starfield_control_panel from '/img/instruments/videomancer/starfield/starfield_control_panel.png';
import starfield_exercise1_result from '/img/instruments/videomancer/starfield/starfield_exercise1_result.gif';
import starfield_exercise2_result from '/img/instruments/videomancer/starfield/starfield_exercise2_result.gif';
import starfield_exercise3_result from '/img/instruments/videomancer/starfield/starfield_exercise3_result.gif';
import starfield_hero from '/img/instruments/videomancer/starfield/starfield_hero.png';

# Starfield

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={starfield_hero} alt="Starfield hero image"/>
*A perspective starfield streaming outward from a central vanishing point, with 32 register-based stars rendered at varying depths and brightnesses against a dimmed video background.*
<img src={starfield_animation} alt="Starfield animated output"/>
*Starfield output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

The starfield effect is one of the most immediately recognizable images in computing history. Before the World Wide Web, before multitasking operating systems, there was the Windows 3.1 Starfield screensaver — a simple perspective simulation where white dots streamed outward from the center of the screen, growing brighter and faster as they approached. It was millions of people's first encounter with the idea that a computer could generate something that looked like motion through three-dimensional space using nothing but arithmetic.

Starfield recreates that effect in dedicated FPGA hardware, maintaining 32 stars entirely in register fabric with zero BRAM. Each star has an X and Y offset from a configurable vanishing point and a Z depth counter. On every frame, Z decrements by a speed-dependent amount; when a star reaches Z=0, it respawns at maximum depth with new random coordinates seeded from a 16-bit LFSR. Screen position is computed by barrel-shifting X and Y by the high bits of Z, approximating perspective division with a simple shifter. Brightness is inversely proportional to depth — distant stars are dim points, nearby stars are bright flares. The result is a convincing parallax field that streams toward (or away from) the viewer.

Beyond the nostalgic recreation, Starfield offers creative controls that extend the original concept: a moveable vanishing point, optional star trails (3-pixel streaks), selectable star size (1×1 or 2×2), six hue tint regions, additive or replace compositing over a dimmed video background, and reversible direction. The effect is purely generative — it synthesizes imagery from scratch rather than processing an input signal.

---

## Background

### Perspective Projection and the Z-Divide

The fundamental principle behind a starfield display is perspective projection: objects farther from the viewer appear smaller and closer to the center of the visual field. In continuous mathematics, this is expressed as $x_{screen} = x_{world} / z$ and $y_{screen} = y_{world} / z$, where Z is the depth axis. On the iCE40 FPGA, true division is expensive, so Starfield approximates the Z-divide with a barrel shifter: the upper 3 bits of the 10-bit Z value select a shift amount (0–7), and the star's X/Y offsets are right-shifted by that amount. Close stars (low Z, shift=0) appear at their full offset from center; distant stars (high Z, shift=7) are shifted nearly to zero, clustering around the vanishing point. This produces the characteristic accelerating outward motion as stars approach.

### LFSR Random Number Generation

When a star reaches the end of its journey (Z=0 for outward motion, Z=max for inward), it must respawn at a new random position. Starfield uses a 16-bit Linear Feedback Shift Register (LFSR) to generate pseudo-random coordinates. An LFSR is a shift register whose input is a linear function (XOR) of its current state, producing a deterministic sequence that visits $2^{16}-1$ states before repeating. The LFSR runs continuously on every clock cycle, so each star that respawns captures a different snapshot of the sequence, producing apparently random positions. The seed value (0xBEEF) ensures a consistent starting state across power cycles.

### Register-Based State Storage

The 32-star state ($X$, $Y$, $Z$ per star = 96 words × 10–11 bits each) fits entirely in the FPGA's register fabric — no Block RAM required. This is unusual for a particle system: most implementations store state in memory arrays accessed through address/data ports. Register-based storage allows all 32 stars to be read simultaneously during rasterization (the brightness comparison loop), enabling a fully parallel per-pixel "which star is here?" test. The trade-off is silicon area: 32 register sets consume approximately 3000 flip-flops, but the iCE40 HX4K provides 3520, leaving headroom for the rest of the logic.

### Additive Compositing

When multiple luminous objects (stars) are rendered over a background, two compositing strategies are common. *Replace* mode overwrites the background — wherever a star pixel is drawn, the background is hidden. *Additive* mode sums the star brightness with the background, allowing both to be visible simultaneously. Additive compositing is physically motivated: real stars emit light that adds to whatever light is already present. In Starfield's additive mode, a bright star drawn over a dimmed video background results in a pixel brighter than either source alone, clamped at maximum white if the sum exceeds 1023.

### Star Trails and Motion Blur

Real-world cameras capture motion blur when bright objects move across the sensor during exposure. Starfield's trail feature simulates this by extending each star 2 pixels behind its current position along the same scanline, at half brightness. This creates a short streak that implies velocity, making the stars appear to be in motion rather than simply appearing and disappearing. The trail direction is always horizontal (trailing in the scan direction), which is a simplification but produces a convincing impression of streaking motion at video rates.


---

## Signal Flow

```
registers_in
│
├─ reg(0) → Warp Speed      (Z decrement per frame)
├─ reg(1) → Density          (active star count: 4..32 in steps of 4)
├─ reg(2) → Center X         (vanishing point H offset)
├─ reg(3) → Center Y         (vanishing point V offset)
├─ reg(4) → Star Hue         (colour tint selection)
├─ reg(5) → Bg Dim           (background video dimming)
├─ reg(6)(0) → Trails        (3-pixel streak)
├─ reg(6)(1) → Star Size     (1x1 / 2x2)
├─ reg(6)(2) → Direction     (outward / inward)
├─ reg(6)(3) → Composite     (additive / replace)
├─ reg(6)(4) → Bypass
└─ reg(7) → Mix

Video Input (YUV 4:4:4)
│
├─ LFSR16 Noise Generator (continuous, seed 0xBEEF)
│
├─ Timing Generator (hsync/vsync → h_count, v_count)
│
├─ Vanishing Point
│   ├─ origin_x = center_x + 448
│   └─ origin_y = center_y
│
├─ Star Update (vblank, 1 star per clock, 32 clocks)
│   ├─ speed = warp_speed >> 3 + 1
│   ├─ Outward: z -= speed; if z ≤ speed → respawn (LFSR X/Y, Z=max)
│   └─ Inward:  z += speed; if z ≥ max-speed → respawn (LFSR X/Y, Z=min)
│
├─ Rendering Pipeline (per pixel clock)
│   ├─ For each star i < active_stars:
│   │   ├─ shift_amt = z[9:7]              (barrel shift selector)
│   │   ├─ screen_x = origin_x + (star_x >> shift_amt)
│   │   ├─ screen_y = origin_y + (star_y >> shift_amt)
│   │   ├─ Match: screen == h_count, v_count
│   │   ├─ 2x2: also match +1 in both axes
│   │   ├─ Trail: match h_count+1, h_count+2 at half bright
│   │   └─ brightness = 1023 − z (closer = brighter)
│   └─ Select brightest matching star
│
├─ Background Dimming
│   ├─ bg_y = input_y × (1023 − bg_dim) >> 10
│   └─ bg_u/v = input (or neutral if bg_dim > 900)
│
├─ Colour Mapping + Compositing
│   ├─ Star hue: 6 tint regions based on star_hue register
│   ├─ Additive: bg + star (clamped at 1023)
│   └─ Replace:  star only (background hidden)
│
├─ Interpolator Mix (3× channels, 4 clk)
│   └─ mix = lerp(delayed_input, star_output, mix_amount)
│
├─ Sync Delay Pipeline (8-clock shift register)
│
└─ Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → input Y/U/V (no delay)
```

The star update runs during vertical blanking, processing one star per clock cycle across 32 cycles. This serial update is safe because rasterization only occurs during active video — the two processes never overlap. The LFSR runs continuously regardless of whether stars are being updated, which means the random coordinates captured at respawn time depend on the exact clock cycle at which each star expires. This produces apparently random spatial distribution despite the deterministic LFSR sequence.

The rendering pipeline performs a 32-way parallel comparison on every pixel clock: each star's projected screen position is compared against the current pixel coordinates. If multiple stars overlap, the brightest one wins (the `v_best_bright` accumulator). This approach avoids the need for a Z-buffer or scan-line sort — a luxury afforded by the small star count fitting entirely in registers.

---

## Parameter Reference

<img src={starfield_control_panel} alt="Videomancer front panel with Starfield loaded"/>
*Videomancer's front panel with Starfield active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Warp Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the speed at which stars move along the Z axis. The register value is right-shifted by 3 and incremented by 1 to produce the per-frame Z decrement. At 0%, stars barely crawl; at 100%, they rush toward (or away from) the viewer, with each star's lifetime lasting only a few frames before respawning. The visual impression is logarithmic — doubling the speed approximately doubles the apparent velocity of the star stream. Default is ~25%, giving a moderate warp-speed drift suitable for ambient backgrounds.

---

#### Knob 2 — Density
| Property | Value |
|----------|-------|
| Range | 4 – 32 |
| Default | 18 |

Controls how many of the 32 available stars are active, quantized to 8 density levels (4, 8, 12, 16, 20, 24, 28, 32 stars). At minimum, 4 stars produce a sparse field. At maximum, 32 stars fill the frame with a dense constellation. Inactive stars are simply skipped during both update and rendering, so reducing density saves no hardware resources — it changes only the visual density of the field. The stepped response ensures that each density level is visually distinct.

---

#### Knob 3 — Center X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Shifts the vanishing point horizontally. The register value (0–1023) is added to a fixed offset of 448 to produce the screen-space X origin. At centre (register 512), the vanishing point is at pixel 960 — the horizontal midpoint of a 1920-wide frame. Sweeping this control slides the convergence point left or right, causing all stars to stream toward or away from a shifted center. At extremes, the vanishing point moves near the left or right edge, creating an asymmetric perspective field.

---

#### Knob 4 — Center Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Shifts the vanishing point vertically. The register value (0–1023) maps directly to the screen-space Y origin. At centre (register 512), the vanishing point is at vertical pixel 512. This control works identically to Center X but on the vertical axis. Combined with Center X, it allows the vanishing point to be placed anywhere within the frame — matching the classic screensaver's centered origin is the default, but off-center origins create dramatic oblique perspective effects.

---

#### Knob 5 — Star Hue
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 180deg |
| Suffix | deg |

Selects the colour tint applied to all stars. The register value is divided into six regions of approximately 170 counts each, mapping to Red, Yellow-Green, White (neutral), Cyan, Blue, and Magenta tint zones. The tint is applied by offsetting U and V channels relative to neutral (512), with the offset magnitude proportional to star brightness. At White, stars are pure luminance with no colour cast. At other settings, the stars take on a consistent hue that intensifies as they brighten (approach the viewer). The tint does not vary per star — all stars share the same hue.

---

#### Knob 6 — Bg Dim
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the dimming of the background video. The input video luminance is multiplied by (1023 − bg_dim) / 1024. At 0%, the background is at full brightness (no dimming). At 100%, the background is pure black. Above approximately 88% (register > 900), the chroma channels are also forced to neutral gray, preventing colour bleed from the dimmed video. The default of ~75% produces a dark (but not black) background through which the input video is faintly visible, giving contextual depth to the star field.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Trails** | Off | On |
| **8 — Star Size** | 1x1 | 2x2 |
| **9 — Direction** | Outward | Inward |
| **10 — Composite** | Add | Replace |
| **11 — Bypass** | Off | On |

The five toggles control independent binary features with no interaction between them. Trails (toggle 7) adds horizontal pixel streaks. Star Size (toggle 8) doubles the rendered pixel size. Direction (toggle 9) reverses the Z-axis motion. Composite (toggle 10) selects additive vs replace blending. Bypass (toggle 11) overrides everything at the output mux. Each toggle independently modifies one aspect of the rendering without affecting the others.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the delayed input video (dry) and the composited starfield output (wet). At 0% (fader down), the output is the unprocessed input — no stars are visible. At 100% (fader up), the output is the full starfield composited over the dimmed background. Intermediate values create a semi-transparent overlay where stars appear ghosted over the original video. The crossfade operates independently on Y, U, and V channels via three interpolator_u instances.

---

## Guided Exercises

These exercises build from a static understanding of the perspective field through animated star streaming to creative compositing with video sources. Because Starfield is a generative synthesis program, each exercise produces output from scratch — allow a few seconds for stars to distribute across the depth range before evaluating the visual result.

### Exercise 1: Classic Screensaver

<img src={starfield_exercise1_result} alt="Classic Screensaver result"/>
*Classic Screensaver — simulated result across source images.*
**Objective**: Recreate the Windows 3.1 Starfield screensaver: white dots streaming outward from center against a black background.

1. **Set centre origin**: Center X at ~50%, Center Y at ~50%. The vanishing point should be near frame center.
2. **Maximum density**: Set Density to maximum (32 stars active).
3. **Moderate speed**: Set Warp Speed to ~25%. Stars should stream outward at a comfortable pace.
4. **White stars**: Set Star Hue to ~50% (neutral/white zone).
5. **Black background**: Set Bg Dim to ~100% (full dimming, background is black).
6. **No extras**: Trails Off, Star Size 1×1, Direction Outward, Composite Additive.
7. **Observe**: Watch stars spawn at the center as dim points and accelerate outward, brightening as they approach. Stars that reach the edge respawn at the center.
8. **Increase speed**: Push Warp Speed to ~80%. The field becomes a rushing tunnel of light.

**Key concepts**: Perspective projection via barrel shift approximates Z-divide, stars spawn at Z=max and advance to Z=min, brightness is inversely proportional to depth, LFSR provides pseudo-random spawn positions

---

### Exercise 2: Coloured Reverse Warp with Trails

<img src={starfield_exercise2_result} alt="Coloured Reverse Warp with Trails result"/>
*Coloured Reverse Warp with Trails — simulated result across source images.*
**Objective**: Explore reverse direction, colour tinting, and trail effects for a hyperspace-like visual.

1. **Reverse direction**: Toggle Direction to Inward. Stars now spawn at the edges and converge toward the center.
2. **Enable trails**: Toggle Trails On. Each star gains a short horizontal streak.
3. **Increase size**: Toggle Star Size to 2×2. Stars become more visible.
4. **Colour tint**: Set Star Hue to ~15% (red zone). Stars glow red.
5. **Fast speed**: Set Warp Speed to ~60%. The inward convergence is rapid.
6. **Dim background**: Set Bg Dim to ~90% for a near-black background with faint video ghosting.
7. **Try other hues**: Sweep Star Hue through all six tint regions. Note how the hue changes the mood — cyan feels cold, red feels energetic.
8. **Reduce density**: Lower Density to ~50% (about 16 stars). The field opens up, each star trail becoming individually visible.

**Key concepts**: Direction toggle reverses Z motion (inward = stars recede toward vanishing point), Trails add motion blur streaks, Star Size doubles visual weight, Star Hue maps to 6 tint regions via register value

---

### Exercise 3: PIP Starfield over Live Video

<img src={starfield_exercise3_result} alt="PIP Starfield over Live Video result"/>
*PIP Starfield over Live Video — simulated result across source images.*
**Objective**: Composite the starfield over live video using additive and replace modes, with the vanishing point offset for dramatic asymmetric perspective.

1. **Connect video**: Feed a live camera or recorded footage.
2. **Dim background lightly**: Set Bg Dim to ~50%. The input video is visible at half brightness.
3. **Offset vanishing point**: Set Center X to ~75%, Center Y to ~30%. Stars stream from the upper-right.
4. **Moderate stars**: Density ~75% (about 24 stars), Warp Speed ~35%.
5. **Blue tint**: Set Star Hue to ~80% (blue zone) for cold space-like stars.
6. **Additive test**: With Composite at Add, notice how stars illuminate the dimmed video — bright stars add to the scene.
7. **Replace test**: Toggle Composite to Replace. Stars now punch through the video — hard bright dots against the dim scene.
8. **Mix overlay**: Set Mix to ~70%. The starfield is semi-transparent, creating a ghostly overlay.

**Key concepts**: Additive compositing sums star and background (physically motivated), Replace compositing overwrites background, Mix fader controls overall opacity, offset vanishing point creates asymmetric perspective, bg_dim controls background visibility

---


## Tips

- **Start with low speed**: Warp Speed ~20–30% gives a gentle drift that lets you appreciate the perspective projection. High speeds produce a rushing tunnel effect.
- **Offset the vanishing point**: Moving Center X/Y away from the centre creates dramatic asymmetric perspectives — stars appear to stream from a corner or edge of the frame.
- **Trails for motion**: Enable Trails when speed is moderate or high for a convincing motion-blur effect. They are less useful at very low speeds where stars move slowly.
- **Additive for layering**: Additive compositing over a dimmed video source is the most visually rich mode — stars appear as luminous objects floating in front of the scene.
- **Bg Dim for mood**: Low Bg Dim (~30%) lets the video show through clearly; high Bg Dim (~90%) isolates the stars against near-blackness. Match to your composition needs.
- **2×2 for visibility**: On large displays or when viewed from a distance, switch to 2×2 mode — single-pixel stars can be hard to see at normal viewing distances.
- **Density for texture**: Low density (4–8 stars) creates a sparse, contemplative field. High density (28–32) fills the frame with a busy, energetic stream.
- **Reverse for retreat**: Inward direction creates the impression of retreating into the distance — useful for transitions or endings.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive compositing** | A blending mode where the luminance of the foreground (star) is added to the background, allowing both to contribute to the final pixel value. Values above 1023 are clamped to maximum white. |
| **Barrel shifter** | A digital circuit that shifts a binary value by a variable number of positions in a single clock cycle, used here to approximate perspective division. |
| **Compositing** | The process of combining multiple visual elements into a single output frame. |
| **DVE** | Digital Video Effects; historically, a dedicated hardware unit for video transforms. Starfield is not a DVE effect per se but uses similar compositing techniques. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the starfield rendering pipeline. |
| **LFSR** | Linear Feedback Shift Register; a deterministic pseudo-random number generator that produces a maximal-length sequence by XORing selected bits and feeding the result back to the input. |
| **Perspective projection** | The geometric transformation that maps 3D world coordinates to 2D screen coordinates by dividing X and Y by Z depth, causing distant objects to appear smaller and closer to the vanishing point. |
| **Rasterization** | The process of converting geometric primitives (here, star positions) into discrete pixel values for display. |
| **Vanishing point** | The screen-space position toward which all depth lines converge in a perspective projection — the point from which stars appear to emanate. |
| **YUV** | A colour model that separates luminance (Y) from two chrominance components (U and V), used throughout the Videomancer video pipeline. |
